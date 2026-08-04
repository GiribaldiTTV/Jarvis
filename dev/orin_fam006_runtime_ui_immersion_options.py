"""FAM-006 dual Recording candidate / Log Viewer rename packet.

This helper is intentionally branch-local. It produces reviewable rendered
candidate-selection evidence for Recording Studio A/C and the shared Log Viewer
direction without choosing the final Recording winner or claiming H1, Live
Validation, UTS, or PR readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import textwrap
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from nexus_paths import EXTERNAL_STATE_ROOT, USER_HUB_ROOT, WORKTREES_ROOT
from orin_fam006_unified_defect_ledger import write_packet_artifacts


WORKTREE = WORKTREES_ROOT / "FAM-006"
USER_ROOT = USER_HUB_ROOT
PACKET_ROOT = USER_ROOT / "FAM-006"
EXTERNAL_BRANCH_ROOT = EXTERNAL_STATE_ROOT / "branches" / "feature_fam_006_dashboard_recording_start_stop_local_file"
SCREENSHOT_ROOT = (
    Path("C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI")
    / "fam_006_runtime_ui_immersion_options"
)
PRIMARY_REVIEW = "DUAL_RECORDING_CANDIDATE_LOG_VIEWER_RENAME_REVIEW.md"
PACKET_STATUS = "fam006-dual-recording-candidate-log-viewer-rename"
BRANCH = "feature/fam-006-dashboard-recording-start-stop-local-file"

SOURCE_CONTEXT = {
    "Docs_Main.md": WORKTREE / "Docs/Main.md",
    "Docs_nexus_startup_contract.md": WORKTREE / "Docs/nexus_startup_contract.md",
    "Docs_phase_governance.md": WORKTREE / "Docs/phase_governance.md",
    "Docs_branch_plans_README.md": WORKTREE / "Docs/branch_plans/README.md",
    "Docs_nexus_vision.md": WORKTREE / "Docs/nexus_vision.md",
    "FAM-002_desktop_interface.md": WORKTREE / "Docs/family_visions/FAM-002_desktop_interface.md",
    "FAM-006_monitoring_and_hud.md": WORKTREE / "Docs/family_visions/FAM-006_monitoring_and_hud.md",
    "FAM-006_recording.md": WORKTREE / "Docs/family_feature_visions/FAM-006_recording.md",
    "ui_reference_catalog_index.md": WORKTREE / "Docs/ui_reference_catalog/index.md",
    "UIREF-001_top_level_window_frame.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-001_top_level_window_frame.md",
    "UIREF-002_window_control_cluster.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-002_window_control_cluster.md",
    "UIREF-003_control_state_and_selector_grammar.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-003_control_state_and_selector_grammar.md",
    "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
    "UIREF-005_design_token_and_shared_rule_baseline.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-005_design_token_and_shared_rule_baseline.md",
    "UIREF-006_negative_example_and_enforcement_contract.md": WORKTREE / "Docs/ui_reference_catalog/UIREF-006_negative_example_and_enforcement_contract.md",
    "Docs_user_test_summary_guidance.md": WORKTREE / "Docs/user_test_summary_guidance.md",
    "Docs_validation_helper_registry.md": WORKTREE / "Docs/validation_helper_registry.md",
    "Docs_incident_patterns.md": WORKTREE / "Docs/incident_patterns.md",
    "Docs_external_operational_state_store_reform_plan.md": WORKTREE
    / "Docs/external_operational_state_store_reform_plan.md",
    "feature_fam_006_dashboard_recording_start_stop_local_file.md": WORKTREE
    / "Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md",
    "external_branch_plan.md": EXTERNAL_BRANCH_ROOT / "branch_plan.md",
}

CODE_SOURCES = {
    "ai_control_center_html": WORKTREE / "nexus_visual/ai_control_center.html",
    "monitoring_hud_css": WORKTREE / "nexus_visual/monitoring_hud.css",
    "studio_html": WORKTREE / "nexus_visual/monitoring_hud_studio.html",
    "studio_js": WORKTREE / "nexus_visual/monitoring_hud_studio.js",
    "studio_primitives_css": WORKTREE / "nexus_visual/nexus_window_primitives.css",
    "desktop_renderer": WORKTREE / "desktop/desktop_renderer.py",
}

REFERENCE_MEDIA = [
    Path("C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/AI Control Center- Accepted.png"),
    Path(
        "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/"
        "fam_006_pre_live_visual_conformance/20260624_212956_feature_studio_visual_fail_repair/"
        "focused_comparator_crops/ai_control_center_window_control_cluster.png"
    ),
    Path(
        "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/"
        "fam_006_pre_live_visual_conformance/20260624_212956_feature_studio_visual_fail_repair/"
        "focused_comparator_crops/ai_control_center_panel_rhythm.png"
    ),
    Path(
        "C:/Users/anden/OneDrive/Pictures/Screenshots/Nexus Desktop AI/"
        "fam_006_pre_live_visual_conformance/20260624_212956_feature_studio_visual_fail_repair/"
        "focused_comparator_crops/ai_control_center_button_grammar.png"
    ),
]

REQUIRED_MEDIA = {
    "reference_board.png",
    "code_grammar_comparison_board.png",
    "recording_candidate_a_focused.png",
    "recording_candidate_c_focused.png",
    "log_viewer_log_a_focused.png",
    "recording_candidates_board.png",
    "log_viewer_candidate_board.png",
    "candidate_selection_comparison_board.png",
    "full_desktop_context_options.png",
    "annotated_spacing_callouts.png",
    "rename_to_log_viewer_proof_board.png",
}

REQUIRED_REVIEW_AIDS = {
    "Review Aids/Code Grammar Audit/code_level_visual_grammar_audit.json",
    "Review Aids/Code Grammar Audit/code_level_visual_grammar_audit.md",
    "Review Aids/USER Defect Design Ledger/user_defect_design_ledger.json",
    "Review Aids/Recording Studio Options/recording_studio_options.json",
    "Review Aids/Recording Candidate Deltas/recording_candidate_deltas.md",
    "Review Aids/Log Viewer Candidate/log_viewer_candidate.json",
    "Review Aids/Resize Behavior/resize_behavior_decision.json",
    "Review Aids/Convergence/branch_local_comparator_convergence_note.md",
    "Review Aids/Helper Validator Hardening/helper_validator_hardening_status.json",
    "Review Aids/UDL False Green/udl_false_green_status.json",
    "Review Aids/Unified Defect Ledger/unified_defect_ledger.json",
    "Review Aids/Unified Defect Ledger/UNIFIED_DEFECT_LEDGER.md",
    "Review Aids/Unified Defect Ledger/false_green_incident_ledger.json",
    "Review Aids/Unified Defect Ledger/FALSE_GREEN_INCIDENT_LEDGER.md",
    "Review Aids/Unified Defect Ledger/unified_defect_ledger_gate.json",
    "Review Aids/Validation Outputs/packet_self_validation.json",
}


@dataclass(frozen=True)
class OptionSpec:
    option_id: str
    title: str
    subtitle: str
    surface: str
    mode: str
    width: int
    height: int
    rows: tuple[tuple[str, str], ...]
    buttons: tuple[str, ...]
    recommendation: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=WORKTREE, text=True, stderr=subprocess.STDOUT).strip()


def _identity() -> dict[str, Any]:
    upstream = _run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    status = _run_git("status", "--short")
    return {
        "worktreePath": str(WORKTREE),
        "gitRoot": _run_git("rev-parse", "--show-toplevel"),
        "branch": _run_git("branch", "--show-current"),
        "upstream": upstream,
        "head": _run_git("rev-parse", "HEAD"),
        "originMain": _run_git("rev-parse", "origin/main"),
        "mergeBase": _run_git("merge-base", "HEAD", "origin/main"),
        "aheadBehindOriginMain": _run_git("rev-list", "--left-right", "--count", "origin/main...HEAD"),
        "aheadBehindUpstream": _run_git("rev-list", "--left-right", "--count", f"{upstream}...HEAD"),
        "cleanliness": "clean" if not status else status,
    }


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copy2(source, target)
    else:
        target.write_text(f"MISSING SOURCE: {source}\n", encoding="utf-8")


def _extract_block(text: str, selector_fragment: str) -> str:
    index = text.find(selector_fragment)
    if index == -1:
        return ""
    start = text.find("{", index)
    if start == -1:
        return ""
    depth = 0
    for pos in range(start, len(text)):
        char = text[pos]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : pos]
    return ""


def _property(block: str, name: str) -> str:
    match = re.search(rf"{re.escape(name)}\s*:\s*([^;]+);", block)
    return match.group(1).strip() if match else "missing"


def _code_grammar_audit() -> dict[str, Any]:
    ai = _read(CODE_SOURCES["ai_control_center_html"])
    base = _read(CODE_SOURCES["monitoring_hud_css"])
    studio = _read(CODE_SOURCES["studio_primitives_css"])
    studio_html = _read(CODE_SOURCES["studio_html"])
    rows = []
    comparisons = [
        (
            "title-size",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__title',
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__title',
            "font-size",
            "Adapt by class: child title must be smaller than main window but still prominent.",
        ),
        (
            "subtitle-visibility",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__subtitle',
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__subtitle',
            "display",
            "Repair in options: child subtitle/description must be visible under title.",
        ),
        (
            "content-top-gutter",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__control-hub',
            _read(CODE_SOURCES["studio_html"]),
            'data-product-surface="fam006-feature-studio"] .monitoring-hud__control-hub',
            "margin-top",
            "Repair in options: first content row needs a visible top gutter.",
        ),
        (
            "state-row-padding",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__state-row',
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__studio-truth-row',
            "padding",
            "Copy the compact row rhythm, adapted only for child footprint.",
        ),
        (
            "state-row-label-size",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__state-row span',
            base,
            ".monitoring-hud__state-row span",
            "font-size",
            "Use the compact AI row label size when possible.",
        ),
        (
            "state-row-value-size",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__state-row strong',
            base,
            ".monitoring-hud__state-row strong",
            "font-size",
            "Use AI compact value sizing for dense controller state.",
        ),
        (
            "button-height",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__hub-action--content-fit',
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__hub-action--content-fit',
            "height",
            "Match content-fit pill behavior, not oversized wells.",
        ),
        (
            "button-horizontal-buffer",
            base,
            ".monitoring-hud__hub-action--content-fit",
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__hub-action--content-fit',
            "padding",
            "Use AI/HUD content-fit button padding: equal 14px left and right label buffer.",
        ),
        (
            "button-min-height",
            base,
            ".monitoring-hud__hub-action--content-fit",
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__hub-action--content-fit',
            "min-height",
            "Use the same vertical hitbox rhythm as AI Control Center content-fit buttons.",
        ),
        (
            "button-label-size",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__hub-action--content-fit > .monitoring-hud__button-label',
            studio,
            'data-feature-studio-primitive="fam006-unique-child-studio-shell-v5"] .monitoring-hud__hub-action--content-fit > .monitoring-hud__button-label',
            "font-size",
            "Use exact compact label size unless USER selects a deliberate exception.",
        ),
        (
            "row-label-color",
            base,
            ".monitoring-hud__state-row span",
            base,
            ".monitoring-hud__state-row span",
            "color",
            "Use the same row label color family and opacity as AI/HUD row grammar.",
        ),
        (
            "row-value-color",
            base,
            ".monitoring-hud__state-row strong",
            base,
            ".monitoring-hud__state-row strong",
            "color",
            "Use the same row value mint color family and opacity as AI/HUD row grammar.",
        ),
        (
            "window-control-button-size",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__window-control-button',
            studio,
            'data-window-control-primitive="nexus-uiref-002-compact-cluster-v1"] .monitoring-hud__window-control-button',
            "width",
            "Copy exact primitive.",
        ),
        (
            "window-control-cluster-top",
            ai,
            'data-product-surface="nexus-ai-control-center"] .monitoring-hud__window-controls',
            studio,
            'data-window-control-primitive="nexus-uiref-002-compact-cluster-v1"] .monitoring-hud__window-controls',
            "top",
            "Copy exact primitive except local x-offset for narrow Recording Studio.",
        ),
    ]
    for key, ai_text, ai_selector, studio_text, studio_selector, prop, recommendation in comparisons:
        ai_value = _property(_extract_block(ai_text, ai_selector), prop)
        studio_value = _property(_extract_block(studio_text, studio_selector), prop)
        mismatch = ai_value != studio_value
        if key in {"title-size", "window-control-cluster-top"}:
            status = "ADAPT_WITH_DISPOSITION" if mismatch else "MATCH"
        elif key == "window-control-button-size":
            status = "MATCH" if ai_value == studio_value else "COPY_EXACT_REQUIRED"
        else:
            status = "MISMATCH_REPAIR_OPTION_REQUIRED" if mismatch else "MATCH"
        rows.append(
            {
                "key": key,
                "property": prop,
                "aiControlCenterValue": ai_value,
                "recordingStudioCurrentValue": studio_value,
                "logViewerCurrentValue": studio_value,
                "mismatchStatus": status,
                "repairRecommendation": recommendation,
                "referenceSource": ai_selector,
                "studioSource": studio_selector,
            }
        )
    return {
        "schema": "fam006-runtime-ui-immersion-code-grammar-audit-v1",
        "status": "REPAIR_OPTIONS_REQUIRED",
        "aiControlCenterSource": "nexus_visual/ai_control_center.html inline style plus monitoring_hud.css",
        "hudDashboardSource": "nexus_visual/monitoring_hud.css",
        "studioCurrentSource": "nexus_visual/nexus_window_primitives.css and monitoring_hud_studio.html",
        "branchLocalComparatorOnly": True,
        "runtimeVisibleRenameApplied": True,
        "finalRecordingWinnerImplemented": False,
        "notGlobalLaw": True,
        "studioHtmlContractMarkers": {
            "titleCardState": "data-title-card-state=\"absent\"" in studio_html,
            "sharedPrimitiveConsumer": "data-shared-primitive-consumer=\"nexus-window-primitives-v1\"" in studio_html,
            "resizeTaxonomy": "no-resize-recording-edge-resize-log-viewer" in studio_html,
        },
        "childWindowTitleReference": {
            "referenceSurfaces": ["Overlay Profile Settings", "Manage Monitors"],
            "source": "nexus_visual/monitoring_hud.html .monitoring-hud__child-window-header",
            "currentUserSteering": "Unique studio candidates must put the actual surface title on top, with supporting description beneath it.",
            "disposition": "Title-first hierarchy is recorded as the current FAM-006 review target; attached child windows remain useful references for compact title treatment and close/control placement.",
        },
        "rows": rows,
    }


def _defect_ledger() -> dict[str, Any]:
    seeds = [
        ("FAM006-RUIO-001", "Child windows do not feel like same product family", "Verified by USER report and current packet repair posture."),
        ("FAM006-RUIO-002", "Surface color/shimmer/glow diverges from comparator", "Inferred from current primitive being separate and USER full-desktop review."),
        ("FAM006-RUIO-003", "Approximation used instead of actual code/token comparison", "Verified by repeated false-green class; this packet performs selector audit."),
        ("FAM006-RUIO-004", "Child title hierarchy inconsistent", "Verified: current primitive hid subtitle; this packet restores title-first hierarchy with description beneath per USER steering."),
        ("FAM006-RUIO-005", "Rows begin too close to chrome/title", "Verified: current studio control hub margin-top is 3px vs AI 12px."),
        ("FAM006-RUIO-006", "Row spacing and bottom dead-space need redesign", "Verified by USER report and branch-plan known-bad receipts."),
        ("FAM006-RUIO-007", "Start/Pause/Stop is admitted for Recording candidates A/C, not final winner authority", "Verified by prompt boundary."),
        ("FAM006-RUIO-008", "Log Viewer rename must stay doorway shell without fake rows/paths", "Verified by USER direction and prompt boundary."),
        ("FAM006-RUIO-009", "Resize behavior needs class decision", "Verified by current data resize taxonomy and USER report."),
        ("FAM006-RUIO-010", "Full-desktop proof must catch focused-crop false green", "Verified by UDL/false-green receipts."),
    ]
    return {
        "schema": "fam006-runtime-ui-immersion-user-defect-design-ledger-v1",
        "status": "REPAIR_OPTIONS_REQUIRED",
        "runtimeFixesWithheld": True,
        "rows": [
            {
                "defectId": defect_id,
                "title": title,
                "classification": "USER_REPORTED_DESIGN_DEFECT",
                "verification": verification,
                "futureRepairLaneCandidate": "bounded FAM-006 runtime implementation-match repair after USER selects option",
                "currentPacketDisposition": "design option / source-truth grounded review evidence",
            }
            for defect_id, title, verification in seeds
        ],
    }


def _recording_options() -> list[OptionSpec]:
    return [
        OptionSpec(
            "REC-A",
            "Segmented dual-row controller",
            "ACTIVE OVERLAY RECORDING",
            "Recording Studio",
            "segmented",
            438,
            168,
            (("TARGET", "Default Overlay Profile / 2 active monitors"), ("STATE", "Ready for local recording")),
            ("START", "PAUSE", "STOP", "OPEN LOG VIEWER"),
            "Best when USER wants explicit transport controls inside the smallest readable footprint.",
        ),
        OptionSpec(
            "REC-C",
            "Split transport plus route",
            "ACTIVE OVERLAY RECORDING",
            "Recording Studio",
            "split",
            462,
            176,
            (("TARGET", "Default Overlay Profile"), ("STATE", "Ready / 2 active monitors")),
            ("START", "PAUSE", "STOP", "OPEN LOG VIEWER"),
            "Best when USER wants recording transport grouped separately from the Log Viewer route without growing height too much.",
        ),
    ]


def _log_options() -> list[OptionSpec]:
    return [
        OptionSpec(
            "LOG-A",
            "Ultra compact doorway",
            "NATIVE AND EXPORTED LOG ACCESS",
            "Log Viewer",
            "doorway",
            430,
            138,
            (("VIEWER", "Deferred"),),
            ("OPEN NATIVE LOGS", "OPEN EXPORTED LOGS"),
            "Best if current branch only needs a doorway shell with minimal visual weight.",
        ),
    ]


def _font(name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = {
        "regular": ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/bahnschrift.ttf"],
        "bold": ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/bahnschrift.ttf"],
        "semi": ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/bahnschrift.ttf"],
    }.get(name, ["C:/Windows/Fonts/segoeui.ttf"])
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_KICKER = _font("semi", 10)
FONT_TITLE = _font("bold", 17)
FONT_SUBTITLE = _font("semi", 11)
FONT_LABEL = _font("semi", 10)
FONT_VALUE = _font("bold", 11)
FONT_BUTTON = _font("bold", 11)
FONT_BODY = _font("regular", 11)
BUTTON_PAD_X = 14
BUTTON_H = 31


def _rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int, int], outline: tuple[int, int, int, int] | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _text_center(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, font: ImageFont.ImageFont, fill: tuple[int, int, int, int]) -> None:
    bounds = draw.textbbox((0, 0), text, font=font)
    x = box[0] + (box[2] - box[0] - (bounds[2] - bounds[0])) / 2
    y = box[1] + (box[3] - box[1] - (bounds[3] - bounds[1])) / 2 - 1
    draw.text((x, y), text, font=font, fill=fill)


def _draw_grid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(0, width, 20):
        draw.line((x, 0, x, height), fill=(13, 54, 66, 96))
    for y in range(0, height, 20):
        draw.line((0, y, width, y), fill=(12, 47, 58, 90))


def _draw_control_pill(draw: ImageDraw.ImageDraw, x: int, y: int, controls: tuple[str, ...]) -> None:
    pill_w = 4 + len(controls) * 28
    _rounded(draw, (x, y, x + pill_w, y + 30), 15, (7, 36, 53, 190), (122, 232, 255, 112))
    for index, control in enumerate(controls):
        bx = x + 3 + index * 28
        _rounded(draw, (bx, y + 3, bx + 26, y + 27), 13, (5, 22, 36, 158), (122, 232, 255, 62))
        cx = bx + 13
        cy = y + 15
        if control == "min":
            draw.line((cx - 5, cy, cx + 5, cy), fill=(235, 252, 255, 235), width=2)
        elif control == "max":
            draw.rectangle((cx - 5, cy - 5, cx + 5, cy + 5), outline=(235, 252, 255, 235), width=2)
        else:
            draw.line((cx - 5, cy - 5, cx + 5, cy + 5), fill=(235, 252, 255, 235), width=2)
            draw.line((cx + 5, cy - 5, cx - 5, cy + 5), fill=(235, 252, 255, 235), width=2)


def _draw_row(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, label: str, value: str) -> int:
    draw.line((x, y, x + w, y), fill=(116, 240, 255, 100), width=1)
    draw.line((x, y + 1, x + w, y + 1), fill=(0, 0, 0, 95), width=1)
    draw.rectangle((x, y + 6, x + 2, y + 20), fill=(117, 228, 255, 92))
    draw.text((x + 9, y + 5), label.upper(), font=FONT_LABEL, fill=(145, 202, 218, 220))
    draw.text((x + 126, y + 5), value, font=FONT_VALUE, fill=(157, 246, 218, 235))
    return y + 28


def _draw_button(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, primary: bool = False) -> None:
    fill = (8, 40, 58, 224) if not primary else (8, 55, 68, 236)
    outline = (117, 228, 255, 92) if not primary else (116, 255, 223, 122)
    glow = (80, 231, 232, 28) if primary else (84, 218, 255, 18)
    _rounded(draw, (box[0] + 1, box[1] + 2, box[2] + 1, box[3] + 3), 16, glow)
    _rounded(draw, box, 16, fill, outline)
    _text_center(draw, box, label.upper(), FONT_BUTTON, (235, 252, 255, 238))


def _button_width(label: str, min_width: int = 0) -> int:
    bbox = FONT_BUTTON.getbbox(label.upper())
    return max(min_width, (bbox[2] - bbox[0]) + BUTTON_PAD_X * 2)


def _render_window(spec: OptionSpec, target: Path, annotate: bool = False) -> None:
    img = Image.new("RGBA", (spec.width, spec.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    _rounded(draw, (0, 0, spec.width - 1, spec.height - 1), 24, (4, 17, 32, 246), (125, 235, 255, 86))
    _draw_grid(draw, spec.width, spec.height)
    draw.rectangle((1, 1, spec.width - 2, spec.height - 2), outline=(214, 248, 255, 20), width=1)
    controls = ("min", "close")
    _draw_control_pill(draw, spec.width - 16 - (4 + len(controls) * 28), 14, controls)
    draw.text((18, 17), spec.surface.upper(), font=FONT_TITLE, fill=(234, 253, 255, 242))
    draw.text((18, 39), spec.subtitle.upper(), font=FONT_KICKER, fill=(139, 233, 255, 222))
    content_y = 61
    if annotate:
        draw.line((18, 56, spec.width - 18, 56), fill=(255, 214, 113, 155), width=1)
        draw.text((22, 47), "title-to-row gutter", font=FONT_BODY, fill=(255, 214, 113, 230))
    row_x = 18
    row_w = spec.width - 36
    for label, value in spec.rows:
        content_y = _draw_row(draw, row_x, content_y, row_w, label, value)
    action_y = content_y + (4 if spec.mode in {"segmented", "doorway", "wide"} else 2)
    if spec.surface == "Recording Studio" and spec.mode == "segmented":
        x = 18
        for label in spec.buttons[:3]:
            bw = _button_width(label)
            _draw_button(draw, (x, action_y, x + bw, action_y + BUTTON_H), label, label == "START")
            x += bw + 8
        bw = _button_width(spec.buttons[3])
        _draw_button(draw, (x + 4, action_y, x + 4 + bw, action_y + BUTTON_H), spec.buttons[3], False)
    elif spec.surface == "Recording Studio" and spec.mode == "transport":
        x = 18
        for label in spec.buttons:
            button_w = _button_width(label)
            _draw_button(draw, (x, action_y, x + button_w, action_y + BUTTON_H), label, label == "START")
            x += button_w + 8
    elif spec.surface == "Recording Studio":
        first_w = _button_width("START / PAUSE / STOP")
        second_w = _button_width("OPEN LOG VIEWER")
        _draw_button(draw, (18, action_y, 18 + first_w, action_y + BUTTON_H), "START / PAUSE / STOP", True)
        _draw_button(draw, (30 + first_w, action_y, 30 + first_w + second_w, action_y + BUTTON_H), "OPEN LOG VIEWER", False)
    else:
        gap = 10
        first_w = _button_width(spec.buttons[0])
        second_w = _button_width(spec.buttons[1])
        total_w = first_w + gap + second_w
        x = max(18, (spec.width - total_w) // 2)
        _draw_button(draw, (x, action_y, x + first_w, action_y + BUTTON_H), spec.buttons[0], False)
        _draw_button(draw, (x + first_w + gap, action_y, x + total_w, action_y + BUTTON_H), spec.buttons[1], False)
    if annotate:
        bottom_gap = spec.height - (action_y + BUTTON_H) - 14
        draw.text((spec.width - 150, spec.height - 22), f"bottom gutter {bottom_gap}px", font=FONT_BODY, fill=(255, 214, 113, 230))
    target.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(target)


def _make_board(media_dir: Path, specs: list[OptionSpec], output: Path, title: str) -> None:
    margin = 24
    label_h = 34
    width = max(spec.width for spec in specs) + margin * 2
    height = margin + sum(spec.height + label_h + 18 for spec in specs)
    img = Image.new("RGB", (width, height), (1, 5, 11))
    draw = ImageDraw.Draw(img)
    draw.text((margin, 10), title.upper(), font=_font("bold", 18), fill=(234, 253, 255))
    y = 46
    for spec in specs:
        path = media_dir / f"{spec.option_id.lower().replace('-', '_')}.png"
        if not path.exists():
            _render_window(spec, path)
        draw.text((margin, y), f"{spec.option_id} - {spec.title}: {spec.recommendation}", font=FONT_BODY, fill=(174, 226, 240))
        option_img = Image.open(path).convert("RGB")
        img.paste(option_img, (margin, y + label_h))
        y += spec.height + label_h + 18
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)


def _render_media(media_dir: Path, audit: dict[str, Any]) -> dict[str, str]:
    media_dir.mkdir(parents=True, exist_ok=True)
    recording = _recording_options()
    log_options = _log_options()
    files: dict[str, str] = {}
    names = [
        "recording_candidate_a_focused.png",
        "recording_candidate_c_focused.png",
    ]
    for spec, name in zip(recording, names):
        _render_window(spec, media_dir / name, annotate=name.endswith("candidate_c_focused.png"))
        files[name] = str(media_dir / name)
    names = [
        "log_viewer_log_a_focused.png",
    ]
    for spec, name in zip(log_options, names):
        _render_window(spec, media_dir / name, annotate=True)
        files[name] = str(media_dir / name)

    _make_board(media_dir, recording, media_dir / "recording_candidates_board.png", "Recording Studio runtime candidates")
    _make_board(media_dir, log_options, media_dir / "log_viewer_candidate_board.png", "Log Viewer LOG-A runtime candidate")
    files["recording_candidates_board.png"] = str(media_dir / "recording_candidates_board.png")
    files["log_viewer_candidate_board.png"] = str(media_dir / "log_viewer_candidate_board.png")

    ref_board = Image.new("RGB", (1160, 720), (1, 5, 11))
    draw = ImageDraw.Draw(ref_board)
    draw.text((24, 20), "BRANCH-LOCAL COMPARATOR REFERENCES", font=_font("bold", 22), fill=(234, 253, 255))
    x = 24
    y = 62
    for ref in REFERENCE_MEDIA:
        if not ref.exists():
            continue
        image = Image.open(ref).convert("RGB")
        image.thumbnail((520, 290))
        ref_board.paste(image, (x, y))
        draw.text((x, y + image.height + 8), ref.name, font=FONT_BODY, fill=(174, 226, 240))
        x += 550
        if x > 600:
            x = 24
            y += 350
    ref_board.save(media_dir / "reference_board.png")
    files["reference_board.png"] = str(media_dir / "reference_board.png")

    grammar_board = Image.new("RGB", (1280, 760), (2, 8, 16))
    draw = ImageDraw.Draw(grammar_board)
    draw.text((24, 18), "CODE-LEVEL VISUAL GRAMMAR AUDIT", font=_font("bold", 22), fill=(234, 253, 255))
    headers = ["Key", "AI/HUD value", "Studio current", "Status"]
    xs = [24, 310, 585, 860]
    for x, header in zip(xs, headers):
        draw.text((x, 62), header, font=FONT_LABEL, fill=(139, 233, 255))
    row_y = 90
    for row in audit["rows"]:
        draw.line((24, row_y - 5, 1240, row_y - 5), fill=(116, 240, 255, 75))
        values = [
            row["key"],
            row["aiControlCenterValue"],
            row["recordingStudioCurrentValue"],
            row["mismatchStatus"],
        ]
        for x, value in zip(xs, values):
            draw.text((x, row_y), str(value)[:42], font=FONT_BODY, fill=(220, 244, 250))
        row_y += 58
    grammar_board.save(media_dir / "code_grammar_comparison_board.png")
    files["code_grammar_comparison_board.png"] = str(media_dir / "code_grammar_comparison_board.png")

    side = Image.new("RGB", (1460, 880), (1, 5, 11))
    draw = ImageDraw.Draw(side)
    draw.text((28, 20), "SIDE-BY-SIDE: COMPARATOR VS OPTIONS", font=_font("bold", 22), fill=(234, 253, 255))
    ref = media_dir / "reference_board.png"
    if ref.exists():
        ref_img = Image.open(ref).convert("RGB")
        ref_img.thumbnail((620, 390))
        side.paste(ref_img, (28, 64))
    rec = Image.open(media_dir / "recording_candidates_board.png").convert("RGB")
    rec.thumbnail((380, 760))
    side.paste(rec, (680, 64))
    log = Image.open(media_dir / "log_viewer_candidate_board.png").convert("RGB")
    log.thumbnail((380, 760))
    side.paste(log, (1080, 64))
    side.save(media_dir / "candidate_selection_comparison_board.png")
    files["candidate_selection_comparison_board.png"] = str(media_dir / "candidate_selection_comparison_board.png")

    context = Image.new("RGB", (1400, 820), (0, 3, 8))
    draw = ImageDraw.Draw(context)
    _draw_grid(draw, 1400, 820)
    _rounded(draw, (610, 52, 1340, 748), 28, (4, 17, 32, 246), (125, 235, 255, 86))
    draw.text((642, 86), "NEXUS DESKTOP AI", font=FONT_KICKER, fill=(139, 233, 255))
    draw.text((642, 106), "HUD Dashboard context", font=_font("bold", 30), fill=(234, 253, 255))
    draw.text((642, 150), "Recording card doorway remains parent context; studios are standalone-capable child windows.", font=FONT_BODY, fill=(174, 226, 240))
    rec_img = Image.open(media_dir / "recording_candidate_a_focused.png").convert("RGB")
    log_img = Image.open(media_dir / "log_viewer_log_a_focused.png").convert("RGB")
    context.paste(rec_img, (42, 128))
    context.paste(log_img, (42, 340))
    draw.text((42, 80), "Full-desktop/context render, not runtime proof", font=_font("bold", 18), fill=(234, 253, 255))
    context.save(media_dir / "full_desktop_context_options.png")
    files["full_desktop_context_options.png"] = str(media_dir / "full_desktop_context_options.png")

    annotated = Image.new("RGB", (1000, 580), (1, 5, 11))
    draw = ImageDraw.Draw(annotated)
    rec_c = Image.open(media_dir / "recording_candidate_c_focused.png").convert("RGB")
    log_c = Image.open(media_dir / "log_viewer_log_a_focused.png").convert("RGB")
    annotated.paste(rec_c, (36, 72))
    annotated.paste(log_c, (36, 300))
    draw.text((36, 26), "ANNOTATED TITLE / BUTTON / ROW GUTTER CALLOUTS", font=_font("bold", 20), fill=(234, 253, 255))
    for y0, label in ((72, "Recording Studio"), (300, "Log Viewer")):
        draw.line((34, y0 + 58, 520, y0 + 58), fill=(255, 214, 113), width=2)
        draw.text((548, y0 + 49), f"{label}: title first, description below, then row gutter", font=FONT_BODY, fill=(255, 214, 113))
        draw.line((34, y0 + 126, 520, y0 + 126), fill=(126, 248, 218), width=2)
        draw.text((548, y0 + 117), "Buttons use 31px height, 11px text, 14px left/right buffer", font=FONT_BODY, fill=(126, 248, 218))
    annotated.save(media_dir / "annotated_spacing_callouts.png")
    files["annotated_spacing_callouts.png"] = str(media_dir / "annotated_spacing_callouts.png")

    rename = Image.new("RGB", (900, 360), (1, 5, 11))
    draw = ImageDraw.Draw(rename)
    draw.text((24, 24), "RENAME-TO-LOG-VIEWER PROOF", font=_font("bold", 20), fill=(234, 253, 255))
    draw.text((24, 62), "Runtime-visible destination name: LOG VIEWER", font=FONT_BODY, fill=(174, 226, 240))
    draw.text((24, 88), "Recording route action: OPEN LOG VIEWER", font=FONT_BODY, fill=(174, 226, 240))
    draw.text((24, 114), "Shared LOG-A candidate title: LOG VIEWER", font=FONT_BODY, fill=(174, 226, 240))
    draw.text((24, 140), "Historical Source Truth Context may contain prior name only as evidence.", font=FONT_BODY, fill=(255, 214, 113))
    log_img = Image.open(media_dir / "log_viewer_log_a_focused.png").convert("RGB")
    rename.paste(log_img, (24, 190))
    rename.save(media_dir / "rename_to_log_viewer_proof_board.png")
    files["rename_to_log_viewer_proof_board.png"] = str(media_dir / "rename_to_log_viewer_proof_board.png")

    return files


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(value.replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def _purge_packet() -> None:
    def clear_readonly(function: Any, path: str, _excinfo: Any) -> None:
        os.chmod(path, stat.S_IWRITE)
        function(path)

    if PACKET_ROOT.exists():
        shutil.rmtree(PACKET_ROOT, onexc=clear_readonly)
    for zip_path in USER_ROOT.glob("FAM-006-*.zip"):
        zip_path.unlink()


def _write_source_context() -> None:
    context = PACKET_ROOT / "Source Truth Context"
    for name, source in SOURCE_CONTEXT.items():
        _copy_file(source, context / name)


def _write_packet(media_root: Path, packet_time: str) -> dict[str, Any]:
    _purge_packet()
    audit = _code_grammar_audit()
    defect = _defect_ledger()
    media_files = _render_media(media_root, audit)
    _write_source_context()

    review_dir = PACKET_ROOT / "USER Review"
    aids = PACKET_ROOT / "Review Aids"
    media_dir = aids / "Rendered Media"
    media_dir.mkdir(parents=True, exist_ok=True)
    for path in media_root.glob("*.png"):
        shutil.copy2(path, media_dir / path.name)

    _write_json(aids / "Code Grammar Audit/code_level_visual_grammar_audit.json", audit)
    _write_md(
        aids / "Code Grammar Audit/code_level_visual_grammar_audit.md",
        "# Code-Level Visual Grammar Audit\n\n"
        + _markdown_table(
            ["Key", "AI Control Center / HUD value", "Studio current value", "Status", "Recommendation"],
            [
                [
                    row["key"],
                    row["aiControlCenterValue"],
                    row["recordingStudioCurrentValue"],
                    row["mismatchStatus"],
                    row["repairRecommendation"],
                ]
                for row in audit["rows"]
            ],
        ),
    )
    _write_json(aids / "USER Defect Design Ledger/user_defect_design_ledger.json", defect)
    _write_md(
        aids / "USER Defect Design Ledger/user_defect_design_ledger.md",
        "# USER Defect / Design Ledger\n\n"
        + _markdown_table(
            ["ID", "Title", "Verification", "Disposition"],
            [
                [
                    row["defectId"],
                    row["title"],
                    row["verification"],
                    row["currentPacketDisposition"],
                ]
                for row in defect["rows"]
            ],
        ),
    )

    recording_json = {
        "schema": "fam006-recording-studio-dual-candidate-selection-v1",
        "status": "REVIEW_CANDIDATES_ONLY",
        "runtimeVisibleRenameApplied": True,
        "finalRecordingWinnerImplemented": False,
        "requiredControlsExplored": ["START", "PAUSE", "STOP", "OPEN LOG VIEWER"],
        "options": [spec.__dict__ for spec in _recording_options()],
        "excludedOptions": ["REC-B"],
    }
    log_json = {
        "schema": "fam006-log-viewer-renamed-log-a-candidate-v1",
        "status": "REVIEW_CANDIDATE_ONLY",
        "runtimeVisibleRenameApplied": True,
        "finalRecordingWinnerImplemented": False,
        "currentSurfaceName": "Log Viewer",
        "priorSurfaceName": "Log Viewer Studio",
        "forbiddenPatternsExcluded": [
            "fake data rows",
            "local path display by default",
            "graph/export customization",
            "previous-log selection",
            "helper/proof commentary inside product UI",
        ],
        "options": [spec.__dict__ for spec in _log_options()],
    }
    _write_json(aids / "Recording Studio Options/recording_studio_options.json", recording_json)
    _write_md(
        aids / "Recording Studio Options/recording_studio_options.md",
        "# Recording Studio Candidates\n\n"
        + _markdown_table(
            ["Option", "Layout", "Footprint", "Controls", "Rationale"],
            [
                [
                    spec.option_id,
                    spec.title,
                    f"{spec.width}x{spec.height}",
                    ", ".join(spec.buttons),
                    spec.recommendation,
                ]
                for spec in _recording_options()
            ],
        ),
    )
    _write_md(
        aids / "Recording Candidate Deltas/recording_candidate_deltas.md",
        "# Recording Candidate A / C Deltas\n\n"
        "| Delta | REC-A | REC-C |\n"
        "| --- | --- | --- |\n"
        "| Control grouping | Three discrete START / PAUSE / STOP buttons plus separate OPEN LOG VIEWER route | One compact START / PAUSE / STOP transport pill plus separate OPEN LOG VIEWER route |\n"
        "| Space tradeoff | Clearer individual controls; tighter horizontal fit pressure | Slightly wider but cleaner separation between transport and route action |\n"
        "| USER decision | Pick if explicit button separation matters most | Pick if grouped recording transport with a cleaner route action matters most |\n",
    )
    _write_json(aids / "Log Viewer Candidate/log_viewer_candidate.json", log_json)
    _write_md(
        aids / "Log Viewer Candidate/log_viewer_candidate.md",
        "# Log Viewer Candidate\n\n"
        + _markdown_table(
            ["Option", "Layout", "Footprint", "Actions", "Rationale"],
            [
                [
                    spec.option_id,
                    spec.title,
                    f"{spec.width}x{spec.height}",
                    ", ".join(spec.buttons),
                    spec.recommendation,
                ]
                for spec in _log_options()
            ],
        ),
    )

    resize = {
        "schema": "fam006-studio-resize-decision-v1",
        "recordingStudio": {
            "recommendedCurrentScope": "fixed-size position-memory-only",
            "edgeCursorExpected": False,
            "reason": "Recording Studio is an ultra-lightweight detached recording controller; resizing is not needed for current branch purpose.",
            "proofRequiredIfImplemented": "no resize affordance, movable window, same-session placement proof, later persisted-position proof when global reset setting exists",
        },
        "logViewer": {
            "recommendedCurrentScope": "fixed-size doorway shell until full viewer/log graph scope is selected",
            "edgeCursorExpected": False,
            "reason": "Current branch Log Viewer is a folder-access doorway shell with no graph/viewer workspace; resize can be deferred until full viewer need is admitted.",
            "proofRequiredIfResizableLater": "edge-resize proof, no attached-child corner grip, before/during/after media, content reflow proof",
        },
    }
    _write_json(aids / "Resize Behavior/resize_behavior_decision.json", resize)
    _write_md(
        aids / "Resize Behavior/resize_behavior_decision.md",
        "# Resize Behavior Decision\n\n"
        "Recording Studio should remain fixed-size in current scope. Log Viewer should also remain fixed-size while it is only a deferred doorway shell. If later full viewer or graph scope is selected, Log Viewer can become edge-resizable with fresh proof.\n",
    )

    _write_md(
        aids / "Convergence/branch_local_comparator_convergence_note.md",
        "# Branch-Local Comparator / Future Convergence Note\n\n"
        "AI Control Center and HUD Dashboard are used here as the active FAM-006 branch-local comparator for current immersion and primitive alignment. This packet does not promote AI Control Center as permanent global law. FAM-007 may change AI Control Center, so later convergence should route through Governance/FAM-002/UIREF before any durable shared primitive or global rule is promoted. The durable candidate rule is: new child windows inherit current source-truth window primitives/tokens and accepted family grammar, with source-truth disposition for every variant.\n",
    )

    hardening = {
        "schema": "fam006-runtime-ui-immersion-helper-hardening-v1",
        "status": "BRANCH_LOCAL_HELPER_ADDED",
        "helper": "dev/orin_fam006_runtime_ui_immersion_options.py",
        "falseAcceptGateIntegration": "packet class recognized by dev/orin_fam006_false_accept_regression_gate.py",
        "runtimeVisibleRenameApplied": True,
        "finalRecordingWinnerImplemented": False,
        "hardWarnsOrFails": [
            "missing code-level selector/token audit",
            "missing rendered Recording Studio or Log Viewer candidates",
            "missing title/subtitle hierarchy section",
            "fake Log Viewer data rows or local paths by default",
            "missing resize behavior decision",
            "missing branch-local comparator convergence note",
        ],
    }
    _write_json(aids / "Helper Validator Hardening/helper_validator_hardening_status.json", hardening)

    udl = {
        "schema": "fam006-runtime-ui-immersion-udl-status-v1",
        "status": "NO_NEW_KNOWN_BAD_ADMITTED_BY_THIS_PACKET",
        "currentKnownBadRelevantToThisPacket": "FAM-006-20260624-170523.zip remains known-bad for implementation-match/B2 placement proof; this packet is candidate-selection review only.",
        "falseAcceptBoundary": "This packet must not be accepted as final Recording winner selection, runtime implementation match, H1, LV, UTS, PR Readiness, or global Governance proof.",
    }
    _write_json(aids / "UDL False Green/udl_false_green_status.json", udl)

    manifest = {
        "schema": "fam006-runtime-ui-immersion-packet-manifest-v1",
        "packetStatus": PACKET_STATUS,
        "generatedAt": packet_time,
        "identity": _identity(),
        "mediaFiles": sorted(path.name for path in media_dir.glob("*.png")),
        "codeSources": {key: str(path) for key, path in CODE_SOURCES.items()},
        "runtimeVisibleRenameApplied": True,
        "finalRecordingWinnerImplemented": False,
        "sourceTruthContextFiles": sorted(SOURCE_CONTEXT),
    }
    _write_json(aids / "packet_manifest.json", manifest)

    _write_json(aids / "Validation Outputs/packet_self_validation.json", {"status": "PENDING_FINAL_VALIDATION"})

    _write_md(
        PACKET_ROOT / "START_HERE.md",
        f"""# FAM-006 Dual Recording Candidate / Log Viewer Rename Packet

