# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=rar-issue-candidate-durability-validator; status=shared
"""Validate RAR issue-candidate durability without mutating state.

This helper is intentionally narrow. It checks the table shape and disposition
semantics that keep RAR issue candidates from disappearing after a packet is
generated or reviewed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


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


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def _normalize_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().upper())
    token = re.sub(r"_+", "_", token).strip("_")
    return token


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
    header_index = None
    for index, line in enumerate(lines):
        if _line_cells(line) == _line_cells(header):
            header_index = index
            break
    if header_index is None or header_index + 1 >= len(lines):
        return rows
    separator_cells = _line_cells(lines[header_index + 1])
    if len(separator_cells) != expected_columns or not _is_separator(separator_cells):
        return rows
    for line in lines[header_index + 2 :]:
        cells = _line_cells(line)
        if not cells:
            break
        if len(cells) != expected_columns:
            rows.append(cells)
            continue
        rows.append(cells)
    return rows


def parse_issue_candidate_decision_surface(text: str, source: str = "<text>") -> list[CandidateRow]:
    rows: list[CandidateRow] = []
    for cells in _table_rows_after_header(text, DECISION_SURFACE_HEADER, 12):
        if len(cells) != 12:
            rows.append(
                CandidateRow(
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
            )
            continue
        rows.append(CandidateRow(*cells, source=source))
    return rows


def parse_external_candidate_ids(text: str) -> set[str]:
    ids = {row.candidate_id for row in parse_issue_candidate_decision_surface(text) if row.candidate_id}
    for cells in _table_rows_after_header(text, LEGACY_RAR_HEADER, 8):
        if len(cells) == 8 and not _is_empty(cells[0]):
            ids.add(cells[0])
    for match in re.finditer(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)*-\d{2,}\b", text):
        if "UIREF" not in match.group(0):
            ids.add(match.group(0))
    return ids


def _has_packeted_only_terminal_claim(text: str) -> bool:
    normalized = _normalize_text(text)
    return any(pattern in normalized for pattern in PACKETED_ONLY_PATTERNS)


def validate_text(text: str, source: str = "<text>") -> list[str]:
    failures: list[str] = []
    rows = parse_issue_candidate_decision_surface(text, source=source)

    if _has_packeted_only_terminal_claim(text):
        failures.append(
            f"{source}: RAR Issue Candidate Durability Missing: packeted-only or packet-reviewed-only wording is not a durable disposition"
        )

    if "issue candidate" in _normalize_text(text) and not rows:
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
        if existing and (
            existing.surface,
            existing.element_group,
            existing.defect,
            existing.proposed_carrier,
        ) != (
            row.surface,
            row.element_group,
            row.defect,
            row.proposed_carrier,
        ):
            failures.append(f"{source}: {row.candidate_id}: duplicate/conflicting lineage")
        seen[row.candidate_id] = row

        disposition = _normalize_token(row.current_disposition)
        if any(pattern in _normalize_text(row.current_disposition) for pattern in PACKETED_ONLY_PATTERNS):
            failures.append(f"{source}: {row_label}: packeted-only disposition is not legal")
        if disposition not in LEGAL_DISPOSITIONS:
            failures.append(f"{source}: {row_label}: unsupported durable disposition {row.current_disposition!r}")

        blocking = _normalize_token(row.progression_blocking)
        if blocking not in {"YES", "NO"}:
            failures.append(f"{source}: {row_label}: Progression Blocking? must be YES or NO")

        carrier_decision_text = f"{row.proposed_carrier} {row.exact_user_decision}"
        carrier_decision_normalized = _normalize_text(carrier_decision_text)
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

        if disposition in {"MAPPED_OPEN_GITHUB_ISSUE", "MAPPED_CLOSED_GITHUB_ISSUE_RECONCILED"}:
            if not re.search(r"#\d+", row.github_issue):
                failures.append(f"{source}: {row_label}: mapped GitHub disposition requires issue number")

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

        if disposition in ACTIVE_DISPOSITIONS and blocking == "NO":
            if not re.search(r"\b(owner|carrier|trigger|review)\b", carrier_decision_normalized):
                failures.append(
                    f"{source}: {row_label}: non-blocking active carry-forward requires owner, carrier, reason, and trigger"
                )

    return failures


def _packet_markdown_text(packet_folder: Path) -> str:
    parts: list[str] = []
    for path in sorted(packet_folder.rglob("*.md")):
        relative = path.relative_to(packet_folder)
        if any(part.casefold() == "source truth context" for part in relative.parts):
            continue
        parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def validate_packet_folder(packet_folder: Path, external_ledger: Path | None = None) -> list[str]:
    failures: list[str] = []
    if not packet_folder.exists() or not packet_folder.is_dir():
        return [f"{packet_folder}: packet folder missing"]

    packet_text = _packet_markdown_text(packet_folder)
    failures.extend(validate_text(packet_text, source=str(packet_folder)))

    if external_ledger:
        external_text = external_ledger.read_text(encoding="utf-8")
        active_ids = parse_external_candidate_ids(external_text)
        if active_ids and DECISION_SURFACE_HEADER not in packet_text:
            failures.append(
                f"{packet_folder}: Issue Candidate Decision Surface missing from active USER-facing packet files"
            )
        for candidate_id in sorted(active_ids):
            if candidate_id not in packet_text:
                failures.append(
                    f"{packet_folder}: external RAR issue candidate {candidate_id} missing from active USER-facing packet files"
                )
    return failures


def load_github_snapshot(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("GitHub snapshot must be a JSON object mapping issue numbers to state strings")
    return {str(key): str(value) for key, value in data.items()}


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

    if args.github_snapshot:
        load_github_snapshot(args.github_snapshot)

    failures: list[str] = []
    if args.validate_file:
        failures.extend(
            validate_text(args.validate_file.read_text(encoding="utf-8"), source=str(args.validate_file))
        )
    if args.validate_packet_folder:
        failures.extend(validate_packet_folder(args.validate_packet_folder, args.external_ledger))
    if not args.validate_file and not args.validate_packet_folder:
        parser.print_help()
        return 0

    if failures:
        print("FAIL: RAR issue-candidate durability validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: RAR issue-candidate durability validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
