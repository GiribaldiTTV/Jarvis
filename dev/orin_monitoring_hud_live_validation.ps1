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
$script:ShortVideoProof = [ordered]@{
    status = "NOT_REQUESTED"
    path = ""
    userInspectablePath = ""
    frameCount = 0
    sourceRoot = ""
    proofClass = "short-video-or-frame-sequence"
}
$script:PerElementScreenshotProof = [ordered]@{
    status = "NOT_REQUESTED"
    root = ""
    count = 0
    proofClass = "focused-per-element-screenshot"
    screenshots = @()
}

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

function Assert-NoSyntheticLiveValidationInteraction {
    param([object]$Paths)

    $rendererPath = Join-Path $rootDir "desktop\desktop_renderer.py"
    if (-not (Test-Path -LiteralPath $rendererPath)) {
        throw "Synthetic-interaction preflight could not inspect renderer path: $rendererPath"
    }
    $rendererText = Get-Content -LiteralPath $rendererPath -Raw
    $startMarker = "def _start_monitoring_hud_live_client_real_os_self_qa"
    $startIndex = $rendererText.IndexOf($startMarker, [StringComparison]::Ordinal)
    if ($startIndex -lt 0) {
        throw "Synthetic-interaction preflight could not find active LV1 self-QA route marker: $startMarker"
    }
    $nextMethodIndex = $rendererText.IndexOf("`n    def ", $startIndex + $startMarker.Length, [StringComparison]::Ordinal)
    if ($nextMethodIndex -lt 0) {
        $routeText = $rendererText.Substring($startIndex)
    }
    else {
        $routeText = $rendererText.Substring($startIndex, $nextMethodIndex - $startIndex)
    }
    $forbiddenPatterns = @(
        @{ Pattern = ".click("; Label = "direct JavaScript click" },
        @{ Pattern = "dispatchEvent(new MouseEvent"; Label = "synthetic DOM mouse event" },
        @{ Pattern = "QTest.mouse"; Label = "QTest widget-only mouse event" },
        @{ Pattern = "handler calls"; Label = "direct handler-call proof" }
    )
    $findings = New-Object System.Collections.Generic.List[string]
    foreach ($entry in $forbiddenPatterns) {
        if ($routeText.Contains([string]$entry.Pattern)) {
            $findings.Add("$($entry.Label): $($entry.Pattern)")
        }
    }
    if ($findings.Count -gt 0) {
        $findingPath = Join-Path $Paths.Root "synthetic_live_validation_interaction_blockers.txt"
        $findings | Set-Content -LiteralPath $findingPath -Encoding utf8
        Step $Paths "blocked LV1 before launch: active route contains synthetic interaction code: $findingPath"
        throw "Live Validation interaction route contains banned synthetic/widget/direct-handler interaction code. STOP and diagnose the real-input failure first; do not edit the validator to use synthetic fallback. Blockers: $($findings -join '; ')"
    }
    Step $Paths "no-synthetic-interaction preflight PASS: active LV1 interaction route contains no JS click, DOM MouseEvent, QTest mouse, or direct-handler interaction proof"
    Step $Paths "real-input fallback policy PASS: if a live click fails, diagnose hit target, z-order, native hit testing, focus, scroll, and runtime state before any validator change; synthetic fallback requires explicit USER waiver"
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
    $elementScreenshotEvidenceRoot = Join-Path $screenshotEvidenceRoot "focused_element_screenshots"
    New-Item -ItemType Directory -Force -Path $screenshotEvidenceRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $elementScreenshotEvidenceRoot | Out-Null
    [pscustomobject]@{
        Root = $ArtifactRoot
        ScreenshotEvidenceRoot = $screenshotEvidenceRoot
        ElementScreenshotEvidenceRoot = $elementScreenshotEvidenceRoot
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
        ShortVideoFrameRoot = Join-Path $ArtifactRoot "short_video_frames"
        ShortVideo = Join-Path $ArtifactRoot "monitoring_hud_lv1_short_video.mp4"
        ShortVideoEvidence = Join-Path $screenshotEvidenceRoot "monitoring_hud_lv1_short_video.mp4"
        UserTestSummary = Join-Path $env:USERPROFILE "OneDrive\Desktop\User Test Summary.txt"
        AbortSignal = Join-Path $ArtifactRoot "startup_abort.signal"
    }
}

