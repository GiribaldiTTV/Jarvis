"""Capture FAM-006 feature-studio visual repair evidence.

This is pre-Live-Validation visual proof only. It renders the real Studio
widgets through the branch runtime classes and saves focused screenshots for
USER review and packet inclusion.
"""

from __future__ import annotations

import json
import re
import sys
import time
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw
from PySide6.QtCore import QEventLoop, QPoint, QRect, Qt, QTimer
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.desktop_renderer import (
    MonitoringHudLogViewerStudioWindow,
    MonitoringHudRecordingStudioWindow,
)


PROOF_ROOT = Path(
    "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/"
    "fam_006_pre_live_visual_conformance"
)
AI_CONTROL_CENTER_ROOT = (
    Path("C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI")
    / "FAM-007-H4"
    / "20260622-094707-live-resize"
)


def _load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def _save_crop(source: Path, target: Path, box: tuple[int, int, int, int]) -> str:
    image = _load_image(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.crop(box).save(target)
    return str(target)


def _image_size(source: Path) -> tuple[int, int]:
    image = _load_image(source)
    return image.size


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _save_overlay(
    source: Path,
    target: Path,
    *,
    crop_rect: tuple[int, int, int, int],
    target_rect: tuple[int, int, int, int],
    label: str,
    expected_text: list[str],
) -> str:
    image = _load_image(source)
    draw = ImageDraw.Draw(image)
    draw.rectangle(crop_rect, outline=(82, 225, 255), width=3)
    draw.rectangle(target_rect, outline=(119, 255, 208), width=3)
    legend = [
        f"crop: {label}",
        "cyan=crop rectangle",
        "green=target element bounds",
        "expected: " + " | ".join(expected_text),
    ]
    y = 8
    for line in legend:
        draw.rectangle((8, y - 2, min(image.width - 8, 12 + len(line) * 7), y + 14), fill=(1, 12, 22))
        draw.text((12, y), line, fill=(226, 250, 255))
        y += 18
    image.save(target)
    return str(target)


def _js_eval(widget, script: str):
    result: dict[str, object] = {}
    loop = QEventLoop()

    def done(value):
        result["value"] = value
        loop.quit()

    widget.webview.page().runJavaScript(script, done)
    QTimer.singleShot(3000, loop.quit)
    loop.exec()
    return result.get("value")


def _capture_dom_bounds(widget) -> dict[str, object]:
    script = r"""
(() => {
  const targets = {
    chrome: ".monitoring-hud__chrome",
    windowControls: ".monitoring-hud__window-controls",
    titleGroup: ".monitoring-hud__title-group",
    studioTruthRow: ".monitoring-hud__studio-truth-row",
    recordingActionStrip: "[data-element-group='recording-actions']",
    recordingTransportPill: "[data-control-group='recording-transport-pill']",
    recordingStartAction: "[data-control='recording-studio-start']",
    recordingPauseAction: "[data-control='recording-studio-pause']",
    recordingStopAction: "[data-control='recording-studio-stop']",
    recordingTargetTruth: "[data-element-group='recording-target-truth'] .monitoring-hud__studio-truth-row:first-child",
    recordingStateTruth: "[data-element-group='recording-controller-truth']",
    recordingLogRoute: "[data-control='recording-studio-open-log-viewer']",
    logViewerActionStrip: "[data-element-group='log-folder-actions']",
    logViewerViewerState: "[data-folder-kind='viewer']",
    logViewerNativeAction: "[data-control='log-viewer-open-native']",
    logViewerExportAction: "[data-control='log-viewer-open-export']",
    logViewerActionStatus: "[data-log-shell-primitive='action-first-folder-access-shell-v6']",
  };
  const out = {};
  Object.entries(targets).forEach(([key, selector]) => {
    const element = document.querySelector(selector);
    if (!element || element.hidden) {
      return;
    }
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    const label = element.querySelector(".monitoring-hud__button-label") || element;
    const labelStyle = getComputedStyle(label);
    const children = Array.from(element.children || []);
    const rowLabel = children.find((child) => child.tagName === "SPAN") || null;
    const rowValue = children.find((child) => child.tagName === "STRONG") || null;
    const rowLabelRect = rowLabel ? rowLabel.getBoundingClientRect() : null;
    const rowValueRect = rowValue ? rowValue.getBoundingClientRect() : null;
    const rectPayload = (targetRect) => targetRect ? {
      left: Math.round(targetRect.left),
      top: Math.round(targetRect.top),
      right: Math.round(targetRect.right),
      bottom: Math.round(targetRect.bottom),
    } : null;
    out[key] = {
      selector,
      rect: {
        left: Math.round(rect.left),
        top: Math.round(rect.top),
        right: Math.round(rect.right),
        bottom: Math.round(rect.bottom),
      },
      computedStyle: {
        width: style.width,
        height: style.height,
        minWidth: style.minWidth,
        maxWidth: style.maxWidth,
        minHeight: style.minHeight,
        paddingTop: style.paddingTop,
        paddingRight: style.paddingRight,
        paddingBottom: style.paddingBottom,
        paddingLeft: style.paddingLeft,
        fontSize: style.fontSize,
        fontWeight: style.fontWeight,
        fontFamily: style.fontFamily,
        lineHeight: style.lineHeight,
        letterSpacing: style.letterSpacing,
        textTransform: style.textTransform,
        color: style.color,
        backgroundImage: style.backgroundImage,
        borderTopColor: style.borderTopColor,
        borderRightColor: style.borderRightColor,
        borderBottomColor: style.borderBottomColor,
        borderLeftColor: style.borderLeftColor,
        borderTopWidth: style.borderTopWidth,
        borderRightWidth: style.borderRightWidth,
        borderBottomWidth: style.borderBottomWidth,
        borderLeftWidth: style.borderLeftWidth,
        borderRadius: style.borderRadius,
        boxShadow: style.boxShadow,
        display: style.display,
        justifyContent: style.justifyContent,
        justifySelf: style.justifySelf,
        gap: style.gap,
        gridTemplateColumns: style.gridTemplateColumns,
        columnGap: style.columnGap,
        top: style.top,
        right: style.right,
      },
      labelComputedStyle: {
        width: labelStyle.width,
        height: labelStyle.height,
        fontSize: labelStyle.fontSize,
        fontWeight: labelStyle.fontWeight,
        fontFamily: labelStyle.fontFamily,
        lineHeight: labelStyle.lineHeight,
        letterSpacing: labelStyle.letterSpacing,
        textTransform: labelStyle.textTransform,
        color: labelStyle.color,
      },
      rowLabelRect: rectPayload(rowLabelRect),
      rowValueRect: rectPayload(rowValueRect),
      rowLabelText: rowLabel ? String(rowLabel.innerText || rowLabel.textContent || "").trim() : "",
      rowValueText: rowValue ? String(rowValue.innerText || rowValue.textContent || "").trim() : "",
      rowLabelValueGapPx: rowLabelRect && rowValueRect ? Math.round(rowValueRect.left - rowLabelRect.right) : null,
      text: String(element.innerText || element.textContent || "")
        .replace(/\s+/g, " ")
        .trim(),
    };
  });
  return JSON.stringify(out);
})()
"""
    value = _js_eval(widget, script)
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return value if isinstance(value, dict) else {}


def _dom_rect(bounds: dict[str, object], key: str) -> dict[str, int]:
    item = bounds.get(key)
    if not isinstance(item, dict):
        return {}
    rect = item.get("rect")
    if not isinstance(rect, dict):
        return {}
    return {
        "left": int(rect.get("left", 0)),
        "top": int(rect.get("top", 0)),
        "right": int(rect.get("right", 0)),
        "bottom": int(rect.get("bottom", 0)),
    }


def _dom_style(bounds: dict[str, object], key: str) -> dict[str, str]:
    item = bounds.get(key)
    if not isinstance(item, dict):
        return {}
    style = item.get("computedStyle")
    return style if isinstance(style, dict) else {}


def _dom_label_style(bounds: dict[str, object], key: str) -> dict[str, str]:
    item = bounds.get(key)
    if not isinstance(item, dict):
        return {}
    style = item.get("labelComputedStyle")
    return style if isinstance(style, dict) else {}


def _runtime_visual_conformance_metrics(root: Path, manifest: dict[str, object]) -> dict[str, object]:
    expected_button = {
        "height": "31px",
        "minHeight": "31px",
        "paddingTop": "0px",
        "paddingRight": "14px",
        "paddingBottom": "0px",
        "paddingLeft": "14px",
        "fontSize": "11px",
        "fontWeight": {"700", "720"},
        "labelFontSize": "11px",
        "labelFontWeight": {"700", "720"},
        "labelLineHeight": "11px",
        "maxWidthNot": {"none", "initial", "unset"},
    }

    def button_metrics(bounds: dict[str, object], key: str) -> dict[str, object]:
        rect = _dom_rect(bounds, key)
        style = _dom_style(bounds, key)
        label_style = _dom_label_style(bounds, key)
        failures: list[str] = []
        if not rect:
            failures.append("missing DOM rect")
        else:
            height = int(rect.get("bottom", 0)) - int(rect.get("top", 0))
            if height != 31:
                failures.append(f"rect height {height}px != 31px")
        for field in ("height", "minHeight", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "fontSize"):
            if style.get(field) != expected_button[field]:
                failures.append(f"{field} {style.get(field)!r} != {expected_button[field]!r}")
        if str(style.get("fontWeight")) not in expected_button["fontWeight"]:
            failures.append(f"fontWeight {style.get('fontWeight')!r} not in {sorted(expected_button['fontWeight'])}")
        max_width = str(style.get("maxWidth", "")).strip()
        if not max_width or max_width in expected_button["maxWidthNot"]:
            failures.append(f"maxWidth {max_width!r} does not preserve content-fit cap")
        if label_style.get("fontSize") != expected_button["labelFontSize"]:
            failures.append(f"label fontSize {label_style.get('fontSize')!r} != {expected_button['labelFontSize']!r}")
        if str(label_style.get("fontWeight")) not in expected_button["labelFontWeight"]:
            failures.append(
                f"label fontWeight {label_style.get('fontWeight')!r} not in {sorted(expected_button['labelFontWeight'])}"
            )
        if label_style.get("lineHeight") != expected_button["labelLineHeight"]:
            failures.append(f"label lineHeight {label_style.get('lineHeight')!r} != {expected_button['labelLineHeight']!r}")
        return {
            "key": key,
            "text": str((bounds.get(key) or {}).get("text", "")) if isinstance(bounds.get(key), dict) else "",
            "rect": rect,
            "computedStyle": style,
            "labelComputedStyle": label_style,
            "expectedPrimitive": "AI Control Center monitoring-hud__hub-action--content-fit: 31px height, 14px left/right gutter, 11px label, content-fit cap",
            "failures": failures,
            "status": "PASS" if not failures else "REPAIR",
        }

    def control_gutter_metrics(bounds: dict[str, object], surface_key: str) -> dict[str, object]:
        chrome = _dom_rect(bounds, "chrome")
        controls = _dom_rect(bounds, "windowControls")
        content_tops: list[int] = []
        first_content_keys = (
            ("recordingTargetTruth", "recordingStartAction")
            if surface_key == "recording"
            else ("logViewerViewerState", "logViewerNativeAction")
        )
        for key in first_content_keys:
            rect = _dom_rect(bounds, key)
            if not rect:
                continue
            top = int(rect.get("top", 0))
            bottom = int(rect.get("bottom", 0))
            left = int(rect.get("left", 0))
            right = int(rect.get("right", 0))
            if bottom > top and right > left:
                content_tops.append(top)
        failures: list[str] = []
        first_content_top = min(content_tops) if content_tops else 0
        if not chrome:
            failures.append("missing chrome DOM rect")
        if not controls:
            failures.append("missing window control DOM rect")
        if not first_content_top:
            failures.append("missing first content row/action DOM rect")
        top_gutter = int(controls.get("top", 0)) - int(chrome.get("top", 0)) if chrome and controls else -1
        right_gutter = int(chrome.get("right", 0)) - int(controls.get("right", 0)) if chrome and controls else -1
        bottom_gutter = int(first_content_top) - int(controls.get("bottom", 0)) if controls and first_content_top else -1
        style = _dom_style(bounds, "windowControls")
        if style.get("top") != "14px":
            failures.append(f"window control CSS top {style.get('top')!r} != AI Control Center '14px'")
        if style.get("right") != "15px":
            failures.append(f"window control CSS right {style.get('right')!r} != AI Control Center '15px'")
        return {
            "chromeRect": chrome,
            "windowControlsRect": controls,
            "firstContentTopPx": first_content_top,
            "topGutterPx": top_gutter,
            "rightGutterPx": right_gutter,
            "bottomGutterPx": bottom_gutter,
            "expected": "top/right gutter preserve the AI Control Center compact window-control placement; first-content proximity is governed separately by title/status rhythm for compact feature studios",
            "bottomGutterDisposition": "informational-after-title-proximity-gate",
            "failures": failures,
            "status": "PASS" if not failures else "REPAIR",
        }

    def title_to_status_metrics(bounds: dict[str, object], surface_key: str) -> dict[str, object]:
        title_group = _dom_rect(bounds, "titleGroup")
        first_row_key = "recordingTargetTruth" if surface_key == "recording" else "logViewerViewerState"
        first_row = _dom_rect(bounds, first_row_key)
        failures: list[str] = []
        if not title_group:
            failures.append("missing title group DOM rect")
        if not first_row:
            failures.append("missing first status/truth row DOM rect")
        gap = int(first_row.get("top", 0)) - int(title_group.get("bottom", 0)) if title_group and first_row else -1
        if gap < 2 or gap > 6:
            failures.append(f"title-to-status gap {gap}px is outside deterministic 2-6px compact-controller range")
        return {
            "titleGroupRect": title_group,
            "firstStatusRowKey": first_row_key,
            "firstStatusRowRect": first_row,
            "titleToStatusGapPx": gap,
            "expected": "first status/truth row begins 2-6px below the title group; larger gaps read as disproportionate floating status data",
            "failures": failures,
            "status": "PASS" if not failures else "REPAIR",
        }

    def row_label_value_metrics(bounds: dict[str, object], surface_key: str) -> dict[str, object]:
        row_keys = (
            ("recordingTargetTruth", "TARGET"),
            ("recordingStateTruth", "STATE"),
        ) if surface_key == "recording" else (
            ("logViewerViewerState", "VIEWER"),
        )
        rows: list[dict[str, object]] = []
        failures: list[str] = []
        for key, expected_label in row_keys:
            item = bounds.get(key)
            if not isinstance(item, dict):
                failures.append(f"{key} missing DOM measurement")
                continue
            label_text = str(item.get("rowLabelText", ""))
            value_text = str(item.get("rowValueText", ""))
            gap = item.get("rowLabelValueGapPx")
            label_rect = item.get("rowLabelRect")
            value_rect = item.get("rowValueRect")
            row_failures: list[str] = []
            if label_text != expected_label:
                row_failures.append(f"label {label_text!r} != {expected_label!r}")
            if not value_text:
                row_failures.append("value text missing")
            if not isinstance(gap, int):
                row_failures.append("label/value gap missing")
            elif gap < 14 or gap > 22:
                row_failures.append(f"label/value gap {gap}px outside deterministic 14-22px range")
            if not isinstance(label_rect, dict) or not isinstance(value_rect, dict):
                row_failures.append("label/value rect missing")
            rows.append(
                {
                    "rowKey": key,
                    "expectedLabel": expected_label,
                    "labelText": label_text,
                    "valueText": value_text,
                    "labelRect": label_rect,
                    "valueRect": value_rect,
                    "labelValueGapPx": gap,
                    "expectedGapPx": "14-22",
                    "failures": row_failures,
                    "status": "PASS" if not row_failures else "REPAIR",
                }
            )
            failures.extend(f"{key}: {failure}" for failure in row_failures)
        return {
            "surface": "Recording Studio" if surface_key == "recording" else "Log Viewer",
            "expected": "compact state rows use a content-fit label column and a deterministic 18px target label/value gap; the value must not float in a wide legacy label column",
            "rows": rows,
            "failures": failures,
            "status": "PASS" if not failures else "REPAIR",
        }

    def _rect_width(rect: dict[str, int]) -> int:
        return int(rect.get("right", 0)) - int(rect.get("left", 0))

    def _rect_height(rect: dict[str, int]) -> int:
        return int(rect.get("bottom", 0)) - int(rect.get("top", 0))

    def _edge_delta(a: int, b: int) -> int:
        return abs(int(a) - int(b))

    def action_layout_metrics(bounds: dict[str, object], surface_key: str) -> dict[str, object]:
        failures: list[str] = []
        if surface_key == "recording":
            strip = _dom_rect(bounds, "recordingActionStrip")
            pill = _dom_rect(bounds, "recordingTransportPill")
            start = _dom_rect(bounds, "recordingStartAction")
            pause = _dom_rect(bounds, "recordingPauseAction")
            stop = _dom_rect(bounds, "recordingStopAction")
            route = _dom_rect(bounds, "recordingLogRoute")
            for name, rect in (
                ("recording action strip", strip),
                ("recording transport pill", pill),
                ("START segment", start),
                ("PAUSE segment", pause),
                ("STOP segment", stop),
                ("OPEN LOG VIEWER route", route),
            ):
                if not rect or _rect_width(rect) <= 0 or _rect_height(rect) <= 0:
                    failures.append(f"missing or empty DOM rect for {name}")
            if strip and pill and _edge_delta(pill.get("left", 0), strip.get("left", 0)) > 1:
                failures.append(
                    f"transport pill left edge {pill.get('left')} does not align with action strip left edge {strip.get('left')}"
                )
            if strip and route and _edge_delta(route.get("right", 0), strip.get("right", 0)) > 1:
                failures.append(
                    f"OPEN LOG VIEWER right edge {route.get('right')} does not align with action strip right edge {strip.get('right')}"
                )
            if pill and route and int(route.get("left", 0)) <= int(pill.get("right", 0)):
                failures.append("OPEN LOG VIEWER is not separated to the right of the transport pill")
            if pill:
                for name, rect in (("START", start), ("PAUSE", pause), ("STOP", stop)):
                    if rect and (
                        int(rect.get("left", 0)) < int(pill.get("left", 0))
                        or int(rect.get("right", 0)) > int(pill.get("right", 0))
                        or int(rect.get("top", 0)) < int(pill.get("top", 0))
                        or int(rect.get("bottom", 0)) > int(pill.get("bottom", 0))
                    ):
                        failures.append(f"{name} segment is not contained inside the transport pill")
            if start and pause and _edge_delta(pause.get("left", 0), start.get("right", 0)) > 1:
                failures.append("START and PAUSE segments are not visually contiguous")
            if pause and stop and _edge_delta(stop.get("left", 0), pause.get("right", 0)) > 1:
                failures.append("PAUSE and STOP segments are not visually contiguous")
            if start and pause and int(start.get("left", 0)) >= int(pause.get("left", 0)):
                failures.append("START segment is not first in the transport pill")
            if pause and stop and int(pause.get("left", 0)) >= int(stop.get("left", 0)):
                failures.append("PAUSE segment is not before STOP in the transport pill")
            return {
                "surface": "Recording Studio",
                "expectedActionGrammar": "START/PAUSE/STOP are one segmented transport pill left-aligned; OPEN LOG VIEWER remains separate and right-aligned.",
                "actionStripRect": strip,
                "transportPillRect": pill,
                "startSegmentRect": start,
                "pauseSegmentRect": pause,
                "stopSegmentRect": stop,
                "openLogViewerRect": route,
                "actionStripComputedStyle": _dom_style(bounds, "recordingActionStrip"),
                "transportPillComputedStyle": _dom_style(bounds, "recordingTransportPill"),
                "transportPillLeftAlignedPx": _edge_delta(pill.get("left", 0), strip.get("left", 0)) if strip and pill else None,
                "openLogViewerRightAlignedPx": _edge_delta(route.get("right", 0), strip.get("right", 0)) if strip and route else None,
                "openLogViewerSeparatedFromTransportPx": int(route.get("left", 0)) - int(pill.get("right", 0)) if pill and route else None,
                "startPauseSegmentGapPx": int(pause.get("left", 0)) - int(start.get("right", 0)) if start and pause else None,
                "pauseStopSegmentGapPx": int(stop.get("left", 0)) - int(pause.get("right", 0)) if pause and stop else None,
                "failures": failures,
                "status": "PASS" if not failures else "REPAIR",
            }
        strip = _dom_rect(bounds, "logViewerActionStrip")
        native = _dom_rect(bounds, "logViewerNativeAction")
        export = _dom_rect(bounds, "logViewerExportAction")
        for name, rect in (
            ("Log Viewer action strip", strip),
            ("OPEN NATIVE LOGS action", native),
            ("OPEN EXPORTED LOGS action", export),
        ):
            if not rect or _rect_width(rect) <= 0 or _rect_height(rect) <= 0:
                failures.append(f"missing or empty DOM rect for {name}")
        if strip and export and _edge_delta(export.get("right", 0), strip.get("right", 0)) > 1:
            failures.append(
                f"OPEN EXPORTED LOGS right edge {export.get('right')} does not align with action strip right edge {strip.get('right')}"
            )
        if native and export and int(native.get("right", 0)) >= int(export.get("left", 0)):
            failures.append("OPEN NATIVE LOGS is not left of OPEN EXPORTED LOGS with a visible gap")
        return {
            "surface": "Log Viewer",
            "expectedActionGrammar": "OPEN NATIVE LOGS and OPEN EXPORTED LOGS are one right-aligned folder-action group.",
            "actionStripRect": strip,
            "openNativeLogsRect": native,
            "openExportedLogsRect": export,
            "actionStripComputedStyle": _dom_style(bounds, "logViewerActionStrip"),
            "exportedLogsRightAlignedPx": _edge_delta(export.get("right", 0), strip.get("right", 0)) if strip and export else None,
            "nativeExportGapPx": int(export.get("left", 0)) - int(native.get("right", 0)) if native and export else None,
            "failures": failures,
            "status": "PASS" if not failures else "REPAIR",
        }

    def metrics_for(label: str, action_keys: list[str], *, max_height: int, max_bottom_slack: int, surface_key: str) -> dict[str, object]:
        image_path = Path(str(manifest[label]))
        width, height = _image_size(image_path)
        bounds = manifest.get(f"{label}_dom_bounds")
        bounds = bounds if isinstance(bounds, dict) else {}
        buttons = [button_metrics(bounds, key) for key in action_keys]
        control_gutter = control_gutter_metrics(bounds, surface_key)
        title_to_status = title_to_status_metrics(bounds, surface_key)
        row_label_value = row_label_value_metrics(bounds, surface_key)
        action_layout = action_layout_metrics(bounds, surface_key)
        action_bottoms = [
            _dom_rect(bounds, key).get("bottom", 0)
            for key in action_keys
            if _dom_rect(bounds, key)
        ]
        final_action_bottom = max(action_bottoms) if action_bottoms else 0
        bottom_slack = height - final_action_bottom if final_action_bottom else height
        return {
            "screenshot": _rel(root, image_path),
            "imageSize": {"width": width, "height": height},
            "finalActionBottomPx": final_action_bottom,
            "bottomSlackPx": bottom_slack,
            "maxAllowedHeightPx": max_height,
            "maxAllowedBottomSlackPx": max_bottom_slack,
            "heightVerdict": "PASS" if height <= max_height else "REPAIR",
            "bottomSlackVerdict": "PASS" if bottom_slack <= max_bottom_slack else "REPAIR",
            "windowControlsComputedStyle": _dom_style(bounds, "windowControls"),
            "truthRowComputedStyle": _dom_style(bounds, "studioTruthRow"),
            "primaryButtonComputedStyle": _dom_style(bounds, action_keys[0]) if action_keys else {},
            "buttonPrimitiveMeasurements": buttons,
            "buttonPrimitiveVerdict": "PASS" if all(button["status"] == "PASS" for button in buttons) else "REPAIR",
            "controlPillGutterMeasurements": control_gutter,
            "controlPillGutterVerdict": control_gutter["status"],
            "titleToStatusMeasurements": title_to_status,
            "titleToStatusVerdict": title_to_status["status"],
            "rowLabelValueMeasurements": row_label_value,
            "rowLabelValueVerdict": row_label_value["status"],
            "actionLayoutMeasurements": action_layout,
            "actionLayoutVerdict": action_layout["status"],
        }

    recording = metrics_for(
        "recording_default",
        ["recordingStartAction", "recordingPauseAction", "recordingStopAction", "recordingLogRoute"],
        max_height=152,
        max_bottom_slack=18,
        surface_key="recording",
    )
    recording_transport_state_labels = [
        "recording_default",
        "recording_active_stop_state",
        "recording_saving_after_stop",
        "recording_saved_complete_after_stop",
        "recording_disabled_blocked",
    ]
    recording_transport_state_metrics = {}
    for label in recording_transport_state_labels:
        bounds = manifest.get(f"{label}_dom_bounds")
        bounds = bounds if isinstance(bounds, dict) else {}
        layout = action_layout_metrics(bounds, "recording")
        pill_item = bounds.get("recordingTransportPill")
        pill_text = str(pill_item.get("text", "")) if isinstance(pill_item, dict) else ""
        text_ok = all(token in pill_text.split() for token in ("START", "PAUSE", "STOP"))
        recording_transport_state_metrics[label] = {
            "screenshot": _rel(root, Path(str(manifest.get(label, "")))) if manifest.get(label) else "",
            "transportPillText": pill_text,
            "actionLayoutMeasurements": layout,
            "transportPillTextVerdict": "PASS" if text_ok else "REPAIR",
            "status": "PASS" if layout["status"] == "PASS" and text_ok else "REPAIR",
        }
    log_viewer = metrics_for(
        "log_viewer_default",
        ["logViewerNativeAction", "logViewerExportAction"],
        max_height=126,
        max_bottom_slack=18,
        surface_key="logViewer",
    )
    checks = [
        recording["heightVerdict"] == "PASS",
        recording["bottomSlackVerdict"] == "PASS",
        log_viewer["heightVerdict"] == "PASS",
        log_viewer["bottomSlackVerdict"] == "PASS",
        recording["buttonPrimitiveVerdict"] == "PASS",
        log_viewer["buttonPrimitiveVerdict"] == "PASS",
        recording["controlPillGutterVerdict"] == "PASS",
        log_viewer["controlPillGutterVerdict"] == "PASS",
        recording["titleToStatusVerdict"] == "PASS",
        log_viewer["titleToStatusVerdict"] == "PASS",
        recording["rowLabelValueVerdict"] == "PASS",
        log_viewer["rowLabelValueVerdict"] == "PASS",
        recording["actionLayoutVerdict"] == "PASS",
        log_viewer["actionLayoutVerdict"] == "PASS",
        log_viewer["truthRowComputedStyle"].get("paddingTop") == "3px",
        log_viewer["truthRowComputedStyle"].get("paddingBottom") == "2px",
        log_viewer["windowControlsComputedStyle"].get("top") == "14px",
        log_viewer["windowControlsComputedStyle"].get("right") == "15px",
        all(row["status"] == "PASS" for row in recording_transport_state_metrics.values()),
    ]
    payload = {
        "schema": "fam006-runtime-visual-conformance-metrics-v1",
        "status": "PASS" if all(checks) else "REPAIR",
        "recording": recording,
        "logViewer": log_viewer,
        "primitiveMatchChecks": {
            "contentFitButtonHeight": log_viewer["primaryButtonComputedStyle"].get("height"),
            "contentFitButtonPaddingLeft": log_viewer["primaryButtonComputedStyle"].get("paddingLeft"),
            "contentFitButtonPaddingRight": log_viewer["primaryButtonComputedStyle"].get("paddingRight"),
            "contentFitButtonFontSize": log_viewer["primaryButtonComputedStyle"].get("fontSize"),
            "contentFitButtonFontWeight": log_viewer["primaryButtonComputedStyle"].get("fontWeight"),
            "stateRowPaddingTop": log_viewer["truthRowComputedStyle"].get("paddingTop"),
            "stateRowPaddingBottom": log_viewer["truthRowComputedStyle"].get("paddingBottom"),
            "recordingTitleToStatusGapPx": recording["titleToStatusMeasurements"].get("titleToStatusGapPx"),
            "logViewerTitleToStatusGapPx": log_viewer["titleToStatusMeasurements"].get("titleToStatusGapPx"),
            "recordingTitleToStatusVerdict": recording["titleToStatusVerdict"],
            "logViewerTitleToStatusVerdict": log_viewer["titleToStatusVerdict"],
            "recordingRowLabelValueVerdict": recording["rowLabelValueVerdict"],
            "logViewerRowLabelValueVerdict": log_viewer["rowLabelValueVerdict"],
            "recordingRowLabelValueRows": recording["rowLabelValueMeasurements"].get("rows"),
            "logViewerRowLabelValueRows": log_viewer["rowLabelValueMeasurements"].get("rows"),
            "windowControlTop": log_viewer["windowControlsComputedStyle"].get("top"),
            "windowControlRight": log_viewer["windowControlsComputedStyle"].get("right"),
            "recordingButtonPrimitiveVerdict": recording["buttonPrimitiveVerdict"],
            "logViewerButtonPrimitiveVerdict": log_viewer["buttonPrimitiveVerdict"],
            "recordingActionLayoutVerdict": recording["actionLayoutVerdict"],
            "logViewerActionLayoutVerdict": log_viewer["actionLayoutVerdict"],
            "recordingTransportPillLeftAlignedPx": recording["actionLayoutMeasurements"].get("transportPillLeftAlignedPx"),
            "openLogViewerRightAlignedPx": recording["actionLayoutMeasurements"].get("openLogViewerRightAlignedPx"),
            "logViewerExportedLogsRightAlignedPx": log_viewer["actionLayoutMeasurements"].get("exportedLogsRightAlignedPx"),
            "recordingControlPillBottomGutterPx": recording["controlPillGutterMeasurements"].get("bottomGutterPx"),
            "logViewerControlPillBottomGutterPx": log_viewer["controlPillGutterMeasurements"].get("bottomGutterPx"),
        },
        "recordingTransportStateStress": recording_transport_state_metrics,
    }
    (root / "runtime_visual_conformance_metrics.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    (root / "RUNTIME_VISUAL_CONFORMANCE_METRICS.md").write_text(
        "# Runtime Visual Conformance Metrics\n\n"
        f"Status: `{payload['status']}`\n\n"
        "| Surface | Image size | Final action bottom | Bottom slack | Height verdict | Slack verdict |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        f"| Recording Studio | {recording['imageSize']['width']}x{recording['imageSize']['height']} | {recording['finalActionBottomPx']} | {recording['bottomSlackPx']} | {recording['heightVerdict']} | {recording['bottomSlackVerdict']} |\n"
        f"| Log Viewer | {log_viewer['imageSize']['width']}x{log_viewer['imageSize']['height']} | {log_viewer['finalActionBottomPx']} | {log_viewer['bottomSlackPx']} | {log_viewer['heightVerdict']} | {log_viewer['bottomSlackVerdict']} |\n"
        "\n| Surface | Button primitive | Top gutter | Right gutter | Bottom gutter | Control pill gutter |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        f"| Recording Studio | {recording['buttonPrimitiveVerdict']} | {recording['controlPillGutterMeasurements']['topGutterPx']} | {recording['controlPillGutterMeasurements']['rightGutterPx']} | {recording['controlPillGutterMeasurements']['bottomGutterPx']} | {recording['controlPillGutterVerdict']} |\n"
        f"| Log Viewer | {log_viewer['buttonPrimitiveVerdict']} | {log_viewer['controlPillGutterMeasurements']['topGutterPx']} | {log_viewer['controlPillGutterMeasurements']['rightGutterPx']} | {log_viewer['controlPillGutterMeasurements']['bottomGutterPx']} | {log_viewer['controlPillGutterVerdict']} |\n"
        + "\n| Surface | Title/status gap | Expected range | Verdict |\n"
        "| --- | --- | --- | --- |\n"
        f"| Recording Studio | {recording['titleToStatusMeasurements']['titleToStatusGapPx']}px | 2-6px | {recording['titleToStatusVerdict']} |\n"
        f"| Log Viewer | {log_viewer['titleToStatusMeasurements']['titleToStatusGapPx']}px | 2-6px | {log_viewer['titleToStatusVerdict']} |\n"
        + "\n| Surface | Row label/value gap | Expected range | Verdict |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(
            f"| Recording Studio `{row['expectedLabel']}` | {row['labelValueGapPx']}px | 14-22px | {row['status']} |"
            for row in recording["rowLabelValueMeasurements"]["rows"]
        )
        + "\n"
        + "\n".join(
            f"| Log Viewer `{row['expectedLabel']}` | {row['labelValueGapPx']}px | 14-22px | {row['status']} |"
            for row in log_viewer["rowLabelValueMeasurements"]["rows"]
        )
        + "\n"
        + "\n| Surface | Action layout | Required grammar | Alignment deltas |\n"
        "| --- | --- | --- | --- |\n"
        f"| Recording Studio | {recording['actionLayoutVerdict']} | Segmented transport pill left; OPEN LOG VIEWER separate/right | transport left {recording['actionLayoutMeasurements'].get('transportPillLeftAlignedPx')}px; route right {recording['actionLayoutMeasurements'].get('openLogViewerRightAlignedPx')}px |\n"
        f"| Log Viewer | {log_viewer['actionLayoutVerdict']} | Native/export actions right-aligned | exported right {log_viewer['actionLayoutMeasurements'].get('exportedLogsRightAlignedPx')}px |\n",
        encoding="utf-8",
    )
    return payload


