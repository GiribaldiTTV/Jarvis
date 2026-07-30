"""Adversarial fixtures for target-scoped external-state currentness."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import orin_external_state_validation as validator
import orin_external_state_lock_release as lock_release
import orin_external_state_target_reconcile as reconciler
from orin_external_state_common import atomic_write_json


TARGET = "worktrees/Governance/worktree_state.md"
HEAD = "a" * 40
ORIGIN_MAIN = "b" * 40
WORKTREE_PATH = r"C:\Nexus Worktrees\Governance"
SLOT = "governance-standing"

REAL_LEGACY_COMPLETION_ASSIGNMENTS = {
    "receipt-1": [
        "External State Item Status=RRI-20260727-001 current-gate autonomous-repair implementation and validation complete in the Governance worktree; durability is blocked only by the standing-gate neutral-main fast-forward requirement",
        "Current Validation State=Current-gate semantic contract, canonical publication, target-set rollback, lock lifecycle, governance, source-owner, packet false-green, public boundary, and external currentness checks PASS; standing Governance intake gate is expected RED only for dirty tracked files and stale neutral main",
        "Final Disposition=Current-gate implementation and validation are complete but not durable; one consolidated USER decision for neutral-main fast-forward is required before standing-gate validation, commit, and push can complete",
    ],
    "receipt-2": [
        "External State Item Status=RRI-20260727-001 current-gate autonomous-repair implementation, same-gate allowlist repair, validation, commit, and feature-branch push are complete; PR Readiness Stage 1 is not started",
        "Final Disposition=RRI-20260727-001 current-gate repair is durable at pushed HEAD 52fd1238145fedf222c79371f42e601dac833680; no PR exists; next gate is separate USER approval for PR Readiness Stage 1 analysis only",
        "Current Validation State=Complete routed validation contract PASS at pushed HEAD 52fd1238145fedf222c79371f42e601dac833680, including the 7114-check standing Governance intake gate; clean worktree and explicit feature-branch push verified",
    ],
    "receipt-3": [
        "External State Item Status=PR Readiness Stage 1 projection-ownership false green is repaired, committed, pushed, packeted, and externally reconciled; Stage 1 is ready for separate Stage 2 USER review",
        "Current Validation State=Complete routed PR Readiness Stage 1 contract PASS at pushed commit 771caab90b0be290227ea67ba2778c41496a06f9; omitted-live-projection and historical-route negative fixtures PASS; canonical packet parity/current identity PASS; governed four-record target-set publication PASS",
        r"Final Disposition=PR Readiness Stage 1 is complete at pushed commit 771caab90b0be290227ea67ba2778c41496a06f9 with canonical packet C:\Nexus USER\Governance-20260727-162840.zip; stale pr_readiness_state.md is historical receipt evidence only; no PR exists; next gate is separate USER approval for Stage 2 and PR creation only",
    ],
}
PROFILE_BY_RECEIPT = {
    "receipt-1": "rri-20260727-001-current-gate",
    "receipt-2": "rri-20260727-001-durability-final",
    "receipt-3": "rri-20260727-001-pr1-projection",
}


def _target_path(root: Path) -> Path:
    """Build fixture targets with the host platform's path semantics."""

    return root.joinpath(*TARGET.split("/"))


def _manifest(root: Path, source_head: str = "c" * 40) -> None:
    (root / "state_manifest.json").write_text(
        json.dumps(
            {
                "External State Schema": "external-state-v1",
                "State Version": 1,
                "Last Updated": "2026-01-01T00:00:00Z",
                "Last Updated By": "fixture",
                "Root": str(root),
                "Worktree": "neutral-main",
                "Branch": "main",
                "Source Repo HEAD": source_head,
            }
        ),
        encoding="utf-8",
    )


def _record(
    root: Path,
    *,
    record_class: str = "Live Worktree Projection",
    branch: str = "feature/release-readiness-source-truth-intake",
    head: str = HEAD,
    origin_main: str = ORIGIN_MAIN,
    worktree_path: str = WORKTREE_PATH,
    slot: str = SLOT,
) -> Path:
    target = _target_path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "\n".join(
            [
                "# Target Currentness Fixture",
                "External State Schema: `external-state-v1`",
                "State Version: `1`",
                "Last Updated: `2026-01-01T00:00:00Z`",
                "Last Updated By: `fixture`",
                "Record Class: `" + record_class + "`",
                "Record Role: `Current worktree assignment projection`",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Worktree: `Governance`",
                "Worktree Path: `" + worktree_path + "`",
                "Branch: `" + branch + "`",
                "Source Repo HEAD: `" + head + "`",
                "Origin/Main: `" + origin_main + "`",
                "Slot ID: `" + slot + "`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return target


def _expectations(target: Path) -> dict[str, str]:
    return {
        "expected_branch": "feature/release-readiness-source-truth-intake",
        "expected_source_head": HEAD,
        "expected_origin_main": ORIGIN_MAIN,
        "expected_worktree_path": WORKTREE_PATH,
        "expected_worktree_slot": SLOT,
        "expected_target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    }


def _snapshot(
    root: Path,
    target: Path,
    name: str,
    *,
    include_target: bool = True,
    snapshot_bytes: bytes | None = None,
    manifest_root: str | None = None,
    manifest_hash: str | None = None,
) -> Path:
    snapshot = root / "snapshots" / name
    snapshot.mkdir(parents=True)
    if include_target:
        snapshot_target = _target_path(snapshot)
        snapshot_target.parent.mkdir(parents=True, exist_ok=True)
        snapshot_target.write_bytes(snapshot_bytes if snapshot_bytes is not None else target.read_bytes())
    target_hash = manifest_hash
    if target_hash is None and include_target:
        target_hash = hashlib.sha256(
            _target_path(snapshot).read_bytes()
        ).hexdigest()
    atomic_write_json(
        snapshot / "snapshot_manifest.json",
        {
            "External State Schema": "external-state-v1",
            "State Version": 1,
            "Last Updated": "2026-01-01T00:00:00Z",
            "Last Updated By": "fixture",
            "Root": manifest_root or str(root.resolve()),
            "Copied Files": [
                {
                    "path": TARGET,
                    "sha256": target_hash or "",
                }
            ],
        },
    )
    return snapshot


def _run(root: Path, targets: list[str] | None = None, **overrides: str | None) -> list[str]:
    target = _target_path(root)
    values = _expectations(target)
    values.update(overrides)
    return validator.validate_target_currentness(
        root,
        targets or [TARGET],
        expected_schema="external-state-v1",
        **values,
    )


def _assert_pass(name: str, failures: list[str]) -> None:
    if failures:
        raise AssertionError(f"{name} unexpectedly failed:\n" + "\n".join(failures))


def _assert_failure(name: str, needle: str, failures: list[str]) -> None:
    if not any(needle in failure for failure in failures):
        raise AssertionError(f"{name} did not fail on {needle!r}:\n" + "\n".join(failures))


def _write_legacy_journal_fixture(
    root: Path,
    *,
    filename: str = "legacy-completed.json",
    target_count: int = 3,
    include_post_record_state: bool = False,
    completion_assignment: bool = True,
    completion_assignment_value: str | None = None,
    completion_assignments: list[str] | None = None,
    lock_state: str = "Released",
    lock_workload_id: str | None = None,
    recovery_payload: bool = False,
    inconsistent_snapshot_hash: bool = False,
    first_target_override: str | None = None,
) -> Path:
    audit_path = root / "audit_log" / filename
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    lock_id = "worktree-legacy-fixture"
    workload_id = "legacy-completed-workload"
    snapshot_relative = "snapshots/legacy-completed"
    snapshot_root = root / "snapshots" / "legacy-completed"
    snapshot_root.mkdir(parents=True, exist_ok=True)
    targets: list[dict[str, object]] = []
    copied_files: list[dict[str, object]] = []
    target_paths: list[str] = []
    for index in range(1, target_count + 1):
        relative = f"worktrees/Fixture-{index}/worktree_state.md"
        before_bytes = f"legacy before {index}\n".encode()
        before_hash = hashlib.sha256(before_bytes).hexdigest()
        after_hash = hashlib.sha256(f"legacy after {index}\n".encode()).hexdigest()
        snapshot_copy = snapshot_root.joinpath(*relative.split("/"))
        snapshot_copy.parent.mkdir(parents=True, exist_ok=True)
        snapshot_copy.write_bytes(before_bytes)
        manifest_hash = "f" * 64 if inconsistent_snapshot_hash and index == 1 else before_hash
        copied_files.append({"path": relative, "sha256": manifest_hash, "size": len(before_bytes)})
        assignments = [
            "State Version=2",
            "Last Updated=2026-07-27T20:00:00Z",
            "Last Updated By=fixture",
        ]
        if completion_assignment:
            assignments.extend(
                completion_assignments
                or (
                    [completion_assignment_value]
                    if completion_assignment_value is not None
                    else REAL_LEGACY_COMPLETION_ASSIGNMENTS["receipt-1"]
                )
            )
        row: dict[str, object] = {
            "Additions": [],
            "After SHA256": after_hash,
            "Assignments": assignments,
            "Before SHA256": before_hash,
            "Section Renames": [],
            "Target": relative,
        }
        if first_target_override is not None and index == 1:
            row["Target"] = first_target_override
        if include_post_record_state:
            row["Post Record State"] = "live"
        if recovery_payload and index == 1:
            row["Before Text"] = before_bytes.decode()
        targets.append(row)
        target_paths.append(relative)
    atomic_write_json(
        snapshot_root / "snapshot_manifest.json",
        {
            "External State Schema": "external-state-v1",
            "Root": str(root.resolve()),
            "Copied Files": copied_files,
            "Last Updated": "2026-07-27T19:59:00Z",
        },
    )
    atomic_write_json(
        root / "locks" / f"{lock_id}.json",
        {
            "External State Schema": "external-state-v1",
            "Lock ID": lock_id,
            "Lock State": lock_state,
            "Workload ID": lock_workload_id or workload_id,
            "Workload State": "Completed" if lock_state == "Released" else "Active",
            "Released At": "2026-07-27T20:01:00Z" if lock_state == "Released" else "",
            "Retain Between Workloads": "No",
            "Intended Write Set": ";".join(
                [audit_path.relative_to(root).as_posix(), snapshot_relative, *target_paths]
            ),
        },
    )
    atomic_write_json(
        audit_path,
        {
            "External State Schema": "external-state-v1",
            "Last Updated": "2026-07-27T20:00:00Z",
            "Last Updated By": "fixture",
            "Lock ID": lock_id,
            "Snapshot": snapshot_relative,
            "Targets": targets,
            "Transition": validator.TARGET_SET_TRANSITION,
            "Workload ID": workload_id,
        },
    )
    return audit_path


def _write_legacy_lock_write_set_extra_fixture(root: Path) -> Path:
    path = _write_legacy_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    lock_path = root / "locks" / f"{payload['Lock ID']}.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Intended Write Set"] += ";worktrees/Unjournaled/state.md"
    atomic_write_json(lock_path, lock)
    return path


def _write_legacy_padded_lock_field_fixture(root: Path, field: str) -> Path:
    path = _write_legacy_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    lock_path = root / "locks" / f"{payload['Lock ID']}.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock[field] = f" {lock[field]} "
    atomic_write_json(lock_path, lock)
    return path


def _write_legacy_released_at_fixture(root: Path, value: object) -> Path:
    path = _write_legacy_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    lock_path = root / "locks" / f"{payload['Lock ID']}.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Released At"] = value
    atomic_write_json(lock_path, lock)
    return path


def _write_legacy_snapshot_updated_fixture(root: Path, value: object) -> Path:
    path = _write_legacy_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    snapshot_root = root.joinpath(*payload["Snapshot"].split("/"))
    manifest_path = snapshot_root / "snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["Last Updated"] = value
    atomic_write_json(manifest_path, manifest)
    return path


def _write_legacy_receipt_updated_fixture(root: Path, value: object) -> Path:
    path = _write_legacy_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Last Updated"] = value
    atomic_write_json(path, payload)
    return path


def _write_legacy_completion_matrix_fixture(
    root: Path,
    completion_rows: list[list[object]],
    *,
    post_record_states: list[str | None] | None = None,
) -> Path:
    audit_path = _write_legacy_journal_fixture(root, target_count=len(completion_rows))
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    for index, (row, completion_assignments) in enumerate(
        zip(payload["Targets"], completion_rows)
    ):
        row["Assignments"] = [
            assignment
            for assignment in row["Assignments"]
            if not isinstance(assignment, str)
            or "=" not in assignment
            or assignment.split("=", 1)[0].strip().casefold()
            not in validator.LEGACY_COMPLETION_FIELDS
        ]
        row["Assignments"].extend(completion_assignments)
        if post_record_states is not None:
            state = post_record_states[index]
            if state is None:
                row.pop("Post Record State", None)
            else:
                row["Post Record State"] = state
    atomic_write_json(audit_path, payload)
    return audit_path


def _write_exact_real_legacy_receipt_fixture(root: Path, receipt: str) -> Path:
    if receipt == "receipt-1":
        rows = [
            REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt][0:2],
            REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt],
            REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt],
        ]
        return _write_legacy_completion_matrix_fixture(root, rows)
    if receipt == "receipt-2":
        return _write_legacy_completion_matrix_fixture(
            root,
            [REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt]] * 3,
        )
    rows = [
        REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt],
        REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt],
        REAL_LEGACY_COMPLETION_ASSIGNMENTS[receipt],
        [],
    ]
    return _write_legacy_completion_matrix_fixture(
        root,
        rows,
        post_record_states=["live", "live", "live", "historical-receipt"],
    )


def _write_fixture_compatibility_manifest(
    root: Path,
    audit_path: Path,
    profile: str,
    *,
    admitted_path: str | None = None,
    admitted_sha256: str | None = None,
) -> Path:
    rows: list[dict[str, str]] = []
    profiles = list(validator.LEGACY_COMPLETION_PROFILES)
    for index, profile_name in enumerate(profiles, start=1):
        if profile_name == profile:
            relative = admitted_path or audit_path.relative_to(root).as_posix()
            digest = admitted_sha256 or hashlib.sha256(audit_path.read_bytes()).hexdigest()
        else:
            relative = f"audit_log/unused-{index}.json"
            digest = str(index) * 64
        rows.append(
            {
                "Audit Path": relative,
                "SHA256": digest,
                "Compatibility Profile": profile_name,
                "Receipt Class": validator.LEGACY_RECEIPT_CLASS,
                "Immutable Purpose": validator.LEGACY_RECEIPT_PURPOSE,
            }
        )
    manifest_path = root / "fixture_legacy_receipt_compatibility.json"
    atomic_write_json(
        manifest_path,
        {
            "Schema": validator.LEGACY_RECEIPT_COMPATIBILITY_SCHEMA,
            "Purpose": validator.LEGACY_RECEIPT_PURPOSE,
            "Receipts": rows,
        },
    )
    return manifest_path


def _resolve_case_manifest(
    root: Path,
    setup_result: object,
    admitted_profile: str | None,
) -> Path:
    if (
        isinstance(setup_result, tuple)
        and len(setup_result) == 2
        and isinstance(setup_result[0], Path)
        and isinstance(setup_result[1], Path)
    ):
        return setup_result[1]
    if admitted_profile is not None:
        if not isinstance(setup_result, Path):
            raise AssertionError("admitted journal fixture did not return its audit path")
        return _write_fixture_compatibility_manifest(root, setup_result, admitted_profile)
    return validator.LEGACY_RECEIPT_COMPATIBILITY_MANIFEST


def _write_tampered_admitted_receipt_fixture(root: Path) -> tuple[Path, Path]:
    audit_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    manifest_path = _write_fixture_compatibility_manifest(
        root,
        audit_path,
        PROFILE_BY_RECEIPT["receipt-1"],
    )
    original = audit_path.read_bytes()
    tampered = original.replace(b'"Last Updated By": "fixture"', b'"Last Updated By": "fixturf"', 1)
    if tampered == original:
        raise AssertionError("tamper fixture did not alter the admitted receipt")
    audit_path.write_bytes(tampered)
    return audit_path, manifest_path


def _write_renamed_admitted_receipt_fixture(root: Path) -> tuple[Path, Path]:
    original_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    manifest_path = _write_fixture_compatibility_manifest(
        root,
        original_path,
        PROFILE_BY_RECEIPT["receipt-1"],
    )
    payload = json.loads(original_path.read_text(encoding="utf-8"))
    copied_path = original_path.with_name("copied-accepted-receipt.json")
    original_relative = original_path.relative_to(root).as_posix()
    copied_relative = copied_path.relative_to(root).as_posix()
    original_path.rename(copied_path)
    lock_path = root / "locks" / f"{payload['Lock ID']}.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Intended Write Set"] = str(lock["Intended Write Set"]).replace(
        original_relative,
        copied_relative,
    )
    atomic_write_json(lock_path, lock)
    return copied_path, manifest_path


def _write_case_renamed_admitted_receipt_fixture(root: Path) -> tuple[Path, Path]:
    original_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    manifest_path = _write_fixture_compatibility_manifest(
        root,
        original_path,
        PROFILE_BY_RECEIPT["receipt-1"],
    )
    payload = json.loads(original_path.read_text(encoding="utf-8"))
    case_path = original_path.with_name(original_path.name.swapcase())
    intermediate = original_path.with_name("case-rename-intermediate.tmp")
    original_relative = original_path.relative_to(root).as_posix()
    case_relative = case_path.relative_to(root).as_posix()
    original_path.rename(intermediate)
    intermediate.rename(case_path)
    lock_path = root / "locks" / f"{payload['Lock ID']}.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Intended Write Set"] = str(lock["Intended Write Set"]).replace(
        original_relative,
        case_relative,
    )
    atomic_write_json(lock_path, lock)
    return case_path, manifest_path


def _accept_registered_path_without_hash(
    root: Path,
    audit_path: Path,
    manifest_path: Path,
    _actual_digest: str,
) -> tuple[str | None, list[str]]:
    registry, issues = validator._load_legacy_receipt_compatibility_registry(manifest_path)
    if issues:
        return None, issues
    relative = audit_path.relative_to(root).as_posix().casefold()
    entry = registry.get(relative)
    if entry is None:
        return None, ["path not admitted"]
    return entry["Compatibility Profile"], []


def _accept_registered_hash_without_path(
    _root: Path,
    audit_path: Path,
    manifest_path: Path,
    actual_digest: str,
) -> tuple[str | None, list[str]]:
    registry, issues = validator._load_legacy_receipt_compatibility_registry(manifest_path)
    if issues:
        return None, issues
    for entry in registry.values():
        if entry["SHA256"] == actual_digest:
            return entry["Compatibility Profile"], []
    return None, ["hash not admitted"]


def _write_legacy_case_alias_fixture(root: Path) -> Path:
    audit_path = _write_legacy_journal_fixture(root, target_count=2)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["Targets"][1]["Target"] = payload["Targets"][0]["Target"].swapcase()
    atomic_write_json(audit_path, payload)
    return audit_path


def _write_modern_case_alias_fixture(root: Path) -> Path:
    audit_path = _write_modern_journal_fixture(root)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    alias = dict(payload["Targets"][0])
    alias["Target"] = alias["Target"].swapcase()
    payload["Targets"].append(alias)
    atomic_write_json(audit_path, payload)
    return audit_path


def _write_modern_noncanonical_transition_fixture(
    root: Path,
    *,
    key: str = "transition",
    value: str | None = None,
) -> Path:
    audit_path = _write_modern_journal_fixture(root)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload.pop("Transition")
    payload[key] = value or validator.TARGET_SET_TRANSITION
    atomic_write_json(audit_path, payload)
    return audit_path


def _write_modern_journal_fixture(
    root: Path,
    *,
    filename: str = "modern-journal.json",
    state: object = "Committed",
    include_state: bool = True,
    last_updated: str = "2026-07-28T00:00:00Z",
    schema: str = "external-state-v1",
    lock_state: str = "Released",
) -> Path:
    path = root / "audit_log" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    target_relative = "worktrees/Fixture/worktree_state.md"
    before_bytes = b"modern fixture before\n"
    after_bytes = b"modern fixture after\n"
    before_hash = hashlib.sha256(before_bytes).hexdigest()
    after_hash = hashlib.sha256(after_bytes).hexdigest()
    snapshot_relative = "snapshots/modern-fixture"
    snapshot_root = root.joinpath(*snapshot_relative.split("/"))
    snapshot_copy = snapshot_root.joinpath(*target_relative.split("/"))
    snapshot_copy.parent.mkdir(parents=True, exist_ok=True)
    snapshot_copy.write_bytes(before_bytes)
    atomic_write_json(
        snapshot_root / "snapshot_manifest.json",
        {
            "External State Schema": "external-state-v1",
            "Root": str(root.resolve()),
            "Copied Files": [
                {
                    "path": target_relative,
                    "sha256": before_hash,
                    "size": len(before_bytes),
                }
            ],
            "Last Updated": "2026-07-27T23:59:59Z",
        },
    )
    live_target = root.joinpath(*target_relative.split("/"))
    live_target.parent.mkdir(parents=True, exist_ok=True)
    live_target.write_bytes(after_bytes)
    payload: dict[str, object] = {
        "External State Schema": schema,
        "Transition": validator.TARGET_SET_TRANSITION,
        "Lock ID": "branch-modern-fixture",
        "Workload ID": "modern-fixture-workload",
        "Snapshot": snapshot_relative,
        "Targets": [
            {
                "Target": target_relative,
                "Before SHA256": before_hash,
                "After SHA256": after_hash,
            }
        ],
        "Last Updated": last_updated,
        "Last Updated By": "fixture",
    }
    if include_state:
        payload["Transaction State"] = state
    atomic_write_json(path, payload)
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        lock_path,
        {
            "External State Schema": "external-state-v1",
            "Lock ID": "branch-modern-fixture",
            "Lock State": lock_state,
            "Workload ID": "modern-fixture-workload",
            "Workload State": "Completed",
            "Retain Between Workloads": "No",
            "Released At": "2026-07-28T00:00:01Z",
            "Intended Write Set": ";".join(
                [
                    path.relative_to(root).as_posix(),
                    snapshot_relative,
                    target_relative,
                ]
            ),
        },
    )
    return path


