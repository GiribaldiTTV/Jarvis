param(
    [int]$StartupTimeoutSeconds = 45,
    [int]$ActionTimeoutSeconds = 12,
    [int]$ExitConfirmationTimeoutSeconds = 18,
    [switch]$KeepRuntimeOpenOnFailure
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;

public static class CodexHumanClientWin32 {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
    [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    private delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [StructLayout(LayoutKind.Sequential)]
    private struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct NOTIFYICONIDENTIFIER {
        public uint cbSize;
        public IntPtr hWnd;
        public uint uID;
        public Guid guidItem;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct INPUT {
        public uint type;
        public MOUSEINPUT mi;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct MOUSEINPUT {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [DllImport("user32.dll")] private static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern int GetWindowText(IntPtr hWnd, StringBuilder lpWindowText, int nMaxCount);
    [DllImport("user32.dll")] private static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] private static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] private static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")] private static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);
    [DllImport("user32.dll")] private static extern int GetSystemMetrics(int nIndex);
    [DllImport("user32.dll")] private static extern IntPtr WindowFromPoint(POINT point);
    [DllImport("shell32.dll")] private static extern int Shell_NotifyIconGetRect(ref NOTIFYICONIDENTIFIER identifier, out RECT iconLocation);

    [StructLayout(LayoutKind.Sequential)]
    private struct POINT {
        public int X;
        public int Y;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct CURSORINFO {
        public int cbSize;
        public int flags;
        public IntPtr hCursor;
        public POINT ptScreenPos;
    }

    [DllImport("user32.dll")] private static extern bool GetCursorInfo(out CURSORINFO pci);
    [DllImport("user32.dll", SetLastError = true)] private static extern IntPtr LoadCursor(IntPtr hInstance, IntPtr lpCursorName);
    [DllImport("user32.dll")] private static extern IntPtr SendMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] private static extern IntPtr GetAncestor(IntPtr hWnd, uint gaFlags);

    private static IntPtr LoadSystemCursor(int cursorId) {
        return LoadCursor(IntPtr.Zero, new IntPtr(cursorId));
    }

    public static string GetCursorKind() {
        CURSORINFO info = new CURSORINFO();
        info.cbSize = Marshal.SizeOf(typeof(CURSORINFO));
        if (!GetCursorInfo(out info) || info.hCursor == IntPtr.Zero) {
            return "unknown";
        }
        if (info.hCursor == LoadSystemCursor(32644)) { return "size-west-east"; }
        if (info.hCursor == LoadSystemCursor(32645)) { return "size-north-south"; }
        if (info.hCursor == LoadSystemCursor(32642)) { return "size-northwest-southeast"; }
        if (info.hCursor == LoadSystemCursor(32643)) { return "size-northeast-southwest"; }
        if (info.hCursor == LoadSystemCursor(32512)) { return "arrow"; }
        return "other:" + info.hCursor.ToString();
    }

    public static string GetNativeHitTestKind(long hwndValue, int x, int y) {
        if (hwndValue == 0) { return "hwnd-zero"; }
        IntPtr hwnd = new IntPtr(hwndValue);
        int lParamValue = unchecked((int)(((y & 0xFFFF) << 16) | (x & 0xFFFF)));
        int result = SendMessage(hwnd, 0x0084, IntPtr.Zero, new IntPtr(lParamValue)).ToInt32();
        switch (result) {
            case 10: return "htleft";
            case 11: return "htright";
            case 12: return "httop";
            case 13: return "httopleft";
            case 14: return "httopright";
            case 15: return "htbottom";
            case 16: return "htbottomleft";
            case 17: return "htbottomright";
            case 1: return "htclient";
            case 0: return "htnowhere";
            default: return "ht:" + result.ToString();
        }
    }

    public static long GetRootWindowHandleAtPoint(int x, int y) {
        POINT point = new POINT();
        point.X = x;
        point.Y = y;
        IntPtr hwnd = WindowFromPoint(point);
        if (hwnd == IntPtr.Zero) { return 0; }
        IntPtr root = GetAncestor(hwnd, 2);
        if (root == IntPtr.Zero) { root = hwnd; }
        return root.ToInt64();
    }

    private static void SendMouseButton(uint downFlag, uint upFlag) {
        INPUT[] inputs = new INPUT[2];
        inputs[0].type = 0;
        inputs[0].mi.dwFlags = downFlag;
        inputs[1].type = 0;
        inputs[1].mi.dwFlags = upFlag;
        SendInput(2, inputs, Marshal.SizeOf(typeof(INPUT)));
    }

    public static void SendLeftClick() {
        SendMouseButton(0x0002, 0x0004);
    }

    public static void SendAbsoluteLeftClick(int x, int y) {
        int virtualX = GetSystemMetrics(76);
        int virtualY = GetSystemMetrics(77);
        int virtualWidth = GetSystemMetrics(78);
        int virtualHeight = GetSystemMetrics(79);
        int absoluteX = (int)Math.Round(((double)(x - virtualX) * 65535.0) / Math.Max(1, virtualWidth - 1));
        int absoluteY = (int)Math.Round(((double)(y - virtualY) * 65535.0) / Math.Max(1, virtualHeight - 1));
        INPUT[] inputs = new INPUT[3];
        inputs[0].type = 0;
        inputs[0].mi.dx = absoluteX;
        inputs[0].mi.dy = absoluteY;
        inputs[0].mi.dwFlags = 0x0001 | 0x4000 | 0x8000;
        inputs[1].type = 0;
        inputs[1].mi.dwFlags = 0x0002;
        inputs[2].type = 0;
        inputs[2].mi.dwFlags = 0x0004;
        SendInput(3, inputs, Marshal.SizeOf(typeof(INPUT)));
    }

    public static void SendRightClick() {
        SendMouseButton(0x0008, 0x0010);
    }

    public static string GetWindowSummaryAtPoint(int x, int y) {
        POINT point = new POINT();
        point.X = x;
        point.Y = y;
        IntPtr hwnd = WindowFromPoint(point);
        if (hwnd == IntPtr.Zero) {
            return "hwnd=0";
        }
        StringBuilder className = new StringBuilder(256);
        StringBuilder title = new StringBuilder(512);
        GetClassName(hwnd, className, className.Capacity);
        GetWindowText(hwnd, title, title.Capacity);
        uint processId;
        GetWindowThreadProcessId(hwnd, out processId);
        RECT rect;
        string rectText = "rect=unknown";
        if (GetWindowRect(hwnd, out rect)) {
            rectText = string.Format("rect={0},{1},{2},{3}", rect.Left, rect.Top, rect.Right, rect.Bottom);
        }
        return string.Format(
            "hwnd={0}|class={1}|title={2}|pid={3}|{4}",
            hwnd.ToString(),
            className.ToString(),
            title.ToString(),
            processId,
            rectText
        );
    }

    public static int[] GetNotifyIconRectForProcess(int processId) {
        List<IntPtr> candidates = new List<IntPtr>();
        EnumWindows(delegate(IntPtr hWnd, IntPtr lParam) {
            StringBuilder className = new StringBuilder(256);
            GetClassName(hWnd, className, className.Capacity);
            string name = className.ToString();
            if (!name.Contains("TrayIconMessageWindowClass")) {
                return true;
            }

            uint windowProcessId;
            GetWindowThreadProcessId(hWnd, out windowProcessId);
            if (windowProcessId == (uint)processId) {
                candidates.Add(hWnd);
            }

            return true;
        }, IntPtr.Zero);

        foreach (IntPtr hWnd in candidates) {
            for (uint uid = 0; uid < 16; uid++) {
                NOTIFYICONIDENTIFIER identifier = new NOTIFYICONIDENTIFIER();
                identifier.cbSize = (uint)Marshal.SizeOf(typeof(NOTIFYICONIDENTIFIER));
                identifier.hWnd = hWnd;
                identifier.uID = uid;
                identifier.guidItem = Guid.Empty;

                RECT rect;
                int result = Shell_NotifyIconGetRect(ref identifier, out rect);
                if (result == 0 && rect.Right > rect.Left && rect.Bottom > rect.Top) {
                    return new int[] { rect.Left, rect.Top, rect.Right, rect.Bottom };
                }
            }
        }

        return new int[0];
    }

    public static int[] GetVisiblePopupRectForProcess(int processId) {
        int[] result = new int[0];
        EnumWindows(delegate(IntPtr hWnd, IntPtr lParam) {
            if (result.Length == 4) {
                return true;
            }

            uint windowProcessId;
            GetWindowThreadProcessId(hWnd, out windowProcessId);
            if (windowProcessId != (uint)processId || !IsWindowVisible(hWnd)) {
                return true;
            }

            StringBuilder className = new StringBuilder(256);
            GetClassName(hWnd, className, className.Capacity);
            string classValue = className.ToString();
            StringBuilder title = new StringBuilder(512);
            GetWindowText(hWnd, title, title.Capacity);
            string titleValue = title.ToString();
            if (!classValue.Contains("QWindowPopup") && classValue != "#32768" && titleValue != "Nexus Desktop AI Tray") {
                return true;
            }

            RECT rect;
            if (GetWindowRect(hWnd, out rect) && rect.Right > rect.Left && rect.Bottom > rect.Top) {
                result = new int[] { rect.Left, rect.Top, rect.Right, rect.Bottom };
            }

            return true;
        }, IntPtr.Zero);

        return result;
    }

    public static long GetVisiblePopupHandleForProcess(int processId) {
        IntPtr result = IntPtr.Zero;
        EnumWindows(delegate(IntPtr hWnd, IntPtr lParam) {
            if (result != IntPtr.Zero) {
                return true;
            }

            uint windowProcessId;
            GetWindowThreadProcessId(hWnd, out windowProcessId);
            if (windowProcessId != (uint)processId || !IsWindowVisible(hWnd)) {
                return true;
            }

            StringBuilder className = new StringBuilder(256);
            GetClassName(hWnd, className, className.Capacity);
            string classValue = className.ToString();
            StringBuilder title = new StringBuilder(512);
            GetWindowText(hWnd, title, title.Capacity);
            string titleValue = title.ToString();
            if (!classValue.Contains("QWindowPopup") && !classValue.Contains("QMenu") && classValue != "#32768" && titleValue != "Nexus Desktop AI Tray") {
                return true;
            }

            RECT rect;
            if (GetWindowRect(hWnd, out rect) && rect.Right > rect.Left && rect.Bottom > rect.Top) {
                result = hWnd;
            }

            return true;
        }, IntPtr.Zero);

        return result.ToInt64();
    }

    public static int[] GetVisibleDashboardRectForProcess(int processId) {
        int[] result = new int[0];
        EnumWindows(delegate(IntPtr hWnd, IntPtr lParam) {
            if (result.Length == 4) {
                return true;
            }

            uint windowProcessId;
            GetWindowThreadProcessId(hWnd, out windowProcessId);
            if (windowProcessId != (uint)processId || !IsWindowVisible(hWnd)) {
                return true;
            }

            StringBuilder title = new StringBuilder(512);
            GetWindowText(hWnd, title, title.Capacity);
            string titleValue = title.ToString();
            if (titleValue != "Nexus Desktop AI") {
                return true;
            }

            StringBuilder className = new StringBuilder(256);
            GetClassName(hWnd, className, className.Capacity);
            string classValue = className.ToString();
            if (!classValue.Contains("QWindowIcon")) {
                return true;
            }

            RECT rect;
            if (GetWindowRect(hWnd, out rect) && rect.Right > rect.Left && rect.Bottom > rect.Top) {
                result = new int[] { rect.Left, rect.Top, rect.Right, rect.Bottom };
            }

            return true;
        }, IntPtr.Zero);

        return result;
    }

    public static long GetVisibleDashboardHandleForProcess(int processId) {
        IntPtr result = IntPtr.Zero;
        EnumWindows(delegate(IntPtr hWnd, IntPtr lParam) {
            if (result != IntPtr.Zero) {
                return true;
            }

            uint windowProcessId;
            GetWindowThreadProcessId(hWnd, out windowProcessId);
            if (windowProcessId != (uint)processId || !IsWindowVisible(hWnd)) {
                return true;
            }

            StringBuilder title = new StringBuilder(512);
            GetWindowText(hWnd, title, title.Capacity);
            string titleValue = title.ToString();
            if (titleValue != "Nexus Desktop AI") {
                return true;
            }

            StringBuilder className = new StringBuilder(256);
            GetClassName(hWnd, className, className.Capacity);
            string classValue = className.ToString();
            if (!classValue.Contains("QWindowIcon")) {
                return true;
            }

            RECT rect;
            if (GetWindowRect(hWnd, out rect) && rect.Right > rect.Left && rect.Bottom > rect.Top) {
                result = hWnd;
            }

            return true;
        }, IntPtr.Zero);

        return result.ToInt64();
    }

    public static int[] GetVisibleWindowRectForProcessByTitle(int processId, string expectedTitle) {
        int[] result = new int[0];
        EnumWindows(delegate(IntPtr hWnd, IntPtr lParam) {
            if (result.Length == 4) {
                return true;
            }

            uint windowProcessId;
            GetWindowThreadProcessId(hWnd, out windowProcessId);
            if (windowProcessId != (uint)processId || !IsWindowVisible(hWnd)) {
                return true;
            }

            StringBuilder title = new StringBuilder(512);
            GetWindowText(hWnd, title, title.Capacity);
            if (title.ToString() != expectedTitle) {
                return true;
            }

            RECT rect;
            if (GetWindowRect(hWnd, out rect) && rect.Right > rect.Left && rect.Bottom > rect.Top) {
                result = new int[] { rect.Left, rect.Top, rect.Right, rect.Bottom };
            }

            return true;
        }, IntPtr.Zero);

        return result;
    }
}
"@

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
$LogRoot = Join-Path $RootDir "dev\logs\fam_006_human_client_validation\$Stamp"
$ScreenshotRoot = Join-Path $LogRoot "screenshots"
$ManifestPath = Join-Path $LogRoot "human_client_manifest.json"
$LatestManifestPath = Join-Path $RootDir "dev\logs\fam_006_human_client_validation\latest_manifest.json"
$DesktopShortcutPath = Join-Path $env:USERPROFILE "OneDrive\Desktop\Nexus Desktop Launcher.lnk"

New-Item -ItemType Directory -Force -Path $ScreenshotRoot | Out-Null

$script:Steps = New-Object System.Collections.Generic.List[object]
$script:Artifacts = New-Object System.Collections.Generic.List[object]
$script:RuntimeProcessIds = New-Object System.Collections.Generic.List[int]
$script:RuntimeLogPath = ""
$script:CleanupNotes = New-Object System.Collections.Generic.List[string]

function Add-Step {
    param(
        [string]$Id,
        [string]$Title,
        [string]$Status,
        [string]$Detail,
        [string]$ProofClass = "live-human-ui",
        [hashtable]$Evidence = @{}
    )

    $script:Steps.Add([ordered]@{
        id = $Id
        title = $Title
        status = $Status
        detail = $Detail
        proofClass = $ProofClass
        evidence = $Evidence
        timestamp = (Get-Date).ToUniversalTime().ToString("o")
    }) | Out-Null
}

function Add-Artifact {
    param([string]$Label, [string]$Path)
    $script:Artifacts.Add([ordered]@{ label = $Label; path = $Path }) | Out-Null
}

function Capture-VirtualScreenshot {
    param([string]$Label)

    $safe = ($Label -replace "[^A-Za-z0-9_-]", "_").Trim("_")
    $path = Join-Path $ScreenshotRoot ("{0}_{1}.png" -f ((Get-Date -Format "HHmmss_fff")), $safe)
    $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bounds.Size)
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    Add-Artifact -Label $Label -Path $path
    return $path
}

function Send-Key {
    param([byte]$Vk)
    [CodexHumanClientWin32]::keybd_event($Vk, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [CodexHumanClientWin32]::keybd_event($Vk, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 180
}

function Send-WinB {
    [CodexHumanClientWin32]::keybd_event(0x5B, 0, 0, [UIntPtr]::Zero)
    [CodexHumanClientWin32]::keybd_event(0x42, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 100
    [CodexHumanClientWin32]::keybd_event(0x42, 0, 2, [UIntPtr]::Zero)
    [CodexHumanClientWin32]::keybd_event(0x5B, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function Send-ShiftF10 {
    [CodexHumanClientWin32]::keybd_event(0x10, 0, 0, [UIntPtr]::Zero)
    [CodexHumanClientWin32]::keybd_event(0x79, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [CodexHumanClientWin32]::keybd_event(0x79, 0, 2, [UIntPtr]::Zero)
    [CodexHumanClientWin32]::keybd_event(0x10, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 450
}

function Get-FocusedName {
    try { return [System.Windows.Automation.AutomationElement]::FocusedElement.Current.Name } catch { return "" }
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
        $matches = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            $condition
        )
        for ($i = 0; $i -lt $matches.Count; $i++) {
            $element = $matches.Item($i)
            try {
                $rect = $element.Current.BoundingRectangle
                $type = $element.Current.ControlType.ProgrammaticName
                if (-not $rect.IsEmpty -and -not $element.Current.IsOffscreen -and ($ControlTypeName -eq "" -or $type -eq $ControlTypeName)) {
                    return $element
                }
            } catch {}
        }
        Start-Sleep -Milliseconds 250
    }
    return $null
}

function Find-VisibleElementByNameContains {
    param(
        [string]$NamePart,
        [string]$ControlTypeName = "",
        [int]$TimeoutSeconds = 8
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $matches = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition
        )
        for ($i = 0; $i -lt $matches.Count; $i++) {
            $element = $matches.Item($i)
            try {
                $name = [string]$element.Current.Name
                $rect = $element.Current.BoundingRectangle
                $type = $element.Current.ControlType.ProgrammaticName
                if ($name -like "*$NamePart*" -and -not $rect.IsEmpty -and -not $element.Current.IsOffscreen -and ($ControlTypeName -eq "" -or $type -eq $ControlTypeName)) {
                    return $element
                }
            } catch {}
        }
        Start-Sleep -Milliseconds 250
    }
    return $null
}

function Click-ElementCenter {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [string]$Label,
        [ValidateSet("left", "right")]
        [string]$Button = "left"
    )

    if (-not $Element) { throw "Missing element for $Label" }
    $rect = $Element.Current.BoundingRectangle
    if ($rect.IsEmpty -or $Element.Current.IsOffscreen) { throw "Element '$Label' is offscreen or empty" }
    $x = [int]($rect.Left + ($rect.Width / 2))
    $y = [int]($rect.Top + ($rect.Height / 2))
    $down = if ($Button -eq "right") { 0x0008 } else { 0x0002 }
    $up = if ($Button -eq "right") { 0x0010 } else { 0x0004 }
    [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 90
    [CodexHumanClientWin32]::mouse_event($down, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 90
    [CodexHumanClientWin32]::mouse_event($up, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 400
}

function Find-VisibleRuntimeElementByName {
    param(
        [string]$Name,
        [string]$ControlTypeName = "",
        [int]$TimeoutSeconds = 8
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $runtimeIds = @((Find-ProcessesForLogRoot) | ForEach-Object { [int]$_.ProcessId })
        if ($runtimeIds.Count -eq 0) {
            Start-Sleep -Milliseconds 180
            continue
        }
        $matches = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $Name))
        )
        for ($i = 0; $i -lt $matches.Count; $i++) {
            $element = $matches.Item($i)
            try {
                $rect = $element.Current.BoundingRectangle
                $type = $element.Current.ControlType.ProgrammaticName
                if (
                    $runtimeIds -contains [int]$element.Current.ProcessId -and
                    -not $rect.IsEmpty -and
                    -not $element.Current.IsOffscreen -and
                    ($ControlTypeName -eq "" -or $type -eq $ControlTypeName)
                ) {
                    return $element
                }
            } catch {}
        }
        Start-Sleep -Milliseconds 250
    }
    return $null
}

function Click-RuntimeButtonAndWaitForDialog {
    param(
        [string]$ButtonName,
        [string]$DialogTitle,
        [string]$StepId,
        [string]$StepTitle,
        [string]$ExpectedOpenMarker = "",
        [string]$DismissMarker = ""
    )

    $beforeLines = (Read-RuntimeLines).Count
    $button = Find-VisibleRuntimeElementByName -Name $ButtonName -ControlTypeName "ControlType.Button" -TimeoutSeconds 8
    if (-not $button) {
        $shot = Capture-VirtualScreenshot ("ncp_button_missing_{0}" -f ($ButtonName -replace "[^A-Za-z0-9_-]", "_"))
        Add-Step -Id $StepId -Title $StepTitle -Status "FAIL" -Detail "Visible runtime button '$ButtonName' was not found." -Evidence @{ screenshot = $shot }
        throw "Visible runtime button '$ButtonName' was not found"
    }
    $rect = $button.Current.BoundingRectangle
    Click-ElementCenter -Element $button -Label $ButtonName
    Start-Sleep -Milliseconds 650
    if ($ExpectedOpenMarker -and -not (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedOpenMarker -AfterLine $beforeLines -TimeoutSeconds 8)) {
        $shot = Capture-VirtualScreenshot ("ncp_button_missing_open_marker_{0}" -f ($ButtonName -replace "[^A-Za-z0-9_-]", "_"))
        Add-Step -Id $StepId -Title $StepTitle -Status "FAIL" -Detail "Clicked '$ButtonName' but expected runtime marker '$ExpectedOpenMarker' was not emitted." -Evidence @{
            screenshot = $shot
            buttonRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
            expectedOpenMarker = $ExpectedOpenMarker
            runtimeLinesBeforeClick = $beforeLines
        }
        throw "Clicked '$ButtonName' but expected runtime marker '$ExpectedOpenMarker' was not emitted"
    }
    $dialogRect = Wait-ForVisibleRuntimeWindowByTitle -Title $DialogTitle -TimeoutSeconds 8
    $shotAfterClick = Capture-VirtualScreenshot ("ncp_button_dialog_{0}" -f ($ButtonName -replace "[^A-Za-z0-9_-]", "_"))
    if (-not $dialogRect -or $dialogRect.Count -ne 4) {
        Add-Step -Id $StepId -Title $StepTitle -Status "FAIL" -Detail "Clicked '$ButtonName' but dialog '$DialogTitle' did not become visible." -Evidence @{
            screenshot = $shotAfterClick
            buttonRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
            runtimeLinesBeforeClick = $beforeLines
        }
        throw "Clicked '$ButtonName' but dialog '$DialogTitle' did not become visible"
    }

    Add-Step -Id $StepId -Title $StepTitle -Status "PASS" -Detail "Clicked '$ButtonName' and visible dialog '$DialogTitle' opened." -Evidence @{
        screenshot = $shotAfterClick
        buttonRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
        dialogRect = $dialogRect
    }
    $dismiss = Dismiss-VisibleRuntimeDialog -Title $DialogTitle -TimeoutSeconds 5 -ExpectedDismissMarker $DismissMarker
    if (-not $dismiss.dismissed) {
        throw "Visible runtime dialog '$DialogTitle' was opened by '$ButtonName' but was not dismissible through the human-client cleanup path"
    }
    Start-Sleep -Milliseconds 500
}

function Click-RuntimeButtonAndWaitForCloseableWindow {
    param(
        [string]$ButtonName,
        [string]$DialogTitle,
        [string]$StepId,
        [string]$StepTitle,
        [string]$ExpectedOpenMarker = "",
        [string]$DismissMarker = ""
    )

    $beforeLines = (Read-RuntimeLines).Count
    $button = Find-VisibleRuntimeElementByName -Name $ButtonName -ControlTypeName "ControlType.Button" -TimeoutSeconds 8
    if (-not $button) {
        $shot = Capture-VirtualScreenshot ("ncp_button_missing_{0}" -f ($ButtonName -replace "[^A-Za-z0-9_-]", "_"))
        Add-Step -Id $StepId -Title $StepTitle -Status "FAIL" -Detail "Visible runtime button '$ButtonName' was not found." -Evidence @{ screenshot = $shot }
        throw "Visible runtime button '$ButtonName' was not found"
    }
    $rect = $button.Current.BoundingRectangle
    Click-ElementCenter -Element $button -Label $ButtonName
    Start-Sleep -Milliseconds 650
    if ($ExpectedOpenMarker -and -not (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedOpenMarker -AfterLine $beforeLines -TimeoutSeconds 8)) {
        $shot = Capture-VirtualScreenshot ("ncp_button_missing_open_marker_{0}" -f ($ButtonName -replace "[^A-Za-z0-9_-]", "_"))
        Add-Step -Id $StepId -Title $StepTitle -Status "FAIL" -Detail "Clicked '$ButtonName' but expected runtime marker '$ExpectedOpenMarker' was not emitted." -Evidence @{
            screenshot = $shot
            buttonRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
            expectedOpenMarker = $ExpectedOpenMarker
            runtimeLinesBeforeClick = $beforeLines
        }
        throw "Clicked '$ButtonName' but expected runtime marker '$ExpectedOpenMarker' was not emitted"
    }
    $dialogRect = Wait-ForVisibleRuntimeWindowByTitle -Title $DialogTitle -TimeoutSeconds 8
    $shotAfterClick = Capture-VirtualScreenshot ("ncp_button_window_{0}" -f ($ButtonName -replace "[^A-Za-z0-9_-]", "_"))
    if (-not $dialogRect -or $dialogRect.Count -ne 4) {
        Add-Step -Id $StepId -Title $StepTitle -Status "FAIL" -Detail "Clicked '$ButtonName' but window '$DialogTitle' did not become visible." -Evidence @{
            screenshot = $shotAfterClick
            buttonRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
        }
        throw "Clicked '$ButtonName' but window '$DialogTitle' did not become visible"
    }
    Add-Step -Id $StepId -Title $StepTitle -Status "PASS" -Detail "Clicked '$ButtonName' and visible window '$DialogTitle' opened." -Evidence @{
        screenshot = $shotAfterClick
        buttonRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
        dialogRect = $dialogRect
    }
    try {
        $null = Click-VisibleRuntimeDialogButton -Title $DialogTitle -ButtonName "Close" -TimeoutSeconds 3
    } catch {
        $dismiss = Dismiss-VisibleRuntimeDialog -Title $DialogTitle -TimeoutSeconds 4 -ExpectedDismissMarker $DismissMarker
        if (-not $dismiss.dismissed) {
            throw
        }
    }
    Start-Sleep -Milliseconds 500
}

function Drag-FromTo {
    param([int]$StartX, [int]$StartY, [int]$EndX, [int]$EndY, [string]$Label)
    [CodexHumanClientWin32]::SetCursorPos($StartX, $StartY) | Out-Null
    Start-Sleep -Milliseconds 150
    [CodexHumanClientWin32]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    $steps = 14
    for ($i = 1; $i -le $steps; $i++) {
        $x = [int]($StartX + (($EndX - $StartX) * $i / $steps))
        $y = [int]($StartY + (($EndY - $StartY) * $i / $steps))
        [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
        Start-Sleep -Milliseconds 35
    }
    [CodexHumanClientWin32]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 550
}

function Get-CursorKindAtPoint {
    param([int]$X, [int]$Y)
    [CodexHumanClientWin32]::SetCursorPos($X, $Y) | Out-Null
    Start-Sleep -Milliseconds 260
    return [CodexHumanClientWin32]::GetCursorKind()
}

function Get-NativeHitTestKindAtPoint {
    param([long]$WindowHandle, [int]$X, [int]$Y)
    return [CodexHumanClientWin32]::GetNativeHitTestKind($WindowHandle, $X, $Y)
}

function Get-RootWindowHandleAtPoint {
    param([int]$X, [int]$Y)
    return [CodexHumanClientWin32]::GetRootWindowHandleAtPoint($X, $Y)
}

function Test-ResizeCursorKind {
    param([string]$Kind)
    return $Kind -like "size-*"
}

function Test-NonResizeCursorKind {
    param([string]$Kind)
    return $Kind -ne "unknown" -and $Kind -notlike "size-*"
}

function Read-RuntimeLines {
    if (-not $script:RuntimeLogPath -or -not (Test-Path -LiteralPath $script:RuntimeLogPath)) { return @() }
    try { return Get-Content -LiteralPath $script:RuntimeLogPath -ErrorAction Stop } catch { return @() }
}

function Wait-ForRuntimeMarker {
    param([string]$Marker, [int]$TimeoutSeconds = 10)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ((Read-RuntimeLines) -match [regex]::Escape($Marker)) { return $true }
        Start-Sleep -Milliseconds 250
    }
    return $false
}

function Wait-ForRuntimeMarkerAfterLine {
    param([string]$Marker, [int]$AfterLine = 0, [int]$TimeoutSeconds = 10)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $lines = @(Read-RuntimeLines)
        if ($lines.Count -gt $AfterLine) {
            $tail = $lines[$AfterLine..($lines.Count - 1)]
            if ($tail -match [regex]::Escape($Marker)) { return $true }
        }
        Start-Sleep -Milliseconds 250
    }
    return $false
}

function Wait-ForRuntimeLog {
    param([int]$TimeoutSeconds)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $candidate = Get-ChildItem -Path $LogRoot -Filter "Runtime_*.txt" -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if ($candidate) {
            $script:RuntimeLogPath = $candidate.FullName
            return $true
        }
        Start-Sleep -Milliseconds 250
    }
    return $false
}

function Find-ProcessesForLogRoot {
    $escaped = [regex]::Escape($LogRoot)
    $result = @()
    try {
        $processes = Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
            $_.CommandLine -and ($_.CommandLine -match $escaped)
        }
        foreach ($process in $processes) {
            $result += [ordered]@{ processId = [int]$process.ProcessId; commandLine = [string]$process.CommandLine }
        }
    } catch {}
    return $result
}

function Cleanup-Runtime {
    $processes = Find-ProcessesForLogRoot
    foreach ($process in $processes) {
        try {
            Stop-Process -Id $process.processId -Force -ErrorAction Stop
            $script:CleanupNotes.Add("stopped process $($process.processId)") | Out-Null
        } catch {
            $script:CleanupNotes.Add("failed to stop process $($process.processId): $($_.Exception.Message)") | Out-Null
        }
    }
}

function Open-HiddenTrayOnNexus {
    $runtimeProcesses = Find-ProcessesForLogRoot
    foreach ($process in $runtimeProcesses) {
        $rect = [CodexHumanClientWin32]::GetNotifyIconRectForProcess([int]$process.ProcessId)
        if ($rect -and $rect.Length -eq 4) {
            $x = [int](($rect[0] + $rect[2]) / 2)
            $y = [int](($rect[1] + $rect[3]) / 2)
            [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
            Start-Sleep -Milliseconds 160
            [CodexHumanClientWin32]::SendRightClick()
            Start-Sleep -Milliseconds 650
            return
        }
    }

    throw "Nexus tray icon rectangle not found for runtime process IDs: $($runtimeProcesses.ProcessId -join ', ')"
}

function Get-VisibleTrayMenuRect {
    param([int]$TimeoutSeconds = 5)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $runtimeProcesses = Find-ProcessesForLogRoot
        foreach ($process in $runtimeProcesses) {
            $rect = [CodexHumanClientWin32]::GetVisiblePopupRectForProcess([int]$process.ProcessId)
            if ($rect -and $rect.Length -eq 4) {
                return $rect
            }
        }
        $fallbackButton = Find-VisibleRuntimeElementByName -Name $ButtonName -ControlTypeName "ControlType.Button" -TimeoutSeconds 1
        if ($fallbackButton) {
            try {
                $rect = $fallbackButton.Current.BoundingRectangle
                if ($rect.Width -gt 0 -and $rect.Height -gt 0 -and $fallbackButton.Current.IsEnabled) {
                    $x = [int]($rect.X + ($rect.Width / 2))
                    $y = [int]($rect.Y + ($rect.Height / 2))
                    [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
                    Start-Sleep -Milliseconds 150
                    [CodexHumanClientWin32]::SendLeftClick()
                    return @{
                        button = $ButtonName
                        clicked = @($x, $y)
                        buttonRect = @(
                            [int]$rect.X,
                            [int]$rect.Y,
                            [int]($rect.X + $rect.Width),
                            [int]($rect.Y + $rect.Height)
                        )
                        fallback = "runtime-process-button-search"
                        dialogRect = $lastDialogRect
                    }
                }
            } catch {}
        }
        Start-Sleep -Milliseconds 120
    }

    return @()
}

function Get-VisibleTrayMenuHandle {
    param([int]$TimeoutSeconds = 5)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $runtimeProcesses = Find-ProcessesForLogRoot
        foreach ($process in $runtimeProcesses) {
            $handle = [CodexHumanClientWin32]::GetVisiblePopupHandleForProcess([int]$process.ProcessId)
            if ($handle -and $handle -ne 0) {
                return [IntPtr]$handle
            }
        }
        Start-Sleep -Milliseconds 120
    }

    return [IntPtr]::Zero
}

function Test-RectCenterInside {
    param(
        [Parameter(Mandatory = $true)]$InnerRect,
        [Parameter(Mandatory = $true)]$OuterRect
    )

    if ($InnerRect.IsEmpty -or $OuterRect.IsEmpty -or $InnerRect.Width -le 0 -or $InnerRect.Height -le 0) {
        return $false
    }

    $centerX = [double]($InnerRect.X + ($InnerRect.Width / 2))
    $centerY = [double]($InnerRect.Y + ($InnerRect.Height / 2))
    return (
        $centerX -ge [double]$OuterRect.X -and
        $centerX -le [double]($OuterRect.X + $OuterRect.Width) -and
        $centerY -ge [double]$OuterRect.Y -and
        $centerY -le [double]($OuterRect.Y + $OuterRect.Height)
    )
}

function Click-VisibleTrayMenuAction {
    param([string]$ActionName)

    Open-HiddenTrayOnNexus
    $menuHandle = Get-VisibleTrayMenuHandle -TimeoutSeconds 5
    if ($menuHandle -eq [IntPtr]::Zero) {
        throw "Visible Nexus tray context menu did not appear for action '$ActionName'"
    }

    $menuElement = [System.Windows.Automation.AutomationElement]::FromHandle($menuHandle)
    if (-not $menuElement) {
        throw "Visible Nexus tray context menu was found but UIAutomation could not bind to it for action '$ActionName'"
    }

    $menuRect = $menuElement.Current.BoundingRectangle
    $items = $menuElement.FindAll(
        [System.Windows.Automation.TreeScope]::Subtree,
        [System.Windows.Automation.Condition]::TrueCondition
    )
    $target = $null
    $targetControlType = ""
    foreach ($preferredControlType in @(
        [System.Windows.Automation.ControlType]::Button,
        [System.Windows.Automation.ControlType]::MenuItem
    )) {
        for ($i = 0; $i -lt $items.Count; $i++) {
            $item = $items.Item($i)
            if (
                $item.Current.ControlType -eq $preferredControlType -and
                $item.Current.Name -eq $ActionName -and
                $item.Current.IsEnabled
            ) {
                $candidateRect = $item.Current.BoundingRectangle
                if (Test-RectCenterInside -InnerRect $candidateRect -OuterRect $menuRect) {
                    $target = $item
                    $targetControlType = $item.Current.ControlType.ProgrammaticName
                    break
                }
            }
        }
        if ($target) { break }
    }
    $coordinateFallback = $false
    if (-not $target) {
        $nativeY = $null
        if ($ActionName -in @("Enable HUD Feature", "Disable HUD Feature")) {
            $nativeY = [int]($menuRect.Y + 17)
        } elseif ($ActionName -in @("Close HUD Dashboard", "Open HUD Dashboard")) {
            $nativeY = [int]($menuRect.Y + 39)
        } elseif ($ActionName -eq "HUD Overlay Deferred") {
            $nativeY = [int]($menuRect.Y + 61)
        } elseif ($ActionName -eq "Open Command Overlay") {
            $nativeY = [int]($menuRect.Y + 89)
        } elseif ($ActionName -eq "Create Custom Task") {
            $nativeY = [int]($menuRect.Y + 111)
        } elseif ($ActionName -eq "Exit Nexus Desktop AI") {
            $nativeY = [int]($menuRect.Y + $menuRect.Height - 12)
        }
        if ($null -ne $nativeY) {
            $targetControlType = "ControlType.NativeMenuCoordinate"
            $coordinateFallback = $true
            $itemRect = [pscustomobject]@{
                X = [double]$menuRect.X
                Y = [double]($nativeY - 11)
                Width = [double]$menuRect.Width
                Height = 22.0
            }
        }
    }
    if (-not $target -and -not $coordinateFallback) {
        throw "Visible Nexus tray context menu did not expose enabled action '$ActionName'"
    }
    if ($target) {
        $itemRect = $target.Current.BoundingRectangle
    }
    if ($itemRect.Width -le 0 -or $itemRect.Height -le 0) {
        throw "Visible Nexus tray action '$ActionName' has invalid bounds '$itemRect'"
    }

    if ($coordinateFallback) {
        $x = [int]($menuRect.X + [Math]::Min(115, [Math]::Max(70, $menuRect.Width / 2)))
    } elseif ($targetControlType -eq "ControlType.Button") {
        $x = [int]($itemRect.X + ($itemRect.Width / 2))
    } else {
        $x = [int]($itemRect.X + [Math]::Min(42, [Math]::Max(16, $itemRect.Width / 3)))
    }
    $y = [int]($itemRect.Y + ($itemRect.Height / 2))

    $menuShot = Capture-VirtualScreenshot ("tray_menu_before_{0}" -f ($ActionName -replace "[^A-Za-z0-9_-]", "_"))
    [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 1800
    $windowAtPointBeforeClick = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($x, $y)
    [CodexHumanClientWin32]::SendAbsoluteLeftClick($x, $y)
    Start-Sleep -Milliseconds 120
    $windowAtPointAfterClick = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($x, $y)
    $activationMethod = "desktop-shortcut + real-tray-popup + SetCursorPos + SendInput mouse button click on visible tray command control"
    Start-Sleep -Milliseconds 650

    return @{
        screenshot = $menuShot
        activationMethod = $activationMethod
        menuRect = @(
            [int]$menuRect.X,
            [int]$menuRect.Y,
            [int]($menuRect.X + $menuRect.Width),
            [int]($menuRect.Y + $menuRect.Height)
        )
        menuItemRect = @(
            [int]$itemRect.X,
            [int]$itemRect.Y,
            [int]($itemRect.X + $itemRect.Width),
            [int]($itemRect.Y + $itemRect.Height)
        )
        targetControlType = $targetControlType
        coordinateFallback = $coordinateFallback
        clicked = @($x, $y)
        windowAtPointBeforeClick = $windowAtPointBeforeClick
        windowAtPointAfterClick = $windowAtPointAfterClick
    }
}

function Invoke-TrayAction {
    param([string]$ActionName, [string]$ExpectedMarker = "", [int]$TimeoutSeconds = 8)
    $beforeCount = 0
    if ($ExpectedMarker) {
        $beforeCount = ((Read-RuntimeLines) | Select-String -Pattern ([regex]::Escape($ExpectedMarker))).Count
    }
    $clickEvidence = Click-VisibleTrayMenuAction -ActionName $ActionName
    if ($ExpectedMarker) {
        $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
        while ((Get-Date) -lt $deadline) {
            $count = ((Read-RuntimeLines) | Select-String -Pattern ([regex]::Escape($ExpectedMarker))).Count
            if ($count -gt $beforeCount) { return $clickEvidence }
            Start-Sleep -Milliseconds 250
        }
        $afterTimeoutShot = Capture-VirtualScreenshot ("tray_menu_after_timeout_{0}" -f ($ActionName -replace "[^A-Za-z0-9_-]", "_"))
        throw "Tray menu action '$ActionName' did not emit expected marker '$ExpectedMarker'; clicked=($($clickEvidence.clicked -join ',')); before=$($clickEvidence.windowAtPointBeforeClick); after=$($clickEvidence.windowAtPointAfterClick); after_timeout_screenshot=$afterTimeoutShot"
    }
    return $clickEvidence
}

function Get-DashboardWindow {
    $runtimeProcesses = Find-ProcessesForLogRoot
    foreach ($process in $runtimeProcesses) {
        $rect = [CodexHumanClientWin32]::GetVisibleDashboardRectForProcess([int]$process.ProcessId)
        if ($rect -and $rect.Length -eq 4) {
            $handle = [CodexHumanClientWin32]::GetVisibleDashboardHandleForProcess([int]$process.ProcessId)
            $bounds = [pscustomobject]@{
                Left = [double]$rect[0]
                Top = [double]$rect[1]
                Right = [double]$rect[2]
                Bottom = [double]$rect[3]
                Width = [double]($rect[2] - $rect[0])
                Height = [double]($rect[3] - $rect[1])
            }
            return [pscustomobject]@{
                Current = [pscustomobject]@{
                    BoundingRectangle = $bounds
                    NativeWindowHandle = [long]$handle
                }
            }
        }
    }

    return $null
}

function Wait-ForVisibleRuntimeWindowByTitle {
    param([string]$Title, [int]$TimeoutSeconds = 5)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $runtimeProcesses = Find-ProcessesForLogRoot
        $runtimeIds = @($runtimeProcesses | ForEach-Object { [int]$_.ProcessId })
        foreach ($process in $runtimeProcesses) {
            $rect = [CodexHumanClientWin32]::GetVisibleWindowRectForProcessByTitle([int]$process.ProcessId, $Title)
            if ($rect -and $rect.Length -eq 4) {
                return @(
                    [int]$rect[0],
                    [int]$rect[1],
                    [int]$rect[2],
                    [int]$rect[3]
                )
            }
        }
        $matches = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $Title))
        )
        for ($i = 0; $i -lt $matches.Count; $i++) {
            $element = $matches.Item($i)
            try {
                $rect = $element.Current.BoundingRectangle
                if (
                    $runtimeIds -contains [int]$element.Current.ProcessId -and
                    -not $rect.IsEmpty -and
                    -not $element.Current.IsOffscreen
                ) {
                    return @(
                        [int]$rect.X,
                        [int]$rect.Y,
                        [int]($rect.X + $rect.Width),
                        [int]($rect.Y + $rect.Height)
                    )
                }
            } catch {}
        }
        Start-Sleep -Milliseconds 120
    }

    return @()
}

