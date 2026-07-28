"""Release one external-state lock through an auditable atomic transition."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    ExternalStateError,
    atomic_write_json,
    load_json,
    resolve_path,
    utc_now,
    validate_canonical_root,
    validate_initialized_root,
)
from orin_external_state_lock_lifecycle import (
    LOCK_TYPES,
    NON_RELEASED_LOCK_STATES,
    _intended_write_set_is_valid,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Release one External Governance State lock.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--lock-id", required=True)
    parser.add_argument(
        "--expected-workload-id",
        required=True,
        help=(
            "Exact workload that acquired the lock, or the recovery workload identity "
            "when --legacy-missing-workload-recovery is explicitly authorized."
        ),
    )
    parser.add_argument(
        "--expected-lock-sha256",
        help="Exact authoritative payload digest required for bounded legacy recovery.",
    )
    parser.add_argument(
        "--legacy-missing-workload-recovery",
        action="store_true",
        help=(
            "USER-approved migration path for a pre-upgrade lock whose only modern "
            "shape defect is a missing Workload ID. Requires --expected-lock-sha256."
        ),
    )
    parser.add_argument(
        "--legacy-recovery-authorization",
        help=(
            "Exact USER approval receipt/reference proving the legacy owner process "
            "and protected transaction are complete."
        ),
    )
    parser.add_argument("--reason", required=True)
    parser.add_argument("--apply", action="store_true")
    return parser


def _before_release_atomic_replacement(_lock_path: Path, _expected_bytes: bytes) -> None:
    """Test seam for adversarial lock mutation before final release validation."""


def _matching_transaction_journal_failures(
    root: Path,
    lock_id: str,
    *,
    context: str,
) -> list[str]:
    failures: list[str] = []
    for journal_path in sorted((root / "audit_log").glob("*.json")):
        try:
            journal = load_json(journal_path)
        except Exception as exc:  # noqa: BLE001 - ambiguous transaction state blocks
            failures.append(
                f"{context} cannot inspect transaction journal {journal_path}: {exc}"
            )
            continue
        if not isinstance(journal, dict):
            failures.append(
                f"{context} found a malformed transaction journal: {journal_path}"
            )
            continue
        if journal.get("Lock ID") != lock_id:
            continue
        transaction_like = (
            journal.get("Transition") == "Bounded coherent target-set reconciliation"
            or "Transaction State" in journal
            or "Targets" in journal
        )
        if not transaction_like:
            continue
        transaction_state = journal.get("Transaction State")
        if transaction_state == "Committed":
            continue
        if transaction_state == "Prepared":
            failures.append(
                f"{context} is blocked by an incomplete prepared transaction journal: "
                f"{journal_path}"
            )
        else:
            failures.append(
                f"{context} is blocked by a non-committed target-set transaction "
                f"journal with state {transaction_state!r}: {journal_path}"
            )
    return failures


def _legacy_recovery_shape_failures(
    root: Path,
    lock_id: str,
    payload: dict[str, object],
) -> list[str]:
    """Validate legacy recovery facts that can drift before publication."""
    failures: list[str] = []
    payload_workload_id = str(payload.get("Workload ID", "")).strip()
    if payload_workload_id:
        failures.append(
            "Legacy recovery refused a lock that already has a Workload ID"
        )
    if payload.get("Lock Type") not in LOCK_TYPES:
        failures.append("Legacy recovery requires a valid supported Lock Type")
    if not _intended_write_set_is_valid(
        str(payload.get("Intended Write Set", ""))
    ):
        failures.append("Legacy recovery requires a valid exact Intended Write Set")
    owner_process_id: int | None = None
    if "Owning Process ID" in payload:
        recorded_process_id = payload["Owning Process ID"]
        if type(recorded_process_id) is int and recorded_process_id > 0:
            owner_process_id = recorded_process_id
        elif (
            isinstance(recorded_process_id, str)
            and recorded_process_id.isdigit()
            and int(recorded_process_id) > 0
        ):
            owner_process_id = int(recorded_process_id)
        else:
            failures.append(
                "Legacy recovery requires an absent owner-process marker or a positive recorded PID"
            )
    if owner_process_id is not None:
        from orin_external_state_lock_lifecycle import process_is_running

        if process_is_running(owner_process_id) is not False:
            failures.append(
                "Legacy recovery requires the recorded owner process to be proven exited"
            )
    return failures


def release_lock(
    root: Path,
    lock_id: str,
    reason: str,
    apply: bool,
    *,
    expected_workload_id: str | None = None,
    expected_lock_sha256: str | None = None,
    legacy_missing_workload_recovery: bool = False,
    legacy_recovery_authorization: str | None = None,
) -> tuple[bool, list[str]]:
    root = resolve_path(root)
    failures = validate_canonical_root(root)
    failures.extend(validate_initialized_root(root))
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", lock_id):
        failures.append(f"Lock ID is not a safe filename: {lock_id!r}")
    lock_path = root / "locks" / f"{lock_id}.json"
    if not (expected_workload_id or "").strip():
        failures.append("Lock workload identity is required for release")
    if expected_lock_sha256 is not None and not re.fullmatch(
        r"[0-9a-f]{64}", expected_lock_sha256
    ):
        failures.append("Lock release precondition digest is invalid")
    if legacy_missing_workload_recovery and expected_lock_sha256 is None:
        failures.append(
            "Legacy missing-workload recovery requires an exact lock payload SHA256"
        )
    if legacy_missing_workload_recovery and not (
        legacy_recovery_authorization or ""
    ).strip():
        failures.append(
            "Legacy missing-workload recovery requires an explicit USER authorization receipt"
        )
    if not lock_path.is_file():
        failures.append(f"Lock is missing: {lock_path}")
    if failures:
        return False, failures
    try:
        initial_lock_bytes = lock_path.read_bytes()
    except OSError as exc:
        return False, [f"Lock is unreadable: {lock_path}: {exc}"]
    if expected_lock_sha256 is not None and hashlib.sha256(
        initial_lock_bytes
    ).hexdigest() != expected_lock_sha256:
        return False, [
            "Lock changed since stale classification; no write performed"
        ]
    try:
        payload = load_json(lock_path)
    except Exception as exc:  # noqa: BLE001 - corrupt operational state blocks release
        return False, [f"Lock is unreadable: {lock_path}: {exc}"]
    if payload.get("Lock ID") != lock_id:
        return False, [
            f"Lock payload ID mismatch: expected {lock_id!r}, found {payload.get('Lock ID')!r}"
        ]
    payload_workload_id = str(payload.get("Workload ID", "")).strip()
    if legacy_missing_workload_recovery:
        legacy_shape_failures = _legacy_recovery_shape_failures(
            root, lock_id, payload
        )
        if legacy_shape_failures:
            return False, legacy_shape_failures
    elif payload_workload_id != expected_workload_id:
        return False, [
            "Lock workload ID mismatch: expected "
            f"{expected_workload_id!r}, found {payload.get('Workload ID')!r}"
        ]
    journal_failures = _matching_transaction_journal_failures(
        root,
        lock_id,
        context=("Legacy recovery" if legacy_missing_workload_recovery else "Lock release"),
    )
    if journal_failures:
        return False, journal_failures
    if payload.get("Lock State") not in NON_RELEASED_LOCK_STATES:
        return False, [f"Lock is already released or invalid: {lock_path}"]
    release_payload = dict(payload)
    if legacy_missing_workload_recovery:
        release_payload["Legacy Original Workload ID"] = "MISSING"
        release_payload["Legacy Lock Recovery"] = (
            "Applied through explicit missing-workload migration with payload-digest CAS"
        )
        release_payload["Recovery Workload ID"] = expected_workload_id
        release_payload["Legacy Recovery Authorization"] = legacy_recovery_authorization
        release_payload["Workload ID"] = expected_workload_id
    release_payload["Lock State"] = "Released"
    release_payload["Workload State"] = "Completed"
    release_payload["Released At"] = utc_now()
    release_payload["Release Reason"] = reason
    release_payload["Last Updated"] = utc_now()
    if not apply:
        return True, [f"READY: {lock_path}", "No write performed; omit --apply was honored"]
    from orin_external_state_lock_lifecycle import lock_table_guard

    try:
        with lock_table_guard(root):
            _before_release_atomic_replacement(lock_path, initial_lock_bytes)
            try:
                final_lock_bytes = lock_path.read_bytes()
            except OSError as exc:
                return False, [f"Lock changed during release validation; no write performed: {exc}"]
            if final_lock_bytes != initial_lock_bytes:
                return False, ["Lock changed during release validation; no write performed"]
            if legacy_missing_workload_recovery:
                legacy_shape_failures = _legacy_recovery_shape_failures(
                    root, lock_id, payload
                )
                if legacy_shape_failures:
                    return False, legacy_shape_failures
            journal_failures = _matching_transaction_journal_failures(
                root,
                lock_id,
                context=(
                    "Legacy recovery"
                    if legacy_missing_workload_recovery
                    else "Lock release"
                ),
            )
            if journal_failures:
                return False, journal_failures
            atomic_write_json(lock_path, release_payload)
            try:
                authoritative = load_json(lock_path)
            except Exception as exc:  # noqa: BLE001 - authoritative reread is mandatory
                return False, [f"Lock release authoritative reread failed: {exc}"]
    except ExternalStateError as exc:
        return False, [str(exc)]
    if authoritative.get("Lock State") != "Released" or authoritative.get("Lock ID") != lock_id:
        return False, ["Lock release authoritative reread did not prove Released state"]
    from orin_external_state_lock_lifecycle import inspect_lock_table

    inventory = inspect_lock_table(root, current_workload_id=expected_workload_id)
    active = [item for item in inventory if item.active]
    workload_active = [
        item for item in active if expected_workload_id and item.workload_id == expected_workload_id
    ]
    return True, [
        f"RELEASED: {lock_path}",
        "Release Receipt State: AUTHORITATIVE_ENTRY_RELEASED",
        *(
            ["Legacy Missing-Workload Recovery: APPLIED"]
            if legacy_missing_workload_recovery
            else []
        ),
        f"Completed Workload Active Lock Count After Release: {len(workload_active)}",
        f"Authoritative Active Lock Count After Release: {len(active)}",
    ]


def main() -> int:
    args = build_parser().parse_args()
    ok, messages = release_lock(
        Path(args.root),
        args.lock_id,
        args.reason,
        args.apply,
        expected_workload_id=args.expected_workload_id,
        expected_lock_sha256=args.expected_lock_sha256,
        legacy_missing_workload_recovery=args.legacy_missing_workload_recovery,
        legacy_recovery_authorization=args.legacy_recovery_authorization,
    )
    print("External State Lock Release")
    for message in messages:
        print(message)
    print(f"Release Result: {'PASS' if ok else 'BLOCKED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
