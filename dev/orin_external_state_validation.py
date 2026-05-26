from __future__ import annotations

import argparse
from pathlib import Path

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    REQUIRED_STATE_FIELDS,
    iter_state_files,
    load_json,
    resolve_path,
    validate_canonical_root,
)


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


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    repo_paths = [resolve_path(path) for path in args.repo]
    issues = validate_canonical_root(root, repo_paths)

    print("External State Validation")
    print(f"Root: {root}")
    print(f"Root Required: {'YES' if args.require_root else 'NO'}")

    if issues:
        print("Validation Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    if not root.exists():
        print("Validation Result: External State Missing")
        print("Clean Clone Boundary: PASS - missing root is not a repo validation failure")
        return 1 if args.require_root else 0

    manifest_path = root / "state_manifest.json"
    if not manifest_path.exists():
        issues.append("External State Corrupt: state_manifest.json missing")
    else:
        issues.extend(validate_manifest(manifest_path, args.schema))

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
        if schema:
            schemas.add(str(schema))
    if len(schemas) > 1 or (schemas and args.schema not in schemas):
        issues.append(
            "External State Schema Conflict: mixed or unsupported schema values found: "
            + ", ".join(sorted(schemas))
        )

    if issues:
        print("Validation Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    print("Validation Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
