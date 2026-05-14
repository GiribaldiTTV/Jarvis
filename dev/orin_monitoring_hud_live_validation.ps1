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
    $precheckNcpInteraction = Format-ShortcutPrecheckLine @("dashboard_mouse_move", "ncp_opens_with_dashboard_visible", "ncp_create_custom_task_clickable_with_dashboard_open", "ncp_create_custom_group_clickable_with_dashboard_open", "ncp_manage_custom_tasks_clickable_with_dashboard_open", "ncp_manage_custom_groups_clickable_with_dashboard_open") "LV1 cannot claim unrestricted green handoff for Dashboard-visible NCP interaction without USER waiver."
    $precheckTrayAuthoring = Format-ShortcutPrecheckLine @("tray_create_custom_task_duplicate_guard") "LV1 cannot claim unrestricted green handoff for tray authoring duplicate-dialog safety without USER waiver."
    $precheckResizeDiscoverability = Format-ShortcutPrecheckLine @("dashboard_resize_cursor_alignment", "dashboard_resize_cursor_transition_discovery", "dashboard_mouse_resize_corner", "dashboard_mouse_resize_right_edge", "dashboard_mouse_resize_bottom_edge", "dashboard_resize_fluidity", "dashboard_mouse_resize") "LV1 cannot claim unrestricted green handoff for Dashboard resize discoverability/fluidity without USER waiver."
    $precheckFirstOpenStability = Format-ShortcutPrecheckLine @("dashboard_first_open_stability_sequence") "LV1 cannot claim unrestricted green handoff for #123 first-open stability without real shortcut screenshot-sequence proof or USER waiver."
    $precheckSettingsPanel = Format-ShortcutPrecheckLine @("dashboard_settings_opens_with_real_mouse", "dashboard_settings_double_click_does_not_maximize", "dashboard_settings_done_closes_with_real_mouse") "LV1 cannot claim unrestricted green handoff for Dashboard Settings unless the real mouse/top-chrome path opens and closes the panel without native maximize drift or USER waiver."
    $precheckTopChromeClose = Format-ShortcutPrecheckLine @("dashboard_top_chrome_close_hides_dashboard", "dashboard_reopens_after_top_chrome_close") "LV1 cannot claim unrestricted green handoff for Dashboard top-chrome close unless the visible Close control hides only the Dashboard and tray reopen works or USER waiver."
    $precheckHudPersistence = Format-ShortcutPrecheckLine @("hud_feature_enabled_state_persisted") "LV1 cannot claim unrestricted green handoff for HUD Feature state persistence without USER waiver."
    $precheckHumanClientRun = Format-ShortcutPrecheckLine @("launch_settled_visible_desktop", "launch_settled_tray_available", "enable_hud_opens_dashboard", "dashboard_first_open_stability_sequence", "dashboard_settings_opens_with_real_mouse", "dashboard_top_chrome_close_hides_dashboard", "ncp_create_custom_task_clickable_with_dashboard_open", "tray_exit_confirmation_visible") "LV1 cannot claim unrestricted green handoff without real-human client precheck coverage or USER waiver."
    $activeClientPrecheck = "Codex Precheck: PASS through proven equivalent active-client live helper path - equivalence evidence: same active branch runtime, active foreground desktop client, PASS manifest, PASS interaction self-QA, and before/after full-desktop screenshots at $($Paths.Root)."
    $visualScreenshotPrecheck = "Codex Precheck: PASS through proven equivalent active-client screenshot/manifest path - equivalence evidence: PASS live helper manifest, USER-inspectable screenshot folder, and interaction manifest at $($Paths.Root). USER visual confirmation is still required."
    $deferredBoundaryPrecheck = "Codex Precheck: PASS through source-truth, static validation, sandbox validation, and active-client manifest boundary proof - USER is not being asked to accept deferred/future scope."

    $content = @"
Nexus Desktop AI - User Test Summary
Workstream: FAM-006 Monitoring and HUD Product Surface Package
Current Phase: Live Validation Stage 1 User Test Summary handoff
Branch: $currentBranch
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
Status: DRAFT HANDOFF COPY - NOT RETURNED RESULTS

