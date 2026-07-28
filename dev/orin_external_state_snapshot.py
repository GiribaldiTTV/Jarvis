from __future__ import annotations

import argparse
from contextlib import nullcontext
import re
import shutil
from pathlib import Path

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    atomic_write_json,
    copy_tree_snapshot,
    load_json,
    new_lock_id,
    resolve_path,
    sha256_file,
    utc_now,
    validate_canonical_root,
    validate_initialized_root,
)
from orin_external_state_lock_lifecycle import lock_table_guard


def _after_target_copy(_relative: str, _source: Path, _destination: Path) -> None:
    """Test seam for authoritative lock drift during a targeted snapshot."""


def _after_snapshot_guard_acquired(_snapshot_dir: Path) -> None:
    """Test seam for a same-name snapshot published while this invocation waits."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create dry-run or applied External Governance State snapshots.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--worktree", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--created-by", default="Codex")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA_VERSION)
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Exact relative target to snapshot; repeat for a bounded target set.",
    )
    parser.add_argument(
        "--snapshot-name",
        help="Deterministic snapshots/<name> directory. Required for applied targeted snapshots.",
    )
    parser.add_argument(
        "--lock-id",
        help="Workload lock admitting every target and snapshot directory. Required for applied targeted snapshots.",
    )
    parser.add_argument("--source-head", default="not captured by snapshot scaffold")
    parser.add_argument("--apply", action="store_true", help="Write snapshot files. Omit for dry-run.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    root_issues = validate_canonical_root(root)
    snapshot_name = args.snapshot_name or new_lock_id("snapshot")
    snapshot_dir = root / "snapshots" / snapshot_name

    print("External State Snapshot Packet")
    print(f"Root: {root}")
    print(f"Snapshot Directory: {snapshot_dir}")
    print(f"Reason: {args.reason}")
    print(f"Mutation Approval: {'Granted by --apply' if args.apply else 'Not granted - dry run'}")

    if root_issues:
        print("Snapshot Result: BLOCKED")
        for issue in root_issues:
            print(issue)
        return 1
    if not root.exists():
        print("Snapshot Result: External State Missing")
        return 1 if args.apply else 0
    initialization_issues = validate_initialized_root(root, args.schema)
    if initialization_issues:
        print("Snapshot Result: BLOCKED")
        for issue in initialization_issues:
            print(issue)
        return 1
    targeted = bool(args.target)
    if args.snapshot_name and not re.fullmatch(r"[A-Za-z0-9_.-]+", args.snapshot_name):
        print("Snapshot Result: BLOCKED")
        print(f"Snapshot name is not a safe directory name: {args.snapshot_name!r}")
        return 1
    if targeted and args.apply and not args.snapshot_name:
        print("Snapshot Result: BLOCKED")
        print("Applied targeted snapshot requires --snapshot-name")
        return 1
    if targeted and args.apply and not args.lock_id:
        print("Snapshot Result: BLOCKED")
        print("Applied targeted snapshot requires --lock-id")
        return 1
    resolved_targets: list[tuple[str, Path]] = []
    lock_payload: dict[str, object] | None = None
    if targeted:
        from orin_external_state_target_reconcile import (
            _lock_failures,
            _parse_intended_write_set,
        )
        from orin_external_state_validation import _resolve_target_path

        failures: list[str] = []
        seen: set[str] = set()
        for raw_target in args.target:
            relative, target_path, target_failures = _resolve_target_path(root, raw_target)
            failures.extend(target_failures)
            if relative is None or target_path is None:
                continue
            key = relative.casefold()
            if key in seen:
                failures.append(f"Targeted snapshot contains duplicate target: {relative}")
                continue
            seen.add(key)
            resolved_targets.append((relative, target_path))
        if args.apply and resolved_targets and args.lock_id:
            lock_payload, lock_failures = _lock_failures(
                root,
                args.lock_id,
                resolved_targets[0][0],
                args.branch,
                args.worktree,
            )
            failures.extend(lock_failures)
            if lock_payload is not None:
                workload_id = str(lock_payload.get("Workload ID", "")).strip()
                if not workload_id:
                    failures.append("Snapshot admitting lock omits Workload ID")
                admitted = _parse_intended_write_set(lock_payload.get("Intended Write Set", ""))
                required = {relative for relative, _path in resolved_targets}
                required.add(f"snapshots/{snapshot_name}")
                missing = sorted(required - admitted)
                if missing:
                    failures.append(
                        "Snapshot lock write set omits exact transaction targets: "
                        + ", ".join(missing)
                    )
        if failures:
            print("Snapshot Result: BLOCKED")
            for failure in failures:
                print(failure)
            return 1
    if not args.apply:
        print(
            "Snapshot Result: READY - no snapshot created; "
            f"target count={len(resolved_targets) if targeted else 'full root'}"
        )
        return 0

    if snapshot_dir.exists():
        print("Snapshot Result: BLOCKED")
        print(f"Snapshot directory already exists: {snapshot_dir}")
        return 1
    copied: list[dict[str, object]] = []
    try:
        transaction_guard = lock_table_guard(root) if targeted else nullcontext()
        with transaction_guard:
            _after_snapshot_guard_acquired(snapshot_dir)
            try:
                snapshot_dir.mkdir(parents=True, exist_ok=False)
            except FileExistsError:
                print("Snapshot Result: BLOCKED")
                print(f"Snapshot directory already exists: {snapshot_dir}")
                return 1
            transaction_lock_payload = lock_payload
            if targeted:
                transaction_lock_payload, transaction_lock_failures = _lock_failures(
                    root,
                    args.lock_id,
                    resolved_targets[0][0],
                    args.branch,
                    args.worktree,
                )
                if transaction_lock_failures or transaction_lock_payload != lock_payload:
                    lock_change_details = transaction_lock_failures or [
                        "authoritative lock payload differs from the preflight payload"
                    ]
                    raise RuntimeError(
                        "Snapshot admitting lock changed before the guarded copy transaction: "
                        + "; ".join(lock_change_details)
                    )
                admitted = _parse_intended_write_set(
                    transaction_lock_payload.get("Intended Write Set", "")
                )
                required = {relative for relative, _path in resolved_targets}
                required.add(f"snapshots/{snapshot_name}")
                missing = sorted(required - admitted)
                if missing:
                    raise RuntimeError(
                        "Snapshot lock write set changed before copy and omits: "
                        + ", ".join(missing)
                    )
                copied = []
            if targeted:
                for relative, source in resolved_targets:
                    source_before_hash = sha256_file(source)
                    destination = snapshot_dir.joinpath(*relative.split("/"))
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
                    destination_hash = sha256_file(destination)
                    source_after_hash = sha256_file(source)
                    if not (
                        source_before_hash.casefold()
                        == destination_hash.casefold()
                        == source_after_hash.casefold()
                    ):
                        raise RuntimeError(
                            f"Target changed during snapshot copy: {relative}"
                        )
                    copied.append(
                        {
                            "path": relative,
                            "sha256": destination_hash,
                            "size": destination.stat().st_size,
                        }
                    )
                    _after_target_copy(relative, source, destination)
                final_lock_payload, final_lock_failures = _lock_failures(
                    root,
                    args.lock_id,
                    resolved_targets[0][0],
                    args.branch,
                    args.worktree,
                )
                if final_lock_failures or final_lock_payload != transaction_lock_payload:
                    lock_change_details = final_lock_failures or [
                        "authoritative lock payload changed during copy"
                    ]
                    raise RuntimeError(
                        "Snapshot admitting lock changed during the guarded copy transaction: "
                        + "; ".join(lock_change_details)
                    )
            else:
                copied = copy_tree_snapshot(root, snapshot_dir)
            manifest = {
                "External State Schema": args.schema,
                "State Version": 1,
                "Last Updated": utc_now(),
                "Last Updated By": args.created_by,
                "Root": str(root.resolve()),
                "Worktree": args.worktree,
                "Branch": args.branch,
                "Source Repo HEAD": args.source_head,
                "Snapshot Reason": args.reason,
                "Lock ID": args.lock_id or "",
                "Workload ID": (
                    str(transaction_lock_payload.get("Workload ID", ""))
                    if transaction_lock_payload is not None
                    else ""
                ),
                "Copied Files": copied,
            }
            manifest_path = snapshot_dir / "snapshot_manifest.json"
            atomic_write_json(manifest_path, manifest)
            authoritative_manifest = load_json(manifest_path)
            if authoritative_manifest.get("Root") != str(root.resolve()):
                raise RuntimeError("authoritative snapshot manifest root mismatch")
            if authoritative_manifest.get("Copied Files") != copied:
                raise RuntimeError("authoritative snapshot manifest file inventory mismatch")
            if targeted and authoritative_manifest.get("Lock ID") != args.lock_id:
                raise RuntimeError("authoritative snapshot manifest lock identity mismatch")
            expected_workload_id = (
                str(transaction_lock_payload.get("Workload ID", ""))
                if transaction_lock_payload is not None
                else ""
            )
            if targeted and authoritative_manifest.get("Workload ID") != expected_workload_id:
                raise RuntimeError("authoritative snapshot manifest workload identity mismatch")
    except Exception as exc:  # noqa: BLE001 - a partial snapshot is never canonical
        shutil.rmtree(snapshot_dir, ignore_errors=True)
        print("Snapshot Result: BLOCKED")
        print(f"Snapshot transaction failed and partial output was removed: {exc}")
        return 1
    print(f"Snapshot Result: APPLIED - {len(copied)} files copied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
