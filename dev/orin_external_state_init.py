from __future__ import annotations

import argparse

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    STATE_DIRECTORIES,
    atomic_write_json,
    atomic_write_text,
    git_branch,
    resolve_path,
    state_manifest_payload,
    validate_canonical_root,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare or apply the External Governance State bootstrap scaffold."
    )
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--worktree", required=True, help="Worktree label, e.g. Governance")
    parser.add_argument("--repo", required=True, help="Source repo path")
    parser.add_argument("--branch", help="Source branch; defaults to git branch for --repo")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA_VERSION)
    parser.add_argument("--initialization-scope", default="Bootstrap scaffold only")
    parser.add_argument("--created-by", default="Codex")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create the external state root. Omit for dry-run bootstrap packet.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    repo = resolve_path(args.repo)
    branch = args.branch or git_branch(repo)
    issues = validate_canonical_root(root, [repo])

    print("External State Bootstrap Packet")
    print(f"Desired Root: {root}")
    print(f"Worktree Label: {args.worktree}")
    print(f"Source Repo Path: {repo}")
    print(f"Branch: {branch}")
    print(f"Schema Version: {args.schema}")
    print(f"Initialization Scope: {args.initialization_scope}")
    print(f"Mutation Approval: {'Granted by --apply' if args.apply else 'Not granted - dry run'}")

    if issues:
        print("Bootstrap Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    if not args.apply:
        print("Bootstrap Result: READY - no files created")
        print("Exact USER Decision Needed: approve --apply root initialization before active workflow uses central state")
        return 0

    root.mkdir(parents=True, exist_ok=True)
    for directory in STATE_DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)

    manifest = state_manifest_payload(
        root=root,
        worktree_label=args.worktree,
        repo=repo,
        branch=branch,
        schema=args.schema,
        created_by=args.created_by,
        initialization_scope=args.initialization_scope,
    )
    atomic_write_json(root / "state_manifest.json", manifest)
    atomic_write_text(
        root / "README.md",
        "# Nexus Governance State\n\n"
        "This local-private folder owns accepted operational state only after USER-approved initialization.\n"
        "Repo source truth remains the durable governance owner.\n",
    )
    atomic_write_text(
        root / "state_index.md",
        "# Generated External State Index\n\n"
        "Generated index placeholder. Primary state lives in branch, worktree, release-window, "
        "candidate, promotion, acknowledgement, and fold-down records.\n",
    )

    print("Bootstrap Result: APPLIED")
    print("External State Missing: CLEARED for initialized root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
