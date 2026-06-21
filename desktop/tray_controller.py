import ctypes
import ctypes.wintypes

from PySide6.QtGui import QAction, QColor, QCursor, QFont, QIcon, QPainter, QPen, QPixmap
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from .resident_access import (
    TRAY_DISCOVERY_DURATION_MS,
    TRAY_DISCOVERY_MESSAGE,
    TRAY_IDENTITY_LABEL,
    TRAY_ORIN_MARK_LABEL,
    TRAY_TOOLTIP_TEXT,
    build_resident_access_menu_plan,
)

QUICK_SLOT_COMMAND_BASE_ID = 200


def build_resident_tray_icon() -> QIcon:
    icon = QIcon()
    for size in (16, 20, 24, 32, 48, 64):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)

        margin = max(1, int(size * 0.08))
        body_rect = pixmap.rect().adjusted(margin, margin, -margin, -margin)
        radius = max(3, int(size * 0.24))
        painter.setPen(QPen(QColor("#0f766e"), max(1, int(size * 0.08))))
        painter.setBrush(QColor("#111827"))
        painter.drawRoundedRect(body_rect, radius, radius)

        painter.setPen(QPen(QColor("#f8fafc"), max(1, int(size * 0.09))))
        left_x = int(size * 0.32)
        right_x = int(size * 0.68)
        top_y = int(size * 0.28)
        bottom_y = int(size * 0.72)
        painter.drawLine(left_x, bottom_y, left_x, top_y)
        painter.drawLine(left_x, top_y, right_x, bottom_y)
        painter.drawLine(right_x, bottom_y, right_x, top_y)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#22c55e"))
        dot_size = max(3, int(size * 0.18))
        painter.drawEllipse(
            int(size * 0.66),
            int(size * 0.12),
            dot_size,
            dot_size,
        )
        painter.end()
        icon.addPixmap(pixmap)
    return icon


class TrayCommandPopup(QWidget):
    """Small user-facing tray menu surface with real button hit targets."""

    def __init__(self, owner):
        super().__init__(None, Qt.Popup | Qt.FramelessWindowHint)
        self.owner = owner
        self.setWindowTitle("Nexus Desktop AI Tray")
        self.setObjectName("nexusDesktopTrayPopup")
        self.setMinimumWidth(320)
        self._command_buttons = []
        self.setStyleSheet(
            "#nexusDesktopTrayPopup {"
            " background: #07111f;"
            " border: 1px solid #25636c;"
            " border-radius: 6px;"
            "}"
            "#nexusDesktopTrayIdentity {"
            " color: #f8fafc;"
            " font-size: 12px;"
            " min-height: 18px;"
            " padding: 7px 10px 2px 10px;"
            "}"
            "#nexusDesktopTrayStatus {"
            " background: #082f49;"
            " border: 1px solid #38bdf8;"
            " border-radius: 5px;"
            " color: #e0f2fe;"
            " font-size: 12px;"
            " margin: 2px 8px 7px 8px;"
            " min-height: 34px;"
            " padding: 6px 8px;"
            "}"
            "QPushButton {"
            " background: #0f172a;"
            " border: 1px solid transparent;"
            " border-radius: 5px;"
            " color: #f8fafc;"
            " min-height: 26px;"
            " padding: 5px 12px;"
            " text-align: left;"
            "}"
            "QPushButton:hover {"
            " background: #173b52;"
            " border-color: #38bdf8;"
            "}"
            "QPushButton:focus {"
            " border-color: #7dd3fc;"
            "}"
            "QPushButton:pressed {"
            " background: #0f766e;"
            "}"
            "QPushButton:disabled {"
            " background: #101827;"
            " border-color: #1f2937;"
            " color: #64748b;"
            "}"
            "QFrame {"
            " background: #244454;"
            " max-height: 1px;"
            " min-height: 1px;"
            "}"
        )
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(1)
        identity = QLabel(f"{TRAY_IDENTITY_LABEL} / {TRAY_ORIN_MARK_LABEL}", self)
        identity.setObjectName("nexusDesktopTrayIdentity")
        identity.setAccessibleName(TRAY_IDENTITY_LABEL)
        identity_font = QFont("Segoe UI")
        identity_font.setWeight(QFont.DemiBold)
        identity.setFont(identity_font)
        self.layout.addWidget(identity)
        self.resident_status_label = QLabel("", self)
        self.resident_status_label.setObjectName("nexusDesktopTrayStatus")
        self.resident_status_label.setAccessibleName("Resident access status")
        self.resident_status_label.setWordWrap(True)
        self.layout.addWidget(self.resident_status_label)
        self.add_separator()

    def add_separator(self):
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        self.layout.addWidget(line)
        return line

    def add_button(self, text, handler):
        button = QPushButton(text, self)
        button.setAccessibleName(text)
        button.setMinimumWidth(240)
        button.clicked.connect(lambda _checked=False: self.owner._invoke_button_action(handler))
        self._command_buttons.append((button, handler))
        self.layout.addWidget(button)
        return button

    def popup_at_cursor(self):
        self.adjustSize()
        pos = QCursor.pos()
        size = self.sizeHint()
        self.move(pos.x() - size.width(), pos.y() - size.height())
        self.show()
        self.raise_()
        self.activateWindow()

    def hideEvent(self, event):
        try:
            self.owner._handle_popup_hidden()
        finally:
            super().hideEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for button, handler in list(self._command_buttons):
                if (
                    button is not None
                    and button.isVisible()
                    and button.isEnabled()
                    and button.geometry().contains(event.pos())
                ):
                    self.owner._emit(
                        f"RENDERER_MAIN|TRAY_POPUP_BUTTON_RELEASE_ROUTED|action={button.text()}"
                    )
                    self.owner._invoke_button_action(handler)
                    event.accept()
                    return
        super().mouseReleaseEvent(event)


