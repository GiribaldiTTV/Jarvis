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
        if args.require_root or args.require_stage4_records:
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
