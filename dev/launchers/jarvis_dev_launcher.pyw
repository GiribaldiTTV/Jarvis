import os
import subprocess
import sys

from PySide6.QtCore import QPoint, QRect, Qt, QTimer
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEV_LAUNCHERS_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
SUPPORT_BUNDLE_TRIAGE_SCRIPT = os.path.join(ROOT_DIR, "dev", "jarvis_support_bundle_triage.py")

PYTHONW_PATH = r"C:\Users\anden\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe"

LANE_CONFIG = {
    "diagnostics": {
        "label": "Diagnostics UI Test",
        "detail": (
            "Launches the standalone diagnostics window with safe manual test content. "
            "Best for focus, monitor, dismiss, and passive-window checks."
        ),
        "quiet_launcher": "launch_jarvis_diagnostics_manual_test.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": LOGS_DIR,
        "runtime_fixed": os.path.join(LOGS_DIR, "Runtime_manual_diagnostics_test.txt"),
        "crash_folder": "",
    },
    "repeatedCrash": {
        "label": "Repeated-Crash Failure Lane",
        "detail": (
            "Exercises the real launcher recovery path using a deterministic repeated crash "
            "target until diagnostics completion."
        ),
        "quiet_launcher": "launch_jarvis_launcher_failure_manual_test.vbs",
        "voice_launcher": "launch_jarvis_launcher_failure_manual_test_with_voice.vbs",
        "supports_voice": True,
        "log_root": os.path.join(LOGS_DIR, "manual_launcher_failure_test"),
        "log_root_with_voice": os.path.join(LOGS_DIR, "manual_launcher_failure_test_with_voice"),
        "crash_folder": "crash",
    },
    "startupAbort": {
        "label": "Startup-Abort Lane",
        "detail": (
            "Exercises launcher stall observation, cooperative startup abort, recovery, "
            "and diagnostics completion."
        ),
        "quiet_launcher": "launch_jarvis_launcher_startup_abort_manual_test.vbs",
        "voice_launcher": "launch_jarvis_launcher_startup_abort_manual_test_with_voice.vbs",
        "supports_voice": True,
        "log_root": os.path.join(LOGS_DIR, "manual_launcher_startup_abort_test"),
        "log_root_with_voice": os.path.join(LOGS_DIR, "manual_launcher_startup_abort_test_with_voice"),
        "crash_folder": "crash",
    },
    "voiceRegression": {
        "label": "Voice Regression Harness",
        "detail": (
            "Runs the contained FB-018 voice regression harness across the current launcher-owned "
            "voice lanes and direct diagnostics voice probes, then writes a pass/fail report."
        ),
        "quiet_launcher": "launch_jarvis_voice_regression_harness.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "voice_regression_harness"),
        "report_root": os.path.join(LOGS_DIR, "voice_regression_harness", "reports"),
        "report_prefix": "VoiceRegressionReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "desktopHealthy": {
        "label": "Healthy Desktop Launch Validation",
        "detail": (
            "Runs a contained offscreen validation of the current default desktop renderer target "
            "and verifies healthy startup milestones such as WINDOW_SHOW_CALLED and STARTUP_READY."
        ),
        "quiet_launcher": "launch_jarvis_desktop_entrypoint_validation.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "desktop_entrypoint_validation"),
        "report_root": os.path.join(LOGS_DIR, "desktop_entrypoint_validation", "reports"),
        "report_prefix": "DesktopEntrypointValidationReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "launcherHealthy": {
        "label": "Healthy Launcher Path Validation",
        "detail": (
            "Runs the real desktop launcher against its current default target, waits for "
            "launcher-owned healthy startup markers, then triggers a controlled shutdown and "
            "captures reusable pass/fail evidence for the contained healthy path."
        ),
        "quiet_launcher": "launch_jarvis_desktop_launcher_healthy_validation.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "desktop_launcher_healthy_validation"),
        "report_root": os.path.join(LOGS_DIR, "desktop_launcher_healthy_validation", "reports"),
        "report_prefix": "DesktopLauncherHealthyValidationReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "launcherRegression": {
        "label": "Desktop Launcher Regression Harness",
        "detail": (
            "Runs the contained desktop launcher regression harness across the current healthy, "
            "repeated-crash, and startup-abort launcher paths, then writes one consolidated "
            "pass/fail report."
        ),
        "quiet_launcher": "launch_jarvis_desktop_launcher_regression_harness.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "desktop_launcher_regression_harness"),
        "report_root": os.path.join(LOGS_DIR, "desktop_launcher_regression_harness", "reports"),
        "report_prefix": "DesktopLauncherRegressionHarnessReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "supportBundleTriageHarness": {
        "label": "Support Bundle Triage Harness",
        "detail": (
            "Runs the contained FB-019 support-bundle triage regression harness across the "
            "current supported launcher-owned bundle classes and safe unknown fallback, then "
            "writes one consolidated pass/fail report."
        ),
        "quiet_launcher": "launch_jarvis_support_bundle_triage_harness.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "support_bundle_triage_harness"),
        "report_root": os.path.join(LOGS_DIR, "support_bundle_triage_harness", "reports"),
        "report_prefix": "SupportBundleTriageHarnessReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "supportBundleTriageToolkitValidation": {
        "label": "Support Bundle Triage Toolkit Validation",
        "detail": (
            "Runs the contained offscreen validator for the raw FB-019 toolkit flow and verifies "
            "toolkit-driven zip-input triage, extracted-folder triage, and latest-report reachability."
        ),
        "quiet_launcher": "launch_jarvis_support_bundle_triage_toolkit_validation.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "support_bundle_triage_toolkit_validation"),
        "report_root": os.path.join(LOGS_DIR, "support_bundle_triage_toolkit_validation", "reports"),
        "report_prefix": "SupportBundleTriageToolkitValidationReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "diagnosticsReportIssueValidation": {
        "label": "Diagnostics Report Issue Validation",
        "detail": (
            "Runs the contained offscreen validator for the production diagnostics Report Issue flow "
            "and verifies support-bundle creation, manifest manual-submission contract fields, and "
            "GitHub issue-prefill open-attempt handling."
        ),
        "quiet_launcher": "launch_jarvis_diagnostics_report_issue_validation.vbs",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "diagnostics_report_issue_validation"),
        "report_root": os.path.join(LOGS_DIR, "diagnostics_report_issue_validation", "reports"),
        "report_prefix": "DiagnosticsReportIssueValidationReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
    },
    "supportBundleTriage": {
        "label": "Support Bundle Triage Helper",
        "detail": (
            "Runs the raw FB-019 support-bundle triage helper against a selected support-bundle "
            ".zip or extracted bundle folder, then writes a compact internal triage report with "
            "the closest current repro lane suggestion."
        ),
        "quiet_launcher": "",
        "voice_launcher": "",
        "supports_voice": False,
        "log_root": os.path.join(LOGS_DIR, "support_bundle_triage"),
        "report_root": os.path.join(LOGS_DIR, "support_bundle_triage", "reports"),
        "report_prefix": "SupportBundleTriageReport_",
        "report_suffix": ".txt",
        "crash_folder": "",
        "requires_bundle_input": True,
        "script_path": SUPPORT_BUNDLE_TRIAGE_SCRIPT,
    },
}

