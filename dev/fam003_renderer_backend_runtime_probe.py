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
    result: dict[str, Any] = {"done": False, "value": None}

    def complete(value: Any) -> None:
        result["value"] = value
        result["done"] = True

    webview.page().runJavaScript(script, complete)
    _wait_for(lambda: bool(result["done"]), "JavaScript callback", timeout_s)
    value = result["value"]
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


def _process_snapshot(label: str, sample_ms: int = 650) -> dict[str, Any]:
    root = psutil.Process(os.getpid())
    processes = [root, *root.children(recursive=True)]
    for process in processes:
        try:
            process.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _pump(sample_ms)
    cpu = 0.0
    rss = 0
    alive = []
    for process in processes:
        try:
            cpu += process.cpu_percent(None)
            memory = process.memory_info().rss
            rss += memory
            alive.append({"pid": process.pid, "name": process.name(), "rssBytes": memory})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    chromium_children = [row for row in alive if "QtWebEngineProcess" in row["name"]]
    return {
        "label": label,
        "sampleDurationMs": sample_ms,
        "processCount": len(alive),
        "webEngineSubprocessCount": len(chromium_children),
        "cpuPercentSum": round(cpu, 2),
        "rssBytes": rss,
        "rssMiB": round(rss / (1024 * 1024), 2),
        "processes": alive,
    }


def _responsiveness_sample(webviews: list[Any], duration_ms: int = 900) -> dict[str, Any]:
    gaps: list[float] = []
    start = time.perf_counter()
    previous = start
    iteration = 0
    while (time.perf_counter() - start) * 1000.0 < duration_ms:
        QApplication.processEvents()
        now = time.perf_counter()
        gaps.append((now - previous) * 1000.0)
        previous = now
        if webviews and iteration % 6 == 0:
            view = webviews[(iteration // 6) % len(webviews)]
            view.page().runJavaScript("window.scrollBy(0, 8); window.scrollBy(0, -8);")
        iteration += 1
        time.sleep(0.012)
    ordered = sorted(gaps)
    p95_index = min(len(ordered) - 1, max(0, int(len(ordered) * 0.95)))
    return {
        "durationMs": round((time.perf_counter() - start) * 1000.0, 2),
        "iterationCount": len(gaps),
        "medianDispatchGapMs": round(statistics.median(gaps), 3) if gaps else 0.0,
        "p95DispatchGapMs": round(ordered[p95_index], 3) if ordered else 0.0,
        "maxDispatchGapMs": round(max(gaps), 3) if gaps else 0.0,
        "unresponsiveIntervalOver1000Ms": any(gap > 1000.0 for gap in gaps),
    }


def _record(steps: list[dict[str, Any]], step_id: str, passed: bool, detail: Any) -> None:
    steps.append({"id": step_id, "status": "PASS" if passed else "FAIL", "detail": detail})
    if not passed:
        raise ProbeFailure(f"{step_id} failed: {detail}")


def run_option_d_workstream_probe(
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

    def add_capture(widget, label: str, surface_id: str) -> dict[str, Any]:
        result = _capture(widget, evidence_root, label, surface_id)
        captures.append(result)
        return result

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
        metrics["startupReadyMs"] = round((time.time_ns() - launch_started_ns) / 1_000_000, 2) if launch_started_ns else None
        metrics["rendererReadyMs"] = metrics["startupReadyMs"]
        metrics["machine"] = {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "qt": QtCore.qVersion(),
            "logicalCpuCount": psutil.cpu_count(logical=True),
            "physicalMemoryGiB": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        }

        _wait_for(lambda: bool(core_window.is_core_visualization_ready()), "ORIN Core ready")
        core_capture_started = time.perf_counter()
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
        metrics["firstWebEngineRenderMs"] = round((time.perf_counter() - core_capture_started) * 1000.0, 2)

        tray_entry.global_settings_action.trigger()
        settings_open_ms = _wait_for(
            lambda: bool(getattr(window, "_resident_access_settings_dialog", None) and window._resident_access_settings_dialog.isVisible()),
            "Global Settings from tray",
        )
        dialog = window._resident_access_settings_dialog
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
        metrics["surfaceOpenMs"] = {"recordingSuite": round((time.perf_counter() - recording_open_started) * 1000.0, 2)}
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
        metrics["surfaceOpenMs"]["logViewer"] = round((time.perf_counter() - log_open_started) * 1000.0, 2)
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
        recording_restore = add_capture(recording, "10_nexus-recording-suite_restored", "nexus-recording-suite")
        surfaces["nexus-recording-suite"]["evidence"].append(recording_restore["path"])

        _dom_click(log_viewer.webview, "#monitoring-hud-studio-close-action")
        _wait_for(lambda: not log_viewer.isVisible(), "Log Viewer close")
        _dom_click(window.webview, "#monitoring-hud-recording-open-folder")
        _wait_for(lambda: log_viewer.isVisible(), "Log Viewer reopen from HUD")
        log_reopen = add_capture(log_viewer, "11_nexus-log-viewer_reopened", "nexus-log-viewer")
        surfaces["nexus-log-viewer"]["evidence"].append(log_reopen["path"])

        ai_open_started = time.perf_counter()
        tray_entry.ai_status_action.trigger()
        _wait_for(
            lambda: bool(getattr(window, "_ai_control_center_dialog", None) and window._ai_control_center_dialog.isVisible()),
            "AI Dashboard from tray",
        )
        ai_dashboard = window._ai_control_center_dialog
        _wait_for(lambda: bool(ai_dashboard._page_ready), "AI Dashboard WebEngine ready")
        metrics["surfaceOpenMs"]["aiDashboard"] = round((time.perf_counter() - ai_open_started) * 1000.0, 2)
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
        ai_restore = add_capture(ai_dashboard, "14_ai-status-command-center_restored", "ai-status-command-center")
        surfaces["ai-status-command-center"]["evidence"].append(ai_restore["path"])
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
        tray_entry.monitoring_hud_dashboard_action.trigger()
        _pump(220)
        _record(
            steps,
            "hud-repeated-open-is-idempotent",
            window.isVisible() and bool(window.monitoring_hud_feature_state().get("dashboard_visible")),
            window.monitoring_hud_feature_state(),
        )
        hud_restore = add_capture(window, "15_hud-dashboard_tray_restored", "hud-dashboard")
        surfaces["hud-dashboard"]["evidence"].append(hud_restore["path"])

        active_webviews = [core_window.webview, window.webview, recording.webview, log_viewer.webview, ai_dashboard.webview]
        metrics["activeProcess"] = _process_snapshot("representative-active", 700)
        metrics["responsiveness"] = _responsiveness_sample(active_webviews)
        _pump(500)
        metrics["idleProcess"] = _process_snapshot("settled-idle", 900)
        _record(
            steps,
            "responsiveness-no-freeze",
            not metrics["responsiveness"]["unresponsiveIntervalOver1000Ms"],
            metrics["responsiveness"],
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
            "steps": steps,
            "surfaces": surfaces,
            "captures": captures,
            "metrics": metrics,
            "materialRegression": {
                "detected": status != "PASS",
                "visualCorruption": any(not item.get("nonBlank") for item in captures),
                "unresponsiveInterval": bool(metrics.get("responsiveness", {}).get("unresponsiveIntervalOver1000Ms")),
                "thresholdSource": "no repo-defined quantitative threshold; measured evidence is preserved for USER review",
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
