"""Adversarial fixtures for target-scoped external-state currentness."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
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
                    else [
                        "External State Item Status=Complete",
                        "Current Validation State=PASS",
                    ]
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


def _write_modern_journal_fixture(
    root: Path,
    *,
    filename: str = "modern-journal.json",
    state: object = "Committed",
    include_state: bool = True,
    last_updated: str = "2026-07-28T00:00:00Z",
    schema: str = "external-state-v1",
) -> Path:
    path = root / "audit_log" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "External State Schema": schema,
        "Transition": validator.TARGET_SET_TRANSITION,
        "Lock ID": "branch-modern-fixture",
        "Workload ID": "modern-fixture-workload",
        "Snapshot": "snapshots/modern-fixture",
        "Targets": [
            {
                "Target": "worktrees/Fixture/worktree_state.md",
                "Before SHA256": "a" * 64,
                "After SHA256": "b" * 64,
            }
        ],
        "Last Updated": last_updated,
        "Last Updated By": "fixture",
    }
    if include_state:
        payload["Transaction State"] = state
    atomic_write_json(path, payload)
    return path


def _run_journal_case(
    name: str,
    setup: object,
    *,
    should_pass: bool,
) -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-legacy-journal-") as temp_dir:
        root = Path(temp_dir)
        setup(root)  # type: ignore[operator]
        failures = validator.validate_incomplete_target_set_journals(root)
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
) -> None:
    with tempfile.TemporaryDirectory(prefix="ndai-legacy-mutation-") as temp_dir:
        root = Path(temp_dir)
        setup(root)  # type: ignore[operator]
        baseline = validator.validate_incomplete_target_set_journals(root)
        if not baseline:
            raise AssertionError(f"mutation {name} has no failing baseline")
        original = getattr(validator, attribute)
        setattr(validator, attribute, replacement)
        try:
            mutated = validator.validate_incomplete_target_set_journals(root)
        finally:
            setattr(validator, attribute, original)
        if mutated:
            raise AssertionError(
                f"mutation {name} survived the focused suite:\n" + "\n".join(mutated)
            )
    print(f"Legacy journal mutation: {name}: KILLED")


def _run_legacy_journal_compatibility_fixtures() -> None:
    complete = [
        "External State Item Status=Complete",
        "Current Validation State=PASS",
    ]
    complete_with_final = [*complete, "Final Disposition=Complete"]
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
        (
            "every target row carries canonical completion",
            lambda root: _write_legacy_completion_matrix_fixture(root, [complete] * 3),
        ),
        (
            "multiple accepted completion fields agree",
            lambda root: _write_legacy_completion_matrix_fixture(
                root,
                [complete_with_final] * 3,
            ),
        ),
        ("modern Committed journal", lambda root: _write_modern_journal_fixture(root)),
        (
            "unrelated historical audit",
            lambda root: atomic_write_json(
                root / "audit_log" / "unrelated.json",
                {"External State Schema": "external-state-v1", "Transition": "Other audit"},
            ),
        ),
        (
            "legacy receipt with modern-looking filename",
            lambda root: _write_legacy_journal_fixture(root, filename="current-journal.json"),
        ),
    ]
    for name, setup in positive_cases:
        _run_journal_case(name, setup, should_pass=True)

    negative_cases = [
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
            "modern journal invalid schema",
            lambda root: _write_modern_journal_fixture(root, schema="external-state-v0"),
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
            "legacy-looking receipt with recovery payload",
            lambda root: _write_legacy_journal_fixture(root, recovery_payload=True),
        ),
        (
            "legacy receipt with active lock evidence",
            lambda root: _write_legacy_journal_fixture(root, lock_state="Locked"),
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
        _run_journal_case(name, setup, should_pass=False)

    negative_setups = dict(negative_cases)
    accept_missing_state = lambda *_args, **_kwargs: []
    accept_modern_state = lambda _payload: []
    accept_completion_set = lambda _rows: []
    accept_completion_profile = lambda _values: "mutated-complete"
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
        "malformed state ignored",
        negative_setups["modern journal unknown Transaction State"],
        "_validate_modern_target_set_journal",
        accept_modern_state,
    )
    _assert_journal_mutation_killed(
        "active-lock evidence ignored",
        negative_setups["legacy receipt with active lock evidence"],
        "_validate_legacy_lock_evidence",
        lambda *_args, **_kwargs: [],
    )
    _assert_journal_mutation_killed(
        "any one completed row greens the target set",
        negative_setups["only one target row has completion evidence"],
        "_validate_legacy_completion_evidence",
        accept_completion_set,
    )
    _assert_journal_mutation_killed(
        "missing row-level completion ignored",
        negative_setups["one target row has no completion disposition"],
        "_validate_legacy_completion_evidence",
        accept_completion_set,
    )
    _assert_journal_mutation_killed(
        "contradictory completion fields ignored",
        negative_setups["contradictory completion fields in one row"],
        "_legacy_completion_profile",
        accept_completion_profile,
    )
    _assert_journal_mutation_killed(
        "any occurrence of pass accepted",
        negative_setups["completion phrase rejected: pending pass"],
        "_legacy_completion_profile",
        accept_completion_profile,
    )
    _assert_journal_mutation_killed(
        "any occurrence of complete accepted",
        negative_setups["completion phrase rejected: will complete after review"],
        "_legacy_completion_profile",
        accept_completion_profile,
    )
    _assert_journal_mutation_killed(
        "negation checked only immediately before positive word",
        negative_setups["completion phrase rejected: not yet complete"],
        "_legacy_completion_profile",
        accept_completion_profile,
    )
    _assert_journal_mutation_killed(
        "pending future conditional wording accepted",
        negative_setups["completion phrase rejected: complete only after USER review"],
        "_legacy_completion_profile",
        accept_completion_profile,
    )
    _assert_journal_mutation_killed(
        "released lock accepted without coherent receipt completion",
        negative_setups["legacy receipt lacking completion evidence"],
        "_validate_legacy_completion_evidence",
        accept_completion_set,
    )
    _assert_journal_mutation_killed(
        "historical provenance checks skipped",
        negative_setups["legacy receipt with inconsistent snapshot hash"],
        "_validate_legacy_snapshot_evidence",
        lambda *_args, **_kwargs: [],
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ndai-target-currentness-") as temp_dir:
        root = Path(temp_dir)
        _manifest(root)
        target = _record(root)
        _assert_pass("valid selected live projection", _run(root))
        _assert_pass("stale root manifest is separate posture", _run(root))

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
            + "## Historical Receipts\nSource Repo HEAD: `historical-receipt-head`\n",
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
            apply=False,
            **expectations,
        )
        _assert_pass("target writer dry run", [] if ok and audit is None and target.read_bytes() == before else messages)

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