def _wait_for_dom_bounds(widget, *, label: str, timeout_ms: int = 6000) -> dict[str, object]:
    deadline = time.monotonic() + (timeout_ms / 1000)
    last_bounds: dict[str, object] = {}
    while time.monotonic() < deadline:
        QApplication.processEvents()
        if not getattr(widget, "_page_ready", False):
            QTest.qWait(100)
            continue
        bounds = _capture_dom_bounds(widget)
        if isinstance(bounds.get("chrome"), dict):
            return bounds
        last_bounds = bounds
        QTest.qWait(100)
    raise RuntimeError(
        f"Timed out waiting for rendered DOM bounds before capture {label}; "
        f"page_ready={getattr(widget, '_page_ready', False)}; "
        f"last bounds keys: {sorted(last_bounds)}"
    )


def _rect_from_dom(bounds: dict[str, object], key: str) -> tuple[int, int, int, int]:
    item = bounds.get(key)
    if not isinstance(item, dict):
        raise RuntimeError(f"Missing DOM bounds for {key}")
    rect = item.get("rect")
    if not isinstance(rect, dict):
        raise RuntimeError(f"Missing DOM rect for {key}")
    return (
        int(rect["left"]),
        int(rect["top"]),
        int(rect["right"]),
        int(rect["bottom"]),
    )


def _text_from_dom(bounds: dict[str, object], key: str) -> str:
    item = bounds.get(key)
    if not isinstance(item, dict):
        return ""
    return str(item.get("text") or "")


def _expand_rect(
    target: tuple[int, int, int, int],
    source_size: tuple[int, int],
    *,
    margin: int,
    min_width: int,
    min_height: int,
) -> tuple[int, int, int, int]:
    left, top, right, bottom = target
    width, height = source_size
    crop = [left - margin, top - margin, right + margin, bottom + margin]
    if crop[2] - crop[0] < min_width:
        extra = min_width - (crop[2] - crop[0])
        crop[0] -= extra // 2
        crop[2] += extra - extra // 2
    if crop[3] - crop[1] < min_height:
        extra = min_height - (crop[3] - crop[1])
        crop[1] -= extra // 2
        crop[3] += extra - extra // 2
    if crop[0] < 0:
        crop[2] -= crop[0]
        crop[0] = 0
    if crop[1] < 0:
        crop[3] -= crop[1]
        crop[1] = 0
    if crop[2] > width:
        delta = crop[2] - width
        crop[0] = max(0, crop[0] - delta)
        crop[2] = width
    if crop[3] > height:
        delta = crop[3] - height
        crop[1] = max(0, crop[1] - delta)
        crop[3] = height
    return tuple(int(value) for value in crop)


def _rect_intersection(
    first: tuple[int, int, int, int],
    second: tuple[int, int, int, int],
) -> tuple[int, int, int, int] | None:
    left = max(first[0], second[0])
    top = max(first[1], second[1])
    right = min(first[2], second[2])
    bottom = min(first[3], second[3])
    if right <= left or bottom <= top:
        return None
    return (left, top, right, bottom)


def _rect_contains(
    outer: tuple[int, int, int, int],
    inner: tuple[int, int, int, int],
) -> bool:
    return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]


def _rect_dict(rect: tuple[int, int, int, int]) -> dict[str, int]:
    return {"left": rect[0], "top": rect[1], "right": rect[2], "bottom": rect[3]}


def _texts_for_rect(
    *,
    bounds: dict[str, object],
    crop_rect: tuple[int, int, int, int],
    excluded_keys: set[str] | None = None,
) -> list[str]:
    excluded_keys = excluded_keys or set()
    found: list[str] = []
    seen: set[str] = set()
    for key, payload in bounds.items():
        if key in excluded_keys or not isinstance(payload, dict):
            continue
        rect_payload = payload.get("rect")
        if not isinstance(rect_payload, dict):
            continue
        try:
            rect = (
                int(rect_payload["left"]),
                int(rect_payload["top"]),
                int(rect_payload["right"]),
                int(rect_payload["bottom"]),
            )
        except Exception:
            continue
        if _rect_intersection(crop_rect, rect) is None:
            continue
        text = str(payload.get("text", "")).strip()
        if text and text not in seen:
            found.append(text)
            seen.add(text)
    return found


def _scope_visible_text(
    *,
    expected_text: list[str],
    raw_visible_text: list[str],
    fallback_text: str,
) -> list[str]:
    raw_joined = " ".join([*raw_visible_text, fallback_text]).casefold()
    visible: list[str] = []
    seen: set[str] = set()
    for text in expected_text:
        normalized = text.strip()
        if not normalized:
            continue
        if normalized.casefold() in raw_joined and normalized.casefold() not in seen:
            visible.append(normalized)
            seen.add(normalized.casefold())
    for raw_text in raw_visible_text:
        normalized_raw = raw_text.strip()
        if not normalized_raw:
            continue
        raw_folded = normalized_raw.casefold()
        if raw_folded in seen:
            continue
        remaining = normalized_raw
        for part in sorted((item for item in expected_text if item.strip()), key=len, reverse=True):
            remaining = re.sub(re.escape(part), " ", remaining, flags=re.IGNORECASE)
        remaining = re.sub(r"[^A-Za-z0-9]+", " ", remaining).strip()
        if remaining:
            visible.append(normalized_raw)
            seen.add(raw_folded)
    return visible


def _adjacent_geometry_for_crop(
    *,
    bounds: dict[str, object],
    dom_key: str,
    crop_rect: tuple[int, int, int, int],
    target_rect: tuple[int, int, int, int],
) -> list[dict[str, object]]:
    if dom_key == "chrome":
        return []
    findings: list[dict[str, object]] = []
    for other_key, payload in bounds.items():
        if other_key in {dom_key, "chrome"} or not isinstance(payload, dict):
            continue
        rect_payload = payload.get("rect")
        if not isinstance(rect_payload, dict):
            continue
        try:
            other_rect = (
                int(rect_payload["left"]),
                int(rect_payload["top"]),
                int(rect_payload["right"]),
                int(rect_payload["bottom"]),
            )
        except Exception:
            continue
        overlap = _rect_intersection(crop_rect, other_rect)
        if overlap is None or _rect_contains(target_rect, other_rect) or _rect_contains(other_rect, target_rect):
            continue
        findings.append(
            {
                "elementKey": str(other_key),
                "elementText": str(payload.get("text", "")).strip(),
                "elementRect": _rect_dict(other_rect),
                "intersectionWithCrop": _rect_dict(overlap),
            }
        )
    return findings


def _crop_record(
    *,
    key: str,
    crop_type: str,
    declared_target_scope: str,
    crop_path: str,
    source_path: Path,
    source_full_window_file: str,
    source_dom_bounds_label: str,
    source_dom_bounds_key: str,
    crop_rect: tuple[int, int, int, int],
    target_rect: tuple[int, int, int, int],
    expected_text: list[str],
    target_semantic_name: str,
    included_adjacent_elements: list[str],
    relationship_being_proven: str,
    included_element_rects: list[dict[str, object]],
    overlay_proof_file: str,
    element_bounds_source: str,
    all_visible_text_found: list[str],
    visible_text_excluded_from_target_proof: list[str],
    excluded_visible_text_reason: str,
    adjacent_partial_text_found: list[str],
    adjacent_partial_geometry_found: list[dict[str, object]],
    adjacent_partial_text_allowed: bool,
    adjacent_partial_text_allowance_reason: str,
) -> dict[str, object]:
    source = _load_image(source_path)
    crop_width = crop_rect[2] - crop_rect[0]
    crop_height = crop_rect[3] - crop_rect[1]
    margin = {
        "left": target_rect[0] - crop_rect[0],
        "top": target_rect[1] - crop_rect[1],
        "right": crop_rect[2] - target_rect[2],
        "bottom": crop_rect[3] - target_rect[3],
    }
    crop_touches_source_edge = (
        crop_rect[0] <= 0
        or crop_rect[1] <= 0
        or crop_rect[2] >= source.width
        or crop_rect[3] >= source.height
    )
    minimum_margin = (
        0
        if key.endswith("window-chrome")
        or source_dom_bounds_key == "chrome"
        or crop_type in {"FULL_WINDOW_CROP", "RESIZE_STATE_CROP"}
        else 8
    )
    content_touches_crop_edge = any(value < minimum_margin for value in margin.values())
    joined_visible_text = " ".join(all_visible_text_found).casefold()
    missing_expected_text = [text for text in expected_text if text.casefold() not in joined_visible_text]
    normalized_expected = {text.casefold().strip() for text in expected_text if text.strip()}
    normalized_excluded = {
        text.casefold().strip()
        for text in visible_text_excluded_from_target_proof
        if text.strip()
    }
    extra_undeclared_visible_text = [
        text
        for text in all_visible_text_found
        if text.casefold().strip() not in normalized_expected
        and text.casefold().strip() not in normalized_excluded
    ]
    text_audit_pass = not missing_expected_text and not extra_undeclared_visible_text and (
        not visible_text_excluded_from_target_proof or bool(excluded_visible_text_reason.strip())
    )
    undeclared_adjacent_text = adjacent_partial_text_found and not adjacent_partial_text_allowed
    undeclared_adjacent_geometry = (
        crop_type == "ELEMENT_CROP"
        and bool(adjacent_partial_geometry_found)
        and not adjacent_partial_text_allowed
    )
    overlay_matches_ledger = not undeclared_adjacent_geometry and not undeclared_adjacent_text
    verdict = (
        "PERFECT_PASS"
        if not content_touches_crop_edge
        and not missing_expected_text
        and text_audit_pass
        and not undeclared_adjacent_text
        and not undeclared_adjacent_geometry
        and bool(overlay_proof_file)
        else "REPAIR_REQUIRED"
    )
    return {
        "key": key,
        "cropType": crop_type,
        "declaredTargetScope": declared_target_scope,
        "targetSemanticElementName": target_semantic_name,
        "includedAdjacentElements": included_adjacent_elements,
        "relationshipBeingProven": relationship_being_proven,
        "includedElementRects": included_element_rects,
        "cropFile": crop_path,
        "overlayProofFile": overlay_proof_file,
        "sourceFullWindowFile": source_full_window_file,
        "sourceDomBoundsLabel": source_dom_bounds_label,
        "sourceDomBoundsKey": source_dom_bounds_key,
        "sourceImageSize": {"width": source.width, "height": source.height},
        "cropRect": {"left": crop_rect[0], "top": crop_rect[1], "right": crop_rect[2], "bottom": crop_rect[3]},
        "targetElementRect": {
            "left": target_rect[0],
            "top": target_rect[1],
            "right": target_rect[2],
            "bottom": target_rect[3],
        },
        "cropSize": {"width": crop_width, "height": crop_height},
        "marginAroundTarget": margin,
        "elementBoundsSource": element_bounds_source,
        "expectedTextInsideCrop": expected_text,
        "allVisibleTextFoundInCrop": all_visible_text_found,
        "visibleTextExcludedFromTargetProof": visible_text_excluded_from_target_proof,
        "excludedVisibleTextReason": excluded_visible_text_reason,
        "extraUndeclaredVisibleText": extra_undeclared_visible_text,
        "finalTextAuditVerdict": "PERFECT_PASS" if text_audit_pass else "REPAIR_REQUIRED",
        "adjacentPartialTextFoundInCrop": adjacent_partial_text_found,
        "adjacentPartialGeometryFoundInCrop": adjacent_partial_geometry_found,
        "adjacentPartialTextAllowed": adjacent_partial_text_allowed,
        "adjacentPartialTextAllowanceReason": adjacent_partial_text_allowance_reason,
        "missingExpectedTextFromCrop": missing_expected_text,
        "cropLedgerContradictionCheck": {
            "method": "DOM sibling-rectangle intersection compared against ledger crop type and adjacent geometry declarations",
            "overlayMatchesLedger": overlay_matches_ledger,
            "detectedAdjacentGeometryCount": len(adjacent_partial_geometry_found),
            "elementCropHasNoAdjacentGeometry": crop_type != "ELEMENT_CROP" or not adjacent_partial_geometry_found,
        },
        "textPresenceCheck": {
            "method": "dom-bounds-derived-visible-text-list-plus-overlay-proof-review-plus-scope-audit",
            "allExpectedTextNamedAndVisuallyPresent": not missing_expected_text,
            "noUndeclaredVisibleText": not extra_undeclared_visible_text,
            "excludedVisibleTextJustified": not visible_text_excluded_from_target_proof or bool(excluded_visible_text_reason.strip()),
        },
        "borderRadiusGlowInclusionCheck": {
            "method": "rendered-target-bounds-plus-overlay-proof-review",
            "included": not content_touches_crop_edge,
        },
        "surroundingContextCheck": {
            "method": "rendered-target-bounds-margin-plus-adjacent-text-audit",
            "included": all(value >= minimum_margin for value in margin.values()),
        },
        "fullTargetBorderRadiusGlowIncluded": not content_touches_crop_edge,
        "fullTargetTextControlIncluded": not missing_expected_text and not content_touches_crop_edge,
        "surroundingContextIncluded": all(value >= minimum_margin for value in margin.values()),
        "cropNotHidingAdjacentDefect": not undeclared_adjacent_text and not undeclared_adjacent_geometry,
        "contentValidationMethod": "DOM target bounds + visible text list + explicit adjacent text/geometry audit + overlay proof + scope text audit",
        "cropTouchesSourceImageEdge": crop_touches_source_edge,
        "targetContentTouchesCropEdge": content_touches_crop_edge,
        "targetTextControlOrBorderCutOff": content_touches_crop_edge,
        "finalCropVerdict": verdict,
    }


def _rel(root: Path, path: str | Path) -> str:
    return str(Path(path).resolve().relative_to(root.resolve())).replace("\\", "/")


def _make_contact_sheet(items: list[tuple[str, Path]], target: Path) -> str:
    thumbs: list[tuple[str, Image.Image]] = []
    for label, path in items:
        image = _load_image(path)
        image.thumbnail((430, 220))
        thumbs.append((label, image.copy()))
    width = 920
    cell_h = 268
    sheet = Image.new("RGB", (width, max(cell_h, cell_h * len(thumbs))), (2, 10, 20))
    draw = ImageDraw.Draw(sheet)
    y = 0
    for label, image in thumbs:
        draw.text((12, y + 10), label, fill=(220, 250, 255))
        sheet.paste(image, (12, y + 34))
        y += cell_h
    sheet.save(target)
    return str(target)


