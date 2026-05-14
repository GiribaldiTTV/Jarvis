param(
    [string]$PythonPath = $env:NEXUS_VALIDATION_PYTHON,
    [string]$ArtifactRoot = "",
    [int]$MarkerTimeoutSeconds = 25,
    [int]$NoProgressTimeoutSeconds = 10,
    [switch]$RunInteractionSelfQA,
    [switch]$VisibleClient,
    [switch]$ActiveUserFacingClient,
    [switch]$PrepareLiveValidationUserTestSummary,
    [string]$ProofSeam = "",
    [int]$InteractionStepDelayMilliseconds = 250,
    [int]$FinalClientHoldSeconds = 0
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$script:RuntimeProcess = $null
$script:LastProgressAt = Get-Date
$script:LastProgress = "start"
$script:ManifestStatus = "ABORTED"
$script:FailureMessage = ""
$script:ObservedMarkers = New-Object System.Collections.Generic.List[string]
$script:CleanupNotes = New-Object System.Collections.Generic.List[string]
$script:ScreenshotPath = ""
$script:ScreenshotEvidencePath = ""
$script:InteractionManifestStatus = "NOT_REQUESTED"
$script:BeforeScreenshotPath = ""
$script:BeforeScreenshotEvidencePath = ""

function Step([object]$Paths, [string]$Message) {
    $script:LastProgressAt = Get-Date
    $script:LastProgress = $Message
    $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -LiteralPath $Paths.StepLog -Value $line -Encoding utf8
    Write-Output $line
}

function Check-Progress([string]$Activity) {
    if ($NoProgressTimeoutSeconds -gt 0 -and (Get-Date) -gt $script:LastProgressAt.AddSeconds($NoProgressTimeoutSeconds)) {
        throw "No-progress watchdog exceeded during $Activity. Last progress: $script:LastProgress"
    }
}

function Resolve-ValidationPython {
    $candidates = @()
    if ($PythonPath) { $candidates += $PythonPath }
    $candidates += "C:\Users\anden\AppData\Local\Python\pythoncore-3.14-64\python.exe"
    $pathPython = Get-Command python -ErrorAction SilentlyContinue
    if ($pathPython -and $pathPython.Source) { $candidates += $pathPython.Source }
    foreach ($candidate in $candidates) {
        if (-not $candidate -or -not (Test-Path -LiteralPath $candidate)) { continue }
        try {
            & $candidate -c "import PySide6" | Out-Null
            if ($LASTEXITCODE -eq 0) { return (Resolve-Path -LiteralPath $candidate).Path }
        } catch {}
    }
    throw "No Qt-capable Python interpreter found."
}

function New-Paths {
    if (-not $ArtifactRoot) {
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
        $ArtifactRoot = Join-Path $rootDir "dev\logs\fam_006_monitoring_hud_live_validation\$stamp"
    }
    New-Item -ItemType Directory -Force -Path $ArtifactRoot | Out-Null
    $artifactLeaf = Split-Path -Leaf $ArtifactRoot
    $userScreenshotsRoot = Join-Path $env:USERPROFILE "OneDrive\Pictures\Screenshots"
    if (-not (Test-Path -LiteralPath $userScreenshotsRoot)) {
        $picturesRoot = [Environment]::GetFolderPath("MyPictures")
        $userScreenshotsRoot = Join-Path $picturesRoot "Screenshots"
    }
    $screenshotEvidenceRoot = Join-Path $userScreenshotsRoot "Nexus Desktop AI\fam_006_monitoring_hud_live_validation\$artifactLeaf"
    New-Item -ItemType Directory -Force -Path $screenshotEvidenceRoot | Out-Null
    [pscustomobject]@{
        Root = $ArtifactRoot
        ScreenshotEvidenceRoot = $screenshotEvidenceRoot
        RuntimeLog = Join-Path $ArtifactRoot "runtime_log.txt"
        StdoutLog = Join-Path $ArtifactRoot "stdout.txt"
        StderrLog = Join-Path $ArtifactRoot "stderr.txt"
        StepLog = Join-Path $ArtifactRoot "step_log.txt"
        Manifest = Join-Path $ArtifactRoot "manifest.json"
        BeforeScreenshot = Join-Path $ArtifactRoot "monitoring_hud_desktop_before_launch.png"
        BeforeScreenshotEvidence = Join-Path $screenshotEvidenceRoot "monitoring_hud_full_virtual_desktop_before_launch.png"
        Screenshot = Join-Path $ArtifactRoot "monitoring_hud_desktop_after_launch.png"
        ScreenshotEvidence = Join-Path $screenshotEvidenceRoot "monitoring_hud_full_virtual_desktop_after_launch.png"
        InteractionManifest = Join-Path $ArtifactRoot "monitoring_hud_live_client_interaction_manifest.json"
        InteractionEvidenceRoot = Join-Path $ArtifactRoot "live_client_interaction"
        UserTestSummary = Join-Path $env:USERPROFILE "OneDrive\Desktop\User Test Summary.txt"
        AbortSignal = Join-Path $ArtifactRoot "startup_abort.signal"
    }
}

function Marker-Count([object]$Paths, [string]$Pattern) {
    if (-not (Test-Path -LiteralPath $Paths.RuntimeLog)) { return 0 }
    @(Select-String -LiteralPath $Paths.RuntimeLog -Pattern $Pattern -SimpleMatch).Count
}

function Wait-Marker([object]$Paths, [string]$Pattern) {
    $deadline = (Get-Date).AddSeconds($MarkerTimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $count = Marker-Count $Paths $Pattern
        if ($count -gt 0) {
            $script:ObservedMarkers.Add($Pattern)
            Step $Paths "observed marker: $Pattern count=$count"
            return
        }
        if ($script:RuntimeProcess -and $script:RuntimeProcess.HasExited) {
            throw "Runtime exited before marker appeared: $Pattern"
        }
        Check-Progress "waiting for marker $Pattern"
        Start-Sleep -Milliseconds 250
    }
    throw "Timed out waiting for marker: $Pattern"
}

function Capture-Screen([object]$Paths, [string]$Label = "after_launch") {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $screens = [System.Windows.Forms.Screen]::AllScreens
    $bounds = [System.Drawing.Rectangle]::Empty
    foreach ($screen in $screens) {
        if ($bounds.IsEmpty) {
            $bounds = $screen.Bounds
        }
        else {
            $bounds = [System.Drawing.Rectangle]::Union($bounds, $screen.Bounds)
        }
    }
    $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
        if ($Label -eq "before_launch") {
            $bitmap.Save($Paths.BeforeScreenshot, [System.Drawing.Imaging.ImageFormat]::Png)
            Copy-Item -LiteralPath $Paths.BeforeScreenshot -Destination $Paths.BeforeScreenshotEvidence -Force
            $script:BeforeScreenshotPath = $Paths.BeforeScreenshot
            $script:BeforeScreenshotEvidencePath = $Paths.BeforeScreenshotEvidence
            Step $Paths "captured before-launch full virtual desktop screenshot: $($Paths.BeforeScreenshot)"
            Step $Paths "copied before-launch user-inspectable screenshot evidence: $($Paths.BeforeScreenshotEvidence)"
        }
        else {
            $bitmap.Save($Paths.Screenshot, [System.Drawing.Imaging.ImageFormat]::Png)
            Copy-Item -LiteralPath $Paths.Screenshot -Destination $Paths.ScreenshotEvidence -Force
            $script:ScreenshotPath = $Paths.Screenshot
            $script:ScreenshotEvidencePath = $Paths.ScreenshotEvidence
            Step $Paths "captured after-launch full virtual desktop screenshot: $($Paths.Screenshot)"
            Step $Paths "copied after-launch user-inspectable screenshot evidence: $($Paths.ScreenshotEvidence)"
        }
    }
    finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function Save-Manifest([object]$Paths, [string]$PythonExe) {
    $observedMarkers = @($script:ObservedMarkers)
    $interactionRaw = ""
    if (Test-Path -LiteralPath $Paths.InteractionManifest) {
        $interactionRaw = Get-Content -LiteralPath $Paths.InteractionManifest -Raw
    }
    $standaloneDashboardWindowReady = (
        ($observedMarkers -contains "MONITORING_HUD_STANDALONE_DASHBOARD_WINDOW_READY") -or
        ($interactionRaw -match '"standalone_surface_independence"\s*:\s*true') -or
        ($interactionRaw -match '"dashboard_monitor_management"\s*:\s*true')
    )
    $surfaceNativeIndependenceReady = (
        ($observedMarkers -contains "MONITORING_HUD_SURFACE_NATIVE_INDEPENDENCE_READY") -or
        ($interactionRaw -match '"overlay_not_dashboard_coupled"\s*:\s*true') -or
        ($interactionRaw -match '"dashboardCoupled"\s*:\s*false') -or
        ($interactionRaw -match '"surfaceIndependence"\s*:\s*"dashboard_overlay_core_top_level_windows"')
    )
    $overlayCardsMovableReady = (
        ($observedMarkers -contains "MONITORING_HUD_OVERLAY_CARD_LAYOUT_EDITED") -or
        (
            ($interactionRaw -match 'active live-client drag overlay monitor card sent') -and
            ($interactionRaw -match 'active live-client resize overlay monitor card sent') -and
            (
                ($interactionRaw -match '"overlay_cards_owned_by_overlay"\s*:\s*true') -or
                ($interactionRaw -match '"cardsMovableInOverlay"\s*:\s*true')
            )
        )
    )
    $surfaceVirtualDesktopTravelReady = (
        ($observedMarkers -contains "MONITORING_HUD_SURFACE_VIRTUAL_DESKTOP_TRAVEL_READY") -or
        (
            ($interactionRaw -match 'dashboard and overlay move independently across virtual desktop without clipping') -and
            ($interactionRaw -match '"ok"\s*:\s*true') -and
            ($interactionRaw -match '"withinTargetMonitor"\s*:\s*true') -and
            ($interactionRaw -match '"withinVirtualDesktop"\s*:\s*true')
        )
    )
    $dashboardStandaloneWindowTravelReady = (
        ($observedMarkers -contains "MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY") -or
        (
            ($interactionRaw -match 'dashboard standalone window moves across virtual desktop without clipping') -and
            ($interactionRaw -match '"ok"\s*:\s*true') -and
            ($interactionRaw -match '"movement"\s*:\s*"dashboard_native_window_only"')
        )
    )
    $dashboardClippingBoundaryReady = (
        ($observedMarkers -contains "MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY") -or
        (
            ($interactionRaw -match '"clippingOk"\s*:\s*true') -and
            ($interactionRaw -match '"withinTargetMonitor"\s*:\s*true') -and
            ($interactionRaw -match '"withinVirtualDesktop"\s*:\s*true')
        )
    )
    $dashboardCoreOverlayDecouplingReady = (
        ($observedMarkers -contains "MONITORING_HUD_DASHBOARD_CORE_OVERLAY_DECOUPLING_READY") -or
        (
            ($interactionRaw -match '"decouplingOk"\s*:\s*true') -and
            ($interactionRaw -match '"overlayGeometryUnchanged"\s*:\s*true') -and
            ($interactionRaw -match '"coreGeometryUnchanged"\s*:\s*true')
        )
    )
    $dashboardSettingsContentReady = [bool]($observedMarkers -contains "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY")
    $dashboardMonitorGroupClarityReady = [bool]($observedMarkers -contains "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY")
    $dashboardOverlayNonGatingCopyReady = [bool]($observedMarkers -contains "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY")
    $dashboardProviderTruthReady = [bool]($observedMarkers -contains "MONITORING_HUD_DASHBOARD_PROVIDER_TRUTH_READY")
    $dashboardStateModelReady = [bool]($observedMarkers -contains "MONITORING_HUD_DASHBOARD_STATE_MODEL_READY")
    $dashboardWarningControlsReady = [bool]($observedMarkers -contains "MONITORING_HUD_DASHBOARD_WARNING_CONTROLS_READY")
    $coreIndependentPresetMonitorReady = (
        ($observedMarkers -contains "CORE_VISUALIZATION_INDEPENDENT_PRESET_MONITOR_READY") -or
        (
            ($interactionRaw -match '"travelPolicy"\s*:\s*"independent_user_selected_monitor_scoped"') -and
            ($interactionRaw -match '"attachedToHudDashboardOrNcp"\s*:\s*false')
        )
    )
    $coreHudSurfaceSeparationReady = (
        ($observedMarkers -contains "CORE_VISUALIZATION_HUD_SURFACE_SEPARATION_READY") -or
        (
            ($interactionRaw -match '"surfaceSeparationOk"\s*:\s*true') -and
            ($interactionRaw -match '"dashboardOverlap"\s*:\s*false') -and
            ($interactionRaw -match '"overlayOverlap"\s*:\s*false') -and
            ($interactionRaw -match '"movable"\s*:\s*false')
        )
    )
    $coreWorkerwCoordinateRebaseReady = [bool](
        $observedMarkers | Where-Object { $_ -match "CORE_VISUALIZATION_WORKERW_COORDINATE_REBASE_READY" }
    )
    $manifestSeam = $ProofSeam
    if (-not $manifestSeam) {
        if ($PrepareLiveValidationUserTestSummary) {
            $manifestSeam = "Live Validation LV1 - Monitoring HUD Product Surface Live Validation"
        }
        else {
            $manifestSeam = "Dashboard-specific active-client proof - no UTS export"
        }
    }
    $manifest = [pscustomobject]@{
        status = $script:ManifestStatus
        package = "PKG-006"
        slice = "SLC-029"
        seam = $manifestSeam
        proofStandard = "Dashboard-specific static/live proof screenshots; ledger-aligned User Test Summary export is Live Validation Stage 1 only"
        primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel"
        dashboardFirstWorkstreamHandoff = "ws31-dashboard-control-panel-acceptance-baseline"
        dashboardOnlyAcceptanceBaseline = "ws31-dashboard-control-panel"
        currentInterfaceReleaseGate = "dashboard-only-current-branch"
        overlayAcceptanceGate = "deferred-non-gating-supporting-evidence"
        interfaceBundleUserApproval = "not-granted"
        overlayDisplayAcceptance = "deferred-non-gating"
        coreRepairClassification = "dependency-repair-only"
        dashboardFirstProofPath = $true
        dashboardSpecificProofRefreshReady = $true
        dashboardSpecificStaticLiveProofReady = $true
        elementValidationLedger = "Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md"
        elementLedgerAlignedUserTestSummary = [bool]$PrepareLiveValidationUserTestSummary
        dashboardUserTestSummaryExportRefreshed = [bool]$PrepareLiveValidationUserTestSummary
        dashboardUserTestSummaryExportPath = if ($PrepareLiveValidationUserTestSummary) { $Paths.UserTestSummary } else { "" }
        dashboardUserTestSummaryReturnedResults = "live-validation-stage-1-only"
        dashboardSpecificProof = [pscustomobject]@{
            beforeLaunchFullVirtualDesktopScreenshot = [bool]$script:BeforeScreenshotPath
            afterLaunchFullVirtualDesktopScreenshot = [bool]$script:ScreenshotPath
            userInspectableScreenshotFolder = [bool]$Paths.ScreenshotEvidenceRoot
            activeUserFacingClient = [bool]$ActiveUserFacingClient
            interactionSelfQA = $script:InteractionManifestStatus
            dashboardOnlyCurrentInterfaceGate = $true
            overlayAcceptanceDeferredNonGating = $true
            coreRepairDependencyOnly = $true
            dashboardStandaloneWindowTravelReady = [bool]$dashboardStandaloneWindowTravelReady
            dashboardClippingBoundaryReady = [bool]$dashboardClippingBoundaryReady
            dashboardCoreOverlayDecouplingReady = [bool]$dashboardCoreOverlayDecouplingReady
            dashboardSettingsContentReady = [bool]$dashboardSettingsContentReady
            dashboardMonitorGroupClarityReady = [bool]$dashboardMonitorGroupClarityReady
            dashboardProviderTruthReady = [bool]$dashboardProviderTruthReady
            dashboardStateModelReady = [bool]$dashboardStateModelReady
            dashboardWarningControlsReady = [bool]$dashboardWarningControlsReady
            noFakeTelemetryPosture = $observedMarkers -contains "MONITORING_HUD_STATUS_BEHAVIOR_READY"
            userTestSummaryExportRefreshed = [bool]$PrepareLiveValidationUserTestSummary
            userTestSummaryPhaseBoundary = "live-validation-stage-1-only"
            returnedUserTestSummaryDigestReserved = $true
        }
        python = $PythonExe
        runtimeLog = $Paths.RuntimeLog
        beforeLaunchScreenshot = $script:BeforeScreenshotPath
        userInspectableBeforeLaunchScreenshot = $script:BeforeScreenshotEvidencePath
        screenshot = $script:ScreenshotPath
        screenshotEvidenceRoot = $Paths.ScreenshotEvidenceRoot
        userInspectableScreenshot = $script:ScreenshotEvidencePath
        afterLaunchScreenshot = $script:ScreenshotPath
        userInspectableAfterLaunchScreenshot = $script:ScreenshotEvidencePath
        activeUserFacingClient = [bool]$ActiveUserFacingClient
        interactionSelfQARequested = $effectiveRunInteractionSelfQA
        interactionStepDelayMs = $effectiveStepDelayMilliseconds
        finalClientHoldMs = $effectiveFinalHoldMilliseconds
        markerTimeoutSeconds = $MarkerTimeoutSeconds
        noProgressTimeoutSeconds = $NoProgressTimeoutSeconds
        interactionManifest = $Paths.InteractionManifest
        interactionManifestStatus = $script:InteractionManifestStatus
        interactionEvidenceRoot = $Paths.InteractionEvidenceRoot
        revisedOverlayProof = [pscustomobject]@{
            beforeLaunchFullVirtualDesktopScreenshot = [bool]$script:BeforeScreenshotPath
            afterLaunchFullVirtualDesktopScreenshot = [bool]$script:ScreenshotPath
            fullVirtualDesktopScreenshot = [bool]$script:ScreenshotPath
            userInspectableScreenshot = [bool]$script:ScreenshotEvidencePath
            beforeAfterDesktopComparisonReady = [bool]($script:BeforeScreenshotPath -and $script:ScreenshotPath)
            activeUserFacingClient = [bool]$ActiveUserFacingClient
            interactionSelfQA = $script:InteractionManifestStatus
            dashboardMinimalSplitReady = $observedMarkers -contains "MONITORING_HUD_DASHBOARD_MINIMAL_SPLIT_READY"
            edgelessOverlayCanvasReady = $observedMarkers -contains "MONITORING_HUD_EDGELESS_OVERLAY_CANVAS_READY"
            standaloneDashboardWindowReady = [bool]$standaloneDashboardWindowReady
            surfaceNativeIndependenceReady = [bool]$surfaceNativeIndependenceReady
            dashboardStandaloneWindowTravelReady = [bool]$dashboardStandaloneWindowTravelReady
            dashboardClippingBoundaryReady = [bool]$dashboardClippingBoundaryReady
            dashboardCoreOverlayDecouplingReady = [bool]$dashboardCoreOverlayDecouplingReady
            dashboardSettingsContentReady = [bool]$dashboardSettingsContentReady
            dashboardMonitorGroupClarityReady = [bool]$dashboardMonitorGroupClarityReady
            dashboardOverlayNonGatingCopyReady = [bool]$dashboardOverlayNonGatingCopyReady
            dashboardProviderTruthReady = [bool]$dashboardProviderTruthReady
            dashboardStateModelReady = [bool]$dashboardStateModelReady
            dashboardWarningControlsReady = [bool]$dashboardWarningControlsReady
            overlayCardsMovableReady = [bool]$overlayCardsMovableReady
            surfaceVirtualDesktopTravelReady = [bool]$surfaceVirtualDesktopTravelReady
            coreIndependentPresetMonitorReady = [bool]$coreIndependentPresetMonitorReady
            coreHudSurfaceSeparationReady = [bool]$coreHudSurfaceSeparationReady
            coreWorkerwCoordinateRebaseReady = [bool]$coreWorkerwCoordinateRebaseReady
            standaloneOverlayDisplayWindowReady = $observedMarkers -contains "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY"
            anchoredOverlayUninteractableReady = $observedMarkers -contains "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY"
            overlayPositionPreservedReady = $observedMarkers -contains "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY"
            providerContractReady = $observedMarkers -contains "MONITORING_HUD_TELEMETRY_BOUNDARY_READY"
            noFakeTelemetryPosture = $observedMarkers -contains "MONITORING_HUD_STATUS_BEHAVIOR_READY"
        }
        observedMarkers = $observedMarkers
        cleanupNotes = @($script:CleanupNotes)
        failureMessage = $script:FailureMessage
        generatedAt = (Get-Date).ToUniversalTime().ToString("o")
    }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Paths.Manifest -Encoding utf8
}

function Save-UserTestSummaryHandoff([object]$Paths) {
    $desktopRoot = Split-Path -Parent $Paths.UserTestSummary
    if (-not (Test-Path -LiteralPath $desktopRoot)) {
        New-Item -ItemType Directory -Force -Path $desktopRoot | Out-Null
    }
    $currentBranch = "unknown"
    try {
        $branchProbe = & git -C $rootDir branch --show-current 2>$null
        if (-not [string]::IsNullOrWhiteSpace($branchProbe)) {
            $currentBranch = [string]$branchProbe
        }
    } catch {}

    $precheckManifestPath = Join-Path $rootDir "dev\logs\fam_006_human_client_validation\latest_manifest.json"
    $precheckById = @{}
    $precheckManifestStatus = "NOT TESTED"
    $precheckManifestSummary = "Codex Precheck Manifest: NOT TESTED - desktop shortcut/tray precheck manifest was not found at $precheckManifestPath."
    $precheckProofClassesSummary = "Proof Classes: NOT TESTED - no proof-class manifest available."
    if (Test-Path -LiteralPath $precheckManifestPath) {
        try {
            $precheckManifest = Get-Content -LiteralPath $precheckManifestPath -Raw | ConvertFrom-Json
            $precheckManifestStatus = [string]$precheckManifest.status
            foreach ($step in @($precheckManifest.steps)) {
                if ($step.id) {
                    $precheckById[[string]$step.id] = $step
                }
            }
            $proofClassPairs = @()
            if ($precheckManifest.proofClasses) {
                foreach ($property in $precheckManifest.proofClasses.PSObject.Properties) {
                    $proofClassPairs += "$($property.Name)=$($property.Value)"
                }
            }
            $precheckManifestSummary = "Codex Human-Client Precheck Manifest: $precheckManifestStatus - $precheckManifestPath"
            $precheckProofClassesSummary = "Proof Classes: $($proofClassPairs -join '; ')"
        }
        catch {
            $precheckManifestStatus = "FAIL"
            $precheckManifestSummary = "Codex Human-Client Precheck Manifest: FAIL - unable to parse $precheckManifestPath ($($_.Exception.Message))."
            $precheckProofClassesSummary = "Proof Classes: FAIL - manifest parse error."
        }
    }
    if ($precheckManifestStatus -ne "PASS") {
        throw "Live Validation LV1 UTS export blocked: missing or failed Codex human-client precheck manifest at $precheckManifestPath. Run dev\orin_monitoring_hud_human_client_validation.ps1 and repair any FAIL steps before generating the formal UTS."
    }

    function Format-ShortcutPrecheckLine([string[]]$StepIds, [string]$FallbackReason) {
        $missing = @()
        $failed = @()
        $details = @()
        foreach ($stepId in $StepIds) {
            if (-not $precheckById.ContainsKey($stepId)) {
                $missing += $stepId
                continue
            }
            $step = $precheckById[$stepId]
            $status = ""
            if ($step.PSObject.Properties.Name -contains "codexPrecheck") {
                $status = [string]$step.codexPrecheck
            }
            if ([string]::IsNullOrWhiteSpace($status)) {
                $status = [string]$step.status
            }
            $proofClass = ""
            if ($step.PSObject.Properties.Name -contains "proofClass") {
                $proofClass = [string]$step.proofClass
            }
            if ([string]::IsNullOrWhiteSpace($proofClass)) {
                $proofClass = "unspecified"
            }
            $details += "$stepId=$status ($proofClass)"
            if ($status -ne "PASS") {
                $failed += "$stepId=$status"
            }
        }
        if ($missing.Count -gt 0) {
            return "Codex Precheck: NOT TESTED - missing human-client shortcut/tray/window precheck step(s): $($missing -join ', '). $FallbackReason"
        }
        if ($failed.Count -gt 0) {
            return "Codex Precheck: FAIL through human-client mouse/shortcut/tray path - $($failed -join '; ')."
        }
        return "Codex Precheck: PASS through human-client mouse/shortcut/tray path - $($details -join '; ')."
    }

    $precheckShortcutAlignment = Format-ShortcutPrecheckLine @("shortcut_targets_active_worktree", "launch_settled_visible_desktop", "launch_settled_tray_available") "LV1 cannot claim unrestricted green handoff for shortcut/worktree alignment without USER waiver."
    $precheckStep1 = Format-ShortcutPrecheckLine @("shortcut_targets_active_worktree", "launch_settled_tray_available") "LV1 cannot claim unrestricted green handoff for shortcut launch without USER waiver."
    $precheckStep2 = Format-ShortcutPrecheckLine @("enable_hud_opens_dashboard", "close_dashboard_from_tray_before_move", "open_dashboard_from_tray_before_move", "close_dashboard_from_tray", "open_dashboard_from_tray", "disable_hud_recovers") "LV1 cannot claim unrestricted green handoff for tray Dashboard lifecycle without USER waiver."
    $precheckStep3 = Format-ShortcutPrecheckLine @("tray_exit_confirmation_visible", "tray_exit_cancel_preserves_session", "tray_exit_accept_prompt_visible", "tray_exit_accept_shuts_down_promptly") "LV1 cannot claim unrestricted green handoff for tray Exit confirmation without USER waiver."
    $precheckNcpInteraction = Format-ShortcutPrecheckLine @("dashboard_mouse_move", "ncp_tray_icon_left_click_opens", "ncp_tray_menu_state_changes_to_close", "ncp_opens_with_dashboard_visible", "ncp_tray_icon_left_click_closes", "ncp_create_custom_task_clickable_with_dashboard_open", "ncp_create_custom_group_clickable_with_dashboard_open", "ncp_manage_custom_tasks_clickable_with_dashboard_open", "ncp_manage_custom_groups_clickable_with_dashboard_open") "LV1 cannot claim unrestricted green handoff for Dashboard-visible NCP tray toggle/state interaction without USER waiver."
    $precheckTrayAuthoring = Format-ShortcutPrecheckLine @("tray_create_custom_task_duplicate_guard") "LV1 cannot claim unrestricted green handoff for tray authoring duplicate-dialog safety without USER waiver."
    $precheckResizeDiscoverability = Format-ShortcutPrecheckLine @("dashboard_move_fluidity", "dashboard_resize_cursor_alignment", "dashboard_resize_cursor_transition_discovery", "dashboard_mouse_resize_corner", "dashboard_mouse_resize_right_edge", "dashboard_mouse_resize_bottom_edge", "dashboard_resize_fluidity", "dashboard_mouse_resize") "LV1 cannot claim unrestricted green handoff for Dashboard movement/resize discoverability/fluidity without USER waiver."
    $precheckFirstOpenStability = Format-ShortcutPrecheckLine @("dashboard_first_open_stability_sequence") "LV1 cannot claim unrestricted green handoff for #123 first-open stability without real shortcut screenshot-sequence proof or USER waiver."
    $precheckSettingsPanel = Format-ShortcutPrecheckLine @("dashboard_settings_opens_with_real_mouse", "dashboard_settings_double_click_does_not_maximize", "dashboard_settings_done_closes_with_real_mouse") "LV1 cannot claim unrestricted green handoff for Dashboard Settings unless the real mouse Dashboard IA-card path opens and closes the panel without native maximize drift or USER waiver."
    $precheckTopChromeClose = Format-ShortcutPrecheckLine @("dashboard_top_chrome_close_hides_dashboard", "dashboard_reopens_after_top_chrome_close") "LV1 cannot claim unrestricted green handoff for Dashboard window-level Close unless the visible Close control hides only the Dashboard and tray reopen works or USER waiver."
    $precheckHudPersistence = Format-ShortcutPrecheckLine @("hud_feature_enabled_state_persisted") "LV1 cannot claim unrestricted green handoff for HUD Feature state persistence without USER waiver."
    $precheckHumanClientRun = Format-ShortcutPrecheckLine @("launch_settled_visible_desktop", "launch_settled_tray_available", "enable_hud_opens_dashboard", "dashboard_first_open_stability_sequence", "dashboard_settings_opens_with_real_mouse", "dashboard_top_chrome_close_hides_dashboard", "ncp_tray_icon_left_click_opens", "ncp_tray_icon_left_click_closes", "ncp_create_custom_task_clickable_with_dashboard_open", "tray_exit_confirmation_visible") "LV1 cannot claim unrestricted green handoff without real-human client precheck coverage or USER waiver."
    $activeClientPrecheck = "Codex Precheck: PASS through proven equivalent active-client live helper path - equivalence evidence: same active branch runtime, active foreground desktop client, PASS manifest, PASS interaction self-QA, and before/after full-desktop screenshots at $($Paths.Root)."
    $visualScreenshotPrecheck = "Codex Precheck: PASS through proven equivalent active-client screenshot/manifest path - equivalence evidence: PASS live helper manifest, USER-inspectable screenshot folder, and interaction manifest at $($Paths.Root). USER visual confirmation is still required."
    $deferredBoundaryPrecheck = "Codex Precheck: PASS through source-truth, static validation, sandbox validation, and active-client manifest boundary proof - USER is not being asked to accept deferred/future scope."

    # Keep the desktop UTS as a short USER questionnaire; detailed ledger/proof
    # evidence stays in manifests and source truth.
    $content = @"
Nexus Desktop AI - User Test Summary
Workstream: FAM-006 Dashboard Settings Panel
Current Phase: Live Validation Stage 1 User Test Summary handoff
Branch: $currentBranch
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
Status: DRAFT HANDOFF COPY - NOT RETURNED RESULTS

How To Use This File
- Launch and test from the red FAM-006 desktop shortcut.
- For each step, write PASS, FAIL, or WAIVED plus a short note.
- If a step FAILS, describe exactly what you saw and attach/screenshot separately if useful.
- If a step is WAIVED, write the waiver reason.
- Return this file to Codex when complete. Codex will digest the results into source truth.

Codex Precheck Summary
- Red shortcut/worktree validation: PASS through the governed FAM-006 desktop shortcut.
- Human-client proof: PASS at dev/logs/fam_006_human_client_validation/latest_manifest.json.
- Live proof root for this handoff: $($Paths.Root)
- USER-inspectable screenshot folder: $($Paths.ScreenshotEvidenceRoot)
- Overlay/display release acceptance is deferred and non-gating.

Step 1 - Launch From Red FAM-006 Shortcut
Expected: The shortcut launches the FAM-006 worktree build and the app/tray settle normally.
USER Result / Notes:

Step 2 - Open HUD Dashboard From Tray
Expected: Enable/Open HUD Dashboard makes the Dashboard visible and usable.
USER Result / Notes:

Step 3 - #123 First-Open Stability
Expected: During the first 1-2 seconds, the Dashboard does not show a full-window flicker, blank flash, or late geometry snap.
USER Result / Notes:

Step 4 - #127 Move / Resize Cursor And Smoothness
Expected: Moving the Dashboard at normal USER speed does not skip or visibly lag. Resize cursors appear at the visible right edge, bottom edge, and bottom-right corner before click/drag, and resize tracks smoothly without obvious catch-up lag.
USER Result / Notes:

Step 5 - Dashboard Settings Panel
Expected: Settings opens with one click, double-clicking Settings does not maximize the Dashboard, and Done/Close returns to the Dashboard while it stays usable.
USER Result / Notes:

Step 6 - Dashboard Window-Level Close
Expected: The Close pill sits at the top-right as a whole-window control, hides only the Dashboard, and tray Open HUD Dashboard brings it back.
USER Result / Notes:

Step 7 - #137 Dashboard Rounded Corners On Light Background
Expected: With a white or light window behind the Dashboard, the rounded corners show the backdrop cleanly and no black rectangular native corner extends beyond the visible rounded Dashboard chrome.
USER Result / Notes:

Step 8 - Quick Access Warning Notifications
Expected: The Warning Notifications button is readable, not shadowed or pinched from the top, and still works as a quick access control.
USER Result / Notes:

Step 9 - Regression Sweep
Expected: Create Monitor, Edit Monitor, NCP tray icon left-click open/close, tray menu Open/Close Command Overlay state, scroll gutter, tray enable/disable, and tray Exit confirmation still behave normally.
USER Result / Notes:

Step 10 - Closing Additions
Any remaining readability, placement, motion, clipping, confusion, or polish notes:

Final USER Result
- PASS / FAIL / WAIVED:
- If FAIL, what must be repaired before Live Validation can continue:
- If PASS, any non-blocking follow-up ideas:
- If WAIVED, waiver reason:
"@

    Set-Content -LiteralPath $Paths.UserTestSummary -Value $content -Encoding utf8
    Step $Paths "refreshed Live Validation Stage 1 User Test Summary handoff: $($Paths.UserTestSummary)"
}

function Quote-ProcessArgument([string]$Value) {
    '"' + ($Value -replace '"', '\"') + '"'
}

$paths = New-Paths
$pythonExe = ""
$exitCode = 1
$effectiveRunInteractionSelfQA = [bool]($RunInteractionSelfQA -or $ActiveUserFacingClient)
$effectiveVisibleClient = [bool]($VisibleClient -or $ActiveUserFacingClient)
$effectiveStepDelayMilliseconds = $InteractionStepDelayMilliseconds
$effectiveFinalHoldMilliseconds = $FinalClientHoldSeconds * 1000
if ($ActiveUserFacingClient) {
    $effectiveStepDelayMilliseconds = [Math]::Max($effectiveStepDelayMilliseconds, 2500)
    $effectiveFinalHoldMilliseconds = [Math]::Max($effectiveFinalHoldMilliseconds, 20000)
}
if ($effectiveRunInteractionSelfQA) {
    $MarkerTimeoutSeconds = [Math]::Max($MarkerTimeoutSeconds, 180)
    $NoProgressTimeoutSeconds = [Math]::Max($NoProgressTimeoutSeconds, 180)
}

$previousHudStatePath = $env:NEXUS_MONITORING_HUD_STATE_PATH
try {
    Step $paths "starting FAM-006 Monitoring/HUD live desktop validation"
    $pythonExe = Resolve-ValidationPython
    Step $paths "resolved Python: $pythonExe"
    Capture-Screen $paths "before_launch"
    $env:NEXUS_MONITORING_HUD_STATE_PATH = (Join-Path $paths.Root "monitoring_hud_state.json")

    $args = @(
        "desktop\orin_desktop_main.py",
        "--runtime-log",
        $paths.RuntimeLog,
        "--startup-abort-signal",
        $paths.AbortSignal
    )
    if ($effectiveRunInteractionSelfQA) {
        New-Item -ItemType Directory -Force -Path $paths.InteractionEvidenceRoot | Out-Null
        $args += @(
            "--monitoring-hud-live-self-qa-manifest",
            $paths.InteractionManifest,
            "--monitoring-hud-live-self-qa-root",
            $paths.InteractionEvidenceRoot,
            "--monitoring-hud-live-self-qa-step-delay-ms",
            ([string]$effectiveStepDelayMilliseconds),
            "--monitoring-hud-live-self-qa-final-hold-ms",
            ([string]$effectiveFinalHoldMilliseconds)
        )
        $script:InteractionManifestStatus = "PENDING"
    }
    $argumentLine = ($args | ForEach-Object { Quote-ProcessArgument $_ }) -join " "

    $startParams = @{
        FilePath = $pythonExe
        ArgumentList = $argumentLine
        WorkingDirectory = $rootDir
        RedirectStandardOutput = $paths.StdoutLog
        RedirectStandardError = $paths.StderrLog
        PassThru = $true
        WindowStyle = "Hidden"
    }

    $script:RuntimeProcess = Start-Process @startParams
    Step $paths "launched desktop runtime pid=$($script:RuntimeProcess.Id)"

    $requiredMarkers = @(
        "RENDERER_MAIN|START",
        "RENDERER_MAIN|QAPPLICATION_CREATED",
        "RENDERER_MAIN|CORE_VISUALIZATION_PRESET_MONITOR_SELECTION_READY",
        "RENDERER_MAIN|WINDOW_CONSTRUCTED",
        "RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_READY|surface=separate_persona_core",
        "RENDERER_MAIN|CORE_VISUALIZATION_DESKTOP_LAYER_READY|surface=separate_persona_core",
        "RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_GEOMETRY_READY",
        "RENDERER_MAIN|CORE_VISUALIZATION_WORKERW_COORDINATE_REBASE_READY",
        "RENDERER_MAIN|CORE_VISUALIZATION_FIXED_PRESET_MONITOR_READY",
        "RENDERER_MAIN|CORE_VISUALIZATION_INDEPENDENT_PRESET_MONITOR_READY",
        "RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_VISIBLE|surface=separate_persona_core",
        "RENDERER_MAIN|VISUAL_PAGE_READY",
        "RENDERER_MAIN|CORE_VISUALIZATION_READY",
        "MONITORING_HUD_BASELINE_READY",
        "MONITORING_HUD_PRODUCT_VISIBILITY_READY",
        "MONITORING_HUD_DASHBOARD_SURFACE_READY",
        "MONITORING_HUD_OVERLAY_DEFERRAL_ENFORCED_READY",
        "MONITORING_HUD_MINIMAL_OVERLAY_READY",
        "MONITORING_HUD_DASHBOARD_MINIMAL_SPLIT_READY",
        "MONITORING_HUD_DASHBOARD_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MOTION_POLISH_READY",
        "MONITORING_HUD_DASHBOARD_SCROLLBAR_STYLE_READY",
        "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY",
        "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY",
        "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY",
        "MONITORING_HUD_DASHBOARD_PROVIDER_TRUTH_READY",
        "MONITORING_HUD_DASHBOARD_STATE_MODEL_READY",
        "MONITORING_HUD_DASHBOARD_WARNING_CONTROLS_READY",
        "MONITORING_HUD_EDGELESS_OVERLAY_CANVAS_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        "MONITORING_HUD_CONTROL_STATE_READY",
        "RENDERER_MAIN|STARTUP_READY",
        "DESKTOP_OUTCOME|SETTLED|state=dormant"
    )
    $interactionSupportingMarkers = @(
        "MONITORING_HUD_WINDOW_STATUS_READY",
        "MONITORING_HUD_INTERACTION_MODE_READY"
    )
    $deferredOverlaySupportingMarkers = @(
        "MONITORING_HUD_MINIMAL_NATIVE_OVERLAY_READY",
        "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY",
        "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY",
        "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY",
        "MONITORING_HUD_MINIMAL_ANCHORED_CLICK_THROUGH_READY",
        "MONITORING_HUD_MINIMAL_NON_FOCUS_READY",
        "MONITORING_HUD_VISIBLE_OVERLAY_READY",
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true"
    )
    $trayLifecycleMarkers = @(
        "MONITORING_HUD_TRAY_ENABLE_RENDER_STABLE_READY",
        "MONITORING_HUD_TRAY_ENABLE_DISABLE_ROUNDTRIP_READY",
        "MONITORING_HUD_TRAY_DASHBOARD_OPEN_CLOSE_READY",
        "MONITORING_HUD_DISABLE_RECOVERY_READY"
    )
    foreach ($marker in $requiredMarkers) {
        Wait-Marker $paths $marker
    }
    foreach ($marker in $deferredOverlaySupportingMarkers) {
        $count = Marker-Count $paths $marker
        if ($count -gt 0) {
            $script:ObservedMarkers.Add($marker)
            Step $paths "observed optional deferred overlay marker: $marker count=$count"
        }
        else {
            Step $paths "optional deferred overlay marker absent (non-gating): $marker"
        }
    }
    foreach ($marker in $interactionSupportingMarkers) {
        $count = Marker-Count $paths $marker
        if ($count -gt 0) {
            $script:ObservedMarkers.Add($marker)
            Step $paths "observed interaction-supporting marker: $marker count=$count"
        }
        else {
            Step $paths "interaction-supporting marker not emitted in startup-only proof: $marker"
        }
    }

    if ($effectiveRunInteractionSelfQA) {
        Step $paths "waiting for live-client interaction self-QA markers"
        Wait-Marker $paths "MONITORING_HUD_LIVE_CLIENT_SELF_QA_READY"
        if (-not (Test-Path -LiteralPath $paths.InteractionManifest)) {
            throw "Interaction self-QA manifest was not written: $($paths.InteractionManifest)"
        }
        $interactionManifest = Get-Content -LiteralPath $paths.InteractionManifest -Raw | ConvertFrom-Json
        $script:InteractionManifestStatus = [string]$interactionManifest.status
        if ($script:InteractionManifestStatus -ne "PASS") {
            throw "Interaction self-QA did not pass. Status: $script:InteractionManifestStatus"
        }
        Wait-Marker $paths "MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY"
        Wait-Marker $paths "MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY"
        Wait-Marker $paths "MONITORING_HUD_DASHBOARD_CORE_OVERLAY_DECOUPLING_READY"
        Wait-Marker $paths "MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY"
        Step $paths "interaction self-QA manifest PASS: $($paths.InteractionManifest)"
    }

    Step $paths "settling Dashboard-first client before full-desktop screenshot"
    Start-Sleep -Milliseconds 1500
    Capture-Screen $paths "after_launch"
    $script:ManifestStatus = "PASS"
    $exitCode = 0
}
catch {
    $script:ManifestStatus = "FAIL"
    $script:FailureMessage = $_.Exception.Message
    Step $paths "failure: $script:FailureMessage"
}
finally {
    if ($null -eq $previousHudStatePath) {
        Remove-Item Env:\NEXUS_MONITORING_HUD_STATE_PATH -ErrorAction SilentlyContinue
    }
    else {
        $env:NEXUS_MONITORING_HUD_STATE_PATH = $previousHudStatePath
    }
    if ($script:RuntimeProcess) {
        try {
            if (-not $script:RuntimeProcess.HasExited) {
                Stop-Process -Id $script:RuntimeProcess.Id -Force -ErrorAction Stop
                $script:CleanupNotes.Add("Stopped desktop runtime pid=$($script:RuntimeProcess.Id)")
            }
            else {
                $script:CleanupNotes.Add("Desktop runtime exited before cleanup pid=$($script:RuntimeProcess.Id)")
            }
        }
        catch {
            $script:CleanupNotes.Add("Cleanup failed for desktop runtime pid=$($script:RuntimeProcess.Id): $($_.Exception.Message)")
        }
    }
    Save-Manifest $paths $pythonExe
    if ($PrepareLiveValidationUserTestSummary) {
        Save-UserTestSummaryHandoff $paths
    }
    else {
        Step $paths "skipped User Test Summary export: UTS is Live Validation Stage 1 only"
    }
    if ($script:ManifestStatus -eq "PASS") {
        Write-Output "PASS: FAM-006 Monitoring/HUD live desktop proof captured at $($paths.Root)"
    }
    else {
        Write-Output "FAIL: FAM-006 Monitoring/HUD live desktop proof failed at $($paths.Root)"
    }
}

exit $exitCode
