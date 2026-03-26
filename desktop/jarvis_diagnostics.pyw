# Version 1.3.2 rev 13 diagnostics UI

import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QLabel, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QFont, QGuiApplication

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(ROOT_DIR, "logs")
CRASH_FOLDER = os.path.join(LOG_DIR, "crash")
STATUS_FILE = os.path.join(LOG_DIR, "diagnostics_status.txt")
STOP_SIGNAL_FILE = os.path.join(LOG_DIR, "diagnostics_stop.signal")
RUNTIME_LOG_FILE = ""


def ui_runtime(msg):
    if not RUNTIME_LOG_FILE:
        return
    try:
        import datetime
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        with open(RUNTIME_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] UI|{msg}\n")
    except Exception:
        pass


def parse_runtime_log_arg(argv):
    global RUNTIME_LOG_FILE
    for i, arg in enumerate(argv):
        if arg == "--runtime-log" and i + 1 < len(argv):
            RUNTIME_LOG_FILE = argv[i + 1]
            return

    env_runtime = os.environ.get("JARVIS_RUNTIME_LOG", "").strip()
    if env_runtime:
        RUNTIME_LOG_FILE = env_runtime


class DiagnosticsWindow(QWidget):
    def __init__(self):
        super().__init__()

        ui_runtime("DiagnosticsWindow.__init__ start")

        self.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.resize(920, 660)
        ui_runtime(f"Initial window size set: {self.width()}x{self.height()}")

        self.setStyleSheet("""
        QWidget {
            background: #05090d;
            color: #6ee7ff;
        }

        QLabel {
            color: #6ee7ff;
        }

        QFrame.panel {
            border: 1px solid #00e1ff;
            border-radius: 8px;
            background: #031018;
        }

        QTextEdit {
            background: #02070b;
            border: 1px solid #00e1ff;
            border-radius: 6px;
            color: #6ee7ff;
            font-family: Consolas;
            font-size: 11pt;
            padding: 4px;
            selection-background-color: #0a3a46;
        }

        QTextEdit QScrollBar:vertical {
            background: #031018;
            width: 12px;
            margin: 2px;
            border: 1px solid #00b8d9;
            border-radius: 6px;
        }

        QTextEdit QScrollBar::handle:vertical {
            background: #00cfff;
            min-height: 24px;
            border-radius: 5px;
            border: 1px solid #7befff;
        }

        QTextEdit QScrollBar::add-line:vertical,
        QTextEdit QScrollBar::sub-line:vertical {
            background: transparent;
            height: 0px;
            border: none;
        }

        QTextEdit QScrollBar::add-page:vertical,
        QTextEdit QScrollBar::sub-page:vertical {
            background: #031018;
            border-radius: 4px;
        }

        QPushButton {
            background: #07151b;
            border: 1px solid #00e1ff;
            border-radius: 8px;
            padding: 8px;
            color: #6ee7ff;
        }

        QPushButton:hover {
            background: #0f2a35;
        }
        """)

        root = QVBoxLayout()
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(10)

        self.stark = QLabel("STARK INDUSTRIES")
        self.stark.setAlignment(Qt.AlignCenter)
        self.stark.setFont(QFont("Consolas", 18, QFont.Bold))
        self.stark.setStyleSheet("color:#d4af37;")
        root.addWidget(self.stark)

        title = QLabel("J.A.R.V.I.S. SYSTEM DIAGNOSTICS")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Consolas", 13, QFont.Bold))
        root.addWidget(title)

        self.summary = QLabel("Failure Summary: waiting for diagnostic input...")
        self.summary.setAlignment(Qt.AlignCenter)
        root.addWidget(self.summary)

        trace_title = QLabel("DIAGNOSTIC TRACE")
        trace_title.setFont(QFont("Consolas", 11, QFont.Bold))
        trace_title.setContentsMargins(0, 10, 0, 4)
        root.addWidget(trace_title)

        trace_panel = QFrame()
        trace_panel.setObjectName("panel")
        trace_layout = QVBoxLayout()
        trace_layout.setContentsMargins(4, 3, 4, 4)

        self.trace = QTextEdit()
        self.trace.setReadOnly(True)
        trace_layout.addWidget(self.trace)
        trace_panel.setLayout(trace_layout)
        root.addWidget(trace_panel, 3)

        jarvis_title = QLabel("JARVIS")
        jarvis_title.setFont(QFont("Consolas", 11, QFont.Bold))
        jarvis_title.setContentsMargins(0, 10, 0, 4)
        root.addWidget(jarvis_title)

        speech_panel = QFrame()
        speech_panel.setObjectName("panel")
        speech_layout = QVBoxLayout()
        speech_layout.setContentsMargins(4, 3, 4, 4)

        self.speech = QTextEdit()
        self.speech.setReadOnly(True)
        self.speech.setMinimumHeight(120)
        speech_layout.addWidget(self.speech)
        speech_panel.setLayout(speech_layout)
        root.addWidget(speech_panel, 1)

        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Open Crash Folder")
        open_btn.clicked.connect(self.open_crash)

        dismiss_btn = QPushButton("Dismiss")
        dismiss_btn.clicked.connect(self.dismiss_diagnostics)

        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(dismiss_btn)
        root.addLayout(btn_layout)

        self.setLayout(root)
        ui_runtime("Layout initialized: trace_panel=3, speech_panel=1, resizable window enabled")

        self.dragPos = QPoint()
        self._seen = 0
        self.voice_history = []
        self.voice_current = ""
        self.current_state = "STARTED"
        self._last_rendered_state = ""

        self.move_to_right_monitor()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_status)
        self.timer.start(80)

    def move_to_right_monitor(self):
        screens = QGuiApplication.screens()
        target = max(screens, key=lambda s: s.geometry().x())
        geo = target.geometry()
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)
        ui_runtime(f"Moved to monitor: x={geo.x()} y={geo.y()} w={geo.width()} h={geo.height()} :: window=({x},{y},{self.width()},{self.height()})")

    def showEvent(self, event):
        super().showEvent(event)
        ui_runtime(f"showEvent :: visible size={self.width()}x{self.height()} pos=({self.x()},{self.y()})")
        QTimer.singleShot(0, self.raise_)
        QTimer.singleShot(25, self.raise_)

    def dismiss_diagnostics(self):
        ui_runtime(f"Dismiss button clicked :: current_state={self.current_state}")
        self.cleanup_and_exit()

    def cleanup_and_exit(self):
        ui_runtime(f"cleanup_and_exit start :: current_state={self.current_state}")
        try:
            self.timer.stop()
        except Exception:
            pass

        if self.current_state in ("STARTED", "RECOVERING"):
            try:
                with open(STOP_SIGNAL_FILE, "w", encoding="utf-8") as f:
                    f.write("dismissed")
                ui_runtime("Stop signal created due to early dismiss")
            except Exception:
                pass

        if self.current_state == "COMPLETE":
            for cleanup_path in (STOP_SIGNAL_FILE, STATUS_FILE):
                try:
                    if os.path.exists(cleanup_path):
                        os.remove(cleanup_path)
                        ui_runtime(f"Removed completion cleanup file: {cleanup_path}")
                except Exception:
                    pass

        try:
            self.hide()
            ui_runtime("Window hidden during cleanup")
        except Exception:
            pass

        app = QApplication.instance()
        if app:
            ui_runtime("Requesting QApplication quit")
            app.quit()

        ui_runtime("Process exiting via os._exit(0)")
        os._exit(0)

    def closeEvent(self, event):
        ui_runtime(f"closeEvent accepted :: current_state={self.current_state}")
        event.accept()
        self.cleanup_and_exit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        ui_runtime(f"resizeEvent :: width={size.width()} height={size.height()}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            diff = event.globalPosition().toPoint() - self.dragPos
            self.move(self.pos() + diff)
            self.dragPos = event.globalPosition().toPoint()

    def render_voice_panel(self):
        lines = list(self.voice_history)
        if self.voice_current:
            lines.append(self.voice_current)
        self.speech.setPlainText("\n".join(lines))
        self.speech.verticalScrollBar().setValue(self.speech.verticalScrollBar().maximum())

    def append_trace(self, payload):
        self.trace.append(payload)
        self.trace.verticalScrollBar().setValue(self.trace.verticalScrollBar().maximum())

    def poll_status(self):
        if not os.path.exists(STATUS_FILE):
            return

        try:
            with open(STATUS_FILE, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return

        new = lines[self._seen:]
        self._seen = len(lines)

        for raw in new:
            line = raw.strip()
            if not line or "|" not in line:
                continue

            kind, payload = line.split("|", 1)

            if kind == "SUMMARY":
                self.summary.setText("Failure Summary: " + payload)

            elif kind == "STATE":
                state = payload.strip()
                self.current_state = state

                mapping = {
                    "STARTED": "Jarvis State: Starting Diagnostics",
                    "RECOVERING": "Jarvis State: Attempting Recovery",
                    "COMPLETE": "Jarvis State: Offline",
                }

                should_render = True
                if state == "RECOVERING" and self._last_rendered_state == "RECOVERING":
                    should_render = False

                if should_render:
                    display = mapping.get(state, f"Jarvis State: {state}")
                    ui_runtime(f"State updated :: {state}")
                    self.append_trace("")
                    self.append_trace(display)
                    self.append_trace("---------------------------------------------------")
                    self.append_trace("")
                    self._last_rendered_state = state

            elif kind == "TRACE":
                self.append_trace(payload)

            elif kind == "VOICE_CLEAR":
                self.voice_current = ""
                self.render_voice_panel()

            elif kind == "VOICE_SYNC":
                self.voice_current = payload
                self.render_voice_panel()

            elif kind == "VOICE_FINAL":
                final_line = payload.strip()
                self.voice_current = ""
                if final_line and (not self.voice_history or self.voice_history[-1] != final_line):
                    self.voice_history.append(final_line)
                    ui_runtime(f"VOICE_FINAL appended :: {final_line}")
                self.render_voice_panel()

    def open_crash(self):
        if os.path.exists(CRASH_FOLDER):
            os.startfile(CRASH_FOLDER)

def main():
    parse_runtime_log_arg(sys.argv)
    ui_runtime(f"Diagnostics process starting :: runtime_log={RUNTIME_LOG_FILE or 'UNSET'}")
    ui_runtime(f"Diagnostics status target :: {STATUS_FILE}")
    ui_runtime(f"Diagnostics stop target :: {STOP_SIGNAL_FILE}")
    app = QApplication(sys.argv)
    w = DiagnosticsWindow()
    w.show()
    ui_runtime("Diagnostics window shown")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
