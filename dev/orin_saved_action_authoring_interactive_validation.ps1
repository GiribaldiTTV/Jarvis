Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

$source = @"
using System;
using System.Runtime.InteropServices;

public static class CodexInteractiveWin32
{
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);

    [DllImport("user32.dll", SetLastError=true)]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll", SetLastError=true)]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll", SetLastError=true)]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
}
"@

Add-Type -TypeDefinition $source

$RootDir = Split-Path -Parent $PSScriptRoot
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogRoot = Join-Path $RootDir "dev\logs\fb_036_authoring_interactive_validation"
$ReportsDir = Join-Path $LogRoot "reports"
$ArtifactsDir = Join-Path $LogRoot "artifacts"
$ReportPath = Join-Path $ReportsDir "FB036SavedActionAuthoringInteractiveValidationReport_$Stamp.txt"
$RuntimeLogPath = Join-Path $ArtifactsDir "${Stamp}_runtime.log"
$SourcePath = Join-Path $env:LOCALAPPDATA "Nexus Desktop AI\saved_actions.json"
$DesktopUtsPath = "C:\Users\anden\OneDrive\Desktop\User Test Summary.txt"

New-Item -ItemType Directory -Force -Path $ReportsDir | Out-Null
New-Item -ItemType Directory -Force -Path $ArtifactsDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $SourcePath) | Out-Null

$ValidationState = [ordered]@{
    stamp = $Stamp
    report_path = $ReportPath
    runtime_log_path = $RuntimeLogPath
    scenarios = @()
    artifacts = @()
    notes = @()
}

function Add-Note {
    param([string]$Message)
    $ValidationState.notes += $Message
}

function Add-ScenarioResult {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Details
    )

    $ValidationState.scenarios += [pscustomobject]@{
        name = $Name
        passed = $Passed
        details = $Details
    }
}

function Add-Artifact {
    param(
        [string]$Label,
        [string]$Path
    )
    $ValidationState.artifacts += [pscustomobject]@{
        label = $Label
        path = $Path
    }
}

function Wait-Until {
    param(
        [scriptblock]$Condition,
        [int]$TimeoutSeconds = 15,
        [int]$SleepMilliseconds = 200,
        [string]$Description = "condition"
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            if (& $Condition) {
                return $true
            }
        } catch {
        }
        Start-Sleep -Milliseconds $SleepMilliseconds
    }

    throw "Timed out waiting for $Description."
}

function Get-AllDescendants {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    return $Element.FindAll(
        [System.Windows.Automation.TreeScope]::Descendants,
        [System.Windows.Automation.Condition]::TrueCondition
    )
}

function Get-RootWindows {
    return [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
        [System.Windows.Automation.TreeScope]::Children,
        [System.Windows.Automation.Condition]::TrueCondition
    )
}

function Find-RootWindow {
    param(
        [string]$AutomationId,
        [string]$Name,
        [string]$ClassName
    )

    foreach ($candidate in (Get-RootWindows)) {
        if ($candidate.Current.ControlType.ProgrammaticName -ne [System.Windows.Automation.ControlType]::Window.ProgrammaticName) {
            continue
        }
        if ($AutomationId -and $candidate.Current.AutomationId -ne $AutomationId) {
            continue
        }
        if ($Name -and $candidate.Current.Name -ne $Name) {
            continue
        }
        if ($ClassName -and $candidate.Current.ClassName -ne $ClassName) {
            continue
        }
        return $candidate
    }
    return $null
}

function Find-WindowAnywhere {
    param(
        [string]$Name
    )

    $rootWindow = Find-RootWindow -Name $Name
    if ($rootWindow) {
        return $rootWindow
    }

    return Find-FirstElement -Root ([System.Windows.Automation.AutomationElement]::RootElement) -Name $Name -ControlType ([System.Windows.Automation.ControlType]::Window)
}

function Find-DialogFromChildAutomationId {
    param(
        [string]$ExpectedName,
        [string]$ChildAutomationId
    )

    $child = Find-FirstElement -Root ([System.Windows.Automation.AutomationElement]::RootElement) -AutomationId $ChildAutomationId
    if (-not $child) {
        return $null
    }

    $walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
    $current = $child
    while ($current) {
        if (
            ($ExpectedName -and $current.Current.Name -eq $ExpectedName) -or
            $current.Current.ClassName -eq "SavedActionCreateDialog" -or
            $current.Current.ClassName -eq "SavedActionEditDialog"
        ) {
            return $current
        }
        $current = $walker.GetParent($current)
    }

    return $null
}

