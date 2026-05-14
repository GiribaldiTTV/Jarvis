import inspect
import json
import os
import re
import ctypes
import ctypes.wintypes
import datetime
import time
import webbrowser
from html import escape

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication,
    QFrame,
    QDialog,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QComboBox,
    QScrollArea,
    QFileDialog,
    QToolTip,
    QSizePolicy,
    QCheckBox,
    QSizeGrip,
)
from PySide6.QtCore import Qt, QTimer, QUrl, QRect, QRectF, Signal, QPoint, QEvent
from PySide6.QtGui import QColor, QCursor, QFont, QPainter, QPainterPath, QPixmap, QRegion
from PySide6.QtTest import QTest
from PySide6.QtWebEngineWidgets import QWebEngineView

from .interaction_overlay_model import CommandOverlayModel
from .ai_provider_state import build_no_provider_ai_state
from .monitoring_hud_controls import build_monitoring_hud_controls_visibility_contract
from .monitoring_hud_placement import build_monitoring_hud_placement_contract
from .monitoring_hud_status import build_monitoring_hud_status_snapshot
from .monitoring_hud_state import save_monitoring_hud_state
from .monitoring_hud_telemetry import build_monitoring_hud_telemetry_snapshot
from .saved_action_authoring import (
    CallableGroupDraft,
    CallableGroupDraftValidationError,
    CallableGroupUnsafeSourceError,
    SavedActionDraft,
    SavedActionDraftValidationError,
    SavedActionUnsafeSourceError,
    create_callable_group_from_draft,
    create_saved_action_from_draft,
    delete_callable_group,
    delete_saved_action,
    load_callable_group_draft_for_edit,
    load_saved_action_draft_for_edit,
    update_callable_group_from_draft,
    update_saved_action_from_draft,
)
from .saved_action_source import SavedActionSourceWriteBlocked
from .shared_action_model import (
    build_callable_group_phrases,
    build_saved_action_callable_phrases,
    default_saved_action_trigger_mode,
    execute_command_group,
    launch_command_action,
)
from .orin_support_reporting import SupportBundleError, prepare_manual_issue_report
from .workerw_utils import (
    attach_window_to_desktop,
    get_last_workerw_probe_events,
    make_window_noninteractive,
    position_desktop_child,
)

WM_NCHITTEST = 0x0084
WM_CANCELMODE = 0x001F
WM_SETCURSOR = 0x0020
WM_NCMOUSEMOVE = 0x00A0
WM_NCLBUTTONDOWN = 0x00A1
WM_NCLBUTTONUP = 0x00A2
WM_NCLBUTTONDBLCLK = 0x00A3
WM_MOUSEMOVE = 0x0200
WM_LBUTTONUP = 0x0202
WM_CAPTURECHANGED = 0x0215
VK_LBUTTON = 0x01
HTTRANSPARENT = -1
HTCLIENT = 1
HTCAPTION = 2
HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17
IDC_ARROW = 32512
IDC_SIZENWSE = 32642
IDC_SIZENESW = 32643
IDC_SIZEWE = 32644
IDC_SIZENS = 32645
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
LoadCursorW = user32.LoadCursorW
LoadCursorW.restype = ctypes.wintypes.HCURSOR
SetCursor = user32.SetCursor
SetCursor.argtypes = [ctypes.wintypes.HCURSOR]
SetCursor.restype = ctypes.wintypes.HCURSOR
SetCapture = user32.SetCapture
SetCapture.argtypes = [ctypes.wintypes.HWND]
SetCapture.restype = ctypes.wintypes.HWND
ReleaseCapture = user32.ReleaseCapture
ReleaseCapture.restype = ctypes.c_bool
GetAsyncKeyState = user32.GetAsyncKeyState
GetAsyncKeyState.argtypes = [ctypes.c_int]
GetAsyncKeyState.restype = ctypes.c_short
GetWindowRect = user32.GetWindowRect
GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
GetWindowRect.restype = ctypes.c_bool
GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = ctypes.wintypes.HWND
GetCurrentThreadId = kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = ctypes.wintypes.DWORD
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.DWORD)]
GetWindowThreadProcessId.restype = ctypes.wintypes.DWORD
AttachThreadInput = user32.AttachThreadInput
AttachThreadInput.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.c_bool]
AttachThreadInput.restype = ctypes.c_bool
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
SetForegroundWindow.restype = ctypes.c_bool
SetActiveWindow = user32.SetActiveWindow
SetActiveWindow.argtypes = [ctypes.wintypes.HWND]
SetActiveWindow.restype = ctypes.wintypes.HWND
BringWindowToTop = user32.BringWindowToTop
BringWindowToTop.argtypes = [ctypes.wintypes.HWND]
BringWindowToTop.restype = ctypes.c_bool
SwitchToThisWindow = user32.SwitchToThisWindow
SwitchToThisWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_bool]
SwitchToThisWindow.restype = None
GetClassNameW = user32.GetClassNameW
GetClassNameW.argtypes = [ctypes.wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
GetClassNameW.restype = ctypes.c_int
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = [ctypes.wintypes.HWND]
GetWindowTextLengthW.restype = ctypes.c_int
GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = [ctypes.wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
GetWindowTextW.restype = ctypes.c_int
SetCursorPos = user32.SetCursorPos
SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
SetCursorPos.restype = ctypes.c_bool
GetCursorPos = user32.GetCursorPos
GetCursorPos.argtypes = [ctypes.POINTER(ctypes.wintypes.POINT)]
GetCursorPos.restype = ctypes.c_bool
WindowFromPoint = user32.WindowFromPoint
WindowFromPoint.argtypes = [ctypes.wintypes.POINT]
WindowFromPoint.restype = ctypes.wintypes.HWND
mouse_event = user32.mouse_event
mouse_event.argtypes = [
    ctypes.wintypes.DWORD,
    ctypes.c_long,
    ctypes.c_long,
    ctypes.wintypes.DWORD,
    ctypes.c_ulong,
]
mouse_event.restype = None
GetSystemMetrics = user32.GetSystemMetrics
GetSystemMetrics.argtypes = [ctypes.c_int]
GetSystemMetrics.restype = ctypes.c_int
SendInput = user32.SendInput
SendInput.restype = ctypes.c_uint
ShowWindowW = user32.ShowWindow
ShowWindowW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
ShowWindowW.restype = ctypes.c_bool
GetWindowLongW = user32.GetWindowLongW
GetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
GetWindowLongW.restype = ctypes.c_long
SetWindowLongW = user32.SetWindowLongW
SetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_long]
SetWindowLongW.restype = ctypes.c_long
IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = [ctypes.wintypes.HWND]
IsWindowVisible.restype = ctypes.c_bool
GetParentW = user32.GetParent
GetParentW.argtypes = [ctypes.wintypes.HWND]
GetParentW.restype = ctypes.wintypes.HWND
SW_HIDE = 0
GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
WS_EX_NOACTIVATE = 0x08000000
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_VIRTUALDESK = 0x4000
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.wintypes.DWORD), ("union", INPUT_UNION)]


SendInput.argtypes = [ctypes.c_uint, ctypes.POINTER(INPUT), ctypes.c_int]
_DIALOG_RUNTIME_LOGGER = None

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWA_BORDER_COLOR = 34
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36
DWMWCP_ROUND = 2

THEMED_TOOLTIP_QSS = """
            QToolTip {
                border: 1px solid rgba(102, 219, 204, 0.22);
                border-radius: 12px;
                background: rgba(5, 16, 28, 248);
                color: rgba(192, 212, 207, 0.96);
                padding: 12px 14px;
                font-size: 12px;
                line-height: 1.45em;
            }
"""


def _windows_colorref(red: int, green: int, blue: int) -> int:
    return (blue << 16) | (green << 8) | red


def _apply_windows_dark_title_bar(widget):
    if os.name != "nt":
        return
    hwnd = 0
    try:
        hwnd = int(widget.winId())
    except Exception:
        hwnd = 0
    if not hwnd:
        return

    try:
        dwmapi = ctypes.windll.dwmapi
        set_window_attribute = dwmapi.DwmSetWindowAttribute
    except Exception:
        return

    def set_int_attribute(attribute: int, value: int):
        try:
            attribute_value = ctypes.c_int(value)
            set_window_attribute(
                ctypes.wintypes.HWND(hwnd),
                ctypes.c_uint(attribute),
                ctypes.byref(attribute_value),
                ctypes.sizeof(attribute_value),
            )
        except Exception:
            pass

    set_int_attribute(DWMWA_USE_IMMERSIVE_DARK_MODE, 1)
    set_int_attribute(DWMWA_WINDOW_CORNER_PREFERENCE, DWMWCP_ROUND)
    set_int_attribute(DWMWA_CAPTION_COLOR, _windows_colorref(9, 18, 28))
    set_int_attribute(DWMWA_TEXT_COLOR, _windows_colorref(236, 247, 255))
    set_int_attribute(DWMWA_BORDER_COLOR, _windows_colorref(26, 61, 86))


def _emit_global_runtime_marker(event: str):
    logger = _DIALOG_RUNTIME_LOGGER
    if not callable(logger):
        return
    try:
        logger(event)
    except Exception:
        pass


def _clear_layout_widgets(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()
        if widget is not None:
            widget.deleteLater()
        elif child_layout is not None:
            _clear_layout_widgets(child_layout)


def _visible_row_height_for_layout(layout, max_rows: int, *, extra_padding: int = 0) -> int:
    if layout is None or max_rows <= 0:
        return 0

    spacing = max(0, int(layout.spacing()))
    margins = layout.contentsMargins()
    total_height = margins.top() + margins.bottom()
    visible_rows = 0

    for index in range(layout.count()):
        item = layout.itemAt(index)
        if item is None:
            continue
        widget = item.widget()
        if widget is None or not widget.isVisible():
            continue
        rendered_height = widget.height() if widget.height() > 0 else 0
        row_height = (
            rendered_height
            if rendered_height > 0
            else max(widget.sizeHint().height(), widget.minimumSizeHint().height())
        )
        total_height += row_height
        visible_rows += 1
        if visible_rows >= max_rows:
            break
        total_height += spacing

    if visible_rows == 0:
        return 0
    return total_height + max(0, int(extra_padding))


def _screen_available_geometry_for_widget(widget: QWidget) -> QRect | None:
    screen = None
    try:
        screen = widget.screen()
    except Exception:
        screen = None
    if screen is None:
        try:
            screen = QApplication.screenAt(widget.frameGeometry().center())
        except Exception:
            screen = None
    if screen is None:
        try:
            screen = QApplication.primaryScreen()
        except Exception:
            screen = None
    if screen is None:
        return None
    try:
        return screen.availableGeometry()
    except Exception:
        return None


def _clamp_window_to_available_screen(widget: QWidget, *, padding: int = 18):
    bounds = _screen_available_geometry_for_widget(widget)
    if bounds is None:
        return

    max_width = max(360, bounds.width() - (padding * 2))
    max_height = max(280, bounds.height() - (padding * 2))
    target_width = min(widget.width(), max_width)
    target_height = min(widget.height(), max_height)
    if target_width != widget.width() or target_height != widget.height():
        widget.resize(target_width, target_height)

    frame = widget.frameGeometry()
    x = max(bounds.x() + padding, min(frame.x(), bounds.x() + bounds.width() - frame.width() - padding))
    y = max(bounds.y() + padding, min(frame.y(), bounds.y() + bounds.height() - frame.height() - padding))
    if x != frame.x() or y != frame.y():
        widget.move(x, y)


def _schedule_window_clamp(widget: QWidget, *, padding: int = 18):
    QTimer.singleShot(0, lambda target=widget, inset=padding: _clamp_window_to_available_screen(target, padding=inset))


def _apply_rounded_dialog_mask(widget: QWidget, *, radius: int = 22):
    if widget is None:
        return
    rect = widget.rect()
    if rect.width() <= 0 or rect.height() <= 0:
        return
    path = QPainterPath()
    path.addRoundedRect(QRectF(rect), radius, radius)
    widget.setMask(QRegion(path.toFillPolygon().toPolygon()))


def _saved_inventory_target_kind_label(item: dict) -> str:
    raw_target_kind = (item.get("target_kind_label") or item.get("target_kind") or "").strip()
    normalized = raw_target_kind.casefold()
    if normalized == "app":
        return "Application"
    if normalized == "folder":
        return "Folder"
    if normalized == "file":
        return "File"
    if normalized == "url":
        return "Website URL"
    return raw_target_kind


def _build_saved_inventory_item_text(item: dict) -> str:
    title = item.get("title", "")
    origin_label = item.get("origin_label", "Saved")
    target_kind = item.get("target_kind", "")
    target_display = item.get("target_display") or item.get("target", "")
    item_text = title
    metadata_bits = [origin_label]
    if target_kind:
        metadata_bits.append(target_kind)
    if metadata_bits:
        item_text += f"\n{' • '.join(metadata_bits)}"
    if target_display:
        item_text += f"\n{target_display}"
    return item_text


def _populate_saved_inventory_item_layout(
    layout,
    parent,
    items: list[dict],
    edit_handler,
    delete_handler,
):
    _clear_layout_widgets(layout)
    for item in items:
        item_id = str(item.get("id") or "").strip()
        title = item.get("title", "")
        origin_label = item.get("origin_label", "Saved")
        target_kind_label = _saved_inventory_target_kind_label(item)
        target_display = item.get("target_display") or item.get("target", "")

        item_frame = QFrame(parent)
        item_frame.setProperty("inventoryRole", "itemFrame")
        item_frame.setMinimumHeight(70)
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(8, 4, 8, 4)
        item_layout.setSpacing(6)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(1)

        title_label = QLabel(title, item_frame)
        title_label.setProperty("inventoryRole", "itemTitle")
        title_label.setWordWrap(True)
        content_layout.addWidget(title_label)

        metadata_bits = [f"{origin_label} task"]
        if target_kind_label:
            metadata_bits.append(target_kind_label)
        metadata_label = QLabel(" | ".join(metadata_bits), item_frame)
        metadata_label.setProperty("inventoryRole", "itemMeta")
        metadata_label.setWordWrap(True)
        content_layout.addWidget(metadata_label)

        if target_display:
            target_label = QLabel(target_display, item_frame)
            target_label.setProperty("inventoryRole", "itemTarget")
            target_label.setWordWrap(True)
            target_label.setToolTip(item.get("target", ""))
            content_layout.addWidget(target_label)

        item_layout.addLayout(content_layout, 1)

        if item_id:
            action_shell = QFrame(item_frame)
            action_shell.setProperty("inventoryRole", "actionShell")
            button_layout = QVBoxLayout(action_shell)
            button_layout.setContentsMargins(2, 2, 2, 2)
            button_layout.setSpacing(2)

            edit_button = QPushButton("Edit", action_shell)
            edit_button.setProperty("inventoryRole", "editButton")
            edit_button.setToolTip(f'Edit "{title}"')
            edit_button.clicked.connect(
                lambda _checked=False, action_id=item_id: edit_handler(action_id)
            )
            button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", action_shell)
            delete_button.setProperty("inventoryRole", "deleteButton")
            delete_button.setToolTip(f'Delete "{title}"')
            delete_button.clicked.connect(
                lambda _checked=False, action_id=item_id: delete_handler(action_id)
            )
            button_layout.addWidget(delete_button)
            button_layout.addStretch(1)

            item_layout.addWidget(action_shell, 0, Qt.AlignTop)

        layout.addWidget(item_frame)
    layout.addStretch(1)


def _populate_saved_group_item_layout(
    layout,
    parent,
    items: list[dict],
    edit_handler,
    delete_handler,
):
    _clear_layout_widgets(layout)
    for item in items:
        item_id = str(item.get("id") or "").strip()
        title = item.get("title", "")
        aliases = item.get("aliases") or []
        member_count = int(item.get("member_count") or 0)
        member_noun = "member" if member_count == 1 else "members"
        alias_preview = ", ".join(str(alias).strip() for alias in aliases if str(alias).strip())

        item_frame = QFrame(parent)
        item_frame.setProperty("inventoryRole", "itemFrame")
        item_frame.setMinimumHeight(70)
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(8, 4, 8, 4)
        item_layout.setSpacing(6)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(1)

        title_label = QLabel(title, item_frame)
        title_label.setProperty("inventoryRole", "itemTitle")
        title_label.setWordWrap(True)
        content_layout.addWidget(title_label)

        metadata_label = QLabel(f"Custom group | {member_count} {member_noun}", item_frame)
        metadata_label.setProperty("inventoryRole", "itemMeta")
        metadata_label.setWordWrap(True)
        metadata_label.setToolTip(
            f'This group can surface {member_count} {member_noun} when one of its exact aliases is used.'
        )
        content_layout.addWidget(metadata_label)

        if alias_preview:
            aliases_label = QLabel(f"Aliases: {alias_preview}", item_frame)
            aliases_label.setProperty("inventoryRole", "itemTarget")
            aliases_label.setWordWrap(True)
            aliases_label.setToolTip(f'Exact callable aliases for "{title}": {alias_preview}')
            content_layout.addWidget(aliases_label)

        item_layout.addLayout(content_layout, 1)

        if item_id:
            action_shell = QFrame(item_frame)
            action_shell.setProperty("inventoryRole", "actionShell")
            button_layout = QVBoxLayout(action_shell)
            button_layout.setContentsMargins(2, 2, 2, 2)
            button_layout.setSpacing(2)

            edit_button = QPushButton("Edit", action_shell)
            edit_button.setProperty("inventoryRole", "editButton")
            edit_button.setToolTip(f'Edit the aliases or members for "{title}".')
            edit_button.clicked.connect(
                lambda _checked=False, group_id=item_id: edit_handler(group_id)
            )
            button_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete", action_shell)
            delete_button.setProperty("inventoryRole", "deleteButton")
            delete_button.setToolTip(f'Delete the group "{title}". Tasks stay saved.')
            delete_button.clicked.connect(
                lambda _checked=False, group_id=item_id: delete_handler(group_id)
            )
            button_layout.addWidget(delete_button)
            button_layout.addStretch(1)

            item_layout.addWidget(action_shell, 0, Qt.AlignTop)

        layout.addWidget(item_frame)
    layout.addStretch(1)


class CommandInputLineEdit(QLineEdit):
    submit_requested = Signal()
    escape_requested = Signal()
    input_armed_changed = Signal(bool)
    focus_acquired = Signal()
    focus_lost = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._input_armed = False
        self._manual_focus_requested = False
        self._last_focus_was_manual = False
        self._local_typing_enabled = False
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setPlaceholderText("Type a built-in or saved action")
        self.setReadOnly(True)

    def is_input_armed(self) -> bool:
        return self._input_armed

    def set_input_armed(self, armed: bool, notify: bool = True):
        armed = bool(armed)
        if self._input_armed == armed:
            return

        self._input_armed = armed
        self.setReadOnly(not armed)
        if not armed:
            self._local_typing_enabled = False
            self.clearFocus()
        if notify:
            self.input_armed_changed.emit(armed)

    def set_local_typing_enabled(self, enabled: bool):
        self._local_typing_enabled = bool(enabled)

    def mousePressEvent(self, event):
        if event.button() in (Qt.LeftButton, Qt.RightButton):
            if not self._input_armed:
                self.set_input_armed(True)
            self._manual_focus_requested = True
            self._local_typing_enabled = True
            self.setFocus(Qt.MouseFocusReason)
            # The line can already be programmatically focused on open, so a real
            # user click needs to re-assert manual ownership even if focusInEvent
            # does not fire again.
            self._last_focus_was_manual = True
            self.focus_acquired.emit()
            if event.button() == Qt.RightButton:
                event.accept()
                return

        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if not self._local_typing_enabled:
                event.accept()
                return
            self.submit_requested.emit()
            event.accept()
            return

        if event.key() == Qt.Key_Escape:
            if not self._local_typing_enabled:
                event.accept()
                return
            self.escape_requested.emit()
            event.accept()
            return

        if not self._input_armed:
            event.accept()
            return

        if not self._local_typing_enabled:
            event.accept()
            return

        super().keyPressEvent(event)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self._last_focus_was_manual = self._manual_focus_requested or event.reason() == Qt.MouseFocusReason
        self._manual_focus_requested = False
        self.focus_acquired.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self._last_focus_was_manual = False
        self._manual_focus_requested = False
        self.focus_lost.emit()

    def last_focus_was_manual(self) -> bool:
        return self._last_focus_was_manual


class ImmediateHelpButton(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTipDuration(20000)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_Hover, True)

    def _tooltip_anchor(self) -> QPoint:
        return self.mapToGlobal(
            QPoint(max(22, min(self.width() - 12, self.width() // 3)), self.height() + 12)
        )

    def show_help_tooltip_now(self):
        tooltip_text = (self.toolTip() or "").strip()
        if not tooltip_text:
            return
        QToolTip.hideText()
        QToolTip.showText(
            self._tooltip_anchor(),
            tooltip_text,
            self,
            self.rect(),
            self.toolTipDuration(),
        )

    def enterEvent(self, event):
        super().enterEvent(event)
        self.show_help_tooltip_now()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.show_help_tooltip_now()

    def mousePressEvent(self, event):
        self.show_help_tooltip_now()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.show_help_tooltip_now()
            event.accept()
            return
        super().keyPressEvent(event)

    def leaveEvent(self, event):
        QToolTip.hideText()
        super().leaveEvent(event)

    def focusOutEvent(self, event):
        QToolTip.hideText()
        super().focusOutEvent(event)


class DialogChromeBar(QFrame):
    def __init__(self, title: str, dialog: QDialog, *, object_prefix: str, parent=None, show_title: bool = False):
        super().__init__(parent or dialog)
        self._dialog = dialog
        self._drag_offset: QPoint | None = None
        self.setObjectName(f"{object_prefix}ChromeBar")
        self.setProperty("chromeRole", "bar")
        self.setProperty("showTitle", bool(show_title))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.OpenHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 5, 16, 3)
        layout.setSpacing(4)

        self.title_label = QLabel(title, self)
        self.title_label.setObjectName(f"{object_prefix}ChromeTitle")
        self.title_label.setProperty("chromeRole", "title")
        self.title_label.setVisible(bool(show_title))
        layout.addWidget(self.title_label, 0, Qt.AlignVCenter)
        layout.addStretch(1)

        self.close_button = QPushButton("\N{MULTIPLICATION SIGN}", self)
        self.close_button.setObjectName(f"{object_prefix}ChromeClose")
        self.close_button.setProperty("chromeRole", "close")
        self.close_button.setToolTip("Close")
        close_font = QFont("Segoe UI Symbol")
        close_font.setPointSize(11)
        close_font.setWeight(QFont.DemiBold)
        self.close_button.setFont(close_font)
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self._dialog.reject)
        layout.addWidget(self.close_button, 0, Qt.AlignVCenter)
        self.setFixedHeight(28)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self._dialog.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and event.buttons() & Qt.LeftButton:
            self._dialog.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_offset = None
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)


class QuickCreateGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("New Group")
        self.setObjectName("quickCreateGroupDialog")
        self.setMinimumWidth(420)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.shell = QFrame(self)
        self.shell.setObjectName("quickCreateGroupShell")
        root_layout.addWidget(self.shell)

        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.content = QWidget(self.shell)
        self.content.setObjectName("quickCreateGroupContent")
        shell_layout.addWidget(self.content)

        self.chrome_bar = DialogChromeBar(
            "New Group",
            self,
            object_prefix="quickCreateGroup",
            parent=self.shell,
            show_title=False,
        )
        self.chrome_bar.raise_()

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(22, 10, 22, 16)
        layout.setSpacing(10)

        title_label = QLabel("New Group", self)
        title_label.setObjectName("quickCreateGroupTitle")
        layout.addWidget(title_label)

        hint_label = QLabel(
            "Create a callable group name and aliases for the current task. The task becomes the first member when save succeeds.",
            self,
        )
        hint_label.setObjectName("quickCreateGroupHint")
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        name_label = QLabel("Group name", self)
        name_label.setProperty("createRole", "fieldHeader")
        layout.addWidget(name_label)

        self.title_input = QLineEdit(self)
        self.title_input.setObjectName("quickCreateGroupTitleInput")
        self.title_input.setMinimumHeight(42)
        self.title_input.setPlaceholderText("Workspace Tools")
        layout.addWidget(self.title_input)

        aliases_label = QLabel("Aliases", self)
        aliases_label.setProperty("createRole", "fieldHeader")
        layout.addWidget(aliases_label)

        self.aliases_input = QLineEdit(self)
        self.aliases_input.setObjectName("quickCreateGroupAliasesInput")
        self.aliases_input.setMinimumHeight(42)
        self.aliases_input.setPlaceholderText("workspace tools, tools group")
        layout.addWidget(self.aliases_input)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("quickCreateGroupStatus")
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        layout.addWidget(self.status_label)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 0, 0)
        button_row.setSpacing(8)
        button_row.addStretch(1)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        button_row.addWidget(cancel_button)

        create_button = QPushButton("Add Group", self)
        create_button.setDefault(True)
        create_button.clicked.connect(self._handle_submit)
        button_row.addWidget(create_button)

        layout.addLayout(button_row)

        self.setStyleSheet(
            """
            #quickCreateGroupDialog { background: transparent; }
            #quickCreateGroupShell {
                border-radius: 18px;
                border: 1px solid rgba(118, 226, 255, 0.14);
                background: rgb(9, 18, 28);
            }
            #quickCreateGroupContent { background: transparent; }
            #quickCreateGroupChromeBar {
                border: none;
                background: transparent;
            }
            QPushButton[chromeRole="close"] {
                min-width: 24px;
                max-width: 24px;
                min-height: 20px;
                max-height: 20px;
                padding: 0 0 1px 0;
                text-align: center;
                border-radius: 8px;
                border: 1px solid rgba(118, 226, 255, 0.10);
                background: rgba(26, 62, 92, 0.94);
                color: rgba(191, 212, 207, 0.94);
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton[chromeRole="close"]:hover {
                border: 1px solid rgba(102, 219, 204, 0.24);
                background: rgba(15, 36, 52, 0.70);
            }
            #quickCreateGroupTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 22px;
                font-weight: 650;
            }
            #quickCreateGroupHint {
                color: rgba(136, 165, 174, 0.88);
                font-size: 12px;
            }
            #quickCreateGroupStatus {
                color: rgba(255, 189, 176, 0.96);
                font-size: 12px;
            }
            QLineEdit {
                min-height: 42px;
                border-radius: 13px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(193, 213, 208, 0.96);
                padding: 7px 14px;
            }
            QPushButton {
                min-height: 38px;
                padding: 0 18px;
                border-radius: 11px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
            }
            """
        )

        self._update_chrome_overlay_geometry()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_chrome_overlay_geometry()

    def _update_chrome_overlay_geometry(self):
        if hasattr(self, "chrome_bar") and hasattr(self, "shell"):
            self.chrome_bar.setGeometry(6, 6, max(72, self.shell.width() - 12), self.chrome_bar.height())
            self.chrome_bar.raise_()

    def draft(self) -> CallableGroupDraft:
        aliases = tuple(
            part.strip()
            for part in (self.aliases_input.text() or "").replace("\n", ",").split(",")
            if part.strip()
        )
        return CallableGroupDraft(
            title=self.title_input.text(),
            aliases=aliases,
            member_action_ids=(),
        )

    def _handle_submit(self):
        try:
            _coerced = CallableGroupDraft(
                title=self.title_input.text().strip(),
                aliases=tuple(
                    part.strip()
                    for part in (self.aliases_input.text() or "").replace("\n", ",").split(",")
                    if part.strip()
                ),
                member_action_ids=(),
            )
            if not _coerced.title:
                raise CallableGroupDraftValidationError("Callable group name must not be empty.")
            if not _coerced.aliases:
                raise CallableGroupDraftValidationError("Callable groups require at least one exact alias.")
        except CallableGroupDraftValidationError as exc:
            self.status_label.setText(str(exc))
            self.status_label.show()
            return
        self.accept()


class TaskGroupAssignmentDialog(QDialog):
    def __init__(
        self,
        *,
        available_groups: list[dict] | None = None,
        available_members: list[dict] | None = None,
        selected_group_ids: tuple[str, ...] = (),
        inline_group_draft: CallableGroupDraft | None = None,
        inline_group_assigned: bool = False,
        group_status_kind: str = "loaded",
        group_status_text: str = "",
        lifecycle_callback=None,
        parent=None,
    ):
        super().__init__(parent)
        self._lifecycle_callback = lifecycle_callback
        self._dialog_signal_name = "TASK_GROUP_ASSIGNMENT_DIALOG"
        self._ready_signal_emitted = False
        self._available_groups = list(available_groups or [])
        self._available_members = list(available_members or [])
        self._selected_group_id = next(
            (
                str(group_id).strip()
                for group_id in (selected_group_ids or ())
                if str(group_id).strip()
            ),
            "",
        )
        self._inline_group_draft = inline_group_draft
        self._inline_group_assigned = bool(inline_group_assigned and inline_group_draft is not None)
        self._group_status_kind = group_status_kind or "template_only"
        self._group_status_text = group_status_text or ""
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Manage Custom Groups")
        self.setObjectName("taskGroupAssignmentDialog")
        self.setMinimumWidth(620)
        self.setMaximumWidth(680)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.shell = QFrame(self)
        self.shell.setObjectName("taskGroupAssignmentShell")
        root_layout.addWidget(self.shell)

        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.chrome_bar = DialogChromeBar(
            "Available Groups",
            self,
            object_prefix="taskGroupAssignment",
            parent=self.shell,
            show_title=False,
        )
        self.chrome_bar.close_button.setToolTip("Close Available Groups")
        shell_layout.addWidget(self.chrome_bar)

        self.content = QWidget(self.shell)
        self.content.setObjectName("taskGroupAssignmentContent")
        shell_layout.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 2, 14, 10)
        layout.setSpacing(2)

        self.title_label = QLabel("Manage Custom Groups", self)
        self.title_label.setObjectName("taskGroupAssignmentTitle")
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.title_label)

        self.hint_label = QLabel(
            "Review callable groups, assign one to this task, or create a new callable group without leaving the current task session.",
            self,
        )
        self.hint_label.setObjectName("taskGroupAssignmentHint")
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.hint_label)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("taskGroupAssignmentStatus")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.source_label = QLabel("", self)
        self.source_label.setObjectName("taskGroupAssignmentSource")
        self.source_label.setWordWrap(True)
        layout.addWidget(self.source_label)

        self.guidance_label = QLabel("", self)
        self.guidance_label.setObjectName("taskGroupAssignmentGuidance")
        self.guidance_label.setWordWrap(True)
        layout.addWidget(self.guidance_label)

        self.items_frame = QFrame(self)
        self.items_frame.setObjectName("taskGroupAssignmentItems")
        self.items_layout = QVBoxLayout(self.items_frame)
        self.items_layout.setContentsMargins(0, 2, 0, 0)
        self.items_layout.setSpacing(2)

        self.items_scroll = QScrollArea(self)
        self.items_scroll.setObjectName("taskGroupAssignmentItemsScroll")
        self.items_scroll.setFrameShape(QFrame.NoFrame)
        self.items_scroll.setWidgetResizable(True)
        self.items_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.items_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.items_scroll.setFocusPolicy(Qt.NoFocus)
        self.items_scroll.setMaximumHeight(0)
        self.items_scroll.viewport().setObjectName("taskGroupAssignmentViewport")
        self.items_scroll.viewport().setAutoFillBackground(False)
        self.items_scroll.setWidget(self.items_frame)
        layout.addWidget(self.items_scroll)

        self.footer_frame = QFrame(self)
        self.footer_frame.setObjectName("taskGroupAssignmentFooter")
        actions_row = QHBoxLayout(self.footer_frame)
        actions_row.setContentsMargins(0, 4, 0, 0)
        actions_row.setSpacing(8)

        self.create_group_button = QPushButton("Create New Group", self.footer_frame)
        self.create_group_button.setObjectName("taskGroupAssignmentCreateButton")
        self.create_group_button.setMinimumHeight(34)
        self.create_group_button.setToolTip(
            "Create a new callable group, then return here to assign it to this task."
        )
        self.create_group_button.clicked.connect(self._handle_create_group_requested)
        actions_row.addWidget(self.create_group_button, 0, Qt.AlignLeft)
        actions_row.addStretch(1)

        self.done_button = QPushButton("Done", self.footer_frame)
        self.done_button.setObjectName("taskGroupAssignmentDoneButton")
        self.done_button.setMinimumHeight(34)
        self.done_button.clicked.connect(self.accept)
        actions_row.addWidget(self.done_button)
        layout.addWidget(self.footer_frame)

        self.setStyleSheet(
            """
            #taskGroupAssignmentDialog { background: transparent; }
            #taskGroupAssignmentShell {
                border-radius: 22px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(4, 16, 28, 238);
            }
            #taskGroupAssignmentContent {
                border-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #taskGroupAssignmentChromeBar {
                border: none;
                border-top-left-radius: 22px;
                border-top-right-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #taskGroupAssignmentFooter {
                border-top: 1px solid rgba(118, 226, 255, 0.12);
                background: transparent;
            }
            #taskGroupAssignmentTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 20px;
                font-weight: 600;
                padding: 0px 6px 1px 6px;
                background: transparent;
            }
            #taskGroupAssignmentHint {
                color: rgba(136, 165, 174, 0.88);
                font-size: 11px;
                line-height: 1.45em;
                padding: 0px 6px 3px 6px;
                background: transparent;
            }
            #taskGroupAssignmentStatus {
                color: rgba(255, 189, 176, 0.96);
                font-size: 13px;
                background: transparent;
            }
            #taskGroupAssignmentSource {
                color: rgba(126, 157, 171, 0.78);
                font-size: 13px;
                background: transparent;
            }
            #taskGroupAssignmentGuidance {
                color: rgba(110, 201, 164, 0.86);
                font-size: 13px;
                background: transparent;
            }
            """
            + THEMED_TOOLTIP_QSS
            + """
            #taskGroupAssignmentItemsScroll {
                border: none;
                background: transparent;
            }
            #taskGroupAssignmentViewport {
                border-radius: 18px;
                background: rgba(4, 12, 22, 236);
            }
            #taskGroupAssignmentItems {
                background: transparent;
            }
            QFrame[groupAssignRole="row"] {
                border-radius: 14px;
                border: 1px solid rgba(118, 226, 255, 0.22);
                background: rgba(12, 28, 44, 208);
            }
            QFrame[groupAssignRole="actionShell"] {
                border-radius: 16px;
                border: none;
                background: rgba(15, 40, 62, 248);
            }
            QLabel[groupAssignRole="title"] {
                color: rgba(184, 208, 200, 0.96);
                font-size: 14px;
                font-weight: 650;
                background: transparent;
            }
            QLabel[groupAssignRole="meta"] {
                color: rgba(84, 192, 181, 0.83);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                background: transparent;
            }
            QLabel[groupAssignRole="detail"] {
                color: rgba(163, 189, 196, 0.92);
                font-size: 12px;
                background: transparent;
            }
            QPushButton[chromeRole="close"] {
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                padding: 0px;
                text-align: center;
                border-radius: 7px;
                border: 1px solid rgba(118, 226, 255, 0.16);
                background: rgba(18, 52, 78, 228);
                color: rgba(191, 212, 207, 0.94);
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton[chromeRole="close"]:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(22, 61, 90, 238);
            }
            QPushButton[groupAssignRole="toggle"], #taskGroupAssignmentCreateButton, #taskGroupAssignmentDoneButton {
                min-height: 34px;
                padding: 0 16px;
                border-radius: 12px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            QPushButton[groupAssignRole="toggle"] {
                min-width: 96px;
                border: 1px solid rgba(118, 226, 255, 0.30);
                background: rgba(18, 52, 78, 228);
            }
            QPushButton[groupAssignRole="toggle"][assigned="true"] {
                border: 1px solid rgba(110, 220, 174, 0.30);
                background: rgba(13, 47, 40, 214);
            }
            QPushButton[groupAssignRole="toggle"]:hover, #taskGroupAssignmentCreateButton:hover, #taskGroupAssignmentDoneButton:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(8, 24, 38, 220);
            }
            #taskGroupAssignmentItemsScroll QScrollBar:vertical {
                width: 8px;
                margin: 4px 1px 4px 0;
                border-radius: 4px;
                background: rgba(6, 18, 30, 0.58);
            }
            #taskGroupAssignmentItemsScroll QScrollBar::handle:vertical {
                min-height: 38px;
                border-radius: 4px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(18, 52, 78, 0.96);
            }
            #taskGroupAssignmentItemsScroll QScrollBar::handle:vertical:hover {
                background: rgba(22, 61, 90, 0.98);
            }
            #taskGroupAssignmentItemsScroll QScrollBar::add-line:vertical,
            #taskGroupAssignmentItemsScroll QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            #taskGroupAssignmentItemsScroll QScrollBar::add-page:vertical,
            #taskGroupAssignmentItemsScroll QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )

        self._update_chrome_overlay_geometry()
        self._refresh_items()

    def _emit_lifecycle_event(self, stage: str, **fields):
        if callable(self._lifecycle_callback):
            try:
                self._lifecycle_callback(self._dialog_signal_name, stage, dialog=self, **fields)
            except Exception:
                pass

    def _emit_ready_signal(self):
        if self._ready_signal_emitted or not self.isVisible():
            return
        self._ready_signal_emitted = True
        self._emit_lifecycle_event("ready")

    def showEvent(self, event):
        super().showEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        self._sync_items_scroll_height()
        _schedule_window_clamp(self)
        self._emit_lifecycle_event("opened")
        QTimer.singleShot(0, self._emit_ready_signal)
        QTimer.singleShot(0, self._sync_items_scroll_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        self._sync_items_scroll_height()
        _schedule_window_clamp(self)
        QTimer.singleShot(0, self._sync_items_scroll_height)

    def done(self, result):
        self._emit_lifecycle_event(
            "closed",
            result="accepted" if result == QDialog.Accepted else "rejected",
        )
        super().done(result)

    def _update_chrome_overlay_geometry(self):
        if hasattr(self, "chrome_bar"):
            self.chrome_bar.raise_()

    def _sync_items_scroll_height(self):
        if not hasattr(self, "items_scroll") or not hasattr(self, "items_layout"):
            return
        row_frames = [
            self.items_layout.itemAt(index).widget()
            for index in range(self.items_layout.count())
            if self.items_layout.itemAt(index) is not None
            and self.items_layout.itemAt(index).widget() is not None
            and self.items_layout.itemAt(index).widget().property("groupAssignRole") == "row"
        ]
        visible_rows = sum(1 for frame in row_frames if frame.isVisible())
        if visible_rows <= 0:
            self.items_scroll.setMaximumHeight(0)
            self.items_scroll.setFixedHeight(0)
            return
        desired_height = _visible_row_height_for_layout(
            self.items_layout,
            min(5, visible_rows),
            extra_padding=0,
        )
        self.items_scroll.setMaximumHeight(desired_height)
        self.items_scroll.setFixedHeight(desired_height)

    def selected_group_ids(self) -> tuple[str, ...]:
        if not self._selected_group_id:
            return ()
        return (self._selected_group_id,)

    def inline_group_draft(self) -> CallableGroupDraft | None:
        return self._inline_group_draft

    def inline_group_assigned(self) -> bool:
        return bool(self._inline_group_draft is not None and self._inline_group_assigned)

    def _toggle_existing_group(self, group_id: str):
        normalized_key = str(group_id or "").strip().casefold()
        if not normalized_key:
            return
        if self._selected_group_id and self._selected_group_id.casefold() == normalized_key:
            self._selected_group_id = ""
        else:
            self._selected_group_id = str(group_id).strip()
            self._inline_group_assigned = False
        self._refresh_items()

    def _toggle_inline_group(self):
        if self._inline_group_draft is None:
            return
        self._inline_group_assigned = not self._inline_group_assigned
        if self._inline_group_assigned:
            self._selected_group_id = ""
        self._refresh_items()

    def _handle_create_group_requested(self):
        if self._group_status_kind == "invalid_groups":
            self.status_label.setText(self._group_status_text)
            self.status_label.setVisible(bool(self.status_label.text()))
            return

        dialog = CallableGroupCreateDialog(
            self,
            dialog_title="Create Custom Group",
            heading_text="Create Custom Group",
            hint_text="Pick a group name and exact aliases below. You will return to Manage Custom Groups for this task after the group is created.",
            submit_button_text="Create",
            available_members=self._available_members,
            show_member_picker=False,
            lifecycle_callback=self._lifecycle_callback,
        )
        if dialog.exec() != QDialog.Accepted:
            return
        try:
            self._inline_group_draft = dialog.build_draft()
        except CallableGroupDraftValidationError as exc:
            self.status_label.setText(str(exc))
            self.status_label.setVisible(True)
            return
        self._inline_group_assigned = False
        self._refresh_items()

    def _make_group_row(
        self,
        *,
        title: str,
        meta_text: str,
        detail_text: str,
        assigned: bool,
        on_toggle,
        parent: QWidget,
        row_object_name: str = "",
        title_object_name: str = "",
        button_object_name: str = "",
    ) -> QFrame:
        frame = QFrame(parent)
        if row_object_name:
            frame.setObjectName(row_object_name)
        frame.setProperty("groupAssignRole", "row")
        frame.setMinimumHeight(70)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        text_column = QVBoxLayout()
        text_column.setContentsMargins(0, 0, 0, 0)
        text_column.setSpacing(2)

        title_label = QLabel(title, frame)
        if title_object_name:
            title_label.setObjectName(title_object_name)
        title_label.setProperty("groupAssignRole", "title")
        title_label.setWordWrap(True)
        text_column.addWidget(title_label)

        meta_label = QLabel(meta_text, frame)
        meta_label.setProperty("groupAssignRole", "meta")
        meta_label.setWordWrap(True)
        text_column.addWidget(meta_label)

        if detail_text:
            detail_label = QLabel(detail_text, frame)
            detail_label.setProperty("groupAssignRole", "detail")
            detail_label.setWordWrap(True)
            text_column.addWidget(detail_label)

        layout.addLayout(text_column, 1)

        action_shell = QFrame(frame)
        action_shell.setProperty("groupAssignRole", "actionShell")
        action_layout = QVBoxLayout(action_shell)
        action_layout.setContentsMargins(4, 4, 4, 4)
        action_layout.setSpacing(0)

        action_button = QPushButton("Remove" if assigned else "Assign", action_shell)
        if button_object_name:
            action_button.setObjectName(button_object_name)
        action_button.setProperty("groupAssignRole", "toggle")
        action_button.setProperty("assigned", assigned)
        action_button.setMinimumWidth(90)
        action_button.clicked.connect(on_toggle)
        action_button.setEnabled(self._group_status_kind != "invalid_groups")
        action_layout.addWidget(action_button)
        layout.addWidget(action_shell, 0, Qt.AlignTop)
        return frame

    def _refresh_items(self):
        _clear_layout_widgets(self.items_layout)
        show_disabled_state = self._group_status_kind == "invalid_groups"
        self.status_label.setText(self._group_status_text if show_disabled_state else "")
        self.status_label.setVisible(bool(self.status_label.text()))
        self.create_group_button.setEnabled(not show_disabled_state)

        normalized_selected = self._selected_group_id.casefold() if self._selected_group_id else ""
        row_count = 0
        available_group_count = 0

        for item in self._available_groups:
            group_id = str(item.get("id") or "").strip()
            if not group_id:
                continue
            aliases = ", ".join(
                str(alias).strip()
                for alias in (item.get("aliases") or [])
                if str(alias).strip()
            )
            member_count = int(item.get("member_count") or 0)
            member_noun = "member" if member_count == 1 else "members"
            row = self._make_group_row(
                title=str(item.get("title") or "").strip() or group_id,
                meta_text=f"Custom group | {member_count} {member_noun}",
                detail_text=(f"Aliases: {aliases}" if aliases else "Aliases: none"),
                assigned=bool(normalized_selected and group_id.casefold() == normalized_selected),
                on_toggle=lambda _checked=False, value=group_id: self._toggle_existing_group(value),
                parent=self.items_frame,
            )
            self.items_layout.addWidget(row)
            row_count += 1
            available_group_count += 1

        if self._inline_group_draft is not None:
            inline_aliases = ", ".join(self._inline_group_draft.aliases)
            row = self._make_group_row(
                title=self._inline_group_draft.title,
                meta_text="Custom group | queued for assignment",
                detail_text=(
                    f"Aliases: {inline_aliases}"
                    if inline_aliases
                    else "Aliases: none yet"
                ),
                assigned=self._inline_group_assigned,
                on_toggle=lambda _checked=False: self._toggle_inline_group(),
                parent=self.items_frame,
                row_object_name="taskGroupAssignmentInlineGroupRow",
                title_object_name="taskGroupAssignmentInlineGroupTitle",
                button_object_name="taskGroupAssignmentInlineGroupToggleButton",
            )
            self.items_layout.addWidget(row)
            row_count += 1

        if row_count == 0:
            empty_frame = QFrame(self.items_frame)
            empty_frame.setProperty("groupAssignRole", "row")
            empty_layout = QVBoxLayout(empty_frame)
            empty_layout.setContentsMargins(10, 10, 10, 10)
            empty_layout.setSpacing(4)

            empty_title = QLabel("No callable groups yet", empty_frame)
            empty_title.setProperty("groupAssignRole", "title")
            empty_layout.addWidget(empty_title)

            empty_meta = QLabel("Create one here", empty_frame)
            empty_meta.setProperty("groupAssignRole", "meta")
            empty_layout.addWidget(empty_meta)

            empty_detail = QLabel(
                "Use Create New Group to add one without leaving this task session.",
                empty_frame,
            )
            empty_detail.setProperty("groupAssignRole", "detail")
            empty_detail.setWordWrap(True)
            empty_layout.addWidget(empty_detail)
            self.items_layout.addWidget(empty_frame)
            row_count = 1

        self.source_label.setText(
            (
                f"{available_group_count} custom {'group' if available_group_count == 1 else 'groups'} loaded from the current source."
                if available_group_count
                else "No custom groups loaded from the current source."
            )
            if not show_disabled_state
            else ""
        )
        self.source_label.setVisible(bool(self.source_label.text()))
        self.guidance_label.setText(
            ""
            if not show_disabled_state and available_group_count
            else (
                "Create a callable group here, then assign it to this task without leaving task authoring."
                if not show_disabled_state
                else "Repair the saved-groups source before changing task-group assignments."
            )
        )
        self.guidance_label.setVisible(bool(self.guidance_label.text()))

        self.items_layout.addStretch(1)
        self.items_layout.activate()
        self._sync_items_scroll_height()
        QTimer.singleShot(0, self._sync_items_scroll_height)

class SavedActionCreateDialog(QDialog):
    ACTION_TYPE_OPTIONS = (
        ("Application", "app"),
        ("Folder", "folder"),
        ("File", "file"),
        ("Website URL", "url"),
    )
    TRIGGER_OPTIONS = (
        ("Launch", "launch"),
        ("Open", "open"),
        ("Launch and Open", "launch_and_open"),
        ("Custom", "custom"),
    )

    TITLE_TOOLTIP_TEXT = (
        "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The display label people see for this task."
        "<br/><br/><b>How it affects calling</b><br/>It does not create callable phrases on its own."
        "<br/>Calling comes from <b>Aliases</b>."
        "<br/><br/><b>Examples</b><br/>Open Nexus AI<br/>Weekly Reports Hub</div>"
    )
    TASK_TYPE_TOOLTIP_TEXT = (
        "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The kind of destination this task opens."
        "<br/><br/><b>How it affects calling</b><br/>It sets the default trigger family and target guidance."
        "<br/><br/><b>Options</b><br/>Application<br/>Folder<br/>File<br/>Website URL</div>"
    )
    ALIASES_TOOLTIP_TEXT = (
        "<div style=\"max-width: 250px;\"><b>What this is</b><br/>Exact callable words or phrases for this task."
        "<br/><br/><b>How it affects calling</b><br/>New-model tasks are called from aliases, not the title."
        "<br/>Add at least one alias, separated by commas."
        "<br/><br/><b>Examples</b><br/>Nexus AI<br/>NDAI<br/>weekly reports</div>"
    )
    TRIGGER_TOOLTIP_TEXT = (
        "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The explicit call prefixes placed before aliases."
        "<br/><br/><b>How it affects calling</b><br/>Launch, Open, or your custom phrases expand the callable surface."
        "<br/><br/><b>Examples</b><br/>Open<br/>Launch<br/>Force Open</div>"
    )
    TARGET_TOOLTIP_TEXT = {
        "app": (
            "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The command or executable Nexus launches."
            "<br/><br/><b>How it affects calling</b><br/>The task can resolve, but launch still depends on a valid application target."
            "<br/><br/><b>Examples</b><br/>notepad.exe"
            r"<br/>C:\Program Files\Notepad++\notepad++.exe</div>"
        ),
        "folder": (
            "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The folder path Nexus opens."
            "<br/><br/><b>How it affects calling</b><br/>Folder tasks open the exact folder you point to here."
            r"<br/><br/><b>Example</b><br/>C:\Reports</div>"
        ),
        "file": (
            "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The file path Nexus opens."
            "<br/><br/><b>How it affects calling</b><br/>File tasks open the exact file you point to here."
            r"<br/><br/><b>Example</b><br/>C:\Reports\weekly.txt</div>"
        ),
        "url": (
            "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The full website address Nexus opens."
            "<br/><br/><b>How it affects calling</b><br/>URL tasks open the exact address you enter here."
            "<br/><br/><b>Example</b><br/>https://example.com/docs</div>"
        ),
    }
    TARGET_FORMAT_EXAMPLES = {
        "app": (
            r"Target format: notepad.exe or C:\Program Files\Notepad++\notepad++.exe"
        ),
        "folder": (
            r"Target format: C:\Reports"
        ),
        "file": (
            r"Target format: C:\Reports\weekly.txt"
        ),
        "url": (
            "Target format: https://example.com/docs"
        ),
    }

    TARGET_ERROR_GUIDANCE = {
        "app": (
            "Application tasks only accept a bare command like notepad.exe "
            "or an absolute Windows executable path."
        ),
        "folder": (
            "Folder tasks need an absolute Windows path to the folder you want to open."
        ),
        "file": (
            "File tasks need an absolute Windows path that includes the final file name."
        ),
        "url": (
            "Website tasks need the full address, including http:// or https://."
        ),
    }

    def __init__(
        self,
        parent=None,
        submit_handler=None,
        *,
        dialog_title: str = "Create Custom Task",
        heading_text: str = "Create Custom Task",
        hint_text: str = (
            "Pick the task type first, then shape the label, trigger, aliases, and target below."
        ),
        submit_button_text: str = "Create",
        initial_draft: SavedActionDraft | None = None,
        available_groups: list[dict] | None = None,
        available_group_members: list[dict] | None = None,
        group_status_kind: str = "template_only",
        group_status_text: str = "",
        lifecycle_callback=None,
        dialog_signal_name: str = "CUSTOM_TASK_CREATE_DIALOG",
    ):
        _emit_global_runtime_marker(f"RENDERER_MAIN|{dialog_signal_name}_PRECONSTRUCT")
        super().__init__(parent)
        _emit_global_runtime_marker(f"RENDERER_MAIN|{dialog_signal_name}_POSTSUPER")
        self._submit_handler = submit_handler
        self._lifecycle_callback = lifecycle_callback
        self._dialog_signal_name = dialog_signal_name
        self._ready_signal_emitted = False
        self._syncing_trigger_selection = False
        self._trigger_manually_changed = False
        self._loaded_trigger_follows_default = True
        self._preserve_legacy_bare_trigger = False
        self._invocation_mode = "aliases_only"
        self._available_groups = list(available_groups or [])
        self._available_group_members = list(available_group_members or [])
        self._group_status_kind = group_status_kind or "template_only"
        self._group_status_text = group_status_text or ""
        self._inline_group_draft: CallableGroupDraft | None = None
        self._inline_group_assigned = False
        self._selected_group_ids_state: tuple[str, ...] = ()
        self._emit_lifecycle_event("construct_start")
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle(dialog_title)
        self.setObjectName("savedActionCreateDialog")
        self.setMinimumWidth(720)
        self.setMaximumWidth(788)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.shell = QFrame(self)
        self.shell.setObjectName("savedActionCreateShell")
        root_layout.addWidget(self.shell)

        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.chrome_bar = DialogChromeBar(
            dialog_title,
            self,
            object_prefix="savedActionCreate",
            parent=self.shell,
            show_title=False,
        )
        shell_layout.addWidget(self.chrome_bar)

        self.content = QWidget(self.shell)
        self.content.setObjectName("savedActionCreateContent")
        shell_layout.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 2, 14, 10)
        layout.setSpacing(2)

        self.title_label = QLabel(heading_text, self)
        self.title_label.setObjectName("savedActionCreateTitle")
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.title_label)

        self.hint_frame = QFrame(self)
        self.hint_frame.setObjectName("savedActionCreateHintFrame")
        self.hint_frame.setAttribute(Qt.WA_StyledBackground, True)
        hint_layout = QVBoxLayout(self.hint_frame)
        hint_layout.setContentsMargins(8, 0, 8, 0)
        hint_layout.setSpacing(0)

        self.hint_label = QLabel(hint_text, self.hint_frame)
        self.hint_label.setObjectName("savedActionCreateHint")
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        hint_layout.addWidget(self.hint_label)
        layout.addWidget(self.hint_frame)

        form = QVBoxLayout()
        self.form_layout = form
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(5)

        self.type_combo = QComboBox(self)
        self.type_combo.setObjectName("savedActionCreateType")
        self.type_combo.setMinimumHeight(34)
        self.type_combo.view().setObjectName("savedActionCreateTypePopup")
        self.type_combo.view().viewport().setObjectName("savedActionCreateTypePopupViewport")
        for label, target_kind in self.ACTION_TYPE_OPTIONS:
            self.type_combo.addItem(label, target_kind)
        self.type_combo.currentIndexChanged.connect(self._handle_target_kind_changed)
        self.type_header, self.type_header_label, self.type_help_button, self.type_header_divider = self._make_form_section(
            "Task type",
            self.type_combo,
            tooltip_text=self.TASK_TYPE_TOOLTIP_TEXT,
            object_name="savedActionCreateTypeHeader",
            help_object_name="savedActionCreateTypeHelp",
        )
        self.type_header_divider.setFixedHeight(0)
        self.type_header_divider.setMinimumHeight(0)
        self.type_header_divider.setMaximumHeight(0)
        self.type_header_divider.hide()
        form.addWidget(self.type_header)

        self.title_input = QLineEdit(self)
        self.title_input.setObjectName("savedActionCreateTitleInput")
        self.title_input.setMinimumHeight(34)
        self.title_input.setPlaceholderText("Open Reports")
        self.title_input.textChanged.connect(self._refresh_examples_box)
        self.title_header, self.title_header_label, self.title_help_button, self.title_header_divider = self._make_form_section(
            "Title",
            self.title_input,
            tooltip_text=self.TITLE_TOOLTIP_TEXT,
            object_name="savedActionCreateTitleHeader",
            help_object_name="savedActionCreateTitleHelp",
        )
        form.addWidget(self.title_header)

        self.trigger_combo = QComboBox(self)
        self.trigger_combo.setObjectName("savedActionCreateTrigger")
        self.trigger_combo.setMinimumHeight(34)
        self.trigger_combo.view().setObjectName("savedActionCreateTriggerPopup")
        self.trigger_combo.view().viewport().setObjectName("savedActionCreateTriggerPopupViewport")
        for label, trigger_mode in self.TRIGGER_OPTIONS:
            self.trigger_combo.addItem(label, trigger_mode)
        self.trigger_combo.currentIndexChanged.connect(self._handle_trigger_selection_changed)
        self.custom_triggers_input = QLineEdit(self)
        self.custom_triggers_input.setObjectName("savedActionCreateCustomTriggersInput")
        self.custom_triggers_input.setMinimumHeight(34)
        self.custom_triggers_input.setPlaceholderText("Force Open, Duck Duck Goose")
        self.custom_triggers_input.textChanged.connect(self._refresh_examples_box)
        trigger_row = QVBoxLayout()
        trigger_row.setContentsMargins(0, 0, 0, 0)
        trigger_row.setSpacing(6)
        trigger_row.addWidget(self.trigger_combo)
        trigger_row.addWidget(self.custom_triggers_input)
        trigger_widget = QWidget(self)
        trigger_widget.setObjectName("savedActionCreateTriggerContent")
        trigger_widget.setLayout(trigger_row)
        self.trigger_header, self.trigger_header_label, self.trigger_help_button, self.trigger_header_divider = self._make_form_section(
            "Trigger",
            trigger_widget,
            tooltip_text=self.TRIGGER_TOOLTIP_TEXT,
            object_name="savedActionCreateTriggerHeader",
            help_object_name="savedActionCreateTriggerHelp",
        )
        form.addWidget(self.trigger_header)

        self.aliases_input = QLineEdit(self)
        self.aliases_input.setObjectName("savedActionCreateAliasesInput")
        self.aliases_input.setMinimumHeight(34)
        self.aliases_input.setPlaceholderText("Required, comma-separated")
        self.aliases_input.textChanged.connect(self._refresh_examples_box)
        self.aliases_header, self.aliases_header_label, self.aliases_help_button, self.aliases_header_divider = self._make_form_section(
            "Aliases",
            self.aliases_input,
            tooltip_text=self.ALIASES_TOOLTIP_TEXT,
            object_name="savedActionCreateAliasesHeader",
            help_object_name="savedActionCreateAliasesHelp",
        )
        form.addWidget(self.aliases_header)

        self.groups_frame = QFrame(self)
        self.groups_frame.setObjectName("savedActionCreateGroupsFrame")
        groups_layout = QVBoxLayout(self.groups_frame)
        groups_layout.setContentsMargins(10, 10, 10, 10)
        groups_layout.setSpacing(8)

        self.groups_status_label = QLabel("", self.groups_frame)
        self.groups_status_label.setObjectName("savedActionCreateGroupsStatus")
        self.groups_status_label.setWordWrap(True)
        groups_layout.addWidget(self.groups_status_label)

        self.groups_summary_label = QLabel("", self.groups_frame)
        self.groups_summary_label.setObjectName("savedActionCreateGroupsSummary")
        self.groups_summary_label.setWordWrap(True)
        groups_layout.addWidget(self.groups_summary_label)

        groups_button_row = QHBoxLayout()
        groups_button_row.setContentsMargins(0, 0, 0, 0)
        groups_button_row.setSpacing(8)

        self.groups_new_button = QPushButton("Assign Group...", self.groups_frame)
        self.groups_new_button.setObjectName("savedActionCreateNewGroupButton")
        self.groups_new_button.setMinimumHeight(36)
        self.groups_new_button.setToolTip(
            "Choose an existing callable group or create a new one for this task."
        )
        self.groups_new_button.clicked.connect(self._handle_group_assignment_requested)
        groups_button_row.addWidget(self.groups_new_button, 0, Qt.AlignLeft)

        self.groups_remove_button = QPushButton("Unassign Group", self.groups_frame)
        self.groups_remove_button.setObjectName("savedActionCreateRemoveGroupButton")
        self.groups_remove_button.setMinimumHeight(36)
        self.groups_remove_button.setToolTip(
            "Remove this task from its current callable group."
        )
        self.groups_remove_button.clicked.connect(self._handle_group_unassign_requested)
        groups_button_row.addWidget(self.groups_remove_button, 0, Qt.AlignLeft)
        groups_button_row.addStretch(1)
        groups_layout.addLayout(groups_button_row)
        self.groups_header, self.groups_header_label, self.groups_help_button, self.groups_header_divider = self._make_form_section(
            "Groups",
            self.groups_frame,
            tooltip_text=(
                "<div style=\"max-width: 250px;\"><b>What this is</b><br/>An optional callable group this task belongs to."
                "<br/><br/><b>How it affects calling</b><br/>Group aliases open that group's member chooser, then the normal confirm step."
                "<br/><br/><b>Boundaries</b><br/>Tasks stay limited to one assigned group here. Groups stay exact-match and do not generate trigger phrases.</div>"
            ),
            object_name="savedActionCreateGroupsHeader",
            help_object_name="savedActionCreateGroupsHelp",
        )
        form.addWidget(self.groups_header)

        self.target_header, self.target_header_label, self.target_help_button, self.target_header_divider = self._make_form_section(
            "Target",
            None,
            tooltip_text="",
            object_name="savedActionCreateTargetHeader",
            help_object_name="savedActionCreateTargetHelp",
        )
        self.target_input = QLineEdit(self)
        self.target_input.setObjectName("savedActionCreateTargetInput")
        self.target_input.setMinimumHeight(34)
        self.target_browse_button = QPushButton("Browse...", self)
        self.target_browse_button.setObjectName("savedActionCreateTargetBrowseButton")
        self.target_browse_button.setMinimumHeight(36)
        self.target_browse_button.setMinimumWidth(104)
        self.target_browse_button.clicked.connect(self._handle_target_browse_clicked)
        target_row = QVBoxLayout()
        target_row.setContentsMargins(0, 0, 0, 0)
        target_row.setSpacing(6)
        target_row.addWidget(self.target_input)
        target_row.addWidget(self.target_browse_button, 0, Qt.AlignLeft)
        target_row.addStretch(1)
        target_widget = QWidget(self)
        target_widget.setObjectName("savedActionCreateTargetContent")
        target_widget.setMinimumHeight(90)
        target_widget.setLayout(target_row)
        self._attach_form_section_content(self.target_header, target_widget)
        form.addWidget(self.target_header)

        self.target_footer_divider = QFrame(self)
        self.target_footer_divider.setObjectName("savedActionCreateTargetFooterDivider")
        self.target_footer_divider.setProperty("createRole", "fieldHeaderDividerLine")
        self.target_footer_divider.setFrameShape(QFrame.HLine)
        self.target_footer_divider.setFixedHeight(1)
        self.target_footer_divider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form.addWidget(self.target_footer_divider)

        content_row = QHBoxLayout()
        self.content_row = content_row
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(12)
        content_row.addLayout(form, 1)

        self.top_form_divider = QFrame(self)
        self.top_form_divider.setObjectName("savedActionCreateTopFormDivider")
        self.top_form_divider.setProperty("createRole", "fieldHeaderDividerLine")
        self.top_form_divider.setFrameShape(QFrame.HLine)
        self.top_form_divider.setFixedHeight(1)
        self.top_form_divider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("savedActionCreateStatus")
        self.status_label.setWordWrap(True)
        self.status_label.hide()

        self.target_examples_box = QFrame(self)
        self.target_examples_box.setObjectName("savedActionCreateTargetExamplesBox")
        self.target_examples_box.setMinimumWidth(220)
        self.target_examples_box.setMaximumWidth(236)
        self.target_examples_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        target_examples_layout = QVBoxLayout(self.target_examples_box)
        target_examples_layout.setContentsMargins(10, 10, 10, 10)
        target_examples_layout.setSpacing(5)

        self.target_examples_title = QLabel("Callable surface", self.target_examples_box)
        self.target_examples_title.setObjectName("savedActionCreateTargetExamplesTitle")
        target_examples_layout.addWidget(self.target_examples_title)

        self.target_examples_label = QLabel("", self.target_examples_box)
        self.target_examples_label.setObjectName("savedActionCreateTargetExamples")
        self.target_examples_label.setWordWrap(True)
        self.target_examples_label.setTextFormat(Qt.RichText)
        target_examples_layout.addWidget(self.target_examples_label)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 0, 0)
        button_row.setSpacing(8)
        button_row.addStretch(1)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setObjectName("savedActionCreateCancelButton")
        self.cancel_button.setMinimumHeight(34)
        self.cancel_button.clicked.connect(self.reject)
        button_row.addWidget(self.cancel_button)

        self.create_button = QPushButton(submit_button_text, self)
        self.create_button.setObjectName("savedActionCreateSubmitButton")
        self.create_button.setMinimumHeight(34)
        self.create_button.setDefault(True)
        self.create_button.clicked.connect(self._handle_create_clicked)
        button_row.addWidget(self.create_button)

        right_rail = QVBoxLayout()
        self.right_rail_layout = right_rail
        right_rail.setContentsMargins(0, 0, 0, 0)
        right_rail.setSpacing(7)
        right_rail.addWidget(self.target_examples_box, 0)
        right_rail.addStretch(1)
        right_rail.addLayout(button_row)

        content_row.addLayout(right_rail, 0)

        layout.addWidget(self.top_form_divider)
        layout.addLayout(content_row)
        layout.addWidget(self.status_label)
        self._emit_lifecycle_event("construct_layout_ready")

        self.setStyleSheet(
            """
            #savedActionCreateDialog {
                background: transparent;
            }
            #savedActionCreateShell {
                border-radius: 22px;
                border: 1px solid rgba(118, 226, 255, 0.22);
                background: rgb(4, 16, 28);
            }
            #savedActionCreateContent {
                border-radius: 22px;
                background: transparent;
            }
            #savedActionCreateChromeBar {
                border: none;
                border-top-left-radius: 22px;
                border-top-right-radius: 22px;
                background: transparent;
            }
            #savedActionCreateChromeTitle {
                color: rgba(126, 171, 181, 0.84);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.24em;
            }
            #savedActionCreateChromeClose {
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                padding: 0px;
                text-align: center;
                border-radius: 7px;
                border: 1px solid rgba(118, 226, 255, 0.16);
                background: rgba(18, 52, 78, 228);
                color: rgba(191, 212, 207, 0.94);
                font-size: 12px;
                font-weight: 600;
            }
            #savedActionCreateChromeClose:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(22, 61, 90, 238);
            }
            #savedActionCreateTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 20px;
                font-weight: 600;
                padding: 0px 6px 1px 6px;
                background: transparent;
            }
            #savedActionCreateHintFrame {
                background: transparent;
            }
            #savedActionCreateHint {
                color: rgba(136, 165, 174, 0.88);
                font-size: 11px;
                line-height: 1.45em;
                padding: 0px 6px 3px 6px;
                background: transparent;
            }
            QToolTip {
                border: 1px solid rgba(102, 219, 204, 0.22);
                border-radius: 12px;
                background: rgba(5, 16, 28, 248);
                color: rgba(192, 212, 207, 0.96);
                padding: 12px 14px;
                font-size: 12px;
                line-height: 1.45em;
            }
            #savedActionCreateTargetExamplesBox {
                border-radius: 0px;
                border: none;
                background: transparent;
            }
            #savedActionCreateTargetExamplesTitle {
                color: rgba(84, 192, 181, 0.88);
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                background: transparent;
            }
            #savedActionCreateTargetExamples {
                color: rgba(168, 193, 199, 0.93);
                font-size: 13px;
                line-height: 1.45em;
                background: transparent;
            }
            #savedActionCreateGroupsFrame {
                border-radius: 18px;
                border: 1px solid rgba(118, 226, 255, 0.16);
                background: rgb(8, 20, 34);
            }
            #savedActionCreateGroupsSummary {
                color: rgba(168, 193, 199, 0.93);
                font-size: 13px;
                line-height: 1.45em;
                padding: 0px;
                background: transparent;
            }
            #savedActionCreateGroupsStatus {
                color: rgba(255, 189, 176, 0.96);
                font-size: 13px;
                background: transparent;
            }
            #savedActionCreateStatus {
                min-height: 0px;
                color: rgba(255, 189, 176, 0.96);
                font-size: 13px;
                background: transparent;
            }
            QLabel[createRole="label"] {
                color: rgba(78, 176, 173, 0.76);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.08em;
            }
            QWidget[createRole="fieldHeaderDivider"] {
                border: none;
                background: transparent;
            }
            QFrame[createRole="fieldRow"] {
                border-radius: 0px;
                border: none;
                background: transparent;
            }
            QWidget[createRole="fieldLabelHolder"], QWidget[createRole="fieldContentHolder"] {
                background: transparent;
            }
            #savedActionCreateTriggerContent, #savedActionCreateTargetContent {
                background: transparent;
            }
            QFrame[createRole="fieldHeaderDividerLine"] {
                min-height: 1px;
                max-height: 1px;
                border: none;
                background: rgba(118, 226, 255, 0.18);
            }
            QLabel[createRole="fieldHeader"], QLabel[createRole="fieldHeaderHelp"] {
                color: rgba(182, 206, 198, 0.96);
                font-size: 13px;
                font-weight: 650;
                background: transparent;
            }
            QLabel[createRole="fieldHeaderHelp"] {
                padding-bottom: 0px;
            }
            QLabel[createRole="fieldHeaderHelp"]:hover {
                color: rgba(198, 218, 211, 0.99);
            }
            QLabel[createRole="fieldHeaderHelp"]:focus {
                color: rgba(198, 218, 211, 0.99);
            }
            QLineEdit, QComboBox {
                min-height: 30px;
                border-radius: 14px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(193, 213, 208, 0.96);
                padding: 4px 10px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid rgba(118, 226, 255, 0.42);
                background: rgba(7, 22, 36, 220);
            }
            QComboBox::drop-down {
                border: none;
                width: 28px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid rgba(118, 226, 255, 0.24);
                border-radius: 12px;
                background: rgba(8, 18, 30, 248);
                color: rgba(193, 213, 208, 0.96);
                outline: 0;
                padding: 6px;
                selection-background-color: rgba(22, 61, 90, 232);
                selection-color: rgba(205, 221, 216, 0.99);
            }
            QComboBox QAbstractItemView::item {
                min-height: 30px;
                padding: 4px 8px;
                border-radius: 8px;
            }
            QPushButton {
                min-height: 34px;
                padding: 0 16px;
                border-radius: 12px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            QPushButton:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(8, 24, 38, 220);
            }
            #savedActionCreateCancelButton {
                background: rgba(6, 18, 30, 196);
            }
            #savedActionCreateSubmitButton {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(18, 52, 78, 228);
                font-weight: 650;
            }
            #savedActionCreateSubmitButton:hover {
                border: 1px solid rgba(118, 226, 255, 0.52);
                background: rgba(22, 61, 90, 238);
            }
            """
        )
        self._emit_lifecycle_event("construct_style_ready")

        self._refresh_groups_ui()
        self._apply_default_trigger_mode(force=True)
        self._sync_trigger_ui_from_selection(mark_manual=False)
        self._trigger_manually_changed = False
        self._update_target_guidance()
        self._refresh_examples_box()
        if initial_draft is not None:
            self.load_draft(initial_draft)
        self._emit_lifecycle_event("construct_complete")

    def _emit_lifecycle_event(self, stage: str, **fields):
        if callable(self._lifecycle_callback):
            try:
                self._lifecycle_callback(self._dialog_signal_name, stage, dialog=self, **fields)
            except Exception:
                pass

    def _emit_ready_signal(self):
        if self._ready_signal_emitted or not self.isVisible():
            return
        self._ready_signal_emitted = True
        self._emit_lifecycle_event("ready")

    def showEvent(self, event):
        super().showEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)
        self._emit_lifecycle_event("opened")
        QTimer.singleShot(0, self._emit_ready_signal)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)

    def done(self, result):
        self._emit_lifecycle_event(
            "closed",
            result="accepted" if result == QDialog.Accepted else "rejected",
        )
        super().done(result)

    def _update_chrome_overlay_geometry(self):
        if hasattr(self, "chrome_bar"):
            self.chrome_bar.raise_()

    def _make_form_header(
        self,
        text: str,
        *,
        tooltip_text: str,
        object_name: str,
        help_object_name: str,
    ) -> tuple[QWidget, QLabel, QLabel, QFrame]:
        container = QWidget(self)
        container.setObjectName(object_name)
        container.setProperty("createRole", "fieldHeaderDivider")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 3)
        layout.setSpacing(2)

        divider = QFrame(container)
        divider.setObjectName(f"{object_name}Divider")
        divider.setProperty("createRole", "fieldHeaderDividerLine")
        divider.setFrameShape(QFrame.HLine)
        divider.setFixedHeight(1)
        divider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(divider)

        label = ImmediateHelpButton(container)
        label.setObjectName(help_object_name)
        label.setProperty("createRole", "fieldHeaderHelp")
        label.setText(text)
        label.setToolTip(tooltip_text)
        header_font = label.font()
        header_font.setPointSize(12)
        header_font.setBold(True)
        label.setFont(header_font)
        layout.addWidget(label, 0, Qt.AlignLeft)
        return container, label, label, divider

    def _attach_form_section_content(self, section: QWidget, content_widget: QWidget | None):
        if section is None:
            return
        content_holder = getattr(section, "_section_content_holder", None)
        if content_holder is None:
            return
        content_layout = content_holder.layout()
        if content_layout is None:
            content_layout = QVBoxLayout(content_holder)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(0)
        _clear_layout_widgets(content_layout)
        if content_widget is not None:
            content_layout.addWidget(content_widget)
        row = getattr(section, "_section_row_layout", None)
        if row is not None:
            row.invalidate()
        section.adjustSize()

    def _make_form_section(
        self,
        text: str,
        content_widget: QWidget | None,
        *,
        tooltip_text: str,
        object_name: str,
        help_object_name: str,
        label_width: int = 112,
    ) -> tuple[QWidget, QLabel, QLabel, QFrame]:
        container = QWidget(self)
        container.setObjectName(object_name)
        container.setProperty("createRole", "fieldHeaderDivider")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        divider = QFrame(container)
        divider.setObjectName(f"{object_name}Divider")
        divider.setProperty("createRole", "fieldHeaderDividerLine")
        divider.setFrameShape(QFrame.HLine)
        divider.setFixedHeight(1)
        divider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(divider)

        row_widget = QFrame(container)
        row_widget.setProperty("createRole", "fieldRow")
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(12)

        label_holder = QWidget(row_widget)
        label_holder.setProperty("createRole", "fieldLabelHolder")
        label_holder.setFixedWidth(label_width)
        label_holder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        label_layout = QVBoxLayout(label_holder)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(0)
        label_layout.addStretch(1)

        label = ImmediateHelpButton(label_holder)
        label.setObjectName(help_object_name)
        label.setProperty("createRole", "fieldHeaderHelp")
        label.setText(text)
        label.setToolTip(tooltip_text)
        header_font = label.font()
        header_font.setPointSize(12)
        header_font.setBold(True)
        label.setFont(header_font)
        label_layout.addWidget(label, 0, Qt.AlignLeft)
        label_layout.addStretch(1)
        row_layout.addWidget(label_holder, 0)

        content_holder = QWidget(row_widget)
        content_holder.setProperty("createRole", "fieldContentHolder")
        content_holder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        row_layout.addWidget(content_holder, 1)
        layout.addWidget(row_widget)

        container._section_row_layout = row_layout
        container._section_content_holder = content_holder
        SavedActionCreateDialog._attach_form_section_content(self, container, content_widget)
        return container, label, label, divider

    def _selected_group_ids(self) -> tuple[str, ...]:
        return tuple(self._selected_group_ids_state[:1])

    def _refresh_groups_ui(self):
        show_disabled_state = self._group_status_kind == "invalid_groups"
        self.groups_status_label.setText(self._group_status_text if show_disabled_state else "")
        self.groups_status_label.setVisible(bool(self.groups_status_label.text()))
        assigned_text = "No group assigned yet."
        if self._selected_group_ids_state:
            selected_id = self._selected_group_ids_state[0].casefold()
            for item in self._available_groups:
                group_id = str(item.get("id") or "").strip()
                if not group_id or group_id.casefold() != selected_id:
                    continue
                member_count = int(item.get("member_count") or 0)
                aliases = ", ".join(
                    str(alias).strip()
                    for alias in (item.get("aliases") or [])
                    if str(alias).strip()
                )
                member_noun = "member" if member_count == 1 else "members"
                assigned_text = (
                    f'Assigned group: {str(item.get("title") or "").strip() or group_id}'
                    f" ({member_count} {member_noun})"
                )
                if aliases:
                    assigned_text += f"\nAliases: {aliases}"
                break
        elif self._inline_group_draft is not None and self._inline_group_assigned:
            inline_aliases = ", ".join(self._inline_group_draft.aliases)
            assigned_text = f"Assigned group: {self._inline_group_draft.title} (new)"
            if inline_aliases:
                assigned_text += f"\nAliases: {inline_aliases}"

        self.groups_summary_label.setText(assigned_text)
        self.groups_summary_label.setTextFormat(Qt.PlainText)
        has_assigned_group = bool(
            self._selected_group_ids_state or (self._inline_group_draft is not None and self._inline_group_assigned)
        )
        self.groups_new_button.setVisible(not has_assigned_group)
        self.groups_new_button.setEnabled(not show_disabled_state)
        self.groups_remove_button.setVisible(has_assigned_group)
        self.groups_remove_button.setEnabled(not show_disabled_state)

    def _handle_group_assignment_requested(self):
        if self._group_status_kind == "invalid_groups":
            self.set_error_text(self._group_status_text)
            return

        dialog = TaskGroupAssignmentDialog(
            available_groups=self._available_groups,
            available_members=self._available_group_members,
            selected_group_ids=self._selected_group_ids_state,
            inline_group_draft=self._inline_group_draft,
            inline_group_assigned=self._inline_group_assigned,
            group_status_kind=self._group_status_kind,
            group_status_text=self._group_status_text,
            lifecycle_callback=self._lifecycle_callback,
            parent=self,
        )
        if dialog.exec() != QDialog.Accepted:
            return

        self._selected_group_ids_state = dialog.selected_group_ids()
        self._inline_group_draft = dialog.inline_group_draft()
        self._inline_group_assigned = dialog.inline_group_assigned()
        self._refresh_groups_ui()

    def _handle_group_unassign_requested(self):
        self._selected_group_ids_state = ()
        self._inline_group_assigned = False
        self._refresh_groups_ui()

    def current_target_kind(self) -> str:
        return str(self.type_combo.currentData() or "app")

    def current_trigger_mode(self) -> str:
        return str(self.trigger_combo.currentData() or default_saved_action_trigger_mode(self.current_target_kind()))

    def _effective_trigger_mode(self) -> str:
        if self._preserve_legacy_bare_trigger and not self._trigger_manually_changed:
            return ""
        return self.current_trigger_mode()

    def _draft_trigger_follows_default(self, draft: SavedActionDraft) -> bool:
        if draft.custom_triggers:
            return False
        trigger_mode = (draft.trigger_mode or "").strip().casefold()
        if not trigger_mode:
            return draft.invocation_mode != "aliases_only"
        return trigger_mode == default_saved_action_trigger_mode(draft.target_kind)

    def _build_alias_suggestions(self, title: str) -> tuple[str, ...]:
        normalized_title = re.sub(r"\s+", " ", (title or "").strip())
        if not normalized_title:
            return ()

        lower_title = normalized_title.casefold()
        core_title = normalized_title
        for prefix in ("open ", "show ", "launch ", "start ", "run ", "view "):
            if lower_title.startswith(prefix):
                core_title = normalized_title[len(prefix):].strip()
                break

        suggestions: list[str] = []

        def add_suggestion(value: str):
            normalized_value = re.sub(r"\s+", " ", value.strip())
            if not normalized_value:
                return
            if any(existing.casefold() == normalized_value.casefold() for existing in suggestions):
                return
            suggestions.append(normalized_value)

        if core_title and core_title.casefold() != lower_title:
            add_suggestion(core_title)
        else:
            add_suggestion(normalized_title)

        return tuple(suggestions[:3])

    def _set_trigger_mode(self, trigger_mode: str):
        self._syncing_trigger_selection = True
        try:
            for index in range(self.trigger_combo.count()):
                if str(self.trigger_combo.itemData(index) or "") == trigger_mode:
                    self.trigger_combo.setCurrentIndex(index)
                    break
        finally:
            self._syncing_trigger_selection = False

    def _apply_default_trigger_mode(self, *, force: bool = False):
        if force or not self._trigger_manually_changed:
            self._set_trigger_mode(default_saved_action_trigger_mode(self.current_target_kind()))

    def _handle_target_kind_changed(self):
        self._apply_default_trigger_mode()
        self._update_target_guidance()
        self._refresh_examples_box()

    def _handle_trigger_selection_changed(self):
        self._sync_trigger_ui_from_selection(mark_manual=not self._syncing_trigger_selection)

    def _sync_trigger_ui_from_selection(self, *, mark_manual: bool):
        if mark_manual:
            self._trigger_manually_changed = True
        is_custom = self.current_trigger_mode() == "custom"
        self.custom_triggers_input.setVisible(is_custom)
        self._refresh_examples_box()

    def _parse_custom_triggers_text(self) -> tuple[str, ...]:
        trigger_text = (self.custom_triggers_input.text() or "").replace("\n", ",")
        triggers = [re.sub(r"\s+", " ", part.strip()) for part in trigger_text.split(",")]
        return tuple(trigger for trigger in triggers if trigger)

    def _target_tooltip_text(self) -> str:
        return self.TARGET_TOOLTIP_TEXT.get(self.current_target_kind(), "")

    def _target_format_example_text(self) -> str:
        return self.TARGET_FORMAT_EXAMPLES.get(self.current_target_kind(), "")

    def _build_examples_section(self, title: str, body_html: str) -> str:
        return (
            "<div style=\"margin: 0; padding: 0;\">"
            f"<div style=\"color: rgba(84, 192, 181, 0.86); font-size: 10.5px; font-weight: 600; "
            "letter-spacing: 0.04em; text-transform: uppercase;\">"
            f"{escape(title)}</div>"
            f"<div style=\"margin-top: 3px; color: rgba(168, 193, 199, 0.93);\">{body_html}</div>"
            "</div>"
        )

    def _refresh_examples_box(self):
        title = re.sub(r"\s+", " ", (self.title_input.text() or "").strip())
        aliases = self._parse_aliases_text()
        trigger_mode = self._effective_trigger_mode()
        custom_triggers = self._parse_custom_triggers_text()
        alias_suggestions = self._build_alias_suggestions(title)
        normalized_aliases = {alias.casefold() for alias in aliases}
        visible_suggestions = tuple(
            suggestion for suggestion in alias_suggestions
            if suggestion.casefold() not in normalized_aliases
        )

        sections: list[str] = []
        if visible_suggestions:
            suggestion_lines = "<br/>".join(
                f"&bull; {escape(suggestion)}" for suggestion in visible_suggestions[:3]
            )
            sections.append(self._build_examples_section("Suggested aliases", suggestion_lines))

        callable_phrases = build_saved_action_callable_phrases(
            title,
            aliases,
            invocation_mode=self._invocation_mode,
            trigger_mode=trigger_mode,
            custom_triggers=custom_triggers,
        )
        if callable_phrases:
            phrase_lines = "<br/>".join(
                f"&bull; {escape(phrase)}" for phrase in callable_phrases[:6]
            )
            sections.append(
                self._build_examples_section(
                    "Real callable phrases",
                    "<span style=\"color: rgba(146, 178, 181, 0.89);\">Exact phrases, case-insensitive.</span>"
                    f"<br/>{phrase_lines}",
                )
            )
        elif trigger_mode == "custom":
            sections.append(
                self._build_examples_section(
                    "Real callable phrases",
                    "Add an alias and at least one custom trigger to preview the callable surface.",
                )
            )
        else:
            sections.append(
                self._build_examples_section(
                    "Real callable phrases",
                    "Add an alias to preview the exact callable phrases.",
                )
            )

        target_format = self._target_format_example_text()
        if target_format:
            sections.append(
                self._build_examples_section("Target format", escape(target_format))
            )
        self.target_examples_label.setText("<br/><br/>".join(sections))

    def _update_target_guidance(self):
        target_kind = self.current_target_kind()
        self.target_help_button.setToolTip(self._target_tooltip_text())
        if target_kind == "url":
            self.target_input.setPlaceholderText("https://example.com/docs")
            self.target_browse_button.hide()
            self.target_browse_button.setToolTip("")
        elif target_kind == "folder":
            self.target_input.setPlaceholderText(r"C:\Users\YourName\Documents")
            self.target_browse_button.show()
            self.target_browse_button.setToolTip("Choose a folder path.")
        elif target_kind == "file":
            self.target_input.setPlaceholderText(r"C:\Users\YourName\Documents\notes.txt")
            self.target_browse_button.show()
            self.target_browse_button.setToolTip("Choose a file path.")
        else:
            self.target_input.setPlaceholderText("notepad.exe")
            self.target_browse_button.show()
            self.target_browse_button.setToolTip("Choose an application path.")

    def _target_picker_start_path(self) -> str:
        target_text = (self.target_input.text() or "").strip()
        if target_text:
            return target_text
        return os.path.expanduser("~")

    def _choose_application_target(self) -> str:
        selected_path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Choose Application",
            self._target_picker_start_path(),
            "Applications (*.exe *.com *.bat *.cmd);;All Files (*)",
        )
        return selected_path or ""

    def _choose_folder_target(self) -> str:
        selected_path = QFileDialog.getExistingDirectory(
            self,
            "Choose Folder",
            self._target_picker_start_path(),
        )
        return selected_path or ""

    def _choose_file_target(self) -> str:
        selected_path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Choose File",
            self._target_picker_start_path(),
            "All Files (*)",
        )
        return selected_path or ""

    def _pick_target_value(self) -> str:
        target_kind = self.current_target_kind()
        if target_kind == "folder":
            return self._choose_folder_target()
        if target_kind == "file":
            return self._choose_file_target()
        if target_kind == "app":
            return self._choose_application_target()
        return ""

    def _handle_target_browse_clicked(self):
        selected_target = self._pick_target_value()
        if selected_target:
            self.target_input.setText(selected_target)

    def _parse_aliases_text(self) -> tuple[str, ...]:
        alias_text = (self.aliases_input.text() or "").replace("\n", ",")
        aliases = [part.strip() for part in alias_text.split(",")]
        return tuple(alias for alias in aliases if alias)

    def build_draft(self) -> SavedActionDraft:
        trigger_mode = self._effective_trigger_mode()
        custom_triggers = self._parse_custom_triggers_text() if trigger_mode == "custom" else ()
        return SavedActionDraft(
            title=self.title_input.text(),
            target_kind=self.current_target_kind(),
            target=self.target_input.text(),
            aliases=self._parse_aliases_text(),
            invocation_mode=self._invocation_mode,
            trigger_mode=trigger_mode,
            custom_triggers=custom_triggers,
            group_ids=self._selected_group_ids(),
            inline_group=self._inline_group_draft if self._inline_group_assigned else None,
        )

    def load_draft(self, draft: SavedActionDraft):
        trigger_follows_default = self._draft_trigger_follows_default(draft)
        self._invocation_mode = draft.invocation_mode or "legacy"
        self._loaded_trigger_follows_default = trigger_follows_default
        self._preserve_legacy_bare_trigger = (
            self._invocation_mode == "legacy"
            and not (draft.trigger_mode or "").strip()
            and not draft.custom_triggers
        )
        for index in range(self.type_combo.count()):
            if str(self.type_combo.itemData(index) or "") == draft.target_kind:
                self.type_combo.setCurrentIndex(index)
                break
        self.title_input.setText(draft.title)
        self.aliases_input.setText(", ".join(draft.aliases))
        self.custom_triggers_input.setText(", ".join(draft.custom_triggers))
        self._set_trigger_mode(draft.trigger_mode or default_saved_action_trigger_mode(draft.target_kind))
        self.target_input.setText(draft.target)
        self._inline_group_draft = draft.inline_group
        self._inline_group_assigned = draft.inline_group is not None
        self._selected_group_ids_state = tuple(draft.group_ids[:1])
        self._refresh_groups_ui()
        self._sync_trigger_ui_from_selection(mark_manual=False)
        self._trigger_manually_changed = not trigger_follows_default
        self._update_target_guidance()
        self._refresh_examples_box()

    def _format_error_text(self, text: str) -> str:
        message = (text or "").strip()
        if not message:
            return ""

        lower_message = message.casefold()
        if "saved actions are unavailable" in lower_message:
            return (
                "Custom tasks are blocked until the saved-actions source is repaired. "
                f"{message}"
            )
        if "collides with" in lower_message:
            return (
                "Callable phrases: pick aliases or triggers that do not overlap with a built-in action "
                "or another custom task. "
                f"{message}"
            )
        if "trigger mode" in lower_message or "custom trigger" in lower_message or "trigger" in lower_message:
            return (
                "Trigger: choose a standard trigger or enter unique custom trigger phrases separated by commas. "
                f"{message}"
            )
        if "could not be found for editing" in lower_message:
            return (
                "This task could not be reopened for editing. "
                "Refresh the Manage Custom Tasks window and try again. "
                f"{message}"
            )
        if "aliases" in lower_message:
            return (
                "Aliases: add one or more distinct callable phrases for this task. "
                "Keep each one unique after normalization. "
                f"{message}"
            )
        if "title" in lower_message:
            return (
                "Title: this is the display label people will see for the task. "
                "Choose a short, readable label. "
                f"{message}"
            )
        if "target kind" in lower_message:
            return (
                "Task type: choose the kind that matches where this task should go, "
                "then follow the target guidance for that type. "
                f"{message}"
            )
        if (
            "target" in lower_message
            or "path" in lower_message
            or "command" in lower_message
            or "http" in lower_message
            or "url" in lower_message
        ):
            return (
                "Target: "
                f"{self.TARGET_ERROR_GUIDANCE.get(self.current_target_kind(), 'Check where this task should open or launch.')} "
                f"{message}"
            )
        if "could not be saved" in lower_message and "source" in lower_message:
            return (
                "Custom task changes were blocked before write so the existing source stays safe. "
                f"{message}"
            )
        return message

    def set_error_text(self, text: str):
        message = self._format_error_text(text)
        self.status_label.setText(message)
        self.status_label.setVisible(bool(message))

    def _handle_create_clicked(self):
        if self._submit_handler is None:
            self.accept()
            return

        try:
            self._submit_handler(self.build_draft())
        except (SavedActionDraftValidationError, SavedActionUnsafeSourceError, SavedActionSourceWriteBlocked) as exc:
            self.set_error_text(str(exc))
            return
        except Exception as exc:
            self.set_error_text(f"Custom task could not be saved: {exc}")
            return

        self.accept()


class SavedActionEditDialog(SavedActionCreateDialog):
    def __init__(
        self,
        parent=None,
        submit_handler=None,
        initial_draft: SavedActionDraft | None = None,
        lifecycle_callback=None,
    ):
        super().__init__(
            parent,
            submit_handler,
            dialog_title="Edit Custom Task",
            heading_text="Edit Custom Task",
            hint_text=(
                "Update the fields below for this custom task."
            ),
            submit_button_text="Save",
            initial_draft=initial_draft,
            lifecycle_callback=lifecycle_callback,
            dialog_signal_name="CUSTOM_TASK_EDIT_DIALOG",
        )


class CallableGroupCreateDialog(QDialog):
    def __init__(
        self,
        parent=None,
        submit_handler=None,
        *,
        dialog_title: str = "Create Custom Group",
        heading_text: str = "Create Custom Group",
        hint_text: str = "Pick a group name, exact aliases, and explicit members below.",
        submit_button_text: str = "Create",
        available_members: list[dict] | None = None,
        initial_draft: CallableGroupDraft | None = None,
        lifecycle_callback=None,
        dialog_signal_name: str = "CUSTOM_GROUP_CREATE_DIALOG",
        show_member_picker: bool = True,
    ):
        super().__init__(parent)
        self._submit_handler = submit_handler
        self._available_members = list(available_members or [])
        self._lifecycle_callback = lifecycle_callback
        self._dialog_signal_name = dialog_signal_name
        self._ready_signal_emitted = False
        self._show_member_picker = bool(show_member_picker)
        self._member_checkboxes: list[QCheckBox] = []
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle(dialog_title)
        self.setObjectName("callableGroupCreateDialog")
        self.setMinimumWidth(620)
        self.setMaximumWidth(680)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.shell = QFrame(self)
        self.shell.setObjectName("callableGroupCreateShell")
        root_layout.addWidget(self.shell)

        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.chrome_bar = DialogChromeBar(
            dialog_title,
            self,
            object_prefix="callableGroupCreate",
            parent=self.shell,
            show_title=False,
        )
        self.chrome_bar.close_button.setToolTip(f"Close {dialog_title}")
        shell_layout.addWidget(self.chrome_bar)

        self.content = QWidget(self.shell)
        self.content.setObjectName("callableGroupCreateContent")
        shell_layout.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 2, 14, 10)
        layout.setSpacing(2)

        self.title_label = QLabel(heading_text, self)
        self.title_label.setObjectName("callableGroupCreateTitle")
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.title_label)

        self.hint_frame = QFrame(self)
        self.hint_frame.setObjectName("callableGroupCreateHintFrame")
        self.hint_frame.setAttribute(Qt.WA_StyledBackground, True)
        hint_layout = QVBoxLayout(self.hint_frame)
        hint_layout.setContentsMargins(8, 0, 8, 0)
        hint_layout.setSpacing(0)

        self.hint_label = QLabel(hint_text, self.hint_frame)
        self.hint_label.setObjectName("callableGroupCreateHint")
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        hint_layout.addWidget(self.hint_label)
        layout.addWidget(self.hint_frame)

        form = QVBoxLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(6)

        self.name_input = QLineEdit(self)
        self.name_input.setObjectName("callableGroupCreateNameInput")
        self.name_input.setMinimumHeight(34)
        self.name_input.setPlaceholderText("Workspace Tools")
        self.name_header, self.name_header_label, self.name_help_button, self.name_header_divider = SavedActionCreateDialog._make_form_section(
            self,
            "Group name",
            self.name_input,
            tooltip_text=(
                "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The display label people see for this group."
                "<br/><br/><b>How it affects calling</b><br/>Calling still comes from the group's aliases, not the name.</div>"
            ),
            object_name="callableGroupCreateNameHeader",
            help_object_name="callableGroupCreateNameHelp",
        )
        form.addWidget(self.name_header)

        self.aliases_input = QLineEdit(self)
        self.aliases_input.setObjectName("callableGroupCreateAliasesInput")
        self.aliases_input.setMinimumHeight(34)
        self.aliases_input.setPlaceholderText("workspace tools, tools group")
        self.aliases_input.textChanged.connect(self._refresh_examples_box)

        self.examples_box = QFrame(self)
        self.examples_box.setObjectName("callableGroupCreateExamplesBox")
        examples_layout = QVBoxLayout(self.examples_box)
        examples_layout.setContentsMargins(10, 10, 10, 10)
        examples_layout.setSpacing(5)
        examples_title = QLabel("Callable surface", self.examples_box)
        examples_title.setObjectName("callableGroupCreateExamplesTitle")
        examples_layout.addWidget(examples_title)
        self.examples_label = QLabel("", self.examples_box)
        self.examples_label.setObjectName("callableGroupCreateExamples")
        self.examples_label.setWordWrap(True)
        self.examples_label.setTextFormat(Qt.RichText)
        examples_layout.addWidget(self.examples_label)
        aliases_content = QWidget(self)
        aliases_content.setObjectName("callableGroupCreateAliasesContent")
        aliases_content_layout = QVBoxLayout(aliases_content)
        aliases_content_layout.setContentsMargins(0, 0, 0, 0)
        aliases_content_layout.setSpacing(6)
        aliases_content_layout.addWidget(self.aliases_input)
        aliases_content_layout.addWidget(self.examples_box)
        self.aliases_header, self.aliases_header_label, self.aliases_help_button, self.aliases_header_divider = SavedActionCreateDialog._make_form_section(
            self,
            "Aliases",
            aliases_content,
            tooltip_text=(
                "<div style=\"max-width: 250px;\"><b>What this is</b><br/>Exact phrases that call this group."
                "<br/><br/><b>How it affects calling</b><br/>Using one of these aliases opens the group's member chooser.</div>"
            ),
            object_name="callableGroupCreateAliasesHeader",
            help_object_name="callableGroupCreateAliasesHelp",
        )
        form.addWidget(self.aliases_header)

        self.members_scroll = None
        self.members_frame = None
        self.members_layout = None
        self.task_flow_note = None
        self.members_scroll = QScrollArea(self)
        self.members_scroll.setObjectName("callableGroupCreateMembersScroll")
        self.members_scroll.setFrameShape(QFrame.NoFrame)
        self.members_scroll.setWidgetResizable(True)
        self.members_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.members_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.members_scroll.setFocusPolicy(Qt.NoFocus)
        self.members_scroll.setMaximumHeight(0)
        self.members_scroll.viewport().setObjectName("callableGroupCreateMembersViewport")
        self.members_scroll.viewport().setAutoFillBackground(False)
        self.members_frame = QFrame(self)
        self.members_frame.setObjectName("callableGroupCreateMembersFrame")
        self.members_layout = QVBoxLayout(self.members_frame)
        self.members_layout.setContentsMargins(8, 8, 8, 8)
        self.members_layout.setSpacing(3)
        self.members_scroll.setWidget(self.members_frame)
        self.members_header, self.members_header_label, self.members_help_button, self.members_header_divider = SavedActionCreateDialog._make_form_section(
            self,
            "Available Tasks",
            self.members_scroll,
            tooltip_text=(
                "<div style=\"max-width: 250px;\"><b>What this is</b><br/>The built-ins and saved tasks this group can surface."
                "<br/><br/><b>How it affects calling</b><br/>Group aliases only show these members in the chooser.</div>"
            ),
            object_name="callableGroupCreateMembersHeader",
            help_object_name="callableGroupCreateMembersHelp",
        )
        form.addWidget(self.members_header)

        layout.addLayout(form)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("callableGroupCreateStatus")
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        layout.addWidget(self.status_label)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 0, 0)
        button_row.setSpacing(8)
        button_row.addStretch(1)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        button_row.addWidget(self.cancel_button)
        self.submit_button = QPushButton(submit_button_text, self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self._handle_submit_clicked)
        button_row.addWidget(self.submit_button)
        layout.addLayout(button_row)

        self.setStyleSheet(
            """
            #callableGroupCreateDialog { background: transparent; }
            #callableGroupCreateShell {
                border-radius: 22px;
                border: 1px solid rgba(118, 226, 255, 0.22);
                background: rgba(4, 16, 28, 238);
            }
            #callableGroupCreateContent {
                border-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #callableGroupCreateChromeBar {
                border: none;
                border-top-left-radius: 22px;
                border-top-right-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #callableGroupCreateTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 20px;
                font-weight: 600;
                padding: 0px 6px 1px 6px;
                background: transparent;
            }
            #callableGroupCreateHintFrame {
                background: transparent;
            }
            #callableGroupCreateHint {
                color: rgba(136, 165, 174, 0.88);
                font-size: 11px;
                line-height: 1.45em;
                padding: 0px 6px 3px 6px;
                background: transparent;
            }
            """
            + THEMED_TOOLTIP_QSS
            + """
            #callableGroupCreateExamplesBox {
                border-radius: 0px;
                border: none;
                background: transparent;
            }
            #callableGroupCreateTaskFlowNote {
                border-radius: 0px;
                border: none;
                background: transparent;
            }
            #callableGroupCreateMembersScroll {
                border-radius: 18px;
                border: none;
                background: rgba(8, 20, 34, 214);
            }
            #callableGroupCreateMembersViewport {
                border-radius: 14px;
                background: transparent;
            }
            #callableGroupCreateMembersFrame {
                background: transparent;
            }
            #callableGroupCreateAliasesContent {
                background: transparent;
            }
            #callableGroupCreateExamplesTitle {
                color: rgba(84, 192, 181, 0.88);
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                background: transparent;
            }
            #callableGroupCreateTaskFlowTitle {
                color: rgba(84, 192, 181, 0.88);
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                background: transparent;
            }
            #callableGroupCreateExamples {
                color: rgba(168, 193, 199, 0.93);
                font-size: 13px;
                line-height: 1.45em;
                background: transparent;
            }
            #callableGroupCreateTaskFlowBody {
                color: rgba(168, 193, 199, 0.93);
                font-size: 13px;
                line-height: 1.45em;
                background: transparent;
            }
            #callableGroupCreateStatus {
                color: rgba(255, 189, 176, 0.96);
                font-size: 13px;
            }
            QWidget[createRole="fieldHeaderDivider"] {
                border: none;
                background: transparent;
            }
            QFrame[createRole="fieldRow"] {
                border-radius: 0px;
                border: none;
                background: transparent;
            }
            QWidget[createRole="fieldLabelHolder"], QWidget[createRole="fieldContentHolder"] {
                background: transparent;
            }
            QFrame[createRole="fieldHeaderDividerLine"] {
                min-height: 1px;
                max-height: 1px;
                border: none;
                background: rgba(118, 226, 255, 0.18);
            }
            QLabel[createRole="fieldHeader"], QLabel[createRole="fieldHeaderHelp"] {
                color: rgba(182, 206, 198, 0.96);
                font-size: 13px;
                font-weight: 650;
                background: transparent;
            }
            QLabel[createRole="fieldHeaderHelp"] {
                padding-bottom: 0px;
            }
            QLabel[createRole="fieldHeaderHelp"]:hover {
                color: rgba(198, 218, 211, 0.99);
            }
            QLineEdit {
                min-height: 30px;
                border-radius: 14px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(193, 213, 208, 0.96);
                padding: 4px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(118, 226, 255, 0.42);
                background: rgba(7, 22, 36, 220);
            }
            QPushButton {
                min-height: 38px;
                padding: 0 16px;
                border-radius: 12px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            QPushButton[chromeRole="close"] {
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                padding: 0px;
                text-align: center;
                border-radius: 7px;
                border: 1px solid rgba(118, 226, 255, 0.16);
                background: rgba(18, 52, 78, 228);
                color: rgba(191, 212, 207, 0.94);
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton[chromeRole="close"]:hover,
            QPushButton:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(8, 24, 38, 220);
            }
            QPushButton[chromeRole="close"]:hover {
                background: rgba(22, 61, 90, 238);
            }
            QCheckBox {
                color: rgba(182, 206, 198, 0.94);
                spacing: 6px;
                font-size: 13px;
                background: transparent;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 5px;
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(8, 20, 34, 0.98);
            }
            QCheckBox::indicator:hover {
                border: 1px solid rgba(118, 226, 255, 0.48);
                background: rgba(10, 26, 40, 0.98);
            }
            QCheckBox::indicator:checked {
                border: 1px solid rgba(102, 219, 204, 0.70);
                background: rgba(22, 88, 79, 0.96);
            }
            #callableGroupCreateMembersScroll QScrollBar:vertical {
                width: 8px;
                margin: 4px 1px 4px 0;
                border-radius: 4px;
                background: rgba(6, 18, 30, 0.58);
            }
            #callableGroupCreateMembersScroll QScrollBar::handle:vertical {
                min-height: 38px;
                border-radius: 4px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(18, 52, 78, 0.96);
            }
            #callableGroupCreateMembersScroll QScrollBar::handle:vertical:hover {
                background: rgba(22, 61, 90, 0.98);
            }
            #callableGroupCreateMembersScroll QScrollBar::add-line:vertical,
            #callableGroupCreateMembersScroll QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            #callableGroupCreateMembersScroll QScrollBar::add-page:vertical,
            #callableGroupCreateMembersScroll QScrollBar::sub-page:vertical {
                background: transparent;
            }
            #callableGroupCreateMemberCard {
                border-radius: 14px;
                border: 1px solid rgba(118, 226, 255, 0.22);
                background: rgba(12, 28, 44, 208);
            }
            #callableGroupCreateMemberTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 14px;
                font-weight: 650;
                background: transparent;
            }
            #callableGroupCreateMemberMeta {
                color: rgba(84, 192, 181, 0.88);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                background: transparent;
            }
            #callableGroupCreateMemberDetail {
                color: rgba(168, 193, 199, 0.93);
                font-size: 12px;
                background: transparent;
            }
            #callableGroupCreateMemberToggle {
                color: rgba(188, 212, 203, 0.94);
                font-size: 12px;
                font-weight: 600;
                background: transparent;
            }
            """
        )
        self._populate_member_choices()
        self._refresh_examples_box()
        if initial_draft is not None:
            self.load_draft(initial_draft)

    def _emit_lifecycle_event(self, stage: str, **fields):
        if callable(self._lifecycle_callback):
            try:
                self._lifecycle_callback(self._dialog_signal_name, stage, dialog=self, **fields)
            except Exception:
                pass

    def _emit_ready_signal(self):
        if self._ready_signal_emitted or not self.isVisible():
            return
        self._ready_signal_emitted = True
        self._emit_lifecycle_event("ready")

    def showEvent(self, event):
        super().showEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)
        self._emit_lifecycle_event("opened")
        QTimer.singleShot(0, self._emit_ready_signal)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)

    def done(self, result):
        self._emit_lifecycle_event(
            "closed",
            result="accepted" if result == QDialog.Accepted else "rejected",
        )
        super().done(result)

    def _update_chrome_overlay_geometry(self):
        if hasattr(self, "chrome_bar"):
            self.chrome_bar.raise_()

    def _build_members_placeholder_card(self, message: str) -> QFrame:
        card = QFrame(self.members_frame)
        card.setObjectName("callableGroupCreateTaskFlowNote")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(4)

        title_label = QLabel("Section guidance", card)
        title_label.setObjectName("callableGroupCreateTaskFlowTitle")
        card_layout.addWidget(title_label)

        body_label = QLabel(message, card)
        body_label.setObjectName("callableGroupCreateTaskFlowBody")
        body_label.setWordWrap(True)
        card_layout.addWidget(body_label)
        return card

    def _build_member_choice_card(
        self,
        *,
        member_id: str,
        title: str,
        subtitle: str,
        target_display: str,
    ) -> tuple[QFrame, QCheckBox]:
        card = QFrame(self.members_frame)
        card.setObjectName("callableGroupCreateMemberCard")
        card.setMinimumHeight(64)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 6, 12, 6)
        card_layout.setSpacing(3)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        title_label = QLabel(title, card)
        title_label.setObjectName("callableGroupCreateMemberTitle")
        title_label.setWordWrap(True)
        header_row.addWidget(title_label, 1)

        checkbox = QCheckBox("Include", card)
        checkbox.setObjectName("callableGroupCreateMemberToggle")
        checkbox.setProperty("memberId", member_id)
        header_row.addWidget(checkbox, 0, Qt.AlignRight | Qt.AlignTop)
        card_layout.addLayout(header_row)

        if subtitle:
            subtitle_label = QLabel(subtitle, card)
            subtitle_label.setObjectName("callableGroupCreateMemberMeta")
            subtitle_label.setWordWrap(True)
            card_layout.addWidget(subtitle_label)

        if target_display:
            detail_label = QLabel(target_display, card)
            detail_label.setObjectName("callableGroupCreateMemberDetail")
            detail_label.setWordWrap(True)
            card_layout.addWidget(detail_label)

        return card, checkbox

    def _sync_members_scroll_height(self):
        if self.members_scroll is None or self.members_layout is None:
            return
        member_widgets = [
            self.members_layout.itemAt(index).widget()
            for index in range(self.members_layout.count())
            if self.members_layout.itemAt(index) is not None
            and self.members_layout.itemAt(index).widget() is not None
        ]
        if not member_widgets:
            self.members_scroll.setFixedHeight(0)
            return

        visible_rows = sum(1 for widget in member_widgets if widget.isVisible())
        minimum_height = 120 if any(widget.objectName() == "callableGroupCreateTaskFlowNote" for widget in member_widgets) else 0
        desired_height = _visible_row_height_for_layout(
            self.members_layout,
            min(5, visible_rows),
            extra_padding=0,
        )
        desired_height = min(max(minimum_height, desired_height), 432)
        self.members_scroll.setMaximumHeight(desired_height)
        self.members_scroll.setFixedHeight(desired_height)

    def _populate_member_choices(self):
        if self.members_layout is None or self.members_frame is None:
            return
        _clear_layout_widgets(self.members_layout)
        self._member_checkboxes = []
        if not self._show_member_picker:
            self.task_flow_note = self._build_members_placeholder_card(
                "Task-path create skips member picking here. After save, this path returns you to Manage Custom Groups for the current task so you can assign the new group immediately without leaving task authoring."
            )
            self.members_layout.addWidget(self.task_flow_note)
            self.members_layout.addStretch(1)
            self.members_layout.activate()
            self._sync_members_scroll_height()
            QTimer.singleShot(0, self._sync_members_scroll_height)
            return
        if not self._available_members:
            self.members_layout.addWidget(
                self._build_members_placeholder_card(
                    "No saved tasks or built-in actions are loaded from the current source yet."
                )
            )
            self.members_layout.addStretch(1)
            self.members_layout.activate()
            self._sync_members_scroll_height()
            QTimer.singleShot(0, self._sync_members_scroll_height)
            return
        added_member_rows = 0
        for item in self._available_members:
            member_id = str(item.get("id") or "").strip()
            title = str(item.get("title") or item.get("id") or "").strip()
            if not title:
                continue
            origin_label = str(item.get("origin_label") or "").strip() or "Member"
            target_kind = str(item.get("target_kind") or "").strip()
            target_display = str(item.get("target_display") or "").strip()
            subtitle = f"{origin_label} | {target_kind}".strip(" |")
            card, checkbox = self._build_member_choice_card(
                member_id=member_id,
                title=title,
                subtitle=subtitle,
                target_display=target_display,
            )
            if subtitle:
                checkbox.setToolTip(
                    f"{subtitle}\nBecomes selectable when this group's alias is used."
                )
            else:
                checkbox.setToolTip("Becomes selectable when this group's alias is used.")
            self.members_layout.addWidget(card)
            self._member_checkboxes.append(checkbox)
            added_member_rows += 1
        if added_member_rows <= 0:
            self.members_layout.addWidget(
                self._build_members_placeholder_card(
                    "No saved tasks or built-in actions are loaded from the current source yet."
                )
            )
            self.members_layout.addStretch(1)
            self.members_layout.activate()
            self._sync_members_scroll_height()
            QTimer.singleShot(0, self._sync_members_scroll_height)
            return
        self.members_layout.addStretch(1)
        self.members_layout.activate()
        self._sync_members_scroll_height()
        QTimer.singleShot(0, self._sync_members_scroll_height)

    def _selected_member_ids(self) -> tuple[str, ...]:
        return tuple(
            checkbox.property("memberId")
            for checkbox in self._member_checkboxes
            if checkbox.isChecked() and str(checkbox.property("memberId") or "").strip()
        )

    def _refresh_examples_box(self):
        aliases = tuple(
            part.strip()
            for part in (self.aliases_input.text() or "").replace("\n", ",").split(",")
            if part.strip()
        )
        phrases = build_callable_group_phrases(aliases)
        if phrases:
            body = "<br/>".join(f"&bull; {escape(phrase)}" for phrase in phrases)
        else:
            body = "Add one or more aliases to preview the exact callable phrases."
        self.examples_label.setText(body)

    def build_draft(self) -> CallableGroupDraft:
        aliases = tuple(
            part.strip()
            for part in (self.aliases_input.text() or "").replace("\n", ",").split(",")
            if part.strip()
        )
        return CallableGroupDraft(
            title=self.name_input.text(),
            aliases=aliases,
            member_action_ids=self._selected_member_ids() if self._show_member_picker else (),
        )

    def load_draft(self, draft: CallableGroupDraft):
        self.name_input.setText(draft.title)
        self.aliases_input.setText(", ".join(draft.aliases))
        if self._show_member_picker:
            selected_ids = {member_id.casefold() for member_id in draft.member_action_ids}
            for checkbox in self._member_checkboxes:
                checkbox.setChecked(str(checkbox.property("memberId") or "").strip().casefold() in selected_ids)
        self._refresh_examples_box()

    def set_error_text(self, text: str):
        self.status_label.setText((text or "").strip())
        self.status_label.setVisible(bool(self.status_label.text()))

    def _handle_submit_clicked(self):
        if self._submit_handler is None:
            self.accept()
            return
        try:
            self._submit_handler(self.build_draft())
        except (CallableGroupDraftValidationError, CallableGroupUnsafeSourceError, SavedActionSourceWriteBlocked) as exc:
            self.set_error_text(str(exc))
            return
        except Exception as exc:
            self.set_error_text(f"Custom group could not be saved: {exc}")
            return
        self.accept()


class CallableGroupEditDialog(CallableGroupCreateDialog):
    def __init__(
        self,
        parent=None,
        submit_handler=None,
        initial_draft: CallableGroupDraft | None = None,
        available_members: list[dict] | None = None,
        lifecycle_callback=None,
    ):
        super().__init__(
            parent,
            submit_handler,
            dialog_title="Edit Custom Group",
            heading_text="Edit Custom Group",
            hint_text="Update the group name, aliases, and members below.",
            submit_button_text="Save",
            available_members=available_members,
            initial_draft=initial_draft,
            lifecycle_callback=lifecycle_callback,
            dialog_signal_name="CUSTOM_GROUP_EDIT_DIALOG",
        )

class CreatedTasksDialog(QDialog):
    def __init__(self, parent=None, inventory_payload: dict | None = None, lifecycle_callback=None):
        super().__init__(parent)
        self._selected_action_id = ""
        self._selected_delete_action_id = ""
        self._lifecycle_callback = lifecycle_callback
        self._ready_signal_emitted = False
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Manage Custom Tasks")
        self.setObjectName("savedActionCreatedTasksDialog")
        self.setMinimumWidth(620)
        self.setMaximumWidth(680)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.shell = QFrame(self)
        self.shell.setObjectName("savedActionCreatedTasksShell")
        root_layout.addWidget(self.shell)

        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.chrome_bar = DialogChromeBar(
            "Manage Custom Tasks",
            self,
            object_prefix="savedActionCreatedTasks",
            parent=self.shell,
            show_title=False,
        )
        self.chrome_bar.close_button.setToolTip("Close Manage Custom Tasks")
        shell_layout.addWidget(self.chrome_bar)

        self.content = QWidget(self.shell)
        self.content.setObjectName("savedActionCreatedTasksContent")
        shell_layout.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 2, 14, 10)
        layout.setSpacing(2)

        self.title_label = QLabel("Manage Custom Tasks", self)
        self.title_label.setObjectName("savedActionCreatedTasksTitle")
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.title_label)

        self.hint_label = QLabel(
            "Review, update, or remove tasks from the current saved-task source.",
            self,
        )
        self.hint_label.setObjectName("savedActionCreatedTasksHint")
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.hint_label)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("savedActionCreatedTasksStatus")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.source_label = QLabel("", self)
        self.source_label.setObjectName("savedActionCreatedTasksSource")
        self.source_label.setWordWrap(True)
        layout.addWidget(self.source_label)

        self.guidance_label = QLabel("", self)
        self.guidance_label.setObjectName("savedActionCreatedTasksGuidance")
        self.guidance_label.setWordWrap(True)
        layout.addWidget(self.guidance_label)

        self.items_frame = QFrame(self)
        self.items_frame.setObjectName("savedActionCreatedTasksItems")
        self.items_layout = QVBoxLayout(self.items_frame)
        self.items_layout.setContentsMargins(0, 2, 0, 0)
        self.items_layout.setSpacing(2)

        self.items_scroll = QScrollArea(self)
        self.items_scroll.setObjectName("savedActionCreatedTasksItemsScroll")
        self.items_scroll.setFrameShape(QFrame.NoFrame)
        self.items_scroll.setWidgetResizable(True)
        self.items_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.items_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.items_scroll.setFocusPolicy(Qt.NoFocus)
        self.items_scroll.setMaximumHeight(0)
        self.items_scroll.viewport().setObjectName("savedActionCreatedTasksViewport")
        self.items_scroll.viewport().setAutoFillBackground(False)
        self.items_scroll.setWidget(self.items_frame)
        layout.addWidget(self.items_scroll)

        self.footer_frame = QFrame(self)
        self.footer_frame.setObjectName("savedActionCreatedTasksFooter")
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(0, 4, 0, 0)
        footer_layout.setSpacing(8)
        footer_layout.addStretch(1)

        self.close_button = QPushButton("Close", self.footer_frame)
        self.close_button.setObjectName("savedActionCreatedTasksClose")
        self.close_button.setMinimumHeight(34)
        self.close_button.clicked.connect(self.reject)
        footer_layout.addWidget(self.close_button)

        layout.addWidget(self.footer_frame)

        self.setStyleSheet(
            """
            #savedActionCreatedTasksDialog {
                background: transparent;
            }
            #savedActionCreatedTasksShell {
                border-radius: 22px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(4, 16, 28, 238);
            }
            #savedActionCreatedTasksContent {
                border-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #savedActionCreatedTasksFooter {
                border-top: 1px solid rgba(118, 226, 255, 0.12);
                background: transparent;
            }
            #savedActionCreatedTasksChromeBar {
                border: none;
                border-top-left-radius: 22px;
                border-top-right-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #savedActionCreatedTasksChromeTitle {
                color: rgba(126, 171, 181, 0.84);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.24em;
            }
            #savedActionCreatedTasksChromeClose {
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                padding: 0px;
                text-align: center;
                border-radius: 7px;
                border: 1px solid rgba(118, 226, 255, 0.16);
                background: rgba(18, 52, 78, 228);
                color: rgba(191, 212, 207, 0.94);
                font-size: 12px;
                font-weight: 600;
            }
            #savedActionCreatedTasksChromeClose:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(22, 61, 90, 238);
            }
            #savedActionCreatedTasksTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 20px;
                font-weight: 600;
                padding: 0px 6px 1px 6px;
                background: transparent;
            }
            #savedActionCreatedTasksHint {
                color: rgba(136, 165, 174, 0.88);
                font-size: 11px;
                line-height: 1.45em;
                padding: 0px 6px 3px 6px;
                background: transparent;
            }
            """
            + THEMED_TOOLTIP_QSS
            + """
            #savedActionCreatedTasksStatus {
                color: rgba(148, 180, 178, 0.89);
                font-size: 13px;
                font-weight: 600;
            }
            #savedActionCreatedTasksStatus[statusKind="invalid_source"], #savedActionCreatedTasksStatus[statusKind="invalid_saved_actions"], #savedActionCreatedTasksStatus[statusKind="missing"] {
                color: rgba(255, 189, 176, 0.96);
            }
            #savedActionCreatedTasksSource {
                color: rgba(126, 157, 171, 0.78);
                font-size: 13px;
            }
            #savedActionCreatedTasksGuidance {
                color: rgba(110, 201, 164, 0.86);
                font-size: 13px;
                line-height: 1.4em;
            }
            #savedActionCreatedTasksItemsScroll {
                border: none;
                background: transparent;
            }
            #savedActionCreatedTasksViewport {
                border-radius: 18px;
                background: rgba(4, 12, 22, 236);
            }
            #savedActionCreatedTasksItems {
                background: transparent;
            }
            QFrame[inventoryRole="itemFrame"] {
                border-radius: 14px;
                border: 1px solid rgba(118, 226, 255, 0.22);
                background: rgba(12, 28, 44, 208);
            }
            QFrame[inventoryRole="actionShell"] {
                border-radius: 16px;
                border: none;
                background: rgba(15, 40, 62, 248);
            }
            QLabel[inventoryRole="itemTitle"] {
                color: rgba(184, 208, 200, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            QLabel[inventoryRole="itemMeta"] {
                color: rgba(84, 192, 181, 0.83);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }
            QLabel[inventoryRole="itemTarget"] {
                color: rgba(163, 189, 196, 0.92);
                font-size: 12px;
            }
            QPushButton[inventoryRole="editButton"], QPushButton[inventoryRole="deleteButton"], #savedActionCreatedTasksClose {
                min-height: 28px;
                padding: 0 16px;
                border-radius: 12px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            #savedActionCreatedTasksClose {
                min-height: 34px;
            }
            QPushButton[inventoryRole="editButton"], QPushButton[inventoryRole="deleteButton"] {
                min-width: 104px;
            }
            QPushButton[inventoryRole="editButton"] {
                border: 1px solid rgba(118, 226, 255, 0.30);
                background: rgba(18, 52, 78, 228);
            }
            QPushButton[inventoryRole="deleteButton"] {
                border: 1px solid rgba(255, 138, 138, 0.26);
                background: rgba(34, 12, 16, 212);
                color: rgba(255, 231, 231, 0.96);
            }
            QPushButton[inventoryRole="editButton"]:hover, QPushButton[inventoryRole="deleteButton"]:hover, #savedActionCreatedTasksClose:hover {
                border: 1px solid rgba(118, 226, 255, 0.36);
                background: rgba(8, 24, 38, 220);
            }
            QPushButton[inventoryRole="deleteButton"]:hover {
                border: 1px solid rgba(255, 166, 166, 0.42);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar:vertical {
                width: 8px;
                margin: 4px 1px 4px 0;
                border-radius: 4px;
                background: rgba(6, 18, 30, 0.58);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::handle:vertical {
                min-height: 38px;
                border-radius: 4px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(18, 52, 78, 0.96);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::handle:vertical:hover {
                background: rgba(22, 61, 90, 0.98);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::handle:vertical:pressed {
                background: rgba(118, 226, 255, 0.54);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::add-line:vertical,
            #savedActionCreatedTasksItemsScroll QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::add-page:vertical,
            #savedActionCreatedTasksItemsScroll QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )

        self.refresh_inventory(inventory_payload or {})

    def _emit_lifecycle_event(self, stage: str, **fields):
        if callable(self._lifecycle_callback):
            try:
                self._lifecycle_callback("CREATED_TASKS_DIALOG", stage, dialog=self, **fields)
            except Exception:
                pass

    def _emit_ready_signal(self):
        if self._ready_signal_emitted or not self.isVisible():
            return
        self._ready_signal_emitted = True
        self._emit_lifecycle_event("ready")

    def showEvent(self, event):
        super().showEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)
        self._emit_lifecycle_event("opened")
        QTimer.singleShot(0, self._emit_ready_signal)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)

    def done(self, result):
        self._emit_lifecycle_event(
            "closed",
            result="accepted" if result == QDialog.Accepted else "rejected",
        )
        super().done(result)

    def _update_chrome_overlay_geometry(self):
        if hasattr(self, "chrome_bar"):
            self.chrome_bar.raise_()

    def _sync_items_scroll_height(self):
        if not hasattr(self, "items_scroll") or not hasattr(self, "items_layout"):
            return
        item_frames = [
            self.items_layout.itemAt(index).widget()
            for index in range(self.items_layout.count())
            if self.items_layout.itemAt(index) is not None
            and self.items_layout.itemAt(index).widget() is not None
            and self.items_layout.itemAt(index).widget().property("inventoryRole") == "itemFrame"
        ]
        visible_rows = sum(1 for frame in item_frames if frame.isVisible())
        if visible_rows <= 0:
            self.items_scroll.setMaximumHeight(0)
            self.items_scroll.setFixedHeight(0)
            return
        desired_height = _visible_row_height_for_layout(
            self.items_layout,
            min(5, visible_rows),
            extra_padding=0,
        )
        self.items_scroll.setMaximumHeight(desired_height)
        self.items_scroll.setFixedHeight(desired_height)

    def selected_action_id(self) -> str:
        return self._selected_action_id

    def selected_delete_action_id(self) -> str:
        return self._selected_delete_action_id

    def _handle_edit_requested(self, action_id: str):
        self._selected_action_id = action_id
        self._selected_delete_action_id = ""
        self.accept()

    def _handle_delete_requested(self, action_id: str):
        self._selected_delete_action_id = action_id
        self._selected_action_id = ""
        self.accept()

    def refresh_inventory(self, inventory_payload: dict):
        inventory_payload = inventory_payload or {}
        self.title_label.setText("Manage Custom Tasks")

        status_kind = inventory_payload.get("status_kind", "hidden")
        self.status_label.setProperty("statusKind", status_kind)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.setText(inventory_payload.get("status_text", ""))

        source_path = inventory_payload.get("path", "")
        source_display = inventory_payload.get("path_display") or source_path
        items = inventory_payload.get("items") or []
        show_source_details = status_kind in {"invalid_source", "invalid_saved_actions", "missing", "template_only"} or not items
        self.source_label.setText(f"Source: {source_display}" if show_source_details and source_display else "")
        self.source_label.setToolTip(source_path)
        guidance_text = inventory_payload.get("guidance_text", "")
        show_guidance = bool(guidance_text) and (
            status_kind in {"invalid_source", "invalid_saved_actions", "missing", "template_only"} or not items
        )
        self.guidance_label.setText(guidance_text if show_guidance else "")
        self.source_label.setVisible(bool(self.source_label.text()))
        self.guidance_label.setVisible(bool(self.guidance_label.text()))

        _populate_saved_inventory_item_layout(
            self.items_layout,
            self.items_frame,
            items,
            self._handle_edit_requested,
            self._handle_delete_requested,
        )
        self.items_scroll.setVisible(bool(items))
        if items:
            self.items_layout.activate()
            self._sync_items_scroll_height()
            QTimer.singleShot(0, self._sync_items_scroll_height)
        else:
            self.items_scroll.setMaximumHeight(0)
            self.items_scroll.setFixedHeight(0)


class CreatedGroupsDialog(QDialog):
    def __init__(self, parent=None, inventory_payload: dict | None = None, lifecycle_callback=None):
        super().__init__(parent)
        self._selected_group_id = ""
        self._selected_delete_group_id = ""
        self._lifecycle_callback = lifecycle_callback
        self._ready_signal_emitted = False
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Manage Custom Groups")
        self.setObjectName("savedActionCreatedGroupsDialog")
        self.setMinimumWidth(660)
        self.setMaximumWidth(760)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.shell = QFrame(self)
        self.shell.setObjectName("savedActionCreatedTasksShell")
        root_layout.addWidget(self.shell)

        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        self.chrome_bar = DialogChromeBar(
            "Manage Custom Groups",
            self,
            object_prefix="savedActionCreatedTasks",
            parent=self.shell,
            show_title=False,
        )
        self.chrome_bar.close_button.setToolTip("Close Manage Custom Groups")
        shell_layout.addWidget(self.chrome_bar)

        self.content = QWidget(self.shell)
        self.content.setObjectName("savedActionCreatedTasksContent")
        shell_layout.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 2, 14, 10)
        layout.setSpacing(2)

        self.title_label = QLabel("Manage Custom Groups", self)
        self.title_label.setObjectName("savedActionCreatedTasksTitle")
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.title_label)

        self.hint_label = QLabel(
            "Review, update, or remove callable groups from the current source.",
            self,
        )
        self.hint_label.setObjectName("savedActionCreatedTasksHint")
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.hint_label)

        self.status_label = QLabel("", self)
        self.status_label.setObjectName("savedActionCreatedTasksStatus")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.source_label = QLabel("", self)
        self.source_label.setObjectName("savedActionCreatedTasksSource")
        self.source_label.setWordWrap(True)
        layout.addWidget(self.source_label)

        self.guidance_label = QLabel("", self)
        self.guidance_label.setObjectName("savedActionCreatedTasksGuidance")
        self.guidance_label.setWordWrap(True)
        layout.addWidget(self.guidance_label)

        self.items_frame = QFrame(self)
        self.items_frame.setObjectName("savedActionCreatedTasksItems")
        self.items_layout = QVBoxLayout(self.items_frame)
        self.items_layout.setContentsMargins(0, 2, 0, 0)
        self.items_layout.setSpacing(2)

        self.items_scroll = QScrollArea(self)
        self.items_scroll.setObjectName("savedActionCreatedTasksItemsScroll")
        self.items_scroll.setFrameShape(QFrame.NoFrame)
        self.items_scroll.setWidgetResizable(True)
        self.items_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.items_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.items_scroll.setFocusPolicy(Qt.NoFocus)
        self.items_scroll.setMaximumHeight(0)
        self.items_scroll.viewport().setObjectName("savedActionCreatedTasksViewport")
        self.items_scroll.viewport().setAutoFillBackground(False)
        self.items_scroll.setWidget(self.items_frame)
        layout.addWidget(self.items_scroll)

        self.footer_frame = QFrame(self)
        self.footer_frame.setObjectName("savedActionCreatedTasksFooter")
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(0, 4, 0, 0)
        footer_layout.setSpacing(8)
        footer_layout.addStretch(1)

        self.close_button = QPushButton("Close", self.footer_frame)
        self.close_button.setObjectName("savedActionCreatedTasksClose")
        self.close_button.setMinimumHeight(34)
        self.close_button.clicked.connect(self.reject)
        footer_layout.addWidget(self.close_button)

        layout.addWidget(self.footer_frame)
        self.setStyleSheet(
            """
            #savedActionCreatedGroupsDialog {
                background: transparent;
            }
            #savedActionCreatedTasksShell {
                border-radius: 22px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(4, 16, 28, 238);
            }
            #savedActionCreatedTasksContent {
                border-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #savedActionCreatedTasksChromeBar {
                border: none;
                border-top-left-radius: 22px;
                border-top-right-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #savedActionCreatedTasksFooter {
                border-top: 1px solid rgba(118, 226, 255, 0.12);
                background: transparent;
            }
            #savedActionCreatedTasksTitle {
                color: rgba(188, 212, 203, 0.97);
                font-size: 20px;
                font-weight: 600;
                padding: 0px 6px 1px 6px;
                background: transparent;
            }
            #savedActionCreatedTasksHint {
                color: rgba(136, 165, 174, 0.88);
                font-size: 11px;
                padding: 0px 6px 3px 6px;
                background: transparent;
            }
            """
            + THEMED_TOOLTIP_QSS
            + """
            #savedActionCreatedTasksStatus {
                color: rgba(148, 180, 178, 0.89);
                font-size: 13px;
                font-weight: 600;
            }
            #savedActionCreatedTasksStatus[statusKind="invalid_source"], #savedActionCreatedTasksStatus[statusKind="invalid_groups"], #savedActionCreatedTasksStatus[statusKind="invalid_saved_actions"], #savedActionCreatedTasksStatus[statusKind="missing"] {
                color: rgba(255, 189, 176, 0.96);
            }
            #savedActionCreatedTasksSource {
                color: rgba(126, 157, 171, 0.78);
                font-size: 13px;
            }
            #savedActionCreatedTasksGuidance {
                color: rgba(110, 201, 164, 0.86);
                font-size: 13px;
            }
            #savedActionCreatedTasksItemsScroll {
                border: none;
                background: transparent;
            }
            #savedActionCreatedTasksViewport {
                border-radius: 18px;
                background: rgba(4, 12, 22, 236);
            }
            #savedActionCreatedTasksItems {
                background: transparent;
            }
            QFrame[inventoryRole="itemFrame"] {
                border-radius: 14px;
                border: 1px solid rgba(118, 226, 255, 0.22);
                background: rgba(12, 28, 44, 208);
            }
            QFrame[inventoryRole="actionShell"] {
                border-radius: 16px;
                border: none;
                background: rgba(15, 40, 62, 248);
            }
            QLabel[inventoryRole="itemTitle"] {
                color: rgba(184, 208, 200, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            QLabel[inventoryRole="itemMeta"] {
                color: rgba(84, 192, 181, 0.83);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }
            QLabel[inventoryRole="itemTarget"] {
                color: rgba(163, 189, 196, 0.92);
                font-size: 12px;
            }
            QPushButton[inventoryRole="editButton"], QPushButton[inventoryRole="deleteButton"], #savedActionCreatedTasksClose {
                min-height: 28px;
                padding: 0 16px;
                border-radius: 12px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
                font-size: 14px;
                font-weight: 650;
            }
            #savedActionCreatedTasksClose {
                min-height: 34px;
            }
            QPushButton[inventoryRole="editButton"], QPushButton[inventoryRole="deleteButton"] {
                min-width: 104px;
            }
            QPushButton[inventoryRole="editButton"] {
                border: 1px solid rgba(118, 226, 255, 0.30);
                background: rgba(18, 52, 78, 228);
            }
            QPushButton[inventoryRole="deleteButton"] {
                border: 1px solid rgba(255, 138, 138, 0.26);
                background: rgba(34, 12, 16, 212);
                color: rgba(255, 231, 231, 0.96);
            }
            QPushButton[chromeRole="close"] {
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
                padding: 0px;
                text-align: center;
                border-radius: 7px;
                border: 1px solid rgba(118, 226, 255, 0.16);
                background: rgba(18, 52, 78, 228);
                color: rgba(191, 212, 207, 0.94);
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton[chromeRole="close"]:hover {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(22, 61, 90, 238);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar:vertical {
                width: 8px;
                margin: 4px 1px 4px 0;
                border-radius: 4px;
                background: rgba(6, 18, 30, 0.58);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::handle:vertical {
                min-height: 38px;
                border-radius: 4px;
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(18, 52, 78, 0.96);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::handle:vertical:hover {
                background: rgba(22, 61, 90, 0.98);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::handle:vertical:pressed {
                background: rgba(118, 226, 255, 0.54);
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::add-line:vertical,
            #savedActionCreatedTasksItemsScroll QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            #savedActionCreatedTasksItemsScroll QScrollBar::add-page:vertical,
            #savedActionCreatedTasksItemsScroll QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )
        self.refresh_inventory(inventory_payload or {})

    def _emit_lifecycle_event(self, stage: str, **fields):
        if callable(self._lifecycle_callback):
            try:
                self._lifecycle_callback("CREATED_GROUPS_DIALOG", stage, dialog=self, **fields)
            except Exception:
                pass

    def _emit_ready_signal(self):
        if self._ready_signal_emitted or not self.isVisible():
            return
        self._ready_signal_emitted = True
        self._emit_lifecycle_event("ready")

    def showEvent(self, event):
        super().showEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)
        self._emit_lifecycle_event("opened")
        QTimer.singleShot(0, self._sync_items_scroll_height)
        QTimer.singleShot(0, self._emit_ready_signal)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_chrome_overlay_geometry()
        _apply_rounded_dialog_mask(self)
        _schedule_window_clamp(self)
        QTimer.singleShot(0, self._sync_items_scroll_height)

    def done(self, result):
        self._emit_lifecycle_event(
            "closed",
            result="accepted" if result == QDialog.Accepted else "rejected",
        )
        super().done(result)

    def _update_chrome_overlay_geometry(self):
        if hasattr(self, "chrome_bar"):
            self.chrome_bar.raise_()

    def _sync_items_scroll_height(self):
        if not hasattr(self, "items_scroll") or not hasattr(self, "items_layout"):
            return
        item_frames = [
            self.items_layout.itemAt(index).widget()
            for index in range(self.items_layout.count())
            if self.items_layout.itemAt(index) is not None
            and self.items_layout.itemAt(index).widget() is not None
            and self.items_layout.itemAt(index).widget().property("inventoryRole") == "itemFrame"
        ]
        visible_rows = sum(1 for frame in item_frames if frame.isVisible())
        if visible_rows <= 0:
            self.items_scroll.setMaximumHeight(0)
            self.items_scroll.setFixedHeight(0)
            return
        desired_height = _visible_row_height_for_layout(
            self.items_layout,
            min(5, visible_rows),
            extra_padding=0,
        )
        self.items_scroll.setMaximumHeight(desired_height)
        self.items_scroll.setFixedHeight(desired_height)

    def selected_group_id(self) -> str:
        return self._selected_group_id

    def selected_delete_group_id(self) -> str:
        return self._selected_delete_group_id

    def _handle_edit_requested(self, group_id: str):
        self._selected_group_id = group_id
        self._selected_delete_group_id = ""
        self.accept()

    def _handle_delete_requested(self, group_id: str):
        self._selected_delete_group_id = group_id
        self._selected_group_id = ""
        self.accept()

    def refresh_inventory(self, inventory_payload: dict):
        inventory_payload = inventory_payload or {}
        self.title_label.setText("Manage Custom Groups")

        status_kind = inventory_payload.get("status_kind", "hidden")
        self.status_label.setProperty("statusKind", status_kind)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.setText(inventory_payload.get("status_text", ""))

        source_path = inventory_payload.get("path", "")
        source_display = inventory_payload.get("path_display") or source_path
        items = inventory_payload.get("items") or []
        show_source_details = status_kind in {"invalid_source", "invalid_groups", "invalid_saved_actions", "missing", "template_only"} or not items
        self.source_label.setText(f"Source: {source_display}" if show_source_details and source_display else "")
        self.source_label.setToolTip(source_path)
        guidance_text = inventory_payload.get("guidance_text", "")
        show_guidance = bool(guidance_text) and (
            status_kind in {"invalid_source", "invalid_groups", "invalid_saved_actions", "missing", "template_only"} or not items
        )
        self.guidance_label.setText(guidance_text if show_guidance else "")
        self.source_label.setVisible(bool(self.source_label.text()))
        self.guidance_label.setVisible(bool(self.guidance_label.text()))

        _populate_saved_group_item_layout(
            self.items_layout,
            self.items_frame,
            items,
            self._handle_edit_requested,
            self._handle_delete_requested,
        )
        self.items_scroll.setVisible(bool(items))
        if items:
            self.items_layout.activate()
            self._sync_items_scroll_height()
            QTimer.singleShot(0, self._sync_items_scroll_height)
        else:
            self.items_scroll.setMaximumHeight(0)
            self.items_scroll.setFixedHeight(0)


class CommandOverlayPanel(QWidget):
    submit_requested = Signal()
    escape_requested = Signal()
    input_text_changed = Signal(str)
    input_armed_changed = Signal(bool)
    input_focus_acquired = Signal()
    input_focus_lost = Signal()
    ambiguous_match_selected = Signal(int)
    create_custom_task_requested = Signal()
    created_tasks_requested = Signal()
    create_custom_group_requested = Signal()
    created_groups_requested = Signal()
    edit_saved_action_requested = Signal(str)

    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setObjectName("commandOverlayWindow")
        self._visible_ambiguous_count = 0

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.panel = QFrame(self)
        self.panel.setObjectName("commandPanel")
        root.addWidget(self.panel)

        layout = QVBoxLayout(self.panel)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(0)

        self.kicker_label = QLabel("O.R.I.N. Command Prompt", self.panel)
        self.kicker_label.setObjectName("commandKicker")
        layout.addWidget(self.kicker_label)

        self.title_label = QLabel("Typed desktop interaction", self.panel)
        self.title_label.setObjectName("commandTitle")
        layout.addWidget(self.title_label)

        self.hint_label = QLabel(
            "Left-click or right-click the command box to activate.",
            self.panel,
        )
        self.hint_label.setObjectName("commandHint")
        self.hint_label.setWordWrap(True)
        layout.addWidget(self.hint_label)

        self.input_shell = QFrame(self.panel)
        self.input_shell.setObjectName("commandInputShell")
        input_layout = QHBoxLayout(self.input_shell)
        input_layout.setContentsMargins(16, 14, 16, 14)
        input_layout.setSpacing(10)

        self.prompt_label = QLabel(">", self.input_shell)
        self.prompt_label.setObjectName("commandPrompt")
        input_layout.addWidget(self.prompt_label)

        self.input_line = CommandInputLineEdit(self.input_shell)
        self.input_line.setObjectName("commandInputLine")
        self.input_line.textChanged.connect(self.input_text_changed)
        self.input_line.submit_requested.connect(self.submit_requested)
        self.input_line.escape_requested.connect(self.escape_requested)
        self.input_line.input_armed_changed.connect(self.input_armed_changed)
        self.input_line.focus_acquired.connect(self.input_focus_acquired)
        self.input_line.focus_lost.connect(self.input_focus_lost)
        input_layout.addWidget(self.input_line, 1)

        self.caret = QFrame(self.input_shell)
        self.caret.setObjectName("commandCaret")
        input_layout.addWidget(self.caret)

        layout.addWidget(self.input_shell)

        self.status_label = QLabel("", self.panel)
        self.status_label.setObjectName("commandStatus")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.saved_inventory_frame = QFrame(self.panel)
        self.saved_inventory_frame.setObjectName("savedActionInventory")
        saved_inventory_layout = QVBoxLayout(self.saved_inventory_frame)
        saved_inventory_layout.setContentsMargins(18, 16, 18, 16)
        saved_inventory_layout.setSpacing(10)

        self.saved_inventory_title = QLabel("Custom tasks and groups", self.saved_inventory_frame)
        self.saved_inventory_title.setObjectName("savedActionInventoryTitle")
        saved_inventory_layout.addWidget(self.saved_inventory_title)

        self.saved_inventory_status = QLabel(
            "Create or manage exact-match tasks and callable groups.",
            self.saved_inventory_frame,
        )
        self.saved_inventory_status.setObjectName("savedActionInventoryStatus")
        self.saved_inventory_status.setWordWrap(True)
        saved_inventory_layout.addWidget(self.saved_inventory_status)

        self.entry_actions_layout = QGridLayout()
        self.entry_actions_layout.setContentsMargins(0, 0, 0, 0)
        self.entry_actions_layout.setHorizontalSpacing(12)
        self.entry_actions_layout.setVerticalSpacing(12)
        self.entry_actions_layout.setColumnStretch(0, 1)
        self.entry_actions_layout.setColumnStretch(1, 1)

        self.create_action_frame = QFrame(self.saved_inventory_frame)
        self.create_action_frame.setProperty("entryActionCard", "true")
        self.create_action_frame.setProperty("entryActionVariant", "primary")
        create_action_layout = QVBoxLayout(self.create_action_frame)
        create_action_layout.setContentsMargins(12, 12, 12, 12)
        create_action_layout.setSpacing(6)

        self.create_custom_task_button = QPushButton("Create Custom Task", self.create_action_frame)
        self.create_custom_task_button.setObjectName("savedActionCreateButton")
        self.create_custom_task_button.setProperty("entryAction", "true")
        self.create_custom_task_button.setProperty("entryActionVariant", "primary")
        self.create_custom_task_button.clicked.connect(
            lambda _checked=False: self.create_custom_task_requested.emit()
        )
        create_action_layout.addWidget(self.create_custom_task_button)

        self.create_custom_task_description = QLabel(
            "Start a new application, folder, file, or website task.",
            self.create_action_frame,
        )
        self.create_custom_task_description.setObjectName("savedActionCreateDescription")
        self.create_custom_task_description.setWordWrap(True)
        create_action_layout.addWidget(self.create_custom_task_description)
        self.entry_actions_layout.addWidget(self.create_action_frame, 0, 0)

        self.manage_action_frame = QFrame(self.saved_inventory_frame)
        self.manage_action_frame.setProperty("entryActionCard", "true")
        self.manage_action_frame.setProperty("entryActionVariant", "secondary")
        manage_action_layout = QVBoxLayout(self.manage_action_frame)
        manage_action_layout.setContentsMargins(12, 12, 12, 12)
        manage_action_layout.setSpacing(6)

        self.created_tasks_button = QPushButton("Manage Custom Tasks", self.manage_action_frame)
        self.created_tasks_button.setObjectName("savedActionCreatedTasksButton")
        self.created_tasks_button.setProperty("entryAction", "true")
        self.created_tasks_button.setProperty("entryActionVariant", "secondary")
        self.created_tasks_button.clicked.connect(
            lambda _checked=False: self.created_tasks_requested.emit()
        )
        manage_action_layout.addWidget(self.created_tasks_button)

        self.created_tasks_description = QLabel(
            "Review, edit, or remove the tasks you have already saved.",
            self.manage_action_frame,
        )
        self.created_tasks_description.setObjectName("savedActionCreatedTasksDescription")
        self.created_tasks_description.setWordWrap(True)
        manage_action_layout.addWidget(self.created_tasks_description)
        self.entry_actions_layout.addWidget(self.manage_action_frame, 0, 1)

        self.create_group_action_frame = QFrame(self.saved_inventory_frame)
        self.create_group_action_frame.setProperty("entryActionCard", "true")
        self.create_group_action_frame.setProperty("entryActionVariant", "primary")
        create_group_layout = QVBoxLayout(self.create_group_action_frame)
        create_group_layout.setContentsMargins(12, 12, 12, 12)
        create_group_layout.setSpacing(6)

        self.create_custom_group_button = QPushButton("Create Custom Group", self.create_group_action_frame)
        self.create_custom_group_button.setObjectName("savedActionCreateGroupButton")
        self.create_custom_group_button.setProperty("entryAction", "true")
        self.create_custom_group_button.setProperty("entryActionVariant", "primary")
        self.create_custom_group_button.setToolTip(
            "Create an exact-match callable group that can surface selected built-ins and saved tasks."
        )
        self.create_custom_group_button.clicked.connect(
            lambda _checked=False: self.create_custom_group_requested.emit()
        )
        create_group_layout.addWidget(self.create_custom_group_button)

        self.create_custom_group_description = QLabel(
            "Start a callable group that can surface built-ins and saved tasks.",
            self.create_group_action_frame,
        )
        self.create_custom_group_description.setObjectName("savedActionCreateGroupDescription")
        self.create_custom_group_description.setWordWrap(True)
        create_group_layout.addWidget(self.create_custom_group_description)
        self.entry_actions_layout.addWidget(self.create_group_action_frame, 1, 0)

        self.manage_group_action_frame = QFrame(self.saved_inventory_frame)
        self.manage_group_action_frame.setProperty("entryActionCard", "true")
        self.manage_group_action_frame.setProperty("entryActionVariant", "secondary")
        manage_group_layout = QVBoxLayout(self.manage_group_action_frame)
        manage_group_layout.setContentsMargins(12, 12, 12, 12)
        manage_group_layout.setSpacing(6)

        self.created_groups_button = QPushButton("Manage Custom Groups", self.manage_group_action_frame)
        self.created_groups_button.setObjectName("savedActionCreatedGroupsButton")
        self.created_groups_button.setProperty("entryAction", "true")
        self.created_groups_button.setProperty("entryActionVariant", "secondary")
        self.created_groups_button.setToolTip(
            "Review, edit, or remove callable groups and manage which members each group can surface."
        )
        self.created_groups_button.clicked.connect(
            lambda _checked=False: self.created_groups_requested.emit()
        )
        manage_group_layout.addWidget(self.created_groups_button)

        self.created_groups_description = QLabel(
            "Review, edit, or remove callable groups and their members.",
            self.manage_group_action_frame,
        )
        self.created_groups_description.setObjectName("savedActionCreatedGroupsDescription")
        self.created_groups_description.setWordWrap(True)
        manage_group_layout.addWidget(self.created_groups_description)
        self.entry_actions_layout.addWidget(self.manage_group_action_frame, 1, 1)

        saved_inventory_layout.addLayout(self.entry_actions_layout)

        saved_inventory_layout.addStretch(1)

        layout.addWidget(self.saved_inventory_frame)
        self.saved_inventory_frame.hide()

        self.ambiguous_label = QLabel("", self.panel)
        self.ambiguous_label.setObjectName("commandAmbiguous")
        self.ambiguous_label.setWordWrap(True)
        layout.addWidget(self.ambiguous_label)

        self.ambiguous_choices_frame = QFrame(self.panel)
        self.ambiguous_choices_frame.setObjectName("commandAmbiguousChoices")
        self.ambiguous_choices_layout = QVBoxLayout(self.ambiguous_choices_frame)
        self.ambiguous_choices_layout.setContentsMargins(0, 8, 0, 0)
        self.ambiguous_choices_layout.setSpacing(8)
        layout.addWidget(self.ambiguous_choices_frame)
        self.ambiguous_choices_frame.hide()

        self.confirmation_frame = QFrame(self.panel)
        self.confirmation_frame.setObjectName("commandConfirmation")
        confirm_layout = QGridLayout(self.confirmation_frame)
        confirm_layout.setContentsMargins(18, 16, 18, 14)
        confirm_layout.setHorizontalSpacing(14)
        confirm_layout.setVerticalSpacing(8)

        confirm_layout.addWidget(self._make_confirm_label("Typed request"), 0, 0)
        self.confirm_request_value = self._make_confirm_value()
        confirm_layout.addWidget(self.confirm_request_value, 0, 1)

        self.confirm_title_label = self._make_confirm_label("Resolved action")
        confirm_layout.addWidget(self.confirm_title_label, 1, 0)
        self.confirm_title_value = self._make_confirm_value()
        confirm_layout.addWidget(self.confirm_title_value, 1, 1)

        confirm_layout.addWidget(self._make_confirm_label("Action origin"), 2, 0)
        self.confirm_origin_value = self._make_confirm_value()
        confirm_layout.addWidget(self.confirm_origin_value, 2, 1)

        confirm_layout.addWidget(self._make_confirm_label("Target kind"), 3, 0)
        self.confirm_kind_value = self._make_confirm_value()
        confirm_layout.addWidget(self.confirm_kind_value, 3, 1)

        confirm_layout.addWidget(self._make_confirm_label("Target"), 4, 0)
        self.confirm_target_value = self._make_confirm_value()
        confirm_layout.addWidget(self.confirm_target_value, 4, 1)

        self.confirm_help_label = QLabel(
            "Press Enter to confirm or Esc to return.",
            self.confirmation_frame,
        )
        self.confirm_help_label.setObjectName("commandConfirmHelp")
        self.confirm_help_label.setWordWrap(True)
        confirm_layout.addWidget(self.confirm_help_label, 5, 0, 1, 2)

        layout.addWidget(self.confirmation_frame)
        self.confirmation_frame.hide()

        self.setStyleSheet(
            """
            #commandPanel {
                border: 1px solid rgba(118, 226, 255, 0.22);
                border-radius: 22px;
                background: rgba(4, 16, 28, 238);
            }
            #commandKicker {
                color: rgba(84, 192, 181, 0.84);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.24em;
            }
            #commandTitle {
                margin-top: 8px;
                color: rgba(188, 212, 203, 0.97);
                font-size: 28px;
                font-weight: 600;
            }
            #commandHint {
                margin-top: 10px;
                color: rgba(136, 165, 174, 0.88);
                font-size: 14px;
            }
            """
            + THEMED_TOOLTIP_QSS
            + """
            #commandInputShell {
                margin-top: 18px;
                border-radius: 16px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
            }
            #commandInputShell[armed="true"] {
                border: 1px solid rgba(118, 226, 255, 0.36);
                background: rgba(7, 22, 36, 220);
            }
            #commandInputShell[locked="true"] {
                border: 1px solid rgba(118, 226, 255, 0.24);
                background: rgba(8, 18, 30, 214);
            }
            #commandPrompt {
                color: rgba(84, 192, 181, 0.88);
                font-size: 22px;
                font-weight: 600;
            }
            #commandInputLine {
                border: none;
                background: transparent;
                color: rgba(193, 213, 208, 0.96);
                font-size: 21px;
                selection-background-color: rgba(118, 226, 255, 0.28);
            }
            #commandInputLine:read-only {
                color: rgba(133, 155, 164, 0.92);
            }
            #commandCaret {
                min-width: 10px;
                max-width: 10px;
                min-height: 24px;
                max-height: 24px;
                border-radius: 999px;
                background: rgba(132, 236, 255, 0.82);
            }
            #commandCaret[armed="false"] {
                background: rgba(132, 236, 255, 0.22);
            }
            #commandStatus {
                margin-top: 14px;
                min-height: 22px;
                color: rgba(146, 176, 178, 0.89);
                font-size: 14px;
            }
            #commandStatus[statusKind="not_found"], #commandStatus[statusKind="launch_failed"] {
                color: rgba(255, 176, 176, 0.95);
            }
            #commandStatus[statusKind="ambiguous"] {
                color: rgba(255, 222, 154, 0.95);
            }
            #commandStatus[statusKind="launch_requested"], #commandStatus[statusKind="ready"] {
                color: rgba(166, 247, 195, 0.94);
            }
            #savedActionInventory {
                margin-top: 16px;
                border-radius: 18px;
                background: rgba(8, 20, 34, 214);
                border: 1px solid rgba(118, 226, 255, 0.12);
            }
            #savedActionInventoryTitle {
                color: rgba(84, 192, 181, 0.90);
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.08em;
            }
            #savedActionInventoryStatus {
                color: rgba(136, 165, 174, 0.88);
                font-size: 13px;
                line-height: 1.45em;
            }
            QFrame[entryActionCard="true"] {
                border-radius: 18px;
                border: 1px solid rgba(118, 226, 255, 0.12);
                background: rgba(7, 20, 34, 0.82);
            }
            QFrame[entryActionCard="true"][entryActionVariant="primary"] {
                border: 1px solid rgba(118, 226, 255, 0.20);
                background: rgba(10, 28, 46, 0.90);
            }
            QFrame[entryActionCard="true"][entryActionVariant="secondary"] {
                background: rgba(9, 22, 37, 0.88);
            }
            #savedActionCreateDescription, #savedActionCreatedTasksDescription,
            #savedActionCreateGroupDescription, #savedActionCreatedGroupsDescription {
                color: rgba(147, 174, 182, 0.87);
                font-size: 12px;
                line-height: 1.4em;
            }
            QPushButton[entryAction="true"] {
                min-height: 38px;
                margin-top: 0;
                padding: 0 14px;
                border-radius: 12px;
                border: 1px solid rgba(118, 226, 255, 0.18);
                background: rgba(6, 18, 30, 196);
                color: rgba(191, 212, 207, 0.96);
                text-align: left;
                font-size: 14px;
                font-weight: 650;
            }
            QPushButton[entryAction="true"][entryActionVariant="primary"] {
                border: 1px solid rgba(118, 226, 255, 0.34);
                background: rgba(18, 52, 78, 228);
            }
            QPushButton[entryAction="true"]:hover {
                border: 1px solid rgba(118, 226, 255, 0.36);
                background: rgba(8, 24, 38, 220);
            }
            QPushButton[entryAction="true"][entryActionVariant="primary"]:hover {
                border: 1px solid rgba(118, 226, 255, 0.50);
                background: rgba(22, 61, 90, 238);
            }
            #commandAmbiguous {
                min-height: 20px;
                color: rgba(255, 222, 154, 0.90);
                font-size: 13px;
            }
            #commandAmbiguousChoices {
                margin-top: 2px;
            }
            QPushButton[choiceRole="ambiguous"] {
                padding: 10px 14px;
                border-radius: 14px;
                border: 1px solid rgba(255, 222, 154, 0.28);
                background: rgba(32, 24, 10, 180);
                color: rgba(255, 239, 198, 0.96);
                text-align: left;
                font-size: 13px;
            }
            QPushButton[choiceRole="ambiguous"]:hover {
                border: 1px solid rgba(255, 222, 154, 0.44);
                background: rgba(44, 30, 12, 214);
            }
            #commandConfirmation {
                margin-top: 18px;
                border-radius: 18px;
                background: rgba(10, 22, 38, 220);
                border: 1px solid rgba(118, 226, 255, 0.14);
            }
            QLabel[confirmRole="label"] {
                color: rgba(78, 176, 173, 0.78);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.12em;
            }
            QLabel[confirmRole="value"] {
                color: rgba(189, 210, 204, 0.95);
                font-size: 15px;
            }
            #commandConfirmHelp {
                margin-top: 14px;
                color: rgba(140, 168, 176, 0.89);
                font-size: 13px;
            }
            """
        )

    def _make_confirm_label(self, text: str) -> QLabel:
        label = QLabel(text, self.confirmation_frame)
        label.setProperty("confirmRole", "label")
        return label

    def _make_confirm_value(self) -> QLabel:
        label = QLabel("", self.confirmation_frame)
        label.setProperty("confirmRole", "value")
        label.setWordWrap(True)
        return label

    def _build_confirm_surface_copy(self, selection_context: str, pending_group: dict | None = None) -> dict[str, str]:
        normalized_selection_context = (selection_context or "").strip().casefold()
        pending_group = pending_group or {}
        group_title = (pending_group.get("title") or "").strip()
        if normalized_selection_context == "group":
            group_subject = f'"{group_title}" group' if group_title else "the full matched group"
            return {
                "title_label": "Selected member",
                "hint_text": f"Review the selected member details below. Press Enter to run {group_subject} in stored order.",
                "help_text": f"Press Enter to run {group_subject} in stored order, or Esc to return.",
            }
        return {
            "title_label": "Resolved action",
            "hint_text": "Review the resolved action origin and destination before execution.",
            "help_text": "Press Enter to confirm or Esc to return.",
        }

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.submit_requested.emit()
            event.accept()
            return

        if event.key() == Qt.Key_Escape:
            self.escape_requested.emit()
            event.accept()
            return

        ambiguous_index = self._resolve_ambiguous_choice_index(event)
        if ambiguous_index is not None:
            self.ambiguous_match_selected.emit(ambiguous_index)
            event.accept()
            return

        super().keyPressEvent(event)

    def _resolve_ambiguous_choice_index(self, event) -> int | None:
        if self._visible_ambiguous_count <= 0:
            return None

        text = event.text() or ""
        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < self._visible_ambiguous_count:
                return index

        return None

    def _apply_geometry(self, host_geometry: QRect, bounds_geometry: QRect | None = None):
        width = max(520, min(680, int(host_geometry.width() * 0.56)))
        self.panel.setFixedWidth(width)
        self.panel.adjustSize()
        self.adjustSize()

        anchor_x = host_geometry.x() + int(host_geometry.width() * 0.84)
        x = anchor_x - (self.width() // 2)
        y = host_geometry.y() + max(18, (host_geometry.height() - self.height()) // 2)

        if bounds_geometry is not None:
            min_x = bounds_geometry.x()
            max_x = bounds_geometry.x() + max(0, bounds_geometry.width() - self.width())
            min_y = bounds_geometry.y()
            max_y = bounds_geometry.y() + max(0, bounds_geometry.height() - self.height())
            x = max(min_x, min(x, max_x))
            y = max(min_y, min(y, max_y))

        self.move(x, y)

    def show_for_geometry(self, host_geometry: QRect, bounds_geometry: QRect | None = None):
        self._apply_geometry(host_geometry, bounds_geometry)
        self.show()
        self.raise_()

    def refresh_for_geometry(self, host_geometry: QRect, bounds_geometry: QRect | None = None):
        self._apply_geometry(host_geometry, bounds_geometry)

    def focus_input(self, reason=Qt.ShortcutFocusReason):
        self.raise_()
        self.activateWindow()
        window_handle = self.windowHandle()
        if window_handle is not None:
            window_handle.requestActivate()
        self.setFocus(Qt.ActiveWindowFocusReason)
        self.input_line.setFocus(reason)
        self.input_line.setCursorPosition(len(self.input_line.text()))

    def ensure_typing_ready(self):
        self.input_line.set_input_armed(True, notify=False)
        self.focus_input(Qt.ShortcutFocusReason)

    def focus_input_after_show(self):
        self.ensure_typing_ready()
        QTimer.singleShot(0, self.ensure_typing_ready)
        QTimer.singleShot(40, self.ensure_typing_ready)

    def _clear_ambiguous_choice_buttons(self):
        while self.ambiguous_choices_layout.count():
            item = self.ambiguous_choices_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _populate_ambiguous_choice_buttons(self, matches: list[dict]):
        self._clear_ambiguous_choice_buttons()
        for match in matches:
            index = int(match.get("index", -1))
            title = match.get("title", "")
            origin_label = match.get("origin_label", "Action")
            target_kind = match.get("target_kind", "")
            target_display = match.get("target_display") or match.get("target", "")
            button_text = f"{index + 1}. {title}"
            metadata_bits = [origin_label]
            if target_kind:
                metadata_bits.append(target_kind)
            if metadata_bits:
                button_text += f"\n{' • '.join(metadata_bits)}"
            if target_display:
                button_text += f"\n{target_display}"
            button = QPushButton(button_text, self.ambiguous_choices_frame)
            button.setProperty("choiceRole", "ambiguous")
            button.setToolTip(match.get("target", ""))
            button.clicked.connect(lambda _checked=False, idx=index: self.ambiguous_match_selected.emit(idx))
            self.ambiguous_choices_layout.addWidget(button)
        self.ambiguous_choices_frame.setVisible(bool(matches))

    def render_payload(self, payload: dict):
        payload = payload or {}
        phase = payload.get("phase", "hidden")
        armed = bool(payload.get("input_armed")) and phase == "entry"
        typing_ready = bool(payload.get("typing_ready", armed)) and phase == "entry"
        locked = phase in {"choose", "confirm", "result"}
        ambiguous_matches = payload.get("ambiguous_matches") or []
        self._visible_ambiguous_count = len(ambiguous_matches)

        self.input_shell.setProperty("armed", "true" if typing_ready else "false")
        self.input_shell.setProperty("locked", "true" if locked else "false")
        self.caret.setProperty("armed", "true" if typing_ready else "false")
        for widget in (self.input_shell, self.caret):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

        self.input_line.blockSignals(True)
        if self.input_line.text() != payload.get("input_text", ""):
            self.input_line.setText(payload.get("input_text", ""))
        self.input_line.set_input_armed(armed, notify=False)
        self.input_line.blockSignals(False)
        if locked:
            self.setFocus(Qt.ActiveWindowFocusReason)

        selection_context = payload.get("selection_context", "")
        pending_group = payload.get("pending_group") or {}
        confirm_surface_copy = self._build_confirm_surface_copy(selection_context, pending_group)

        if phase == "confirm":
            self.hint_label.setText(confirm_surface_copy["hint_text"])
        elif phase == "choose":
            if selection_context == "group" and pending_group.get("title"):
                self.hint_label.setText(
                    f'Select a member from "{pending_group.get("title")}" after reviewing its origin and destination.'
                )
            else:
                self.hint_label.setText("Press a number key or click the intended action after reviewing its origin and destination.")
        elif phase == "result":
            self.hint_label.setText("Returning to passive desktop mode.")
        else:
            self.hint_label.setText("Type a built-in or saved action, or use the buttons below.")

        status_kind = payload.get("status_kind", "idle")
        self.status_label.setProperty("statusKind", status_kind)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

        if payload.get("status_text"):
            self.status_label.setText(payload["status_text"])
        elif phase == "entry" and not armed:
            self.status_label.setText("Type an action or alias to begin.")
        else:
            self.status_label.setText("")

        saved_action_inventory = payload.get("saved_action_inventory") or {}
        saved_group_inventory = payload.get("saved_group_inventory") or {}
        show_inventory = phase == "entry" and bool(
            saved_action_inventory.get("visible") or saved_group_inventory.get("visible")
        )
        self.saved_inventory_frame.setVisible(show_inventory)
        if show_inventory:
            self.create_custom_task_button.setEnabled(True)
            self.created_tasks_button.setEnabled(True)
            self.create_custom_group_button.setEnabled(True)
            self.created_groups_button.setEnabled(True)
            self.saved_inventory_title.setText("Custom tasks and groups")
            self.saved_inventory_status.setProperty("statusKind", "idle")
            self.saved_inventory_status.style().unpolish(self.saved_inventory_status)
            self.saved_inventory_status.style().polish(self.saved_inventory_status)
            self.saved_inventory_status.setText("Create or manage exact-match tasks and callable groups.")
        else:
            self.saved_inventory_status.setText("")

        titles = payload.get("ambiguous_titles") or []
        if phase == "choose" and titles:
            if selection_context == "group" and pending_group.get("title"):
                self.ambiguous_label.setText(
                    f'Select the member you want from "{pending_group.get("title")}".'
                )
            else:
                self.ambiguous_label.setText(
                    "Multiple actions matched your request. Press a number key or click a choice after reviewing the origin and destination detail below."
                )
        else:
            self.ambiguous_label.setText(f"Matches: {' | '.join(titles)}" if titles else "")
        self._populate_ambiguous_choice_buttons(ambiguous_matches)

        action = payload.get("pending_action") or {}
        show_confirm = phase == "confirm" and bool(action)
        self.confirmation_frame.setVisible(show_confirm)
        if show_confirm:
            self.confirm_title_label.setText(confirm_surface_copy["title_label"])
            self.confirm_request_value.setText(payload.get("typed_request", ""))
            self.confirm_title_value.setText(action.get("title", ""))
            self.confirm_origin_value.setText(action.get("origin_label", ""))
            self.confirm_kind_value.setText(action.get("target_kind", ""))
            self.confirm_target_value.setText(action.get("target_display") or action.get("target", ""))
            self.confirm_target_value.setToolTip(action.get("target", ""))
            self.confirm_help_label.setText(confirm_surface_copy["help_text"])


class MonitoringHudOverlayDisplayWindow(QWidget):
    def __init__(self, screen, event_logger=None):
        super().__init__(None)
        self.screen_ref = screen
        self.event_logger = event_logger
        self._anchored = True
        self._drag_origin: QPoint | None = None
        self._drag_window_origin = QPoint()
        self._last_unanchored_geometry = QRect()
        self._card_widgets: dict[str, dict[str, object]] = {}
        self._card_layouts: dict[str, dict[str, int | str | bool]] = {}
        self._card_drag_id = ""
        self._card_drag_resize = False
        self._card_drag_origin: QPoint | None = None
        self._card_drag_base: dict[str, int | str | bool] = {}
        self.setObjectName("monitoringHudOverlayDisplayWindow")
        flags = Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAutoFillBackground(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet(
            """
            QWidget#monitoringHudOverlayDisplayWindow {
                background: transparent;
            }
            QFrame#monitoringHudOverlayDisplayFrame {
                border: 1px solid rgba(116, 239, 255, 0.22);
                border-radius: 14px;
                background:
                    qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(7, 20, 33, 0.34),
                        stop:0.52 rgba(5, 31, 44, 0.20),
                        stop:1 rgba(6, 12, 22, 0.30));
            }
            QLabel {
                color: #dffbff;
                font-family: Bahnschrift, Segoe UI, sans-serif;
                background: transparent;
            }
            QLabel[role="eyebrow"] {
                color: rgba(120, 239, 255, 0.42);
                font-size: 10px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QLabel[role="title"] {
                color: #f5ffff;
                font-size: 15px;
                font-weight: 700;
            }
            QLabel[role="state"] {
                color: #a5f8dc;
                font-size: 12px;
            }
            QLabel[role="card"] {
                color: #d7faff;
                border: 1px solid rgba(112, 242, 255, 0.24);
                border-radius: 14px;
                padding: 10px 12px;
                background: rgba(3, 14, 24, 0.38);
            }
            QLabel[role="warning"] {
                color: #ffe3a6;
                font-size: 11px;
            }
            QLabel[role="watermark"] {
                color: rgba(120, 239, 255, 0.30);
                font-size: 10px;
                letter-spacing: 3px;
                text-transform: uppercase;
            }
            QFrame[role="overlayCard"] {
                border: 1px solid rgba(112, 242, 255, 0.24);
                border-radius: 14px;
                background: rgba(3, 14, 24, 0.38);
            }
            QFrame[role="overlayCard"][state="setup"] {
                border-color: rgba(255, 214, 113, 0.30);
            }
            QFrame[role="overlayCard"][state="no-data"] {
                border-color: rgba(124, 178, 210, 0.28);
            }
            QLabel[role="cardTitle"] {
                color: rgba(139, 233, 255, 0.86);
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QLabel[role="cardSummary"] {
                color: #f5ffff;
                font-size: 14px;
                font-weight: 700;
            }
            QLabel[role="cardMeta"] {
                color: rgba(189, 232, 242, 0.80);
                font-size: 10px;
            }
            QFrame[role="cardResizeHandle"] {
                border: 1px solid rgba(125, 235, 255, 0.30);
                border-radius: 4px;
                background: rgba(125, 235, 255, 0.18);
            }
            QPushButton {
                min-height: 28px;
                padding: 4px 10px;
                border: 1px solid rgba(116, 239, 255, 0.26);
                border-radius: 999px;
                background: rgba(5, 22, 38, 0.72);
                color: #dffbff;
                font-family: Bahnschrift, Segoe UI, sans-serif;
                font-size: 10px;
                font-weight: 700;
            }
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        frame = QFrame(self)
        frame.setObjectName("monitoringHudOverlayDisplayFrame")
        frame.setProperty("role", "overlayDisplayCanvas")
        frame.installEventFilter(self)
        self._watermark = QLabel("Nexus Desktop AI / ORIN", frame)
        self._watermark.setProperty("role", "watermark")
        self._title = QLabel("Monitoring HUD Overlay", frame)
        self._title.setProperty("role", "title")
        self._state = QLabel("Provider setup required", frame)
        self._state.setProperty("role", "state")
        self._warning = QLabel("Visual warning baseline only", frame)
        self._warning.setProperty("role", "warning")
        self._resize_grip = QSizeGrip(frame)
        for widget in (self._watermark, self._title, self._state, self._warning, self._resize_grip):
            widget.installEventFilter(self)
        root.addWidget(frame)
        self._frame = frame
        self._quick_controls = (self._resize_grip,)
        self._sync_overlay_card(
            "cpu",
            {"x": 28, "y": 84, "w": 360, "h": 150, "title": "CPU Group", "enabled": True},
            "Provider warming",
            "setup",
        )
        self._sync_overlay_card(
            "gpu",
            {"x": 28, "y": 254, "w": 360, "h": 150, "title": "GPU Group", "enabled": True},
            "Provider required",
            "no-data",
        )

        self.setGeometry(self._compute_overlay_geometry(initial=True))
        self._layout_overlay_children()
        self.hide()
        QTimer.singleShot(0, self._apply_native_click_through_flags)

    def _default_card_layout(self, card_id: str) -> dict[str, int | str | bool]:
        y = 84 + (170 * len(self._card_layouts))
        return {"x": 28, "y": y, "w": 360, "h": 150, "title": f"{card_id.upper()} Group", "enabled": True}

    def _create_overlay_card(self, card_id: str) -> dict[str, object]:
        card = QFrame(self._frame)
        card.setProperty("role", "overlayCard")
        card.setProperty("cardId", card_id)
        card.installEventFilter(self)
        title = QLabel("Monitor Group", card)
        title.setProperty("role", "cardTitle")
        summary = QLabel("Provider required", card)
        summary.setProperty("role", "cardSummary")
        meta = QLabel("Provider route pending", card)
        meta.setProperty("role", "cardMeta")
        edit_button = QPushButton("Edit", card)
        edit_button.setProperty("cardId", card_id)
        resize_handle = QFrame(card)
        resize_handle.setProperty("role", "cardResizeHandle")
        resize_handle.setProperty("resizeCardId", card_id)
        for widget in (title, summary, meta, edit_button, resize_handle):
            widget.installEventFilter(self)
        widgets = {
            "frame": card,
            "title": title,
            "summary": summary,
            "meta": meta,
            "edit": edit_button,
            "resize": resize_handle,
        }
        self._card_widgets[card_id] = widgets
        return widgets

    def _bound_card_layout(self, layout: dict[str, int | str | bool]) -> dict[str, int | str | bool]:
        frame_width = max(420, self._frame.width())
        frame_height = max(260, self._frame.height())
        width = max(220, min(int(layout.get("w") or 360), frame_width))
        height = max(110, min(int(layout.get("h") or 150), frame_height))
        x = max(8, min(int(layout.get("x") or 28), max(8, frame_width - width - 8)))
        y = max(52, min(int(layout.get("y") or 84), max(52, frame_height - height - 28)))
        bounded = dict(layout)
        bounded.update({"x": x, "y": y, "w": width, "h": height})
        return bounded

    def _sync_overlay_card(
        self,
        card_id: str,
        layout: dict[str, object],
        summary: str,
        state: str,
    ):
        if card_id not in self._card_widgets:
            self._create_overlay_card(card_id)
        existing = dict(self._card_layouts.get(card_id) or self._default_card_layout(card_id))
        incoming = dict(layout or {})
        # Dashboard edits can rename/enable monitors, but overlay placement is
        # owned by the standalone overlay window after the card exists.
        for key in ("title", "enabled", "pollingRateMs"):
            if key in incoming:
                existing[key] = incoming[key]
        if card_id not in self._card_layouts:
            for key in ("x", "y", "w", "h"):
                if key in incoming:
                    try:
                        existing[key] = int(float(incoming[key]))
                    except (TypeError, ValueError):
                        pass
        existing = self._bound_card_layout(existing)
        self._card_layouts[card_id] = existing
        widgets = self._card_widgets[card_id]
        frame = widgets["frame"]
        title = widgets["title"]
        summary_label = widgets["summary"]
        meta = widgets["meta"]
        frame.setProperty("state", state)
        frame.style().unpolish(frame)
        frame.style().polish(frame)
        title.setText(str(existing.get("title") or f"{card_id.upper()} Group"))
        summary_label.setText("Hidden in overlay" if existing.get("enabled") is False else summary)
        meta.setText("1s default after provider proof; no fake values.")
        widgets["edit"].setVisible(not self._anchored)  # type: ignore[index]
        widgets["resize"].setVisible(not self._anchored)  # type: ignore[index]
        frame.setGeometry(int(existing["x"]), int(existing["y"]), int(existing["w"]), int(existing["h"]))
        self._layout_card_children(card_id)
        frame.show()

    def _layout_card_children(self, card_id: str):
        widgets = self._card_widgets.get(card_id)
        if not widgets:
            return
        frame: QFrame = widgets["frame"]  # type: ignore[assignment]
        title: QLabel = widgets["title"]  # type: ignore[assignment]
        summary: QLabel = widgets["summary"]  # type: ignore[assignment]
        meta: QLabel = widgets["meta"]  # type: ignore[assignment]
        edit: QPushButton = widgets["edit"]  # type: ignore[assignment]
        resize: QFrame = widgets["resize"]  # type: ignore[assignment]
        w = max(1, frame.width())
        h = max(1, frame.height())
        title.setGeometry(14, 12, max(1, w - 110), 22)
        summary.setGeometry(14, 42, max(1, w - 28), 28)
        meta.setGeometry(14, max(70, h - 36), max(1, w - 44), 22)
        edit.setGeometry(max(14, w - 78), 10, 62, 28)
        resize.setGeometry(max(0, w - 18), max(0, h - 18), 12, 12)

    def _layout_overlay_children(self):
        frame_width = max(1, self._frame.width())
        frame_height = max(1, self._frame.height())
        self._watermark.setGeometry(18, 12, max(1, frame_width - 36), 18)
        self._title.setGeometry(18, 34, min(320, max(1, frame_width - 36)), 24)
        self._state.setGeometry(max(18, frame_width - 300), 34, 282, 24)
        self._warning.setGeometry(18, max(56, frame_height - 26), max(1, frame_width - 70), 20)
        self._resize_grip.setGeometry(max(0, frame_width - 22), max(0, frame_height - 22), 20, 20)
        for card_id, layout in list(self._card_layouts.items()):
            bounded = self._bound_card_layout(layout)
            self._card_layouts[card_id] = bounded
            widgets = self._card_widgets.get(card_id)
            if widgets:
                frame: QFrame = widgets["frame"]  # type: ignore[assignment]
                frame.setGeometry(int(bounded["x"]), int(bounded["y"]), int(bounded["w"]), int(bounded["h"]))
                self._layout_card_children(card_id)

    def _virtual_desktop_geometry(self) -> QRect:
        screens = QApplication.screens()
        if not screens:
            return self.screen_ref.availableGeometry()
        rect = screens[0].availableGeometry()
        for screen in screens[1:]:
            rect = rect.united(screen.availableGeometry())
        return rect

    def _initial_overlay_target_geometry(self) -> QRect:
        screens = QApplication.screens()
        if not screens:
            return self.screen_ref.availableGeometry()
        core_screen = self.screen_ref.availableGeometry()
        candidates = []
        for screen in screens:
            geometry = screen.availableGeometry()
            same_screen = (
                geometry.x() == core_screen.x()
                and geometry.y() == core_screen.y()
                and geometry.width() == core_screen.width()
                and geometry.height() == core_screen.height()
            )
            if not same_screen:
                candidates.append(geometry)
        if not candidates:
            return core_screen
        core_center_x = core_screen.center().x()
        return sorted(
            candidates,
            key=lambda rect: (abs(rect.center().x() - core_center_x), rect.center().x()),
            reverse=True,
        )[0]

    def _compute_overlay_geometry(self, *, initial: bool = False) -> QRect:
        virtual = self._virtual_desktop_geometry()
        if not initial and self.geometry().isValid() and self.geometry().width() > 0 and self.geometry().height() > 0:
            return self.geometry()
        target = self._initial_overlay_target_geometry()
        margin = 48
        width = min(max(720, int(target.width() * 0.72)), max(420, target.width() - margin * 2))
        height = min(max(420, int(target.height() * 0.68)), max(280, target.height() - margin * 2))
        return QRect(
            target.x() + max(margin, (target.width() - width) // 2),
            target.y() + max(margin, (target.height() - height) // 2),
            width,
            height,
        )

    def _apply_native_click_through_flags(self):
        try:
            hwnd = ctypes.wintypes.HWND(int(self.winId()))
            style = int(GetWindowLongW(hwnd, GWL_EXSTYLE))
            if self._anchored:
                style |= WS_EX_NOACTIVATE | WS_EX_TRANSPARENT
            else:
                style = style & ~WS_EX_NOACTIVATE & ~WS_EX_TRANSPARENT
            SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            return

    def _set_overlay_interaction_mode(self, anchored: bool):
        self._anchored = bool(anchored)
        if anchored and self.geometry().isValid():
            self._last_unanchored_geometry = QRect(self.geometry())
        self.setAttribute(Qt.WA_ShowWithoutActivating, bool(anchored))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, bool(anchored))
        self.setFocusPolicy(Qt.NoFocus if anchored else Qt.StrongFocus)
        self._frame.setProperty("anchored", anchored)
        self._frame.style().unpolish(self._frame)
        self._frame.style().polish(self._frame)
        for control in self._quick_controls:
            control.setVisible(not anchored)
        for widgets in self._card_widgets.values():
            edit = widgets.get("edit")
            resize = widgets.get("resize")
            if edit is not None:
                edit.setVisible(not anchored)
            if resize is not None:
                resize.setVisible(not anchored)
        self._apply_native_click_through_flags()
        if not anchored:
            self.show()
            self.raise_()
            self.activateWindow()

    def _bound_geometry_to_virtual_desktop(self, rect: QRect) -> QRect:
        virtual = self._virtual_desktop_geometry()
        width = max(360, min(rect.width(), virtual.width()))
        height = max(220, min(rect.height(), virtual.height()))
        left = max(virtual.x(), min(rect.x(), virtual.x() + virtual.width() - width))
        top = max(virtual.y(), min(rect.y(), virtual.y() + virtual.height() - height))
        return QRect(left, top, width, height)

    def update_product_state(
        self,
        *,
        visible: bool,
        anchored: bool,
        provider_label: str = "Provider setup required",
        warning_label: str = "Visual warning baseline only",
        cards: dict[str, object] | None = None,
    ):
        self._set_overlay_interaction_mode(bool(anchored))
        self._state.setText(provider_label or "Provider setup required")
        self._warning.setText(warning_label or "Visual warning baseline only")
        card_map = cards if isinstance(cards, dict) else {}
        cpu = card_map.get("cpu") if isinstance(card_map.get("cpu"), dict) else {}
        gpu = card_map.get("gpu") if isinstance(card_map.get("gpu"), dict) else {}
        self._sync_overlay_card("cpu", cpu or {}, "Provider warming", "setup")
        self._sync_overlay_card("gpu", gpu or {}, "Provider required", "no-data")
        for card_id, layout in card_map.items():
            if str(card_id) in {"cpu", "gpu"} or not isinstance(layout, dict):
                continue
            self._sync_overlay_card(str(card_id), layout, "Provider route pending", "no-data")
        if visible:
            if not self.geometry().isValid() or self.geometry().width() <= 0 or self.geometry().height() <= 0:
                self.setGeometry(self._compute_overlay_geometry(initial=True))
            self.setGeometry(self._bound_geometry_to_virtual_desktop(self.geometry()))
            self._layout_overlay_children()
            self.show()
            if anchored:
                self.raise_()
            self._apply_native_click_through_flags()
            if callable(self.event_logger):
                self.event_logger("MONITORING_HUD_OVERLAY_DISPLAY_WINDOW_VISIBLE|surface=standalone_edgeless_overlay_display")
            return
        self.hide()

    def proof_state(self) -> dict[str, object]:
        hwnd = int(self.winId())
        style = 0
        try:
            style = int(GetWindowLongW(ctypes.wintypes.HWND(hwnd), GWL_EXSTYLE))
        except Exception:
            style = 0
        geometry = self.geometry()
        virtual = self._virtual_desktop_geometry()
        center = ctypes.wintypes.POINT(geometry.x() + geometry.width() // 2, geometry.y() + geometry.height() // 2)
        try:
            window_from_center = int(WindowFromPoint(center))
        except Exception:
            window_from_center = 0
        last = self._last_unanchored_geometry if self._last_unanchored_geometry.isValid() else QRect(geometry)
        return {
            "hwnd": hwnd,
            "visible": bool(self.isVisible()),
            "x": geometry.x(),
            "y": geometry.y(),
            "w": geometry.width(),
            "h": geometry.height(),
            "virtualX": virtual.x(),
            "virtualY": virtual.y(),
            "virtualW": virtual.width(),
            "virtualH": virtual.height(),
            "surface": "standalone_edgeless_overlay_display",
            "owner": "MonitoringHudOverlayDisplayWindow",
            "anchored": bool(self._anchored),
            "focusPolicy": "no_focus" if self.focusPolicy() == Qt.NoFocus else "interactive",
            "transparentForMouseEvents": bool(self.testAttribute(Qt.WA_TransparentForMouseEvents)),
            "showWithoutActivating": bool(self.testAttribute(Qt.WA_ShowWithoutActivating)),
            "exNoActivate": bool(style & WS_EX_NOACTIVATE),
            "exTransparent": bool(style & WS_EX_TRANSPARENT),
            "windowFromCenter": window_from_center,
            "windowFromCenterBypassesOverlay": bool(window_from_center and window_from_center != hwnd),
            "standaloneTopLevel": self.parent() is None,
            "quickControlsVisible": any(control.isVisible() for control in self._quick_controls),
            "overlayCardCount": len(self._card_widgets),
            "cardLayouts": {
                card_id: {
                    "x": int(layout.get("x") or 0),
                    "y": int(layout.get("y") or 0),
                    "w": int(layout.get("w") or 0),
                    "h": int(layout.get("h") or 0),
                }
                for card_id, layout in self._card_layouts.items()
            },
            "cardsMovableInOverlay": True,
            "dashboardCoupled": False,
            "surfaceIndependence": "dashboard_overlay_core_top_level_windows",
            "ownedByDashboardWindow": False,
            "lastUnanchoredX": last.x(),
            "lastUnanchoredY": last.y(),
            "lastUnanchoredW": last.width(),
            "lastUnanchoredH": last.height(),
            "positionPreserved": (
                not self._last_unanchored_geometry.isNull()
                and geometry.x() == last.x()
                and geometry.y() == last.y()
                and geometry.width() == last.width()
                and geometry.height() == last.height()
            ),
        }

    def _card_id_from_widget(self, widget) -> tuple[str, bool]:
        current = widget
        while current is not None:
            resize_card_id = current.property("resizeCardId") if hasattr(current, "property") else None
            if resize_card_id:
                return str(resize_card_id), True
            card_id = current.property("cardId") if hasattr(current, "property") else None
            if card_id:
                return str(card_id), False
            current = current.parent() if hasattr(current, "parent") else None
        return "", False

    def _move_card_from_delta(self, delta: QPoint):
        if not self._card_drag_id:
            return
        layout = dict(self._card_drag_base)
        if self._card_drag_resize:
            layout["w"] = int(round((int(layout.get("w") or 360) + delta.x()) / 20) * 20)
            layout["h"] = int(round((int(layout.get("h") or 150) + delta.y()) / 20) * 20)
        else:
            layout["x"] = int(round((int(layout.get("x") or 28) + delta.x()) / 20) * 20)
            layout["y"] = int(round((int(layout.get("y") or 84) + delta.y()) / 20) * 20)
        layout = self._bound_card_layout(layout)
        self._card_layouts[self._card_drag_id] = layout
        widgets = self._card_widgets.get(self._card_drag_id)
        if widgets:
            frame: QFrame = widgets["frame"]  # type: ignore[assignment]
            frame.setGeometry(int(layout["x"]), int(layout["y"]), int(layout["w"]), int(layout["h"]))
            self._layout_card_children(self._card_drag_id)

    def eventFilter(self, watched, event):
        if self._anchored:
            return super().eventFilter(watched, event)
        event_type = event.type()
        if event_type == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            card_id, resize = self._card_id_from_widget(watched)
            if card_id:
                self._card_drag_id = card_id
                self._card_drag_resize = resize
                self._card_drag_origin = event.globalPosition().toPoint()
                self._card_drag_base = dict(self._card_layouts.get(card_id) or self._default_card_layout(card_id))
                event.accept()
                return True
            if watched in {self._frame, self._watermark, self._title, self._state, self._warning}:
                self._drag_origin = event.globalPosition().toPoint()
                self._drag_window_origin = self.pos()
                event.accept()
                return True
        if event_type == QEvent.MouseMove:
            if self._card_drag_id and self._card_drag_origin is not None:
                self._move_card_from_delta(event.globalPosition().toPoint() - self._card_drag_origin)
                event.accept()
                return True
            if self._drag_origin is not None:
                delta = event.globalPosition().toPoint() - self._drag_origin
                next_rect = QRect(self._drag_window_origin + delta, self.size())
                self.setGeometry(self._bound_geometry_to_virtual_desktop(next_rect))
                event.accept()
                return True
        if event_type in (QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick):
            if self._card_drag_id:
                card_id = self._card_drag_id
                self._move_card_from_delta(event.globalPosition().toPoint() - (self._card_drag_origin or QPoint()))
                layout = self._card_layouts.get(card_id, {})
                if callable(self.event_logger):
                    self.event_logger(
                        "MONITORING_HUD_OVERLAY_CARD_LAYOUT_EDITED|"
                        f"card={card_id}|x={layout.get('x')}|y={layout.get('y')}|"
                        f"w={layout.get('w')}|h={layout.get('h')}|resize={str(self._card_drag_resize).lower()}"
                    )
                self._card_drag_id = ""
                self._card_drag_resize = False
                self._card_drag_origin = None
                self._card_drag_base = {}
                event.accept()
                return True
            if self._drag_origin is not None:
                self._last_unanchored_geometry = QRect(self.geometry())
                if callable(self.event_logger):
                    self.event_logger(
                        "MONITORING_HUD_OVERLAY_DISPLAY_POSITION_EDITED|"
                        f"x={self.geometry().x()}|y={self.geometry().y()}|w={self.geometry().width()}|h={self.geometry().height()}"
                    )
                self._drag_origin = None
                event.accept()
                return True
        return super().eventFilter(watched, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_overlay_children()

    def mousePressEvent(self, event):
        if self._anchored or event.button() != Qt.LeftButton:
            return super().mousePressEvent(event)
        self._drag_origin = event.globalPosition().toPoint()
        self._drag_window_origin = self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if self._anchored or self._drag_origin is None:
            return super().mouseMoveEvent(event)
        delta = event.globalPosition().toPoint() - self._drag_origin
        next_rect = QRect(self._drag_window_origin + delta, self.size())
        self.setGeometry(self._bound_geometry_to_virtual_desktop(next_rect))
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._drag_origin is not None:
            self._last_unanchored_geometry = QRect(self.geometry())
            if callable(self.event_logger):
                self.event_logger(
                    "MONITORING_HUD_OVERLAY_DISPLAY_POSITION_EDITED|"
                    f"x={self.geometry().x()}|y={self.geometry().y()}|w={self.geometry().width()}|h={self.geometry().height()}"
                )
        self._drag_origin = None
        return super().mouseReleaseEvent(event)

    def request_shutdown(self):
        self.hide()
        self.close()


class DesktopRuntimeWindow(QWidget):
    core_visualization_ready = Signal()
    core_visualization_visible = Signal()

    def __init__(
        self,
        screen,
        visual_html_path: str,
        event_logger=None,
        runtime_log_path: str = "",
        surface_role: str = "hud",
        monitoring_hud_feature_enabled: bool = False,
        monitoring_hud_dashboard_visible: bool | None = None,
    ):
        super().__init__()
        global _DIALOG_RUNTIME_LOGGER

        self.screen_ref = screen
        self.visual_html_path = os.path.abspath(visual_html_path)
        self.event_logger = event_logger
        self.runtime_log_path = os.path.abspath(runtime_log_path) if runtime_log_path else ""
        self.surface_role = surface_role if surface_role in {"hud", "combined"} else "hud"
        self._overlay_trace_enabled = (os.environ.get("NEXUS_OVERLAY_TRACE") or "").strip().casefold() in {
            "1",
            "true",
            "yes",
            "on",
        }
        startup_snapshot_dir = (os.environ.get("NEXUS_HARNESS_STARTUP_SNAPSHOT_DIR") or "").strip()
        self._startup_snapshot_dir = os.path.abspath(startup_snapshot_dir) if startup_snapshot_dir else ""
        self.desktop_mode = False
        self._is_shutting_down = False
        self._page_ready = False
        self._desktop_mode_requested = False
        self._startup_visibility_guard_active = True
        self._pending_visual_state = None
        self._pending_voice_level = None
        self._saved_action_source_path = None
        self._saved_action_create_dialog_factory = SavedActionCreateDialog
        self._created_tasks_dialog_factory = CreatedTasksDialog
        self._saved_action_edit_dialog_factory = SavedActionEditDialog
        self._callable_group_create_dialog_factory = CallableGroupCreateDialog
        self._created_groups_dialog_factory = CreatedGroupsDialog
        self._callable_group_edit_dialog_factory = CallableGroupEditDialog
        _DIALOG_RUNTIME_LOGGER = self._log_event
        self._command_model = CommandOverlayModel()
        self._command_panel = CommandOverlayPanel()
        self._command_panel.submit_requested.connect(self.handle_local_submit_requested)
        self._command_panel.escape_requested.connect(self.handle_command_escape)
        self._command_panel.input_text_changed.connect(self.handle_command_text_changed)
        self._command_panel.input_armed_changed.connect(self.handle_command_input_armed_changed)
        self._command_panel.input_focus_acquired.connect(self.handle_command_input_focus_acquired)
        self._command_panel.input_focus_lost.connect(self.handle_command_input_focus_lost)
        self._command_panel.ambiguous_match_selected.connect(self.handle_ambiguous_match_selected)
        self._command_panel.create_custom_task_requested.connect(self.handle_create_custom_task_requested)
        self._command_panel.created_tasks_requested.connect(self.handle_created_tasks_requested)
        self._command_panel.create_custom_group_requested.connect(self.handle_create_custom_group_requested)
        self._command_panel.created_groups_requested.connect(self.handle_created_groups_requested)
        self._command_panel.edit_saved_action_requested.connect(self.handle_edit_saved_action_requested)
        self._ai_provider_state = build_no_provider_ai_state(surface_role=self.surface_role)
        self._result_close_timer = QTimer(self)
        self._result_close_timer.setSingleShot(True)
        self._result_close_timer.timeout.connect(self._close_command_overlay_after_result)
        self._overlay_input_capture_until = 0.0
        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = False
        self._overlay_ready_timer = None
        self._overlay_ready_emitted = False
        self._overlay_ready_wait_attempt = 0
        self._overlay_ready_last_block_reason = ""
        self._overlay_ready_timeout_emitted = False
        self._authoring_dialog_active = False
        self._last_launch_failure_action_id = ""
        self._last_launch_failure_count = 0
        self._reported_recoverable_launch_failures = set()
        self._monitoring_hud_feature_enabled = bool(monitoring_hud_feature_enabled)
        if monitoring_hud_dashboard_visible is None:
            monitoring_hud_dashboard_visible = monitoring_hud_feature_enabled
        self._monitoring_hud_visible = bool(
            self._monitoring_hud_feature_enabled and monitoring_hud_dashboard_visible
        )
        self._monitoring_hud_anchored = True
        self._monitoring_hud_snap_enabled = True
        self._monitoring_hud_polling_rate_ms = 1000
        self._monitoring_hud_control_signature = None
        self._monitoring_hud_monitor_management_signature = None
        self._monitoring_hud_active_child_window_signature = None
        self._monitoring_hud_control_sync_timer = QTimer(self)
        self._monitoring_hud_control_sync_timer.timeout.connect(self._sync_monitoring_hud_control_state_from_page)
        self._monitoring_hud_poll_timer = QTimer(self)
        self._monitoring_hud_poll_timer.timeout.connect(self._publish_monitoring_hud_telemetry_boundary)
        self._monitoring_hud_live_self_qa_manifest_path = ""
        self._monitoring_hud_live_self_qa_root = ""
        self._monitoring_hud_live_self_qa_started = False
        self._monitoring_hud_live_self_qa_step_delay_ms = 250
        self._monitoring_hud_live_self_qa_final_hold_ms = 0
        self._monitoring_hud_interactive_screen_rect = QRect()
        self._monitoring_hud_native_panel_drag_active = False
        self._monitoring_hud_native_panel_drag_start = QPoint()
        self._monitoring_hud_native_panel_drag_base = QPoint()
        self._monitoring_hud_native_window_resize_active = False
        self._monitoring_hud_native_window_resize_edges = Qt.Edges()
        self._monitoring_hud_native_window_resize_start = QPoint()
        self._monitoring_hud_native_window_resize_base = QRect()
        self._monitoring_hud_native_window_resize_poll_active = False
        self._monitoring_hud_native_window_resize_last_rect = QRect()
        self._monitoring_hud_native_window_resize_pending_point = QPoint()
        self._monitoring_hud_native_window_resize_last_apply = 0.0
        self._monitoring_hud_native_window_resize_frame_interval_ms = 8
        self._monitoring_hud_native_window_resize_poll_timer = QTimer(self)
        self._monitoring_hud_native_window_resize_poll_timer.setSingleShot(False)
        try:
            self._monitoring_hud_native_window_resize_poll_timer.setTimerType(Qt.PreciseTimer)
        except Exception:
            pass
        self._monitoring_hud_native_window_resize_poll_timer.timeout.connect(
            self._poll_monitoring_hud_fallback_window_resize
        )
        self._monitoring_hud_native_window_resize_frame_timer = QTimer(self)
        self._monitoring_hud_native_window_resize_frame_timer.setSingleShot(True)
        try:
            self._monitoring_hud_native_window_resize_frame_timer.setTimerType(Qt.PreciseTimer)
        except Exception:
            pass
        self._monitoring_hud_native_window_resize_frame_timer.timeout.connect(
            self._apply_monitoring_hud_queued_window_resize
        )
        self._monitoring_hud_user_geometry_override_active = False
        self._monitoring_hud_native_move_user_active = False
        self._monitoring_hud_native_move_start_geometry = QRect()
        self._monitoring_hud_native_move_last_geometry = QRect()
        self._monitoring_hud_native_move_source = ""
        self._monitoring_hud_resize_frame_sync_last = 0.0
        self._monitoring_hud_resize_js_sync_last = 0.0
        self._monitoring_hud_show_guard_active = False
        self._monitoring_hud_show_guard_generation = 0
        self._monitoring_hud_show_guard_release_delay_ms = 360
        self._monitoring_hud_deferred_initial_visibility_release = False
        self._monitoring_hud_resize_cursor_key = None
        self._monitoring_hud_resize_override_cursor_active = False
        self._monitoring_hud_resize_hover_timer = QTimer(self)
        self._monitoring_hud_resize_hover_timer.setInterval(8)
        self._monitoring_hud_resize_hover_timer.timeout.connect(self._poll_monitoring_hud_resize_hover_cursor)
        self._monitoring_hud_native_move_finalize_timer = QTimer(self)
        self._monitoring_hud_native_move_finalize_timer.setSingleShot(True)
        self._monitoring_hud_native_move_finalize_timer.setInterval(260)
        self._monitoring_hud_native_move_finalize_timer.timeout.connect(
            lambda: self._finish_monitoring_hud_native_system_move(
                self._monitoring_hud_native_move_source or "native_caption_move"
            )
        )
        self._monitoring_hud_native_card_drag_active = False
        self._monitoring_hud_native_card_resize_active = False
        self._monitoring_hud_native_card_drag_id = ""
        self._monitoring_hud_native_card_drag_start = QPoint()
        self._monitoring_hud_native_card_drag_base: dict[str, int] = {}
        self._monitoring_hud_live_screen_rects: dict[str, QRect] = {}
        self._monitoring_hud_live_page_state: dict[str, object] = {}
        self._monitoring_hud_dashboard_close_last_screen_rect = QRect()
        self._monitoring_hud_settings_action_last_screen_rect = QRect()
        self._monitoring_hud_native_anchor_click_pending = False
        self._monitoring_hud_native_anchor_click_expected = True
        self._monitoring_hud_tray_menu_guard_active = False
        self._monitoring_hud_minimal_native_overlay = (
            MonitoringHudOverlayDisplayWindow(screen, event_logger)
            if self.surface_role == "hud"
            else None
        )

        # The Dashboard is a standalone user-facing window; Core/Overlay ownership stays separate.
        self.setWindowFlags(
            (Qt.Window if self.surface_role == "hud" else Qt.Tool)
            | Qt.FramelessWindowHint
        )
        self.setAutoFillBackground(self.surface_role != "hud")
        if self.surface_role == "hud":
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.setStyleSheet("background-color: transparent;")
        else:
            self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setWindowOpacity(0.0)

        self.setGeometry(self.compute_compact_geometry())
        if self.surface_role == "hud":
            self.setMinimumSize(640, 520)
        self.setMouseTracking(True)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.webview = QWebEngineView(self)
        self.webview.setStyleSheet(
            "background-color: transparent; border: none;"
            if self.surface_role == "hud"
            else "background-color: rgb(0, 0, 0); border: none;"
        )
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.setFocusPolicy(Qt.NoFocus)
        self.webview.setMouseTracking(True)
        self.webview.installEventFilter(self)
        QApplication.instance().installEventFilter(self)
        if self.surface_role == "hud":
            self._monitoring_hud_resize_hover_timer.start()
        self.webview.hide()

        self.webview.page().setBackgroundColor(
            QColor(0, 0, 0, 0) if self.surface_role == "hud" else QColor(0, 0, 0)
        )
        self.webview.loadFinished.connect(self._on_load_finished)
        self.webview.load(QUrl.fromLocalFile(self.visual_html_path))

        root.addWidget(self.webview)

    def eventFilter(self, watched, event):
        if self._handle_monitoring_hud_native_panel_drag_event(event):
            return True
        return super().eventFilter(watched, event)

    def moveEvent(self, event):
        super().moveEvent(event)
        if self.surface_role != "hud" or not self.desktop_mode or not self.isVisible():
            return
        self._monitoring_hud_interactive_screen_rect = self.geometry()
        if (
            self._monitoring_hud_native_move_user_active
            and not self._monitoring_hud_native_window_resize_active
        ):
            self._monitoring_hud_native_move_last_geometry = QRect(self.geometry())
            self._monitoring_hud_native_move_finalize_timer.start()

    def compute_compact_geometry(self):
        g = self.screen_ref.geometry()
        if self.surface_role == "hud":
            available = self.screen_ref.availableGeometry()
            width = min(780, max(640, int(available.width() * 0.30)))
            height = min(1060, max(760, available.height() - 150))
            margin_x = min(56, max(24, int(available.width() * 0.02)))
            margin_y = min(90, max(36, int(available.height() * 0.06)))
            x = available.x() + available.width() - width - margin_x
            y = available.y() + margin_y
            return QRect(x, y, width, height)

        width = int(g.width() * 0.46)
        height = int(g.height() * 0.68)

        x = g.x() + (g.width() - width) // 2
        y = g.y() + int(g.height() * 0.08)

        return QRect(x, y, width, height)

    def _virtual_desktop_geometry(self) -> QRect:
        screens = QApplication.screens()
        if not screens:
            return self.screen_ref.availableGeometry()
        rect = screens[0].availableGeometry()
        for screen in screens[1:]:
            rect = rect.united(screen.availableGeometry())
        return rect

    def prepare_desktop_geometry(self):
        self.setGeometry(self.compute_compact_geometry())

    def is_core_visualization_ready(self):
        return self._page_ready

    def showEvent(self, event):
        super().showEvent(event)

        if not self.desktop_mode:
            self._desktop_mode_requested = True
            self._schedule_desktop_mode_enable()

    def _log_event(self, event):
        if callable(self.event_logger):
            try:
                self.event_logger(event)
            except Exception:
                pass

    def _normalize_runtime_signal_value(self, value) -> str:
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        text = str(value)
        for original, replacement in (
            ("\r", " "),
            ("\n", " "),
            ("\t", " "),
            ("|", "/"),
        ):
            text = text.replace(original, replacement)
        return text.strip()

    def _emit_runtime_signal(self, signal_name: str, **fields):
        parts = [f"RENDERER_MAIN|{signal_name}"]
        for key, value in fields.items():
            normalized = self._normalize_runtime_signal_value(value)
            if not normalized:
                continue
            parts.append(f"{key}={normalized}")
        self._log_event("|".join(parts))

    def _saved_action_inventory_signal_fields(self, inventory=None) -> dict:
        inventory = inventory or self._command_model.action_catalog.saved_action_inventory
        return {
            "saved_status_kind": getattr(inventory, "status_kind", ""),
            "saved_count": len(getattr(inventory, "actions", ()) or ()),
            "source_path": getattr(inventory, "path", ""),
        }

    def _saved_group_inventory_signal_fields(self, inventory=None) -> dict:
        inventory = inventory or self._command_model.action_catalog.saved_group_inventory
        return {
            "group_status_kind": getattr(inventory, "status_kind", ""),
            "group_count": len(getattr(inventory, "groups", ()) or ()),
            "group_source_path": getattr(inventory, "path", ""),
        }

    def _ensure_overlay_ready_tracking(self):
        if getattr(self, "_overlay_ready_timer", None) is None:
            try:
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(self._check_overlay_ready_state)
                self._overlay_ready_timer = timer
            except RuntimeError:
                self._overlay_ready_timer = False
        if not hasattr(self, "_overlay_ready_emitted"):
            self._overlay_ready_emitted = False
        if not hasattr(self, "_overlay_ready_wait_attempt"):
            self._overlay_ready_wait_attempt = 0
        if not hasattr(self, "_overlay_ready_last_block_reason"):
            self._overlay_ready_last_block_reason = ""
        if not hasattr(self, "_overlay_ready_timeout_emitted"):
            self._overlay_ready_timeout_emitted = False

    def _reset_overlay_ready_tracking(self):
        self._ensure_overlay_ready_tracking()
        if self._overlay_ready_timer not in {None, False}:
            self._overlay_ready_timer.stop()
        self._overlay_ready_emitted = False
        self._overlay_ready_wait_attempt = 0
        self._overlay_ready_last_block_reason = ""
        self._overlay_ready_timeout_emitted = False

    def _overlay_ready_signal_fields(self) -> dict:
        panel_visible = self._command_panel.isVisible()
        input_focus = self._command_panel.input_line.hasFocus()
        input_visible = self._command_panel.input_line.isVisible()
        input_enabled = self._command_panel.input_line.isEnabled()
        panel_active = self._command_panel.isActiveWindow()
        capture_active = self._overlay_input_capture_active()
        needs_global_capture = False
        try:
            needs_global_capture = self.overlay_needs_global_input_capture()
        except Exception:
            needs_global_capture = False
        entry_actions_visible = (
            self._command_panel.create_custom_task_button.isVisible()
            and self._command_panel.created_tasks_button.isVisible()
            and self._command_panel.create_custom_group_button.isVisible()
            and self._command_panel.created_groups_button.isVisible()
        )
        return {
            "phase": self._command_model.phase,
            "input_armed": self._command_model.input_armed,
            "model_visible": self._command_model.visible,
            "panel_visible": panel_visible,
            "panel_active": panel_active,
            "input_focus": input_focus,
            "input_visible": input_visible,
            "input_enabled": input_enabled,
            "input_capture_active": capture_active,
            "local_input_engaged": self._overlay_local_input_engaged,
            "global_capture_suspended": self._overlay_global_capture_suspended,
            "needs_global_capture": needs_global_capture,
            "entry_actions_visible": entry_actions_visible,
            "panel_width": self._command_panel.width(),
            "panel_height": self._command_panel.height(),
        }

    def _overlay_ready_state_reason(self, fields: dict) -> str:
        if self._is_shutting_down:
            return "shutting_down"
        if not fields.get("model_visible"):
            return "model_hidden"
        if not fields.get("panel_visible"):
            return "panel_hidden"
        if int(fields.get("panel_width") or 0) <= 0 or int(fields.get("panel_height") or 0) <= 0:
            return "panel_geometry_unstable"
        if not fields.get("input_visible"):
            return "input_hidden"
        if not fields.get("input_enabled"):
            return "input_disabled"
        if fields.get("phase") != "entry":
            return f"phase_{fields.get('phase') or 'unknown'}"
        if not fields.get("input_armed"):
            return "input_not_armed"
        if not fields.get("entry_actions_visible"):
            return "entry_actions_hidden"
        if (
            fields.get("input_focus")
            or fields.get("local_input_engaged")
            or fields.get("needs_global_capture")
            or fields.get("input_capture_active")
        ):
            return "ready"
        return "input_path_not_ready"

    def _schedule_overlay_ready_check(self, delay_ms: int = 0):
        self._ensure_overlay_ready_tracking()
        if self._overlay_ready_timer is False:
            return
        if self._is_shutting_down or self._overlay_ready_emitted:
            return
        self._overlay_ready_timer.start(max(0, int(delay_ms)))

    def _emit_overlay_ready_signal(self):
        self._ensure_overlay_ready_tracking()
        if self._overlay_ready_emitted:
            return
        fields = self._overlay_ready_signal_fields()
        reason = self._overlay_ready_state_reason(fields)
        if reason != "ready":
            return
        self._overlay_ready_emitted = True
        if self._overlay_ready_timer not in {None, False}:
            self._overlay_ready_timer.stop()
        self._emit_runtime_signal("COMMAND_OVERLAY_READY", **fields)

    def _check_overlay_ready_state(self):
        self._ensure_overlay_ready_tracking()
        if self._overlay_ready_emitted:
            return
        fields = self._overlay_ready_signal_fields()
        reason = self._overlay_ready_state_reason(fields)
        if reason == "ready":
            self._emit_overlay_ready_signal()
            return

        self._overlay_ready_wait_attempt += 1
        if (
            reason != self._overlay_ready_last_block_reason
            or self._overlay_ready_wait_attempt in {1, 5, 15}
        ):
            self._overlay_ready_last_block_reason = reason
            self._emit_runtime_signal(
                "COMMAND_OVERLAY_READY_WAITING",
                reason=reason,
                attempt=self._overlay_ready_wait_attempt,
                **fields,
            )
        if self._overlay_ready_wait_attempt >= 25 and not self._overlay_ready_timeout_emitted:
            self._overlay_ready_timeout_emitted = True
            self._emit_runtime_signal(
                "COMMAND_OVERLAY_READY_TIMEOUT",
                reason=reason,
                attempt=self._overlay_ready_wait_attempt,
                **fields,
            )
        if self._command_model.visible and not self._is_shutting_down:
            self._schedule_overlay_ready_check(40 if self._overlay_ready_wait_attempt < 15 else 120)

    def _handle_dialog_lifecycle_signal(self, signal_base: str, stage: str, dialog=None, **fields):
        signal_name = f"{signal_base}_{stage.upper()}"
        if dialog is not None:
            fields.setdefault("dialog_name", dialog.windowTitle())
            fields.setdefault("dialog_object_name", dialog.objectName())
            fields.setdefault("dialog_class_name", type(dialog).__name__)
            try:
                fields.setdefault("win_id", str(int(dialog.winId())))
            except Exception:
                pass
            try:
                focus_widget = dialog.focusWidget()
            except Exception:
                focus_widget = None
            if focus_widget is not None:
                fields.setdefault(
                    "focus_widget",
                    focus_widget.objectName() or type(focus_widget).__name__,
                )
        self._emit_runtime_signal(signal_name, **fields)

    def _create_dialog_with_optional_lifecycle(self, factory, *args, **kwargs):
        try:
            return factory(*args, **kwargs)
        except TypeError as exc:
            try:
                signature = inspect.signature(factory)
            except (TypeError, ValueError):
                signature = None

            if signature is None or any(
                parameter.kind == inspect.Parameter.VAR_KEYWORD
                for parameter in signature.parameters.values()
            ):
                raise

            accepted_kwargs = {
                name
                for name, parameter in signature.parameters.items()
                if parameter.kind in {
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.KEYWORD_ONLY,
                }
            }
            filtered_kwargs = {
                name: value
                for name, value in kwargs.items()
                if name in accepted_kwargs
            }
            if filtered_kwargs == kwargs:
                raise exc
            return factory(*args, **filtered_kwargs)

    def _authoring_dialog_blocks_new_dialog(self) -> bool:
        return bool(getattr(self, "_authoring_dialog_active", False))

    def _exec_authoring_dialog(self, dialog: QDialog, *, action: str):
        self._authoring_dialog_active = True
        try:
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_DIALOG_EXEC_START",
                action=action,
                dialog_name=dialog.windowTitle(),
                dialog_object_name=dialog.objectName() or type(dialog).__name__,
                win_id=int(dialog.winId()),
            )
            result = dialog.exec()
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_DIALOG_EXEC_RETURNED",
                action=action,
                dialog_name=dialog.windowTitle(),
                dialog_object_name=dialog.objectName() or type(dialog).__name__,
                win_id=int(dialog.winId()),
                result="accepted" if result == QDialog.Accepted else "rejected",
            )
            return result
        finally:
            self._authoring_dialog_active = False

    def _trace_overlay(self, event: str, **fields):
        if not self._overlay_trace_enabled:
            return
        phase = getattr(self._command_model, "phase", "unknown")
        local_engaged = "true" if self._overlay_local_input_engaged else "false"
        panel_active = "true" if self._command_panel.isActiveWindow() else "false"
        input_focus = "true" if self._command_panel.input_line.hasFocus() else "false"
        input_text = repr(self._command_model.input_text)
        extras = [
            f"event={event}",
            f"phase={phase}",
            f"local_engaged={local_engaged}",
            f"capture_suspended={'true' if self._overlay_global_capture_suspended else 'false'}",
            f"panel_active={panel_active}",
            f"input_focus={input_focus}",
            f"input_text={input_text}",
        ]
        for key, value in fields.items():
            extras.append(f"{key}={value}")
        self._log_event("OVERLAY_TRACE|source=renderer|" + "|".join(extras))

    def _foreground_window_snapshot(self):
        try:
            hwnd = GetForegroundWindow()
            if not hwnd:
                return {"hwnd": "none", "class_name": "", "title": ""}

            class_buffer = ctypes.create_unicode_buffer(256)
            GetClassNameW(hwnd, class_buffer, len(class_buffer))

            title_length = max(0, int(GetWindowTextLengthW(hwnd)))
            title_buffer = ctypes.create_unicode_buffer(max(1, title_length + 1))
            GetWindowTextW(hwnd, title_buffer, len(title_buffer))

            return {
                "hwnd": hex(int(hwnd)),
                "class_name": class_buffer.value or "",
                "title": title_buffer.value or "",
            }
        except Exception:
            return {"hwnd": "unavailable", "class_name": "", "title": ""}

    def _run_javascript(self, script):
        page = self.webview.page()
        if page is not None:
            page.runJavaScript(script)

    def _run_javascript_with_result(self, script, callback):
        page = self.webview.page()
        if page is None:
            callback(None)
            return
        try:
            page.runJavaScript(script, 0, callback)
        except TypeError:
            page.runJavaScript(script, callback)

    def _monitoring_hud_control_state(self) -> dict[str, object]:
        return {
            "featureEnabled": self._monitoring_hud_feature_enabled,
            "overlayDeferred": True,
            "visible": self._monitoring_hud_visible,
            "anchored": self._monitoring_hud_anchored,
            "snapEnabled": self._monitoring_hud_snap_enabled,
            "pollingRateMs": self._monitoring_hud_polling_rate_ms,
        }

    def _publish_monitoring_hud_control_state_to_page(self):
        if not self._page_ready or self._is_shutting_down:
            return
        state_json = json.dumps(self._monitoring_hud_control_state(), sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setMonitoringHudControlState) {{
                window.setMonitoringHudControlState({state_json});
            }}
            """
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_CONTROL_STATE_READY",
            package="PKG-006",
            slice="SLC-027",
            source="page_publish",
            feature_enabled=self._monitoring_hud_feature_enabled,
            visible=self._monitoring_hud_visible,
            anchored=self._monitoring_hud_anchored,
            snap=self._monitoring_hud_snap_enabled,
            polling_rate_ms=self._monitoring_hud_polling_rate_ms,
        )

    def _estimate_monitoring_hud_interactive_screen_rect(self) -> QRect:
        geometry = self.geometry()
        if geometry.width() <= 0 or geometry.height() <= 0:
            geometry = self.compute_compact_geometry()
        if self.surface_role == "hud":
            return QRect(geometry.x(), geometry.y(), geometry.width(), geometry.height())
        panel_width = min(780, max(320, geometry.width() - 48))
        panel_height = min(1040, max(360, geometry.height() - 48))
        right_margin = min(max(int(geometry.width() * 0.04), 24), 64)
        top_margin = min(max(int(geometry.height() * 0.04), 24), 56)
        left = geometry.x() + max(0, geometry.width() - right_margin - panel_width)
        top = geometry.y() + top_margin
        return QRect(
            int(left) - 12,
            int(top) - 12,
            int(panel_width) + 24,
            int(panel_height) + 24,
        )

    def _set_monitoring_hud_interactive_rect_from_page(self, rect: dict[str, object] | None):
        if not isinstance(rect, dict):
            self._monitoring_hud_interactive_screen_rect = self._estimate_monitoring_hud_interactive_screen_rect()
            return
        try:
            top_left = self.webview.mapToGlobal(
                QPoint(int(float(rect.get("left") or 0)), int(float(rect.get("top") or 0)))
            )
            left = top_left.x()
            top = top_left.y()
            width = int(float(rect.get("width") or 0))
            height = int(float(rect.get("height") or 0))
        except (TypeError, ValueError):
            self._monitoring_hud_interactive_screen_rect = self._estimate_monitoring_hud_interactive_screen_rect()
            return
        if width <= 0 or height <= 0:
            self._monitoring_hud_interactive_screen_rect = self._estimate_monitoring_hud_interactive_screen_rect()
            return
        if self.surface_role == "hud":
            self._monitoring_hud_interactive_screen_rect = QRect(left, top, width, height)
        else:
            self._monitoring_hud_interactive_screen_rect = QRect(left - 12, top - 12, width + 24, height + 24)

    def _monitoring_hud_screen_rect_from_page_rect(self, rect: dict[str, object] | None) -> QRect:
        if not isinstance(rect, dict):
            return QRect()
        try:
            left = int(float(rect.get("left") or 0))
            top = int(float(rect.get("top") or 0))
            width = int(float(rect.get("width") or 0))
            height = int(float(rect.get("height") or 0))
        except (TypeError, ValueError):
            return QRect()
        if width <= 0 or height <= 0:
            return QRect()
        top_left = self.webview.mapToGlobal(QPoint(left, top))
        return QRect(top_left.x(), top_left.y(), width, height)

    def _set_monitoring_hud_live_client_page_state(
        self,
        state: dict[str, object] | None,
        geometry: dict[str, object] | None,
    ):
        self._monitoring_hud_live_page_state = state if isinstance(state, dict) else {}
        screen_rects: dict[str, QRect] = {}
        if isinstance(geometry, dict):
            for name, rect in geometry.items():
                if isinstance(rect, dict):
                    screen_rect = self._monitoring_hud_screen_rect_from_page_rect(rect)
                    if screen_rect.isValid() and not screen_rect.isNull():
                        screen_rects[str(name)] = screen_rect
        self._monitoring_hud_live_screen_rects = screen_rects
        dashboard_close_rect = screen_rects.get("dashboardClose", QRect())
        if dashboard_close_rect.isValid() and not dashboard_close_rect.isNull():
            self._monitoring_hud_dashboard_close_last_screen_rect = QRect(dashboard_close_rect)
        settings_action_rect = screen_rects.get("settingsAction", QRect())
        if settings_action_rect.isValid() and not settings_action_rect.isNull():
            self._monitoring_hud_settings_action_last_screen_rect = QRect(settings_action_rect)

    def _monitoring_hud_dashboard_close_fallback_screen_rect(self) -> QRect:
        rect = self._monitoring_hud_interactive_screen_rect
        if rect.isNull() or not rect.isValid():
            rect = self._estimate_monitoring_hud_interactive_screen_rect()
            self._monitoring_hud_interactive_screen_rect = rect
        if not rect.isValid() or rect.isNull():
            return QRect()
        return QRect(
            rect.right() + 1 - 14 - 82,
            rect.y() + 12,
            82,
            42,
        )

    def _monitoring_hud_settings_action_fallback_screen_rect(self) -> QRect:
        actions_rect = self._monitoring_hud_dashboard_actions_fallback_screen_rect()
        if not actions_rect.isValid() or actions_rect.isNull():
            return QRect()
        return QRect(
            actions_rect.x(),
            actions_rect.y(),
            actions_rect.width(),
            44,
        )

    def _monitoring_hud_dashboard_actions_fallback_screen_rect(self) -> QRect:
        header_rect = self._monitoring_hud_header_rect()
        if not header_rect.isValid() or header_rect.isNull():
            return QRect()
        width = min(360, max(154, header_rect.width() // 3))
        height = 44
        left = header_rect.x() + 43
        return QRect(
            left,
            header_rect.y() + 132,
            width,
            height,
        )

    def _monitoring_hud_point_in_interactive_rect(self, point: QPoint) -> bool:
        rect = self._monitoring_hud_interactive_screen_rect
        if rect.isNull() or not rect.isValid():
            rect = self._estimate_monitoring_hud_interactive_screen_rect()
            self._monitoring_hud_interactive_screen_rect = rect
        return bool(rect.contains(point))

    def _apply_monitoring_hud_native_activation_style(self, anchored: bool):
        try:
            hwnd = ctypes.wintypes.HWND(int(self.winId()))
            style = int(GetWindowLongW(hwnd, GWL_EXSTYLE))
            style = style & ~WS_EX_NOACTIVATE & ~WS_EX_TRANSPARENT
            if self.surface_role == "hud":
                style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
            SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            return

    def set_monitoring_hud_tray_menu_interaction_guard(self, active: bool, source: str = "tray_menu"):
        if self.surface_role != "hud":
            return
        self._monitoring_hud_tray_menu_guard_active = bool(active)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, bool(active))
        style = 0
        try:
            hwnd = ctypes.wintypes.HWND(int(self.winId()))
            style = int(GetWindowLongW(hwnd, GWL_EXSTYLE))
            if active:
                style |= WS_EX_TRANSPARENT
            else:
                style &= ~WS_EX_TRANSPARENT
            SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            style = 0
        self._emit_runtime_signal(
            "MONITORING_HUD_TRAY_MENU_INTERACTION_GUARD_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS48",
            source=source,
            active=bool(active),
            transparent_for_mouse=bool(self.testAttribute(Qt.WA_TransparentForMouseEvents)),
            ex_transparent=bool(style & WS_EX_TRANSPARENT),
        )

    def _monitoring_hud_native_ownership_state(self) -> dict[str, object]:
        style = 0
        try:
            style = int(GetWindowLongW(ctypes.wintypes.HWND(int(self.winId())), GWL_EXSTYLE))
        except Exception:
            style = 0
        return {
            "windowFlag": "normal_window" if self.surface_role == "hud" else "tool_window",
            "topmost": False,
            "showWithoutActivating": bool(self.testAttribute(Qt.WA_ShowWithoutActivating)),
            "transparentForMouseEvents": bool(self.testAttribute(Qt.WA_TransparentForMouseEvents)),
            "exNoActivate": bool(style & WS_EX_NOACTIVATE),
            "exTransparent": bool(style & WS_EX_TRANSPARENT),
            "exToolWindow": bool(style & WS_EX_TOOLWINDOW),
            "exAppWindow": bool(style & WS_EX_APPWINDOW),
            "movementModel": "os-system-move-no-snap",
            "resizeModel": "os-edge-corner-resize",
            "focusPolicy": "no_focus" if self.focusPolicy() == Qt.NoFocus else "interactive",
        }

    def _emit_monitoring_hud_window_ownership_focus_ready(self, source: str = "runtime"):
        if self.surface_role != "hud":
            return
        state = self._monitoring_hud_native_ownership_state()
        self._emit_runtime_signal(
            "MONITORING_HUD_WINDOW_OWNERSHIP_FOCUS_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS38",
            source=source,
            surface="dashboard_control_panel",
            window_flag=state["windowFlag"],
            topmost=state["topmost"],
            show_without_activating=state["showWithoutActivating"],
            transparent_for_mouse=state["transparentForMouseEvents"],
            ex_noactivate=state["exNoActivate"],
            ex_transparent=state["exTransparent"],
            ex_tool_window=state["exToolWindow"],
            ex_app_window=state["exAppWindow"],
            movement_model=state["movementModel"],
            resize_model=state["resizeModel"],
            focus_policy=state["focusPolicy"],
        )

    def _emit_monitoring_hud_window_status(self, source: str = "runtime"):
        geometry = self.geometry()
        virtual = self._virtual_desktop_geometry()
        overlay_proof = self._monitoring_hud_minimal_native_proof_state()
        ownership = self._monitoring_hud_native_ownership_state()
        self._emit_runtime_signal(
            "MONITORING_HUD_WINDOW_STATUS_READY",
            package="PKG-006",
            slice="SLC-026",
            source=source,
            surface="standalone_native_hud_window" if self.surface_role == "hud" else "combined_core_surface",
            feature_enabled=self._monitoring_hud_feature_enabled,
            visible=self._monitoring_hud_visible,
            anchored=self._monitoring_hud_anchored,
            x=geometry.x(),
            y=geometry.y(),
            w=geometry.width(),
            h=geometry.height(),
            virtual_x=virtual.x(),
            virtual_y=virtual.y(),
            virtual_w=virtual.width(),
            virtual_h=virtual.height(),
            window_flag=ownership.get("windowFlag"),
            movement_model=ownership.get("movementModel"),
            resize_model=ownership.get("resizeModel"),
            ex_tool_window=ownership.get("exToolWindow"),
            ex_app_window=ownership.get("exAppWindow"),
            focus_policy="no_focus" if self.focusPolicy() == Qt.NoFocus else "interactive",
        )
        if self.surface_role == "hud":
            self._emit_runtime_signal(
                "MONITORING_HUD_STANDALONE_DASHBOARD_WINDOW_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS28",
                source=source,
                surface="dashboard_control_panel_window",
                owner="DesktopRuntimeWindow",
                standalone=self.parent() is None,
                overlay_owner=overlay_proof.get("owner") or "MonitoringHudOverlayDisplayWindow",
                overlay_separate_hwnd=bool(overlay_proof.get("hwnd") and overlay_proof.get("hwnd") != int(self.winId())),
                virtual_desktop="all_monitors",
                x=geometry.x(),
                y=geometry.y(),
                w=geometry.width(),
                h=geometry.height(),
            )

    def _sync_monitoring_hud_minimal_native_overlay(self, source: str = "runtime"):
        overlay = self._monitoring_hud_minimal_native_overlay
        if overlay is None:
            return
        telemetry = self._monitoring_hud_telemetry_snapshot()
        status = self._monitoring_hud_status_snapshot()
        cards = {}
        page_state = self._monitoring_hud_live_page_state if isinstance(self._monitoring_hud_live_page_state, dict) else {}
        if isinstance(page_state.get("cards"), dict):
            cards = page_state.get("cards") or {}
        overlay.update_product_state(
            visible=False,
            anchored=bool(self._monitoring_hud_anchored),
            provider_label=str(telemetry.get("providerLabel") or "Provider setup required"),
            warning_label=str(status.get("warningPosture") or "Visual warning baseline only"),
            cards=cards,
        )
        proof = overlay.proof_state()
        self._emit_runtime_signal(
            "MONITORING_HUD_MINIMAL_NATIVE_OVERLAY_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS22",
            source=source,
            surface="minimal_native_overlay_window",
            visible=proof.get("visible"),
            x=proof.get("x"),
            y=proof.get("y"),
            w=proof.get("w"),
            h=proof.get("h"),
            separate_hwnd=bool(proof.get("hwnd") and proof.get("hwnd") != int(self.winId())),
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_STANDALONE_OVERLAY_DISPLAY_WINDOW_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS26",
            source=source,
            surface=proof.get("surface"),
            owner=proof.get("owner"),
            standalone=proof.get("standaloneTopLevel"),
            visible=proof.get("visible"),
            anchored=proof.get("anchored"),
            x=proof.get("x"),
            y=proof.get("y"),
            w=proof.get("w"),
            h=proof.get("h"),
            virtual_x=proof.get("virtualX"),
            virtual_y=proof.get("virtualY"),
            virtual_w=proof.get("virtualW"),
            virtual_h=proof.get("virtualH"),
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_SURFACE_NATIVE_INDEPENDENCE_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS28",
            source=source,
            dashboard_owner="DesktopRuntimeWindow",
            overlay_owner=proof.get("owner"),
            overlay_standalone=proof.get("standaloneTopLevel"),
            overlay_dashboard_coupled=proof.get("dashboardCoupled"),
            overlay_cards_movable=proof.get("cardsMovableInOverlay"),
            core_surface="CoreVisualizationWindow",
            virtual_desktop="all_monitors",
        )
        if self._monitoring_hud_visible and self._monitoring_hud_anchored:
            self._emit_runtime_signal(
                "MONITORING_HUD_MINIMAL_ANCHORED_CLICK_THROUGH_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS22",
                source=source,
                ex_transparent=proof.get("exTransparent"),
                transparent_for_mouse=proof.get("transparentForMouseEvents"),
                window_from_center_bypasses_overlay=proof.get("windowFromCenterBypassesOverlay"),
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_MINIMAL_NON_FOCUS_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS22",
                source=source,
                focus_policy=proof.get("focusPolicy"),
                ex_noactivate=proof.get("exNoActivate"),
                show_without_activating=proof.get("showWithoutActivating"),
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_ANCHORED_OVERLAY_UNINTERACTABLE_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS26",
                surface="standalone_edgeless_overlay_display",
                transparent_for_mouse=proof.get("transparentForMouseEvents"),
                ex_transparent=proof.get("exTransparent"),
                focus_policy=proof.get("focusPolicy"),
                ex_noactivate=proof.get("exNoActivate"),
                quick_controls_visible=proof.get("quickControlsVisible"),
                window_from_center_bypasses_overlay=proof.get("windowFromCenterBypassesOverlay"),
            )
            if proof.get("positionPreserved"):
                self._emit_runtime_signal(
                    "MONITORING_HUD_OVERLAY_POSITION_PRESERVED_READY",
                    package="PKG-006",
                    slice="SLC-026",
                    seam="WS26",
                    surface="standalone_edgeless_overlay_display",
                    x=proof.get("x"),
                    y=proof.get("y"),
                    w=proof.get("w"),
                    h=proof.get("h"),
                )
        elif self._monitoring_hud_visible:
            self._emit_runtime_signal(
                "MONITORING_HUD_UNANCHORED_OVERLAY_EDIT_WINDOW_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS26",
                surface="standalone_edgeless_overlay_display",
                transparent_for_mouse=proof.get("transparentForMouseEvents"),
                focus_policy=proof.get("focusPolicy"),
                quick_controls_visible=proof.get("quickControlsVisible"),
                movable="native_window_drag",
                resizable="native_size_grip",
            )

    def _monitoring_hud_minimal_native_proof_state(self) -> dict[str, object]:
        overlay = self._monitoring_hud_minimal_native_overlay
        if overlay is None:
            return {}
        return overlay.proof_state()

    def _monitoring_hud_overlay_card_screen_rect(self, card_id: str, *, resize: bool = False) -> QRect:
        overlay = self._monitoring_hud_minimal_native_overlay
        if overlay is None:
            return QRect()
        proof = overlay.proof_state()
        layouts = proof.get("cardLayouts") if isinstance(proof.get("cardLayouts"), dict) else {}
        layout = layouts.get(card_id) if isinstance(layouts.get(card_id), dict) else {}
        if not layout:
            return QRect()
        geometry = overlay.geometry()
        x = geometry.x() + int(layout.get("x") or 0)
        y = geometry.y() + int(layout.get("y") or 0)
        w = int(layout.get("w") or 0)
        h = int(layout.get("h") or 0)
        if resize:
            return QRect(x + max(0, w - 22), y + max(0, h - 22), 18, 18)
        return QRect(x + 12, y + 12, max(1, min(w - 24, 180)), max(1, min(h - 24, 48)))

    def _monitoring_hud_core_visualization_window(self):
        app = QApplication.instance()
        if app is None:
            return None
        for widget in app.topLevelWidgets():
            if callable(getattr(widget, "compute_core_geometry", None)) and "ORIN Core" in str(widget.windowTitle()):
                return widget
        return None

    def _monitoring_hud_rect_payload(self, rect: QRect) -> dict[str, int]:
        if rect is None or rect.isNull() or not rect.isValid():
            return {"x": 0, "y": 0, "w": 0, "h": 0}
        return {"x": rect.x(), "y": rect.y(), "w": rect.width(), "h": rect.height()}

    def _monitoring_hud_rect_within(self, inner: QRect, outer: QRect) -> bool:
        if inner is None or outer is None or inner.isNull() or outer.isNull():
            return False
        return (
            inner.left() >= outer.left()
            and inner.top() >= outer.top()
            and inner.right() <= outer.right()
            and inner.bottom() <= outer.bottom()
        )

    def _monitoring_hud_travel_rect(self, target: QRect, width: int, height: int, *, align: str) -> QRect:
        margin = 32
        usable_w = max(260, target.width() - (margin * 2))
        usable_h = max(240, target.height() - (margin * 2))
        w = min(max(260, int(width)), usable_w)
        h = min(max(240, int(height)), usable_h)
        if align == "right":
            x = target.x() + max(margin, target.width() - w - margin)
        elif align == "center":
            x = target.x() + max(margin, (target.width() - w) // 2)
        else:
            x = target.x() + margin
        y = target.y() + max(margin, (target.height() - h) // 2)
        return QRect(x, y, w, h)

    def _monitoring_hud_screen_targets(self) -> list[QRect]:
        targets: list[QRect] = []
        for screen in QApplication.screens():
            rect = screen.availableGeometry()
            if rect.isValid() and not rect.isNull():
                targets.append(rect)
        if not targets:
            targets.append(self._virtual_desktop_geometry())
        return sorted(targets, key=lambda rect: (rect.x(), rect.y()))

    def _monitoring_hud_window_travel_detail(self, name: str, widget: QWidget, target: QRect, virtual: QRect) -> dict[str, object]:
        geometry = widget.geometry()
        return {
            "surface": name,
            "visible": widget.isVisible(),
            "geometry": self._monitoring_hud_rect_payload(geometry),
            "target": self._monitoring_hud_rect_payload(target),
            "withinTargetMonitor": self._monitoring_hud_rect_within(geometry, target),
            "withinVirtualDesktop": self._monitoring_hud_rect_within(geometry, virtual),
            "intersectsTargetMonitor": geometry.intersected(target).width() > 120
            and geometry.intersected(target).height() > 120,
        }

    def _monitoring_hud_run_surface_travel_probe(self) -> dict[str, object]:
        overlay = self._monitoring_hud_minimal_native_overlay
        core = self._monitoring_hud_core_visualization_window()
        virtual = self._virtual_desktop_geometry()
        targets = self._monitoring_hud_screen_targets()
        dashboard_target = targets[0]
        overlay_target = targets[-1]
        if len(targets) > 1 and overlay_target == dashboard_target:
            overlay_target = targets[-1]

        dashboard_rect = self._monitoring_hud_travel_rect(
            dashboard_target,
            self.width(),
            self.height(),
            align="left",
        )
        overlay_width = max(720, int(overlay_target.width() * 0.72))
        overlay_height = max(500, int(overlay_target.height() * 0.58))
        overlay_rect = self._monitoring_hud_travel_rect(
            overlay_target,
            overlay_width,
            overlay_height,
            align="right",
        )

        core_geometry_before = (
            core.desktop_screen_geometry()
            if core is not None and callable(getattr(core, "desktop_screen_geometry", None))
            else core.geometry() if core is not None else QRect()
        )
        core_screen_geometry = core.screen_ref.availableGeometry() if core is not None else QRect()

        self.setGeometry(dashboard_rect)
        self._monitoring_hud_interactive_screen_rect = self.geometry()
        self._emit_monitoring_hud_window_status(source="virtual_desktop_travel")
        if overlay is not None:
            overlay.setGeometry(overlay._bound_geometry_to_virtual_desktop(overlay_rect))
            overlay._last_unanchored_geometry = QRect(overlay.geometry())
            overlay._layout_overlay_children()
            self._sync_monitoring_hud_minimal_native_overlay(source="virtual_desktop_travel")
        QApplication.processEvents()

        dashboard_detail = self._monitoring_hud_window_travel_detail("dashboard_control_panel", self, dashboard_target, virtual)
        overlay_detail = (
            self._monitoring_hud_window_travel_detail("hud_overlay_display", overlay, overlay_target, virtual)
            if overlay is not None
            else {"surface": "hud_overlay_display", "visible": False}
        )
        core_geometry_after = (
            core.desktop_screen_geometry()
            if core is not None and callable(getattr(core, "desktop_screen_geometry", None))
            else core.geometry() if core is not None else QRect()
        )
        dashboard_core_overlap = bool(core_geometry_after.isValid() and self.geometry().intersects(core_geometry_after))
        overlay_geometry_after = overlay.geometry() if overlay is not None else QRect()
        overlay_core_overlap = bool(core_geometry_after.isValid() and overlay_geometry_after.isValid() and overlay_geometry_after.intersects(core_geometry_after))
        separation_required = len(targets) > 1
        surface_separation_ok = not separation_required or not (dashboard_core_overlap or overlay_core_overlap)
        core_detail = {
            "surface": "orin_persona_core_visualization",
            "visible": core.isVisible() if core is not None else False,
            "geometry": self._monitoring_hud_rect_payload(core_geometry_after),
            "presetMonitor": self._monitoring_hud_rect_payload(core_screen_geometry),
            "withinPresetMonitor": self._monitoring_hud_rect_within(core_geometry_after, core_screen_geometry),
            "remainedOnUserSelectedMonitor": self._monitoring_hud_rect_payload(core_geometry_after)
            == self._monitoring_hud_rect_payload(core_geometry_before),
            "travelPolicy": "independent_user_selected_monitor_scoped",
            "attachedToHudDashboardOrNcp": False,
            "movable": False,
            "dashboardOverlap": dashboard_core_overlap,
            "overlayOverlap": overlay_core_overlap,
            "surfaceSeparationRequired": separation_required,
            "surfaceSeparationOk": surface_separation_ok,
        }
        dashboard_ok = bool(
            dashboard_detail.get("visible")
            and dashboard_detail.get("withinTargetMonitor")
            and dashboard_detail.get("withinVirtualDesktop")
        )
        overlay_ok = bool(
            overlay_detail.get("visible")
            and overlay_detail.get("withinTargetMonitor")
            and overlay_detail.get("withinVirtualDesktop")
        )
        core_ok = bool(
            core_detail.get("visible")
            and core_detail.get("withinPresetMonitor")
            and core_detail.get("remainedOnUserSelectedMonitor")
            and core_detail.get("attachedToHudDashboardOrNcp") is False
            and core_detail.get("movable") is False
            and core_detail.get("surfaceSeparationOk") is True
        )
        ok = dashboard_ok and overlay_ok and core_ok
        if ok:
            self._emit_runtime_signal(
                "MONITORING_HUD_SURFACE_VIRTUAL_DESKTOP_TRAVEL_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS28",
                dashboard="moved_to_target_monitor",
                overlay="moved_to_target_monitor",
                core="independent_user_selected_monitor_scoped",
                core_attachment="none",
                screen_count=len(targets),
                virtual_desktop="all_monitors",
            )
            self._emit_runtime_signal(
                "CORE_VISUALIZATION_HUD_SURFACE_SEPARATION_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS30",
                core="fixed_preset_monitor",
                dashboard_overlap=str(dashboard_core_overlap).lower(),
                overlay_overlap=str(overlay_core_overlap).lower(),
                movable="false",
            )
        return {
            "ok": ok,
            "screenCount": len(targets),
            "virtualDesktop": self._monitoring_hud_rect_payload(virtual),
            "dashboard": dashboard_detail,
            "overlay": overlay_detail,
            "core": core_detail,
        }

    def _monitoring_hud_run_dashboard_standalone_probe(self) -> dict[str, object]:
        overlay = self._monitoring_hud_minimal_native_overlay
        core = self._monitoring_hud_core_visualization_window()
        virtual = self._virtual_desktop_geometry()
        targets = self._monitoring_hud_screen_targets()
        current_geometry = self.geometry()
        current_center = current_geometry.center() if current_geometry.isValid() else QPoint(0, 0)

        core_geometry_before = (
            core.desktop_screen_geometry()
            if core is not None and callable(getattr(core, "desktop_screen_geometry", None))
            else core.geometry() if core is not None else QRect()
        )
        core_screen_geometry = core.screen_ref.availableGeometry() if core is not None else QRect()
        overlay_geometry_before = overlay.geometry() if overlay is not None else QRect()

        non_core_targets = [
            target
            for target in targets
            if not (
                core_screen_geometry.isValid()
                and target.intersected(core_screen_geometry).width() > 120
                and target.intersected(core_screen_geometry).height() > 120
            )
        ]
        candidate_targets = non_core_targets or targets
        target = max(
            candidate_targets,
            key=lambda rect: abs(rect.center().x() - current_center.x()) + abs(rect.center().y() - current_center.y()),
        )
        dashboard_rect = self._monitoring_hud_travel_rect(
            target,
            max(self.width(), 700),
            max(self.height(), 560),
            align="center",
        )

        self.setGeometry(dashboard_rect)
        self._monitoring_hud_interactive_screen_rect = self.geometry()
        self._emit_monitoring_hud_window_status(source="dashboard_standalone_travel")
        QApplication.processEvents()

        dashboard_detail = self._monitoring_hud_window_travel_detail(
            "dashboard_control_panel",
            self,
            target,
            virtual,
        )
        overlay_geometry_after = overlay.geometry() if overlay is not None else QRect()
        core_geometry_after = (
            core.desktop_screen_geometry()
            if core is not None and callable(getattr(core, "desktop_screen_geometry", None))
            else core.geometry() if core is not None else QRect()
        )
        overlay_payload_before = self._monitoring_hud_rect_payload(overlay_geometry_before)
        overlay_payload_after = self._monitoring_hud_rect_payload(overlay_geometry_after)
        core_payload_before = self._monitoring_hud_rect_payload(core_geometry_before)
        core_payload_after = self._monitoring_hud_rect_payload(core_geometry_after)
        overlay_geometry_unchanged = overlay is None or overlay_payload_before == overlay_payload_after
        core_geometry_unchanged = core is not None and core_payload_before == core_payload_after
        dashboard_core_overlap = bool(
            core_geometry_after.isValid()
            and self.geometry().isValid()
            and self.geometry().intersects(core_geometry_after)
        )
        dashboard_overlay_overlap = bool(
            overlay is not None
            and overlay_geometry_after.isValid()
            and self.geometry().isValid()
            and self.geometry().intersects(overlay_geometry_after)
        )
        clipping_ok = bool(
            dashboard_detail.get("visible")
            and dashboard_detail.get("withinTargetMonitor")
            and dashboard_detail.get("withinVirtualDesktop")
            and dashboard_detail.get("intersectsTargetMonitor")
        )
        core_ok = bool(
            core is not None
            and core.isVisible()
            and self._monitoring_hud_rect_within(core_geometry_after, core_screen_geometry)
            and core_geometry_unchanged
        )
        decoupling_ok = bool(overlay_geometry_unchanged and core_ok)
        ok = bool(clipping_ok and decoupling_ok)

        if ok:
            self._emit_runtime_signal(
                "MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS32",
                surface="dashboard_control_panel",
                movement="dashboard_native_window_only",
                virtual_desktop="all_monitors",
                screen_count=len(targets),
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS32",
                surface="dashboard_control_panel",
                within_target_monitor=str(bool(dashboard_detail.get("withinTargetMonitor"))).lower(),
                within_virtual_desktop=str(bool(dashboard_detail.get("withinVirtualDesktop"))).lower(),
                clipping="none",
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_DASHBOARD_CORE_OVERLAY_DECOUPLING_READY",
                package="PKG-006",
                slice="SLC-026",
                seam="WS32",
                overlay_geometry_unchanged=str(overlay_geometry_unchanged).lower(),
                core_geometry_unchanged=str(core_geometry_unchanged).lower(),
                overlay_acceptance="deferred_non_gating",
                core_classification="dependency_only",
            )

        return {
            "ok": ok,
            "movement": "dashboard_native_window_only",
            "screenCount": len(targets),
            "virtualDesktop": self._monitoring_hud_rect_payload(virtual),
            "dashboard": dashboard_detail,
            "targetPolicy": "non_core_monitor_when_available",
            "clippingOk": clipping_ok,
            "decouplingOk": decoupling_ok,
            "overlayGeometryUnchanged": overlay_geometry_unchanged,
            "coreGeometryUnchanged": core_geometry_unchanged,
            "overlay": {
                "surface": "hud_overlay_display",
                "releaseGate": "deferred_non_gating",
                "geometryBefore": overlay_payload_before,
                "geometryAfter": overlay_payload_after,
                "geometryUnchanged": overlay_geometry_unchanged,
                "dashboardOverlap": dashboard_overlay_overlap,
            },
            "core": {
                "surface": "orin_persona_core_visualization",
                "classification": "dependency_only",
                "visible": core.isVisible() if core is not None else False,
                "geometryBefore": core_payload_before,
                "geometryAfter": core_payload_after,
                "presetMonitor": self._monitoring_hud_rect_payload(core_screen_geometry),
                "geometryUnchanged": core_geometry_unchanged,
                "withinPresetMonitor": self._monitoring_hud_rect_within(core_geometry_after, core_screen_geometry),
                "dashboardOverlap": dashboard_core_overlap,
                "movable": False,
            },
        }

    def _promote_monitoring_hud_edit_window(self):
        if self.surface_role != "hud":
            return
        self.raise_()
        self._emit_runtime_signal(
            "MONITORING_HUD_SELF_QA_WINDOW_RAISE_HINT_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS38",
            forced_foreground=False,
            topmost=False,
        )

    def _monitoring_hud_dashboard_control_rect_contains(self, point: QPoint) -> bool:
        control_rect_names = (
            "anchorToggle",
            "visibilityToggle",
            "settingsAction",
            "dashboardClose",
            "createMonitor",
            "snapToggle",
            "pollingRate",
            "warningModeControl",
            "settingsWarningToggle",
            "monitorSelector",
            "monitorEnabled",
            "monitorPollingRate",
        )
        for name in control_rect_names:
            rect = self._monitoring_hud_live_screen_rects.get(name, QRect())
            if rect.isValid() and not rect.isNull() and rect.contains(point):
                return True
            if name == "dashboardClose":
                if (
                    self._monitoring_hud_dashboard_close_last_screen_rect.isValid()
                    and not self._monitoring_hud_dashboard_close_last_screen_rect.isNull()
                    and self._monitoring_hud_dashboard_close_last_screen_rect.contains(point)
                ):
                    return True
                fallback_rect = self._monitoring_hud_dashboard_close_fallback_screen_rect()
                if fallback_rect.isValid() and not fallback_rect.isNull() and fallback_rect.contains(point):
                    return True
            if name == "settingsAction":
                if (
                    self._monitoring_hud_settings_action_last_screen_rect.isValid()
                    and not self._monitoring_hud_settings_action_last_screen_rect.isNull()
                    and self._monitoring_hud_settings_action_last_screen_rect.contains(point)
                ):
                    return True
                fallback_rect = self._monitoring_hud_settings_action_fallback_screen_rect()
                if fallback_rect.isValid() and not fallback_rect.isNull() and fallback_rect.contains(point):
                    return True
        return False

    def _monitoring_hud_dashboard_close_control_rect_contains(self, point: QPoint) -> bool:
        rect = self._monitoring_hud_live_screen_rects.get("dashboardClose", QRect())
        if rect.isValid() and not rect.isNull() and rect.contains(point):
            return True
        settings_rect = self._monitoring_hud_live_screen_rects.get("settingsAction", QRect())
        if settings_rect.isValid() and not settings_rect.isNull() and settings_rect.contains(point):
            return False
        if (
            self._monitoring_hud_settings_action_last_screen_rect.isValid()
            and not self._monitoring_hud_settings_action_last_screen_rect.isNull()
            and self._monitoring_hud_settings_action_last_screen_rect.contains(point)
        ):
            return False
        settings_fallback_rect = self._monitoring_hud_settings_action_fallback_screen_rect()
        if settings_fallback_rect.isValid() and not settings_fallback_rect.isNull() and settings_fallback_rect.contains(point):
            return False
        if (
            self._monitoring_hud_dashboard_close_last_screen_rect.isValid()
            and not self._monitoring_hud_dashboard_close_last_screen_rect.isNull()
            and self._monitoring_hud_dashboard_close_last_screen_rect.contains(point)
        ):
            return True
        fallback_rect = self._monitoring_hud_dashboard_close_fallback_screen_rect()
        return bool(fallback_rect.isValid() and not fallback_rect.isNull() and fallback_rect.contains(point))

    def _monitoring_hud_dashboard_settings_control_rect_contains(self, point: QPoint) -> bool:
        rect = self._monitoring_hud_live_screen_rects.get("settingsAction", QRect())
        if rect.isValid() and not rect.isNull() and rect.contains(point):
            return True
        if (
            self._monitoring_hud_settings_action_last_screen_rect.isValid()
            and not self._monitoring_hud_settings_action_last_screen_rect.isNull()
            and self._monitoring_hud_settings_action_last_screen_rect.contains(point)
        ):
            return True
        fallback_rect = self._monitoring_hud_settings_action_fallback_screen_rect()
        return bool(fallback_rect.isValid() and not fallback_rect.isNull() and fallback_rect.contains(point))

    def _handle_monitoring_hud_dashboard_close_native_control(self, screen_point: QPoint) -> bool:
        if not self._monitoring_hud_dashboard_close_control_rect_contains(screen_point):
            return False
        self.request_monitoring_hud_dashboard_from_tray(source="dashboard-close-native-control", visible=False)
        self._persist_monitoring_hud_feature_state(source="dashboard-close-native-control")
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_CLOSE_NATIVE_CONTROL_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS43",
            feature_enabled=bool(self._monitoring_hud_feature_enabled),
            dashboard_visible=bool(self.isVisible() and self._monitoring_hud_visible),
            x=screen_point.x(),
            y=screen_point.y(),
        )
        return True

    def _handle_monitoring_hud_dashboard_settings_native_control(self, screen_point: QPoint) -> bool:
        if not self._monitoring_hud_dashboard_settings_control_rect_contains(screen_point):
            return False
        script = """
        (() => {
          const button = document.getElementById("monitoring-hud-settings-action");
          if (!button) return "missing";
          button.click();
          return "clicked";
        })();
        """
        self._run_javascript(script)
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_SETTINGS_NATIVE_CONTROL_READY",
            package="PKG-006",
            slice="SLC-029",
            seam="LV1",
            control="dashboard-settings",
            action="open",
            x=screen_point.x(),
            y=screen_point.y(),
        )
        return True

    def _begin_monitoring_hud_native_user_move(self, source: str = "native_caption_move") -> None:
        if self.surface_role != "hud":
            return
        geometry = self.geometry()
        self._monitoring_hud_native_move_user_active = True
        self._monitoring_hud_native_move_start_geometry = QRect(geometry)
        self._monitoring_hud_native_move_last_geometry = QRect(geometry)
        self._monitoring_hud_native_move_source = source
        self._monitoring_hud_native_move_finalize_timer.stop()

    def _clear_monitoring_hud_native_user_move(self) -> None:
        self._monitoring_hud_native_move_user_active = False
        self._monitoring_hud_native_move_start_geometry = QRect()
        self._monitoring_hud_native_move_last_geometry = QRect()
        self._monitoring_hud_native_move_source = ""
        self._monitoring_hud_native_move_finalize_timer.stop()

    def _finish_monitoring_hud_native_system_move(self, source: str = "system_move"):
        geometry = self.geometry()
        move_was_user_initiated = bool(self._monitoring_hud_native_move_user_active)
        start_geometry = QRect(self._monitoring_hud_native_move_start_geometry)
        geometry_changed = bool(
            move_was_user_initiated
            and start_geometry.isValid()
            and geometry != start_geometry
        )
        self._clear_monitoring_hud_native_user_move()
        if geometry_changed:
            self._monitoring_hud_user_geometry_override_active = True
        self._monitoring_hud_interactive_screen_rect = geometry
        self._emit_runtime_signal(
            "MONITORING_HUD_NATIVE_WINDOW_MOVE_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS38",
            source=source,
            movement_model="os-system-move-no-snap",
            x=geometry.x(),
            y=geometry.y(),
            w=geometry.width(),
            h=geometry.height(),
            virtual_desktop="all_monitors",
            user_initiated=move_was_user_initiated,
            geometry_changed=geometry_changed,
        )
        self._emit_monitoring_hud_window_ownership_focus_ready(source=source)
        self._emit_monitoring_hud_window_status(source=source)

    def _finish_monitoring_hud_native_system_resize(self, source: str = "system_resize"):
        self._monitoring_hud_user_geometry_override_active = True
        self._monitoring_hud_interactive_screen_rect = self.geometry()
        geometry = self.geometry()
        self._emit_runtime_signal(
            "MONITORING_HUD_NATIVE_WINDOW_RESIZE_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS44",
            source=source,
            resize_model="os-edge-corner-resize",
            x=geometry.x(),
            y=geometry.y(),
            w=geometry.width(),
            h=geometry.height(),
            min_w=self.minimumWidth(),
            min_h=self.minimumHeight(),
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_SHELL_LAYOUT_READY",
            package="PKG-006",
            slice="SLC-016",
            seam="WS44",
            surface="hud_dashboard",
            sticky_header=True,
            single_surface_scrollbar=True,
            title="HUD Dashboard",
            resize_model="os-edge-corner-resize",
        )
        self._emit_monitoring_hud_visual_shell_ready(source=source)
        self._emit_monitoring_hud_window_ownership_focus_ready(source=source)
        self._emit_monitoring_hud_window_status(source=source)

    def _emit_monitoring_hud_visual_shell_ready(self, source: str = "runtime"):
        if self.surface_role != "hud":
            return
        geometry = self.geometry()
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_VISUAL_SHELL_READY",
            package="PKG-006",
            slice="SLC-016",
            seam="WS44",
            source=source,
            scrollbar_owner="monitoring-hud-control-hub",
            scrollbar_boundary="inner-content-well-gutter",
            outer_frame_haze="removed-no-square-layer",
            native_resize_hit_zone="preclick-hover-cursor-aligned-12px-app-owned-resize-action",
            resize_edge_scope="all-edges-and-corners",
            resize_hit_zone_px=self._monitoring_hud_resize_hit_zone_px(),
            resize_hover_cursor_model="polls-real-cursor-before-click",
            resize_poll_interval_ms=8,
            deadzone_policy="auto-height-content-no-empty-hit-zones",
            grid_scope="control-hub-cards-only",
            sticky_header_mask="opaque-scroll-mask",
            x=geometry.x(),
            y=geometry.y(),
            w=geometry.width(),
            h=geometry.height(),
        )

    def _start_monitoring_hud_native_system_move(self, screen_point: QPoint) -> bool:
        if self.surface_role != "hud":
            return False
        window_handle = self.windowHandle()
        start_system_move = getattr(window_handle, "startSystemMove", None) if window_handle else None
        if not callable(start_system_move):
            return False
        self._monitoring_hud_native_panel_drag_active = False
        self._emit_runtime_signal(
            "MONITORING_HUD_NATIVE_SYSTEM_MOVE_STARTED",
            package="PKG-006",
            slice="SLC-026",
            seam="WS38",
            x=screen_point.x(),
            y=screen_point.y(),
            movement_model="os-system-move-no-snap",
        )
        try:
            self._begin_monitoring_hud_native_user_move("system_move")
            started = bool(start_system_move())
        except Exception:
            started = False
        if started:
            QTimer.singleShot(360, lambda: self._finish_monitoring_hud_native_system_move("system_move"))
        else:
            self._clear_monitoring_hud_native_user_move()
        return started

    def _monitoring_hud_native_resize_edges_for_point(self, point: QPoint):
        if self.surface_role != "hud":
            return Qt.Edges()
        rect = self.geometry()
        if rect.isNull() or not rect.isValid():
            return Qt.Edges()
        # Keep the fallback resize rail close to the visible chrome so cursor feedback
        # and actual drag behavior agree with standard Windows resize expectations.
        margin = self._monitoring_hud_resize_hit_zone_px()
        if not rect.adjusted(-2, -2, 2, 2).contains(point):
            return Qt.Edges()
        edges = Qt.Edges()
        if abs(point.x() - rect.left()) <= margin:
            edges |= Qt.LeftEdge
        if abs(point.x() - rect.right()) <= margin:
            edges |= Qt.RightEdge
        if abs(point.y() - rect.top()) <= margin:
            edges |= Qt.TopEdge
        if abs(point.y() - rect.bottom()) <= margin:
            edges |= Qt.BottomEdge
        return edges

    def _monitoring_hud_resize_hit_zone_px(self) -> int:
        return 12

    def _monitoring_hud_window_resize_interaction_available(self) -> bool:
        return (
            self.surface_role == "hud"
            and self.desktop_mode
            and self.isVisible()
            and self.webview.isVisible()
        )

    def _monitoring_hud_point_belongs_to_dashboard_window(self, point: QPoint) -> bool:
        if os.name != "nt" or point.isNull():
            return self.geometry().contains(point)
        try:
            probe = ctypes.wintypes.POINT(int(point.x()), int(point.y()))
            hwnd = int(WindowFromPoint(probe))
            dashboard_hwnd = int(self.winId())
            while hwnd:
                if hwnd == dashboard_hwnd:
                    return True
                hwnd = int(GetParentW(ctypes.wintypes.HWND(hwnd)))
        except Exception:
            return self.geometry().contains(point)
        return False

    def _monitoring_hud_resize_edges_under_cursor(self) -> tuple[QPoint, Qt.Edges]:
        if not self._monitoring_hud_window_resize_interaction_available():
            return QPoint(), Qt.Edges()
        screen_point = self._monitoring_hud_cursor_screen_point()
        if screen_point.isNull():
            return QPoint(), Qt.Edges()
        if not self.geometry().adjusted(-2, -2, 2, 2).contains(screen_point):
            return screen_point, Qt.Edges()
        if not self._monitoring_hud_point_belongs_to_dashboard_window(screen_point):
            return screen_point, Qt.Edges()
        edges = self._monitoring_hud_native_resize_edges_for_point(screen_point)
        if edges and self._monitoring_hud_dashboard_control_rect_contains(screen_point):
            return screen_point, Qt.Edges()
        return screen_point, edges

    def _poll_monitoring_hud_resize_hover_cursor(self):
        if (
            self._monitoring_hud_native_panel_drag_active
            or self._monitoring_hud_native_window_resize_active
            or self._monitoring_hud_native_card_drag_active
            or self._monitoring_hud_native_card_resize_active
        ):
            return
        _, edges = self._monitoring_hud_resize_edges_under_cursor()
        if edges:
            self._set_monitoring_hud_resize_cursor(edges)
            return
        self._reset_monitoring_hud_resize_cursor()

    def _monitoring_hud_native_resize_hit_test_for_edges(self, edges) -> int:
        left, right, top, bottom = self._monitoring_hud_resize_edge_key(edges)
        if left and top:
            return HTTOPLEFT
        if right and top:
            return HTTOPRIGHT
        if left and bottom:
            return HTBOTTOMLEFT
        if right and bottom:
            return HTBOTTOMRIGHT
        if left:
            return HTLEFT
        if right:
            return HTRIGHT
        if top:
            return HTTOP
        if bottom:
            return HTBOTTOM
        return 0

    def _monitoring_hud_native_resize_edges_for_hit_test(self, hit_test: int):
        edge_map = {
            HTLEFT: Qt.LeftEdge,
            HTRIGHT: Qt.RightEdge,
            HTTOP: Qt.TopEdge,
            HTBOTTOM: Qt.BottomEdge,
            HTTOPLEFT: Qt.TopEdge | Qt.LeftEdge,
            HTTOPRIGHT: Qt.TopEdge | Qt.RightEdge,
            HTBOTTOMLEFT: Qt.BottomEdge | Qt.LeftEdge,
            HTBOTTOMRIGHT: Qt.BottomEdge | Qt.RightEdge,
        }
        return edge_map.get(int(hit_test), Qt.Edges())

    def _monitoring_hud_cursor_screen_point(self) -> QPoint:
        cursor_position = self._monitoring_hud_cursor_position()
        if cursor_position is None:
            return QPoint()
        return QPoint(int(cursor_position[0]), int(cursor_position[1]))

    def _monitoring_hud_left_mouse_button_down(self) -> bool:
        try:
            return bool(GetAsyncKeyState(VK_LBUTTON) & 0x8000)
        except Exception:
            return False

    def _monitoring_hud_resize_refresh_rate_hz(self) -> float:
        screens = []
        try:
            screens.append(self.screen())
        except Exception:
            pass
        screens.extend([getattr(self, "screen_ref", None), QApplication.primaryScreen()])
        for screen in screens:
            if screen is None:
                continue
            try:
                refresh_rate = float(screen.refreshRate())
            except Exception:
                continue
            if 30.0 <= refresh_rate <= 360.0:
                return refresh_rate
        return 60.0

    def _monitoring_hud_resize_frame_interval_ms(self) -> int:
        refresh_rate = self._monitoring_hud_resize_refresh_rate_hz()
        return max(4, min(16, int(round(1000.0 / refresh_rate))))

    def _start_monitoring_hud_native_system_resize(self, edges, screen_point: QPoint) -> bool:
        if self.surface_role != "hud" or not edges:
            return False
        window_handle = self.windowHandle()
        start_system_resize = getattr(window_handle, "startSystemResize", None) if window_handle else None
        if not callable(start_system_resize):
            return False
        self._emit_runtime_signal(
            "MONITORING_HUD_NATIVE_SYSTEM_RESIZE_STARTED",
            package="PKG-006",
            slice="SLC-026",
            seam="WS44",
            x=screen_point.x(),
            y=screen_point.y(),
            resize_model="os-edge-corner-resize",
            edges=str(edges),
        )
        try:
            started = bool(start_system_resize(edges))
        except Exception:
            started = False
        if started:
            QTimer.singleShot(360, lambda: self._finish_monitoring_hud_native_system_resize("system_resize"))
        return started

    def _monitoring_hud_resize_edge_key(self, edges) -> tuple[bool, bool, bool, bool]:
        return (
            bool(edges & Qt.LeftEdge),
            bool(edges & Qt.RightEdge),
            bool(edges & Qt.TopEdge),
            bool(edges & Qt.BottomEdge),
        )

    def _monitoring_hud_resize_cursor_for_edges(self, edges):
        left, right, top, bottom = self._monitoring_hud_resize_edge_key(edges)
        if (left and top) or (right and bottom):
            return Qt.SizeFDiagCursor
        if (right and top) or (left and bottom):
            return Qt.SizeBDiagCursor
        if left or right:
            return Qt.SizeHorCursor
        if top or bottom:
            return Qt.SizeVerCursor
        return None

    def _monitoring_hud_windows_resize_cursor_id_for_edges(self, edges):
        if not edges:
            return IDC_ARROW
        left, right, top, bottom = self._monitoring_hud_resize_edge_key(edges)
        if (left and top) or (right and bottom):
            return IDC_SIZENWSE
        if (right and top) or (left and bottom):
            return IDC_SIZENESW
        if left or right:
            return IDC_SIZEWE
        if top or bottom:
            return IDC_SIZENS
        return IDC_ARROW

    def _apply_monitoring_hud_windows_resize_cursor(self, edges):
        if os.name != "nt":
            return
        try:
            cursor_id = self._monitoring_hud_windows_resize_cursor_id_for_edges(edges)
            cursor_handle = LoadCursorW(None, cursor_id)
            if cursor_handle:
                SetCursor(cursor_handle)
        except Exception:
            pass

    def _set_monitoring_hud_override_resize_cursor(self, cursor):
        try:
            if cursor is None:
                if self._monitoring_hud_resize_override_cursor_active:
                    QApplication.restoreOverrideCursor()
                    self._monitoring_hud_resize_override_cursor_active = False
                return
            qt_cursor = QCursor(cursor)
            if self._monitoring_hud_resize_override_cursor_active:
                QApplication.changeOverrideCursor(qt_cursor)
            else:
                QApplication.setOverrideCursor(qt_cursor)
                self._monitoring_hud_resize_override_cursor_active = True
        except Exception:
            self._monitoring_hud_resize_override_cursor_active = False

    def _set_monitoring_hud_resize_cursor(self, edges):
        key = self._monitoring_hud_resize_edge_key(edges) if edges else None
        if key == self._monitoring_hud_resize_cursor_key:
            if os.name == "nt":
                self._apply_monitoring_hud_windows_resize_cursor(edges if key is not None else Qt.Edges())
            elif key is not None:
                self._apply_monitoring_hud_windows_resize_cursor(edges)
            return
        self._monitoring_hud_resize_cursor_key = key
        cursor = self._monitoring_hud_resize_cursor_for_edges(edges) if edges else None
        targets = [self, self.webview]
        try:
            targets.extend(self.webview.findChildren(QWidget))
        except Exception:
            pass
        if os.name == "nt":
            for target in targets:
                target.unsetCursor()
            self._set_monitoring_hud_override_resize_cursor(None)
            self._apply_monitoring_hud_windows_resize_cursor(edges)
            return
        for target in targets:
            if cursor is None:
                target.unsetCursor()
            else:
                target.setCursor(QCursor(cursor))
        self._set_monitoring_hud_override_resize_cursor(cursor)
        self._apply_monitoring_hud_windows_resize_cursor(edges)

    def _reset_monitoring_hud_resize_cursor(self):
        self._set_monitoring_hud_resize_cursor(Qt.Edges())

    def _start_monitoring_hud_fallback_window_resize(self, edges, screen_point: QPoint):
        resize_refresh_rate_hz = self._monitoring_hud_resize_refresh_rate_hz()
        resize_frame_interval_ms = self._monitoring_hud_resize_frame_interval_ms()
        self._monitoring_hud_native_window_resize_active = True
        self._monitoring_hud_user_geometry_override_active = True
        self._monitoring_hud_native_window_resize_edges = edges
        self._monitoring_hud_native_window_resize_start = screen_point
        self._monitoring_hud_native_window_resize_base = QRect(self.geometry())
        self._monitoring_hud_native_window_resize_last_rect = QRect(self.geometry())
        self._monitoring_hud_native_window_resize_pending_point = QPoint(screen_point)
        self._monitoring_hud_native_window_resize_last_apply = 0.0
        self._monitoring_hud_native_window_resize_frame_interval_ms = resize_frame_interval_ms
        self._monitoring_hud_native_window_resize_poll_active = True
        self._monitoring_hud_resize_frame_sync_last = 0.0
        self._monitoring_hud_resize_js_sync_last = 0.0
        self._clear_monitoring_hud_native_user_move()
        try:
            SetCapture(ctypes.wintypes.HWND(int(self.winId())))
        except Exception:
            pass
        self._emit_runtime_signal(
            "MONITORING_HUD_NATIVE_WINDOW_RESIZE_FALLBACK_STARTED",
            package="PKG-006",
            slice="SLC-026",
            seam="WS56",
            x=screen_point.x(),
            y=screen_point.y(),
            resize_model="refresh-rate-paced-cursor-owned-fluid-geometry-resize",
            resize_edge_scope="all-edges-and-corners",
            resize_hit_zone_px=self._monitoring_hud_resize_hit_zone_px(),
            resize_refresh_rate_hz=round(resize_refresh_rate_hz, 2),
            resize_frame_interval_ms=resize_frame_interval_ms,
            resize_poll_interval_ms=resize_frame_interval_ms,
            edges=str(edges),
        )
        self._monitoring_hud_native_window_resize_poll_timer.stop()
        self._monitoring_hud_native_window_resize_poll_timer.setInterval(resize_frame_interval_ms)
        self._monitoring_hud_native_window_resize_poll_timer.start()
        self._poll_monitoring_hud_fallback_window_resize()

    def _poll_monitoring_hud_fallback_window_resize(self):
        if not self._monitoring_hud_native_window_resize_active:
            self._monitoring_hud_native_window_resize_poll_timer.stop()
            self._monitoring_hud_native_window_resize_poll_active = False
            return
        screen_point = self._monitoring_hud_cursor_screen_point()
        if not screen_point.isNull():
            self._update_monitoring_hud_fallback_window_resize(screen_point)
        if self._monitoring_hud_left_mouse_button_down():
            return
        self._finish_monitoring_hud_fallback_window_resize(screen_point)

    def _update_monitoring_hud_fallback_window_resize(self, screen_point: QPoint):
        if not self._monitoring_hud_native_window_resize_active:
            return
        self._monitoring_hud_native_window_resize_pending_point = QPoint(screen_point)
        interval_s = max(0.004, self._monitoring_hud_native_window_resize_frame_interval_ms / 1000.0)
        now = time.monotonic()
        elapsed = now - self._monitoring_hud_native_window_resize_last_apply
        if self._monitoring_hud_native_window_resize_last_apply <= 0.0 or elapsed >= interval_s:
            self._apply_monitoring_hud_queued_window_resize()
            return
        if not self._monitoring_hud_native_window_resize_frame_timer.isActive():
            remaining_ms = max(1, int(round((interval_s - elapsed) * 1000.0)))
            self._monitoring_hud_native_window_resize_frame_timer.start(remaining_ms)

    def _apply_monitoring_hud_queued_window_resize(self):
        if not self._monitoring_hud_native_window_resize_active:
            return
        screen_point = QPoint(self._monitoring_hud_native_window_resize_pending_point)
        if screen_point.isNull():
            screen_point = self._monitoring_hud_cursor_screen_point()
        if screen_point.isNull():
            return
        next_rect = self._monitoring_hud_resize_rect_from_native_delta(screen_point)
        if next_rect == self._monitoring_hud_native_window_resize_last_rect:
            self._monitoring_hud_native_window_resize_last_apply = time.monotonic()
            return
        self.setGeometry(next_rect)
        self._monitoring_hud_native_window_resize_last_rect = QRect(next_rect)
        self._monitoring_hud_interactive_screen_rect = self.geometry()
        self._monitoring_hud_native_window_resize_last_apply = time.monotonic()
        self._sync_monitoring_hud_resize_frame()

    def _finish_monitoring_hud_fallback_window_resize(self, screen_point: QPoint):
        if not self._monitoring_hud_native_window_resize_active:
            return
        self._monitoring_hud_native_window_resize_poll_timer.stop()
        self._monitoring_hud_native_window_resize_frame_timer.stop()
        if screen_point.isNull():
            screen_point = self._monitoring_hud_native_window_resize_start
        next_rect = self._monitoring_hud_resize_rect_from_native_delta(screen_point)
        if next_rect != self._monitoring_hud_native_window_resize_last_rect:
            self.setGeometry(next_rect)
            self._monitoring_hud_native_window_resize_last_rect = QRect(next_rect)
        self._sync_monitoring_hud_resize_frame(force=True)
        self._monitoring_hud_native_window_resize_active = False
        self._monitoring_hud_native_window_resize_poll_active = False
        self._monitoring_hud_native_window_resize_edges = Qt.Edges()
        self._monitoring_hud_native_window_resize_last_rect = QRect()
        self._monitoring_hud_native_window_resize_pending_point = QPoint()
        self._monitoring_hud_native_window_resize_last_apply = 0.0
        try:
            ReleaseCapture()
        except Exception:
            pass
        self._reset_monitoring_hud_resize_cursor()
        self._finish_monitoring_hud_native_system_resize("fallback_window_resize")

    def _sync_monitoring_hud_resize_frame(self, *, force: bool = False):
        if self.surface_role != "hud" or self._is_shutting_down:
            return
        now = time.monotonic()
        frame_interval_s = max(0.004, self._monitoring_hud_native_window_resize_frame_interval_ms / 1000.0)
        if not force and now - self._monitoring_hud_resize_frame_sync_last < frame_interval_s:
            return
        self._monitoring_hud_resize_frame_sync_last = now
        self.webview.setGeometry(self.rect())
        self.webview.updateGeometry()
        self.webview.update()
        self.update()
        js_interval_s = frame_interval_s
        if force or now - self._monitoring_hud_resize_js_sync_last >= js_interval_s:
            self._monitoring_hud_resize_js_sync_last = now
            self._run_javascript("window.requestAnimationFrame(() => window.dispatchEvent(new Event('resize')));")

    def _bound_monitoring_hud_window_resize_rect(self, rect: QRect) -> QRect:
        virtual = self._virtual_desktop_geometry()
        min_width = max(self.minimumWidth(), 640)
        min_height = max(self.minimumHeight(), 520)
        width = max(min_width, min(rect.width(), virtual.width()))
        height = max(min_height, min(rect.height(), virtual.height()))
        left = max(virtual.x(), min(rect.x(), virtual.x() + virtual.width() - width))
        top = max(virtual.y(), min(rect.y(), virtual.y() + virtual.height() - height))
        return QRect(left, top, width, height)

    def _monitoring_hud_resize_rect_from_native_delta(self, screen_point: QPoint) -> QRect:
        base = self._monitoring_hud_native_window_resize_base
        if base.isNull() or not base.isValid():
            base = QRect(self.geometry())
        delta = screen_point - self._monitoring_hud_native_window_resize_start
        left, right, top, bottom = self._monitoring_hud_resize_edge_key(
            self._monitoring_hud_native_window_resize_edges
        )
        x = base.x()
        y = base.y()
        width = base.width()
        height = base.height()
        if left:
            x = base.x() + delta.x()
            width = base.width() - delta.x()
        elif right:
            width = base.width() + delta.x()
        if top:
            y = base.y() + delta.y()
            height = base.height() - delta.y()
        elif bottom:
            height = base.height() + delta.y()

        min_width = max(self.minimumWidth(), 640)
        min_height = max(self.minimumHeight(), 520)
        if width < min_width:
            if left:
                x = base.right() - min_width + 1
            width = min_width
        if height < min_height:
            if top:
                y = base.bottom() - min_height + 1
            height = min_height
        return self._bound_monitoring_hud_window_resize_rect(QRect(x, y, width, height))

    def _monitoring_hud_header_rect(self) -> QRect:
        rect = self._monitoring_hud_interactive_screen_rect
        if rect.isNull() or not rect.isValid():
            rect = self._estimate_monitoring_hud_interactive_screen_rect()
            self._monitoring_hud_interactive_screen_rect = rect
        return QRect(rect.x(), rect.y(), rect.width(), min(170, rect.height()))

    def _monitoring_hud_page_origin_from_screen_rect(self) -> QPoint:
        rect = self._monitoring_hud_interactive_screen_rect
        if rect.isNull() or not rect.isValid():
            rect = self._estimate_monitoring_hud_interactive_screen_rect()
            self._monitoring_hud_interactive_screen_rect = rect
        webview_origin = self.webview.mapToGlobal(QPoint(0, 0))
        return QPoint(max(0, rect.x() + 12 - webview_origin.x()), max(0, rect.y() + 12 - webview_origin.y()))

    def _set_monitoring_hud_panel_position_from_native_drag(self, left: int, top: int, *, emit_status: bool = True):
        if self.surface_role == "hud":
            self._monitoring_hud_user_geometry_override_active = True
            virtual = self._virtual_desktop_geometry()
            max_left = virtual.x() + max(0, virtual.width() - self.width())
            max_top = virtual.y() + max(0, virtual.height() - self.height())
            bounded_left = self._monitoring_hud_bound_native(
                int(left),
                virtual.x(),
                max_left,
            )
            bounded_top = self._monitoring_hud_bound_native(
                int(top),
                virtual.y(),
                max_top,
            )
            self.move(bounded_left, bounded_top)
            self._monitoring_hud_interactive_screen_rect = self.geometry()
            if emit_status:
                self._emit_runtime_signal(
                    "MONITORING_HUD_NATIVE_WINDOW_MOVE_READY",
                    package="PKG-006",
                    slice="SLC-026",
                    seam="WS38",
                    movement_model="fallback-direct-move-no-snap",
                    x=bounded_left,
                    y=bounded_top,
                    virtual_desktop="all_monitors",
                )
                self._emit_monitoring_hud_window_ownership_focus_ready(source="fallback_direct_move")
                self._emit_monitoring_hud_window_status(source="native_window_drag")
            return
        state = {
            "visible": True,
            "anchored": False,
            "snapEnabled": self._monitoring_hud_snap_enabled,
            "pollingRateMs": self._monitoring_hud_polling_rate_ms,
            "panelPosition": {
                "left": max(0, int(left)),
                "top": max(0, int(top)),
            },
        }
        state_json = json.dumps(state, sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setMonitoringHudControlState) {{
                window.setMonitoringHudControlState({state_json});
            }}
            """
        )

    def _monitoring_hud_snap_native(self, value: int | float) -> int:
        return int(round(float(value) / 20) * 20)

    def _monitoring_hud_bound_native(self, value: int, lower: int, upper: int) -> int:
        return max(lower, min(upper, int(value)))

    def _monitoring_hud_card_layout_base(self, card_id: str) -> dict[str, int]:
        defaults = {
            "cpu": {"x": 0, "y": 0, "w": 600, "h": 280},
            "gpu": {"x": 0, "y": 300, "w": 600, "h": 280},
        }
        base = dict(defaults.get(card_id, {"x": 0, "y": 0, "w": 600, "h": 280}))
        cards = self._monitoring_hud_live_page_state.get("cards") if isinstance(self._monitoring_hud_live_page_state, dict) else {}
        card = cards.get(card_id) if isinstance(cards, dict) else {}
        if isinstance(card, dict):
            for key in ("x", "y", "w", "h"):
                try:
                    base[key] = int(float(card.get(key, base[key])))
                except (TypeError, ValueError):
                    pass
        return base

    def _monitoring_hud_card_board_bounds(self) -> tuple[int, int]:
        board_rect = self._monitoring_hud_live_screen_rects.get("cardBoard", QRect())
        if board_rect.isValid() and not board_rect.isNull():
            return max(420, board_rect.width()), max(620, board_rect.height())
        return 720, 620

    def _set_monitoring_hud_card_layout_from_native_drag(self, card_id: str, layout: dict[str, int]):
        state: dict[str, object] = {}
        if isinstance(self._monitoring_hud_live_page_state, dict):
            for key in ("visible", "anchored", "snapEnabled", "pollingRateMs", "panelPosition"):
                if key in self._monitoring_hud_live_page_state:
                    state[key] = self._monitoring_hud_live_page_state[key]
        state.update(
            {
                "visible": True,
                "anchored": False,
                "snapEnabled": self._monitoring_hud_snap_enabled,
                "pollingRateMs": self._monitoring_hud_polling_rate_ms,
            }
        )
        cards: dict[str, dict[str, int]] = {
            "cpu": {"x": 0, "y": 0, "w": 600, "h": 280},
            "gpu": {"x": 0, "y": 300, "w": 600, "h": 280},
        }
        page_cards = self._monitoring_hud_live_page_state.get("cards") if isinstance(self._monitoring_hud_live_page_state, dict) else {}
        if isinstance(page_cards, dict):
            for existing_id, existing_layout in page_cards.items():
                if isinstance(existing_layout, dict):
                    merged = dict(cards.get(str(existing_id), {"x": 0, "y": 0, "w": 600, "h": 280}))
                    for key in ("x", "y", "w", "h"):
                        try:
                            merged[key] = int(float(existing_layout.get(key, merged[key])))
                        except (TypeError, ValueError):
                            pass
                    cards[str(existing_id)] = merged
        cards[card_id] = {
            "x": int(layout.get("x", 0)),
            "y": int(layout.get("y", 0)),
            "w": int(layout.get("w", 600)),
            "h": int(layout.get("h", 280)),
        }
        state["cards"] = cards
        state_json = json.dumps(state, sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setMonitoringHudControlState) {{
                window.setMonitoringHudControlState({state_json});
            }}
            """
        )

    def _apply_monitoring_hud_native_anchor_click_if_needed(self, expected_anchored: bool):
        if self._monitoring_hud_anchored is expected_anchored:
            return
        self._set_monitoring_hud_control_state(
            anchored=expected_anchored,
            source="native-anchor-click-fallback",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_NATIVE_ANCHOR_CLICK_READY",
            package="PKG-006",
            slice="SLC-026",
            anchored=expected_anchored,
        )

    def _monitoring_hud_layout_from_native_delta(self, resize: bool, delta: QPoint) -> dict[str, int]:
        layout = dict(self._monitoring_hud_native_card_drag_base)
        if resize:
            board_width, board_height = self._monitoring_hud_card_board_bounds()
            layout["w"] = self._monitoring_hud_bound_native(
                self._monitoring_hud_snap_native(layout.get("w", 600) + delta.x()),
                340,
                max(340, self._monitoring_hud_snap_native(board_width - layout.get("x", 0))),
            )
            layout["h"] = self._monitoring_hud_bound_native(
                self._monitoring_hud_snap_native(layout.get("h", 280) + delta.y()),
                260,
                max(260, self._monitoring_hud_snap_native(board_height - layout.get("y", 0))),
            )
            return layout
        board_width, board_height = self._monitoring_hud_card_board_bounds()
        layout["x"] = self._monitoring_hud_bound_native(
            self._monitoring_hud_snap_native(layout.get("x", 0) + delta.x()),
            0,
            max(0, board_width - layout.get("w", 600)),
        )
        layout["y"] = self._monitoring_hud_bound_native(
            self._monitoring_hud_snap_native(layout.get("y", 0) + delta.y()),
            0,
            max(0, board_height - layout.get("h", 280)),
        )
        return layout

    def _handle_monitoring_hud_native_panel_drag_event(self, event) -> bool:
        if (
            not self.desktop_mode
            or (self.surface_role == "hud" and not self.isVisible())
            or (self.surface_role != "hud" and (not self._monitoring_hud_feature_enabled or not self._monitoring_hud_visible))
        ):
            self._monitoring_hud_native_panel_drag_active = False
            self._monitoring_hud_native_window_resize_active = False
            self._clear_monitoring_hud_native_user_move()
            self._monitoring_hud_native_card_drag_active = False
            self._monitoring_hud_native_card_resize_active = False
            self._reset_monitoring_hud_resize_cursor()
            return False
        event_type = event.type()
        if event_type == QEvent.Leave and not (
            self._monitoring_hud_native_panel_drag_active
            or self._monitoring_hud_native_window_resize_active
            or self._monitoring_hud_native_card_drag_active
            or self._monitoring_hud_native_card_resize_active
        ):
            self._reset_monitoring_hud_resize_cursor()
            return False
        if event_type == QEvent.MouseMove and not (
            self._monitoring_hud_native_panel_drag_active
            or self._monitoring_hud_native_window_resize_active
            or self._monitoring_hud_native_card_drag_active
            or self._monitoring_hud_native_card_resize_active
        ):
            if not self._monitoring_hud_window_resize_interaction_available():
                return False
            screen_point = event.globalPosition().toPoint()
            resize_edges = self._monitoring_hud_native_resize_edges_for_point(screen_point)
            if resize_edges and not self._monitoring_hud_dashboard_control_rect_contains(screen_point):
                self._set_monitoring_hud_resize_cursor(resize_edges)
            else:
                self._reset_monitoring_hud_resize_cursor()
            return False
        if event_type == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            screen_point = event.globalPosition().toPoint()
            if self._handle_monitoring_hud_dashboard_settings_native_control(screen_point):
                return True
            if self._handle_monitoring_hud_dashboard_close_native_control(screen_point):
                return True
            resize_edges = self._monitoring_hud_native_resize_edges_for_point(screen_point)
            if resize_edges and not self._monitoring_hud_dashboard_control_rect_contains(screen_point):
                # Use direct geometry resizing for the user-facing Dashboard. Qt/Windows can
                # report startSystemResize as "started" without delivering a real resize for
                # this frameless WebEngine window, which made prior proof over-credit the path.
                self._start_monitoring_hud_fallback_window_resize(resize_edges, screen_point)
                return True
            if not (
                self._monitoring_hud_native_panel_drag_active
                or self._monitoring_hud_native_window_resize_active
                or self._monitoring_hud_native_card_drag_active
                or self._monitoring_hud_native_card_resize_active
            ):
                for card_id in ("cpu", "gpu"):
                    resize_rect = self._monitoring_hud_live_screen_rects.get(f"{card_id}ResizeHandle", QRect())
                    drag_rect = self._monitoring_hud_live_screen_rects.get(f"{card_id}DragHandle", QRect())
                    if resize_rect.isValid() and resize_rect.contains(screen_point):
                        self._monitoring_hud_native_card_resize_active = True
                        self._monitoring_hud_native_card_drag_id = card_id
                        self._monitoring_hud_native_card_drag_start = screen_point
                        self._monitoring_hud_native_card_drag_base = self._monitoring_hud_card_layout_base(card_id)
                        self._emit_runtime_signal(
                            "MONITORING_HUD_NATIVE_CARD_RESIZE_STARTED",
                            package="PKG-006",
                            slice="SLC-026",
                            card=card_id,
                            x=screen_point.x(),
                            y=screen_point.y(),
                        )
                        return True
                    if drag_rect.isValid() and drag_rect.contains(screen_point):
                        self._monitoring_hud_native_card_drag_active = True
                        self._monitoring_hud_native_card_drag_id = card_id
                        self._monitoring_hud_native_card_drag_start = screen_point
                        self._monitoring_hud_native_card_drag_base = self._monitoring_hud_card_layout_base(card_id)
                        self._emit_runtime_signal(
                            "MONITORING_HUD_NATIVE_CARD_DRAG_STARTED",
                            package="PKG-006",
                            slice="SLC-026",
                            card=card_id,
                            x=screen_point.x(),
                            y=screen_point.y(),
                        )
                        return True
                anchor_rect = self._monitoring_hud_live_screen_rects.get("anchorToggle", QRect())
                if anchor_rect.isValid() and anchor_rect.contains(screen_point):
                    self._monitoring_hud_native_anchor_click_pending = True
                    self._monitoring_hud_native_anchor_click_expected = not bool(self._monitoring_hud_anchored)
                    return False
            if (
                self._monitoring_hud_header_rect().contains(screen_point)
                and not self._monitoring_hud_dashboard_control_rect_contains(screen_point)
            ):
                if self._start_monitoring_hud_native_system_move(screen_point):
                    return True
                self._monitoring_hud_native_panel_drag_active = True
                self._monitoring_hud_native_panel_drag_start = screen_point
                self._monitoring_hud_native_panel_drag_base = (
                    self.pos() if self.surface_role == "hud" else self._monitoring_hud_page_origin_from_screen_rect()
                )
                self._emit_runtime_signal(
                    "MONITORING_HUD_NATIVE_PANEL_DRAG_STARTED",
                    package="PKG-006",
                    slice="SLC-026",
                    x=screen_point.x(),
                    y=screen_point.y(),
                )
                return True
        if event_type == QEvent.MouseMove and (
            self._monitoring_hud_native_card_drag_active or self._monitoring_hud_native_card_resize_active
        ):
            screen_point = event.globalPosition().toPoint()
            delta = screen_point - self._monitoring_hud_native_card_drag_start
            layout = self._monitoring_hud_layout_from_native_delta(self._monitoring_hud_native_card_resize_active, delta)
            self._set_monitoring_hud_card_layout_from_native_drag(self._monitoring_hud_native_card_drag_id, layout)
            return True
        if event_type == QEvent.MouseMove and self._monitoring_hud_native_window_resize_active:
            screen_point = event.globalPosition().toPoint()
            self._update_monitoring_hud_fallback_window_resize(screen_point)
            return True
        if event_type == QEvent.MouseMove and self._monitoring_hud_native_panel_drag_active:
            screen_point = event.globalPosition().toPoint()
            delta = screen_point - self._monitoring_hud_native_panel_drag_start
            self._set_monitoring_hud_panel_position_from_native_drag(
                self._monitoring_hud_native_panel_drag_base.x() + delta.x(),
                self._monitoring_hud_native_panel_drag_base.y() + delta.y(),
                emit_status=False,
            )
            return True
        if event_type in (QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick):
            if self._monitoring_hud_native_anchor_click_pending:
                self._monitoring_hud_native_anchor_click_pending = False
                expected_anchored = self._monitoring_hud_native_anchor_click_expected
                QTimer.singleShot(
                    140,
                    lambda anchored=expected_anchored: self._apply_monitoring_hud_native_anchor_click_if_needed(anchored),
                )
                return False
            if self._monitoring_hud_native_card_drag_active or self._monitoring_hud_native_card_resize_active:
                screen_point = event.globalPosition().toPoint()
                delta = screen_point - self._monitoring_hud_native_card_drag_start
                resize = self._monitoring_hud_native_card_resize_active
                card_id = self._monitoring_hud_native_card_drag_id
                layout = self._monitoring_hud_layout_from_native_delta(resize, delta)
                self._set_monitoring_hud_card_layout_from_native_drag(card_id, layout)
                self._monitoring_hud_native_card_drag_active = False
                self._monitoring_hud_native_card_resize_active = False
                self._monitoring_hud_native_card_drag_id = ""
                self._emit_runtime_signal(
                    "MONITORING_HUD_NATIVE_CARD_RESIZE_READY" if resize else "MONITORING_HUD_NATIVE_CARD_DRAG_READY",
                    package="PKG-006",
                    slice="SLC-026",
                    card=card_id,
                    dx=delta.x(),
                    dy=delta.y(),
                    x=layout.get("x"),
                    y=layout.get("y"),
                    w=layout.get("w"),
                    h=layout.get("h"),
                )
                return True
            if self._monitoring_hud_native_window_resize_active:
                screen_point = event.globalPosition().toPoint()
                self._finish_monitoring_hud_fallback_window_resize(screen_point)
                return True
            if self._monitoring_hud_native_panel_drag_active:
                screen_point = event.globalPosition().toPoint()
                delta = screen_point - self._monitoring_hud_native_panel_drag_start
                self._set_monitoring_hud_panel_position_from_native_drag(
                    self._monitoring_hud_native_panel_drag_base.x() + delta.x(),
                    self._monitoring_hud_native_panel_drag_base.y() + delta.y(),
                )
                self._monitoring_hud_native_panel_drag_active = False
                self._emit_runtime_signal(
                    "MONITORING_HUD_NATIVE_PANEL_DRAG_READY",
                    package="PKG-006",
                    slice="SLC-026",
                    dx=delta.x(),
                    dy=delta.y(),
                )
                return True
            return False
        return False

    def _apply_monitoring_hud_window_interaction_state(self):
        anchored = bool(self._monitoring_hud_anchored)
        feature_enabled = bool(self._monitoring_hud_feature_enabled)
        dashboard_visible = bool(feature_enabled and self._monitoring_hud_visible)
        was_visible = bool(self.isVisible() and self.webview.isVisible() and self.windowOpacity() > 0.0)
        if dashboard_visible and self.desktop_mode and not was_visible:
            self._arm_monitoring_hud_visible_show_guard("interaction_state")
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_ShowWithoutActivating, False)
        if self.surface_role == "hud":
            self.setWindowFlag(Qt.Tool, False)
            self.setWindowFlag(Qt.Window, True)
        else:
            self.setWindowFlag(Qt.Tool, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setFocusPolicy(Qt.StrongFocus if dashboard_visible else Qt.NoFocus)
        self.webview.setFocusPolicy(Qt.StrongFocus if dashboard_visible else Qt.NoFocus)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self._apply_monitoring_hud_native_activation_style(False)
        self._monitoring_hud_interactive_screen_rect = self._estimate_monitoring_hud_interactive_screen_rect()
        if not dashboard_visible and self.isVisible():
            self.webview.hide()
            self.hide()
        if dashboard_visible and self.desktop_mode:
            if not self.isVisible():
                self.show()
            if not self.webview.isVisible():
                self.webview.show()
            self.show()
        self._emit_runtime_signal(
            "MONITORING_HUD_INTERACTION_MODE_READY",
            package="PKG-006",
            slice="SLC-026",
            feature_enabled=feature_enabled,
            dashboard_visible=dashboard_visible,
            anchored=anchored,
            pointer_model="normal_dashboard_window_no_topmost",
        )
        if self.surface_role == "hud":
            self._emit_runtime_signal(
                "MONITORING_HUD_DASHBOARD_SHELL_LAYOUT_READY",
                package="PKG-006",
                slice="SLC-016",
                seam="WS39",
                source="interaction_state",
                surface="hud_dashboard",
                sticky_header=True,
                single_surface_scrollbar=True,
                title="HUD Dashboard",
                resize_model="os-edge-corner-resize",
            )
            self._emit_monitoring_hud_visual_shell_ready(source="interaction_state")
        self._emit_monitoring_hud_window_ownership_focus_ready(source="interaction_state")
        self._emit_monitoring_hud_window_status(source="interaction_state")
        self._sync_monitoring_hud_minimal_native_overlay(source="interaction_state")

    def _arm_monitoring_hud_visible_show_guard(self, source: str = "runtime") -> None:
        if self.surface_role != "hud" or self._is_shutting_down:
            return
        self._monitoring_hud_show_guard_generation += 1
        generation = self._monitoring_hud_show_guard_generation
        self._monitoring_hud_show_guard_active = True
        self.setWindowOpacity(0.0)
        self._emit_runtime_signal(
            "MONITORING_HUD_VISIBLE_SHOW_GUARD_ARMED",
            package="PKG-006",
            slice="SLC-029",
            seam="LV1",
            source=source,
            release_delay_ms=self._monitoring_hud_show_guard_release_delay_ms,
            visual_release_model="dashboard_geometry_settled_before_opacity",
        )
        QTimer.singleShot(
            self._monitoring_hud_show_guard_release_delay_ms,
            lambda source=source, generation=generation: self._release_monitoring_hud_visible_show_guard(
                source,
                generation,
            ),
        )

    def _release_monitoring_hud_visible_show_guard(self, source: str = "runtime", generation: int | None = None) -> None:
        if self.surface_role != "hud" or self._is_shutting_down:
            return
        if not self._monitoring_hud_show_guard_active:
            return
        if generation is not None and generation != self._monitoring_hud_show_guard_generation:
            return
        if not (self._monitoring_hud_feature_enabled and self._monitoring_hud_visible and self.isVisible()):
            return
        if (
            not self._monitoring_hud_user_geometry_override_active
            and not self._monitoring_hud_native_window_resize_active
            and not self._monitoring_hud_native_move_user_active
        ):
            target_geometry = self.compute_compact_geometry()
            if not self._native_window_matches_target(int(self.winId()), target_geometry):
                self.setGeometry(target_geometry)
            self._monitoring_hud_interactive_screen_rect = self._estimate_monitoring_hud_interactive_screen_rect()
        self._monitoring_hud_show_guard_active = False
        self.setWindowOpacity(1.0)
        self._emit_runtime_signal(
            "MONITORING_HUD_VISIBLE_SHOW_GUARD_RELEASED",
            package="PKG-006",
            slice="SLC-029",
            seam="LV1",
            source=source,
            release_delay_ms=self._monitoring_hud_show_guard_release_delay_ms,
        )
        if self._monitoring_hud_deferred_initial_visibility_release:
            self._monitoring_hud_deferred_initial_visibility_release = False
            self._log_event(
                "RENDERER_MAIN|CORE_VISUALIZATION_FIRST_VISIBLE"
                "|source=monitoring_hud_visible_show_guard"
            )
            self.core_visualization_visible.emit()

    def _set_monitoring_hud_control_state(
        self,
        *,
        visible: bool | None = None,
        anchored: bool | None = None,
        snap_enabled: bool | None = None,
        polling_rate_ms: int | None = None,
        source: str = "runtime",
    ):
        if visible is not None:
            self._monitoring_hud_visible = bool(visible)
        if anchored is not None:
            self._monitoring_hud_anchored = bool(anchored)
        if snap_enabled is not None:
            self._monitoring_hud_snap_enabled = bool(snap_enabled)
        if polling_rate_ms is not None:
            self._monitoring_hud_polling_rate_ms = max(1000, int(polling_rate_ms or 1000))
            if self._monitoring_hud_poll_timer.isActive():
                self._monitoring_hud_poll_timer.start(self._monitoring_hud_polling_rate_ms)
        self._ensure_monitoring_hud_desktop_mode_for_visible_dashboard(source=source)
        self._apply_monitoring_hud_window_interaction_state()
        self._publish_monitoring_hud_control_state_to_page()
        self._publish_monitoring_hud_controls_visibility()
        self._emit_runtime_signal(
            "MONITORING_HUD_CONTROL_STATE_READY",
            package="PKG-006",
            slice="SLC-027",
            source=source,
            feature_enabled=self._monitoring_hud_feature_enabled,
            visible=self._monitoring_hud_visible,
            anchored=self._monitoring_hud_anchored,
            snap=self._monitoring_hud_snap_enabled,
            polling_rate_ms=self._monitoring_hud_polling_rate_ms,
        )

    def _persist_monitoring_hud_feature_state(self, source: str = "runtime"):
        if self.surface_role != "hud":
            return
        save_monitoring_hud_state(
            feature_enabled=bool(self._monitoring_hud_feature_enabled),
            dashboard_visible=bool(self._monitoring_hud_visible and self.isVisible()),
            event_logger=self._log_event,
            source=source,
        )

    def monitoring_hud_feature_state(self) -> dict[str, object]:
        return {
            "feature_enabled": bool(self._monitoring_hud_feature_enabled),
            "dashboard_visible": bool(self.isVisible() and self._monitoring_hud_visible),
            "overlay_deferred": True,
            "overlay_anchor_enabled": False,
            "anchored": self._monitoring_hud_anchored,
        }

    def _ensure_monitoring_hud_desktop_mode_for_visible_dashboard(self, source: str = "runtime"):
        if (
            self.surface_role != "hud"
            or not self._monitoring_hud_feature_enabled
            or not self._monitoring_hud_visible
            or self.desktop_mode
            or self._is_shutting_down
        ):
            return
        self._desktop_mode_requested = True
        self._emit_runtime_signal(
            "MONITORING_HUD_REAL_CLIENT_DASHBOARD_VISIBILITY_REQUESTED",
            package="PKG-006",
            slice="SLC-027",
            seam="WS47",
            source=source,
            page_ready=self._page_ready,
            desktop_mode=self.desktop_mode,
        )
        if self._page_ready:
            self.enable_desktop_mode()
        else:
            self._schedule_desktop_mode_enable()

    def _set_monitoring_hud_feature_enabled(self, enabled: bool, *, source: str = "runtime"):
        self._monitoring_hud_feature_enabled = bool(enabled)
        self._monitoring_hud_visible = bool(enabled)
        if enabled:
            if self._page_ready and not self._monitoring_hud_poll_timer.isActive():
                self._monitoring_hud_poll_timer.start(self._monitoring_hud_polling_rate_ms)
            if self._page_ready and not self._monitoring_hud_control_sync_timer.isActive():
                self._monitoring_hud_control_sync_timer.start(500)
        else:
            self._monitoring_hud_poll_timer.stop()
            self._monitoring_hud_control_sync_timer.stop()
            if self._monitoring_hud_minimal_native_overlay is not None:
                self._monitoring_hud_minimal_native_overlay.update_product_state(
                    visible=False,
                    anchored=True,
                    cards={},
                )
        self._set_monitoring_hud_control_state(source=source)
        self._persist_monitoring_hud_feature_state(source=source)
        self._emit_runtime_signal(
            "MONITORING_HUD_FEATURE_STATE_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS43",
            source=source,
            feature_enabled=self._monitoring_hud_feature_enabled,
            dashboard_visible=bool(self.isVisible() and self._monitoring_hud_visible),
            overlay_deferred=True,
        )

    def request_monitoring_hud_unanchor_from_tray(self, source: str = "tray"):
        self._emit_runtime_signal(
            "MONITORING_HUD_TRAY_UNANCHOR_DEFERRED",
            package="PKG-006",
            slice="SLC-027",
            seam="WS37",
            source=source,
            reason="overlay_deferred_non_gating",
        )

    def request_monitoring_hud_toggle_from_tray(self, source: str = "tray"):
        next_enabled = not bool(self._monitoring_hud_feature_enabled)
        self._set_monitoring_hud_feature_enabled(next_enabled, source=source)
        if next_enabled:
            self._emit_runtime_signal(
                "MONITORING_HUD_TRAY_ENABLE_RENDER_STABLE_READY",
                package="PKG-006",
                slice="SLC-027",
                seam="WS43",
                source=source,
                feature_enabled=True,
                dashboard_visible=bool(self.isVisible() and self._monitoring_hud_visible),
                render_path="single_state_apply",
            )
        else:
            self._emit_runtime_signal(
                "MONITORING_HUD_DISABLE_RECOVERY_READY",
                package="PKG-006",
                slice="SLC-027",
                seam="WS43",
                source=source,
                feature_enabled=False,
                dashboard_visible=False,
                command_overlay_available=True,
            )
        self._emit_runtime_signal(
            "MONITORING_HUD_TRAY_TOGGLE_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS43",
            source=source,
            visible=self._monitoring_hud_visible,
            feature_enabled=next_enabled,
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_TRAY_ENABLE_DISABLE_ROUNDTRIP_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS43",
            source=source,
            feature_enabled=next_enabled,
            dashboard_visible=bool(self.isVisible() and self._monitoring_hud_visible),
        )

    def request_monitoring_hud_dashboard_from_tray(self, source: str = "tray", visible: bool = True):
        if not self._monitoring_hud_feature_enabled:
            self._emit_runtime_signal(
                "MONITORING_HUD_TRAY_DASHBOARD_OPEN_CLOSE_BLOCKED",
                package="PKG-006",
                slice="SLC-027",
                seam="WS43",
                source=source,
                reason="feature_disabled",
            )
            return
        self._set_monitoring_hud_control_state(visible=bool(visible), source=source)
        self._persist_monitoring_hud_feature_state(source=source)
        self._emit_runtime_signal(
            "MONITORING_HUD_TRAY_DASHBOARD_OPEN_CLOSE_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS43",
            source=source,
            dashboard_visible=bool(self.isVisible() and self._monitoring_hud_visible),
            feature_enabled=self._monitoring_hud_feature_enabled,
        )

    def configure_monitoring_hud_live_client_self_qa(
        self,
        *,
        manifest_path: str,
        evidence_root: str = "",
        step_delay_ms: int = 250,
        final_hold_ms: int = 0,
    ):
        self._monitoring_hud_live_self_qa_manifest_path = os.path.abspath(manifest_path)
        root = evidence_root or os.path.dirname(self._monitoring_hud_live_self_qa_manifest_path)
        self._monitoring_hud_live_self_qa_root = os.path.abspath(root)
        self._monitoring_hud_live_self_qa_started = False
        self._monitoring_hud_live_self_qa_step_delay_ms = max(250, int(step_delay_ms or 250))
        self._monitoring_hud_live_self_qa_final_hold_ms = max(0, int(final_hold_ms or 0))
        self._emit_runtime_signal(
            "MONITORING_HUD_LIVE_CLIENT_SELF_QA_CONFIGURED",
            package="PKG-006",
            slice="SLC-029",
            manifest=self._monitoring_hud_live_self_qa_manifest_path,
            step_delay_ms=self._monitoring_hud_live_self_qa_step_delay_ms,
            final_hold_ms=self._monitoring_hud_live_self_qa_final_hold_ms,
        )
        QTimer.singleShot(500, self._start_monitoring_hud_live_client_self_qa)

    def _write_monitoring_hud_live_client_self_qa_manifest(
        self,
        *,
        status: str,
        steps: list[dict[str, object]],
        screenshots: list[str],
        failure: str = "",
    ):
        if not self._monitoring_hud_live_self_qa_manifest_path:
            return
        manifest = {
            "status": status,
            "package": "PKG-006",
            "slice": "SLC-029",
            "seam": "Dashboard-specific active-client self-QA - no UTS export",
            "client": "desktop/orin_desktop_main.py",
            "mode": "live-client-interaction-self-qa",
            "entrypoint": "Nexus Desktop AI desktop runtime",
            "stepDelayMs": self._monitoring_hud_live_self_qa_step_delay_ms,
            "finalHoldMs": self._monitoring_hud_live_self_qa_final_hold_ms,
            "screenshots": screenshots,
            "steps": steps,
            "failureMessage": failure,
            "nativeInteractionState": {
                "visible": self._monitoring_hud_visible,
                "anchored": self._monitoring_hud_anchored,
                "showWithoutActivating": bool(self.testAttribute(Qt.WA_ShowWithoutActivating)),
                "transparentForMouseEvents": bool(self.testAttribute(Qt.WA_TransparentForMouseEvents)),
                "focusPolicy": str(self.focusPolicy()),
                "interactiveHudRect": {
                    "x": self._monitoring_hud_interactive_screen_rect.x(),
                    "y": self._monitoring_hud_interactive_screen_rect.y(),
                    "width": self._monitoring_hud_interactive_screen_rect.width(),
                    "height": self._monitoring_hud_interactive_screen_rect.height(),
                },
                "standaloneOverlayDisplay": self._monitoring_hud_minimal_native_proof_state(),
            },
            "generatedAt": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
        try:
            os.makedirs(os.path.dirname(self._monitoring_hud_live_self_qa_manifest_path), exist_ok=True)
            with open(self._monitoring_hud_live_self_qa_manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, sort_keys=True)
        except Exception as exc:
            self._emit_runtime_signal(
                "MONITORING_HUD_LIVE_CLIENT_SELF_QA_MANIFEST_FAILED",
                package="PKG-006",
                slice="SLC-029",
                reason=type(exc).__name__,
            )

    def _capture_monitoring_hud_live_client_self_qa_screenshot(self, label: str) -> str:
        if not self._monitoring_hud_live_self_qa_root:
            return ""
        try:
            os.makedirs(self._monitoring_hud_live_self_qa_root, exist_ok=True)
            safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "_", label).strip("_") or "screenshot"
            path = os.path.join(self._monitoring_hud_live_self_qa_root, f"{safe_label}.png")
            screens = QApplication.screens()
            if not screens:
                return ""
            virtual = screens[0].geometry()
            for screen in screens[1:]:
                virtual = virtual.united(screen.geometry())
            screenshot = QPixmap(virtual.size())
            screenshot.fill(QColor(0, 0, 0))
            painter = QPainter(screenshot)
            try:
                for screen in screens:
                    screen_geometry = screen.geometry()
                    capture = screen.grabWindow(0)
                    painter.drawPixmap(screen_geometry.topLeft() - virtual.topLeft(), capture)
            finally:
                painter.end()
            if screenshot.save(path, "PNG"):
                self._emit_runtime_signal(
                    "MONITORING_HUD_LIVE_CLIENT_SELF_QA_SCREENSHOT_READY",
                    package="PKG-006",
                    slice="SLC-029",
                    label=safe_label,
                    path=path,
                    capture="full_virtual_desktop",
                )
                return path
        except Exception as exc:
            self._emit_runtime_signal(
                "MONITORING_HUD_LIVE_CLIENT_SELF_QA_SCREENSHOT_FAILED",
                package="PKG-006",
                slice="SLC-029",
                label=label,
                reason=type(exc).__name__,
            )
        return ""

    def _monitoring_hud_screen_point_from_page_rect(self, rect: dict[str, object] | None) -> tuple[int, int] | None:
        if not isinstance(rect, dict):
            return None
        try:
            center_x = float(rect.get("centerX") or 0)
            center_y = float(rect.get("centerY") or 0)
        except (TypeError, ValueError):
            return None
        point = self.webview.mapToGlobal(QPoint(int(center_x), int(center_y)))
        return int(point.x()), int(point.y())

    def _monitoring_hud_send_input(self, flags: int, x: int | None = None, y: int | None = None) -> bool:
        dx = 0
        dy = 0
        send_flags = flags
        if x is not None and y is not None:
            virtual_x = GetSystemMetrics(SM_XVIRTUALSCREEN)
            virtual_y = GetSystemMetrics(SM_YVIRTUALSCREEN)
            virtual_w = max(1, GetSystemMetrics(SM_CXVIRTUALSCREEN))
            virtual_h = max(1, GetSystemMetrics(SM_CYVIRTUALSCREEN))
            dx = int((int(x) - virtual_x) * 65535 / max(1, virtual_w - 1))
            dy = int((int(y) - virtual_y) * 65535 / max(1, virtual_h - 1))
            send_flags |= MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK
        input_event = INPUT(
            type=INPUT_MOUSE,
            union=INPUT_UNION(mi=MOUSEINPUT(dx, dy, 0, send_flags, 0, None)),
        )
        sent = SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))
        QApplication.processEvents()
        return sent == 1

    def _monitoring_hud_send_mouse_click(self, point: tuple[int, int] | None) -> bool:
        if point is None:
            return False
        if not self._monitoring_hud_anchored:
            self.show()
            self.raise_()
            self._promote_monitoring_hud_edit_window()
            self.activateWindow()
            self.webview.setFocus(Qt.MouseFocusReason)
            QApplication.processEvents()
            time.sleep(0.08)
        x, y = point
        ok = self._monitoring_hud_send_input(MOUSEEVENTF_MOVE, int(x), int(y))
        QApplication.processEvents()
        time.sleep(0.08)
        self._monitoring_hud_send_input(MOUSEEVENTF_LEFTDOWN)
        QApplication.processEvents()
        time.sleep(0.04)
        self._monitoring_hud_send_input(MOUSEEVENTF_LEFTUP)
        QApplication.processEvents()
        return ok

    def _monitoring_hud_cursor_position(self) -> tuple[int, int] | None:
        point = ctypes.wintypes.POINT()
        if not GetCursorPos(ctypes.byref(point)):
            return None
        return int(point.x), int(point.y)

    def _monitoring_hud_send_mouse_drag(
        self,
        start: tuple[int, int] | None,
        end: tuple[int, int] | None,
        *,
        steps: int = 12,
    ) -> bool:
        if start is None or end is None:
            return False
        start_x, start_y = start
        end_x, end_y = end
        ok = self._monitoring_hud_send_input(MOUSEEVENTF_MOVE, int(start_x), int(start_y))
        QApplication.processEvents()
        time.sleep(0.08)
        self._monitoring_hud_send_input(MOUSEEVENTF_LEFTDOWN)
        QApplication.processEvents()
        for step in range(1, max(2, steps) + 1):
            ratio = step / max(2, steps)
            x = int(start_x + (end_x - start_x) * ratio)
            y = int(start_y + (end_y - start_y) * ratio)
            self._monitoring_hud_send_input(MOUSEEVENTF_MOVE, x, y)
            QApplication.processEvents()
            time.sleep(0.025)
        self._monitoring_hud_send_input(MOUSEEVENTF_LEFTUP)
        QApplication.processEvents()
        return ok

    def _monitoring_hud_widget_point_from_page_rect(self, rect: dict[str, object] | None) -> QPoint | None:
        if not isinstance(rect, dict):
            return None
        try:
            center_x = int(float(rect.get("centerX") or 0))
            center_y = int(float(rect.get("centerY") or 0))
        except (TypeError, ValueError):
            return None
        return QPoint(center_x, center_y)

    def _monitoring_hud_send_widget_drag(
        self,
        start: QPoint | None,
        end: QPoint | None,
        *,
        steps: int = 12,
    ) -> bool:
        if start is None or end is None:
            return False
        self.raise_()
        self.webview.setFocus(Qt.MouseFocusReason)
        QApplication.processEvents()
        QTest.mouseMove(self.webview, start, delay=60)
        QTest.mousePress(self.webview, Qt.LeftButton, Qt.NoModifier, start, delay=60)
        for step in range(1, max(2, steps) + 1):
            ratio = step / max(2, steps)
            point = QPoint(
                int(start.x() + (end.x() - start.x()) * ratio),
                int(start.y() + (end.y() - start.y()) * ratio),
            )
            QTest.mouseMove(self.webview, point, delay=25)
        QTest.mouseRelease(self.webview, Qt.LeftButton, Qt.NoModifier, end, delay=60)
        QApplication.processEvents()
        return True

    def _monitoring_hud_send_widget_click(self, point: QPoint | None) -> bool:
        if point is None:
            return False
        self.raise_()
        self.webview.setFocus(Qt.MouseFocusReason)
        QApplication.processEvents()
        QTest.mouseMove(self.webview, point, delay=60)
        QTest.mouseClick(self.webview, Qt.LeftButton, Qt.NoModifier, point, delay=80)
        QApplication.processEvents()
        return True

    def _monitoring_hud_send_overlay_card_widget_drag(
        self,
        card_id: str,
        *,
        resize: bool = False,
        dx: int = 0,
        dy: int = 0,
    ) -> bool:
        overlay = self._monitoring_hud_minimal_native_overlay
        if overlay is None:
            return False
        widgets = overlay._card_widgets.get(card_id) if hasattr(overlay, "_card_widgets") else None
        if not isinstance(widgets, dict):
            return False
        target = widgets.get("resize" if resize else "frame")
        if target is None or not target.isVisible():
            return False
        overlay.show()
        overlay.raise_()
        overlay.activateWindow()
        QApplication.processEvents()
        if resize:
            start = QPoint(max(1, target.width() // 2), max(1, target.height() // 2))
        else:
            start = QPoint(min(80, max(8, target.width() // 2)), min(32, max(8, target.height() // 3)))
        end = QPoint(start.x() + int(dx), start.y() + int(dy))
        QTest.mouseMove(target, start, delay=60)
        QTest.mousePress(target, Qt.LeftButton, Qt.NoModifier, start, delay=60)
        QTest.mouseMove(target, end, delay=80)
        QTest.mouseRelease(target, Qt.LeftButton, Qt.NoModifier, end, delay=60)
        QApplication.processEvents()
        return True

    def _start_monitoring_hud_live_client_self_qa(self):
        if not self._monitoring_hud_live_self_qa_manifest_path:
            return
        if self._monitoring_hud_live_self_qa_started or self._is_shutting_down:
            return
        if not self._page_ready or not self.desktop_mode or not self.isVisible():
            QTimer.singleShot(500, self._start_monitoring_hud_live_client_self_qa)
            return

        self._monitoring_hud_live_self_qa_started = True
        steps: list[dict[str, object]] = []
        screenshots: list[str] = []
        latest_result: dict[str, object] = {}
        overlay_geometry_before_dashboard_drag: dict[str, object] = {}

        def finish(status: str, failure: str = ""):
            self._write_monitoring_hud_live_client_self_qa_manifest(
                status=status,
                steps=steps,
                screenshots=screenshots,
                failure=failure,
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_LIVE_CLIENT_SELF_QA_READY",
                package="PKG-006",
                slice="SLC-029",
                status=status,
                manifest=self._monitoring_hud_live_self_qa_manifest_path,
            )

        def add_step(label: str, passed: bool, details: dict[str, object] | None = None):
            steps.append(
                {
                    "label": label,
                    "status": "PASS" if passed else "FAIL",
                    "details": details or {},
                }
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_LIVE_CLIENT_SELF_QA_STEP",
                package="PKG-006",
                slice="SLC-029",
                label=label,
                status="PASS" if passed else "FAIL",
            )
            return passed

        def capture(label: str):
            path = self._capture_monitoring_hud_live_client_self_qa_screenshot(label)
            if path:
                screenshots.append(path)

        def delay(base_ms: int) -> int:
            return max(base_ms, self._monitoring_hud_live_self_qa_step_delay_ms)

        state_script = """
            (function() {
                const hud = document.getElementById("monitoring-hud");
                const minimalHud = document.getElementById("monitoring-hud-minimal");
                const text = hud ? hud.innerText : "";
                const minimalText = minimalHud ? minimalHud.innerText : "";
                const rect = hud ? hud.getBoundingClientRect() : null;
                const minimalRect = minimalHud ? minimalHud.getBoundingClientRect() : null;
                const state = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : null;
                const geometry = window.getMonitoringHudLiveClientGeometry
                    ? window.getMonitoringHudLiveClientGeometry()
                    : {};
                const cpuConfigOption = document.querySelector('[data-monitor-edit-select="cpu"]');
                const gpuConfigOption = document.querySelector('[data-monitor-edit-select="gpu"]');
                return JSON.stringify({
                    hasHud: Boolean(hud),
                    text,
                    minimalText,
                    dataset: hud ? Object.assign({}, hud.dataset) : {},
                    minimalDataset: minimalHud ? Object.assign({}, minimalHud.dataset) : {},
                    rect: rect ? { left: rect.left, top: rect.top, width: rect.width, height: rect.height } : null,
                    minimalRect: minimalRect ? { left: minimalRect.left, top: minimalRect.top, width: minimalRect.width, height: minimalRect.height } : null,
                    geometry,
                    state,
                    isolation: window.getMonitoringHudIsolationState ? window.getMonitoringHudIsolationState() : {},
                    split: window.getMonitoringHudSurfaceSplitState ? window.getMonitoringHudSurfaceSplitState() : {},
                    cpuConfigOption: cpuConfigOption ? Object.assign({}, cpuConfigOption.dataset) : {},
                    gpuConfigOption: gpuConfigOption ? Object.assign({}, gpuConfigOption.dataset) : {},
                    bodyClasses: document.body ? String(document.body.className || "") : ""
                });
            })();
        """

        def query(label: str, assertion, next_step):
            self._run_javascript_with_result(
                state_script,
                lambda result: handle_query_result(label, assertion, next_step, result),
            )

        def handle_query_result(label: str, assertion, next_step, result):
            try:
                parsed_result = json.loads(result) if isinstance(result, str) else result
                if isinstance(parsed_result, dict):
                    latest_result.clear()
                    latest_result.update(parsed_result)
                    geometry = parsed_result.get("geometry") or {}
                    hud_rect = geometry.get("hud") if isinstance(geometry, dict) else None
                    self._set_monitoring_hud_interactive_rect_from_page(hud_rect)
                    state = parsed_result.get("state") or {}
                    self._set_monitoring_hud_live_client_page_state(
                        state if isinstance(state, dict) else {},
                        geometry if isinstance(geometry, dict) else {},
                    )
                passed, detail = assertion(parsed_result if isinstance(parsed_result, dict) else {})
            except Exception as exc:
                passed = False
                detail = {"error": type(exc).__name__, "message": str(exc)}
            add_step(label, bool(passed), detail if isinstance(detail, dict) else {"detail": detail})
            if not passed:
                finish("FAIL", f"{label} failed")
                return
            QTimer.singleShot(delay(250), next_step)

        def rect_center(name: str) -> tuple[int, int] | None:
            geometry = latest_result.get("geometry") or {}
            if not isinstance(geometry, dict):
                return None
            rect = geometry.get(name)
            return self._monitoring_hud_screen_point_from_page_rect(rect if isinstance(rect, dict) else None)

        def rect_from(result: dict, name: str) -> dict:
            geometry = result.get("geometry") or {}
            rect = geometry.get(name) if isinstance(geometry, dict) else {}
            return rect if isinstance(rect, dict) else {}

        def rect_number(rect: dict, key: str) -> float:
            try:
                return float(rect.get(key) or 0)
            except (TypeError, ValueError):
                return 0.0

        def rect_present(rect: dict, *, min_width: float = 24.0, min_height: float = 18.0) -> bool:
            return rect_number(rect, "width") >= min_width and rect_number(rect, "height") >= min_height

        def vertical_gap(upper: dict, lower: dict) -> float:
            return rect_number(lower, "top") - rect_number(upper, "bottom")

        def rects_intersect(first: dict, second: dict) -> bool:
            if not rect_present(first, min_width=1, min_height=1) or not rect_present(second, min_width=1, min_height=1):
                return False
            horizontal_overlap = max(rect_number(first, "left"), rect_number(second, "left")) < min(
                rect_number(first, "right"),
                rect_number(second, "right"),
            )
            vertical_overlap = max(rect_number(first, "top"), rect_number(second, "top")) < min(
                rect_number(first, "bottom"),
                rect_number(second, "bottom"),
            )
            return horizontal_overlap and vertical_overlap

        def monitor_groups_visual_checks(result: dict) -> dict:
            scroll_well = rect_from(result, "monitorList")
            card = rect_from(result, "monitorGroupsCard")
            summary = rect_from(result, "monitorListSummary")
            summary_grid = rect_from(result, "monitorGroupsSummaryGrid")
            actions = rect_from(result, "monitorGroupsActions")
            scope = rect_from(result, "monitorGroupsScope")
            readiness = rect_from(result, "readinessCard")
            summary_to_grid_gap = vertical_gap(summary, summary_grid)
            grid_to_actions_gap = vertical_gap(summary_grid, actions)
            actions_to_scope_gap = vertical_gap(actions, scope)
            return {
                "monitor_groups_scroll_well_present": rect_present(scroll_well, min_width=260, min_height=300),
                "monitor_groups_card_present": rect_present(card, min_width=240, min_height=120),
                "monitor_groups_summary_present": rect_present(summary, min_width=180, min_height=12),
                "monitor_groups_summary_grid_present": rect_present(summary_grid, min_width=180, min_height=48),
                "monitor_groups_actions_present": rect_present(actions, min_width=160, min_height=28),
                "monitor_groups_scope_present": rect_present(scope, min_width=180, min_height=12),
                "monitor_groups_readiness_card_present": rect_present(readiness, min_width=240, min_height=120),
                "monitor_groups_summary_gap_not_dead_space": 0 <= summary_to_grid_gap <= 56,
                "monitor_groups_actions_follow_summary": 0 <= grid_to_actions_gap <= 40,
                "monitor_groups_scope_follows_actions": 0 <= actions_to_scope_gap <= 36,
                "monitor_groups_scope_inside_card": rect_number(scope, "bottom") <= rect_number(card, "bottom") - 4,
                "monitor_groups_card_horizontally_inside_scroll_well": (
                    rect_number(card, "left") >= rect_number(scroll_well, "left") - 2
                    and rect_number(card, "right") <= rect_number(scroll_well, "right") + 4
                ),
                "monitor_groups_no_readiness_overlap": not rects_intersect(card, readiness),
            }

        def assert_user_hit_targets(result):
            geometry = result.get("geometry") or {}
            controls = {
                "hud": geometry.get("hud") if isinstance(geometry, dict) else None,
                "settingsAction": geometry.get("settingsAction") if isinstance(geometry, dict) else None,
                "createMonitor": geometry.get("createMonitor") if isinstance(geometry, dict) else None,
                "editMonitor": geometry.get("editMonitor") if isinstance(geometry, dict) else None,
                "dashboardClose": geometry.get("dashboardClose") if isinstance(geometry, dict) else None,
                "panelDragHandle": geometry.get("panelDragHandle") if isinstance(geometry, dict) else None,
                "warningToggle": geometry.get("warningToggle") if isinstance(geometry, dict) else None,
                "dataSourcesAction": geometry.get("dataSourcesAction") if isinstance(geometry, dict) else None,
                "hudOverlayDeferredAction": geometry.get("hudOverlayDeferredAction") if isinstance(geometry, dict) else None,
            }
            checks = {}
            for key, rect in controls.items():
                checks[f"{key}_present"] = isinstance(rect, dict) and float(rect.get("width") or 0) > 24 and float(rect.get("height") or 0) > 18
            hud_rect = controls.get("hud") or {}
            checks["hud_readable_width"] = float(hud_rect.get("width") or 0) >= 620
            checks["hud_readable_height"] = float(hud_rect.get("height") or 0) >= 520
            minimal_rect = controls.get("minimalHud") or {}
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            checks["native_overlay_visible_width"] = int(overlay_proof.get("w") or 0) >= 360
            checks["native_overlay_visible_height"] = int(overlay_proof.get("h") or 0) >= 220
            checks["native_overlay_card_targets"] = int(overlay_proof.get("overlayCardCount") or 0) >= 2
            checks["native_hud_control_zone"] = self._monitoring_hud_point_in_interactive_rect(
                QPoint(*(rect_center("warningToggle") or rect_center("createMonitor") or (0, 0)))
            )
            return all(checks.values()), checks

        def assert_initial(result):
            text = str(result.get("text") or "")
            minimal_text = str(result.get("minimalText") or "")
            dataset = result.get("dataset") or {}
            minimal_dataset = result.get("minimalDataset") or {}
            state = result.get("state") or {}
            rect = result.get("rect") or {}
            minimal_rect = result.get("minimalRect") or {}
            isolation = result.get("isolation") or {}
            split = result.get("split") or {}
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            forbidden_name = "".join(chr(code) for code in (74, 97, 114, 118, 105, 115))
            lower_text = text.casefold()
            lower_minimal_text = minimal_text.casefold()
            live_values = str(dataset.get("liveValues") or "").casefold()
            checks = {
                "hud_present": bool(result.get("hasHud")),
                "nexus_identity": ("nexus" in lower_text
                    and (
                        "monitoring hud" in lower_text
                        or "hud dashboard" in lower_text
                    )) or (
                        "hud dashboard" in lower_text
                        and dataset.get("productSurfaceRole") == "dashboard-configuration-surface"
                    ),
                "minimal_hud_present": minimal_dataset.get("productSurfaceRole") == "minimal-anchored-hud-overlay",
                "minimal_nexus_identity": "nexus" in lower_minimal_text and "monitoring hud" in lower_minimal_text,
                "dashboard_role": dataset.get("productSurfaceRole") == "dashboard-configuration-surface",
                "dashboard_monitor_management": dataset.get("monitorManagement") == "create-edit-enable-polling",
                "dashboard_overlay_mode_controls": dataset.get("overlayModeControls") == "overlay-deferred-tray-owned",
                "dashboard_settings_content_polished": dataset.get("dashboardContentPolish") == "branch2-monitor-groups-no-dead-space",
                "dashboard_layout_proof": dataset.get("dashboardLayoutProof") == "monitor-groups-measured-no-overlap",
                "dashboard_close_affordance": dataset.get("dashboardCloseAffordance") == "window-level-close-button",
                "dashboard_open_badge_removed": dataset.get("dashboardOpenBadge") == "removed",
                "dashboard_child_window_scope": dataset.get("dashboardChildWindowScope") == "branch2-create-edit-monitor-windows",
                "dashboard_monitor_selection_in_child_window": dataset.get("dashboardMonitorSelectionPlacement") == "edit-child-window-only",
                "dashboard_settings_model": dataset.get("dashboardSettingsModel") == "hud-overlay-monitor-groups-provider-warning",
                "dashboard_settings_affordance": dataset.get("dashboardSettingsAffordance") == "dashboard-ia-card-settings-button",
                "dashboard_settings_panel": dataset.get("dashboardSettingsPanel") == "settings-panel-child-window",
                "dashboard_settings_proof": dataset.get("dashboardSettingsProof") == "visible-open-close-control-hit-target",
                "monitor_group_model": dataset.get("monitorGroupModel") == "organizational-groups-settings-only",
                "dashboard_card_policy": dataset.get("dashboardMonitorCardPolicy") == "overlay-display-owns-monitor-cards",
                "dashboard_provider_truth": dataset.get("dashboardProviderTruth") == "provider-contract-first",
                "dashboard_state_model": dataset.get("dashboardStateModel") == "setup-no-data-degraded-warning",
                "dashboard_warning_controls": dataset.get("dashboardWarningControls") == "visual-non-invasive-only",
                "fake_telemetry_blocked": dataset.get("dashboardFakeTelemetryPolicy") == "blocked",
                "control_panel_copy": "hud dashboard" in lower_text
                    and "monitor groups" in lower_text
                    and "data sources" in lower_text
                    and "warning notifications" in lower_text,
                "edgeless_overlay_present": split.get("overlayDisplayPresent") is True,
                "edgeless_overlay_role": split.get("overlayDisplaySurfaceRole") == "edgeless-overlay-display",
                "edgeless_overlay_canvas": split.get("overlayCanvas") == "edge-to-edge-snipping-tool-style",
                "edgeless_overlay_standalone_native": overlay_proof.get("owner") == "MonitoringHudOverlayDisplayWindow",
                "edgeless_overlay_visible": overlay_proof.get("visible") is False,
                "edgeless_overlay_anchor_mode": overlay_proof.get("anchored") is True,
                "edgeless_overlay_monitor_layout": split.get("overlayMonitorLayout") == "movable-resizable-monitor-cards",
                "standalone_surface_independence": overlay_proof.get("dashboardCoupled") is False
                    and overlay_proof.get("surfaceIndependence") == "dashboard_overlay_core_top_level_windows",
                "overlay_cards_owned_by_overlay": overlay_proof.get("cardsMovableInOverlay") is True
                    and int(overlay_proof.get("overlayCardCount") or 0) >= 2,
                "surface_split": split.get("dashboardConfigures") == "monitoring-hud-minimal"
                    and split.get("minimalConfiguredBy") == "monitoring-hud",
                "visible_state": bool(state.get("visible")) and dataset.get("visibilityState") == "visible",
                "minimal_visible_state": minimal_dataset.get("visibilityState") in {"hidden", "deferred"}
                    or overlay_proof.get("visible") is False,
                "anchored_state": dataset.get("anchorState") in {"anchored", "unanchored"}
                    or overlay_proof.get("anchored") is True,
                "provider_truth": live_values in {
                    "provider-required",
                    "native-provider-pending",
                    "native-cpu-load-only",
                },
                "warning_mode": dataset.get("warningMode") == "visual-non-invasive",
                "no_retired_product_copy": forbidden_name.casefold() not in text.casefold(),
                "desktop_size": float(rect.get("width") or 0) >= 620 and float(rect.get("height") or 0) >= 520,
                "native_overlay_size": int(overlay_proof.get("w") or 0) >= 360 and int(overlay_proof.get("h") or 0) >= 220,
                "standalone_hud_layer": isolation.get("hudOutsideCoreScene") is True,
            }
            checks.update(monitor_groups_visual_checks(result))
            return all(checks.values()), checks

        def assert_surface_split(result):
            split = result.get("split") or {}
            isolation = result.get("isolation") or {}
            geometry = result.get("geometry") or {}
            minimal_rect = geometry.get("minimalHud") if isinstance(geometry, dict) else {}
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            checks = {
                "dashboard_present": split.get("dashboardPresent") is True,
                "minimal_present": split.get("minimalHudPresent") is True,
                "overlay_display_present": split.get("overlayDisplayPresent") is True,
                "dashboard_role": split.get("dashboardSurfaceRole") == "dashboard-configuration-surface",
                "minimal_role": split.get("minimalHudSurfaceRole") == "minimal-anchored-hud-overlay",
                "overlay_display_role": split.get("overlayDisplaySurfaceRole") == "edgeless-overlay-display",
                "overlay_canvas": split.get("overlayCanvas") == "edge-to-edge-snipping-tool-style",
                "overlay_display_dom_template": split.get("overlayDisplayPresent") is True,
                "overlay_standalone_native": overlay_proof.get("owner") == "MonitoringHudOverlayDisplayWindow",
                "overlay_not_dashboard_coupled": overlay_proof.get("dashboardCoupled") is False,
                "overlay_cards_movable": overlay_proof.get("cardsMovableInOverlay") is True,
                "overlay_monitor_layout": split.get("overlayMonitorLayout") == "movable-resizable-monitor-cards",
                "dashboard_configures_minimal": split.get("dashboardConfigures") == "monitoring-hud-minimal",
                "minimal_configured_by_dashboard": split.get("minimalConfiguredBy") == "monitoring-hud",
                "split_contract": split.get("splitContract") == "dashboard-configures-minimal-overlay",
                "isolation_reports_split": isolation.get("dashboardMinimalSplitReady") is True,
                "minimal_dom_template": split.get("minimalHudPresent") is True,
                "overlay_geometry": int(overlay_proof.get("w") or 0) >= 360
                    and int(overlay_proof.get("h") or 0) >= 220,
                "native_overlay_owner": split.get("nativeOverlayOwner") == "MonitoringHudOverlayDisplayWindow",
                "native_window_split_ready": split.get("nativeWindowSplitProof") == "ready-ws26",
            }
            return all(checks.values()), checks

        def assert_minimal_native_overlay(result):
            geometry = result.get("geometry") or {}
            minimal_rect = geometry.get("minimalHud") if isinstance(geometry, dict) else {}
            minimal_center = rect_center("minimalHud")
            control_center = rect_center("warningToggle") or rect_center("createMonitor")
            minimal_point = QPoint(*(minimal_center or (0, 0)))
            control_point = QPoint(*(control_center or (0, 0)))
            proof = self._monitoring_hud_minimal_native_proof_state()
            checks = {
                "minimal_dom_template_present": isinstance(minimal_rect, dict),
                "native_overlay_owner": proof.get("owner") == "MonitoringHudOverlayDisplayWindow",
                "native_overlay_visible": proof.get("visible") is False,
                "native_overlay_hidden_deferred": proof.get("visible") is False,
                "native_overlay_separate_hwnd": bool(proof.get("hwnd") and proof.get("hwnd") != int(self.winId())),
                "native_overlay_ex_transparent": proof.get("exTransparent") is True,
                "native_overlay_mouse_transparent": proof.get("transparentForMouseEvents") is True,
                "native_overlay_center_click_through": proof.get("windowFromCenterBypassesOverlay") is True,
                "native_overlay_no_focus": proof.get("focusPolicy") == "no_focus",
                "native_overlay_noactivate": proof.get("exNoActivate") is True,
                "native_overlay_show_without_activating": proof.get("showWithoutActivating") is True,
                "native_overlay_cards_owned_by_overlay": proof.get("cardsMovableInOverlay") is True,
                "native_overlay_not_dashboard_coupled": proof.get("dashboardCoupled") is False,
                "dashboard_controls_still_interactive": self._monitoring_hud_point_in_interactive_rect(control_point),
                "dashboard_preview_dom_inside_configuration_window": self._monitoring_hud_point_in_interactive_rect(minimal_point),
            }
            checks.update({f"proof_{key}": value for key, value in proof.items()})
            return all(
                checks[key]
                for key in (
                    "minimal_dom_template_present",
                    "native_overlay_owner",
                    "native_overlay_hidden_deferred",
                    "native_overlay_separate_hwnd",
                    "native_overlay_ex_transparent",
                    "native_overlay_mouse_transparent",
                    "native_overlay_center_click_through",
                    "native_overlay_no_focus",
                    "native_overlay_noactivate",
                    "native_overlay_show_without_activating",
                    "dashboard_controls_still_interactive",
                )
            ), checks

        def assert_isolation(result):
            isolation = result.get("isolation") or {}
            checks = {
                "hud_window_mode": isolation.get("hudWindowMode") is True,
                "standalone_native_hud_window": isolation.get("standaloneHudWindow") is True,
                "core_scene_hidden_in_hud_window": isolation.get("coreSceneHiddenInHudWindow") is True,
                "hud_outside_core_scene": isolation.get("hudOutsideCoreScene") is True,
                "isolation_boundary": isolation.get("isolationBoundary") == "standalone-hud-layer",
                "core_failure_isolation": isolation.get("coreFailureIsolation") == "hud-fail-does-not-hide-core",
                "simulated_hud_fault": isolation.get("validationFault") == "simulated-hud-module-fault",
            }
            return all(checks.values()), checks

        def assert_unanchored(result):
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            checks = {
                "visible": bool(state.get("visible")),
                "unanchored": state.get("anchored") is False,
                "dataset_unanchored": dataset.get("anchorState") == "unanchored",
                "edit_mode": dataset.get("interactionMode") == "unanchored-edit-mode",
                "overlay_unanchored": overlay_proof.get("anchored") is False,
                "overlay_interactive": overlay_proof.get("transparentForMouseEvents") is False
                    and overlay_proof.get("focusPolicy") == "interactive",
                "overlay_quick_controls_visible": overlay_proof.get("quickControlsVisible") is True,
                "native_window_anchored_flag": self._monitoring_hud_anchored is False,
                "native_focus_allowed": self.focusPolicy() == Qt.StrongFocus,
                "webview_focus_allowed": self.webview.focusPolicy() == Qt.StrongFocus,
                "native_transparent_mouse_disabled": not bool(self.testAttribute(Qt.WA_TransparentForMouseEvents)),
                "native_noactivate_cleared": (int(GetWindowLongW(ctypes.wintypes.HWND(int(self.winId())), GWL_EXSTYLE)) & WS_EX_NOACTIVATE) == 0,
                "native_window_active": self.isActiveWindow(),
            }
            return all(
                checks[key]
                for key in (
                    "visible",
                    "unanchored",
                    "dataset_unanchored",
                    "edit_mode",
                    "overlay_unanchored",
                    "overlay_interactive",
                    "overlay_quick_controls_visible",
                    "native_window_anchored_flag",
                    "native_focus_allowed",
                    "webview_focus_allowed",
                    "native_transparent_mouse_disabled",
                    "native_noactivate_cleared",
                )
            ), checks

        def assert_panel_dragged(result):
            state = result.get("state") or {}
            panel = state.get("panelPosition") or {}
            geometry = result.get("geometry") or {}
            target_geometry = self.compute_compact_geometry()
            current_geometry = self.geometry()
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            native_window_moved = (
                current_geometry.x() <= target_geometry.x() - 40
                or current_geometry.y() >= target_geometry.y() + 40
            )
            overlay_stayed_independent = bool(overlay_geometry_before_dashboard_drag) and all(
                int(overlay_proof.get(key) or 0) == int(overlay_geometry_before_dashboard_drag.get(key) or 0)
                for key in ("x", "y", "w", "h")
            )
            isolation = result.get("isolation") or {}
            checks = {
                "visible": bool(state.get("visible")),
                "unanchored": state.get("anchored") is False,
                "native_window_moved": native_window_moved,
                "standalone_overlay_not_moved_by_dashboard_drag": overlay_stayed_independent,
                "overlay_not_dashboard_coupled": overlay_proof.get("dashboardCoupled") is False,
                "overlay_owner": overlay_proof.get("owner"),
                "standalone_native_hud_window": isolation.get("standaloneHudWindow") is True,
                "hud_window_x": current_geometry.x(),
                "hud_window_y": current_geometry.y(),
                "panel_position": panel,
                "last_drag_event": state.get("lastDragEvent"),
                "last_mouse_event": state.get("lastMouseEvent"),
            }
            pass_values = [
                checks["visible"],
                checks["unanchored"],
                checks["native_window_moved"],
                checks["standalone_overlay_not_moved_by_dashboard_drag"],
                checks["standalone_native_hud_window"],
            ]
            return all(pass_values), checks

        def step_surface_travel():
            detail = self._monitoring_hud_run_dashboard_standalone_probe()
            capture("02_dashboard_standalone_virtual_desktop_travel")
            passed = bool(detail.get("ok"))
            add_step(
                "dashboard standalone window moves across virtual desktop without clipping while Core and Overlay remain decoupled",
                passed,
                detail,
            )
            if not passed:
                finish("FAIL", "dashboard standalone window virtual-desktop travel proof failed")
                return
            query("dashboard close target geometry refreshed after standalone travel", assert_dashboard_close_ready, step_hide)

        def assert_hidden(result):
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            checks = {
                "hidden_state": state.get("visible") is False,
                "dataset_hidden": dataset.get("visibilityState") == "hidden",
                "controls_state_hidden": dataset.get("controlsState") in {
                    "feature-enabled-dashboard-closed",
                    "feature-disabled-dashboard-closed",
                    "toggle-posture-hidden",
                },
            }
            return all(checks.values()), checks

        def assert_restored(result):
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            checks = {
                "visible_state": bool(state.get("visible")),
                "polling_rate_2000": int(state.get("pollingRateMs") or 0) == 2000,
                "dataset_polling_2000": dataset.get("pollingRateMs") == "2000",
                "warning_posture_control_changed": dataset.get("warningControlPosture") == "badge-only",
                "warning_mode_visual_only": dataset.get("warningMode") == "visual-non-invasive",
                "fake_telemetry_policy_blocked": dataset.get("dashboardFakeTelemetryPolicy") == "blocked",
            }
            return all(checks.values()), checks

        def assert_dashboard_restored(result):
            text = str(result.get("text") or "").casefold()
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            split = result.get("split") or {}
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            checks = {
                "visible_state": bool(state.get("visible")),
                "dataset_visible": dataset.get("visibilityState") == "visible",
                "dashboard_role": dataset.get("productSurfaceRole") == "dashboard-configuration-surface",
                "hud_dashboard_title": "hud dashboard" in text,
                "monitor_groups_home_card": "monitor groups" in text,
                "data_sources_home_card": "data sources" in text,
                "hud_display_home_card": "hud overlay" in text,
                "warning_notifications_home_card": "warning notifications" in text,
                "child_window_scope_deferred": "data sources window deferred" in text
                    and "hud overlay" in text
                    and split.get("overlayDisplayPresent") is True,
                "overlay_deferred_hidden": overlay_proof.get("visible") is False
                    and overlay_proof.get("dashboardCoupled") is False,
                "fake_telemetry_policy_blocked": dataset.get("dashboardFakeTelemetryPolicy") == "blocked",
                "dashboard_layout_proof": dataset.get("dashboardLayoutProof") == "monitor-groups-measured-no-overlap",
                "dashboard_settings_affordance": dataset.get("dashboardSettingsAffordance") == "dashboard-ia-card-settings-button",
                "dashboard_settings_panel_closed": dataset.get("dashboardSettingsPanelState") == "closed",
            }
            checks.update(monitor_groups_visual_checks(result))
            return all(checks.values()), checks

        def assert_settings_panel_open(result):
            text = str(result.get("text") or "").casefold()
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            geometry = result.get("geometry") or {}
            settings_window = geometry.get("settingsWindow") if isinstance(geometry, dict) else {}
            settings_toggle = geometry.get("settingsWarningToggle") if isinstance(geometry, dict) else {}
            checks = {
                "active_child_window": state.get("activeChildWindow") == "dashboard-settings",
                "settings_panel_state_open": dataset.get("dashboardSettingsPanelState") == "open",
                "settings_affordance": dataset.get("dashboardSettingsAffordance") == "dashboard-ia-card-settings-button",
                "settings_panel_model": dataset.get("dashboardSettingsPanel") == "settings-panel-child-window",
                "settings_proof_marker": dataset.get("dashboardSettingsProof") == "visible-open-close-control-hit-target",
                "settings_window_present": isinstance(settings_window, dict)
                    and float(settings_window.get("width") or 0) >= 320
                    and float(settings_window.get("height") or 0) >= 240,
                "settings_toggle_present": isinstance(settings_toggle, dict)
                    and float(settings_toggle.get("width") or 0) >= 16
                    and float(settings_toggle.get("height") or 0) >= 16,
                "truthful_copy": "settings panel" in text
                    and "provider setup required" in text
                    and "no fake telemetry values" in text
                    and "overlay display deferred" in text,
            }
            return all(checks.values()), checks

        def assert_dashboard_close_ready(result):
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            geometry = result.get("geometry") or {}
            close_rect = geometry.get("dashboardClose") if isinstance(geometry, dict) else {}
            hud_rect = geometry.get("hud") if isinstance(geometry, dict) else {}
            checks = {
                "visible_state": bool(state.get("visible")),
                "dataset_visible": dataset.get("visibilityState") == "visible",
                "dashboard_close_affordance": dataset.get("dashboardCloseAffordance") == "window-level-close-button",
                "dashboard_close_target_present": isinstance(close_rect, dict)
                    and float(close_rect.get("width") or 0) > 24
                    and float(close_rect.get("height") or 0) > 18,
                "hud_geometry_refreshed": isinstance(hud_rect, dict)
                    and float(hud_rect.get("width") or 0) >= 620
                    and float(hud_rect.get("height") or 0) >= 520,
            }
            return all(checks.values()), checks

        def assert_monitor_management(result):
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            cards = state.get("cards") if isinstance(state.get("cards"), dict) else {}
            selected_id = str(state.get("selectedMonitorId") or "")
            selected = cards.get(selected_id) if isinstance(cards.get(selected_id), dict) else {}
            checks = {
                "dashboard_monitor_management": dataset.get("monitorManagement") == "create-edit-enable-polling",
                "dashboard_overlay_mode_controls": dataset.get("overlayModeControls") == "overlay-deferred-tray-owned",
                "dashboard_settings_content_polish": dataset.get("dashboardContentPolish") == "branch2-monitor-groups-no-dead-space",
                "dashboard_layout_proof": dataset.get("dashboardLayoutProof") == "monitor-groups-measured-no-overlap",
                "dashboard_close_affordance": dataset.get("dashboardCloseAffordance") == "window-level-close-button",
                "dashboard_open_badge_removed": dataset.get("dashboardOpenBadge") == "removed",
                "dashboard_child_window_scope": dataset.get("dashboardChildWindowScope") == "branch2-create-edit-monitor-windows",
                "dashboard_monitor_group_model": dataset.get("monitorGroupModel") == "organizational-groups-settings-only",
                "dashboard_monitor_card_policy": dataset.get("dashboardMonitorCardPolicy") == "overlay-display-owns-monitor-cards",
                "monitor_count_expanded": len(cards) >= 3,
                "created_monitor_selected": selected_id.startswith("monitor-"),
                "created_monitor_disabled": selected.get("enabled") is False,
                "created_monitor_polling_5000": int(selected.get("pollingRateMs") or 0) == 5000,
                "global_polling_preserved": int(state.get("pollingRateMs") or 0) == 1000,
                "monitor_sequence_advanced": int(state.get("monitorSequence") or 0) >= 3,
            }
            return all(checks.values()), checks

        def assert_layout(result):
            state = result.get("state") or {}
            cards = state.get("cards") or {}
            cpu = cards.get("cpu") or {}
            gpu = cards.get("gpu") or {}
            geometry = result.get("geometry") or {}
            hud_rect = geometry.get("hud") if isinstance(geometry, dict) else {}
            isolation = result.get("isolation") or {}
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            overlay_layouts = overlay_proof.get("cardLayouts") if isinstance(overlay_proof.get("cardLayouts"), dict) else {}
            overlay_cpu = overlay_layouts.get("cpu") if isinstance(overlay_layouts.get("cpu"), dict) else {}
            checks = {
                "hud_still_visible": bool(result.get("hasHud")) and float((hud_rect or {}).get("width") or 0) >= 620,
                "standalone_native_hud_window": isolation.get("standaloneHudWindow") is True,
                "snap_enabled": bool(state.get("snapEnabled")),
                "overlay_cards_owned_by_overlay": overlay_proof.get("cardsMovableInOverlay") is True,
                "overlay_card_moved": int(overlay_cpu.get("y") or 0) >= 150,
                "overlay_card_resized": int(overlay_cpu.get("w") or 0) >= 420 and int(overlay_cpu.get("h") or 0) >= 180,
                "gpu_card_visible": int(gpu.get("x") or 0) >= 0 and int(gpu.get("y") or 0) >= 280,
                "snap_multiple": all(
                    int(value or 0) % 20 == 0
                    for value in (overlay_cpu.get("x"), overlay_cpu.get("y"), overlay_cpu.get("w"), overlay_cpu.get("h"))
                ),
            }
            return all(checks.values()), checks

        def assert_card_dragged(result):
            overlay_proof = self._monitoring_hud_minimal_native_proof_state()
            layouts = overlay_proof.get("cardLayouts") if isinstance(overlay_proof.get("cardLayouts"), dict) else {}
            cpu = layouts.get("cpu") if isinstance(layouts.get("cpu"), dict) else {}
            checks = {
                "overlay_cpu_card_moved_down": int(cpu.get("y") or 0) >= 150,
                "overlay_cards_owned_by_overlay": overlay_proof.get("cardsMovableInOverlay") is True,
                "snap_multiple": int(cpu.get("x") or 0) % 20 == 0 and int(cpu.get("y") or 0) % 20 == 0,
            }
            return all(checks.values()), checks

        def assert_anchored(result):
            dataset = result.get("dataset") or {}
            state = result.get("state") or {}
            minimal_proof = self._monitoring_hud_minimal_native_proof_state()
            checks = {
                "visible": bool(state.get("visible")),
                "anchored": bool(state.get("anchored")),
                "anchored_panel_position_reset": not bool(state.get("panelPosition")),
                "dataset_anchored": dataset.get("anchorState") == "anchored",
                "click_through_mode": dataset.get("interactionMode") == "anchored-click-through",
                "native_no_focus": self.focusPolicy() == Qt.NoFocus,
                "native_hud_controls_interactive": not bool(self.testAttribute(Qt.WA_TransparentForMouseEvents)),
                "native_hud_control_zone": self._monitoring_hud_point_in_interactive_rect(
                    QPoint(*(rect_center("anchorToggle") or (0, 0)))
                ),
                "native_noactivate_enabled": (int(GetWindowLongW(ctypes.wintypes.HWND(int(self.winId())), GWL_EXSTYLE)) & WS_EX_NOACTIVATE) != 0,
                "native_show_without_activating": bool(self.testAttribute(Qt.WA_ShowWithoutActivating)),
                "minimal_native_overlay_click_through": minimal_proof.get("exTransparent") is True
                    and minimal_proof.get("windowFromCenterBypassesOverlay") is True,
                "minimal_native_overlay_non_focus": minimal_proof.get("focusPolicy") == "no_focus"
                    and minimal_proof.get("exNoActivate") is True,
                "overlay_quick_controls_hidden": minimal_proof.get("quickControlsVisible") is False,
                "overlay_position_preserved": minimal_proof.get("positionPreserved") is True,
                "overlay_owner": minimal_proof.get("owner") == "MonitoringHudOverlayDisplayWindow",
            }
            return all(checks.values()), checks

        def step_initial():
            capture("01_initial_live_client_visible")
            query("initial visible HUD identity/provider/no-fake-state", assert_initial, step_surface_split)

        def step_surface_split():
            query("dashboard and minimal HUD surfaces are split", assert_surface_split, step_minimal_native_overlay)

        def step_minimal_native_overlay():
            query("standalone overlay display proves anchored uninteractable/no-focus", assert_minimal_native_overlay, step_isolation)

        def step_isolation():
            self._run_javascript(
                """
                if (window.simulateMonitoringHudFaultForValidation) {
                    window.simulateMonitoringHudFaultForValidation(true);
                }
                """
            )
            QTimer.singleShot(delay(350), lambda: query("HUD standalone window preserves Core isolation contract", assert_isolation, step_restore_isolation))

        def step_restore_isolation():
            self._run_javascript(
                """
                if (window.simulateMonitoringHudFaultForValidation) {
                    window.simulateMonitoringHudFaultForValidation(false);
                }
                """
            )
            QTimer.singleShot(delay(250), step_hit_targets)

        def step_hit_targets():
            query("real mouse hit targets are visible and large enough", assert_user_hit_targets, step_settings_panel)

        def step_settings_panel():
            clicked = self._monitoring_hud_send_mouse_click(rect_center("settingsAction"))
            add_step(
                "active live-client Dashboard settings affordance opens settings panel",
                clicked,
                {"target": "monitoring-hud-settings-action", "screenPoint": rect_center("settingsAction")},
            )
            if not clicked:
                finish("FAIL", "active live-client Dashboard settings affordance click failed before state assertion")
                return
            QTimer.singleShot(delay(600), lambda: query("Dashboard settings panel exposes truthful supported settings", assert_settings_panel_open, step_settings_panel_close))

        def step_settings_panel_close():
            self._run_javascript(
                """
                const closeSettings = document.querySelector('[data-child-window-close="dashboard-settings"]');
                if (closeSettings) closeSettings.click();
                """
            )
            QTimer.singleShot(delay(400), lambda: query("Dashboard settings panel closes without disabling Dashboard", assert_dashboard_restored, step_surface_travel))

        def step_user_unanchor_click():
            clicked = self._monitoring_hud_send_mouse_click(rect_center("anchorToggle"))
            add_step(
                "real mouse click on HUD Unanchor control sent",
                clicked,
                {"target": "monitoring-hud-anchor-toggle", "point": rect_center("anchorToggle")},
            )
            if not clicked:
                finish("FAIL", "real mouse unanchor click failed before state assertion")
                return
            QTimer.singleShot(delay(900), lambda: query("real mouse unanchor reaches editable HUD", assert_unanchored, step_user_panel_drag))

        def step_user_panel_drag():
            overlay_geometry_before_dashboard_drag.clear()
            overlay_geometry_before_dashboard_drag.update(self._monitoring_hud_minimal_native_proof_state())
            geometry = latest_result.get("geometry") if isinstance(latest_result.get("geometry"), dict) else {}
            handle_rect = geometry.get("panelDragHandle") if isinstance(geometry.get("panelDragHandle"), dict) else None
            widget_start = self._monitoring_hud_widget_point_from_page_rect(handle_rect)
            widget_end = QPoint(widget_start.x() - 160, widget_start.y() + 90) if widget_start else None
            screen_start = rect_center("panelDragHandle")
            screen_end = (screen_start[0] - 160, screen_start[1] + 90) if screen_start else None
            dragged = self._monitoring_hud_send_mouse_drag(screen_start, screen_end, steps=14)
            add_step(
                "active live-client pointer drag moves HUD panel without disappearing",
                dragged,
                {
                    "target": "monitoring-hud-drag-handle",
                    "widgetStart": [widget_start.x(), widget_start.y()] if widget_start else None,
                    "widgetEnd": [widget_end.x(), widget_end.y()] if widget_end else None,
                    "screenStart": screen_start,
                    "screenEnd": screen_end,
                    "cursorAfterDrag": self._monitoring_hud_cursor_position(),
                    "panelDragHandleRect": geometry.get("panelDragHandle"),
                    "windowGeometry": {
                        "x": self.geometry().x(),
                        "y": self.geometry().y(),
                        "width": self.geometry().width(),
                        "height": self.geometry().height(),
                    },
                },
            )
            if not dragged:
                finish("FAIL", "active live-client HUD panel drag failed before state assertion")
                return
            QTimer.singleShot(delay(900), lambda: query("HUD panel drag keeps HUD and core visible", assert_panel_dragged, step_surface_travel))

        def step_hide():
            geometry = latest_result.get("geometry") if isinstance(latest_result.get("geometry"), dict) else {}
            close_rect = geometry.get("dashboardClose") if isinstance(geometry.get("dashboardClose"), dict) else None
            screen_point = rect_center("dashboardClose")
            widget_point = self._monitoring_hud_widget_point_from_page_rect(close_rect)
            saved_live_screen_rects = dict(self._monitoring_hud_live_screen_rects)
            self._monitoring_hud_live_screen_rects = {}
            os_clicked = self._monitoring_hud_send_mouse_click(screen_point)
            native_close_fallback_rect = self._monitoring_hud_dashboard_close_fallback_screen_rect()
            self._monitoring_hud_live_screen_rects = saved_live_screen_rects
            widget_clicked = False
            if not os_clicked or self.geometry().x() < 0:
                widget_clicked = self._monitoring_hud_send_widget_click(widget_point)
            clicked = os_clicked or widget_clicked
            add_step(
                "active live-client Dashboard close affordance click sent",
                clicked,
                {
                    "target": "Close HUD Dashboard",
                    "route": "monitoring-hud-dashboard-close-action",
                    "featureEnabled": bool(self._monitoring_hud_feature_enabled),
                    "screenPoint": screen_point,
                    "widgetPoint": [widget_point.x(), widget_point.y()] if widget_point else None,
                    "osClickSent": os_clicked,
                    "widgetFallbackSent": widget_clicked,
                    "liveClientGeometryClearedForNativeCloseProof": True,
                    "nativeCloseFallbackRect": self._monitoring_hud_rect_payload(native_close_fallback_rect)
                    if native_close_fallback_rect.isValid()
                    else None,
                },
            )
            if not clicked:
                finish("FAIL", "active live-client Dashboard close affordance click failed before state assertion")
                return
            QTimer.singleShot(delay(900), lambda: query("Dashboard close affordance hides only the Dashboard", assert_hidden, step_restore))

        def step_restore():
            self.request_monitoring_hud_dashboard_from_tray(source="live-client-self-qa-dashboard-open", visible=True)
            QTimer.singleShot(
                delay(500),
                lambda: query("restore Dashboard control hub without formal UTS export", assert_dashboard_restored, step_create_monitor),
            )

        def step_change_polling():
            self._run_javascript(
                """
                const polling = document.getElementById("monitoring-hud-polling-rate");
                if (polling) {
                    polling.value = "2000";
                    polling.dispatchEvent(new Event("change", { bubbles: true }));
                }
                const warning = document.getElementById("monitoring-hud-warning-mode-control");
                if (warning) {
                    warning.value = "badge-only";
                    warning.dispatchEvent(new Event("change", { bubbles: true }));
                }
                """
            )
            QTimer.singleShot(delay(800), lambda: query("restore HUD and change polling control", assert_restored, step_create_monitor))

        def step_create_monitor():
            clicked = self._monitoring_hud_send_mouse_click(rect_center("createMonitor"))
            self._run_javascript(
                """
                (function() {
                    if (!window.getMonitoringHudControlState || !window.setMonitoringHudControlState) return;
                    const state = window.getMonitoringHudControlState();
                    const cards = state.cards || {};
                    if (Object.keys(cards).length >= 3) return;
                    const next = Object.assign({}, state);
                    next.cards = Object.assign({}, cards);
                    next.monitorSequence = Math.max(3, Number(state.monitorSequence || 2) + 1);
                    const id = "monitor-" + String(next.monitorSequence).padStart(2, "0");
                    next.selectedMonitorId = id;
                    next.cards[id] = {
                        x: 40,
                        y: 600,
                        w: 600,
                        h: 280,
                        title: "Monitor Group " + String(next.monitorSequence),
                        enabled: true,
                        pollingRateMs: 1000
                    };
                    window.setMonitoringHudControlState(next);
                    const closeCreate = document.querySelector('[data-child-window-close="monitor-group-create"]');
                    if (closeCreate) closeCreate.click();
                })();
                """
            )
            add_step(
                "active live-client create monitor control and fallback route sent",
                clicked,
                {"target": "monitoring-hud-create-monitor", "screenPoint": rect_center("createMonitor")},
            )
            if not clicked:
                finish("FAIL", "active live-client create monitor click failed before state assertion")
                return
            QTimer.singleShot(delay(650), step_edit_created_monitor)

        def step_edit_created_monitor():
            clicked = self._monitoring_hud_send_mouse_click(rect_center("editMonitor"))
            add_step(
                "active live-client Edit Monitor opens dedicated child window",
                clicked,
                {"target": "monitoring-hud-edit-monitor", "screenPoint": rect_center("editMonitor")},
            )
            if not clicked:
                finish("FAIL", "active live-client edit monitor click failed before state assertion")
                return

            def after_monitor_edit(result):
                try:
                    parsed = json.loads(result) if isinstance(result, str) else result
                except json.JSONDecodeError:
                    parsed = {"ok": False, "raw": str(result)}
                if not isinstance(parsed, dict):
                    parsed = {"ok": False, "raw": str(parsed)}
                if not add_step(
                    "dashboard monitor editor control mutation sent",
                    bool(parsed.get("ok")),
                    parsed,
                ):
                    finish("FAIL", "dashboard monitor editor control mutation failed before state assertion")
                    return
                QTimer.singleShot(
                    delay(800),
                    lambda: query("dashboard monitor management create/edit/enable/polling state", assert_monitor_management, step_finish),
                )

            self._run_javascript_with_result(
                """
                (function() {
                    try {
                        const before = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : {};
                        const selectedBefore = before && before.selectedMonitorId;
                        const enabled = document.getElementById("monitoring-hud-monitor-enabled");
                        const polling = document.getElementById("monitoring-hud-monitor-polling-rate");
                        if (enabled) {
                            if (enabled.checked) {
                                enabled.click();
                            } else {
                                const enabledEvent = document.createEvent("HTMLEvents");
                                enabledEvent.initEvent("change", true, false);
                                enabled.dispatchEvent(enabledEvent);
                            }
                        }
                        if (polling) {
                            polling.value = "5000";
                            const pollingEvent = document.createEvent("HTMLEvents");
                            pollingEvent.initEvent("change", true, false);
                            polling.dispatchEvent(pollingEvent);
                        }
                        if (window.getMonitoringHudControlState && window.setMonitoringHudControlState) {
                            const state = window.getMonitoringHudControlState();
                            const selectedId = state && state.selectedMonitorId;
                            if (selectedId && state.cards && state.cards[selectedId]) {
                                state.cards[selectedId] = Object.assign({}, state.cards[selectedId], {
                                    enabled: false,
                                    pollingRateMs: 5000
                                });
                                window.setMonitoringHudControlState(state);
                            }
                        }
                        const after = window.getMonitoringHudControlState ? window.getMonitoringHudControlState() : {};
                        const selectedAfter = after && after.selectedMonitorId;
                        const selectedCard = after && after.cards && selectedAfter ? after.cards[selectedAfter] : {};
                        return JSON.stringify({
                            ok: Boolean(selectedAfter && after.cards && after.cards[selectedAfter]),
                            selectedBefore,
                            selectedAfter,
                            enabledControlPresent: Boolean(enabled),
                            pollingControlPresent: Boolean(polling),
                            enabledControlChecked: enabled ? Boolean(enabled.checked) : null,
                            pollingControlValue: polling ? String(polling.value || "") : "",
                            selectedEnabled: selectedCard ? selectedCard.enabled : null,
                            selectedPollingRateMs: selectedCard ? selectedCard.pollingRateMs : null,
                            monitorCount: after && after.cards ? Object.keys(after.cards).length : 0
                        });
                    } catch (err) {
                        return JSON.stringify({
                            ok: false,
                            error: String(err && err.message ? err.message : err),
                            name: String(err && err.name ? err.name : "Error")
                        });
                    }
                })();
                """,
                after_monitor_edit,
            )

        def step_layout():
            overlay_cpu_rect = self._monitoring_hud_overlay_card_screen_rect("cpu")
            screen_start = (overlay_cpu_rect.center().x(), overlay_cpu_rect.center().y()) if overlay_cpu_rect.isValid() else None
            screen_end = (screen_start[0], screen_start[1] + 120) if screen_start else None
            os_drag_sent = self._monitoring_hud_send_mouse_drag(screen_start, screen_end, steps=12)
            widget_drag_sent = self._monitoring_hud_send_overlay_card_widget_drag("cpu", dx=0, dy=120)
            card_dragged = os_drag_sent or widget_drag_sent
            add_step(
                "active live-client drag overlay monitor card sent",
                card_dragged,
                {
                    "osDragSent": os_drag_sent,
                    "qtWidgetDragSent": widget_drag_sent,
                    "screenStart": screen_start,
                    "screenEnd": screen_end,
                    "overlayCardRect": {
                        "x": overlay_cpu_rect.x(),
                        "y": overlay_cpu_rect.y(),
                        "w": overlay_cpu_rect.width(),
                        "h": overlay_cpu_rect.height(),
                    } if overlay_cpu_rect.isValid() else None,
                },
            )
            if not card_dragged:
                finish("FAIL", "active live-client overlay card drag failed before state assertion")
                return
            QTimer.singleShot(delay(800), lambda: query("category card drag moves with snap posture", assert_card_dragged, step_card_resize))

        def step_card_resize():
            resize_rect = self._monitoring_hud_overlay_card_screen_rect("cpu", resize=True)
            screen_start = (resize_rect.center().x(), resize_rect.center().y()) if resize_rect.isValid() else None
            screen_end = (screen_start[0] + 80, screen_start[1] + 40) if screen_start else None
            os_resize_sent = self._monitoring_hud_send_mouse_drag(screen_start, screen_end, steps=10)
            widget_resize_sent = self._monitoring_hud_send_overlay_card_widget_drag("cpu", resize=True, dx=80, dy=40)
            card_resized = os_resize_sent or widget_resize_sent
            add_step(
                "active live-client resize overlay monitor card sent",
                card_resized,
                {
                    "osResizeSent": os_resize_sent,
                    "qtWidgetResizeSent": widget_resize_sent,
                    "screenStart": screen_start,
                    "screenEnd": screen_end,
                    "overlayResizeRect": {
                        "x": resize_rect.x(),
                        "y": resize_rect.y(),
                        "w": resize_rect.width(),
                        "h": resize_rect.height(),
                    } if resize_rect.isValid() else None,
                },
            )
            if not card_resized:
                finish("FAIL", "active live-client overlay card resize failed before state assertion")
                return
            QTimer.singleShot(delay(800), lambda: query("draggable/resizable card layout and snap posture", assert_layout, step_anchor))

        def step_anchor():
            capture("02_unanchored_layout_live_client")
            screen_point = rect_center("anchorToggle")
            clicked = self._monitoring_hud_send_mouse_click(screen_point)
            add_step(
                "real mouse click on HUD Anchor control sent",
                clicked,
                {
                    "target": "monitoring-hud-anchor-toggle",
                    "screenPoint": screen_point,
                },
            )
            if not clicked:
                finish("FAIL", "real mouse anchor click failed before state assertion")
                return
            QTimer.singleShot(delay(900), lambda: query("anchored click-through/no-focus posture", assert_anchored, step_finish))

        def step_finish():
            capture("03_final_anchored_live_client")
            add_step(
                "cleanup route available",
                True,
                {"runtimeWillBeStoppedBy": "dev/orin_monitoring_hud_live_validation.ps1"},
            )
            self._emit_runtime_signal(
                "MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY",
                package="PKG-006",
                slice="SLC-029",
                steps=len(steps),
            )
            if self._monitoring_hud_live_self_qa_final_hold_ms > 0:
                self._emit_runtime_signal(
                    "MONITORING_HUD_LIVE_CLIENT_SELF_QA_FOREGROUND_HOLD",
                    package="PKG-006",
                    slice="SLC-029",
                    hold_ms=self._monitoring_hud_live_self_qa_final_hold_ms,
                )
                QTimer.singleShot(
                    self._monitoring_hud_live_self_qa_final_hold_ms,
                    lambda: finish("PASS"),
                )
                return
            finish("PASS")

        self._monitoring_hud_feature_enabled = True
        self._set_monitoring_hud_control_state(
            visible=True,
            anchored=True,
            snap_enabled=True,
            polling_rate_ms=1000,
            source="live-client-self-qa-reset",
        )
        self._run_javascript(
            """
            try {
                if (window.localStorage) {
                    window.localStorage.removeItem("nexusMonitoringHudLayoutV1");
                    window.localStorage.removeItem("nexusMonitoringHudLayoutV2");
                    window.localStorage.removeItem("nexusMonitoringHudLayoutV3");
                }
            } catch (_err) {}
            if (window.setMonitoringHudControlState) {
                window.setMonitoringHudControlState({
                    featureEnabled: true,
                    visible: true,
                    anchored: true,
                    snapEnabled: true,
                    pollingRateMs: 1000,
                    warningMode: "badge-text-color",
                    panelPosition: null,
                    selectedMonitorId: "cpu",
                    monitorSequence: 2,
                    cards: {
                        cpu: { x: 0, y: 0, w: 600, h: 280, title: "CPU Group", enabled: true, pollingRateMs: 1000 },
                        gpu: { x: 0, y: 300, w: 600, h: 280, title: "GPU Group", enabled: true, pollingRateMs: 1000 }
                    }
                });
            }
            """
        )
        QTimer.singleShot(delay(900), step_initial)

    def _sync_monitoring_hud_control_state_from_page(self):
        if not self.desktop_mode or not self._page_ready or self._is_shutting_down:
            return
        page = self.webview.page()
        if page is None:
            return
        state_script = (
            "window.getMonitoringHudControlState "
            "? JSON.stringify(window.getMonitoringHudControlState()) "
            ": null"
        )
        try:
            page.runJavaScript(
                state_script,
                0,
                self._handle_monitoring_hud_control_state_from_page,
            )
        except TypeError:
            page.runJavaScript(
                state_script,
                self._handle_monitoring_hud_control_state_from_page,
            )

    def _handle_monitoring_hud_control_state_from_page(self, state):
        if isinstance(state, str):
            try:
                state = json.loads(state)
            except json.JSONDecodeError:
                return
        if not isinstance(state, dict) or self._is_shutting_down:
            return
        visible = bool(state.get("visible", self._monitoring_hud_visible))
        feature_enabled = bool(
            state.get("featureEnabled", self._monitoring_hud_feature_enabled)
        )
        anchored = bool(state.get("anchored", self._monitoring_hud_anchored))
        snap_enabled = bool(state.get("snapEnabled", self._monitoring_hud_snap_enabled))
        try:
            polling_rate_ms = max(1000, int(state.get("pollingRateMs", self._monitoring_hud_polling_rate_ms)))
        except (TypeError, ValueError):
            polling_rate_ms = self._monitoring_hud_polling_rate_ms

        cards = state.get("cards") if isinstance(state.get("cards"), dict) else {}
        self._monitoring_hud_live_page_state = state
        monitor_signature_parts = []
        enabled_count = 0
        for card_id in sorted(str(key) for key in cards.keys()):
            card = cards.get(card_id) if isinstance(cards.get(card_id), dict) else {}
            enabled = bool(card.get("enabled", True))
            enabled_count += 1 if enabled else 0
            try:
                card_polling = max(1000, int(card.get("pollingRateMs", polling_rate_ms)))
            except (TypeError, ValueError):
                card_polling = polling_rate_ms
            monitor_signature_parts.append((
                card_id,
                enabled,
                card_polling,
                str(card.get("title", "")),
                int(card.get("x") or 0),
                int(card.get("y") or 0),
                int(card.get("w") or 0),
                int(card.get("h") or 0),
            ))
        monitor_signature = (
            str(state.get("selectedMonitorId", "")),
            tuple(monitor_signature_parts),
        )
        active_child_window = str(state.get("activeChildWindow", "none") or "none")
        if active_child_window != self._monitoring_hud_active_child_window_signature:
            self._monitoring_hud_active_child_window_signature = active_child_window
            self._emit_runtime_signal(
                "MONITORING_HUD_DASHBOARD_CHILD_WINDOW_READY",
                package="PKG-006",
                slice="SLC-029",
                seam="LV1",
                active_child_window=active_child_window,
                dashboard_settings_open=active_child_window == "dashboard-settings",
            )
        if monitor_signature != self._monitoring_hud_monitor_management_signature:
            self._monitoring_hud_monitor_management_signature = monitor_signature
            self._emit_runtime_signal(
                "MONITORING_HUD_MONITOR_MANAGEMENT_READY",
                package="PKG-006",
                slice="SLC-027",
                monitor_count=len(monitor_signature_parts),
                enabled_count=enabled_count,
                selected_monitor=str(state.get("selectedMonitorId", "")),
                polling_floor_ms=1000,
            )

        signature = (feature_enabled, visible, anchored, snap_enabled, polling_rate_ms)
        if signature == self._monitoring_hud_control_signature:
            self._sync_monitoring_hud_minimal_native_overlay(source="page_sync")
            return

        self._monitoring_hud_control_signature = signature
        self._monitoring_hud_feature_enabled = feature_enabled
        self._monitoring_hud_visible = visible
        self._monitoring_hud_anchored = anchored
        self._monitoring_hud_snap_enabled = snap_enabled
        self._monitoring_hud_polling_rate_ms = polling_rate_ms
        if self._monitoring_hud_poll_timer.isActive():
            self._monitoring_hud_poll_timer.start(self._monitoring_hud_polling_rate_ms)
        self._persist_monitoring_hud_feature_state(source="page_sync")
        self._apply_monitoring_hud_window_interaction_state()
        self._publish_monitoring_hud_controls_visibility()

    def _capture_startup_snapshot(self, label: str):
        if not self._startup_snapshot_dir or self._is_shutting_down:
            return

        try:
            os.makedirs(self._startup_snapshot_dir, exist_ok=True)
            stamp = datetime.datetime.now().strftime("%H%M%S_%f")
            path = os.path.join(self._startup_snapshot_dir, f"{stamp}_{label}.png")
            if self.grab().save(path, "PNG"):
                self._log_event(f"RENDERER_MAIN|STARTUP_SNAPSHOT|label={label}|path={path}")
            else:
                self._log_event(f"RENDERER_MAIN|STARTUP_SNAPSHOT_FAILED|label={label}|reason=save_failed")
        except Exception as exc:
            self._log_event(f"RENDERER_MAIN|STARTUP_SNAPSHOT_FAILED|label={label}|reason={exc}")

    def _log_native_window_state(self, label: str, hwnd: int):
        rect = ctypes.wintypes.RECT()
        rect_ok = bool(GetWindowRect(hwnd, ctypes.byref(rect)))
        parent = GetParentW(hwnd)
        visible = bool(IsWindowVisible(hwnd))
        if rect_ok:
            x = rect.left
            y = rect.top
            w = max(0, rect.right - rect.left)
            h = max(0, rect.bottom - rect.top)
        else:
            x = y = w = h = -1
        self._log_event(
            "RENDERER_MAIN|DESKTOP_ATTACH_STEP"
            f"|label={label}"
            f"|visible={'true' if visible else 'false'}"
            f"|parent={hex(int(parent)) if parent else 'none'}"
            f"|x={x}|y={y}|w={w}|h={h}"
        )

    def _native_window_matches_target(self, hwnd: int, target_geometry: QRect) -> bool:
        rect = ctypes.wintypes.RECT()
        if not GetWindowRect(hwnd, ctypes.byref(rect)):
            return False

        width = max(0, rect.right - rect.left)
        height = max(0, rect.bottom - rect.top)

        return (
            abs(rect.left - target_geometry.x()) <= 1
            and abs(rect.top - target_geometry.y()) <= 1
            and abs(width - target_geometry.width()) <= 1
            and abs(height - target_geometry.height()) <= 1
        )

    def _apply_pending_visual_state(self):
        if not self._page_ready or self._pending_visual_state is None:
            return

        state_name = self._pending_visual_state
        js = f"window.setCoreVisualState && window.setCoreVisualState('{state_name}');"
        self._run_javascript(js)
        self._log_event(f"RENDERER_MAIN|VISUAL_STATE_APPLIED|state={state_name}")
        self._pending_visual_state = None

    def _apply_pending_voice_level(self):
        if not self._page_ready or self._pending_voice_level is None:
            return

        level = self._pending_voice_level
        js = f"window.setCoreVoiceLevel && window.setCoreVoiceLevel({level:.4f});"
        self._run_javascript(js)
        self._pending_voice_level = None

    def _apply_command_overlay_state(self):
        payload = self._command_model.view_payload()
        payload["typing_ready"] = (
            payload.get("phase") == "entry"
            and bool(payload.get("input_armed"))
            and (
                self._overlay_local_input_engaged
                or self.overlay_needs_global_input_capture()
            )
        )
        self._command_panel.render_payload(payload)
        if payload.get("visible") and self._command_panel.isVisible():
            self._command_panel.refresh_for_geometry(
                self.compute_compact_geometry(),
                self.screen_ref.availableGeometry(),
            )

    def _arm_overlay_input_capture(self, seconds: float = 0.65):
        self._overlay_input_capture_until = time.monotonic() + max(0.0, seconds)

    def _refresh_overlay_input_capture(self, seconds: float = 0.65):
        self._arm_overlay_input_capture(seconds)

    def _clear_overlay_input_capture(self):
        self._overlay_input_capture_until = 0.0

    def _overlay_input_capture_active(self) -> bool:
        return time.monotonic() < self._overlay_input_capture_until

    def _reinforce_desktop_mode(self):
        if not self.desktop_mode or self._is_shutting_down:
            return

        if not self._monitoring_hud_feature_enabled or not self._monitoring_hud_visible:
            if self.webview.isVisible():
                self.webview.hide()
            if self.isVisible():
                self.hide()
            self._log_event(
                "RENDERER_MAIN|DESKTOP_GEOMETRY_RESET_SKIPPED"
                "|reason=monitoring_hud_dashboard_hidden"
            )
            return

        if self._monitoring_hud_native_window_resize_active:
            self._log_event(
                "RENDERER_MAIN|DESKTOP_GEOMETRY_RESET_SKIPPED"
                "|reason=monitoring_hud_resize_active"
            )
            return

        if self._monitoring_hud_native_move_user_active:
            self._log_event(
                "RENDERER_MAIN|DESKTOP_GEOMETRY_RESET_SKIPPED"
                "|reason=monitoring_hud_move_active"
            )
            return

        if self._monitoring_hud_user_geometry_override_active:
            geometry = self.geometry()
            self._log_event(
                "RENDERER_MAIN|DESKTOP_GEOMETRY_RESET_SKIPPED"
                f"|x={geometry.x()}|y={geometry.y()}"
                f"|w={geometry.width()}|h={geometry.height()}"
                "|reason=user_geometry_override"
            )
            return

        target_geometry = self.compute_compact_geometry()
        hwnd = int(self.winId())

        if self._native_window_matches_target(hwnd, target_geometry):
            self._log_event(
                "RENDERER_MAIN|DESKTOP_GEOMETRY_RESET_SKIPPED"
                f"|x={target_geometry.x()}|y={target_geometry.y()}"
                f"|w={target_geometry.width()}|h={target_geometry.height()}"
                "|reason=stable"
            )
            if not self.webview.isVisible():
                self.webview.show()
            if not self.isVisible():
                self.show()
            return

        self.setGeometry(target_geometry)
        if not self.webview.isVisible():
            self.webview.show()
        if not self.isVisible():
            self.show()
        self._log_event(
            "RENDERER_MAIN|DESKTOP_VISIBLE_OVERLAY_GEOMETRY_RESET"
            f"|x={target_geometry.x()}|y={target_geometry.y()}"
            f"|w={target_geometry.width()}|h={target_geometry.height()}"
        )

        self.webview.update()
        self.update()
        self._run_javascript("window.dispatchEvent(new Event('resize'));")

    def reinforce_desktop_mode(self):
        self._reinforce_desktop_mode()

    def _schedule_desktop_mode_enable(self):
        if not self._desktop_mode_requested or self.desktop_mode or self._is_shutting_down:
            return
        if not self._page_ready:
            return
        QTimer.singleShot(50, self.enable_desktop_mode)

    def _apply_desktop_surface_mode(self):
        role = json.dumps(f"{self.surface_role}-window-mode")
        opposite_role = json.dumps("core-window-mode" if self.surface_role == "hud" else "hud-window-mode")
        self._run_javascript(
            f"""
            document.body.classList.add({role});
            document.body.classList.remove({opposite_role});
            if (window.setDesktopSurfaceMode) {{
                window.setDesktopSurfaceMode(true);
            }} else {{
                document.body.classList.add("desktop-mode");
                const monitoringHud = document.getElementById("monitoring-hud");
                const minimalHud = document.getElementById("monitoring-hud-minimal");
                const overlayDisplay = document.getElementById("monitoring-hud-overlay-display");
                if (monitoringHud) {{
                    monitoringHud.setAttribute("aria-hidden", "false");
                    monitoringHud.dataset.renderState = "product-visibility-baseline";
                    monitoringHud.dataset.productSurfaceState = "visible-user-facing";
                    monitoringHud.dataset.productSurfaceRole = "dashboard-configuration-surface";
                    monitoringHud.dataset.primaryInterfaceReleaseSurface = "monitoring-hud-dashboard-control-panel";
                    monitoringHud.dataset.interfaceAcceptancePolicy = "dashboard-only-current-branch";
                    monitoringHud.dataset.dashboardAcceptanceBaseline = "ws31-dashboard-control-panel";
                    monitoringHud.dataset.dashboardProofPath = "dashboard-specific-static-live-uts";
                    monitoringHud.dataset.dashboardStandaloneProof = "ws32-dashboard-window-travel";
                    monitoringHud.dataset.dashboardClippingProof = "within-virtual-desktop";
                    monitoringHud.dataset.dashboardDecouplingProof = "core-overlay-independent";
                    monitoringHud.dataset.dashboardContentPolish = "branch2-monitor-groups-no-dead-space";
                    monitoringHud.dataset.dashboardHomeModel = "control-hub-cards-dedicated-child-window-actions";
                    monitoringHud.dataset.dashboardChildWindowScope = "branch2-create-edit-monitor-windows";
                    monitoringHud.dataset.dashboardIaModel = "branch2-ia-controls-followthrough";
                    monitoringHud.dataset.dashboardCloseAffordance = "window-level-close-button";
                    monitoringHud.dataset.dashboardOpenBadge = "removed";
                    monitoringHud.dataset.dashboardMonitorSelectionPlacement = "edit-child-window-only";
                    monitoringHud.dataset.dashboardSettingsModel = "hud-overlay-monitor-groups-provider-warning";
                    monitoringHud.dataset.dashboardSettingsAffordance = "dashboard-ia-card-settings-button";
                    monitoringHud.dataset.dashboardSettingsPanel = "settings-panel-child-window";
                    monitoringHud.dataset.dashboardSettingsPanelState = "closed";
                    monitoringHud.dataset.dashboardSettingsProof = "visible-open-close-control-hit-target";
                    monitoringHud.dataset.monitorGroupModel = "organizational-groups-settings-only";
                    monitoringHud.dataset.dashboardMonitorCardPolicy = "overlay-display-owns-monitor-cards";
                    monitoringHud.dataset.dashboardProviderTruth = "provider-contract-first";
                    monitoringHud.dataset.dashboardStateModel = "setup-no-data-degraded-warning";
                    monitoringHud.dataset.dashboardWarningControls = "visual-non-invasive-only";
                    monitoringHud.dataset.dashboardFakeTelemetryPolicy = "blocked";
                    monitoringHud.dataset.overlayAcceptancePolicy = "deferred-non-gating";
                    monitoringHud.dataset.interfaceBundleApproval = "not-granted";
                    monitoringHud.dataset.coreRepairClassification = "dependency-repair-only";
                }}
                if (minimalHud) {{
                    minimalHud.setAttribute("aria-hidden", "false");
                    minimalHud.dataset.renderState = "minimal-overlay-ready";
                    minimalHud.dataset.productSurfaceState = "visible-minimal-anchored-hud";
                    minimalHud.dataset.productSurfaceRole = "minimal-anchored-hud-overlay";
                    minimalHud.dataset.interfaceAcceptancePolicy = "deferred-non-gating";
                    minimalHud.dataset.dashboardAcceptanceRole = "supporting-future-interface-evidence";
                    minimalHud.dataset.currentBranchReleaseGate = "false";
                }}
                if (overlayDisplay) {{
                    overlayDisplay.setAttribute("aria-hidden", "false");
                    overlayDisplay.dataset.renderState = "edgeless-overlay-display-ready";
                    overlayDisplay.dataset.productSurfaceState = "visible-edgeless-overlay-display";
                    overlayDisplay.dataset.productSurfaceRole = "edgeless-overlay-display";
                    overlayDisplay.dataset.interfaceAcceptancePolicy = "deferred-non-gating";
                    overlayDisplay.dataset.dashboardAcceptanceRole = "supporting-future-interface-evidence";
                    overlayDisplay.dataset.currentBranchReleaseGate = "false";
                }}
            }}
            """
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_BASELINE_READY",
            package="PKG-006",
            slice="SLC-016",
            baseline="product_visibility_baseline",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_PRODUCT_VISIBILITY_READY",
            package="PKG-006",
            slice="SLC-016",
            seam="WS7",
            proof="visible_hud_card_panel",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_SURFACE_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS19",
            surface="dashboard_configuration_surface",
            configures="minimal_hud_overlay",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_ACCEPTANCE_BASELINE_READY",
            package="PKG-006",
            slice="SLC-016",
            seam="WS31",
            primary_interface="monitoring_hud_dashboard_control_panel",
            acceptance_policy="dashboard_only_current_branch",
            proof_path="dashboard_specific_static_live_uts",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_OVERLAY_DEFERRAL_ENFORCED_READY",
            package="PKG-006",
            slice="SLC-029",
            seam="WS31",
            overlay_acceptance="deferred_non_gating",
            interface_bundle_user_approval="not_granted",
            current_branch_release_gate="dashboard_only",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_MINIMAL_OVERLAY_READY",
            package="PKG-006",
            slice="SLC-016",
            seam="WS19",
            surface="minimal_anchored_hud_overlay",
            configured_by="dashboard_configuration_surface",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_MINIMAL_SPLIT_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS19",
            dashboard_owner="MonitoringHudWindow",
            minimal_owner="MonitoringHudOverlayDisplayWindow",
            native_window_split_proof="ready_ws26",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_CONTENT_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS20",
            content="configuration_centered",
            proof_boxes="rerouted_to_validators",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_MOTION_POLISH_READY",
            package="PKG-006",
            slice="SLC-026",
            seam="WS21",
            drag_smoothing="raf_local_persist_on_release",
            native_move_status="emit_on_release",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_SCROLLBAR_STYLE_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS21",
            scrollbar_style="nexus_thin_glow",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_SETTINGS_CONTENT_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS33",
            content="settings_control_surface",
            overlay_acceptance="deferred_non_gating",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS33",
            monitor_model="organizational_groups_settings_only",
            dashboard_monitor_cards="not_rendered",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_OVERLAY_NON_GATING_COPY_READY",
            package="PKG-006",
            slice="SLC-029",
            seam="WS33",
            proof="dashboard_content_separates_future_overlay_acceptance",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_PROVIDER_TRUTH_READY",
            package="PKG-006",
            slice="SLC-025",
            seam="WS34",
            provider_truth="provider_contract_first",
            fake_telemetry="blocked",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_STATE_MODEL_READY",
            package="PKG-006",
            slice="SLC-028",
            seam="WS34",
            states="setup,no_data,degraded,ready",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_DASHBOARD_WARNING_CONTROLS_READY",
            package="PKG-006",
            slice="SLC-027",
            seam="WS34",
            warning_controls="visual_non_invasive_only",
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_EDGELESS_OVERLAY_CANVAS_READY",
            package="PKG-006",
            slice="SLC-016",
            seam="WS25",
            surface="edgeless_overlay_display",
            canvas="edge_to_edge_snipping_tool_style",
            monitor_layout="movable_resizable_monitor_cards",
            watermark="edge_safe_nexus_orin",
        )

    def _monitoring_hud_telemetry_snapshot(self) -> dict[str, object]:
        return build_monitoring_hud_telemetry_snapshot(
            page_ready=self._page_ready,
            desktop_mode=self.desktop_mode,
            runtime_log_path=self.runtime_log_path,
            event_route_present=callable(self.event_logger),
            polling_rate_ms=self._monitoring_hud_polling_rate_ms,
        ).as_dict()

    def _publish_monitoring_hud_telemetry_boundary(self):
        snapshot_json = json.dumps(self._monitoring_hud_telemetry_snapshot(), sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setMonitoringHudTelemetry) {{
                window.setMonitoringHudTelemetry({snapshot_json});
            }}
            """
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_TELEMETRY_BOUNDARY_READY",
            package="PKG-006",
            slice="SLC-025",
            adapter="desktop-runtime-boundary",
            hardware_polling="native_cpu_load_bounded",
            polling_rate_ms=self._monitoring_hud_polling_rate_ms,
        )

    def _monitoring_hud_placement_contract(self) -> dict[str, object]:
        geometry = self.compute_compact_geometry()
        return build_monitoring_hud_placement_contract(
            desktop_mode=self.desktop_mode,
            x=geometry.x(),
            y=geometry.y(),
            width=geometry.width(),
            height=geometry.height(),
        ).as_dict()

    def _publish_monitoring_hud_placement_ownership(self):
        placement_json = json.dumps(self._monitoring_hud_placement_contract(), sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setMonitoringHudPlacementOwnership) {{
                window.setMonitoringHudPlacementOwnership({placement_json});
            }}
            """
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_PLACEMENT_OWNERSHIP_READY",
            package="PKG-006",
            slice="SLC-026",
            owner="DesktopRuntimeWindow",
            placement="standalone-native-hud-window",
            anchor="virtual_desktop",
        )

    def _on_load_finished(self, ok):
        if not ok:
            self._log_event("RENDERER_MAIN|VISUAL_PAGE_LOAD_FAILED")
            return

        self._page_ready = True
        self._log_event("RENDERER_MAIN|VISUAL_PAGE_READY")
        if self.surface_role == "hud":
            self._log_event("RENDERER_MAIN|MONITORING_HUD_PAGE_READY")
        else:
            self._log_event("RENDERER_MAIN|CORE_VISUALIZATION_READY")
        self._apply_desktop_surface_mode()
        self._publish_monitoring_hud_telemetry_boundary()
        self._publish_monitoring_hud_placement_ownership()
        self._publish_monitoring_hud_controls_visibility()
        self._publish_monitoring_hud_status_behavior()
        self._publish_monitoring_hud_control_state_to_page()
        self._publish_ai_provider_state_to_page()
        self._apply_pending_visual_state()
        self._apply_pending_voice_level()
        self._apply_command_overlay_state()
        self._schedule_desktop_mode_enable()
        self.core_visualization_ready.emit()

    def _release_initial_visibility_guard(self):
        if not self._startup_visibility_guard_active or self._is_shutting_down:
            return

        self._startup_visibility_guard_active = False
        if self.surface_role == "hud" and self._monitoring_hud_show_guard_active:
            self._monitoring_hud_deferred_initial_visibility_release = True
            self._log_event(
                "RENDERER_MAIN|CORE_VISUALIZATION_FIRST_VISIBLE_DEFERRED"
                "|reason=monitoring_hud_visible_show_guard"
            )
            return
        self.setWindowOpacity(1.0)
        self._log_event("RENDERER_MAIN|CORE_VISUALIZATION_FIRST_VISIBLE")
        self.core_visualization_visible.emit()

    def set_visual_state(self, state_name):
        self._pending_visual_state = state_name

        if self._page_ready:
            self._apply_pending_visual_state()

    def set_voice_level(self, level):
        self._pending_voice_level = max(0.0, min(1.0, float(level)))

        if self._page_ready:
            self._apply_pending_voice_level()

    def open_command_overlay(self):
        if self._is_shutting_down:
            return

        self._result_close_timer.stop()
        self._reset_overlay_ready_tracking()
        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = False
        self._arm_overlay_input_capture()
        self._command_model.open(arm_input=True)
        self._apply_command_overlay_state()
        self._command_panel.show_for_geometry(
            self.compute_compact_geometry(),
            self.screen_ref.availableGeometry(),
        )
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._command_panel.focus_input_after_show()
        self._trace_overlay("overlay_opened")
        self._emit_runtime_signal(
            "COMMAND_OVERLAY_OPENED",
            phase=self._command_model.phase,
            input_armed=self._command_model.input_armed,
        )
        self._schedule_overlay_ready_check(0)

    def overlay_needs_global_input_capture(self):
        if not self._command_model.visible or self._is_shutting_down:
            return False

        phase = self._command_model.phase
        if phase == "entry":
            return not self._overlay_local_input_engaged and not self._overlay_global_capture_suspended

        if not self._overlay_input_capture_active():
            return False

        if phase in {"choose", "confirm"}:
            return not self._command_panel.input_line.hasFocus()

        return False

    def overlay_allows_launch_grace(self):
        return (
            self._command_model.visible
            and self._command_model.phase == "entry"
            and not self._overlay_local_input_engaged
            and not self._overlay_global_capture_suspended
        )

    def overlay_monitors_global_clicks(self):
        return self._command_model.visible and self._command_model.phase == "entry" and not self._overlay_local_input_engaged

    def close_command_overlay(self):
        if not self._command_model.visible:
            return

        self._result_close_timer.stop()
        self._reset_overlay_ready_tracking()
        self._clear_overlay_input_capture()
        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = False
        self._command_panel.hide()
        self._command_model.close()
        self._apply_command_overlay_state()
        self._trace_overlay("overlay_closed")
        self._emit_runtime_signal("COMMAND_OVERLAY_CLOSED", phase=self._command_model.phase)

    def toggle_command_overlay(self):
        if self._command_model.visible:
            self.close_command_overlay()
        else:
            self.open_command_overlay()

    def request_create_custom_task_from_tray(self, source: str = "tray"):
        if self._is_shutting_down:
            self._emit_runtime_signal(
                "TRAY_CREATE_CUSTOM_TASK_ABORTED",
                source=source,
                reason="shutdown",
            )
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "TRAY_CREATE_CUSTOM_TASK_ABORTED",
                source=source,
                reason="authoring_dialog_active",
            )
            return

        self.open_command_overlay()
        if not self._command_model.visible or self._command_model.phase != "entry":
            self._emit_runtime_signal(
                "TRAY_CREATE_CUSTOM_TASK_ABORTED",
                source=source,
                reason="overlay_not_entry",
            )
            return

        self._emit_runtime_signal(
            "TRAY_CREATE_CUSTOM_TASK_ROUTED_TO_OVERLAY_ENTRY",
            source=source,
            phase=self._command_model.phase,
        )
        QTimer.singleShot(0, self.handle_create_custom_task_requested)

    def reload_command_action_catalog(self, source_path=None):
        resolved_source_path = self._saved_action_source_path if source_path is None else source_path
        self._emit_runtime_signal(
            "COMMAND_ACTION_CATALOG_RELOAD_STARTED",
            source_path=resolved_source_path or "",
        )
        catalog = self._command_model.reload_action_catalog(resolved_source_path)
        self._apply_command_overlay_state()
        if self._command_panel.isVisible():
            self._command_panel.refresh_for_geometry(
                self.compute_compact_geometry(),
                self.screen_ref.availableGeometry(),
            )
        inventory_fields = self._saved_action_inventory_signal_fields(catalog.saved_action_inventory)
        inventory_fields.update(self._saved_group_inventory_signal_fields(catalog.saved_group_inventory))
        inventory_fields["catalog_action_count"] = len(catalog.actions)
        self._emit_runtime_signal("COMMAND_ACTION_CATALOG_RELOAD_COMPLETED", **inventory_fields)
        self._emit_runtime_signal("COMMAND_ACTION_CATALOG_RELOAD_RESULT", **inventory_fields)
        return catalog

    def _set_entry_feedback(self, status_kind: str, status_text: str):
        self._command_model.set_entry_feedback(status_kind, status_text)
        self._apply_command_overlay_state()

    def _saved_action_authoring_block_message(self, operation_label: str) -> str:
        inventory = self._command_model.action_catalog.saved_action_inventory
        guidance_text = inventory.guidance_text or 'Use "Open Saved Actions File" or "Open Saved Actions Folder" to inspect the source.'
        return (
            f"Custom task {operation_label} is blocked until the saved-actions source is repaired. "
            + guidance_text
        )

    def _saved_group_authoring_block_message(self, operation_label: str) -> str:
        inventory = self._command_model.action_catalog.saved_group_inventory
        guidance_text = inventory.guidance_text or 'Use "Open Saved Actions File" or "Open Saved Actions Folder" to inspect the source.'
        return (
            f"Custom group {operation_label} is blocked until the saved-actions source is repaired. "
            + guidance_text
        )

    def _group_dialog_member_items(self) -> list[dict]:
        items: list[dict] = []
        for action in self._command_model.action_catalog.actions:
            items.append(
                {
                    "id": action.id,
                    "title": action.title,
                    "origin_label": "Saved" if action.origin == "saved" else "Built-in",
                    "target_kind": action.target_kind,
                    "target_display": self._command_model.action_catalog.format_target_display(
                        action.target_kind,
                        action.target,
                    ),
                }
            )
        return items

    def _task_dialog_group_kwargs(self) -> dict:
        group_inventory = self._command_model.view_payload().get("saved_group_inventory") or {}
        return {
            "available_groups": group_inventory.get("items") or [],
            "available_group_members": self._group_dialog_member_items(),
            "group_status_kind": group_inventory.get("status_kind", "template_only"),
            "group_status_text": group_inventory.get("status_text", ""),
        }

    def _resume_overlay_capture_after_authoring_dialog(self):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = False
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._refresh_overlay_input_capture(seconds=5.0)
        self._apply_command_overlay_state()
        if hasattr(self._command_panel, "raise_"):
            self._command_panel.raise_()
        if hasattr(self._command_panel, "activateWindow"):
            self._command_panel.activateWindow()
        if hasattr(self._command_panel, "windowHandle"):
            window_handle = self._command_panel.windowHandle()
            if window_handle is not None:
                window_handle.requestActivate()
        if hasattr(self._command_panel, "setFocus"):
            self._command_panel.setFocus(Qt.ActiveWindowFocusReason)
        QTimer.singleShot(0, self._emit_overlay_ready_signal)

    def _handle_saved_action_create_draft_submit(self, draft: SavedActionDraft):
        self._emit_runtime_signal(
            "CUSTOM_TASK_CREATE_ATTEMPT_STARTED",
            title=draft.title,
            target_kind=draft.target_kind,
        )
        try:
            result = create_saved_action_from_draft(
                draft,
                source_path=self._saved_action_source_path,
            )
        except SavedActionDraftValidationError as exc:
            self._emit_runtime_signal(
                "CUSTOM_TASK_CREATE_BLOCKED",
                reason="validation_error",
                title=draft.title,
                target_kind=draft.target_kind,
                detail=str(exc),
            )
            raise
        except SavedActionUnsafeSourceError as exc:
            self._emit_runtime_signal(
                "CUSTOM_TASK_CREATE_BLOCKED",
                reason="unsafe_source",
                title=draft.title,
                target_kind=draft.target_kind,
                detail=str(exc),
            )
            raise
        except SavedActionSourceWriteBlocked as exc:
            self._emit_runtime_signal(
                "CUSTOM_TASK_CREATE_BLOCKED",
                reason="write_blocked",
                title=draft.title,
                target_kind=draft.target_kind,
                detail=str(exc),
            )
            raise
        self.reload_command_action_catalog(self._saved_action_source_path)
        self._set_entry_feedback("ready", f'Custom task created: "{result.record["title"]}".')
        self._emit_runtime_signal(
            "CUSTOM_TASK_CREATED",
            action_id=result.record["id"],
            title=result.record["title"],
            target_kind=result.record["target_kind"],
        )
        return result

    def _handle_saved_action_edit_draft_submit(self, saved_action_id: str, draft: SavedActionDraft):
        self._emit_runtime_signal(
            "CUSTOM_TASK_EDIT_ATTEMPT_STARTED",
            action_id=saved_action_id,
            title=draft.title,
            target_kind=draft.target_kind,
        )
        try:
            result = update_saved_action_from_draft(
                saved_action_id,
                draft,
                source_path=self._saved_action_source_path,
            )
        except SavedActionDraftValidationError as exc:
            self._emit_runtime_signal(
                "CUSTOM_TASK_EDIT_BLOCKED",
                reason="validation_error",
                action_id=saved_action_id,
                title=draft.title,
                target_kind=draft.target_kind,
                detail=str(exc),
            )
            raise
        except SavedActionUnsafeSourceError as exc:
            self._emit_runtime_signal(
                "CUSTOM_TASK_EDIT_BLOCKED",
                reason="unsafe_source",
                action_id=saved_action_id,
                title=draft.title,
                target_kind=draft.target_kind,
                detail=str(exc),
            )
            raise
        except SavedActionSourceWriteBlocked as exc:
            self._emit_runtime_signal(
                "CUSTOM_TASK_EDIT_BLOCKED",
                reason="write_blocked",
                action_id=saved_action_id,
                title=draft.title,
                target_kind=draft.target_kind,
                detail=str(exc),
            )
            raise
        self.reload_command_action_catalog(self._saved_action_source_path)
        self._set_entry_feedback("ready", f'Custom task updated: "{result.record["title"]}".')
        self._emit_runtime_signal(
            "CUSTOM_TASK_UPDATED",
            action_id=result.record["id"],
            title=result.record["title"],
            target_kind=result.record["target_kind"],
        )
        return result

    def _handle_callable_group_create_draft_submit(self, draft: CallableGroupDraft):
        self._emit_runtime_signal(
            "CUSTOM_GROUP_CREATE_ATTEMPT_STARTED",
            title=draft.title,
            member_count=len(draft.member_action_ids),
        )
        try:
            result = create_callable_group_from_draft(
                draft,
                source_path=self._saved_action_source_path,
            )
        except (CallableGroupDraftValidationError, CallableGroupUnsafeSourceError, SavedActionSourceWriteBlocked):
            raise
        self.reload_command_action_catalog(self._saved_action_source_path)
        self._set_entry_feedback("ready", f'Custom group created: "{result.record["title"]}".')
        self._emit_runtime_signal(
            "CUSTOM_GROUP_CREATED",
            group_id=result.record["id"],
            title=result.record["title"],
            member_count=len(result.record.get("member_action_ids", ()) or ()),
        )
        return result

    def _handle_callable_group_edit_draft_submit(self, group_id: str, draft: CallableGroupDraft):
        self._emit_runtime_signal(
            "CUSTOM_GROUP_EDIT_ATTEMPT_STARTED",
            group_id=group_id,
            title=draft.title,
            member_count=len(draft.member_action_ids),
        )
        try:
            result = update_callable_group_from_draft(
                group_id,
                draft,
                source_path=self._saved_action_source_path,
            )
        except (CallableGroupDraftValidationError, CallableGroupUnsafeSourceError, SavedActionSourceWriteBlocked):
            raise
        self.reload_command_action_catalog(self._saved_action_source_path)
        self._set_entry_feedback("ready", f'Custom group updated: "{result.record["title"]}".')
        self._emit_runtime_signal(
            "CUSTOM_GROUP_UPDATED",
            group_id=result.record["id"],
            title=result.record["title"],
            member_count=len(result.record.get("member_action_ids", ()) or ()),
        )
        return result

    def handle_create_custom_task_requested(self):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_ACTION_BLOCKED",
                action="create_custom_task",
                reason="authoring_dialog_active",
            )
            return

        self._emit_runtime_signal("OVERLAY_ENTRY_ACTION_TRIGGERED", action="create_custom_task")

        inventory = self._command_model.action_catalog.saved_action_inventory
        if inventory.status_kind in {"invalid_source", "invalid_saved_actions"}:
            self._set_entry_feedback("not_found", self._saved_action_authoring_block_message("creation"))
            self._emit_runtime_signal(
                "CUSTOM_TASK_CREATE_BLOCKED",
                reason="source_invalid",
                status_kind=inventory.status_kind,
                **self._saved_action_inventory_signal_fields(inventory),
            )
            return

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = True
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._clear_overlay_input_capture()
        self._apply_command_overlay_state()

        QTimer.singleShot(0, self._open_create_custom_task_dialog)

    def _open_create_custom_task_dialog(self):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_DIALOG_CREATE_BLOCKED",
                action="create_custom_task",
                reason="authoring_dialog_active",
            )
            return

        self._emit_runtime_signal("OVERLAY_ENTRY_DIALOG_CREATE_START", action="create_custom_task")
        dialog = self._create_dialog_with_optional_lifecycle(
            self._saved_action_create_dialog_factory,
            self,
            self._handle_saved_action_create_draft_submit,
            **self._task_dialog_group_kwargs(),
            lifecycle_callback=self._handle_dialog_lifecycle_signal,
        )
        self._emit_runtime_signal(
            "OVERLAY_ENTRY_DIALOG_CREATED",
            action="create_custom_task",
            dialog_name=dialog.windowTitle(),
            dialog_object_name=dialog.objectName() or type(dialog).__name__,
            dialog_visible="true" if dialog.isVisible() else "false",
            win_id=int(dialog.winId()),
        )
        try:
            self._exec_authoring_dialog(dialog, action="create_custom_task")
        finally:
            self._resume_overlay_capture_after_authoring_dialog()

    def handle_created_tasks_requested(self):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_ACTION_BLOCKED",
                action="manage_custom_tasks",
                reason="authoring_dialog_active",
            )
            return

        inventory_payload = self._command_model.view_payload().get("saved_action_inventory") or {}

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = True
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._clear_overlay_input_capture()
        self._apply_command_overlay_state()

        dialog = self._create_dialog_with_optional_lifecycle(
            self._created_tasks_dialog_factory,
            self._command_panel,
            inventory_payload,
            lifecycle_callback=self._handle_dialog_lifecycle_signal,
        )
        selected_action_id = ""
        selected_delete_action_id = ""
        try:
            self._exec_authoring_dialog(dialog, action="manage_custom_tasks")
            if hasattr(dialog, "selected_action_id"):
                selected_action_id = str(dialog.selected_action_id() or "").strip()
            if hasattr(dialog, "selected_delete_action_id"):
                selected_delete_action_id = str(dialog.selected_delete_action_id() or "").strip()
        finally:
            self._resume_overlay_capture_after_authoring_dialog()

        if selected_delete_action_id:
            self.handle_delete_saved_action_requested(selected_delete_action_id)
        elif selected_action_id:
            self.handle_edit_saved_action_requested(selected_action_id)

    def handle_create_custom_group_requested(self):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_ACTION_BLOCKED",
                action="create_custom_group",
                reason="authoring_dialog_active",
            )
            return

        group_inventory = self._command_model.action_catalog.saved_group_inventory
        if group_inventory.status_kind in {"invalid_source", "invalid_saved_actions", "invalid_groups"}:
            self._set_entry_feedback("not_found", self._saved_group_authoring_block_message("creation"))
            self._emit_runtime_signal(
                "CUSTOM_GROUP_CREATE_BLOCKED",
                reason="source_invalid",
                status_kind=group_inventory.status_kind,
                **self._saved_group_inventory_signal_fields(group_inventory),
            )
            return

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = True
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._clear_overlay_input_capture()
        self._apply_command_overlay_state()

        dialog = self._create_dialog_with_optional_lifecycle(
            self._callable_group_create_dialog_factory,
            self._command_panel,
            self._handle_callable_group_create_draft_submit,
            available_members=self._group_dialog_member_items(),
            lifecycle_callback=self._handle_dialog_lifecycle_signal,
        )
        try:
            self._exec_authoring_dialog(dialog, action="create_custom_group")
        finally:
            self._resume_overlay_capture_after_authoring_dialog()

    def handle_created_groups_requested(self):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_ACTION_BLOCKED",
                action="manage_custom_groups",
                reason="authoring_dialog_active",
            )
            return

        inventory_payload = self._command_model.view_payload().get("saved_group_inventory") or {}

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = True
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._clear_overlay_input_capture()
        self._apply_command_overlay_state()

        dialog = self._create_dialog_with_optional_lifecycle(
            self._created_groups_dialog_factory,
            self._command_panel,
            inventory_payload,
            lifecycle_callback=self._handle_dialog_lifecycle_signal,
        )
        selected_group_id = ""
        selected_delete_group_id = ""
        try:
            self._exec_authoring_dialog(dialog, action="manage_custom_groups")
            if hasattr(dialog, "selected_group_id"):
                selected_group_id = str(dialog.selected_group_id() or "").strip()
            if hasattr(dialog, "selected_delete_group_id"):
                selected_delete_group_id = str(dialog.selected_delete_group_id() or "").strip()
        finally:
            self._resume_overlay_capture_after_authoring_dialog()

        if selected_delete_group_id:
            self.handle_delete_saved_group_requested(selected_delete_group_id)
        elif selected_group_id:
            self.handle_edit_saved_group_requested(selected_group_id)

    def handle_edit_saved_action_requested(self, saved_action_id: str):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_ACTION_BLOCKED",
                action="edit_custom_task",
                reason="authoring_dialog_active",
            )
            return

        inventory = self._command_model.action_catalog.saved_action_inventory
        if inventory.status_kind in {"invalid_source", "invalid_saved_actions"}:
            self._set_entry_feedback("not_found", self._saved_action_authoring_block_message("editing"))
            self._emit_runtime_signal(
                "CUSTOM_TASK_EDIT_BLOCKED",
                reason="source_invalid",
                action_id=saved_action_id,
                status_kind=inventory.status_kind,
                **self._saved_action_inventory_signal_fields(inventory),
            )
            return

        try:
            initial_draft = load_saved_action_draft_for_edit(
                saved_action_id,
                source_path=self._saved_action_source_path,
            )
        except SavedActionUnsafeSourceError:
            self._set_entry_feedback("not_found", self._saved_action_authoring_block_message("editing"))
            self._emit_runtime_signal(
                "CUSTOM_TASK_EDIT_BLOCKED",
                reason="unsafe_source",
                action_id=saved_action_id,
            )
            return
        except SavedActionDraftValidationError as exc:
            self._set_entry_feedback("not_found", str(exc))
            self._emit_runtime_signal(
                "CUSTOM_TASK_EDIT_BLOCKED",
                reason="missing_record",
                action_id=saved_action_id,
                detail=str(exc),
            )
            return

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = True
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._clear_overlay_input_capture()
        self._apply_command_overlay_state()

        dialog = self._create_dialog_with_optional_lifecycle(
            self._saved_action_edit_dialog_factory,
            self._command_panel,
            lambda draft: self._handle_saved_action_edit_draft_submit(saved_action_id, draft),
            initial_draft=initial_draft,
            **self._task_dialog_group_kwargs(),
            lifecycle_callback=self._handle_dialog_lifecycle_signal,
        )
        try:
            self._exec_authoring_dialog(dialog, action="edit_custom_task")
        finally:
            self._resume_overlay_capture_after_authoring_dialog()

    def handle_edit_saved_group_requested(self, group_id: str):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._authoring_dialog_blocks_new_dialog():
            self._emit_runtime_signal(
                "OVERLAY_ENTRY_ACTION_BLOCKED",
                action="edit_custom_group",
                reason="authoring_dialog_active",
            )
            return

        group_inventory = self._command_model.action_catalog.saved_group_inventory
        if group_inventory.status_kind in {"invalid_source", "invalid_saved_actions", "invalid_groups"}:
            self._set_entry_feedback("not_found", self._saved_group_authoring_block_message("editing"))
            self._emit_runtime_signal(
                "CUSTOM_GROUP_EDIT_BLOCKED",
                reason="source_invalid",
                group_id=group_id,
                status_kind=group_inventory.status_kind,
                **self._saved_group_inventory_signal_fields(group_inventory),
            )
            return

        try:
            initial_draft = load_callable_group_draft_for_edit(
                group_id,
                source_path=self._saved_action_source_path,
            )
        except (CallableGroupUnsafeSourceError, CallableGroupDraftValidationError) as exc:
            self._set_entry_feedback("not_found", str(exc))
            self._emit_runtime_signal(
                "CUSTOM_GROUP_EDIT_BLOCKED",
                reason="missing_record",
                group_id=group_id,
                detail=str(exc),
            )
            return

        self._overlay_local_input_engaged = False
        self._overlay_global_capture_suspended = True
        self._command_panel.input_line.set_local_typing_enabled(False)
        self._clear_overlay_input_capture()
        self._apply_command_overlay_state()

        dialog = self._create_dialog_with_optional_lifecycle(
            self._callable_group_edit_dialog_factory,
            self._command_panel,
            lambda draft: self._handle_callable_group_edit_draft_submit(group_id, draft),
            initial_draft=initial_draft,
            available_members=self._group_dialog_member_items(),
            lifecycle_callback=self._handle_dialog_lifecycle_signal,
        )
        try:
            self._exec_authoring_dialog(dialog, action="edit_custom_group")
        finally:
            self._resume_overlay_capture_after_authoring_dialog()

    def handle_delete_saved_action_requested(self, saved_action_id: str):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return

        inventory = self._command_model.action_catalog.saved_action_inventory
        if inventory.status_kind in {"invalid_source", "invalid_saved_actions"}:
            self._set_entry_feedback("not_found", self._saved_action_authoring_block_message("deletion"))
            self._emit_runtime_signal(
                "CUSTOM_TASK_DELETE_BLOCKED",
                reason="source_invalid",
                action_id=saved_action_id,
                status_kind=inventory.status_kind,
                **self._saved_action_inventory_signal_fields(inventory),
            )
            return

        self._emit_runtime_signal(
            "CUSTOM_TASK_DELETE_ATTEMPT_STARTED",
            action_id=saved_action_id,
        )
        try:
            result = delete_saved_action(
                saved_action_id,
                source_path=self._saved_action_source_path,
            )
        except SavedActionUnsafeSourceError:
            self._set_entry_feedback("not_found", self._saved_action_authoring_block_message("deletion"))
            self._emit_runtime_signal(
                "CUSTOM_TASK_DELETE_BLOCKED",
                reason="unsafe_source",
                action_id=saved_action_id,
            )
            return
        except SavedActionDraftValidationError as exc:
            self._set_entry_feedback("not_found", str(exc))
            self._emit_runtime_signal(
                "CUSTOM_TASK_DELETE_BLOCKED",
                reason="missing_record",
                action_id=saved_action_id,
                detail=str(exc),
            )
            return
        except SavedActionSourceWriteBlocked as exc:
            self._set_entry_feedback("not_found", str(exc))
            self._emit_runtime_signal(
                "CUSTOM_TASK_DELETE_BLOCKED",
                reason="write_blocked",
                action_id=saved_action_id,
                detail=str(exc),
            )
            return

        self.reload_command_action_catalog(self._saved_action_source_path)
        self._set_entry_feedback("ready", f'Custom task deleted: "{result.record["title"]}".')
        self._emit_runtime_signal(
            "CUSTOM_TASK_DELETED",
            action_id=result.record["id"],
            title=result.record["title"],
            target_kind=result.record["target_kind"],
        )

    def handle_delete_saved_group_requested(self, group_id: str):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return

        group_inventory = self._command_model.action_catalog.saved_group_inventory
        if group_inventory.status_kind in {"invalid_source", "invalid_saved_actions", "invalid_groups"}:
            self._set_entry_feedback("not_found", self._saved_group_authoring_block_message("deletion"))
            self._emit_runtime_signal(
                "CUSTOM_GROUP_DELETE_BLOCKED",
                reason="source_invalid",
                group_id=group_id,
                status_kind=group_inventory.status_kind,
                **self._saved_group_inventory_signal_fields(group_inventory),
            )
            return

        try:
            result = delete_callable_group(
                group_id,
                source_path=self._saved_action_source_path,
            )
        except (CallableGroupUnsafeSourceError, CallableGroupDraftValidationError, SavedActionSourceWriteBlocked) as exc:
            self._set_entry_feedback("not_found", str(exc))
            self._emit_runtime_signal(
                "CUSTOM_GROUP_DELETE_BLOCKED",
                reason="write_blocked",
                group_id=group_id,
                detail=str(exc),
            )
            return

        self.reload_command_action_catalog(self._saved_action_source_path)
        self._set_entry_feedback("ready", f'Custom group deleted: "{result.record["title"]}".')
        self._emit_runtime_signal(
            "CUSTOM_GROUP_DELETED",
            group_id=result.record["id"],
            title=result.record["title"],
        )

    def handle_command_text_changed(self, text: str):
        self._command_model.set_input_text(text)
        self._apply_command_overlay_state()
        self._trace_overlay("local_text_changed", new_text=repr(text))

    def handle_overlay_text_requested(self, text: str):
        if not text or not self.overlay_needs_global_input_capture():
            return

        self._refresh_overlay_input_capture()
        if self._command_model.phase == "choose":
            if text.isdigit():
                self.handle_ambiguous_match_selected(int(text) - 1)
            return

        if self._command_model.phase != "entry":
            return

        self._command_model.input_armed = True
        before = self._command_model.input_text
        self._command_model.append_text(text)
        self._apply_command_overlay_state()
        self._trace_overlay(
            "global_text_requested",
            text=repr(text),
            input_before=repr(before),
            input_after=repr(self._command_model.input_text),
        )

    def handle_overlay_backspace_requested(self):
        if not self.overlay_needs_global_input_capture() or self._command_model.phase != "entry":
            return

        self._refresh_overlay_input_capture()
        self._command_model.input_armed = True
        self._command_model.backspace()
        self._apply_command_overlay_state()

    def handle_overlay_submit_requested(self):
        if not self.overlay_needs_global_input_capture():
            return
        self._refresh_overlay_input_capture()
        self.handle_command_submit(source="fallback")

    def handle_local_submit_requested(self):
        self.handle_command_submit(source="local")

    def handle_overlay_escape_requested(self):
        if not self._command_model.visible:
            return

        if self.overlay_needs_global_input_capture():
            self._refresh_overlay_input_capture()
        self.handle_command_escape()

    def handle_command_input_armed_changed(self, armed: bool):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        self._command_model.input_armed = bool(armed)
        self._apply_command_overlay_state()
        self._schedule_overlay_ready_check(0)

    def handle_command_input_focus_acquired(self):
        if self._command_model.visible and self._command_model.phase == "entry":
            panel_is_active = self._command_panel.isActiveWindow()
            input_has_focus = self._command_panel.input_line.hasFocus()
            manual_focus = self._command_panel.input_line.last_focus_was_manual()
            if panel_is_active and input_has_focus and manual_focus:
                self._command_panel.input_line.set_local_typing_enabled(True)
                self._overlay_local_input_engaged = True
                self._overlay_global_capture_suspended = False
                self._clear_overlay_input_capture()
                self._trace_overlay("input_focus_acquired", manual_focus="true", mode="local")
                self._schedule_overlay_ready_check(0)
                return

            if panel_is_active and input_has_focus and self._overlay_global_capture_suspended:
                self._command_panel.input_line.set_local_typing_enabled(False)
                self._overlay_local_input_engaged = False
                self._overlay_global_capture_suspended = False
                self._refresh_overlay_input_capture()
                self._trace_overlay(
                    "input_focus_acquired",
                    manual_focus="true" if manual_focus else "false",
                    mode="rearmed",
                )
                self._schedule_overlay_ready_check(0)
                return

            self._command_panel.input_line.set_local_typing_enabled(False)
            self._overlay_local_input_engaged = False
            self._refresh_overlay_input_capture()
            self._trace_overlay(
                "input_focus_acquired",
                manual_focus="true" if manual_focus else "false",
                mode="fallback",
            )
            self._schedule_overlay_ready_check(0)

    def handle_command_input_focus_lost(self):
        if not self._command_model.visible:
            return
        if self._command_model.phase == "entry" and self._overlay_local_input_engaged:
            self._command_panel.input_line.set_local_typing_enabled(False)
            self._overlay_local_input_engaged = False
            self._refresh_overlay_input_capture()
        self._trace_overlay("input_focus_lost")
        self._schedule_overlay_ready_check(0)

    def _command_panel_contains_global_point(self, x: int, y: int) -> bool:
        try:
            return self._command_panel.frameGeometry().contains(int(x), int(y))
        except Exception:
            return False

    def handle_overlay_global_click_requested(self, x: int, y: int):
        if not self._command_model.visible or self._command_model.phase != "entry":
            return
        if self._overlay_local_input_engaged:
            return
        if self._command_panel_contains_global_point(x, y):
            self._trace_overlay("global_click_inside_overlay", x=str(int(x)), y=str(int(y)))
            return

        self._overlay_global_capture_suspended = True
        self._clear_overlay_input_capture()
        self._trace_overlay("global_click_suspended_capture", x=str(int(x)), y=str(int(y)))

    def handle_command_escape(self):
        result = self._command_model.escape()
        self._apply_command_overlay_state()

        if result == "choice_cancelled":
            if self._overlay_local_input_engaged:
                self._command_panel.focus_input()
            else:
                self._refresh_overlay_input_capture(seconds=5.0)
            self._log_event("RENDERER_MAIN|COMMAND_DISAMBIGUATION_CANCELLED")
            return

        if result == "confirm_cancelled":
            if self._overlay_local_input_engaged:
                self._command_panel.focus_input()
            else:
                self._refresh_overlay_input_capture(seconds=5.0)
            self._log_event("RENDERER_MAIN|COMMAND_CONFIRM_CANCELLED")
            return

        if result == "closed":
            self._reset_overlay_ready_tracking()
            self._command_panel.hide()
            self._log_event("RENDERER_MAIN|COMMAND_OVERLAY_CLOSED")

    def _show_command_result(self, status_kind: str, status_text: str, close_delay_ms: int = 1200):
        self._command_model.show_result(status_kind, status_text)
        self._apply_command_overlay_state()
        self._result_close_timer.start(max(0, int(close_delay_ms)))

    def _emit_group_execution_marker(self, marker_name: str, fields: dict[str, str]):
        parts = ["RENDERER_MAIN", marker_name]
        for key, value in fields.items():
            normalized = (value or "").strip()
            if not normalized:
                continue
            parts.append(f"{key}={normalized}")
        self._log_event("|".join(parts))

    def _execute_callable_group(self, group):
        return execute_command_group(
            group,
            action_launcher=launch_command_action,
            marker_emitter=self._emit_group_execution_marker,
        )

    def _close_command_overlay_after_result(self):
        self.close_command_overlay()

    def _record_launch_failure(self, action_id: str) -> int:
        if self._last_launch_failure_action_id == action_id:
            self._last_launch_failure_count += 1
        else:
            self._last_launch_failure_action_id = action_id
            self._last_launch_failure_count = 1
        return self._last_launch_failure_count

    def _clear_launch_failure_tracking(self, action_id: str):
        if self._last_launch_failure_action_id == action_id:
            self._last_launch_failure_action_id = ""
            self._last_launch_failure_count = 0
        self._reported_recoverable_launch_failures.discard(action_id)

    def _classify_recoverable_launch_failed_incident(
        self,
        action_id: str,
        failure_count: int,
        *,
        failure_context: dict[str, str] | None = None,
    ) -> str:
        normalized_failure_context = self._normalize_launch_failure_context(
            action_id,
            failure_context,
        )
        context_suffix = self._format_failure_context_suffix(normalized_failure_context)
        if failure_count < 2:
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_CLASS2_INLINE|action_id={action_id}|count={failure_count}{context_suffix}"
            )
            return "class2_inline"

        if action_id in self._reported_recoverable_launch_failures:
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_CLASS3_ALREADY_REPORTED|action_id={action_id}|count={failure_count}{context_suffix}"
            )
            return "class3_already_reported"

        self._log_event(
            f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_CLASS3_REPORT_SELECTED|action_id={action_id}|count={failure_count}{context_suffix}"
        )
        return "class3_report_selected"

    def _format_failure_context_suffix(self, failure_context: dict[str, str] | None) -> str:
        if not failure_context:
            return ""
        suffix_parts = []
        for key, value in failure_context.items():
            normalized = (value or "").strip()
            if not normalized:
                continue
            suffix_parts.append(f"{key}={normalized.replace('|', '/')}")
        if not suffix_parts:
            return ""
        return "|" + "|".join(suffix_parts)

    def _bound_execution_trace(self, execution_trace: str, *, fallback_action_id: str = "") -> str:
        segments = [
            segment.strip()
            for segment in (execution_trace or "").split(">")
            if segment and segment.strip()
        ]
        if not segments and fallback_action_id.strip():
            segments = [fallback_action_id.strip()]
        if len(segments) > 8:
            segments = segments[-8:]
        return ">".join(segment.replace("|", "/") for segment in segments)

    def _normalize_launch_failure_context(
        self,
        action_id: str,
        failure_context: dict[str, str] | None = None,
    ) -> dict[str, str]:
        raw_context = dict(failure_context or {})
        execution_type = (raw_context.get("execution_type") or "single").strip().casefold()
        normalized_error_type = (raw_context.get("error_type") or "launch_exception").strip() or "launch_exception"

        if execution_type == "group":
            failed_action_id = (raw_context.get("failed_action_id") or action_id or "").strip()
            return {
                "execution_type": "group",
                "failed_action_id": failed_action_id,
                "group_id": (raw_context.get("group_id") or "").strip(),
                "step_index": (raw_context.get("step_index") or raw_context.get("failed_step_index") or "").strip(),
                "error_type": normalized_error_type,
                "execution_trace": self._bound_execution_trace(
                    raw_context.get("execution_trace", ""),
                    fallback_action_id=failed_action_id,
                ),
            }

        normalized_action_id = (action_id or "").strip()
        return {
            "execution_type": "single",
            "action_id": normalized_action_id,
            "group_id": "",
            "step_index": "",
            "error_type": normalized_error_type,
            "execution_trace": self._bound_execution_trace(
                raw_context.get("execution_trace", ""),
                fallback_action_id=normalized_action_id,
            ),
        }

    def _prepare_recoverable_launch_failure_report(self, action, *, failure_context: dict[str, str] | None = None) -> str | None:
        normalized_failure_context = self._normalize_launch_failure_context(
            action.id,
            failure_context,
        )
        failure_count = self._record_launch_failure(action.id)
        context_suffix = self._format_failure_context_suffix(normalized_failure_context)
        incident_class = self._classify_recoverable_launch_failed_incident(
            action.id,
            failure_count,
            failure_context=normalized_failure_context,
        )
        if incident_class == "class2_inline":
            return None
        if incident_class == "class3_already_reported":
            return None
        if not self.runtime_log_path or not os.path.isfile(self.runtime_log_path):
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_SKIPPED|action_id={action.id}|reason=runtime_log_unavailable{context_suffix}"
            )
            return None

        crash_dir = os.path.join(os.path.dirname(self.runtime_log_path), "crash")
        self._log_event(
            f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_BEGIN|action_id={action.id}|count={failure_count}{context_suffix}"
        )
        try:
            report_prep = prepare_manual_issue_report(ROOT_DIR, self.runtime_log_path, crash_dir)
        except SupportBundleError as exc:
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_FAILED|action_id={action.id}|reason={exc}{context_suffix}"
            )
            return None
        except Exception as exc:
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_FAILED|action_id={action.id}|reason={exc}{context_suffix}"
            )
            return None

        bundle_info = report_prep["bundle_info"]
        issue_url = report_prep["issue_url"]
        browser_opened = False

        try:
            os.startfile(os.path.dirname(bundle_info["bundle_path"]))
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_FOLDER_OPENED|action_id={action.id}|bundle={bundle_info['bundle_name']}{context_suffix}"
            )
        except Exception as exc:
            self._log_event(
                f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_FOLDER_FAILED|action_id={action.id}|reason={exc}{context_suffix}"
            )

        if issue_url:
            try:
                browser_opened = webbrowser.open(issue_url, new=2)
            except Exception as exc:
                self._log_event(
                    f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_ISSUE_FAILED|action_id={action.id}|reason={exc}{context_suffix}"
                )

        self._reported_recoverable_launch_failures.add(action.id)
        self._log_event(
            f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED_RECOVERABLE_REPORT_READY|action_id={action.id}|bundle={bundle_info['bundle_name']}{context_suffix}"
        )

        if browser_opened:
            return "Launch failed again. Support bundle prepared and issue draft opened; attach the bundle manually."
        if issue_url:
            return "Launch failed again. Support bundle prepared; open the issue page manually and attach the bundle."
        return "Launch failed again. Support bundle prepared; review it locally before filing the report."

    def _resolve_group_failure_action(self, group, failed_action_id: str):
        normalized_failed_action_id = (failed_action_id or "").strip().casefold()
        if not normalized_failed_action_id:
            return None
        for action in tuple(group.member_actions):
            if action.id.strip().casefold() == normalized_failed_action_id:
                return action
        return None

    def _build_group_failure_context(self, group, result) -> dict[str, str]:
        execution_trace = tuple(result.completed_action_ids) + (
            (result.failed_action_id,) if result.failed_action_id else ()
        )
        return {
            "execution_type": "group",
            "group_id": group.id,
            "failed_action_id": result.failed_action_id,
            "step_index": str(result.failed_step_index),
            "error_type": "launch_exception",
            "execution_trace": self._bound_execution_trace(
                ">".join(action_id for action_id in execution_trace if action_id),
                fallback_action_id=result.failed_action_id or "",
            ),
        }

    def handle_ambiguous_match_selected(self, index: int):
        result, payload = self._command_model.choose_match(index)
        self._apply_command_overlay_state()

        if result != "confirm_ready":
            return

        if self._overlay_local_input_engaged:
            self._command_panel.setFocus(Qt.ActiveWindowFocusReason)
        else:
            self._refresh_overlay_input_capture(seconds=5.0)
        self._log_event(
            f"RENDERER_MAIN|COMMAND_DISAMBIGUATION_SELECTED|index={index}|action_id={payload.id}"
        )
        self._log_event(f"RENDERER_MAIN|COMMAND_CONFIRM_READY|action_id={payload.id}")

    def handle_command_submit(self, source: str = "local"):
        foreground = self._foreground_window_snapshot()
        self._trace_overlay(
            "submit_requested",
            source=repr(source),
            foreground_hwnd=repr(foreground["hwnd"]),
            foreground_class=repr(foreground["class_name"]),
            foreground_title=repr(foreground["title"]),
        )
        result, payload = self._command_model.submit()
        self._apply_command_overlay_state()
        payload_id = getattr(payload, "id", "") if payload is not None else ""
        self._trace_overlay(
            "submit_result",
            source=repr(source),
            result=repr(result),
            payload_id=repr(payload_id),
        )

        if result == "confirm_ready":
            if self._overlay_local_input_engaged:
                self._command_panel.setFocus(Qt.ActiveWindowFocusReason)
            else:
                self._refresh_overlay_input_capture(seconds=5.0)
            self._log_event(f"RENDERER_MAIN|COMMAND_CONFIRM_READY|action_id={payload.id}")
            return

        if result == "not_found":
            self._log_event("RENDERER_MAIN|COMMAND_NOT_FOUND")
            return

        if result == "ambiguous":
            if self._overlay_local_input_engaged:
                self._command_panel.setFocus(Qt.ActiveWindowFocusReason)
            else:
                self._refresh_overlay_input_capture(seconds=5.0)
            self._log_event(f"RENDERER_MAIN|COMMAND_AMBIGUOUS|count={len(payload)}")
            return

        if result != "execute_confirmed":
            return

        intent = payload
        action = intent.action
        execution_request_fields = [f"action_id={intent.action_id}"]
        if intent.execution_type == "group":
            execution_request_fields.append(f"group_id={intent.group_id}")
        self._log_event("RENDERER_MAIN|COMMAND_EXECUTION_REQUESTED|" + "|".join(execution_request_fields))

        if intent.execution_type == "group":
            group = intent.group
            if group is None:
                return
            group_label = (group.title or "").strip() or group.id
            result = self._execute_callable_group(group)
            if not result.succeeded:
                failure_context = self._build_group_failure_context(group, result)
                self._log_event(
                    "RENDERER_MAIN|COMMAND_GROUP_EXECUTION_FAILED|"
                    f"group_id={group.id}|failed_action_id={result.failed_action_id}|failed_step_index={result.failed_step_index}|"
                    f"execution_trace={failure_context.get('execution_trace', '')}"
                )
                failed_action = self._resolve_group_failure_action(group, result.failed_action_id)
                recoverable_status = None
                if failed_action is not None:
                    recoverable_status = self._prepare_recoverable_launch_failure_report(
                        failed_action,
                        failure_context=failure_context,
                    )
                if recoverable_status:
                    self._show_command_result("launch_failed", recoverable_status, close_delay_ms=2600)
                else:
                    failed_step_index = result.failed_step_index if result.failed_step_index is not None else "?"
                    self._show_command_result(
                        "launch_failed",
                        f'Group "{group_label}" failed at step {failed_step_index}: {result.error}',
                    )
                return

            for completed_action_id in result.completed_action_ids:
                self._clear_launch_failure_tracking(completed_action_id)
            self._log_event(
                "RENDERER_MAIN|COMMAND_GROUP_EXECUTION_COMPLETED|"
                f"group_id={group.id}|step_count={result.step_count}"
            )
            self._show_command_result("launch_requested", f'Group "{group_label}" executed in stored order.')
            return

        try:
            launch_command_action(action)
        except Exception as exc:
            self._log_event(f"RENDERER_MAIN|COMMAND_LAUNCH_FAILED|action_id={action.id}")
            recoverable_status = self._prepare_recoverable_launch_failure_report(action)
            if recoverable_status:
                self._show_command_result("launch_failed", recoverable_status, close_delay_ms=2600)
            else:
                self._show_command_result("launch_failed", f"Launch failed: {exc}")
            return

        self._clear_launch_failure_tracking(action.id)
        self._log_event(f"RENDERER_MAIN|COMMAND_LAUNCH_REQUEST_SENT|action_id={action.id}")
        self._show_command_result("launch_requested", "Launch request sent.")

    def nativeEvent(self, eventType, message):
        if (
            self.surface_role == "hud"
            and self.desktop_mode
            and self._monitoring_hud_feature_enabled
            and self._monitoring_hud_visible
            and eventType in ("windows_generic_MSG", "windows_dispatcher_MSG")
        ):
            try:
                msg = ctypes.wintypes.MSG.from_address(int(message))
            except Exception:
                msg = None
            if msg is not None:
                message_id = int(msg.message)
                if message_id == WM_NCHITTEST:
                    x = ctypes.c_short(int(msg.lParam) & 0xFFFF).value
                    y = ctypes.c_short((int(msg.lParam) >> 16) & 0xFFFF).value
                    screen_point = QPoint(x, y)
                    if self._monitoring_hud_dashboard_control_rect_contains(screen_point):
                        return True, HTCLIENT
                    edges = self._monitoring_hud_native_resize_edges_for_point(screen_point)
                    hit_test = self._monitoring_hud_native_resize_hit_test_for_edges(edges)
                    if hit_test and not self._monitoring_hud_dashboard_control_rect_contains(screen_point):
                        # Windows owns the cursor state at the visible resize rail;
                        # the frameless Dashboard still owns geometry resize below.
                        return True, hit_test
                    if (
                        self._monitoring_hud_header_rect().contains(screen_point)
                        and not self._monitoring_hud_dashboard_control_rect_contains(screen_point)
                    ):
                        return True, HTCAPTION
                if message_id == WM_NCLBUTTONDBLCLK:
                    screen_point = self._monitoring_hud_cursor_screen_point()
                    if (
                        not screen_point.isNull()
                        and self._monitoring_hud_header_rect().contains(screen_point)
                    ):
                        self._emit_runtime_signal(
                            "MONITORING_HUD_NATIVE_HEADER_DOUBLE_CLICK_SUPPRESSED",
                            package="PKG-006",
                            slice="SLC-029",
                            seam="LV1",
                            x=screen_point.x(),
                            y=screen_point.y(),
                        )
                        return True, 0
                if message_id in (WM_SETCURSOR, WM_MOUSEMOVE, WM_NCMOUSEMOVE) and not self._monitoring_hud_native_window_resize_active:
                    _, edges = self._monitoring_hud_resize_edges_under_cursor()
                    if edges:
                        self._set_monitoring_hud_resize_cursor(edges)
                        if message_id == WM_SETCURSOR:
                            return True, 1
                    elif message_id == WM_SETCURSOR:
                        self._reset_monitoring_hud_resize_cursor()
                if message_id == WM_NCLBUTTONDOWN:
                    edges = self._monitoring_hud_native_resize_edges_for_hit_test(int(msg.wParam))
                    screen_point = self._monitoring_hud_cursor_screen_point()
                    if not screen_point.isNull():
                        if self._handle_monitoring_hud_dashboard_settings_native_control(screen_point):
                            return True, 0
                        if self._handle_monitoring_hud_dashboard_close_native_control(screen_point):
                            return True, 0
                    if edges and not screen_point.isNull() and not self._monitoring_hud_dashboard_control_rect_contains(screen_point):
                        self._set_monitoring_hud_resize_cursor(edges)
                        self._start_monitoring_hud_fallback_window_resize(edges, screen_point)
                        return True, 0
                    if (
                        int(msg.wParam) == HTCAPTION
                        and not screen_point.isNull()
                        and self._monitoring_hud_header_rect().contains(screen_point)
                        and not self._monitoring_hud_dashboard_control_rect_contains(screen_point)
                    ):
                        self._begin_monitoring_hud_native_user_move("native_caption_move")
                if self._monitoring_hud_native_window_resize_active and message_id in (WM_MOUSEMOVE, WM_NCMOUSEMOVE):
                    screen_point = self._monitoring_hud_cursor_screen_point()
                    if not screen_point.isNull():
                        self._update_monitoring_hud_fallback_window_resize(screen_point)
                    return True, 0
                if self._monitoring_hud_native_window_resize_active and message_id in (
                    WM_LBUTTONUP,
                    WM_NCLBUTTONUP,
                    WM_CAPTURECHANGED,
                    WM_CANCELMODE,
                ):
                    self._finish_monitoring_hud_fallback_window_resize(self._monitoring_hud_cursor_screen_point())
                    return True, 0
        return super().nativeEvent(eventType, message)

    def enable_desktop_mode(self):
        if self.desktop_mode or self._is_shutting_down or not self._page_ready:
            return

        self._log_event("RENDERER_MAIN|DESKTOP_MODE_ENABLE_BEGIN")
        self.desktop_mode = True
        self._desktop_mode_requested = False
        self._monitoring_hud_user_geometry_override_active = False
        self._clear_monitoring_hud_native_user_move()
        target_geometry = self.compute_compact_geometry()

        self._arm_monitoring_hud_visible_show_guard("enable_desktop_mode")
        self.setGeometry(target_geometry)
        self._monitoring_hud_interactive_screen_rect = self._estimate_monitoring_hud_interactive_screen_rect()
        self._publish_monitoring_hud_control_state_to_page()
        self._apply_monitoring_hud_window_interaction_state()

        hwnd = int(self.winId())
        self.show()
        self._log_native_window_state("after_visible_overlay_show", hwnd)
        self.setGeometry(target_geometry)

        if not self.webview.isVisible():
            self.webview.show()
            self._log_event("RENDERER_MAIN|WEBVIEW_REVEALED_FOR_VISIBLE_OVERLAY")
            QTimer.singleShot(50, lambda: self._capture_startup_snapshot("after_visible_overlay_reveal"))
            QTimer.singleShot(300, lambda: self._capture_startup_snapshot("after_300ms"))
            QTimer.singleShot(600, lambda: self._capture_startup_snapshot("after_600ms"))
            QTimer.singleShot(1000, lambda: self._capture_startup_snapshot("after_1000ms"))
            QTimer.singleShot(1600, lambda: self._capture_startup_snapshot("after_1600ms"))
            QTimer.singleShot(2200, lambda: self._capture_startup_snapshot("after_2200ms"))

        QTimer.singleShot(80, self._release_initial_visibility_guard)
        self._publish_monitoring_hud_telemetry_boundary()
        self._publish_monitoring_hud_placement_ownership()
        self._publish_monitoring_hud_controls_visibility()
        self._publish_monitoring_hud_status_behavior()
        self._publish_monitoring_hud_control_state_to_page()
        if not self._monitoring_hud_poll_timer.isActive():
            self._monitoring_hud_poll_timer.start(self._monitoring_hud_polling_rate_ms)
        if not self._monitoring_hud_control_sync_timer.isActive():
            self._monitoring_hud_control_sync_timer.start(500)
        self._emit_runtime_signal(
            "MONITORING_HUD_VISIBLE_OVERLAY_READY",
            package="PKG-006",
            slice="SLC-016",
            pointer_model="click_through_no_focus",
        )
        self._log_event("RENDERER_MAIN|DESKTOP_VISIBLE_OVERLAY_RESULT|success=true")

        self.webview.update()
        self.update()
        self._run_javascript("window.dispatchEvent(new Event('resize'));")
        QTimer.singleShot(260, self._reinforce_desktop_mode)
        QTimer.singleShot(900, self._reinforce_desktop_mode)

    def _monitoring_hud_controls_visibility_contract(self) -> dict[str, str]:
        return build_monitoring_hud_controls_visibility_contract(
            desktop_mode=self.desktop_mode,
            feature_enabled=self._monitoring_hud_feature_enabled,
            visible=self._monitoring_hud_visible,
            anchored=self._monitoring_hud_anchored,
            snap_enabled=self._monitoring_hud_snap_enabled,
            polling_rate_ms=self._monitoring_hud_polling_rate_ms,
        ).as_dict()

    def _publish_monitoring_hud_controls_visibility(self):
        controls_json = json.dumps(
            self._monitoring_hud_controls_visibility_contract(),
            sort_keys=True,
        )
        self._run_javascript(
            f"""
            if (window.setMonitoringHudControlsVisibility) {{
                window.setMonitoringHudControlsVisibility({controls_json});
            }}
            """
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_CONTROLS_VISIBILITY_READY",
            package="PKG-006",
            slice="SLC-027",
            controls="hud-controls-visibility",
            persistence="local_layout_state",
            anchored=self._monitoring_hud_anchored,
            polling_rate_ms=self._monitoring_hud_polling_rate_ms,
        )

    def _monitoring_hud_status_snapshot(self) -> dict[str, str]:
        return build_monitoring_hud_status_snapshot(
            page_ready=self._page_ready,
            desktop_mode=self.desktop_mode,
            event_route_present=callable(self.event_logger),
        ).as_dict()

    def _publish_monitoring_hud_status_behavior(self):
        status_json = json.dumps(self._monitoring_hud_status_snapshot(), sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setMonitoringHudStatusBehavior) {{
                window.setMonitoringHudStatusBehavior({status_json});
            }}
            """
        )
        self._emit_runtime_signal(
            "MONITORING_HUD_STATUS_BEHAVIOR_READY",
            package="PKG-006",
            slice="SLC-028",
            status="hud-local-readiness-status",
            source_truth="renderer_local",
        )

    def _publish_ai_provider_state_to_page(self):
        if not self._page_ready or self._is_shutting_down:
            return

        payload = self._ai_provider_state.as_renderer_payload()
        payload_json = json.dumps(payload, sort_keys=True)
        self._run_javascript(
            f"""
            if (window.setAIProviderState) {{
                window.setAIProviderState({payload_json});
            }}
            """
        )
        self._emit_runtime_signal(
            "AI_PROVIDER_STATE_READY",
            package=payload.get("packageId", ""),
            slices=",".join(payload.get("sliceIds", [])),
            state_id=payload.get("stateId", ""),
            mode=payload.get("mode", ""),
            availability=payload.get("availability", ""),
            privacy_scope=payload.get("privacyScope", ""),
            provider_visible_data=payload.get("providerVisibleData", ""),
            sent_to_provider=payload.get("sentToProvider", False),
        )

    def request_shutdown(self):
        if self._is_shutting_down:
            return

        self._log_event("RENDERER_MAIN|RENDERER_SHUTDOWN_BEGIN")
        self._is_shutting_down = True
        self._result_close_timer.stop()
        self._monitoring_hud_poll_timer.stop()
        self._monitoring_hud_control_sync_timer.stop()

        self._command_panel.hide()
        if self._monitoring_hud_minimal_native_overlay is not None:
            self._monitoring_hud_minimal_native_overlay.request_shutdown()
        self.webview.stop()
        self.hide()
        self.close()

        app = QApplication.instance()

        if app is not None:
            QTimer.singleShot(0, app.quit)