Packet Status: `{PACKET_STATUS}`

Start with `USER Review/{PRIMARY_REVIEW}`.

This packet is candidate-selection review evidence only. It applies the visible Log Viewer rename, but it does not choose the final Recording winner or approve the selected Recording runtime implementation, H1, Live Validation, UTS, PR Readiness, PR creation, merge, release, issue mutation, FAM-007 mutation, Governance mutation, or neutral-main mutation.
""",
    )
    primary = f"""# FAM-006 Dual Recording Candidate / Log Viewer Rename Review

Packet Status: `{PACKET_STATUS}`

## Decision Boundary

This packet compares the current Recording Studio and renamed Log Viewer surface against the current AI Control Center / HUD Dashboard code-level grammar and produces runtime-accurate candidate renders. The visible Log Viewer rename is applied; the final Recording winner remains unselected.

## Comparator Status

AI Control Center and HUD Dashboard are used as branch-local FAM-006 comparators only. They are not promoted as permanent global law by this packet.

## Code-Level Audit Result

The audit is in `Review Aids/Code Grammar Audit/code_level_visual_grammar_audit.md`. It compares title hierarchy, subtitle visibility, top gutter, state rows, buttons, and window control primitives by selector/property.

## Title / Button / Row Comparator Rules

The current review target uses title-first unique studio hierarchy: `RECORDING STUDIO` and `LOG VIEWER` sit on the top line, with a short supporting description beneath. Overlay Profile Settings and Manage Monitors remain the child-window compact-header reference, but USER steering requires these unique studio candidates to put the actual window title first.

