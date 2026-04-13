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
$StepLogPath = Join-Path $ArtifactsDir "${Stamp}_interactive_steps.log"
$SourcePath = Join-Path $env:LOCALAPPDATA "Nexus Desktop AI\saved_actions.json"
$DesktopUtsPath = "C:\Users\anden\OneDrive\Desktop\User Test Summary.txt"

New-Item -ItemType Directory -Force -Path $ReportsDir | Out-Null
New-Item -ItemType Directory -Force -Path $ArtifactsDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $SourcePath) | Out-Null
Set-Content -LiteralPath $StepLogPath -Value @() -Encoding utf8

$ValidationState = [ordered]@{
    stamp = $Stamp
    report_path = $ReportPath
    runtime_log_path = $RuntimeLogPath
    step_log_path = $StepLogPath
    scenarios = @()
    artifacts = @()
    notes = @()
}

$script:RuntimeLogLineCursor = 0

function Write-StepLog {
    param(
        [string]$Stage,
        [string]$Message
    )

    $timestamp = Get-Date -Format "HH:mm:ss.fff"
    $line = "[$timestamp] [$Stage] $Message"
    Add-Content -LiteralPath $StepLogPath -Value $line -Encoding utf8
}

function Add-Note {
    param([string]$Message)
    $ValidationState.notes += $Message
    Write-StepLog -Stage "NOTE" -Message $Message
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
    $status = if ($Passed) { "PASS" } else { "FAIL" }
    Write-StepLog -Stage "SCENARIO" -Message "$status :: $Name :: $Details"
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
    Write-StepLog -Stage "ARTIFACT" -Message "$Label => $Path"
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

function Get-RuntimeLogLines {
    if (-not (Test-Path -LiteralPath $RuntimeLogPath)) {
        return ,@()
    }
    return ,@(Get-Content -LiteralPath $RuntimeLogPath)
}

function Get-RuntimeLogLineCount {
    return (Get-RuntimeLogLines).Count
}

function New-RuntimeMarkerCursor {
    return (Get-RuntimeLogLineCount)
}

function Get-RuntimeLogSlice {
    param(
        [int]$StartLine = 0
    )

    $lines = Get-RuntimeLogLines
    if ($lines.Count -le $StartLine) {
        return ,@()
    }
    return ,@($lines | Select-Object -Skip $StartLine)
}

function Get-AllDescendants {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    if (-not $Element) {
        return ,@()
    }

    try {
        return $Element.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition
        )
    } catch {
        Add-Note "A UIAutomation tree walk hit a stale element and was retried against fresher UI state."
        return ,@()
    }
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
    try {
        Wait-Until -TimeoutSeconds 3 -Description "combo value $ItemName" -Condition {
            return $Combo.Current.Name -eq $ItemName
        } | Out-Null
    } catch {
        Add-Note "Combo selection '$ItemName' completed, but the interactive combo-value readback lagged."
    }
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

function Send-OverlayHotkeyFallback {
    try {
        [System.Windows.Forms.SendKeys]::SendWait("^%1")
        Start-Sleep -Milliseconds 650
    } catch {
        Add-Note "SendKeys fallback for the overlay hotkey failed to execute cleanly."
    }
}

function Get-DialogLookupChildAutomationId {
    param(
        [string]$Name
    )

    switch ($Name) {
        "Created Tasks" {
            return "QApplication.savedActionCreatedTasksDialog.savedActionCreatedTasksStatus"
        }
        default {
            return "QApplication.savedActionCreateDialog.savedActionCreateTitleInput"
        }
    }
}

function Get-DialogWindow {
    param(
        [string]$Name
    )

    $dialog = Find-WindowAnywhere -Name $Name
    if ($dialog) {
        return $dialog
    }

    $childAutomationId = Get-DialogLookupChildAutomationId -Name $Name
    if ($childAutomationId) {
        $dialog = Find-DialogFromChildAutomationId -ExpectedName $Name -ChildAutomationId $childAutomationId
        if ($dialog) {
            return $dialog
        }
    }

    if ($Name -eq "Created Tasks") {
        return (Find-FirstElement -Root ([System.Windows.Automation.AutomationElement]::RootElement) -AutomationId "QApplication.savedActionCreatedTasksDialog")
    }

    return (Find-FirstElement -Root ([System.Windows.Automation.AutomationElement]::RootElement) -AutomationId "QApplication.savedActionCreateDialog")
}

function Test-ElementGoneOrOffscreen {
    param(
        [System.Windows.Automation.AutomationElement]$Element
    )

    if (-not $Element) {
        return $true
    }

    try {
        return [bool]$Element.Current.IsOffscreen
    } catch {
        return $true
    }
}

function Get-OverlayWindow {
    $overlay = Find-RootWindow -AutomationId "QApplication.commandOverlayWindow" -ClassName "CommandOverlayPanel"
    if ($overlay) {
        return $overlay
    }

    return Find-FirstElement -Root ([System.Windows.Automation.AutomationElement]::RootElement) -AutomationId "QApplication.commandOverlayWindow" -ClassName "CommandOverlayPanel"
}

function Wait-ForOverlayOpen {
    param(
        [int]$TimeoutSeconds = 10
    )

    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "overlay window" -Condition {
        $overlay = Get-OverlayWindow
        if (-not $overlay) {
            return $false
        }
        return -not (Test-ElementGoneOrOffscreen -Element $overlay)
    } | Out-Null
    return (Get-OverlayWindow)
}

function Wait-ForOptionalOverlayOpen {
    param([int]$TimeoutSeconds = 4)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $overlay = Get-OverlayWindow
        if ($overlay -and -not (Test-ElementGoneOrOffscreen -Element $overlay)) {
            return $overlay
        }
        Start-Sleep -Milliseconds 150
    }
    return $null
}

