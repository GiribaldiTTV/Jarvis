"""Normal-launcher Workstream probe for the temporary shared WebEngine backend."""

from __future__ import annotations

import json
import os
import platform
import statistics
import time
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import psutil
from PySide6 import QtCore
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication


MANIFEST_ENV = "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_MANIFEST"
EVIDENCE_ROOT_ENV = "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_ROOT"
SOURCE_HEAD_ENV = "NEXUS_FAM003_RENDERER_BACKEND_SOURCE_HEAD"
SESSION_INDEX_ENV = "NEXUS_FAM003_RENDERER_BACKEND_SESSION_INDEX"
LAUNCH_STARTED_NS_ENV = "NEXUS_FAM003_RENDERER_BACKEND_LAUNCH_STARTED_NS"
EXPECTED_POLICY = "temporary-shared-runtime-safety-policy"
EXPECTED_CLASSIFICATION = "shared-desktop-runtime-not-fam003-only"
EXPECTED_FLAG = "--disable-gpu"
JAVASCRIPT_CALLBACK_MAX_ATTEMPTS = 3
PERFORMANCE_METHODOLOGY_VERSION = "fam003-option-d-nonintrusive-performance-v3"
PERFORMANCE_SETTLE_DURATION_MS = 5_000
PERFORMANCE_SAMPLE_DURATION_MS = 10_000
PERFORMANCE_SAMPLE_INTERVAL_MS = 250
_JAVASCRIPT_RETRY_EVENTS: list[dict[str, Any]] = []


class ProbeFailure(RuntimeError):
    pass


def _pump(duration_ms: int = 120) -> None:
    deadline = time.perf_counter() + max(0, duration_ms) / 1000.0
    while time.perf_counter() < deadline:
        QApplication.processEvents()
        time.sleep(0.012)


def _wait_for(predicate: Callable[[], bool], label: str, timeout_s: float = 8.0) -> float:
    started = time.perf_counter()
    while time.perf_counter() - started < timeout_s:
        QApplication.processEvents()
        if predicate():
            return (time.perf_counter() - started) * 1000.0
        time.sleep(0.025)
    raise ProbeFailure(f"timed out waiting for {label}")


def _geometry(widget) -> dict[str, int]:
    rect = widget.geometry()
    return {"x": rect.x(), "y": rect.y(), "width": rect.width(), "height": rect.height()}


def _exercise_resize(widget, label: str) -> dict[str, Any]:
    original = QRect(widget.geometry())
    minimum = widget.minimumSize()
    maximum = widget.maximumSize()
    candidates = (
        (max(minimum.width(), original.width() - 120), max(minimum.height(), original.height() - 120)),
        (min(maximum.width(), original.width() + 120), min(maximum.height(), original.height() + 120)),
    )
    target = next(
        ((width, height) for width, height in candidates if width != original.width() or height != original.height()),
        None,
    )
    if target is None:
        raise ProbeFailure(f"{label} exposes no usable resize range")
    widget.resize(*target)
    elapsed_ms = _wait_for(
        lambda: widget.width() != original.width() or widget.height() != original.height(),
        f"{label} geometry change",
    )
    return {
        "original": {"width": original.width(), "height": original.height()},
        "requested": {"width": target[0], "height": target[1]},
        "actual": {"width": widget.width(), "height": widget.height()},
        "minimum": {"width": minimum.width(), "height": minimum.height()},
        "maximum": {"width": maximum.width(), "height": maximum.height()},
        "elapsedMs": round(elapsed_ms, 2),
        "changed": True,
    }


def _exercise_monitoring_hud_resize(widget) -> dict[str, Any]:
    original = QRect(widget.geometry())
    minimum_width, minimum_height = widget._monitoring_hud_effective_window_minimum_size()
    requested = QRect(
        original.x(),
        original.y(),
        max(minimum_width, original.width() - 120),
        max(minimum_height, original.height() - 120),
    )
    target = widget._bound_monitoring_hud_window_resize_rect(requested)
    if target.size() == original.size():
        requested = QRect(
            original.x(),
            original.y(),
            original.width() + 120,
            original.height() + 120,
        )
        target = widget._bound_monitoring_hud_window_resize_rect(requested)
    if target.size() == original.size():
        raise ProbeFailure("HUD Dashboard exposes no usable bounded resize range")

    widget._monitoring_hud_user_geometry_override_active = True
    widget.setGeometry(target)
    widget._monitoring_hud_interactive_screen_rect = QRect(widget.geometry())
    widget._sync_monitoring_hud_resize_frame(force=True)
    elapsed_ms = _wait_for(
        lambda: widget.width() != original.width() or widget.height() != original.height(),
        "HUD Dashboard bounded geometry change",
    )
    actual = QRect(widget.geometry())
    return {
        "contract": "monitoring-hud-bounded-native-window-geometry",
        "original": {"width": original.width(), "height": original.height()},
        "requested": {"width": requested.width(), "height": requested.height()},
        "boundedTarget": {"width": target.width(), "height": target.height()},
        "actual": {"width": actual.width(), "height": actual.height()},
        "minimum": {"width": minimum_width, "height": minimum_height},
        "elapsedMs": round(elapsed_ms, 2),
        "changed": actual.size() != original.size(),
    }


def _restore_monitoring_hud_geometry(widget, rect: QRect) -> None:
    widget._monitoring_hud_user_geometry_override_active = True
    widget.setGeometry(widget._bound_monitoring_hud_window_resize_rect(rect))
    widget._monitoring_hud_interactive_screen_rect = QRect(widget.geometry())
    widget._sync_monitoring_hud_resize_frame(force=True)
    _pump(180)


def _javascript(webview, script: str, timeout_s: float = 6.0) -> Any:
    value: Any = None
    for attempt in range(1, JAVASCRIPT_CALLBACK_MAX_ATTEMPTS + 1):
        result: dict[str, Any] = {"done": False, "value": None}

        def complete(callback_value: Any, target: dict[str, Any] = result) -> None:
            target["value"] = callback_value
            target["done"] = True

        webview.page().runJavaScript(script, complete)
        try:
            _wait_for(lambda: bool(result["done"]), "JavaScript callback", timeout_s)
            value = result["value"]
            if attempt > 1:
                _JAVASCRIPT_RETRY_EVENTS.append(
                    {"attempt": attempt, "recovered": True, "exhausted": False}
                )
            break
        except ProbeFailure:
            exhausted = attempt == JAVASCRIPT_CALLBACK_MAX_ATTEMPTS
            _JAVASCRIPT_RETRY_EVENTS.append(
                {"attempt": attempt, "recovered": False, "exhausted": exhausted}
            )
            if exhausted:
                raise
            _pump(240)
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _dom_state(webview, *, interaction: str = "query") -> dict[str, Any]:
    if interaction == "scroll":
        script = """
        (function() {
          const root = document.scrollingElement || document.documentElement;
          const before = root ? root.scrollTop : 0;
          if (root) root.scrollTop = Math.max(0, root.scrollHeight - root.clientHeight);
          window.dispatchEvent(new Event('scroll'));
          const text = document.body ? String(document.body.innerText || '') : '';
          return JSON.stringify({
            readyState: document.readyState,
            textLength: text.trim().length,
            bodyChildCount: document.body ? document.body.children.length : 0,
            canvasCount: document.querySelectorAll('canvas').length,
            buttonCount: document.querySelectorAll('button').length,
            scrollHeight: root ? root.scrollHeight : 0,
            clientHeight: root ? root.clientHeight : 0,
            scrollBefore: before,
            scrollAfter: root ? root.scrollTop : 0,
            viewport: {width: window.innerWidth, height: window.innerHeight}
          });
        })();
        """
    else:
        script = """
        (function() {
          const root = document.scrollingElement || document.documentElement;
          const text = document.body ? String(document.body.innerText || '') : '';
          return JSON.stringify({
            readyState: document.readyState,
            textLength: text.trim().length,
            bodyChildCount: document.body ? document.body.children.length : 0,
            canvasCount: document.querySelectorAll('canvas').length,
            buttonCount: document.querySelectorAll('button').length,
            scrollHeight: root ? root.scrollHeight : 0,
            clientHeight: root ? root.clientHeight : 0,
            scrollTop: root ? root.scrollTop : 0,
            viewport: {width: window.innerWidth, height: window.innerHeight}
          });
        })();
        """
    value = _javascript(webview, script)
    return value if isinstance(value, dict) else {"error": "non-dict DOM result", "value": value}