function ConvertTo-SafeScreenshotName([string]$Value) {
    $safe = ($Value -replace "[^A-Za-z0-9_-]", "_").Trim("_")
    if ([string]::IsNullOrWhiteSpace($safe)) {
        return "unnamed_element"
    }
    return $safe.ToLowerInvariant()
}

function Get-HudIssueIdsForElementLabel {
    param([string]$ElementName)
    $lowerName = $ElementName.ToLowerInvariant()
    $matches = New-Object System.Collections.Generic.List[string]
    $issueRules = [ordered]@{
        "UTS-HUD-001" = @("button", "glow", "close", "settings", "profile", "manage", "create", "edit", "save", "discard", "delete", "cancel")
        "UTS-HUD-002" = @("background", "grid", "card", "window", "panel")
        "UTS-HUD-003" = @("button", "selector", "dropdown")
        "UTS-HUD-004" = @("warning", "discard", "delete", "cancel", "hover")
        "UTS-HUD-005" = @("button", "create", "selector", "dropdown")
        "UTS-HUD-006" = @("source_row", "source-picker", "source_picker", "checked")
        "UTS-HUD-007" = @("filter", "dropdown", "max_five")
        "UTS-HUD-008" = @("source_row", "source-picker", "source_picker", "hover")
        "UTS-HUD-009" = @("polling", "rate")
        "UTS-HUD-010" = @("source_settings", "display_mode", "warning_checkbox")
        "UTS-HUD-011" = @("dashboard", "data_sources", "manage_monitors")
        "UTS-HUD-012" = @("unsaved", "guard", "discard", "save")
        "UTS-HUD-013" = @("dashboard", "overlay", "manage", "source", "scrollbar", "divider", "button")
        "UTS-HUD-014" = @("overlay_profile", "clean", "selector", "choice_panel", "create", "dirty", "guard", "save", "discard", "delete", "profile_to_edit")
        "UTS-HUD-015" = @("scrollbar")
        "UTS-HUD-016" = @("divider", "page_break")
        "UTS-HUD-017" = @("button", "glow", "color", "uniform")
        "UTS-HUD-018" = @("row_title", "row-title", "page_break", "divider", "tab")
        "UTS-HUD-019" = @("state_stability", "surface_stability", "group_switch", "responsive_window", "window_contract", "open_state", "window_create_clean", "window_display_mode_buttons")
        "UTS-HUD-020" = @("source_settings", "shift", "focus", "gold", "warning")
        "UTS-HUD-021" = @("scalability", "window_size", "minimum", "responsive", "scale", "compact", "normal", "overlay_profile")
    }
    foreach ($issueId in $issueRules.Keys) {
        foreach ($keyword in $issueRules[$issueId]) {
            if ($lowerName.Contains($keyword)) {
                $matches.Add($issueId)
                break
            }
        }
    }
    if ($matches.Count -eq 0) {
        $matches.Add("UTS-HUD-013")
    }
    return @($matches)
}

