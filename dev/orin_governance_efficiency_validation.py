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
    "Branch records are authority and compact receipt surfaces",
    "Branch records must not become durable family dossiers",
    "Package Trace and Slice Trace detail belongs",
)

BRANCH_PLAN_README_REQUIRED = (
    "Branch plans are canonical while the owning branch is active",
    "At PR Readiness, the `PR Fold-Down Packet:` must classify plan content",
    "It must not preserve stale active phase",
)

WORKSTREAM_INDEX_REQUIRED = (
    "workstreams and family dossiers own durable package trace, slice trace",
    "workstreams and family dossiers must not mirror live Git/GitHub state",
    "Do not promote:",
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
