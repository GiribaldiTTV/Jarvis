from __future__ import annotations

import argparse

from orin_external_state_common import DEFAULT_EXTERNAL_STATE_ROOT, iter_state_files, resolve_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview external-state fold-down candidates without mutation.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--branch-slug", help="Optional branch slug to focus the preview")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    print("External State Fold-Down Preview")
    print(f"Root: {root}")
    print(f"Branch Slug: {args.branch_slug or 'All'}")
    print("Mutation Status: Not started - preview only")

    if not root.exists():
        print("Preview Result: External State Missing")
        return 0

    files = iter_state_files(root)
    if args.branch_slug:
        needle = args.branch_slug.lower()
        files = [path for path in files if needle in path.as_posix().lower()]

    print(f"Candidate File Count: {len(files)}")
    for path in files[:100]:
        print(f"- {path.relative_to(root).as_posix()}")
    if len(files) > 100:
        print(f"- ... {len(files) - 100} more")
    print("Preview Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