class DesktopTrayEntry:
    """Owns the Windows tray icon, menu state, and tray-to-runtime routing."""

    def __init__(self, app, window, event_logger=None, shutdown_confirmation_requester=None):
        self.app = app
        self.window = window
        self.event_logger = event_logger or (lambda _event: None)
        self.shutdown_confirmation_requester = (
            shutdown_confirmation_requester if callable(shutdown_confirmation_requester) else None
        )
        self.tray_icon = None
        self.tray_menu = None
        self.tray_popup = None
        self.identity_action = None
        self.ai_control_center_action = None
        self.open_overlay_action = None
        self.create_custom_task_action = None
        self.global_settings_action = None
        self.ai_status_action = None
        self.privacy_lockdown_action = None
        self.quick_slot_actions = []
        self.quick_slot_buttons = []
        self.quick_slot_route_ids = []
        self.monitoring_hud_primary_action = None
        self.monitoring_hud_dashboard_action = None
        self.monitoring_hud_unanchor_action = None
        self.exit_action = None
        self.monitoring_hud_primary_button = None
        self.monitoring_hud_dashboard_button = None
        self.monitoring_hud_unanchor_button = None
        self.monitoring_hud_status_label = None
        self.resident_status_label = None
        self.ai_control_center_button = None
        self.open_overlay_button = None
        self.create_custom_task_button = None
        self.global_settings_button = None
        self.ai_status_button = None
        self.privacy_lockdown_button = None
        self.exit_button = None
        self._discovery_cue_shown = False
        self._popup_guard_active = False

    def _emit(self, event):
        try:
            self.event_logger(event)
        except Exception:
            pass

    def initialize(self):
        self._emit("RENDERER_MAIN|TRAY_ENTRY_INITIALIZE_REQUESTED")
        try:
            tray_available = QSystemTrayIcon.isSystemTrayAvailable()

            if not tray_available:
                self._emit("RENDERER_MAIN|TRAY_ENTRY_READY|available=false")
                return False

            icon = build_resident_tray_icon()

            self.tray_menu = QMenu(TRAY_IDENTITY_LABEL)
            self.tray_menu.setTitle(TRAY_IDENTITY_LABEL)
            self.tray_menu.aboutToShow.connect(self._handle_menu_about_to_show)
            self.tray_menu.aboutToHide.connect(self._handle_menu_about_to_hide)
            self.identity_action = QAction(TRAY_IDENTITY_LABEL, self.tray_menu)
            self.identity_action.setEnabled(False)
            self.tray_menu.addAction(self.identity_action)
            self.tray_menu.addSeparator()

            self.monitoring_hud_primary_action = self._add_button_action(
                "Enable HUD Feature",
                self.request_monitoring_hud_toggle_from_tray,
            )
            self.monitoring_hud_dashboard_action = self._add_button_action(
                "Open HUD Dashboard",
                self.request_monitoring_hud_dashboard_from_tray,
            )
            self.monitoring_hud_unanchor_action = self._add_button_action(
                "HUD Overlay Deferred",
                self.request_monitoring_hud_unanchor_from_tray,
            )
            self.tray_menu.addSeparator()

            self.global_settings_action = self._add_button_action(
                "Global Settings",
                self.request_global_settings_from_tray,
            )
            self.ai_status_action = self._add_button_action(
                "AI Status / Command Center",
                self.request_ai_status_from_tray,
            )
            self.privacy_lockdown_action = self._add_button_action(
                "Privacy Lockdown",
                self.request_privacy_lockdown_from_tray,
            )
            self.tray_menu.addSeparator()

            for index in range(5):
                action = self._add_button_action(
                    f"Quick Access {index + 1}",
                    lambda source, slot_index=index: self.request_quick_slot_from_tray(slot_index, source),
                )
                self.quick_slot_actions.append(action)
            self.tray_menu.addSeparator()

            self.exit_action = self._add_button_action(
                "Exit Nexus Desktop AI",
                self.request_shutdown_from_tray,
            )
            self._initialize_popup()
            self.refresh_resident_access_actions("initialize")
            self.refresh_monitoring_hud_actions("initialize")

            self.tray_icon = QSystemTrayIcon(icon, self.app)
            self.tray_icon.setToolTip(TRAY_TOOLTIP_TEXT)
            self.tray_icon.activated.connect(self._handle_activation)
            self.tray_icon.show()
            self._emit("RENDERER_MAIN|TRAY_ENTRY_READY|available=true")
            self._emit(
                f"RENDERER_MAIN|TRAY_IDENTITY_READY|label={TRAY_IDENTITY_LABEL}|hidden_overflow_hint=true"
            )
            self._emit("RENDERER_MAIN|TRAY_RESIDENT_ACCESS_TRAY_ICON_READY|identity=ndai_orin|single_tray_icon=true")
            self._emit("RENDERER_MAIN|TRAY_ICON_SHOWN")
            return True
        except Exception as exc:
            self.close()
            self._emit(
                f"RENDERER_MAIN|TRAY_ENTRY_READY|available=false|reason={type(exc).__name__}"
            )
            return False

    def _initialize_popup(self):
        self.tray_popup = TrayCommandPopup(self)
        self.resident_status_label = self.tray_popup.resident_status_label
        self.monitoring_hud_status_label = QLabel("HUD Dashboard Closed", self.tray_popup)
        self.monitoring_hud_status_label.setAccessibleName("HUD Dashboard status")
        self.tray_popup.layout.addWidget(self.monitoring_hud_status_label)
        self.monitoring_hud_primary_button = self.tray_popup.add_button(
            "Enable HUD Feature",
            self.request_monitoring_hud_toggle_from_tray,
        )
        self.monitoring_hud_dashboard_button = self.tray_popup.add_button(
            "Open HUD Dashboard",
            self.request_monitoring_hud_dashboard_from_tray,
        )
        self.monitoring_hud_unanchor_button = self.tray_popup.add_button(
            "HUD Overlay Deferred",
            self.request_monitoring_hud_unanchor_from_tray,
        )
        self.tray_popup.add_separator()
        self.global_settings_button = self.tray_popup.add_button(
            "Global Settings",
            self.request_global_settings_from_tray,
        )
        self.ai_status_button = self.tray_popup.add_button(
            "AI Status / Command Center",
            self.request_ai_status_from_tray,
        )
        self.privacy_lockdown_button = self.tray_popup.add_button(
            "Privacy Lockdown",
            self.request_privacy_lockdown_from_tray,
        )
        self.tray_popup.add_separator()
        for index in range(5):
            button = self.tray_popup.add_button(
                f"Quick Access {index + 1}",
                lambda source, slot_index=index: self.request_quick_slot_from_tray(slot_index, source),
            )
            self.quick_slot_buttons.append(button)
        self.exit_button = self.tray_popup.add_button(
            "Exit Nexus Desktop AI",
            self.request_shutdown_from_tray,
        )

    def _add_button_action(self, text, handler):
        action = QWidgetAction(self.tray_menu)
        action.setText(text)
        button = QPushButton(text, self.tray_menu)
        button.setFlat(True)
        button.setMinimumHeight(24)
        button.setMinimumWidth(240)
        button.setAccessibleName(text)
        button.setStyleSheet(
            "QPushButton { text-align: left; padding: 4px 12px; border: none; }"
            "QPushButton:disabled { opacity: 0.55; }"
        )
        button.clicked.connect(lambda _checked=False: self._invoke_button_action(handler))
        action.setDefaultWidget(button)
        self.tray_menu.addAction(action)
        return action

    def _set_action_text(self, action, text):
        action.setText(text)
        widget = action.defaultWidget() if hasattr(action, "defaultWidget") else None
        if widget is not None:
            widget.setText(text)
            widget.setAccessibleName(text)

    def _set_button_text(self, button, text):
        if button is not None:
            button.setText(text)
            button.setAccessibleName(text)

    def _set_action_enabled(self, action, enabled):
        action.setEnabled(bool(enabled))
        widget = action.defaultWidget() if hasattr(action, "defaultWidget") else None
        if widget is not None:
            widget.setEnabled(bool(enabled))

    def _set_button_enabled(self, button, enabled):
        if button is not None:
            button.setEnabled(bool(enabled))

    def _set_action_visible(self, action, visible):
        action.setVisible(bool(visible))
        widget = action.defaultWidget() if hasattr(action, "defaultWidget") else None
        if widget is not None:
            widget.setVisible(bool(visible))

    def _set_button_visible(self, button, visible):
        if button is not None:
            button.setVisible(bool(visible))

    def _set_label_text_visible(self, label, text, visible):
        if label is not None:
            label.setText(text)
            label.setAccessibleName(text)
            label.setVisible(bool(visible))

    def _invoke_button_action(self, handler):
        if self.tray_popup is not None and self.tray_popup.isVisible():
            self.tray_popup.hide()
        if self.tray_menu is not None and self.tray_menu.isVisible():
            self.tray_menu.hide()
        handler("menu")

    def _handle_activation(self, reason):
        reason_name = getattr(reason, "name", str(reason))
        trigger_reason = QSystemTrayIcon.ActivationReason.Trigger
        double_click_reason = QSystemTrayIcon.ActivationReason.DoubleClick
        context_reason = getattr(QSystemTrayIcon.ActivationReason, "Context", None)
        if context_reason is not None and reason == context_reason:
            self._emit("RENDERER_MAIN|TRAY_CONTEXT_MENU_REQUESTED|source=tray_icon")
            self.refresh_monitoring_hud_actions("tray_context_activation")
            self._show_tray_popup()
            return
        if reason in (trigger_reason, double_click_reason):
            self.request_overlay_from_tray(f"activation_{reason_name}")
            return

        self._emit(f"RENDERER_MAIN|TRAY_ACTIVATION_IGNORED|reason={reason_name}")

    def _show_tray_popup(self):
        if self.tray_popup is None:
            return
        self._release_mouse_capture_for_tray_popup()
        self.refresh_resident_access_actions("tray_popup_about_to_show")
        self.refresh_monitoring_hud_actions("tray_popup_about_to_show")
        if self._show_native_tray_menu():
            self.refresh_resident_access_actions("tray_native_menu_closed")
            self.refresh_monitoring_hud_actions("tray_native_menu_closed")
            return
        self._popup_guard_active = True
        self.tray_popup.popup_at_cursor()

    def _show_native_tray_menu(self):
        if not hasattr(ctypes, "windll"):
            return False
        try:
            user32 = ctypes.windll.user32
            menu = user32.CreatePopupMenu()
            if not menu:
                return False

            MF_STRING = 0x0000
            MF_GRAYED = 0x0001
            MF_SEPARATOR = 0x0800
            TPM_RIGHTBUTTON = 0x0002
            TPM_RETURNCMD = 0x0100
            WM_NULL = 0x0000

            state = self._monitoring_hud_state()
            feature_enabled = bool(state.get("feature_enabled"))
            dashboard_visible = bool(state.get("dashboard_visible"))
            overlay_deferred = state.get("overlay_deferred", True) is not False
            overlay_anchor_enabled = bool(state.get("overlay_anchor_enabled")) and not overlay_deferred
            feature_text = "Disable HUD Feature" if feature_enabled else "Enable HUD Feature"
            dashboard_text = "Close HUD Dashboard" if dashboard_visible else "Open HUD Dashboard"
            resident_plan = self._resident_access_plan()
            quick_slots = list(resident_plan.get("quickSlots", ()) or [])

            def append(command_id, text, enabled=True):
                flags = MF_STRING if enabled else (MF_STRING | MF_GRAYED)
                user32.AppendMenuW(menu, flags, int(command_id), ctypes.c_wchar_p(text))

            append(80, self._native_menu_status_text(resident_plan), False)
            user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
            append(100, feature_text, True)
            if feature_enabled:
                append(101, dashboard_text, True)
            append(102, "HUD Overlay Deferred" if overlay_deferred else "Unanchor HUD Overlay", feature_enabled and overlay_anchor_enabled)
            user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
            append(110, "Global Settings", True)
            append(120, "AI Status / Command Center", True)
            append(130, "Privacy Lockdown", True)
            user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
            for index, route in enumerate(quick_slots[:5]):
                route_id = str(route.get("routeId", ""))
                append(
                    QUICK_SLOT_COMMAND_BASE_ID + index,
                    self._route_label_for_menu(route),
                    bool(route.get("enabled", True) or route_id in {"ai_status_command_center", "privacy_lockdown"}),
                )
            user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
            append(300, "Exit Nexus Desktop AI", True)

            pos = QCursor.pos()
            owner_hwnd = int(self.window.winId()) if hasattr(self.window, "winId") else 0
            if owner_hwnd:
                user32.SetForegroundWindow(ctypes.wintypes.HWND(owner_hwnd))
            self._emit("RENDERER_MAIN|TRAY_NATIVE_MENU_REQUESTED|source=tray_icon")
            command_id = user32.TrackPopupMenu(
                menu,
                TPM_RIGHTBUTTON | TPM_RETURNCMD,
                int(pos.x()),
                int(pos.y()),
                0,
                ctypes.wintypes.HWND(owner_hwnd),
                None,
            )
            if owner_hwnd:
                user32.PostMessageW(ctypes.wintypes.HWND(owner_hwnd), WM_NULL, 0, 0)
            user32.DestroyMenu(menu)
            if not command_id:
                self._emit("RENDERER_MAIN|TRAY_NATIVE_MENU_DISMISSED|source=tray_icon")
                return True
            self._dispatch_native_menu_command(int(command_id))
            return True
        except Exception as exc:
            self._emit(f"RENDERER_MAIN|TRAY_NATIVE_MENU_FAILED|reason={type(exc).__name__}")
            return False

    def _dispatch_native_menu_command(self, command_id):
        commands = {
            100: self.request_monitoring_hud_toggle_from_tray,
            101: self.request_monitoring_hud_dashboard_from_tray,
            102: self.request_monitoring_hud_unanchor_from_tray,
            110: self.request_global_settings_from_tray,
            120: self.request_ai_status_from_tray,
            130: self.request_privacy_lockdown_from_tray,
            300: self.request_shutdown_from_tray,
        }
        if QUICK_SLOT_COMMAND_BASE_ID <= command_id < QUICK_SLOT_COMMAND_BASE_ID + 5:
            slot_index = command_id - QUICK_SLOT_COMMAND_BASE_ID
            self._emit(f"RENDERER_MAIN|TRAY_NATIVE_MENU_QUICK_SLOT_SELECTED|slot={slot_index + 1}")
            self.request_quick_slot_from_tray(slot_index, "menu")
            return
        handler = commands.get(command_id)
        if handler is None:
            self._emit(f"RENDERER_MAIN|TRAY_NATIVE_MENU_COMMAND_IGNORED|command_id={command_id}")
            return
        self._emit(f"RENDERER_MAIN|TRAY_NATIVE_MENU_COMMAND_SELECTED|command_id={command_id}")
        handler("menu")

    def _release_mouse_capture_for_tray_popup(self):
        if not hasattr(ctypes, "windll"):
            return
        try:
            ctypes.windll.user32.ReleaseCapture()
            self._emit("RENDERER_MAIN|TRAY_MOUSE_CAPTURE_RELEASED|source=tray_context_activation")
        except Exception as exc:
            self._emit(
                f"RENDERER_MAIN|TRAY_MOUSE_CAPTURE_RELEASE_SKIPPED|reason={type(exc).__name__}"
            )

    def _handle_popup_hidden(self):
        if not self._popup_guard_active:
            return
        self._popup_guard_active = False
        self.refresh_monitoring_hud_actions("tray_popup_about_to_hide")

    def request_overlay_from_tray(self, source):
        visible_before = self._command_overlay_visible()
        next_visible = not visible_before
        self._emit(
            "RENDERER_MAIN|TRAY_ACTIVATION_REQUESTED"
            f"|source={source}|command_overlay_visible={str(visible_before).lower()}"
        )
        handler_name = "close_command_overlay" if visible_before else "open_command_overlay"
        handler = getattr(self.window, handler_name, None)
        if callable(handler):
            handler()
        else:
            self.window.toggle_command_overlay()
        self.refresh_resident_access_actions(source)
        self.refresh_monitoring_hud_actions(source)
        self._emit(
            "RENDERER_MAIN|TRAY_ACTIVATION_ROUTED_TO_OVERLAY"
            f"|source={source}|next_visible={str(next_visible).lower()}"
        )

    def request_create_custom_task_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_CREATE_CUSTOM_TASK_REQUESTED|source={source}")
        self.window.request_create_custom_task_from_tray(source=source)
        self.refresh_resident_access_actions(source)

    def request_global_settings_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_GLOBAL_SETTINGS_REQUESTED|source={source}")
        handler = getattr(self.window, "open_resident_access_settings", None)
        if callable(handler):
            handler(source=source, focus="quick_access")
            self._emit(f"RENDERER_MAIN|TRAY_GLOBAL_SETTINGS_ROUTED|source={source}|focus=quick_access")
        else:
            self._emit(f"RENDERER_MAIN|TRAY_GLOBAL_SETTINGS_UNAVAILABLE|source={source}|reason=handler_unavailable")
        self.refresh_resident_access_actions(source)

    def request_ai_status_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_AI_STATUS_REQUESTED|source={source}")
        command_center_handler = getattr(self.window, "show_ai_control_center_from_tray", None)
        if callable(command_center_handler):
            result = command_center_handler(source=source)
            if isinstance(result, dict):
                route_visible = bool(
                    result.get("shown")
                    or result.get("visible")
                    or (result.get("qtVisible") and result.get("nativeVisible"))
                )
                route_reason = str(result.get("reason") or "route_not_visible")
            else:
                route_visible = result is True
                route_reason = "route_not_visible"
            if route_visible:
                self._emit(
                    "RENDERER_MAIN|TRAY_AI_STATUS_COMMAND_CENTER_ROUTED"
                    f"|source={source}|owner=FAM-007|route=fam007-ai-control-center"
                    "|provider_visible_data=none|provider_execution=blocked"
                )
                self.refresh_resident_access_actions(source)
                return
            self._emit(
                "RENDERER_MAIN|TRAY_AI_STATUS_COMMAND_CENTER_UNAVAILABLE"
                f"|source={source}|reason={route_reason}"
            )

        handler = getattr(self.window, "request_ai_status_from_resident_access", None)
        if callable(handler):
            handler(source=source)
            self._emit(f"RENDERER_MAIN|TRAY_AI_STATUS_ROUTED|source={source}|route_only=true")
        else:
            settings_handler = getattr(self.window, "open_resident_access_settings", None)
            if callable(settings_handler):
                settings_handler(source=source, focus="ai_status")
                self._emit(f"RENDERER_MAIN|TRAY_AI_STATUS_ROUTED|source={source}|focus=ai_status")
            else:
                self._emit(f"RENDERER_MAIN|TRAY_AI_STATUS_UNAVAILABLE|source={source}|reason=handler_unavailable")
        self.refresh_resident_access_actions(source)

    def request_privacy_lockdown_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_PRIVACY_LOCKDOWN_REQUESTED|source={source}")
        handler = getattr(self.window, "request_privacy_lockdown_from_resident_access", None)
        if callable(handler):
            handler(source=source)
            self._emit(f"RENDERER_MAIN|TRAY_PRIVACY_LOCKDOWN_ROUTED|source={source}|route_only=true")
        else:
            settings_handler = getattr(self.window, "open_resident_access_settings", None)
            if callable(settings_handler):
                settings_handler(source=source, focus="privacy")
                self._emit(f"RENDERER_MAIN|TRAY_PRIVACY_LOCKDOWN_ROUTED|source={source}|focus=privacy")
            else:
                self._emit(f"RENDERER_MAIN|TRAY_PRIVACY_LOCKDOWN_UNAVAILABLE|source={source}|reason=handler_unavailable")
        self.refresh_resident_access_actions(source)

    def request_quick_slot_from_tray(self, slot_index, source):
        try:
            index = int(slot_index)
        except (TypeError, ValueError):
            index = -1
        if index < 0 or index >= len(self.quick_slot_route_ids):
            self._emit(
                f"RENDERER_MAIN|TRAY_QUICK_SLOT_IGNORED|source={source}|slot={index + 1}|reason=slot_unavailable"
            )
            return
        route_id = self.quick_slot_route_ids[index]
        self._emit(
            f"RENDERER_MAIN|TRAY_QUICK_SLOT_REQUESTED|source={source}|slot={index + 1}|route_id={route_id}"
        )
        if route_id == "command_overlay":
            self.request_overlay_from_tray(source)
            return
        if route_id == "create_custom_task":
            self.request_create_custom_task_from_tray(source)
            return
        handler = getattr(self.window, "request_resident_quick_action_from_tray", None)
        if callable(handler):
            handler(route_id=route_id, source=source)
            self._emit(
                f"RENDERER_MAIN|TRAY_QUICK_SLOT_ROUTED|source={source}|slot={index + 1}|route_id={route_id}"
            )
        else:
            self._emit(
                f"RENDERER_MAIN|TRAY_QUICK_SLOT_UNAVAILABLE|source={source}|slot={index + 1}|route_id={route_id}|reason=handler_unavailable"
            )
        self.refresh_resident_access_actions(source)

    def request_ai_control_center_from_tray(self, source):
        self._emit(
            "RENDERER_MAIN|TRAY_AI_CONTROL_CENTER_REQUESTED"
            f"|source={source}|carry_in=f3-ff01-narrow-doorway|owner=FAM-007"
        )
        handler = getattr(self.window, "show_ai_control_center_from_tray", None)
        if not callable(handler):
            self._emit(
                f"RENDERER_MAIN|TRAY_AI_CONTROL_CENTER_ABORTED|source={source}|reason=handler_unavailable"
            )
            return
        result = handler(source=source)
        if isinstance(result, dict):
            route_visible = bool(
                result.get("shown")
                or result.get("visible")
                or (result.get("qtVisible") and result.get("nativeVisible"))
            )
            route_reason = result.get("reason", "route_not_visible")
        else:
            route_visible = result is True
            route_reason = "route_not_visible"
        if not route_visible:
            self._emit(
                "RENDERER_MAIN|TRAY_AI_CONTROL_CENTER_ABORTED"
                f"|source={source}|reason={route_reason}"
            )
            return
        self._emit(
            "RENDERER_MAIN|TRAY_AI_CONTROL_CENTER_ROUTED"
            f"|source={source}|provider_visible_data=none|provider_execution=blocked"
        )

    def _monitoring_hud_state(self):
        provider = getattr(self.window, "monitoring_hud_feature_state", None)
        if callable(provider):
            try:
                state = provider()
                if isinstance(state, dict):
                    return state
            except Exception:
                pass
        return {
            "feature_enabled": False,
            "dashboard_visible": False,
            "overlay_deferred": True,
            "overlay_anchor_enabled": False,
        }

    def _command_overlay_state(self):
        provider = getattr(self.window, "command_overlay_state", None)
        if callable(provider):
            try:
                state = provider()
                if isinstance(state, dict):
                    return state
            except Exception:
                pass
        return {"visible": False, "phase": "closed"}

    def _command_overlay_visible(self):
        return bool(self._command_overlay_state().get("visible"))

    def _command_overlay_action_text(self):
        return "Close Command Overlay" if self._command_overlay_visible() else "Open Command Overlay"

    def _resident_access_plan(self):
        provider = getattr(self.window, "resident_access_status_snapshot", None)
        if callable(provider):
            try:
                plan = provider()
                if isinstance(plan, dict):
                    return plan
            except Exception:
                pass
        return build_resident_access_menu_plan(
            monitoring_hud_state=self._monitoring_hud_state(),
            command_overlay_state=self._command_overlay_state(),
        )

    def _route_label_for_menu(self, route):
        route_id = str(route.get("routeId", "") if isinstance(route, dict) else "")
        if route_id == "command_overlay":
            return self._command_overlay_action_text()
        return str(route.get("label", "Quick Access") if isinstance(route, dict) else "Quick Access")

    def _native_menu_status_text(self, plan):
        status = str(plan.get("statusLabel") if isinstance(plan, dict) else "").strip()
        if not status:
            status = "AI local/no provider; Provider-visible data: none"
        return f"{TRAY_IDENTITY_LABEL} - {status.rstrip('.')}"

    def refresh_resident_access_actions(self, source="runtime"):
        if not self.quick_slot_actions and not self.quick_slot_buttons:
            return

        plan = self._resident_access_plan()
        status_label = str(plan.get("statusLabel") or "Ready - AI local/no provider")
        if self.identity_action is not None:
            self._set_action_text(self.identity_action, self._native_menu_status_text(plan))
        if self.resident_status_label is not None:
            self.resident_status_label.setText(status_label)
            self.resident_status_label.setAccessibleName(status_label)
            self.resident_status_label.setVisible(True)

        if self.tray_icon is not None:
            self.tray_icon.setToolTip(str(plan.get("tooltipText") or TRAY_TOOLTIP_TEXT))

        quick_slots = list(plan.get("quickSlots", ()) or [])
        self.quick_slot_route_ids = [
            str(route.get("routeId", "") if isinstance(route, dict) else "")
            for route in quick_slots[:5]
        ]
        self.open_overlay_action = None
        self.open_overlay_button = None
        self.create_custom_task_action = None
        self.create_custom_task_button = None

        for index in range(5):
            route = quick_slots[index] if index < len(quick_slots) else None
            visible = route is not None
            label = self._route_label_for_menu(route) if route is not None else ""
            enabled = bool(route.get("enabled", True)) if isinstance(route, dict) else False
            action = self.quick_slot_actions[index] if index < len(self.quick_slot_actions) else None
            button = self.quick_slot_buttons[index] if index < len(self.quick_slot_buttons) else None
            if action is not None:
                self._set_action_text(action, label)
                self._set_action_visible(action, visible)
                self._set_action_enabled(action, enabled)
            if button is not None:
                self._set_button_text(button, label)
                self._set_button_visible(button, visible)
                self._set_button_enabled(button, enabled)
            route_id = self.quick_slot_route_ids[index] if index < len(self.quick_slot_route_ids) else ""
            if route_id == "command_overlay":
                self.open_overlay_action = action
                self.open_overlay_button = button
            elif route_id == "create_custom_task":
                self.create_custom_task_action = action
                self.create_custom_task_button = button

        menu_budget = plan.get("menuBudget") if isinstance(plan.get("menuBudget"), dict) else {}
        current_slots = menu_budget.get("currentQuickSlots", len(self.quick_slot_route_ids))
        maximum_slots = menu_budget.get("maximumQuickSlots", 5)
        ai_privacy = plan.get("aiPrivacy") if isinstance(plan.get("aiPrivacy"), dict) else {}
        self._emit(
            "RENDERER_MAIN|TRAY_RESIDENT_ACCESS_ACTIONS_REFRESHED"
            f"|source={source}"
            f"|quick_slot_count={current_slots}"
            f"|max_quick_slots={maximum_slots}"
            f"|provider_visible_data={str(ai_privacy.get('providerVisibleDataLabel', 'Provider-visible data: none')).replace('|', '/')}"
            "|single_tray_icon=true"
        )

    def refresh_monitoring_hud_actions(self, source="runtime"):
        if (
            self.monitoring_hud_primary_action is None
            or self.monitoring_hud_dashboard_action is None
            or self.monitoring_hud_unanchor_action is None
        ):
            return
        state = self._monitoring_hud_state()
        feature_enabled = bool(state.get("feature_enabled"))
        dashboard_visible = bool(state.get("dashboard_visible"))
        overlay_deferred = state.get("overlay_deferred", True) is not False
        overlay_anchor_enabled = bool(state.get("overlay_anchor_enabled")) and not overlay_deferred
        open_enabled = feature_enabled and not dashboard_visible
        close_enabled = feature_enabled and dashboard_visible
        command_overlay_visible = self._command_overlay_visible()
        command_overlay_text = "Close Command Overlay" if command_overlay_visible else "Open Command Overlay"

        if not feature_enabled:
            self._set_action_text(self.monitoring_hud_primary_action, "Enable HUD Feature")
            self._set_button_text(self.monitoring_hud_primary_button, "Enable HUD Feature")
            self._set_action_text(self.monitoring_hud_dashboard_action, "Open HUD Dashboard")
            self._set_button_text(self.monitoring_hud_dashboard_button, "Open HUD Dashboard")
            self._set_label_text_visible(
                self.monitoring_hud_status_label,
                "HUD Dashboard Closed",
                False,
            )
        elif dashboard_visible:
            self._set_action_text(self.monitoring_hud_primary_action, "Disable HUD Feature")
            self._set_button_text(self.monitoring_hud_primary_button, "Disable HUD Feature")
            self._set_action_text(self.monitoring_hud_dashboard_action, "Close HUD Dashboard")
            self._set_button_text(self.monitoring_hud_dashboard_button, "Close HUD Dashboard")
            self._set_label_text_visible(
                self.monitoring_hud_status_label,
                "HUD Dashboard Open",
                True,
            )
        else:
            self._set_action_text(self.monitoring_hud_primary_action, "Disable HUD Feature")
            self._set_button_text(self.monitoring_hud_primary_button, "Disable HUD Feature")
            self._set_action_text(self.monitoring_hud_dashboard_action, "Open HUD Dashboard")
            self._set_button_text(self.monitoring_hud_dashboard_button, "Open HUD Dashboard")
            self._set_label_text_visible(
                self.monitoring_hud_status_label,
                "HUD Dashboard Closed",
                True,
            )
        self._set_action_enabled(self.monitoring_hud_primary_action, True)
        self._set_button_enabled(self.monitoring_hud_primary_button, True)
        self._set_action_visible(self.monitoring_hud_dashboard_action, feature_enabled)
        self._set_action_enabled(self.monitoring_hud_dashboard_action, feature_enabled)
        self._set_button_visible(self.monitoring_hud_dashboard_button, feature_enabled)
        self._set_button_enabled(self.monitoring_hud_dashboard_button, feature_enabled)
        self._set_action_text(
            self.monitoring_hud_unanchor_action,
            "HUD Overlay Deferred" if overlay_deferred else "Unanchor HUD Overlay",
        )
        self._set_button_text(
            self.monitoring_hud_unanchor_button,
            "HUD Overlay Deferred" if overlay_deferred else "Unanchor HUD Overlay",
        )
        self._set_action_enabled(
            self.monitoring_hud_unanchor_action,
            feature_enabled and overlay_anchor_enabled,
        )
        self._set_button_enabled(
            self.monitoring_hud_unanchor_button,
            feature_enabled and overlay_anchor_enabled,
        )
        if self.open_overlay_action is not None:
            self._set_action_text(self.open_overlay_action, command_overlay_text)
        self._set_button_text(self.open_overlay_button, command_overlay_text)
        self._emit(
            "RENDERER_MAIN|TRAY_MONITORING_HUD_ACTIONS_REFRESHED"
            f"|source={source}"
            f"|feature_enabled={str(feature_enabled).lower()}"
            f"|dashboard_visible={str(dashboard_visible).lower()}"
            f"|dashboard_action_enabled={str((open_enabled or close_enabled)).lower()}"
            f"|dashboard_open_action_enabled={str(open_enabled).lower()}"
            f"|dashboard_close_action_enabled={str(close_enabled).lower()}"
            f"|overlay_deferred={str(overlay_deferred).lower()}"
            f"|overlay_anchor_enabled={str(overlay_anchor_enabled).lower()}"
            f"|command_overlay_visible={str(command_overlay_visible).lower()}"
            f"|command_overlay_action={'close' if command_overlay_visible else 'open'}"
        )

    def _handle_menu_about_to_show(self):
        guard = getattr(self.window, "set_monitoring_hud_tray_menu_interaction_guard", None)
        if callable(guard):
            guard(True, source="tray_menu_about_to_show")
        self.refresh_resident_access_actions("tray_menu_about_to_show")
        self.refresh_monitoring_hud_actions("tray_menu_about_to_show")

    def _handle_menu_about_to_hide(self):
        guard = getattr(self.window, "set_monitoring_hud_tray_menu_interaction_guard", None)
        if callable(guard):
            QTimer.singleShot(80, lambda: guard(False, source="tray_menu_about_to_hide"))

    def request_monitoring_hud_toggle_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_MONITORING_HUD_TOGGLE_REQUESTED|source={source}")
        self.window.request_monitoring_hud_toggle_from_tray(source=source)
        self.refresh_resident_access_actions(source)
        self.refresh_monitoring_hud_actions(source)

    def request_monitoring_hud_primary_from_tray(self, source):
        state = self._monitoring_hud_state()
        feature_enabled = bool(state.get("feature_enabled"))
        dashboard_visible = bool(state.get("dashboard_visible"))
        if not feature_enabled:
            self.request_monitoring_hud_toggle_from_tray(source)
            return
        self.request_monitoring_hud_dashboard_from_tray(source, visible=not dashboard_visible)

    def request_monitoring_hud_dashboard_from_tray(self, source, visible=None):
        state = self._monitoring_hud_state()
        feature_enabled = bool(state.get("feature_enabled"))
        dashboard_visible = bool(state.get("dashboard_visible"))
        if not feature_enabled:
            self._emit(
                f"RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_ABORTED|source={source}|reason=feature_disabled"
            )
            self.refresh_resident_access_actions(source)
            self.refresh_monitoring_hud_actions(source)
            return
        next_visible = (not dashboard_visible) if visible is None else bool(visible)
        self._emit(
            "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_REQUESTED"
            f"|source={source}|visible={str(next_visible).lower()}"
        )
        handler = getattr(self.window, "request_monitoring_hud_dashboard_from_tray", None)
        if not callable(handler):
            self._emit(
                f"RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_ABORTED|source={source}|reason=handler_unavailable"
            )
            return
        handler(source=source, visible=next_visible)
        self.refresh_resident_access_actions(source)
        self.refresh_monitoring_hud_actions(source)

    def request_monitoring_hud_unanchor_from_tray(self, source):
        state = self._monitoring_hud_state()
        if state.get("overlay_deferred", True) is not False:
            self._emit(
                f"RENDERER_MAIN|TRAY_MONITORING_HUD_UNANCHOR_DEFERRED|source={source}|reason=overlay_deferred"
            )
            return
        self._emit(f"RENDERER_MAIN|TRAY_MONITORING_HUD_UNANCHOR_REQUESTED|source={source}")
        self.window.request_monitoring_hud_unanchor_from_tray(source=source)
        self.refresh_resident_access_actions(source)
        self.refresh_monitoring_hud_actions(source)

    def request_shutdown_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_SHUTDOWN_CONFIRMATION_REQUESTED|source={source}")
        if self.shutdown_confirmation_requester is None:
            self._emit(
                f"RENDERER_MAIN|TRAY_SHUTDOWN_CONFIRMATION_UNAVAILABLE|source={source}"
            )
            return
        self.shutdown_confirmation_requester(f"tray_{source}")

    def show_discovery_cue(self):
        if self.tray_icon is None:
            self._emit("RENDERER_MAIN|TRAY_DISCOVERY_CUE_SKIPPED|reason=tray_unavailable")
            return False

        if self._discovery_cue_shown:
            self._emit("RENDERER_MAIN|TRAY_DISCOVERY_CUE_SKIPPED|reason=already_shown")
            return False

        self._discovery_cue_shown = True
        try:
            supports_messages = QSystemTrayIcon.supportsMessages()
        except Exception:
            supports_messages = True

        if not supports_messages:
            self._emit("RENDERER_MAIN|TRAY_DISCOVERY_CUE_SKIPPED|reason=messages_unavailable")
            return False

        try:
            message_icon = getattr(getattr(QSystemTrayIcon, "MessageIcon", object), "Information", None)
            if message_icon is None:
                message_icon = getattr(QSystemTrayIcon, "Information", 1)
            self.tray_icon.showMessage(
                TRAY_IDENTITY_LABEL,
                TRAY_DISCOVERY_MESSAGE,
                message_icon,
                TRAY_DISCOVERY_DURATION_MS,
            )
            self._emit("RENDERER_MAIN|TRAY_DISCOVERY_CUE_REQUESTED|hidden_overflow_hint=true")
            return True
        except Exception as exc:
            self._emit(
                f"RENDERER_MAIN|TRAY_DISCOVERY_CUE_FAILED|reason={type(exc).__name__}"
            )
            return False

    def close(self):
        if self.tray_icon is None:
            return

        try:
            self.tray_icon.hide()
            self._emit("RENDERER_MAIN|TRAY_ICON_HIDDEN")
        except Exception as exc:
            self._emit(f"RENDERER_MAIN|TRAY_ICON_HIDE_FAILED|reason={type(exc).__name__}")
        finally:
            self.tray_icon = None
