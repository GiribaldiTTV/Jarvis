"""Inspect and enforce workload-scoped external-state lock lifecycles."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import os
import re
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from orin_external_state_common import (
    DEFAULT_EXTERNAL_STATE_ROOT,
    ExternalStateError,
    load_json,
    resolve_path,
    validate_canonical_root,
    validate_initialized_root,
)


NON_RELEASED_LOCK_STATES = {
    "Locked",
    "Expired",
    "Stale",
    "Conflict",
    "Recovery Required",
}
LOCK_TYPES = {
    "state-root",
    "migration",
    "release-window",
    "worktree",
    "branch",
    "review-bundle",
    "fold-down",
    "governance-candidate",
}
COMPLETED_WORKLOAD_STATES = {
    "Completed",
    "Blocked",
    "Cancelled",
    "Failed",
    "Idle",
    "Waiting For USER",
    "Waiting For Approval",
}


@dataclass(frozen=True)
class LockInspection:
    path: Path
    lock_id: str
    lock_state: str
    lock_type: str
    workload_id: str
    workload_state: str
    owner: str
    owner_process_id: int | None
    process_running: bool | None
    intended_write_set: str
    acquired_at: str
    last_activity_at: str
    classification: str
    active: bool
    error: str = ""


def _windows_kernel32():
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    kernel32.OpenProcess.restype = ctypes.c_void_p
    kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    kernel32.GetExitCodeProcess.restype = ctypes.c_int
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p]
    kernel32.CreateMutexW.restype = ctypes.c_void_p
    kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.WaitForSingleObject.restype = ctypes.c_uint32
    kernel32.ReleaseMutex.argtypes = [ctypes.c_void_p]
    kernel32.ReleaseMutex.restype = ctypes.c_int
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int
    return kernel32


def _process_is_running(process_id: int) -> bool:
    if process_id <= 0:
        return False
    if os.name == "nt":
        process_query_limited_information = 0x1000
        still_active = 259
        kernel32 = _windows_kernel32()
        handle = kernel32.OpenProcess(
            process_query_limited_information,
            False,
            process_id,
        )
        if not handle:
            return False
        try:
            exit_code = ctypes.c_ulong()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                return False
            return exit_code.value == still_active
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(process_id, 0)
    except OSError:
        return False
    return True


def _owner_process_id(payload: dict[str, object]) -> int | None:
    value = payload.get("Owning Process ID")
    if isinstance(value, int) and value > 0:
        return value
    if isinstance(value, str) and value.isdigit() and int(value) > 0:
        return int(value)
    return None


def _intended_write_set_is_valid(raw: str) -> bool:
    raw_targets = [item.strip().replace("\\", "/") for item in raw.split(";") if item.strip()]
    if not raw_targets:
        return False
    target_keys: list[str] = []
    for target in raw_targets:
        parts = target.split("/")
        if (
            target.startswith("/")
            or re.match(r"^[A-Za-z]:", target)
            or any(part in {"", ".", ".."} for part in parts)
        ):
            return False
        target_keys.append(target.casefold())
    return len(target_keys) == len(set(target_keys))


def inspect_lock_table(
    root: str | Path,
    *,
    current_workload_id: str | None = None,
    process_checker: Callable[[int], bool] | None = None,
) -> list[LockInspection]:
    """Read the authoritative lock directory on every call and classify every entry."""

    root = resolve_path(root)
    checker = process_checker or _process_is_running
    locks_dir = root / "locks"
    if not locks_dir.is_dir():
        return []
    inspections: list[LockInspection] = []
    for path in sorted(locks_dir.glob("*.json")):
        try:
            payload = load_json(path)
        except Exception as exc:  # noqa: BLE001 - malformed lock is a blocking classification
            inspections.append(
                LockInspection(
                    path=path,
                    lock_id=path.stem,
                    lock_state="MALFORMED",
                    lock_type="",
                    workload_id="",
                    workload_state="",
                    owner="",
                    owner_process_id=None,
                    process_running=None,
                    intended_write_set="",
                    acquired_at="",
                    last_activity_at="",
                    classification="MALFORMED",
                    active=False,
                    error=str(exc),
                )
            )
            continue

        lock_id = str(payload.get("Lock ID", ""))
        lock_state = str(payload.get("Lock State", ""))
        lock_type = str(payload.get("Lock Type", ""))
        workload_id = str(payload.get("Workload ID", ""))
        workload_state = str(payload.get("Workload State", ""))
        intended_write_set = str(payload.get("Intended Write Set", ""))
        process_id = _owner_process_id(payload)
        process_running = checker(process_id) if process_id is not None else None
        identity_malformed = (
            lock_id != path.stem
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", lock_id)
            or lock_state not in NON_RELEASED_LOCK_STATES | {"Released"}
        )
        conflict_metadata_malformed = (
            lock_type not in LOCK_TYPES
            or not _intended_write_set_is_valid(intended_write_set)
        )
        malformed = identity_malformed or (
            lock_state != "Released" and conflict_metadata_malformed
        )
        active = lock_state in NON_RELEASED_LOCK_STATES
        if malformed:
            classification = "MALFORMED"
        elif lock_state == "Released":
            classification = "RELEASED_RESIDUE"
        elif not workload_id:
            classification = "MALFORMED"
        elif (
            process_running is False
            and workload_state in COMPLETED_WORKLOAD_STATES
        ):
            classification = "STALE_COMPLETED_WORKLOAD"
        elif current_workload_id and workload_id != current_workload_id:
            classification = "FOREIGN_ACTIVE"
        else:
            classification = "ACTIVE_VALID"
        inspections.append(
            LockInspection(
                path=path,
                lock_id=lock_id or path.stem,
                lock_state=lock_state,
                lock_type=lock_type,
                workload_id=workload_id,
                workload_state=workload_state,
                owner=str(payload.get("Last Updated By", "")),
                owner_process_id=process_id,
                process_running=process_running,
                intended_write_set=intended_write_set,
                acquired_at=str(payload.get("Acquired At", payload.get("Last Updated", ""))),
                last_activity_at=str(payload.get("Last Activity At", payload.get("Last Updated", ""))),
                classification=classification,
                active=active,
                error="invalid lock identity, state, type, or intended write set" if malformed else "",
            )
        )
    return inspections


@contextmanager
def lock_table_guard(root: str | Path, *, attempts: int = 100, delay: float = 0.02):
    """Serialize inspect-and-create without representing the guard as a workload lock."""

    root = resolve_path(root)
    if os.name == "nt":
        wait_object_0 = 0x00000000
        wait_abandoned = 0x00000080
        mutex_name = (
            "Local\\NDAIExternalStateLockTable-"
            + hashlib.sha256(str(root).casefold().encode("utf-8")).hexdigest()[:24]
        )
        kernel32 = _windows_kernel32()
        handle = kernel32.CreateMutexW(None, False, mutex_name)
        if not handle:
            raise ExternalStateError(
                "BLOCKED_BY_FOREIGN_EXTERNAL_STATE_LOCK: lock-table mutex creation failed"
            )
        timeout_ms = max(1, int(attempts * delay * 1000))
        wait_result = kernel32.WaitForSingleObject(handle, timeout_ms)
        acquired = wait_result in {wait_object_0, wait_abandoned}
        if not acquired:
            kernel32.CloseHandle(handle)
            raise ExternalStateError(
                "BLOCKED_BY_FOREIGN_EXTERNAL_STATE_LOCK: lock-table acquisition guard is busy"
            )
        try:
            yield
        finally:
            kernel32.ReleaseMutex(handle)
            kernel32.CloseHandle(handle)
        return

    guard_path = root / "locks" / ".lock_table.guard"
    guard_path.parent.mkdir(parents=True, exist_ok=True)
    handle = guard_path.open("a+b")
    if guard_path.stat().st_size == 0:
        handle.write(b"\0")
        handle.flush()
    acquired = False
    try:
        for _ in range(attempts):
            handle.seek(0)
            try:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                time.sleep(delay)
                continue
            acquired = True
            break
        if not acquired:
            raise ExternalStateError(
                "BLOCKED_BY_FOREIGN_EXTERNAL_STATE_LOCK: lock-table acquisition guard is busy"
            )
        yield
    finally:
        if acquired:
            handle.seek(0)
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def verify_final_lock_state(
    root: str | Path,
    *,
    workload_id: str,
    require_global_zero: bool = False,
    claimed_active_count: int | None = None,
) -> tuple[bool, list[str]]:
    """Independently reread the table; caller claims never substitute for the read."""

    root = resolve_path(root)
    failures = validate_canonical_root(root)
    failures.extend(validate_initialized_root(root))
    if not workload_id.strip():
        failures.append("Completed Workload Identity Missing")
    inspections = inspect_lock_table(root, current_workload_id=workload_id)
    malformed = [item for item in inspections if item.classification == "MALFORMED"]
    active = [item for item in inspections if item.active]
    workload_active = [item for item in active if item.workload_id == workload_id]
    if malformed:
        failures.extend(
            f"External State Corrupt: malformed lock entry {item.path}" for item in malformed
        )
    if workload_active:
        failures.append(
            "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED: completed workload retains "
            + ", ".join(item.lock_id for item in workload_active)
        )
    if require_global_zero and active:
        failures.append(
            "Authoritative Active Lock Count Not Zero: "
            + ", ".join(item.lock_id for item in active)
        )
    messages = [
        f"Claimed Active Lock Count: {claimed_active_count if claimed_active_count is not None else 'Not supplied'}",
        "Authoritative Lock Table Read: PASS",
        f"Completed Workload Active Lock Count: {len(workload_active)}",
        f"Authoritative Active Lock Count: {len(active)}",
    ]
    return not failures, [*messages, *failures]


def release_stale_completed_lock(
    root: str | Path,
    *,
    lock_id: str,
    expected_workload_id: str,
    reason: str,
    apply: bool,
    process_checker: Callable[[int], bool] | None = None,
) -> tuple[bool, list[str]]:
    inspections = inspect_lock_table(
        root,
        current_workload_id=expected_workload_id,
        process_checker=process_checker,
    )
    matches = [item for item in inspections if item.lock_id == lock_id]
    if len(matches) != 1:
        return False, [f"Stale Lock Recovery Required: expected one lock {lock_id}, found {len(matches)}"]
    inspection = matches[0]
    if inspection.workload_id != expected_workload_id:
        return False, ["Stale Lock Recovery Required: workload identity mismatch"]
    if inspection.classification != "STALE_COMPLETED_WORKLOAD":
        return False, [
            "Stale Lock Recovery Required: lock is not proven stale completed workload; "
            f"classification is {inspection.classification}"
        ]
    from orin_external_state_lock_release import release_lock

    return release_lock(
        Path(root),
        lock_id,
        reason,
        apply,
        expected_workload_id=expected_workload_id,
    )


class ExternalStateLockTransaction:
    """Acquire and always release one exact lock around a protected workload block."""

    def __init__(
        self,
        *,
        root: str | Path,
        lock_type: str,
        owner: str,
        workload_id: str,
        worktree: str,
        branch: str,
        intended_write_set: str,
        expires: str,
        owner_process_id: int | None = None,
    ) -> None:
        self.root = resolve_path(root)
        self.lock_type = lock_type
        self.owner = owner
        self.workload_id = workload_id
        self.worktree = worktree
        self.branch = branch
        self.intended_write_set = intended_write_set
        self.expires = expires
        self.owner_process_id = owner_process_id or os.getpid()
        self.lock_id = ""

    def __enter__(self) -> "ExternalStateLockTransaction":
        from orin_external_state_lock import acquire_lock

        ok, messages, lock_id = acquire_lock(
            root=self.root,
            lock_type=self.lock_type,
            owner=self.owner,
            workload_id=self.workload_id,
            owner_process_id=self.owner_process_id,
            worktree=self.worktree,
            branch=self.branch,
            intended_write_set=self.intended_write_set,
            expires=self.expires,
            apply=True,
        )
        if not ok:
            raise ExternalStateError("; ".join(messages))
        self.lock_id = lock_id
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        from orin_external_state_lock_release import release_lock

        ok, release_messages = release_lock(
            self.root,
            self.lock_id,
            "Protected workload transaction completed or exited; guaranteed cleanup",
            True,
            expected_workload_id=self.workload_id,
        )
        verified, verify_messages = verify_final_lock_state(
            self.root,
            workload_id=self.workload_id,
            require_global_zero=False,
        )
        if not ok or not verified:
            cleanup_error = ExternalStateError(
                "BLOCKED_EXTERNAL_STATE_LOCK_RELEASE_FAILED: "
                + "; ".join([*release_messages, *verify_messages])
            )
            if exc is not None:
                raise cleanup_error from exc
            raise cleanup_error
        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect or verify external-state lock lifecycle.")
    parser.add_argument("--root", default=str(DEFAULT_EXTERNAL_STATE_ROOT))
    parser.add_argument("--workload-id")
    parser.add_argument("--verify-final", action="store_true")
    parser.add_argument("--require-global-zero", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.verify_final:
        inspections = inspect_lock_table(args.root, current_workload_id=args.workload_id)
        for item in inspections:
            print(
                f"{item.lock_id}: {item.classification}; state={item.lock_state}; "
                f"workload={item.workload_id or 'MISSING'}; owner={item.owner or 'MISSING'}; "
                f"process={item.owner_process_id or 'NOT_RECORDED'}; "
                f"process_running={item.process_running}; acquired={item.acquired_at or 'MISSING'}; "
                f"last_activity={item.last_activity_at or 'MISSING'}; "
                f"targets={item.intended_write_set or 'MISSING'}"
            )
        print(f"Authoritative Active Lock Count: {sum(item.active for item in inspections)}")
        return 0
    if not (args.workload_id or "").strip():
        print("External State Final Lock Gate")
        print("Completed Workload Identity Missing")
        print("Final Lock Gate Result: BLOCKED")
        return 1
    ok, messages = verify_final_lock_state(
        args.root,
        workload_id=args.workload_id,
        require_global_zero=args.require_global_zero,
    )
    print("External State Final Lock Gate")
    for message in messages:
        print(message)
    print(f"Final Lock Gate Result: {'PASS' if ok else 'BLOCKED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
