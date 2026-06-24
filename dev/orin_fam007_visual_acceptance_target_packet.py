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
import re
import shutil
import subprocess
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKTREE_LABEL = "FAM-007"
BRANCH_SLUG = "feature_fam_007_ai_control_center_readiness_diagnostics"
EXTERNAL_BRANCH_ROOT = Path(r"C:\Nexus Governance State\branches") / BRANCH_SLUG
BRANCH_STATE = EXTERNAL_BRANCH_ROOT / "branch_state.md"
BRANCH_PLAN = EXTERNAL_BRANCH_ROOT / "branch_plan.md"
UDL_PATH = EXTERNAL_BRANCH_ROOT / "unified_defect_ledger.md"
USER_ROOT = Path(r"C:\Nexus USER")
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
OPTION_IDS = ("OPTION-A", "OPTION-B", "OPTION-C", "OPTION-D")
EXPECTED_RENDER_IMAGE_COUNT = len(OPTION_IDS) * 4
EXPECTED_ANNOTATED_IMAGE_COUNT = len(OPTION_IDS) * 2

REQUIRED_PACKET_FILES = [
    "START_HERE.md",
    "USER Review/VISUAL_ACCEPTANCE_TARGET_REVIEW.md",
    "Review Aids/VISUAL_IMPACT_CLASSIFICATION.md",
    "Review Aids/VISUAL_OPTIONS_PACKET.md",
    "Review Aids/ELEMENT_LEGENDS.md",
    "Review Aids/ANNOTATION_MANIFEST.md",
    "Review Aids/IMAGE_RELEVANCE_MANIFEST.md",
    "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
    "Review Aids/STATE_COVERAGE_MATRIX.md",
    "Review Aids/STATE_COVERAGE_STORYBOARD.md",
    "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
    "Review Aids/CAVEAT_LEDGER.md",
    "Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md",
    "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
    "Review Aids/REJECTED_PATTERNS_LEDGER.md",
    "Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
    "Review Aids/SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md",
    "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md",
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
        "this is the only current FAM-007 USER packet ZIP retained under C:\\Nexus USER. "
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
Finding: `The branch-local Visual Acceptance Target packet generator could create visual legends that were hard to map to exact render regions, and focused annotated renders could clip or truncate callout labels outside the image canvas.`
Required Disposition: `Future Visual Acceptance Target packets must include clean and annotated renders, stable annotation IDs, color plus non-color cues, an annotation manifest mapping marker ID to element ID and visual region, in-canvas annotation labels, in-bounds target boxes, in-bounds label boxes, in-bounds leader lines, and template-not-endstate wording.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now renders annotated images with a right-side in-canvas annotation key panel, keeps clean renders beside annotated renders, records label boxes and leader lines in ANNOTATION_MANIFEST.md, and validates annotation geometry plus visible marker label pixels for every annotated render.`
Proof: `Current Visual Acceptance Target packet validation fails if any annotation target, label box, or leader line extends outside the image canvas, or if the marker label area does not contain visible text pixels.`
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
Finding: `The prior Visual Acceptance Target packet presented Option A, Option B, and Option C without a distinct hybrid target that carried the USER-approved old AI Control Center row grammar as a reference while preserving the current AI Dashboard / AI Control Center doorway model. That created a risk that USER would have to choose between correct structure and the row-based product feel they explicitly wanted.`
Required Disposition: `Current FAM-007 visual target packets must present Option D as a branch-local hybrid candidate: Option A source-truth product structure and doorway labels, Option B compact grouping rhythm, accepted old AI Control Center row grammar as a visual grammar reference, and Option C as rejected-risk boundary only. Option D is still a candidate render, not implementation proof or a product/runtime mutation.`
Repair: `dev/orin_fam007_visual_acceptance_target_packet.py now generates Option D clean focused, annotated focused, clean desktop/context, and annotated desktop/context renders; maps Option D through image relevance, annotation, artifact-to-surface, state, rejected-pattern, and primary USER review text; and validates all four options as the curated final-packet image set.`
Proof: `Current Visual Acceptance Target packet validation fails if Option D, its annotated markers, its row-grammar wording, or its curated render media are missing from the generated folder or ZIP.`
Current Review Packet: `{zip_path}`
No-Fake-Preservation Rule: `This repair does not approve runtime UI implementation, H1/LV, USER UTS, PR Readiness, PR creation, merge, release, provider/model/private/cache/memory/download/packaging, sibling/Governance/FAM-002/UIREF mutation, imports, or v1.8.0 work.`
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


def _draw_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, lines: list[str]) -> None:
    draw.rounded_rectangle(box, radius=18, fill=(5, 24, 38), outline=(66, 185, 210), width=2)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 58, y1 + 52), radius=12, fill=(8, 54, 74), outline=(76, 214, 234))
    draw.text((x1 + 28, y1 + 25), "ID", fill=(158, 240, 237), font=_font(11))
    draw.text((x1 + 74, y1 + 19), title.upper(), fill=(235, 248, 252), font=_font(18))
    yy = y1 + 56
    for line in lines:
        draw.text((x1 + 74, yy), line, fill=(158, 205, 213), font=_font(13))
        yy += 23
    button_y = y2 - 50
    draw.rounded_rectangle((x2 - 186, button_y, x2 - 24, button_y + 30), radius=15, fill=(7, 34, 49), outline=(61, 168, 198), width=2)
    draw.text((x2 - 166, button_y + 8), "OPEN SURFACE", fill=(226, 245, 249), font=_font(11))


