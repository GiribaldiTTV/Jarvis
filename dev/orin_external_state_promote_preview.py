from __future__ import annotations

import argparse

from orin_external_state_common import DEFAULT_EXTERNAL_STATE_ROOT, resolve_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview worktree-staging to central external-state promotion.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--source-state", required=True)
    parser.add_argument("--target-state", required=True)
    parser.add_argument("--reason", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    source_state = resolve_path(args.source_state)
    print("External State Promotion Preview")
    print(f"Root: {root}")
    print(f"Source State: {source_state}")
    print(f"Target State: {args.target_state}")
    print(f"Reason: {args.reason}")
    print("Required Before Apply: lock acquisition, central state version check, conflict scan, validation, audit log")
    print("Mutation Status: Not started - preview only")
    if not root.exists():
        print("Promotion Preview Result: External State Missing")
        return 0
    if not source_state.exists():
        print("Promotion Preview Result: BLOCKED - source state missing")
        return 1
    print("Promotion Preview Result: READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
