"""Positive and negative fixtures for workload-scoped external-state locks."""

from __future__ import annotations

import json
import multiprocessing
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from orin_external_state_common import atomic_write_json
from orin_external_state_lock import acquire_lock
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

        # Negative: a dead process does not make an active workload safe to release.
        _lock(root, "negative-dead-owner", "dead-owner")
        dead = inspect_lock_table(
            root,
            current_workload_id="dead-owner",
            process_checker=lambda _pid: False,
        )
        dead_row = next(item for item in dead if item.lock_id == "negative-dead-owner")
        if dead_row.classification != "ACTIVE_VALID":
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
