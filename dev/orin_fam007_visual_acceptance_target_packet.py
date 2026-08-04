"""Generate and validate the FAM-007 visual acceptance target USER packet.

Helper Status: Workstream-scoped
Owner Workstream: FAM-007 AI Dashboard / AI Control Center visual target gate
Reason Reusable Helper Was Not Extended: this pass is branch-local and depends on
the active FAM-007 external state, current proof roots, and single-current-packet
review rules.
Consolidation Target: future reusable visual-target packet helper after
Governance/FAM-002 defines a global template.
Promotion Decision Point: before PR Readiness or when a second branch needs the
same visual-target packet contract.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from nexus_paths import EXTERNAL_STATE_ROOT, USER_HUB_ROOT


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKTREE_LABEL = "FAM-007"
BRANCH_SLUG = "feature_fam_007_ai_control_center_readiness_diagnostics"
EXTERNAL_BRANCH_ROOT = EXTERNAL_STATE_ROOT / "branches" / BRANCH_SLUG
BRANCH_STATE = EXTERNAL_BRANCH_ROOT / "branch_state.md"
BRANCH_PLAN = EXTERNAL_BRANCH_ROOT / "branch_plan.md"
UDL_PATH = EXTERNAL_BRANCH_ROOT / "unified_defect_ledger.md"
USER_ROOT = USER_HUB_ROOT
PACKET_DIR = USER_ROOT / WORKTREE_LABEL
ACCEPTED_HISTORICAL_ZIP = USER_ROOT / "FAM-007-20260623-123429.zip"
PRIMARY_REVIEW_FILE = "VISUAL_ACCEPTANCE_TARGET_REVIEW.md"
RECOVERY_PRIMARY_REVIEW_FILE = "ACCEPTED_HISTORICAL_PACKET_RECOVERY_REVIEW.md"
BLOCKED_GATES = (
    "H1/LV acceptance; USER UTS acceptance; PR Readiness; PR creation; merge; release; "
    "cleanup; issue mutation; provider/model execution; prompt send; downloads; runtime "
    "cache behavior; memory/learning/personalization; private Developer/Owner setup; "
    "installer/shortcut/packaging execution; sibling/Governance mutation; imports; "
    "v1.8.0 work."
)
VISUAL_PACKET_PURPOSE = (
    "Branch-local visual acceptance target process and review packet. It creates rendered "
    "targets, legends, selection ledgers, a draft target, rejected-pattern and reusable-"
    "recipe templates, artifact-to-surface mapping, caveat and material-deviation rules, "
    "state coverage planning, and validation evidence before any future visible UI/UX "
    "implementation."
)
VISUAL_NEXT_LEGAL_PHASE = (
    "USER review of the branch-local Visual Acceptance Target packet only. H1/LV "
    "acceptance, the later LV1 review gate, USER UTS acceptance, and PR Readiness "
    "remain separate pending gates requiring later source-truth-routed USER decisions "
    "after this packet is accepted or revised."
)
RECOVERY_NEXT_LEGAL_PHASE = (
    "USER decision on the accepted-historical packet recovery / retention blocker packet "
    "and missing accepted-historical packet artifact. USER may accept the packet and "
    "provide the missing accepted historical ZIP, accept the packet and approve a "
    "retention waiver, or hold the packet chain blocked while directing a later "
    "source-truth-routed recovery path."
)
PROOF_ROOT = Path(
    r"C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI"
    r"\FAM-007-H4\20260623-112831-child-window"
)
PROOF_LOG_ROOT = REPO_ROOT / "dev" / "logs" / "fam_007_ai_control_center_live_resize" / "20260623-112831"
MANIFEST_PATH = PROOF_LOG_ROOT / "live_resize_manifest.json"
OPTION_IDS = ("OPTION-A", "OPTION-B", "OPTION-C", "OPTION-D", "OPTION-E", "OPTION-F", "OPTION-G")
EXPECTED_RENDER_IMAGE_COUNT = len(OPTION_IDS) * 4
EXPECTED_ANNOTATED_IMAGE_COUNT = len(OPTION_IDS) * 2
DRAFT_TEMPLATE_ROOT = "Review Aids/Draft Window Templates"
DRAFT_RENDER_AUTHORITY = "Real rendered draft-window/template using branch-local HTML/CSS and PySide6 QWebEngine screenshot capture"
OPTION_F_SEED_PACKET_PATH = r"D:\Nexus Desktop AI Data\USER\FAM-007-20260624-142922.zip"
OPTION_F_SEED_PACKET_SHA256 = "eb7a73ff42cbcc502fe093efc21aed2e789a39d4ac00323a1d9467e7bb672092"
OPTION_F_FUTURE_OWNER_ROUTE = (
    "FAM-003 for Global Settings / parent-window customization controls; "
    "FAM-006 for HUD Dashboard adoption; FAM-002/UIREF for reusable visual grammar or template promotion; "
    "Governance/phase owner if this becomes a cross-branch acceptance rule"
)
OPTION_F_NON_APPROVALS = (
    "not runtime implementation; not active settings behavior; not persistence/schema approval; "
    "not drag/drop approval; not cross-FAM adoption approval; not global template promotion"
)

REQUIRED_PACKET_FILES = [
    "START_HERE.md",
    "USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md",
    "Review Aids/VISUAL_IMPACT_CLASSIFICATION.md",
    "Review Aids/VISUAL_OPTIONS_PACKET.md",
    "Review Aids/ELEMENT_LEGENDS.md",
    "Review Aids/ANNOTATION_MANIFEST.md",
    "Review Aids/IMAGE_RELEVANCE_MANIFEST.md",
    "Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md",
    "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
    "Review Aids/STATE_COVERAGE_MATRIX.md",
    "Review Aids/STATE_COVERAGE_STORYBOARD.md",
    "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
    "Review Aids/CAVEAT_LEDGER.md",
    "Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md",
    "Review Aids/FUTURE_LAYOUT_ARRANGEMENT_CANDIDATES.md",
    "Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md",
    "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
    "Review Aids/REJECTED_PATTERNS_LEDGER.md",
    "Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
    "Review Aids/SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md",
    "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md",
    "Review Aids/UI_UX_WORKSTREAM_EXIT_GATE_CANDIDATE.md",
    "Review Aids/UDL_FALSE_GREEN_STATUS.md",
    "Review Aids/VALIDATION_SUMMARY.md",
    "Source Truth Context/current_external_branch_state.md",
    "Source Truth Context/current_external_branch_plan.md",
    "Source Truth Context/branch_record.md",
    "Source Truth Context/validation_helper_registry.md",
    "Source Truth Context/ui_reference_catalog_index.md",
    "Source Truth Context/UIREF-001_top_level_window_frame.md",
    "Source Truth Context/UIREF-002_window_control_cluster.md",
    "Source Truth Context/UIREF-003_control_state_and_selector_grammar.md",
    "Source Truth Context/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
    "Source Truth Context/UIREF-005_design_token_and_shared_rule_baseline.md",
    "Source Truth Context/UIREF-006_negative_example_and_enforcement_contract.md",
]


@dataclass(frozen=True)
class RenderOption:
    option_id: str
    authority: str
    footprint: str
    focused_media: str
    desktop_media: str
    annotated_focused_media: str
    annotated_desktop_media: str
    description: str


@dataclass(frozen=True)
class AnnotationSpec:
    option_id: str
    annotation_id: str
    element_type: str
    target_label: str
    region: tuple[int, int, int, int]
    marker_style: str
    color_name: str
    color: tuple[int, int, int]
    non_color_cue: str
    purpose: str


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(relative_path: str, text: str) -> None:
    target = PACKET_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8")


def _copy_file(source: Path, relative_path: str) -> None:
    target = PACKET_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _packet_file_entries() -> list[Path]:
    return sorted(path for path in PACKET_DIR.rglob("*") if path.is_file())


def _zip_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _accepted_historical_zips() -> set[Path]:
    return set()


def _purge_packet_root() -> None:
    if PACKET_DIR.exists():
        shutil.rmtree(PACKET_DIR)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    accepted = _accepted_historical_zips()
    for zip_path in USER_ROOT.glob(f"{WORKTREE_LABEL}-*.zip"):
        if zip_path not in accepted:
            zip_path.unlink()
    stable_zip = USER_ROOT / f"{WORKTREE_LABEL}.zip"
    if stable_zip.exists():
        stable_zip.unlink()


def _update_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}: `.*?`$", re.MULTILINE)
    replacement = f"{field}: `{value}`"
    if pattern.search(text):
        return pattern.sub(lambda _match: replacement, text, count=1)
    return text.rstrip() + "\n" + replacement + "\n"


def _replace_section(text: str, heading: str, lines: list[str]) -> str:
    replacement = "\n".join([heading, "", *lines]).rstrip()
    pattern = re.compile(rf"^{re.escape(heading)}\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda _match: replacement + "\n\n", text, count=1)
    return text.rstrip() + "\n\n" + replacement + "\n"


def _section(text: str, heading: str) -> str:
    text = text.replace("\r\n", "\n")
    match = re.search(rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    return match.group("body") if match else ""


def _visual_exact_user_decision_text(zip_path: Path) -> str:
    return (
        f"I accept the FAM-007 branch-local Visual Acceptance Target packet at {zip_path} "
        "as the current USER review packet for visual target/process selection only. I "
        "accept that the visible current review surface is USER Review/"
        f"{PRIMARY_REVIEW_FILE}, that packet validation is not USER acceptance, and that "
        f"this is the only current FAM-007 USER packet ZIP retained under {USER_HUB_ROOT}. "
        "This does not approve H1/LV acceptance, the later "
        "LV1 review gate, USER UTS acceptance, PR Readiness, PR creation, merge, release, "
        "cleanup, issue mutation, provider/model execution, prompt send, downloads, "
        "runtime cache behavior, memory/learning/personalization, private Developer/Owner "
        "setup, installer/shortcut/packaging execution, sibling/Governance mutation, "
        "imports, or v1.8.0 work."
    )


def _visual_next_legal_phase_lines(zip_path: Path) -> list[str]:
    return [
        f"Next Legal Phase: `{VISUAL_NEXT_LEGAL_PHASE}`",
        f"Exact USER Decision Text: `{_visual_exact_user_decision_text(zip_path)}`",
    ]


def _recovery_exact_user_decision_text(zip_path: Path) -> str:
    return (
        f"I accept the FAM-007 accepted-historical packet recovery / retention blocker "
        f"packet at {zip_path}. I understand that {ACCEPTED_HISTORICAL_ZIP} was not found "
        "in the searched local roots, that Codex did not recreate or fake the accepted "
        "historical artifact, and that packet validation, ChatGPT review, helper PASS, "
        "external-state updates, or Codex digests are not USER acceptance. I choose this "
        "artifact disposition: [provide/upload the missing ZIP] OR [approve an explicit "
        "retention waiver for the missing accepted-historical ZIP while preserving "
        "F7-UDL-018 as waived historical retention debt] OR [keep the packet chain blocked "
        "and direct a later source-truth-routed recovery path]. This does not approve "
        "H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, "
        "unrelated cleanup, issue mutation, provider/model execution, prompt send, downloads, "
        "runtime cache behavior, memory/learning/personalization, private Developer/Owner "
        "setup, installer/shortcut/packaging execution, sibling/Governance mutation, "
        "imports, or v1.8.0 work."
    )


def _recovery_next_legal_phase_lines(zip_path: Path) -> list[str]:
    return [
        f"Next Legal Phase: `{RECOVERY_NEXT_LEGAL_PHASE}`",
        f"Exact USER Decision Text: `{_recovery_exact_user_decision_text(zip_path)}`",
    ]


def _update_branch_state_for_visual_packet(text: str, zip_path: Path) -> str:
    text = _update_field(
        text,
        "External State Item Status",
        (
            f"Current USER review packet is the branch-local Visual Acceptance Target packet "
            f"{zip_path}. It is a reviewable visual-target/process packet only. The accepted "
            "historical Workstream implementation / H1-LV proof packet is retained as "
            "external-state history and copied source-truth context only, not as a second "
            "root USER packet ZIP. H1/LV "
            f"acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, "
            f"cleanup, issue mutation, provider/model execution, prompt send, downloads, "
            f"runtime cache behavior, memory/learning/personalization, private Developer/Owner "
            f"setup, installer/shortcut/packaging execution, sibling/Governance mutation, "
            f"imports, and v1.8.0 remain blocked."
        ),
    )
    text = _update_field(
        text,
        "Current Gate",
        (
            "USER review of the branch-local Visual Acceptance Target packet; the underlying "
            "Hardening H1 / Live Validation decision gate remains pending separate USER "
            "approval and is not accepted by this packet."
        ),
    )
    text = _update_field(
        text,
        "Packet Reviewability State",
        (
            f"Visual Acceptance Target packet generated for USER review at {zip_path}; "
            "packet validation is supporting evidence only and is not USER acceptance."
        ),
    )
    text = _update_field(
        text,
        "USER Gate State",
        (
            "Pending USER review of the Visual Acceptance Target packet; H1/LV acceptance "
            "and USER UTS acceptance remain pending separate USER decision."
        ),
    )
    text = _update_field(
        text,
        "Next Legal Phase",
        VISUAL_NEXT_LEGAL_PHASE,
    )
    return _replace_section(text, "## Next Legal Phase", _visual_next_legal_phase_lines(zip_path))


def _update_branch_plan_for_visual_packet(text: str, zip_path: Path) -> str:
    text = _replace_section(
        text,
        "## Packet Review State",
        [
            (
                "Packet Reviewability State: `Reviewable branch-local Visual Acceptance Target "
                f"packet at {zip_path}. Packet validation is not USER acceptance; this packet "
                "does not accept H1/LV, USER UTS, PR Readiness, PR creation, merge, release, "
                "or runtime/provider/private/cache/memory/download/packaging work.`"
            ),
            "RAR Packet Reviewability State: `Accepted historical RAR evidence remains context only; this Visual Acceptance Target packet is the only current retained FAM-007 USER packet ZIP.`",
            "USER Gate State: `Pending USER review of the Visual Acceptance Target packet; H1/LV resume requires separate approval.`",
            f"Primary USER Review File: `{PRIMARY_REVIEW_FILE}`",
            f"USER Review Folder: `{PACKET_DIR}`",
            f"USER Review ZIP: `{zip_path}`",
            "Packet Validation Is USER Acceptance: `No`",
        ],
    )
    return _replace_section(text, "## Next Legal Phase", _visual_next_legal_phase_lines(zip_path))


def _update_branch_state_for_recovery_packet(text: str, zip_path: Path) -> str:
    text = _update_field(
        text,
        "External State Item Status",
        (
            f"Current USER review packet is the accepted-historical packet recovery / "
            f"retention blocker packet {zip_path}. ChatGPT review may classify it as "
            f"ACCEPTED FOR USER REVIEW / truthful blocker evidence, but USER acceptance "
            f"remains pending until exact USER decision text is provided. The accepted historical Workstream "
            f"implementation / H1-LV proof packet {ACCEPTED_HISTORICAL_ZIP} is missing "
            f"from local retained artifacts after required search and is not currently "
            f"preserved. H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, "
            f"merge, release, unrelated cleanup, issue mutation, provider/model execution, "
            f"prompt send, downloads, runtime cache behavior, memory/learning/personalization, "
            f"private Developer/Owner setup, installer/shortcut/packaging execution, "
            f"sibling/Governance mutation, imports, and v1.8.0 remain blocked."
        ),
    )
    text = _update_field(
        text,
        "Current Gate",
        (
            "USER decision on accepted-historical artifact disposition remains pending; "
            "ChatGPT review may accept the recovery / retention blocker packet as "
            "reviewable truthful blocker evidence only."
        ),
    )
    text = _update_field(
        text,
        "Packet Reviewability State",
        (
            f"Accepted-historical recovery / retention blocker packet is reviewable at "
            f"{zip_path}; ChatGPT review verdict may be ACCEPTED FOR USER REVIEW / truthful "
            "blocker evidence; packet validation and ChatGPT review are supporting evidence "
            "only and are not USER acceptance."
        ),
    )
    text = _update_field(
        text,
        "USER Gate State",
        (
            "Pending USER decision. USER has not provided the missing ZIP, approved a "
            "retention waiver, accepted the recovery blocker packet as a USER decision, "
            "or selected a later source-truth-routed recovery path. H1/LV acceptance and "
            "USER UTS acceptance remain pending separate USER decision."
        ),
    )
    text = _update_field(text, "Next Legal Phase", RECOVERY_NEXT_LEGAL_PHASE)
    return _replace_section(text, "## Next Legal Phase", _recovery_next_legal_phase_lines(zip_path))


def _update_branch_plan_for_recovery_packet(text: str, zip_path: Path) -> str:
    text = _replace_section(
        text,
        "## Packet Review State",
        [
            (
                "Packet Reviewability State: `Reviewable accepted-historical packet "
                f"recovery / retention blocker packet at {zip_path}. ChatGPT review may "
                "classify it as ACCEPTED FOR USER REVIEW / truthful blocker evidence only. "
                "Packet validation and ChatGPT review are not USER acceptance; the accepted "
                "historical ZIP is missing and is not claimed preserved by this active packet.`"
            ),
            "Accepted Historical Packet: `MISSING - C:\\Nexus USER\\FAM-007-20260623-123429.zip was not recovered in searched local roots.`",
            "USER Gate State: `Pending USER decision. USER has not accepted the recovery blocker packet as a USER decision, provided/uploaded the missing ZIP, explicitly approved a retention waiver, or selected a later source-truth-routed recovery path.`",
            f"Primary USER Review File: `{RECOVERY_PRIMARY_REVIEW_FILE}`",
            f"USER Review Folder: `{PACKET_DIR}`",
            f"USER Review ZIP: `{zip_path}`",
            "Packet Validation Is USER Acceptance: `No`",
        ],
    )
    return _replace_section(text, "## Next Legal Phase", _recovery_next_legal_phase_lines(zip_path))


def _append_receipt(path: Path, heading: str, lines: list[str]) -> None:
    text = _read_text(path)
    if heading in text:
        return
    body = "\n\n" + heading + "\n\n" + "\n".join(lines) + "\n"
    path.write_text(text.rstrip() + body, encoding="utf-8")


def _remove_stale_packet_sprawl_receipts(path: Path) -> None:
    text = _read_text(path)
    cleaned = text
    for heading_pattern in (
        r"Branch-Local Visual Acceptance Target Packet Receipt - .+?",
        r"Accepted-Historical Packet Recovery / Retention Blocker Receipt - .+?",
        r"H1 / Live Validation Decision-Prep Packet Receipt - .+?",
    ):
        cleaned = re.sub(
            rf"\n## {heading_pattern}\n.*?(?=\n## |\Z)",
            "",
            cleaned,
            flags=re.DOTALL,
        )
    replacements = {
        "Accepted Historical Packet:": "Previously Accepted Review Packet:",
        "Missing Accepted Historical Packet:": "Superseded Missing Artifact Reference:",
        "Previously Missing Accepted Historical Packet:": "Superseded Missing Artifact Reference:",
        "packet stale-same-label cleanup versus accepted historical ZIP preservation requires USER/governance decision before regenerating C:\\Nexus USER\\FAM-007": "single-current-packet rule resolved same-label cleanup; only the current regenerated FAM-007 ZIP remains under C:\\Nexus USER",
        "Do not regenerate the next H1/LV decision packet until USER resolves the accepted-historical same-label ZIP preservation versus normal stale same-label cleanup handling, or Governance provides a packet artifact retention rule.": "Resolved by USER single-current-packet direction: do not preserve a second FAM-007 root ZIP; regenerate only the current packet and purge stale same-label ZIPs.",
    }
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    if cleaned != text:
        path.write_text(cleaned.rstrip() + "\n", encoding="utf-8")


def _historical_artifact_sha256() -> str:
    if not ACCEPTED_HISTORICAL_ZIP.exists():
        return "MISSING"
    return hashlib.sha256(ACCEPTED_HISTORICAL_ZIP.read_bytes()).hexdigest().upper()


def _mark_udl_018_restored(udl_text: str, zip_path: Path) -> str:
    restored_lines = [
        "Status: `SUPERSEDED_BY_SINGLE_CURRENT_PACKET_RULE`",
        f"Superseded Artifact Path: `{ACCEPTED_HISTORICAL_ZIP}`",
        f"Superseded Artifact SHA256 When Present: `{_historical_artifact_sha256()}`",
        "Accepted-Historical Validation: `Not required for the active Visual Acceptance Target packet after USER clarified that FAM-007 must retain one current USER packet ZIP only.`",
        "Restoration Disposition: `The prior missing-artifact repair is historical context only. The active packet chain no longer preserves or requires a standalone accepted-historical ZIP under C:\\Nexus USER; current packet evidence is regenerated into the single current packet folder/ZIP.`",
        f"Current Review Packet: `{zip_path}`",
        "USER Packet Acceptance: `Pending USER review of the current Visual Acceptance Target packet. Packet validation, ChatGPT review, helper PASS, external-state updates, or Codex digests are not USER acceptance.`",
        "Trace Preservation: `This row preserves that an accepted-historical artifact repair occurred, then was superseded by the USER single-current-packet rule to prevent packet ZIP sprawl.`",
    ]
    if "## F7-UDL-018 " not in udl_text:
        return (
            udl_text.rstrip()
            + "\n\n## F7-UDL-018 Accepted-Historical Artifact Restored - 2026-06-24\n\n"
            + "\n".join(restored_lines)
            + "\n"
        )
    replacement = (
        "## F7-UDL-018 Accepted-Historical Artifact Restored - 2026-06-24\n\n"
        + "\n".join(restored_lines)
        + "\n"
    )
    return re.sub(
        r"## F7-UDL-018 .+?(?=\n## |\Z)",
        lambda _match: replacement,
        udl_text,
        count=1,
        flags=re.DOTALL,
    )


def _update_visual_packet_udl_rows(udl_text: str, zip_path: Path) -> str:
    row_019 = f"""## F7-UDL-019 Visual Target Legend Mapping / Annotation Bounds - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The branch-local Visual Acceptance Target packet generator could create visual legends that were hard to map to exact render regions, and focused annotated renders could clip or truncate callout labels outside the image canvas. The prior six broad callouts were still too generic for USER feedback such as "change D-ROW-01B" or "move D-BTN-03."`
Required Disposition: `Future Visual Acceptance Target packets must include clean and annotated focused render pairs, option-specific group-level and element-level annotation IDs, color plus non-color cues, an annotation manifest mapping each visible ID to element/group type, target label, marker style, visual region, in-canvas label box, leader line, and purpose, plus template-not-endstate wording.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now renders annotated images with option-specific IDs such as A-STATUS-01, D-CARD-02, D-ROW-02B, E-CARD-04, E-BTN-04, F-SUMMARY-01, and F-BTN-00; keeps clean focused renders beside annotated focused renders; records element/group type, target label, marker style, color cue, non-color cue, label boxes, and leader lines in ANNOTATION_MANIFEST.md; and validates annotation geometry, visible ID pixels, group/element coverage, and clean+annotated pairing for every option.`
Proof: `Current Visual Acceptance Target packet validation fails if any annotation target, label box, or leader line extends outside the image canvas, if a visible ID label cannot be detected, if an option lacks group-level or element-level IDs, if Option D, Option E, or Option F lacks precise required IDs, or if any option lacks the primary clean focused plus annotated focused render pair.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair does not restore or require a second historical packet ZIP and does not approve H1/LV, USER UTS, PR Readiness, PR creation, merge, release, provider/model/private/cache/memory/download/packaging, sibling mutation, imports, or v1.8.0 work.`
"""
    row_021 = f"""## F7-UDL-021 Final Packet Image Relevance / Decision Clarity - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `Final USER-review packets that are not repair-cycle/debug packets can over-include raw proof dumps or helper-only screenshot evidence, making the current USER decision ambiguous.`
Required Disposition: `Final Visual Acceptance Target packets must include only USER decision images, required context images, and required annotation images needed to compare, select, accept, reject, or revise the current visual target. Repair/debug evidence images must be excluded from final USER decision packets unless a current source-truth rule admits them for that decision and labels them clearly.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now writes IMAGE_RELEVANCE_MANIFEST.md, declares every included image classification and USER purpose, excludes raw H1/LV screenshot proof dumps from the final visual-target packet, and validates that the final packet contains exactly the curated render media images with declared USER-decision purposes.`
Proof: `Current Visual Acceptance Target packet validation fails when an included image lacks a declared USER-decision purpose, when final packet images appear outside the curated Render Media path, when image counts drift from the expected curated set, or when START_HERE / primary USER review bypass the curated decision path.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair preserves artifact-of-record validation for the current packet without overloading the final USER-facing decision packet with repair/debug proof images.`
"""
    row_022 = f"""## F7-UDL-022 Visual Acceptance Comparative-Audit Ledger Hardening - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The branch-local Visual Acceptance Target packet was weaker than the FAM-003 comparison model for artifact-to-surface mapping, implementation-difference rules, accepted-with-caveats handling, rejected-pattern explanations, and FAM-007-specific state coverage clarity.`
Required Disposition: `Current and future FAM-007 Visual Acceptance Target packets must include explicit artifact-to-surface mapping, material-deviation / implementation-difference rules, caveat handling, strengthened rejected-pattern explanations, and a FAM-007 state coverage storyboard or plan.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now generates ARTIFACT_TO_SURFACE_LEDGER.md, IMPLEMENTATION_DIFFERENCE_RULE.md, CAVEAT_LEDGER.md, STATE_COVERAGE_STORYBOARD.md, a stronger STATE_COVERAGE_MATRIX.md, and a stronger REJECTED_PATTERNS_LEDGER.md, while preserving template-not-endstate wording and single-current-packet boundaries.`
Proof: `Current Visual Acceptance Target packet validation fails if the artifact-to-surface ledger, implementation-difference rule, caveat ledger, state storyboard, rejected-pattern ledger, or required boundary terms are missing from the generated packet or final ZIP.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair does not approve H1/LV, USER UTS, PR Readiness, PR creation, merge, release, provider/model/private/cache/memory/download/packaging, sibling mutation, imports, v1.8.0 work, or global Governance/FAM-002/UIREF mutation.`
"""
    row_023 = f"""## F7-UDL-023 Option D Row-Grammar Visual Target Candidate - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The prior Visual Acceptance Target packet presented Option A, Option B, and Option C without a distinct hybrid target that carried the USER-approved old AI Control Center row grammar as a reference while preserving the current AI Dashboard / AI Control Center doorway model. The first Option D repair added the hybrid target, but its annotation overlay was still too broad to support precise USER feedback about rows, cards, buttons, and status strips.`
Required Disposition: `Current FAM-007 visual target packets must present Option D as a branch-local hybrid candidate: Option A source-truth product structure and doorway labels, Option B compact grouping rhythm, accepted old AI Control Center row grammar as a visual grammar reference, and Option C as rejected-risk boundary only. Option D annotations must expose row-level, card-level, button-level, status-strip, header, and control-cluster review IDs. Option D is still a candidate render, not implementation proof or a product/runtime mutation.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now generates Option D / D2 clean focused, annotated focused, clean desktop/context, and annotated desktop/context renders with IDs such as D-HEADER-01, D-STATUS-01, D-CARD-01, D-ROW-01A, D-ROW-02B, D-BTN-03; maps those IDs through image relevance, annotation, artifact-to-surface, state, rejected-pattern, and primary USER review text; and validates the retained historical/context options as part of the curated final-packet image set. The D2 refinement makes the option read as a mature draft window rather than a generated concept while keeping the compact grouped-doorway boundary.`
Proof: `Current Visual Acceptance Target packet validation fails if Option D, its row-level/card-level/button-level/status-level IDs, its row-grammar wording, or its curated render media are missing from the generated folder or ZIP.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair does not approve runtime UI implementation, H1/LV, USER UTS, PR Readiness, PR creation, merge, release, provider/model/private/cache/memory/download/packaging, sibling/Governance/FAM-002/UIREF mutation, imports, or v1.8.0 work.`
"""
    row_024 = f"""## F7-UDL-024 UI/UX Workstream Exit Acceptance Gate Candidate - 2026-06-24