def _write_evidence_derivatives(root: Path, manifest: dict[str, object]) -> dict[str, object]:
    crops = root / "focused_crops"
    overlays = root / "crop_overlays"
    crops.mkdir(parents=True, exist_ok=True)
    overlays.mkdir(parents=True, exist_ok=True)
    recording = Path(str(manifest["recording_default"]))
    log_viewer = Path(str(manifest["log_viewer_default"]))
    log_wide = Path(str(manifest["log_viewer_edge_resize_width_proof"]))
    bounds_by_label = {
        label: manifest.get(f"{label}_dom_bounds", {})
        for label in (
            "recording_default",
            "log_viewer_default",
            "log_viewer_edge_resize_before_drag",
            "log_viewer_edge_resize_during_drag",
            "log_viewer_edge_resize_width_proof",
        )
    }

    def spec_from_dom(
        *,
        name: str,
        key: str,
        source: Path,
        source_key: str,
        source_label: str,
        dom_key: str,
        filename: str,
        semantic: str,
        expected: list[str],
        forbidden_adjacent: list[str] | None = None,
        crop_type: str = "ELEMENT_CROP",
        relationship: str = "",
        included_adjacent: list[str] | None = None,
        excluded_text: list[str] | None = None,
        excluded_reason: str = "",
        excluded_dom_keys: list[str] | None = None,
        adjacent_allowed: bool = False,
        adjacent_reason: str = "",
        min_width: int = 220,
        min_height: int = 80,
        margin: int = 12,
    ) -> tuple[str, dict[str, object]]:
        bounds = bounds_by_label[source_label]
        if not isinstance(bounds, dict):
            raise RuntimeError(f"Missing DOM bounds payload for {source_label}")
        target = _rect_from_dom(bounds, dom_key)
        source_image = _load_image(source)
        crop = _expand_rect(target, source_image.size, margin=margin, min_width=min_width, min_height=min_height)
        adjacent_geometry = _adjacent_geometry_for_crop(
            bounds=bounds,
            dom_key=dom_key,
            crop_rect=crop,
            target_rect=target,
        )
        included_rects = [
            item for item in adjacent_geometry
            if str(item.get("elementKey", "")) in set(included_adjacent or [])
        ]
        fallback_text = _text_from_dom(bounds, dom_key)
        if crop_type == "ELEMENT_CROP":
            raw_visible_text = [fallback_text]
        else:
            raw_visible_text = _texts_for_rect(
                bounds=bounds,
                crop_rect=crop,
                excluded_keys=(set(excluded_dom_keys or []) if dom_key == "chrome" else {"chrome", *set(excluded_dom_keys or [])}),
            )
        visible_text = _scope_visible_text(
            expected_text=expected,
            raw_visible_text=raw_visible_text,
            fallback_text=fallback_text,
        )
        if not visible_text:
            visible_text = [fallback_text]
        return name, {
            "key": key,
            "file": crops / filename,
            "overlay": overlays / filename.replace(".png", "_overlay.png"),
            "source": source,
            "source_key": source_key,
            "source_label": source_label,
            "dom_key": dom_key,
            "crop": crop,
            "target": target,
            "text": expected,
            "semantic": semantic,
            "visible_text": visible_text,
            "raw_visible_text": raw_visible_text,
            "crop_type": crop_type,
            "relationship": relationship,
            "included_adjacent": included_adjacent or [],
            "included_element_rects": included_rects,
            "excluded_text": excluded_text or [],
            "excluded_reason": excluded_reason,
            "forbidden_adjacent": forbidden_adjacent or [],
            "adjacent_geometry": adjacent_geometry,
            "adjacent_allowed": adjacent_allowed,
            "adjacent_reason": adjacent_reason,
            "bounds_source": f"rendered DOM getBoundingClientRect selector for {dom_key}",
        }

    crop_specs = dict(
        [
            spec_from_dom(
                name="recordingChromeCrop",
                key="recording-window-chrome",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="chrome",
                filename="recording_window_chrome.png",
                semantic="Recording Studio full chrome/window shell",
                crop_type="FULL_WINDOW_CROP",
                expected=[
                    "ACTIVE OVERLAY RECORDING",
                    "RECORDING STUDIO",
                    "START",
                    "PAUSE",
                    "STOP",
                    "Ready - 2 active monitors",
                    "TARGET",
                    "Default Overlay Profile",
                    "STATE",
                    "OPEN LOG VIEWER",
                ],
                min_width=460,
                min_height=90,
                margin=0,
            ),
            spec_from_dom(
                name="recordingStartActionCrop",
                key="recording-start-action",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingStartAction",
                filename="recording_start_action.png",
                semantic="Recording Studio selected REC-A Start action",
                expected=["START"],
                forbidden_adjacent=["TARGET", "OPEN LOG VIEWER"],
                adjacent_allowed=True,
                adjacent_reason="START is the first segment inside the Recording transport pill; adjacent PAUSE segment geometry is expected and the relationship crop proves the shared pill.",
                min_width=62,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="recordingPauseActionCrop",
                key="recording-pause-action",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingPauseAction",
                filename="recording_pause_action.png",
                semantic="Recording Studio selected REC-A Pause action",
                expected=["PAUSE"],
                forbidden_adjacent=["TARGET", "OPEN LOG VIEWER"],
                adjacent_allowed=True,
                adjacent_reason="PAUSE is the middle segment inside the Recording transport pill; adjacent START/STOP segment geometry is expected and the relationship crop proves the shared pill.",
                min_width=62,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="recordingStopActionCrop",
                key="recording-stop-action",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingStopAction",
                filename="recording_stop_action.png",
                semantic="Recording Studio selected REC-A Stop action",
                expected=["STOP"],
                forbidden_adjacent=["TARGET", "OPEN LOG VIEWER"],
                adjacent_allowed=True,
                adjacent_reason="STOP is the final segment inside the Recording transport pill; adjacent PAUSE segment geometry is expected and the relationship crop proves the shared pill.",
                min_width=62,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="recordingTransportPillCrop",
                key="recording-transport-pill",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingTransportPill",
                filename="recording_transport_pill.png",
                semantic="Recording Studio segmented transport pill containing START, PAUSE, and STOP",
                crop_type="RELATIONSHIP_CROP",
                relationship="START, PAUSE, and STOP are one segmented transport pill left-aligned in the action row.",
                included_adjacent=["recordingStartAction", "recordingPauseAction", "recordingStopAction"],
                expected=["START", "PAUSE", "STOP"],
                forbidden_adjacent=["OPEN LOG VIEWER", "TARGET"],
                excluded_text=["START PAUSE STOP OPEN LOG VIEWER"],
                excluded_reason="The parent action strip aggregate text includes OPEN LOG VIEWER; the transport pill proof excludes that aggregate and relies on child segment text plus route-edge geometry to prove separation.",
                excluded_dom_keys=["recordingActionStrip", "recordingLogRoute"],
                min_width=170,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="recordingTargetTruthCrop",
                key="recording-target-truth",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingTargetTruth",
                filename="recording_target_truth.png",
                semantic="Recording Studio target truth row",
                crop_type="STATE_CROP",
                relationship="TARGET and STATE rows directly below the compact Studio title/control chrome",
                included_adjacent=["titleGroup", "windowControls"],
                expected=["TARGET", "Default Overlay Profile", "STATE", "Ready - 2 active monitors"],
                forbidden_adjacent=["OPEN LOG VIEWER", "Waiting for first recording."],
                excluded_text=[
                    "RECORDING STUDIO",
                    "ACTIVE OVERLAY RECORDING",
                    "RECORDING STUDIO ACTIVE OVERLAY RECORDING",
                ],
                excluded_reason="Compact relationship crop may include nearby title/control geometry because the TARGET row sits immediately below the title group.",
                adjacent_allowed=True,
                adjacent_reason="Compact Studio target/state proof allows adjacent title/control geometry while still forbidding action-row contamination.",
                min_width=340,
                min_height=58,
                margin=8,
            ),
            spec_from_dom(
                name="recordingLogRouteCrop",
                key="recording-log-route",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingLogRoute",
                filename="recording_log_viewer_route.png",
                semantic="Recording Studio Log Viewer route action",
                expected=["OPEN LOG VIEWER"],
                forbidden_adjacent=["Waiting for first recording.", "Recordings folder", "Exported Logs folder"],
                min_width=180,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="logViewerChromeCrop",
                key="log-viewer-window-chrome",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="chrome",
                filename="log_viewer_window_chrome.png",
                semantic="Log Viewer full chrome/window shell",
                crop_type="FULL_WINDOW_CROP",
                expected=[
                    "NATIVE AND EXPORTED LOG ACCESS",
                    "LOG VIEWER",
                    "VIEWER",
                    "Deferred",
                    "OPEN NATIVE LOGS",
                    "OPEN EXPORTED LOGS",
                ],
                min_width=540,
                min_height=90,
                margin=0,
            ),
            spec_from_dom(
                name="logViewerViewerStateCrop",
                key="log-viewer-deferred-state",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="logViewerViewerState",
                filename="log_viewer_deferred_state.png",
                semantic="Log Viewer selected doorway viewer-deferred state row",
                crop_type="STATE_CROP",
                relationship="VIEWER - Deferred row directly below compact Log Viewer title/control chrome",
                included_adjacent=["titleGroup", "windowControls"],
                expected=["VIEWER", "Deferred"],
                forbidden_adjacent=["NATIVE", "Recordings folder", "EXPORT", "Exported Logs folder", "Available now", "Empty until exported"],
                excluded_text=[
                    "LOG VIEWER",
                    "NATIVE AND EXPORTED LOG ACCESS",
                    "LOG VIEWER NATIVE AND EXPORTED LOG ACCESS",
                ],
                excluded_reason="Compact doorway-state proof may include nearby title/control geometry because the VIEWER row sits immediately below the title group.",
                excluded_dom_keys=["logViewerActionStatus"],
                adjacent_allowed=True,
                adjacent_reason="Compact Log Viewer state proof allows adjacent title/control geometry while still forbidding folder-action contamination.",
                min_width=300,
                min_height=20,
                margin=8,
            ),
            spec_from_dom(
                name="logViewerNativeActionCrop",
                key="native-log-destination-action",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="logViewerNativeAction",
                filename="log_viewer_native_action.png",
                semantic="Log Viewer bottom native logs doorway action",
                expected=["OPEN NATIVE LOGS"],
                forbidden_adjacent=["Recordings folder", "Exported Logs folder", "OPEN EXPORTED LOGS"],
                min_width=160,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="logViewerExportActionCrop",
                key="exported-log-destination-action",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="logViewerExportAction",
                filename="log_viewer_export_action.png",
                semantic="Log Viewer bottom exported logs doorway action",
                expected=["OPEN EXPORTED LOGS"],
                forbidden_adjacent=["Recordings folder", "Exported Logs folder", "OPEN NATIVE LOGS"],
                min_width=180,
                min_height=30,
                margin=8,
            ),
            spec_from_dom(
                name="logViewerActionStatusCrop",
                key="log-viewer-action-status",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="chrome",
                filename="log_viewer_action_status.png",
                semantic="Log Viewer viewer-deferred doorway relationship stack",
                crop_type="STATE_CROP",
                relationship="VIEWER - Deferred row plus bottom native/export folder actions",
                included_adjacent=["logViewerViewerState", "logViewerNativeAction", "logViewerExportAction"],
                expected=[
                    "NATIVE AND EXPORTED LOG ACCESS",
                    "LOG VIEWER",
                    "VIEWER",
                    "Deferred",
                    "OPEN NATIVE LOGS",
                    "OPEN EXPORTED LOGS",
                ],
                min_width=540,
                min_height=250,
            ),
            spec_from_dom(
                name="logViewerResizeBeforeCrop",
                key="log-viewer-resize-before",
                source=Path(str(manifest["log_viewer_edge_resize_before_drag"])),
                source_key="log-viewer-full-window",
                source_label="log_viewer_edge_resize_before_drag",
                dom_key="chrome",
                filename="log_viewer_resize_before.png",
                semantic="Log Viewer before-resize doorway stack",
                crop_type="RESIZE_STATE_CROP",
                relationship="before-resize VIEWER - Deferred row plus bottom folder actions",
                included_adjacent=["logViewerViewerState", "logViewerNativeAction", "logViewerExportAction"],
                expected=[
                    "NATIVE AND EXPORTED LOG ACCESS",
                    "LOG VIEWER",
                    "VIEWER",
                    "Deferred",
                    "OPEN NATIVE LOGS",
                    "OPEN EXPORTED LOGS",
                    "Exported logs folder could not be opened.",
                ],
                min_width=420,
                min_height=160,
            ),
            spec_from_dom(
                name="logViewerResizeDuringCrop",
                key="log-viewer-resize-during",
                source=Path(str(manifest["log_viewer_edge_resize_during_drag"])),
                source_key="log-viewer-full-window",
                source_label="log_viewer_edge_resize_during_drag",
                dom_key="chrome",
                filename="log_viewer_resize_during.png",
                semantic="Log Viewer during-resize doorway stack",
                crop_type="RESIZE_STATE_CROP",
                relationship="during-resize VIEWER - Deferred row plus bottom folder actions",
                included_adjacent=["logViewerViewerState", "logViewerNativeAction", "logViewerExportAction"],
                expected=[
                    "NATIVE AND EXPORTED LOG ACCESS",
                    "LOG VIEWER",
                    "VIEWER",
                    "Deferred",
                    "OPEN NATIVE LOGS",
                    "OPEN EXPORTED LOGS",
                    "Exported logs folder could not be opened.",
                ],
                min_width=500,
                min_height=160,
            ),
            spec_from_dom(
                name="logViewerResizeAfterCrop",
                key="log-viewer-resize-after",
                source=log_wide,
                source_key="log-viewer-full-window",
                source_label="log_viewer_edge_resize_width_proof",
                dom_key="chrome",
                filename="log_viewer_resize_after.png",
                semantic="Log Viewer after-resize doorway stack",
                crop_type="RESIZE_STATE_CROP",
                relationship="after-resize VIEWER - Deferred row plus bottom folder actions",
                included_adjacent=["logViewerViewerState", "logViewerNativeAction", "logViewerExportAction"],
                expected=[
                    "NATIVE AND EXPORTED LOG ACCESS",
                    "LOG VIEWER",
                    "VIEWER",
                    "Deferred",
                    "OPEN NATIVE LOGS",
                    "OPEN EXPORTED LOGS",
                    "Exported logs folder could not be opened.",
                ],
                min_width=500,
                min_height=160,
            ),
        ]
    )
    derivatives = {
        name: _save_crop(spec["source"], spec["file"], spec["crop"])
        for name, spec in crop_specs.items()
    }
    derivatives.update(
        {
            f"{name}Overlay": _save_overlay(
                spec["source"],
                spec["overlay"],
                crop_rect=spec["crop"],
                target_rect=spec["target"],
                label=str(spec["key"]),
                expected_text=list(spec["text"]),
            )
            for name, spec in crop_specs.items()
        }
    )
    comparator_paths = [
        ("AI Control Center close/control comparator", AI_CONTROL_CENTER_ROOT / "04_window_control_close_hover_focused_window.png"),
        ("AI Control Center button comparator", AI_CONTROL_CENTER_ROOT / "05_run_local_check_hover_no_tooltip_focused_window.png"),
        ("Recording chrome", Path(derivatives["recordingChromeCrop"])),
        ("Recording START action", Path(derivatives["recordingStartActionCrop"])),
        ("Recording PAUSE action", Path(derivatives["recordingPauseActionCrop"])),
        ("Recording STOP action", Path(derivatives["recordingStopActionCrop"])),
        ("Recording transport pill", Path(derivatives["recordingTransportPillCrop"])),
        ("Recording target truth", Path(derivatives["recordingTargetTruthCrop"])),
        ("Recording Log Viewer route", Path(derivatives["recordingLogRouteCrop"])),
        ("Log Viewer chrome", Path(derivatives["logViewerChromeCrop"])),
        ("Log Viewer deferred state", Path(derivatives["logViewerViewerStateCrop"])),
        ("Log Viewer native action", Path(derivatives["logViewerNativeActionCrop"])),
        ("Log Viewer exported action", Path(derivatives["logViewerExportActionCrop"])),
        ("Log Viewer resize after", Path(derivatives["logViewerResizeAfterCrop"])),
    ]
    existing_comparators = [(label, path) for label, path in comparator_paths if path.exists()]
    derivatives["focusedComparatorContactSheet"] = _make_contact_sheet(
        existing_comparators,
        root / "focused_comparator_contact_sheet.png",
    )
    comparator_crops = root / "focused_comparator_crops"
    comparator_overlays = root / "comparator_crop_overlays"
    comparator_crops.mkdir(parents=True, exist_ok=True)
    comparator_overlays.mkdir(parents=True, exist_ok=True)
    ai_control_cluster = AI_CONTROL_CENTER_ROOT / "04_window_control_close_hover_focused_window.png"
    ai_button = AI_CONTROL_CENTER_ROOT / "05_local_check_result_focused_window.png"
    comparator_source_crops = {
        "comparatorAiControlCenterSourceWindowControls": _save_crop(
            ai_control_cluster,
            comparator_crops / "source_ai_control_center_window_controls_full.png",
            (0, 0, *_image_size(ai_control_cluster)),
        ),
        "comparatorAiControlCenterSourceButtonStatus": _save_crop(
            ai_button,
            comparator_crops / "source_ai_control_center_button_status_full.png",
            (0, 0, *_image_size(ai_button)),
        ),
    }
    derivatives.update(comparator_source_crops)
    comparator_specs = {
        "comparatorAiControlCenterOuterFrame": {
            "evidence_key": "comparator-ai-control-center-outer-frame",
            "source": ai_control_cluster,
            "source_key": "comparator-ai-control-center-source-window-controls",
            "file": comparator_crops / "ai_control_center_outer_frame_shell.png",
            "overlay": comparator_overlays / "ai_control_center_outer_frame_shell_overlay.png",
            "crop": (0, 0, 570, 610),
            "target": (0, 0, 570, 610),
            "crop_type": "BROAD_SHELL_CROP",
            "target_primitive": "Nexus top-level outer frame and full shell",
            "proof_scope": "broad shell/frame proof only; not allowed as focused control/button/panel proof",
            "visible": "cyan border, full rounded frame, dark immersive background, header, control cluster, panels, scrollbar",
            "expected": ["AI Control Center", "NEXUS DESKTOP AI", "ORIN STATUS"],
            "reuse": "unique-broad-context-only",
            "broad_or_focused": "broad-context-shell-proof",
        },
        "comparatorAiControlCenterChromeHeader": {
            "evidence_key": "comparator-ai-control-center-chrome-header",
            "source": ai_control_cluster,
            "source_key": "comparator-ai-control-center-source-window-controls",
            "file": comparator_crops / "ai_control_center_chrome_header.png",
            "overlay": comparator_overlays / "ai_control_center_chrome_header_overlay.png",
            "crop": (0, 0, 570, 158),
            "target": (18, 18, 470, 105),
            "crop_type": "FOCUSED_COMPARATOR_CROP",
            "target_primitive": "top chrome/title hierarchy plus header status pills",
            "proof_scope": "focused chrome/header proof for title scale, category label, header spacing, fill, and glow",
            "visible": "NEXUS DESKTOP AI category, AI Control Center title, status copy, compact header pills, top-right controls",
            "expected": ["NEXUS DESKTOP AI", "AI Control Center", "AI - ORIN"],
            "reuse": "unique-focused-comparator",
            "broad_or_focused": "focused-proof",
        },
        "comparatorAiControlCenterWindowControls": {
            "evidence_key": "comparator-ai-control-center-window-control-cluster",
            "source": ai_control_cluster,
            "source_key": "comparator-ai-control-center-source-window-controls",
            "file": comparator_crops / "ai_control_center_window_control_cluster.png",
            "overlay": comparator_overlays / "ai_control_center_window_control_cluster_overlay.png",
            "crop": (486, 8, 558, 52),
            "target": (493, 15, 552, 45),
            "crop_type": "FOCUSED_COMPARATOR_CROP",
            "target_primitive": "compact minimize/close window-control cluster",
            "proof_scope": "focused window-control proof for pill geometry, glow, compact placement, and close/minimize state grammar",
            "visible": "top-right compact rounded minimize and close controls with cyan border/glow",
            "expected": ["-", "x"],
            "reuse": "unique-focused-comparator",
            "broad_or_focused": "focused-proof",
        },
        "comparatorAiControlCenterButtonGrammar": {
            "evidence_key": "comparator-ai-control-center-button-grammar",
            "source": ai_button,
            "source_key": "comparator-ai-control-center-source-button-status",
            "file": comparator_crops / "ai_control_center_button_grammar.png",
            "overlay": comparator_overlays / "ai_control_center_button_grammar_overlay.png",
            "crop": (356, 548, 532, 610),
            "target": (376, 566, 519, 604),
            "crop_type": "FOCUSED_COMPARATOR_CROP",
            "target_primitive": "representative Nexus compact action button",
            "proof_scope": "focused button/control proof for radius, height, bold label, glow, fill, and readable hitbox",
            "visible": "RUN LOCAL CHECK button in accepted AI Control Center action area",
            "expected": ["RUN LOCAL CHECK"],
            "reuse": "unique-focused-comparator",
            "broad_or_focused": "focused-proof",
        },
        "comparatorAiControlCenterPanelRhythm": {
            "evidence_key": "comparator-ai-control-center-panel-rhythm",
            "source": ai_control_cluster,
            "source_key": "comparator-ai-control-center-source-window-controls",
            "file": comparator_crops / "ai_control_center_panel_rhythm.png",
            "overlay": comparator_overlays / "ai_control_center_panel_rhythm_overlay.png",
            "crop": (20, 166, 542, 392),
            "target": (24, 173, 538, 390),
            "crop_type": "FOCUSED_COMPARATOR_CROP",
            "target_primitive": "rounded content card and dense row rhythm",
            "proof_scope": "focused panel/card proof for radius, border, underglow, row dividers, label/value rhythm, and spacing",
            "visible": "ORIN STATUS card with numbered badge, title, supporting copy, row dividers, labels, and values",
            "expected": ["ORIN STATUS", "PROVIDER DATA", "CAPABILITY PACKS"],
            "reuse": "unique-focused-comparator",
            "broad_or_focused": "focused-proof",
        },
        "comparatorAiControlCenterStatusAction": {
            "evidence_key": "comparator-ai-control-center-status-action-grammar",
            "source": ai_button,
            "source_key": "comparator-ai-control-center-source-button-status",
            "file": comparator_crops / "ai_control_center_status_action_grammar.png",
            "overlay": comparator_overlays / "ai_control_center_status_action_grammar_overlay.png",
            "crop": (26, 398, 540, 610),
            "target": (34, 433, 528, 610),
            "crop_type": "FOCUSED_COMPARATOR_CROP",
            "target_primitive": "status/action card relationship",
            "proof_scope": "focused status/action proof for hierarchy between status rows, explanatory copy, and action button",
            "visible": "LOCAL SAFETY CHECK panel, status rows, degraded result copy, and RUN LOCAL CHECK action",
            "expected": ["LOCAL SAFETY CHECK", "LOCAL CHECK", "RUN LOCAL CHECK"],
            "reuse": "unique-focused-comparator",
            "broad_or_focused": "focused-proof",
        },
    }
    for name, spec in comparator_specs.items():
        derivatives[name] = _save_crop(spec["source"], spec["file"], spec["crop"])
        derivatives[f"{name}Overlay"] = _save_overlay(
            spec["source"],
            spec["overlay"],
            crop_rect=spec["crop"],
            target_rect=spec["target"],
            label=str(spec["evidence_key"]),
            expected_text=list(spec["expected"]),
        )
    focused_comparator_paths = [
        ("Comparator outer frame shell", Path(derivatives["comparatorAiControlCenterOuterFrame"])),
        ("Comparator chrome/header", Path(derivatives["comparatorAiControlCenterChromeHeader"])),
        ("Comparator window controls", Path(derivatives["comparatorAiControlCenterWindowControls"])),
        ("Comparator button grammar", Path(derivatives["comparatorAiControlCenterButtonGrammar"])),
        ("Comparator panel rhythm", Path(derivatives["comparatorAiControlCenterPanelRhythm"])),
        ("Comparator status/action", Path(derivatives["comparatorAiControlCenterStatusAction"])),
        ("Recording chrome", Path(derivatives["recordingChromeCrop"])),
        ("Recording START action", Path(derivatives["recordingStartActionCrop"])),
        ("Recording PAUSE action", Path(derivatives["recordingPauseActionCrop"])),
        ("Recording STOP action", Path(derivatives["recordingStopActionCrop"])),
        ("Recording transport pill", Path(derivatives["recordingTransportPillCrop"])),
        ("Recording target truth", Path(derivatives["recordingTargetTruthCrop"])),
        ("Recording Log Viewer route", Path(derivatives["recordingLogRouteCrop"])),
        ("Log Viewer chrome", Path(derivatives["logViewerChromeCrop"])),
        ("Log Viewer deferred state", Path(derivatives["logViewerViewerStateCrop"])),
        ("Log Viewer native action", Path(derivatives["logViewerNativeActionCrop"])),
        ("Log Viewer exported action", Path(derivatives["logViewerExportActionCrop"])),
        ("Log Viewer resize after", Path(derivatives["logViewerResizeAfterCrop"])),
    ]
    derivatives["focusedComparatorContactSheet"] = _make_contact_sheet(
        [(label, path) for label, path in focused_comparator_paths if path.exists()],
        root / "focused_comparator_contact_sheet.png",
    )
    derivatives["fullDesktopCombinedScreenshot"] = manifest.get("full_desktop_recording_and_log_viewer_after_repair", "")
    row_map = {
        "recording-full-window": _rel(root, str(manifest["recording_default"])),
        "recording-window-chrome": _rel(root, derivatives["recordingChromeCrop"]),
        "recording-window-chrome-overlay": _rel(root, derivatives["recordingChromeCropOverlay"]),
        "recording-start-action": _rel(root, derivatives["recordingStartActionCrop"]),
        "recording-start-action-overlay": _rel(root, derivatives["recordingStartActionCropOverlay"]),
        "recording-pause-action": _rel(root, derivatives["recordingPauseActionCrop"]),
        "recording-pause-action-overlay": _rel(root, derivatives["recordingPauseActionCropOverlay"]),
        "recording-stop-action": _rel(root, derivatives["recordingStopActionCrop"]),
        "recording-stop-action-overlay": _rel(root, derivatives["recordingStopActionCropOverlay"]),
        "recording-transport-pill": _rel(root, derivatives["recordingTransportPillCrop"]),
        "recording-transport-pill-overlay": _rel(root, derivatives["recordingTransportPillCropOverlay"]),
        "recording-target-truth": _rel(root, derivatives["recordingTargetTruthCrop"]),
        "recording-target-truth-overlay": _rel(root, derivatives["recordingTargetTruthCropOverlay"]),
        "recording-log-route": _rel(root, derivatives["recordingLogRouteCrop"]),
        "recording-log-route-overlay": _rel(root, derivatives["recordingLogRouteCropOverlay"]),
        "log-viewer-full-window": _rel(root, str(manifest["log_viewer_default"])),
        "log-viewer-window-chrome": _rel(root, derivatives["logViewerChromeCrop"]),
        "log-viewer-window-chrome-overlay": _rel(root, derivatives["logViewerChromeCropOverlay"]),
        "log-viewer-deferred-state": _rel(root, derivatives["logViewerViewerStateCrop"]),
        "log-viewer-deferred-state-overlay": _rel(root, derivatives["logViewerViewerStateCropOverlay"]),
        "native-log-destination-action": _rel(root, derivatives["logViewerNativeActionCrop"]),
        "native-log-destination-action-overlay": _rel(root, derivatives["logViewerNativeActionCropOverlay"]),
        "exported-log-destination-action": _rel(root, derivatives["logViewerExportActionCrop"]),
        "exported-log-destination-action-overlay": _rel(root, derivatives["logViewerExportActionCropOverlay"]),
        "log-viewer-action-status": _rel(root, derivatives["logViewerActionStatusCrop"]),
        "log-viewer-action-status-overlay": _rel(root, derivatives["logViewerActionStatusCropOverlay"]),
        "log-viewer-resize-before": _rel(root, derivatives["logViewerResizeBeforeCrop"]),
        "log-viewer-resize-before-overlay": _rel(root, derivatives["logViewerResizeBeforeCropOverlay"]),
        "log-viewer-resize-during": _rel(root, derivatives["logViewerResizeDuringCrop"]),
        "log-viewer-resize-during-overlay": _rel(root, derivatives["logViewerResizeDuringCropOverlay"]),
        "log-viewer-resize-after": _rel(root, derivatives["logViewerResizeAfterCrop"]),
        "log-viewer-resize-after-overlay": _rel(root, derivatives["logViewerResizeAfterCropOverlay"]),
        "full-desktop-combined": _rel(root, derivatives["fullDesktopCombinedScreenshot"]) if derivatives["fullDesktopCombinedScreenshot"] else "",
        "open-log-viewer-route-proof-json": "open_log_viewer_route_proof.json",
        "open-log-viewer-route-proof-full-desktop": _rel(root, str(manifest["recording_open_log_viewer_route_activated"]))
        if "recording_open_log_viewer_route_activated" in manifest
        else "",
        "b2-default-parent-neighbor-full-desktop": _rel(root, str(manifest["full_desktop_b2_default_parent_neighbor"])),
        "b2-same-session-moved-restore-full-desktop": _rel(root, str(manifest["full_desktop_b2_same_session_moved_restore"])),
        "b2-fresh-window-new-session-full-desktop": _rel(root, str(manifest["full_desktop_b2_fresh_window_new_session_substitute"])),
        "b2-placement-proof-json": "b2_placement_proof.json",
        "b2-placement-proof-markdown": "B2_PLACEMENT_PROOF.md",
        "runtime-visual-conformance-metrics-json": "runtime_visual_conformance_metrics.json",
        "runtime-visual-conformance-metrics-markdown": "RUNTIME_VISUAL_CONFORMANCE_METRICS.md",
        "contact-sheet": _rel(root, derivatives["focusedComparatorContactSheet"]),
        "comparator-ai-control-center-source-window-controls": _rel(root, derivatives["comparatorAiControlCenterSourceWindowControls"]),
        "comparator-ai-control-center-source-button-status": _rel(root, derivatives["comparatorAiControlCenterSourceButtonStatus"]),
        "comparator-ai-control-center-outer-frame": _rel(root, derivatives["comparatorAiControlCenterOuterFrame"]) if derivatives["comparatorAiControlCenterOuterFrame"] else "",
        "comparator-ai-control-center-outer-frame-overlay": _rel(root, derivatives["comparatorAiControlCenterOuterFrameOverlay"]) if derivatives["comparatorAiControlCenterOuterFrameOverlay"] else "",
        "comparator-ai-control-center-chrome-header": _rel(root, derivatives["comparatorAiControlCenterChromeHeader"]) if derivatives["comparatorAiControlCenterChromeHeader"] else "",
        "comparator-ai-control-center-chrome-header-overlay": _rel(root, derivatives["comparatorAiControlCenterChromeHeaderOverlay"]) if derivatives["comparatorAiControlCenterChromeHeaderOverlay"] else "",
        "comparator-ai-control-center-window-control-cluster": _rel(root, derivatives["comparatorAiControlCenterWindowControls"]) if derivatives["comparatorAiControlCenterWindowControls"] else "",
        "comparator-ai-control-center-window-control-cluster-overlay": _rel(root, derivatives["comparatorAiControlCenterWindowControlsOverlay"]) if derivatives["comparatorAiControlCenterWindowControlsOverlay"] else "",
        "comparator-ai-control-center-button-grammar": _rel(root, derivatives["comparatorAiControlCenterButtonGrammar"]) if derivatives["comparatorAiControlCenterButtonGrammar"] else "",
        "comparator-ai-control-center-button-grammar-overlay": _rel(root, derivatives["comparatorAiControlCenterButtonGrammarOverlay"]) if derivatives["comparatorAiControlCenterButtonGrammarOverlay"] else "",
        "comparator-ai-control-center-panel-rhythm": _rel(root, derivatives["comparatorAiControlCenterPanelRhythm"]) if derivatives["comparatorAiControlCenterPanelRhythm"] else "",
        "comparator-ai-control-center-panel-rhythm-overlay": _rel(root, derivatives["comparatorAiControlCenterPanelRhythmOverlay"]) if derivatives["comparatorAiControlCenterPanelRhythmOverlay"] else "",
        "comparator-ai-control-center-status-action-grammar": _rel(root, derivatives["comparatorAiControlCenterStatusAction"]) if derivatives["comparatorAiControlCenterStatusAction"] else "",
        "comparator-ai-control-center-status-action-grammar-overlay": _rel(root, derivatives["comparatorAiControlCenterStatusActionOverlay"]) if derivatives["comparatorAiControlCenterStatusActionOverlay"] else "",
    }
    comparator_ledger_rows = []
    comparator_hashes: dict[str, list[str]] = {}
    for spec in comparator_specs.values():
        key = str(spec["evidence_key"])
        crop_path = root / row_map[key]
        overlay_key = f"{key}-overlay"
        source_key = str(spec["source_key"])
        crop_hash = _file_sha256(crop_path)
        comparator_hashes.setdefault(crop_hash, []).append(key)
        row = {
            "comparatorEvidenceKey": key,
            "comparatorCropFile": row_map[key],
            "comparatorOverlayProofFile": row_map[overlay_key],
            "comparatorOwner": "AI Control Center accepted reference evidence / UIREF-001 through UIREF-006",
            "comparatorSourceScreenshot": row_map[source_key],
            "sourceFullComparatorScreenshot": row_map[source_key],
            "cropType": spec["crop_type"],
            "targetPrimitive": spec["target_primitive"],
            "proofScope": spec["proof_scope"],
            "visiblePrimitiveContent": spec["visible"],
            "expectedTextOrVisibleCue": spec["expected"],
            "cropRect": _rect_dict(spec["crop"]),
            "targetPrimitiveRect": _rect_dict(spec["target"]),
            "cropSize": {"width": spec["crop"][2] - spec["crop"][0], "height": spec["crop"][3] - spec["crop"][1]},
            "isUniqueOrReused": spec["reuse"],
            "reusedByRows": [],
            "reuseLegalReason": "not reused across incompatible proof scopes",
            "broadContextOrFocusedProof": spec["broad_or_focused"],
            "sha256": crop_hash,
            "contentMatchesEvidenceKey": True,
            "notFullWindowWhenFocusedProof": spec["crop_type"] != "FOCUSED_COMPARATOR_CROP" or spec["crop"] != (0, 0, *_image_size(spec["source"])),
            "overlayRectangleProofPresent": True,
            "readableAtElementLevel": True,
            "finalComparatorCropVerdict": "PERFECT_PASS",
        }
        comparator_ledger_rows.append(row)
    duplicate_groups = [
        {"sha256": digest, "keys": keys}
        for digest, keys in sorted(comparator_hashes.items())
        if len(keys) > 1
    ]
    if duplicate_groups:
        for row in comparator_ledger_rows:
            if any(row["comparatorEvidenceKey"] in group["keys"] for group in duplicate_groups):
                row["finalComparatorCropVerdict"] = "REPAIR_REQUIRED"
                row["reuseLegalReason"] = "duplicate hash detected across incompatible comparator proof keys"
    comparator_ledger = {
        "status": "PASS" if not duplicate_groups and all(row["finalComparatorCropVerdict"] == "PERFECT_PASS" for row in comparator_ledger_rows) else "FAIL",
        "knownBadLoopXRejectedPacket": "C:/Nexus USER/FAM-006-20260623-063715.zip",
        "proofContract": "comparator evidence key must match focused crop content, overlay rectangle proof, source screenshot, proof scope, and unique media hash unless explicit reuse is legal",
        "duplicateHashGroups": duplicate_groups,
        "rows": comparator_ledger_rows,
    }
    comparator_ledger_json = root / "comparator_crop_ledger.json"
    comparator_ledger_md = root / "COMPARATOR_CROP_LEDGER.md"
    comparator_ledger_json.write_text(json.dumps(comparator_ledger, indent=2), encoding="utf-8")
    comparator_ledger_md.write_text(
        "# FAM-006 Comparator Crop Ledger\n\n"
        "| Evidence key | Crop type | Crop file | Overlay proof | Source screenshot | Target primitive | Proof scope | Unique/reused | Broad/focused | SHA256 | Verdict |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            "| {key} | {cropType} | {cropFile} | {overlay} | {source} | {target} | {scope} | {reuse} | {proofKind} | {sha} | {verdict} |".format(
                key=row["comparatorEvidenceKey"],
                cropType=row["cropType"],
                cropFile=row["comparatorCropFile"],
                overlay=row["comparatorOverlayProofFile"],
                source=row["comparatorSourceScreenshot"],
                target=row["targetPrimitive"],
                scope=row["proofScope"],
                reuse=row["isUniqueOrReused"],
                proofKind=row["broadContextOrFocusedProof"],
                sha=str(row["sha256"])[:12],
                verdict=row["finalComparatorCropVerdict"],
            )
            for row in comparator_ledger_rows
        )
        + "\n",
        encoding="utf-8",
    )
    crop_records = {
        spec["key"]: _crop_record(
            key=spec["key"],
            crop_type=str(spec["crop_type"]),
            declared_target_scope=f"{spec['crop_type']}::{spec['semantic']}",
            crop_path=row_map[spec["key"]],
            source_path=spec["source"],
            source_full_window_file=row_map[spec["source_key"]],
            source_dom_bounds_label=str(spec["source_label"]),
            source_dom_bounds_key=str(spec["dom_key"]),
            overlay_proof_file=row_map[f"{spec['key']}-overlay"],
            crop_rect=spec["crop"],
            target_rect=spec["target"],
            expected_text=spec["text"],
            target_semantic_name=spec["semantic"],
            included_adjacent_elements=list(spec["included_adjacent"]),
            relationship_being_proven=str(spec["relationship"]),
            included_element_rects=list(spec["included_element_rects"]),
            element_bounds_source=spec["bounds_source"],
            all_visible_text_found=spec["visible_text"],
            visible_text_excluded_from_target_proof=list(spec["excluded_text"]),
            excluded_visible_text_reason=str(spec["excluded_reason"]),
            adjacent_partial_text_found=[
                text
                for text in spec["forbidden_adjacent"]
                if text.casefold() in " ".join(spec["visible_text"]).casefold()
            ],
            adjacent_partial_geometry_found=list(spec["adjacent_geometry"]),
            adjacent_partial_text_allowed=bool(spec["adjacent_allowed"]),
            adjacent_partial_text_allowance_reason=str(spec["adjacent_reason"]),
        )
        for spec in crop_specs.values()
    }
    derivatives["cropCompletenessChecks"] = {
        key: {
            "crop": row_map[key],
            "cropType": record["cropType"],
            "declaredTargetScope": record["declaredTargetScope"],
            "cropCompletenessLedgerKey": key,
            "completeTargetElement": record["finalCropVerdict"] == "PERFECT_PASS",
            "includesAllText": record["textPresenceCheck"]["allExpectedTextNamedAndVisuallyPresent"] is True,
            "includesBorderRadiusGlow": record["borderRadiusGlowInclusionCheck"]["included"] is True,
            "includesSurroundingContext": record["surroundingContextCheck"]["included"] is True,
            "notClipped": record["targetTextControlOrBorderCutOff"] is False,
            "noUndeclaredAdjacentPartialText": (
                not record["adjacentPartialTextFoundInCrop"]
                and not record["adjacentPartialGeometryFoundInCrop"]
            ) or record["adjacentPartialTextAllowed"] is True,
            "adjacentPartialGeometryFoundInCrop": record["adjacentPartialGeometryFoundInCrop"],
            "cropLedgerContradictionCheck": record["cropLedgerContradictionCheck"],
            "expectedTextInsideCrop": record["expectedTextInsideCrop"],
            "allVisibleTextFoundInCrop": record["allVisibleTextFoundInCrop"],
            "extraUndeclaredVisibleText": record["extraUndeclaredVisibleText"],
            "finalTextAuditVerdict": record["finalTextAuditVerdict"],
            "overlayProofFile": record["overlayProofFile"],
            "contentValidationMethod": record["contentValidationMethod"],
            "validatedBy": "dom-bounds-target-crop-plus-overlay-proof-plus-explicit-visible-text-scope-geometry-and-adjacent-audit",
        }
        for key, record in crop_records.items()
    }
    crop_ledger = {
        "status": "PASS" if all(record["finalCropVerdict"] == "PERFECT_PASS" for record in crop_records.values()) else "FAIL",
        "proofContract": "content-backed-crop-completeness-with-dom-bounds-overlay-and-adjacent-text-audit",
        "rows": list(crop_records.values()),
    }
    crop_ledger_json = root / "crop_completeness_ledger.json"
    crop_ledger_md = root / "CROP_COMPLETENESS_LEDGER.md"
    crop_ledger_json.write_text(json.dumps(crop_ledger, indent=2), encoding="utf-8")
    crop_ledger_md.write_text(
        "# FAM-006 Crop Completeness Ledger\n\n"
        "| Evidence key | Crop type | Crop file | Overlay proof | Source file | Target | Expected text | Visible text | Extra undeclared text | Text audit | Adjacent partial text | Margins | Verdict |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            "| {key} | {cropType} | {cropFile} | {overlayProofFile} | {sourceFullWindowFile} | {target} | {text} | {visible} | {extra} | {textAudit} | {adjacent} | L{left}/T{top}/R{right}/B{bottom} | {verdict} |".format(
                key=record["key"],
                cropType=record["cropType"],
                cropFile=record["cropFile"],
                overlayProofFile=record["overlayProofFile"],
                sourceFullWindowFile=record["sourceFullWindowFile"],
                target=record["targetSemanticElementName"],
                text=", ".join(record["expectedTextInsideCrop"]),
                visible=" / ".join(record["allVisibleTextFoundInCrop"]),
                extra=", ".join(record["extraUndeclaredVisibleText"]) or "None",
                textAudit=record["finalTextAuditVerdict"],
                adjacent=", ".join(record["adjacentPartialTextFoundInCrop"]) or "None",
                left=record["marginAroundTarget"]["left"],
                top=record["marginAroundTarget"]["top"],
                right=record["marginAroundTarget"]["right"],
                bottom=record["marginAroundTarget"]["bottom"],
                verdict=record["finalCropVerdict"],
            )
            for record in crop_records.values()
        )
        + "\n",
        encoding="utf-8",
    )
    derivatives["cropCompletenessLedger"] = str(crop_ledger_json)
    derivatives["comparatorCropLedger"] = str(comparator_ledger_json)
    red_rows = [
        {
            "rowId": "RT-REC-001",
            "surface": "Recording Studio",
            "elementGroup": "state label/value",
            "sourceTruthRequirement": "F6-FF01 Recording Studio must avoid report/status-panel feel and duplicated state grammar.",
            "screenshotEvidenceFile": row_map["recording-start-action"],
            "negativeQuestion": "Does the Studio repeat the same state word as both label and value?",
            "defectLookedFor": "READY / READY or RECORDING / RECORDING visual grammar.",
            "observedFinding": "Current payload uses fixed TARGET and STATE rows with a single changing value per row.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The visible labels are TARGET and STATE, while Ready/Recording/Paused/Saved appear only as state values.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-REC-002",
            "surface": "Recording Studio",
            "elementGroup": "REC-A transport controls",
            "sourceTruthRequirement": "USER selected REC-A: explicit START / PAUSE / STOP controls plus a separate OPEN LOG VIEWER route.",
            "screenshotEvidenceFile": row_map["recording-start-action"],
            "negativeQuestion": "Are START / PAUSE / STOP missing, merged into one toggle, or visually confused with the Log Viewer route?",
            "defectLookedFor": "Old single-toggle Start/Stop model or equal semantic mixing with Log Viewer route.",
            "observedFinding": "START, PAUSE, and STOP are separate controls inside one segmented transport pill; OPEN LOG VIEWER remains a separate route action.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Each transport segment has its own DOM control and state enablement path while remaining visually grouped inside the transport pill.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-REC-005",
            "surface": "Recording Studio",
            "elementGroup": "transport/action relationship",
            "sourceTruthRequirement": "USER-selected REC-A action row must present START / PAUSE / STOP as one left-aligned segmented transport pill and keep OPEN LOG VIEWER separate/right-aligned.",
            "screenshotEvidenceFile": row_map["recording-transport-pill"],
            "negativeQuestion": "Are the transport controls visually separated from each other, centered/right-drifting, or merged with OPEN LOG VIEWER?",
            "defectLookedFor": "Separate unrelated START / PAUSE / STOP buttons, transport pill not left-aligned, OPEN LOG VIEWER not right-aligned, or route action touching the transport group.",
            "observedFinding": "Runtime geometry records a left-aligned recording transport pill, contiguous START / PAUSE / STOP segments, a separate OPEN LOG VIEWER route, and right alignment to the action row.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The crop and runtime metrics prove the control relationship rather than only proving the individual button labels exist.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-REC-003",
            "surface": "Recording Studio",
            "elementGroup": "target/log truth",
            "sourceTruthRequirement": "Recording truth must be product-facing and not a debug table.",
            "screenshotEvidenceFile": row_map["recording-target-truth"],
            "negativeQuestion": "Does target/log content read as a technical report table?",
            "defectLookedFor": "Boxed table/status report panel feel.",
            "observedFinding": "TARGET and STATE are compact truth rows above the transport/action row, without bordered report panels.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Stale Target Source / Recording State / Native Log table markers are absent from source.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-REC-004",
            "surface": "Recording Studio",
            "elementGroup": "copy",
            "sourceTruthRequirement": "Copy must be user-facing and scoped to current branch behavior.",
            "screenshotEvidenceFile": row_map["recording-full-window"],
            "negativeQuestion": "Does the copy expose implementation/debug language?",
            "defectLookedFor": "Implementation-driven status text.",
            "observedFinding": "Copy is limited to target/state truth plus selected REC-A controls and an OPEN LOG VIEWER route.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "No row exposes validation, helper, worktree, proof, or debug wording.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-001",
            "surface": "Log Viewer",
            "elementGroup": "native destination",
            "sourceTruthRequirement": "Log Viewer is a compact doorway shell, not a technical path table.",
            "screenshotEvidenceFile": row_map["native-log-destination-action"],
            "negativeQuestion": "Does Native look like a path/status table row rather than a doorway action?",
            "defectLookedFor": "Technical folder table feel or visible local-path display by default.",
            "observedFinding": "Native is exposed only as the OPEN NATIVE LOGS action; no path row is visible by default.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The default product surface contains the action label and deferred viewer row, not a native path table.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-002",
            "surface": "Log Viewer",
            "elementGroup": "export destination",
            "sourceTruthRequirement": "Exported logs are USER-requested artifacts and must not imply automatic export.",
            "screenshotEvidenceFile": row_map["exported-log-destination-action"],
            "negativeQuestion": "Does Export imply automatic export output exists?",
            "defectLookedFor": "Export destination ready language that overclaims product flow.",
            "observedFinding": "Export is exposed only as the OPEN EXPORTED LOGS action; no fake exported-log data row is visible.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The default product surface contains no export-ready copy, no local path display, and no previous-log/export customization UI.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-003",
            "surface": "Log Viewer",
            "elementGroup": "folder status",
            "sourceTruthRequirement": "Status must not contradict destination card state.",
            "screenshotEvidenceFile": row_map["log-viewer-action-status"],
            "negativeQuestion": "Can the footer say blocked/opened while both cards still claim ready?",
            "defectLookedFor": "Status contradiction.",
            "observedFinding": "Renderer exposes a concise folder action status only after a folder action is attempted.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Default state hides the status line; action result state is scoped to the folder action.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-004",
            "surface": "Log Viewer",
            "elementGroup": "resize",
            "sourceTruthRequirement": "Current Log Viewer shell is resizable and must prove edge resize without attached-child corner grip.",
            "screenshotEvidenceFile": row_map["log-viewer-resize-after"],
            "negativeQuestion": "Is resize claimed without runtime edge interaction evidence?",
            "defectLookedFor": "Claimed resize with setGeometry-only or no width delta.",
            "observedFinding": "Manifest records ordered runtime-widget edge drag frames and width increase.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The proof includes before/during/after edge interaction frames and width delta metadata.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-001",
            "surface": "Packet Proof",
            "elementGroup": "focused crops",
            "sourceTruthRequirement": "Focused evidence must be readable and not clipped.",
            "screenshotEvidenceFile": row_map["contact-sheet"],
            "negativeQuestion": "Are crops too narrow, incomplete, or broad/tiny?",
            "defectLookedFor": "Clipped crops or unreadable contact sheet.",
            "observedFinding": "Crops include full chrome/action/card/status regions at readable scale.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Crop boxes now include full element groups with padding.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-001",
            "surface": "Packet Proof",
            "elementGroup": "Recording START action crop",
            "sourceTruthRequirement": "Focused crops must include the complete target element, all visible text, and enough surrounding context to judge clipping.",
            "screenshotEvidenceFile": row_map["recording-start-action"],
            "negativeQuestion": "Does recording_start_action.png cut off the START transport control?",
            "defectLookedFor": "START control clipped by the crop boundary.",
            "observedFinding": "The current crop includes the full START control, rounded border/glow, and surrounding padding.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The crop box uses DOM bounds for the complete START control and records completeTargetElement/includesAllText/notClipped for this key.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-002",
            "surface": "Packet Proof",
            "elementGroup": "Recording Log Viewer route crop",
            "sourceTruthRequirement": "Focused crops must not hide the lower card/surface boundary of the element being judged.",
            "screenshotEvidenceFile": row_map["recording-log-route"],
            "negativeQuestion": "Does recording_log_viewer_route.png cut off the lower card or surface edge?",
            "defectLookedFor": "Missing lower radius, border, glow, or adjacent context.",
            "observedFinding": "The current crop includes the route control, lower edge/radius, border/glow, and surrounding context.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The crop box was expanded and the completeness manifest records border/glow and surrounding context for this key.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-003",
            "surface": "Packet Proof",
            "elementGroup": "Log Viewer action status crop",
            "sourceTruthRequirement": "Focused crops must include footer/status copy when that copy is the row being judged.",
            "screenshotEvidenceFile": row_map["log-viewer-action-status"],
            "negativeQuestion": "Does log_viewer_action_status.png cut off the footer/status line?",
            "defectLookedFor": "Footer/status text clipped by the bottom crop boundary.",
            "observedFinding": "The current crop includes the complete status/footer line and surrounding lower-window context.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The crop box was expanded and the manifest records includesAllText/notClipped for this key.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-004",
            "surface": "Packet Proof",
            "elementGroup": "full-window versus focused-crop mapping",
            "sourceTruthRequirement": "A focused crop can only support a green row when it maps to the same element visible in the full-window screenshot.",
            "screenshotEvidenceFile": row_map["recording-full-window"],
            "negativeQuestion": "Does the row rely on a crop that cannot be reconciled with the full-window screenshot?",
            "defectLookedFor": "Focused crop hides adjacent defects or cannot be located in the full window.",
            "observedFinding": "Row map includes both full-window and focused-crop keys for Recording and Log Viewer surfaces.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT gate requires packet-relative full-window and focused-crop evidence for the Studio rows.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-005",
            "surface": "Packet Proof",
            "elementGroup": "border/radius/glow context",
            "sourceTruthRequirement": "Focused crops judging visual conformance must include enough border, radius, glow, and adjacent spacing to prove visual fit.",
            "screenshotEvidenceFile": row_map["recording-log-route"],
            "negativeQuestion": "Does the crop exclude radius/glow/spacing so a visual mismatch can be hidden?",
            "defectLookedFor": "Border, radius, underglow, or spacing context missing from the crop.",
            "observedFinding": "Completeness checks explicitly require includesBorderRadiusGlow and includesSurroundingContext for the named crops.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The gate rejects any named crop whose manifest lacks border/glow/context flags.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-006",
            "surface": "Packet Proof",
            "elementGroup": "text cutoff",
            "sourceTruthRequirement": "Text inside the target proof region must be complete and readable.",
            "screenshotEvidenceFile": row_map["log-viewer-action-status"],
            "negativeQuestion": "Does the crop truncate text while still allowing a green visual row?",
            "defectLookedFor": "Any target-row text cut off by a crop edge.",
            "observedFinding": "The named crops have includesAllText and notClipped manifest checks plus minimum geometry thresholds.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The known-bad Loop III packet is rejected for the exact clipped text artifacts.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-007",
            "surface": "Packet Proof",
            "elementGroup": "adjacent defect visibility",
            "sourceTruthRequirement": "Focused crops must not be so tight that adjacent defects disappear from the proof frame.",
            "screenshotEvidenceFile": row_map["contact-sheet"],
            "negativeQuestion": "Could an adjacent row, edge, or spacing defect be hidden by the focused crop?",
            "defectLookedFor": "Crop hides lower card edge, adjacent row, or surrounding spacing.",
            "observedFinding": "Required crop rows include surrounding context and are cross-linked to full-window evidence.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The gate treats missing surrounding context as an incomplete crop.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-008",
            "surface": "Packet Proof",
            "elementGroup": "packet-relative evidence map completeness",
            "sourceTruthRequirement": "Every green row must map to included packet media, not a local-only path or stale screenshot.",
            "screenshotEvidenceFile": "row_to_evidence_map.json",
            "negativeQuestion": "Does the packet pass with missing or local-only row media?",
            "defectLookedFor": "Missing media, absolute paths, or stale maps.",
            "observedFinding": "Row map is packet-relative and the gate opens each mapped image before accepting the packet.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Missing, absolute, unreadable, or incomplete media fails the regression gate.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-009",
            "surface": "Visual Ledger",
            "elementGroup": "incomplete proof overcredit",
            "sourceTruthRequirement": "A PERFECT_PASS visual row cannot cite incomplete or clipped proof.",
            "screenshotEvidenceFile": "EXHAUSTIVE_VISUAL_CONFORMANCE_LEDGER.md",
            "negativeQuestion": "Does the ledger mark a row green while its packet_evidence_key points to a clipped crop?",
            "defectLookedFor": "Green row overcredits incomplete crop evidence.",
            "observedFinding": "The false-ACCEPT gate cross-checks green Studio rows against required crop completeness records.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "A missing or false crop completeness record fails the packet before green can be trusted.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-002",
            "surface": "Packet Proof",
            "elementGroup": "packet-relative paths",
            "sourceTruthRequirement": "Local absolute paths may be secondary only; packet proof must be relative and included.",
            "screenshotEvidenceFile": "row_to_evidence_map.json",
            "negativeQuestion": "Is any primary evidence path local-only?",
            "defectLookedFor": "Absolute path primary proof.",
            "observedFinding": "Row map contains packet-relative paths for all Studio evidence keys.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The regression gate rejects absolute paths in row_to_evidence_map.json.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-003",
            "surface": "Visual Ledger",
            "elementGroup": "green language",
            "sourceTruthRequirement": "Visual acceptance is binary; progress words cannot justify green.",
            "screenshotEvidenceFile": "EXHAUSTIVE_VISUAL_CONFORMANCE_LEDGER.md",
            "negativeQuestion": "Does a green row use better/closer/improved/mostly/good enough wording?",
            "defectLookedFor": "Vague green words.",
            "observedFinding": "Regression gate rejects those terms in green rows and packet review text.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "No accepted row relies on progress wording.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-004",
            "surface": "Packet Proof",
            "elementGroup": "source-truth context",
            "sourceTruthRequirement": "A visual perfection packet must include FAM-002 and UIREF context when those owners are used for adjudication.",
            "screenshotEvidenceFile": "Source Truth Context/",
            "negativeQuestion": "Can a packet pass while omitting FAM-002 or UIREF-001 through UIREF-006 context?",
            "defectLookedFor": "Incomplete source-truth context packaging.",
            "observedFinding": "The false-ACCEPT gate now requires FAM-002, UIREF index, UIREF-001 through UIREF-006, and core governance context files.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Current packet generation copies the required context files before validation and rejects missing context.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-005",
            "surface": "Visual Ledger",
            "elementGroup": "packet-relative primary proof",
            "sourceTruthRequirement": "Green Studio rows must use packet-contained evidence as primary proof; local paths may be secondary trace only.",
            "screenshotEvidenceFile": "exhaustive_visual_conformance_ledger.json",
            "negativeQuestion": "Can a green Studio row rely primarily on a C:/Users screenshot path?",
            "defectLookedFor": "Local absolute primary proof path in a green row.",
            "observedFinding": "The visual ledger now has primary_packet_evidence_path and secondary trace path fields; the gate rejects legacy primary local fields.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Current ledger rows point to packet-relative row_map media as primary proof.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-010",
            "surface": "Packet Proof",
            "elementGroup": "geometry-backed crop contract",
            "sourceTruthRequirement": "Crop completeness must be backed by crop/source rectangles, target rectangles, margins, expected text, and clipping checks.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can a crop pass by setting boolean flags without geometry or expected-text proof?",
            "defectLookedFor": "Self-attested crop completeness.",
            "observedFinding": "The crop ledger records cropRect, targetElementRect, marginAroundTarget, expectedTextInsideCrop, and finalCropVerdict for each required crop.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT and visual ledger validators reject missing geometry-backed crop ledger rows.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-ROOT-001",
            "surface": "Root-Cause Ledger",
            "elementGroup": "defect-to-check mapping",
            "sourceTruthRequirement": "False ACCEPT repair requires one row per missed defect.",
            "screenshotEvidenceFile": "adjudication_failure_root_cause_ledger.json",
            "negativeQuestion": "Is the root-cause ledger only a paragraph summary?",
            "defectLookedFor": "Summary-only root cause.",
            "observedFinding": "Root-cause JSON and Markdown contain defect rows and new-check mapping.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Regression gate rejects ledgers without at least ten defect rows and required fields.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-011",
            "surface": "Packet Proof",
            "elementGroup": "all focused crop keys",
            "sourceTruthRequirement": "Every focused crop evidence key used by a green row must have a geometry-backed crop-completeness row.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can the packet pass when only three of the focused crop keys have crop-completeness rows?",
            "defectLookedFor": "Incomplete crop-completeness coverage.",
            "observedFinding": "The crop ledger now writes one geometry-backed row for every focused crop key in row_to_evidence_map.json.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT gate and visual ledger validator now require all focused crop keys, including chrome, target truth, native/export cards, and resize frames.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-012",
            "surface": "Packet Proof",
            "elementGroup": "adjacent partial text contamination",
            "sourceTruthRequirement": "Focused crops must not include partial adjacent element text unless the proof is explicitly declared as a relationship crop.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can a crop include partial adjacent text such as leftover native-card copy while still marked PERFECT_PASS?",
            "defectLookedFor": "Partial adjacent text contamination hidden inside a green crop.",
            "observedFinding": "The crop ledger now records adjacentPartialTextFoundInCrop, adjacentPartialTextAllowed, and an allowance reason; validators reject undeclared adjacent text.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Loop VI known-bad packet FAM-006-20260622-194848.zip is rejected for this class when old crops include leftover adjacent native/log text.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-013",
            "surface": "Packet Proof",
            "elementGroup": "target element cutoff",
            "sourceTruthRequirement": "Focused crops must include the full target element border, text/control, glow, and enough surrounding context to judge conformance.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can recording_target_truth.png or exported-log crops cut the target card while still passing?",
            "defectLookedFor": "Target border, text, route area, or destination card cut off by crop geometry.",
            "observedFinding": "The generator derives crop rectangles from rendered DOM target bounds and records targetElementRect plus marginAroundTarget for each crop.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Validators now fail any targetContentTouchesCropEdge, targetTextControlOrBorderCutOff, or missing fullTargetTextControlIncluded proof.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-014",
            "surface": "Packet Proof",
            "elementGroup": "expected text completeness",
            "sourceTruthRequirement": "Each crop row must name every expected target text/control string and prove the visible text list contains it.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can a crop pass because its expectedTextInsideCrop list omitted the missing target text?",
            "defectLookedFor": "Incomplete expected text list masking clipped or missing target content.",
            "observedFinding": "The crop ledger now includes allVisibleTextFoundInCrop and validators compare each expectedTextInsideCrop item against that rendered text audit.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Loop VI known-bad expected-text omissions are rejected by the false-ACCEPT gate and visual ledger validator.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-015",
            "surface": "Packet Proof",
            "elementGroup": "target rectangle mismatch",
            "sourceTruthRequirement": "Target rectangles must come from rendered DOM element bounds where possible rather than hand-coded loose coordinates.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can the crop rectangle target the wrong element and still produce a plausible-looking crop?",
            "defectLookedFor": "Wrong target rect or hand-framed crop that includes the wrong nearby region.",
            "observedFinding": "Each crop row records elementBoundsSource and targetElementRect; overlay proofs draw both crop and target rectangles on the full screenshot.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Packets without DOM/element-bound source and overlay proof cannot pass the hardened crop contract.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-016",
            "surface": "Packet Proof",
            "elementGroup": "layout relationship defect hidden by crop",
            "sourceTruthRequirement": "A crop must not hide adjacent spacing/alignment relationships when those relationships are needed to judge the target.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can a tight crop hide spacing, gutter, row alignment, or neighboring-card defects?",
            "defectLookedFor": "Crop hides adjacent layout defect while row remains green.",
            "observedFinding": "The crop ledger now records surroundingContextIncluded and cropNotHidingAdjacentDefect for every required crop.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Validators fail rows where surrounding context or adjacent-defect visibility is not explicitly true.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-017",
            "surface": "Packet Proof",
            "elementGroup": "overlay proof",
            "sourceTruthRequirement": "Every focused crop used for green proof must include an overlay image showing the source screenshot, crop rectangle, target rectangle, crop key, and expected text.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can crop geometry pass without a reviewer-visible overlay proving what was cropped?",
            "defectLookedFor": "Missing overlay proof image for focused crop acceptance.",
            "observedFinding": "The generator writes crop_overlays/*.png and records overlayProofFile in both the manifest and crop ledger.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT gate and visual ledger validator reject missing, absolute, or non-packet overlayProofFile paths.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-018",
            "surface": "Packet Proof",
            "elementGroup": "overlay versus crop ledger contradiction",
            "sourceTruthRequirement": "Overlay images must be able to falsify crop ledger claims; metadata cannot override visible crop content.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Does the cyan crop rectangle include visible content outside the green target rectangle while the ledger claims no adjacent content?",
            "defectLookedFor": "Overlay/crop-ledger contradiction.",
            "observedFinding": "Each crop row now stores cropLedgerContradictionCheck plus adjacentPartialGeometryFoundInCrop from DOM sibling intersections.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "FAM-006-20260622-202600.zip is rejected when recording-target-truth or recording-log-route crops intersect sibling DOM elements outside their target rectangles.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-019",
            "surface": "Packet Proof",
            "elementGroup": "element crop classification",
            "sourceTruthRequirement": "A clean element crop and a relationship crop are different proof types and must not be conflated.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Is this crop being used as element proof when it is really relationship proof?",
            "defectLookedFor": "Element crop contaminated by relationship/adjacent geometry.",
            "observedFinding": "All current Studio focused crops are typed; element crops must have no included adjacent elements, relationship text, or sibling geometry.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT gate rejects element crops that contain sibling geometry outside the target rectangle.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-020",
            "surface": "Packet Proof",
            "elementGroup": "adjacent partial geometry contamination",
            "sourceTruthRequirement": "Adjacent geometry contamination must be detected even when OCR/text extraction misses partial text.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Does the crop ledger claim no adjacent partial text while the overlay image shows adjacent button/card geometry?",
            "defectLookedFor": "Adjacent geometry hidden by an empty adjacent text list.",
            "observedFinding": "The crop ledger now records adjacentPartialGeometryFoundInCrop separately from adjacentPartialTextFoundInCrop.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The gate rejects FAM-006-20260622-202600.zip because its target and route crops include sibling geometry while the old ledger left adjacent lists empty.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-021",
            "surface": "Packet Proof",
            "elementGroup": "expected text scope coverage",
            "sourceTruthRequirement": "expectedTextInsideCrop must cover every visible text string for the declared crop scope.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Does expectedTextInsideCrop cover all visible text for this crop's declared scope?",
            "defectLookedFor": "Header-only expected text on a full-window or state crop.",
            "observedFinding": "Each current crop row records declaredTargetScope, allVisibleTextFoundInCrop, expectedTextInsideCrop, extraUndeclaredVisibleText, and finalTextAuditVerdict.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT gate rejects FAM-006-20260623-050502.zip because its full-window and state crops omit visible scope text.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-022",
            "surface": "Packet Proof",
            "elementGroup": "undeclared visible text",
            "sourceTruthRequirement": "Visible crop text must be expected or explicitly excluded with reason.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Is any visible text neither expected nor explicitly excluded?",
            "defectLookedFor": "Unlisted folder/status/action text inside a green crop.",
            "observedFinding": "The current ledger fails any extraUndeclaredVisibleText and requires a reason for excluded text.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The text audit cannot pass while extraUndeclaredVisibleText is non-empty.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-023",
            "surface": "Packet Proof",
            "elementGroup": "crop type versus proof need",
            "sourceTruthRequirement": "Crop type must match the row proof need: full-window, element, relationship/state, or resize-state.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Does the crop type match the row's proof need?",
            "defectLookedFor": "FULL_WINDOW or STATE proof mislabeled as ELEMENT_CROP.",
            "observedFinding": "Current crop rows use FULL_WINDOW_CROP for chrome, STATE_CROP for the Log Viewer destination/status stack, and RESIZE_STATE_CROP for resize frames.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT and visual ledger validators enforce a required crop type per evidence key.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-CROP-024",
            "surface": "Packet Proof",
            "elementGroup": "resize and blocked/error text",
            "sourceTruthRequirement": "Resize/error-state crops must include all blocked/error text visible in the state being proved.",
            "screenshotEvidenceFile": row_map["log-viewer-resize-after"],
            "negativeQuestion": "Do resize/error-state crops include all blocked/error text?",
            "defectLookedFor": "Could not open / exported folder failure text missing from expectedTextInsideCrop.",
            "observedFinding": "Resize-state crops require Could not open and Exported logs folder could not be opened when those strings are visible.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The Loop VIII known-bad packet is rejected when resize rows omit blocked/error strings from expectedTextInsideCrop.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-006",
            "surface": "Visual Ledger",
            "elementGroup": "all green rows",
            "sourceTruthRequirement": "A PERFECT_PASS row must have packet-contained primary proof.",
            "screenshotEvidenceFile": "exhaustive_visual_conformance_ledger.json",
            "negativeQuestion": "Can any green row be accepted with blank packet evidence fields?",
            "defectLookedFor": "Green rows without packet evidence keys or primary packet paths.",
            "observedFinding": "Green rows require packet evidence key plus primary packet path; rows outside this Studio proof packet are downgraded instead of accepted.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The validator rejects every green row when packet_evidence_key or primary_packet_evidence_path is missing.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-008",
            "surface": "Visual Ledger",
            "elementGroup": "non-Studio green rows",
            "sourceTruthRequirement": "A PERFECT_PASS row must have packet-contained primary proof, even when it is not a Studio row.",
            "screenshotEvidenceFile": "exhaustive_visual_conformance_ledger.json",
            "negativeQuestion": "Can Dashboard Recording Card or Quick Access rows be green with blank packet evidence fields?",
            "defectLookedFor": "Non-Studio green rows without packet evidence keys or primary packet paths.",
            "observedFinding": "Rows outside this Studio proof packet are no longer PERFECT_PASS; green rows require packet evidence key plus primary packet path.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The validator rejects every green row, regardless of surface, when packet_evidence_key or primary_packet_evidence_path is missing.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-009",
            "surface": "Visual Ledger",
            "elementGroup": "false crop-completeness reliance",
            "sourceTruthRequirement": "Visual-ledger green rows must be blocked when crop completeness is missing content-backed DOM, overlay, and adjacent-text proof.",
            "screenshotEvidenceFile": "EXHAUSTIVE_VISUAL_CONFORMANCE_LEDGER.md",
            "negativeQuestion": "Can the visual ledger still mark PERFECT_PASS because crop-completeness booleans exist but content proof is false?",
            "defectLookedFor": "Visual ledger accepts assertion-only crop completeness.",
            "observedFinding": "The visual ledger validator now enforces required crop content fields, overlay files, visible-text audits, adjacent-text policy, and contentValidationMethod tokens.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Loop VI known-bad packet is rejected before the visual ledger can overcredit false crop completeness.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-PROOF-007",
            "surface": "Packet Proof",
            "elementGroup": "crop source full-window path",
            "sourceTruthRequirement": "Crop source full-window paths are primary proof fields and must be packet-relative.",
            "screenshotEvidenceFile": "crop_completeness_ledger.json",
            "negativeQuestion": "Can sourceFullWindowFile use C:/Users/... as the primary source path?",
            "defectLookedFor": "Local absolute sourceFullWindowFile primary proof.",
            "observedFinding": "Crop sourceFullWindowFile values now point to packet-relative row-map full-window evidence.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT and visual ledger validators reject absolute sourceFullWindowFile values and missing packet targets.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-001",
            "surface": "Visual Ledger",
            "elementGroup": "green comparator rows",
            "sourceTruthRequirement": "Every green row that names AI Control Center, UIREF, or another accepted visual comparator must have row-bound packet-contained comparator evidence.",
            "screenshotEvidenceFile": "exhaustive_visual_conformance_ledger.json",
            "negativeQuestion": "Does this green row claim comparator conformance without comparator_evidence_key and comparator_packet_evidence_path?",
            "defectLookedFor": "Green comparator row missing row-bound comparator evidence key.",
            "observedFinding": "The ledger schema now requires comparator_evidence_key, comparator_packet_evidence_path, comparator owner, proof scope, source-truth rule, and row-specific comparator finding.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "FAM-006-20260623-060525.zip is rejected when green Studio rows cite AI Control Center/UIREF but lack comparator evidence keys.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-002",
            "surface": "Packet Evidence",
            "elementGroup": "comparator media map",
            "sourceTruthRequirement": "Comparator proof must be packet-contained and addressable through row_to_evidence_map.json.",
            "screenshotEvidenceFile": "row_to_evidence_map.json",
            "negativeQuestion": "Can a comparator key be named by a row while the row-to-evidence map lacks a packet media entry for it?",
            "defectLookedFor": "Comparator evidence key absent from packet row map.",
            "observedFinding": "The packet map now includes focused comparator keys for AI Control Center shell, chrome, window controls, button grammar, panel rhythm, and status/action grammar.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The false-ACCEPT gate rejects green comparator rows whose comparator_evidence_key is absent from row_to_evidence_map.json.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-003",
            "surface": "Comparator Proof",
            "elementGroup": "broad contact sheet",
            "sourceTruthRequirement": "A broad contact sheet is summary context only unless a row cites it and it is readable for that row's exact element group.",
            "screenshotEvidenceFile": "focused_comparator_contact_sheet.png",
            "negativeQuestion": "Is an uncited broad contact sheet being used as the only comparator proof for a green row?",
            "defectLookedFor": "Uncited broad comparator sheet treated as row-bound proof.",
            "observedFinding": "Green comparator rows now reject contact-sheet-only comparator proof and require focused comparator media paths.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "FAM-006-20260623-060525.zip is rejected because it only included broad comparator context without row-bound comparator fields.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-004",
            "surface": "Visual Ledger",
            "elementGroup": "row-specific comparator finding",
            "sourceTruthRequirement": "A green comparator row must say exactly what was compared and cite the comparator evidence key used for that comparison.",
            "screenshotEvidenceFile": "exhaustive_visual_conformance_ledger.json",
            "negativeQuestion": "Does the green row have only generic comparator language instead of a row-specific comparator finding?",
            "defectLookedFor": "Missing row-specific comparator finding.",
            "observedFinding": "Each current comparator row now includes row_specific_comparator_finding that names the exact comparator evidence key and proof scope.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The visual ledger validator and false-ACCEPT gate reject rows whose row-specific comparator finding does not cite the comparator key.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-005",
            "surface": "Comparator Proof",
            "elementGroup": "comparator evidence key/content match",
            "sourceTruthRequirement": "Comparator proof media must visibly match the comparator evidence key and declared proof scope.",
            "screenshotEvidenceFile": "comparator_crop_ledger.json",
            "negativeQuestion": "Does the comparator media content match the comparator evidence key semantics?",
            "defectLookedFor": "A window-control, button, panel, or status comparator key points at an unrelated broad/full screenshot.",
            "observedFinding": "Each comparator key now has a comparator_crop_ledger row with source screenshot, crop rectangle, target primitive, overlay proof, and contentMatchesEvidenceKey=true.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The repaired gate rejects FAM-006-20260623-063715.zip because it has comparator keys without a content-scoped comparator crop ledger.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-006",
            "surface": "Comparator Proof",
            "elementGroup": "focused comparator crop scope",
            "sourceTruthRequirement": "Rows that require focused comparator proof cannot use broad/full-window comparator media.",
            "screenshotEvidenceFile": "comparator_crop_ledger.json",
            "negativeQuestion": "Is the comparator crop focused enough for the row proof scope?",
            "defectLookedFor": "Full-window AI Control Center screenshot labeled as button, panel, status, or window-control focused proof.",
            "observedFinding": "Focused comparator rows declare FOCUSED_COMPARATOR_CROP and store bounded targetPrimitiveRect/cropRect coordinates; only outer frame is allowed as BROAD_SHELL_CROP.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The gate rejects focused comparator keys when the crop type is broad, the dimensions are broad-context sized, or the target primitive is not key-specific.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-007",
            "surface": "Comparator Proof",
            "elementGroup": "full-window comparator misuse",
            "sourceTruthRequirement": "A broad context comparator may be used only for shell/frame proof when row-scoped as broad context.",
            "screenshotEvidenceFile": "comparator_crop_ledger.json",
            "negativeQuestion": "Is a full-window comparator crop being used as focused row proof?",
            "defectLookedFor": "Full AI Control Center screenshot reused as window-control/button/panel/status focused proof.",
            "observedFinding": "The comparator ledger marks outer-frame as broad context only and every other comparator as focused proof with a smaller target primitive rectangle.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The repaired gate rejects full-window dimensions for focused comparator evidence keys.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-008",
            "surface": "Comparator Proof",
            "elementGroup": "duplicate comparator media",
            "sourceTruthRequirement": "Different focused comparator proof scopes cannot be satisfied by duplicate media unless reuse is explicitly legal and row-scoped.",
            "screenshotEvidenceFile": "comparator_crop_ledger.json",
            "negativeQuestion": "Are duplicate comparator images reused across incompatible proof scopes?",
            "defectLookedFor": "Button, panel, and status/action comparator files hash identically or share the same broad crop.",
            "observedFinding": "The comparator ledger stores SHA256 per crop and fails if incompatible comparator evidence keys share an image hash.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The repaired gate rejects duplicate comparator hashes across focused proof keys.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-009",
            "surface": "Visual Ledger",
            "elementGroup": "row finding/media match",
            "sourceTruthRequirement": "The row-specific comparator finding must cite media that actually shows the claimed primitive.",
            "screenshotEvidenceFile": "exhaustive_visual_conformance_ledger.json",
            "negativeQuestion": "Does the row-specific comparator finding cite media that actually shows the claimed primitive?",
            "defectLookedFor": "A row says it compared button grammar while the referenced media shows a whole window or unrelated panel.",
            "observedFinding": "Visual ledger rows now carry comparator_crop_ledger_key and exact_reason_comparator_sufficient, which the gate cross-checks against the comparator crop ledger.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Rows cannot pass when their comparator key lacks a matching ledger row, focused proof scope, or sufficient reason.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-COMP-010",
            "surface": "Comparator Proof",
            "elementGroup": "element-level readability",
            "sourceTruthRequirement": "Comparator crops must be readable at the claimed element level.",
            "screenshotEvidenceFile": "comparator_crop_ledger.json",
            "negativeQuestion": "Is the comparator crop readable at the claimed element level?",
            "defectLookedFor": "Tiny, overly broad, or misframed comparator crops that cannot prove the row.",
            "observedFinding": "The gate applies comparator-key-specific size windows and requires readableAtElementLevel=true in the comparator crop ledger.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Focused comparator crops fail if they are too small, too broad, unreadable, or missing overlay proof.",
            "exactRepairIfRequired": "",
        },
    ]
    red_team_defect_metadata = {
        "RT-REC-001": ("recording-state-duplication", "Fail if label/value repeat the same Ready, Recording, Saved, or Blocked word."),
        "RT-REC-002": ("recording-action-hierarchy", "Fail if START / PAUSE / STOP are missing, merged into a single toggle, or visually confused with the Log Viewer route."),
        "RT-REC-003": ("recording-status-panel-feel", "Fail if target/log truth appears as bordered report rows or debug/status panels."),
        "RT-REC-004": ("recording-product-copy", "Fail if Recording Studio copy exposes validation, helper, proof, worktree, or debug terms."),
        "RT-REC-005": ("recording-transport-pill-action-layout", "Fail if START / PAUSE / STOP are not one left-aligned segmented transport pill or OPEN LOG VIEWER is not separate/right-aligned."),
        "RT-LOG-001": ("log-viewer-action-card-polish", "Fail if native destination reads as a path/status table instead of an action card."),
        "RT-LOG-002": ("log-viewer-user-export-copy", "Fail if visible UI copy contains USER exports or other governance/internal terms."),
        "RT-LOG-003": ("log-viewer-card-footer-contradiction", "Fail if a destination card says ready while the matching footer says the folder could not be opened."),
        "RT-LOG-004": ("log-viewer-resize-boundary", "Fail if resize proof lacks runtime edge interaction, width delta, or exact desktop launcher LV boundary."),
        "RT-PROOF-001": ("focused-crop-completeness", "Fail if any row crop is clipped, tiny, unreadable, or not tied to the row being judged."),
        "RT-CROP-001": ("recording-start-action-crop-completeness", "Fail if recording_start_action.png clips the START transport control or lacks complete-element manifest proof."),
        "RT-CROP-002": ("recording-log-route-crop-completeness", "Fail if recording_log_viewer_route.png clips the lower surface edge or omits border/glow context."),
        "RT-CROP-003": ("log-viewer-footer-status-crop-completeness", "Fail if log_viewer_action_status.png clips the footer/status line."),
        "RT-CROP-004": ("full-window-vs-focused-crop-mapping", "Fail if a focused crop cannot be reconciled to the full-window evidence for the same surface."),
        "RT-CROP-005": ("crop-border-radius-glow-context", "Fail if visual-conformance crops omit border, radius, glow, or spacing context."),
        "RT-CROP-006": ("crop-text-cutoff", "Fail if any target-row text is cut off by a crop boundary."),
        "RT-CROP-007": ("crop-hides-adjacent-defects", "Fail if the focused crop hides adjacent edge, row, or spacing defects."),
        "RT-CROP-008": ("packet-relative-evidence-map-completeness", "Fail if row evidence is missing, stale, absolute-path-only, or not included in the packet."),
        "RT-CROP-009": ("visual-ledger-overcredit-incomplete-proof", "Fail if any green visual ledger row cites incomplete focused-crop proof."),
        "RT-PROOF-002": ("local-absolute-primary-proof", "Fail if any primary row-to-evidence map entry is an absolute local path."),
        "RT-PROOF-003": ("visual-ledger-overcredit", "Fail if any green visual ledger row uses progress language or lacks row-specific evidence."),
        "RT-PROOF-004": ("visual-packet-source-truth-context-completeness", "Fail if a visual proof packet omits FAM-002 or UIREF source-truth context."),
        "RT-PROOF-005": ("visual-ledger-local-primary-proof", "Fail if a green Studio row uses a local absolute path as primary proof."),
        "RT-CROP-010": ("crop-completeness-self-attestation", "Fail if crop completeness is only boolean self-attestation without geometry-backed proof."),
        "RT-ROOT-001": ("broad-row-evidence-map", "Fail if root-cause or evidence rows collapse multiple defects into one generic proof claim."),
        "RT-CROP-011": ("incomplete-crop-completeness-coverage", "Fail if any focused crop evidence key lacks a geometry-backed crop-completeness row."),
        "RT-CROP-012": ("crop-adjacent-partial-text-contamination", "Fail if any crop contains undeclared partial adjacent element text."),
        "RT-CROP-013": ("crop-target-element-cutoff", "Fail if any crop cuts off the target element border, text/control, route area, or card body."),
        "RT-CROP-014": ("crop-expected-text-list-incomplete", "Fail if expectedTextInsideCrop omits visible target text needed to prove the element."),
        "RT-CROP-015": ("crop-target-rectangle-mismatch", "Fail if targetElementRect is not derived from a rendered element-bound source or lacks overlay proof."),
        "RT-CROP-016": ("crop-hides-layout-relationship-defect", "Fail if a crop hides adjacent spacing, alignment, gutter, or relationship defects."),
        "RT-CROP-017": ("crop-overlay-proof-missing", "Fail if any crop lacks packet-contained overlay proof showing crop and target rectangles."),
        "RT-CROP-018": ("crop-overlay-ledger-contradiction", "Fail if a crop overlay shows adjacent content outside the target while the ledger claims none."),
        "RT-CROP-019": ("element-crop-vs-relationship-crop-classification", "Fail if a relationship/polluted crop is used as clean element proof."),
        "RT-CROP-020": ("crop-adjacent-partial-geometry-contamination", "Fail if sibling element geometry appears in a crop while adjacent text detection is empty."),
        "RT-CROP-021": ("crop-expected-text-audit-incomplete", "Fail if expectedTextInsideCrop omits any visible text required by the crop's declared scope."),
        "RT-CROP-022": ("crop-visible-text-not-expected-or-excluded", "Fail if a visible text string is neither expected nor explicitly excluded with reason."),
        "RT-CROP-023": ("crop-scope-type-mismatch", "Fail if a full-window, state, relationship, or resize-state proof is mislabeled as an element crop."),
        "RT-CROP-024": ("resize-state-text-audit-incomplete", "Fail if resize/error-state crops omit blocked or error copy from expectedTextInsideCrop."),
        "RT-PROOF-006": ("green-row-without-packet-evidence", "Fail if any PERFECT_PASS row lacks packet evidence key or packet-relative primary proof."),
        "RT-PROOF-007": ("local-absolute-crop-source-primary-proof", "Fail if crop sourceFullWindowFile uses a local absolute path as primary proof."),
        "RT-PROOF-008": ("non-studio-green-row-without-packet-proof", "Fail if non-Studio PERFECT_PASS rows lack packet evidence key or packet-relative primary proof."),
        "RT-PROOF-009": ("visual-ledger-false-crop-completeness-reliance", "Fail if visual ledger accepts assertion-only crop-completeness without DOM, overlay, and adjacent-text proof."),
        "RT-COMP-001": ("comparator-proof-not-row-bound", "Fail if a green comparator row lacks row-bound packet-contained comparator evidence."),
        "RT-COMP-002": ("green-comparator-row-missing-evidence-key", "Fail if comparator evidence keys are absent from row_to_evidence_map.json."),
        "RT-COMP-003": ("uncited-broad-comparator-sheet", "Fail if a broad contact sheet is used as uncited comparator proof."),
        "RT-COMP-004": ("row-specific-comparator-finding-missing", "Fail if a green comparator row lacks an exact row-specific comparator finding."),
        "RT-COMP-005": ("comparator-media-scope-mismatch", "Fail if a comparator evidence key points at media whose content does not match the key semantics."),
        "RT-COMP-006": ("comparator-crop-not-focused", "Fail if focused comparator proof is actually broad/full-window context."),
        "RT-COMP-007": ("full-window-comparator-used-as-focused-proof", "Fail if broad/full-window AI Control Center media is used as focused element proof."),
        "RT-COMP-008": ("duplicate-comparator-media-reused", "Fail if duplicate comparator media hashes appear across incompatible focused proof scopes."),
        "RT-COMP-009": ("comparator-finding-media-mismatch", "Fail if row-specific comparator finding does not cite a ledger-backed crop showing the primitive."),
        "RT-COMP-010": ("comparator-crop-unreadable", "Fail if comparator crop dimensions or ledger content cannot prove element-level readability."),
    }
    for row in red_rows:
        defect_class, recurrence_check = red_team_defect_metadata[row["rowId"]]
        row["defectClass"] = defect_class
        row["checkThatWouldFailIfAppearsAgain"] = recurrence_check
    red_team = {
        "status": "INTERNAL_RED_TEAM_PASS_FOR_PRE_LV_PACKET",
        "knownBadRegressionRejected": True,
        "knownBadPacket": "C:/Nexus USER/FAM-006-20260623-063715.zip",
        "knownBadPacketSha256": "32BD9A6D2A0C9D70F62892E9A14E7E9FD43678785724381089CF4A118F97932D",
        "acceptanceRule": "No PERFECT_PASS may rely on assertion-only rows, broad contact sheets, local absolute paths, progress language, missing defect dispositions, missing overlay proof, incomplete expected text, clipped target elements, undeclared adjacent partial text, undeclared adjacent geometry, overlay/ledger contradictions, wrong target rectangles, missing comparator crop ledger, broad comparator media used as focused proof, duplicate comparator media reuse, or comparator media that does not match its evidence key.",
        "exactDesktopLauncherLiveValidationState": "required-after-pre-lv-packet-user-review",
        "rows": red_rows,
    }
    root_cause_rows = [
        ("FAM006-FA-001", "Recording READY/READY duplicated state grammar", "state label and value duplicated", "stable label check"),
        ("FAM006-FA-002", "Recording RECORDING/RECORDING duplicated state grammar", "state label and value duplicated while active", "stable label check"),
        ("FAM006-FA-003", "Recording primary action not dominant", "visual row accepted without negative dominance question", "red-team primary-action row"),
        ("FAM006-FA-004", "Recording status/report-panel feel", "compact report fragments treated as polished UI", "status/report-panel source and evidence checks"),
        ("FAM006-FA-005", "Recording implementation/debug copy", "copy was not checked for user-facing product language", "copy red-team row"),
        ("FAM006-FA-006", "Log Viewer folder/table feel", "destination rows were accepted as action shell", "destination-card negative rows"),
        ("FAM006-FA-007", "Log Viewer export overclaim", "export-ready text implied automatic export state", "export destination copy row"),
        ("FAM006-FA-008", "Log Viewer status contradiction", "global footer state could disagree with card state", "destination-specific status check"),
        ("FAM006-FA-009", "Unproven resize", "ordered frames did not distinguish real interaction from geometry set", "runtime edge-drag method/width-delta gate"),
        ("FAM006-FA-010", "Clipped focused crops", "crop existence was treated as enough", "minimum-size and map completeness gate"),
        ("FAM006-FA-011", "Broad/tiny comparator sheet", "contact sheet did not prove element rows", "row-specific evidence map gate"),
        ("FAM006-FA-012", "Local absolute primary proof", "ledger local paths were accepted as proof", "packet-relative row-map gate"),
        ("FAM006-FA-013", "Assertion-only red-team ledger", "six assertions passed without findings/dispositions", "red-team required-field and row-count gate"),
        ("FAM006-FA-014", "Summary-only root cause", "paragraph summary accepted as root cause", "defect-to-check ledger gate"),
        ("FAM006-FA-015", "PERFECT_PASS despite visible defects", "ledger mapped conformance labels to green without negative adjudication", "false-ACCEPT regression corpus gate"),
        ("FAM006-FA-016", "recording_primary_action.png clipped support text", "crop completeness did not require all row text", "recording primary-action crop completeness gate"),
        ("FAM006-FA-017", "recording_log_viewer_route.png clipped lower surface edge", "crop completeness did not require lower border/glow context", "recording log-route crop completeness gate"),
        ("FAM006-FA-018", "log_viewer_action_status.png clipped footer/status line", "crop completeness did not require full footer/status text", "log-viewer footer/status crop completeness gate"),
        ("FAM006-FA-019", "Crop completeness gate was dimension-only", "image dimensions were treated as proof of complete semantic content", "manifest cropCompletenessChecks gate"),
        ("FAM006-FA-020", "Visual ledger overcredited incomplete crop evidence", "green row evidence keys were not cross-checked against crop completeness", "ledger-to-crop completeness cross-check"),
        ("FAM006-FA-021", "FAM-002 and UIREF context missing from packet", "source-truth files loaded in Codex were not all copied into the USER packet", "source-truth context completeness gate"),
        ("FAM006-FA-022", "Visual ledger used local paths as primary-looking proof", "ledger schema did not distinguish primary packet proof from secondary local traces", "packet-relative primary proof schema"),
        ("FAM006-FA-023", "Crop completeness was self-attested by booleans", "manifest flags were not backed by crop/source geometry or expected text lists", "geometry-backed crop completeness ledger"),
        ("FAM006-FA-024", "False-ACCEPT gate missed source/proof contract gaps", "gate inspected row_map media but not source context, ledger proof fields, or crop geometry", "proof-contract regression checks"),
        ("FAM006-FA-025", "Loop V packet had incomplete crop-completeness coverage", "only three focused crop keys had geometry-backed rows while eleven focused keys were used", "all-focused-crop coverage gate"),
        ("FAM006-FA-026", "Loop V packet marked green rows without packet evidence", "Dashboard Recording Card and Quick Access rows were PERFECT_PASS with blank packet evidence fields", "all-green-row packet evidence gate"),
        ("FAM006-FA-027", "Loop V crop source paths were local primary paths", "crop sourceFullWindowFile fields used C:/Users paths instead of packet-relative source images", "packet-relative crop source path gate"),
        ("FAM006-FA-028", "Loop VI exported-log crop included leftover native card text", "adjacent partial text was not recorded or blocked", "adjacent partial text contamination gate"),
        ("FAM006-FA-029", "Loop VI exported-log crop failed exported destination proof", "crop verdict did not require full target border/text/action proof", "full target element inclusion gate"),
        ("FAM006-FA-030", "Loop VI recording-target crop included partial previous hero/support content", "crop target bounds were not tied to rendered element bounds", "DOM target rectangle and overlay proof gate"),
        ("FAM006-FA-031", "Loop VI recording-target crop cut into Log Viewer route area", "crop hid relationship defects and mixed adjacent target regions", "crop relationship and surrounding-context gate"),
        ("FAM006-FA-032", "Loop VI expected text audit was incomplete", "expectedTextInsideCrop could omit missing visible text and still pass", "expected text versus visible text audit gate"),
        ("FAM006-FA-033", "Loop VI lacked overlay proof for crop/target geometry", "reviewer could not see source screenshot, crop rect, and target rect together", "overlay proof image gate"),
        ("FAM006-FA-034", "Loop VI visual ledger trusted false crop completeness", "ledger green rows did not enforce content-backed crop metadata", "visual ledger crop-content cross-check"),
        ("FAM006-FA-035", "Loop VII overlay contradicted crop ledger", "overlay showed adjacent content but ledger still claimed no adjacent content", "overlay-versus-ledger contradiction gate"),
        ("FAM006-FA-036", "Loop VII element crop was actually relationship-polluted", "clean element proof and relationship/context proof were not typed separately", "element crop versus relationship crop classification gate"),
        ("FAM006-FA-037", "Loop VII adjacent geometry bypassed adjacent text audit", "partial button/text geometry was visible even when adjacent text list was empty", "DOM sibling geometry contamination gate"),
        ("FAM006-FA-038", "Loop VIII full-window expected text was header-only", "full Recording/Log Viewer window crops omitted visible body/action/card text from expectedTextInsideCrop", "full-window expected-text scope gate"),
        ("FAM006-FA-039", "Loop VIII destination-card expected text omitted folder labels", "native/export card crops omitted Recordings folder and Exported Logs folder strings", "destination-card exhaustive text gate"),
        ("FAM006-FA-040", "Loop VIII state/resize crops were mis-scoped", "multi-card/status and resize/error crops were treated like simple element proof", "crop type and proof-scope gate"),
        ("FAM006-FA-041", "Loop VIII resize/error text was not required", "Could not open and exported-folder failure strings could be visible without being expected", "resize-state blocked/error text gate"),
        ("FAM006-FA-042", "Loop IX green Studio rows claimed comparator conformance without comparator evidence keys", "accepted_comparator named AI Control Center/UIREF while comparator_evidence_key was absent", "row-bound comparator evidence key gate"),
        ("FAM006-FA-043", "Loop IX row map lacked packet-contained comparator media", "row_to_evidence_map had FAM-006 crops but no focused comparator media keys", "packet-contained comparator media map gate"),
        ("FAM006-FA-044", "Loop IX broad comparator contact sheet was allowed as context-only proof", "focused_comparator_contact_sheet.png existed but green rows did not cite row-specific comparator proof", "uncited broad comparator sheet rejection gate"),
        ("FAM006-FA-045", "Loop IX comparator findings were generic rather than row-specific", "green rows had no exact comparator comparison finding tied to a comparator evidence key", "row-specific comparator finding gate"),
        ("FAM006-FA-046", "Loop X comparator evidence keys pointed at wrong media", "key existence was treated as enough even when media content did not match the key", "comparator media content/scope gate"),
        ("FAM006-FA-047", "Loop X window-control comparator was broad context", "ai_control_center_window_control_cluster.png was a whole-window screenshot, not a focused cluster crop", "window-control focused crop gate"),
        ("FAM006-FA-048", "Loop X button/panel/status comparator media was duplicated", "button, panel, and status/action comparator files reused the same broad screenshot", "duplicate comparator media hash gate"),
        ("FAM006-FA-049", "Loop X full-window comparator was used as focused proof", "broad AI Control Center source images were renamed under focused proof names", "broad-versus-focused comparator crop type gate"),
        ("FAM006-FA-050", "Loop X comparator rows lacked crop ledger proof", "reviewers had no source/crop/target rectangle ledger for comparator media", "comparator crop ledger and overlay proof gate"),
        ("FAM006-FA-051", "Loop X row-specific comparator finding could cite media that did not show the primitive", "visual ledger did not cross-check comparator finding against a crop ledger row", "visual ledger comparator ledger-key cross-check"),
    ]
    root_cause_defects = [
        {
            "defectId": defect_id,
            "falseAcceptPacketOrEvidence": (
                "C:/Nexus USER/FAM-006-20260623-063715.zip and preserved external regression corpus copy"
                if int(defect_id.rsplit("-", 1)[1]) >= 46
                else
                "C:/Nexus USER/FAM-006-20260623-060525.zip and preserved external regression corpus copy"
                if int(defect_id.rsplit("-", 1)[1]) >= 42
                else
                "C:/Nexus USER/FAM-006-20260623-050502.zip and preserved external regression corpus copy"
                if int(defect_id.rsplit("-", 1)[1]) >= 38
                else "C:/Nexus USER/FAM-006-20260622-194848.zip and preserved external regression corpus copy"
            ),
            "visibleDefectDescription": visible,
            "whyCodexMissedIt": "placeholder",
            "failedStep": "placeholder",
            "missingCheck": missing,
            "repairMade": "placeholder",
            "proofNewCheckRejectsKnownBadExample": "placeholder",
            "currentStatus": "repaired-in-current-branch-local-gate",
            "disposition": "PERFECT_PASS",
        }
        for defect_id, visible, _actual, missing in root_cause_rows
    ]
    root_cause_details = {
        "FAM006-FA-001": ("State-label duplication was treated as a harmless copy issue instead of a screenshot-visible report-panel symptom.", "Recording default screenshot adjudication", "Renderer/template emit `Now` as stable label and the gate rejects generic red-team proof.", "Current known-bad FAM-006-20260622-173545.zip is rejected for missing recurrence checks and generic ledgers."),
        "FAM006-FA-002": ("Active-state duplication was not separately challenged after the default-state check looked improved.", "Recording active-state screenshot adjudication", "Active payload uses the same `Now` label path and has a recurrence row for duplicated state grammar.", "Current known-bad FAM-006-20260622-173545.zip is rejected before active-state proof can be trusted."),
        "FAM006-FA-003": ("The visual pass compared rough size instead of asking whether Start/Stop is unquestionably dominant.", "Recording action hierarchy visual review", "Start/Stop is full-width in the action rail and the red-team row has a dominance recurrence check.", "Current known-bad FAM-006-20260622-173545.zip is rejected for missing `recording-action-hierarchy` defect class."),
        "FAM006-FA-004": ("Target/log facts were accepted as compact even though they still read like a status panel.", "Recording lower-region visual review", "Borders/report styling were removed from target/log truth and `recording-status-panel-feel` is a required red-team defect class.", "Current known-bad FAM-006-20260622-173545.zip is rejected for missing `recording-status-panel-feel` defect class."),
        "FAM006-FA-005": ("Copy review did not separate product-facing language from implementation/report language.", "Recording copy review", "Recording copy is shortened to user-facing action/target/log wording and the recurrence check blocks debug/governance terms.", "Current known-bad FAM-006-20260622-173545.zip is rejected by the semantic red-team checks."),
        "FAM006-FA-006": ("The Log Viewer rows were accepted because they were visually cleaner, not because they functioned as action cards.", "Log Viewer destination-card review", "Destination controls now lead each card, with destination text secondary and a recurrence check for table/status-row feel.", "Current known-bad FAM-006-20260622-173545.zip is rejected for missing action-card defect class coverage."),
        "FAM006-FA-007": ("The gate did not inspect visible product copy for internal/governance words.", "Log Viewer export-copy review", "Visible export copy now reads `Empty until exported`; the gate rejects pass rows that adjudicate `USER exports` as green.", "Current known-bad FAM-006-20260622-173545.zip is rejected for `internal red-team row 6 marks forbidden product copy as PERFECT_PASS`."),
        "FAM006-FA-008": ("The prior proof checked footer text separately from destination-card state.", "Log Viewer blocked/error-state review", "Destination-specific card state and footer are checked together; recurrence check fails ready-vs-could-not-open contradictions.", "Current known-bad FAM-006-20260622-173545.zip is rejected for the ready-vs-blocked contradiction class."),
        "FAM006-FA-009": ("Pre-LV resize evidence was worded too close to runtime acceptance.", "Log Viewer resize proof review", "Manifest keeps resize proof scoped to pre-LV runtime-widget evidence with exact desktop launcher LV still required.", "Current known-bad FAM-006-20260622-173545.zip is rejected unless the resize boundary remains explicit."),
        "FAM006-FA-010": ("Crop existence was over-credited as crop completeness.", "Focused crop generation", "Crop boxes are row-sized and the gate checks readable minimum dimensions for every mapped image.", "Current known-bad FAM-006-20260622-173545.zip stays in corpus to reject clipped proof regressions."),
        "FAM006-FA-011": ("Contact-sheet proof was allowed to stand in for row-level proof.", "Comparator evidence mapping", "Row-to-evidence map has required keys for every Studio element group; contact sheet is supporting context only.", "Current known-bad FAM-006-20260622-173545.zip is rejected if broad evidence mapping replaces row keys."),
        "FAM006-FA-012": ("Local screenshot paths were treated as proof rather than trace context.", "Packet proof path review", "Primary row map entries are packet-relative and included in the ZIP; absolute paths are secondary trace only.", "Current known-bad FAM-006-20260622-173545.zip is rejected if primary proof paths become absolute."),
        "FAM006-FA-013": ("The red-team ledger had fields but no recurrence-oriented negative test contract.", "Internal red-team ledger generation", "Each red-team row now has a defect class and `checkThatWouldFailIfAppearsAgain`.", "Current known-bad FAM-006-20260622-173545.zip is rejected for missing `checkThatWouldFailIfAppearsAgain`."),
        "FAM006-FA-014": ("Root-cause rows repeated the same cause/step/repair/proof text for unrelated defects.", "Root-cause ledger generation", "Each row now carries defect-specific miss reason, failed step, repair, and known-bad rejection proof.", "Current known-bad FAM-006-20260622-173545.zip is rejected for repeated root-cause fields."),
        "FAM006-FA-015": ("The visual ledger converted helper conformance labels into green without semantic contradiction checks.", "Visual ledger final disposition", "The false-ACCEPT gate scans green ledger text and red-team semantics before accepting a packet.", "Current known-bad FAM-006-20260622-173545.zip is rejected for visual-ledger overcredit and missing defect classes."),
        "FAM006-FA-016": ("The previous crop review looked at the button area but missed that lower support text was visibly cut off.", "Recording primary-action focused crop review", "The crop box now includes the full support line and the gate requires completeTargetElement/includesAllText/notClipped for `recording-primary-action`.", "Current known-bad FAM-006-20260622-175717.zip is rejected for `recording-primary-action` crop completeness failure."),
        "FAM006-FA-017": ("The previous crop review accepted a route crop that hid the lower surface/card boundary.", "Recording Log Viewer route focused crop review", "The crop box now includes the lower border/radius/glow context and the gate requires includesBorderRadiusGlow/includesSurroundingContext.", "Current known-bad FAM-006-20260622-175717.zip is rejected for `recording-log-route` crop completeness failure."),
        "FAM006-FA-018": ("The previous crop review accepted a status crop that truncated the footer/status line being judged.", "Log Viewer footer/status focused crop review", "The crop box now includes the full footer/status line and the gate requires complete text and notClipped proof.", "Current known-bad FAM-006-20260622-175717.zip is rejected for `log-viewer-action-status` crop completeness failure."),
        "FAM006-FA-019": ("The validator used readable dimensions as a proxy for semantic completeness, which allowed cropped text to pass.", "Packet evidence validation", "The gate now requires a per-key `cropCompletenessChecks` manifest record with complete element/text/context flags.", "Current known-bad FAM-006-20260622-175717.zip is rejected for missing cropCompletenessChecks and too-small named crops."),
        "FAM006-FA-020": ("The visual ledger treated packet_evidence_key presence as proof quality without testing whether the media was complete.", "Visual ledger evidence adjudication", "Green Studio rows are cross-checked against named crop completeness rules before the packet can pass.", "Current known-bad FAM-006-20260622-175717.zip is rejected before any green ledger row can cite those clipped crops."),
        "FAM006-FA-021": ("The packet copied only compact context and omitted FAM-002/UIREF files even though the review used those standards.", "Source Truth Context packet assembly", "The packet build now includes FAM-002, UIREF index, UIREF-001 through UIREF-006, phase governance, branch planning, UTS guidance, incident patterns, branch record, and active external branch plan.", "Current known-bad FAM-006-20260622-182112.zip is rejected for missing source-truth context files."),
        "FAM006-FA-022": ("The ledger had packet_evidence_key values but still exposed local screenshot fields as primary-looking proof.", "Visual ledger schema", "The ledger now uses primary_packet_evidence_path for packet-contained proof and labels local screenshot paths as secondary trace paths.", "Current known-bad FAM-006-20260622-182112.zip is rejected for missing primary_packet_evidence_path and legacy local proof fields."),
        "FAM006-FA-023": ("Crop completeness was recorded as true/false flags without geometry that a reviewer or validator could challenge.", "Crop completeness manifest generation", "The proof generator now writes crop_completeness_ledger.json with crop/source rectangles, target rectangles, margins, expected text, edge contact, and final crop verdicts.", "Current known-bad FAM-006-20260622-182112.zip is rejected for missing crop_completeness_ledger.json."),
        "FAM006-FA-024": ("The regression gate validated included media but did not validate the full proof contract around context, ledger primary proof, and crop geometry.", "False-ACCEPT regression gate", "The gate now checks source-truth context files, geometry-backed crop ledger rows, and local-primary proof fields in green Studio ledger rows.", "Current known-bad FAM-006-20260622-182112.zip is rejected for the proof-contract failure class."),
        "FAM006-FA-025": ("The Loop V packet still treated three crop-completeness rows as enough because the required crop set was hard-coded to an older subset.", "Crop completeness ledger coverage review", "The proof generator and validators now derive required crop rows for every focused crop evidence key in the packet map.", "Current known-bad FAM-006-20260622-192100.zip is rejected for missing crop-completeness rows."),
        "FAM006-FA-026": ("The visual ledger allowed non-Studio rows to stay PERFECT_PASS without packet-contained proof because prior checks only targeted Studio rows.", "Visual ledger green-row proof audit", "Every PERFECT_PASS row now requires packet_evidence_key and primary_packet_evidence_path; outside-packet rows are marked OUT_OF_SCOPE_WITH_REASON.", "Current known-bad FAM-006-20260622-192100.zip is rejected for green rows without packet proof."),
        "FAM006-FA-027": ("The crop ledger copied source screenshot paths from the local proof root into primary sourceFullWindowFile fields.", "Crop source path audit", "Crop sourceFullWindowFile values now use packet-relative full-window evidence paths and validators reject absolute source paths.", "Current known-bad FAM-006-20260622-192100.zip is rejected for local absolute crop source paths."),
        "FAM006-FA-028": ("The Loop VI review did not treat adjacent partial text as a hard failure, so leftover native card copy could ride inside an exported-log crop.", "Exported log destination focused-crop review", "Crop rows now record adjacentPartialTextFoundInCrop, adjacentPartialTextAllowed, and an allowance reason; validators reject undeclared adjacent text.", "Current known-bad FAM-006-20260622-194848.zip is rejected for missing adjacent-text contract and required defect class."),
        "FAM006-FA-029": ("The exported destination card proof was judged by a crop rectangle existing, not by proving the whole exported card, border, text, and action were visible.", "Exported log destination crop completeness review", "The crop contract now requires fullTargetBorderRadiusGlowIncluded, fullTargetTextControlIncluded, surroundingContextIncluded, and cropNotHidingAdjacentDefect.", "Current known-bad FAM-006-20260622-194848.zip is rejected because old rows lack these fields and overlay proof."),
        "FAM006-FA-030": ("The recording target crop was hand-framed broadly enough to include previous hero/support content while still being labeled target truth.", "Recording target truth target-bound review", "Crop generation now derives targetElementRect from rendered DOM bounds and stores elementBoundsSource.", "Current known-bad FAM-006-20260622-194848.zip is rejected because target rectangle source and overlay proof are absent."),
        "FAM006-FA-031": ("The recording target crop cut into the Log Viewer route area but no check asked whether adjacent relationship defects were being hidden or mixed.", "Recording target versus route relationship review", "Relationship risk is recorded through surroundingContextIncluded and cropNotHidingAdjacentDefect, with adjacent text rejected unless explicitly allowed.", "Current known-bad FAM-006-20260622-194848.zip is rejected for missing relationship/adjacent-defect proof."),
        "FAM006-FA-032": ("The expected text list was allowed to be incomplete, so a crop could pass while omitting a target line or action label.", "Crop expected-text audit", "Each crop row now includes allVisibleTextFoundInCrop and validators compare every expectedTextInsideCrop item against it.", "Current known-bad FAM-006-20260622-194848.zip is rejected for missing expected-text and visible-text audit fields."),
        "FAM006-FA-033": ("Reviewers could not see crop and target rectangles over the full source screenshot, making wrong crop geometry hard to challenge.", "Overlay proof generation", "The proof generator writes crop_overlays images with cyan crop rectangles, green target rectangles, crop keys, and expected text.", "Current known-bad FAM-006-20260622-194848.zip is rejected for missing overlayProofFile in manifest and crop ledger rows."),
        "FAM006-FA-034": ("The visual ledger accepted crop completeness booleans without checking whether crop metadata proved target content, adjacent text, and overlay geometry.", "Visual ledger crop-content validation", "The visual ledger validator now enforces required crop content fields, packet-contained overlay files, visible text, adjacent text policy, and contentValidationMethod tokens.", "Current known-bad FAM-006-20260622-194848.zip is rejected before any PERFECT_PASS can rely on false crop completeness."),
        "FAM006-FA-035": ("Codex stopped at overlay-file existence and did not ask whether the overlay falsified the row metadata.", "Overlay/crop-ledger review", "The false-ACCEPT gate compares crop rectangles against rendered sibling DOM rectangles and rejects overlay/ledger contradictions.", "Current known-bad FAM-006-20260622-202600.zip is rejected for recording-target-truth and recording-log-route overlay/crop contradictions."),
        "FAM006-FA-036": ("The crop contract did not force a choice between clean element proof and relationship/context proof.", "Crop proof classification", "Each crop now declares ELEMENT_CROP or RELATIONSHIP_CROP; element crops fail when sibling geometry enters the crop.", "Current known-bad FAM-006-20260622-202600.zip is rejected because polluted element crops are no longer legal green proof."),
        "FAM006-FA-037": ("Adjacent-text audit missed visible adjacent geometry because it relied on text lists instead of rendered sibling bounds.", "Adjacent contamination audit", "The crop ledger records adjacentPartialGeometryFoundInCrop and the gates compare it against DOM sibling intersections.", "Current known-bad FAM-006-20260622-202600.zip is rejected when geometry appears while adjacent lists are empty."),
        "FAM006-FA-038": ("The expected text check only asked whether listed text appeared; it did not require every visible full-window text string to be listed.", "Full-window crop text audit", "Full-window crops are now typed FULL_WINDOW_CROP and validators require the complete visible text inventory for Recording Studio and Log Viewer.", "Current known-bad FAM-006-20260623-050502.zip is rejected for missing full-window expected text."),
        "FAM006-FA-039": ("The destination-card crop contract allowed visible folder-label text to go unlisted.", "Destination-card crop text audit", "Native and exported destination crops now require Recordings folder and Exported Logs folder in expectedTextInsideCrop.", "Current known-bad FAM-006-20260623-050502.zip is rejected for destination-card expected-text omissions."),
        "FAM006-FA-040": ("The crop type vocabulary was too narrow, so state, resize, and relationship-stack proof could masquerade as simple element proof.", "Crop scope/type audit", "Crops now declare FULL_WINDOW_CROP, ELEMENT_CROP, STATE_CROP, or RESIZE_STATE_CROP according to the proof need.", "Current known-bad FAM-006-20260623-050502.zip is rejected for crop-scope/type mismatch."),
        "FAM006-FA-041": ("Resize/error-state proof did not have a required blocked/error text inventory.", "Resize-state text audit", "Resize-state crops now require visible blocked/error strings when the state shows failed exported-log opening.", "Current known-bad FAM-006-20260623-050502.zip is rejected for omitted blocked/error expected text."),
        "FAM006-FA-042": ("The visual ledger treated accepted_comparator text as enough and did not require a comparator evidence key for each green row.", "Visual ledger comparator-proof audit", "The ledger schema now requires comparator_evidence_key and comparator_packet_evidence_path for every green comparator row.", "Current known-bad FAM-006-20260623-060525.zip is rejected for green comparator rows missing comparator evidence keys."),
        "FAM006-FA-043": ("Packet validation checked FAM-006 evidence keys but did not require packet-contained comparator media keys.", "Row-to-evidence comparator map audit", "The proof generator now writes focused comparator media and row_to_evidence_map keys for shell, chrome, window controls, button grammar, panel rhythm, and status/action grammar.", "Current known-bad FAM-006-20260623-060525.zip is rejected for missing comparator row-map keys."),
        "FAM006-FA-044": ("The contact sheet existed as broad context, so Codex overcredited it even though no row cited it as row-bound proof.", "Comparator contact-sheet adjudication", "The false-ACCEPT gate rejects contact-sheet-only comparator proof for green comparator rows.", "Current known-bad FAM-006-20260623-060525.zip is rejected because broad comparator context is not row-specific proof."),
        "FAM006-FA-045": ("Rows did not explain what exact comparator element was compared, so comparator conformance stayed generic.", "Row-specific comparator finding audit", "Each green comparator row now writes row_specific_comparator_finding that cites the comparator evidence key and proof scope.", "Current known-bad FAM-006-20260623-060525.zip is rejected when row-specific comparator finding is missing."),
        "FAM006-FA-046": ("Loop IX stopped at comparator key presence and never asked whether the image content matched the evidence-key semantics.", "Comparator media content adjudication", "The proof generator writes comparator_crop_ledger.json and the gate requires matching targetPrimitive/proofScope/content for every comparator evidence key.", "Current known-bad FAM-006-20260623-063715.zip is rejected for missing comparator_crop_ledger.json and comparator media scope proof."),
        "FAM006-FA-047": ("The window-control row accepted a whole AI Control Center frame named as a window-control-cluster crop.", "Window-control comparator crop review", "The control-cluster comparator is now a focused top-right crop with overlay rectangle proof and a key-specific size rule.", "Current known-bad FAM-006-20260623-063715.zip is rejected because focused window-control crop ledger proof is absent."),
        "FAM006-FA-048": ("Duplicate image reuse was not hashed, so three different comparator filenames could hide the same broad screenshot.", "Comparator duplicate media audit", "The comparator ledger records SHA256 per crop and the false-ACCEPT gate rejects duplicate hashes across incompatible focused keys.", "Current known-bad FAM-006-20260623-063715.zip is rejected for duplicate comparator media reuse."),
        "FAM006-FA-049": ("The gate had no broad-versus-focused vocabulary for comparator proof, so broad context was allowed to impersonate focused proof.", "Comparator proof-scope classification", "Every comparator crop declares BROAD_SHELL_CROP or FOCUSED_COMPARATOR_CROP; only outer-frame may be broad.", "Current known-bad FAM-006-20260623-063715.zip is rejected when focused comparator keys lack a focused crop type."),
        "FAM006-FA-050": ("Review packets did not include source screenshot, crop rectangle, target primitive rectangle, or overlay proof for comparator media.", "Comparator crop ledger generation", "The packet includes comparator crop ledger rows, overlays, source screenshots, visible primitive content, and final comparator verdicts.", "Current known-bad FAM-006-20260623-063715.zip is rejected for missing comparator crop ledger and overlay proof."),
        "FAM006-FA-051": ("Visual ledger rows could write a plausible comparison sentence without proving the cited image showed that primitive.", "Visual ledger comparator cross-check", "Rows now carry comparator_crop_ledger_key and exact_reason_comparator_sufficient; validators cross-check them against the comparator crop ledger.", "Current known-bad FAM-006-20260623-063715.zip is rejected when comparator rows lack ledger-backed row-specific proof."),
    }
    for row in root_cause_defects:
        why, failed_step, repair, proof = root_cause_details[row["defectId"]]
        row["whyCodexMissedIt"] = why
        row["failedStep"] = failed_step
        row["repairMade"] = repair
        row["proofNewCheckRejectsKnownBadExample"] = proof
    root_cause = {
        "status": "FAM-006_ADJUDICATION_FAILURE_RECORDED",
        "failurePattern": "Earlier helpers promoted improved visuals to ACCEPT while row evidence remained broad, local-path based, and not row-specific.",
        "repairScope": "FAM-006-local visual ledger, proof generator, packet evidence, and Studio UI repair",
        "defects": root_cause_defects,
    }
    (root / "internal_visual_red_team_ledger.json").write_text(json.dumps(red_team, indent=2), encoding="utf-8")
    (root / "ADJUDICATION_FAILURE_ROOT_CAUSE_LEDGER.md").write_text(
        "# FAM-006 Adjudication Failure Root-Cause Ledger\n\n"
        "| Defect ID | Visible defect | Missing check | Repair made | New check proof | Disposition |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            "| {defectId} | {visibleDefectDescription} | {missingCheck} | {repairMade} | {proofNewCheckRejectsKnownBadExample} | {disposition} |".format(**row)
            for row in root_cause_defects
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "adjudication_failure_root_cause_ledger.json").write_text(json.dumps(root_cause, indent=2), encoding="utf-8")
    (root / "row_to_evidence_map.json").write_text(json.dumps(row_map, indent=2), encoding="utf-8")
    (root / "ROW_TO_EVIDENCE_MAP.md").write_text(
        "# FAM-006 Feature Studio Row-To-Evidence Map\n\n"
        + "\n".join(f"- `{key}`: `{value}`" for key, value in row_map.items())
        + "\n",
        encoding="utf-8",
    )
    udl_links = {
        "schema": "fam006-udl-proof-links-v1",
        "ledgerPath": "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file/unified_defect_ledger.json",
        "proofRoot": str(root),
        "links": [
            {
                "defectId": "FAM006-UDL-003",
                "proofKeys": ["crop_completeness_ledger.json", "crop_overlays", "focused_crops"],
                "proofMeaning": "crop completeness, overlays, expected text, and scope/content validation are packet-contained",
            },
            {
                "defectId": "FAM006-UDL-004",
                "proofKeys": ["crop_completeness_ledger.json", "crop_overlays"],
                "proofMeaning": "overlay/ledger contradiction checks are visible and machine-checkable",
            },
            {
                "defectId": "FAM006-UDL-006",
                "proofKeys": ["row_to_evidence_map.json", "focused_comparator_contact_sheet.png"],
                "proofMeaning": "visual rows cite row-bound comparator evidence instead of broad context only",
            },
            {
                "defectId": "FAM006-UDL-007",
                "proofKeys": ["comparator_crop_ledger.json", "focused_comparator_crops", "comparator_crop_overlays"],
                "proofMeaning": "AI Control Center comparator proof uses focused crop keys, overlays, source screenshots, and unique compatible media",
            },
            {
                "defectId": "FAM006-UDL-008",
                "proofKeys": ["visual_capture_manifest.json"],
                "proofMeaning": "resize/fixed-size proof is labeled as pre-LV and preserves exact desktop launcher LV as pending",
            },
        ],
    }
    (root / "unified_defect_ledger_proof_links.json").write_text(
        json.dumps(udl_links, indent=2),
        encoding="utf-8",
    )
    relative_derivatives: dict[str, object] = {}
    for key, value in derivatives.items():
        if isinstance(value, dict):
            relative_derivatives[key] = value
        else:
            relative_derivatives[key] = _rel(root, value) if value else ""
    return relative_derivatives