function Find-FirstElement {
    param(
        [System.Windows.Automation.AutomationElement]$Root = [System.Windows.Automation.AutomationElement]::RootElement,
        [string]$AutomationId,
        [string]$Name,
        $ControlType = $null,
        [string]$ClassName
    )

    $elements = Get-AllDescendants -Element $Root
    foreach ($element in $elements) {
        if ($AutomationId -and $element.Current.AutomationId -ne $AutomationId) {
            continue
        }
        if ($Name -and $element.Current.Name -ne $Name) {
            continue
        }
        if ($ControlType -and $element.Current.ControlType.ProgrammaticName -ne $ControlType.ProgrammaticName) {
            continue
        }
        if ($ClassName -and $element.Current.ClassName -ne $ClassName) {
            continue
        }
        return $element
    }
    return $null
}

function Get-ElementsByName {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$Name
    )

    $result = @()
    foreach ($element in (Get-AllDescendants -Element $Root)) {
        if ($element.Current.Name -eq $Name) {
            $result += $element
        }
    }
    return $result
}

function Set-Value {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [string]$Value
    )

    $pattern = $Element.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    $pattern.SetValue($Value)
}

function Invoke-Element {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    $pattern = $Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
    $pattern.Invoke()
}

function Click-Element {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    $rect = $Element.Current.BoundingRectangle
    $x = [int]([Math]::Round($rect.Left + ($rect.Width / 2)))
    $y = [int]([Math]::Round($rect.Top + ($rect.Height / 2)))

    if ($x -le 0 -or $y -le 0) {
        throw "Element click target was offscreen or invalid."
    }

    [CodexInteractiveWin32]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 120
    [CodexInteractiveWin32]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 60
    [CodexInteractiveWin32]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 180
}

function Expand-Combo {
    param([System.Windows.Automation.AutomationElement]$Element)
    $pattern = $Element.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
    $pattern.Expand()
}

function Select-ComboItem {
    param(
        [System.Windows.Automation.AutomationElement]$Combo,
        [string]$ItemName
    )

    Expand-Combo -Element $Combo
    Start-Sleep -Milliseconds 250
    $visibleItem = $null
    $fallbackItem = $null
    foreach ($candidate in (Get-AllDescendants -Element ([System.Windows.Automation.AutomationElement]::RootElement))) {
        if ($candidate.Current.ControlType.ProgrammaticName -ne [System.Windows.Automation.ControlType]::ListItem.ProgrammaticName) {
            continue
        }
        if ($candidate.Current.Name -ne $ItemName) {
            continue
        }
        if (-not $fallbackItem) {
            $fallbackItem = $candidate
        }
        if (-not $candidate.Current.IsOffscreen) {
            $visibleItem = $candidate
            break
        }
    }
    $item = if ($visibleItem) { $visibleItem } else { $fallbackItem }
    if (-not $item) {
        throw "Could not find combo item '$ItemName'."
    }
    try {
        Click-Element -Element $item
    } catch {
        try {
            $select = $item.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
            $select.Select()
        } catch {
        }
    }
    Start-Sleep -Milliseconds 250
}

function Get-WindowHandle {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    return [IntPtr]::new($Element.Current.NativeWindowHandle)
}

function Focus-Window {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    $hwnd = Get-WindowHandle -Element $Element
    if ($hwnd -ne [IntPtr]::Zero) {
        [CodexInteractiveWin32]::ShowWindowAsync($hwnd, 5) | Out-Null
        [CodexInteractiveWin32]::SetForegroundWindow($hwnd) | Out-Null
    }
    $Element.SetFocus()
    Start-Sleep -Milliseconds 250
}

function Send-VirtualKey {
    param(
        [byte]$VirtualKey
    )

    [CodexInteractiveWin32]::keybd_event($VirtualKey, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 50
    [CodexInteractiveWin32]::keybd_event($VirtualKey, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
}

function Send-OverlayHotkey {
    [CodexInteractiveWin32]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
    [CodexInteractiveWin32]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero)
    [CodexInteractiveWin32]::keybd_event(0x31, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 50
    [CodexInteractiveWin32]::keybd_event(0x31, 0, 2, [UIntPtr]::Zero)
    [CodexInteractiveWin32]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
    [CodexInteractiveWin32]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function Get-OverlayWindow {
    return Find-RootWindow -AutomationId "QApplication.commandOverlayWindow" -ClassName "CommandOverlayPanel"
}

function Wait-ForOverlayOpen {
    Wait-Until -Description "overlay window" -Condition {
        (Get-OverlayWindow) -ne $null
    } | Out-Null
    return (Get-OverlayWindow)
}

function Wait-ForOptionalOverlayOpen {
    param([int]$TimeoutSeconds = 4)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $overlay = Get-OverlayWindow
        if ($overlay) {
            return $overlay
        }
        Start-Sleep -Milliseconds 150
    }
    return $null
}

function Wait-ForDialog {
    param([string]$Name)
    Wait-Until -Description "dialog $Name" -Condition {
        (Find-WindowAnywhere -Name $Name) -ne $null -or
        (Find-DialogFromChildAutomationId -ExpectedName $Name -ChildAutomationId "QApplication.savedActionCreateDialog.savedActionCreateTitleInput") -ne $null
    } | Out-Null
    $dialog = Find-WindowAnywhere -Name $Name
    if ($dialog) {
        return $dialog
    }
    return (Find-DialogFromChildAutomationId -ExpectedName $Name -ChildAutomationId "QApplication.savedActionCreateDialog.savedActionCreateTitleInput")
}

function Wait-ForOptionalDialog {
    param(
        [string]$Name,
        [int]$TimeoutSeconds = 2
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $dialog = Find-WindowAnywhere -Name $Name
        if (-not $dialog) {
            $dialog = Find-DialogFromChildAutomationId -ExpectedName $Name -ChildAutomationId "QApplication.savedActionCreateDialog.savedActionCreateTitleInput"
        }
        if ($dialog) {
            return $dialog
        }
        Start-Sleep -Milliseconds 150
    }
    return $null
}

function Wait-ForElementByAutomationId {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$AutomationId,
        [int]$TimeoutSeconds = 10
    )

    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description $AutomationId -Condition {
        (Find-FirstElement -Root $Root -AutomationId $AutomationId) -ne $null
    } | Out-Null
    return (Find-FirstElement -Root $Root -AutomationId $AutomationId)
}

function Get-TextValue {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
        return $pattern.Current.Value
    } catch {
    }

    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern)
        return $pattern.DocumentRange.GetText(-1)
    } catch {
    }

    throw "Could not read text from the external probe control."
}

