"""Validate the FAM-003 same-defect false-closure gate.

This is a branch-local proof gate. It does not prove visual conformance and it
does not make LV green. It proves that the current branch state either blocks
a new LV1 retest candidate while recurring defects remain reopened, that the
recurring rows have v22 branch-local closure proof before a fresh packet is
generated, or that a fresh packet has been generated and USER LV1 retest is
still pending.
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
    "F3-LV1-UI-030",
    "F3-LV1-UI-031",
    "F3-LV1-UI-032",
    "F3-LV1-UI-033",
    "F3-LV1-UI-034",
    "F3-LV1-UI-035",
    "F3-LV1-UI-036",
    "F3-LV1-UI-037",
    "F3-LV1-UI-038",
)
LOOP_BREAKER_ID = "F3-LV1-PROOF-003"
PACKET_IMAGE_INTEGRITY_ID = "F3-LV1-PROOF-004"
PRIOR_FALSE_PACKETS = (
    "FAM-003-20260624-123610.zip",
    "FAM-003-20260624-140049.zip",
    "FAM-003-20260624-145524.zip",
    "FAM-003-20260624-153928.zip",
)
COMMON_REQUIRED_LEDGER_PHRASES = (
    "row-by-row red-team adjudication table",
    "`NOT CLOSED` support",
    "accepted reference comparisons",
    "before/after screenshot references",
    "expected-vs-actual reasoning",
    "marker strings, screenshot existence, state existence, or validator green alone cannot close",
    "Result: `PASS - WOULD BLOCK`",
)
BLOCKED_MODE_PHRASES = (
    "Retest Candidate Gate: `BLOCKED`",
    "Posture: `LOOP-BREAKER ONLY`",
)
REPAIRED_MODE_PHRASES = (
    "Retest Candidate Gate: `PASS - READY FOR FRESH LV1 RETEST PACKET`",
    "Posture: `REPAIRED PROOF / PACKET PENDING`",
    "V22 Same-Defect Layout-System Repair Closure Receipt",
    "Proof Root: `C:\\Nexus Worktrees\\FAM-003\\dev\\logs\\fam003_settings_repair_visual_validation\\20260625-112601`",
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
        r"^\|\s*`(F3-LV1-(?:UI|PROOF|FUNC)-\d{3})`\s*\|\s*`([^`]+)`\s*\|",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        statuses[match.group(1)] = match.group(2).strip()
    return statuses


def _latest_udl_status(text: str, defect_id: str) -> str:
    section_pattern = re.compile(
        rf"^##\s+{re.escape(defect_id)}\b(?P<body>.*?)(?=^##\s+F3-LV1-(?:UI|PROOF|FUNC)-\d{{3}}\b|\Z)",
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


def _has_binary_safe_v22_pending(text: str) -> bool:
    return bool(
        re.search(
            r"USER-operated visual retest pending for the fresh (?:binary-safe )?v22 layout-system repair packet",
            text,
        )
    )


def _has_folder_zip_parity(text: str) -> bool:
    return bool(
        re.search(r"(?:folder-ZIP|Folder\s*/\s*ZIP) parity\s*\d+\s*/\s*\d+", text, re.IGNORECASE)
    )


def _has_v22_proof_stamp(text: str) -> bool:
    return bool(
        re.search(
            r"fam003_settings_repair_visual_validation[\\/]+20260625-\d{6}",
            text,
            re.IGNORECASE,
        )
    )


def main() -> int:
    rows: list[tuple[str, bool, str]] = []
    ledger_text = _read(RECURRENCE_LEDGER)
    udl_text = _read(UDL)
    blocked_mode = "Retest Candidate Gate: `BLOCKED`" in ledger_text
    repaired_mode = "Retest Candidate Gate: `PASS - READY FOR FRESH LV1 RETEST PACKET`" in ledger_text
    active_state_text = "\n".join(_read(state_file) for state_file in STATE_FILES)
    uts_text = _read(UTS_PATH)
    packet_generated_mode = (
        repaired_mode
        and _has_binary_safe_v22_pending(active_state_text)
        and re.search(r"FAM-003-\d{8}-\d{6}\.zip", active_state_text)
        and "Result: USER RETEST PENDING" in uts_text
    )

    _row(rows, "same-defect recurrence ledger exists", bool(ledger_text), str(RECURRENCE_LEDGER))
    _row(rows, "active false-green UDL exists", bool(udl_text), str(UDL))
    _row(
        rows,
        "recurrence gate mode is recognized",
        blocked_mode or repaired_mode,
        f"blocked={blocked_mode}; repaired={repaired_mode}; packet_generated={packet_generated_mode}",
    )

    for phrase in COMMON_REQUIRED_LEDGER_PHRASES:
        _row(rows, f"ledger phrase present: {phrase}", phrase in ledger_text, str(RECURRENCE_LEDGER))
    mode_phrases = BLOCKED_MODE_PHRASES if blocked_mode else REPAIRED_MODE_PHRASES
    for phrase in mode_phrases:
        _row(rows, f"ledger mode phrase present: {phrase}", phrase in ledger_text, str(RECURRENCE_LEDGER))

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

    if blocked_mode:
        reopened_bad = [
            f"{defect_id}={table_statuses.get(defect_id, '<missing>')}"
            for defect_id in REOPENED_IDS
            if table_statuses.get(defect_id) != "REOPENED"
        ]
        _row(rows, "recurring UI/proof rows are reopened", not reopened_bad, str(reopened_bad))
    else:
        closed_bad = [
            f"{defect_id}={table_statuses.get(defect_id, '<missing>')}"
            for defect_id in REOPENED_IDS
            if table_statuses.get(defect_id) != "CLOSED_WITH_PROOF"
        ]
        _row(rows, "recurring UI/proof rows are closed with proof", not closed_bad, str(closed_bad))
    _row(
        rows,
        "loop-breaker proof row is closed with proof",
        table_statuses.get(LOOP_BREAKER_ID) == "CLOSED_WITH_PROOF",
        f"{LOOP_BREAKER_ID}={table_statuses.get(LOOP_BREAKER_ID, '<missing>')}",
    )

    expected_udl_status = "REOPENED" if blocked_mode else "CLOSED_WITH_PROOF"
    udl_bad = [
        f"{defect_id}={_latest_udl_status(udl_text, defect_id) or '<missing>'}"
        for defect_id in REOPENED_IDS
        if _latest_udl_status(udl_text, defect_id) != expected_udl_status
    ]
    _row(rows, f"active UDL latest recurring rows are {expected_udl_status}", not udl_bad, str(udl_bad))
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
        if blocked_mode:
            ok = (
                "same_defect_recurrence_ledger_20260624.md" in text
                and "Retest Candidate Gate: `BLOCKED" in text
                and "USER retest candidate blocked" in text
            )
            label = "active state records blocked gate"
        else:
            pre_packet_ok = (
                "same_defect_recurrence_ledger_20260624.md" in text
                and "same-defect v22 layout-system repair proof complete" in text
                and "fresh USER retest packet generation pending" in text
            )
            post_packet_ok = (
                "same_defect_recurrence_ledger_20260624.md" in text
                and _has_binary_safe_v22_pending(text)
                and re.search(r"FAM-003-\d{8}-\d{6}\.zip", text)
                and _has_folder_zip_parity(text)
            )
            ok = pre_packet_ok or post_packet_ok
            label = "active state records repaired/post-packet gate"
        _row(rows, f"{label}: {state_file.name}", ok, str(state_file))

    if blocked_mode:
        uts_ok = (
            "Result: BLOCKED - LOOP-BREAKER ONLY" in uts_text
            and "No USER LV1 visual retest action is requested" in uts_text
            and "FAM-003-20260624-153928.zip" in uts_text
        )
        uts_label = "UTS handoff is blocked, not retest pending"
    else:
        pre_packet_uts_ok = (
            "Result: REPAIRED - RETEST PACKET PENDING" in uts_text
            and "No USER LV1 visual retest action is requested until a fresh packet is generated" in uts_text
            and _has_v22_proof_stamp(uts_text)
        )
        post_packet_uts_ok = (
            "Result: USER RETEST PENDING" in uts_text
            and re.search(r"FAM-003-\d{8}-\d{6}\.zip", uts_text)
            and "PASS:" in uts_text
            and "FAIL:" in uts_text
            and "WAIVED:" in uts_text
            and _has_v22_proof_stamp(uts_text)
        )
        uts_ok = pre_packet_uts_ok or post_packet_uts_ok
        uts_label = "UTS handoff waits for or routes fresh retest packet"
    _row(rows, uts_label, uts_ok, str(UTS_PATH))

    bundle_text = _read(Path(__file__).with_name("orin_user_review_bundle.py"))
    bundle_ok = (
        "same-defect recurrence ledger is missing" in bundle_text
        and "same-defect recurrence gate is BLOCKED" in bundle_text
        and LOOP_BREAKER_ID in bundle_text
    )
    _row(rows, "packet validator enforces recurrence gate", bundle_ok, "dev/orin_user_review_bundle.py")

    if PACKET_IMAGE_INTEGRITY_ID in udl_text or PACKET_IMAGE_INTEGRITY_ID in active_state_text:
        proof4_status = _latest_udl_status(udl_text, PACKET_IMAGE_INTEGRITY_ID)
        _row(
            rows,
            "active UDL latest packet image-integrity row is closed with proof",
            proof4_status == "CLOSED_WITH_PROOF",
            f"{PACKET_IMAGE_INTEGRITY_ID}={proof4_status or '<missing>'}",
        )

    failed = [row for row in rows if not row[1]]
    for name, ok, detail in rows:
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {name} - {detail}")

    if failed:
        print("FAIL: FAM-003 same-defect recurrence validation failed")
        return 1
    if repaired_mode and packet_generated_mode:
        print("PASS: FAM-003 same-defect recurrence gate is repaired and USER retest packet is pending USER result")
    elif repaired_mode:
        print("PASS: FAM-003 same-defect recurrence gate is repaired and ready for fresh packet generation")
    else:
        print("PASS: FAM-003 same-defect recurrence gate blocks false retest candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