Status: `GOVERNANCE_CANDIDATE_RECORDED`
Finding: `FAM-007 and FAM-006 false-green loops show that UI/UX-bearing branches can leave Workstream with helper PASS, screenshot existence, ChatGPT review, or packet reviewability even when USER visual acceptance is pending, rejected, stale, or unproven. That gap can route visibly deficient UI into Hardening or Live Validation and make the USER discover defects that should have been blocked earlier.`
Required Disposition: `A durable UI/UX Workstream Exit Acceptance Gate belongs in the phase-governance / FAM-002 / UIREF governance carrier, not as silent global law inside this FAM-007 packet pass. This branch may record the candidate, generate USER-reviewable wording, and enforce branch-local packet boundary text, but it must not mutate global Governance/FAM-002/UIREF without the correct carrier.`
Candidate Rule: `For branches that implemented, materially repaired, or materially changed user-facing UI/UX, visual layout, interactive window behavior, child/domain window behavior, user-facing card/row/control grammar, or visual target implementation, Workstream exit should require USER Accepted, USER Accepted With Caveats, USER Waived, USER Deferred With Explicit Source-Truth Boundary, or Not Applicable With Reason before Hardening, Live Validation, PR Readiness, PR creation, merge, or release-facing progression. Packet Reviewability State, ChatGPT review, helper PASS, screenshot existence, and visual-target acceptance alone are not USER acceptance or implementation proof.`
Proof: `The regenerated Visual Acceptance Target packet includes Review Aids/UI_UX_WORKSTREAM_EXIT_GATE_CANDIDATE.md and Review Aids/GOVERNANCE_CANDIDATE_ONLY.md with exact owner, proposed rule shape, blocker names, validator/helper impacts, and USER decision needed.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This row records a governance candidate only. It does not mutate Docs/phase_governance.md, FAM-002, UIREF, sibling worktrees, H1/LV acceptance, USER UTS, PR Readiness, PR creation, merge, release, provider/model/private/cache/memory/download/packaging, imports, or v1.8.0 work.`
"""
    row_025 = f"""## F7-UDL-025 Visual Acceptance Exploration Loop / Variant Generation - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The branch-local Visual Acceptance Target packet could be read as a "pick the cleanest available option" packet instead of a USER-guided exploration and refinement loop. That would let Codex recommendations, available renders, helper PASS, or packet validation substitute for USER visual preference and could lead to near-duplicate variant churn instead of meaningful compliant new directions.`
Required Disposition: `Current and future FAM-007 Visual Acceptance Target packets must state that clean enough is not the acceptance standard. The standard is USER-selected visual direction after meaningful compliant option exploration. When USER does not accept a target, the next cycle must generate revised, combined, or new real draft-window variants with retained traits, rejected traits, new territory, and material-difference explanation.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now generates Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md, strengthens START_HERE and the primary USER review file, expands the Visual Selection Ledger template with retained/rejected/new-territory fields, records no-near-duplicate and real-draft-window requirements, and validates exploration-loop, variant-distinctness, and retained/rejected-traits wording in the folder and final ZIP. The current cycles add Option E as a polish/reference candidate, Option F as a future layout-arrangement candidate with a wide top summary/action zone and horizontal domain lanes, and Option G as the recommended D-primary/E-polish refined target while preserving A/B/C/D as comparison context.`
Proof: `Current Visual Acceptance Target packet validation fails if the packet omits VISUAL_ACCEPTANCE_EXPLORATION_LOOP, VAT-CYCLE-20260624-02, VAT-CYCLE-20260624-03, Option E, Option F, Option G, the clean-enough rejection standard, retained traits, rejected traits, new territory, material differences, no near-duplicates, real draft-window requirement, or the statement that packet validation proves completeness/currentness only and not USER acceptance or preference.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This row records branch-local process hardening and a governance candidate only. It does not mutate runtime UI, Docs/phase_governance.md, Governance, FAM-002, UIREF, sibling worktrees, H1/LV acceptance, USER UTS, PR Readiness, PR creation, merge, release, provider/model/private/cache/memory/download/packaging, imports, or v1.8.0 work.`
"""
    row_026 = f"""## F7-UDL-026 Real Draft Window Template Render Repair - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The prior Visual Acceptance Target packet was reviewable as a concept packet, but Options B through F were static concept drawings produced by the helper rather than actual usable rendered draft windows/templates. That let a packet look polished while failing the USER standard for real draft-window/template review. The current refinement extends the same standard to Option G.`
Required Disposition: `Current selectable or current-cycle options must be actual runtime screenshots or real rendered draft-window/template media. Static concept drawings may remain only as clearly labeled historical/rejected/reference evidence and must not be presented as selectable current visual targets.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now renders Options B through G from branch-local HTML/CSS draft-window templates through PySide6 QWebEngine before annotation overlays are added; writes Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md; keeps Option A as actual runtime baseline; demotes Option F as a future user-customizable layout arrangement candidate; and validates focused/desktop HTML template artifacts for every non-runtime option.`
Proof: `Current Visual Acceptance Target packet validation fails if the draft-window template render manifest is missing, if non-runtime options lack focused and desktop HTML template artifacts, if required real rendered draft-window/template wording is missing, if PIL/ImageDraw is claimed as clean candidate media authority, or if ZIP/folder parity omits the template artifacts.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair does not mutate runtime UI, create a reusable/global template, mutate Governance/FAM-002/UIREF/sibling worktrees, approve H1/LV, USER UTS, PR Readiness, PR creation, merge, release, issue mutation, provider/model/private/cache/memory/download/packaging, imports, or v1.8.0 work.`
"""
    row_027 = f"""## F7-UDL-027 Option F Future Layout Arrangement Candidate Preservation - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The USER identified Option F as useful future parent-window layout-customization evidence, but it must not be converted into the current selected FAM-007 visual target, runtime implementation approval, Global Settings behavior, persistence/schema approval, drag/drop approval, HUD Dashboard adoption, UIREF/FAM-002 template promotion, or global Governance rule from this branch-local carrier.`
Required Disposition: `Preserve Option F as a future candidate, possible USER-configurable layout arrangement pattern, and example only, subject to later source-truth owner approval. The record must cite the seed packet path and SHA, Option F artifact paths, deterministic reorder/renumber example, future surfaces, future owners, and explicit non-approvals.`
Source Packet: `{OPTION_F_SEED_PACKET_PATH}`
Source Packet SHA256: `{OPTION_F_SEED_PACKET_SHA256}`
Option F Artifact Paths: `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_focused.png`; `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_desktop.png`; `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_focused_annotated.png`; `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_desktop_annotated.png`; `Review Aids/Draft Window Templates/Option-F-wide-orientation-lanes/option-f_focused_template.html`; `Review Aids/Draft Window Templates/Option-F-wide-orientation-lanes/option-f_desktop_template.html`
Demonstrates: `A possible USER-configurable layout arrangement pattern for parent-window/card ordering: a wide summary/action zone, horizontal domain lanes, and deterministic visible order/numbering if a later approved customization model allows card movement. Example only: if USER moves Card 4 into Card 2 position, the future arrangement model must deterministically reconcile visible order and numbering so the moved card becomes Card 2 and displaced/downstream cards renumber/reorder according to the approved policy.`
Future Surfaces: `AI Dashboard; HUD Dashboard; future parent windows; Global Settings parent-window customization controls if later approved.`
Future Owners Before Implementation: `{OPTION_F_FUTURE_OWNER_ROUTE}`
Proof Boundary: `Option F is visual/template candidate only. {OPTION_F_NON_APPROVALS}.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This row preserves branch-local evidence and owner routing only. It does not mutate runtime UI, create a reusable/global template, mutate Governance/FAM-002/UIREF/FAM-003/FAM-006/sibling worktrees, approve H1/LV, USER UTS, PR Readiness, PR creation, merge, release, issue mutation, provider/model/private/cache/memory/download/packaging, imports, or v1.8.0 work.`
"""
    row_028 = f"""## F7-UDL-028 Option D Primary Target Refinement / Option F Boundary Preservation - 2026-06-24

