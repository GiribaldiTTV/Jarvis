param(
    [int]$StartupTimeoutSeconds = 45,
    [switch]$KeepRuntimeOpenOnFailure
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class Fam003VisibleInput {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr extra);
    [DllImport("user32.dll")] public static extern void keybd_event(byte key, byte scan, uint flags, UIntPtr extra);
    public static void LeftClick() { mouse_event(0x0002, 0, 0, 0, UIntPtr.Zero); mouse_event(0x0004, 0, 0, 0, UIntPtr.Zero); }
    public static void RightClick() { mouse_event(0x0008, 0, 0, 0, UIntPtr.Zero); mouse_event(0x0010, 0, 0, 0, UIntPtr.Zero); }
    public static void DoubleClick() { LeftClick(); System.Threading.Thread.Sleep(110); LeftClick(); }
    public static void Drag(int startX, int startY, int endX, int endY, int frames) {
        SetCursorPos(startX, startY); System.Threading.Thread.Sleep(180); mouse_event(0x0002, 0, 0, 0, UIntPtr.Zero);
        for (int i = 1; i <= frames; i++) {
            int x = startX + ((endX - startX) * i / frames);
            int y = startY + ((endY - startY) * i / frames);
            SetCursorPos(x, y); System.Threading.Thread.Sleep(70);
        }
        mouse_event(0x0004, 0, 0, 0, UIntPtr.Zero); System.Threading.Thread.Sleep(220);
    }
}
"@

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Launcher = Join-Path $env:USERPROFILE "OneDrive\Desktop\Nexus Desktop Launcher.lnk"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ProofRoot = Join-Path $Root "dev\logs\fam003_human_client_live_validation\$Stamp"
$FrameRoot = Join-Path $ProofRoot "ordered_frames"
$ManifestPath = Join-Path $ProofRoot "fam003_human_client_live_validation_manifest.json"
$LatestManifestPath = Join-Path $Root "dev\logs\fam003_human_client_live_validation\latest_manifest.json"
New-Item -ItemType Directory -Force -Path $FrameRoot | Out-Null
$script:Steps = New-Object System.Collections.Generic.List[object]
$script:Frames = New-Object System.Collections.Generic.List[object]
$script:RuntimeProcesses = @()
$script:Failure = ""

function Add-Step {
    param([string]$Id, [string]$Status, [string]$Detail, [hashtable]$Evidence = @{})
    $script:Steps.Add([ordered]@{
        id = $Id
        status = $Status
        codexPrecheck = $Status
        detail = $Detail
        evidence = $Evidence
        proofClass = "external-visible-human-client"
        timestamp = (Get-Date).ToUniversalTime().ToString("o")
    }) | Out-Null
}

function Capture-Frame {
    param([string]$Name)
    $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bitmap.Size)
        $path = Join-Path $FrameRoot ("{0:D3}_{1}.png" -f $script:Frames.Count, $Name)
        $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
        $script:Frames.Add([ordered]@{ index = $script:Frames.Count; path = $path; bytes = (Get-Item $path).Length }) | Out-Null
        return $path
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function Find-VisibleElement {
    param([string]$Name = "", [string]$Contains = "", [string]$Type = "", [int]$TimeoutSeconds = 8)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $all = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition
        )
        for ($i = 0; $i -lt $all.Count; $i++) {
            $element = $all.Item($i)
            try {
                $currentName = [string]$element.Current.Name
                $currentType = [string]$element.Current.ControlType.ProgrammaticName
                $rect = $element.Current.BoundingRectangle
                if ($rect.IsEmpty -or $element.Current.IsOffscreen) { continue }
                if ($Name -and $currentName -ne $Name) { continue }
                if ($Contains -and $currentName -notlike "*$Contains*") { continue }
                if ($Type -and $currentType -ne $Type) { continue }
                return $element
            } catch {}
        }
        Start-Sleep -Milliseconds 220
    }
    return $null
}

function Element-Evidence {
    param([object]$Element)
    if (-not $Element) { return @{ visible = $false } }
    $rect = $Element.Current.BoundingRectangle
    return @{
        visible = (-not $rect.IsEmpty -and -not $Element.Current.IsOffscreen)
        enabled = [bool]$Element.Current.IsEnabled
        name = [string]$Element.Current.Name
        controlType = [string]$Element.Current.ControlType.ProgrammaticName
        rect = @([int]$rect.Left, [int]$rect.Top, [int]($rect.Left + $rect.Width), [int]($rect.Top + $rect.Height))
    }
}

