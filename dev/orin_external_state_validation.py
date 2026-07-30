from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import stat
import re
from pathlib import PureWindowsPath

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    DEFAULT_SCHEMA_VERSION,
    REQUIRED_STATE_FIELDS,
    iter_state_files,
    load_json,
    resolve_path,
    sha256_file,
    validate_canonical_root,
    validate_initialized_root,
)


REQUIRED_STAGE4_RECORDS = [
    "central/active_branch_authority_state.md",
    "central/selected_next_state.md",
    "worktrees/Governance/worktree_state.md",
    "branches/feature_release_readiness_source_truth_intake/branch_state.md",
    "branches/feature_release_readiness_source_truth_intake/branch_plan.md",
    "branches/feature_release_readiness_source_truth_intake/ufd_ledger.md",
    "branches/feature_release_readiness_source_truth_intake/change_intent_ledger.md",
    "branches/feature_release_readiness_source_truth_intake/element_to_phase_matrix.md",
    "branches/feature_release_readiness_source_truth_intake/pr_readiness_state.md",
    "release_windows/current_release_window_state.md",
    "review_bundles/Governance/manifest.md",
    "cross_worktree_lessons/queue_state.md",
    "governance_candidates/queue_state.md",
    "promotion_packets/stage4_active_state_migration_execution_20260526.md",
    "acknowledgements/Governance/stage4_active_state_migration_execution_ack.md",
]

TARGET_SET_TRANSITION = "Bounded coherent target-set reconciliation"
MAX_EXTERNAL_STATE_EVIDENCE_BYTES = 16 * 1024 * 1024
SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
CANONICAL_UTC_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$"
)
LEGACY_RECEIPT_COMPATIBILITY_MANIFEST = Path(__file__).with_name(
    "orin_external_state_legacy_receipt_compatibility.json"
)
LEGACY_RECEIPT_COMPATIBILITY_SCHEMA = "legacy-external-state-receipt-compatibility-v1"
LEGACY_RECEIPT_CLASS = "Immutable Legacy Completed Audit Receipt"
LEGACY_RECEIPT_PURPOSE = "Pre-Transaction-State target-set completion evidence"
LEGACY_TARGET_SET_RECEIPT_FIELDS = {
    "External State Schema",
    "Last Updated",
    "Last Updated By",
    "Lock ID",
    "Snapshot",
    "Targets",
    "Transition",
    "Workload ID",
}
LEGACY_TARGET_ROW_FIELDS = {
    "Additions",
    "After SHA256",
    "Assignments",
    "Before SHA256",
    "Section Renames",
    "Target",
}
LEGACY_TARGET_ROW_OPTIONAL_FIELDS = {"Post Record State"}
LEGACY_COMPLETION_FIELDS = {
    "current validation state",
    "external state item status",
    "final disposition",
}
LEGACY_REQUIRED_COMPLETION_FIELDS = {
    "current validation state",
    "external state item status",
}

STRICT_JSON_CASE_AMBIGUOUS_FIELDS = frozenset(
    field.casefold()
    for field in {
        "Additions",
        "After SHA256",
        "Assignments",
        "Audit Path",
        "Before SHA256",
        "Before Text",
        "Compatibility Profile",
        "Copied Files",
        "External State Schema",
        "Immutable Purpose",
        "Last Updated",
        "Last Updated By",
        "Lock ID",
        "Lock State",
        "Path",
        "Post Record State",
        "Purpose",
        "Receipt Class",
        "Receipts",
        "Released At",
        "Retain Between Workloads",
        "Root",
        "Schema",
        "Section Renames",
        "SHA256",
        "Size",
        "Snapshot",
        "Target",
        "Targets",
        "Transaction State",
        "Transition",
        "Workload State",
        "Workload ID",
        "Intended Write Set",
    }
)


class StrictJSONError(ValueError):
    pass


def _is_json_integer_resource_limit(exc: ValueError) -> bool:
    message = str(exc).casefold()
    return "integer string conversion" in message and "limit" in message


def _strict_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    payload: dict[str, object] = {}
    case_spellings: dict[str, str] = {}
    for key, value in pairs:
        if key in payload:
            raise StrictJSONError(f"duplicate JSON field {key!r}")
        folded = key.casefold()
        prior = case_spellings.get(folded)
        if (
            prior is not None
            and prior != key
            and folded in STRICT_JSON_CASE_AMBIGUOUS_FIELDS
        ):
            raise StrictJSONError(
                f"case-ambiguous JSON fields {prior!r} and {key!r}"
            )
        payload[key] = value
        case_spellings.setdefault(folded, key)
    return payload


def _strict_json_loads(text: str) -> object:
    def reject_constant(value: str) -> object:
        raise StrictJSONError(f"non-standard JSON numeric constant {value!r}")

    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_json_object,
            parse_constant=reject_constant,
        )
    except StrictJSONError:
        raise
    except (RecursionError, MemoryError) as exc:
        raise StrictJSONError("JSON exceeds safe decoder resource limits") from exc
    except ValueError as exc:
        if not _is_json_integer_resource_limit(exc):
            raise
        raise StrictJSONError("JSON exceeds safe decoder resource limits") from exc


def _strict_json_load_bytes(path: Path, raw_bytes: bytes) -> object:
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StrictJSONError(f"{path}: JSON is not UTF-8: {exc}") from exc
    except MemoryError as exc:
        raise StrictJSONError(f"{path}: JSON exceeds safe decoder resource limits") from exc
    try:
        return _strict_json_loads(text)
    except (json.JSONDecodeError, StrictJSONError) as exc:
        raise StrictJSONError(f"{path}: {exc}") from exc


def _strict_json_load_path(path: Path) -> object:
    try:
        raw_bytes = path.read_bytes()
    except OSError as exc:
        raise StrictJSONError(f"{path}: unreadable JSON: {exc}") from exc
    return _strict_json_load_bytes(path, raw_bytes)