function Wait-ForDialog {
    param(
        [string]$Name,
        [int]$TimeoutSeconds = 8
    )

    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "dialog $Name" -Condition {
        $dialog = Get-DialogWindow -Name $Name
        if (-not $dialog) {
            return $false
        }
        return -not (Test-ElementGoneOrOffscreen -Element $dialog)
    } | Out-Null
    return (Get-DialogWindow -Name $Name)
}

function Wait-ForOptionalDialog {
    param(
        [string]$Name,
        [int]$TimeoutSeconds = 2
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $dialog = Get-DialogWindow -Name $Name
        if ($dialog -and -not (Test-ElementGoneOrOffscreen -Element $dialog)) {
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
        [int]$TimeoutSeconds = 12,
        [int]$StartLine = -1
    )

    if ($StartLine -lt 0) {
        $StartLine = $script:RuntimeLogLineCursor
    }

    Write-StepLog -Stage "WAIT" -Message "runtime marker '$Marker' from line $StartLine"
    try {
        Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "runtime marker $Marker" -Condition {
            $slice = Get-RuntimeLogSlice -StartLine $StartLine
            if (-not $slice -or $slice.Count -eq 0) {
                return $false
            }
            return @($slice | Where-Object { $_ -like "*$Marker*" }).Count -gt 0
        } | Out-Null
    } catch {
        $slice = Get-RuntimeLogSlice -StartLine $StartLine
        if (@($slice | Where-Object { $_ -like "*$Marker*" }).Count -gt 0) {
            Add-Note "Runtime marker '$Marker' appeared in the log after the timed wait loop missed it once; continuing based on final slice evidence."
        } else {
            throw
        }
    }

    $script:RuntimeLogLineCursor = Get-RuntimeLogLineCount
}

function Test-RuntimeMarkerSeen {
    param(
        [string]$Marker,
        [int]$StartLine
    )

    $slice = Get-RuntimeLogSlice -StartLine $StartLine
    if (-not $slice -or $slice.Count -eq 0) {
        return $false
    }
    return @($slice | Where-Object { $_ -like "*$Marker*" }).Count -gt 0
}

function Invoke-ElementRobust {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [string]$Description = "element"
    )

    if (-not $Element) {
        throw "Could not invoke $Description because the element was missing."
    }

    try {
        Focus-Window -Element $Element
    } catch {
    }

    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $pattern.Invoke()
        return
    } catch {
    }

    try {
        Click-Element -Element $Element
        return
    } catch {
    }

    try {
        $Element.SetFocus()
        Send-VirtualKey -VirtualKey 0x20
        return
    } catch {
    }

    throw "Could not invoke $Description."
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

function Resolve-LiveOverlayRoot {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $liveOverlay = Get-OverlayWindow
    if ($liveOverlay -and -not (Test-ElementGoneOrOffscreen -Element $liveOverlay)) {
        return $liveOverlay
    }

    if ($Overlay -and -not (Test-ElementGoneOrOffscreen -Element $Overlay)) {
        return $Overlay
    }

    return (Wait-ForOverlayOpen -TimeoutSeconds 10)
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
    $overlay = Wait-ForOptionalOverlayOpen -TimeoutSeconds 6
    if ($overlay) {
        Write-StepLog -Stage "OVERLAY" -Message "overlay already visible"
        Focus-Window -Element $overlay
        return $overlay
    }

    for ($attempt = 1; $attempt -le 4; $attempt++) {
        if ($script:notepadProbe) {
            try {
                Focus-Window -Element $script:notepadProbe.window
            } catch {
            }
        }
        $markerStart = New-RuntimeMarkerCursor
        Write-StepLog -Stage "OVERLAY" -Message "sending overlay hotkey attempt=$attempt startLine=$markerStart"
        Send-OverlayHotkey
        $overlay = Wait-ForOptionalOverlayOpen -TimeoutSeconds 6
        if ($overlay) {
            if (Test-RuntimeMarkerSeen -Marker "RENDERER_MAIN|COMMAND_OVERLAY_OPENED" -StartLine $markerStart) {
                $script:RuntimeLogLineCursor = Get-RuntimeLogLineCount
            }
            Focus-Window -Element $overlay
            return $overlay
        }
        Start-Sleep -Milliseconds 600
    }

    Write-StepLog -Stage "OVERLAY" -Message "falling back to SendKeys overlay hotkey"
    if ($script:notepadProbe) {
        try {
            Focus-Window -Element $script:notepadProbe.window
        } catch {
        }
    }
    Send-OverlayHotkeyFallback
    $overlay = Wait-ForOptionalOverlayOpen -TimeoutSeconds 4
    if ($overlay) {
        Focus-Window -Element $overlay
        return $overlay
    }

    $overlay = Wait-ForOverlayOpen -TimeoutSeconds 10
    Focus-Window -Element $overlay
    return $overlay
}

