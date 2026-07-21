param(
    [int]$StartupTimeoutSeconds = 45,
    [switch]$KeepRuntimeOpenOnFailure,
    [switch]$ResizeCursorProofOnly
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Fam003VisibleInputSource = @"
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
public static class Fam003VisibleInput {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr extra);
    [DllImport("user32.dll")] public static extern void keybd_event(byte key, byte scan, uint flags, UIntPtr extra);
    public static void LeftClick() { mouse_event(0x0002, 0, 0, 0, UIntPtr.Zero); mouse_event(0x0004, 0, 0, 0, UIntPtr.Zero); }
    public static void LeftDown() { mouse_event(0x0002, 0, 0, 0, UIntPtr.Zero); }
    public static void LeftUp() { mouse_event(0x0004, 0, 0, 0, UIntPtr.Zero); }
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

public sealed class Fam003CursorSnapshot {
    public bool QuerySucceeded { get; set; }
    public bool Visible { get; set; }
    public long Handle { get; set; }
    public int X { get; set; }
    public int Y { get; set; }
    public int HotspotX { get; set; }
    public int HotspotY { get; set; }
    public string Fingerprint { get; set; }
}

public static class Fam003CursorProof {
    const int CURSOR_SHOWING = 0x00000001;
    const int DI_NORMAL = 0x0003;

    [StructLayout(LayoutKind.Sequential)]
    struct POINT { public int X; public int Y; }

    [StructLayout(LayoutKind.Sequential)]
    struct CURSORINFO {
        public int cbSize;
        public int flags;
        public IntPtr hCursor;
        public POINT ptScreenPos;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct ICONINFO {
        [MarshalAs(UnmanagedType.Bool)] public bool fIcon;
        public int xHotspot;
        public int yHotspot;
        public IntPtr hbmMask;
        public IntPtr hbmColor;
    }

    [DllImport("user32.dll")] static extern bool GetCursorInfo(ref CURSORINFO info);
    [DllImport("user32.dll")] static extern bool GetIconInfo(IntPtr hIcon, out ICONINFO info);
    [DllImport("user32.dll")] static extern bool DrawIconEx(IntPtr hdc, int x, int y, IntPtr hIcon, int cx, int cy, int step, IntPtr brush, int flags);
    [DllImport("user32.dll")] static extern IntPtr LoadCursor(IntPtr instance, IntPtr cursorName);
    [DllImport("gdi32.dll")] static extern bool DeleteObject(IntPtr value);

    static string Fingerprint(IntPtr handle) {
        if (handle == IntPtr.Zero) return "";
        using (Bitmap bitmap = new Bitmap(64, 64, PixelFormat.Format32bppArgb)) {
            using (Graphics graphics = Graphics.FromImage(bitmap)) {
                graphics.Clear(Color.Transparent);
                IntPtr hdc = graphics.GetHdc();
                try { DrawIconEx(hdc, 0, 0, handle, 0, 0, 0, IntPtr.Zero, DI_NORMAL); }
                finally { graphics.ReleaseHdc(hdc); }
            }
            using (MemoryStream stream = new MemoryStream()) {
                bitmap.Save(stream, ImageFormat.Png);
                using (SHA256 sha = SHA256.Create()) {
                    byte[] hash = sha.ComputeHash(stream.ToArray());
                    return BitConverter.ToString(hash).Replace("-", "");
                }
            }
        }
    }

    public static Fam003CursorSnapshot Snapshot() {
        CURSORINFO info = new CURSORINFO();
        info.cbSize = Marshal.SizeOf(typeof(CURSORINFO));
        if (!GetCursorInfo(ref info)) return new Fam003CursorSnapshot { QuerySucceeded = false, Fingerprint = "" };
        int hotX = 0;
        int hotY = 0;
        ICONINFO icon;
        if (info.hCursor != IntPtr.Zero && GetIconInfo(info.hCursor, out icon)) {
            hotX = icon.xHotspot;
            hotY = icon.yHotspot;
            if (icon.hbmMask != IntPtr.Zero) DeleteObject(icon.hbmMask);
            if (icon.hbmColor != IntPtr.Zero) DeleteObject(icon.hbmColor);
        }
        return new Fam003CursorSnapshot {
            QuerySucceeded = true,
            Visible = (info.flags & CURSOR_SHOWING) != 0,
            Handle = info.hCursor.ToInt64(),
            X = info.ptScreenPos.X,
            Y = info.ptScreenPos.Y,
            HotspotX = hotX,
            HotspotY = hotY,
            Fingerprint = Fingerprint(info.hCursor)
        };
    }

    public static string SystemCursorFingerprint(int cursorId) {
        return Fingerprint(LoadCursor(IntPtr.Zero, new IntPtr(cursorId)));
    }

    public static bool DrawSnapshot(Graphics graphics, Fam003CursorSnapshot snapshot, int virtualLeft, int virtualTop) {
        if (snapshot == null || !snapshot.QuerySucceeded || !snapshot.Visible || snapshot.Handle == 0) return false;
        IntPtr hdc = graphics.GetHdc();
        try {
            return DrawIconEx(
                hdc,
                snapshot.X - snapshot.HotspotX - virtualLeft,
                snapshot.Y - snapshot.HotspotY - virtualTop,
                new IntPtr(snapshot.Handle),
                0,
                0,
                0,
                IntPtr.Zero,
                DI_NORMAL
            );
        } finally {
            graphics.ReleaseHdc(hdc);
        }
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
Add-Type -TypeDefinition $Fam003VisibleInputSource -ReferencedAssemblies @("System.Drawing.dll")

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Launcher = Join-Path $env:USERPROFILE "OneDrive\Desktop\Nexus Desktop Launcher.lnk"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$ProofLane = if ($ResizeCursorProofOnly) { "fam003_resize_cursor_workstream_proof" } else { "fam003_human_client_live_validation" }
$ProofRoot = Join-Path $Root "dev\logs\$ProofLane\$Stamp"
$FrameRoot = Join-Path $ProofRoot "ordered_frames"
$ManifestName = if ($ResizeCursorProofOnly) { "fam003_resize_cursor_workstream_proof_manifest.json" } else { "fam003_human_client_live_validation_manifest.json" }
$ManifestPath = Join-Path $ProofRoot $ManifestName
$LatestManifestPath = Join-Path $Root "dev\logs\$ProofLane\latest_manifest.json"
New-Item -ItemType Directory -Force -Path $FrameRoot | Out-Null
$script:Steps = New-Object System.Collections.Generic.List[object]
$script:Frames = New-Object System.Collections.Generic.List[object]
$script:RuntimeProcesses = @()
$script:RuntimeProcessIds = @()
$script:Failure = ""
$script:MinimizedCoveringWindows = New-Object System.Collections.Generic.List[long]
$script:ExplorerBaseline = @()
$explorerShell = New-Object -ComObject Shell.Application
foreach ($explorerWindow in @($explorerShell.Windows())) {
    try {
        $script:ExplorerBaseline += "{0}|{1}" -f $explorerWindow.HWND, $explorerWindow.LocationURL
    } catch {}
}

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
    param([string]$Name, [switch]$IncludeCursor)
    $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bitmap.Size)
        $cursor = [Fam003CursorProof]::Snapshot()
        $cursorComposited = if ($IncludeCursor) {
            [Fam003CursorProof]::DrawSnapshot($graphics, $cursor, $bounds.Left, $bounds.Top)
        } else {
            $false
        }
        $path = Join-Path $FrameRoot ("{0:D3}_{1}.png" -f $script:Frames.Count, $Name)
        $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
        $script:Frames.Add([ordered]@{
            index = $script:Frames.Count
            path = $path
            bytes = (Get-Item $path).Length
            capturedAtUtc = (Get-Date).ToUniversalTime().ToString("o")
            virtualBounds = @($bounds.Left, $bounds.Top, $bounds.Right, $bounds.Bottom)
            cursorRequested = [bool]$IncludeCursor
            cursorComposited = [bool]$cursorComposited
            cursor = @{
                querySucceeded = [bool]$cursor.QuerySucceeded
                visible = [bool]$cursor.Visible
                handle = [long]$cursor.Handle
                x = [int]$cursor.X
                y = [int]$cursor.Y
                hotspotX = [int]$cursor.HotspotX
                hotspotY = [int]$cursor.HotspotY
                fingerprint = [string]$cursor.Fingerprint
            }
        }) | Out-Null
        return $path
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

function Test-FiniteRectangle {
    param([object]$Rectangle)
    foreach ($value in @($Rectangle.Left, $Rectangle.Top, $Rectangle.Width, $Rectangle.Height)) {
        if ([double]::IsNaN([double]$value) -or [double]::IsInfinity([double]$value)) { return $false }
    }
    return $true
}

function Find-VisibleElement {
    param(
        [string]$Name = "",
        [string]$Contains = "",
        [string]$Type = "",
        [string]$ClassContains = "",
        [int[]]$ProcessIds = @(),
        [int]$TimeoutSeconds = 8
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $conditions = New-Object System.Collections.Generic.List[System.Windows.Automation.Condition]
        if ($Name) {
            $conditions.Add(
                (New-Object System.Windows.Automation.PropertyCondition(
                    [System.Windows.Automation.AutomationElement]::NameProperty,
                    $Name
                ))
            ) | Out-Null
        }
        if ($Type) {
            $controlType = switch ($Type) {
                "ControlType.Button" { [System.Windows.Automation.ControlType]::Button }
                "ControlType.Edit" { [System.Windows.Automation.ControlType]::Edit }
                "ControlType.Window" { [System.Windows.Automation.ControlType]::Window }
                "ControlType.MenuItem" { [System.Windows.Automation.ControlType]::MenuItem }
                default { $null }
            }
            if ($controlType) {
                $conditions.Add(
                    (New-Object System.Windows.Automation.PropertyCondition(
                        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
                        $controlType
                    ))
                ) | Out-Null
            }
        }
        if ($ProcessIds.Count -gt 0) {
            $processConditions = @(
                $ProcessIds | ForEach-Object {
                    New-Object System.Windows.Automation.PropertyCondition(
                        [System.Windows.Automation.AutomationElement]::ProcessIdProperty,
                        [int]$_
                    )
                }
            )
            $conditions.Add(
                $(if ($processConditions.Count -eq 1) {
                    $processConditions[0]
                } else {
                    New-Object System.Windows.Automation.OrCondition($processConditions)
                })
            ) | Out-Null
        }
        $condition = if ($conditions.Count -eq 0) {
            [System.Windows.Automation.Condition]::TrueCondition
        } elseif ($conditions.Count -eq 1) {
            $conditions[0]
        } else {
            New-Object System.Windows.Automation.AndCondition($conditions.ToArray())
        }
        $all = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            $condition
        )
        for ($i = 0; $i -lt $all.Count; $i++) {
            $element = $all.Item($i)
            try {
                $currentName = [string]$element.Current.Name
                $currentType = [string]$element.Current.ControlType.ProgrammaticName
                $currentClass = [string]$element.Current.ClassName
                $currentProcessId = [int]$element.Current.ProcessId
                $rect = $element.Current.BoundingRectangle
                if (-not (Test-FiniteRectangle $rect) -or $rect.IsEmpty -or $element.Current.IsOffscreen) { continue }
                if ($Name -and $currentName -ne $Name) { continue }
                if ($Contains -and $currentName -notlike "*$Contains*") { continue }
                if ($Type -and $currentType -ne $Type) { continue }
                if ($ClassContains -and $currentClass -notlike "*$ClassContains*") { continue }
                if ($ProcessIds.Count -gt 0 -and $ProcessIds -notcontains $currentProcessId) { continue }
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
    try {
        $rect = $Element.Current.BoundingRectangle
        if (-not (Test-FiniteRectangle $rect)) {
            return @{ visible = $false; invalidRectangle = $true }
        }
        return @{
            visible = (-not $rect.IsEmpty -and -not $Element.Current.IsOffscreen)
            enabled = [bool]$Element.Current.IsEnabled
            name = [string]$Element.Current.Name
            controlType = [string]$Element.Current.ControlType.ProgrammaticName
            className = [string]$Element.Current.ClassName
            processId = [int]$Element.Current.ProcessId
            rect = @([int]$rect.Left, [int]$rect.Top, [int]($rect.Left + $rect.Width), [int]($rect.Top + $rect.Height))
        }
    } catch {
        return @{ visible = $false; staleElement = $true }
    }
}

function Get-TopLevelWindowElement {
    param([object]$Element)
    if (-not $Element) { return $null }
    $walker = [System.Windows.Automation.TreeWalker]::RawViewWalker
    $current = $Element
    while ($current) {
        try {
            if ($current.Current.ControlType.ProgrammaticName -eq "ControlType.Window") { return $current }
            $current = $walker.GetParent($current)
        } catch {
            return $null
        }
    }
    return $null
}

function Find-VisibleDescendant {
    param(
        [object]$RootElement,
        [string]$Name,
        [int]$TimeoutMilliseconds = 1050
    )
    if (-not $RootElement) { return $null }
    $deadline = (Get-Date).AddMilliseconds($TimeoutMilliseconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $all = $RootElement.FindAll(
                [System.Windows.Automation.TreeScope]::Descendants,
                [System.Windows.Automation.Condition]::TrueCondition
            )
            for ($i = 0; $i -lt $all.Count; $i++) {
                $element = $all.Item($i)
                $rect = $element.Current.BoundingRectangle
                if (-not (Test-FiniteRectangle $rect) -or $rect.IsEmpty -or $element.Current.IsOffscreen) { continue }
                if ([string]$element.Current.Name -eq $Name) { return $element }
            }
        } catch {}
        Start-Sleep -Milliseconds 35
    }
    return $null
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

function Close-NewFam003ExplorerWindows {
    $closed = @()
    $shell = New-Object -ComObject Shell.Application
    foreach ($window in @($shell.Windows())) {
        try {
            $signature = "{0}|{1}" -f $window.HWND, $window.LocationURL
            if ($script:ExplorerBaseline -contains $signature) { continue }
            if (-not $window.LocationURL) { continue }
            $uri = [System.Uri]$window.LocationURL
            $localPath = [System.Uri]::UnescapeDataString($uri.LocalPath).Replace('/', '\')
            if (-not $localPath.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) { continue }
            $closed += @{ title = $window.LocationName; url = $window.LocationURL; hwnd = $window.HWND; localPath = $localPath }
            $window.Quit()
        } catch {}
    }
    return @($closed)
}

function Get-NewFam003ExplorerEffects {
    $effects = @()
    $shell = New-Object -ComObject Shell.Application
    foreach ($window in @($shell.Windows())) {
        try {
            $signature = "{0}|{1}" -f $window.HWND, $window.LocationURL
            if ($script:ExplorerBaseline -contains $signature) { continue }
            if (-not $window.LocationURL) { continue }
            $uri = [System.Uri]$window.LocationURL
            $localPath = [System.Uri]::UnescapeDataString($uri.LocalPath).Replace('/', '\')
            if (-not $localPath.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) { continue }
            $effects += @{ title = $window.LocationName; url = $window.LocationURL; hwnd = $window.HWND; localPath = $localPath }
        } catch {}
    }
    return @($effects)
}

function Wait-NewFam003ExplorerEffect {
    param([int]$TimeoutSeconds = 5)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $effects = @(Get-NewFam003ExplorerEffects)
        if ($effects.Count -gt 0) { return @($effects) }
        Start-Sleep -Milliseconds 150
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
    $global = Find-VisibleElement -Name "Global Settings" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 5
    if (-not $global) { throw "Visible tray right-click did not expose Global Settings" }
    return @{ tray = $evidence; clickPoint = $point; globalSettings = (Element-Evidence $global) }
}

function Invoke-ResizeCursorWorkstreamProof {
    $trayOpen = Open-TrayMenu
    $global = Find-VisibleElement -Name "Global Settings" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    if (-not $global) { throw "Visible tray right-click did not expose Global Settings" }
    $globalEvidence = Element-Evidence $global
    $globalPoint = Move-And-Click $global
    $settings = Find-VisibleElement -Name "Global Settings - Nexus Desktop AI" -Type "ControlType.Window" -ClassContains "ResidentAccessSettingsDialog" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 8
    if (-not $settings) { throw "Visible Global Settings tray action did not open the Settings window" }

    $settingsBefore = Element-Evidence $settings
    $settingsOpenFrame = Capture-Frame "settings_open_current_runtime" -IncludeCursor
    Add-Step "settings_open_current_runtime" "PASS" "The exact FAM-003 Desktop launcher started the current pushed runtime, and the visible resident tray action opened the top-level Global Settings window." @{
        tray = $trayOpen.tray
        trayClickPoint = $trayOpen.clickPoint
        globalSettingsAction = $globalEvidence
        globalSettingsClickPoint = $globalPoint
        settingsWindow = $settingsBefore
        frame = $settingsOpenFrame
    }

    $rect = $settings.Current.BoundingRectangle
    $arrowFingerprint = [Fam003CursorProof]::SystemCursorFingerprint(32512)
    $rightResizeFingerprint = [Fam003CursorProof]::SystemCursorFingerprint(32644)

    $outsideX = [int]($rect.Left + ($rect.Width / 2))
    $outsideY = [int]($rect.Top + [Math]::Min(110, $rect.Height / 3))
    [Fam003VisibleInput]::SetCursorPos($outsideX, $outsideY) | Out-Null
    Start-Sleep -Milliseconds 420
    $outsideFrame = Capture-Frame "pointer_outside_resize_zone_normal" -IncludeCursor
    $outsideCursor = $script:Frames[$script:Frames.Count - 1].cursor
    $outsideComposited = [bool]$script:Frames[$script:Frames.Count - 1].cursorComposited
    $outsideHitZone = ($outsideX -ge [int]($rect.Right - 8))
    $outsideNormal = (
        $outsideComposited -and
        [bool]$outsideCursor.visible -and
        [string]$outsideCursor.fingerprint -eq $arrowFingerprint -and
        -not $outsideHitZone
    )
    Add-Step "pointer_outside_resize_zone" $(if ($outsideNormal) { "PASS" } else { "FAIL" }) "The real pointer must be visibly embedded with the normal arrow shape outside the resize hit zone before the transition sequence begins." @{
        point = @($outsideX, $outsideY)
        hitZone = [bool]$outsideHitZone
        cursor = $outsideCursor
        expectedArrowFingerprint = $arrowFingerprint
        frame = $outsideFrame
        captureMethod = "GDI CopyFromScreen plus DrawIconEx of the GetCursorInfo hCursor at the sampled GetCursorInfo screen position"
    }

    $edgeX = [int]($rect.Right - 4)
    $edgeY = [int]($rect.Top + ($rect.Height / 2))
    [Fam003VisibleInput]::SetCursorPos(($edgeX - 24), $edgeY) | Out-Null
    Start-Sleep -Milliseconds 120
    [Fam003VisibleInput]::SetCursorPos($edgeX, $edgeY) | Out-Null
    Start-Sleep -Milliseconds 520
    $preDragFrame = Capture-Frame "pointer_right_edge_visible_resize_cursor_pre_drag" -IncludeCursor
    $preDragCursor = $script:Frames[$script:Frames.Count - 1].cursor
    $preDragComposited = [bool]$script:Frames[$script:Frames.Count - 1].cursorComposited
    $edgeDistance = [int]$rect.Right - $edgeX
    $edgeHitZone = (
        $edgeDistance -ge 0 -and $edgeDistance -le 8 -and
        $edgeY -gt ([int]$rect.Top + 12) -and
        $edgeY -lt ([int]$rect.Bottom - 12)
    )
    $preDragResize = (
        $preDragComposited -and
        [bool]$preDragCursor.visible -and
        [string]$preDragCursor.fingerprint -eq $rightResizeFingerprint -and
        [string]$preDragCursor.fingerprint -ne $arrowFingerprint -and
        $edgeHitZone
    )
    $cursorClassification = if ($preDragResize) {
        "VISIBLE_CURSOR_TRANSITION_PROVEN"
    } elseif ($preDragComposited -and [bool]$preDragCursor.visible -and $edgeHitZone -and [string]$preDragCursor.fingerprint -eq $arrowFingerprint) {
        "PRODUCT_CURSOR_FAILURE"
    } else {
        "CURSOR_CAPTURE_UNPROVEN"
    }
    Add-Step "visible_cursor_transition_pre_drag" $(if ($preDragResize) { "PASS" } else { "FAIL" }) "The real USER-visible pointer must change from the normal arrow to the horizontal resize cursor inside the right-edge hit zone before mouse-down." @{
        point = @($edgeX, $edgeY)
        rightEdgeDistance = $edgeDistance
        hitZone = [bool]$edgeHitZone
        cursor = $preDragCursor
        expectedResizeFingerprint = $rightResizeFingerprint
        expectedArrowFingerprint = $arrowFingerprint
        classification = $cursorClassification
        frame = $preDragFrame
        captureMethod = "GDI CopyFromScreen plus DrawIconEx of the GetCursorInfo hCursor at the sampled GetCursorInfo screen position"
    }

    $mouseDownAnchorAttempts = @()
    $mouseDownAnchorProven = $false
    $mouseDownAnchorCursor = $null
    $mouseDownAnchorCursorEvidence = $null
    for ($anchorAttempt = 1; $anchorAttempt -le 3; $anchorAttempt++) {
        [Fam003VisibleInput]::SetCursorPos($edgeX, $edgeY) | Out-Null
        Start-Sleep -Milliseconds 140
        $mouseDownAnchorCursor = [Fam003CursorProof]::Snapshot()
        $positionMatched = (
            [Math]::Abs([int]$mouseDownAnchorCursor.X - $edgeX) -le 2 -and
            [Math]::Abs([int]$mouseDownAnchorCursor.Y - $edgeY) -le 2
        )
        $cursorMatched = (
            [bool]$mouseDownAnchorCursor.Visible -and
            [string]$mouseDownAnchorCursor.Fingerprint -eq $rightResizeFingerprint
        )
        $mouseDownAnchorCursorEvidence = @{
            querySucceeded = [bool]$mouseDownAnchorCursor.QuerySucceeded
            visible = [bool]$mouseDownAnchorCursor.Visible
            handle = [long]$mouseDownAnchorCursor.Handle
            x = [int]$mouseDownAnchorCursor.X; y = [int]$mouseDownAnchorCursor.Y
            hotspotX = [int]$mouseDownAnchorCursor.HotspotX; hotspotY = [int]$mouseDownAnchorCursor.HotspotY
            fingerprint = [string]$mouseDownAnchorCursor.Fingerprint
        }
        $mouseDownAnchorAttempts += @{
            attempt = $anchorAttempt; pointMatched = [bool]$positionMatched
            cursorMatched = [bool]$cursorMatched; cursor = $mouseDownAnchorCursorEvidence
        }
        if ($positionMatched -and $cursorMatched) {
            $mouseDownAnchorProven = $true
            break
        }
    }
    Add-Step "pointer_reanchored_before_mouse_down" $(if ($mouseDownAnchorProven) { "PASS" } else { "FAIL" }) "The real pointer must be re-anchored at the proven resize edge and retain the resize cursor immediately before mouse-down." @{
        point = @($edgeX, $edgeY); pointMatches = [bool]$mouseDownAnchorProven
        expectedResizeFingerprint = $rightResizeFingerprint
        cursor = $mouseDownAnchorCursorEvidence; attempts = @($mouseDownAnchorAttempts)
        immediatelyBeforeMouseDown = $true; maximumAttempts = 3
    }
    if (-not $mouseDownAnchorProven) { throw "Pointer could not be anchored at the resize edge immediately before mouse-down" }

    [Fam003VisibleInput]::LeftDown()
    Start-Sleep -Milliseconds 140
    $mouseDownFrame = Capture-Frame "mouse_down_with_visible_resize_cursor" -IncludeCursor
    $mouseDownCursor = $script:Frames[$script:Frames.Count - 1].cursor
    $mouseDownComposited = [bool]$script:Frames[$script:Frames.Count - 1].cursorComposited
    $mouseDownResize = (
        $mouseDownComposited -and
        [bool]$mouseDownCursor.visible -and
        [string]$mouseDownCursor.fingerprint -eq $rightResizeFingerprint -and
        [Math]::Abs([int]$mouseDownCursor.x - $edgeX) -le 8 -and
        [Math]::Abs([int]$mouseDownCursor.y - $edgeY) -le 8
    )
    Add-Step "mouse_down_with_visible_resize_cursor" $(if ($mouseDownResize -and $preDragResize) { "PASS" } else { "FAIL" }) "Mouse-down must begin only after the pre-drag resize cursor and hit-zone proof are established." @{
        point = @($edgeX, $edgeY)
        preDragFrame = $preDragFrame
        mouseDownFrame = $mouseDownFrame
        cursor = $mouseDownCursor
        preDragRequirementSatisfied = [bool]$preDragResize
        anchorRequirementSatisfied = [bool]$mouseDownAnchorProven
    }

    $targetX = $edgeX - 80
    $midDragFrame = $null
    try {
        for ($step = 1; $step -le 8; $step++) {
            $x = [int]($edgeX + (($targetX - $edgeX) * $step / 8))
            [Fam003VisibleInput]::SetCursorPos($x, $edgeY) | Out-Null
            Start-Sleep -Milliseconds 80
            if ($step -eq 4) {
                $midDragFrame = Capture-Frame "held_drag_mid_resize" -IncludeCursor
            }
        }
    } finally {
        [Fam003VisibleInput]::LeftUp()
    }
    Start-Sleep -Milliseconds 650
    $settingsAfter = Find-VisibleElement -Name "Global Settings - Nexus Desktop AI" -Type "ControlType.Window" -ClassContains "ResidentAccessSettingsDialog" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    $settingsAfterEvidence = Element-Evidence $settingsAfter
    $mouseUpFrame = Capture-Frame "mouse_up_completed_resize" -IncludeCursor
    $widthBefore = $settingsBefore.rect[2] - $settingsBefore.rect[0]
    $widthAfter = $settingsAfterEvidence.rect[2] - $settingsAfterEvidence.rect[0]
    $geometryDelta = $widthAfter - $widthBefore
    $geometryPass = $settingsAfterEvidence.visible -and $geometryDelta -le -60
    Add-Step "held_drag_and_completed_resize" $(if ($geometryPass -and $mouseDownResize) { "PASS" } else { "FAIL" }) "A held real-pointer drag must change the top-level Settings window geometry, and mouse-up must leave a valid visibly different window." @{
        before = $settingsBefore
        after = $settingsAfterEvidence
        widthBefore = $widthBefore
        widthAfter = $widthAfter
        widthDelta = $geometryDelta
        start = @($edgeX, $edgeY)
        end = @($targetX, $edgeY)
        midDragFrame = $midDragFrame
        mouseUpFrame = $mouseUpFrame
        classification = $(if ($geometryPass) { "GEOMETRY_RESIZE_PROVEN" } else { "GEOMETRY_RESIZE_UNPROVEN" })
    }

    $afterRect = if ($settingsAfter) { $settingsAfter.Current.BoundingRectangle } else { $rect }
    $leaveX = [int]($afterRect.Left + ($afterRect.Width / 2))
    $leaveY = [int]($afterRect.Top + [Math]::Min(110, $afterRect.Height / 3))
    [Fam003VisibleInput]::SetCursorPos($leaveX, $leaveY) | Out-Null
    Start-Sleep -Milliseconds 420
    $leaveFrame = Capture-Frame "pointer_left_resize_zone_normal_cursor" -IncludeCursor
    $leaveCursor = $script:Frames[$script:Frames.Count - 1].cursor
    $leaveComposited = [bool]$script:Frames[$script:Frames.Count - 1].cursorComposited
    $leaveNormal = (
        $leaveComposited -and
        [bool]$leaveCursor.visible -and
        [string]$leaveCursor.fingerprint -eq $arrowFingerprint
    )
    Add-Step "pointer_leaves_resize_zone" $(if ($leaveNormal) { "PASS" } else { "FAIL" }) "After mouse-up, moving the real pointer away from the resize edge must visibly restore the normal arrow cursor." @{
        point = @($leaveX, $leaveY)
        cursor = $leaveCursor
        expectedArrowFingerprint = $arrowFingerprint
        frame = $leaveFrame
    }

    $overall = $outsideNormal -and $preDragResize -and $mouseDownResize -and $geometryPass -and $leaveNormal
    Add-Step "resize_cursor_workstream_proof" $(if ($overall) { "PASS" } else { "FAIL" }) "Workstream proof requires both completed geometry resize and a current ordered visible cursor transition; internal Qt cursor state remains supporting evidence only." @{
        geometryClassification = $(if ($geometryPass) { "GEOMETRY_RESIZE_PROVEN" } else { "GEOMETRY_RESIZE_UNPROVEN" })
        visibleCursorClassification = $cursorClassification
        internalCursorClassification = "INTERNAL_CURSOR_STATE_SUPPORTING_ONLY"
        preDragCursorFrame = $preDragFrame
        hitZoneProven = [bool]$edgeHitZone
        mouseDownAfterPreDrag = [bool]($preDragResize -and $mouseDownResize)
        mouseDownAnchorProven = [bool]$mouseDownAnchorProven
        completedResize = [bool]$geometryPass
        postDragNormalCursor = [bool]$leaveNormal
    }

    [System.Windows.Forms.SendKeys]::SendWait("%{F4}")
    Start-Sleep -Milliseconds 400
}

function Inspect-Submenu {
    param([string]$Parent, [string]$Child)
    $parentElement = Find-VisibleElement -Name $Parent -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    if (-not $parentElement) { return @{ status = "MISSING"; parent = @{ visible = $false }; child = @{ visible = $false } } }
    $parentEvidence = Element-Evidence $parentElement
    $activationPoint = Move-And-Click $parentElement
    Start-Sleep -Milliseconds 700
    $childElement = Find-VisibleElement -Name $Child -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 3
    return @{
        status = $(if ($childElement) { "PASS" } else { "FAIL" })
        parent = $parentEvidence
        child = (Element-Evidence $childElement)
        activationPoint = $activationPoint
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
    $launcherAnchorAttempts = @()
    $launcherAnchorProven = $false
    $cursorPosition = @()
    for ($launcherAnchorAttempt = 1; $launcherAnchorAttempt -le 3; $launcherAnchorAttempt++) {
        [Fam003VisibleInput]::SetCursorPos($launchX, $launchY) | Out-Null
        Start-Sleep -Milliseconds 140
        $cursorPosition = [Fam003DesktopShell]::CursorPosition()
        $pointMatched = ($cursorPosition[0] -eq $launchX -and $cursorPosition[1] -eq $launchY)
        $launcherAnchorAttempts += @{ attempt = $launcherAnchorAttempt; point = @($cursorPosition); pointMatched = [bool]$pointMatched }
        if ($pointMatched) { $launcherAnchorProven = $true; break }
    }
    Add-Step "pointer_anchored_on_exact_desktop_launcher" $(if ($launcherAnchorProven) { "PASS" } else { "FAIL" }) "The real pointer must be anchored on the exact FAM-003 Desktop icon before visible activation." @{
        expectedPoint = @($launchX, $launchY); actualPoint = @($cursorPosition)
        pointMatches = [bool]$launcherAnchorProven; attempts = @($launcherAnchorAttempts); maximumAttempts = 3
    }
    if (-not $launcherAnchorProven) { throw "The real cursor did not reach the exact Desktop launcher" }
    $cursorOnLauncherFrame = Capture-Frame "cursor_positioned_on_exact_windows_desktop_launcher"
    [Fam003VisibleInput]::SetCursorPos($launchX, $launchY) | Out-Null
    Start-Sleep -Milliseconds 100
    $activationCursorPosition = [Fam003DesktopShell]::CursorPosition()
    if ($activationCursorPosition[0] -ne $launchX -or $activationCursorPosition[1] -ne $launchY) { throw "The real cursor left the exact Desktop launcher before activation" }
    [Fam003VisibleInput]::DoubleClick()
    Start-Sleep -Milliseconds 700
    $afterLaunch = Capture-Frame "after_exact_windows_desktop_launcher_double_click"
    Add-Step "visible_exact_launcher_activation" "PASS" "The helper minimized only windows covering the exact icon through their visible Minimize controls, then moved the real pointer to and double-clicked the actual FAM-003 Windows Desktop shortcut." @{
        before = $beforeLaunch; boundedCoveringWindows = @($coveringWindows); broadDesktopDisruption = $false
        desktopItem = @{ index = $launcherItem.Index; name = $launcherItem.Name; rect = @($launcherItem.Left, $launcherItem.Top, ($launcherItem.Left + $launcherItem.Width), ($launcherItem.Top + $launcherItem.Height)); shellClass = $hitClass }
        cursorPosition = @($cursorPosition); activationCursorPosition = @($activationCursorPosition); cursorFrame = $cursorOnLauncherFrame; after = $afterLaunch; clickPoint = @($launchX, $launchY)
        launcherAnchorProven = [bool]$launcherAnchorProven; launcherAnchorAttempts = @($launcherAnchorAttempts)
        directProcessLaunch = $false; environmentInjection = $false; fileExplorerFallback = $false
    }

    $script:RuntimeProcesses = Wait-For-Runtime
    if ($script:RuntimeProcesses.Count -eq 0) { throw "Exact Desktop shortcut did not start a FAM-003 runtime process" }
    $script:RuntimeProcessIds = @($script:RuntimeProcesses | ForEach-Object { [int]$_.ProcessId })
    Add-Step "runtime_process_provenance" "PASS" "Runtime process command lines resolve to the active FAM-003 root." @{
        processes = @($script:RuntimeProcesses | ForEach-Object { @{ pid = $_.ProcessId; commandLine = $_.CommandLine } })
    }
    Start-Sleep -Seconds 4

    if ($ResizeCursorProofOnly) {
        Invoke-ResizeCursorWorkstreamProof
    } else {
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
    $hudParent = Find-VisibleElement -Name "HUD" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 3
    $hudStatePath = Join-Path $env:LOCALAPPDATA "Nexus Desktop AI\monitoring_hud_state.json"
    $hudState = if (Test-Path $hudStatePath) { Get-Content $hudStatePath -Raw | ConvertFrom-Json } else { $null }
    $hudStateKnown = (
        $null -ne $hudState -and
        $null -ne $hudState.PSObject.Properties["featureEnabled"]
    )
    $hudFeatureEnabled = $hudStateKnown -and [bool]$hudState.featureEnabled
    if ($hudParent -and (-not $hudStateKnown -or -not $hudFeatureEnabled)) {
        $hudFrame = Capture-Frame "tray_hud_doorway_invalid_for_current_state"
        Add-Step "hud_dashboard_resident_doorway" "FAIL" "The resident HUD doorway must be hidden when owner state is disabled or unknown." @{
            statePath = $hudStatePath; stateKnown = [bool]$hudStateKnown; featureEnabled = [bool]$hudFeatureEnabled
            doorwayVisible = $true; visibilityDisposition = "invalid-visible-disabled-or-unknown"; frame = $hudFrame
            currentRouteLabel = "HUD Dashboard"; futureNamingCandidate = "Overlay Dashboard"; futureNamingCandidateStatus = "not-admitted-current-carrier"
            usedDirectHandler = $false; enabledRouteProofStatus = "not-evaluated-invalid-actual-state"
            externalParentLauncherState = "invalid-visible-disabled-or-unknown"; externalIntegrationStatus = "not-completed"
        }
    } elseif ($hudParent) {
        $hud = Inspect-Submenu "HUD" "Open HUD Dashboard"
        if ($hud.status -ne "PASS") { $hud = Inspect-Submenu "HUD" "Close HUD Dashboard" }
        $hudFrame = Capture-Frame "tray_hud_submenu_open"
        $hudAction = if ($hud.child.name) { Find-VisibleElement -Name ([string]$hud.child.name) -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 3 } else { $null }
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
            statePath = $hudStatePath; stateKnown = [bool]$hudStateKnown; featureEnabled = [bool]$hudFeatureEnabled
            doorwayVisible = $true; visibilityDisposition = "visible-enabled"; submenu = $hud; submenuFrame = $hudFrame
            actionClickPoint = $hudActionPoint; targetWindow = $hudWindowEvidence; openedFrame = $hudOpenedFrame
            alreadyOpenState = $closeState; alreadyOpenFrame = $hudAlreadyOpenFrame; usedDirectHandler = $false
            currentRouteLabel = "HUD Dashboard"; futureNamingCandidate = "Overlay Dashboard"; futureNamingCandidateStatus = "not-admitted-current-carrier"
            enabledRouteProofStatus = $(if ($hudStatus -eq "PASS") { "actual-visible-route-pass" } else { "actual-visible-route-fail" })
            externalParentLauncherState = $(if ($hudStatus -eq "PASS") { "visible-route-activated" } elseif (-not $hudWindow) { "target-window-missing" } else { "already-open-state-missing" })
            externalIntegrationStatus = $(if ($hudStatus -eq "PASS") { "observed-current-enabled-session" } else { "failed-current-enabled-session" })
        }
    } else {
        $hudFrame = Capture-Frame "tray_hud_doorway_hidden_by_current_state"
        $hudHiddenStatus = if ($hudStateKnown -and -not $hudFeatureEnabled) { "PASS" } else { "FAIL" }
        Add-Step "hud_dashboard_resident_doorway" $hudHiddenStatus "Current owner state is disabled, so FAM-003 source truth requires the optional HUD doorway to stay hidden. This proves the actual disabled-state obligation only; it does not claim enabled-state external integration." @{
            statePath = $hudStatePath; stateKnown = [bool]$hudStateKnown; featureEnabled = [bool]$hudFeatureEnabled
            doorwayVisible = $false; visibilityDisposition = $(if ($hudHiddenStatus -eq "PASS") { "hidden-disabled" } else { "hidden-without-deterministic-owner-state" })
            frame = $hudFrame; usedDirectHandler = $false; currentRouteLabel = "HUD Dashboard"
            futureNamingCandidate = "Overlay Dashboard"; futureNamingCandidateStatus = "not-admitted-current-carrier"
            enabledRouteProofStatus = "not-proven-by-current-disabled-session"
            externalParentLauncherState = "not-applicable-current-disabled-state"
            externalIntegrationStatus = "post-merge-owner-integration-required"
        }
    }
    [System.Windows.Forms.SendKeys]::SendWait("{ESC}")

    $null = Open-TrayMenu
    $global = Find-VisibleElement -Name "Global Settings" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    $globalEvidence = Element-Evidence $global
    $globalPoint = Move-And-Click $global
    $settings = Find-VisibleElement -Name "Global Settings - Nexus Desktop AI" -Type "ControlType.Window" -ClassContains "ResidentAccessSettingsDialog" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 8
    if (-not $settings) { throw "Visible Global Settings tray action did not open the Settings window" }
    $settingsBefore = Element-Evidence $settings
    $settingsBeforeFrame = Capture-Frame "settings_before_live_resize"
    $rect = $settings.Current.BoundingRectangle
    $rightEdgeX = [int]($rect.Right - 4)
    $rightEdgeY = [int]($rect.Top + ($rect.Height / 2))
    [Fam003VisibleInput]::Drag($rightEdgeX, $rightEdgeY, ($rightEdgeX - 80), $rightEdgeY, 8)
    Start-Sleep -Milliseconds 700
    $settingsMiddle = Find-VisibleElement -Name "Global Settings - Nexus Desktop AI" -Type "ControlType.Window" -ClassContains "ResidentAccessSettingsDialog" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    $settingsMiddleEvidence = Element-Evidence $settingsMiddle
    $settingsMiddleFrame = Capture-Frame "settings_after_live_shrink"
    $middleRect = $settingsMiddle.Current.BoundingRectangle
    $middleRightEdgeX = [int]($middleRect.Right - 4)
    $middleRightEdgeY = [int]($middleRect.Top + ($middleRect.Height / 2))
    [Fam003VisibleInput]::Drag($middleRightEdgeX, $middleRightEdgeY, ($middleRightEdgeX + 100), $middleRightEdgeY, 8)
    Start-Sleep -Milliseconds 700
    $settingsAfter = Find-VisibleElement -Name "Global Settings - Nexus Desktop AI" -Type "ControlType.Window" -ClassContains "ResidentAccessSettingsDialog" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    $settingsAfterEvidence = Element-Evidence $settingsAfter
    $settingsAfterFrame = Capture-Frame "settings_after_live_resize"
    $widthBefore = $settingsBefore.rect[2] - $settingsBefore.rect[0]
    $widthMiddle = $settingsMiddleEvidence.rect[2] - $settingsMiddleEvidence.rect[0]
    $widthAfter = $settingsAfterEvidence.rect[2] - $settingsAfterEvidence.rect[0]
    $resizePass = (
        $settingsMiddleEvidence.visible -and $settingsAfterEvidence.visible -and
        $widthMiddle -le ($widthBefore - 60) -and
        $widthAfter -ge ($widthMiddle + 80)
    )
    Add-Step "settings_visible_route_and_live_resize" $(if ($resizePass) { "PASS" } else { "FAIL" }) "Global Settings must open from the visible tray action and prove bidirectional resize through real right-edge pointer drags away from transparent rounded corners." @{
        buttonVisibleAtInput = $globalEvidence.visible; clickPoint = $globalPoint
        before = $settingsBefore; middle = $settingsMiddleEvidence; after = $settingsAfterEvidence
        beforeFrame = $settingsBeforeFrame; middleFrame = $settingsMiddleFrame; afterFrame = $settingsAfterFrame
        firstDrag = @{ start = @($rightEdgeX, $rightEdgeY); end = @(($rightEdgeX - 80), $rightEdgeY) }
        secondDrag = @{ start = @($middleRightEdgeX, $middleRightEdgeY); end = @(($middleRightEdgeX + 100), $middleRightEdgeY) }
        usedDirectHandler = $false
    }
    [System.Windows.Forms.SendKeys]::SendWait("%{F4}")
    Start-Sleep -Milliseconds 700

    $ncpTray = Find-VisibleElement -Contains "Nexus Desktop AI" -Type "ControlType.Button" -ClassContains "SystemTray" -TimeoutSeconds 5
    if (-not $ncpTray) { throw "Tray icon missing before NCP visible-input proof" }
    $ncpPoint = Move-And-Click $ncpTray
    Start-Sleep -Milliseconds 800
    $ncpEntry = Find-VisibleElement -Contains "O.R.I.N. Command Prompt" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 5
    if (-not $ncpEntry) { $ncpEntry = Find-VisibleElement -Contains "Typed desktop interaction" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 3 }
    $ncpEntryEvidence = Element-Evidence $ncpEntry
    $ncpOverlay = Get-TopLevelWindowElement $ncpEntry
    $ncpOverlayEvidence = Element-Evidence $ncpOverlay
    $ncpEntryFrame = Capture-Frame "ncp_entry_opened_from_tray"
    $ncpInput = if ($ncpEntry) { Find-VisibleElement -Type "ControlType.Edit" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 3 } else { $null }
    $ncpInputEvidence = Element-Evidence $ncpInput
    if ($ncpInput) {
        Move-And-Click $ncpInput | Out-Null
        [System.Windows.Forms.SendKeys]::SendWait("open nexus folder")
    }
    $ncpTypedFrame = Capture-Frame "ncp_typed_input"
    if ($ncpInput) { [System.Windows.Forms.SendKeys]::SendWait("{ENTER}"); Start-Sleep -Milliseconds 900 }
    $ncpChoose = Find-VisibleElement -Contains "Multiple actions matched" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 5
    $ncpChooseEvidence = Element-Evidence $ncpChoose
    $ncpChooseFrame = Capture-Frame "ncp_choose_visible_choices"
    if ($ncpChoose) {
        [System.Windows.Forms.SendKeys]::SendWait("2")
        Start-Sleep -Milliseconds 500
    }
    $ncpConfirm = Find-VisibleElement -Contains "Resolved action" -ProcessIds $script:RuntimeProcessIds -TimeoutSeconds 4
    $ncpConfirmEvidence = Element-Evidence $ncpConfirm
    $ncpConfirmFrame = Capture-Frame "ncp_confirm_selected_action"
    if ($ncpConfirm) {
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    }
    $ncpResult = Find-VisibleDescendant -RootElement $ncpOverlay -Name "Launch request sent." -TimeoutMilliseconds 1050
    $ncpResultEvidence = Element-Evidence $ncpResult
    $ncpResultFrame = Capture-Frame "ncp_result_launch_requested"
    $ncpTargetEffects = @(Wait-NewFam003ExplorerEffect -TimeoutSeconds 5)
    $ncpPass = (
        $ncpOverlayEvidence.visible -and $ncpEntryEvidence.visible -and $ncpInputEvidence.visible -and
        $ncpChooseEvidence.visible -and $ncpConfirmEvidence.visible -and
        $ncpResultEvidence.visible -and $ncpTargetEffects.Count -gt 0
    )
    Add-Step "ncp_visible_keyboard_flow" $(if ($ncpPass) { "PASS" } else { "FAIL" }) "NCP must open from the visible tray icon, expose visible typed, choose, confirm, and result states, and produce the selected real target effect without direct handler calls." @{
        trayClickPoint = $ncpPoint; overlay = $ncpOverlayEvidence; entry = $ncpEntryEvidence; input = $ncpInputEvidence; entryFrame = $ncpEntryFrame; typedText = "open nexus folder"; typedFrame = $ncpTypedFrame; choose = $ncpChooseEvidence; chooseFrame = $ncpChooseFrame; confirm = $ncpConfirmEvidence; confirmFrame = $ncpConfirmFrame; result = $ncpResultEvidence; resultFrame = $ncpResultFrame; targetEffects = $ncpTargetEffects; usedDirectHandler = $false
    }
    }
} catch {
    $script:Failure = $_.Exception.Message
    Add-Step "human_client_exception" "FAIL" $script:Failure @{ stack = $_.ScriptStackTrace }
} finally {
    $explorerCleanup = @(Close-NewFam003ExplorerWindows)
    Add-Step "bounded_explorer_effect_cleanup" "PASS" "Any new Explorer tab created by the NCP functional effect was closed only when rooted inside the active FAM-003 worktree; baseline USER tabs were preserved." @{
        baselineSignatures = @($script:ExplorerBaseline); closed = $explorerCleanup
    }
    $stepRows = @($script:Steps | ForEach-Object { $_ })
    $frameRows = @($script:Frames | ForEach-Object { $_ })
    $blocking = @($stepRows | Where-Object { $_.status -ne "PASS" })
    $status = if ($blocking.Count -eq 0) { "PASS" } else { "BLOCKED" }
    try {
        $payload = [ordered]@{
            schema = $(if ($ResizeCursorProofOnly) { "fam003-r2-workstream-resize-cursor-proof-v1" } else { "fam003-external-visible-human-client-v2" })
            status = $status
            proofMode = $(if ($ResizeCursorProofOnly) { "R2_WORKSTREAM_RESIZE_CURSOR_ONLY" } else { "FORMAL_LV_HUMAN_CLIENT" })
            timestamp = $Stamp
            worktree = $Root
            branch = (& git -C $Root branch --show-current).Trim()
            head = (& git -C $Root rev-parse HEAD).Trim()
            formalLauncherPath = $Launcher
            launcherActivationMethod = "visible-windows-desktop-icon-pointer-double-click"
            directHandlerBypass = $false
            environmentInjectedRuntimeProof = $false
            formalHardening = $false
            formalLiveValidation = (-not $ResizeCursorProofOnly)
            utsStatus = "NOT_REQUESTED"
            cursorCaptureMethod = $(if ($ResizeCursorProofOnly) { "GDI CopyFromScreen plus DrawIconEx of the actual GetCursorInfo hCursor at the sampled GetCursorInfo screen position" } else { "not-required-for-non-cursor-frames" })
            cursorFabrication = $false
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
    Write-Output $(if ($ResizeCursorProofOnly) { "FAM-003 R2 RESIZE CURSOR WORKSTREAM PROOF: $status" } else { "FAM-003 HUMAN CLIENT LV: $status" })
    Write-Output "Proof Root: $ProofRoot"
    Write-Output "Manifest: $ManifestPath"
}