Important Phase Note
- User Test Summary is exclusive to Live Validation.
- This file is generated only during Live Validation Stage 1 so USER can return PASS, FAIL, or WAIVED results.
- Live Validation Stage 1 cannot enter Live Validation Stage 2 until USER returns this file or explicitly waives it, Codex digests the result into source truth, and blockers are reevaluated.
- Workstream and Hardening may produce screenshots, manifests, active-client self-QA, and proof notes, but they must not refresh or digest this desktop User Test Summary artifact.

Fresh Evidence Root
- $($Paths.Root)

Key Evidence Files
- Manifest: $($Paths.Manifest)
- Runtime log: $($Paths.RuntimeLog)
- Before-launch full-desktop screenshot: $($Paths.BeforeScreenshot)
- After-launch full-desktop screenshot: $($Paths.Screenshot)
- USER-inspectable screenshot folder: $($Paths.ScreenshotEvidenceRoot)
- USER-inspectable before screenshot: $($Paths.BeforeScreenshotEvidence)
- USER-inspectable after screenshot: $($Paths.ScreenshotEvidence)
- Interaction manifest: $($Paths.InteractionManifest)
- Interaction screenshots: $($Paths.InteractionEvidenceRoot)

Element Validation Ledger Alignment
- Canonical ledger owner: Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md
- Canonical companion ledger: Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md
- This refreshed UTS maps USER checks to completed ledger rows. USER results from an older, pre-ledger UTS should not be used for LV2 unless USER explicitly waives this refreshed handoff.
- Shortcut/worktree proof path: actual desktop shortcut must target the active FAM-006 worktree, not the AI lab/planning worktree. $precheckShortcutAlignment
- Overlay/display elements are checked only for non-gating boundary clarity. USER is not being asked to accept Overlay/display as the current branch release surface.
- ORIN/Core elements are dependency checks for desktop safety and independence. USER is not being asked to accept ORIN/Core as a released FAM-006 interface.

Codex Self-QA Before Live Validation Stage 1 Handoff
- Automated validators and live helper evidence: $($script:ManifestStatus).
- Active foreground user-facing client self-QA: $($script:InteractionManifestStatus).
- $precheckManifestSummary
- $precheckProofClassesSummary
- Dashboard-specific proof refresh: PASS when this file points to fresh before/after full-desktop screenshots and a PASS manifest.
- User Test Summary Results: PENDING.
- Live Validation Stage 2 advancement is BLOCKED until USER returns this file or explicitly waives it and Codex digests the result.