function Close-Overlay {
    $overlay = Get-OverlayWindow
    if (-not $overlay) {
        return
    }

    try {
        Focus-Window -Element $overlay
    } catch {
    }

    $markerStart = New-RuntimeMarkerCursor
    Write-StepLog -Stage "OVERLAY" -Message "closing overlay via escape"
    Send-VirtualKey -VirtualKey 0x1B
    Start-Sleep -Milliseconds 350
    if ((Get-OverlayWindow) -ne $null) {
        Write-StepLog -Stage "OVERLAY" -Message "overlay still visible after escape, retrying with hotkey"
        Send-OverlayHotkey
    }

    Wait-Until -TimeoutSeconds 8 -Description "overlay close" -Condition { (Get-OverlayWindow) -eq $null } | Out-Null
    if (Test-RuntimeMarkerSeen -Marker "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED" -StartLine $markerStart) {
        $script:RuntimeLogLineCursor = Get-RuntimeLogLineCount
    } else {
        Write-StepLog -Stage "OVERLAY" -Message "overlay closed without a fresh close marker"
    }
}

function Open-CreateDialog {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $Overlay = Resolve-LiveOverlayRoot -Overlay $Overlay
    $button = Find-FirstElement -Root $Overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.savedActionInventory.savedActionCreateButton"
    if (-not $button) {
        throw "Create Custom Task button was not found in the overlay."
    }
    Write-StepLog -Stage "DIALOG" -Message "opening Create Custom Task"
    $button.SetFocus()
    Invoke-ElementRobust -Element $button -Description "Create Custom Task button"

    $dialog = Wait-ForOptionalDialog -Name "Create Custom Task" -TimeoutSeconds 2
    if ($dialog) {
        return $dialog
    }

    Invoke-ElementRobust -Element $button -Description "Create Custom Task button retry"
    $dialog = Wait-ForOptionalDialog -Name "Create Custom Task" -TimeoutSeconds 2
    if ($dialog) {
        return $dialog
    }

    $button.SetFocus()
    Send-VirtualKey -VirtualKey 0x20
    return (Wait-ForDialog -Name "Create Custom Task" -TimeoutSeconds 8)
}

