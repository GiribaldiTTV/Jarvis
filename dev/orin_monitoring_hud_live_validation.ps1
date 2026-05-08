param(
    [string]$PythonPath = $env:NEXUS_VALIDATION_PYTHON,
    [string]$ArtifactRoot = "",
    [int]$MarkerTimeoutSeconds = 25,
    [int]$NoProgressTimeoutSeconds = 10,
    [switch]$RunInteractionSelfQA,
    [switch]$VisibleClient,
    [switch]$ActiveUserFacingClient,
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
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
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
        proofStandard = "WS30 active-client before-after desktop proof plus fixed Core/HUD surface separation"
        primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel"
        dashboardFirstWorkstreamHandoff = "ws31-dashboard-control-panel-acceptance-baseline"
        dashboardOnlyAcceptanceBaseline = "ws31-dashboard-control-panel"
        currentInterfaceReleaseGate = "dashboard-only-current-branch"
        overlayAcceptanceGate = "deferred-non-gating-supporting-evidence"
        interfaceBundleUserApproval = "not-granted"
        overlayDisplayAcceptance = "deferred-non-gating"
        coreRepairClassification = "dependency-repair-only"
        dashboardFirstProofPath = $true
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
    if ($script:ManifestStatus -eq "PASS") {
        Write-Output "PASS: FAM-006 Monitoring/HUD live desktop proof captured at $($paths.Root)"
    }
    else {
        Write-Output "FAIL: FAM-006 Monitoring/HUD live desktop proof failed at $($paths.Root)"
    }
}

exit $exitCode
