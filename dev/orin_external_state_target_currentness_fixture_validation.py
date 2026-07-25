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
from orin_external_state_common import atomic_write_json, sha256_file


TARGET = "worktrees/Governance/worktree_state.md"
HEAD = "a" * 40
ORIGIN_MAIN = "b" * 40
WORKTREE_PATH = r"C:\Nexus Worktrees\Governance"
SLOT = "governance-standing"


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
                "Worktree: `Governance`",
                "Worktree Path: `" + worktree_path + "`",
                "Branch: `" + branch + "`",
                "Source Repo HEAD: `" + head + "`",
                "Origin/Main: `" + origin_main + "`",
                "Slot ID: `" + slot + "`",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
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
    relative_target: str = TARGET,
    include_target: bool = True,
    snapshot_bytes: bytes | None = None,
    manifest_root: str | None = None,
    manifest_hash: str | None = None,
) -> Path:
    snapshot = root / "snapshots" / name
    snapshot.mkdir(parents=True)
    if include_target:
        snapshot_target = snapshot.joinpath(*relative_target.split("/"))
        snapshot_target.parent.mkdir(parents=True, exist_ok=True)
        snapshot_target.write_bytes(snapshot_bytes if snapshot_bytes is not None else target.read_bytes())
    target_hash = manifest_hash
    if target_hash is None and include_target:
        target_hash = hashlib.sha256(
            snapshot.joinpath(*relative_target.split("/")).read_bytes()
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
                    "path": relative_target,
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


SEMANTIC_TARGETS = (
    "branches/feature_fixture/branch_plan.md",
    "branches/feature_fixture/branch_state.md",
    "worktrees/FAM-003/worktree_state.md",
)
SEMANTIC_BRANCH = "feature/fixture"
SEMANTIC_WORKTREE_PATH = r"C:\Nexus Worktrees\FAM-003"
SEMANTIC_SLOT = "runtime-active-3"
SEMANTIC_GATE = "R2 Workstream completion USER review pending - performance decision required"
SEMANTIC_WORKSTREAM = "USER_DECISION_REQUIRED"
SEMANTIC_STAGES = "NOT_ENTERED / NOT_ENTERED / NOT_REQUESTED"
SEMANTIC_NEXT = "USER decision on Decision 2 Option G planning-revision preparation only, if USER chooses to proceed"
SEMANTIC_TRANSITION = "MIGRATION_COMPLETE_CURRENT_PENDING_USER_PERFORMANCE_DECISION"


def _write_semantic_record(
    root: Path,
    relative: str,
    *,
    state_version: int = 2,
    last_updated: str = "2026-01-02T00:00:00+00:00",
    next_phase: str = SEMANTIC_NEXT,
    transition: str = SEMANTIC_TRANSITION,
) -> Path:
    record_class = {
        SEMANTIC_TARGETS[0]: "Live Branch Plan",
        SEMANTIC_TARGETS[1]: "Live Branch Projection",
        SEMANTIC_TARGETS[2]: "Live Worktree Projection",
    }[relative]
    path = root.joinpath(*relative.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# Projection Set Semantic Fixture",
                "External State Schema: `external-state-v1`",
                f"State Version: `{state_version}`",
                f"Last Updated: `{last_updated}`",
                "Last Updated By: `Codex`",
                f"Record Class: `{record_class}`",
                "Record Role: `Current fixture projection`",
                "Worktree: `FAM-003`",
                f"Worktree Path: `{SEMANTIC_WORKTREE_PATH}`",
                f"Branch: `{SEMANTIC_BRANCH}`",
                f"Source Repo HEAD: `{HEAD}`",
                f"Origin/Main: `{ORIGIN_MAIN}`",
                f"Slot ID: `{SEMANTIC_SLOT}`",
                f"Current Gate: `{SEMANTIC_GATE}`",
                f"Workstream Result: `{SEMANTIC_WORKSTREAM}`",
                f"H1 / LV / UTS: `{SEMANTIC_STAGES}`",
                f"Next Legal Phase: `{next_phase}`",
                f"Transition Status: `{transition}`",
                "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`",
                "",
                "\ufeff## Historical Receipt",
                "Next Legal Phase: `USER Decision 1 on this bounded migration`",
                "Decision 1: `PENDING_HISTORICAL_ONLY`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _semantic_fixture(root: Path) -> tuple[Path, Path]:
    _manifest(root, source_head=HEAD)
    snapshot = root / "snapshots" / "semantic-before"
    for target in SEMANTIC_TARGETS:
        snapshot_target = _write_semantic_record(
            snapshot,
            target,
            state_version=1,
            last_updated="2026-01-01T00:00:00+00:00",
        )
        current_target = root.joinpath(*target.split("/"))
        current_target.parent.mkdir(parents=True, exist_ok=True)
        current_target.write_bytes(snapshot_target.read_bytes())
        _write_semantic_record(root, target)
    audit = root / "audit_log" / "migration-completion.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(
        audit,
        {
            "Transition Status": "MIGRATION_COMPLETE",
            "Decision 1": "COMPLETE",
            "Decision 2": "ELIGIBLE_FOR_SEPARATE_USER_APPROVAL_ONLY",
            "Decision 3": "SEPARATE_FUTURE_GATE",
            "Workstream": SEMANTIC_WORKSTREAM,
            "H1 / LV / UTS": SEMANTIC_STAGES,
            "Next Legal Phase": SEMANTIC_NEXT,
            "Source Repo HEAD": HEAD,
            "Origin/Main": ORIGIN_MAIN,
        },
    )
    review = root / "review" / "primary.md"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text(
        "Decision 1 is complete. Decision 2 is eligible for a separate USER approval only. "
        "Decision 3 remains a future gate.\n",
        encoding="utf-8",
    )
    return audit, review


def _semantic_run(root: Path) -> list[str]:
    return validator.validate_projection_set_semantic_coherence(
        root,
        list(SEMANTIC_TARGETS),
        expected_target_hashes={
            target: sha256_file(root.joinpath(*target.split("/"))) for target in SEMANTIC_TARGETS
        },
        expected_branch=SEMANTIC_BRANCH,
        expected_source_head=HEAD,
        expected_origin_main=ORIGIN_MAIN,
        expected_worktree_path=SEMANTIC_WORKTREE_PATH,
        expected_worktree_slot=SEMANTIC_SLOT,
        expected_current_gate=SEMANTIC_GATE,
        expected_workstream_result=SEMANTIC_WORKSTREAM,
        expected_stage_states=SEMANTIC_STAGES,
        expected_next_legal_phase=SEMANTIC_NEXT,
        expected_transition_status=SEMANTIC_TRANSITION,
        expected_state_version=2,
        expected_last_updated_by="Codex",
        previous_snapshot="snapshots/semantic-before",
        completion_audit="audit_log/migration-completion.json",
        primary_review="review/primary.md",
        expected_decision_1="COMPLETE",
        expected_decision_2="ELIGIBLE_FOR_SEPARATE_USER_APPROVAL_ONLY",
        expected_decision_3="SEPARATE_FUTURE_GATE",
    )


def _run_projection_set_semantic_fixtures(parent: Path) -> None:
    def case(name: str) -> Path:
        root = parent / name
        root.mkdir(parents=True, exist_ok=True)
        _semantic_fixture(root)
        return root

    root = case("semantic-valid-historical-text")
    _assert_pass("historical Decision 1 receipt is not live state", _semantic_run(root))

    root = case("semantic-decision1-stale-route")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(root, target, next_phase="USER Decision 1 on this bounded migration")
    _assert_failure(
        "Decision 1 complete but next route asks for Decision 1",
        "Decision 1 is complete",
        _semantic_run(root),
    )

    root = case("semantic-migration-pending")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(root, target, transition="MIGRATION_PENDING")
    _assert_failure(
        "migration complete audit but live transition remains pending",
        "live Transition Status mismatch",
        _semantic_run(root),
    )

    root = case("semantic-decision2-started")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(root, target, next_phase="Decision 2 approved and started")
    _assert_failure(
        "Decision 2 eligible but live state says started",
        "claims it is approved or started",
        _semantic_run(root),
    )

    root = case("semantic-decision3-merged")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(
            root,
            target,
            next_phase="USER approval for Decision 2 and Decision 3 planning",
        )
    _assert_failure(
        "Decision 3 merged into Decision 2",
        "Decision 3 was merged",
        _semantic_run(root),
    )

    root = case("semantic-cross-target-mismatch")
    _write_semantic_record(root, SEMANTIC_TARGETS[2], next_phase="USER Decision 1 on this bounded migration")
    _assert_failure(
        "cross-target next legal phase mismatch",
        "cross-target Next Legal Phase mismatch",
        _semantic_run(root),
    )

    root = case("semantic-audit-review-live-disagreement")
    audit = root / "audit_log" / "migration-completion.json"
    payload = json.loads(audit.read_text(encoding="utf-8"))
    payload["Decision 1"] = "PENDING"
    atomic_write_json(audit, payload)
    _assert_failure(
        "audit review and live state disagree",
        "completion audit Decision 1 mismatch",
        _semantic_run(root),
    )

    root = case("semantic-stale-version-timestamp")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(
            root,
            target,
            state_version=1,
            last_updated="2026-01-01T00:00:00+00:00",
        )
    failures = _semantic_run(root)
    _assert_failure("state version did not advance", "State Version did not advance", failures)
    _assert_failure("timestamp did not advance", "Last Updated did not advance", failures)

    root = case("semantic-packet-eligibility-live-decision1")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(root, target, next_phase="USER Decision 1 on this bounded migration")
    _assert_failure(
        "packet says eligibility while active state routes Decision 1",
        "packet says Decision 1 is complete",
        _semantic_run(root),
    )

    root = case("semantic-target-only-false-green")
    for target in SEMANTIC_TARGETS:
        _write_semantic_record(root, target, next_phase="USER Decision 1 on this bounded migration")
    selected = root.joinpath(*SEMANTIC_TARGETS[0].split("/"))
    _assert_pass(
        "legacy target-currentness intentionally does not adjudicate phase semantics",
        validator.validate_target_currentness(
            root,
            [SEMANTIC_TARGETS[0]],
            expected_branch=SEMANTIC_BRANCH,
            expected_source_head=HEAD,
            expected_origin_main=ORIGIN_MAIN,
            expected_worktree_path=SEMANTIC_WORKTREE_PATH,
            expected_worktree_slot=SEMANTIC_SLOT,
            expected_target_sha256=sha256_file(selected),
        ),
    )
    _assert_failure(
        "projection-set semantic mode closes target-only false green",
        "Decision 1 is complete",
        _semantic_run(root),
    )


UFD_TARGET = "branches/feature_fam_003_settings_resize_proof/branch_plan.md"
UFD_BRANCH = "feature/fam-003-settings-resize-proof"
UFD_WORKTREE_PATH = r"C:\Nexus Worktrees\FAM-003"
UFD_SLOT = "runtime-active-3"
UFD_OWNER = (
    r"C:\Nexus Governance State\branches"
    r"\feature_fam_003_settings_resize_proof\branch_plan.md"
)
UFD_FOLD_DOWN_TARGET = "Docs/branch_records/feature_fam_003_settings_resize_proof.md"
ELEMENT_HEADER = (
    "| Element ID | Element / Surface | Element Classification | "
    "Workstream Implementation Plan | Workstream Proof Plan | "
    "Hardening Proof Plan | Live Validation Proof / Waiver Plan | "
    "UTS / USER Acceptance Path | Future / Deferred Boundary | "
    "USER Decision State | Source Owner / Ledger Owner |"
)


def _ufd_fixture_rows() -> list[str]:
    rows: list[str] = []
    for index in range(1, 19):
        item_id = f"UFD-FAM003-20260724-{index:03d}"
        rows.append(
            "\n".join(
                (
                    f"### UFD Item: {item_id}",
                    f"Feedback ID: `{item_id}`",
                    f"Feedback Summary: `Atomic Option G direction {index}`",
                    "Feedback Source: `USER direction`",
                    "Feedback Phase: `BP3 repair`",
                    "Disposition Type: `Current Branch Requirement`",
                    "USER Decision State: `Accepted by USER`",
                    "Owner Class: `Branch Plan`",
                    f"Canonical Owner File: `{UFD_OWNER}`",
                    "Workstream Severity: `Level 2 seam-blocking`",
                    "Status: `Closed`",
                    f"Fold-Down Target: `{UFD_FOLD_DOWN_TARGET}`",
                    "Pointer Locations: `Supporting packet and evidence copies`",
                    "Source / Date: `USER / 2026-07-24`",
                    f"USER Direction Or Finding: `Accepted Option G direction {index}`",
                    "Affected Scope: `Option G`",
                    "Affected Artifact: `BP3 planning`",
                    "Classification: `Incorporated`",
                    "Owner: `FAM-003`",
                    "Carrier: `feature/fam-003-settings-resize-proof`",
                    "Planning Or Implementation Effect: `Planning carrydown only`",
                    "Proof / Closure Requirement: `Canonical owner and copy-equivalence proof`",
                    "Remaining USER Decision: `BP3 acceptance only`",
                )
            )
        )
    return rows


def _element_to_phase_fixture() -> str:
    classifications = (
        "Touched",
        "Touched",
        "Touched",
        "Affected",
        "Planned",
        "Planned",
        "Affected",
        "Affected",
        "Affected",
        "Affected",
        "Deferred",
    )
    rows = []
    for index, classification in enumerate(classifications, start=1):
        rows.append(
            f"| `OPTG-ELEM-{index:02d}` | Element {index} | {classification} | "
            f"Implement plan {index} | Workstream proof {index} | Hardening proof {index} | "
            f"Live Validation proof or waiver {index} | UTS acceptance {index} | "
            f"Future boundary {index} | BP3 pending | {UFD_OWNER} |"
        )
    return "\n".join(
        (
            "## Element-to-Phase Proof Matrix",
            "",
            "Matrix Status: `Present`",
            "USER Review Status: `Pending`",
            "Open Element Questions: `None`",
            f"Element Coverage Owner: `{UFD_OWNER}`",
            f"Element Validation Ledger Owner: `{UFD_OWNER}`",
            "",
            ELEMENT_HEADER,
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *rows,
        )
    )


def _write_ufd_record(root: Path, text_override: str | None = None) -> Path:
    target = root.joinpath(*UFD_TARGET.split("/"))
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n\n".join(_ufd_fixture_rows())
    text = text_override or (
        "# FAM-003 UFD Target Currentness Fixture\n"
        "External State Schema: `external-state-v1`\n"
        "State Version: `1`\n"
        "Last Updated: `2026-01-01T00:00:00Z`\n"
        "Last Updated By: `fixture`\n"
        "Record Class: `Live Branch Plan`\n"
        "Record Role: `Current branch planning projection`\n"
        "Worktree: `FAM-003`\n"
        f"Worktree Path: `{UFD_WORKTREE_PATH}`\n"
        f"Branch: `{UFD_BRANCH}`\n"
        f"Source Repo HEAD: `{HEAD}`\n"
        f"Origin/Main: `{ORIGIN_MAIN}`\n"
        f"Slot ID: `{UFD_SLOT}`\n"
        "USER Feedback Disposition Required: `Yes`\n"
        "UFD Ledger Status: `Complete`\n"
        f"UFD Ledger Owner: `{UFD_OWNER}`\n"
        "UFD Item Count: `18`\n"
        f"UFD Physical Detail Location: `{UFD_OWNER}`\n"
        "UFD Current Owner Class: `Branch Plan`\n"
        f"UFD Current Canonical Owner File: `{UFD_OWNER}`\n"
        f"UFD Future Fold-Down Target: `{UFD_FOLD_DOWN_TARGET}`\n"
        "Open UFD Count: `0`\n"
        "Blocking UFD Count: `0`\n"
        "Fold-Down Status: `Pending`\n\n"
        f"{rows}\n\n"
        f"{_element_to_phase_fixture()}\n\n"
        "Historical Receipt Boundary: `Historical receipts below do not redefine live fields.`\n"
    )
    target.write_text(text, encoding="utf-8")
    return target


def _run_ufd_owner_fixtures(parent: Path) -> None:
    root = parent / "ufd-owner"
    root.mkdir(parents=True, exist_ok=True)
    _manifest(root)
    target = _write_ufd_record(root)
    original = target.read_text(encoding="utf-8")

    def validate(text: str) -> list[str]:
        _write_ufd_record(root, text)
        return validator.validate_target_currentness(
            root,
            [UFD_TARGET],
            expected_branch=UFD_BRANCH,
            expected_source_head=HEAD,
            expected_origin_main=ORIGIN_MAIN,
            expected_worktree_path=UFD_WORKTREE_PATH,
            expected_worktree_slot=UFD_SLOT,
            expected_target_sha256=sha256_file(target),
            expected_schema="external-state-v1",
        )

    _assert_pass("canonical UFD owner with 18 physical rows", validate(original))
    rows = "\n\n".join(_ufd_fixture_rows())
    matrix = _element_to_phase_fixture()
    historical = (
        "Historical Receipt Boundary: "
        "`Historical receipts below do not redefine live fields.`\n"
    )
    cases = (
        (
            "declared owner without atomic rows",
            original.replace(rows + "\n\n", ""),
            "exactly 18 physical atomic rows",
        ),
        (
            "owner marker disagrees with physical file",
            original.replace(UFD_OWNER, "Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md", 1),
            "UFD Ledger Owner does not match",
        ),
        (
            "physical detail location disagrees",
            original.replace(
                f"UFD Physical Detail Location: `{UFD_OWNER}`",
                "UFD Physical Detail Location: `ufd_ledger.md`",
            ),
            "UFD Physical Detail Location",
        ),
        (
            "declared item count disagrees",
            original.replace("UFD Item Count: `18`", "UFD Item Count: `17`"),
            "declared UFD Item Count does not match",
        ),
        (
            "atomic rows below historical boundary",
            original.replace(rows + "\n\n", "").replace(
                historical,
                historical + rows + "\n",
            ),
            "exactly 18 physical atomic rows",
        ),
        (
            "atomic row missing required field",
            original.replace("Proof / Closure Requirement:", "Proof Closure Requirement:", 1),
            "missing required field Proof / Closure Requirement:",
        ),
        (
            "open count disagrees with rows",
            original.replace("Open UFD Count: `0`", "Open UFD Count: `1`"),
            "Open UFD Count 1 does not match",
        ),
        (
            "blocking count disagrees with rows",
            original.replace("Blocking UFD Count: `0`", "Blocking UFD Count: `1`"),
            "Blocking UFD Count 1 does not match",
        ),
        (
            "pointer target redirects canonical detail",
            original.replace(
                "UFD Physical Detail Location:",
                "UFD Detail Record:",
                1,
            ),
            "must not redirect full-detail authority",
        ),
        (
            "duplicate atomic item",
            original.replace(_ufd_fixture_rows()[-1], _ufd_fixture_rows()[-2], 1),
            "duplicate atomic row",
        ),
        (
            "row owner class points to future branch record",
            original.replace("Owner Class: `Branch Plan`", "Owner Class: `Branch Record`", 1),
            "Owner Class must be Branch Plan",
        ),
        (
            "row canonical owner points to future branch record",
            original.replace(
                f"Canonical Owner File: `{UFD_OWNER}`",
                f"Canonical Owner File: `{UFD_FOLD_DOWN_TARGET}`",
                1,
            ),
            "Canonical Owner File must match",
        ),
        (
            "row canonical owner points to packet aid",
            original.replace(
                f"Canonical Owner File: `{UFD_OWNER}`",
                "Canonical Owner File: `Review Aids/OPTION_G_UFD_AND_FOLD_DOWN.md`",
                1,
            ),
            "Canonical Owner File must match",
        ),
        (
            "row canonical owner is ambiguous relative path",
            original.replace(
                f"Canonical Owner File: `{UFD_OWNER}`",
                "Canonical Owner File: `branch_plan.md`",
                1,
            ),
            "Canonical Owner File must match",
        ),
        (
            "row fold-down target is missing",
            original.replace(
                f"Fold-Down Target: `{UFD_FOLD_DOWN_TARGET}`",
                "Fold-Down Target: ``",
                1,
            ),
            "Fold-Down Target must identify",
        ),
        (
            "row fold-down target conflates current owner",
            original.replace(
                f"Fold-Down Target: `{UFD_FOLD_DOWN_TARGET}`",
                f"Fold-Down Target: `{UFD_OWNER}`",
                1,
            ),
            "Fold-Down Target must identify",
        ),
        (
            "ledger current owner class points to branch record",
            original.replace(
                "UFD Current Owner Class: `Branch Plan`",
                "UFD Current Owner Class: `Branch Record`",
            ),
            "UFD Current Owner Class must be Branch Plan",
        ),
        (
            "ledger current canonical owner points to branch record",
            original.replace(
                f"UFD Current Canonical Owner File: `{UFD_OWNER}`",
                f"UFD Current Canonical Owner File: `{UFD_FOLD_DOWN_TARGET}`",
            ),
            "UFD Current Canonical Owner File must match",
        ),
        (
            "ledger future fold-down target is missing",
            original.replace(
                f"UFD Future Fold-Down Target: `{UFD_FOLD_DOWN_TARGET}`",
                "UFD Future Fold-Down Target: ``",
            ),
            "UFD Future Fold-Down Target must identify",
        ),
        (
            "ledger future fold-down target conflates current owner",
            original.replace(
                f"UFD Future Fold-Down Target: `{UFD_FOLD_DOWN_TARGET}`",
                f"UFD Future Fold-Down Target: `{UFD_OWNER}`",
            ),
            "UFD Future Fold-Down Target must identify",
        ),
        (
            "canonical row uses this annex",
            original.replace(
                "Pointer Locations: `Supporting packet and evidence copies`",
                "Pointer Locations: `this annex`",
                1,
            ),
            "context-relative location wording",
        ),
        (
            "canonical row uses the annex",
            original.replace(
                "Pointer Locations: `Supporting packet and evidence copies`",
                "Pointer Locations: `the annex`",
                1,
            ),
            "context-relative location wording",
        ),
        (
            "canonical row uses this supporting record",
            original.replace(
                "Pointer Locations: `Supporting packet and evidence copies`",
                "Pointer Locations: `this supporting record`",
                1,
            ),
            "context-relative location wording",
        ),
        (
            "canonical row uses the record above",
            original.replace(
                "Pointer Locations: `Supporting packet and evidence copies`",
                "Pointer Locations: `the record above`",
                1,
            ),
            "context-relative location wording",
        ),
        (
            "matrix exists only as a pointer",
            original.replace(matrix + "\n\n", ""),
            "does not physically contain the canonical Element-to-Phase",
        ),
        (
            "matrix coverage owner uses context-relative phrase",
            original.replace(
                f"Element Coverage Owner: `{UFD_OWNER}`",
                "Element Coverage Owner: `this branch-plan-owned annex`",
            ),
            "Element Coverage Owner must name",
        ),
        (
            "matrix ledger owner uses context-relative phrase",
            original.replace(
                f"Element Validation Ledger Owner: `{UFD_OWNER}`",
                "Element Validation Ledger Owner: `future Workstream raw-evidence manifest`",
            ),
            "Element Validation Ledger Owner must name",
        ),
        (
            "matrix header uses legacy aliases",
            original.replace(
                ELEMENT_HEADER,
                ELEMENT_HEADER.replace("Element Classification", "Classification"),
            ),
            "exact 11-column schema",
        ),
        (
            "matrix row uses invalid preserved classification",
            original.replace("| Element 7 | Affected |", "| Element 7 | Preserved |"),
            "invalid Element Classification",
        ),
        (
            "matrix omits one required row",
            original.replace(
                next(
                    line
                    for line in matrix.splitlines()
                    if line.startswith("| `OPTG-ELEM-11`")
                )
                + "\n",
                "",
            ),
            "must contain exactly 11 ordered unique rows",
        ),
        (
            "matrix duplicates one required ID",
            original.replace("`OPTG-ELEM-11`", "`OPTG-ELEM-10`", 1),
            "must contain exactly 11 ordered unique rows",
        ),
        (
            "matrix row has an empty proof path",
            original.replace("| Workstream proof 1 |", "|  |", 1),
            "contains an empty required cell",
        ),
        (
            "matrix moved below historical boundary",
            original.replace(
                matrix + "\n\n" + historical,
                historical + matrix + "\n",
            ),
            "does not physically contain the canonical Element-to-Phase",
        ),
        (
            "matrix status is invalid",
            original.replace("Matrix Status: `Present`", "Matrix Status: `COMPLETE`"),
            "Matrix Status is missing or invalid",
        ),
        (
            "matrix user review status is invalid",
            original.replace(
                "USER Review Status: `Pending`",
                "USER Review Status: `Green by validator`",
            ),
            "USER Review Status is missing or invalid",
        ),
        (
            "matrix row has an extra column",
            original.replace(
                "| Future boundary 1 | BP3 pending |",
                "| Future boundary 1 | extra | BP3 pending |",
                1,
            ),
            "has 12 columns",
        ),
    )
    for name, text, needle in cases:
        _assert_failure(name, needle, validate(text))


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

        legacy_relative = "branches/legacy-schema-fixture/branch_state.md"
        legacy_target = root.joinpath(*legacy_relative.split("/"))
        legacy_target.parent.mkdir(parents=True, exist_ok=True)
        legacy_body = (
            b"\xef\xbb\xbf## Legacy Branch State\n"
            b"Branch: `historical-wrong-branch`\n"
            b"Source Repo HEAD: `historical-wrong-head`\n"
            b"Current Gate: `historical-only`\n"
        )
        legacy_target.write_bytes(legacy_body)
        legacy_lock_id = "branch-fixture-legacy-schema-lock"
        atomic_write_json(
            root / "locks" / f"{legacy_lock_id}.json",
            {
                "External State Schema": "external-state-v1",
                "Lock ID": legacy_lock_id,
                "Lock State": "Locked",
                "Worktree": WORKTREE_PATH,
                "Branch": "feature/release-readiness-source-truth-intake",
                "Intended Write Set": legacy_relative,
            },
        )
        legacy_snapshot = _snapshot(
            root,
            legacy_target,
            "fixture-legacy-schema-addition",
            relative_target=legacy_relative,
        )
        legacy_expectations = {
            "expected_branch": "feature/release-readiness-source-truth-intake",
            "expected_source_head": HEAD,
            "expected_origin_main": ORIGIN_MAIN,
            "expected_worktree_path": WORKTREE_PATH,
            "expected_worktree_slot": SLOT,
            "expected_target_sha256": sha256_file(legacy_target),
        }
        legacy_additions = [
            "External State Schema=external-state-v1",
            "State Version=1",
            "Record Class=Live Branch Projection",
            "Record Role=Current active branch phase, blocker, and next legal phase fields",
            "Branch=feature/release-readiness-source-truth-intake",
            f"Source Repo HEAD={HEAD}",
            f"Origin/Main={ORIGIN_MAIN}",
            "Worktree=Governance",
            f"Worktree Path={WORKTREE_PATH}",
            f"Slot ID={SLOT}",
            "Last Updated=2026-01-02T00:00:00+00:00",
            "Last Updated By=Codex",
            "Historical Receipt Boundary=Existing record body below this boundary is immutable historical receipt evidence.",
        ]
        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=legacy_relative,
            lock_id=legacy_lock_id,
            snapshot=legacy_snapshot.relative_to(root).as_posix(),
            assignments=[],
            additions=legacy_additions,
            apply=False,
            **legacy_expectations,
        )
        if not ok or audit is not None or legacy_target.read_bytes() != legacy_body:
            raise AssertionError(
                "legacy-schema target writer dry run was rejected or mutated the target:\n"
                + "\n".join(messages)
            )

        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=legacy_relative,
            lock_id=legacy_lock_id,
            snapshot=legacy_snapshot.relative_to(root).as_posix(),
            assignments=[],
            additions=[item for item in legacy_additions if not item.startswith("External State Schema=")],
            apply=False,
            **legacy_expectations,
        )
        if ok or audit is not None or not any("External State Schema Conflict" in item for item in messages):
            raise AssertionError(
                "legacy-schema target writer accepted a projection without the schema addition:\n"
                + "\n".join(messages)
            )

        ok, messages, audit = reconciler.reconcile_target(
            root=root,
            target=legacy_relative,
            lock_id=legacy_lock_id,
            snapshot=legacy_snapshot.relative_to(root).as_posix(),
            assignments=[],
            additions=legacy_additions,
            apply=True,
            **legacy_expectations,
        )
        migrated_legacy = legacy_target.read_bytes()
        if not ok or audit is None:
            raise AssertionError(
                "legacy-schema target writer apply was rejected:\n" + "\n".join(messages)
            )
        if not migrated_legacy.startswith(b"External State Schema: `external-state-v1`\n"):
            raise AssertionError("legacy-schema target writer did not place the live header at byte zero")
        if not migrated_legacy.endswith(legacy_body):
            raise AssertionError("legacy-schema target writer did not preserve the BOM-prefixed historical bytes")
        if migrated_legacy.index(b"Historical Receipt Boundary:") > migrated_legacy.index(b"\xef\xbb\xbf##"):
            raise AssertionError("legacy-schema target writer placed the boundary after historical bytes")
        post_failures = validator.validate_target_currentness(
            root,
            [legacy_relative],
            expected_target_sha256=sha256_file(legacy_target),
            expected_schema="external-state-v1",
            **{key: value for key, value in legacy_expectations.items() if key != "expected_target_sha256"},
        )
        if post_failures:
            raise AssertionError(
                "BOM-safe migrated target did not pass currentness validation:\n"
                + "\n".join(post_failures)
            )

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

    with tempfile.TemporaryDirectory(prefix="ndai-projection-set-semantics-") as temp_dir:
        _run_projection_set_semantic_fixtures(Path(temp_dir))

    with tempfile.TemporaryDirectory(prefix="ndai-ufd-owner-") as temp_dir:
        _run_ufd_owner_fixtures(Path(temp_dir))

    print(
        "Target-scoped external-state currentness fixture validation: PASS "
        "(24 canonical-UFD + 12 Element-to-Phase negative fixtures)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