function Move-And-Click {
    param([object]$Element, [ValidateSet("left", "right", "double")][string]$Button = "left")
    if (-not $Element) { throw "Visible target is missing" }
    $rect = $Element.Current.BoundingRectangle
    if ($rect.IsEmpty -or $Element.Current.IsOffscreen) { throw "Visible target is offscreen" }
    $x = [int]($rect.Left + ($rect.Width / 2))
    $y = [int]($rect.Top + ($rect.Height / 2))
    [Fam003VisibleInput]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 180
    if ($Button -eq "right") { [Fam003VisibleInput]::RightClick() }
    elseif ($Button -eq "double") { [Fam003VisibleInput]::DoubleClick() }
    else { [Fam003VisibleInput]::LeftClick() }
    Start-Sleep -Milliseconds 500
    return @($x, $y)
}

function Find-RuntimeProcesses {
    $escapedRoot = [regex]::Escape($Root)
    return @(Get-CimInstance Win32_Process | Where-Object {
        $_.CommandLine -match $escapedRoot -and
        ($_.CommandLine -like "*orin_desktop_launcher.pyw*" -or $_.CommandLine -like "*orin_desktop_main.py*")
    })
}

function Wait-For-Runtime {
    $deadline = (Get-Date).AddSeconds($StartupTimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $processes = Find-RuntimeProcesses
        if ($processes.Count -gt 0) { return $processes }
        Start-Sleep -Milliseconds 300
    }
    return @()
}

function Open-TrayMenu {
    $tray = Find-VisibleElement -Name "Nexus Desktop AI" -Type "ControlType.Button" -TimeoutSeconds 4
    if (-not $tray) {
        $overflow = Find-VisibleElement -Contains "Hidden" -Type "ControlType.Button" -TimeoutSeconds 3
        if ($overflow) { Move-And-Click $overflow | Out-Null; Start-Sleep -Milliseconds 500 }
        $tray = Find-VisibleElement -Name "Nexus Desktop AI" -Type "ControlType.Button" -TimeoutSeconds 6
    }
    if (-not $tray) { throw "Nexus Desktop AI tray icon is not visible through the notification area or hidden-icons overflow" }
    $evidence = Element-Evidence $tray
    $point = Move-And-Click $tray -Button right
    $global = Find-VisibleElement -Name "Global Settings" -TimeoutSeconds 5
    if (-not $global) { throw "Visible tray right-click did not expose Global Settings" }
    return @{ tray = $evidence; clickPoint = $point; globalSettings = (Element-Evidence $global) }
}

function Inspect-Submenu {
    param([string]$Parent, [string]$Child)
    $parentElement = Find-VisibleElement -Name $Parent -TimeoutSeconds 4
    if (-not $parentElement) { return @{ status = "MISSING"; parent = @{ visible = $false }; child = @{ visible = $false } } }
    $parentEvidence = Element-Evidence $parentElement
    $rect = $parentElement.Current.BoundingRectangle
    [Fam003VisibleInput]::SetCursorPos([int]($rect.Left + ($rect.Width / 2)), [int]($rect.Top + ($rect.Height / 2))) | Out-Null
    Start-Sleep -Milliseconds 700
    $childElement = Find-VisibleElement -Name $Child -TimeoutSeconds 3
    return @{
        status = $(if ($childElement) { "PASS" } else { "FAIL" })
        parent = $parentEvidence
        child = (Element-Evidence $childElement)
    }
}