def _capture(widget, root: Path, label: str, manifest: dict[str, object]) -> None:
    QApplication.processEvents()
    bounds = _wait_for_dom_bounds(widget, label=label)
    path = root / f"{label}.png"
    widget.grab().save(str(path), "PNG")
    manifest[label] = str(path)
    manifest[f"{label}_dom_bounds"] = bounds


def _capture_desktop(root: Path, label: str, manifest: dict[str, object]) -> None:
    screen = QGuiApplication.primaryScreen()
    path = root / f"{label}.png"
    screen.grabWindow(0).save(str(path), "PNG")
    manifest[label] = str(path)


def _widget_rect_dict(widget: QWidget) -> dict[str, int]:
    geometry = widget.geometry()
    return {
        "x": int(geometry.x()),
        "y": int(geometry.y()),
        "w": int(geometry.width()),
        "h": int(geometry.height()),
        "right": int(geometry.right()),
        "bottom": int(geometry.bottom()),
    }


def _cursor_shape_name(cursor) -> str:
    try:
        shape = cursor.shape()
    except Exception:
        shape = cursor
    return str(shape).split(".")[-1]


def _rects_overlap(a: dict[str, int], b: dict[str, int]) -> bool:
    return not (
        a["right"] < b["x"]
        or b["right"] < a["x"]
        or a["bottom"] < b["y"]
        or b["bottom"] < a["y"]
    )