function Click-VisibleRuntimeDialogButton {
    param([string]$Title, [string]$ButtonName, [int]$TimeoutSeconds = 5)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $lastDialogRect = @()
    while ((Get-Date) -lt $deadline) {
        $runtimeProcesses = Find-ProcessesForLogRoot
        $runtimeIds = @($runtimeProcesses | ForEach-Object { [int]$_.processId })
        foreach ($process in $runtimeProcesses) {
            $rect = [CodexHumanClientWin32]::GetVisibleWindowRectForProcessByTitle([int]$process.ProcessId, $Title)
            if ($rect -and $rect.Length -eq 4) {
                $lastDialogRect = @([int]$rect[0], [int]$rect[1], [int]$rect[2], [int]$rect[3])
            }
        }
        $windows = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $Title))
        )
        for ($i = 0; $i -lt $windows.Count; $i++) {
            $windowElement = $windows.Item($i)
            if ($runtimeIds -notcontains [int]$windowElement.Current.ProcessId) {
                continue
            }
            $buttons = $windowElement.FindAll(
                [System.Windows.Automation.TreeScope]::Subtree,
                (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button))
            )
            for ($j = 0; $j -lt $buttons.Count; $j++) {
                $button = $buttons.Item($j)
                if ($button.Current.Name -ne $ButtonName -or -not $button.Current.IsEnabled) {
                    continue
                }
                $rect = $button.Current.BoundingRectangle
                if ($rect.Width -le 0 -or $rect.Height -le 0) {
                    continue
                }
                $x = [int]($rect.X + ($rect.Width / 2))
                $y = [int]($rect.Y + ($rect.Height / 2))
                [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
                Start-Sleep -Milliseconds 150
                [CodexHumanClientWin32]::SendLeftClick()
                return @{
                    button = $ButtonName
                    clicked = @($x, $y)
                    buttonRect = @(
                        [int]$rect.X,
                        [int]$rect.Y,
                        [int]($rect.X + $rect.Width),
                        [int]($rect.Y + $rect.Height)
                    )
                }
            }
        }
        Start-Sleep -Milliseconds 120
    }

    if ($lastDialogRect.Count -eq 4 -and $ButtonName -in @("Yes", "No")) {
        $x = if ($ButtonName -eq "Yes") { [int]($lastDialogRect[2] - 146) } else { [int]($lastDialogRect[2] - 61) }
        $y = [int]($lastDialogRect[3] - 29)
        [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
        Start-Sleep -Milliseconds 150
        [CodexHumanClientWin32]::SendLeftClick()
        return @{
            button = $ButtonName
            clicked = @($x, $y)
            buttonRect = @()
            fallback = "dialog-rect-coordinate-click"
            dialogRect = $lastDialogRect
        }
    }

    throw "Visible runtime dialog '$Title' did not expose enabled button '$ButtonName'"
}

