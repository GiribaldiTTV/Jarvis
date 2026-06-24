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


STANDARD_PACKET_LABEL = "FAM-003"
RETIRED_PACKET_LABELS = ("FAM-003-Visual-Acceptance",)
RENDER_MEDIA_PREFIX = "Source Truth Context/Proof Artifacts/Visual Target Render Media"
DEFAULT_PACKET_DIR = Path(r"C:\Nexus USER\FAM-003")
DEFAULT_STATE_ROOT = Path(
    r"C:\Nexus Governance State\branches\feature_fam_003_resident_access_quick_actions"
)
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
    "ARTIFACT_TO_SURFACE_LEDGER.md",
    "PACKET_MANIFEST.md",
    "VALIDATION_RESULTS.md",
)
REQUIRED_RENDER_FILES = tuple(
    f"{RENDER_MEDIA_PREFIX}/Option {option}/{name}.png"
    for option in ("A", "B", "C", "D", "E", "F")
    for name in ("focused_surface", "desktop_context", "state_matrix")
) + (f"{RENDER_MEDIA_PREFIX}/visual_options_contact_sheet.png",)
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
        "C/A Hybrid",
        "Polished NDAI Compact Shell",
        "Deterministic Dirty Guard",
        "Branch-Local Visual Acceptance Target overlay",
        "USER/ChatGPT UI findings are seed defects",
        "Codex Independent Evidence Inspection",
        "Durable repo-wide",
        "GOV-VAT-001",
        "GOV-VAT-002",
        "GOV-VAT-003",
    )
    for marker in required_markers:
        if marker not in combined_user_text and marker not in "\n".join(
            _read_text(packet_dir / "Review Aids" / aid)
            for aid in REQUIRED_REVIEW_AIDS
            if (packet_dir / "Review Aids" / aid).exists()
        ):
            failures.append(f"required marker missing from packet text: {marker}")

    for state_file in REQUIRED_STATE_FILES:
        if not (state_root / state_file).exists():
            failures.append(f"external visual-target state file missing: {state_file}")

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
