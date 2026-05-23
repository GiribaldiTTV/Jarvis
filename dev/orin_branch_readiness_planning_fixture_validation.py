# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=branch-readiness-planning-fixture-validator; status=shared
"""Regression fixtures for Branch Readiness product-system planning.

The governance validator is intentionally broad and source-truth heavy. This
fixture helper keeps one small regression seam focused on the failure pattern
where a broad implementation branch reaches a later phase with marker-only
planning.
"""

from __future__ import annotations

from pathlib import Path

import orin_branch_governance_validation as governance


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "dev" / "fixtures" / "branch_readiness_planning"
SHALLOW_FIXTURE = FIXTURE_DIR / "shallow_live_validation_product_plan.md"
CONCRETE_FIXTURE = FIXTURE_DIR / "concrete_live_validation_product_plan.md"
VALID_BRANCH_RUNTIME_PLAN_FIXTURE = (
    FIXTURE_DIR / "valid_branch_runtime_engineering_plan.md"
)
SHALLOW_BRANCH_RUNTIME_PLAN_FIXTURE = (
    FIXTURE_DIR / "shallow_branch_runtime_engineering_plan.md"
)
BACKLOG_SPRAWL_FIXTURE = FIXTURE_DIR / "invalid_backlog_planning_sprawl.md"
FOLD_DOWN_FIXTURE = FIXTURE_DIR / "valid_pr_fold_down_packet.md"
VALID_BRANCH_VISION_CONTRACT_FIXTURE = (
    FIXTURE_DIR / "valid_branch_vision_contract_snapshot.md"
)
INVALID_PROPOSED_BRANCH_VISION_CONTRACT_FIXTURE = (
    FIXTURE_DIR / "invalid_proposed_branch_vision_contract_snapshot.md"
)
INVALID_BLOCKING_BRANCH_VISION_CONTRACT_FIXTURE = (
    FIXTURE_DIR / "invalid_blocking_branch_vision_question.md"
)
VALID_USER_FEEDBACK_DISPOSITION_FIXTURE = (
    FIXTURE_DIR / "valid_user_feedback_disposition.md"
)
INVALID_USER_FEEDBACK_NO_OWNER_FIXTURE = (
    FIXTURE_DIR / "invalid_user_feedback_no_durable_owner.md"
)
INVALID_USER_FEEDBACK_BAD_ID_FIXTURE = (
    FIXTURE_DIR / "invalid_user_feedback_bad_id.md"
)
VALID_REBASELINE_OVERLAP_INTENT_FIXTURE = (
    FIXTURE_DIR / "valid_rebaseline_overlap_intent.md"
)
INVALID_REBASELINE_OVERLAP_UNKNOWN_HIGH_RISK_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_overlap_unknown_high_risk.md"
)
INVALID_REBASELINE_OVERLAP_FALLBACK_ONLY_PASS_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_overlap_fallback_only_pass.md"
)
VALID_REBASELINE_OVERLAP_LOW_RISK_WARN_FIXTURE = (
    FIXTURE_DIR / "valid_rebaseline_overlap_low_risk_warn.md"
)
EXPECTED_SHALLOW_FAILURE_SNIPPETS = (
    "placeholder/self-assessed wording",
    "is too shallow",
    "Scale / Data Volume Model must name concrete scale pressure",
    "Planning Adequacy Review must explain why the plan is not shallow",
    "Whole-System Interaction Map must describe multiple interacting pieces",
    "Runtime Branch Engineering Contract value for 'Planned Runtime Delta:'",
    "Workstream Seam Map must map multiple seams",
)
EXPECTED_NEGATIVE_APPROVAL_FAILURE_SNIPPET = (
    "requires Runtime Implementation Approval to be approved, granted, or waived"
)
EXPECTED_MISSING_PLAN_PATH_FAILURE_SNIPPET = (
    "Branch Runtime Engineering Plan Path: points to missing file"
)
EXPECTED_BRANCH_RUNTIME_PLAN_FAILURE_SNIPPETS = (
    "Branch Runtime Engineering Plan value for 'Current Runtime Baseline:'",
    "Branch Runtime Engineering Plan marker 'Planned Runtime Delta:'",
    "Branch Runtime Engineering Plan value for 'Per-Seam Implementation Checklist:'",
)
EXPECTED_PROPOSED_VISION_FAILURE_SNIPPET = (
    "Branch Vision Snapshot Status cannot stay Proposed"
)
EXPECTED_BLOCKING_VISION_FAILURE_SNIPPET = (
    "Open Vision Questions must be None, queued non-blocking, or Deferred With Waiver"
)
EXPECTED_UFD_NO_OWNER_FAILURE_SNIPPET = (
    "No Durable Owner Needed requires No-Action Reason"
)
EXPECTED_UFD_BAD_ID_FAILURE_SNIPPET = "Feedback ID must use the UFD-* namespace"
EXPECTED_REBASELINE_UNKNOWN_RISK_FAILURE_SNIPPET = (
    "Semantic Merge Risk Unknown is blocked for high-risk overlap surfaces"
)
EXPECTED_REBASELINE_FALLBACK_ONLY_FAILURE_SNIPPET = (
    "Fallback Evidence cannot be used as a compatibility bypass"
)


