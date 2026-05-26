from __future__ import annotations

import argparse

from orin_external_state_common import DEFAULT_EXTERNAL_STATE_ROOT, load_json, resolve_path, validate_canonical_root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report External Governance State root posture.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--repo", action="append", default=[], help="Repo path that root must not live inside")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    repo_paths = [resolve_path(path) for path in args.repo]
    issues = validate_canonical_root(root, repo_paths)

    print("External State Report")
    print(f"Root: {root}")
    print(f"Root Exists: {'YES' if root.exists() else 'NO'}")
    print(f"Canonical Root Check: {'PASS' if not issues else 'BLOCKED'}")
    for issue in issues:
        print(issue)
    if issues:
        print("External State Result: BLOCKED")
        return 1

    manifest_path = root / "state_manifest.json"
    if not root.exists():
        print("External State Result: External State Missing")
        return 0
    if not manifest_path.exists():
        print("External State Result: External State Corrupt - state_manifest.json missing")
        return 1

    manifest = load_json(manifest_path)
    print(f"External State Schema: {manifest.get('External State Schema', 'MISSING')}")
    print(f"State Version: {manifest.get('State Version', 'MISSING')}")
    print(f"Last Updated: {manifest.get('Last Updated', 'MISSING')}")
    print(f"Source Repo HEAD: {manifest.get('Source Repo HEAD', 'MISSING')}")
    print("External State Result: Clear")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
