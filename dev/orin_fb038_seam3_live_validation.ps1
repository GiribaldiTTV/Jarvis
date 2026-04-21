param(
    [string]$PythonPath = $env:NEXUS_VALIDATION_PYTHON,
    [string]$ArtifactRoot = "",
    [int]$MarkerTimeoutSeconds = 12,
    [int]$NoProgressTimeoutSeconds = 10
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$script:RuntimeProcess = $null
$script:LastProgressAt = Get-Date
$script:LastProgress = "start"

function Step([object]$Paths, [string]$Message) {
    $script:LastProgressAt = Get-Date
    $script:LastProgress = $Message
    $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -LiteralPath $Paths.StepLog -Value $line
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

function Init-UiAutomation {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    if (-not ("NativeInputFb038Seam3" -as [type])) {
        Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class NativeInputFb038Seam3 {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
'@
    }
}

function New-Paths {
    if (-not $ArtifactRoot) {
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $ArtifactRoot = Join-Path $rootDir "dev\logs\fb_038_tray_create_completion_live_validation\$stamp"
    }
    New-Item -ItemType Directory -Force -Path $ArtifactRoot | Out-Null
    [pscustomobject]@{
        Root = $ArtifactRoot
        RuntimeLog = Join-Path $ArtifactRoot "runtime_log.txt"
        StdoutLog = Join-Path $ArtifactRoot "stdout.txt"
        StderrLog = Join-Path $ArtifactRoot "stderr.txt"
        StepLog = Join-Path $ArtifactRoot "step_log.txt"
        Summary = Join-Path $ArtifactRoot "summary.txt"
        Before = Join-Path $ArtifactRoot "saved_actions_before.json"
        Backup = Join-Path $ArtifactRoot "saved_actions_original_backup.json"
        AfterCreate = Join-Path $ArtifactRoot "saved_actions_after_create.json"
        Restored = Join-Path $ArtifactRoot "saved_actions_restored.json"
        CreatedRecord = Join-Path $ArtifactRoot "created_record.json"
        StartupPng = Join-Path $ArtifactRoot "01_startup_ready.png"
        DialogPng = Join-Path $ArtifactRoot "02_create_custom_task_dialog.png"
        ConfirmPng = Join-Path $ArtifactRoot "03_created_task_confirm.png"
        ResultPng = Join-Path $ArtifactRoot "04_created_task_result.png"
    }
}

function Snapshot([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return [pscustomobject]@{ Exists = $false; Hash = ""; LastWriteUtc = ""; Length = 0 }
    }
    $item = Get-Item -LiteralPath $Path
    [pscustomobject]@{
        Exists = $true
        Hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
        LastWriteUtc = $item.LastWriteTimeUtc.ToString("o")
        Length = $item.Length
    }
}

function Save-Json($Value, [string]$Path) {
    $Value | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Path -Encoding utf8
}

function Marker-Count([object]$Paths, [string]$Pattern) {
    if (-not (Test-Path -LiteralPath $Paths.RuntimeLog)) { return 0 }
    @(Select-String -LiteralPath $Paths.RuntimeLog -Pattern $Pattern).Count
}

function Wait-Marker([object]$Paths, [string]$Pattern, [int]$Count = 1, [int]$Timeout = $MarkerTimeoutSeconds) {
    $deadline = (Get-Date).AddSeconds($Timeout)
    $heartbeat = Get-Date
    while ((Get-Date) -lt $deadline) {
        $current = Marker-Count $Paths $Pattern
        if ($current -ge $Count) {
            Step $Paths "observed marker: $Pattern count=$current"
            return $true
        }
        if ($script:RuntimeProcess -and $script:RuntimeProcess.HasExited) {
            Step $Paths "runtime exited while waiting for $Pattern"
            return $false
        }
        if ((Get-Date) -gt $heartbeat.AddSeconds(2)) {
            $heartbeat = Get-Date
            Step $Paths "waiting for marker: $Pattern current_count=$current"
        }
        Check-Progress "marker wait $Pattern"
        Start-Sleep -Milliseconds 250
    }
    return $false
}

function Send-Key([byte]$Vk) {
    [NativeInputFb038Seam3]::keybd_event($Vk, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [NativeInputFb038Seam3]::keybd_event($Vk, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 220
}

function Send-WinB {
    [NativeInputFb038Seam3]::keybd_event(0x5B, 0, 0, [UIntPtr]::Zero)
    [NativeInputFb038Seam3]::keybd_event(0x42, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 100
    [NativeInputFb038Seam3]::keybd_event(0x42, 0, 2, [UIntPtr]::Zero)
    [NativeInputFb038Seam3]::keybd_event(0x5B, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function Send-ShiftF10 {
    [NativeInputFb038Seam3]::keybd_event(0x10, 0, 0, [UIntPtr]::Zero)
    [NativeInputFb038Seam3]::keybd_event(0x79, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [NativeInputFb038Seam3]::keybd_event(0x79, 0, 2, [UIntPtr]::Zero)
    [NativeInputFb038Seam3]::keybd_event(0x10, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function Focused-Name {
    try { return [System.Windows.Automation.AutomationElement]::FocusedElement.Current.Name } catch { return "" }
}

function Find-VisibleByName([string]$Name, [string]$ControlTypeName = "", [int]$Timeout = 8) {
    $deadline = (Get-Date).AddSeconds($Timeout)
    $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $Name)
    while ((Get-Date) -lt $deadline) {
        $matches = [System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Descendants, $condition)
        for ($i = 0; $i -lt $matches.Count; $i++) {
            $element = $matches.Item($i)
            try {
                $rect = $element.Current.BoundingRectangle
                $type = $element.Current.ControlType.ProgrammaticName
                if (-not $rect.IsEmpty -and -not $element.Current.IsOffscreen -and ($ControlTypeName -eq "" -or $type -eq $ControlTypeName)) { return $element }
            } catch {}
        }
        Start-Sleep -Milliseconds 250
    }
    return $null
}

function Find-ByAutomationSuffix($Root, [string]$Suffix, [string]$ControlTypeName = "") {
    $matches = $Root.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
    for ($i = 0; $i -lt $matches.Count; $i++) {
        $element = $matches.Item($i)
        try {
            $id = [string]$element.Current.AutomationId
            $type = $element.Current.ControlType.ProgrammaticName
            $rect = $element.Current.BoundingRectangle
            if (($id -eq $Suffix -or $id.EndsWith("." + $Suffix)) -and -not $rect.IsEmpty -and -not $element.Current.IsOffscreen -and ($ControlTypeName -eq "" -or $type -eq $ControlTypeName)) { return $element }
        } catch {}
    }
    return $null
}

function Click-Element([object]$Paths, $Element, [string]$Label) {
    $rect = $Element.Current.BoundingRectangle
    $x = [int]($rect.X + ($rect.Width / 2))
    $y = [int]($rect.Y + ($rect.Height / 2))
    Step $Paths "click $Label at $x,$y"
    [NativeInputFb038Seam3]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 100
    [NativeInputFb038Seam3]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [NativeInputFb038Seam3]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 420
}

function Invoke-Element($Element) {
    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $pattern.Invoke()
        Start-Sleep -Milliseconds 500
        return $true
    } catch {
        return $false
    }
}

function Set-Value([object]$Paths, $Element, [string]$Value, [string]$Label) {
    if (-not $Element) { throw "Missing element for $Label" }
    try { $Element.SetFocus() } catch {}
    $pattern = $Element.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    $pattern.SetValue($Value)
    Step $Paths "set $Label to '$Value'"
    Start-Sleep -Milliseconds 250
}

function Open-TrayMenuAction([object]$Paths, [string]$ActionName, [string]$MarkerPattern) {
    $needed = (Marker-Count $Paths $MarkerPattern) + 1
    for ($attempt = 1; $attempt -le 2; $attempt++) {
        Send-WinB
        Send-Key 0x0D
        Step $Paths "hidden tray focus after Enter: '$(Focused-Name)'"
        for ($i = 0; $i -lt 18 -and (Focused-Name) -ne "Nexus Desktop AI"; $i++) { Send-Key 0x27 }
        for ($i = 0; $i -lt 18 -and (Focused-Name) -ne "Nexus Desktop AI"; $i++) { Send-Key 0x28 }
        if ((Focused-Name) -ne "Nexus Desktop AI") { throw "Nexus tray icon focus not found." }
        Send-ShiftF10
        $item = Find-VisibleByName $ActionName "ControlType.MenuItem" 8
        if (-not $item) { throw "Visible tray menu action '$ActionName' not found." }
        if (Invoke-Element $item) { Step $Paths "invoked tray menu action '$ActionName'" } else { Click-Element $Paths $item $ActionName }
        if (Wait-Marker $Paths $MarkerPattern $needed 5) { return }
        Send-Key 0x1B
        Step $Paths "retrying tray action '$ActionName'"
    }
    throw "Tray action '$ActionName' did not emit $MarkerPattern"
}

function Capture-Screen([object]$Paths, [string]$Path) {
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    Step $Paths "screenshot captured: $Path"
}

function Dialog-Input($Dialog, [string]$LeafId) {
    $found = Find-ByAutomationSuffix $Dialog $LeafId "ControlType.Edit"
    if ($found) { return $found }
    $found = Find-ByAutomationSuffix ([System.Windows.Automation.AutomationElement]::RootElement) $LeafId "ControlType.Edit"
    if ($found) { return $found }
    $edits = @()
    $all = $Dialog.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
    for ($i = 0; $i -lt $all.Count; $i++) {
        $e = $all.Item($i)
        try {
            if ($e.Current.ControlType.ProgrammaticName -ne "ControlType.Edit" -or $e.Current.IsOffscreen) { continue }
            $r = $e.Current.BoundingRectangle
            if ($r.IsEmpty) { continue }
            $edits += [pscustomobject]@{ Element = $e; Top = [double]$r.Top; Left = [double]$r.Left }
        } catch {}
    }
    $ordered = @($edits | Sort-Object -Property @{ Expression = "Top"; Ascending = $true }, @{ Expression = "Left"; Ascending = $true })
    $idx = switch ($LeafId) { "savedActionCreateTitleInput" { 0 } "savedActionCreateAliasesInput" { 1 } "savedActionCreateTargetInput" { 2 } default { -1 } }
    if ($idx -ge 0 -and $ordered.Count -gt $idx) { return $ordered[$idx].Element }
    return $null
}

function Saved-Records([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    $payload = Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json
    if ($payload -is [array]) { return @($payload) }
    if ($payload.actions) { return @($payload.actions) }
    return @()
}

function Created-Record([string]$Path, [string]$Title) {
    foreach ($record in (Saved-Records $Path)) {
        if ([string]$record.title -eq $Title) { return $record }
    }
    return $null
}

function Stop-Runtime([object]$Paths) {
    if ($script:RuntimeProcess -and -not $script:RuntimeProcess.HasExited) {
        $script:RuntimeProcess.CloseMainWindow() | Out-Null
        if (-not $script:RuntimeProcess.WaitForExit(7000)) {
            Stop-Process -Id $script:RuntimeProcess.Id -Force
            Step $Paths "runtime force-stopped"
        }
    }
}

function Cleanup-Notepad([object]$Paths, [int[]]$BaselineIds) {
    $closed = 0
    $processes = @(Get-Process -Name notepad -ErrorAction SilentlyContinue | Where-Object { $BaselineIds -notcontains [int]$_.Id })
    foreach ($process in $processes) {
        try {
            if ($process.MainWindowHandle -ne 0) {
                $process.CloseMainWindow() | Out-Null
                if ($process.WaitForExit(3000)) { $closed++; continue }
            }
            Stop-Process -Id $process.Id -Force -ErrorAction Stop
            $closed++
        } catch {
            Step $Paths "notepad cleanup warning pid=$($process.Id): $($_.Exception.Message)"
        }
    }
    Step $Paths "notepad cleanup complete closed=$closed" | Out-Null
    return "closed=$closed"
}

function Restore-Saved([object]$Paths, [string]$SourcePath, [bool]$HadOriginal) {
    if ($HadOriginal) { Copy-Item -LiteralPath $Paths.Backup -Destination $SourcePath -Force }
    elseif (Test-Path -LiteralPath $SourcePath) { Remove-Item -LiteralPath $SourcePath -Force }
    $snap = Snapshot $SourcePath
    Save-Json $snap $Paths.Restored
    Step $Paths "saved_actions restored hash=$($snap.Hash) length=$($snap.Length)" | Out-Null
    return $snap
}

$paths = New-Paths
$python = Resolve-ValidationPython
$savedActionsPath = Join-Path $env:LOCALAPPDATA "Nexus Desktop AI\saved_actions.json"
$hadOriginal = Test-Path -LiteralPath $savedActionsPath
$before = $null
$afterCreate = $null
$restored = $null
$cleanup = ""
$baselineNotepadIds = @()
$stamp = Get-Date -Format "yyyyMMddHHmmss"
$title = "FB038 Seam3 Live Notepad $stamp"
$alias = "fb038 seam3 live $stamp"
$phrase = "launch $alias"
$actionId = ""

Push-Location $rootDir
try {
    Init-UiAutomation
    Remove-Item Env:QT_QPA_PLATFORM -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $savedActionsPath) | Out-Null
    if ($hadOriginal) { Copy-Item -LiteralPath $savedActionsPath -Destination $paths.Backup -Force } else { Set-Content -LiteralPath $paths.Backup -Value "" }
    $before = Snapshot $savedActionsPath
    Save-Json $before $paths.Before
    Step $paths "FB038_SEAM3_LIVE_VALIDATION|START"
    Step $paths "python=$python"
    Step $paths "title=$title alias=$alias phrase=$phrase"
    $baselineNotepadIds = @(Get-Process -Name notepad -ErrorAction SilentlyContinue | ForEach-Object { [int]$_.Id })

    $argString = '-u "desktop\orin_desktop_main.py" --runtime-log "' + $paths.RuntimeLog + '"'
    $script:RuntimeProcess = Start-Process -FilePath $python -ArgumentList $argString -WorkingDirectory $rootDir -RedirectStandardOutput $paths.StdoutLog -RedirectStandardError $paths.StderrLog -PassThru
    if (-not (Wait-Marker $paths "RENDERER_MAIN\|STARTUP_READY" 1 35)) { throw "startup ready marker missing" }
    if (-not (Wait-Marker $paths "RENDERER_MAIN\|TRAY_ICON_SHOWN" 1 20)) { throw "tray icon shown marker missing" }
    Capture-Screen $paths $paths.StartupPng

    Open-TrayMenuAction $paths "Create Custom Task" "RENDERER_MAIN\|TRAY_CREATE_CUSTOM_TASK_REQUESTED"
    foreach ($pattern in @(
        "RENDERER_MAIN\|COMMAND_OVERLAY_OPENED",
        "RENDERER_MAIN\|TRAY_CREATE_CUSTOM_TASK_ROUTED_TO_OVERLAY_ENTRY",
        "RENDERER_MAIN\|OVERLAY_ENTRY_ACTION_TRIGGERED\|action=create_custom_task",
        "RENDERER_MAIN\|OVERLAY_ENTRY_DIALOG_CREATED\|action=create_custom_task"
    )) {
        if (-not (Wait-Marker $paths $pattern 1 $MarkerTimeoutSeconds)) { throw "route marker missing: $pattern" }
    }

    $dialog = Find-VisibleByName "Create Custom Task" "" 10
    if (-not $dialog) { throw "Create Custom Task dialog not found" }
    Step $paths "Create Custom Task dialog found"
    Capture-Screen $paths $paths.DialogPng

    Set-Value $paths (Dialog-Input $dialog "savedActionCreateTitleInput") $title "title"
    Set-Value $paths (Dialog-Input $dialog "savedActionCreateAliasesInput") $alias "alias"
    Set-Value $paths (Dialog-Input $dialog "savedActionCreateTargetInput") "notepad.exe" "target"
    $submit = Find-VisibleByName "Create" "ControlType.Button" 4
    if (-not $submit) { throw "Create submit button not found" }
    if (Invoke-Element $submit) { Step $paths "Create submit invoked" } else { Click-Element $paths $submit "Create submit" }

    foreach ($pattern in @(
        "RENDERER_MAIN\|CUSTOM_TASK_CREATE_ATTEMPT_STARTED",
        "RENDERER_MAIN\|COMMAND_ACTION_CATALOG_RELOAD_COMPLETED",
        "RENDERER_MAIN\|CUSTOM_TASK_CREATED"
    )) {
        if (-not (Wait-Marker $paths $pattern 1 $MarkerTimeoutSeconds)) { throw "create marker missing: $pattern" }
    }

    $afterCreate = Snapshot $savedActionsPath
    Save-Json $afterCreate $paths.AfterCreate
    if (-not $afterCreate.Exists -or ($afterCreate.Hash -eq $before.Hash -and $afterCreate.Length -eq $before.Length)) { throw "saved_actions did not update after create" }
    $record = Created-Record $savedActionsPath $title
    if (-not $record) { throw "created record not found" }
    Save-Json $record $paths.CreatedRecord
    $actionId = [string]$record.id
    if ([string]$record.target_kind -ne "app" -or [string]$record.target -ne "notepad.exe" -or -not (@($record.aliases) -contains $alias)) { throw "created record content incorrect" }
    Step $paths "created record verified id=$actionId"

    $overlayInput = $null
    $deadline = (Get-Date).AddSeconds(8)
    while ((Get-Date) -lt $deadline -and -not $overlayInput) {
        $overlayInput = Find-ByAutomationSuffix ([System.Windows.Automation.AutomationElement]::RootElement) "commandInputLine" "ControlType.Edit"
        Start-Sleep -Milliseconds 200
    }
    if (-not $overlayInput) { throw "overlay input not found after create" }
    $confirmNeeded = (Marker-Count $paths "RENDERER_MAIN\|COMMAND_CONFIRM_READY\|action_id=$actionId") + 1
    Set-Value $paths $overlayInput $phrase "created task command"
    Click-Element $paths $overlayInput "overlay input"
    Send-Key 0x0D
    if (-not (Wait-Marker $paths "RENDERER_MAIN\|COMMAND_CONFIRM_READY\|action_id=$actionId" $confirmNeeded 8)) { throw "created task did not resolve to confirm" }
    Capture-Screen $paths $paths.ConfirmPng
    $launchNeeded = (Marker-Count $paths "RENDERER_MAIN\|COMMAND_LAUNCH_REQUEST_SENT\|action_id=$actionId") + 1
    Send-Key 0x0D
    if (-not (Wait-Marker $paths "RENDERER_MAIN\|COMMAND_LAUNCH_REQUEST_SENT\|action_id=$actionId" $launchNeeded 8)) { throw "created task did not emit launch request" }
    Capture-Screen $paths $paths.ResultPng

    $notepadSeen = $false
    $deadline = (Get-Date).AddSeconds(8)
    while ((Get-Date) -lt $deadline) {
        $launched = @(Get-Process -Name notepad -ErrorAction SilentlyContinue | Where-Object { $baselineNotepadIds -notcontains [int]$_.Id })
        if ($launched.Count -gt 0) {
            Step $paths "notepad launch observed pid=$($launched[0].Id)"
            $notepadSeen = $true
            break
        }
        Start-Sleep -Milliseconds 250
    }
    if (-not $notepadSeen) { throw "notepad.exe launch not observed" }

    Stop-Runtime $paths
    Wait-Marker $paths "RENDERER_MAIN\|TRAY_ICON_HIDDEN" 1 8 | Out-Null
    $cleanup = Cleanup-Notepad $paths $baselineNotepadIds
    $restored = Restore-Saved $paths $savedActionsPath $hadOriginal
    if ($before.Exists -ne $restored.Exists -or $before.Hash -ne $restored.Hash -or $before.Length -ne $restored.Length) { throw "saved_actions restore did not match original snapshot" }
    $leftoverRuntime = @(Get-Process | Where-Object { $_.ProcessName -match "^(Nexus|orin|jarvis)$" })
    if ($leftoverRuntime.Count -gt 0) { throw "leftover runtime process count=$($leftoverRuntime.Count)" }

    @(
        "RESULT: PASS",
        "ARTIFACT_ROOT: $($paths.Root)",
        "RUNTIME_LOG: $($paths.RuntimeLog)",
        "STEP_LOG: $($paths.StepLog)",
        "CREATED_ACTION_ID: $actionId",
        "CREATED_PHRASE: $phrase",
        "CREATED_RECORD: $($paths.CreatedRecord)",
        "SAVED_ACTIONS_AFTER_CREATE: $($paths.AfterCreate)",
        "SAVED_ACTIONS_RESTORED: $($paths.Restored)",
        "PERSISTED_STATE_UPDATED: confirmed",
        "CATALOG_RELOAD: confirmed",
        "CREATED_TASK_RESOLUTION: confirmed",
        "CONFIRM_RESULT_FLOW: PASS",
        "CLEANUP_RESULT: $cleanup"
    ) | Set-Content -LiteralPath $paths.Summary
    Step $paths "FB038_SEAM3_LIVE_VALIDATION|PASS|summary=$($paths.Summary)"
    Write-Output "FB038_SEAM3_LIVE_VALIDATION|PASS|summary=$($paths.Summary)"
} catch {
    try { Stop-Runtime $paths } catch {}
    try { $cleanup = Cleanup-Notepad $paths $baselineNotepadIds } catch {}
    try { if (-not $restored) { $restored = Restore-Saved $paths $savedActionsPath $hadOriginal } } catch {}
    @(
        "RESULT: FAIL",
        "ARTIFACT_ROOT: $($paths.Root)",
        "RUNTIME_LOG: $($paths.RuntimeLog)",
        "STEP_LOG: $($paths.StepLog)",
        "FAILURE: $($_.Exception.Message)",
        "LAST_PROGRESS: $script:LastProgress",
        "CLEANUP_RESULT: $cleanup"
    ) | Set-Content -LiteralPath $paths.Summary
    Write-Error $_
    exit 1
} finally {
    Pop-Location
}
