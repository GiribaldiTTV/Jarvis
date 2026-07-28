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
    return "# BR1 Candidate Viability / Grouping Matrix\n\n" + _field_lines(fields)


def _field_lines(fields: dict[str, str]) -> str:
    return "\n".join(
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


def _finding(
    code: str,
    finding_class: FindingClass,
    message: str = "fixture",
    *,
    defect_key: str = "",
) -> GateFinding:
    return GateFinding(
        code=code,
        finding_class=finding_class,
        message=message,
        artifact="fixture",
        root_cause_owner="fixture-owner",
        defect_key=defect_key,
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

    identity_only_packet = {
        "USER Review/STAGE1_REVIEW.md": (
            "# Branch Readiness Stage 1\n\n"
            "Branch Readiness Stage 2: `NOT AUTHORIZED`\n"
        )
    }
    identity_only_result = validate_br1_stage1_packet(identity_only_packet, contract)
    _expect_code(identity_only_result, "BR1_REQUIRED_ARTIFACT_MISSING")
    negative.append("independent Stage 1 identity cannot hide a missing matrix")

    future_stage1_packet = {
        "USER Review/CURRENT_REVIEW.md": (
            "# Live Validation Review\n\n"
            "Next Legal Phase: `Branch Readiness Stage 1`\n"
        )
    }
    future_stage1_result = validate_br1_stage1_packet(future_stage1_packet, contract)
    _require(
        not future_stage1_result.applies and not future_stage1_result.findings,
        "A future Branch Readiness Stage 1 reference was misclassified as the current gate",
    )
    positive.append("future Stage 1 wording does not activate the BR1 contract")

    missing_field_values = dict(fields)
    missing_field_values.pop("Proof path")
    missing_field = validate_br1_stage1_packet(_packet(missing_field_values), contract)
    _expect_code(missing_field, "BR1_REQUIRED_FIELD_MISSING")
    negative.append("missing required field")

    ordinary_fields = dict(fields)
    ordinary_fields.pop("Platform Contract Adoption Matrix when applicable")
    ordinary_fields.pop("Repo-Wide Migration Neutralization Proof when applicable")
    ordinary_result = validate_br1_stage1_packet(_packet(ordinary_fields), contract)
    _require(
        not any(
            finding.code == "BR1_REQUIRED_FIELD_MISSING"
            and "when applicable" in finding.message
            for finding in ordinary_result.findings
        ),
        "Inapplicable conditional BR1 fields were enforced as unconditional requirements",
    )
    positive.append("inapplicable conditional BR1 fields may be omitted")

    for field_name, trigger_field, trigger_value, label in (
        (
            "Platform Contract Adoption Matrix when applicable",
            "Dependency Scope Class",
            "Platform contract adoption required for the shared surface.",
            "applicable platform contract matrix is required",
        ),
        (
            "Repo-Wide Migration Neutralization Proof when applicable",
            "Dependency Scope Class",
            "Repo-wide migration required across active carriers.",
            "applicable repo-wide migration proof is required",
        ),
    ):
        applicable_fields = dict(fields)
        applicable_fields.pop(field_name)
        applicable_fields[trigger_field] = trigger_value
        applicable_result = validate_br1_stage1_packet(_packet(applicable_fields), contract)
        _require(
            any(
                finding.code == "BR1_REQUIRED_FIELD_MISSING"
                and field_name in finding.message
                for finding in applicable_result.findings
            ),
            f"{label} did not fail closed",
        )
        negative.append(label)

    for field_name, negated_triggers in (
        (
            "Platform Contract Adoption Matrix when applicable",
            (
                "No platform contract applies to this isolated candidate.",
                "Platform contract is not applicable to this isolated candidate.",
            ),
        ),
        (
            "Repo-Wide Migration Neutralization Proof when applicable",
            (
                "No repo-wide migration is planned for this bounded candidate.",
                "Repo-wide migration is not planned for this bounded candidate.",
            ),
        ),
    ):
        for negated_trigger in negated_triggers:
            negated_fields = dict(fields)
            negated_fields.pop(field_name)
            negated_fields["Dependency Scope Class"] = negated_trigger
            negated_result = validate_br1_stage1_packet(_packet(negated_fields), contract)
            _require(
                not any(
                    finding.code == "BR1_REQUIRED_FIELD_MISSING"
                    and field_name in finding.message
                    for finding in negated_result.findings
                ),
                f"Bounded negation incorrectly activated {field_name}: {negated_trigger}",
            )
    positive.append("pre-term and post-term negation preserve conditional non-applicability")

    incomplete_second_candidate = _packet(fields)
    matrix_path = f"Review Aids/{BR1_MATRIX_ARTIFACT}"
    incomplete_second_candidate[matrix_path] += (
        "\n\nOption name: `Incomplete second candidate`\n"
        "Implementation-bearing route class: `User-visible behavior change`\n"
    )
    second_candidate_result = validate_br1_stage1_packet(
        incomplete_second_candidate,
        contract,
    )
    _require(
        any(
            finding.code == "BR1_REQUIRED_FIELD_MISSING"
            and "Incomplete second candidate" in finding.message
            and "Proof path" in finding.message
            for finding in second_candidate_result.findings
        ),
        "A complete first BR1 option masked missing fields in a later candidate",
    )
    negative.append("each BR1 matrix candidate requires its own complete field set")

    section_bounded_fields = dict(fields)
    section_bounded_fields.pop("Proof path")
    section_bounded_packet = _packet(section_bounded_fields)
    section_bounded_packet[matrix_path] = section_bounded_packet[matrix_path].replace(
        "# BR1 Candidate Viability / Grouping Matrix",
        "# Candidate Matrix With A Malformed Heading",
        1,
    )
    section_bounded_packet[matrix_path] += (
        "\n\n## Packet Summary\n"
        "Proof path: `This belongs to the summary, not the candidate.`\n"
    )
    section_bounded_result = validate_br1_stage1_packet(
        section_bounded_packet,
        contract,
    )
    _require(
        any(
            finding.code == "BR1_REQUIRED_FIELD_MISSING"
            and "Proof path" in finding.message
            for finding in section_bounded_result.findings
        ),
        "The last BR1 candidate borrowed a required field from a later Markdown section",
    )
    negative.append("candidate fields stop at the next Markdown section boundary")

    valid_candidate_fields = dict(fields)
    valid_candidate_fields["Implementation-bearing route class"] = (
        "User-visible behavior change"
    )
    _require(
        len(contract.invalid_candidate_shapes) == 11,
        "Invalid candidate shapes were not compiled as exact source-owner entries",
    )
    for invalid_only_shape in (
        "planning-only",
        "readiness-only",
        "support-only",
        "infrastructure-only",
        "manifest-only",
        "registry-only",
        "proof-only",
    ):
        invalid_shape_fields = dict(valid_candidate_fields)
        invalid_shape_fields["Main feature/package objective"] = (
            f"This is a {invalid_only_shape} branch."
        )
        invalid_shape_result = validate_br1_stage1_packet(
            _packet(invalid_shape_fields),
            contract,
        )
        _expect_code(invalid_shape_result, "BR1_INVALID_CANDIDATE_SHAPE")
        negative.append(f"explicit {invalid_only_shape} candidate shape")

    for invalid_shape_text, invalid_shape_label in (
        ("This is a setup-only branch.", "setup-only without exact USER action gate"),
        (
            "This candidate's purpose is to choose later candidates.",
            "candidate whose purpose is to choose later candidates",
        ),
        (
            "This candidate defers every concrete deliverable to another branch.",
            "candidate that defers every concrete deliverable",
        ),
    ):
        invalid_shape_fields = dict(valid_candidate_fields)
        invalid_shape_fields["Main feature/package objective"] = invalid_shape_text
        invalid_shape_result = validate_br1_stage1_packet(
            _packet(invalid_shape_fields),
            contract,
        )
        _expect_code(invalid_shape_result, "BR1_INVALID_CANDIDATE_SHAPE")
        negative.append(invalid_shape_label)

    negated_shape_fields = dict(valid_candidate_fields)
    negated_shape_fields["Main feature/package objective"] = (
        "This is not a planning-only branch; it implements visible shell behavior."
    )
    negated_shape_result = validate_br1_stage1_packet(
        _packet(negated_shape_fields),
        contract,
    )
    _require(
        not any(
            finding.code == "BR1_INVALID_CANDIDATE_SHAPE"
            for finding in negated_shape_result.findings
        ),
        "Negated invalid-shape wording was treated as an affirmative invalid candidate",
    )
    positive.append("negated invalid-shape wording remains non-applicable")

    gated_setup_fields = dict(valid_candidate_fields)
    gated_setup_fields["Main feature/package objective"] = "This is a setup-only branch."
    gated_setup_fields["Exact USER decision needed"] = (
        "Exact USER action gate authorizes the named setup behavior only."
    )
    gated_setup_result = validate_br1_stage1_packet(
        _packet(gated_setup_fields),
        contract,
    )
    _require(
        not any(
            finding.code == "BR1_INVALID_CANDIDATE_SHAPE"
            for finding in gated_setup_result.findings
        ),
        "Setup-only candidate with an exact USER action gate was rejected",
    )
    positive.append("setup-only candidate preserves the exact USER action-gate exception")

    subordinate_support_fields = dict(valid_candidate_fields)
    subordinate_support_fields["Main feature/package objective"] = (
        "Deliver visible runtime behavior while grouping support-only scripts into the package."
    )
    subordinate_support_fields["Support / infrastructure relationship"] = (
        "Support-only scripts are subordinate implementation work inside the runtime package."
    )
    subordinate_support_result = validate_br1_stage1_packet(
        _packet(subordinate_support_fields),
        contract,
    )
    _require(
        not any(
            finding.code == "BR1_INVALID_CANDIDATE_SHAPE"
            for finding in subordinate_support_result.findings
        ),
        "Subordinate support-only work misclassified the whole candidate as support-only",
    )
    positive.append("subordinate support-only work does not classify the whole candidate")
    _require(
        any(
            row.field_name == "Invalid Candidate Shapes"
            for row in negated_shape_result.manual_rows
        ),
        "Compiled invalid candidate shapes were not exposed for substantive manual review",
    )

    unnamed_first_candidate_fields = dict(valid_candidate_fields)
    unnamed_first_candidate_fields.pop("Option name")
    unnamed_first_candidate_fields["Implementation-bearing route class"] = (
        "Foundation / infrastructure"
    )
    malformed_first_candidate = _packet(valid_candidate_fields)
    malformed_first_candidate[matrix_path] = (
        "# BR1 Candidate Viability / Grouping Matrix\n\n"
        f"{_field_lines(unnamed_first_candidate_fields)}\n\n"
        f"{_field_lines(valid_candidate_fields)}\n"
    )
    malformed_first_result = validate_br1_stage1_packet(
        malformed_first_candidate,
        contract,
    )
    _require(
        any(
            finding.code == "BR1_REQUIRED_FIELD_MISSING"
            and "candidate 1" in finding.message
            and "Option name" in finding.message
            for finding in malformed_first_result.findings
        )
        and any(
            finding.code == "BR1_ROUTE_CLASS_ENUM_INVALID"
            and "candidate 1" in finding.message
            for finding in malformed_first_result.findings
        ),
        "Governed fields before the first Option name boundary were discarded",
    )
    negative.append("pre-boundary candidate fields cannot be discarded")

    duplicate_route_candidate = _packet(fields)
    duplicate_route_candidate[matrix_path] += (
        "\nImplementation-bearing route class: `Maintenance / tooling / validation`\n"
    )
    duplicate_route_result = validate_br1_stage1_packet(
        duplicate_route_candidate,
        contract,
    )
    _expect_code(duplicate_route_result, "BR1_ROUTE_CLASS_DUPLICATE")
    negative.append("each BR1 candidate requires exactly one route class")

    two_missing_fields = dict(fields)
    two_missing_fields.pop("Proof path")
    two_missing_fields.pop("Blockers")
    two_missing_result = validate_br1_stage1_packet(_packet(two_missing_fields), contract)
    missing_findings = [
        finding
        for finding in two_missing_result.findings
        if finding.code == "BR1_REQUIRED_FIELD_MISSING"
        and ("Proof path" in finding.message or "Blockers" in finding.message)
    ]
    _require(
        len(missing_findings) == 2
        and len({finding.signature for finding in missing_findings}) == 2,
        "Distinct missing fields collided on one continuation signature",
    )
    signature_latch = InternalRepairContinuationLatch()
    signature_dispositions = [
        signature_latch.observe(finding) for finding in missing_findings
    ]
    _require(
        all(disposition.occurrence == 1 for disposition in signature_dispositions),
        "A distinct missing field was misclassified as a repeated defect",
    )
    negative.append("distinct field defects retain distinct repair signatures")

    placeholder_candidate_fields = dict(fields)
    placeholder_candidate_fields["Option name"] = "TBD"
    placeholder_candidate_fields.pop("Proof path")
    placeholder_result = validate_br1_stage1_packet(
        _packet(placeholder_candidate_fields),
        contract,
    )
    placeholder_finding = next(
        finding
        for finding in placeholder_result.findings
        if finding.code == "BR1_REQUIRED_FIELD_MISSING"
        and "Proof path" in finding.message
    )
    named_candidate_fields = dict(placeholder_candidate_fields)
    named_candidate_fields["Option name"] = "Named candidate"
    named_result = validate_br1_stage1_packet(_packet(named_candidate_fields), contract)
    named_finding = next(
        finding
        for finding in named_result.findings
        if finding.code == "BR1_REQUIRED_FIELD_MISSING"
        and "Proof path" in finding.message
    )
    _require(
        placeholder_finding.signature == named_finding.signature,
        "Option-name repair reset the unchanged candidate-field defect signature",
    )
    stable_candidate_latch = InternalRepairContinuationLatch()
    stable_candidate_latch.observe(placeholder_finding)
    _require(
        stable_candidate_latch.observe(named_finding).root_cause_repair_required,
        "Unchanged candidate-field defect did not escalate after option-name repair",
    )
    negative.append("candidate display-name repair cannot reset a recurring defect")

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

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        canonical_folder, canonical_zip = _write_pair(root, "FAM-007", "accepted")
        draft_root = root / "draft-valid"
        draft_folder, draft_zip = _write_pair(draft_root, "FAM-007", "replacement")
        superseded_directory = root / "FAM-007-20260727-123456.zip"
        superseded_directory.mkdir()
        marker = superseded_directory / "preserve.txt"
        marker.write_text("unrelated extracted directory", encoding="utf-8")
        publisher = CanonicalPacketPublisher(root)
        try:
            publisher.publish(
                draft_folder=draft_folder,
                draft_zip=draft_zip,
                canonical_folder=canonical_folder,
                canonical_zip=canonical_zip,
                superseded_paths=(canonical_zip, superseded_directory),
                validate_draft=lambda: None,
                validate_final=lambda: None,
            )
        except CanonicalPublishError as exc:
            _require(
                "must be a regular file" in str(exc),
                "Non-file superseded ZIP blocked for the wrong reason",
            )
        else:
            raise AssertionError("ZIP-named superseded directory reached publication")
        _require(
            marker.read_text(encoding="utf-8") == "unrelated extracted directory",
            "ZIP-named superseded directory was modified or removed",
        )
        _require(
            (canonical_folder / "value.txt").read_text(encoding="utf-8") == "accepted",
            "Canonical packet changed before non-file superseded path rejection",
        )
    negative.append("non-file superseded ZIP path reached canonical publication")

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
    same_code_decisions = consolidate_user_decisions(
        (
            _finding(
                "DECISION_SHARED",
                FindingClass.USER_DECISION_REQUIRED,
                "choose alpha",
            ),
            _finding(
                "DECISION_SHARED",
                FindingClass.USER_DECISION_REQUIRED,
                "choose beta",
            ),
        )
    )
    _require(
        len(same_code_decisions) == 2,
        "Distinct USER decisions sharing a code were consolidated away",
    )
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

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        canonical_folder, canonical_zip = _write_pair(root, "Governance", "old")
        draft_root = root / "draft"
        draft_folder, draft_zip = _write_pair(draft_root, "Governance", "new")
        interrupted = False

        def interrupt_after_first_backup(stage: str, _source: Path, _destination: Path) -> None:
            nonlocal interrupted
            if stage == "backup" and not interrupted:
                interrupted = True
                raise SystemExit("simulated canonical publication process exit")

        try:
            CanonicalPacketPublisher(root, after_move=interrupt_after_first_backup).publish(
                draft_folder=draft_folder,
                draft_zip=draft_zip,
                canonical_folder=canonical_folder,
                canonical_zip=canonical_zip,
                superseded_paths=(canonical_zip,),
                validate_draft=lambda: None,
                validate_final=lambda: None,
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("Canonical publication interruption fixture did not exit")
        _require(
            any(root.glob(".canonical-publish-*")),
            "Interrupted publication did not preserve its durable transaction",
        )
        try:
            CanonicalPacketPublisher(root).publish(
                draft_folder=draft_folder,
                draft_zip=draft_zip,
                canonical_folder=canonical_folder,
                canonical_zip=canonical_zip,
                superseded_paths=(canonical_zip,),
                validate_draft=lambda: None,
                validate_final=lambda: None,
            )
        except CanonicalPublishError as exc:
            _require(
                "owner process is still active" in str(exc),
                "Active interrupted publication blocked for the wrong reason",
            )
        else:
            raise AssertionError("A second publisher recovered an active transaction")
        negative.append("interrupted canonical publication cannot strand hidden prior state")

        recovered = CanonicalPacketPublisher(
            root,
            process_checker=lambda _pid: False,
        ).publish(
            draft_folder=draft_folder,
            draft_zip=draft_zip,
            canonical_folder=canonical_folder,
            canonical_zip=canonical_zip,
            superseded_paths=(canonical_zip,),
            validate_draft=lambda: _require(
                (canonical_folder / "value.txt").read_text() == "old",
                "Interrupted publication did not restore prior canonical state before retry",
            ),
            validate_final=lambda: None,
        )
        _require(
            not recovered.rollback_performed
            and (canonical_folder / "value.txt").read_text() == "new"
            and not any(root.glob(".canonical-publish-*")),
            "Recovered canonical publication did not produce one clean final pair",
        )
        positive.append("next invocation recovers interrupted canonical publication")

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        canonical_folder, canonical_zip = _write_pair(root, "Governance", "old")
        draft_root = root / "draft"
        draft_folder, draft_zip = _write_pair(draft_root, "Governance", "committed")

        def interrupt_after_commit(stage: str, _source: Path, _destination: Path) -> None:
            if stage == "commit":
                raise SystemExit("simulated exit after canonical commit")

        try:
            CanonicalPacketPublisher(root, after_move=interrupt_after_commit).publish(
                draft_folder=draft_folder,
                draft_zip=draft_zip,
                canonical_folder=canonical_folder,
                canonical_zip=canonical_zip,
                superseded_paths=(canonical_zip,),
                validate_draft=lambda: None,
                validate_final=lambda: None,
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("Committed canonical interruption fixture did not exit")
        CanonicalPacketPublisher(
            root,
            process_checker=lambda _pid: False,
        )._recover_orphaned_transactions()
        _require(
            (canonical_folder / "value.txt").read_text() == "committed"
            and not any(root.glob(".canonical-publish-*")),
            "Committed canonical recovery did not preserve the validated publication",
        )

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
                    "Record Class: `Live Branch Projection`",
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

            state_path.write_text(
                "\n".join(
                    (
                        "# Historical Branch State",
                        "Record Class: `Historical Receipt`",
                        f"Branch: `{branch_name}`",
                        f"Source Repo HEAD: `{source_head}`",
                        "Current Stage: `Stage 1 Ready For Stage 2`",
                        "Current Pull Request: `None - no open/current PR`",
                        "Current Approval State: `PR creation, merge, release remain unapproved`",
                    )
                ),
                encoding="utf-8",
            )
            _require(
                not branch_validation._external_branch_operational_live_header(
                    branch_name,
                    source_head,
                ),
                "Historical external branch projection was admitted as live pre-PR state",
            )
            negative.append("historical external projection cannot satisfy live pre-PR state")
        finally:
            branch_validation.EXTERNAL_BRANCH_RUNTIME_ENGINEERING_PLAN_DIRECTORY = original_directory

    _require(len(negative) == 50, f"Expected 50 negative fixtures, got {len(negative)}")
    _require(len(positive) == 26, f"Expected 26 positive fixtures, got {len(positive)}")
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
