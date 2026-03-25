import os
import ctypes

from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer, QUrl, QRect
from PySide6.QtGui import QColor
from PySide6.QtWebEngineWidgets import QWebEngineView

from .workerw_utils import attach_window_to_desktop, make_window_noninteractive

WM_NCHITTEST = 0x0084
HTTRANSPARENT = -1


class DesktopJarvisWindow(QWidget):
    def __init__(self, screen, visual_html_path: str):
        super().__init__()

        self.screen_ref = screen
        self.visual_html_path = os.path.abspath(visual_html_path)

        self.desktop_mode = False
        self._is_shutting_down = False

        # Window configuration (Concept 2 test)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("background: transparent;")

        self.setGeometry(self.compute_compact_geometry())

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.webview = QWebEngineView(self)
        self.webview.setAttribute(Qt.WA_TranslucentBackground, True)
        self.webview.setStyleSheet("background: transparent; border: none;")
        self.webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.webview.setFocusPolicy(Qt.NoFocus)

        self.webview.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self.webview.load(QUrl.fromLocalFile(self.visual_html_path))

        root.addWidget(self.webview)

    def compute_compact_geometry(self):
        g = self.screen_ref.geometry()

        width = int(g.width() * 0.46)
        height = int(g.height() * 0.68)

        x = g.x() + (g.width() - width) // 2
        y = g.y() + int(g.height() * 0.08)

        return QRect(x, y, width, height)

    def showEvent(self, event):
        super().showEvent(event)

        if not self.desktop_mode:
            QTimer.singleShot(50, self.enable_desktop_mode)

    def nativeEvent(self, eventType, message):
        if self.desktop_mode:
            msg = ctypes.wintypes.MSG.from_address(int(message))

            if msg.message == WM_NCHITTEST:
                return True, HTTRANSPARENT

        return super().nativeEvent(eventType, message)

    def enable_desktop_mode(self):
        if self.desktop_mode or self._is_shutting_down:
            return

        self.desktop_mode = True

        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.hide()
        self.show()

        hwnd = int(self.winId())

        attach_window_to_desktop(hwnd)
        make_window_noninteractive(hwnd)

        self.lower()

    def request_shutdown(self):
        if self._is_shutting_down:
            return

        self._is_shutting_down = True

        self.webview.stop()
        self.hide()
        self.close()

        app = QApplication.instance()

        if app is not None:
            QTimer.singleShot(0, app.quit)