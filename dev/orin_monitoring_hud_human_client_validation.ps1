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
    [DllImport("user32.dll")] private static extern int GetMenuItemCount(IntPtr hMenu);
    [DllImport("user32.dll")] private static extern bool GetMenuItemRect(IntPtr hWnd, IntPtr hMenu, uint uItem, out RECT rect);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern int GetMenuStringW(IntPtr hMenu, uint uIDItem, StringBuilder lpString, int nMaxCount, uint uFlag);
    [DllImport("user32.dll")] private static extern uint GetMenuState(IntPtr hMenu, uint uId, uint uFlags);
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

    public static void SendAbsoluteRightClick(int x, int y) {
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
        inputs[1].mi.dwFlags = 0x0008;
        inputs[2].type = 0;
        inputs[2].mi.dwFlags = 0x0010;
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
            for (uint uid = 0; uid < 256; uid++) {
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

    public static string[] GetNativeMenuItemsForPopup(long hwndValue) {
        if (hwndValue == 0) { return new string[0]; }
        IntPtr hwnd = new IntPtr(hwndValue);
        IntPtr hMenu = SendMessage(hwnd, 0x01E1, IntPtr.Zero, IntPtr.Zero);
        if (hMenu == IntPtr.Zero) { return new string[0]; }
        int count = GetMenuItemCount(hMenu);
        if (count <= 0) { return new string[0]; }
        List<string> items = new List<string>();
        for (uint index = 0; index < (uint)count; index++) {
            StringBuilder text = new StringBuilder(256);
            GetMenuStringW(hMenu, index, text, text.Capacity, 0x00000400);
            RECT rect;
            if (!GetMenuItemRect(hwnd, hMenu, index, out rect)) {
                rect = new RECT();
            }
            uint state = GetMenuState(hMenu, index, 0x00000400);
            bool enabled = (state & 0x00000003) == 0;
            bool separator = (state & 0x00000800) != 0;
            items.Add(string.Format(
                "{0}|{1}|{2}|{3},{4},{5},{6}",
                index,
                enabled ? "enabled" : "disabled",
                separator ? "<separator>" : text.ToString().Replace("|", "/"),
                rect.Left,
                rect.Top,
                rect.Right,
                rect.Bottom
            ));
        }
        return items.ToArray();
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

    public static int[] GetWindowRectByHandle(long hwndValue) {
        if (hwndValue == 0) {
            return new int[0];
        }
        IntPtr hwnd = new IntPtr(hwndValue);
        RECT rect;
        if (GetWindowRect(hwnd, out rect) && rect.Right > rect.Left && rect.Bottom > rect.Top) {
            return new int[] { rect.Left, rect.Top, rect.Right, rect.Bottom };
        }
        return new int[0];
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
$DefaultDesktopShortcutPath = Join-Path $env:USERPROFILE "OneDrive\Desktop\FAM-006 RED - Nexus Desktop AI Launcher.lnk"
$DesktopShortcutPath = if ($env:NEXUS_DESKTOP_VALIDATION_SHORTCUT_PATH) {
    $env:NEXUS_DESKTOP_VALIDATION_SHORTCUT_PATH
} else {
    $DefaultDesktopShortcutPath
}

New-Item -ItemType Directory -Force -Path $ScreenshotRoot | Out-Null

$script:Steps = New-Object System.Collections.Generic.List[object]
$script:Artifacts = New-Object System.Collections.Generic.List[object]
$script:RuntimeProcessIds = New-Object System.Collections.Generic.List[int]
$script:RuntimeLogPath = ""
$script:CleanupNotes = New-Object System.Collections.Generic.List[string]
$script:ShortcutResolution = [ordered]@{
    path = $DesktopShortcutPath
    targetPath = ""
    workingDirectory = ""
    arguments = ""
    activeRoot = $RootDir
    status = "NOT_TESTED"
    detail = ""
}

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

function Resolve-ShortcutForActiveRoot {
    param([string]$ShortcutPath)

    $result = [ordered]@{
        path = $ShortcutPath
        targetPath = ""
        workingDirectory = ""
        arguments = ""
        activeRoot = $RootDir
        status = "FAIL"
        detail = ""
    }

    try {
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($ShortcutPath)
        $targetPath = [string]$shortcut.TargetPath
        $workingDirectory = [string]$shortcut.WorkingDirectory
        $arguments = [string]$shortcut.Arguments
        $result.targetPath = $targetPath
        $result.workingDirectory = $workingDirectory
        $result.arguments = $arguments

        $resolvedRoot = (Resolve-Path -LiteralPath $RootDir).Path.TrimEnd('\')
        $targetMatches = $false
        $workingDirectoryMatches = $false
        if (-not [string]::IsNullOrWhiteSpace($targetPath) -and (Test-Path -LiteralPath $targetPath)) {
            $resolvedTarget = (Resolve-Path -LiteralPath $targetPath).Path
            $targetMatches = $resolvedTarget.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)
        }
        if (-not [string]::IsNullOrWhiteSpace($workingDirectory) -and (Test-Path -LiteralPath $workingDirectory)) {
            $resolvedWorkingDirectory = (Resolve-Path -LiteralPath $workingDirectory).Path.TrimEnd('\')
            $workingDirectoryMatches = $resolvedWorkingDirectory.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)
        }

        if ($targetMatches -and $workingDirectoryMatches) {
            $result.status = "PASS"
            $result.detail = "Desktop shortcut target and working directory are rooted in the active FAM-006 worktree."
            return $result
        }

        $result.detail = "Desktop shortcut is not rooted in the active FAM-006 worktree; targetMatches=$targetMatches; workingDirectoryMatches=$workingDirectoryMatches."
        return $result
    } catch {
        $result.detail = "Unable to inspect desktop shortcut target: $($_.Exception.Message)"
        return $result
    }
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

function Send-AltF4 {
    [CodexHumanClientWin32]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [CodexHumanClientWin32]::keybd_event(0x73, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [CodexHumanClientWin32]::keybd_event(0x73, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [CodexHumanClientWin32]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 220
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
        [object]$Element,
        [string]$Label,
        [ValidateSet("left", "right")]
        [string]$Button = "left"
    )

    if (-not $Element) { throw "Missing element for $Label" }
    try {
        $walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
        $node = $Element
        $nativeHandle = 0
        while ($node) {
            $candidateHandle = [int]$node.Current.NativeWindowHandle
            if ($candidateHandle -ne 0) {
                $nativeHandle = $candidateHandle
            }
            $node = $walker.GetParent($node)
        }
        if ($nativeHandle -ne 0) {
            $windowHandle = [IntPtr]$nativeHandle
            [CodexHumanClientWin32]::BringWindowToTop($windowHandle) | Out-Null
            [CodexHumanClientWin32]::SetForegroundWindow($windowHandle) | Out-Null
            Start-Sleep -Milliseconds 220
        }
    } catch {}
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

function Find-VisibleRuntimeElementByNames {
    param(
        [string[]]$Names,
        [string]$ControlTypeName = "",
        [int]$TimeoutSeconds = 8
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        foreach ($name in @($Names)) {
            $element = Find-VisibleRuntimeElementByName -Name $name -ControlTypeName $ControlTypeName -TimeoutSeconds 1
            if ($element) {
                return [pscustomobject]@{
                    Element = $element
                    Name = $name
                }
            }
        }
        Start-Sleep -Milliseconds 120
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

function Get-NativeWindowRectByHandle {
    param([long]$WindowHandle)
    if ($WindowHandle -eq 0) { return $null }
    $rect = [CodexHumanClientWin32]::GetWindowRectByHandle($WindowHandle)
    if (-not $rect -or $rect.Count -ne 4) { return $null }
    return [pscustomobject]@{
        Left = [int]$rect[0]
        Top = [int]$rect[1]
        Right = [int]$rect[2]
        Bottom = [int]$rect[3]
        Width = [int]($rect[2] - $rect[0])
        Height = [int]($rect[3] - $rect[1])
    }
}

function Format-ColorSample {
    param([object]$Sample)
    if (-not $Sample) { return "missing" }
    return "($($Sample.x),$($Sample.y))=rgb($($Sample.r),$($Sample.g),$($Sample.b))/brightness=$($Sample.brightness)"
}

function Invoke-DashboardRoundedCornerMaskProbe {
    param(
        [object]$Dashboard,
        [long]$WindowHandle
    )
    if (-not $Dashboard) { throw "Dashboard is missing for rounded-corner mask proof" }
    if ($WindowHandle -eq 0) {
        $bounds = $Dashboard.Current.BoundingRectangle
        $WindowHandle = Get-RootWindowHandleAtPoint -X ([int]($bounds.Left + ($bounds.Width / 2))) -Y ([int]($bounds.Top + ($bounds.Height / 2)))
    }
    $probePath = Join-Path $RootDir "dev\orin_dashboard_rounded_corner_mask_probe.py"
    if (-not (Test-Path -LiteralPath $probePath)) {
        throw "Rounded-corner mask probe is missing: $probePath"
    }
    $probeRoot = Join-Path $LogRoot "rounded_corner_mask"
    New-Item -ItemType Directory -Force -Path $probeRoot | Out-Null
    $probeOutput = & python $probePath --window-handle $WindowHandle --output-dir $probeRoot 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Rounded-corner mask probe failed: $($probeOutput -join "`n")"
    }
    $payload = ($probeOutput -join "`n") | ConvertFrom-Json
    if ($payload.screenshot) {
        Add-Artifact -Label "dashboard_rounded_corner_mask_light_backdrop" -Path ([string]$payload.screenshot)
    }
    return $payload
}

function Drag-FromToWithGeometrySamples {
    param(
        [object]$Element,
        [int]$StartX,
        [int]$StartY,
        [int]$EndX,
        [int]$EndY,
        [string]$Label,
        [long]$WindowHandle = 0,
        [int]$Steps = 28,
        [int]$StepDelayMs = 16
    )
    $samples = @()
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    [CodexHumanClientWin32]::SetCursorPos($StartX, $StartY) | Out-Null
    Start-Sleep -Milliseconds 120
    [CodexHumanClientWin32]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    for ($i = 1; $i -le $Steps; $i++) {
        $x = [int]($StartX + (($EndX - $StartX) * $i / $Steps))
        $y = [int]($StartY + (($EndY - $StartY) * $i / $Steps))
        [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
        Start-Sleep -Milliseconds $StepDelayMs
        $rect = if ($WindowHandle -ne 0) { Get-NativeWindowRectByHandle -WindowHandle $WindowHandle } else { $null }
        if (-not $rect) {
            $currentElement = Get-DashboardWindow
            if ($currentElement) {
                $rect = $currentElement.Current.BoundingRectangle
            } else {
                $rect = $Element.Current.BoundingRectangle
            }
        }
        $samples += [pscustomobject]@{
            Step = $i
            X = $x
            Y = $y
            ElapsedMs = [Math]::Round($stopwatch.Elapsed.TotalMilliseconds, 1)
            Left = [int]$rect.Left
            Top = [int]$rect.Top
            Right = [int]$rect.Right
            Bottom = [int]$rect.Bottom
            Width = [int]$rect.Width
            Height = [int]$rect.Height
        }
    }
    [CodexHumanClientWin32]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 350
    return $samples
}

function Drag-FromToWithGeometryAndVisualSamples {
    param(
        [object]$Element,
        [int]$StartX,
        [int]$StartY,
        [int]$EndX,
        [int]$EndY,
        [string]$Label,
        [long]$WindowHandle = 0,
        [int]$Steps = 42,
        [int]$StepDelayMs = 8,
        [int[]]$CaptureSteps = @(8, 16, 24, 32, 40)
    )
    $samples = @()
    $frames = @()
    $captureStepSet = @{}
    foreach ($step in @($CaptureSteps)) { $captureStepSet[[int]$step] = $true }
    $safeLabel = $Label -replace "[^A-Za-z0-9_-]", "_"
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    [CodexHumanClientWin32]::SetCursorPos($StartX, $StartY) | Out-Null
    Start-Sleep -Milliseconds 120
    [CodexHumanClientWin32]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    for ($i = 1; $i -le $Steps; $i++) {
        $x = [int]($StartX + (($EndX - $StartX) * $i / $Steps))
        $y = [int]($StartY + (($EndY - $StartY) * $i / $Steps))
        [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
        Start-Sleep -Milliseconds $StepDelayMs
        $rect = if ($WindowHandle -ne 0) { Get-NativeWindowRectByHandle -WindowHandle $WindowHandle } else { $null }
        if (-not $rect) {
            $currentElement = Get-DashboardWindow
            if ($currentElement) {
                $rect = $currentElement.Current.BoundingRectangle
            } else {
                $rect = $Element.Current.BoundingRectangle
            }
        }
        $sample = [pscustomobject]@{
            Step = $i
            X = $x
            Y = $y
            ElapsedMs = [Math]::Round($stopwatch.Elapsed.TotalMilliseconds, 1)
            Left = [int]$rect.Left
            Top = [int]$rect.Top
            Right = [int]$rect.Right
            Bottom = [int]$rect.Bottom
            Width = [int]$rect.Width
            Height = [int]$rect.Height
        }
        $samples += $sample
        if ($captureStepSet.ContainsKey([int]$i)) {
            $shot = Capture-VirtualScreenshot ("during_drag_{0}_{1:00}" -f $safeLabel, $i)
            $frames += [ordered]@{
                index = $i
                elapsedMs = $sample.ElapsedMs
                dashboardVisible = $true
                dashboardRect = @($sample.Left, $sample.Top, $sample.Right, $sample.Bottom)
                screenshot = $shot
            }
        }
    }
    [CodexHumanClientWin32]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 350
    return [pscustomobject]@{
        Samples = $samples
        Frames = $frames
        MouseHeldUntilFramesCaptured = $true
        Method = "SetCursorPos plus mouse_event held left button with screenshot captures before release"
    }
}

function Test-DashboardDuringDragVisualProof {
    param(
        [object[]]$Samples,
        [object[]]$Frames,
        [string]$Mode
    )
    $uniqueSizes = @($Samples | ForEach-Object { "$($_.Width)x$($_.Height)" } | Sort-Object -Unique).Count
    $visibleFrames = @($Frames | Where-Object { $_.dashboardVisible -and $_.dashboardRect -and $_.dashboardRect.Count -eq 4 -and $_.screenshot })
    $signatures = @()
    if ($visibleFrames.Count -ge 3) {
        $referenceRect = $visibleFrames[-1].dashboardRect
        $signatures = @($visibleFrames | ForEach-Object { Get-DashboardFrameSignature -Frame $_ -ReferenceRect $referenceRect })
        $signatures = @($signatures | Where-Object { $_ -and $_.samples -and $_.samples.Count -gt 0 })
    }
    $signatureDeltaCount = 0
    $maxMeanDelta = 0.0
    for ($i = 1; $i -lt $signatures.Count; $i++) {
        $previous = $signatures[$i - 1].samples
        $current = $signatures[$i].samples
        $count = [Math]::Min($previous.Count, $current.Count)
        $total = 0.0
        for ($j = 0; $j -lt $count; $j++) {
            $total += [Math]::Abs([double]$current[$j] - [double]$previous[$j])
        }
        $mean = if ($count -gt 0) { $total / $count } else { 0.0 }
        $maxMeanDelta = [Math]::Max($maxMeanDelta, $mean)
        if ($mean -gt 0.45) { $signatureDeltaCount += 1 }
    }
    $pass = $uniqueSizes -ge 8 -and $visibleFrames.Count -ge 4 -and $signatures.Count -ge 4 -and $signatureDeltaCount -ge 2
    return [pscustomobject]@{
        Mode = $Mode
        Pass = [bool]$pass
        UniqueGeometrySizes = [int]$uniqueSizes
        VisibleFrameCount = [int]$visibleFrames.Count
        SignatureCount = [int]$signatures.Count
        SignatureDeltaCount = [int]$signatureDeltaCount
        MaxMeanDelta = [Math]::Round($maxMeanDelta, 2)
        MouseHeldUntilFramesCaptured = $true
        Expectation = "during-drag visual/frame proof must show geometry and pixel-signature updates before mouse release for grow and shrink"
    }
}

function Measure-ResizeTracking {
    param(
        [object[]]$Samples,
        [double]$BaseWidth,
        [double]$BaseHeight,
        [double]$StartX,
        [double]$StartY,
        [string]$Mode
    )
    $lagSamples = @()
    $maxLag = 0.0
    $sumLag = 0.0
    $count = 0
    $maxInterval = 0.0
    $previousElapsed = $null
    foreach ($sample in @($Samples)) {
        $expectedWidth = $BaseWidth
        $expectedHeight = $BaseHeight
        if ($Mode -eq "right" -or $Mode -eq "corner") {
            $expectedWidth = $BaseWidth + ([double]$sample.X - $StartX)
        }
        if ($Mode -eq "bottom" -or $Mode -eq "corner") {
            $expectedHeight = $BaseHeight + ([double]$sample.Y - $StartY)
        }
        $widthLag = if ($Mode -eq "right" -or $Mode -eq "corner") { [Math]::Abs(([double]$sample.Width) - $expectedWidth) } else { 0.0 }
        $heightLag = if ($Mode -eq "bottom" -or $Mode -eq "corner") { [Math]::Abs(([double]$sample.Height) - $expectedHeight) } else { 0.0 }
        $lag = [Math]::Max($widthLag, $heightLag)
        $maxLag = [Math]::Max($maxLag, $lag)
        $sumLag += $lag
        $count += 1
        if ($null -ne $previousElapsed -and $null -ne $sample.ElapsedMs) {
            $maxInterval = [Math]::Max($maxInterval, [Math]::Abs(([double]$sample.ElapsedMs) - $previousElapsed))
        }
        if ($null -ne $sample.ElapsedMs) {
            $previousElapsed = [double]$sample.ElapsedMs
        }
        $lagSamples += [pscustomobject]@{
            Step = $sample.Step
            ElapsedMs = $sample.ElapsedMs
            X = $sample.X
            Y = $sample.Y
            Width = $sample.Width
            Height = $sample.Height
            ExpectedWidth = [Math]::Round($expectedWidth, 1)
            ExpectedHeight = [Math]::Round($expectedHeight, 1)
            LagPx = [Math]::Round($lag, 1)
        }
    }
    $averageLag = if ($count -gt 0) { $sumLag / $count } else { 999.0 }
    $pass = $count -ge 36 -and $maxLag -le 16.0 -and $averageLag -le 8.0 -and $maxInterval -le 34.0
    return [pscustomobject]@{
        Mode = $Mode
        Pass = [bool]$pass
        SampleCount = $count
        MaxLagPx = [Math]::Round($maxLag, 1)
        AverageLagPx = [Math]::Round($averageLag, 1)
        MaxSampleIntervalMs = [Math]::Round($maxInterval, 1)
        MaxAllowedLagPx = 16
        MaxAllowedAverageLagPx = 8
        MaxAllowedSampleIntervalMs = 34
        Samples = $lagSamples
    }
}

function Measure-MoveTracking {
    param(
        [object[]]$Samples,
        [double]$BaseLeft,
        [double]$BaseTop,
        [double]$StartX,
        [double]$StartY
    )
    $lagSamples = @()
    $maxLag = 0.0
    $sumLag = 0.0
    $count = 0
    $maxInterval = 0.0
    $previousElapsed = $null
    foreach ($sample in @($Samples)) {
        $expectedLeft = $BaseLeft + ([double]$sample.X - $StartX)
        $expectedTop = $BaseTop + ([double]$sample.Y - $StartY)
        $leftLag = [Math]::Abs(([double]$sample.Left) - $expectedLeft)
        $topLag = [Math]::Abs(([double]$sample.Top) - $expectedTop)
        $lag = [Math]::Max($leftLag, $topLag)
        $maxLag = [Math]::Max($maxLag, $lag)
        $sumLag += $lag
        $count += 1
        if ($null -ne $previousElapsed -and $null -ne $sample.ElapsedMs) {
            $maxInterval = [Math]::Max($maxInterval, [Math]::Abs(([double]$sample.ElapsedMs) - $previousElapsed))
        }
        if ($null -ne $sample.ElapsedMs) {
            $previousElapsed = [double]$sample.ElapsedMs
        }
        $lagSamples += [pscustomobject]@{
            Step = $sample.Step
            ElapsedMs = $sample.ElapsedMs
            X = $sample.X
            Y = $sample.Y
            Left = $sample.Left
            Top = $sample.Top
            ExpectedLeft = [Math]::Round($expectedLeft, 1)
            ExpectedTop = [Math]::Round($expectedTop, 1)
            LagPx = [Math]::Round($lag, 1)
        }
    }
    $averageLag = if ($count -gt 0) { $sumLag / $count } else { 999.0 }
    $pass = $count -ge 42 -and $maxLag -le 24.0 -and $averageLag -le 12.0 -and $maxInterval -le 34.0
    return [pscustomobject]@{
        Pass = [bool]$pass
        SampleCount = $count
        MaxLagPx = [Math]::Round($maxLag, 1)
        AverageLagPx = [Math]::Round($averageLag, 1)
        MaxSampleIntervalMs = [Math]::Round($maxInterval, 1)
        MaxAllowedLagPx = 24
        MaxAllowedAverageLagPx = 12
        MaxAllowedSampleIntervalMs = 34
        Samples = $lagSamples
    }
}

function Move-DashboardAwayFromTrayMenuIfNeeded {
    param([object]$Dashboard)
    if (-not $Dashboard) { return }
    $rect = $Dashboard.Current.BoundingRectangle
    $virtual = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $trayZoneLeft = [double]($virtual.Right - 380)
    $trayZoneTop = [double]($virtual.Bottom - 220)
    $overlapsTrayZone = ([double]$rect.Right -gt $trayZoneLeft) -and ([double]$rect.Bottom -gt $trayZoneTop)
    if (-not $overlapsTrayZone) {
        Add-Step -Id "dashboard_clear_of_tray_menu_before_cleanup" -Title "Dashboard does not cover the tray menu cleanup zone" -Status "PASS" -Detail "Dashboard rect=($([int]$rect.Left),$([int]$rect.Top),$([int]$rect.Right),$([int]$rect.Bottom)); trayZone=($([int]$trayZoneLeft),$([int]$trayZoneTop),$($virtual.Right),$($virtual.Bottom))." -Evidence @{ dashboardRect = @([int]$rect.Left, [int]$rect.Top, [int]$rect.Right, [int]$rect.Bottom); trayZone = @([int]$trayZoneLeft, [int]$trayZoneTop, [int]$virtual.Right, [int]$virtual.Bottom) }
        return
    }
    $targetLeft = [Math]::Max([double]($virtual.Left + 40), [double]$rect.Left - [Math]::Min(900.0, [Math]::Max(420.0, [double]$rect.Width * 0.75)))
    $deltaX = [int]($targetLeft - [double]$rect.Left)
    $startX = [int]($rect.Left + ($rect.Width / 2))
    $startY = [int]($rect.Top + 48)
    $handle = [long]$Dashboard.Current.NativeWindowHandle
    $samples = Drag-FromToWithGeometrySamples -Element $Dashboard -WindowHandle $handle -StartX $startX -StartY $startY -EndX ([int]($startX + $deltaX)) -EndY $startY -Label "Dashboard move away from tray menu cleanup zone" -Steps 42 -StepDelayMs 8
    Start-Sleep -Milliseconds 350
    $afterDashboard = Get-DashboardWindow
    $shot = Capture-VirtualScreenshot "05d_after_dashboard_repositioned_clear_of_tray_menu"
    if (-not $afterDashboard) {
        Add-Step -Id "dashboard_repositioned_clear_of_tray_menu_for_cleanup" -Title "Dashboard is repositioned away from tray menu before cleanup actions" -Status "FAIL" -Detail "Dashboard disappeared while repositioning away from tray menu cleanup zone." -Evidence @{ screenshot = $shot; moveSamples = $samples }
        throw "Dashboard disappeared while repositioning away from tray menu cleanup zone"
    }
    $afterRect = $afterDashboard.Current.BoundingRectangle
    $clear = ([double]$afterRect.Right -le $trayZoneLeft) -or ([double]$afterRect.Bottom -le $trayZoneTop)
    Add-Step -Id "dashboard_repositioned_clear_of_tray_menu_for_cleanup" -Title "Dashboard is repositioned away from tray menu before cleanup actions" -Status ($(if ($clear) { "PASS" } else { "FAIL" })) -Detail "before=($([int]$rect.Left),$([int]$rect.Top),$([int]$rect.Right),$([int]$rect.Bottom)); after=($([int]$afterRect.Left),$([int]$afterRect.Top),$([int]$afterRect.Right),$([int]$afterRect.Bottom)); trayZone=($([int]$trayZoneLeft),$([int]$trayZoneTop),$($virtual.Right),$($virtual.Bottom))." -Evidence @{ screenshot = $shot; before = @([int]$rect.Left, [int]$rect.Top, [int]$rect.Right, [int]$rect.Bottom); after = @([int]$afterRect.Left, [int]$afterRect.Top, [int]$afterRect.Right, [int]$afterRect.Bottom); moveSamples = $samples }
    if (-not $clear) { throw "Dashboard still covers the tray menu cleanup zone after repositioning" }
}

function Get-CursorKindAtPoint {
    param([int]$X, [int]$Y)
    [CodexHumanClientWin32]::SetCursorPos($X, $Y) | Out-Null
    [CodexHumanClientWin32]::mouse_event(0x0001, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 120
    return [CodexHumanClientWin32]::GetCursorKind()
}

function Get-NativeHitTestKindAtPoint {
    param([long]$WindowHandle, [int]$X, [int]$Y)
    return [CodexHumanClientWin32]::GetNativeHitTestKind($WindowHandle, $X, $Y)
}

function Find-ResizeCursorTransition {
    param(
        [long]$WindowHandle,
        [int]$StartX,
        [int]$StartY,
        [int]$EndX,
        [int]$EndY,
        [string]$ExpectedHit,
        [string]$Label,
        [int]$Steps = 24
    )
    for ($i = 0; $i -le $Steps; $i++) {
        $x = [int]($StartX + (($EndX - $StartX) * $i / [Math]::Max(1, $Steps)))
        $y = [int]($StartY + (($EndY - $StartY) * $i / [Math]::Max(1, $Steps)))
        $cursor = Get-CursorKindAtPoint -X $x -Y $y
        $hit = Get-NativeHitTestKindAtPoint -WindowHandle $WindowHandle -X $x -Y $y
        if ((Test-ResizeCursorKind $cursor) -and $hit -eq $ExpectedHit) {
            return [pscustomobject]@{
                Found = $true
                X = $x
                Y = $y
                Cursor = $cursor
                HitTest = $hit
                Step = $i
                Label = $Label
            }
        }
    }
    return [pscustomobject]@{
        Found = $false
        X = $EndX
        Y = $EndY
        Cursor = "not-found"
        HitTest = "not-found"
        Step = -1
        Label = $Label
    }
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

function Click-ScreenPoint {
    param([int]$X, [int]$Y, [string]$Label)
    $before = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($X, $Y)
    [CodexHumanClientWin32]::SetCursorPos($X, $Y) | Out-Null
    Start-Sleep -Milliseconds 120
    [CodexHumanClientWin32]::SendAbsoluteLeftClick($X, $Y)
    Start-Sleep -Milliseconds 480
    $after = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($X, $Y)
    return [ordered]@{
        label = $Label
        clicked = @($X, $Y)
        windowAtPointBeforeClick = $before
        windowAtPointAfterClick = $after
        method = "SetCursorPos + SendInput absolute left click"
    }
}

function DoubleClick-ScreenPoint {
    param([int]$X, [int]$Y, [string]$Label)
    $before = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($X, $Y)
    [CodexHumanClientWin32]::SetCursorPos($X, $Y) | Out-Null
    Start-Sleep -Milliseconds 120
    [CodexHumanClientWin32]::SendAbsoluteLeftClick($X, $Y)
    Start-Sleep -Milliseconds 120
    [CodexHumanClientWin32]::SendAbsoluteLeftClick($X, $Y)
    Start-Sleep -Milliseconds 520
    $after = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($X, $Y)
    return [ordered]@{
        label = $Label
        clicked = @($X, $Y)
        windowAtPointBeforeClick = $before
        windowAtPointAfterClick = $after
        method = "SetCursorPos + two SendInput absolute left clicks"
    }
}

function Convert-RuntimeMarkerLineToMap {
    param([string]$Line)
    $result = @{}
    foreach ($part in ($Line -split "\|")) {
        $index = $part.IndexOf("=")
        if ($index -le 0) { continue }
        $key = $part.Substring(0, $index).Trim()
        $value = $part.Substring($index + 1).Trim()
        if ($key) { $result[$key] = $value }
    }
    return $result
}

function Get-LatestSettingsWindowRectFromRuntimeLog {
    $lines = @(Read-RuntimeLines)
    for ($i = $lines.Count - 1; $i -ge 0; $i--) {
        $line = [string]$lines[$i]
        if ($line -notmatch "MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY") { continue }
        if ($line -notmatch "dashboard_settings_open=true") { continue }
        if ($line -notmatch "settings_window_present=true") { continue }
        $map = Convert-RuntimeMarkerLineToMap -Line $line
        try {
            $left = [int]$map["settings_window_left"]
            $top = [int]$map["settings_window_top"]
            $right = [int]$map["settings_window_right"]
            $bottom = [int]$map["settings_window_bottom"]
            if ($right -le $left -or $bottom -le $top) { return $null }
            return [pscustomobject]@{
                Left = $left
                Top = $top
                Right = $right
                Bottom = $bottom
                Width = [int]($right - $left)
                Height = [int]($bottom - $top)
                sourceLine = $line
            }
        } catch {
            return $null
        }
    }
    return $null
}

function Get-DashboardTopChromeControlPoints {
    param([object]$Dashboard)
    if (-not $Dashboard) { throw "Dashboard is missing while calculating Dashboard control points" }
    $rect = $Dashboard.Current.BoundingRectangle
    $headerHeight = [Math]::Min(170, [int]$rect.Height)
    $actionsWidth = [Math]::Min(360, [Math]::Max(154, [int]($rect.Width / 3)))
    $actionsLeft = [int]$rect.Left + 43
    $actionsTop = [int]$rect.Top + 132
    $closeLeft = [int]$rect.Right - 14 - 82
    $closeTop = [int]$rect.Top + 12
    return [ordered]@{
        headerRect = @([int]$rect.Left, [int]$rect.Top, [int]$rect.Right, [int]($rect.Top + $headerHeight))
        actionsRect = @($actionsLeft, $actionsTop, [int]($actionsLeft + $actionsWidth), [int]($actionsTop + 44))
        closePoint = @([int]($closeLeft + 41), [int]($closeTop + 21))
        settingsPoint = @([int]($actionsLeft + [Math]::Min(77, $actionsWidth / 2)), [int]($actionsTop + 22))
    }
}

function Get-SettingsChildWindowControlPoints {
    param([object]$Dashboard)
    if (-not $Dashboard) { throw "Dashboard is missing while calculating settings child-window control points" }
    $runtimeRect = Get-LatestSettingsWindowRectFromRuntimeLog
    if ($runtimeRect) {
        return [ordered]@{
            estimatedRect = @($runtimeRect.Left, $runtimeRect.Top, $runtimeRect.Right, $runtimeRect.Bottom)
            closePoint = @([int]($runtimeRect.Right - 42), [int]($runtimeRect.Top + 30))
            donePoint = @([int]($runtimeRect.Left + 42), [int]($runtimeRect.Bottom - 32))
            source = "runtime-child-window-marker"
            sourceLine = $runtimeRect.sourceLine
        }
    }
    $rect = $Dashboard.Current.BoundingRectangle
    $childWidth = [Math]::Min(520, [Math]::Max(320, [int]$rect.Width - 44))
    $childHeight = [Math]::Min(620, [Math]::Max(360, [int]$rect.Height - 44))
    $left = [int]($rect.Left + (($rect.Width - $childWidth) / 2))
    $top = [int]($rect.Top + (($rect.Height - $childHeight) / 2))
    return [ordered]@{
        estimatedRect = @($left, $top, [int]($left + $childWidth), [int]($top + $childHeight))
        closePoint = @([int]($left + $childWidth - 42), [int]($top + 30))
        donePoint = @([int]($left + 42), [int]($top + $childHeight - 32))
    }
}

function Capture-DashboardTimedSequence {
    param(
        [string]$LabelPrefix,
        [int]$FrameCount = 8,
        [int]$IntervalMs = 140
    )
    $frames = @()
    for ($i = 0; $i -lt $FrameCount; $i++) {
        $dashboard = Get-DashboardWindow
        $rectPayload = $null
        if ($dashboard) {
            $rect = $dashboard.Current.BoundingRectangle
            $rectPayload = @([int]$rect.Left, [int]$rect.Top, [int]$rect.Right, [int]$rect.Bottom)
        }
        $shot = Capture-VirtualScreenshot ("{0}_{1:00}" -f $LabelPrefix, $i)
        $frames += [ordered]@{
            index = $i
            elapsedMs = $i * $IntervalMs
            dashboardVisible = [bool]$dashboard
            dashboardRect = $rectPayload
            screenshot = $shot
        }
        Start-Sleep -Milliseconds $IntervalMs
    }
    return $frames
}

function Test-DashboardSequenceGeometryStable {
    param([object[]]$Frames, [int]$MaxDeltaPx = 10)
    $visibleFrames = @($Frames | Where-Object { $_.dashboardVisible -and $_.dashboardRect -and $_.dashboardRect.Count -eq 4 })
    if ($visibleFrames.Count -ne $Frames.Count) { return $false }
    $lefts = @($visibleFrames | ForEach-Object { [int]$_.dashboardRect[0] })
    $tops = @($visibleFrames | ForEach-Object { [int]$_.dashboardRect[1] })
    $widths = @($visibleFrames | ForEach-Object { [int]$_.dashboardRect[2] - [int]$_.dashboardRect[0] })
    $heights = @($visibleFrames | ForEach-Object { [int]$_.dashboardRect[3] - [int]$_.dashboardRect[1] })
    $maxDelta = @(
        (($lefts | Measure-Object -Maximum).Maximum - ($lefts | Measure-Object -Minimum).Minimum),
        (($tops | Measure-Object -Maximum).Maximum - ($tops | Measure-Object -Minimum).Minimum),
        (($widths | Measure-Object -Maximum).Maximum - ($widths | Measure-Object -Minimum).Minimum),
        (($heights | Measure-Object -Maximum).Maximum - ($heights | Measure-Object -Minimum).Minimum)
    ) | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum
    return [int]$maxDelta -le $MaxDeltaPx
}

function Get-DashboardFrameSignature {
    param([object]$Frame, [object]$ReferenceRect, [int]$GridSize = 18)
    if (-not $Frame -or -not $Frame.screenshot -or -not (Test-Path -LiteralPath $Frame.screenshot)) {
        return $null
    }
    if (-not $ReferenceRect -or $ReferenceRect.Count -ne 4) {
        return $null
    }
    $bitmap = [System.Drawing.Bitmap]::FromFile([string]$Frame.screenshot)
    try {
        $left = [Math]::Max(0, [int]$ReferenceRect[0])
        $top = [Math]::Max(0, [int]$ReferenceRect[1])
        $right = [Math]::Min($bitmap.Width - 1, [int]$ReferenceRect[2])
        $bottom = [Math]::Min($bitmap.Height - 1, [int]$ReferenceRect[3])
        if ($right -le $left -or $bottom -le $top) { return $null }
        $marginX = [Math]::Max(8, [int](($right - $left) * 0.04))
        $marginY = [Math]::Max(8, [int](($bottom - $top) * 0.04))
        $sampleLeft = [Math]::Min($right, $left + $marginX)
        $sampleTop = [Math]::Min($bottom, $top + $marginY)
        $sampleRight = [Math]::Max($sampleLeft, $right - $marginX)
        $sampleBottom = [Math]::Max($sampleTop, $bottom - $marginY)
        $samples = New-Object System.Collections.Generic.List[double]
        for ($gy = 0; $gy -lt $GridSize; $gy++) {
            for ($gx = 0; $gx -lt $GridSize; $gx++) {
                $x = [int]($sampleLeft + (($sampleRight - $sampleLeft) * (($gx + 0.5) / $GridSize)))
                $y = [int]($sampleTop + (($sampleBottom - $sampleTop) * (($gy + 0.5) / $GridSize)))
                $color = $bitmap.GetPixel($x, $y)
                $samples.Add(([double]$color.R + [double]$color.G + [double]$color.B) / 3.0)
            }
        }
        return [pscustomobject]@{
            index = [int]$Frame.index
            screenshot = [string]$Frame.screenshot
            samples = $samples.ToArray()
        }
    }
    finally {
        $bitmap.Dispose()
    }
}

function Test-DashboardSequenceVisualContinuity {
    param(
        [object[]]$Frames,
        [double]$LargeTransitionThreshold = 24.0,
        [double]$SettledDeltaThreshold = 15.0
    )
    $visibleFrames = @($Frames | Where-Object { $_.dashboardVisible -and $_.dashboardRect -and $_.dashboardRect.Count -eq 4 })
    if ($visibleFrames.Count -lt 4) {
        return [pscustomobject]@{
            Pass = $false
            Reason = "fewer than four visible dashboard frames"
            LargeTransitionCount = 0
            MaxMeanDelta = 0
            Deltas = @()
        }
    }
    $referenceRect = $visibleFrames[-1].dashboardRect
    $signatures = @($visibleFrames | ForEach-Object { Get-DashboardFrameSignature -Frame $_ -ReferenceRect $referenceRect })
    $signatures = @($signatures | Where-Object { $_ -and $_.samples -and $_.samples.Count -gt 0 })
    if ($signatures.Count -lt 4) {
        return [pscustomobject]@{
            Pass = $false
            Reason = "screenshot signatures unavailable"
            LargeTransitionCount = 0
            MaxMeanDelta = 0
            Deltas = @()
        }
    }
    $deltas = @()
    for ($i = 1; $i -lt $signatures.Count; $i++) {
        $previous = $signatures[$i - 1].samples
        $current = $signatures[$i].samples
        $count = [Math]::Min($previous.Count, $current.Count)
        $total = 0.0
        for ($j = 0; $j -lt $count; $j++) {
            $total += [Math]::Abs([double]$current[$j] - [double]$previous[$j])
        }
        $mean = if ($count -gt 0) { $total / $count } else { 999.0 }
        $deltas += [pscustomobject]@{
            from = [int]$signatures[$i - 1].index
            to = [int]$signatures[$i].index
            meanLumaDelta = [Math]::Round($mean, 2)
        }
    }
    $largeTransitions = @($deltas | Where-Object { [double]$_.meanLumaDelta -gt $LargeTransitionThreshold })
    $settledDeltas = if ($deltas.Count -gt 2) { @($deltas | Select-Object -Last ([Math]::Min(3, $deltas.Count))) } else { @($deltas) }
    $maxMeanDelta = if ($deltas.Count -gt 0) { ($deltas | Measure-Object -Property meanLumaDelta -Maximum).Maximum } else { 0 }
    $maxSettledDelta = if ($settledDeltas.Count -gt 0) { ($settledDeltas | Measure-Object -Property meanLumaDelta -Maximum).Maximum } else { 0 }
    $pass = $largeTransitions.Count -le 1 -and [double]$maxSettledDelta -le $SettledDeltaThreshold
    return [pscustomobject]@{
        Pass = [bool]$pass
        Reason = if ($pass) { "no repeated visible flicker transitions after initial appearance" } else { "visible dashboard frames changed too much after first appearance" }
        LargeTransitionCount = [int]$largeTransitions.Count
        MaxMeanDelta = [Math]::Round([double]$maxMeanDelta, 2)
        MaxSettledDelta = [Math]::Round([double]$maxSettledDelta, 2)
        Deltas = $deltas
    }
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
    $deadline = (Get-Date).AddSeconds(8)
    while ((Get-Date) -lt $deadline) {
        $runtimeProcesses = Find-ProcessesForLogRoot
        foreach ($process in $runtimeProcesses) {
            $rect = [CodexHumanClientWin32]::GetNotifyIconRectForProcess([int]$process.ProcessId)
            if ($rect -and $rect.Length -eq 4) {
                $x = [int](($rect[0] + $rect[2]) / 2)
                $y = [int](($rect[1] + $rect[3]) / 2)
                for ($attempt = 1; $attempt -le 3; $attempt++) {
                    [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
                    Start-Sleep -Milliseconds 220
                    [CodexHumanClientWin32]::SendAbsoluteRightClick($x, $y)
                    Start-Sleep -Milliseconds 750
                    $menuRect = Get-VisibleTrayMenuRect -TimeoutSeconds 1
                    if ($menuRect -and $menuRect.Length -eq 4) {
                        return @{
                            processId = [int]$process.ProcessId
                            notifyIconRect = @([int]$rect[0], [int]$rect[1], [int]$rect[2], [int]$rect[3])
                            clicked = @($x, $y)
                            attempt = $attempt
                            menuRect = @([int]$menuRect[0], [int]$menuRect[1], [int]$menuRect[2], [int]$menuRect[3])
                            clickMethod = "Shell_NotifyIconGetRect + absolute right click"
                        }
                    }
                }
            }
        }
        Start-Sleep -Milliseconds 300
    }

    $runtimeProcesses = Find-ProcessesForLogRoot
    throw "Nexus tray icon rectangle not found for runtime process IDs: $($runtimeProcesses.ProcessId -join ', ')"
}

function Click-NexusTrayIcon {
    param([string]$Label = "Nexus tray icon")

    $deadline = (Get-Date).AddSeconds(8)
    while ((Get-Date) -lt $deadline) {
        $runtimeProcesses = Find-ProcessesForLogRoot
        foreach ($process in $runtimeProcesses) {
            $rect = [CodexHumanClientWin32]::GetNotifyIconRectForProcess([int]$process.ProcessId)
            if ($rect -and $rect.Length -eq 4) {
                $x = [int](($rect[0] + $rect[2]) / 2)
                $y = [int](($rect[1] + $rect[3]) / 2)
                [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
                Start-Sleep -Milliseconds 220
                [CodexHumanClientWin32]::SendLeftClick()
                Start-Sleep -Milliseconds 350
                return @{
                    label = $Label
                    processId = [int]$process.ProcessId
                    notifyIconRect = @([int]$rect[0], [int]$rect[1], [int]$rect[2], [int]$rect[3])
                    clicked = @($x, $y)
                    clickMethod = "Shell_NotifyIconGetRect + SetCursorPos + left click"
                }
            }
        }
        Start-Sleep -Milliseconds 300
    }

    $runtimeProcesses = Find-ProcessesForLogRoot
    throw "Nexus tray icon rectangle not found for runtime process IDs: $($runtimeProcesses.ProcessId -join ', ')"
}

function Invoke-TrayIconActivation {
    param([string]$ExpectedMarker = "", [int]$TimeoutSeconds = 8, [string]$Label = "Nexus tray icon activation")

    $beforeCount = 0
    if ($ExpectedMarker) {
        $beforeCount = ((Read-RuntimeLines) | Select-String -Pattern ([regex]::Escape($ExpectedMarker))).Count
    }
    $clickEvidence = Click-NexusTrayIcon -Label $Label
    if ($ExpectedMarker) {
        $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
        while ((Get-Date) -lt $deadline) {
            $count = ((Read-RuntimeLines) | Select-String -Pattern ([regex]::Escape($ExpectedMarker))).Count
            if ($count -gt $beforeCount) { return $clickEvidence }
            Start-Sleep -Milliseconds 250
        }
        $afterTimeoutShot = Capture-VirtualScreenshot ("tray_icon_after_timeout_{0}" -f ($Label -replace "[^A-Za-z0-9_-]", "_"))
        throw "Tray icon activation '$Label' did not emit expected marker '$ExpectedMarker'; clicked=($($clickEvidence.clicked -join ',')); after_timeout_screenshot=$afterTimeoutShot"
    }
    return $clickEvidence
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

    $trayOpenEvidence = Open-HiddenTrayOnNexus
    $menuHandle = Get-VisibleTrayMenuHandle -TimeoutSeconds 1
    $menuElement = $null
    $coordinateOnlyMenu = $false
    if ($menuHandle -ne [IntPtr]::Zero) {
        $menuElement = [System.Windows.Automation.AutomationElement]::FromHandle($menuHandle)
    }
    if (-not $menuElement -and $trayOpenEvidence.menuRect) {
        $coordinateOnlyMenu = $true
        $menuRectPayload = @($trayOpenEvidence.menuRect)
        $menuRect = [pscustomobject]@{
            X = [double]$menuRectPayload[0]
            Y = [double]$menuRectPayload[1]
            Width = [double]($menuRectPayload[2] - $menuRectPayload[0])
            Height = [double]($menuRectPayload[3] - $menuRectPayload[1])
        }
    } elseif (-not $menuElement) {
        throw "Visible Nexus tray context menu did not appear for action '$ActionName'"
    }

    if (-not $itemRect -and -not $coordinateOnlyMenu) {
        $menuRect = $menuElement.Current.BoundingRectangle
        if ($trayOpenEvidence.menuRect) {
            $openedMenuRect = @($trayOpenEvidence.menuRect)
            $openedLeft = [double]$openedMenuRect[0]
            $openedTop = [double]$openedMenuRect[1]
            $openedRight = [double]$openedMenuRect[2]
            $openedBottom = [double]$openedMenuRect[3]
            $openedCenterX = ($openedLeft + $openedRight) / 2
            $openedCenterY = ($openedTop + $openedBottom) / 2
            $candidateCenterX = [double]($menuRect.X + ($menuRect.Width / 2))
            $candidateCenterY = [double]($menuRect.Y + ($menuRect.Height / 2))
            $sameTrayPopup = (
                [Math]::Abs($candidateCenterX - $openedCenterX) -le 12 -and
                [Math]::Abs($candidateCenterY - $openedCenterY) -le 12
            )
            if (-not $sameTrayPopup) {
                $coordinateOnlyMenu = $true
                $menuHandle = [IntPtr]::Zero
                $menuElement = $null
                $menuRect = [pscustomobject]@{
                    X = $openedLeft
                    Y = $openedTop
                    Width = [double]($openedRight - $openedLeft)
                    Height = [double]($openedBottom - $openedTop)
                }
                $items = @()
            }
        }
    }
    if (-not $itemRect -and -not $coordinateOnlyMenu) {
        $items = $menuElement.FindAll(
            [System.Windows.Automation.TreeScope]::Subtree,
            [System.Windows.Automation.Condition]::TrueCondition
        )
    } else {
        $items = @()
    }
    $target = $null
    $targetControlType = ""
    $itemRect = $null
    $nativeMenuItems = @()
    if ($menuHandle -ne [IntPtr]::Zero) {
        try {
            $nativeMenuItems = @([CodexHumanClientWin32]::GetNativeMenuItemsForPopup($menuHandle.ToInt64()))
        } catch {
            $nativeMenuItems = @()
        }
        foreach ($nativeItem in $nativeMenuItems) {
            $parts = ([string]$nativeItem).Split("|", 4)
            if ($parts.Count -ne 4) { continue }
            $enabled = $parts[1] -eq "enabled"
            $text = $parts[2]
            $rectParts = $parts[3].Split(",")
            if (-not $enabled -or $text -ne $ActionName -or $rectParts.Count -ne 4) { continue }
            $left = [int]$rectParts[0]
            $top = [int]$rectParts[1]
            $right = [int]$rectParts[2]
            $bottom = [int]$rectParts[3]
            if ($right -gt $left -and $bottom -gt $top) {
                $itemRect = [pscustomobject]@{
                    X = [double]$left
                    Y = [double]$top
                    Width = [double]($right - $left)
                    Height = [double]($bottom - $top)
                }
                $targetControlType = "ControlType.NativeMenuItemRect"
                $coordinateFallback = $true
                break
            }
        }
    }
    if (-not $coordinateOnlyMenu) {
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
    }
    $coordinateFallback = $coordinateOnlyMenu
    if ($itemRect -and -not $target) {
        $coordinateFallback = $true
    }
    if (-not $target -and -not $itemRect) {
        $nativeY = $null
        if ($ActionName -in @("Enable HUD Feature", "Disable HUD Feature")) {
            $nativeY = [int]($menuRect.Y + 17)
        } elseif ($ActionName -in @("Close HUD Dashboard", "Open HUD Dashboard")) {
            $nativeY = [int]($menuRect.Y + 39)
        } elseif ($ActionName -eq "HUD Overlay Deferred") {
            $nativeY = [int]($menuRect.Y + 61)
        } elseif ($ActionName -in @("Open Command Overlay", "Close Command Overlay")) {
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

    if ($coordinateFallback -or $targetControlType -eq "ControlType.Button" -or $targetControlType -like "ControlType.NativeMenu*") {
        $x = [int]($itemRect.X + ($itemRect.Width / 2))
    } else {
        $x = [int]($itemRect.X + [Math]::Min(42, [Math]::Max(16, $itemRect.Width / 3)))
    }
    $y = [int]($itemRect.Y + ($itemRect.Height / 2))

    $menuShot = Capture-VirtualScreenshot ("tray_menu_before_{0}" -f ($ActionName -replace "[^A-Za-z0-9_-]", "_"))
    [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 450
    $windowAtPointBeforeClick = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($x, $y)
    [CodexHumanClientWin32]::SendAbsoluteLeftClick($x, $y)
    Start-Sleep -Milliseconds 220
    $windowAtPointAfterClick = [CodexHumanClientWin32]::GetWindowSummaryAtPoint($x, $y)
    $activationMethod = "desktop-shortcut + real-tray-popup + SetCursorPos + absolute left mouse click on visible tray command center"
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
        trayOpenEvidence = $trayOpenEvidence
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

function Close-CommandOverlayBeforeDashboardResize {
    $indicatorBefore = Find-VisibleRuntimeElementByName -Name "O.R.I.N. Command Prompt" -TimeoutSeconds 1
    $beforeLines = (Read-RuntimeLines).Count
    $closeMarker = $false
    $trayCloseEvidence = $null
    if ($indicatorBefore) {
        $trayCloseEvidence = Invoke-TrayIconActivation -ExpectedMarker "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED" -TimeoutSeconds 5 -Label "NCP tray icon left-click close before Dashboard resize"
        $closeMarker = $true
    }
    Start-Sleep -Milliseconds 500
    $indicatorAfter = Find-VisibleRuntimeElementByName -Name "O.R.I.N. Command Prompt" -TimeoutSeconds 1
    $dashboard = Get-DashboardWindow
    $shot = Capture-VirtualScreenshot "04e_after_command_overlay_closed_before_dashboard_resize"
    $pass = (-not $indicatorAfter) -and [bool]$dashboard
    Add-Step -Id "ncp_tray_icon_left_click_closes" -Title "NCP tray icon left-click closes the Command Overlay" -Status ($(if ($pass) { "PASS" } else { "FAIL" })) -Detail "overlay_visible_before=$([bool]$indicatorBefore); close_marker=$closeMarker; overlay_visible_after=$([bool]$indicatorAfter); dashboard_visible=$([bool]$dashboard)." -Evidence @{ screenshot = $shot; trayIconClick = $trayCloseEvidence; expectedClosedMarker = "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED" }
    Add-Step -Id "ncp_closed_before_dashboard_resize" -Title "Command Overlay is closed before Dashboard resize proof" -Status ($(if ($pass) { "PASS" } else { "FAIL" })) -Detail "overlay_visible_before=$([bool]$indicatorBefore); close_marker=$closeMarker; overlay_visible_after=$([bool]$indicatorAfter); dashboard_visible=$([bool]$dashboard)." -Evidence @{ screenshot = $shot; expectedClosedMarker = "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED"; trayIconClick = $trayCloseEvidence }
    if (-not $pass) {
        throw "Command Overlay remained visible or Dashboard disappeared before resize proof"
    }
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
        if ($lastDialogRect.Count -eq 4) {
            $runtimeButtons = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
                [System.Windows.Automation.TreeScope]::Descendants,
                (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button))
            )
            $bestButton = $null
            $bestButtonRect = $null
            $bestCenterY = -2147483648
            for ($j = 0; $j -lt $runtimeButtons.Count; $j++) {
                $button = $runtimeButtons.Item($j)
                try {
                    if (
                        $button.Current.Name -ne $ButtonName -or
                        -not $button.Current.IsEnabled -or
                        $runtimeIds -notcontains [int]$button.Current.ProcessId
                    ) {
                        continue
                    }
                    $rect = $button.Current.BoundingRectangle
                    if ($rect.IsEmpty -or $rect.Width -le 0 -or $rect.Height -le 0 -or $button.Current.IsOffscreen) {
                        continue
                    }
                    $centerX = [int]($rect.X + ($rect.Width / 2))
                    $centerY = [int]($rect.Y + ($rect.Height / 2))
                    if (
                        $centerX -lt $lastDialogRect[0] -or
                        $centerX -gt $lastDialogRect[2] -or
                        $centerY -lt $lastDialogRect[1] -or
                        $centerY -gt ($lastDialogRect[1] + 1100)
                    ) {
                        continue
                    }
                    if (-not $bestButton -or $centerY -gt $bestCenterY) {
                        $bestButton = $button
                        $bestButtonRect = $rect
                        $bestCenterY = $centerY
                    }
                } catch {}
            }
            if ($bestButton) {
                $x = [int]($bestButtonRect.X + ($bestButtonRect.Width / 2))
                $y = [int]($bestButtonRect.Y + ($bestButtonRect.Height / 2))
                [CodexHumanClientWin32]::SetCursorPos($x, $y) | Out-Null
                Start-Sleep -Milliseconds 150
                [CodexHumanClientWin32]::SendLeftClick()
                return @{
                    button = $ButtonName
                    clicked = @($x, $y)
                    buttonRect = @(
                        [int]$bestButtonRect.X,
                        [int]$bestButtonRect.Y,
                        [int]($bestButtonRect.X + $bestButtonRect.Width),
                        [int]($bestButtonRect.Y + $bestButtonRect.Height)
                    )
                    fallback = "runtime-wide-dialog-button"
                    dialogRect = $lastDialogRect
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
    $preferredButtons = @()
    if ($Title -in @("Create Custom Task", "Create Custom Group")) {
        $preferredButtons = @("Cancel")
    } elseif ($Title -in @("Manage Custom Tasks", "Manage Custom Groups")) {
        $preferredButtons = @("Close", "Cancel")
    }
    foreach ($preferredButton in $preferredButtons) {
        try {
            $clickEvidence = Click-VisibleRuntimeDialogButton -Title $Title -ButtonName $preferredButton -TimeoutSeconds 2
            $buttonDeadline = (Get-Date).AddSeconds($TimeoutSeconds)
            while ((Get-Date) -lt $buttonDeadline) {
                if ($ExpectedDismissMarker -and (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedDismissMarker -AfterLine $beforeLineCount -TimeoutSeconds 1)) {
                    return @{
                        method = "visible-runtime-button-runtime-marker"
                        beforeRect = $before
                        clicked = $clickEvidence.clicked
                        button = $preferredButton
                        dismissed = $true
                        marker = $ExpectedDismissMarker
                    }
                }
                $afterButton = Wait-ForVisibleRuntimeWindowByTitle -Title $Title -TimeoutSeconds 1
                if (-not $afterButton -or $afterButton.Count -ne 4) {
                    return @{
                        method = "visible-runtime-button"
                        beforeRect = $before
                        clicked = $clickEvidence.clicked
                        button = $preferredButton
                        dismissed = $true
                    }
                }
                Start-Sleep -Milliseconds 120
            }
        } catch {}
    }
    if ($before -and $before.Count -eq 4 -and $Title -in @("Create Custom Task", "Create Custom Group", "Manage Custom Tasks", "Manage Custom Groups")) {
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
    if ($before -and $before.Count -eq 4 -and $Title -in @("Create Custom Task", "Create Custom Group", "Manage Custom Tasks", "Manage Custom Groups")) {
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
    if ($before -and $before.Count -eq 4 -and $Title -in @("Create Custom Task", "Create Custom Group", "Manage Custom Tasks", "Manage Custom Groups")) {
        $focusX = [int](($before[0] + $before[2]) / 2)
        $focusY = [int](($before[1] + $before[3]) / 2)
        [CodexHumanClientWin32]::SetCursorPos($focusX, $focusY) | Out-Null
        Start-Sleep -Milliseconds 120
        [CodexHumanClientWin32]::SendLeftClick()
        Start-Sleep -Milliseconds 160
        Send-AltF4
        $altF4Deadline = (Get-Date).AddSeconds($TimeoutSeconds)
        while ((Get-Date) -lt $altF4Deadline) {
            if ($ExpectedDismissMarker -and (Wait-ForRuntimeMarkerAfterLine -Marker $ExpectedDismissMarker -AfterLine $beforeLineCount -TimeoutSeconds 1)) {
                return @{
                    method = "dialog-focus-alt-f4-runtime-marker"
                    beforeRect = $before
                    clicked = @($focusX, $focusY)
                    dismissed = $true
                    marker = $ExpectedDismissMarker
                }
            }
            $afterAltF4 = Wait-ForVisibleRuntimeWindowByTitle -Title $Title -TimeoutSeconds 1
            if (-not $afterAltF4 -or $afterAltF4.Count -ne 4) {
                return @{
                    method = "dialog-focus-alt-f4"
                    beforeRect = $before
                    clicked = @($focusX, $focusY)
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
        seam = "FAM-006 human-client Dashboard/tray/resize validation"
        startedAt = $script:StartedAt
        finishedAt = (Get-Date).ToUniversalTime().ToString("o")
        desktopShortcutPath = $DesktopShortcutPath
        logRoot = $LogRoot
        runtimeLog = $script:RuntimeLogPath
        formalUtsTouched = $false
        shortcutResolution = $script:ShortcutResolution
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

    $script:ShortcutResolution = Resolve-ShortcutForActiveRoot -ShortcutPath $DesktopShortcutPath
    Add-Step -Id "shortcut_targets_active_worktree" -Title "Desktop shortcut targets the active FAM-006 worktree" -Status $script:ShortcutResolution.status -Detail $script:ShortcutResolution.detail -Evidence @{
        shortcutPath = $script:ShortcutResolution.path
        targetPath = $script:ShortcutResolution.targetPath
        workingDirectory = $script:ShortcutResolution.workingDirectory
        activeRoot = $script:ShortcutResolution.activeRoot
        arguments = $script:ShortcutResolution.arguments
    }
    if ($script:ShortcutResolution.status -ne "PASS") {
        throw $script:ShortcutResolution.detail
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

    $initialTrayOpenEvidence = Open-HiddenTrayOnNexus
    $initialMenuRect = @($initialTrayOpenEvidence.menuRect)
    if (-not $initialMenuRect -or $initialMenuRect.Length -ne 4) {
        $initialMenuRect = Get-VisibleTrayMenuRect -TimeoutSeconds 5
    }
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

    $firstOpenStartLine = (Read-RuntimeLines).Count
    $earlyOpenEvidence = Invoke-TrayAction -ActionName "Open HUD Dashboard" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED|source=menu|visible=true" -TimeoutSeconds $ActionTimeoutSeconds
    $firstOpenFrames = @(Capture-DashboardTimedSequence -LabelPrefix "03c_first_open_stability" -FrameCount 11 -IntervalMs 110)
    $firstOpenShowGuardReleased = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_VISIBLE_SHOW_GUARD_RELEASED" -AfterLine $firstOpenStartLine -TimeoutSeconds 2
    $firstOpenStable = Test-DashboardSequenceGeometryStable -Frames $firstOpenFrames -MaxDeltaPx 10
    $firstOpenVisual = Test-DashboardSequenceVisualContinuity -Frames $firstOpenFrames
    $firstOpenPass = $firstOpenStable -and $firstOpenShowGuardReleased -and $firstOpenVisual.Pass
    Add-Step -Id "dashboard_first_open_stability_sequence" -Title "Dashboard first-open shortcut path stays visually and geometrically stable" -Status ($(if ($firstOpenPass) { "PASS" } else { "FAIL" })) -Detail "Captured $($firstOpenFrames.Count) full-desktop frames at 110ms cadence after real tray Open HUD Dashboard; show_guard_released=$firstOpenShowGuardReleased; geometry_stable=$firstOpenStable; visual_continuity=$($firstOpenVisual.Pass); large_visual_transitions=$($firstOpenVisual.LargeTransitionCount); max_visual_delta=$($firstOpenVisual.MaxMeanDelta); max_settled_delta=$($firstOpenVisual.MaxSettledDelta)." -Evidence @{ frames = $firstOpenFrames; visualContinuity = $firstOpenVisual; maxAllowedGeometryDeltaPx = 10; expectedMarker = "MONITORING_HUD_VISIBLE_SHOW_GUARD_RELEASED"; visualContinuityPolicy = "initial appearance may transition once; repeated visible flicker or late settled-frame shifts fail" }
    if (-not $firstOpenPass) { throw "Dashboard first-open sequence did not meet visual and geometry stability proof through the real shortcut/tray path" }
    $earlyOpenShot = Capture-VirtualScreenshot "03c_after_open_hud_dashboard_before_move"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "open_dashboard_from_tray_before_move" -Title "Tray Open HUD Dashboard shows visible Dashboard before movement/resize" -Status ($(if ($dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after open before move: $([bool]$dashboard)" -Evidence @{ screenshot = $earlyOpenShot; trayClick = $earlyOpenEvidence }
    if (-not $dashboard) { throw "Open HUD Dashboard did not show the visible Dashboard before movement/resize" }

    $dashboardHandleForControls = [long]$dashboard.Current.NativeWindowHandle
    $chromePoints = Get-DashboardTopChromeControlPoints -Dashboard $dashboard
    $settingsPoint = @($chromePoints.settingsPoint)
    $settingsPointSource = "heuristic-dashboard-ia-card-actions"
    $settingsElementMatch = Find-VisibleRuntimeElementByNames -Names @("Open HUD Dashboard settings", "Settings") -ControlTypeName "ControlType.Button" -TimeoutSeconds 2
    $settingsElementRect = @()
    if ($settingsElementMatch -and $settingsElementMatch.Element) {
        try {
            $rect = $settingsElementMatch.Element.Current.BoundingRectangle
            if (-not $rect.IsEmpty -and $rect.Width -gt 0 -and $rect.Height -gt 0) {
                $settingsPoint = @([int]($rect.X + ($rect.Width / 2)), [int]($rect.Y + ($rect.Height / 2)))
                $settingsElementRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
                $settingsPointSource = "uia-visible-runtime-button:$($settingsElementMatch.Name)"
            }
        } catch {}
    }
    $settingsHit = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandleForControls -X ([int]$settingsPoint[0]) -Y ([int]$settingsPoint[1])
    $settingsBeforeLine = (Read-RuntimeLines).Count
    $settingsClickEvidence = Click-ScreenPoint -X ([int]$settingsPoint[0]) -Y ([int]$settingsPoint[1]) -Label "Dashboard Settings IA-card button"
    $settingsNativeMarker = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_DASHBOARD_SETTINGS_NATIVE_CONTROL_READY" -AfterLine $settingsBeforeLine -TimeoutSeconds 4
    $settingsChildMarker = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY" -AfterLine $settingsBeforeLine -TimeoutSeconds 4
    $settingsShot = Capture-VirtualScreenshot "03d_after_dashboard_settings_real_mouse_click"
    $dashboardAfterSettings = Get-DashboardWindow
    $settingsPass = $settingsChildMarker -and $dashboardAfterSettings -and ($settingsHit -eq "htclient")
    Add-Step -Id "dashboard_settings_opens_with_real_mouse" -Title "Dashboard Settings opens through real mouse control hit-test path" -Status ($(if ($settingsPass) { "PASS" } else { "FAIL" })) -Detail "settingsPoint=($($settingsPoint -join ',')); source=$settingsPointSource; hitTest=$settingsHit; native_marker=$settingsNativeMarker; child_window_marker=$settingsChildMarker; dashboard_visible_after_click=$([bool]$dashboardAfterSettings)." -Evidence @{ screenshot = $settingsShot; click = $settingsClickEvidence; controlPoints = $chromePoints; settingsElementRect = $settingsElementRect; pointSource = $settingsPointSource; hitTest = $settingsHit; expectedMarkers = @("MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY"); optionalMarkers = @("MONITORING_HUD_DASHBOARD_SETTINGS_NATIVE_CONTROL_READY") }
    if (-not $settingsPass) { throw "Dashboard Settings did not open through the real mouse IA-card path" }

    $rectBeforeDoubleClick = $dashboardAfterSettings.Current.BoundingRectangle
    $doubleClickBeforeLine = (Read-RuntimeLines).Count
    $doubleClickEvidence = DoubleClick-ScreenPoint -X ([int]$settingsPoint[0]) -Y ([int]$settingsPoint[1]) -Label "Dashboard Settings double-click protection"
    $doubleClickSuppressed = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_NATIVE_HEADER_DOUBLE_CLICK_SUPPRESSED" -AfterLine $doubleClickBeforeLine -TimeoutSeconds 2
    $dashboardAfterDoubleClick = Get-DashboardWindow
    $rectAfterDoubleClick = if ($dashboardAfterDoubleClick) { $dashboardAfterDoubleClick.Current.BoundingRectangle } else { $null }
    $doubleClickGeometryOk = $dashboardAfterDoubleClick -and [Math]::Abs($rectAfterDoubleClick.Width - $rectBeforeDoubleClick.Width) -le 10 -and [Math]::Abs($rectAfterDoubleClick.Height - $rectBeforeDoubleClick.Height) -le 10
    $doubleClickShot = Capture-VirtualScreenshot "03e_after_dashboard_settings_double_click"
    Add-Step -Id "dashboard_settings_double_click_does_not_maximize" -Title "Settings click area does not turn into a native header maximize gesture" -Status ($(if ($doubleClickGeometryOk) { "PASS" } else { "FAIL" })) -Detail "suppressed_marker_seen=$doubleClickSuppressed; width_before=$($rectBeforeDoubleClick.Width); height_before=$($rectBeforeDoubleClick.Height); width_after=$($rectAfterDoubleClick.Width); height_after=$($rectAfterDoubleClick.Height)." -Evidence @{ screenshot = $doubleClickShot; click = $doubleClickEvidence; geometryTolerancePx = 10 }
    if (-not $doubleClickGeometryOk) { throw "Dashboard Settings double-click changed the native Dashboard geometry" }

    $settingsDone = Find-VisibleRuntimeElementByName -Name "Done" -ControlTypeName "ControlType.Button" -TimeoutSeconds 4
    $settingsCloseBeforeLine = (Read-RuntimeLines).Count
    $settingsCloseEvidence = $null
    if ($settingsDone) {
        Click-ElementCenter -Element $settingsDone -Label "Dashboard Settings Done"
        Start-Sleep -Milliseconds 650
        $settingsCloseEvidence = @{ method = "uia-visible-done-button" }
    } else {
        $settingsChildPoints = Get-SettingsChildWindowControlPoints -Dashboard $dashboardAfterDoubleClick
        $donePoint = @($settingsChildPoints.donePoint)
        $settingsCloseEvidence = Click-ScreenPoint -X ([int]$donePoint[0]) -Y ([int]$donePoint[1]) -Label "Dashboard Settings estimated Done button"
    }
    $settingsClosedMarker = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY" -AfterLine $settingsCloseBeforeLine -TimeoutSeconds 4
    if (-not $settingsClosedMarker) {
        $settingsChildPoints = Get-SettingsChildWindowControlPoints -Dashboard $dashboardAfterDoubleClick
        $settingsClosePoint = @($settingsChildPoints.closePoint)
        $settingsCloseBeforeLine = (Read-RuntimeLines).Count
        $settingsCloseEvidence = Click-ScreenPoint -X ([int]$settingsClosePoint[0]) -Y ([int]$settingsClosePoint[1]) -Label "Dashboard Settings estimated Close button"
        $settingsClosedMarker = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY" -AfterLine $settingsCloseBeforeLine -TimeoutSeconds 4
    }
    $settingsClosedShot = Capture-VirtualScreenshot "03f_after_dashboard_settings_done"
    Add-Step -Id "dashboard_settings_done_closes_with_real_mouse" -Title "Dashboard Settings panel closes through visible user control" -Status ($(if ($settingsClosedMarker) { "PASS" } else { "FAIL" })) -Detail "Done button found by UIA=$([bool]$settingsDone); child_window_close_marker=$settingsClosedMarker." -Evidence @{ screenshot = $settingsClosedShot; marker = "MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY"; closeEvidence = $settingsCloseEvidence }
    if (-not $settingsClosedMarker) { throw "Dashboard Settings panel did not close through a visible Done or Close control" }

    $dashboard = Get-DashboardWindow
    if (-not $dashboard) { throw "Dashboard disappeared before window-level Close proof" }
    $chromePoints = Get-DashboardTopChromeControlPoints -Dashboard $dashboard
    $closePoint = @($chromePoints.closePoint)
    $closePointSource = "heuristic-window-level-top-right"
    $closeElementMatch = Find-VisibleRuntimeElementByNames -Names @("Close HUD Dashboard", "Close") -ControlTypeName "ControlType.Button" -TimeoutSeconds 2
    $closeElementRect = @()
    if ($closeElementMatch -and $closeElementMatch.Element) {
        try {
            $rect = $closeElementMatch.Element.Current.BoundingRectangle
            if (-not $rect.IsEmpty -and $rect.Width -gt 0 -and $rect.Height -gt 0) {
                $closePoint = @([int]($rect.X + ($rect.Width / 2)), [int]($rect.Y + ($rect.Height / 2)))
                $closeElementRect = @([int]$rect.X, [int]$rect.Y, [int]($rect.X + $rect.Width), [int]($rect.Y + $rect.Height))
                $closePointSource = "uia-visible-runtime-button:$($closeElementMatch.Name)"
            }
        } catch {}
    }
    $closeHit = Get-NativeHitTestKindAtPoint -WindowHandle ([long]$dashboard.Current.NativeWindowHandle) -X ([int]$closePoint[0]) -Y ([int]$closePoint[1])
    $topCloseBeforeLine = (Read-RuntimeLines).Count
    $topCloseClick = Click-ScreenPoint -X ([int]$closePoint[0]) -Y ([int]$closePoint[1]) -Label "Dashboard window-level Close button"
    $topCloseMarker = Wait-ForRuntimeMarkerAfterLine -Marker "MONITORING_HUD_DASHBOARD_CLOSE_NATIVE_CONTROL_READY" -AfterLine $topCloseBeforeLine -TimeoutSeconds 4
    $topCloseShot = Capture-VirtualScreenshot "03g_after_dashboard_top_chrome_close"
    $dashboardAfterTopClose = Get-DashboardWindow
    $topClosePass = (-not $dashboardAfterTopClose) -and ($closeHit -eq "htclient")
    Add-Step -Id "dashboard_top_chrome_close_hides_dashboard" -Title "Dashboard window-level Close hides Dashboard without disabling HUD Feature" -Status ($(if ($topClosePass) { "PASS" } else { "FAIL" })) -Detail "closePoint=($($closePoint -join ',')); source=$closePointSource; hitTest=$closeHit; native_marker=$topCloseMarker; dashboard_visible_after_close=$([bool]$dashboardAfterTopClose)." -Evidence @{ screenshot = $topCloseShot; click = $topCloseClick; controlPoints = $chromePoints; closeElementRect = $closeElementRect; pointSource = $closePointSource; hitTest = $closeHit; optionalMarker = "MONITORING_HUD_DASHBOARD_CLOSE_NATIVE_CONTROL_READY"; expectedLayout = "window-level top-right Close pill, outside the Dashboard IA card controls" }
    if (-not $topClosePass) { throw "Dashboard window-level Close did not hide the Dashboard through the real mouse path" }

    $reopenAfterX = Invoke-TrayAction -ActionName "Open HUD Dashboard" -ExpectedMarker "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED|source=menu|visible=true" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 900
    $reopenAfterXShot = Capture-VirtualScreenshot "03h_after_reopen_dashboard_after_top_chrome_close"
    $dashboard = Get-DashboardWindow
    Add-Step -Id "dashboard_reopens_after_top_chrome_close" -Title "Tray reopens Dashboard after window-level Close" -Status ($(if ($dashboard) { "PASS" } else { "FAIL" })) -Detail "Dashboard visible after tray reopen from window-level Close: $([bool]$dashboard)" -Evidence @{ screenshot = $reopenAfterXShot; trayClick = $reopenAfterX }
    if (-not $dashboard) { throw "Dashboard did not reopen after window-level Close" }

    $roundedMaskMarker = Wait-ForRuntimeMarker -Marker "MONITORING_HUD_DASHBOARD_ROUNDED_WINDOW_MASK_READY" -TimeoutSeconds 2
    $roundedMaskProof = Invoke-DashboardRoundedCornerMaskProbe -Dashboard $dashboard -WindowHandle ([long]$dashboard.Current.NativeWindowHandle)
    $cornerText = (@($roundedMaskProof.CornerSamples) | ForEach-Object { Format-ColorSample $_ }) -join "; "
    $visibleText = (@($roundedMaskProof.VisibleSamples) | ForEach-Object { Format-ColorSample $_ }) -join "; "
    $roundedMaskPass = $roundedMaskMarker -and $roundedMaskProof.Pass
    Add-Step -Id "dashboard_rounded_corner_mask_light_backdrop" -Title "Dashboard rounded native window mask prevents black corner bleed over a white backdrop" -Status ($(if ($roundedMaskPass) { "PASS" } else { "FAIL" })) -Detail "mask_marker=$roundedMaskMarker; corner_exterior_white=$($roundedMaskProof.CornerPass); visible_dashboard_interior=$($roundedMaskProof.VisibleDashboardPass); corner_samples=$cornerText; interior_samples=$visibleText." -Evidence @{ screenshot = $roundedMaskProof.Screenshot; windowRect = $roundedMaskProof.WindowRect; backdropRect = $roundedMaskProof.BackdropRect; cornerSamples = $roundedMaskProof.CornerSamples; visibleSamples = $roundedMaskProof.VisibleSamples; expectedMarker = "MONITORING_HUD_DASHBOARD_ROUNDED_WINDOW_MASK_READY"; policy = $roundedMaskProof.Policy }
    if (-not $roundedMaskPass) { throw "Dashboard rounded corner native mask did not prove white-backdrop transparency at exterior corner samples" }

    $rectBeforeMove = $dashboard.Current.BoundingRectangle
    $moveHandle = [long]$dashboard.Current.NativeWindowHandle
    $moveStartX = [int]($rectBeforeMove.Left + ($rectBeforeMove.Width / 2))
    $moveStartY = [int]($rectBeforeMove.Top + 48)
    $moveEndX = [int]($moveStartX + 220)
    $moveEndY = [int]($moveStartY + 116)
    $moveSamples = Drag-FromToWithGeometrySamples -Element $dashboard -WindowHandle $moveHandle -StartX $moveStartX -StartY $moveStartY -EndX $moveEndX -EndY $moveEndY -Label "Dashboard header normal-speed move fluidity" -Steps 48 -StepDelayMs 8
    $dashboard = Get-DashboardWindow
    $moveShot = Capture-VirtualScreenshot "04_after_dashboard_mouse_drag"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_move" -Title "Dashboard moves through mouse drag" -Status "FAIL" -Detail "Dashboard disappeared after mouse drag." -Evidence @{ screenshot = $moveShot }
        throw "Dashboard disappeared after mouse drag"
    }
    $rectAfterMove = $dashboard.Current.BoundingRectangle
    $moved = ([Math]::Abs($rectAfterMove.Left - $rectBeforeMove.Left) -ge 12) -or ([Math]::Abs($rectAfterMove.Top - $rectBeforeMove.Top) -ge 12)
    $moveUniquePositions = @($moveSamples | ForEach-Object { "$($_.Left),$($_.Top)" } | Sort-Object -Unique).Count
    $moveTracking = Measure-MoveTracking -Samples $moveSamples -BaseLeft $rectBeforeMove.Left -BaseTop $rectBeforeMove.Top -StartX $moveStartX -StartY $moveStartY
    $moveFluidityPass = $moved -and $moveUniquePositions -ge 24 -and $moveTracking.Pass
    Add-Step -Id "dashboard_mouse_move" -Title "Dashboard moves through mouse drag" -Status ($(if ($moved) { "PASS" } else { "FAIL" })) -Detail "before=($($rectBeforeMove.Left),$($rectBeforeMove.Top)); after=($($rectAfterMove.Left),$($rectAfterMove.Top)); uniquePositionSamples=$moveUniquePositions" -Evidence @{ screenshot = $moveShot; geometrySamples = $moveSamples }
    if (-not $moved) { throw "Dashboard did not move through human-like mouse drag" }
    Add-Step -Id "dashboard_move_fluidity" -Title "Dashboard movement tracks the cursor at normal USER speed" -Status ($(if ($moveFluidityPass) { "PASS" } else { "FAIL" })) -Detail "uniquePositionSamples=$moveUniquePositions; maxLag=$($moveTracking.MaxLagPx)px/avg=$($moveTracking.AverageLagPx)px; maxSampleInterval=$($moveTracking.MaxSampleIntervalMs)ms; sampled at 48 steps with 8ms delay while the left button was held." -Evidence @{ screenshot = $moveShot; geometrySamples = $moveSamples; moveTracking = $moveTracking; minimumUniquePositionSamples = 24; expectation = "returned USER validation says normal-speed movement skips, so LV1 requires high-cadence intermediate geometry plus cursor-to-window tracking-lag proof" }
    if (-not $moveFluidityPass) { throw "Dashboard movement did not track cursor movement smoothly enough during normal-speed drag proof" }

    $ncpTrayIconOpenEvidence = Invoke-TrayIconActivation -ExpectedMarker "RENDERER_MAIN|COMMAND_OVERLAY_READY|phase=entry" -TimeoutSeconds $ActionTimeoutSeconds -Label "NCP tray icon left-click open"
    Start-Sleep -Milliseconds 900
    $ncpTrayIconOpenShot = Capture-VirtualScreenshot "04a_after_tray_icon_open_ncp"
    $ncpVisibleAfterTrayIconOpen = Find-VisibleRuntimeElementByName -Name "O.R.I.N. Command Prompt" -TimeoutSeconds 2
    Add-Step -Id "ncp_tray_icon_left_click_opens" -Title "NCP tray icon left-click opens the Command Overlay" -Status ($(if ($ncpVisibleAfterTrayIconOpen) { "PASS" } else { "FAIL" })) -Detail "Command Overlay visible after tray icon left-click open: $([bool]$ncpVisibleAfterTrayIconOpen)." -Evidence @{ screenshot = $ncpTrayIconOpenShot; trayIconClick = $ncpTrayIconOpenEvidence; expectedMarker = "RENDERER_MAIN|COMMAND_OVERLAY_READY|phase=entry" }
    if (-not $ncpVisibleAfterTrayIconOpen) { throw "Tray icon left-click did not open the Command Overlay" }

    $ncpMenuCloseEvidence = Invoke-TrayAction -ActionName "Close Command Overlay" -ExpectedMarker "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 650
    $ncpMenuCloseShot = Capture-VirtualScreenshot "04a_after_tray_menu_close_ncp"
    $ncpVisibleAfterMenuClose = Find-VisibleRuntimeElementByName -Name "O.R.I.N. Command Prompt" -TimeoutSeconds 1
    Add-Step -Id "ncp_tray_menu_state_changes_to_close" -Title "Tray menu changes Command Overlay action from Open to Close while NCP is open" -Status ($(if (-not $ncpVisibleAfterMenuClose) { "PASS" } else { "FAIL" })) -Detail "Close Command Overlay was exposed by the tray menu and closed the NCP; overlay_visible_after=$([bool]$ncpVisibleAfterMenuClose)." -Evidence @{ screenshot = $ncpMenuCloseShot; trayClick = $ncpMenuCloseEvidence; expectedMarker = "RENDERER_MAIN|COMMAND_OVERLAY_CLOSED" }
    if ($ncpVisibleAfterMenuClose) { throw "Tray menu Close Command Overlay did not close the Command Overlay" }

    $ncpOpenEvidence = Invoke-TrayAction -ActionName "Open Command Overlay" -ExpectedMarker "RENDERER_MAIN|COMMAND_OVERLAY_READY|phase=entry" -TimeoutSeconds $ActionTimeoutSeconds
    Start-Sleep -Milliseconds 900
    $ncpOpenShot = Capture-VirtualScreenshot "04b_after_open_ncp_with_dashboard_visible"
    Add-Step -Id "ncp_opens_with_dashboard_visible" -Title "Tray opens NCP while HUD Dashboard remains visible" -Status "PASS" -Detail "Open Command Overlay emitted ready state while the Dashboard was visible and moved." -Evidence @{ screenshot = $ncpOpenShot; trayClick = $ncpOpenEvidence }

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

    Close-CommandOverlayBeforeDashboardResize
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
    $cornerArcRightX = [int]($rectBeforeResize.Right - 5)
    $cornerArcRightY = [int]($rectBeforeResize.Bottom - 17)
    $cornerArcBottomX = [int]($rectBeforeResize.Right - 17)
    $cornerArcBottomY = [int]($rectBeforeResize.Bottom - 5)
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
    $cursorCornerArcRight = Get-CursorKindAtPoint -X $cornerArcRightX -Y $cornerArcRightY
    $hitCornerArcRight = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $cornerArcRightX -Y $cornerArcRightY
    $cursorCornerArcBottom = Get-CursorKindAtPoint -X $cornerArcBottomX -Y $cornerArcBottomY
    $hitCornerArcBottom = Get-NativeHitTestKindAtPoint -WindowHandle $dashboardHandle -X $cornerArcBottomX -Y $cornerArcBottomY
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
        $hitCornerArcRight -eq "htbottomright" -and
        $hitCornerArcBottom -eq "htbottomright" -and
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
        (Test-ResizeCursorKind $cursorCornerArcRight) -and
        (Test-ResizeCursorKind $cursorCornerArcBottom) -and
        (Test-NonResizeCursorKind $cursorRightOutside) -and
        (Test-NonResizeCursorKind $cursorBottomOutside) -and
        (Test-NonResizeCursorKind $cursorCornerOutside) -and
        (Test-NonResizeCursorKind $cursorRightInterior) -and
        (Test-NonResizeCursorKind $cursorBottomInterior) -and
        (Test-NonResizeCursorKind $cursorRightOutsideAfter)
    )
    Add-Step -Id "dashboard_resize_cursor_alignment" -Title "Dashboard exposes Windows resize hit-tests only near the visible edge" -Status ($(if ($cursorAlignmentPass) { "PASS" } else { "FAIL" })) -Detail "cursor: rightOutside24px=$cursorRightOutside; rightEdge10px=$cursorRight; bottomOutside24px=$cursorBottomOutside; bottomEdge10px=$cursorBottom; cornerOutside24px=$cursorCornerOutside; corner10px=$cursorCorner; right28pxInside=$cursorRightInterior; bottom28pxInside=$cursorBottomInterior; rightOutsideAfter=$cursorRightOutsideAfter | hitTest: rightOutside24px=$hitRightOutside; rightEdge10px=$hitRight; bottomOutside24px=$hitBottomOutside; bottomEdge10px=$hitBottom; cornerOutside24px=$hitCornerOutside; corner10px=$hitCorner; right28pxInside=$hitRightInterior; bottom28pxInside=$hitBottomInterior; rightOutsideAfter=$hitRightOutsideAfter" -Evidence @{ rightEdgeOffsetPx = 10; bottomEdgeOffsetPx = 10; cornerOffsetPx = 10; interiorOffsetPx = 28; outsideOffsetPx = 24; expectedEdgeHitTests = "htright,htbottom,htbottomright"; expectedOutsideAndInteriorHitTests = "not edge"; cursorHandlePolicy = "edge cursor state must differ from outside/interior; WebEngine may report opaque cursor handles" }
    if (-not $cursorAlignmentPass) { throw "Dashboard resize cursor was not aligned to the visible edge/corner rail" }

    $cornerArcExpansionPass = (
        $hitCornerArcRight -eq "htbottomright" -and
        $hitCornerArcBottom -eq "htbottomright" -and
        (Test-ResizeCursorKind $cursorCornerArcRight) -and
        (Test-ResizeCursorKind $cursorCornerArcBottom)
    )
    Add-Step -Id "dashboard_resize_corner_arc_diagonal_zone" -Title "Dashboard rounded corner exposes a larger diagonal resize zone" -Status ($(if ($cornerArcExpansionPass) { "PASS" } else { "FAIL" })) -Detail "central 50% rounded-corner arc policy; right-side arc point offset=(5,17) cursor=$cursorCornerArcRight hitTest=$hitCornerArcRight; bottom-side arc point offset=(17,5) cursor=$cursorCornerArcBottom hitTest=$hitCornerArcBottom." -Evidence @{ rightSideArcPoint = @($cornerArcRightX, $cornerArcRightY); bottomSideArcPoint = @($cornerArcBottomX, $cornerArcBottomY); rightSideArcOffsetPx = @(5,17); bottomSideArcOffsetPx = @(17,5); expectedHitTest = "htbottomright"; expectedCursor = "size-*"; diagonalResizeArcPolicy = "central-50-percent-of-rounded-corner-arc" }
    if (-not $cornerArcExpansionPass) { throw "Dashboard rounded-corner diagonal resize zone did not cover the central 50 percent arc samples" }

    $cornerTransition = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX ([int]($rectBeforeResize.Right + 24)) -StartY ([int]($rectBeforeResize.Bottom + 24)) -EndX ([int]($rectBeforeResize.Right - 16)) -EndY ([int]($rectBeforeResize.Bottom - 16)) -ExpectedHit "htbottomright" -Label "corner outside-to-edge transition"
    $rightTransitionFromOutside = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX $rightOutsideX -StartY $rightSampleY -EndX ([int]($rectBeforeResize.Right - 16)) -EndY $rightSampleY -ExpectedHit "htright" -Label "right outside-to-edge transition"
    $rightTransitionFromInside = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX $rightInteriorX -StartY $rightSampleY -EndX ([int]($rectBeforeResize.Right + 4)) -EndY $rightSampleY -ExpectedHit "htright" -Label "right inside-to-edge transition"
    $bottomTransitionFromOutside = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX $bottomSampleX -StartY $bottomOutsideY -EndX $bottomSampleX -EndY ([int]($rectBeforeResize.Bottom - 16)) -ExpectedHit "htbottom" -Label "bottom outside-to-edge transition"
    $bottomTransitionFromInside = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX $bottomSampleX -StartY $bottomInteriorY -EndX $bottomSampleX -EndY ([int]($rectBeforeResize.Bottom + 4)) -ExpectedHit "htbottom" -Label "bottom inside-to-edge transition"
    $cornerOffset = [Math]::Max([Math]::Abs($rectBeforeResize.Right - $cornerTransition.X), [Math]::Abs($rectBeforeResize.Bottom - $cornerTransition.Y))
    $rightOutsideOffset = [Math]::Abs($rectBeforeResize.Right - $rightTransitionFromOutside.X)
    $rightInsideOffset = [Math]::Abs($rectBeforeResize.Right - $rightTransitionFromInside.X)
    $bottomOutsideOffset = [Math]::Abs($rectBeforeResize.Bottom - $bottomTransitionFromOutside.Y)
    $bottomInsideOffset = [Math]::Abs($rectBeforeResize.Bottom - $bottomTransitionFromInside.Y)
    $transitionPass = (
        $cornerTransition.Found -and $cornerOffset -le 14 -and
        $rightTransitionFromOutside.Found -and $rightOutsideOffset -le 14 -and
        $rightTransitionFromInside.Found -and $rightInsideOffset -le 14 -and
        $bottomTransitionFromOutside.Found -and $bottomOutsideOffset -le 14 -and
        $bottomTransitionFromInside.Found -and $bottomInsideOffset -le 14
    )
    Add-Step -Id "dashboard_resize_cursor_transition_discovery" -Title "Dashboard resize cursor appears before click from outside and inside approaches" -Status ($(if ($transitionPass) { "PASS" } else { "FAIL" })) -Detail "preclick hover delay=90ms; corner=$($cornerTransition.Found)/$($cornerTransition.HitTest)/$($cornerTransition.Cursor)/offset=$cornerOffset; rightOutside=$($rightTransitionFromOutside.Found)/$($rightTransitionFromOutside.HitTest)/$($rightTransitionFromOutside.Cursor)/offset=$rightOutsideOffset; rightInside=$($rightTransitionFromInside.Found)/$($rightTransitionFromInside.HitTest)/$($rightTransitionFromInside.Cursor)/offset=$rightInsideOffset; bottomOutside=$($bottomTransitionFromOutside.Found)/$($bottomTransitionFromOutside.HitTest)/$($bottomTransitionFromOutside.Cursor)/offset=$bottomOutsideOffset; bottomInside=$($bottomTransitionFromInside.Found)/$($bottomTransitionFromInside.HitTest)/$($bottomTransitionFromInside.Cursor)/offset=$bottomInsideOffset" -Evidence @{ corner = $cornerTransition; rightOutside = $rightTransitionFromOutside; rightInside = $rightTransitionFromInside; bottomOutside = $bottomTransitionFromOutside; bottomInside = $bottomTransitionFromInside; maxExpectedVisibleEdgeOffsetPx = 14; hoverDelayMs = 90; mouseButtonState = "not pressed before transition detection" }
    if (-not $transitionPass) { throw "Dashboard resize cursor transition was not discoverable near the visible edge from outside/inside approaches" }

    $cornerSamples = Drag-FromToWithGeometrySamples -Element $dashboard -WindowHandle $dashboardHandle -StartX ([int]$cornerTransition.X) -StartY ([int]$cornerTransition.Y) -EndX ([int]($cornerTransition.X + 80)) -EndY ([int]($cornerTransition.Y + 70)) -Label "Dashboard discovered bottom-right resize cursor transition" -Steps 42 -StepDelayMs 8
    Start-Sleep -Milliseconds 450
    $dashboard = Get-DashboardWindow
    $resizeShot = Capture-VirtualScreenshot "05a_after_dashboard_corner_resize"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_resize_corner" -Title "Dashboard corner resize rail is easy to trigger" -Status "FAIL" -Detail "Dashboard disappeared after corner resize attempt." -Evidence @{ screenshot = $resizeShot }
        throw "Dashboard disappeared after resize attempt"
    }
    $rectAfterResize = $dashboard.Current.BoundingRectangle
    $cornerResized = ([Math]::Abs($rectAfterResize.Width - $rectBeforeResize.Width) -ge 20) -or ([Math]::Abs($rectAfterResize.Height - $rectBeforeResize.Height) -ge 20)
    Add-Step -Id "dashboard_mouse_resize_corner" -Title "Dashboard corner resize cursor transition triggers geometry resize" -Status ($(if ($cornerResized) { "PASS" } else { "FAIL" })) -Detail "before=($($rectBeforeResize.Width)x$($rectBeforeResize.Height)); after=($($rectAfterResize.Width)x$($rectAfterResize.Height)); start=($($cornerTransition.X),$($cornerTransition.Y)) discovered from outside-to-edge cursor transition" -Evidence @{ screenshot = $resizeShot; transition = $cornerTransition }
    if (-not $cornerResized) { throw "Dashboard did not resize through the cursor-aligned corner rail" }

    $rectBeforeRightResize = $dashboard.Current.BoundingRectangle
    $rightStartY = [int]($rectBeforeRightResize.Top + ($rectBeforeRightResize.Height * 0.54))
    $rightResizeTransition = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX ([int]($rectBeforeRightResize.Right + 24)) -StartY $rightStartY -EndX ([int]($rectBeforeRightResize.Right - 16)) -EndY $rightStartY -ExpectedHit "htright" -Label "right edge transition before resize action"
    $rightResizeTransitionOffset = [Math]::Abs($rectBeforeRightResize.Right - $rightResizeTransition.X)
    if (-not $rightResizeTransition.Found -or $rightResizeTransitionOffset -gt 14) {
        throw "Dashboard right-edge resize cursor was not discoverable near the visible edge before resize action"
    }
    $rightSamples = Drag-FromToWithGeometrySamples -Element $dashboard -WindowHandle $dashboardHandle -StartX ([int]$rightResizeTransition.X) -StartY ([int]$rightResizeTransition.Y) -EndX ([int]($rightResizeTransition.X + 76)) -EndY ([int]$rightResizeTransition.Y) -Label "Dashboard discovered right-edge resize cursor transition" -Steps 42 -StepDelayMs 8
    Start-Sleep -Milliseconds 450
    $dashboard = Get-DashboardWindow
    $rightResizeShot = Capture-VirtualScreenshot "05b_after_dashboard_right_edge_resize"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_resize_right_edge" -Title "Dashboard right-edge resize rail is easy to trigger" -Status "FAIL" -Detail "Dashboard disappeared after right-edge resize attempt." -Evidence @{ screenshot = $rightResizeShot }
        throw "Dashboard disappeared after right-edge resize attempt"
    }
    $rectAfterRightResize = $dashboard.Current.BoundingRectangle
    $rightResized = [Math]::Abs($rectAfterRightResize.Width - $rectBeforeRightResize.Width) -ge 20
    $rightUniqueWidths = @($rightSamples | ForEach-Object { $_.Width } | Sort-Object -Unique).Count
    Add-Step -Id "dashboard_mouse_resize_right_edge" -Title "Dashboard right-edge resize cursor transition triggers geometry resize" -Status ($(if ($rightResized) { "PASS" } else { "FAIL" })) -Detail "beforeWidth=$($rectBeforeRightResize.Width); afterWidth=$($rectAfterRightResize.Width); uniqueWidthSamples=$rightUniqueWidths; start=($($rightResizeTransition.X),$($rightResizeTransition.Y)) discovered from outside-to-edge cursor transition; offset=$rightResizeTransitionOffset" -Evidence @{ screenshot = $rightResizeShot; transition = $rightResizeTransition; geometrySamples = $rightSamples }
    if (-not $rightResized) { throw "Dashboard did not resize through the cursor-aligned right-edge rail" }

    $rectBeforeBottomResize = $dashboard.Current.BoundingRectangle
    $bottomStartX = [int]($rectBeforeBottomResize.Left + ($rectBeforeBottomResize.Width * 0.46))
    $bottomResizeTransition = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX $bottomStartX -StartY ([int]($rectBeforeBottomResize.Bottom + 24)) -EndX $bottomStartX -EndY ([int]($rectBeforeBottomResize.Bottom - 16)) -ExpectedHit "htbottom" -Label "bottom edge transition before resize action"
    $bottomResizeTransitionOffset = [Math]::Abs($rectBeforeBottomResize.Bottom - $bottomResizeTransition.Y)
    if (-not $bottomResizeTransition.Found -or $bottomResizeTransitionOffset -gt 14) {
        throw "Dashboard bottom-edge resize cursor was not discoverable near the visible edge before resize action"
    }
    $bottomSamples = Drag-FromToWithGeometrySamples -Element $dashboard -WindowHandle $dashboardHandle -StartX ([int]$bottomResizeTransition.X) -StartY ([int]$bottomResizeTransition.Y) -EndX ([int]$bottomResizeTransition.X) -EndY ([int]($bottomResizeTransition.Y + 76)) -Label "Dashboard discovered bottom-edge resize cursor transition" -Steps 42 -StepDelayMs 8
    Start-Sleep -Milliseconds 450
    $dashboard = Get-DashboardWindow
    $bottomResizeShot = Capture-VirtualScreenshot "05c_after_dashboard_bottom_edge_resize"
    if (-not $dashboard) {
        Add-Step -Id "dashboard_mouse_resize_bottom_edge" -Title "Dashboard bottom-edge resize rail is easy to trigger" -Status "FAIL" -Detail "Dashboard disappeared after bottom-edge resize attempt." -Evidence @{ screenshot = $bottomResizeShot }
        throw "Dashboard disappeared after bottom-edge resize attempt"
    }
    $rectAfterBottomResize = $dashboard.Current.BoundingRectangle
    $bottomResized = [Math]::Abs($rectAfterBottomResize.Height - $rectBeforeBottomResize.Height) -ge 20
    $bottomUniqueHeights = @($bottomSamples | ForEach-Object { $_.Height } | Sort-Object -Unique).Count
    Add-Step -Id "dashboard_mouse_resize_bottom_edge" -Title "Dashboard bottom-edge resize cursor transition triggers geometry resize" -Status ($(if ($bottomResized) { "PASS" } else { "FAIL" })) -Detail "beforeHeight=$($rectBeforeBottomResize.Height); afterHeight=$($rectAfterBottomResize.Height); uniqueHeightSamples=$bottomUniqueHeights; start=($($bottomResizeTransition.X),$($bottomResizeTransition.Y)) discovered from outside-to-edge cursor transition; offset=$bottomResizeTransitionOffset" -Evidence @{ screenshot = $bottomResizeShot; transition = $bottomResizeTransition; geometrySamples = $bottomSamples }
    if (-not $bottomResized) { throw "Dashboard did not resize through the cursor-aligned bottom-edge rail" }

    $rectBeforeGrowVisual = $dashboard.Current.BoundingRectangle
    $growVisualTransition = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX ([int]($rectBeforeGrowVisual.Right + 24)) -StartY ([int]($rectBeforeGrowVisual.Bottom + 24)) -EndX ([int]($rectBeforeGrowVisual.Right - 16)) -EndY ([int]($rectBeforeGrowVisual.Bottom - 16)) -ExpectedHit "htbottomright" -Label "corner grow visual proof transition"
    if (-not $growVisualTransition.Found) { throw "Dashboard corner resize cursor was not discoverable before grow visual proof" }
    $growVisual = Drag-FromToWithGeometryAndVisualSamples -Element $dashboard -WindowHandle $dashboardHandle -StartX ([int]$growVisualTransition.X) -StartY ([int]$growVisualTransition.Y) -EndX ([int]($growVisualTransition.X + 56)) -EndY ([int]($growVisualTransition.Y + 48)) -Label "Dashboard grow live visual resize proof" -Steps 42 -StepDelayMs 8
    $growVisualProof = Test-DashboardDuringDragVisualProof -Samples $growVisual.Samples -Frames $growVisual.Frames -Mode "grow"
    Add-Step -Id "dashboard_resize_grow_during_drag_visual_proof" -Title "Dashboard grow resize repaints while the mouse is held" -Status ($(if ($growVisualProof.Pass) { "PASS" } else { "FAIL" })) -Detail "uniqueSizes=$($growVisualProof.UniqueGeometrySizes); capturedFrames=$($growVisualProof.VisibleFrameCount); pixelSignatureDeltas=$($growVisualProof.SignatureDeltaCount); maxMeanDelta=$($growVisualProof.MaxMeanDelta); frames captured before mouse release." -Evidence @{ visualProof = $growVisualProof; samples = $growVisual.Samples; frames = $growVisual.Frames; transition = $growVisualTransition }
    if (-not $growVisualProof.Pass) { throw "Dashboard grow resize did not produce during-drag visual/pixel-signature proof before mouse release" }

    $dashboard = Get-DashboardWindow
    $rectBeforeShrinkVisual = $dashboard.Current.BoundingRectangle
    $shrinkVisualTransition = Find-ResizeCursorTransition -WindowHandle $dashboardHandle -StartX ([int]($rectBeforeShrinkVisual.Right + 24)) -StartY ([int]($rectBeforeShrinkVisual.Bottom + 24)) -EndX ([int]($rectBeforeShrinkVisual.Right - 16)) -EndY ([int]($rectBeforeShrinkVisual.Bottom - 16)) -ExpectedHit "htbottomright" -Label "corner shrink visual proof transition"
    if (-not $shrinkVisualTransition.Found) { throw "Dashboard corner resize cursor was not discoverable before shrink visual proof" }
    $shrinkVisual = Drag-FromToWithGeometryAndVisualSamples -Element $dashboard -WindowHandle $dashboardHandle -StartX ([int]$shrinkVisualTransition.X) -StartY ([int]$shrinkVisualTransition.Y) -EndX ([int]($shrinkVisualTransition.X - 64)) -EndY ([int]($shrinkVisualTransition.Y - 56)) -Label "Dashboard shrink live visual resize proof" -Steps 42 -StepDelayMs 8
    $shrinkTracking = Measure-ResizeTracking -Samples $shrinkVisual.Samples -BaseWidth $rectBeforeShrinkVisual.Width -BaseHeight $rectBeforeShrinkVisual.Height -StartX $shrinkVisualTransition.X -StartY $shrinkVisualTransition.Y -Mode "corner"
    $shrinkVisualProof = Test-DashboardDuringDragVisualProof -Samples $shrinkVisual.Samples -Frames $shrinkVisual.Frames -Mode "shrink"
    Add-Step -Id "dashboard_resize_shrink_during_drag_visual_proof" -Title "Dashboard shrink resize repaints while the mouse is held" -Status ($(if ($shrinkVisualProof.Pass -and $shrinkTracking.Pass) { "PASS" } else { "FAIL" })) -Detail "uniqueSizes=$($shrinkVisualProof.UniqueGeometrySizes); capturedFrames=$($shrinkVisualProof.VisibleFrameCount); pixelSignatureDeltas=$($shrinkVisualProof.SignatureDeltaCount); maxMeanDelta=$($shrinkVisualProof.MaxMeanDelta); shrinkMaxLag=$($shrinkTracking.MaxLagPx)px/avg=$($shrinkTracking.AverageLagPx)px; frames captured before mouse release." -Evidence @{ visualProof = $shrinkVisualProof; tracking = $shrinkTracking; samples = $shrinkVisual.Samples; frames = $shrinkVisual.Frames; transition = $shrinkVisualTransition }
    if (-not ($shrinkVisualProof.Pass -and $shrinkTracking.Pass)) { throw "Dashboard shrink resize did not produce during-drag visual/pixel-signature proof before mouse release" }

    $resizeShot = Capture-VirtualScreenshot "05_after_dashboard_mouse_resize"
    $cornerUniqueSizes = @($cornerSamples | ForEach-Object { "$($_.Width)x$($_.Height)" } | Sort-Object -Unique).Count
    $cornerTracking = Measure-ResizeTracking -Samples $cornerSamples -BaseWidth $rectBeforeResize.Width -BaseHeight $rectBeforeResize.Height -StartX $cornerTransition.X -StartY $cornerTransition.Y -Mode "corner"
    $rightTracking = Measure-ResizeTracking -Samples $rightSamples -BaseWidth $rectBeforeRightResize.Width -BaseHeight $rectBeforeRightResize.Height -StartX $rightResizeTransition.X -StartY $rightResizeTransition.Y -Mode "right"
    $bottomTracking = Measure-ResizeTracking -Samples $bottomSamples -BaseWidth $rectBeforeBottomResize.Width -BaseHeight $rectBeforeBottomResize.Height -StartX $bottomResizeTransition.X -StartY $bottomResizeTransition.Y -Mode "bottom"
    $resizeFluidityPass = (
        $cornerUniqueSizes -ge 12 -and
        $rightUniqueWidths -ge 12 -and
        $bottomUniqueHeights -ge 12 -and
        $cornerTracking.Pass -and
        $rightTracking.Pass -and
        $bottomTracking.Pass -and
        $growVisualProof.Pass -and
        $shrinkVisualProof.Pass -and
        $shrinkTracking.Pass
    )
    Add-Step -Id "dashboard_resize_fluidity" -Title "Dashboard resize tracks and repaints at a high-refresh cadence" -Status ($(if ($resizeFluidityPass) { "PASS" } else { "FAIL" })) -Detail "cornerUniqueSizes=$cornerUniqueSizes; rightUniqueWidths=$rightUniqueWidths; bottomUniqueHeights=$bottomUniqueHeights; cornerMaxLag=$($cornerTracking.MaxLagPx)px/avg=$($cornerTracking.AverageLagPx)px; rightMaxLag=$($rightTracking.MaxLagPx)px/avg=$($rightTracking.AverageLagPx)px; bottomMaxLag=$($bottomTracking.MaxLagPx)px/avg=$($bottomTracking.AverageLagPx)px; growVisualDeltas=$($growVisualProof.SignatureDeltaCount); shrinkVisualDeltas=$($shrinkVisualProof.SignatureDeltaCount); sampled at 42 steps with 8ms delay while the left button was held." -Evidence @{ cornerSamples = $cornerSamples; rightSamples = $rightSamples; bottomSamples = $bottomSamples; growVisual = $growVisual; shrinkVisual = $shrinkVisual; cornerTracking = $cornerTracking; rightTracking = $rightTracking; bottomTracking = $bottomTracking; shrinkTracking = $shrinkTracking; growVisualProof = $growVisualProof; shrinkVisualProof = $shrinkVisualProof; minimumUniqueSamples = 12; expectation = "returned UTS said #127 shrink/grow smoothness still had frozen/catch-up behavior, so LV1 requires high-cadence geometry, cursor-to-window tracking-lag, and during-drag visual/pixel-signature proof before mouse release" }
    if (-not $resizeFluidityPass) { throw "Dashboard resize did not track cursor movement smoothly enough during high-cadence drag proof" }
    Add-Step -Id "dashboard_mouse_resize" -Title "Dashboard resizes through pre-click Windows resize cursor transitions" -Status "PASS" -Detail "Corner, right-edge, bottom-edge, grow, and shrink resize actions changed real Dashboard geometry after the helper discovered the same standard Windows resize cursor transition a USER would look for before clicking." -Evidence @{ screenshot = $resizeShot; cornerBefore = "$($rectBeforeResize.Width)x$($rectBeforeResize.Height)"; cornerAfter = "$($rectAfterResize.Width)x$($rectAfterResize.Height)"; rightBeforeWidth = $rectBeforeRightResize.Width; rightAfterWidth = $rectAfterRightResize.Width; bottomBeforeHeight = $rectBeforeBottomResize.Height; bottomAfterHeight = $rectAfterBottomResize.Height; cursorRight = $cursorRight; cursorBottom = $cursorBottom; cursorCorner = $cursorCorner; cursorRightInterior = $cursorRightInterior; cursorBottomInterior = $cursorBottomInterior; cornerTransition = $cornerTransition; rightTransition = $rightResizeTransition; bottomTransition = $bottomResizeTransition; resizeFluidity = @{ cornerUniqueSizes = $cornerUniqueSizes; rightUniqueWidths = $rightUniqueWidths; bottomUniqueHeights = $bottomUniqueHeights; cornerTracking = $cornerTracking; rightTracking = $rightTracking; bottomTracking = $bottomTracking; shrinkTracking = $shrinkTracking; growVisualProof = $growVisualProof; shrinkVisualProof = $shrinkVisualProof } }

    $dashboard = Get-DashboardWindow
    Move-DashboardAwayFromTrayMenuIfNeeded -Dashboard $dashboard

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