Buttons in the rendered candidates use the AI Control Center / HUD content-fit button contract: 31px height, 11px label text, matching top/bottom buffer, and equal 14px left/right label buffer. Rows use the AI/HUD state-row color, size, font, and underglow family as the comparator.

## Recording Studio Candidates

- `REC-A`: compact segmented START / PAUSE / STOP plus OPEN LOG VIEWER.
- `REC-C`: split route action with grouped recording transport and separate Log Viewer route.

Rendered media is under `Review Aids/Rendered Media`.

## Log Viewer Candidate

- `LOG-A`: ultra-compact doorway shell.

The Log Viewer candidate keeps `VIEWER - Deferred`, bottom OPEN NATIVE LOGS / OPEN EXPORTED LOGS actions, no fake data rows, no local path display by default, no graph/export customization, no previous-log selection, and no helper/proof copy inside product UI.

## Recommended Path

Recommended review route: USER selects REC-A or REC-C for Recording Studio, accepts or revises the shared LOG-A-based Log Viewer direction, or holds/rejects the candidate direction. After USER selection, the next legal phase is a separate bounded FAM-006 runtime implementation-match repair against the selected direction, followed by renewed H1 and exact USER desktop launcher Live Validation only after implementation proof is green.

## Exact USER Decision Summary

