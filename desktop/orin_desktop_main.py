import os
import sys
import ctypes
import ctypes.wintypes
import datetime
import json
import threading
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PySide6.QtGui import QCursor
from PySide6.QtCore import QObject, QTimer, Qt, Signal, Slot, QPoint
from PySide6.QtWidgets import QApplication, QMessageBox

from desktop.core_visualization_renderer import CoreVisualizationWindow
from desktop.hotkeys import ShutdownBus, GlobalHotkeyManager
from desktop.monitoring_hud_access import MonitoringHudAccessAdapter
from desktop.monitoring_hud_state import load_monitoring_hud_state
from desktop.resident_access import build_resident_access_menu_plan
from desktop.single_instance import NamedSignal
from desktop.tray_controller import DesktopTrayEntry, TRAY_IDENTITY_LABEL, build_resident_tray_icon

try:
    from desktop.desktop_renderer import DesktopRuntimeWindow
    DESKTOP_RUNTIME_IMPORT_ERROR = None
except Exception as exc:
    DesktopRuntimeWindow = None
    DESKTOP_RUNTIME_IMPORT_ERROR = exc

RUNTIME_LOG_FILE = ""
STARTUP_ABORT_SIGNAL_FILE = ""
MONITORING_HUD_LIVE_SELF_QA_MANIFEST = ""
MONITORING_HUD_LIVE_SELF_QA_ROOT = ""
MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS = 250
MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS = 0
MONITORING_HUD_LIVE_SELF_QA_LANE = "full"
RUNTIME_RELAUNCH_EVENT = r"Local\NexusRuntimeRelaunchRequestV1"
RUNTIME_DESKTOP_SETTLED_EVENT = r"Local\NexusRuntimeDesktopSettledV1"
AUTHORITATIVE_DESKTOP_SETTLED_MARKER = "DESKTOP_OUTCOME|SETTLED|state=dormant"
MONITORING_HUD_STARTUP_ENV = "NEXUS_MONITORING_HUD_STARTUP_ENABLED"
MONITORING_HUD_LIVE_SELF_QA_MANIFEST_ENV = "NEXUS_MONITORING_HUD_LIVE_SELF_QA_MANIFEST"
MONITORING_HUD_LIVE_SELF_QA_ROOT_ENV = "NEXUS_MONITORING_HUD_LIVE_SELF_QA_ROOT"
MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS_ENV = "NEXUS_MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS"
MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS_ENV = "NEXUS_MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS"
MONITORING_HUD_LIVE_SELF_QA_LANE_ENV = "NEXUS_MONITORING_HUD_LIVE_SELF_QA_LANE"
SHUTDOWN_CONFIRMATION_DECISION_ENV = "NEXUS_SHUTDOWN_CONFIRMATION_DECISION"
SHUTDOWN_CONFIRMATION_TIMEOUT_ENV = "NEXUS_SHUTDOWN_CONFIRMATION_TIMEOUT_MS"
REAL_CLIENT_TRAY_PRECHECK_MANIFEST_ENV = "NEXUS_MONITORING_HUD_REAL_CLIENT_TRAY_PRECHECK_MANIFEST"
REAL_CLIENT_TRAY_PRECHECK_EXIT_ENV = "NEXUS_MONITORING_HUD_REAL_CLIENT_TRAY_PRECHECK_EXIT"
FAM003_SETTINGS_LIVE_RESIZE_MANIFEST_ENV = "NEXUS_FAM003_SETTINGS_LIVE_RESIZE_MANIFEST"
FAM003_SETTINGS_LIVE_RESIZE_EXIT_ENV = "NEXUS_FAM003_SETTINGS_LIVE_RESIZE_EXIT"
FAM003_LV_VISIBLE_INPUT_MANIFEST_ENV = "NEXUS_FAM003_LV_VISIBLE_INPUT_MANIFEST"
FAM003_LV_VISIBLE_INPUT_EXIT_ENV = "NEXUS_FAM003_LV_VISIBLE_INPUT_EXIT"
DESKTOP_VALIDATION_SHORTCUT_ENV = "NEXUS_DESKTOP_VALIDATION_SHORTCUT_PATH"
SHUTDOWN_CONFIRMATION_ACCEPTED = "accepted"
SHUTDOWN_CONFIRMATION_CANCELLED = "cancelled"
SHUTDOWN_CONFIRMATION_TIMEOUT = "timeout"
SHUTDOWN_CONFIRMATION_DEFAULT_TIMEOUT_MS = 15000


class ShutdownConfirmationDispatcher(QObject):
    def __init__(self, handler, parent=None):
        super().__init__(parent)
        self._handler = handler

    @Slot(str)
    def request(self, source="hotkey"):
        self._handler(source)


class DesktopRuntimeUnavailable(QObject):
    core_visualization_visible = Signal()

    def __init__(self, event_logger=None, reason="desktop runtime unavailable"):
        super().__init__()
        self.event_logger = event_logger or (lambda _event: None)
        self.reason = str(reason or "desktop runtime unavailable")
        self._monitoring_hud_access_adapter = MonitoringHudAccessAdapter(
            query_state=self.monitoring_hud_feature_state,
            persist_enabled=lambda _enabled, _source: False,
            open_or_restore_dashboard=lambda _source: False,
            close_dashboard=lambda _source: False,
            event_logger=self._emit,
        )
        self._emit("RENDERER_MAIN|DESKTOP_RUNTIME_UNAVAILABLE|reason=" + self.reason.replace("|", "/"))

    def _emit(self, event):
        try:
            self.event_logger(event)
        except Exception:
            pass

    def show(self):
        self._emit("RENDERER_MAIN|DESKTOP_RUNTIME_FALLBACK_VISIBLE|core_survived=true")
        self.core_visualization_visible.emit()

    def request_shutdown(self):
        self._emit("RENDERER_MAIN|DESKTOP_RUNTIME_FALLBACK_SHUTDOWN")
        QTimer.singleShot(0, self.deleteLater)
        return True

    def set_visual_state(self, _state_name):
        return

    def configure_monitoring_hud_live_client_self_qa(self, **_kwargs):
        self._emit("RENDERER_MAIN|MONITORING_HUD_LIVE_CLIENT_SELF_QA_UNAVAILABLE|reason=desktop_runtime_unavailable")

    def toggle_command_overlay(self):
        self._emit("RENDERER_MAIN|COMMAND_OVERLAY_UNAVAILABLE|reason=desktop_runtime_unavailable")

    def open_command_overlay(self):
        self.toggle_command_overlay()

    def command_overlay_state(self):
        return {"visible": False, "phase": "closed"}

    def request_create_custom_task_from_tray(self, source="tray"):
        self._emit(f"RENDERER_MAIN|TRAY_CREATE_CUSTOM_TASK_ABORTED|source={source}|reason=desktop_runtime_unavailable")

    def resident_access_status_snapshot(self):
        return build_resident_access_menu_plan(
            monitoring_hud_state=self.monitoring_hud_feature_state(),
            command_overlay_state=self.command_overlay_state(),
        )

    def open_resident_access_settings(self, source="tray", focus="quick_access"):
        self._emit(
            "RENDERER_MAIN|RESIDENT_ACCESS_SETTINGS_OPEN_ABORTED"
            f"|source={source}|focus={focus}|reason=desktop_runtime_unavailable"
        )

    def request_ai_status_from_resident_access(self, source="tray"):
        self._emit(
            "RENDERER_MAIN|RESIDENT_ACCESS_AI_STATUS_UNAVAILABLE"
            f"|source={source}|reason=desktop_runtime_unavailable"
        )

    def request_privacy_lockdown_from_resident_access(self, source="tray"):
        self._emit(
            "RENDERER_MAIN|RESIDENT_ACCESS_PRIVACY_LOCKDOWN_UNAVAILABLE"
            f"|source={source}|reason=desktop_runtime_unavailable"
        )

    def request_resident_quick_action_from_tray(self, route_id="", source="tray"):
        self._emit(
            "RENDERER_MAIN|RESIDENT_ACCESS_QUICK_ACTION_ABORTED"
            f"|source={source}|route_id={route_id}|reason=desktop_runtime_unavailable"
        )

    def show_ai_control_center_from_tray(self, source="tray"):
        self._emit(f"RENDERER_MAIN|AI_CONTROL_CENTER_ABORTED|source={source}|reason=desktop_runtime_unavailable")
        return {"shown": False, "reason": "desktop_runtime_unavailable"}

    def monitoring_hud_feature_state(self):
        return {
            "feature_enabled": False,
            "dashboard_visible": False,
            "runtime_available": False,
            "dashboard_available": False,
            "resident_route_state": "not_installed",
            "resident_route_reason": "HUD runtime is unavailable.",
            "overlay_deferred": True,
            "overlay_anchor_enabled": False,
            "source": "desktop_runtime_unavailable",
        }

    def monitoring_hud_access(self):
        return self._monitoring_hud_access_adapter

    def request_monitoring_hud_toggle_from_tray(self, source="tray"):
        self._emit(f"RENDERER_MAIN|TRAY_MONITORING_HUD_TOGGLE_ABORTED|source={source}|reason=desktop_runtime_unavailable")

    def request_monitoring_hud_dashboard_from_tray(self, source="tray", visible=True):
        self._emit(
            "RENDERER_MAIN|TRAY_MONITORING_HUD_DASHBOARD_ABORTED"
            f"|source={source}|visible={str(bool(visible)).lower()}|reason=desktop_runtime_unavailable"
        )
        return (
            self._monitoring_hud_access_adapter.open_or_restore_dashboard(source)
            if visible
            else self._monitoring_hud_access_adapter.close_dashboard(source)
        )

    def request_monitoring_hud_unanchor_from_tray(self, source="tray"):
        self._emit(f"RENDERER_MAIN|TRAY_MONITORING_HUD_UNANCHOR_ABORTED|source={source}|reason=desktop_runtime_unavailable")

    def handle_overlay_text_requested(self, _text):
        return

    def handle_overlay_backspace_requested(self):
        return

    def handle_overlay_submit_requested(self):
        return

    def handle_overlay_escape_requested(self):
        return

    def handle_overlay_global_click_requested(self, _x, _y):
        return

    def overlay_needs_global_input_capture(self):
        return False

    def overlay_allows_launch_grace(self):
        return False

    def overlay_monitors_global_clicks(self):
        return False