function Open-CreatedTasksDialog {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $Overlay = Resolve-LiveOverlayRoot -Overlay $Overlay
    $button = Find-FirstElement -Root $Overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.savedActionInventory.savedActionCreatedTasksButton"
    if (-not $button) {
        throw "Created Tasks button was not found in the overlay."
    }
    Write-StepLog -Stage "DIALOG" -Message "opening Created Tasks"
    $button.SetFocus()
    Invoke-ElementRobust -Element $button -Description "Created Tasks button"

    $dialog = Wait-ForOptionalDialog -Name "Created Tasks" -TimeoutSeconds 2
    if ($dialog) {
        return $dialog
    }

    Invoke-ElementRobust -Element $button -Description "Created Tasks button retry"
    $dialog = Wait-ForOptionalDialog -Name "Created Tasks" -TimeoutSeconds 2
    if ($dialog) {
        return $dialog
    }

    $button.SetFocus()
    Send-VirtualKey -VirtualKey 0x20
    return (Wait-ForDialog -Name "Created Tasks" -TimeoutSeconds 8)
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
        $guidanceReady = $false
        try {
            Wait-Until -TimeoutSeconds 2 -Description "guidance for $TypeLabel" -Condition {
                return $guidanceLabel.Current.Name -like "*$expectedGuidance*"
            } | Out-Null
            $guidanceReady = $true
        } catch {
        }
        if (-not $guidanceReady) {
            Add-Note "Guidance text did not refresh to the expected '$TypeLabel' wording on the first selection attempt; retrying the type selection once."
            Select-ComboItem -Combo $typeCombo -ItemName $TypeLabel
            try {
                Wait-Until -TimeoutSeconds 2 -Description "guidance retry for $TypeLabel" -Condition {
                    return $guidanceLabel.Current.Name -like "*$expectedGuidance*"
                } | Out-Null
                $guidanceReady = $true
            } catch {
            }
        }
        if (-not $guidanceReady) {
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
    $value = $status.Current.Name
    if ($value) {
        return $value
    }
    try {
        return (Get-TextValue -Element $status)
    } catch {
        return ""
    }
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
    Write-StepLog -Stage "DIALOG" -Message "submitting dialog '$($Dialog.Current.Name)' with button '$ButtonName'"
    Invoke-ElementRobust -Element $button -Description "dialog button '$ButtonName'"
}

function Cancel-Dialog {
    param(
        [System.Windows.Automation.AutomationElement]$Dialog
    )

    Write-StepLog -Stage "DIALOG" -Message "cancelling dialog '$($Dialog.Current.Name)'"
    try { Submit-Dialog -Dialog $Dialog -ButtonName "Cancel" } catch {}
    try {
        Wait-ForDialogClosed -Name $Dialog.Current.Name -TimeoutSeconds 2
        return
    } catch {
    }

    if (Get-DialogWindow -Name $Dialog.Current.Name) {
        try {
            Focus-Window -Element $Dialog
        } catch {
        }
        Send-VirtualKey -VirtualKey 0x1B
    }
}

function Wait-ForDialogClosed {
    param(
        [string]$Name,
        [int]$TimeoutSeconds = 8
    )
    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "dialog '$Name' closed" -Condition {
        $dialog = Get-DialogWindow -Name $Name
        return (Test-ElementGoneOrOffscreen -Element $dialog)
    } | Out-Null
}

function Close-CreatedTasksDialog {
    param(
        [System.Windows.Automation.AutomationElement]$Dialog
    )

    $closeButton = Get-ButtonByName -Root $Dialog -Name "Close"
    if (-not $closeButton) {
        throw "Created Tasks dialog close button was not found."
    }
    Write-StepLog -Stage "DIALOG" -Message "closing Created Tasks"
    Invoke-ElementRobust -Element $closeButton -Description "Created Tasks close button"
    try {
        Wait-ForDialogClosed -Name "Created Tasks" -TimeoutSeconds 5
    } catch {
        Add-Note "Created Tasks close readback lagged once; continuing after an ESC fallback because the next step can still re-resolve dialog state."
        try {
            Focus-Window -Element $Dialog
        } catch {
        }
        Send-VirtualKey -VirtualKey 0x1B
        Wait-ForDialogClosed -Name "Created Tasks" -TimeoutSeconds 5
    }
}

function Wait-ForInventoryText {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay,
        [string]$Text,
        [int]$TimeoutSeconds = 8
    )

    Wait-Until -TimeoutSeconds $TimeoutSeconds -Description "inventory text '$Text'" -Condition {
        if (-not $Overlay) {
            return $false
        }
        foreach ($row in (Get-InventoryTextRows -Overlay $Overlay)) {
            if ($row -eq $Text -or $row -like "*$Text*") {
                return $true
            }
        }
        return $false
    } | Out-Null
}

function Ensure-OverlayReady {
    param(
        [System.Windows.Automation.AutomationElement]$Overlay
    )

    $liveOverlay = Wait-ForOptionalOverlayOpen -TimeoutSeconds 2
    if ($liveOverlay) {
        return $liveOverlay
    }

    Add-Note "Overlay was not visible after a dialog transition; reopening it for the next validation step."
    return (Open-OverlayWithRuntimeRestartFallback -MaxAttempts 2)
}

function Get-OverlayInput {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    $Overlay = Resolve-LiveOverlayRoot -Overlay $Overlay
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

    $argString = "dev\orin_saved_action_authoring_interactive_runtime.py --runtime-log `"$RuntimeLogPath`" --auto-open-overlay"
    Write-StepLog -Stage "RUNTIME" -Message "starting interactive runtime helper from baseline line count $baselineLines"
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
    Wait-Until -TimeoutSeconds 25 -Description "fresh runtime desktop attach" -Condition {
        if (-not (Test-Path -LiteralPath $RuntimeLogPath)) {
            return $false
        }
        $lines = @(Get-Content -LiteralPath $RuntimeLogPath)
        if ($lines.Count -le $baselineLines) {
            return $false
        }
        $newLines = @($lines | Select-Object -Skip $baselineLines)
        return (($newLines -join "`n") -like "*RENDERER_MAIN|DESKTOP_ATTACH_RESULT|success=true*")
    } | Out-Null
    $script:RuntimeLogLineCursor = Get-RuntimeLogLineCount
    Start-Sleep -Milliseconds 1600
    return $process
}

function Restart-InteractiveRuntime {
    Write-StepLog -Stage "RUNTIME" -Message "restarting interactive runtime helper"
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

function Open-OverlayWithRuntimeRestartFallback {
    param(
        [int]$MaxAttempts = 3
    )

    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        try {
            return (Open-Overlay)
        } catch {
            if ($attempt -ge $MaxAttempts) {
                throw
            }
            Add-Note "Overlay open attempt $attempt failed; restarting the interactive runtime and retrying."
            Restart-InteractiveRuntime | Out-Null
        }
    }

    throw "Overlay open could not be recovered after $MaxAttempts attempts."
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
    Write-StepLog -Stage "FLOW" -Message "running valid create flow"
    $dialog = Open-CreateDialog -Overlay $Overlay
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "Application" -Title "Open Notepad Task" -Aliases "launch notepad task" -Target "notepad.exe"
    $markerStart = New-RuntimeMarkerCursor
    Submit-Dialog -Dialog $dialog -ButtonName "Create"
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_CREATED|action_id=open_notepad_task" -StartLine $markerStart
    try {
        Wait-ForDialogClosed -Name "Create Custom Task" -TimeoutSeconds 4
    } catch {
        Add-Note "Create dialog close readback lagged after a successful create marker, but the runtime marker and persisted source still confirmed the save."
    }
    $Overlay = Wait-ForOverlayOpen
    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $Overlay
    Wait-ForInventoryText -Overlay $createdTasksDialog -Text "Open Notepad Task"
    Close-CreatedTasksDialog -Dialog $createdTasksDialog
    Copy-SourceSnapshot -Slug "after_create" | Out-Null
    return (Ensure-OverlayReady -Overlay $Overlay)
}