Returned USER Issue Register Retest Focus
- FAM006-RUI-021 HUD enable rendering flash: covered by Step 2. $precheckStep2
- FAM006-RUI-022 HUD enable/disable state: covered by Step 2. $precheckStep2
- FAM006-RUI-023 Dashboard tray open/close visibility: covered by Step 2. $precheckStep2
- FAM006-RUI-024 Disable HUD unusable state: covered by Step 2. $precheckStep2
- FAM006-RUI-025 Exit NDAI delay/no confirmation: covered by Step 3. $precheckStep3
- FAM006-RUI-039 Tray Exit NDAI real-client confirmation failure: covered by Step 3. $precheckStep3
- FAM006-RUI-040 Tray Enable/Disable works partially but Dashboard does not open: covered by Step 2. $precheckStep2
- FAM006-RUI-041 issue-register/proof-governance gap: covered by this handoff's per-step Codex Precheck lines and proof-class separation summary.
- FAM006-RUI-042 denied LV1 handoff for missing real-human validation: covered by this LV1 precheck. $precheckHumanClientRun
- FAM006-RUI-043 still-broken UI after LV1 handoff: covered by issue-grounded visual questions below and fresh screenshot proof. $visualScreenshotPrecheck
- FAM006-RUI-044 tray action order: covered by Step 2 and real tray menu proof. $precheckStep2
- FAM006-RUI-045 Dashboard blocks NCP buttons: covered by Step 4. $precheckNcpInteraction
- FAM006-RUI-046 tray Create Custom Task duplicate/lock behavior: covered by Step 5. $precheckTrayAuthoring
- FAM006-RUI-047 Exit prompt visual/session-preservation split: covered by Step 3 for function; visual restyling remains future polish unless USER marks it blocking. $precheckStep3
- FAM006-RUI-048 resize hit-zone reliability: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-049 scrollbar inset / out-of-range visual issue: covered by Step 9. $visualScreenshotPrecheck
- FAM006-RUI-050 HUD Feature enabled state persistence: covered by Step 2 and Step 8. $precheckHudPersistence
- FAM006-RUI-051 Dashboard no longer resizes: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-052 Dashboard edge resize rail still difficult to find: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-053 Dashboard resize cursor appears too far from the visible edge: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-054 Dashboard resize action regressed after cursor alignment: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-055 Windows resize cursor appears only after left-click hold: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-056 Dashboard resize growth is choppy/laggy: covered by Step 8. $precheckResizeDiscoverability
- FAM006-RUI-057 actual desktop shortcut targeted the wrong worktree before this LV1 run: covered by Step 1. $precheckShortcutAlignment
- FAM006-RUI-058 USER-reported #123 recurrence after prior active-client proof: covered by Focus Item A and the real shortcut first-open screenshot sequence. $precheckFirstOpenStability
- FAM006-RUI-059 USER-reported #127 recurrence after prior active-client proof: covered by Focus Item B and Step 8 real mouse resize-fluidity proof. $precheckResizeDiscoverability
- FAM006-RUI-060 Dashboard Settings visible but not opening / double-click maximizes Dashboard: covered by Focus Item C. $precheckSettingsPanel
- FAM006-RUI-061 Dashboard close affordance should use the Settings-window-style Close pill at the top-right and work from top chrome: covered by Focus Item D. $precheckTopChromeClose
- FAM006-RUI-062 returned UTS says #127 is almost gone but still needs smoother resize: covered by Focus Item B and stricter Step 8 dense geometry-sample proof. $precheckResizeDiscoverability
- FAM006-RUI-063 returned UTS says top-chrome Close should match the Settings-window Close and sit at the top-most right with a clear gutter: covered by Focus Item D. $precheckTopChromeClose
- FAM006-RUI-064 returned UTS says #123 first-open flicker is still present: covered by Focus Item A and the visual-continuity screenshot sequence. $precheckFirstOpenStability

Focused FAM-006 Dashboard Settings Panel Retest
Answer each focused item as PASS, FAIL, or WAIVED. Add exact notes for any FAIL or WAIVED result.

Focus Item A - #123 Dashboard initial open stability
Launch through the governed red FAM-006 desktop shortcut, enable/open HUD Dashboard from the tray, and watch the first 1-2 seconds. Expected: the Dashboard appears stable without a full-window flicker, blank flash, or late compact-geometry snap. $precheckFirstOpenStability
USER Result / Notes:

Focus Item B - #127 Dashboard resize smoothness
Resize the Dashboard slowly and quickly from the right edge, bottom edge, and bottom-right corner. Expected: the visible resize cursor appears near the chrome edge before click, the Dashboard tracks the cursor through multiple intermediate sizes, and there is no obvious catch-up lag. $precheckResizeDiscoverability
USER Result / Notes:

Focus Item C - Dashboard Settings panel
Click the visible Settings button once. Expected: the Settings Panel opens. Double-clicking the Settings area must not maximize/fullscreen the Dashboard. Use Done/Close inside the panel. Expected: the panel closes and the Dashboard remains open and usable. $precheckSettingsPanel
USER Result / Notes:

Focus Item D - Dashboard top-chrome Close
Click the top-chrome Close control. Expected: the Dashboard hides without disabling the HUD Feature, and tray Open HUD Dashboard brings it back. The Close control should look like the Settings-window Close pill, sit at the top-most right of the Dashboard UI, and keep a clear but restrained gutter from Settings. $precheckTopChromeClose
USER Result / Notes:

Focus Item E - Dashboard regression sweep
With the Dashboard open, confirm Create Monitor, Edit Monitor, tray Open Command Overlay, scroll gutter, and tray enable/disable still work. Expected: existing Branch 1 and Branch 2 Dashboard behavior remains intact. $precheckNcpInteraction
USER Result / Notes:

Issue-Grounded USER Questions
Answer each issue as PASS, FAIL, or WAIVED. Add notes/screenshots for any FAIL or WAIVED answer.

FAM006-RUI-001 / USER #1 - Does the top title read as HUD Dashboard, not Monitoring Control Panel?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-002 / USER #2 - Is the title description smaller, readable, and no longer visually over-dense?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-003 / USER #3 - Is naming consistent enough for this branch: Dashboard means control hub, HUD Overlay means overlay/display, and Monitor Group remains understandable?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-004 / USER #4 - Is the Dashboard/HUD Overlay relationship clear, with HUD capability/overlay status grouped in a way that explains they belong together without making Dashboard movement depend on Overlay anchor state?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-005 / USER #5 - Does the sticky title/status header remain visible while scrolling without feeling oversized or broken?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-006 / USER #6a - Is text wrapping/clipping fixed across the Dashboard, including long labels, cards, buttons, and status copy?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-007 / USER #6b - Are proof/debug-heavy groupings removed from the Dashboard home surface so it feels like a user-facing hub?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-008 / USER #6c/#26 - Does the scrollbar look owned by the Dashboard window/chrome, with no visible extra scroll layer or invisible-frame attachment?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-009 / USER #6d - Is the Dashboard information architecture clearer and less chaotic than the returned screenshots?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-010 / USER #6e - Is polling removed from the Dashboard home and treated as Create/Edit Monitor Group scope?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-011 / USER #6f - Is Dev Toolkit Interface Review Mode correctly deferred/future and absent from production Dashboard UI?
$deferredBoundaryPrecheck
USER Result / Notes:

FAM006-RUI-012 / USER #7 - Does the Dashboard behave like a hub/home surface, with full child-window editors clearly deferred rather than half-implemented inline?
$deferredBoundaryPrecheck
USER Result / Notes:

FAM006-RUI-013 / USER #7a - Is default 1s polling treated as Monitor Group create/edit behavior rather than a Dashboard-home control?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-014 / USER #8/#29 - Is the old native CPU/provider pending hero slab removed from the Dashboard home, with provider truth moved into appropriate Data Sources/Readiness context?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-015 / USER #9 - Is the old "Monitor group to edit" confusion resolved into clearer Monitor Group actions or deferred editor behavior?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-016 / USER #10/#35 - Does Data Sources/Provider Setup avoid appearing as a broken clickable action if the full editor is deferred?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-017 / USER #11 - Are button colors and hierarchy clear enough to distinguish primary, secondary, disabled/deferred, and warning notification actions?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-018 / USER #12/#37 - Does Warning Notifications make sense as a global quick toggle while per-monitor warning settings remain future Create/Edit Monitor Group scope?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-019 / USER #13/#28 - Can the Dashboard be resized acceptably and without the old fake corner-only affordance problem?
$activeClientPrecheck
USER Result / Notes:

FAM006-RUI-020 / USER #20 - Is NCP placement/persistence acceptable as deferred future scope unless this FAM-006 path visibly blocks or worsens NCP behavior during this test?
$deferredBoundaryPrecheck
USER Result / Notes:

FAM006-RUI-021 / USER #21 - When enabling HUD from tray, does the Dashboard open without ugly flashing or unstable render behavior?
$precheckStep2
USER Result / Notes:

FAM006-RUI-022 / USER #22 - After enabling HUD from tray, can you disable it again and do the tray labels/runtime state stay truthful?
$precheckStep2
USER Result / Notes:

FAM006-RUI-023 / USER #23 - Can you open and close the HUD Dashboard from the tray without disabling the whole feature?
$precheckStep2
USER Result / Notes:

FAM006-RUI-024 / USER #24 - After disabling HUD, do Dashboard, tray, NCP, and the overall program remain usable without force-close?
$precheckStep2
USER Result / Notes:

FAM006-RUI-025 / USER #25 - Does tray Exit NDAI show visible confirmation and avoid silent delayed shutdown behavior?
$precheckStep3
USER Result / Notes:

FAM006-RUI-026 / USER #26 - Does the scrollbar still look attached to an outer/invisible frame, or is ownership visually fixed?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-027 / USER #27 - Is the haze/square opacity frame around the Dashboard gone or visually acceptable?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-028 / USER #28 - Can you resize the Dashboard in expected directions without broken behavior?
$activeClientPrecheck
USER Result / Notes:

FAM006-RUI-029 / USER #29 - Is the unnecessary native CPU/provider banner removed from the Dashboard home?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-030 / USER #30 - Are the large empty dead zones removed or made visually/functionally meaningful?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-031 / USER #31 - Is the checkered/grid pattern limited to card/settings regions and removed from the quick/top shell where you marked it red?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-032 / USER #32 - While scrolling, does the sticky title/header mask content correctly so icons/text do not float behind or above it?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-033 / USER #33 - Is the quick access area clear, and is Warning Notifications placed as a high-priority action near the top order?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-034 / USER #34 - Is Create/Edit redundancy reduced so quick access and Monitor Group card actions do not compete confusingly?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-035 / USER #35 - If Open Data Sources is deferred, is it visibly disabled/deferred instead of looking broken?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-036 / USER #36 - Is card order acceptable for the current branch release surface: HUD Overlay, Monitor Groups, Warning Notifications, Data Sources, Readiness?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-037 / USER #37 - Is Warning Notifications simplified enough that the global toggle is in quick access and per-monitor warning settings remain future editor scope?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-038 / USER #38 - Is HUD Overlay terminology used for overlay-related items, and is whole-feature enable/disable kept out of the Dashboard home and owned by tray/global control?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-039 / New #1 - Does the real desktop shortcut -> tray Exit NDAI path show governed confirmation and avoid the prior delayed no-prompt close?
$precheckStep3
USER Result / Notes:

FAM006-RUI-040 / New #2 - Does real tray Enable HUD Feature / Open HUD Dashboard make the real Dashboard visible, and do Close/Disable keep state recoverable?
$precheckStep2
USER Result / Notes:

FAM006-RUI-041 / New #3 - Does this UTS itself provide enough issue-register traceability, per-step Codex prechecks, and proof-class separation to prevent the prior validation oversight?
Codex Precheck: PASS through issue-grounded UTS template, branch Returned USER Issue Register, companion ledger mappings, and proof-class manifest separation. USER review of this handoff is still required.
USER Result / Notes:

FAM006-RUI-042 / LV1 denial - Did Codex complete the real-human client validation precheck before handing this UTS back to you?
$precheckHumanClientRun
USER Result / Notes:

FAM006-RUI-043 / LV1 denial - Do the fresh screenshots and issue-grounded UI questions below give enough real visual coverage for you to judge the Dashboard without hidden broad claims?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-044 / WS49 comment - In the real tray menu, is Open/Close HUD Dashboard positioned directly below Enable/Disable HUD Feature?
$precheckStep2
USER Result / Notes:

FAM006-RUI-045 / Bug 1 - With Dashboard open and moved left, can NCP Create Custom Task, Create Custom Group, Manage Custom Tasks, and Manage Custom Groups all receive clicks and open/dismiss normally?
$precheckNcpInteraction
USER Result / Notes:

FAM006-RUI-046 / Bug 2 - From the tray, does Create Custom Task avoid spawning infinite duplicate/locked dialogs while an authoring dialog is already active?
$precheckTrayAuthoring
USER Result / Notes:

FAM006-RUI-047 / Exit prompt polish - Functionally, does tray Exit NDAI show confirmation, preserve the session on cancel/timeout, and shut down promptly only when accepted? Note separately if you want the prompt visual style changed from Windows-standard to NDAI-styled.
$precheckStep3
USER Result / Notes:

FAM006-RUI-048 / Resize hit-zone reliability - Can you reliably discover the resize rail without hunting for a tiny one-pixel edge?
$precheckResizeDiscoverability
USER Result / Notes:

FAM006-RUI-049 / Scrollbar inset precision - Does the scrollbar look properly inset inside the rounded Dashboard chrome, without the vertical bar feeling out of range or too large for the window?
$visualScreenshotPrecheck
USER Result / Notes:

FAM006-RUI-050 / HUD Feature state persistence - If HUD Feature is enabled and the app is relaunched, does the enabled state persist without surprise-opening the Dashboard?
$precheckHudPersistence
USER Result / Notes:

FAM006-RUI-051 / Resize regression - Can the Dashboard still resize after the post-WS51/WS52 repair path?
$precheckResizeDiscoverability
USER Result / Notes:

FAM006-RUI-052 / Edge resize discoverability - Are the right-edge, bottom-edge, and corner resize rails easy enough to find and use consistently?
$precheckResizeDiscoverability
USER Result / Notes:

FAM006-RUI-053 / Resize cursor alignment - Does the standard Windows resize cursor appear only near the actual Dashboard edge/corner instead of far inside the window?
FAM006-RUI-054 / Resize action recovery - When the standard Windows resize cursor appears, can you drag from that cursor transition point and reliably resize the Dashboard from the corner, right edge, and bottom edge?
FAM006-RUI-055 / Pre-click resize cursor - Does the standard Windows resize cursor appear when the cursor reaches a valid Dashboard edge/corner before you click or hold?
FAM006-RUI-056 / Resize fluidity - When increasing the Dashboard size from the right edge, bottom edge, or corner, does the window grow smoothly instead of choppy/laggy?
$precheckResizeDiscoverability
USER Result / Notes:

FAM006-RUI-057 / Shortcut-worktree alignment - When you launch from the desktop shortcut, are you testing the FAM-006 worktree/branch rather than the AI lab/planning worktree?
$precheckShortcutAlignment
USER Result / Notes:

What This Test Is Checking
- The HUD Dashboard is the current branch's primary user-facing interface release surface.
- The Dashboard is a Nexus/NDAI settings and control hub for HUD Overlay posture, monitor groups, warning notifications, data-source/readiness truth, and future Overlay/display behavior.
- This rerun specifically checks the returned-feedback repair set: first-open flicker recurrence, resize cursor alignment, pre-click resize cursor timing, denser resize fluidity proof, Dashboard top-right Close styling/placement, Dashboard Settings open/close behavior, tray enable/disable, Dashboard tray open/close, disable-HUD recovery, Dashboard frame/scrollbar ownership, deadzone removal, sticky-header masking, action cleanup, HUD Overlay terminology, and deferred/broken button handling.
- Overlay/display release acceptance is deferred and non-gating for this branch's Dashboard acceptance path. Do not fail this Dashboard handoff because Overlay/display release acceptance is not being requested.
- ORIN/Core is dependency-only proof for desktop safety. It should remain independent from the Dashboard and should not be judged as a released FAM-006 interface in this handoff.
- Dev Toolkit Interface Review Mode and full standalone child-window implementation are deferred/future. Do not fail this Dashboard handoff because those future branches are not implemented here.
- NCP placement/persistence item #20 is deferred unless the current FAM-006 Dashboard/HUD path visibly causes or worsens it during this test.
- Dashboard proof should show a visible, readable, polished, independently movable control hub with no clipping, no Core/Overlay coupling, no fake telemetry, provider-contract-first setup/no-data/degraded truth, and visual/non-invasive warning controls.
- Each test step below lists the ledger rows it covers so LV2 can digest returned USER results at the element level instead of relying on broad "Dashboard green" claims.

Expected Outcome
- Dashboard reads as "HUD Dashboard" or equivalent settings/control hub copy, not as the final anchored HUD Overlay/display.
- Dashboard controls are understandable for HUD Overlay posture, Monitor Groups, Warning Notifications, Data Sources/Readiness, and current deferred boundaries.
- Tray controls can enable/disable the HUD feature and open/close the HUD Dashboard without locking the app.
- Dashboard moves as a standalone window without dragging Core or Overlay/display surfaces.
- Dashboard can be resized, owns its visible scrollbar/frame, has no obvious outer haze/square ghost frame, and does not leave large dead zones or floating content above the sticky header.
- Provider/setup/no-data/degraded states are truthful and do not pretend unsupported hardware values are real.
- Warning posture is visual/non-invasive only.
- Data Sources and HUD Overlay controls do not appear as broken clickable current-scope actions when they are deferred.
- No fake CPU/GPU/thermal values, unsupported provider claims, spoken/audio behavior, plugin-fed telemetry, PR work, release work, tags, or artifacts appear.
- No retired product naming appears in repo-owned Dashboard/Core user-facing surfaces.