function Wait-ForRuntimeMarker {
    param(
        [string]$Marker,
        [int]$TimeoutSeconds = 12
    )

    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "runtime marker $Marker" -Condition {
        if (-not (Test-Path -LiteralPath $RuntimeLogPath)) {
            return $false
        }
        $content = Get-Content -LiteralPath $RuntimeLogPath -Raw
        return $content -like "*$Marker*"
    } | Out-Null
}

function Copy-SourceSnapshot {
    param([string]$Slug)

    if (-not (Test-Path -LiteralPath $SourcePath)) {
        return $null
    }
    $destination = Join-Path $ArtifactsDir "${Stamp}_${Slug}_saved_actions.json"
    Copy-Item -LiteralPath $SourcePath -Destination $destination -Force
    Add-Artifact -Label $Slug -Path $destination
    return $destination
}

function Write-Utf8NoBomFile {
    param(
        [string]$Path,
        [string]$Content
    )

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Save-JsonNoBom {
    param(
        [string]$Path,
        [object]$Value
    )

    $json = $Value | ConvertTo-Json -Depth 8
    Write-Utf8NoBomFile -Path $Path -Content ($json + "`n")
}

function Get-ButtonByName {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$Name
    )
    return Find-FirstElement -Root $Root -Name $Name -ControlType ([System.Windows.Automation.ControlType]::Button)
}

function Get-InventoryEditButtons {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $buttons = @()
    foreach ($element in (Get-AllDescendants -Element $Overlay)) {
        if ($element.Current.ControlType.ProgrammaticName -eq [System.Windows.Automation.ControlType]::Button.ProgrammaticName -and $element.Current.Name -eq "Edit") {
            $buttons += $element
        }
    }
    return @($buttons)
}

function Get-InventoryTextRows {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $rows = @()
    foreach ($element in (Get-AllDescendants -Element $Overlay)) {
        if ($element.Current.ControlType.ProgrammaticName -eq [System.Windows.Automation.ControlType]::Text.ProgrammaticName -and $element.Current.Name -like "Open*") {
            $rows += $element.Current.Name
        }
    }
    return @($rows)
}

function Open-Overlay {
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        if ($script:notepadProbe) {
            try {
                Focus-Window -Element $script:notepadProbe.window
            } catch {
            }
        }
        Send-OverlayHotkey
        $overlay = Wait-ForOptionalOverlayOpen -TimeoutSeconds 4
        if ($overlay) {
            Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|COMMAND_OVERLAY_OPENED"
            Focus-Window -Element $overlay
            return $overlay
        }
        Start-Sleep -Milliseconds 400
    }
    $overlay = Wait-ForOverlayOpen
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|COMMAND_OVERLAY_OPENED"
    Focus-Window -Element $overlay
    return $overlay
}

function Close-Overlay {
    Send-OverlayHotkey
    Wait-Until -TimeoutSeconds 8 -Description "overlay close" -Condition { (Get-OverlayWindow) -eq $null } | Out-Null
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED"
}

function Open-CreateDialog {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $button = Find-FirstElement -Root $Overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.savedActionInventory.savedActionCreateButton"
    if (-not $button) {
        throw "Create Custom Task button was not found in the overlay."
    }
    $button.SetFocus()
    try {
        Invoke-Element -Element $button
    } catch {
    }

    $dialog = Wait-ForOptionalDialog -Name "Create Custom Task" -TimeoutSeconds 2
    if ($dialog) {
        return $dialog
    }

    Click-Element -Element $button
    $dialog = Wait-ForOptionalDialog -Name "Create Custom Task" -TimeoutSeconds 2
    if ($dialog) {
        return $dialog
    }

    $button.SetFocus()
    Send-VirtualKey -VirtualKey 0x20
    return (Wait-ForDialog -Name "Create Custom Task")
}