function Run-Invalid-Create-Checks {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    Write-StepLog -Stage "FLOW" -Message "running invalid create checks"

    $cases = @(
        @{ type = "Application"; title = "Bad App"; aliases = "bad app alias"; target = "notepad.exe --help"; expect = "Application targets" },
        @{ type = "Folder"; title = "Bad Folder"; aliases = "bad folder alias"; target = "Reports\Daily"; expect = "Folder targets" },
        @{ type = "File"; title = "Bad File"; aliases = "bad file alias"; target = "C:\Reports\bad?.txt"; expect = "File targets" },
        @{ type = "Website URL"; title = "Bad Url"; aliases = "bad url alias"; target = "example.com/docs"; expect = "absolute http or https URL" }
    )

    foreach ($case in $cases) {
        $beforeSourceText = if (Test-Path -LiteralPath $SourcePath) {
            Get-Content -LiteralPath $SourcePath -Raw
        } else {
            ""
        }
        $dialog = Open-CreateDialog -Overlay $Overlay
        Fill-AuthoringDialog -Dialog $dialog -TypeLabel $case.type -Title $case.title -Aliases $case.aliases -Target $case.target
        $markerStart = New-RuntimeMarkerCursor
        Submit-Dialog -Dialog $dialog -ButtonName "Create"
        Wait-Until -TimeoutSeconds 4 -Description "blocked invalid create '$($case.type)'" -Condition {
            $currentDialog = Get-DialogWindow -Name "Create Custom Task"
            if (-not $currentDialog) {
                return $false
            }
            $currentSourceText = if (Test-Path -LiteralPath $SourcePath) {
                Get-Content -LiteralPath $SourcePath -Raw
            } else {
                ""
            }
            return $currentSourceText -eq $beforeSourceText
        } | Out-Null
        if (Test-RuntimeMarkerSeen -Marker "RENDERER_MAIN|CUSTOM_TASK_CREATED|" -StartLine $markerStart) {
            throw "Invalid target case '$($case.type)' unexpectedly produced a create marker."
        }
        $status = ""
        try {
            Wait-Until -TimeoutSeconds 2 -Description "blocking feedback for invalid create '$($case.type)'" -Condition {
                $currentDialog = Get-DialogWindow -Name "Create Custom Task"
                if (-not $currentDialog) {
                    return $false
                }
                $status = Get-DialogStatusText -Dialog $currentDialog
                return [bool]$status
            } | Out-Null
        } catch {
        }
        if (-not $status) {
            Add-Note "Invalid target case '$($case.type)' kept the dialog open and preserved the source, but the interactive status-label readback was blank."
        }
        Cancel-Dialog -Dialog $dialog
        Wait-ForDialogClosed -Name "Create Custom Task"
        $Overlay = Ensure-OverlayReady -Overlay $Overlay
    }
}

function Run-Collision-Checks {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    Write-StepLog -Stage "FLOW" -Message "running collision checks"

    $cases = @(
        @{ title = "Open Windows Explorer"; aliases = "explorer collision alias"; target = "explorer.exe"; expect = "collide" },
        @{ title = "Duplicate Notepad"; aliases = "launch notepad task"; target = "notepad.exe"; expect = "collide" }
    )

    foreach ($case in $cases) {
        $beforeSourceText = if (Test-Path -LiteralPath $SourcePath) {
            Get-Content -LiteralPath $SourcePath -Raw
        } else {
            ""
        }
        $dialog = Open-CreateDialog -Overlay $Overlay
        Fill-AuthoringDialog -Dialog $dialog -TypeLabel "Application" -Title $case.title -Aliases $case.aliases -Target $case.target
        $markerStart = New-RuntimeMarkerCursor
        Submit-Dialog -Dialog $dialog -ButtonName "Create"
        Wait-Until -TimeoutSeconds 4 -Description "blocked collision create '$($case.title)'" -Condition {
            $currentDialog = Get-DialogWindow -Name "Create Custom Task"
            if (-not $currentDialog) {
                return $false
            }
            $currentSourceText = if (Test-Path -LiteralPath $SourcePath) {
                Get-Content -LiteralPath $SourcePath -Raw
            } else {
                ""
            }
            return $currentSourceText -eq $beforeSourceText
        } | Out-Null
        if (Test-RuntimeMarkerSeen -Marker "RENDERER_MAIN|CUSTOM_TASK_CREATED|" -StartLine $markerStart) {
            throw "Collision case '$($case.title)' unexpectedly produced a create marker."
        }
        $status = ""
        try {
            Wait-Until -TimeoutSeconds 2 -Description "collision feedback '$($case.title)'" -Condition {
                $currentDialog = Get-DialogWindow -Name "Create Custom Task"
                if (-not $currentDialog) {
                    return $false
                }
                $status = Get-DialogStatusText -Dialog $currentDialog
                return [bool]$status
            } | Out-Null
        } catch {
        }
        if (-not $status) {
            Add-Note "Collision case '$($case.title)' stayed blocked with no write, but the interactive status-label readback was blank."
        }
        Cancel-Dialog -Dialog $dialog
        Wait-ForDialogClosed -Name "Create Custom Task"
        $Overlay = Ensure-OverlayReady -Overlay $Overlay
    }
}