def parse_runtime_log_arg(argv):
    global RUNTIME_LOG_FILE
    for i, arg in enumerate(argv):
        if arg == "--runtime-log" and i + 1 < len(argv):
            RUNTIME_LOG_FILE = argv[i + 1]
            return


def parse_startup_abort_signal_arg(argv):
    global STARTUP_ABORT_SIGNAL_FILE
    for i, arg in enumerate(argv):
        if arg == "--startup-abort-signal" and i + 1 < len(argv):
            STARTUP_ABORT_SIGNAL_FILE = argv[i + 1]
            return


def parse_monitoring_hud_live_self_qa_args(argv):
    global MONITORING_HUD_LIVE_SELF_QA_MANIFEST, MONITORING_HUD_LIVE_SELF_QA_ROOT
    global MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS, MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS
    global MONITORING_HUD_LIVE_SELF_QA_LANE
    MONITORING_HUD_LIVE_SELF_QA_MANIFEST = (
        os.environ.get(MONITORING_HUD_LIVE_SELF_QA_MANIFEST_ENV) or ""
    ).strip()
    MONITORING_HUD_LIVE_SELF_QA_ROOT = (
        os.environ.get(MONITORING_HUD_LIVE_SELF_QA_ROOT_ENV) or ""
    ).strip()
    env_step_delay = (os.environ.get(MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS_ENV) or "").strip()
    if env_step_delay:
        try:
            MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS = max(250, int(env_step_delay))
        except ValueError:
            MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS = 250
    env_final_hold = (os.environ.get(MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS_ENV) or "").strip()
    if env_final_hold:
        try:
            MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS = max(0, int(env_final_hold))
        except ValueError:
            MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS = 0
    env_lane = (os.environ.get(MONITORING_HUD_LIVE_SELF_QA_LANE_ENV) or "").strip()
    if env_lane:
        MONITORING_HUD_LIVE_SELF_QA_LANE = env_lane
    for i, arg in enumerate(argv):
        if arg == "--monitoring-hud-live-self-qa-manifest" and i + 1 < len(argv):
            MONITORING_HUD_LIVE_SELF_QA_MANIFEST = argv[i + 1]
        elif arg == "--monitoring-hud-live-self-qa-root" and i + 1 < len(argv):
            MONITORING_HUD_LIVE_SELF_QA_ROOT = argv[i + 1]
        elif arg == "--monitoring-hud-live-self-qa-step-delay-ms" and i + 1 < len(argv):
            try:
                MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS = max(250, int(argv[i + 1]))
            except ValueError:
                MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS = 250
        elif arg == "--monitoring-hud-live-self-qa-final-hold-ms" and i + 1 < len(argv):
            try:
                MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS = max(0, int(argv[i + 1]))
            except ValueError:
                MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS = 0
        elif arg == "--monitoring-hud-live-self-qa-lane" and i + 1 < len(argv):
            MONITORING_HUD_LIVE_SELF_QA_LANE = argv[i + 1]