def _write_modern_live_target_mismatch_fixture(root: Path, state: str) -> Path:
    path = _write_modern_journal_fixture(root)
    target = root / "worktrees" / "Fixture" / "worktree_state.md"
    if state == "missing":
        target.unlink()
    elif state == "before":
        target.write_bytes(b"modern fixture before\n")
    elif state == "unrelated":
        target.write_bytes(b"unrelated live target contents\n")
    else:
        raise AssertionError(f"unknown live target mismatch state {state!r}")
    return path


def _write_modern_journal_chain_fixture(root: Path, variant: str = "valid") -> Path:
    target_relative = "worktrees/Fixture/worktree_state.md"
    state_0 = b"modern chain state 0\n"
    state_1 = b"modern chain state 1\n"
    state_2 = b"modern chain state 2\n"
    disconnected = b"modern chain disconnected state\n"
    transitions = [
        ("chain-1", state_0, state_1, "2026-07-28T00:01:00Z"),
        ("chain-2", state_1, state_2, "2026-07-28T00:02:00Z"),
    ]
    if variant == "discontinuous":
        transitions[1] = ("chain-2", disconnected, state_2, "2026-07-28T00:02:00Z")
    elif variant == "ambiguous-timestamp":
        transitions[1] = ("chain-2", state_1, state_2, "2026-07-28T00:01:00Z")
    elif variant == "forked":
        transitions[1] = ("chain-2", state_0, state_2, "2026-07-28T00:02:00Z")
    elif variant == "reversed-chronology":
        transitions[0] = ("chain-1", state_0, state_1, "2026-07-28T00:02:00Z")
        transitions[1] = ("chain-2", state_1, state_2, "2026-07-28T00:01:00Z")
    elif variant == "two-step-cycle":
        transitions[1] = ("chain-2", state_1, state_0, "2026-07-28T00:02:00Z")
    elif variant == "longer-cycle":
        transitions.append(("chain-3", state_2, state_0, "2026-07-28T00:03:00Z"))
    elif variant not in {"valid", "latest-live-mismatch"}:
        raise AssertionError(f"unknown modern journal chain variant {variant!r}")

    for name, before_bytes, after_bytes, updated in transitions:
        before_hash = hashlib.sha256(before_bytes).hexdigest()
        after_hash = hashlib.sha256(after_bytes).hexdigest()
        audit_relative = f"audit_log/{name}.json"
        snapshot_relative = f"snapshots/{name}"
        lock_id = f"branch-{name}"
        workload_id = f"{name}-workload"
        snapshot_root = root.joinpath(*snapshot_relative.split("/"))
        snapshot_copy = snapshot_root.joinpath(*target_relative.split("/"))
        snapshot_copy.parent.mkdir(parents=True, exist_ok=True)
        snapshot_copy.write_bytes(before_bytes)
        updated_time = datetime.fromisoformat(updated.replace("Z", "+00:00"))
        snapshot_updated = (updated_time - timedelta(seconds=30)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        atomic_write_json(
            snapshot_root / "snapshot_manifest.json",
            {
                "External State Schema": "external-state-v1",
                "Root": str(root.resolve()),
                "Copied Files": [
                    {
                        "path": target_relative,
                        "sha256": before_hash,
                        "size": len(before_bytes),
                    }
                ],
                "Last Updated": snapshot_updated,
            },
        )
        audit_path = root.joinpath(*audit_relative.split("/"))
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(
            audit_path,
            {
                "External State Schema": "external-state-v1",
                "Transition": validator.TARGET_SET_TRANSITION,
                "Lock ID": lock_id,
                "Workload ID": workload_id,
                "Snapshot": snapshot_relative,
                "Targets": [
                    {
                        "Target": target_relative,
                        "Before SHA256": before_hash,
                        "After SHA256": after_hash,
                    }
                ],
                "Last Updated": updated,
                "Last Updated By": "fixture",
                "Transaction State": "Committed",
            },
        )
        lock_path = root / "locks" / f"{lock_id}.json"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(
            lock_path,
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Released",
                "Workload ID": workload_id,
                "Workload State": "Completed",
                "Retain Between Workloads": "No",
                "Released At": (updated_time + timedelta(seconds=30)).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                ),
                "Intended Write Set": ";".join(
                    [audit_relative, snapshot_relative, target_relative]
                ),
            },
        )

    live_target = root.joinpath(*target_relative.split("/"))
    live_target.parent.mkdir(parents=True, exist_ok=True)
    live_target.write_bytes(
        b"modern chain unrelated live bytes\n"
        if variant == "latest-live-mismatch"
        else state_0
        if variant in {"two-step-cycle", "longer-cycle"}
        else state_2
    )
    return root / "audit_log" / f"{transitions[-1][0]}.json"


def _write_modern_nested_audit_directory_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root, state="Prepared")
    nested_path = root / "audit_log" / "hidden" / "prepared.json"
    nested_path.parent.mkdir(parents=True, exist_ok=True)
    path.replace(nested_path)
    return nested_path


def _write_non_json_target_set_transaction_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root, state="Prepared")
    non_json_path = root / "audit_log" / "prepared.txt"
    path.replace(non_json_path)
    return non_json_path


def _write_utf16_non_json_target_set_transaction_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root, state="Prepared")
    text = path.read_text(encoding="utf-8")
    path.unlink()
    non_json_path = root / "audit_log" / "prepared.log"
    non_json_path.write_text(text, encoding="utf-16")
    return non_json_path


def _write_plain_text_target_set_transaction_fixture(
    root: Path,
    *,
    encoding: str = "utf-8",
) -> Path:
    audit_root = root / "audit_log"
    audit_root.mkdir(parents=True, exist_ok=True)
    suffix = ".log" if encoding == "utf-16" else ".txt"
    path = audit_root / f"prepared-plain{suffix}"
    path.write_text(
        "Transition: Bounded coherent target-set reconciliation\n"
        "Transaction State: Prepared\n",
        encoding=encoding,
    )
    return path


def _write_non_object_target_set_transaction_fixture(root: Path) -> Path:
    path = root / "audit_log" / "prepared-array.json"
    atomic_write_json(
        path,
        [
            {
                "Transition": validator.TARGET_SET_TRANSITION,
                "Transaction State": "Prepared",
            }
        ],
    )
    return path


def _write_wrapped_target_set_transaction_fixture(root: Path) -> Path:
    path = root / "audit_log" / "prepared-envelope.json"
    atomic_write_json(
        path,
        {
            "Envelope": {
                "Transition": validator.TARGET_SET_TRANSITION,
                "Transaction State": "Prepared",
            }
        },
    )
    return path


def _write_modern_recovery_alias_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Targets"][0]["before text"] = "recoverable target contents"
    atomic_write_json(path, payload)
    return path


def _write_modern_recovery_payload_fixture(root: Path, location: str) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if location == "top-level":
        payload["Before Text"] = "recoverable target contents"
    elif location == "nested":
        payload["Metadata"] = {"before text": "recoverable target contents"}
    else:
        raise AssertionError(f"unknown recovery payload location {location!r}")
    atomic_write_json(path, payload)
    return path


def _write_modern_recovery_payload_alias_fixture(root: Path, key: str) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Metadata"] = {key: "original target contents"}
    atomic_write_json(path, payload)
    return path


def _write_modern_missing_audit_metadata_fixture(root: Path, field: str) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.pop(field, None)
    atomic_write_json(path, payload)
    return path


def _write_modern_future_transaction_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(
        root,
        last_updated="2099-01-01T00:00:00Z",
    )
    manifest_path = root / "snapshots" / "modern-fixture" / "snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["Last Updated"] = "2098-12-31T23:59:59Z"
    atomic_write_json(manifest_path, manifest)
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Released At"] = "2099-01-01T00:00:01Z"
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_future_release_fixture(root: Path) -> Path:
    return _write_modern_released_at_fixture(root, "2099-01-01T00:00:00Z")


def _write_modern_equal_hash_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Targets"][0]["After SHA256"] = payload["Targets"][0]["Before SHA256"]
    atomic_write_json(path, payload)
    return path


def _write_modern_non_string_hash_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Targets"][0]["After SHA256"] = int("1" * 64)
    atomic_write_json(path, payload)
    return path


def _write_modern_target_value_fixture(root: Path, value: object) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Targets"][0]["Target"] = value
    atomic_write_json(path, payload)
    return path


def _write_modern_missing_snapshot_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    (root / "snapshots" / "modern-fixture" / "snapshot_manifest.json").unlink()
    return path


def _write_modern_snapshot_root_fixture(root: Path, value: str | None) -> Path:
    path = _write_modern_journal_fixture(root)
    manifest_path = root / "snapshots" / "modern-fixture" / "snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if value is None:
        manifest.pop("Root", None)
    else:
        manifest["Root"] = value
    atomic_write_json(manifest_path, manifest)
    return path


def _write_modern_snapshot_timestamp_fixture(
    root: Path,
    value: object | None,
) -> Path:
    path = _write_modern_journal_fixture(root)
    manifest_path = root / "snapshots" / "modern-fixture" / "snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if value is None:
        manifest.pop("Last Updated", None)
    else:
        manifest["Last Updated"] = value
    atomic_write_json(manifest_path, manifest)
    return path


def _write_modern_case_ambiguous_snapshot_root_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    manifest_path = root / "snapshots" / "modern-fixture" / "snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _write_json_with_field_pair(
        manifest_path,
        manifest,
        "Root",
        manifest["Root"],
        str(root.parent / "foreign-root"),
        second_key="root",
    )
    return path


def _write_modern_snapshot_namespace_root_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    snapshot_namespace = root / "snapshots"
    snapshot_root = snapshot_namespace / "modern-fixture"
    for item in list(snapshot_root.iterdir()):
        item.rename(snapshot_namespace / item.name)
    snapshot_root.rmdir()
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["Snapshot"] = "snapshots"
    atomic_write_json(path, payload)
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Intended Write Set"] = str(lock["Intended Write Set"]).replace(
        "snapshots/modern-fixture",
        "snapshots",
    )
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_tampered_snapshot_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    snapshot_copy = (
        root
        / "snapshots"
        / "modern-fixture"
        / "worktrees"
        / "Fixture"
        / "worktree_state.md"
    )
    snapshot_copy.write_text("tampered modern fixture\n", encoding="utf-8")
    return path


def _write_modern_snapshot_extra_file_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    snapshot_root = root / "snapshots" / "modern-fixture"
    extra_relative = "secrets.txt"
    extra_bytes = b"unrelated recoverable material\n"
    (snapshot_root / extra_relative).write_bytes(extra_bytes)
    manifest_path = snapshot_root / "snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["Copied Files"].append(
        {
            "path": extra_relative,
            "sha256": hashlib.sha256(extra_bytes).hexdigest(),
            "size": len(extra_bytes),
        }
    )
    atomic_write_json(manifest_path, manifest)
    return path


def _write_modern_snapshot_unmanifested_file_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    snapshot_root = root / "snapshots" / "modern-fixture"
    (snapshot_root / "unmanifested-secret.txt").write_text(
        "unrelated unmanifested recoverable material\n",
        encoding="utf-8",
    )
    return path


def _write_modern_lock_write_set_omission_fixture(root: Path, omitted: str) -> Path:
    path = _write_modern_journal_fixture(root)
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    entries = str(lock["Intended Write Set"]).split(";")
    omission_map = {
        "audit": path.relative_to(root).as_posix(),
        "snapshot": "snapshots/modern-fixture",
        "target": "worktrees/Fixture/worktree_state.md",
    }
    lock["Intended Write Set"] = ";".join(
        entry for entry in entries if entry != omission_map[omitted]
    )
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_lock_write_set_extra_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Intended Write Set"] += ";worktrees/Unjournaled/worktree_state.md"
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_non_string_lock_identity_fixture(root: Path, field: str) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    original_lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(original_lock_path.read_text(encoding="utf-8"))
    if field == "Workload ID":
        payload[field] = "123"
        lock[field] = 123
        lock_path = original_lock_path
    elif field == "Lock ID":
        payload[field] = "123"
        lock[field] = 123
        lock_path = root / "locks" / "123.json"
        original_lock_path.unlink()
    else:
        raise AssertionError(f"unknown modern lock identity field {field!r}")
    atomic_write_json(path, payload)
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_padded_lock_field_fixture(root: Path, field: str) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if field == "Workload ID":
        payload[field] = str(payload[field]) + " "
        lock[field] = str(lock[field]) + " "
        atomic_write_json(path, payload)
    else:
        lock[field] = str(lock[field]) + " "
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_deep_unrelated_metadata_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    nested: object = "unrelated metadata"
    for _ in range(500):
        nested = [nested]
    payload["Metadata"] = nested
    atomic_write_json(path, payload)
    return path


def _write_nested_malformed_value_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "nested-malformed-value-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":[1, {bad}], "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_missing_comma_before_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "missing-comma-before-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"x":1 "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '","Transaction State":"Prepared"}',
        encoding="utf-8",
    )
    return path


def _write_bare_transition_key_fixture(root: Path) -> Path:
    path = root / "audit_log" / "bare-transition-key.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{Transition:"'
        + validator.TARGET_SET_TRANSITION
        + '","Transaction State":"Prepared"}',
        encoding="utf-8",
    )
    return path


def _write_mismatched_nested_comma_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "mismatched-nested-comma-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":[1,{bad],more}], "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_mismatched_nested_string_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "mismatched-nested-string-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":[1,{bad],"more"}], "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_mismatched_nested_member_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "mismatched-nested-member-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":[1,{bad],"x":1}], "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_unmatched_inner_closer_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "unmatched-inner-closer-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":{bad],"x":1}, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_unmatched_inner_closer_array_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "unmatched-inner-closer-array-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":[bad},"x"], "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_root_frame_mismatched_closer_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "root-frame-mismatched-closer-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":[1}}, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_leading_junk_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "leading-junk-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        'x{"Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '","Transaction State":"Prepared"}',
        encoding="utf-8",
    )
    return path


def _write_quoted_junk_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "quoted-junk-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '"prefix { text" {"Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '","Transaction State":"Prepared"}',
        encoding="utf-8",
    )
    return path


def _write_modern_released_at_fixture(root: Path, value: object) -> Path:
    path = _write_modern_journal_fixture(root)
    lock_path = root / "locks" / "branch-modern-fixture.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["Released At"] = value
    atomic_write_json(lock_path, lock)
    return path


def _write_modern_whitespace_evidence_path_fixture(root: Path, location: str) -> Path:
    path = _write_modern_journal_fixture(root)
    if location == "journal target":
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["Targets"][0]["Target"] = " " + payload["Targets"][0]["Target"]
        atomic_write_json(path, payload)
    elif location == "snapshot root":
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["Snapshot"] += " "
        atomic_write_json(path, payload)
    elif location == "snapshot manifest path":
        manifest_path = root / "snapshots" / "modern-fixture" / "snapshot_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["Copied Files"][0]["path"] += " "
        atomic_write_json(manifest_path, manifest)
    elif location == "lock write set":
        lock_path = root / "locks" / "branch-modern-fixture.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["Intended Write Set"] = str(lock["Intended Write Set"]).replace(
            ";worktrees/Fixture/worktree_state.md",
            "; worktrees/Fixture/worktree_state.md",
        )
        atomic_write_json(lock_path, lock)
    else:
        raise AssertionError(f"unknown whitespace evidence location {location!r}")
    return path


def _write_modern_nonstandard_constant_fixture(root: Path, location: str) -> Path:
    path = _write_modern_journal_fixture(root)
    if location == "journal":
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["Unchecked Metadata"] = float("nan")
        atomic_write_json(path, payload)
    elif location == "lock":
        lock_path = root / "locks" / "branch-modern-fixture.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["Released At"] = float("nan")
        atomic_write_json(lock_path, lock)
    elif location == "snapshot":
        manifest_path = root / "snapshots" / "modern-fixture" / "snapshot_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["Unchecked Metadata"] = float("inf")
        atomic_write_json(manifest_path, manifest)
    else:
        raise AssertionError(f"unknown non-standard constant location {location!r}")
    return path


def _write_deeply_nested_json_fixture(root: Path, *, target_set: bool) -> Path:
    filename = "deep-target-set.json" if target_set else "deep-unrelated.json"
    path = root / "audit_log" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    prefix = (
        '{"Transition":"' + validator.TARGET_SET_TRANSITION + '","Nested":'
        if target_set
        else '{"Nested":'
    )
    depth = 100_000
    path.write_text(prefix + "[" * depth + "0" + "]" * depth + "}", encoding="utf-8")
    return path


def _write_malformed_nested_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "malformed-nested-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Metadata":{"Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"},',
        encoding="utf-8",
    )
    return path


def _write_mismatched_delimiter_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "mismatched-delimiter-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"junk":[},"Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_malformed_transition_value_fixture(root: Path) -> Path:
    path = root / "audit_log" / "malformed-transition-value.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"Transition":', encoding="utf-8")
    return path


def _write_invalid_escape_brace_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "invalid-escape-brace-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":"bad\\q {", "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_illegal_container_after_value_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "illegal-container-after-value-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":1 {, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_malformed_container_value_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "malformed-container-value-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes": [, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '", "Transaction State":"Prepared"}',
        encoding="utf-8",
    )
    return path