Status: `CLOSED_WITH_PROOF`
Finding: `The USER clarified that Option D is the primary current-behavior-aligned direction and that Option E may contribute selective polish, while Option F must remain future layout-arrangement evidence only. A packet that recommends Option E first or lets Option F read as a current selectable target can misroute the visual decision and blur current FAM-007 scope.`
Required Disposition: `Create a new refined current-cycle candidate that is primarily Option D behavior and row grammar, selectively borrows compatible Option E production-window maturity, rejects Option E Settings-card scope broadening, preserves Option F as future-only, and remains real rendered draft-window/template evidence rather than runtime UI implementation proof.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now generates OPTION-G as the recommended D-primary/E-polish target basis, renders it through the branch-local HTML/CSS + PySide6 QWebEngine draft-window path, annotates G-STATUS-01, G-CARD-01, G-ROW-02B, and G-BTN-03, updates the primary USER review and review aids to make Option G the recommendation, and preserves Option F only in future-layout candidate/support context.`
Proof: `Current Visual Acceptance Target packet validation fails if Option G, VAT-CYCLE-20260624-03, D-primary/E-polish wording, Option F future-only wording, Option G annotation IDs, Option G render media, or Option G template artifacts are missing from the generated folder or final ZIP.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair does not mutate runtime UI, create a reusable/global template, mutate Governance/FAM-002/UIREF/FAM-003/FAM-006/sibling worktrees, approve active settings/customization behavior, approve persistence/schema/drag/drop, approve H1/LV, USER UTS, PR Readiness, PR creation, merge, release, issue mutation, provider/model/private/cache/memory/download/packaging, imports, or v1.8.0 work.`
"""
    if "## F7-UDL-019 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-019 .+?(?=\n## |\Z)",
            lambda _match: row_019,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_019
    if "## F7-UDL-021 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-021 .+?(?=\n## |\Z)",
            lambda _match: row_021,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_021
    if "## F7-UDL-022 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-022 .+?(?=\n## |\Z)",
            lambda _match: row_022,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_022
    if "## F7-UDL-023 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-023 .+?(?=\n## |\Z)",
            lambda _match: row_023,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_023
    if "## F7-UDL-024 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-024 .+?(?=\n## |\Z)",
            lambda _match: row_024,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_024
    if "## F7-UDL-025 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-025 .+?(?=\n## |\Z)",
            lambda _match: row_025,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_025
    if "## F7-UDL-026 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-026 .+?(?=\n## |\Z)",
            lambda _match: row_026,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_026
    if "## F7-UDL-027 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-027 .+?(?=\n## |\Z)",
            lambda _match: row_027,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_027
    if "## F7-UDL-028 " in udl_text:
        udl_text = re.sub(
            r"## F7-UDL-028 .+?(?=\n## |\Z)",
            lambda _match: row_028,
            udl_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        udl_text = udl_text.rstrip() + "\n\n" + row_028
    return udl_text


def _update_external_state(zip_path: Path) -> None:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    head = _git_value("rev-parse", "HEAD")
    origin_main = _git_value("rev-parse", "origin/main")
    for path in (BRANCH_STATE, BRANCH_PLAN):
        text = _read_text(path)
        text = _update_field(text, "Last Updated", now)
        text = _update_field(text, "Source Repo HEAD", head)
        text = _update_field(text, "Source origin/main", origin_main)
        text = _update_field(text, "USER Review ZIP", str(zip_path))
        if path == BRANCH_STATE:
            text = _update_branch_state_for_visual_packet(text, zip_path)
        if path == BRANCH_PLAN:
            text = _update_branch_plan_for_visual_packet(text, zip_path)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        _remove_stale_packet_sprawl_receipts(path)
        _append_receipt(
            path,
            f"## Branch-Local Visual Acceptance Target Packet Receipt - {now}",
            [
                "Receipt Status: `VISUAL_ACCEPTANCE_TARGET_PACKET_GENERATED_PENDING_USER_REVIEW`",
                f"USER Review ZIP: `{zip_path}`",
                "Standalone Historical Packet: `Not retained as a second root USER packet ZIP; historical context remains in external state and copied Source Truth Context only.`",
                f"Packet Purpose: `{VISUAL_PACKET_PURPOSE}`",
                "UI/UX Workstream Exit Acceptance Gate: `Governance candidate recorded only; global phase-governance law was not mutated by this FAM-007 pass.`",
                "Visual Acceptance Exploration Loop: `Branch-local rule recorded: clean enough is not acceptance, packet validation is not USER preference, rejected targets require materially different new/revised/combined real draft-window variants with retained/rejected traits and no near-duplicate label-only changes.`",
                "Real Draft Window Template Repair: `Options B through G are rendered from branch-local HTML/CSS draft-window templates through PySide6 QWebEngine; Option A remains actual runtime baseline; annotation overlays are review aids only.`",
                "Option G Current-Cycle Recommendation: `Recommended refined D/E target basis: Option D behavior and row grammar first, selective Option E visual maturity second, no Option E Settings-card scope broadening, and no Option F layout-customization behavior.`",
                f"Option F Future Layout Arrangement Candidate: `Branch-local future candidate/example only from seed packet {OPTION_F_SEED_PACKET_PATH} sha256 {OPTION_F_SEED_PACKET_SHA256}; {OPTION_F_NON_APPROVALS}; future owner route is {OPTION_F_FUTURE_OWNER_ROUTE}.`",
                "Implementation Status: `No product/runtime UI implementation authorized or performed by this packet.`",
                f"Blocked Gates: `{BLOCKED_GATES}`",
            ],
        )
    if UDL_PATH.exists():
        udl_text = _read_text(UDL_PATH)
        udl_text = re.sub(
            r"^Current HEAD: `.*?`$",
            f"Current HEAD: `{head}`",
            udl_text,
            count=1,
            flags=re.MULTILINE,
        )
        classification = (
            "Current HEAD Field Classification: `Active current packet metadata; refreshed "
            "during Visual Acceptance Target packet regeneration so copied Source Truth "
            "Context cannot be mistaken for stale proof-snapshot truth.`"
        )
        if "Current HEAD Field Classification:" not in udl_text:
            udl_text = udl_text.replace(f"Current HEAD: `{head}`", f"Current HEAD: `{head}`\n{classification}", 1)
        else:
            udl_text = re.sub(
                r"^Current HEAD Field Classification: `.*?`$",
                classification,
                udl_text,
                count=1,
                flags=re.MULTILINE,
            )
        udl_text = _mark_udl_018_restored(udl_text, zip_path)
        udl_text = _update_visual_packet_udl_rows(udl_text, zip_path)
        UDL_PATH.write_text(udl_text.rstrip() + "\n", encoding="utf-8")


def _update_external_state_for_recovery_packet(zip_path: Path) -> None:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    head = _git_value("rev-parse", "HEAD")
    origin_main = _git_value("rev-parse", "origin/main")
    for path in (BRANCH_STATE, BRANCH_PLAN):
        text = _read_text(path)
        text = _update_field(text, "Last Updated", now)
        text = _update_field(text, "Source Repo HEAD", head)
        text = _update_field(text, "Source origin/main", origin_main)
        text = _update_field(text, "USER Review ZIP", str(zip_path))
        if path == BRANCH_STATE:
            text = _update_branch_state_for_recovery_packet(text, zip_path)
        if path == BRANCH_PLAN:
            text = _update_branch_plan_for_recovery_packet(text, zip_path)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        _append_receipt(
            path,
            f"## Accepted-Historical Packet Recovery / Retention Blocker Receipt - {now}",
            [
                "Receipt Status: `ACCEPTED_HISTORICAL_PACKET_MISSING_BLOCKER_PACKET_GENERATED_PENDING_USER_REVIEW`",
                f"USER Review ZIP: `{zip_path}`",
                f"Missing Accepted Historical Packet: `{ACCEPTED_HISTORICAL_ZIP}`",
                "Recovery Result: `NOT RECOVERED - do not fake preservation or convert missing historical artifact into PASS.`",
                "Packet Purpose: `USER decision packet for accepted-historical artifact recovery, retention waiver, or blocked-chain disposition.`",
                f"Blocked Gates: `{BLOCKED_GATES}`",
            ],
        )
    if UDL_PATH.exists():
        udl_text = _read_text(UDL_PATH)
        udl_text = re.sub(
            r"^Current HEAD: `.*?`$",
            f"Current HEAD: `{head}`",
            udl_text,
            count=1,
            flags=re.MULTILINE,
        )
        classification = (
            "Current HEAD Field Classification: `Active current packet metadata; refreshed "
            "during accepted-historical recovery blocker packet regeneration so copied "
            "Source Truth Context cannot be mistaken for stale proof-snapshot truth.`"
        )
        if "Current HEAD Field Classification:" not in udl_text:
            udl_text = udl_text.replace(f"Current HEAD: `{head}`", f"Current HEAD: `{head}`\n{classification}", 1)
        else:
            udl_text = re.sub(
                r"^Current HEAD Field Classification: `.*?`$",
                classification,
                udl_text,
                count=1,
                flags=re.MULTILINE,
            )
        if "F7-UDL-018" not in udl_text:
            udl_text += (
                "\n\n## F7-UDL-018 Accepted-Historical Artifact Missing - 2026-06-24\n\n"
                "Status: `BLOCKED_SOURCE_TRUTH`\n"
                f"Missing Artifact: `{ACCEPTED_HISTORICAL_ZIP}`\n"
                "Finding: `The accepted historical Workstream implementation / H1-LV proof packet is not present in the retained local USER packet root, Recycle Bin, known local workspaces, user profile roots, OneDrive roots, Downloads/Documents/Desktop, artifact roots, or Codex attachment cache searched by this recovery pass.`\n"
                "Required Disposition: `USER must provide/upload the missing ZIP, approve an explicit retention waiver, or keep the packet chain blocked until recovered.`\n"
                "No-Fake-Preservation Rule: `Do not recreate the accepted historical packet or claim it is preserved without the original artifact bytes or an explicit USER waiver/source-truth disposition.`\n"
                f"Current Recovery Packet: `{zip_path}`\n"
            )
        else:
            udl_text = re.sub(
                r"^Current Recovery Packet: `.*?`$",
                lambda _match: f"Current Recovery Packet: `{zip_path}`",
                udl_text,
                flags=re.MULTILINE,
            )
        UDL_PATH.write_text(udl_text.rstrip() + "\n", encoding="utf-8")


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (Path(r"C:\Windows\Fonts\segoeui.ttf"), Path(r"C:\Windows\Fonts\arial.ttf")):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def _draw_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    *,
    number: str = "01",
    action: str = "Open Surface",
) -> None:
    draw.rounded_rectangle(box, radius=18, fill=(5, 24, 38), outline=(66, 185, 210), width=2)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 58, y1 + 52), radius=12, fill=(8, 54, 74), outline=(76, 214, 234))
    draw.text((x1 + 27, y1 + 25), number, fill=(158, 240, 237), font=_font(11))
    draw.text((x1 + 74, y1 + 19), title.upper(), fill=(235, 248, 252), font=_font(18))
    yy = y1 + 56
    for line in lines:
        draw.text((x1 + 74, yy), line, fill=(158, 205, 213), font=_font(13))
        yy += 23
    button_y = y2 - 50
    action_font = _font(11)
    button_width = max(142, _text_width(draw, action.upper(), action_font) + 36)
    draw.rounded_rectangle((x2 - button_width - 24, button_y, x2 - 24, button_y + 30), radius=15, fill=(7, 34, 49), outline=(61, 168, 198), width=2)
    draw.text((x2 - button_width - 6, button_y + 8), action.upper(), fill=(226, 245, 249), font=action_font)


ANNOTATION_COLOR_PALETTE = [
    ("cyan", (80, 218, 238)),
    ("yellow", (236, 202, 89)),
    ("magenta", (230, 112, 225)),
    ("green", (92, 220, 156)),
    ("amber", (242, 166, 80)),
    ("blue", (105, 164, 255)),
    ("mint", (120, 234, 206)),
    ("white", (232, 246, 249)),
]

ANNOTATION_LABEL_PANEL_WIDTH = 360
ANNOTATION_LABEL_BOX_WIDTH = 304
ANNOTATION_LABEL_BOX_HEIGHT = 28


def _option_letter(option_id: str) -> str:
    return option_id.split("-")[-1]


def _clip_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return (
        max(0, min(width - 2, x1)),
        max(0, min(height - 2, y1)),
        max(1, min(width, x2)),
        max(1, min(height, y2)),
    )


def _offset_box(box: tuple[int, int, int, int], x: int, y: int) -> tuple[int, int, int, int]:
    return (box[0] + x, box[1] + y, box[2] + x, box[3] + y)


def _window_geometry(option_id: str, width: int, height: int, *, desktop: bool) -> tuple[int, int, int, int]:
    if option_id == "OPTION-A":
        if desktop:
            return (2670, 78, 560, 560)
        return (0, 0, 570, 610)
    if option_id == "OPTION-D":
        return (810, 58, 748, 722) if desktop else (36, 36, 748, 722)
    if option_id == "OPTION-E":
        return (760, 54, 820, 728) if desktop else (34, 34, 820, 728)
    if option_id == "OPTION-F":
        return (700, 82, 910, 620) if desktop else (34, 34, 910, 620)
    if option_id == "OPTION-G":
        return (740, 52, 840, 752) if desktop else (32, 32, 840, 752)
    return (850, 82, 650, 660) if desktop else (48, 48, 650, 660)


def _annotation_spec(
    option_id: str,
    suffix: str,
    element_type: str,
    target_label: str,
    region: tuple[int, int, int, int],
    marker_style: str,
    color_index: int,
    purpose: str,
) -> AnnotationSpec:
    color_name, color = ANNOTATION_COLOR_PALETTE[color_index % len(ANNOTATION_COLOR_PALETTE)]
    return AnnotationSpec(
        option_id=option_id,
        annotation_id=f"{_option_letter(option_id)}-{suffix}",
        element_type=element_type,
        target_label=target_label,
        region=region,
        marker_style=marker_style,
        color_name=color_name,
        color=color,
        non_color_cue=f"text ID plus {marker_style} marker plus leader line",
        purpose=purpose,
    )


def _generic_option_specs(option_id: str, width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    x, y, win_w, win_h = _window_geometry(option_id, width, height, desktop=desktop)
    specs = [
        ("HEADER-01", "group", "Title/header group", (x + 26, y + 24, x + win_w - 26, y + 128), "bracket", 2, "Identifies the title, subtitle, and top visual hierarchy."),
        ("CTRL-01", "element", "Window control cluster", (x + win_w - 128, y + 38, x + win_w - 46, y + 68), "circle", 1, "Identifies compact window-level controls."),
        ("CARD-01", "group", "AI Control Center card", (x + 34, y + 186, x + win_w - 34, y + 332), "box", 0, "Identifies the first doorway/card group."),
        ("BTN-01", "element", "Open Control Center action", (x + win_w - 224, y + 284, x + win_w - 58, y + 314), "arrow", 4, "Identifies the button/action in the first card."),
        ("CARD-02", "group", "Readiness & Diagnostics card", (x + 34, y + 350, x + win_w - 34, y + 496), "box", 3, "Identifies the second doorway/card group."),
        ("BTN-02", "element", "Open Diagnostics action", (x + win_w - 224, y + 448, x + win_w - 58, y + 478), "arrow", 5, "Identifies the button/action in the second card."),
        ("CARD-03", "group", "Capabilities & Maintenance card", (x + 34, y + 514, x + win_w - 34, y + 660), "box", 6, "Identifies the third card/status group."),
        ("BTN-03", "element", "Open Capabilities action", (x + win_w - 224, y + 612, x + win_w - 58, y + 642), "arrow", 7, "Identifies the button/action in the third card."),
    ]
    return [
        _annotation_spec(option_id, suffix, element_type, label, _clip_box(region, width, height), style, color_index, purpose)
        for suffix, element_type, label, region, style, color_index, purpose in specs
    ]


def _option_a_specs(width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    x, y, _win_w, _win_h = _window_geometry("OPTION-A", width, height, desktop=desktop)
    base_specs = [
        ("HEADER-01", "group", "AI Dashboard header", (14, 14, 555, 154), "bracket", 2, "Identifies the current implementation title/header group."),
        ("CTRL-01", "element", "Window control cluster", (493, 16, 553, 46), "circle", 1, "Identifies the current implementation window controls."),
        ("STATUS-01", "group", "Global AI status strip", (25, 108, 381, 140), "bracket", 5, "Identifies the compact AI / status / provider strip."),
        ("CARD-01", "group", "Control Center card", (24, 172, 538, 306), "box", 0, "Identifies the current Control Center doorway card."),
        ("BTN-01", "element", "Open Control Center button", (355, 264, 528, 296), "arrow", 4, "Identifies the first doorway open action."),
        ("CARD-02", "group", "Diagnostics card", (24, 312, 538, 445), "box", 3, "Identifies the current Diagnostics doorway card."),
        ("BTN-02", "element", "Open Diagnostics button", (382, 404, 528, 436), "arrow", 5, "Identifies the second doorway open action."),
        ("CARD-03", "group", "Capabilities card", (24, 453, 538, 586), "box", 6, "Identifies the current Capabilities doorway card."),
        ("BTN-03", "element", "Open Capabilities button", (381, 546, 528, 577), "arrow", 7, "Identifies the third doorway open action."),
        ("SCROLL-01", "element", "Scrollable content rail", (543, 172, 554, 577), "bracket", 1, "Identifies the scrollbar/overflow affordance."),
    ]
    return [
        _annotation_spec("OPTION-A", suffix, element_type, label, _clip_box(_offset_box(region, x, y), width, height), style, color_index, purpose)
        for suffix, element_type, label, region, style, color_index, purpose in base_specs
    ]


def _option_d_specs(width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    x, y, win_w, _win_h = _window_geometry("OPTION-D", width, height, desktop=desktop)
    card_x1 = x + 28
    card_x2 = x + win_w - 28
    specs = [
        ("HEADER-01", "group", "AI Dashboard header", (x + 18, y + 18, x + win_w - 18, y + 164), "bracket", 2, "Identifies the hybrid target title/header group."),
        ("CTRL-01", "element", "Window control cluster", (x + win_w - 92, y + 28, x + win_w - 28, y + 62), "circle", 1, "Identifies compact window-level controls."),
        ("STATUS-01", "group", "AI / ORIN status strip", (x + 42, y + 122, x + 460, y + 158), "bracket", 5, "Identifies the compact AI / ORIN / provider strip."),
        ("CARD-01", "group", "AI Status & Trust card", (card_x1, y + 184, card_x2, y + 354), "box", 0, "Identifies the first grouped doorway card."),
        ("ROW-01A", "element", "AI state row", (card_x1 + 22, y + 253, card_x2 - 22, y + 276), "bracket", 6, "Identifies row 1 in card 01."),
        ("ROW-01B", "element", "Provider row", (card_x1 + 22, y + 280, card_x2 - 22, y + 303), "bracket", 6, "Identifies row 2 in card 01."),
        ("ROW-01C", "element", "Visible data row", (card_x1 + 22, y + 307, card_x2 - 22, y + 330), "bracket", 6, "Identifies row 3 in card 01."),
        ("BTN-01", "element", "Open Control Center button", (card_x2 - 188, y + 312, card_x2 - 20, y + 342), "arrow", 4, "Identifies the first doorway open action."),
        ("CARD-02", "group", "Readiness & Diagnostics card", (card_x1, y + 370, card_x2, y + 540), "box", 3, "Identifies the second grouped doorway card."),
        ("ROW-02A", "element", "Local check row", (card_x1 + 22, y + 439, card_x2 - 22, y + 462), "bracket", 6, "Identifies row 1 in card 02."),
        ("ROW-02B", "element", "Report row", (card_x1 + 22, y + 466, card_x2 - 22, y + 489), "bracket", 6, "Identifies row 2 in card 02."),
        ("ROW-02C", "element", "Prompt/data row", (card_x1 + 22, y + 493, card_x2 - 22, y + 516), "bracket", 6, "Identifies row 3 in card 02."),
        ("BTN-02", "element", "Open Diagnostics button", (card_x2 - 164, y + 498, card_x2 - 20, y + 528), "arrow", 5, "Identifies the second doorway open action."),
        ("CARD-03", "group", "Capabilities & Maintenance card", (card_x1, y + 556, card_x2, y + 704), "box", 7, "Identifies the third grouped doorway card."),
        ("ROW-03A", "element", "Capability packs row", (card_x1 + 22, y + 625, card_x2 - 22, y + 648), "bracket", 6, "Identifies row 1 in card 03."),
        ("ROW-03B", "element", "Updates row", (card_x1 + 22, y + 652, card_x2 - 22, y + 675), "bracket", 6, "Identifies row 2 in card 03."),
        ("BTN-03", "element", "Open Capabilities button", (card_x2 - 168, y + 662, card_x2 - 20, y + 692), "arrow", 4, "Identifies the third doorway open action."),
    ]
    return [
        _annotation_spec("OPTION-D", suffix, element_type, label, _clip_box(region, width, height), style, color_index, purpose)
        for suffix, element_type, label, region, style, color_index, purpose in specs
    ]


def _option_e_specs(width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    x, y, win_w, _win_h = _window_geometry("OPTION-E", width, height, desktop=desktop)
    left_x1 = x + 30
    left_x2 = x + 418
    right_x1 = x + 436
    right_x2 = x + win_w - 30
    specs = [
        ("HEADER-01", "group", "Production doorway header", (x + 18, y + 18, x + win_w - 18, y + 150), "bracket", 2, "Identifies the polished title/header group and trust summary."),
        ("CTRL-01", "element", "Window control cluster", (x + win_w - 92, y + 28, x + win_w - 28, y + 62), "circle", 1, "Identifies compact window-level controls."),
        ("STATUS-01", "group", "AI trust status strip", (x + 42, y + 112, x + 538, y + 146), "bracket", 5, "Identifies compact ORIN/provider/data truth."),
        ("CARD-01", "group", "AI Control Center doorway", (left_x1, y + 174, left_x2, y + 380), "box", 0, "Identifies the main focused control domain doorway."),
        ("ROW-01A", "element", "AI state row", (left_x1 + 20, y + 252, left_x2 - 20, y + 275), "bracket", 6, "Identifies control-center AI truth row."),
        ("ROW-01B", "element", "Provider boundary row", (left_x1 + 20, y + 280, left_x2 - 20, y + 303), "bracket", 6, "Identifies provider/model blocked truth row."),
        ("BTN-01", "element", "Open Control Center button", (left_x2 - 182, y + 336, left_x2 - 20, y + 368), "arrow", 4, "Identifies primary focused-domain action."),
        ("CARD-02", "group", "Readiness & Diagnostics doorway", (right_x1, y + 174, right_x2, y + 380), "box", 3, "Identifies diagnostics/readiness domain doorway."),
        ("ROW-02A", "element", "Local check row", (right_x1 + 20, y + 252, right_x2 - 20, y + 275), "bracket", 6, "Identifies local check state."),
        ("ROW-02B", "element", "Report doorway row", (right_x1 + 20, y + 280, right_x2 - 20, y + 303), "bracket", 6, "Identifies readiness report placement."),
        ("BTN-02", "element", "Open Diagnostics button", (right_x2 - 158, y + 336, right_x2 - 20, y + 368), "arrow", 5, "Identifies diagnostics domain action."),
        ("CARD-03", "group", "Capabilities doorway", (left_x1, y + 400, left_x2, y + 624), "box", 7, "Identifies capability/maintenance doorway."),
        ("ROW-03A", "element", "Capability pack row", (left_x1 + 20, y + 486, left_x2 - 20, y + 509), "bracket", 6, "Identifies blocked capability-pack state."),
        ("BTN-03", "element", "Open Capabilities button", (left_x2 - 164, y + 580, left_x2 - 20, y + 612), "arrow", 4, "Identifies capability domain action."),
        ("CARD-04", "group", "Activity and settings handoff card", (right_x1, y + 400, right_x2, y + 624), "box", 7, "Identifies compact future-gated activity/settings doorway."),
        ("ROW-04A", "element", "Settings handoff row", (right_x1 + 20, y + 486, right_x2 - 20, y + 509), "bracket", 6, "Identifies FAM-003 settings route without mutation."),
        ("BTN-04", "element", "Open Settings handoff button", (right_x2 - 142, y + 580, right_x2 - 20, y + 612), "arrow", 5, "Identifies future-gated settings action."),
    ]
    return [
        _annotation_spec("OPTION-E", suffix, element_type, label, _clip_box(region, width, height), style, color_index, purpose)
        for suffix, element_type, label, region, style, color_index, purpose in specs
    ]


def _option_f_specs(width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    x, y, win_w, _win_h = _window_geometry("OPTION-F", width, height, desktop=desktop)
    card_y1 = y + 320
    card_y2 = y + 540
    card_w = 268
    specs = [
        ("HEADER-01", "group", "Wide orientation header", (x + 18, y + 18, x + win_w - 18, y + 138), "bracket", 2, "Identifies wide title/header hierarchy."),
        ("CTRL-01", "element", "Window control cluster", (x + win_w - 92, y + 28, x + win_w - 28, y + 62), "circle", 1, "Identifies compact window-level controls."),
        ("SUMMARY-01", "group", "Top summary and state zone", (x + 30, y + 160, x + win_w - 30, y + 294), "box", 0, "Identifies the alternate strong top summary zone."),
        ("STATUS-01", "group", "AI/provider/data status row", (x + 52, y + 246, x + 560, y + 282), "bracket", 5, "Identifies compact trust-state row in the top zone."),
        ("BTN-00", "element", "Primary Diagnostics action", (x + win_w - 238, y + 238, x + win_w - 52, y + 274), "arrow", 4, "Identifies primary action placement in the summary zone."),
        ("CARD-01", "group", "Control Center lane", (x + 30, card_y1, x + 30 + card_w, card_y2), "box", 3, "Identifies first horizontal domain lane."),
        ("ROW-01A", "element", "Control summary row", (x + 50, card_y1 + 96, x + 30 + card_w - 20, card_y1 + 119), "bracket", 6, "Identifies control lane state row."),
        ("BTN-01", "element", "Open Control action", (x + 30 + card_w - 156, card_y2 - 44, x + 30 + card_w - 20, card_y2 - 12), "arrow", 4, "Identifies first lane action."),
        ("CARD-02", "group", "Diagnostics lane", (x + 322, card_y1, x + 322 + card_w, card_y2), "box", 7, "Identifies second horizontal domain lane."),
        ("ROW-02A", "element", "Diagnostics summary row", (x + 342, card_y1 + 96, x + 322 + card_w - 20, card_y1 + 119), "bracket", 6, "Identifies diagnostics lane state row."),
        ("BTN-02", "element", "Open Diagnostics action", (x + 322 + card_w - 150, card_y2 - 44, x + 322 + card_w - 20, card_y2 - 12), "arrow", 5, "Identifies second lane action."),
        ("CARD-03", "group", "Capabilities lane", (x + 614, card_y1, x + 614 + card_w, card_y2), "box", 7, "Identifies third horizontal domain lane."),
        ("ROW-03A", "element", "Capability summary row", (x + 634, card_y1 + 96, x + 614 + card_w - 20, card_y1 + 119), "bracket", 6, "Identifies capability lane state row."),
        ("BTN-03", "element", "Open Capabilities action", (x + 614 + card_w - 150, card_y2 - 44, x + 614 + card_w - 20, card_y2 - 12), "arrow", 4, "Identifies third lane action."),
    ]
    return [
        _annotation_spec("OPTION-F", suffix, element_type, label, _clip_box(region, width, height), style, color_index, purpose)
        for suffix, element_type, label, region, style, color_index, purpose in specs
    ]


def _option_g_specs(width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    x, y, win_w, _win_h = _window_geometry("OPTION-G", width, height, desktop=desktop)
    card_x1 = x + 30
    card_x2 = x + win_w - 30
    specs = [
        ("HEADER-01", "group", "D/E hybrid target header", (x + 18, y + 18, x + win_w - 18, y + 162), "bracket", 2, "Identifies the polished header retained from D/E without changing product scope."),
        ("CTRL-01", "element", "Window control cluster", (x + win_w - 92, y + 28, x + win_w - 28, y + 62), "circle", 1, "Identifies compact window-level controls."),
        ("STATUS-01", "group", "Compact trust status strip", (x + 42, y + 120, x + 588, y + 156), "bracket", 5, "Identifies compact AI / provider / data truth retained from Option D and polished like Option E."),
        ("CARD-01", "group", "AI Status & Trust doorway", (card_x1, y + 184, card_x2, y + 354), "box", 0, "Identifies the first grouped doorway card."),
        ("ROW-01A", "element", "AI state row", (card_x1 + 22, y + 253, card_x2 - 22, y + 276), "bracket", 6, "Identifies row 1 in card 01."),
        ("ROW-01B", "element", "Provider boundary row", (card_x1 + 22, y + 280, card_x2 - 22, y + 303), "bracket", 6, "Identifies row 2 in card 01."),
        ("ROW-01C", "element", "Visible data row", (card_x1 + 22, y + 307, card_x2 - 22, y + 330), "bracket", 6, "Identifies row 3 in card 01."),
        ("BTN-01", "element", "Open Control Center button", (card_x2 - 188, y + 312, card_x2 - 20, y + 342), "arrow", 4, "Identifies the first doorway open action."),
        ("CARD-02", "group", "AI Readiness & Diagnostics doorway", (card_x1, y + 370, card_x2, y + 540), "box", 3, "Identifies the second grouped doorway card."),
        ("ROW-02A", "element", "Local check row", (card_x1 + 22, y + 439, card_x2 - 22, y + 462), "bracket", 6, "Identifies row 1 in card 02."),
        ("ROW-02B", "element", "Readiness report row", (card_x1 + 22, y + 466, card_x2 - 22, y + 489), "bracket", 6, "Identifies readiness report placement behind diagnostics/readiness."),
        ("ROW-02C", "element", "Prompt/data row", (card_x1 + 22, y + 493, card_x2 - 22, y + 516), "bracket", 6, "Identifies row 3 in card 02."),
        ("BTN-02", "element", "Open Diagnostics button", (card_x2 - 164, y + 498, card_x2 - 20, y + 528), "arrow", 5, "Identifies the second doorway open action."),
        ("CARD-03", "group", "Capabilities & Maintenance doorway", (card_x1, y + 556, card_x2, y + 706), "box", 7, "Identifies the third grouped doorway card without promoting active downloads/settings."),
        ("ROW-03A", "element", "Capability packs row", (card_x1 + 22, y + 625, card_x2 - 22, y + 648), "bracket", 6, "Identifies blocked capability-pack state."),
        ("ROW-03B", "element", "Downloads and updates row", (card_x1 + 22, y + 652, card_x2 - 22, y + 675), "bracket", 6, "Identifies disabled/future-gated maintenance state."),
        ("BTN-03", "element", "Open Capabilities button", (card_x2 - 168, y + 664, card_x2 - 20, y + 694), "arrow", 4, "Identifies the third doorway open action."),
    ]
    return [
        _annotation_spec("OPTION-G", suffix, element_type, label, _clip_box(region, width, height), style, color_index, purpose)
        for suffix, element_type, label, region, style, color_index, purpose in specs
    ]


def _annotation_specs(option_id: str, width: int, height: int, *, desktop: bool) -> list[AnnotationSpec]:
    if option_id == "OPTION-A":
        return _option_a_specs(width, height, desktop=desktop)
    if option_id == "OPTION-D":
        return _option_d_specs(width, height, desktop=desktop)
    if option_id == "OPTION-E":
        return _option_e_specs(width, height, desktop=desktop)
    if option_id == "OPTION-F":
        return _option_f_specs(width, height, desktop=desktop)
    if option_id == "OPTION-G":
        return _option_g_specs(width, height, desktop=desktop)
    return _generic_option_specs(option_id, width, height, desktop=desktop)


def _callout_geometry(target: tuple[int, int, int, int], index: int, canvas_width: int) -> dict[str, tuple[int, ...]]:
    x1, y1, x2, y2 = target
    label_x = canvas_width - ANNOTATION_LABEL_PANEL_WIDTH + 18
    label_y = 58 + (index - 1) * 42
    label_box = (
        label_x,
        label_y,
        label_x + ANNOTATION_LABEL_BOX_WIDTH,
        label_y + ANNOTATION_LABEL_BOX_HEIGHT,
    )
    anchor_x = x2 if x2 < label_x else x1
    anchor_y = y1 + max(16, min(44, (y2 - y1) // 3))
    line = (anchor_x, anchor_y, label_x, label_y + ANNOTATION_LABEL_BOX_HEIGHT // 2)
    return {"label_box": label_box, "leader_line": line}


def _draw_callout(
    draw: ImageDraw.ImageDraw,
    label: str,
    target: tuple[int, int, int, int],
    index: int,
    *,
    color: tuple[int, int, int],
    shape: str,
    canvas_width: int,
) -> dict[str, tuple[int, ...]]:
    x1, y1, x2, y2 = target
    if shape == "circle":
        draw.ellipse(target, outline=color, width=3)
    elif shape == "bracket":
        draw.line((x1, y1, x1, y2), fill=color, width=3)
        draw.line((x1, y1, min(x1 + 28, x2), y1), fill=color, width=3)
        draw.line((x1, y2, min(x1 + 28, x2), y2), fill=color, width=3)
    elif shape == "arrow":
        draw.rounded_rectangle(target, radius=12, outline=color, width=3)
        draw.polygon([(x1 - 8, y1 + (y2 - y1) // 2), (x1 + 8, y1 + 5), (x1 + 8, y2 - 5)], fill=color)
    else:
        draw.rounded_rectangle(target, radius=12, outline=color, width=3)
    geometry = _callout_geometry(target, index, canvas_width)
    label_box = geometry["label_box"]
    leader_line = geometry["leader_line"]
    label_x, label_y, _, _ = label_box
    draw.line(leader_line, fill=color, width=2)
    draw.rounded_rectangle(label_box, radius=8, fill=(1, 14, 23), outline=color, width=2)
    if shape == "circle":
        draw.ellipse((label_x + 7, label_y + 7, label_x + 21, label_y + 21), outline=color, width=2)
    elif shape == "bracket":
        draw.line((label_x + 8, label_y + 7, label_x + 8, label_y + 21), fill=color, width=2)
        draw.line((label_x + 8, label_y + 7, label_x + 20, label_y + 7), fill=color, width=2)
        draw.line((label_x + 8, label_y + 21, label_x + 20, label_y + 21), fill=color, width=2)
    elif shape == "arrow":
        draw.polygon([(label_x + 8, label_y + 14), (label_x + 22, label_y + 7), (label_x + 22, label_y + 21)], fill=color)
    else:
        draw.rectangle((label_x + 7, label_y + 7, label_x + 21, label_y + 21), outline=color, width=2)
    draw.text((label_x + 28, label_y + 7), label, fill=(238, 248, 252), font=_font(10))
    return geometry


def _annotate_render(source: Path, target: Path, option_id: str, *, desktop: bool) -> list[dict[str, str]]:
    with Image.open(source) as image:
        base = image.convert("RGB")
    annotated = Image.new("RGB", (base.width + ANNOTATION_LABEL_PANEL_WIDTH, base.height), (0, 5, 8))
    annotated.paste(base, (0, 0))
    draw = ImageDraw.Draw(annotated)
    panel_x = base.width
    draw.rectangle((panel_x, 0, annotated.width, annotated.height), fill=(2, 16, 25))
    draw.line((panel_x, 0, panel_x, annotated.height), fill=(59, 161, 190), width=2)
    draw.text((panel_x + 20, 22), "ANNOTATION KEY", fill=(104, 225, 239), font=_font(13))
    draw.text((panel_x + 20, 40), "Use IDs in feedback", fill=(158, 205, 213), font=_font(11))
    specs = _annotation_specs(option_id, base.width, base.height, desktop=desktop)
    rows: list[dict[str, str]] = []
    for index, spec in enumerate(specs, start=1):
        geometry = _draw_callout(draw, spec.annotation_id, spec.region, index, color=spec.color, shape=spec.marker_style, canvas_width=annotated.width)
        rows.append(
            {
                "option": spec.option_id,
                "annotation": spec.annotation_id,
                "element_type": spec.element_type,
                "target_label": spec.target_label,
                "region": f"{spec.region[0]},{spec.region[1]},{spec.region[2]},{spec.region[3]}",
                "marker_style": spec.marker_style,
                "color_cue": spec.color_name,
                "non_color_cue": spec.non_color_cue,
                "label_box": ",".join(str(value) for value in geometry["label_box"]),
                "leader_line": ",".join(str(value) for value in geometry["leader_line"]),
                "purpose": spec.purpose,
                "file": str(target.relative_to(PACKET_DIR)).replace("\\", "/"),
            }
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    annotated.save(target)
    return rows


def _draw_option_mockup(path: Path, option: str, title: str, subtitle: str, desktop: bool) -> None:
    width, height = (1600, 900) if desktop else (760, 760)
    img = Image.new("RGB", (width, height), (0, 5, 8))
    draw = ImageDraw.Draw(img)
    for radius in range(120, 470, 70):
        draw.ellipse((160 - radius, 380 - radius, 160 + radius, 380 + radius), outline=(7, 43, 56), width=1)
    win_w, win_h = 650, 660
    x = 850 if desktop else 48
    y = 82 if desktop else 48
    draw.rounded_rectangle((x + 6, y + 8, x + win_w + 6, y + win_h + 8), radius=29, fill=(0, 12, 18))
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=28, fill=(2, 14, 25), outline=(65, 183, 214), width=2)
    header_fill = (3, 18, 31) if option == "OPTION-B" else (5, 20, 33)
    draw.rounded_rectangle((x + 26, y + 24, x + win_w - 26, y + 128), radius=24, fill=header_fill, outline=(25, 96, 119), width=1)
    draw.text((x + 48, y + 42), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 48, y + 66), title, fill=(238, 248, 252), font=_font(29))
    draw.text((x + 48, y + 106), subtitle, fill=(158, 205, 213), font=_font(13))
    draw.rounded_rectangle((x + win_w - 128, y + 38, x + win_w - 46, y + 68), radius=15, fill=(4, 28, 40), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 102, y + 46), "-  x", fill=(230, 247, 250), font=_font(13))
    _draw_status_strip(draw, x + 42, y + 142, ["AI - ORIN", "PROVIDER - BLOCKED", "DATA - NONE"])
    if option == "OPTION-B":
        cards = [
            ("01", "AI Control Center", ["Trust state and quick orientation.", "Provider blocked; no prompt path active."], "Open Control Center"),
            ("02", "Readiness & Diagnostics", ["Local check and report doorway.", "Detailed evidence opens in its own surface."], "Open Diagnostics"),
            ("03", "Capabilities & Maintenance", ["Capability packs remain blocked.", "Updates are future-gated; no download."], "Open Capabilities"),
        ]
    else:
        cards = [
            ("01", "AI Workspace Panel", ["Risk comparator: this starts to feel like a workspace.", "Useful context, but heavier than the hub should be."], "Open Panel"),
            ("02", "Diagnostics Report Area", ["Risk comparator: more report body appears inline.", "Detail belongs behind a focused child surface."], "Open Diagnostics"),
            ("03", "Maintenance And Capability Detail", ["Risk comparator: maintenance detail consumes top level.", "Keep top-level action compact instead."], "Open Capabilities"),
        ]
    card_boxes = [
        (x + 34, y + 186, x + win_w - 34, y + 332),
        (x + 34, y + 350, x + win_w - 34, y + 496),
        (x + 34, y + 514, x + win_w - 34, y + 660),
    ]
    for card_box, (number, card_title, lines, action) in zip(card_boxes, cards):
        _draw_card(draw, card_box, card_title, lines, number=number, action=action)
    if desktop:
        draw.rectangle((0, height - 62, width, height), fill=(0, 10, 14))
        draw.text((24, height - 42), "Full desktop/context render: monitor-space footprint and surrounding UI relationship", fill=(130, 190, 198), font=_font(15))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def _draw_status_strip(draw: ImageDraw.ImageDraw, x: int, y: int, labels: list[str]) -> None:
    font = _font(11)
    strip_width = 0
    widths = []
    for label in labels:
        width = _text_width(draw, label, font) + 28
        widths.append(width)
        strip_width += width
    draw.rounded_rectangle((x, y, x + strip_width + 12, y + 36), radius=18, fill=(4, 30, 42), outline=(49, 138, 164), width=1)
    xx = x + 14
    for label, width in zip(labels, widths):
        draw.text((xx, y + 12), label, fill=(175, 240, 226), font=font)
        xx += width


def _html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _css_row(label: str, value: str) -> str:
    return (
        '<div class="row">'
        f'<span class="row-label">{_html_escape(label)}</span>'
        f'<span class="row-value">{_html_escape(value)}</span>'
        "</div>"
    )


def _css_card(
    number: str,
    title: str,
    description: str,
    rows: list[tuple[str, str]],
    action: str,
    *,
    left: int,
    top: int,
    width: int,
    height: int,
    compact: bool = False,
) -> str:
    row_html = "\n".join(_css_row(label, value) for label, value in rows)
    return f"""
      <section class="card{' compact' if compact else ''}" style="left:{left}px; top:{top}px; width:{width}px; height:{height}px;">
        <div class="badge">{_html_escape(number)}</div>
        <div class="card-copy">
          <strong>{_html_escape(title)}</strong>
          <span>{_html_escape(description)}</span>
        </div>
        <div class="rows">{row_html}</div>
        <button class="action">{_html_escape(action)}</button>
      </section>
    """


def _draft_option_canvas(option_id: str, *, desktop: bool) -> tuple[int, int]:
    if desktop:
        if option_id == "OPTION-D":
            return (1600, 940)
        if option_id == "OPTION-E":
            return (1600, 920)
        if option_id == "OPTION-F":
            return (1680, 820)
        if option_id == "OPTION-G":
            return (1600, 920)
        return (1600, 900)
    if option_id == "OPTION-D":
        return (840, 840)
    if option_id == "OPTION-E":
        return (900, 800)
    if option_id == "OPTION-F":
        return (980, 690)
    if option_id == "OPTION-G":
        return (920, 820)
    return (760, 760)


def _draft_option_payload(option_id: str) -> dict[str, object]:
    payloads: dict[str, dict[str, object]] = {
        "OPTION-B": {
            "title": "Compact Directory Variant",
            "subtitle": "Dense doorway shell with stronger category grouping.",
            "labels": ["AI - ORIN", "PROVIDER - BLOCKED", "DATA - NONE"],
            "mode": "vertical",
            "cards": [
                ("01", "AI Control Center", "Trust state and quick orientation.", [("AI", "ORIN not implemented"), ("Provider", "Blocked; no model path active"), ("Visible data", "None leaves this machine")], "Open Control Center"),
                ("02", "Readiness & Diagnostics", "Local check and report doorway.", [("Local check", "Waiting for USER action"), ("Report", "Local readiness result only"), ("Prompt/data", "Not accepted, sent, or stored")], "Open Diagnostics"),
                ("03", "Capabilities & Maintenance", "Capability packs remain blocked.", [("Capability packs", "Install intent blocked"), ("Downloads", "Disabled"), ("Updates", "Future-gated")], "Open Capabilities"),
            ],
            "footer": "Historical/rejected comparison retained as a real rendered template, not a selectable final target.",
        },
        "OPTION-C": {
            "title": "Studio-Weighted Variant",
            "subtitle": "Rejected-risk comparator: too workspace/report weighted for the top level.",
            "labels": ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED"],
            "mode": "vertical",
            "cards": [
                ("01", "AI Workspace Panel", "Rejected-risk: this starts to feel like a workspace.", [("Risk", "Too much top-level workspace mass"), ("Provider", "Blocked"), ("Data", "None leaves this machine")], "Open Panel"),
                ("02", "Diagnostics Report Area", "Rejected-risk: report body appears inline.", [("Risk", "Detail belongs behind child surface"), ("Report", "Doorway only at top level"), ("Prompt/data", "Not sent or stored")], "Open Diagnostics"),
                ("03", "Maintenance Detail", "Rejected-risk: maintenance detail consumes top level.", [("Risk", "Too much lifecycle detail"), ("Downloads", "Disabled"), ("Updates", "Future-gated")], "Open Capabilities"),
            ],
            "footer": "Retained to show what not to accept: a top-level surface that becomes a workspace/report body.",
        },
        "OPTION-D": {
            "title": "AI Dashboard",
            "subtitle": "Top-level AI orientation, trust state, and category doorways.",
            "labels": ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED"],
            "mode": "d",
            "cards": [
                ("01", "AI Status & Trust", "Truthful AI state before any action.", [("AI", "ORIN not implemented; no real AI executing"), ("Provider", "Blocked; no provider/model path active"), ("Visible data", "None leaves this machine")], "Open Control Center"),
                ("02", "Readiness & Diagnostics", "Local checks and report doorway.", [("Local check", "Waiting for USER action"), ("Report", "Local readiness result only"), ("Prompt/data", "Not accepted, sent, stored, or indexed")], "Open Diagnostics"),
                ("03", "Capabilities & Maintenance", "Install/update intent without execution.", [("Capability packs", "Install intent blocked; downloads disabled"), ("Updates", "Future-gated; no install execution")], "Open Capabilities"),
            ],
            "footer": "Primary behavior-aligned candidate: compact doorway surface with row grammar inside grouped cards.",
        },
        "OPTION-E": {
            "title": "AI Dashboard",
            "subtitle": "Production doorway draft: compact AI truth, domain launchers, and future-gated handoffs.",
            "labels": ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED", "DATA - NONE"],
            "mode": "grid",
            "cards": [
                ("01", "AI Control Center", "Focused control domain for AI trust and status.", [("AI state", "ORIN not implemented"), ("Provider", "Blocked; no model path active"), ("Visible data", "None leaves this machine")], "Open Control Center"),
                ("02", "Readiness & Diagnostics", "Local checks, readiness report, and safe next steps.", [("Local check", "Waiting for USER action"), ("Readiness report", "Local decision aid only"), ("Prompt/data", "Not sent, stored, or indexed")], "Open Diagnostics"),
                ("03", "Capabilities", "Capability and maintenance lifecycle doorway.", [("Capability packs", "Install intent blocked"), ("Downloads", "Disabled"), ("Updates", "Future-gated")], "Open Capabilities"),
                ("04", "AI Settings", "Global settings handoff without FAM-003 mutation.", [("Settings route", "Future Global Settings / AI"), ("Private setup", "Developer and Owner gated"), ("Memory/cache", "Not active")], "Open Settings"),
            ],
            "footer": "Polished production doorway candidate; detailed reports, setup, logs, and provider internals open behind domain doors.",
        },
        "OPTION-F": {
            "title": "AI Dashboard",
            "subtitle": "Wide orientation draft: one trust summary, then horizontal domain lanes.",
            "labels": ["AI - ORIN", "PROVIDER - BLOCKED", "DATA - NONE"],
            "mode": "lanes",
            "cards": [
                ("01", "Control Center", "Focused AI control domain.", [("Control summary", "Trust state only; no execution")], "Open Control"),
                ("02", "Diagnostics", "Local checks and report.", [("Diagnostics summary", "Waiting for local action")], "Open Diagnostics"),
                ("03", "Capabilities", "Packs and maintenance.", [("Capability summary", "Downloads disabled")], "Open Capabilities"),
            ],
            "footer": "Future layout-arrangement candidate: wider summary/action zone and horizontal domain lanes.",
        },
        "OPTION-G": {
            "title": "AI Dashboard",
            "subtitle": "Refined D/E target: compact AI truth, grouped doorways, and polished row grammar.",
            "labels": ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED", "DATA - NONE"],
            "mode": "g",
            "cards": [
                ("01", "AI Status & Trust", "Truth-first orientation before any AI action.", [("AI", "ORIN not implemented; no real AI executing"), ("Provider", "Blocked; no provider/model path active"), ("Visible data", "None leaves this machine")], "Open Control Center"),
                ("02", "AI Readiness & Diagnostics", "Local checks and readiness report doorway.", [("Local check", "Waiting for USER action"), ("Readiness report", "Local decision aid behind diagnostics"), ("Prompt/data", "Not accepted, sent, stored, or indexed")], "Open Diagnostics"),
                ("03", "Capabilities & Maintenance", "Capability state without install or update execution.", [("Capability packs", "Install intent blocked; downloads disabled"), ("Downloads/updates", "Future-gated; no install execution")], "Open Capabilities"),
            ],
            "footer": "Recommended current-cycle target basis: Option D behavior and row grammar with selective Option E polish; no Option F customization.",
        },
    }
    return payloads[option_id]


def _draft_template_html(option_id: str, *, desktop: bool) -> str:
    canvas_width, canvas_height = _draft_option_canvas(option_id, desktop=desktop)
    win_x, win_y, win_w, win_h = _window_geometry(option_id, canvas_width, canvas_height, desktop=desktop)
    payload = _draft_option_payload(option_id)
    labels = payload["labels"]
    status_cells = "".join(f"<span>{_html_escape(str(label))}</span>" for label in labels)  # type: ignore[arg-type]
    mode = str(payload["mode"])
    cards = payload["cards"]  # type: ignore[assignment]
    if mode == "grid":
        coords = [(30, 174, 388, 206), (436, 174, 354, 206), (30, 400, 388, 224), (436, 400, 354, 224)]
    elif mode == "lanes":
        coords = [(30, 320, 268, 220), (322, 320, 268, 220), (614, 320, 268, 220)]
    elif mode == "d":
        coords = [(28, 184, win_w - 56, 170), (28, 370, win_w - 56, 170), (28, 556, win_w - 56, 148)]
    elif mode == "g":
        coords = [(30, 184, win_w - 60, 170), (30, 370, win_w - 60, 170), (30, 556, win_w - 60, 150)]
    else:
        coords = [(34, 186, win_w - 68, 146), (34, 350, win_w - 68, 146), (34, 514, win_w - 68, 146)]
    card_html = "\n".join(
        _css_card(
            number,
            title,
            description,
            rows,
            action,
            left=left,
            top=top,
            width=width,
            height=height,
            compact=mode == "lanes",
        )
        for (number, title, description, rows, action), (left, top, width, height) in zip(cards, coords)
    )
    summary = ""
    if mode == "lanes":
        summary = """
        <section class="summary-zone">
          <strong>ORIN is not implemented; provider/model execution is not active.</strong>
          <span>Use the domain lanes below to open focused AI control, diagnostics, or capability surfaces.</span>
          <button class="summary-action">Open Diagnostics</button>
        </section>
        """
    footer_html = ""
    if mode in {"grid", "lanes"}:
        footer_html = f'<div class="footer">{_html_escape(str(payload["footer"]))}</div>'
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ width:{canvas_width}px; height:{canvas_height}px; margin:0; overflow:hidden; }}
  body {{
    font-family: "Segoe UI", Arial, sans-serif;
    background:
      linear-gradient(rgba(42,130,157,.12) 1px, transparent 1px),
      linear-gradient(90deg, rgba(42,130,157,.12) 1px, transparent 1px),
      radial-gradient(circle at 14% 44%, rgba(64,203,240,.18), transparent 22%),
      #000508;
    background-size: 32px 32px, 32px 32px, 100% 100%, 100% 100%;
    color: #eaf7fa;
  }}
  .window {{
    position:absolute; left:{win_x}px; top:{win_y}px; width:{win_w}px; height:{win_h}px;
    border: 2px solid #48bcd4; border-radius:30px; background:#010f1a;
    box-shadow: 8px 10px 0 rgba(0,9,14,.88), 0 0 30px rgba(46, 190, 220, .13);
    overflow:hidden;
  }}
  .header {{
    position:absolute; left:18px; right:18px; top:18px; height:{146 if mode in {"d", "g"} else 132 if mode == "grid" else 120}px;
    border-radius:24px; background:#020d19; border:1px solid rgba(63,160,190,.28);
  }}
  .brand {{ position:absolute; left:26px; top:18px; color:#60dcef; text-transform:uppercase; font-weight:800; font-size:13px; letter-spacing:1.8px; }}
  .title {{ position:absolute; left:26px; top:42px; font-size:31px; line-height:33px; font-weight:900; }}
  .subtitle {{ position:absolute; left:26px; top:82px; max-width:650px; color:#98c8d2; font-weight:800; font-size:12px; }}
  .controls {{ position:absolute; right:28px; top:28px; width:64px; height:34px; border:2px solid #4fc9e1; border-radius:17px; background:#041e2a; display:flex; align-items:center; justify-content:space-evenly; }}
  .controls span {{ width:24px; height:24px; border-radius:50%; border:1px solid rgba(126,225,240,.62); display:flex; align-items:center; justify-content:center; color:#e9f8fb; font-weight:900; font-size:13px; }}
  .strip {{ position:absolute; left:42px; top:{122 if mode in {"d", "g"} else 112 if mode == "grid" else 142}px; height:36px; border-radius:18px; border:1px solid rgba(73,178,205,.72); background:#041e2a; padding:0 14px; display:flex; gap:20px; align-items:center; color:#b4f0e2; font-weight:900; font-size:11px; text-transform:uppercase; }}
  .summary-zone {{ position:absolute; left:30px; top:160px; right:30px; height:134px; border-radius:20px; border:1px solid #267391; background:#031422; padding:22px 24px; }}
  .summary-zone strong {{ display:block; font-size:17px; font-weight:900; }}
  .summary-zone span {{ display:block; margin-top:12px; color:#94c2cd; font-weight:800; font-size:12px; }}
  .summary-action {{ position:absolute; right:34px; bottom:20px; }}
  .card {{ position:absolute; border-radius:18px; border:1px solid #267391; background:#031322; box-shadow: 3px 5px 0 rgba(0,9,14,.84); }}
  .badge {{ position:absolute; left:16px; top:16px; width:36px; height:36px; border-radius:12px; display:flex; align-items:center; justify-content:center; background:#053346; border:1px solid #48c2dc; color:#78eaef; font-size:12px; font-weight:900; }}
  .card-copy {{ position:absolute; left:66px; top:14px; right:18px; }}
  .card-copy strong {{ display:block; font-size:16px; line-height:18px; font-weight:900; text-transform:uppercase; }}
  .card-copy span {{ display:block; margin-top:4px; color:#98c8d2; font-size:11px; font-weight:800; }}
  .rows {{ position:absolute; left:22px; right:22px; top:70px; }}
  .row {{ height:27px; border-top:1px solid #54b2c7; box-shadow: inset 0 1px 0 rgba(7,43,57,.95); display:flex; align-items:center; font-size:10px; font-weight:900; }}
  .row::before {{ content:""; width:3px; height:14px; background:#50bdd0; margin-right:9px; }}
  .row-label {{ width:152px; color:#76b4c4; text-transform:uppercase; }}
  .row-value {{ color:#98ead3; }}
  .action, .summary-action {{ position:absolute; right:20px; bottom:12px; min-width:122px; height:32px; border-radius:16px; border:2px solid #46abc7; background:#062534; color:#e8f6f9; font-size:10px; font-weight:900; text-transform:uppercase; }}
  .compact .card-copy strong {{ font-size:14px; }}
  .compact .rows {{ top:96px; }}
  .footer {{ position:absolute; left:48px; right:48px; bottom:36px; color:#80bac6; font-size:12px; font-weight:800; }}
  .desktop-footer {{ position:absolute; left:24px; bottom:20px; right:24px; color:#82bec8; background:#000a0e; font-size:15px; font-weight:800; }}
</style>
</head>
<body>
  <main class="window" data-real-draft-window-template="true" data-option="{option_id}" data-renderer="PySide6-QWebEngine">
    <section class="header">
      <div class="brand">Nexus Desktop AI</div>
      <div class="title">{_html_escape(str(payload["title"]))}</div>
      <div class="subtitle">{_html_escape(str(payload["subtitle"]))}</div>
      <div class="controls" aria-label="Window controls"><span>-</span><span>x</span></div>
      <div class="strip">{status_cells}</div>
    </section>
    {summary}
    {card_html}
    {footer_html}
  </main>
  {f'<div class="desktop-footer">{_html_escape(str(payload["footer"]))}</div>' if desktop else ''}
</body>
</html>
"""