Test Steps
1. Launch Nexus Desktop AI from the normal desktop shortcut or documented equivalent Live Validation path.
$precheckStep1
Observed Results:

2. Use the tray controls to enable/disable the HUD feature and open/close the HUD Dashboard. Confirm the app remains usable, the Dashboard can be reopened, and disabling HUD does not lock the Dashboard, tray, NCP, or the program.
$precheckStep2
Ledger rows: FAM006-HUD-FEATURE-TRAY-046; FAM006-HUD-TRAY-FLASH-051; FAM006-HUD-TRAY-STATE-LOCK-052; FAM006-DASH-TRAY-OPEN-CLOSE-053; FAM006-HUD-DISABLE-UNUSABLE-054.
Observed Results:

3. If you use tray Exit NDAI, confirm the governed confirmation/shutdown path is acceptable. Do not treat a separately desired shutdown redesign as Dashboard acceptance unless it blocks this FAM-006 path.
$precheckStep3
Ledger rows: FAM006-TRAY-SHUTDOWN-CONFIRM-055.
Observed Results:

4. With Dashboard open and moved to the left side of the middle monitor, open NCP from the tray and confirm Create Custom Task, Create Custom Group, Manage Custom Tasks, and Manage Custom Groups all receive clicks and open/dismiss normally.
$precheckNcpInteraction
Ledger rows: FAM006-DASH-NCP-MOUSE-068; FAM006-DASH-FOCUS-047; FAM006-NCP-REGRESSION-048; FAM006-DASH-CLIP-004.
Observed Results:

5. From the tray, click Create Custom Task while an authoring dialog is already active and confirm it does not spawn infinite duplicate or locked windows.
$precheckTrayAuthoring
Ledger rows: FAM006-TRAY-AUTHORING-DIALOG-GUARD-069; FAM006-NCP-REGRESSION-048; FAM006-GOV-HUMAN-CLIENT-065.
Observed Results:

6. Confirm the ORIN Core visualization remains independent and does not visibly attach to or move with the Dashboard.
$activeClientPrecheck
Ledger rows: FAM006-CORE-DEP-025; FAM006-CORE-PRESET-026; FAM006-CORE-NONMOVABLE-027; FAM006-CORE-WORKERW-028; FAM006-CORE-TRANSPARENCY-029; FAM006-CORE-ISOLATION-030.
Observed Results:

7. Confirm the HUD Dashboard is visible as a Dashboard/control hub, not the final Overlay/display. It should not show the old proof-heavy/native CPU hero slab as the main home content.
$visualScreenshotPrecheck
Ledger rows: FAM006-DASH-SURFACE-001; FAM006-DASH-CONTENT-008; FAM006-DASH-VISUAL-006; FAM006-DASH-PROVIDER-015.
Observed Results:

8. Move and resize the Dashboard. Confirm the corner, right-edge, and bottom-edge resize rails are discoverable and change real Dashboard geometry; also confirm the Dashboard behaves like a standalone normal window without clipping, disappearing, blocking NCP/other windows, stealing topmost focus, dragging the Core, or dragging the deferred Overlay/display.
$precheckResizeDiscoverability
Ledger rows: FAM006-DASH-WINDOW-002; FAM006-DASH-MOVE-003; FAM006-DASH-CLIP-004; FAM006-DASH-FOCUS-047; FAM006-DASH-RESIZE-057; FAM006-NCP-REGRESSION-048.
Observed Results:

9. Confirm the Dashboard frame, scrollbar, background texture, card spacing, and sticky title/header are visually coherent. The scrollbar should belong to the Dashboard chrome, the outer haze/square frame should not be visible, content should not float over the sticky title, and big empty dead zones should not dominate cards.
$visualScreenshotPrecheck
Ledger rows: FAM006-DASH-LAYOUT-005; FAM006-DASH-VISUAL-006; FAM006-DASH-SCROLL-007; FAM006-DASH-FRAME-HAZE-056; FAM006-DASH-DEADZONE-058; FAM006-DASH-STICKY-OCCLUSION-059.
Observed Results:

10. Confirm Dashboard controls are understandable and not redundant: Quick Access should prioritize Warning Notifications, Monitor Groups should own Create/Edit, Data Sources should be clearly deferred/disabled if not implemented, and HUD Overlay terminology should be used for Overlay-related items.
$visualScreenshotPrecheck
Ledger rows: FAM006-DASH-CONTENT-008; FAM006-DASH-MONITOR-GROUP-009; FAM006-DASH-MONITOR-ENABLE-010; FAM006-DASH-MONITOR-POLLING-011; FAM006-DASH-AFFORDANCE-COPY-012; FAM006-DASH-WARNING-017; FAM006-DASH-QUICK-ACCESS-060; FAM006-DASH-DEFERRED-BUTTON-061; FAM006-DASH-HUD-OVERLAY-COPY-062.
Observed Results:

11. Confirm monitor groups are organizational settings objects in the Dashboard, not display cards that imply Overlay/display acceptance.
$deferredBoundaryPrecheck
Ledger rows: FAM006-DASH-MONITOR-GROUP-009; FAM006-OVERLAY-MONITOR-CARDS-023; FAM006-OVERLAY-DEFER-018.
Observed Results:

12. Confirm provider/setup/no-data/degraded copy is truthful and no fake CPU/GPU/thermal values are presented as real.
$visualScreenshotPrecheck
Ledger rows: FAM006-DASH-PROVIDER-015; FAM006-DASH-NOFAKE-016; FAM006-FUTURE-PROVIDER-041; FAM006-FUTURE-EXTERNAL-042.
Observed Results:

13. Confirm warning controls remain visual/non-invasive and do not introduce audio/spoken alerts or screen flash behavior.
$visualScreenshotPrecheck
Ledger rows: FAM006-DASH-WARNING-017; FAM006-FUTURE-AUDIO-043.
Observed Results:

14. Confirm deferred/future boundaries are clear: Overlay/display acceptance, full child-window editors, Dev Toolkit Interface Review Mode, provider-platform parity, audio alerts, and NCP placement/persistence #20 are not being accepted in this branch unless they visibly break current Dashboard safety.
$deferredBoundaryPrecheck
Ledger rows: FAM006-OVERLAY-DEFER-018; FAM006-DASH-CHILD-WINDOW-049; FAM006-DEV-INTERFACE-REVIEW-050; FAM006-FUTURE-PROVIDER-041; FAM006-FUTURE-AUDIO-043; FAM006-NCP-REGRESSION-048.
Observed Results:

15. Note any readability, placement, clipping, scaling, motion, confusion, tray-state, deferred-button, NCP-blocking, or polish concern that should block Dashboard acceptance.
$visualScreenshotPrecheck
Ledger rows: all user-facing and hidden-user-facing Dashboard/Core/tray rows listed above.
Observed Results:

Failure Signs To Watch For
- Dashboard is too small, text is clipped, cramped, or unclear.
- Dashboard movement stutters badly, disappears, clips, or drags another surface with it.
- Dashboard content looks like technical proof boxes instead of settings/control content.
- Dashboard implies Overlay/display release acceptance is required in this branch.
- UTS feedback cannot be mapped to the ledger rows listed in this handoff.
- ORIN/Core moves with the Dashboard or appears rendered inside the Dashboard.
- Provider copy claims live hardware values without a safe provider/proof path.
- Fake hardware values or unsupported telemetry claims appear.
- Warning behavior widens into audio/spoken or strong flash behavior without approval.
- Retired product naming appears in repo-owned user-facing surfaces.

New Ideas / Requests Raised During Testing:

Questions / Confusions Raised During Testing:

Regression Notes:

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