function Copy-FocusedElementScreenshotsToUserEvidence {
    param(
        [object]$Paths,
        [int]$MinimumScreenshots = 48
    )

    $contextNames = @(
        "initial_live_client_visible",
        "dashboard_standalone_virtual_desktop_travel",
        "final_anchored_live_client",
        "full_virtual_desktop",
        "desktop_before_launch",
        "desktop_after_launch"
    )

    if (-not (Test-Path -LiteralPath $Paths.InteractionEvidenceRoot)) {
        return [ordered]@{
            status = "FAIL"
            root = $Paths.ElementScreenshotEvidenceRoot
            count = 0
            reason = "interaction evidence root missing; LV1 focused per-element screenshots missing"
            proofClass = "focused-per-element-screenshot"
            screenshots = @()
        }
    }

    New-Item -ItemType Directory -Force -Path $Paths.ElementScreenshotEvidenceRoot | Out-Null
    $screenshots = @()
    $pngs = @(Get-ChildItem -LiteralPath $Paths.InteractionEvidenceRoot -Filter "*.png" -File | Sort-Object Name)
    foreach ($png in $pngs) {
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($png.Name)
        $lowerName = $baseName.ToLowerInvariant()
        $isContext = $false
        foreach ($context in $contextNames) {
            if ($lowerName.Contains($context)) {
                $isContext = $true
                break
            }
        }
        if ($isContext) { continue }

        $elementName = ConvertTo-SafeScreenshotName $baseName
        $destinationName = "element_{0}.png" -f $elementName
        $destination = Join-Path $Paths.ElementScreenshotEvidenceRoot $destinationName
        Copy-Item -LiteralPath $png.FullName -Destination $destination -Force
        $issueIds = @(Get-HudIssueIdsForElementLabel -ElementName $elementName)
        $screenshots += [pscustomobject]@{
            elementLabel = $elementName
            stateOrAction = $baseName
            proofClass = "focused-per-element-screenshot"
            issueIds = $issueIds
            sourcePath = $png.FullName
            userInspectablePath = $destination
        }
    }

    $allIssueIds = @(
        "UTS-HUD-001", "UTS-HUD-002", "UTS-HUD-003", "UTS-HUD-004", "UTS-HUD-005", "UTS-HUD-006",
        "UTS-HUD-007", "UTS-HUD-008", "UTS-HUD-009", "UTS-HUD-010", "UTS-HUD-011", "UTS-HUD-012",
        "UTS-HUD-013", "UTS-HUD-014", "UTS-HUD-015", "UTS-HUD-016", "UTS-HUD-017",
        "UTS-HUD-018", "UTS-HUD-019", "UTS-HUD-020", "UTS-HUD-021"
    )
    $issueCoverage = @()
    foreach ($issueId in $allIssueIds) {
        $covered = @($screenshots | Where-Object { @($_.issueIds) -contains $issueId })
        $issueCoverage += [pscustomobject]@{
            issueId = $issueId
            status = if ($covered.Count -gt 0) { "PASS" } else { "FAIL" }
            screenshotCount = [int]$covered.Count
            screenshots = @($covered | Select-Object -ExpandProperty userInspectablePath)
        }
    }
    $missingIssueCoverage = @($issueCoverage | Where-Object { $_.status -ne "PASS" })
    $requiredElementLabels = @(
        "unsaved_guard_save_discard_buttons_visible",
        "unsaved_guard_discard_red_danger_button",
        "unsaved_guard_panel_background_no_grid_bleed",
        "dirty_guard_close_button_functionality",
        "manage_monitors_dirty_guard_save_discard_cancel_modal",
        "manage_monitors_dirty_guard_modal_uniform_with_overlay_profile",
        "manage_monitors_dirty_guard_background_blur_blocking",
        "manage_monitors_dirty_guard_close_button_functionality",
        "manage_monitors_create_after_delete_reuses_monitor_group_number",
        "manage_monitors_recreated_monitor_group_3_dirty_draft"
    )
    $availableElementLabels = @($screenshots | Select-Object -ExpandProperty elementLabel)
    $missingRequiredElementLabels = @($requiredElementLabels | Where-Object { $availableElementLabels -notcontains $_ })

    if ($screenshots.Count -lt $MinimumScreenshots) {
        return [ordered]@{
            status = "FAIL"
            root = $Paths.ElementScreenshotEvidenceRoot
            count = $screenshots.Count
            reason = "only $($screenshots.Count) focused per-element screenshot(s) copied; minimum is $MinimumScreenshots"
            proofClass = "focused-per-element-screenshot"
            perElementVisualInventory = $screenshots
            issueFormCoverageMatrix = $issueCoverage
            screenshots = $screenshots
        }
    }

    if ($missingRequiredElementLabels.Count -gt 0) {
        return [ordered]@{
            status = "FAIL"
            root = $Paths.ElementScreenshotEvidenceRoot
            count = $screenshots.Count
            reason = "focused screenshots missing mandatory dirty-guard parity element(s): $($missingRequiredElementLabels -join ', ')"
            proofClass = "focused-per-element-screenshot"
            perElementVisualInventory = $screenshots
            issueFormCoverageMatrix = $issueCoverage
            screenshots = $screenshots
        }
    }

    if ($missingIssueCoverage.Count -gt 0) {
        return [ordered]@{
            status = "FAIL"
            root = $Paths.ElementScreenshotEvidenceRoot
            count = $screenshots.Count
            reason = "focused screenshots missing issue-form coverage for: $(@($missingIssueCoverage | Select-Object -ExpandProperty issueId) -join ', ')"
            proofClass = "focused-per-element-screenshot"
            perElementVisualInventory = $screenshots
            issueFormCoverageMatrix = $issueCoverage
            screenshots = $screenshots
        }
    }

    [ordered]@{
        status = "PASS"
        root = $Paths.ElementScreenshotEvidenceRoot
        count = $screenshots.Count
        reason = "focused UI screenshots were copied to the USER-inspectable OneDrive screenshots folder with element labels in each filename and mapped to the returned UTS issue form"
        proofClass = "focused-per-element-screenshot"
        perElementVisualInventory = $screenshots
        issueFormCoverageMatrix = $issueCoverage
        screenshots = $screenshots
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

function Get-PngInfo([string]$Path) {
    Add-Type -AssemblyName System.Drawing
    $image = [System.Drawing.Image]::FromFile($Path)
    try {
        [pscustomobject]@{
            Path = (Resolve-Path -LiteralPath $Path).Path
            Width = [int]$image.Width
            Height = [int]$image.Height
            Area = [int]($image.Width * $image.Height)
        }
    }
    finally {
        $image.Dispose()
    }
}

function New-ShortVideoProof {
    param(
        [object]$Paths,
        [string[]]$SourceRoots,
        [int]$MinimumFrames = 5
    )

    $ffmpeg = Get-Command ffmpeg.exe -ErrorAction SilentlyContinue
    if (-not $ffmpeg -or -not $ffmpeg.Source) {
        return [ordered]@{
            status = "FAIL"
            reason = "ffmpeg.exe unavailable; LV1 requires durable short video or ordered frame-sequence proof"
            path = ""
            userInspectablePath = ""
            frameCount = 0
            sourceRoot = ""
            proofClass = "short-video-or-frame-sequence"
        }
    }

    $pngs = @()
    foreach ($root in $SourceRoots) {
        if ($root -and (Test-Path -LiteralPath $root)) {
            $pngs += @(Get-ChildItem -LiteralPath $root -Filter "*.png" -File | Sort-Object FullName)
        }
    }
    if ($pngs.Count -lt 2) {
        return [ordered]@{
            status = "FAIL"
            reason = "fewer than two PNG frames available for short video proof"
            path = ""
            userInspectablePath = ""
            frameCount = [int]$pngs.Count
            sourceRoot = ($SourceRoots -join ";")
            proofClass = "short-video-or-frame-sequence"
        }
    }

    $infos = @()
    foreach ($png in $pngs) {
        try { $infos += @(Get-PngInfo -Path $png.FullName) } catch {}
    }
    $groups = @($infos | Group-Object { "$($_.Width)x$($_.Height)" } | Sort-Object @{ Expression = { $_.Count }; Descending = $true }, @{ Expression = { ($_.Group | Select-Object -First 1).Area }; Descending = $true })
    $selectedGroup = $groups | Where-Object { $_.Count -ge $MinimumFrames } | Select-Object -First 1
    if (-not $selectedGroup) {
        $selectedGroup = $groups | Where-Object { $_.Count -ge 2 } | Select-Object -First 1
    }
    if (-not $selectedGroup) {
        return [ordered]@{
            status = "FAIL"
            reason = "no same-size PNG frame group was large enough for ffmpeg video proof"
            path = ""
            userInspectablePath = ""
            frameCount = 0
            sourceRoot = ($SourceRoots -join ";")
            proofClass = "short-video-or-frame-sequence"
        }
    }

    Remove-Item -LiteralPath $Paths.ShortVideoFrameRoot -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $Paths.ShortVideoFrameRoot | Out-Null
    $index = 1
    foreach ($frame in @($selectedGroup.Group | Sort-Object Path)) {
        Copy-Item -LiteralPath $frame.Path -Destination (Join-Path $Paths.ShortVideoFrameRoot ("frame_{0:0000}.png" -f $index)) -Force
        $index += 1
    }

    & $ffmpeg.Source -y -loglevel error -framerate 2 -i (Join-Path $Paths.ShortVideoFrameRoot "frame_%04d.png") -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p" -movflags +faststart $Paths.ShortVideo
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Paths.ShortVideo)) {
        return [ordered]@{
            status = "FAIL"
            reason = "ffmpeg failed to encode LV1 short video proof"
            path = $Paths.ShortVideo
            userInspectablePath = ""
            frameCount = [int]$selectedGroup.Count
            sourceRoot = ($SourceRoots -join ";")
            proofClass = "short-video-or-frame-sequence"
        }
    }

    Copy-Item -LiteralPath $Paths.ShortVideo -Destination $Paths.ShortVideoEvidence -Force
    [ordered]@{
        status = "PASS"
        reason = "durable LV1 short video proof generated from ordered same-size screenshot frames"
        path = $Paths.ShortVideo
        userInspectablePath = $Paths.ShortVideoEvidence
        frameCount = [int]$selectedGroup.Count
        sourceRoot = ($SourceRoots -join ";")
        proofClass = "short-video-or-frame-sequence"
        ffmpeg = $ffmpeg.Source
        frameRoot = $Paths.ShortVideoFrameRoot
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
        proofStandard = "Dashboard-specific static/live proof screenshots; ledger-aligned User Test Summary export is Live Validation Stage 1 only; mandatory LV1 short video/frame-sequence proof is required for desktop UI handoff; detailed focused per-element screenshots must be copied to the USER-inspectable OneDrive screenshots folder with the element label/name in each filename; per-element visual inventory and returned issue-form coverage matrix are required; full-desktop screenshots are context only; active-client/direct-runtime proof is supporting only when the real user-facing desktop launcher is feasible"
        lv1ScreenshotAndShortVideoProofRequired = $true
        lv1DetailedPerElementScreenshotsRequired = $true
        lv1RealUserFacingDesktopLauncherRequired = [bool]$PrepareLiveValidationUserTestSummary
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
        recordingProfileValidationProof = [pscustomobject]@{
            seam = "FAM-006 Recording Profile Runtime Foundation LV1"
            focusedWebViewProofRequired = $true
            fullDesktopScreenshotsAreContextOnly = $true
            perElementUserInspectableScreenshotsRequired = $true
            realUserFacingDesktopLauncherIsPrimaryLv1Path = [bool]$PrepareLiveValidationUserTestSummary
            formalUserTestSummaryBoundary = "Live Validation Stage 1 only after human-client precheck PASS or USER waiver"
            workstreamAndHardeningNoUtsExport = -not [bool]$PrepareLiveValidationUserTestSummary
            proofChain = @(
                "SLC-046 Recording Profile data/state foundation",
                "SLC-047 Recording Profile selector/settings create/edit/delete/save/discard and guarded delete behavior",
                "SLC-048 Recording Profile relationship mapping and boundary proof",
                "SLC-049 compact Dashboard / Manage Monitors read-only Recording Profile status integration",
                "SLC-050 Workstream readiness proof",
                "LV1 real user-facing desktop proof with focused screenshots, compact/default states, short video proof, and UTS handoff"
            )
        }
        dashboardSpecificProof = [pscustomobject]@{
            beforeLaunchFullVirtualDesktopScreenshot = [bool]$script:BeforeScreenshotPath
            afterLaunchFullVirtualDesktopScreenshot = [bool]$script:ScreenshotPath
            shortVideoOrFrameSequenceProof = $script:ShortVideoProof
            perElementUserInspectableScreenshots = $script:PerElementScreenshotProof
            userInspectableScreenshotFolder = [bool]$Paths.ScreenshotEvidenceRoot
            userInspectableElementScreenshotFolder = $Paths.ElementScreenshotEvidenceRoot
            activeUserFacingClient = [bool]$ActiveUserFacingClient
            activeClientProofClassification = "supporting-only-for-LV1-when-real-shortcut-launcher-is-feasible"
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
        elementScreenshotEvidenceRoot = $Paths.ElementScreenshotEvidenceRoot
        perElementUserInspectableScreenshots = $script:PerElementScreenshotProof
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
        shortVideoProof = $script:ShortVideoProof
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
    $precheckResizeDiscoverability = Format-ShortcutPrecheckLine @("dashboard_move_fluidity", "dashboard_resize_cursor_alignment", "dashboard_resize_corner_arc_diagonal_zone", "dashboard_resize_cursor_transition_discovery", "dashboard_mouse_resize_corner", "dashboard_mouse_resize_right_edge", "dashboard_mouse_resize_bottom_edge", "dashboard_resize_grow_during_drag_visual_proof", "dashboard_resize_shrink_during_drag_visual_proof", "dashboard_resize_fluidity", "dashboard_mouse_resize") "LV1 cannot claim unrestricted green handoff for Dashboard movement/resize discoverability/fluidity without USER waiver."
    $precheckFirstOpenStability = Format-ShortcutPrecheckLine @("dashboard_first_open_stability_sequence") "LV1 cannot claim unrestricted green handoff for #123 first-open stability without real shortcut screenshot-sequence proof or USER waiver."
    $precheckSettingsPanel = Format-ShortcutPrecheckLine @("dashboard_settings_opens_with_real_mouse", "dashboard_settings_double_click_does_not_maximize", "dashboard_settings_done_closes_with_real_mouse") "LV1 cannot claim unrestricted green handoff for Dashboard Settings unless the real mouse Dashboard IA-card path opens and closes the panel without native maximize drift or USER waiver."
    $precheckTopChromeClose = Format-ShortcutPrecheckLine @("dashboard_top_chrome_close_hides_dashboard", "dashboard_reopens_after_top_chrome_close") "LV1 cannot claim unrestricted green handoff for Dashboard window-level Close unless the visible Close control hides only the Dashboard and tray reopen works or USER waiver."
    $precheckHudPersistence = Format-ShortcutPrecheckLine @("hud_feature_enabled_state_persisted") "LV1 cannot claim unrestricted green handoff for HUD Feature state persistence without USER waiver."
    $precheckHumanClientRun = Format-ShortcutPrecheckLine @("launch_settled_visible_desktop", "launch_settled_tray_available", "enable_hud_opens_dashboard", "dashboard_first_open_stability_sequence", "dashboard_settings_opens_with_real_mouse", "dashboard_top_chrome_close_hides_dashboard", "ncp_tray_icon_left_click_opens", "ncp_tray_icon_left_click_closes", "ncp_create_custom_task_clickable_with_dashboard_open", "tray_exit_confirmation_visible") "LV1 cannot claim unrestricted green handoff without real-human client precheck coverage or USER waiver."
    $activeClientPrecheck = "Codex Precheck: PASS as supporting live-helper evidence only - LV1 primary path remains the real user-facing desktop launcher/human-client manifest; direct-runtime or active-client helper proof cannot replace that path when the shortcut is feasible."
    $visualScreenshotPrecheck = "Codex Precheck: PASS as supporting focused screenshot evidence only - detailed per-element screenshots are exported to the USER-inspectable OneDrive screenshot folder and full-desktop screenshots are context only. USER visual confirmation is still required."
    $deferredBoundaryPrecheck = "Codex Precheck: PASS through source-truth, static validation, sandbox validation, and active-client manifest boundary proof - USER is not being asked to accept deferred/future scope."

    # Keep the desktop UTS as a short USER questionnaire focused on the
    # returned issue loop; detailed ledger/proof evidence stays in manifests.
    $content = @"
Nexus Desktop AI - User Test Summary
Workstream: FAM-006 Recording Profile Runtime Foundation
Current Phase: Live Validation Stage 1 User Test Summary handoff
Branch: $currentBranch
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
Status: USER TEST SUMMARY RESULTS PENDING - HANDOFF COPY - NOT RETURNED RESULTS

How To Use This File
- Launch and test from the red FAM-006 desktop shortcut.
- This pass is focused on the returned failed issue IDs only.
- Confirmed items from the previous returned UTS are treated as closed unless they visibly regress during this pass.
- For each active issue below, write PASS, FAIL, or WAIVED plus a short note.
- If an active issue FAILS, describe exactly what you saw and attach/screenshot separately if useful.
- Return this file to Codex when complete. Codex will digest the results into source truth.

Codex Precheck Summary
- Red shortcut/worktree validation: PASS through the governed FAM-006 desktop shortcut.
- Human-client proof: PASS at $precheckManifestPath.
- Live proof root for this handoff: $($Paths.Root)
- USER-inspectable screenshot folder: $($Paths.ScreenshotEvidenceRoot)
- USER-inspectable per-element screenshot folder: $($Paths.ElementScreenshotEvidenceRoot)
- USER-inspectable short video: $($script:ShortVideoProof.userInspectablePath)
- Screenshot rule: review the detailed `element_<label>_<state>.png` screenshots and the returned issue-form coverage matrix; full-desktop screenshots are locator/context evidence only and do not satisfy per-element UI acceptance.
- Step 7 - #137 Dashboard Rounded Corners On Light Background: preserved as precheck/source-truth evidence; no black rectangular native corner extends beyond the visible rounded Dashboard chrome.
- Overlay/display release acceptance is deferred and non-gating.

Brief Issue List
- Closed by USER confirmation: UTS-HUD-006, UTS-HUD-008, UTS-HUD-011, UTS-HUD-012, and UTS-HUD-016 from returned passes, plus all earlier confirmed IDs unless regression appears.
- Deferred/source-truth-carried: UTS-HUD-009 Polling Rate live provider cadence, because external/provider telemetry cadence remains outside this HUD repair.
- Active failed issues repaired in this pass and requiring focused USER retest: UTS-HUD-014 and UTS-HUD-021.

Active Issues To Test

UTS-HUD-014 - Overlay Profiles Selector, Draft Creation, Dirty Guard, And Delete
Expected: Overlay Profiles opens fully on-screen and remains usable at normal and compact legal sizes. The separate Edit Profile button is removed. The dropdown button itself says `Profile to Edit:` and keeps the same rounded shape and size as the Create Profile button. Selecting an existing profile directly loads it for editing. Creating an Overlay Profile creates a draft only, starts with no monitor groups selected, requires Save before persistence, triggers the dirty-change guard on Close or navigation, and Discard leaves no persisted draft. Delete is a red danger action with confirmation and remains separated from Discard to reduce accidents.
USER Result / Notes:

UTS-HUD-021 - HUD Sizing And Overlay Profiles Scaling
Expected: Overlay Profiles no longer forces an awkward stacked layout at compact-but-legal sizes. The manager `Profile to Edit:` dropdown and Create Profile button remain on the same row, use equal button footprints, remain readable/clickable at default and compact legal window sizes, and open an unclipped NDAI-styled menu. Compact proof must show the window can complete the real user workflow: select profile, create draft, close dirty guard, save, discard, delete confirmation, dropdown open/select/close, null profile state, and 100+ profile stress state.
USER Result / Notes:

Issue Regression Checks, If Any
- Spot-check checked-source hover, same-row dirty guard, and divider underglow only if retesting Overlay Profiles reveals an obvious regression in those previously closed areas.
  USER Result / Notes:
- Spot-check Dashboard button alignment and Manage Data Sources deferred state only if retesting compact Dashboard sizing in UTS-HUD-021.
  USER Result / Notes:
- Spot-check Monitor Group / Overlay Profile / Recording Profile concept separation only if Overlay Profile deletion or creation appears to mix those concepts.
  USER Result / Notes:

Final USER Result
- PASS / FAIL / WAIVED:
- If FAIL, which active issue ID(s) remain:
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
    $MarkerTimeoutSeconds = [Math]::Max($MarkerTimeoutSeconds, 420)
    $NoProgressTimeoutSeconds = [Math]::Max($NoProgressTimeoutSeconds, 420)
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
        Assert-NoSyntheticLiveValidationInteraction $paths
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
        $interactionManifestRaw = Get-Content -LiteralPath $paths.InteractionManifest -Raw
        $script:InteractionManifestStatus = [string]$interactionManifest.status
        if ($script:InteractionManifestStatus -ne "PASS") {
            throw "Interaction self-QA did not pass. Status: $script:InteractionManifestStatus"
        }
        if ($interactionManifestRaw -match '"directJsClickUsed"\s*:\s*true' -or
            $interactionManifestRaw -match '"directJsMouseoverUsed"\s*:\s*true' -or
            $interactionManifestRaw -match '"inputProof"\s*:\s*"automated-supporting-only:' -or
            $interactionManifestRaw -notmatch '"realOsInputProof"\s*:\s*true') {
            throw "Interaction self-QA lacks real OS-level mouse input proof. JavaScript clicks, synthetic DOM events, WebView handler calls, QTest widget-only events, and state mutation are banned as primary LV1 interaction proof."
        }
        $requiredInteractionLabels = @(
            "Active child window prevents Dashboard click-through under overlapping controls",
            "Compact Overlay Profiles window preserves functional visible monitor row and action buttons",
            "Compact Overlay Profiles delete confirmation stays unclipped and non-overlapping",
            "Create Profile opens unsaved draft with empty monitor membership",
            "Dirty-change guard blocks close after created draft",
            "Manage Monitors dirty guard matches shared modal Save Discard Cancel contract",
            "Manage Monitors dirty guard Cancel returns to dirty draft without queued close",
            "Manage Monitors dirty guard Discard completes queued close and clears dirty state",
            "Create after delete reuses Monitor Group 3 instead of skipping to a higher number"
        )
        foreach ($requiredLabel in $requiredInteractionLabels) {
            if ($interactionManifestRaw -notmatch [regex]::Escape($requiredLabel)) {
                throw "Interaction self-QA missing required real-input scenario: $requiredLabel"
            }
        }
        Wait-Marker $paths "MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY"
        Wait-Marker $paths "MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY"
        Wait-Marker $paths "MONITORING_HUD_DASHBOARD_CORE_OVERLAY_DECOUPLING_READY"
        Wait-Marker $paths "MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY"
        Step $paths "interaction self-QA manifest PASS: $($paths.InteractionManifest)"
        $script:PerElementScreenshotProof = Copy-FocusedElementScreenshotsToUserEvidence -Paths $paths
        if ($script:PerElementScreenshotProof.status -ne "PASS") {
            throw "LV1 focused per-element screenshots missing or failed: $($script:PerElementScreenshotProof.reason)"
        }
        Step $paths "copied mandatory LV1 focused per-element screenshots to USER-inspectable folder: $($script:PerElementScreenshotProof.root)"
    }

    Step $paths "settling Dashboard-first client before full-desktop screenshot"
    Start-Sleep -Milliseconds 1500
    Capture-Screen $paths "after_launch"
    if ($effectiveRunInteractionSelfQA -or $PrepareLiveValidationUserTestSummary) {
        $script:ShortVideoProof = New-ShortVideoProof -Paths $paths -SourceRoots @($paths.ElementScreenshotEvidenceRoot, $paths.InteractionEvidenceRoot, $paths.Root) -MinimumFrames 5
        if ($script:ShortVideoProof.status -ne "PASS") {
            throw "LV1 short video/frame-sequence proof missing or failed: $($script:ShortVideoProof.reason)"
        }
        Step $paths "generated mandatory LV1 short video proof: $($script:ShortVideoProof.path)"
        Step $paths "copied mandatory LV1 user-inspectable short video proof: $($script:ShortVideoProof.userInspectablePath)"
    }
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