def _ensure_qt_application():
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu --disable-software-rasterizer")
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    from PySide6.QtWidgets import QApplication

    return QApplication.instance() or QApplication(sys.argv)


def _render_html_png(html: str, target: Path, *, width: int, height: int) -> None:
    from PySide6.QtCore import QEventLoop, QTimer, QUrl
    from PySide6.QtWebEngineWidgets import QWebEngineView

    app = _ensure_qt_application()
    target.parent.mkdir(parents=True, exist_ok=True)
    view = QWebEngineView()
    view.resize(width, height)
    view.setHtml(html, QUrl.fromLocalFile(str(PACKET_DIR) + os.sep))
    view.show()
    loop = QEventLoop()
    view.loadFinished.connect(lambda _ok: QTimer.singleShot(450, loop.quit))
    QTimer.singleShot(4000, loop.quit)
    loop.exec()
    app.processEvents()
    pixmap = view.grab()
    if not pixmap.save(str(target)):
        view.close()
        raise RuntimeError(f"Failed to render draft-window template screenshot: {target}")
    view.close()
    app.processEvents()


def _render_draft_option_media(option_id: str, folder: str, focused: Path, desktop_path: Path) -> tuple[str, str]:
    template_dir = PACKET_DIR / DRAFT_TEMPLATE_ROOT / folder
    template_dir.mkdir(parents=True, exist_ok=True)
    focused_html = _draft_template_html(option_id, desktop=False)
    desktop_html = _draft_template_html(option_id, desktop=True)
    focused_template = template_dir / f"{option_id.lower()}_focused_template.html"
    desktop_template = template_dir / f"{option_id.lower()}_desktop_template.html"
    focused_template.write_text(focused_html, encoding="utf-8")
    desktop_template.write_text(desktop_html, encoding="utf-8")
    focused_width, focused_height = _draft_option_canvas(option_id, desktop=False)
    desktop_width, desktop_height = _draft_option_canvas(option_id, desktop=True)
    _render_html_png(focused_html, focused, width=focused_width, height=focused_height)
    _render_html_png(desktop_html, desktop_path, width=desktop_width, height=desktop_height)
    return (
        str(focused_template.relative_to(PACKET_DIR)).replace("\\", "/"),
        str(desktop_template.relative_to(PACKET_DIR)).replace("\\", "/"),
    )


def _draw_soft_grid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for gx in range(0, width, 32):
        draw.line((gx, 0, gx, height), fill=(3, 25, 34), width=1)
    for gy in range(0, height, 32):
        draw.line((0, gy, width, gy), fill=(3, 25, 34), width=1)


def _draw_corner_glow(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    for radius, shade in ((380, 13), (300, 18), (220, 24), (150, 32)):
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(4, shade, shade + 18), width=1)


def _draw_row_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    number: str,
    title: str,
    description: str,
    rows: list[tuple[str, str]],
    action: str | None = None,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 3, y1 + 5, x2 + 3, y2 + 5), radius=18, fill=(0, 9, 14))
    draw.rounded_rectangle(box, radius=18, fill=(3, 19, 34), outline=(38, 115, 145), width=1)
    draw.rounded_rectangle((x1 + 16, y1 + 16, x1 + 52, y1 + 52), radius=12, fill=(5, 51, 70), outline=(72, 194, 220), width=1)
    draw.text((x1 + 25, y1 + 26), number, fill=(120, 234, 239), font=_font(12))
    draw.text((x1 + 66, y1 + 15), title.upper(), fill=(236, 247, 250), font=_font(16))
    draw.text((x1 + 66, y1 + 40), description, fill=(148, 194, 205), font=_font(11))
    yy = y1 + 70
    label_font = _font(10)
    value_font = _font(10)
    for label, value in rows:
        draw.line((x1 + 22, yy, x2 - 22, yy), fill=(84, 178, 199), width=1)
        draw.line((x1 + 22, yy + 1, x2 - 22, yy + 1), fill=(9, 42, 56), width=1)
        draw.rectangle((x1 + 22, yy + 6, x1 + 25, yy + 20), fill=(80, 189, 207))
        draw.text((x1 + 34, yy + 5), label.upper(), fill=(118, 180, 196), font=label_font)
        draw.text((x1 + 196, yy + 5), value, fill=(152, 234, 211), font=value_font)
        yy += 27
    if action:
        action_font = _font(11)
        button_w = max(124, _text_width(draw, action.upper(), action_font) + 36)
        bx2 = x2 - 20
        bx1 = bx2 - button_w
        by1 = y2 - 42
        by2 = y2 - 12
        draw.rounded_rectangle((bx1, by1, bx2, by2), radius=15, fill=(6, 37, 52), outline=(70, 171, 199), width=2)
        draw.text((bx1 + 18, by1 + 9), action.upper(), fill=(232, 246, 249), font=action_font)


def _draw_option_d_mockup(path: Path, desktop: bool) -> None:
    width, height = (1600, 940) if desktop else (840, 840)
    img = Image.new("RGB", (width, height), (0, 5, 8))
    draw = ImageDraw.Draw(img)
    _draw_soft_grid(draw, width, height)
    _draw_corner_glow(draw, 190, 390)
    win_w, win_h = 748, 722
    x = 810 if desktop else 36
    y = 58 if desktop else 36
    draw.rounded_rectangle((x + 8, y + 10, x + win_w + 8, y + win_h + 10), radius=32, fill=(0, 11, 17))
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=30, fill=(1, 15, 26), outline=(72, 188, 212), width=2)
    draw.rounded_rectangle((x + 18, y + 18, x + win_w - 18, y + 164), radius=24, fill=(2, 13, 25), outline=(18, 61, 82), width=1)
    draw.text((x + 44, y + 36), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 44, y + 62), "AI Dashboard", fill=(240, 248, 250), font=_font(30))
    draw.text((x + 44, y + 104), "Top-level AI orientation, trust state, and category doorways.", fill=(152, 200, 210), font=_font(12))
    draw.rounded_rectangle((x + win_w - 92, y + 28, x + win_w - 28, y + 62), radius=17, fill=(4, 30, 42), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 75, y + 37), "-  x", fill=(230, 247, 250), font=_font(13))
    _draw_status_strip(draw, x + 42, y + 122, ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED"])
    card_x1 = x + 28
    card_x2 = x + win_w - 28
    _draw_row_card(
        draw,
        (card_x1, y + 184, card_x2, y + 354),
        "01",
        "AI Status & Trust",
        "Truthful AI state before any action.",
        [
            ("AI", "ORIN not implemented; no real AI executing"),
            ("Provider", "Blocked; no provider/model path active"),
            ("Visible data", "None leaves this machine"),
        ],
        "Open Control Center",
    )
    _draw_row_card(
        draw,
        (card_x1, y + 370, card_x2, y + 540),
        "02",
        "Readiness & Diagnostics",
        "Local checks and report doorway.",
        [
            ("Local check", "Waiting for USER action"),
            ("Report", "Local readiness result only"),
            ("Prompt/data", "Not accepted, sent, stored, or indexed"),
        ],
        "Open Diagnostics",
    )
    _draw_row_card(
        draw,
        (card_x1, y + 556, card_x2, y + 704),
        "03",
        "Capabilities & Maintenance",
        "Install/update intent without execution.",
        [
            ("Capability packs", "Install intent blocked; downloads disabled"),
            ("Updates", "Future-gated; no install execution"),
        ],
        "Open Capabilities",
    )
    if desktop:
        draw.rectangle((0, height - 62, width, height), fill=(0, 10, 14))
        draw.text((24, height - 42), "Option D desktop/context render: compact doorway surface with row grammar inside grouped cards", fill=(130, 190, 198), font=_font(15))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _draw_option_e_mockup(path: Path, desktop: bool) -> None:
    width, height = (1600, 920) if desktop else (900, 800)
    img = Image.new("RGB", (width, height), (0, 5, 8))
    draw = ImageDraw.Draw(img)
    _draw_soft_grid(draw, width, height)
    _draw_corner_glow(draw, 230, 360)
    win_w, win_h = 820, 728
    x = 760 if desktop else 34
    y = 54 if desktop else 34
    draw.rounded_rectangle((x + 8, y + 10, x + win_w + 8, y + win_h + 10), radius=32, fill=(0, 11, 17))
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=30, fill=(1, 15, 26), outline=(72, 188, 212), width=2)
    draw.rounded_rectangle((x + 18, y + 18, x + win_w - 18, y + 150), radius=24, fill=(2, 12, 23), outline=(18, 62, 82), width=1)
    draw.text((x + 44, y + 34), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 44, y + 58), "AI Dashboard", fill=(240, 248, 250), font=_font(31))
    draw.text((x + 44, y + 98), "Production doorway draft: compact AI truth, domain launchers, and future-gated handoffs.", fill=(152, 200, 210), font=_font(12))
    draw.rounded_rectangle((x + win_w - 92, y + 28, x + win_w - 28, y + 62), radius=17, fill=(4, 30, 42), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 75, y + 37), "-  x", fill=(230, 247, 250), font=_font(13))
    _draw_status_strip(draw, x + 42, y + 112, ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED", "DATA - NONE"])
    left_x1 = x + 30
    left_x2 = x + 418
    right_x1 = x + 436
    right_x2 = x + win_w - 30
    _draw_row_card(
        draw,
        (left_x1, y + 174, left_x2, y + 380),
        "01",
        "AI Control Center",
        "Focused control domain for AI trust and status.",
        [
            ("AI state", "ORIN not implemented"),
            ("Provider", "Blocked; no model path active"),
            ("Visible data", "None leaves this machine"),
        ],
        "Open Control Center",
    )
    _draw_row_card(
        draw,
        (right_x1, y + 174, right_x2, y + 380),
        "02",
        "Readiness & Diagnostics",
        "Local checks, readiness report, and safe next steps.",
        [
            ("Local check", "Waiting for USER action"),
            ("Readiness report", "Local decision aid only"),
            ("Prompt/data", "Not sent, stored, or indexed"),
        ],
        "Open Diagnostics",
    )
    _draw_row_card(
        draw,
        (left_x1, y + 400, left_x2, y + 624),
        "03",
        "Capabilities",
        "Capability and maintenance lifecycle doorway.",
        [
            ("Capability packs", "Install intent blocked"),
            ("Downloads", "Disabled"),
            ("Updates", "Future-gated"),
        ],
        "Open Capabilities",
    )
    _draw_row_card(
        draw,
        (right_x1, y + 400, right_x2, y + 624),
        "04",
        "AI Settings",
        "Global settings handoff without FAM-003 mutation.",
        [
            ("Settings route", "Future Global Settings / AI"),
            ("Private setup", "Developer and Owner gated"),
            ("Memory/cache", "Not active"),
        ],
        "Open Settings",
    )
    draw.text((x + 48, y + 668), "Top level stays compact: detailed reports, setup, logs, and provider internals open behind domain doors.", fill=(128, 186, 198), font=_font(12))
    if desktop:
        draw.rectangle((0, height - 62, width, height), fill=(0, 10, 14))
        draw.text((24, height - 42), "Option E desktop/context render: polished two-by-two production doorway draft", fill=(130, 190, 198), font=_font(15))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _draw_option_f_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    number: str,
    title: str,
    summary: str,
    row: str,
    action: str,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 3, y1 + 5, x2 + 3, y2 + 5), radius=18, fill=(0, 9, 14))
    draw.rounded_rectangle(box, radius=18, fill=(3, 19, 34), outline=(38, 115, 145), width=1)
    draw.rounded_rectangle((x1 + 16, y1 + 16, x1 + 52, y1 + 52), radius=12, fill=(5, 51, 70), outline=(72, 194, 220), width=1)
    draw.text((x1 + 25, y1 + 26), number, fill=(120, 234, 239), font=_font(12))
    draw.text((x1 + 66, y1 + 16), title.upper(), fill=(236, 247, 250), font=_font(14))
    draw.text((x1 + 18, y1 + 68), summary, fill=(148, 194, 205), font=_font(11))
    draw.line((x1 + 20, y1 + 96, x2 - 20, y1 + 96), fill=(84, 178, 199), width=1)
    draw.rectangle((x1 + 20, y1 + 104, x1 + 23, y1 + 118), fill=(80, 189, 207))
    draw.text((x1 + 32, y1 + 102), row, fill=(152, 234, 211), font=_font(10))
    action_font = _font(10)
    button_w = max(126, _text_width(draw, action.upper(), action_font) + 30)
    bx2 = x2 - 20
    bx1 = bx2 - button_w
    by1 = y2 - 44
    by2 = y2 - 12
    draw.rounded_rectangle((bx1, by1, bx2, by2), radius=15, fill=(6, 37, 52), outline=(70, 171, 199), width=2)
    draw.text((bx1 + 15, by1 + 10), action.upper(), fill=(232, 246, 249), font=action_font)


def _draw_option_f_mockup(path: Path, desktop: bool) -> None:
    width, height = (1680, 820) if desktop else (980, 690)
    img = Image.new("RGB", (width, height), (0, 5, 8))
    draw = ImageDraw.Draw(img)
    _draw_soft_grid(draw, width, height)
    _draw_corner_glow(draw, 310, 320)
    win_w, win_h = 910, 620
    x = 700 if desktop else 34
    y = 82 if desktop else 34
    draw.rounded_rectangle((x + 8, y + 10, x + win_w + 8, y + win_h + 10), radius=32, fill=(0, 11, 17))
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=30, fill=(1, 15, 26), outline=(72, 188, 212), width=2)
    draw.rounded_rectangle((x + 18, y + 18, x + win_w - 18, y + 138), radius=24, fill=(2, 13, 25), outline=(18, 61, 82), width=1)
    draw.text((x + 44, y + 36), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 44, y + 60), "AI Dashboard", fill=(240, 248, 250), font=_font(31))
    draw.text((x + 44, y + 101), "Wide orientation draft: one trust summary, then horizontal domain lanes.", fill=(152, 200, 210), font=_font(12))
    draw.rounded_rectangle((x + win_w - 92, y + 28, x + win_w - 28, y + 62), radius=17, fill=(4, 30, 42), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 75, y + 37), "-  x", fill=(230, 247, 250), font=_font(13))
    draw.rounded_rectangle((x + 30, y + 160, x + win_w - 30, y + 294), radius=20, fill=(3, 20, 34), outline=(38, 115, 145), width=1)
    draw.text((x + 54, y + 182), "ORIN is not implemented; provider/model execution is not active.", fill=(236, 247, 250), font=_font(17))
    draw.text((x + 54, y + 214), "Use the domain lanes below to open focused AI control, diagnostics, or capability surfaces.", fill=(148, 194, 205), font=_font(12))
    _draw_status_strip(draw, x + 52, y + 246, ["AI - ORIN", "PROVIDER - BLOCKED", "DATA - NONE"])
    action_font = _font(11)
    bx2 = x + win_w - 52
    bx1 = bx2 - 186
    by1 = y + 238
    draw.rounded_rectangle((bx1, by1, bx2, by1 + 36), radius=18, fill=(6, 37, 52), outline=(70, 171, 199), width=2)
    draw.text((bx1 + 18, by1 + 11), "OPEN DIAGNOSTICS", fill=(232, 246, 249), font=action_font)
    card_y1 = y + 320
    card_y2 = y + 540
    card_w = 268
    _draw_option_f_card(draw, (x + 30, card_y1, x + 30 + card_w, card_y2), "01", "Control Center", "Focused AI control domain.", "Trust state only; no execution", "Open Control")
    _draw_option_f_card(draw, (x + 322, card_y1, x + 322 + card_w, card_y2), "02", "Diagnostics", "Local checks and report.", "Waiting for local action", "Open Diagnostics")
    _draw_option_f_card(draw, (x + 614, card_y1, x + 614 + card_w, card_y2), "03", "Capabilities", "Packs and maintenance.", "Downloads disabled", "Open Capabilities")
    draw.text((x + 48, y + 574), "Alternate hierarchy: fewer vertical rows, stronger summary/action zone, horizontal domain scan.", fill=(128, 186, 198), font=_font(12))
    if desktop:
        draw.rectangle((0, height - 62, width, height), fill=(0, 10, 14))
        draw.text((24, height - 42), "Option F desktop/context render: wide summary plus horizontal domain-lane draft", fill=(130, 190, 198), font=_font(15))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _copy_actual_media() -> list[RenderOption]:
    option_root = PACKET_DIR / "Review Aids" / "Render Media" / "Option-A-current-implementation"
    for kind, source in {
        "focused": PROOF_ROOT / "01_dashboard_initial_focused_window.png",
        "desktop": PROOF_ROOT / "01_dashboard_initial_full_desktop.png",
    }.items():
        target = option_root / f"option_a_current_{kind}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    focused = option_root / "option_a_current_focused.png"
    desktop = option_root / "option_a_current_desktop.png"
    annotated_focused = option_root / "option_a_current_focused_annotated.png"
    annotated_desktop = option_root / "option_a_current_desktop_annotated.png"
    _annotate_render(focused, annotated_focused, "OPTION-A", desktop=False)
    _annotate_render(desktop, annotated_desktop, "OPTION-A", desktop=True)
    return [
        RenderOption(
            "OPTION-A",
            "Design Candidate Render using actual app/runtime screenshot",
            "DOORWAY_SHELL",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_focused.png",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_desktop.png",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_focused_annotated.png",
            "Review Aids/Render Media/Option-A-current-implementation/option_a_current_desktop_annotated.png",
            "Actual current branch render: compact hub, category doorways, and child/domain window proof carry-in.",
        )
    ]


def _copy_manifest_media() -> None:
    if not PROOF_ROOT.exists():
        raise FileNotFoundError(f"Missing proof media root: {PROOF_ROOT}")
    for source in sorted(PROOF_ROOT.glob("*.png")):
        if source.name.endswith("_focused_window.png"):
            target_dir = PACKET_DIR / "Review Aids" / "Inspectable Evidence" / "focused_window_screenshots"
        elif source.name.endswith("_full_desktop.png"):
            target_dir = PACKET_DIR / "Review Aids" / "Inspectable Evidence" / "full_desktop_screenshots"
        else:
            target_dir = PACKET_DIR / "Review Aids" / "Inspectable Evidence" / "other_screenshots"
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_dir / source.name)


def _current_packet_section(text: str) -> str:
    return _section(text, "## Packet Review State")


