"""Validate the FAM-003 same-defect false-closure loop breaker.

This is a branch-local proof gate. It does not prove visual conformance and it
does not make LV green. It proves that the current branch state blocks a new
LV1 retest candidate while recurring defects remain reopened.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


BRANCH_ROOT = Path(
    r"C:\Nexus Governance State\branches\feature_fam_003_resident_access_quick_actions"
)
WORKTREE_STATE = Path(r"C:\Nexus Governance State\worktrees\FAM-003\worktree_state.md")
UTS_PATH = Path(r"C:\Nexus USER\UTS - FAM-003.txt")
RECURRENCE_LEDGER = BRANCH_ROOT / "same_defect_recurrence_ledger_20260624.md"
UDL = BRANCH_ROOT / "unified_defect_ledger_20260623_false_green.md"
STATE_FILES = (
    BRANCH_ROOT / "branch_plan.md",
    BRANCH_ROOT / "branch_state.md",
    BRANCH_ROOT / "adoption_reconciliation.md",
    WORKTREE_STATE,
)

REOPENED_IDS = (
    "F3-LV1-UI-001",
    "F3-LV1-UI-016",
    "F3-LV1-UI-020",
    "F3-LV1-UI-021",
    "F3-LV1-PROOF-002",
)
LOOP_BREAKER_ID = "F3-LV1-PROOF-003"
PRIOR_FALSE_PACKETS = (
    "FAM-003-20260624-123610.zip",
    "FAM-003-20260624-140049.zip",
    "FAM-003-20260624-145524.zip",
    "FAM-003-20260624-153928.zip",
)
REQUIRED_LEDGER_PHRASES = (
    "Retest Candidate Gate: `BLOCKED`",
    "Posture: `LOOP-BREAKER ONLY`",
    "row-by-row red-team adjudication table",
    "`NOT CLOSED` support",
    "accepted reference comparisons",
    "before/after screenshot references",
    "expected-vs-actual reasoning",
    "marker strings, screenshot existence, state existence, or validator green alone cannot close",
    "Result: `PASS - WOULD BLOCK`",
)
ALLOWED_STATUSES = {
    "OPEN",
    "REPRODUCED",
    "IN_REPAIR",
    "FIXED_PENDING_PROOF",
    "PROOF_FAILED",
    "REOPENED",
    "CLOSED_WITH_PROOF",
    "BLOCKED_SOURCE_TRUTH",
    "OUT_OF_SCOPE_USER_APPROVAL_REQUIRED",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _table_statuses(text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    pattern = re.compile(
        r"^\|\s*`(F3-LV1-(?:UI|PROOF)-\d{3})`\s*\|\s*`([^`]+)`\s*\|",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        statuses[match.group(1)] = match.group(2).strip()
    return statuses


def _latest_udl_status(text: str, defect_id: str) -> str:
    section_pattern = re.compile(
        rf"^##\s+{re.escape(defect_id)}\b(?P<body>.*?)(?=^##\s+F3-LV1-(?:UI|PROOF)-\d{{3}}\b|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    status = ""
    for match in section_pattern.finditer(text):
        status_match = re.search(r"^Status:\s*`?([^`\n]+)`?", match.group("body"), re.MULTILINE)
        if status_match:
            status = status_match.group(1).strip()
    return status


def _row(rows: list[tuple[str, bool, str]], name: str, ok: bool, detail: str) -> None:
    rows.append((name, ok, detail))


def main() -> int:
    rows: list[tuple[str, bool, str]] = []
    ledger_text = _read(RECURRENCE_LEDGER)
    udl_text = _read(UDL)

    _row(rows, "same-defect recurrence ledger exists", bool(ledger_text), str(RECURRENCE_LEDGER))
    _row(rows, "active false-green UDL exists", bool(udl_text), str(UDL))

    for phrase in REQUIRED_LEDGER_PHRASES:
        _row(rows, f"ledger phrase present: {phrase}", phrase in ledger_text, str(RECURRENCE_LEDGER))

    table_statuses = _table_statuses(ledger_text)
    missing_table_rows = [
        defect_id for defect_id in (*REOPENED_IDS, LOOP_BREAKER_ID) if defect_id not in table_statuses
    ]
    illegal_table_statuses = [
        f"{defect_id}={status}"
        for defect_id, status in table_statuses.items()
        if status not in ALLOWED_STATUSES
    ]
    _row(rows, "recurrence table includes required rows", not missing_table_rows, str(missing_table_rows))
    _row(rows, "recurrence table statuses are legal", not illegal_table_statuses, str(illegal_table_statuses))

    reopened_bad = [
        f"{defect_id}={table_statuses.get(defect_id, '<missing>')}"
        for defect_id in REOPENED_IDS
        if table_statuses.get(defect_id) != "REOPENED"
    ]
    _row(rows, "recurring UI/proof rows are reopened", not reopened_bad, str(reopened_bad))
    _row(
        rows,
        "loop-breaker proof row is closed with proof",
        table_statuses.get(LOOP_BREAKER_ID) == "CLOSED_WITH_PROOF",
        f"{LOOP_BREAKER_ID}={table_statuses.get(LOOP_BREAKER_ID, '<missing>')}",
    )

    udl_bad = [
        f"{defect_id}={_latest_udl_status(udl_text, defect_id) or '<missing>'}"
        for defect_id in REOPENED_IDS
        if _latest_udl_status(udl_text, defect_id) != "REOPENED"
    ]
    _row(rows, "active UDL latest recurring rows are reopened", not udl_bad, str(udl_bad))
    proof3_status = _latest_udl_status(udl_text, LOOP_BREAKER_ID)
    _row(
        rows,
        "active UDL latest loop-breaker row is closed with proof",
        proof3_status == "CLOSED_WITH_PROOF",
        f"{LOOP_BREAKER_ID}={proof3_status or '<missing>'}",
    )

    missing_prior_packets = [packet for packet in PRIOR_FALSE_PACKETS if packet not in ledger_text]
    _row(rows, "prior false packets named and would be blocked", not missing_prior_packets, str(missing_prior_packets))

    for state_file in STATE_FILES:
        text = _read(state_file)
        ok = (
            "same_defect_recurrence_ledger_20260624.md" in text
            and "Retest Candidate Gate: `BLOCKED" in text
            and "USER retest candidate blocked" in text
        )
        _row(rows, f"active state records blocked gate: {state_file.name}", ok, str(state_file))

    uts_text = _read(UTS_PATH)
    uts_ok = (
        "Result: BLOCKED - LOOP-BREAKER ONLY" in uts_text
        and "No USER LV1 visual retest action is requested" in uts_text
        and "FAM-003-20260624-153928.zip" in uts_text
    )
    _row(rows, "UTS handoff is blocked, not retest pending", uts_ok, str(UTS_PATH))

    bundle_text = _read(Path(__file__).with_name("orin_user_review_bundle.py"))
    bundle_ok = (
        "same-defect recurrence ledger is missing" in bundle_text
        and "same-defect recurrence gate is BLOCKED" in bundle_text
        and LOOP_BREAKER_ID in bundle_text
    )
    _row(rows, "packet validator enforces recurrence gate", bundle_ok, "dev/orin_user_review_bundle.py")

    failed = [row for row in rows if not row[1]]
    for name, ok, detail in rows:
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {name} - {detail}")

    if failed:
        print("FAIL: FAM-003 same-defect recurrence validation failed")
        return 1
    print("PASS: FAM-003 same-defect recurrence gate blocks false retest candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
