"""Safely update one live external-state projection under an admitted transition."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from pathlib import PureWindowsPath
from typing import Callable, Sequence

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
    _has_reparse_point,
    _resolve_target_path,
    validate_target_historical_receipt,
    validate_target_currentness,
)
from orin_external_state_lock_lifecycle import inspect_lock_table, lock_table_guard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply one audited, target-scoped external-state projection transition."
    )
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--target", required=True, help="One relative external-state record path")
    parser.add_argument(
        "--lock-id",
        default="",
        help="Required with --apply; dry-run projection does not acquire or require a lock.",
    )
    parser.add_argument(
        "--workload-id",
        default="",
        help="Exact caller workload identity; required with --apply.",
    )
    parser.add_argument(
        "--snapshot",
        default="",
        help="Required with --apply; dry-run projection does not create or require a snapshot.",
    )
    parser.add_argument("--expected-branch", required=True)
    parser.add_argument("--expected-source-head", required=True)
    parser.add_argument(
        "--post-expected-source-head",
        help="Expected Source Repo HEAD after this transition; defaults to the pre-write expectation",
    )
    parser.add_argument(
        "--post-expected-origin-main",
        help="Expected origin/main after this transition; defaults to the pre-write expectation",
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
    parser.add_argument(
        "--rename-section",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help="Rename one existing Markdown section heading; repeat for multiple sections",
    )
    parser.add_argument(
        "--retire-as-historical-receipt",
        action="store_true",
        help="Validate the post-state as historical receipt evidence instead of a live projection.",
    )
    parser.add_argument("--apply", action="store_true", help="Apply the atomic transition")
    return parser


def _safe_relative_path(root: Path, raw: str, label: str) -> tuple[Path | None, list[str]]:
    failures: list[str] = []
    windows = PureWindowsPath(raw)
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    candidate = resolve_path(root.joinpath(*parts))
    if (
        not raw
        or Path(raw).is_absolute()
        or windows.is_absolute()
        or windows.drive
        or windows.root
        or any(part == "" for part in parts)
        or any(part in {".", ".."} for part in parts)
        or ("/" in raw and "\\" in raw)
        or normalized.endswith("/")
        or any(":" in part for part in parts)
        or not is_relative_to(candidate, root.resolve())
    ):
        failures.append(f"{label} must remain relative and confined to the external root: {raw!r}")
        return None, failures
    cursor = root.resolve(strict=False)
    for part in parts:
        cursor = cursor / part
        if _has_reparse_point(cursor):
            failures.append(
                f"{label} must not traverse a reparse/symlink component: {raw!r}"
            )
            return None, failures
    return candidate, failures


def _parse_assignments(
    raw_assignments: list[str],
    *,
    required: bool = True,
) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    failures: list[str] = []
    for raw in raw_assignments:
        field, separator, value = raw.partition("=")
        field = field.strip()
        value = value.strip()
        if (
            not separator
            or not field
            or not value
            or "`" in value
            or "\r" in value
            or "\n" in value
        ):
            failures.append(f"Invalid --set-field assignment: {raw!r}")
            continue
        if field in values:
            failures.append(f"Duplicate --set-field assignment: {field}")
            continue
        values[field] = value
    if required and not values:
        failures.append("At least one --set-field assignment is required")
    return values, failures


def _parse_section_renames(raw_renames: list[str]) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    failures: list[str] = []
    for raw in raw_renames:
        old, separator, new = raw.partition("=")
        old = old.strip()
        new = new.strip()
        if (
            not separator
            or not old
            or not new
            or "`" in old
            or "`" in new
            or old in values
        ):
            failures.append(f"Invalid --rename-section assignment: {raw!r}")
            continue
        values[old] = new
    return values, failures


def _parse_intended_write_set(raw: object) -> set[str]:
    """Return exact normalized entries from a semicolon-delimited write set."""

    if isinstance(raw, str):
        values = raw.split(";")
    elif isinstance(raw, (list, tuple, set)):
        values = [str(value) for value in raw]
    else:
        values = []
    return {
        value.strip().replace("\\", "/")
        for value in values
        if value.strip()
    }


def _line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith(("\n", "\r")):
        return line[-1]
    return ""


def _path_compare_key(value: object) -> str:
    """Normalize paths without imposing case-insensitivity on POSIX hosts."""

    return os.path.normcase(os.path.normpath(str(value)))


def _read_text_preserve_newlines(path: Path) -> str:
    """Read UTF-8 text without translating source-record newline bytes."""

    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _lock_failures(
    root: Path,
    lock_id: str,
    target: str,
    expected_branch: str,
    expected_worktree_path: str,
    expected_workload_id: str = "",
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
    lifecycle_matches = [
        inspection
        for inspection in inspect_lock_table(root)
        if inspection.path == lock_path
    ]
    if len(lifecycle_matches) != 1:
        failures.append(
            "Required lock lifecycle classification is unavailable or ambiguous: "
            f"expected one entry, found {len(lifecycle_matches)}"
        )
    elif lifecycle_matches[0].classification != "ACTIVE_VALID":
        failures.append(
            "Required lock lifecycle classification is not ACTIVE_VALID: "
            f"{lifecycle_matches[0].classification}"
        )
    if payload.get("Lock ID") != lock_id:
        failures.append(
            f"Lock payload ID mismatch: expected {lock_id!r}, found {payload.get('Lock ID')!r}"
        )
    if payload.get("Lock State") != "Locked":
        failures.append(f"Required lock is not held: {lock_path}")
    if expected_workload_id and payload.get("Workload ID") != expected_workload_id:
        failures.append(
            "Lock workload mismatch: expected "
            f"{expected_workload_id!r}, found {payload.get('Workload ID')!r}"
        )
    if payload.get("Branch") != expected_branch:
        failures.append(f"Lock branch mismatch: expected {expected_branch!r}, found {payload.get('Branch')!r}")
    lock_worktree = str(payload.get("Worktree", ""))
    accepted_worktree_values = {
        expected_worktree_path,
        PureWindowsPath(expected_worktree_path).name,
    }
    if lock_worktree not in accepted_worktree_values:
        failures.append(
            "Lock worktree mismatch: expected one of "
            f"{sorted(accepted_worktree_values)!r}, found {lock_worktree!r}"
        )
    intended_entries = _parse_intended_write_set(payload.get("Intended Write Set", ""))
    if target.replace("\\", "/") not in intended_entries:
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
    live_end = next(
        (
            index
            for index, line in enumerate(lines)
            if line.rstrip("\r\n").startswith("## ")
        ),
        len(lines),
    )
    for index, line in enumerate(lines[:live_end]):
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
        insert_at = live_end
        newline = next(
            (_line_ending(line) for line in lines[:live_end] if _line_ending(line)),
            "\n",
        )
        additions_text = [f"{field}: `{value}`{newline}" for field, value in additions.items()]
        lines[insert_at:insert_at] = additions_text
    return "".join(lines), failures


def _rename_sections(
    text: str,
    renames: dict[str, str],
) -> tuple[str, list[str], list[tuple[str, str]]]:
    failures: list[str] = []
    renamed: list[tuple[str, str]] = []
    result = text
    for old, new in renames.items():
        old_heading = old if old.startswith("## ") else f"## {old}"
        new_heading = new if new.startswith("## ") else f"## {new}"
        pattern = re.compile(rf"(?m)^{re.escape(old_heading)}[ \t]*(\r\n|\n|\r|$)")
        matches = list(pattern.finditer(result))
        if len(matches) != 1:
            failures.append(
                f"Target transition requires exactly one section {old_heading!r}: found {len(matches)}"
            )
            continue
        destination_pattern = re.compile(rf"(?m)^{re.escape(new_heading)}[ \t]*(\r\n|\n|\r|$)")
        destination_matches = list(destination_pattern.finditer(result))
        if any(match.start() != matches[0].start() for match in destination_matches):
            failures.append(
                f"Target transition section rename destination already exists: {new_heading!r}"
            )
            continue
        result = pattern.sub(lambda match: f"{new_heading}{match.group(1)}", result, count=1)
        renamed.append((old_heading, new_heading))
    return result, failures, renamed


def _projected_target_validation(
    *,
    relative: str,
    projected_text: str,
    expected_branch: str,
    expected_source_head: str,
    expected_origin_main: str,
    expected_worktree_path: str,
    expected_worktree_slot: str,
    post_record_state: str,
) -> list[str]:
    """Validate a dry-run projection without mutating the live external root."""

    with tempfile.TemporaryDirectory(prefix="ndai-target-projection-") as temp_dir:
        projected_root = Path(temp_dir)
        projected_target = projected_root.joinpath(*relative.split("/"))
        projected_target.parent.mkdir(parents=True, exist_ok=True)
        projected_target.write_bytes(projected_text.encode("utf-8"))
        projected_hash = sha256_file(projected_target)
        validation = (
            validate_target_historical_receipt
            if post_record_state == "historical-receipt"
            else validate_target_currentness
        )
        return validation(
            projected_root,
            [relative],
            expected_branch=expected_branch,
            expected_source_head=expected_source_head,
            expected_origin_main=expected_origin_main,
            expected_worktree_path=expected_worktree_path,
            expected_worktree_slot=expected_worktree_slot,
            expected_target_sha256=projected_hash,
        )


def _snapshot_failures(
    *,
    root: Path,
    snapshot_path: Path,
    relative: str,
    expected_target_sha256: str,
    transition_started_ns: int,
    expected_lock_id: str,
    expected_workload_id: str,
) -> list[str]:
    failures: list[str] = []
    manifest_path = snapshot_path / "snapshot_manifest.json"
    if not manifest_path.is_file():
        return [f"Transition Snapshot Contract: snapshot manifest is missing: {manifest_path}"]
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:  # noqa: BLE001 - malformed recovery evidence must block
        return [f"Transition Snapshot Contract: snapshot manifest is unreadable: {exc}"]
    manifest_root = _path_compare_key(manifest.get("Root", ""))
    expected_root = _path_compare_key(root.resolve())
    if manifest_root != expected_root:
        failures.append(
            f"Transition Snapshot Contract: snapshot root mismatch: expected {root}, found {manifest.get('Root', 'MISSING')}"
        )
    manifest_lock_id = str(manifest.get("Lock ID", ""))
    if not expected_lock_id or manifest_lock_id != expected_lock_id:
        failures.append(
            "Transition Snapshot Contract: snapshot lock identity mismatch: "
            f"expected {expected_lock_id or 'MISSING'}, found {manifest_lock_id or 'MISSING'}"
        )
    manifest_workload_id = str(manifest.get("Workload ID", ""))
    if not expected_workload_id or manifest_workload_id != expected_workload_id:
        failures.append(
            "Transition Snapshot Contract: snapshot workload identity mismatch: "
            f"expected {expected_workload_id or 'MISSING'}, found {manifest_workload_id or 'MISSING'}"
        )
    if manifest_path.stat().st_mtime_ns > transition_started_ns:
        failures.append("Transition Snapshot Contract: snapshot was created after the transition began")
    snapshot_target = snapshot_path / Path(*relative.split("/"))
    snapshot_cursor = snapshot_path
    snapshot_target_has_reparse_component = _has_reparse_point(snapshot_cursor)
    for part in relative.split("/"):
        snapshot_cursor = snapshot_cursor / part
        if _has_reparse_point(snapshot_cursor):
            snapshot_target_has_reparse_component = True
            break
    if snapshot_target_has_reparse_component:
        failures.append(
            "Transition Snapshot Contract: snapshot target must be an independent regular file; "
            f"reparse/symlink target is forbidden: {relative}"
        )
    elif not snapshot_target.is_file():
        failures.append(f"Transition Snapshot Contract: snapshot does not contain target: {relative}")
    else:
        if snapshot_target.stat().st_mtime_ns > transition_started_ns:
            failures.append(
                "Transition Snapshot Contract: snapshot target was created after the transition began"
            )
        else:
            snapshot_hash = sha256_file(snapshot_target)
            if snapshot_hash.casefold() != expected_target_sha256.casefold():
                failures.append(
                    f"Transition Snapshot Contract: snapshot target hash mismatch for {relative}: "
                    f"expected {expected_target_sha256}, found {snapshot_hash}"
                )
    copied = manifest.get("Copied Files", [])
    copied_hash = None
    if isinstance(copied, list):
        for entry in copied:
            if isinstance(entry, dict) and str(entry.get("path", "")).replace("\\", "/") == relative:
                copied_hash = str(entry.get("sha256", ""))
                break
    if copied_hash is None:
        failures.append(f"Transition Snapshot Contract: manifest omits target copy: {relative}")
    elif copied_hash.casefold() != expected_target_sha256.casefold():
        failures.append(
            f"Transition Snapshot Contract: manifest target hash mismatch for {relative}: "
            f"expected {expected_target_sha256}, found {copied_hash}"
        )
    return failures


def _before_atomic_replacement_check(_target_path: Path, _expected_hash: str) -> None:
    """Test seam for adversarial mutation between preparation and the final reread."""


def _before_final_lock_check(_root: Path, _lock_id: str) -> None:
    """Test seam for lock mutation immediately before atomic replacement."""


def _before_final_snapshot_check(_snapshot_path: Path) -> None:
    """Test seam for recovery-snapshot mutation before final validation."""


def _live_header_text(text: str) -> str:
    """Restrict audit field lookup to live fields before historical receipts."""

    lines = text.splitlines(keepends=True)
    live_end = next(
        (
            index
            for index, line in enumerate(lines)
            if line.rstrip("\r\n").startswith("## ")
        ),
        len(lines),
    )
    return "".join(lines[:live_end])


def _live_field_value(text: str, field: str) -> str:
    for line in _live_header_text(text).splitlines():
        if re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", line):
            value = re.sub(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", "", line).strip()
            if value.startswith("`") and value.endswith("`"):
                return value[1:-1]
            return value
    return "MISSING"


def _non_updated_lines(text: str, fields: set[str]) -> list[str]:
    result: list[str] = []
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if any(re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", content) for field in fields):
            continue
        result.append(line)
    return result


def _non_updated_lines_with_sections(
    text: str,
    fields: set[str],
    section_headings: set[str],
) -> list[str]:
    result: list[str] = []
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if content in section_headings:
            continue
        if any(re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", content) for field in fields):
            continue
        result.append(line)
    return result


def _publish_single_target(
    *,
    root: Path,
    target: str,
    target_path: Path,
    relative: str,
    lock_id: str,
    expected_branch: str,
    expected_worktree_path: str,
    expected_workload_id: str,
    initial_lock_payload: dict[str, object] | None,
    snapshot_path: Path | None,
    expected_target_sha256: str,
    transition_started_ns: int,
    after_text: str,
    before_text: str,
    before_hash: str,
    post_record_state: str,
    post_source_head: str,
    post_origin_main: str,
    expected_source_head: str,
    expected_worktree_slot: str,
    write_audit: bool,
    changed_fields: set[str],
    updates: dict[str, str],
    additions_map: dict[str, str],
    renamed_sections: list[tuple[str, str]],
    snapshot: str,
) -> tuple[bool, list[str], Path | None]:
    _before_final_lock_check(root, lock_id)
    final_lock_payload, final_lock_failures = _lock_failures(
        root,
        lock_id,
        target,
        expected_branch,
        expected_worktree_path,
        expected_workload_id,
    )
    if final_lock_failures:
        return False, [f"Final lock validation: {item}" for item in final_lock_failures], None
    if final_lock_payload != initial_lock_payload:
        return False, [
            "Lock changed between validation and atomic replacement; no replacement performed"
        ], None
    _before_final_snapshot_check(snapshot_path)
    final_snapshot_failures = _snapshot_failures(
        root=root,
        snapshot_path=snapshot_path,
        relative=relative,
        expected_target_sha256=expected_target_sha256,
        transition_started_ns=transition_started_ns,
        expected_lock_id=lock_id,
        expected_workload_id=str((final_lock_payload or {}).get("Workload ID", "")),
    )
    if final_snapshot_failures:
        return False, [
            f"Final snapshot validation: {item}" for item in final_snapshot_failures
        ], None
    atomic_write_text(target_path, after_text)
    actual_after_hash = sha256_file(target_path)
    post_validation_func = (
        validate_target_historical_receipt
        if post_record_state == "historical-receipt"
        else validate_target_currentness
    )
    post_validation = post_validation_func(
        root,
        [target],
        expected_branch=expected_branch,
        expected_source_head=post_source_head,
        expected_origin_main=post_origin_main,
        expected_worktree_path=expected_worktree_path,
        expected_worktree_slot=expected_worktree_slot,
        expected_target_sha256=actual_after_hash,
    )
    if post_validation:
        atomic_write_text(target_path, before_text)
        return False, [f"Post-write target validation: {item}" for item in post_validation], None

    if not write_audit:
        return True, [
            f"APPLIED: {relative}",
            f"Before SHA256: {before_hash}",
            f"After SHA256: {actual_after_hash}",
            "Audit: deferred to bounded target-set transaction",
        ], None

    audit_path = root / "audit_log" / f"target-currentness-{new_lock_id('audit')}.json"
    changed_field_details = [
        {
            "Field": field,
            "Before": _live_field_value(before_text, field),
            "After": _live_field_value(after_text, field),
        }
        for field in sorted(changed_fields)
    ]
    audit_payload = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Transition": (
            "Target-scoped historical projection retirement"
            if post_record_state == "historical-receipt"
            else "Target-scoped live projection reconciliation"
        ),
        "Post Record State": post_record_state,
        "Target": relative,
        "Lock ID": lock_id,
        "Snapshot": snapshot,
        "Before SHA256": before_hash,
        "After SHA256": actual_after_hash,
        "Changed Fields": sorted(changed_fields),
        "Replaced Fields": sorted(updates),
        "Added Fields": sorted(additions_map),
        "Renamed Sections": [
            {"Before": old, "After": new}
            for old, new in renamed_sections
        ],
        "Changed Field Details": changed_field_details,
        "Source Identity": {
            "Branch": expected_branch,
            "Before Source Repo HEAD": expected_source_head,
            "After Source Repo HEAD": post_source_head,
            "Origin/Main": post_origin_main,
            "Worktree Path": expected_worktree_path,
            "Slot ID": expected_worktree_slot,
        },
        "Branch": expected_branch,
        "Before Source Repo HEAD": expected_source_head,
        "After Source Repo HEAD": post_source_head,
        "Origin/Main": post_origin_main,
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
    section_renames: list[str] | None = None,
    post_expected_source_head: str | None = None,
    post_expected_origin_main: str | None = None,
    write_audit: bool = True,
    post_record_state: str = "live",
    expected_workload_id: str = "",
) -> tuple[bool, list[str], Path | None]:
    root = resolve_path(root)
    transition_started_ns = time.time_ns()
    failures = validate_canonical_root(root)
    failures.extend(validate_initialized_root(root))
    if post_record_state not in {"live", "historical-receipt"}:
        failures.append(f"Unsupported post-record state: {post_record_state!r}")
    if failures:
        return False, failures, None

    section_renames_map, section_rename_failures = _parse_section_renames(section_renames or [])
    updates, assignment_failures = _parse_assignments(
        assignments,
        required=not additions and not section_renames_map,
    )
    additions_map, addition_failures = _parse_assignments(additions) if additions else ({}, [])
    if set(updates) & set(additions_map):
        assignment_failures.append("A field cannot be both --set-field and --add-field: " + ", ".join(sorted(set(updates) & set(additions_map))))
    failures.extend(assignment_failures)
    failures.extend(addition_failures)
    failures.extend(section_rename_failures)
    snapshot_path: Path | None = None
    initial_lock_payload: dict[str, object] | None = None
    if apply and not lock_id:
        failures.append("Applied target reconciliation requires a workload-scoped lock ID")
    if apply and not expected_workload_id:
        failures.append("Applied target reconciliation requires an exact workload ID")
    if apply and not snapshot:
        failures.append("Applied target reconciliation requires a pre-write snapshot")
    if snapshot:
        snapshot_path, snapshot_failures = _safe_relative_path(root, snapshot, "Snapshot path")
        failures.extend(snapshot_failures)
        if snapshot_path is None or not snapshot_path.is_dir():
            failures.append(f"Snapshot directory is missing: {snapshot_path or snapshot}")
    if lock_id:
        initial_lock_payload, lock_failures = _lock_failures(
            root,
            lock_id,
            target,
            expected_branch,
            expected_worktree_path,
            expected_workload_id,
        )
        failures.extend(lock_failures)
    relative, target_path, target_failures = _resolve_target_path(root, target)
    failures.extend(target_failures)
    if target_path is None or relative is None:
        return False, failures, None
    if failures:
        return False, failures, None

    if snapshot_path is not None:
        expected_snapshot_workload_id = str(
            (initial_lock_payload or {}).get("Workload ID", "")
        )
        failures.extend(
            _snapshot_failures(
                root=root,
                snapshot_path=snapshot_path,
                relative=relative,
                expected_target_sha256=expected_target_sha256,
                transition_started_ns=transition_started_ns,
                expected_lock_id=lock_id,
                expected_workload_id=expected_snapshot_workload_id,
            )
        )
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
    addable_identity_fields = set(additions_map)
    allowed_pre_additions = {
        f"{relative} is missing required field {field}"
        for field in addable_identity_fields
    }
    pre_validation = [
        item
        for item in pre_validation
        if not (
            any(item.endswith(allowed) for allowed in allowed_pre_additions)
            or (
                "unsupported or missing live Record Class" in item
                and "Record Class" in addable_identity_fields
            )
            or (
                item.endswith("is missing Record Role classification")
                and "Record Role" in addable_identity_fields
            )
            or (
                item.endswith("is missing Historical Receipt Boundary")
                and "Historical Receipt Boundary" in addable_identity_fields
            )
        )
    ]
    if pre_validation:
        return False, [f"Pre-write target validation: {item}" for item in pre_validation], None

    before_text = _read_text_preserve_newlines(target_path)
    before_hash = sha256_file(target_path)
    if before_hash.casefold() != expected_target_sha256.casefold():
        return False, [
            "Pre-write target bytes changed after validation; no replacement performed: "
            f"expected {expected_target_sha256}, found {before_hash}"
        ], None
    after_text, replacement_failures = _replace_existing_fields(before_text, updates, additions_map)
    if replacement_failures:
        return False, replacement_failures, None
    after_text, section_failures, renamed_sections = _rename_sections(after_text, section_renames_map)
    if section_failures:
        return False, section_failures, None
    changed_fields = set(updates) | set(additions_map)
    allowed_section_lines = {heading for pair in renamed_sections for heading in pair}
    if _non_updated_lines_with_sections(before_text, changed_fields, allowed_section_lines) != _non_updated_lines_with_sections(after_text, changed_fields, allowed_section_lines):
        return False, ["No-loss comparison failed: an unselected target line changed"], None
    after_hash = hashlib.sha256(after_text.encode("utf-8")).hexdigest()

    post_source_head = post_expected_source_head or expected_source_head
    post_origin_main = post_expected_origin_main or expected_origin_main

    if not apply:
        projected_validation = _projected_target_validation(
            relative=relative,
            projected_text=after_text,
            expected_branch=expected_branch,
            expected_source_head=post_source_head,
            expected_origin_main=post_origin_main,
            expected_worktree_path=expected_worktree_path,
            expected_worktree_slot=expected_worktree_slot,
            post_record_state=post_record_state,
        )
        if projected_validation:
            return False, [
                f"Projected post-write target validation: {item}"
                for item in projected_validation
            ], None
        return True, [
            f"READY: {relative}",
            f"Before SHA256: {before_hash}",
            f"After SHA256: {after_hash}",
            "No write performed; omit --apply was honored",
        ], None

    _before_atomic_replacement_check(target_path, before_hash)
    final_before_text = _read_text_preserve_newlines(target_path)
    final_before_hash = sha256_file(target_path)
    if final_before_hash.casefold() != before_hash.casefold() or final_before_text != before_text:
        return False, [
            "Target changed between validation and atomic replacement; no replacement performed: "
            f"expected {before_hash}, found {final_before_hash}"
        ], None
    with lock_table_guard(root):
        return _publish_single_target(
            root=root,
            target=target,
            target_path=target_path,
            relative=relative,
            lock_id=lock_id,
            expected_branch=expected_branch,
            expected_worktree_path=expected_worktree_path,
            expected_workload_id=expected_workload_id,
            initial_lock_payload=initial_lock_payload,
            snapshot_path=snapshot_path,
            expected_target_sha256=expected_target_sha256,
            transition_started_ns=transition_started_ns,
            after_text=after_text,
            before_text=before_text,
            before_hash=before_hash,
            post_record_state=post_record_state,
            post_source_head=post_source_head,
            post_origin_main=post_origin_main,
            expected_source_head=expected_source_head,
            expected_worktree_slot=expected_worktree_slot,
            write_audit=write_audit,
            changed_fields=changed_fields,
            updates=updates,
            additions_map=additions_map,
            renamed_sections=renamed_sections,
            snapshot=snapshot,
        )


@dataclass(frozen=True)
class TargetReconcileRequest:
    """One member of a bounded, all-or-rollback projection-set transaction."""

    target: str
    expected_branch: str
    expected_source_head: str
    expected_origin_main: str
    expected_worktree_path: str
    expected_worktree_slot: str
    expected_target_sha256: str
    assignments: tuple[str, ...]
    additions: tuple[str, ...] = ()
    section_renames: tuple[str, ...] = ()
    post_expected_source_head: str | None = None
    post_expected_origin_main: str | None = None
    post_record_state: str = "live"


def _project_request_text(
    before_text: str,
    request: TargetReconcileRequest,
) -> tuple[str | None, list[str]]:
    renames, failures = _parse_section_renames(list(request.section_renames))
    updates, assignment_failures = _parse_assignments(
        list(request.assignments),
        required=not request.additions and not renames,
    )
    additions, addition_failures = (
        _parse_assignments(list(request.additions)) if request.additions else ({}, [])
    )
    failures.extend(assignment_failures)
    failures.extend(addition_failures)
    overlap = set(updates) & set(additions)
    if overlap:
        failures.append(
            "A field cannot be both --set-field and --add-field: "
            + ", ".join(sorted(overlap))
        )
    if failures:
        return None, failures
    after_text, replacement_failures = _replace_existing_fields(
        before_text,
        updates,
        additions,
    )
    failures.extend(replacement_failures)
    after_text, section_failures, renamed_sections = _rename_sections(after_text, renames)
    failures.extend(section_failures)
    changed_fields = set(updates) | set(additions)
    allowed_section_lines = {heading for pair in renamed_sections for heading in pair}
    if not failures and _non_updated_lines_with_sections(
        before_text,
        changed_fields,
        allowed_section_lines,
    ) != _non_updated_lines_with_sections(
        after_text,
        changed_fields,
        allowed_section_lines,
    ):
        failures.append("No-loss comparison failed: an unselected target line changed")
    return (after_text if not failures else None), failures


def _rollback_target_set(
    *,
    target_states: Sequence[tuple[Path, str, str]],
    audit_path: Path | None,
) -> list[str]:
    failures: list[str] = []
    for target_path, before_text, applied_hash in reversed(target_states):
        try:
            current_hash = sha256_file(target_path)
        except OSError as exc:
            failures.append(f"Target-set rollback could not read {target_path}: {exc}")
            continue
        if current_hash.casefold() != applied_hash.casefold():
            failures.append(
                "Target-set rollback refused to overwrite drifted target "
                f"{target_path}: expected {applied_hash}, found {current_hash}"
            )
            continue
        try:
            atomic_write_text(target_path, before_text)
        except Exception as exc:  # noqa: BLE001 - rollback must report restore failure
            failures.append(f"Target-set rollback failed for {target_path}: {exc}")
            continue
        expected_before_hash = hashlib.sha256(before_text.encode("utf-8")).hexdigest()
        actual_before_hash = sha256_file(target_path)
        if actual_before_hash.casefold() != expected_before_hash.casefold():
            failures.append(
                f"Target-set rollback verification failed for {target_path}: "
                f"expected {expected_before_hash}, found {actual_before_hash}"
            )
    if not failures and audit_path is not None and audit_path.exists():
        try:
            audit_path.unlink()
        except Exception as exc:  # noqa: BLE001 - rollback must report cleanup failure
            failures.append(f"Target-set rollback could not remove audit {audit_path}: {exc}")
    return failures


def _after_target_set_member_publish(_relative: str, _target_path: Path) -> None:
    """Test seam for abrupt termination after one set member is published."""


def _recover_prepared_target_set_journal(
    *,
    root: Path,
    audit_path: Path,
    audit_target: str,
    lock_id: str,
    workload_id: str,
    requests: Sequence[TargetReconcileRequest],
    apply: bool,
) -> list[str] | None:
    if not audit_path.is_file():
        return None
    try:
        journal = load_json(audit_path)
    except Exception:
        return None
    if (
        journal.get("Transition") != "Bounded coherent target-set reconciliation"
        or journal.get("Transaction State") != "Prepared"
    ):
        return None
    if not apply or not lock_id or not workload_id or not requests:
        return [
            "Incomplete target-set transaction journal requires an applied, locked recovery workload"
        ]
    if journal.get("Workload ID") != workload_id:
        return [
            "Incomplete target-set transaction journal workload differs from the requested "
            f"recovery workload: expected {workload_id!r}, "
            f"found {journal.get('Workload ID')!r}"
        ]
    rows = journal.get("Targets")
    if not isinstance(rows, list) or not rows:
        return ["Incomplete target-set transaction journal has no recoverable target rows"]
    journal_targets: list[str] = []
    journal_paths: dict[str, Path] = {}
    for row in rows:
        if not isinstance(row, dict):
            return ["Incomplete target-set journal contains a malformed recovery row"]
        relative, target_path, target_failures = _resolve_target_path(
            root,
            str(row.get("Target", "")),
        )
        if target_failures or relative is None or target_path is None:
            return [
                f"Incomplete target-set recovery target: {item}"
                for item in target_failures
            ]
        journal_targets.append(relative)
        journal_paths[relative] = target_path
    requested_targets = [request.target.replace("\\", "/") for request in requests]
    if journal_targets != requested_targets:
        return [
            "Incomplete target-set transaction journal target set differs from the requested recovery set"
        ]
    for row, request in zip(rows, requests, strict=True):
        if str(row.get("Before SHA256", "")).casefold() != (
            request.expected_target_sha256.casefold()
        ):
            return [
                "Incomplete target-set transaction journal pre-state differs from the requested "
                f"recovery contract: {request.target}"
            ]
    first_request = requests[0]
    with lock_table_guard(root):
        try:
            authoritative = load_json(audit_path)
        except Exception as exc:
            return [f"Incomplete target-set journal authoritative reread failed: {exc}"]
        if authoritative != journal:
            return ["Incomplete target-set transaction journal changed during recovery preflight"]
        lock_payload, lock_failures = _lock_failures(
            root,
            lock_id,
            journal_targets[0],
            first_request.expected_branch,
            first_request.expected_worktree_path,
            workload_id,
        )
        if lock_failures or lock_payload is None:
            return [f"Recovery lock validation: {item}" for item in lock_failures]
        admitted = _parse_intended_write_set(lock_payload.get("Intended Write Set", ""))
        required = set(journal_targets) | {audit_target.replace("\\", "/")}
        missing = sorted(required - admitted)
        if missing:
            return [
                "Recovery lock write set omits incomplete transaction targets: "
                + ", ".join(missing)
            ]
        restore_rows: list[tuple[Path, str, str, str]] = []
        for row in rows:
            relative = str(row.get("Target", "")).replace("\\", "/")
            target_path = journal_paths[relative]
            before_text = row.get("Before Text")
            before_hash = str(row.get("Before SHA256", ""))
            after_hash = str(row.get("After SHA256", ""))
            if not isinstance(before_text, str) or not before_hash or not after_hash:
                return [f"Incomplete target-set journal row is not recoverable: {relative}"]
            embedded_before_hash = hashlib.sha256(before_text.encode("utf-8")).hexdigest()
            if embedded_before_hash.casefold() != before_hash.casefold():
                return [
                    "Incomplete target-set recovery refused corrupt embedded pre-state "
                    f"for {relative}: expected {before_hash}, found {embedded_before_hash}"
                ]
            try:
                current_hash = sha256_file(target_path)
            except OSError as exc:
                return [f"Incomplete target-set recovery could not read {relative}: {exc}"]
            if current_hash.casefold() not in {before_hash.casefold(), after_hash.casefold()}:
                return [
                    "Incomplete target-set recovery refused drifted target "
                    f"{relative}: found {current_hash}"
                ]
            restore_rows.append((target_path, before_text, before_hash, current_hash))
        for target_path, before_text, before_hash, current_hash in restore_rows:
            if current_hash.casefold() != before_hash.casefold():
                try:
                    atomic_write_text(target_path, before_text)
                except Exception as exc:  # noqa: BLE001 - retain journal for retry
                    return [f"Incomplete target-set recovery write failed: {target_path}: {exc}"]
            try:
                restored_hash = sha256_file(target_path)
            except OSError as exc:
                return [f"Incomplete target-set recovery verification read failed: {target_path}: {exc}"]
            if restored_hash.casefold() != before_hash.casefold():
                return [f"Incomplete target-set recovery verification failed: {target_path}"]
        try:
            audit_path.unlink()
        except OSError as exc:
            return [f"Incomplete target-set recovery could not remove its journal: {exc}"]
    return [
        "Recovered incomplete target-set transaction and removed its prepared journal",
        "Rerun required after recovery preflight",
    ]


def _apply_target_set(
    *,
    root: Path,
    lock_id: str,
    workload_id: str,
    snapshot: str,
    audit_path: Path,
    resolved: Sequence[tuple[TargetReconcileRequest, str, Path, str, str]],
    lock_payload: dict[str, object],
    final_validation: Callable[[Path], list[str]],
) -> tuple[bool, list[str], Path | None]:
    if audit_path.exists():
        return False, [f"Target-set audit path already exists: {audit_path}"], None
    first_request, first_relative, _first_path, _first_before, _first_after = resolved[0]
    final_lock_payload, final_lock_failures = _lock_failures(
        root,
        lock_id,
        first_relative,
        first_request.expected_branch,
        first_request.expected_worktree_path,
        workload_id,
    )
    if final_lock_failures or final_lock_payload != lock_payload:
        details = final_lock_failures or [
            "authoritative lock payload changed before target-set publication"
        ]
        return False, [f"Target-set final lock validation: {item}" for item in details], None
    journal_payload = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Transition": "Bounded coherent target-set reconciliation",
        "Transaction State": "Prepared",
        "Lock ID": lock_id,
        "Workload ID": lock_payload.get("Workload ID", "MISSING"),
        "Snapshot": snapshot,
        "Targets": [
            {
                "Target": relative,
                "Before SHA256": request.expected_target_sha256,
                "Before Text": before_text,
                "After SHA256": hashlib.sha256(projected_text.encode("utf-8")).hexdigest(),
            }
            for request, relative, _target_path, before_text, projected_text in resolved
        ],
        "Last Updated": utc_now(),
        "Last Updated By": lock_payload.get("Last Updated By", "Codex"),
    }
    try:
        atomic_write_json(audit_path, journal_payload)
        if load_json(audit_path) != journal_payload:
            raise ValueError("prepared target-set journal authoritative reread mismatch")
    except Exception as exc:
        cleanup_failure = ""
        if audit_path.exists():
            try:
                audit_path.unlink()
            except OSError as cleanup_exc:
                cleanup_failure = f"; incomplete journal cleanup failed: {cleanup_exc}"
        return False, [
            f"Target-set journal preparation failed before publication: {exc}{cleanup_failure}"
        ], None

    applied_states: list[tuple[Path, str, str]] = []
    messages: list[str] = []
    for request, relative, target_path, before_text, _projected_text in resolved:
        ok, target_messages, _ = reconcile_target(
            root=root,
            target=relative,
            lock_id=lock_id,
            snapshot=snapshot,
            expected_branch=request.expected_branch,
            expected_source_head=request.expected_source_head,
            expected_origin_main=request.expected_origin_main,
            expected_worktree_path=request.expected_worktree_path,
            expected_worktree_slot=request.expected_worktree_slot,
            expected_target_sha256=request.expected_target_sha256,
            assignments=list(request.assignments),
            additions=list(request.additions),
            section_renames=list(request.section_renames),
            post_expected_source_head=request.post_expected_source_head,
            post_expected_origin_main=request.post_expected_origin_main,
            post_record_state=request.post_record_state,
            apply=True,
            write_audit=False,
            expected_workload_id=workload_id,
        )
        if not ok:
            rollback_failures = _rollback_target_set(
                target_states=applied_states,
                audit_path=audit_path,
            )
            rollback_messages = (
                ["Target-set rollback: PASS - all applied projections restored"]
                if not rollback_failures
                else [f"Target-set rollback: {item}" for item in rollback_failures]
            )
            return False, [
                *messages,
                *(f"{relative}: {item}" for item in target_messages),
                *rollback_messages,
            ], None
        applied_hash = sha256_file(target_path)
        applied_states.append((target_path, before_text, applied_hash))
        messages.extend(f"{relative}: {item}" for item in target_messages)
        _after_target_set_member_publish(relative, target_path)

    try:
        final_failures = final_validation(root)
    except Exception as exc:  # noqa: BLE001 - raised validation must use the same rollback path
        rollback_failures = _rollback_target_set(
            target_states=applied_states,
            audit_path=audit_path,
        )
        rollback_messages = (
            ["Target-set rollback: PASS - all applied projections restored"]
            if not rollback_failures
            else [f"Target-set rollback: {item}" for item in rollback_failures]
        )
        return False, [
            f"Target-set final validation raised: {exc}",
            *rollback_messages,
        ], None
    if final_failures:
        rollback_failures = _rollback_target_set(
            target_states=applied_states,
            audit_path=audit_path,
        )
        rollback_messages = (
            ["Target-set rollback: PASS - all applied projections restored"]
            if not rollback_failures
            else [f"Target-set rollback: {item}" for item in rollback_failures]
        )
        return False, [
            *(f"Target-set final validation: {item}" for item in final_failures),
            *rollback_messages,
        ], None

    audit_payload = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Transition": "Bounded coherent target-set reconciliation",
        "Transaction State": "Committed",
        "Lock ID": lock_id,
        "Workload ID": lock_payload.get("Workload ID", "MISSING"),
        "Snapshot": snapshot,
        "Targets": [
            {
                "Target": relative,
                "Before SHA256": request.expected_target_sha256,
                "After SHA256": sha256_file(target_path),
                "Assignments": list(request.assignments),
                "Additions": list(request.additions),
                "Section Renames": list(request.section_renames),
                "Post Record State": request.post_record_state,
            }
            for request, relative, target_path, _before_text, _projected_text in resolved
        ],
        "Last Updated": utc_now(),
        "Last Updated By": lock_payload.get("Last Updated By", "Codex"),
    }
    try:
        atomic_write_json(audit_path, audit_payload)
        authoritative_audit = load_json(audit_path)
        if authoritative_audit != audit_payload:
            raise ValueError("authoritative target-set committed audit reread mismatch")
        final_failures = final_validation(root)
        for target_path, _before_text, applied_hash in applied_states:
            if sha256_file(target_path).casefold() != applied_hash.casefold():
                final_failures.append(
                    f"target changed after set publication validation: {target_path}"
                )
        if final_failures:
            raise ValueError("; ".join(final_failures))
    except Exception as exc:  # noqa: BLE001 - the set must roll back on any final failure
        journal_restore_failure = ""
        try:
            atomic_write_json(audit_path, journal_payload)
        except Exception as journal_exc:  # noqa: BLE001 - preserve both failure causes
            journal_restore_failure = (
                f"Target-set rollback could not restore its prepared journal: {journal_exc}"
            )
        rollback_failures = _rollback_target_set(
            target_states=applied_states,
            audit_path=audit_path,
        )
        if journal_restore_failure:
            rollback_failures.insert(0, journal_restore_failure)
        rollback_messages = (
            ["Target-set rollback: PASS - all applied projections and audit restored"]
            if not rollback_failures
            else [f"Target-set rollback: {item}" for item in rollback_failures]
        )
        return False, [
            f"Target-set final publication failed: {exc}",
            *rollback_messages,
        ], None
    return True, [
        "APPLIED: coherent target-set publication validated",
        *messages,
        f"Audit: {audit_path}",
    ], audit_path


def reconcile_target_set(
    *,
    root: Path,
    lock_id: str,
    snapshot: str,
    audit_target: str,
    requests: Sequence[TargetReconcileRequest],
    final_validation: Callable[[Path], list[str]],
    apply: bool,
    workload_id: str = "",
) -> tuple[bool, list[str], Path | None]:
    """Publish a coherent projection set or restore every member.

    Dry-run compilation needs neither a lock nor a snapshot. Applied publication
    requires one lock whose exact write set contains every projection and the
    deterministic set-level audit target.
    """

    root = resolve_path(root)
    failures = validate_canonical_root(root)
    failures.extend(validate_initialized_root(root))
    if not requests:
        failures.append("Target-set reconciliation requires at least one target")
    audit_path, audit_path_failures = _safe_relative_path(
        root,
        audit_target,
        "Target-set audit path",
    )
    failures.extend(audit_path_failures)
    if audit_path is not None:
        try:
            audit_relative = audit_path.relative_to(root)
        except ValueError:
            failures.append("Target-set audit path must remain below the external-state root")
        else:
            if (
                len(audit_relative.parts) != 2
                or audit_relative.parts[0] != "audit_log"
                or audit_relative.suffix != ".json"
            ):
                failures.append(
                    "Target-set audit path must be a direct audit_log/*.json journal"
                )
    if not failures and audit_path is not None:
        recovery_messages = _recover_prepared_target_set_journal(
            root=root,
            audit_path=audit_path,
            audit_target=audit_target,
            lock_id=lock_id,
            workload_id=workload_id,
            requests=requests,
            apply=apply,
        )
        if recovery_messages is not None:
            return False, recovery_messages, None
    resolved: list[tuple[TargetReconcileRequest, str, Path, str, str]] = []
    normalized_targets: set[str] = set()
    for request in requests:
        relative, target_path, target_failures = _resolve_target_path(root, request.target)
        failures.extend(target_failures)
        if relative is None or target_path is None:
            continue
        key = relative.casefold()
        if key in normalized_targets:
            failures.append(f"Target-set reconciliation contains duplicate target: {relative}")
            continue
        normalized_targets.add(key)
        try:
            before_text = _read_text_preserve_newlines(target_path)
            before_hash = sha256_file(target_path)
        except OSError as exc:
            failures.append(f"Target-set reconciliation cannot read {relative}: {exc}")
            continue
        if before_hash.casefold() != request.expected_target_sha256.casefold():
            failures.append(
                f"Target-set pre-write hash mismatch for {relative}: expected "
                f"{request.expected_target_sha256}, found {before_hash}"
            )
        projected_text, projection_failures = _project_request_text(before_text, request)
        failures.extend(f"{relative}: {item}" for item in projection_failures)
        if projected_text is not None:
            resolved.append((request, relative, target_path, before_text, projected_text))
    if audit_path is not None and str(audit_path).casefold() in {
        str(item[2]).casefold() for item in resolved
    }:
        failures.append("Target-set audit path aliases a projection target")
    if failures or audit_path is None or len(resolved) != len(requests):
        return False, failures, None

    with tempfile.TemporaryDirectory(prefix="ndai-target-set-projection-") as temp_dir:
        projected_root = Path(temp_dir)
        for _request, relative, _target_path, _before_text, projected_text in resolved:
            projected_path = projected_root.joinpath(*relative.split("/"))
            projected_path.parent.mkdir(parents=True, exist_ok=True)
            projected_path.write_text(projected_text, encoding="utf-8", newline="")
        projected_failures = final_validation(projected_root)
    if projected_failures:
        return False, [
            f"Projected target-set final validation: {item}"
            for item in projected_failures
        ], None

    dry_run_messages: list[str] = []
    for request, relative, _target_path, _before_text, _projected_text in resolved:
        ok, messages, _ = reconcile_target(
            root=root,
            target=relative,
            lock_id="",
            snapshot="",
            expected_branch=request.expected_branch,
            expected_source_head=request.expected_source_head,
            expected_origin_main=request.expected_origin_main,
            expected_worktree_path=request.expected_worktree_path,
            expected_worktree_slot=request.expected_worktree_slot,
            expected_target_sha256=request.expected_target_sha256,
            assignments=list(request.assignments),
            additions=list(request.additions),
            section_renames=list(request.section_renames),
            post_expected_source_head=request.post_expected_source_head,
            post_expected_origin_main=request.post_expected_origin_main,
            post_record_state=request.post_record_state,
            apply=False,
        )
        if not ok:
            return False, [f"{relative}: {item}" for item in messages], None
        dry_run_messages.extend(f"{relative}: {item}" for item in messages)
    if not apply:
        return True, [
            "READY: coherent target-set draft validated without lock acquisition",
            *dry_run_messages,
        ], None

    if not lock_id:
        return False, ["Applied target-set reconciliation requires a workload-scoped lock ID"], None
    if not workload_id:
        return False, ["Applied target-set reconciliation requires an exact workload ID"], None
    if not snapshot:
        return False, ["Applied target-set reconciliation requires a pre-write snapshot"], None
    lock_payload, lock_failures = _lock_failures(
        root,
        lock_id,
        resolved[0][1],
        resolved[0][0].expected_branch,
        resolved[0][0].expected_worktree_path,
        workload_id,
    )
    if lock_failures or lock_payload is None:
        return False, lock_failures, None
    admitted = _parse_intended_write_set(lock_payload.get("Intended Write Set", ""))
    required_write_set = {item[1] for item in resolved} | {
        audit_target.replace("\\", "/"),
        snapshot.replace("\\", "/"),
    }
    missing_targets = sorted(required_write_set - admitted)
    if missing_targets:
        return False, [
            "Target-set lock write set omits exact transaction targets: "
            + ", ".join(missing_targets)
        ], None
    if audit_path.exists():
        return False, [f"Target-set audit path already exists: {audit_path}"], None

    with lock_table_guard(root):
        return _apply_target_set(
            root=root,
            lock_id=lock_id,
            workload_id=workload_id,
            snapshot=snapshot,
            audit_path=audit_path,
            resolved=resolved,
            lock_payload=lock_payload,
            final_validation=final_validation,
        )


def main() -> int:
    args = build_parser().parse_args()
    ok, messages, _ = reconcile_target(
        root=Path(args.root),
        target=args.target,
        lock_id=args.lock_id,
        expected_workload_id=args.workload_id,
        snapshot=args.snapshot,
        expected_branch=args.expected_branch,
        expected_source_head=args.expected_source_head,
        post_expected_source_head=args.post_expected_source_head,
        post_expected_origin_main=args.post_expected_origin_main,
        expected_origin_main=args.expected_origin_main,
        expected_worktree_path=args.expected_worktree_path,
        expected_worktree_slot=args.expected_worktree_slot,
        expected_target_sha256=args.expected_target_sha256,
        assignments=args.set_field,
        additions=args.add_field,
        section_renames=args.rename_section,
        post_record_state=(
            "historical-receipt" if args.retire_as_historical_receipt else "live"
        ),
        apply=args.apply,
    )
    print("External State Target Reconciliation")
    for message in messages:
        print(message)
    print(f"Transition Result: {'PASS' if ok else 'BLOCKED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