def _generate_candidate_media() -> list[RenderOption]:
    specs = [
        ("OPTION-B", "Compact Directory Variant", "Slightly denser doorway shell with stronger category grouping.", "Option-B-compact-directory", "DOORWAY_SHELL"),
        ("OPTION-C", "Studio-Weighted Variant", "Larger information-forward shell retained only as a rejected-risk comparator.", "Option-C-studio-weighted", "SETTINGS_PANEL"),
    ]
    result = []
    for option_id, title, subtitle, folder, footprint in specs:
        focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_focused.png"
        desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_desktop.png"
        annotated_focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_focused_annotated.png"
        annotated_desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_desktop_annotated.png"
        _render_draft_option_media(option_id, folder, focused, desktop)
        _annotate_render(focused, annotated_focused, option_id, desktop=False)
        _annotate_render(desktop, annotated_desktop, option_id, desktop=True)
        result.append(
            RenderOption(
                option_id,
                DRAFT_RENDER_AUTHORITY,
                footprint,
                str(focused.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(annotated_focused.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(annotated_desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
                subtitle,
            )
        )
    return result


def _generate_option_d_media() -> list[RenderOption]:
    folder = "Option-D-row-grammar-doorway"
    focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / "option-d_focused.png"
    desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / "option-d_desktop.png"
    annotated_focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / "option-d_focused_annotated.png"
    annotated_desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / "option-d_desktop_annotated.png"
    _render_draft_option_media("OPTION-D", folder, focused, desktop)
    _annotate_render(focused, annotated_focused, "OPTION-D", desktop=False)
    _annotate_render(desktop, annotated_desktop, "OPTION-D", desktop=True)
    return [
        RenderOption(
            "OPTION-D",
            DRAFT_RENDER_AUTHORITY,
            "DOORWAY_SHELL",
            str(focused.relative_to(PACKET_DIR)).replace("\\", "/"),
            str(desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
            str(annotated_focused.relative_to(PACKET_DIR)).replace("\\", "/"),
            str(annotated_desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
            "Hybrid target: Option A product structure/source-truth labels, Option B compact grouping rhythm, accepted AI Control Center row grammar and full-window feel, with Option C retained only as rejected-risk boundary.",
        )
    ]


def _generate_next_cycle_media() -> list[RenderOption]:
    specs = [
        (
            "OPTION-E",
            "Option-E-production-doorway",
            _draw_option_e_mockup,
            "DOORWAY_SHELL",
            "Next-cycle production doorway variant: a polished two-by-two grouped card grid with stronger finished-window rhythm, compact trust strip, AI Settings handoff, and row grammar kept inside grouped doorway cards.",
        ),
        (
            "OPTION-F",
            "Option-F-wide-orientation-lanes",
            _draw_option_f_mockup,
            "WIDE_ORIENTATION_LANES",
            "Next-cycle alternate hierarchy variant: a wider top summary/action zone with horizontal domain lanes, fewer vertical rows, and a materially different scan path from the row-grammar doorway grid.",
        ),
        (
            "OPTION-G",
            "Option-G-d-e-refined-target",
            _draw_option_e_mockup,
            "DOORWAY_SHELL",
            "Recommended refined current-cycle target: Option D behavior, grouped doorway cards, and row grammar with selective Option E production polish, without Option F layout-customization behavior.",
        ),
    ]
    result = []
    for option_id, folder, draw_func, footprint, description in specs:
        focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_focused.png"
        desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_desktop.png"
        annotated_focused = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_focused_annotated.png"
        annotated_desktop = PACKET_DIR / "Review Aids" / "Render Media" / folder / f"{option_id.lower()}_desktop_annotated.png"
        _render_draft_option_media(option_id, folder, focused, desktop)
        _annotate_render(focused, annotated_focused, option_id, desktop=False)
        _annotate_render(desktop, annotated_desktop, option_id, desktop=True)
        result.append(
            RenderOption(
                option_id,
                DRAFT_RENDER_AUTHORITY,
                footprint,
                str(focused.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(annotated_focused.relative_to(PACKET_DIR)).replace("\\", "/"),
                str(annotated_desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
                description,
            )
        )
    return result


def _options_table(options: list[RenderOption]) -> str:
    rows = [
        "| Option ID | Surface | Footprint | Authority | Clean Focused Render | Annotated Focused Render | Clean Desktop / Context Render | Annotated Desktop / Context Render | USER critique focus |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        rows.append(
            f"| `{option.option_id}` | AI Dashboard / AI Control Center visual acceptance target guide | `{option.footprint}` | `{option.authority}` | `{option.focused_media}` | `{option.annotated_focused_media}` | `{option.desktop_media}` | `{option.annotated_desktop_media}` | {option.description} |"
        )
    return "\n".join(rows)


def _decision_options_table(options: list[RenderOption]) -> str:
    rows = [
        "| Option ID | Surface | Footprint | Authority | USER critique focus |",
        "| --- | --- | --- | --- | --- |",
    ]
    for option in options:
        rows.append(
            f"| `{option.option_id}` | AI Dashboard / AI Control Center visual acceptance target guide | `{option.footprint}` | `{option.authority}` | {option.description} |"
        )
    return "\n".join(rows)


def _annotation_manifest_table(options: list[RenderOption]) -> str:
    rows = [
        "| Option ID | Annotation ID | Element / group type | Target label / name | Visual region | Marker style | Color cue | Non-color cue | Label box | Leader line | Purpose | Annotated file |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        for image_path, desktop in (
            (option.annotated_focused_media, False),
            (option.annotated_desktop_media, True),
        ):
            target_path = PACKET_DIR / image_path
            with Image.open(target_path) as image:
                base_width = image.size[0] - ANNOTATION_LABEL_PANEL_WIDTH
                specs = _annotation_specs(option.option_id, base_width, image.size[1], desktop=desktop)
            for index, spec in enumerate(specs, start=1):
                box = spec.region
                geometry = _callout_geometry(box, index, base_width + ANNOTATION_LABEL_PANEL_WIDTH)
                label_box = geometry["label_box"]
                leader_line = geometry["leader_line"]
                rows.append(
                    f"| `{option.option_id}` | `{spec.annotation_id}` | `{spec.element_type}` | {spec.target_label} | `{box[0]},{box[1]},{box[2]},{box[3]}` | `{spec.marker_style}` | `{spec.color_name}` | {spec.non_color_cue} | `{label_box[0]},{label_box[1]},{label_box[2]},{label_box[3]}` | `{leader_line[0]},{leader_line[1]},{leader_line[2]},{leader_line[3]}` | {spec.purpose} | `{image_path}` |"
                )
    return "\n".join(rows)


def _image_relevance_manifest_table(options: list[RenderOption]) -> str:
    rows = [
        "| Included image | Classification | Why USER needs it | Supported decision |",
        "| --- | --- | --- | --- |",
    ]
    for option in options:
        rows.extend(
            [
                (
                    f"| `{option.focused_media}` | `USER decision image` | Clean focused view of {option.option_id} without annotation overlays. | Compare/select/revise visual target footprint and layout. |"
                ),
                (
                    f"| `{option.annotated_focused_media}` | `required annotation image` | Focused view with in-canvas marker IDs, outlines, and leader lines. | Map visible element groups to the element ledger without guessing. |"
                ),
                (
                    f"| `{option.desktop_media}` | `required context image` | Clean desktop/context view showing placement and monitor relationship. | Judge footprint and surrounding desktop relationship. |"
                ),
                (
                    f"| `{option.annotated_desktop_media}` | `required annotation image` | Desktop/context view with in-canvas marker IDs, outlines, and leader lines. | Map context-level placement and same element IDs. |"
                ),
            ]
        )
    return "\n".join(rows)


def _draft_template_manifest_table(options: list[RenderOption]) -> str:
    rows = [
        "| Option ID | Clean media authority | Focused render source | Desktop/context render source | Template artifact status | Review disposition |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        if option.option_id == "OPTION-A":
            rows.append(
                f"| `{option.option_id}` | actual current app/runtime screenshot | `{option.focused_media}` | `{option.desktop_media}` | `No branch-local draft template: runtime baseline only` | current implementation baseline/comparator, not selectable proof by itself |"
            )
            continue
        folder = Path(option.focused_media).parent.name
        focused_template = f"{DRAFT_TEMPLATE_ROOT}/{folder}/{option.option_id.lower()}_focused_template.html"
        desktop_template = f"{DRAFT_TEMPLATE_ROOT}/{folder}/{option.option_id.lower()}_desktop_template.html"
        disposition = {
            "OPTION-B": "historical compact-directory reference; not recommended as current target",
            "OPTION-C": "historical/rejected workspace-weighted risk comparator",
            "OPTION-D": "primary behavior-aligned candidate matured into a real rendered draft-window/template",
            "OPTION-E": "polished production-doorway candidate regenerated as a real rendered draft-window/template",
            "OPTION-F": "future user-customizable layout arrangement candidate, not the selected FAM-007 target",
            "OPTION-G": "recommended current-cycle D/E hybrid target basis regenerated as a real rendered draft-window/template",
        }[option.option_id]
        rows.append(
            f"| `{option.option_id}` | `{DRAFT_RENDER_AUTHORITY}` | `{focused_template}` -> `{option.focused_media}` | `{desktop_template}` -> `{option.desktop_media}` | `HTML/CSS draft template rendered by PySide6 QWebEngine; annotation overlay added afterward for USER review` | {disposition} |"
        )
    return "\n".join(rows)


def _artifact_to_surface_ledger_table(options: list[RenderOption]) -> str:
    source_paths = (
        "nexus_visual/ai_control_center.html; nexus_visual/ai_control_center.css; "
        "nexus_visual/ai_control_center.js; desktop/desktop_renderer.py; "
        "dev/orin_ai_control_center_live_resize_validation.py"
    )
    rows = [
        "| Artifact | Artifact class | USER-facing surface | Element groups | Source / code path | UIREF owner | Branch-local proof target | Future implementation comparison use |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        option_note = {
            "OPTION-A": "Actual current-branch runtime snapshot used as source-structure evidence and comparator; not accepted implementation proof by itself.",
            "OPTION-B": "Deterministic branch-local candidate mockup for possible denser doorway grouping.",
            "OPTION-C": "Deterministic branch-local rejected-risk comparator showing larger settings/workspace mass.",
            "OPTION-D": "Mature D2-style hybrid row-grammar doorway target using Option A structure, Option B grouping discipline, and the attached accepted AI Control Center row grammar; not implementation proof by itself.",
            "OPTION-E": "Next-cycle production doorway variant with a polished two-by-two grouped-card grid, AI Settings handoff, and row grammar kept inside compact domain cards; not implementation proof by itself.",
            "OPTION-F": "Future candidate / possible USER-configurable layout arrangement pattern only: wide top summary/action zone and horizontal domain lanes from seed packet "
            f"{OPTION_F_SEED_PACKET_PATH} sha256 {OPTION_F_SEED_PACKET_SHA256}; example only, subject to later source-truth owner approval, and not implementation proof by itself.",
            "OPTION-G": "Recommended current-cycle D/E hybrid target basis: Option D behavior and row grammar, selective Option E visual maturity, no AI Settings scope broadening, and no Option F layout-customization behavior; not implementation proof by itself.",
        }[option.option_id]
        for artifact, artifact_class, proof_target in (
            (option.focused_media, "candidate clean focused render", "focused footprint, density, hierarchy, copy, and doorway layout"),
            (option.annotated_focused_media, "candidate annotated focused render", "element-group trace and visible callout mapping"),
            (option.desktop_media, "candidate clean desktop/context render", "desktop placement, scale, and surrounding visual relationship"),
            (option.annotated_desktop_media, "candidate annotated desktop/context render", "context-level element-group trace and callout mapping"),
        ):
            rows.append(
                f"| `{artifact}` | `{artifact_class}` | AI Dashboard / AI Control Center visual-target guide | option-specific review IDs such as `A-STATUS-01`, `B-CARD-02`, `C-BTN-03`, `D-ROW-02B`, `E-CARD-04`, `E-BTN-04`, `F-SUMMARY-01`, `F-BTN-00`, `G-ROW-02B`, and `G-BTN-03` | `{source_paths}` | UIREF-001, UIREF-002, UIREF-003, UIREF-004, UIREF-005, UIREF-006 | {proof_target}; {option_note} | Later implementation-match proof must compare actual app screenshots/video against this artifact, explain material differences, and route USER approval when required. |"
            )
    return "\n".join(rows)


def _write_packet_files(options: list[RenderOption]) -> None:
    options_table = _options_table(options)
    decision_options_table = _decision_options_table(options)
    annotation_table = _annotation_manifest_table(options)
    image_relevance_table = _image_relevance_manifest_table(options)
    draft_template_table = _draft_template_manifest_table(options)
    artifact_to_surface_table = _artifact_to_surface_ledger_table(options)
    _write_text(
        "START_HERE.md",
        """
# FAM-007 Visual Acceptance Target Packet

Primary review file: `USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md`

Current gate: branch-local UI/UX Visual Acceptance Target review.

Purpose: review a branch-local process that requires rendered visual targets before future visible UI/UX implementation. A visual target is a planning guide/template candidate, not final implemented product truth by itself. This packet does not accept H1/LV, USER UTS, PR Readiness, PR creation, merge, release, or runtime/provider/private/cache/memory/download/packaging work.

Review order:

1. Open the primary USER Review file.
2. For each option, inspect the primary clean focused render and its primary annotated focused render under `Review Aids/Render Media`.
3. Use `Review Aids/IMAGE_RELEVANCE_MANIFEST.md` to see why each included image is present in this final USER decision packet.
4. Use `Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md` to distinguish actual-runtime baseline media from real rendered draft-window/template media. Options B through G are rendered from branch-local HTML/CSS templates through PySide6 QWebEngine; they are not freehand static concept drawings.
5. Use the visible annotation IDs in the annotated focused renders for feedback, such as `D-ROW-02B`, `D-CARD-03`, or `D-BTN-03`.
6. Use `Review Aids/ANNOTATION_MANIFEST.md` and `Review Aids/ELEMENT_LEGENDS.md` to map every visible ID to the exact visual region, marker style, color cue, non-color cue, target label, and purpose.
7. Use `Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md` to map every artifact to the visible surface, element group, source/code path, UIREF owner, and future implementation comparison use.
8. Use `Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md` and `Review Aids/CAVEAT_LEDGER.md` before accepting with caveats or claiming implementation match.
9. Use the Visual Selection Ledger template to accept, reject, combine, or revise specific options and element IDs.
10. Read `Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md` before deciding. Clean enough is not the acceptance standard; the standard is USER-selected visual direction after meaningful compliant option exploration.
11. Review the Draft Branch Visual Acceptance Target. It remains a branch-local guide until USER accepts or revises it, and implementation still requires code-to-visual proof and later review where source truth requires it.

Annotation ID Boundary: annotation IDs are USER review references for this packet. They do not become source-truth implementation IDs unless a later source-truth owner explicitly promotes them.

Image Scope Rule: this final USER review packet is curated for decision clarity. It includes primary clean focused plus annotated focused render pairs for every option, preserves clean and annotated render media together, and includes secondary desktop/context images where useful for footprint judgment. Repair-cycle/debug evidence belongs in explicitly labeled repair packets or helper output, not in this final USER decision path.

Visual Acceptance Exploration Loop: if USER does not accept the packet's recommendation or current option set, the next cycle must generate new, revised, or combined real NDAI draft-window options. Near-duplicate variants with label-only changes are rejected. Each new option must differ materially in at least one meaningful dimension such as visual grammar, layout, UX flow, grouping, row/info grammar, density, hierarchy, doorway/workspace balance, action placement, state visibility, or child/domain routing.
""",
    )
    _write_text(
        "USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md",
        f"""
# FAM-007 Visual Acceptance Target Review

Verdict requested: accept, revise, reject, or hold this branch-local Visual Acceptance Target guide process.

## What This Packet Does

This packet creates a current-branch visual target guide process for FAM-007 visible UI/UX work. Future visible UI/UX implementation on this branch should not proceed from prose alone. It should first have a rendered visual target substantial enough to judge scale, footprint, spacing, density, hierarchy, controls, state behavior, resize behavior, copy, and relation to accepted Nexus references.

Visual Target Boundary: a USER-accepted visual target is a branch-local guide, comparator, template candidate, or expectation-alignment artifact. It should be as close to the intended product result as practical, but it is not final implemented product truth by itself. Final implementation still requires source-truth reconciliation, code-to-visual proof, validation, and USER review where the current phase requires it.

Image Scope Boundary: this final USER review packet is curated for the current decision. Included images are limited to clean option renders, annotated option renders, and minimal desktop/context renders needed to compare, select, accept, reject, or revise the visual target. Repair/debug proof dumps are intentionally excluded from the primary USER decision packet.

Primary Image Pairing: each option includes one primary clean focused render and one primary annotated focused render. Use the clean render to judge the visual target without overlays. Use the annotated render to cite exact element/group IDs in feedback, such as `D-ROW-01B`, `D-CARD-02`, `D-BTN-03`, or `A-STATUS-01`.

Annotation ID Boundary: annotation IDs are review references for this packet only. They help the USER point to rows, cards, buttons, status strips, and element groups. They are not source-truth implementation IDs unless later source truth explicitly promotes them.

Implementation Difference Boundary: actual implementation may differ from the accepted visual target only with source-truth-grounded explanation. Material visual differences require USER approval or a recorded source-truth-routed justification before implementation-match claims. Helper PASS, screenshot existence, "closer", "better", or packet parity cannot prove implementation match.

Caveat Boundary: USER may accept a visual target with caveats, but caveat acceptance only records required follow-up, deferred elements, source-truth reconciliation needs, and future proof obligations. It never accepts H1/LV, USER UTS, PR Readiness, PR creation, merge, release, runtime mutation, or provider/model/private/cache/memory/download/packaging behavior.

Governance Candidate Boundary: this packet records a proposed `UI/UX Workstream Exit Acceptance Gate` because FAM-007 and FAM-006 showed the same false-green risk. That gate is a candidate for a future Governance/FAM-002/UIREF carrier. This FAM-007 pass does not mutate global phase governance or promote the candidate as binding repo-wide law.

## Visual Acceptance Exploration Loop

Rule ID: `VISUAL_ACCEPTANCE_EXPLORATION_LOOP`

Clean enough is not the acceptance standard. The standard is USER-selected visual direction after meaningful compliant option exploration.

Packet validation proves completeness/currentness only; it does not prove USER acceptance, USER preference, runtime implementation match, H1/LV acceptance, or product readiness.

If USER does not accept the current recommendation or option set, the next visual acceptance cycle must generate new, revised, or combined real NDAI draft-window options. Near-duplicate options with label-only changes are rejected. Each new option must materially differ in at least one meaningful dimension: visual grammar, layout, UX flow, grouping, row/info grammar, density, hierarchy, doorway/workspace balance, action placement, state visibility, or child/domain routing.

Each cycle must record retained traits, rejected traits, new territory, and why the next options materially differ from the prior packet while remaining source-truth, Vision, UIREF, and FAM compliant.

Real Draft Window Requirement: options must look and read like believable NDAI product windows, not rough concepts, generic placeholders, diagram panels, static concept drawings, or status-debug boards. Current draft options must be produced from rendered draft-window/template sources or actual runtime screenshots. Real FAM-007 product language is allowed where source truth permits it; deterministic information appears only where it helps the USER choose the direction.

## Current Branch Visual Impact Classification

Current branch classification includes `MATERIAL_UI_UX_CHANGE`, `EXISTING_SURFACE_LAYOUT_CHANGE`, `NEW_SURFACE_OR_WINDOW`, `NEW_CONTROL_CLUSTER`, `SETTINGS_OR_IA_CHANGE`, `STATUS_ERROR_OR_EMPTY_STATE_CHANGE`, `VISUAL_SYSTEM_ADOPTION`, `USER_REPORTED_VISUAL_FAILURE`, and `FALSE_GREEN_VISUAL_PROOF_FAILURE`.

Any future visible UI/UX change on this branch needs a rendered visual target before product/runtime UI implementation, unless source truth records a narrow exception.

## Render Authority Levels

1. `Concept Render`: brainstorming only, not source truth.
2. `Design Candidate Render`: USER selection artifact, substantial and labeled.
3. `Visual Acceptance Target`: USER-accepted branch-local visual guide / expectation target.
4. `Implementation Match Proof`: actual implementation screenshot or video proving the implementation matches the accepted target.

## Visual Options

{decision_options_table}

## Recommended Decision

Current-cycle recommendation: review `OPTION-G` first as the strongest refined draft target candidate for this cycle. It uses `OPTION-D / D2` as the primary current-behavior-aligned direction, keeps compact doorway/orientation behavior and row grammar inside grouped cards, and borrows only compatible `OPTION-E` polish such as production-window maturity, stronger spacing, cleaner hierarchy, and compact trust-strip refinement. It does not borrow `OPTION-E` Settings-card scope broadening and does not borrow `OPTION-F` layout-customization behavior.

Retained Comparison Context: `OPTION-A` remains actual current-runtime structure evidence, not acceptance. `OPTION-B` remains compact grouping reference. `OPTION-C` remains a rejected-risk boundary because it trends toward larger workspace/report/status-monitor mass. `OPTION-D / D2` remains the strongest previous row-grammar doorway candidate and the primary behavior basis for `OPTION-G`, not USER-accepted final direction. `OPTION-E` remains a polish/reference candidate, not the primary target. `OPTION-F` remains future-layout evidence only.

Option D / D2 Boundary: the attached old accepted screenshot is a visual grammar reference, not a literal target and not source truth. `OPTION-D` is a branch-local candidate render and draft target basis only; it does not prove current runtime implementation, approve product/runtime UI mutation, or promote a global template.

Option E Boundary: `OPTION-E` is retained for USER review as the current-cycle polished production doorway reference candidate. It provides selective polish input for `OPTION-G`, but it is not the primary recommendation, not USER acceptance, not runtime implementation proof, and not a global template.

Option G Boundary: `OPTION-G` is the recommended current-cycle D/E hybrid target basis and D-primary/E-polish refinement. It is primarily Option D behavior and row grammar, selectively borrows Option E visual maturity, rejects Settings-card scope broadening, excludes Option F layout-customization behavior, and remains visual/template evidence only. It is not USER acceptance, not runtime implementation proof, not active settings behavior, and not a global template.

Option F Boundary: `OPTION-F` is retained as a future candidate, possible USER-configurable layout arrangement pattern, and example only. It is not the current selected FAM-007 target and is subject to later source-truth owner approval. It should be selected only if the USER explicitly chooses the wider summary/action hierarchy over the grouped-card doorway grid. It is not runtime implementation, not active settings behavior, not persistence/schema approval, not drag/drop approval, and not global template promotion.

Option F Provenance: `OPTION-F` is preserved from seed packet `{OPTION_F_SEED_PACKET_PATH}` with SHA256 `{OPTION_F_SEED_PACKET_SHA256}`. Its exact active packet artifact paths are recorded in `Review Aids/FUTURE_LAYOUT_ARRANGEMENT_CANDIDATES.md` so this primary decision file does not bypass the curated manifests.

Option F Future Example: if a future approved parent-window customization control lets USER move Card 4 into Card 2 position, the arrangement model must deterministically reconcile visible order and numbering so the moved card becomes Card 2 and displaced/downstream cards renumber/reorder according to the approved policy. Future possible surfaces include AI Dashboard, HUD Dashboard, future parent windows, and Global Settings parent-window customization controls if later approved. Future owners before implementation are: `{OPTION_F_FUTURE_OWNER_ROUTE}`.

Anti-Regression Boundary: the AI Dashboard / AI Control Center top-level surface must remain a compact doorway/orientation surface. Row grammar belongs inside grouped doorway cards and focused child/detail surfaces; it must not regress into twelve separate top-level status cards, a status monitor, a debugger surface, or a long report body.

Recommendation Boundary: `OPTION-G` is recommended as a draft target basis, not as proof that the current runtime implementation is accepted or complete. If USER accepts `OPTION-G`, `OPTION-D`, `OPTION-E`, `OPTION-F` as future-only context, a combination, or a revised direction, later implementation-match proof must still compare actual app evidence against the accepted target and classify any material differences.

## USER Decision Needed

Decide whether this branch-local process and draft target guide are accepted, revised, rejected, combined from multiple options, or held for future visible UI/UX changes on this branch.

This decision does not approve H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, cleanup, issue mutation, provider/model execution, prompt send, downloads, runtime cache behavior, memory/learning/personalization, private Developer/Owner setup, installer/shortcut/packaging execution, sibling/Governance mutation, imports, or v1.8.0 work.
""",
    )
    _write_text(
        "Review Aids/VISUAL_IMPACT_CLASSIFICATION.md",
        """
# Visual Impact Classification

| Classification | Result | Basis |
| --- | --- | --- |
| `NO_VISUAL_IMPACT` | `NO` | Current branch owns visible AI Dashboard / AI Control Center UI and proof surfaces. |
| `TEXT_ONLY_VISIBLE_CHANGE` | `YES` | Copy and labels were repaired repeatedly and remain visual-proof relevant. |
| `MINOR_EXISTING_UI_CHANGE` | `YES` | Window controls, status rows, scrollbars, and copy have visible impact. |
| `MATERIAL_UI_UX_CHANGE` | `YES` | AI Dashboard/category doorway and child-window model materially changed product IA. |
| `EXISTING_SURFACE_LAYOUT_CHANGE` | `YES` | AI Control Center layout moved from stacked content to doorway shell. |
| `NEW_SURFACE_OR_WINDOW` | `YES` | Child/domain windows were introduced and proved. |
| `NEW_CONTROL_CLUSTER` | `YES` | Compact NDAI window controls exist. |
| `SETTINGS_OR_IA_CHANGE` | `YES` | Settings route and IA model are future-gated but visible. |
| `STATUS_ERROR_OR_EMPTY_STATE_CHANGE` | `YES` | Provider/no-provider/blocked/capability states are visible. |
| `VISUAL_SYSTEM_ADOPTION` | `YES` | UIREF and FAM-002 visual grammar adoption are in scope. |
| `AMBIGUOUS_VISUAL_CONTRACT` | `YES` | Prior false-green loops show prose-only targets were not enough. |
| `USER_REPORTED_VISUAL_FAILURE` | `YES` | USER repeatedly rejected visual/IA mismatches. |
| `FALSE_GREEN_VISUAL_PROOF_FAILURE` | `YES` | Branch records multiple packet/proof false-green repairs. |
""",
    )
    _write_text("Review Aids/VISUAL_OPTIONS_PACKET.md", "# Visual Options Packet\n\n" + options_table)
    _write_text(
        "Review Aids/ELEMENT_LEGENDS.md",
        """
# Element Legends

Use this with `Review Aids/ANNOTATION_MANIFEST.md`. Each annotation uses color plus a non-color cue: a stable marker ID, outline shape, and pointer/callout line. Color alone is never the mapping proof.

ID Syntax: `<option letter>-<element group>-<ordinal or row suffix>`.

Examples:

| Example ID | Meaning |
| --- | --- |
| `A-STATUS-01` | Option A global status strip |
| `B-CARD-02` | Option B second card/group |
| `C-BTN-03` | Option C third button/action |
| `D-ROW-02B` | Option D second row in card 02 |
| `D-BTN-03` | Option D third button/action |
| `E-CARD-04` | Option E AI Settings handoff card |
| `F-SUMMARY-01` | Option F wide top summary zone |
| `G-ROW-02B` | Option G readiness report row in the refined D/E hybrid |
| `G-BTN-03` | Option G capabilities doorway button |

Element / Group Classes:

| Class | Meaning | Typical marker |
| --- | --- | --- |
| `HEADER` | title/header group | bracket |
| `CTRL` | window control cluster | circle |
| `STATUS` | compact AI/provider/trust status strip | bracket |
| `CARD` | grouped doorway card | box |
| `ROW` | specific row inside a grouped card | bracket |
| `BTN` | specific button/action | arrow plus box |
| `SCROLL` | scrollbar or overflow affordance | bracket |

Review Boundary: these IDs are USER review references for this packet. They do not become source-truth implementation IDs unless a later source-truth owner explicitly promotes them.

Example review language: `Accept G as the target basis`, `Keep G-CARD-02`, `change D-ROW-01B`, `borrow E spacing only`, `preserve F as future-only`, `revise F-SUMMARY-01 for later layout work`, or `reject C-CARD-03 as too workspace-like.`
""",
    )
    _write_text(
        "Review Aids/ANNOTATION_MANIFEST.md",
        f"""
# Annotation Manifest

Purpose: map every visible annotation ID in the annotated render files to an exact element/group type, target name, visual region, marker style, color cue, non-color cue, and purpose. The clean renders remain available beside the annotated renders so the USER can inspect the design without callout overlays.

Annotation Rule: every current visual target option must include option-specific review IDs, group-level IDs, element-level IDs, color plus a non-color cue such as marker ID, outline shape, bracket, arrow, box, circle, and pointer line. Annotations should identify the region without hiding critical UI content. IDs are review references only unless later source truth promotes them.

{annotation_table}
""",
    )
    _write_text(
        "Review Aids/IMAGE_RELEVANCE_MANIFEST.md",
        f"""
# Image Relevance Manifest

Purpose: list every image included in this final USER-review packet and why the USER needs it for the current visual target decision.

Packet Mode: `final USER decision packet`

Allowed image classifications in this packet: `USER decision image`, `required context image`, and `required annotation image`.

Excluded from this final USER decision packet: redundant proof dumps, duplicate state screenshots, helper-only evidence images, raw repair/debug evidence images, and images without a declared USER-decision purpose.

{image_relevance_table}
""",
    )
    _write_text(
        "Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md",
        f"""
# Draft Window Template Render Manifest

Purpose: prove that the selectable visual packet options are either actual runtime screenshots or real rendered draft-window/template screenshots. This file exists because previous packet cycles let static concept drawings appear equivalent to real draft windows.

Render Standard: Options B through G are generated as branch-local HTML/CSS draft-window templates and rendered through PySide6 QWebEngine before annotation overlays are added. Option A remains the actual current runtime baseline screenshot. Annotation overlays are review aids only and are not the clean render authority.

Non-Authority: PIL/ImageDraw is not the source for clean candidate media in this repaired packet. Static concept drawings and not freehand static concept drawings are acceptable only as rejected/historical/reference artifacts when explicitly labeled, not as selectable current draft-window options. PIL remains allowed only for annotation overlays and image-openability/geometry validation.

Runtime Boundary: this manifest does not mutate runtime UI, does not approve implementation, and does not create a reusable/global template. It repairs this branch-local packet process so USER review sees real draft-window/template media.

{draft_template_table}
""",
    )
    _write_text(
        "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
        f"""
# Artifact-To-Surface Ledger

Purpose: map each included visual artifact to the USER-facing surface, visible element groups, source/code path, UIREF owner, branch-local proof target, and future implementation comparison use.

Ledger Rule: a render artifact can become a USER-accepted visual target guide only after USER selection. It is not implementation proof, LV proof, UTS proof, PR Readiness proof, or final product truth by itself.

{artifact_to_surface_table}
""",
    )
    _write_text(
        "Review Aids/FUTURE_LAYOUT_ARRANGEMENT_CANDIDATES.md",
        f"""
# Future Layout Arrangement Candidates

Current Status: `FUTURE_CANDIDATE_EXAMPLE_ONLY`

Purpose: preserve layout-arrangement ideas that may be useful later without treating them as the current selected FAM-007 target, active settings behavior, runtime implementation, persistence/schema approval, drag/drop approval, or a global UIREF/FAM-002/Governance rule.

Seed / Source Packet: `{OPTION_F_SEED_PACKET_PATH}`

Seed / Source Packet SHA256: `{OPTION_F_SEED_PACKET_SHA256}`

| Candidate | Current disposition | Why retained | What must happen before use |
| --- | --- | --- | --- |
| `OPTION-F` | `FUTURE_LAYOUT_ARRANGEMENT_CANDIDATE`; future candidate; possible USER-configurable layout arrangement pattern; example only; subject to later source-truth owner approval | explores a wide top summary/action zone and horizontal domain lanes that could later support parent-window layout arrangements | USER must explicitly select or request this direction; the correct owner/carrier must approve settings, persistence/schema, drag/drop, reusable grammar, or cross-branch adoption before implementation; later proof must compare actual runtime UI against the accepted target |

## Option F Artifact Paths

| Artifact | Path | Boundary |
| --- | --- | --- |
| Focused clean render | `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_focused.png` | Visual/template candidate only |
| Desktop/context clean render | `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_desktop.png` | Visual/template candidate only |
| Focused annotated render | `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_focused_annotated.png` | Review callout aid only |
| Desktop/context annotated render | `Review Aids/Render Media/Option-F-wide-orientation-lanes/option-f_desktop_annotated.png` | Review callout aid only |
| Focused HTML/CSS draft template | `Review Aids/Draft Window Templates/Option-F-wide-orientation-lanes/option-f_focused_template.html` | Branch-local draft-window/template artifact only |
| Desktop/context HTML/CSS draft template | `Review Aids/Draft Window Templates/Option-F-wide-orientation-lanes/option-f_desktop_template.html` | Branch-local draft-window/template artifact only |

## What Option F Demonstrates

Option F demonstrates a possible USER-configurable layout arrangement pattern for parent-window/card ordering. It has a wide top summary/action zone, horizontal domain lanes, and a future layout model where card order can be reconciled deterministically if source truth later approves customization.

Deterministic reorder example: if a future approved parent-window customization control lets USER move Card 4 into Card 2 position, the arrangement model must deterministically reconcile visible order and numbering so the moved card becomes Card 2. The displaced/downstream cards must renumber/reorder consistently according to the approved layout policy.

Possible future surfaces: AI Dashboard, HUD Dashboard, future parent windows, and Global Settings parent-window customization controls if later approved.

Future owners before implementation: {OPTION_F_FUTURE_OWNER_ROUTE}.

## Non-Approvals

Boundary: Option F is a real rendered draft-window/template artifact in this packet, but it is not the current selected FAM-007 target. It is visual/template candidate only. {OPTION_F_NON_APPROVALS}. It does not authorize provider/model/private/cache/memory/download/packaging behavior, PR Readiness, PR creation, merge, release, issue mutation, or sibling/Governance mutation.
""",
    )
    _write_text(
        "Review Aids/STATE_COVERAGE_MATRIX.md",
        """
# State Coverage Matrix

| State | FAM-007 relevance | Current packet coverage | Later implementation-match requirement | Disposition |
| --- | --- | --- | --- | --- |
| default / focused | normal AI Dashboard / AI Control Center opening state | clean focused and desktop/context renders for every option | actual app focused screenshot/video must match accepted target or explain difference | `COVERED_FOR_TARGET_SELECTION` |
| hover | launcher buttons, window controls, Settings icon, category cards | not rendered in final decision packet to preserve image clarity | focused hover screenshot/video or USER waiver required before visual green if controls are touched | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| focus / keyboard focus | window controls and launch buttons | target requirement recorded | focus-visible proof or not-applicable rationale required before visual green | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| pressed / clicked | launchers, close/minimize, copy/report actions | target requirement recorded | ordered-frame proof or short video required when claiming interaction behavior | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| disabled / future-gated | provider/model/private/cache/memory/download/install/settings routes | target requirement recorded | disabled/future-gated visual state must be shown where a control exists | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
| provider/model unavailable | trust-boundary, no-provider, provider-visible-data none | compact status group identified by option-specific IDs such as `A-STATUS-01` or `D-STATUS-01` | backend-to-visual truth mapping and screenshot proof required | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
| generated/report state | local AI readiness report generated | not part of current final visual target images | actual report/focused surface proof required before H1/LV claim | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| copy-success / action-result | readiness report copy action | not rendered in final decision packet | success/confirmation proof required before claiming copy-result UI green | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| child/domain window open | AI Control Center / Diagnostics / Capabilities child surfaces | Option A carries current child-window proof context as candidate evidence | fresh actual opened-window proof required after target acceptance or runtime change | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| resized / minimum layout | top-level and child window geometry | current proof carried as historical branch evidence, not current acceptance proof | fresh resized/minimum screenshot or manifest proof required before LV green after changes | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| blocked / error / degraded | provider blocked, failed readiness check, unavailable capability | target requirement recorded | readable failure/recovery/blocked surface proof required | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
| empty / no-data | no report/result yet | target requirement recorded | empty-state proof required when the surface can appear without data | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
""",
    )
    _write_text(
        "Review Aids/STATE_COVERAGE_STORYBOARD.md",
        """
# FAM-007 State Coverage Storyboard / Plan

Purpose: identify which FAM-007 states must be rendered now, which are deferred to implementation proof, and which are future-gated.

Current Packet Mode: `visual target selection`, not runtime implementation proof.

| Storyboard Step | State / moment | Visible surface | Required proof later | Current disposition |
| --- | --- | --- | --- | --- |
| `SB-001` | Default AI Dashboard / Control Center doorway shell | top-level AI Dashboard / AI Control Center | accepted target render plus actual app match proof later | `RENDERED_FOR_TARGET_SELECTION` |
| `SB-002` | Hover over category launcher | AI Dashboard category card button | focused screenshot or video showing hover grammar | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-003` | Focus-visible launcher / window control | keyboard or focus state | screenshot/video or accessibility proof | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-004` | Pressed/clicked launcher opens child/domain window | category launcher path | ordered frames or short video with real click path | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-005` | Disabled or future-gated provider/model/private/cache/memory/download action | status, settings, capability doorway | screenshot proving disabled/future-gated state and truthful copy | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
| `SB-006` | Provider/model unavailable / no-provider configured | compact trust/status area | backend-to-visual truth mapping plus visual proof | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
| `SB-007` | Local readiness report generated | diagnostics/readiness child surface | actual generated report visual proof | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-008` | Copy-success or action-result state | readiness/report action | visual confirmation or state proof | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-009` | Child/domain window open and positioned | AI Control Center / Diagnostics / Capabilities | full desktop/context screenshot and focused window proof | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-010` | Resized / minimum supported layout | top-level or child windows | resized/minimum screenshot or manifest proof | `DEFERRED_TO_IMPLEMENTATION_PROOF` |
| `SB-011` | Empty / no-data state | readiness/report surface before generation | screenshot of empty state with readable guidance | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
| `SB-012` | Error / blocked / degraded state | diagnostics/status/recovery surface | screenshot showing recovery guidance and trust boundary | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |

Storyboard Rule: if a later pass claims visual green for one of these states, it must include actual app evidence or a USER-approved waiver. This current packet records the plan and target-selection basis only.
""",
    )
    _write_text(
        "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
        """
# Implementation Difference / Material-Deviation Rule

Rule Status: `BRANCH_LOCAL_VISUAL_TARGET_RULE`

Accepted visual targets are high-fidelity guides/templates/comparators for implementation alignment. They are not guaranteed final screenshots and are not final product truth by themselves.

Actual implementation may differ from the accepted visual target only when the difference is source-truth-grounded, technically necessary, or USER-approved.

Material visual differences require USER approval or a recorded source-truth-routed justification before implementation-match claims.

Material visual differences require one of these dispositions before implementation-match can be claimed:

| Difference class | Examples | Required disposition |
| --- | --- | --- |
| `MINOR_NON_MATERIAL` | tiny antialiasing, OS font rasterization, one-pixel layout tolerance | record in implementation-match proof |
| `SOURCE_TRUTH_GROUNDED` | UIREF/FAM/source-truth requirement conflicts with target detail | cite source truth and compare visually |
| `TECHNICAL_RUNTIME_CONSTRAINT` | runtime size/monitor behavior prevents exact target shape | explain constraint and provide actual proof |
| `USER_APPROVAL_REQUIRED` | layout hierarchy, surface purpose, button/state behavior, copy meaning, visible grouping, window chrome, state handling, or target option changes | get USER approval or route a revised target packet |
| `BLOCKER` | helper PASS, screenshot existence, "closer", "better", packet parity, or marker presence used as proof without visual comparison | stop; cannot claim implementation match |

Implementation-match proof must compare actual app screenshots/video against the accepted target and classify every material difference. Helper PASS, screenshot existence, "closer", "better", or packet parity cannot prove implementation match.
""",
    )
    _write_text(
        "Review Aids/CAVEAT_LEDGER.md",
        """
# Caveat Ledger

Purpose: support USER acceptance with caveats without turning caveats into phase acceptance or runtime approval.

Current Caveat State: `NONE_RECORDED_YET`

| Caveat ID | USER caveat / condition | Affected option or element | Required follow-up | Deferred element / state | Source-truth reconciliation needed | Future proof obligation | Gate impact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CAV-001` | None recorded yet | none | none | none | none | none | no acceptance until USER records decision |

Caveat Rule: USER may accept a visual target with caveats, but caveat acceptance only records required follow-up, deferred elements, source-truth reconciliation needs, and future proof obligations.

Caveat Boundary: caveat acceptance does not approve H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, runtime mutation, provider/model execution, prompt send, downloads, runtime cache behavior, memory/learning/personalization, private Developer/Owner setup, installer/shortcut/packaging execution, sibling/Governance mutation, imports, or v1.8.0 work.
""",
    )
    _write_text(
        "Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md",
        """
# Visual Acceptance Exploration Loop

Rule ID: `VISUAL_ACCEPTANCE_EXPLORATION_LOOP`

Purpose: keep FAM-007 visual acceptance as a USER-guided exploration and refinement loop until the USER selects or waives a visual direction.

## Acceptance Standard

Clean enough is not the acceptance standard.

The acceptance standard is USER-selected visual direction after meaningful compliant option exploration.

Packet validation proves completeness/currentness only. It does not prove USER acceptance, USER preference, runtime implementation match, H1/LV acceptance, Live Validation acceptance, UTS acceptance, PR Readiness, or product readiness.

Codex recommendations, ChatGPT review, helper PASS, screenshot existence, packet parity, attractive renders, or the cleanest available option cannot become USER acceptance.

## Variant Generation Rule

If USER does not accept the current target or option set, the next visual acceptance cycle must generate new, revised, or combined options.

Near-duplicates with label-only changes are rejected.

Each new or revised option must materially differ in at least one meaningful dimension:

| Dimension | Example of meaningful difference |
| --- | --- |
| visual grammar | different treatment of header, cards, dividers, row grammar, or control grouping |
| layout | different footprint, columns, card rhythm, or section arrangement |
| UX flow | different route from top-level doorway to child/domain/focused surface |
| grouping | different category grouping or subsystem clustering |
| row/info grammar | different way labels, values, summaries, and state rows are displayed |
| density | materially different information density without becoming clutter |
| hierarchy | different title, summary, card, or action emphasis |
| doorway/workspace balance | different split between compact orientation and deeper workspace surfaces |
| action placement | materially different placement, grouping, or priority of buttons and launchers |
| state visibility | different visibility model for provider, blocked, empty, disabled, success, or error states |
| child/domain routing | different route to AI Control Center, Diagnostics, Capabilities, Settings, or later surfaces |

All variants must remain source-truth, Project Vision, Product Experience Contract, UIREF, FAM-002, Family Vision, and FAM-007 FFV compliant.

## Retained / Rejected Traits Ledger

| Cycle | Source option / evidence | Retained traits | Rejected traits | New territory to explore if USER rejects | Material difference proof |
| --- | --- | --- | --- | --- | --- |
| `VAT-CYCLE-20260624-01` | `OPTION-A` current implementation direction | source-truth product structure, real category launcher labels, child/domain window model, compact Dashboard doorway concept | current runtime shape is not accepted by itself; can be too bound to existing implementation; cannot substitute for USER-selected target | keep current route truth while exploring stronger visual grammar and better doorway hierarchy | differs from pure current-runtime proof by adding design-candidate comparison and annotation IDs |
| `VAT-CYCLE-20260624-01` | `OPTION-B` compact grouping direction | compact spacing, directory rhythm, simple grouped cards | weaker row/info grammar; less mature as a product window | combine compact rhythm with stronger accepted row grammar | differs from Option A in density and grouping rhythm |
| `VAT-CYCLE-20260624-01` | `OPTION-C` workspace/status-risk boundary | useful negative comparator for what not to regress into | status-monitor/debugger/workspace sprawl; long detail at top level; too much report body | avoid twelve-card/status-monitor/debugger top-level patterns | differs by being retained as rejected-risk evidence, not a target |
| `VAT-CYCLE-20260624-01` | accepted old AI Control Center visual reference | strong header, compact status strip, numbered cards, row-based label/value grammar, truthful product feel | old surface is not a literal target, not source truth by itself, and does not carry current IA alone | apply its grammar inside grouped doorway cards and focused surfaces | differs by carrying visual grammar without renaming or reverting IA |
| `VAT-CYCLE-20260624-01` | `OPTION-D / D2` mature row-grammar doorway candidate | hybrid of source-truth doorway IA, compact grouping, old ACC row grammar, precise element IDs, real draft-window posture | still pending USER acceptance; not implementation proof; not global template | if rejected, next cycle must produce materially new variants, not label-only D copies | differs by adding row-level/card-level/status/action IDs and mature draft window shape |
| `VAT-CYCLE-20260624-02` | `OPTION-E` polished production doorway candidate | D/D2 row grammar, compact trust strip, grouped doorway card discipline, source-truth AI Dashboard / AI Control Center IA | avoids treating D as accepted; avoids status-monitor sprawl; avoids label-only D copy | two-by-two grouped-card grid, AI Settings handoff, stronger production-window polish, clearer domain launchers | materially differs from D by changing card rhythm, hierarchy, action placement, grouped system density, and settings handoff |
| `VAT-CYCLE-20260624-02` | `OPTION-F` wide orientation lanes candidate | compact trust truth, domain doorway purpose, category launch behavior, no-provider/provider-blocked boundaries | rejects vertical-row dominance and explores whether a wider summary/action model reads better; not current selected target; not runtime/settings/schema/drag-drop approval | wide top summary/action zone, horizontal domain lanes, fewer vertical rows, alternate scan path, and future candidate / possible USER-configurable layout arrangement pattern example only | materially differs from D/E by changing footprint, hierarchy, card flow, summary emphasis, action priority, and future parent-window arrangement model |
| `VAT-CYCLE-20260624-03` | `OPTION-G` refined D/E current-target candidate | Option D behavior alignment, compact doorway/orientation, grouped cards, row grammar inside cards, provider/model/data truth, and selected Option E maturity/spacing/hierarchy polish | rejects Option E Settings-card scope broadening; rejects Option F layout-customization behavior for the current target; rejects workspace/report/status-monitor drift | recommended current-cycle target basis: a D-primary/E-polish hybrid that remains compact, useful, and implementation-guidance ready without approving runtime UI | materially differs from D by adding selective E production polish and differs from E by removing the Settings-card broadening and returning to the D behavioral model |

## Real Draft Window Requirement

Every option in a USER-review visual target packet must be a believable NDAI draft window. It must be inspectable like a real product surface, not a rough concept, generic placeholder, diagram panel, static concept drawings, debug dashboard, or proof-only screen.

Real FAM-007 product language is allowed where source truth permits it. Deterministic information should appear only where it helps the USER choose the visual direction or understand trust boundaries.

## Anti-Regression Boundary

The packet must preserve these boundaries unless source truth and USER approval change them:

- no twelve-card, status-monitor, or debugger sprawl
- AI Dashboard remains a compact doorway/orientation surface
- row grammar belongs inside grouped doorway cards or focused child/detail surfaces, not as endless top-level status cards
- long reports, diagnostics, setup flows, logs, selectors, provider internals, capability details, memory/cache/private setup, and long workflows route behind category doorways, focused surfaces, child/domain surfaces, or future-gated placeholders

## Governance Boundary

This is a branch-local FAM-007 packet/process repair. A repo-wide Visual Acceptance Exploration Loop belongs to a later Governance/FAM-002/UIREF/reusable-helper carrier after USER approval. This packet records that governance candidate but does not mutate Governance, FAM-002, UIREF, runtime UI, sibling worktrees, issues, PRs, merges, releases, provider/model/private/cache/memory/download/packaging behavior, imports, or v1.8.0 work.
""",
    )
    _write_text(
        "Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md",
        f"# Visual Selection Ledger Template\n\n| Decision ID | Cycle | Surface | Option ID | Element ID | Accepted / Rejected / Combine / Revise | Retained Traits | Rejected Traits | New Territory Requested | Material Difference Required Next | USER Notes | Source-Truth Impact | Branch-Local Vs Durable Design Principle | Implementation Requirement | Proof Requirement | Future Reuse Note |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| `VSL-001` | `VAT-CYCLE-20260624-03` | AI Dashboard / AI Control Center | `OPTION-G` | `G-HEADER-01`; `G-STATUS-01`; `G-CARD-02`; `G-ROW-02B`; `G-BTN-03` |  | Option D behavior, grouped cards, row grammar; selective Option E production polish | Option E Settings-card scope broadening; Option F layout-customization behavior; workspace/report/status-monitor drift | USER may accept G, revise G by element ID, combine D/E traits differently, or request a new cycle | any next option must materially differ from G, not label-only copy |  | branch-local visual target only unless source truth later promotes | branch-local now; durable design principle only after correct owner approval | no runtime implementation in this packet | later actual app screenshots/video plus implementation-difference ledger | candidate source specimen only after USER selection |\n| `VSL-OPTION-F-CANDIDATE` | `VAT-CYCLE-20260624-02` | AI Dashboard / possible future parent windows | `OPTION-F` | `F-SUMMARY-01`; `F-CARD-02`; `F-BTN-00` | Future candidate/example only unless USER later selects | wide top summary/action zone; horizontal domain lanes; deterministic parent-window arrangement concept | not current selected target; not runtime/settings/schema/drag-drop approval | possible USER-configurable layout arrangement pattern for parent windows | if later approved, card movement must deterministically renumber/reorder visible cards | seed packet `{OPTION_F_SEED_PACKET_PATH}` sha256 `{OPTION_F_SEED_PACKET_SHA256}` | requires FAM-003/FAM-006/FAM-002/UIREF/Governance owner routing before implementation | branch-local candidate evidence now; durable design principle only after correct owner approval | no implementation in this packet | later actual runtime screenshots/video plus settings/schema/proof if approved | preserve as example only; subject to later source-truth owner approval |"
    )
    _write_text(
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        f"""
# Draft Branch Visual Acceptance Target

Target ID: `FAM007-VAT-001`

Target Status: `DRAFT`

Target Boundary: `Branch-local guide/template candidate only; not final implemented product truth by itself.`

Recommended Draft Basis: `OPTION-G pending USER selection; OPTION-D / D2 is the primary behavior basis; OPTION-E is polish/reference only; OPTION-F is future-layout evidence only`

Option G Recommended Target Basis: `OPTION-G is a refined D/E hybrid: Option D behavior and row grammar first, selective Option E production maturity/spacing/hierarchy polish second, no Option E Settings-card scope broadening, and no Option F layout-customization behavior. It is visual/template evidence only, not runtime implementation proof.`

Option F Preservation: `OPTION-F is a future candidate, possible USER-configurable layout arrangement pattern, and example only. It is preserved from seed packet {OPTION_F_SEED_PACKET_PATH} SHA256 {OPTION_F_SEED_PACKET_SHA256}. It is not the current selected target, not runtime implementation, not active settings behavior, not persistence/schema approval, not drag/drop approval, not cross-FAM adoption approval, and not global template promotion. Later implementation would require owner routing through {OPTION_F_FUTURE_OWNER_ROUTE}.`

Option F Deterministic Arrangement Example: `If a future approved parent-window customization control lets USER move Card 4 into Card 2 position, the arrangement model must deterministically reconcile visible order and numbering so the moved card becomes Card 2 and displaced/downstream cards renumber/reorder according to the approved policy.`

Selected Option(s): `Pending USER selection`

Surface Purpose: AI Dashboard / AI Control Center should be a compact top-level AI orientation and control-entry doorway. It should tell the USER what AI exists, what state it is in, what is safe or blocked, and where to go for grouped AI subsystems.

Footprint Class: `DOORWAY_SHELL`

Default Dimensions: current implementation proof carries 570x610 dashboard context; future accepted target may revise dimensions only with render proof.

Resize Behavior: product windows must declare resizable/fixed behavior and prove move/resize or not-applicable reason.

State Matrix: default, hover, focus, pressed, disabled, empty/no-data, blocked/error, success/complete, and resized/fixed-size proof must be classified.

Copy Rules: copy must be truthful, compact, user-readable, and must not imply provider/model/cache/memory/download/private setup execution.

Spacing / Density Rules: top-level content stays compact, orienting, trust-critical, or navigational. Long report bodies and setup/detail flows go behind focused surfaces.

Row Grammar Rule: row-based label/value grammar from the attached old accepted AI Control Center image is a visual grammar reference for grouped cards and focused child/detail surfaces. It is not a literal target, not source truth by itself, and must not expand the top-level AI Dashboard into a status monitor, debugger, or long report body.

Button / Control Rules: same-purpose buttons and window controls consume UIREF-002 and UIREF-003 unless a source-truth exception is recorded.

Status / Error / Empty Rules: provider-visible data, no-provider, blocked install intent, and future-gated private/setup states must map to backend truth.

Accepted Reference Surfaces: UIREF-001 through UIREF-006; current FAM-007 actual runtime proof is a branch-local candidate, not global template promotion.

Implementation Constraints: no future visible UI/UX implementation on this branch should proceed without USER_ACCEPTED target guide or source-truth-governed exception. Final implementation still requires code-to-visual proof, validation, and USER review where source truth requires it.

Material Difference Rule: actual implementation may differ from the accepted visual target only with source-truth-grounded explanation. Material visual differences require USER approval or recorded source-truth-routed justification before implementation-match claims.

Caveat Handling: USER may accept this draft target with caveats; caveats must be recorded in `Review Aids/CAVEAT_LEDGER.md` and carried into later implementation-match proof.

Proof Requirements: implementation-match screenshots/video, focused element proof, full desktop/context proof, artifact-to-surface trace, state coverage, and code-to-visual trace.

LV Gating Rule: Live Validation cannot claim UI green by helper output, screenshot existence, or marker presence alone.
""",
    )
    _write_text(
        "Review Aids/REJECTED_PATTERNS_LEDGER.md",
        """
# Rejected Patterns Ledger

Boundary: rejected patterns are candidate/comparator dispositions, not claims that a candidate was a failed final UI.

| Pattern ID | Rejected / deferred pattern | Source option or prior evidence | Product / UX risk | Governance risk | State / proof gap | UIREF / FAM boundary risk | Implementation-match risk | Future avoidance guidance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RPL-001` | oversized inner cards | prior AI Control Center repair loops; `OPTION-C` risk | consumes space and weakens doorway clarity | could reopen stacked-workspace IA failure | requires more scroll/resize states | risks drifting from compact doorway model | harder to compare as compact target | keep top-level cards compact and route detail behind child/domain surfaces |
| `RPL-002` | path-dominant or proof-token layout | prior readiness rows | reads like debug/proof instead of product | proof strings can be mistaken for source truth | report readability proof needed | conflicts with Product Experience Contract | implementation can pass helper while failing USER readability | show USER-readable trust copy first |
| `RPL-003` | verbose inline helper copy | prior stacked top-level report body | turns hub into workspace | blurs visual target with helper output | missing empty/error/report states | conflicts with AI Home / Control Foyer doorway model | target and actual implementation become non-comparable | keep top-level compact and route long reports behind child surfaces |
| `RPL-004` | action buried under status | prior stacked layout | USER cannot predict where to click | weakens deterministic action hierarchy | hover/focus/pressed proof becomes ambiguous | conflicts with UIREF-003 control grammar | visual match can hide behavior mismatch | keep one clear primary launcher/action visible per category |
| `RPL-005` | fake workspace for deferred feature | capability/provider/private placeholders | implies unavailable capability exists | could imply provider/model/private/cache/memory/download approval | disabled/future-gated state proof required | crosses FAM-008/private/provider boundaries | accepted target could overclaim runtime behavior | use compact future-gated/blocked copy and route future work to owning gates |
| `RPL-006` | marker-only or local-path proof | packet false-green incidents | USER cannot inspect real artifact | helper PASS could replace USER judgment | missing ZIP-byte media proof | violates packet proof owner boundaries | implementation-match claim lacks artifact of record | include real media in ZIP with annotation and relevance manifests |
| `RPL-007` | candidate treated as final product truth | previous false-green loops | USER may accept a direction as if runtime is done | bypasses H1/LV/UTS/PR gates | no actual app state proof | conflicts with UIREF-006 overclaim enforcement | implementation differences go unclassified | keep candidate, target, implementation proof, LV proof, UTS proof, and PR proof separate |
| `RPL-008` | twelve-card status monitor / debugger top-level regression | previous AI Control Center IA failures; `OPTION-C` risk boundary | top-level AI surface stops being a compact doorway/orientation surface | could bypass BP/IA ownership by turning grouped systems into one status board | state coverage explodes without focused child-surface proof | conflicts with AI Home / Control Foyer internal model and Product Experience Contract | visual target can look informative while failing navigation intent | keep AI Dashboard compact; place row grammar inside grouped doorway cards and route detailed reports behind focused surfaces |
| `RPL-009` | near-duplicate variant generation with label-only changes | visual acceptance exploration loops | creates busywork while failing USER request for meaningful design alternatives | validator could see a new option while USER sees the same design | no material-difference proof | conflicts with Product Experience Contract and USER critique loop | recommendation can become a stale preference trap | every new cycle must change at least one meaningful dimension and record retained/rejected traits |
| `RPL-010` | future-layout/customization candidate promoted into current target | Option F boundary preservation and current D/E refinement request | makes a future settings/customization concept look like approved current FAM-007 product behavior | could bypass FAM-003, FAM-006, FAM-002/UIREF, or Governance owner routing | no runtime/settings/schema/drag-drop proof or approval exists | conflicts with FAM-007 branch-local carrier boundary | implementation could silently adopt customization behavior without legal gate | keep Option F future-only; current target must use Option D behavior with compatible Option E polish unless USER separately approves a new carrier |
""",
    )
    _write_text("Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md", "# Reusable Design Recipe Template\n\nStatus: `TEMPLATE ONLY - fill after USER accepts a Visual Acceptance Target guide. This template is not final implemented product truth by itself.`\n\n| Field | Value |\n| --- | --- |\n| Accepted surface class |  |\n| Accepted footprint class |  |\n| Token values / dimensions |  |\n| Padding |  |\n| Spacing |  |\n| Button heights |  |\n| Font scale |  |\n| Status chip pattern |  |\n| Title/header grammar |  |\n| Resize behavior |  |\n| Copy pattern |  |\n| State pattern |  |\n| Accepted comparator references |  |\n| Rejected alternatives |  |\n| Future branch reuse notes |  |\n| Proof requirements |  |")
    _write_text("Review Aids/SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md", "# Source-Truth Conflict Classification\n\n| Candidate Decision | Classification | Disposition |\n| --- | --- | --- |\n| Require rendered visual target before future visible UI implementation on this branch | `BRANCH_LOCAL_VISUAL_DECISION` | legal branch-local process; Governance/global version is candidate only |\n| Treat current FAM-007 actual screenshot as branch-local target candidate | `NO_CONFLICT` | comparator seed only, not global template promotion |\n| Require FAM-002/UIREF comparison for same-class controls | `NO_CONFLICT` | matches Project Vision, FAM-002, UIREF-001 through UIREF-006 |\n| Record UI/UX Workstream Exit Acceptance Gate candidate | `GOVERNANCE_CANDIDATE_ONLY` | branch-local candidate wording and UDL row only; no global phase-governance mutation |\n| Record Visual Acceptance Exploration Loop rule | `BRANCH_LOCAL_VISUAL_DECISION_WITH_GOVERNANCE_CANDIDATE` | legal branch-local packet/helper repair; repo-wide version belongs to future Governance/FAM-002/UIREF/reusable-helper carrier |\n| Preserve Option F as future layout-arrangement candidate/example | `BRANCH_LOCAL_EVIDENCE_POINTER_WITH_OWNER_ROUTING` | legal to record seed packet, SHA, artifact paths, deterministic reorder example, possible future surfaces, and future owners; not legal here to approve runtime implementation, active settings behavior, persistence/schema, drag/drop, FAM-006 HUD adoption, FAM-002/UIREF template promotion, or global Governance rule |\n| Create Option G refined D/E target candidate | `BRANCH_LOCAL_VISUAL_DECISION` | legal branch-local packet/helper repair: D primary behavior alignment, E polish only where compatible, F future-only; no runtime UI mutation |\n| Promote AI Dashboard / AI Control Center as global gold standard | `GOVERNANCE_CANDIDATE_ONLY` | not done here |\n| Add reusable global helper/validator for all branches | `GOVERNANCE_CANDIDATE_ONLY` | not done here |\n| Implement product/runtime UI change in this pass | `USER_DECISION_REQUIRED` | not approved by this packet |")
    _write_text("Review Aids/GOVERNANCE_CANDIDATE_ONLY.md", "# Governance Candidate Only\n\nCandidate 1: create a global Visual Acceptance Target process for future Nexus visible UI/UX work.\n\nCandidate 2: create a global UI/UX Workstream Exit Acceptance Gate for branches that implement, materially repair, or materially change UI/UX.\n\nCandidate 3: create a global Visual Acceptance Exploration Loop rule for UI/UX target selection. The loop should say clean enough is not the acceptance standard; USER-selected visual direction after meaningful compliant option exploration is the standard; packet validation proves completeness/currentness only; rejected packets must generate materially different new, revised, or combined real draft-window options with retained traits, rejected traits, new territory, and no near-duplicate label-only variants.\n\nReason: FAM-007 and FAM-006 false-green loops show that implementation-first UI work and helper-green review can create repair loops. A global rule should require substantial rendered targets, annotated and clean render media, annotation manifests, element legends, state matrices, full desktop/context renders, rejected-pattern ledgers, reusable design recipes, implementation-match proof, retained/rejected-traits ledgers, variant distinctness proof, and explicit USER visual acceptance or waiver before visible UI work progresses past Workstream.\n\nTemplate Boundary: a global visual target process should say that accepted targets are guides/templates/comparators for implementation alignment, not final product truth by themselves.\n\nGate Boundary: a global UI/UX Workstream Exit Acceptance Gate should say that Packet Reviewability State, ChatGPT review, helper PASS, screenshot existence, visual-target acceptance, or packet parity cannot clear USER visual acceptance for an implemented UI/UX change.\n\nExploration Boundary: a global exploration loop should keep Codex recommendations as recommendations, not USER preference or acceptance, and should reject near-duplicate variants that do not explore meaningful new design territory.\n\nApproval Needed: USER-approved Governance/FAM-002/UIREF carrier after this branch-local process is reviewed. This FAM-007 pass does not mutate Governance, FAM-002, UIREF, or promote a global template.")
    _write_text(
        "Review Aids/UI_UX_WORKSTREAM_EXIT_GATE_CANDIDATE.md",
        """
# UI/UX Workstream Exit Acceptance Gate Candidate

Status: `GOVERNANCE_CANDIDATE_ONLY`

Legal Carrier Finding: this FAM-007 pass may repair branch-local packet/helper/external-state proof because it is the active visual-target carrier. A repo-wide phase-gate rule belongs to the phase-governance / FAM-002 / UIREF governance carrier unless source truth later admits this branch as the explicit global repair carrier. This packet therefore records the candidate and does not mutate `Docs/phase_governance.md`.

Candidate Rule Name: `UI/UX Workstream Exit Acceptance Gate`

Applicability: branches that implemented, materially repaired, or materially changed user-facing UI/UX, visual layout, interactive window behavior, child/domain window behavior, user-facing card/row/control grammar, or visual target implementation.

Non-Applicability: backend-only, validator-only, docs-only, or non-visible work unless the branch makes UI/UX claims.

Gate Placement: checked at Workstream exit before Hardening.

Required USER Gate State: one of `USER Accepted`, `USER Accepted With Caveats`, `USER Waived`, `USER Deferred With Explicit Source-Truth Boundary`, or `Not Applicable With Reason`.

Blocking States: `Pending`, `Rejected`, `Stale`, `Unproven`, `Packet Reviewability Only`, `ChatGPT Review Only`, `Helper PASS Only`, `Screenshot Existence Only`, `Visual Target Treated As Implementation Proof`, or `Implementation Difference Unrouted`.

Blocked Progression While Not Cleared: Hardening, Live Validation, PR Readiness, PR creation, merge, and release-facing progression.

Repair Loop: if USER rejects, requests revisions, or accepts with blocking caveats, remain in Workstream repair loop; regenerate target/packet/implementation comparison evidence; update UDL rows; close rows only with current proof; rerun validation; return to USER review.

Validator / Helper Impact: future global validators should check current branch UI/UX applicability, USER Gate State, packet acceptance versus reviewability, visual-target versus implementation-proof distinction, implementation-difference ledger, accepted-with-caveats ledger, stale visual packet status, and false-green fixture coverage.

Proposed Blocker Names: `UI/UX Acceptance Pending`, `UI/UX Acceptance Rejected`, `UI/UX Acceptance Stale`, `UI/UX Acceptance Evidence Missing`, `Visual Target Treated As Implementation Proof`, `Packet Reviewability Treated As USER Acceptance`, `ChatGPT Review Treated As USER Acceptance`, `Implementation Difference Unrouted`, and `UI/UX Workstream Exit Acceptance Missing`.

Exact USER Decision Needed For Global Adoption: approve a Governance/FAM-002/UIREF carrier to codify the UI/UX Workstream Exit Acceptance Gate, update validators/helpers/fixtures, and decide whether existing active UI-bearing branches must run RAR/adoption review against the new gate.
""",
    )
    _write_text("Review Aids/UDL_FALSE_GREEN_STATUS.md", "# UDL / False-Green Status\n\nCurrent branch has a Unified Defect Ledger and multiple false-green packet/proof repair receipts.\n\nThis visual target packet prevents another implementation-first loop by requiring rendered design candidate media, annotated and clean visual-to-legend mapping, full desktop/context render media, stable element IDs, state coverage, a draft target guide, rejected-pattern ledger, reusable design recipe template, curated decision-relevant packet images, packet media included in the ZIP, and an explicit Visual Acceptance Exploration Loop.\n\nUDL rows F7-UDL-019, F7-UDL-021, F7-UDL-022, F7-UDL-023, F7-UDL-024, F7-UDL-025, F7-UDL-026, F7-UDL-027, and F7-UDL-028 track annotation readability/bounds, final-packet image relevance, comparative-audit ledgers, the Option D / D2 row-grammar hybrid target candidate, the UI/UX Workstream Exit Acceptance Gate governance candidate, the Visual Acceptance Exploration Loop / variant-generation repair, real draft-window/template render repair, Option F future layout-arrangement candidate preservation, and Option G D-primary/E-polish target refinement. Option G is recommended as branch-local visual target evidence only. Option F is preserved as future candidate/example evidence only and does not approve runtime/settings/schema/drag-drop behavior. Existing known-bad packet defects remain preserved as historical false-green evidence.")
    _write_text("Review Aids/VALIDATION_SUMMARY.md", "# Packet Check Notes\n\nPacket-local checks are run by `dev/orin_fam007_visual_acceptance_target_packet.py --validate`.\n\nRequired checks include required files, exactly one primary USER review file, render media in the packet, image openability, focused and full desktop/context render media for each option, annotated renders for each option, annotation manifest mapping marker IDs to visual regions, annotation label/leader geometry in bounds, visible marker label text pixels inside each label box, image relevance manifest coverage for every included image, final USER-review image scope, element legend, state matrix, template-not-endstate wording, Visual Selection Ledger template, Draft Branch Visual Acceptance Target, Rejected Patterns Ledger, Reusable Design Recipe template, Visual Acceptance Exploration Loop, VAT-CYCLE-20260624-02, VAT-CYCLE-20260624-03, Option E, Option F, Option G, Option G D-primary/E-polish wording, Option G media/template artifacts, Option F seed packet path/SHA, Option F artifact paths, deterministic reorder example, future owner routing, non-approval boundaries, variant distinctness wording, retained/rejected traits, timestamped ZIP, and folder/ZIP parity.\n\nDetailed command results stay in Codex/helper output and final digest rather than in USER-facing text walls.")

    context_files = {
        "Source Truth Context/current_external_branch_state.md": BRANCH_STATE,
        "Source Truth Context/current_external_branch_plan.md": BRANCH_PLAN,
        "Source Truth Context/branch_record.md": REPO_ROOT / "Docs" / "branch_records" / "feature_fam_007_ai_control_center_readiness_diagnostics.md",
        "Source Truth Context/validation_helper_registry.md": REPO_ROOT / "Docs" / "validation_helper_registry.md",
        "Source Truth Context/ui_reference_catalog_index.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "index.md",
        "Source Truth Context/UIREF-001_top_level_window_frame.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-001_top_level_window_frame.md",
        "Source Truth Context/UIREF-002_window_control_cluster.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-002_window_control_cluster.md",
        "Source Truth Context/UIREF-003_control_state_and_selector_grammar.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-003_control_state_and_selector_grammar.md",
        "Source Truth Context/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-004_dialog_status_recovery_and_doorway_surfaces.md",
        "Source Truth Context/UIREF-005_design_token_and_shared_rule_baseline.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-005_design_token_and_shared_rule_baseline.md",
        "Source Truth Context/UIREF-006_negative_example_and_enforcement_contract.md": REPO_ROOT / "Docs" / "ui_reference_catalog" / "UIREF-006_negative_example_and_enforcement_contract.md",
    }
    if UDL_PATH.exists():
        context_files["Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md"] = UDL_PATH
    for relative, source in context_files.items():
        _copy_file(source, relative)


def _recovery_search_roots() -> list[Path]:
    return [
        USER_ROOT,
        Path(r"C:\$Recycle.Bin"),
        Path(r"D:\Nexus Desktop AI Data\Worktrees"),
        Path(r"C:\Nexus Desktop AI"),
        Path(r"C:\Users\anden\OneDrive\Desktop"),
        Path(r"C:\Users\anden\OneDrive\Documents"),
        Path(r"C:\Users\anden\OneDrive\Pictures"),
        Path(r"C:\Users\anden\Downloads"),
        Path(r"C:\Users\anden\Documents"),
        Path(r"C:\Users\anden\Desktop"),
        Path(r"C:\Users\anden\.codex\attachments"),
        Path(r"D:\Nexus Artifacts"),
        Path(r"D:\Nexus Repos"),
        Path(r"D:\Nexus Worktrees"),
        Path(r"D:\Nexus Dev ORIN"),
    ]


def _find_accepted_historical_packet() -> tuple[list[Path], list[str]]:
    matches: list[Path] = []
    searched: list[str] = []
    for root in _recovery_search_roots():
        if not root.exists():
            searched.append(f"{root} - missing root")
            continue
        searched.append(str(root))
        try:
            matches.extend(path for path in root.rglob(ACCEPTED_HISTORICAL_ZIP.name) if path.is_file())
        except (OSError, PermissionError) as exc:
            searched.append(f"{root} - search error: {exc}")
    unique = sorted({path.resolve() for path in matches})
    return unique, searched


def _copy_recovery_context() -> None:
    context_files = {
        "Source Truth Context/current_external_branch_state.md": BRANCH_STATE,
        "Source Truth Context/current_external_branch_plan.md": BRANCH_PLAN,
        "Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md": UDL_PATH,
        "Source Truth Context/branch_record.md": REPO_ROOT / "Docs" / "branch_records" / "feature_fam_007_ai_control_center_readiness_diagnostics.md",
        "Source Truth Context/validation_helper_registry.md": REPO_ROOT / "Docs" / "validation_helper_registry.md",
        "Source Truth Context/phase_governance.md": REPO_ROOT / "Docs" / "phase_governance.md",
    }
    for relative, source in context_files.items():
        if source.exists():
            _copy_file(source, relative)


def _write_recovery_packet_files(zip_path: Path, searched: list[str], matches: list[Path]) -> None:
    search_rows = "\n".join(f"| `{root}` | searched |" for root in searched)
    match_text = "\n".join(f"- `{match}`" for match in matches) if matches else "- None found."
    _write_text(
        "START_HERE.md",
        f"""
# FAM-007 Accepted-Historical Packet Recovery / Retention Blocker

Review Purpose: decide how to handle the missing accepted historical packet artifact.

Local USER Hub Folder: `C:\\Nexus USER\\FAM-007`

Review Order:

1. `USER Review/{RECOVERY_PRIMARY_REVIEW_FILE}`
2. `Review Aids/ACCEPTED_HISTORICAL_SEARCH_PROOF.md`
3. `Review Aids/ARTIFACT_DISPOSITION_OPTIONS.md`
4. `Source Truth Context/current_external_branch_state.md`
5. `Source Truth Context/current_external_branch_plan.md`
6. `Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md`

USER Decision This Packet Supports: provide/upload the missing accepted historical ZIP, approve a retention waiver, or keep the packet chain blocked until recovered.

Pending USER Decisions: accepted-historical artifact disposition only. H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, provider/model execution, downloads, cache, memory, private setup, packaging, sibling/Governance mutation, imports, and v1.8.0 remain blocked.
""",
    )
    _write_text(
        f"USER Review/{RECOVERY_PRIMARY_REVIEW_FILE}",
        f"""
# Accepted-Historical Packet Recovery / Retention Review

## Current Decision

Verdict For This Packet: `BLOCKER / USER DECISION REQUIRED`

Missing Accepted Historical Packet: `{ACCEPTED_HISTORICAL_ZIP}`

Current Recovery Packet: `{zip_path}`

## What Happened

What Happened: the active FAM-007 source truth recorded the accepted historical Workstream implementation / H1-LV proof packet as preserved evidence, but the local artifact is missing from the searched roots. Codex did not recover a copy and must not recreate or fake preservation.

## Why This Matters

Why It Matters: accepted-historical validation requires the original timestamped ZIP artifact as the immutable evidence record. UDL rows F7-UDL-016 and F7-UDL-017 rely on that artifact being available and byte-validated in accepted-historical mode.

## Current Disposition

Current Disposition: the Visual Acceptance Target packet chain is blocked on accepted-historical artifact disposition. The branch may not claim the accepted historical packet is preserved while the ZIP is missing.

## USER Options

USER Options:

| Option | Meaning | Result |
| --- | --- | --- |
| Provide / upload the missing ZIP | USER supplies the original `FAM-007-20260623-123429.zip` artifact. | Codex restores it to `C:\\Nexus USER`, validates accepted-historical mode, regenerates the Visual Acceptance Target packet, and resumes packet review. |
| Approve retention waiver | USER explicitly accepts that the local historical ZIP is unavailable and waives local retained-ZIP proof for this chain. | Codex records waiver wording in source truth/external state and regenerates the current packet without claiming local preservation. |
| Keep blocked | USER does not waive and cannot provide the ZIP. | Packet chain remains blocked until artifact recovery succeeds. |

Not Approved By This Packet: H1/LV acceptance, USER UTS acceptance, PR Readiness, PR creation, merge, release, unrelated cleanup, issue mutation, provider/model execution, prompt send, downloads, runtime cache behavior, memory/learning/personalization, private Developer/Owner setup, installer/shortcut/packaging execution, sibling/Governance mutation, imports, or v1.8.0 work.

## Exact USER Decision Supported

Suggested USER Decision Text:

`{_recovery_exact_user_decision_text(zip_path)}`
""",
    )
    _write_text(
        "Review Aids/ACCEPTED_HISTORICAL_SEARCH_PROOF.md",
        f"""
# Accepted-Historical Packet Search Proof

Target Filename: `{ACCEPTED_HISTORICAL_ZIP.name}`

Target Restore Path: `{ACCEPTED_HISTORICAL_ZIP}`

Search Result: `NOT RECOVERED`

Matches Found:

{match_text}

Searched Roots:

| Root | Result |
| --- | --- |
{search_rows}

Search Interpretation: no exact retained artifact was found. No same-packet copy can be validated without artifact bytes or a recorded matching SHA/source artifact.
""",
    )
    _write_text(
        "Review Aids/ARTIFACT_DISPOSITION_OPTIONS.md",
        """
# Artifact Disposition Options

| Disposition | Allowed Now | Notes |
| --- | --- | --- |
| Restore exact ZIP | Yes, if USER supplies or local search finds it | Must validate in accepted-historical mode after restore. |
| Mark recovered without ZIP bytes | No | Would fake preservation and reintroduce false-green risk. |
| Recreate ZIP from current folder | No | Would not be the accepted historical artifact. |
| Waive local retained-ZIP proof | USER decision required | Must be explicit and source-truth-routed. |
| Keep chain blocked | Yes | Safest default if the artifact cannot be recovered and USER does not waive. |
""",
    )
    _write_text(
        "Review Aids/PACKET_CHECK_NOTES.md",
        """
# Packet Check Notes

This packet is intentionally a blocker/decision packet. It should validate as a current USER review packet while preserving that the accepted historical ZIP is missing.

Required checks:

- exactly one primary USER review file
- timestamped ZIP
- folder/ZIP parity
- copied Source Truth Context says the accepted historical ZIP is missing, not preserved
- no H1/LV acceptance
- no USER UTS acceptance
- no wording that opens PR Readiness
- no PR creation approval
- no packet validation as USER acceptance
""",
    )
    _copy_recovery_context()


def generate_recovery_blocker() -> Path:
    zip_path = USER_ROOT / f"{WORKTREE_LABEL}-{_stamp()}.zip"
    matches, searched = _find_accepted_historical_packet()
    if matches:
        raise RuntimeError(f"Accepted historical packet was found and should be restored instead: {matches[0]}")
    _purge_packet_root()
    _update_external_state_for_recovery_packet(zip_path)
    _write_recovery_packet_files(zip_path, searched, matches)
    _create_zip(zip_path)
    return zip_path


def validate_recovery_blocker(packet_dir: Path = PACKET_DIR, zip_path: Path | None = None) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if zip_path is None:
        zips = sorted(USER_ROOT.glob(f"{WORKTREE_LABEL}-*.zip"), key=lambda path: path.stat().st_mtime, reverse=True)
        zip_path = zips[0] if zips else None
    if zip_path is None or not zip_path.exists():
        return False, ["Timestamped recovery ZIP missing"]
    primary = packet_dir / "USER Review" / RECOVERY_PRIMARY_REVIEW_FILE
    if not primary.exists():
        failures.append(f"Recovery primary review file missing: {RECOVERY_PRIMARY_REVIEW_FILE}")
    primary_files = list((packet_dir / "USER Review").glob("*.md")) if (packet_dir / "USER Review").exists() else []
    if len(primary_files) != 1:
        failures.append(f"Expected exactly one recovery primary USER review file; found {len(primary_files)}")
    with zipfile.ZipFile(zip_path, "r") as archive:
        zip_entries = {info.filename for info in archive.infolist() if not info.is_dir()}
        folder_entries = {path.relative_to(packet_dir).as_posix() for path in _packet_file_entries()}
        if folder_entries != zip_entries:
            failures.append("Recovery packet folder/ZIP parity failed")
        if f"USER Review/{RECOVERY_PRIMARY_REVIEW_FILE}" not in zip_entries:
            failures.append("Recovery ZIP missing primary review file")
        state_text = archive.read("Source Truth Context/current_external_branch_state.md").decode("utf-8")
        plan_text = archive.read("Source Truth Context/current_external_branch_plan.md").decode("utf-8")
        udl_text = archive.read("Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md").decode("utf-8")
        active_text = (
            _section(state_text, "## Next Legal Phase")
            + "\n"
            + _section(plan_text, "## Packet Review State")
            + "\n"
            + _section(plan_text, "## Next Legal Phase")
        )
        head = _git_value("rev-parse", "HEAD")
        source_head_pattern = re.compile(r"^Source Repo HEAD: `(.*?)`\r?$", re.MULTILINE)
        state_heads = source_head_pattern.findall(state_text)
        plan_heads = source_head_pattern.findall(plan_text)
        if not state_heads or state_heads[0] != head:
            failures.append("Recovery copied branch state Source Repo HEAD does not match live HEAD")
        if not plan_heads or plan_heads[0] != head:
            failures.append("Recovery copied branch plan Source Repo HEAD does not match live HEAD")
        if f"Current HEAD: `{head}`" not in udl_text:
            failures.append("Recovery copied UDL Current HEAD does not match live HEAD")
        if "Current HEAD Field Classification:" not in udl_text:
            failures.append("Recovery copied UDL does not classify Current HEAD currentness")
        if str(zip_path) not in active_text:
            failures.append("Recovery active copied context does not name final ZIP")
        if str(zip_path) not in udl_text:
            failures.append("Recovery copied UDL does not name final recovery packet")
        if udl_text.count("## F7-UDL-018 ") != 1:
            failures.append("Copied UDL must contain exactly one F7-UDL-018 heading")
        for required in ("MISSING", "not currently preserved", "recovery / retention blocker"):
            if required not in state_text and required not in plan_text:
                failures.append(f"Recovery copied context missing required blocker wording: {required}")
        forbidden = [
            "remains preserved as historical evidence",
            "I accept the FAM-007 Hardening H1 Green packet",
            "PR Readiness active",
            "PR creation approved",
            "packet validation is USER acceptance",
        ]
        for term in forbidden:
            if term in active_text:
                failures.append(f"Recovery active copied context contains forbidden wording: {term}")
        if "F7-UDL-018" not in udl_text or "BLOCKED_SOURCE_TRUTH" not in udl_text:
            failures.append("Copied UDL missing F7-UDL-018 blocked artifact row")
    return not failures, failures


def _create_zip(zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in _packet_file_entries():
            archive.write(path, path.relative_to(PACKET_DIR).as_posix())


def _box_in_bounds(box: tuple[int, ...], width: int, height: int) -> bool:
    return len(box) == 4 and 0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height


def _line_in_bounds(line: tuple[int, ...], width: int, height: int) -> bool:
    return len(line) == 4 and 0 <= line[0] <= width and 0 <= line[2] <= width and 0 <= line[1] <= height and 0 <= line[3] <= height


def _option_id_from_annotated_path(path: Path) -> str | None:
    normalized = path.as_posix().casefold()
    if "option-a" in normalized or "option_a" in normalized:
        return "OPTION-A"
    if "option-b" in normalized:
        return "OPTION-B"
    if "option-c" in normalized:
        return "OPTION-C"
    if "option-d" in normalized:
        return "OPTION-D"
    if "option-e" in normalized or "option_e" in normalized:
        return "OPTION-E"
    if "option-f" in normalized or "option_f" in normalized:
        return "OPTION-F"
    if "option-g" in normalized or "option_g" in normalized:
        return "OPTION-G"
    return None


def _validate_annotation_images(packet_dir: Path) -> list[str]:
    failures: list[str] = []
    annotated_images = sorted((packet_dir / "Review Aids" / "Render Media").rglob("*_annotated.png"))
    if len(annotated_images) < EXPECTED_ANNOTATED_IMAGE_COUNT:
        failures.append(f"Expected at least {EXPECTED_ANNOTATED_IMAGE_COUNT} annotated render images; found {len(annotated_images)}")
    for image_path in annotated_images:
        option_id = _option_id_from_annotated_path(image_path)
        if option_id is None:
            failures.append(f"Cannot infer option ID for annotated image: {image_path}")
            continue
        desktop = "desktop" in image_path.name.casefold()
        with Image.open(image_path) as image:
            rgb = image.convert("RGB")
        width, height = rgb.size
        base_width = width - ANNOTATION_LABEL_PANEL_WIDTH
        if base_width <= 0:
            failures.append(f"Annotated image missing annotation side panel width: {image_path}")
            continue
        specs = _annotation_specs(option_id, base_width, height, desktop=desktop)
        group_count = sum(1 for spec in specs if spec.element_type == "group")
        element_count = sum(1 for spec in specs if spec.element_type == "element")
        if group_count < 2:
            failures.append(f"Annotated image lacks group-level coverage for {option_id}: {image_path}")
        if element_count < 2:
            failures.append(f"Annotated image lacks element-level coverage for {option_id}: {image_path}")
        if option_id == "OPTION-D" and desktop is False:
            for required in ("D-ROW-01A", "D-ROW-01B", "D-ROW-02B", "D-BTN-03", "D-STATUS-01"):
                if required not in {spec.annotation_id for spec in specs}:
                    failures.append(f"Option D focused annotations missing required precise ID: {required}")
        if option_id == "OPTION-E" and desktop is False:
            for required in ("E-CARD-04", "E-BTN-04", "E-STATUS-01", "E-ROW-02B"):
                if required not in {spec.annotation_id for spec in specs}:
                    failures.append(f"Option E focused annotations missing required precise ID: {required}")
        if option_id == "OPTION-F" and desktop is False:
            for required in ("F-SUMMARY-01", "F-BTN-00", "F-CARD-03", "F-STATUS-01"):
                if required not in {spec.annotation_id for spec in specs}:
                    failures.append(f"Option F focused annotations missing required precise ID: {required}")
        if option_id == "OPTION-G" and desktop is False:
            for required in ("G-STATUS-01", "G-CARD-01", "G-ROW-02B", "G-BTN-03"):
                if required not in {spec.annotation_id for spec in specs}:
                    failures.append(f"Option G focused annotations missing required precise ID: {required}")
        for index, spec in enumerate(specs, start=1):
            marker_id = spec.annotation_id
            target_box = spec.region
            geometry = _callout_geometry(target_box, index, width)
            label_box = geometry["label_box"]
            leader_line = geometry["leader_line"]
            if not _box_in_bounds(target_box, width, height):
                failures.append(f"Annotation target box out of bounds for {marker_id} in {image_path}: {target_box} within {width}x{height}")
            if not _box_in_bounds(label_box, width, height):
                failures.append(f"Annotation label box out of bounds for {marker_id} in {image_path}: {label_box} within {width}x{height}")
            if not _line_in_bounds(leader_line, width, height):
                failures.append(f"Annotation leader line out of bounds for {marker_id} in {image_path}: {leader_line} within {width}x{height}")
            label_crop = rgb.crop(label_box)
            light_pixels = 0
            pixel_iter = label_crop.get_flattened_data() if hasattr(label_crop, "get_flattened_data") else label_crop.getdata()
            for red, green, blue in pixel_iter:
                if red > 210 and green > 220 and blue > 220:
                    light_pixels += 1
            if light_pixels < 12:
                failures.append(f"Annotation ID not visibly present in label box for {marker_id} in {image_path}")
    return failures


def _validate_image_relevance_manifest(packet_dir: Path) -> list[str]:
    failures: list[str] = []
    manifest = packet_dir / "Review Aids" / "IMAGE_RELEVANCE_MANIFEST.md"
    if not manifest.exists():
        return ["Image relevance manifest missing"]
    text = manifest.read_text(encoding="utf-8")
    allowed_classes = {
        "USER decision image",
        "required context image",
        "required annotation image",
    }
    image_paths = sorted(
        path.relative_to(packet_dir).as_posix()
        for path in packet_dir.rglob("*")
        if path.is_file() and path.suffix.casefold() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    )
    if len(image_paths) != EXPECTED_RENDER_IMAGE_COUNT:
        failures.append(f"Expected exactly {EXPECTED_RENDER_IMAGE_COUNT} curated final-packet images; found {len(image_paths)}")
    for relative in image_paths:
        if not relative.startswith("Review Aids/Render Media/"):
            failures.append(f"Final USER packet includes non-curated image outside Render Media: {relative}")
        if f"`{relative}`" not in text:
            failures.append(f"Image missing declared USER-decision purpose in IMAGE_RELEVANCE_MANIFEST.md: {relative}")
    for line in text.splitlines():
        if not line.startswith("| `Review Aids/Render Media/"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            failures.append(f"Malformed image relevance row: {line}")
            continue
        classification = cells[1]
        why_user_needs_it = cells[2]
        supported_decision = cells[3]
        if classification not in allowed_classes:
            failures.append(f"Image relevance row uses invalid final-packet classification {classification!r}: {line}")
        if not why_user_needs_it or not supported_decision:
            failures.append(f"Image relevance row missing USER purpose or supported decision: {line}")
    option_rows = {option_id: [] for option_id in OPTION_IDS}
    for relative in image_paths:
        option_id = _option_id_from_annotated_path(Path(relative)) or (
            "OPTION-A" if "option_a" in relative.casefold() else None
        )
        if option_id in option_rows:
            option_rows[option_id].append(relative)
    for option_id, rows in option_rows.items():
        focused = [row for row in rows if "focused" in row.casefold() and "_annotated" not in row.casefold()]
        annotated_focused = [row for row in rows if "focused" in row.casefold() and "_annotated" in row.casefold()]
        if len(focused) != 1 or len(annotated_focused) != 1:
            failures.append(f"{option_id} missing one clean focused plus one annotated focused primary render pair: clean={focused}, annotated={annotated_focused}")
    primary_text = ""
    for relative in ("START_HERE.md", f"USER Review/{PRIMARY_REVIEW_FILE}"):
        path = packet_dir / relative
        if path.exists():
            primary_text += "\n" + path.read_text(encoding="utf-8")
    primary_image_refs = len(re.findall(r"\.(?:png|jpg|jpeg|gif|webp)\b", primary_text, flags=re.IGNORECASE))
    if primary_image_refs > 0:
        failures.append("Primary USER decision path directly embeds image filenames instead of routing through curated manifests")
    if "curated for decision clarity" not in primary_text:
        failures.append("Primary USER decision path missing curated final-packet image-scope wording")
    return failures


def _validate_comparative_audit_repair_aids(packet_dir: Path) -> list[str]:
    failures: list[str] = []
    required_terms_by_file = {
        "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md": [
            "source/code path",
            "UIREF owner",
            "future implementation comparison use",
            "not implementation proof",
            "OPTION-A",
            "OPTION-B",
            "OPTION-C",
            "OPTION-D",
            "OPTION-E",
            "OPTION-F",
            "OPTION-G",
        ],
        "Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md": [
            "real rendered draft-window/template",
            "PySide6 QWebEngine",
            "not freehand static concept drawings",
            "PIL/ImageDraw is not the source for clean candidate media",
            "Option A remains the actual current runtime baseline screenshot",
            "Options B through G",
        ],
        "Review Aids/FUTURE_LAYOUT_ARRANGEMENT_CANDIDATES.md": [
            "FUTURE_LAYOUT_ARRANGEMENT_CANDIDATE",
            "OPTION-F",
            "not the current selected FAM-007 target",
            "possible USER-configurable layout arrangement pattern",
            "example only",
            "subject to later source-truth owner approval",
            OPTION_F_SEED_PACKET_PATH,
            OPTION_F_SEED_PACKET_SHA256,
            "option-f_focused.png",
            "option-f_desktop.png",
            "option-f_focused_annotated.png",
            "option-f_desktop_annotated.png",
            "option-f_focused_template.html",
            "option-f_desktop_template.html",
            "Card 4 into Card 2 position",
            "moved card becomes Card 2",
            "displaced/downstream cards",
            "AI Dashboard",
            "HUD Dashboard",
            "future parent windows",
            "Global Settings parent-window customization controls",
            "FAM-003",
            "FAM-006",
            "FAM-002/UIREF",
            "Governance/phase owner",
            "not runtime implementation",
            "not active settings behavior",
            "not persistence/schema approval",
            "not drag/drop approval",
        ],
        "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md": [
            "Material visual differences require USER approval",
            "source-truth-grounded",
            "Helper PASS",
            "screenshot existence",
            "cannot prove implementation match",
        ],
        "Review Aids/CAVEAT_LEDGER.md": [
            "Current Caveat State: `NONE_RECORDED_YET`",
            "acceptance does not approve H1/LV acceptance",
            "future proof obligations",
            "source-truth reconciliation",
        ],
        "Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md": [
            "VISUAL_ACCEPTANCE_EXPLORATION_LOOP",
            "Clean enough is not the acceptance standard",
            "USER-selected visual direction",
            "Packet validation proves completeness/currentness only",
            "Near-duplicates with label-only changes are rejected",
            "static concept drawings",
            "retained traits",
            "rejected traits",
            "New territory",
            "VAT-CYCLE-20260624-02",
            "OPTION-E",
            "OPTION-F",
            "OPTION-G",
            "VAT-CYCLE-20260624-03",
            "D-primary/E-polish hybrid",
            "materially differ",
            "Real Draft Window Requirement",
        ],
        "Review Aids/STATE_COVERAGE_STORYBOARD.md": [
            "hover",
            "focus",
            "pressed",
            "Disabled or future-gated",
            "Provider/model unavailable",
            "Local readiness report generated",
            "Copy-success",
            "Resized / minimum",
            "actual app evidence or a USER-approved waiver",
        ],
        "Review Aids/STATE_COVERAGE_MATRIX.md": [
            "DEFERRED_TO_IMPLEMENTATION_PROOF",
            "REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE",
            "provider/model unavailable",
            "child/domain window open",
        ],
        "Review Aids/REJECTED_PATTERNS_LEDGER.md": [
            "Product / UX risk",
            "Governance risk",
            "State / proof gap",
            "UIREF / FAM boundary risk",
            "Implementation-match risk",
            "candidate/comparator dispositions",
            "twelve-card status monitor",
            "near-duplicate variant generation",
        ],
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md": [
            "Material Difference Rule",
            "Caveat Handling",
            "artifact-to-surface trace",
            "Row Grammar Rule",
            "OPTION-D",
            "OPTION-E",
            "OPTION-F",
            "OPTION-G",
            "Option F Preservation",
            "Option G Recommended Target Basis",
            "Option F Deterministic Arrangement Example",
            "Card 4 into Card 2 position",
        ],
        "Review Aids/UI_UX_WORKSTREAM_EXIT_GATE_CANDIDATE.md": [
            "GOVERNANCE_CANDIDATE_ONLY",
            "UI/UX Workstream Exit Acceptance Gate",
            "Packet Reviewability Only",
            "Visual Target Treated As Implementation Proof",
            "Governance/FAM-002/UIREF carrier",
        ],
        "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md": [
            "Visual Acceptance Exploration Loop",
            "clean enough is not the acceptance standard",
            "USER-selected visual direction",
            "no near-duplicate label-only variants",
        ],
    }
    for relative, terms in required_terms_by_file.items():
        path = packet_dir / relative
        if not path.exists():
            failures.append(f"Comparative-audit repair aid missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        text_folded = text.casefold()
        for term in terms:
            if term.casefold() not in text_folded:
                failures.append(f"{relative} missing required comparative-audit term: {term}")
    primary_text = ""
    for relative in ("START_HERE.md", f"USER Review/{PRIMARY_REVIEW_FILE}"):
        path = packet_dir / relative
        if path.exists():
            primary_text += "\n" + path.read_text(encoding="utf-8")
    for term in (
        "ARTIFACT_TO_SURFACE_LEDGER.md",
        "DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md",
        "IMPLEMENTATION_DIFFERENCE_RULE.md",
        "CAVEAT_LEDGER.md",
        "VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md",
        "Material visual differences require USER approval",
        "caveat acceptance only records required follow-up",
        "Clean enough is not the acceptance standard",
        "USER-selected visual direction",
        "real rendered draft-window/template",
        "OPTION-E",
        "OPTION-F",
        "OPTION-G",
        "OPTION-D",
        "D-primary/E-polish",
        "row grammar",
    ):
        if term.casefold() not in primary_text.casefold():
            failures.append(f"Primary USER decision path missing comparative-audit routing/boundary term: {term}")
    return failures


def generate() -> Path:
    zip_path = USER_ROOT / f"{WORKTREE_LABEL}-{_stamp()}.zip"
    _purge_packet_root()
    _update_external_state(zip_path)
    options = _copy_actual_media() + _generate_candidate_media() + _generate_option_d_media() + _generate_next_cycle_media()
    _write_packet_files(options)
    _create_zip(zip_path)
    return zip_path


def validate(packet_dir: Path = PACKET_DIR, zip_path: Path | None = None) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not packet_dir.exists():
        return False, [f"Packet folder missing: {packet_dir}"]
    if zip_path is None:
        zips = sorted(USER_ROOT.glob(f"{WORKTREE_LABEL}-*.zip"), key=lambda path: path.stat().st_mtime, reverse=True)
        zip_path = zips[0] if zips else None
    if zip_path is None or not zip_path.exists():
        failures.append("Timestamped ZIP missing")
    for relative in REQUIRED_PACKET_FILES:
        if not (packet_dir / relative).exists():
            failures.append(f"Required packet file missing: {relative}")
    primary_files = list((packet_dir / "USER Review").glob("*.md"))
    if len(primary_files) != 1:
        failures.append(f"Expected exactly one primary USER review file; found {len(primary_files)}")
    option_text_path = packet_dir / "Review Aids" / "VISUAL_OPTIONS_PACKET.md"
    option_text = option_text_path.read_text(encoding="utf-8") if option_text_path.exists() else ""
    for option_id in OPTION_IDS:
        if option_id not in option_text:
            failures.append(f"Visual option missing: {option_id}")
    media_files = sorted((packet_dir / "Review Aids" / "Render Media").rglob("*.png"))
    if len(media_files) != EXPECTED_RENDER_IMAGE_COUNT:
        failures.append(f"Expected exactly {EXPECTED_RENDER_IMAGE_COUNT} curated render media PNGs; found {len(media_files)}")
    for image_path in media_files:
        try:
            with Image.open(image_path) as image:
                image.verify()
        except Exception as exc:
            failures.append(f"Image cannot be opened: {image_path}: {exc}")
    failures.extend(_validate_annotation_images(packet_dir))
    failures.extend(_validate_image_relevance_manifest(packet_dir))
    failures.extend(_validate_comparative_audit_repair_aids(packet_dir))
    annotation_manifest = packet_dir / "Review Aids" / "ANNOTATION_MANIFEST.md"
    annotation_text = annotation_manifest.read_text(encoding="utf-8") if annotation_manifest.exists() else ""
    if not annotation_text:
        failures.append("Annotation manifest missing or empty")
    for option_id in OPTION_IDS:
        sample_image = next((path for path in media_files if _option_id_from_annotated_path(path) == option_id), None)
        if sample_image is None:
            failures.append(f"Cannot find sample render for annotation manifest validation: {option_id}")
            continue
        with Image.open(sample_image) as image:
            width, height = image.size
        for spec in _annotation_specs(option_id, width, height, desktop="desktop" in sample_image.name.casefold()):
            if spec.annotation_id not in annotation_text:
                failures.append(f"Annotation manifest missing marker: {spec.annotation_id}")
    generated_text = ""
    for relative in (
        "START_HERE.md",
        f"USER Review/{PRIMARY_REVIEW_FILE}",
        "Review Aids/VISUAL_OPTIONS_PACKET.md",
        "Review Aids/ELEMENT_LEGENDS.md",
        "Review Aids/ANNOTATION_MANIFEST.md",
        "Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md",
        "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
        "Review Aids/CAVEAT_LEDGER.md",
        "Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md",
        "Review Aids/FUTURE_LAYOUT_ARRANGEMENT_CANDIDATES.md",
        "Review Aids/STATE_COVERAGE_STORYBOARD.md",
        "Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
        "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md",
        "Review Aids/UI_UX_WORKSTREAM_EXIT_GATE_CANDIDATE.md",
        "Review Aids/VALIDATION_SUMMARY.md",
    ):
        path = packet_dir / relative
        if path.exists():
            generated_text += "\n" + path.read_text(encoding="utf-8")
    required_boundary_terms = (
        "not final implemented product truth by itself",
        "code-to-visual proof",
        "clean and annotated render media",
        "Clean enough is not the acceptance standard",
        "USER-selected visual direction",
        "retained traits",
        "rejected traits",
        "new territory",
        "materially differ",
        "Near-duplicates with label-only changes are rejected",
        "Real Draft Window Requirement",
        "real rendered draft-window/template",
        "PySide6 QWebEngine",
        "not freehand static concept drawings",
        "PIL/ImageDraw is not the source for clean candidate media",
        "future user-customizable layout arrangement candidate",
        "future candidate",
        "possible USER-configurable layout arrangement pattern",
        "example only",
        "subject to later source-truth owner approval",
        OPTION_F_SEED_PACKET_PATH,
        OPTION_F_SEED_PACKET_SHA256,
        "option-f_focused.png",
        "option-f_desktop.png",
        "option-f_focused_annotated.png",
        "option-f_desktop_annotated.png",
        "option-f_focused_template.html",
        "option-f_desktop_template.html",
        "Card 4 into Card 2 position",
        "moved card becomes Card 2",
        "displaced/downstream cards",
        "AI Dashboard",
        "HUD Dashboard",
        "future parent windows",
        "Global Settings parent-window customization controls",
        "FAM-003",
        "FAM-006",
        "FAM-002/UIREF",
        "Governance/phase owner",
        "not runtime implementation",
        "not active settings behavior",
        "not persistence/schema approval",
        "not drag/drop approval",
        "OPTION-D",
        "OPTION-E",
        "OPTION-F",
        "OPTION-G",
        "VAT-CYCLE-20260624-02",
        "VAT-CYCLE-20260624-03",
        "recommended current-cycle target basis",
        "D-primary/E-polish hybrid",
        "Option D behavior and row grammar",
        "selective Option E",
        "without Option F layout-customization behavior",
        "option-g_focused.png",
        "option-g_desktop.png",
        "option-g_focused_annotated.png",
        "option-g_desktop_annotated.png",
        "option-g_focused_template.html",
        "option-g_desktop_template.html",
        "G-ROW-02B",
        "G-BTN-03",
        "two-by-two grouped-card grid",
        "wide top summary/action zone",
        "row grammar",
    )
    for term in required_boundary_terms:
        if term not in generated_text:
            failures.append(f"Generated visual packet text missing required boundary wording: {term}")
    if "{OPTION_F_" in generated_text:
        failures.append("Generated visual packet text contains unresolved Option F placeholder braces")
    forbidden_final_product_terms = (
        "final UI",
        "true end state",
        "guaranteed final render",
        "accepted final product",
        "final branch visual contract",
    )
    for term in forbidden_final_product_terms:
        if term.casefold() in generated_text.casefold():
            failures.append(f"Generated visual packet text implies final product truth: {term}")
    if zip_path and zip_path.exists():
        folder_entries = {path.relative_to(packet_dir).as_posix() for path in _packet_file_entries()}
        with zipfile.ZipFile(zip_path, "r") as archive:
            zip_entries = {info.filename for info in archive.infolist() if not info.is_dir()}
            if folder_entries != zip_entries:
                failures.append("Folder/ZIP parity failed")
            image_entries = [entry for entry in zip_entries if entry.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]
            if len(image_entries) != EXPECTED_RENDER_IMAGE_COUNT:
                failures.append(f"Expected exactly {EXPECTED_RENDER_IMAGE_COUNT} curated ZIP images; found {len(image_entries)}")
            annotated_entries = [entry for entry in image_entries if "_annotated" in entry]
            if len(annotated_entries) != EXPECTED_ANNOTATED_IMAGE_COUNT:
                failures.append(f"Expected {EXPECTED_ANNOTATED_IMAGE_COUNT} annotated ZIP images for every option render; found {len(annotated_entries)}")
            if "Review Aids/ANNOTATION_MANIFEST.md" not in zip_entries:
                failures.append("ZIP missing annotation manifest")
            if "Review Aids/IMAGE_RELEVANCE_MANIFEST.md" not in zip_entries:
                failures.append("ZIP missing image relevance manifest")
            if "Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md" not in zip_entries:
                failures.append("ZIP missing draft-window template render manifest")
            template_entries = [entry for entry in zip_entries if entry.startswith(f"{DRAFT_TEMPLATE_ROOT}/") and entry.endswith("_template.html")]
            if len(template_entries) != (len(OPTION_IDS) - 1) * 2:
                failures.append(f"Expected two HTML draft templates for every non-runtime option; found {len(template_entries)}")
            for option_id in OPTION_IDS:
                if option_id == "OPTION-A":
                    continue
                option_slug = option_id.lower()
                matching_templates = [entry for entry in template_entries if option_slug in entry]
                if len(matching_templates) != 2:
                    failures.append(f"{option_id} missing focused+desktop rendered draft template HTML artifacts: {matching_templates}")
            for required_entry in (
                "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
                "Review Aids/DRAFT_WINDOW_TEMPLATE_RENDER_MANIFEST.md",
                "Review Aids/FUTURE_LAYOUT_ARRANGEMENT_CANDIDATES.md",
                "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
                "Review Aids/CAVEAT_LEDGER.md",
                "Review Aids/VISUAL_ACCEPTANCE_EXPLORATION_LOOP.md",
                "Review Aids/STATE_COVERAGE_STORYBOARD.md",
            ):
                if required_entry not in zip_entries:
                    failures.append(f"ZIP missing comparative-audit repair aid: {required_entry}")
            primary_entries = [entry for entry in zip_entries if entry.startswith("USER Review/") and entry.endswith(".md")]
            if primary_entries != [f"USER Review/{PRIMARY_REVIEW_FILE}"]:
                failures.append(f"Unexpected primary USER review entries in ZIP: {primary_entries}")
            required_zip_entries = {
                "Source Truth Context/current_external_branch_state.md",
                "Source Truth Context/current_external_branch_plan.md",
                "Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md",
            }
            missing_context = sorted(required_zip_entries - zip_entries)
            if missing_context:
                failures.append(f"ZIP missing required Source Truth Context entries: {missing_context}")
            else:
                head = _git_value("rev-parse", "HEAD")
                state_text = archive.read("Source Truth Context/current_external_branch_state.md").decode("utf-8")
                plan_text = archive.read("Source Truth Context/current_external_branch_plan.md").decode("utf-8")
                udl_text = archive.read("Source Truth Context/FAM_007_UNIFIED_DEFECT_LEDGER.md").decode("utf-8")
                state_next_gate = _section(state_text, "## Next Legal Phase")
                plan_next_gate = _section(plan_text, "## Next Legal Phase")
                stale_next_gate_terms = [
                    "Live Validation LV1 Review",
                    "Hardening H1 Green packet",
                    "I accept the FAM-007 Hardening H1 Green packet",
                    "approve bounded Live Validation LV1 review",
                ]
                if str(zip_path) not in state_text or str(zip_path) not in plan_text:
                    failures.append("Copied Source Truth Context does not name the final ZIP path")
                if "VISUAL_ACCEPTANCE_TARGET_REVIEW.md" not in plan_text:
                    failures.append("Copied branch plan does not name the visual acceptance target primary review file")
                if "WORKSTREAM_IMPLEMENTATION_H1_LV_REVIEW.md" in _current_packet_section(plan_text):
                    failures.append("Copied branch plan active Packet Review State still names stale H1/LV primary review file")
                if not state_next_gate:
                    failures.append("Copied branch state missing active Next Legal Phase section")
                if not plan_next_gate:
                    failures.append("Copied branch plan missing active Next Legal Phase section")
                if VISUAL_NEXT_LEGAL_PHASE not in state_next_gate or VISUAL_NEXT_LEGAL_PHASE not in plan_next_gate:
                    failures.append("Copied active Next Legal Phase sections do not match the Visual Acceptance Target gate")
                if str(zip_path) not in state_next_gate or str(zip_path) not in plan_next_gate:
                    failures.append("Copied active Next Legal Phase decision text does not name the final ZIP path")
                for term in stale_next_gate_terms:
                    if term in state_next_gate or term in plan_next_gate or term in _current_packet_section(plan_text):
                        failures.append(f"Copied active current packet sections contain stale H1/LV next-gate text: {term}")
                if "H1/LV decision-preparation packet generated" in state_text:
                    failures.append("Copied branch state still describes the current visual packet as H1/LV decision-prep")
                if f"Current HEAD: `{head}`" not in udl_text:
                    failures.append("Copied UDL Current HEAD does not match live HEAD")
                if "Current HEAD Field Classification:" not in udl_text:
                    failures.append("Copied UDL does not classify Current HEAD currentness")
                for term in (
                    "F7-UDL-027",
                    "F7-UDL-028",
                    "Option F Future Layout Arrangement Candidate Preservation",
                    "Option D Primary Target Refinement / Option F Boundary Preservation",
                    OPTION_F_SEED_PACKET_PATH,
                    OPTION_F_SEED_PACKET_SHA256,
                    "OPTION-G",
                    "G-ROW-02B",
                    "D-primary/E-polish",
                    "Card 4 into Card 2 position",
                    "moved card becomes Card 2",
                    "Future Owners Before Implementation",
                    "not runtime implementation",
                    "not active settings behavior",
                    "not persistence/schema approval",
                    "not drag/drop approval",
                ):
                    if term not in udl_text:
                        failures.append(f"Copied UDL missing Option F preservation term: {term}")
            for entry in zip_entries:
                if entry.lower().endswith(".png"):
                    try:
                        with archive.open(entry) as handle:
                            with Image.open(handle) as image:
                                image.verify()
                    except Exception as exc:
                        failures.append(f"ZIP image cannot be opened: {entry}: {exc}")
    return not failures, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--generate-recovery-blocker", action="store_true")
    parser.add_argument("--validate-recovery-blocker", action="store_true")
    parser.add_argument("--zip", type=Path)
    args = parser.parse_args()
    zip_path = args.zip
    if args.generate_recovery_blocker:
        zip_path = generate_recovery_blocker()
        print(f"Generated recovery blocker packet folder: {PACKET_DIR}")
        print(f"Generated recovery blocker packet ZIP: {zip_path}")
        print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
    if args.validate_recovery_blocker:
        ok, failures = validate_recovery_blocker(zip_path=zip_path)
        if ok:
            print("FAM-007 accepted-historical recovery blocker packet validation: PASS")
            if zip_path:
                print(f"ZIP: {zip_path}")
                print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
            return 0
        print("FAM-007 accepted-historical recovery blocker packet validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    if args.generate:
        zip_path = generate()
        print(f"Generated packet folder: {PACKET_DIR}")
        print(f"Generated packet ZIP: {zip_path}")
        print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
    if args.validate:
        ok, failures = validate(zip_path=zip_path)
        if ok:
            print("FAM-007 visual acceptance target packet validation: PASS")
            if zip_path:
                print(f"ZIP: {zip_path}")
                print(f"ZIP SHA256: {_zip_sha256(zip_path)}")
            return 0
        print("FAM-007 visual acceptance target packet validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    if not args.generate and not args.validate and not args.generate_recovery_blocker and not args.validate_recovery_blocker:
        parser.error("choose --generate, --validate, or both")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