# These profiles are exact normalized states from the three immutable pre-state
# receipts. Receipt admission is additionally bound to the registry path and hash.
LEGACY_COMPLETION_PROFILES = {
    "rri-20260727-001-current-gate": {
        "external state item status": (
            "rri-20260727-001 current-gate autonomous-repair implementation and validation "
            "complete in the governance worktree; durability is blocked only by the "
            "standing-gate neutral-main fast-forward requirement"
        ),
        "current validation state": (
            "current-gate semantic contract, canonical publication, target-set rollback, lock "
            "lifecycle, governance, source-owner, packet false-green, public boundary, and "
            "external currentness checks pass; standing governance intake gate is expected red "
            "only for dirty tracked files and stale neutral main"
        ),
        "final disposition": (
            "current-gate implementation and validation are complete but not durable; one "
            "consolidated user decision for neutral-main fast-forward is required before "
            "standing-gate validation, commit, and push can complete"
        ),
    },
    "rri-20260727-001-durability-final": {
        "external state item status": (
            "rri-20260727-001 current-gate autonomous-repair implementation, same-gate allowlist "
            "repair, validation, commit, and feature-branch push are complete; pr readiness "
            "stage 1 is not started"
        ),
        "current validation state": (
            "complete routed validation contract pass at pushed head "
            "52fd1238145fedf222c79371f42e601dac833680, including the 7114-check standing "
            "governance intake gate; clean worktree and explicit feature-branch push verified"
        ),
        "final disposition": (
            "rri-20260727-001 current-gate repair is durable at pushed head "
            "52fd1238145fedf222c79371f42e601dac833680; no pr exists; next gate is separate user "
            "approval for pr readiness stage 1 analysis only"
        ),
    },
    "rri-20260727-001-pr1-projection": {
        "external state item status": (
            "pr readiness stage 1 projection-ownership false green is repaired, committed, "
            "pushed, packeted, and externally reconciled; stage 1 is ready for separate stage 2 "
            "user review"
        ),
        "current validation state": (
            "complete routed pr readiness stage 1 contract pass at pushed commit "
            "771caab90b0be290227ea67ba2778c41496a06f9; omitted-live-projection and historical-route "
            "negative fixtures pass; canonical packet parity/current identity pass; governed "
            "four-record target-set publication pass"
        ),
        "final disposition": (
            "pr readiness stage 1 is complete at pushed commit "
            "771caab90b0be290227ea67ba2778c41496a06f9 with canonical packet "
            "c:\\nexus user\\governance-20260727-162840.zip; stale pr_readiness_state.md is "
            "historical receipt evidence only; no pr exists; next gate is separate user approval "
            "for stage 2 and pr creation only"
        ),
    },
}


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
    parser.add_argument(
        "--require-stage4-records",
        action="store_true",
        help=(
            "Require the approved Stage 4 active-state migration record set. "
            "Use only for approved local external-state workflows, not clean-clone CI."
        ),
    )
    parser.add_argument(
        "--expected-source-head",
        help="Expected Source Repo HEAD for the manifest and required migrated markdown records.",
    )
    parser.add_argument(
        "--target-currentness",
        action="store_true",
        help=(
            "Run additive target-scoped currentness validation. This mode requires one explicit "
            "relative target and per-target identity expectations; it does not claim root-wide currentness."
        ),
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Relative external-state record path for --target-currentness. Repeat only to prove duplicate-target rejection.",
    )
    parser.add_argument("--expected-branch", help="Expected Branch value for the selected target record.")
    parser.add_argument("--expected-origin-main", help="Expected origin/main value for the selected target record.")
    parser.add_argument("--expected-worktree-path", help="Expected Worktree Path value for the selected target record.")
    parser.add_argument("--expected-worktree-slot", help="Expected Slot ID value for the selected target record.")
    parser.add_argument(
        "--expected-target-sha256",
        help="Expected SHA256 of the selected target record before validation (TOCTOU precondition).",
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


def markdown_field_value(text: str, field: str) -> str | None:
    pattern = re.compile(
        rf"^\s*(?:-\s*)?{re.escape(field)}:\s*(.*?)\s*$",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
        return value[1:-1].strip()
    return value


TARGET_LIVE_RECORD_CLASSES = {
    "live worktree projection",
    "live branch projection",
    "live branch plan",
    "live branch plan projection",
    "live central authority projection",
    "live selected-next projection",
    "live release-window projection",
    "live review-bundle projection",
}
TARGET_HISTORICAL_RECORD_CLASSES = {
    "historical receipt",
    "historical projection",
    "accepted historical receipt",
}


def _normalized_windows_value(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().strip("`").replace("/", "\\").rstrip("\\").casefold()


def _first_markdown_field(text: str, fields: tuple[str, ...]) -> str | None:
    for field in fields:
        value = markdown_field_value(text, field)
        if value:
            return value
    return None


def _live_header_text(text: str) -> str:
    """Restrict currentness parsing to the live header before receipt sections."""

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


def _markdown_field_values(text: str, fields: tuple[str, ...]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in fields:
        pattern = re.compile(
            rf"^\s*(?:-\s*)?{re.escape(field)}:\s*(.*?)\s*$",
            re.MULTILINE,
        )
        for match in pattern.finditer(text):
            value = match.group(1).strip()
            if value.startswith("`") and value.endswith("`") and value.count("`") == 2:
                value = value[1:-1].strip()
            if value:
                values.append((field, value))
    return values


def _field_alias_failures(
    relative: str,
    text: str,
    fields: tuple[str, ...],
) -> list[str]:
    values = _markdown_field_values(text, fields)
    if len(values) <= 1:
        return []
    rendered = ", ".join(f"{field}={value!r}" for field, value in values)
    return [
        f"Target Currentness: duplicate or conflicting live identity fields for {relative}: {rendered}"
    ]


def _has_reparse_point(path: Path) -> bool:
    try:
        if os.path.islink(path):
            return True
        metadata = os.stat(path, follow_symlinks=False)
        attributes = getattr(metadata, "st_file_attributes", 0)
        return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    except OSError:
        return False


def _resolve_target_path(root: Path, raw_target: str) -> tuple[str | None, Path | None, list[str]]:
    failures: list[str] = []
    if not isinstance(raw_target, str) or not raw_target.strip():
        return None, None, ["Target Currentness Contract: target path is missing"]
    raw = raw_target.strip()
    windows = PureWindowsPath(raw)
    if Path(raw).is_absolute() or windows.is_absolute() or windows.drive or windows.root:
        failures.append(f"Target Path Security: absolute/off-root target is forbidden: {raw_target}")
        return None, None, failures
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    if (
        not parts
        or any(part in {"", "..", "."} for part in parts)
        or "/" in raw and "\\" in raw
        or normalized.endswith("/")
        or any(":" in part for part in parts)
    ):
        failures.append(f"Target Path Security: traversal or alias segments are forbidden: {raw_target}")
        return None, None, failures
    relative = "/".join(parts)
    root_resolved = root.resolve(strict=False)
    candidate = (root / Path(*parts)).resolve(strict=False)
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        failures.append(f"Target Path Security: resolved target escapes external root: {raw_target}")
        return None, None, failures
    cursor = root_resolved
    for part in parts:
        cursor = cursor / part
        if cursor.exists() and _has_reparse_point(cursor):
            failures.append(f"Target Path Security: reparse/symlink escape is forbidden: {relative}")
            return relative, None, failures
    if not candidate.is_file():
        failures.append(f"Target Currentness: selected target is missing or not a file: {relative}")
        return relative, None, failures
    return relative, candidate, failures


def validate_target_currentness(
    root: Path,
    targets: list[str],
    *,
    expected_branch: str | None,
    expected_source_head: str | None,
    expected_origin_main: str | None,
    expected_worktree_path: str | None,
    expected_worktree_slot: str | None,
    expected_target_sha256: str | None,
    expected_schema: str = DEFAULT_SCHEMA_VERSION,
) -> list[str]:
    """Validate exactly one selected live external record without claiming root-wide freshness."""

    failures = validate_canonical_root(root)
    root = resolve_path(root)
    if not root.is_dir():
        failures.append(f"External State Missing: target-scoped validation root is absent: {root}")
        return failures
    if len(targets) != 1:
        failures.append(
            "Target Currentness Contract: exactly one explicit target is required; "
            f"received {len(targets)} (duplicate/ambiguous target selection is rejected)"
        )
        return failures
    required_expectations = {
        "expected branch": expected_branch,
        "expected source HEAD": expected_source_head,
        "expected origin/main": expected_origin_main,
        "expected worktree path": expected_worktree_path,
        "expected worktree slot": expected_worktree_slot,
        "expected target SHA256": expected_target_sha256,
    }
    missing = [name for name, value in required_expectations.items() if not value]
    if missing:
        failures.append(
            "Target Currentness Contract: fail closed; missing explicit expectations: "
            + ", ".join(missing)
        )
        return failures
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_target_sha256 or ""):
        failures.append("Target Currentness Contract: expected target SHA256 must be 64 hexadecimal characters")
        return failures

    relative, target_path, path_failures = _resolve_target_path(root, targets[0])
    failures.extend(path_failures)
    if target_path is None or relative is None:
        return failures

    try:
        before_hash = sha256_file(target_path)
        target_bytes = target_path.read_bytes()
        target_bytes_hash = hashlib.sha256(target_bytes).hexdigest()
        text = target_bytes.decode("utf-8")
        after_hash = sha256_file(target_path)
    except (OSError, UnicodeDecodeError) as exc:
        failures.append(f"Target Currentness: selected target is malformed or unreadable: {relative}: {exc}")
        return failures

    if before_hash != after_hash or target_bytes_hash != before_hash or target_bytes_hash != after_hash:
        failures.append(f"Target Currentness: selected target changed during validation (TOCTOU): {relative}")
    if before_hash.casefold() != (expected_target_sha256 or "").casefold():
        failures.append(
            f"Target Currentness: target hash precondition failed for {relative}: "
            f"expected {expected_target_sha256}, found {before_hash}"
        )
    if failures:
        return failures

    live_text = _live_header_text(text)
    failures.extend(_field_alias_failures(relative, live_text, ("Branch", "Current Branch")))
    failures.extend(_field_alias_failures(relative, live_text, ("Source Repo HEAD", "Current HEAD")))
    failures.extend(_field_alias_failures(relative, live_text, ("Origin/Main", "Source origin/main")))
    failures.extend(_field_alias_failures(relative, live_text, ("Worktree Path",)))
    failures.extend(_field_alias_failures(relative, live_text, ("Slot ID",)))
    if failures:
        return failures

    schema = markdown_field_value(live_text, "External State Schema")
    if schema != expected_schema:
        failures.append(
            f"External State Schema Conflict: {relative}: expected {expected_schema}, found {schema or 'MISSING'}"
        )
    record_class = _normalized_windows_value(markdown_field_value(live_text, "Record Class")).replace("\\", " ")
    if record_class in TARGET_HISTORICAL_RECORD_CLASSES or "historical receipt" in record_class:
        failures.append(f"Target Currentness: historical receipt cannot be selected as live state: {relative}")
    elif record_class not in TARGET_LIVE_RECORD_CLASSES:
        failures.append(
            f"Target Currentness: unsupported or missing live Record Class in {relative}: "
            f"{record_class or 'MISSING'}"
        )

    actual_branch = _first_markdown_field(live_text, ("Branch", "Current Branch"))
    actual_head = _first_markdown_field(live_text, ("Source Repo HEAD", "Current HEAD"))
    actual_origin = _first_markdown_field(live_text, ("Origin/Main", "Source origin/main"))
    actual_worktree = markdown_field_value(live_text, "Worktree Path")
    actual_slot = markdown_field_value(live_text, "Slot ID")
    for label, actual, expected, normalizer in (
        ("Branch", actual_branch, expected_branch, lambda value: (value or "").strip()),
        ("Source Repo HEAD", actual_head, expected_source_head, lambda value: (value or "").strip().casefold()),
        ("Origin/Main", actual_origin, expected_origin_main, lambda value: (value or "").strip().casefold()),
        ("Worktree Path", actual_worktree, expected_worktree_path, _normalized_windows_value),
        ("Slot ID", actual_slot, expected_worktree_slot, lambda value: (value or "").strip().casefold()),
    ):
        if not actual:
            failures.append(f"Target Currentness: {relative} is missing required field {label}")
        elif normalizer(actual) != normalizer(expected):
            failures.append(
                f"Target Currentness: {relative} {label} mismatch: expected {expected!r}, found {actual!r}"
            )

    record_role = markdown_field_value(live_text, "Record Role")
    for authority_marker in ("Record Role", "Historical Receipt Boundary"):
        marker_rows = re.findall(
            rf"^[ \t]*(?:-[ \t]*)?{re.escape(authority_marker)}:[^\r\n]*(?=\r?$)",
            live_text,
            flags=re.M | re.I,
        )
        if len(marker_rows) != 1:
            failures.append(
                f"Target Currentness: {relative} requires exactly one {authority_marker} marker"
            )
    if not _target_record_role_is_live(record_role):
        failures.append(
            f"Target Currentness: {relative} Record Role is not affirmative live authority"
        )
    historical_boundary = markdown_field_value(live_text, "Historical Receipt Boundary")
    if not _historical_receipt_boundary_is_protective(historical_boundary):
        failures.append(
            f"Target Currentness: {relative} Historical Receipt Boundary does not "
            "prevent historical receipts from redefining live authority"
        )
    return failures


def _target_record_role_is_live(value: str | None) -> bool:
    normalized = re.sub(r"\s+", " ", (value or "").casefold().strip(" `\t\r\n."))
    live_identity = any(term in normalized for term in ("current", "live", "active"))
    authority_shape = any(
        term in normalized
        for term in ("projection", "assignment", "state", "authority")
    )
    historical_only = re.search(
        r"\b(?:historical|receipt|archive|archived)\b.{0,30}\b(?:only|exclusive)\b|"
        r"\b(?:only|exclusive)\b.{0,30}\b(?:historical|receipt|archive|archived)\b",
        normalized,
    )
    denied = re.search(
        r"\b(?:no|not|never|without|lacks?|missing|unavailable|inactive|"
        r"non[- ]authoritative|non[- ]operational|unauthori[sz]ed|nominal|"
        r"forged|fabricated|falsified|counterfeit|invalid|unverified|purported|"
        r"alleged|simulated|placeholder|paper[- ]only)\b.{0,30}\b"
        r"(?:authority|assignment|projection|state|role)\b|"
        r"\b(?:authority|assignment|projection|state|role)\b.{0,30}\b"
        r"(?:none|absent|denied|revoked|inactive|unavailable|nominal|forged|"
        r"fabricated|falsified|counterfeit|invalid|unverified|purported|alleged|"
        r"simulated|placeholder|non[- ]operational|exists? only on paper|"
        r"only on paper)\b",
        normalized,
    )
    return bool(
        live_identity
        and authority_shape
        and historical_only is None
        and denied is None
    )


def _historical_receipt_boundary_is_protective(value: str | None) -> bool:
    normalized = re.sub(r"\s+", " ", (value or "").casefold().strip(" `\t\r\n."))
    if "historical" not in normalized:
        return False
    protective_clause = (
        r"\b(?:do not|does not|cannot|can not|must not|never)\b.{0,45}\b"
        r"(?:redefine|override|replace|reactivate|grant|own|control|retain|"
        r"preserve|source|supply|carry)\b|"
        r"\bhistorical identity evidence only\b"
    )
    protective = re.search(protective_clause, normalized)
    scrubbed = re.sub(protective_clause, "", normalized)
    contradictory = re.search(
        r"\b(?:redefine|override|replace|reactivate|grant|own|control)(?:s|ed|ing)?\b",
        scrubbed,
    )
    retained_authority = re.search(
        r"\b(?:retain(?:s|ed|ing)?|persist(?:s|ed|ing)?|continue(?:s|d|ing)?|"
        r"surviv(?:e|es|ed|ing)|preserv(?:e|es|ed|ing)|carr(?:y|ies|ied|ying) forward)\b"
        r".{0,45}\b(?:active|live|current|authority|assignment|ownership|control|role|state)\b|"
        r"\b(?:active|live|current|authority|assignment|ownership|control|role|state)\b"
        r".{0,45}\b(?:remain(?:s|ed|ing)?|retain(?:s|ed|ing)?|persist(?:s|ed|ing)?|"
        r"continue(?:s|d|ing)?|surviv(?:e|es|ed|ing)|comes? from|deriv(?:e|es|ed|ing) from|"
        r"sourc(?:e|es|ed|ing) from|inherit(?:s|ed|ing)? from|flows? from)\b|"
        r"\b(?:historical|receipt|archive)[- ](?:sourced|derived|owned|granted)\b"
        r".{0,30}\b(?:authority|assignment|ownership|control|role|state)\b",
        scrubbed,
    )
    conditional_exception = re.search(
        r"\b(?:unless|except|provided|subject to|until|if approved|when approved|"
        r"may|might|can still|could still)\b",
        scrubbed,
    )
    return bool(
        protective is not None
        and contradictory is None
        and retained_authority is None
        and conditional_exception is None
    )


def markdown_field_value_with_continuation(text: str, field: str) -> str | None:
    marker_pattern = re.compile(
        rf"^\s*(?:-\s*)?{re.escape(field)}:\s*(.*?)\s*$",
        re.IGNORECASE,
    )
    any_field_pattern = re.compile(r"^\s*(?:-\s*)?[A-Za-z][A-Za-z0-9 /_-]*:\s*")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = marker_pattern.match(line)
        if not match:
            continue
        values: list[str] = []
        first_value = match.group(1).strip()
        if first_value:
            values.append(first_value)
        for next_line in lines[index + 1 :]:
            stripped = next_line.strip()
            if not stripped:
                break
            if re.match(
                r"^(?:[-*]|\d+\.)?\s*(?:slice\s+\d+|slc-\d+)\b",
                stripped,
                re.IGNORECASE,
            ):
                values.append(stripped)
                continue
            if any_field_pattern.match(next_line):
                break
            if next_line[:1].isspace() and values:
                values.append(stripped)
                continue
            if values:
                values.append(stripped)
                continue
            break
        return " ".join(values).strip()
    return None


def resolve_markdown_path(value: str | None, root: Path) -> Path | None:
    if not value:
        return None
    cleaned = value.strip().strip("`").strip()
    if not cleaned:
        return None
    path = Path(cleaned)
    return path if path.is_absolute() else root / cleaned


def active_branch_plan_path(active_text: str, root: Path) -> Path | None:
    path_value = markdown_field_value(active_text, "Branch Runtime Engineering Plan Path")
    plan_path = resolve_markdown_path(path_value, root)
    if plan_path:
        return plan_path
    return resolve_markdown_path(
        markdown_field_value(active_text, "Branch Runtime Engineering Plan"),
        root,
    )


def normalized_route_value(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def route_word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9_/-]*", value))


def slice_map_deliverable_count(value: str) -> int:
    entries = re.split(r"(?:\.\s+|;\s+|\n+)", value)
    identifiers: set[str] = set()
    pair_pattern = re.compile(
        r"\b(?:slice\s+(\d+)\s*/\s*slc-(\d+)|slc-(\d+)\s*/\s*slice\s+(\d+))\b",
        flags=re.IGNORECASE,
    )
    identifier_pattern = re.compile(
        r"\b(?:slc-(\d+)|slice\s+(\d+))\b",
        flags=re.IGNORECASE,
    )
    for entry_index, entry in enumerate(entries):
        protected_spans: list[tuple[int, int]] = []
        for pair_index, pair in enumerate(pair_pattern.finditer(entry)):
            left = pair.group(1) or pair.group(3)
            right = pair.group(2) or pair.group(4)
            left_id = int(left)
            right_id = int(right)
            if left_id == right_id:
                identifiers.add(str(left_id))
            else:
                identifiers.add(f"entry-{entry_index}-pair-{pair_index}")
            protected_spans.append(pair.span())

        for match in identifier_pattern.finditer(entry):
            if any(start <= match.start() < end for start, end in protected_spans):
                continue
            identifiers.add(str(int(match.group(1) or match.group(2))))
    return len(identifiers)


def slice_map_mismatched_alias_pairs(value: str) -> list[str]:
    pair_pattern = re.compile(
        r"\b(?:slice\s+(\d+)\s*/\s*slc-(\d+)|slc-(\d+)\s*/\s*slice\s+(\d+))\b",
        flags=re.IGNORECASE,
    )
    mismatches: list[str] = []
    for pair in pair_pattern.finditer(value):
        left = pair.group(1) or pair.group(3)
        right = pair.group(2) or pair.group(4)
        if int(left) != int(right):
            mismatches.append(pair.group(0))
    return mismatches


def value_declares_multi_slice(value: str) -> bool:
    normalized = normalized_route_value(value)
    positive_match = re.search(r"\bmulti[- ]slice\b|\bmultiple\s+slices\b", normalized)
    if not positive_match:
        return False

    negation_match = re.search(
        r"\b(?:no|not|without)\b[^.\n;:]{0,80}\b(?:multi[- ]slice|multiple\s+slices)\b"
        r"|\bnon[- ]multi[- ]slice\b",
        normalized,
    )
    if negation_match and negation_match.start() < positive_match.start():
        return False

    postfixed_negation_match = re.search(
        r"\b(?:multi[- ]slice|multiple\s+slices)\b\s+(?:(?:is|are)\s+)?(?:"
        r"not\s+(?:required|needed|applicable|in\s+scope|part\s+of\s+this\s+branch)"
        r"|out\s+of\s+scope|unneeded)",
        normalized,
    )
    if postfixed_negation_match and postfixed_negation_match.start() == positive_match.start():
        return False

    future_gate_match = re.search(
        r"\bfuture(?:[- ]gated)?\b[^.\n;:]{0,80}"
        r"\b(?:multi[- ]slice|multiple\s+slices)\b[^.\n;:]{0,100}"
        r"\b(?:user[- ]gated|future[- ]gated|deferred|later|out\s+of\s+scope|outside)\b",
        normalized,
    )
    if future_gate_match and future_gate_match.start() <= positive_match.start():
        return False

    future_scope_match = re.search(
        r"\bfuture(?:[- ]gated)?\b[^.\n;:]{0,80}"
        r"\b(?:multi[- ]slice|multiple\s+slices)\b[^.\n;:]{0,140}"
        r"\b(?:outside|out\s+of\s+scope|not\s+part\s+of|excluded\s+from|deferred\s+beyond)\b"
        r"[^.\n;:]{0,80}\b(?:this|current)\s+branch\b",
        normalized,
    )
    if future_scope_match and future_scope_match.start() <= positive_match.start():
        return False

    postfixed_future_scope_match = re.search(
        r"\b(?:multi[- ]slice|multiple\s+slices)\b[^.\n;:]{0,140}"
        r"\b(?:future[- ]gated|user[- ]gated|deferred|later)\b[^.\n;:]{0,120}"
        r"\b(?:outside|out\s+of\s+scope|not\s+part\s+of|excluded\s+from)\b"
        r"[^.\n;:]{0,80}\b(?:this|current)\s+branch\b",
        normalized,
    )
    if (
        postfixed_future_scope_match
        and postfixed_future_scope_match.start() == positive_match.start()
    ):
        return False

    policy_non_carrier_match = re.search(
        r"\b(?:validat(?:e|es|ing)|validator|governance|policy|prevent(?:s|ing)?|"
        r"check(?:s|ing)?)\b[^.\n;:]{0,120}\b(?:multi[- ]slice|multiple\s+slices)\b"
        r"[^.\n;:]{0,160}\b(?:without|not)\b[^.\n;:]{0,120}"
        r"\b(?:carrier|creating|making|becoming|current\s+scope)\b",
        normalized,
    )
    if policy_non_carrier_match and policy_non_carrier_match.start() <= positive_match.start():
        return False
    return True


def multi_slice_marker_value_is_negative(value: str) -> bool:
    normalized = normalized_route_value(value)
    negative_patterns = (
        r"^(?:no|false|n/a|none|not applicable|not required)\.?$",
        r"^(?:not applicable|not required|n/a|none)\b.*\b(?:future|deferred|user[- ]gated|outside|out\s+of\s+scope)\b",
        r"^(?:future[- ]gated|deferred|not current|non[- ]current)\b.*\b(?:multi[- ]slice|multiple\s+slices)\b.*\b(?:future[- ]gated|user[- ]gated|deferred|outside|out\s+of\s+scope|not\s+current|non[- ]current)\b",
        r"\bnot\s+a?\s*multi[- ]slice\s+carrier\b",
        r"\bnot\s+multi[- ]slice\b",
        r"\bnon[- ]multi[- ]slice\b",
        r"\bsingle[- ]slice\b",
        r"\bone\s+slice\b",
        r"\bno\s+current\s+multi[- ]slice\b",
    )
    return any(re.search(pattern, normalized) for pattern in negative_patterns)


def plan_declares_multi_slice_carrier(plan_text: str) -> bool:
    carrier_value = markdown_field_value(plan_text, "Multi-Slice Carrier")
    slice_map = markdown_field_value_with_continuation(plan_text, "Slice Map")
    if slice_map and slice_map_deliverable_count(slice_map) >= 2:
        return True

    if carrier_value:
        return not multi_slice_marker_value_is_negative(carrier_value)

    current_scope_fields = (
        "Package Summary",
        "Package",
    )
    return any(
        value_declares_multi_slice(value)
        for field in current_scope_fields
        if (value := markdown_field_value_with_continuation(plan_text, field))
    )


def same_branch_split_decision_is_positive(value: str) -> bool:
    normalized = normalized_route_value(value)
    if re.search(
        r"\bno\s+separate\s+branch\s+required\b[^.\n]{0,160}"
        r"\bsame\s+branch\s+(?:remains|is|can\s+remain|may\s+remain)\s+legal\b",
        normalized,
    ):
        return True
    hard_negative_terms = (
        "same branch is not legal",
        "same branch not legal",
        "same branch is illegal",
        "not legal for same branch",
        "not legal in same branch",
        "cannot stay same branch",
        "cannot remain same branch",
        "must split",
        "required separate branch",
        "separate branch required",
        "different branch required",
        "same-branch blocked",
        "blocked same branch",
        "whether same branch",
        "pending decision",
        "before deciding",
        "deciding whether",
        "decide whether",
    )
    if any(term in normalized for term in hard_negative_terms):
        return False
    positive_terms = (
        "no split required",
        "split not required",
        "same branch remains legal",
        "same branch is legal",
        "same branch legal",
        "same branch remains valid",
        "same branch can remain legal",
        "same branch may remain legal",
        "same branch remains the legal",
        "same branch remains the approved",
        "same branch carrier",
        "same branch package",
    )
    if any(term in normalized for term in positive_terms):
        return True
    if "split required" in normalized:
        return False
    return False


def separate_branch_split_required_is_positive(value: str) -> bool:
    normalized = normalized_route_value(value)
    negative_terms = (
        "not required",
        "not needed",
        "not necessary",
        "split not required",
        "no split",
        "keep same branch",
        "same branch remains",
        "same branch is legal",
        "same branch legal",
        "same branch carrier",
        "same branch package",
        "remain same branch",
        "split optional",
        "whether to split",
        "deciding whether",
        "decide whether",
        "pending decision",
    )
    if any(term in normalized for term in negative_terms):
        return False
    explicit_split_terms = (
        "split required",
        "separate branch required",
        "required separate branch",
        "separate carrier",
        "separate user-approved carrier",
        "different branch",
        "different carrier",
        "must split",
        "must wait for a separate",
    )
    if any(term in normalized for term in explicit_split_terms):
        return True
    if normalized.startswith(("yes.", "yes;", "yes:", "yes ")):
        return any(term in normalized for term in explicit_split_terms)
    return normalized == "yes"


def validate_implementation_route_values(plan_text: str) -> list[str]:
    issues: list[str] = []
    marker_values = {
        "Selected Implementation Route": markdown_field_value(
            plan_text, "Selected Implementation Route"
        )
        or "",
        "Concrete Deliverable": markdown_field_value(plan_text, "Concrete Deliverable")
        or "",
        "Implementation Output": markdown_field_value(
            plan_text, "Implementation Output"
        )
        or "",
        "Infrastructure / Setup Relationship": markdown_field_value(
            plan_text, "Infrastructure / Setup Relationship"
        )
        or "",
        "USER Action Gate": markdown_field_value(plan_text, "USER Action Gate") or "",
        "Route Disposition": markdown_field_value(plan_text, "Route Disposition") or "",
        "Retarget / Rename Recommendation": markdown_field_value(
            plan_text, "Retarget / Rename Recommendation"
        )
        or "",
    }
    combined_route = normalized_route_value(
        "\n".join(
            (
                marker_values["Selected Implementation Route"],
                marker_values["Concrete Deliverable"],
                marker_values["Implementation Output"],
            )
        )
    )
    full_normalized = normalized_route_value(plan_text)
    setup_normalized = normalized_route_value(
        marker_values["Infrastructure / Setup Relationship"]
    )
    disposition_normalized = normalized_route_value(marker_values["Route Disposition"])
    retarget_normalized = normalized_route_value(
        marker_values["Retarget / Rename Recommendation"]
    )
    user_gate = marker_values["USER Action Gate"]

    concrete_terms = (
        "implementation",
        "enforcement",
        "runtime",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "consent shell",
        "trust-boundary",
        "security",
        "capability-pack",
        "memory/cache",
        "provider",
        "user-facing",
        "workflow",
    )
    concrete_behavior_terms = (
        "enforce",
        "block",
        "validate",
        "fail-closed",
        "detect",
        "route",
        "render",
        "persist",
        "execute",
        "control",
        "runtime",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "user-facing",
    )
    actual_implementation_terms = (
        "implement",
        "implemented",
        "enforce",
        "enforcement",
        "block",
        "reject",
        "prevent",
        "fail-closed",
        "fails closed",
        "validate",
        "persist",
        "execute",
        "route",
        "disable",
        "update",
        "create",
    )
    implemented_target_terms = (
        "behavior",
        "control",
        "workflow",
        "surface",
        "state",
        "transition",
        "enforcement",
        "consent shell",
        "consent-shell",
        "trust-boundary",
        "boundary",
        "exclusion",
        "suppression",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "runtime",
        "user-facing",
    )
    evidence_only_route_terms = (
        "proof package",
        "proof packet",
        "validation proof",
        "setup proof",
        "readiness proof",
        "registry proof",
        "boundary proof",
        "review packet",
        "packet generation",
        "decision path",
        "readiness matrix",
        "validation plan",
        "boundary controls",
        "boundary-control labels",
    )
    tbd_route_terms = (
        "implementation output is tbd",
        "tbd",
        "to be determined",
        "decide later",
        "selected later",
        "later during bp2",
        "bp2 will choose",
        "bp2 will decide",
    )
    negated_real_behavior_terms = (
        "does not add behavior",
        "does not change behavior",
        "does not change state",
        "does not enforce",
        "does not implement",
        "will not add behavior",
        "will not change behavior",
        "will not enforce",
        "will not implement",
        "no enforcement behavior",
        "no implemented behavior",
        "no implemented control",
        "no validator behavior",
        "no runtime behavior",
        "no source-truth behavior",
        "no user-facing surface",
        "no state transition",
        "behavior changes are deferred",
        "without implemented behavior",
    )
    planning_only_terms = (
        "planning-only",
        "readiness-only",
        "setup-only",
        "lane setup only",
        "choose later branches",
        "identify later branches",
        "no implementation route",
        "implementation output: none",
    )
    fake_feature_terms = (
        "setup feature",
        "readiness feature",
        "planning feature",
        "decision feature",
        "registry feature",
        "skeleton feature",
        "packet feature",
        "review feature",
        "feature label",
    )

    real_behavior_present = (
        any(term in combined_route for term in actual_implementation_terms)
        and any(term in combined_route for term in implemented_target_terms)
        and not any(term in combined_route for term in negated_real_behavior_terms)
    )
    if (
        route_word_count(marker_values["Concrete Deliverable"]) < 8
        or route_word_count(marker_values["Implementation Output"]) < 8
        or not any(term in combined_route for term in concrete_terms)
        or not real_behavior_present
        or any(term in combined_route for term in planning_only_terms)
    ):
        issues.append(
            "External active branch plan route values must name a concrete "
            "implementation behavior before BP1"
        )
    if any(term in combined_route for term in negated_real_behavior_terms):
        issues.append(
            "External active branch plan route values cannot negate implementation behavior"
        )
    if (
        any(term in combined_route for term in evidence_only_route_terms)
        and not real_behavior_present
    ):
        issues.append(
            "External active branch plan route values cannot substitute proof, readiness, "
            "or boundary-label evidence for implementation behavior"
        )
    if any(term in combined_route for term in tbd_route_terms):
        issues.append(
            "External active branch plan route values cannot defer implementation output "
            "to BP2 or a later decision"
        )
    if any(term in combined_route for term in fake_feature_terms) and not (
        real_behavior_present
        and any(term in combined_route for term in concrete_behavior_terms)
    ):
        issues.append(
            "External active branch plan route values cannot label planning, setup, "
            "registry, skeleton, packet, or review work as the feature"
        )
    if any(
        term in full_normalized
        for term in (
            "lane setup",
            "repo/root/remote",
            "private root",
            "private remote",
            "skeleton setup",
            "registry creation",
        )
    ) and not (
        "execution-enabling" in setup_normalized
        or "selected implementation route" in setup_normalized
        or "exact user action gate" in setup_normalized
    ):
        issues.append(
            "External active branch plan infrastructure/setup values must tie to "
            "the selected route or exact USER action gate"
        )
    if "Dev lane" in plan_text:
        issues.append("Use Developer lane, not Dev lane, in current branch-planning text")
    if "developer" in full_normalized and "Developer lane" not in plan_text:
        issues.append(
            "Developer lane terminology must be explicit when developer lane scope appears"
        )
    if "hold" in disposition_normalized and route_word_count(user_gate) < 6:
        issues.append("External active branch plan HOLD requires an exact USER action gate")
    if (
        "retarget" in disposition_normalized or "rename" in disposition_normalized
    ) and not (
        ("retarget" in retarget_normalized or "rename" in retarget_normalized)
        and any(term in retarget_normalized for term in concrete_terms)
    ):
        issues.append(
            "External active branch plan retarget/rename disposition requires "
            "a concrete recommendation"
        )
    if route_word_count(user_gate) < 6:
        issues.append(
            "External active branch plan route values must name pending USER action gate posture"
        )
    return issues


def validate_slice_slc_seam_model_text(plan_text: str) -> list[str]:
    issues: list[str] = []
    normalized = normalized_route_value(plan_text)
    ambiguity_patterns = (
        r"\bslc(?:[- ]\d+)?\s+is\s+the\s+seam\b",
        r"\bslcs\s+are\s+seams\b",
        r"\bslc(?:[- ]\d+)?\s+means\s+seam\b",
        r"\bslice\s+is\s+(?:the\s+)?proof\b",
        r"\bseam\s+is\s+the\s+branch\s+deliverable\b",
        r"\bseam\s+is\s+the\s+feature\b",
        r"\bseam-only\s+branch\b",
        r"\bslc[- ]\d+\s+branch(?:es)?(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+\s+(?:owns|has)\s+(?:a\s+|the\s+|its\s+own\s+)?branch(?:es)?(?=[\s.,;:]|$)",
        r"\bslcs\s+(?:own|owns|have|has)\s+(?:a\s+|the\s+|their\s+own\s+)?branch(?:es)?(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+(?:own|owns|have|has)\s+(?:a\s+|the\s+|their\s+own\s+|its\s+own\s+)?branch(?:es)?(?=[\s.,;:]|$)",
        r"\bbranch(?:es)?\s+(?:for|per)\s+slc[- ]\d+\b",
        r"\bslc(?:[- ]\d+)?\s+is\s+a\s+branch(?=[\s.,;:]|$)",
        r"\bslcs\s+are\s+branches(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+are\s+branches(?=[\s.,;:]|$)",
        r"\bslc(?:[- ]\d+)?\s+is\s+a\s+separate\s+branch(?=[\s.,;:]|$)",
        r"\bslcs\s+are\s+separate\s+branches(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+are\s+separate\s+branches(?=[\s.,;:]|$)",
        r"\bslc(?:[- ]\d+)?\s+becomes\s+a\s+branch(?=[\s.,;:]|$)",
        r"\bslcs\s+become\s+branches(?=[\s.,;:]|$)",
        r"\bslc[- ]\d+(?:\s*(?:,|and)\s*slc[- ]\d+)+\s+become\s+branches(?=[\s.,;:]|$)",
        r"\bslc(?:[- ]\d+)?\s+creates\s+the\s+branch(?=[\s.,;:]|$)",
        r"\beach\s+slc(?:[- ]\d+)?\s+is\s+a\s+branch(?=[\s.,;:]|$)",
        r"\beach\s+slc(?:[- ]\d+)?\s+(?:owns|has)\s+(?:a\s+|the\s+|its\s+own\s+)?branch(?=[\s.,;:]|$)",
        r"\beach\s+slc(?:[- ]\d+)?\s+becomes\s+a\s+branch(?=[\s.,;:]|$)",
    )
    if any(re.search(pattern, normalized) for pattern in ambiguity_patterns):
        issues.append(
            "SLC / Slice / Seam terminology ambiguity: SLC must resolve to "
            "Slice-level deliverables, and seams must remain execution or "
            "validation checkpoints"
        )

    slc_slice_alias_terms = (
        "slice-level",
        "alias",
        "historical",
        "short form",
        "short-form",
        "shorthand",
        "abbreviation",
        "slc is slice",
        "slc means slice",
        "slc/slice",
        "slice/slc",
    )
    if "slc" in normalized and not any(
        term in normalized for term in slc_slice_alias_terms
    ):
        issues.append(
            "SLC / Slice / Seam terminology ambiguity: SLC use must name "
            "its Slice-level alias, shorthand, or historical traceability posture"
        )

    if plan_declares_multi_slice_carrier(plan_text):
        required_markers = (
            "FAM",
            "Package",
            "Selected Implementation Route",
            "Slice Map",
            "Shared Owner / Worktree",
            "Shared Validation / Proof Path",
            "Split Decision",
        )
        for marker in required_markers:
            marker_value = (
                markdown_field_value_with_continuation(plan_text, marker)
                if marker == "Slice Map"
                else markdown_field_value(plan_text, marker)
            )
            if not marker_value:
                issues.append(f"Multi-slice carrier missing {marker}:")
        route = markdown_field_value(plan_text, "Selected Implementation Route") or ""
        slice_map = markdown_field_value_with_continuation(plan_text, "Slice Map") or ""
        validation = (
            markdown_field_value(plan_text, "Shared Validation / Proof Path") or ""
        )
        split_decision = markdown_field_value(plan_text, "Split Decision") or ""
        if route_word_count(route) < 8:
            issues.append("Multi-slice carrier must name a concrete implementation route")
        if slice_map_mismatched_alias_pairs(slice_map):
            issues.append(
                "Multi-slice carrier Slice Map contains mismatched Slice/SLC alias pair"
            )
        if slice_map_deliverable_count(slice_map) < 2:
            issues.append("Multi-slice carrier must map at least two slices")
        if route_word_count(validation) < 8:
            issues.append(
                "Multi-slice carrier must name a shared validation/proof path"
            )
        if not same_branch_split_decision_is_positive(split_decision):
            issues.append("Multi-slice carrier must prove why the grouped branch is legal")

    if "required separate branch case:" in normalized:
        required_markers = (
            "Required Separate Branch Case",
            "Divergence Basis",
            "Split Required",
            "Blocked Same-Branch Reason",
            "Recommended Carrier",
        )
        for marker in required_markers:
            if not markdown_field_value(plan_text, marker):
                issues.append(f"Required separate branch case missing {marker}:")
        divergence = markdown_field_value(plan_text, "Divergence Basis") or ""
        split_required = markdown_field_value(plan_text, "Split Required") or ""
        if not any(
            term in divergence.casefold()
            for term in (
                "different fam",
                "different package",
                "private",
                "provider",
                "runtime",
                "release timing",
                "validation path",
                "owner/worktree",
            )
        ):
            issues.append(
                "Required separate branch case must name a real divergence basis"
            )
        if not separate_branch_split_required_is_positive(split_required):
            issues.append(
                "Required separate branch case must explicitly require a split"
            )
    return issues


def validate_active_branch_plan_posture(root: Path) -> list[str]:
    issues: list[str] = []
    active_state = root / "central" / "active_branch_authority_state.md"
    if not active_state.is_file():
        return issues

    active_text = active_state.read_text(encoding="utf-8")
    plan_path = active_branch_plan_path(active_text, root)
    branch_state_path = resolve_markdown_path(
        markdown_field_value(active_text, "Branch State"),
        root,
    )
    branch_state_text = (
        branch_state_path.read_text(encoding="utf-8")
        if branch_state_path and branch_state_path.is_file()
        else ""
    )
    bp1_value = "BP1 USER Branch Vision Review"
    active_routes_to_bp1 = bp1_value in {
        (markdown_field_value(active_text, "Next Gate") or "").strip("` "),
        (markdown_field_value(active_text, "Next Legal Phase") or "").strip("` "),
        (markdown_field_value(branch_state_text, "Next Legal Phase") or "").strip("` "),
    }
    if not active_routes_to_bp1:
        active_routes_to_bp1 = (
            "Next Gate: `BP1 USER Branch Vision Review`" in active_text
            or "Next Legal Phase: `BP1 USER Branch Vision Review`" in active_text
            or "Next Legal Phase: `BP1 USER Branch Vision Review`" in branch_state_text
            or "Next Gate: BP1 USER Branch Vision Review" in active_text
            or "Next Legal Phase: BP1 USER Branch Vision Review" in active_text
            or "Next Legal Phase: BP1 USER Branch Vision Review" in branch_state_text
        )
    if not active_routes_to_bp1:
        return issues

    if not plan_path or not plan_path.is_file():
        return [
            "External active branch state routes to BP1 without an existing active branch plan"
        ]

    plan_text = plan_path.read_text(encoding="utf-8")
    required_route_markers = (
        "Selected Implementation Route",
        "Implementation Route Class",
        "Concrete Deliverable",
        "Implementation Output",
        "Infrastructure / Setup Relationship",
        "USER Action Gate",
        "Route Disposition",
        "Retarget / Rename Recommendation",
    )
    missing_route_markers = [
        marker
        for marker in required_route_markers
        if not markdown_field_value(plan_text, marker)
    ]
    route_resolution_status = markdown_field_value(
        plan_text, "BR2 Route Resolution Status"
    )
    route_disposition = normalized_route_value(
        markdown_field_value(plan_text, "Route Disposition") or ""
    )
    has_hold_or_retarget = bool(route_resolution_status) or any(
        disposition in route_disposition
        for disposition in ("hold", "retarget", "rename")
    )
    if has_hold_or_retarget:
        issues.append(
            "External active branch state routes to BP1 while active branch plan "
            "is still HOLD/RETARGET route resolution"
        )
    if missing_route_markers:
        issues.append(
            "External active branch state routes to BP1 without "
            "implementation-bearing route fields in active branch plan: "
            + ", ".join(missing_route_markers)
        )
    else:
        issues.extend(validate_implementation_route_values(plan_text))
    issues.extend(validate_slice_slc_seam_model_text(plan_text))
    return issues


def validate_fam007_workstream_visual_acceptance_gate(root: Path) -> list[str]:
    issues: list[str] = []
    branch_root = root / "branches" / "feature_fam_007_ai_control_center_readiness_diagnostics"
    branch_state = branch_root / "branch_state.md"
    branch_plan = branch_root / "branch_plan.md"
    if not branch_state.is_file() or not branch_plan.is_file():
        return issues

    state_text = branch_state.read_text(encoding="utf-8")
    plan_text = branch_plan.read_text(encoding="utf-8")
    state_normalized = state_text.casefold()
    plan_normalized = plan_text.casefold()
    is_ui_workstream_repair = (
        "option g runtime ui repair implemented" in state_normalized
        or "workstream_implementation_repaired" in plan_normalized
        or "option g runtime adoption / child-window grammar repair" in plan_normalized
    )
    active_next = (
        markdown_field_value(state_text, "Next Legal Phase")
        or markdown_field_value(plan_text, "Next Legal Phase")
        or ""
    ).casefold()
    active_current_gate = (markdown_field_value(state_text, "Current Gate") or "").casefold()
    active_next_routes_to_visual_review = "workstream-exit visual acceptance" in active_next
    routes_to_h1_lv = (
        not active_next_routes_to_visual_review
        and (
            active_next.startswith("prepare hardening h1")
            or active_next.startswith("prepare a source-truth-routed hardening h1")
            or active_next.startswith("prepare h1")
            or active_next.startswith("hardening h1")
            or active_next.startswith("live validation")
            or active_next.startswith("h1/lv")
        )
    ) or (
        not active_next_routes_to_visual_review
        and (
            "prepare hardening h1" in active_next
            or "prepare a source-truth-routed hardening h1" in active_next
            or "prepare h1/lv" in active_next
        )
    ) or (
        "next legal gate is hardening h1" in active_current_gate
        or "next legal gate is h1" in active_current_gate
    )
    if not is_ui_workstream_repair or not routes_to_h1_lv:
        return issues

    gate_state = markdown_field_value(state_text, "Workstream Exit Visual Acceptance Gate State") or ""
    gate_state_norm = gate_state.casefold()
    accepted_or_waived = any(
        marker in gate_state_norm
        for marker in (
            "user accepted",
            "user waived",
            "user deferred with explicit source-truth boundary",
        )
    )
    if not accepted_or_waived:
        issues.append(
            "FAM-007 Workstream Visual Acceptance Gate Bypass: active state routes "
            "Option G UI/UX Workstream repair toward H1/LV before USER accepted, "
            "waived, or explicitly deferred the runtime visual acceptance gate"
        )
    return issues


def validate_markdown_record(
    path: Path,
    expected_schema: str,
    expected_source_head: str | None,
) -> list[str]:
    issues: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - local state read errors should be reported cleanly
        return [f"External State Corrupt: {path}: {exc}"]

    for field in REQUIRED_STATE_FIELDS:
        value = markdown_field_value(text, field)
        if not value:
            issues.append(f"External State Corrupt: {path}: missing {field}")
            continue
        if field == "External State Schema" and value != expected_schema:
            issues.append(
                f"External State Schema Conflict: {path}: expected {expected_schema}, found {value}"
            )
        if field == "Source Repo HEAD" and expected_source_head and value != expected_source_head:
            issues.append(
                f"External State Version Conflict: {path}: expected Source Repo HEAD "
                f"{expected_source_head}, found {value}"
            )
    return issues


def validate_stage4_records(
    root: Path,
    expected_schema: str,
    expected_source_head: str | None,
) -> list[str]:
    issues: list[str] = []
    for relative_record in REQUIRED_STAGE4_RECORDS:
        record_path = root / relative_record
        if not record_path.exists():
            issues.append(f"External State Missing: required migrated record missing: {relative_record}")
            continue
        issues.extend(validate_markdown_record(record_path, expected_schema, expected_source_head))
    return issues


def validate_released_locks(root: Path) -> list[str]:
    issues: list[str] = []
    locks_dir = root / "locks"
    if not locks_dir.exists():
        return ["External State Missing: locks directory missing"]
    for lock_path in sorted(locks_dir.glob("*.json")):
        try:
            payload = load_json(lock_path)
        except Exception as exc:  # noqa: BLE001 - corrupt lock files block local operational workflow
            issues.append(f"External State Corrupt: {lock_path}: {exc}")
            continue
        lock_state = str(payload.get("Lock State", "MISSING"))
        if lock_state not in {"Released", "Expired"}:
            issues.append(f"Stale Lock Recovery Required: {lock_path}: Lock State is {lock_state}")
    return issues


def _safe_external_relative_parts(value: object) -> tuple[str, ...] | None:
    if not isinstance(value, str):
        return None
    raw = value.strip()
    candidate = PureWindowsPath(raw)
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    reserved_names = {"con", "prn", "aux", "nul"} | {
        f"{prefix}{index}"
        for prefix in ("com", "lpt")
        for index in range(1, 10)
    }
    if (
        not raw
        or raw != value
        or Path(raw).is_absolute()
        or candidate.is_absolute()
        or candidate.drive
        or candidate.root
        or any(part in {"", ".", ".."} for part in parts)
        or ("/" in raw and "\\" in raw)
        or normalized.endswith("/")
        or any(":" in part for part in parts)
        or any(any(ord(character) < 32 for character in part) for part in parts)
        or any(
            any(0xD800 <= ord(character) <= 0xDFFF for character in part)
            for part in parts
        )
        or any(any(character in '<>"|?*' for character in part) for part in parts)
        or any(part.endswith((" ", ".")) for part in parts)
        or any(part.split(".", 1)[0].casefold() in reserved_names for part in parts)
    ):
        return None
    return tuple(parts)


def _host_path_key(value: str) -> str:
    return os.path.normcase(value.replace("/", os.sep)).replace("\\", "/")


def _canonical_utc_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not CANONICAL_UTC_TIMESTAMP_PATTERN.fullmatch(value):
        return None
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    return parsed if parsed.utcoffset() == timedelta(0) else None


def _is_canonical_utc_timestamp(value: object) -> bool:
    return _canonical_utc_datetime(value) is not None


def _confined_evidence_file(base: Path, parts: tuple[str, ...]) -> Path | None:
    base_resolved = base.resolve(strict=False)
    candidate = base.joinpath(*parts).resolve(strict=False)
    try:
        candidate.relative_to(base_resolved)
    except ValueError:
        return None
    cursor = base_resolved
    for part in parts:
        cursor = cursor / part
        if cursor.exists() and _has_reparse_point(cursor):
            return None
    return candidate if candidate.is_file() else None


def _confined_component_states(
    base: Path,
    parts: tuple[str, ...],
) -> tuple[Path, list[os.stat_result]]:
    cursor = Path(os.path.abspath(base))
    components = [cursor]
    for part in parts:
        cursor /= part
        components.append(cursor)
    states: list[os.stat_result] = []
    for component in components:
        metadata = os.stat(component, follow_symlinks=False)
        if _has_reparse_point(component):
            raise OSError("evidence path traverses a reparse point")
        states.append(metadata)
    return cursor, states


def _open_confined_evidence_file(
    base: Path,
    parts: tuple[str, ...],
) -> tuple[Path, int, list[os.stat_result], os.stat_result]:
    candidate = _confined_evidence_file(base, parts)
    if candidate is None:
        raise OSError("evidence file is missing or escapes through a reparse point")
    checked_candidate, before_states = _confined_component_states(base, parts)
    if checked_candidate.resolve(strict=False) != candidate:
        raise OSError("evidence path changed during confinement check")
    before = before_states[-1]
    if not stat.S_ISREG(before.st_mode) or _has_reparse_point(candidate):
        raise OSError("evidence file is not a regular confined file")

    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(candidate, flags)
    try:
        opened_before = os.fstat(descriptor)
        if not os.path.samestat(before, opened_before):
            raise OSError("evidence file changed between confinement check and open")
        return checked_candidate, descriptor, before_states, opened_before
    except Exception:
        os.close(descriptor)
        raise


def _verify_confined_evidence_file(
    base: Path,
    parts: tuple[str, ...],
    checked_candidate: Path,
    descriptor: int,
    before_states: list[os.stat_result],
    opened_before: os.stat_result,
) -> None:
    opened_after = os.fstat(descriptor)
    if (
        not os.path.samestat(opened_before, opened_after)
        or opened_before.st_size != opened_after.st_size
        or opened_before.st_mtime_ns != opened_after.st_mtime_ns
    ):
        raise OSError("evidence file changed while reading")
    after_candidate, after_states = _confined_component_states(base, parts)
    if (
        after_candidate != checked_candidate
        or len(after_states) != len(before_states)
        or any(
            not os.path.samestat(before_state, after_state)
            for before_state, after_state in zip(before_states, after_states)
        )
    ):
        raise OSError("evidence path changed while reading")


def _read_confined_evidence_file(
    base: Path,
    parts: tuple[str, ...],
) -> tuple[Path, bytes]:
    candidate, descriptor, before_states, opened_before = _open_confined_evidence_file(
        base,
        parts,
    )
    try:
        if opened_before.st_size > MAX_EXTERNAL_STATE_EVIDENCE_BYTES:
            raise OSError(
                "evidence file exceeds the bounded read limit of "
                f"{MAX_EXTERNAL_STATE_EVIDENCE_BYTES} bytes"
            )
        payload = bytearray()
        try:
            while chunk := os.read(descriptor, 1024 * 1024):
                if len(payload) + len(chunk) > MAX_EXTERNAL_STATE_EVIDENCE_BYTES:
                    raise OSError(
                        "evidence file grew beyond the bounded read limit of "
                        f"{MAX_EXTERNAL_STATE_EVIDENCE_BYTES} bytes"
                    )
                payload.extend(chunk)
            raw_bytes = bytes(payload)
        except MemoryError as exc:
            raise OSError("evidence file read exceeded safe resource limits") from exc
        _verify_confined_evidence_file(
            base,
            parts,
            candidate,
            descriptor,
            before_states,
            opened_before,
        )
        return candidate, raw_bytes
    finally:
        os.close(descriptor)


def _strict_json_load_confined(
    base: Path,
    parts: tuple[str, ...],
) -> tuple[Path, object]:
    path, payload, _ = _strict_json_load_confined_with_digest(base, parts)
    return path, payload


def _strict_json_load_confined_with_digest(
    base: Path,
    parts: tuple[str, ...],
) -> tuple[Path, object, str]:
    path, raw_bytes = _read_confined_evidence_file(base, parts)
    return (
        path,
        _strict_json_load_bytes(path, raw_bytes),
        hashlib.sha256(raw_bytes).hexdigest(),
    )


def _sha256_confined_evidence_file(base: Path, parts: tuple[str, ...]) -> str:
    candidate, descriptor, before_states, opened_before = _open_confined_evidence_file(
        base,
        parts,
    )
    try:
        if opened_before.st_size > MAX_EXTERNAL_STATE_EVIDENCE_BYTES:
            raise OSError(
                "evidence file exceeds the bounded hash limit of "
                f"{MAX_EXTERNAL_STATE_EVIDENCE_BYTES} bytes"
            )
        digest = hashlib.sha256()
        hashed_size = 0
        while chunk := os.read(descriptor, 1024 * 1024):
            hashed_size += len(chunk)
            if hashed_size > MAX_EXTERNAL_STATE_EVIDENCE_BYTES:
                raise OSError(
                    "evidence file grew beyond the bounded hash limit of "
                    f"{MAX_EXTERNAL_STATE_EVIDENCE_BYTES} bytes"
                )
            digest.update(chunk)
        _verify_confined_evidence_file(
            base,
            parts,
            candidate,
            descriptor,
            before_states,
            opened_before,
        )
        return digest.hexdigest()
    finally:
        os.close(descriptor)


def _load_legacy_receipt_compatibility_registry(
    manifest_path: Path,
) -> tuple[dict[str, dict[str, str]], list[str]]:
    try:
        payload = _strict_json_load_path(manifest_path)
    except Exception as exc:  # noqa: BLE001 - compatibility identity must fail closed
        return {}, [f"legacy receipt compatibility registry is unreadable: {manifest_path}: {exc}"]
    if not isinstance(payload, dict):
        return {}, ["legacy receipt compatibility registry is not an object"]

    issues: list[str] = []
    if set(payload) != {"Schema", "Purpose", "Receipts"}:
        issues.append("legacy receipt compatibility registry has an unexpected top-level shape")
    if payload.get("Schema") != LEGACY_RECEIPT_COMPATIBILITY_SCHEMA:
        issues.append("legacy receipt compatibility registry has an invalid Schema")
    if payload.get("Purpose") != LEGACY_RECEIPT_PURPOSE:
        issues.append("legacy receipt compatibility registry has an invalid Purpose")

    rows = payload.get("Receipts")
    if not isinstance(rows, list):
        return {}, [*issues, "legacy receipt compatibility registry has no Receipts list"]

    registry: dict[str, dict[str, str]] = {}
    seen_hashes: set[str] = set()
    seen_profiles: set[str] = set()
    required_row_fields = {
        "Audit Path",
        "SHA256",
        "Compatibility Profile",
        "Receipt Class",
        "Immutable Purpose",
    }
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or set(row) != required_row_fields:
            issues.append(f"legacy receipt compatibility row {index} has an invalid shape")
            continue
        path_parts = _safe_external_relative_parts(row.get("Audit Path"))
        if (
            not path_parts
            or len(path_parts) != 2
            or path_parts[0].casefold() != "audit_log"
            or not path_parts[1].casefold().endswith(".json")
        ):
            issues.append(f"legacy receipt compatibility row {index} has an invalid Audit Path")
            continue
        normalized_path = "/".join(path_parts)
        path_key = _host_path_key(normalized_path)
        digest = str(row.get("SHA256", ""))
        digest_key = digest.casefold()
        profile = str(row.get("Compatibility Profile", ""))
        if not SHA256_PATTERN.fullmatch(digest):
            issues.append(f"legacy receipt compatibility row {index} has an invalid SHA256")
        if profile not in LEGACY_COMPLETION_PROFILES:
            issues.append(
                f"legacy receipt compatibility row {index} has an unknown Compatibility Profile"
            )
        if row.get("Receipt Class") != LEGACY_RECEIPT_CLASS:
            issues.append(f"legacy receipt compatibility row {index} has an invalid Receipt Class")
        if row.get("Immutable Purpose") != LEGACY_RECEIPT_PURPOSE:
            issues.append(f"legacy receipt compatibility row {index} has an invalid Immutable Purpose")
        if path_key in registry:
            issues.append(f"legacy receipt compatibility registry duplicates path {normalized_path}")
        if digest_key in seen_hashes:
            issues.append(f"legacy receipt compatibility registry duplicates SHA256 {digest}")
        if profile in seen_profiles:
            issues.append(f"legacy receipt compatibility registry duplicates profile {profile}")
        registry[path_key] = {
            "Audit Path": normalized_path,
            "SHA256": digest_key,
            "Compatibility Profile": profile,
        }
        seen_hashes.add(digest_key)
        seen_profiles.add(profile)

    expected_profiles = set(LEGACY_COMPLETION_PROFILES)
    if len(rows) != 3 or seen_profiles != expected_profiles:
        issues.append(
            "legacy receipt compatibility registry must bind exactly the three immutable profiles"
        )
    return ({}, issues) if issues else (registry, [])


def _validate_legacy_receipt_identity(
    root: Path,
    audit_path: Path,
    manifest_path: Path,
    actual_digest: str,
) -> tuple[str | None, list[str]]:
    registry, registry_issues = _load_legacy_receipt_compatibility_registry(manifest_path)
    if registry_issues:
        return None, registry_issues
    try:
        relative_path = audit_path.resolve(strict=True).relative_to(root.resolve(strict=True)).as_posix()
    except (OSError, ValueError):
        return None, ["legacy receipt audit path is outside the external-state root"]
    path_parts = _safe_external_relative_parts(relative_path)
    if not path_parts:
        return None, ["legacy receipt audit path is unsafe"]
    normalized_path = "/".join(path_parts)
    entry = registry.get(_host_path_key(normalized_path))
    if entry is None:
        return None, [
            "state-less target-set record is not an admitted immutable receipt path: "
            + normalized_path
        ]
    profile = entry["Compatibility Profile"]
    if actual_digest.casefold() != entry["SHA256"]:
        return profile, [
            "legacy receipt SHA256 does not match its admitted immutable identity: "
            + normalized_path
        ]
    return profile, []


def _normalized_legacy_assignment_value(value: str) -> str:
    return " ".join(value.casefold().split())


def _legacy_completion_profile(values: dict[str, str]) -> str | None:
    for profile_name, profile in LEGACY_COMPLETION_PROFILES.items():
        if all(values.get(field) == profile[field] for field in LEGACY_REQUIRED_COMPLETION_FIELDS):
            final_disposition = values.get("final disposition")
            if final_disposition is None or final_disposition == profile["final disposition"]:
                return profile_name
    return None


def _validate_legacy_completion_evidence(
    rows: list[object],
    expected_profile: str | None,
) -> list[str]:
    issues: list[str] = []
    live_profiles: list[tuple[int, str]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        post_record_state = row.get("Post Record State", "live")
        if not isinstance(post_record_state, str) or post_record_state not in {
            "live",
            "historical-receipt",
        }:
            issues.append(
                f"legacy receipt target row {index} has invalid Post Record State"
            )
            post_record_state = "live"

        assignments = row.get("Assignments")
        if not isinstance(assignments, list):
            continue
        parsed: dict[str, str] = {}
        malformed = False
        for raw_assignment in assignments:
            if not isinstance(raw_assignment, str) or "=" not in raw_assignment:
                issues.append(
                    f"legacy receipt target row {index} has malformed or ambiguous assignment"
                )
                malformed = True
                continue
            field, value = raw_assignment.split("=", 1)
            normalized_field = field.strip().casefold()
            normalized_value = _normalized_legacy_assignment_value(value)
            if not normalized_field or not normalized_value:
                issues.append(
                    f"legacy receipt target row {index} has malformed or ambiguous assignment"
                )
                malformed = True
                continue
            if normalized_field in parsed:
                issues.append(
                    f"legacy receipt target row {index} duplicates assignment field {field.strip()!r}"
                )
                malformed = True
                continue
            parsed[normalized_field] = normalized_value

        completion_values = {
            field: parsed[field]
            for field in LEGACY_COMPLETION_FIELDS
            if field in parsed
        }
        if post_record_state == "historical-receipt":
            if completion_values:
                issues.append(
                    f"legacy receipt historical target row {index} carries live completion evidence"
                )
            continue
        missing_fields = sorted(LEGACY_REQUIRED_COMPLETION_FIELDS - completion_values.keys())
        if missing_fields:
            issues.append(
                f"legacy receipt live target row {index} lacks completion field(s): "
                + ", ".join(missing_fields)
            )
            continue
        if malformed:
            continue
        profile = _legacy_completion_profile(completion_values)
        if profile is None:
            issues.append(
                f"legacy receipt live target row {index} has no exact accepted completion profile"
            )
            continue
        if expected_profile is not None and profile != expected_profile:
            issues.append(
                f"legacy receipt live target row {index} uses profile {profile!r}, "
                f"expected {expected_profile!r}"
            )
            continue
        live_profiles.append((index, profile))

    if not live_profiles:
        issues.append("legacy receipt has no live target row with exact completion evidence")
    elif len({profile for _, profile in live_profiles}) != 1:
        issues.append("legacy receipt completion profiles disagree across its live target set")
    return issues


def _snapshot_physical_inventory(
    snapshot_path: Path,
    *,
    evidence_label: str,
) -> tuple[set[str], list[str]]:
    physical_snapshot_files: set[str] = set()
    inventory_issues: list[str] = []
    snapshot_walk_errors: list[OSError] = []

    def record_snapshot_walk_error(error: OSError) -> None:
        snapshot_walk_errors.append(error)

    for current_root, directory_names, file_names in os.walk(
        snapshot_path,
        followlinks=False,
        onerror=record_snapshot_walk_error,
    ):
        current_path = Path(current_root)
        for directory_name in tuple(directory_names):
            directory_path = current_path / directory_name
            if _has_reparse_point(directory_path):
                inventory_issues.append(
                    f"{evidence_label} snapshot contains an unconfined reparse directory: "
                    f"{directory_path.relative_to(snapshot_path).as_posix()}"
                )
                directory_names.remove(directory_name)
        for file_name in file_names:
            file_path = current_path / file_name
            relative_file = file_path.relative_to(snapshot_path).as_posix()
            if relative_file == "snapshot_manifest.json":
                continue
            if _has_reparse_point(file_path):
                inventory_issues.append(
                    f"{evidence_label} snapshot contains an unconfined reparse file: "
                    f"{relative_file}"
                )
                continue
            physical_snapshot_files.add(_host_path_key(relative_file))
    inventory_issues.extend(
        f"{evidence_label} snapshot traversal failed: {error}"
        for error in snapshot_walk_errors
    )
    return physical_snapshot_files, inventory_issues


def _validate_snapshot_evidence(
    root: Path,
    snapshot: object,
    target_before_hashes: dict[str, str],
    *,
    evidence_label: str,
    transaction_updated: object | None = None,
) -> list[str]:
    issues: list[str] = []
    snapshot_parts = _safe_external_relative_parts(snapshot)
    if (
        not snapshot_parts
        or len(snapshot_parts) != 2
        or _host_path_key(snapshot_parts[0]) != _host_path_key("snapshots")
    ):
        return [
            f"{evidence_label} Snapshot is not a safe isolated snapshots/<snapshot-id> path"
        ]
    try:
        snapshot_path, snapshot_before_states = _confined_component_states(
            root,
            snapshot_parts,
        )
        if not stat.S_ISDIR(snapshot_before_states[-1].st_mode):
            raise OSError("snapshot evidence path is not a directory")
    except OSError as exc:
        return [f"{evidence_label} snapshot directory is missing or unconfined: {exc}"]
    try:
        manifest_path, manifest, manifest_digest = _strict_json_load_confined_with_digest(
            root,
            (*snapshot_parts, "snapshot_manifest.json"),
        )
    except Exception as exc:  # noqa: BLE001 - corrupt provenance must fail closed
        return [f"{evidence_label} snapshot manifest is missing, unconfined, or malformed: {exc}"]
    if not isinstance(manifest, dict):
        return [f"{evidence_label} snapshot manifest is not an object: {manifest_path}"]
    if manifest_path.parent != snapshot_path:
        return [f"{evidence_label} snapshot directory changed before manifest validation"]
    if manifest.get("External State Schema") != DEFAULT_SCHEMA_VERSION:
        issues.append(f"{evidence_label} snapshot manifest schema is not external-state-v1")
    manifest_updated = _canonical_utc_datetime(manifest.get("Last Updated"))
    if manifest_updated is None:
        issues.append(f"{evidence_label} snapshot manifest Last Updated is not canonical UTC")
    transaction_timestamp = _canonical_utc_datetime(transaction_updated)
    if (
        manifest_updated is not None
        and transaction_timestamp is not None
        and manifest_updated > transaction_timestamp
    ):
        issues.append(f"{evidence_label} snapshot manifest postdates the transaction")
    manifest_root = manifest.get("Root")
    try:
        manifest_root_path = Path(manifest_root) if isinstance(manifest_root, str) else None
        root_key = _host_path_key(str(root.resolve(strict=False)))
        manifest_root_key = (
            _host_path_key(str(manifest_root_path.resolve(strict=False)))
            if manifest_root_path is not None
            and manifest_root.strip() == manifest_root
            and manifest_root_path.is_absolute()
            else ""
        )
    except (OSError, RuntimeError, ValueError):
        manifest_root_key = ""
    if not manifest_root_key or manifest_root_key != root_key:
        issues.append(
            f"{evidence_label} snapshot manifest Root does not match the current external-state root"
        )
    copied_files = manifest.get("Copied Files")
    if not isinstance(copied_files, list) or not copied_files:
        issues.append(f"{evidence_label} snapshot manifest has no copied-file evidence")
        return issues
    copied_hashes: dict[str, str] = {}
    copied_paths: dict[str, tuple[str, ...]] = {}
    for row in copied_files:
        if not isinstance(row, dict):
            issues.append(f"{evidence_label} snapshot manifest contains a malformed copied-file row")
            continue
        relative_parts = _safe_external_relative_parts(row.get("path"))
        relative = "/".join(relative_parts or ())
        relative_key = _host_path_key(relative)
        digest_value = row.get("sha256")
        digest = digest_value if isinstance(digest_value, str) else ""
        if not relative_parts or not SHA256_PATTERN.fullmatch(digest):
            issues.append(f"{evidence_label} snapshot manifest contains invalid path/hash evidence")
            continue
        try:
            snapshot_digest = _sha256_confined_evidence_file(
                root,
                (*snapshot_parts, *relative_parts),
            )
        except OSError as exc:
            issues.append(
                f"{evidence_label} snapshot copy is unreadable for {relative}: {exc}"
            )
            continue
        if snapshot_digest.casefold() != digest.casefold():
            issues.append(
                f"{evidence_label} snapshot copy is missing or disagrees with its manifest for "
                f"{relative}"
            )
            continue
        if relative_key in copied_hashes:
            issues.append(f"{evidence_label} snapshot manifest duplicates target {relative}")
            continue
        copied_hashes[relative_key] = digest.casefold()
        copied_paths[relative_key] = relative_parts
    for relative, before_hash in target_before_hashes.items():
        if copied_hashes.get(_host_path_key(relative)) != before_hash.casefold():
            issues.append(
                f"{evidence_label} Before SHA256 does not match its snapshot manifest for "
                f"{relative}"
            )
    expected_snapshot_targets = {
        _host_path_key(relative) for relative in target_before_hashes
    }
    unexpected_snapshot_targets = sorted(
        set(copied_hashes) - expected_snapshot_targets
    )
    if unexpected_snapshot_targets:
        issues.append(
            f"{evidence_label} snapshot manifest contains unexpected files outside "
            "the journal target set: " + ", ".join(unexpected_snapshot_targets)
        )
    physical_snapshot_files, inventory_issues = _snapshot_physical_inventory(
        snapshot_path,
        evidence_label=evidence_label,
    )
    issues.extend(inventory_issues)
    try:
        snapshot_after_path, snapshot_after_states = _confined_component_states(
            root,
            snapshot_parts,
        )
        snapshot_identity_changed = (
            snapshot_after_path != snapshot_path
            or len(snapshot_after_states) != len(snapshot_before_states)
            or any(
                not os.path.samestat(before_state, after_state)
                for before_state, after_state in zip(
                    snapshot_before_states,
                    snapshot_after_states,
                )
            )
        )
    except OSError:
        snapshot_identity_changed = True
    if snapshot_identity_changed:
        issues.append(f"{evidence_label} snapshot directory changed during validation")
    for relative_key, digest in copied_hashes.items():
        try:
            revalidated_digest = _sha256_confined_evidence_file(
                root,
                (*snapshot_parts, *copied_paths[relative_key]),
            )
        except OSError as exc:
            issues.append(
                f"{evidence_label} snapshot copy changed after inventory for "
                f"{relative_key}: {exc}"
            )
            continue
        if revalidated_digest.casefold() != digest:
            issues.append(
                f"{evidence_label} snapshot copy changed after inventory for {relative_key}"
            )
    try:
        revalidated_manifest_digest = _sha256_confined_evidence_file(
            root,
            (*snapshot_parts, "snapshot_manifest.json"),
        )
    except OSError as exc:
        issues.append(
            f"{evidence_label} snapshot manifest changed after inventory: {exc}"
        )
    else:
        if revalidated_manifest_digest.casefold() != manifest_digest.casefold():
            issues.append(f"{evidence_label} snapshot manifest changed after inventory")
    revalidated_snapshot_files, revalidated_inventory_issues = (
        _snapshot_physical_inventory(
            snapshot_path,
            evidence_label=evidence_label,
        )
    )
    issues.extend(revalidated_inventory_issues)
    if revalidated_snapshot_files != physical_snapshot_files:
        issues.append(f"{evidence_label} snapshot inventory changed after hashing")
    unmanifested_snapshot_files = sorted(
        revalidated_snapshot_files - set(copied_hashes)
    )
    if unmanifested_snapshot_files:
        issues.append(
            f"{evidence_label} snapshot contains unmanifested files: "
            + ", ".join(unmanifested_snapshot_files)
        )
    return issues


def _validate_legacy_snapshot_evidence(
    root: Path,
    snapshot: object,
    target_before_hashes: dict[str, str],
    transaction_updated: object,
) -> list[str]:
    return _validate_snapshot_evidence(
        root,
        snapshot,
        target_before_hashes,
        evidence_label="legacy receipt",
        transaction_updated=transaction_updated,
    )


def _validate_modern_snapshot_evidence(
    root: Path,
    snapshot: object,
    target_before_hashes: dict[str, str],
    transaction_updated: object,
) -> list[str]:
    return _validate_snapshot_evidence(
        root,
        snapshot,
        target_before_hashes,
        evidence_label="modern Committed journal",
        transaction_updated=transaction_updated,
    )


def _validate_legacy_lock_evidence(
    root: Path,
    audit_path: Path,
    lock_id: object,
    workload_id: object,
    snapshot: object,
    targets: set[str],
    transaction_updated: object,
) -> list[str]:
    issues: list[str] = []
    lock_text = str(lock_id or "").strip()
    workload_text = str(workload_id or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", lock_text):
        return ["legacy receipt Lock ID is missing or unsafe"]
    if not workload_text:
        return ["legacy receipt Workload ID is missing"]
    try:
        lock_path, lock, lock_digest = _strict_json_load_confined_with_digest(
            root,
            ("locks", f"{lock_text}.json"),
        )
    except Exception as exc:  # noqa: BLE001 - ambiguous lock evidence must fail closed
        return [f"legacy receipt lock evidence is missing, unconfined, or malformed: {exc}"]
    if not isinstance(lock, dict):
        return [f"legacy receipt lock evidence is not an object: {lock_path}"]
    expected_values = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Lock ID": lock_text,
        "Lock State": "Released",
        "Workload ID": workload_text,
        "Workload State": "Completed",
        "Retain Between Workloads": "No",
    }
    for field, expected in expected_values.items():
        if str(lock.get(field, "")).strip() != expected:
            issues.append(
                f"legacy receipt lock evidence has {field}={lock.get(field)!r}, expected {expected!r}"
            )
    released_timestamp = _canonical_utc_datetime(lock.get("Released At"))
    if released_timestamp is None:
        issues.append(
            "legacy receipt lock evidence has no canonical UTC Released At timestamp"
        )
    transaction_timestamp = _canonical_utc_datetime(transaction_updated)
    if (
        released_timestamp is not None
        and transaction_timestamp is not None
        and released_timestamp < transaction_timestamp
    ):
        issues.append("legacy receipt lock evidence was released before the transaction")
    write_set_value = lock.get("Intended Write Set")
    write_set: set[str] = set()
    if not isinstance(write_set_value, str):
        issues.append("legacy receipt lock evidence has malformed Intended Write Set")
    else:
        for item in write_set_value.split(";"):
            if not item:
                continue
            if item != item.strip():
                issues.append(
                    "legacy receipt lock evidence has whitespace-padded Intended Write Set entry"
                )
                continue
            parts = _safe_external_relative_parts(item)
            if not parts:
                issues.append("legacy receipt lock evidence has unsafe Intended Write Set entry")
                continue
            normalized = _host_path_key("/".join(parts))
            if normalized in write_set:
                issues.append(
                    "legacy receipt lock evidence duplicates Intended Write Set entry "
                    f"{item}"
                )
                continue
            write_set.add(normalized)
    try:
        audit_relative = audit_path.relative_to(root).as_posix()
    except ValueError:
        audit_relative = ""
    snapshot_parts = _safe_external_relative_parts(snapshot)
    snapshot_relative = _host_path_key("/".join(snapshot_parts or ()))
    required_write_set = {
        _host_path_key(audit_relative),
        snapshot_relative,
        *(_host_path_key(target) for target in targets),
    }
    expected_write_set = {item for item in required_write_set if item}
    missing = sorted(expected_write_set - write_set)
    if missing:
        issues.append(
            "legacy receipt lock write set omits receipt evidence: " + ", ".join(missing)
        )
    unexpected = sorted(write_set - expected_write_set)
    if unexpected:
        issues.append(
            "legacy receipt lock write set contains unexpected evidence: "
            + ", ".join(unexpected)
        )
    try:
        revalidated_lock_digest = _sha256_confined_evidence_file(
            root,
            ("locks", f"{lock_text}.json"),
        )
    except OSError as exc:
        issues.append(f"legacy receipt lock evidence changed during validation: {exc}")
    else:
        if revalidated_lock_digest.casefold() != lock_digest.casefold():
            issues.append("legacy receipt lock evidence changed during validation")
    return issues


def _validate_legacy_completed_target_set_receipt(
    root: Path,
    path: Path,
    payload: dict[str, object],
    compatibility_manifest_path: Path,
    actual_digest: str,
) -> list[str]:
    issues: list[str] = []
    compatibility_profile, identity_issues = _validate_legacy_receipt_identity(
        root,
        path,
        compatibility_manifest_path,
        actual_digest,
    )
    issues.extend(identity_issues)
    if set(payload) != LEGACY_TARGET_SET_RECEIPT_FIELDS:
        issues.append("state-less record does not have the exact legacy completed-receipt fields")
    if payload.get("External State Schema") != DEFAULT_SCHEMA_VERSION:
        issues.append("legacy receipt schema is not external-state-v1")
    if payload.get("Transition") != TARGET_SET_TRANSITION:
        issues.append("legacy receipt transition identity is invalid")
    for field in ("Last Updated", "Last Updated By", "Lock ID", "Snapshot", "Workload ID"):
        if not str(payload.get(field, "")).strip():
            issues.append(f"legacy receipt is missing {field}")
    transaction_updated = payload.get("Last Updated")
    if _canonical_utc_datetime(transaction_updated) is None:
        issues.append("legacy receipt Last Updated is not canonical UTC")

    rows = payload.get("Targets")
    target_before_hashes: dict[str, str] = {}
    if not isinstance(rows, list) or not rows:
        issues.append("legacy receipt has no target rows")
        return issues
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            issues.append(f"legacy receipt target row {index} is not an object")
            continue
        row_fields = set(row)
        if not LEGACY_TARGET_ROW_FIELDS.issubset(row_fields) or not row_fields.issubset(
            LEGACY_TARGET_ROW_FIELDS | LEGACY_TARGET_ROW_OPTIONAL_FIELDS
        ):
            issues.append(f"legacy receipt target row {index} has a non-legacy field shape")
        if "Before Text" in row or any("recover" in str(key).casefold() for key in row):
            issues.append(f"legacy receipt target row {index} contains recovery payload")
        relative_parts = _safe_external_relative_parts(row.get("Target"))
        relative = "/".join(relative_parts or ())
        if not relative_parts:
            issues.append(f"legacy receipt target row {index} has an unsafe target path")
        elif _host_path_key(relative) in target_before_hashes:
            issues.append(f"legacy receipt duplicates target {relative}")
        before_hash = str(row.get("Before SHA256", ""))
        after_hash = str(row.get("After SHA256", ""))
        if not SHA256_PATTERN.fullmatch(before_hash) or not SHA256_PATTERN.fullmatch(after_hash):
            issues.append(f"legacy receipt target row {index} has malformed hash evidence")
        elif before_hash.casefold() == after_hash.casefold():
            issues.append(f"legacy receipt target row {index} has no before/after transition")
        if relative_parts:
            target_before_hashes[_host_path_key(relative)] = before_hash
        for list_field in ("Additions", "Assignments", "Section Renames"):
            value = row.get(list_field)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                issues.append(f"legacy receipt target row {index} has malformed {list_field}")

    issues.extend(_validate_legacy_completion_evidence(rows, compatibility_profile))

    if target_before_hashes:
        issues.extend(
            _validate_legacy_snapshot_evidence(
                root,
                payload.get("Snapshot"),
                target_before_hashes,
                transaction_updated,
            )
        )
        issues.extend(
            _validate_legacy_lock_evidence(
                root,
                path,
                payload.get("Lock ID"),
                payload.get("Workload ID"),
                payload.get("Snapshot"),
                set(target_before_hashes),
                transaction_updated,
            )
        )
    return issues


def _contains_recovery_payload_field(value: object) -> bool:
    pending = [value]
    while pending:
        current = pending.pop()
        if isinstance(current, dict):
            for key, nested in current.items():
                if isinstance(key, str):
                    key_with_word_boundaries = re.sub(
                        r"(?<=[a-z0-9])(?=[A-Z])",
                        " ",
                        key,
                    )
                    normalized_key = re.sub(
                        r"[-_/]+",
                        " ",
                        key_with_word_boundaries.casefold(),
                    ).strip()
                    if (
                        normalized_key == "before text"
                        or any(
                            marker in normalized_key
                            for marker in ("recovery", "rollback", "pre write", "prewrite")
                        )
                        or (
                            "original target" in normalized_key
                            and any(
                                payload_term in normalized_key
                                for payload_term in ("data", "text", "content", "payload", "copy")
                            )
                        )
                        or (
                            bool(
                                set(normalized_key.split())
                                & {
                                    "archive",
                                    "archived",
                                    "backup",
                                    "backups",
                                    "old",
                                    "original",
                                    "previous",
                                    "prior",
                                    "restore",
                                    "revert",
                                    "saved",
                                    "undo",
                                }
                            )
                            and any(
                                payload_term in normalized_key
                                for payload_term in (
                                    "bytes",
                                    "data",
                                    "file",
                                    "text",
                                    "content",
                                    "payload",
                                    "copy",
                                    "snapshot",
                                    "state",
                                    "value",
                                )
                            )
                        )
                    ):
                        return True
                pending.append(nested)
        elif isinstance(current, list):
            pending.extend(current)
    return False


def _validate_modern_target_set_journal(
    payload: dict[str, object],
    target_before_hashes: dict[str, str] | None = None,
    target_after_hashes: dict[str, str] | None = None,
) -> list[str]:
    issues: list[str] = []
    before_hashes = target_before_hashes if target_before_hashes is not None else {}
    after_hashes = target_after_hashes if target_after_hashes is not None else {}
    if payload.get("External State Schema") != DEFAULT_SCHEMA_VERSION:
        issues.append("modern target-set transaction journal has an invalid Schema")
    if payload.get("Transition") != TARGET_SET_TRANSITION:
        issues.append("modern target-set transaction journal has an invalid Transition")
    last_updated = payload.get("Last Updated")
    if not _is_canonical_utc_timestamp(last_updated):
        issues.append(
            "modern target-set transaction journal has no canonical Last Updated timestamp"
        )
    last_updated_by = payload.get("Last Updated By")
    if not isinstance(last_updated_by, str) or not last_updated_by.strip():
        issues.append("modern target-set transaction journal is missing Last Updated By")
    state = payload.get("Transaction State")
    if not isinstance(state, str) or not state.strip():
        return [*issues, "modern target-set transaction journal has missing or blank Transaction State"]
    if state == "Prepared":
        return [*issues, "incomplete target-set transaction journal requires locked recovery"]
    if state != "Committed":
        return [*issues, f"target-set transaction journal has invalid state {state!r}"]
    if _contains_recovery_payload_field(payload):
        issues.append("modern Committed journal retains recoverable Before Text")
    for field in ("Lock ID", "Workload ID", "Snapshot"):
        if not str(payload.get(field, "")).strip():
            issues.append(f"modern Committed journal is missing {field}")
    rows = payload.get("Targets")
    if not isinstance(rows, list) or not rows:
        return [*issues, "modern Committed journal has no target rows"]
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            issues.append(f"modern Committed journal target row {index} is not an object")
            continue
        relative_parts = _safe_external_relative_parts(row.get("Target"))
        relative = "/".join(relative_parts or ())
        relative_key = _host_path_key(relative)
        target_is_unique = bool(relative_parts) and relative_key not in seen
        if not target_is_unique:
            issues.append(f"modern Committed journal target row {index} has unsafe/duplicate target")
        else:
            seen.add(relative_key)
        normalized_hashes: dict[str, str] = {}
        for hash_field in ("Before SHA256", "After SHA256"):
            value = row.get(hash_field)
            if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
                issues.append(
                    f"modern Committed journal target row {index} has malformed {hash_field}"
                )
            else:
                normalized_hashes[hash_field] = value.casefold()
        if target_is_unique and "Before SHA256" in normalized_hashes:
            before_hashes[relative_key] = normalized_hashes["Before SHA256"]
        if target_is_unique and "After SHA256" in normalized_hashes:
            after_hashes[relative] = normalized_hashes["After SHA256"]
        if (
            len(normalized_hashes) == 2
            and normalized_hashes["Before SHA256"] == normalized_hashes["After SHA256"]
        ):
            issues.append(
                f"modern Committed journal target row {index} has no before/after transition"
            )
    return issues


def _validate_modern_committed_target_evidence(
    root: Path,
    target_after_hashes: dict[str, str],
) -> list[str]:
    issues: list[str] = []
    for relative, expected_digest in target_after_hashes.items():
        relative_parts = _safe_external_relative_parts(relative)
        if not relative_parts:
            issues.append(
                f"modern Committed journal target has an unsafe live path: {relative}"
            )
            continue
        try:
            actual_digest = _sha256_confined_evidence_file(root, relative_parts)
        except OSError as exc:
            issues.append(
                f"modern Committed journal live target is missing or unconfined for "
                f"{relative}: {exc}"
            )
            continue
        if actual_digest.casefold() != expected_digest.casefold():
            issues.append(
                f"modern Committed journal live target does not match After SHA256 for "
                f"{relative}"
            )
    return issues


def _validate_modern_lock_evidence(
    root: Path,
    audit_path: Path,
    payload: dict[str, object],
    targets: set[str],
) -> list[str]:
    lock_id = payload.get("Lock ID")
    workload_id = payload.get("Workload ID")
    if not isinstance(lock_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", lock_id):
        return ["modern Committed journal Lock ID is missing or unsafe"]
    if not isinstance(workload_id, str) or not workload_id.strip():
        return ["modern Committed journal Workload ID is missing"]
    if workload_id != workload_id.strip():
        return ["modern Committed journal Workload ID is not canonical"]
    try:
        lock_path, lock, lock_digest = _strict_json_load_confined_with_digest(
            root,
            ("locks", f"{lock_id}.json"),
        )
    except Exception as exc:  # noqa: BLE001 - ambiguous lock evidence must fail closed
        return [f"modern Committed journal lock evidence is missing, unconfined, or malformed: {exc}"]
    if not isinstance(lock, dict):
        return [f"modern Committed journal lock evidence is not an object: {lock_path}"]

    issues: list[str] = []
    expected_values = {
        "External State Schema": DEFAULT_SCHEMA_VERSION,
        "Lock ID": lock_id,
        "Lock State": "Released",
        "Workload ID": workload_id,
        "Workload State": "Completed",
        "Retain Between Workloads": "No",
    }
    for field, expected in expected_values.items():
        actual = lock.get(field)
        if not isinstance(actual, str) or actual != expected:
            issues.append(
                f"modern Committed journal lock evidence has {field}={lock.get(field)!r}, "
                f"expected {expected!r}"
            )
    released_at = lock.get("Released At")
    released_timestamp = _canonical_utc_datetime(released_at)
    if released_timestamp is None:
        issues.append(
            "modern Committed journal lock evidence has no canonical UTC Released At timestamp"
        )
    transaction_timestamp = _canonical_utc_datetime(payload.get("Last Updated"))
    if (
        released_timestamp is not None
        and transaction_timestamp is not None
        and released_timestamp < transaction_timestamp
    ):
        issues.append(
            "modern Committed journal lock evidence was released before the transaction"
        )
    write_set_value = lock.get("Intended Write Set")
    write_set: set[str] = set()
    if not isinstance(write_set_value, str):
        issues.append("modern Committed journal lock evidence has malformed Intended Write Set")
    else:
        for item in write_set_value.split(";"):
            if not item:
                continue
            if item != item.strip():
                issues.append(
                    "modern Committed journal lock evidence has whitespace-padded "
                    "Intended Write Set entry"
                )
                continue
            parts = _safe_external_relative_parts(item)
            if not parts:
                issues.append(
                    "modern Committed journal lock evidence has unsafe Intended Write Set entry"
                )
                continue
            normalized = _host_path_key("/".join(parts))
            if normalized in write_set:
                issues.append(
                    "modern Committed journal lock evidence duplicates Intended Write Set entry "
                    f"{item}"
                )
                continue
            write_set.add(normalized)
    try:
        audit_relative = _host_path_key(audit_path.relative_to(root).as_posix())
    except ValueError:
        audit_relative = ""
    snapshot_parts = _safe_external_relative_parts(payload.get("Snapshot"))
    snapshot_relative = _host_path_key("/".join(snapshot_parts or ()))
    required_write_set = {
        audit_relative,
        snapshot_relative,
        *(_host_path_key(target) for target in targets),
    }
    expected_write_set = {item for item in required_write_set if item}
    missing = sorted(expected_write_set - write_set)
    if missing:
        issues.append(
            "modern Committed journal lock write set omits journal evidence: "
            + ", ".join(missing)
        )
    unexpected = sorted(write_set - expected_write_set)
    if unexpected:
        issues.append(
            "modern Committed journal lock write set contains unexpected evidence: "
            + ", ".join(unexpected)
        )
    try:
        revalidated_lock_digest = _sha256_confined_evidence_file(
            root,
            ("locks", f"{lock_id}.json"),
        )
    except OSError as exc:
        issues.append(
            f"modern Committed journal lock evidence changed during validation: {exc}"
        )
    else:
        if revalidated_lock_digest.casefold() != lock_digest.casefold():
            issues.append(
                "modern Committed journal lock evidence changed during validation"
            )
    return issues


def _tolerant_json_string_end(text: str, start: int) -> int:
    """Skip one JSON-like string without treating invalid escapes as structure."""

    index = start + 1
    while index < len(text):
        character = text[index]
        if character == "\\":
            index += 2
            continue
        if character == '"':
            return index + 1
        index += 1
    return len(text)


def _first_structural_json_object_start(text: str) -> int:
    index = 0
    while index < len(text):
        if text[index] == '"':
            index = _tolerant_json_string_end(text, index)
            continue
        if text[index] == "{":
            return index
        index += 1
    return -1


def _tolerant_json_member_starts_at(text: str, start: int) -> bool:
    """Return whether text after a comma can begin a JSON object member."""

    cursor = start
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor >= len(text) or text[cursor] != '"':
        return False
    key_end = _tolerant_json_string_end(text, cursor)
    if key_end > len(text) or key_end == 0 or text[key_end - 1] != '"':
        return False
    cursor = key_end
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    return cursor < len(text) and text[cursor] == ":"


def _tolerant_json_member_continuation(text: str, start: int) -> int:
    """Resume at the next apparent root-member delimiter after malformed syntax."""

    index = start
    first_closing_brace: int | None = None
    # The caller is recovering a malformed value inside the root object. Keep that
    # root as an immutable sentinel so malformed nested closers cannot consume it.
    nested_stack: list[str] = ["{"]
    nested_has_content: list[bool] = [True]
    while index < len(text):
        character = text[index]
        if character == '"':
            index = _tolerant_json_string_end(text, index)
            if nested_has_content:
                nested_has_content[-1] = True
            continue
        if character in "{[":
            if nested_has_content:
                nested_has_content[-1] = True
            nested_stack.append(character)
            nested_has_content.append(False)
            index += 1
            continue
        if character in "}]":
            expected = "{" if character == "}" else "["
            if nested_stack and nested_stack[-1] == expected:
                if len(nested_stack) == 1:
                    if character == "}" and first_closing_brace is None:
                        first_closing_brace = index
                else:
                    nested_stack.pop()
                    nested_has_content.pop()
                    nested_has_content[-1] = True
            elif nested_stack:
                matching_index = next(
                    (
                        candidate
                        for candidate in range(len(nested_stack) - 1, -1, -1)
                        if nested_stack[candidate] == expected
                    ),
                    None,
                )
                if matching_index == 0:
                    # The closer points at the immutable root through malformed
                    # nested depth. Discard one malformed child frame, never root.
                    nested_stack.pop()
                    nested_has_content.pop()
                elif matching_index is None:
                    # An unmatched closer can terminate an empty malformed
                    # container, but it cannot discard depth that already
                    # contains accountable malformed-value content.
                    if not nested_has_content[-1]:
                        nested_stack.pop()
                        nested_has_content.pop()
                else:
                    intervening_has_content = any(
                        nested_has_content[matching_index + 1 :]
                    )
                    if not intervening_has_content:
                        del nested_stack[matching_index:]
                        del nested_has_content[matching_index:]
                nested_has_content[-1] = True
            index += 1
            continue
        if character == ",":
            plausible_member = _tolerant_json_member_starts_at(text, index + 1)
            if plausible_member and (
                nested_stack == ["{"] or not nested_has_content[-1]
            ):
                return index + 1
            if nested_has_content:
                nested_has_content[-1] = False
            index += 1
            continue
        if nested_has_content and not character.isspace():
            nested_has_content[-1] = True
        index += 1
    return first_closing_brace if first_closing_brace is not None else len(text)


def _raw_text_has_target_set_transition(text: str) -> bool:
    if text.startswith("\ufeff"):
        text = text.removeprefix("\ufeff")
    decoder = json.JSONDecoder()
    first_object = _first_structural_json_object_start(text)
    if first_object < 0:
        return False
    index = first_object
    stack: list[str] = []
    awaiting_root_member = False
    while index < len(text):
        character = text[index]
        if character == "{" and stack == ["{"] and awaiting_root_member:
            # A container cannot begin an object member. Ignore the stray token so
            # malformed syntax cannot make a later root Transition look nested.
            index += 1
            continue
        if character == "[" and stack == ["{"] and awaiting_root_member:
            index += 1
            continue
        if character == "{":
            stack.append("{")
            if len(stack) == 1:
                awaiting_root_member = True
            index += 1
            continue
        if character == "[":
            stack.append("[")
            index += 1
            continue
        if character in "}]":
            expected = "{" if character == "}" else "["
            if stack and stack[-1] == expected:
                if len(stack) == 1:
                    # Keep the root frame immutable during malformed recovery. A
                    # later plausible member must remain visible after extra closers.
                    awaiting_root_member = True
                else:
                    stack.pop()
            elif len(stack) > 1:
                # Parsing already failed. Drop the innermost malformed container so a
                # later explicit root-level Transition cannot evade fail-closed recovery.
                stack.pop()
            index += 1
            continue
        if character == "," and stack == ["{"]:
            awaiting_root_member = True
            index += 1
            continue
        if character != '"':
            index += 1
            continue
        tolerant_key_end = _tolerant_json_string_end(text, index)
        try:
            key, key_end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            index = tolerant_key_end
            continue
        index = key_end
        if not isinstance(key, str) or stack != ["{"]:
            continue
        awaiting_root_member = False
        transition_key = key.strip().casefold() == "transition"
        cursor = key_end
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor >= len(text) or text[cursor] != ":":
            if transition_key:
                return True
            awaiting_root_member = True
            continue
        cursor += 1
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor >= len(text):
            if transition_key:
                return True
            continue
        if transition_key and text[cursor] != '"':
            return True
        tolerant_value_end = (
            _tolerant_json_string_end(text, cursor)
            if text[cursor] == '"'
            else cursor
        )
        try:
            value, value_end = decoder.raw_decode(text, cursor)
        except json.JSONDecodeError:
            if transition_key:
                return True
            index = (
                tolerant_value_end
                if text[cursor] == '"'
                else _tolerant_json_member_continuation(text, cursor)
            )
            if text[cursor] != '"':
                awaiting_root_member = True
            continue
        except (RecursionError, MemoryError):
            if transition_key:
                return True
            index = _tolerant_json_member_continuation(text, cursor)
            awaiting_root_member = True
            continue
        except ValueError as exc:
            if not _is_json_integer_resource_limit(exc):
                raise
            if transition_key:
                return True
            index = _tolerant_json_member_continuation(text, cursor)
            awaiting_root_member = True
            continue
        index = value_end
        if transition_key:
            if not isinstance(value, str):
                return True
            if value.strip().casefold() == TARGET_SET_TRANSITION.casefold():
                return True
        delimiter = value_end
        while delimiter < len(text) and text[delimiter].isspace():
            delimiter += 1
        if delimiter < len(text) and text[delimiter] not in ",}":
            index = (
                delimiter
                if stack == ["{"]
                and _tolerant_json_member_starts_at(text, delimiter)
                else _tolerant_json_member_continuation(text, delimiter)
            )
            awaiting_root_member = True
    return False


def _is_target_set_transaction(payload: dict[str, object]) -> bool:
    return payload.get("Transition") == TARGET_SET_TRANSITION


def _has_noncanonical_target_set_transition(payload: dict[str, object]) -> bool:
    for key, value in payload.items():
        if not isinstance(key, str) or key.strip().casefold() != "transition":
            continue
        if not isinstance(value, str):
            return True
        if value.strip().casefold() != TARGET_SET_TRANSITION.casefold():
            continue
        return key != "Transition" or value != TARGET_SET_TRANSITION
    return False


def _is_json_audit_entry(path: Path) -> bool:
    return path.suffix.casefold() == ".json"


def validate_incomplete_target_set_journals(
    root: Path,
    compatibility_manifest_path: Path = LEGACY_RECEIPT_COMPATIBILITY_MANIFEST,
) -> list[str]:
    failures: list[str] = []
    committed_target_after_hash_sets: list[dict[str, str]] = []
    committed_snapshot_evidence: list[
        tuple[object, dict[str, str], object]
    ] = []
    committed_lock_evidence: list[
        tuple[Path, dict[str, object], set[str]]
    ] = []
    audit_root = root / "audit_log"
    if _has_reparse_point(audit_root):
        return [
            "Target-set transaction audit root is not a confined regular directory: "
            f"{audit_root}"
        ]
    if os.path.lexists(audit_root) and not audit_root.exists():
        return [
            "Target-set transaction audit root is an unresolved filesystem alias: "
            f"{audit_root}"
        ]
    if not audit_root.exists():
        return [
            "Target-set transaction audit root is missing from the initialized "
            f"external-state scaffold: {audit_root}"
        ]
    if not audit_root.is_dir():
        return [
            "Target-set transaction audit root is not a confined regular directory: "
            f"{audit_root}"
        ]
    try:
        audit_path_before, audit_before_states = _confined_component_states(
            root,
            ("audit_log",),
        )
    except OSError as exc:
        return [f"Target-set transaction audit root is unconfined: {audit_root}: {exc}"]
    try:
        discovered_entries = sorted(audit_root.iterdir())
    except OSError as exc:
        return [f"Target-set transaction audit root is unreadable: {audit_root}: {exc}"]
    discovered_paths = [
        path for path in discovered_entries if _is_json_audit_entry(path)
    ]
    discovered_inventory = {
        (
            _host_path_key(path.name),
            "reparse"
            if _has_reparse_point(path)
            else "directory"
            if path.is_dir()
            else "entry",
        )
        for path in discovered_entries
    }
    for discovered_entry in discovered_entries:
        if _has_reparse_point(discovered_entry):
            failures.append(
                "Target-set transaction audit root contains an unconfined filesystem "
                f"alias: {discovered_entry}"
            )
        elif discovered_entry.is_dir():
            failures.append(
                "Target-set transaction audit root contains a nested directory; "
                f"audit evidence must be flat: {discovered_entry}"
            )
    discovered_hashes: dict[str, str] = {}
    for discovered_path in discovered_paths:
        try:
            path, raw_bytes = _read_confined_evidence_file(
                root,
                ("audit_log", discovered_path.name),
            )
        except OSError as exc:
            failures.append(
                "Target-set transaction journal is not a confined regular file: "
                f"{discovered_path}: {exc}"
            )
            continue
        discovered_hashes[_host_path_key(discovered_path.name)] = hashlib.sha256(
            raw_bytes
        ).hexdigest()
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"Target-set transaction journal is not UTF-8: {path}: {exc}")
            continue
        except MemoryError:
            failures.append(
                f"Target-set transaction journal exceeds safe decoder resource limits: {path}"
            )
            continue
        try:
            payload = _strict_json_loads(text)
        except (json.JSONDecodeError, StrictJSONError) as exc:
            if _raw_text_has_target_set_transition(text):
                failures.append(
                    f"Target-set transaction journal is malformed or ambiguous: {path}: {exc}"
                )
            continue
        if not isinstance(payload, dict):
            continue
        if _has_noncanonical_target_set_transition(payload):
            failures.append(
                "Target-set transaction journal uses a noncanonical Transition key or value: "
                f"{path}"
            )
            continue
        if not _is_target_set_transaction(payload):
            continue
        if "Transaction State" in payload:
            target_before_hashes: dict[str, str] = {}
            target_after_hashes: dict[str, str] = {}
            journal_issues = _validate_modern_target_set_journal(
                payload,
                target_before_hashes,
                target_after_hashes,
            )
            state = payload.get("Transaction State")
            if isinstance(state, str) and state.strip() == "Committed":
                if target_before_hashes:
                    snapshot = payload.get("Snapshot")
                    transaction_updated = payload.get("Last Updated")
                    journal_issues.extend(
                        _validate_modern_snapshot_evidence(
                            root,
                            snapshot,
                            target_before_hashes,
                            transaction_updated,
                        )
                    )
                    committed_snapshot_evidence.append(
                        (
                            snapshot,
                            dict(target_before_hashes),
                            transaction_updated,
                        )
                    )
                journal_issues.extend(
                    _validate_modern_lock_evidence(
                        root,
                        path,
                        payload,
                        set(target_before_hashes),
                    )
                )
                committed_lock_evidence.append(
                    (
                        path,
                        dict(payload),
                        set(target_before_hashes),
                    )
                )
                journal_issues.extend(
                    _validate_modern_committed_target_evidence(
                        root,
                        target_after_hashes,
                    )
                )
                committed_target_after_hash_sets.append(dict(target_after_hashes))
        else:
            journal_issues = _validate_legacy_completed_target_set_receipt(
                root,
                path,
                payload,
                compatibility_manifest_path,
                hashlib.sha256(raw_bytes).hexdigest(),
            )
        failures.extend(f"Target-set transaction journal invalid: {path}: {issue}" for issue in journal_issues)
    rediscovered_paths: list[Path] = []
    rediscovered_inventory = discovered_inventory
    try:
        rediscovered_entries = sorted(audit_root.iterdir())
        rediscovered_paths = [
            path for path in rediscovered_entries if _is_json_audit_entry(path)
        ]
        audit_path_after, audit_after_states = _confined_component_states(
            root,
            ("audit_log",),
        )
        rediscovered_inventory = {
            (
                _host_path_key(path.name),
                "reparse"
                if _has_reparse_point(path)
                else "directory"
                if path.is_dir()
                else "entry",
            )
            for path in rediscovered_entries
        }
        audit_inventory_changed = (
            audit_path_after != audit_path_before
            or len(audit_after_states) != len(audit_before_states)
            or any(
                not os.path.samestat(before_state, after_state)
                for before_state, after_state in zip(
                    audit_before_states,
                    audit_after_states,
                )
            )
            or rediscovered_inventory != discovered_inventory
        )
    except OSError:
        audit_inventory_changed = True
    if audit_inventory_changed:
        failures.append("Target-set transaction audit inventory changed during validation")
    for discovered_path in discovered_paths:
        relative_key = _host_path_key(discovered_path.name)
        expected_digest = discovered_hashes.get(relative_key)
        if expected_digest is None:
            continue
        try:
            revalidated_digest = _sha256_confined_evidence_file(
                root,
                ("audit_log", discovered_path.name),
            )
        except OSError as exc:
            failures.append(
                "Target-set transaction audit file changed during validation: "
                f"{discovered_path}: {exc}"
            )
            continue
        if revalidated_digest.casefold() != expected_digest.casefold():
            failures.append(
                "Target-set transaction audit file changed during validation: "
                f"{discovered_path}"
            )
    try:
        final_entries = sorted(audit_root.iterdir())
        final_audit_path, final_audit_states = _confined_component_states(
            root,
            ("audit_log",),
        )
        final_inventory = {
            (
                _host_path_key(path.name),
                "reparse"
                if _has_reparse_point(path)
                else "directory"
                if path.is_dir()
                else "entry",
            )
            for path in final_entries
        }
        final_inventory_changed = (
            final_audit_path != audit_path_before
            or len(final_audit_states) != len(audit_before_states)
            or any(
                not os.path.samestat(before_state, final_state)
                for before_state, final_state in zip(
                    audit_before_states,
                    final_audit_states,
                )
            )
            or final_inventory != rediscovered_inventory
        )
    except OSError:
        final_inventory_changed = True
    if final_inventory_changed:
        failures.append(
            "Target-set transaction audit inventory changed after final hashing"
        )
    for target_after_hashes in committed_target_after_hash_sets:
        failures.extend(
            "Target-set transaction live target changed during validation: " + issue
            for issue in _validate_modern_committed_target_evidence(
                root,
                target_after_hashes,
            )
        )
    for snapshot, target_before_hashes, transaction_updated in committed_snapshot_evidence:
        failures.extend(
            "Target-set transaction snapshot changed during validation: " + issue
            for issue in _validate_modern_snapshot_evidence(
                root,
                snapshot,
                target_before_hashes,
                transaction_updated,
            )
        )
    for audit_path, payload, target_before_hashes in committed_lock_evidence:
        failures.extend(
            "Target-set transaction lock changed during validation: " + issue
            for issue in _validate_modern_lock_evidence(
                root,
                audit_path,
                payload,
                target_before_hashes,
            )
        )
    return failures


def main() -> int:
    args = build_parser().parse_args()
    root = resolve_path(args.root)
    repo_paths = [resolve_path(path) for path in args.repo]
    issues = validate_canonical_root(root, repo_paths)

    print("External State Validation")
    print(f"Root: {root}")
    print(f"Root Required: {'YES' if args.require_root else 'NO'}")
    print(f"Stage 4 Records Required: {'YES' if args.require_stage4_records else 'NO'}")

    if issues:
        print("Validation Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    if not root.exists():
        print("Validation Result: External State Missing")
        if (
            args.require_root
            or args.require_stage4_records
            or args.expected_source_head
            or args.target_currentness
        ):
            print("Clean Clone Boundary: BLOCKED - required local external-state validation needs the root")
            return 1
        print("Clean Clone Boundary: PASS - missing root is not a repo validation failure")
        return 0

    if args.target_currentness:
        if args.require_stage4_records:
            print("Validation Result: BLOCKED")
            print("Target-scoped currentness cannot be combined with global Stage 4 record validation")
            return 1
        initialization_issues = validate_initialized_root(root, args.schema)
        if initialization_issues:
            print("Validation Scope: TARGET_SCOPED_CURRENTNESS")
            print("Root Manifest Posture: BLOCKED - target currentness requires an initialized external-state root")
            print("Target Currentness Validation: BLOCKED")
            for issue in initialization_issues:
                print(issue)
            return 1
        target_issues = validate_incomplete_target_set_journals(root)
        target_issues.extend(validate_target_currentness(
            root,
            args.target,
            expected_branch=args.expected_branch,
            expected_source_head=args.expected_source_head,
            expected_origin_main=args.expected_origin_main,
            expected_worktree_path=args.expected_worktree_path,
            expected_worktree_slot=args.expected_worktree_slot,
            expected_target_sha256=args.expected_target_sha256,
            expected_schema=args.schema,
        ))
        print("Validation Scope: TARGET_SCOPED_CURRENTNESS")
        print(f"Selected Target: {args.target[0] if args.target else 'MISSING'}")
        print("Root Manifest Posture: STRUCTURAL_ONLY - root initialization/index posture is reported separately and is not asserted current for this target")
        if target_issues:
            print("Target Currentness Validation: BLOCKED")
            for issue in target_issues:
                print(issue)
            return 1
        print("Target Currentness Validation: PASS")
        print("Target PASS Is Root-Wide PASS: NO")
        return 0

    manifest_path = root / "state_manifest.json"
    if not manifest_path.exists():
        issues.append("External State Corrupt: state_manifest.json missing")
    else:
        issues.extend(validate_manifest(manifest_path, args.schema))
        if args.expected_source_head:
            try:
                manifest = load_json(manifest_path)
                source_head = manifest.get("Source Repo HEAD")
                if source_head != args.expected_source_head:
                    issues.append(
                        "External State Version Conflict: expected manifest Source Repo HEAD "
                        f"{args.expected_source_head}, found {source_head or 'MISSING'}"
                    )
            except Exception as exc:  # noqa: BLE001 - duplicate manifest read for clearer source-head issue
                issues.append(f"External State Corrupt: {manifest_path}: {exc}")

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
        if not schema:
            issues.append(f"External State Corrupt: {state_file}: missing External State Schema")
            continue
        schemas.add(str(schema))
    if len(schemas) > 1 or (schemas and args.schema not in schemas):
        issues.append(
            "External State Schema Conflict: mixed or unsupported schema values found: "
            + ", ".join(sorted(schemas))
        )

    issues.extend(validate_incomplete_target_set_journals(root))

    if args.require_stage4_records:
        issues.extend(validate_stage4_records(root, args.schema, args.expected_source_head))
        issues.extend(validate_released_locks(root))
        issues.extend(validate_active_branch_plan_posture(root))
        issues.extend(validate_fam007_workstream_visual_acceptance_gate(root))

    if issues:
        print("Validation Result: BLOCKED")
        for issue in issues:
            print(issue)
        return 1

    if args.require_stage4_records:
        print("Stage 4 Migrated Record Validation: PASS")
    print("Validation Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