def _dom_click(webview, selector: str) -> dict[str, Any]:
    script = f"""
    (function() {{
      const element = document.querySelector({json.dumps(selector)});
      if (!element) return JSON.stringify({{clicked:false, reason:'missing'}});
      if (element.disabled || element.getAttribute('aria-disabled') === 'true') {{
        return JSON.stringify({{clicked:false, reason:'disabled'}});
      }}
      element.focus();
      element.click();
      return JSON.stringify({{
        clicked:true,
        tag:String(element.tagName || ''),
        id:String(element.id || ''),
        text:String(element.textContent || '').trim()
      }});
    }})();
    """
    result = _javascript(webview, script)
    if not isinstance(result, dict) or result.get("clicked") is not True:
        raise ProbeFailure(f"normal routed DOM control was not clickable: {selector}: {result}")
    _pump(220)
    return result


def _deferred_ai_domain_state(webview) -> dict[str, Any]:
    script = """
    (function() {
      const selectors = [
        '#ai-control-center-open-control-surface-action',
        '#ai-control-center-open-readiness-surface-action',
        '#ai-control-center-open-maintenance-surface-action'
      ];
      return JSON.stringify(selectors.map((selector) => {
        const element = document.querySelector(selector);
        return {
          selector,
          present: Boolean(element),
          disabled: Boolean(element && (element.disabled || element.getAttribute('aria-disabled') === 'true')),
          control: element ? String(element.dataset.control || '') : '',
          targetWindow: element ? String(element.closest('[data-target-window]')?.dataset.targetWindow || '') : ''
        };
      }));
    })();
    """
    result = _javascript(webview, script)
    return {"rows": result if isinstance(result, list) else [], "allDeferred": bool(result) and all(row.get("disabled") for row in result)}


