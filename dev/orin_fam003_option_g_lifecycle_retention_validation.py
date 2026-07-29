"""Validate the bounded FAM-003 Option G lifecycle and retention Workstream."""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
RENDERER = ROOT / "desktop" / "desktop_renderer.py"
CONTROLLER = ROOT / "dev" / "fam003_option_d_performance_controller.py"
OBSERVER = ROOT / "dev" / "fam003_option_d_performance_observer.py"
FIXTURES = ROOT / "dev" / "fixtures" / "fam003_option_g_lifecycle_retention_negative_cases.json"
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_option_g_lifecycle_retention"
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


def validate_sources(renderer: str, controller: str, observer: str = "") -> list[str]:
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
    controller_open = _method_source(
        controller, "NonintrusivePerformanceController", "_open_active_surfaces"
    )

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
        "OPTG-FG-35": (
            "page.renderProcessPid()" in controller
            and '"surfaceRendererMap": self._surface_renderer_map()' in controller
            and '"DIRECT_QWEBENGINEPAGE_RENDER_PROCESS_PID"' in observer
        ),
        "OPTG-FG-36": (
            "def _externalize_raw_samples" in controller
            and '"retainedRawSampleCount": 0' in controller
            and '"rawSamplesReference"' in controller
        ),
        "OPTG-FG-37": (
            '"hud-dashboard-only"' in controller
            and '"log-viewer-only"' in controller
            and '*("hud-log-viewer-bundle",) * REPEATED_CYCLE_COUNT' in controller
            and "ai_status_action" not in controller_open
            and "_monitoring_hud_recording_studio_window" not in controller_open
        ),
        "OPTG-FG-38": (
            "def _controller_memory_snapshot(self, label: str)" in controller
            and '"controllerMemoryAccounting": controller_memory_accounting' in controller
            and '"rawSampleDeepBytesBeforeRelease": sum(' in controller
        ),
        "OPTG-FG-39": (
            'METHODOLOGY_VERSION = "fam003-option-g-owner-attribution-v5"' in observer
            and '"invalidSampleCount": 0' in observer
            and '"droppedSampleCount": 0' in observer
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


def validate_negative_fixtures(
    renderer: str, controller: str, observer: str = ""
) -> list[str]:
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    failures: list[str] = []
    for case in payload.get("cases", []):
        targets = {"renderer": renderer, "controller": controller, "observer": observer}
        target = targets[case["target"]]
        if target.count(case["find"]) != 1:
            failures.append(f"{case['id']}:fixture-anchor-count={target.count(case['find'])}")
            continue
        mutated = target.replace(case["find"], case["replace"], 1)
        mutated_renderer = mutated if case["target"] == "renderer" else renderer
        mutated_controller = mutated if case["target"] == "controller" else controller
        mutated_observer = mutated if case["target"] == "observer" else observer
        observed = validate_sources(mutated_renderer, mutated_controller, mutated_observer)
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


def _externalized_raw_samples(
    session: dict[str, Any], observation: dict[str, Any], prefix: str
) -> tuple[list[dict[str, Any]], list[str]]:
    failures: list[str] = []
    reference = observation.get("rawSamplesReference") or {}
    manifest_path = Path(str(session.get("manifestPath") or ""))
    if not manifest_path.is_absolute():
        return [], [f"{prefix}-RAW-MANIFEST-PATH"]
    session_root = manifest_path.resolve().parent
    relative = Path(str(reference.get("relativePath") or ""))
    target = (session_root / relative).resolve()
    try:
        target.relative_to(session_root)
    except ValueError:
        return [], [f"{prefix}-RAW-PATH-ESCAPE"]
    if not target.is_file():
        return [], [f"{prefix}-RAW-FILE-MISSING"]
    encoded = target.read_bytes()
    if hashlib.sha256(encoded).hexdigest().upper() != reference.get("sha256"):
        failures.append(f"{prefix}-RAW-HASH")
    if len(encoded) != reference.get("byteCount"):
        failures.append(f"{prefix}-RAW-BYTES")
    try:
        payload = json.loads(encoded.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return [], [*failures, f"{prefix}-RAW-JSON"]
    raw_samples = payload.get("rawSamples", [])
    if len(raw_samples) != reference.get("rawSampleCount"):
        failures.append(f"{prefix}-RAW-REFERENCE-COUNT")
    return raw_samples, failures


def validate_evidence(path: Path, expected_head: str) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    sessions = data.get("normalLauncherSessions", [])
    failures: list[str] = []
    if len(sessions) < 3:
        failures.append(f"OPTG-EVIDENCE-SESSIONS:{len(sessions)}")
    all_observations: list[dict[str, Any]] = []
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
        all_observations.extend(observations)
        states = [row.get("state") for row in observations]
        required_counts = {
            "startup-resident-idle": 1,
            "representative-active": 5,
            "post-use-resident-idle": 5,
            "long-settle-resident-idle": 1,
        }
        for state, count in required_counts.items():
            if states.count(state) != count:
                failures.append(f"{prefix}-STATE-{state}:{states.count(state)}")
        for observation in observations:
            state = observation.get("state")
            condition = observation.get("attributionCondition", "resident-baseline")
            inventories = [
                observation.get("surfaceInventoryBefore", {}),
                observation.get("surfaceInventoryAfter", {}),
            ]
            raw_samples, raw_failures = _externalized_raw_samples(
                session, observation, f"{prefix}-{state}-{condition}"
            )
            failures.extend(raw_failures)
            if observation.get("rawSampleCount") != len(raw_samples):
                failures.append(f"{prefix}-RAW-SAMPLE-COUNT-{state}")
            if observation.get("invalidSampleCount") != 0:
                failures.append(f"{prefix}-INVALID-SAMPLE-{state}")
            if observation.get("droppedSampleCount") != 0:
                failures.append(f"{prefix}-DROPPED-SAMPLE-{state}")
            if any(
                sample.get("productProcessCount") != len(sample.get("productProcesses", []))
                for sample in raw_samples
            ):
                failures.append(f"{prefix}-RAW-PROCESS-COUNT-{state}")
            process_rows = observation.get("perProcess", [])
            reproduced_cpu = round(
                sum(float(row.get("cpuTimeSeconds") or 0.0) for row in process_rows), 6
            )
            reported_cpu = round(
                float((observation.get("totalProductTree") or {}).get("cpuTimeSeconds") or 0.0),
                6,
            )
            if reproduced_cpu != reported_cpu:
                failures.append(f"{prefix}-RAW-CPU-PARITY-{state}")
            renderer_map = observation.get("surfaceRendererMap", [])
            mapped_by_surface = {
                row.get("surfaceId"): int(row.get("rendererPid") or 0)
                for row in renderer_map
            }
            expected_visible: set[str] = set()
            if state == "representative-active":
                if condition in {"hud-dashboard-only", "hud-log-viewer-bundle"}:
                    expected_visible.add("hud-dashboard")
                if condition in {"log-viewer-only", "hud-log-viewer-bundle"}:
                    expected_visible.add("nexus-log-viewer")
            for surface_id in expected_visible:
                renderer_pid = mapped_by_surface.get(surface_id, 0)
                if renderer_pid <= 0:
                    failures.append(f"{prefix}-RENDERER-PID-{state}-{surface_id}")
                    continue
                process_row = next(
                    (row for row in process_rows if row.get("pid") == renderer_pid),
                    {},
                )
                if process_row.get("role") != "webengine-renderer":
                    failures.append(
                        f"{prefix}-RENDERER-PROCESS-{state}-{surface_id}"
                    )
                if surface_id not in process_row.get("attributedSurfaceIds", []):
                    failures.append(
                        f"{prefix}-RENDERER-DIRECT-MAP-{state}-{surface_id}"
                    )
            memory_after = observation.get(
                "controllerMemoryAfterRawExternalization", {}
            )
            if memory_after.get("retainedRawSampleCount") != 0:
                failures.append(f"{prefix}-CONTROLLER-RAW-RETAINED-{state}")
            for inventory in inventories:
                hud = _surface(inventory, "hud-dashboard")
                log_viewer = _surface(inventory, "nexus-log-viewer")
                recording = _surface(inventory, "nexus-recording-suite")
                hud_expected = state == "representative-active" and condition in {
                    "hud-dashboard-only",
                    "hud-log-viewer-bundle",
                }
                log_expected = state == "representative-active" and condition in {
                    "log-viewer-only",
                    "hud-log-viewer-bundle",
                }
                if any(
                    timer.get("active") is not hud_expected
                    for timer in (
                        _timer(hud, "hud-resize-hover"),
                        _timer(hud, "hud-recording-control-click-bridge"),
                    )
                ):
                    failures.append(f"{prefix}-HUD-TIMER-{state}-{condition}")
                if (
                    _timer(log_viewer, "log-viewer-resize-hover").get("active")
                    is not log_expected
                ):
                    failures.append(f"{prefix}-LOG-TIMER-{state}-{condition}")
                recording_timer = _timer(recording, "recording-studio-resize-hover")
                if recording_timer.get("active") is not False:
                    failures.append(f"{prefix}-RECORDING-TIMER-{state}")
                if recording.get("studioResizable") is not False:
                    failures.append(f"{prefix}-RECORDING-RESIZABLE-{state}")
                if recording.get("width") != 432 or recording.get("height") != 154:
                    failures.append(f"{prefix}-RECORDING-GEOMETRY-{state}")
        if session.get("attributionSequence") != [
            "hud-dashboard-only",
            "log-viewer-only",
            "hud-log-viewer-bundle",
            "hud-log-viewer-bundle",
            "hud-log-viewer-bundle",
        ]:
            failures.append(f"{prefix}-ATTRIBUTION-SEQUENCE")
        condition_rows = [
            row.get("attributionCondition")
            for row in observations
            if row.get("state") == "representative-active"
        ]
        if condition_rows != session.get("attributionSequence"):
            failures.append(f"{prefix}-ATTRIBUTION-ORDER")
        controller_memory = session.get("controllerMemoryAccounting", {})
        if controller_memory.get("retainedRawSampleCount") != 0:
            failures.append(f"{prefix}-CONTROLLER-FINAL-RAW")
        if controller_memory.get("rawSamplesExternalizedToDisk") is not True:
            failures.append(f"{prefix}-CONTROLLER-STREAMING")
        if controller_memory.get("rawSampleFileCount") != len(observations):
            failures.append(f"{prefix}-CONTROLLER-RAW-FILE-COUNT")
        if not isinstance(
            controller_memory.get("retainedStructureDeepBytes"), dict
        ):
            failures.append(f"{prefix}-CONTROLLER-DEEP-SIZE")
        for observation in observations:
            overhead = observation.get("observerOverhead", {})
            if (overhead.get("ussMiB") or {}).get("median") is None:
                failures.append(f"{prefix}-OBSERVER-MEMORY")
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
    product_cpu = [
        float((row.get("totalProductTree") or {}).get("cpuCoreEquivalentPercent") or 0.0)
        for row in all_observations
    ]
    observer_cpu = [
        float((row.get("observerOverhead") or {}).get("cpuCoreEquivalentPercent") or 0.0)
        for row in all_observations
    ]
    relative_overhead = (
        statistics.median(observer_cpu) / statistics.median(product_cpu) * 100.0
        if product_cpu and statistics.median(product_cpu) > 0
        else None
    )
    if relative_overhead is None or relative_overhead > 5.0:
        failures.append(
            "OPTG-EVIDENCE-OBSERVER-OVERHEAD:"
            f"{relative_overhead if relative_overhead is not None else 'missing'}"
        )
    return failures


def _build_ws04_attribution_ledger(
    sessions: list[dict[str, Any]], root: Path, source_head: str
) -> dict[str, Any]:
    process_rows: list[dict[str, Any]] = []
    controller_rows: list[dict[str, Any]] = []
    monotonic_renderer_rows: list[dict[str, Any]] = []
    for session in sessions:
        session_index = int(session.get("sessionIndex") or 0)
        for observation in session.get("observations", []):
            condition = observation.get("attributionCondition", "resident-baseline")
            state = observation.get("state")
            for process in observation.get("perProcess", []):
                if process.get("role") not in {
                    "webengine-renderer",
                    "desktop-python-parent",
                }:
                    continue
                memory = process.get("memoryMiB") or {}
                process_rows.append(
                    {
                        "sessionIndex": session_index,
                        "requestId": observation.get("requestId"),
                        "state": state,
                        "cycleIndex": observation.get("cycleIndex"),
                        "attributionCondition": condition,
                        "pid": process.get("pid"),
                        "parentPid": process.get("parentPid"),
                        "creationTimeEpoch": process.get("creationTimeEpoch"),
                        "role": process.get("role"),
                        "attributedSurfaceIds": process.get(
                            "attributedSurfaceIds", []
                        ),
                        "ownerClassifications": process.get(
                            "attributedOwnerClassifications", []
                        ),
                        "attributionBasis": process.get(
                            "surfaceAttributionBasis"
                        ),
                        "ussMedianMiB": (memory.get("ussBytes") or {}).get(
                            "median"
                        ),
                        "privateCommitMedianMiB": (
                            memory.get("privateCommitBytes") or {}
                        ).get("median"),
                        "rssMedianMiB": (memory.get("rssBytes") or {}).get(
                            "median"
                        ),
                        "presentAtEnd": process.get("presentAtEnd"),
                        "evidencePath": observation.get("rawSamplesReference", {}).get(
                            "relativePath"
                        ),
                    }
                )
            controller_rows.append(
                {
                    "sessionIndex": session_index,
                    "requestId": observation.get("requestId"),
                    "state": state,
                    "cycleIndex": observation.get("cycleIndex"),
                    "attributionCondition": condition,
                    "controllerMemoryAfterRawExternalization": observation.get(
                        "controllerMemoryAfterRawExternalization", {}
                    ),
                    "rawSamplesReference": observation.get(
                        "rawSamplesReference", {}
                    ),
                }
            )
        bundle_post = [
            row
            for row in session.get("observations", [])
            if row.get("state") == "post-use-resident-idle"
            and row.get("attributionCondition") == "hud-log-viewer-bundle"
        ]
        renderer_pids = sorted(
            {
                int(process.get("pid"))
                for row in bundle_post
                for process in row.get("perProcess", [])
                if process.get("role") == "webengine-renderer"
            }
        )
        for pid in renderer_pids:
            pid_rows = [
                next(
                    (
                        process
                        for process in row.get("perProcess", [])
                        if process.get("role") == "webengine-renderer"
                        and int(process.get("pid")) == pid
                    ),
                    {},
                )
                for row in bundle_post
            ]
            uss_values = [
                float((row.get("memoryMiB", {}).get("ussBytes") or {}).get("median"))
                for row in pid_rows
                if (row.get("memoryMiB", {}).get("ussBytes") or {}).get("median")
                is not None
            ]
            surface_ids = sorted(
                {
                    surface_id
                    for row in pid_rows
                    for surface_id in row.get("attributedSurfaceIds", [])
                }
            )
            owners = sorted(
                {
                    owner
                    for row in pid_rows
                    for owner in row.get("attributedOwnerClassifications", [])
                }
            )
            monotonic = len(uss_values) == 3 and all(
                right > left for left, right in zip(uss_values, uss_values[1:])
            )
            if monotonic:
                monotonic_renderer_rows.append(
                    {
                        "sessionIndex": session_index,
                        "pid": pid,
                        "ussMedianMiBByRepeatedBundleClose": uss_values,
                        "attributedSurfaceIds": surface_ids,
                        "ownerClassifications": owners,
                        "directAttribution": bool(surface_ids),
                        "sharedRendererReuse": len(surface_ids) > 1,
                        "classification": "REPEATED_BUNDLE_CLOSE_MONOTONIC_USS_GROWTH",
                    }
                )

    foreign_or_excluded = [
        row
        for row in monotonic_renderer_rows
        if not row["directAttribution"]
        or row["sharedRendererReuse"]
        or any(
            owner.startswith("FAM-006")
            or owner in {"ORIN-CORE-UNRESOLVED", "FAM-007"}
            for owner in row["ownerClassifications"]
        )
    ]
    controller_final_rows = [
        session.get("controllerMemoryAccounting", {}) for session in sessions
    ]
    controller_raw_retention_excluded = all(
        row.get("retainedRawSampleCount") == 0
        and row.get("rawSamplesExternalizedToDisk") is True
        for row in controller_final_rows
    )
    if foreign_or_excluded:
        outcome = "FOREIGN_SHARED_OR_EXCLUDED_OWNER_BLOCKER"
    elif monotonic_renderer_rows:
        outcome = "UNKNOWN_OWNER_BLOCKER"
    else:
        outcome = "ACCEPTED_MEASUREMENT_INSTRUMENTATION_ONLY_NO_PRODUCT_REPAIR"
    allowlist_rows = [f"OPTG-ALLOW-{index:02d}" for index in range(1, 9)]
    payload = {
        "schema": "fam003-option-g-ws04-attribution-ledger-v1",
        "sourceHead": source_head,
        "sessionCount": len(sessions),
        "measurementMethodology": "DIRECT_PAGE_PID_PLUS_CONTROLLED_SURFACE_SEQUENCE_V5",
        "processRows": process_rows,
        "controllerRows": controller_rows,
        "controllerFinalAccounting": controller_final_rows,
        "controllerRawRetentionExcluded": controller_raw_retention_excluded,
        "monotonicRendererRows": monotonic_renderer_rows,
        "foreignSharedOrExcludedRows": foreign_or_excluded,
        "activatedAllowlistRows": [],
        "nonactivatedAllowlistRows": allowlist_rows,
        "allowlistTriggerDisposition": (
            "No named timer/lifecycle trigger remains active; renderer memory "
            "association does not activate timer allowlist repair."
        ),
        "recordingStudioDisposition": (
            "PROTECTED_NOT_OPENED_BY_ATTRIBUTION_SEQUENCE; STATIC_AND_TIMER_"
            "INVARIANTS_REVALIDATED"
        ),
        "ws04Outcome": outcome,
        "ws05Disposition": (
            "BLOCKED_NO_PRODUCT_MUTATION"
            if outcome.endswith("BLOCKER")
            else "SKIPPED_NO_PRODUCT_REPAIR_TRIGGER"
        ),
        "remainingUncertainty": (
            "Monotonic retained renderer memory maps to a foreign, shared, "
            "generic, or unresolved owner boundary."
            if outcome.endswith("BLOCKER")
            else "No repeated-bundle monotonic renderer growth remained after raw-sample externalization."
        ),
    }
    ledger_path = root / "fam003_option_g_ws04_attribution_ledger.json"
    ledger_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    markdown = root / "FAM003_OPTION_G_WS04_ATTRIBUTION_LEDGER.md"
    markdown.write_text(
        "# FAM-003 Option G WS04 Attribution Ledger\n\n"
        f"Source HEAD: `{source_head}`\n\n"
        f"Sessions: `{len(sessions)}`\n\n"
        f"WS04 Outcome: `{outcome}`\n\n"
        f"Controller Raw Retention Excluded: `{str(controller_raw_retention_excluded).upper()}`\n\n"
        f"Monotonic Renderer Rows: `{len(monotonic_renderer_rows)}`\n\n"
        f"Foreign / Shared / Excluded Rows: `{len(foreign_or_excluded)}`\n\n"
        "Activated Allowlist Rows: `NONE`\n\n"
        "WS05: `"
        + payload["ws05Disposition"]
        + "`\n\n"
        "The JSON ledger beside this review owns the complete per-process and "
        "controller-accounting evidence rows. It is generated evidence, not a "
        "new canonical planning owner.\n",
        encoding="utf-8",
    )
    payload["jsonPath"] = str(ledger_path)
    payload["markdownPath"] = str(markdown)
    payload["jsonSha256"] = hashlib.sha256(ledger_path.read_bytes()).hexdigest().upper()
    return payload


def _validate_attribution_ledger(ledger: dict[str, Any], expected_head: str) -> list[str]:
    failures: list[str] = []
    if ledger.get("sourceHead") != expected_head:
        failures.append("OPTG-ATTRIBUTION-HEAD")
    if ledger.get("sessionCount", 0) < 3:
        failures.append("OPTG-ATTRIBUTION-SESSIONS")
    if ledger.get("controllerRawRetentionExcluded") is not True:
        failures.append("OPTG-ATTRIBUTION-CONTROLLER-CONTAMINATION")
    if ledger.get("activatedAllowlistRows"):
        failures.append("OPTG-ATTRIBUTION-UNPROVEN-ALLOWLIST-ACTIVATION")
    allowed_outcomes = {
        "ACCEPTED_MEASUREMENT_INSTRUMENTATION_ONLY_NO_PRODUCT_REPAIR",
        "FOREIGN_SHARED_OR_EXCLUDED_OWNER_BLOCKER",
        "UNKNOWN_OWNER_BLOCKER",
    }
    if ledger.get("ws04Outcome") not in allowed_outcomes:
        failures.append("OPTG-ATTRIBUTION-OUTCOME")
    if not ledger.get("processRows") or not ledger.get("controllerRows"):
        failures.append("OPTG-ATTRIBUTION-ROWS")
    return failures


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def run_sessions(run_count: int, output_root: Path | None) -> tuple[Path, str]:
    from dev.orin_fam003_option_d_nonintrusive_performance_validation import (
        _launch_session,
        _runtime_processes,
        resolve_desktop_shortcut_for_current_root,
    )

    if run_count < 3:
        raise RuntimeError("Option G lifecycle proof requires at least three normal-launch sessions")
    head = _git("rev-parse", "HEAD")
    branch = _git("branch", "--show-current")
    if branch != "feature/fam-003-settings-resize-proof":
        raise RuntimeError(f"wrong FAM-003 carrier: {branch}")
    resolution = resolve_desktop_shortcut_for_current_root(ROOT)
    if resolution.get("mode") != "actual-desktop-shortcut-current-root":
        raise RuntimeError(f"exact current-root Desktop shortcut unavailable: {resolution}")
    if _runtime_processes():
        raise RuntimeError("an active FAM-003 desktop runtime would contaminate measurement")
    root = (
        output_root.resolve()
        if output_root is not None
        else LOG_ROOT / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    )
    root.mkdir(parents=True, exist_ok=False)
    sessions = [
        _launch_session(str(resolution["path"]), root, head, index)
        for index in range(1, run_count + 1)
    ]
    manifest = root / "fam003_option_g_lifecycle_retention_manifest.json"
    payload = {
        "schema": "fam003-option-g-lifecycle-retention-workstream-v1",
        "status": "PENDING_VALIDATION",
        "branch": branch,
        "sourceHead": head,
        "normalLauncher": resolution,
        "normalLauncherSessions": sessions,
        "formalH1Entered": False,
        "formalLiveValidationEntered": False,
        "utsRequested": False,
        "optionDTemporary": True,
    }
    attribution_ledger = _build_ws04_attribution_ledger(sessions, root, head)
    payload["ws04AttributionLedger"] = attribution_ledger
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failures = validate_evidence(manifest, head)
    failures.extend(_validate_attribution_ledger(attribution_ledger, head))
    payload["status"] = "PASS" if not failures else "FAIL"
    payload["validationFailures"] = failures
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise RuntimeError(f"Option G lifecycle evidence failed: {failures}")
    return manifest, head


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-base", default=DEFAULT_IMPLEMENTATION_BASE)
    parser.add_argument("--evidence-manifest", type=Path)
    parser.add_argument("--expected-head", default="")
    parser.add_argument("--run-sessions", type=int, default=0)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--skip-fixtures", action="store_true")
    args = parser.parse_args()

    renderer = RENDERER.read_text(encoding="utf-8")
    controller = CONTROLLER.read_text(encoding="utf-8")
    observer = OBSERVER.read_text(encoding="utf-8")
    failures = validate_sources(renderer, controller, observer)
    failures.extend(validate_changed_regions(renderer, args.implementation_base))
    fixture_count = 0
    if not args.skip_fixtures:
        fixture_payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
        fixture_count = len(fixture_payload.get("cases", []))
        failures.extend(validate_negative_fixtures(renderer, controller, observer))
    if args.run_sessions:
        try:
            generated_manifest, generated_head = run_sessions(
                args.run_sessions, args.output_root
            )
        except RuntimeError as exc:
            failures.append(f"OPTG-EVIDENCE-RUN:{exc}")
        else:
            args.evidence_manifest = generated_manifest
            args.expected_head = generated_head
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
