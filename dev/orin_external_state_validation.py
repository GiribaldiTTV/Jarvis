from __future__ import annotations

import argparse
from pathlib import Path
import re

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    REQUIRED_STATE_FIELDS,
    iter_state_files,
    load_json,
    resolve_path,
    validate_canonical_root,
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
    pattern = re.compile(rf"^{re.escape(field)}:\s*`?([^`\n]+?)`?\s*$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def resolve_markdown_path(value: str | None, root: Path) -> Path | None:
    if not value:
        return None
    cleaned = value.strip().strip("`").strip()
    if not cleaned:
        return None
    path = Path(cleaned)
    return path if path.is_absolute() else root / cleaned


def normalized_route_value(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def route_word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9_/-]*", value))


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


def validate_active_branch_plan_posture(root: Path) -> list[str]:
    issues: list[str] = []
    active_state = root / "central" / "active_branch_authority_state.md"
    if not active_state.is_file():
        return issues

    active_text = active_state.read_text(encoding="utf-8")
    plan_path = resolve_markdown_path(
        markdown_field_value(active_text, "Branch Runtime Engineering Plan"),
        root,
    )
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
    has_hold_or_retarget = (
        "BR2 Route Resolution Status:" in plan_text
        or "Route Disposition: `HOLD" in plan_text
        or "Route Disposition: HOLD" in plan_text
        or "Route Disposition: `RETARGET" in plan_text
        or "Route Disposition: RETARGET" in plan_text
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
        if args.require_root or args.require_stage4_records or args.expected_source_head:
            print("Clean Clone Boundary: BLOCKED - required local external-state validation needs the root")
            return 1
        print("Clean Clone Boundary: PASS - missing root is not a repo validation failure")
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