QUICK_LAUNCH_GROUPS = (
    {
        "label": "Diagnostics & Recovery Checks",
        "options": (
            {
                "label": "Diagnostics UI Test (Quiet)",
                "lane_key": "diagnostics",
                "with_voice": False,
                "detail": "Standalone diagnostics window checks without launcher recovery or voice playback.",
            },
            {
                "label": "Repeated-Crash Failure Lane (Quiet)",
                "lane_key": "repeatedCrash",
                "with_voice": False,
                "detail": "Real launcher repeated-crash recovery flow without audio playback.",
            },
            {
                "label": "Repeated-Crash Failure Lane (With Voice / Audio)",
                "lane_key": "repeatedCrash",
                "with_voice": True,
                "detail": "Real launcher repeated-crash recovery flow with dedicated voice-enabled evidence.",
            },
            {
                "label": "Startup-Abort Lane (Quiet)",
                "lane_key": "startupAbort",
                "with_voice": False,
                "detail": "Launcher stall and cooperative startup-abort recovery without audio playback.",
            },
            {
                "label": "Startup-Abort Lane (With Voice / Audio)",
                "lane_key": "startupAbort",
                "with_voice": True,
                "detail": "Launcher stall and cooperative startup-abort recovery with voice-enabled evidence.",
            },
        ),
    },
    {
        "label": "Voice & Launcher Regression",
        "options": (
            {
                "label": "Voice Regression Harness (Quiet)",
                "lane_key": "voiceRegression",
                "with_voice": False,
                "detail": "Contained regression harness for launcher-owned voice lanes and direct diagnostics probes.",
            },
            {
                "label": "Desktop Launcher Regression Harness (Quiet)",
                "lane_key": "launcherRegression",
                "with_voice": False,
                "detail": "Consolidated launcher regression sweep across the healthy and failure-path launcher lanes.",
            },
        ),
    },
    {
        "label": "Healthy Startup Validation",
        "options": (
            {
                "label": "Healthy Desktop Launch Validation (Quiet)",
                "lane_key": "desktopHealthy",
                "with_voice": False,
                "detail": "Contained offscreen validation for the current default desktop renderer target.",
            },
            {
                "label": "Healthy Launcher Path Validation (Quiet)",
                "lane_key": "launcherHealthy",
                "with_voice": False,
                "detail": "Real launcher healthy-path validation with a controlled shutdown and reusable evidence.",
            },
        ),
    },
    {
        "label": "Support Bundles & Reporting",
        "options": (
            {
                "label": "Support Bundle Triage Harness (Quiet)",
                "lane_key": "supportBundleTriageHarness",
                "with_voice": False,
                "detail": "Contained regression harness for supported support-bundle classes and safe unknown fallback.",
            },
        ),
    },
)

