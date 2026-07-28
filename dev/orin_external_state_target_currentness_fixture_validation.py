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
SEMANTIC_TARGETS = {
    "branches/feature_release_readiness_source_truth_intake/branch_state.md": "branch_state",
    "branches/feature_release_readiness_source_truth_intake/branch_plan.md": "branch_plan",
    "worktrees/Governance/worktree_state.md": "worktree_state",
}
SEMANTIC_CYCLE = "RRI-20260727-001"
PR_STATE_TARGET = (
    "branches/feature_release_readiness_source_truth_intake/pr_readiness_state.md"
)


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


def _semantic_root(root: Path) -> dict[str, Path]:
    _manifest(root)
    paths: dict[str, Path] = {}
    common = [
        "External State Schema: `external-state-v1`",
        "State Version: `1`",
        "Last Updated: `2026-07-27T20:00:00Z`",
        "Last Updated By: `fixture`",
        "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
        "Worktree: `C:\\Nexus Worktrees\\Governance`",
        "Worktree Path: `C:\\Nexus Worktrees\\Governance`",
        "Slot ID: `governance-standing`",
        "Branch: `feature/release-readiness-source-truth-intake`",
        f"Source Repo HEAD: `{HEAD}`",
        f"Origin/Main: `{ORIGIN_MAIN}`",
        f"Current Cycle: `{SEMANTIC_CYCLE}`",
        "Current Gate: `Bounded semantic currentness and lock-lifecycle reconciliation active; neutral-main fast-forward-only rebaseline pending separate USER decision.`",
        "Current USER Packet Status: `Pre-merge packet is historical evidence only; no post-merge packet was generated.`",
        "Current Pull Request: `None - no open/current PR; PR #290 historical merged evidence only.`",
        "Current PR State: `None / historical merged evidence only`",
        "Current Approval State: `Bounded reconciliation approved; staging, commit, and push are not approved.`",
        "Current Write Set: `branch_state.md; branch_plan.md; worktree_state.md`",
        "Current Validation State: `Semantic currentness and lock lifecycle validated; repair uncommitted.`",
        "Neutral Main State: `Stale versus fetched origin/main; fast-forward pending USER decision.`",
        "Next Legal Gate: `USER decision on fresh neutral-main fast-forward / Governance durability packet.`",
        "Final Disposition: `Bounded semantic-currentness and lock-lifecycle reconciliation remains active; neutral-main rebaseline is pending separate USER decision.`",
    ]
    record_contracts = {
        "branch_state": (
            "Live Branch Projection",
            "Post-merge Governance branch authority projection",
        ),
        "branch_plan": (
            "Live Branch Plan Projection",
            "Post-merge Governance branch plan projection",
        ),
        "worktree_state": (
            "Live Worktree Projection",
            "Current worktree assignment and acknowledgement projection",
        ),
    }
    for relative, label in SEMANTIC_TARGETS.items():
        record_class, record_role = record_contracts[label]
        path = root.joinpath(*relative.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        identity = [
            f"Record Class: `{record_class}`",
            f"Record Role: `{record_role}`",
        ]
        path.write_text(
            "# Semantic Currentness Fixture\n" + "\n".join([*common[:4], *identity, *common[4:]]) + "\n",
            encoding="utf-8",
        )
        paths[relative] = path
    return paths


def _semantic_failures(
    root: Path,
    repo_branch_record: Path | None = None,
) -> list[str]:
    return validator.validate_governance_semantic_currentness(
        root,
        expected_cycle=SEMANTIC_CYCLE,
        repo_branch_record=repo_branch_record,
    )


def _semantic_pr_projection(root: Path, record_class: str) -> Path:
    path = root.joinpath(*PR_STATE_TARGET.split("/"))
    path.write_text(
        "\n".join(
            [
                "# PR State Fixture",
                "External State Schema: `external-state-v1`",
                f"Record Class: `{record_class}`",
                "Record Role: `Historical PR readiness snapshot receipt`",
                "Historical Receipt Boundary: `This record does not own live PR truth.`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _semantic_target_snapshot(
    root: Path,
    paths: dict[str, Path],
    name: str,
    lock_id: str,
) -> Path:
    command = [
        sys.executable,
        str(Path(__file__).with_name("orin_external_state_snapshot.py")),
        "--root",
        str(root),
        "--reason",
        "bounded target-set fixture",
        "--worktree",
        WORKTREE_PATH,
        "--branch",
        "feature/release-readiness-source-truth-intake",
        "--snapshot-name",
        name,
        "--lock-id",
        lock_id,
        "--source-head",
        HEAD,
        "--apply",
    ]
    for relative in paths:
        command.extend(("--target", relative))
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(
            "targeted snapshot helper failed:\n" + result.stdout + result.stderr
        )
    snapshot = root / "snapshots" / name
    if not snapshot.is_dir():
        raise AssertionError("targeted snapshot helper did not create its exact directory")
    manifest = json.loads(
        (snapshot / "snapshot_manifest.json").read_text(encoding="utf-8")
    )
    lock_payload = json.loads(
        (root / "locks" / f"{lock_id}.json").read_text(encoding="utf-8")
    )
    if manifest.get("Lock ID") != lock_id or manifest.get("Workload ID") != lock_payload.get(
        "Workload ID"
    ):
        raise AssertionError("targeted snapshot manifest omitted its lock/workload binding")
    return snapshot


def _snapshot(
    root: Path,
    target: Path,
    name: str,
    *,
    include_target: bool = True,
    snapshot_bytes: bytes | None = None,
    manifest_root: str | None = None,
    manifest_hash: str | None = None,
    lock_id: str = "worktree-fixture-lock",
    workload_id: str = "fixture-workload",
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
            "Lock ID": lock_id,
            "Workload ID": workload_id,
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
                "Current Branch: `feature/release-readiness-source-truth-intake`",
            ).replace(
                f"Source Repo HEAD: `{HEAD}`",
                f"Source Repo HEAD: `{HEAD}`\nCurrent HEAD: `{HEAD.upper()}`",
            ).replace(
                f"Origin/Main: `{ORIGIN_MAIN}`",
                f"Origin/Main: `{ORIGIN_MAIN}`\nSource origin/main: `{ORIGIN_MAIN.upper()}`",
            ),
            encoding="utf-8",
        )
        _assert_pass("equivalent live identity aliases", _run(root))
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
                "Workload ID": "fixture-workload",
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
            lock_id="",
            snapshot="",
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
                "Workload ID": "fixture-workload",
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
            apply=True,
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
                "Workload ID": "fixture-workload",
                "Worktree": "Governance",
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        label_snapshot = _snapshot(
            root, target, "fixture-label-lock", lock_id=label_lock_id
        )
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        historical_snapshot = _snapshot(
            root,
            target,
            "fixture-historical-only-field",
            lock_id=historical_lock_id,
        )
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
            (
                "snapshot from another lock",
                _snapshot(
                    root,
                    target,
                    "fixture-wrong-lock",
                    lock_id="different-workload-lock",
                ),
                "snapshot lock identity mismatch",
            ),
            (
                "snapshot from another workload",
                _snapshot(
                    root,
                    target,
                    "fixture-wrong-workload",
                    workload_id="different-workload",
                ),
                "snapshot workload identity mismatch",
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
                apply=True,
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
                apply=True,
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
                "Workload ID": "fixture-workload",
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        rollback_snapshot = _snapshot(
            root, target, "fixture-rollback", lock_id=rollback_lock_id
        )
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
            root,
            lock_id,
            "fixture transition complete",
            apply=True,
            expected_workload_id="fixture-workload",
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        released, release_messages = lock_release.release_lock(
            root,
            release_mismatch_id,
            "fixture mismatched payload",
            apply=False,
            expected_workload_id="fixture-workload",
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
                "Workload ID": "fixture-workload",
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
                root,
                release_race_id,
                "fixture release race",
                apply=True,
                expected_workload_id="fixture-workload",
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        new_head = "d" * 40
        transition_snapshot = _snapshot(
            root,
            target,
            "fixture-head-transition-snapshot",
            lock_id=transition_lock_id,
        )
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
            root,
            transition_lock_id,
            "fixture head transition complete",
            apply=True,
            expected_workload_id="fixture-workload",
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        adversarial_snapshot = _snapshot(
            root,
            target,
            "fixture-adversarial-snapshot",
            lock_id=adversarial_lock_id,
        )
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        lock_race_snapshot = _snapshot(
            root, target, "fixture-lock-race", lock_id=lock_race_id
        )
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
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        snapshot_race_snapshot = _snapshot(
            root,
            target,
            "fixture-snapshot-race",
            lock_id=snapshot_race_id,
        )
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
        lock_id = "worktree-fixture-crlf"
        snapshot = _snapshot(root, target, "fixture-crlf", lock_id=lock_id)
        atomic_write_json(
            root / "locks" / f"{lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Locked",
                "Workload ID": "fixture-workload",
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

    with tempfile.TemporaryDirectory(prefix="ndai-target-retirement-") as temp_dir:
        root = Path(temp_dir)
        _manifest(root)
        snapshot_helper = Path(__file__).with_name("orin_external_state_snapshot.py")
        escaped_snapshot = root.parent / f"{root.name}-escaped-snapshot"
        for unsafe_name in (
            f"../{escaped_snapshot.name}",
            str(escaped_snapshot),
        ):
            unsafe_snapshot = subprocess.run(
                [
                    sys.executable,
                    str(snapshot_helper),
                    "--root",
                    str(root),
                    "--reason",
                    "unsafe full-root snapshot name fixture",
                    "--worktree",
                    WORKTREE_PATH,
                    "--branch",
                    "feature/release-readiness-source-truth-intake",
                    "--snapshot-name",
                    unsafe_name,
                    "--apply",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if unsafe_snapshot.returncode == 0 or "not a safe directory name" not in (
                unsafe_snapshot.stdout + unsafe_snapshot.stderr
            ):
                raise AssertionError(
                    f"full-root snapshot accepted unsafe name {unsafe_name!r}:\n"
                    + unsafe_snapshot.stdout
                    + unsafe_snapshot.stderr
                )
            if escaped_snapshot.exists():
                raise AssertionError("unsafe full-root snapshot escaped the canonical root")
        target = _record(root)
        target.write_text(
            target.read_text(encoding="utf-8")
            + "## Historical Receipt\nReceipt Value: `preserve exactly`\n",
            encoding="utf-8",
        )
        historical_section = target.read_text(encoding="utf-8").split(
            "## Historical Receipt", 1
        )[1]
        lock_id = "worktree-fixture-historical-retirement"
        snapshot = _snapshot(
            root,
            target,
            "fixture-historical-retirement",
            lock_id=lock_id,
        )
        atomic_write_json(
            root / "locks" / f"{lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Locked",
                "Workload ID": "fixture-workload",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": TARGET,
            },
        )
        expectations = _expectations(target)
        before = target.read_bytes()
        invalid_ok, invalid_messages, invalid_audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id="",
            snapshot="",
            assignments=["Last Updated=2026-01-02T00:00:00Z"],
            additions=[],
            post_record_state="historical-receipt",
            apply=False,
            **expectations,
        )
        if invalid_ok or invalid_audit is not None or target.read_bytes() != before or not any(
            "unsupported or missing historical Record Class" in item
            for item in invalid_messages
        ):
            raise AssertionError(
                "historical retirement accepted a live post-state:\n"
                + "\n".join(invalid_messages)
            )

        retirement_assignments = [
            "State Version=2",
            "Last Updated=2026-01-02T00:00:00Z",
            "Record Class=Historical Receipt",
            "Record Role=Historical worktree projection receipt; not live operational state",
            "Historical Receipt Boundary=This retired projection and all sections below are historical evidence only.",
        ]
        dry_ok, dry_messages, dry_audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id="",
            snapshot="",
            assignments=retirement_assignments,
            additions=[],
            post_record_state="historical-receipt",
            apply=False,
            **expectations,
        )
        if not dry_ok or dry_audit is not None or target.read_bytes() != before:
            raise AssertionError(
                "historical retirement dry run failed or mutated the target:\n"
                + "\n".join(dry_messages)
            )
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=TARGET,
            lock_id=lock_id,
            snapshot=snapshot.relative_to(root).as_posix(),
            assignments=retirement_assignments,
            additions=[],
            post_record_state="historical-receipt",
            apply=True,
            **expectations,
        )
        if not ok or audit is None:
            raise AssertionError(
                "historical retirement apply failed:\n" + "\n".join(messages)
            )
        after_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        _assert_pass(
            "retired target validates as historical receipt",
            validator.validate_target_historical_receipt(
                root,
                [TARGET],
                expected_target_sha256=after_hash,
                **{
                    key: value
                    for key, value in expectations.items()
                    if key != "expected_target_sha256"
                },
            ),
        )
        retired_text = target.read_text(encoding="utf-8")
        target.write_text(
            retired_text.replace(
                "Branch: `feature/release-readiness-source-truth-intake`",
                "Branch: `feature/release-readiness-source-truth-intake`\n"
                "Current Branch: `feature/conflicting-historical-alias`",
                1,
            ),
            encoding="utf-8",
        )
        conflicting_receipt_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        _assert_failure(
            "historical receipt conflicting identity aliases",
            "duplicate or conflicting historical identity fields",
            validator.validate_target_historical_receipt(
                root,
                [TARGET],
                expected_target_sha256=conflicting_receipt_hash,
                **{
                    key: value
                    for key, value in expectations.items()
                    if key != "expected_target_sha256"
                },
            ),
        )
        target.write_text(retired_text, encoding="utf-8")
        _assert_failure(
            "retired target cannot validate as live currentness",
            "historical receipt cannot be selected as live state",
            _run(root, expected_target_sha256=after_hash),
        )
        if target.read_text(encoding="utf-8").split("## Historical Receipt", 1)[1] != historical_section:
            raise AssertionError("historical retirement rewrote preserved receipt evidence")
        audit_payload = json.loads(audit.read_text(encoding="utf-8"))
        if audit_payload.get("Post Record State") != "historical-receipt":
            raise AssertionError("historical retirement audit omitted the post-record state")

    with tempfile.TemporaryDirectory(prefix="ndai-governance-semantic-currentness-") as temp_dir:
        root = Path(temp_dir)
        paths = _semantic_root(root)
        _assert_pass("coherent three-record Governance posture", _semantic_failures(root))

        pr_state = _semantic_pr_projection(root, "Live Branch Projection")
        _assert_failure(
            "same-branch live projection omitted from semantic inventory",
            "same-branch live projection omitted from semantic target inventory",
            _semantic_failures(root),
        )
        pr_state.write_text(
            pr_state.read_text(encoding="utf-8").replace(
                "Record Class: `Live Branch Projection`",
                "Record Class: `Historical Receipt`",
                1,
            ),
            encoding="utf-8",
        )
        _assert_pass(
            "same-branch historical receipt is excluded from live semantic inventory",
            _semantic_failures(root),
        )
        pr_state.unlink()

        repo_record = root / "repo_branch_record.md"
        repo_record.write_text(
            "\n".join(
                [
                    "# Branch Record Fixture",
                    "Active Seam: `External operational state only - current state is external.`",
                    "Intake State: `External operational state only - current PR state lives in "
                    "pr_readiness_state.md.`",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        _assert_failure(
            "repo route treats historical PR snapshot as current",
            "without an explicit historical-only, non-current boundary",
            _semantic_failures(root, repo_record),
        )
        repo_record.write_text(
            repo_record.read_text(encoding="utf-8").replace(
                "current PR state lives in pr_readiness_state.md.",
                "pr_readiness_state.md is historical snapshot evidence only and is not a current-state route.",
                1,
            )
            + "Receipt: `pr_readiness_state.md was retired without rewriting historical evidence.`\n",
            encoding="utf-8",
        )
        _assert_pass(
            "repo route classifies PR snapshot as historical only",
            _semantic_failures(root, repo_record),
        )

        evolved_fields = {
            "Current Gate: `Bounded semantic currentness and lock-lifecycle reconciliation active; neutral-main fast-forward-only rebaseline pending separate USER decision.`":
                "Current Gate: `Current-gate autonomous repair completed; later PR action remains separately gated.`",
            "Current USER Packet Status: `Pre-merge packet is historical evidence only; no post-merge packet was generated.`":
                "Current USER Packet Status: `Current canonical packet published and validated.`",
            "Current Pull Request: `None - no open/current PR; PR #290 historical merged evidence only.`":
                "Current Pull Request: `PR #301 https://example.invalid/pull/301`",
            "Current PR State: `None / historical merged evidence only`":
                "Current PR State: `Open / review pending`",
            "Current Approval State: `Bounded reconciliation approved; staging, commit, and push are not approved.`":
                "Current Approval State: `Bounded repair, commit, and push approved and completed; merge not approved.`",
            "Current Validation State: `Semantic currentness and lock lifecycle validated; repair uncommitted.`":
                "Current Validation State: `Current-gate semantic, packet, and lock validations PASS at durable HEAD.`",
            "Neutral Main State: `Stale versus fetched origin/main; fast-forward pending USER decision.`":
                "Neutral Main State: `Current and equal to origin/main.`",
            "Next Legal Gate: `USER decision on fresh neutral-main fast-forward / Governance durability packet.`":
                "Next Legal Gate: `USER review of current gate only.`",
        }
        for path in paths.values():
            text = path.read_text(encoding="utf-8")
            for before, after in evolved_fields.items():
                text = text.replace(before, after, 1)
            path.write_text(text, encoding="utf-8")
        _assert_pass(
            "coherent evolved Governance posture is not hardcoded to one cycle state",
            _semantic_failures(root),
        )
        paths = _semantic_root(root)

        for path in paths.values():
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "Current Approval State: `Bounded reconciliation approved; staging, commit, and push are not approved.`",
                    "Current Approval State: `Approval pending; approved action is unknown.`",
                    1,
                ),
                encoding="utf-8",
            )
        _assert_failure(
            "incidental approved substring is not an approval boundary",
            "must state an explicit approved or not-approved boundary",
            _semantic_failures(root),
        )
        paths = _semantic_root(root)

        for path in paths.values():
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "Neutral Main State: `Stale versus fetched origin/main; fast-forward pending USER decision.`",
                    "Neutral Main State: `Not current; rebaseline pending USER decision.`",
                    1,
                ),
                encoding="utf-8",
            )
        _assert_failure(
            "negated neutral-main currentness is not a current classification",
            "negates currentness without classifying neutral main as stale",
            _semantic_failures(root),
        )
        paths = _semantic_root(root)

        plan = paths["branches/feature_release_readiness_source_truth_intake/branch_plan.md"]
        original_plan = plan.read_text(encoding="utf-8")
        plan.write_text(
            original_plan.replace(
                "Final Disposition: `Bounded semantic-currentness and lock-lifecycle reconciliation remains active; neutral-main rebaseline is pending separate USER decision.`",
                "Final Disposition: `Standing cycle remains idle.`",
                1,
            ),
            encoding="utf-8",
        )
        _assert_failure(
            "stale Final Disposition",
            "Final Disposition retains stale idle posture",
            _semantic_failures(root),
        )
        plan.write_text(original_plan, encoding="utf-8")

        mutations = (
            (
                "branch-state current gate disagreement",
                "Current Gate: `Bounded semantic currentness and lock-lifecycle reconciliation active; neutral-main fast-forward-only rebaseline pending separate USER decision.`",
                "Current Gate: `Stage 1 Ready For Stage 2 - stale historical packet posture.`",
                "disagree on Current Gate",
            ),
            (
                "branch-plan old packet posture",
                "Current USER Packet Status: `Pre-merge packet is historical evidence only; no post-merge packet was generated.`",
                "Current USER Packet Status: `Current active PR Readiness Stage 1 packet is ready for Stage 2.`",
                "disagree on Current USER Packet Status",
            ),
            (
                "worktree current PR contradiction",
                "Current Pull Request: `None - no open/current PR; PR #290 historical merged evidence only.`",
                "Current Pull Request: `PR #290 open/current`",
                "disagree on Current Pull Request",
            ),
        )
        for label, before, after, needle in mutations:
            target = paths[next(relative for relative, name in SEMANTIC_TARGETS.items() if name == (
                "branch_state" if "branch-state" in label else "branch_plan" if "branch-plan" in label else "worktree_state"
            ))]
            original = target.read_text(encoding="utf-8")
            target.write_text(original.replace(before, after, 1), encoding="utf-8")
            _assert_failure(label, needle, _semantic_failures(root))
            target.write_text(original, encoding="utf-8")

        target = paths["branches/feature_release_readiness_source_truth_intake/branch_state.md"]
        original = target.read_text(encoding="utf-8")
        target.write_text(
            original + "\n## Historical Receipt\nCurrent Gate: `Stage 1 Ready For Stage 2`\n",
            encoding="utf-8",
        )
        _assert_pass("historical wording remains evidence", _semantic_failures(root))
        target.write_text(original, encoding="utf-8")
        target.write_text(
            original + "\n## Current Gate\nCurrent Gate: `Stage 1 Ready For Stage 2`\n",
            encoding="utf-8",
        )
        _assert_failure("current section is not historical", "current section", _semantic_failures(root))
        target.write_text(original, encoding="utf-8")

        target = paths["worktrees/Governance/worktree_state.md"]
        original = target.read_text(encoding="utf-8")
        target.write_text(original.replace(f"Current Cycle: `{SEMANTIC_CYCLE}`", "Current Cycle: `None`", 1), encoding="utf-8")
        _assert_failure("missing live cycle identity", "Current Cycle", _semantic_failures(root))
        target.write_text(original, encoding="utf-8")

        target.write_text(original.replace("Current PR State: `None / historical merged evidence only`", "Current PR State: `Open`", 1), encoding="utf-8")
        _assert_failure("merged PR represented as active", "Current PR State", _semantic_failures(root))
        target.write_text(original, encoding="utf-8")

    def target_set_requests(paths: dict[str, Path]):
        assignments = (
            "State Version=2",
            "Last Updated=2026-07-27T21:00:00Z",
            "Current Gate=Current-gate target-set fixture published; later actions remain separately gated.",
            "Current Approval State=Bounded target-set repair approved and completed; later actions not approved.",
            "Current Validation State=Coherent target-set semantic validation PASS.",
            "Next Legal Gate=USER review of the coherent current gate.",
        )
        return tuple(
            reconciler.TargetReconcileRequest(
                target=relative,
                expected_branch="feature/release-readiness-source-truth-intake",
                expected_source_head=HEAD,
                expected_origin_main=ORIGIN_MAIN,
                expected_worktree_path=WORKTREE_PATH,
                expected_worktree_slot=SLOT,
                expected_target_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                assignments=assignments,
            )
            for relative, path in paths.items()
        )

    audit_target = "audit_log/target-set-current-gate-fixture.json"
    with tempfile.TemporaryDirectory(prefix="ndai-governance-target-set-") as temp_dir:
        root = Path(temp_dir)
        paths = _semantic_root(root)
        before = {relative: path.read_bytes() for relative, path in paths.items()}
        requests = target_set_requests(paths)
        dry_ok, dry_messages, dry_audit = reconciler.reconcile_target_set(
            root=root,
            lock_id="",
            snapshot="",
            audit_target=audit_target,
            requests=requests,
            final_validation=_semantic_failures,
            apply=False,
        )
        if not dry_ok or dry_audit is not None:
            raise AssertionError(
                "coherent target-set draft failed before lock acquisition:\n"
                + "\n".join(dry_messages)
            )
        if any(path.read_bytes() != before[relative] for relative, path in paths.items()):
            raise AssertionError("target-set draft validation mutated a live projection")
        if any((root / "locks").glob("*.json")):
            raise AssertionError("target-set draft validation acquired a lock")

        lock_id = "target-set-success-lock"
        snapshot_relative = "snapshots/target-set-success"
        write_set = ";".join(
            [*paths, audit_target, snapshot_relative]
        )
        atomic_write_json(
            root / "locks" / f"{lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Locked",
                "Workload ID": "target-set-success-workload",
                "Last Updated By": "fixture",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": write_set,
            },
        )
        snapshot = _semantic_target_snapshot(
            root,
            paths,
            "target-set-success",
            lock_id,
        )
        ok, messages, audit = reconciler.reconcile_target_set(
            root=root,
            lock_id=lock_id,
            snapshot=snapshot.relative_to(root).as_posix(),
            audit_target=audit_target,
            requests=requests,
            final_validation=_semantic_failures,
            apply=True,
        )
        if not ok or audit is None or not audit.is_file():
            raise AssertionError(
                "coherent target-set publication failed:\n" + "\n".join(messages)
            )
        _assert_pass("coherent target-set final semantic validation", _semantic_failures(root))
        if any(path.read_bytes() == before[relative] for relative, path in paths.items()):
            raise AssertionError("coherent target-set publication omitted a projection")

    with tempfile.TemporaryDirectory(prefix="ndai-governance-target-set-rollback-") as temp_dir:
        root = Path(temp_dir)
        paths = _semantic_root(root)
        before = {relative: path.read_bytes() for relative, path in paths.items()}
        requests = target_set_requests(paths)
        lock_id = "target-set-rollback-lock"
        snapshot_relative = "snapshots/target-set-rollback"
        atomic_write_json(
            root / "locks" / f"{lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": lock_id,
                "Lock State": "Locked",
                "Workload ID": "target-set-rollback-workload",
                "Last Updated By": "fixture",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": ";".join(
                    [*paths, audit_target, snapshot_relative]
                ),
            },
        )
        snapshot = _semantic_target_snapshot(
            root,
            paths,
            "target-set-rollback",
            lock_id,
        )

        def fail_only_after_live_publication(candidate_root: Path) -> list[str]:
            semantic = _semantic_failures(candidate_root)
            if candidate_root.resolve() == root.resolve() and not semantic:
                return ["forced set-level final validation failure"]
            return semantic

        ok, messages, audit = reconciler.reconcile_target_set(
            root=root,
            lock_id=lock_id,
            snapshot=snapshot.relative_to(root).as_posix(),
            audit_target=audit_target,
            requests=requests,
            final_validation=fail_only_after_live_publication,
            apply=True,
        )
        if ok or audit is not None or not any(
            "forced set-level final validation failure" in message for message in messages
        ):
            raise AssertionError(
                "target-set final failure did not block publication:\n" + "\n".join(messages)
            )
        if any(path.read_bytes() != before[relative] for relative, path in paths.items()):
            raise AssertionError("target-set final failure did not restore every projection")
        if (root / audit_target).exists():
            raise AssertionError("target-set rollback retained its audit as current state")

        def raise_only_after_live_publication(candidate_root: Path) -> list[str]:
            semantic = _semantic_failures(candidate_root)
            if candidate_root.resolve() == root.resolve() and not semantic:
                raise RuntimeError("forced set-level final validator exception")
            return semantic

        ok, messages, audit = reconciler.reconcile_target_set(
            root=root,
            lock_id=lock_id,
            snapshot=snapshot.relative_to(root).as_posix(),
            audit_target=audit_target,
            requests=requests,
            final_validation=raise_only_after_live_publication,
            apply=True,
        )
        if ok or audit is not None or not any(
            "forced set-level final validator exception" in message
            for message in messages
        ):
            raise AssertionError(
                "raised target-set validator exception did not block publication:\n"
                + "\n".join(messages)
            )
        if any(path.read_bytes() != before[relative] for relative, path in paths.items()):
            raise AssertionError(
                "raised target-set validator exception did not restore every projection"
            )
        if (root / audit_target).exists():
            raise AssertionError(
                "raised target-set validator exception retained an audit as current state"
            )

    print("Target-scoped external-state currentness fixture validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