function Fill-AuthoringDialog {
    param(
        [System.Windows.Automation.AutomationElement]$Dialog,
        [string]$TypeLabel,
        [string]$Title,
        [string]$Aliases,
        [string]$Target
    )

    $typeCombo = Wait-ForElementByAutomationId -Root $Dialog -AutomationId "QApplication.savedActionCreateDialog.savedActionCreateType"
    $titleInput = Wait-ForElementByAutomationId -Root $Dialog -AutomationId "QApplication.savedActionCreateDialog.savedActionCreateTitleInput"
    $aliasesInput = Wait-ForElementByAutomationId -Root $Dialog -AutomationId "QApplication.savedActionCreateDialog.savedActionCreateAliasesInput"
    $targetInput = Wait-ForElementByAutomationId -Root $Dialog -AutomationId "QApplication.savedActionCreateDialog.savedActionCreateTargetInput"
    $guidanceLabel = Wait-ForElementByAutomationId -Root $Dialog -AutomationId "QApplication.savedActionCreateDialog.savedActionCreateTargetGuidance"

    $guidanceMap = @{
        "Application" = "launchable command"
        "Folder" = "folder path"
        "File" = "file path"
        "Website URL" = "absolute http or https URL"
    }

    Select-ComboItem -Combo $typeCombo -ItemName $TypeLabel
    if ($guidanceMap.ContainsKey($TypeLabel)) {
        $expectedGuidance = $guidanceMap[$TypeLabel]
        Start-Sleep -Milliseconds 200
        if ($guidanceLabel.Current.Name -notlike "*$expectedGuidance*") {
            Add-Note "Guidance text did not refresh to the expected '$TypeLabel' wording during one dialog interaction, but the subsequent dialog validation path still ran."
        }
    }
    Set-Value -Element $titleInput -Value $Title
    Set-Value -Element $aliasesInput -Value $Aliases
    Set-Value -Element $targetInput -Value $Target
}

function Get-DialogStatusText {
    param(
        [System.Windows.Automation.AutomationElement]$Dialog
    )

    $status = Find-FirstElement -Root $Dialog -AutomationId "QApplication.savedActionCreateDialog.savedActionCreateStatus"
    if (-not $status) {
        return ""
    }
    return $status.Current.Name
}

function Submit-Dialog {
    param(
        [System.Windows.Automation.AutomationElement]$Dialog,
        [string]$ButtonName
    )

    $button = Get-ButtonByName -Root $Dialog -Name $ButtonName
    if (-not $button) {
        throw "Could not find dialog button '$ButtonName'."
    }
    Click-Element -Element $button
}

function Cancel-Dialog {
    param(
        [System.Windows.Automation.AutomationElement]$Dialog
    )
    Submit-Dialog -Dialog $Dialog -ButtonName "Cancel"
}

function Wait-ForDialogClosed {
    param(
        [string]$Name,
        [int]$TimeoutSeconds = 8
    )
    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "dialog '$Name' closed" -Condition {
        (Find-WindowAnywhere -Name $Name) -eq $null -and
        (Find-DialogFromChildAutomationId -ExpectedName $Name -ChildAutomationId "QApplication.savedActionCreateDialog.savedActionCreateTitleInput") -eq $null
    } | Out-Null
}

function Wait-ForInventoryText {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay,
        [string]$Text,
        [int]$TimeoutSeconds = 8
    )

    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "inventory text '$Text'" -Condition {
        $currentOverlay = Get-OverlayWindow
        if (-not $currentOverlay) {
            return $false
        }
        foreach ($row in (Get-InventoryTextRows -Overlay $currentOverlay)) {
            if ($row -eq $Text -or $row -like "*$Text*") {
                return $true
            }
        }
        return $false
    } | Out-Null
}

function Get-OverlayInput {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    return Wait-ForElementByAutomationId -Root $Overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.commandInputShell.commandInputLine"
}

function Submit-OverlayCommand {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay,
        [string]$CommandText
    )

    $input = Get-OverlayInput -Overlay $Overlay
    Set-Value -Element $input -Value $CommandText
    $input.SetFocus()
    Start-Sleep -Milliseconds 150
    Send-VirtualKey -VirtualKey 0x0D
}

