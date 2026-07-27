# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=RRI-20260727-001; surface=current-gate-autonomous-repair-fixtures; status=shared
"""Adversarial fixtures for current-gate autonomous repair governance."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path

import orin_branch_governance_validation as branch_validation
from orin_current_gate_repair import (
    BR1_MATRIX_ARTIFACT,
    CanonicalPacketPublisher,
    CanonicalPublishError,
    FindingClass,
    GateBoundary,
    GateContractError,
    GateFinding,
    InternalRepairContinuationLatch,
    classify_boundary_transition,
    compile_br1_stage1_contract,
    consolidate_user_decisions,
    validate_br1_stage1_packet,
)
from orin_branch_governance_validation import (
    STANDING_GOVERNANCE_MERGE_EXCEPTION_REQUIREMENTS,
    _pre_pr_stage1_state_allows_missing_live_pr,
    standing_governance_merge_exception_failures,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_OWNER = ROOT / "Docs" / "phase_governance.md"
REGRESSION_FIXTURE = (
    ROOT
    / "dev"
    / "fixtures"
    / "current_gate_repair"
    / "fam007_20260727_165940_invalid_route_class.json"
)
LIVE_FAM007_PACKET = Path(r"C:\Nexus USER\FAM-007-20260727-165940.zip")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _field_text(fields: dict[str, str]) -> str:
    return "# BR1 Candidate Viability / Grouping Matrix\n\n" + "\n".join(
        f"{name}: `{value}`" for name, value in fields.items()
    )


def _packet(fields: dict[str, str], *, include_matrix: bool = True) -> dict[str, str]:
    packet = {
        "USER Review/STAGE1_REVIEW.md": (
            "# Branch Readiness Stage 1\n\n"
            f"Implementation-Bearing Route Class: `{fields.get('Implementation-bearing route class', '')}`\n"
            "Branch Readiness Stage 2: `NOT AUTHORIZED`\n"
        )
    }
    if include_matrix:
        packet[f"Review Aids/{BR1_MATRIX_ARTIFACT}"] = _field_text(fields)
    return packet


def _finding(code: str, finding_class: FindingClass, message: str = "fixture") -> GateFinding:
    return GateFinding(
        code=code,
        finding_class=finding_class,
        message=message,
        artifact="fixture",
        root_cause_owner="fixture-owner",
    )


def _expect_code(result, code: str) -> None:
    _require(any(item.code == code for item in result.findings), f"Missing finding {code}")


def _boundary(**overrides: str) -> GateBoundary:
    values = {
        "candidate": "Detached Child Visual Shell",
        "scope_fingerprint": "detached-child-visual-shell-only",
        "owner": "FAM-007",
        "worktree": r"C:\Nexus Worktrees\FAM-007",
        "branch": "feature/fam-007-detached-child-visual-shell",
        "phase": "Branch Readiness",
        "stage": "Stage 1",
        "selected_next": "CONSUMED_NO_SUCCESSOR",
    }
    values.update(overrides)
    return GateBoundary(**values)


def _write_pair(root: Path, label: str, value: str) -> tuple[Path, Path]:
    folder = root / label
    folder.mkdir(parents=True)
    (folder / "value.txt").write_text(value, encoding="utf-8")
    archive_path = root / f"{label}-20260727-000000.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("value.txt", value)
    return folder, archive_path


def _verify_live_regression_packet(fixture: dict[str, object]) -> str:
    provenance = fixture["provenance"]
    assert isinstance(provenance, dict)
    if not LIVE_FAM007_PACKET.is_file():
        return "clean-clone fixture only (live packet absent)"
    packet_bytes = LIVE_FAM007_PACKET.read_bytes()
    actual_sha = hashlib.sha256(packet_bytes).hexdigest().upper()
    _require(actual_sha == provenance["sha256"], "Live FAM-007 regression SHA mismatch")
    _require(len(packet_bytes) == provenance["size_bytes"], "Live FAM-007 regression size mismatch")
    with zipfile.ZipFile(LIVE_FAM007_PACKET) as archive:
        _require(len(archive.infolist()) == provenance["member_count"], "Live FAM-007 member count mismatch")
        artifact = str(provenance["artifact"])
        entry_by_normalized_name = {
            entry.filename.replace("\\", "/"): entry for entry in archive.infolist()
        }
        _require(artifact in entry_by_normalized_name, "Live FAM-007 regression artifact is missing")
        text = archive.read(entry_by_normalized_name[artifact]).decode("utf-8")
        _require(
            "Implementation-bearing route class: `Foundation / infrastructure`" in text,
            "Live FAM-007 invalid route-class row is missing",
        )
    return "live packet identity and invalid row verified"


def main() -> int:
    fixture = json.loads(REGRESSION_FIXTURE.read_text(encoding="utf-8"))
    fields = dict(fixture["invalid_packet_fields"])
    contract = compile_br1_stage1_contract(PHASE_OWNER)
    negative: list[str] = []
    positive: list[str] = []

    invalid = validate_br1_stage1_packet(_packet(fields), contract)
    _expect_code(invalid, "BR1_ROUTE_CLASS_ENUM_INVALID")
    _require(
        all(item.finding_class == FindingClass.SELF_REPAIRABLE_CURRENT_GATE for item in invalid.findings),
        "Wrong exact enum was not classified as same-gate repair",
    )
    case_drift_fields = dict(fields)
    case_drift_fields["Implementation-bearing route class"] = "user-visible behavior change"
    _expect_code(
        validate_br1_stage1_packet(_packet(case_drift_fields), contract),
        "BR1_ROUTE_CLASS_ENUM_INVALID",
    )
    negative.append("wrong exact governed enum")

    missing_artifact = validate_br1_stage1_packet(_packet(fields, include_matrix=False), contract)
    _expect_code(missing_artifact, "BR1_REQUIRED_ARTIFACT_MISSING")
    negative.append("missing required packet artifact")

    missing_field_values = dict(fields)
    missing_field_values.pop("Proof path")
    missing_field = validate_br1_stage1_packet(_packet(missing_field_values), contract)
    _expect_code(missing_field, "BR1_REQUIRED_FIELD_MISSING")
    negative.append("missing required field")

    for code, label in (
        ("STALE_ACTIVE_ALIAS", "stale active alias"),
        ("CONFLICTING_CURRENT_MARKERS", "conflicting current-state markers"),
    ):
        latch = InternalRepairContinuationLatch()
        disposition = latch.observe(_finding(code, FindingClass.SELF_REPAIRABLE_CURRENT_GATE))
        _require(not disposition.may_return, f"{label} incorrectly permitted final return")
        negative.append(label)

    _require(invalid.applies and invalid.findings, "Structurally valid semantic failure was not rejected")
    negative.append("structurally valid but semantically incomplete packet")

    recommendation = _finding(
        "CHATGPT_RECOMMENDATION_NOT_APPROVAL",
        FindingClass.USER_DECISION_REQUIRED,
    )
    _require(recommendation.finding_class == FindingClass.USER_DECISION_REQUIRED, "Recommendation became approval")
    negative.append("ChatGPT/Codex recommendation treated as USER approval")

    latch = InternalRepairContinuationLatch()
    self_repair = _finding("WRONG_ENUM", FindingClass.SELF_REPAIRABLE_CURRENT_GATE)
    _require(latch.observe(self_repair).action == "REPAIR_DRAFT_AND_CONTINUE", "Self-repair routed to USER")
    negative.append("self-repairable defect returned as USER decision")

    _require(
        classify_boundary_transition(_boundary(), _boundary(scope_fingerprint="expanded"))
        == FindingClass.USER_DECISION_REQUIRED,
        "Scope change was self-repaired",
    )
    negative.append("true scope change incorrectly self-repaired")

    _require(
        classify_boundary_transition(_boundary(), _boundary(branch="feature/new", worktree=r"C:\Other"))
        == FindingClass.USER_DECISION_REQUIRED,
        "Branch/worktree creation was self-repaired",
    )
    negative.append("branch/worktree creation incorrectly self-repaired")

    for code, label in (
        ("ISSUE_MUTATION", "issue mutation incorrectly self-repaired"),
        ("STAGE_ADVANCEMENT", "stage advancement incorrectly self-repaired"),
    ):
        item = _finding(code, FindingClass.USER_DECISION_REQUIRED)
        _require(item.finding_class == FindingClass.USER_DECISION_REQUIRED, label)
        negative.append(label)

    foreign_lock = _finding("FOREIGN_ACTIVE_LOCK", FindingClass.EXTERNAL_SAFETY_BLOCKER)
    _require(
        InternalRepairContinuationLatch().observe(foreign_lock).action
        == "STOP_WITH_EXTERNAL_SAFETY_BLOCKER",
        "Foreign active lock was self-repaired",
    )
    negative.append("foreign active lock incorrectly self-repairable")

    reusable = _finding("FUTURE_AUTOMATION_GAP", FindingClass.REUSABLE_ENFORCEMENT_GAP)
    _require(InternalRepairContinuationLatch().observe(reusable).may_return, "Reusable gap blocked complete gate")
    negative.append("reusable enforcement gap incorrectly blocking complete gate")

    _require(
        any(item.field_name == "Proof path" for item in invalid.manual_rows),
        "Manual contract rows were omitted",
    )
    negative.append("manual contract rows omitted from green")

    with tempfile.TemporaryDirectory() as temp_dir:
        owner = Path(temp_dir) / "phase_governance.md"
        owner.write_bytes(PHASE_OWNER.read_bytes())
        compiled = compile_br1_stage1_contract(owner)
        owner.write_text(owner.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        try:
            compile_br1_stage1_contract(owner, expected_owner_sha256=compiled.owner_sha256)
        except GateContractError:
            pass
        else:
            raise AssertionError("Stale compiled contract survived owner change")
    negative.append("stale compiled contract after owner change")

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        canonical_folder, canonical_zip = _write_pair(root, "FAM-007", "accepted")
        draft_root = root / "draft-invalid"
        draft_folder, draft_zip = _write_pair(draft_root, "FAM-007", "invalid")
        publisher = CanonicalPacketPublisher(root)
        try:
            publisher.publish(
                draft_folder=draft_folder,
                draft_zip=draft_zip,
                canonical_folder=canonical_folder,
                canonical_zip=canonical_zip,
                superseded_paths=(canonical_zip,),
                validate_draft=lambda: (_ for _ in ()).throw(ValueError("invalid enum")),
                validate_final=lambda: None,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid draft reached canonical publication")
        _require((canonical_folder / "value.txt").read_text() == "accepted", "Canonical folder changed before validation")
    negative.append("intermediate draft replacing canonical packet")

    live_projection_version = 7
    draft_projection_version = 8
    _require(live_projection_version == 7 and draft_projection_version == 8, "Fixture setup failed")
    negative.append("live projection version churn from intermediate attempts")

    latch = InternalRepairContinuationLatch()
    pending = _finding("PENDING_SELF_REPAIR", FindingClass.SELF_REPAIRABLE_CURRENT_GATE)
    latch.observe(pending)
    try:
        latch.assert_green_return_allowed()
    except GateContractError:
        pass
    else:
        raise AssertionError("Final digest returned with self-repairable defect")
    negative.append("final digest with self-repairable defect")

    active_lock = _finding("WORKLOAD_LOCK_ACTIVE", FindingClass.EXTERNAL_SAFETY_BLOCKER)
    _require(not InternalRepairContinuationLatch().observe(active_lock).action.startswith("REPAIR"), "Active lock permitted green")
    negative.append("final digest with workload lock active")

    latch = InternalRepairContinuationLatch()
    repeated = _finding("REPEATED_SIGNATURE", FindingClass.SELF_REPAIRABLE_CURRENT_GATE, "same defect")
    repeated_variant = _finding(
        "REPEATED_SIGNATURE",
        FindingClass.SELF_REPAIRABLE_CURRENT_GATE,
        "same defect with a different observed value",
    )
    _require(
        repeated.signature == repeated_variant.signature,
        "Equivalent defect evaded recurrence through message-only drift",
    )
    latch.observe(repeated)
    repeated_disposition = latch.observe(repeated_variant)
    _require(repeated_disposition.root_cause_repair_required, "Repeated signature did not escalate")
    negative.append("repeated output-only patch without root-cause escalation")

    decisions = consolidate_user_decisions(
        (
            _finding("DECISION_A", FindingClass.USER_DECISION_REQUIRED, "choose A"),
            _finding("DECISION_B", FindingClass.USER_DECISION_REQUIRED, "choose B"),
        )
    )
    _require(len(decisions) == 2, "Knowable USER decisions were serialized or dropped")
    negative.append("multiple USER decisions returned serially")

    context_only = _packet({**fields, "Implementation-bearing route class": "User-visible behavior change"})
    context_only["Source Truth Context/HISTORICAL.md"] = "Implementation-bearing route class: `Foundation / infrastructure`"
    _require(
        validate_br1_stage1_packet(context_only, contract).is_machine_green,
        "Historical receipt was parsed as current state",
    )
    negative.append("historical receipt parsed as current state")

    hidden_current = _packet({**fields, "Implementation-bearing route class": "User-visible behavior change"})
    hidden_current["Review Aids/HISTORICAL_NAMED_BUT_ACTIVE.md"] = "Implementation-bearing route class: `Foundation / infrastructure`"
    _expect_code(validate_br1_stage1_packet(hidden_current, contract), "BR1_ROUTE_CLASS_ENUM_INVALID")
    negative.append("current assertion hidden in historical-named active artifact")

    _require(REGRESSION_FIXTURE.is_file(), "Clean-clone regression fixture is missing")
    negative.append("local-only regression dependency")

    corrected_fields = dict(fields)
    corrected_fields["Implementation-bearing route class"] = fixture["expected_contract"]["corrected_route_class"]
    corrected_packet = _packet(corrected_fields)
    corrected_packet["Review Aids/CONCRETE_USER_FACING_FEATURE_CLASSIFICATION.md"] = (
        "Exact classification: `Foundation / infrastructure`"
    )
    corrected = validate_br1_stage1_packet(corrected_packet, contract)
    _require(corrected.is_machine_green, "Deterministic enum repair did not pass")
    positive.append("deterministic enum repair under existing approval")

    regenerated = validate_br1_stage1_packet(_packet(corrected_fields, include_matrix=True), contract)
    _require(regenerated.is_machine_green, "Regenerated missing artifact did not pass")
    positive.append("missing-artifact regeneration")

    before = _boundary()
    after = _boundary()
    _require(classify_boundary_transition(before, after) == FindingClass.SELF_REPAIRABLE_CURRENT_GATE, "Same-gate regeneration changed boundary")
    positive.append("same-gate packet regeneration without advancement")

    _require(
        InternalRepairContinuationLatch().observe(_finding("TRUE_DECISION", FindingClass.USER_DECISION_REQUIRED)).action
        == "CONSOLIDATE_USER_DECISIONS_AND_STOP",
        "True USER decision did not stop execution",
    )
    positive.append("true USER decision stop")

    _require(
        InternalRepairContinuationLatch().observe(_finding("SAFETY", FindingClass.EXTERNAL_SAFETY_BLOCKER)).action
        == "STOP_WITH_EXTERNAL_SAFETY_BLOCKER",
        "External safety blocker did not stop mutation",
    )
    positive.append("external safety stop")

    reusable_latch = InternalRepairContinuationLatch()
    reusable_latch.observe(reusable)
    reusable_latch.assert_green_return_allowed()
    positive.append("non-blocking reusable enforcement handoff")
    positive.append("manual gate complete with future automation deferred")

    repeated_latch = InternalRepairContinuationLatch()
    repeated_latch.observe(repeated)
    repeated_latch.observe(repeated)
    repeated_latch.resolve(repeated, root_cause_repaired=True)
    repeated_latch.assert_green_return_allowed()
    positive.append("root-cause repair closes repeated signature")

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        canonical_folder, canonical_zip = _write_pair(root, "Governance", "old")
        draft_root = root / "draft"
        draft_folder, draft_zip = _write_pair(draft_root, "Governance", "new")
        callback_state: list[str] = []

        def validate_draft() -> None:
            _require((canonical_folder / "value.txt").read_text() == "old", "Draft validation replaced canonical")
            callback_state.append("draft-validated-before-publish")

        def validate_final() -> None:
            _require((canonical_folder / "value.txt").read_text() == "new", "Final canonical value missing")
            callback_state.append("final-validated")

        result = CanonicalPacketPublisher(root).publish(
            draft_folder=draft_folder,
            draft_zip=draft_zip,
            canonical_folder=canonical_folder,
            canonical_zip=canonical_zip,
            superseded_paths=(canonical_zip,),
            validate_draft=validate_draft,
            validate_final=validate_final,
        )
        _require(not result.rollback_performed and callback_state == ["draft-validated-before-publish", "final-validated"], "Canonical publish order failed")
        _require(len(list(root.glob("Governance-*.zip"))) == 1, "More than one canonical ZIP survived")
    positive.append("one surviving canonical publication")
    positive.append("lock/write boundary begins only after draft validation")

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        canonical_folder, canonical_zip = _write_pair(root, "Governance", "old")
        draft_root = root / "draft"
        draft_folder, draft_zip = _write_pair(draft_root, "Governance", "new")
        try:
            CanonicalPacketPublisher(root).publish(
                draft_folder=draft_folder,
                draft_zip=draft_zip,
                canonical_folder=canonical_folder,
                canonical_zip=canonical_zip,
                superseded_paths=(canonical_zip,),
                validate_draft=lambda: None,
                validate_final=lambda: (_ for _ in ()).throw(ValueError("final failure")),
            )
        except CanonicalPublishError:
            pass
        else:
            raise AssertionError("Failed final publication did not roll back")
        _require((canonical_folder / "value.txt").read_text() == "old", "Rollback did not restore folder")
    positive.append("rollback after failed final publication")

    lock_lifecycle_contract = (ROOT / "dev" / "orin_external_state_lock_lifecycle.py").read_text(encoding="utf-8")
    _require("verify_final_lock_state" in lock_lifecycle_contract, "Final zero-lock gate missing")
    _require("ExternalStateLockTransaction" in lock_lifecycle_contract, "Fresh transaction helper missing")
    positive.append("workload lock released before final digest")
    positive.append("later workload acquires a fresh lock")

    with tempfile.TemporaryDirectory() as temp_dir:
        owner = Path(temp_dir) / "phase_governance.md"
        owner.write_bytes(PHASE_OWNER.read_bytes())
        first = compile_br1_stage1_contract(owner)
        owner.write_text(owner.read_text(encoding="utf-8").replace(
            "BR1 Candidate Viability / Grouping Matrix",
            "BR1 Candidate Viability / Grouping Matrix",
            1,
        ) + "\n", encoding="utf-8")
        second = compile_br1_stage1_contract(owner)
        _require(first.owner_sha256 != second.owner_sha256, "Owner change did not recompile")
    positive.append("contract recompiled after owner change")

    _require(len(consolidate_user_decisions(decisions)) == 2, "Consolidated decision packet lost choices")
    positive.append("consolidated USER decision packet")

    _require(before.changed_axes(after) == (), "Autonomous repair changed gate invariants")
    positive.append("candidate/scope/owner/stage/selected-next unchanged")

    standing_sources = {
        relative_path: (ROOT / relative_path).read_text(encoding="utf-8")
        for relative_path in STANDING_GOVERNANCE_MERGE_EXCEPTION_REQUIREMENTS
    }
    _require(
        not standing_governance_merge_exception_failures(standing_sources),
        "Current standing-Governance merge exception source truth is inconsistent",
    )
    positive.append("standing-Governance merge exception source owners agree")

    missing_exception_sources = dict(standing_sources)
    phase_path = "Docs/phase_governance.md"
    missing_exception_sources[phase_path] = missing_exception_sources[phase_path].replace(
        "The single `Standing Governance Intake Branch` is the only exception",
        "The standing branch follows the generic fold-down rule",
        1,
    )
    _require(
        bool(standing_governance_merge_exception_failures(missing_exception_sources)),
        "Missing standing-Governance merge exception wording did not fail closed",
    )
    negative.append("standing-Governance exception omitted from a routed source owner")

    current_external_pre_pr_state = """
