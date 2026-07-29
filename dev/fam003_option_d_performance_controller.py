"""Nonblocking Qt controller for externally observed Option D performance proof."""

from __future__ import annotations

import json
import hashlib
import os
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Callable

import psutil
from PySide6 import QtCore

from dev.fam003_option_d_performance_observer import METHODOLOGY_VERSION


MANIFEST_ENV = "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_MANIFEST"
SOURCE_HEAD_ENV = "NEXUS_FAM003_RENDERER_BACKEND_SOURCE_HEAD"
SESSION_INDEX_ENV = "NEXUS_FAM003_RENDERER_BACKEND_SESSION_INDEX"
LAUNCH_STARTED_NS_ENV = "NEXUS_FAM003_RENDERER_BACKEND_LAUNCH_STARTED_NS"
EXPECTED_FLAG = "--disable-gpu"
EXPECTED_POLICY = "temporary-shared-runtime-safety-policy"
EXPECTED_CLASSIFICATION = "shared-desktop-runtime-not-fam003-only"
SETTLE_DURATION_MS = 5_000
LONG_SETTLE_DURATION_MS = 20_000
SAMPLE_DURATION_MS = 10_000
SAMPLE_INTERVAL_MS = 250
POLL_INTERVAL_MS = 500
HEARTBEAT_INTERVAL_MS = 100
WORKLOAD_INTERVAL_MS = 750
REPEATED_CYCLE_COUNT = 3
ATTRIBUTION_CONDITIONS = (
    "hud-dashboard-only",
    "log-viewer-only",
    "hud-log-viewer-bundle",
)
ATTRIBUTION_SEQUENCE = (
    "hud-dashboard-only",
    "log-viewer-only",
    *("hud-log-viewer-bundle",) * REPEATED_CYCLE_COUNT,
)


def _deep_size(value: Any) -> int:
    seen: set[int] = set()

    def visit(item: Any) -> int:
        identity = id(item)
        if identity in seen:
            return 0
        seen.add(identity)
        size = sys.getsizeof(item)
        if isinstance(item, dict):
            return size + sum(visit(key) + visit(child) for key, child in item.items())
        if isinstance(item, (list, tuple, set, frozenset)):
            return size + sum(visit(child) for child in item)
        return size

    return visit(value)


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


