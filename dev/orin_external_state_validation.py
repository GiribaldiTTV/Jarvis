from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import re
from pathlib import PureWindowsPath

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    REQUIRED_STATE_FIELDS,
    iter_state_files,
    load_json,
    resolve_path,
    sha256_file,
    validate_canonical_root,
    validate_initialized_root,
)


REQUIRED_STAGE4_RECORDS = [
    "central/active_branch_authority_state.md",
    "central/selected_next_state.md",
    "worktrees/Governance/worktree_state.md",
    "branches/feature_release_readiness_source_truth_intake/branch_state.md",
    "branches/feature_release_readiness_source_truth_intake/branch_plan.md",
    "branches/feature_release_readiness_source_truth_intake/ufd_ledger.md",
    "branches/feature_release_readiness_source_truth_intake/change_intent_ledger.md",
    "branches/feature_release_readiness_source_truth_intake/element_to_phase_matrix.md",
    "branches/feature_release_readiness_source_truth_intake/pr_readiness_state.md",
    "release_windows/current_release_window_state.md",
    "review_bundles/Governance/manifest.md",
    "cross_worktree_lessons/queue_state.md",
    "governance_candidates/queue_state.md",
    "promotion_packets/stage4_active_state_migration_execution_20260526.md",
    "acknowledgements/Governance/stage4_active_state_migration_execution_ack.md",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate External Governance State scaffold posture.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--repo", action="append", default=[], help="Repo path that root must not live inside")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA_VERSION)
    parser.add_argument(
        "--require-root",
        action="store_true",
        help="Fail when the external root is absent. Omit for clean-clone-safe local report mode.",
    )
    parser.add_argument(
        "--require-stage4-records",
        action="store_true",
        help=(
            "Require the approved Stage 4 active-state migration record set. "
            "Use only for approved local external-state workflows, not clean-clone CI."
        ),
    )
    parser.add_argument(
        "--expected-source-head",
        help="Expected Source Repo HEAD for the manifest and required migrated markdown records.",
    )
    parser.add_argument(
        "--target-currentness",
        action="store_true",
        help=(
            "Run additive target-scoped currentness validation. This mode requires one explicit "
            "relative target and per-target identity expectations; it does not claim root-wide currentness."
        ),
    )
    parser.add_argument(
        "--projection-set-semantic-coherence",
        action="store_true",
        help=(
            "Validate a selected set of live projections as one semantic transition. This mode "
            "requires explicit target hashes, prior snapshot, completion audit, and primary review."
        ),
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Relative external-state record path for --target-currentness. Repeat only to prove duplicate-target rejection.",
    )
    parser.add_argument("--expected-branch", help="Expected Branch value for the selected target record.")
    parser.add_argument("--expected-origin-main", help="Expected origin/main value for the selected target record.")
    parser.add_argument("--expected-worktree-path", help="Expected Worktree Path value for the selected target record.")
    parser.add_argument("--expected-worktree-slot", help="Expected Slot ID value for the selected target record.")
    parser.add_argument(
        "--expected-target-sha256",
        help="Expected SHA256 of the selected target record before validation (TOCTOU precondition).",
    )
    parser.add_argument(
        "--expected-target-hash",
        action="append",
        default=[],
        metavar="TARGET=SHA256",
        help="Expected target/hash pair for projection-set semantic validation. Repeat per target.",
    )
    parser.add_argument("--expected-current-gate")
    parser.add_argument("--expected-workstream-result")
    parser.add_argument("--expected-stage-states")
    parser.add_argument("--expected-next-legal-phase")
    parser.add_argument("--expected-transition-status")
    parser.add_argument("--expected-state-version", type=int)
    parser.add_argument("--expected-last-updated-by")
    parser.add_argument("--previous-snapshot")
    parser.add_argument("--completion-audit")
    parser.add_argument("--primary-review")
    parser.add_argument("--expected-decision-1")
    parser.add_argument("--expected-decision-2")
    parser.add_argument("--expected-decision-3")
    parser.add_argument(
        "--expected-completion-transition-status",
        default="MIGRATION_COMPLETE",
        help=(
            "Expected Transition Status in the completion audit. Defaults to the "
            "legacy migration completion value; later governed transitions must pass "
            "their exact audited status explicitly."
        ),
    )
    return parser


def validate_manifest(manifest_path: Path, expected_schema: str) -> list[str]:
    issues: list[str] = []
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:  # noqa: BLE001 - corrupt local state should become a validation issue
        return [f"External State Corrupt: {manifest_path}: {exc}"]
    for field in REQUIRED_STATE_FIELDS:
        if field not in manifest:
            issues.append(f"Missing required manifest field: {field}")
    schema = manifest.get("External State Schema")
    if schema != expected_schema:
        issues.append(
            f"External State Schema Conflict: expected {expected_schema}, found {schema or 'MISSING'}"
        )
    return issues


def markdown_field_value(text: str, field: str) -> str | None:
    pattern = re.compile(
        rf"^\s*(?:-\s*)?{re.escape(field)}:\s*(.*?)\s*$",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
        return value[1:-1].strip()
    return value


TARGET_LIVE_RECORD_CLASSES = {
    "live worktree projection",
    "live branch projection",
    "live branch plan",
    "live branch plan projection",
    "live central authority projection",
    "live selected-next projection",
    "live release-window projection",
    "live review-bundle projection",
}
TARGET_HISTORICAL_RECORD_CLASSES = {
    "historical receipt",
    "historical projection",
    "accepted historical receipt",
}


def _normalized_windows_value(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().strip("`").replace("/", "\\").rstrip("\\").casefold()


def _first_markdown_field(text: str, fields: tuple[str, ...]) -> str | None:
    for field in fields:
        value = markdown_field_value(text, field)
        if value:
            return value
    return None


def _live_header_text(text: str) -> str:
    """Restrict currentness parsing to the live header before receipt sections."""

    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        if re.match(r"^\s*(?:-\s*)?Historical Receipt Boundary:\s*", content):
            return "".join(lines[: index + 1])
    for index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        if content.lstrip("\ufeff").startswith("## "):
            return "".join(lines[:index])
    return "".join(lines)


FAM003_OPTION_G_BRANCH = "feature/fam-003-settings-resize-proof"
FAM003_OPTION_G_UFD_COUNT = 18
FAM003_OPTION_G_UFD_FOLD_DOWN_TARGET = (
    "Docs/branch_records/feature_fam_003_settings_resize_proof.md"
)
FAM003_OPTION_G_VISION_HEADING = "## Branch Vision Contract Snapshot"
FAM003_OPTION_G_VISION_MARKERS = (
    "Vision Contract Required:",
    "Vision Contract Requirement Reason:",
    "Branch Vision Snapshot Status:",
    "Open Vision Questions:",
    "USER Vision Green:",
    "Implementation Scope:",
    "Seam Map:",
    "Stop Conditions:",
    "Design Assumption Ledger:",
    "Vision Question Queue:",
    "Question Severity Policy:",
    "Vision-to-Implementation Traceability:",
    "Branch Plan Revision Packet:",
    "Project Vision Owner:",
    "Project Vision SHA256:",
    "FAM-003 Family Vision Owner:",
    "FAM-003 Family Vision SHA256:",
    "F3-FF01 Owner:",
    "F3-FF01 SHA256:",
    "Accepted BP1 Owner:",
    "Accepted BP1 SHA256:",
    "Accepted BP1 Acceptance Receipt:",
    "Accepted BP2 Owner:",
    "Accepted BP2 SHA256:",
    "Accepted BP2 Acceptance Receipt:",
    "Accepted BP2 Acceptance Receipt SHA256:",
)
UFD_CONTEXT_RELATIVE_LOCATION_RE = re.compile(
    r"\b(?:this|the)\s+annex\b"
    r"|\bthis supporting record\b"
    r"|\bthe record above\b",
    re.IGNORECASE,
)
FAM003_OPTION_G_UFD_ITEM_MARKERS = (
    "Feedback ID:",
    "Feedback Summary:",
    "Feedback Source:",
    "Feedback Phase:",
    "Disposition Type:",
    "USER Decision State:",
    "Owner Class:",
    "Canonical Owner File:",
    "Workstream Severity:",
    "Status:",
    "Fold-Down Target:",
    "Pointer Locations:",
    "Source / Date:",
    "USER Direction Or Finding:",
    "Affected Scope:",
    "Affected Artifact:",
    "Classification:",
    "Owner:",
    "Carrier:",
    "Planning Or Implementation Effect:",
    "Proof / Closure Requirement:",
    "Remaining USER Decision:",
)
ELEMENT_TO_PHASE_HEADING = "## Element-to-Phase Proof Matrix"
ELEMENT_TO_PHASE_HEADER = (
    "Element ID",
    "Element / Surface",
    "Element Classification",
    "Workstream Implementation Plan",
    "Workstream Proof Plan",
    "Hardening Proof Plan",
    "Live Validation Proof / Waiver Plan",
    "UTS / USER Acceptance Path",
    "Future / Deferred Boundary",
    "USER Decision State",
    "Source Owner / Ledger Owner",
)
ELEMENT_TO_PHASE_CLASSIFICATIONS = {
    "Planned",
    "Created",
    "Touched",
    "Affected",
    "Deferred",
    "Future",
    "Dependency-Only",
    "Non-Gating Supporting",
}
FAM003_OPTION_G_ELEMENT_IDS = tuple(
    f"OPTG-ELEM-{index:02d}" for index in range(1, 12)
)


def _markdown_table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped[1:-1].split("|")]


def _element_to_phase_section(live_text: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(ELEMENT_TO_PHASE_HEADING)}\s*\n"
        r"(.*?)(?=^Historical Receipt Boundary:|^## |\Z)",
        live_text,
    )
    return match.group(0).rstrip() if match else ""


def _validate_active_branch_plan_element_matrix(
    relative: str,
    live_text: str,
) -> list[str]:
    """Validate the physical Element-to-Phase matrix owned by an active branch plan."""

    failures: list[str] = []
    branch = markdown_field_value(live_text, "Branch") or ""
    matrix_declared = markdown_field_value(
        live_text,
        "Element-to-Phase Proof Matrix",
    )
    normalized_relative = relative.replace("\\", "/")
    is_branch_plan = normalized_relative.endswith("/branch_plan.md")
    if not is_branch_plan:
        if matrix_declared:
            failures.append(
                "Element-to-Phase Ownership: the active matrix is declared outside "
                f"the branch-plan owner: {relative}"
            )
        return failures
    if branch != FAM003_OPTION_G_BRANCH and not matrix_declared:
        return failures
    expected_owner = "C:\\Nexus Governance State\\" + normalized_relative.replace("/", "\\")
    section = _element_to_phase_section(live_text)
    if not section:
        failures.append(
            "Element-to-Phase Ownership: the active branch plan does not physically "
            "contain the canonical Element-to-Phase Proof Matrix above the historical boundary"
        )
        return failures

    marker_expectations = (
        ("Matrix Status", {"required", "present", "accepted"}),
        ("USER Review Status", {"pending", "accepted", "revised", "waived", "needs user decision"}),
        ("Open Element Questions", {"none", "queued", "blocking", "deferred with waiver"}),
    )
    for marker, allowed in marker_expectations:
        value = markdown_field_value(section, marker)
        if not value or value.casefold() not in allowed:
            failures.append(
                f"Element-to-Phase Schema: {marker} is missing or invalid; found "
                f"{value or 'MISSING'!r}"
            )

    for marker in ("Element Coverage Owner", "Element Validation Ledger Owner"):
        value = markdown_field_value(section, marker)
        if _normalized_windows_value(value) != _normalized_windows_value(expected_owner):
            failures.append(
                f"Element-to-Phase Ownership: {marker} must name the physical active "
                f"branch plan {expected_owner!r}; found {value or 'MISSING'!r}"
            )

    table_lines = [line for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        failures.append("Element-to-Phase Schema: the canonical matrix table is missing")
        return failures
    header = tuple(_markdown_table_cells(table_lines[0]))
    if header != ELEMENT_TO_PHASE_HEADER:
        failures.append(
            "Element-to-Phase Schema: canonical table header must match the exact "
            f"11-column schema; found {header!r}"
        )
    separator = _markdown_table_cells(table_lines[1])
    if len(separator) != len(ELEMENT_TO_PHASE_HEADER) or any(
        not re.fullmatch(r":?-{3,}:?", cell) for cell in separator
    ):
        failures.append(
            "Element-to-Phase Schema: table separator does not match the exact 11-column schema"
        )

    rows: list[list[str]] = []
    for line in table_lines[2:]:
        cells = _markdown_table_cells(line)
        if cells:
            rows.append(cells)
    expected_ids = (
        FAM003_OPTION_G_ELEMENT_IDS if branch == FAM003_OPTION_G_BRANCH else ()
    )
    row_ids = [row[0] for row in rows if row]
    if expected_ids and tuple(row_ids) != expected_ids:
        failures.append(
            "Element-to-Phase Coverage: FAM-003 Option G must contain exactly "
            f"{len(expected_ids)} ordered unique rows {expected_ids!r}; found {tuple(row_ids)!r}"
        )
    elif len(row_ids) != len(set(item.casefold() for item in row_ids)):
        failures.append("Element-to-Phase Coverage: duplicate Element IDs are forbidden")

    for index, row in enumerate(rows, start=1):
        row_id = row[0] if row else f"row-{index}"
        if len(row) != len(ELEMENT_TO_PHASE_HEADER):
            failures.append(
                f"Element-to-Phase Schema: {row_id} has {len(row)} columns; "
                f"expected {len(ELEMENT_TO_PHASE_HEADER)}"
            )
            continue
        if any(not cell.strip() for cell in row):
            failures.append(
                f"Element-to-Phase Proof Path: {row_id} contains an empty required cell"
            )
        if row[2] not in ELEMENT_TO_PHASE_CLASSIFICATIONS:
            failures.append(
                f"Element-to-Phase Schema: {row_id} uses invalid Element Classification "
                f"{row[2]!r}"
            )
        if row[2] in {"Planned", "Created", "Touched", "Affected"}:
            for column in range(3, 8):
                if not row[column].strip():
                    failures.append(
                        f"Element-to-Phase Proof Path: {row_id} omits "
                        f"{ELEMENT_TO_PHASE_HEADER[column]}"
                    )
    return failures


def _validate_active_branch_plan_ufd(relative: str, live_text: str) -> list[str]:
    """Prove that a declared active UFD owner physically owns its atomic rows."""

    failures: list[str] = []
    required = (markdown_field_value(live_text, "USER Feedback Disposition Required") or "").casefold()
    if "yes" not in required:
        return failures

    branch = markdown_field_value(live_text, "Branch") or ""
    normalized_relative = relative.replace("\\", "/")
    if not normalized_relative.endswith("/branch_plan.md"):
        failures.append(
            "Canonical UFD Ownership: USER Feedback Disposition Required is active "
            f"outside the canonical branch-plan target: {relative}"
        )
        return failures

    expected_owner = "C:\\Nexus Governance State\\" + normalized_relative.replace("/", "\\")
    owner = markdown_field_value(live_text, "UFD Ledger Owner")
    if _normalized_windows_value(owner) != _normalized_windows_value(expected_owner):
        failures.append(
            "Canonical UFD Ownership: UFD Ledger Owner does not match the physical "
            f"active branch plan: expected {expected_owner!r}, found {owner or 'MISSING'!r}"
        )

    physical_location = markdown_field_value(live_text, "UFD Physical Detail Location")
    if _normalized_windows_value(physical_location) != _normalized_windows_value(expected_owner):
        failures.append(
            "Canonical UFD Ownership: UFD Physical Detail Location must identify "
            f"the active branch plan itself: expected {expected_owner!r}, "
            f"found {physical_location or 'MISSING'!r}"
        )
    if markdown_field_value(live_text, "UFD Detail Record"):
        failures.append(
            "Canonical UFD Ownership: UFD Detail Record must not redirect full-detail "
            "authority away from the declared active branch-plan owner"
        )
    current_owner_class = markdown_field_value(live_text, "UFD Current Owner Class")
    if (current_owner_class or "").casefold() != "branch plan":
        failures.append(
            "Canonical UFD Ownership: UFD Current Owner Class must be Branch Plan "
            f"while the active external branch plan owns the ledger; found "
            f"{current_owner_class or 'MISSING'!r}"
        )
    current_owner_file = markdown_field_value(
        live_text,
        "UFD Current Canonical Owner File",
    )
    if _normalized_windows_value(current_owner_file) != _normalized_windows_value(
        expected_owner
    ):
        failures.append(
            "Canonical UFD Ownership: UFD Current Canonical Owner File must match "
            f"the active external branch plan: expected {expected_owner!r}, found "
            f"{current_owner_file or 'MISSING'!r}"
        )
    future_fold_down_target = markdown_field_value(
        live_text,
        "UFD Future Fold-Down Target",
    )
    if (
        branch == FAM003_OPTION_G_BRANCH
        and future_fold_down_target != FAM003_OPTION_G_UFD_FOLD_DOWN_TARGET
    ):
        failures.append(
            "Canonical UFD Ownership: UFD Future Fold-Down Target must identify "
            "the FAM-003 repo branch record compact receipt while fold-down is "
            f"pending; found {future_fold_down_target or 'MISSING'!r}"
        )
    if _normalized_windows_value(future_fold_down_target) == _normalized_windows_value(
        expected_owner
    ):
        failures.append(
            "Canonical UFD Ownership: current canonical ownership and future "
            "fold-down ownership must remain distinct"
        )

    item_matches = list(
        re.finditer(
            r"(?ms)^### UFD Item:\s*(UFD-[^\n]+)\n"
            r"(.*?)(?=^### UFD Item:|^## |\Z)",
            live_text,
        )
    )
    declared_count_text = markdown_field_value(live_text, "UFD Item Count")
    declared_count_match = re.search(r"\d+", declared_count_text or "")
    if not declared_count_match:
        failures.append("Canonical UFD Ownership: UFD Item Count is missing or non-numeric")
        declared_count = -1
    else:
        declared_count = int(declared_count_match.group(0))
    if declared_count != len(item_matches):
        failures.append(
            "Canonical UFD Ownership: declared UFD Item Count does not match physical "
            f"atomic rows: declared {declared_count}, found {len(item_matches)}"
        )
    if branch == FAM003_OPTION_G_BRANCH and len(item_matches) != FAM003_OPTION_G_UFD_COUNT:
        failures.append(
            "Canonical UFD Ownership: FAM-003 Option G requires exactly "
            f"{FAM003_OPTION_G_UFD_COUNT} physical atomic rows; found {len(item_matches)}"
        )

    open_items = 0
    blocking_items = 0
    seen_ids: set[str] = set()
    required_markers = (
        FAM003_OPTION_G_UFD_ITEM_MARKERS
        if branch == FAM003_OPTION_G_BRANCH
        else FAM003_OPTION_G_UFD_ITEM_MARKERS[:12]
    )
    for item_match in item_matches:
        item_id = item_match.group(1).strip()
        item_text = item_match.group(2)
        normalized_id = item_id.casefold()
        if normalized_id in seen_ids:
            failures.append(f"Canonical UFD Ownership: duplicate atomic row {item_id}")
        seen_ids.add(normalized_id)
        for marker in required_markers:
            if marker not in item_text:
                failures.append(
                    f"Canonical UFD Ownership: {item_id} is missing required field {marker}"
                )
        feedback_id = markdown_field_value(item_text, "Feedback ID") or ""
        if feedback_id.casefold() != normalized_id:
            failures.append(
                f"Canonical UFD Ownership: {item_id} Feedback ID does not match its heading"
            )
        owner_class = markdown_field_value(item_text, "Owner Class")
        if (owner_class or "").casefold() != "branch plan":
            failures.append(
                f"Canonical UFD Ownership: {item_id} Owner Class must be Branch Plan "
                "while fold-down is pending"
            )
        canonical_owner = markdown_field_value(item_text, "Canonical Owner File")
        if _normalized_windows_value(canonical_owner) != _normalized_windows_value(
            expected_owner
        ):
            failures.append(
                f"Canonical UFD Ownership: {item_id} Canonical Owner File must match "
                "the physical active branch-plan owner"
            )
        fold_down_target = markdown_field_value(item_text, "Fold-Down Target")
        if (
            branch == FAM003_OPTION_G_BRANCH
            and fold_down_target != FAM003_OPTION_G_UFD_FOLD_DOWN_TARGET
        ):
            failures.append(
                f"Canonical UFD Ownership: {item_id} Fold-Down Target must identify "
                "the future compact branch-record receipt"
            )
        if _normalized_windows_value(canonical_owner) == _normalized_windows_value(
            fold_down_target
        ):
            failures.append(
                f"Canonical UFD Ownership: {item_id} conflates current canonical "
                "ownership with its future fold-down target"
            )
        if UFD_CONTEXT_RELATIVE_LOCATION_RE.search(item_text):
            failures.append(
                f"Canonical UFD Ownership: {item_id} contains context-relative "
                "location wording that changes meaning across supporting copies"
            )
        remaining_decision = (
            markdown_field_value(item_text, "Remaining USER Decision") or ""
        ).strip()
        if branch == FAM003_OPTION_G_BRANCH and "bp3 acceptance" in remaining_decision.casefold():
            failures.append(
                f"Canonical UFD Vocabulary: {item_id} uses BP3 acceptance where "
                "the actionable BP3 state is USER Approved; use 'BP3 approval only'"
            )
        status = (markdown_field_value(item_text, "Status") or "").casefold()
        if any(term in status for term in ("open", "queued", "blocking", "deferred")):
            open_items += 1
        if "blocking" in status:
            blocking_items += 1

    for marker, actual in (
        ("Open UFD Count", open_items),
        ("Blocking UFD Count", blocking_items),
    ):
        value = markdown_field_value(live_text, marker)
        match = re.search(r"\d+", value or "")
        declared = int(match.group(0)) if match else -1
        if declared != actual:
            failures.append(
                f"Canonical UFD Ownership: {marker} {declared} does not match "
                f"physical atomic-row state {actual}"
            )

    return failures


def _validate_active_branch_plan_vision(relative: str, live_text: str) -> list[str]:
    """Validate the current FAM-003 Branch Vision snapshot in its active owner."""

    failures: list[str] = []
    branch = markdown_field_value(live_text, "Branch") or ""
    if branch != FAM003_OPTION_G_BRANCH:
        return failures
    if not relative.replace("\\", "/").endswith("/branch_plan.md"):
        return failures
    if FAM003_OPTION_G_VISION_HEADING not in live_text:
        return [
            "Branch Vision Contract Snapshot: required active snapshot is absent "
            "from the live FAM-003 branch plan above the historical boundary"
        ]
    section = live_text.split(FAM003_OPTION_G_VISION_HEADING, 1)[1]
    section = section.split("\n## ", 1)[0]
    for marker in FAM003_OPTION_G_VISION_MARKERS:
        value = markdown_field_value(section, marker.rstrip(":"))
        if marker not in section or not value:
            failures.append(
                f"Branch Vision Contract Snapshot: active snapshot is missing a "
                f"nonblank {marker} value"
            )
    required = (markdown_field_value(section, "Vision Contract Required") or "").casefold()
    status = (markdown_field_value(section, "Branch Vision Snapshot Status") or "").casefold()
    questions = (markdown_field_value(section, "Open Vision Questions") or "").casefold()
    user_green = (markdown_field_value(section, "USER Vision Green") or "").casefold()
    if "yes" not in required:
        failures.append("Branch Vision Contract Snapshot: FAM-003 runtime branch must say required Yes")
    if "accepted" not in status:
        failures.append("Branch Vision Contract Snapshot: accepted BP1 carrydown must use Accepted status")
    if questions not in {"none", "none; no blocking vision questions"}:
        failures.append("Branch Vision Contract Snapshot: Open Vision Questions must be None")
    if user_green not in {"yes", "green", "accepted"}:
        failures.append("Branch Vision Contract Snapshot: USER Vision Green must be Yes")
    implementation_scope = (
        markdown_field_value(section, "Implementation Scope") or ""
    ).casefold()
    seam_map = (markdown_field_value(section, "Seam Map") or "").casefold()
    if (
        "accepted bp1" not in implementation_scope
        or "accepted bp2" not in implementation_scope
        or "workstream implementation" in implementation_scope
    ):
        failures.append(
            "Branch Vision Contract Snapshot: implementation scope exceeds accepted BP1/BP2 carrydown"
        )
    if not all(
        marker.casefold() in seam_map
        for marker in ("F3-OPTG-D01", "OPTG-WS01", "OPTG-WS07", "OPTG-ALLOW-08")
    ):
        failures.append(
            "Branch Vision Contract Snapshot: seam map disagrees with the accepted Option G BP3 plan"
        )
    expected_owners = {
        "Project Vision Owner": "Docs/nexus_vision.md",
        "FAM-003 Family Vision Owner": (
            "Docs/family_visions/FAM-003_interaction_and_actions.md"
        ),
        "F3-FF01 Owner": "Docs/family_feature_visions/F3-FF01.md",
        "Accepted BP1 Owner": "bp1_branch_vision_revision_20260715.md",
        "Accepted BP2 Owner": "decision2_option_g_bp2_gate_repair_20260724.md",
        "Accepted BP2 Acceptance Receipt": (
            "decision2_option_g_bp2_acceptance_20260724.md"
        ),
    }
    for field, expected in expected_owners.items():
        if markdown_field_value(section, field) != expected:
            failures.append(
                f"Branch Vision Contract Snapshot: {field} must identify {expected}"
            )
    for field in (
        "Project Vision SHA256",
        "FAM-003 Family Vision SHA256",
        "F3-FF01 SHA256",
        "Accepted BP1 SHA256",
        "Accepted BP2 SHA256",
        "Accepted BP2 Acceptance Receipt SHA256",
    ):
        if not re.fullmatch(
            r"[0-9A-Fa-f]{64}", markdown_field_value(section, field) or ""
        ):
            failures.append(
                f"Branch Vision Contract Snapshot: {field} must be a full SHA256"
            )
    return failures


def _markdown_field_values(text: str, fields: tuple[str, ...]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in fields:
        pattern = re.compile(
            rf"^\s*(?:-\s*)?{re.escape(field)}:\s*(.*?)\s*$",
            re.MULTILINE,
        )
        for match in pattern.finditer(text):
            value = match.group(1).strip()
            if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
                value = value[1:-1].strip()
            if value:
                values.append((field, value))
    return values


def _field_alias_failures(
    relative: str,
    text: str,
    fields: tuple[str, ...],
) -> list[str]:
    values = _markdown_field_values(text, fields)
    if len(values) <= 1:
        return []
    rendered = ", ".join(f"{field}={value!r}" for field, value in values)
    return [
        f"Target Currentness: duplicate or conflicting live identity fields for {relative}: {rendered}"
    ]


def _has_reparse_point(path: Path) -> bool:
    try:
        if os.path.islink(path):
            return True
        metadata = os.stat(path, follow_symlinks=False)
        attributes = getattr(metadata, "st_file_attributes", 0)
        return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    except OSError:
        return False


def _resolve_target_path(root: Path, raw_target: str) -> tuple[str | None, Path | None, list[str]]:
    failures: list[str] = []
    if not isinstance(raw_target, str) or not raw_target.strip():
        return None, None, ["Target Currentness Contract: target path is missing"]
    raw = raw_target.strip()
    windows = PureWindowsPath(raw)
    if Path(raw).is_absolute() or windows.is_absolute() or windows.drive or windows.root:
        failures.append(f"Target Path Security: absolute/off-root target is forbidden: {raw_target}")
        return None, None, failures
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    if (
        not parts
        or any(part in {"", "..", "."} for part in parts)
        or "/" in raw and "\\" in raw
        or normalized.endswith("/")
        or any(":" in part for part in parts)
    ):
        failures.append(f"Target Path Security: traversal or alias segments are forbidden: {raw_target}")
        return None, None, failures
    relative = "/".join(parts)
    root_resolved = root.resolve(strict=False)
    candidate = (root / Path(*parts)).resolve(strict=False)
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        failures.append(f"Target Path Security: resolved target escapes external root: {raw_target}")
        return None, None, failures
    cursor = root_resolved
    for part in parts:
        cursor = cursor / part
        if cursor.exists() and _has_reparse_point(cursor):
            failures.append(f"Target Path Security: reparse/symlink escape is forbidden: {relative}")
            return relative, None, failures
    if not candidate.is_file():
        failures.append(f"Target Currentness: selected target is missing or not a file: {relative}")
        return relative, None, failures
    return relative, candidate, failures


def validate_target_currentness(
    root: Path,
    targets: list[str],
    *,
    expected_branch: str | None,
    expected_source_head: str | None,
    expected_origin_main: str | None,
    expected_worktree_path: str | None,
    expected_worktree_slot: str | None,
    expected_target_sha256: str | None,
    expected_schema: str = DEFAULT_SCHEMA_VERSION,
) -> list[str]:
    """Validate exactly one selected live external record without claiming root-wide freshness."""

    failures = validate_canonical_root(root)
    root = resolve_path(root)
    if not root.is_dir():
        failures.append(f"External State Missing: target-scoped validation root is absent: {root}")
        return failures
    if len(targets) != 1:
        failures.append(
            "Target Currentness Contract: exactly one explicit target is required; "
            f"received {len(targets)} (duplicate/ambiguous target selection is rejected)"
        )
        return failures
    required_expectations = {
        "expected branch": expected_branch,
        "expected source HEAD": expected_source_head,
        "expected origin/main": expected_origin_main,
        "expected worktree path": expected_worktree_path,
        "expected worktree slot": expected_worktree_slot,
        "expected target SHA256": expected_target_sha256,
    }
    missing = [name for name, value in required_expectations.items() if not value]
    if missing:
        failures.append(
            "Target Currentness Contract: fail closed; missing explicit expectations: "
            + ", ".join(missing)
        )
        return failures
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_target_sha256 or ""):
        failures.append("Target Currentness Contract: expected target SHA256 must be 64 hexadecimal characters")
        return failures

    relative, target_path, path_failures = _resolve_target_path(root, targets[0])
    failures.extend(path_failures)
    if target_path is None or relative is None:
        return failures

    try:
        before_hash = sha256_file(target_path)
        target_bytes = target_path.read_bytes()
        target_bytes_hash = hashlib.sha256(target_bytes).hexdigest()
        text = target_bytes.decode("utf-8")
        after_hash = sha256_file(target_path)
    except (OSError, UnicodeDecodeError) as exc:
        failures.append(f"Target Currentness: selected target is malformed or unreadable: {relative}: {exc}")
        return failures

    if before_hash != after_hash or target_bytes_hash != before_hash or target_bytes_hash != after_hash:
        failures.append(f"Target Currentness: selected target changed during validation (TOCTOU): {relative}")
    if before_hash.casefold() != (expected_target_sha256 or "").casefold():
        failures.append(
            f"Target Currentness: target hash precondition failed for {relative}: "
            f"expected {expected_target_sha256}, found {before_hash}"
        )
    if failures:
        return failures

    live_text = _live_header_text(text)
    failures.extend(_field_alias_failures(relative, live_text, ("Branch", "Current Branch")))
    failures.extend(_field_alias_failures(relative, live_text, ("Source Repo HEAD", "Current HEAD")))
    failures.extend(_field_alias_failures(relative, live_text, ("Origin/Main", "Source origin/main")))
    failures.extend(_field_alias_failures(relative, live_text, ("Worktree Path",)))
    failures.extend(_field_alias_failures(relative, live_text, ("Slot ID",)))
    if failures:
        return failures

    schema = markdown_field_value(live_text, "External State Schema")
    if schema != expected_schema:
        failures.append(
            f"External State Schema Conflict: {relative}: expected {expected_schema}, found {schema or 'MISSING'}"
        )
    record_class = _normalized_windows_value(markdown_field_value(live_text, "Record Class")).replace("\\", " ")
    if record_class in TARGET_HISTORICAL_RECORD_CLASSES or "historical receipt" in record_class:
        failures.append(f"Target Currentness: historical receipt cannot be selected as live state: {relative}")
    elif record_class not in TARGET_LIVE_RECORD_CLASSES:
        failures.append(
            f"Target Currentness: unsupported or missing live Record Class in {relative}: "
            f"{record_class or 'MISSING'}"
        )

    actual_branch = _first_markdown_field(live_text, ("Branch", "Current Branch"))
    actual_head = _first_markdown_field(live_text, ("Source Repo HEAD", "Current HEAD"))
    actual_origin = _first_markdown_field(live_text, ("Origin/Main", "Source origin/main"))
    actual_worktree = markdown_field_value(live_text, "Worktree Path")
    actual_slot = markdown_field_value(live_text, "Slot ID")
    for label, actual, expected, normalizer in (
        ("Branch", actual_branch, expected_branch, lambda value: (value or "").strip()),
        ("Source Repo HEAD", actual_head, expected_source_head, lambda value: (value or "").strip().casefold()),
        ("Origin/Main", actual_origin, expected_origin_main, lambda value: (value or "").strip().casefold()),
        ("Worktree Path", actual_worktree, expected_worktree_path, _normalized_windows_value),
        ("Slot ID", actual_slot, expected_worktree_slot, lambda value: (value or "").strip().casefold()),
    ):
        if not actual:
            failures.append(f"Target Currentness: {relative} is missing required field {label}")
        elif normalizer(actual) != normalizer(expected):
            failures.append(
                f"Target Currentness: {relative} {label} mismatch: expected {expected!r}, found {actual!r}"
            )

    if markdown_field_value(live_text, "Record Role") is None:
        failures.append(f"Target Currentness: {relative} is missing Record Role classification")
    if markdown_field_value(live_text, "Historical Receipt Boundary") is None:
        failures.append(f"Target Currentness: {relative} is missing Historical Receipt Boundary")
    failures.extend(_validate_active_branch_plan_vision(relative, live_text))
    failures.extend(_validate_active_branch_plan_ufd(relative, live_text))
    failures.extend(_validate_active_branch_plan_element_matrix(relative, live_text))
    return failures


PROJECTION_SET_FIELDS = (
    "State Version",
    "Last Updated",
    "Last Updated By",
    "Worktree",
    "Worktree Path",
    "Branch",
    "Source Repo HEAD",
    "Origin/Main",
    "Slot ID",
    "Current Gate",
    "Workstream Result",
    "H1 / LV / UTS",
    "Next Legal Phase",
    "Transition Status",
)


def _parse_target_hash_pairs(values: list[str]) -> tuple[dict[str, str], list[str]]:
    pairs: dict[str, str] = {}
    failures: list[str] = []
    for value in values:
        if "=" not in value:
            failures.append(f"Projection Set Contract: expected TARGET=SHA256, found {value!r}")
            continue
        target, digest = (item.strip() for item in value.split("=", 1))
        normalized = target.replace("\\", "/")
        if normalized in pairs:
            failures.append(f"Projection Set Contract: duplicate target hash supplied: {normalized}")
        elif not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            failures.append(f"Projection Set Contract: invalid SHA256 for {normalized}: {digest!r}")
        else:
            pairs[normalized] = digest
    return pairs, failures


def _parse_timestamp(value: str, label: str, failures: list[str]) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        failures.append(f"Projection Set Semantics: malformed timestamp for {label}: {value!r}")
        return None
    if parsed.tzinfo is None:
        failures.append(f"Projection Set Semantics: timestamp is not timezone-aware for {label}: {value!r}")
        return None
    return parsed


def _historical_receipt_bytes(data: bytes, label: str, failures: list[str]) -> bytes | None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        failures.append(f"Projection Set Semantics: malformed UTF-8 in {label}: {exc}")
        return None
    match = re.search(
        r"^\s*(?:-\s*)?Historical Receipt Boundary:\s*.*?(?:\r\n|\n|\r|$)",
        text,
        re.MULTILINE,
    )
    if not match:
        failures.append(f"Projection Set Semantics: Historical Receipt Boundary is missing in {label}")
        return None
    return text[match.end() :].encode("utf-8")


def _load_semantic_json(path: Path, label: str, failures: list[str]) -> dict[str, object] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        failures.append(f"Projection Set Semantics: {label} is missing or unreadable: {path}: {exc}")
        return None
    if not isinstance(payload, dict):
        failures.append(f"Projection Set Semantics: {label} must be a JSON object: {path}")
        return None
    return payload


def validate_projection_set_semantic_coherence(
    root: Path,
    targets: list[str],
    *,
    expected_target_hashes: dict[str, str],
    expected_branch: str | None,
    expected_source_head: str | None,
    expected_origin_main: str | None,
    expected_worktree_path: str | None,
    expected_worktree_slot: str | None,
    expected_current_gate: str | None,
    expected_workstream_result: str | None,
    expected_stage_states: str | None,
    expected_next_legal_phase: str | None,
    expected_transition_status: str | None,
    expected_state_version: int | None,
    expected_last_updated_by: str | None,
    previous_snapshot: str | None,
    completion_audit: str | None,
    primary_review: str | None,
    expected_decision_1: str | None,
    expected_decision_2: str | None,
    expected_decision_3: str | None,
    expected_completion_transition_status: str = "MIGRATION_COMPLETE",
    expected_schema: str = DEFAULT_SCHEMA_VERSION,
) -> list[str]:
    """Validate cross-projection phase semantics without treating historical receipts as live state."""

    failures = validate_canonical_root(root)
    root = resolve_path(root)
    required = {
        "expected branch": expected_branch,
        "expected source HEAD": expected_source_head,
        "expected origin/main": expected_origin_main,
        "expected worktree path": expected_worktree_path,
        "expected worktree slot": expected_worktree_slot,
        "expected current gate": expected_current_gate,
        "expected workstream result": expected_workstream_result,
        "expected H1 / LV / UTS": expected_stage_states,
        "expected next legal phase": expected_next_legal_phase,
        "expected transition status": expected_transition_status,
        "expected state version": expected_state_version,
        "expected last updated by": expected_last_updated_by,
        "previous snapshot": previous_snapshot,
        "completion audit": completion_audit,
        "primary review": primary_review,
        "expected Decision 1": expected_decision_1,
        "expected Decision 2": expected_decision_2,
        "expected Decision 3": expected_decision_3,
        "expected completion audit transition status": expected_completion_transition_status,
    }
    missing = [name for name, value in required.items() if value is None or value == ""]
    if missing:
        failures.append(
            "Projection Set Contract: fail closed; missing explicit expectations: " + ", ".join(missing)
        )
    normalized_targets = [target.replace("\\", "/") for target in targets]
    if len(normalized_targets) < 2 or len(set(normalized_targets)) != len(normalized_targets):
        failures.append(
            "Projection Set Contract: at least two distinct explicit targets are required; "
            f"received {len(targets)}"
        )
    if set(normalized_targets) != set(expected_target_hashes):
        failures.append(
            "Projection Set Contract: target/hash selection mismatch; targets="
            + repr(sorted(normalized_targets))
            + ", hashes="
            + repr(sorted(expected_target_hashes))
        )
    if failures:
        return failures

    records: dict[str, tuple[Path, bytes, str, dict[str, str | None]]] = {}
    for target in normalized_targets:
        target_failures = validate_target_currentness(
            root,
            [target],
            expected_branch=expected_branch,
            expected_source_head=expected_source_head,
            expected_origin_main=expected_origin_main,
            expected_worktree_path=expected_worktree_path,
            expected_worktree_slot=expected_worktree_slot,
            expected_target_sha256=expected_target_hashes[target],
            expected_schema=expected_schema,
        )
        failures.extend(target_failures)
        relative, path, path_failures = _resolve_target_path(root, target)
        failures.extend(path_failures)
        if target_failures or path is None or relative is None:
            continue
        data = path.read_bytes()
        text = data.decode("utf-8")
        live_text = _live_header_text(text)
        fields = {field: markdown_field_value(live_text, field) for field in PROJECTION_SET_FIELDS}
        records[relative] = (path, data, live_text, fields)
    if failures:
        return failures

    reference_target = normalized_targets[0]
    reference_fields = records[reference_target][3]
    for field in PROJECTION_SET_FIELDS:
        reference = reference_fields[field]
        if reference is None:
            failures.append(f"Projection Set Semantics: {reference_target} is missing live field {field}")
            continue
        for target in normalized_targets[1:]:
            actual = records[target][3][field]
            if actual != reference:
                failures.append(
                    f"Projection Set Semantics: cross-target {field} mismatch: "
                    f"{reference_target}={reference!r}; {target}={actual!r}"
                )

    expected_fields: dict[str, object] = {
        "State Version": expected_state_version,
        "Last Updated By": expected_last_updated_by,
        "Current Gate": expected_current_gate,
        "Workstream Result": expected_workstream_result,
        "H1 / LV / UTS": expected_stage_states,
        "Next Legal Phase": expected_next_legal_phase,
        "Transition Status": expected_transition_status,
    }
    for field, expected in expected_fields.items():
        actual = reference_fields[field]
        if field == "State Version":
            try:
                actual_value: object = int(actual or "")
            except ValueError:
                actual_value = actual
        else:
            actual_value = actual
        if actual_value != expected:
            failures.append(
                f"Projection Set Semantics: live {field} mismatch: expected {expected!r}, found {actual!r}"
            )

    snapshot_path = (root / Path(*(previous_snapshot or "").replace("\\", "/").split("/"))).resolve()
    try:
        snapshot_path.relative_to(root.resolve())
    except ValueError:
        failures.append(f"Projection Set Contract: previous snapshot escapes external root: {previous_snapshot}")
        snapshot_path = root / "__invalid_snapshot__"
    if not snapshot_path.is_dir():
        failures.append(f"Projection Set Semantics: previous snapshot is missing: {snapshot_path}")
    else:
        for target in normalized_targets:
            snapshot_target = snapshot_path.joinpath(*target.split("/"))
            if not snapshot_target.is_file():
                failures.append(f"Projection Set Semantics: snapshot target is missing: {snapshot_target}")
                continue
            current_data = records[target][1]
            snapshot_data = snapshot_target.read_bytes()
            current_tail = _historical_receipt_bytes(current_data, target, failures)
            snapshot_tail = _historical_receipt_bytes(snapshot_data, f"snapshot/{target}", failures)
            if current_tail is not None and snapshot_tail is not None and current_tail != snapshot_tail:
                failures.append(f"Projection Set Semantics: historical receipt bytes changed for {target}")
            snapshot_live = _live_header_text(snapshot_data.decode("utf-8"))
            previous_version = markdown_field_value(snapshot_live, "State Version")
            current_version = records[target][3]["State Version"]
            try:
                if int(current_version or "") != int(previous_version or "") + 1:
                    failures.append(
                        f"Projection Set Semantics: State Version did not advance by one for {target}: "
                        f"previous={previous_version!r}, current={current_version!r}"
                    )
            except ValueError:
                failures.append(
                    f"Projection Set Semantics: non-integer State Version for {target}: "
                    f"previous={previous_version!r}, current={current_version!r}"
                )
            previous_updated = markdown_field_value(snapshot_live, "Last Updated")
            current_updated = records[target][3]["Last Updated"]
            previous_time = _parse_timestamp(previous_updated or "", f"snapshot/{target}", failures)
            current_time = _parse_timestamp(current_updated or "", target, failures)
            if previous_time is not None and current_time is not None and current_time <= previous_time:
                failures.append(
                    f"Projection Set Semantics: Last Updated did not advance for {target}: "
                    f"previous={previous_updated!r}, current={current_updated!r}"
                )

    audit_path = Path(completion_audit or "")
    if not audit_path.is_absolute():
        audit_path = root / audit_path
    audit = _load_semantic_json(audit_path, "completion audit", failures)
    if audit is not None:
        audit_expectations = {
            "Transition Status": expected_completion_transition_status,
            "Decision 1": expected_decision_1,
            "Decision 2": expected_decision_2,
            "Decision 3": expected_decision_3,
            "Workstream": expected_workstream_result,
            "H1 / LV / UTS": expected_stage_states,
            "Next Legal Phase": expected_next_legal_phase,
        }
        for field, expected in audit_expectations.items():
            if audit.get(field) != expected:
                failures.append(
                    f"Projection Set Semantics: completion audit {field} mismatch: "
                    f"expected {expected!r}, found {audit.get(field)!r}"
                )

    review_path = Path(primary_review or "")
    if not review_path.is_absolute():
        review_path = root / review_path
    try:
        review_text = review_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        failures.append(f"Projection Set Semantics: primary review is missing or unreadable: {review_path}: {exc}")
        review_text = ""
    review_folded = review_text.casefold()
    for label, needles in (
        ("Decision 1 completion", ("decision 1", "complete")),
        ("Decision 2 separate approval", ("decision 2", "separate", "approval")),
        ("Decision 3 future gate", ("decision 3", "future")),
    ):
        if not all(needle in review_folded for needle in needles):
            failures.append(f"Projection Set Semantics: primary review lacks {label} semantics")

    next_phase = (reference_fields["Next Legal Phase"] or "").casefold()
    if expected_decision_1 == "COMPLETE" and "decision 1" in next_phase:
        failures.append("Projection Set Semantics: Decision 1 is complete but live Next Legal Phase asks for Decision 1")
    if expected_decision_2 == "ELIGIBLE_FOR_SEPARATE_USER_APPROVAL_ONLY":
        if "decision 2" not in next_phase or not any(
            marker in next_phase for marker in ("user decision", "user approval")
        ):
            failures.append(
                "Projection Set Semantics: Decision 2 is eligible for separate USER approval but live Next Legal Phase does not route a USER decision"
            )
        if re.search(r"\b(?:approved|started|in progress|underway)\b", next_phase):
            failures.append(
                "Projection Set Semantics: Decision 2 is only eligible but live Next Legal Phase claims it is approved or started"
            )
    if expected_decision_3 == "SEPARATE_FUTURE_GATE" and "decision 3" in next_phase:
        failures.append("Projection Set Semantics: Decision 3 was merged into the active Decision 2 route")
    if "decision 1" in next_phase and "decision 1" not in review_folded:
        failures.append("Projection Set Semantics: packet/live route disagreement about Decision 1")
    if "decision 1" in next_phase and "decision 1 is complete" in review_folded:
        failures.append("Projection Set Semantics: packet says Decision 1 is complete while live state routes Decision 1")
    return failures


def markdown_field_value_with_continuation(text: str, field: str) -> str | None:
    marker_pattern = re.compile(
        rf"^\s*(?:-\s*)?{re.escape(field)}:\s*(.*?)\s*$",
        re.IGNORECASE,
    )
    any_field_pattern = re.compile(r"^\s*(?:-\s*)?[A-Za-z][A-Za-z0-9 /_-]*:\s*")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = marker_pattern.match(line)
        if not match:
            continue
        values: list[str] = []
        first_value = match.group(1).strip()
        if first_value:
            values.append(first_value)
        for next_line in lines[index + 1 :]:
            stripped = next_line.strip()
            if not stripped:
                break
            if re.match(
                r"^(?:[-*]|\d+\.)?\s*(?:slice\s+\d+|slc-\d+)\b",
                stripped,
                re.IGNORECASE,
            ):
                values.append(stripped)
                continue
            if any_field_pattern.match(next_line):
                break
            if next_line[:1].isspace() and values:
                values.append(stripped)
                continue
            if values:
                values.append(stripped)
                continue
            break
        return " ".join(values).strip()
    return None


def resolve_markdown_path(value: str | None, root: Path) -> Path | None:
    if not value:
        return None
    cleaned = value.strip().strip("`").strip()
    if not cleaned:
        return None
    path = Path(cleaned)
    return path if path.is_absolute() else root / cleaned


def active_branch_plan_path(active_text: str, root: Path) -> Path | None:
    path_value = markdown_field_value(active_text, "Branch Runtime Engineering Plan Path")
    plan_path = resolve_markdown_path(path_value, root)
    if plan_path:
        return plan_path
    return resolve_markdown_path(
        markdown_field_value(active_text, "Branch Runtime Engineering Plan"),
        root,
    )


def normalized_route_value(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def route_word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9_/-]*", value))


def slice_map_deliverable_count(value: str) -> int:
    entries = re.split(r"(?:\.\s+|;\s+|\n+)", value)
    identifiers: set[str] = set()
    pair_pattern = re.compile(
        r"\b(?:slice\s+(\d+)\s*/\s*slc-(\d+)|slc-(\d+)\s*/\s*slice\s+(\d+))\b",
        flags=re.IGNORECASE,
    )
    identifier_pattern = re.compile(
        r"\b(?:slc-(\d+)|slice\s+(\d+))\b",
        flags=re.IGNORECASE,
    )
    for entry_index, entry in enumerate(entries):
        protected_spans: list[tuple[int, int]] = []
        for pair_index, pair in enumerate(pair_pattern.finditer(entry)):
            left = pair.group(1) or pair.group(3)
            right = pair.group(2) or pair.group(4)
            left_id = int(left)
            right_id = int(right)
            if left_id == right_id:
                identifiers.add(str(left_id))
            else:
                identifiers.add(f"entry-{entry_index}-pair-{pair_index}")
            protected_spans.append(pair.span())

        for match in identifier_pattern.finditer(entry):
            if any(start <= match.start() < end for start, end in protected_spans):
                continue
            identifiers.add(str(int(match.group(1) or match.group(2))))
    return len(identifiers)


def slice_map_mismatched_alias_pairs(value: str) -> list[str]:
    pair_pattern = re.compile(
        r"\b(?:slice\s+(\d+)\s*/\s*slc-(\d+)|slc-(\d+)\s*/\s*slice\s+(\d+))\b",
        flags=re.IGNORECASE,
    )
    mismatches: list[str] = []
    for pair in pair_pattern.finditer(value):
        left = pair.group(1) or pair.group(3)
        right = pair.group(2) or pair.group(4)
        if int(left) != int(right):
            mismatches.append(pair.group(0))
    return mismatches


def value_declares_multi_slice(value: str) -> bool:
    normalized = normalized_route_value(value)
    positive_match = re.search(r"\bmulti[- ]slice\b|\bmultiple\s+slices\b", normalized)
    if not positive_match:
        return False

    negation_match = re.search(
        r"\b(?:no|not|without)\b[^.\n;:]{0,80}\b(?:multi[- ]slice|multiple\s+slices)\b"
        r"|\bnon[- ]multi[- ]slice\b",
        normalized,
    )
    if negation_match and negation_match.start() < positive_match.start():
        return False

    postfixed_negation_match = re.search(
        r"\b(?:multi[- ]slice|multiple\s+slices)\b\s+(?:(?:is|are)\s+)?(?:"
        r"not\s+(?:required|needed|applicable|in\s+scope|part\s+of\s+this\s+branch)"
        r"|out\s+of\s+scope|unneeded)",
        normalized,
    )
    if postfixed_negation_match and postfixed_negation_match.start() == positive_match.start():
        return False

    future_gate_match = re.search(
        r"\bfuture(?:[- ]gated)?\b[^.\n;:]{0,80}"
        r"\b(?:multi[- ]slice|multiple\s+slices)\b[^.\n;:]{0,100}"
        r"\b(?:user[- ]gated|future[- ]gated|deferred|later|out\s+of\s+scope|outside)\b",
        normalized,
    )
    if future_gate_match and future_gate_match.start() <= positive_match.start():
        return False

    future_scope_match = re.search(
        r"\bfuture(?:[- ]gated)?\b[^.\n;:]{0,80}"
        r"\b(?:multi[- ]slice|multiple\s+slices)\b[^.\n;:]{0,140}"
        r"\b(?:outside|out\s+of\s+scope|not\s+part\s+of|excluded\s+from|deferred\s+beyond)\b"
        r"[^.\n;:]{0,80}\b(?:this|current)\s+branch\b",
        normalized,
    )
    if future_scope_match and future_scope_match.start() <= positive_match.start():
        return False

    postfixed_future_scope_match = re.search(
        r"\b(?:multi[- ]slice|multiple\s+slices)\b[^.\n;:]{0,140}"
        r"\b(?:future[- ]gated|user[- ]gated|deferred|later)\b[^.\n;:]{0,120}"
        r"\b(?:outside|out\s+of\s+scope|not\s+part\s+of|excluded\s+from)\b"
        r"[^.\n;:]{0,80}\b(?:this|current)\s+branch\b",
        normalized,
    )
    if (
        postfixed_future_scope_match
        and postfixed_future_scope_match.start() == positive_match.start()
    ):
        return False

    policy_non_carrier_match = re.search(
        r"\b(?:validat(?:e|es|ing)|validator|governance|policy|prevent(?:s|ing)?|"
        r"check(?:s|ing)?)\b[^.\n;:]{0,120}\b(?:multi[- ]slice|multiple\s+slices)\b"
        r"[^.\n;:]{0,160}\b(?:without|not)\b[^.\n;:]{0,120}"
        r"\b(?:carrier|creating|making|becoming|current\s+scope)\b",
        normalized,
    )
    if policy_non_carrier_match and policy_non_carrier_match.start() <= positive_match.start():
        return False
    return True


def multi_slice_marker_value_is_negative(value: str) -> bool:
    normalized = normalized_route_value(value)
    negative_patterns = (
        r"^(?:no|false|n/a|none|not applicable|not required)\.?$",
        r"^(?:not applicable|not required|n/a|none)\b.*\b(?:future|deferred|user[- ]gated|outside|out\s+of\s+scope)\b",
        r"^(?:future[- ]gated|deferred|not current|non[- ]current)\b.*\b(?:multi[- ]slice|multiple\s+slices)\b.*\b(?:future[- ]gated|user[- ]gated|deferred|outside|out\s+of\s+scope|not\s+current|non[- ]current)\b",
        r"\bnot\s+a?\s*multi[- ]slice\s+carrier\b",
        r"\bnot\s+multi[- ]slice\b",
        r"\bnon[- ]multi[- ]slice\b",
        r"\bsingle[- ]slice\b",
        r"\bone\s+slice\b",
        r"\bno\s+current\s+multi[- ]slice\b",
    )
    return any(re.search(pattern, normalized) for pattern in negative_patterns)


def plan_declares_multi_slice_carrier(plan_text: str) -> bool:
    carrier_value = markdown_field_value(plan_text, "Multi-Slice Carrier")
    slice_map = markdown_field_value_with_continuation(plan_text, "Slice Map")
    if slice_map and slice_map_deliverable_count(slice_map) >= 2:
        return True

    if carrier_value:
        return not multi_slice_marker_value_is_negative(carrier_value)

    current_scope_fields = (
        "Package Summary",
        "Package",
    )
    return any(
        value_declares_multi_slice(value)
        for field in current_scope_fields
        if (value := markdown_field_value_with_continuation(plan_text, field))
    )


def same_branch_split_decision_is_positive(value: str) -> bool:
    normalized = normalized_route_value(value)
    if re.search(
        r"\bno\s+separate\s+branch\s+required\b[^.\n]{0,160}"
        r"\bsame\s+branch\s+(?:remains|is|can\s+remain|may\s+remain)\s+legal\b",
        normalized,
    ):
        return True
    hard_negative_terms = (
        "same branch is not legal",
        "same branch not legal",
        "same branch is illegal",
        "not legal for same branch",
        "not legal in same branch",
        "cannot stay same branch",
        "cannot remain same branch",
        "must split",
        "required separate branch",
        "separate branch required",
        "different branch required",
        "same-branch blocked",
        "blocked same branch",
        "whether same branch",
        "pending decision",
        "before deciding",
        "deciding whether",
        "decide whether",
    )
    if any(term in normalized for term in hard_negative_terms):
        return False
    positive_terms = (
        "no split required",
        "split not required",
        "same branch remains legal",
        "same branch is legal",
        "same branch legal",
        "same branch remains valid",
        "same branch can remain legal",
        "same branch may remain legal",
        "same branch remains the legal",
        "same branch remains the approved",
        "same branch carrier",
        "same branch package",
    )
    if any(term in normalized for term in positive_terms):
        return True
    if "split required" in normalized:
        return False
    return False


def separate_branch_split_required_is_positive(value: str) -> bool:
    normalized = normalized_route_value(value)
    negative_terms = (
        "not required",
        "not needed",
        "not necessary",
        "split not required",
        "no split",
        "keep same branch",
        "same branch remains",
        "same branch is legal",
        "same branch legal",
        "same branch carrier",
        "same branch package",
        "remain same branch",
        "split optional",
        "whether to split",
        "deciding whether",
        "decide whether",
        "pending decision",
    )
    if any(term in normalized for term in negative_terms):
        return False
    explicit_split_terms = (
        "split required",
        "separate branch required",
        "required separate branch",
        "separate carrier",
        "separate user-approved carrier",
        "different branch",
        "different carrier",
        "must split",
        "must wait for a separate",
    )
    if any(term in normalized for term in explicit_split_terms):
        return True
    if normalized.startswith(("yes.", "yes;", "yes:", "yes ")):
        return any(term in normalized for term in explicit_split_terms)
    return normalized == "yes"


def validate_implementation_route_values(plan_text: str) -> list[str]:
    issues: list[str] = []
    marker_values = {
        "Selected Implementation Route": markdown_field_value(
            plan_text, "Selected Implementation Route"
        )
        or "",
        "Concrete Deliverable": markdown_field_value(plan_text, "Concrete Deliverable")
        or "",
        "Implementation Output": markdown_field_value(
            plan_text, "Implementation Output"
        )
        or "",
        "Infrastructure / Setup Relationship": markdown_field_value(
            plan_text, "Infrastructure / Setup Relationship"
        )
        or "",
        "USER Action Gate": markdown_field_value(plan_text, "USER Action Gate") or "",
        "Route Disposition": markdown_field_value(plan_text, "Route Disposition") or "",
        "Retarget / Rename Recommendation": markdown_field_value(
            plan_text, "Retarget / Rename Recommendation"
        )
        or "",
    }
    combined_route = normalized_route_value(
        "\n".join(
            (
                marker_values["Selected Implementation Route"],
                marker_values["Concrete Deliverable"],
                marker_values["Implementation Output"],
            )
        )
    )
    full_normalized = normalized_route_value(plan_text)
    setup_normalized = normalized_route_value(
        marker_values["Infrastructure / Setup Relationship"]
    )
    disposition_normalized = normalized_route_value(marker_values["Route Disposition"])
    retarget_normalized = normalized_route_value(
        marker_values["Retarget / Rename Recommendation"]
    )
    user_gate = marker_values["USER Action Gate"]

    concrete_terms = (
        "implementation",
        "enforcement",
        "runtime",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "consent shell",
        "trust-boundary",
        "security",
        "capability-pack",
        "memory/cache",
        "provider",
        "user-facing",
        "workflow",
    )
    concrete_behavior_terms = (
        "enforce",
        "block",
        "validate",
        "fail-closed",
        "detect",
        "route",
        "render",
        "persist",
        "execute",
        "control",
        "runtime",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "user-facing",
    )
    actual_implementation_terms = (
        "implement",
        "implemented",
        "enforce",
        "enforcement",
        "block",
        "reject",
        "prevent",
        "fail-closed",
        "fails closed",
        "validate",
        "persist",
        "execute",
        "route",
        "disable",
        "update",
        "create",
    )
    implemented_target_terms = (
        "behavior",
        "control",
        "workflow",
        "surface",
        "state",
        "transition",
        "enforcement",
        "consent shell",
        "consent-shell",
        "trust-boundary",
        "boundary",
        "exclusion",
        "suppression",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "runtime",
        "user-facing",
    )
    evidence_only_route_terms = (
        "proof package",
        "proof packet",
        "validation proof",
        "setup proof",
        "readiness proof",
        "registry proof",
        "boundary proof",
        "review packet",
        "packet generation",
        "decision path",
        "readiness matrix",
        "validation plan",
        "boundary controls",
        "boundary-control labels",
    )
    tbd_route_terms = (
        "implementation output is tbd",
        "tbd",
        "to be determined",
        "decide later",
        "selected later",
        "later during bp2",
        "bp2 will choose",
        "bp2 will decide",
    )
    negated_real_behavior_terms = (
        "does not add behavior",
        "does not change behavior",
        "does not change state",
        "does not enforce",
        "does not implement",
        "will not add behavior",
        "will not change behavior",
        "will not enforce",
        "will not implement",
        "no enforcement behavior",
        "no implemented behavior",
        "no implemented control",
        "no validator behavior",
        "no runtime behavior",
        "no source-truth behavior",
        "no user-facing surface",
        "no state transition",
        "behavior changes are deferred",
        "without implemented behavior",
    )
    planning_only_terms = (
        "planning-only",
        "readiness-only",
        "setup-only",
        "lane setup only",
        "choose later branches",
        "identify later branches",
        "no implementation route",
        "implementation output: none",
    )
    fake_feature_terms = (
        "setup feature",
        "readiness feature",
        "planning feature",
        "decision feature",
        "registry feature",
        "skeleton feature",
        "packet feature",
        "review feature",
        "feature label",
    )

    real_behavior_present = (
        any(term in combined_route for term in actual_implementation_terms)
        and any(term in combined_route for term in implemented_target_terms)
        and not any(term in combined_route for term in negated_real_behavior_terms)
    )
    if (
        route_word_count(marker_values["Concrete Deliverable"]) < 8
        or route_word_count(marker_values["Implementation Output"]) < 8
        or not any(term in combined_route for term in concrete_terms)
        or not real_behavior_present
        or any(term in combined_route for term in planning_only_terms)
    ):
        issues.append(
            "External active branch plan route values must name a concrete "
            "implementation behavior before BP1"
        )
    if any(term in combined_route for term in negated_real_behavior_terms):
        issues.append(
            "External active branch plan route values cannot negate implementation behavior"
        )
    if (
        any(term in combined_route for term in evidence_only_route_terms)
        and not real_behavior_present
    ):
        issues.append(
            "External active branch plan route values cannot substitute proof, readiness, "
            "or boundary-label evidence for implementation behavior"
        )
    if any(term in combined_route for term in tbd_route_terms):
        issues.append(
            "External active branch plan route values cannot defer implementation output "
            "to BP2 or a later decision"
        )
    if any(term in combined_route for term in fake_feature_terms) and not (
        real_behavior_present
        and any(term in combined_route for term in concrete_behavior_terms)
    ):
        issues.append(
            "External active branch plan route values cannot label planning, setup, "
            "registry, skeleton, packet, or review work as the feature"
        )
    if any(
        term in full_normalized
        for term in (
            "lane setup",
            "repo/root/remote",
            "private root",
            "private remote",
            "skeleton setup",
            "registry creation",
        )
    ) and not (
        "execution-enabling" in setup_normalized
        or "selected implementation route" in setup_normalized
        or "exact user action gate" in setup_normalized
    ):
        issues.append(
            "External active branch plan infrastructure/setup values must tie to "
            "the selected route or exact USER action gate"
        )
    if "Dev lane" in plan_text:
        issues.append("Use Developer lane, not Dev lane, in current branch-planning text")
    if "developer" in full_normalized and "Developer lane" not in plan_text:
        issues.append(
            "Developer lane terminology must be explicit when developer lane scope appears"
        )
    if "hold" in disposition_normalized and route_word_count(user_gate) < 6:
        issues.append("External active branch plan HOLD requires an exact USER action gate")
    if (
        "retarget" in disposition_normalized or "rename" in disposition_normalized
    ) and not (
        ("retarget" in retarget_normalized or "rename" in retarget_normalized)
        and any(term in retarget_normalized for term in concrete_terms)
    ):
        issues.append(
            "External active branch plan retarget/rename disposition requires "
            "a concrete recommendation"
        )
    if route_word_count(user_gate) < 6:
        issues.append(
            "External active branch plan route values must name pending USER action gate posture"
        )
    return issues


def validate_slice_slc_seam_model_text(plan_text: str) -> list[str]:
    issues: list[str] = []
    normalized = normalized_route_value(plan_text)
    ambiguity_patterns = (
        r"\bslc(?:[- ]\d+)?\s+is\s+the\s+seam\b",
        r"\bslcs\s+are\s+seams\b",
        r"\bslc(?:[- ]\d+)?\s+means\s+seam\b",
        r"\bslice\s+is\s+(?:the\s+)?proof\b",
        r"\bseam\s+is\s+the\s+branch\s+deliverable\b",
        r"\bseam\s+is\s+the\s+feature\b",
        r"\bseam-only\s+branch\b",
        r"\bslc[- ]\d+\s+branch(?:es)?(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+\s+(?:owns|has)\s+(?:a\s+|the\s+|its\s+own\s+)?branch(?:es)?(?=[\s.,;:]|$)",
        r"\bslcs\s+(?:own|owns|have|has)\s+(?:a\s+|the\s+|their\s+own\s+)?branch(?:es)?(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+(?:own|owns|have|has)\s+(?:a\s+|the\s+|their\s+own\s+|its\s+own\s+)?branch(?:es)?(?=[\s.,;:]|$)",
        r"\bbranch(?:es)?\s+(?:for|per)\s+slc[- ]\d+\b",
        r"\bslc(?:[- ]\d+)?\s+is\s+a\s+branch(?=[\s.,;:]|$)",
        r"\bslcs\s+are\s+branches(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+are\s+branches(?=[\s.,;:]|$)",
        r"\bslc(?:[- ]\d+)?\s+is\s+a\s+separate\s+branch(?=[\s.,;:]|$)",
        r"\bslcs\s+are\s+separate\s+branches(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+are\s+separate\s+branches(?=[\s.,;:]|$)",
        r"\bslc(?:[- ]\d+)?\s+becomes\s+a\s+branch(?=[\s.,;:]|$)",
        r"\bslcs\s+become\s+branches(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+become\s+branches(?=[\s.,;:]|$)",
        r"\bslc(?:[- ]\d+)?\s+creates\s+the\s+branch(?=[\s.,;:]|$)",
        r"\beach\s+slc(?:[- ]\d+)?\s+is\s+a\s+branch(?=[\s.,;:]|$)",
        r"\beach\s+slc(?:[- ]\d+)?\s+(?:owns|has)\s+(?:a\s+|the\s+|its\s+own\s+)?branch(?=[\s.,;:]|$)",
        r"\beach\s+slc(?:[- ]\d+)?\s+becomes\s+a\s+branch(?=[\s.,;:]|$)",
    )
    if any(re.search(pattern, normalized) for pattern in ambiguity_patterns):
        issues.append(
            "SLC / Slice / Seam terminology ambiguity: SLC must resolve to "
            "Slice-level deliverables, and seams must remain execution or "
            "validation checkpoints"
        )

    slc_slice_alias_terms = (
        "slice-level",
        "alias",
        "historical",
        "short form",
        "short-form",
        "shorthand",
        "abbreviation",
        "slc is slice",
        "slc means slice",
        "slc/slice",
        "slice/slc",
    )
    if "slc" in normalized and not any(
        term in normalized for term in slc_slice_alias_terms
    ):
        issues.append(
            "SLC / Slice / Seam terminology ambiguity: SLC use must name "
            "its Slice-level alias, shorthand, or historical traceability posture"
        )

    if plan_declares_multi_slice_carrier(plan_text):
        required_markers = (
            "FAM",
            "Package",
            "Selected Implementation Route",
            "Slice Map",
            "Shared Owner / Worktree",
            "Shared Validation / Proof Path",
            "Split Decision",
        )
        for marker in required_markers:
            marker_value = (
                markdown_field_value_with_continuation(plan_text, marker)
                if marker == "Slice Map"
                else markdown_field_value(plan_text, marker)
            )
            if not marker_value:
                issues.append(f"Multi-slice carrier missing {marker}:")
        route = markdown_field_value(plan_text, "Selected Implementation Route") or ""
        slice_map = markdown_field_value_with_continuation(plan_text, "Slice Map") or ""
        validation = (
            markdown_field_value(plan_text, "Shared Validation / Proof Path") or ""
        )
        split_decision = markdown_field_value(plan_text, "Split Decision") or ""
        if route_word_count(route) < 8:
            issues.append("Multi-slice carrier must name a concrete implementation route")
        if slice_map_mismatched_alias_pairs(slice_map):
            issues.append(
                "Multi-slice carrier Slice Map contains mismatched Slice/SLC alias pair"
            )
        if slice_map_deliverable_count(slice_map) < 2:
            issues.append("Multi-slice carrier must map at least two slices")
        if route_word_count(validation) < 8:
            issues.append(
                "Multi-slice carrier must name a shared validation/proof path"
            )
        if not same_branch_split_decision_is_positive(split_decision):
            issues.append("Multi-slice carrier must prove why the grouped branch is legal")

    if "required separate branch case:" in normalized:
        required_markers = (
            "Required Separate Branch Case",
            "Divergence Basis",
            "Split Required",
            "Blocked Same-Branch Reason",
            "Recommended Carrier",
        )
        for marker in required_markers:
            if not markdown_field_value(plan_text, marker):
                issues.append(f"Required separate branch case missing {marker}:")
        divergence = markdown_field_value(plan_text, "Divergence Basis") or ""
        split_required = markdown_field_value(plan_text, "Split Required") or ""
        if not any(
            term in divergence.casefold()
            for term in (
                "different fam",
                "different package",
                "private",
                "provider",
                "runtime",
                "release timing",
                "validation path",
                "owner/worktree",
            )
        ):
            issues.append(
                "Required separate branch case must name a real divergence basis"
            )
        if not separate_branch_split_required_is_positive(split_required):
            issues.append(
                "Required separate branch case must explicitly require a split"
            )
    return issues


def validate_active_branch_plan_posture(root: Path) -> list[str]:
    issues: list[str] = []
    active_state = root / "central" / "active_branch_authority_state.md"
    if not active_state.is_file():
        return issues

    active_text = active_state.read_text(encoding="utf-8")
    plan_path = active_branch_plan_path(active_text, root)
    branch_state_path = resolve_markdown_path(
        markdown_field_value(active_text, "Branch State"),
        root,
    )
    branch_state_text = (
        branch_state_path.read_text(encoding="utf-8")
        if branch_state_path and branch_state_path.is_file()
        else ""
    )
    bp1_value = "BP1 USER Branch Vision Review"
    active_routes_to_bp1 = bp1_value in {
        (markdown_field_value(active_text, "Next Gate") or "").strip("` "),
        (markdown_field_value(active_text, "Next Legal Phase") or "").strip("` "),
        (markdown_field_value(branch_state_text, "Next Legal Phase") or "").strip("` "),
    }
    if not active_routes_to_bp1:
        active_routes_to_bp1 = (
            "Next Gate: `BP1 USER Branch Vision Review`" in active_text
            or "Next Legal Phase: `BP1 USER Branch Vision Review`" in active_text
            or "Next Legal Phase: `BP1 USER Branch Vision Review`" in branch_state_text
            or "Next Gate: BP1 USER Branch Vision Review" in active_text
            or "Next Legal Phase: BP1 USER Branch Vision Review" in active_text
            or "Next Legal Phase: BP1 USER Branch Vision Review" in branch_state_text
        )
    if not active_routes_to_bp1:
        return issues

    if not plan_path or not plan_path.is_file():
        return [
            "External active branch state routes to BP1 without an existing active branch plan"
        ]

    plan_text = plan_path.read_text(encoding="utf-8")
    required_route_markers = (
        "Selected Implementation Route",
        "Implementation Route Class",
        "Concrete Deliverable",
        "Implementation Output",
        "Infrastructure / Setup Relationship",
        "USER Action Gate",
        "Route Disposition",
        "Retarget / Rename Recommendation",
    )
    missing_route_markers = [
        marker
        for marker in required_route_markers
        if not markdown_field_value(plan_text, marker)
    ]
    route_resolution_status = markdown_field_value(
        plan_text, "BR2 Route Resolution Status"
    )
    route_disposition = normalized_route_value(
        markdown_field_value(plan_text, "Route Disposition") or ""
    )
    has_hold_or_retarget = bool(route_resolution_status) or any(
        disposition in route_disposition
        for disposition in ("hold", "retarget", "rename")
    )
    if has_hold_or_retarget:
        issues.append(
            "External active branch state routes to BP1 while active branch plan "
            "is still HOLD/RETARGET route resolution"
        )
    if missing_route_markers:
        issues.append(
            "External active branch state routes to BP1 without "
            "implementation-bearing route fields in active branch plan: "
            + ", ".join(missing_route_markers)
        )
    else:
        issues.extend(validate_implementation_route_values(plan_text))
    issues.extend(validate_slice_slc_seam_model_text(plan_text))
    return issues


def validate_fam007_workstream_visual_acceptance_gate(root: Path) -> list[str]:
    issues: list[str] = []
    branch_root = root / "branches" / "feature_fam_007_ai_control_center_readiness_diagnostics"
    branch_state = branch_root / "branch_state.md"
    branch_plan = branch_root / "branch_plan.md"
    if not branch_state.is_file() or not branch_plan.is_file():
        return issues

    state_text = branch_state.read_text(encoding="utf-8")
    plan_text = branch_plan.read_text(encoding="utf-8")
    state_normalized = state_text.casefold()
    plan_normalized = plan_text.casefold()
    is_ui_workstream_repair = (
        "option g runtime ui repair implemented" in state_normalized
        or "workstream_implementation_repaired" in plan_normalized
        or "option g runtime adoption / child-window grammar repair" in plan_normalized
    )
    active_next = (
        markdown_field_value(state_text, "Next Legal Phase")
        or markdown_field_value(plan_text, "Next Legal Phase")
        or ""
    ).casefold()
    active_current_gate = (markdown_field_value(state_text, "Current Gate") or "").casefold()
    active_next_routes_to_visual_review = "workstream-exit visual acceptance" in active_next
    routes_to_h1_lv = (
        not active_next_routes_to_visual_review
        and (
            active_next.startswith("prepare hardening h1")
            or active_next.startswith("prepare a source-truth-routed hardening h1")
            or active_next.startswith("prepare h1")
            or active_next.startswith("hardening h1")
            or active_next.startswith("live validation")
            or active_next.startswith("h1/lv")
        )
    ) or (
        not active_next_routes_to_visual_review
        and (
            "prepare hardening h1" in active_next
            or "prepare a source-truth-routed hardening h1" in active_next
            or "prepare h1/lv" in active_next
        )
    ) or (
        "next legal gate is hardening h1" in active_current_gate
        or "next legal gate is h1" in active_current_gate
    )
    if not is_ui_workstream_repair or not routes_to_h1_lv:
        return issues

    gate_state = markdown_field_value(state_text, "Workstream Exit Visual Acceptance Gate State") or ""
    gate_state_norm = gate_state.casefold()
    accepted_or_waived = any(
        marker in gate_state_norm
        for marker in (
            "user accepted",
            "user waived",
            "user deferred with explicit source-truth boundary",
        )
    )
    if not accepted_or_waived:
        issues.append(
            "FAM-007 Workstream Visual Acceptance Gate Bypass: active state routes "
            "Option G UI/UX Workstream repair toward H1/LV before USER accepted, "
            "waived, or explicitly deferred the runtime visual acceptance gate"
        )
    return issues


def validate_markdown_record(
    path: Path,
    expected_schema: str,
    expected_source_head: str | None,
) -> list[str]:
    issues: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - local state read errors should be reported cleanly
        return [f"External State Corrupt: {path}: {exc}"]

    for field in REQUIRED_STATE_FIELDS:
        value = markdown_field_value(text, field)
        if not value:
            issues.append(f"External State Corrupt: {path}: missing {field}")
            continue
        if field == "External State Schema" and value != expected_schema:
            issues.append(
                f"External State Schema Conflict: {path}: expected {expected_schema}, found {value}"
            )
        if field == "Source Repo HEAD" and expected_source_head and value != expected_source_head:
            issues.append(
                f"External State Version Conflict: {path}: expected Source Repo HEAD "
                f"{expected_source_head}, found {value}"
            )
    return issues


def validate_stage4_records(
    root: Path,
    expected_schema: str,
    expected_source_head: str | None,
) -> list[str]:
    issues: list[str] = []
    for relative_record in REQUIRED_STAGE4_RECORDS:
        record_path = root / relative_record
        if not record_path.exists():
            issues.append(f"External State Missing: required migrated record missing: {relative_record}")
            continue
        issues.extend(validate_markdown_record(record_path, expected_schema, expected_source_head))
    return issues


def validate_released_locks(root: Path) -> list[str]:
    issues: list[str] = []
    locks_dir = root / "locks"
    if not locks_dir.exists():
        return ["External State Missing: locks directory missing"]
    for lock_path in sorted(locks_dir.glob("*.json")):
        try:
            payload = load_json(lock_path)
        except Exception as exc:  # noqa: BLE001 - corrupt lock files block local operational workflow
            issues.append(f"External State Corrupt: {lock_path}: {exc}")
            continue
        lock_state = str(payload.get("Lock State", "MISSING"))
        if lock_state not in {"Released", "Expired"}:
            issues.append(f"Stale Lock Recovery Required: {lock_path}: Lock State is {lock_state}")
    return issues


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    repo_paths = [resolve_path(path) for path in args.repo]
    issues = validate_canonical_root(root, repo_paths)

    print("External State Validation")
    print(f"Root: {root}")
    print(f"Root Required: {'YES' if args.require_root else 'NO'}")
    print(f"Stage 4 Records Required: {'YES' if args.require_stage4_records else 'NO'}")

    if issues:
        print("Validation Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    if not root.exists():
        print("Validation Result: External State Missing")
        if (
            args.require_root
            or args.require_stage4_records
            or args.expected_source_head
            or args.target_currentness
            or args.projection_set_semantic_coherence
        ):
            print("Clean Clone Boundary: BLOCKED - required local external-state validation needs the root")
            return 1
        print("Clean Clone Boundary: PASS - missing root is not a repo validation failure")
        return 0

    if args.target_currentness and args.projection_set_semantic_coherence:
        print("Validation Result: BLOCKED")
        print("Target-scoped currentness and projection-set semantic coherence are mutually exclusive modes")
        return 1

    if args.target_currentness:
        if args.require_stage4_records:
            print("Validation Result: BLOCKED")
            print("Target-scoped currentness cannot be combined with global Stage 4 record validation")
            return 1
        initialization_issues = validate_initialized_root(root, args.schema)
        if initialization_issues:
            print("Validation Scope: TARGET_SCOPED_CURRENTNESS")
            print("Root Manifest Posture: BLOCKED - target currentness requires an initialized external-state root")
            print("Target Currentness Validation: BLOCKED")
            for issue in initialization_issues:
                print(issue)
            return 1
        target_issues = validate_target_currentness(
            root,
            args.target,
            expected_branch=args.expected_branch,
            expected_source_head=args.expected_source_head,
            expected_origin_main=args.expected_origin_main,
            expected_worktree_path=args.expected_worktree_path,
            expected_worktree_slot=args.expected_worktree_slot,
            expected_target_sha256=args.expected_target_sha256,
            expected_schema=args.schema,
        )
        print("Validation Scope: TARGET_SCOPED_CURRENTNESS")
        print(f"Selected Target: {args.target[0] if args.target else 'MISSING'}")
        print("Root Manifest Posture: STRUCTURAL_ONLY - root initialization/index posture is reported separately and is not asserted current for this target")
        if target_issues:
            print("Target Currentness Validation: BLOCKED")
            for issue in target_issues:
                print(issue)
            return 1
        print("Target Currentness Validation: PASS")
        print("Target PASS Is Root-Wide PASS: NO")
        return 0

    if args.projection_set_semantic_coherence:
        if args.require_stage4_records:
            print("Validation Result: BLOCKED")
            print("Projection-set semantic coherence cannot be combined with global Stage 4 record validation")
            return 1
        initialization_issues = validate_initialized_root(root, args.schema)
        if initialization_issues:
            print("Validation Scope: PROJECTION_SET_SEMANTIC_COHERENCE")
            print("Root Manifest Posture: BLOCKED - semantic coherence requires an initialized external-state root")
            print("Projection Set Semantic Coherence: BLOCKED")
            for issue in initialization_issues:
                print(issue)
            return 1
        target_hashes, hash_failures = _parse_target_hash_pairs(args.expected_target_hash)
        semantic_issues = hash_failures + validate_projection_set_semantic_coherence(
            root,
            args.target,
            expected_target_hashes=target_hashes,
            expected_branch=args.expected_branch,
            expected_source_head=args.expected_source_head,
            expected_origin_main=args.expected_origin_main,
            expected_worktree_path=args.expected_worktree_path,
            expected_worktree_slot=args.expected_worktree_slot,
            expected_current_gate=args.expected_current_gate,
            expected_workstream_result=args.expected_workstream_result,
            expected_stage_states=args.expected_stage_states,
            expected_next_legal_phase=args.expected_next_legal_phase,
            expected_transition_status=args.expected_transition_status,
            expected_state_version=args.expected_state_version,
            expected_last_updated_by=args.expected_last_updated_by,
            previous_snapshot=args.previous_snapshot,
            completion_audit=args.completion_audit,
            primary_review=args.primary_review,
            expected_decision_1=args.expected_decision_1,
            expected_decision_2=args.expected_decision_2,
            expected_decision_3=args.expected_decision_3,
            expected_completion_transition_status=args.expected_completion_transition_status,
            expected_schema=args.schema,
        )
        print("Validation Scope: PROJECTION_SET_SEMANTIC_COHERENCE")
        print("Selected Targets: " + (", ".join(args.target) if args.target else "MISSING"))
        print("Root Manifest Posture: STRUCTURAL_ONLY - selected projection semantics do not assert root-wide currentness")
        if semantic_issues:
            print("Projection Set Semantic Coherence: BLOCKED")
            for issue in semantic_issues:
                print(issue)
            return 1
        print("Projection Set Semantic Coherence: PASS")
        print("Historical Receipt Text Defines Current State: NO")
        print("Projection Set PASS Is Root-Wide PASS: NO")
        return 0

    manifest_path = root / "state_manifest.json"
    if not manifest_path.exists():
        issues.append("External State Corrupt: state_manifest.json missing")
    else:
        issues.extend(validate_manifest(manifest_path, args.schema))
        if args.expected_source_head:
            try:
                manifest = load_json(manifest_path)
                source_head = manifest.get("Source Repo HEAD")
                if source_head != args.expected_source_head:
                    issues.append(
                        "External State Version Conflict: expected manifest Source Repo HEAD "
                        f"{args.expected_source_head}, found {source_head or 'MISSING'}"
                    )
            except Exception as exc:  # noqa: BLE001 - duplicate manifest read for clearer source-head issue
                issues.append(f"External State Corrupt: {manifest_path}: {exc}")

    schemas = set()
    for state_file in iter_state_files(root):
        if state_file.suffix.lower() != ".json":
            continue
        if state_file == manifest_path:
            continue
        try:
            payload = load_json(state_file)
        except Exception as exc:  # noqa: BLE001 - report corrupt local state, do not hide parser detail
            issues.append(f"External State Corrupt: {state_file}: {exc}")
            continue
        schema = payload.get("External State Schema")
        if not schema:
            issues.append(f"External State Corrupt: {state_file}: missing External State Schema")
            continue
        schemas.add(str(schema))
    if len(schemas) > 1 or (schemas and args.schema not in schemas):
        issues.append(
            "External State Schema Conflict: mixed or unsupported schema values found: "
            + ", ".join(sorted(schemas))
        )

    if args.require_stage4_records:
        issues.extend(validate_stage4_records(root, args.schema, args.expected_source_head))
        issues.extend(validate_released_locks(root))
        issues.extend(validate_active_branch_plan_posture(root))
        issues.extend(validate_fam007_workstream_visual_acceptance_gate(root))

    if issues:
        print("Validation Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    if args.require_stage4_records:
        print("Stage 4 Migrated Record Validation: PASS")
    print("Validation Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
