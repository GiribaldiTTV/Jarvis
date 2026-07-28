from __future__ import annotations

import argparse
import re
from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    ExternalStateError,
    atomic_write_json,
    new_lock_id,
    resolve_path,
    utc_now,
    validate_canonical_root,
    validate_initialized_root,
)
from orin_external_state_lock_lifecycle import LOCK_TYPES, inspect_lock_table, lock_table_guard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create dry-run or applied External Governance State lock packets.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--lock-type", required=True, choices=sorted(LOCK_TYPES))
    parser.add_argument("--owner", required=True)
    parser.add_argument(
        "--workload-id",
        help="Exact Codex workload identity. Required for applied locks.",
    )
    parser.add_argument(
        "--owner-process-id",
        type=int,
        help="Optional long-lived process that owns the protected transaction.",
    )
    parser.add_argument("--worktree", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--intended-write-set", required=True)
    parser.add_argument("--expires", required=True, help="Expiration timestamp or policy text")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA_VERSION)
    parser.add_argument("--apply", action="store_true", help="Write lock file. Omit for dry-run packet.")
    return parser


def _write_set(raw: str) -> set[str]:
    return {item.strip().replace("\\", "/") for item in raw.split(";") if item.strip()}


def _write_set_failures(targets: set[str], raw: str) -> list[str]:
    failures: list[str] = []
    raw_targets = [item.strip().replace("\\", "/") for item in raw.split(";") if item.strip()]
    for target in raw_targets:
        parts = target.split("/")
        if (
            target.startswith("/")
            or re.match(r"^[A-Za-z]:", target)
            or any(part in {"", ".", ".."} for part in parts)
        ):
            failures.append(f"External State Lock Target Invalid: {target!r}")
    target_keys = [target.casefold() for target in raw_targets]
    if len(target_keys) != len(set(target_keys)) or len(targets) != len(raw_targets):
        failures.append("External State Lock Target Invalid: duplicate or aliased target")
    return failures


def _targets_overlap(left: str, right: str) -> bool:
    left_parts = tuple(part.casefold() for part in left.split("/"))
    right_parts = tuple(part.casefold() for part in right.split("/"))
    shared = min(len(left_parts), len(right_parts))
    return left_parts[:shared] == right_parts[:shared]


def _lock_conflicts(root, *, workload_id: str | None, lock_type: str, targets: set[str]) -> list[str]:
    failures: list[str] = []
    target_keys = {target.casefold() for target in targets}
    for inspection in inspect_lock_table(root, current_workload_id=workload_id):
        if inspection.classification == "MALFORMED":
            failures.append(
                f"External State Corrupt: lock table contains malformed entry {inspection.path}"
            )
            continue
        if not inspection.active:
            continue
        existing_target_keys = {
            target.casefold() for target in _write_set(inspection.intended_write_set)
        }
        broad_lock = inspection.lock_type in {"state-root", "migration"} or lock_type in {
            "state-root",
            "migration",
        }
        path_overlap = any(
            _targets_overlap(requested, existing)
            for requested in target_keys
            for existing in existing_target_keys
        )
        if broad_lock or path_overlap:
            failures.append(
                "External State Owner Conflict: overlapping active lock "
                f"{inspection.lock_id} ({inspection.classification})"
            )
    return failures


def acquire_lock(
    *,
    root,
    lock_type: str,
    owner: str,
    workload_id: str | None,
    worktree: str,
    branch: str,
    intended_write_set: str,
    expires: str,
    schema: str = DEFAULT_SCHEMA_VERSION,
    owner_process_id: int | None = None,
    apply: bool = False,
) -> tuple[bool, list[str], str]:
    root = resolve_path(root)
    failures = validate_canonical_root(root)
    lock_type_valid = lock_type in LOCK_TYPES
    if not lock_type_valid:
        failures.append(
            f"External State Lock Type Invalid: unsupported lock type {lock_type!r}"
        )
    targets = _write_set(intended_write_set)
    if not targets:
        failures.append("External State Lock Missing: exact intended write set is empty")
    failures.extend(_write_set_failures(targets, intended_write_set))
    if apply and not (workload_id or "").strip():
        failures.append("External State Lock Missing: --workload-id is required with --apply")
    if owner_process_id is not None and owner_process_id <= 0:
        failures.append("External State Lock Owner Process Invalid: process ID must be positive")
    if not root.exists():
        failures.append("External State Missing: canonical root does not exist")
    else:
        failures.extend(validate_initialized_root(root, schema))

    lock_id = (
        new_lock_id(lock_type)
        if lock_type_valid
        else "INVALID-LOCK-TYPE-NOT-ACQUIRED"
    )
    if failures:
        return False, failures, lock_id
    acquired_at = utc_now()
    lock_payload = {
        "External State Schema": schema,
        "State Version": 1,
        "Last Updated": acquired_at,
        "Last Updated By": owner,
        "Worktree": worktree,
        "Branch": branch,
        "Source Repo HEAD": "not captured by lock scaffold",
        "Lock ID": lock_id,
        "Lock Type": lock_type,
        "Lock State": "Locked",
        "Workload ID": workload_id or "DRY-RUN-NOT-APPLIED",
        "Workload State": "Active",
        "Owning Process ID": owner_process_id if owner_process_id is not None else "Not recorded",
        "Acquired At": acquired_at,
        "Last Activity At": acquired_at,
        "Intended Write Set": ";".join(sorted(targets)),
        "Expiration": expires,
        "Retain Between Workloads": "No",
        "Release Required Before Final Digest": "Yes",
    }

    if not apply:
        failures.extend(
            _lock_conflicts(
                root,
                workload_id=workload_id,
                lock_type=lock_type,
                targets=targets,
            )
        )
        if failures:
            return False, failures, lock_id
        return True, ["READY - no lock file created"], lock_id

    try:
        with lock_table_guard(root):
            failures.extend(
                _lock_conflicts(
                    root,
                    workload_id=workload_id,
                    lock_type=lock_type,
                    targets=targets,
                )
            )
            if failures:
                return False, failures, lock_id
            lock_path = root / "locks" / f"{lock_id}.json"
            atomic_write_json(lock_path, lock_payload)
    except ExternalStateError as exc:
        return False, [str(exc)], lock_id
    return True, [f"APPLIED - {lock_path}"], lock_id


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    ok, messages, lock_id = acquire_lock(
        root=root,
        lock_type=args.lock_type,
        owner=args.owner,
        workload_id=args.workload_id,
        owner_process_id=args.owner_process_id,
        worktree=args.worktree,
        branch=args.branch,
        intended_write_set=args.intended_write_set,
        expires=args.expires,
        schema=args.schema,
        apply=args.apply,
    )

    print("External State Lock Packet")
    print(f"Root: {root}")
    print(f"Lock ID: {lock_id}")
    print(f"Lock Type: {args.lock_type}")
    print("Lock State: Locked")
    print(f"Workload ID: {args.workload_id or 'MISSING'}")
    print(f"Owner Process ID: {args.owner_process_id or 'Not recorded'}")
    print(f"Mutation Approval: {'Granted by --apply' if args.apply else 'Not granted - dry run'}")
    if not ok:
        print("Lock Result: BLOCKED")
        for issue in messages:
            print(issue)
        return 1
    for message in messages:
        print(f"Lock Result: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
