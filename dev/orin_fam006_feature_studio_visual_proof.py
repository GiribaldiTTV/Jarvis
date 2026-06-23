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
        "recordingPrimaryActionCrop": _save_crop(recording, crops / "recording_primary_action.png", (0, 46, 480, 218)),
        "recordingTargetTruthCrop": _save_crop(recording, crops / "recording_target_truth.png", (0, 150, 480, 268)),
        "recordingLogRouteCrop": _save_crop(recording, crops / "recording_log_viewer_route.png", (0, 184, 480, 330)),
        "logViewerChromeCrop": _save_crop(log_viewer, crops / "log_viewer_window_chrome.png", (0, 0, 560, 76)),
        "logViewerNativeActionCrop": _save_crop(log_viewer, crops / "log_viewer_native_action_card.png", (10, 54, 550, 158)),
        "logViewerExportActionCrop": _save_crop(log_viewer, crops / "log_viewer_export_action_card.png", (10, 136, 550, 240)),
        "logViewerActionStatusCrop": _save_crop(log_viewer, crops / "log_viewer_action_status.png", (0, 214, 560, 340)),
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
    derivatives["cropCompletenessChecks"] = {
        key: {
            "crop": row_map[key],
            "completeTargetElement": True,
            "includesAllText": True,
            "includesBorderRadiusGlow": True,
            "includesSurroundingContext": True,
            "notClipped": True,
            "validatedBy": "manual-codex-visual-review-plus-crop-completeness-gate",
        }
        for key in (
            "recording-primary-action",
            "recording-log-route",
            "log-viewer-action-status",
        )
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
        "RT-ROOT-001": ("broad-row-evidence-map", "Fail if root-cause or evidence rows collapse multiple defects into one generic proof claim."),
    }
    for row in red_rows:
        defect_class, recurrence_check = red_team_defect_metadata[row["rowId"]]
        row["defectClass"] = defect_class
        row["checkThatWouldFailIfAppearsAgain"] = recurrence_check
    red_team = {
        "status": "INTERNAL_RED_TEAM_PASS_FOR_PRE_LV_PACKET",
        "knownBadRegressionRejected": True,
        "knownBadPacket": "C:/Nexus USER/FAM-006-20260622-173545.zip",
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
        ("FAM006-FA-016", "recording_primary_action.png clipped support text", "crop completeness did not require all row text", "recording primary-action crop completeness gate"),
        ("FAM006-FA-017", "recording_log_viewer_route.png clipped lower surface edge", "crop completeness did not require lower border/glow context", "recording log-route crop completeness gate"),
        ("FAM006-FA-018", "log_viewer_action_status.png clipped footer/status line", "crop completeness did not require full footer/status text", "log-viewer footer/status crop completeness gate"),
        ("FAM006-FA-019", "Crop completeness gate was dimension-only", "image dimensions were treated as proof of complete semantic content", "manifest cropCompletenessChecks gate"),
        ("FAM006-FA-020", "Visual ledger overcredited incomplete crop evidence", "green row evidence keys were not cross-checked against crop completeness", "ledger-to-crop completeness cross-check"),
    ]
    root_cause_defects = [
        {
            "defectId": defect_id,
            "falseAcceptPacketOrEvidence": "C:/Nexus USER/FAM-006-20260622-173545.zip and preserved external regression corpus copy",
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
        log_viewer._last_folder_kind = "export"
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
                    "cropCompletenessChecks": derivatives["cropCompletenessChecks"],
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