try {
    $head = (& git -C $Root rev-parse HEAD).Trim()
    $branch = (& git -C $Root branch --show-current).Trim()
    $shortcut = New-Object -ComObject WScript.Shell
    $link = $shortcut.CreateShortcut($Launcher)
    $launcherValid = (
        (Test-Path -LiteralPath $Launcher) -and
        ([System.IO.Path]::GetFullPath([string]$link.TargetPath).StartsWith([System.IO.Path]::GetFullPath($Root), [System.StringComparison]::OrdinalIgnoreCase)) -and
        ([System.IO.Path]::GetFullPath([string]$link.WorkingDirectory).TrimEnd('\') -eq [System.IO.Path]::GetFullPath($Root).TrimEnd('\'))
    )
    Add-Step "formal_launcher_provenance" $(if ($launcherValid) { "PASS" } else { "FAIL" }) "Exact USER Desktop shortcut target and working directory must resolve to the active FAM-003 root." @{
        launcherPath = $Launcher; targetPath = $link.TargetPath; workingDirectory = $link.WorkingDirectory; exactPathMatch = [bool]$launcherValid
    }
    if (-not $launcherValid) { throw "Exact USER Desktop launcher provenance is invalid" }

    $beforeLaunch = Capture-Frame "before_exact_launcher_open"
    Start-Process explorer.exe -ArgumentList "/select,`"$Launcher`""
    $launcherItem = Find-VisibleElement -Contains "Nexus Desktop Launcher" -TimeoutSeconds 10
    if (-not $launcherItem) { throw "File Explorer did not expose the exact USER Desktop launcher as a visible item" }
    $launcherEvidence = Element-Evidence $launcherItem
    $launchPoint = Move-And-Click $launcherItem -Button double
    $afterLaunch = Capture-Frame "after_exact_launcher_double_click"
    Add-Step "visible_exact_launcher_activation" "PASS" "The exact Desktop shortcut was selected in visible File Explorer and double-clicked with real pointer input." @{
        before = $beforeLaunch; after = $afterLaunch; item = $launcherEvidence; clickPoint = $launchPoint; directProcessLaunch = $false; environmentInjection = $false
    }

    $script:RuntimeProcesses = Wait-For-Runtime
    if ($script:RuntimeProcesses.Count -eq 0) { throw "Exact Desktop shortcut did not start a FAM-003 runtime process" }
    Add-Step "runtime_process_provenance" "PASS" "Runtime process command lines resolve to the active FAM-003 root." @{
        processes = @($script:RuntimeProcesses | ForEach-Object { @{ pid = $_.ProcessId; commandLine = $_.CommandLine } })
    }
    Start-Sleep -Seconds 4

    $trayOpen = Open-TrayMenu
    $trayFrame = Capture-Frame "tray_compact_menu_open"
    $quick = Inspect-Submenu "Quick Access" "Command Overlay"
    $quickFrame = Capture-Frame "tray_quick_access_submenu_open"
    [System.Windows.Forms.SendKeys]::SendWait("{ESC}")
    $null = Open-TrayMenu
    $ai = Inspect-Submenu "AI" "AI Status / Command Center"
    $aiFrame = Capture-Frame "tray_ai_submenu_open"
    [System.Windows.Forms.SendKeys]::SendWait("{ESC}")
    Add-Step "tray_compact_hierarchy" $(if ($quick.status -eq "PASS" -and $ai.status -eq "PASS") { "PASS" } else { "FAIL" }) "Visible right-click menu must expose real Quick Access and AI submenu children." @{
        open = $trayOpen; trayFrame = $trayFrame; quickAccess = $quick; quickFrame = $quickFrame; ai = $ai; aiFrame = $aiFrame; usedDirectHandler = $false
    }

    $null = Open-TrayMenu
    $hudParent = Find-VisibleElement -Name "HUD" -TimeoutSeconds 3
    $hudStatePath = Join-Path $env:LOCALAPPDATA "Nexus Desktop AI\monitoring_hud_state.json"
    $hudState = if (Test-Path $hudStatePath) { Get-Content $hudStatePath -Raw | ConvertFrom-Json } else { $null }
    if ($hudParent) {
        $hud = Inspect-Submenu "HUD" "Open HUD Dashboard"
        if ($hud.status -ne "PASS") { $hud = Inspect-Submenu "HUD" "Close HUD Dashboard" }
        $hudFrame = Capture-Frame "tray_hud_submenu_open"
        $hudAction = if ($hud.child.name) { Find-VisibleElement -Name ([string]$hud.child.name) -TimeoutSeconds 3 } else { $null }
        $hudActionPoint = if ($hudAction) { Move-And-Click $hudAction } else { $null }
        Start-Sleep -Milliseconds 900
        $hudWindow = Find-VisibleElement -Name "HUD Dashboard" -TimeoutSeconds 6
        $hudWindowEvidence = Element-Evidence $hudWindow
        $hudOpenedFrame = Capture-Frame "hud_dashboard_opened_from_resident_route"
        $closeState = @{ status = "MISSING" }
        if ($hudWindow) {
            $null = Open-TrayMenu
            $closeState = Inspect-Submenu "HUD" "Close HUD Dashboard"
        }
        $hudAlreadyOpenFrame = Capture-Frame "hud_dashboard_already_open_menu_state"
        $hudStatus = if ($hud.status -eq "PASS" -and $hudWindow -and $closeState.status -eq "PASS") { "PASS" } else { "FAIL" }
        Add-Step "hud_dashboard_resident_doorway" $hudStatus "The visible resident HUD submenu must activate the FAM-006-owned HUD Dashboard and then expose deterministic already-open menu state. The current source-truth label is HUD Dashboard; Overlay Dashboard is not admitted on this carrier." @{
            statePath = $hudStatePath; featureEnabled = [bool]$hudState.featureEnabled; submenu = $hud; submenuFrame = $hudFrame; actionClickPoint = $hudActionPoint; targetWindow = $hudWindowEvidence; openedFrame = $hudOpenedFrame; alreadyOpenState = $closeState; alreadyOpenFrame = $hudAlreadyOpenFrame; usedDirectHandler = $false; externalParentLauncherState = $(if ($hudStatus -eq "PASS") { "visible-route-activated" } elseif (-not $hudWindow) { "target-window-missing" } else { "already-open-state-missing" })
        }
    } else {
        $hudFrame = Capture-Frame "tray_hud_doorway_hidden_by_current_state"
        Add-Step "hud_dashboard_resident_doorway" "BLOCKED_SOURCE_TRUTH" "Current USER state has featureEnabled=false, and FAM-003 source truth requires USER-disabled optional feature doorways to stay hidden." @{
            statePath = $hudStatePath; featureEnabled = [bool]$hudState.featureEnabled; frame = $hudFrame; usedDirectHandler = $false; externalParentLauncherState = "not-exercisable-while-user-disabled"
        }
    }
    [System.Windows.Forms.SendKeys]::SendWait("{ESC}")

    $null = Open-TrayMenu
    $global = Find-VisibleElement -Name "Global Settings" -TimeoutSeconds 4
    $globalEvidence = Element-Evidence $global
    $globalPoint = Move-And-Click $global
    $settings = Find-VisibleElement -Name "Settings" -TimeoutSeconds 8
    if (-not $settings) { throw "Visible Global Settings tray action did not open the Settings window" }
    $settingsBefore = Element-Evidence $settings
    $settingsBeforeFrame = Capture-Frame "settings_before_live_resize"
    $rect = $settings.Current.BoundingRectangle
    [Fam003VisibleInput]::Drag([int]($rect.Right - 2), [int]($rect.Bottom - 2), [int]($rect.Right + 150), [int]($rect.Bottom + 90), 8)
    Start-Sleep -Milliseconds 700
    $settingsAfter = Find-VisibleElement -Name "Settings" -TimeoutSeconds 4
    $settingsAfterEvidence = Element-Evidence $settingsAfter
    $settingsAfterFrame = Capture-Frame "settings_after_live_resize"
    $widthBefore = $settingsBefore.rect[2] - $settingsBefore.rect[0]
    $widthAfter = $settingsAfterEvidence.rect[2] - $settingsAfterEvidence.rect[0]
    $resizePass = $settingsAfterEvidence.visible -and ($widthAfter -gt ($widthBefore + 80))
    Add-Step "settings_visible_route_and_live_resize" $(if ($resizePass) { "PASS" } else { "FAIL" }) "Global Settings must open from the visible tray action and resize through an external pointer drag." @{
        buttonVisibleAtInput = $globalEvidence.visible; clickPoint = $globalPoint; before = $settingsBefore; after = $settingsAfterEvidence; beforeFrame = $settingsBeforeFrame; afterFrame = $settingsAfterFrame; usedDirectHandler = $false
    }
    [System.Windows.Forms.SendKeys]::SendWait("%{F4}")
    Start-Sleep -Milliseconds 700

    $ncpTray = Find-VisibleElement -Name "Nexus Desktop AI" -Type "ControlType.Button" -TimeoutSeconds 5
    if (-not $ncpTray) { throw "Tray icon missing before NCP visible-input proof" }
    $ncpPoint = Move-And-Click $ncpTray
    Start-Sleep -Milliseconds 800
    $ncpEntry = Find-VisibleElement -Contains "O.R.I.N. Command Prompt" -TimeoutSeconds 5
    if (-not $ncpEntry) { $ncpEntry = Find-VisibleElement -Contains "Typed desktop interaction" -TimeoutSeconds 3 }
    $ncpEntryFrame = Capture-Frame "ncp_entry_opened_from_tray"
    [System.Windows.Forms.SendKeys]::SendWait("open nexus folder")
    $ncpTypedFrame = Capture-Frame "ncp_typed_input"
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    Start-Sleep -Milliseconds 900
    $ncpChoose = Find-VisibleElement -Contains "Multiple actions matched" -TimeoutSeconds 5
    $ncpChooseFrame = Capture-Frame "ncp_choose_visible_choices"
    if ($ncpChoose) {
        [System.Windows.Forms.SendKeys]::SendWait("2")
        Start-Sleep -Milliseconds 500
    }
    $ncpConfirm = Find-VisibleElement -Contains "Resolved action" -TimeoutSeconds 4
    $ncpConfirmFrame = Capture-Frame "ncp_confirm_selected_action"
    if ($ncpConfirm) {
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        Start-Sleep -Milliseconds 900
    }
    $ncpResult = Find-VisibleElement -Contains "Launch request sent" -TimeoutSeconds 5
    $ncpResultFrame = Capture-Frame "ncp_result_launch_requested"
    $ncpPass = $ncpEntry -and $ncpChoose -and $ncpConfirm -and $ncpResult
    Add-Step "ncp_visible_keyboard_flow" $(if ($ncpPass) { "PASS" } else { "FAIL" }) "NCP must open from the visible tray icon and expose visible typed, choose, confirm, and result states without direct handler calls." @{
        trayClickPoint = $ncpPoint; entry = (Element-Evidence $ncpEntry); entryFrame = $ncpEntryFrame; typedText = "open nexus folder"; typedFrame = $ncpTypedFrame; choose = (Element-Evidence $ncpChoose); chooseFrame = $ncpChooseFrame; confirm = (Element-Evidence $ncpConfirm); confirmFrame = $ncpConfirmFrame; result = (Element-Evidence $ncpResult); resultFrame = $ncpResultFrame; usedDirectHandler = $false
    }
} catch {
    $script:Failure = $_.Exception.Message
    Add-Step "human_client_exception" "FAIL" $script:Failure @{ stack = $_.ScriptStackTrace }
} finally {
    $blocking = @($script:Steps | Where-Object { $_.status -ne "PASS" })
    $status = if ($blocking.Count -eq 0) { "PASS" } else { "BLOCKED" }
    $payload = [ordered]@{
        schema = "fam003-external-visible-human-client-v1"
        status = $status
        timestamp = $Stamp
        worktree = $Root
        branch = (& git -C $Root branch --show-current).Trim()
        head = (& git -C $Root rev-parse HEAD).Trim()
        formalLauncherPath = $Launcher
        launcherActivationMethod = "visible-file-explorer-selected-item-double-click"
        directHandlerBypass = $false
        environmentInjectedRuntimeProof = $false
        utsStatus = "NOT_REQUESTED"
        steps = @($script:Steps)
        blockingRows = $blocking
        orderedFrames = @($script:Frames)
        orderedFrameCount = $script:Frames.Count
        proofRoot = $ProofRoot
        failure = $script:Failure
    }
    $json = $payload | ConvertTo-Json -Depth 14
    $json | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
    $json | Set-Content -LiteralPath $LatestManifestPath -Encoding UTF8

    if (-not $KeepRuntimeOpenOnFailure -or $status -eq "PASS") {
        foreach ($process in @(Find-RuntimeProcesses)) {
            try { Stop-Process -Id $process.ProcessId -Force -ErrorAction Stop } catch {}
        }
    }
    Write-Output "FAM-003 HUMAN CLIENT LV: $status"
    Write-Output "Proof Root: $ProofRoot"
    Write-Output "Manifest: $ManifestPath"
}
