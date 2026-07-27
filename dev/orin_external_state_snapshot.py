from __future__ import annotations

import argparse
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
    if targeted and args.snapshot_name and not re.fullmatch(r"[A-Za-z0-9_.-]+", args.snapshot_name):
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
            payload, lock_failures = _lock_failures(
                root,
                args.lock_id,
                resolved_targets[0][0],
                args.branch,
                args.worktree,
            )
            failures.extend(lock_failures)
            if payload is not None:
                admitted = _parse_intended_write_set(payload.get("Intended Write Set", ""))
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
    if targeted:
        copied: list[dict[str, object]] = []
        try:
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
        except Exception as exc:  # noqa: BLE001 - a partial snapshot is never canonical
            shutil.rmtree(snapshot_dir, ignore_errors=True)
            print("Snapshot Result: BLOCKED")
            print(f"Targeted snapshot failed and partial output was removed: {exc}")
            return 1
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
        "Copied Files": copied,
    }
    manifest_path = snapshot_dir / "snapshot_manifest.json"
    try:
        atomic_write_json(manifest_path, manifest)
        authoritative_manifest = load_json(manifest_path)
        if authoritative_manifest.get("Root") != str(root.resolve()):
            raise RuntimeError("authoritative snapshot manifest root mismatch")
        if authoritative_manifest.get("Copied Files") != copied:
            raise RuntimeError("authoritative snapshot manifest file inventory mismatch")
    except Exception as exc:  # noqa: BLE001 - manifest proof is part of the snapshot
        shutil.rmtree(snapshot_dir, ignore_errors=True)
        print("Snapshot Result: BLOCKED")
        print(f"Snapshot manifest failed and snapshot output was removed: {exc}")
        return 1
    print(f"Snapshot Result: APPLIED - {len(copied)} files copied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
