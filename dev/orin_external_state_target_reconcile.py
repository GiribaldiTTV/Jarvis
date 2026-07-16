"""Safely update one live external-state projection under an admitted transition."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from pathlib import PureWindowsPath

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    atomic_write_json,
    atomic_write_text,
    is_relative_to,
    load_json,
    new_lock_id,
    resolve_path,
    sha256_file,
    utc_now,
    validate_canonical_root,
    validate_initialized_root,
)
from orin_external_state_validation import (
    _resolve_target_path,
    validate_target_currentness,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply one audited, target-scoped external-state projection transition."
    )
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--target", required=True, help="One relative external-state record path")
    parser.add_argument("--lock-id", required=True)
    parser.add_argument("--snapshot", required=True, help="Snapshot directory relative to the external root")
    parser.add_argument("--expected-branch", required=True)
    parser.add_argument("--expected-source-head", required=True)
    parser.add_argument(
        "--post-expected-source-head",
        help="Expected Source Repo HEAD after this transition; defaults to the pre-write expectation",
    )
    parser.add_argument("--expected-origin-main", required=True)
    parser.add_argument("--expected-worktree-path", required=True)
    parser.add_argument("--expected-worktree-slot", required=True)
    parser.add_argument("--expected-target-sha256", required=True)
    parser.add_argument(
        "--set-field",
        action="append",
        default=[],
        metavar="FIELD=VALUE",
        help="Replace an existing top-level Markdown field; repeat for multiple fields",
    )
    parser.add_argument(
        "--add-field",
        action="append",
        default=[],
        metavar="FIELD=VALUE",
        help="Add one missing top-level Markdown field; repeat for multiple fields",
    )
    parser.add_argument("--apply", action="store_true", help="Apply the atomic transition")
    return parser


def _safe_relative_path(root: Path, raw: str, label: str) -> tuple[Path | None, list[str]]:
    failures: list[str] = []
    windows = PureWindowsPath(raw)
    candidate = resolve_path(root / raw)
    parts = [part for part in raw.replace("\\", "/").split("/") if part]
    if (
        not raw
        or Path(raw).is_absolute()
        or windows.is_absolute()
        or windows.drive
        or windows.root
        or any(part in {".", ".."} for part in parts)
        or not is_relative_to(candidate, root.resolve())
    ):
        failures.append(f"{label} must remain relative and confined to the external root: {raw!r}")
        return None, failures
    return candidate, failures


def _parse_assignments(raw_assignments: list[str]) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    failures: list[str] = []
    for raw in raw_assignments:
        field, separator, value = raw.partition("=")
        field = field.strip()
        value = value.strip()
        if not separator or not field or not value or "`" in value:
            failures.append(f"Invalid --set-field assignment: {raw!r}")
            continue
        if field in values:
            failures.append(f"Duplicate --set-field assignment: {field}")
            continue
        values[field] = value
    if not values:
        failures.append("At least one --set-field assignment is required")
    return values, failures


def _lock_failures(
    root: Path,
    lock_id: str,
    target: str,
    expected_branch: str,
    expected_worktree_path: str,
) -> tuple[dict[str, object] | None, list[str]]:
    failures: list[str] = []
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", lock_id):
        return None, [f"Lock ID is not a safe filename: {lock_id!r}"]
    lock_path = root / "locks" / f"{lock_id}.json"
    if not lock_path.is_file():
        return None, [f"Required lock is missing: {lock_path}"]
    try:
        payload = load_json(lock_path)
    except Exception as exc:  # noqa: BLE001 - corrupt operational state is a blocking result
        return None, [f"Required lock is unreadable: {lock_path}: {exc}"]
    if payload.get("Lock State") != "Locked":
        failures.append(f"Required lock is not held: {lock_path}")
    if payload.get("Branch") != expected_branch:
        failures.append(f"Lock branch mismatch: expected {expected_branch!r}, found {payload.get('Branch')!r}")
    if payload.get("Worktree") != expected_worktree_path:
        failures.append(
            f"Lock worktree mismatch: expected {expected_worktree_path!r}, found {payload.get('Worktree')!r}"
        )
    intended = str(payload.get("Intended Write Set", ""))
    target_parts = target.rstrip("/").rsplit("/", 1)
    compound_target_allowed = (
        len(target_parts) == 2
        and target_parts[0] in intended
        and target_parts[1] in intended
    )
    if target not in intended and "Governance projection" not in intended and not compound_target_allowed:
        failures.append(f"Lock write set does not admit target projection: {target}")
    return payload, failures


def _replace_existing_fields(
    text: str,
    updates: dict[str, str],
    additions: dict[str, str],
) -> tuple[str, list[str]]:
    lines = text.splitlines(keepends=True)
    failures: list[str] = []
    found: dict[str, int] = {field: 0 for field in {**updates, **additions}}
    replaced: list[str] = []
    header_end = next(
        (index for index, line in enumerate(lines) if line.rstrip("\r\n").startswith("## ")),
        len(lines),
    )
    for index, line in enumerate(lines[:header_end]):
        content = line.rstrip("\r\n")
        newline = line[len(content) :]
        replacement = None
        for field in additions:
            if re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", content):
                found[field] += 1
        for field, value in updates.items():
            match = re.match(rf"^(\s*(?:-\s*)?{re.escape(field)}:\s*).*$", content)
            if not match:
                continue
            found[field] += 1
            replacement = f"{match.group(1)}`{value}`{newline}"
            replaced.append(field)
            break
        if replacement is not None:
            lines[index] = replacement
    for field, count in found.items():
        if field in additions and count != 0:
            failures.append(f"Target transition add-field already exists: {field}")
        elif field in updates and count != 1:
            failures.append(f"Target transition requires exactly one existing field {field}: found {count}")
    if not failures and additions:
        insert_at = next(
            (index for index, line in enumerate(lines) if line.startswith("## ")),
            len(lines),
        )
        additions_text = [f"{field}: `{value}`\n" for field, value in additions.items()]
        lines[insert_at:insert_at] = additions_text
    return "".join(lines), failures


def _non_updated_lines(text: str, fields: set[str]) -> list[str]:
    result: list[str] = []
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if any(re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", content) for field in fields):
            continue
        result.append(line)
    return result


def reconcile_target(
    *,
    root: Path,
    target: str,
    lock_id: str,
    snapshot: str,
    expected_branch: str,
    expected_source_head: str,
    expected_origin_main: str,
    expected_worktree_path: str,
    expected_worktree_slot: str,
    expected_target_sha256: str,
    assignments: list[str],
    additions: list[str],
    apply: bool,
    post_expected_source_head: str | None = None,
) -> tuple[bool, list[str], Path | None]:
    root = resolve_path(root)
    failures = validate_canonical_root(root)
    failures.extend(validate_initialized_root(root))
    if failures:
        return False, failures, None

    updates, assignment_failures = _parse_assignments(assignments)
    additions_map, addition_failures = _parse_assignments(additions) if additions else ({}, [])
    if set(updates) & set(additions_map):
        assignment_failures.append("A field cannot be both --set-field and --add-field: " + ", ".join(sorted(set(updates) & set(additions_map))))
    failures.extend(assignment_failures)
    failures.extend(addition_failures)
    snapshot_path, snapshot_failures = _safe_relative_path(root, snapshot, "Snapshot path")
    failures.extend(snapshot_failures)
    if snapshot_path is None or not snapshot_path.is_dir():
        failures.append(f"Snapshot directory is missing: {snapshot_path or snapshot}")
    _, lock_failures = _lock_failures(
        root, lock_id, target, expected_branch, expected_worktree_path
    )
    failures.extend(lock_failures)
    relative, target_path, target_failures = _resolve_target_path(root, target)
    failures.extend(target_failures)
    if target_path is None or relative is None:
        return False, failures, None
    if failures:
        return False, failures, None

    pre_validation = validate_target_currentness(
        root,
        [target],
        expected_branch=expected_branch,
        expected_source_head=expected_source_head,
        expected_origin_main=expected_origin_main,
        expected_worktree_path=expected_worktree_path,
        expected_worktree_slot=expected_worktree_slot,
        expected_target_sha256=expected_target_sha256,
    )
    allowed_pre_additions = {
        f"{relative} is missing required field {field}"
        for field in additions_map
    }
    pre_validation = [
        item
        for item in pre_validation
        if not any(item.endswith(allowed) for allowed in allowed_pre_additions)
    ]
    if pre_validation:
        return False, [f"Pre-write target validation: {item}" for item in pre_validation], None

    before_text = target_path.read_text(encoding="utf-8")
    after_text, replacement_failures = _replace_existing_fields(before_text, updates, additions_map)
    if replacement_failures:
        return False, replacement_failures, None
    changed_fields = set(updates) | set(additions_map)
    if _non_updated_lines(before_text, changed_fields) != _non_updated_lines(after_text, changed_fields):
        return False, ["No-loss comparison failed: an unselected target line changed"], None
    before_hash = sha256_file(target_path)
    after_hash = hashlib.sha256(after_text.encode("utf-8")).hexdigest()

    if not apply:
        return True, [
            f"READY: {relative}",
            f"Before SHA256: {before_hash}",
            f"After SHA256: {after_hash}",
            "No write performed; omit --apply was honored",
        ], None

    atomic_write_text(target_path, after_text)
    actual_after_hash = sha256_file(target_path)
    post_source_head = post_expected_source_head or expected_source_head
    post_validation = validate_target_currentness(
        root,
        [target],
        expected_branch=expected_branch,
        expected_source_head=post_source_head,
        expected_origin_main=expected_origin_main,
        expected_worktree_path=expected_worktree_path,
        expected_worktree_slot=expected_worktree_slot,
        expected_target_sha256=actual_after_hash,
    )
    if post_validation:
        atomic_write_text(target_path, before_text)
        return False, [f"Post-write target validation: {item}" for item in post_validation], None

    audit_path = root / "audit_log" / f"target-currentness-{new_lock_id('audit')}.json"
    audit_payload = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Transition": "Target-scoped live projection reconciliation",
        "Target": relative,
        "Lock ID": lock_id,
        "Snapshot": snapshot,
        "Before SHA256": before_hash,
        "After SHA256": actual_after_hash,
        "Changed Fields": sorted(updates),
        "Branch": expected_branch,
        "Before Source Repo HEAD": expected_source_head,
        "After Source Repo HEAD": post_source_head,
        "Origin/Main": expected_origin_main,
        "Worktree Path": expected_worktree_path,
        "Slot ID": expected_worktree_slot,
        "Last Updated": utc_now(),
        "Last Updated By": "Codex",
    }
    try:
        atomic_write_json(audit_path, audit_payload)
    except Exception as exc:  # noqa: BLE001 - no silent unaudited transition
        atomic_write_text(target_path, before_text)
        return False, [f"Audit entry write failed; target rolled back: {exc}"], None
    return True, [
        f"APPLIED: {relative}",
        f"Before SHA256: {before_hash}",
        f"After SHA256: {actual_after_hash}",
        f"Audit: {audit_path}",
    ], audit_path


def main() -> int:
    args = build_parser().parse_args()
    ok, messages, _ = reconcile_target(
        root=Path(args.root),
        target=args.target,
        lock_id=args.lock_id,
        snapshot=args.snapshot,
        expected_branch=args.expected_branch,
        expected_source_head=args.expected_source_head,
        post_expected_source_head=args.post_expected_source_head,
        expected_origin_main=args.expected_origin_main,
        expected_worktree_path=args.expected_worktree_path,
        expected_worktree_slot=args.expected_worktree_slot,
        expected_target_sha256=args.expected_target_sha256,
        assignments=args.set_field,
        additions=args.add_field,
        apply=args.apply,
    )
    print("External State Target Reconciliation")
    for message in messages:
        print(message)
    print(f"Transition Result: {'PASS' if ok else 'BLOCKED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
