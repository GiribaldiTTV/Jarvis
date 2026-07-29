from __future__ import annotations

import argparse
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
TARGET_SET_TRANSITION_FIELD_PATTERN = re.compile(
    rf'(?:^|[{{,])\s*"Transition"\s*:\s*"{re.escape(TARGET_SET_TRANSITION)}"'
)
SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
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

    if markdown_field_value(live_text, "Record Role") is None:
        failures.append(f"Target Currentness: {relative} is missing Record Role classification")
    if markdown_field_value(live_text, "Historical Receipt Boundary") is None:
        failures.append(f"Target Currentness: {relative} is missing Historical Receipt Boundary")
    return failures


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
    raw = str(value or "").strip()
    candidate = PureWindowsPath(raw)
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    if (
        not raw
        or Path(raw).is_absolute()
        or candidate.is_absolute()
        or candidate.drive
        or candidate.root
        or any(part in {"", ".", ".."} for part in parts)
        or ("/" in raw and "\\" in raw)
        or normalized.endswith("/")
        or any(":" in part for part in parts)
    ):
        return None
    return tuple(parts)


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


def _load_legacy_receipt_compatibility_registry(
    manifest_path: Path,
) -> tuple[dict[str, dict[str, str]], list[str]]:
    try:
        payload = load_json(manifest_path)
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
        path_key = normalized_path.casefold()
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
    entry = registry.get(normalized_path.casefold())
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


def _validate_legacy_snapshot_evidence(
    root: Path,
    snapshot: object,
    target_before_hashes: dict[str, str],
) -> list[str]:
    issues: list[str] = []
    snapshot_parts = _safe_external_relative_parts(snapshot)
    if not snapshot_parts or snapshot_parts[0].casefold() != "snapshots":
        return ["legacy receipt Snapshot is not a safe snapshots-relative path"]
    manifest_path = _confined_evidence_file(
        root,
        (*snapshot_parts, "snapshot_manifest.json"),
    )
    if manifest_path is None:
        return ["legacy receipt snapshot manifest is missing or escapes through a reparse point"]
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:  # noqa: BLE001 - corrupt provenance must fail closed
        return [f"legacy receipt snapshot manifest is malformed: {manifest_path}: {exc}"]
    if manifest.get("External State Schema") != DEFAULT_SCHEMA_VERSION:
        issues.append("legacy receipt snapshot manifest schema is not external-state-v1")
    copied_files = manifest.get("Copied Files")
    if not isinstance(copied_files, list) or not copied_files:
        issues.append("legacy receipt snapshot manifest has no copied-file evidence")
        return issues
    copied_hashes: dict[str, str] = {}
    for row in copied_files:
        if not isinstance(row, dict):
            issues.append("legacy receipt snapshot manifest contains a malformed copied-file row")
            continue
        relative = str(row.get("path", "")).replace("\\", "/")
        relative_key = relative.casefold()
        digest = str(row.get("sha256", ""))
        if _safe_external_relative_parts(relative) is None or not SHA256_PATTERN.fullmatch(digest):
            issues.append("legacy receipt snapshot manifest contains invalid path/hash evidence")
            continue
        snapshot_relative_parts = _safe_external_relative_parts(relative)
        snapshot_copy = _confined_evidence_file(
            manifest_path.parent,
            snapshot_relative_parts or (),
        )
        if snapshot_copy is None or sha256_file(snapshot_copy).casefold() != digest.casefold():
            issues.append(
                "legacy receipt snapshot copy is missing or disagrees with its manifest for "
                f"{relative}"
            )
            continue
        if relative_key in copied_hashes:
            issues.append(f"legacy receipt snapshot manifest duplicates target {relative}")
            continue
        copied_hashes[relative_key] = digest.casefold()
    for relative, before_hash in target_before_hashes.items():
        if copied_hashes.get(relative.casefold()) != before_hash.casefold():
            issues.append(
                "legacy receipt Before SHA256 does not match its snapshot manifest for "
                f"{relative}"
            )
    return issues