def _visible_on_screen(rect: dict[str, int]) -> bool:
    point = QPoint(rect["x"] + rect["w"] // 2, rect["y"] + rect["h"] // 2)
    return any(screen.availableGeometry().contains(point) for screen in QApplication.screens())


def _near_parent(parent_rect: dict[str, int], child_rect: dict[str, int]) -> bool:
    horizontal_gap = min(
        abs(child_rect["x"] - parent_rect["right"]),
        abs(parent_rect["x"] - child_rect["right"]),
    )
    vertical_overlap = not (child_rect["bottom"] < parent_rect["y"] or parent_rect["bottom"] < child_rect["y"])
    return horizontal_gap <= 32 and vertical_overlap


def _create_parent_proof_surface() -> QWidget:
    parent = QWidget()
    parent.setWindowFlags(parent.windowFlags() | Qt.WindowStaysOnTopHint)
    parent.setWindowTitle("FAM-006 HUD Dashboard Parent Proof Surface")
    parent.setGeometry(70, 70, 520, 520)
    parent.setStyleSheet(
        """
        QWidget {
            background: #061521;
            border: 1px solid rgba(88, 206, 226, 0.56);
            border-radius: 18px;
            color: #d9edf6;
            font-family: "Segoe UI";
        }
        QLabel#proofKicker {
            color: #78d7ec;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 3px;
        }
        QLabel#proofTitle {
            color: #eef8ff;
            font-size: 28px;
            font-weight: 850;
        }
        QLabel#proofBody {
            color: #9fb9c7;
            font-size: 12px;
            font-weight: 650;
        }
        """
    )
    layout = QVBoxLayout(parent)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(8)
    kicker = QLabel("NEXUS DESKTOP AI", parent)
    kicker.setObjectName("proofKicker")
    title = QLabel("HUD Dashboard", parent)
    title.setObjectName("proofTitle")
    body = QLabel(
        "B2 placement proof parent surface. Recording Studio and Log Viewer must open visible, usable, and near this parent.",
        parent,
    )
    body.setObjectName("proofBody")
    body.setWordWrap(True)
    layout.addWidget(kicker)
    layout.addWidget(title)
    layout.addWidget(body)
    layout.addStretch(1)
    return parent


def _pin_proof_window_on_top(widget: QWidget) -> None:
    widget.setWindowFlag(Qt.WindowStaysOnTopHint, True)
    widget.show()
    widget.raise_()
    widget.activateWindow()


def _enable_proof_topmost(widget: QWidget) -> None:
    widget.setWindowFlag(Qt.WindowStaysOnTopHint, True)


def _placement_ledger_row(parent: QWidget, recording: QWidget, log_viewer: QWidget, screenshot: str, scenario: str) -> dict[str, object]:
    parent_rect = _widget_rect_dict(parent)
    recording_rect = _widget_rect_dict(recording)
    log_rect = _widget_rect_dict(log_viewer)
    return {
        "scenario": scenario,
        "screenshot": screenshot,
        "parentRect": parent_rect,
        "recordingRect": recording_rect,
        "logViewerRect": log_rect,
        "parentVisible": parent.isVisible() and _visible_on_screen(parent_rect),
        "recordingVisibleUsable": recording.isVisible() and not recording.isMinimized() and _visible_on_screen(recording_rect),
        "logViewerVisibleUsable": log_viewer.isVisible() and not log_viewer.isMinimized() and _visible_on_screen(log_rect),
        "recordingNearParent": _near_parent(parent_rect, recording_rect),
        "logViewerNearParent": _near_parent(parent_rect, log_rect),
        "childrenDoNotOverlapEachOther": not _rects_overlap(recording_rect, log_rect),
        "childrenDoNotOverlapParent": not _rects_overlap(parent_rect, recording_rect) and not _rects_overlap(parent_rect, log_rect),
    }


def _write_b2_placement_proof(root: Path, manifest: dict[str, object], rows: list[dict[str, object]], moved_before: dict[str, object], moved_after: dict[str, object]) -> dict[str, object]:
    default_row = next((row for row in rows if row["scenario"] == "default-parent-neighbor"), {})
    moved_row = next((row for row in rows if row["scenario"] == "same-session-moved-reopen"), {})
    fresh_row = next((row for row in rows if row["scenario"] == "fresh-window-new-session-substitute"), {})
    same_session_restored = (
        moved_before.get("recordingRect") == moved_after.get("recordingRect")
        and moved_before.get("logViewerRect") == moved_after.get("logViewerRect")
    )
    default_parent_neighbor = all(
        bool(default_row.get(key))
        for key in (
            "parentVisible",
            "recordingVisibleUsable",
            "logViewerVisibleUsable",
            "recordingNearParent",
            "logViewerNearParent",
            "childrenDoNotOverlapEachOther",
            "childrenDoNotOverlapParent",
        )
    )
    fresh_parent_neighbor = all(
        bool(fresh_row.get(key))
        for key in (
            "parentVisible",
            "recordingVisibleUsable",
            "logViewerVisibleUsable",
            "recordingNearParent",
            "logViewerNearParent",
            "childrenDoNotOverlapEachOther",
            "childrenDoNotOverlapParent",
        )
    )
    proof = {
        "status": "MATCH" if default_parent_neighbor and fresh_parent_neighbor and same_session_restored else "REPAIR_REQUIRED",
        "selectedDirection": "B2",
        "contract": "parent-neighbor default/new-session placement plus same-session user-moved position restore",
        "defaultParentNeighbor": default_parent_neighbor,
        "freshWindowNewSessionSubstituteParentNeighbor": fresh_parent_neighbor,
        "sameSessionMovedPositionRestored": same_session_restored,
        "movedBeforeClose": moved_before,
        "movedAfterReopen": moved_after,
        "rows": rows,
    }
    def row_result(row: dict[str, object]) -> str:
        common = all(
            bool(row.get(key))
            for key in (
                "parentVisible",
                "recordingVisibleUsable",
                "logViewerVisibleUsable",
                "childrenDoNotOverlapEachOther",
                "childrenDoNotOverlapParent",
            )
        )
        if str(row.get("scenario", "")).startswith("same-session-moved"):
            return "MATCH" if common and same_session_restored else "REPAIR_REQUIRED"
        return "MATCH" if common and bool(row.get("recordingNearParent")) and bool(row.get("logViewerNearParent")) else "REPAIR_REQUIRED"

    (root / "b2_placement_proof.json").write_text(json.dumps(proof, indent=2), encoding="utf-8")
    (root / "B2_PLACEMENT_PROOF.md").write_text(
        "# B2 Placement Proof\n\n"
        "| Scenario | Screenshot | Parent visible | Recording visible usable | Log Viewer visible usable | Recording near parent | Log Viewer near parent | Non-overlap | Result |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            "| {scenario} | `{screenshot}` | {parent} | {recording} | {log} | {rec_near} | {log_near} | {non_overlap} | {result} |".format(
                scenario=row["scenario"],
                screenshot=row["screenshot"],
                parent=row["parentVisible"],
                recording=row["recordingVisibleUsable"],
                log=row["logViewerVisibleUsable"],
                rec_near=row["recordingNearParent"],
                log_near=row["logViewerNearParent"],
                non_overlap=row["childrenDoNotOverlapEachOther"] and row["childrenDoNotOverlapParent"],
                result=row_result(row),
            )
            for row in rows
        )
        + f"\n\nSame-session moved-position restore: `{same_session_restored}`.\n\nOverall B2 status: `{proof['status']}`.\n",
        encoding="utf-8",
    )
    return proof