Please choose REC-A or REC-C for Recording Studio and accept, revise, hold, or reject the shared Log Viewer direction. This does not accept implementation or advance to H1/LV/UTS.
"""
    _write_md(review_dir / PRIMARY_REVIEW, primary)
    write_packet_artifacts(PACKET_ROOT)
    return {
        "packetRoot": str(PACKET_ROOT),
        "mediaRoot": str(media_root),
        "mediaFiles": media_files,
        "manifest": manifest,
    }


def validate_packet(root: Path = PACKET_ROOT) -> list[str]:
    failures: list[str] = []
    if not root.exists():
        return [f"packet root missing: {root}"]
    if not (root / "START_HERE.md").is_file():
        failures.append("START_HERE.md missing")
    review_files = sorted((root / "USER Review").glob("*.md")) if (root / "USER Review").exists() else []
    if [path.name for path in review_files] != [PRIMARY_REVIEW]:
        failures.append("USER Review must contain exactly the primary dual Recording candidate / Log Viewer rename review file")
    primary = root / "USER Review" / PRIMARY_REVIEW
    if primary.exists() and PACKET_STATUS not in _read(primary):
        failures.append("primary review file missing packet status")
    for rel in REQUIRED_REVIEW_AIDS:
        if not (root / rel).is_file():
            failures.append(f"missing review aid: {rel}")
    media_dir = root / "Review Aids/Rendered Media"
    present_media = {path.name for path in media_dir.glob("*.png")} if media_dir.exists() else set()
    missing_media = sorted(REQUIRED_MEDIA - present_media)
    if missing_media:
        failures.append(f"missing rendered media: {', '.join(missing_media)}")
    context_names = {path.name for path in (root / "Source Truth Context").glob("*") if path.is_file()} if (root / "Source Truth Context").exists() else set()
    missing_context = sorted(set(SOURCE_CONTEXT) - context_names)
    if missing_context:
        failures.append(f"missing Source Truth Context files: {', '.join(missing_context)}")
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "\x00" in text:
            failures.append(f"text hygiene null byte: {path.relative_to(root)}")
        if "lorem ipsum" in text.casefold() or "todo" in text.casefold():
            failures.append(f"placeholder text found: {path.relative_to(root)}")
    log_json = root / "Review Aids/Log Viewer Candidate/log_viewer_candidate.json"
    if log_json.exists():
        data = json.loads(_read(log_json))
        forbidden = " ".join(data.get("forbiddenPatternsExcluded", []))
        for phrase in ("fake data rows", "local path display by default", "helper/proof commentary"):
            if phrase not in forbidden:
                failures.append(f"log option forbidden pattern missing: {phrase}")
    rec_json = root / "Review Aids/Recording Studio Options/recording_studio_options.json"
    if rec_json.exists():
        data = json.loads(_read(rec_json))
        controls = set(data.get("requiredControlsExplored", []))
        for control in ("START", "PAUSE", "STOP", "OPEN LOG VIEWER"):
            if control not in controls:
                failures.append(f"recording option missing required control exploration: {control}")
        option_ids = {row.get("option_id") for row in data.get("options", [])}
        if option_ids != {"REC-A", "REC-C"}:
            failures.append("recording candidates must be exactly REC-A and REC-C")
        if "REC-B" not in set(data.get("excludedOptions", [])):
            failures.append("recording candidates must explicitly exclude REC-B")
    return failures


def is_runtime_ui_immersion_options_packet(root: Path) -> bool:
    primary = root / "USER Review" / PRIMARY_REVIEW
    manifest = root / "Review Aids" / "packet_manifest.json"
    if not primary.is_file() or not manifest.is_file():
        return False
    return PACKET_STATUS in _read(primary)


def _zip_packet(packet_time: str) -> dict[str, str]:
    for old_zip in USER_ROOT.glob("FAM-006-*.zip"):
        old_zip.unlink()
    zip_path = USER_ROOT / f"FAM-006-{packet_time}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKET_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKET_ROOT).as_posix())
    proof = {
        "External State Schema": "external-state-v1",
        "schema": "fam006-runtime-ui-immersion-post-zip-manifest-v1",
        "packetRoot": str(PACKET_ROOT),
        "zipPath": str(zip_path),
        "zipSha256": _sha256(zip_path),
        "generatedAt": packet_time,
        "nonSelfMutatingShaProof": True,
    }
    EXTERNAL_BRANCH_ROOT.mkdir(parents=True, exist_ok=True)
    _write_json(EXTERNAL_BRANCH_ROOT / "runtime_ui_immersion_options_post_zip_manifest.json", proof)
    return proof


def generate() -> int:
    if _identity()["branch"] != BRANCH:
        print("BLOCKED: wrong branch")
        return 2
    packet_time = time.strftime("%Y%m%d-%H%M%S")
    media_root = SCREENSHOT_ROOT / packet_time
    result = _write_packet(media_root, packet_time)
    failures = validate_packet(PACKET_ROOT)
    self_validation = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "packetRoot": str(PACKET_ROOT),
        "timestamp": packet_time,
    }
    _write_json(PACKET_ROOT / "Review Aids/Validation Outputs/packet_self_validation.json", self_validation)
    if failures:
        print(json.dumps(self_validation, indent=2))
        return 1
    proof = _zip_packet(packet_time)
    print(json.dumps({"status": "PASS", **result, "zip": proof}, indent=2))
    return 0


def validate() -> int:
    failures = validate_packet(PACKET_ROOT)
    status = {"status": "PASS" if not failures else "FAIL", "failures": failures}
    print(json.dumps(status, indent=2))
    return 0 if not failures else 1


def zip_only() -> int:
    manifest_path = PACKET_ROOT / "Review Aids" / "packet_manifest.json"
    if not manifest_path.is_file():
        print("packet manifest missing")
        return 1
    manifest = json.loads(_read(manifest_path))
    packet_time = str(manifest.get("generatedAt") or time.strftime("%Y%m%d-%H%M%S"))
    failures = validate_packet(PACKET_ROOT)
    if failures:
        print(json.dumps({"status": "FAIL", "failures": failures}, indent=2))
        return 1
    proof = _zip_packet(packet_time)
    print(json.dumps({"status": "PASS", "zip": proof}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--validate-packet", action="store_true")
    parser.add_argument("--zip-only", action="store_true")
    args = parser.parse_args()
    if args.generate:
        return generate()
    if args.validate_packet:
        return validate()
    if args.zip_only:
        return zip_only()
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