CONFIG_LANE_GROUPS = (
    {
        "label": "Diagnostics & Recovery Checks",
        "lane_keys": ("diagnostics", "repeatedCrash", "startupAbort"),
    },
    {
        "label": "Voice, Healthy Start, & Regression",
        "lane_keys": ("voiceRegression", "desktopHealthy", "launcherHealthy", "launcherRegression"),
    },
    {
        "label": "Support Bundles & Reporting",
        "lane_keys": (
            "supportBundleTriageHarness",
            "supportBundleTriageToolkitValidation",
            "diagnosticsReportIssueValidation",
            "supportBundleTriage",
        ),
    },
)


def latest_file_matching(folder_path: str, prefix: str) -> str:
    if not os.path.isdir(folder_path):
        return ""
    best_path = ""
    best_time = -1.0
    for name in os.listdir(folder_path):
        if not name.lower().startswith(prefix.lower()):
            continue
        path = os.path.join(folder_path, name)
        if not os.path.isfile(path):
            continue
        try:
            modified = os.path.getmtime(path)
        except OSError:
            continue
        if modified >= best_time:
            best_time = modified
            best_path = path
    return best_path


class TitleBar(QFrame):
    def __init__(self, owner):
        super().__init__(owner)
        self.owner = owner
        self.drag_active = False
        self.drag_pos = QPoint()
        self.setObjectName("titleBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        title = QLabel("JARVIS DEV TOOLKIT // INTERNAL")
        title.setObjectName("titleBarLabel")
        layout.addWidget(title, 1)

        minimize_btn = QPushButton("MIN")
        minimize_btn.setObjectName("titleBarButton")
        minimize_btn.clicked.connect(self.owner.showMinimized)
        layout.addWidget(minimize_btn)

        dismiss_btn = QPushButton("DISMISS")
        dismiss_btn.setObjectName("titleBarButton")
        dismiss_btn.clicked.connect(self.owner.close)
        layout.addWidget(dismiss_btn)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_active = True
            self.drag_pos = event.globalPosition().toPoint() - self.owner.frameGeometry().topLeft()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_active and (event.buttons() & Qt.LeftButton):
            self.owner.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_active = False
        super().mouseReleaseEvent(event)


class Panel(QFrame):
    def __init__(self, title_text: str):
        super().__init__()
        self.setObjectName("panel")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName("panelTitle")
        self.layout.addWidget(title)


class DevLauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Dev Toolkit")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.resize(980, 720)
        self.setMinimumSize(840, 620)

        self._drag_active = False
        self._resize_active = False
        self._resize_edges = set()
        self._resize_start_pos = QPoint()
        self._resize_start_geom = QRect()
        self._edge_margin = 8
        self.setMouseTracking(True)

        self.pending_launch_key = ""
        self.selected_lane_key = "diagnostics"

        self.launch_timer = QTimer(self)
        self.launch_timer.setSingleShot(True)
        self.launch_timer.timeout.connect(self.run_selected_launcher)

        self.setStyleSheet(
            """
            QWidget {
                background: #04080d;
                color: #6ee7ff;
                font-family: Consolas;
            }

            QFrame#shell {
                background: #061019;
                border: 1px solid #0fe1ff;
            }

            QFrame#titleBar {
                background: #07131b;
                border: 1px solid #0fe1ff;
            }

            QLabel#titleBarLabel {
                color: #9feeff;
                font-size: 12pt;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QPushButton#titleBarButton {
                min-width: 76px;
                padding: 5px 8px;
                border: 1px solid #00d8ff;
                background: #0a1b26;
                color: #f4fbff;
                font-size: 10pt;
            }

            QPushButton#titleBarButton:hover {
                background: #133444;
            }

            QFrame#banner {
                border: 1px solid #0fe1ff;
                background: #07131b;
            }

            QLabel#bannerTop {
                color: #d4af37;
                font-size: 11pt;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#bannerTitle {
                color: #d4af37;
                font-size: 24pt;
                font-weight: 700;
            }

            QLabel#bannerSubtitle {
                color: #ff4c4c;
                font-size: 12pt;
                font-weight: 700;
            }

            QFrame#panel {
                border: 1px solid #0fe1ff;
                background: #08131c;
            }

            QLabel#panelTitle {
                color: #d4af37;
                font-size: 13pt;
                font-weight: 700;
            }

            QLabel#fieldLabel {
                color: #9feeff;
                font-size: 10pt;
                font-weight: 700;
            }

            QPushButton, QComboBox {
                background: #0a1b26;
                border: 1px solid #00d8ff;
                border-radius: 6px;
                color: #f4fbff;
                padding: 10px 8px;
                font-size: 11pt;
            }

            QPushButton:hover, QComboBox:hover {
                background: #12303e;
            }

            QPushButton:disabled, QComboBox:disabled {
                color: #5e8994;
                border-color: #24606d;
                background: #071118;
            }

            QPushButton[checkable="true"] {
                text-align: left;
            }

            QPushButton:checked {
                background: #173847;
                border-color: #7fefff;
                color: #f0fdff;
            }

            QLabel#detailBox, QLabel#noteBox, QLabel#statusBox {
                border: 1px solid #134353;
                background: #06111a;
                padding: 10px;
                color: #9fd7df;
                font-size: 10pt;
            }

            QLabel#statusBox {
                color: #d4af37;
            }

            QLabel#modeLine {
                color: #8cc6cf;
                font-size: 9pt;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: #031018;
                width: 12px;
                margin: 2px;
                border: 1px solid #00b8d9;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #00cfff;
                min-height: 24px;
                border-radius: 5px;
                border: 1px solid #7befff;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: transparent;
                height: 0px;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: #031018;
                border-radius: 4px;
            }

            QScrollBar:horizontal {
                background: #031018;
                height: 12px;
                margin: 2px;
                border: 1px solid #00b8d9;
                border-radius: 6px;
            }

            QScrollBar::handle:horizontal {
                background: #00cfff;
                min-width: 24px;
                border-radius: 5px;
                border: 1px solid #7befff;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: transparent;
                width: 0px;
                border: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: #031018;
                border-radius: 4px;
            }
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        shell = QFrame()
        shell.setObjectName("shell")
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(14, 14, 14, 14)
        shell_layout.setSpacing(12)

        self.title_bar = TitleBar(self)
        shell_layout.addWidget(self.title_bar)

        banner = QFrame()
        banner.setObjectName("banner")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(12, 12, 12, 12)
        banner_layout.setSpacing(4)

        banner_top = QLabel("STARK INDUSTRIES // INTERNAL TOOLING")
        banner_top.setObjectName("bannerTop")
        banner_top.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(banner_top)

        banner_title = QLabel("JARVIS DEV TOOLKIT")
        banner_title.setObjectName("bannerTitle")
        banner_title.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(banner_title)

        banner_subtitle = QLabel("Manual validation launch surface")
        banner_subtitle.setObjectName("bannerSubtitle")
        banner_subtitle.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(banner_subtitle)

        shell_layout.addWidget(banner)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        left_col = QVBoxLayout()
        left_col.setSpacing(12)
        right_col = QVBoxLayout()
        right_col.setSpacing(12)

        quick_panel = Panel("Quick Presets")
        self._add_quick_launches(quick_panel.layout)
        left_col.addWidget(quick_panel)

        config_panel = Panel("Custom Launch")
        self._build_configurable_panel(config_panel.layout)
        left_col.addWidget(config_panel, 1)

        evidence_panel = Panel("Evidence & Utilities")
        self._build_evidence_panel(evidence_panel.layout)
        right_col.addWidget(evidence_panel)

        notes_panel = Panel("Notes")
        notes_label = QLabel(
            "- Quick Presets launch the most common lanes immediately with a fixed audio mode.\n"
            "- Custom Launch lets you choose the lane family, exact lane, launch delay, and audio mode.\n"
            "- Only Repeated-Crash and Startup-Abort support With Voice / Audio.\n"
            "- Support Bundle Triage Helper will ask for a bundle zip or extracted folder when launched.\n"
            "- Production behavior is unchanged unless you explicitly launch one of these internal test lanes."
        )
        notes_label.setObjectName("noteBox")
        notes_label.setWordWrap(True)
        notes_panel.layout.addWidget(notes_label)
        right_col.addWidget(notes_panel)

        status_panel = Panel("Status")
        self.status_label = QLabel("Ready.")
        self.status_label.setObjectName("statusBox")
        self.status_label.setWordWrap(True)
        status_panel.layout.addWidget(self.status_label)
        right_col.addWidget(status_panel)
        right_col.addStretch(1)

        left_widget = QWidget()
        left_widget.setLayout(left_col)
        right_widget = QWidget()
        right_widget.setLayout(right_col)
        content_layout.addWidget(left_widget, 5)
        content_layout.addWidget(right_widget, 4)

        scroll.setWidget(content)
        shell_layout.addWidget(scroll, 1)
        root.addWidget(shell)

        self.center_on_primary()
        self.update_ui()

    def _add_quick_launches(self, layout):
        quick_group_label = QLabel("Purpose")
        quick_group_label.setObjectName("fieldLabel")
        layout.addWidget(quick_group_label)

        self.quick_group_combo = QComboBox()
        for group in QUICK_LAUNCH_GROUPS:
            self.quick_group_combo.addItem(group["label"])
        self.quick_group_combo.currentIndexChanged.connect(self.populate_quick_presets)
        layout.addWidget(self.quick_group_combo)

        quick_preset_label = QLabel("Quick Option")
        quick_preset_label.setObjectName("fieldLabel")
        layout.addWidget(quick_preset_label)

        self.quick_preset_combo = QComboBox()
        self.quick_preset_combo.currentIndexChanged.connect(self.update_quick_detail)
        layout.addWidget(self.quick_preset_combo)

        self.quick_detail_label = QLabel()
        self.quick_detail_label.setObjectName("detailBox")
        self.quick_detail_label.setWordWrap(True)
        layout.addWidget(self.quick_detail_label)

        self.quick_launch_btn = QPushButton("Launch Quick Option")
        self.quick_launch_btn.clicked.connect(self.launch_selected_quick_preset)
        layout.addWidget(self.quick_launch_btn)

        note = QLabel(
            "Use Quick Presets when you want the most common lanes with the audio mode already chosen for you."
        )
        note.setObjectName("noteBox")
        note.setWordWrap(True)
        layout.addWidget(note)

        self.populate_quick_presets()

    def _build_configurable_panel(self, layout):
        lane_group_label = QLabel("Purpose")
        lane_group_label.setObjectName("fieldLabel")
        layout.addWidget(lane_group_label)

        self.lane_group_combo = QComboBox()
        for group in CONFIG_LANE_GROUPS:
            self.lane_group_combo.addItem(group["label"])
        self.lane_group_combo.currentIndexChanged.connect(self.on_lane_group_changed)
        layout.addWidget(self.lane_group_combo)

        lane_choice_label = QLabel("Test / Helper")
        lane_choice_label.setObjectName("fieldLabel")
        layout.addWidget(lane_choice_label)

        self.lane_combo = QComboBox()
        self.lane_combo.currentIndexChanged.connect(self.on_lane_choice_changed)
        layout.addWidget(self.lane_combo)

        self.detail_label = QLabel()
        self.detail_label.setObjectName("detailBox")
        self.detail_label.setWordWrap(True)
        self.detail_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        layout.addWidget(self.detail_label)

        delay_label = QLabel("Launch Delay")
        delay_label.setObjectName("fieldLabel")
        layout.addWidget(delay_label)

        self.delay_combo = QComboBox()
        self.delay_combo.addItems(["Now", "3s", "5s", "10s"])
        self.delay_combo.currentIndexChanged.connect(self.update_ui)
        layout.addWidget(self.delay_combo)

        self.audio_label = QLabel("Audio Mode")
        self.audio_label.setObjectName("fieldLabel")
        self.audio_label.setWordWrap(True)
        layout.addWidget(self.audio_label)

        self.audio_combo = QComboBox()
        self.audio_combo.addItems(["Quiet", "With Voice / Audio"])
        self.audio_combo.currentIndexChanged.connect(self.update_ui)
        layout.addWidget(self.audio_combo)

        self.launch_btn = QPushButton("Launch Selected Lane")
        self.launch_btn.clicked.connect(self.schedule_or_launch)
        layout.addWidget(self.launch_btn)

        self.cancel_btn = QPushButton("Cancel Pending Launch")
        self.cancel_btn.clicked.connect(self.cancel_launch)
        layout.addWidget(self.cancel_btn)

        self.mode_line = QLabel()
        self.mode_line.setObjectName("modeLine")
        self.mode_line.setWordWrap(True)
        layout.addWidget(self.mode_line)

        self.populate_lane_choices("diagnostics")

    def _build_evidence_panel(self, layout):
        buttons = [
            ("Open Selected Log Root", self.open_selected_log_root),
            ("Open Latest Runtime Log", self.open_latest_runtime_log),
            ("Open Crash Folder", self.open_crash_folder),
            ("Open Launchers Folder", self.open_launchers_folder),
        ]
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
            if text == "Open Crash Folder":
                self.crash_folder_btn = btn

        note = QLabel(
            "Evidence helpers follow the currently selected lane and voice mode when lane-specific logs are used."
        )
        note.setObjectName("noteBox")
        note.setWordWrap(True)
        layout.addWidget(note)

    def current_quick_group(self) -> dict:
        index = self.quick_group_combo.currentIndex()
        if index < 0:
            index = 0
        return QUICK_LAUNCH_GROUPS[index]

    def current_quick_selection(self) -> tuple[str, bool]:
        data = self.quick_preset_combo.currentData()
        if isinstance(data, tuple) and len(data) == 2:
            return data
        first_option = QUICK_LAUNCH_GROUPS[0]["options"][0]
        return first_option["lane_key"], first_option["with_voice"]

    def populate_quick_presets(self, *_args):
        group = self.current_quick_group()
        self.quick_preset_combo.blockSignals(True)
        self.quick_preset_combo.clear()
        for option in group["options"]:
            self.quick_preset_combo.addItem(option["label"], (option["lane_key"], option["with_voice"]))
        self.quick_preset_combo.blockSignals(False)
        self.quick_preset_combo.setCurrentIndex(0)
        self.update_quick_detail()

    def update_quick_detail(self, *_args):
        lane_key, with_voice = self.current_quick_selection()
        lane = LANE_CONFIG[lane_key]
        detail = lane["detail"]
        for option in self.current_quick_group()["options"]:
            if option["lane_key"] == lane_key and option["with_voice"] == with_voice:
                detail = option.get("detail", detail)
                break
        audio_mode = "With Voice / Audio" if with_voice else "Quiet"
        self.quick_detail_label.setText(
            f"Lane: {lane['label']}\n"
            f"Audio: {audio_mode}\n"
            f"Purpose: {detail}"
        )

    def launch_selected_quick_preset(self):
        lane_key, with_voice = self.current_quick_selection()
        self.quick_launch(lane_key, with_voice)

    def current_lane_group(self) -> dict:
        index = self.lane_group_combo.currentIndex()
        if index < 0:
            index = 0
        return CONFIG_LANE_GROUPS[index]

    def populate_lane_choices(self, preferred_lane_key: str = ""):
        group = self.current_lane_group()
        self.lane_combo.blockSignals(True)
        self.lane_combo.clear()
        preferred_index = 0
        for index, lane_key in enumerate(group["lane_keys"]):
            lane = LANE_CONFIG[lane_key]
            self.lane_combo.addItem(lane["label"], lane_key)
            if lane_key == preferred_lane_key:
                preferred_index = index
        self.lane_combo.setCurrentIndex(preferred_index)
        self.lane_combo.blockSignals(False)
        self.selected_lane_key = self.lane_combo.currentData() or group["lane_keys"][0]
        self.update_ui()

    def on_lane_group_changed(self, *_args):
        self.populate_lane_choices()

    def on_lane_choice_changed(self, *_args):
        lane_key = self.lane_combo.currentData()
        if lane_key:
            self.selected_lane_key = lane_key
        self.update_ui()

    def current_lane_key(self) -> str:
        return self.selected_lane_key or "diagnostics"

    def current_lane(self) -> dict:
        return LANE_CONFIG[self.current_lane_key()]

    def voice_requested(self) -> bool:
        return self.audio_combo.currentIndex() == 1 and self.current_lane().get("supports_voice", False)

    def active_log_root(self) -> str:
        lane = self.current_lane()
        if lane.get("report_root"):
            return lane["report_root"]
        if self.voice_requested() and lane.get("log_root_with_voice"):
            return lane["log_root_with_voice"]
        return lane["log_root"]

    def active_launcher_filename(self) -> str:
        lane = self.current_lane()
        if self.voice_requested() and lane.get("voice_launcher"):
            return lane["voice_launcher"]
        return lane["quiet_launcher"]

    def active_label(self) -> str:
        lane = self.current_lane()
        if self.voice_requested() and lane.get("supports_voice"):
            return lane["label"] + " With Voice"
        return lane["label"]

    def select_lane(self, lane_key: str):
        group_index = 0
        for index, group in enumerate(CONFIG_LANE_GROUPS):
            if lane_key in group["lane_keys"]:
                group_index = index
                break
        self.lane_group_combo.blockSignals(True)
        self.lane_group_combo.setCurrentIndex(group_index)
        self.lane_group_combo.blockSignals(False)
        self.populate_lane_choices(lane_key)

    def audio_mode_summary(self, lane: dict) -> str:
        if lane.get("supports_voice", False):
            return "Quiet or With Voice / Audio"
        return "Quiet only"

    def audio_mode_label_text(self, lane: dict) -> str:
        if lane.get("supports_voice", False):
            return "Audio Mode"
        return "Audio Mode (Quiet only for this lane)"

    def detail_text_for_lane(self, lane: dict) -> str:
        return (
            f"Lane: {lane['label']}\n"
            f"Purpose: {lane['detail']}\n"
            f"Audio Support: {self.audio_mode_summary(lane)}"
        )

    def update_mode_line(self, lane: dict):
        selected_audio = self.audio_combo.currentText() if lane.get("supports_voice", False) else "Quiet only"
        self.mode_line.setText(
            f"Selected Group: {self.current_lane_group()['label']} | "
            f"Lane: {lane['label']} | "
            f"Audio: {selected_audio} | "
            f"Delay: {self.delay_combo.currentText()}"
        )

    def update_ui(self):
        lane = self.current_lane()
        self.detail_label.setText(self.detail_text_for_lane(lane))

        supports_voice = lane.get("supports_voice", False)
        self.audio_combo.setEnabled(supports_voice)
        if not supports_voice:
            self.audio_combo.setCurrentIndex(0)
        self.audio_label.setText(self.audio_mode_label_text(lane))

        if hasattr(self, "crash_folder_btn"):
            self.crash_folder_btn.setEnabled(bool(lane.get("crash_folder")))
        self.update_mode_line(lane)
        self.cancel_btn.setEnabled(self.launch_timer.isActive())

    def set_status(self, text: str):
        self.status_label.setText(text)

    def schedule_or_launch(self):
        self.cancel_launch(silent=True)
        delay_text = self.delay_combo.currentText()
        if delay_text == "Now":
            self.run_selected_launcher()
            return

        delay_seconds = int(delay_text.rstrip("s"))
        self.pending_launch_key = self.current_lane_key()
        self.launch_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.launch_timer.start(delay_seconds * 1000)
        self.set_status(f"Launching {self.active_label()} in {delay_seconds} second(s)...")

    def cancel_launch(self, silent: bool = False):
        if self.launch_timer.isActive():
            self.launch_timer.stop()
        self.pending_launch_key = ""
        self.launch_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        if not silent:
            self.set_status("Pending launch cancelled.")

    def run_selected_launcher(self):
        try:
            lane = self.current_lane()
            if lane.get("requires_bundle_input"):
                source_path = self.select_support_bundle_source()
                if not source_path:
                    self.set_status("Launch cancelled: no support bundle selected.")
                    return
                subprocess.Popen([PYTHONW_PATH, lane["script_path"], source_path], cwd=ROOT_DIR)
                self.set_status(f"Launched: {self.active_label()} :: {source_path}")
                return

            launcher_path = os.path.join(DEV_LAUNCHERS_DIR, self.active_launcher_filename())
            subprocess.Popen(["wscript.exe", launcher_path], cwd=DEV_LAUNCHERS_DIR)
            self.set_status(f"Launched: {self.active_label()}")
        except Exception as exc:
            self.set_status(f"Launch failed: {self.active_label()} :: {exc}")
        finally:
            self.launch_timer.stop()
            self.launch_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)

    def select_support_bundle_source(self) -> str:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Support Bundle Zip",
            LOGS_DIR,
            "Support Bundle Zip (*.zip);;All Files (*)",
        )
        if file_path:
            return file_path

        return QFileDialog.getExistingDirectory(
            self,
            "Select Extracted Support Bundle Folder",
            LOGS_DIR,
        )

    def quick_launch(self, lane_key: str, with_voice: bool):
        self.select_lane(lane_key)
        self.delay_combo.setCurrentText("Now")
        self.audio_combo.setCurrentIndex(1 if with_voice else 0)
        self.update_ui()
        self.schedule_or_launch()

    def open_launchers_folder(self):
        self.open_path(DEV_LAUNCHERS_DIR, "Opened: Dev launchers folder")

    def open_selected_log_root(self):
        root = self.active_log_root()
        if not os.path.isdir(root):
            self.set_status(f"Log root not found yet: {root}")
            return
        self.open_path(root, f"Opened log root: {root}")

    def open_latest_runtime_log(self):
        lane = self.current_lane()
        report_root = lane.get("report_root", "")
        report_prefix = lane.get("report_prefix", "")
        report_suffix = lane.get("report_suffix", "")
        if report_root and report_prefix:
            if not os.path.isdir(report_root):
                self.set_status(f"Report folder not found yet: {report_root}")
                return
            latest = ""
            best_time = -1.0
            for name in os.listdir(report_root):
                if not name.lower().startswith(report_prefix.lower()):
                    continue
                if report_suffix and not name.lower().endswith(report_suffix.lower()):
                    continue
                path = os.path.join(report_root, name)
                if not os.path.isfile(path):
                    continue
                try:
                    modified = os.path.getmtime(path)
                except OSError:
                    continue
                if modified >= best_time:
                    best_time = modified
                    latest = path
            if not latest:
                self.set_status(f"No report found yet in: {report_root}")
                return
            self.open_path(latest, f"Opened latest report: {latest}")
            return

        fixed = lane.get("runtime_fixed", "")
        if fixed:
            if not os.path.isfile(fixed):
                self.set_status("No diagnostics runtime log found yet.")
                return
            self.open_path(fixed, f"Opened latest runtime log: {fixed}")
            return

        root = self.active_log_root()
        if not os.path.isdir(root):
            self.set_status(f"Log root not found yet: {root}")
            return
        latest = latest_file_matching(root, "Runtime_")
        if not latest:
            self.set_status(f"No runtime log found yet in: {root}")
            return
        self.open_path(latest, f"Opened latest runtime log: {latest}")

    def open_crash_folder(self):
        lane = self.current_lane()
        crash_folder_name = lane.get("crash_folder", "")
        if not crash_folder_name:
            self.set_status("Diagnostics UI Test does not use a dedicated crash folder.")
            return
        crash_path = os.path.join(self.active_log_root(), crash_folder_name)
        if not os.path.isdir(crash_path):
            self.set_status(f"Crash folder not found yet: {crash_path}")
            return
        self.open_path(crash_path, f"Opened crash folder: {crash_path}")

    def open_path(self, path: str, success_message: str):
        try:
            os.startfile(path)
            self.set_status(success_message)
        except Exception as exc:
            self.set_status(f"Open failed: {path} :: {exc}")

    def center_on_primary(self):
        screen = QGuiApplication.primaryScreen()
        if not screen:
            return
        geo = screen.availableGeometry()
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)

    def _hit_test_edges(self, pos):
        rect = self.rect()
        x = pos.x()
        y = pos.y()
        margin = self._edge_margin
        edges = set()

        if x <= margin:
            edges.add("left")
        elif x >= rect.width() - margin:
            edges.add("right")

        if y <= margin:
            edges.add("top")
        elif y >= rect.height() - margin:
            edges.add("bottom")

        return edges

    def _apply_cursor_for_edges(self, edges):
        if {"left", "top"} <= edges or {"right", "bottom"} <= edges:
            self.setCursor(Qt.SizeFDiagCursor)
        elif {"right", "top"} <= edges or {"left", "bottom"} <= edges:
            self.setCursor(Qt.SizeBDiagCursor)
        elif "left" in edges or "right" in edges:
            self.setCursor(Qt.SizeHorCursor)
        elif "top" in edges or "bottom" in edges:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def _resize_geometry(self, global_pos):
        delta = global_pos - self._resize_start_pos
        rect = QRect(self._resize_start_geom)

        if "left" in self._resize_edges:
            new_left = rect.left() + delta.x()
            max_left = rect.right() - self.minimumWidth()
            rect.setLeft(min(new_left, max_left))

        if "right" in self._resize_edges:
            new_width = max(self.minimumWidth(), rect.width() + delta.x())
            rect.setWidth(new_width)

        if "top" in self._resize_edges:
            new_top = rect.top() + delta.y()
            max_top = rect.bottom() - self.minimumHeight()
            rect.setTop(min(new_top, max_top))

        if "bottom" in self._resize_edges:
            new_height = max(self.minimumHeight(), rect.height() + delta.y())
            rect.setHeight(new_height)

        self.setGeometry(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edges = self._hit_test_edges(event.position().toPoint())
            if edges:
                self._resize_active = True
                self._resize_edges = edges
                self._resize_start_pos = event.globalPosition().toPoint()
                self._resize_start_geom = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        global_pos = event.globalPosition().toPoint()

        if self._resize_active:
            self._resize_geometry(global_pos)
            event.accept()
            return

        self._apply_cursor_for_edges(self._hit_test_edges(pos))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resize_active = False
        self._resize_edges = set()
        self._apply_cursor_for_edges(self._hit_test_edges(event.position().toPoint()))
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        if not self._resize_active:
            self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Consolas", 10))
    window = DevLauncherWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