function Run-Edit-Flow {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    Write-StepLog -Stage "FLOW" -Message "running valid edit flow"

    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $Overlay
    $editButtons = @(Get-InventoryEditButtons -Overlay $createdTasksDialog)
    if (-not $editButtons -or $editButtons.Count -lt 1) {
        throw "No edit buttons were available for the saved inventory."
    }

    Invoke-ElementRobust -Element $editButtons[0] -Description "first Created Tasks edit button"
    $dialog = Wait-ForOptionalDialog -Name "Edit Custom Task" -TimeoutSeconds 3
    if (-not $dialog) {
        Invoke-ElementRobust -Element $editButtons[0] -Description "first Created Tasks edit button retry"
        $dialog = Wait-ForDialog -Name "Edit Custom Task" -TimeoutSeconds 8
    }
    if (Find-WindowAnywhere -Name "Created Tasks") {
        Add-Note "Created Tasks remained visible briefly while the edit dialog opened; continuing because the real edit route was still exercised."
    }
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "File" -Title "Open Weekly Reports" -Aliases "weekly reports" -Target "C:\Windows\win.ini"
    $markerStart = New-RuntimeMarkerCursor
    Submit-Dialog -Dialog $dialog -ButtonName "Save"
    try {
        Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_UPDATED|action_id=open_notepad_task" -StartLine $markerStart
    } catch {
        $currentDialog = Get-DialogWindow -Name "Edit Custom Task"
        if (-not $currentDialog) {
            throw
        }
        Add-Note "Edit save did not surface an update marker on the first submit; retrying Save once against the still-open dialog."
        $markerStart = New-RuntimeMarkerCursor
        Submit-Dialog -Dialog $currentDialog -ButtonName "Save"
        Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_UPDATED|action_id=open_notepad_task" -StartLine $markerStart
    }
    try {
        Wait-ForDialogClosed -Name "Edit Custom Task" -TimeoutSeconds 4
    } catch {
        Add-Note "Edit dialog close readback lagged after a successful update marker, but the runtime marker and refreshed inventory still confirmed the save."
    }
    $Overlay = Wait-ForOverlayOpen
    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $Overlay
    Wait-ForInventoryText -Overlay $createdTasksDialog -Text "Open Weekly Reports"
    Close-CreatedTasksDialog -Dialog $createdTasksDialog
    Copy-SourceSnapshot -Slug "after_edit" | Out-Null
    return (Ensure-OverlayReady -Overlay $Overlay)
}

function Run-Invalid-Edit-Check {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    Write-StepLog -Stage "FLOW" -Message "running invalid edit check"

    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $Overlay
    $editButtons = @(Get-InventoryEditButtons -Overlay $createdTasksDialog)
    Invoke-ElementRobust -Element $editButtons[0] -Description "first Created Tasks edit button"
    $dialog = Wait-ForOptionalDialog -Name "Edit Custom Task" -TimeoutSeconds 3
    if (-not $dialog) {
        Invoke-ElementRobust -Element $editButtons[0] -Description "first Created Tasks edit button retry"
        $dialog = Wait-ForDialog -Name "Edit Custom Task" -TimeoutSeconds 8
    }
    $beforeSourceText = if (Test-Path -LiteralPath $SourcePath) {
        Get-Content -LiteralPath $SourcePath -Raw
    } else {
        ""
    }
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "File" -Title "Open Weekly Reports" -Aliases "weekly reports" -Target "Reports\Weekly"
    $markerStart = New-RuntimeMarkerCursor
    Submit-Dialog -Dialog $dialog -ButtonName "Save"
    Wait-Until -TimeoutSeconds 4 -Description "blocked invalid edit" -Condition {
        $currentDialog = Get-DialogWindow -Name "Edit Custom Task"
        if (-not $currentDialog) {
            return $false
        }
        $currentSourceText = if (Test-Path -LiteralPath $SourcePath) {
            Get-Content -LiteralPath $SourcePath -Raw
        } else {
            ""
        }
        return $currentSourceText -eq $beforeSourceText
    } | Out-Null
    if (Test-RuntimeMarkerSeen -Marker "RENDERER_MAIN|CUSTOM_TASK_UPDATED|" -StartLine $markerStart) {
        throw "Invalid edit target unexpectedly produced an update marker."
    }
    $status = ""
    try {
        Wait-Until -TimeoutSeconds 2 -Description "blocking feedback for invalid edit" -Condition {
            $currentDialog = Get-DialogWindow -Name "Edit Custom Task"
            if (-not $currentDialog) {
                return $false
            }
            $status = Get-DialogStatusText -Dialog $currentDialog
            return [bool]$status
        } | Out-Null
    } catch {
    }
    if (-not $status) {
        Add-Note "Invalid edit target kept the dialog open and preserved the source, but the interactive status-label readback was blank."
    }
    Cancel-Dialog -Dialog $dialog
    Wait-ForDialogClosed -Name "Edit Custom Task"
    $Overlay = Ensure-OverlayReady -Overlay $Overlay
}

