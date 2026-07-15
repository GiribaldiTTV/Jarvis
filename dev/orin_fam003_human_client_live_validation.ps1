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
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
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

public sealed class Fam003DesktopIconInfo {
    public int Index { get; set; }
    public string Name { get; set; }
    public int Left { get; set; }
    public int Top { get; set; }
    public int Width { get; set; }
    public int Height { get; set; }
}

public static class Fam003DesktopShell {
    const uint PROCESS_VM_OPERATION = 0x0008;
    const uint PROCESS_VM_READ = 0x0010;
    const uint PROCESS_VM_WRITE = 0x0020;
    const uint PROCESS_QUERY_INFORMATION = 0x0400;
    const uint MEM_COMMIT = 0x1000;
    const uint MEM_RESERVE = 0x2000;
    const uint MEM_RELEASE = 0x8000;
    const uint PAGE_READWRITE = 0x04;
    const int LVM_FIRST = 0x1000;
    const int LVM_GETITEMCOUNT = LVM_FIRST + 4;
    const int LVM_GETITEMRECT = LVM_FIRST + 14;
    const int LVM_GETITEMTEXTW = LVM_FIRST + 115;

    public delegate bool EnumWindowProc(IntPtr hWnd, IntPtr lParam);

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    struct LVITEM {
        public uint mask;
        public int iItem;
        public int iSubItem;
        public uint state;
        public uint stateMask;
        public IntPtr pszText;
        public int cchTextMax;
        public int iImage;
        public IntPtr lParam;
        public int iIndent;
        public int iGroupId;
        public uint cColumns;
        public IntPtr puColumns;
        public IntPtr piColFmt;
        public int iGroup;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct POINT { public int X; public int Y; }

    [StructLayout(LayoutKind.Sequential)]
    struct RECT { public int Left; public int Top; public int Right; public int Bottom; }

    [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern IntPtr FindWindow(string className, string title);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern IntPtr FindWindowEx(IntPtr parent, IntPtr after, string className, string title);
    [DllImport("user32.dll")] static extern bool EnumWindows(EnumWindowProc callback, IntPtr lParam);
    [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
    [DllImport("user32.dll")] static extern IntPtr SendMessage(IntPtr hWnd, int message, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] static extern bool ClientToScreen(IntPtr hWnd, ref POINT point);
    [DllImport("user32.dll")] static extern IntPtr WindowFromPoint(POINT point);
    [DllImport("user32.dll")] static extern IntPtr GetAncestor(IntPtr hWnd, uint flags);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern int GetClassName(IntPtr hWnd, StringBuilder value, int maxCount);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern int GetWindowText(IntPtr hWnd, StringBuilder value, int maxCount);
    [DllImport("user32.dll")] static extern bool GetCursorPos(out POINT point);
    [DllImport("user32.dll")] static extern bool ShowWindowAsync(IntPtr hWnd, int command);
    [DllImport("kernel32.dll")] static extern IntPtr OpenProcess(uint access, bool inherit, uint processId);
    [DllImport("kernel32.dll")] static extern IntPtr VirtualAllocEx(IntPtr process, IntPtr address, UIntPtr size, uint allocationType, uint protect);
    [DllImport("kernel32.dll")] static extern bool VirtualFreeEx(IntPtr process, IntPtr address, UIntPtr size, uint freeType);
    [DllImport("kernel32.dll")] static extern bool WriteProcessMemory(IntPtr process, IntPtr address, byte[] buffer, int size, out IntPtr written);
    [DllImport("kernel32.dll")] static extern bool ReadProcessMemory(IntPtr process, IntPtr address, byte[] buffer, int size, out IntPtr read);
    [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);

    static byte[] StructureBytes<T>(T value) {
        int size = Marshal.SizeOf(typeof(T));
        IntPtr local = Marshal.AllocHGlobal(size);
        try {
            Marshal.StructureToPtr(value, local, false);
            byte[] bytes = new byte[size];
            Marshal.Copy(local, bytes, 0, size);
            return bytes;
        } finally { Marshal.FreeHGlobal(local); }
    }

    static T ReadStructure<T>(byte[] bytes) {
        IntPtr local = Marshal.AllocHGlobal(bytes.Length);
        try {
            Marshal.Copy(bytes, 0, local, bytes.Length);
            return (T)Marshal.PtrToStructure(local, typeof(T));
        } finally { Marshal.FreeHGlobal(local); }
    }

    public static IntPtr DesktopListView() {
        IntPtr progman = FindWindow("Progman", "Program Manager");
        IntPtr defView = FindWindowEx(progman, IntPtr.Zero, "SHELLDLL_DefView", null);
        IntPtr listView = FindWindowEx(defView, IntPtr.Zero, "SysListView32", "FolderView");
        if (listView != IntPtr.Zero) return listView;

        EnumWindows(delegate(IntPtr window, IntPtr ignored) {
            IntPtr childDefView = FindWindowEx(window, IntPtr.Zero, "SHELLDLL_DefView", null);
            if (childDefView == IntPtr.Zero) return true;
            listView = FindWindowEx(childDefView, IntPtr.Zero, "SysListView32", "FolderView");
            return listView == IntPtr.Zero;
        }, IntPtr.Zero);
        return listView;
    }

    public static Fam003DesktopIconInfo FindIcon(string exactDisplayName) {
        IntPtr listView = DesktopListView();
        if (listView == IntPtr.Zero) throw new InvalidOperationException("Windows Desktop list view was not found");
        uint processId;
        GetWindowThreadProcessId(listView, out processId);
        IntPtr process = OpenProcess(PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_QUERY_INFORMATION, false, processId);
        if (process == IntPtr.Zero) throw new InvalidOperationException("Windows Desktop shell process could not be opened for read-only item inspection");

        int textBytes = 1024;
        int itemBytes = Marshal.SizeOf(typeof(LVITEM));
        int rectBytes = Marshal.SizeOf(typeof(RECT));
        IntPtr remoteText = VirtualAllocEx(process, IntPtr.Zero, (UIntPtr)textBytes, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        IntPtr remoteItem = VirtualAllocEx(process, IntPtr.Zero, (UIntPtr)itemBytes, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        IntPtr remoteRect = VirtualAllocEx(process, IntPtr.Zero, (UIntPtr)rectBytes, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        try {
            int count = SendMessage(listView, LVM_GETITEMCOUNT, IntPtr.Zero, IntPtr.Zero).ToInt32();
            IntPtr transferred;
            for (int index = 0; index < count; index++) {
                LVITEM item = new LVITEM();
                item.iSubItem = 0;
                item.pszText = remoteText;
                item.cchTextMax = textBytes / 2;
                WriteProcessMemory(process, remoteItem, StructureBytes(item), itemBytes, out transferred);
                SendMessage(listView, LVM_GETITEMTEXTW, (IntPtr)index, remoteItem);
                byte[] textBuffer = new byte[textBytes];
                ReadProcessMemory(process, remoteText, textBuffer, textBytes, out transferred);
                string name = Encoding.Unicode.GetString(textBuffer).Split('\0')[0];
                if (!String.Equals(name, exactDisplayName, StringComparison.OrdinalIgnoreCase)) continue;

                RECT rect = new RECT();
                rect.Left = 0;
                WriteProcessMemory(process, remoteRect, StructureBytes(rect), rectBytes, out transferred);
                if (SendMessage(listView, LVM_GETITEMRECT, (IntPtr)index, remoteRect) == IntPtr.Zero) {
                    throw new InvalidOperationException("Windows Desktop icon rectangle could not be read");
                }
                byte[] rectBuffer = new byte[rectBytes];
                ReadProcessMemory(process, remoteRect, rectBuffer, rectBytes, out transferred);
                rect = ReadStructure<RECT>(rectBuffer);
                POINT origin = new POINT();
                origin.X = rect.Left;
                origin.Y = rect.Top;
                ClientToScreen(listView, ref origin);
                Fam003DesktopIconInfo result = new Fam003DesktopIconInfo();
                result.Index = index;
                result.Name = name;
                result.Left = origin.X;
                result.Top = origin.Y;
                result.Width = rect.Right - rect.Left;
                result.Height = rect.Bottom - rect.Top;
                return result;
            }
            return null;
        } finally {
            if (remoteText != IntPtr.Zero) VirtualFreeEx(process, remoteText, UIntPtr.Zero, MEM_RELEASE);
            if (remoteItem != IntPtr.Zero) VirtualFreeEx(process, remoteItem, UIntPtr.Zero, MEM_RELEASE);
            if (remoteRect != IntPtr.Zero) VirtualFreeEx(process, remoteRect, UIntPtr.Zero, MEM_RELEASE);
            CloseHandle(process);
        }
    }

    public static string HitClassAt(int x, int y) {
        POINT point = new POINT(); point.X = x; point.Y = y;
        IntPtr window = WindowFromPoint(point);
        StringBuilder value = new StringBuilder(256);
        GetClassName(window, value, value.Capacity);
        return value.ToString();
    }

    public static long RootWindowAt(int x, int y) {
        POINT point = new POINT(); point.X = x; point.Y = y;
        return GetAncestor(WindowFromPoint(point), 2).ToInt64();
    }

    public static string WindowTitle(long handle) {
        StringBuilder value = new StringBuilder(512);
        GetWindowText((IntPtr)handle, value, value.Capacity);
        return value.ToString();
    }

    public static bool RestoreWindow(long handle) {
        return ShowWindowAsync((IntPtr)handle, 9);
    }

    public static int[] CursorPosition() {
        POINT point;
        GetCursorPos(out point);
        return new int[] { point.X, point.Y };
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
$script:MinimizedCoveringWindows = New-Object System.Collections.Generic.List[long]

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
    param(
        [string]$Name = "",
        [string]$Contains = "",
        [string]$Type = "",
        [string]$ClassContains = "",
        [int]$TimeoutSeconds = 8
    )
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
                $currentClass = [string]$element.Current.ClassName
                $rect = $element.Current.BoundingRectangle
                if ($rect.IsEmpty -or $element.Current.IsOffscreen) { continue }
                if ($Name -and $currentName -ne $Name) { continue }
                if ($Contains -and $currentName -notlike "*$Contains*") { continue }
                if ($Type -and $currentType -ne $Type) { continue }
                if ($ClassContains -and $currentClass -notlike "*$ClassContains*") { continue }
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
    $tray = Find-VisibleElement -Contains "Nexus Desktop AI" -Type "ControlType.Button" -ClassContains "SystemTray" -TimeoutSeconds 4
    if (-not $tray) {
        $overflow = Find-VisibleElement -Contains "Hidden" -Type "ControlType.Button" -TimeoutSeconds 3
        if ($overflow) { Move-And-Click $overflow | Out-Null; Start-Sleep -Milliseconds 500 }
        $tray = Find-VisibleElement -Contains "Nexus Desktop AI" -Type "ControlType.Button" -ClassContains "SystemTray" -TimeoutSeconds 6
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

    $beforeLaunch = Capture-Frame "before_exact_desktop_launcher_exposure"
    $launcherDisplayName = [System.IO.Path]::GetFileNameWithoutExtension($Launcher)
    $launcherItem = [Fam003DesktopShell]::FindIcon($launcherDisplayName)
    if (-not $launcherItem) { throw "The exact USER launcher was not found in the actual Windows Desktop shell" }
    $launchX = [int]($launcherItem.Left + ($launcherItem.Width / 2))
    $launchY = [int]($launcherItem.Top + ($launcherItem.Height / 2))
    $coveringWindows = @()
    for ($attempt = 0; $attempt -lt 4; $attempt++) {
        $hitClass = [Fam003DesktopShell]::HitClassAt($launchX, $launchY)
        if ($hitClass -eq "SysListView32") { break }
        $rootHandle = [Fam003DesktopShell]::RootWindowAt($launchX, $launchY)
        if ($rootHandle -eq 0) { throw "The exact Desktop launcher is covered, but its covering window could not be identified" }
        $rootElement = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$rootHandle)
        $minimizeButton = $null
        $windowChildren = $rootElement.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
        for ($childIndex = 0; $childIndex -lt $windowChildren.Count; $childIndex++) {
            $candidate = $windowChildren.Item($childIndex)
            try {
                $candidateRect = $candidate.Current.BoundingRectangle
                if (
                    $candidate.Current.ControlType.ProgrammaticName -eq "ControlType.Button" -and
                    $candidate.Current.Name -eq "Minimize" -and
                    -not $candidateRect.IsEmpty -and
                    -not $candidate.Current.IsOffscreen -and
                    $candidate.Current.IsEnabled
                ) {
                    $minimizeButton = $candidate
                    break
                }
            } catch {}
        }
        if (-not $minimizeButton) { throw "The exact Desktop launcher is covered by a window without a visible Minimize control" }
        $coveringTitle = [Fam003DesktopShell]::WindowTitle($rootHandle)
        $minimizeEvidence = Element-Evidence $minimizeButton
        $minimizePoint = Move-And-Click $minimizeButton
        $script:MinimizedCoveringWindows.Add([long]$rootHandle) | Out-Null
        $coveringWindows += @{ handle = $rootHandle; title = $coveringTitle; minimize = $minimizeEvidence; clickPoint = $minimizePoint }
        Start-Sleep -Milliseconds 700
    }
    $hitClass = [Fam003DesktopShell]::HitClassAt($launchX, $launchY)
    if ($hitClass -ne "SysListView32") { throw "The exact Desktop launcher remains covered after bounded visible window minimization; hit class was '$hitClass'" }
    [Fam003VisibleInput]::SetCursorPos($launchX, $launchY) | Out-Null
    Start-Sleep -Milliseconds 600
    $cursorPosition = [Fam003DesktopShell]::CursorPosition()
    if ($cursorPosition[0] -ne $launchX -or $cursorPosition[1] -ne $launchY) { throw "The real cursor did not reach the exact Desktop launcher" }
    $cursorOnLauncherFrame = Capture-Frame "cursor_positioned_on_exact_windows_desktop_launcher"
    [Fam003VisibleInput]::DoubleClick()
    Start-Sleep -Milliseconds 700
    $afterLaunch = Capture-Frame "after_exact_windows_desktop_launcher_double_click"
    Add-Step "visible_exact_launcher_activation" "PASS" "The helper minimized only windows covering the exact icon through their visible Minimize controls, then moved the real pointer to and double-clicked the actual FAM-003 Windows Desktop shortcut." @{
        before = $beforeLaunch; boundedCoveringWindows = @($coveringWindows); broadDesktopDisruption = $false
        desktopItem = @{ index = $launcherItem.Index; name = $launcherItem.Name; rect = @($launcherItem.Left, $launcherItem.Top, ($launcherItem.Left + $launcherItem.Width), ($launcherItem.Top + $launcherItem.Height)); shellClass = $hitClass }
        cursorPosition = @($cursorPosition); cursorFrame = $cursorOnLauncherFrame; after = $afterLaunch; clickPoint = @($launchX, $launchY)
        directProcessLaunch = $false; environmentInjection = $false; fileExplorerFallback = $false
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

    $ncpTray = Find-VisibleElement -Contains "Nexus Desktop AI" -Type "ControlType.Button" -ClassContains "SystemTray" -TimeoutSeconds 5
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
    $stepRows = @($script:Steps | ForEach-Object { $_ })
    $frameRows = @($script:Frames | ForEach-Object { $_ })
    $blocking = @($stepRows | Where-Object { $_.status -ne "PASS" })
    $status = if ($blocking.Count -eq 0) { "PASS" } else { "BLOCKED" }
    try {
        $payload = [ordered]@{
            schema = "fam003-external-visible-human-client-v2"
            status = $status
            timestamp = $Stamp
            worktree = $Root
            branch = (& git -C $Root branch --show-current).Trim()
            head = (& git -C $Root rev-parse HEAD).Trim()
            formalLauncherPath = $Launcher
            launcherActivationMethod = "visible-windows-desktop-icon-pointer-double-click"
            directHandlerBypass = $false
            environmentInjectedRuntimeProof = $false
            utsStatus = "NOT_REQUESTED"
            steps = $stepRows
            blockingRows = $blocking
            orderedFrames = $frameRows
            orderedFrameCount = $frameRows.Count
            proofRoot = $ProofRoot
            failure = $script:Failure
        }
        $json = $payload | ConvertTo-Json -Depth 14
        $json | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
        $json | Set-Content -LiteralPath $LatestManifestPath -Encoding UTF8
    } finally {
        if (-not $KeepRuntimeOpenOnFailure -or $status -eq "PASS") {
            foreach ($process in @(Find-RuntimeProcesses)) {
                try { Stop-Process -Id $process.ProcessId -Force -ErrorAction Stop } catch {}
            }
        }
        foreach ($coveringHandle in @($script:MinimizedCoveringWindows)) {
            try { [Fam003DesktopShell]::RestoreWindow([long]$coveringHandle) | Out-Null } catch {}
        }
    }
    Write-Output "FAM-003 HUMAN CLIENT LV: $status"
    Write-Output "Proof Root: $ProofRoot"
    Write-Output "Manifest: $ManifestPath"
}
