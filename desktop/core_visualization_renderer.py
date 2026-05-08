import os

from PySide6.QtCore import Qt, QTimer, QUrl, QRect, Signal
from PySide6.QtGui import QColor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout, QWidget

from .workerw_utils import (
    attach_window_to_desktop,
    make_window_noninteractive,
    position_desktop_child,
)


class CoreVisualizationWindow(QWidget):
    """Independent ORIN persona Core visualization window.

    FAM-006 HUD surfaces may be launched beside this window, but the Core
    visual must not depend on HUD render files or HUD runtime state.
    """

    core_visualization_ready = Signal()
    core_visualization_visible = Signal()

    def __init__(self, screen, visual_html_path: str, event_logger=None):
        super().__init__()
        self.screen_ref = screen
        self.visual_html_path = os.path.abspath(visual_html_path)
        self.event_logger = event_logger
        self._page_ready = False
        self._is_shutting_down = False
        self._pending_visual_state = "dormant"
        self._pending_voice_level = None
        self._desktop_layer_attached = False
        self._desktop_layer_logged = False
        self._visible_logged = False

        self.setWindowTitle("Nexus Desktop AI - ORIN Core")
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setGeometry(self.compute_core_geometry())

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.webview = QWebEngineView(self)
        self.webview.setStyleSheet("background-color: rgb(0, 0, 0); border: none;")
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.setFocusPolicy(Qt.NoFocus)
        self.webview.page().setBackgroundColor(QColor(0, 0, 0))
        self.webview.loadFinished.connect(self._on_load_finished)
        self.webview.load(QUrl.fromLocalFile(self.visual_html_path))
        root.addWidget(self.webview)

    def _log_event(self, event):
        if callable(self.event_logger):
            try:
                self.event_logger(event)
            except Exception:
                pass

    def compute_core_geometry(self):
        g = self.screen_ref.availableGeometry()
        width = min(max(680, int(g.width() * 0.38)), 980)
        height = min(max(620, int(g.height() * 0.72)), 1040)
        x = g.x() + max(0, (g.width() - width) // 2)
        y = g.y() + max(0, (g.height() - height) // 2)
        return QRect(x, y, width, height)

    def desktop_screen_geometry(self):
        return self.compute_core_geometry()

    def is_core_visualization_ready(self):
        return self._page_ready

    def _apply_desktop_layer_mode(self, source: str = "runtime"):
        if self._is_shutting_down:
            return
        geometry = self.compute_core_geometry()
        self.setGeometry(geometry)
        try:
            hwnd = int(self.winId())
            self._desktop_layer_attached = bool(attach_window_to_desktop(hwnd))
            if self._desktop_layer_attached:
                make_window_noninteractive(hwnd)
                position_desktop_child(
                    hwnd,
                    geometry.x(),
                    geometry.y(),
                    geometry.width(),
                    geometry.height(),
                )
            else:
                self.setAttribute(Qt.WA_ShowWithoutActivating, True)
                self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
                self.setFocusPolicy(Qt.NoFocus)
        except Exception as exc:
            self._desktop_layer_attached = False
            self._log_event(
                "RENDERER_MAIN|CORE_VISUALIZATION_DESKTOP_LAYER_FAILED"
                f"|surface=separate_persona_core|source={source}|error={type(exc).__name__}"
            )
            return

        if self._desktop_layer_attached:
            self._log_event(
                "RENDERER_MAIN|CORE_VISUALIZATION_DESKTOP_LAYER_READY"
                "|surface=separate_persona_core"
                "|desktop_layer=workerw"
                "|hud_attachment=none"
                "|dashboard_attachment=none"
                "|overlay_attachment=none"
                "|ncp_attachment=none"
                f"|source={source}"
            )
            self._desktop_layer_logged = True
        else:
            self._log_event(
                "RENDERER_MAIN|CORE_VISUALIZATION_DESKTOP_LAYER_FALLBACK"
                "|surface=separate_persona_core"
                "|desktop_layer=unavailable"
                "|hud_attachment=none"
                "|dashboard_attachment=none"
                "|overlay_attachment=none"
                "|ncp_attachment=none"
                f"|source={source}"
            )

    def _on_load_finished(self, ok):
        if not ok:
            self._log_event("RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_LOAD_FAILED")
            return
        self._page_ready = True
        self._apply_desktop_layer_mode(source="load_finished")
        self._apply_pending_visual_state()
        self._apply_pending_voice_level()
        self._log_event("RENDERER_MAIN|CORE_VISUALIZATION_READY")
        self._log_event("RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_READY|surface=separate_persona_core")
        geometry = self.geometry()
        screen_geometry = self.screen_ref.availableGeometry()
        center_dx = abs(geometry.center().x() - screen_geometry.center().x())
        center_dy = abs(geometry.center().y() - screen_geometry.center().y())
        self._log_event(
            "RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_GEOMETRY_READY"
            f"|x={geometry.x()}|y={geometry.y()}"
            f"|w={geometry.width()}|h={geometry.height()}"
            f"|screen_x={screen_geometry.x()}|screen_y={screen_geometry.y()}"
            f"|screen_w={screen_geometry.width()}|screen_h={screen_geometry.height()}"
            f"|center_dx={center_dx}|center_dy={center_dy}"
        )
        self._log_event(
            "RENDERER_MAIN|CORE_VISUALIZATION_INDEPENDENT_PRESET_MONITOR_READY"
            "|surface=separate_persona_core"
            "|scope=user_selected_install_monitor"
            "|product_attachment=none"
            f"|desktop_layer={'workerw' if self._desktop_layer_attached else 'fallback'}"
            f"|screen_x={screen_geometry.x()}|screen_y={screen_geometry.y()}"
            f"|screen_w={screen_geometry.width()}|screen_h={screen_geometry.height()}"
        )
        self.core_visualization_ready.emit()

    def showEvent(self, event):
        super().showEvent(event)
        if self._page_ready:
            self._apply_desktop_layer_mode(source="show_event")
            if not self._visible_logged:
                self._log_event("RENDERER_MAIN|CORE_VISUALIZATION_WINDOW_VISIBLE|surface=separate_persona_core")
                self._visible_logged = True
            self.core_visualization_visible.emit()

    def _apply_pending_visual_state(self):
        if not self._page_ready:
            return
        state = repr(self._pending_visual_state or "dormant")
        self.webview.page().runJavaScript(
            f"""
            if (window.setVisualState) {{
                window.setVisualState({state});
            }} else {{
                document.body.className = document.body.className
                    .replace(/\\bstate-\\S+/g, "")
                    .trim();
                document.body.classList.add("state-" + {state});
            }}
            """
        )

    def _apply_pending_voice_level(self):
        if not self._page_ready or self._pending_voice_level is None:
            return
        level = max(0.0, min(1.0, float(self._pending_voice_level)))
        self.webview.page().runJavaScript(
            f"window.setCoreVoiceLevel && window.setCoreVoiceLevel({level:.4f});"
        )
        self._pending_voice_level = None

    def set_visual_state(self, state_name):
        self._pending_visual_state = state_name
        self._apply_pending_visual_state()

    def set_voice_level(self, level):
        self._pending_voice_level = level
        self._apply_pending_voice_level()

    def request_shutdown(self):
        self._is_shutting_down = True
        try:
            self.close()
        except RuntimeError:
            return
        try:
            QTimer.singleShot(0, self.deleteLater)
        except RuntimeError:
            return