function Dismiss-VisibleRuntimeDialog {
    param([string]$Title, [int]$TimeoutSeconds = 5, [string]$ExpectedDismissMarker = "")

    $before = Wait-ForVisibleRuntimeWindowByTitle -Title $Title -TimeoutSeconds 1
    $beforeLineCount = (Read-RuntimeLines).Count
    if ($before -and $before.Count -eq 4 -and $Title -in @("Create Custom Task", "Create Custom Group")) {
        $x = [int]($before[2] - 205)
        $y = [int]($before[1] + 342)
        [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
        Start-Sleep -Milliseconds 150
        [CodexHumanClientWin32]::SendLeftClick()
        $coordinateDeadline = (Get-Date).AddSeconds($TimeoutSeconds)
        while ((Get-Date) -lt $coordinateDeadline) {
            if ($ExpectedDismissMarker -and (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedDismissMarker -AfterLine $beforeLineCount -TimeoutSeconds 1)) {
                return @{
                    method = "dialog-title-relative-coordinate-click-runtime-marker"
                    beforeRect = $before
                    clicked = @($x, $y)
                    dismissed = $true
                    marker = $ExpectedDismissMarker
                }
            }
            $afterCoordinate = Wait-ForVisibleRuntimeWindowByTitle -Title $Title -TimeoutSeconds 1
            if (-not $afterCoordinate -or $afterCoordinate.Count -ne 4) {
                return @{
                    method = "dialog-title-relative-coordinate-click"
                    beforeRect = $before
                    clicked = @($x, $y)
                    dismissed = $true
                }
            }
            Start-Sleep -Milliseconds 120
        }
    }
    [CodexHumanClientWin32]::keybd_event(0x1B, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 100
    [CodexHumanClientWin32]::keybd_event(0x1B, 0, 2, [UIntPtr]::Zero)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ($ExpectedDismissMarker -and (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedDismissMarker -AfterLine $beforeLineCount -TimeoutSeconds 1)) {
            return @{
                method = "escape-key-runtime-marker"
                beforeRect = $before
                dismissed = $true
                marker = $ExpectedDismissMarker
            }
        }
        $after = Wait-ForVisibleRuntimeWindowByTitle -Title $Title -TimeoutSeconds 1
        if (-not $after -or $after.Count -ne 4) {
            return @{
                method = "escape-key"
                beforeRect = $before
                dismissed = $true
            }
        }
        Start-Sleep -Milliseconds 120
    }
    if ($before -and $before.Count -eq 4 -and $Title -in @("Create Custom Task", "Create Custom Group")) {
        $x = [int]($before[2] - 205)
        $y = [int]($before[1] + 342)
        [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
        Start-Sleep -Milliseconds 150
        [CodexHumanClientWin32]::SendLeftClick()
        $coordinateDeadline = (Get-Date).AddSeconds($TimeoutSeconds)
        while ((Get-Date) -lt $coordinateDeadline) {
            if ($ExpectedDismissMarker -and (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedDismissMarker -AfterLine $beforeLineCount -TimeoutSeconds 1)) {
                return @{
                    method = "dialog-title-relative-coordinate-click-runtime-marker"
                    beforeRect = $before
                    clicked = @($x, $y)
                    dismissed = $true
                    marker = $ExpectedDismissMarker
                }
            }
            $afterCoordinate = Wait-ForVisibleRuntimeWindowByTitle -Title $Title -TimeoutSeconds 1
            if (-not $afterCoordinate -or $afterCoordinate.Count -ne 4) {
                return @{
                    method = "dialog-title-relative-coordinate-click"
                    beforeRect = $before
                    clicked = @($x, $y)
                    dismissed = $true
                }
            }
            Start-Sleep -Milliseconds 120
        }
    }
    return @{
        method = "escape-key"
        beforeRect = $before
        dismissed = $false
    }
}

function Wait-ForRuntimeExit {
    param([int]$TimeoutSeconds = 8)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ((Find-ProcessesForLogRoot).Count -eq 0) {
            return $true
        }
        Start-Sleep -Milliseconds 200
    }

    return (Find-ProcessesForLogRoot).Count -eq 0
}

function Save-Manifest {
    param([string]$Status, [string]$Failure = "")
    $payload = [ordered]@{
        schema = "fam006-human-client-validation-v1"
        status = $Status
        failure = $Failure
        seam = "Workstream WS53 - Dashboard Resize Edge Discoverability Repair"
        startedAt = $script:StartedAt
        finishedAt = (Get-Date).ToUniversalTime().ToString("o")
        desktopShortcutPath = $DesktopShortcutPath
        logRoot = $LogRoot
        runtimeLog = $script:RuntimeLogPath
        formalUtsTouched = $false
        proofClasses = [ordered]@{
            staticProof = "supporting-only"
            sandboxProof = "supporting-only"
            appSideCallbackProof = "not-used-for-pass"
            fakeOffscreenModelProof = "not-used-for-pass"
            activeClientScreenshotProof = "supporting-only"
            liveHumanMouseTrayProof = $Status
            liveHumanMouseWindowProof = $Status
            videoProof = "not-available-ffmpeg-missing; screenshot-sequence-captured"
        }
        steps = $script:Steps
        artifacts = $script:Artifacts
        cleanupNotes = $script:CleanupNotes
    }
    $payload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $ManifestPath -Encoding utf8
    Copy-Item -LiteralPath $ManifestPath -Destination $LatestManifestPath -Force
}

$script:StartedAt = (Get-Date).ToUniversalTime().ToString("o")
$overallStatus = "PASS"
$failureMessage = ""

try {
    if (-not (Test-Path -LiteralPath $DesktopShortcutPath)) {
        throw "Desktop shortcut missing: $DesktopShortcutPath"
    }

    $env:NEXUS_HARNESS_LOG_ROOT = $LogRoot
    $env:NEXUS_HARNESS_DISABLE_DIAGNOSTICS = "1"
    $env:NEXUS_HARNESS_DISABLE_VOICE = "1"
    $env:NEXUS_HARNESS_SUPPRESS_ALREADY_RUNNING_DIALOGS = "1"
    $env:NEXUS_MONITORING_HUD_STARTUP_ENABLED = "0"
    $env:NEXUS_MONITORING_HUD_STATE_PATH = (Join-Path $LogRoot "monitoring_hud_state.json")
    $env:NEXUS_SHUTDOWN_CONFIRMATION_TIMEOUT_MS = "15000"

    Start-Process -FilePath $DesktopShortcutPath -WindowStyle Hidden
    Add-Step -Id "shortcut_launch_requested" -Title "Launch through desktop shortcut" -Status "PASS" -Detail "Started $DesktopShortcutPath"

    if (-not (Wait-ForRuntimeLog -TimeoutSeconds $StartupTimeoutSeconds)) {
        throw "Runtime log was not created under $LogRoot"
    }
    if (-not (Wait-ForRuntimeMarker -Marker "DESKTOP_OUTCOME|SETTLED|state=dormant" -TimeoutSeconds $StartupTimeoutSeconds)) {
        throw "Runtime did not settle through the desktop shortcut path"
    }
    $launchShot = Capture-VirtualScreenshot "01_after_shortcut_launch_settled"
    Add-Step -Id "launch_settled_visible_desktop" -Title "Shortcut launch settles with visible desktop context" -Status "PASS" -Detail "Runtime settled; screenshot captured." -Evidence @{ screenshot = $launchShot; runtimeLog = $script:RuntimeLogPath }

    Open-HiddenTrayOnNexus
    $initialMenuRect = Get-VisibleTrayMenuRect -TimeoutSeconds 5
    if (-not $initialMenuRect -or $initialMenuRect.Length -ne 4) {
        throw "Visible tray context menu was not opened from the real Nexus tray icon"
    }
    $menuShot = Capture-VirtualScreenshot "02_real_tray_menu_enable_visible"
    Send-Key 0x1B
    Add-Step -Id "launch_settled_tray_available" -Title "Real tray menu opens from the Nexus tray icon after shortcut launch" -Status "PASS" -Detail "Visible Nexus tray context menu opened from the real tray icon; menu rect=($($initialMenuRect -join ','))" -Evidence @{ screenshot = $menuShot; menuRect = @($initialMenuRect[0], $initialMenuRect[1], $initialMenuRect[2], $initialMenuRect[3]) }

    $enableEvidence = Invoke-TrayAction -ActionName "Enable HUD Feature" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_TOGGLE_REQUESTED|source=menu" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 1000
    $dashboard = Get-DashboardWindow
    $enabledShot = Capture-VirtualScreenshot "03_after_enable_hud_feature"
    if (-not $dashboard) {
        Add-Step -Id "enable_hud_opens_dashboard" -Title "Enable HUD Feature opens visible HUD Dashboard" -Status "FAIL" -Detail "Dashboard window was not visible after real tray Enable HUD Feature." -Evidence @{ screenshot = $enabledShot; trayClick = $enableEvidence }
        throw "Enable HUD Feature did not make the HUD Dashboard visible through the real tray path"
    }
    Add-Step -Id "enable_hud_opens_dashboard" -Title "Enable HUD Feature opens visible HUD Dashboard" -Status "PASS" -Detail "Dashboard window was visible after the real tray action." -Evidence @{ screenshot = $enabledShot; trayClick = $enableEvidence }
    if (Test-Path -LiteralPath $env:NEXUS_MONITORING_HUD_STATE_PATH) {
        $statePayload = Get-Content -LiteralPath $env:NEXUS_MONITORING_HUD_STATE_PATH -Raw | ConvertFrom-Json
        $statePersisted = [bool]$statePayload.featureEnabled
        Add-Step -Id "hud_feature_enabled_state_persisted" -Title "Enable HUD Feature writes durable feature state" -Status ($(if ($statePersisted) { "PASS" } else { "FAIL" })) -Detail "featureEnabled=$($statePayload.featureEnabled); dashboardVisible=$($statePayload.dashboardVisible)" -Evidence @{ statePath = $env:NEXUS_MONITORING_HUD_STATE_PATH }
        if (-not $statePersisted) { throw "Enable HUD Feature did not persist featureEnabled=true" }
    } else {
        Add-Step -Id "hud_feature_enabled_state_persisted" -Title "Enable HUD Feature writes durable feature state" -Status "FAIL" -Detail "State file missing: $env:NEXUS_MONITORING_HUD_STATE_PATH" -Evidence @{ statePath = $env:NEXUS_MONITORING_HUD_STATE_PATH }
        throw "Enable HUD Feature did not create a durable state file"
    }

    $earlyCloseEvidence = Invoke-TrayAction -ActionName "Close HUD Dashboard" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED|source=menu|visible=false" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 1000
    $earlyCloseShot = Capture-VirtualScreenshot "03b_after_close_hud_dashboard_before_move"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "close_dashboard_from_tray_before_move" -Title "Tray Close HUD Dashboard hides visible Dashboard before movement/resize" -Status ($(if (-not $dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after close before move: $([bool]$dashboard)" -Evidence @{ screenshot = $earlyCloseShot; trayClick = $earlyCloseEvidence }
    if ($dashboard) { throw "Close HUD Dashboard did not hide the visible Dashboard before movement/resize" }

    $earlyOpenEvidence = Invoke-TrayAction -ActionName "Open HUD Dashboard" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED|source=menu|visible=true" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 1000
    $earlyOpenShot = Capture-VirtualScreenshot "03c_after_open_hud_dashboard_before_move"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "open_dashboard_from_tray_before_move" -Title "Tray Open HUD Dashboard shows visible Dashboard before movement/resize" -Status ($(if ($dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after open before move: $([bool]$dashboard)" -Evidence @{ screenshot = $earlyOpenShot; trayClick = $earlyOpenEvidence }
    if (-not $dashboard) { throw "Open HUD Dashboard did not show the visible Dashboard before movement/resize" }

    $rectBeforeMove = $dashboard.Current.BoundingRectangle
    Drag-FromTo -StartX ([int]($rectBeforeMove.Left + ($rectBeforeMove.Width / 2))) -StartY ([int]($rectBeforeMove.Top + 48)) -EndX ([int]($rectBeforeMove.Left + ($rectBeforeMove.Width / 2) + 90)) -EndY ([int]($rectBeforeMove.Top + 88)) -Label "Dashboard header move"
    $dashboard = Get-DashboardWindow
    $moveShot = Capture-VirtualScreenshot "04_after_dashboard_mouse_drag"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_move" -Title "Dashboard moves through mouse drag" -Status "FAIL" -Detail "Dashboard disappeared after mouse drag." -Evidence @{ screenshot = $moveShot }
        throw "Dashboard disappeared after mouse drag"
    }
    $rectAfterMove = $dashboard.Current.BoundingRectangle
    $moved = ([Math]::Abs($rectAfterMove.Left - $rectBeforeMove.Left) -ge 12) -or ([Math]::Abs($rectAfterMove.Top - $rectBeforeMove.Top) -ge 12)
    Add-Step -Id "dashboard_mouse_move" -Title "Dashboard moves through mouse drag" -Status ($(if ($moved) { "PASS" } else { "FAIL" })) -Detail "before=($($rectBeforeMove.Left),$($rectBeforeMove.Top)); after=($($rectAfterMove.Left),$($rectAfterMove.Top))" -Evidence @{ screenshot = $moveShot }
    if (-not $moved) { throw "Dashboard did not move through human-like mouse drag" }

    $ncpOpenEvidence = Invoke-TrayAction -ActionName "Open Command Overlay" -ExpectedMarker "RENDERER_MAIN|TRAY_ACTIVATION_ROUTED_TO_OVERLAY|source=menu" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 900
    $ncpOpenShot = Capture-VirtualScreenshot "04b_after_open_ncp_with_dashboard_visible"
    Add-Step -Id "ncp_opens_with_dashboard_visible" -Title "Tray opens NCP while HUD Dashboard remains visible" -Status "PASS" -Detail "Open Command Overlay route completed while the Dashboard was visible and moved." -Evidence @{ screenshot = $ncpOpenShot; trayClick = $ncpOpenEvidence }

    Click-RuntimeButtonAndWaitForDialog -ButtonName "Create Custom Task" -DialogTitle "Create Custom Task" -StepId "ncp_create_custom_task_clickable_with_dashboard_open" -StepTitle "NCP Create Custom Task remains clickable with Dashboard open" -ExpectedOpenMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_START|action=create_custom_task" -DismissMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_RETURNED|action=create_custom_task"
    Click-RuntimeButtonAndWaitForDialog -ButtonName "Create Custom Group" -DialogTitle "Create Custom Group" -StepId "ncp_create_custom_group_clickable_with_dashboard_open" -StepTitle "NCP Create Custom Group remains clickable with Dashboard open" -ExpectedOpenMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_START|action=create_custom_group" -DismissMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_RETURNED|action=create_custom_group"
    Click-RuntimeButtonAndWaitForCloseableWindow -ButtonName "Manage Custom Tasks" -DialogTitle "Manage Custom Tasks" -StepId "ncp_manage_custom_tasks_clickable_with_dashboard_open" -StepTitle "NCP Manage Custom Tasks remains clickable with Dashboard open" -ExpectedOpenMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_START|action=manage_custom_tasks" -DismissMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_RETURNED|action=manage_custom_tasks"
    Click-RuntimeButtonAndWaitForCloseableWindow -ButtonName "Manage Custom Groups" -DialogTitle "Manage Custom Groups" -StepId "ncp_manage_custom_groups_clickable_with_dashboard_open" -StepTitle "NCP Manage Custom Groups remains clickable with Dashboard open" -ExpectedOpenMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_START|action=manage_custom_groups" -DismissMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_RETURNED|action=manage_custom_groups"

    $duplicateGuardEvidence = Invoke-TrayAction -ActionName "Create Custom Task" -ExpectedMarker "RENDERER_MAIN|TRAY_CREATE_CUSTOM_TASK_REQUESTED|source=menu" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 900
    $duplicateGuardShot = Capture-VirtualScreenshot "04c_after_tray_create_custom_task_dialog"
    $dialogOne = Wait-ForVisibleRuntimeWindowByTitle -Title "Create Custom Task" -TimeoutSeconds 5
    $secondCreateEvidence = Invoke-TrayAction -ActionName "Create Custom Task" -ExpectedMarker "RENDERER_MAIN|TRAY_CREATE_CUSTOM_TASK_ABORTED|source=menu|reason=authoring_dialog_active" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 650
    $duplicateGuardAfterShot = Capture-VirtualScreenshot "04d_after_duplicate_tray_create_custom_task_blocked"
    Add-Step -Id "tray_create_custom_task_duplicate_guard" -Title "Tray Create Custom Task cannot spawn infinite dialogs" -Status ($(if ($dialogOne -and $dialogOne.Count -eq 4) { "PASS" } else { "FAIL" })) -Detail "First tray Create Custom Task opened one dialog; second tray request was blocked while the dialog was active." -Evidence @{ screenshot = $duplicateGuardAfterShot; firstClick = $duplicateGuardEvidence; secondClick = $secondCreateEvidence; firstDialogRect = $dialogOne; firstDialogScreenshot = $duplicateGuardShot }
    if (-not $dialogOne -or $dialogOne.Count -ne 4) { throw "Tray Create Custom Task did not open a single visible dialog for duplicate guard proof" }
    try {
        $null = Click-VisibleRuntimeDialogButton -Title "Create Custom Task" -ButtonName "Cancel" -TimeoutSeconds 5
    } catch {
        $dismissDuplicate = Dismiss-VisibleRuntimeDialog -Title "Create Custom Task" -TimeoutSeconds 5 -ExpectedDismissMarker "RENDERER_MAIN|OVERLAY_ENTRY_DIALOG_EXEC_RETURNED|action=create_custom_task"
        if (-not $dismissDuplicate.dismissed) {
            throw
        }
    }
    Start-Sleep -Milliseconds 600

    $dashboard = Get-DashboardWindow
    if (-not $dashboard) { throw "Dashboard disappeared before resize proof after NCP interaction checks" }
    $rectBeforeResize = $dashboard.Current.BoundingRectangle
    $dashboardHandle = [long]$dashboard.Current.NativeWindowHandle
    if ($dashboardHandle -eq 0) {
        $dashboardHandle = Get-RootWindowHandleAtPoint -X ([int]($rectBeforeResize.Left + ($rectBeforeResize.Width * 0.50))) -Y ([int]($rectBeforeResize.Top + ($rectBeforeResize.Height * 0.50)))
    }
    $rightSampleY = [int]($rectBeforeResize.Top + ($rectBeforeResize.Height * 0.54))
    $bottomSampleX = [int]($rectBeforeResize.Left + ($rectBeforeResize.Width * 0.46))
    $rightOutsideX = [int]($rectBeforeResize.Right + 24)
    $rightEdgeX = [int]($rectBeforeResize.Right - 10)
    $rightInteriorX = [int]($rectBeforeResize.Right - 28)
    $bottomOutsideY = [int]($rectBeforeResize.Bottom + 24)
    $bottomEdgeY = [int]($rectBeforeResize.Bottom - 10)
    $bottomInteriorY = [int]($rectBeforeResize.Bottom - 28)
    $cornerOutsideX = [int]($rectBeforeResize.Right + 24)
    $cornerOutsideY = [int]($rectBeforeResize.Bottom + 24)
    $cornerEdgeX = [int]($rectBeforeResize.Right - 10)
    $cornerEdgeY = [int]($rectBeforeResize.Bottom - 10)
    $cursorRightOutside = Get-CursorKindAtPoint -X $rightOutsideX -Y $rightSampleY
    $hitRightOutside = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $rightOutsideX -Y $rightSampleY
    $cursorRight = Get-CursorKindAtPoint -X $rightEdgeX -Y $rightSampleY
    $hitRight = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $rightEdgeX -Y $rightSampleY
    $cursorBottomOutside = Get-CursorKindAtPoint -X $bottomSampleX -Y $bottomOutsideY
    $hitBottomOutside = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $bottomSampleX -Y $bottomOutsideY
    $cursorBottom = Get-CursorKindAtPoint -X $bottomSampleX -Y $bottomEdgeY
    $hitBottom = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $bottomSampleX -Y $bottomEdgeY
    $cursorCornerOutside = Get-CursorKindAtPoint -X $cornerOutsideX -Y $cornerOutsideY
    $hitCornerOutside = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $cornerOutsideX -Y $cornerOutsideY
    $cursorCorner = Get-CursorKindAtPoint -X $cornerEdgeX -Y $cornerEdgeY
    $hitCorner = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $cornerEdgeX -Y $cornerEdgeY
    $cursorRightInterior = Get-CursorKindAtPoint -X $rightInteriorX -Y $rightSampleY
    $hitRightInterior = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $rightInteriorX -Y $rightSampleY
    $cursorBottomInterior = Get-CursorKindAtPoint -X $bottomSampleX -Y $bottomInteriorY
    $hitBottomInterior = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $bottomSampleX -Y $bottomInteriorY
    $cursorRightOutsideAfter = Get-CursorKindAtPoint -X $rightOutsideX -Y $rightSampleY
    $hitRightOutsideAfter = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $rightOutsideX -Y $rightSampleY
    $cursorAlignmentPass = (
        $hitRight -eq "htright" -and
        $hitBottom -eq "htbottom" -and
        $hitCorner -eq "htbottomright" -and
        $hitRightOutside -ne "htright" -and
        $hitBottomOutside -ne "htbottom" -and
        $hitCornerOutside -ne "htbottomright" -and
        $hitRightInterior -ne "htright" -and
        $hitBottomInterior -ne "htbottom" -and
        $hitRightOutsideAfter -ne "htright" -and
        $cursorRight -ne $cursorRightOutside -and
        $cursorRight -ne $cursorRightInterior -and
        $cursorRight -ne $cursorRightOutsideAfter -and
        $cursorBottom -ne $cursorBottomOutside -and
        $cursorBottom -ne $cursorBottomInterior -and
        $cursorCorner -ne $cursorCornerOutside -and
        (Test-NonResizeCursorKind $cursorRightOutside) -and
        (Test-NonResizeCursorKind $cursorBottomOutside) -and
        (Test-NonResizeCursorKind $cursorCornerOutside) -and
        (Test-NonResizeCursorKind $cursorRightInterior) -and
        (Test-NonResizeCursorKind $cursorBottomInterior) -and
        (Test-NonResizeCursorKind $cursorRightOutsideAfter)
    )
    Add-Step -Id "dashboard_resize_cursor_alignment" -Title "Dashboard exposes Windows resize hit-tests only near the visible edge" -Status ($(if ($cursorAlignmentPass) { "PASS" } else { "FAIL" })) -Detail "cursor: rightOutside24px=$cursorRightOutside; rightEdge10px=$cursorRight; bottomOutside24px=$cursorBottomOutside; bottomEdge10px=$cursorBottom; cornerOutside24px=$cursorCornerOutside; corner10px=$cursorCorner; right28pxInside=$cursorRightInterior; bottom28pxInside=$cursorBottomInterior; rightOutsideAfter=$cursorRightOutsideAfter | hitTest: rightOutside24px=$hitRightOutside; rightEdge10px=$hitRight; bottomOutside24px=$hitBottomOutside; bottomEdge10px=$hitBottom; cornerOutside24px=$hitCornerOutside; corner10px=$hitCorner; right28pxInside=$hitRightInterior; bottom28pxInside=$hitBottomInterior; rightOutsideAfter=$hitRightOutsideAfter" -Evidence @{ rightEdgeOffsetPx = 10; bottomEdgeOffsetPx = 10; cornerOffsetPx = 10; interiorOffsetPx = 28; outsideOffsetPx = 24; expectedEdgeHitTests = "htright,htbottom,htbottomright"; expectedOutsideAndInteriorHitTests = "not edge"; cursorHandlePolicy = "edge cursor state must differ from outside/interior; WebEngine may report opaque cursor handles" }
    if (-not $cursorAlignmentPass) { throw "Dashboard resize cursor was not aligned to the visible edge/corner rail" }

    Drag-FromTo -StartX ([int]($rectBeforeResize.Right - 10)) -StartY ([int]($rectBeforeResize.Bottom - 10)) -EndX ([int]($rectBeforeResize.Right + 70)) -EndY ([int]($rectBeforeResize.Bottom + 60)) -Label "Dashboard cursor-aligned bottom-right resize rail"
    Start-Sleep -Milliseconds 450
    $dashboard = Get-DashboardWindow
    $resizeShot = Capture-VirtualScreenshot "05a_after_dashboard_corner_resize"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_resize_corner" -Title "Dashboard corner resize rail is easy to trigger" -Status "FAIL" -Detail "Dashboard disappeared after corner resize attempt." -Evidence @{ screenshot = $resizeShot }
        throw "Dashboard disappeared after resize attempt"
    }
    $rectAfterResize = $dashboard.Current.BoundingRectangle
    $cornerResized = ([Math]::Abs($rectAfterResize.Width - $rectBeforeResize.Width) -ge 20) -or ([Math]::Abs($rectAfterResize.Height - $rectBeforeResize.Height) -ge 20)
    Add-Step -Id "dashboard_mouse_resize_corner" -Title "Dashboard corner resize rail is cursor-aligned and triggers geometry resize" -Status ($(if ($cornerResized) { "PASS" } else { "FAIL" })) -Detail "before=($($rectBeforeResize.Width)x$($rectBeforeResize.Height)); after=($($rectAfterResize.Width)x$($rectAfterResize.Height)); start was 10px inside the visible corner rail" -Evidence @{ screenshot = $resizeShot }
    if (-not $cornerResized) { throw "Dashboard did not resize through the cursor-aligned corner rail" }

    $rectBeforeRightResize = $dashboard.Current.BoundingRectangle
    $rightStartY = [int]($rectBeforeRightResize.Top + ($rectBeforeRightResize.Height * 0.54))
    Drag-FromTo -StartX ([int]($rectBeforeRightResize.Right - 10)) -StartY $rightStartY -EndX ([int]($rectBeforeRightResize.Right + 66)) -EndY $rightStartY -Label "Dashboard cursor-aligned right-edge resize rail"
    Start-Sleep -Milliseconds 450
    $dashboard = Get-DashboardWindow
    $rightResizeShot = Capture-VirtualScreenshot "05b_after_dashboard_right_edge_resize"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_resize_right_edge" -Title "Dashboard right-edge resize rail is easy to trigger" -Status "FAIL" -Detail "Dashboard disappeared after right-edge resize attempt." -Evidence @{ screenshot = $rightResizeShot }
        throw "Dashboard disappeared after right-edge resize attempt"
    }
    $rectAfterRightResize = $dashboard.Current.BoundingRectangle
    $rightResized = [Math]::Abs($rectAfterRightResize.Width - $rectBeforeRightResize.Width) -ge 20
    Add-Step -Id "dashboard_mouse_resize_right_edge" -Title "Dashboard right-edge resize rail is cursor-aligned and triggers geometry resize" -Status ($(if ($rightResized) { "PASS" } else { "FAIL" })) -Detail "beforeWidth=$($rectBeforeRightResize.Width); afterWidth=$($rectAfterRightResize.Width); start was 10px inside the visible right-edge rail" -Evidence @{ screenshot = $rightResizeShot }
    if (-not $rightResized) { throw "Dashboard did not resize through the cursor-aligned right-edge rail" }

    $rectBeforeBottomResize = $dashboard.Current.BoundingRectangle
    $bottomStartX = [int]($rectBeforeBottomResize.Left + ($rectBeforeBottomResize.Width * 0.46))
    Drag-FromTo -StartX $bottomStartX -StartY ([int]($rectBeforeBottomResize.Bottom - 10)) -EndX $bottomStartX -EndY ([int]($rectBeforeBottomResize.Bottom + 66)) -Label "Dashboard cursor-aligned bottom-edge resize rail"
    Start-Sleep -Milliseconds 450
    $dashboard = Get-DashboardWindow
    $bottomResizeShot = Capture-VirtualScreenshot "05c_after_dashboard_bottom_edge_resize"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_resize_bottom_edge" -Title "Dashboard bottom-edge resize rail is easy to trigger" -Status "FAIL" -Detail "Dashboard disappeared after bottom-edge resize attempt." -Evidence @{ screenshot = $bottomResizeShot }
        throw "Dashboard disappeared after bottom-edge resize attempt"
    }
    $rectAfterBottomResize = $dashboard.Current.BoundingRectangle
    $bottomResized = [Math]::Abs($rectAfterBottomResize.Height - $rectBeforeBottomResize.Height) -ge 20
    Add-Step -Id "dashboard_mouse_resize_bottom_edge" -Title "Dashboard bottom-edge resize rail is cursor-aligned and triggers geometry resize" -Status ($(if ($bottomResized) { "PASS" } else { "FAIL" })) -Detail "beforeHeight=$($rectBeforeBottomResize.Height); afterHeight=$($rectAfterBottomResize.Height); start was 10px inside the visible bottom-edge rail" -Evidence @{ screenshot = $bottomResizeShot }
    if (-not $bottomResized) { throw "Dashboard did not resize through the cursor-aligned bottom-edge rail" }

    $resizeShot = Capture-VirtualScreenshot "05_after_dashboard_mouse_resize"
    Add-Step -Id "dashboard_mouse_resize" -Title "Dashboard resizes through cursor-aligned edge and corner rails" -Status "PASS" -Detail "Corner, right-edge, and bottom-edge resize rails changed real Dashboard geometry from the same user-visible cursor rail." -Evidence @{ screenshot = $resizeShot; cornerBefore = "$($rectBeforeResize.Width)x$($rectBeforeResize.Height)"; cornerAfter = "$($rectAfterResize.Width)x$($rectAfterResize.Height)"; rightBeforeWidth = $rectBeforeRightResize.Width; rightAfterWidth = $rectAfterRightResize.Width; bottomBeforeHeight = $rectBeforeBottomResize.Height; bottomAfterHeight = $rectAfterBottomResize.Height; cursorRight = $cursorRight; cursorBottom = $cursorBottom; cursorCorner = $cursorCorner; cursorRightInterior = $cursorRightInterior; cursorBottomInterior = $cursorBottomInterior }

    $closeEvidence = Invoke-TrayAction -ActionName "Close HUD Dashboard" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED|source=menu|visible=false" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 1000
    $closeShot = Capture-VirtualScreenshot "06_after_close_hud_dashboard"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "close_dashboard_from_tray" -Title "Tray Close HUD Dashboard hides visible Dashboard" -Status ($(if (-not $dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after close: $([bool]$dashboard)" -Evidence @{ screenshot = $closeShot; trayClick = $closeEvidence }
    if ($dashboard) { throw "Close HUD Dashboard did not hide the visible Dashboard" }

    $openEvidence = Invoke-TrayAction -ActionName "Open HUD Dashboard" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED|source=menu|visible=true" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 1000
    $openShot = Capture-VirtualScreenshot "07_after_open_hud_dashboard"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "open_dashboard_from_tray" -Title "Tray Open HUD Dashboard shows visible Dashboard" -Status ($(if ($dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after open: $([bool]$dashboard)" -Evidence @{ screenshot = $openShot; trayClick = $openEvidence }
    if (-not $dashboard) { throw "Open HUD Dashboard did not show the visible Dashboard" }

    $disableEvidence = Invoke-TrayAction -ActionName "Disable HUD Feature" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_TOGGLE_REQUESTED|source=menu" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 1000
    $disableShot = Capture-VirtualScreenshot "08_after_disable_hud_feature"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "disable_hud_recovers" -Title "Disable HUD Feature hides Dashboard and leaves app usable" -Status ($(if (-not $dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after disable: $([bool]$dashboard)" -Evidence @{ screenshot = $disableShot; trayClick = $disableEvidence }
    if ($dashboard) { throw "Disable HUD Feature did not hide the visible Dashboard" }

    $exitEvidence = Invoke-TrayAction -ActionName "Exit Nexus Desktop AI" -ExpectedMarker "RENDERER_MAIN|TRAY_SHUTDOWN_CONFIRMATION_REQUESTED|source=menu" -TimeoutSeconds $ActionTimeoutSeconds
    $dialogVisibleMarker = "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_DIALOG_VISIBLE|source=tray_menu"
    $dialogVisible = Wait-ForRuntimeMarker -Marker $dialogVisibleMarker -TimeoutSeconds 5
    $dialogRect = Wait-ForVisibleRuntimeWindowByTitle -Title "Confirm shutdown" -TimeoutSeconds 5
    $confirmShot = Capture-VirtualScreenshot "09_exit_confirmation_prompt"
    if (-not $dialogVisible -or -not $dialogRect -or $dialogRect.Count -ne 4) {
        Add-Step -Id "tray_exit_confirmation_visible" -Title "Tray Exit NDAI shows visible confirmation" -Status "FAIL" -Detail "Visible confirmation marker=$dialogVisible; visible window rect=($($dialogRect -join ','))" -Evidence @{ screenshot = $confirmShot; trayClick = $exitEvidence; expectedMarker = $dialogVisibleMarker }
        throw "Tray Exit NDAI did not show a detectable visible confirmation dialog"
    }
    Start-Sleep -Milliseconds 1200
    $confirmShot = Capture-VirtualScreenshot "09_exit_confirmation_prompt"
    Add-Step -Id "tray_exit_confirmation_visible" -Title "Tray Exit NDAI shows visible confirmation" -Status "PASS" -Detail "Visible confirmation marker emitted; top-level dialog rect=($($dialogRect -join ',')); prompt screenshot captured before timeout." -Evidence @{ screenshot = $confirmShot; trayClick = $exitEvidence; marker = $dialogVisibleMarker; dialogRect = $dialogRect }

    $noEvidence = Click-VisibleRuntimeDialogButton -Title "Confirm shutdown" -ButtonName "No" -TimeoutSeconds 5
    $cancelled = Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_CANCELLED|source=tray_menu" -TimeoutSeconds 3
    if (-not $cancelled) {
        $cancelled = Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_TIMEOUT|source=tray_menu" -TimeoutSeconds $ExitConfirmationTimeoutSeconds
    }
    $preserved = Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_SESSION_PRESERVED|source=tray_menu" -TimeoutSeconds 3
    $cancelShot = Capture-VirtualScreenshot "10_after_exit_confirmation_cancel"
    $stillHasRuntime = (Find-ProcessesForLogRoot).Count -gt 0
    $sessionPreserved = $cancelled -and $preserved -and $stillHasRuntime
    Add-Step -Id "tray_exit_cancel_preserves_session" -Title "Tray Exit cancel or timeout preserves session" -Status ($(if ($sessionPreserved) { "PASS" } else { "FAIL" })) -Detail "cancel_or_timeout_marker=$cancelled; preserved_marker=$preserved; runtime_process_still_present=$stillHasRuntime" -Evidence @{ screenshot = $cancelShot; buttonClick = $noEvidence }
    if (-not $sessionPreserved) { throw "Tray Exit cancel/timeout did not preserve the session" }

    $exitAcceptEvidence = Invoke-TrayAction -ActionName "Exit Nexus Desktop AI" -ExpectedMarker "RENDERER_MAIN|TRAY_SHUTDOWN_CONFIRMATION_REQUESTED|source=menu" -TimeoutSeconds $ActionTimeoutSeconds
    $acceptDialogVisible = Wait-ForRuntimeMarker -Marker $dialogVisibleMarker -TimeoutSeconds 5
    $acceptDialogRect = Wait-ForVisibleRuntimeWindowByTitle -Title "Confirm shutdown" -TimeoutSeconds 5
    $acceptPromptShot = Capture-VirtualScreenshot "11_exit_confirmation_accept_prompt"
    if (-not $acceptDialogVisible -or -not $acceptDialogRect -or $acceptDialogRect.Count -ne 4) {
        Add-Step -Id "tray_exit_accept_prompt_visible" -Title "Tray Exit accept path shows visible confirmation" -Status "FAIL" -Detail "Visible confirmation marker=$acceptDialogVisible; visible window rect=($($acceptDialogRect -join ','))" -Evidence @{ screenshot = $acceptPromptShot; trayClick = $exitAcceptEvidence; expectedMarker = $dialogVisibleMarker }
        throw "Tray Exit accept path did not show a detectable visible confirmation dialog"
    }
    Add-Step -Id "tray_exit_accept_prompt_visible" -Title "Tray Exit accept path shows visible confirmation" -Status "PASS" -Detail "Visible confirmation marker emitted; top-level dialog rect=($($acceptDialogRect -join ',')); prompt screenshot captured before accepting shutdown." -Evidence @{ screenshot = $acceptPromptShot; trayClick = $exitAcceptEvidence; marker = $dialogVisibleMarker; dialogRect = $acceptDialogRect }

    $yesEvidence = Click-VisibleRuntimeDialogButton -Title "Confirm shutdown" -ButtonName "Yes" -TimeoutSeconds 5
    $accepted = Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_ACCEPTED|source=tray_menu" -TimeoutSeconds 4
    $shutdownRequested = Wait-ForRuntimeMarker -Marker "RENDERER_MAIN|SHUTDOWN_REQUESTED" -TimeoutSeconds 4
    $runtimeExited = Wait-ForRuntimeExit -TimeoutSeconds 8
    $shutdownShot = Capture-VirtualScreenshot "12_after_exit_confirmation_accept"
    $shutdownAccepted = $accepted -and $shutdownRequested -and $runtimeExited
    Add-Step -Id "tray_exit_accept_shuts_down_promptly" -Title "Tray Exit Yes closes runtime promptly" -Status ($(if ($shutdownAccepted) { "PASS" } else { "FAIL" })) -Detail "accepted_marker=$accepted; shutdown_requested_marker=$shutdownRequested; runtime_exited=$runtimeExited" -Evidence @{ screenshot = $shutdownShot; buttonClick = $yesEvidence }
    if (-not $shutdownAccepted) { throw "Tray Exit Yes did not close the runtime promptly" }
}
catch {
    $overallStatus = "FAIL"
    $failureMessage = $_.Exception.Message
    Add-Step -Id "human_client_validation_failure" -Title "Human-client validation failure" -Status "FAIL" -Detail $failureMessage -ProofClass "live-human-ui"
}
finally {
    try {
        Capture-VirtualScreenshot "99_final_state" | Out-Null
    } catch {}
    if (-not $KeepRuntimeOpenOnFailure) {
        Cleanup-Runtime
    }
    Save-Manifest -Status $overallStatus -Failure $failureMessage
    if ($overallStatus -eq "PASS") {
        Write-Output "PASS: FAM-006 human-client validation passed. Manifest: $ManifestPath"
    }
    else {
        Write-Output "FAIL: FAM-006 human-client validation failed. Manifest: $ManifestPath"
    }
}

if ($overallStatus -eq "PASS") { exit 0 }
exit 1
