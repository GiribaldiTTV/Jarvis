"""Validate the FAM-003 visual acceptance target USER packet.

This helper is branch-local proof support only. It validates packet shape,
required visual-target decision artifacts, and render-media presence. It does
not prove USER acceptance, Live Validation green, or implementation match.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

from nexus_paths import EXTERNAL_STATE_ROOT, USER_HUB_ROOT

STANDARD_PACKET_LABEL = "FAM-003"
RETIRED_PACKET_LABELS = ("FAM-003-Visual-Acceptance",)
RENDER_MEDIA_PREFIX = "Source Truth Context/Proof Artifacts/Visual Target Render Media"
DEFAULT_PACKET_DIR = USER_HUB_ROOT / "FAM-003"
DEFAULT_STATE_ROOT = EXTERNAL_STATE_ROOT / "branches" / "feature_fam_003_resident_access_quick_actions"
REQUIRED_REVIEW_AIDS = (
    "VISUAL_IMPACT_CLASSIFICATION.md",
    "VISUAL_OPTIONS_PACKET.md",
    "ELEMENT_LEGENDS_AND_STATE_COVERAGE.md",
    "VISUAL_SELECTION_LEDGER_TEMPLATE.md",
    "DRAFT_BRANCH_VISUAL_ACCEPTANCE_TARGET.md",
    "REJECTED_PATTERNS_LEDGER.md",
    "REUSABLE_DESIGN_RECIPE_TEMPLATE.md",
    "SOURCE_TRUTH_CONFLICT_CLASSIFICATION.md",
    "UDL_FALSE_GREEN_INTEGRATION.md",
    "GOVERNANCE_CANDIDATE_ONLY.md",
    "BRANCH_LOCAL_GOVERNANCE_HARDENING.md",
    "GOVERNANCE_SOURCE_TRUTH_PROOF.md",
    "ARTIFACT_TO_SURFACE_LEDGER.md",
    "PACKET_MANIFEST.md",
    "VALIDATION_RESULTS.md",
)
REQUIRED_RENDER_FILES = tuple(
    f"{RENDER_MEDIA_PREFIX}/Option {option}/{name}.png"
    for option in ("A", "B", "C", "D", "E", "F", "G", "G2")
    for name in ("focused_surface", "annotated_focused_surface", "desktop_context", "state_matrix")
) + (
    *(
        f"{RENDER_MEDIA_PREFIX}/Option G/{name}.png"
        for name in (
            "tray_parent_page",
            "annotated_tray_parent_page",
            "quick_access_child_page",
            "annotated_quick_access_child_page",
            "dropdown_open_state",
            "annotated_dropdown_open_state",
            "dirty_unsaved_state",
            "annotated_dirty_unsaved_state",
            "close_guard_state",
            "annotated_close_guard_state",
        )
    ),
    *(
        f"{RENDER_MEDIA_PREFIX}/Option G2/{name}.png"
        for name in (
            "tray_parent_page",
            "annotated_tray_parent_page",
            "quick_access_child_page",
            "annotated_quick_access_child_page",
            "dropdown_open_state",
            "annotated_dropdown_open_state",
            "dirty_unsaved_state",
            "annotated_dirty_unsaved_state",
            "close_guard_state",
            "annotated_close_guard_state",
        )
    ),
    f"{RENDER_MEDIA_PREFIX}/visual_options_contact_sheet.png",
    f"{RENDER_MEDIA_PREFIX}/visual_options_annotated_contact_sheet.png",
)
REQUIRED_STATE_FILES = (
    "visual_acceptance_target_process_20260624.md",
    "visual_impact_classification_20260624.md",
    "visual_options_packet_20260624.md",
    "draft_branch_visual_acceptance_target_20260624.md",
    "visual_selection_ledger_template_20260624.md",
    "rejected_patterns_ledger_20260624.md",
    "reusable_design_recipe_template_20260624.md",
    "source_truth_conflict_classification_20260624.md",
    "udl_false_green_integration_20260624.md",
    "visual_acceptance_governance_hardening_20260624.md",
    "governance_proof_packet_repair_20260624.md",
    "visual_acceptance_target_validation_results_20260624.md",
)
FORBIDDEN_ACTIVE_REVIEW_PATTERNS = (
    re.compile(r"\bUSER_BRANCH_PLAN_REVIEW\.md\b", re.IGNORECASE),
    re.compile(r"\bGenerated BP2 Branch Plan Review\b", re.IGNORECASE),
    re.compile(r"\bBP2 gate remains open\b", re.IGNORECASE),
    re.compile(r"\bPR-ready\s*[:=]\s*(YES|PASS|TRUE)\b", re.IGNORECASE),
    re.compile(r"\bLV green\s*[:=]\s*(YES|PASS|TRUE)\b", re.IGNORECASE),
)


def _iter_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def _relative_files(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in _iter_files(root)}


def _file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in _iter_files(root):
        hashes[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def _zip_hashes(zip_path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    with zipfile.ZipFile(zip_path, "r") as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            normalized = PurePosixPath(info.filename).as_posix()
            hashes[normalized] = hashlib.sha256(archive.read(info.filename)).hexdigest()
    return hashes


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate(packet_dir: Path, packet_zip: Path | None, state_root: Path) -> list[str]:
    failures: list[str] = []
    if packet_dir.name != STANDARD_PACKET_LABEL:
        failures.append(
            f"nonstandard packet folder name: {packet_dir.name}; expected {STANDARD_PACKET_LABEL}"
        )
    for retired_label in RETIRED_PACKET_LABELS:
        retired_root = packet_dir.parent / retired_label
        if retired_root.exists():
            failures.append(f"retired nonstandard packet folder still exists: {retired_root}")
        retired_stable_zip = packet_dir.parent / f"{retired_label}.zip"
        if retired_stable_zip.exists():
            failures.append(f"retired nonstandard stable ZIP still exists: {retired_stable_zip}")
        for retired_zip in packet_dir.parent.glob(f"{retired_label}-*.zip"):
            failures.append(f"retired nonstandard timestamped ZIP still exists: {retired_zip}")
    if not packet_dir.exists():
        return [f"packet folder missing: {packet_dir}"]

    packet_files = _relative_files(packet_dir)
    if "START_HERE.md" not in packet_files:
        failures.append("START_HERE.md missing")
    for folder in ("USER Review", "Review Aids", "Source Truth Context"):
        if not (packet_dir / folder).is_dir():
            failures.append(f"{folder}/ folder missing")

    primary_reviews = [
        entry
        for entry in packet_files
        if entry.startswith("USER Review/") and entry.lower().endswith(".md")
    ]
    if primary_reviews != ["USER Review/FAM003_VISUAL_ACCEPTANCE_TARGET_REVIEW.md"]:
        failures.append(f"unexpected primary USER review files: {primary_reviews}")

    for aid in REQUIRED_REVIEW_AIDS:
        if f"Review Aids/{aid}" not in packet_files:
            failures.append(f"missing review aid: {aid}")
    for media in REQUIRED_RENDER_FILES:
        if media not in packet_files:
            failures.append(f"missing render media: {media}")

    combined_user_text = ""
    for entry in ("START_HERE.md", *primary_reviews):
        path = packet_dir / PurePosixPath(entry)
        if path.exists():
            combined_user_text += f"\n--- {entry} ---\n{_read_text(path)}"
    for pattern in FORBIDDEN_ACTIVE_REVIEW_PATTERNS:
        if pattern.search(combined_user_text):
            failures.append(f"forbidden active review wording: {pattern.pattern}")

    review_aid_text = "\n".join(
        _read_text(packet_dir / "Review Aids" / aid)
        for aid in REQUIRED_REVIEW_AIDS
        if (packet_dir / "Review Aids" / aid).exists()
    )
    governance_proof_text = ""
    governance_proof_root = packet_dir / "Source Truth Context" / "Governance Proof"
    if governance_proof_root.exists():
        governance_proof_text = "\n".join(
            _read_text(path)
            for path in sorted(governance_proof_root.rglob("*"))
            if path.is_file() and path.suffix.lower() in {".md", ".patch", ".txt"}
        )
    supporting_text = "\n".join((review_aid_text, governance_proof_text))

    required_markers = (
        "Design Candidate Render",
        "Visual Acceptance Target",
        "USER_ACCEPTED",
        "not LV green",
        "not UTS complete",
        "not PR-ready",
        "Visual Selection Ledger",
        "Rejected Patterns Ledger",
        "Reusable Design Recipe",
        "Implementation Match Proof",
        "VAT-OPT-D",
        "VAT-OPT-E",
        "VAT-OPT-F",
        "VAT-OPT-G",
        "VAT-OPT-G2",
        "C/A Hybrid",
        "Polished NDAI Compact Shell",
        "Deterministic Dirty Guard",
        "D/E/F Consolidated Visual Target",
        "Final Clean G",
        "3 active of 4",
        "Tray is its own selectable parent page",
        "Quick Access is a child page under Tray",
        "Save / Discard / Cancel appear only in the close-guard state",
        "AI Status / Command Center doorway",
        "FAM-007-owned doorway only",
        "product-copy cleanup",
        "space-efficiency cleanup",
        "naming cleanup",
        "Command Overlay",
        "Create Task",
        "Saved Actions",
        "Tray Help",
        "current runtime source still has BP2 maximum 5",
        "Branch-Local Visual Acceptance Target overlay",
        "USER/ChatGPT UI findings are seed defects",
        "Codex Independent Evidence Inspection",
        "Durable repo-wide",
        "GOV-VAT-001",
        "GOV-VAT-002",
        "GOV-VAT-003",
        "GOV-VAT-004",
        "GOV-VAT-005",
        "GOV-VAT-006",
        "VIS-VAT-001",
        "VIS-VAT-002",
        "VIS-VAT-003",
        "VIS-VAT-004",
        "VIS-VAT-005",
        "VIS-VAT-006",
        "Governance Source-Truth Proof",
        "HARDENING_COMMIT_BOUNDED_DIFF.patch",
        "CURRENT_REPAIR_BOUNDED_DIFF.patch",
        "Changed File Snapshots",
        "actual pre-archive command receipts",
        "Legend / Callout Traceability",
        "color-coded",
        "text-labeled callouts",
        "annotated_focused_surface.png",
        "annotated_tray_parent_page.png",
        "annotated_quick_access_child_page.png",
        "annotated_dropdown_open_state.png",
        "annotated_dirty_unsaved_state.png",
        "annotated_close_guard_state.png",
        "Option G2/dropdown_open_state.png",
        "Option G2/annotated_close_guard_state.png",
        "visual_options_annotated_contact_sheet.png",
        "guide/template",
        "not a guaranteed literal final",
        "Implementation Match Proof must compare actual app evidence",
        "PENDING_EXTERNAL_POST_ZIP_RECEIPT",
    )
    for marker in required_markers:
        if marker not in combined_user_text and marker not in supporting_text:
            failures.append(f"required marker missing from packet text: {marker}")

    for state_file in REQUIRED_STATE_FILES:
        if not (state_root / state_file).exists():
            failures.append(f"external visual-target state file missing: {state_file}")
    governance_diff = (
        packet_dir
        / "Source Truth Context"
        / "Governance Proof"
        / "HARDENING_COMMIT_BOUNDED_DIFF.patch"
    )
    if not governance_diff.exists():
        failures.append("governance hardening bounded diff artifact missing")
    else:
        diff_text = _read_text(governance_diff)
        for expected in (
            "Harden FAM-003 visual acceptance governance",
            "Docs/phase_governance.md",
            "Docs/validation_helper_registry.md",
            "dev/orin_fam003_visual_acceptance_target_packet.py",
            "dev/orin_fam003_visual_acceptance_target_validation.py",
        ):
            if expected not in diff_text:
                failures.append(f"governance hardening bounded diff missing marker: {expected}")
    snapshots_dir = packet_dir / "Source Truth Context" / "Governance Proof" / "Changed File Snapshots"
    if not snapshots_dir.is_dir():
        failures.append("governance changed-file snapshots folder missing")
    else:
        for expected_snapshot in (
            "Docs__phase_governance.md",
            "Docs__validation_helper_registry.md",
            "Docs__branch_records__feature_fam_003_resident_access_quick_actions.md",
            "dev__orin_fam003_visual_acceptance_target_packet.py",
            "dev__orin_fam003_visual_acceptance_target_validation.py",
        ):
            if not (snapshots_dir / expected_snapshot).exists():
                failures.append(f"governance changed-file snapshot missing: {expected_snapshot}")
    validation_receipts = (
        packet_dir
        / "Source Truth Context"
        / "Governance Proof"
        / "VALIDATION_COMMAND_RECEIPTS.md"
    )
    if not validation_receipts.exists():
        failures.append("governance validation command receipts missing")
    else:
        receipts_text = _read_text(validation_receipts)
        self_check_pending = "Packet validator self-check: `PENDING_CURRENT_RUN`" in receipts_text
        final_pass_recorded = "Packet validator self-check: `FINAL_PASS_RECORDED`" in receipts_text
        if final_pass_recorded and re.search(r"\|\s*`\d+`\s*\|\s*`FAIL`\s*\|", receipts_text):
            failures.append("active final validation command receipts contain FAIL")
        for expected in (
            "Validation Command Receipts",
            "git show --stat",
            "git diff --check",
            "origin/main...HEAD",
        ):
            if expected not in receipts_text:
                failures.append(f"governance validation command receipts missing marker: {expected}")
        if (
            "PASS: FAM-003 visual acceptance target packet is complete and reviewable"
            not in receipts_text
            and not self_check_pending
        ):
            failures.append(
                "governance validation command receipts missing marker: "
                "PASS: FAM-003 visual acceptance target packet is complete and reviewable"
            )
        if not self_check_pending and not final_pass_recorded:
            failures.append("validation receipts missing packet-validator self-check disposition")

    current_repair_diff = (
        packet_dir
        / "Source Truth Context"
        / "Governance Proof"
        / "CURRENT_REPAIR_BOUNDED_DIFF.patch"
    )
    if not current_repair_diff.exists():
        failures.append("current repair bounded diff artifact missing")
    else:
        current_diff_text = _read_text(current_repair_diff)
        for expected in (
            "VIS-VAT-001",
            "VIS-VAT-002",
            "VIS-VAT-003",
            "VIS-VAT-004",
            "VIS-VAT-005",
            "VIS-VAT-006",
            "GOV-VAT-005",
            "GOV-VAT-006",
            "annotated_focused_surface.png",
            "annotated_close_guard_state.png",
            "VAT-OPT-G",
            "VAT-OPT-G2",
            "Final Clean G",
            "visual_options_annotated_contact_sheet.png",
            "not a guaranteed literal final",
        ):
            if expected not in current_diff_text:
                failures.append(f"current repair bounded diff missing marker: {expected}")

    if packet_zip is not None:
        if not packet_zip.exists():
            failures.append(f"packet ZIP missing: {packet_zip}")
        else:
            if not re.fullmatch(rf"{re.escape(STANDARD_PACKET_LABEL)}-\d{{8}}-\d{{6}}\.zip", packet_zip.name):
                failures.append(
                    f"nonstandard packet ZIP name: {packet_zip.name}; expected "
                    f"{STANDARD_PACKET_LABEL}-YYYYMMDD-HHMMSS.zip"
                )
            if packet_zip.parent != packet_dir.parent:
                failures.append(
                    f"packet ZIP must live beside packet folder: {packet_zip.parent} != {packet_dir.parent}"
                )
            legacy_stable_zip = packet_dir.parent / f"{STANDARD_PACKET_LABEL}.zip"
            if legacy_stable_zip.exists():
                failures.append(f"legacy stable packet ZIP still exists: {legacy_stable_zip}")
            stale_zips = [
                path
                for path in packet_dir.parent.glob(f"{STANDARD_PACKET_LABEL}-*.zip")
                if path.resolve() != packet_zip.resolve()
            ]
            for stale_zip in stale_zips:
                failures.append(f"stale same-label timestamped ZIP still exists: {stale_zip}")
            folder_hashes = _file_hashes(packet_dir)
            zip_hashes = _zip_hashes(packet_zip)
            if folder_hashes != zip_hashes:
                missing = sorted(set(folder_hashes) - set(zip_hashes))
                extra = sorted(set(zip_hashes) - set(folder_hashes))
                mismatched = sorted(
                    key
                    for key in set(folder_hashes).intersection(zip_hashes)
                    if folder_hashes[key] != zip_hashes[key]
                )
                failures.append(
                    "folder/ZIP parity failed: "
                    f"missing={missing}; extra={extra}; mismatched={mismatched}"
                )
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-folder", type=Path, default=DEFAULT_PACKET_DIR)
    parser.add_argument("--packet-zip", type=Path)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    args = parser.parse_args(argv)

    failures = validate(args.packet_folder, args.packet_zip, args.state_root)
    if failures:
        print("FAIL: FAM-003 visual acceptance target packet validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: FAM-003 visual acceptance target packet is complete and reviewable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
