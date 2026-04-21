param(
    [string]$PythonPath = $env:NEXUS_VALIDATION_PYTHON,
    [string]$ArtifactRoot = "",
    [int]$MarkerTimeoutSeconds = 12
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir

function Resolve-ValidationPython {
    $candidates = @()

    if ($PythonPath) {
        $candidates += $PythonPath
    }

    $candidates += "C:\Users\anden\AppData\Local\Python\pythoncore-3.14-64\python.exe"

    $pathPython = Get-Command python -ErrorAction SilentlyContinue
    if ($pathPython -and $pathPython.Source) {
        $candidates += $pathPython.Source
    }

    foreach ($candidate in $candidates) {
        if (-not $candidate) {
            continue
        }

        if (-not (Test-Path -LiteralPath $candidate)) {
            continue
        }

        try {
            & $candidate -c "import PySide6" | Out-Null
            if ($LASTEXITCODE -eq 0) {
                return (Resolve-Path -LiteralPath $candidate).Path
            }
        }
        catch {
            continue
        }
    }

    throw "No Qt-capable Python interpreter found. Set NEXUS_VALIDATION_PYTHON to a python.exe with PySide6 installed."
}

function Initialize-NativeInput {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    if (-not ("NativeInputFb038Seam2LiveValidation" -as [type])) {
        Add-Type @'
using System;
using System.Runtime.InteropServices;

public static class NativeInputFb038Seam2LiveValidation {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
'@
    }
}

function New-RunPaths {
    if (-not $ArtifactRoot) {
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $ArtifactRoot = Join-Path $rootDir "dev\logs\fb_038_tray_create_live_validation\$stamp"
    }

    New-Item -ItemType Directory -Force -Path $ArtifactRoot | Out-Null

    return [pscustomobject]@{
        Root = $ArtifactRoot
        RuntimeLog = Join-Path $ArtifactRoot "runtime_log.txt"
        StdoutLog = Join-Path $ArtifactRoot "stdout.txt"
        StderrLog = Join-Path $ArtifactRoot "stderr.txt"
        StepLog = Join-Path $ArtifactRoot "step_log.txt"
        Summary = Join-Path $ArtifactRoot "summary.txt"
        SavedBefore = Join-Path $ArtifactRoot "saved_actions_before.json"
        SavedAfter = Join-Path $ArtifactRoot "saved_actions_after.json"
        StartupScreenshot = Join-Path $ArtifactRoot "01_startup_ready.png"
        DialogScreenshot = Join-Path $ArtifactRoot "02_create_custom_task_dialog.png"
        AfterCancelScreenshot = Join-Path $ArtifactRoot "03_after_cancel.png"
        HotkeyScreenshot = Join-Path $ArtifactRoot "04_hotkey_overlay.png"
    }
}

function Write-Step {
    param(
        [object]$Paths,
        [string]$Message
    )

    $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -LiteralPath $Paths.StepLog -Value $line
    Write-Output $line
}

function Write-Summary {
    param(
        [object]$Paths,
        [string]$Result,
        [string]$Failure = "",
        [object]$Before = $null,
        [object]$After = $null
    )

    $lines = @(
        "RESULT: $Result",
        "ARTIFACT_ROOT: $($Paths.Root)",
        "RUNTIME_LOG: $($Paths.RuntimeLog)",
        "STDOUT: $($Paths.StdoutLog)",
        "STDERR: $($Paths.StderrLog)",
        "STEP_LOG: $($Paths.StepLog)",
        "SAVED_ACTIONS_BEFORE: $($Paths.SavedBefore)",
        "SAVED_ACTIONS_AFTER: $($Paths.SavedAfter)"
    )

    if ($Failure) {
        $lines += "FAILURE: $Failure"
    }

    if ($Before -and $After) {
        $lines += @(
            "SAVED_ACTIONS_HASH_BEFORE: $($Before.Hash)",
            "SAVED_ACTIONS_HASH_AFTER: $($After.Hash)",
            "SAVED_ACTIONS_LASTWRITE_BEFORE: $($Before.LastWriteUtc)",
            "SAVED_ACTIONS_LASTWRITE_AFTER: $($After.LastWriteUtc)",
            "SAVED_ACTIONS_LENGTH_BEFORE: $($Before.Length)",
            "SAVED_ACTIONS_LENGTH_AFTER: $($After.Length)"
        )
    }

    if ($Result -eq "PASS") {
        $lines += @(
            "REQUIRED_MARKERS: observed",
            "ABSENT_CREATE_MARKERS: confirmed",
            "PERSISTED_STATE_UNCHANGED: confirmed",
            "TRAY_OPEN_COMMAND_OVERLAY_BASELINE: PASS",
            "HOTKEY_OVERLAY_BASELINE: PASS"
        )
    }

    Set-Content -LiteralPath $Paths.Summary -Value ($lines -join "`r`n")
}

function Fail-Validation {
    param(
        [object]$Paths,
        [string]$Message,
        [object]$Before = $null,
        [object]$After = $null
    )

    Write-Step $Paths "FAIL: $Message"
    Write-Summary -Paths $Paths -Result "FAIL" -Failure $Message -Before $Before -After $After
    throw $Message
}

function Get-FileSnapshot {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return [pscustomobject]@{
            Exists = $false
            Hash = ""
            LastWriteUtc = ""
            Length = 0
        }
    }

    $item = Get-Item -LiteralPath $Path
    return [pscustomobject]@{
        Exists = $true
        Hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
        LastWriteUtc = $item.LastWriteTimeUtc.ToString("o")
        Length = $item.Length
    }
}

function Save-Snapshot {
    param(
        [object]$Snapshot,
        [string]$Path
    )

    $Snapshot | ConvertTo-Json | Set-Content -LiteralPath $Path
}

function Get-MarkerCount {
    param(
        [object]$Paths,
        [string]$Pattern
    )

    if (-not (Test-Path -LiteralPath $Paths.RuntimeLog)) {
        return 0
    }

    return @(Select-String -LiteralPath $Paths.RuntimeLog -Pattern $Pattern).Count
}

function Wait-ForMarkerCount {
    param(
        [object]$Paths,
        [string]$Pattern,
        [int]$MinimumCount,
        [int]$TimeoutSeconds = $MarkerTimeoutSeconds
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $count = Get-MarkerCount -Paths $Paths -Pattern $Pattern
        if ($count -ge $MinimumCount) {
            Write-Step $Paths "observed marker: $Pattern count=$count"
            return $true
        }

        if ($script:RuntimeProcess -and $script:RuntimeProcess.HasExited) {
            Write-Step $Paths "runtime exited with code $($script:RuntimeProcess.ExitCode) while waiting for $Pattern"
            return $false
        }

        Start-Sleep -Milliseconds 250
    }

    return $false
}

function Wait-ForMarker {
    param(
        [object]$Paths,
        [string]$Pattern,
        [int]$TimeoutSeconds = $MarkerTimeoutSeconds
    )

    return Wait-ForMarkerCount -Paths $Paths -Pattern $Pattern -MinimumCount 1 -TimeoutSeconds $TimeoutSeconds
}

function Send-Key {
    param([byte]$VirtualKey)

    [NativeInputFb038Seam2LiveValidation]::keybd_event($VirtualKey, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 90
    [NativeInputFb038Seam2LiveValidation]::keybd_event($VirtualKey, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 250
}

function Send-WinB {
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x5B, 0, 0, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x42, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 100
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x42, 0, 2, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x5B, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
}

function Send-ShiftF10 {
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x10, 0, 0, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x79, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 90
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x79, 0, 2, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x10, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
}

function Send-CtrlAltHome {
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x24, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 120
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x24, 0, 2, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
    [NativeInputFb038Seam2LiveValidation]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
}

function Get-FocusedName {
    try {
        return [System.Windows.Automation.AutomationElement]::FocusedElement.Current.Name
    }
    catch {
        return ""
    }
}

function Find-VisibleElementByName {
    param(
        [string]$Name,
        [string]$ControlTypeName = "",
        [int]$TimeoutSeconds = 8
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::NameProperty,
        $Name
    )

    while ((Get-Date) -lt $deadline) {
        try {
            $matches = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
                [System.Windows.Automation.TreeScope]::Descendants,
                $condition
            )

            for ($i = 0; $i -lt $matches.Count; $i++) {
                $element = $matches.Item($i)
                $rect = $element.Current.BoundingRectangle
                $typeName = $element.Current.ControlType.ProgrammaticName
                if (-not $rect.IsEmpty -and -not $element.Current.IsOffscreen -and ($ControlTypeName -eq "" -or $typeName -eq $ControlTypeName)) {
                    return $element
                }
            }
        }
        catch {
            # Retry until timeout; UIAutomation can throw during menu transitions.
        }

        Start-Sleep -Milliseconds 250
    }

    return $null
}

function Click-ElementCenter {
    param(
        [object]$Paths,
        [object]$Element
    )

    $rect = $Element.Current.BoundingRectangle
    if ($rect.IsEmpty) {
        throw "Cannot click element with empty bounding rectangle: $($Element.Current.Name)"
    }

    $x = [int]($rect.X + ($rect.Width / 2))
    $y = [int]($rect.Y + ($rect.Height / 2))
    Write-Step $Paths "click element '$($Element.Current.Name)' at $x,$y"

    [NativeInputFb038Seam2LiveValidation]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 120
    [NativeInputFb038Seam2LiveValidation]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 100
    [NativeInputFb038Seam2LiveValidation]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 500
}

function Invoke-ElementIfSupported {
    param([object]$Element)

    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        if ($pattern) {
            $pattern.Invoke()
            Start-Sleep -Milliseconds 500
            return $true
        }
    }
    catch {
        return $false
    }

    return $false
}

function Open-HiddenTrayOnNexus {
    param([object]$Paths)

    Send-WinB
    Send-Key 0x0D
    Start-Sleep -Milliseconds 300

    Write-Step $Paths "hidden tray focus after Enter: '$(Get-FocusedName)'"

    if ((Get-FocusedName) -ne "Nexus Desktop AI") {
        for ($i = 0; $i -lt 18 -and (Get-FocusedName) -ne "Nexus Desktop AI"; $i++) {
            Send-Key 0x27
        }
        for ($i = 0; $i -lt 18 -and (Get-FocusedName) -ne "Nexus Desktop AI"; $i++) {
            Send-Key 0x28
        }
    }

    if ((Get-FocusedName) -ne "Nexus Desktop AI") {
        Fail-Validation -Paths $Paths -Message "Nexus tray icon focus not found; current focus='$(Get-FocusedName)'"
    }

    Write-Step $Paths "Nexus tray icon focused in hidden tray overflow"
}

function Invoke-TrayMenuActionAndWait {
    param(
        [object]$Paths,
        [string]$ActionName,
        [string]$ExpectedMarkerPattern,
        [int]$ExpectedMarkerCount
    )

    for ($attempt = 1; $attempt -le 2; $attempt++) {
        Open-HiddenTrayOnNexus -Paths $Paths
        Send-ShiftF10

        $menuItem = Find-VisibleElementByName -Name $ActionName -ControlTypeName "ControlType.MenuItem" -TimeoutSeconds 8
        if (-not $menuItem) {
            Fail-Validation -Paths $Paths -Message "Visible tray menu action '$ActionName' not found"
        }

        $rect = $menuItem.Current.BoundingRectangle
        Write-Step $Paths "visible tray menu action '$ActionName' at $($rect.X),$($rect.Y),$($rect.Width),$($rect.Height)"

        if ($attempt -eq 1) {
            if (Invoke-ElementIfSupported -Element $menuItem) {
                Write-Step $Paths "invoked tray menu action '$ActionName' through UIAutomation InvokePattern"
            }
            else {
                Click-ElementCenter -Paths $Paths -Element $menuItem
            }
        }
        else {
            Click-ElementCenter -Paths $Paths -Element $menuItem
        }

        if (Wait-ForMarkerCount -Paths $Paths -Pattern $ExpectedMarkerPattern -MinimumCount $ExpectedMarkerCount -TimeoutSeconds 5) {
            return
        }

        Send-Key 0x1B
        Write-Step $Paths "retrying tray menu action '$ActionName' after attempt $attempt did not emit expected marker"
    }

    Fail-Validation -Paths $Paths -Message "Tray menu action '$ActionName' did not emit expected marker: $ExpectedMarkerPattern"
}

function Capture-Screenshot {
    param(
        [object]$Paths,
        [string]$Path
    )

    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    Write-Step $Paths "screenshot captured: $Path"
}

function Cancel-CreateCustomTaskDialog {
    param([object]$Paths)

    $cancel = Find-VisibleElementByName -Name "Cancel" -ControlTypeName "ControlType.Button" -TimeoutSeconds 8
    if (-not $cancel) {
        Fail-Validation -Paths $Paths -Message "Create Custom Task Cancel button not found"
    }

    Write-Step $Paths "found visible Create Custom Task Cancel button"
    Click-ElementCenter -Paths $Paths -Element $cancel
}

function Stop-Runtime {
    param([object]$Paths)

    if ($script:RuntimeProcess -and -not $script:RuntimeProcess.HasExited) {
        $script:RuntimeProcess.CloseMainWindow() | Out-Null
        if (-not $script:RuntimeProcess.WaitForExit(7000)) {
            Stop-Process -Id $script:RuntimeProcess.Id -Force
            Write-Step $Paths "runtime process force-stopped after graceful close timeout"
        }
    }
}

$paths = New-RunPaths
$python = Resolve-ValidationPython
$savedActionsPath = Join-Path $env:LOCALAPPDATA "Nexus Desktop AI\saved_actions.json"
$script:RuntimeProcess = $null
$beforeSnapshot = $null
$afterSnapshot = $null

Push-Location $rootDir
try {
    Initialize-NativeInput
    Remove-Item Env:QT_QPA_PLATFORM -ErrorAction SilentlyContinue

    Write-Step $paths "FB038_SEAM2_LIVE_VALIDATION|START"
    Write-Step $paths "python=$python"

    $argString = '-u "desktop\orin_desktop_main.py" --runtime-log "' + $paths.RuntimeLog + '"'
    $script:RuntimeProcess = Start-Process `
        -FilePath $python `
        -ArgumentList $argString `
        -WorkingDirectory $rootDir `
        -RedirectStandardOutput $paths.StdoutLog `
        -RedirectStandardError $paths.StderrLog `
        -PassThru

    if (-not (Wait-ForMarker -Paths $paths -Pattern "RENDERER_MAIN\|STARTUP_READY" -TimeoutSeconds 35)) {
        Fail-Validation -Paths $paths -Message "startup ready marker missing"
    }
    if (-not (Wait-ForMarker -Paths $paths -Pattern "RENDERER_MAIN\|TRAY_ICON_SHOWN" -TimeoutSeconds 20)) {
        Fail-Validation -Paths $paths -Message "tray icon shown marker missing"
    }

    Capture-Screenshot -Paths $paths -Path $paths.StartupScreenshot

    $beforeSnapshot = Get-FileSnapshot -Path $savedActionsPath
    Save-Snapshot -Snapshot $beforeSnapshot -Path $paths.SavedBefore
    Write-Step $paths "snapshot before saved_actions hash=$($beforeSnapshot.Hash) write=$($beforeSnapshot.LastWriteUtc) length=$($beforeSnapshot.Length)"

    $createMarkerCount = (Get-MarkerCount -Paths $paths -Pattern "RENDERER_MAIN\|TRAY_CREATE_CUSTOM_TASK_REQUESTED") + 1
    Invoke-TrayMenuActionAndWait `
        -Paths $paths `
        -ActionName "Create Custom Task" `
        -ExpectedMarkerPattern "RENDERER_MAIN\|TRAY_CREATE_CUSTOM_TASK_REQUESTED" `
        -ExpectedMarkerCount $createMarkerCount

    foreach ($pattern in @(
        "RENDERER_MAIN\|COMMAND_OVERLAY_OPENED",
        "RENDERER_MAIN\|TRAY_CREATE_CUSTOM_TASK_ROUTED_TO_OVERLAY_ENTRY",
        "RENDERER_MAIN\|OVERLAY_ENTRY_ACTION_TRIGGERED\|action=create_custom_task",
        "RENDERER_MAIN\|OVERLAY_ENTRY_DIALOG_CREATED\|action=create_custom_task"
    )) {
        if (-not (Wait-ForMarker -Paths $paths -Pattern $pattern -TimeoutSeconds $MarkerTimeoutSeconds)) {
            Fail-Validation -Paths $paths -Message "required marker missing: $pattern" -Before $beforeSnapshot
        }
    }

    $dialog = Find-VisibleElementByName -Name "Create Custom Task" -TimeoutSeconds 10
    if (-not $dialog) {
        Fail-Validation -Paths $paths -Message "Create Custom Task dialog not found by UIAutomation" -Before $beforeSnapshot
    }

    Write-Step $paths "Create Custom Task dialog found by UIAutomation"
    Capture-Screenshot -Paths $paths -Path $paths.DialogScreenshot

    Cancel-CreateCustomTaskDialog -Paths $paths
    if (-not (Wait-ForMarker -Paths $paths -Pattern "RENDERER_MAIN\|OVERLAY_ENTRY_DIALOG_EXEC_RETURNED\|action=create_custom_task" -TimeoutSeconds $MarkerTimeoutSeconds)) {
        Fail-Validation -Paths $paths -Message "dialog exec return marker missing after Cancel button invocation" -Before $beforeSnapshot
    }

    Write-Step $paths "dialog canceled via Cancel button without submit"
    Capture-Screenshot -Paths $paths -Path $paths.AfterCancelScreenshot

    $afterSnapshot = Get-FileSnapshot -Path $savedActionsPath
    Save-Snapshot -Snapshot $afterSnapshot -Path $paths.SavedAfter
    Write-Step $paths "snapshot after saved_actions hash=$($afterSnapshot.Hash) write=$($afterSnapshot.LastWriteUtc) length=$($afterSnapshot.Length)"

    if ($beforeSnapshot.Exists -ne $afterSnapshot.Exists -or
        $beforeSnapshot.Hash -ne $afterSnapshot.Hash -or
        $beforeSnapshot.LastWriteUtc -ne $afterSnapshot.LastWriteUtc -or
        $beforeSnapshot.Length -ne $afterSnapshot.Length) {
        Fail-Validation -Paths $paths -Message "saved_actions.json changed after open/cancel" -Before $beforeSnapshot -After $afterSnapshot
    }

    if (Select-String -LiteralPath $paths.RuntimeLog -Pattern "RENDERER_MAIN\|CUSTOM_TASK_CREATE_ATTEMPT_STARTED|RENDERER_MAIN\|CUSTOM_TASK_CREATED" -Quiet) {
        Fail-Validation -Paths $paths -Message "create attempt or created marker appeared during open/cancel validation" -Before $beforeSnapshot -After $afterSnapshot
    }

    Write-Step $paths "confirmed absence of CUSTOM_TASK_CREATE_ATTEMPT_STARTED and CUSTOM_TASK_CREATED"

    Send-Key 0x1B
    Wait-ForMarker -Paths $paths -Pattern "RENDERER_MAIN\|COMMAND_OVERLAY_CLOSED" -TimeoutSeconds 5 | Out-Null

    $trayOpenMarkerCount = (Get-MarkerCount -Paths $paths -Pattern "RENDERER_MAIN\|TRAY_ACTIVATION_REQUESTED") + 1
    $overlayOpenMarkerCount = (Get-MarkerCount -Paths $paths -Pattern "RENDERER_MAIN\|COMMAND_OVERLAY_OPENED") + 1
    Invoke-TrayMenuActionAndWait `
        -Paths $paths `
        -ActionName "Open Command Overlay" `
        -ExpectedMarkerPattern "RENDERER_MAIN\|TRAY_ACTIVATION_REQUESTED" `
        -ExpectedMarkerCount $trayOpenMarkerCount

    if (-not (Wait-ForMarkerCount -Paths $paths -Pattern "RENDERER_MAIN\|COMMAND_OVERLAY_OPENED" -MinimumCount $overlayOpenMarkerCount -TimeoutSeconds $MarkerTimeoutSeconds)) {
        Fail-Validation -Paths $paths -Message "Open Command Overlay did not reach a new overlay-open marker" -Before $beforeSnapshot -After $afterSnapshot
    }
    Write-Step $paths "tray Open Command Overlay baseline path passed"

    Send-Key 0x1B
    Wait-ForMarker -Paths $paths -Pattern "RENDERER_MAIN\|COMMAND_OVERLAY_CLOSED" -TimeoutSeconds 5 | Out-Null

    $hotkeyOverlayOpenCount = (Get-MarkerCount -Paths $paths -Pattern "RENDERER_MAIN\|COMMAND_OVERLAY_OPENED") + 1
    Send-CtrlAltHome

    if (-not (Wait-ForMarkerCount -Paths $paths -Pattern "RENDERER_MAIN\|COMMAND_OVERLAY_OPENED" -MinimumCount $hotkeyOverlayOpenCount -TimeoutSeconds $MarkerTimeoutSeconds)) {
        Fail-Validation -Paths $paths -Message "hotkey overlay did not reach a new overlay-open marker" -Before $beforeSnapshot -After $afterSnapshot
    }

    Write-Step $paths "hotkey overlay baseline path passed"
    Capture-Screenshot -Paths $paths -Path $paths.HotkeyScreenshot

    Stop-Runtime -Paths $paths
    Wait-ForMarker -Paths $paths -Pattern "RENDERER_MAIN\|TRAY_ICON_HIDDEN" -TimeoutSeconds 8 | Out-Null

    $leftovers = @(Get-Process | Where-Object { $_.ProcessName -match "^(Nexus|orin|jarvis)$" })
    if ($leftovers.Count -gt 0) {
        Fail-Validation -Paths $paths -Message ("leftover runtime process count=" + $leftovers.Count) -Before $beforeSnapshot -After $afterSnapshot
    }

    Write-Summary -Paths $paths -Result "PASS" -Before $beforeSnapshot -After $afterSnapshot
    Write-Step $paths "FB038_SEAM2_LIVE_VALIDATION|PASS|summary=$($paths.Summary)"
    Write-Output "FB038_SEAM2_LIVE_VALIDATION|PASS|summary=$($paths.Summary)"
}
catch {
    Stop-Runtime -Paths $paths
    if (-not (Test-Path -LiteralPath $paths.Summary)) {
        Write-Summary -Paths $paths -Result "FAIL" -Failure $_.Exception.Message -Before $beforeSnapshot -After $afterSnapshot
    }
    Write-Error $_
    exit 1
}
finally {
    Pop-Location
}
