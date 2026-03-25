import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

# --- Win32 function bindings ---
SendMessageTimeoutW = user32.SendMessageTimeoutW
EnumWindows = user32.EnumWindows
FindWindowW = user32.FindWindowW
FindWindowExW = user32.FindWindowExW
SetParent = user32.SetParent
ShowWindow = user32.ShowWindow
SetWindowPos = user32.SetWindowPos
GetWindowLongPtrW = user32.GetWindowLongPtrW
SetWindowLongPtrW = user32.SetWindowLongPtrW

LONG_PTR = ctypes.c_ssize_t
ULONG_PTR = ctypes.c_size_t

SendMessageTimeoutW.argtypes = [
    wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
    wintypes.UINT, wintypes.UINT, ctypes.POINTER(wintypes.DWORD)
]
SendMessageTimeoutW.restype = wintypes.LPARAM

EnumWindows.argtypes = [ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
EnumWindows.restype = wintypes.BOOL

FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindowW.restype = wintypes.HWND

FindWindowExW.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindowExW.restype = wintypes.HWND

SetParent.argtypes = [wintypes.HWND, wintypes.HWND]
SetParent.restype = wintypes.HWND

ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
ShowWindow.restype = wintypes.BOOL

SetWindowPos.argtypes = [
    wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, wintypes.UINT
]
SetWindowPos.restype = wintypes.BOOL

GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
GetWindowLongPtrW.restype = LONG_PTR

SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, LONG_PTR]
SetWindowLongPtrW.restype = LONG_PTR

# --- Constants ---
SMTO_NORMAL = 0x0000
SW_SHOW = 5

HWND_BOTTOM = 1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
SWP_FRAMECHANGED = 0x0020
SWP_NOOWNERZORDER = 0x0200
SWP_NOSENDCHANGING = 0x0400

GWL_STYLE = -16
GWL_EXSTYLE = -20

WS_CHILD = 0x40000000
WS_VISIBLE = 0x10000000
WS_POPUP = 0x80000000
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_SYSMENU = 0x00080000

WS_EX_TOOLWINDOW = 0x00000080
WS_EX_TRANSPARENT = 0x00000020
WS_EX_NOACTIVATE = 0x08000000
WS_EX_APPWINDOW = 0x00040000

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)


def _to_signed_long_ptr(value: int) -> int:
    """Convert a Python int into a pointer-sized signed integer for SetWindowLongPtrW."""
    bits = ctypes.sizeof(LONG_PTR) * 8
    mask = (1 << bits) - 1
    value &= mask
    sign_bit = 1 << (bits - 1)
    if value & sign_bit:
        value -= (1 << bits)
    return value


def _set_window_long_ptr(hwnd: int, index: int, value: int) -> int:
    return SetWindowLongPtrW(hwnd, index, _to_signed_long_ptr(value))


def get_workerw():
    progman = FindWindowW("Progman", None)
    if progman:
        result = wintypes.DWORD()
        SendMessageTimeoutW(
            progman,
            0x052C,
            0,
            0,
            SMTO_NORMAL,
            1000,
            ctypes.byref(result),
        )

    workerw = None

    @WNDENUMPROC
    def enum_windows_proc(hwnd, lparam):
        nonlocal workerw
        shell_def_view = FindWindowExW(hwnd, None, "SHELLDLL_DefView", None)
        if shell_def_view:
            possible = FindWindowExW(None, hwnd, "WorkerW", None)
            if possible:
                workerw = possible
                return False
        return True

    EnumWindows(enum_windows_proc, 0)
    return workerw


def attach_window_to_desktop(hwnd: int) -> bool:
    workerw = get_workerw()
    if not workerw:
        return False

    # Parent first so the shell owns the window relationship.
    SetParent(hwnd, workerw)

    # Force child-style hosting to try to avoid normal app-window treatment.
    style = int(GetWindowLongPtrW(hwnd, GWL_STYLE))
    style &= ~(
        WS_POPUP
        | WS_OVERLAPPEDWINDOW
        | WS_CAPTION
        | WS_THICKFRAME
        | WS_MINIMIZEBOX
        | WS_MAXIMIZEBOX
        | WS_SYSMENU
    )
    style |= WS_CHILD | WS_VISIBLE
    _set_window_long_ptr(hwnd, GWL_STYLE, style)

    exstyle = int(GetWindowLongPtrW(hwnd, GWL_EXSTYLE))
    exstyle &= ~WS_EX_APPWINDOW
    exstyle |= WS_EX_TRANSPARENT | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW
    _set_window_long_ptr(hwnd, GWL_EXSTYLE, exstyle)

    ShowWindow(hwnd, SW_SHOW)
    SetWindowPos(
        hwnd,
        HWND_BOTTOM,
        0,
        0,
        0,
        0,
        SWP_NOMOVE
        | SWP_NOSIZE
        | SWP_NOACTIVATE
        | SWP_SHOWWINDOW
        | SWP_FRAMECHANGED
        | SWP_NOOWNERZORDER
        | SWP_NOSENDCHANGING,
    )
    return True


def make_window_noninteractive(hwnd: int) -> None:
    # Reapply the desktop-child styles after the widget has finished showing.
    style = int(GetWindowLongPtrW(hwnd, GWL_STYLE))
    style &= ~(
        WS_POPUP
        | WS_OVERLAPPEDWINDOW
        | WS_CAPTION
        | WS_THICKFRAME
        | WS_MINIMIZEBOX
        | WS_MAXIMIZEBOX
        | WS_SYSMENU
    )
    style |= WS_CHILD | WS_VISIBLE
    _set_window_long_ptr(hwnd, GWL_STYLE, style)

    exstyle = int(GetWindowLongPtrW(hwnd, GWL_EXSTYLE))
    exstyle &= ~WS_EX_APPWINDOW
    exstyle |= WS_EX_TRANSPARENT | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW
    _set_window_long_ptr(hwnd, GWL_EXSTYLE, exstyle)

    SetWindowPos(
        hwnd,
        HWND_BOTTOM,
        0,
        0,
        0,
        0,
        SWP_NOMOVE
        | SWP_NOSIZE
        | SWP_NOACTIVATE
        | SWP_SHOWWINDOW
        | SWP_FRAMECHANGED
        | SWP_NOOWNERZORDER
        | SWP_NOSENDCHANGING,
    )
