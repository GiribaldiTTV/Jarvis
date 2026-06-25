"""FAM-006 false-ACCEPT regression gate.

This branch-local gate prevents the specific returned-UTS failure loop where a
packet claims Studio visual ACCEPT while the packet evidence still contains
summary-only root cause, assertion-only red-team rows, local-only proof, weak
resize proof, clipped crops, or progress-language green claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from orin_fam006_unified_defect_ledger import scan_packet_text_hygiene, validate_udl_state
from orin_fam006_full_desktop_false_green_review import validate as validate_full_desktop_false_green_packet
from orin_fam006_visual_acceptance_target_packet import validate as validate_visual_acceptance_target_packet


USER_ROOT = Path("C:/Nexus USER")
DEFAULT_CURRENT_PACKET = USER_ROOT / "FAM-006"
EXTERNAL_BRANCH_ROOT = Path(
    "C:/Nexus Governance State/branches/feature_fam_006_dashboard_recording_start_stop_local_file"
)
KNOWN_BAD_CORPUS_ROOT = EXTERNAL_BRANCH_ROOT / "false_accept_regression_corpus"
KNOWN_BAD_ZIPS = [
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260624-145849.zip",
    USER_ROOT / "FAM-006-20260624-145849.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260624-142638.zip",
    USER_ROOT / "FAM-006-20260624-142638.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260624-135010.zip",
    USER_ROOT / "FAM-006-20260624-135010.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260624-132551.zip",
    USER_ROOT / "FAM-006-20260624-132551.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260624-130151.zip",
    USER_ROOT / "FAM-006-20260624-130151.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260624-121535.zip",
    USER_ROOT / "FAM-006-20260624-121535.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-123110.zip",
    USER_ROOT / "FAM-006-20260623-123110.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-121602.zip",
    USER_ROOT / "FAM-006-20260623-121602.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-120234.zip",
    USER_ROOT / "FAM-006-20260623-120234.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-113615.zip",
    USER_ROOT / "FAM-006-20260623-113615.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-063715.zip",
    USER_ROOT / "FAM-006-20260623-063715.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-060525.zip",
    USER_ROOT / "FAM-006-20260623-060525.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-050502.zip",
    USER_ROOT / "FAM-006-20260623-050502.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-202600.zip",
    USER_ROOT / "FAM-006-20260622-202600.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-194848.zip",
    USER_ROOT / "FAM-006-20260622-194848.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-192100.zip",
    USER_ROOT / "FAM-006-20260622-192100.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-182112.zip",
    USER_ROOT / "FAM-006-20260622-182112.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-175717.zip",
    USER_ROOT / "FAM-006-20260622-175717.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-173545.zip",
    USER_ROOT / "FAM-006-20260622-173545.zip",
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260622-170147.zip",
    USER_ROOT / "FAM-006-20260622-170147.zip",
]
KNOWN_BAD_RECONSTRUCTED_RECORDS = [
    KNOWN_BAD_CORPUS_ROOT / "FAM-006-20260623-071500.reconstructed-known-bad.json",
]

REQUIRED_RED_TEAM_FIELDS = {
    "rowId",
    "surface",
    "elementGroup",
    "sourceTruthRequirement",
    "screenshotEvidenceFile",
    "negativeQuestion",
    "defectLookedFor",
    "observedFinding",
    "finalDisposition",
    "whyDefectAbsentIfPass",
    "exactRepairIfRequired",
    "checkThatWouldFailIfAppearsAgain",
}

REQUIRED_ROOT_CAUSE_FIELDS = {
    "defectId",
    "falseAcceptPacketOrEvidence",
    "visibleDefectDescription",
    "whyCodexMissedIt",
    "failedStep",
    "missingCheck",
    "repairMade",
    "proofNewCheckRejectsKnownBadExample",
    "currentStatus",
    "disposition",
}

REQUIRED_EVIDENCE_KEYS = {
    "recording-full-window",
    "recording-window-chrome",
    "recording-primary-action",
    "recording-target-truth",
    "recording-log-route",
    "log-viewer-full-window",
    "log-viewer-window-chrome",
    "native-log-destination-action",
    "exported-log-destination-action",
    "log-viewer-action-status",
    "log-viewer-resize-before",
    "log-viewer-resize-during",
    "log-viewer-resize-after",
    "full-desktop-combined",
    "b2-default-parent-neighbor-full-desktop",
    "b2-same-session-moved-restore-full-desktop",
    "b2-fresh-window-new-session-full-desktop",
    "b2-placement-proof-json",
    "b2-placement-proof-markdown",
    "contact-sheet",
    "comparator-ai-control-center-outer-frame",
    "comparator-ai-control-center-chrome-header",
    "comparator-ai-control-center-window-control-cluster",
    "comparator-ai-control-center-button-grammar",
    "comparator-ai-control-center-panel-rhythm",
    "comparator-ai-control-center-status-action-grammar",
}

REQUIRED_SOURCE_TRUTH_CONTEXT_FILES = {
    "Docs_Main.md",
    "Docs_nexus_startup_contract.md",
    "Docs_phase_governance.md",
    "Docs_branch_plans_README.md",
    "Docs_nexus_vision.md",
    "FAM-002_desktop_interface.md",
    "FAM-006_monitoring_and_hud.md",
    "FAM-006_recording.md",
    "ui_reference_catalog_index.md",
    "UIREF-001_top_level_window_frame.md",
    "UIREF-002_window_control_cluster.md",
    "UIREF-003_control_state_and_selector_grammar.md",
    "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
    "UIREF-005_design_token_and_shared_rule_baseline.md",
    "UIREF-006_negative_example_and_enforcement_contract.md",
    "Docs_user_test_summary_guidance.md",
    "Docs_validation_helper_registry.md",
    "Docs_incident_patterns.md",
    "feature_fam_006_dashboard_recording_start_stop_local_file.md",
    "external_branch_plan.md",
}

DEFAULT_CROP_RULE = {
    "minWidth": 220,
    "minHeight": 60,
    "requires": (
        "completeTargetElement",
        "includesAllText",
        "includesBorderRadiusGlow",
        "includesSurroundingContext",
        "notClipped",
    ),
}

REQUIRED_CROP_COMPLETENESS = {
    "recording-window-chrome": {**DEFAULT_CROP_RULE, "minWidth": 390, "minHeight": 160},
    "recording-primary-action": {**DEFAULT_CROP_RULE, "minWidth": 150, "minHeight": 34},
    "recording-target-truth": {**DEFAULT_CROP_RULE, "minWidth": 350, "minHeight": 58},
    "recording-log-route": {
        **DEFAULT_CROP_RULE,
        "minWidth": 180,
        "minHeight": 34,
    },
    "log-viewer-window-chrome": {**DEFAULT_CROP_RULE, "minWidth": 425, "minHeight": 160},
    "native-log-destination-action": {**DEFAULT_CROP_RULE, "minWidth": 160, "minHeight": 28},
    "exported-log-destination-action": {**DEFAULT_CROP_RULE, "minWidth": 180, "minHeight": 28},
    "log-viewer-action-status": {**DEFAULT_CROP_RULE, "minWidth": 390, "minHeight": 110},
    "log-viewer-resize-before": {**DEFAULT_CROP_RULE, "minWidth": 425, "minHeight": 160},
    "log-viewer-resize-during": {**DEFAULT_CROP_RULE, "minWidth": 500, "minHeight": 160},
    "log-viewer-resize-after": {**DEFAULT_CROP_RULE, "minWidth": 500, "minHeight": 160},
}

FORBIDDEN_GREEN_WORDS = (
    "better",
    "closer",
    "improved",
    "mostly",
    "cleaner",
    "good enough",
    "clean enough",
    "green enough",
    "looks okay",
    "looks acceptable",
)

FORBIDDEN_PRODUCT_COPY = (
    "ready when user exports",
    "user exports",
)

REQUIRED_RED_TEAM_DEFECT_CLASSES = {
    "log-viewer-user-export-copy",
    "log-viewer-card-footer-contradiction",
    "recording-action-hierarchy",
    "recording-status-panel-feel",
    "local-absolute-primary-proof",
    "broad-row-evidence-map",
    "visual-ledger-overcredit",
    "recording-primary-action-crop-completeness",
    "recording-log-route-crop-completeness",
    "log-viewer-footer-status-crop-completeness",
    "full-window-vs-focused-crop-mapping",
    "crop-border-radius-glow-context",
    "crop-text-cutoff",
    "crop-hides-adjacent-defects",
    "packet-relative-evidence-map-completeness",
    "visual-ledger-overcredit-incomplete-proof",
    "visual-packet-source-truth-context-completeness",
    "visual-ledger-local-primary-proof",
    "crop-completeness-self-attestation",
    "incomplete-crop-completeness-coverage",
    "green-row-without-packet-evidence",
    "local-absolute-crop-source-primary-proof",
    "non-studio-green-row-without-packet-proof",
    "crop-adjacent-partial-text-contamination",
    "crop-target-element-cutoff",
    "crop-expected-text-list-incomplete",
    "crop-target-rectangle-mismatch",
    "crop-hides-layout-relationship-defect",
    "crop-overlay-proof-missing",
    "visual-ledger-false-crop-completeness-reliance",
    "crop-overlay-ledger-contradiction",
    "element-crop-vs-relationship-crop-classification",
    "crop-adjacent-partial-geometry-contamination",
    "crop-expected-text-audit-incomplete",
    "crop-scope-type-mismatch",
    "crop-visible-text-not-expected-or-excluded",
    "resize-state-text-audit-incomplete",
    "comparator-proof-not-row-bound",
    "green-comparator-row-missing-evidence-key",
    "uncited-broad-comparator-sheet",
    "row-specific-comparator-finding-missing",
    "comparator-media-scope-mismatch",
    "comparator-crop-not-focused",
    "full-window-comparator-used-as-focused-proof",
    "duplicate-comparator-media-reused",
    "comparator-finding-media-mismatch",
    "comparator-crop-unreadable",
}

COMPARATOR_CROP_RULES = {
    "comparator-ai-control-center-outer-frame": {
        "cropType": "BROAD_SHELL_CROP",
        "minWidth": 520,
        "minHeight": 560,
        "maxWidth": 620,
        "maxHeight": 660,
        "proofKind": "broad-context-shell-proof",
    },
    "comparator-ai-control-center-chrome-header": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 500,
        "minHeight": 120,
        "maxWidth": 620,
        "maxHeight": 190,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-window-control-cluster": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 60,
        "minHeight": 35,
        "maxWidth": 130,
        "maxHeight": 80,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-button-grammar": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 150,
        "minHeight": 50,
        "maxWidth": 260,
        "maxHeight": 110,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-panel-rhythm": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 460,
        "minHeight": 180,
        "maxWidth": 550,
        "maxHeight": 260,
        "proofKind": "focused-proof",
    },
    "comparator-ai-control-center-status-action-grammar": {
        "cropType": "FOCUSED_COMPARATOR_CROP",
        "minWidth": 460,
        "minHeight": 170,
        "maxWidth": 550,
        "maxHeight": 250,
        "proofKind": "focused-proof",
    },
}

REQUIRED_CROP_CONTENT_FIELDS = {
    "cropType",
    "declaredTargetScope",
    "targetSemanticElementName",
    "includedAdjacentElements",
    "relationshipBeingProven",
    "includedElementRects",
    "overlayProofFile",
    "elementBoundsSource",
    "allVisibleTextFoundInCrop",
    "visibleTextExcludedFromTargetProof",
    "excludedVisibleTextReason",
    "extraUndeclaredVisibleText",
    "finalTextAuditVerdict",
    "adjacentPartialTextFoundInCrop",
    "adjacentPartialGeometryFoundInCrop",
    "adjacentPartialTextAllowed",
    "adjacentPartialTextAllowanceReason",
    "cropLedgerContradictionCheck",
    "fullTargetBorderRadiusGlowIncluded",
    "fullTargetTextControlIncluded",
    "surroundingContextIncluded",
    "cropNotHidingAdjacentDefect",
    "contentValidationMethod",
}

CROP_TYPE_ELEMENT = "ELEMENT_CROP"
CROP_TYPE_RELATIONSHIP = "RELATIONSHIP_CROP"
VALID_CROP_TYPES = {
    CROP_TYPE_ELEMENT,
    CROP_TYPE_RELATIONSHIP,
    "FULL_WINDOW_CROP",
    "FULL_SHELL_CROP",
    "STATE_CROP",
    "RESIZE_STATE_CROP",
}
REQUIRED_CROP_TYPES = {
    "recording-window-chrome": "FULL_WINDOW_CROP",
    "recording-primary-action": "ELEMENT_CROP",
    "recording-target-truth": "ELEMENT_CROP",
    "recording-log-route": "ELEMENT_CROP",
    "log-viewer-window-chrome": "FULL_WINDOW_CROP",
    "native-log-destination-action": "ELEMENT_CROP",
    "exported-log-destination-action": "ELEMENT_CROP",
    "log-viewer-action-status": "STATE_CROP",
    "log-viewer-resize-before": "RESIZE_STATE_CROP",
    "log-viewer-resize-during": "RESIZE_STATE_CROP",
    "log-viewer-resize-after": "RESIZE_STATE_CROP",
}
REQUIRED_SCOPE_TEXT = {
    "recording-window-chrome": [
        "ACTIVE OVERLAY RECORDING",
        "RECORDING STUDIO",
        "START RECORDING",
        "TARGET",
        "Default Overlay Profile",
        "STATE",
        "Ready - 2 active monitors",
        "OPEN LOG VIEWER STUDIO",
    ],
    "recording-primary-action": ["START RECORDING"],
    "recording-target-truth": ["TARGET", "Default Overlay Profile", "STATE", "Ready - 2 active monitors"],
    "recording-log-route": ["OPEN LOG VIEWER STUDIO"],
    "log-viewer-window-chrome": [
        "RECORDING LOGS",
        "LOG VIEWER STUDIO",
        "VIEWER",
        "Deferred",
        "OPEN NATIVE LOGS",
        "OPEN EXPORTED LOGS",
    ],
    "native-log-destination-action": ["OPEN NATIVE LOGS"],
    "exported-log-destination-action": ["OPEN EXPORTED LOGS"],
    "log-viewer-action-status": [
        "VIEWER",
        "Deferred",
        "OPEN NATIVE LOGS",
        "OPEN EXPORTED LOGS",
    ],
    "log-viewer-resize-before": [
        "RECORDING LOGS",
        "LOG VIEWER STUDIO",
        "VIEWER",
        "Deferred",
        "OPEN NATIVE LOGS",
        "OPEN EXPORTED LOGS",
        "Exported logs folder could not be opened.",
    ],
    "log-viewer-resize-during": [
        "RECORDING LOGS",
        "LOG VIEWER STUDIO",
        "VIEWER",
        "Deferred",
        "OPEN NATIVE LOGS",
        "OPEN EXPORTED LOGS",
        "Exported logs folder could not be opened.",
    ],
    "log-viewer-resize-after": [
        "RECORDING LOGS",
        "LOG VIEWER STUDIO",
        "VIEWER",
        "Deferred",
        "OPEN NATIVE LOGS",
        "OPEN EXPORTED LOGS",
        "Exported logs folder could not be opened.",
    ],
}
CROP_DOM_KEYS = {
    "recording-window-chrome": "chrome",
    "recording-primary-action": "recordingPrimaryAction",
    "recording-target-truth": "recordingTargetTruth",
    "recording-log-route": "recordingLogRoute",
    "log-viewer-window-chrome": "chrome",
    "native-log-destination-action": "logViewerNativeAction",
    "exported-log-destination-action": "logViewerExportAction",
    "log-viewer-action-status": "logViewerActionStatus",
    "log-viewer-resize-before": "logViewerActionStatus",
    "log-viewer-resize-during": "logViewerActionStatus",
    "log-viewer-resize-after": "logViewerActionStatus",
}
CROP_SOURCE_LABELS = {
    "recording_default.png": "recording_default",
    "log_viewer_default.png": "log_viewer_default",
    "log_viewer_edge_resize_before_drag.png": "log_viewer_edge_resize_before_drag",
    "log_viewer_edge_resize_during_drag.png": "log_viewer_edge_resize_during_drag",
    "log_viewer_edge_resize_width_proof.png": "log_viewer_edge_resize_width_proof",
}

MIN_ROOT_CAUSE_UNIQUE_FIELDS = (
    "whyCodexMissedIt",
    "failedStep",
    "missingCheck",
    "repairMade",
    "proofNewCheckRejectsKnownBadExample",
)


@dataclass
class PacketInspection:
    label: str
    path: str
    accepted: bool
    failures: list[str]
    artifactSummary: dict[str, Any]


def _read_json(path: Path) -> tuple[dict[str, Any] | list[Any] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001 - validation reports exact parse failure
        return None, str(exc)


def _find_one(root: Path, pattern: str) -> Path | None:
    matches = sorted(root.glob(pattern))
    return matches[0] if matches else None


def _is_accepted_visual_target_packet(root: Path) -> bool:
    primary = root / "USER Review" / "CURRENT_BRANCH_VISUAL_ACCEPTANCE_TARGET_REVIEW.md"
    target = root / "Review Aids" / "Accepted Branch Visual Acceptance Target.json"
    lifecycle = root / "Review Aids" / "Visual Acceptance Lifecycle.md"
    if not primary.is_file() or not target.is_file() or not lifecycle.is_file():
        return False
    primary_text = primary.read_text(encoding="utf-8", errors="replace")
    lifecycle_text = lifecycle.read_text(encoding="utf-8", errors="replace")
    data, error = _read_json(target)
    return (
        error is None
        and isinstance(data, dict)
        and data.get("status") == "USER_ACCEPTED"
        and "branch-local-accepted-visual-target-review" in primary_text
        and "Implementation Match Proof" in lifecycle_text
        and "does not claim implementation match" in lifecycle_text
    )


def _is_full_desktop_false_green_packet(root: Path) -> bool:
    primary = root / "USER Review" / "FULL_DESKTOP_FALSE_GREEN_REVIEW.md"
    options = root / "Review Aids" / "VISUAL_AND_PLACEMENT_OPTIONS.md"
    media = root / "Review Aids" / "Evidence" / "Options" / "visual_and_placement_options_board.png"
    if not primary.is_file() or not options.is_file() or not media.is_file():
        return False
    primary_text = primary.read_text(encoding="utf-8", errors="replace")
    return "Packet Status: `full-desktop-visual-false-green-review`" in primary_text


def _image_size(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _rect_from_mapping(value: Any) -> tuple[int, int, int, int] | None:
    if not isinstance(value, dict):
        return None
    try:
        return (
            int(value["left"]),
            int(value["top"]),
            int(value["right"]),
            int(value["bottom"]),
        )
    except Exception:
        return None


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


def _source_label_for_row(row: dict[str, Any]) -> str:
    explicit = str(row.get("sourceDomBoundsLabel", "")).strip()
    if explicit:
        return explicit
    source = Path(str(row.get("sourceFullWindowFile", ""))).name
    return CROP_SOURCE_LABELS.get(source, Path(source).stem)


def _detect_adjacent_geometry(
    *,
    key: str,
    row: dict[str, Any],
    manifest: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not isinstance(manifest, dict):
        return []
    target_key = str(row.get("sourceDomBoundsKey") or CROP_DOM_KEYS.get(key, "")).strip()
    if target_key == "chrome":
        return []
    source_label = _source_label_for_row(row)
    dom_bounds = manifest.get("domBounds", {}).get(f"{source_label}_dom_bounds")
    if not isinstance(dom_bounds, dict):
        return []
    crop_rect = _rect_from_mapping(row.get("cropRect"))
    target_rect = _rect_from_mapping(row.get("targetElementRect"))
    if crop_rect is None or target_rect is None:
        return []
    findings: list[dict[str, Any]] = []
    for dom_key, payload in dom_bounds.items():
        if dom_key in {target_key, "chrome"} or not isinstance(payload, dict):
            continue
        other_rect = _rect_from_mapping(payload.get("rect"))
        if other_rect is None:
            continue
        overlap = _rect_intersection(crop_rect, other_rect)
        if overlap is None:
            continue
        if _rect_contains(target_rect, other_rect) or _rect_contains(other_rect, target_rect):
            continue
        findings.append(
            {
                "elementKey": dom_key,
                "elementText": str(payload.get("text", "")).strip(),
                "elementRect": _rect_dict(other_rect),
                "intersectionWithCrop": _rect_dict(overlap),
            }
        )
    return findings


def _validate_crop_completeness(
    row_map: dict[str, Any],
    manifest: dict[str, Any] | None,
    evidence_root: Path,
) -> list[str]:
    failures: list[str] = []
    checks = manifest.get("cropCompletenessChecks") if isinstance(manifest, dict) else None
    if not isinstance(checks, dict):
        failures.append("visual_capture_manifest.json missing cropCompletenessChecks object")
        checks = {}
    for key, rule in REQUIRED_CROP_COMPLETENESS.items():
        text = str(row_map.get(key, "")).strip()
        if not text:
            failures.append(f"crop completeness key {key} missing from row_to_evidence_map")
            continue
        target = evidence_root / text
        size = _image_size(target)
        if size is None:
            failures.append(f"crop completeness key {key} image unreadable")
            continue
        min_width = int(rule["minWidth"])
        min_height = int(rule["minHeight"])
        if size[0] < min_width or size[1] < min_height:
            failures.append(
                f"crop completeness key {key} image too small for complete focused proof: "
                f"{size[0]}x{size[1]} < {min_width}x{min_height}"
            )
        check = checks.get(key)
        if not isinstance(check, dict):
            failures.append(f"crop completeness key {key} missing manifest completeness record")
            continue
        crop_value = str(check.get("crop", "")).strip()
        if crop_value and crop_value != text:
            failures.append(f"crop completeness key {key} manifest crop path mismatch: {crop_value} != {text}")
        for required in rule["requires"]:
            if check.get(required) is not True:
                failures.append(f"crop completeness key {key} manifest flag {required} is not true")
        if check.get("noUndeclaredAdjacentPartialText") is not True:
            failures.append(f"crop completeness key {key} has undeclared adjacent partial text or lacks adjacent-text audit")
        overlay = str(check.get("overlayProofFile", "")).strip()
        if not overlay:
            failures.append(f"crop completeness key {key} missing overlayProofFile")
        elif Path(overlay).is_absolute():
            failures.append(f"crop completeness key {key} overlayProofFile is local absolute proof: {overlay}")
        elif not (evidence_root / overlay).exists():
            failures.append(f"crop completeness key {key} overlayProofFile missing from packet: {overlay}")
        method = str(check.get("contentValidationMethod", "")).casefold()
        if not all(token in method for token in ("dom", "overlay", "adjacent", "geometry", "text", "scope")):
            failures.append(f"crop completeness key {key} contentValidationMethod does not prove DOM/overlay/adjacent/geometry/text/scope validation")
        validator = str(check.get("validatedBy", "")).strip()
        if not validator or "overlay" not in validator.casefold() or "adjacent" not in validator.casefold():
            failures.append(f"crop completeness key {key} missing overlay/adjacent-aware validatedBy")
    return failures


def _validate_source_truth_context(root: Path) -> list[str]:
    context_root = root / "Source Truth Context"
    if not context_root.exists():
        return ["missing Source Truth Context folder"]
    names = {path.name for path in context_root.glob("*") if path.is_file()}
    missing = sorted(REQUIRED_SOURCE_TRUTH_CONTEXT_FILES - names)
    if missing:
        return [f"Source Truth Context missing required files: {', '.join(missing)}"]
    return []


def _validate_crop_ledger(root: Path, row_map: dict[str, Any], manifest: dict[str, Any] | None, evidence_root: Path) -> list[str]:
    failures: list[str] = []
    ledger_path = _find_one(root, "Review Aids/Evidence/**/crop_completeness_ledger.json")
    if ledger_path is None:
        return ["missing crop_completeness_ledger.json"]
    data, error = _read_json(ledger_path)
    rows = data.get("rows", []) if isinstance(data, dict) else []
    if error or not isinstance(data, dict) or not isinstance(rows, list):
        return [f"invalid crop_completeness_ledger.json: {error}"]
    if data.get("status") != "PASS":
        failures.append("crop completeness ledger status is not PASS")
    rows_by_key = {str(row.get("key", "")): row for row in rows if isinstance(row, dict)}
    checks = (manifest or {}).get("cropCompletenessChecks", {})
    if not isinstance(checks, dict):
        checks = {}
    required_fields = {
        "cropFile",
        "sourceFullWindowFile",
        "sourceImageSize",
        "cropRect",
        "targetElementRect",
        "cropSize",
        "marginAroundTarget",
        "expectedTextInsideCrop",
        "textPresenceCheck",
        "borderRadiusGlowInclusionCheck",
        "surroundingContextCheck",
        "cropTouchesSourceImageEdge",
        "targetContentTouchesCropEdge",
        "targetTextControlOrBorderCutOff",
        "finalCropVerdict",
    }
    required_fields |= REQUIRED_CROP_CONTENT_FIELDS
    for key in REQUIRED_CROP_COMPLETENESS:
        row = rows_by_key.get(key)
        if not isinstance(row, dict):
            failures.append(f"crop completeness ledger missing row for {key}")
            continue
        missing = sorted(required_fields - set(row))
        if missing:
            failures.append(f"crop completeness ledger row {key} missing fields: {', '.join(missing)}")
        if row.get("cropFile") != row_map.get(key):
            failures.append(f"crop completeness ledger row {key} cropFile does not match row_to_evidence_map")
        overlay_file = str(row.get("overlayProofFile", "")).strip()
        if not overlay_file:
            failures.append(f"crop completeness ledger row {key} missing overlayProofFile")
        elif Path(overlay_file).is_absolute():
            failures.append(f"crop completeness ledger row {key} overlayProofFile is local absolute primary proof: {overlay_file}")
        elif not (evidence_root / overlay_file).exists():
            failures.append(f"crop completeness ledger row {key} overlayProofFile target missing from packet: {overlay_file}")
        source_file = str(row.get("sourceFullWindowFile", "")).strip()
        if not source_file:
            failures.append(f"crop completeness ledger row {key} missing sourceFullWindowFile")
        elif Path(source_file).is_absolute():
            failures.append(f"crop completeness ledger row {key} sourceFullWindowFile is local absolute primary proof: {source_file}")
        elif source_file not in row_map.values():
            failures.append(f"crop completeness ledger row {key} sourceFullWindowFile is not packet row-map proof: {source_file}")
        elif not (evidence_root / source_file).exists():
            failures.append(f"crop completeness ledger row {key} sourceFullWindowFile target missing from packet: {source_file}")
        if row.get("finalCropVerdict") != "PERFECT_PASS":
            failures.append(f"crop completeness ledger row {key} is not PERFECT_PASS")
        crop_type = str(row.get("cropType", "")).strip()
        if crop_type not in VALID_CROP_TYPES:
            failures.append(f"crop completeness ledger row {key} has invalid or missing cropType: {crop_type or '<missing>'}")
            crop_type = CROP_TYPE_ELEMENT
        required_crop_type = REQUIRED_CROP_TYPES.get(key)
        if required_crop_type and crop_type != required_crop_type:
            failures.append(
                f"crop completeness ledger row {key} cropType mismatch: "
                f"{crop_type} != required {required_crop_type}"
            )
        declared_scope = str(row.get("declaredTargetScope", "")).strip()
        if not declared_scope:
            failures.append(f"crop completeness ledger row {key} missing declaredTargetScope")
        included_adjacent = row.get("includedAdjacentElements")
        if not isinstance(included_adjacent, list):
            failures.append(f"crop completeness ledger row {key} missing includedAdjacentElements list")
            included_adjacent = []
        included_rects = row.get("includedElementRects")
        if not isinstance(included_rects, list):
            failures.append(f"crop completeness ledger row {key} missing includedElementRects list")
            included_rects = []
        relationship = str(row.get("relationshipBeingProven", "")).strip()
        if crop_type in {CROP_TYPE_RELATIONSHIP, "STATE_CROP", "RESIZE_STATE_CROP"} and not relationship:
            failures.append(f"relationship crop {key} does not name the relationship being proven")
        if crop_type == CROP_TYPE_ELEMENT and (included_adjacent or relationship or included_rects):
            failures.append(f"element crop {key} declares relationship/adjacent elements instead of staying clean")
        if crop_type in {CROP_TYPE_RELATIONSHIP, "STATE_CROP", "RESIZE_STATE_CROP"} and not included_adjacent:
            failures.append(f"{crop_type} row {key} does not declare included elements")
        expected_text = row.get("expectedTextInsideCrop")
        if not isinstance(expected_text, list) or not expected_text or not all(str(item).strip() for item in expected_text):
            failures.append(f"crop completeness ledger row {key} missing expected text list")
            expected_text = []
        visible_text = row.get("allVisibleTextFoundInCrop")
        if not isinstance(visible_text, list) or not visible_text:
            failures.append(f"crop completeness ledger row {key} missing allVisibleTextFoundInCrop")
            visible_text = []
        required_scope_text = REQUIRED_SCOPE_TEXT.get(key, [])
        normalized_expected = {str(item).casefold().strip() for item in expected_text if str(item).strip()}
        for required_text in required_scope_text:
            if required_text.casefold().strip() not in normalized_expected:
                failures.append(
                    f"crop completeness ledger row {key} expectedTextInsideCrop omits required visible scope text: "
                    f"{required_text}"
                )
        joined_visible_text = " ".join(str(item) for item in visible_text).casefold()
        if isinstance(expected_text, list):
            for text in expected_text:
                if str(text).casefold() not in joined_visible_text:
                    failures.append(f"crop completeness ledger row {key} expected text not found in visible-text audit: {text}")
        for required_text in required_scope_text:
            if required_text.casefold() not in joined_visible_text:
                failures.append(
                    f"crop completeness ledger row {key} required scope text not found in allVisibleTextFoundInCrop: "
                    f"{required_text}"
                )
        excluded_text = row.get("visibleTextExcludedFromTargetProof")
        if not isinstance(excluded_text, list):
            failures.append(f"crop completeness ledger row {key} missing visibleTextExcludedFromTargetProof list")
            excluded_text = []
        exclusion_reason = str(row.get("excludedVisibleTextReason", "")).strip()
        if excluded_text and not exclusion_reason:
            failures.append(f"crop completeness ledger row {key} excludes visible text without reason")
        extra_text = row.get("extraUndeclaredVisibleText")
        if not isinstance(extra_text, list):
            failures.append(f"crop completeness ledger row {key} missing extraUndeclaredVisibleText list")
            extra_text = []
        if extra_text:
            failures.append(
                f"crop completeness ledger row {key} has visible text neither expected nor excluded: "
                f"{', '.join(str(item) for item in extra_text)}"
            )
        if row.get("finalTextAuditVerdict") != "PERFECT_PASS":
            failures.append(f"crop completeness ledger row {key} finalTextAuditVerdict is not PERFECT_PASS")
        adjacent = row.get("adjacentPartialTextFoundInCrop")
        if not isinstance(adjacent, list):
            failures.append(f"crop completeness ledger row {key} missing adjacentPartialTextFoundInCrop list")
            adjacent = []
        if adjacent and row.get("adjacentPartialTextAllowed") is not True:
            failures.append(f"crop completeness ledger row {key} has undeclared adjacent partial text: {', '.join(str(item) for item in adjacent)}")
        adjacent_geometry = row.get("adjacentPartialGeometryFoundInCrop")
        if not isinstance(adjacent_geometry, list):
            failures.append(f"crop completeness ledger row {key} missing adjacentPartialGeometryFoundInCrop list")
            adjacent_geometry = []
        detected_geometry = _detect_adjacent_geometry(key=key, row=row, manifest=manifest)
        if detected_geometry and not adjacent_geometry:
            failures.append(
                f"crop completeness ledger row {key} overlay/crop contradiction: crop intersects adjacent DOM elements "
                f"but adjacentPartialGeometryFoundInCrop is empty: "
                f"{', '.join(str(item.get('elementKey')) for item in detected_geometry)}"
            )
        if detected_geometry and crop_type == CROP_TYPE_ELEMENT:
            failures.append(
                f"element crop {key} contains undeclared adjacent geometry outside target rectangle: "
                f"{', '.join(str(item.get('elementKey')) for item in detected_geometry)}"
            )
        if detected_geometry and row.get("adjacentPartialTextAllowed") is not True:
            failures.append(
                f"crop completeness ledger row {key} includes adjacent geometry but adjacent content is not declared/allowed"
            )
        declared_geometry_keys = {
            str(item.get("elementKey", "")).strip()
            for item in adjacent_geometry
            if isinstance(item, dict)
        }
        detected_geometry_keys = {
            str(item.get("elementKey", "")).strip()
            for item in detected_geometry
            if isinstance(item, dict)
        }
        missing_detected_keys = sorted(detected_geometry_keys - declared_geometry_keys)
        if missing_detected_keys:
            failures.append(
                f"crop completeness ledger row {key} misses overlay-detected adjacent geometry keys: "
                f"{', '.join(missing_detected_keys)}"
            )
        contradiction = row.get("cropLedgerContradictionCheck")
        if not isinstance(contradiction, dict):
            failures.append(f"crop completeness ledger row {key} missing cropLedgerContradictionCheck object")
        else:
            if contradiction.get("overlayMatchesLedger") is not True:
                failures.append(f"crop completeness ledger row {key} overlay does not match ledger")
            if detected_geometry and contradiction.get("detectedAdjacentGeometryCount") != len(detected_geometry):
                failures.append(
                    f"crop completeness ledger row {key} contradiction check does not count overlay-detected adjacent geometry"
                )
        if row.get("fullTargetBorderRadiusGlowIncluded") is not True:
            failures.append(f"crop completeness ledger row {key} does not prove full target border/radius/glow included")
        if row.get("fullTargetTextControlIncluded") is not True:
            failures.append(f"crop completeness ledger row {key} does not prove full target text/control included")
        if row.get("surroundingContextIncluded") is not True:
            failures.append(f"crop completeness ledger row {key} does not prove surrounding context included")
        if row.get("cropNotHidingAdjacentDefect") is not True:
            failures.append(f"crop completeness ledger row {key} may hide an adjacent spacing/alignment defect")
        if detected_geometry and row.get("cropNotHidingAdjacentDefect") is True and crop_type == CROP_TYPE_ELEMENT:
            failures.append(
                f"crop completeness ledger row {key} says cropNotHidingAdjacentDefect=true while overlay shows adjacent geometry"
            )
        method = str(row.get("contentValidationMethod", "")).casefold()
        if not all(token in method for token in ("dom", "overlay", "adjacent", "geometry", "text", "scope")):
            failures.append(f"crop completeness ledger row {key} contentValidationMethod is not DOM/overlay/adjacent/geometry/text/scope backed")
        for rect_name in ("cropRect", "targetElementRect"):
            rect = row.get(rect_name)
            if not isinstance(rect, dict) or not all(name in rect for name in ("left", "top", "right", "bottom")):
                failures.append(f"crop completeness ledger row {key} missing {rect_name} coordinates")
        margin = row.get("marginAroundTarget")
        if not isinstance(margin, dict) or not all(name in margin for name in ("left", "top", "right", "bottom")):
            failures.append(f"crop completeness ledger row {key} missing marginAroundTarget values")
        else:
            minimum_margin = 0 if crop_type in {"FULL_WINDOW_CROP", "STATE_CROP", "RESIZE_STATE_CROP"} else 8
            if any(int(margin[name]) < minimum_margin for name in ("left", "top", "right", "bottom")):
                failures.append(f"crop completeness ledger row {key} margin too tight: {margin}")
        if row.get("targetContentTouchesCropEdge") is True or row.get("targetTextControlOrBorderCutOff") is True:
            failures.append(f"crop completeness ledger row {key} says target touches edge or is cut off")
        check = checks.get(key)
        if not isinstance(check, dict) or check.get("cropCompletenessLedgerKey") != key:
            failures.append(f"crop completeness manifest check for {key} lacks cropCompletenessLedgerKey")
        target = evidence_root / str(row_map.get(key, ""))
        if not target.exists():
            failures.append(f"crop completeness ledger row {key} target media missing from packet")
    return failures


def _crop_key_complete(
    row_map: dict[str, Any],
    manifest: dict[str, Any] | None,
    evidence_root: Path,
    key: str,
) -> bool:
    rule = REQUIRED_CROP_COMPLETENESS.get(key)
    if rule is None:
        return True
    text = str(row_map.get(key, "")).strip()
    if not text:
        return False
    target = evidence_root / text
    size = _image_size(target)
    if size is None:
        return False
    if size[0] < int(rule["minWidth"]) or size[1] < int(rule["minHeight"]):
        return False
    checks = (manifest or {}).get("cropCompletenessChecks", {})
    if not isinstance(checks, dict):
        return False
    check = checks.get(key)
    if not isinstance(check, dict):
        return False
    if str(check.get("crop", "")).strip() != text:
        return False
    overlay = str(check.get("overlayProofFile", "")).strip()
    validator = str(check.get("validatedBy", "")).casefold()
    return (
        all(check.get(required) is True for required in rule["requires"])
        and check.get("noUndeclaredAdjacentPartialText") is True
        and bool(overlay)
        and not Path(overlay).is_absolute()
        and (evidence_root / overlay).exists()
        and "overlay" in validator
        and "adjacent" in validator
    )


def _validate_comparator_crop_ledger(
    root: Path,
    row_map: dict[str, Any],
    evidence_root: Path,
) -> list[str]:
    failures: list[str] = []
    ledger_path = _find_one(root, "Review Aids/Evidence/**/comparator_crop_ledger.json")
    if ledger_path is None:
        return ["missing comparator_crop_ledger.json"]
    data, error = _read_json(ledger_path)
    rows = data.get("rows", []) if isinstance(data, dict) else []
    if error or not isinstance(data, dict) or not isinstance(rows, list):
        return [f"invalid comparator_crop_ledger.json: {error}"]
    if data.get("status") != "PASS":
        failures.append("comparator crop ledger status is not PASS")
    if data.get("duplicateHashGroups"):
        failures.append(f"comparator crop ledger reports duplicate hash groups: {data.get('duplicateHashGroups')}")
    rows_by_key = {
        str(row.get("comparatorEvidenceKey", "")): row
        for row in rows
        if isinstance(row, dict)
    }
    missing_rows = sorted(set(COMPARATOR_CROP_RULES) - set(rows_by_key))
    if missing_rows:
        failures.append(f"comparator crop ledger missing rows: {', '.join(missing_rows)}")
    seen_hashes: dict[str, list[str]] = {}
    for key, rule in COMPARATOR_CROP_RULES.items():
        row = rows_by_key.get(key)
        if not isinstance(row, dict):
            continue
        crop_file = str(row.get("comparatorCropFile", "")).strip()
        if crop_file != str(row_map.get(key, "")).strip():
            failures.append(f"comparator crop ledger row {key} crop file does not match row map")
        if not crop_file or Path(crop_file).is_absolute():
            failures.append(f"comparator crop ledger row {key} crop file is missing or absolute")
            crop_path = evidence_root / "__missing__"
        else:
            crop_path = evidence_root / crop_file
            if not crop_path.exists():
                failures.append(f"comparator crop ledger row {key} crop file missing from packet: {crop_file}")
            elif crop_path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                size = _image_size(crop_path)
                if size is None:
                    failures.append(f"comparator crop ledger row {key} crop image unreadable")
                else:
                    width, height = size
                    if width < int(rule["minWidth"]) or height < int(rule["minHeight"]):
                        failures.append(f"comparator crop ledger row {key} crop too small: {width}x{height}")
                    if width > int(rule["maxWidth"]) or height > int(rule["maxHeight"]):
                        failures.append(f"comparator crop ledger row {key} crop too broad: {width}x{height}")
                    actual_hash = _file_sha256(crop_path)
                    seen_hashes.setdefault(actual_hash, []).append(key)
                    declared_hash = str(row.get("sha256", "")).strip().upper()
                    if declared_hash and declared_hash != actual_hash:
                        failures.append(f"comparator crop ledger row {key} sha256 does not match packet media")
                    elif not declared_hash:
                        failures.append(f"comparator crop ledger row {key} missing sha256")
        overlay = str(row.get("comparatorOverlayProofFile", "")).strip()
        if not overlay:
            failures.append(f"comparator crop ledger row {key} missing comparatorOverlayProofFile")
        elif Path(overlay).is_absolute():
            failures.append(f"comparator crop ledger row {key} overlay path is absolute")
        elif not (evidence_root / overlay).exists():
            failures.append(f"comparator crop ledger row {key} overlay proof missing from packet: {overlay}")
        source = str(row.get("comparatorSourceScreenshot", "")).strip()
        if not source:
            failures.append(f"comparator crop ledger row {key} missing comparatorSourceScreenshot")
        elif Path(source).is_absolute():
            failures.append(f"comparator crop ledger row {key} source screenshot path is absolute")
        elif not (evidence_root / source).exists():
            failures.append(f"comparator crop ledger row {key} source screenshot missing from packet: {source}")
        if str(row.get("cropType", "")).strip() != str(rule["cropType"]):
            failures.append(
                f"comparator crop ledger row {key} cropType mismatch: {row.get('cropType')} != {rule['cropType']}"
            )
        if str(row.get("broadContextOrFocusedProof", "")).strip() != str(rule["proofKind"]):
            failures.append(
                f"comparator crop ledger row {key} proof kind mismatch: "
                f"{row.get('broadContextOrFocusedProof')} != {rule['proofKind']}"
            )
        for required in (
            "targetPrimitive",
            "proofScope",
            "visiblePrimitiveContent",
            "cropRect",
            "targetPrimitiveRect",
            "cropSize",
        ):
            if required not in row or not str(row.get(required, "")).strip():
                failures.append(f"comparator crop ledger row {key} missing {required}")
        if row.get("contentMatchesEvidenceKey") is not True:
            failures.append(f"comparator crop ledger row {key} contentMatchesEvidenceKey is not true")
        if row.get("overlayRectangleProofPresent") is not True:
            failures.append(f"comparator crop ledger row {key} overlayRectangleProofPresent is not true")
        if row.get("readableAtElementLevel") is not True:
            failures.append(f"comparator crop ledger row {key} readableAtElementLevel is not true")
        if row.get("finalComparatorCropVerdict") != "PERFECT_PASS":
            failures.append(f"comparator crop ledger row {key} is not PERFECT_PASS")
    for digest, keys in seen_hashes.items():
        if len(keys) > 1:
            failures.append(
                f"duplicate comparator media hash {digest[:12]} reused across incompatible keys: {', '.join(keys)}"
            )
    return failures


def _validate_b2_placement_proof(
    row_map: dict[str, Any],
    evidence_root: Path,
) -> list[str]:
    failures: list[str] = []
    proof_rel = str(row_map.get("b2-placement-proof-json", "") or "").strip()
    if not proof_rel:
        return ["B2 placement proof JSON is missing from row_to_evidence_map"]
    if Path(proof_rel).is_absolute():
        return ["B2 placement proof JSON path is absolute/local-only"]
    proof_path = evidence_root / proof_rel
    data, error = _read_json(proof_path)
    if error or not isinstance(data, dict):
        return [f"invalid B2 placement proof JSON: {error}"]
    if data.get("selectedDirection") != "B2":
        failures.append("B2 placement proof selectedDirection is not B2")
    if data.get("status") != "MATCH":
        failures.append("B2 placement proof status is not MATCH")
    for field in (
        "defaultParentNeighbor",
        "freshWindowNewSessionSubstituteParentNeighbor",
        "sameSessionMovedPositionRestored",
    ):
        if data.get(field) is not True:
            failures.append(f"B2 placement proof missing true {field}")
    rows = data.get("rows", [])
    if not isinstance(rows, list) or len(rows) < 3:
        failures.append("B2 placement proof must include default, same-session, and fresh/new-session rows")
        rows = []
    rows_by_scenario = {
        str(row.get("scenario", "")): row
        for row in rows
        if isinstance(row, dict)
    }
    for scenario, key, require_near_parent in (
        ("default-parent-neighbor", "b2-default-parent-neighbor-full-desktop", True),
        ("same-session-moved-after-reopen", "b2-same-session-moved-restore-full-desktop", False),
        ("fresh-window-new-session-substitute", "b2-fresh-window-new-session-full-desktop", True),
    ):
        row = rows_by_scenario.get(scenario)
        if not row:
            failures.append(f"B2 placement proof missing scenario row {scenario}")
            continue
        screenshot_rel = str(row.get("screenshot", "") or "").strip()
        mapped_rel = str(row_map.get(key, "") or "").strip()
        if not mapped_rel:
            failures.append(f"row_to_evidence_map missing {key}")
        elif Path(mapped_rel).is_absolute():
            failures.append(f"row_to_evidence_map key {key} uses local absolute path")
        elif not (evidence_root / mapped_rel).exists():
            failures.append(f"row_to_evidence_map key {key} target missing: {mapped_rel}")
        if screenshot_rel and mapped_rel and screenshot_rel != mapped_rel:
            failures.append(f"B2 scenario {scenario} screenshot does not match row map key {key}")
        for boolean_field in (
            "parentVisible",
            "recordingVisibleUsable",
            "logViewerVisibleUsable",
            "childrenDoNotOverlapEachOther",
            "childrenDoNotOverlapParent",
        ):
            if row.get(boolean_field) is not True:
                failures.append(f"B2 scenario {scenario} missing true {boolean_field}")
        if require_near_parent:
            for boolean_field in ("recordingNearParent", "logViewerNearParent"):
                if row.get(boolean_field) is not True:
                    failures.append(f"B2 scenario {scenario} missing true {boolean_field}")
    moved_before = data.get("movedBeforeClose", {})
    moved_after = data.get("movedAfterReopen", {})
    if not isinstance(moved_before, dict) or not isinstance(moved_after, dict):
        failures.append("B2 placement proof missing moved before/after objects")
    else:
        if moved_before.get("recordingRect") != moved_after.get("recordingRect"):
            failures.append("B2 same-session Recording Studio moved geometry did not restore")
        if moved_before.get("logViewerRect") != moved_after.get("logViewerRect"):
            failures.append("B2 same-session Log Viewer Studio moved geometry did not restore")
    return failures


def _inspect_packet_root(root: Path, label: str) -> PacketInspection:
    failures: list[str] = []
    failures.extend(_validate_source_truth_context(root))
    failures.extend(f"packet text hygiene: {failure}" for failure in scan_packet_text_hygiene(root))
    is_known_bad = label.startswith("known-bad:")
    if not is_known_bad and _is_full_desktop_false_green_packet(root):
        packet_failures = validate_full_desktop_false_green_packet(root)
        failures.extend(f"full-desktop false-green packet: {failure}" for failure in packet_failures)
        option_media = sorted((root / "Review Aids" / "Evidence" / "Options").glob("*.png"))
        return PacketInspection(
            label=label,
            path=str(root),
            accepted=not failures,
            failures=failures,
            artifactSummary={
                "packetClass": "full-desktop-visual-false-green-review",
                "optionMediaCount": len(option_media),
                "runtimeImplementationProofRequired": "separate USER-selected implementation-match repair; not claimed by this packet",
            },
        )
    if not is_known_bad and _is_accepted_visual_target_packet(root):
        target_failures = validate_visual_acceptance_target_packet(root)
        failures.extend(f"accepted visual target packet: {failure}" for failure in target_failures)
        target_json = root / "Review Aids" / "Accepted Branch Visual Acceptance Target.json"
        accepted_media = sorted((root / "Review Aids" / "Accepted Visual Target" / "media").glob("*.png"))
        return PacketInspection(
            label=label,
            path=str(root),
            accepted=not failures,
            failures=failures,
            artifactSummary={
                "packetClass": "accepted-visual-target",
                "acceptedTargetJson": str(target_json),
                "acceptedTargetMediaCount": len(accepted_media),
                "runtimeImplementationProofRequired": "separate implementation-match packet; not claimed by this accepted target packet",
            },
        )
    evidence_roots = sorted((root / "Review Aids" / "Evidence").glob("*")) if (root / "Review Aids" / "Evidence").exists() else []
    evidence_root = next((path for path in evidence_roots if path.is_dir()), None)
    if evidence_root is None:
        failures.append("missing Review Aids/Evidence proof root")
        evidence_root = root

    row_map_path = _find_one(root, "Review Aids/Evidence/**/row_to_evidence_map.json")
    manifest_path = _find_one(root, "Review Aids/Evidence/**/visual_capture_manifest.json")
    red_team_path = _find_one(root, "Review Aids/Evidence/**/internal_visual_red_team_ledger.json")
    root_cause_path = _find_one(root, "Review Aids/Evidence/**/adjudication_failure_root_cause_ledger.json")
    visual_ledger_path = _find_one(root, "Review Aids/exhaustive_visual_conformance_ledger.json")
    embedded_udl_path = _find_one(root, "Review Aids/Unified Defect Ledger/unified_defect_ledger.json")
    embedded_incident_path = _find_one(root, "Review Aids/Unified Defect Ledger/false_green_incident_ledger.json")
    if embedded_udl_path is not None or embedded_incident_path is not None:
        if embedded_udl_path is None:
            failures.append("packet has incident ledger but missing unified_defect_ledger.json")
        else:
            data, error = _read_json(embedded_udl_path)
            defects = data.get("defects", []) if isinstance(data, dict) else []
            defect_ids = {str(row.get("defectId", "")) for row in defects if isinstance(row, dict)}
            if error or not isinstance(data, dict) or not isinstance(defects, list):
                failures.append(f"invalid embedded unified_defect_ledger.json: {error}")
            for required_id in (
                "FAM006-UDL-012",
                "FAM006-UDL-013",
                "FAM006-UDL-014",
                "FAM006-UDL-015",
                "FAM006-UDL-016",
                "FAM006-UDL-017",
            ):
                if required_id not in defect_ids:
                    failures.append(f"embedded UDL missing latest false-green defect {required_id}")
            sweep_values: dict[str, list[str]] = {}
            generic_sweep = (
                "Adjacent proof path inspected: packet evidence, crop/overlay/text/scope, "
                "visual ledger, red-team/root-cause row, false-ACCEPT gate."
            )
            for row in defects:
                if not isinstance(row, dict):
                    continue
                defect_id = str(row.get("defectId", "<missing>"))
                sweep = str(row.get("adjacentDefectSweepResult", "")).strip()
                sweep_values.setdefault(sweep, []).append(defect_id)
                if sweep == generic_sweep:
                    failures.append(f"{defect_id}: embedded UDL adjacent sweep is generic copied text")
                if not all(
                    token in sweep.casefold()
                    for token in ("adjacent", "surfaces", "proof", "validator", "additional", "defects", "repair scope")
                ):
                    failures.append(f"{defect_id}: embedded UDL adjacent sweep is not row-specific/substantive")
            for sweep, ids in sweep_values.items():
                if sweep and len(ids) > 1:
                    failures.append(
                        "embedded UDL duplicate adjacent sweep across unrelated defects: "
                        + ", ".join(ids)
                    )
        if embedded_incident_path is None:
            failures.append("packet has UDL but missing false_green_incident_ledger.json")
        else:
            data, error = _read_json(embedded_incident_path)
            incidents = data.get("incidents", []) if isinstance(data, dict) else []
            if error or not isinstance(data, dict) or not isinstance(incidents, list):
                failures.append(f"invalid embedded false_green_incident_ledger.json: {error}")
            elif len(incidents) < 11:
                failures.append(f"embedded false-green incident ledger is generic: expected at least 11 rows, found {len(incidents)}")
            covered = {
                str(row.get("packetPathOrReconstructedRecord", ""))
                for row in incidents
                if isinstance(row, dict)
            }
            if not any("071500" in item for item in covered):
                failures.append("embedded false-green incident ledger missing 071500 reconstructed-known-bad incident")
            if not any("113615" in item for item in covered):
                failures.append("embedded false-green incident ledger missing 113615 UDL false-green incident")
            if not any("120234" in item for item in covered):
                failures.append("embedded false-green incident ledger missing 120234 packet text-hygiene incident")
            if not any("121602" in item for item in covered):
                failures.append("embedded false-green incident ledger missing 121602 packet text-hygiene incident")
            if not any("123110" in item for item in covered):
                failures.append("embedded false-green incident ledger missing 123110 source-context/adjacent-sweep incident")
            for index, row in enumerate(incidents, start=1):
                if not isinstance(row, dict):
                    failures.append(f"embedded false-green incident row {index} is not an object")
                    continue
                for field in (
                    "incidentId",
                    "packetPathOrReconstructedRecord",
                    "packetSha256",
                    "head",
                    "codexClaim",
                    "userOrChatGPTRejection",
                    "validatorFailed",
                    "insufficientProofArtifact",
                    "overclaimedLedgerRow",
                    "missedOrMisusedComparator",
                    "fam006PreventionAdded",
                    "linkedDefectIds",
                    "finalIncidentStatus",
                ):
                    if row.get(field) in (None, "", []):
                        failures.append(f"embedded false-green incident row {index} missing {field}")
                if len(row.get("linkedDefectIds", [])) > 3:
                    failures.append(f"embedded false-green incident row {index} is generic and links too many defects")

    row_map: dict[str, Any] = {}
    manifest_data: dict[str, Any] | None = None
    if row_map_path is None:
        failures.append("missing row_to_evidence_map.json")
    else:
        data, error = _read_json(row_map_path)
        if error or not isinstance(data, dict):
            failures.append(f"invalid row_to_evidence_map.json: {error}")
        else:
            row_map = data
            missing = sorted(REQUIRED_EVIDENCE_KEYS - set(row_map))
            if missing:
                failures.append(f"row_to_evidence_map missing keys: {', '.join(missing)}")
            for key, value in sorted(row_map.items()):
                text = str(value or "").strip()
                if not text:
                    failures.append(f"row_to_evidence_map key {key} has empty path")
                    continue
                if Path(text).is_absolute():
                    failures.append(f"row_to_evidence_map key {key} uses local absolute path")
                    continue
                target = row_map_path.parent / text
                if not target.exists():
                    failures.append(f"row_to_evidence_map key {key} target missing: {text}")
                    continue
                if target.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                    size = _image_size(target)
                    if size is None:
                        failures.append(f"row_to_evidence_map key {key} image unreadable")
                    elif key in REQUIRED_CROP_COMPLETENESS:
                        rule = REQUIRED_CROP_COMPLETENESS[key]
                        if size[0] < int(rule["minWidth"]) or size[1] < int(rule["minHeight"]):
                            failures.append(
                                f"row_to_evidence_map key {key} image too small/clipped: {size[0]}x{size[1]}"
                            )
                    elif key in COMPARATOR_CROP_RULES:
                        rule = COMPARATOR_CROP_RULES[key]
                        if size[0] < int(rule["minWidth"]) or size[1] < int(rule["minHeight"]):
                            failures.append(
                                f"comparator evidence key {key} image too small for scope: "
                                f"{size[0]}x{size[1]} < {rule['minWidth']}x{rule['minHeight']}"
                            )
                        if size[0] > int(rule["maxWidth"]) or size[1] > int(rule["maxHeight"]):
                            failures.append(
                                f"comparator evidence key {key} image too broad for scope: "
                                f"{size[0]}x{size[1]} > {rule['maxWidth']}x{rule['maxHeight']}"
                            )
                    elif key != "contact-sheet" and (size[0] < 220 or size[1] < 60):
                        failures.append(f"row_to_evidence_map key {key} image too small/clipped: {size[0]}x{size[1]}")

    if manifest_path is None:
        failures.append("missing visual_capture_manifest.json")
    else:
        data, error = _read_json(manifest_path)
        if error or not isinstance(data, dict):
            failures.append(f"invalid visual_capture_manifest.json: {error}")
        else:
            manifest_data = data
            resize = data.get("resizeProof", {})
            if not isinstance(resize, dict):
                failures.append("resizeProof missing object")
            else:
                method = str(resize.get("method", ""))
                runtime_truth = str(resize.get("runtimeTruth", ""))
                if "runtime-widget-edge" not in method and "fixed-size-source-truth" not in method:
                    failures.append(f"resize proof method is not runtime-edge or fixed-size source-truth: {method}")
                if resize.get("directGeometrySetUsed") is True or method in {"setGeometry-only", "scripted-resize-call"}:
                    failures.append("resize proof uses direct/scripted geometry as primary proof")
                if method.startswith("runtime-widget-edge") and not resize.get("widthIncreased"):
                    failures.append("resize proof does not prove width increased")
                if "exact-desktop-launcher-live-validation-still-required" not in runtime_truth:
                    failures.append("resize proof does not preserve exact desktop launcher LV boundary")

    if row_map_path is not None and row_map:
        failures.extend(_validate_crop_completeness(row_map, manifest_data, row_map_path.parent))
        failures.extend(_validate_crop_ledger(root, row_map, manifest_data, row_map_path.parent))
        failures.extend(_validate_comparator_crop_ledger(root, row_map, row_map_path.parent))
        failures.extend(_validate_b2_placement_proof(row_map, row_map_path.parent))

    if red_team_path is None:
        failures.append("missing internal_visual_red_team_ledger.json")
    else:
        data, error = _read_json(red_team_path)
        rows = data.get("rows", []) if isinstance(data, dict) else []
        if error or not isinstance(data, dict) or not isinstance(rows, list):
            failures.append(f"invalid internal_visual_red_team_ledger.json: {error}")
        else:
            if len(rows) < 12:
                failures.append(f"internal red-team ledger row count too low: {len(rows)}")
            dispositions = [str(row.get("finalDisposition", "")) for row in rows if isinstance(row, dict)]
            known_bad_proven = data.get("knownBadRegressionRejected") is True
            if rows and all(disposition == "PERFECT_PASS" for disposition in dispositions) and not known_bad_proven:
                failures.append("internal red-team ledger is all PERFECT_PASS and lacks negative repair/adjudication branches")
            defect_classes = {
                str(row.get("defectClass", "")).strip()
                for row in rows
                if isinstance(row, dict) and str(row.get("defectClass", "")).strip()
            }
            missing_classes = sorted(REQUIRED_RED_TEAM_DEFECT_CLASSES - defect_classes)
            if missing_classes:
                failures.append(f"internal red-team ledger missing defect classes: {', '.join(missing_classes)}")
            for index, row in enumerate(rows, start=1):
                if not isinstance(row, dict):
                    failures.append(f"internal red-team row {index} is not an object")
                    continue
                missing = REQUIRED_RED_TEAM_FIELDS - set(row)
                if missing:
                    failures.append(f"internal red-team row {index} missing fields: {', '.join(sorted(missing))}")
                if row.get("finalDisposition") == "REPAIR_REQUIRED":
                    failures.append(f"internal red-team row {index} remains REPAIR_REQUIRED")
                adjudicated_text = " ".join(
                    str(row.get(field, ""))
                    for field in ("observedFinding", "whyDefectAbsentIfPass", "exactRepairIfRequired")
                ).casefold()
                if any(term in adjudicated_text for term in FORBIDDEN_PRODUCT_COPY) and row.get("finalDisposition") == "PERFECT_PASS":
                    failures.append(f"internal red-team row {index} marks forbidden product copy as PERFECT_PASS")
                if "could not be opened" in adjudicated_text and "ready" in adjudicated_text and row.get("finalDisposition") == "PERFECT_PASS":
                    failures.append(f"internal red-team row {index} marks card/footer ready-vs-blocked contradiction as PERFECT_PASS")

    if root_cause_path is None:
        failures.append("missing adjudication_failure_root_cause_ledger.json")
    else:
        data, error = _read_json(root_cause_path)
        defects = data.get("defects", []) if isinstance(data, dict) else []
        if error or not isinstance(data, dict) or not isinstance(defects, list):
            failures.append(f"invalid adjudication_failure_root_cause_ledger.json: {error}")
        else:
            if len(defects) < 10:
                failures.append(f"root-cause defect row count too low: {len(defects)}")
            if len(defects) >= 2:
                for field in MIN_ROOT_CAUSE_UNIQUE_FIELDS:
                    unique = {
                        str(row.get(field, "")).strip()
                        for row in defects
                        if isinstance(row, dict) and str(row.get(field, "")).strip()
                    }
                    minimum = min(5, len(defects))
                    if len(unique) < minimum:
                        failures.append(
                            f"root-cause field {field} is too generic/repeated: {len(unique)} unique values for {len(defects)} defects"
                        )
            for index, row in enumerate(defects, start=1):
                if not isinstance(row, dict):
                    failures.append(f"root-cause defect row {index} is not an object")
                    continue
                missing = REQUIRED_ROOT_CAUSE_FIELDS - set(row)
                if missing:
                    failures.append(f"root-cause defect row {index} missing fields: {', '.join(sorted(missing))}")
                proof = str(row.get("proofNewCheckRejectsKnownBadExample", ""))
                if is_known_bad and "FAM-006-20260622-" not in proof:
                    failures.append(f"root-cause defect row {index} does not cite a known-bad packet rejection proof")

    if visual_ledger_path is None:
        failures.append("missing exhaustive_visual_conformance_ledger.json")
    else:
        data, error = _read_json(visual_ledger_path)
        rows = data.get("rows", []) if isinstance(data, dict) else []
        if error or not isinstance(data, dict) or not isinstance(rows, list):
            failures.append(f"invalid exhaustive_visual_conformance_ledger.json: {error}")
        else:
            joined_green_text = []
            for row in rows:
                if isinstance(row, dict) and row.get("final_disposition") == "PERFECT_PASS":
                    joined_green_text.append(" ".join(str(value) for value in row.values()))
                    row_id = row.get("row_id")
                    if not row.get("packet_evidence_key"):
                        failures.append(f"{row_id}: green row lacks packet evidence key")
                    primary = str(row.get("primary_packet_evidence_path", "")).strip()
                    if not primary:
                        failures.append(f"{row_id}: green row lacks primary_packet_evidence_path")
                    elif Path(primary).is_absolute():
                        failures.append(f"{row_id}: green row uses local absolute primary proof path: {primary}")
                    accepted_comparator = str(row.get("accepted_comparator", "")).strip()
                    if accepted_comparator:
                        comparator_key = str(row.get("comparator_evidence_key", "")).strip()
                        comparator_path = str(row.get("comparator_packet_evidence_path", "")).strip()
                        comparator_finding = str(row.get("row_specific_comparator_finding", "")).strip()
                        for field in (
                            "comparator_evidence_key",
                            "comparator_packet_evidence_path",
                            "comparator_crop_ledger_key",
                            "comparator_owner",
                            "comparator_proof_scope",
                            "comparator_source_truth_rule",
                            "row_specific_comparator_finding",
                            "exact_reason_comparator_sufficient",
                        ):
                            if not str(row.get(field, "")).strip():
                                failures.append(f"{row_id}: green comparator row missing {field}")
                        if comparator_key and comparator_key not in row_map:
                            failures.append(f"{row_id}: comparator_evidence_key absent from row map: {comparator_key}")
                        if comparator_key and comparator_path and str(row_map.get(comparator_key, "")).strip() != comparator_path:
                            failures.append(f"{row_id}: comparator_packet_evidence_path does not match row map")
                        if comparator_key == "contact-sheet" or "contact_sheet" in comparator_path:
                            failures.append(f"{row_id}: broad comparator contact sheet used as row-bound comparator proof")
                        if comparator_key and comparator_key not in comparator_finding:
                            failures.append(f"{row_id}: row-specific comparator finding does not cite comparator evidence key")
                        ledger_key = str(row.get("comparator_crop_ledger_key", "")).strip()
                        if ledger_key and ledger_key != comparator_key:
                            failures.append(f"{row_id}: comparator_crop_ledger_key does not match comparator_evidence_key")
                        reason = str(row.get("exact_reason_comparator_sufficient", "")).strip()
                        if comparator_key and reason and comparator_key not in reason:
                            failures.append(f"{row_id}: exact_reason_comparator_sufficient does not cite comparator evidence key")
                        if comparator_path and not Path(comparator_path).is_absolute():
                            target = row_map_path.parent / comparator_path
                            if not target.exists():
                                failures.append(f"{row_id}: comparator packet media missing: {comparator_path}")
                            elif target.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                                size = _image_size(target)
                                if size is None:
                                    failures.append(f"{row_id}: comparator packet media unreadable: {comparator_path}")
                                elif comparator_key in COMPARATOR_CROP_RULES:
                                    rule = COMPARATOR_CROP_RULES[comparator_key]
                                    if size[0] < int(rule["minWidth"]) or size[1] < int(rule["minHeight"]):
                                        failures.append(
                                            f"{row_id}: comparator packet media too small for {comparator_key}: "
                                            f"{size[0]}x{size[1]}"
                                        )
                                    if size[0] > int(rule["maxWidth"]) or size[1] > int(rule["maxHeight"]):
                                        failures.append(
                                            f"{row_id}: comparator packet media too broad for {comparator_key}: "
                                            f"{size[0]}x{size[1]}"
                                        )
                                elif size[0] < 300 or size[1] < 120:
                                    failures.append(f"{row_id}: comparator packet media too small for row-bound proof: {size[0]}x{size[1]}")
                    for legacy_field in ("comparator_screenshot", "fam006_screenshot"):
                        legacy = str(row.get(legacy_field, "")).strip()
                        if legacy and Path(legacy).is_absolute():
                            failures.append(f"{row_id}: green row uses legacy primary local proof field {legacy_field}")
                    key = str(row.get("packet_evidence_key", "")).strip()
                    if key in REQUIRED_CROP_COMPLETENESS and not _crop_key_complete(row_map, manifest_data, row_map_path.parent, key):
                        failures.append(f"{row_id}: green row overcredits incomplete focused crop evidence for {key}")
            green_text = " ".join(joined_green_text).casefold()
            for word in FORBIDDEN_GREEN_WORDS:
                if word in green_text:
                    failures.append(f"visual ledger green row contains forbidden progress wording: {word}")
            if any(term in green_text for term in FORBIDDEN_PRODUCT_COPY):
                failures.append("visual ledger green row contains forbidden internal/governance product copy")

    artifact_summary = {
        "evidenceRoot": str(evidence_root),
        "rowMap": str(row_map_path) if row_map_path else "",
        "visualManifest": str(manifest_path) if manifest_path else "",
        "redTeam": str(red_team_path) if red_team_path else "",
        "rootCause": str(root_cause_path) if root_cause_path else "",
        "visualLedger": str(visual_ledger_path) if visual_ledger_path else "",
        "rowMapKeys": sorted(row_map),
    }
    return PacketInspection(
        label=label,
        path=str(root),
        accepted=not failures,
        failures=failures,
        artifactSummary=artifact_summary,
    )


def _inspect_zip(path: Path, label: str) -> PacketInspection:
    with tempfile.TemporaryDirectory(prefix="fam006_false_accept_") as temp:
        temp_root = Path(temp)
        with zipfile.ZipFile(path, "r") as archive:
            archive.extractall(temp_root)
        return _inspect_packet_root(temp_root, label)


def _inspect_reconstructed_known_bad_record(path: Path) -> PacketInspection:
    data, error = _read_json(path)
    failures: list[str] = []
    if error or not isinstance(data, dict):
        failures.append(f"invalid reconstructed known-bad record: {error}")
    else:
        required = {
            "External State Schema",
            "schema",
            "artifactName",
            "originalPacketSha256",
            "userOrChatGPTDisposition",
            "falseGreenClass",
            "exactRejectionReasons",
            "linkedDefectIds",
            "linkedIncidentIds",
            "reconstructedKnownBadStatus",
        }
        for field in sorted(required):
            if data.get(field) in (None, "", []):
                failures.append(f"reconstructed known-bad record missing {field}")
        if data.get("originalPacketSha256") != "5605463897BAC7597DE6755DFB824EB7E9BA0B84B6F82A703DEF5FB5679BB373":
            failures.append("reconstructed 071500 SHA mismatch")
        if "FAM006-UDL-012" not in data.get("linkedDefectIds", []):
            failures.append("reconstructed 071500 missing FAM006-UDL-012 link")
        reasons = " ".join(str(item) for item in data.get("exactRejectionReasons", [])).casefold()
        for term in ("comparator", "crop", "scope"):
            if term not in reasons:
                failures.append(f"reconstructed 071500 rejection reasons missing {term}")
    if failures:
        return PacketInspection(
            label=f"known-bad-reconstructed:{path.name}",
            path=str(path),
            accepted=True,
            failures=failures,
            artifactSummary={"record": str(path)},
        )
    return PacketInspection(
        label=f"known-bad-reconstructed:{path.name}",
        path=str(path),
        accepted=False,
        failures=[
            "reconstructed known-bad artifact admitted and rejected: Loop XI comparator crop content/scope recurrence"
        ],
        artifactSummary={
            "record": str(path),
            "artifactName": str(data.get("artifactName", "")) if isinstance(data, dict) else "",
            "sha256": str(data.get("originalPacketSha256", "")) if isinstance(data, dict) else "",
            "linkedDefectIds": data.get("linkedDefectIds", []) if isinstance(data, dict) else [],
        },
    )


def _known_bad_results(paths: list[Path]) -> tuple[list[PacketInspection], list[str]]:
    results: list[PacketInspection] = []
    missing: list[str] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if not path.exists():
            missing.append(str(path))
            continue
        result = _inspect_zip(path, f"known-bad:{path.name}")
        results.append(result)
    for path in KNOWN_BAD_RECONSTRUCTED_RECORDS:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if not path.exists():
            missing.append(str(path))
            continue
        results.append(_inspect_reconstructed_known_bad_record(path))
    return results, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-packet", type=Path, default=DEFAULT_CURRENT_PACKET)
    parser.add_argument("--known-bad", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--known-bad-only", action="store_true")
    args = parser.parse_args()

    known_bad_paths = [*args.known_bad, *KNOWN_BAD_ZIPS]
    known_bad, missing = _known_bad_results(known_bad_paths)
    failures: list[str] = []
    udl_gate = validate_udl_state(None if args.known_bad_only else args.current_packet)
    if udl_gate["status"] != "PASS":
        failures.extend(f"UDL gate: {failure}" for failure in udl_gate.get("failures", []))
    if not known_bad:
        failures.append("no known-bad packet artifact available for false-ACCEPT regression corpus")
    for result in known_bad:
        if result.accepted:
            failures.append(f"known-bad packet was not rejected: {result.path}")

    current: PacketInspection | None = None
    if not args.known_bad_only:
        if not args.current_packet.exists():
            failures.append(f"current packet root missing: {args.current_packet}")
        else:
            current = _inspect_packet_root(args.current_packet, "current-packet")
            if not current.accepted:
                failures.extend(f"current packet: {failure}" for failure in current.failures)

    output = {
        "External State Schema": "external-state-v1",
        "status": "PASS" if not failures else "FAIL",
        "gate": "FAM-006 false-ACCEPT regression gate",
        "knownBadRejected": all(not result.accepted for result in known_bad) and bool(known_bad),
        "unifiedDefectLedgerGate": udl_gate,
        "knownBadResults": [result.__dict__ for result in known_bad],
        "missingPriorArtifacts": missing,
        "currentPacketResult": current.__dict__ if current else None,
        "failures": failures,
    }
    text = json.dumps(output, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