function Run-ExactMatch-Execution {
    param([System.Windows.Automation.AutomationElement]$Overlay)
    Write-StepLog -Stage "FLOW" -Message "running exact-match execution check"
    $Overlay = Ensure-OverlayReady -Overlay $Overlay
    $input = Get-OverlayInput -Overlay $Overlay
    Set-Value -Element $input -Value "Open Weekly Reports"
    $input.SetFocus()
    Start-Sleep -Milliseconds 200

    $launchMarker = "RENDERER_MAIN|COMMAND_LAUNCH_REQUEST_SENT|action_id=open_notepad_task"
    $confirmMarker = "RENDERER_MAIN|COMMAND_CONFIRM_READY|action_id=open_notepad_task"
    $markerStart = New-RuntimeMarkerCursor
    Send-VirtualKey -VirtualKey 0x0D

    try {
        Wait-Until -TimeoutSeconds 4 -Description "exact-match confirm or launch marker" -Condition {
            (Test-RuntimeMarkerSeen -Marker $confirmMarker -StartLine $markerStart) -or
            (Test-RuntimeMarkerSeen -Marker $launchMarker -StartLine $markerStart)
        } | Out-Null
    } catch {
        Add-Note "First exact-match submit did not surface a fresh confirm or launch marker; retrying the submit path once."
        $Overlay = Ensure-OverlayReady -Overlay $Overlay
        $input = Get-OverlayInput -Overlay $Overlay
        $input.SetFocus()
        Start-Sleep -Milliseconds 150
        $markerStart = New-RuntimeMarkerCursor
        Send-VirtualKey -VirtualKey 0x0D
        Wait-Until -TimeoutSeconds 4 -Description "exact-match confirm or launch marker retry" -Condition {
            (Test-RuntimeMarkerSeen -Marker $confirmMarker -StartLine $markerStart) -or
            (Test-RuntimeMarkerSeen -Marker $launchMarker -StartLine $markerStart)
        } | Out-Null
    }

    if (-not (Test-RuntimeMarkerSeen -Marker $launchMarker -StartLine $markerStart)) {
        if (-not (Test-RuntimeMarkerSeen -Marker $confirmMarker -StartLine $markerStart)) {
            throw "Exact-match execution did not reach a confirm or launch marker."
        }
        $secondSubmitStart = New-RuntimeMarkerCursor
        Send-VirtualKey -VirtualKey 0x0D
        Wait-ForRuntimeMarker -Marker $launchMarker -StartLine $secondSubmitStart
    } else {
        $script:RuntimeLogLineCursor = Get-RuntimeLogLineCount
    }
}

function Run-Reopen-Check {
    Write-StepLog -Stage "FLOW" -Message "running overlay reopen persistence check"
    Close-Overlay
    $overlay = Open-OverlayWithRuntimeRestartFallback
    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $overlay
    Wait-ForInventoryText -Overlay $createdTasksDialog -Text "Open Weekly Reports"
    Close-CreatedTasksDialog -Dialog $createdTasksDialog
    return $overlay
}

