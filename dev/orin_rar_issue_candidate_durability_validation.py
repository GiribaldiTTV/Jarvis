# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=rar-issue-candidate-durability-validator; status=shared
"""Validate RAR issue-candidate durability without mutating state.

The helper is intentionally read-only. It checks the packet / external-ledger /
GitHub-snapshot contract that keeps RAR issue candidates visible until they are
durably repaired, waived, rejected, routed, or reconciled.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


DECISION_SURFACE_HEADER = (
    "| Candidate ID | Owning FAM | Surface | Element Group | Defect | "
    "Evidence Pointer | Current Disposition | Progression Blocking? | "
    "Proposed Carrier | GitHub Issue | Last Verified | Exact USER Decision Needed |"
)
LEGACY_RAR_HEADER = (
    "| Issue Candidate | Owner FAM | Surface | Element Group | Defect Class | "
    "Evidence | Proposed Carrier | GitHub Issue Mutation Approved? |"
)

ACTIVE_DISPOSITIONS = {
    "ACTIVE_PENDING_USER_DECISION",
    "ACTIVE_PENDING_REPAIR",
    "ACTIVE_PENDING_GITHUB_MAPPING",
    "UNKNOWN_GITHUB_STATE",
    "STALE_GITHUB_STATE",
}
CURRENT_PACKET_DISPOSITIONS = ACTIVE_DISPOSITIONS | {
    "DEFERRED_WITH_OWNER",
    "GITHUB_CREATION_APPROVED_PENDING",
    "MAPPED_OPEN_GITHUB_ISSUE",
}
TERMINAL_DISPOSITIONS = {
    "REPAIRED_VERIFIED",
    "USER_REJECTED_WITH_REASON",
    "USER_WAIVED_WITH_REASON",
    "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED",
}
GITHUB_MAPPED_DISPOSITIONS = {
    "MAPPED_OPEN_GITHUB_ISSUE",
    "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED",
}
LEGAL_DISPOSITIONS = ACTIVE_DISPOSITIONS | {
    "REPAIRED_VERIFIED",
    "USER_REJECTED_WITH_REASON",
    "USER_WAIVED_WITH_REASON",
    "DEFERRED_WITH_OWNER",
    "ROUTED_TO_LEGAL_CARRIER",
    "GITHUB_CREATION_APPROVED_PENDING",
    "MAPPED_OPEN_GITHUB_ISSUE",
    "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED",
}
PACKETED_ONLY_PATTERNS = (
    "packeted only",
    "packet only",
    "packet-reviewed only",
    "issue candidate packet user-reviewed",
)
EMPTY_VALUES = {"", "none", "n/a", "na", "not applicable", "tbd", "todo", "unknown"}
HISTORICAL_PACKETED_ONLY_CONTEXT = (
    "previous",
    "prior",
    "historical",
    "formerly",
    "invalid",
    "not durable",
    "repaired",
    "replaced",
)
PRIMARY_REVIEW_FOLDER = "user review"
REVIEW_AIDS_FOLDER = "review aids"
SOURCE_TRUTH_CONTEXT_FOLDER = "source truth context"


@dataclass(frozen=True)
class GitHubIssueSnapshot:
    issue: str
    state: str
    source: str
    last_verified: str


@dataclass(frozen=True)
class CandidateRow:
    candidate_id: str
    owning_fam: str
    surface: str
    element_group: str
    defect: str
    evidence_pointer: str
    current_disposition: str
    progression_blocking: str
    proposed_carrier: str
    github_issue: str
    last_verified: str
    exact_user_decision: str
    source: str

    @property
    def disposition(self) -> str:
        return _normalize_token(self.current_disposition)

    @property
    def blocks_progression(self) -> bool:
        return _normalize_token(self.progression_blocking) == "YES"

    @property
    def requires_current_packet(self) -> bool:
        if self.disposition in CURRENT_PACKET_DISPOSITIONS:
            return True
        if self.blocks_progression:
            return True
        return False


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def _mentions_issue_candidate(value: str) -> bool:
    return bool(re.search(r"\bissue[-\s]+candidate\b", value, flags=re.IGNORECASE))


def _normalize_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().upper())
    token = re.sub(r"_+", "_", token).strip("_")
    aliases = {
        "REPAIRED_AND_INDEPENDENTLY_VERIFIED": "REPAIRED_VERIFIED",
        "USER_WAIVED_WITH_REASON_AND_SCOPE": "USER_WAIVED_WITH_REASON",
        "DEFERRED_WITH_DURABLE_OWNER_REASON_TARGET_CARRIER_NEXT_REVIEW_TRIGGER": "DEFERRED_WITH_OWNER",
        "DEFERRED_WITH_DURABLE_OWNER_REASON_TARGET_CARRIER_AND_NEXT_REVIEW_TRIGGER": "DEFERRED_WITH_OWNER",
        "ROUTED_TO_ANOTHER_LEGAL_CARRIER_WITH_ACCEPTANCE_RECEIPT": "ROUTED_TO_LEGAL_CARRIER",
        "APPROVED_FOR_GITHUB_ISSUE_CREATION_PENDING_MUTATION": "GITHUB_CREATION_APPROVED_PENDING",
        "MAPPED_TO_OPEN_GITHUB_ISSUE": "MAPPED_OPEN_GITHUB_ISSUE",
        "MAPPED_TO_CLOSED_GITHUB_ISSUE_AND_RECONCILED_AGAINST_REPAIR_EVIDENCE": "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED",
    }
    return aliases.get(token, token)


def _is_empty(value: str) -> bool:
    return _normalize_text(value) in EMPTY_VALUES


def _line_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _is_separator(cells: Iterable[str]) -> bool:
    cell_list = list(cells)
    return bool(cell_list) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cell_list)


def _table_rows_after_header(text: str, header: str, expected_columns: int) -> list[list[str]]:
    lines = text.splitlines()
    rows: list[list[str]] = []
    for index, line in enumerate(lines):
        if _line_cells(line) == _line_cells(header):
            if index + 1 >= len(lines):
                continue
            separator_cells = _line_cells(lines[index + 1])
            if len(separator_cells) != expected_columns or not _is_separator(separator_cells):
                continue
            for row_line in lines[index + 2 :]:
                cells = _line_cells(row_line)
                if not cells:
                    break
                rows.append(cells)
    return rows


def _candidate_from_malformed_row(source: str) -> CandidateRow:
    return CandidateRow(
        candidate_id="",
        owning_fam="",
        surface="",
        element_group="",
        defect="",
        evidence_pointer="",
        current_disposition="",
        progression_blocking="",
        proposed_carrier="",
        github_issue="",
        last_verified="",
        exact_user_decision="",
        source=source,
    )


def _legacy_row_to_candidate(cells: list[str], source: str) -> CandidateRow:
    return CandidateRow(
        candidate_id=cells[0],
        owning_fam=cells[1],
        surface=cells[2],
        element_group=cells[3],
        defect=cells[4],
        evidence_pointer=cells[5],
        current_disposition="ACTIVE_PENDING_USER_DECISION",
        progression_blocking="YES",
        proposed_carrier=cells[6],
        github_issue="PENDING" if _normalize_text(cells[7]) == "yes" else "NONE - issue mutation not approved",
        last_verified="Legacy RAR ledger import - current verification required",
        exact_user_decision=(
            "USER must review this legacy RAR issue candidate and choose repair, "
            "waiver with reason, route, deferral, or approved GitHub issue creation."
        ),
        source=source,
    )


def _looks_like_date_or_receipt(value: str) -> bool:
    normalized = _normalize_text(value)
    if (
        re.search(r"\b20\d{2}-\d{2}-\d{2}(?:\b|T)", value)
        or re.search(r"\b20\d{6}\b", value)
    ):
        return True
    return any(word in normalized for word in ("receipt", "verified from", "not created yet"))


def _issue_number(value: str) -> str | None:
    match = re.search(r"#(\d+)", value)
    if match:
        return match.group(1)
    match = re.search(r"\b(\d+)\b", value)
    if not match:
        return None
    return match.group(1)


def _snapshot_state(value: object) -> GitHubIssueSnapshot:
    if isinstance(value, str):
        state = value
        source = "snapshot"
        last_verified = "snapshot"
        issue = ""
    elif isinstance(value, Mapping):
        state = str(value.get("state", ""))
        source = str(value.get("source", "snapshot"))
        last_verified = str(
            value.get(
                "last_verified",
                value.get("lastVerified", value.get("updatedAt", value.get("updated_at", "snapshot"))),
            )
        )
        issue = str(value.get("issue", ""))
    else:
        state = ""
        source = "snapshot"
        last_verified = "snapshot"
        issue = ""
    return GitHubIssueSnapshot(
        issue=issue,
        state=_normalize_token(state),
        source=source,
        last_verified=last_verified,
    )


def _candidate_ids_from_rows(rows: Iterable[CandidateRow]) -> set[str]:
    return {row.candidate_id for row in rows if row.candidate_id}


def _candidate_row_key(row: CandidateRow) -> tuple[str, ...]:
    return (
        row.candidate_id,
        row.owning_fam,
        row.surface,
        row.element_group,
        row.defect,
        row.evidence_pointer,
        row.current_disposition,
        row.progression_blocking,
        row.proposed_carrier,
        row.github_issue,
        row.last_verified,
        row.exact_user_decision,
    )


def _candidate_lineage_key(row: CandidateRow) -> tuple[str, ...]:
    return (
        row.candidate_id,
        row.owning_fam,
        row.surface,
        row.element_group,
        row.defect,
    )


def _explicit_lineage_present(candidate_id: str, text: str) -> bool:
    escaped = re.escape(candidate_id)
    return bool(
        re.search(
            rf"\b(predecessor|successor|lineage|renamed from|renamed to)\b[^\n|]*\b{escaped}\b|\b{escaped}\b[^\n|]*\b(predecessor|successor|lineage|renamed from|renamed to)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def _candidate_id_present(candidate_id: str, text: str) -> bool:
    escaped = re.escape(candidate_id)
    return bool(re.search(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", text))


def _is_historical_packeted_only_line(line: str) -> bool:
    normalized = _normalize_text(line)
    if not any(pattern in normalized for pattern in PACKETED_ONLY_PATTERNS):
        return False
    return any(word in normalized for word in HISTORICAL_PACKETED_ONLY_CONTEXT)


def _active_packeted_only_lines(text: str) -> list[str]:
    active_lines: list[str] = []
    for line in text.splitlines():
        normalized = _normalize_text(line)
        if not any(pattern in normalized for pattern in PACKETED_ONLY_PATTERNS):
            continue
        if _is_historical_packeted_only_line(line):
            continue
        active_lines.append(line.strip())
    return active_lines


def _github_snapshot_for_issue(
    github_snapshot: Mapping[str, GitHubIssueSnapshot] | None, issue: str
) -> GitHubIssueSnapshot | None:
    if github_snapshot is None:
        return None
    issue_number = _issue_number(issue)
    if issue_number is None:
        return None
    return github_snapshot.get(issue_number)


def _validate_github_mapping(
    row: CandidateRow,
    row_label: str,
    github_snapshot: Mapping[str, GitHubIssueSnapshot] | None,
    source: str,
) -> list[str]:
    failures: list[str] = []
    if row.disposition not in GITHUB_MAPPED_DISPOSITIONS:
        return failures
    if not re.search(r"#\d+", row.github_issue):
        failures.append(f"{source}: {row_label}: mapped GitHub disposition requires issue number")
        return failures
    if github_snapshot is None:
        failures.append(f"{source}: {row_label}: mapped GitHub disposition requires GitHub snapshot reconciliation")
        return failures
    snapshot = _github_snapshot_for_issue(github_snapshot, row.github_issue)
    if snapshot is None:
        failures.append(f"{source}: {row_label}: RAR GitHub Issue State Unknown")
        return failures
    if snapshot.state not in {"OPEN", "CLOSED"}:
        failures.append(f"{source}: {row_label}: RAR GitHub Issue State Unknown")
        return failures
    if not _looks_like_date_or_receipt(snapshot.last_verified):
        failures.append(f"{source}: {row_label}: GitHub snapshot Last Verified missing")
    if row.disposition == "MAPPED_OPEN_GITHUB_ISSUE" and snapshot.state != "OPEN":
        failures.append(f"{source}: {row_label}: RAR GitHub Issue Mapping Stale: expected open issue")
    if row.disposition == "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED" and snapshot.state != "CLOSED":
        failures.append(f"{source}: {row_label}: RAR GitHub Issue Mapping Stale: expected closed issue")
    return failures


def parse_issue_candidate_decision_surface(text: str, source: str = "<text>") -> list[CandidateRow]:
    rows: list[CandidateRow] = []
    for cells in _table_rows_after_header(text, DECISION_SURFACE_HEADER, 12):
        if len(cells) != 12:
            rows.append(_candidate_from_malformed_row(source))
            continue
        rows.append(CandidateRow(*cells, source=source))
    return rows


def parse_external_candidate_rows(text: str, source: str = "<external-ledger>") -> list[CandidateRow]:
    rows = parse_issue_candidate_decision_surface(text, source=source)
    for cells in _table_rows_after_header(text, LEGACY_RAR_HEADER, 8):
        if len(cells) == 8 and not _is_empty(cells[0]):
            rows.append(_legacy_row_to_candidate(cells, source))
        elif len(cells) != 8:
            rows.append(_candidate_from_malformed_row(source))
    return rows


def parse_external_candidate_ids(text: str) -> set[str]:
    return _candidate_ids_from_rows(parse_external_candidate_rows(text))


def validate_text(
    text: str,
    source: str = "<text>",
    github_snapshot: Mapping[str, GitHubIssueSnapshot] | None = None,
) -> list[str]:
    failures: list[str] = []
    rows = parse_issue_candidate_decision_surface(text, source=source)

    active_packeted_only = _active_packeted_only_lines(text)
    if active_packeted_only:
        failures.append(
            f"{source}: RAR Issue Candidate Durability Missing: packeted-only or packet-reviewed-only wording is not a durable disposition"
        )

    if _mentions_issue_candidate(text) and not rows:
        failures.append(f"{source}: Issue Candidate Decision Surface Missing")
        return failures

    seen: dict[str, CandidateRow] = {}
    for index, row in enumerate(rows, start=1):
        row_label = row.candidate_id or f"row {index}"
        required = {
            "Candidate ID": row.candidate_id,
            "Owning FAM": row.owning_fam,
            "Surface": row.surface,
            "Element Group": row.element_group,
            "Defect": row.defect,
            "Evidence Pointer": row.evidence_pointer,
            "Current Disposition": row.current_disposition,
            "Progression Blocking?": row.progression_blocking,
            "Proposed Carrier": row.proposed_carrier,
            "GitHub Issue": row.github_issue,
            "Last Verified": row.last_verified,
            "Exact USER Decision Needed": row.exact_user_decision,
        }
        for label, value in required.items():
            if _is_empty(value):
                failures.append(f"{source}: {row_label}: {label} missing")

        if not re.search(r"[A-Za-z][A-Za-z0-9]*[-_][A-Za-z0-9]+[-_]\d+", row.candidate_id):
            failures.append(f"{source}: {row_label}: stable candidate ID or lineage fingerprint missing")

        existing = seen.get(row.candidate_id)
        if existing and _candidate_row_key(existing) != _candidate_row_key(row):
            failures.append(f"{source}: {row.candidate_id}: duplicate/conflicting lineage")
        elif not existing:
            seen[row.candidate_id] = row

        disposition = _normalize_token(row.current_disposition)
        if any(pattern in _normalize_text(row.current_disposition) for pattern in PACKETED_ONLY_PATTERNS):
            failures.append(f"{source}: {row_label}: packeted-only disposition is not legal")
        if disposition not in LEGAL_DISPOSITIONS:
            failures.append(f"{source}: {row_label}: unsupported durable disposition {row.current_disposition!r}")

        blocking = _normalize_token(row.progression_blocking)
        if blocking not in {"YES", "NO"}:
            failures.append(f"{source}: {row_label}: Progression Blocking? must be YES or NO")
        if blocking == "YES" and disposition in TERMINAL_DISPOSITIONS:
            failures.append(
                f"{source}: {row_label}: terminal disposition cannot remain progression blocking"
            )

        carrier_decision_text = f"{row.proposed_carrier} {row.exact_user_decision}"
        carrier_decision_normalized = _normalize_text(carrier_decision_text)
        if not _looks_like_date_or_receipt(row.last_verified):
            failures.append(f"{source}: {row_label}: Last Verified requires dated or receipt-based freshness evidence")

        failures.extend(_validate_github_mapping(row, row_label, github_snapshot, source))

        if disposition in {"USER_REJECTED_WITH_REASON", "USER_WAIVED_WITH_REASON"}:
            if not re.search(r"\b(reason|because)\b", carrier_decision_normalized):
                failures.append(f"{source}: {row_label}: USER rejection/waiver requires reason")
            if disposition == "USER_WAIVED_WITH_REASON" and "scope" not in carrier_decision_normalized:
                failures.append(f"{source}: {row_label}: USER waiver requires scope")

        if disposition == "DEFERRED_WITH_OWNER":
            for expected in ("owner", "reason", "trigger"):
                if expected not in carrier_decision_normalized:
                    failures.append(
                        f"{source}: {row_label}: deferred disposition requires durable owner, reason, and next review trigger"
                    )
                    break

        if disposition == "ROUTED_TO_LEGAL_CARRIER" and "receipt" not in carrier_decision_normalized:
            failures.append(f"{source}: {row_label}: routed disposition requires carrier acceptance/receipt")

        if disposition == "GITHUB_CREATION_APPROVED_PENDING":
            if _normalize_token(row.github_issue) not in {"PENDING", "APPROVED_PENDING", "NONE_PENDING"}:
                failures.append(f"{source}: {row_label}: approved issue creation must remain visibly pending")
            if not re.search(r"\b(approval|approved|receipt)\b", carrier_decision_normalized):
                failures.append(f"{source}: {row_label}: approved issue creation requires USER approval receipt")

        if disposition == "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED":
            if not re.search(r"\b(independent|verified|revalidated|reconciled)\b", _normalize_text(carrier_decision_text)):
                failures.append(
                    f"{source}: {row_label}: closed GitHub issue mapping requires independent repair/reconciliation evidence"
                )

        if disposition == "REPAIRED_VERIFIED":
            if not re.search(r"\b(independent|verified|revalidated)\b", _normalize_text(carrier_decision_text)):
                failures.append(f"{source}: {row_label}: repaired disposition requires independent verification evidence")

        if disposition in {"UNKNOWN_GITHUB_STATE", "STALE_GITHUB_STATE"}:
            if re.search(r"\b(closed|resolved|reconciled|green)\b", _normalize_text(row.exact_user_decision)):
                failures.append(f"{source}: {row_label}: unknown/stale GitHub state cannot close candidate")

        if disposition in CURRENT_PACKET_DISPOSITIONS and blocking == "NO":
            has_owner = "owner" in carrier_decision_normalized
            has_reason = "reason" in carrier_decision_normalized
            has_route = "carrier" in carrier_decision_normalized or "route" in carrier_decision_normalized
            has_trigger = "trigger" in carrier_decision_normalized
            if not (has_owner and has_reason and has_route and has_trigger):
                failures.append(
                    f"{source}: {row_label}: non-blocking active carry-forward requires owner, carrier/route, reason, and trigger"
                )

    return failures


def _packet_markdown_files(packet_folder: Path) -> list[Path]:
    return sorted(packet_folder.rglob("*.md"))


def _path_has_part(path: Path, part: str) -> bool:
    return any(path_part.casefold() == part for path_part in path.parts)


def _path_first_part_is(path: Path, part: str) -> bool:
    return bool(path.parts) and path.parts[0].casefold() == part


def _packet_non_context_markdown_text(packet_folder: Path) -> str:
    parts: list[str] = []
    for path in sorted(packet_folder.rglob("*.md")):
        relative = path.relative_to(packet_folder)
        if _path_has_part(relative, SOURCE_TRUTH_CONTEXT_FOLDER):
            continue
        parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def _primary_decision_surface_paths(packet_folder: Path) -> list[Path]:
    primary_paths: list[Path] = []
    for path in _packet_markdown_files(packet_folder):
        relative = path.relative_to(packet_folder)
        if not _path_first_part_is(relative, PRIMARY_REVIEW_FOLDER):
            continue
        if parse_issue_candidate_decision_surface(path.read_text(encoding="utf-8"), source=str(path)):
            primary_paths.append(path)
    primary_paths.extend(_start_here_routed_primary_paths(packet_folder, excluded=set(primary_paths)))
    return primary_paths


def _context_decision_surface_paths(packet_folder: Path) -> list[Path]:
    context_paths: list[Path] = []
    for path in _packet_markdown_files(packet_folder):
        relative = path.relative_to(packet_folder)
        if not _path_has_part(relative, SOURCE_TRUTH_CONTEXT_FOLDER):
            continue
        if parse_issue_candidate_decision_surface(path.read_text(encoding="utf-8"), source=str(path)):
            context_paths.append(path)
    return context_paths


def _start_here_routed_primary_paths(packet_folder: Path, excluded: set[Path] | None = None) -> list[Path]:
    start_here = packet_folder / "START_HERE.md"
    if not start_here.exists():
        return []
    excluded = excluded or set()
    start_text = start_here.read_text(encoding="utf-8")
    routed_paths: list[Path] = []
    for path in _packet_markdown_files(packet_folder):
        if path in excluded:
            continue
        relative = path.relative_to(packet_folder)
        if _path_has_part(relative, SOURCE_TRUTH_CONTEXT_FOLDER):
            continue
        if _path_has_part(relative, REVIEW_AIDS_FOLDER):
            continue
        path_text = relative.as_posix()
        name_text = path.name
        path_is_explicit = path_text in start_text
        name_is_unambiguous = bool(
            re.search(rf"(?<![/\\\w.-]){re.escape(name_text)}(?![/\\\w.-])", start_text)
        ) and not re.search(rf"[/\\]{re.escape(name_text)}(?![/\\\w.-])", start_text)
        if not path_is_explicit and not name_is_unambiguous:
            continue
        route_target = path_text if path_is_explicit else name_text
        route_window_pattern = rf"(primary|decision|issue[ -]candidate|user review|start here|review order).{{0,160}}{re.escape(route_target)}|{re.escape(route_target)}.{{0,160}}(primary|decision|issue[ -]candidate|user review)"
        if not re.search(route_window_pattern, start_text, flags=re.IGNORECASE | re.DOTALL):
            continue
        if parse_issue_candidate_decision_surface(path.read_text(encoding="utf-8"), source=str(path)):
            routed_paths.append(path)
    return routed_paths


def _supporting_decision_surface_paths(packet_folder: Path) -> list[Path]:
    supporting_paths: list[Path] = []
    primary_paths = set(_primary_decision_surface_paths(packet_folder))
    for path in _packet_markdown_files(packet_folder):
        relative = path.relative_to(packet_folder)
        if _path_has_part(relative, SOURCE_TRUTH_CONTEXT_FOLDER):
            continue
        if path in primary_paths:
            continue
        if _path_first_part_is(relative, PRIMARY_REVIEW_FOLDER):
            continue
        if parse_issue_candidate_decision_surface(path.read_text(encoding="utf-8"), source=str(path)):
            supporting_paths.append(path)
    return supporting_paths


def _packet_primary_text(packet_folder: Path) -> str:
    parts: list[str] = []
    for path in _primary_decision_surface_paths(packet_folder):
        parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def _issue_candidate_rows_from_paths(paths: Iterable[Path]) -> list[CandidateRow]:
    rows: list[CandidateRow] = []
    for path in paths:
        rows.extend(parse_issue_candidate_decision_surface(path.read_text(encoding="utf-8"), source=str(path)))
    return rows


def validate_packet_folder(
    packet_folder: Path,
    external_ledger: Path | None = None,
    github_snapshot: Mapping[str, GitHubIssueSnapshot] | None = None,
) -> list[str]:
    failures: list[str] = []
    if not packet_folder.exists() or not packet_folder.is_dir():
        return [f"{packet_folder}: packet folder missing"]

    packet_text = _packet_non_context_markdown_text(packet_folder)
    primary_paths = _primary_decision_surface_paths(packet_folder)
    supporting_paths = _supporting_decision_surface_paths(packet_folder)
    context_paths = _context_decision_surface_paths(packet_folder)
    if supporting_paths and not primary_paths:
        failures.append(
            f"{packet_folder}: Issue Candidate Table Only In Copied Context or secondary review aid; primary USER decision surface missing"
        )
    if context_paths and not primary_paths:
        failures.append(
            f"{packet_folder}: Issue Candidate Table Only In Copied Context or secondary review aid; primary USER decision surface missing"
        )
    if len(primary_paths) > 1:
        failures.append(f"{packet_folder}: multiple primary Issue Candidate Decision Surface files")
    active_packeted_only = _active_packeted_only_lines(packet_text)
    if active_packeted_only:
        failures.append(
            f"{packet_folder}: RAR Issue Candidate Durability Missing: packeted-only or packet-reviewed-only wording is not a durable disposition"
        )
    primary_text = _packet_primary_text(packet_folder)
    primary_rows = parse_issue_candidate_decision_surface(primary_text, source=str(packet_folder))
    primary_row_ids = _candidate_ids_from_rows(primary_rows)
    primary_rows_by_id: dict[str, list[CandidateRow]] = {}
    for row in primary_rows:
        primary_rows_by_id.setdefault(row.candidate_id, []).append(row)
    supporting_context_rows = _issue_candidate_rows_from_paths([*supporting_paths, *context_paths])
    for row in supporting_context_rows:
        if not row.requires_current_packet:
            continue
        if row.candidate_id in primary_row_ids or _explicit_lineage_present(row.candidate_id, primary_text):
            continue
        failures.append(
            f"{packet_folder}: supporting/context RAR issue candidate {row.candidate_id} missing from active USER-facing packet files"
        )
    if primary_text:
        failures.extend(validate_text(primary_text, source=str(packet_folder), github_snapshot=github_snapshot))
    else:
        if _mentions_issue_candidate(packet_text):
            failures.append(f"{packet_folder}: Issue Candidate Decision Surface Missing")

    if external_ledger:
        external_text = external_ledger.read_text(encoding="utf-8")
        expanded_external_rows = parse_issue_candidate_decision_surface(external_text, source=str(external_ledger))
        external_rows = parse_external_candidate_rows(external_text, source=str(external_ledger))
        if expanded_external_rows:
            external_failures = validate_text(
                external_text, source=str(external_ledger), github_snapshot=github_snapshot
            )
            failures.extend(external_failures)
        elif "issue candidate" in _normalize_text(external_text) and not external_rows:
            failures.append(f"{external_ledger}: Issue Candidate Decision Surface Missing")
        current_rows = [row for row in external_rows if row.requires_current_packet]
        current_ids = _candidate_ids_from_rows(current_rows)
        if current_ids and not primary_paths:
            failures.append(
                f"{packet_folder}: Issue Candidate Decision Surface missing from active USER-facing packet files"
            )
        for candidate_id in sorted(current_ids):
            current_row_matches = [row for row in current_rows if row.candidate_id == candidate_id]
            primary_row_matches = primary_rows_by_id.get(candidate_id, [])
            lineage_matches = any(
                _candidate_lineage_key(external_row) == _candidate_lineage_key(primary_row)
                for external_row in current_row_matches
                for primary_row in primary_row_matches
            )
            if not lineage_matches and not _explicit_lineage_present(candidate_id, primary_text):
                failures.append(
                    f"{packet_folder}: external RAR issue candidate {candidate_id} missing from active USER-facing packet files"
                )
    return list(dict.fromkeys(failures))


def load_github_snapshot(path: Path) -> dict[str, GitHubIssueSnapshot]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("GitHub snapshot must be a JSON object mapping issue numbers to state details")
    snapshot: dict[str, GitHubIssueSnapshot] = {}
    for raw_key, raw_value in data.items():
        issue_number = _issue_number(str(raw_key))
        if issue_number is None:
            continue
        parsed = _snapshot_state(raw_value)
        snapshot[issue_number] = GitHubIssueSnapshot(
            issue=issue_number,
            state=parsed.state,
            source=parsed.source,
            last_verified=parsed.last_verified,
        )
    return snapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate RAR issue-candidate durability tables without mutating GitHub or external state."
    )
    parser.add_argument("--validate-file", type=Path, help="Validate one markdown file")
    parser.add_argument("--validate-packet-folder", type=Path, help="Validate a USER packet folder")
    parser.add_argument("--external-ledger", type=Path, help="Optional external RAR ledger for packet parity")
    parser.add_argument(
        "--github-snapshot",
        type=Path,
        help="Optional read-only JSON issue-state snapshot for deterministic caller records",
    )
    args = parser.parse_args(argv)

    github_snapshot = load_github_snapshot(args.github_snapshot) if args.github_snapshot else None

    failures: list[str] = []
    if args.validate_file:
        failures.extend(
            validate_text(
                args.validate_file.read_text(encoding="utf-8"),
                source=str(args.validate_file),
                github_snapshot=github_snapshot,
            )
        )
    if args.validate_packet_folder:
        failures.extend(validate_packet_folder(args.validate_packet_folder, args.external_ledger, github_snapshot))
    if not args.validate_file and not args.validate_packet_folder:
        parser.print_help()
        print("FAIL: no validation target supplied")
        return 2

    if failures:
        print("FAIL: RAR issue-candidate durability validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: RAR issue-candidate durability validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
