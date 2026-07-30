"""Safely update one live external-state projection under an admitted transition."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import time
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
    _has_reparse_point,
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
        "--set-section-field",
        action="append",
        default=[],
        metavar="SECTION::FIELD=VALUE",
        help=(
            "Replace one existing field inside one exact level-two Markdown section; "
            "repeat for multiple fields"
        ),
    )
    parser.add_argument(
        "--rename-section",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help="Rename one existing Markdown section heading; repeat for multiple sections",
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


def _parse_section_assignments(
    raw_assignments: list[str],
) -> tuple[dict[tuple[str, str], str], list[str]]:
    values: dict[tuple[str, str], str] = {}
    normalized_keys: set[tuple[str, str]] = set()
    failures: list[str] = []
    for raw in raw_assignments:
        selector, equals, value = raw.partition("=")
        section, separator, field = selector.partition("::")
        section = section.strip()
        field = field.strip()
        value = value.strip()
        key = (section, field)
        normalized_key = (section.casefold(), field.casefold())
        if (
            not equals
            or not separator
            or not section
            or not field
            or not value
            or section.startswith("#")
            or "`" in section
            or "`" in field
            or "`" in value
            or "\r" in raw
            or "\n" in raw
            or normalized_key in normalized_keys
        ):
            failures.append(f"Invalid --set-section-field assignment: {raw!r}")
            continue
        values[key] = value
        normalized_keys.add(normalized_key)
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


def _markdown_fence_states(lines: list[str]) -> list[bool]:
    """Mark fenced code-block lines so examples cannot become live selectors."""

    states: list[bool] = []
    active_marker = ""
    active_length = 0
    for line in lines:
        content = line.rstrip("\r\n")
        marker_match = re.match(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$", content)
        if active_marker:
            states.append(True)
            if (
                marker_match
                and marker_match.group(1)[0] == active_marker
                and len(marker_match.group(1)) >= active_length
                and not marker_match.group(2).strip()
            ):
                active_marker = ""
                active_length = 0
            continue
        if marker_match:
            marker = marker_match.group(1)
            active_marker = marker[0]
            active_length = len(marker)
            states.append(True)
            continue
        states.append(False)
    return states


def _is_level_two_heading(content: str) -> bool:
    return re.match(r"^##[ \t]+", content) is not None


def _markdown_fences_are_balanced(lines: list[str]) -> bool:
    return not _markdown_fence_states([*lines, "NDAI fence-balance sentinel"])[-1]


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
    if payload.get("Lock ID") != lock_id:
        failures.append(
            f"Lock payload ID mismatch: expected {lock_id!r}, found {payload.get('Lock ID')!r}"
        )
    if payload.get("Lock State") != "Locked":
        failures.append(f"Required lock is not held: {lock_path}")
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
    fenced = _markdown_fence_states(lines)
    failures: list[str] = []
    if not _markdown_fences_are_balanced(lines):
        return text, ["Target transition Markdown contains an unterminated fenced block"]
    found: dict[str, int] = {field: 0 for field in {**updates, **additions}}
    replaced: list[str] = []
    live_end = next(
        (
            index
            for index, line in enumerate(lines)
            if not fenced[index] and _is_level_two_heading(line.rstrip("\r\n"))
        ),
        len(lines),
    )
    for index, line in enumerate(lines[:live_end]):
        if fenced[index]:
            continue
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


def _replace_existing_section_fields(
    text: str,
    updates: dict[tuple[str, str], str],
) -> tuple[str, list[str]]:
    lines = text.splitlines(keepends=True)
    fenced = _markdown_fence_states(lines)
    failures: list[str] = []
    if not _markdown_fences_are_balanced(lines):
        return text, ["Target transition Markdown contains an unterminated fenced block"]
    section_ranges: dict[str, tuple[int, int]] = {}
    for section, _ in updates:
        heading = f"## {section}"
        matches = [
            index
            for index, line in enumerate(lines)
            if not fenced[index]
            and re.fullmatch(
                rf"##[ \t]+{re.escape(section)}[ \t]*",
                line.rstrip("\r\n"),
                flags=re.I,
            )
        ]
        if len(matches) != 1:
            failures.append(
                f"Target transition requires exactly one section {heading!r}: found {len(matches)}"
            )
            continue
        start = matches[0] + 1
        end = next(
            (
                index
                for index in range(start, len(lines))
                if not fenced[index]
                and _is_level_two_heading(lines[index].rstrip("\r\n"))
            ),
            len(lines),
        )
        section_ranges[section] = (start, end)
    if failures:
        return text, failures

    for (section, field), value in updates.items():
        start, end = section_ranges[section]
        matches = []
        for index in range(start, end):
            if fenced[index]:
                continue
            content = lines[index].rstrip("\r\n")
            match = re.match(
                rf"^(\s*(?:-\s*)?{re.escape(field)}:\s*).*$",
                content,
                flags=re.I,
            )
            if match:
                matches.append((index, match.group(1)))
        if len(matches) != 1:
            failures.append(
                f"Target transition requires exactly one existing field {field} "
                f"inside section '## {section}': found {len(matches)}"
            )
            continue
        index, prefix = matches[0]
        newline = _line_ending(lines[index])
        lines[index] = f"{prefix}`{value}`{newline}"
    if failures:
        return text, failures
    return "".join(lines), []


def _rename_sections(
    text: str,
    renames: dict[str, str],
) -> tuple[str, list[str], list[tuple[str, str]]]:
    failures: list[str] = []
    renamed: list[tuple[str, str]] = []
    lines = text.splitlines(keepends=True)
    fenced = _markdown_fence_states(lines)
    if not _markdown_fences_are_balanced(lines):
        return text, ["Target transition Markdown contains an unterminated fenced block"], []
    for old, new in renames.items():
        old_heading = old if old.startswith("## ") else f"## {old}"
        new_heading = new if new.startswith("## ") else f"## {new}"
        matches = [
            index
            for index, line in enumerate(lines)
            if not fenced[index]
            and re.fullmatch(
                rf"{re.escape(old_heading)}[ \t]*",
                line.rstrip("\r\n"),
                flags=re.I,
            )
        ]
        if len(matches) != 1:
            failures.append(
                f"Target transition requires exactly one section {old_heading!r}: found {len(matches)}"
            )
            continue
        destination_matches = [
            index
            for index, line in enumerate(lines)
            if not fenced[index]
            and re.fullmatch(
                rf"{re.escape(new_heading)}[ \t]*",
                line.rstrip("\r\n"),
                flags=re.I,
            )
        ]
        if any(index != matches[0] for index in destination_matches):
            failures.append(
                f"Target transition section rename destination already exists: {new_heading!r}"
            )
            continue
        newline = _line_ending(lines[matches[0]])
        lines[matches[0]] = f"{new_heading}{newline}"
        renamed.append((old_heading, new_heading))
    return "".join(lines), failures, renamed


def _projected_target_validation(
    *,
    relative: str,
    projected_text: str,
    expected_branch: str,
    expected_source_head: str,
    expected_origin_main: str,
    expected_worktree_path: str,
    expected_worktree_slot: str,
) -> list[str]:
    """Validate a dry-run projection without mutating the live external root."""

    with tempfile.TemporaryDirectory(prefix="ndai-target-projection-") as temp_dir:
        projected_root = Path(temp_dir)
        projected_target = projected_root.joinpath(*relative.split("/"))
        projected_target.parent.mkdir(parents=True, exist_ok=True)
        projected_target.write_bytes(projected_text.encode("utf-8"))
        projected_hash = sha256_file(projected_target)
        return validate_target_currentness(
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
    fenced = _markdown_fence_states(lines)
    live_end = next(
        (
            index
            for index, line in enumerate(lines)
            if not fenced[index] and _is_level_two_heading(line.rstrip("\r\n"))
        ),
        len(lines),
    )
    return "".join(lines[:live_end])


def _live_field_value(text: str, field: str) -> str:
    lines = _live_header_text(text).splitlines()
    fenced = _markdown_fence_states(lines)
    for index, line in enumerate(lines):
        if fenced[index]:
            continue
        if re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", line):
            value = re.sub(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", "", line).strip()
            if value.startswith("`") and value.endswith("`"):
                return value[1:-1]
            return value
    return "MISSING"


def _section_field_value(text: str, section: str, field: str) -> str:
    lines = text.splitlines()
    fenced = _markdown_fence_states(lines)
    matches = [
        index
        for index, line in enumerate(lines)
        if not fenced[index]
        and re.fullmatch(rf"##[ \t]+{re.escape(section)}[ \t]*", line, flags=re.I)
    ]
    if len(matches) != 1:
        return "MISSING"
    start = matches[0] + 1
    end = next(
        (
            index
            for index in range(start, len(lines))
            if not fenced[index] and _is_level_two_heading(lines[index])
        ),
        len(lines),
    )
    values = []
    for index in range(start, end):
        if fenced[index]:
            continue
        line = lines[index]
        if re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", line, flags=re.I):
            value = re.sub(
                rf"^\s*(?:-\s*)?{re.escape(field)}:\s*",
                "",
                line,
                flags=re.I,
            ).strip()
            values.append(value[1:-1] if value.startswith("`") and value.endswith("`") else value)
    return values[0] if len(values) == 1 else "MISSING"


def _non_updated_lines(text: str, fields: set[str]) -> list[str]:
    result: list[str] = []
    lines = text.splitlines(keepends=True)
    fenced = _markdown_fence_states(lines)
    for index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        if not fenced[index] and any(
            re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", content)
            for field in fields
        ):
            continue
        result.append(line)
    return result


def _non_updated_lines_with_sections(
    text: str,
    fields: set[str],
    section_headings: set[str],
    section_fields: set[tuple[str, str]] | None = None,
) -> list[str]:
    result: list[str] = []
    active_section = ""
    section_fields = section_fields or set()
    lines = text.splitlines(keepends=True)
    fenced = _markdown_fence_states(lines)
    for index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        section_match = (
            None
            if fenced[index]
            else re.match(r"^##[ \t]+(.+?)[ \t]*$", content)
        )
        if section_match:
            active_section = section_match.group(1).casefold()
        if not fenced[index] and content in section_headings:
            continue
        if not fenced[index] and any(
            re.match(rf"^\s*(?:-\s*)?{re.escape(field)}:\s*", content)
            for field in fields
        ):
            continue
        if not fenced[index] and any(
            active_section == section.casefold()
            and re.match(
                rf"^\s*(?:-\s*)?{re.escape(field)}:\s*",
                content,
                flags=re.I,
            )
            for section, field in section_fields
        ):
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
    section_assignments: list[str] | None = None,
    section_renames: list[str] | None = None,
    post_expected_source_head: str | None = None,
    post_expected_origin_main: str | None = None,
) -> tuple[bool, list[str], Path | None]:
    root = resolve_path(root)
    transition_started_ns = time.time_ns()
    failures = validate_canonical_root(root)
    failures.extend(validate_initialized_root(root))
    if failures:
        return False, failures, None

    section_renames_map, section_rename_failures = _parse_section_renames(section_renames or [])
    section_updates, section_assignment_failures = _parse_section_assignments(
        section_assignments or []
    )
    updates, assignment_failures = _parse_assignments(
        assignments,
        required=not additions and not section_updates and not section_renames_map,
    )
    additions_map, addition_failures = _parse_assignments(additions) if additions else ({}, [])
    if set(updates) & set(additions_map):
        assignment_failures.append("A field cannot be both --set-field and --add-field: " + ", ".join(sorted(set(updates) & set(additions_map))))
    renamed_section_keys = {section.casefold() for section in section_renames_map}
    overlapping_section_updates = sorted(
        {
            section
            for section, _ in section_updates
            if section.casefold() in renamed_section_keys
        }
    )
    if overlapping_section_updates:
        section_assignment_failures.append(
            "A section cannot be renamed and have a field replaced in the same transition: "
            + ", ".join(overlapping_section_updates)
        )
    failures.extend(assignment_failures)
    failures.extend(addition_failures)
    failures.extend(section_assignment_failures)
    failures.extend(section_rename_failures)
    snapshot_path, snapshot_failures = _safe_relative_path(root, snapshot, "Snapshot path")
    failures.extend(snapshot_failures)
    if snapshot_path is None or not snapshot_path.is_dir():
        failures.append(f"Snapshot directory is missing: {snapshot_path or snapshot}")
    initial_lock_payload, lock_failures = _lock_failures(
        root, lock_id, target, expected_branch, expected_worktree_path
    )
    failures.extend(lock_failures)
    relative, target_path, target_failures = _resolve_target_path(root, target)
    failures.extend(target_failures)
    if target_path is None or relative is None:
        return False, failures, None
    if failures:
        return False, failures, None

    failures.extend(
        _snapshot_failures(
            root=root,
            snapshot_path=snapshot_path,
            relative=relative,
            expected_target_sha256=expected_target_sha256,
            transition_started_ns=transition_started_ns,
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
    after_text, section_replacement_failures = _replace_existing_section_fields(
        after_text,
        section_updates,
    )
    if section_replacement_failures:
        return False, section_replacement_failures, None
    after_text, section_failures, renamed_sections = _rename_sections(after_text, section_renames_map)
    if section_failures:
        return False, section_failures, None
    changed_fields = set(updates) | set(additions_map)
    changed_section_fields = set(section_updates)
    allowed_section_lines = {heading for pair in renamed_sections for heading in pair}
    if _non_updated_lines_with_sections(
        before_text,
        changed_fields,
        allowed_section_lines,
        changed_section_fields,
    ) != _non_updated_lines_with_sections(
        after_text,
        changed_fields,
        allowed_section_lines,
        changed_section_fields,
    ):
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
    _before_final_lock_check(root, lock_id)
    final_lock_payload, final_lock_failures = _lock_failures(
        root, lock_id, target, expected_branch, expected_worktree_path
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
    )
    if final_snapshot_failures:
        return False, [
            f"Final snapshot validation: {item}" for item in final_snapshot_failures
        ], None
    atomic_write_text(target_path, after_text)
    actual_after_hash = sha256_file(target_path)
    post_validation = validate_target_currentness(
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

    audit_path = root / "audit_log" / f"target-currentness-{new_lock_id('audit')}.json"
    changed_field_details = [
        {
            "Field": field,
            "Before": _live_field_value(before_text, field),
            "After": _live_field_value(after_text, field),
        }
        for field in sorted(changed_fields)
    ]
    changed_field_details.extend(
        {
            "Field": f"{section}::{field}",
            "Before": _section_field_value(before_text, section, field),
            "After": _section_field_value(after_text, section, field),
        }
        for section, field in sorted(changed_section_fields)
    )
    changed_field_labels = sorted(changed_fields) + [
        f"{section}::{field}" for section, field in sorted(changed_section_fields)
    ]
    audit_payload = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Transition": "Target-scoped live projection reconciliation",
        "Target": relative,
        "Lock ID": lock_id,
        "Snapshot": snapshot,
        "Before SHA256": before_hash,
        "After SHA256": actual_after_hash,
        "Changed Fields": changed_field_labels,
        "Replaced Fields": sorted(updates),
        "Replaced Section Fields": [
            f"{section}::{field}" for section, field in sorted(changed_section_fields)
        ],
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
        post_expected_origin_main=args.post_expected_origin_main,
        expected_origin_main=args.expected_origin_main,
        expected_worktree_path=args.expected_worktree_path,
        expected_worktree_slot=args.expected_worktree_slot,
        expected_target_sha256=args.expected_target_sha256,
        assignments=args.set_field,
        additions=args.add_field,
        section_assignments=args.set_section_field,
        section_renames=args.rename_section,
        apply=args.apply,
    )
    print("External State Target Reconciliation")
    for message in messages:
        print(message)
    print(f"Transition Result: {'PASS' if ok else 'BLOCKED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