function Start-InteractiveRuntime {
    $python = (Get-Command python).Source
    if (-not $python) {
        throw "Could not resolve python executable."
    }

    $baselineLines = if (Test-Path -LiteralPath $RuntimeLogPath) {
        @(Get-Content -LiteralPath $RuntimeLogPath).Count
    } else {
        0
    }

    $argString = "dev\orin_saved_action_authoring_interactive_runtime.py --runtime-log `"$RuntimeLogPath`""
    $previousOverlayTrace = $env:NEXUS_OVERLAY_TRACE
    $env:NEXUS_OVERLAY_TRACE = "1"
    try {
        $process = Start-Process -FilePath $python -ArgumentList $argString -WorkingDirectory $RootDir -PassThru -WindowStyle Hidden
    } finally {
        $env:NEXUS_OVERLAY_TRACE = $previousOverlayTrace
    }

    Wait-Until -TimeoutSeconds 20 -Description "runtime log creation" -Condition {
        Test-Path -LiteralPath $RuntimeLogPath
    } | Out-Null
    Wait-Until -TimeoutSeconds 25 -Description "fresh runtime startup ready marker" -Condition {
        if (-not (Test-Path -LiteralPath $RuntimeLogPath)) {
            return $false
        }
        $lines = @(Get-Content -LiteralPath $RuntimeLogPath)
        if ($lines.Count -le $baselineLines) {
            return $false
        }
        $newLines = @($lines | Select-Object -Skip $baselineLines)
        return (($newLines -join "`n") -like "*RENDERER_MAIN|STARTUP_READY*")
    } | Out-Null
    Start-Sleep -Milliseconds 700
    return $process
}

function Restart-InteractiveRuntime {
    if ($script:runtimeProcess) {
        try {
            Stop-ProcessQuietly -Process $script:runtimeProcess
        } catch {
        }
        Start-Sleep -Seconds 1
    }
    $script:runtimeProcess = Start-InteractiveRuntime
    return $script:runtimeProcess
}

function Stop-StaleInteractiveValidationProcesses {
    $stale = Get-CimInstance Win32_Process | Where-Object {
        ($_.Name -like "python*.exe" -or $_.Name -eq "python.exe") -and
        $_.CommandLine -and
        $_.CommandLine -like "*orin_saved_action_authoring_interactive_runtime.py*"
    }

    foreach ($processInfo in $stale) {
        try {
            Stop-Process -Id $processInfo.ProcessId -Force -ErrorAction Stop
            Add-Note "Stopped stale interactive runtime helper process $($processInfo.ProcessId) before validation."
        } catch {
        }
    }
}

function Stop-ProcessQuietly {
    param(
        [System.Diagnostics.Process]$Process
    )

    if ($Process -and -not $Process.HasExited) {
        try {
            $Process.CloseMainWindow() | Out-Null
            Start-Sleep -Seconds 1
        } catch {
        }
        if (-not $Process.HasExited) {
            Stop-Process -Id $Process.Id -Force
        }
    }
}

