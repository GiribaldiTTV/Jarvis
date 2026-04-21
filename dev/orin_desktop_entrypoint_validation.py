import datetime
import json
import os
import re
import subprocess
import sys
import time


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV_LOGS_DIR = os.path.join(ROOT_DIR, "dev", "logs")
BASE_LOG_ROOT = os.path.join(DEV_LOGS_DIR, "desktop_entrypoint_validation")
REPORTS_DIR = os.path.join(BASE_LOG_ROOT, "reports")

LAUNCHER_SCRIPT = os.path.join(ROOT_DIR, "desktop", "orin_desktop_launcher.pyw")
DEFAULT_TARGET_SCRIPT = os.path.join(ROOT_DIR, "desktop", "orin_desktop_main.py")
EXPECTED_DEFAULT_TARGET_LINE = re.compile(
    r'DEFAULT_TARGET_SCRIPT\s*=\s*os\.path\.join\(ROOT_DIR,\s*"desktop",\s*"orin_desktop_main\.py"\)'
)

EXPECTED_MILESTONES = [
    "RENDERER_MAIN|START",
    "RENDERER_MAIN|QAPPLICATION_CREATED",
    "RENDERER_MAIN|VISUAL_HTML_RESOLVED",
    "RENDERER_MAIN|WINDOW_CONSTRUCTED",
    "RENDERER_MAIN|SHUTDOWN_BUS_READY",
    "RENDERER_MAIN|TRAY_ENTRY_INITIALIZE_REQUESTED",
    "RENDERER_MAIN|TRAY_ENTRY_READY",
    "RENDERER_MAIN|HOTKEYS_STARTED",
    "RENDERER_MAIN|WINDOW_SHOW_DEFERRED_UNTIL_CORE_READY",
    "RENDERER_MAIN|CORE_VISUALIZATION_READY",
    "RENDERER_MAIN|WINDOW_SHOW_REQUESTED",
    "RENDERER_MAIN|CORE_VISUALIZATION_FIRST_VISIBLE",
    "RENDERER_MAIN|STARTUP_READY",
]


def hidden_subprocess_kwargs():
    kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
    }

    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        kwargs["startupinfo"] = startupinfo
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    return kwargs


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def read_text(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.rstrip("\r\n") for line in f]


def line_status(ok, detail):
    return {"ok": bool(ok), "detail": detail}


def first_marker_index(lines, marker):
    for index, line in enumerate(lines):
        if marker in line:
            return index
    return -1