class NonintrusivePerformanceController(QtCore.QObject):
    """Coordinates product state with an external sampler using ordinary QTimers."""

    def __init__(
        self,
        *,
        window,
        core_window,
        tray_entry,
        runtime_log_path: str,
        do_shutdown: Callable[[], None],
        runtime_milestone: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.window = window
        self.core_window = core_window
        self.tray_entry = tray_entry
        self.runtime_log_path = runtime_log_path
        self.do_shutdown = do_shutdown
        self.runtime_milestone = runtime_milestone
        self.manifest_path = Path(os.environ[MANIFEST_ENV]).resolve()
        self.session_root = self.manifest_path.parent
        self.request_root = self.session_root / "observer_requests"
        self.result_root = self.session_root / "observer_results"
        self.source_head = os.environ.get(SOURCE_HEAD_ENV, "")
        self.session_index = int(os.environ.get(SESSION_INDEX_ENV, "0") or 0)
        self.started_at = time.time()
        self.request_count = 0
        self.current_request: dict[str, Any] | None = None
        self.current_result_path: Path | None = None
        self.current_state_started_ns = 0
        self.current_cycle = 0
        self.pending_results: list[dict[str, Any]] = []
        self.surface_timelines: dict[str, Any] = {}
        self.cycle_results: list[dict[str, Any]] = []
        self.active_workload_events: list[dict[str, Any]] = []
        self.raw_sample_receipts: list[dict[str, Any]] = []
        self._workload_index = 0
        self._hud_original_geometry = None
        self._heartbeat_timestamps: list[int] = []
        self._heartbeat_callback_ns = 0
        self._poll_callback_ns = 0
        self._workload_callback_ns = 0
        self._lifecycle_callback_ns = 0
        self._lifecycle_callback_counts: dict[str, int] = {}
        self._lifecycle_timer_bindings: list[tuple[QtCore.QTimer, Callable[[], None]]] = []
        self._heartbeat_timer = QtCore.QTimer(self)
        self._heartbeat_timer.setInterval(HEARTBEAT_INTERVAL_MS)
        self._heartbeat_timer.timeout.connect(self._heartbeat)
        self._poll_timer = QtCore.QTimer(self)
        self._poll_timer.setInterval(POLL_INTERVAL_MS)
        self._poll_timer.timeout.connect(self._poll_observer_result)
        self._workload_timer = QtCore.QTimer(self)
        self._workload_timer.setInterval(WORKLOAD_INTERVAL_MS)
        self._workload_timer.timeout.connect(self._active_workload_tick)

    def _controller_memory_snapshot(self, label: str) -> dict[str, Any]:
        memory = psutil.Process(os.getpid()).memory_full_info()
        structures = {
            "pendingResults": self.pending_results,
            "surfaceTimelines": self.surface_timelines,
            "cycleResults": self.cycle_results,
            "activeWorkloadEvents": self.active_workload_events,
            "rawSampleReceipts": self.raw_sample_receipts,
        }
        return {
            "label": label,
            "capturedAtEpoch": time.time(),
            "desktopParentRssBytes": int(getattr(memory, "rss", 0)),
            "desktopParentUssBytes": int(getattr(memory, "uss", 0)),
            "retainedStructureDeepBytes": {
                key: _deep_size(value) for key, value in structures.items()
            },
            "pendingResultCount": len(self.pending_results),
            "retainedRawSampleCount": sum(
                len(row.get("rawSamples", [])) for row in self.pending_results
            ),
        }

    def _surface_renderer_map(self) -> list[dict[str, Any]]:
        candidates = (
            ("orin-core-visualization", self.core_window, "ORIN-CORE-UNRESOLVED"),
            ("hud-dashboard", self.window, "FAM-006-SURFACE/FAM-003-LIFECYCLE-CARRIER"),
            (
                "nexus-recording-suite",
                getattr(self.window, "_monitoring_hud_recording_studio_window", None),
                "FAM-006-PROTECTED",
            ),
            (
                "nexus-log-viewer",
                getattr(self.window, "_monitoring_hud_log_viewer_studio_window", None),
                "FAM-006-SURFACE/FAM-003-LIFECYCLE-CARRIER",
            ),
            (
                "ai-status-command-center",
                getattr(self.window, "_ai_control_center_dialog", None),
                "FAM-007",
            ),
        )
        rows: list[dict[str, Any]] = []
        for surface_id, widget, owner_classification in candidates:
            webview = getattr(widget, "webview", None) if widget is not None else None
            page = webview.page() if webview is not None else None
            try:
                pid = int(page.renderProcessPid()) if page is not None else 0
                url = webview.url().toString() if webview is not None else ""
            except RuntimeError:
                pid = 0
                url = ""
            rows.append(
                {
                    "surfaceId": surface_id,
                    "rendererPid": pid,
                    "pageUrl": url,
                    "ownerClassification": owner_classification,
                    "proofBasis": "QWebEnginePage.renderProcessPid measurement-only query",
                }
            )
        return rows

    def _externalize_raw_samples(self, result: dict[str, Any]) -> dict[str, Any]:
        raw_samples = result.pop("rawSamples", [])
        raw_payload = {
            "schema": "fam003-option-g-externalized-raw-samples-v1",
            "sourceHead": self.source_head,
            "sessionIndex": self.session_index,
            "requestId": result["requestId"],
            "state": result["state"],
            "cycleIndex": result.get("cycleIndex", 0),
            "attributionCondition": result.get("attributionCondition", "resident-baseline"),
            "rawSamples": raw_samples,
        }
        encoded = _json_bytes(raw_payload)
        relative_path = Path("raw_samples") / f"{result['requestId']}.json"
        target = self.session_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_bytes(encoded)
        temporary.replace(target)
        receipt = {
            "relativePath": relative_path.as_posix(),
            "sha256": hashlib.sha256(encoded).hexdigest().upper(),
            "byteCount": len(encoded),
            "rawSampleCount": len(raw_samples),
            "rawSampleDeepBytesBeforeRelease": _deep_size(raw_samples),
        }
        self.raw_sample_receipts.append(receipt)
        result["rawSamplesReference"] = receipt
        return receipt

    def start(self) -> None:
        self._attach_lifecycle_timer_probes()
        self.runtime_milestone(
            "RENDERER_MAIN|FAM003_OPTION_D_NONINTRUSIVE_PROBE_STARTED|formal_lv=false"
        )
        QtCore.QTimer.singleShot(SETTLE_DURATION_MS, self._request_startup_idle)

    def _lifecycle_timer_targets(self) -> tuple[tuple[str, object, str], ...]:
        return (
            ("hud-resize-hover", self.window, "_monitoring_hud_resize_hover_timer"),
            (
                "hud-recording-control-click-bridge",
                self.window,
                "_monitoring_hud_recording_control_click_bridge_timer",
            ),
            (
                "log-viewer-resize-hover",
                getattr(self.window, "_monitoring_hud_log_viewer_studio_window", None),
                "_resize_hover_timer",
            ),
            (
                "recording-studio-resize-hover",
                getattr(self.window, "_monitoring_hud_recording_studio_window", None),
                "_resize_hover_timer",
            ),
        )

    def _record_lifecycle_timer_callback(self, timer_id: str) -> None:
        started = time.perf_counter_ns()
        self._lifecycle_callback_counts[timer_id] = (
            self._lifecycle_callback_counts.get(timer_id, 0) + 1
        )
        self._lifecycle_callback_ns += time.perf_counter_ns() - started

    def _attach_lifecycle_timer_probes(self) -> None:
        if self._lifecycle_timer_bindings:
            return
        for timer_id, owner, attribute in self._lifecycle_timer_targets():
            timer = getattr(owner, attribute, None) if owner is not None else None
            if not isinstance(timer, QtCore.QTimer):
                continue
            callback = lambda timer_id=timer_id: self._record_lifecycle_timer_callback(timer_id)
            timer.timeout.connect(callback)
            self._lifecycle_timer_bindings.append((timer, callback))
            self._lifecycle_callback_counts.setdefault(timer_id, 0)

    def _detach_lifecycle_timer_probes(self) -> None:
        for timer, callback in self._lifecycle_timer_bindings:
            try:
                timer.timeout.disconnect(callback)
            except (RuntimeError, TypeError):
                pass
        self._lifecycle_timer_bindings.clear()

    def _lifecycle_timer_state(self, owner, attribute: str, timer_id: str) -> dict[str, Any]:
        timer = getattr(owner, attribute, None) if owner is not None else None
        if not isinstance(timer, QtCore.QTimer):
            return {
                "timerId": timer_id,
                "exists": False,
                "active": False,
                "intervalMs": None,
                "remainingTimeMs": None,
                "callbackCount": self._lifecycle_callback_counts.get(timer_id, 0),
            }
        return {
            "timerId": timer_id,
            "exists": True,
            "active": timer.isActive(),
            "intervalMs": timer.interval(),
            "remainingTimeMs": timer.remainingTime(),
            "callbackCount": self._lifecycle_callback_counts.get(timer_id, 0),
        }

    def _surface_inventory(self, state_label: str) -> dict[str, Any]:
        renderer_rows = {
            row["surfaceId"]: row for row in self._surface_renderer_map()
        }
        candidates = (
            ("orin-core-visualization", self.core_window, "startup-resident-webengine", True),
            ("hud-dashboard", self.window, "on-demand-webengine", False),
            ("global-settings-native", getattr(self.window, "_resident_access_settings_dialog", None), "on-demand-native", False),
            ("nexus-recording-suite", getattr(self.window, "_monitoring_hud_recording_studio_window", None), "on-demand-webengine", False),
            ("nexus-log-viewer", getattr(self.window, "_monitoring_hud_log_viewer_studio_window", None), "on-demand-webengine", False),
            ("ai-status-command-center", getattr(self.window, "_ai_control_center_dialog", None), "on-demand-webengine", False),
        )
        rows: list[dict[str, Any]] = []
        for surface_id, widget, classification, intentionally_persistent in candidates:
            exists = widget is not None
            try:
                visible = bool(exists and widget.isVisible())
                minimized = bool(exists and widget.isMinimized())
                page_ready = getattr(widget, "_page_ready", None) if exists else None
                width = int(widget.width()) if exists else None
                height = int(widget.height()) if exists else None
                studio_resizable = getattr(widget, "STUDIO_RESIZABLE", None) if exists else None
            except RuntimeError:
                exists = False
                visible = False
                minimized = False
                page_ready = None
                width = None
                height = None
                studio_resizable = None
            lifecycle_timers: list[dict[str, Any]] = []
            if surface_id == "hud-dashboard":
                lifecycle_timers = [
                    self._lifecycle_timer_state(
                        widget,
                        "_monitoring_hud_resize_hover_timer",
                        "hud-resize-hover",
                    ),
                    self._lifecycle_timer_state(
                        widget,
                        "_monitoring_hud_recording_control_click_bridge_timer",
                        "hud-recording-control-click-bridge",
                    ),
                ]
            elif surface_id == "nexus-log-viewer":
                lifecycle_timers = [
                    self._lifecycle_timer_state(
                        widget,
                        "_resize_hover_timer",
                        "log-viewer-resize-hover",
                    )
                ]
            elif surface_id == "nexus-recording-suite":
                lifecycle_timers = [
                    self._lifecycle_timer_state(
                        widget,
                        "_resize_hover_timer",
                        "recording-studio-resize-hover",
                    )
                ]
            rows.append(
                {
                    "surfaceId": surface_id,
                    "classification": classification,
                    "exists": exists,
                    "visible": visible,
                    "hidden": bool(exists and not visible),
                    "minimized": minimized,
                    "pageReady": page_ready,
                    "width": width,
                    "height": height,
                    "studioResizable": studio_resizable,
                    "intentionallyPersistent": intentionally_persistent,
                    "lifecycleTimers": lifecycle_timers,
                    "lifecycleTransitionGeneration": (
                        getattr(widget, "_monitoring_hud_lifecycle_transition_generation", None)
                        if surface_id == "hud-dashboard"
                        else None
                    ),
                    "rendererProcessPid": (
                        renderer_rows.get(surface_id, {}).get("rendererPid")
                    ),
                    "rendererPageUrl": (
                        renderer_rows.get(surface_id, {}).get("pageUrl")
                    ),
                }
            )
        tray_icon = getattr(self.tray_entry, "tray_icon", None)
        rows.append(
            {
                "surfaceId": "resident-tray-native",
                "classification": "startup-resident-native",
                "exists": tray_icon is not None,
                "visible": bool(tray_icon is not None and tray_icon.isVisible()),
                "hidden": False,
                "minimized": False,
                "pageReady": None,
                "intentionallyPersistent": True,
            }
        )
        return {
            "stateLabel": state_label,
            "capturedAtEpoch": time.time(),
            "surfaces": rows,
            "onDemandVisible": [
                row["surfaceId"]
                for row in rows
                if not row["intentionallyPersistent"] and (row["visible"] or row["minimized"])
            ],
            "persistentResidentVisible": [
                row["surfaceId"]
                for row in rows
                if row["intentionallyPersistent"] and row["visible"]
            ],
        }

    def _request_startup_idle(self) -> None:
        self._request_observation(
            state="startup-resident-idle",
            cycle_index=0,
            expected_on_demand=False,
            workload={
                "classification": "IDLE",
                "operation": "none",
                "inputCadenceMs": None,
                "expectedRenderingWork": "normal persistent ORIN Core and resident tray only",
            },
        )

    def _attribution_condition(self) -> str:
        if self.current_cycle <= 0:
            return "resident-baseline"
        return ATTRIBUTION_SEQUENCE[self.current_cycle - 1]

    def _condition_surface_ids(self) -> tuple[str, ...]:
        condition = self._attribution_condition()
        if condition == "hud-dashboard-only":
            return ("hud-dashboard",)
        if condition == "log-viewer-only":
            return ("nexus-log-viewer",)
        if condition == "hud-log-viewer-bundle":
            return ("hud-dashboard", "nexus-log-viewer")
        return ()

    def _request_observation(
        self,
        *,
        state: str,
        cycle_index: int,
        expected_on_demand: bool,
        workload: dict[str, Any],
    ) -> None:
        self.request_count += 1
        request_id = f"request_{self.request_count:02d}_{state}_cycle_{cycle_index}"
        inventory = self._surface_inventory(f"{state}-before")
        request = {
            "schema": "fam003-option-d-observation-request-v1",
            "methodologyVersion": METHODOLOGY_VERSION,
            "requestId": request_id,
            "sourceHead": self.source_head,
            "sessionIndex": self.session_index,
            "state": state,
            "cycleIndex": cycle_index,
            "attributionCondition": (
                self._attribution_condition()
                if state in {"representative-active", "post-use-resident-idle"}
                else "resident-baseline"
            ),
            "rootPid": os.getpid(),
            "sampleDurationMs": SAMPLE_DURATION_MS,
            "sampleIntervalMs": SAMPLE_INTERVAL_MS,
            "surfaceInventoryBefore": inventory,
            "surfaceRendererMap": self._surface_renderer_map(),
            "controllerMemoryBeforeObservation": self._controller_memory_snapshot(
                f"{state}-cycle-{cycle_index}-before-observation"
            ),
            "expectedOnDemandVisible": expected_on_demand,
            "workload": workload,
            "productEventLoop": "normal QApplication.exec lifecycle",
            "nestedEventPump": False,
            "screenshotOrDomInspectionDuringSample": False,
        }
        self.current_request = request
        self.current_result_path = self.result_root / f"{request_id}.json"
        self.current_state_started_ns = time.perf_counter_ns()
        self._heartbeat_timestamps = []
        self._heartbeat_callback_ns = 0
        self._poll_callback_ns = 0
        self._workload_callback_ns = 0
        self._heartbeat_timer.start()
        if state == "representative-active":
            self._workload_timer.start()
        _atomic_json(self.request_root / f"{request_id}.json", request)
        self._poll_timer.start()
        self.runtime_milestone(
            f"RENDERER_MAIN|FAM003_OPTION_D_OBSERVATION_REQUESTED|state={state}|cycle={cycle_index}|request={request_id}"
        )

    def _heartbeat(self) -> None:
        started = time.perf_counter_ns()
        self._heartbeat_timestamps.append(started)
        self._heartbeat_callback_ns += time.perf_counter_ns() - started

    def _poll_observer_result(self) -> None:
        started = time.perf_counter_ns()
        try:
            if self.current_result_path is None or not self.current_result_path.exists():
                return
            try:
                result = json.loads(self.current_result_path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                return
            self._poll_timer.stop()
            self._heartbeat_timer.stop()
            self._workload_timer.stop()
            inventory_after = self._surface_inventory(f"{result['state']}-after")
            expected_visible = bool((self.current_request or {}).get("expectedOnDemandVisible"))
            visible = bool(
                (self.current_request or {}).get("surfaceInventoryBefore", {}).get("onDemandVisible")
                or inventory_after.get("onDemandVisible")
            )
            heartbeat_gaps = [
                (right - left) / 1_000_000.0
                for left, right in zip(self._heartbeat_timestamps, self._heartbeat_timestamps[1:])
            ]
            result.update(
                {
                    "surfaceInventoryAfter": inventory_after,
                    "surfaceStateMatchesMethodology": visible is expected_visible,
                    "controllerInstrumentation": {
                        "runsInProductProcess": True,
                        "usesOrdinaryQTimerCallbacks": True,
                        "usesNestedEventLoop": False,
                        "callsQApplicationProcessEvents": False,
                        "callsSleepOnGuiThread": False,
                        "writesDuringMeasuredInterval": False,
                        "performsScreenshots": False,
                        "performsDomQueries": False,
                        "injectsInputDuringIdle": False,
                        "activeWorkloadUsesProductCallbacks": result["state"] == "representative-active",
                        "heartbeatIntervalMs": HEARTBEAT_INTERVAL_MS,
                        "heartbeatCount": len(self._heartbeat_timestamps),
                        "heartbeatP95GapMs": round(
                            statistics.quantiles(heartbeat_gaps, n=20)[18]
                            if len(heartbeat_gaps) >= 20
                            else max(heartbeat_gaps, default=0.0),
                            3,
                        ),
                        "heartbeatMaxGapMs": round(max(heartbeat_gaps, default=0.0), 3),
                        "heartbeatCallbackCpuEstimateMs": round(self._heartbeat_callback_ns / 1_000_000.0, 6),
                        "pollCallbackCpuEstimateMs": round(self._poll_callback_ns / 1_000_000.0, 6),
                        "workloadCallbackCpuEstimateMs": round(self._workload_callback_ns / 1_000_000.0, 6),
                    },
                }
            )
            raw_receipt = self._externalize_raw_samples(result)
            result["controllerMemoryAfterRawExternalization"] = (
                self._controller_memory_snapshot(
                    f"{result['state']}-cycle-{result.get('cycleIndex', 0)}-after-raw-externalization"
                )
            )
            result["controllerInstrumentation"]["rawSamplesExternalized"] = True
            result["controllerInstrumentation"]["rawSamplesReference"] = raw_receipt
            self.pending_results.append(result)
            self.runtime_milestone(
                f"RENDERER_MAIN|FAM003_OPTION_D_OBSERVATION_COMPLETE|state={result['state']}|cycle={result.get('cycleIndex', 0)}"
            )
            QtCore.QTimer.singleShot(0, lambda result=result: self._advance_after_result(result))
        finally:
            self._poll_callback_ns += time.perf_counter_ns() - started

    def _advance_after_result(self, result: dict[str, Any]) -> None:
        state = result["state"]
        if state == "startup-resident-idle":
            self.current_cycle = 1
            self._open_active_surfaces()
            return
        if state == "representative-active":
            self._close_active_surfaces()
            return
        if state == "post-use-resident-idle":
            self.cycle_results.append(
                {
                    "cycleIndex": self.current_cycle,
                    "activeRequestId": next(
                        row["requestId"]
                        for row in reversed(self.pending_results)
                        if row["state"] == "representative-active" and row.get("cycleIndex") == self.current_cycle
                    ),
                    "postUseRequestId": result["requestId"],
                }
            )
            if self.current_cycle < len(ATTRIBUTION_SEQUENCE):
                self.current_cycle += 1
                QtCore.QTimer.singleShot(750, self._open_active_surfaces)
            else:
                QtCore.QTimer.singleShot(LONG_SETTLE_DURATION_MS, self._request_long_settle)
            return
        if state == "long-settle-resident-idle":
            self._finish()

    def _open_active_surfaces(self) -> None:
        opened_at = time.perf_counter_ns()
        condition_surfaces = set(self._condition_surface_ids())
        if "hud-dashboard" in condition_surfaces:
            self.window.set_monitoring_hud_feature_enabled(
                True, source="fam003-option-g-attribution"
            )
            self.window.open_or_restore_monitoring_hud_dashboard(
                source="fam003-option-g-attribution"
            )
        log_viewer = getattr(self.window, "_monitoring_hud_log_viewer_studio_window", None)
        if "nexus-log-viewer" in condition_surfaces and log_viewer is not None:
            log_viewer.update_product_state(
                request_id=f"attribution-cycle-{self.current_cycle}",
                activate_window=True,
                parent_geometry=self.window.geometry(),
            )
        self._hud_original_geometry = self.window.geometry()
        QtCore.QTimer.singleShot(
            1_500,
            lambda opened_at=opened_at: self._active_surfaces_ready(opened_at),
        )

    def _active_surfaces_ready(self, opened_at: int) -> None:
        inventory = self._surface_inventory(f"active-cycle-{self.current_cycle}-ready")
        visible = set(inventory["onDemandVisible"])
        required = set(self._condition_surface_ids())
        if visible != required:
            self._fail(f"active surfaces failed to open: expected={sorted(required)} visible={sorted(visible)}")
            return
        elapsed_ms = (time.perf_counter_ns() - opened_at) / 1_000_000.0
        self.surface_timelines[f"cycle{self.current_cycle}"] = {
            "routeActivationToAllVisibleMs": round(elapsed_ms, 3),
            "interactiveReadyMs": round(elapsed_ms, 3),
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "UNPROVEN_NO_NONINTRUSIVE_PAINT_MARKER",
            "evidenceCollectionIncluded": False,
            "visibleSurfaces": sorted(visible),
        }
        self._workload_index = 0
        self._request_observation(
            state="representative-active",
            cycle_index=self.current_cycle,
            expected_on_demand=True,
            workload={
                "classification": "MEANINGFUL_SURFACE_SPECIFIC_ACTIVE",
                "operation": "320px bounded scroll on the active attribution surface set plus HUD-only bounded resize",
                "inputCadenceMs": WORKLOAD_INTERVAL_MS,
                "expectedRenderingWork": "WebEngine repaint/composition, HUD relayout, and child-window rendering",
                "attributionCondition": self._attribution_condition(),
                "surfaces": sorted(required),
            },
        )

    def _active_workload_tick(self) -> None:
        started = time.perf_counter_ns()
        try:
            candidate_map = {
                "hud-dashboard": self.window,
                "nexus-log-viewer": getattr(
                    self.window, "_monitoring_hud_log_viewer_studio_window", None
                ),
            }
            candidates = [
                (surface_id, candidate_map[surface_id])
                for surface_id in self._condition_surface_ids()
            ]
            surface_id, widget = candidates[self._workload_index % len(candidates)]
            direction = 320 if (self._workload_index // len(candidates)) % 2 == 0 else -320
            if widget is not None and widget.isVisible() and getattr(widget, "webview", None) is not None:
                widget.webview.page().runJavaScript(f"window.scrollBy(0, {direction});")
                self.active_workload_events.append(
                    {
                        "cycleIndex": self.current_cycle,
                        "atEpoch": time.time(),
                        "surfaceId": surface_id,
                        "action": "scroll",
                        "distancePx": direction,
                    }
                )
            if (
                surface_id == "hud-dashboard"
                and self._workload_index % 4 == 0
                and self._hud_original_geometry is not None
            ):
                original = self._hud_original_geometry
                grow = (self._workload_index // 4) % 2 == 0
                self.window.resize(
                    original.width() + (80 if grow else 0),
                    original.height() + (48 if grow else 0),
                )
                self.active_workload_events.append(
                    {
                        "cycleIndex": self.current_cycle,
                        "atEpoch": time.time(),
                        "surfaceId": "hud-dashboard",
                        "action": "bounded-resize",
                        "width": self.window.width(),
                        "height": self.window.height(),
                    }
                )
            self._workload_index += 1
        finally:
            self._workload_callback_ns += time.perf_counter_ns() - started

    def _close_active_surfaces(self) -> None:
        if self._hud_original_geometry is not None:
            self.window.setGeometry(self._hud_original_geometry)
        self.window.close_monitoring_hud_dashboard(source="fam003-option-g-attribution")
        for attribute in (
            "_monitoring_hud_log_viewer_studio_window",
        ):
            widget = getattr(self.window, attribute, None)
            if widget is not None:
                widget.close()
        QtCore.QTimer.singleShot(SETTLE_DURATION_MS, self._request_post_use_idle)

    def _request_post_use_idle(self) -> None:
        inventory = self._surface_inventory(f"post-use-cycle-{self.current_cycle}-settled")
        if inventory["onDemandVisible"]:
            self._fail(f"post-use on-demand surfaces remained visible: {inventory['onDemandVisible']}")
            return
        self._request_observation(
            state="post-use-resident-idle",
            cycle_index=self.current_cycle,
            expected_on_demand=False,
            workload={
                "classification": "IDLE",
                "operation": "none",
                "inputCadenceMs": None,
                "expectedRenderingWork": "normal persistent ORIN Core and resident tray after normal close/hide",
                "attributionCondition": self._attribution_condition(),
            },
        )

    def _request_long_settle(self) -> None:
        inventory = self._surface_inventory("long-settle-resident-idle-before")
        if inventory["onDemandVisible"]:
            self._fail(
                "long-settle on-demand surfaces remained visible: "
                f"{inventory['onDemandVisible']}"
            )
            return
        self._request_observation(
            state="long-settle-resident-idle",
            cycle_index=self.current_cycle,
            expected_on_demand=False,
            workload={
                "classification": "IDLE_LONG_SETTLE",
                "operation": "none",
                "inputCadenceMs": None,
                "settleDurationMs": LONG_SETTLE_DURATION_MS,
                "expectedRenderingWork": (
                    "normal persistent ORIN Core and resident tray after the final long settle"
                ),
            },
        )

    def _startup_timeline(self) -> dict[str, Any]:
        launch_started_ns = int(os.environ.get(LAUNCH_STARTED_NS_ENV, "0") or 0)
        controller_started_ns = int(self.started_at * 1_000_000_000)
        process_created_ns = int(psutil.Process(os.getpid()).create_time() * 1_000_000_000)
        first_visible_signal_ms = (
            round((controller_started_ns - launch_started_ns) / 1_000_000.0, 3)
            if launch_started_ns
            else None
        )
        return {
            "launcherInvocationMs": 0.0,
            "desktopParentProcessCreatedMs": (
                round((process_created_ns - launch_started_ns) / 1_000_000.0, 3)
                if launch_started_ns
                else None
            ),
            "qApplicationReadyMs": None,
            "qApplicationReadyDisposition": "UNPROVEN_NO_HIGH_RESOLUTION_RUNTIME_MARKER",
            "firstPersistentWebEngineViewCreatedMs": None,
            "firstPersistentWebEngineViewCreatedDisposition": "UNPROVEN_NO_HIGH_RESOLUTION_RUNTIME_MARKER",
            "domContentReadyMs": None,
            "domContentReadyDisposition": "UNPROVEN_NO_LAUNCH_RELATIVE_MARKER",
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "UNPROVEN_NO_NONINTRUSIVE_PAINT_MARKER",
            "firstVisibleProductSignalMs": first_visible_signal_ms,
            "firstVisibleProductSignalDefinition": "launcher invocation to CORE_VISUALIZATION_FIRST_VISIBLE callback that schedules this controller",
            "residentReadyMs": first_visible_signal_ms,
            "evidenceCollectionIncluded": False,
            "observerOverheadIncluded": False,
        }

    def _finish(self) -> None:
        startup = next(row for row in self.pending_results if row["state"] == "startup-resident-idle")
        post_rows = [row for row in self.pending_results if row["state"] == "post-use-resident-idle"]
        active_rows = [row for row in self.pending_results if row["state"] == "representative-active"]
        long_settle = next(
            row for row in self.pending_results if row["state"] == "long-settle-resident-idle"
        )
        startup_uss = float(startup["totalProductTree"]["ussMedianMiBSum"])
        post_uss = [float(row["totalProductTree"]["ussMedianMiBSum"]) for row in post_rows]
        repeated_cycle_trend = {
            "startupUssMedianMiB": startup_uss,
            "postUseUssMedianMiBByCycle": post_uss,
            "postUseMinusStartupUssMiBByCycle": [round(value - startup_uss, 3) for value in post_uss],
            "monotonicPostUseGrowth": all(right > left for left, right in zip(post_uss, post_uss[1:])),
            "classification": "MEASURED_NOT_AUTOMATICALLY_A_LEAK",
        }
        controller_memory_accounting = self._controller_memory_snapshot(
            "final-before-manifest-write"
        )
        controller_memory_accounting.update(
            {
                "rawSamplesExternalizedToDisk": True,
                "rawSampleFileCount": len(self.raw_sample_receipts),
                "rawSampleDiskByteCount": sum(
                    int(row["byteCount"]) for row in self.raw_sample_receipts
                ),
                "rawSampleDeepBytesBeforeRelease": sum(
                    int(row["rawSampleDeepBytesBeforeRelease"])
                    for row in self.raw_sample_receipts
                ),
                "retainedRawSampleCount": 0,
                "classification": (
                    "MEASUREMENT_RAW_SAMPLES_STREAMED_TO_DISK_"
                    "NO_LONG_LIVED_RAW_SAMPLE_RETENTION"
                ),
                "scope": (
                    "controller-owned Python structures only; desktop-parent USS "
                    "also includes product/runtime allocations"
                ),
            }
        )
        payload = {
            "schema": "fam003-option-d-nonintrusive-runtime-session-v1",
            "status": "PASS",
            "methodologyVersion": METHODOLOGY_VERSION,
            "sourceHead": self.source_head,
            "sessionIndex": self.session_index,
            "runtimeLog": self.runtime_log_path,
            "startedAtEpoch": self.started_at,
            "finishedAtEpoch": time.time(),
            "normalLauncherProof": True,
            "productEventLoop": {
                "lifecycle": "normal QApplication.exec",
                "nestedEventPump": False,
                "qApplicationProcessEventsCalls": 0,
                "guiThreadSleepCalls": 0,
            },
            "effectiveBackend": {
                "effectiveFlags": os.environ.get("NEXUS_RENDERER_EFFECTIVE_QTWEBENGINE_CHROMIUM_FLAGS", ""),
                "childInheritedFlags": os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", ""),
                "policy": os.environ.get("NEXUS_RENDERER_BACKEND_POLICY", ""),
                "classification": os.environ.get("NEXUS_RENDERER_BACKEND_CLASSIFICATION", ""),
                "temporary": True,
            },
            "startupTimeline": self._startup_timeline(),
            "observations": self.pending_results,
            "startupResidentIdle": startup,
            "representativeActiveCycles": active_rows,
            "postUseResidentIdleCycles": post_rows,
            "longSettleResidentIdle": long_settle,
            "repeatedCycleTrend": repeated_cycle_trend,
            "surfaceTimelines": self.surface_timelines,
            "activeWorkloadEvents": self.active_workload_events,
            "cycleResults": self.cycle_results,
            "attributionConditions": list(ATTRIBUTION_CONDITIONS),
            "attributionSequence": list(ATTRIBUTION_SEQUENCE),
            "finalSurfaceRendererMap": self._surface_renderer_map(),
            "controllerMemoryAccounting": controller_memory_accounting,
            "rawSampleReceipts": self.raw_sample_receipts,
            "observerRequestCount": self.request_count,
            "lifecycleTimerInstrumentation": {
                "callbackCounts": dict(sorted(self._lifecycle_callback_counts.items())),
                "callbackCpuEstimateMs": round(
                    self._lifecycle_callback_ns / 1_000_000.0, 6
                ),
                "includedInProductTotals": True,
                "purpose": "Option G named-timer lifecycle attribution only",
            },
            "formalH1Entered": False,
            "formalLiveValidationEntered": False,
            "utsRequested": False,
            "materialRegression": {
                "detected": None,
                "disposition": "USER_DECISION_REQUIRED",
                "baselineComparable": False,
                "requiredMetricsAdjudicated": True,
                "firstPaintProven": False,
                "reason": "nonintrusive absolute measurements are valid, but no safe equivalent baseline or governed threshold exists",
            },
        }
        stop = {
            "schema": "fam003-option-d-observer-stop-v1",
            "expectedRequestCount": self.request_count,
            "sourceHead": self.source_head,
        }
        _atomic_json(self.session_root / "observer_stop.json", stop)
        _atomic_json(self.manifest_path, payload)
        self._detach_lifecycle_timer_probes()
        self.runtime_milestone(
            f"RENDERER_MAIN|FAM003_OPTION_D_NONINTRUSIVE_PROBE_WRITTEN|status=PASS|manifest={self.manifest_path}|formal_lv=false"
        )
        QtCore.QTimer.singleShot(750, self.do_shutdown)

    def _fail(self, reason: str) -> None:
        self._heartbeat_timer.stop()
        self._poll_timer.stop()
        self._workload_timer.stop()
        self._detach_lifecycle_timer_probes()
        _atomic_json(
            self.manifest_path,
            {
                "schema": "fam003-option-d-nonintrusive-runtime-session-v1",
                "status": "FAIL",
                "failure": reason,
                "methodologyVersion": METHODOLOGY_VERSION,
                "sourceHead": self.source_head,
                "sessionIndex": self.session_index,
                "formalH1Entered": False,
                "formalLiveValidationEntered": False,
                "utsRequested": False,
            },
        )
        _atomic_json(
            self.session_root / "observer_stop.json",
            {
                "schema": "fam003-option-d-observer-stop-v1",
                "expectedRequestCount": self.request_count,
                "sourceHead": self.source_head,
            },
        )
        self.runtime_milestone(
            f"RENDERER_MAIN|FAM003_OPTION_D_NONINTRUSIVE_PROBE_FAILED|reason={reason}|formal_lv=false"
        )
        QtCore.QTimer.singleShot(500, self.do_shutdown)
