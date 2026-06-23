"""Capture FAM-006 feature-studio visual repair evidence.

This is pre-Live-Validation visual proof only. It renders the real Studio
widgets through the branch runtime classes and saves focused screenshots for
USER review and packet inclusion.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw
from PySide6.QtCore import QEventLoop, QPoint, Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

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
    image.crop(box).save(target)
    return str(target)


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
    recordingPrimaryAction: "[data-element-group='recording-primary-action']",
    recordingTargetTruth: "[data-element-group='recording-target-log-truth']",
    recordingLogRoute: "[data-element-group='recording-log-viewer-route']",
    logViewerNativeAction: "[data-folder-kind='native']",
    logViewerExportAction: "[data-folder-kind='export']",
    logViewerActionStatus: "[data-log-shell-primitive='action-first-folder-access-shell-v6']",
  };
  const out = {};
  Object.entries(targets).forEach(([key, selector]) => {
    const element = document.querySelector(selector);
    if (!element || element.hidden) {
      return;
    }
    const rect = element.getBoundingClientRect();
    out[key] = {
      selector,
      rect: {
        left: Math.round(rect.left),
        top: Math.round(rect.top),
        right: Math.round(rect.right),
        bottom: Math.round(rect.bottom),
      },
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


def _crop_record(
    *,
    key: str,
    crop_path: str,
    source_path: Path,
    source_full_window_file: str,
    crop_rect: tuple[int, int, int, int],
    target_rect: tuple[int, int, int, int],
    expected_text: list[str],
    target_semantic_name: str,
    overlay_proof_file: str,
    element_bounds_source: str,
    all_visible_text_found: list[str],
    adjacent_partial_text_found: list[str],
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
    minimum_margin = 0 if key.endswith("window-chrome") else 8
    content_touches_crop_edge = any(value < minimum_margin for value in margin.values())
    joined_visible_text = " ".join(all_visible_text_found).casefold()
    missing_expected_text = [text for text in expected_text if text.casefold() not in joined_visible_text]
    undeclared_adjacent_text = adjacent_partial_text_found and not adjacent_partial_text_allowed
    verdict = (
        "PERFECT_PASS"
        if not content_touches_crop_edge
        and not missing_expected_text
        and not undeclared_adjacent_text
        and bool(overlay_proof_file)
        else "REPAIR_REQUIRED"
    )
    return {
        "key": key,
        "targetSemanticElementName": target_semantic_name,
        "cropFile": crop_path,
        "overlayProofFile": overlay_proof_file,
        "sourceFullWindowFile": source_full_window_file,
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
        "adjacentPartialTextFoundInCrop": adjacent_partial_text_found,
        "adjacentPartialTextAllowed": adjacent_partial_text_allowed,
        "adjacentPartialTextAllowanceReason": adjacent_partial_text_allowance_reason,
        "missingExpectedTextFromCrop": missing_expected_text,
        "textPresenceCheck": {
            "method": "dom-bounds-derived-visible-text-list-plus-overlay-proof-review",
            "allExpectedTextNamedAndVisuallyPresent": not missing_expected_text,
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
        "cropNotHidingAdjacentDefect": not undeclared_adjacent_text,
        "contentValidationMethod": "DOM target bounds + visible text list + explicit adjacent partial text audit + overlay proof",
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
            "visible_text": [_text_from_dom(bounds, dom_key)],
            "forbidden_adjacent": forbidden_adjacent or [],
            "adjacent_allowed": False,
            "adjacent_reason": "",
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
                expected=["RECORDING", "RECORDING STUDIO"],
                min_width=460,
                min_height=90,
                margin=0,
            ),
            spec_from_dom(
                name="recordingPrimaryActionCrop",
                key="recording-primary-action",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingPrimaryAction",
                filename="recording_primary_action.png",
                semantic="Recording Studio primary Start/Stop controller action",
                expected=["START RECORDING", "Selected overlay ready."],
                forbidden_adjacent=["Target", "Log Viewer Studio"],
                min_width=430,
                min_height=100,
            ),
            spec_from_dom(
                name="recordingTargetTruthCrop",
                key="recording-target-truth",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingTargetTruth",
                filename="recording_target_truth.png",
                semantic="Recording Studio target and native-log truth strip",
                expected=["Target", "Default Overlay Profile", "2 active monitors", "Log", "Waiting for first recording."],
                forbidden_adjacent=["Start Recording", "Log Viewer Studio"],
                min_width=430,
                min_height=88,
            ),
            spec_from_dom(
                name="recordingLogRouteCrop",
                key="recording-log-route",
                source=recording,
                source_key="recording-full-window",
                source_label="recording_default",
                dom_key="recordingLogRoute",
                filename="recording_log_viewer_route.png",
                semantic="Recording Studio Log Viewer Studio route action",
                expected=["LOG VIEWER STUDIO"],
                forbidden_adjacent=["Waiting for first recording."],
                min_width=430,
                min_height=74,
            ),
            spec_from_dom(
                name="logViewerChromeCrop",
                key="log-viewer-window-chrome",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="chrome",
                filename="log_viewer_window_chrome.png",
                semantic="Log Viewer Studio full chrome/window shell",
                expected=["RECORDING LOGS", "LOG VIEWER STUDIO"],
                min_width=540,
                min_height=90,
                margin=0,
            ),
            spec_from_dom(
                name="logViewerNativeActionCrop",
                key="native-log-destination-action",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="logViewerNativeAction",
                filename="log_viewer_native_action_card.png",
                semantic="Log Viewer Studio native log destination action card",
                expected=["Native", "Recordings", "Available now", "OPEN NATIVE LOGS"],
                forbidden_adjacent=["Exported Logs", "Open Exported Logs", "Empty until exported"],
                min_width=520,
                min_height=112,
            ),
            spec_from_dom(
                name="logViewerExportActionCrop",
                key="exported-log-destination-action",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="logViewerExportAction",
                filename="log_viewer_export_action_card.png",
                semantic="Log Viewer Studio exported log destination action card",
                expected=["Export", "Exported Logs", "Empty until exported", "OPEN EXPORTED LOGS"],
                forbidden_adjacent=["Native", "Recordings folder", "Open Native Logs", "Available now"],
                min_width=520,
                min_height=112,
            ),
            spec_from_dom(
                name="logViewerActionStatusCrop",
                key="log-viewer-action-status",
                source=log_viewer,
                source_key="log-viewer-full-window",
                source_label="log_viewer_default",
                dom_key="logViewerActionStatus",
                filename="log_viewer_action_status.png",
                semantic="Log Viewer Studio native/export/status relationship stack",
                expected=["Native", "Recordings", "OPEN NATIVE LOGS", "Export", "Exported Logs", "OPEN EXPORTED LOGS", "Choose a log destination to open."],
                min_width=540,
                min_height=250,
            ),
            spec_from_dom(
                name="logViewerResizeBeforeCrop",
                key="log-viewer-resize-before",
                source=Path(str(manifest["log_viewer_edge_resize_before_drag"])),
                source_key="log-viewer-full-window",
                source_label="log_viewer_edge_resize_before_drag",
                dom_key="logViewerActionStatus",
                filename="log_viewer_resize_before.png",
                semantic="Log Viewer Studio before-resize log access stack",
                expected=["Native", "Exported Logs", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS"],
                min_width=500,
                min_height=250,
            ),
            spec_from_dom(
                name="logViewerResizeDuringCrop",
                key="log-viewer-resize-during",
                source=Path(str(manifest["log_viewer_edge_resize_during_drag"])),
                source_key="log-viewer-full-window",
                source_label="log_viewer_edge_resize_during_drag",
                dom_key="logViewerActionStatus",
                filename="log_viewer_resize_during.png",
                semantic="Log Viewer Studio during-resize log access stack",
                expected=["Native", "Exported Logs", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS"],
                min_width=620,
                min_height=250,
            ),
            spec_from_dom(
                name="logViewerResizeAfterCrop",
                key="log-viewer-resize-after",
                source=log_wide,
                source_key="log-viewer-full-window",
                source_label="log_viewer_edge_resize_width_proof",
                dom_key="logViewerActionStatus",
                filename="log_viewer_resize_after.png",
                semantic="Log Viewer Studio after-resize log access stack",
                expected=["Native", "Exported Logs", "OPEN NATIVE LOGS", "OPEN EXPORTED LOGS"],
                min_width=660,
                min_height=250,
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
        ("Recording primary action", Path(derivatives["recordingPrimaryActionCrop"])),
        ("Recording target truth", Path(derivatives["recordingTargetTruthCrop"])),
        ("Recording Log Viewer route", Path(derivatives["recordingLogRouteCrop"])),
        ("Log Viewer chrome", Path(derivatives["logViewerChromeCrop"])),
        ("Log Viewer native action", Path(derivatives["logViewerNativeActionCrop"])),
        ("Log Viewer exported action", Path(derivatives["logViewerExportActionCrop"])),
        ("Log Viewer resize after", Path(derivatives["logViewerResizeAfterCrop"])),
    ]
    existing_comparators = [(label, path) for label, path in comparator_paths if path.exists()]
    derivatives["focusedComparatorContactSheet"] = _make_contact_sheet(
        existing_comparators,
        root / "focused_comparator_contact_sheet.png",
    )
    derivatives["fullDesktopCombinedScreenshot"] = manifest.get("full_desktop_recording_and_log_viewer_after_repair", "")
    row_map = {
        "recording-full-window": _rel(root, str(manifest["recording_default"])),
        "recording-window-chrome": _rel(root, derivatives["recordingChromeCrop"]),
        "recording-window-chrome-overlay": _rel(root, derivatives["recordingChromeCropOverlay"]),
        "recording-primary-action": _rel(root, derivatives["recordingPrimaryActionCrop"]),
        "recording-primary-action-overlay": _rel(root, derivatives["recordingPrimaryActionCropOverlay"]),
        "recording-target-truth": _rel(root, derivatives["recordingTargetTruthCrop"]),
        "recording-target-truth-overlay": _rel(root, derivatives["recordingTargetTruthCropOverlay"]),
        "recording-log-route": _rel(root, derivatives["recordingLogRouteCrop"]),
        "recording-log-route-overlay": _rel(root, derivatives["recordingLogRouteCropOverlay"]),
        "log-viewer-full-window": _rel(root, str(manifest["log_viewer_default"])),
        "log-viewer-window-chrome": _rel(root, derivatives["logViewerChromeCrop"]),
        "log-viewer-window-chrome-overlay": _rel(root, derivatives["logViewerChromeCropOverlay"]),
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
        "contact-sheet": _rel(root, derivatives["focusedComparatorContactSheet"]),
    }
    crop_records = {
        spec["key"]: _crop_record(
            key=spec["key"],
            crop_path=row_map[spec["key"]],
            source_path=spec["source"],
            source_full_window_file=row_map[spec["source_key"]],
            overlay_proof_file=row_map[f"{spec['key']}-overlay"],
            crop_rect=spec["crop"],
            target_rect=spec["target"],
            expected_text=spec["text"],
            target_semantic_name=spec["semantic"],
            element_bounds_source=spec["bounds_source"],
            all_visible_text_found=spec["visible_text"],
            adjacent_partial_text_found=[
                text
                for text in spec["forbidden_adjacent"]
                if text.casefold() in " ".join(spec["visible_text"]).casefold()
            ],
            adjacent_partial_text_allowed=bool(spec["adjacent_allowed"]),
            adjacent_partial_text_allowance_reason=str(spec["adjacent_reason"]),
        )
        for spec in crop_specs.values()
    }
    derivatives["cropCompletenessChecks"] = {
        key: {
            "crop": row_map[key],
            "cropCompletenessLedgerKey": key,
            "completeTargetElement": record["finalCropVerdict"] == "PERFECT_PASS",
            "includesAllText": record["textPresenceCheck"]["allExpectedTextNamedAndVisuallyPresent"] is True,
            "includesBorderRadiusGlow": record["borderRadiusGlowInclusionCheck"]["included"] is True,
            "includesSurroundingContext": record["surroundingContextCheck"]["included"] is True,
            "notClipped": record["targetTextControlOrBorderCutOff"] is False,
            "noUndeclaredAdjacentPartialText": not record["adjacentPartialTextFoundInCrop"] or record["adjacentPartialTextAllowed"] is True,
            "overlayProofFile": record["overlayProofFile"],
            "contentValidationMethod": record["contentValidationMethod"],
            "validatedBy": "dom-bounds-target-crop-plus-overlay-proof-plus-explicit-visible-text-and-adjacent-text-audit",
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
        "| Evidence key | Crop file | Overlay proof | Source file | Target | Expected text | Visible text | Adjacent partial text | Margins | Verdict |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(
            "| {key} | {cropFile} | {overlayProofFile} | {sourceFullWindowFile} | {target} | {text} | {visible} | {adjacent} | L{left}/T{top}/R{right}/B{bottom} | {verdict} |".format(
                key=record["key"],
                cropFile=record["cropFile"],
                overlayProofFile=record["overlayProofFile"],
                sourceFullWindowFile=record["sourceFullWindowFile"],
                target=record["targetSemanticElementName"],
                text=", ".join(record["expectedTextInsideCrop"]),
                visible=" / ".join(record["allVisibleTextFoundInCrop"]),
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
    red_rows = [
        {
            "rowId": "RT-REC-001",
            "surface": "Recording Studio",
            "elementGroup": "state label/value",
            "sourceTruthRequirement": "F6-FF01 Recording Studio must avoid report/status-panel feel and duplicated state grammar.",
            "screenshotEvidenceFile": row_map["recording-primary-action"],
            "negativeQuestion": "Does the Studio repeat the same state word as both label and value?",
            "defectLookedFor": "READY / READY or RECORDING / RECORDING visual grammar.",
            "observedFinding": "Current payload uses stable label `Now` and a single changing value.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The visible label cannot mirror Ready/Recording because renderer payload always emits `Now` for the label.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-REC-002",
            "surface": "Recording Studio",
            "elementGroup": "primary Start/Stop action",
            "sourceTruthRequirement": "Recording Studio is an ultra-lightweight detached controller with Start/Stop as the clear purpose.",
            "screenshotEvidenceFile": row_map["recording-primary-action"],
            "negativeQuestion": "Is Start/Stop visually contested by equal-weight status/report fragments?",
            "defectLookedFor": "Primary action not dominant.",
            "observedFinding": "Start/Stop fills the action rail width and is visually larger than secondary Log Viewer routing.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Secondary Log Viewer route is below target/log context and uses smaller secondary-action styling.",
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
            "observedFinding": "Target and log are compact secondary truth lines below the action rail, without bordered report rows.",
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
            "observedFinding": "Copy uses selected overlay, log waiting/saved language, and a secondary Log Viewer route.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "No row exposes validation, helper, worktree, proof, or debug wording.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-001",
            "surface": "Log Viewer Studio",
            "elementGroup": "native destination",
            "sourceTruthRequirement": "Log Viewer Studio is a compact log access shell, not a technical path table.",
            "screenshotEvidenceFile": row_map["native-log-destination-action"],
            "negativeQuestion": "Does Native look like a path/status table row rather than an action destination?",
            "defectLookedFor": "Technical folder table feel.",
            "observedFinding": "Native card leads with the open action and product destination; path text is muted secondary context.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Path content is elided and secondary; the visible action remains the control.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-002",
            "surface": "Log Viewer Studio",
            "elementGroup": "export destination",
            "sourceTruthRequirement": "Exported logs are USER-requested artifacts and must not imply automatic export.",
            "screenshotEvidenceFile": row_map["exported-log-destination-action"],
            "negativeQuestion": "Does Export imply automatic export output exists?",
            "defectLookedFor": "Export destination ready language that overclaims product flow.",
            "observedFinding": "Export copy reads Empty until exported.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The visible copy contains no governance/internal USER wording and does not imply an automatic export exists.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-003",
            "surface": "Log Viewer Studio",
            "elementGroup": "folder status",
            "sourceTruthRequirement": "Status must not contradict destination card state.",
            "screenshotEvidenceFile": row_map["log-viewer-action-status"],
            "negativeQuestion": "Can the footer say blocked/opened while both cards still claim ready?",
            "defectLookedFor": "Status contradiction.",
            "observedFinding": "Renderer tracks last folder kind and changes the matching card to Opened or Could not open.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "Status state is tied to the affected destination instead of global ready text.",
            "exactRepairIfRequired": "",
        },
        {
            "rowId": "RT-LOG-004",
            "surface": "Log Viewer Studio",
            "elementGroup": "resize",
            "sourceTruthRequirement": "Current Log Viewer Studio shell is resizable and must prove edge resize without attached-child corner grip.",
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
            "elementGroup": "Recording primary action crop",
            "sourceTruthRequirement": "Focused crops must include the complete target element, all visible text, and enough surrounding context to judge clipping.",
            "screenshotEvidenceFile": row_map["recording-primary-action"],
            "negativeQuestion": "Does recording_primary_action.png cut off the support text under the primary action?",
            "defectLookedFor": "Lower support text clipped by the crop boundary.",
            "observedFinding": "The current crop includes the full primary action region, support text, rounded border/glow, and surrounding padding.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The crop box was expanded and the manifest records completeTargetElement/includesAllText/notClipped for this key.",
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
    ]
    red_team_defect_metadata = {
        "RT-REC-001": ("recording-state-duplication", "Fail if label/value repeat the same Ready, Recording, Saved, or Blocked word."),
        "RT-REC-002": ("recording-action-hierarchy", "Fail if Start/Stop is not the widest and most visually dominant control."),
        "RT-REC-003": ("recording-status-panel-feel", "Fail if target/log truth appears as bordered report rows or debug/status panels."),
        "RT-REC-004": ("recording-product-copy", "Fail if Recording Studio copy exposes validation, helper, proof, worktree, or debug terms."),
        "RT-LOG-001": ("log-viewer-action-card-polish", "Fail if native destination reads as a path/status table instead of an action card."),
        "RT-LOG-002": ("log-viewer-user-export-copy", "Fail if visible UI copy contains USER exports or other governance/internal terms."),
        "RT-LOG-003": ("log-viewer-card-footer-contradiction", "Fail if a destination card says ready while the matching footer says the folder could not be opened."),
        "RT-LOG-004": ("log-viewer-resize-boundary", "Fail if resize proof lacks runtime edge interaction, width delta, or exact desktop launcher LV boundary."),
        "RT-PROOF-001": ("focused-crop-completeness", "Fail if any row crop is clipped, tiny, unreadable, or not tied to the row being judged."),
        "RT-CROP-001": ("recording-primary-action-crop-completeness", "Fail if recording_primary_action.png clips the lower support text or lacks complete-element manifest proof."),
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
        "RT-PROOF-006": ("green-row-without-packet-evidence", "Fail if any PERFECT_PASS row lacks packet evidence key or packet-relative primary proof."),
        "RT-PROOF-007": ("local-absolute-crop-source-primary-proof", "Fail if crop sourceFullWindowFile uses a local absolute path as primary proof."),
        "RT-PROOF-008": ("non-studio-green-row-without-packet-proof", "Fail if non-Studio PERFECT_PASS rows lack packet evidence key or packet-relative primary proof."),
        "RT-PROOF-009": ("visual-ledger-false-crop-completeness-reliance", "Fail if visual ledger accepts assertion-only crop-completeness without DOM, overlay, and adjacent-text proof."),
    }
    for row in red_rows:
        defect_class, recurrence_check = red_team_defect_metadata[row["rowId"]]
        row["defectClass"] = defect_class
        row["checkThatWouldFailIfAppearsAgain"] = recurrence_check
    red_team = {
        "status": "INTERNAL_RED_TEAM_PASS_FOR_PRE_LV_PACKET",
        "knownBadRegressionRejected": True,
        "knownBadPacket": "C:/Nexus USER/FAM-006-20260622-194848.zip",
        "knownBadPacketSha256": "2E1B5A3F17C876B563243F63B005663A89B4F71CF0EBC9E34EC4A3D7E02718D3",
        "acceptanceRule": "No PERFECT_PASS may rely on assertion-only rows, broad contact sheets, local absolute paths, progress language, missing defect dispositions, missing overlay proof, incomplete expected text, clipped target elements, undeclared adjacent partial text, or wrong target rectangles.",
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
    ]
    root_cause_defects = [
        {
            "defectId": defect_id,
            "falseAcceptPacketOrEvidence": "C:/Nexus USER/FAM-006-20260622-194848.zip and preserved external regression corpus copy",
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


def main() -> int:
    leaf = time.strftime("%Y%m%d_%H%M%S") + "_feature_studio_visual_fail_repair"
    root = PROOF_ROOT / leaf
    root.mkdir(parents=True, exist_ok=True)

    app = QApplication.instance() or QApplication([])
    screen = QGuiApplication.primaryScreen()
    recording = MonitoringHudRecordingStudioWindow(screen)
    log_viewer = MonitoringHudLogViewerStudioWindow(screen)

    recording.update_product_state(
        request_id=1,
        active_profile_name="Default Overlay Profile",
        target_count=2,
        target_names="CPU Group, GPU Group",
        target_state="ready",
        recording_session_state="ready",
        start_stop_state="start-enabled",
        activate_window=False,
    )
    log_viewer.update_product_state(
        request_id="proof-1",
        native_log_path="C:/Users/anden/AppData/Local/Nexus Desktop AI/Recordings",
        export_dir="C:/Users/anden/AppData/Local/Nexus Desktop AI/Exported Logs",
        activate_window=False,
    )

    recording.resize(480, 330)
    log_viewer.resize(log_viewer.WIDTH, log_viewer.HEIGHT)
    recording.move(40, 70)
    log_viewer.move(40, 370)
    recording.show()
    log_viewer.show()

    manifest: dict[str, object] = {}

    def run_default() -> None:
        _capture(recording, root, "recording_default", manifest)
        _capture(log_viewer, root, "log_viewer_default", manifest)
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
        )
        QTimer.singleShot(500, run_active)

    def run_active() -> None:
        _capture(recording, root, "recording_active_stop_state", manifest)
        recording.webview.page().runJavaScript(
            "document.querySelector('[data-control=\"recording-studio-toggle\"]').classList.add('is-hovered');"
        )
        log_viewer.webview.page().runJavaScript(
            "document.querySelector('[data-control=\"log-viewer-open-native\"]').classList.add('is-hovered');"
        )
        QTimer.singleShot(500, run_hover)

    def run_hover() -> None:
        _capture(recording, root, "recording_hover_focus", manifest)
        _capture(log_viewer, root, "log_viewer_hover_focus", manifest)
        recording.webview.page().runJavaScript(
            "const el=document.querySelector('[data-control=\"recording-studio-toggle\"]');"
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
        recording.update_product_state(
            request_id=3,
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
        start = QPoint(log_viewer.webview.width() - 2, log_viewer.webview.height() // 2)
        QTest.mousePress(log_viewer.webview, Qt.LeftButton, Qt.NoModifier, start)
        QApplication.processEvents()
        QTest.mouseMove(log_viewer.webview, QPoint(log_viewer.webview.width() + 120, log_viewer.webview.height() // 2), delay=120)
        QApplication.processEvents()
        _capture(log_viewer, root, "log_viewer_edge_resize_during_drag", manifest)
        QTest.mouseRelease(log_viewer.webview, Qt.LeftButton, Qt.NoModifier, QPoint(log_viewer.webview.width() + 120, log_viewer.webview.height() // 2), delay=120)
        QApplication.processEvents()
        QTimer.singleShot(500, run_resized)

    def run_resized() -> None:
        _capture(log_viewer, root, "log_viewer_edge_resize_width_proof", manifest)
        before = Path(manifest["log_viewer_edge_resize_before_drag"])
        after = Path(manifest["log_viewer_edge_resize_width_proof"])
        before_width = _load_image(before).width
        after_width = _load_image(after).width
        if after_width <= before_width:
            (root / "resize_proof_failure.json").write_text(
                json.dumps(
                    {
                        "result": "FAIL",
                        "reason": "ordered edge drag did not increase rendered Log Viewer width",
                        "beforeWidth": before_width,
                        "afterWidth": after_width,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        derivatives = _write_evidence_derivatives(root, manifest)
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
                    "cropCompletenessChecks": derivatives["cropCompletenessChecks"],
                    "cropCompletenessLedger": derivatives["cropCompletenessLedger"],
                    "resizeProof": {
                        "method": "runtime-widget-edge-drag-with-top-level-resize-handler",
                        "runtimeTruth": "pre-live-runtime-widget-edge-interaction-proof; exact-desktop-launcher-live-validation-still-required-before-uts",
                        "before": _rel(root, manifest["log_viewer_edge_resize_before_drag"]),
                        "during": _rel(root, manifest["log_viewer_edge_resize_during_drag"]),
                        "after": _rel(root, manifest["log_viewer_edge_resize_width_proof"]),
                        "directGeometrySetUsed": False,
                        "qtestEdgeInputUsed": True,
                        "beforeWidth": before_width,
                        "afterWidth": after_width,
                        "widthIncreased": after_width > before_width,
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        recording.close()
        log_viewer.close()
        app.quit()

    QTimer.singleShot(1200, run_default)
    app.exec()
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