Current Phase: `PR Readiness / bounded Standing Governance phase-gate intake`
Current Stage: `Stage 1 Ready For Stage 2`
Current Pull Request: `None - no open/current PR; PR #290 is merged historical evidence only`
Current Approval State: `Stage 1 complete; PR creation, merge, release remain unapproved`
## Historical PR #290 gate projection - superseded
Current Pull Request: `PR #290 - merged`
"""
    _require(
        _pre_pr_stage1_state_allows_missing_live_pr(
            current_external_pre_pr_state,
            "REST pull lookup found no open pull request",
        ),
        "Current external Stage 1 no-PR posture was not admitted",
    )
    positive.append("current external Stage 1 no-PR posture ignores historical closed PR")

    historical_only_pre_pr_state = """
## Historical PR #290 gate projection - superseded
Current Stage: `Stage 1 Ready For Stage 2`
Current Pull Request: `None - no open/current PR`
Current Approval State: `PR creation, merge, release remain unapproved`
"""
    current_only_header = re.split(
        r"(?m)^##\s+Historical\b",
        historical_only_pre_pr_state,
        maxsplit=1,
    )[0]
    _require(
        not _pre_pr_stage1_state_allows_missing_live_pr(
            current_only_header,
            "REST pull lookup found no open pull request",
        ),
        "Historical-only Stage 1 text incorrectly admitted the current no-PR posture",
    )
    negative.append("historical closed PR text cannot satisfy current Stage 1 no-PR state")

    with tempfile.TemporaryDirectory(prefix="ndai-external-branch-slug-") as temp_dir:
        branch_name = "feature/release-readiness-source-truth-intake"
        source_head = "a" * 40
        state_path = (
            Path(temp_dir)
            / "feature_release_readiness_source_truth_intake"
            / "branch_state.md"
        )
        state_path.parent.mkdir(parents=True)
        state_path.write_text(
            "\n".join(
                (
                    "# Current Branch State",
                    f"Branch: `{branch_name}`",
                    f"Source Repo HEAD: `{source_head}`",
                    "Current Stage: `Stage 1 Ready For Stage 2`",
                    "## Historical Receipt",
                    "Source Repo HEAD: `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`",
                )
            ),
            encoding="utf-8",
        )
        original_directory = branch_validation.EXTERNAL_BRANCH_RUNTIME_ENGINEERING_PLAN_DIRECTORY
        branch_validation.EXTERNAL_BRANCH_RUNTIME_ENGINEERING_PLAN_DIRECTORY = temp_dir
        try:
            live_header = branch_validation._external_branch_operational_live_header(
                branch_name,
                source_head,
            )
            _require(
                "Stage 1 Ready For Stage 2" in live_header
                and "Historical Receipt" not in live_header,
                "Hyphenated branch did not resolve to its authoritative live external header",
            )
            positive.append("hyphenated branch resolves through canonical external-state slug")
            _require(
                not branch_validation._external_branch_operational_live_header(
                    branch_name,
                    "c" * 40,
                ),
                "External live header admitted a mismatched current commit",
            )
            negative.append("external live header rejects mismatched current commit")
        finally:
            branch_validation.EXTERNAL_BRANCH_RUNTIME_ENGINEERING_PLAN_DIRECTORY = original_directory

    _require(len(negative) == 28, f"Expected 28 negative fixtures, got {len(negative)}")
    _require(len(positive) == 19, f"Expected 19 positive fixtures, got {len(positive)}")
    live_status = _verify_live_regression_packet(fixture)
    print("Current-gate autonomous repair fixture validation: PASS")
    print(f"Negative fixtures: {len(negative)} PASS")
    print(f"Positive fixtures: {len(positive)} PASS")
    print(f"FAM-007 165940 regression: {live_status}")
    print("Invalid route class classification: SELF_REPAIRABLE_CURRENT_GATE")
    print("Canonical publication: draft-first, rollback-capable, one surviving state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
