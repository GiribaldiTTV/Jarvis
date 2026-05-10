import ctypes
import ctypes.wintypes

from PySide6.QtGui import QAction, QCursor
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMenu,
    QPushButton,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)


TRAY_IDENTITY_LABEL = "Nexus Desktop AI"
TRAY_DISCOVERY_MESSAGE = (
    "Nexus Desktop AI is running in the Windows notification area. "
    "If you do not see the icon, open hidden icons (^)."
)
TRAY_DISCOVERY_DURATION_MS = 4500


class TrayCommandPopup(QWidget):
    """Small user-facing tray menu surface with real button hit targets."""

    def __init__(self, owner):
        super().__init__(None, Qt.Popup | Qt.FramelessWindowHint)
        self.owner = owner
        self.setWindowTitle("Nexus Desktop AI Tray")
        self.setObjectName("nexusDesktopTrayPopup")
        self._command_buttons = []
        self.setStyleSheet(
            "#nexusDesktopTrayPopup {"
            " background: #ffffff;"
            " border: 1px solid #bababa;"
            "}"
            "QLabel {"
            " color: #202124;"
            " padding: 5px 10px;"
            "}"
            "QPushButton {"
            " background: transparent;"
            " border: none;"
            " color: #202124;"
            " min-height: 24px;"
            " padding: 4px 12px;"
            " text-align: left;"
            "}"
            "QPushButton:hover {"
            " background: #e8f0fe;"
            "}"
            "QPushButton:disabled {"
            " color: #8a8f98;"
            "}"
            "QFrame {"
            " background: #d7d7d7;"
            " max-height: 1px;"
            " min-height: 1px;"
            "}"
        )
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(1)
        identity = QLabel(TRAY_IDENTITY_LABEL, self)
        identity.setAccessibleName(TRAY_IDENTITY_LABEL)
        self.layout.addWidget(identity)
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
        button.setMinimumWidth(170)
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
        self.open_overlay_action = None
        self.create_custom_task_action = None
        self.monitoring_hud_primary_action = None
        self.monitoring_hud_disable_action = None
        self.monitoring_hud_unanchor_action = None
        self.exit_action = None
        self.monitoring_hud_primary_button = None
        self.monitoring_hud_disable_button = None
        self.monitoring_hud_unanchor_button = None
        self.monitoring_hud_status_label = None
        self.open_overlay_button = None
        self.create_custom_task_button = None
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

            icon = self.app.windowIcon()
            if icon.isNull():
                icon = self.app.style().standardIcon(QStyle.SP_ComputerIcon)

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
                self.request_monitoring_hud_primary_from_tray,
            )
            self.monitoring_hud_disable_action = self._add_button_action(
                "Disable HUD Feature",
                self.request_monitoring_hud_toggle_from_tray,
            )
            self.monitoring_hud_unanchor_action = self._add_button_action(
                "HUD Overlay Deferred",
                self.request_monitoring_hud_unanchor_from_tray,
            )
            self.tray_menu.addSeparator()

            self.open_overlay_action = self._add_button_action(
                "Open Command Overlay",
                self.request_overlay_from_tray,
            )
            self.create_custom_task_action = self._add_button_action(
                "Create Custom Task",
                self.request_create_custom_task_from_tray,
            )
            self.tray_menu.addSeparator()

            self.exit_action = self._add_button_action(
                "Exit Nexus Desktop AI",
                self.request_shutdown_from_tray,
            )
            self._initialize_popup()
            self.refresh_monitoring_hud_actions("initialize")

            self.tray_icon = QSystemTrayIcon(icon, self.app)
            self.tray_icon.setToolTip(TRAY_IDENTITY_LABEL)
            self.tray_icon.activated.connect(self._handle_activation)
            self.tray_icon.show()
            self._emit("RENDERER_MAIN|TRAY_ENTRY_READY|available=true")
            self._emit(
                f"RENDERER_MAIN|TRAY_IDENTITY_READY|label={TRAY_IDENTITY_LABEL}|hidden_overflow_hint=true"
            )
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
        self.monitoring_hud_status_label = QLabel("HUD Dashboard Closed", self.tray_popup)
        self.monitoring_hud_status_label.setAccessibleName("HUD Dashboard status")
        self.tray_popup.layout.addWidget(self.monitoring_hud_status_label)
        self.monitoring_hud_primary_button = self.tray_popup.add_button(
            "Enable HUD Feature",
            self.request_monitoring_hud_primary_from_tray,
        )
        self.monitoring_hud_disable_button = self.tray_popup.add_button(
            "Disable HUD Feature",
            self.request_monitoring_hud_toggle_from_tray,
        )
        self.monitoring_hud_unanchor_button = self.tray_popup.add_button(
            "HUD Overlay Deferred",
            self.request_monitoring_hud_unanchor_from_tray,
        )
        self.tray_popup.add_separator()
        self.open_overlay_button = self.tray_popup.add_button(
            "Open Command Overlay",
            self.request_overlay_from_tray,
        )
        self.create_custom_task_button = self.tray_popup.add_button(
            "Create Custom Task",
            self.request_create_custom_task_from_tray,
        )
        self.tray_popup.add_separator()
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
        button.setMinimumWidth(150)
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
        self.refresh_monitoring_hud_actions("tray_popup_about_to_show")
        if self._show_native_tray_menu():
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
            primary_text = (
                "Enable HUD Feature"
                if not feature_enabled
                else "Close HUD Dashboard" if dashboard_visible else "Open HUD Dashboard"
            )

            def append(command_id, text, enabled=True):
                flags = MF_STRING if enabled else (MF_STRING | MF_GRAYED)
                user32.AppendMenuW(menu, flags, int(command_id), ctypes.c_wchar_p(text))

            append(100, primary_text, True)
            if feature_enabled:
                append(101, "Disable HUD Feature", True)
            append(102, "HUD Overlay Deferred" if overlay_deferred else "Unanchor HUD Overlay", feature_enabled and overlay_anchor_enabled)
            user32.AppendMenuW(menu, MF_SEPARATOR, 0, None)
            append(200, "Open Command Overlay", True)
            append(201, "Create Custom Task", True)
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
            100: self.request_monitoring_hud_primary_from_tray,
            101: self.request_monitoring_hud_toggle_from_tray,
            102: self.request_monitoring_hud_unanchor_from_tray,
            200: self.request_overlay_from_tray,
            201: self.request_create_custom_task_from_tray,
            300: self.request_shutdown_from_tray,
        }
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
        self._emit(f"RENDERER_MAIN|TRAY_ACTIVATION_REQUESTED|source={source}")
        self.window.toggle_command_overlay()
        self._emit(f"RENDERER_MAIN|TRAY_ACTIVATION_ROUTED_TO_OVERLAY|source={source}")

    def request_create_custom_task_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_CREATE_CUSTOM_TASK_REQUESTED|source={source}")
        self.window.request_create_custom_task_from_tray(source=source)

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

    def refresh_monitoring_hud_actions(self, source="runtime"):
        if (
            self.monitoring_hud_primary_action is None
            or self.monitoring_hud_disable_action is None
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

        if not feature_enabled:
            self._set_action_text(self.monitoring_hud_primary_action, "Enable HUD Feature")
            self._set_button_text(self.monitoring_hud_primary_button, "Enable HUD Feature")
            self._set_label_text_visible(
                self.monitoring_hud_status_label,
                "HUD Dashboard Closed",
                False,
            )
        elif dashboard_visible:
            self._set_action_text(self.monitoring_hud_primary_action, "Close HUD Dashboard")
            self._set_button_text(self.monitoring_hud_primary_button, "Close HUD Dashboard")
            self._set_label_text_visible(
                self.monitoring_hud_status_label,
                "HUD Dashboard Open",
                True,
            )
        else:
            self._set_action_text(self.monitoring_hud_primary_action, "Open HUD Dashboard")
            self._set_button_text(self.monitoring_hud_primary_button, "Open HUD Dashboard")
            self._set_label_text_visible(
                self.monitoring_hud_status_label,
                "HUD Dashboard Closed",
                True,
            )
        self._set_action_enabled(self.monitoring_hud_primary_action, True)
        self._set_button_enabled(self.monitoring_hud_primary_button, True)
        self._set_action_visible(self.monitoring_hud_disable_action, feature_enabled)
        self._set_action_enabled(self.monitoring_hud_disable_action, feature_enabled)
        self._set_button_visible(self.monitoring_hud_disable_button, feature_enabled)
        self._set_button_enabled(self.monitoring_hud_disable_button, feature_enabled)
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
        )

    def _handle_menu_about_to_show(self):
        guard = getattr(self.window, "set_monitoring_hud_tray_menu_interaction_guard", None)
        if callable(guard):
            guard(True, source="tray_menu_about_to_show")
        self.refresh_monitoring_hud_actions("tray_menu_about_to_show")

    def _handle_menu_about_to_hide(self):
        guard = getattr(self.window, "set_monitoring_hud_tray_menu_interaction_guard", None)
        if callable(guard):
            QTimer.singleShot(80, lambda: guard(False, source="tray_menu_about_to_hide"))

    def request_monitoring_hud_toggle_from_tray(self, source):
        self._emit(f"RENDERER_MAIN|TRAY_MONITORING_HUD_TOGGLE_REQUESTED|source={source}")
        self.window.request_monitoring_hud_toggle_from_tray(source=source)
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