ANNOTATION_ELEMENTS = [
    ("CHROME-001", "cyan box", "NDAI custom window frame / shell"),
    ("CTRL-001", "yellow circle", "compact window control cluster"),
    ("TITLE-001", "magenta bracket", "title strip and subtitle copy"),
    ("PANEL-001", "green box", "category doorway card or panel body"),
    ("ACTION-001", "amber arrow", "primary open/action button"),
    ("STATUS-001", "blue bracket", "compact AI/provider/trust status"),
]

ANNOTATION_LABEL_PANEL_WIDTH = 260
ANNOTATION_LABEL_BOX_WIDTH = 216
ANNOTATION_LABEL_BOX_HEIGHT = 34


def _annotation_targets(width: int, height: int, *, desktop: bool) -> dict[str, tuple[int, int, int, int]]:
    if desktop and height >= 930:
        x, y, win_w, win_h = 820, 70, 720, 690
        return {
            "CHROME-001": (x, y, x + win_w, y + win_h),
            "CTRL-001": (x + win_w - 112, y + 26, x + win_w - 28, y + 70),
            "TITLE-001": (x + 38, y + 30, x + 500, y + 158),
            "PANEL-001": (x + 28, y + 178, x + win_w - 28, y + 616),
            "ACTION-001": (x + win_w - 220, y + 272, x + win_w - 44, y + 642),
            "STATUS-001": (x + 38, y + 116, x + 440, y + 160),
        }
    if not desktop and width >= 800 and height >= 820:
        x, y, win_w, win_h = 48, 40, 720, 690
        return {
            "CHROME-001": (x, y, x + win_w, y + win_h),
            "CTRL-001": (x + win_w - 112, y + 26, x + win_w - 28, y + 70),
            "TITLE-001": (x + 38, y + 30, x + 500, y + 158),
            "PANEL-001": (x + 28, y + 178, x + win_w - 28, y + 616),
            "ACTION-001": (x + win_w - 220, y + 272, x + win_w - 44, y + 642),
            "STATUS-001": (x + 38, y + 116, x + 440, y + 160),
        }
    if not desktop and width < 700:
        x, y, win_w, win_h = 20, 20, max(360, width - 40), max(360, height - 40)
        return {
            "CHROME-001": (x, y, x + win_w, y + win_h),
            "CTRL-001": (max(x + win_w - 124, x + 20), y + 20, x + win_w - 24, y + 66),
            "TITLE-001": (x + 24, y + 26, min(x + win_w - 120, x + 400), y + 116),
            "PANEL-001": (x + 24, y + 140, x + win_w - 24, min(y + 340, y + win_h - 116)),
            "ACTION-001": (max(x + win_w - 208, x + 80), y + 248, x + win_w - 28, min(y + 430, y + win_h - 76)),
            "STATUS-001": (x + 24, max(y + win_h - 118, y + 300), x + win_w - 24, y + win_h - 20),
        }
    if desktop:
        x, y, win_w, win_h = 850, 82, 650, 620
    else:
        x, y, win_w, win_h = 48, 48, 650, 620
    return {
        "CHROME-001": (x, y, x + win_w, y + win_h),
        "CTRL-001": (x + win_w - 136, y + 32, x + win_w - 38, y + 76),
        "TITLE-001": (x + 40, y + 36, x + 430, y + 126),
        "PANEL-001": (x + 30, y + 168, x + win_w - 30, y + 502),
        "ACTION-001": (x + win_w - 220, y + 270, x + win_w - 44, y + 486),
        "STATUS-001": (x + 30, y + 510, x + win_w - 30, y + 674),
    }