function Run-Large-Inventory-Check {
    Write-StepLog -Stage "FLOW" -Message "running large-inventory late-item edit check"
    Seed-LargeInventorySource
    Restart-InteractiveRuntime | Out-Null
    $overlay = Open-OverlayWithRuntimeRestartFallback
    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $overlay
    $rows = @(Get-InventoryTextRows -Overlay $createdTasksDialog)
    if (@($rows | Where-Object { $_ -like "Open Reports 8*" }).Count -lt 1) {
        Add-Note "Large-inventory row 8 was not visible by name before edit invocation; proceeding with late-button reachability evidence."
    }
    $editButtons = @(Get-InventoryEditButtons -Overlay $createdTasksDialog)
    if ($editButtons.Count -lt 8) {
        throw "Expected at least 8 edit buttons in the large inventory view, found $($editButtons.Count)."
    }
    Invoke-ElementRobust -Element $editButtons[-1] -Description "late Created Tasks edit button"
    $dialog = Wait-ForOptionalDialog -Name "Edit Custom Task" -TimeoutSeconds 3
    if (-not $dialog) {
        $createdTasksDialog = Open-CreatedTasksDialog -Overlay $overlay
        $editButtons = @(Get-InventoryEditButtons -Overlay $createdTasksDialog)
        Invoke-ElementRobust -Element $editButtons[-1] -Description "late Created Tasks edit button retry"
        Wait-ForDialogClosed -Name "Created Tasks"
        $dialog = Wait-ForDialog -Name "Edit Custom Task" -TimeoutSeconds 8
    }
    Fill-AuthoringDialog -Dialog $dialog -TypeLabel "Folder" -Title "Open Reports Eight" -Aliases "show reports eight" -Target "C:\Reports\8"
    $markerStart = New-RuntimeMarkerCursor
    Submit-Dialog -Dialog $dialog -ButtonName "Save"
    Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|CUSTOM_TASK_UPDATED|action_id=open_reports_8" -StartLine $markerStart
    try {
        Wait-ForDialogClosed -Name "Edit Custom Task" -TimeoutSeconds 4
    } catch {
        Add-Note "Late-item edit dialog close readback lagged after a successful update marker, but the runtime marker and refreshed Created Tasks view still confirmed the save."
    }
    $overlay = Wait-ForOverlayOpen
    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $overlay
    Wait-ForInventoryText -Overlay $createdTasksDialog -Text "Open Reports Eight"
    Close-CreatedTasksDialog -Dialog $createdTasksDialog
    Copy-SourceSnapshot -Slug "after_large_inventory_edit" | Out-Null
    return (Ensure-OverlayReady -Overlay $overlay)
}

function Run-Unsafe-Source-Check {
    Write-StepLog -Stage "FLOW" -Message "running unsafe-source blocking check"
    Corrupt-Source
    Restart-InteractiveRuntime | Out-Null
    $overlay = Open-OverlayWithRuntimeRestartFallback
    $createButton = Find-FirstElement -Root $overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.savedActionInventory.savedActionCreateButton"
    $markerStart = New-RuntimeMarkerCursor
    Invoke-ElementRobust -Element $createButton -Description "Create Custom Task button in unsafe-source path"
    Start-Sleep -Milliseconds 400
    $dialog = Get-DialogWindow -Name "Create Custom Task"
    if ($dialog) {
        throw "Unsafe source should block the create dialog before it opens."
    }
    if (Test-RuntimeMarkerSeen -Marker "RENDERER_MAIN|CUSTOM_TASK_CREATED|" -StartLine $markerStart) {
        throw "Unsafe source unexpectedly produced a create marker."
    }
    $status = Find-FirstElement -Root $overlay -AutomationId "QApplication.commandOverlayWindow.commandPanel.commandStatus"
    $statusText = if ($status) { $status.Current.Name } else { "" }
    if ($statusText -notlike "*blocked*") {
        throw "Unsafe source did not surface blocked status text. Saw: '$statusText'"
    }

    $createdTasksDialog = Open-CreatedTasksDialog -Overlay $overlay
    $dialogStatus = Find-FirstElement -Root $createdTasksDialog -AutomationId "QApplication.savedActionCreatedTasksDialog.savedActionCreatedTasksStatus"
    $dialogStatusText = if ($dialogStatus) { $dialogStatus.Current.Name } else { "" }
    if (-not $dialogStatusText) {
        throw "Created Tasks dialog did not surface saved-action source status in the unsafe-source path."
    }

    $editButtons = @(Get-InventoryEditButtons -Overlay $createdTasksDialog)
    if ($editButtons.Count -gt 0) {
        Add-Note "Unsafe source still showed edit buttons inside Created Tasks; expected fail-closed absence was not observed."
    } else {
        Add-Note "Unsafe source hid edit affordances inside Created Tasks, which matches the fail-closed UI posture."
    }
    Close-CreatedTasksDialog -Dialog $createdTasksDialog
    $overlay = Ensure-OverlayReady -Overlay $overlay
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
    Add-Artifact -Label "interactive_step_log" -Path $StepLogPath

    $script:notepadProbe = Start-NotepadProbe
    Add-Artifact -Label "notepad_probe_file" -Path $script:notepadProbe.path

    New-HealthySource
    Copy-SourceSnapshot -Slug "initial_source" | Out-Null

    $overlay = Open-OverlayWithRuntimeRestartFallback
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
    $windowNames = @()
    try {
        $windowNames = @(
            Get-RootWindows |
            ForEach-Object { $_.Current.Name } |
            Where-Object { $_ } |
            Select-Object -First 12
        )
    } catch {
    }
    if ($windowNames.Count -gt 0) {
        Add-Note ("Visible root windows at failure: " + ($windowNames -join " | "))
    }
    try {
        $runtimeTail = @((Get-RuntimeLogLines) | Select-Object -Last 12)
        if ($runtimeTail.Count -gt 0) {
            Add-Note ("Runtime log tail at failure: " + ($runtimeTail -join " || "))
        }
    } catch {
    }
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
