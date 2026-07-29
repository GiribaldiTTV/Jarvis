"""Validate the bounded FAM-003 Option G lifecycle and retention Workstream."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "desktop" / "desktop_renderer.py"
CONTROLLER = ROOT / "dev" / "fam003_option_d_performance_controller.py"
FIXTURES = ROOT / "dev" / "fixtures" / "fam003_option_g_lifecycle_retention_negative_cases.json"
DEFAULT_IMPLEMENTATION_BASE = "0242816c7f179684f50cd510c2961ce2c109da11"
EXPECTED_RECORDING_CLASS_SHA256 = "8990492939ED174C4920283674811C63DD8F7F688E26A8EBD1796BEA04276970"
ALLOWED_RENDERER_REGIONS = {
    "MonitoringHudStudioWebWindow.__init__",
    "MonitoringHudStudioWebWindow._sync_resize_hover_polling_lifecycle",
    "MonitoringHudStudioWebWindow._poll_native_edge_resize_hover_cursor",
    "MonitoringHudStudioWebWindow.closeEvent",
    "MonitoringHudStudioWebWindow._show_or_raise",
    "DesktopRuntimeWindow.__init__",
    "DesktopRuntimeWindow._apply_monitoring_hud_window_interaction_state",
    "DesktopRuntimeWindow.request_shutdown",
}


def _class_node(source: str, class_name: str) -> ast.ClassDef | None:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    return next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == class_name
        ),
        None,
    )


def _node_source(source: str, node: ast.AST | None) -> str:
    if node is None or not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
        return ""
    lines = source.splitlines()
    return "\n".join(lines[node.lineno - 1 : node.end_lineno]) + "\n"


def _method_source(source: str, class_name: str, method_name: str) -> str:
    class_node = _class_node(source, class_name)
    if class_node is None:
        return ""
    method = next(
        (
            node
            for node in class_node.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == method_name
        ),
        None,
    )
    return _node_source(source, method)


def _contains_all(text: str, fragments: tuple[str, ...]) -> bool:
    return all(fragment in text for fragment in fragments)


def validate_sources(renderer: str, controller: str) -> list[str]:
    failures: list[str] = []
    try:
        renderer_tree = ast.parse(renderer)
    except SyntaxError:
        return ["OPTG-FG-AST"]
    classes = {
        node.name: node
        for node in renderer_tree.body
        if isinstance(node, ast.ClassDef)
    }

    def method_source(class_name: str, method_name: str) -> str:
        class_node = classes.get(class_name)
        if class_node is None:
            return ""
        method = next(
            (
                node
                for node in class_node.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == method_name
            ),
            None,
        )
        return _node_source(renderer, method)

    studio_init = method_source("MonitoringHudStudioWebWindow", "__init__")
    studio_sync = method_source(
        "MonitoringHudStudioWebWindow", "_sync_resize_hover_polling_lifecycle"
    )
    studio_poll = method_source(
        "MonitoringHudStudioWebWindow", "_poll_native_edge_resize_hover_cursor"
    )
    studio_show = method_source("MonitoringHudStudioWebWindow", "_show_or_raise")
    studio_close = method_source("MonitoringHudStudioWebWindow", "closeEvent")
    recording_node = classes.get("MonitoringHudRecordingStudioWindow")
    recording = _node_source(renderer, recording_node)
    desktop_init = method_source("DesktopRuntimeWindow", "__init__")
    hud_apply = method_source(
        "DesktopRuntimeWindow", "_apply_monitoring_hud_window_interaction_state"
    )
    shutdown = method_source("DesktopRuntimeWindow", "request_shutdown")

    checks = {
        "OPTG-FG-01": "self._resize_hover_timer.start()" not in studio_init,
        "OPTG-FG-02": "self.winId()" in studio_init and "self.windowHandle()" in studio_init,
        "OPTG-FG-03": "visibilityChanged.connect" in studio_init,
        "OPTG-FG-04": "windowStateChanged.connect" in studio_init,
        "OPTG-FG-05": bool(studio_sync),
        "OPTG-FG-06": "self.STUDIO_RESIZABLE" in studio_sync,
        "OPTG-FG-07": "self.isVisible()" in studio_sync,
        "OPTG-FG-08": "not self.isMinimized()" in studio_sync,
        "OPTG-FG-09": _contains_all(
            studio_sync,
            ("if not self._resize_hover_timer.isActive():", "self._resize_hover_timer.start()"),
        ),
        "OPTG-FG-10": _contains_all(
            studio_sync,
            ("if self._resize_hover_timer.isActive():", "self._resize_hover_timer.stop()"),
        ),
        "OPTG-FG-11": "self._reset_native_edge_resize_cursor()" in studio_sync,
        "OPTG-FG-12": "not self._sync_resize_hover_polling_lifecycle()" in studio_poll,
        "OPTG-FG-13": "self._sync_resize_hover_polling_lifecycle()" in studio_show,
        "OPTG-FG-14": "self._resize_hover_timer.stop()" in studio_close,
        "OPTG-FG-15": "STUDIO_RESIZABLE = False" in recording,
        "OPTG-FG-16": _contains_all(
            recording,
            (
                "class MonitoringHudRecordingStudioWindow(MonitoringHudStudioWebWindow):\n"
                "    WIDTH = 432\n"
                "    HEIGHT = 154\n"
                "    MINIMUM_WIDTH = 432\n"
                "    MINIMUM_HEIGHT = 154",
            ),
        ),
        "OPTG-FG-17": (
            hashlib.sha256(recording.encode("utf-8")).hexdigest().upper()
            == EXPECTED_RECORDING_CLASS_SHA256
        ),
        "OPTG-FG-18": (
            "self._monitoring_hud_resize_hover_timer.start()" not in desktop_init
            and "self._monitoring_hud_recording_control_click_bridge_timer.start()"
            not in desktop_init
        ),
        "OPTG-FG-19": "window_handle.visibilityChanged.connect" in desktop_init,
        "OPTG-FG-20": "window_handle.windowStateChanged.connect" in desktop_init,
        "OPTG-FG-21": (
            "lifecycle_ready = bool(\n"
            "            self.surface_role == \"hud\"\n"
            "            and dashboard_visible\n"
            "            and self.desktop_mode"
        ) in hud_apply,
        "OPTG-FG-22": "and self._page_ready" in hud_apply,
        "OPTG-FG-23": _contains_all(
            hud_apply,
            ("self.isVisible()", "not self.isMinimized()", "self.webview.isVisible()"),
        ),
        "OPTG-FG-24": "not self._is_shutting_down" in hud_apply,
        "OPTG-FG-25": (
            "if not lifecycle_ready:\n"
            "            self._reset_monitoring_hud_resize_cursor()\n"
            "            self._monitoring_hud_recording_control_click_bridge_down = False\n"
            "            self._monitoring_hud_recording_control_click_bridge_press_point = QPoint()"
        ) in hud_apply,
        "OPTG-FG-26": _contains_all(
            hud_apply,
            (
                "self._monitoring_hud_resize_hover_timer",
                "self._monitoring_hud_recording_control_click_bridge_timer",
                "if lifecycle_ready and not timer.isActive():",
                "elif not lifecycle_ready and timer.isActive():",
            ),
        ),
        "OPTG-FG-27": _contains_all(
            shutdown,
            (
                "self._monitoring_hud_resize_hover_timer.stop()",
                "self._monitoring_hud_recording_control_click_bridge_timer.stop()",
            ),
        ),
        "OPTG-FG-28": _contains_all(
            shutdown,
            (
                "self._monitoring_hud_resize_hover_timer.timeout.disconnect",
                "self._monitoring_hud_recording_control_click_bridge_timer.timeout.disconnect",
            ),
        ),
        "OPTG-FG-29": _contains_all(
            controller,
            (
                '("hud-resize-hover", self.window, "_monitoring_hud_resize_hover_timer")',
                '"hud-recording-control-click-bridge",\n'
                '                self.window,',
                '"log-viewer-resize-hover",\n'
                '                getattr(self.window, "_monitoring_hud_log_viewer_studio_window", None),',
                '"recording-studio-resize-hover",\n'
                '                getattr(self.window, "_monitoring_hud_recording_studio_window", None),',
            ),
        ),
        "OPTG-FG-30": "REPEATED_CYCLE_COUNT = 3" in controller,
        "OPTG-FG-31": (
            "LONG_SETTLE_DURATION_MS = 20_000" in controller
            and 'state="long-settle-resident-idle"' in controller
        ),
        "OPTG-FG-32": '"lifecycleTimerInstrumentation": {' in controller,
        "OPTG-FG-33": '"performsDomQueries": False' in controller,
        "OPTG-FG-34": (
            'EXPECTED_POLICY = "temporary-shared-runtime-safety-policy"' in controller
            and '"temporary": True' in controller
        ),
    }
    for code, passed in checks.items():
        if not passed:
            failures.append(code)
    return failures


def _line_owner(source: str, line_number: int) -> str:
    tree = ast.parse(source)
    owner = "MODULE"
    owner_span = sys.maxsize
    for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
        if not (class_node.lineno <= line_number <= class_node.end_lineno):
            continue
        candidate = class_node.name
        span = class_node.end_lineno - class_node.lineno
        for method in (
            node
            for node in class_node.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ):
            if method.lineno <= line_number <= method.end_lineno:
                candidate = f"{class_node.name}.{method.name}"
                span = method.end_lineno - method.lineno
                break
        if span < owner_span:
            owner = candidate
            owner_span = span
    return owner


def validate_changed_regions(renderer: str, implementation_base: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--unified=0", implementation_base, "--", str(RENDERER.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return [f"OPTG-REGION-GIT:{result.stderr.strip() or result.returncode}"]
    owners: set[str] = set()
    for line in result.stdout.splitlines():
        match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if not match:
            continue
        start = int(match.group(1))
        count = int(match.group(2) or "1")
        probe = max(1, start if count else start + 1)
        owners.add(_line_owner(renderer, probe))
    return [
        f"OPTG-REGION-ESCAPE:{owner}"
        for owner in sorted(owners - ALLOWED_RENDERER_REGIONS)
    ]


def validate_negative_fixtures(renderer: str, controller: str) -> list[str]:
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in payload.get("cases", []):
        target = renderer if case["target"] == "renderer" else controller
        if target.count(case["find"]) != 1:
            failures.append(f"{case['id']}:fixture-anchor-count={target.count(case['find'])}")
            continue
        mutated = target.replace(case["find"], case["replace"], 1)
        mutated_renderer = mutated if case["target"] == "renderer" else renderer
        mutated_controller = mutated if case["target"] == "controller" else controller
        observed = validate_sources(mutated_renderer, mutated_controller)
        if case["expected"] not in observed:
            failures.append(f"{case['id']}:unexpected-green:{case['expected']}")
    return failures


def _surface(inventory: dict[str, Any], surface_id: str) -> dict[str, Any]:
    return next(
        (row for row in inventory.get("surfaces", []) if row.get("surfaceId") == surface_id),
        {},
    )


def _timer(surface: dict[str, Any], timer_id: str) -> dict[str, Any]:
    return next(
        (row for row in surface.get("lifecycleTimers", []) if row.get("timerId") == timer_id),
        {},
    )


def validate_evidence(path: Path, expected_head: str) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    sessions = data.get("normalLauncherSessions", [])
    failures: list[str] = []
    if len(sessions) < 3:
        failures.append(f"OPTG-EVIDENCE-SESSIONS:{len(sessions)}")
    for index, session in enumerate(sessions, start=1):
        prefix = f"OPTG-EVIDENCE-S{index:02d}"
        if session.get("sourceHead") != expected_head:
            failures.append(f"{prefix}-HEAD")
        if session.get("normalLauncherProof") is not True:
            failures.append(f"{prefix}-LAUNCHER")
        if session.get("formalH1Entered") is not False:
            failures.append(f"{prefix}-H1")
        if session.get("formalLiveValidationEntered") is not False:
            failures.append(f"{prefix}-LV")
        if session.get("utsRequested") is not False:
            failures.append(f"{prefix}-UTS")
        observations = session.get("observations", [])
        states = [row.get("state") for row in observations]
        required_counts = {
            "startup-resident-idle": 1,
            "representative-active": 3,
            "post-use-resident-idle": 3,
            "long-settle-resident-idle": 1,
        }
        for state, count in required_counts.items():
            if states.count(state) != count:
                failures.append(f"{prefix}-STATE-{state}:{states.count(state)}")
        for observation in observations:
            state = observation.get("state")
            inventories = [
                observation.get("surfaceInventoryBefore", {}),
                observation.get("surfaceInventoryAfter", {}),
            ]
            for inventory in inventories:
                hud = _surface(inventory, "hud-dashboard")
                log_viewer = _surface(inventory, "nexus-log-viewer")
                recording = _surface(inventory, "nexus-recording-suite")
                timer_rows = (
                    _timer(hud, "hud-resize-hover"),
                    _timer(hud, "hud-recording-control-click-bridge"),
                    _timer(log_viewer, "log-viewer-resize-hover"),
                )
                expected_active = state == "representative-active"
                if any(timer.get("active") is not expected_active for timer in timer_rows):
                    failures.append(f"{prefix}-TIMER-{state}")
                recording_timer = _timer(recording, "recording-studio-resize-hover")
                if recording_timer.get("active") is not False:
                    failures.append(f"{prefix}-RECORDING-TIMER-{state}")
                if recording.get("studioResizable") is not False:
                    failures.append(f"{prefix}-RECORDING-RESIZABLE-{state}")
                if recording.get("width") != 432 or recording.get("height") != 154:
                    failures.append(f"{prefix}-RECORDING-GEOMETRY-{state}")
        instrumentation = session.get("lifecycleTimerInstrumentation", {})
        counts = instrumentation.get("callbackCounts", {})
        if any(counts.get(timer_id, 0) <= 0 for timer_id in (
            "hud-resize-hover",
            "hud-recording-control-click-bridge",
            "log-viewer-resize-hover",
        )):
            failures.append(f"{prefix}-CALLBACK-COUNTS")
        if counts.get("recording-studio-resize-hover", 0) != 0:
            failures.append(f"{prefix}-RECORDING-CALLBACK")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-base", default=DEFAULT_IMPLEMENTATION_BASE)
    parser.add_argument("--evidence-manifest", type=Path)
    parser.add_argument("--expected-head", default="")
    parser.add_argument("--skip-fixtures", action="store_true")
    args = parser.parse_args()

    renderer = RENDERER.read_text(encoding="utf-8")
    controller = CONTROLLER.read_text(encoding="utf-8")
    failures = validate_sources(renderer, controller)
    failures.extend(validate_changed_regions(renderer, args.implementation_base))
    fixture_count = 0
    if not args.skip_fixtures:
        fixture_payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
        fixture_count = len(fixture_payload.get("cases", []))
        failures.extend(validate_negative_fixtures(renderer, controller))
    if args.evidence_manifest:
        if not args.expected_head:
            failures.append("OPTG-EVIDENCE-EXPECTED-HEAD-MISSING")
        else:
            failures.extend(validate_evidence(args.evidence_manifest.resolve(), args.expected_head))

    print("FAM-003 Option G Lifecycle / Retention Validation")
    print(f"Implementation Base: {args.implementation_base}")
    print(f"Negative Fixtures: {fixture_count}")
    print(f"Evidence Manifest: {args.evidence_manifest or 'NOT_REQUESTED'}")
    if failures:
        print("Validation Result: FAIL")
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("Validation Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