def _callout_geometry(target: tuple[int, int, int, int], index: int, canvas_width: int) -> dict[str, tuple[int, ...]]:
    x1, y1, x2, y2 = target
    label_x = canvas_width - ANNOTATION_LABEL_PANEL_WIDTH + 20
    label_y = 64 + (index - 1) * 50
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
    draw.rounded_rectangle(target, radius=12, outline=color, width=4)
    geometry = _callout_geometry(target, index, canvas_width)
    label_box = geometry["label_box"]
    leader_line = geometry["leader_line"]
    label_x, label_y, _, _ = label_box
    draw.line(leader_line, fill=color, width=3)
    draw.rounded_rectangle(label_box, radius=10, fill=(1, 14, 23), outline=color, width=3)
    if shape == "circle":
        draw.ellipse((label_x + 7, label_y + 7, label_x + 21, label_y + 21), outline=color, width=3)
    elif shape == "bracket":
        draw.line((label_x + 8, label_y + 7, label_x + 8, label_y + 21), fill=color, width=3)
        draw.line((label_x + 8, label_y + 7, label_x + 20, label_y + 7), fill=color, width=3)
        draw.line((label_x + 8, label_y + 21, label_x + 20, label_y + 21), fill=color, width=3)
    elif shape == "arrow":
        draw.polygon([(label_x + 8, label_y + 14), (label_x + 22, label_y + 7), (label_x + 22, label_y + 21)], fill=color)
    else:
        draw.rectangle((label_x + 7, label_y + 7, label_x + 21, label_y + 21), outline=color, width=3)
    draw.text((label_x + 28, label_y + 8), label, fill=(238, 248, 252), font=_font(10))
    return geometry


