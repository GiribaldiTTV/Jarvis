"""Positive and negative fixtures for workload-scoped external-state locks."""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from orin_external_state_common import ExternalStateError, atomic_write_json
from orin_external_state_lock import acquire_lock
import orin_external_state_lock_lifecycle as lock_lifecycle
import orin_external_state_lock_release as lock_release_module
from orin_external_state_lock_lifecycle import (
    ExternalStateLockTransaction,
    inspect_lock_table,
    release_stale_completed_lock,
    verify_final_lock_state,
)
from orin_external_state_lock_release import release_lock


WORKTREE = r"C:\Nexus Worktrees\Governance"
BRANCH = "feature/release-readiness-source-truth-intake"
TARGETS = "central/active_branch_authority_state.md;central/selected_next_state.md"


class FixtureValidationFailure(RuntimeError):
    pass


class FixtureBlocked(RuntimeError):
    pass


def _competing_acquire(root_value: str, start, results, workload_id: str) -> None:
    start.wait()
    result = acquire_lock(
        root=Path(root_value),
        lock_type="branch",
        owner="fixture-child",
        workload_id=workload_id,
        owner_process_id=os.getpid(),
        worktree=WORKTREE,
        branch=BRANCH,
        intended_write_set=TARGETS,
        expires="release before fixture child exits",
        apply=True,
    )
    results.put((workload_id, *result))


def _root(path: Path) -> None:
    atomic_write_json(
        path / "state_manifest.json",
        {
            "External State Schema": "external-state-v1",
            "State Version": 1,
            "Last Updated": "2026-01-01T00:00:00Z",
            "Last Updated By": "fixture",
            "Worktree": "Governance",
            "Branch": BRANCH,
            "Source Repo HEAD": "a" * 40,
        },
    )
    (path / "locks").mkdir(parents=True, exist_ok=True)
    (path / "audit_log").mkdir(parents=True, exist_ok=True)


def _lock(
    root: Path,
    lock_id: str,
    workload_id: str,
    *,
    state: str = "Locked",
    workload_state: str = "Active",
    process_id: int | str = 999999,
    targets: str = TARGETS,
) -> Path:
    path = root / "locks" / f"{lock_id}.json"
    atomic_write_json(
        path,
        {
            "External State Schema": "external-state-v1",
            "State Version": 1,
            "Last Updated": "2026-01-01T00:00:00Z",
            "Last Updated By": "fixture",
            "Worktree": WORKTREE,
            "Branch": BRANCH,
            "Source Repo HEAD": "a" * 40,
            "Lock ID": lock_id,
            "Lock Type": "branch",
            "Lock State": state,
            "Workload ID": workload_id,
            "Workload State": workload_state,
            "Owning Process ID": process_id,
            "Acquired At": "2026-01-01T00:00:00Z",
            "Last Activity At": "2026-01-01T00:00:00Z",
            "Intended Write Set": targets,
            "Expiration": "release before final digest",
            "Retain Between Workloads": "No",
            "Release Required Before Final Digest": "Yes",
        },
    )
    return path


def _assert_blocked(name: str, result: tuple[bool, list[str]], needle: str) -> None:
    ok, messages = result
    if ok or not any(needle in message for message in messages):
        raise AssertionError(f"{name} did not block on {needle!r}:\n" + "\n".join(messages))


def _assert_released(root: Path, workload_id: str) -> None:
    ok, messages = verify_final_lock_state(
        root,
        workload_id=workload_id,
        require_global_zero=True,
    )
    if not ok:
        raise AssertionError("workload lock was not released:\n" + "\n".join(messages))