def _collect_failures():
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    return failures, require


def _validate_fixture(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures, require = _collect_failures()
    governance._validate_product_definition_plan(
        require,
        path.as_posix(),
        text,
        branch_class="implementation",
        current_phase="Live Validation",
        blockers=[],
        next_legal_phase="Live Validation",
    )
    governance._validate_runtime_engineering_contract(
        require,
        path.as_posix(),
        text,
        branch_class="implementation",
        current_phase="Live Validation",
    )
    return failures


def _validate_runtime_contract_text(text: str, *, phase: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_runtime_engineering_contract(
        require,
        "<runtime-contract-fixture>",
        text,
        branch_class="implementation",
        current_phase=phase,
    )
    return failures


def _validate_branch_runtime_plan_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_branch_runtime_engineering_plan(
        require,
        "<branch-runtime-engineering-plan-fixture>",
        text,
    )
    return failures


def _validate_branch_vision_contract_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_branch_vision_contract_snapshot(
        require,
        "<branch-vision-contract-fixture>",
        text,
    )
    return failures


def _validate_user_feedback_disposition_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_user_feedback_disposition(
        require,
        "<user-feedback-disposition-fixture>",
        text,
    )
    return failures


def _validate_branch_change_intent_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_branch_change_intent_ledger(
        require,
        "<branch-change-intent-fixture>",
        text,
    )
    return failures


def _validate_compact_backlog_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_branch_runtime_backlog_compactness(
        require,
        "<backlog-compactness-fixture>",
        text,
    )
    return failures


def _validate_missing_plan_pointer_text() -> list[str]:
    failures, require = _collect_failures()
    governance._validate_branch_runtime_engineering_plan_pointer(
        require,
        "<missing-plan-pointer-fixture>",
        (
            "Branch Runtime Engineering Plan: Accepted\n"
            "Branch Runtime Engineering Plan Path: "
            "Docs/branch_plans/missing_runtime_plan_fixture.md\n"
            "Engineering Plan Status: Accepted\n"
        ),
        branch_class="implementation",
        current_phase="Workstream",
    )
    return failures


def validate() -> list[str]:
    failures: list[str] = []
    for fixture in (
        SHALLOW_FIXTURE,
        CONCRETE_FIXTURE,
        VALID_BRANCH_RUNTIME_PLAN_FIXTURE,
        SHALLOW_BRANCH_RUNTIME_PLAN_FIXTURE,
        BACKLOG_SPRAWL_FIXTURE,
        FOLD_DOWN_FIXTURE,
        VALID_BRANCH_VISION_CONTRACT_FIXTURE,
        INVALID_PROPOSED_BRANCH_VISION_CONTRACT_FIXTURE,
        INVALID_BLOCKING_BRANCH_VISION_CONTRACT_FIXTURE,
        VALID_USER_FEEDBACK_DISPOSITION_FIXTURE,
        INVALID_USER_FEEDBACK_NO_OWNER_FIXTURE,
        INVALID_USER_FEEDBACK_BAD_ID_FIXTURE,
        VALID_REBASELINE_OVERLAP_INTENT_FIXTURE,
        INVALID_REBASELINE_OVERLAP_UNKNOWN_HIGH_RISK_FIXTURE,
        INVALID_REBASELINE_OVERLAP_FALLBACK_ONLY_PASS_FIXTURE,
        VALID_REBASELINE_OVERLAP_LOW_RISK_WARN_FIXTURE,
    ):
        if not fixture.is_file():
            failures.append(f"Missing Branch Readiness planning fixture: {fixture}")

    if failures:
        return failures

    shallow_failures = _validate_fixture(SHALLOW_FIXTURE)
    if not shallow_failures:
        failures.append(
            "Shallow Live Validation fixture unexpectedly passed planning validation"
        )
    else:
        shallow_text = "\n".join(shallow_failures)
        for snippet in EXPECTED_SHALLOW_FAILURE_SNIPPETS:
            if snippet not in shallow_text:
                failures.append(
                    "Shallow Live Validation fixture did not report expected "
                    f"failure snippet: {snippet!r}"
                )

    concrete_failures = _validate_fixture(CONCRETE_FIXTURE)
    if concrete_failures:
        failures.append(
            "Concrete Live Validation fixture unexpectedly failed planning validation: "
            + "; ".join(concrete_failures[:5])
        )

    concrete_text = CONCRETE_FIXTURE.read_text(encoding="utf-8")
    negative_approval_text = concrete_text.replace(
        (
            "Runtime Implementation Approval: USER approved implementation before "
            "this Live Validation fixture; runtime approval is not inferred from planning."
        ),
        "Runtime Implementation Approval: Not approved by USER.",
    )
    negative_approval_failures = _validate_runtime_contract_text(
        negative_approval_text,
        phase="Workstream",
    )
    if EXPECTED_NEGATIVE_APPROVAL_FAILURE_SNIPPET not in "\n".join(
        negative_approval_failures
    ):
        failures.append(
            "Negative runtime approval fixture did not reject "
            "`Runtime Implementation Approval: Not approved by USER`"
        )

    shallow_release_failures = _validate_runtime_contract_text(
        SHALLOW_FIXTURE.read_text(encoding="utf-8"),
        phase="Release Readiness",
    )
    if "Runtime Branch Engineering Contract value for 'Planned Runtime Delta:'" not in "\n".join(
        shallow_release_failures
    ):
        failures.append(
            "Shallow Release Readiness fixture did not prove runtime contract enforcement"
        )

    concrete_release_failures = _validate_runtime_contract_text(
        concrete_text,
        phase="Release Readiness",
    )
    if concrete_release_failures:
        failures.append(
            "Concrete Release Readiness runtime contract fixture unexpectedly failed: "
            + "; ".join(concrete_release_failures[:5])
        )

    valid_plan_failures = _validate_branch_runtime_plan_text(
        VALID_BRANCH_RUNTIME_PLAN_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_plan_failures:
        failures.append(
            "Valid Branch Runtime Engineering Plan fixture unexpectedly failed: "
            + "; ".join(valid_plan_failures[:5])
        )

    shallow_plan_failures = _validate_branch_runtime_plan_text(
        SHALLOW_BRANCH_RUNTIME_PLAN_FIXTURE.read_text(encoding="utf-8")
    )
    if not shallow_plan_failures:
        failures.append(
            "Shallow Branch Runtime Engineering Plan fixture unexpectedly passed"
        )
    else:
        shallow_plan_text = "\n".join(shallow_plan_failures)
        for snippet in EXPECTED_BRANCH_RUNTIME_PLAN_FAILURE_SNIPPETS:
            if snippet not in shallow_plan_text:
                failures.append(
                    "Shallow Branch Runtime Engineering Plan fixture did not report "
                    f"expected failure snippet: {snippet!r}"
                )

    backlog_sprawl_failures = _validate_compact_backlog_text(
        BACKLOG_SPRAWL_FIXTURE.read_text(encoding="utf-8")
    )
    if not backlog_sprawl_failures:
        failures.append("Backlog planning-sprawl fixture unexpectedly passed")

    fold_down_failures = _validate_branch_runtime_plan_text(
        FOLD_DOWN_FIXTURE.read_text(encoding="utf-8")
    )
    if fold_down_failures:
        failures.append(
            "Valid PR fold-down Branch Runtime Engineering Plan fixture unexpectedly failed: "
            + "; ".join(fold_down_failures[:5])
        )

    missing_plan_failures = _validate_missing_plan_pointer_text()
    if EXPECTED_MISSING_PLAN_PATH_FAILURE_SNIPPET not in "\n".join(
        missing_plan_failures
    ):
        failures.append(
            "Missing Branch Runtime Engineering Plan path fixture did not reject "
            "an accepted plan pointer to a nonexistent file"
        )

    valid_vision_failures = _validate_branch_vision_contract_text(
        VALID_BRANCH_VISION_CONTRACT_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_vision_failures:
        failures.append(
            "Valid Branch Vision Contract Snapshot fixture unexpectedly failed: "
            + "; ".join(valid_vision_failures[:5])
        )

    proposed_vision_failures = _validate_branch_vision_contract_text(
        INVALID_PROPOSED_BRANCH_VISION_CONTRACT_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_PROPOSED_VISION_FAILURE_SNIPPET not in "\n".join(
        proposed_vision_failures
    ):
        failures.append(
            "Invalid proposed-only Branch Vision Contract fixture did not reject "
            "Codex/ChatGPT recommendations without USER acceptance"
        )

    blocking_vision_failures = _validate_branch_vision_contract_text(
        INVALID_BLOCKING_BRANCH_VISION_CONTRACT_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BLOCKING_VISION_FAILURE_SNIPPET not in "\n".join(
        blocking_vision_failures
    ):
        failures.append(
            "Invalid blocking Branch Vision Contract fixture did not reject "
            "open blocking vision questions"
        )

    valid_ufd_failures = _validate_user_feedback_disposition_text(
        VALID_USER_FEEDBACK_DISPOSITION_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_ufd_failures:
        failures.append(
            "Valid USER Feedback Disposition fixture unexpectedly failed: "
            + "; ".join(valid_ufd_failures[:5])
        )

    no_owner_ufd_failures = _validate_user_feedback_disposition_text(
        INVALID_USER_FEEDBACK_NO_OWNER_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_UFD_NO_OWNER_FAILURE_SNIPPET not in "\n".join(no_owner_ufd_failures):
        failures.append(
            "Invalid USER Feedback Disposition no-owner fixture did not reject "
            "No Durable Owner Needed without No-Action Reason"
        )

    bad_id_ufd_failures = _validate_user_feedback_disposition_text(
        INVALID_USER_FEEDBACK_BAD_ID_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_UFD_BAD_ID_FAILURE_SNIPPET not in "\n".join(bad_id_ufd_failures):
        failures.append(
            "Invalid USER Feedback Disposition bad-ID fixture did not reject "
            "non-UFD feedback ID namespace"
        )

    valid_overlap_failures = _validate_branch_change_intent_text(
        VALID_REBASELINE_OVERLAP_INTENT_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_overlap_failures:
        failures.append(
            "Valid Rebaseline Overlap Intent fixture unexpectedly failed: "
            + "; ".join(valid_overlap_failures[:5])
        )

    invalid_overlap_failures = _validate_branch_change_intent_text(
        INVALID_REBASELINE_OVERLAP_UNKNOWN_HIGH_RISK_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_REBASELINE_UNKNOWN_RISK_FAILURE_SNIPPET not in "\n".join(
        invalid_overlap_failures
    ):
        failures.append(
            "Invalid Rebaseline Overlap Intent fixture did not reject Unknown "
            "semantic merge risk for a high-risk overlap surface"
        )

    fallback_only_failures = _validate_branch_change_intent_text(
        INVALID_REBASELINE_OVERLAP_FALLBACK_ONLY_PASS_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_REBASELINE_FALLBACK_ONLY_FAILURE_SNIPPET not in "\n".join(
        fallback_only_failures
    ):
        failures.append(
            "Invalid Rebaseline Overlap Intent fixture did not reject fallback-only "
            "PASS / compatibility-bypass wording after the effective point"
        )

    low_risk_warn_failures = _validate_branch_change_intent_text(
        VALID_REBASELINE_OVERLAP_LOW_RISK_WARN_FIXTURE.read_text(encoding="utf-8")
    )
    if low_risk_warn_failures:
        failures.append(
            "Valid low-risk WARN Rebaseline Overlap Intent fixture unexpectedly failed: "
            + "; ".join(low_risk_warn_failures[:5])
        )

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: Branch Readiness planning fixture validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Branch Readiness planning fixture validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