def _annotate_render(source: Path, target: Path, option_id: str, *, desktop: bool) -> list[dict[str, str]]:
    colors = [
        (80, 218, 238),
        (236, 202, 89),
        (230, 112, 225),
        (92, 220, 156),
        (242, 166, 80),
        (105, 164, 255),
    ]
    shapes = ["box", "circle", "bracket", "box", "arrow", "bracket"]
    with Image.open(source) as image:
        base = image.convert("RGB")
    annotated = Image.new("RGB", (base.width + ANNOTATION_LABEL_PANEL_WIDTH, base.height), (0, 5, 8))
    annotated.paste(base, (0, 0))
    draw = ImageDraw.Draw(annotated)
    panel_x = base.width
    draw.rectangle((panel_x, 0, annotated.width, annotated.height), fill=(2, 16, 25))
    draw.line((panel_x, 0, panel_x, annotated.height), fill=(59, 161, 190), width=2)
    draw.text((panel_x + 20, 22), "ANNOTATION KEY", fill=(104, 225, 239), font=_font(13))
    draw.text((panel_x + 20, 40), "IDs stay in-canvas", fill=(158, 205, 213), font=_font(11))
    targets = _annotation_targets(base.width, base.height, desktop=desktop)
    rows: list[dict[str, str]] = []
    for index, (element_id, cue, purpose) in enumerate(ANNOTATION_ELEMENTS, start=1):
        marker_id = f"{option_id}-A{index:02d}"
        target_box = targets[element_id]
        color = colors[index - 1]
        geometry = _draw_callout(draw, marker_id, target_box, index, color=color, shape=shapes[index - 1], canvas_width=annotated.width)
        rows.append(
            {
                "option": option_id,
                "annotation": marker_id,
                "element": element_id,
                "cue": cue,
                "region": f"{target_box[0]},{target_box[1]},{target_box[2]},{target_box[3]}",
                "label_box": ",".join(str(value) for value in geometry["label_box"]),
                "leader_line": ",".join(str(value) for value in geometry["leader_line"]),
                "purpose": purpose,
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
    for radius in range(80, 420, 60):
        draw.ellipse((130 - radius, 340 - radius, 130 + radius, 340 + radius), outline=(8, 47, 62), width=1)
    win_w, win_h = 650, 620
    x = 850 if desktop else 48
    y = 82 if desktop else 48
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=28, fill=(3, 14, 25), outline=(65, 183, 214), width=2)
    draw.rounded_rectangle((x + 26, y + 24, x + win_w - 26, y + 128), radius=24, fill=(5, 22, 35), outline=(25, 96, 119), width=1)
    draw.text((x + 48, y + 42), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 48, y + 66), title, fill=(238, 248, 252), font=_font(29))
    draw.text((x + 48, y + 106), subtitle, fill=(158, 205, 213), font=_font(13))
    draw.rounded_rectangle((x + win_w - 128, y + 38, x + win_w - 46, y + 68), radius=15, fill=(4, 28, 40), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 102, y + 46), "-  x", fill=(230, 247, 250), font=_font(13))
    draw.text((x + 36, y + 146), f"{option} ELEMENT LEGEND", fill=(108, 225, 236), font=_font(12))
    _draw_card(draw, (x + 34, y + 174, x + win_w - 34, y + 324), "CHROME-001 / TITLE-001", ["NDAI chrome, compact controls, dashboard title group"])
    _draw_card(draw, (x + 34, y + 346, x + win_w - 34, y + 496), "PANEL-001 / ACTION-001", ["Category doorway card, one primary open action, compact truth copy"])
    _draw_card(draw, (x + 34, y + 518, x + win_w - 34, y + 668), "STATUS-001 / ERROR-001", ["Provider-visible data none, blocked provider/model/cache/memory paths"])
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
    draw.rounded_rectangle(box, radius=18, fill=(3, 19, 34), outline=(32, 97, 124), width=1)
    draw.rounded_rectangle((x1 + 16, y1 + 16, x1 + 52, y1 + 52), radius=12, fill=(5, 51, 70), outline=(72, 194, 220), width=1)
    draw.text((x1 + 25, y1 + 26), number, fill=(120, 234, 239), font=_font(12))
    draw.text((x1 + 66, y1 + 15), title.upper(), fill=(236, 247, 250), font=_font(16))
    draw.text((x1 + 66, y1 + 40), description, fill=(148, 194, 205), font=_font(11))
    yy = y1 + 70
    label_font = _font(10)
    value_font = _font(10)
    for label, value in rows:
        draw.line((x1 + 22, yy, x2 - 22, yy), fill=(69, 166, 190), width=1)
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
    width, height = (1600, 940) if desktop else (820, 840)
    img = Image.new("RGB", (width, height), (0, 5, 8))
    draw = ImageDraw.Draw(img)
    for gx in range(0, width, 32):
        draw.line((gx, 0, gx, height), fill=(5, 34, 44), width=1)
    for gy in range(0, height, 32):
        draw.line((0, gy, width, gy), fill=(5, 34, 44), width=1)
    for radius in range(120, 470, 70):
        draw.ellipse((190 - radius, 390 - radius, 190 + radius, 390 + radius), outline=(8, 50, 64), width=1)
    win_w, win_h = 720, 690
    x = 820 if desktop else 48
    y = 70 if desktop else 40
    draw.rounded_rectangle((x, y, x + win_w, y + win_h), radius=28, fill=(1, 15, 26), outline=(67, 179, 205), width=2)
    draw.rounded_rectangle((x + 18, y + 18, x + win_w - 18, y + 162), radius=24, fill=(2, 15, 28), outline=(15, 56, 78), width=1)
    draw.text((x + 44, y + 36), "NEXUS DESKTOP AI", fill=(96, 220, 239), font=_font(13))
    draw.text((x + 44, y + 62), "AI Dashboard", fill=(240, 248, 250), font=_font(30))
    draw.text((x + 44, y + 104), "Top-level AI orientation, trust state, and category doorways.", fill=(152, 200, 210), font=_font(12))
    draw.rounded_rectangle((x + win_w - 96, y + 28, x + win_w - 28, y + 62), radius=17, fill=(4, 30, 42), outline=(79, 201, 225), width=2)
    draw.text((x + win_w - 78, y + 37), "-  x", fill=(230, 247, 250), font=_font(13))
    _draw_status_strip(draw, x + 42, y + 122, ["AI - ORIN", "STATUS - NOT IMPLEMENTED", "PROVIDER - BLOCKED"])
    card_x1 = x + 28
    card_x2 = x + win_w - 28
    _draw_row_card(
        draw,
        (card_x1, y + 182, card_x2, y + 346),
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
        (card_x1, y + 362, card_x2, y + 526),
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
        (card_x1, y + 542, card_x2, y + 686),
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
        _draw_option_mockup(focused, option_id, title, subtitle, desktop=False)
        _draw_option_mockup(desktop, option_id, title, subtitle, desktop=True)
        _annotate_render(focused, annotated_focused, option_id, desktop=False)
        _annotate_render(desktop, annotated_desktop, option_id, desktop=True)
        result.append(
            RenderOption(
                option_id,
                "Design Candidate Render using deterministic branch-local layout mockup",
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
    _draw_option_d_mockup(focused, desktop=False)
    _draw_option_d_mockup(desktop, desktop=True)
    _annotate_render(focused, annotated_focused, "OPTION-D", desktop=False)
    _annotate_render(desktop, annotated_desktop, "OPTION-D", desktop=True)
    return [
        RenderOption(
            "OPTION-D",
            "Design Candidate Render using deterministic branch-local high-fidelity row-grammar target",
            "DOORWAY_SHELL",
            str(focused.relative_to(PACKET_DIR)).replace("\\", "/"),
            str(desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
            str(annotated_focused.relative_to(PACKET_DIR)).replace("\\", "/"),
            str(annotated_desktop.relative_to(PACKET_DIR)).replace("\\", "/"),
            "Hybrid target: Option A product structure/source-truth labels, Option B compact grouping rhythm, accepted AI Control Center row grammar and full-window feel, with Option C retained only as rejected-risk boundary.",
        )
    ]


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
        "| Option ID | Annotation ID | Element ID | Color + non-color cue | Visual region | Label box | Leader line | Purpose | Annotated file |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for option in options:
        for image_path, desktop in (
            (option.annotated_focused_media, False),
            (option.annotated_desktop_media, True),
        ):
            target_path = PACKET_DIR / image_path
            with Image.open(target_path) as image:
                base_width = image.size[0] - ANNOTATION_LABEL_PANEL_WIDTH
                targets = _annotation_targets(base_width, image.size[1], desktop=desktop)
            for index, (element_id, cue, purpose) in enumerate(ANNOTATION_ELEMENTS, start=1):
                marker_id = f"{option.option_id}-A{index:02d}"
                box = targets[element_id]
                geometry = _callout_geometry(box, index, base_width + ANNOTATION_LABEL_PANEL_WIDTH)
                label_box = geometry["label_box"]
                leader_line = geometry["leader_line"]
                rows.append(
                    f"| `{option.option_id}` | `{marker_id}` | `{element_id}` | {cue}; visible label `{marker_id}` plus outline/callout line | `{box[0]},{box[1]},{box[2]},{box[3]}` | `{label_box[0]},{label_box[1]},{label_box[2]},{label_box[3]}` | `{leader_line[0]},{leader_line[1]},{leader_line[2]},{leader_line[3]}` | {purpose} | `{image_path}` |"
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
            "OPTION-D": "Hybrid row-grammar doorway target using Option A structure, Option B grouping discipline, and the attached accepted AI Control Center row grammar; not implementation proof by itself.",
        }[option.option_id]
        for artifact, artifact_class, proof_target in (
            (option.focused_media, "candidate clean focused render", "focused footprint, density, hierarchy, copy, and doorway layout"),
            (option.annotated_focused_media, "candidate annotated focused render", "element-group trace and visible callout mapping"),
            (option.desktop_media, "candidate clean desktop/context render", "desktop placement, scale, and surrounding visual relationship"),
            (option.annotated_desktop_media, "candidate annotated desktop/context render", "context-level element-group trace and callout mapping"),
        ):
            rows.append(
                f"| `{artifact}` | `{artifact_class}` | AI Dashboard / AI Control Center visual-target guide | `CHROME-001`, `CTRL-001`, `TITLE-001`, `PANEL-001`, `ACTION-001`, `STATUS-001` | `{source_paths}` | UIREF-001, UIREF-002, UIREF-003, UIREF-004, UIREF-005, UIREF-006 | {proof_target}; {option_note} | Later implementation-match proof must compare actual app screenshots/video against this artifact, explain material differences, and route USER approval when required. |"
            )
    return "\n".join(rows)


def _write_packet_files(options: list[RenderOption]) -> None:
    options_table = _options_table(options)
    decision_options_table = _decision_options_table(options)
    annotation_table = _annotation_manifest_table(options)
    image_relevance_table = _image_relevance_manifest_table(options)
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
2. Inspect the curated clean and annotated render media under `Review Aids/Render Media`.
3. Use `Review Aids/IMAGE_RELEVANCE_MANIFEST.md` to see why each included image is present in this final USER decision packet.
4. Use `Review Aids/ANNOTATION_MANIFEST.md` and `Review Aids/ELEMENT_LEGENDS.md` to map every callout marker to the exact visual region it identifies.
5. Use `Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md` to map every artifact to the visible surface, element group, source/code path, UIREF owner, and future implementation comparison use.
6. Use `Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md` and `Review Aids/CAVEAT_LEDGER.md` before accepting with caveats or claiming implementation match.
7. Use the Visual Selection Ledger template to accept, reject, combine, or revise specific options and element IDs.
8. Review the Draft Branch Visual Acceptance Target. It remains a branch-local guide until USER accepts or revises it, and implementation still requires code-to-visual proof and later review where source truth requires it.

Image Scope Rule: this final USER review packet is curated for decision clarity. It includes only the images needed to compare visual target options, understand clean versus annotated renders, and judge focused/desktop context. Repair-cycle/debug evidence belongs in explicitly labeled repair packets or helper output, not in this final USER decision path.
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

Implementation Difference Boundary: actual implementation may differ from the accepted visual target only with source-truth-grounded explanation. Material visual differences require USER approval or a recorded source-truth-routed justification before implementation-match claims. Helper PASS, screenshot existence, "closer", "better", or packet parity cannot prove implementation match.

Caveat Boundary: USER may accept a visual target with caveats, but caveat acceptance only records required follow-up, deferred elements, source-truth reconciliation needs, and future proof obligations. It never accepts H1/LV, USER UTS, PR Readiness, PR creation, merge, release, runtime mutation, or provider/model/private/cache/memory/download/packaging behavior.

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

Recommended: review `OPTION-D` as the strongest draft target candidate. It combines `OPTION-A` source-truth product structure and real doorway labels, `OPTION-B` cleaner grouping and compact directory rhythm, and the attached old accepted AI Control Center screenshot as a row-grammar reference for strong title/header, compact deterministic status strip, numbered grouped cards, row-based label/value grammar, useful truthful information, and a realistic full-window product feel. `OPTION-C` remains a rejected-risk boundary because it trends toward the larger workspace/report/status-monitor pattern that caused earlier false-green loops.

Option D Boundary: the attached old accepted screenshot is a visual grammar reference, not a literal target and not source truth. `OPTION-D` is a branch-local candidate render and draft target basis only; it does not prove current runtime implementation, approve product/runtime UI mutation, or promote a global template.

Anti-Regression Boundary: the AI Dashboard / AI Control Center top-level surface must remain a compact doorway/orientation surface. Row grammar belongs inside grouped doorway cards and focused child/detail surfaces; it must not regress into twelve separate top-level status cards, a status monitor, a debugger surface, or a long report body.

Recommendation Boundary: `OPTION-D` is recommended as a draft target basis, not as proof that the current runtime implementation is accepted or complete. If USER accepts `OPTION-D`, later implementation-match proof must still compare actual app evidence against the accepted target and classify any material differences.

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

| Element ID | Meaning | Visible cue in annotated renders | Applies To |
| --- | --- | --- | --- |
| `CHROME-001` | NDAI custom window chrome / frame | cyan box with `OPTION-*-A01` marker | all options |
| `CTRL-001` | compact window control cluster | yellow circle with `OPTION-*-A02` marker | all options |
| `TITLE-001` | title strip and subtitle copy | magenta bracket with `OPTION-*-A03` marker | all options |
| `PANEL-001` | category doorway card or panel body | green box with `OPTION-*-A04` marker | all options |
| `ACTION-001` | primary open/action button | amber arrow with `OPTION-*-A05` marker | all options |
| `STATUS-001` | compact AI/provider/trust status | blue bracket with `OPTION-*-A06` marker | all options |
| `ROW-001` | state row inside child/detail surface | future implementation-match proof marker required | child/detail surfaces |
| `SCROLL-001` | scrollbar treatment | future implementation-match proof marker required | options with overflow |
| `RESIZE-001` | resize affordance / behavior | future implementation-match proof marker required | all product windows |
| `EMPTY-001` | empty/no-data state | future implementation-match proof marker required | future child surfaces |
| `ERROR-001` | blocked/error/unavailable state | future implementation-match proof marker required | all options |

Example review language: `I accept ACTION-001 from OPTION-A, reject PANEL-001 from OPTION-C, and want STATUS-001 revised.`
""",
    )
    _write_text(
        "Review Aids/ANNOTATION_MANIFEST.md",
        f"""
# Annotation Manifest

Purpose: map every visible callout marker in the annotated render files to an exact element ID and visual region. The clean renders remain available beside the annotated renders so the USER can inspect the design without callout overlays.

Annotation Rule: every current visual target option must include color plus a non-color cue such as marker ID, outline shape, bracket, arrow, box, circle, and pointer line. Annotations should identify the region without hiding critical UI content.

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
        "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
        f"""
# Artifact-To-Surface Ledger

Purpose: map each included visual artifact to the USER-facing surface, visible element groups, source/code path, UIREF owner, branch-local proof target, and future implementation comparison use.

Ledger Rule: a render artifact can become a USER-accepted visual target guide only after USER selection. It is not implementation proof, LV proof, UTS proof, PR Readiness proof, or final product truth by itself.

{artifact_to_surface_table}
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
| provider/model unavailable | trust-boundary, no-provider, provider-visible-data none | compact status group identified by `STATUS-001` | backend-to-visual truth mapping and screenshot proof required | `REQUIRED_BEFORE_LATER_VISUAL_ACCEPTANCE` |
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
    _write_text("Review Aids/VISUAL_SELECTION_LEDGER_TEMPLATE.md", "# Visual Selection Ledger Template\n\n| Decision ID | Surface | Option ID | Element ID | Accepted / Rejected / Combine / Revise | USER Notes | Source-Truth Impact | Branch-Local Vs Durable Design Principle | Implementation Requirement | Proof Requirement | Future Reuse Note |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| `VSL-001` | AI Dashboard / AI Control Center |  |  |  |  |  |  |  |  |  |")
    _write_text(
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        """
# Draft Branch Visual Acceptance Target

Target ID: `FAM007-VAT-001`

Target Status: `DRAFT`

Target Boundary: `Branch-local guide/template candidate only; not final implemented product truth by itself.`

Recommended Draft Basis: `OPTION-D pending USER selection`

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
""",
    )
    _write_text("Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md", "# Reusable Design Recipe Template\n\nStatus: `TEMPLATE ONLY - fill after USER accepts a Visual Acceptance Target guide. This template is not final implemented product truth by itself.`\n\n| Field | Value |\n| --- | --- |\n| Accepted surface class |  |\n| Accepted footprint class |  |\n| Token values / dimensions |  |\n| Padding |  |\n| Spacing |  |\n| Button heights |  |\n| Font scale |  |\n| Status chip pattern |  |\n| Title/header grammar |  |\n| Resize behavior |  |\n| Copy pattern |  |\n| State pattern |  |\n| Accepted comparator references |  |\n| Rejected alternatives |  |\n| Future branch reuse notes |  |\n| Proof requirements |  |")
    _write_text("Review Aids/SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md", "# Source-Truth Conflict Classification\n\n| Candidate Decision | Classification | Disposition |\n| --- | --- | --- |\n| Require rendered visual target before future visible UI implementation on this branch | `BRANCH_LOCAL_VISUAL_DECISION` | legal branch-local process; Governance/global version is candidate only |\n| Treat current FAM-007 actual screenshot as branch-local target candidate | `NO_CONFLICT` | comparator seed only, not global template promotion |\n| Require FAM-002/UIREF comparison for same-class controls | `NO_CONFLICT` | matches Project Vision, FAM-002, UIREF-001 through UIREF-006 |\n| Promote AI Dashboard / AI Control Center as global gold standard | `GOVERNANCE_CANDIDATE_ONLY` | not done here |\n| Add reusable global helper/validator for all branches | `GOVERNANCE_CANDIDATE_ONLY` | not done here |\n| Implement product/runtime UI change in this pass | `USER_DECISION_REQUIRED` | not approved by this packet |")
    _write_text("Review Aids/GOVERNANCE_CANDIDATE_ONLY.md", "# Governance Candidate Only\n\nCandidate: create a global Visual Acceptance Target process for all future Nexus visible UI/UX work.\n\nReason: FAM-007 and FAM-006 false-green loops show that implementation-first UI work creates repair loops. A global rule should require substantial rendered targets, annotated and clean render media, annotation manifests, element legends, state matrices, full desktop/context renders, rejected-pattern ledgers, reusable design recipes, and implementation-match proof before visible UI work can proceed.\n\nTemplate Boundary: a global visual target process should say that accepted targets are guides/templates/comparators for implementation alignment, not final product truth by themselves.\n\nApproval Needed: USER-approved Governance/FAM-002 carrier after this branch-local process is reviewed. This FAM-007 pass does not mutate Governance and does not promote a global template.")
    _write_text("Review Aids/UDL_FALSE_GREEN_STATUS.md", "# UDL / False-Green Status\n\nCurrent branch has a Unified Defect Ledger and multiple false-green packet/proof repair receipts.\n\nThis visual target packet prevents another implementation-first loop by requiring rendered design candidate media, annotated and clean visual-to-legend mapping, full desktop/context render media, stable element IDs, state coverage, a draft target guide, rejected-pattern ledger, reusable design recipe template, curated decision-relevant packet images, and packet media included in the ZIP.\n\nUDL rows F7-UDL-019, F7-UDL-021, F7-UDL-022, and F7-UDL-023 track annotation readability/bounds, final-packet image relevance, comparative-audit ledgers, and the Option D row-grammar hybrid target candidate. Existing known-bad packet defects remain preserved as historical false-green evidence.")
    _write_text("Review Aids/VALIDATION_SUMMARY.md", "# Packet Check Notes\n\nPacket-local checks are run by `dev/orin_fam007_visual_acceptance_target_packet.py --validate`.\n\nRequired checks include required files, exactly one primary USER review file, render media in the packet, image openability, focused and full desktop/context render media for each option, annotated renders for each option, annotation manifest mapping marker IDs to visual regions, annotation label/leader geometry in bounds, visible marker label text pixels inside each label box, image relevance manifest coverage for every included image, final USER-review image scope, element legend, state matrix, template-not-endstate wording, Visual Selection Ledger template, Draft Branch Visual Acceptance Target, Rejected Patterns Ledger, Reusable Design Recipe template, timestamped ZIP, and folder/ZIP parity.\n\nDetailed command results stay in Codex/helper output and final digest rather than in USER-facing text walls.")

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
        Path(r"C:\Nexus Worktrees"),
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
        targets = _annotation_targets(base_width, height, desktop=desktop)
        for index, (element_id, _cue, _purpose) in enumerate(ANNOTATION_ELEMENTS, start=1):
            marker_id = f"{option_id}-A{index:02d}"
            target_box = targets[element_id]
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
        ],
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md": [
            "Material Difference Rule",
            "Caveat Handling",
            "artifact-to-surface trace",
            "Row Grammar Rule",
            "OPTION-D",
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
        "IMPLEMENTATION_DIFFERENCE_RULE.md",
        "CAVEAT_LEDGER.md",
        "Material visual differences require USER approval",
        "caveat acceptance only records required follow-up",
        "OPTION-D",
        "row grammar",
    ):
        if term.casefold() not in primary_text.casefold():
            failures.append(f"Primary USER decision path missing comparative-audit routing/boundary term: {term}")
    return failures


def generate() -> Path:
    zip_path = USER_ROOT / f"{WORKTREE_LABEL}-{_stamp()}.zip"
    _purge_packet_root()
    _update_external_state(zip_path)
    options = _copy_actual_media() + _generate_candidate_media() + _generate_option_d_media()
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
        for index in range(1, len(ANNOTATION_ELEMENTS) + 1):
            marker_id = f"{option_id}-A{index:02d}"
            if marker_id not in annotation_text:
                failures.append(f"Annotation manifest missing marker: {marker_id}")
    generated_text = ""
    for relative in (
        "START_HERE.md",
        f"USER Review/{PRIMARY_REVIEW_FILE}",
        "Review Aids/VISUAL_OPTIONS_PACKET.md",
        "Review Aids/ELEMENT_LEGENDS.md",
        "Review Aids/ANNOTATION_MANIFEST.md",
        "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
        "Review Aids/DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
        "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
        "Review Aids/CAVEAT_LEDGER.md",
        "Review Aids/STATE_COVERAGE_STORYBOARD.md",
        "Review Aids/REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
        "Review Aids/GOVERNANCE_CANDIDATE_ONLY.md",
        "Review Aids/VALIDATION_SUMMARY.md",
    ):
        path = packet_dir / relative
        if path.exists():
            generated_text += "\n" + path.read_text(encoding="utf-8")
    required_boundary_terms = (
        "not final implemented product truth by itself",
        "code-to-visual proof",
        "clean and annotated render media",
        "OPTION-D",
        "row grammar",
    )
    for term in required_boundary_terms:
        if term not in generated_text:
            failures.append(f"Generated visual packet text missing required boundary wording: {term}")
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
            for required_entry in (
                "Review Aids/ARTIFACT_TO_SURFACE_LEDGER.md",
                "Review Aids/IMPLEMENTATION_DIFFERENCE_RULE.md",
                "Review Aids/CAVEAT_LEDGER.md",
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