def _validate_legacy_lock_evidence(
    root: Path,
    audit_path: Path,
    lock_id: object,
    workload_id: object,
    snapshot: object,
    targets: set[str],
) -> list[str]:
    issues: list[str] = []
    lock_text = str(lock_id or "").strip()
    workload_text = str(workload_id or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", lock_text):
        return ["legacy receipt Lock ID is missing or unsafe"]
    if not workload_text:
        return ["legacy receipt Workload ID is missing"]
    lock_path = _confined_evidence_file(root, ("locks", f"{lock_text}.json"))
    if lock_path is None:
        return ["legacy receipt lock evidence is missing or escapes through a reparse point"]
    try:
        lock = load_json(lock_path)
    except Exception as exc:  # noqa: BLE001 - ambiguous lock evidence must fail closed
        return [f"legacy receipt lock evidence is malformed: {lock_path}: {exc}"]
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
    if not str(lock.get("Released At", "")).strip():
        issues.append("legacy receipt lock evidence has no Released At completion timestamp")
    write_set = {
        item.strip().replace("\\", "/").casefold()
        for item in str(lock.get("Intended Write Set", "")).split(";")
        if item.strip()
    }
    try:
        audit_relative = audit_path.relative_to(root).as_posix()
    except ValueError:
        audit_relative = ""
    required_write_set = {
        audit_relative.casefold(),
        str(snapshot or "").replace("\\", "/").casefold(),
        *(target.casefold() for target in targets),
    }
    missing = sorted(item for item in required_write_set if item and item not in write_set)
    if missing:
        issues.append(
            "legacy receipt lock write set omits receipt evidence: " + ", ".join(missing)
        )
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
        elif relative.casefold() in target_before_hashes:
            issues.append(f"legacy receipt duplicates target {relative}")
        before_hash = str(row.get("Before SHA256", ""))
        after_hash = str(row.get("After SHA256", ""))
        if not SHA256_PATTERN.fullmatch(before_hash) or not SHA256_PATTERN.fullmatch(after_hash):
            issues.append(f"legacy receipt target row {index} has malformed hash evidence")
        elif before_hash.casefold() == after_hash.casefold():
            issues.append(f"legacy receipt target row {index} has no before/after transition")
        if relative_parts:
            target_before_hashes[relative.casefold()] = before_hash
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
            )
        )
    return issues


def _validate_modern_target_set_journal(payload: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if payload.get("External State Schema") != DEFAULT_SCHEMA_VERSION:
        issues.append("modern target-set transaction journal has an invalid Schema")
    if payload.get("Transition") != TARGET_SET_TRANSITION:
        issues.append("modern target-set transaction journal has an invalid Transition")
    state = payload.get("Transaction State")
    if not isinstance(state, str) or not state.strip():
        return [*issues, "modern target-set transaction journal has missing or blank Transaction State"]
    state = state.strip()
    if state == "Prepared":
        return [*issues, "incomplete target-set transaction journal requires locked recovery"]
    if state != "Committed":
        return [*issues, f"target-set transaction journal has invalid state {state!r}"]
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
        if not relative_parts or relative.casefold() in seen:
            issues.append(f"modern Committed journal target row {index} has unsafe/duplicate target")
        else:
            seen.add(relative.casefold())
        if "Before Text" in row:
            issues.append(f"modern Committed journal target row {index} retains recoverable Before Text")
        for hash_field in ("Before SHA256", "After SHA256"):
            if not SHA256_PATTERN.fullmatch(str(row.get(hash_field, ""))):
                issues.append(
                    f"modern Committed journal target row {index} has malformed {hash_field}"
                )
    return issues


def _is_target_set_transaction(payload: dict[str, object]) -> bool:
    return payload.get("Transition") == TARGET_SET_TRANSITION


def validate_incomplete_target_set_journals(
    root: Path,
    compatibility_manifest_path: Path = LEGACY_RECEIPT_COMPATIBILITY_MANIFEST,
) -> list[str]:
    failures: list[str] = []
    audit_root = root / "audit_log"
    if not audit_root.is_dir():
        return failures
    for path in sorted(audit_root.glob("*.json")):
        try:
            raw_bytes = path.read_bytes()
        except OSError as exc:
            failures.append(f"Target-set transaction journal is unreadable: {path}: {exc}")
            continue
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"Target-set transaction journal is not UTF-8: {path}: {exc}")
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            if TARGET_SET_TRANSITION_FIELD_PATTERN.search(text):
                failures.append(f"Target-set transaction journal is malformed: {path}: {exc}")
            continue
        if not isinstance(payload, dict):
            continue
        if not _is_target_set_transaction(payload):
            continue
        if "Transaction State" in payload:
            journal_issues = _validate_modern_target_set_journal(payload)
        else:
            journal_issues = _validate_legacy_completed_target_set_receipt(
                root,
                path,
                payload,
                compatibility_manifest_path,
                hashlib.sha256(raw_bytes).hexdigest(),
            )
        failures.extend(f"Target-set transaction journal invalid: {path}: {issue}" for issue in journal_issues)
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