def runtime_milestone(event):
    if not RUNTIME_LOG_FILE:
        return
    try:
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        with open(RUNTIME_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {event}\n")
    except Exception:
        pass


def normalize_shutdown_confirmation_decision(value):
    normalized = (str(value or "").strip().casefold())
    if normalized in {"accept", "accepted", "yes", "y", "true", "1"}:
        return SHUTDOWN_CONFIRMATION_ACCEPTED
    if normalized in {"cancel", "cancelled", "decline", "declined", "no", "n", "false", "0"}:
        return SHUTDOWN_CONFIRMATION_CANCELLED
    if normalized in {"timeout", "timed_out", "expired"}:
        return SHUTDOWN_CONFIRMATION_TIMEOUT
    return ""


def shutdown_confirmation_timeout_ms():
    value = (os.environ.get(SHUTDOWN_CONFIRMATION_TIMEOUT_ENV) or "").strip()
    if not value:
        return SHUTDOWN_CONFIRMATION_DEFAULT_TIMEOUT_MS
    try:
        return min(120000, max(1000, int(value)))
    except ValueError:
        return SHUTDOWN_CONFIRMATION_DEFAULT_TIMEOUT_MS


def shutdown_confirmation_allows_shutdown(decision):
    return normalize_shutdown_confirmation_decision(decision) == SHUTDOWN_CONFIRMATION_ACCEPTED


def shutdown_confirmation_runtime_markers(decision, source="hotkey"):
    normalized = normalize_shutdown_confirmation_decision(decision) or SHUTDOWN_CONFIRMATION_CANCELLED
    safe_source = str(source or "hotkey").replace("|", "_")
    if normalized == SHUTDOWN_CONFIRMATION_ACCEPTED:
        return (
            f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_ACCEPTED|source={safe_source}",
            f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_CLEAN_SHUTDOWN_REQUESTED|source={safe_source}",
        )
    if normalized == SHUTDOWN_CONFIRMATION_TIMEOUT:
        return (
            f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_TIMEOUT|source={safe_source}",
            f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_SESSION_PRESERVED|source={safe_source}|reason=timeout",
        )
    return (
        f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_CANCELLED|source={safe_source}",
        f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_SESSION_PRESERVED|source={safe_source}|reason=cancelled",
    )


def shutdown_confirmation_requested_marker(source="hotkey"):
    safe_source = str(source or "hotkey").replace("|", "_")
    return f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_REQUESTED|source={safe_source}"


def _screen_label(screen):
    if screen is None:
        return "none"
    try:
        name = screen.name()
    except Exception:
        name = ""
    geometry = screen.geometry()
    return (
        f"name={str(name or 'unknown').replace('|', '_')}"
        f"|x={geometry.x()}|y={geometry.y()}|w={geometry.width()}|h={geometry.height()}"
    )


def resolve_core_visualization_screen(app):
    """Keep the persona Core on the preset install monitor, not on HUD surfaces.

    Until installer-owned monitor preference exists in repo truth, the safest
    approximation is the center physical monitor when three or more screens are
    present, otherwise the OS primary screen.
    """
    screens = list(app.screens())
    primary = app.primaryScreen()
    if not screens:
        return primary, "primary-fallback"

    indexed = list(enumerate(screens))
    configured = (os.environ.get("NEXUS_CORE_MONITOR_INDEX") or "").strip()
    if configured:
        try:
            requested_index = int(configured)
        except ValueError:
            requested_index = -1
        if 0 <= requested_index < len(screens):
            return screens[requested_index], f"configured-index-{requested_index}"

    if len(screens) >= 3:
        by_x_center = sorted(indexed, key=lambda item: (item[1].geometry().center().x(), item[1].geometry().center().y()))
        original_index, screen = by_x_center[len(by_x_center) // 2]
        return screen, f"middle-monitor-default-{original_index}"

    return primary or screens[0], "primary-fallback"


def _show_shutdown_confirmation_dialog(timeout_ms, event_logger=None, source="hotkey"):
    safe_source = str(source or "hotkey").replace("|", "_")
    timeout_ms = max(1000, int(timeout_ms))
    if os.name == "nt":
        try:
            user32 = ctypes.windll.user32
            message_box_timeout = getattr(user32, "MessageBoxTimeoutW")
            flags = 0x00000004 | 0x00000030 | 0x00000100 | 0x00010000 | 0x00040000
            if callable(event_logger):
                event_logger(
                    "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_DIALOG_VISIBLE"
                    f"|source={safe_source}|timeout_ms={timeout_ms}|implementation=win32_message_box_timeout"
                )
            result = message_box_timeout(
                None,
                "Choose Yes to close the desktop runtime, or No to keep the current session running.",
                "Confirm shutdown",
                flags,
                0,
                timeout_ms,
            )
            if result == 6:
                return SHUTDOWN_CONFIRMATION_ACCEPTED
            if result == 32000:
                return SHUTDOWN_CONFIRMATION_TIMEOUT
            return SHUTDOWN_CONFIRMATION_CANCELLED
        except Exception as exc:
            if callable(event_logger):
                event_logger(
                    "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_NATIVE_FALLBACK"
                    f"|source={safe_source}|reason={type(exc).__name__}"
                )

    message_box = QMessageBox()
    message_box.setWindowTitle("Confirm shutdown")
    message_box.setText("Shut down Nexus Desktop AI?")
    message_box.setInformativeText(
        "Choose Yes to close the desktop runtime, or No to keep the current session running."
    )
    message_box.setIcon(QMessageBox.Icon.Warning)
    message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    message_box.setDefaultButton(QMessageBox.StandardButton.No)
    message_box.setEscapeButton(QMessageBox.StandardButton.No)
    message_box.setWindowModality(Qt.WindowModality.ApplicationModal)
    message_box.setWindowFlags(
        message_box.windowFlags()
        | Qt.WindowType.Window
        | Qt.WindowType.WindowStaysOnTopHint
    )

    timed_out = {"value": False}

    def expire_confirmation():
        timed_out["value"] = True
        message_box.reject()

    timer = QTimer(message_box)
    timer.setSingleShot(True)
    timer.timeout.connect(expire_confirmation)
    timer.start(timeout_ms)

    try:
        message_box.show()
        screen = QApplication.screenAt(QCursor.pos()) or QApplication.primaryScreen()
        if screen is not None:
            geometry = message_box.frameGeometry()
            geometry.moveCenter(screen.availableGeometry().center())
            message_box.move(geometry.topLeft())
        message_box.raise_()
        message_box.activateWindow()
        QApplication.processEvents()
        if callable(event_logger):
            event_logger(
                "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_DIALOG_VISIBLE"
                f"|source={safe_source}|timeout_ms={timeout_ms}|implementation=qt_message_box"
            )
        result = message_box.exec()
    finally:
        timer.stop()

    if timed_out["value"]:
        return SHUTDOWN_CONFIRMATION_TIMEOUT
    if result == QMessageBox.StandardButton.Yes:
        return SHUTDOWN_CONFIRMATION_ACCEPTED
    return SHUTDOWN_CONFIRMATION_CANCELLED


def write_desktop_settled_signal_file():
    if not RUNTIME_LOG_FILE:
        return False
    try:
        signal_path = os.path.join(os.path.dirname(RUNTIME_LOG_FILE), "desktop_settled.signal")
        with open(signal_path, "w", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}|renderer authoritative settled\n")
        return True
    except Exception:
        return False


def overlay_trace_enabled():
    value = (os.environ.get("NEXUS_OVERLAY_TRACE") or "").strip().casefold()
    return value in {"1", "true", "yes", "on"}


def harness_relaunch_shutdown_delay_seconds():
    value = (os.environ.get("NEXUS_HARNESS_RELAUNCH_SHUTDOWN_DELAY_SECONDS") or "").strip()
    if not value:
        return 0.0
    try:
        return max(0.0, float(value))
    except ValueError:
        return 0.0


def harness_ignore_relaunch_request():
    value = (os.environ.get("NEXUS_HARNESS_IGNORE_RELAUNCH_REQUEST") or "").strip().casefold()
    return value in {"1", "true", "yes", "on"}


def monitoring_hud_startup_enabled():
    if MONITORING_HUD_LIVE_SELF_QA_MANIFEST:
        return True
    value = (os.environ.get(MONITORING_HUD_STARTUP_ENV) or "").strip().casefold()
    return value in {"1", "true", "yes", "on"}


def real_client_tray_precheck_manifest_path():
    return (os.environ.get(REAL_CLIENT_TRAY_PRECHECK_MANIFEST_ENV) or "").strip()


def real_client_tray_precheck_exits_after_run():
    value = (os.environ.get(REAL_CLIENT_TRAY_PRECHECK_EXIT_ENV) or "").strip().casefold()
    return value in {"1", "true", "yes", "on"}


def real_client_tray_precheck_shortcut_path():
    return (
        os.environ.get(DESKTOP_VALIDATION_SHORTCUT_ENV)
        or r"C:\Users\anden\OneDrive\Desktop\Nexus Desktop Launcher.lnk"
    )


def fam003_settings_live_resize_manifest_path():
    return (os.environ.get(FAM003_SETTINGS_LIVE_RESIZE_MANIFEST_ENV) or "").strip()


def fam003_settings_live_resize_exits_after_run():
    value = (os.environ.get(FAM003_SETTINGS_LIVE_RESIZE_EXIT_ENV) or "").strip().casefold()
    return value in {"1", "true", "yes", "on"}


def fam003_lv_visible_input_manifest_path():
    return (os.environ.get(FAM003_LV_VISIBLE_INPUT_MANIFEST_ENV) or "").strip()


def fam003_lv_visible_input_exits_after_run():
    value = (os.environ.get(FAM003_LV_VISIBLE_INPUT_EXIT_ENV) or "").strip().casefold()
    return value in {"1", "true", "yes", "on"}


def startup_abort_requested():
    return bool(STARTUP_ABORT_SIGNAL_FILE) and os.path.exists(STARTUP_ABORT_SIGNAL_FILE)


def exit_if_startup_abort_requested(hotkeys=None, tray_entry=None):
    if not startup_abort_requested():
        return False

    runtime_milestone("RENDERER_MAIN|STARTUP_ABORTED")

    if tray_entry is not None:
        try:
            tray_entry.close()
        except Exception:
            pass

    if hotkeys is not None:
        try:
            hotkeys.stop()
        except Exception:
            pass

    return True


def main():
    parse_runtime_log_arg(sys.argv)
    parse_startup_abort_signal_arg(sys.argv)
    parse_monitoring_hud_live_self_qa_args(sys.argv)
    runtime_milestone("RENDERER_MAIN|START")
    if exit_if_startup_abort_requested():
        return 0

    app = QApplication(sys.argv)
    app.setApplicationName(TRAY_IDENTITY_LABEL)
    app.setWindowIcon(build_resident_tray_icon())
    app.setQuitOnLastWindowClosed(False)
    try:
        app.setApplicationDisplayName(TRAY_IDENTITY_LABEL)
    except Exception:
        pass
    runtime_milestone("RENDERER_MAIN|QAPPLICATION_CREATED")
    if exit_if_startup_abort_requested():
        return 0

    visual_html_path = os.path.join(ROOT_DIR, "nexus_visual", "orin_core_desktop.html")
    monitoring_hud_html_path = os.path.join(ROOT_DIR, "nexus_visual", "monitoring_hud.html")
    monitoring_hud_forced_startup_visible = monitoring_hud_startup_enabled()
    monitoring_hud_saved_state = load_monitoring_hud_state(runtime_milestone)
    monitoring_hud_saved_feature_enabled = bool(monitoring_hud_saved_state.get("featureEnabled"))
    monitoring_hud_feature_enabled_at_startup = (
        bool(monitoring_hud_forced_startup_visible) or monitoring_hud_saved_feature_enabled
    )
    monitoring_hud_dashboard_visible_at_startup = bool(monitoring_hud_forced_startup_visible)
    runtime_milestone(
        "RENDERER_MAIN|MONITORING_HUD_STARTUP_STATE_READY"
        f"|source={monitoring_hud_saved_state.get('source', 'unknown')}"
        f"|feature_enabled={str(monitoring_hud_feature_enabled_at_startup).lower()}"
        f"|dashboard_visible={str(monitoring_hud_dashboard_visible_at_startup).lower()}"
        f"|forced_visible={str(bool(monitoring_hud_forced_startup_visible)).lower()}"
    )
    runtime_milestone("RENDERER_MAIN|VISUAL_HTML_RESOLVED")
    if exit_if_startup_abort_requested():
        return 0

    screen = app.primaryScreen()
    core_screen, core_screen_source = resolve_core_visualization_screen(app)
    runtime_milestone(
        "RENDERER_MAIN|CORE_VISUALIZATION_PRESET_MONITOR_SELECTION_READY"
        f"|source={core_screen_source}|{_screen_label(core_screen)}"
    )
    core_window = CoreVisualizationWindow(
        core_screen or screen,
        visual_html_path,
        event_logger=runtime_milestone,
    )
    if DesktopRuntimeWindow is None:
        window = DesktopRuntimeUnavailable(
            event_logger=runtime_milestone,
            reason=repr(DESKTOP_RUNTIME_IMPORT_ERROR),
        )
    else:
        try:
            window = DesktopRuntimeWindow(
                screen,
                monitoring_hud_html_path,
                event_logger=runtime_milestone,
                runtime_log_path=RUNTIME_LOG_FILE,
                surface_role="hud",
                monitoring_hud_feature_enabled=monitoring_hud_feature_enabled_at_startup,
                monitoring_hud_dashboard_visible=monitoring_hud_dashboard_visible_at_startup,
                monitoring_hud_initial_state=monitoring_hud_saved_state,
            )
        except Exception as exc:
            window = DesktopRuntimeUnavailable(
                event_logger=runtime_milestone,
                reason=repr(exc),
            )
    if MONITORING_HUD_LIVE_SELF_QA_MANIFEST:
        window.configure_monitoring_hud_live_client_self_qa(
            manifest_path=MONITORING_HUD_LIVE_SELF_QA_MANIFEST,
            evidence_root=MONITORING_HUD_LIVE_SELF_QA_ROOT,
            step_delay_ms=MONITORING_HUD_LIVE_SELF_QA_STEP_DELAY_MS,
            final_hold_ms=MONITORING_HUD_LIVE_SELF_QA_FINAL_HOLD_MS,
            lane=MONITORING_HUD_LIVE_SELF_QA_LANE,
        )
    runtime_milestone("RENDERER_MAIN|WINDOW_CONSTRUCTED")
    if exit_if_startup_abort_requested():
        return 0

    bus = ShutdownBus()
    runtime_milestone("RENDERER_MAIN|SHUTDOWN_BUS_READY")
    hotkeys = GlobalHotkeyManager(bus)
    relaunch_signal = NamedSignal(RUNTIME_RELAUNCH_EVENT)
    desktop_settled_signal = NamedSignal(RUNTIME_DESKTOP_SETTLED_EVENT)
    shutdown_started = False
    shutdown_confirmation_active = False
    shutdown_force_kill_timer = None
    shutdown_cleanup_timeout_timer = None
    shutdown_pending_components = set()
    if exit_if_startup_abort_requested():
        return 0

    def do_shutdown():
        nonlocal shutdown_started, shutdown_force_kill_timer, shutdown_cleanup_timeout_timer
        if shutdown_started:
            return
        settings_guard = getattr(window, "request_resident_access_settings_shutdown_guard", None)
        if callable(settings_guard):
            try:
                if settings_guard(source="client_shutdown", resume_callback=do_shutdown):
                    runtime_milestone(
                        "RENDERER_MAIN|SHUTDOWN_BLOCKED_BY_RESIDENT_SETTINGS_DIRTY_GUARD"
                        "|source=client_shutdown"
                    )
                    return
            except TypeError:
                if settings_guard(source="client_shutdown"):
                    runtime_milestone(
                        "RENDERER_MAIN|SHUTDOWN_BLOCKED_BY_RESIDENT_SETTINGS_DIRTY_GUARD"
                        "|source=client_shutdown"
                    )
                    return
        shutdown_started = True
        runtime_milestone("RENDERER_MAIN|SHUTDOWN_REQUESTED")
        tray_entry.close()
        hotkeys.stop()

        def finish_shutdown_if_released():
            if shutdown_pending_components:
                return
            if shutdown_cleanup_timeout_timer is not None:
                shutdown_cleanup_timeout_timer.stop()
            runtime_milestone(
                "RENDERER_MAIN|NATIVE_SURFACES_RELEASED|components=core_visualization,desktop_runtime"
            )
            runtime_milestone("RENDERER_MAIN|QT_QUIT_REQUESTED|reason=native_surfaces_released")
            QTimer.singleShot(0, app.quit)

        def component_released(component):
            shutdown_pending_components.discard(component)
            runtime_milestone(
                f"RENDERER_MAIN|SHUTDOWN_COMPONENT_RELEASED|component={component}"
            )
            finish_shutdown_if_released()

        def register_shutdown_component(component, target):
            shutdown_pending_components.add(component)
            target.destroyed.connect(
                lambda _object=None, name=component: component_released(name)
            )

        def cleanup_timeout():
            pending = ",".join(sorted(shutdown_pending_components)) or "none"
            runtime_milestone(
                f"RENDERER_MAIN|SHUTDOWN_CLEANUP_TIMEOUT|pending={pending}"
            )
            app.exit(1)

        register_shutdown_component("core_visualization", core_window)
        register_shutdown_component("desktop_runtime", window)
        core_window.request_shutdown()
        window.request_shutdown()
        shutdown_cleanup_timeout_timer = QTimer(app)
        shutdown_cleanup_timeout_timer.setSingleShot(True)
        shutdown_cleanup_timeout_timer.timeout.connect(cleanup_timeout)
        shutdown_cleanup_timeout_timer.start(4000)
        shutdown_force_kill_timer = threading.Timer(7.0, hotkeys.force_kill)
        shutdown_force_kill_timer.daemon = True
        shutdown_force_kill_timer.start()

    def request_shutdown_confirmation(source="hotkey"):
        nonlocal shutdown_confirmation_active
        safe_source = str(source or "hotkey").replace("|", "_")
        if shutdown_started:
            runtime_milestone(
                f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_IGNORED|source={safe_source}|reason=shutdown_started"
            )
            return
        if shutdown_confirmation_active:
            runtime_milestone(
                f"RENDERER_MAIN|SHUTDOWN_CONFIRMATION_IGNORED|source={safe_source}|reason=already_active"
            )
            return
        settings_guard = getattr(window, "request_resident_access_settings_shutdown_guard", None)
        if callable(settings_guard):
            try:
                if settings_guard(
                    source=f"shutdown_confirmation_{safe_source}",
                    resume_callback=lambda: request_shutdown_confirmation(source=safe_source),
                ):
                    runtime_milestone(
                        "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_BLOCKED_BY_RESIDENT_SETTINGS_DIRTY_GUARD"
                        f"|source={safe_source}"
                    )
                    return
            except TypeError:
                if settings_guard(source=f"shutdown_confirmation_{safe_source}"):
                    runtime_milestone(
                        "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_BLOCKED_BY_RESIDENT_SETTINGS_DIRTY_GUARD"
                        f"|source={safe_source}"
                    )
                    return

        shutdown_confirmation_active = True
        try:
            runtime_milestone(shutdown_confirmation_requested_marker(safe_source))
            env_decision = normalize_shutdown_confirmation_decision(
                os.environ.get(SHUTDOWN_CONFIRMATION_DECISION_ENV)
            )
            if env_decision:
                runtime_milestone(
                    "RENDERER_MAIN|SHUTDOWN_CONFIRMATION_DECISION_SOURCE"
                    f"|source={safe_source}|mode=harness_env|decision={env_decision}"
                )
                decision = env_decision
            else:
                decision = _show_shutdown_confirmation_dialog(
                    shutdown_confirmation_timeout_ms(),
                    event_logger=runtime_milestone,
                    source=safe_source,
                )

            for marker in shutdown_confirmation_runtime_markers(decision, safe_source):
                runtime_milestone(marker)

            if shutdown_confirmation_allows_shutdown(decision):
                do_shutdown()
        finally:
            shutdown_confirmation_active = False

    def poll_relaunch_request():
        if relaunch_signal.consume():
            runtime_milestone("RENDERER_MAIN|RELAUNCH_REQUEST_RECEIVED")
            if harness_ignore_relaunch_request():
                runtime_milestone("RENDERER_MAIN|HARNESS_RELAUNCH_REQUEST_IGNORED")
                return
            delay_seconds = harness_relaunch_shutdown_delay_seconds()
            if delay_seconds > 0:
                runtime_milestone(
                    f"RENDERER_MAIN|HARNESS_RELAUNCH_SHUTDOWN_DELAY|seconds={delay_seconds:g}"
                )
                time.sleep(delay_seconds)
            do_shutdown()

    shutdown_confirmation_dispatcher = ShutdownConfirmationDispatcher(
        request_shutdown_confirmation,
        app,
    )

    bus.shutdown_requested.connect(do_shutdown)
    bus.shutdown_confirmation_requested.connect(
        shutdown_confirmation_dispatcher.request,
        Qt.ConnectionType.QueuedConnection,
    )
    bus.command_overlay_toggle_requested.connect(window.toggle_command_overlay)
    bus.command_overlay_text_requested.connect(window.handle_overlay_text_requested)
    bus.command_overlay_backspace_requested.connect(window.handle_overlay_backspace_requested)
    bus.command_overlay_submit_requested.connect(window.handle_overlay_submit_requested)
    bus.command_overlay_escape_requested.connect(window.handle_overlay_escape_requested)
    bus.command_overlay_global_click_requested.connect(window.handle_overlay_global_click_requested)
    tray_entry = DesktopTrayEntry(
        app,
        window,
        runtime_milestone,
        shutdown_confirmation_requester=request_shutdown_confirmation,
    )
    tray_entry.initialize()
    hotkeys.set_overlay_input_enabled_provider(window.overlay_needs_global_input_capture)
    hotkeys.set_overlay_launch_grace_allowed_provider(window.overlay_allows_launch_grace)
    hotkeys.set_overlay_click_monitor_provider(window.overlay_monitors_global_clicks)
    if overlay_trace_enabled():
        hotkeys.set_debug_logger(runtime_milestone)
    hotkeys.start()
    runtime_milestone("RENDERER_MAIN|HOTKEYS_STARTED")
    if exit_if_startup_abort_requested(hotkeys, tray_entry):
        return 0

    print("Nexus Desktop AI Desktop Runtime - Version 1.02")
    print("Command Overlay: Ctrl + Alt + Home or Ctrl + Alt + 1")
    print("Hotkey: Ctrl + Alt + End or Ctrl + Alt + 2 (direct shutdown; tray exit asks for confirmation)")

    real_client_tray_precheck_started = False

    def run_real_client_tray_precheck():
        nonlocal real_client_tray_precheck_started
        manifest_path = real_client_tray_precheck_manifest_path()
        if not manifest_path or real_client_tray_precheck_started or shutdown_started:
            return
        real_client_tray_precheck_started = True
        runtime_milestone("RENDERER_MAIN|REAL_CLIENT_TRAY_PRECHECK_STARTED|seam=WS47")

        started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        steps = []

        def pump(duration_ms=250):
            deadline = time.time() + (max(0, duration_ms) / 1000.0)
            while time.time() < deadline:
                QApplication.processEvents()
                time.sleep(0.025)

        def current_state():
            provider = getattr(window, "monitoring_hud_feature_state", None)
            if callable(provider):
                try:
                    state = provider()
                    if isinstance(state, dict):
                        return dict(state)
                except Exception as exc:
                    return {"error": f"{type(exc).__name__}: {exc}"}
            return {"error": "monitoring_hud_feature_state unavailable"}

        def visible_tray_action_texts():
            try:
                texts = [
                    action.text()
                    for action in tray_entry.tray_menu.actions()
                    if not action.isSeparator() and action.isVisible()
                ]
                for submenu in (
                    tray_entry.quick_access_menu,
                    tray_entry.ai_menu,
                    tray_entry.hud_menu,
                ):
                    if submenu is None or not submenu.menuAction().isVisible():
                        continue
                    texts.extend(
                        action.text()
                        for action in submenu.actions()
                        if not action.isSeparator() and action.isVisible()
                    )
                return texts
            except Exception:
                return []

        def record_step(step_id, title, ok, detail, proof_class="active-client-tray-precheck"):
            steps.append(
                {
                    "id": step_id,
                    "title": title,
                    "codexPrecheck": "PASS" if ok else "FAIL",
                    "proofClass": proof_class,
                    "detail": detail,
                    "state": current_state(),
                }
            )

        def write_manifest(status, failure=""):
            payload = {
                "schema": "fam006-ws47-real-client-tray-precheck-v1",
                "status": status,
                "failure": failure,
                "startedAt": started_at,
                "finishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "seam": "Workstream WS47 - Dashboard Real-Client Tray Shortcut And Proof-Governance Repair",
                "shortcutPath": real_client_tray_precheck_shortcut_path(),
                "proofClasses": {
                    "staticProof": "supporting",
                    "sandboxProof": "supporting",
                    "fakeOffscreenModelProof": "supporting-only-not-acceptance",
                    "activeClientTrayPrecheck": status,
                    "realUserOperatedTrayProof": "USER_LV1_REQUIRED",
                },
                "steps": steps,
                "formalUtsTouched": False,
            }
            try:
                os.makedirs(os.path.dirname(os.path.abspath(manifest_path)), exist_ok=True)
                with open(manifest_path, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle, indent=2, sort_keys=True)
                runtime_milestone(
                    "RENDERER_MAIN|REAL_CLIENT_TRAY_PRECHECK_MANIFEST_WRITTEN"
                    f"|status={status}|path={manifest_path}"
                )
            except Exception as exc:
                runtime_milestone(
                    "RENDERER_MAIN|REAL_CLIENT_TRAY_PRECHECK_MANIFEST_FAILED"
                    f"|reason={type(exc).__name__}"
                )

        try:
            tray_entry.refresh_monitoring_hud_actions("real_client_precheck_initial")
            initial_state = current_state()
            record_step(
                "launch_settled_tray_available",
                "Desktop shortcut runtime settled with tray available and USER-disabled HUD rows hidden",
                tray_entry.tray_icon is not None
                and not bool(initial_state.get("feature_enabled"))
                and "Open HUD Dashboard" not in visible_tray_action_texts()
                and "HUD Overlay Deferred" not in visible_tray_action_texts(),
                (
                    "tray icon exists, HUD feature starts disabled, "
                    f"visible_actions={visible_tray_action_texts()}"
                ),
            )

            access_provider = getattr(window, "monitoring_hud_access", None)
            hud_access = access_provider() if callable(access_provider) else None
            settings_setup = getattr(hud_access, "set_enabled", None)
            if callable(settings_setup):
                settings_setup(True, "real_client_precheck_settings_setup")
            tray_entry.refresh_monitoring_hud_actions("real_client_precheck_settings_setup")
            pump(700)
            enabled_state = current_state()
            record_step(
                "settings_setup_admits_hud_route",
                "Settings/setup-owned HUD admission makes the dashboard route available for tray proof",
                bool(enabled_state.get("feature_enabled"))
                and "Open HUD Dashboard" in visible_tray_action_texts()
                and "Close HUD Dashboard" not in visible_tray_action_texts(),
                (
                    f"feature_enabled={enabled_state.get('feature_enabled')} "
                    f"dashboard_visible={enabled_state.get('dashboard_visible')} "
                    f"window_visible={window.isVisible()} visible_actions={visible_tray_action_texts()}"
                ),
            )

            close_dashboard = getattr(hud_access, "close_dashboard", None)
            if callable(close_dashboard):
                close_dashboard("real_client_precheck_owner_close")
            pump(350)
            closed_state = current_state()
            record_step(
                "owner_bounded_close_keeps_feature_enabled",
                "Owner-bounded close hides HUD Dashboard without changing enabled resident access",
                bool(closed_state.get("feature_enabled"))
                and not bool(closed_state.get("dashboard_visible"))
                and not bool(window.isVisible()),
                f"feature_enabled={closed_state.get('feature_enabled')} dashboard_visible={closed_state.get('dashboard_visible')} window_visible={window.isVisible()}",
            )

            tray_entry.request_monitoring_hud_dashboard_from_tray("real_client_precheck_open")
            pump(500)
            reopened_state = current_state()
            record_step(
                "open_dashboard_from_tray",
                "Tray Open HUD Dashboard makes the real Dashboard visible",
                bool(reopened_state.get("feature_enabled"))
                and bool(reopened_state.get("dashboard_visible"))
                and bool(window.isVisible()),
                f"feature_enabled={reopened_state.get('feature_enabled')} dashboard_visible={reopened_state.get('dashboard_visible')} window_visible={window.isVisible()}",
            )

            tray_entry.request_monitoring_hud_dashboard_from_tray("real_client_precheck_restore")
            pump(250)
            restored_state = current_state()
            record_step(
                "restore_dashboard_from_tray",
                "Repeated tray activation restores or focuses HUD Dashboard and never closes it",
                bool(restored_state.get("feature_enabled"))
                and bool(restored_state.get("dashboard_visible"))
                and bool(window.isVisible())
                and "Open HUD Dashboard" in visible_tray_action_texts()
                and "Close HUD Dashboard" not in visible_tray_action_texts(),
                f"feature_enabled={restored_state.get('feature_enabled')} dashboard_visible={restored_state.get('dashboard_visible')} window_visible={window.isVisible()}",
            )

            if callable(settings_setup):
                settings_setup(False, "real_client_precheck_settings_disable")
            tray_entry.refresh_monitoring_hud_actions("real_client_precheck_settings_disable")
            pump(500)
            disabled_state = current_state()
            record_step(
                "settings_disable_hides_hud_rows",
                "Settings/setup-owned HUD disable hides HUD rows and leaves runtime recoverable",
                not bool(disabled_state.get("feature_enabled"))
                and not bool(disabled_state.get("dashboard_visible"))
                and not bool(window.isVisible())
                and "Open HUD Dashboard" not in visible_tray_action_texts()
                and "HUD Overlay Deferred" not in visible_tray_action_texts()
                and not shutdown_started,
                (
                    f"feature_enabled={disabled_state.get('feature_enabled')} "
                    f"dashboard_visible={disabled_state.get('dashboard_visible')} "
                    f"window_visible={window.isVisible()} shutdown_started={shutdown_started} "
                    f"visible_actions={visible_tray_action_texts()}"
                ),
            )

            tray_entry.request_shutdown_from_tray("real_client_precheck_exit")
            pump(150)
            record_step(
                "tray_exit_confirmation_preserves_session_on_timeout",
                "Tray Exit requests visible confirmation and timeout/cancel preserves the session",
                not shutdown_started,
                f"shutdown_started={shutdown_started}",
                proof_class="active-client-confirmation-dialog-precheck",
            )

            status = "PASS" if all(step["codexPrecheck"] == "PASS" for step in steps) else "FAIL"
            write_manifest(status)
        except Exception as exc:
            record_step(
                "real_client_tray_precheck_exception",
                "Real-client tray precheck exception",
                False,
                f"{type(exc).__name__}: {exc}",
            )
            write_manifest("FAIL", f"{type(exc).__name__}: {exc}")
        finally:
            if real_client_tray_precheck_exits_after_run():
                QTimer.singleShot(500, do_shutdown)

    fam003_lv_visible_input_started = False

    def run_fam003_lv_visible_input_precheck():
        nonlocal fam003_lv_visible_input_started
        manifest_path = fam003_lv_visible_input_manifest_path()
        if not manifest_path or fam003_lv_visible_input_started or shutdown_started:
            return
        fam003_lv_visible_input_started = True
        runtime_milestone("RENDERER_MAIN|FAM003_LV_VISIBLE_INPUT_PRECHECK_STARTED")
        started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        steps = []

        def pump(duration_ms=250):
            deadline = time.time() + (max(0, duration_ms) / 1000.0)
            while time.time() < deadline:
                QApplication.processEvents()
                time.sleep(0.025)

        def record_step(step_id, title, ok, detail, evidence=None, proof_class="visible-user-level-input"):
            steps.append(
                {
                    "id": step_id,
                    "title": title,
                    "codexPrecheck": "PASS" if ok else "FAIL",
                    "proofClass": proof_class,
                    "detail": detail,
                    "evidence": evidence or {},
                }
            )

        def write_manifest(status, failure=""):
            payload = {
                "schema": "fam003-lv-visible-input-precheck-v1",
                "status": status,
                "failure": failure,
                "startedAt": started_at,
                "finishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "surface": "FAM-003 LV1 visible tray/NCP control surfaces",
                "shortcutPath": real_client_tray_precheck_shortcut_path(),
                "normalLauncherProof": True,
                "proofMethod": (
                    "exact normal launcher plus Win32 visible cursor/mouse/keyboard input; "
                    "tray icon geometry is attempted before fallback popup proof"
                ),
                "formalUtsTouched": False,
                "proofClasses": {
                    "trayIconContextClick": next(
                        (
                            step["codexPrecheck"]
                            for step in steps
                            if step["id"] == "tray_icon_context_click_opens_popup"
                        ),
                        "NOT_RUN",
                    ),
                    "trayVisiblePopupButtonClick": next(
                        (
                            step["codexPrecheck"]
                            for step in steps
                            if step["id"] == "tray_visible_popup_button_click"
                        ),
                        "NOT_RUN",
                    ),
                    "ncpHotkeyKeyboardFlow": next(
                        (
                            step["codexPrecheck"]
                            for step in steps
                            if step["id"] == "ncp_hotkey_keyboard_flow"
                        ),
                        "NOT_RUN",
                    ),
                },
                "steps": steps,
            }
            try:
                os.makedirs(os.path.dirname(os.path.abspath(manifest_path)), exist_ok=True)
                with open(manifest_path, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle, indent=2, sort_keys=True)
                runtime_milestone(
                    "RENDERER_MAIN|FAM003_LV_VISIBLE_INPUT_PRECHECK_MANIFEST_WRITTEN"
                    f"|status={status}|path={manifest_path}"
                )
            except Exception as exc:
                runtime_milestone(
                    "RENDERER_MAIN|FAM003_LV_VISIBLE_INPUT_PRECHECK_MANIFEST_FAILED"
                    f"|reason={type(exc).__name__}"
                )

        if not hasattr(ctypes, "windll"):
            record_step(
                "win32_visible_input_available",
                "Win32 visible input route is available",
                False,
                "ctypes.windll unavailable",
            )
            write_manifest("FAIL", "ctypes.windll unavailable")
            return

        user32 = ctypes.windll.user32
        set_cursor_pos = user32.SetCursorPos
        set_cursor_pos.argtypes = [ctypes.c_int, ctypes.c_int]
        set_cursor_pos.restype = ctypes.c_bool
        mouse_event = user32.mouse_event
        mouse_event.argtypes = [
            ctypes.wintypes.DWORD,
            ctypes.c_long,
            ctypes.c_long,
            ctypes.wintypes.DWORD,
            ctypes.c_ulong,
        ]
        mouse_event.restype = None
        keybd_event = user32.keybd_event
        keybd_event.argtypes = [
            ctypes.wintypes.BYTE,
            ctypes.wintypes.BYTE,
            ctypes.wintypes.DWORD,
            ctypes.c_ulong,
        ]
        keybd_event.restype = None
        vk_key_scan = user32.VkKeyScanW
        vk_key_scan.argtypes = [ctypes.wintypes.WCHAR]
        vk_key_scan.restype = ctypes.c_short
        set_foreground_window = user32.SetForegroundWindow
        set_foreground_window.argtypes = [ctypes.wintypes.HWND]
        set_foreground_window.restype = ctypes.c_bool

        left_down = 0x0002
        left_up = 0x0004
        right_down = 0x0008
        right_up = 0x0010
        key_up = 0x0002
        vk_shift = 0x10
        vk_control = 0x11
        vk_menu = 0x12
        vk_return = 0x0D
        vk_home = 0x24

        def click_point(point, button="left"):
            set_cursor_pos(int(point.x()), int(point.y()))
            pump(80)
            if button == "right":
                mouse_event(right_down, 0, 0, 0, 0)
                pump(45)
                mouse_event(right_up, 0, 0, 0, 0)
            else:
                mouse_event(left_down, 0, 0, 0, 0)
                pump(45)
                mouse_event(left_up, 0, 0, 0, 0)
            pump(260)

        def press_vk(vk):
            keybd_event(int(vk), 0, 0, 0)
            pump(30)
            keybd_event(int(vk), 0, key_up, 0)
            pump(60)

        def press_combo(*vks):
            for vk in vks:
                keybd_event(int(vk), 0, 0, 0)
                pump(20)
            for vk in reversed(vks):
                keybd_event(int(vk), 0, key_up, 0)
                pump(25)

        def type_text(text):
            typed = []
            for char in text:
                scan = int(vk_key_scan(char))
                if scan == -1:
                    continue
                vk = scan & 0xFF
                shift_state = (scan >> 8) & 0xFF
                if shift_state & 1:
                    keybd_event(vk_shift, 0, 0, 0)
                    pump(8)
                keybd_event(vk, 0, 0, 0)
                pump(8)
                keybd_event(vk, 0, key_up, 0)
                if shift_state & 1:
                    keybd_event(vk_shift, 0, key_up, 0)
                typed.append(char)
                pump(18)
            return "".join(typed)

        try:
            tray_entry.refresh_resident_access_actions("fam003_lv_visible_input_initial")
            tray_entry.refresh_monitoring_hud_actions("fam003_lv_visible_input_initial")
            pump(250)
            record_step(
                "win32_visible_input_available",
                "Win32 visible input route is available",
                True,
                "SetCursorPos, mouse_event, and keybd_event are available",
            )

            tray_geometry = None
            tray_geometry_available = False
            try:
                tray_geometry = tray_entry.tray_icon.geometry()
                tray_geometry_available = bool(
                    tray_geometry is not None
                    and tray_geometry.isValid()
                    and not tray_geometry.isEmpty()
                )
            except Exception:
                tray_geometry = None

            tray_popup_method = "none"
            if tray_geometry_available:
                center = tray_geometry.center()
                click_point(center, button="right")
                tray_popup_method = "tray_icon_context_click"
            popup_visible_after_icon_click = bool(
                tray_entry.tray_popup is not None and tray_entry.tray_popup.isVisible()
            )
            record_step(
                "tray_icon_context_click_opens_popup",
                "Visible Windows tray icon context click opens the NDAI tray popup",
                popup_visible_after_icon_click,
                (
                    f"trayGeometryAvailable={tray_geometry_available}; "
                    f"popupVisible={popup_visible_after_icon_click}; method={tray_popup_method}"
                ),
                {
                    "trayGeometryAvailable": tray_geometry_available,
                    "trayGeometry": (
                        {
                            "x": tray_geometry.x(),
                            "y": tray_geometry.y(),
                            "width": tray_geometry.width(),
                            "height": tray_geometry.height(),
                        }
                        if tray_geometry_available
                        else None
                    ),
                    "popupGeometry": (
                        {
                            "x": tray_entry.tray_popup.geometry().x(),
                            "y": tray_entry.tray_popup.geometry().y(),
                            "width": tray_entry.tray_popup.geometry().width(),
                            "height": tray_entry.tray_popup.geometry().height(),
                        }
                        if popup_visible_after_icon_click
                        else None
                    ),
                },
            )

            button = getattr(tray_entry, "global_settings_action", None)
            button_click_ok = False
            dialog_visible = False
            button_evidence = {
                "popupMethod": tray_popup_method,
                "hiddenHandlerOnly": False,
            }
            if popup_visible_after_icon_click and button is not None and button.isVisible() and button.isEnabled():
                button_rect = tray_entry.tray_menu.actionGeometry(button)
                button_center = tray_entry.tray_menu.mapToGlobal(button_rect.center())
                button_evidence["buttonText"] = button.text()
                button_evidence["buttonCenter"] = {"x": button_center.x(), "y": button_center.y()}
                click_point(button_center, button="left")
                pump(600)
                dialog = getattr(window, "_resident_access_settings_dialog", None)
                dialog_visible = bool(dialog is not None and dialog.isVisible())
                button_click_ok = dialog_visible
                if dialog is not None and dialog.isVisible():
                    dialog.close()
                    pump(180)
            record_step(
                "tray_visible_popup_button_click",
                "Visible NDAI tray popup button click routes to Global Settings",
                button_click_ok,
                f"buttonVisible={bool(button is not None and button.isVisible())}; dialogVisible={dialog_visible}; popupMethod={tray_popup_method}",
                button_evidence,
            )

            ncp_activation = "hotkey"
            try:
                hwnd = int(window.winId())
                set_foreground_window(ctypes.wintypes.HWND(hwnd))
            except Exception:
                pass
            pump(180)
            press_combo(vk_control, vk_menu, vk_home)
            pump(700)
            if not bool(window.command_overlay_state().get("visible")):
                ncp_activation = "hotkey_failed_no_direct_fallback"
            typed = type_text("open nexus folder")
            press_vk(vk_return)
            pump(750)
            phase_after_submit = str(window.command_overlay_state().get("phase"))
            if phase_after_submit == "choose":
                type_text("2")
                pump(300)
                press_vk(vk_return)
                pump(750)
            elif phase_after_submit == "confirm":
                press_vk(vk_return)
                pump(750)
            final_state = window.command_overlay_state()
            ncp_ok = (
                bool(final_state.get("visible"))
                and str(final_state.get("phase")) in {"result", "confirm", "choose"}
                and typed == "open nexus folder"
                and ncp_activation == "hotkey"
            )
            record_step(
                "ncp_hotkey_keyboard_flow",
                "NCP opens from the normal runtime and advances through visible keyboard input",
                ncp_ok,
                (
                    f"activation={ncp_activation}; typed={typed!r}; "
                    f"phaseAfterSubmit={phase_after_submit}; finalPhase={final_state.get('phase')}"
                ),
                {
                    "activationMethod": ncp_activation,
                    "typedText": typed,
                    "phaseAfterSubmit": phase_after_submit,
                    "finalState": final_state,
                    "fallbackUsed": ncp_activation != "hotkey",
                },
            )
            try:
                window.close_command_overlay()
            except Exception:
                pass
            pump(120)
            status = "PASS" if all(step["codexPrecheck"] == "PASS" for step in steps) else "FAIL"
            write_manifest(status)
        except Exception as exc:
            record_step(
                "fam003_lv_visible_input_exception",
                "FAM-003 visible input precheck exception",
                False,
                f"{type(exc).__name__}: {exc}",
            )
            write_manifest("FAIL", f"{type(exc).__name__}: {exc}")
        finally:
            if fam003_lv_visible_input_exits_after_run():
                QTimer.singleShot(500, do_shutdown)

    fam003_settings_live_resize_started = False

    def run_fam003_settings_live_resize_precheck():
        nonlocal fam003_settings_live_resize_started
        manifest_path = fam003_settings_live_resize_manifest_path()
        if not manifest_path or fam003_settings_live_resize_started or shutdown_started:
            return
        fam003_settings_live_resize_started = True
        runtime_milestone("RENDERER_MAIN|FAM003_SETTINGS_LIVE_RESIZE_PRECHECK_STARTED")
        started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        steps = []

        def pump(duration_ms=250):
            deadline = time.time() + (max(0, duration_ms) / 1000.0)
            while time.time() < deadline:
                QApplication.processEvents()
                time.sleep(0.025)

        def record_step(step_id, title, ok, detail, evidence=None):
            steps.append(
                {
                    "id": step_id,
                    "title": title,
                    "codexPrecheck": "PASS" if ok else "FAIL",
                    "detail": detail,
                    "evidence": evidence or {},
                }
            )

        def write_manifest(status, failure=""):
            payload = {
                "schema": "fam003-settings-live-resize-precheck-v2",
                "status": status,
                "failure": failure,
                "startedAt": started_at,
                "finishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "surface": "FAM-003 Global Settings",
                "shortcutPath": real_client_tray_precheck_shortcut_path(),
                "normalLauncherProof": True,
                "proofMethod": "normal desktop shortcut launch plus Windows resize cursor hover proof plus SetCursorPos held Win32 left-button drag",
                "formalUtsTouched": False,
                "steps": steps,
            }
            try:
                os.makedirs(os.path.dirname(os.path.abspath(manifest_path)), exist_ok=True)
                with open(manifest_path, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle, indent=2, sort_keys=True)
                runtime_milestone(
                    "RENDERER_MAIN|FAM003_SETTINGS_LIVE_RESIZE_PRECHECK_MANIFEST_WRITTEN"
                    f"|status={status}|path={manifest_path}"
                )
            except Exception as exc:
                runtime_milestone(
                    "RENDERER_MAIN|FAM003_SETTINGS_LIVE_RESIZE_PRECHECK_MANIFEST_FAILED"
                    f"|reason={type(exc).__name__}"
                )

        def drive_resize_drag(dialog):
            user32 = ctypes.windll.user32
            set_cursor_pos = user32.SetCursorPos
            set_cursor_pos.argtypes = [ctypes.c_int, ctypes.c_int]
            set_cursor_pos.restype = ctypes.c_bool
            mouse_event = user32.mouse_event
            mouse_event.argtypes = [
                ctypes.wintypes.DWORD,
                ctypes.c_long,
                ctypes.c_long,
                ctypes.wintypes.DWORD,
                ctypes.c_ulong,
            ]
            mouse_event.restype = None
            move = 0x0001
            left_down = 0x0002
            left_up = 0x0004

            class CursorInfo(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.wintypes.DWORD),
                    ("flags", ctypes.wintypes.DWORD),
                    ("hCursor", ctypes.wintypes.HCURSOR),
                    ("ptScreenPos", ctypes.wintypes.POINT),
                ]

            get_cursor_info = user32.GetCursorInfo
            get_cursor_info.argtypes = [ctypes.POINTER(CursorInfo)]
            get_cursor_info.restype = ctypes.c_bool
            load_cursor = user32.LoadCursorW
            load_cursor.restype = ctypes.wintypes.HCURSOR
            bring_window_to_top = user32.BringWindowToTop
            bring_window_to_top.argtypes = [ctypes.wintypes.HWND]
            bring_window_to_top.restype = ctypes.c_bool
            set_foreground_window = user32.SetForegroundWindow
            set_foreground_window.argtypes = [ctypes.wintypes.HWND]
            set_foreground_window.restype = ctypes.c_bool
            set_active_window = user32.SetActiveWindow
            set_active_window.argtypes = [ctypes.wintypes.HWND]
            set_active_window.restype = ctypes.wintypes.HWND
            get_foreground_window = user32.GetForegroundWindow
            get_foreground_window.restype = ctypes.wintypes.HWND

            def current_cursor_handle():
                info = CursorInfo()
                info.cbSize = ctypes.sizeof(CursorInfo)
                if not get_cursor_info(ctypes.byref(info)):
                    return 0, False
                return int(info.hCursor or 0), bool(int(info.flags) & 0x00000001)

            def focus_dialog_window():
                hwnd = ctypes.wintypes.HWND(int(dialog.winId()))
                try:
                    bring_window_to_top(hwnd)
                    set_active_window(hwnd)
                    set_foreground_window(hwnd)
                except Exception:
                    pass
                QApplication.processEvents()
                return int(get_foreground_window() or 0)

            def settle_cursor_at_point(point):
                set_cursor_pos(int(point.x() - 2), int(point.y() - 2))
                QApplication.processEvents()
                time.sleep(0.045)
                set_cursor_pos(int(point.x()), int(point.y()))
                mouse_event(move, 1, 0, 0, 0)
                QApplication.processEvents()
                time.sleep(0.035)
                set_cursor_pos(int(point.x()), int(point.y()))
                for _ in range(18):
                    QApplication.processEvents()
                    time.sleep(0.010)
                try:
                    getattr(dialog, "_poll_settings_resize_hover_cursor")()
                except Exception:
                    pass
                first = current_cursor_handle()
                for _ in range(9):
                    QApplication.processEvents()
                    time.sleep(0.010)
                try:
                    getattr(dialog, "_poll_settings_resize_hover_cursor")()
                except Exception:
                    pass
                second = current_cursor_handle()
                return second if second[0] else first

            expected_cursor = int(load_cursor(None, 32642) or 0)
            arrow_cursor = int(load_cursor(None, 32512) or 0)
            before = dialog.geometry()
            foreground_after_focus = focus_dialog_window()
            start_global = dialog.mapToGlobal(dialog.rect().bottomRight() - QPoint(8, 8))
            end_global = start_global + QPoint(170, 120)
            cursor_before_drag, cursor_visible = settle_cursor_at_point(start_global)
            cursor_edges = getattr(dialog, "_settings_resize_edges_for_screen_point")(start_global)
            cursor_edges_under = getattr(dialog, "_settings_resize_edges_under_cursor")()[1]
            cursor_key = getattr(dialog, "_settings_resize_cursor_key", None)
            point_belongs = getattr(dialog, "_settings_point_belongs_to_window")(start_global)
            cursor_matches_resize = cursor_visible and expected_cursor and cursor_before_drag == expected_cursor
            cursor_changed_from_arrow = cursor_visible and arrow_cursor and cursor_before_drag != arrow_cursor
            mouse_event(left_down, 0, 0, 0, 0)
            try:
                for step in range(1, 38):
                    x = int(start_global.x() + (end_global.x() - start_global.x()) * step / 37)
                    y = int(start_global.y() + (end_global.y() - start_global.y()) * step / 37)
                    set_cursor_pos(x, y)
                    mouse_event(move, 0, 0, 0, 0)
                    QApplication.processEvents()
                    time.sleep(0.008)
            finally:
                mouse_event(left_up, 0, 0, 0, 0)
            pump(220)
            after = dialog.geometry()
            return {
                "before": {
                    "x": before.x(),
                    "y": before.y(),
                    "width": before.width(),
                    "height": before.height(),
                },
                "after": {
                    "x": after.x(),
                    "y": after.y(),
                    "width": after.width(),
                    "height": after.height(),
                },
                "widthDelta": after.width() - before.width(),
                "heightDelta": after.height() - before.height(),
                "start": {"x": start_global.x(), "y": start_global.y()},
                "end": {"x": end_global.x(), "y": end_global.y()},
                "maximum": {
                    "width": dialog.maximumWidth(),
                    "height": dialog.maximumHeight(),
                },
                "minimum": {
                    "width": dialog.minimumWidth(),
                    "height": dialog.minimumHeight(),
                },
                "cursorBeforeDrag": {
                    "handle": cursor_before_drag,
                    "expectedResizeCursor": expected_cursor,
                    "arrowCursor": arrow_cursor,
                    "visible": cursor_visible,
                    "matchesResizeCursor": cursor_matches_resize,
                    "changedFromArrow": cursor_changed_from_arrow,
                    "edgesForScreen": str(cursor_edges),
                    "edgesUnderCursor": str(cursor_edges_under),
                    "cursorKey": str(cursor_key),
                    "foregroundAfterFocus": foreground_after_focus,
                    "dialogWindowHandle": int(dialog.winId()),
                    "settingsHoverPollTickedForValidation": True,
                    "pointBelongsToWindow": bool(point_belongs),
                    "startPointInsideResizeRail": bool(getattr(cursor_edges, "value", cursor_edges)),
                },
                "resizeActiveAfterRelease": bool(getattr(dialog, "_settings_resize_active", False)),
                "windowResizeBehavior": str(dialog.property("windowResizeBehavior") or ""),
            }

        try:
            opener = getattr(window, "open_resident_access_settings", None)
            if not callable(opener):
                record_step(
                    "settings_open_route_available",
                    "Runtime exposes the FAM-003 Global Settings open route",
                    False,
                    "open_resident_access_settings is unavailable",
                )
                write_manifest("FAIL", "open_resident_access_settings unavailable")
                return
            opener(source="fam003_settings_live_resize_precheck", focus="quick_access")
            pump(700)
            dialog = getattr(window, "_resident_access_settings_dialog", None)
            open_ok = dialog is not None and dialog.isVisible()
            record_step(
                "settings_window_opened",
                "Global Settings opens through the resident access runtime route",
                open_ok,
                f"dialog_present={dialog is not None}; visible={bool(dialog and dialog.isVisible())}",
            )
            if not open_ok:
                write_manifest("FAIL", "Global Settings did not open")
                return
            dialog.move(160, 120)
            dialog.resize(700, 360)
            dialog.raise_()
            dialog.activateWindow()
            pump(260)
            resize_evidence = drive_resize_drag(dialog)
            resize_ok = (
                resize_evidence["widthDelta"] >= 120
                and resize_evidence["heightDelta"] >= 80
                and resize_evidence["cursorBeforeDrag"]["matchesResizeCursor"]
                and not resize_evidence["resizeActiveAfterRelease"]
                and resize_evidence["windowResizeBehavior"]
                == "uiref-007-frameless-top-level-hover-polled-edge-corner-cursor-app-owned-fallback-8px-edge-12px-corner-no-visible-grip-splitter-travel-76-270-horizontal-overflow-minimum-684x388-dynamic-content-minimum-maximum-840x610-close-intercept-cursor-release-hysteresis-v42"
            )
            record_step(
                "settings_window_user_drag_resize",
                "Global Settings resizes through a real held left-button drag on the reachable resize rail",
                resize_ok,
                (
                    f"delta={resize_evidence['widthDelta']}x{resize_evidence['heightDelta']}; "
                    f"cursorMatchesResize={resize_evidence['cursorBeforeDrag']['matchesResizeCursor']}; "
                    f"behavior={resize_evidence['windowResizeBehavior']}"
                ),
                resize_evidence,
            )
            dirty_dialog = dialog
            if dirty_dialog is not None and getattr(dirty_dialog, "_slot_combos", None):
                combo = dirty_dialog._slot_combos[0]
                if combo.count() > 1:
                    combo.setCurrentIndex((combo.currentIndex() + 1) % combo.count())
                    pump(160)
            dirty_before_shutdown = bool(
                dirty_dialog is not None
                and dirty_dialog.isVisible()
                and getattr(dirty_dialog, "_has_unsaved_changes")()
            )
            do_shutdown()
            pump(260)
            dirty_shutdown_blocked = bool(
                dirty_dialog is not None
                and dirty_dialog.isVisible()
                and not shutdown_started
                and getattr(dirty_dialog, "_close_guard_active", False)
                and dirty_dialog.close_guard_overlay.isVisible()
                and dirty_dialog.property("dirtyCloseInterceptSource") == "client_shutdown"
            )
            record_step(
                "settings_dirty_client_shutdown_guard",
                "Dirty Global Settings blocks the actual client shutdown route before any app close",
                dirty_before_shutdown and dirty_shutdown_blocked,
                (
                    f"dirtyBefore={dirty_before_shutdown}; shutdownStarted={shutdown_started}; "
                    f"dialogVisible={bool(dirty_dialog and dirty_dialog.isVisible())}; "
                    f"guard={bool(dirty_dialog and getattr(dirty_dialog, '_close_guard_active', False))}; "
                    f"source={dirty_dialog.property('dirtyCloseInterceptSource') if dirty_dialog else None!r}"
                ),
                {
                    "dirtyBeforeShutdown": dirty_before_shutdown,
                    "shutdownStarted": shutdown_started,
                    "dialogVisible": bool(dirty_dialog and dirty_dialog.isVisible()),
                    "guardActive": bool(dirty_dialog and getattr(dirty_dialog, "_close_guard_active", False)),
                    "interceptSource": str(dirty_dialog.property("dirtyCloseInterceptSource") if dirty_dialog else ""),
                },
            )
            if dirty_dialog is not None and dirty_dialog.isVisible() and getattr(dirty_dialog, "_close_guard_active", False):
                dirty_dialog.guard_cancel_button.click()
                pump(180)
            cancel_kept_alive = bool(
                dirty_dialog is not None
                and dirty_dialog.isVisible()
                and not shutdown_started
                and getattr(dirty_dialog, "_has_unsaved_changes")()
                and not getattr(dirty_dialog, "_close_guard_active", False)
                and dirty_dialog.property("dirtyCloseResolution") == "cancel-preserved-dirty-window-open"
            )
            record_step(
                "settings_dirty_client_shutdown_cancel",
                "Cancel keeps the dirty Settings window and client alive after shutdown guard",
                cancel_kept_alive,
                (
                    f"shutdownStarted={shutdown_started}; dialogVisible={bool(dirty_dialog and dirty_dialog.isVisible())}; "
                    f"dirty={bool(dirty_dialog and getattr(dirty_dialog, '_has_unsaved_changes')())}; "
                    f"resolution={dirty_dialog.property('dirtyCloseResolution') if dirty_dialog else None!r}"
                ),
            )
            status = "PASS" if all(step["codexPrecheck"] == "PASS" for step in steps) else "FAIL"
            write_manifest(status)
        except Exception as exc:
            record_step(
                "settings_live_resize_exception",
                "FAM-003 Settings live resize precheck exception",
                False,
                f"{type(exc).__name__}: {exc}",
            )
            write_manifest("FAIL", f"{type(exc).__name__}: {exc}")
        finally:
            if fam003_settings_live_resize_exits_after_run():
                QTimer.singleShot(500, do_shutdown)

    def settle_passive_default_handoff():
        if exit_if_startup_abort_requested(hotkeys, tray_entry):
            app.quit()
            return
        window.set_visual_state("dormant")
        core_window.set_visual_state("dormant")
        runtime_milestone("RENDERER_MAIN|PASSIVE_DEFAULT_HANDOFF_REQUESTED|state=dormant")
        if desktop_settled_signal.signal():
            runtime_milestone("RENDERER_MAIN|DESKTOP_SETTLED_SIGNAL_SET")
        if write_desktop_settled_signal_file():
            runtime_milestone("RENDERER_MAIN|DESKTOP_SETTLED_SIGNAL_FILE_SET")
        runtime_milestone(AUTHORITATIVE_DESKTOP_SETTLED_MARKER)

    startup_ready_marked = False

    def mark_startup_ready():
        nonlocal startup_ready_marked
        if startup_ready_marked:
            return
        if exit_if_startup_abort_requested(hotkeys, tray_entry):
            app.quit()
            return
        startup_ready_marked = True
        runtime_milestone("RENDERER_MAIN|STARTUP_READY")
        tray_entry.show_discovery_cue()
        settle_passive_default_handoff()
        if real_client_tray_precheck_manifest_path():
            QTimer.singleShot(800, run_real_client_tray_precheck)
        if fam003_settings_live_resize_manifest_path():
            QTimer.singleShot(950, run_fam003_settings_live_resize_precheck)

    window_show_requested = False

    def show_window_after_core_visualization_ready():
        nonlocal window_show_requested
        if window_show_requested:
            return
        if exit_if_startup_abort_requested(hotkeys, tray_entry):
            app.quit()
            return
        window_show_requested = True
        core_window.show()
        if monitoring_hud_dashboard_visible_at_startup:
            window.show()
            runtime_milestone("RENDERER_MAIN|WINDOW_SHOW_REQUESTED|reason=core_and_hud_visualization_ready|surfaces=core_and_dashboard|monitoring_hud_startup=enabled")
        else:
            runtime_milestone("RENDERER_MAIN|WINDOW_SHOW_REQUESTED|reason=core_visualization_ready|surfaces=core_only|monitoring_hud_startup=suppressed")
            runtime_milestone(
                "RENDERER_MAIN|MONITORING_HUD_STARTUP_SUPPRESSED"
                f"|surface=dashboard|overlay=deferred|feature_enabled={str(monitoring_hud_feature_enabled_at_startup).lower()}"
            )

    core_window.core_visualization_ready.connect(show_window_after_core_visualization_ready)
    if monitoring_hud_dashboard_visible_at_startup:
        window.core_visualization_visible.connect(mark_startup_ready)
    else:
        core_window.core_visualization_visible.connect(mark_startup_ready)
    runtime_milestone("RENDERER_MAIN|WINDOW_SHOW_DEFERRED_UNTIL_CORE_READY")
    if core_window.is_core_visualization_ready():
        QTimer.singleShot(0, show_window_after_core_visualization_ready)

    relaunch_timer = QTimer()
    relaunch_timer.timeout.connect(poll_relaunch_request)
    relaunch_timer.start(200)

    exit_code = app.exec()
    if shutdown_force_kill_timer is not None:
        shutdown_force_kill_timer.cancel()
    if shutdown_cleanup_timeout_timer is not None:
        shutdown_cleanup_timeout_timer.stop()
    relaunch_timer.stop()
    relaunch_signal.close()
    desktop_settled_signal.close()
    tray_entry.close()
    hotkeys.stop()
    runtime_milestone(f"RENDERER_MAIN|EVENT_LOOP_EXIT|code={exit_code}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