def _transaction(root: Path, workload_id: str) -> ExternalStateLockTransaction:
    return ExternalStateLockTransaction(
        root=root,
        lock_type="branch",
        owner="fixture",
        workload_id=workload_id,
        owner_process_id=os.getpid(),
        worktree=WORKTREE,
        branch=BRANCH,
        intended_write_set=TARGETS,
        expires="release before fixture completion",
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ndai-lock-lifecycle-") as temp_dir:
        root = Path(temp_dir)
        _root(root)

        # Negative: success/complete/waiting postures cannot retain an active lock.
        _lock(root, "negative-success-digest", "negative-success")
        _assert_blocked(
            "success digest with active lock",
            verify_final_lock_state(root, workload_id="negative-success"),
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
        )
        validator = Path(__file__).with_name("orin_external_state_validation.py")
        retained_cli = subprocess.run(
            [
                sys.executable,
                str(validator),
                "--root",
                str(root),
                "--final-lock-gate",
                "--completed-workload-id",
                "negative-success",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if retained_cli.returncode == 0 or "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED" not in (
            retained_cli.stdout + retained_cli.stderr
        ):
            raise AssertionError(
                "public final-lock gate accepted a retained workload lock:\n"
                + retained_cli.stdout
                + retained_cli.stderr
            )
        release_lock(
            root,
            "negative-success-digest",
            "fixture reset",
            True,
            expected_workload_id="negative-success",
        )
        released_cli = subprocess.run(
            [
                sys.executable,
                str(validator),
                "--root",
                str(root),
                "--final-lock-gate",
                "--completed-workload-id",
                "negative-success",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if released_cli.returncode != 0:
            raise AssertionError(
                "public final-lock gate rejected a released workload lock:\n"
                + released_cli.stdout
                + released_cli.stderr
            )

        _lock(
            root,
            "negative-foreign-global-zero",
            "foreign-global-zero-workload",
            targets="branches/other/branch_state.md",
        )
        foreign_global_cli = subprocess.run(
            [
                sys.executable,
                str(validator),
                "--root",
                str(root),
                "--final-lock-gate",
                "--completed-workload-id",
                "completed-local-workload",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if foreign_global_cli.returncode == 0 or "Authoritative Active Lock Count Not Zero" not in (
            foreign_global_cli.stdout + foreign_global_cli.stderr
        ):
            raise AssertionError(
                "public final-lock gate accepted a foreign active lock:\n"
                + foreign_global_cli.stdout
                + foreign_global_cli.stderr
            )
        release_lock(
            root,
            "negative-foreign-global-zero",
            "fixture reset",
            True,
            expected_workload_id="foreign-global-zero-workload",
        )

        for currentness_mode in ("--semantic-currentness", "--target-currentness"):
            combined_cli = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    "--root",
                    str(root),
                    currentness_mode,
                    "--final-lock-gate",
                    "--completed-workload-id",
                    "combined-mode-workload",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if combined_cli.returncode == 0 or "exclusive validation modes" not in (
                combined_cli.stdout + combined_cli.stderr
            ):
                raise AssertionError(
                    f"public validator accepted {currentness_mode} with final-lock gate:\n"
                    + combined_cli.stdout
                    + combined_cli.stderr
                )

        for global_gate_args, label in (
            (["--require-stage4-records"], "global Stage 4 records"),
            (["--expected-source-head", "0" * 40], "manifest source HEAD"),
        ):
            combined_semantic_cli = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    "--root",
                    str(root),
                    "--semantic-currentness",
                    *global_gate_args,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if combined_semantic_cli.returncode == 0 or (
                "Semantic currentness cannot be combined with global"
                not in combined_semantic_cli.stdout + combined_semantic_cli.stderr
            ):
                raise AssertionError(
                    f"public validator accepted semantic currentness with {label}:\n"
                    + combined_semantic_cli.stdout
                    + combined_semantic_cli.stderr
                )

        missing_root = root / "missing-external-state-root"
        for gate_args, label in (
            (["--semantic-currentness"], "semantic currentness"),
            (
                [
                    "--final-lock-gate",
                    "--completed-workload-id",
                    "missing-root-workload",
                ],
                "final lock",
            ),
        ):
            missing_root_cli = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    "--root",
                    str(missing_root),
                    *gate_args,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if missing_root_cli.returncode == 0 or "Clean Clone Boundary: BLOCKED" not in (
                missing_root_cli.stdout + missing_root_cli.stderr
            ):
                raise AssertionError(
                    f"explicit {label} gate accepted a missing external-state root:\n"
                    + missing_root_cli.stdout
                    + missing_root_cli.stderr
                )

        _lock(
            root,
            "negative-completed-retained",
            "negative-completed",
            workload_state="Completed",
        )
        _assert_blocked(
            "completed workload retained lock",
            verify_final_lock_state(root, workload_id="negative-completed"),
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
        )
        release_lock(
            root,
            "negative-completed-retained",
            "fixture reset",
            True,
            expected_workload_id="negative-completed",
        )

        _lock(
            root,
            "negative-waiting-retained",
            "negative-waiting",
            workload_state="Waiting For USER",
        )
        _assert_blocked(
            "waiting for USER retained lock",
            verify_final_lock_state(root, workload_id="negative-waiting"),
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
        )
        release_lock(
            root,
            "negative-waiting-retained",
            "fixture reset",
            True,
            expected_workload_id="negative-waiting",
        )

        # Negative: raw failure/exception/multi-write bypasses are caught by final verification.
        for label in ("validation-failure", "exception", "multi-target-write-failure"):
            lock_id = f"negative-{label}"
            _lock(root, lock_id, label)
            _assert_blocked(
                label,
                verify_final_lock_state(root, workload_id=label),
                "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
            )
            release_lock(
                root,
                lock_id,
                "fixture reset",
                True,
                expected_workload_id=label,
            )

        # Negative: a receipt does not override the authoritative active entry.
        _lock(root, "negative-receipt-only", "receipt-only")
        atomic_write_json(
            root / "audit_log" / "release-receipt.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": "negative-receipt-only",
                "Claimed State": "Released",
            },
        )
        _assert_blocked(
            "receipt without authoritative release",
            verify_final_lock_state(root, workload_id="receipt-only"),
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
        )
        release_lock(
            root,
            "negative-receipt-only",
            "fixture reset",
            True,
            expected_workload_id="receipt-only",
        )

        # Negative: a dead process makes an active workload orphaned, never valid authority.
        _lock(root, "negative-dead-owner", "dead-owner")
        dead = inspect_lock_table(
            root,
            current_workload_id="dead-owner",
            process_checker=lambda _pid: False,
        )
        dead_row = next(item for item in dead if item.lock_id == "negative-dead-owner")
        if dead_row.classification != "ORPHANED_ACTIVE_WORKLOAD":
            raise AssertionError(f"dead owner classified as {dead_row.classification}")
        _assert_blocked(
            "dead process with active workload state",
            release_stale_completed_lock(
                root,
                lock_id="negative-dead-owner",
                expected_workload_id="dead-owner",
                reason="active workload must remain protected",
                apply=True,
                process_checker=lambda _pid: False,
            ),
            "not proven stale completed workload",
        )
        release_lock(
            root,
            "negative-dead-owner",
            "fixture reset",
            True,
            expected_workload_id="dead-owner",
        )

        identityless_path = _lock(
            root,
            "negative-identityless-release",
            "identityless-release-workload",
        )
        release_helper = Path(__file__).with_name("orin_external_state_lock_release.py")
        identityless_cli = subprocess.run(
            [
                sys.executable,
                str(release_helper),
                "--root",
                str(root),
                "--lock-id",
                "negative-identityless-release",
                "--reason",
                "must remain blocked",
                "--apply",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if identityless_cli.returncode == 0 or "--expected-workload-id" not in (
            identityless_cli.stdout + identityless_cli.stderr
        ):
            raise AssertionError(
                "release CLI accepted an identity-less applied release:\n"
                + identityless_cli.stdout
                + identityless_cli.stderr
            )
        _assert_blocked(
            "identity-less applied release",
            release_lock(
                root,
                "negative-identityless-release",
                "must remain blocked",
                True,
            ),
            "workload identity is required",
        )
        if json.loads(identityless_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("identity-less release mutated the authoritative lock")
        release_lock(
            root,
            "negative-identityless-release",
            "fixture reset",
            True,
            expected_workload_id="identityless-release-workload",
        )

        modern_legacy_path = _lock(
            root,
            "negative-modern-legacy-recovery",
            "modern-owner-workload",
        )
        _assert_blocked(
            "legacy recovery against modern lock",
            release_lock(
                root,
                "negative-modern-legacy-recovery",
                "must not recover a modern foreign lock",
                True,
                expected_workload_id="legacy-recovery-workload",
                expected_lock_sha256=hashlib.sha256(
                    modern_legacy_path.read_bytes()
                ).hexdigest(),
                legacy_missing_workload_recovery=True,
                legacy_recovery_authorization="USER-approved fixture recovery",
            ),
            "already has a Workload ID",
        )
        release_lock(
            root,
            "negative-modern-legacy-recovery",
            "fixture reset",
            True,
            expected_workload_id="modern-owner-workload",
        )

        legacy_path = _lock(
            root,
            "positive-legacy-missing-workload",
            "pre-upgrade-workload-not-recorded",
        )
        legacy_payload = json.loads(legacy_path.read_text(encoding="utf-8"))
        legacy_payload.pop("Workload ID")
        for invalid_process_id in ("abc", 0, -1):
            invalid_process_payload = dict(legacy_payload)
            invalid_process_payload["Owning Process ID"] = invalid_process_id
            atomic_write_json(legacy_path, invalid_process_payload)
            _assert_blocked(
                f"legacy recovery with invalid owner PID {invalid_process_id!r}",
                release_lock(
                    root,
                    "positive-legacy-missing-workload",
                    "invalid owner identity must block",
                    True,
                    expected_workload_id="legacy-recovery-workload",
                    expected_lock_sha256=hashlib.sha256(
                        legacy_path.read_bytes()
                    ).hexdigest(),
                    legacy_missing_workload_recovery=True,
                    legacy_recovery_authorization="USER-approved fixture recovery",
                ),
                "absent owner-process marker or a positive recorded PID",
            )
        atomic_write_json(legacy_path, legacy_payload)
        legacy_digest = hashlib.sha256(legacy_path.read_bytes()).hexdigest()
        legacy_row = next(
            item
            for item in inspect_lock_table(root, current_workload_id="legacy-recovery-workload")
            if item.lock_id == "positive-legacy-missing-workload"
        )
        if legacy_row.classification != "MALFORMED" or not legacy_row.active:
            raise AssertionError(
                "pre-upgrade missing-workload lock was not retained as a blocking entry"
            )
        _assert_blocked(
            "ordinary release of pre-upgrade lock",
            release_lock(
                root,
                "positive-legacy-missing-workload",
                "ordinary ownership check must remain enforced",
                True,
                expected_workload_id="legacy-recovery-workload",
            ),
            "Lock workload ID mismatch",
        )
        _assert_blocked(
            "legacy recovery without payload digest",
            release_lock(
                root,
                "positive-legacy-missing-workload",
                "missing recovery precondition",
                True,
                expected_workload_id="legacy-recovery-workload",
                legacy_missing_workload_recovery=True,
            ),
            "requires an exact lock payload SHA256",
        )
        _assert_blocked(
            "legacy recovery after payload drift",
            release_lock(
                root,
                "positive-legacy-missing-workload",
                "wrong recovery precondition",
                True,
                expected_workload_id="legacy-recovery-workload",
                expected_lock_sha256="0" * 64,
                legacy_missing_workload_recovery=True,
                legacy_recovery_authorization="USER-approved fixture recovery",
            ),
            "changed since stale classification",
        )
        legacy_race_journal = root / "audit_log" / "legacy-recovery-race.json"
        original_before_release = (
            lock_release_module._before_release_atomic_replacement
        )

        def _inject_prepared_journal(_lock_path: Path, _expected_bytes: bytes) -> None:
            atomic_write_json(
                legacy_race_journal,
                {
                    "Lock ID": "positive-legacy-missing-workload",
                    "Transaction State": "Prepared",
                },
            )

        lock_release_module._before_release_atomic_replacement = (
            _inject_prepared_journal
        )
        try:
            _assert_blocked(
                "legacy recovery transaction-journal race",
                release_lock(
                    root,
                    "positive-legacy-missing-workload",
                    "race must be caught inside the publication guard",
                    True,
                    expected_workload_id="legacy-recovery-workload",
                    expected_lock_sha256=legacy_digest,
                    legacy_missing_workload_recovery=True,
                    legacy_recovery_authorization="USER-approved fixture recovery",
                ),
                "incomplete prepared transaction journal",
            )
        finally:
            lock_release_module._before_release_atomic_replacement = (
                original_before_release
            )
            legacy_race_journal.unlink(missing_ok=True)
        if hashlib.sha256(legacy_path.read_bytes()).hexdigest() != legacy_digest:
            raise AssertionError(
                "legacy recovery race fixture changed the authoritative lock"
            )
        for invalid_state in (None, "", "Corrupt"):
            def _inject_ambiguous_journal(
                _lock_path: Path,
                _expected_bytes: bytes,
                state=invalid_state,
            ) -> None:
                payload = {
                    "Transition": "Bounded coherent target-set reconciliation",
                    "Lock ID": "positive-legacy-missing-workload",
                    "Targets": [],
                }
                if state is not None:
                    payload["Transaction State"] = state
                atomic_write_json(legacy_race_journal, payload)

            lock_release_module._before_release_atomic_replacement = (
                _inject_ambiguous_journal
            )
            try:
                _assert_blocked(
                    f"legacy recovery with ambiguous journal state {invalid_state!r}",
                    release_lock(
                        root,
                        "positive-legacy-missing-workload",
                        "ambiguous transaction evidence must block",
                        True,
                        expected_workload_id="legacy-recovery-workload",
                        expected_lock_sha256=legacy_digest,
                        legacy_missing_workload_recovery=True,
                        legacy_recovery_authorization="USER-approved fixture recovery",
                    ),
                    "non-committed target-set transaction journal",
                )
            finally:
                lock_release_module._before_release_atomic_replacement = (
                    original_before_release
                )
                legacy_race_journal.unlink(missing_ok=True)
        atomic_write_json(
            legacy_race_journal,
            {
                "Transition": "Bounded coherent target-set reconciliation",
                "Lock ID": "positive-legacy-missing-workload",
                "Transaction State": "Committed",
                "Targets": [],
            },
        )
        recovered, recovery_messages = release_lock(
            root,
            "positive-legacy-missing-workload",
            "USER-approved pre-upgrade lock migration fixture",
            True,
            expected_workload_id="legacy-recovery-workload",
            expected_lock_sha256=legacy_digest,
            legacy_missing_workload_recovery=True,
            legacy_recovery_authorization="USER-approved fixture recovery",
        )
        recovered_payload = json.loads(legacy_path.read_text(encoding="utf-8"))
        if (
            not recovered
            or recovered_payload.get("Lock State") != "Released"
            or recovered_payload.get("Workload ID") != "legacy-recovery-workload"
            or recovered_payload.get("Legacy Original Workload ID") != "MISSING"
            or not any(
                "Legacy Missing-Workload Recovery: APPLIED" in message
                for message in recovery_messages
            )
        ):
            raise AssertionError(
                "bounded legacy missing-workload recovery failed:\n"
                + "\n".join(recovery_messages)
            )
        legacy_race_journal.unlink(missing_ok=True)

        ordinary_lock_id = "negative-ordinary-prepared-release"
        ordinary_workload_id = "ordinary-prepared-release-workload"
        ordinary_lock_path = _lock(
            root,
            ordinary_lock_id,
            ordinary_workload_id,
            process_id=os.getpid(),
        )
        ordinary_journal = root / "audit_log" / "ordinary-prepared-release.json"
        atomic_write_json(
            ordinary_journal,
            {
                "Transition": "Bounded coherent target-set reconciliation",
                "Lock ID": ordinary_lock_id,
                "Workload ID": ordinary_workload_id,
                "Transaction State": "Prepared",
                "Targets": [],
            },
        )
        _assert_blocked(
            "ordinary release with prepared target-set journal",
            release_lock(
                root,
                ordinary_lock_id,
                "prepared transaction must block release",
                True,
                expected_workload_id=ordinary_workload_id,
            ),
            "incomplete prepared transaction journal",
        )
        if json.loads(ordinary_lock_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("ordinary release changed a lock with a prepared journal")
        ordinary_journal.unlink()
        released, release_messages = release_lock(
            root,
            ordinary_lock_id,
            "fixture reset after prepared journal removal",
            True,
            expected_workload_id=ordinary_workload_id,
        )
        if not released:
            raise AssertionError(
                "ordinary lock did not release after journal removal:\n"
                + "\n".join(release_messages)
            )

        ordinary_race_lock_id = "negative-ordinary-prepared-release-race"
        ordinary_race_workload_id = "ordinary-prepared-release-race-workload"
        ordinary_race_lock_path = _lock(
            root,
            ordinary_race_lock_id,
            ordinary_race_workload_id,
            process_id=os.getpid(),
        )
        ordinary_race_journal = root / "audit_log" / "ordinary-prepared-release-race.json"
        original_before_release = lock_release_module._before_release_atomic_replacement

        def _inject_ordinary_prepared_journal(
            _lock_path: Path,
            _expected_bytes: bytes,
        ) -> None:
            atomic_write_json(
                ordinary_race_journal,
                {
                    "Transition": "Bounded coherent target-set reconciliation",
                    "Lock ID": ordinary_race_lock_id,
                    "Workload ID": ordinary_race_workload_id,
                    "Transaction State": "Prepared",
                    "Targets": [],
                },
            )

        lock_release_module._before_release_atomic_replacement = (
            _inject_ordinary_prepared_journal
        )
        try:
            _assert_blocked(
                "ordinary release prepared-journal race",
                release_lock(
                    root,
                    ordinary_race_lock_id,
                    "late prepared transaction must block release",
                    True,
                    expected_workload_id=ordinary_race_workload_id,
                ),
                "incomplete prepared transaction journal",
            )
        finally:
            lock_release_module._before_release_atomic_replacement = (
                original_before_release
            )
        if json.loads(ordinary_race_lock_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("ordinary release missed a late prepared journal")
        ordinary_race_journal.unlink()
        released, release_messages = release_lock(
            root,
            ordinary_race_lock_id,
            "fixture reset after prepared-journal race",
            True,
            expected_workload_id=ordinary_race_workload_id,
        )
        if not released:
            raise AssertionError(
                "ordinary race lock did not release after journal removal:\n"
                + "\n".join(release_messages)
            )

        stale_lock_id = "negative-stale-prepared-release"
        stale_workload_id = "stale-prepared-release-workload"
        stale_lock_path = _lock(
            root,
            stale_lock_id,
            stale_workload_id,
            workload_state="Completed",
        )
        stale_journal = root / "audit_log" / "stale-prepared-release.json"
        atomic_write_json(
            stale_journal,
            {
                "Transition": "Bounded coherent target-set reconciliation",
                "Lock ID": stale_lock_id,
                "Workload ID": stale_workload_id,
                "Transaction State": "Prepared",
                "Targets": [],
            },
        )
        _assert_blocked(
            "stale-completed release with prepared target-set journal",
            release_stale_completed_lock(
                root,
                lock_id=stale_lock_id,
                expected_workload_id=stale_workload_id,
                reason="prepared transaction must block stale cleanup",
                apply=True,
                process_checker=lambda _pid: False,
            ),
            "incomplete prepared transaction journal",
        )
        if json.loads(stale_lock_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("stale cleanup changed a lock with a prepared journal")
        stale_journal.unlink()
        released, release_messages = release_stale_completed_lock(
            root,
            lock_id=stale_lock_id,
            expected_workload_id=stale_workload_id,
            reason="fixture reset after prepared journal removal",
            apply=True,
            process_checker=lambda _pid: False,
        )
        if not released:
            raise AssertionError(
                "stale lock did not release after journal removal:\n"
                + "\n".join(release_messages)
            )

        transaction_workload_id = "transaction-prepared-release-workload"
        transaction_journal = root / "audit_log" / "transaction-prepared-release.json"
        transaction_lock_id = ""
        try:
            with _transaction(root, transaction_workload_id) as transaction:
                transaction_lock_id = transaction.lock_id
                atomic_write_json(
                    transaction_journal,
                    {
                        "Transition": "Bounded coherent target-set reconciliation",
                        "Lock ID": transaction_lock_id,
                        "Workload ID": transaction_workload_id,
                        "Transaction State": "Prepared",
                        "Targets": [],
                    },
                )
        except ExternalStateError as exc:
            if "incomplete prepared transaction journal" not in str(exc):
                raise AssertionError(
                    "transaction cleanup blocked for the wrong reason: " + str(exc)
                ) from exc
        else:
            raise AssertionError("transaction cleanup released a lock with a prepared journal")
        transaction_lock_path = root / "locks" / f"{transaction_lock_id}.json"
        if json.loads(transaction_lock_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("transaction cleanup changed a lock with a prepared journal")
        transaction_journal.unlink()
        released, release_messages = release_lock(
            root,
            transaction_lock_id,
            "fixture reset after prepared journal removal",
            True,
            expected_workload_id=transaction_workload_id,
        )
        if not released:
            raise AssertionError(
                "transaction lock did not release after journal removal:\n"
                + "\n".join(release_messages)
            )

        for malformed_id, mutate in (
            ("negative-missing-lock-type", lambda payload: payload.pop("Lock Type")),
            (
                "negative-missing-write-set",
                lambda payload: payload.pop("Intended Write Set"),
            ),
            (
                "negative-invalid-lock-type",
                lambda payload: payload.__setitem__("Lock Type", "unknown-type"),
            ),
            (
                "negative-invalid-write-set",
                lambda payload: payload.__setitem__("Intended Write Set", "../outside.md"),
            ),
        ):
            malformed_path = _lock(root, malformed_id, malformed_id)
            malformed_payload = json.loads(malformed_path.read_text(encoding="utf-8"))
            mutate(malformed_payload)
            atomic_write_json(malformed_path, malformed_payload)
            malformed_row = next(
                item
                for item in inspect_lock_table(root, current_workload_id="local-workload")
                if item.lock_id == malformed_id
            )
            if malformed_row.classification != "MALFORMED":
                raise AssertionError(
                    f"incomplete conflict metadata classified as {malformed_row.classification}"
                )
            acquired, acquire_messages, _ = acquire_lock(
                root=root,
                lock_type="branch",
                owner="fixture",
                workload_id="local-workload",
                owner_process_id=os.getpid(),
                worktree=WORKTREE,
                branch=BRANCH,
                intended_write_set=TARGETS,
                expires="fixture",
                apply=False,
            )
            if acquired or not any(
                "External State Corrupt" in item for item in acquire_messages
            ):
                raise AssertionError(
                    "acquisition did not fail closed on malformed conflict metadata:\n"
                    + "\n".join(acquire_messages)
                )
            release_lock(
                root,
                malformed_id,
                "fixture reset",
                True,
                expected_workload_id=malformed_id,
            )

        for ordinal, invalid_process_id in enumerate(
            (0, -1, "abc", "", None, True, False, 1.5),
            start=1,
        ):
            malformed_id = f"negative-invalid-owner-process-{ordinal}"
            malformed_path = _lock(root, malformed_id, malformed_id)
            malformed_payload = json.loads(malformed_path.read_text(encoding="utf-8"))
            malformed_payload["Owning Process ID"] = invalid_process_id
            atomic_write_json(malformed_path, malformed_payload)
            malformed_row = next(
                item
                for item in inspect_lock_table(root, current_workload_id=malformed_id)
                if item.lock_id == malformed_id
            )
            if malformed_row.classification != "MALFORMED" or not malformed_row.active:
                raise AssertionError(
                    "present invalid owner process ID was not retained as a blocking "
                    f"malformed lock: {invalid_process_id!r} -> "
                    f"{malformed_row.classification}"
                )
            acquired, acquire_messages, _ = acquire_lock(
                root=root,
                lock_type="branch",
                owner="fixture",
                workload_id="local-workload",
                owner_process_id=os.getpid(),
                worktree=WORKTREE,
                branch=BRANCH,
                intended_write_set=TARGETS,
                expires="fixture",
                apply=False,
            )
            if acquired or not any(
                "External State Corrupt" in item for item in acquire_messages
            ):
                raise AssertionError(
                    "acquisition did not fail closed on an invalid recorded owner process ID:\n"
                    + "\n".join(acquire_messages)
                )
            malformed_path.unlink()

        for absent_marker_id, remove_marker in (
            ("positive-owner-process-not-recorded", False),
            ("positive-owner-process-marker-absent", True),
        ):
            absent_marker_path = _lock(
                root,
                absent_marker_id,
                absent_marker_id,
                process_id="Not recorded",
            )
            if remove_marker:
                absent_marker_payload = json.loads(
                    absent_marker_path.read_text(encoding="utf-8")
                )
                absent_marker_payload.pop("Owning Process ID")
                atomic_write_json(absent_marker_path, absent_marker_payload)
            absent_marker_row = next(
                item
                for item in inspect_lock_table(
                    root,
                    current_workload_id=absent_marker_id,
                )
                if item.lock_id == absent_marker_id
            )
            if (
                absent_marker_row.classification != "ACTIVE_VALID"
                or absent_marker_row.owner_process_id is not None
            ):
                raise AssertionError(
                    "an intentional absent owner-process marker was rejected: "
                    f"{absent_marker_row.classification}"
                )
            release_lock(
                root,
                absent_marker_id,
                "fixture reset",
                True,
                expected_workload_id=absent_marker_id,
            )

        ok, messages, _ = acquire_lock(
            root=root,
            lock_type="branch",
            owner="fixture",
            workload_id="verification-dry-run",
            owner_process_id=os.getpid(),
            worktree=WORKTREE,
            branch=BRANCH,
            intended_write_set=TARGETS,
            expires="dry run",
            apply=False,
        )
        if not ok or list((root / "locks").glob("*verification-dry-run*")):
            raise AssertionError("verification-only dry-run created a lock:\n" + "\n".join(messages))

        unsafe, unsafe_messages, _ = acquire_lock(
            root=root,
            lock_type="branch",
            owner="fixture",
            workload_id="unsafe-target",
            owner_process_id=os.getpid(),
            worktree=WORKTREE,
            branch=BRANCH,
            intended_write_set="../outside.md;C:/absolute.md;central/selected_next_state.md",
            expires="dry run",
            apply=False,
        )
        if unsafe or not any("Target Invalid" in item for item in unsafe_messages):
            raise AssertionError("unsafe lock target set did not fail closed")

        locks_before_invalid_type = set((root / "locks").glob("*.json"))
        invalid_type_ok, invalid_type_messages, invalid_type_id = acquire_lock(
            root=root,
            lock_type="branch-typo",
            owner="fixture",
            workload_id="invalid-lock-type",
            owner_process_id=os.getpid(),
            worktree=WORKTREE,
            branch=BRANCH,
            intended_write_set=TARGETS,
            expires="fixture",
            apply=True,
        )
        if (
            invalid_type_ok
            or invalid_type_id != "INVALID-LOCK-TYPE-NOT-ACQUIRED"
            or not any("unsupported lock type" in item for item in invalid_type_messages)
            or set((root / "locks").glob("*.json")) != locks_before_invalid_type
        ):
            raise AssertionError(
                "callable acquire API accepted or materialized an unsupported lock type:\n"
                + "\n".join(invalid_type_messages)
            )
        try:
            with ExternalStateLockTransaction(
                root=root,
                lock_type="branch-typo",
                owner="fixture",
                workload_id="invalid-transaction-lock-type",
                owner_process_id=os.getpid(),
                worktree=WORKTREE,
                branch=BRANCH,
                intended_write_set=TARGETS,
                expires="fixture",
            ):
                raise AssertionError("unsupported transaction lock type entered its body")
        except ExternalStateError as exc:
            if "unsupported lock type" not in str(exc):
                raise
        else:
            raise AssertionError("transaction API accepted an unsupported lock type")
        _lock(root, "negative-verification-retained", "verification-replay")
        _assert_blocked(
            "verification replay retained lock",
            verify_final_lock_state(root, workload_id="verification-replay"),
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
        )
        _assert_blocked(
            "claimed zero without authoritative read",
            verify_final_lock_state(
                root,
                workload_id="verification-replay",
                require_global_zero=True,
                claimed_active_count=0,
            ),
            "Authoritative Active Lock Count Not Zero",
        )
        release_lock(
            root,
            "negative-verification-retained",
            "fixture reset",
            True,
            expected_workload_id="verification-replay",
        )

        # Positive: an active protected transaction holds one exact lock, then releases it.
        with _transaction(root, "positive-success") as transaction:
            active = [
                item
                for item in inspect_lock_table(
                    root,
                    current_workload_id="positive-success",
                    process_checker=lambda _pid: True,
                )
                if item.active
            ]
            if len(active) != 1 or active[0].lock_id != transaction.lock_id:
                raise AssertionError("active protected transaction did not hold one exact lock")
        _assert_released(root, "positive-success")

        # Positive: inspect-and-create is atomic across competing processes.
        context = multiprocessing.get_context("spawn")
        start = context.Event()
        results = context.Queue()
        contenders = [
            context.Process(
                target=_competing_acquire,
                args=(str(root), start, results, f"concurrent-{index}"),
            )
            for index in range(2)
        ]
        for contender in contenders:
            contender.start()
        start.set()
        concurrent_results = [results.get(timeout=15) for _ in contenders]
        for contender in contenders:
            contender.join(timeout=15)
            if contender.exitcode != 0:
                raise AssertionError(f"competing acquisition process failed: {contender.exitcode}")
        winners = [item for item in concurrent_results if item[1]]
        losers = [item for item in concurrent_results if not item[1]]
        if len(winners) != 1 or len(losers) != 1:
            raise AssertionError(f"competing acquisition was not atomic: {concurrent_results}")
        if not any("External State Owner Conflict" in message for message in losers[0][2]):
            raise AssertionError(f"competing acquisition did not report owner conflict: {losers[0]}")
        release_lock(
            root,
            winners[0][3],
            "fixture concurrent acquisition cleanup",
            True,
            expected_workload_id=winners[0][0],
        )
        _assert_released(root, winners[0][0])

        # Positive: blocked, validation-failed, exception, and partial-write exits use finally cleanup.
        for workload_id, error_type in (
            ("positive-blocked", FixtureBlocked),
            ("positive-validation-failure", FixtureValidationFailure),
            ("positive-exception", RuntimeError),
            ("positive-multi-target-failure", OSError),
            ("positive-packet-generation-failure", RuntimeError),
            ("positive-post-write-currentness-failure", FixtureValidationFailure),
            ("positive-user-gate-stop", FixtureBlocked),
            ("positive-cancellation", KeyboardInterrupt),
        ):
            try:
                with _transaction(root, workload_id):
                    raise error_type(workload_id)
            except error_type:
                pass
            else:
                raise AssertionError(f"{workload_id} fixture did not raise")
            _assert_released(root, workload_id)

        # Positive: a later workload gets a fresh lock ID.
        with _transaction(root, "positive-later-one") as first:
            first_id = first.lock_id
        with _transaction(root, "positive-later-two") as second:
            second_id = second.lock_id
        if first_id == second_id:
            raise AssertionError("later workload inherited the previous lock ID")
        _assert_released(root, "positive-later-two")

        # Positive: foreign active lock is preserved and overlapping acquisition blocks.
        foreign_path = _lock(root, "positive-foreign-active", "foreign-workload")
        foreign = inspect_lock_table(
            root,
            current_workload_id="local-workload",
            process_checker=lambda _pid: True,
        )
        foreign_row = next(item for item in foreign if item.lock_id == "positive-foreign-active")
        if foreign_row.classification != "FOREIGN_ACTIVE":
            raise AssertionError(f"foreign lock classified as {foreign_row.classification}")
        acquired, acquire_messages, _ = acquire_lock(
            root=root,
            lock_type="branch",
            owner="fixture",
            workload_id="local-workload",
            owner_process_id=os.getpid(),
            worktree=WORKTREE,
            branch=BRANCH,
            intended_write_set=TARGETS,
            expires="fixture",
            apply=True,
        )
        if acquired or not any("External State Owner Conflict" in item for item in acquire_messages):
            raise AssertionError("foreign active overlapping lock did not block acquisition")
        if json.loads(foreign_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("foreign active lock was mutated")
        release_lock(
            root,
            "positive-foreign-active",
            "fixture reset",
            True,
            expected_workload_id="foreign-workload",
        )

        # Positive: a disjoint foreign lock is reported but not misattributed at final return.
        _lock(
            root,
            "positive-foreign-disjoint",
            "foreign-disjoint",
            targets="branches/other/branch_state.md",
        )
        local_final_ok, local_final_messages = verify_final_lock_state(
            root,
            workload_id="completed-local",
            require_global_zero=False,
        )
        if not local_final_ok or not any(
            "Authoritative Active Lock Count: 1" in item for item in local_final_messages
        ):
            raise AssertionError(
                "disjoint foreign lock was not preserved and reported correctly:\n"
                + "\n".join(local_final_messages)
            )
        release_lock(
            root,
            "positive-foreign-disjoint",
            "fixture reset",
            True,
            expected_workload_id="foreign-disjoint",
        )

        _lock(
            root,
            "positive-casefold-overlap",
            "casefold-foreign",
            targets="CENTRAL/SELECTED_NEXT_STATE.MD",
        )
        casefold_ok, casefold_messages, _ = acquire_lock(
            root=root,
            lock_type="branch",
            owner="fixture",
            workload_id="casefold-local",
            owner_process_id=os.getpid(),
            worktree=WORKTREE,
            branch=BRANCH,
            intended_write_set="central/selected_next_state.md",
            expires="fixture",
            apply=False,
        )
        if casefold_ok or not any("External State Owner Conflict" in item for item in casefold_messages):
            raise AssertionError("case-insensitive overlapping target did not block")
        release_lock(
            root,
            "positive-casefold-overlap",
            "fixture reset",
            True,
            expected_workload_id="casefold-foreign",
        )

        for lock_id, existing_target, requested_target in (
            (
                "positive-ancestor-overlap",
                "snapshots/run",
                "snapshots/run/central/state.md",
            ),
            (
                "positive-descendant-overlap",
                "snapshots/run/central/state.md",
                "snapshots/run",
            ),
        ):
            _lock(root, lock_id, f"{lock_id}-workload", targets=existing_target)
            overlap_ok, overlap_messages, _ = acquire_lock(
                root=root,
                lock_type="branch",
                owner="fixture",
                workload_id=f"{lock_id}-request",
                owner_process_id=os.getpid(),
                worktree=WORKTREE,
                branch=BRANCH,
                intended_write_set=requested_target,
                expires="fixture",
                apply=False,
            )
            if overlap_ok or not any(
                "External State Owner Conflict" in item for item in overlap_messages
            ):
                raise AssertionError(
                    f"ancestor/descendant overlapping target did not block: {lock_id}"
                )
            release_lock(
                root,
                lock_id,
                "fixture reset",
                True,
                expected_workload_id=f"{lock_id}-workload",
            )

        # Negative: stale classification cannot release a payload reactivated before CAS.
        stale_race_path = _lock(
            root,
            "negative-stale-reactivated",
            "stale-reactivated-workload",
            workload_state="Completed",
        )
        original_stale_release_seam = lock_lifecycle._before_stale_release_cas

        def _reactivate_stale_lock(lock_path: Path, _expected_sha256: str) -> None:
            payload = json.loads(lock_path.read_text(encoding="utf-8"))
            payload["Workload State"] = "Active"
            payload["Owning Process ID"] = os.getpid()
            payload["Last Activity At"] = "2026-01-01T00:00:01Z"
            atomic_write_json(lock_path, payload)

        lock_lifecycle._before_stale_release_cas = _reactivate_stale_lock
        try:
            stale_race_result = release_stale_completed_lock(
                root,
                lock_id="negative-stale-reactivated",
                expected_workload_id="stale-reactivated-workload",
                reason="must not release a reactivated workload",
                apply=True,
                process_checker=lambda _pid: False,
            )
        finally:
            lock_lifecycle._before_stale_release_cas = original_stale_release_seam
        _assert_blocked(
            "stale lock reactivated before release",
            stale_race_result,
            "changed since stale classification",
        )
        stale_race_payload = json.loads(stale_race_path.read_text(encoding="utf-8"))
        if (
            stale_race_payload.get("Lock State") != "Locked"
            or stale_race_payload.get("Workload State") != "Active"
        ):
            raise AssertionError("stale-release CAS failure mutated the reactivated lock")
        release_lock(
            root,
            "negative-stale-reactivated",
            "fixture reset",
            True,
            expected_workload_id="stale-reactivated-workload",
        )

        # Positive: proven stale completed-workload lock is safely released, never deleted.
        stale_path = _lock(
            root,
            "positive-stale-cleanup",
            "stale-workload",
            workload_state="Completed",
        )
        cleaned, cleanup_messages = release_stale_completed_lock(
            root,
            lock_id="positive-stale-cleanup",
            expected_workload_id="stale-workload",
            reason="fixture stale completed-workload cleanup",
            apply=True,
            process_checker=lambda _pid: False,
        )
        if not cleaned or not stale_path.exists():
            raise AssertionError("stale cleanup failed or deleted its audit receipt:\n" + "\n".join(cleanup_messages))
        if json.loads(stale_path.read_text(encoding="utf-8"))["Lock State"] != "Released":
            raise AssertionError("stale cleanup did not mark the authoritative entry Released")

        for recoverable_state in (
            "Expired",
            "Stale",
            "Conflict",
            "Recovery Required",
        ):
            state_slug = recoverable_state.casefold().replace(" ", "-")
            recoverable_id = f"positive-stale-{state_slug}"
            recoverable_workload = f"stale-{state_slug}-workload"
            recoverable_path = _lock(
                root,
                recoverable_id,
                recoverable_workload,
                state=recoverable_state,
                workload_state="Completed",
            )
            recovered, recovery_messages = release_stale_completed_lock(
                root,
                lock_id=recoverable_id,
                expected_workload_id=recoverable_workload,
                reason=f"fixture recovery from {recoverable_state}",
                apply=True,
                process_checker=lambda _pid: False,
            )
            recovered_payload = json.loads(recoverable_path.read_text(encoding="utf-8"))
            if not recovered or recovered_payload.get("Lock State") != "Released":
                raise AssertionError(
                    f"stale cleanup could not release {recoverable_state}:\n"
                    + "\n".join(recovery_messages)
                )

        # Unknown process ownership is not proof that stale cleanup is safe.
        _lock(
            root,
            "negative-stale-process-unproven",
            "stale-process-unproven",
            workload_state="Completed",
            process_id="Not recorded",
        )
        _assert_blocked(
            "stale cleanup without process proof",
            release_stale_completed_lock(
                root,
                lock_id="negative-stale-process-unproven",
                expected_workload_id="stale-process-unproven",
                reason="must remain blocked",
                apply=True,
            ),
            "not proven stale completed workload",
        )
        release_lock(
            root,
            "negative-stale-process-unproven",
            "fixture reset",
            True,
            expected_workload_id="stale-process-unproven",
        )

        inaccessible_path = _lock(
            root,
            "negative-inaccessible-owner",
            "inaccessible-owner-workload",
            workload_state="Completed",
        )
        inaccessible = inspect_lock_table(
            root,
            current_workload_id="inaccessible-owner-workload",
            process_checker=lambda _pid: None,
        )
        inaccessible_row = next(
            item
            for item in inaccessible
            if item.lock_id == "negative-inaccessible-owner"
        )
        if inaccessible_row.process_running is not None or inaccessible_row.classification != "ACTIVE_VALID":
            raise AssertionError(
                "inaccessible owner process was treated as confirmed absent"
            )
        _assert_blocked(
            "inaccessible owner stale cleanup",
            release_stale_completed_lock(
                root,
                lock_id="negative-inaccessible-owner",
                expected_workload_id="inaccessible-owner-workload",
                reason="inaccessible process must remain protected",
                apply=True,
                process_checker=lambda _pid: None,
            ),
            "not proven stale completed workload",
        )
        if json.loads(inaccessible_path.read_text(encoding="utf-8"))["Lock State"] != "Locked":
            raise AssertionError("inaccessible owner cleanup mutated the lock")
        release_lock(
            root,
            "negative-inaccessible-owner",
            "fixture reset",
            True,
            expected_workload_id="inaccessible-owner-workload",
        )

        # Expired is still unreleased and cannot pass a final return gate.
        _lock(root, "negative-expired", "expired-workload", state="Expired")
        _assert_blocked(
            "expired lock retained",
            verify_final_lock_state(root, workload_id="expired-workload"),
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED",
        )
        release_lock(
            root,
            "negative-expired",
            "fixture reset",
            True,
            expected_workload_id="expired-workload",
        )

        _assert_released(root, "fixture-final")

    print("External-state lock lifecycle fixture validation: PASS")
    print("Public final-lock gate with retained completed-workload lock: BLOCKED as required")
    print("Public final-lock gate after authoritative release: PASS")
    print("Negative fixtures: 10 requested classes plus expired-lock final-gate coverage PASS")
    print("Positive fixtures: 8 requested classes PASS")
    print("Concurrent acquisition and unknown-process stale-cleanup hardening: PASS")
    print("Final successful fixture workload active-lock count: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