def detect_branch_state():
    head_path = os.path.join(ROOT_DIR, ".git", "HEAD")
    try:
        with open(head_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "unavailable"


def launcher_default_target_line():
    for line in read_lines(LAUNCHER_SCRIPT):
        if line.strip().startswith("DEFAULT_TARGET_SCRIPT"):
            return line.strip()
    return "missing DEFAULT_TARGET_SCRIPT line"


def validate_tray_overlay_route():
    previous_qt_platform = os.environ.get("QT_QPA_PLATFORM")
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    try:
        if ROOT_DIR not in sys.path:
            sys.path.insert(0, ROOT_DIR)

        from PySide6.QtWidgets import QApplication

        from desktop.orin_desktop_main import DesktopTrayEntry

        app = QApplication.instance()
        created_app = False
        if app is None:
            app = QApplication(["orin_desktop_entrypoint_validation"])
            created_app = True

        events = []

        class FakeWindow:
            def __init__(self):
                self.toggle_count = 0
                self.create_custom_task_sources = []

            def toggle_command_overlay(self):
                self.toggle_count += 1

            def request_create_custom_task_from_tray(self, source=""):
                self.create_custom_task_sources.append(source)

        fake_window = FakeWindow()
        tray_entry = DesktopTrayEntry(app, fake_window, events.append)
        tray_entry.request_overlay_from_tray("validation")
        tray_entry.request_create_custom_task_from_tray("validation")

        if created_app:
            app.quit()

        return {
            "ok": True,
            "events": events,
            "toggle_count": fake_window.toggle_count,
            "create_custom_task_sources": fake_window.create_custom_task_sources,
            "error": "",
        }
    except Exception as exc:
        return {
            "ok": False,
            "events": [],
            "toggle_count": 0,
            "create_custom_task_sources": [],
            "error": f"{type(exc).__name__}: {exc}",
        }
    finally:
        if previous_qt_platform is None:
            os.environ.pop("QT_QPA_PLATFORM", None)
        else:
            os.environ["QT_QPA_PLATFORM"] = previous_qt_platform


def validate_tray_initialization_failure_is_bounded():
    previous_qt_platform = os.environ.get("QT_QPA_PLATFORM")
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    try:
        if ROOT_DIR not in sys.path:
            sys.path.insert(0, ROOT_DIR)

        from PySide6.QtWidgets import QApplication

        import desktop.orin_desktop_main as runtime_mod

        app = QApplication.instance()
        created_app = False
        if app is None:
            app = QApplication(["orin_desktop_entrypoint_validation"])
            created_app = True

        events = []

        class FakeWindow:
            def toggle_command_overlay(self):
                raise AssertionError("initialize should not route overlay")

        class FailingTrayIcon:
            class ActivationReason:
                Trigger = object()
                DoubleClick = object()

            @staticmethod
            def isSystemTrayAvailable():
                return True

            def __init__(self, *_args, **_kwargs):
                raise RuntimeError("synthetic tray init failure")

        original_tray_icon = runtime_mod.QSystemTrayIcon
        runtime_mod.QSystemTrayIcon = FailingTrayIcon
        try:
            tray_entry = runtime_mod.DesktopTrayEntry(app, FakeWindow(), events.append)
            initialized = tray_entry.initialize()
        finally:
            runtime_mod.QSystemTrayIcon = original_tray_icon

        if created_app:
            app.quit()

        return {
            "ok": True,
            "initialized": initialized,
            "events": events,
            "error": "",
        }
    except Exception as exc:
        return {
            "ok": False,
            "initialized": True,
            "events": [],
            "error": f"{type(exc).__name__}: {exc}",
        }
    finally:
        if previous_qt_platform is None:
            os.environ.pop("QT_QPA_PLATFORM", None)
        else:
            os.environ["QT_QPA_PLATFORM"] = previous_qt_platform


def validate_tray_identity_initialization():
    previous_qt_platform = os.environ.get("QT_QPA_PLATFORM")
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    try:
        if ROOT_DIR not in sys.path:
            sys.path.insert(0, ROOT_DIR)

        from PySide6.QtWidgets import QApplication

        import desktop.orin_desktop_main as runtime_mod

        app = QApplication.instance()
        created_app = False
        if app is None:
            app = QApplication(["orin_desktop_entrypoint_validation"])
            created_app = True

        events = []

        class FakeWindow:
            def toggle_command_overlay(self):
                raise AssertionError("initialize should not route overlay")

            def request_create_custom_task_from_tray(self, source=""):
                raise AssertionError("initialize should not route authoring")

        class FakeSignal:
            def __init__(self):
                self.callback = None

            def connect(self, callback):
                self.callback = callback

        class FakeTrayIcon:
            latest_instance = None

            class ActivationReason:
                Trigger = object()
                DoubleClick = object()

            class MessageIcon:
                Information = "information"

            @staticmethod
            def isSystemTrayAvailable():
                return True

            @staticmethod
            def supportsMessages():
                return True

            def __init__(self, *_args, **_kwargs):
                self.activated = FakeSignal()
                self.tooltip = ""
                self.context_menu = None
                self.shown = False
                self.hidden = False
                self.messages = []
                FakeTrayIcon.latest_instance = self

            def setToolTip(self, tooltip):
                self.tooltip = tooltip

            def setContextMenu(self, menu):
                self.context_menu = menu

            def show(self):
                self.shown = True

            def hide(self):
                self.hidden = True

            def showMessage(self, title, message, icon, duration_ms):
                self.messages.append(
                    {
                        "title": title,
                        "message": message,
                        "icon": icon,
                        "duration_ms": duration_ms,
                    }
                )

        original_tray_icon = runtime_mod.QSystemTrayIcon
        runtime_mod.QSystemTrayIcon = FakeTrayIcon
        try:
            tray_entry = runtime_mod.DesktopTrayEntry(app, FakeWindow(), events.append)
            initialized = tray_entry.initialize()
            discovery_cue_requested = tray_entry.show_discovery_cue()
            actions = [
                action
                for action in tray_entry.tray_menu.actions()
                if not action.isSeparator()
            ]
            action_texts = [action.text() for action in actions]
            identity_action_enabled = actions[0].isEnabled() if actions else None
            fake_icon = FakeTrayIcon.latest_instance
            tooltip = fake_icon.tooltip if fake_icon is not None else ""
            messages = fake_icon.messages if fake_icon is not None else []
        finally:
            runtime_mod.QSystemTrayIcon = original_tray_icon

        tray_entry.close()

        if created_app:
            app.quit()

        return {
            "ok": True,
            "initialized": initialized,
            "events": events,
            "action_texts": action_texts,
            "identity_action_enabled": identity_action_enabled,
            "tooltip": tooltip,
            "discovery_cue_requested": discovery_cue_requested,
            "messages": messages,
            "error": "",
        }
    except Exception as exc:
        return {
            "ok": False,
            "initialized": False,
            "events": [],
            "action_texts": [],
            "identity_action_enabled": None,
            "tooltip": "",
            "discovery_cue_requested": False,
            "messages": [],
            "error": f"{type(exc).__name__}: {exc}",
        }
    finally:
        if previous_qt_platform is None:
            os.environ.pop("QT_QPA_PLATFORM", None)
        else:
            os.environ["QT_QPA_PLATFORM"] = previous_qt_platform


def run_validation():
    ensure_dir(BASE_LOG_ROOT)
    ensure_dir(REPORTS_DIR)

    launcher_text = read_text(LAUNCHER_SCRIPT)
    launcher_line = launcher_default_target_line()

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    runtime_log = os.path.join(BASE_LOG_ROOT, f"Runtime_{stamp}.txt")

    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"

    proc = subprocess.Popen(
        [
            sys.executable,
            DEFAULT_TARGET_SCRIPT,
            "--runtime-log",
            runtime_log,
        ],
        cwd=ROOT_DIR,
        env=env,
        **hidden_subprocess_kwargs(),
    )

    ready_seen = False
    deadline = time.time() + 20.0
    runtime_lines = []

    try:
        while time.time() < deadline:
            if os.path.exists(runtime_log):
                runtime_lines = read_lines(runtime_log)
                if any("RENDERER_MAIN|STARTUP_READY" in line for line in runtime_lines):
                    ready_seen = True
                    break

            if proc.poll() is not None:
                break

            time.sleep(0.25)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

    stdout_text, stderr_text = proc.communicate()
    runtime_lines = read_lines(runtime_log)

    checks = {
        "launcher_default_target_matches_expected": line_status(
            bool(EXPECTED_DEFAULT_TARGET_LINE.search(launcher_text)),
            launcher_line,
        ),
        "default_target_exists": line_status(
            os.path.exists(DEFAULT_TARGET_SCRIPT),
            DEFAULT_TARGET_SCRIPT,
        ),
        "runtime_log_created": line_status(
            os.path.exists(runtime_log),
            runtime_log,
        ),
    }

    for milestone in EXPECTED_MILESTONES:
        checks[f"milestone::{milestone}"] = line_status(
            any(milestone in line for line in runtime_lines),
            milestone,
        )

    deferred_index = first_marker_index(
        runtime_lines,
        "RENDERER_MAIN|WINDOW_SHOW_DEFERRED_UNTIL_CORE_READY",
    )
    core_ready_index = first_marker_index(
        runtime_lines,
        "RENDERER_MAIN|CORE_VISUALIZATION_READY",
    )
    show_index = first_marker_index(
        runtime_lines,
        "RENDERER_MAIN|WINDOW_SHOW_REQUESTED",
    )
    first_visible_index = first_marker_index(
        runtime_lines,
        "RENDERER_MAIN|CORE_VISUALIZATION_FIRST_VISIBLE",
    )
    startup_ready_index = first_marker_index(
        runtime_lines,
        "RENDERER_MAIN|STARTUP_READY",
    )
    ordering_detail = (
        f"deferred={deferred_index}, core_ready={core_ready_index}, "
        f"show={show_index}, first_visible={first_visible_index}, "
        f"startup_ready={startup_ready_index}"
    )
    checks["window_show_deferred_before_core_ready"] = line_status(
        deferred_index >= 0 and core_ready_index > deferred_index,
        ordering_detail,
    )
    checks["window_show_after_core_visualization_ready"] = line_status(
        show_index > core_ready_index >= 0,
        ordering_detail,
    )
    checks["core_visualization_visible_before_startup_ready"] = line_status(
        startup_ready_index > first_visible_index > show_index,
        ordering_detail,
    )

    checks["startup_ready_reached_before_termination"] = line_status(
        ready_seen,
        "RENDERER_MAIN|STARTUP_READY",
    )
    checks["traceback_absent"] = line_status(
        "Traceback" not in stderr_text,
        stderr_text.strip() or "no traceback in stderr",
    )

    tray_route_result = validate_tray_overlay_route()
    tray_events = tray_route_result["events"]
    checks["tray_route_validation_imported"] = line_status(
        tray_route_result["ok"],
        tray_route_result["error"] or "DesktopTrayEntry imported and exercised",
    )
    checks["tray_route_toggle_overlay_called"] = line_status(
        tray_route_result["toggle_count"] == 1,
        f"toggle_count={tray_route_result['toggle_count']}",
    )
    checks["tray_route_requested_marker"] = line_status(
        any(
            "RENDERER_MAIN|TRAY_ACTIVATION_REQUESTED|source=validation" in event
            for event in tray_events
        ),
        "TRAY_ACTIVATION_REQUESTED",
    )
    checks["tray_route_routed_marker"] = line_status(
        any(
            "RENDERER_MAIN|TRAY_ACTIVATION_ROUTED_TO_OVERLAY|source=validation" in event
            for event in tray_events
        ),
        "TRAY_ACTIVATION_ROUTED_TO_OVERLAY",
    )
    checks["tray_create_custom_task_marker"] = line_status(
        any(
            "RENDERER_MAIN|TRAY_CREATE_CUSTOM_TASK_REQUESTED|source=validation" in event
            for event in tray_events
        ),
        "TRAY_CREATE_CUSTOM_TASK_REQUESTED",
    )
    checks["tray_create_custom_task_route"] = line_status(
        tray_route_result["create_custom_task_sources"] == ["validation"],
        f"create_custom_task_sources={tray_route_result['create_custom_task_sources']}",
    )

    tray_identity_result = validate_tray_identity_initialization()
    tray_identity_events = tray_identity_result["events"]
    tray_identity_messages = tray_identity_result["messages"]
    checks["tray_identity_validation_imported"] = line_status(
        tray_identity_result["ok"],
        tray_identity_result["error"] or "DesktopTrayEntry identity path exercised",
    )
    checks["tray_identity_initializes"] = line_status(
        tray_identity_result["initialized"] is True,
        f"initialized={tray_identity_result['initialized']}",
    )
    checks["tray_identity_tooltip"] = line_status(
        tray_identity_result["tooltip"] == "Nexus Desktop AI",
        f"tooltip={tray_identity_result['tooltip']}",
    )
    checks["tray_identity_menu_header"] = line_status(
        tray_identity_result["action_texts"][:3]
        == ["Nexus Desktop AI", "Open Command Overlay", "Create Custom Task"],
        f"action_texts={tray_identity_result['action_texts']}",
    )
    checks["tray_identity_header_disabled"] = line_status(
        tray_identity_result["identity_action_enabled"] is False,
        f"identity_action_enabled={tray_identity_result['identity_action_enabled']}",
    )
    checks["tray_identity_ready_marker"] = line_status(
        any(
            "RENDERER_MAIN|TRAY_IDENTITY_READY|label=Nexus Desktop AI|hidden_overflow_hint=true"
            in event
            for event in tray_identity_events
        ),
        "TRAY_IDENTITY_READY",
    )
    checks["tray_discovery_cue_requested"] = line_status(
        tray_identity_result["discovery_cue_requested"] is True
        and any(
            "RENDERER_MAIN|TRAY_DISCOVERY_CUE_REQUESTED|hidden_overflow_hint=true"
            in event
            for event in tray_identity_events
        ),
        "TRAY_DISCOVERY_CUE_REQUESTED",
    )
    checks["tray_discovery_cue_hidden_overflow_hint"] = line_status(
        bool(tray_identity_messages)
        and "hidden icons" in tray_identity_messages[0]["message"],
        tray_identity_messages[0]["message"] if tray_identity_messages else "no message",
    )

    tray_failure_result = validate_tray_initialization_failure_is_bounded()
    tray_failure_events = tray_failure_result["events"]
    checks["tray_init_failure_validation_imported"] = line_status(
        tray_failure_result["ok"],
        tray_failure_result["error"] or "DesktopTrayEntry init failure path exercised",
    )
    checks["tray_init_failure_returns_false"] = line_status(
        tray_failure_result["initialized"] is False,
        f"initialized={tray_failure_result['initialized']}",
    )
    checks["tray_init_failure_ready_marker"] = line_status(
        any(
            "RENDERER_MAIN|TRAY_ENTRY_READY|available=false|reason=RuntimeError" in event
            for event in tray_failure_events
        ),
        "TRAY_ENTRY_READY failure marker",
    )

    return {
        "branch_state": detect_branch_state(),
        "runtime_log": runtime_log,
        "target_script": DEFAULT_TARGET_SCRIPT,
        "launcher_line": launcher_line,
        "tray_route_events": tray_events,
        "tray_identity_events": tray_identity_events,
        "tray_identity_actions": tray_identity_result["action_texts"],
        "tray_identity_messages": tray_identity_messages,
        "tray_failure_events": tray_failure_events,
        "stdout": stdout_text.strip(),
        "stderr": stderr_text.strip(),
        "checks": checks,
    }


def build_report_text(report_path, result, overall_ok):
    lines = [
        "JARVIS DESKTOP ENTRYPOINT VALIDATION",
        f"Report: {report_path}",
        f"Branch: {result['branch_state']}",
        f"Overall Result: {'PASS' if overall_ok else 'FAIL'}",
        "",
        f"Default target: {result['target_script']}",
        f"Launcher target line: {result['launcher_line']}",
        f"Runtime log: {result['runtime_log']}",
        "",
        "Checks:",
    ]

    for key, value in result["checks"].items():
        lines.append(f"  {'PASS' if value['ok'] else 'FAIL'} :: {key} :: {value['detail']}")

    if result["stdout"]:
        lines.extend(["", "stdout:", result["stdout"]])
    if result["stderr"]:
        lines.extend(["", "stderr:", result["stderr"]])
    if result.get("tray_route_events"):
        lines.extend(["", "Tray route events:"])
        lines.extend(f"  {event}" for event in result["tray_route_events"])
    if result.get("tray_identity_actions"):
        lines.extend(["", "Tray identity menu actions:"])
        lines.extend(f"  {action}" for action in result["tray_identity_actions"])
    if result.get("tray_identity_events"):
        lines.extend(["", "Tray identity events:"])
        lines.extend(f"  {event}" for event in result["tray_identity_events"])
    if result.get("tray_identity_messages"):
        lines.extend(["", "Tray identity discovery messages:"])
        lines.extend(
            f"  {message['title']} :: {message['message']}"
            for message in result["tray_identity_messages"]
        )
    if result.get("tray_failure_events"):
        lines.extend(["", "Tray init failure events:"])
        lines.extend(f"  {event}" for event in result["tray_failure_events"])

    return "\n".join(lines) + "\n"


def main(argv):
    open_report = "--open-report" in argv

    result = run_validation()
    failures = [key for key, value in result["checks"].items() if not value["ok"]]
    overall_ok = not failures

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"DesktopEntrypointValidationReport_{stamp}.txt")
    json_path = os.path.join(REPORTS_DIR, f"DesktopEntrypointValidationReport_{stamp}.json")

    report_text = build_report_text(report_path, result, overall_ok)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "overall_ok": overall_ok,
                "result": result,
                "report_path": report_path,
                "failures": failures,
            },
            f,
            indent=2,
        )

    if open_report and os.name == "nt":
        try:
            os.startfile(report_path)
        except Exception:
            pass

    print(report_text)
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