def _write_stray_container_after_delimiter_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "stray-container-after-delimiter-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":1, {, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_stray_array_after_delimiter_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "stray-array-after-delimiter-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":1, [, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_stray_container_after_malformed_key_fixture(root: Path) -> Path:
    path = root / "audit_log" / "stray-container-after-malformed-key.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"Notes":1, "Broken" {, "Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_oversized_integer_transition_fixture(root: Path) -> Path:
    path = root / "audit_log" / "oversized-integer-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    digit_limit = sys.get_int_max_str_digits()
    digit_count = max(5_000, digit_limit + 100 if digit_limit else 100_000)
    path.write_text(
        '{"Notes":'
        + ("9" * digit_count)
        + ',"Transition":"'
        + validator.TARGET_SET_TRANSITION
        + '"}',
        encoding="utf-8",
    )
    return path


def _write_bom_prepared_journal_fixture(root: Path) -> Path:
    path = _write_modern_journal_fixture(root, state="Prepared")
    path.write_text("\ufeff" + path.read_text(encoding="utf-8"), encoding="utf-8")
    return path


def _write_uppercase_extension_prepared_fixture(root: Path) -> Path:
    return _write_modern_journal_fixture(
        root,
        filename="pending.JSON",
        state="Prepared",
    )


def _write_malformed_transition_fixture(
    root: Path,
    *,
    escaped_key: bool = False,
    escaped_value: bool = False,
) -> Path:
    key = "Transi\\u0074ion" if escaped_key else "Transition"
    value = validator.TARGET_SET_TRANSITION
    if escaped_value:
        value = value.replace("reconciliation", "reconcili\\u0061tion")
    path = root / "audit_log" / "malformed-escaped-transition.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'{{"{key}":"{value}",', encoding="utf-8")
    return path


def _json_object_with_field_pair(
    payload: dict[str, object],
    field: str,
    first_value: object,
    second_value: object,
    *,
    second_key: str | None = None,
) -> str:
    if field not in payload:
        raise AssertionError(f"fixture field {field!r} not found")
    members: list[str] = []
    for key, value in payload.items():
        if key == field:
            members.append(f"{json.dumps(field)}:{json.dumps(first_value)}")
            members.append(f"{json.dumps(second_key or field)}:{json.dumps(second_value)}")
        else:
            members.append(f"{json.dumps(key)}:{json.dumps(value)}")
    return "{" + ",".join(members) + "}"


def _write_json_with_field_pair(
    path: Path,
    payload: dict[str, object],
    field: str,
    first_value: object,
    second_value: object,
    *,
    second_key: str | None = None,
    collection_field: str | None = None,
) -> Path:
    if collection_field is None:
        text = _json_object_with_field_pair(
            payload,
            field,
            first_value,
            second_value,
            second_key=second_key,
        )
    else:
        rows = payload.get(collection_field)
        if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
            raise AssertionError(f"fixture collection {collection_field!r} is invalid")
        first_row = _json_object_with_field_pair(
            rows[0],
            field,
            first_value,
            second_value,
            second_key=second_key,
        )
        collection_text = "[" + ",".join(
            [first_row, *(json.dumps(row) for row in rows[1:])]
        ) + "]"
        members = [
            f"{json.dumps(key)}:{collection_text if key == collection_field else json.dumps(value)}"
            for key, value in payload.items()
        ]
        text = "{" + ",".join(members) + "}"
    path.write_text(text + "\n", encoding="utf-8")
    return path


def _write_modern_ambiguous_json_fixture(
    root: Path,
    field: str,
    first_value: object,
    *,
    second_value: object | None = None,
    second_key: str | None = None,
    nested: bool = False,
    existing_value: object | None = None,
) -> Path:
    path = _write_modern_journal_fixture(root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    container = payload["Targets"][0] if nested else payload
    if field not in container:
        container[field] = existing_value
        atomic_write_json(path, payload)
    actual_second = container[field] if second_value is None else second_value
    return _write_json_with_field_pair(
        path,
        payload,
        field,
        first_value,
        actual_second,
        second_key=second_key,
        collection_field="Targets" if nested else None,
    )


def _write_ambiguous_registry_fixture(
    root: Path,
    field: str,
    first_value: object,
    *,
    second_key: str | None = None,
    row_field: bool = False,
) -> tuple[Path, Path]:
    audit_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    manifest_path = _write_fixture_compatibility_manifest(
        root,
        audit_path,
        PROFILE_BY_RECEIPT["receipt-1"],
    )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    container = payload["Receipts"][0] if row_field else payload
    return audit_path, _write_json_with_field_pair(
        manifest_path,
        payload,
        field,
        first_value,
        container[field],
        second_key=second_key,
        collection_field="Receipts" if row_field else None,
    )


def _write_unique_registry_fixture(root: Path) -> tuple[Path, Path]:
    audit_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    return audit_path, _write_fixture_compatibility_manifest(
        root,
        audit_path,
        PROFILE_BY_RECEIPT["receipt-1"],
    )


def _write_ambiguous_legacy_evidence_fixture(
    root: Path,
    evidence: str,
    *,
    second_key: str | None = None,
) -> Path:
    audit_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if evidence == "lock":
        evidence_path = root / "locks" / f"{audit['Lock ID']}.json"
        payload = json.loads(evidence_path.read_text(encoding="utf-8"))
        return_path = _write_json_with_field_pair(
            evidence_path,
            payload,
            "Lock State",
            "Locked",
            "Released",
            second_key=second_key,
        )
    elif evidence == "snapshot":
        evidence_path = root / str(audit["Snapshot"]) / "snapshot_manifest.json"
        snapshot = json.loads(evidence_path.read_text(encoding="utf-8"))
        return_path = _write_json_with_field_pair(
            evidence_path,
            snapshot,
            "Copied Files",
            [],
            snapshot["Copied Files"],
            second_key=second_key,
        )
    else:
        raise AssertionError(f"unknown evidence fixture {evidence!r}")
    if not return_path.exists():
        raise AssertionError(f"ambiguous evidence fixture was not written: {return_path}")
    return audit_path


def _write_non_object_legacy_evidence_fixture(root: Path, evidence: str) -> Path:
    audit_path = _write_exact_real_legacy_receipt_fixture(root, "receipt-1")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if evidence == "lock":
        evidence_path = root / "locks" / f"{audit['Lock ID']}.json"
    elif evidence == "snapshot":
        evidence_path = root / str(audit["Snapshot"]) / "snapshot_manifest.json"
    else:
        raise AssertionError(f"unknown evidence fixture {evidence!r}")
    evidence_path.write_text("[]\n", encoding="utf-8")
    return audit_path


def _run_journal_case(
    name: str,
    setup: object,
    *,
    should_pass: bool,
    admitted_profile: str | None = None,
) -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-legacy-journal-") as temp_dir:
        root = Path(temp_dir)
        setup_result = setup(root)  # type: ignore[operator]
        manifest_path = _resolve_case_manifest(root, setup_result, admitted_profile)
        failures = validator.validate_incomplete_target_set_journals(root, manifest_path)
        if should_pass and failures:
            raise AssertionError(f"{name} unexpectedly failed:\n" + "\n".join(failures))
        if not should_pass and not failures:
            raise AssertionError(f"{name} unexpectedly passed")
    print(f"Legacy journal fixture: {name}: PASS")


def _assert_journal_mutation_killed(
    name: str,
    setup: object,
    attribute: str,
    replacement: object,
    *,
    admitted_profile: str | None = None,
) -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-legacy-mutation-") as temp_dir:
        root = Path(temp_dir)
        setup_result = setup(root)  # type: ignore[operator]
        manifest_path = _resolve_case_manifest(root, setup_result, admitted_profile)
        baseline = validator.validate_incomplete_target_set_journals(root, manifest_path)
        if not baseline:
            raise AssertionError(f"mutation {name} has no failing baseline")
        original = getattr(validator, attribute)
        setattr(validator, attribute, replacement)
        try:
            mutated = validator.validate_incomplete_target_set_journals(root, manifest_path)
        finally:
            setattr(validator, attribute, original)
        if mutated:
            raise AssertionError(
                f"mutation {name} survived the focused suite:\n" + "\n".join(mutated)
            )
    print(f"Legacy journal mutation: {name}: KILLED")


def _assert_snapshot_walk_error_reported() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-walk-error-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        original_walk = validator.os.walk

        def walk_with_denied_child(*args: object, **kwargs: object):
            onerror = kwargs.get("onerror")
            if not callable(onerror):
                raise AssertionError("snapshot traversal did not supply os.walk onerror")
            denied_child = root / "snapshots" / "modern-fixture" / "denied-child"
            onerror(PermissionError(13, "Permission denied", str(denied_child)))
            yield from original_walk(*args, **kwargs)

        validator.os.walk = walk_with_denied_child
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.walk = original_walk
        if not any("snapshot traversal failed" in item for item in failures):
            raise AssertionError(
                "snapshot traversal error unexpectedly passed:\n" + "\n".join(failures)
            )
    print("Modern snapshot fixture: traversal error rejected: PASS")


def _assert_snapshot_directory_replacement_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-directory-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        snapshot_path = root / "snapshots" / "modern-fixture"
        unexpected_path = snapshot_path / "unexpected-retained-state.txt"
        unexpected_path.write_text("retained pre-write material", encoding="utf-8")
        replacement_path = root / "snapshot-replacement"
        original_path = root / "snapshot-original"
        shutil.copytree(snapshot_path, replacement_path)
        (replacement_path / unexpected_path.name).unlink()
        original_walk = validator.os.walk
        replaced = False

        def replace_before_inventory(top: object, *args: object, **kwargs: object):
            nonlocal replaced
            if not replaced and Path(top) == snapshot_path:
                snapshot_path.rename(original_path)
                replacement_path.rename(snapshot_path)
                replaced = True
            return original_walk(top, *args, **kwargs)

        validator.os.walk = replace_before_inventory
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.walk = original_walk
        if not replaced or not any(
            "snapshot directory changed during validation" in item
            for item in failures
        ):
            raise AssertionError(
                "snapshot-directory replacement race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern snapshot fixture: directory replacement race rejected: PASS")


def _assert_snapshot_child_mutation_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-child-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        snapshot_path = root / "snapshots" / "modern-fixture"
        snapshot_copy = snapshot_path / "worktrees" / "Fixture" / "worktree_state.md"
        original_walk = validator.os.walk
        mutated = False

        def mutate_before_inventory(top: object, *args: object, **kwargs: object):
            nonlocal mutated
            if not mutated and Path(top) == snapshot_path:
                snapshot_copy.write_text("mutated after initial hash\n", encoding="utf-8")
                mutated = True
            return original_walk(top, *args, **kwargs)

        validator.os.walk = mutate_before_inventory
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.walk = original_walk
        if not mutated or not any(
            "snapshot copy changed after inventory" in item for item in failures
        ):
            raise AssertionError(
                "snapshot child-mutation race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern snapshot fixture: child mutation race rejected: PASS")


def _assert_snapshot_inventory_creation_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-inventory-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        snapshot_path = root / "snapshots" / "modern-fixture"
        late_file = snapshot_path / "created-during-hashing.txt"
        original_walk = validator.os.walk
        snapshot_walks = 0

        def create_after_first_inventory(top: object, *args: object, **kwargs: object):
            nonlocal snapshot_walks
            yield from original_walk(top, *args, **kwargs)
            if Path(top) == snapshot_path:
                snapshot_walks += 1
                if snapshot_walks == 1:
                    late_file.write_text(
                        "unmanifested material created after the first inventory\n",
                        encoding="utf-8",
                    )

        validator.os.walk = create_after_first_inventory
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.walk = original_walk
        if (
            snapshot_walks < 2
            or not any(
                "snapshot inventory changed after hashing" in item
                for item in failures
            )
            or not any("unmanifested files" in item for item in failures)
        ):
            raise AssertionError(
                "snapshot inventory-creation race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern snapshot fixture: post-hash inventory creation race rejected: PASS")


def _assert_audit_inventory_creation_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-audit-inventory-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        audit_root = root / "audit_log"
        original_iterdir = Path.iterdir
        audit_enumerations = 0

        def create_before_recheck(path: Path):
            nonlocal audit_enumerations
            if path == audit_root:
                audit_enumerations += 1
                if audit_enumerations == 2:
                    atomic_write_json(
                        audit_root / "new-prepared-transaction.json",
                        {
                            "Transition": validator.TARGET_SET_TRANSITION,
                            "Transaction State": "Prepared",
                        },
                    )
            return original_iterdir(path)

        Path.iterdir = create_before_recheck
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            Path.iterdir = original_iterdir
        if audit_enumerations < 2 or not any(
            "audit inventory changed during validation" in item for item in failures
        ):
            raise AssertionError(
                "audit inventory creation race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern audit fixture: inventory creation race rejected: PASS")


def _assert_audit_final_inventory_creation_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-audit-final-inventory-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        audit_root = root / "audit_log"
        original_iterdir = Path.iterdir
        audit_enumerations = 0

        def create_after_final_hashes(path: Path):
            nonlocal audit_enumerations
            if path == audit_root:
                audit_enumerations += 1
                if audit_enumerations == 3:
                    atomic_write_json(
                        audit_root / "late-prepared-transaction.json",
                        {
                            "Transition": validator.TARGET_SET_TRANSITION,
                            "Transaction State": "Prepared",
                        },
                    )
            return original_iterdir(path)

        Path.iterdir = create_after_final_hashes
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            Path.iterdir = original_iterdir
        if audit_enumerations < 3 or not any(
            "audit inventory changed after final evidence validation" in item
            for item in failures
        ):
            raise AssertionError(
                "post-evidence audit inventory-creation race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern audit fixture: post-evidence inventory creation race rejected: PASS")


def _assert_audit_creation_during_final_lock_validation_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-audit-final-lock-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        audit_root = root / "audit_log"
        original_validate_lock = validator._validate_modern_lock_evidence
        lock_validations = 0

        def create_during_final_lock_validation(*args: object, **kwargs: object):
            nonlocal lock_validations
            issues = original_validate_lock(*args, **kwargs)
            lock_validations += 1
            if lock_validations == 2:
                atomic_write_json(
                    audit_root / "prepared-during-final-lock-validation.json",
                    {
                        "Transition": validator.TARGET_SET_TRANSITION,
                        "Transaction State": "Prepared",
                    },
                )
            return issues

        validator._validate_modern_lock_evidence = create_during_final_lock_validation
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._validate_modern_lock_evidence = original_validate_lock
        if lock_validations < 2 or not any(
            "audit inventory changed after final evidence validation" in item
            for item in failures
        ):
            raise AssertionError(
                "audit creation during final lock validation escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern audit fixture: final-lock creation race rejected: PASS")


def _assert_audit_creation_during_final_hash_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-audit-final-hash-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        audit_root = root / "audit_log"
        original_hash = validator._sha256_confined_evidence_file
        audit_hashes = 0

        def create_during_final_hash(base: Path, parts: tuple[str, ...]) -> str:
            nonlocal audit_hashes
            digest = original_hash(base, parts)
            if base == root and parts and parts[0] == "audit_log":
                audit_hashes += 1
                if audit_hashes == 2:
                    atomic_write_json(
                        audit_root / "prepared-during-final-hash.json",
                        {
                            "Transition": validator.TARGET_SET_TRANSITION,
                            "Transaction State": "Prepared",
                        },
                    )
            return digest

        validator._sha256_confined_evidence_file = create_during_final_hash
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._sha256_confined_evidence_file = original_hash
        if audit_hashes < 2 or not any(
            "audit inventory changed after final hashing" in item
            for item in failures
        ):
            raise AssertionError(
                "audit creation during final hashing escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern audit fixture: final-hash creation race rejected: PASS")


def _assert_audit_rediscovery_failure_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-audit-rediscovery-failure-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        audit_root = root / "audit_log"
        original_iterdir = Path.iterdir
        audit_enumerations = 0

        def fail_rediscovery(path: Path):
            nonlocal audit_enumerations
            if path == audit_root:
                audit_enumerations += 1
                if audit_enumerations == 2:
                    raise OSError("fixture audit rediscovery failure")
            return original_iterdir(path)

        Path.iterdir = fail_rediscovery
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            Path.iterdir = original_iterdir
        if audit_enumerations < 2 or not any(
            "audit inventory changed during validation" in item for item in failures
        ):
            raise AssertionError(
                "audit rediscovery failure escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern audit fixture: rediscovery failure rejected: PASS")


def _assert_live_target_final_revalidation_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-live-target-final-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        target = root / "worktrees" / "Fixture" / "worktree_state.md"
        target_parts = ("worktrees", "Fixture", "worktree_state.md")
        original_hash = validator._sha256_confined_evidence_file
        target_hashes = 0

        def mutate_after_first_hash(base: Path, parts: tuple[str, ...]):
            nonlocal target_hashes
            digest = original_hash(base, parts)
            if base == root and parts == target_parts:
                target_hashes += 1
                if target_hashes == 1:
                    target.write_bytes(b"late unrelated live target bytes\n")
            return digest

        validator._sha256_confined_evidence_file = mutate_after_first_hash
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._sha256_confined_evidence_file = original_hash
        if target_hashes < 2 or not any(
            "live target changed during validation" in item
            and "does not match After SHA256" in item
            for item in failures
        ):
            raise AssertionError(
                "final live-target mutation escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern live-target fixture: final revalidation race rejected: PASS")


def _assert_snapshot_final_revalidation_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-final-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        snapshot_root = root / "snapshots" / "modern-fixture"
        original_lock_validation = validator._validate_modern_lock_evidence
        lock_validations = 0

        def mutate_during_later_validation(*args, **kwargs):
            nonlocal lock_validations
            issues = original_lock_validation(*args, **kwargs)
            lock_validations += 1
            if lock_validations == 1:
                (snapshot_root / "late-unmanifested.txt").write_bytes(
                    b"late snapshot bytes\n"
                )
            return issues

        validator._validate_modern_lock_evidence = mutate_during_later_validation
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._validate_modern_lock_evidence = original_lock_validation
        if lock_validations < 2 or not any(
            "snapshot changed during validation" in item
            and "unmanifested files" in item
            for item in failures
        ):
            raise AssertionError(
                "post-snapshot lock-phase mutation escaped final validation:\n"
                + "\n".join(failures)
            )
    print("Modern snapshot fixture: final revalidation race rejected: PASS")


def _assert_lock_final_revalidation_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-lock-final-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        lock_path = root / "locks" / "branch-modern-fixture.json"
        original_target_validation = validator._validate_modern_committed_target_evidence
        target_validations = 0

        def reacquire_during_later_validation(*args, **kwargs):
            nonlocal target_validations
            issues = original_target_validation(*args, **kwargs)
            target_validations += 1
            if target_validations == 1:
                lock = json.loads(lock_path.read_text(encoding="utf-8"))
                lock["Lock State"] = "Locked"
                lock["Workload State"] = "Active"
                lock.pop("Released At", None)
                atomic_write_json(lock_path, lock)
            return issues

        validator._validate_modern_committed_target_evidence = (
            reacquire_during_later_validation
        )
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._validate_modern_committed_target_evidence = (
                original_target_validation
            )
        if target_validations < 2 or not any(
            "lock changed during validation" in item
            and "Lock State='Locked'" in item
            for item in failures
        ):
            raise AssertionError(
                "post-lock live-target-phase reacquisition escaped final validation:\n"
                + "\n".join(failures)
            )
    print("Modern lock fixture: final revalidation race rejected: PASS")


def _assert_audit_file_replacement_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-audit-file-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        audit_path = root / "audit_log" / "same.json"
        atomic_write_json(audit_path, {"Notes": "unrelated initial evidence"})
        original_read = validator._read_confined_evidence_file
        replaced = False

        def replace_after_read(base: Path, parts: tuple[str, ...]):
            nonlocal replaced
            result = original_read(base, parts)
            if not replaced and parts == ("audit_log", "same.json"):
                atomic_write_json(
                    audit_path,
                    {
                        "Transition": validator.TARGET_SET_TRANSITION,
                        "Transaction State": "Prepared",
                    },
                )
                replaced = True
            return result

        validator._read_confined_evidence_file = replace_after_read
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._read_confined_evidence_file = original_read
        if not replaced or not any(
            "audit file changed during validation" in item for item in failures
        ):
            raise AssertionError(
                "same-name audit replacement race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern audit fixture: same-name replacement race rejected: PASS")


def _assert_snapshot_manifest_replacement_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-manifest-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        snapshot_path = root / "snapshots" / "modern-fixture"
        manifest_path = snapshot_path / "snapshot_manifest.json"
        original_walk = validator.os.walk
        replaced = False

        def replace_before_inventory(top: object, *args: object, **kwargs: object):
            nonlocal replaced
            if not replaced and Path(top) == snapshot_path:
                atomic_write_json(manifest_path, {"replaced": True})
                replaced = True
            return original_walk(top, *args, **kwargs)

        validator.os.walk = replace_before_inventory
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.walk = original_walk
        if not replaced or not any(
            "snapshot manifest changed after inventory" in item for item in failures
        ):
            raise AssertionError(
                "snapshot-manifest replacement race escaped validation:\n"
                + "\n".join(failures)
            )
    print("Modern snapshot fixture: manifest replacement race rejected: PASS")


def _assert_lock_replacement_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-lock-replacement-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        lock_path = root / "locks" / "branch-modern-fixture.json"
        original_load = validator._strict_json_load_confined_with_digest
        replaced = False

        def replace_after_load(base: Path, parts: tuple[str, ...]):
            nonlocal replaced
            result = original_load(base, parts)
            if not replaced and parts == ("locks", "branch-modern-fixture.json"):
                payload = json.loads(lock_path.read_text(encoding="utf-8"))
                payload["Lock State"] = "Locked"
                atomic_write_json(lock_path, payload)
                replaced = True
            return result

        validator._strict_json_load_confined_with_digest = replace_after_load
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._strict_json_load_confined_with_digest = original_load
        if not replaced or not any(
            "lock evidence changed during validation" in item for item in failures
        ):
            raise AssertionError(
                "lock replacement race escaped validation:\n" + "\n".join(failures)
            )
    print("Modern lock fixture: replacement race rejected: PASS")


def _assert_oversized_evidence_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-oversized-evidence-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        original_limit = validator.MAX_EXTERNAL_STATE_EVIDENCE_BYTES
        validator.MAX_EXTERNAL_STATE_EVIDENCE_BYTES = 128
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
            hash_path = root / "hash-only-evidence.bin"
            hash_path.write_bytes(b"x" * 256)
            try:
                validator._sha256_confined_evidence_file(
                    root,
                    (hash_path.name,),
                )
            except OSError as exc:
                bounded_hash_rejected = "bounded hash limit" in str(exc)
            else:
                bounded_hash_rejected = False
        finally:
            validator.MAX_EXTERNAL_STATE_EVIDENCE_BYTES = original_limit
        if (
            not any("bounded read limit" in item for item in failures)
            or not bounded_hash_rejected
        ):
            raise AssertionError(
                "oversized read or hash evidence unexpectedly passed:\n"
                + "\n".join(failures)
            )
    print("Modern journal fixture: oversized read/hash evidence rejected: PASS")


def _assert_missing_audit_root_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-missing-audit-root-") as temp_dir:
        root = Path(temp_dir)
        failures = validator.validate_incomplete_target_set_journals(root)
        if not any("audit root is missing" in item for item in failures):
            raise AssertionError(
                "missing audit root unexpectedly passed:\n" + "\n".join(failures)
            )
    print("Modern audit fixture: missing audit root rejected: PASS")


def _assert_evidence_read_memory_error_reported() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-evidence-memory-error-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        original_read = validator.os.read

        def fail_evidence_read(_descriptor: int, _size: int) -> bytes:
            raise MemoryError("forced evidence read exhaustion")

        validator.os.read = fail_evidence_read
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.read = original_read
        if not any("safe resource limits" in item for item in failures):
            raise AssertionError(
                "evidence-read MemoryError escaped fail-closed validation:\n"
                + "\n".join(failures)
            )
    print("Modern journal fixture: evidence-read MemoryError reported: PASS")


def _assert_journal_false_positive_mutation_killed(
    name: str,
    setup: object,
    attribute: str,
    replacement: object,
) -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-legacy-selector-mutation-") as temp_dir:
        root = Path(temp_dir)
        setup_result = setup(root)  # type: ignore[operator]
        manifest_path = _resolve_case_manifest(root, setup_result, None)
        baseline = validator.validate_incomplete_target_set_journals(root, manifest_path)
        if baseline:
            raise AssertionError(f"mutation {name} has no passing baseline:\n" + "\n".join(baseline))
        original = getattr(validator, attribute)
        setattr(validator, attribute, replacement)
        try:
            mutated = validator.validate_incomplete_target_set_journals(root, manifest_path)
        finally:
            setattr(validator, attribute, original)
        if not mutated:
            raise AssertionError(f"mutation {name} survived the focused suite")
    print(f"Legacy journal mutation: {name}: KILLED")


def _assert_modern_audit_reparse_rejected(name: str, component: str) -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-modern-audit-reparse-") as temp_dir:
        root = Path(temp_dir)
        audit_path = _write_modern_journal_fixture(root)
        reparse_path = root / "audit_log" if component == "directory" else audit_path
        original = validator._has_reparse_point
        validator._has_reparse_point = lambda path: path == reparse_path or original(path)
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._has_reparse_point = original
        if not any("not a confined regular" in failure for failure in failures):
            raise AssertionError(
                f"{name} unexpectedly passed:\n" + "\n".join(failures)
            )
    print(f"Modern audit reparse fixture: {name}: PASS")


def _assert_broken_audit_reparse_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-broken-audit-reparse-") as temp_dir:
        root = Path(temp_dir)
        audit_root = root / "audit_log"
        original = validator._has_reparse_point
        validator._has_reparse_point = lambda path: path == audit_root or original(path)
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._has_reparse_point = original
        if not any("not a confined regular" in failure for failure in failures):
            raise AssertionError(
                "broken audit-root reparse fixture unexpectedly passed:\n"
                + "\n".join(failures)
            )
    print("Modern audit reparse fixture: broken audit_log alias: PASS")


def _assert_snapshot_hash_read_failure_reported() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-hash-read-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        original = validator._sha256_confined_evidence_file
        validator._sha256_confined_evidence_file = lambda *_args: (_ for _ in ()).throw(
            OSError("simulated snapshot read failure")
        )
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator._sha256_confined_evidence_file = original
        if not any("snapshot copy is unreadable" in failure for failure in failures):
            raise AssertionError(
                "snapshot hash read failure escaped validation:\n" + "\n".join(failures)
            )
    print("Modern snapshot fixture: hash read failure reported: PASS")


def _assert_snapshot_hash_replacement_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-snapshot-hash-race-") as temp_dir:
        root = Path(temp_dir)
        _write_modern_journal_fixture(root)
        snapshot_copy = (
            root
            / "snapshots"
            / "modern-fixture"
            / "worktrees"
            / "Fixture"
            / "worktree_state.md"
        )
        descriptor, outside_name = tempfile.mkstemp(
            prefix="ndai-outside-snapshot-",
            suffix=".bin",
            dir=root.parent,
        )
        os.close(descriptor)
        outside_path = Path(outside_name)
        outside_path.write_bytes(b"modern fixture before\n")
        original_open = validator.os.open
        swapped = False

        def replace_before_open(
            path: object,
            flags: int,
            *args: object,
            **kwargs: object,
        ) -> int:
            nonlocal swapped
            if not swapped and Path(path) == snapshot_copy:
                snapshot_copy.unlink()
                os.link(outside_path, snapshot_copy)
                swapped = True
            return original_open(path, flags, *args, **kwargs)

        validator.os.open = replace_before_open
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.open = original_open
            outside_path.unlink(missing_ok=True)
        if not any("changed between confinement check and open" in item for item in failures):
            raise AssertionError(
                "snapshot hash replacement race escaped validation:\n" + "\n".join(failures)
            )
    print("Modern snapshot fixture: confinement/open replacement race rejected: PASS")


def _assert_journal_read_replacement_race_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-journal-read-race-") as temp_dir:
        root = Path(temp_dir)
        audit_path = _write_modern_journal_fixture(root)
        descriptor, outside_name = tempfile.mkstemp(
            prefix="ndai-outside-journal-",
            suffix=".json",
            dir=root.parent,
        )
        os.close(descriptor)
        outside_path = Path(outside_name)
        outside_path.write_bytes(audit_path.read_bytes())
        original_open = validator.os.open
        swapped = False

        def replace_before_open(
            path: object,
            flags: int,
            *args: object,
            **kwargs: object,
        ) -> int:
            nonlocal swapped
            if not swapped and Path(path) == audit_path:
                audit_path.unlink()
                os.link(outside_path, audit_path)
                swapped = True
            return original_open(path, flags, *args, **kwargs)

        validator.os.open = replace_before_open
        try:
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            validator.os.open = original_open
            outside_path.unlink(missing_ok=True)
        if not any("changed between confinement check and open" in item for item in failures):
            raise AssertionError(
                "journal read replacement race escaped validation:\n" + "\n".join(failures)
            )
    print("Modern journal fixture: confinement/open replacement race rejected: PASS")


def _assert_posix_case_sensitive_evidence_paths() -> None:
    original_host_path_key = validator._host_path_key
    posix_path_key = lambda value: value.replace("\\", "/")
    try:
        validator._host_path_key = posix_path_key
        with tempfile.TemporaryDirectory(prefix="ndai-posix-modern-case-") as temp_dir:
            root = Path(temp_dir)
            audit_path = _write_modern_journal_fixture(root)
            payload = json.loads(audit_path.read_text(encoding="utf-8"))
            payload["Targets"][0]["Target"] = payload["Targets"][0]["Target"].swapcase()
            atomic_write_json(audit_path, payload)
            failures = validator.validate_incomplete_target_set_journals(root)
            if not failures:
                raise AssertionError("POSIX modern case-distinct target unexpectedly passed")
        with tempfile.TemporaryDirectory(prefix="ndai-posix-snapshot-namespace-") as temp_dir:
            root = Path(temp_dir)
            audit_path = _write_modern_journal_fixture(root)
            snapshot_root = root / "snapshots"
            intermediate = root / "snapshot-case-intermediate"
            uppercase_root = root / "SNAPSHOTS"
            snapshot_root.rename(intermediate)
            intermediate.rename(uppercase_root)
            payload = json.loads(audit_path.read_text(encoding="utf-8"))
            payload["Snapshot"] = payload["Snapshot"].replace(
                "snapshots/", "SNAPSHOTS/", 1
            )
            atomic_write_json(audit_path, payload)
            lock_path = root / "locks" / "branch-modern-fixture.json"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            lock["Intended Write Set"] = lock["Intended Write Set"].replace(
                "snapshots/", "SNAPSHOTS/", 1
            )
            atomic_write_json(lock_path, lock)
            failures = validator.validate_incomplete_target_set_journals(root)
            if not any(
                "not a safe isolated snapshots/<snapshot-id> path" in item
                for item in failures
            ):
                raise AssertionError(
                    "POSIX case-distinct snapshots namespace unexpectedly passed:\n"
                    + "\n".join(failures)
                )
        with tempfile.TemporaryDirectory(prefix="ndai-posix-legacy-case-") as temp_dir:
            root = Path(temp_dir)
            _, manifest_path = _write_case_renamed_admitted_receipt_fixture(root)
            failures = validator.validate_incomplete_target_set_journals(
                root,
                manifest_path,
            )
            if not any("not an admitted immutable receipt path" in item for item in failures):
                raise AssertionError(
                    "POSIX case-renamed immutable receipt unexpectedly passed:\n"
                    + "\n".join(failures)
                )
    finally:
        validator._host_path_key = original_host_path_key
    print("Host path semantics fixture: POSIX case-distinct evidence rejected: PASS")


def _assert_relative_snapshot_manifest_root_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-relative-snapshot-root-") as temp_dir:
        root = Path(temp_dir)
        audit_path = _write_modern_snapshot_root_fixture(root, ".")
        original_cwd = Path.cwd()
        try:
            os.chdir(root)
            failures = validator.validate_incomplete_target_set_journals(root)
        finally:
            os.chdir(original_cwd)
        if not any("Root does not match" in item for item in failures):
            raise AssertionError(
                "relative snapshot manifest Root unexpectedly passed from root CWD:\n"
                + "\n".join(failures)
            )
        if not audit_path.is_file():
            raise AssertionError("relative-root fixture audit disappeared")
    print("Modern snapshot fixture: relative manifest Root rejected: PASS")


def _assert_nonstandard_json_constants_rejected() -> None:
    for constant in ("NaN", "Infinity", "-Infinity"):
        try:
            validator._strict_json_loads(f'{{"value":{constant}}}')
        except validator.StrictJSONError:
            continue
        raise AssertionError(f"strict JSON unexpectedly accepted {constant}")
    print("Strict JSON constants: NaN / Infinity / -Infinity: REJECTED")


def _run_legacy_journal_compatibility_fixtures() -> None:
    clock_reference = datetime(2026, 7, 30, tzinfo=timezone.utc)
    within_skew = validator._transaction_timestamp_is_not_future(
        (clock_reference + validator.MAX_TRANSACTION_CLOCK_SKEW).isoformat(),
        now=clock_reference,
    )
    beyond_skew = validator._transaction_timestamp_is_not_future(
        (
            clock_reference
            + validator.MAX_TRANSACTION_CLOCK_SKEW
            + timedelta(microseconds=1)
        ).isoformat(),
        now=clock_reference,
    )
    if not within_skew or beyond_skew:
        raise AssertionError("bounded UTC clock-skew boundary is not enforced exactly")
    print("Modern journal fixture: bounded UTC clock-skew boundary: PASS")

    _assert_nonstandard_json_constants_rejected()
    complete = [
        "External State Item Status=Complete",
        "Current Validation State=PASS",
    ]
    positive_cases = [
        (
            "exact immutable legacy receipt 1 completion profile",
            lambda root: _write_exact_real_legacy_receipt_fixture(root, "receipt-1"),
        ),
        (
            "exact immutable legacy receipt 2 completion profile",
            lambda root: _write_exact_real_legacy_receipt_fixture(root, "receipt-2"),
        ),
        (
            "exact immutable legacy receipt 3 completion profile",
            lambda root: _write_exact_real_legacy_receipt_fixture(root, "receipt-3"),
        ),
        ("modern Committed journal", lambda root: _write_modern_journal_fixture(root)),
        (
            "sequential modern Committed journal chain",
            lambda root: _write_modern_journal_chain_fixture(root),
        ),
        ("strict compatibility registry with unique keys", _write_unique_registry_fixture),
        (
            "unrelated historical audit",
            lambda root: atomic_write_json(
                root / "audit_log" / "unrelated.json",
                {"External State Schema": "external-state-v1", "Transition": "Other audit"},
            ),
        ),
        *[
            (
                f"unrelated audit with non-string Transition value {label}",
                lambda root, value=value, label=label: atomic_write_json(
                    root / "audit_log" / f"unrelated-non-string-{label}.json",
                    {"External State Schema": "external-state-v1", "Transition": value},
                ),
            )
            for label, value in (
                ("integer", 1),
                ("null", None),
                ("boolean", True),
                ("array", [validator.TARGET_SET_TRANSITION]),
                ("object", {"Value": validator.TARGET_SET_TRANSITION}),
            )
        ],
        (
            "unrelated audit mentions target-set phrase only in Notes",
            lambda root: atomic_write_json(
                root / "audit_log" / "notes-only.json",
                {
                    "External State Schema": "external-state-v1",
                    "Transition": "Other audit",
                    "Notes": validator.TARGET_SET_TRANSITION,
                },
            ),
        ),
        (
            "malformed unrelated audit mentions target-set phrase only in Notes",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "malformed-notes-only.json").write_text(
                    '{"Transition":"Other audit","Notes":"'
                    + validator.TARGET_SET_TRANSITION
                    + '",',
                    encoding="utf-8",
                ),
            ),
        ),
        (
            "malformed Notes contain an escaped Transition fragment",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "malformed-escaped-notes.json").write_text(
                    '{"Transition":"Other audit","Notes":"\\"Transition\\":\\"'
                    + validator.TARGET_SET_TRANSITION
                    + '\\"",',
                    encoding="utf-8",
                ),
            ),
        ),
        (
            "unrelated UTF-16 non-JSON audit text",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "historical.log").write_text(
                    "Historical audit note only.",
                    encoding="utf-16",
                ),
            ),
        ),
        (
            "unrelated BOM-less UTF-16LE non-JSON audit text",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "historical-bomless.txt").write_text(
                    "Historical audit note only.",
                    encoding="utf-16-le",
                ),
            ),
        ),
        (
            "unrelated BOM-less UTF-16BE non-JSON audit text",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "historical-bomless-be.txt").write_text(
                    "Historical audit note only.",
                    encoding="utf-16-be",
                ),
            ),
        ),
        (
            "unrelated JSON array audit",
            lambda root: atomic_write_json(
                root / "audit_log" / "unrelated-array.json",
                [{"Transition": "Other audit", "State": "Complete"}],
            ),
        ),
        (
            "unrelated nested JSON object audit",
            lambda root: atomic_write_json(
                root / "audit_log" / "unrelated-envelope.json",
                {"Envelope": {"Transition": "Other audit", "State": "Complete"}},
            ),
        ),
        (
            "unrelated non-JSON audit names target-set phrase only in Notes",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "historical.txt").write_text(
                    "Notes: Bounded coherent target-set reconciliation\n",
                    encoding="utf-8",
                ),
            ),
        ),
        (
            "malformed unrelated audit has nested target-set Transition",
            _write_malformed_nested_transition_fixture,
        ),
        (
            "deeply nested unrelated audit is safely ignored",
            lambda root: _write_deeply_nested_json_fixture(root, target_set=False),
        ),
        (
            "modern journal deeply nested unrelated metadata is safely scanned",
            _write_modern_deep_unrelated_metadata_fixture,
        ),
    ]
    for name, setup in positive_cases:
        receipt = next(
            (
                receipt_name
                for receipt_name in PROFILE_BY_RECEIPT
                if f"receipt {receipt_name[-1]}" in name
            ),
            None,
        )
        _run_journal_case(
            name,
            setup,
            should_pass=True,
            admitted_profile=PROFILE_BY_RECEIPT.get(receipt or ""),
        )

    negative_cases = [
        (
            "new state-less legacy-shaped receipt with generic Complete/PASS",
            lambda root: _write_legacy_completion_matrix_fixture(root, [complete] * 3),
        ),
        (
            "generic Complete/PASS receipt with historical-looking filename",
            lambda root: _write_legacy_journal_fixture(
                root,
                filename="legacy-completed-20200101.json",
                completion_assignments=complete,
            ),
        ),
        (
            "generic Complete/PASS receipt with modern-looking filename",
            lambda root: _write_legacy_journal_fixture(
                root,
                filename="current-journal.json",
                completion_assignments=complete,
            ),
        ),
        (
            "admitted receipt copied or renamed to another audit path",
            _write_renamed_admitted_receipt_fixture,
        ),
        (
            "admitted receipt path with altered bytes",
            _write_tampered_admitted_receipt_fixture,
        ),
        (
            "modern journal missing Transaction State",
            lambda root: _write_modern_journal_fixture(root, include_state=False),
        ),
        (
            "modern journal blank Transaction State",
            lambda root: _write_modern_journal_fixture(root, state=""),
        ),
        (
            "modern journal unknown Transaction State",
            lambda root: _write_modern_journal_fixture(root, state="Complete"),
        ),
        (
            "modern Prepared journal",
            lambda root: _write_modern_journal_fixture(root, state="Prepared"),
        ),
        (
            "modern journal with whitespace-padded Transaction State",
            lambda root: _write_modern_journal_fixture(root, state="Committed "),
        ),
        (
            "modern journal with noncanonical transition key casing",
            _write_modern_noncanonical_transition_fixture,
        ),
        (
            "modern journal with noncanonical transition value casing",
            lambda root: _write_modern_noncanonical_transition_fixture(
                root,
                key="Transition",
                value=validator.TARGET_SET_TRANSITION.upper(),
            ),
        ),
        (
            "Prepared target-set journal below a nested audit directory",
            _write_modern_nested_audit_directory_fixture,
        ),
        (
            "target-set transaction stored in a non-JSON audit entry",
            _write_non_json_target_set_transaction_fixture,
        ),
        (
            "target-set transaction stored in a UTF-16 non-JSON audit entry",
            _write_utf16_non_json_target_set_transaction_fixture,
        ),
        (
            "plain-text target-set transaction stored in a non-JSON audit entry",
            _write_plain_text_target_set_transaction_fixture,
        ),
        (
            "plain-text target-set transaction stored in a UTF-16 audit entry",
            lambda root: _write_plain_text_target_set_transaction_fixture(
                root,
                encoding="utf-16",
            ),
        ),
        (
            "plain-text target-set transaction stored in BOM-less UTF-16LE",
            lambda root: _write_plain_text_target_set_transaction_fixture(
                root,
                encoding="utf-16-le",
            ),
        ),
        (
            "plain-text target-set transaction stored in BOM-less UTF-16BE",
            lambda root: _write_plain_text_target_set_transaction_fixture(
                root,
                encoding="utf-16-be",
            ),
        ),
        (
            "target-set transaction stored below a non-object JSON root",
            _write_non_object_target_set_transaction_fixture,
        ),
        (
            "target-set transaction wrapped below an object JSON root",
            _write_wrapped_target_set_transaction_fixture,
        ),
        *[
            (
                f"modern journal with whitespace-variant Transition {location}",
                lambda root, key=key, value=value: _write_modern_noncanonical_transition_fixture(
                    root,
                    key=key,
                    value=value,
                ),
            )
            for location, key, value in (
                ("key leading", " Transition", validator.TARGET_SET_TRANSITION),
                ("key trailing", "Transition ", validator.TARGET_SET_TRANSITION),
                ("value leading", "Transition", " " + validator.TARGET_SET_TRANSITION),
                ("value trailing", "Transition", validator.TARGET_SET_TRANSITION + " "),
            )
        ],
        (
            "modern journal invalid schema",
            lambda root: _write_modern_journal_fixture(root, schema="external-state-v0"),
        ),
        (
            "modern journal with case-variant recoverable Before Text",
            _write_modern_recovery_alias_fixture,
        ),
        *[
            (
                f"modern journal with recoverable Before Text at {location}",
                lambda root, location=location: _write_modern_recovery_payload_fixture(
                    root,
                    location,
                ),
            )
            for location in ("top-level", "nested")
        ],
        *[
            (
                f"modern journal with nested recovery payload alias {key}",
                lambda root, key=key: _write_modern_recovery_payload_alias_fixture(
                    root,
                    key,
                ),
            )
            for key in (
                "Recovery",
                "Recovery Payload",
                "BeforeText",
                "Before Content",
                "BeforeContent",
                "Before Bytes",
                "BeforeBytes",
                "RecoveryPayload",
                "Rollback Data",
                "RollbackData",
                "Pre-Write Content",
                "PreWriteContent",
                "Original Target Text",
                "OriginalTargetText",
                "Backup Content",
                "BackupContent",
                "Backup Data",
                "Undo Payload",
                "Previous Target Text",
                "Prior Content Copy",
                "Restore Data",
                "Revert Content",
                "Saved State",
                "Archived Payload",
                "Old Value",
                "Original Content",
            )
        ],
        *[
            (
                f"modern journal missing audit metadata {field}",
                lambda root, field=field: _write_modern_missing_audit_metadata_fixture(
                    root,
                    field,
                ),
            )
            for field in ("Last Updated", "Last Updated By")
        ],
        (
            "modern journal with future transaction timestamp",
            _write_modern_future_transaction_fixture,
        ),
        *[
            (
                f"modern Committed journal chain {variant}",
                lambda root, variant=variant: _write_modern_journal_chain_fixture(
                    root,
                    variant,
                ),
            )
            for variant in (
                "discontinuous",
                "ambiguous-timestamp",
                "forked",
                "reversed-chronology",
                "two-step-cycle",
                "longer-cycle",
                "latest-live-mismatch",
            )
        ],
        (
            "modern journal with unchanged target hash",
            _write_modern_equal_hash_fixture,
        ),
        (
            "modern journal with non-string SHA256 that stringifies as hexadecimal",
            _write_modern_non_string_hash_fixture,
        ),
        (
            "modern Committed journal with active lock evidence",
            lambda root: _write_modern_journal_fixture(root, lock_state="Locked"),
        ),
        (
            "modern Committed journal with malformed release timestamp",
            lambda root: _write_modern_released_at_fixture(root, "No release occurred"),
        ),
        (
            "modern Committed journal lock released before the transaction",
            lambda root: _write_modern_released_at_fixture(
                root,
                "2026-07-27T23:59:59Z",
            ),
        ),
        (
            "modern Committed journal lock released in the future",
            _write_modern_future_release_fixture,
        ),
        *[
            (
                f"modern Committed journal with {state} live target",
                lambda root, state=state: _write_modern_live_target_mismatch_fixture(
                    root,
                    state,
                ),
            )
            for state in ("missing", "before", "unrelated")
        ],
        (
            "modern Committed journal with missing snapshot manifest",
            _write_modern_missing_snapshot_fixture,
        ),
        (
            "modern Committed journal with missing snapshot Root",
            lambda root: _write_modern_snapshot_root_fixture(root, None),
        ),
        (
            "modern Committed journal with missing snapshot Last Updated",
            lambda root: _write_modern_snapshot_timestamp_fixture(root, None),
        ),
        (
            "modern Committed journal with malformed snapshot Last Updated",
            lambda root: _write_modern_snapshot_timestamp_fixture(
                root,
                "not-a-canonical-timestamp",
            ),
        ),
        (
            "modern Committed journal snapshot postdates the transaction",
            lambda root: _write_modern_snapshot_timestamp_fixture(
                root,
                "2026-07-29T00:00:00Z",
            ),
        ),
        (
            "modern Committed journal with foreign snapshot Root",
            lambda root: _write_modern_snapshot_root_fixture(
                root,
                str(root.parent / "other-external-state-root"),
            ),
        ),
        (
            "modern Committed journal with case-ambiguous snapshot Root",
            _write_modern_case_ambiguous_snapshot_root_fixture,
        ),
        (
            "modern Committed journal uses the shared snapshots namespace root",
            _write_modern_snapshot_namespace_root_fixture,
        ),
        (
            "modern Committed journal with tampered snapshot copy",
            _write_modern_tampered_snapshot_fixture,
        ),
        (
            "modern Committed journal snapshot contains an unexpected file",
            _write_modern_snapshot_extra_file_fixture,
        ),
        (
            "modern Committed journal snapshot contains an unmanifested file",
            _write_modern_snapshot_unmanifested_file_fixture,
        ),
        *[
            (
                f"modern lock write set omits {omitted}",
                lambda root, omitted=omitted: _write_modern_lock_write_set_omission_fixture(
                    root,
                    omitted,
                ),
            )
            for omitted in ("audit", "snapshot", "target")
        ],
        (
            "modern lock write set includes unexpected target",
            _write_modern_lock_write_set_extra_fixture,
        ),
        *[
            (
                f"modern lock has non-string {field}",
                lambda root, field=field: _write_modern_non_string_lock_identity_fixture(
                    root,
                    field,
                ),
            )
            for field in ("Lock ID", "Workload ID")
        ],
        *[
            (
                f"modern lock has whitespace-padded {field}",
                lambda root, field=field: _write_modern_padded_lock_field_fixture(
                    root,
                    field,
                ),
            )
            for field in (
                "External State Schema",
                "Lock State",
                "Workload State",
                "Retain Between Workloads",
                "Workload ID",
            )
        ],
        *[
            (
                f"modern evidence has whitespace-padded {location}",
                lambda root, location=location: _write_modern_whitespace_evidence_path_fixture(
                    root,
                    location,
                ),
            )
            for location in (
                "journal target",
                "snapshot root",
                "snapshot manifest path",
                "lock write set",
            )
        ],
        *[
            (
                f"modern evidence contains non-standard numeric constant in {location}",
                lambda root, location=location: _write_modern_nonstandard_constant_fixture(
                    root,
                    location,
                ),
            )
            for location in ("journal", "lock", "snapshot")
        ],
        *[
            (
                f"modern journal with non-string Target {kind}",
                lambda root, value=value: _write_modern_target_value_fixture(root, value),
            )
            for kind, value in (
                ("boolean", True),
                ("integer", 7),
                ("list", ["worktrees/Fixture/worktree_state.md"]),
            )
        ],
        *[
            (
                f"modern journal with impossible Target {kind}",
                lambda root, value=value: _write_modern_target_value_fixture(root, value),
            )
            for kind, value in (
                ("NUL", "worktrees/Bad\x00Name/state.md"),
                ("control", "worktrees/Bad\x1fName/state.md"),
                ("wildcard", "worktrees/Bad*/state.md"),
                ("trailing-dot", "worktrees/Bad./state.md"),
                ("trailing-space", "worktrees/Bad /state.md"),
                ("reserved-name", "worktrees/NUL/state.md"),
                ("surrogate", "worktrees/Bad\ud800Name/state.md"),
            )
        ],
        (
            "deeply nested target-set audit reports a validation failure",
            lambda root: _write_deeply_nested_json_fixture(root, target_set=True),
        ),
        (
            "matching malformed JSON",
            lambda root: (
                (root / "audit_log").mkdir(parents=True, exist_ok=True),
                (root / "audit_log" / "malformed.json").write_text(
                    '{"Transition":"Bounded coherent target-set reconciliation",',
                    encoding="utf-8",
                ),
            ),
        ),
        (
            "matching malformed JSON with escaped Transition key",
            lambda root: _write_malformed_transition_fixture(root, escaped_key=True),
        ),
        (
            "matching malformed JSON with escaped Transition value",
            lambda root: _write_malformed_transition_fixture(root, escaped_value=True),
        ),
        (
            "matching malformed JSON after mismatched delimiter",
            _write_mismatched_delimiter_transition_fixture,
        ),
        (
            "matching malformed JSON with unreadable Transition value",
            _write_malformed_transition_value_fixture,
        ),
        (
            "matching malformed JSON after invalid string escape and brace",
            _write_invalid_escape_brace_transition_fixture,
        ),
        (
            "matching malformed JSON with illegal container after decoded value",
            _write_illegal_container_after_value_transition_fixture,
        ),
        (
            "matching malformed JSON with unterminated container value",
            _write_malformed_container_value_transition_fixture,
        ),
        (
            "matching malformed JSON with stray container after member delimiter",
            _write_stray_container_after_delimiter_transition_fixture,
        ),
        (
            "matching malformed JSON with stray array after member delimiter",
            _write_stray_array_after_delimiter_transition_fixture,
        ),
        (
            "matching malformed JSON with stray container after malformed key",
            _write_stray_container_after_malformed_key_fixture,
        ),
        (
            "matching malformed JSON with nested malformed value",
            _write_nested_malformed_value_transition_fixture,
        ),
        (
            "matching malformed JSON with missing comma before Transition",
            _write_missing_comma_before_transition_fixture,
        ),
        (
            "matching malformed JSON with unquoted Transition key",
            _write_bare_transition_key_fixture,
        ),
        (
            "matching malformed JSON after mismatched nested comma",
            _write_mismatched_nested_comma_transition_fixture,
        ),
        (
            "matching malformed JSON after mismatched nested string",
            _write_mismatched_nested_string_transition_fixture,
        ),
        (
            "matching malformed JSON after mismatched nested member",
            _write_mismatched_nested_member_transition_fixture,
        ),
        (
            "matching malformed JSON after unmatched inner closer",
            _write_unmatched_inner_closer_transition_fixture,
        ),
        (
            "matching malformed JSON after unmatched inner closer in array",
            _write_unmatched_inner_closer_array_transition_fixture,
        ),
        (
            "matching malformed JSON after mismatched closers reach root frame",
            _write_root_frame_mismatched_closer_transition_fixture,
        ),
        (
            "matching malformed JSON after leading junk",
            _write_leading_junk_transition_fixture,
        ),
        (
            "matching malformed JSON after quoted junk with a brace",
            _write_quoted_junk_transition_fixture,
        ),
        (
            "matching malformed JSON with oversized integer",
            _write_oversized_integer_transition_fixture,
        ),
        (
            "BOM-prefixed modern Prepared journal",
            _write_bom_prepared_journal_fixture,
        ),
        (
            "uppercase-extension modern Prepared journal",
            _write_uppercase_extension_prepared_fixture,
        ),
        (
            "duplicate Transition exact then unrelated",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Transition",
                validator.TARGET_SET_TRANSITION,
                second_value="Other audit",
            ),
        ),
        (
            "duplicate Transition unrelated then exact",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Transition",
                "Other audit",
                second_value=validator.TARGET_SET_TRANSITION,
            ),
        ),
        (
            "duplicate Transaction State Prepared then Committed",
            lambda root: _write_modern_ambiguous_json_fixture(
                root, "Transaction State", "Prepared"
            ),
        ),
        (
            "duplicate Transaction State Committed then Prepared",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Transaction State",
                "Committed",
                second_value="Prepared",
            ),
        ),
        *[
            (
                f"duplicate modern journal field {field}",
                lambda root, field=field, first=first: _write_modern_ambiguous_json_fixture(
                    root, field, first
                ),
            )
            for field, first in (
                ("Lock ID", "hidden-lock"),
                ("Workload ID", "hidden-workload"),
                ("Snapshot", "hidden-snapshot"),
                ("Targets", []),
            )
        ],
        *[
            (
                f"duplicate nested target field {field}",
                lambda root, field=field, first=first, existing=existing: _write_modern_ambiguous_json_fixture(
                    root,
                    field,
                    first,
                    nested=True,
                    existing_value=existing,
                ),
            )
            for field, first, existing in (
                ("Target", "hidden/target.md", None),
                ("Before SHA256", "0" * 64, None),
                ("After SHA256", "0" * 64, None),
                ("Assignments", [], ["State Version=2"]),
                ("Post Record State", "historical-receipt", "live"),
            )
        ],
        *[
            (
                f"duplicate compatibility registry field {field}",
                lambda root, field=field, first=first, row_field=row_field: _write_ambiguous_registry_fixture(
                    root,
                    field,
                    first,
                    row_field=row_field,
                ),
            )
            for field, first, row_field in (
                ("Schema", "invalid-schema", False),
                ("Purpose", "invalid-purpose", False),
                ("Receipts", [], False),
                ("Audit Path", "audit_log/hidden.json", True),
                ("SHA256", "0" * 64, True),
                ("Compatibility Profile", "hidden-profile", True),
                ("Receipt Class", "hidden-class", True),
                ("Immutable Purpose", "hidden-purpose", True),
            )
        ],
        (
            "case-ambiguous Transition field",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Transition",
                validator.TARGET_SET_TRANSITION,
                second_value="Other audit",
                second_key="transition",
            ),
        ),
        (
            "case-ambiguous Transaction State field",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Transaction State",
                "Committed",
                second_value="Prepared",
                second_key="transaction state",
            ),
        ),
        (
            "case-ambiguous nested Target field",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Target",
                "worktrees/Fixture/worktree_state.md",
                second_value="hidden/target.md",
                second_key="target",
                nested=True,
            ),
        ),
        (
            "case-ambiguous nested SHA256 field",
            lambda root: _write_modern_ambiguous_json_fixture(
                root,
                "Before SHA256",
                "a" * 64,
                second_value="0" * 64,
                second_key="before sha256",
                nested=True,
            ),
        ),
        (
            "case-ambiguous compatibility registry Schema",
            lambda root: _write_ambiguous_registry_fixture(
                root,
                "Schema",
                validator.LEGACY_RECEIPT_COMPATIBILITY_SCHEMA,
                second_key="schema",
            ),
        ),
        (
            "case-ambiguous compatibility registry SHA256",
            lambda root: _write_ambiguous_registry_fixture(
                root,
                "SHA256",
                "0" * 64,
                second_key="sha256",
                row_field=True,
            ),
        ),
        (
            "legacy receipt with duplicate lock evidence",
            lambda root: _write_ambiguous_legacy_evidence_fixture(root, "lock"),
        ),
        (
            "legacy receipt with duplicate snapshot evidence",
            lambda root: _write_ambiguous_legacy_evidence_fixture(root, "snapshot"),
        ),
        (
            "legacy receipt with case-ambiguous lock evidence",
            lambda root: _write_ambiguous_legacy_evidence_fixture(
                root,
                "lock",
                second_key="lock state",
            ),
        ),
        (
            "legacy receipt with case-ambiguous snapshot evidence",
            lambda root: _write_ambiguous_legacy_evidence_fixture(
                root,
                "snapshot",
                second_key="copied files",
            ),
        ),
        (
            "legacy receipt with non-object lock evidence",
            lambda root: _write_non_object_legacy_evidence_fixture(root, "lock"),
        ),
        (
            "legacy receipt with non-object snapshot evidence",
            lambda root: _write_non_object_legacy_evidence_fixture(root, "snapshot"),
        ),
        (
            "legacy-looking receipt with recovery payload",
            lambda root: _write_legacy_journal_fixture(root, recovery_payload=True),
        ),
        (
            "legacy receipt with active lock evidence",
            lambda root: _write_legacy_journal_fixture(root, lock_state="Locked"),
        ),
        *[
            (
                f"legacy receipt lock has whitespace-padded {field}",
                lambda root, field=field: _write_legacy_padded_lock_field_fixture(
                    root,
                    field,
                ),
            )
            for field in (
                "External State Schema",
                "Lock ID",
                "Lock State",
                "Workload ID",
                "Workload State",
                "Retain Between Workloads",
            )
        ],
        (
            "legacy receipt with malformed release timestamp",
            lambda root: _write_legacy_released_at_fixture(root, "No release occurred"),
        ),
        (
            "legacy receipt with lock released before transaction",
            lambda root: _write_legacy_released_at_fixture(
                root,
                "2000-01-01T00:00:00Z",
            ),
        ),
        (
            "legacy receipt with lock released in the future",
            lambda root: _write_legacy_released_at_fixture(
                root,
                "2099-01-01T00:00:00Z",
            ),
        ),
        (
            "legacy receipt with snapshot created after transaction",
            lambda root: _write_legacy_snapshot_updated_fixture(
                root,
                "2099-01-01T00:00:00Z",
            ),
        ),
        (
            "legacy receipt with malformed transaction timestamp",
            lambda root: _write_legacy_receipt_updated_fixture(
                root,
                "No transaction occurred",
            ),
        ),
        (
            "legacy receipt with unexpected lock write-set target",
            _write_legacy_lock_write_set_extra_fixture,
        ),
        (
            "legacy receipt with ambiguous workload evidence",
            lambda root: _write_legacy_journal_fixture(
                root, lock_workload_id="different-workload"
            ),
        ),
        (
            "legacy receipt lacking completion evidence",
            lambda root: _write_legacy_journal_fixture(root, completion_assignment=False),
        ),
        (
            "only one target row has completion evidence",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete, [], []],
            ),
        ),
        (
            "one target row has no completion disposition",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete, [], complete],
            ),
        ),
        (
            "one row PASS while another Pending",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [
                    complete,
                    [
                        "External State Item Status=Complete",
                        "Current Validation State=Pending",
                    ],
                    complete,
                ],
            ),
        ),
        (
            "one row Complete while another Not complete",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [
                    complete,
                    [
                        "External State Item Status=Not complete",
                        "Current Validation State=PASS",
                    ],
                    complete,
                ],
            ),
        ),
        *[
            (
                f"completion phrase rejected: {phrase}",
                lambda root, phrase=phrase: _write_legacy_completion_matrix_fixture(
                    root,
                    [
                        [
                            "External State Item Status=Complete",
                            f"Current Validation State={phrase}",
                        ]
                    ]
                    * 3,
                ),
            )
            for phrase in (
                "not yet complete",
                "pending pass",
                "pass pending validation",
                "will complete after review",
                "complete only after USER review",
                "failed; pass expected",
                "completion unproven",
                "no pass recorded",
            )
        ],
        (
            "contradictory completion fields in one row",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [
                    [
                        "External State Item Status=Complete",
                        "Current Validation State=Pending",
                        "Final Disposition=Complete",
                    ]
                ]
                * 3,
            ),
        ),
        (
            "positive completion token in descriptive prose",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [
                    [
                        "External State Item Status=Report mentions complete migration",
                        "Current Validation State=PASS expected after review",
                    ]
                ]
                * 3,
            ),
        ),
        (
            "positive row paired with malformed assignment",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete, [*complete, 17], complete],
            ),
        ),
        (
            "positive row paired with ambiguous assignment",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete, [*complete, "Validation required"], complete],
            ),
        ),
        (
            "historical target row carries live completion",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete, complete],
                post_record_states=["live", "historical-receipt"],
            ),
        ),
        (
            "unknown target Post Record State",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete],
                post_record_states=["pending"],
            ),
        ),
        (
            "legacy receipt with alternate-stream target",
            lambda root: _write_legacy_journal_fixture(
                root,
                first_target_override="worktrees/Fixture-1/worktree_state.md:stream",
            ),
        ),
        (
            "legacy receipt with case-alias duplicate target",
            _write_legacy_case_alias_fixture,
        ),
        (
            "modern journal with case-alias duplicate target",
            _write_modern_case_alias_fixture,
        ),
        (
            "legacy receipt with inconsistent snapshot hash",
            lambda root: _write_legacy_journal_fixture(
                root, inconsistent_snapshot_hash=True
            ),
        ),
        (
            "state-less modern journal with old timestamp",
            lambda root: _write_modern_journal_fixture(
                root, include_state=False, last_updated="2020-01-01T00:00:00Z"
            ),
        ),
        (
            "state-less modern journal with historical-looking filename",
            lambda root: _write_modern_journal_fixture(
                root, filename="legacy-completed-20200101.json", include_state=False
            ),
        ),
    ]
    for name, setup in negative_cases:
        needs_admitted_identity = name.startswith(
            (
                "legacy-looking receipt with recovery",
                "legacy receipt with",
                "only one target",
                "one target",
                "one row",
                "completion phrase rejected",
                "contradictory completion",
                "positive completion",
                "positive row",
                "historical target",
                "unknown target",
            )
        )
        _run_journal_case(
            name,
            setup,
            should_pass=False,
            admitted_profile=(
                PROFILE_BY_RECEIPT["receipt-1"] if needs_admitted_identity else None
            ),
        )

    _assert_modern_audit_reparse_rejected(
        "audit_log directory reparse boundary",
        "directory",
    )
    _assert_modern_audit_reparse_rejected(
        "journal file reparse boundary",
        "file",
    )
    _assert_broken_audit_reparse_rejected()
    _assert_snapshot_hash_read_failure_reported()
    _assert_snapshot_walk_error_reported()
    _assert_snapshot_directory_replacement_race_rejected()
    _assert_snapshot_child_mutation_race_rejected()
    _assert_snapshot_inventory_creation_race_rejected()
    _assert_audit_inventory_creation_race_rejected()
    _assert_audit_final_inventory_creation_race_rejected()
    _assert_audit_creation_during_final_lock_validation_rejected()
    _assert_audit_creation_during_final_hash_rejected()
    _assert_audit_rediscovery_failure_rejected()
    _assert_live_target_final_revalidation_rejected()
    _assert_snapshot_final_revalidation_rejected()
    _assert_lock_final_revalidation_rejected()
    _assert_audit_file_replacement_race_rejected()
    _assert_snapshot_manifest_replacement_race_rejected()
    _assert_lock_replacement_race_rejected()
    _assert_oversized_evidence_rejected()
    _assert_missing_audit_root_rejected()
    _assert_evidence_read_memory_error_reported()
    _assert_snapshot_hash_replacement_race_rejected()
    _assert_journal_read_replacement_race_rejected()
    _assert_posix_case_sensitive_evidence_paths()
    _assert_relative_snapshot_manifest_root_rejected()

    negative_setups = dict(negative_cases)
    accept_missing_state = lambda *_args, **_kwargs: []
    def accept_modern_state(
        payload: dict[str, object],
        target_before_hashes: dict[str, str] | None = None,
        target_after_hashes: dict[str, str] | None = None,
    ) -> list[str]:
        if target_before_hashes is not None:
            first_before_hash = ""
            rows = payload.get("Targets")
            for row in rows if isinstance(rows, list) else []:
                if not isinstance(row, dict):
                    continue
                parts = validator._safe_external_relative_parts(row.get("Target"))
                before_hash = row.get("Before SHA256")
                if not first_before_hash and isinstance(before_hash, str):
                    first_before_hash = before_hash.casefold()
                if parts and isinstance(before_hash, str):
                    target_before_hashes[
                        validator._host_path_key("/".join(parts))
                    ] = before_hash.casefold()
            if not target_before_hashes and first_before_hash:
                target_before_hashes[
                    validator._host_path_key("worktrees/Fixture/worktree_state.md")
                ] = first_before_hash
        return []
    accept_completion_set = lambda *_args: []
    accept_completion_profile = lambda _values: PROFILE_BY_RECEIPT["receipt-1"]
    accept_unregistered_identity = lambda *_args, **_kwargs: (
        PROFILE_BY_RECEIPT["receipt-1"],
        [],
    )
    permissive_json_loads = lambda text: json.loads(text)
    permissive_json_path = lambda path: validator.load_json(path)
    _assert_journal_mutation_killed(
        "ordinary json.loads last-value-wins restored",
        negative_setups["duplicate modern journal field Lock ID"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "duplicate Transition ignored",
        negative_setups["duplicate Transition exact then unrelated"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "duplicate Transaction State ignored",
        negative_setups["duplicate Transaction State Prepared then Committed"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "Prepared hidden by later Committed",
        negative_setups["duplicate Transaction State Prepared then Committed"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "duplicate nested target fields ignored",
        negative_setups["duplicate nested target field Target"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "duplicate compatibility registry fields ignored",
        negative_setups["duplicate compatibility registry field Audit Path"],
        "_strict_json_load_path",
        permissive_json_path,
    )
    _assert_journal_mutation_killed(
        "duplicate supporting lock fields ignored",
        negative_setups["legacy receipt with duplicate lock evidence"],
        "_strict_json_loads",
        permissive_json_loads,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "duplicate supporting snapshot fields ignored",
        negative_setups["legacy receipt with duplicate snapshot evidence"],
        "_strict_json_loads",
        permissive_json_loads,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "case-ambiguous critical names accepted",
        negative_setups["case-ambiguous Transition field"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "case-ambiguous snapshot Root accepted",
        negative_setups["modern Committed journal with case-ambiguous snapshot Root"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_false_positive_mutation_killed(
        "strict parsing and raw hashing use different bytes",
        _write_unique_registry_fixture,
        "_strict_json_loads",
        lambda text: json.loads(
            text.replace(
                "worktrees/Fixture-1/worktree_state.md",
                "worktrees/Changed-1/worktree_state.md",
            )
        ),
    )
    _assert_journal_mutation_killed(
        "accept every missing Transaction State",
        negative_setups["modern journal missing Transaction State"],
        "_validate_legacy_completed_target_set_receipt",
        accept_missing_state,
    )
    _assert_journal_mutation_killed(
        "accept every old record",
        negative_setups["state-less modern journal with old timestamp"],
        "_validate_legacy_completed_target_set_receipt",
        accept_missing_state,
    )
    _assert_journal_mutation_killed(
        "transition phrase alone proves completion",
        lambda root: atomic_write_json(
            root / "audit_log" / "transition-only.json",
            {"Transition": validator.TARGET_SET_TRANSITION},
        ),
        "_validate_legacy_completed_target_set_receipt",
        accept_missing_state,
    )
    _assert_journal_mutation_killed(
        "Prepared treated as Committed",
        negative_setups["modern Prepared journal"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "whitespace-padded Transaction State accepted",
        negative_setups["modern journal with whitespace-padded Transaction State"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "malformed state ignored",
        negative_setups["modern journal unknown Transaction State"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "case-variant recoverable Before Text ignored",
        negative_setups["modern journal with case-variant recoverable Before Text"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "nested recovery payload ignored",
        negative_setups["modern journal with recoverable Before Text at nested"],
        "_contains_recovery_payload_field",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "nested recovery payload alias ignored",
        negative_setups[
            "modern journal with nested recovery payload alias Recovery Payload"
        ],
        "_contains_recovery_payload_field",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "before-content recovery payload alias ignored",
        negative_setups[
            "modern journal with nested recovery payload alias Before Content"
        ],
        "_contains_recovery_payload_field",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "non-JSON target-set audit entry ignored",
        negative_setups[
            "target-set transaction stored in a non-JSON audit entry"
        ],
        "_is_non_json_audit_entry",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "plain-text target-set audit entry ignored",
        negative_setups[
            "plain-text target-set transaction stored in a non-JSON audit entry"
        ],
        "_raw_text_has_target_set_transition",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "BOM-less UTF-16 target-set audit accepted as NUL-bearing UTF-8",
        negative_setups[
            "plain-text target-set transaction stored in BOM-less UTF-16LE"
        ],
        "_decode_non_json_audit_text",
        lambda raw_bytes: raw_bytes.decode("utf-8"),
    )
    _assert_journal_mutation_killed(
        "non-object JSON target-set root ignored",
        negative_setups[
            "target-set transaction stored below a non-object JSON root"
        ],
        "_json_value_has_target_set_transition",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "wrapped JSON target-set object ignored",
        negative_setups[
            "target-set transaction wrapped below an object JSON root"
        ],
        "_json_value_has_target_set_transition",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "camelCase recovery payload alias ignored",
        negative_setups[
            "modern journal with nested recovery payload alias BeforeText"
        ],
        "_contains_recovery_payload_field",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "backup recovery payload alias ignored",
        negative_setups[
            "modern journal with nested recovery payload alias Backup Content"
        ],
        "_contains_recovery_payload_field",
        lambda *_args, **_kwargs: False,
    )
    _assert_journal_mutation_killed(
        "modern committed journal audit metadata ignored",
        negative_setups["modern journal missing audit metadata Last Updated"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "future modern transaction timestamp accepted",
        negative_setups["modern journal with future transaction timestamp"],
        "_transaction_timestamp_is_not_future",
        lambda *_args, **_kwargs: True,
    )
    _assert_journal_mutation_killed(
        "unchanged modern target hash accepted",
        negative_setups["modern journal with unchanged target hash"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "non-string modern SHA256 coerced",
        negative_setups[
            "modern journal with non-string SHA256 that stringifies as hexadecimal"
        ],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "non-string modern target coerced",
        negative_setups["modern journal with non-string Target boolean"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "modern active-lock evidence ignored",
        negative_setups["modern Committed journal with active lock evidence"],
        "_validate_modern_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "malformed modern release timestamp accepted",
        negative_setups["modern Committed journal with malformed release timestamp"],
        "_validate_modern_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "modern lock release chronology ignored",
        negative_setups[
            "modern Committed journal lock released before the transaction"
        ],
        "_validate_modern_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "future modern lock release accepted",
        negative_setups["modern Committed journal lock released in the future"],
        "_validate_modern_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "modern snapshot evidence ignored",
        negative_setups["modern Committed journal with missing snapshot manifest"],
        "_validate_modern_snapshot_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "modern snapshot transaction chronology ignored",
        negative_setups[
            "modern Committed journal snapshot postdates the transaction"
        ],
        "_validate_modern_snapshot_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "modern committed live-target After SHA256 evidence ignored",
        negative_setups["modern Committed journal with unrelated live target"],
        "_validate_modern_committed_target_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "unexpected modern snapshot file accepted",
        negative_setups[
            "modern Committed journal snapshot contains an unexpected file"
        ],
        "_validate_modern_snapshot_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "unmanifested modern snapshot file accepted",
        negative_setups[
            "modern Committed journal snapshot contains an unmanifested file"
        ],
        "_validate_modern_snapshot_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "shared snapshots namespace root accepted as isolated evidence",
        negative_setups[
            "modern Committed journal uses the shared snapshots namespace root"
        ],
        "_validate_modern_snapshot_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "modern lock write-set evidence ignored",
        negative_setups["modern lock write set omits target"],
        "_validate_modern_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "unexpected modern lock write-set evidence ignored",
        negative_setups["modern lock write set includes unexpected target"],
        "_validate_modern_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "unexpected legacy lock write-set evidence ignored",
        negative_setups["legacy receipt with unexpected lock write-set target"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "whitespace-padded legacy lock state accepted",
        negative_setups["legacy receipt lock has whitespace-padded Lock State"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "malformed legacy release timestamp accepted",
        negative_setups["legacy receipt with malformed release timestamp"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "legacy lock release chronology ignored",
        negative_setups["legacy receipt with lock released before transaction"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "future legacy lock release accepted",
        negative_setups["legacy receipt with lock released in the future"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "legacy snapshot transaction chronology ignored",
        negative_setups["legacy receipt with snapshot created after transaction"],
        "_validate_legacy_snapshot_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "whitespace-padded modern target path normalized",
        negative_setups["modern evidence has whitespace-padded journal target"],
        "_safe_external_relative_parts",
        lambda value: tuple(value.strip().replace("\\", "/").split("/"))
        if isinstance(value, str) and value.strip()
        else None,
    )
    _assert_journal_mutation_killed(
        "non-standard journal numeric constant accepted",
        negative_setups["modern evidence contains non-standard numeric constant in journal"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "non-standard snapshot numeric constant accepted",
        negative_setups["modern evidence contains non-standard numeric constant in snapshot"],
        "_strict_json_loads",
        permissive_json_loads,
    )
    _assert_journal_mutation_killed(
        "impossible modern target path accepted",
        negative_setups["modern journal with impossible Target NUL"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_false_positive_mutation_killed(
        "nested malformed Transition treated as top-level",
        _write_malformed_nested_transition_fixture,
        "_raw_text_has_target_set_transition",
        lambda text: validator.TARGET_SET_TRANSITION in text,
    )
    _assert_journal_mutation_killed(
        "mismatched delimiter hides top-level Transition",
        negative_setups["matching malformed JSON after mismatched delimiter"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "missing comma hides a plausible top-level Transition member",
        negative_setups[
            "matching malformed JSON with missing comma before Transition"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "unquoted Transition key hides a target-set transaction",
        negative_setups["matching malformed JSON with unquoted Transition key"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "mismatched nested delimiter returns at an inner comma",
        negative_setups["matching malformed JSON after mismatched nested comma"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "mismatched nested delimiter discards a nonempty inner container",
        negative_setups["matching malformed JSON after mismatched nested member"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "unmatched inner closer discards accountable malformed depth",
        negative_setups["matching malformed JSON after unmatched inner closer"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "mismatched closer consumes the malformed-audit root frame",
        negative_setups[
            "matching malformed JSON after mismatched closers reach root frame"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "leading junk hides a target-set Transition",
        negative_setups["matching malformed JSON after leading junk"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "quoted junk brace hides a target-set Transition",
        negative_setups[
            "matching malformed JSON after quoted junk with a brace"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "unreadable top-level Transition value ignored",
        negative_setups["matching malformed JSON with unreadable Transition value"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "invalid string escape and brace hide top-level Transition",
        negative_setups["matching malformed JSON after invalid string escape and brace"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "illegal container after decoded value hides top-level Transition",
        negative_setups[
            "matching malformed JSON with illegal container after decoded value"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "unterminated container value hides top-level Transition",
        negative_setups["matching malformed JSON with unterminated container value"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "stray container after member delimiter hides top-level Transition",
        negative_setups[
            "matching malformed JSON with stray container after member delimiter"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "stray array after member delimiter hides top-level Transition",
        negative_setups[
            "matching malformed JSON with stray array after member delimiter"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "stray container after malformed key hides top-level Transition",
        negative_setups[
            "matching malformed JSON with stray container after malformed key"
        ],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "BOM-prefixed target-set journal ignored",
        negative_setups["BOM-prefixed modern Prepared journal"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "uppercase JSON audit extension ignored",
        negative_setups["uppercase-extension modern Prepared journal"],
        "_is_json_audit_entry",
        lambda path: path.suffix == ".json",
    )
    _assert_journal_mutation_killed(
        "escaped malformed Transition key ignored",
        negative_setups["matching malformed JSON with escaped Transition key"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "escaped malformed Transition value ignored",
        negative_setups["matching malformed JSON with escaped Transition value"],
        "_raw_text_has_target_set_transition",
        lambda _text: False,
    )
    _assert_journal_mutation_killed(
        "active-lock evidence ignored",
        negative_setups["legacy receipt with active lock evidence"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "any one completed row greens the target set",
        negative_setups["only one target row has completion evidence"],
        "_validate_legacy_completion_evidence",
        accept_completion_set,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "missing row-level completion ignored",
        negative_setups["one target row has no completion disposition"],
        "_validate_legacy_completion_evidence",
        accept_completion_set,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "contradictory completion fields ignored",
        negative_setups["contradictory completion fields in one row"],
        "_legacy_completion_profile",
        accept_completion_profile,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "any occurrence of pass accepted",
        negative_setups["completion phrase rejected: pending pass"],
        "_legacy_completion_profile",
        accept_completion_profile,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "any occurrence of complete accepted",
        negative_setups["completion phrase rejected: will complete after review"],
        "_legacy_completion_profile",
        accept_completion_profile,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "negation checked only immediately before positive word",
        negative_setups["completion phrase rejected: not yet complete"],
        "_legacy_completion_profile",
        accept_completion_profile,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "pending future conditional wording accepted",
        negative_setups["completion phrase rejected: complete only after USER review"],
        "_legacy_completion_profile",
        accept_completion_profile,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "released lock accepted without coherent receipt completion",
        negative_setups["legacy receipt lacking completion evidence"],
        "_validate_legacy_completion_evidence",
        accept_completion_set,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "historical provenance checks skipped",
        negative_setups["legacy receipt with inconsistent snapshot hash"],
        "_validate_legacy_snapshot_evidence",
        lambda *_args, **_kwargs: [],
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_mutation_killed(
        "path match accepted without immutable hash match",
        _write_tampered_admitted_receipt_fixture,
        "_validate_legacy_receipt_identity",
        _accept_registered_path_without_hash,
    )
    _assert_journal_mutation_killed(
        "immutable hash accepted at another audit path",
        _write_renamed_admitted_receipt_fixture,
        "_validate_legacy_receipt_identity",
        _accept_registered_hash_without_path,
    )
    _assert_journal_mutation_killed(
        "immutable identity registry skipped",
        lambda root: _write_exact_real_legacy_receipt_fixture(root, "receipt-1"),
        "_validate_legacy_receipt_identity",
        accept_unregistered_identity,
    )
    _assert_journal_mutation_killed(
        "filename or age heuristic admits an unregistered receipt",
        lambda root: _write_legacy_journal_fixture(
            root,
            filename="legacy-completed-20200101.json",
        ),
        "_validate_legacy_receipt_identity",
        accept_unregistered_identity,
    )
    _assert_journal_mutation_killed(
        "generic Complete/PASS profile admitted in production",
        negative_setups["new state-less legacy-shaped receipt with generic Complete/PASS"],
        "_legacy_completion_profile",
        accept_completion_profile,
        admitted_profile=PROFILE_BY_RECEIPT["receipt-1"],
    )
    _assert_journal_false_positive_mutation_killed(
        "raw substring discovery selects phrase-only Notes",
        lambda root: atomic_write_json(
            root / "audit_log" / "notes-only.json",
            {
                "External State Schema": "external-state-v1",
                "Transition": "Other audit",
                "Notes": validator.TARGET_SET_TRANSITION,
            },
        ),
        "_is_target_set_transaction",
        lambda payload: validator.TARGET_SET_TRANSITION in json.dumps(payload),
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ndai-target-currentness-") as temp_dir:
        root = Path(temp_dir)
        _manifest(root)
        target = _record(root)
        _assert_pass("valid selected live projection", _run(root))
        _assert_pass("stale root manifest is separate posture", _run(root))

        for label, original, expected_failure in (
            (
                "fenced-only schema field",
                "External State Schema: `external-state-v1`",
                "External State Schema Conflict",
            ),
            (
                "fenced-only record class",
                "Record Class: `Live Worktree Projection`",
                "unsupported or missing live Record Class",
            ),
            (
                "fenced-only record role",
                "Record Role: `Current worktree assignment projection`",
                "requires exactly one Record Role marker",
            ),
            (
                "fenced-only historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "requires exactly one Historical Receipt Boundary marker",
            ),
            (
                "fenced-only branch identity",
                "Branch: `feature/release-readiness-source-truth-intake`",
                "missing required field Branch",
            ),
            (
                "fenced-only source-head identity",
                f"Source Repo HEAD: `{HEAD}`",
                "missing required field Source Repo HEAD",
            ),
            (
                "fenced-only origin-main identity",
                f"Origin/Main: `{ORIGIN_MAIN}`",
                "missing required field Origin/Main",
            ),
            (
                "fenced-only worktree identity",
                f"Worktree Path: `{WORKTREE_PATH}`",
                "missing required field Worktree Path",
            ),
            (
                "fenced-only slot identity",
                f"Slot ID: `{SLOT}`",
                "missing required field Slot ID",
            ),
        ):
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    original,
                    f"```text\n{original}\n```",
                    1,
                ),
                encoding="utf-8",
            )
            _assert_failure(label, expected_failure, _run(root))
            _record(root)

        for label, opener, closer in (
            ("backtick-fenced duplicate authority examples", "```text", "```"),
            ("tilde-fenced duplicate authority examples", "~~~text", "~~~~"),
        ):
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\n".join(
                    [
                        opener,
                        "Record Role: `Historical receipt only`",
                        "Historical Receipt Boundary: `Historical receipts redefine live authority.`",
                        "Branch: `feature/wrong-fenced-branch`",
                        f"Source Repo HEAD: `{'f' * 40}`",
                        "## Historical Receipts",
                        closer,
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            _assert_pass(label, _run(root))
            _record(root)

        target.write_text(
            target.read_text(encoding="utf-8").replace(
                "Branch: `feature/release-readiness-source-truth-intake`",
                "```markdown\n## Historical Receipts\nBranch: `feature/wrong-fenced-branch`\n```\n"
                "Branch: `feature/release-readiness-source-truth-intake`",
                1,
            ),
            encoding="utf-8",
        )
        _assert_pass("fenced level-two heading does not terminate live authority", _run(root))
        _record(root)

        target.write_text(
            target.read_text(encoding="utf-8")
            + "```text\nBranch: `feature/wrong-fenced-branch`\n",
            encoding="utf-8",
        )
        _assert_failure(
            "unterminated target-currentness fence",
            "unterminated fenced block",
            _run(root),
        )
        _record(root)

        _assert_failure(
            "wrong branch",
            "Branch mismatch",
            _run(root, expected_branch="feature/wrong-branch"),
        )
        _assert_failure(
            "wrong source head",
            "Source Repo HEAD mismatch",
            _run(root, expected_source_head="d" * 40),
        )
        _assert_failure(
            "wrong origin main",
            "Origin/Main mismatch",
            _run(root, expected_origin_main="e" * 40),
        )
        _assert_failure(
            "wrong worktree",
            "Worktree Path mismatch",
            _run(root, expected_worktree_path=r"C:\Nexus Worktrees\FAM-007"),
        )
        _assert_failure(
            "wrong slot",
            "Slot ID mismatch",
            _run(root, expected_worktree_slot="runtime-active-1"),
        )
        _assert_failure(
            "stale hash",
            "hash precondition failed",
            _run(root, expected_target_sha256="f" * 64),
        )
        target.write_text(
            target.read_text(encoding="utf-8").replace(
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current worktree assignment projection has not expired`",
                1,
            ),
            encoding="utf-8",
        )
        _assert_pass("explicitly non-expired live role", _run(root))
        _record(root)
        for protective_role in (
            "Current authority is not suspended",
            "Current live authority is not disabled",
            "Current projection is not on hold",
            "Current authority is not revoked",
            "Current assignment is not frozen",
        ):
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{protective_role}`",
                    1,
                ),
                encoding="utf-8",
            )
            _assert_pass(f"protective live role: {protective_role}", _run(root))
            _record(root)
        target.write_text(
            target.read_text(encoding="utf-8").replace(
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts do not restore live authority.`",
                1,
            ),
            encoding="utf-8",
        )
        _assert_pass("explicitly non-restoring historical boundary", _run(root))
        _record(root)
        for protective_boundary in (
            "Historical receipts do not redefine current state.",
            "Historical receipts never control active ownership.",
            "Historical identity evidence only and does not grant current assignment or write authority.",
            "Live authority is not granted by historical receipts.",
        ):
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                    f"Historical Receipt Boundary: `{protective_boundary}`",
                    1,
                ),
                encoding="utf-8",
            )
            _assert_pass(
                f"live-authority-bound historical boundary: {protective_boundary}",
                _run(root),
            )
            _record(root)
        for label, original, replacement, expected_failure in (
            (
                "blank record role",
                "Record Role: `Current worktree assignment projection`",
                "Record Role:",
                "Record Role is not affirmative live authority",
            ),
            (
                "historical-only record role",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Historical receipt only`",
                "Record Role is not affirmative live authority",
            ),
            (
                "negated record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current state has no authority.`",
                "Record Role is not affirmative live authority",
            ),
            *[
                (
                    f"explicitly non-authoritative record role: {value}",
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{value}`",
                    "Record Role is not affirmative live authority",
                )
                for value in (
                    "Current authority is not authoritative",
                    "Current assignment is not an authoritative role",
                    "Current projection remains not authoritative",
                )
            ],
            *[
                (
                    f"explicitly inactive live-role identity: {value}",
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{value}`",
                    "Record Role is not affirmative live authority",
                )
                for value in (
                    "Current authority is not active",
                    "Current authority is not current",
                    "Active authority is not live",
                    "Current projection is no longer live",
                    "Live assignment remains not current",
                )
            ],
            *[
                (
                    f"embedded live-identity token record role: {value}",
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{value}`",
                    "Record Role is not affirmative live authority",
                )
                for value in (
                    "Delivery authority",
                    "Delivery state",
                    "Current statement",
                )
            ],
            (
                "future-gated record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current state authority will begin after USER approval`",
                "Record Role is not affirmative live authority",
            ),
            (
                "pending-activation record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current state authority is pending activation`",
                "Record Role is not affirmative live authority",
            ),
            *[
                (
                    f"ended record role authority: {value}",
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{value}`",
                    "Record Role is not affirmative live authority",
                )
                for value in (
                    "Current state authority has ended",
                    "Current live assignment was terminated",
                    "Active projection has expired",
                    "Closed current state authority",
                )
            ],
            *[
                (
                    f"never-active record role authority: {value}",
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{value}`",
                    "Record Role is not affirmative live authority",
                )
                for value in (
                    "Current authority was never active",
                    "Current authority has not started",
                    "Current live authority failed to activate",
                    "Active projection never became active",
                    "Current authority did not activate",
                    "Current projection is not activated",
                    "Current authority never active",
                    "Current assignment failed activation",
                )
            ],
            *[
                (
                    f"held record role authority: {value}",
                    "Record Role: `Current worktree assignment projection`",
                    f"Record Role: `{value}`",
                    "Record Role is not affirmative live authority",
                )
                for value in (
                    "Current authority is suspended",
                    "Current live authority is disabled",
                    "Current authority is paused",
                    "Current assignment was deactivated",
                    "Current authority remains dormant",
                    "Current projection is on hold",
                    "Current authority is frozen",
                    "Revoked current authority projection",
                    "Current assignment was withdrawn",
                    "Current projection was cancelled",
                )
            ],
            (
                "nominal record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current worktree assignment projection exists only on paper`",
                "Record Role is not affirmative live authority",
            ),
            (
                "forged record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Forged current worktree assignment projection`",
                "Record Role is not affirmative live authority",
            ),
            (
                "invalid record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current worktree assignment projection is invalid`",
                "Record Role is not affirmative live authority",
            ),
            (
                "unverified record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Unverified current worktree assignment projection`",
                "Record Role is not affirmative live authority",
            ),
            (
                "non-operational record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current worktree assignment projection is non-operational`",
                "Record Role is not affirmative live authority",
            ),
            (
                "duplicate record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current worktree assignment projection`\nRecord Role: `Historical receipt only`",
                "requires exactly one Record Role marker",
            ),
            (
                "case-variant duplicate record role authority",
                "Record Role: `Current worktree assignment projection`",
                "Record Role: `Current worktree assignment projection`\nrecord role: `Historical receipt only`",
                "requires exactly one Record Role marker",
            ),
            (
                "blank historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary:",
                "Historical Receipt Boundary does not prevent",
            ),
            (
                "contradictory historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts redefine the live fields.`",
                "Historical Receipt Boundary does not prevent",
            ),
            (
                "conditional historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts cannot redefine live authority unless approved.`",
                "Historical Receipt Boundary does not prevent",
            ),
            *[
                (
                    f"in-clause conditional historical boundary: {value}",
                    "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                    f"Historical Receipt Boundary: `{value}`",
                    "Historical Receipt Boundary does not prevent",
                )
                for value in (
                    "Historical receipts do not unless approved redefine live authority",
                    "Historical receipts do not redefine unless approved live authority",
                    "Historical receipts do not redefine live authority if approved",
                    "Historical receipts subject to approval do not redefine current state",
                )
            ],
            *[
                (
                    f"irrelevant historical boundary: {value}",
                    "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                    f"Historical Receipt Boundary: `{value}`",
                    "Historical Receipt Boundary does not prevent",
                )
                for value in (
                    "Historical receipts do not redefine archived notes",
                    "Historical receipts do not own old metadata",
                    "Historical receipts never control formatting",
                    "Historical receipts do not retain archived settings",
                )
            ],
            (
                "retained active assignment historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts do not redefine live fields; retained active assignment remains.`",
                "Historical Receipt Boundary does not prevent",
            ),
            (
                "receipt-sourced authority historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts do not redefine live fields; current authority comes from the receipt.`",
                "Historical Receipt Boundary does not prevent",
            ),
            (
                "receipt-derived ownership historical boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts do not redefine live fields; receipt-derived ownership remains active.`",
                "Historical Receipt Boundary does not prevent",
            ),
            *[
                (
                    f"positive receipt-owned authority historical boundary: {value}",
                    "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                    f"Historical Receipt Boundary: `{value}`",
                    "Historical Receipt Boundary does not prevent",
                )
                for value in (
                    "Historical receipts do not redefine live authority; historical receipts are authoritative",
                    "Historical receipts do not redefine live authority; historical receipt has live authority",
                    "Historical receipts do not redefine live authority; historical evidence owns current assignment",
                    "Historical receipts do not redefine live authority; archive controls active state",
                )
            ],
            *[
                (
                    f"restored authority historical boundary: {value}",
                    "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                    f"Historical Receipt Boundary: `Historical receipts do not redefine live fields; {value}.`",
                    "Historical Receipt Boundary does not prevent",
                )
                for value in (
                    "active assignment is restored",
                    "authority was renewed",
                    "ownership is reinstated",
                    "live control was reactivated",
                )
            ],
            (
                "duplicate historical receipt boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`\nHistorical Receipt Boundary: `Historical receipts redefine the live fields.`",
                "requires exactly one Historical Receipt Boundary marker",
            ),
            (
                "case-variant duplicate historical receipt boundary",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`\nhistorical receipt boundary: `Historical receipts redefine the live fields.`",
                "requires exactly one Historical Receipt Boundary marker",
            ),
        ):
            target.write_text(
                target.read_text(encoding="utf-8").replace(original, replacement, 1),
                encoding="utf-8",
            )
            _assert_failure(label, expected_failure, _run(root))
            _record(root)
        _assert_failure(
            "missing target",
            "selected target is missing",
            validator.validate_target_currentness(
                root,
                ["worktrees/Missing/worktree_state.md"],
                **_expectations(target),
            ),
        )
        _assert_failure(
            "traversal target",
            "traversal or alias",
            validator.validate_target_currentness(root, ["worktrees/../worktree_state.md"], **_expectations(target)),
        )
        _assert_failure(
            "absolute target",
            "absolute/off-root",
            validator.validate_target_currentness(root, [str(target)], **_expectations(target)),
        )
        _assert_failure(
            "duplicate target selection",
            "exactly one explicit target",
            validator.validate_target_currentness(root, [TARGET, TARGET], **_expectations(target)),
        )
        for alias_target, label in (
            ("worktrees//Governance/worktree_state.md", "repeated separator"),
            ("worktrees/Governance/worktree_state.md/", "trailing separator"),
            ("worktrees\\Governance/worktree_state.md", "mixed separator"),
            ("worktrees/Governance/worktree_state.md:stream", "alternate stream"),
        ):
            _assert_failure(
                label,
                "traversal or alias",
                validator.validate_target_currentness(root, [alias_target], **_expectations(target)),
            )

        target.write_text(
            target.read_text(encoding="utf-8").replace(
                "Branch: `feature/release-readiness-source-truth-intake`",
                "Branch: `feature/release-readiness-source-truth-intake`\nCurrent Branch: `feature/wrong-alias`",
            ),
            encoding="utf-8",
        )
        _assert_failure(
            "conflicting live aliases",
            "duplicate or conflicting live identity fields",
            _run(root),
        )
        _record(root)

        target.write_text(
            target.read_text(encoding="utf-8").replace(
                "Branch: `feature/release-readiness-source-truth-intake`",
                "Branch: `feature/release-readiness-source-truth-intake`\n"
                "Branch: `feature/release-readiness-source-truth-intake`",
                1,
            ),
            encoding="utf-8",
        )
        _assert_failure(
            "duplicate live identity field",
            "duplicate or conflicting live identity fields",
            _run(root),
        )
        _record(root)

        for field, replacement in (
            (
                "Worktree Path",
                "Worktree Path: `C:\\Nexus Worktrees\\Governance`\n"
                "Worktree Path: `C:\\Nexus Worktrees\\FAM-007`",
            ),
            (
                "Slot ID",
                "Slot ID: `governance-standing`\nSlot ID: `runtime-active-1`",
            ),
        ):
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    f"{field}: `{WORKTREE_PATH if field == 'Worktree Path' else SLOT}`",
                    replacement,
                    1,
                ),
                encoding="utf-8",
            )
            _assert_failure(
                f"duplicate {field}",
                "duplicate or conflicting live identity fields",
                _run(root),
            )
            _record(root)

        _record(root, record_class="Historical Receipt")
        _assert_failure("historical receipt selected as live", "historical receipt", _run(root))
        _record(root)
        target.write_bytes(b"not utf-8: \xff")
        _assert_failure("malformed record", "malformed or unreadable", _run(root))
        _record(root, record_class="Unknown Record")
        _assert_failure("unsupported record class", "unsupported or missing live Record Class", _run(root))
        _record(root)

        original_reparse_check = validator._has_reparse_point
        validator._has_reparse_point = lambda path: path.name == "worktree_state.md"
        try:
            _assert_failure("reparse point", "reparse/symlink escape", _run(root))
        finally:
            validator._has_reparse_point = original_reparse_check

        original_hash = validator.sha256_file
        hash_calls = 0

        def changing_hash(path: Path) -> str:
            nonlocal hash_calls
            hash_calls += 1
            return original_hash(path) if hash_calls == 1 else "0" * 64

        validator.sha256_file = changing_hash
        try:
            _assert_failure("TOCTOU target change", "changed during validation", _run(root))
        finally:
            validator.sha256_file = original_hash

        expected_values = _expectations(target)
        original_read_bytes = Path.read_bytes
        original_bytes = original_read_bytes(target)
        tampered_bytes = original_bytes.replace(
            b"Source Repo HEAD:",
            b"Source Repo HEAD: tampered\nSource Repo HEAD:",
            1,
        )
        validator_read_calls = 0

        def changing_bytes(path: Path) -> bytes:
            nonlocal validator_read_calls
            if path == target:
                validator_read_calls += 1
                return tampered_bytes
            return original_read_bytes(path)

        Path.read_bytes = changing_bytes
        try:
            byte_race_messages = validator.validate_target_currentness(
                root,
                [TARGET],
                **expected_values,
            )
        finally:
            Path.read_bytes = original_read_bytes
        if not any("changed during validation" in item for item in byte_race_messages):
            raise AssertionError(
                "target bytes changed between hash and parse without a TOCTOU failure:\n"
                + "\n".join(byte_race_messages)
            )

    with tempfile.TemporaryDirectory(prefix="ndai-target-writer-") as temp_dir:
        root = Path(temp_dir)
        _manifest(root)
        target = _record(root)
        target.write_text(
            target.read_text(encoding="utf-8")
            + "## Historical Receipts\nSource Repo HEAD: `historical-receipt-head`\n"
            + "## Assigned Worktree Confinement\n"
            + "Intended Write Set: `Only dev/original.py`\n",
            encoding="utf-8",
        )
        snapshot = root / "snapshots" / "fixture-snapshot"
        _snapshot(root, target, snapshot.name)
        lock_id = "worktree-fixture-lock"
        atomic_write_json(
            root / "locks" / f"{lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        expectations = _expectations(target)
        before = target.read_bytes()
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot="snapshots/fixture-snapshot",
            assignments=["Last Updated=2026-01-02T00:00:00Z"],
            additions=["Added Fixture Field=added"],
            section_assignments=[
                "Assigned Worktree Confinement::Intended Write Set=Only dev/updated.py"
            ],
            apply=False,
            **expectations,
        )
        _assert_pass("target writer dry run", [] if ok and audit is None and target.read_bytes() == before else messages)

        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot="snapshots/fixture-snapshot",
            assignments=[],
            additions=[],
            section_assignments=[
                "Assigned Worktree Confinement::Intended Write Set=unsafe\nInjected Field: injected"
            ],
            apply=False,
            **expectations,
        )
        if ok or audit is not None or not any(
            "Invalid --set-section-field assignment" in item for item in messages
        ):
            raise AssertionError(
                "newline section assignment was accepted or mutated the target:\n"
                + "\n".join(messages)
            )

        for label, section_assignments, section_renames, expected_fragment in (
            (
                "case-duplicate section assignment",
                [
                    "Assigned Worktree Confinement::Intended Write Set=Only dev/a.py",
                    "assigned worktree confinement::intended write set=Only dev/b.py",
                ],
                [],
                "Invalid --set-section-field assignment",
            ),
            (
                "section update and rename overlap",
                [
                    "Assigned Worktree Confinement::Intended Write Set=Only dev/a.py",
                ],
                ["assigned worktree confinement=Renamed Confinement"],
                "cannot be renamed and have a field replaced",
            ),
        ):
            ok, messages, audit = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot="snapshots/fixture-snapshot",
                assignments=[],
                additions=[],
                section_assignments=section_assignments,
                section_renames=section_renames,
                apply=False,
                **expectations,
            )
            if ok or audit is not None or not any(
                expected_fragment in item for item in messages
            ):
                raise AssertionError(
                    f"{label} was accepted or mutated the target:\n" + "\n".join(messages)
                )

        normalized_before_text = before.decode("utf-8").replace("\r\n", "\n")
        ambiguous_section_text = normalized_before_text.replace(
            "## Assigned Worktree Confinement\n",
            "## assigned worktree confinement\n"
            "Intended Write Set: `Only dev/duplicate-section.py`\n"
            "## Assigned Worktree Confinement\n",
        )
        _, ambiguous_section_failures = reconciler._replace_existing_section_fields(
            ambiguous_section_text,
            {
                ("Assigned Worktree Confinement", "Intended Write Set"):
                "Only dev/updated.py"
            },
        )
        if not any("exactly one section" in item for item in ambiguous_section_failures):
            raise AssertionError("case-variant duplicate section was not rejected")

        ambiguous_field_text = normalized_before_text.replace(
            "Intended Write Set: `Only dev/original.py`\n",
            "Intended Write Set: `Only dev/original.py`\n"
            "intended write set: `Only dev/duplicate-field.py`\n",
        )
        _, ambiguous_field_failures = reconciler._replace_existing_section_fields(
            ambiguous_field_text,
            {
                ("Assigned Worktree Confinement", "Intended Write Set"):
                "Only dev/updated.py"
            },
        )
        if not any("inside section" in item for item in ambiguous_field_failures):
            raise AssertionError("case-variant duplicate section field was not rejected")

        fenced_only_section_text = normalized_before_text.replace(
            "Intended Write Set: `Only dev/original.py`\n",
            "```text\n"
            "Intended Write Set: `Only dev/example.py`\n"
            "```\n",
        )
        fenced_only_result, fenced_only_failures = reconciler._replace_existing_section_fields(
            fenced_only_section_text,
            {
                ("Assigned Worktree Confinement", "Intended Write Set"):
                "Only dev/updated.py"
            },
        )
        if (
            fenced_only_result != fenced_only_section_text
            or not any("inside section" in item for item in fenced_only_failures)
        ):
            raise AssertionError("a fenced section-field example was treated as live authority")

        real_and_fenced_section_text = normalized_before_text.replace(
            "Intended Write Set: `Only dev/original.py`\n",
            "Intended Write Set: `Only dev/original.py`\n"
            "~~~text\n"
            "Intended Write Set: `Only dev/example.py`\n"
            "~~~~\n",
        )
        real_and_fenced_result, real_and_fenced_failures = (
            reconciler._replace_existing_section_fields(
                real_and_fenced_section_text,
                {
                    ("Assigned Worktree Confinement", "Intended Write Set"):
                    "Only dev/updated.py"
                },
            )
        )
        if real_and_fenced_failures:
            raise AssertionError(
                "a real section field plus a fenced example was rejected:\n"
                + "\n".join(real_and_fenced_failures)
            )
        if (
            "Intended Write Set: `Only dev/updated.py`" not in real_and_fenced_result
            or "Intended Write Set: `Only dev/example.py`" not in real_and_fenced_result
            or real_and_fenced_result.count("Only dev/updated.py") != 1
        ):
            raise AssertionError("section-field replacement changed or selected fenced example text")

        fenced_duplicate_heading_text = normalized_before_text.replace(
            "## Assigned Worktree Confinement\n",
            "```markdown\n"
            "## Assigned Worktree Confinement\n"
            "Intended Write Set: `Only dev/example.py`\n"
            "```\n"
            "## Assigned Worktree Confinement\n",
            1,
        )
        _, fenced_duplicate_heading_failures = reconciler._replace_existing_section_fields(
            fenced_duplicate_heading_text,
            {
                ("Assigned Worktree Confinement", "Intended Write Set"):
                "Only dev/updated.py"
            },
        )
        if fenced_duplicate_heading_failures:
            raise AssertionError(
                "a fenced duplicate heading changed live section cardinality:\n"
                + "\n".join(fenced_duplicate_heading_failures)
            )

        fenced_only_top_field = normalized_before_text.replace(
            "Last Updated: `2026-01-01T00:00:00Z`\n",
            "```text\n"
            "Last Updated: `2026-01-01T00:00:00Z`\n"
            "```\n",
            1,
        )
        fenced_top_result, fenced_top_failures = reconciler._replace_existing_fields(
            fenced_only_top_field,
            {"Last Updated": "2026-01-02T00:00:00Z"},
            {},
        )
        if (
            fenced_top_result != fenced_only_top_field
            or not any("exactly one existing field" in item for item in fenced_top_failures)
        ):
            raise AssertionError("a fenced top-level field example was treated as live authority")

        fenced_rename_text = normalized_before_text.replace(
            "## Historical Receipts\n",
            "```markdown\n## Historical Receipts\n```\n## Historical Receipts\n",
            1,
        )
        fenced_rename_result, fenced_rename_failures, fenced_renamed = reconciler._rename_sections(
            fenced_rename_text,
            {"Historical Receipts": "Historical Receipt"},
        )
        if fenced_rename_failures or fenced_renamed != [
            ("## Historical Receipts", "## Historical Receipt")
        ]:
            raise AssertionError(
                "a fenced rename example changed live heading selection:\n"
                + "\n".join(fenced_rename_failures)
            )
        if fenced_rename_result.count("## Historical Receipts") != 1:
            raise AssertionError("a fenced heading example was renamed")

        case_collision_result, case_collision_failures, case_collision_renamed = (
            reconciler._rename_sections(
                normalized_before_text,
                {"Assigned Worktree Confinement": "historical receipts"},
            )
        )
        if (
            case_collision_result != normalized_before_text
            or case_collision_renamed
            or not any("destination already exists" in item for item in case_collision_failures)
        ):
            raise AssertionError("a case-variant section rename destination collision was accepted")

        case_source_result, case_source_failures, case_source_renamed = (
            reconciler._rename_sections(
                normalized_before_text,
                {"historical receipts": "Historical Archive"},
            )
        )
        if case_source_failures or case_source_renamed != [
            ("## historical receipts", "## Historical Archive")
        ] or "## Historical Archive\n" not in case_source_result:
            raise AssertionError(
                "a unique case-variant section source was not renamed deterministically:\n"
                + "\n".join(case_source_failures)
            )

        fenced_destination_text = normalized_before_text.replace(
            "## Historical Receipts\n",
            "```markdown\n## Historical Archive\n```\n## Historical Receipts\n",
            1,
        )
        fenced_destination_result, fenced_destination_failures, fenced_destination_renamed = (
            reconciler._rename_sections(
                fenced_destination_text,
                {"Historical Receipts": "historical archive"},
            )
        )
        if fenced_destination_failures or fenced_destination_renamed != [
            ("## Historical Receipts", "## historical archive")
        ]:
            raise AssertionError(
                "a fenced rename destination was treated as a live collision:\n"
                + "\n".join(fenced_destination_failures)
            )
        if fenced_destination_result.count("## Historical Archive") != 1:
            raise AssertionError("a fenced rename destination example was modified")

        for label, unterminated_text in (
            (
                "backtick",
                normalized_before_text
                + "```text\nIntended Write Set: `Only dev/example.py`\n",
            ),
            (
                "tilde",
                normalized_before_text
                + "~~~text\nIntended Write Set: `Only dev/example.py`\n",
            ),
        ):
            _, unterminated_section_failures = reconciler._replace_existing_section_fields(
                unterminated_text,
                {
                    ("Assigned Worktree Confinement", "Intended Write Set"):
                    "Only dev/updated.py"
                },
            )
            _, unterminated_top_failures = reconciler._replace_existing_fields(
                unterminated_text,
                {"Last Updated": "2026-01-02T00:00:00Z"},
                {},
            )
            _, unterminated_rename_failures, _ = reconciler._rename_sections(
                unterminated_text,
                {"Historical Receipts": "Historical Receipt"},
            )
            for operation, failures in (
                ("section field", unterminated_section_failures),
                ("top-level field", unterminated_top_failures),
                ("section rename", unterminated_rename_failures),
            ):
                if not any("unterminated fenced block" in item for item in failures):
                    raise AssertionError(
                        f"unterminated {label} fence did not block {operation} mutation"
                    )

        for label, assignments, additions in (
            (
                "newline assignment",
                ["Last Updated=2026-01-02T00:00:00Z\nInjected Field: injected"],
                [],
            ),
            (
                "newline addition",
                [],
                ["Added Fixture Field=added\nInjected Field: injected"],
            ),
        ):
            ok, messages, audit = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot="snapshots/fixture-snapshot",
                assignments=assignments,
                additions=additions,
                apply=False,
                **expectations,
            )
            if ok or audit is not None or not any(
                "Invalid --set-field assignment" in item for item in messages
            ):
                raise AssertionError(
                    f"{label} was accepted or mutated the target:\n" + "\n".join(messages)
                )

        mismatched_lock_id = "worktree-fixture-mismatched-payload"
        atomic_write_json(
            root / "locks" / f"{mismatched_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": "different-lock-id",
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        mismatch_ok, mismatch_messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=mismatched_lock_id,
            snapshot="snapshots/fixture-snapshot",
            assignments=["Last Updated=2026-01-02T00:00:01Z"],
            additions=[],
            apply=False,
            **expectations,
        )
        if mismatch_ok or not any("Lock payload ID mismatch" in item for item in mismatch_messages):
            raise AssertionError("target writer accepted a mismatched lock payload ID:\n" + "\n".join(mismatch_messages))

        label_lock_id = "worktree-fixture-label-lock"
        atomic_write_json(
            root / "locks" / f"{label_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": label_lock_id,
                "Lock State": "Locked",
                "Worktree": "Governance",
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        label_snapshot = _snapshot(root, target, "fixture-label-lock")
        label_expectations = _expectations(target)
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=label_lock_id,
            snapshot=label_snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-02T00:00:00Z"],
            additions=[],
            apply=False,
            **label_expectations,
        )
        if not ok or audit is not None or target.read_bytes() != before:
            raise AssertionError("label-style worktree lock was rejected or mutated the target:\n" + "\n".join(messages))

        add_only_snapshot = _snapshot(root, target, "fixture-add-only")
        add_only_expectations = _expectations(target)
        add_only_before = target.read_bytes()
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=add_only_snapshot.relative_to(root).as_posix(),
            assignments=[],
            additions=["Add Only Fixture Field=added"],
            apply=False,
            **add_only_expectations,
        )
        if not ok or audit is not None or target.read_bytes() != add_only_before:
            raise AssertionError("add-only target writer dry run was rejected or mutated the target:\n" + "\n".join(messages))

        dry_run_head = "d" * 40
        dry_run_snapshot = _snapshot(root, target, "fixture-dry-run-head-transition")
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=dry_run_snapshot.relative_to(root).as_posix(),
            assignments=[f"Source Repo HEAD={dry_run_head}"],
            additions=[],
            apply=False,
            post_expected_source_head=dry_run_head,
            **expectations,
        )
        if not ok or audit is not None or target.read_bytes() != before:
            raise AssertionError(
                "target writer dry run did not validate the projected post-state:\n"
                + "\n".join(messages)
            )

        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=dry_run_snapshot.relative_to(root).as_posix(),
            assignments=[f"Source Repo HEAD={dry_run_head}"],
            additions=[],
            apply=False,
            post_expected_source_head="f" * 40,
            **expectations,
        )
        if ok or audit is not None or target.read_bytes() != before or not any(
            "Projected post-write target validation" in item for item in messages
        ):
            raise AssertionError(
                "target writer dry run accepted a mismatched projected post-state:\n"
                + "\n".join(messages)
            )

        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot="snapshots/fixture-snapshot",
            assignments=["Last Updated=2026-01-02T00:00:00Z"],
            additions=["Added Fixture Field=added"],
            section_assignments=[
                "Assigned Worktree Confinement::Intended Write Set=Only dev/updated.py"
            ],
            apply=True,
            section_renames=["Historical Receipts=Historical Receipt"],
            **expectations,
        )
        if not ok or audit is None or not list((root / "audit_log").glob("target-currentness-*.json")):
            raise AssertionError("target writer apply did not produce an audited transition:\n" + "\n".join(messages))
        if "2026-01-02T00:00:00Z" not in target.read_text(encoding="utf-8"):
            raise AssertionError("target writer apply reported success without changing the requested field")
        audit_payload = json.loads(audit.read_text(encoding="utf-8"))
        if "Added Fixture Field" not in audit_payload["Changed Fields"]:
            raise AssertionError("target writer audit omitted an added field")
        section_field = "Assigned Worktree Confinement::Intended Write Set"
        if section_field not in audit_payload["Changed Fields"]:
            raise AssertionError("target writer audit omitted a replaced section field")
        section_detail = next(
            item
            for item in audit_payload["Changed Field Details"]
            if item["Field"] == section_field
        )
        if section_detail != {
            "Field": section_field,
            "Before": "Only dev/original.py",
            "After": "Only dev/updated.py",
        }:
            raise AssertionError("target writer audit lost section-field before/after identity")
        added_detail = next(
            item
            for item in audit_payload["Changed Field Details"]
            if item["Field"] == "Added Fixture Field"
        )
        if added_detail["Before"] != "MISSING":
            raise AssertionError("target writer audit did not preserve MISSING before-state for an added field")
        if "historical-receipt-head" not in target.read_text(encoding="utf-8"):
            raise AssertionError("target writer changed a historical receipt while updating the live header")
        if "## Historical Receipt\n" not in target.read_text(encoding="utf-8"):
            raise AssertionError("target writer did not apply the audited historical-section rename")
        if audit_payload.get("Renamed Sections") != [
            {"Before": "## Historical Receipts", "After": "## Historical Receipt"}
        ]:
            raise AssertionError("target writer audit omitted the section rename")

        target.write_text(
            target.read_text(encoding="utf-8") + "\n## Rename Me\nfixture section\n",
            encoding="utf-8",
        )
        rename_only_snapshot = _snapshot(root, target, "fixture-rename-only")
        rename_only_expectations = _expectations(target)
        rename_only_before = target.read_bytes()
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=rename_only_snapshot.relative_to(root).as_posix(),
            assignments=[],
            additions=[],
            section_renames=["Rename Me=Renamed"],
            apply=False,
            **rename_only_expectations,
        )
        if not ok or audit is not None or target.read_bytes() != rename_only_before:
            raise AssertionError("rename-only target writer dry run was rejected or mutated the target:\n" + "\n".join(messages))

        collision_snapshot = _snapshot(root, target, "fixture-rename-collision")
        collision_before = target.read_bytes()
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=collision_snapshot.relative_to(root).as_posix(),
            assignments=[],
            additions=[],
            section_renames=["Rename Me=Historical Receipt"],
            apply=False,
            **_expectations(target),
        )
        if ok or audit is not None or target.read_bytes() != collision_before or not any(
            "section rename destination already exists" in item for item in messages
        ):
            raise AssertionError(
                "section rename collision was accepted or mutated the target:\n"
                + "\n".join(messages)
            )

        historical_only_field = "Historical-Only Fixture Field"
        target.write_text(
            target.read_text(encoding="utf-8")
            + f"\n## Historical Receipt\n{historical_only_field}: `historical-value`\n",
            encoding="utf-8",
        )
        historical_lock_id = "worktree-fixture-historical-field"
        atomic_write_json(
            root / "locks" / f"{historical_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": historical_lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        historical_snapshot = _snapshot(root, target, "fixture-historical-only-field")
        historical_expectations = _expectations(target)
        historical_expectations["expected_source_head"] = HEAD
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=historical_lock_id,
            snapshot=historical_snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-02T00:00:01Z"],
            additions=[f"{historical_only_field}=new-live-value"],
            apply=True,
            **historical_expectations,
        )
        if not ok or audit is None:
            raise AssertionError("target writer could not add a field shadowed only by historical state:\n" + "\n".join(messages))
        historical_payload = json.loads(audit.read_text(encoding="utf-8"))
        historical_detail = next(
            item for item in historical_payload["Changed Field Details"]
            if item["Field"] == historical_only_field
        )
        if historical_detail["Before"] != "MISSING" or historical_detail["After"] != "new-live-value":
            raise AssertionError("target writer audit treated a historical field as live state")

        negative_cases = [
            (
                "missing snapshot target",
                _snapshot(root, target, "fixture-missing-target", include_target=False),
                "snapshot does not contain target",
            ),
            (
                "wrong snapshot target hash",
                _snapshot(root, target, "fixture-wrong-target-hash", snapshot_bytes=b"wrong snapshot bytes"),
                "snapshot target hash mismatch",
            ),
            (
                "snapshot from another root",
                _snapshot(root, target, "fixture-wrong-root", manifest_root=str(root / "other-root")),
                "snapshot root mismatch",
            ),
        ]
        if os.path.normcase(os.path.normpath(str(root))) == os.path.normpath(str(root)):
            case_snapshot = _snapshot(
                root,
                target,
                "fixture-case-sensitive-root",
                manifest_root=str(root).swapcase(),
            )
            case_expectations = _expectations(target)
            ok, case_messages, _ = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot=case_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-05T00:00:01Z"],
                additions=[],
                apply=False,
                **case_expectations,
            )
            if ok or not any("snapshot root mismatch" in item for item in case_messages):
                raise AssertionError(
                    "case-sensitive snapshot root mismatch was accepted:\n"
                    + "\n".join(case_messages)
                )
        for label, invalid_snapshot, needle in negative_cases:
            invalid_expectations = _expectations(target)
            ok, invalid_messages, _ = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot=invalid_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-05T00:00:00Z"],
                additions=[],
                apply=False,
                **invalid_expectations,
            )
            if ok or not any(needle in item for item in invalid_messages):
                raise AssertionError(f"{label} was accepted:\n" + "\n".join(invalid_messages))

        prefix_lock_id = "worktree-fixture-prefix-write-set"
        atomic_write_json(
            root / "locks" / f"{prefix_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": prefix_lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": f"{TARGET}.backup",
            },
        )
        prefix_snapshot = _snapshot(root, target, "fixture-prefix-write-set")
        prefix_ok, prefix_messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=prefix_lock_id,
            snapshot=prefix_snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-08T00:00:02Z"],
            additions=[],
            apply=False,
            **_expectations(target),
        )
        if prefix_ok or not any("Lock write set does not admit target projection" in item for item in prefix_messages):
            raise AssertionError("a longer write-set prefix was incorrectly accepted:\n" + "\n".join(prefix_messages))

        future_snapshot = _snapshot(root, target, "fixture-future-snapshot")
        future_time = time.time() + 60
        os.utime(future_snapshot / "snapshot_manifest.json", (future_time, future_time))
        future_expectations = _expectations(target)
        ok, future_messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=future_snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-06T00:00:00Z"],
            additions=[],
            apply=False,
            **future_expectations,
        )
        if ok or not any("snapshot was created after the transition began" in item for item in future_messages):
            raise AssertionError("future snapshot was accepted:\n" + "\n".join(future_messages))

        late_target_snapshot = _snapshot(root, target, "fixture-late-target")
        os.utime(_target_path(late_target_snapshot), (future_time, future_time))
        late_target_expectations = _expectations(target)
        ok, late_target_messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=late_target_snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-06T00:00:00Z"],
            additions=[],
            apply=False,
            **late_target_expectations,
        )
        if ok or not any("snapshot target was created after the transition began" in item for item in late_target_messages):
            raise AssertionError(
                "late-created snapshot target was accepted:\n"
                + "\n".join(late_target_messages)
            )

        reparse_snapshot = _snapshot(root, target, "fixture-reparse-snapshot")
        reparse_target = _target_path(reparse_snapshot)
        original_reparse_hook = reconciler._has_reparse_point
        reconciler._has_reparse_point = lambda path: path == reparse_target
        try:
            ok, reparse_messages, _ = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot=reparse_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-06T00:00:01Z"],
                additions=[],
                apply=False,
                **_expectations(target),
            )
        finally:
            reconciler._has_reparse_point = original_reparse_hook
        if ok or not any("reparse/symlink target is forbidden" in item for item in reparse_messages):
            raise AssertionError("reparse/symlink snapshot target was accepted:\n" + "\n".join(reparse_messages))

        intermediate_snapshot = _snapshot(root, target, "fixture-intermediate-reparse/nested")
        intermediate_parent = intermediate_snapshot.parent
        original_reparse_hook = reconciler._has_reparse_point
        reconciler._has_reparse_point = lambda path: path == intermediate_parent
        try:
            ok, intermediate_messages, _ = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot=intermediate_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-06T00:00:02Z"],
                additions=[],
                apply=False,
                **_expectations(target),
            )
        finally:
            reconciler._has_reparse_point = original_reparse_hook
        if ok or not any("must not traverse a reparse/symlink component" in item for item in intermediate_messages):
            raise AssertionError(
                "intermediate reparse snapshot parent was accepted:\n"
                + "\n".join(intermediate_messages)
            )

        nested_snapshot = _snapshot(root, target, "fixture-nested-reparse")
        nested_reparse_component = _target_path(nested_snapshot).parent
        original_reparse_hook = reconciler._has_reparse_point
        reconciler._has_reparse_point = lambda path: path == nested_reparse_component
        try:
            ok, nested_messages, _ = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot=nested_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-06T00:00:03Z"],
                additions=[],
                apply=False,
                **_expectations(target),
            )
        finally:
            reconciler._has_reparse_point = original_reparse_hook
        if ok or not any("reparse/symlink target is forbidden" in item for item in nested_messages):
            raise AssertionError(
                "nested reparse snapshot component was accepted:\n"
                + "\n".join(nested_messages)
            )

        valid_alias_snapshot = _snapshot(root, target, "fixture-snapshot-alias")
        for alias in ("snapshots//fixture-snapshot-alias", "snapshots\\fixture-snapshot-alias\\"):
            alias_expectations = _expectations(target)
            ok, alias_messages, _ = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_id,
                snapshot=alias,
                assignments=["Last Updated=2026-01-07T00:00:00Z"],
                additions=[],
                apply=False,
                **alias_expectations,
            )
            if ok or not any("Snapshot path must remain relative" in item for item in alias_messages):
                raise AssertionError(f"snapshot path alias was accepted ({alias}):\n" + "\n".join(alias_messages))

        backslash_snapshot = _snapshot(root, target, "fixture-backslash-path")
        backslash_snapshot_name = backslash_snapshot.relative_to(root).as_posix().replace("/", "\\")
        backslash_expectations = _expectations(target)
        ok, backslash_messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=backslash_snapshot_name,
            assignments=["Last Updated=2026-01-07T00:00:01Z"],
            additions=[],
            apply=False,
            **backslash_expectations,
        )
        if not ok:
            raise AssertionError(
                "valid backslash-form snapshot path was rejected:\n"
                + "\n".join(backslash_messages)
            )

        rollback_lock_id = "worktree-fixture-rollback"
        atomic_write_json(
            root / "locks" / f"{rollback_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": rollback_lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        rollback_snapshot = _snapshot(root, target, "fixture-rollback")
        rollback_before = target.read_bytes()
        rollback_expectations = _expectations(target)
        rollback_expectations["expected_source_head"] = HEAD
        ok, rollback_messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=rollback_lock_id,
            snapshot=rollback_snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-08T00:00:00Z"],
            additions=[],
            apply=True,
            post_expected_source_head="f" * 40,
            **rollback_expectations,
        )
        if ok or audit is not None or target.read_bytes() != rollback_before or not any("Post-write target validation" in item for item in rollback_messages):
            raise AssertionError("post-write validation failure did not roll back without audit:\n" + "\n".join(rollback_messages))
        released, release_messages = lock_release.release_lock(
            root, lock_id, "fixture transition complete", apply=True
        )
        if not released or json.loads((root / "locks" / f"{lock_id}.json").read_text(encoding="utf-8"))["Lock State"] != "Released":
            raise AssertionError("lock release fixture failed:\n" + "\n".join(release_messages))

        release_mismatch_id = "worktree-fixture-release-mismatched-payload"
        atomic_write_json(
            root / "locks" / f"{release_mismatch_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": "different-release-lock-id",
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        released, release_messages = lock_release.release_lock(
            root, release_mismatch_id, "fixture mismatched payload", apply=False
        )
        if released or not any("Lock payload ID mismatch" in item for item in release_messages):
            raise AssertionError("lock release accepted a mismatched payload ID:\n" + "\n".join(release_messages))

        release_race_id = "worktree-fixture-release-race"
        atomic_write_json(
            root / "locks" / f"{release_race_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": release_race_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        original_release_hook = lock_release._before_release_atomic_replacement

        def mutate_lock_before_release(lock_path: Path, _expected_bytes: bytes) -> None:
            payload = json.loads(lock_path.read_text(encoding="utf-8"))
            payload["Intended Write Set"] = "worktrees/Other/other_state.md"
            atomic_write_json(lock_path, payload)

        lock_release._before_release_atomic_replacement = mutate_lock_before_release
        try:
            released, release_messages = lock_release.release_lock(
                root, release_race_id, "fixture release race", apply=True
            )
        finally:
            lock_release._before_release_atomic_replacement = original_release_hook
        release_race_payload = json.loads(
            (root / "locks" / f"{release_race_id}.json").read_text(encoding="utf-8")
        )
        if released or release_race_payload.get("Lock State") != "Locked" or not any(
            "Lock changed during release validation" in item for item in release_messages
        ):
            raise AssertionError(
                "lock release accepted an intervening lock edit:\n"
                + "\n".join(release_messages)
            )

        transition_lock_id = "worktree-fixture-head-transition"
        atomic_write_json(
            root / "locks" / f"{transition_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": transition_lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        new_head = "d" * 40
        transition_snapshot = _snapshot(root, target, "fixture-head-transition-snapshot")
        ok, messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=transition_lock_id,
            snapshot=transition_snapshot.relative_to(root).as_posix(),
            assignments=[f"Source Repo HEAD={new_head}"],
            additions=[],
            apply=True,
            post_expected_source_head=new_head,
            **_expectations(target),
        )
        if not ok or new_head not in target.read_text(encoding="utf-8"):
            raise AssertionError("target writer did not prove an atomic head transition:\n" + "\n".join(messages))
        released, release_messages = lock_release.release_lock(
            root, transition_lock_id, "fixture head transition complete", apply=True
        )
        if not released:
            raise AssertionError("head-transition lock release fixture failed:\n" + "\n".join(release_messages))

        adversarial_lock_id = "worktree-fixture-adversarial"
        atomic_write_json(
            root / "locks" / f"{adversarial_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": adversarial_lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        adversarial_snapshot = _snapshot(root, target, "fixture-adversarial-snapshot")
        original_hook = reconciler._before_atomic_replacement_check

        def mutate_before_final_reread(path: Path, _expected_hash: str) -> None:
            path.write_text(path.read_text(encoding="utf-8") + "intervening edit\n", encoding="utf-8")

        reconciler._before_atomic_replacement_check = mutate_before_final_reread
        try:
            adversarial_expectations = _expectations(target)
            adversarial_expectations["expected_source_head"] = "d" * 40
            ok, messages, audit = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=adversarial_lock_id,
                snapshot=adversarial_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-04T00:00:00Z"],
                additions=[],
                apply=True,
                **adversarial_expectations,
            )
        finally:
            reconciler._before_atomic_replacement_check = original_hook
        if ok or audit is not None or not any("changed between validation and atomic replacement" in item for item in messages):
            raise AssertionError("target writer accepted an intervening target edit: " + " | ".join(messages))

        lock_race_id = "worktree-fixture-lock-race"
        atomic_write_json(
            root / "locks" / f"{lock_race_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_race_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        lock_race_snapshot = _snapshot(root, target, "fixture-lock-race")
        lock_race_before = target.read_bytes()
        original_lock_hook = reconciler._before_final_lock_check

        def release_lock_before_final_check(lock_root: Path, lock_name: str) -> None:
            lock_path = lock_root / "locks" / f"{lock_name}.json"
            payload = json.loads(lock_path.read_text(encoding="utf-8"))
            payload["Lock State"] = "Released"
            atomic_write_json(lock_path, payload)

        reconciler._before_final_lock_check = release_lock_before_final_check
        try:
            lock_race_expectations = _expectations(target)
            lock_race_expectations["expected_source_head"] = "d" * 40
            ok, messages, audit = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=lock_race_id,
                snapshot=lock_race_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-04T00:00:01Z"],
                additions=[],
                apply=True,
                **lock_race_expectations,
            )
        finally:
            reconciler._before_final_lock_check = original_lock_hook
        if ok or audit is not None or target.read_bytes() != lock_race_before or not any(
            "Final lock validation" in item for item in messages
        ):
            raise AssertionError(
                "target writer accepted a lock change before atomic replacement:\n"
                + "\n".join(messages)
            )

        snapshot_race_id = "worktree-fixture-snapshot-race"
        atomic_write_json(
            root / "locks" / f"{snapshot_race_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": snapshot_race_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        snapshot_race_snapshot = _snapshot(root, target, "fixture-snapshot-race")
        snapshot_race_before = target.read_bytes()
        original_snapshot_hook = reconciler._before_final_snapshot_check

        def corrupt_snapshot_before_final_check(snapshot_path: Path) -> None:
            (snapshot_path / "snapshot_manifest.json").write_text("{}", encoding="utf-8")

        reconciler._before_final_snapshot_check = corrupt_snapshot_before_final_check
        try:
            snapshot_race_expectations = _expectations(target)
            snapshot_race_expectations["expected_source_head"] = "d" * 40
            ok, messages, audit = reconciler.reconcile_target(
                root=root,
                target=TARGET,
                lock_id=snapshot_race_id,
                snapshot=snapshot_race_snapshot.relative_to(root).as_posix(),
                assignments=["Last Updated=2026-01-04T00:00:02Z"],
                additions=[],
                apply=True,
                **snapshot_race_expectations,
            )
        finally:
            reconciler._before_final_snapshot_check = original_snapshot_hook
        if ok or audit is not None or target.read_bytes() != snapshot_race_before or not any(
            "Final snapshot validation" in item for item in messages
        ):
            raise AssertionError(
                "target writer accepted an intervening snapshot edit:\n"
                + "\n".join(messages)
            )

        missing_lock_ok, missing_lock_messages, _ = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id="missing-lock",
            snapshot="snapshots/fixture-snapshot",
            assignments=["Last Updated=2026-01-03T00:00:00Z"],
            additions=[],
            apply=False,
            **_expectations(target),
        )
        if missing_lock_ok or not any("Required lock is missing" in item for item in missing_lock_messages):
            raise AssertionError("target writer did not reject a missing lock")

        missing_root = root / "missing-external-state-root"
        cli_result = subprocess.run(
            [
                sys.executable,
                str(Path(validator.__file__).resolve()),
                "--root",
                str(missing_root),
                "--target-currentness",
                "--target",
                TARGET,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if cli_result.returncode == 0 or "Clean Clone Boundary: BLOCKED" not in cli_result.stdout:
            raise AssertionError(
                "target-currentness CLI accepted a missing external-state root:\n"
                + cli_result.stdout
                + cli_result.stderr
            )

        uninitialized_root = root / "uninitialized-external-state-root"
        _record(uninitialized_root)
        cli_result = subprocess.run(
            [
                sys.executable,
                str(Path(validator.__file__).resolve()),
                "--root",
                str(uninitialized_root),
                "--target-currentness",
                "--target",
                TARGET,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if cli_result.returncode == 0 or "state_manifest.json missing" not in cli_result.stdout:
            raise AssertionError(
                "target-currentness CLI accepted an uninitialized external-state root:\n"
                + cli_result.stdout
                + cli_result.stderr
            )

    with tempfile.TemporaryDirectory(prefix="ndai-target-crlf-") as temp_dir:
        root = Path(temp_dir)
        _manifest(root)
        target = _record(root)
        crlf_bytes = target.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        target.write_bytes(crlf_bytes.replace(b"\n", b"\r\n"))
        with target.open("ab") as handle:
            handle.write(b"## CRLF Historical Receipts\r\nSource Repo HEAD: `crlf-history`\r\n")
        before_bytes = target.read_bytes()
        snapshot = _snapshot(root, target, "fixture-crlf")
        lock_id = "worktree-fixture-crlf"
        atomic_write_json(
            root / "locks" / f"{lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        with target.open("r", encoding="utf-8", newline="") as handle:
            before_text = handle.read()
        projected_text, projected_failures = reconciler._replace_existing_fields(
            before_text,
            {"Last Updated": "2026-01-02T00:00:00Z"},
            {"Added CRLF Fixture Field": "added"},
        )
        projected_text, section_failures, _ = reconciler._rename_sections(
            projected_text,
            {"CRLF Historical Receipts": "CRLF Historical Receipt"},
        )
        if projected_failures or section_failures:
            raise AssertionError(
                "CRLF projection fixture could not construct expected bytes:\n"
                + "\n".join(projected_failures + section_failures)
            )
        projected_hash = hashlib.sha256(projected_text.encode("utf-8")).hexdigest()
        dry_ok, dry_messages, dry_audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-02T00:00:00Z"],
            additions=["Added CRLF Fixture Field=added"],
            apply=False,
            section_renames=["CRLF Historical Receipts=CRLF Historical Receipt"],
            **_expectations(target),
        )
        if not dry_ok or dry_audit is not None or f"After SHA256: {projected_hash}" not in dry_messages:
            raise AssertionError(
                "CRLF dry-run did not report the exact projected byte hash:\n"
                + "\n".join(dry_messages)
            )
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=snapshot.relative_to(root).as_posix(),
            assignments=["Last Updated=2026-01-02T00:00:00Z"],
            additions=["Added CRLF Fixture Field=added"],
            apply=True,
            section_renames=["CRLF Historical Receipts=CRLF Historical Receipt"],
            **_expectations(target),
        )
        after_bytes = target.read_bytes()
        if not ok or audit is None:
            raise AssertionError("CRLF target transition was rejected:\n" + "\n".join(messages))
        if b"2026-01-02T00:00:00Z" not in after_bytes:
            raise AssertionError("CRLF target transition did not update the selected field")
        if b"\n" in after_bytes.replace(b"\r\n", b""):
            raise AssertionError("CRLF target transition introduced a lone LF newline")
        if after_bytes.count(b"\r\n") != before_bytes.count(b"\r\n") + 1:
            raise AssertionError("CRLF target transition changed untouched newline structure")

    _run_legacy_journal_compatibility_fixtures()
    print("Target-scoped external-state currentness fixture validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