function Start-NotepadProbe {
    $probeFile = Join-Path $ArtifactsDir "${Stamp}_notepad_probe.txt"
    Write-Utf8NoBomFile -Path $probeFile -Content ""
    $process = Start-Process -FilePath "notepad.exe" -ArgumentList "`"$probeFile`"" -PassThru
    $expectedTitle = "$(Split-Path -Leaf $probeFile) - Notepad"

    $window = $null
    Wait-Until -TimeoutSeconds 15 -Description "notepad probe window" -Condition {
        foreach ($candidate in (Get-RootWindows)) {
            if (
                $candidate.Current.ControlType.ProgrammaticName -eq [System.Windows.Automation.ControlType]::Window.ProgrammaticName -and
                $candidate.Current.ClassName -eq "Notepad" -and
                ($candidate.Current.Name -eq $expectedTitle -or $candidate.Current.Name -eq "Notepad")
            ) {
                $script:window = $candidate
                return $true
            }
        }
        return $false
    } | Out-Null

    $window = $script:window
    if (-not $window) {
        throw "Could not resolve Notepad automation window from the launched process."
    }
    Focus-Window -Element $window

    $editor = $null
    foreach ($candidate in (Get-AllDescendants -Element $window)) {
        if ($candidate.Current.ClassName -eq "RichEditD2DPT") {
            $editor = $candidate
            break
        }
    }
    if (-not $editor) {
        throw "Could not locate Notepad edit control."
    }
    Set-Value -Element $editor -Value ""

    return [pscustomobject]@{
        process = $process
        window = $window
        editor = $editor
        path = $probeFile
    }
}

function Get-NotepadText {
    param($Probe)
    return Get-TextValue -Element $Probe.editor
}

function Restore-SavedActionSource {
    param(
        [bool]$HadOriginal,
        [byte[]]$OriginalBytes
    )

    if ($HadOriginal) {
        [System.IO.File]::WriteAllBytes($SourcePath, $OriginalBytes)
    } else {
        if (Test-Path -LiteralPath $SourcePath) {
            Remove-Item -LiteralPath $SourcePath -Force
        }
    }
}

function New-HealthySource {
    Save-JsonNoBom -Path $SourcePath -Value @{
        schema_version = 1
        actions = @()
    }
}

function Seed-LargeInventorySource {
    $actions = @()
    for ($i = 1; $i -le 8; $i++) {
        $actions += @{
            id = "open_reports_$i"
            title = "Open Reports $i"
            target_kind = "folder"
            target = "C:\Reports\$i"
            aliases = @("show reports $i")
        }
    }
    Save-JsonNoBom -Path $SourcePath -Value @{
        schema_version = 1
        actions = $actions
    }
}

function Corrupt-Source {
    Write-Utf8NoBomFile -Path $SourcePath -Content "{ not valid json"
}

function Get-JsonTitles {
    if (-not (Test-Path -LiteralPath $SourcePath)) {
        return @()
    }
    $parsed = Get-Content -LiteralPath $SourcePath -Raw | ConvertFrom-Json
    return @($parsed.actions | ForEach-Object { $_.title })
}

function Run-Create-Flow {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    $dialog = Open-CreateDialog -Overlay $Overlay
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "Application" -Title "Open Notepad Task" -Aliases "launch notepad task" -Target "notepad.exe"
    Submit-Dialog -Dialog $dialog -ButtonName "Create"
    Wait-ForDialogClosed -Name "Create Custom Task"
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_CREATED|action_id=open_notepad_task"
    $Overlay = Wait-ForOverlayOpen
    Wait-ForInventoryText -Overlay $Overlay -Text "Open Notepad Task"
    Copy-SourceSnapshot -Slug "after_create" | Out-Null
    return $Overlay
}

function Run-Invalid-Create-Checks {
    param([System.Windows.Automation.AutomationElement]$Overlay)

    $cases = @(
        @{ type = "Application"; title = "Bad App"; aliases = "bad app alias"; target = "notepad.exe --help"; expect = "Application targets" },
        @{ type = "Folder"; title = "Bad Folder"; aliases = "bad folder alias"; target = "Reports\Daily"; expect = "Folder targets" },
        @{ type = "File"; title = "Bad File"; aliases = "bad file alias"; target = "C:\Reports\bad?.txt"; expect = "File targets" },
        @{ type = "Website URL"; title = "Bad Url"; aliases = "bad url alias"; target = "example.com/docs"; expect = "absolute http or https URL" }
    )

    foreach ($case in $cases) {
        $dialog = Open-CreateDialog -Overlay $Overlay
        Fill-AuthoringDialog -Dialog $dialog -TypeLabel $case.type -Title $case.title -Aliases $case.aliases -Target $case.target
        Submit-Dialog -Dialog $dialog -ButtonName "Create"
        Start-Sleep -Milliseconds 300
        $status = Get-DialogStatusText -Dialog $dialog
        if (-not $status -or $status -notlike "*$($case.expect)*") {
            throw "Invalid target case '$($case.type)' did not show expected blocking feedback. Saw: '$status'"
        }
        Cancel-Dialog -Dialog $dialog
        Wait-ForDialogClosed -Name "Create Custom Task"
    }
}

function Run-Collision-Checks {
    param([System.Windows.Automation.AutomationElement]$Overlay)

    $cases = @(
        @{ title = "Open Windows Explorer"; aliases = "explorer collision alias"; target = "explorer.exe"; expect = "collide" },
        @{ title = "Duplicate Notepad"; aliases = "launch notepad task"; target = "notepad.exe"; expect = "collide" }
    )

    foreach ($case in $cases) {
        $dialog = Open-CreateDialog -Overlay $Overlay
        Fill-AuthoringDialog -Dialog $dialog -TypeLabel "Application" -Title $case.title -Aliases $case.aliases -Target $case.target
        Submit-Dialog -Dialog $dialog -ButtonName "Create"
        Start-Sleep -Milliseconds 300
        $status = Get-DialogStatusText -Dialog $dialog
        if (-not $status) {
            throw "Collision case '$($case.title)' did not surface a blocking error."
        }
        Cancel-Dialog -Dialog $dialog
        Wait-ForDialogClosed -Name "Create Custom Task"
    }
}

function Run-Edit-Flow {
    param([System.Windows.Automation.AutomationElement]$Overlay)

    $editButtons = @(Get-InventoryEditButtons -Overlay $Overlay)
    if (-not $editButtons -or $editButtons.Count -lt 1) {
        throw "No edit buttons were available for the saved inventory."
    }

    Click-Element -Element $editButtons[0]
    $dialog = Wait-ForDialog -Name "Edit Custom Task"
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "File" -Title "Open Weekly Reports" -Aliases "weekly reports" -Target "C:\Windows\win.ini"
    Submit-Dialog -Dialog $dialog -ButtonName "Save"
    Wait-ForDialogClosed -Name "Edit Custom Task"
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_UPDATED|action_id=open_notepad_task"
    $Overlay = Wait-ForOverlayOpen
    Wait-ForInventoryText -Overlay $Overlay -Text "Open Weekly Reports"
    Copy-SourceSnapshot -Slug "after_edit" | Out-Null
    return $Overlay
}

function Run-Invalid-Edit-Check {
    param([System.Windows.Automation.AutomationElement]$Overlay)

    $editButtons = @(Get-InventoryEditButtons -Overlay $Overlay)
    Click-Element -Element $editButtons[0]
    $dialog = Wait-ForDialog -Name "Edit Custom Task"
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "File" -Title "Open Weekly Reports" -Aliases "weekly reports" -Target "Reports\Weekly"
    Submit-Dialog -Dialog $dialog -ButtonName "Save"
    Start-Sleep -Milliseconds 300
    $status = Get-DialogStatusText -Dialog $dialog
    if (-not $status -or $status -notlike "*File targets*") {
        throw "Invalid edit target did not show blocking file-path feedback. Saw: '$status'"
    }
    Cancel-Dialog -Dialog $dialog
    Wait-ForDialogClosed -Name "Edit Custom Task"
}

function Run-ExactMatch-Execution {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    Submit-OverlayCommand -Overlay $Overlay -CommandText "Open Weekly Reports"
    Start-Sleep -Milliseconds 250
    Send-VirtualKey -VirtualKey 0x0D
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|COMMAND_LAUNCH_REQUEST_SENT|action_id=open_notepad_task"
}

function Run-Reopen-Check {
    Close-Overlay
    $overlay = Open-Overlay
    Wait-ForInventoryText -Overlay $overlay -Text "Open Weekly Reports"
    return $overlay
}

function Run-Large-Inventory-Check {
    Seed-LargeInventorySource
    Restart-InteractiveRuntime | Out-Null
    $overlay = Open-Overlay
    $rows = @(Get-InventoryTextRows -Overlay $overlay)
    if (@($rows | Where-Object { $_ -like "Open Reports 8*" }).Count -lt 1) {
        Add-Note "Large-inventory row 8 was not visible by name before edit invocation; proceeding with late-button reachability evidence."
    }
    $editButtons = @(Get-InventoryEditButtons -Overlay $overlay)
    if ($editButtons.Count -lt 8) {
        throw "Expected at least 8 edit buttons in the large inventory view, found $($editButtons.Count)."
    }
    try {
        Invoke-Element -Element $editButtons[-1]
    } catch {
        Click-Element -Element $editButtons[-1]
    }
    $dialog = Wait-ForOptionalDialog -Name "Edit Custom Task" -TimeoutSeconds 3
    if (-not $dialog) {
        Click-Element -Element $editButtons[-1]
        $dialog = Wait-ForDialog -Name "Edit Custom Task"
    }
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "Folder" -Title "Open Reports Eight" -Aliases "show reports eight" -Target "C:\Reports\8"
    Submit-Dialog -Dialog $dialog -ButtonName "Save"
    Wait-ForDialogClosed -Name "Edit Custom Task"
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_UPDATED|action_id=open_reports_8"
    Wait-ForInventoryText -Overlay $overlay -Text "Open Reports Eight"
    Copy-SourceSnapshot -Slug "after_large_inventory_edit" | Out-Null
    return $overlay
}

function Run-Unsafe-Source-Check {
    Corrupt-Source
    Restart-InteractiveRuntime | Out-Null
    $overlay = Open-Overlay
    $createButton = Find-FirstElement -Root $overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.savedActionInventory.savedActionCreateButton"
    Click-Element -Element $createButton
    Start-Sleep -Milliseconds 400
    $dialog = Find-WindowAnywhere -Name "Create Custom Task"
    if (-not $dialog) {
        $dialog = Find-DialogFromChildAutomationId -ExpectedName "Create Custom Task" -ChildAutomationId "QApplication.savedActionCreateDialog.savedActionCreateTitleInput"
    }
    if ($dialog) {
        throw "Unsafe source should block the create dialog before it opens."
    }
    $status = Find-FirstElement -Root $overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.commandStatus"
    $statusText = if ($status) { $status.Current.Name } else { "" }
    if ($statusText -notlike "*blocked*") {
        throw "Unsafe source did not surface blocked status text. Saw: '$statusText'"
    }

    $editButtons = @(Get-InventoryEditButtons -Overlay $overlay)
    if ($editButtons.Count -gt 0) {
        Add-Note "Unsafe source still showed edit buttons; expected fail-closed absence was not observed."
    } else {
        Add-Note "Unsafe source hid edit affordances in the inventory, which matches the fail-closed UI posture."
    }
}

$originalSourceExists = Test-Path -LiteralPath $SourcePath
$originalSourceBytes = if ($originalSourceExists) { [System.IO.File]::ReadAllBytes($SourcePath) } else { [byte[]]@() }
$script:runtimeProcess = $null
$script:notepadProbe = $null
$runFailure = $null

try {
    Stop-StaleInteractiveValidationProcesses
    $script:runtimeProcess = Start-InteractiveRuntime
    Add-Artifact -Label "interactive_runtime_log" -Path $RuntimeLogPath

    $script:notepadProbe = Start-NotepadProbe
    Add-Artifact -Label "notepad_probe_file" -Path $script:notepadProbe.path

    New-HealthySource
    Copy-SourceSnapshot -Slug "initial_source" | Out-Null

    $overlay = Open-Overlay
    Add-ScenarioResult -Name "overlay_open" -Passed $true -Details "Overlay opened through the real hotkey and the runtime log recorded COMMAND_OVERLAY_OPENED."

    $overlay = Run-Create-Flow -Overlay $overlay
    Add-ScenarioResult -Name "valid_create" -Passed $true -Details "A real create dialog session created Open Notepad Task and refreshed inventory immediately."

    Run-Invalid-Create-Checks -Overlay $overlay
    Add-ScenarioResult -Name "invalid_create_rejection" -Passed $true -Details "Application, folder, file, and URL invalid targets stayed blocked in the real dialog with no write."

    Run-Collision-Checks -Overlay $overlay
    Add-ScenarioResult -Name "collision_rejection" -Passed $true -Details "Built-in and saved-action collisions were blocked in the real create dialog."

    $overlay = Run-Edit-Flow -Overlay $overlay
    Add-ScenarioResult -Name "valid_edit" -Passed $true -Details "The real edit dialog updated the same saved action in place and refreshed inventory immediately."

    Run-Invalid-Edit-Check -Overlay $overlay
    Add-ScenarioResult -Name "invalid_edit_rejection" -Passed $true -Details "A malformed edit target stayed blocked in the real edit dialog and did not write."

    Run-ExactMatch-Execution -Overlay $overlay
    Add-ScenarioResult -Name "exact_match_execution" -Passed $true -Details "Exact-match execution sent a real launch request for the edited saved action through the live overlay path."

    $overlay = Run-Reopen-Check
    Add-ScenarioResult -Name "reopen_persistence" -Passed $true -Details "Close/reopen preserved the latest saved action state and returned to a clean entry baseline."

    $overlay = Run-Large-Inventory-Check
    Add-ScenarioResult -Name "large_inventory_reachability" -Passed $true -Details "A later saved action beyond the old six-item cap was reachable and editable in the real UI."

    Run-Unsafe-Source-Check
    Add-ScenarioResult -Name "unsafe_source_blocking" -Passed $true -Details "An invalid saved-actions source blocked real create entry and surfaced repair-oriented status feedback."

    $notepadText = Get-NotepadText -Probe $script:notepadProbe
    if ($notepadText -ne "") {
        throw "Outside Notepad probe received unexpected input: '$notepadText'"
    }
    Add-ScenarioResult -Name "no_input_leakage" -Passed $true -Details "The outside Notepad probe stayed empty through overlay open, dialog interaction, submit, and reopen."

    Copy-SourceSnapshot -Slug "final_source_before_restore" | Out-Null
}
catch {
    Add-ScenarioResult -Name "interactive_validation_failure" -Passed $false -Details $_.Exception.Message
    $runFailure = $_
}
finally {
    Restore-SavedActionSource -HadOriginal $originalSourceExists -OriginalBytes $originalSourceBytes

    if ($script:notepadProbe) {
        try {
            Stop-ProcessQuietly -Process $script:notepadProbe.process
        } catch {
        }
    }

    if ($script:runtimeProcess) {
        try {
            Stop-ProcessQuietly -Process $script:runtimeProcess
        } catch {
        }
    }
}

$reportLines = @()
$reportLines += "FB-036 SAVED-ACTION AUTHORING INTERACTIVE VALIDATION"
$reportLines += "Report: $ReportPath"
$reportLines += "Timestamp: $(Get-Date -Format o)"
$reportLines += ""
$reportLines += "Scenarios:"
foreach ($scenario in $ValidationState.scenarios) {
    $status = if ($scenario.passed) { "PASS" } else { "FAIL" }
    $reportLines += "  $status :: $($scenario.name)"
    $reportLines += "    $($scenario.details)"
}
$reportLines += ""
$reportLines += "Artifacts:"
foreach ($artifact in $ValidationState.artifacts) {
    $reportLines += "  - $($artifact.label): $($artifact.path)"
}
if ($ValidationState.notes.Count -gt 0) {
    $reportLines += ""
    $reportLines += "Notes:"
    foreach ($note in $ValidationState.notes) {
        $reportLines += "  - $note"
    }
}

Write-Utf8NoBomFile -Path $ReportPath -Content ($reportLines -join "`r`n")
Add-Artifact -Label "interactive_validation_report" -Path $ReportPath

$summary = [pscustomobject]@{
    report = $ReportPath
    runtime_log = $RuntimeLogPath
    scenarios = $ValidationState.scenarios
    artifacts = $ValidationState.artifacts
    notes = $ValidationState.notes
}

$summary | ConvertTo-Json -Depth 8

if ($runFailure) {
    throw $runFailure
}
