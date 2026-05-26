from __future__ import annotations

import argparse
from pathlib import Path

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    atomic_write_bytes,
    atomic_write_json,
    is_relative_to,
    resolve_path,
    sha256_file,
    utc_now,
    validate_canonical_root,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Promote staged external state into central state with no-loss audit.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--source-state", required=True)
    parser.add_argument("--target-state", required=True, help="Target path relative to external root")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--worktree", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--owner", default="Codex")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA_VERSION)
    parser.add_argument("--apply", action="store_true", help="Apply promotion. Omit for dry-run.")
    return parser


def resolve_target_state(root: Path, target_state: str) -> Path:
    relative_target = Path(target_state)
    if (
        not target_state.strip()
        or relative_target == Path(".")
        or relative_target.is_absolute()
        or any(part == ".." for part in relative_target.parts)
    ):
        raise ValueError("External State Owner Conflict: target state must stay relative to external root")
    target = resolve_path(root / relative_target)
    if not is_relative_to(target, root):
        raise ValueError("External State Owner Conflict: target state resolves outside external root")
    return target


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    source_state = resolve_path(args.source_state)
    root_issues = validate_canonical_root(root)
    try:
        target_state = resolve_target_state(root, args.target_state)
    except ValueError as exc:
        target_state = root / args.target_state
        target_error = str(exc)
    else:
        target_error = ""

    print("External State Promotion Packet")
    print(f"Root: {root}")
    print(f"Source State: {source_state}")
    print(f"Target State: {target_state}")
    print(f"Reason: {args.reason}")
    print(f"Mutation Approval: {'Granted by --apply' if args.apply else 'Not granted - dry run'}")

    if root_issues:
        print("Promotion Result: BLOCKED")
        for issue in root_issues:
            print(issue)
        return 1
    if target_error:
        print("Promotion Result: BLOCKED")
        print(target_error)
        return 1
    if not root.exists():
        print("Promotion Result: External State Missing")
        return 1 if args.apply else 0
    if not source_state.exists() or not source_state.is_file():
        print("Promotion Result: BLOCKED - source state missing")
        return 1
    if not args.apply:
        print("Promotion Result: READY - no files changed")
        return 0

    atomic_write_bytes(target_state, source_state.read_bytes())
    audit_payload = {
        "External State Schema": args.schema,
        "State Version": 1,
        "Last Updated": utc_now(),
        "Last Updated By": args.owner,
        "Worktree": args.worktree,
        "Branch": args.branch,
        "Source Repo HEAD": "not captured by promote scaffold",
        "Promotion Result": "Approved",
        "Source State": str(source_state),
        "Source SHA256": sha256_file(source_state),
        "Target State": str(target_state),
        "Reason": args.reason,
        "No-Loss Rule": "Source staging file preserved by default",
    }
    audit_name = "promotion-" + utc_now().replace(":", "").replace("+00:00", "Z") + ".json"
    atomic_write_json(root / "audit_log" / audit_name, audit_payload)
    print(f"Promotion Result: APPLIED - audit_log/{audit_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
