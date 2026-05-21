# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=governance-efficiency-validator; status=shared
"""Validate the governance efficiency operating model.

This helper is intentionally small and report-only. It checks that the compact
governance reform model exists, is discoverable from the routing docs, and keeps
backlog/roadmap from absorbing detailed runtime-branch planning narrative.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPERATING_MODEL = Path("Docs/governance_efficiency_operating_model.md")
DOCS_INVENTORY_AUDIT = Path("Docs/governance_docs_full_inventory_reform_audit.md")
DOCS_REFORM_REVIEW_INDEX = Path("Docs/governance_docs_reform_user_review_index.md")

REQUIRED_MODEL_PHRASES = (
    "Rule ID And Owner Model",
    "Source-Truth Ownership Matrix",
    "Docs Source-Truth Reform Model",
    "Derived Live Truth Versus Historical Receipt",
    "Duplicate Live-State Guard",
    "Current Summary And Historical Appendix Split",
    "Phase Alias UX",
    "Branch Planning UX Standard",
    "Branch Record / Plan / Workstream Fold-Down Model",
    "Product Vision Contract Model",
    "Vision-To-Plan Interaction Loop",
    "USER Feedback Disposition Model",
    "USER Review Integration Decisions",
    "Standing Governance Ledger Compaction",
    "Release Ownership UX",
    "Public Language Mapping",
    "Validator Modularization Boundary",
    "Validation Runner And Registry Query Rule",
    "Naming Drift Scan Rule",
    "Reform Pass Completion Model",
)

POINTER_REQUIREMENTS = {
    Path("Docs/Main.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "governance efficiency operating model",
    ),
    Path("Docs/phase_governance.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "canonical phase names remain unchanged",
    ),
    Path("Docs/development_rules.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "Rule ID",
    ),
    Path("Docs/codex_modes.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "smallest legal",
    ),
    Path("Docs/validation_helper_registry.md"): (
        "dev/orin_governance_efficiency_validation.py",
        "governance efficiency operating model",
    ),
    Path("Docs/branch_records/index.md"): (
        "Docs Source-Truth Reform Model: Compact Pointer Layer",
        "Current Summary And Historical Appendix Split",
        "PR Readiness fold-down",
    ),
    Path("Docs/branch_plans/README.md"): (
        "Docs Source-Truth Reform Model: Compact Pointer Layer",
        "Fold-Down Model",
        "PR Fold-Down Packet:",
        "USER Feedback Disposition",
        "No-Action Reason:",
    ),
    Path("Docs/workstreams/index.md"): (
        "Docs Source-Truth Reform Model: Compact Pointer Layer",
        "Package And Slice Trace Ownership",
        "Package Trace and Slice Trace detail belongs here",
    ),
    Path("Docs/worktree_slots.md"): (
        "Docs Source-Truth Reform Model: Compact Pointer Layer",
        "This file does not own",
        "Assigned slot does not equal active branch authority",
    ),
    Path("Docs/governance_process_efficiency_reform_plan.md"): (
        "Consolidated Governance Reform Pass",
        "Docs/governance_efficiency_operating_model.md",
        "Marker-first governance scaffolding implemented",
        "USER Feedback Disposition",
    ),
}

BACKLOG_ROADMAP_COMPACTNESS_FORBIDDEN = (
    "Package Trace:",
    "Slice Trace:",
    "Per-Seam Implementation Checklist:",
    "Per-Seam Validation Checklist:",
    "Per-Seam User-Facing Proof Checklist:",
    "Plan-To-Implementation Traceability Table:",
    "Hardening Comparison Checklist:",
    "Live Validation Proof Or Waiver Checklist:",
    "PR Readiness Fold-Down / Retention Checklist:",
    "Release Readiness Public-Scope Translation Checklist:",
)

BACKLOG_ROADMAP_CURRENT_STATE_SECTIONS = (
    "## Current Decision Surface",
    "## Current Branch Execution Posture",
    "## Selected Next Workstream",
)

BACKLOG_ROADMAP_CURRENT_STATE_FORBIDDEN = (
    "Latest Public Prerelease Recorded In Source Truth:",
    "Latest Public Prerelease:",
    "Latest Public Release Commit:",
    "Latest Public Prerelease Publication:",
    "Release Candidate Anchor:",
    "Release Window Contributor Inventory:",
    "Merged-Unreleased PRs:",
    "Active Runtime Branch: Branch-local",
    "Active Runtime Branch:",
    "Current Active Workstream: Branch-local",
    "Current active workstream: Branch-local",
    "PR Readiness Stage 2 / PR creation",
    "PR Readiness Stage 2 execution gate",
)

BACKLOG_ROADMAP_CURRENT_STATE_BRANCH_FIELDS = (
    "Selected Next Implementation Branch",
    "Current Carrier Branch",
    "Branch",
)

BACKLOG_ROADMAP_CURRENT_STATE_FORBIDDEN_PATTERNS = (
    (
        r"(?i)\bPR\s+#\d+\s+is\s+open\b",
        "current-state text records an open live PR",
    ),
    (
        r"(?mi)^\s*Live PR(?:\s|:)",
        "current-state text records live PR state",
    ),
    (
        r"(?mi)^\s*(?:Current-Main Reconciliation Update|Release Scope|Release Artifacts|Post-Release Truth):",
        "current-state text records release or branch execution receipt detail",
    ),
    (
        r"\b[0-9a-f]{40}\b",
        "current-state text pins an exact commit hash",
    ),
)

WORKTREE_SLOT_FORBIDDEN = (
    "Latest Public Prerelease Recorded In Source Truth:",
    "Release Candidate Anchor:",
    "Release Window Contributor Inventory:",
    "Merged-Unreleased PRs:",
    "Live PR State:",
    "Review Decision:",
)

BRANCH_RECORD_INDEX_REQUIRED = (
    "Branch records are authority and structured traceability receipt surfaces",
    "Branch records must not become durable family dossiers",
    "Package Trace and Slice Trace detail belongs",
)

BRANCH_PLAN_README_REQUIRED = (
    "Branch plans are canonical while the owning branch is active",
    "At PR Readiness, the `PR Fold-Down Packet:` must classify plan content",
    "It must not preserve stale active phase",
    "USER Feedback Disposition",
    "UFD-<scope>-YYYYMMDD-NNN",
    "No-Action Reason:",
)

WORKSTREAM_INDEX_REQUIRED = (
    "workstreams and family dossiers own durable package trace, slice trace",
    "workstreams and family dossiers must not mirror live Git/GitHub state",
    "Do not promote:",
)

CORE_GOVERNANCE_MIRROR_DOCS = (
    Path("Docs/Main.md"),
    Path("Docs/development_rules.md"),
    Path("Docs/codex_modes.md"),
    Path("Docs/orin_task_template.md"),
    Path("Docs/codex_user_guide.md"),
)

CORE_GOVERNANCE_DUPLICATE_POLICY_FORBIDDEN = (
    "Release Readiness Candidate Anchor: require",
    "Release Window Aggregation Ownership: merge order does not decide release ownership",
)

AUDIT_REQUIRED_SECTIONS = (
    "## Executive Summary",
    "## How To Review This Dossier",
    "## What Was Completed",
    "## What Remains Deferred",
    "## What Requires USER Decision",
    "## USER Review Intake Model",
    "## USER Response Integration Matrix",
    "## Single-PR Staged Execution Plan",
    "## Disposition Changes From USER Review",
    "## High-Risk Files",
    "## Files Safe To Leave For Now",
    "## Files Needing Future Migration",
    "## Files That May Be Retired Later",
    "## Completed / Deferred Matrix",
    "## Source-Truth Ownership Map",
    "## Complete Docs Manifest",
    "## Complete Docs Cleanup / Disposition Table",
    "## Ambiguity Pass",
    "## Structure Pass",
    "## File-by-File Review Table",
    "## Fact-Class Ownership Table",
    "## Duplicate Truth Map",
    "## Backlog Final Schema",
    "## Roadmap Final Schema",
    "## Branch Records Final Schema",
    "## Branch Plans Lifecycle And Retirement Rule",
    "## Branch Runtime Engineering Plan Lifecycle Proof",
    "## Workstreams / Family Dossier Schema",
    "## Worktree Slots Schema",
    "## Governance Docs Ownership Table",
    "## Git / GitHub / Helper-Derived Truth Plan",
    "## Validator Enforcement Table",
    "## File Retirement / Delete Candidate Table",
    "## File-By-File Review Dossier",
    "## PR Readiness Checklist",
    "## Deferred USER Decisions",
    "## Next Legal Phase",
)

INDEX_REQUIRED_SECTIONS = (
    "## Start Here",
    "## Review Proof",
    "## Suggested Review Order",
    "## Decision Checklist",
    "## User Response Intake Status",
    "## USER Response Integration Summary",
    "## Single-PR Staged Execution Plan",
    "## Disposition Changes From USER Review",
    "## Files Needing USER Decision",
    "## Ambiguity Review Queue",
    "## Structure Review Queue",
    "## High-Risk Review Queue",
    "## Future Migration Queue",
    "## Safe To Leave For Now",
    "## Exact USER Decision This Index Supports",
)


def _read(relative_path: Path) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""

    rest = text[start + len(heading) :]
    next_heading = re.search(r"(?m)^##\s+", rest)
    if next_heading:
        return text[start : start + len(heading) + next_heading.start()]
    return text[start:]


def _field_value(line: str, field: str) -> str | None:
    prefix = f"{field}:"
    stripped = line.strip()
    if not stripped.startswith(prefix):
        return None
    return stripped[len(prefix) :].strip().strip("`").strip()


def _is_empty_branch_state(value: str) -> bool:
    normalized = value.casefold()
    return normalized.startswith("none") or normalized.startswith("not created")


def _docs_file_count() -> int:
    docs_root = ROOT / "Docs"
    return sum(1 for path in docs_root.rglob("*") if path.is_file())


def validate() -> list[str]:
    failures: list[str] = []

    model_text = _read(OPERATING_MODEL)
    if not model_text:
        failures.append(f"{OPERATING_MODEL}: missing governance efficiency operating model")
    else:
        for phrase in REQUIRED_MODEL_PHRASES:
            if phrase not in model_text:
                failures.append(
                    f"{OPERATING_MODEL}: missing required section or phrase {phrase!r}"
                )

    for path, required_phrases in POINTER_REQUIREMENTS.items():
        text = _read(path)
        if not text:
            failures.append(f"{path}: missing required pointer document")
            continue
        for phrase in required_phrases:
            if phrase not in text:
                failures.append(f"{path}: missing governance efficiency pointer {phrase!r}")

    audit_text = _read(DOCS_INVENTORY_AUDIT)
    if not audit_text:
        failures.append(f"{DOCS_INVENTORY_AUDIT}: missing full Docs reform audit dossier")
    else:
        for section in AUDIT_REQUIRED_SECTIONS:
            if section not in audit_text:
                failures.append(
                    f"{DOCS_INVENTORY_AUDIT}: missing required review section {section!r}"
                )
        docs_count = _docs_file_count()
        audit_count_match = re.search(
            r"Audit File Count:\s*(\d+)\s+files under `Docs/`",
            audit_text,
        )
        manifest_count_match = re.search(r"Manifest Files Enumerated:\s*(\d+)", audit_text)
        audit_count = int(audit_count_match.group(1)) if audit_count_match else -1
        manifest_count = int(manifest_count_match.group(1)) if manifest_count_match else -1
        if audit_count != docs_count:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: Audit File Count {audit_count} does not "
                f"match filesystem Docs file count {docs_count}"
            )
        if manifest_count != docs_count:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: Manifest Files Enumerated {manifest_count} "
                f"does not match filesystem Docs file count {docs_count}"
            )
        dossier_entries = len(
            re.findall(r"(?m)^###\s+\d+\.\s+`Docs/", audit_text)
        )
        if dossier_entries != docs_count:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: File-By-File Review Dossier has "
                f"{dossier_entries} entries, expected {docs_count}"
            )
        disposition_rows = len(
            re.findall(
                r"(?m)^\| `Docs/",
                _section(audit_text, "## Complete Docs Cleanup / Disposition Table"),
            )
        )
        if disposition_rows != docs_count:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: cleanup/disposition table has "
                f"{disposition_rows} file rows, expected {docs_count}"
            )
        ambiguity_rows = len(
            re.findall(r"(?m)^\| `Docs/", _section(audit_text, "## Ambiguity Pass"))
        )
        if ambiguity_rows != docs_count:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: Ambiguity Pass has "
                f"{ambiguity_rows} file rows, expected {docs_count}"
            )
        structure_rows = len(
            re.findall(r"(?m)^\| `Docs/", _section(audit_text, "## Structure Pass"))
        )
        if structure_rows != docs_count:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: Structure Pass has "
                f"{structure_rows} file rows, expected {docs_count}"
            )
        if "dev/orin_docs_inventory_reform_audit.py" not in audit_text:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: missing generator helper reference"
            )
        if str(DOCS_REFORM_REVIEW_INDEX).replace("\\", "/") not in audit_text:
            failures.append(
                f"{DOCS_INVENTORY_AUDIT}: missing user review index pointer"
            )

    index_text = _read(DOCS_REFORM_REVIEW_INDEX)
    if not index_text:
        failures.append(f"{DOCS_REFORM_REVIEW_INDEX}: missing user review index")
    else:
        for section in INDEX_REQUIRED_SECTIONS:
            if section not in index_text:
                failures.append(
                    f"{DOCS_REFORM_REVIEW_INDEX}: missing required review section {section!r}"
                )
        if str(DOCS_INVENTORY_AUDIT).replace("\\", "/") not in index_text:
            failures.append(
                f"{DOCS_REFORM_REVIEW_INDEX}: missing full dossier pointer"
            )
        docs_count = _docs_file_count()
        index_count_match = re.search(r"Docs files covered:\s*(\d+)", index_text)
        index_count = int(index_count_match.group(1)) if index_count_match else -1
        if index_count != docs_count:
            failures.append(
                f"{DOCS_REFORM_REVIEW_INDEX}: Docs files covered {index_count} "
                f"does not match filesystem Docs file count {docs_count}"
            )

    for path in (Path("Docs/feature_backlog.md"), Path("Docs/prebeta_roadmap.md")):
        text = _read(path)
        if not text:
            failures.append(f"{path}: missing compact current-state owner")
            continue
        for phrase in BACKLOG_ROADMAP_COMPACTNESS_FORBIDDEN:
            if phrase in text:
                failures.append(
                    f"{path}: detailed source-truth marker {phrase!r} belongs in "
                    "Docs/workstreams, Docs/branch_plans, or folded historical receipts, "
                    "not backlog/roadmap"
                )
        if "Docs Source-Truth Reform Model: Compact Pointer Layer" not in text:
            failures.append(
                f"{path}: missing Docs Source-Truth Reform Model compact pointer marker"
            )

        current_state_text = "\n".join(
            _section(text, heading) for heading in BACKLOG_ROADMAP_CURRENT_STATE_SECTIONS
        )
        for phrase in BACKLOG_ROADMAP_CURRENT_STATE_FORBIDDEN:
            if phrase in current_state_text:
                failures.append(
                    f"{path}: current-state section carries branch-local/live-state phrase "
                    f"{phrase!r}; backlog/roadmap must stay compact and route active branch "
                    "identity to branch authority records, branch plans, or historical receipts"
                )
        for line in current_state_text.splitlines():
            for field in BACKLOG_ROADMAP_CURRENT_STATE_BRANCH_FIELDS:
                value = _field_value(line, field)
                if value is not None and not _is_empty_branch_state(value):
                    failures.append(
                        f"{path}: current-state field {field!r} carries branch-local/live-state "
                        "identity; backlog/roadmap must stay compact and route active branch "
                        "identity to branch authority records, branch plans, or historical receipts"
                    )
        for pattern, label in BACKLOG_ROADMAP_CURRENT_STATE_FORBIDDEN_PATTERNS:
            if re.search(pattern, current_state_text):
                failures.append(
                    f"{path}: current-state section carries branch-local/live-state pattern "
                    f"{label!r}; backlog/roadmap must stay compact and route active branch "
                    "identity to branch authority records, branch plans, or historical receipts"
                )

    worktree_slots_text = _read(Path("Docs/worktree_slots.md"))
    for phrase in WORKTREE_SLOT_FORBIDDEN:
        if phrase in worktree_slots_text:
            failures.append(
                "Docs/worktree_slots.md: slot registry must not carry live release, "
                f"release-window, PR, or review-state field {phrase!r}"
            )
    if re.search(r"\b[0-9a-f]{40}\b", _section(worktree_slots_text, "Standing Slot Receipts")):
        failures.append(
            "Docs/worktree_slots.md: standing slot receipts must not pin exact live commit hashes"
        )

    branch_record_index_text = _read(Path("Docs/branch_records/index.md"))
    for phrase in BRANCH_RECORD_INDEX_REQUIRED:
        if phrase not in branch_record_index_text:
            failures.append(
                f"Docs/branch_records/index.md: missing branch-record reform rule {phrase!r}"
            )

    branch_plan_readme_text = _read(Path("Docs/branch_plans/README.md"))
    for phrase in BRANCH_PLAN_README_REQUIRED:
        if phrase not in branch_plan_readme_text:
            failures.append(
                f"Docs/branch_plans/README.md: missing branch-plan fold-down rule {phrase!r}"
            )

    workstream_index_text = _read(Path("Docs/workstreams/index.md"))
    for phrase in WORKSTREAM_INDEX_REQUIRED:
        if phrase not in workstream_index_text:
            failures.append(
                f"Docs/workstreams/index.md: missing workstream trace ownership rule {phrase!r}"
            )

    for path in CORE_GOVERNANCE_MIRROR_DOCS:
        text = _read(path)
        for phrase in CORE_GOVERNANCE_DUPLICATE_POLICY_FORBIDDEN:
            if phrase in text:
                failures.append(
                    f"{path}: duplicate full release-readiness policy {phrase!r} "
                    "belongs in Docs/phase_governance.md; mirror docs should point to "
                    "the owner instead of repeating full policy prose"
                )

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: governance efficiency validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: governance efficiency validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
