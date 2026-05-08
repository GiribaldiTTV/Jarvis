param(
    [string]$PythonPath = $env:NEXUS_VALIDATION_PYTHON,
    [string]$ArtifactRoot = "",
    [int]$MarkerTimeoutSeconds = 25,
    [int]$NoProgressTimeoutSeconds = 10,
    [switch]$RunInteractionSelfQA,
    [switch]$VisibleClient,
    [switch]$ActiveUserFacingClient,
    [switch]$PrepareLiveValidationUserTestSummary,
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
    $manifest = [pscustomobject]@{
        status = $script:ManifestStatus
        package = "PKG-006"
        slice = "SLC-029"
        seam = "Live Validation LV1 - Monitoring HUD Product Surface Live Validation"
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

    $content = @"
Nexus Desktop AI - User Test Summary
Workstream: FAM-006 Monitoring and HUD Product Surface Package
Current Phase: Live Validation Stage 1 User Test Summary handoff
Branch: feature/fam-006-monitoring-hud-product-surface
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
- Overlay/display elements are checked only for non-gating boundary clarity. USER is not being asked to accept Overlay/display as the current branch release surface.
- ORIN/Core elements are dependency checks for desktop safety and independence. USER is not being asked to accept ORIN/Core as a released FAM-006 interface.

Codex Self-QA Before Live Validation Stage 1 Handoff
- Automated validators and live helper evidence: $($script:ManifestStatus).
- Active foreground user-facing client self-QA: $($script:InteractionManifestStatus).
- Dashboard-specific proof refresh: PASS when this file points to fresh before/after full-desktop screenshots and a PASS manifest.
- User Test Summary Results: PENDING.
- Live Validation Stage 2 advancement is BLOCKED until USER returns this file or explicitly waives it and Codex digests the result.

What This Test Is Checking
- The Monitoring Dashboard is the current branch's primary user-facing interface release surface.
- The Dashboard is a Nexus/NDAI settings and control panel for HUD capability, monitor groups, monitor settings, polling posture, warning posture, provider/setup states, and future Overlay/display behavior.
- Overlay/display release acceptance is deferred and non-gating for this branch's Dashboard acceptance path. Do not fail this Dashboard handoff because Overlay/display release acceptance is not being requested.
- ORIN/Core is dependency-only proof for desktop safety. It should remain independent from the Dashboard and should not be judged as a released FAM-006 interface in this handoff.
- Dashboard proof should show a visible, readable, polished, independently movable control panel with no clipping, no Core/Overlay coupling, no fake telemetry, provider-contract-first setup/no-data/degraded truth, and visual/non-invasive warning controls.
- Each test step below lists the ledger rows it covers so LV2 can digest returned USER results at the element level instead of relying on broad "Dashboard green" claims.

Expected Outcome
- Dashboard reads as "Monitoring Control Panel" or equivalent settings/control copy, not as the final anchored HUD Overlay/display.
- Dashboard controls are understandable for HUD capability, monitor group creation/editing, monitor enablement, polling posture, provider setup state, and warning posture.
- Dashboard moves as a standalone window without dragging Core or Overlay/display surfaces.
- Dashboard is not clipped to the Core, Overlay/display, or a fixed render area.
- Provider/setup/no-data/degraded states are truthful and do not pretend unsupported hardware values are real.
- Warning posture is visual/non-invasive only.
- No fake CPU/GPU/thermal values, unsupported provider claims, spoken/audio behavior, plugin-fed telemetry, PR work, release work, tags, or artifacts appear.
- No retired product naming appears in repo-owned Dashboard/Core user-facing surfaces.

Test Steps
1. Launch Nexus Desktop AI from the normal desktop shortcut or documented equivalent Live Validation path.
Observed Results:

2. Confirm the ORIN Core visualization remains independent and does not visibly attach to or move with the Dashboard.
Ledger rows: FAM006-CORE-DEP-025; FAM006-CORE-PRESET-026; FAM006-CORE-NONMOVABLE-027; FAM006-CORE-WORKERW-028; FAM006-CORE-TRANSPARENCY-029; FAM006-CORE-ISOLATION-030.
Observed Results:

3. Confirm the Monitoring Dashboard is visible as a Dashboard/control panel, not the final Overlay/display.
Ledger rows: FAM006-DASH-SURFACE-001; FAM006-DASH-CONTENT-008; FAM006-DASH-VISUAL-006.
Observed Results:

4. Move the Dashboard and confirm it behaves like a standalone window without clipping, disappearing, dragging the Core, or dragging the deferred Overlay/display.
Ledger rows: FAM006-DASH-WINDOW-002; FAM006-DASH-MOVE-003; FAM006-DASH-CLIP-004.
Observed Results:

5. Confirm Dashboard controls are understandable for HUD capability, monitor groups, monitor enablement, polling posture, provider setup state, and warning posture.
Ledger rows: FAM006-DASH-CONTENT-008; FAM006-DASH-MONITOR-GROUP-009; FAM006-DASH-MONITOR-ENABLE-010; FAM006-DASH-MONITOR-POLLING-011; FAM006-DASH-AFFORDANCE-COPY-012; FAM006-DASH-WARNING-017.
Observed Results:

6. Confirm monitor groups are organizational settings objects in the Dashboard, not display cards that imply Overlay/display acceptance.
Ledger rows: FAM006-DASH-MONITOR-GROUP-009; FAM006-OVERLAY-MONITOR-CARDS-023; FAM006-OVERLAY-DEFER-018.
Observed Results:

7. Confirm provider/setup/no-data/degraded copy is truthful and no fake CPU/GPU/thermal values are presented as real.
Ledger rows: FAM006-DASH-PROVIDER-015; FAM006-DASH-NOFAKE-016; FAM006-FUTURE-PROVIDER-041; FAM006-FUTURE-EXTERNAL-042.
Observed Results:

8. Confirm warning controls remain visual/non-invasive and do not introduce audio/spoken alerts or screen flash behavior.
Ledger rows: FAM006-DASH-WARNING-017; FAM006-FUTURE-AUDIO-043.
Observed Results:

9. Confirm the Dashboard UI is readable, polished, not cramped, and uses Nexus/NDAI styling without default-looking product chrome where the branch owns the surface.
Ledger rows: FAM006-DASH-LAYOUT-005; FAM006-DASH-VISUAL-006; FAM006-DASH-SCROLL-007.
Observed Results:

10. Note any readability, placement, clipping, scaling, motion, confusion, or polish concerns that should block Dashboard acceptance.
Ledger rows: all user-facing and hidden-user-facing Dashboard/Core rows listed above.
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

try {
    Step $paths "starting FAM-006 Monitoring/HUD live desktop validation"
    $pythonExe = Resolve-ValidationPython
    Step $paths "resolved Python: $pythonExe"
    Capture-Screen $paths "before_launch"

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
        "MONITORING_HUD_MINIMAL_NATIVE_OVERLAY_READY",
        "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY",
        "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY",
        "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY",
        "MONITORING_HUD_MINIMAL_ANCHORED_CLICK_THROUGH_READY",
        "MONITORING_HUD_MINIMAL_NON_FOCUS_READY",
        "MONITORING_HUD_VISIBLE_OVERLAY_READY",
        "MONITORING_HUD_WINDOW_STATUS_READY",
        "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
        "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
        "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
        "MONITORING_HUD_STATUS_BEHAVIOR_READY",
        "MONITORING_HUD_INTERACTION_MODE_READY",
        "MONITORING_HUD_CONTROL_STATE_READY",
        "DESKTOP_VISIBLE_OVERLAY_RESULT|success=true",
        "RENDERER_MAIN|STARTUP_READY",
        "DESKTOP_OUTCOME|SETTLED|state=dormant"
    )
    foreach ($marker in $requiredMarkers) {
        Wait-Marker $paths $marker
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

    Step $paths "settling visible overlay before full-desktop screenshot"
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