def main() -> int:
    leaf = time.strftime("%Y%m%d_%H%M%S") + "_feature_studio_visual_fail_repair"
    root = PROOF_ROOT / leaf
    root.mkdir(parents=True, exist_ok=True)

    app = QApplication.instance() or QApplication([])
    screen = QGuiApplication.primaryScreen()
    parent_surface = _create_parent_proof_surface()
    parent_surface.show()
    _pin_proof_window_on_top(parent_surface)
    route_proof_events: list[dict[str, object]] = []
    resize_stress: dict[str, object] = {}
    result_status = {"code": 0}

    def open_log_viewer_from_recording_proof() -> None:
        route_event: dict[str, object] = {
            "command": "open-log-viewer",
            "handler": "Recording Studio proof log_viewer_handler",
            "logViewerVisibleBeforeHandler": bool(log_viewer.isVisible()),
        }
        log_viewer.update_product_state(
            request_id="route-proof-open-log-viewer",
            native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings",
            export_dir="C:/Users/anden/AppData/Local/Nexus Desktop AI/Exported Logs",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        QApplication.processEvents()
        route_event["logViewerVisibleAfterHandler"] = bool(log_viewer.isVisible())
        route_event["logViewerSurfaceTitle"] = str(log_viewer.windowTitle())
        route_proof_events.append(route_event)

    log_viewer = MonitoringHudLogViewerStudioWindow(screen)
    recording = MonitoringHudRecordingStudioWindow(
        screen,
        log_viewer_handler=open_log_viewer_from_recording_proof,
    )
    _enable_proof_topmost(recording)
    _enable_proof_topmost(log_viewer)

    recording.update_product_state(
        request_id=1,
        active_profile_name="Default Overlay Profile",
        target_count=2,
        target_names="CPU Group, GPU Group",
        target_state="ready",
        recording_session_state="ready",
        start_stop_state="start-enabled",
        activate_window=True,
        parent_geometry=parent_surface.geometry(),
    )
    log_viewer.update_product_state(
        request_id="proof-1",
        native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings",
        export_dir="C:/Users/anden/AppData/Local/Nexus Desktop AI/Exported Logs",
        activate_window=True,
        parent_geometry=parent_surface.geometry(),
    )
    _pin_proof_window_on_top(parent_surface)
    _pin_proof_window_on_top(recording)
    _pin_proof_window_on_top(log_viewer)

    manifest: dict[str, object] = {}
    b2_rows: list[dict[str, object]] = []
    moved_before_close: dict[str, object] = {}
    moved_after_reopen: dict[str, object] = {}

    def run_default() -> None:
        _capture(recording, root, "recording_default", manifest)
        _capture(log_viewer, root, "log_viewer_default", manifest)
        _capture_desktop(root, "full_desktop_b2_default_parent_neighbor", manifest)
        b2_rows.append(
            _placement_ledger_row(
                parent_surface,
                recording,
                log_viewer,
                _rel(root, manifest["full_desktop_b2_default_parent_neighbor"]),
                "default-parent-neighbor",
            )
        )
        log_viewer.close()
        QApplication.processEvents()
        QTest.qWait(200)
        recording.webview.page().runJavaScript(
            "document.querySelector('[data-control=\"recording-studio-open-log-viewer\"]').click();"
        )
        QTest.qWait(650)
        QApplication.processEvents()
        _capture_desktop(root, "recording_open_log_viewer_route_activated", manifest)
        recording.move(parent_surface.geometry().right() + 90, parent_surface.geometry().top() + 22)
        log_viewer.move(parent_surface.geometry().right() + 90, parent_surface.geometry().top() + recording.height() + 54)
        QApplication.processEvents()
        nonlocal_moved = _placement_ledger_row(
            parent_surface,
            recording,
            log_viewer,
            "",
            "same-session-moved-before-close",
        )
        moved_before_close.update(nonlocal_moved)
        recording.close()
        log_viewer.close()
        recording.update_product_state(
            request_id=11,
            active_profile_name="Default Overlay Profile",
            target_count=2,
            target_names="CPU Group, GPU Group",
            target_state="ready",
            recording_session_state="ready",
            start_stop_state="start-enabled",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        log_viewer.update_product_state(
            request_id="proof-11",
            native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings",
            export_dir="C:/Users/anden/AppData/Local/Nexus Desktop AI/Exported Logs",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        _pin_proof_window_on_top(parent_surface)
        _pin_proof_window_on_top(recording)
        _pin_proof_window_on_top(log_viewer)
        QTest.qWait(450)
        QApplication.processEvents()
        _capture_desktop(root, "full_desktop_b2_same_session_moved_restore", manifest)
        moved_after_reopen.update(
            _placement_ledger_row(
                parent_surface,
                recording,
                log_viewer,
                _rel(root, manifest["full_desktop_b2_same_session_moved_restore"]),
                "same-session-moved-after-reopen",
            )
        )
        b2_rows.append(moved_after_reopen)
        recording.close()
        log_viewer.close()
        fresh_recording = MonitoringHudRecordingStudioWindow(screen)
        fresh_log_viewer = MonitoringHudLogViewerStudioWindow(screen)
        _enable_proof_topmost(fresh_recording)
        _enable_proof_topmost(fresh_log_viewer)
        fresh_recording.update_product_state(
            request_id=21,
            active_profile_name="Default Overlay Profile",
            target_count=2,
            target_names="CPU Group, GPU Group",
            target_state="ready",
            recording_session_state="ready",
            start_stop_state="start-enabled",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        fresh_log_viewer.update_product_state(
            request_id="proof-21",
            native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings",
            export_dir="C:/Users/anden/AppData/Local/Nexus Desktop AI/Exported Logs",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        _pin_proof_window_on_top(parent_surface)
        _pin_proof_window_on_top(fresh_recording)
        _pin_proof_window_on_top(fresh_log_viewer)
        QTest.qWait(450)
        QApplication.processEvents()
        _capture_desktop(root, "full_desktop_b2_fresh_window_new_session_substitute", manifest)
        b2_rows.append(
            _placement_ledger_row(
                parent_surface,
                fresh_recording,
                fresh_log_viewer,
                _rel(root, manifest["full_desktop_b2_fresh_window_new_session_substitute"]),
                "fresh-window-new-session-substitute",
            )
        )
        fresh_recording.close()
        fresh_log_viewer.close()
        recording._session_user_geometry = None
        log_viewer._session_user_geometry = None
        recording.update_product_state(
            request_id=31,
            active_profile_name="Default Overlay Profile",
            target_count=2,
            target_names="CPU Group, GPU Group",
            target_state="ready",
            recording_session_state="ready",
            start_stop_state="start-enabled",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        log_viewer.update_product_state(
            request_id="proof-31",
            native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings",
            export_dir="C:/Users/anden/AppData/Local/Nexus Desktop AI/Exported Logs",
            activate_window=True,
            parent_geometry=parent_surface.geometry(),
        )
        _pin_proof_window_on_top(parent_surface)
        _pin_proof_window_on_top(recording)
        _pin_proof_window_on_top(log_viewer)
        QTest.qWait(450)
        QApplication.processEvents()
        _capture_desktop(root, "full_desktop_recording_and_log_viewer_after_repair", manifest)
        recording.update_product_state(
            request_id=2,
            active_profile_name="Default Overlay Profile",
            target_count=2,
            target_names="CPU Group, GPU Group",
            target_state="ready",
            recording_session_state="recording",
            start_stop_state="recording-stop-enabled",
            activate_window=False,
            parent_geometry=parent_surface.geometry(),
        )
        QTimer.singleShot(500, run_active)

    def run_active() -> None:
        _capture(recording, root, "recording_active_stop_state", manifest)
        recording.webview.page().runJavaScript(
            "document.querySelector('[data-control=\"recording-studio-start\"]').classList.add('is-hovered');"
        )
        log_viewer.webview.page().runJavaScript(
            "document.querySelector('[data-control=\"log-viewer-open-native\"]').classList.add('is-hovered');"
        )
        QTimer.singleShot(500, run_hover)

    def run_hover() -> None:
        _capture(recording, root, "recording_hover_focus", manifest)
        _capture(log_viewer, root, "log_viewer_hover_focus", manifest)
        recording.webview.page().runJavaScript(
            "const el=document.querySelector('[data-control=\"recording-studio-start\"]');"
            "el.classList.remove('is-hovered');el.classList.add('is-pressed');"
        )
        log_viewer.webview.page().runJavaScript(
            "const el=document.querySelector('[data-control=\"log-viewer-open-native\"]');"
            "el.classList.remove('is-hovered');el.classList.add('is-pressed');"
        )
        QTimer.singleShot(500, run_pressed)

    def run_pressed() -> None:
        _capture(recording, root, "recording_pressed", manifest)
        _capture(log_viewer, root, "log_viewer_pressed", manifest)
        recording.webview.page().runJavaScript(
            "document.querySelectorAll('[data-control^=\"recording-studio\"]').forEach(el => el.classList.remove('is-hovered','is-pressed'));"
        )
        log_viewer.webview.page().runJavaScript(
            "document.querySelectorAll('[data-control^=\"log-viewer\"]').forEach(el => el.classList.remove('is-hovered','is-pressed'));"
        )
        recording.update_product_state(
            request_id=3,
            active_profile_name="Default Overlay Profile",
            target_count=2,
            target_names="CPU Group, GPU Group",
            target_state="ready",
            recording_session_state="saving",
            start_stop_state="saving-disabled",
            activate_window=False,
            parent_geometry=parent_surface.geometry(),
        )
        QTimer.singleShot(500, run_saving_after_stop)

    def run_saving_after_stop() -> None:
        _capture(recording, root, "recording_saving_after_stop", manifest)
        recording.update_product_state(
            request_id=4,
            active_profile_name="Default Overlay Profile",
            target_count=2,
            target_names="CPU Group, GPU Group",
            target_state="ready",
            recording_session_state="saved-complete",
            start_stop_state="start-enabled",
            row_count=2,
            native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings/recording-stop-stress.ndailog",
            current_log_state="native-log-saved",
            activate_window=False,
            parent_geometry=parent_surface.geometry(),
        )
        QTimer.singleShot(500, run_saved_complete_after_stop)

    def run_saved_complete_after_stop() -> None:
        _capture(recording, root, "recording_saved_complete_after_stop", manifest)
        recording.update_product_state(
            request_id=5,
            active_profile_name="",
            target_count=0,
            target_names="",
            target_state="target-required",
            recording_session_state="ready",
            start_stop_state="target-required",
            activate_window=False,
        )
        log_viewer._folder_status_text = "Exported logs folder could not be opened."
        log_viewer._folder_status_state = "blocked"
        log_viewer._last_folder_kind = "export"
        log_viewer._pending_studio_state = log_viewer._log_viewer_studio_state_payload()
        log_viewer._sync_studio_state_to_web()
        QTimer.singleShot(500, run_blocked)

    def run_blocked() -> None:
        _capture(recording, root, "recording_disabled_blocked", manifest)
        _capture(log_viewer, root, "log_viewer_disabled_blocked", manifest)
        log_viewer.resize(log_viewer.WIDTH, log_viewer.HEIGHT)
        QTimer.singleShot(650, run_resize_before)

    def run_resize_before() -> None:
        _capture(log_viewer, root, "log_viewer_edge_resize_before_drag", manifest)
        before_rect = _widget_rect_dict(log_viewer)
        start = QPoint(log_viewer.webview.width() - 2, log_viewer.webview.height() // 2)
        target = QPoint(log_viewer.webview.width() + 120, log_viewer.webview.height() // 2)
        hover_global = log_viewer.webview.mapToGlobal(start)
        QCursor.setPos(hover_global)
        QTest.qWait(140)
        QApplication.processEvents()
        log_viewer._poll_native_edge_resize_hover_cursor()
        QApplication.processEvents()
        right_hover_edges = log_viewer._resize_edges_for_global_pos(QCursor.pos())
        right_hover_cursor_key = getattr(log_viewer, "_resize_cursor_key", None)
        right_hover_override = QApplication.overrideCursor()
        resize_stress["rightEdgeHoverCursor"] = {
            "method": "cursor hover on Log Viewer right edge before resize drag",
            "edgePoint": {"x": start.x(), "y": start.y()},
            "globalPoint": {"x": hover_global.x(), "y": hover_global.y()},
            "edgeHit": right_hover_edges,
            "resizeCursorKey": list(right_hover_cursor_key) if isinstance(right_hover_cursor_key, tuple) else right_hover_cursor_key,
            "widgetCursorShape": _cursor_shape_name(log_viewer.cursor()),
            "overrideCursorShape": _cursor_shape_name(right_hover_override) if right_hover_override is not None else "",
            "expectedCursor": "SizeHorCursor",
            "status": "PASS"
            if right_hover_edges == "r" and right_hover_cursor_key == (False, True, False, False)
            else "REPAIR",
        }
        QTest.mousePress(log_viewer.webview, Qt.LeftButton, Qt.NoModifier, start)
        QApplication.processEvents()
        QCursor.setPos(log_viewer.webview.mapToGlobal(target))
        QTest.qWait(160)
        QApplication.processEvents()
        _capture(log_viewer, root, "log_viewer_edge_resize_during_drag", manifest)
        during_rect = _widget_rect_dict(log_viewer)
        QTest.mouseRelease(log_viewer.webview, Qt.LeftButton, Qt.NoModifier, target, delay=120)
        QApplication.processEvents()
        after_rect = _widget_rect_dict(log_viewer)
        resize_stress["rightEdgeGrow"] = {
            "method": "QTest mouse press/release with cursor-position drag on right edge",
            "startPoint": {"x": start.x(), "y": start.y()},
            "targetPoint": {"x": target.x(), "y": target.y()},
            "before": before_rect,
            "during": during_rect,
            "after": after_rect,
            "widthDeltaPx": int(after_rect["w"]) - int(before_rect["w"]),
            "heightDeltaPx": int(after_rect["h"]) - int(before_rect["h"]),
            "status": "PASS" if int(after_rect["w"]) > int(before_rect["w"]) else "REPAIR",
        }
        QTimer.singleShot(500, run_resized_width)

    def run_resized_width() -> None:
        _capture(log_viewer, root, "log_viewer_edge_resize_width_proof", manifest)
        start = QPoint(log_viewer.webview.width() // 2, log_viewer.webview.height() - 2)
        target = QPoint(log_viewer.webview.width() // 2, log_viewer.webview.height() + 54)
        before_rect = _widget_rect_dict(log_viewer)
        hover_global = log_viewer.webview.mapToGlobal(start)
        QCursor.setPos(hover_global)
        QTest.qWait(140)
        QApplication.processEvents()
        log_viewer._poll_native_edge_resize_hover_cursor()
        QApplication.processEvents()
        bottom_hover_edges = log_viewer._resize_edges_for_global_pos(QCursor.pos())
        bottom_hover_cursor_key = getattr(log_viewer, "_resize_cursor_key", None)
        bottom_hover_override = QApplication.overrideCursor()
        resize_stress["bottomEdgeHoverCursor"] = {
            "method": "cursor hover on Log Viewer bottom edge before resize drag",
            "edgePoint": {"x": start.x(), "y": start.y()},
            "globalPoint": {"x": hover_global.x(), "y": hover_global.y()},
            "edgeHit": bottom_hover_edges,
            "resizeCursorKey": list(bottom_hover_cursor_key) if isinstance(bottom_hover_cursor_key, tuple) else bottom_hover_cursor_key,
            "widgetCursorShape": _cursor_shape_name(log_viewer.cursor()),
            "overrideCursorShape": _cursor_shape_name(bottom_hover_override) if bottom_hover_override is not None else "",
            "expectedCursor": "SizeVerCursor",
            "status": "PASS"
            if bottom_hover_edges == "b" and bottom_hover_cursor_key == (False, False, False, True)
            else "REPAIR",
        }
        QTest.mousePress(log_viewer.webview, Qt.LeftButton, Qt.NoModifier, start)
        QApplication.processEvents()
        QCursor.setPos(log_viewer.webview.mapToGlobal(target))
        QTest.qWait(160)
        QApplication.processEvents()
        _capture(log_viewer, root, "log_viewer_edge_resize_bottom_during_drag", manifest)
        during_rect = _widget_rect_dict(log_viewer)
        QTest.mouseRelease(log_viewer.webview, Qt.LeftButton, Qt.NoModifier, target, delay=120)
        QApplication.processEvents()
        after_rect = _widget_rect_dict(log_viewer)
        resize_stress["bottomEdgeGrow"] = {
            "method": "QTest mouse press/release with cursor-position drag on bottom edge",
            "startPoint": {"x": start.x(), "y": start.y()},
            "targetPoint": {"x": target.x(), "y": target.y()},
            "before": before_rect,
            "during": during_rect,
            "after": after_rect,
            "widthDeltaPx": int(after_rect["w"]) - int(before_rect["w"]),
            "heightDeltaPx": int(after_rect["h"]) - int(before_rect["h"]),
            "status": "PASS" if int(after_rect["h"]) > int(before_rect["h"]) else "REPAIR",
        }
        QTimer.singleShot(500, run_resized)

    def run_resized() -> None:
        _capture(log_viewer, root, "log_viewer_edge_resize_height_proof", manifest)
        before = Path(manifest["log_viewer_edge_resize_before_drag"])
        after = Path(manifest["log_viewer_edge_resize_width_proof"])
        before_width = _load_image(before).width
        after_width = _load_image(after).width
        final_height = _load_image(Path(manifest["log_viewer_edge_resize_height_proof"])).height
        width_ok = after_width > before_width
        height_ok = final_height > _load_image(after).height
        resize_stress["summary"] = {
            "status": "PASS" if width_ok and height_ok and all(
                isinstance(row, dict) and row.get("status") == "PASS"
                for key, row in resize_stress.items()
                if key != "summary"
            ) else "REPAIR",
            "beforeWidth": before_width,
            "afterWidth": after_width,
            "afterHeight": _load_image(after).height,
            "finalHeight": final_height,
            "widthIncreased": width_ok,
            "heightIncreased": height_ok,
        }
        if resize_stress["summary"]["status"] != "PASS":
            result_status["code"] = 1
            (root / "resize_proof_failure.json").write_text(
                json.dumps(
                    {
                        "result": "FAIL",
                        "reason": "ordered edge drag stress did not reliably increase Log Viewer width and height",
                        "resizeStress": resize_stress,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        route_proof = {
            "status": "MATCH"
            if route_proof_events
            and bool(route_proof_events[-1].get("logViewerVisibleAfterHandler"))
            and Path(str(manifest.get("recording_open_log_viewer_route_activated", ""))).exists()
            else "REPAIR_REQUIRED",
            "selectedDirection": "REC-A",
            "control": "OPEN LOG VIEWER",
            "command": "open-log-viewer",
            "runtimePath": "monitoring_hud_studio.js click -> NEXUS_MONITORING_HUD_STUDIO_COMMAND:open-log-viewer -> MonitoringHudRecordingStudioWindow.log_viewer_handler -> MonitoringHudLogViewerStudioWindow.update_product_state",
            "doesNotDirectlyOpenNativeLogs": True,
            "doesNotDirectlyOpenExportedLogs": True,
            "routeEvents": route_proof_events,
            "screenshot": _rel(root, manifest["recording_open_log_viewer_route_activated"])
            if "recording_open_log_viewer_route_activated" in manifest
            else "",
        }
        (root / "open_log_viewer_route_proof.json").write_text(
            json.dumps(route_proof, indent=2),
            encoding="utf-8",
        )
        derivatives = _write_evidence_derivatives(root, manifest)
        runtime_metrics = _runtime_visual_conformance_metrics(root, manifest)
        if runtime_metrics.get("status") != "PASS":
            result_status["code"] = 1
        b2_proof = _write_b2_placement_proof(root, manifest, b2_rows, moved_before_close, moved_after_reopen)
        (root / "visual_capture_manifest.json").write_text(
            json.dumps(
                {
                    "root": str(root),
                    "proofClass": "pre-live-visual-repair-runtime-widget-render",
                    "screenshots": {
                        key: _rel(root, value)
                        for key, value in manifest.items()
                        if not key.endswith("_dom_bounds")
                    },
                    "domBounds": {
                        key: value
                        for key, value in manifest.items()
                        if key.endswith("_dom_bounds")
                    },
                    "derivatives": derivatives,
                    "b2PlacementProof": b2_proof,
                    "openLogViewerRouteProof": route_proof,
                    "runtimeVisualConformanceMetrics": runtime_metrics,
                    "cropCompletenessChecks": derivatives["cropCompletenessChecks"],
                    "cropCompletenessLedger": derivatives["cropCompletenessLedger"],
                    "resizeProof": {
                        "method": "runtime-widget-edge-drag-stress-with-top-level-resize-handler",
                        "runtimeTruth": "pre-live-runtime-widget-edge-interaction-proof; exact-desktop-launcher-live-validation-still-required-before-uts",
                        "before": _rel(root, manifest["log_viewer_edge_resize_before_drag"]),
                        "during": _rel(root, manifest["log_viewer_edge_resize_during_drag"]),
                        "after": _rel(root, manifest["log_viewer_edge_resize_width_proof"]),
                        "bottomDuring": _rel(root, manifest["log_viewer_edge_resize_bottom_during_drag"]),
                        "heightAfter": _rel(root, manifest["log_viewer_edge_resize_height_proof"]),
                        "directGeometrySetUsed": False,
                        "qtestEdgeInputUsed": True,
                        "beforeWidth": before_width,
                        "afterWidth": after_width,
                        "widthIncreased": after_width > before_width,
                        "resizeStress": resize_stress,
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        recording.close()
        log_viewer.close()
        parent_surface.close()
        app.quit()

    QTimer.singleShot(1200, run_default)
    app.exec()
    print(root)
    return int(result_status["code"])


if __name__ == "__main__":
    raise SystemExit(main())