def _image_analysis(pixmap) -> dict[str, Any]:
    image = pixmap.toImage()
    width = image.width()
    height = image.height()
    colors: Counter[tuple[int, int, int, int]] = Counter()
    luminances: list[float] = []
    nontransparent = 0
    samples = 0
    step_x = max(1, width // 40)
    step_y = max(1, height // 32)
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            color = image.pixelColor(x, y)
            rgba = (color.red(), color.green(), color.blue(), color.alpha())
            colors[rgba] += 1
            samples += 1
            if color.alpha() > 8:
                nontransparent += 1
                luminances.append(0.2126 * color.red() + 0.7152 * color.green() + 0.0722 * color.blue())
    luminance_range = max(luminances) - min(luminances) if luminances else 0.0
    nontransparent_ratio = nontransparent / samples if samples else 0.0
    dominant_color_ratio = colors.most_common(1)[0][1] / samples if samples and colors else 1.0
    visually_populated = len(colors) >= 12 and dominant_color_ratio <= 0.90
    return {
        "width": width,
        "height": height,
        "sampleCount": samples,
        "uniqueSampleColors": len(colors),
        "dominantColorRatio": round(dominant_color_ratio, 4),
        "visuallyPopulated": visually_populated,
        "nonTransparentRatio": round(nontransparent_ratio, 4),
        "luminanceRange": round(luminance_range, 2),
        "nonBlank": width >= 100 and height >= 100 and visually_populated and nontransparent_ratio >= 0.15 and luminance_range >= 6.0,
    }


def _capture(widget, root: Path, label: str, surface_id: str) -> dict[str, Any]:
    widget.show()
    widget.raise_()
    widget.activateWindow()
    _pump(260)
    screen = widget.screen() or QApplication.primaryScreen()
    pixmap = widget.grab()
    method = "QWidget.grab"
    analysis = _image_analysis(pixmap) if not pixmap.isNull() else {"nonBlank": False}
    attempt = 1
    while attempt < 3 and not analysis.get("nonBlank"):
        _pump(420)
        pixmap = widget.grab()
        analysis = _image_analysis(pixmap) if not pixmap.isNull() else {"nonBlank": False}
        attempt += 1
    method = f"QWidget.grab-attempt-{attempt}"
    if pixmap.isNull() or pixmap.width() < 100 or pixmap.height() < 100 or not analysis["nonBlank"]:
        fallback = screen.grabWindow(int(widget.winId())) if screen is not None else pixmap
        fallback_analysis = _image_analysis(fallback) if not fallback.isNull() else {"nonBlank": False}
        if fallback_analysis["nonBlank"] or pixmap.isNull() or pixmap.width() < 100 or pixmap.height() < 100:
            pixmap = fallback
            analysis = fallback_analysis
            method = "QScreen.grabWindow-fallback"
    path = root / f"{label}.png"
    if not pixmap.save(str(path), "PNG"):
        raise ProbeFailure(f"could not save screenshot {path}")
    analysis.update(
        {
            "surfaceId": surface_id,
            "path": str(path),
            "bytes": path.stat().st_size,
            "captureMethod": method,
            "captureAttempts": attempt,
            "fullWindow": True,
            "geometry": _geometry(widget),
        }
    )
    if not analysis["nonBlank"]:
        raise ProbeFailure(f"blank/corrupt screenshot for {surface_id}: {analysis}")
    return analysis


def _process_role(process: psutil.Process, root_pid: int) -> tuple[str, str]:
    try:
        command_line = " ".join(process.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        command_line = ""
    if process.pid == root_pid:
        return "desktop-python-parent", command_line
    lowered = command_line.casefold()
    if "qtwebengineprocess" not in lowered:
        return "desktop-child-other", command_line
    if "--type=renderer" in lowered:
        return "webengine-renderer", command_line
    if "--type=gpu-process" in lowered:
        return "webengine-gpu-process-software-policy", command_line
    if "--type=utility" in lowered:
        return "webengine-utility", command_line
    if "--type=zygote" in lowered:
        return "webengine-zygote", command_line
    return "webengine-other", command_line


def _process_tree(root: psutil.Process) -> list[psutil.Process]:
    try:
        return [root, *root.children(recursive=True)]
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []


def _cpu_time_seconds(process: psutil.Process) -> float:
    cpu_times = process.cpu_times()
    return float(cpu_times.user + cpu_times.system)


def _pump_sample_interval(
    duration_ms: int,
    workload_callback: Callable[[], str | None] | None,
) -> tuple[list[float], list[str]]:
    deadline = time.perf_counter() + max(0, duration_ms) / 1000.0
    previous = time.perf_counter()
    gaps: list[float] = []
    interactions: list[str] = []
    if workload_callback is not None:
        interaction = workload_callback()
        if interaction:
            interactions.append(interaction)
    while time.perf_counter() < deadline:
        QApplication.processEvents()
        now = time.perf_counter()
        gaps.append((now - previous) * 1000.0)
        previous = now
        time.sleep(0.012)
    return gaps, interactions


def _sustained_process_sample(
    label: str,
    inventory_provider: Callable[[str], dict[str, Any]],
    *,
    expected_on_demand_visible: bool,
    workload_callback: Callable[[], str | None] | None = None,
) -> dict[str, Any]:
    root = psutil.Process(os.getpid())
    logical_cpu_count = max(1, int(psutil.cpu_count(logical=True) or 1))
    inventory_before = inventory_provider(f"{label}-before")
    raw_samples: list[dict[str, Any]] = []
    process_totals: dict[int, dict[str, Any]] = {}
    all_dispatch_gaps: list[float] = []
    interactions: list[str] = []
    started = time.perf_counter()
    sample_index = 0

    while (time.perf_counter() - started) * 1000.0 < PERFORMANCE_SAMPLE_DURATION_MS:
        remaining_ms = PERFORMANCE_SAMPLE_DURATION_MS - int((time.perf_counter() - started) * 1000.0)
        interval_ms = min(PERFORMANCE_SAMPLE_INTERVAL_MS, max(1, remaining_ms))
        before_processes = _process_tree(root)
        before_cpu: dict[int, float] = {}
        for process in before_processes:
            try:
                before_cpu[process.pid] = _cpu_time_seconds(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        interval_started = time.perf_counter()
        gaps, interval_interactions = _pump_sample_interval(interval_ms, workload_callback)
        interval_duration_s = max(0.001, time.perf_counter() - interval_started)
        all_dispatch_gaps.extend(gaps)
        interactions.extend(interval_interactions)
        rows: list[dict[str, Any]] = []
        for process in _process_tree(root):
            try:
                end_cpu = _cpu_time_seconds(process)
                cpu_delta = max(0.0, end_cpu - before_cpu.get(process.pid, end_cpu))
                rss_bytes = int(process.memory_info().rss)
                role, command_line = _process_role(process, root.pid)
                parent_pid = process.ppid()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            core_equivalent = (cpu_delta / interval_duration_s) * 100.0
            row = {
                "pid": process.pid,
                "parentPid": parent_pid,
                "name": process.name(),
                "role": role,
                "commandLine": command_line,
                "cpuTimeSeconds": round(cpu_delta, 6),
                "cpuCoreEquivalentPercent": round(core_equivalent, 3),
                "cpuWholeMachinePercent": round(core_equivalent / logical_cpu_count, 3),
                "rssBytes": rss_bytes,
                "rssMiB": round(rss_bytes / (1024 * 1024), 3),
            }
            rows.append(row)
            aggregate = process_totals.setdefault(
                process.pid,
                {
                    "pid": process.pid,
                    "parentPid": parent_pid,
                    "name": process.name(),
                    "role": role,
                    "commandLine": command_line,
                    "cpuTimeSeconds": 0.0,
                    "rssSamplesBytes": [],
                },
            )
            aggregate["cpuTimeSeconds"] += cpu_delta
            aggregate["rssSamplesBytes"].append(rss_bytes)
        raw_samples.append(
            {
                "sampleIndex": sample_index,
                "offsetMs": round((interval_started - started) * 1000.0, 3),
                "durationMs": round(interval_duration_s * 1000.0, 3),
                "processes": rows,
                "interactionTargets": interval_interactions,
            }
        )
        sample_index += 1

    duration_ms = (time.perf_counter() - started) * 1000.0
    duration_s = max(0.001, duration_ms / 1000.0)
    per_process: list[dict[str, Any]] = []
    for aggregate in sorted(process_totals.values(), key=lambda row: (row["role"], row["pid"])):
        cpu_seconds = float(aggregate.pop("cpuTimeSeconds"))
        rss_samples = list(aggregate.pop("rssSamplesBytes"))
        core_equivalent = (cpu_seconds / duration_s) * 100.0
        per_process.append(
            {
                **aggregate,
                "cpuTimeSeconds": round(cpu_seconds, 6),
                "cpuCoreEquivalentPercent": round(core_equivalent, 3),
                "cpuWholeMachinePercent": round(core_equivalent / logical_cpu_count, 3),
                "rssMedianMiB": round(statistics.median(rss_samples) / (1024 * 1024), 3),
                "rssMaxMiB": round(max(rss_samples) / (1024 * 1024), 3),
                "rssFinalMiB": round(rss_samples[-1] / (1024 * 1024), 3),
                "sampleCount": len(rss_samples),
            }
        )
    total_cpu_seconds = sum(float(row["cpuTimeSeconds"]) for row in per_process)
    tree_core_equivalent = (total_cpu_seconds / duration_s) * 100.0
    interval_rss_totals = [sum(int(row["rssBytes"]) for row in sample["processes"]) for sample in raw_samples]
    ordered_gaps = sorted(all_dispatch_gaps)
    p95_index = min(len(ordered_gaps) - 1, max(0, int(len(ordered_gaps) * 0.95)))
    inventory_after = inventory_provider(f"{label}-after")
    on_demand_visible = bool(inventory_before["onDemandVisible"] or inventory_after["onDemandVisible"])
    state_matches = on_demand_visible is expected_on_demand_visible
    idle_sample = workload_callback is None
    return {
        "methodologyVersion": PERFORMANCE_METHODOLOGY_VERSION,
        "label": label,
        "classification": "IDLE" if idle_sample else "REPRESENTATIVE_ACTIVE_WORKLOAD",
        "settleDurationMs": PERFORMANCE_SETTLE_DURATION_MS,
        "sampleDurationMs": round(duration_ms, 3),
        "requiredMinimumDurationMs": PERFORMANCE_SAMPLE_DURATION_MS,
        "sampleIntervalMs": PERFORMANCE_SAMPLE_INTERVAL_MS,
        "rawSampleCount": len(raw_samples),
        "logicalProcessorCount": logical_cpu_count,
        "cpuNormalization": {
            "coreEquivalentPercent": "100 percent equals one logical processor fully occupied over the measured wall interval; renderer-tree totals may exceed 100 percent",
            "wholeMachinePercent": "core-equivalent percent divided by logical processor count",
        },
        "surfaceInventoryBefore": inventory_before,
        "surfaceInventoryAfter": inventory_after,
        "expectedOnDemandVisible": expected_on_demand_visible,
        "surfaceStateMatchesMethodology": state_matches,
        "validationActivity": {
            "domInspection": False,
            "screenshotOrFileCapture": False,
            "evidenceGeneration": False,
            "eventLoopPump": True,
            "definedProductWorkload": not idle_sample,
            "contaminationDisposition": "NONE" if idle_sample else "EXPECTED_DEFINED_ACTIVE_WORKLOAD",
        },
        "workload": {
            "interactionCount": len(interactions),
            "interactionTargets": interactions,
            "inputRatePerSecond": round(len(interactions) / duration_s, 3),
            "operation": "rotating asynchronous 8px down/up WebEngine scroll pulse" if interactions else "none",
        },
        "perProcess": per_process,
        "totalRendererTree": {
            "processCount": len(per_process),
            "webEngineSubprocessCount": sum(1 for row in per_process if str(row["role"]).startswith("webengine-")),
            "cpuTimeSeconds": round(total_cpu_seconds, 6),
            "cpuCoreEquivalentPercent": round(tree_core_equivalent, 3),
            "cpuWholeMachinePercent": round(tree_core_equivalent / logical_cpu_count, 3),
            "rssMedianMiB": round(statistics.median(interval_rss_totals) / (1024 * 1024), 3),
            "rssMaxMiB": round(max(interval_rss_totals) / (1024 * 1024), 3),
            "rssFinalMiB": round(interval_rss_totals[-1] / (1024 * 1024), 3),
        },
        "responsiveness": {
            "iterationCount": len(all_dispatch_gaps),
            "medianDispatchGapMs": round(statistics.median(all_dispatch_gaps), 3),
            "p95DispatchGapMs": round(ordered_gaps[p95_index], 3),
            "maxDispatchGapMs": round(max(all_dispatch_gaps), 3),
            "unresponsiveIntervalOver1000Ms": any(gap > 1000.0 for gap in all_dispatch_gaps),
        },
        "rawSamples": raw_samples,
    }


def _record(steps: list[dict[str, Any]], step_id: str, passed: bool, detail: Any) -> None:
    steps.append({"id": step_id, "status": "PASS" if passed else "FAIL", "detail": detail})
    if not passed:
        raise ProbeFailure(f"{step_id} failed: {detail}")


def _run_legacy_intrusive_option_d_probe(
    *,
    window,
    core_window,
    tray_entry,
    runtime_log_path: str,
    do_shutdown: Callable[[], None],
    runtime_milestone: Callable[[str], None],
) -> None:
    manifest_path = Path(os.environ.get(MANIFEST_ENV, "")).resolve()
    evidence_root = Path(os.environ.get(EVIDENCE_ROOT_ENV, manifest_path.parent)).resolve()
    evidence_root.mkdir(parents=True, exist_ok=True)
    started_at = time.time()
    steps: list[dict[str, Any]] = []
    captures: list[dict[str, Any]] = []
    surfaces: dict[str, dict[str, Any]] = {}
    metrics: dict[str, Any] = {}
    original_geometries: dict[str, QRect] = {}
    failure = ""

    def current_surface_inventory(state_label: str) -> dict[str, Any]:
        candidates = (
            ("orin-core-visualization", core_window, "startup-resident-webengine", True),
            ("hud-dashboard", window, "on-demand-webengine", False),
            ("global-settings-native", getattr(window, "_resident_access_settings_dialog", None), "on-demand-native", False),
            ("nexus-recording-suite", getattr(window, "_monitoring_hud_recording_studio_window", None), "on-demand-webengine", False),
            ("nexus-log-viewer", getattr(window, "_monitoring_hud_log_viewer_studio_window", None), "on-demand-webengine", False),
            ("ai-status-command-center", getattr(window, "_ai_control_center_dialog", None), "on-demand-webengine", False),
        )
        rows: list[dict[str, Any]] = []
        for surface_id, widget, classification_name, intentionally_persistent in candidates:
            exists = widget is not None
            try:
                visible = bool(exists and widget.isVisible())
                minimized = bool(exists and widget.isMinimized())
                page_ready = getattr(widget, "_page_ready", None) if exists else None
            except RuntimeError:
                exists = False
                visible = False
                minimized = False
                page_ready = None
            rows.append(
                {
                    "surfaceId": surface_id,
                    "classification": classification_name,
                    "exists": exists,
                    "visible": visible,
                    "hidden": bool(exists and not visible),
                    "minimized": minimized,
                    "pageReady": page_ready,
                    "intentionallyPersistent": intentionally_persistent,
                }
            )
        tray_icon = getattr(tray_entry, "tray_icon", None)
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
        on_demand_visible = [
            row["surfaceId"]
            for row in rows
            if not row["intentionallyPersistent"] and (row["visible"] or row["minimized"])
        ]
        return {
            "stateLabel": state_label,
            "capturedAtEpoch": time.time(),
            "surfaces": rows,
            "onDemandVisible": on_demand_visible,
            "persistentResidentVisible": [
                row["surfaceId"] for row in rows if row["intentionallyPersistent"] and row["visible"]
            ],
        }

    def add_capture(widget, label: str, surface_id: str) -> dict[str, Any]:
        result = _capture(widget, evidence_root, label, surface_id)
        captures.append(result)
        return result

    def add_capture_matching_baseline(
        widget,
        label: str,
        surface_id: str,
        baseline: dict[str, Any],
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for comparison_attempt in range(1, 4):
            result = _capture(widget, evidence_root, label, surface_id)
            unique_ratio = float(result.get("uniqueSampleColors") or 0) / max(
                1.0, float(baseline.get("uniqueSampleColors") or 0)
            )
            byte_ratio = float(result.get("bytes") or 0) / max(1.0, float(baseline.get("bytes") or 0))
            dominant_limit = max(0.18, float(baseline.get("dominantColorRatio") or 0) * 2.5)
            comparison_pass = bool(
                unique_ratio >= 0.85
                and byte_ratio >= 0.75
                and float(result.get("dominantColorRatio") or 1.0) <= dominant_limit
            )
            result["baselineComparison"] = {
                "status": "PASS" if comparison_pass else "FAIL",
                "attempt": comparison_attempt,
                "maximumAttempts": 3,
                "uniqueColorRatio": round(unique_ratio, 4),
                "byteRatio": round(byte_ratio, 4),
                "dominantColorRatio": result.get("dominantColorRatio"),
                "dominantColorLimit": round(dominant_limit, 4),
            }
            if comparison_pass:
                captures.append(result)
                return result
            _pump(520)
        raise ProbeFailure(f"{surface_id} restored capture failed baseline visual coverage: {result}")

    def surface_result(
        surface_id: str,
        widget,
        webview,
        *,
        interaction: str,
        reopen: str,
        resize: str,
        expected_text: str | None = None,
    ) -> None:
        initial = _dom_state(webview)
        scrolled = _dom_state(webview, interaction="scroll")
        identity_present = True
        if expected_text:
            identity_present = bool(
                _javascript(
                    webview,
                    "Boolean((document.body ? String(document.body.innerText || '') : '')"
                    f".toLowerCase().includes({json.dumps(expected_text.casefold())}))",
                )
            )
        identity_proof = {
            "expectedText": expected_text or "NOT_APPLICABLE_WITH_REASON: animated canvas surface",
            "present": identity_present,
        }
        capture = add_capture(widget, f"{len(captures) + 1:02d}_{surface_id}_full_window", surface_id)
        passed = bool(
            initial.get("readyState") == "complete"
            and (int(initial.get("textLength") or 0) > 0 or int(initial.get("canvasCount") or 0) > 0)
            and identity_present
            and capture.get("nonBlank")
        )
        _record(
            steps,
            f"{surface_id}-initial-render",
            passed,
            {"dom": initial, "surfaceIdentity": identity_proof, "capture": capture},
        )
        surfaces[surface_id] = {
            "visualVerdict": "PASS" if passed else "FAIL",
            "functionalVerdict": "PASS" if passed else "FAIL",
            "initialDom": initial,
            "interactionDom": scrolled,
            "meaningfulInteraction": interaction,
            "closeReopen": reopen,
            "resize": resize,
            "identityProof": identity_proof,
            "initialCapture": capture,
            "evidence": [capture["path"]],
        }

    try:
        runtime_milestone("RENDERER_MAIN|FAM003_OPTION_D_WORKSTREAM_PROBE_STARTED|formal_lv=false")
        child_flags = (os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS") or "").strip()
        reported_flags = (os.environ.get("NEXUS_RENDERER_EFFECTIVE_QTWEBENGINE_CHROMIUM_FLAGS") or "").strip()
        policy = (os.environ.get("NEXUS_RENDERER_BACKEND_POLICY") or "").strip()
        classification = (os.environ.get("NEXUS_RENDERER_BACKEND_CLASSIFICATION") or "").strip()
        flag_tokens = child_flags.split()
        _record(
            steps,
            "effective-backend",
            child_flags == reported_flags
            and flag_tokens.count(EXPECTED_FLAG) == 1
            and policy == EXPECTED_POLICY
            and classification == EXPECTED_CLASSIFICATION,
            {
                "parentFlags": os.environ.get("NEXUS_RENDERER_PARENT_QTWEBENGINE_CHROMIUM_FLAGS", ""),
                "reportedEffectiveFlags": reported_flags,
                "childInheritedFlags": child_flags,
                "disableGpuCount": flag_tokens.count(EXPECTED_FLAG),
                "policy": policy,
                "classification": classification,
                "hardwareAccelerationDisabled": EXPECTED_FLAG in flag_tokens,
                "softwareCompositionActive": EXPECTED_FLAG in flag_tokens,
            },
        )

        launch_started_ns = int(os.environ.get(LAUNCH_STARTED_NS_ENV, "0") or 0)
        probe_started_ns = time.time_ns()
        first_visible_signal_ms = (
            round((probe_started_ns - launch_started_ns) / 1_000_000, 2)
            if launch_started_ns
            else None
        )
        renderer_process_start_ms = (
            round((psutil.Process(os.getpid()).create_time() * 1_000_000_000 - launch_started_ns) / 1_000_000, 2)
            if launch_started_ns
            else None
        )
        metrics["startupReadyMs"] = first_visible_signal_ms
        metrics["startupTimeline"] = {
            "definition": "high-resolution launcher invocation to the product CORE_VISUALIZATION_FIRST_VISIBLE callback that schedules this probe",
            "launcherInvocationMs": 0.0,
            "rendererProcessStartMs": renderer_process_start_ms,
            "qApplicationCreatedMs": None,
            "qApplicationCreatedDisposition": "EVENT_EXISTS_IN_RUNTIME_LOG_WITH_SECOND_RESOLUTION_ONLY_NOT_USED_AS_A_PRECISION_METRIC",
            "webEngineViewCreationMs": None,
            "webEngineViewCreationDisposition": "NOT_INSTRUMENTED_BY_CURRENT_ARCHITECTURE",
            "pageLoadStartMs": None,
            "pageLoadStartDisposition": "NOT_INSTRUMENTED_BY_CURRENT_ARCHITECTURE",
            "domContentReadyMs": None,
            "domContentReadyDisposition": "PAGE_READY_PRECEDES_FIRST_VISIBLE_SIGNAL_BUT_HAS_NO_HIGH_RESOLUTION_LAUNCH_RELATIVE_EVENT",
            "firstVisiblePaintSignalMs": first_visible_signal_ms,
            "stableResidentReadyMs": first_visible_signal_ms,
            "observerOverheadIncluded": False,
            "screenshotOrDomInspectionIncluded": False,
            "eventProvenance": "DesktopRuntimeWindow.core_visualization_visible / CORE_VISUALIZATION_FIRST_VISIBLE",
        }
        metrics["machine"] = {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "qt": QtCore.qVersion(),
            "logicalCpuCount": psutil.cpu_count(logical=True),
            "physicalMemoryGiB": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        }

        _wait_for(lambda: bool(core_window.is_core_visualization_ready()), "ORIN Core ready")
        _pump(PERFORMANCE_SETTLE_DURATION_MS)
        metrics["startupResidentIdle"] = _sustained_process_sample(
            "startup-resident-idle",
            current_surface_inventory,
            expected_on_demand_visible=False,
        )
        _record(
            steps,
            "startup-resident-idle-methodology",
            metrics["startupResidentIdle"]["surfaceStateMatchesMethodology"]
            and metrics["startupResidentIdle"]["sampleDurationMs"] >= PERFORMANCE_SAMPLE_DURATION_MS,
            {
                "onDemandVisible": metrics["startupResidentIdle"]["surfaceInventoryBefore"]["onDemandVisible"],
                "sampleDurationMs": metrics["startupResidentIdle"]["sampleDurationMs"],
            },
        )
        surface_result(
            "orin-core-visualization",
            core_window,
            core_window.webview,
            interaction="animated canvas sampled twice",
            reopen="NOT_APPLICABLE_WITH_REASON: startup-resident core is not independently closeable",
            resize="NOT_APPLICABLE_WITH_REASON: fixed resident visualization geometry",
        )
        _pump(420)
        second_core = add_capture(core_window, "02_orin-core-visualization_animation_followup", "orin-core-visualization")
        surfaces["orin-core-visualization"]["evidence"].append(second_core["path"])
        metrics["surfaceTimelines"] = {}

        tray_entry.global_settings_action.trigger()
        settings_open_ms = _wait_for(
            lambda: bool(getattr(window, "_resident_access_settings_dialog", None) and window._resident_access_settings_dialog.isVisible()),
            "Global Settings from tray",
        )
        dialog = window._resident_access_settings_dialog
        metrics["surfaceTimelines"]["globalSettings"] = {
            "routeActivationToVisibleMs": round(settings_open_ms, 2),
            "interactiveReadyMs": round(settings_open_ms, 2),
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "NATIVE_QT_SURFACE_NO_SEPARATE_PAINT_EVENT_IN_CURRENT_ARCHITECTURE",
            "evidenceCollectionIncluded": False,
        }
        dialog.set_focus("hud_dashboard")
        _pump(250)
        add_capture(dialog, "03_global_settings_hud_disabled", "global-settings-native")
        _record(steps, "global-settings-hud-route", dialog._focus == "hud_dashboard", {"openMs": settings_open_ms, "focus": dialog._focus})

        if dialog.hud_enabled_checkbox.isChecked():
            dialog.hud_enabled_checkbox.click()
            _wait_for(lambda: not dialog.hud_enabled_checkbox.isChecked(), "isolated HUD reset to disabled")
        enable_started = time.perf_counter()
        dialog.hud_enabled_checkbox.click()
        enable_ms = _wait_for(
            lambda: bool(window.monitoring_hud_feature_state().get("feature_enabled") and window.isVisible()),
            "HUD enable and automatic Dashboard open",
            12.0,
        )
        metrics["hudAutomaticOpenMs"] = round((time.perf_counter() - enable_started) * 1000.0, 2)
        metrics["surfaceTimelines"]["hudDashboard"] = {
            "routeActivationToVisibleMs": metrics["hudAutomaticOpenMs"],
            "interactiveReadyMs": metrics["hudAutomaticOpenMs"],
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "VIEW_IS_PRELOADED_AND_CURRENT_ARCHITECTURE_EXPOSES_VISIBILITY_AND_PAGE_READY_WITHOUT_A_ROUTE_RELATIVE_PAINT_EVENT",
            "evidenceCollectionIncluded": False,
        }
        _record(
            steps,
            "hud-enable-auto-open",
            dialog.hud_enabled_checkbox.isChecked() and window.isVisible(),
            {"waitMs": enable_ms, "state": window.monitoring_hud_feature_state()},
        )
        add_capture(dialog, "04_global_settings_hud_enabled", "global-settings-native")
        dialog.hide()
        _wait_for(lambda: not dialog.isVisible(), "Global Settings hidden before Dashboard proof")
        original_geometries["hud-dashboard"] = QRect(window.geometry())
        surface_result(
            "hud-dashboard",
            window,
            window.webview,
            interaction="normal Settings enable plus HUD document scroll/query",
            reopen="tray HUD action closes/opens/restores existing singleton",
            resize="supported and exercised",
            expected_text="HUD Dashboard",
        )
        hud_resize = _exercise_monitoring_hud_resize(window)
        resized_capture = add_capture(window, "06_hud-dashboard_resized", "hud-dashboard")
        _restore_monitoring_hud_geometry(window, original_geometries["hud-dashboard"])
        surfaces["hud-dashboard"]["evidence"].append(resized_capture["path"])
        surfaces["hud-dashboard"]["resizeProof"] = hud_resize
        _record(steps, "hud-dashboard-resize", hud_resize["changed"], hud_resize)

        recording_open_started = time.perf_counter()
        _dom_click(window.webview, "#monitoring-hud-recording-studio-open")
        recording = window._monitoring_hud_recording_studio_window
        _wait_for(lambda: bool(recording and recording.isVisible() and recording._page_ready), "Recording Suite normal HUD route")
        recording_open_ms = round((time.perf_counter() - recording_open_started) * 1000.0, 2)
        metrics["surfaceTimelines"]["recordingSuite"] = {
            "routeActivationToVisibleMs": recording_open_ms,
            "interactiveReadyMs": recording_open_ms,
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "CURRENT_CHILD_WINDOW_EXPOSES_PAGE_READY_WITHOUT_A_ROUTE_RELATIVE_PAINT_EVENT",
            "evidenceCollectionIncluded": False,
        }
        original_geometries["recording-suite"] = QRect(recording.geometry())
        surface_result(
            "nexus-recording-suite",
            recording,
            recording.webview,
            interaction="normal OPEN LOG VIEWER routed control plus minimize/restore",
            reopen="normal HUD Recording Suite button",
            resize="NOT_APPLICABLE_WITH_REASON: current Recording Suite is fixed-size by product contract",
            expected_text="Recording Suite",
        )

        log_open_started = time.perf_counter()
        _dom_click(recording.webview, "#monitoring-hud-studio-open-log-viewer-action")
        log_viewer = window._monitoring_hud_log_viewer_studio_window
        _wait_for(lambda: bool(log_viewer and log_viewer.isVisible() and log_viewer._page_ready), "Log Viewer from Recording Suite")
        log_open_ms = round((time.perf_counter() - log_open_started) * 1000.0, 2)
        metrics["surfaceTimelines"]["logViewer"] = {
            "routeActivationToVisibleMs": log_open_ms,
            "interactiveReadyMs": log_open_ms,
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "CURRENT_CHILD_WINDOW_EXPOSES_PAGE_READY_WITHOUT_A_ROUTE_RELATIVE_PAINT_EVENT",
            "evidenceCollectionIncluded": False,
        }
        original_geometries["log-viewer"] = QRect(log_viewer.geometry())
        surface_result(
            "nexus-log-viewer",
            log_viewer,
            log_viewer.webview,
            interaction="Recording Suite route plus document query and supported resize",
            reopen="normal HUD Log Viewer button",
            resize="supported and exercised",
            expected_text="Log Viewer",
        )
        log_original = QRect(log_viewer.geometry())
        log_viewer.resize(log_original.width() + 74, log_original.height() + 44)
        _pump(260)
        log_resized = add_capture(log_viewer, "09_nexus-log-viewer_resized", "nexus-log-viewer")
        log_viewer.setGeometry(log_original)
        surfaces["nexus-log-viewer"]["evidence"].append(log_resized["path"])

        _dom_click(recording.webview, "#monitoring-hud-studio-minimize-action")
        _wait_for(lambda: recording.isMinimized(), "Recording Suite minimize")
        _dom_click(window.webview, "#monitoring-hud-recording-studio-open")
        _wait_for(lambda: recording.isVisible() and not recording.isMinimized(), "Recording Suite restore")
        recording_restore = add_capture_matching_baseline(
            recording,
            "10_nexus-recording-suite_restored",
            "nexus-recording-suite",
            surfaces["nexus-recording-suite"]["initialCapture"],
        )
        surfaces["nexus-recording-suite"]["evidence"].append(recording_restore["path"])
        surfaces["nexus-recording-suite"]["restoreProof"] = recording_restore["baselineComparison"]

        _dom_click(log_viewer.webview, "#monitoring-hud-studio-close-action")
        _wait_for(lambda: not log_viewer.isVisible(), "Log Viewer close")
        _dom_click(window.webview, "#monitoring-hud-recording-open-folder")
        _wait_for(lambda: log_viewer.isVisible(), "Log Viewer reopen from HUD")
        log_reopen = add_capture_matching_baseline(
            log_viewer,
            "11_nexus-log-viewer_reopened",
            "nexus-log-viewer",
            surfaces["nexus-log-viewer"]["initialCapture"],
        )
        surfaces["nexus-log-viewer"]["evidence"].append(log_reopen["path"])
        surfaces["nexus-log-viewer"]["restoreProof"] = log_reopen["baselineComparison"]

        ai_open_started = time.perf_counter()
        tray_entry.ai_status_action.trigger()
        _wait_for(
            lambda: bool(getattr(window, "_ai_control_center_dialog", None) and window._ai_control_center_dialog.isVisible()),
            "AI Dashboard from tray",
        )
        ai_dashboard = window._ai_control_center_dialog
        _wait_for(lambda: bool(ai_dashboard._page_ready), "AI Dashboard WebEngine ready")
        ai_open_ms = round((time.perf_counter() - ai_open_started) * 1000.0, 2)
        metrics["surfaceTimelines"]["aiDashboard"] = {
            "routeActivationToVisibleMs": ai_open_ms,
            "interactiveReadyMs": ai_open_ms,
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "CURRENT_CHILD_WINDOW_EXPOSES_PAGE_READY_WITHOUT_A_ROUTE_RELATIVE_PAINT_EVENT",
            "evidenceCollectionIncluded": False,
        }
        original_geometries["ai-dashboard"] = QRect(ai_dashboard.geometry())
        surface_result(
            "ai-status-command-center",
            ai_dashboard,
            ai_dashboard.webview,
            interaction="normal AI tray route, scroll, minimize/restore, close/reopen",
            reopen="normal tray AI Status / Command Center action",
            resize="supported; existing renderer validator owns detailed geometry proof",
            expected_text="AI Dashboard",
        )
        deferred_domains = _deferred_ai_domain_state(ai_dashboard.webview)
        _record(steps, "ai-domain-routes-remain-deferred", deferred_domains.get("allDeferred") is True, deferred_domains)
        surfaces["ai-control-center-domain"] = {
            "visualVerdict": "NOT_APPLICABLE_WITH_REASON",
            "functionalVerdict": "NOT_APPLICABLE_WITH_REASON",
            "reason": "current AI Dashboard source truth exposes a disabled deferred doorway; detached child is not an accepted current product route",
            "routeState": deferred_domains,
        }
        surfaces["readiness-diagnostics-domain"] = dict(surfaces["ai-control-center-domain"])
        surfaces["capabilities-maintenance-domain"] = dict(surfaces["ai-control-center-domain"])

        ai_resize = _exercise_resize(ai_dashboard, "AI Status / Command Center")
        ai_resized = add_capture(ai_dashboard, "13_ai-status-command-center_resized", "ai-status-command-center")
        surfaces["ai-status-command-center"]["evidence"].append(ai_resized["path"])
        surfaces["ai-status-command-center"]["resizeProof"] = ai_resize
        _record(steps, "ai-status-command-center-resize", ai_resize["changed"], ai_resize)
        ai_dashboard.setGeometry(original_geometries["ai-dashboard"])

        _dom_click(ai_dashboard.webview, "#ai-control-center-minimize-action")
        _wait_for(lambda: ai_dashboard.isMinimized(), "AI Dashboard minimize")
        tray_entry.ai_status_action.trigger()
        _wait_for(lambda: ai_dashboard.isVisible() and not ai_dashboard.isMinimized(), "AI Dashboard restore")
        ai_restore = add_capture_matching_baseline(
            ai_dashboard,
            "14_ai-status-command-center_restored",
            "ai-status-command-center",
            surfaces["ai-status-command-center"]["initialCapture"],
        )
        surfaces["ai-status-command-center"]["evidence"].append(ai_restore["path"])
        surfaces["ai-status-command-center"]["restoreProof"] = ai_restore["baselineComparison"]
        _dom_click(ai_dashboard.webview, "#ai-control-center-close-action")
        _wait_for(lambda: not ai_dashboard.isVisible(), "AI Dashboard close")
        tray_entry.ai_status_action.trigger()
        _wait_for(lambda: ai_dashboard.isVisible(), "AI Dashboard reopen")

        window.request_monitoring_hud_dashboard_from_tray(source="fam003-option-d-close", visible=False)
        _wait_for(lambda: not window.isVisible(), "HUD close before tray restore")
        restore_started = time.perf_counter()
        tray_entry.monitoring_hud_dashboard_action.trigger()
        _wait_for(lambda: window.isVisible(), "HUD tray restore")
        metrics["hudTrayRestoreMs"] = round((time.perf_counter() - restore_started) * 1000.0, 2)
        metrics["surfaceTimelines"]["hudDashboardRestore"] = {
            "routeActivationToVisibleMs": metrics["hudTrayRestoreMs"],
            "interactiveReadyMs": metrics["hudTrayRestoreMs"],
            "firstVisiblePaintMs": None,
            "firstVisiblePaintDisposition": "RESTORED_PRELOADED_SINGLETON_HAS_NO_SEPARATE_ROUTE_RELATIVE_PAINT_EVENT",
            "evidenceCollectionIncluded": False,
        }
        tray_entry.monitoring_hud_dashboard_action.trigger()
        _pump(220)
        _record(
            steps,
            "hud-repeated-open-is-idempotent",
            window.isVisible() and bool(window.monitoring_hud_feature_state().get("dashboard_visible")),
            window.monitoring_hud_feature_state(),
        )
        hud_restore = add_capture_matching_baseline(
            window,
            "15_hud-dashboard_tray_restored",
            "hud-dashboard",
            surfaces["hud-dashboard"]["initialCapture"],
        )
        surfaces["hud-dashboard"]["evidence"].append(hud_restore["path"])
        surfaces["hud-dashboard"]["restoreProof"] = hud_restore["baselineComparison"]

        active_webviews = [
            ("orin-core-visualization", core_window.webview),
            ("hud-dashboard", window.webview),
            ("nexus-recording-suite", recording.webview),
            ("nexus-log-viewer", log_viewer.webview),
            ("ai-status-command-center", ai_dashboard.webview),
        ]
        active_index = 0

        def active_workload_pulse() -> str:
            nonlocal active_index
            surface_id, view = active_webviews[active_index % len(active_webviews)]
            view.page().runJavaScript("window.scrollBy(0, 8); window.scrollBy(0, -8);")
            active_index += 1
            return surface_id

        _pump(PERFORMANCE_SETTLE_DURATION_MS)
        metrics["representativeActive"] = _sustained_process_sample(
            "representative-active",
            current_surface_inventory,
            expected_on_demand_visible=True,
            workload_callback=active_workload_pulse,
        )
        metrics["responsiveness"] = metrics["representativeActive"]["responsiveness"]
        _record(
            steps,
            "responsiveness-no-freeze",
            metrics["representativeActive"]["surfaceStateMatchesMethodology"]
            and not metrics["responsiveness"]["unresponsiveIntervalOver1000Ms"],
            {
                "surfaceStateMatchesMethodology": metrics["representativeActive"]["surfaceStateMatchesMethodology"],
                "responsiveness": metrics["responsiveness"],
            },
        )

        dialog.show()
        dialog.set_focus("hud_dashboard")
        _pump(180)
        if not dialog.hud_enabled_checkbox.isChecked():
            raise ProbeFailure("HUD unexpectedly disabled before final disable step")
        dialog.hud_enabled_checkbox.click()
        _wait_for(
            lambda: not bool(window.monitoring_hud_feature_state().get("feature_enabled")) and not window.isVisible(),
            "HUD disable closes Dashboard",
            10.0,
        )
        tray_entry.refresh_monitoring_hud_actions("fam003-option-d-final-disabled")
        _pump(180)
        _record(
            steps,
            "hud-disable-hides-tray-doorway-settings-recoverable",
            not tray_entry.monitoring_hud_dashboard_action.isVisible() and dialog.isVisible(),
            {
                "state": window.monitoring_hud_feature_state(),
                "trayActionVisible": tray_entry.monitoring_hud_dashboard_action.isVisible(),
                "settingsVisible": dialog.isVisible(),
            },
        )
        add_capture(dialog, "16_global_settings_hud_disabled_recovery", "global-settings-native")

        for target in (recording, log_viewer, ai_dashboard, dialog):
            try:
                target.close()
            except RuntimeError:
                pass
        _wait_for(
            lambda: not current_surface_inventory("post-use-close-check")["onDemandVisible"],
            "all on-demand surfaces closed or hidden before post-use resident idle",
            10.0,
        )
        _pump(PERFORMANCE_SETTLE_DURATION_MS)
        metrics["postUseResidentIdle"] = _sustained_process_sample(
            "post-use-resident-idle",
            current_surface_inventory,
            expected_on_demand_visible=False,
        )
        _record(
            steps,
            "post-use-resident-idle-methodology",
            metrics["postUseResidentIdle"]["surfaceStateMatchesMethodology"]
            and metrics["postUseResidentIdle"]["sampleDurationMs"] >= PERFORMANCE_SAMPLE_DURATION_MS,
            {
                "onDemandVisible": metrics["postUseResidentIdle"]["surfaceInventoryAfter"]["onDemandVisible"],
                "sampleDurationMs": metrics["postUseResidentIdle"]["sampleDurationMs"],
            },
        )

        surfaces["global-settings-native"] = {
            "classification": "native-qt-shared-process-not-webengine",
            "visualVerdict": "PASS",
            "functionalVerdict": "PASS",
            "evidence": [str(evidence_root / "03_global_settings_hud_disabled.png"), str(evidence_root / "16_global_settings_hud_disabled_recovery.png")],
        }
        surfaces["ndai-command-prompt-native"] = {
            "classification": "native-qt-shared-process-not-webengine",
            "visualVerdict": "CURRENT_OPTION_C_CHILD_REQUIRED",
            "functionalVerdict": "CURRENT_OPTION_C_CHILD_REQUIRED",
        }
        surfaces["resident-tray-native"] = {
            "classification": "native-qt-shared-process-not-webengine",
            "visualVerdict": "CURRENT_OPTION_C_CHILD_REQUIRED",
            "functionalVerdict": "PASS",
            "routeEvidence": "Global Settings, AI Dashboard, and HUD Dashboard QAction routes exercised in this session",
        }

        for key, rect in original_geometries.items():
            target = {
                "hud-dashboard": window,
                "recording-suite": recording,
                "log-viewer": log_viewer,
                "ai-dashboard": ai_dashboard,
            }.get(key)
            if target is not None and rect.isValid():
                target.setGeometry(rect)
        for target in (recording, log_viewer, ai_dashboard, dialog):
            try:
                target.close()
            except Exception:
                pass
        _pump(220)
    except Exception as exc:
        failure = f"{type(exc).__name__}: {exc}"
        runtime_milestone(f"RENDERER_MAIN|FAM003_OPTION_D_WORKSTREAM_PROBE_FAILED|reason={type(exc).__name__}")
    finally:
        status = "PASS" if not failure and all(step.get("status") == "PASS" for step in steps) else "FAIL"
        payload = {
            "schema": "fam003-option-d-runtime-session-v1",
            "status": status,
            "failure": failure,
            "proofMode": "R2_WORKSTREAM_ONLY_NOT_H1_NOT_LV_NOT_UTS",
            "formalH1Entered": False,
            "formalLiveValidationEntered": False,
            "utsRequested": False,
            "normalLauncherProof": True,
            "validationOrchestrationOnly": True,
            "productRoutesExercised": [
                "tray Global Settings QAction",
                "Global Settings HUD Dashboard toggle",
                "tray HUD Dashboard QAction",
                "HUD Recording Suite DOM control",
                "Recording Suite Log Viewer DOM control",
                "tray AI Status / Command Center QAction",
            ],
            "sourceHead": os.environ.get(SOURCE_HEAD_ENV, ""),
            "sessionIndex": int(os.environ.get(SESSION_INDEX_ENV, "0") or 0),
            "runtimeLog": runtime_log_path,
            "startedAtEpoch": started_at,
            "finishedAtEpoch": time.time(),
            "effectiveBackend": {
                "parentFlags": os.environ.get("NEXUS_RENDERER_PARENT_QTWEBENGINE_CHROMIUM_FLAGS", ""),
                "effectiveFlags": os.environ.get("NEXUS_RENDERER_EFFECTIVE_QTWEBENGINE_CHROMIUM_FLAGS", ""),
                "childInheritedFlags": os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", ""),
                "policy": os.environ.get("NEXUS_RENDERER_BACKEND_POLICY", ""),
                "classification": os.environ.get("NEXUS_RENDERER_BACKEND_CLASSIFICATION", ""),
                "hardwareAccelerationDisabled": EXPECTED_FLAG in (os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS") or "").split(),
                "softwareCompositionActive": EXPECTED_FLAG in (os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS") or "").split(),
            },
            "javascriptCallbackPolicy": {
                "maxAttempts": JAVASCRIPT_CALLBACK_MAX_ATTEMPTS,
                "retryEvents": list(_JAVASCRIPT_RETRY_EVENTS),
                "exhausted": any(event.get("exhausted") for event in _JAVASCRIPT_RETRY_EVENTS),
            },
            "steps": steps,
            "surfaces": surfaces,
            "captures": captures,
            "metrics": metrics,
            "materialRegression": {
                "detected": True if status != "PASS" else None,
                "disposition": "REPAIR_REQUIRED" if status != "PASS" else "USER_DECISION_REQUIRED",
                "visualCorruption": any(not item.get("nonBlank") for item in captures),
                "unresponsiveInterval": bool(metrics.get("responsiveness", {}).get("unresponsiveIntervalOver1000Ms")),
                "requiredMetricsAdjudicated": bool(
                    metrics.get("startupTimeline")
                    and metrics.get("startupResidentIdle")
                    and metrics.get("representativeActive")
                    and metrics.get("postUseResidentIdle")
                    and metrics.get("surfaceTimelines")
                ),
                "baselineComparable": False,
                "thresholdSource": "no repo-defined quantitative threshold and no safe equivalent hardware-default baseline",
                "decisionReason": "absolute sustained measurements are auditable, but regression magnitude cannot be adjudicated without an equivalent safe baseline or a USER performance decision",
            },
        }
        try:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        finally:
            runtime_milestone(
                "RENDERER_MAIN|FAM003_OPTION_D_WORKSTREAM_PROBE_WRITTEN"
                f"|status={status}|manifest={manifest_path}|formal_lv=false"
            )
            QtCore.QTimer.singleShot(300, do_shutdown)


_ACTIVE_NONINTRUSIVE_CONTROLLER = None


def run_option_d_workstream_probe(
    *,
    window,
    core_window,
    tray_entry,
    runtime_log_path: str,
    do_shutdown: Callable[[], None],
    runtime_milestone: Callable[[str], None],
) -> None:
    """Start the nonblocking controller and return to the normal Qt event loop."""

    global _ACTIVE_NONINTRUSIVE_CONTROLLER
    from dev.fam003_option_d_performance_controller import (
        NonintrusivePerformanceController,
    )

    _ACTIVE_NONINTRUSIVE_CONTROLLER = NonintrusivePerformanceController(
        window=window,
        core_window=core_window,
        tray_entry=tray_entry,
        runtime_log_path=runtime_log_path,
        do_shutdown=do_shutdown,
        runtime_milestone=runtime_milestone,
    )
    _ACTIVE_NONINTRUSIVE_CONTROLLER.start()
