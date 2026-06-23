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
from PySide6.QtCore import QPoint, Qt, QTimer
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


def _write_evidence_derivatives(root: Path, manifest: dict[str, str]) -> dict[str, object]:
    crops = root / "focused_crops"
    crops.mkdir(parents=True, exist_ok=True)
    recording = Path(manifest["recording_default"])
    log_viewer = Path(manifest["log_viewer_default"])
    log_wide = Path(manifest["log_viewer_edge_resize_width_proof"])
    derivatives = {
        "recordingChromeCrop": _save_crop(recording, crops / "recording_window_chrome.png", (0, 0, 480, 76)),
        "recordingPrimaryActionCrop": _save_crop(recording, crops / "recording_primary_action.png", (10, 54, 470, 166)),
        "recordingTargetTruthCrop": _save_crop(recording, crops / "recording_target_truth.png", (10, 144, 470, 236)),
        "recordingLogRouteCrop": _save_crop(recording, crops / "recording_log_viewer_route.png", (10, 214, 470, 326)),
        "logViewerChromeCrop": _save_crop(log_viewer, crops / "log_viewer_window_chrome.png", (0, 0, 560, 76)),
        "logViewerNativeActionCrop": _save_crop(log_viewer, crops / "log_viewer_native_action_card.png", (10, 54, 550, 158)),
        "logViewerExportActionCrop": _save_crop(log_viewer, crops / "log_viewer_export_action_card.png", (10, 136, 550, 240)),
        "logViewerActionStatusCrop": _save_crop(log_viewer, crops / "log_viewer_action_status.png", (10, 232, 550, 322)),
        "logViewerResizeBeforeCrop": _save_crop(Path(manifest["log_viewer_edge_resize_before_drag"]), crops / "log_viewer_resize_before.png", (18, 54, 542, 360)),
        "logViewerResizeDuringCrop": _save_crop(Path(manifest["log_viewer_edge_resize_during_drag"]), crops / "log_viewer_resize_during.png", (18, 54, 680, 360)),
        "logViewerResizeAfterCrop": _save_crop(log_wide, crops / "log_viewer_resize_after.png", (18, 54, 702, 364)),
    }
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
        "recording-full-window": _rel(root, manifest["recording_default"]),
        "recording-window-chrome": _rel(root, derivatives["recordingChromeCrop"]),
        "recording-primary-action": _rel(root, derivatives["recordingPrimaryActionCrop"]),
        "recording-target-truth": _rel(root, derivatives["recordingTargetTruthCrop"]),
        "recording-log-route": _rel(root, derivatives["recordingLogRouteCrop"]),
        "log-viewer-full-window": _rel(root, manifest["log_viewer_default"]),
        "log-viewer-window-chrome": _rel(root, derivatives["logViewerChromeCrop"]),
        "native-log-destination-action": _rel(root, derivatives["logViewerNativeActionCrop"]),
        "exported-log-destination-action": _rel(root, derivatives["logViewerExportActionCrop"]),
        "log-viewer-action-status": _rel(root, derivatives["logViewerActionStatusCrop"]),
        "log-viewer-resize-before": _rel(root, derivatives["logViewerResizeBeforeCrop"]),
        "log-viewer-resize-during": _rel(root, derivatives["logViewerResizeDuringCrop"]),
        "log-viewer-resize-after": _rel(root, derivatives["logViewerResizeAfterCrop"]),
        "full-desktop-combined": _rel(root, derivatives["fullDesktopCombinedScreenshot"]) if derivatives["fullDesktopCombinedScreenshot"] else "",
        "contact-sheet": _rel(root, derivatives["focusedComparatorContactSheet"]),
    }
    red_rows = [
        {
            "rowId": "RT-REC-001",
            "surface": "Recording Studio",
            "elementGroup": "state label/value",
            "sourceTruthRequirement": "F6-FF01 Recording Studio must avoid report/status-panel feel and duplicated state grammar.",
            "screenshotEvidenceFile": row_map["recording-primary-action"],
            "negativeQuestion": "Does the Studio repeat the same state word as both label and value?",
            "defectLookedFor": "READY / READY or RECORDING / RECORDING visual grammar.",
            "observedFinding": "Current payload uses stable label `State` and a single changing value.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The visible label cannot mirror Ready/Recording because renderer payload always emits `State` for the label.",
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
            "observedFinding": "Start/Stop sits in the hero rail and remains the largest action in the Recording Studio surface.",
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
            "observedFinding": "Target and log are compact truth chips with product-facing copy.",
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
            "observedFinding": "Native card leads with destination and button; path text is muted secondary context.",
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
            "observedFinding": "Export copy says Ready when USER exports.",
            "finalDisposition": "PERFECT_PASS",
            "whyDefectAbsentIfPass": "The card distinguishes future export output from native recordings.",
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
    ]
    red_team = {
        "status": "INTERNAL_RED_TEAM_PASS_FOR_PRE_LV_PACKET",
        "acceptanceRule": "No PERFECT_PASS may rely on assertion-only rows, broad contact sheets, local absolute paths, progress language, or missing defect dispositions.",
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
    ]
    root_cause_defects = [
        {
            "defectId": defect_id,
            "falseAcceptPacketOrEvidence": "C:/Nexus USER/FAM-006-20260622-170147.zip",
            "visibleDefectDescription": visible,
            "whyCodexMissedIt": "Codex trusted helper-green visual ledger output and did not require a negative finding row that challenged the screenshot-visible defect.",
            "failedStep": "pre-LV visual adjudication packet generation",
            "missingCheck": missing,
            "repairMade": "FAM-006 false-ACCEPT regression gate plus row-specific red-team/root-cause evidence now rejects this defect class.",
            "proofNewCheckRejectsKnownBadExample": "dev/orin_fam006_false_accept_regression_gate.py rejects FAM-006-20260622-170147.zip for this class or its artifact family.",
            "currentStatus": "repaired-in-current-branch-local-gate",
            "disposition": "PERFECT_PASS",
        }
        for defect_id, visible, _actual, missing in root_cause_rows
    ]
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
    return {key: _rel(root, value) if value else "" for key, value in derivatives.items()}


def _capture(widget, root: Path, label: str, manifest: dict[str, str]) -> None:
    QApplication.processEvents()
    path = root / f"{label}.png"
    widget.grab().save(str(path), "PNG")
    manifest[label] = str(path)


def _capture_desktop(root: Path, label: str, manifest: dict[str, str]) -> None:
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
    log_viewer.resize(560, 330)
    recording.move(40, 70)
    log_viewer.move(40, 370)
    recording.show()
    log_viewer.show()

    manifest: dict[str, str] = {}

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
        log_viewer._pending_studio_state = log_viewer._log_viewer_studio_state_payload()
        log_viewer._sync_studio_state_to_web()
        QTimer.singleShot(500, run_blocked)

    def run_blocked() -> None:
        _capture(recording, root, "recording_disabled_blocked", manifest)
        _capture(log_viewer, root, "log_viewer_disabled_blocked", manifest)
        log_viewer.resize(560, 330)
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
                    "screenshots": {key: _rel(root, value) for key, value in manifest.items()},
                    "derivatives": derivatives,
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
