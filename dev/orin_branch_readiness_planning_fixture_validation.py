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
import orin_worktree_rebaseline_audit as rebaseline


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
VALID_USER_FEEDBACK_UNICODE_SUMMARY_FIXTURE = (
    FIXTURE_DIR / "valid_user_feedback_unicode_summary.md"
)
INVALID_USER_FEEDBACK_NO_OWNER_FIXTURE = (
    FIXTURE_DIR / "invalid_user_feedback_no_durable_owner.md"
)
INVALID_USER_FEEDBACK_BAD_ID_FIXTURE = (
    FIXTURE_DIR / "invalid_user_feedback_bad_id.md"
)
INVALID_USER_FEEDBACK_DUPLICATE_SUMMARY_FIXTURE = (
    FIXTURE_DIR / "invalid_user_feedback_duplicate_summary.md"
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
INVALID_REBASELINE_OVERLAP_FIXTURE_HIGH_IMPACT_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_overlap_fixture_high_impact.md"
)
VALID_REBASELINE_OVERLAP_FIXTURE_LOW_IMPACT_FIXTURE = (
    FIXTURE_DIR / "valid_rebaseline_overlap_fixture_low_impact.md"
)
VALID_ELEMENT_TO_PHASE_MATRIX_FIXTURE = (
    FIXTURE_DIR / "valid_element_to_phase_proof_matrix.md"
)
INVALID_ELEMENT_TO_PHASE_MISSING_HARDENING_FIXTURE = (
    FIXTURE_DIR / "invalid_element_to_phase_missing_hardening.md"
)
INVALID_ELEMENT_TO_PHASE_MISSING_LIVE_VALIDATION_FIXTURE = (
    FIXTURE_DIR / "invalid_element_to_phase_missing_live_validation.md"
)
VALID_ELEMENT_TO_PHASE_DEFERRED_FUTURE_FIXTURE = (
    FIXTURE_DIR / "valid_element_to_phase_deferred_future.md"
)
INVALID_ELEMENT_TO_PHASE_DUPLICATE_ID_FIXTURE = (
    FIXTURE_DIR / "invalid_element_to_phase_duplicate_id.md"
)
VALID_WORKSTREAM_ENTRY_WHOLE_PACKAGE_FIXTURE = (
    FIXTURE_DIR / "valid_workstream_entry_whole_package_analysis.md"
)
INVALID_WORKSTREAM_ENTRY_FIRST_SEAM_ONLY_FIXTURE = (
    FIXTURE_DIR / "invalid_workstream_entry_first_seam_only.md"
)
VALID_USER_BRANCH_PLAN_REVIEW_FIXTURE = (
    FIXTURE_DIR / "valid_user_branch_plan_review_gate.md"
)
INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_OUTCOME_FIXTURE = (
    FIXTURE_DIR / "invalid_user_branch_plan_review_missing_outcome.md"
)
INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_PACKET_FINDING_FIXTURE = (
    FIXTURE_DIR / "invalid_user_branch_plan_review_missing_packet_finding.md"
)
INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_HARDENING_FIXTURE = (
    FIXTURE_DIR / "invalid_user_branch_plan_review_missing_hardening.md"
)
INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_LIVE_VALIDATION_FIXTURE = (
    FIXTURE_DIR / "invalid_user_branch_plan_review_missing_live_validation.md"
)
INVALID_USER_BRANCH_PLAN_REVIEW_FIRST_SEAM_ONLY_FIXTURE = (
    FIXTURE_DIR / "invalid_user_branch_plan_review_first_seam_only.md"
)
INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_RESPONSE_DIGEST_FIXTURE = (
    FIXTURE_DIR / "invalid_user_branch_plan_review_missing_response_digest.md"
)
VALID_USER_BRANCH_PLAN_REVIEW_DEFERRED_SCOPE_FIXTURE = (
    FIXTURE_DIR / "valid_user_branch_plan_review_deferred_scope.md"
)
VALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE = (
    FIXTURE_DIR / "valid_merge_stable_source_truth_projection.md"
)
INVALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE = (
    FIXTURE_DIR / "invalid_merge_stable_source_truth_projection.md"
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
EXPECTED_BRANCH_RUNTIME_PLAN_MISSING_REVIEW_GATE_FAILURE_SNIPPET = (
    "Workstream Entry planning is missing '## USER Branch Plan Review Gate'"
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
EXPECTED_UFD_DUPLICATE_SUMMARY_FAILURE_SNIPPET = "duplicate UFD Feedback Summary"
EXPECTED_REBASELINE_UNKNOWN_RISK_FAILURE_SNIPPET = (
    "Semantic Merge Risk Unknown is blocked for high-risk overlap surfaces"
)
EXPECTED_REBASELINE_FALLBACK_ONLY_FAILURE_SNIPPET = (
    "Fallback Evidence cannot be used as a compatibility bypass"
)
EXPECTED_REBASELINE_FIXTURE_HIGH_IMPACT_FAILURE_SNIPPET = (
    "Regression / Gating Impact Medium, High, or Unknown blocks fixture/test overlap"
)
EXPECTED_ELEMENT_MATRIX_HARDENING_FAILURE_SNIPPET = "Hardening Proof Plan"
EXPECTED_ELEMENT_MATRIX_LIVE_VALIDATION_FAILURE_SNIPPET = (
    "Live Validation Proof / Waiver Plan"
)
EXPECTED_ELEMENT_MATRIX_DUPLICATE_ID_FAILURE_SNIPPET = "duplicates an Element ID"
EXPECTED_WORKSTREAM_ENTRY_FIRST_SEAM_FAILURE_SNIPPET = (
    "Workstream Entry Whole-Package Summary must include"
)
EXPECTED_USER_BRANCH_PLAN_MISSING_OUTCOME_FAILURE_SNIPPET = (
    "Planned User-Facing Outcome:"
)
EXPECTED_USER_BRANCH_PLAN_MISSING_PACKET_FINDING_FAILURE_SNIPPET = (
    "USER Review Packet Finding:"
)
EXPECTED_USER_BRANCH_PLAN_MISSING_HARDENING_FAILURE_SNIPPET = "Hardening Plan:"
EXPECTED_USER_BRANCH_PLAN_MISSING_LIVE_VALIDATION_FAILURE_SNIPPET = (
    "Live Validation / UTS Plan:"
)
EXPECTED_USER_BRANCH_PLAN_FIRST_SEAM_FAILURE_SNIPPET = (
    "cannot be satisfied by first-seam-only implementation planning"
)
EXPECTED_USER_BRANCH_PLAN_MISSING_RESPONSE_DIGEST_FAILURE_SNIPPET = (
    "USER Review Response:"
)
EXPECTED_MERGE_STABLE_PROJECTION_FAILURE_SNIPPET = "PR creation pending"


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


def _without_user_branch_plan_review_gate(text: str) -> str:
    marker = "\n## USER Branch Plan Review Gate\n"
    start = text.find(marker)
    if start == -1:
        return text
    next_heading = text.find("\n## ", start + len(marker))
    if next_heading == -1:
        return text[:start].rstrip() + "\n"
    return text[:start].rstrip() + "\n" + text[next_heading:].lstrip()


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


def _validate_element_to_phase_matrix_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_element_to_phase_proof_matrix(
        require,
        "<element-to-phase-proof-matrix-fixture>",
        text,
        require_matrix=True,
    )
    return failures


def _validate_workstream_entry_whole_package_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    analysis = governance._extract_marker_value(
        text, "Workstream Entry Whole-Package Analysis:"
    )
    summary = governance._extract_marker_value(
        text, "Workstream Entry Whole-Package Summary:"
    )
    normalized_analysis = governance._normalized_planning_value(analysis)
    normalized_summary = governance._normalized_planning_value(summary)

    require(
        bool(analysis),
        "Workstream Entry Whole-Package Analysis marker is missing",
    )
    require(
        bool(summary),
        "Workstream Entry Whole-Package Summary marker is missing",
    )
    require(
        not normalized_analysis.startswith("not required")
        and "first-seam-only" not in normalized_analysis
        and "first seam only" not in normalized_analysis,
        "Workstream Entry Whole-Package Analysis cannot be waived by first-seam-only wording",
    )
    required_summary_phrases = (
        "all admitted slices/seams",
        "completion strategy",
        "first-seam recommendation",
        "seam dependency map",
        "future-gated",
        "preservation surfaces",
        "validation plan",
        "hardening h1",
        "live validation lv1",
        "uts handoff",
        "exact implementation approval text",
    )
    for phrase in required_summary_phrases:
        require(
            phrase in normalized_summary,
            f"Workstream Entry Whole-Package Summary must include {phrase}",
        )
    return failures


def _validate_user_branch_plan_review_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    governance._validate_user_branch_plan_review_gate(
        require,
        "<user-branch-plan-review-fixture>",
        text,
        require_gate=True,
    )
    return failures


def _validate_merge_stable_projection_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    stale_lines = governance._stale_pre_pr_lines(text)
    require(
        not stale_lines,
        (
            "Merge-Stable Source Truth Projection Missing: "
            + "; ".join(line for _, line in stale_lines)
        ),
    )
    return failures


def _validate_merge_stable_projection_helpers() -> list[str]:
    failures, require = _collect_failures()
    broad_allowlist_failures = governance._stale_pre_pr_lines(
        "Status: PR creation pending after blocker scan."
    )
    require(
        bool(broad_allowlist_failures),
        "Merge-stable stale pre-PR detector must not allow blocker/scan wording",
    )
    adjacent_paths = governance._collect_merge_stable_detail_record_paths(
        (
            "Assignment Status: Historical merged-unreleased after PR #201.\n"
            "Branch Authority Record: "
            "`Docs/branch_records/feature_example_merge_stable_fixture.md`\n"
        )
    )
    require(
        "Docs/branch_records/feature_example_merge_stable_fixture.md" in adjacent_paths,
        (
            "Merge-stable detail record collection must capture canonical record paths "
            "from adjacent merge-status blocks"
        ),
    )
    return failures


def _runtime_overlap_ledger_text() -> str:
    return """# Runtime Overlap Fixture

## Branch Change Intent Ledger

### Changed Surface: main.py

Surface Class: runtime
Change Intent: preserve runtime launch behavior while reconciling an overlapping main entrypoint change.
Why This File Was Touched: the branch changed the runtime entrypoint for a governed behavior fix.
Owned Behavior / Fact Class: runtime launch behavior and validation entrypoint.
Canonical Owner / Source Owner: main.py.
Resolution Owner: Current Branch
Shared Surface: Yes.
Overlap Risk: Medium.
Expected Conflict Risk: Medium.
Semantic Merge Risk: Medium
Regression / Gating Impact: Low
Conflict Resolution Rule: compare incoming runtime intent against the branch ledger and stop for USER decision when behavior changes.
Rebaseline Handling: rerun runtime and governance validation before requesting mutation.
Validation Proof: validation required after repair: branch governance validation and compileall.
Fallback Evidence: fallback evidence may classify risk, but it is not a compatibility bypass.
USER Decision / Waiver: USER approval required before mutation.
Fold-Down Target: compact branch receipt when durable.
"""


def _validate_rebaseline_overlap_helper_matrix() -> list[str]:
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    require(
        rebaseline._overall_overlap_gate_result([]) == "Not Applicable",
        "Rebaseline helper no-overlap matrix did not return Not Applicable",
    )
    require(
        governance._bot_review_comment_is_green_signal(
            "Codex Review: Didn't find any major issues. Chef's kiss."
        ),
        "Governance validator did not recognize Codex green review comment as a bot-review signal",
    )
    require(
        governance._bot_review_comment_is_green_signal(
            "Codex Review: Didn\u2019t find any major issues. Chef\u2019s kiss."
        ),
        "Governance validator did not normalize smart apostrophes in Codex green review comments",
    )
    require(
        not governance._bot_review_comment_is_green_signal(
            "Here are some automated review suggestions for this pull request."
        ),
        "Governance validator treated a Codex suggestion comment as a green bot-review signal",
    )
    require(
        not governance._bot_review_comment_is_green_signal(
            "Codex Review: looks good overall, but there is one major issue to fix."
        ),
        "Governance validator treated a contrastive Codex review comment as a green bot-review signal",
    )
    require(
        rebaseline._overlap_intent_missing_status("PASS").startswith("No -"),
        "Rebaseline helper did not return non-blocking intent-missing status for PASS",
    )
    blocked_state, blocked_recommendation = rebaseline._apply_overlap_recommendation(
        "Blocked",
        "Worktree has local changes; do not baseline until the owner reviews or commits/stashes them.",
        "WARN",
    )
    require(
        blocked_state == "Blocked" and "Overlap warning also present" in blocked_recommendation,
        "Rebaseline helper downgraded a dirty-worktree Blocked recommendation when overlap WARN was present",
    )

    missing_runtime = rebaseline._assess_overlap_file("main.py", {})
    require(
        missing_runtime["per_file_result"] == "BLOCKED",
        "Rebaseline helper did not block high-risk runtime overlap with missing ledger",
    )

    runtime_entries = rebaseline._branch_change_intent_entries(_runtime_overlap_ledger_text())
    runtime_with_ledger = rebaseline._assess_overlap_file("main.py", runtime_entries)
    require(
        runtime_with_ledger["branch_intent_present"] == "YES"
        and runtime_with_ledger["per_file_result"] == "PASS",
        "Rebaseline helper did not PASS/evidence-present high-risk runtime overlap with a valid ledger",
    )

    source_truth_missing = rebaseline._assess_overlap_file("Docs/Main.md", {})
    require(
        rebaseline._surface_class("Docs/Main.md") == "governance/source-truth"
        and source_truth_missing["per_file_result"] == "BLOCKED",
        "Rebaseline helper did not classify Docs/Main.md as blocked source-truth overlap without ledger",
    )

    low_reference_missing = rebaseline._assess_overlap_file("Docs/incident_patterns.md", {})
    require(
        rebaseline._surface_class("Docs/incident_patterns.md") == "documentation/reference"
        and low_reference_missing["per_file_result"] == "WARN",
        "Rebaseline helper did not WARN on low-risk reference overlap without ledger",
    )

    valid_entries = rebaseline._branch_change_intent_entries(
        VALID_REBASELINE_OVERLAP_INTENT_FIXTURE.read_text(encoding="utf-8")
    )
    mismatch = rebaseline._assess_overlap_file("Docs/Main.md", valid_entries)
    require(
        mismatch["per_file_result"] == "BLOCKED",
        "Rebaseline helper did not block branch plan ledger path mismatch",
    )

    high_impact_entries = rebaseline._branch_change_intent_entries(
        INVALID_REBASELINE_OVERLAP_FIXTURE_HIGH_IMPACT_FIXTURE.read_text(encoding="utf-8")
    )
    high_impact = rebaseline._assess_overlap_file(
        "dev/fixtures/branch_readiness_planning/valid_user_feedback_disposition.md",
        high_impact_entries,
    )
    require(
        high_impact["per_file_result"] == "BLOCKED",
        "Rebaseline helper did not block fixture/test overlap with high regression impact",
    )

    low_impact_entries = rebaseline._branch_change_intent_entries(
        VALID_REBASELINE_OVERLAP_FIXTURE_LOW_IMPACT_FIXTURE.read_text(encoding="utf-8")
    )
    low_impact = rebaseline._assess_overlap_file(
        "dev/fixtures/branch_readiness_planning/reference_only_example.md",
        low_impact_entries,
    )
    require(
        low_impact["per_file_result"] == "PASS",
        "Rebaseline helper did not accept fixture/test overlap with low regression impact and valid ledger",
    )

    fam_role = rebaseline._worktree_role(Path("C:/Nexus Worktrees/FAM-006"))
    require(
        "FAM-006 implementation lane" not in fam_role
        and "runtime-active candidate" in fam_role,
        "Rebaseline helper still treats FAM-006 as a permanent lane instead of a generic runtime slot",
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
        VALID_USER_FEEDBACK_UNICODE_SUMMARY_FIXTURE,
        INVALID_USER_FEEDBACK_NO_OWNER_FIXTURE,
        INVALID_USER_FEEDBACK_BAD_ID_FIXTURE,
        INVALID_USER_FEEDBACK_DUPLICATE_SUMMARY_FIXTURE,
        VALID_REBASELINE_OVERLAP_INTENT_FIXTURE,
        INVALID_REBASELINE_OVERLAP_UNKNOWN_HIGH_RISK_FIXTURE,
        INVALID_REBASELINE_OVERLAP_FALLBACK_ONLY_PASS_FIXTURE,
        VALID_REBASELINE_OVERLAP_LOW_RISK_WARN_FIXTURE,
        INVALID_REBASELINE_OVERLAP_FIXTURE_HIGH_IMPACT_FIXTURE,
        VALID_REBASELINE_OVERLAP_FIXTURE_LOW_IMPACT_FIXTURE,
        VALID_ELEMENT_TO_PHASE_MATRIX_FIXTURE,
        INVALID_ELEMENT_TO_PHASE_MISSING_HARDENING_FIXTURE,
        INVALID_ELEMENT_TO_PHASE_MISSING_LIVE_VALIDATION_FIXTURE,
        VALID_ELEMENT_TO_PHASE_DEFERRED_FUTURE_FIXTURE,
        INVALID_ELEMENT_TO_PHASE_DUPLICATE_ID_FIXTURE,
        VALID_WORKSTREAM_ENTRY_WHOLE_PACKAGE_FIXTURE,
        INVALID_WORKSTREAM_ENTRY_FIRST_SEAM_ONLY_FIXTURE,
        VALID_USER_BRANCH_PLAN_REVIEW_FIXTURE,
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_OUTCOME_FIXTURE,
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_PACKET_FINDING_FIXTURE,
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_HARDENING_FIXTURE,
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_LIVE_VALIDATION_FIXTURE,
        INVALID_USER_BRANCH_PLAN_REVIEW_FIRST_SEAM_ONLY_FIXTURE,
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_RESPONSE_DIGEST_FIXTURE,
        VALID_USER_BRANCH_PLAN_REVIEW_DEFERRED_SCOPE_FIXTURE,
        VALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE,
        INVALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE,
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

    missing_review_gate_failures = _validate_branch_runtime_plan_text(
        _without_user_branch_plan_review_gate(
            VALID_BRANCH_RUNTIME_PLAN_FIXTURE.read_text(encoding="utf-8")
        )
    )
    if EXPECTED_BRANCH_RUNTIME_PLAN_MISSING_REVIEW_GATE_FAILURE_SNIPPET not in "\n".join(
        missing_review_gate_failures
    ):
        failures.append(
            "Pre-implementation Branch Runtime Engineering Plan fixture did not "
            "reject a missing USER Branch Plan Review Gate"
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

    valid_unicode_ufd_failures = _validate_user_feedback_disposition_text(
        VALID_USER_FEEDBACK_UNICODE_SUMMARY_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_unicode_ufd_failures:
        failures.append(
            "Valid USER Feedback Disposition Unicode summary fixture unexpectedly failed: "
            + "; ".join(valid_unicode_ufd_failures[:5])
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

    duplicate_summary_failures = _validate_user_feedback_disposition_text(
        INVALID_USER_FEEDBACK_DUPLICATE_SUMMARY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_UFD_DUPLICATE_SUMMARY_FAILURE_SNIPPET not in "\n".join(
        duplicate_summary_failures
    ):
        failures.append(
            "Invalid USER Feedback Disposition duplicate-summary fixture did not reject "
            "duplicate meaningful feedback"
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

    high_impact_fixture_failures = _validate_branch_change_intent_text(
        INVALID_REBASELINE_OVERLAP_FIXTURE_HIGH_IMPACT_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_REBASELINE_FIXTURE_HIGH_IMPACT_FAILURE_SNIPPET not in "\n".join(
        high_impact_fixture_failures
    ):
        failures.append(
            "Invalid Rebaseline Overlap fixture/test fixture did not reject High "
            "Regression / Gating Impact"
        )

    low_impact_fixture_failures = _validate_branch_change_intent_text(
        VALID_REBASELINE_OVERLAP_FIXTURE_LOW_IMPACT_FIXTURE.read_text(encoding="utf-8")
    )
    if low_impact_fixture_failures:
        failures.append(
            "Valid low-impact fixture/test Rebaseline Overlap Intent fixture unexpectedly failed: "
            + "; ".join(low_impact_fixture_failures[:5])
        )

    valid_matrix_failures = _validate_element_to_phase_matrix_text(
        VALID_ELEMENT_TO_PHASE_MATRIX_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_matrix_failures:
        failures.append(
            "Valid Element-to-Phase Proof Matrix fixture unexpectedly failed: "
            + "; ".join(valid_matrix_failures[:5])
        )

    missing_hardening_failures = _validate_element_to_phase_matrix_text(
        INVALID_ELEMENT_TO_PHASE_MISSING_HARDENING_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_ELEMENT_MATRIX_HARDENING_FAILURE_SNIPPET not in "\n".join(
        missing_hardening_failures
    ):
        failures.append(
            "Invalid Element-to-Phase Proof Matrix fixture did not reject missing "
            "Hardening proof path"
        )

    missing_live_validation_failures = _validate_element_to_phase_matrix_text(
        INVALID_ELEMENT_TO_PHASE_MISSING_LIVE_VALIDATION_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_ELEMENT_MATRIX_LIVE_VALIDATION_FAILURE_SNIPPET not in "\n".join(
        missing_live_validation_failures
    ):
        failures.append(
            "Invalid Element-to-Phase Proof Matrix fixture did not reject missing "
            "Live Validation proof or waiver path"
        )

    deferred_future_matrix_failures = _validate_element_to_phase_matrix_text(
        VALID_ELEMENT_TO_PHASE_DEFERRED_FUTURE_FIXTURE.read_text(encoding="utf-8")
    )
    if deferred_future_matrix_failures:
        failures.append(
            "Valid deferred/future Element-to-Phase Proof Matrix fixture unexpectedly failed: "
            + "; ".join(deferred_future_matrix_failures[:5])
        )

    duplicate_matrix_failures = _validate_element_to_phase_matrix_text(
        INVALID_ELEMENT_TO_PHASE_DUPLICATE_ID_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_ELEMENT_MATRIX_DUPLICATE_ID_FAILURE_SNIPPET not in "\n".join(
        duplicate_matrix_failures
    ):
        failures.append(
            "Invalid Element-to-Phase Proof Matrix fixture did not reject duplicate "
            "Element ID values"
        )

    valid_whole_package_failures = _validate_workstream_entry_whole_package_text(
        VALID_WORKSTREAM_ENTRY_WHOLE_PACKAGE_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_whole_package_failures:
        failures.append(
            "Valid Workstream Entry Whole-Package Analysis fixture unexpectedly failed: "
            + "; ".join(valid_whole_package_failures[:5])
        )

    first_seam_only_failures = _validate_workstream_entry_whole_package_text(
        INVALID_WORKSTREAM_ENTRY_FIRST_SEAM_ONLY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_WORKSTREAM_ENTRY_FIRST_SEAM_FAILURE_SNIPPET not in "\n".join(
        first_seam_only_failures
    ):
        failures.append(
            "Invalid Workstream Entry fixture did not reject first-seam-only analysis"
        )

    valid_branch_review_failures = _validate_user_branch_plan_review_text(
        VALID_USER_BRANCH_PLAN_REVIEW_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_branch_review_failures:
        failures.append(
            "Valid USER Branch Plan Review fixture unexpectedly failed: "
            + "; ".join(valid_branch_review_failures[:5])
        )

    missing_outcome_failures = _validate_user_branch_plan_review_text(
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_OUTCOME_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_USER_BRANCH_PLAN_MISSING_OUTCOME_FAILURE_SNIPPET not in "\n".join(
        missing_outcome_failures
    ):
        failures.append(
            "Invalid USER Branch Plan Review fixture did not reject missing "
            "planned user-facing outcome"
        )

    missing_packet_finding_failures = _validate_user_branch_plan_review_text(
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_PACKET_FINDING_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_USER_BRANCH_PLAN_MISSING_PACKET_FINDING_FAILURE_SNIPPET not in "\n".join(
        missing_packet_finding_failures
    ):
        failures.append(
            "Invalid USER Branch Plan Review fixture did not reject missing "
            "USER Review Packet Finding"
        )

    missing_review_hardening_failures = _validate_user_branch_plan_review_text(
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_HARDENING_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_USER_BRANCH_PLAN_MISSING_HARDENING_FAILURE_SNIPPET not in "\n".join(
        missing_review_hardening_failures
    ):
        failures.append(
            "Invalid USER Branch Plan Review fixture did not reject missing "
            "Hardening plan"
        )

    missing_review_live_validation_failures = _validate_user_branch_plan_review_text(
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_LIVE_VALIDATION_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_USER_BRANCH_PLAN_MISSING_LIVE_VALIDATION_FAILURE_SNIPPET not in "\n".join(
        missing_review_live_validation_failures
    ):
        failures.append(
            "Invalid USER Branch Plan Review fixture did not reject missing "
            "Live Validation / UTS plan"
        )

    first_seam_review_failures = _validate_user_branch_plan_review_text(
        INVALID_USER_BRANCH_PLAN_REVIEW_FIRST_SEAM_ONLY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_USER_BRANCH_PLAN_FIRST_SEAM_FAILURE_SNIPPET not in "\n".join(
        first_seam_review_failures
    ):
        failures.append(
            "Invalid USER Branch Plan Review fixture did not reject first-seam-only "
            "implementation breakdown"
        )

    missing_response_digest_failures = _validate_user_branch_plan_review_text(
        INVALID_USER_BRANCH_PLAN_REVIEW_MISSING_RESPONSE_DIGEST_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_USER_BRANCH_PLAN_MISSING_RESPONSE_DIGEST_FAILURE_SNIPPET not in "\n".join(
        missing_response_digest_failures
    ):
        failures.append(
            "Invalid USER Branch Plan Review fixture did not reject missing "
            "USER response / Codex digest markers"
        )

    deferred_review_failures = _validate_user_branch_plan_review_text(
        VALID_USER_BRANCH_PLAN_REVIEW_DEFERRED_SCOPE_FIXTURE.read_text(encoding="utf-8")
    )
    if deferred_review_failures:
        failures.append(
            "Valid deferred-scope USER Branch Plan Review fixture unexpectedly failed: "
            + "; ".join(deferred_review_failures[:5])
        )

    valid_merge_stable_failures = _validate_merge_stable_projection_text(
        VALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_merge_stable_failures:
        failures.append(
            "Valid Merge-Stable Source Truth Projection fixture unexpectedly failed: "
            + "; ".join(valid_merge_stable_failures[:5])
        )

    invalid_merge_stable_failures = _validate_merge_stable_projection_text(
        INVALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_MERGE_STABLE_PROJECTION_FAILURE_SNIPPET not in "\n".join(
        invalid_merge_stable_failures
    ):
        failures.append(
            "Invalid Merge-Stable Source Truth Projection fixture did not reject "
            "stale PR creation pending wording"
        )

    failures.extend(_validate_merge_stable_projection_helpers())

    failures.extend(_validate_rebaseline_overlap_helper_matrix())

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
