# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=branch-readiness-planning-fixture-validator; status=shared
"""Regression fixtures for Branch Readiness product-system planning.

The governance validator is intentionally broad and source-truth heavy. This
fixture helper keeps one small regression seam focused on the failure pattern
where a broad implementation branch reaches a later phase with marker-only
planning.
"""

from __future__ import annotations

import inspect
import re
import tempfile
import warnings
import zipfile
from pathlib import Path

import orin_branch_governance_validation as governance
import orin_external_state_validation as external_state
from orin_external_state_common import DEFAULT_EXTERNAL_STATE_ROOT
import orin_user_review_bundle as review_bundle
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
VALID_BRANCH_PLANNING_GATE_STATE_FIXTURE = (
    FIXTURE_DIR / "valid_branch_planning_review_gate_state.md"
)
INVALID_BRANCH_PLANNING_GATE_BYPASS_FIXTURE = (
    FIXTURE_DIR / "invalid_packet_validation_treated_as_user_acceptance.md"
)
VALID_BP1_BRANCH_VISION_REVIEW_FIXTURE = (
    FIXTURE_DIR / "valid_bp1_branch_vision_review.md"
)
VALID_BP1_FAM006_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp1_fam006_ui_runtime_dogfood_review.md"
)
VALID_BP1_FAM007_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp1_fam007_private_boundary_dogfood_review.md"
)
VALID_BP1_GOVERNANCE_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp1_governance_source_truth_dogfood_review.md"
)
INVALID_BP1_MISSING_CONTEXT_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_missing_project_family_branch_context.md"
)
INVALID_BP1_SHALLOW_RECOMMENDATIONS_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_shallow_recommendations.md"
)
INVALID_BP1_TEMPLATE_SHELL_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_template_shell_review.md"
)
INVALID_BP1_PROCESS_MECHANICS_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_process_mechanics_review.md"
)
INVALID_BP1_COPIED_FILE_SURFACE_ONLY_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_copied_file_surface_map_only.md"
)
INVALID_BP1_GENERIC_USER_QUESTIONS_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_generic_user_questions.md"
)
INVALID_BP1_SLC_CENTERED_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_slc_centered_branch_vision_review.md"
)
INVALID_BP1_TECHNICAL_METADATA_FIXTURE = (
    FIXTURE_DIR / "invalid_bp1_technical_metadata.md"
)
INVALID_BP2_MISSING_ACCEPTED_BP1_TRACE_FIXTURE = (
    FIXTURE_DIR / "invalid_bp2_missing_accepted_bp1_trace.md"
)
INVALID_BP2_PRODUCT_DESIGN_WORDING_FIXTURE = (
    FIXTURE_DIR / "invalid_bp2_product_design_contract_wording.md"
)
VALID_BP2_FAM006_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp2_fam006_ui_runtime_dogfood_review.md"
)
VALID_BP2_FAM007_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp2_fam007_private_boundary_dogfood_review.md"
)
INVALID_BP3_IMPLEMENTATION_WITH_PENDING_BP1_BP2_FIXTURE = (
    FIXTURE_DIR / "invalid_bp3_implementation_while_bp1_or_bp2_pending.md"
)
VALID_BP3_ACCEPTED_BP1_BP2_SLC_TRACE_FIXTURE = (
    FIXTURE_DIR / "valid_bp3_accepted_bp1_bp2_slc_traceability_complete.md"
)
VALID_BP3_FAM006_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp3_fam006_ui_runtime_dogfood_review.md"
)
VALID_BP3_FAM007_DOGFOOD_FIXTURE = (
    FIXTURE_DIR / "valid_bp3_fam007_private_boundary_dogfood_review.md"
)
INVALID_USER_PACKET_ACTIVE_BRANCH_METADATA_FIXTURE = (
    FIXTURE_DIR / "invalid_user_packet_active_branch_metadata.md"
)
INVALID_USER_PACKET_ZIP_HASH_FIXTURE = (
    FIXTURE_DIR / "invalid_user_packet_zip_hash.md"
)
INVALID_USER_PACKET_DESKTOP_ACTIVE_UPLOAD_FIXTURE = (
    FIXTURE_DIR / "invalid_user_packet_desktop_active_upload_path.md"
)
INVALID_IMPLEMENTATION_ROUTE_PLANNING_ONLY_FIXTURE = (
    FIXTURE_DIR / "invalid_implementation_route_planning_only_lane_setup.md"
)
VALID_IMPLEMENTATION_ROUTE_SECURITY_BOUNDARY_FIXTURE = (
    FIXTURE_DIR / "valid_implementation_route_security_trust_boundary.md"
)
VALID_BR2_ROUTE_BLOCKER_PACKET_FIXTURE = (
    FIXTURE_DIR / "valid_br2_route_blocker_packet.md"
)
VALID_BR2_ROUTE_BLOCKER_NONE_WORD_ROUTE_FIXTURE = (
    FIXTURE_DIR / "valid_br2_route_blocker_none_word_route.md"
)
INVALID_BR2_ROUTE_BLOCKER_NO_ROUTE_CONTINUE_FIXTURE = (
    FIXTURE_DIR / "invalid_br2_route_blocker_no_route_continue_planning.md"
)
INVALID_BR2_ROUTE_BLOCKER_MARKER_ONLY_DEFERRAL_FIXTURE = (
    FIXTURE_DIR / "invalid_br2_route_blocker_marker_only_deferral.md"
)
INVALID_IMPLEMENTATION_ROUTE_FAKE_FEATURE_LABEL_FIXTURE = (
    FIXTURE_DIR / "invalid_implementation_route_fake_feature_label.md"
)
INVALID_IMPLEMENTATION_ROUTE_PROOF_BOUNDARY_LABEL_FIXTURE = (
    FIXTURE_DIR / "invalid_implementation_route_proof_boundary_label.md"
)
INVALID_IMPLEMENTATION_ROUTE_TBD_OUTPUT_FIXTURE = (
    FIXTURE_DIR / "invalid_implementation_route_tbd_output.md"
)
INVALID_IMPLEMENTATION_ROUTE_BLANK_SELECTED_ROUTE_FIXTURE = (
    FIXTURE_DIR / "invalid_implementation_route_blank_selected_route.md"
)
INVALID_IMPLEMENTATION_ROUTE_NEGATED_BEHAVIOR_FIXTURE = (
    FIXTURE_DIR / "invalid_implementation_route_negated_behavior.md"
)
INVALID_BR2_ROUTE_BLOCKER_PROOF_ONLY_ROUTE_FIXTURE = (
    FIXTURE_DIR / "invalid_br2_route_blocker_proof_only_route.md"
)
INVALID_SLC_SLICE_SEAM_AMBIGUITY_FIXTURE = (
    FIXTURE_DIR / "invalid_slc_slice_seam_terminology_ambiguity.md"
)
VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE = (
    FIXTURE_DIR / "valid_multi_slice_implementation_carrier.md"
)
VALID_REQUIRED_SEPARATE_BRANCH_CASE_FIXTURE = (
    FIXTURE_DIR / "valid_required_separate_branch_case.md"
)
VALID_IMPLEMENTATION_ROUTE_BP2_HOLD_ACTION_GATE_FIXTURE = (
    FIXTURE_DIR / "valid_implementation_route_bp2_hold_action_gate.md"
)
VALID_IMPLEMENTATION_ROUTE_RETARGET_RENAME_FIXTURE = (
    FIXTURE_DIR / "valid_implementation_route_retarget_rename.md"
)
VALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE = (
    FIXTURE_DIR / "valid_merge_stable_source_truth_projection.md"
)
INVALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE = (
    FIXTURE_DIR / "invalid_merge_stable_source_truth_projection.md"
)
VALID_CROSS_FAM_DEPENDENCY_CANDIDATE_FIXTURE = (
    FIXTURE_DIR / "valid_cross_fam_dependency_candidate.md"
)
INVALID_CROSS_FAM_DEPENDENCY_UNCLASSIFIED_FIXTURE = (
    FIXTURE_DIR / "invalid_cross_fam_dependency_unclassified.md"
)
VALID_FAMILY_FEATURE_VISION_FIXTURE = (
    FIXTURE_DIR / "valid_family_feature_vision.md"
)
INVALID_FAMILY_FEATURE_VISION_SLICE_SCOPED_FIXTURE = (
    FIXTURE_DIR / "invalid_family_feature_vision_slice_scoped.md"
)
INVALID_FAMILY_FEATURE_VISION_LIVE_STATE_FIXTURE = (
    FIXTURE_DIR / "invalid_family_feature_vision_live_state_deferred.md"
)
VALID_BR2_DEFERRED_CARRYFORWARD_MATRIX_FIXTURE = (
    FIXTURE_DIR / "valid_br2_deferred_carryforward_matrix.md"
)
INVALID_BR2_DEFERRED_CARRYFORWARD_MATRIX_FIXTURE = (
    FIXTURE_DIR / "invalid_br2_deferred_carryforward_missing_applicability.md"
)
VALID_REBASELINE_ADOPTION_REVIEW_FIXTURE = (
    FIXTURE_DIR / "valid_rebaseline_adoption_review.md"
)
INVALID_REBASELINE_ADOPTION_MARKER_ONLY_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_adoption_marker_only.md"
)
INVALID_REBASELINE_ADOPTION_MISSING_CODE_TRACE_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_adoption_missing_code_trace.md"
)
INVALID_REBASELINE_ADOPTION_UNRESOLVED_GREEN_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_adoption_unresolved_nonconformance_green.md"
)
INVALID_REBASELINE_ADOPTION_MISSING_ISSUE_CANDIDATE_FIXTURE = (
    FIXTURE_DIR / "invalid_rebaseline_adoption_missing_issue_candidate.md"
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
EXPECTED_RUNTIME_DIRECT_PROOF_FAILURE_SNIPPET = (
    "must not classify diagnostic/direct runtime evidence as formal USER launcher proof"
)
EXPECTED_RUNTIME_EXACT_LAUNCHER_FAILURE_SNIPPET = (
    "must name the exact normal USER desktop runtime launcher path"
)
EXPECTED_RUNTIME_PHOTO_VIDEO_FAILURE_SNIPPET = (
    "must name photo/video, ordered frame-sequence, or focused screenshot proof"
)
EXPECTED_RUNTIME_PACKET_EVIDENCE_FAILURE_SNIPPET = (
    "must name the USER review packet, USER review hub, or UTS evidence destination"
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
EXPECTED_BRANCH_PLANNING_GATE_BYPASS_FAILURE_SNIPPET = (
    "Packet Validation Treated As USER Acceptance"
)
EXPECTED_BP1_CONTEXT_FAILURE_SNIPPET = "Project Vision Context"
EXPECTED_RAR_MARKER_ONLY_FAILURE_SNIPPET = "Rebaseline Adoption Review Missing"
EXPECTED_RAR_CODE_TRACE_FAILURE_SNIPPET = "Code-To-Visual Trace Missing"
EXPECTED_RAR_UNRESOLVED_GREEN_FAILURE_SNIPPET = (
    "Product Experience Contract Nonconformance Unresolved"
)
EXPECTED_RAR_ISSUE_CANDIDATE_FAILURE_SNIPPET = "Owned Surface Issue Candidate Missing"
EXPECTED_BP1_SHALLOW_RECOMMENDATION_FAILURE_SNIPPET = (
    "Codex Recommendations are too shallow"
)
EXPECTED_BP1_TEMPLATE_SHELL_FAILURE_SNIPPET = "template-shell BP1 wording"
EXPECTED_BP1_COPIED_SURFACE_FAILURE_SNIPPET = "copied-file list cannot be the BP1 Surface Map"
EXPECTED_BP1_GENERIC_QUESTIONS_FAILURE_SNIPPET = (
    "USER Design Questions must ask branch-specific decision-driving questions"
)
EXPECTED_BP1_SLC_CENTERED_FAILURE_SNIPPET = "BP1 cannot be SLC-centered"
EXPECTED_BP1_TECHNICAL_METADATA_FAILURE_SNIPPET = (
    "BP1 must not center active branch technical metadata"
)
EXPECTED_BP2_ACCEPTED_BP1_TRACE_FAILURE_SNIPPET = "Accepted BP1 trace"
EXPECTED_BP2_PRODUCT_DESIGN_WORDING_FAILURE_SNIPPET = (
    "BP2 must be engineering-plan-first"
)
EXPECTED_BP3_PENDING_FAILURE_SNIPPET = (
    "BP3 cannot approve implementation while BP1 or BP2 is pending"
)
EXPECTED_USER_PACKET_ACTIVE_METADATA_FAILURE_SNIPPET = (
    "USER-facing packet file contains active technical metadata"
)
EXPECTED_USER_PACKET_ZIP_HASH_FAILURE_SNIPPET = (
    "USER-facing packet file contains ZIP/hash technical metadata"
)
EXPECTED_USER_PACKET_DESKTOP_ACTIVE_UPLOAD_FAILURE_SNIPPET = (
    "USER-facing packet file routes active upload/review to Desktop or OneDrive"
)
EXPECTED_IMPLEMENTATION_ROUTE_FAILURE_SNIPPET = (
    "Implementation-bearing route required"
)
EXPECTED_BR2_NO_ROUTE_CONTINUE_FAILURE_SNIPPET = (
    "BR2 blocker packet with no concrete available route"
)
EXPECTED_BR2_MARKER_ONLY_DEFERRAL_FAILURE_SNIPPET = (
    "BR2 blocker packet must offer deferral to a concrete feature route"
)
EXPECTED_FAKE_FEATURE_LABEL_FAILURE_SNIPPET = (
    "Feature label cannot substitute for concrete implementation behavior"
)
EXPECTED_PROOF_BOUNDARY_LABEL_FAILURE_SNIPPET = (
    "Proof/setup/boundary labels cannot substitute for real feature implementation"
)
EXPECTED_TBD_IMPLEMENTATION_OUTPUT_FAILURE_SNIPPET = (
    "Implementation-bearing route cannot defer implementation output to BP2 or a later decision"
)
EXPECTED_BLANK_SELECTED_ROUTE_FAILURE_SNIPPET = (
    "Implementation-bearing route marker requires a value: Selected Implementation Route:"
)
EXPECTED_NEGATED_ROUTE_BEHAVIOR_FAILURE_SNIPPET = (
    "Implementation-bearing route cannot negate implementation behavior"
)
EXPECTED_BR2_PROOF_ONLY_ROUTE_FAILURE_SNIPPET = (
    "BR2 blocker packet concrete routes cannot be proof/readiness labels only"
)
EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET = "SLC / Slice / Seam terminology ambiguity"
EXPECTED_MERGE_STABLE_PROJECTION_FAILURE_SNIPPET = "PR creation pending"
EXPECTED_CROSS_FAM_UNCLASSIFIED_FAILURE_SNIPPET = (
    "Cross-FAM Dependency Scope Unclassified"
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
        "entry-seam recommendation",
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


def _validate_bp1_branch_vision_review_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    normalized = governance._normalized_planning_value(text)
    required_markers = (
        "USER Branch Vision Review:",
        "Review Status:",
        "Contract Status:",
        "Packet Reviewability State:",
        "USER Gate State:",
        "USER Response Proof:",
        "USER Response Digested:",
        "Project Vision Context:",
        "Family Vision Context:",
        "Feature Vision Context:",
        "Branch Goal:",
        "End-State Vision:",
        "What Will I Actually See, And Where Will I See It?:",
        "How It Will Function:",
        "User Experience Flow:",
        "Surface Map:",
        "Product Options / Design Paths:",
        "Codex Recommendations:",
        "Why This Fits The Nexus Vision:",
        "USER Design Questions:",
        "USER Response:",
        "Codex Digest:",
        "Accepted Branch Vision:",
        "Design Assumption Ledger:",
        "Acceptance / Revision / Rejection / Waiver Decision:",
    )
    for marker in required_markers:
        require(marker in text, f"BP1 Branch Vision Review missing {marker}")
    for marker in (
        "Project Vision Context:",
        "Family Vision Context:",
        "Feature Vision Context:",
        "Branch Goal:",
    ):
        value = governance._extract_marker_value(text, marker)
        require(bool(value), f"BP1 Branch Vision Review missing {marker}")
    recommendations = governance._extract_marker_value(text, "Codex Recommendations:")
    require(
        governance._planning_word_count(recommendations) >= 16
        and "placement" in recommendations.casefold()
        and "tradeoff" in recommendations.casefold(),
        "Codex Recommendations are too shallow for BP1 Branch Vision Review",
    )
    require(
        "user response" in recommendations.casefold(),
        "Codex Recommendations must leave USER response space for BP1 review",
    )
    substantive_markers = (
        "Project Vision Context:",
        "Family Vision Context:",
        "Feature Vision Context:",
        "Branch Goal:",
        "End-State Vision:",
        "What Will I Actually See, And Where Will I See It?:",
        "How It Will Function:",
        "User Experience Flow:",
        "Surface Map:",
        "Product Options / Design Paths:",
        "USER Design Questions:",
    )
    for marker in substantive_markers:
        value = governance._extract_marker_value(text, marker)
        require(
            governance._planning_word_count(value) >= 10,
            f"{marker} is too shallow for BP1 substantive review",
        )
    template_shell_phrases = (
        "review `docs/nexus_vision.md`",
        "review the relevant `docs/family_visions/` owner",
        "must explain how this branch supports",
        "family vision context: this bp1 review asks whether",
        "confirm that this branch goal is the right product direction",
        "describe the intended user-visible or source-truth end state",
        "review the copied branch-specific files and note any changes",
        "does this branch vision match what the user wants this branch to become",
        "create an accepted user-facing branch vision",
        "when bp1 closes",
        "bp1 captures",
        "option a accepts the vision, option b revises it, option c waives",
        "use this packet to decide",
        "what exact outcome should user expect to see",
        "user will see a local user hub packet",
        "the accepted bp1 vision will become the target for bp2",
        "user reads the fam-007 packet",
    )
    for phrase in template_shell_phrases:
        require(
            phrase not in normalized,
            "template-shell BP1 wording must not pass reviewability checks",
        )
    surface_map = governance._extract_marker_value(text, "Surface Map:")
    normalized_surface_map = governance._normalized_planning_value(surface_map)
    require(
        " copied as " not in normalized_surface_map
        or any(
            term in normalized_surface_map
            for term in (
                "decision surface",
                "experience surface",
                "review surface",
                "user will see",
                "owner",
            )
        ),
        "copied-file list cannot be the BP1 Surface Map",
    )
    require(
        "review surface" in normalized_surface_map
        and "decision surface" in normalized_surface_map,
        "Surface Map must distinguish review and decision surfaces",
    )
    options = governance._extract_marker_value(text, "Product Options / Design Paths:")
    require(
        "option" in options.casefold()
        and (
            "tradeoff" in options.casefold()
            or "risk" in options.casefold()
            or "defer" in options.casefold()
        ),
        "Product Options / Design Paths must include real options and tradeoffs",
    )
    user_questions = governance._extract_marker_value(text, "USER Design Questions:")
    require(
        user_questions.count("?") >= 2
        and "does this branch vision match what the user wants" not in user_questions.casefold(),
        "USER Design Questions must ask branch-specific decision-driving questions",
    )
    require(
        "bp1 center: slc" not in normalized and "slc-centered: yes" not in normalized,
        "BP1 cannot be SLC-centered; SLCs are engineering route details after vision acceptance",
    )
    for metadata_marker in (
        "Source HEAD:",
        "origin/main:",
        "Ahead/Behind:",
        "Current PR State:",
        "Worktree Cleanliness:",
    ):
        require(
            metadata_marker not in text,
            "BP1 must not center active branch technical metadata",
        )
    return failures


def _validate_bp2_branch_plan_review_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    required_markers = (
        "USER Branch Plan Review:",
        "Packet Reviewability State:",
        "USER Gate State:",
        "USER Response Proof:",
        "USER Response Digested:",
        "Accepted Branch Vision Summary:",
        "Implementation Package Summary:",
        "Branch Scope Size Test:",
        "SLC / Seam Plan:",
        "Affected Surfaces:",
        "Likely Files:",
        "Validators / Helpers:",
        "Proof Requirements:",
        "Element-to-Phase Proof Matrix:",
        "H1 Expectations:",
        "LV / UTS Expectations:",
        "Rollback / Safety Plan:",
        "Future-Gated Boundaries:",
        "Plan Acceptance Checklist:",
        "Exact BP3 Approval Text:",
    )
    for marker in required_markers:
        require(marker in text, f"BP2 Branch Plan Review missing {marker}")
    accepted_trace = governance._extract_marker_value(text, "Accepted Branch Vision Summary:")
    require(
        "bp1 accepted" in accepted_trace.casefold()
        or "bp1 waived" in accepted_trace.casefold(),
        "Accepted BP1 trace is required before BP2 can be green",
    )
    stale_product_design_phrases = (
        "required user-facing product/design planning gate",
        "Do I actually like what Codex is about to build",
        "USER Branch Plan Contract: a required user-facing product/design",
    )
    for phrase in stale_product_design_phrases:
        require(
            phrase.casefold() not in text.casefold(),
            "BP2 must be engineering-plan-first and must not reuse BP1/product-design contract wording",
        )
    substantive_markers = (
        "Implementation Package Summary:",
        "Branch Scope Size Test:",
        "SLC / Seam Plan:",
        "Affected Surfaces:",
        "Likely Files:",
        "Validators / Helpers:",
        "Proof Requirements:",
        "Element-to-Phase Proof Matrix:",
        "H1 Expectations:",
        "LV / UTS Expectations:",
        "Rollback / Safety Plan:",
        "Future-Gated Boundaries:",
        "Plan Acceptance Checklist:",
        "Exact BP3 Approval Text:",
    )
    for marker in substantive_markers:
        value = governance._extract_marker_value(text, marker)
        require(
            governance._planning_word_count(value) >= 10,
            f"{marker} is too shallow for BP2 substantive engineering-plan review",
        )
    normalized = governance._normalized_planning_value(text)
    for phrase in (
        "see copied files",
        "see source files",
        "implementation options: accept revise waive reject",
        "generic implementation plan",
        "tbd",
        "placeholder",
    ):
        require(
            phrase not in normalized,
            "BP2 template-shell review artifact must not pass reviewability checks",
        )
    return failures


def _validate_bp3_orchestration_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    normalized = governance._normalized_planning_value(text)
    for marker in (
        "BP1 Contract Status:",
        "BP2 Contract Status:",
        "BP1 USER Gate State:",
        "BP2 USER Gate State:",
        "BP3 Packet Reviewability State:",
        "BP3 USER Gate State:",
        "Branch Plan Matches Accepted Branch Vision:",
        "Branch Package Size:",
        "SLC Traceability:",
        "Future-Gated Boundaries:",
        "Workstream Entry Seam:",
        "Implementation Approval:",
    ):
        require(marker in text, f"BP3 Orchestration Validation missing {marker}")
    bp1 = governance._normalized_planning_value(
        governance._extract_marker_value(text, "BP1 Contract Status:")
    )
    bp2 = governance._normalized_planning_value(
        governance._extract_marker_value(text, "BP2 Contract Status:")
    )
    bp1_gate = governance._normalized_planning_value(
        governance._extract_marker_value(text, "BP1 USER Gate State:")
    )
    bp2_gate = governance._normalized_planning_value(
        governance._extract_marker_value(text, "BP2 USER Gate State:")
    )
    bp3_gate = governance._normalized_planning_value(
        governance._extract_marker_value(text, "BP3 USER Gate State:")
    )
    implementation_approval = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Implementation Approval:")
    )
    if "approve" in implementation_approval or "approved" in implementation_approval:
        require(
            bp1.startswith(("complete", "waived by user"))
            and bp2.startswith(("complete", "waived by user")),
            "BP3 cannot approve implementation while BP1 or BP2 is pending",
        )
        require(
            bp1_gate.startswith(("user accepted", "user waived"))
            and bp2_gate.startswith(("user accepted", "user waived"))
            and bp3_gate.startswith(("user approved", "user waived")),
            "BP3 cannot approve implementation while a USER review gate is pending",
        )
    require(
        "slc traceability: complete" in normalized,
        "BP3 requires complete SLC traceability to BP1 and BP2",
    )
    substantive_markers = (
        "Branch Plan Matches Accepted Branch Vision:",
        "Branch Package Size:",
        "Future-Gated Boundaries:",
        "Workstream Entry Seam:",
        "Implementation Approval:",
    )
    for marker in substantive_markers:
        value = governance._extract_marker_value(text, marker)
        require(
            governance._planning_word_count(value) >= 8,
            f"{marker} is too shallow for BP3 substantive orchestration review",
        )
    if "approved" in implementation_approval or "approve" in implementation_approval:
        require(
            (
                "admitted same-branch workstream package" in implementation_approval
                or "bounded workstream package" in implementation_approval
            )
            and "entry checkpoint" in implementation_approval
            and "workstream green" in implementation_approval,
            "BP3 implementation approval must name bounded Workstream package execution, entry checkpoint, and Workstream Green continuation",
        )
    return failures


def _validate_branch_planning_gate_state_packet_text(text: str) -> list[str]:
    substantive_bp1_text = (
        "# Fixture USER Branch Vision Review\n\n"
        "USER Branch Vision Review: BP1\n\n"
        "## Packet Reviewability State\nReviewable\n\n"
        "## USER Gate State\nPending USER Review\n\n"
        "## USER Response Proof\nPending USER response.\n\n"
        "## USER Response Digested\nNo - pending USER response.\n\n"
        "## Project Vision Context\n"
        "This fixture keeps Nexus branch planning USER-readable before engineering work by proving packet reviewability and USER acceptance stay separate states.\n\n"
        "## Family Vision Context\n"
        "The fixture family context requires branch-specific review gates, clear owner routing, and no implementation authority before USER closes the gate.\n\n"
        "## Feature Vision Context\n"
        "This review-gate feature protects BP1, BP2, and BP3 packets from becoming false implementation approvals when only reviewability was proven.\n\n"
        "## Branch Goal\n"
        "Demonstrate that the branch planning packet can be reviewable while USER acceptance remains pending and Workstream implementation stays blocked.\n\n"
        "## End-State Vision\n"
        "USER receives a readable planning packet where reviewability, gate state, response proof, and implementation authority are each explicit and auditable.\n\n"
        "## What Will I Actually See, And Where Will I See It?\n"
        "USER sees the BP1 review file in the local USER review packet and can distinguish navigation context from the actual decision surface.\n\n"
        "## How It Will Function\n"
        "BP1 prepares the vision for review, BP2 waits for a legal USER response, and BP3 cannot request implementation while earlier gates remain open.\n\n"
        "## User Experience Flow\n"
        "USER opens START_HERE, reviews the branch vision, checks pending decisions, and responds before Codex can prepare the next planning gate.\n\n"
        "## Surface Map\n"
        "Review surface is USER_BRANCH_VISION_REVIEW.md; decision surface is the USER response; proof surface is the Codex digest; later BP2 and BP3 files trace to this gate state.\n\n"
        "## Product Options / Design Paths\n"
        "Option A keeps the packet reviewable with USER response pending until a clear receipt arrives, with the tradeoff that later stages wait. Option B revises the review packet before acceptance if the vision, decision surface, or proof path is unclear, reducing risk before BP2. Option C waives or rejects the gate with explicit USER text and keeps later stages bounded or deferred.\n\n"
        "## Codex Recommendations\n"
        "Recommendation one keeps reviewability and acceptance independent because packet hygiene can pass while USER intent remains undecided, with the tradeoff that later stages must wait for a clear receipt. USER response: pending. Recommendation two keeps implementation language blocked because false green validation is the core risk this fixture protects against. USER response: pending.\n\n"
        "## Why This Fits The Nexus Vision\n"
        "This supports Nexus by making governance decisions inspectable, USER-controlled, and resistant to Codex treating generated artifacts as permission.\n\n"
        "## USER Design Questions\n"
        "Should this review gate remain pending until USER gives explicit acceptance text? Which packet field should Codex cite as proof before preparing the next gate?\n"
    )
    packet_files = {
        "START_HERE.md": text
        + "\nPrimary USER Review File: `USER Review/USER_BRANCH_PLAN_REVIEW.md`\n",
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/{review_bundle.USER_BRANCH_VISION_REVIEW_FILE}": substantive_bp1_text,
        f"{review_bundle.USER_REVIEW_DIR_NAME}/{review_bundle.USER_BRANCH_PLAN_REVIEW_FILE}": text,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/USER_REVIEW_FOLDER_AND_FILE_DIGEST.md": text,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/GOVERNANCE_REQUIRED_FILES_SCAN.md": text,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": text,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/BRANCH_VISION_VALIDATION_CHECKLIST.md": text,
        f"{review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME}/Main.md": text,
    }
    result = review_bundle._validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch="fixture-branch",
        expected_head="0" * 40,
        expected_origin_main="1" * 40,
    )
    return result.failures


def _validate_user_packet_metadata_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    active_metadata_markers = (
        "HEAD",
        "Source HEAD:",
        "origin/main:",
        "Merge Base:",
        "Ahead/Behind:",
        "Upstream:",
        "Worktree Cleanliness:",
        "Validation Status:",
        "PR State:",
        "Current Branch State:",
    )
    for marker in active_metadata_markers:
        require(
            marker not in text,
            "USER-facing packet file contains active technical metadata",
        )
    hash_markers = (
        "ZIP SHA",
        "ZIP SHA256",
        "ZIP hash",
        "packet hash",
        "upload hash",
    )
    for marker in hash_markers:
        require(
            marker.casefold() not in text.casefold(),
            "USER-facing packet file contains ZIP/hash technical metadata",
        )
    active_upload_markers = (
        "Desktop review bundle",
        "USER Desktop review bundle",
        "OneDrive active review path",
        "Upload from C:\\Users\\anden\\OneDrive\\Desktop",
        "Upload ZIP: C:\\Users\\anden\\OneDrive\\Desktop",
        "Review Location: C:\\Users\\anden\\OneDrive\\Desktop",
    )
    for marker in active_upload_markers:
        require(
            marker.casefold() not in text.casefold(),
            "USER-facing packet file routes active upload/review to Desktop or OneDrive",
        )
    return failures


def _validate_implementation_bearing_route_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    required_markers = (
        "Selected Implementation Route:",
        "Implementation Route Class:",
        "Concrete Deliverable:",
        "Implementation Output:",
        "Infrastructure / Setup Relationship:",
        "USER Action Gate:",
        "Route Disposition:",
        "Retarget / Rename Recommendation:",
    )
    for marker in required_markers:
        require(marker in text, f"Implementation-bearing route missing {marker}")

    def same_line_marker_value(marker: str) -> str:
        normalized_marker = marker.rstrip(":")
        pattern = re.compile(
            rf"^[ \t]*(?:-[ \t]*)?{re.escape(normalized_marker)}:"
            r"[ \t]*`?([^\r\n]*?)`?[ \t]*$",
            flags=re.M,
        )
        matches = pattern.findall(text)
        if not matches:
            return ""
        return matches[-1].strip().strip("`").strip()

    marker_values = {
        marker: same_line_marker_value(marker) for marker in required_markers
    }
    for marker, value in marker_values.items():
        require(
            bool(governance._normalized_planning_value(value)),
            f"Implementation-bearing route marker requires a value: {marker}",
        )

    selected_route = marker_values["Selected Implementation Route:"]
    deliverable = marker_values["Concrete Deliverable:"]
    implementation_output = marker_values["Implementation Output:"]
    setup_relationship = marker_values["Infrastructure / Setup Relationship:"]
    user_gate = marker_values["USER Action Gate:"]
    route_disposition = marker_values["Route Disposition:"]
    retarget = marker_values["Retarget / Rename Recommendation:"]
    combined_route = governance._normalized_planning_value(
        "\n".join((selected_route, deliverable, implementation_output))
    )
    setup_normalized = governance._normalized_planning_value(setup_relationship)
    disposition_normalized = governance._normalized_planning_value(route_disposition)
    retarget_normalized = governance._normalized_planning_value(retarget)
    full_normalized = governance._normalized_planning_value(text)

    concrete_terms = (
        "implementation",
        "enforcement",
        "runtime",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "consent shell",
        "trust-boundary",
        "security",
        "capability-pack",
        "memory/cache",
        "provider",
        "user-facing",
        "workflow",
    )
    concrete_behavior_terms = (
        "enforce",
        "block",
        "validate",
        "fail-closed",
        "detect",
        "route",
        "render",
        "persist",
        "execute",
        "launch",
        "open",
        "save",
        "load",
        "sync",
        "consent",
        "control",
        "runtime",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "user-facing",
    )
    actual_implementation_terms = (
        "implement",
        "implements",
        "implemented",
        "enforce",
        "enforces",
        "enforcement",
        "block",
        "blocks",
        "blocked",
        "reject",
        "rejects",
        "prevent",
        "prevents",
        "fail-closed",
        "fails closed",
        "validate",
        "validates",
        "render",
        "renders",
        "persist",
        "persists",
        "execute",
        "executes",
        "route",
        "routes",
        "disable",
        "disables",
        "update",
        "updates",
        "create",
        "creates",
    )
    implemented_target_terms = (
        "behavior",
        "control",
        "workflow",
        "surface",
        "state",
        "transition",
        "enforcement",
        "consent shell",
        "consent-shell",
        "trust-boundary",
        "boundary",
        "exclusion",
        "suppression",
        "validator",
        "helper",
        "source-truth",
        "source truth",
        "runtime",
        "user-facing",
    )
    evidence_only_route_terms = (
        "proof package",
        "proof packet",
        "validation proof",
        "setup proof",
        "packet proof",
        "readiness proof",
        "registry proof",
        "boundary proof",
        "proof-only",
        "proof as",
        "proof of",
        "review packet",
        "packet generation",
        "decision path",
        "decision-ready",
        "readiness matrix",
        "validation plan",
        "planning candidate",
        "boundary controls",
        "boundary-control labels",
    )
    tbd_route_terms = (
        "implementation output is tbd",
        "tbd",
        "to be determined",
        "figured out later",
        "will be figured out",
        "will choose",
        "choose the validator",
        "decide later",
        "selected later",
        "later during bp2",
        "after user reviews more options",
        "bp2 will choose",
        "bp2 will decide",
    )
    negated_real_behavior_terms = (
        "does not add behavior",
        "does not add implementation",
        "does not add state",
        "does not change behavior",
        "does not change state",
        "does not enforce",
        "does not implement",
        "doesn't add behavior",
        "doesn't add implementation",
        "doesn't change behavior",
        "doesn't change state",
        "doesn't enforce",
        "doesn't implement",
        "will not add behavior",
        "will not add implementation",
        "will not change behavior",
        "will not change state",
        "will not enforce",
        "will not implement",
        "no enforcement behavior",
        "no helper behavior",
        "no implemented behavior",
        "no implemented control",
        "no validator behavior",
        "no runtime behavior",
        "no source-truth behavior",
        "no source truth behavior",
        "no user-facing surface",
        "no state transition",
        "no behavior changes",
        "behavior changes are deferred",
        "changes are deferred",
        "behavior is deferred",
        "without implemented behavior",
        "without naming the control behavior",
        "without naming the actual control",
    )
    planning_only_terms = (
        "planning-only",
        "readiness-only",
        "setup-only",
        "lane setup only",
        "choose later branches",
        "identify later branches",
        "no implementation route",
        "no product/runtime/source-truth/helper deliverable",
        "implementation output: none",
    )
    fake_feature_terms = (
        "setup feature",
        "readiness feature",
        "planning feature",
        "decision feature",
        "decision matrix feature",
        "registry feature",
        "skeleton feature",
        "packet feature",
        "review feature",
        "feature implementation label",
        "feature label",
    )
    real_behavior_present = (
        any(term in combined_route for term in actual_implementation_terms)
        and any(term in combined_route for term in implemented_target_terms)
        and not any(term in combined_route for term in negated_real_behavior_terms)
    )
    negated_real_behavior_detected = any(
        term in combined_route for term in negated_real_behavior_terms
    )
    evidence_only_detected = any(
        term in combined_route for term in evidence_only_route_terms
    )
    require(
        governance._planning_word_count(deliverable) >= 8
        and governance._planning_word_count(implementation_output) >= 8
        and any(term in combined_route for term in concrete_terms)
        and real_behavior_present
        and not any(term in combined_route for term in planning_only_terms),
        (
            "Implementation-bearing route required: concrete deliverable and "
            "implementation output must be named before BP1"
        ),
    )
    require(
        not negated_real_behavior_detected,
        (
            "Implementation-bearing route cannot negate implementation behavior: "
            "name the control, behavior, surface, or state transition that "
            "Workstream will implement or enforce"
        ),
    )
    require(
        not evidence_only_detected or real_behavior_present,
        (
            "Proof/setup/boundary labels cannot substitute for real feature "
            "implementation: name the actual control, behavior, surface, or "
            "state transition Workstream will implement or enforce"
        ),
    )
    require(
        not any(term in combined_route for term in tbd_route_terms),
        (
            "Implementation-bearing route cannot defer implementation output "
            "to BP2 or a later decision: name the actual route behavior before BP1"
        ),
    )
    fake_feature_detected = any(term in combined_route for term in fake_feature_terms)
    negated_behavior_terms = (
        "no runtime",
        "no source-truth",
        "no source truth",
        "no helper",
        "no validator",
        "no enforcement",
        "no consent-shell",
        "no user-facing",
        "no boundary behavior",
        "no behavior changes",
        "without runtime",
        "without source-truth",
        "without source truth",
        "without helper",
        "without validator",
        "without enforcement",
        "without user-facing",
        "without boundary behavior",
    )
    require(
        not fake_feature_detected
        or (
            real_behavior_present
            and any(term in combined_route for term in concrete_behavior_terms)
            and not any(term in combined_route for term in negated_behavior_terms)
        ),
        (
            "Feature label cannot substitute for concrete implementation behavior: "
            "name the behavior, source-truth/helper/validator/runtime output, and proof"
        ),
    )

    if any(
        term in full_normalized
        for term in (
            "lane setup",
            "repo/root/remote",
            "private root",
            "private remote",
            "skeleton setup",
            "registry creation",
        )
    ):
        require(
            "execution-enabling" in setup_normalized
            or "selected implementation route" in setup_normalized
            or "exact user action gate" in setup_normalized,
            (
                "Infrastructure/setup work must be tied to the selected "
                "implementation route or an exact USER action gate"
            ),
        )

    require(
        "Dev lane" not in text,
        "Use Developer lane, not Dev lane, in current branch-planning text",
    )
    if "developer" in full_normalized:
        require(
            "Developer lane" in text,
            "Developer lane terminology must be explicit when developer lane scope appears",
        )

    if "hold" in disposition_normalized:
        exact_gate = governance._extract_marker_value(text, "Exact USER Action Gate:")
        blocked_scope = governance._extract_marker_value(text, "Blocked Scope:")
        require(
            governance._planning_word_count(exact_gate) >= 10,
            "BP2 HOLD requires an exact USER action gate",
        )
        require(
            governance._planning_word_count(blocked_scope) >= 8,
            "BP2 HOLD requires blocked scope",
        )
    if "retarget" in disposition_normalized or "rename" in disposition_normalized:
        require(
            ("retarget" in retarget_normalized or "rename" in retarget_normalized)
            and any(term in retarget_normalized for term in concrete_terms),
            "Route retarget/rename disposition requires a concrete recommendation",
        )

    require(
        governance._planning_word_count(user_gate) >= 6,
        "Implementation-bearing route must name pending USER action gate posture",
    )
    return failures


def _validate_cross_fam_dependency_packet_text(text: str) -> list[str]:
    record_starts = list(
        re.finditer(r"(?im)^\s*(?:-\s*)?Cross-FAM Dependency Map:", text)
    )
    if len(record_starts) > 1:
        failures: list[str] = []
        for index, record_start in enumerate(record_starts):
            record_end = (
                record_starts[index + 1].start()
                if index + 1 < len(record_starts)
                else len(text)
            )
            record_text = text[record_start.start() : record_end]
            failures.extend(
                f"Cross-FAM dependency record {index + 1}: {failure}"
                for failure in _validate_cross_fam_dependency_packet_text(record_text)
            )
        return failures

    failures, require = _collect_failures()
    required_markers = (
        "Cross-FAM Dependency Map:",
        "Dependency ID:",
        "Originating FAM:",
        "Originating FFV / Element:",
        "Affected FAMs:",
        "Affected FFV / Element or Not Created:",
        "Dependency Scope Class:",
        "Carry-In / Deferral / Transfer Decision:",
        "Required Contract / Capability:",
        "Suggested Grouping:",
        "Proof Expectation:",
        "Durable Disposition:",
        "Affected FAM Receipt / Fold-Down Target:",
        "Worktree-To-Worktree Mutation:",
    )
    for marker in required_markers:
        require(marker in text, f"Cross-FAM dependency packet missing {marker}")

    normalized_text = governance._normalized_planning_value(text)
    scope_class = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Dependency Scope Class")
    )
    affected_fams = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Affected FAMs")
    )
    affected_ffv = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Affected FFV / Element or Not Created")
    )
    disposition = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Durable Disposition")
    )
    receipt = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Affected FAM Receipt / Fold-Down Target")
    )
    mutation = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Worktree-To-Worktree Mutation")
    )

    allowed_scope_classes = {
        "awareness only",
        "compatibility default",
        "future adoption",
        "local fam only",
        "cross-fam awareness",
        "dependency-bounded cross-fam work",
        "priority carry-in",
        "platform contract",
        "coordinated cross-fam patch",
        "repo-wide migration / halt",
        "transferred fam work",
    }
    require(
        scope_class in allowed_scope_classes,
        "Cross-FAM Dependency Scope Unclassified",
    )
    require(
        "fam-" in affected_fams.casefold(),
        "Cross-FAM dependency packet must name affected FAM ownership",
    )
    require(
        "not created" in affected_ffv.casefold()
        or re.search(r"\bF\d+-FF\d{2}(?:-E\d{2})?\b", affected_ffv, re.IGNORECASE),
        "Cross-FAM dependency packet must name affected FFV / element or Not Created",
    )
    require(
        disposition
        and disposition.casefold()
        not in {"pending", "todo", "tbd", "none", "n/a", "not applicable"},
        "Cross-FAM dependency packet requires a durable disposition",
    )
    require(
        receipt
        and receipt.casefold()
        not in {"pending", "todo", "tbd", "none", "n/a", "not applicable"},
        "Cross-FAM dependency packet requires affected-FAM receipt or fold-down target",
    )
    require(
        "blocked" in mutation.casefold()
        or "not approved" in mutation.casefold()
        or "none" in mutation.casefold(),
        "Cross-FAM dependency packet must block direct worktree-to-worktree mutation",
    )
    live_repo_ledger_terms = (
        "current branch status",
        "active worktree assignment",
        "selected-next truth",
        "pending pr",
        "release-window status",
        "live dependency queue",
    )
    for term in live_repo_ledger_terms:
        require(
            term not in normalized_text,
            f"Cross-FAM dependency packet must not create repo live-state ledger term: {term}",
        )
    return failures


def _owning_fam_from_ffv(path: Path, text: str) -> str:
    candidates = (
        re.search(r"\bFAM-(\d{3})\b", path.name),
        re.search(r"\bF(\d+)-FF\d{2}\b", path.name, re.IGNORECASE),
        re.search(r"\bF(\d+)-FF\d{2}\b", text, re.IGNORECASE),
    )
    for match in candidates:
        if not match:
            continue
        raw = match.group(1)
        if len(raw) == 3:
            return f"FAM-{raw}"
        return f"FAM-{int(raw):03d}"
    return ""


def _validate_family_feature_vision_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    required_markers = (
        "Family Feature Vision ID:",
        "Parent FAM:",
        "Feature Category:",
        "Category-Level Purpose:",
        "USER-Facing Surfaces:",
        "Experience Flow:",
        "Included Capabilities:",
        "Explicit Non-Goals:",
        "Durable Feature Element Inventory:",
        "Deferred Feature Carryforward:",
        "Design Options:",
        "Proof Expectations:",
        "Branch Readiness Consumption Notes:",
        "BP1 Context Notes:",
        "Fold-Down History:",
        "Active-State Wording Scan:",
    )
    for marker in required_markers:
        require(marker in text, f"Family Feature Vision missing {marker}")
        value = governance._extract_marker_value(text, marker)
        require(bool(value), f"Family Feature Vision must give a real value for {marker}")

    ffv_id = governance._extract_marker_value(text, "Family Feature Vision ID:")
    parent_fam = governance._extract_marker_value(text, "Parent FAM:")
    feature_category = governance._extract_marker_value(text, "Feature Category:")
    normalized_category = governance._normalized_planning_value(feature_category)
    require(
        re.search(r"\bF\d+-FF\d{2}\b", ffv_id) is not None,
        "Family Feature Vision Compact ID Missing",
    )
    require(
        re.search(r"\bFAM-\d{3}\b", parent_fam) is not None,
        "Family Feature Vision Parent FAM Missing",
    )
    require(
        not any(
            term in normalized_category
            for term in (
                "slice",
                "slc",
                "seam",
                "branch route",
                "implementation package",
                "selected next",
            )
        ),
        "Family Feature Vision Slice-Scoped",
    )

    element_inventory = governance._extract_marker_value(
        text,
        "Durable Feature Element Inventory:",
    )
    require(
        re.search(r"\bF\d+-FF\d{2}-E\d{2}\b", element_inventory) is not None,
        "FFV Element Proof Chain Missing",
    )

    deferred = governance._extract_marker_value(text, "Deferred Feature Carryforward:")
    normalized_deferred = governance._normalized_planning_value(deferred)
    for term in ("deferred item", "dependency trigger", "grouping recommendation", "proof expectation", "durable disposition"):
        require(
            term in normalized_deferred,
            f"Deferred Feature Carryforward missing {term}",
        )
    live_state_terms = (
        "active",
        "current branch",
        "selected next",
        "pending pr",
        "in progress",
        "next branch",
        "release window status",
    )
    for term in live_state_terms:
        require(
            re.search(rf"\b{re.escape(term)}\b", normalized_deferred) is None,
            f"FFV Live-State Leakage: Deferred Feature Carryforward contains {term}",
        )

    return failures


def _validate_br2_deferred_carryforward_matrix_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    required_markers = (
        "Option name:",
        "Main feature/package objective:",
        "Applicable deferred carryforward items:",
        "Reason each deferred item is applicable:",
        "Dependency trigger:",
        "Recommended grouping:",
        "Deferred items that remain future-gated:",
        "Reason future-gated items remain deferred:",
        "Validation/proof expectations:",
    )
    for marker in required_markers:
        require(marker in text, f"BR2 Deferred Carryforward matrix missing {marker}")
        require(
            bool(governance._extract_marker_value(text, marker)),
            f"BR2 Deferred Carryforward matrix must give a real value for {marker}",
        )
    normalized = governance._normalized_planning_value(text)
    require(
        "deferred item" in normalized or "none" in governance._normalized_planning_value(
            governance._extract_marker_value(text, "Applicable deferred carryforward items:")
        ),
        "Deferred Carryforward Applicability Missing",
    )
    require(
        "dependency trigger" in normalized,
        "Deferred Carryforward Applicability Missing: dependency trigger not explained",
    )
    require(
        "grouping recommendation" in normalized,
        "Deferred Carryforward Applicability Missing: grouping recommendation not explained",
    )
    require(
        "separate branch for every deferred item" not in normalized
        and "one branch per deferred item" not in normalized,
        "Deferred Carryforward Branch Sprawl",
    )
    return failures


def _validate_rebaseline_adoption_review_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    normalized = governance._normalized_planning_value(text)

    required_markers = (
        "RAR Stage:",
        "Trigger Reason:",
        "Source-Truth Files Loaded:",
        "Incoming Standard / Change Summary:",
        "Merged Standard Source:",
        "Rebaseline / Re-entry Event:",
        "Current Branch Implementation Inventory:",
        "Owned Surface Inventory:",
        "Affected File Inventory:",
        "Affected Surface Inventory:",
        "Affected Branch Artifacts:",
        "Affected Product Surfaces:",
        "Implemented / Touched UI-UX Surfaces:",
        "Implemented / Touched Runtime-Backend Surfaces:",
        "Affected Proof Claims:",
        "Merged Standard Comparison Result:",
        "Frontend / Backend Contract Findings:",
        "Reference / Template / Primitive Classification:",
        "Accepted Reference Set / Comparative Synthesis:",
        "Accepted Reference / Template / Primitive Comparator Matrix:",
        "UI Reference / Template / Shared Primitive Dependency:",
        "NDAI Product Experience Contract Comparison:",
        "UI Element Inventory:",
        "Backend / State Ownership Trace:",
        "Screenshot / Video / Contact-Sheet Evidence:",
        "Visual Element / Element-Group Inspection Ledger:",
        "Vision-To-Proof Matrix:",
        "Scope Coverage Manifest:",
        "Owned-Surface Nonconformance Ledger:",
        "Current Branch Repair Candidates:",
        "Previous / Historical Branch Issue Candidates:",
        "Current Violation Findings:",
        "Issue-Candidate Table:",
        "Repair / Waiver / Defer / Route Decision Table:",
        "Adoption Disposition:",
        "Repair / Waiver / Blocker:",
        "Validation Summary:",
        "USER Packet Path:",
        "USER Packet ZIP Path:",
        "Exact Next USER Decision:",
        "No Repo Live-State Tracking:",
    )
    for marker in required_markers:
        value = governance._extract_marker_value(text, marker)
        require(bool(value), f"Rebaseline Adoption Review Missing: {marker}")
        require(
            governance._planning_word_count(value) >= 3,
            f"Rebaseline Adoption Review Missing: {marker} is too shallow",
        )

    rar_stage = governance._extract_marker_value(text, "RAR Stage:")
    require(
        re.search(r"\bRAR[0-4]\b|Resolved|No Applicable Impact", rar_stage) is not None,
        "Rebaseline Adoption Review Missing: RAR Stage must name RAR0-RAR4 or a resolved disposition",
    )

    code_trace_header = (
        "| Surface | Element Group | Source File / Code Region | Backend / State Owner | "
        "Rendered Evidence | Accepted Reference | Visual Match | Behavior Match | "
        "Status | Defect / Gap | Next Legal Action |"
    )
    accepted_reference_header = (
        "| Element Class | Implementation Authority | Accepted Reference Set | "
        "Invariant Traits | Feature-Specific Traits | Target Surface | "
        "Primitive/Template/Reference-Derived/Exception | Evidence | Gap / Issue |"
    )
    issue_candidate_header = (
        "| Issue Candidate | Owner FAM | Surface | Element Group | Defect Class | "
        "Evidence | Proposed Carrier | GitHub Issue Mutation Approved? |"
    )
    rar_decision_header = (
        "| RAR USER Decision | Meaning | What It Authorizes | What It Does Not Authorize |"
    )
    require(code_trace_header in text, "Code-To-Visual Trace Missing")
    require(
        accepted_reference_header in text,
        "Accepted Reference Comparator Missing",
    )
    require(issue_candidate_header in text, "Owned Surface Issue Candidate Missing")
    require(rar_decision_header in text, "RAR USER Packet Missing")

    for quality in (
        "deterministic",
        "intuitive",
        "immersive",
        "predictable",
        "reliable",
        "consistent",
    ):
        require(
            quality in normalized,
            "NDAI Product Experience Contract Comparison Missing",
        )

    for forbidden in (
        "validator green is sufficient",
        "helper pass is sufficient",
        "screenshot exists therefore accepted",
        "template consumed without approved source",
        "shared primitive consumed without approved source",
    ):
        require(
            forbidden not in normalized,
            "Circular Validation Evidence",
        )

    user_packet_path = governance._extract_marker_value(text, "USER Packet Path:")
    user_packet_zip = governance._extract_marker_value(text, "USER Packet ZIP Path:")
    require(
        "c:\\nexus user" in user_packet_path.casefold()
        or "not required" in user_packet_path.casefold(),
        "RAR USER Packet Missing",
    )
    require(
        re.search(r"[A-Za-z0-9_-]+-\d{8}-\d{6}\.zip", user_packet_zip) is not None
        or "not required" in user_packet_zip.casefold(),
        "RAR USER Packet Missing",
    )

    no_live_state = governance._extract_marker_value(text, "No Repo Live-State Tracking:")
    require(
        "c:\\nexus governance state" in no_live_state.casefold()
        or "external" in no_live_state.casefold(),
        "RAR Live Adoption Ledger In Repo",
    )

    issue_table = governance._extract_marker_value(text, "Issue-Candidate Table:")
    previous_candidates = governance._extract_marker_value(
        text, "Previous / Historical Branch Issue Candidates:"
    )
    if "none" not in previous_candidates.casefold():
        require(
            "issue candidate" in issue_table.casefold()
            and "github issue mutation approved" in text.casefold(),
            "Owned Surface Issue Candidate Missing",
        )

    adoption_disposition = governance._extract_marker_value(
        text, "Adoption Disposition:"
    )
    unresolved_statuses = (
        "NONCONFORMING",
        "UNPROVEN",
        "PARTIAL",
        "EXCEPTION NEEDED",
        "SOURCE-TRUTH GAP",
        "REFERENCE GAP",
        "TEMPLATE GAP",
        "SHARED PRIMITIVE GAP",
    )
    unresolved_present = any(status in text for status in unresolved_statuses)
    claims_green = "Adoption Green With Evidence" in adoption_disposition
    require(
        not (unresolved_present and claims_green),
        "Product Experience Contract Nonconformance Unresolved",
    )

    if "ISSUE CANDIDATE" in text:
        decision_table = governance._extract_marker_value(
            text, "Repair / Waiver / Defer / Route Decision Table:"
        )
        require(
            "USER review" in decision_table
            or "pending USER" in decision_table
            or "issue candidate" in decision_table.casefold(),
            "Issue Candidate Disposition Missing",
        )

    normal_phase = governance._extract_marker_value(text, "Next Legal Phase:")
    if normal_phase:
        require(
            "normal phase progression" not in normal_phase.casefold()
            or "blocked" not in normalized,
            "Normal Phase Progression Blocked By RAR",
        )
    return failures


def _validate_family_feature_vision_scaffolding_source_truth() -> list[str]:
    failures: list[str] = []
    ffv_dir = ROOT / "Docs" / "family_feature_visions"
    expected_files = {
        "README.md": (
            "Family Feature Vision",
            "durable feature-category",
            "Deferred Feature Carryforward",
            "not active branch state",
        ),
        "index.md": (
            "Family Feature Vision Index",
            "F<family>-FF<two digits>",
            "compact durable registry",
        ),
        "TEMPLATE.md": (
            "Family Feature Vision ID:",
            "Feature Category:",
            "Deferred Feature Carryforward:",
            "Active-State Wording Scan:",
        ),
    }
    if not ffv_dir.is_dir():
        return ["Missing generic Family Feature Vision scaffolding directory: Docs/family_feature_visions"]
    for file_name, markers in expected_files.items():
        path = ffv_dir / file_name
        if not path.is_file():
            failures.append(f"Missing generic Family Feature Vision scaffold file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(
                    f"{path.relative_to(ROOT)} missing Family Feature Vision scaffold marker {marker!r}"
                )
    return failures


def _iter_current_worktree_ffv_content_files() -> list[Path]:
    ffv_dir = ROOT / "Docs" / "family_feature_visions"
    if not ffv_dir.is_dir():
        return []
    scaffold_names = {"index.md", "readme.md", "template.md"}
    return sorted(
        path
        for path in ffv_dir.glob("*.md")
        if path.name.casefold() not in scaffold_names
    )


def _validate_current_worktree_family_feature_vision_files() -> list[str]:
    """Apply the binding FFV content standard to admitted repo FFV files."""

    failures: list[str] = []
    for path in _iter_current_worktree_ffv_content_files():
        text = path.read_text(encoding="utf-8")
        for failure in _validate_family_feature_vision_text(text):
            failures.append(f"{path.relative_to(ROOT)}: {failure}")
    return failures


def _validate_current_worktree_ffv_dependency_records() -> list[str]:
    """Scan tracked FFVs in the current worktree for loose cross-FAM dependencies."""

    failures: list[str] = []

    trigger_terms = (
        "dependency",
        "carry-in",
        "platform contract",
        "affected fam",
        "installer",
        "packaging",
        "shortcut",
        "update",
        "patch",
    )
    for path in _iter_current_worktree_ffv_content_files():
        text = path.read_text(encoding="utf-8")
        owning_fam = _owning_fam_from_ffv(path, text)
        mentioned_fams = sorted(set(re.findall(r"\bFAM-\d{3}\b", text)))
        other_fams = [fam for fam in mentioned_fams if fam != owning_fam]
        normalized_text = governance._normalized_planning_value(text)
        if not other_fams:
            continue
        if not any(term in normalized_text for term in trigger_terms):
            continue
        if "Cross-FAM Dependency" not in text and "Dependency Scope Class:" not in text:
            failures.append(
                f"{path.relative_to(ROOT)}: Cross-FAM dependency content mentions "
                f"{', '.join(other_fams)} but lacks a Cross-FAM Dependency record"
            )
            continue
        record_failures = _validate_cross_fam_dependency_packet_text(text)
        if record_failures:
            failures.append(
                f"{path.relative_to(ROOT)}: Cross-FAM dependency record invalid: "
                + "; ".join(record_failures[:5])
            )
    return failures


def _validate_implementation_bearing_source_truth() -> list[str]:
    failures, require = _collect_failures()
    source_truth_markers = {
        ROOT / "Docs" / "phase_governance.md": (
            "Implementation-Bearing Branch Standard",
            "Branch / Slice / SLC / Seam Terminology Model",
            "Selected Implementation Route:",
            "Real Feature Implementation Definition",
            "BR2 Blocker Packet Rule",
            "Slice Definition:",
            "SLC Classification:",
            "Seam Definition:",
            "Multi-Slice Branch Rule:",
            "Developer lane",
        ),
        ROOT / "Docs" / "branch_plans" / "README.md": (
            "Implementation-Bearing Route Requirement",
            "Real feature implementation",
            "Infrastructure / Lane Groundwork Blockers:",
            "Infrastructure / Setup Relationship:",
            "`SLC` is the current branch-planning alias",
            "Multi-slice branches are legal",
            "Developer lane",
        ),
        ROOT / "Docs" / "validation_helper_registry.md": (
            "Implementation-Bearing Branch Planning Validation Invariant",
            "planning-only lane/setup carrier",
            "invalid SLC/Slice/Seam terminology ambiguity packet",
            "valid multi-slice implementation carrier",
            "boundary-control labels",
            "Developer lane",
        ),
    }
    for path, markers in source_truth_markers.items():
        if not path.is_file():
            failures.append(f"Missing implementation-bearing source truth owner: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            require(
                marker in text,
                f"Implementation-bearing source truth missing {marker!r} in {path}",
            )
    return failures


def _validate_slice_slc_seam_model_text(text: str) -> list[str]:
    return external_state.validate_slice_slc_seam_model_text(text)


def _validate_br2_route_blocker_packet_text(text: str) -> list[str]:
    failures, require = _collect_failures()
    required_markers = (
        "BR2 Route Resolution Status:",
        "Infrastructure / Lane Groundwork Blockers:",
        "Required Before This Route Can Proceed:",
        "Concrete Feature Routes Available Now:",
        "Deferrable Groundwork:",
        "Non-Deferrable Groundwork:",
        "Codex Recommendation:",
        "Exact USER Decision Needed:",
        "Route Disposition:",
    )
    for marker in required_markers:
        require(marker in text, f"BR2 route blocker packet missing {marker}")
    normalized = governance._normalized_planning_value(text)
    routes_available = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Concrete Feature Routes Available Now:")
    )
    exact_decision = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Exact USER Decision Needed:")
    )
    required_before = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Required Before This Route Can Proceed:")
    )
    deferrable_groundwork = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Deferrable Groundwork:")
    )
    codex_recommendation = governance._normalized_planning_value(
        governance._extract_marker_value(text, "Codex Recommendation:")
    )
    deferral_decision_text = "\n".join(
        (
            required_before,
            deferrable_groundwork,
            codex_recommendation,
            exact_decision,
        )
    )
    require(
        "hold" in normalized
        or "retarget" in normalized
        or "rename" in normalized
        or "no active branch" in normalized,
        "BR2 blocker packet must stop for hold, retarget, rename, or No Active Branch",
    )
    explicit_no_available_routes = routes_available in {
        "none",
        "none.",
        "none;",
        "none; continue planning anyway.",
        "no concrete feature routes available now",
        "no concrete feature routes available now.",
    }
    if explicit_no_available_routes:
        require(
            "no active branch" in normalized
            and "no remaining implementation-bearing route" in normalized
            and "continue planning" not in routes_available
            and "continue planning" not in exact_decision,
            (
                "BR2 blocker packet with no concrete available route must stop on "
                "No Active Branch or non-deferrable groundwork"
            ),
        )
    else:
        proof_only_route_terms = (
            "proof",
            "proof packet",
            "setup proof",
            "packet proof",
            "readiness proof",
            "readiness matrix",
            "decision path",
            "boundary controls",
            "validation plan",
            "planning candidate",
        )
        route_behavior_terms = (
            "control",
            "enforcement",
            "artifact exclusion",
            "disabled-state",
            "install-intent gate",
            "consent-state enforcement",
            "fail-closed",
            "reject",
            "block",
            "gate",
            "implements",
            "implement",
        )
        require(
            any(
                term in routes_available
                for term in (
                    "security/trust-boundary enforcement control",
                    "trust-boundary enforcement control",
                    "provider/runtime consent",
                    "consent shell",
                    "capability-pack install-intent gate",
                    "memory/cache consent-state enforcement",
                    "agent",
                    "runtime",
                    "source-truth",
                    "source truth",
                    "validator",
                    "helper",
                    "feature route",
                )
            ),
            "BR2 blocker packet must name at least one concrete feature route available now",
        )
        require(
            not any(term in routes_available for term in proof_only_route_terms)
            or any(term in routes_available for term in route_behavior_terms),
            (
                "BR2 blocker packet concrete routes cannot be proof/readiness "
                "labels only: name a control, behavior, gate, enforcement, or "
                "state transition that can be implemented"
            ),
        )
    require(
        "approve prerequisite groundwork" in normalized
        or "approve the prerequisite groundwork" in normalized,
        "BR2 blocker packet must offer prerequisite-groundwork approval path",
    )
    require(
        "defer" in deferral_decision_text
        and (
            "concrete feature route" in deferral_decision_text
            or "concrete worktree-focused feature route" in deferral_decision_text
            or "implementation-bearing route" in deferral_decision_text
        ),
        "BR2 blocker packet must offer deferral to a concrete feature route",
    )
    require(
        "non-deferrable" in normalized and "no remaining implementation-bearing route" in normalized,
        "BR2 blocker packet must state when continued deferral stops being legal",
    )
    require(
        "Dev lane" not in text,
        "Use Developer lane, not Dev lane, in current branch-planning text",
    )
    return failures


def _validate_active_external_branch_plan_posture(
    state_root: Path | None = None,
) -> list[str]:
    failures: list[str] = []
    state_root = DEFAULT_EXTERNAL_STATE_ROOT if state_root is None else state_root
    active_state = state_root / "central" / "active_branch_authority_state.md"
    if not active_state.is_file():
        return failures

    active_text = active_state.read_text(encoding="utf-8")
    plan_value = governance._extract_marker_value(
        active_text, "Branch Runtime Engineering Plan:"
    ).strip("` ")
    branch_state_value = governance._extract_marker_value(
        active_text, "Branch State:"
    ).strip("` ")
    plan_path = Path(plan_value) if plan_value else None
    branch_state_path = Path(branch_state_value) if branch_state_value else None
    branch_state_text = (
        branch_state_path.read_text(encoding="utf-8")
        if branch_state_path and branch_state_path.is_file()
        else ""
    )
    active_routes_to_bp1 = "BP1 USER Branch Vision Review" in {
        governance._extract_marker_value(active_text, "Next Gate:").strip("` "),
        governance._extract_marker_value(active_text, "Next Legal Phase:").strip("` "),
        governance._extract_marker_value(branch_state_text, "Next Legal Phase:").strip(
            "` "
        ),
    }
    if not active_routes_to_bp1:
        active_routes_to_bp1 = (
            "Next Gate: `BP1 USER Branch Vision Review`" in active_text
            or "Next Legal Phase: `BP1 USER Branch Vision Review`" in active_text
            or "Next Legal Phase: `BP1 USER Branch Vision Review`"
            in branch_state_text
        )
    if not active_routes_to_bp1:
        active_routes_to_bp1 = (
            "Next Gate: BP1 USER Branch Vision Review" in active_text
            or "Next Legal Phase: BP1 USER Branch Vision Review" in active_text
            or "Next Legal Phase: BP1 USER Branch Vision Review" in branch_state_text
        )
    if not active_routes_to_bp1:
        return failures
    if not plan_path or not plan_path.is_file():
        return [
            "External active branch state routes to BP1 without an existing active branch plan"
        ]

    plan_text = plan_path.read_text(encoding="utf-8")
    required_route_markers = (
        "Selected Implementation Route:",
        "Implementation Route Class:",
        "Concrete Deliverable:",
        "Implementation Output:",
        "Infrastructure / Setup Relationship:",
        "USER Action Gate:",
        "Route Disposition:",
        "Retarget / Rename Recommendation:",
    )
    has_route_markers = all(marker in plan_text for marker in required_route_markers)
    route_resolution_status = external_state.markdown_field_value(
        plan_text, "BR2 Route Resolution Status"
    )
    route_disposition = governance._normalized_planning_value(
        external_state.markdown_field_value(plan_text, "Route Disposition") or ""
    )
    has_hold_or_retarget = bool(route_resolution_status) or any(
        disposition in route_disposition
        for disposition in ("hold", "retarget", "rename")
    )
    if has_hold_or_retarget:
        failures.append(
            "External active branch state routes to BP1 while active branch plan is still HOLD/RETARGET route resolution"
        )
    if not has_route_markers:
        failures.append(
            "External active branch state routes to BP1 without implementation-bearing route fields in active branch plan"
        )
    else:
        failures.extend(_validate_implementation_bearing_route_text(plan_text))
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
        not governance._phase_status_bot_approval_proven(
            "Bot approval proof: `Comment addressed`"
        ),
        "Governance validator treated comment-addressed closeout as bot approval proof",
    )
    require(
        not governance._phase_status_bot_approval_proven(
            "Bot approval proof: `not required after same-head comment-addressed closeout`"
        ),
        "Governance validator treated historical no-later-thumbs-up wording as bot approval proof",
    )
    require(
        governance._phase_status_bot_approval_proven(
            "Bot approval proof: `Approved by Codex Connector bot thumbs-up`"
        ),
        "Governance validator did not accept an explicit Codex Connector thumbs-up approval proof",
    )
    require(
        governance._phase_status_bot_approval_proven(
            "Bot approval proof: `Comment addressed, then approved by later thumbs-up`"
        ),
        "Governance validator rejected explicit approval proof that mentioned repaired comments",
    )
    require(
        not governance._fallback_bot_approval_clears_comment_latch(
            phase_status_section="",
            bot_comment_count=1,
            bot_approval=True,
        ),
        "Governance validator let unordered fallback bot approval clear a prior bot comment",
    )
    require(
        governance._fallback_bot_approval_clears_comment_latch(
            phase_status_section=(
                "Bot approval proof: `Comment addressed, then approved by later thumbs-up`"
            ),
            bot_comment_count=1,
            bot_approval=True,
        ),
        "Governance validator rejected ordered later approval proof for fallback bot comments",
    )
    require(
        not governance._fallback_bot_approval_clears_comment_latch(
            phase_status_section="Bot approval proof: `Approved by Codex Connector bot thumbs-up`",
            bot_comment_count=1,
            bot_approval=True,
        ),
        "Governance validator treated an unordered approval marker as ordered fallback proof",
    )
    require(
        not governance._fallback_bot_approval_clears_comment_latch(
            phase_status_section=(
                "Bot approval proof: `Codex Connector thumbs-up before repair`"
            ),
            bot_comment_count=1,
            bot_approval=True,
        ),
        "Governance validator treated pre-repair approval wording as ordered fallback proof",
    )
    require(
        not governance._watcher_fallback_current_head_bot_approval_proven(
            "Bot approval proof: `Approved by Codex Connector bot thumbs-up`"
        ),
        "Governance validator let unordered watcher fallback approval prove current-head approval",
    )
    require(
        not governance._watcher_fallback_current_head_bot_approval_proven(
            "Bot approval proof: `Codex Connector thumbs-up before repair`"
        ),
        "Governance validator let pre-repair watcher fallback approval prove current-head approval",
    )
    require(
        governance._watcher_fallback_current_head_bot_approval_proven(
            "Bot approval proof: `Comment addressed, then approved by later thumbs-up after current head`"
        ),
        "Governance validator rejected ordered current-head watcher fallback approval proof",
    )
    for fallback_view in (
        governance._automation_closeout_repair_fallback_pr_view_for_branch,
        governance._pr101_closeout_canon_repair_fallback_pr_view_for_branch,
        governance._pr102_closeout_canon_repair_fallback_pr_view_for_branch,
        governance._pr103_closeout_canon_repair_fallback_pr_view_for_branch,
        governance._active_branch_watcher_fallback_pr_view_for_branch,
    ):
        source = inspect.getsource(fallback_view)
        require(
            'watcher_state.get("botApproval")' not in source,
            (
                "Governance validator fallback PR view still trusts raw watcher "
                f"botApproval in {fallback_view.__name__}"
            ),
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


def _validate_user_review_bundle_identity_guard() -> list[str]:
    source_path = "Docs/Main.md"
    copied_path = f"{review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME}/Main.md"
    current_branch = review_bundle._git_output("rev-parse", "--abbrev-ref", "HEAD")
    current_head = review_bundle._git_output("rev-parse", "HEAD")
    current_origin_main = review_bundle._git_output("rev-parse", "origin/main")
    source_text = review_bundle._git_file_text(current_head, source_path) or ""
    common = "Decision Path Summary: workstream implementation approval\nUSER Decision: approve workstream implementation\n"
    packet_files = {
        "START_HERE.md": (
            "# Review\n\n"
            "USER Decision This Packet Supports: approve workstream implementation\n\n"
            "Primary USER Review File: `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`\n\n"
            "## Files\n\n"
            "| Source path | Copied path |\n"
            "| --- | --- |\n"
            f"| `{source_path}` | `{copied_path}` |\n"
        ),
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/USER_REVIEW_FOLDER_AND_FILE_DIGEST.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/GOVERNANCE_REQUIRED_FILES_SCAN.md": common,
        f"{review_bundle.USER_REVIEW_DIR_NAME}/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/BRANCH_VISION_VALIDATION_CHECKLIST.md": common,
        copied_path: source_text,
    }

    valid_result = review_bundle._validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch=current_branch,
        expected_head=current_head,
        expected_origin_main=current_origin_main,
        enforce_identity=True,
    )
    failures: list[str] = []
    if valid_result.failures:
        failures.append(
            "Valid USER review bundle identity fixture unexpectedly failed: "
            + "; ".join(valid_result.failures[:5])
        )

    wrong_result = review_bundle._validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch="wrong-branch",
        expected_head="0" * 40,
        expected_origin_main="1" * 40,
        enforce_identity=True,
    )
    wrong_failures = "\n".join(wrong_result.failures)
    for expected in (
        "expected branch",
        "expected HEAD",
        "expected origin/main",
    ):
        if expected not in wrong_failures:
            failures.append(
                "Invalid USER review bundle identity fixture did not reject "
                f"{expected}"
            )
    return failures


def _validate_workstream_entry_packet_existing_bp1_substance_guard() -> list[str]:
    source_path = "Docs/Main.md"
    copied_path = f"{review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME}/Main.md"
    current_branch = review_bundle._git_output("rev-parse", "--abbrev-ref", "HEAD")
    current_head = review_bundle._git_output("rev-parse", "HEAD")
    current_origin_main = review_bundle._git_output("rev-parse", "origin/main")
    source_text = review_bundle._git_file_text(current_head, source_path) or ""
    common = (
        "# Existing Packet Fixture\n\n"
        "USER Decision This Packet Supports: workstream entry final decision review\n"
        "Decision Path Summary: workstream entry final decision review\n"
        "USER Decision: Workstream Entry final decision review; implementation remains "
        "blocked pending separate USER approval.\n"
    )
    packet_files = {
        "START_HERE.md": (
            "# Review\n\n"
            "USER Decision This Packet Supports: workstream entry final decision review\n\n"
            "## Files\n\n"
            "| Source path | Copied path |\n"
            "| --- | --- |\n"
            f"| `{source_path}` | `{copied_path}` |\n"
        ),
        f"{review_bundle.USER_REVIEW_DIR_NAME}/{review_bundle.USER_BRANCH_VISION_REVIEW_FILE}": (
            INVALID_BP1_TEMPLATE_SHELL_FIXTURE.read_text(encoding="utf-8")
        ),
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/USER_REVIEW_FOLDER_AND_FILE_DIGEST.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/GOVERNANCE_REQUIRED_FILES_SCAN.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/BRANCH_VISION_VALIDATION_CHECKLIST.md": common,
        copied_path: source_text,
    }

    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        packet_dir = Path(temp_dir)
        for relative_path, text in packet_files.items():
            path = packet_dir / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

        result = review_bundle.validate_workstream_entry_packet_folder(
            packet_dir,
            expected_branch=current_branch,
            expected_head=current_head,
            expected_origin_main=current_origin_main,
        )

    if EXPECTED_BP1_TEMPLATE_SHELL_FAILURE_SNIPPET not in "\n".join(result.failures):
        failures.append(
            "Existing Workstream Entry packet folder validation did not reject "
            "template-shell BP1 review content"
        )
    return failures


def _validate_user_review_bundle_export_zip_identity_guard() -> list[str]:
    source_path = "Docs/Main.md"
    copied_path = f"{review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME}/Main.md"
    current_branch = review_bundle._git_output("rev-parse", "--abbrev-ref", "HEAD")
    current_head = review_bundle._git_output("rev-parse", "HEAD")
    current_origin_main = review_bundle._git_output("rev-parse", "origin/main")
    source_text = review_bundle._git_file_text(current_head, source_path) or ""
    common = (
        "Decision Path Summary: workstream implementation approval\n"
        "USER Decision: approve workstream implementation\n"
    )
    plan_headings = (
        "Contract Status",
        "Packet Reviewability State",
        "USER Gate State",
        "USER Response Proof",
        "USER Response Digested",
        "Acceptance / Waiver / Revision / Rejection Receipt",
        "Contract Version / Revision",
        "Plain-English Branch Summary",
        "What Will I Actually See, And Where Will I See It?",
        "End-State Vision",
        "Visual / Functional Walkthrough",
        "Surface Map",
        "Implementation Options",
        "Recommended Direction",
        "Why This Fits The Nexus Vision",
        "USER Plan Review Decision",
        "USER Decisions Needed",
        "USER Response",
        "Codex Response Digest",
        "Implementation Constraints Created By USER Response",
        "USER Rejected / Deferred Ideas",
        "Vision Delta / Source-Truth Impact",
        "Contract Change Log",
        "Current Branch Scope",
        "Future-Gated Scope",
        "Implementation Staging Notes",
        "Workstream Entry Result",
        "Contract Completion Checklist",
        "Exact USER Decision Supported",
    )
    vision_review_text = (
        "# Fixture USER Branch Vision Review\n\n"
        "USER Branch Vision Review: BP1\n\n"
        "## Review Status\nAccepted by USER for this fixture identity guard.\n\n"
        "## Contract Status\nComplete - fixture USER acceptance is recorded for implementation-ready validation.\n\n"
        "## Packet Reviewability State\nReviewable\n\n"
        "## USER Gate State\nUSER Accepted\n\n"
        "## Contract Revision\nv2 - substantive fixture packet.\n\n"
        "## Project Vision Context\n"
        "This fixture branch supports Nexus by requiring a readable USER vision review before engineering planning. "
        "It protects local-first, inspectable planning and prevents validators from treating a marker-only packet as product direction.\n\n"
        "## Family Vision Context\n"
        "The fixture family context requires branch-specific outcomes, boundaries, and USER decisions before BP2. "
        "Family direction remains the durable owner when the response changes reusable behavior.\n\n"
        "## Feature Vision Context\n"
        "The feature context is a governance review packet that must explain what the branch is trying to prove, "
        "which review surfaces matter, and which implementation behavior remains future-gated.\n\n"
        "## Branch Goal\n"
        "Create a substantive BP1 branch vision that USER can accept, revise, reject, or waive before Codex creates a BP2 engineering plan from it.\n\n"
        "## End-State Vision\n"
        "USER has a concrete accepted or revised branch vision, and later BP2/BP3 proof can trace engineering seams back to that accepted direction.\n\n"
        "## What Will I Actually See, And Where Will I See It?\n"
        "USER sees a decision-focused BP1 review in the local USER hub, with START_HERE used only to navigate supporting source context.\n\n"
        "## How It Will Function\n"
        "BP1 establishes product or governance direction, BP2 converts that accepted direction into implementation planning, and BP3 verifies orchestration before implementation approval.\n\n"
        "## User Experience Flow\n"
        "USER reads START_HERE, reviews the BP1 branch vision, chooses an option or revision, answers design questions, and waits for Codex to digest the response.\n\n"
        "## Surface Map\n"
        "Review surface is USER_BRANCH_VISION_REVIEW.md; context surface is START_HERE; decision surface is USER Response plus Codex Digest; proof surface is later BP2/BP3 traceability.\n\n"
        "## Product Options / Design Paths\n"
        "Option A accepts the fixture vision as scoped and lets BP2 begin from a clear branch-specific outcome, with the tradeoff of one deliberate review pause. Option B revises review surfaces, experience flow, or branch boundaries before BP2 to reduce implementation risk. Option C waives or rejects BP1 and keeps implementation blocked or deferred until USER gives a safer direction.\n\n"
        "## Codex Recommendations\n"
        "Recommendation one keeps packet placement in the local USER hub, names BP1/BP2/BP3 behavior, explains tradeoffs around review time, and cites risk from shallow branch vision because marker-only packet validation can otherwise bypass USER intent. USER response: accepted for fixture. Recommendation two keeps copied files as context instead of the vision so USER can decide from applied branch-specific substance. USER response: accepted for fixture.\n\n"
        "## Why This Fits The Nexus Vision\n"
        "This keeps Nexus planning USER-controlled and inspectable because Codex must explain the branch outcome before engineering seams become the default direction.\n\n"
        "## USER Design Questions\n"
        "What exact fixture outcome should USER inspect before BP2 turns this into engineering seams? Which review surface, experience flow, or branch boundary must remain future-gated if this BP1 review is revised?\n\n"
        "## USER Response\nFixture USER accepted the branch vision for zip identity validation.\n\n"
        "## Codex Digest\nFixture Codex digest records BP1 accepted for this implementation-ready packet identity guard.\n\n"
        "## USER Response Proof\nAccepted by fixture USER.\n\n"
        "## USER Response Digested\nYes - fixture acceptance was digested.\n\n"
        "## Accepted Branch Vision\nFixture accepted Branch Vision requires substantive review packets before implementation-ready validation can pass.\n\n"
        "## Family-Vision Versus Branch-Only Vision Impact\nBranch-only unless USER response creates a reusable family standard.\n\n"
        "## Must-Have Behavior\nBP1 remains a USER gate before BP2.\n\n"
        "## Future-Gated Decisions And Regression-Risk Controls\nRegression-risk control: packet validation is reviewability evidence, not USER acceptance.\n\n"
        "## Deferred And Future-Gated Ideas\nImplementation remains future-gated.\n\n"
        "## Vision Question Queue\nPending USER review.\n\n"
        "## Design Assumption Ledger\nUSER Branch Vision acceptance is required unless explicitly waived.\n\n"
        "## Acceptance / Revision / Rejection / Waiver Decision\nAccepted by fixture USER.\n"
    )
    packet_files = {
        "START_HERE.md": (
            "# Review\n\n"
            "Review Purpose: Fixture packet.\n"
            "USER Decision This Packet Supports: approve workstream implementation\n"
            "Bundle File Count: 8\n"
            "Expected File Count: 1\n"
            "Copied File Count: 1\n"
            "Extra Bundle File Count: 6\n\n"
            "| Source path | Copied path |\n"
            "| --- | --- |\n"
            f"| `{source_path}` | `{copied_path}` |\n"
        ),
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/{review_bundle.USER_BRANCH_VISION_REVIEW_FILE}": vision_review_text,
        f"{review_bundle.USER_REVIEW_DIR_NAME}/{review_bundle.USER_BRANCH_PLAN_REVIEW_FILE}": "\n".join(
            f"## {heading}\nComplete.\n" for heading in plan_headings
        ).replace(
            "## Packet Reviewability State\nComplete.\n",
            "## Packet Reviewability State\nReviewable\n",
        ).replace(
            "## USER Gate State\nComplete.\n",
            "## USER Gate State\nUSER Accepted\n",
        ).replace(
            "## Exact USER Decision Supported\nComplete.\n",
            "## Exact USER Decision Supported\nApprove bounded workstream implementation.\n",
        ),
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/USER_REVIEW_FOLDER_AND_FILE_DIGEST.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/GOVERNANCE_REQUIRED_FILES_SCAN.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": common,
        f"{review_bundle.REVIEW_AIDS_DIR_NAME}/BRANCH_VISION_VALIDATION_CHECKLIST.md": common,
        copied_path: source_text,
    }

    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        export_zip = Path(temp_dir) / "Governance-20260601-120000.zip"
        with zipfile.ZipFile(export_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, text in packet_files.items():
                archive.writestr(name, text)

        try:
            review_bundle._validate_export_zip(
                export_zip,
                source_branch=current_branch,
                source_head=current_head,
                origin_main=current_origin_main,
                expected_label="Governance",
                expected_entries=set(packet_files),
            )
        except ValueError as exc:
            failures.append(
                "Valid USER review export zip identity fixture unexpectedly failed: "
                f"{exc}"
            )

        try:
            review_bundle._validate_export_zip(
                export_zip,
                source_branch="wrong-branch",
                source_head="0" * 40,
                origin_main="1" * 40,
                expected_label="Governance",
                expected_entries=set(packet_files),
            )
        except ValueError as exc:
            wrong_failures = str(exc)
        else:
            wrong_failures = ""
            failures.append("Invalid USER review export zip identity fixture unexpectedly passed")

        stable_zip = Path(temp_dir) / "Governance.zip"
        with zipfile.ZipFile(stable_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, text in packet_files.items():
                archive.writestr(name, text)
        try:
            review_bundle._validate_export_zip(
                stable_zip,
                source_branch=current_branch,
                source_head=current_head,
                origin_main=current_origin_main,
                expected_label="Governance",
                expected_entries=set(packet_files),
            )
        except ValueError as exc:
            stale_name_failures = str(exc)
        else:
            stale_name_failures = ""
            failures.append("Invalid stable-name USER review export zip unexpectedly passed")
        if "creation timestamp" not in stale_name_failures:
            failures.append(
                "Invalid stable-name USER review export zip did not reject missing timestamp"
            )
    for expected in (
        "expected branch",
        "expected HEAD",
        "expected origin/main",
    ):
        if expected not in wrong_failures:
            failures.append(
                "Invalid USER review export zip identity fixture did not reject "
                f"{expected}"
            )
    return failures


def _validate_user_review_bundle_export_zip_cleanup_guard() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        review_root = Path(temp_dir)
        legacy_zip = review_root / "FAM-007.zip"
        stale_timestamped_zip = review_root / "FAM-007-20260601-111111.zip"
        other_label_zip = review_root / "FAM-006-20260601-111111.zip"
        malformed_same_label_zip = review_root / "FAM-007-not-a-timestamp.zip"
        export_zip = review_root / "FAM-007-20260601-222222.zip"
        for path in (
            legacy_zip,
            stale_timestamped_zip,
            other_label_zip,
            malformed_same_label_zip,
        ):
            path.write_text("fixture", encoding="utf-8")

        review_bundle._remove_stale_same_label_export_zips(
            review_root,
            "FAM-007",
            export_zip,
        )

        if legacy_zip.exists():
            failures.append("USER review zip cleanup left legacy same-name FAM-007.zip")
        if stale_timestamped_zip.exists():
            failures.append(
                "USER review zip cleanup left previous same-label timestamped FAM-007 zip"
            )
        if not other_label_zip.exists():
            failures.append("USER review zip cleanup removed a different worktree-label zip")
        if not malformed_same_label_zip.exists():
            failures.append(
                "USER review zip cleanup removed a non-timestamped same-prefix file"
            )
    return failures


def _write_local_user_packet_fixture(packet_dir: Path) -> None:
    (packet_dir / review_bundle.USER_REVIEW_DIR_NAME).mkdir(parents=True, exist_ok=True)
    (packet_dir / review_bundle.REVIEW_AIDS_DIR_NAME).mkdir(parents=True, exist_ok=True)
    (packet_dir / review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME).mkdir(parents=True, exist_ok=True)
    (packet_dir / "START_HERE.md").write_text(
        "# START HERE\n\n"
        "Review Purpose: fixture packet validation.\n"
        "Local USER Hub Folder: fixture local hub.\n"
        "Review Order: open USER Review/FIXTURE_REVIEW.md first.\n"
        "USER Decision This Packet Supports: fixture review only.\n"
        "Pending USER Decisions: none for fixture.\n"
        "Bundle File Count: 5\n"
        "Expected File Count: 2\n"
        "Copied File Count: 2\n"
        "Extra Bundle File Count: 2\n",
        encoding="utf-8",
    )
    (packet_dir / review_bundle.USER_REVIEW_DIR_NAME / "FIXTURE_REVIEW.md").write_text(
        "# Fixture Review\n\n"
        "This is the only primary USER review file for the current fixture gate.\n",
        encoding="utf-8",
    )
    (packet_dir / review_bundle.REVIEW_AIDS_DIR_NAME / "FIXTURE_AID.md").write_text(
        "# Fixture Aid\n\nSupporting review aid.\n",
        encoding="utf-8",
    )
    (packet_dir / review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME / "Main.md").write_text(
        "# Fixture Source Truth Context\n\nCopied context only.\n",
        encoding="utf-8",
    )
    (
        packet_dir
        / review_bundle.SOURCE_TRUTH_CONTEXT_DIR_NAME
        / review_bundle.USER_BRANCH_PLAN_REVIEW_FILE
    ).write_text(
        "# Historical Branch Plan Review Context\n\n"
        "Source HEAD: 0123456789012345678901234567890123456789\n",
        encoding="utf-8",
    )


def _zip_local_user_packet_fixture(packet_dir: Path, export_zip: Path) -> None:
    with zipfile.ZipFile(export_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(packet_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(packet_dir).as_posix())


def _validate_local_user_packet_folder_zip_guard() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        review_root = Path(temp_dir)
        packet_dir = review_root / "Governance"
        export_zip = review_root / "Governance-20260617-111111.zip"
        _write_local_user_packet_fixture(packet_dir)
        _zip_local_user_packet_fixture(packet_dir, export_zip)

        result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if result.failures:
            failures.append(
                "Valid local USER packet folder/ZIP fixture unexpectedly failed: "
                + "; ".join(result.failures[:5])
            )

        bad_metadata_aid = packet_dir / review_bundle.REVIEW_AIDS_DIR_NAME / "BAD_METADATA_AID.md"
        bad_metadata_aid.write_text(
            "# Bad Metadata Aid\n\nSource HEAD: 0123456789012345678901234567890123456789\n",
            encoding="utf-8",
        )
        _zip_local_user_packet_fixture(packet_dir, export_zip)
        bad_metadata_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any(
            "BAD_METADATA_AID.md" in failure and "technical metadata" in failure
            for failure in bad_metadata_result.failures
        ):
            failures.append("Local USER packet validation did not reject technical metadata in Review Aids")
        bad_metadata_aid.unlink()
        _zip_local_user_packet_fixture(packet_dir, export_zip)

        bad_validation_aid = packet_dir / review_bundle.REVIEW_AIDS_DIR_NAME / "BAD_VALIDATION_STATUS_AID.md"
        bad_validation_aid.write_text(
            "# Bad Validation Status Aid\n\nValidation Summary: green-by-helper-output.\n",
            encoding="utf-8",
        )
        _zip_local_user_packet_fixture(packet_dir, export_zip)
        bad_validation_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any(
            "BAD_VALIDATION_STATUS_AID.md" in failure and "technical metadata" in failure
            for failure in bad_validation_result.failures
        ):
            failures.append("Local USER packet validation did not reject validation status in Review Aids")
        bad_validation_aid.unlink()
        _zip_local_user_packet_fixture(packet_dir, export_zip)

        changed_aid = packet_dir / review_bundle.REVIEW_AIDS_DIR_NAME / "FIXTURE_AID.md"
        changed_aid.write_text(
            "# Fixture Aid\n\nChanged after ZIP creation; same filename, stale ZIP content.\n",
            encoding="utf-8",
        )
        stale_content_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any("content hash mismatch" in failure for failure in stale_content_result.failures):
            failures.append("Local USER packet validation did not reject stale ZIP content with matching file names")
        changed_aid.write_text(
            "# Fixture Aid\n\nSupporting review aid.\n",
            encoding="utf-8",
        )
        _zip_local_user_packet_fixture(packet_dir, export_zip)

        copied_zip_dir = review_root / "Copied Zip Outside User Hub"
        copied_zip_dir.mkdir()
        copied_zip = copied_zip_dir / export_zip.name
        copied_zip.write_bytes(export_zip.read_bytes())
        copied_zip_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=copied_zip,
            worktree_label="Governance",
        )
        if not any("must live beside the packet folder" in failure for failure in copied_zip_result.failures):
            failures.append("Local USER packet validation did not reject ZIP outside packet folder parent")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(export_zip, "a", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr(
                    f"{review_bundle.REVIEW_AIDS_DIR_NAME}/FIXTURE_AID.md",
                    "# Fixture Aid\n\nDuplicate ZIP member fixture.\n",
                )
        duplicate_zip_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any("duplicate ZIP entries" in failure for failure in duplicate_zip_result.failures):
            failures.append("Local USER packet validation did not reject duplicate ZIP member names")
        _zip_local_user_packet_fixture(packet_dir, export_zip)

        stale_zip = review_root / "Governance-20260617-101010.zip"
        stale_zip.write_text("stale fixture", encoding="utf-8")
        stale_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any("Stale same-label USER packet ZIP remains" in failure for failure in stale_result.failures):
            failures.append("Local USER packet validation did not reject stale same-label timestamped ZIP")
        stale_zip.unlink()

        stable_zip = review_root / "Governance.zip"
        stable_zip.write_text("legacy stable fixture", encoding="utf-8")
        stable_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any("Stable-name USER packet ZIP is not allowed" in failure for failure in stable_result.failures):
            failures.append("Local USER packet validation did not reject stable-name Governance.zip")
        stable_zip.unlink()

        extra_primary = packet_dir / review_bundle.USER_REVIEW_DIR_NAME / "SECOND_REVIEW.md"
        extra_primary.write_text("# Second Review\n\nInvalid extra primary file.\n", encoding="utf-8")
        _zip_local_user_packet_fixture(packet_dir, export_zip)
        multi_primary_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any("exactly one primary USER review file" in failure for failure in multi_primary_result.failures):
            failures.append("Local USER packet validation did not reject multiple primary USER review files")
        extra_primary.unlink()

        _zip_local_user_packet_fixture(packet_dir, export_zip)
        (packet_dir / review_bundle.REVIEW_AIDS_DIR_NAME / "ZIP_MISMATCH.md").write_text(
            "# ZIP Mismatch\n\nThis file was added after ZIP creation.\n",
            encoding="utf-8",
        )
        mismatch_result = review_bundle.validate_local_user_packet(
            packet_dir,
            export_zip=export_zip,
            worktree_label="Governance",
        )
        if not any("Folder/ZIP parity failed" in failure for failure in mismatch_result.failures):
            failures.append("Local USER packet validation did not reject folder/ZIP parity drift")
    return failures


def _validate_active_overlay_user_branch_plan_review_metadata_guard() -> list[str]:
    source_path = "Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md"
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir)
        review_bundle._write_user_branch_plan_review(
            target=target,
            title="Active Overlay Recording Runtime Foundation",
            review_purpose="Fixture packet metadata guard.",
            source_branch="feature/fam-006-active-overlay-recording-runtime-foundation",
            source_head=review_bundle._git_output("rev-parse", "HEAD"),
            upstream="origin/feature/fam-006-active-overlay-recording-runtime-foundation",
            origin_main=review_bundle._git_output("rev-parse", "origin/main"),
            exact_user_decision="I approve PR Readiness Stage 1 analysis.",
            pending_user_decisions=["Runtime implementation remains pending USER approval."],
            copied=[(source_path, "feature_fam_006_active_overlay_recording_runtime_foundation.md")],
        )
        text = (target / review_bundle.USER_BRANCH_PLAN_REVIEW_FILE).read_text(encoding="utf-8")

    metadata_failures = review_bundle._user_facing_technical_metadata_failures(
        {review_bundle.USER_BRANCH_PLAN_REVIEW_FILE: text}
    )
    if metadata_failures:
        failures.append(
            "Active Overlay USER Branch Plan Review fixture unexpectedly emitted "
            "USER-facing technical metadata: "
            + "; ".join(metadata_failures[:5])
        )
    if "HEAD changes" in text:
        failures.append(
            "Active Overlay USER Branch Plan Review fixture still contains stale HEAD-change wording"
        )
    return failures


def _validate_fam007_workstream_approval_packet_metadata_guard() -> list[str]:
    source_path = (
        "Docs/branch_plans/"
        "feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md"
    )
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir)
        review_bundle._write_user_branch_plan_review(
            target=target,
            title="FAM-007 Breakpoint 2 Dev Owner Skeleton Action Gate Readiness",
            review_purpose="Fixture packet metadata guard.",
            source_branch=(
                "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
            ),
            source_head=review_bundle._git_output("rev-parse", "HEAD"),
            upstream=(
                "origin/feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
            ),
            origin_main=review_bundle._git_output("rev-parse", "origin/main"),
            exact_user_decision="Approve bounded workstream implementation.",
            pending_user_decisions=[
                "Private/runtime/provider/model/cache/memory behavior remains pending USER approval."
            ],
            copied=[
                (
                    source_path,
                    "feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md",
                )
            ],
        )
        text = (target / review_bundle.USER_BRANCH_PLAN_REVIEW_FILE).read_text(encoding="utf-8")

    metadata_failures = review_bundle._user_facing_technical_metadata_failures(
        {review_bundle.USER_BRANCH_PLAN_REVIEW_FILE: text}
    )
    if metadata_failures:
        failures.append(
            "FAM-007 workstream approval USER Branch Plan Review fixture unexpectedly "
            "emitted USER-facing technical metadata: "
            + "; ".join(metadata_failures[:5])
        )
    if "validation summary" in text.casefold():
        failures.append(
            "FAM-007 workstream approval packet still emits forbidden validation-summary wording"
        )
    if "seam 1 only" in text.casefold() or "first bounded workstream seam only" in text.casefold():
        failures.append(
            "FAM-007 workstream approval packet must not treat the entry seam as terminal Workstream authority"
        )
    return failures


def _validate_fam007_bp3_packet_generation_guard() -> list[str]:
    failures: list[str] = []
    exact_decision = (
        "I approve BP3 Workstream Entry / Orchestration Validation for the "
        "FAM-007 Dev/Owner Skeleton Readiness packet review; Workstream "
        "implementation remains pending separate USER approval."
    )
    copied = [
        (
            "Docs/branch_records/feature_fam_007_dev_owner_skeleton_readiness.md",
            "feature_fam_007_dev_owner_skeleton_readiness.md",
        )
    ]
    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir)
        review_bundle._write_workstream_entry_packet_digests(
            target=target,
            source_branch="feature/fam-007-dev-owner-skeleton-readiness",
            source_head="fixture-head",
            origin_main="fixture-origin-main",
            packet_folder=target,
            export_zip=target / "FAM-007-20260601-120000.zip",
            copied=copied,
            extra_bundle_files=["USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"],
            bundle_file_count=6,
            expected_count=len(copied),
            copied_count=len(copied),
            exact_user_decision=exact_decision,
            pending_user_decisions=["Workstream implementation remains pending USER approval."],
        )
        packet_files = {
            "START_HERE.md": (
                "USER Decision This Packet Supports: "
                f"{exact_decision}\n"
                "Decision Path Summary: bp3 orchestration review\n"
                "BP3 Packet Reviewability State: Reviewable\n"
                "BP3 USER Gate State: Pending USER Review\n"
            )
        }
        for path in target.glob("*.md"):
            packet_files[path.name] = path.read_text(encoding="utf-8")

    result = review_bundle._validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch="feature/fam-007-dev-owner-skeleton-readiness",
        expected_head="fixture-head",
        expected_origin_main="fixture-origin-main",
    )
    if result.status != review_bundle.DECISION_STATUS_BP3_ORCHESTRATION_REVIEW:
        failures.append(
            "FAM-007 BP3 generated packet did not classify as bp3-orchestration-review: "
            f"{result.status}; {result.failures[:3]}"
        )
    combined = "\n".join(packet_files.values()).casefold()
    if "workstream entry final decision review" in combined:
        failures.append(
            "FAM-007 BP3 generated packet still emits stale Workstream Entry final-decision wording"
        )
    if "implementation approval: approved" in combined:
        failures.append(
            "FAM-007 BP3 generated packet incorrectly approves implementation"
        )
    if "seam 1 only" in combined or "first bounded workstream seam only" in combined:
        failures.append(
            "FAM-007 BP3 generated packet must not emit first-seam-only Workstream approval wording"
        )
    primary_digest = packet_files.get("WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md", "")
    required_primary_sections = [
        "## Plain-Language BP3 Readiness Summary",
        "## Accepted BP1 Vision Traceability",
        "## Accepted BP2 Plan Traceability",
        "## Proposed Workstream Implementation Order",
        "## Seam / SLC Readiness Assessment",
        "## Expected Files / Helpers / Validators / Fixtures / Review Artifacts",
        "## Direct Proof Plan",
        "## Rollback And Reversibility Posture",
        "## Drift Controls",
        "## Unresolved Blockers And Pending USER Decisions",
        "## Codex Readiness Recommendation",
        "## Specific USER Readiness Questions",
        "## Exact BP3 USER Decision Options",
    ]
    missing_sections = [
        section for section in required_primary_sections if section not in primary_digest
    ]
    if missing_sections:
        failures.append(
            "FAM-007 BP3 primary digest is missing readiness-contract sections: "
            + "; ".join(missing_sections)
        )
    required_primary_proof_terms = [
        "No-private-action proof",
        "Public-leak prevention",
        "Provider-state inactivity",
        "Runtime/cache/memory deferral",
        "GitHub Desktop binding absence",
        "Backup/import deferral",
        "Artifact identity proof",
        "External-state proof",
    ]
    missing_proof_terms = [
        term for term in required_primary_proof_terms if term not in primary_digest
    ]
    if missing_proof_terms:
        failures.append(
            "FAM-007 BP3 primary digest is missing direct-proof topics: "
            + "; ".join(missing_proof_terms)
        )
    if "Seam 5 - Packet, fixture, validator, and fold-down proof" not in primary_digest:
        failures.append(
            "FAM-007 BP3 primary digest must cover the full accepted seam route, "
            "not only the first Workstream seam"
        )
    return failures


def _validate_fam007_workstream_implementation_packet_priority_guard() -> list[str]:
    failures: list[str] = []
    exact_decision = (
        "BP1, BP2, and BP3 are accepted; approve bounded Workstream package "
        "implementation for the FAM-007 Dev/Owner Skeleton Readiness same-branch "
        "package with Seam 1 as the entry checkpoint and continuation until "
        "Workstream Green."
    )
    copied = [
        (
            "Docs/branch_records/feature_fam_007_dev_owner_skeleton_readiness.md",
            "feature_fam_007_dev_owner_skeleton_readiness.md",
        )
    ]
    with tempfile.TemporaryDirectory() as temp_dir:
        target = Path(temp_dir)
        review_bundle._write_workstream_entry_packet_digests(
            target=target,
            source_branch="feature/fam-007-dev-owner-skeleton-readiness",
            source_head="fixture-head",
            origin_main="fixture-origin-main",
            packet_folder=target,
            export_zip=target / "FAM-007-20260601-120000.zip",
            copied=copied,
            extra_bundle_files=["USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"],
            bundle_file_count=6,
            expected_count=len(copied),
            copied_count=len(copied),
            exact_user_decision=exact_decision,
            pending_user_decisions=[
                "Hardening, Live Validation, PR, merge, release, private setup, "
                "provider/runtime/cache/memory behavior, and cleanup remain future "
                "USER decisions."
            ],
        )
        packet_files = {
            "START_HERE.md": (
                "USER Decision This Packet Supports: "
                f"{exact_decision}\n"
                "Decision Path Summary: implementation-ready - BP1, BP2, and BP3 "
                "are accepted; bounded Workstream package implementation is "
                "approved by this packet with Seam 1 as the entry checkpoint.\n"
            )
        }
        for path in target.glob("*.md"):
            packet_files[path.name] = path.read_text(encoding="utf-8")
        review_bundle._write_user_branch_plan_review(
            target=target,
            title="FAM-007 Dev/Owner Skeleton Readiness",
            review_purpose="Fixture Workstream implementation approval support file.",
            source_branch="feature/fam-007-dev-owner-skeleton-readiness",
            source_head="fixture-head",
            upstream="origin/feature/fam-007-dev-owner-skeleton-readiness",
            origin_main="fixture-origin-main",
            exact_user_decision=exact_decision,
            pending_user_decisions=[
                "Hardening, Live Validation, PR, merge, release, private setup, "
                "provider/runtime/cache/memory behavior, and cleanup remain future "
                "USER decisions."
            ],
            copied=copied,
        )
        branch_plan_review = (
            target / review_bundle.USER_BRANCH_PLAN_REVIEW_FILE
        ).read_text(encoding="utf-8")
        packet_files[review_bundle.USER_BRANCH_PLAN_REVIEW_FILE] = branch_plan_review

    result = review_bundle._validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch="feature/fam-007-dev-owner-skeleton-readiness",
        expected_head="fixture-head",
        expected_origin_main="fixture-origin-main",
        require_implementation_ready=True,
    )
    if result.status != review_bundle.DECISION_STATUS_IMPLEMENTATION_READY:
        failures.append(
            "FAM-007 Workstream implementation approval packet did not classify "
            f"as implementation-ready: {result.status}; {result.failures[:3]}"
        )
    combined = "\n".join(packet_files.values()).casefold()
    forbidden_bp3_review_terms = [
        "bp3 packet reviewability state: reviewable",
        "bp3 user gate state: pending user review",
        "workstream implementation itself remains a separate future user decision",
        "exact bp3 user decision options",
    ]
    emitted_forbidden_terms = [
        term for term in forbidden_bp3_review_terms if term in combined
    ]
    if emitted_forbidden_terms:
        failures.append(
            "FAM-007 Workstream implementation approval packet emitted BP3 review "
            "or pending-gate wording despite implementation approval: "
            + "; ".join(emitted_forbidden_terms)
        )
    support_file_forbidden_terms = [
        "pending user response",
        "bp3 active - workstream entry / orchestration validation",
        "workstream implementation remains pending separate user approval",
        "this packet does not authorize workstream implementation",
    ]
    emitted_support_file_terms = [
        term for term in support_file_forbidden_terms
        if term in branch_plan_review.casefold()
    ]
    if emitted_support_file_terms:
        failures.append(
            "FAM-007 Workstream implementation approval support BP2 file emitted "
            "pending or BP3-only wording: "
            + "; ".join(emitted_support_file_terms)
        )
    support_file_required_terms = [
        "Complete - USER accepted the BP2 Branch Plan Contract; BP3 is accepted",
        "Status: Accepted by USER - this BP2 support file is closed as accepted engineering-plan context",
        "Implementation-ready - BP1, BP2, and BP3 are accepted",
    ]
    missing_support_terms = [
        term for term in support_file_required_terms if term not in branch_plan_review
    ]
    if missing_support_terms:
        failures.append(
            "FAM-007 Workstream implementation approval support BP2 file is missing "
            "accepted implementation-ready context: "
            + "; ".join(missing_support_terms)
        )
    required_terms = [
        "bounded Workstream package implementation is approved",
        "Seam 1 as the entry checkpoint",
        "Continuation must proceed one active same-branch seam at a time until Workstream Green",
    ]
    missing_required_terms = [term for term in required_terms if term not in "\n".join(packet_files.values())]
    if missing_required_terms:
        failures.append(
            "FAM-007 Workstream implementation approval packet is missing "
            "implementation-ready terms: "
            + "; ".join(missing_required_terms)
        )
    return failures


def _validate_primary_user_review_file_stage_priority() -> list[str]:
    failures: list[str] = []
    bp3_trace_decision = (
        "I approve BP3 Workstream Entry / Orchestration Validation against "
        "accepted BP1 vision and BP2 branch plan traceability."
    )
    if (
        review_bundle._primary_user_review_file(bp3_trace_decision)
        != "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"
    ):
        failures.append(
            "BP3 primary USER review routing must prioritize Workstream Entry / "
            "Orchestration over BP1/BP2 traceability wording"
        )
    bp3_prerequisite_first_decision = (
        "BP1 and BP2 are accepted; approve BP3 orchestration validation for "
        "Workstream Entry."
    )
    if (
        review_bundle._primary_user_review_file(bp3_prerequisite_first_decision)
        != "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"
    ):
        failures.append(
            "BP3 primary USER review routing must prefer the requested BP3 gate "
            "over prerequisite BP1/BP2 mentions"
        )
    workstream_implementation_decision = "Approve bounded workstream implementation."
    if (
        review_bundle._primary_user_review_file(workstream_implementation_decision)
        != "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"
    ):
        failures.append(
            "Workstream implementation approval packets must route the primary "
            "USER review file to WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md"
        )
    bp2_trace_decision = (
        "I approve BP2 Branch Plan Review after accepted BP1 branch vision proof."
    )
    if (
        review_bundle._primary_user_review_file(bp2_trace_decision)
        != review_bundle.USER_BRANCH_PLAN_REVIEW_FILE
    ):
        failures.append(
            "BP2 primary USER review routing must remain USER_BRANCH_PLAN_REVIEW.md "
            "when BP2 text mentions accepted BP1 proof"
        )
    bp2_prerequisite_first_decision = (
        "BP1 is accepted; approve BP2 Branch Plan Review for engineering planning."
    )
    if (
        review_bundle._primary_user_review_file(bp2_prerequisite_first_decision)
        != review_bundle.USER_BRANCH_PLAN_REVIEW_FILE
    ):
        failures.append(
            "BP2 primary USER review routing must prefer the requested BP2 gate "
            "over prerequisite BP1 mentions"
        )
    bp1_preview_decision = (
        "I approve BP1 Branch Vision Review before BP2 Branch Plan Review and "
        "BP3 orchestration planning begin."
    )
    if (
        review_bundle._primary_user_review_file(bp1_preview_decision)
        != review_bundle.USER_BRANCH_VISION_REVIEW_FILE
    ):
        failures.append(
            "BP1 primary USER review routing must remain USER_BRANCH_VISION_REVIEW.md "
            "when BP1 text previews later BP2/BP3 gates"
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
        VALID_BRANCH_PLANNING_GATE_STATE_FIXTURE,
        INVALID_BRANCH_PLANNING_GATE_BYPASS_FIXTURE,
        VALID_BP1_BRANCH_VISION_REVIEW_FIXTURE,
        VALID_BP1_FAM006_DOGFOOD_FIXTURE,
        VALID_BP1_FAM007_DOGFOOD_FIXTURE,
        VALID_BP1_GOVERNANCE_DOGFOOD_FIXTURE,
        INVALID_BP1_MISSING_CONTEXT_FIXTURE,
        INVALID_BP1_SHALLOW_RECOMMENDATIONS_FIXTURE,
        INVALID_BP1_TEMPLATE_SHELL_FIXTURE,
        INVALID_BP1_PROCESS_MECHANICS_FIXTURE,
        INVALID_BP1_COPIED_FILE_SURFACE_ONLY_FIXTURE,
        INVALID_BP1_GENERIC_USER_QUESTIONS_FIXTURE,
        INVALID_BP1_SLC_CENTERED_FIXTURE,
        INVALID_BP1_TECHNICAL_METADATA_FIXTURE,
        INVALID_BP2_MISSING_ACCEPTED_BP1_TRACE_FIXTURE,
        VALID_BP2_FAM006_DOGFOOD_FIXTURE,
        VALID_BP2_FAM007_DOGFOOD_FIXTURE,
        INVALID_BP3_IMPLEMENTATION_WITH_PENDING_BP1_BP2_FIXTURE,
        VALID_BP3_ACCEPTED_BP1_BP2_SLC_TRACE_FIXTURE,
        VALID_BP3_FAM006_DOGFOOD_FIXTURE,
        VALID_BP3_FAM007_DOGFOOD_FIXTURE,
        INVALID_IMPLEMENTATION_ROUTE_PLANNING_ONLY_FIXTURE,
        VALID_IMPLEMENTATION_ROUTE_SECURITY_BOUNDARY_FIXTURE,
        VALID_BR2_ROUTE_BLOCKER_PACKET_FIXTURE,
        INVALID_BR2_ROUTE_BLOCKER_NO_ROUTE_CONTINUE_FIXTURE,
        INVALID_IMPLEMENTATION_ROUTE_FAKE_FEATURE_LABEL_FIXTURE,
        VALID_IMPLEMENTATION_ROUTE_BP2_HOLD_ACTION_GATE_FIXTURE,
        VALID_IMPLEMENTATION_ROUTE_RETARGET_RENAME_FIXTURE,
        VALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE,
        INVALID_MERGE_STABLE_SOURCE_TRUTH_PROJECTION_FIXTURE,
        VALID_CROSS_FAM_DEPENDENCY_CANDIDATE_FIXTURE,
        INVALID_CROSS_FAM_DEPENDENCY_UNCLASSIFIED_FIXTURE,
        VALID_FAMILY_FEATURE_VISION_FIXTURE,
        INVALID_FAMILY_FEATURE_VISION_SLICE_SCOPED_FIXTURE,
        INVALID_FAMILY_FEATURE_VISION_LIVE_STATE_FIXTURE,
        VALID_BR2_DEFERRED_CARRYFORWARD_MATRIX_FIXTURE,
        INVALID_BR2_DEFERRED_CARRYFORWARD_MATRIX_FIXTURE,
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

    valid_plan_text = VALID_BRANCH_RUNTIME_PLAN_FIXTURE.read_text(encoding="utf-8")
    runtime_negative_cases = (
        (
            "direct runtime primary proof",
            valid_plan_text.replace(
                (
                    "Troubleshooting Mode Decision: Troubleshooting launcher and direct runtime "
                    "routes are diagnostic supporting evidence only and do not replace normal "
                    "launcher proof without parity."
                ),
                (
                    "Troubleshooting Mode Decision: Direct runtime and Dev Toolkit proof are "
                    "formal proof passed for exact USER launcher proof."
                ),
            ),
            EXPECTED_RUNTIME_DIRECT_PROOF_FAILURE_SNIPPET,
        ),
        (
            "missing exact USER launcher path",
            valid_plan_text.replace(
                (
                    "Exact USER Desktop Launcher Path: Formal proof uses the exact normal "
                    "USER desktop runtime launcher path C:\\Users\\anden\\OneDrive\\Desktop\\Nexus Desktop Launcher.lnk "
                    "unless USER waiver is recorded."
                ),
                "Exact USER Desktop Launcher Path: Formal proof uses the current helper launch path unless logs are present.",
            ),
            EXPECTED_RUNTIME_EXACT_LAUNCHER_FAILURE_SNIPPET,
        ),
        (
            "missing photo/video proof",
            valid_plan_text.replace(
                (
                    "Photo / Video Proof Plan: Visible user-facing claims require photo, video, "
                    "ordered frame-sequence, or focused screenshot adjudication instead of "
                    "screenshot-exists metadata."
                ),
                "Photo / Video Proof Plan: Visible user-facing claims are complete when screenshot exists metadata is present.",
            ),
            EXPECTED_RUNTIME_PHOTO_VIDEO_FAILURE_SNIPPET,
        ),
        (
            "missing USER packet evidence",
            valid_plan_text.replace(
                (
                    "USER Packet Evidence Plan: C:\\Nexus USER review hub and UTS packet record "
                    "evidence references with PASS, FAIL, BLOCKED, UNPROVEN, or WAIVED disposition."
                ),
                "USER Packet Evidence Plan: Helper output stores proof internally for later review.",
            ),
            EXPECTED_RUNTIME_PACKET_EVIDENCE_FAILURE_SNIPPET,
        ),
    )
    for label, text, expected_snippet in runtime_negative_cases:
        case_failures = _validate_branch_runtime_plan_text(text)
        if expected_snippet not in "\n".join(case_failures):
            failures.append(
                f"Runtime observability negative fixture '{label}' did not report "
                f"expected failure snippet: {expected_snippet!r}"
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

    valid_gate_state_failures = _validate_branch_planning_gate_state_packet_text(
        VALID_BRANCH_PLANNING_GATE_STATE_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_gate_state_failures:
        failures.append(
            "Valid Branch Planning review-gate state fixture unexpectedly failed: "
            + "; ".join(valid_gate_state_failures[:5])
        )

    gate_bypass_failures = _validate_branch_planning_gate_state_packet_text(
        INVALID_BRANCH_PLANNING_GATE_BYPASS_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BRANCH_PLANNING_GATE_BYPASS_FAILURE_SNIPPET not in "\n".join(
        gate_bypass_failures
    ):
        failures.append(
            "Invalid Branch Planning review-gate fixture did not reject packet "
            "validation treated as USER acceptance"
        )

    failures.extend(_validate_primary_user_review_file_stage_priority())

    valid_bp1_failures = _validate_bp1_branch_vision_review_text(
        VALID_BP1_BRANCH_VISION_REVIEW_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_bp1_failures:
        failures.append(
            "Valid BP1 Branch Vision Review fixture unexpectedly failed: "
            + "; ".join(valid_bp1_failures[:5])
        )

    for fixture, label in (
        (VALID_BP1_FAM006_DOGFOOD_FIXTURE, "FAM-006 UI/runtime BP1 dogfood"),
        (VALID_BP1_FAM007_DOGFOOD_FIXTURE, "FAM-007 private-boundary BP1 dogfood"),
        (VALID_BP1_GOVERNANCE_DOGFOOD_FIXTURE, "Governance source-truth BP1 dogfood"),
    ):
        dogfood_failures = _validate_bp1_branch_vision_review_text(
            fixture.read_text(encoding="utf-8")
        )
        if dogfood_failures:
            failures.append(
                f"Valid {label} fixture unexpectedly failed: "
                + "; ".join(dogfood_failures[:5])
            )

    missing_context_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_MISSING_CONTEXT_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_CONTEXT_FAILURE_SNIPPET not in "\n".join(missing_context_failures):
        failures.append(
            "Invalid BP1 missing-context fixture did not reject missing Project/Family/Feature context"
        )

    shallow_recommendation_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_SHALLOW_RECOMMENDATIONS_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_SHALLOW_RECOMMENDATION_FAILURE_SNIPPET not in "\n".join(
        shallow_recommendation_failures
    ):
        failures.append(
            "Invalid BP1 shallow-recommendations fixture did not reject shallow recommendations"
        )

    template_shell_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_TEMPLATE_SHELL_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_TEMPLATE_SHELL_FAILURE_SNIPPET not in "\n".join(
        template_shell_failures
    ):
        failures.append(
            "Invalid BP1 template-shell fixture did not reject instructional placeholder content"
        )

    process_mechanics_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_PROCESS_MECHANICS_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_TEMPLATE_SHELL_FAILURE_SNIPPET not in "\n".join(
        process_mechanics_failures
    ):
        failures.append(
            "Invalid BP1 process-mechanics fixture did not reject process-only BP1 review content"
        )

    copied_surface_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_COPIED_FILE_SURFACE_ONLY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_COPIED_SURFACE_FAILURE_SNIPPET not in "\n".join(
        copied_surface_failures
    ):
        failures.append(
            "Invalid BP1 copied-file surface fixture did not reject copied-file-list-only surface map"
        )

    generic_questions_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_GENERIC_USER_QUESTIONS_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_GENERIC_QUESTIONS_FAILURE_SNIPPET not in "\n".join(
        generic_questions_failures
    ):
        failures.append(
            "Invalid BP1 generic-questions fixture did not reject non-decision-driving USER questions"
        )

    slc_centered_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_SLC_CENTERED_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_SLC_CENTERED_FAILURE_SNIPPET not in "\n".join(
        slc_centered_failures
    ):
        failures.append(
            "Invalid BP1 SLC-centered fixture did not reject SLC-centered branch vision"
        )

    technical_metadata_failures = _validate_bp1_branch_vision_review_text(
        INVALID_BP1_TECHNICAL_METADATA_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP1_TECHNICAL_METADATA_FAILURE_SNIPPET not in "\n".join(
        technical_metadata_failures
    ):
        failures.append(
            "Invalid BP1 technical-metadata fixture did not reject active branch metadata"
        )

    missing_bp1_trace_failures = _validate_bp2_branch_plan_review_text(
        INVALID_BP2_MISSING_ACCEPTED_BP1_TRACE_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP2_ACCEPTED_BP1_TRACE_FAILURE_SNIPPET not in "\n".join(
        missing_bp1_trace_failures
    ):
        failures.append(
            "Invalid BP2 missing-accepted-BP1 fixture did not reject missing accepted BP1 trace"
        )

    product_design_wording_failures = _validate_bp2_branch_plan_review_text(
        INVALID_BP2_PRODUCT_DESIGN_WORDING_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_BP2_PRODUCT_DESIGN_WORDING_FAILURE_SNIPPET not in "\n".join(
        product_design_wording_failures
    ):
        failures.append(
            "Invalid BP2 product-design wording fixture did not reject stale BP1 contract wording"
        )

    for fixture, label in (
        (VALID_BP2_FAM006_DOGFOOD_FIXTURE, "FAM-006 UI/runtime BP2 dogfood"),
        (VALID_BP2_FAM007_DOGFOOD_FIXTURE, "FAM-007 private-boundary BP2 dogfood"),
    ):
        dogfood_failures = _validate_bp2_branch_plan_review_text(
            fixture.read_text(encoding="utf-8")
        )
        if dogfood_failures:
            failures.append(
                f"Valid {label} fixture unexpectedly failed: "
                + "; ".join(dogfood_failures[:5])
            )

    bp3_pending_failures = _validate_bp3_orchestration_text(
        INVALID_BP3_IMPLEMENTATION_WITH_PENDING_BP1_BP2_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_BP3_PENDING_FAILURE_SNIPPET not in "\n".join(bp3_pending_failures):
        failures.append(
            "Invalid BP3 pending-BP1/BP2 fixture did not reject implementation approval"
        )

    valid_bp3_failures = _validate_bp3_orchestration_text(
        VALID_BP3_ACCEPTED_BP1_BP2_SLC_TRACE_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_bp3_failures:
        failures.append(
            "Valid BP3 accepted-BP1/BP2 fixture unexpectedly failed: "
            + "; ".join(valid_bp3_failures[:5])
        )

    for fixture, label in (
        (VALID_BP3_FAM006_DOGFOOD_FIXTURE, "FAM-006 UI/runtime BP3 dogfood"),
        (VALID_BP3_FAM007_DOGFOOD_FIXTURE, "FAM-007 private-boundary BP3 dogfood"),
    ):
        dogfood_failures = _validate_bp3_orchestration_text(
            fixture.read_text(encoding="utf-8")
        )
        if dogfood_failures:
            failures.append(
                f"Valid {label} fixture unexpectedly failed: "
                + "; ".join(dogfood_failures[:5])
            )

    implementation_route_source_truth_failures = (
        _validate_implementation_bearing_source_truth()
    )
    if implementation_route_source_truth_failures:
        failures.append(
            "Implementation-bearing source truth unexpectedly failed: "
            + "; ".join(implementation_route_source_truth_failures[:5])
        )

    terminology_ambiguity_failures = _validate_slice_slc_seam_model_text(
        INVALID_SLC_SLICE_SEAM_AMBIGUITY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        terminology_ambiguity_failures
    ):
        failures.append(
            "Invalid SLC/Slice/Seam terminology fixture did not reject ambiguity"
        )

    spaced_slc_seam_alias_matrix = (
        "SLC 1 is the seam for the consent shell.",
        "SLC 1 means seam for the consent shell.",
    )
    for phrase in spaced_slc_seam_alias_matrix:
        spaced_slc_seam_failures = _validate_slice_slc_seam_model_text(
            f"""
# Invalid Spaced SLC Seam Alias Matrix Case

SLC is shorthand for Slice and remains a Slice-level deliverable.
{phrase}
"""
        )
        if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
            spaced_slc_seam_failures
        ):
            failures.append(
                "Invalid spaced SLC seam alias fixture did not reject: " + phrase
            )

    for fixture, label in (
        (
            VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE,
            "multi-slice implementation carrier",
        ),
        (
            VALID_REQUIRED_SEPARATE_BRANCH_CASE_FIXTURE,
            "required separate-branch case",
        ),
    ):
        terminology_failures = _validate_slice_slc_seam_model_text(
            fixture.read_text(encoding="utf-8")
        )
        if terminology_failures:
            failures.append(
                f"Valid {label} fixture unexpectedly failed: "
                + "; ".join(terminology_failures[:5])
            )

    prose_only_multi_slice_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        )
        .replace(
            "Multi-Slice Carrier: FAM-007 provider consent shell and artifact "
            "exclusion control.",
            "Package Summary: This is a multi-slice FAM-007 provider consent "
            "shell and artifact exclusion control without future multi-slice "
            "scope creep.",
        )
        .replace(
            "Shared Owner / Worktree: One FAM-007 branch/worktree owns all "
            "slices because they serve the same public-safe provider-boundary "
            "route and one package objective.\n\n",
            "",
        )
    )
    if "Multi-slice carrier missing Shared Owner / Worktree:" not in "\n".join(
        prose_only_multi_slice_failures
    ):
        failures.append(
            "Invalid prose-only multi-slice fixture did not enforce required "
            "multi-slice evidence without the exact carrier marker"
        )

    negated_multi_slice_carrier_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Non-Multi-Slice Branch Plan

Not a Multi-Slice Carrier: This branch owns one Slice-level deliverable and
does not require multi-slice-only owner, split, or shared validation fields.

Selected Implementation Route: One branch-local governance validation repair
that keeps Slice/SLC terminology distinct from seam routing.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
    )
    if negated_multi_slice_carrier_failures:
        failures.append(
            "Valid negated multi-slice carrier declaration unexpectedly failed: "
            + "; ".join(negated_multi_slice_carrier_failures[:5])
        )

    negative_multi_slice_marker_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Single-Slice Branch Plan With Negative Multi-Slice Marker

Multi-Slice Carrier: No

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A single SLC-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
    )
    if negative_multi_slice_marker_failures:
        failures.append(
            "Valid negative Multi-Slice Carrier marker unexpectedly failed: "
            + "; ".join(negative_multi_slice_marker_failures[:5])
        )

    stale_negative_marker_with_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        )
        .replace(
            "Multi-Slice Carrier: FAM-007 provider consent shell and artifact "
            "exclusion control.",
            "Multi-Slice Carrier: No",
        )
        .replace(
            "Shared Owner / Worktree: One FAM-007 branch/worktree owns all "
            "slices because they serve the same public-safe provider-boundary "
            "route and one package objective.\n\n",
            "",
        )
    )
    if "Multi-slice carrier missing Shared Owner / Worktree:" not in "\n".join(
        stale_negative_marker_with_slice_map_failures
    ):
        failures.append(
            "Invalid stale negative carrier marker fixture did not enforce "
            "multi-slice evidence when Slice Map names multiple deliverables"
        )

    no_split_multi_slice_marker_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        )
        .replace(
            "Multi-Slice Carrier: FAM-007 provider consent shell and artifact "
            "exclusion control.",
            "Multi-Slice Carrier: No split required; this multi-slice carrier "
            "remains branch-local because all slices serve one package route.",
        )
        .replace(
            "Shared Owner / Worktree: One FAM-007 branch/worktree owns all "
            "slices because they serve the same public-safe provider-boundary "
            "route and one package objective.\n\n",
            "",
        )
    )
    if "Multi-slice carrier missing Shared Owner / Worktree:" not in "\n".join(
        no_split_multi_slice_marker_failures
    ):
        failures.append(
            "Invalid no-split multi-slice marker fixture did not enforce "
            "required multi-slice evidence"
        )

    future_gated_multi_slice_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Single-Slice Branch Plan With Future-Gated Multi-Slice Boundary

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.

Future-Gated Boundaries: Future multi-slice package expansion remains
USER-gated and outside this current branch plan.
"""
    )
    if future_gated_multi_slice_failures:
        failures.append(
            "Valid future-gated multi-slice boundary unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(future_gated_multi_slice_failures[:5])
        )

    package_summary_future_gated_multi_slice_failures = (
        _validate_slice_slc_seam_model_text(
            """
# Valid Single-Slice Branch Plan With Package Summary Future-Gated Boundary

Package Summary: Future multi-slice package expansion remains USER-gated and
outside this current branch plan.

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
        )
    )
    if package_summary_future_gated_multi_slice_failures:
        failures.append(
            "Valid package-summary future-gated multi-slice boundary unexpectedly "
            "triggered current multi-slice carrier enforcement: "
            + "; ".join(package_summary_future_gated_multi_slice_failures[:5])
        )

    package_summary_postfixed_future_gated_multi_slice_failures = (
        _validate_slice_slc_seam_model_text(
            """
# Valid Package Summary With Postfixed Future-Gated Multi-Slice Boundary

Package Summary: Multi-slice package expansion remains future-gated and outside
this current branch plan.

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
        )
    )
    if package_summary_postfixed_future_gated_multi_slice_failures:
        failures.append(
            "Valid package-summary postfixed future-gated multi-slice boundary "
            "unexpectedly triggered current multi-slice carrier enforcement: "
            + "; ".join(package_summary_postfixed_future_gated_multi_slice_failures[:5])
        )

    explanatory_negative_multi_slice_marker_failures = (
        _validate_slice_slc_seam_model_text(
            """
# Valid Explanatory Negative Multi-Slice Marker

Multi-Slice Carrier: Not applicable; future multi-slice expansion remains USER-gated.

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
        )
    )
    if explanatory_negative_multi_slice_marker_failures:
        failures.append(
            "Valid explanatory negative multi-slice marker unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(explanatory_negative_multi_slice_marker_failures[:5])
        )

    future_gated_only_multi_slice_marker_failures = (
        _validate_slice_slc_seam_model_text(
            """
# Valid Future-Gated-Only Multi-Slice Marker

Multi-Slice Carrier: Future-gated only; multi-slice expansion remains USER-gated and non-current.

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
        )
    )
    if future_gated_only_multi_slice_marker_failures:
        failures.append(
            "Valid future-gated-only multi-slice marker unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(future_gated_only_multi_slice_marker_failures[:5])
        )

    route_policy_multi_slice_reference_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Single-Slice Governance Repair That Mentions Multi-Slice Policy

Selected Implementation Route: Implement governance validator behavior that
prevents multi-slice branches from splitting incorrectly.

Concrete Deliverable: A validator repair that checks multi-slice carrier policy
without making this governance branch a multi-slice implementation carrier.

Implementation Route Class: governance/source-truth validator implementation.
"""
    )
    if route_policy_multi_slice_reference_failures:
        failures.append(
            "Valid route-policy multi-slice reference unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(route_policy_multi_slice_reference_failures[:5])
        )

    package_summary_policy_multi_slice_reference_failures = (
        _validate_slice_slc_seam_model_text(
            """
# Valid Package Summary That Mentions Multi-Slice Policy

Package Summary: This governance package validates multi-slice carrier policy
without making this branch a multi-slice implementation carrier.

Selected Implementation Route: One branch-local governance validation repair
that keeps the current branch scoped to one Slice-level deliverable.

Concrete Deliverable: A validator repair that checks multi-slice carrier policy
without creating current multi-slice package scope.
"""
        )
    )
    if package_summary_policy_multi_slice_reference_failures:
        failures.append(
            "Valid package-summary multi-slice policy reference unexpectedly "
            "triggered current multi-slice carrier enforcement: "
            + "; ".join(package_summary_policy_multi_slice_reference_failures[:5])
        )

    postfixed_negated_multi_slice_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Single-Slice Branch Plan With Postfixed Multi-Slice Negation

Package Summary: Multi-slice not required for this branch; the current route
owns one Slice-level governance validator repair.

Selected Implementation Route: One branch-local governance validation repair
that keeps Slice/SLC terminology distinct from seam routing.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
    )
    if postfixed_negated_multi_slice_failures:
        failures.append(
            "Valid postfixed multi-slice negation unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(postfixed_negated_multi_slice_failures[:5])
        )

    postfixed_negated_multiple_slices_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Single-Slice Branch Plan With Postfixed Multiple-Slices Negation

Package Summary: Multiple slices not required for this branch; the current
route owns one Slice-level governance validator repair.

Selected Implementation Route: One branch-local governance validation repair
that keeps Slice/SLC terminology distinct from seam routing.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
    )
    if postfixed_negated_multiple_slices_failures:
        failures.append(
            "Valid postfixed multiple-slices negation unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(postfixed_negated_multiple_slices_failures[:5])
        )

    prefixed_negated_multiple_slices_failures = _validate_slice_slc_seam_model_text(
        """
# Valid Single-Slice Branch Plan With Prefixed Multiple-Slices Negation

Package Summary: This branch is not multiple slices; the current route owns
one Slice-level governance validator repair.

Selected Implementation Route: One branch-local governance validation repair
that keeps Slice/SLC terminology distinct from seam routing.

Concrete Deliverable: A single Slice-level validator proof for branch planning
terminology without creating a multi-slice package carrier.
"""
    )
    if prefixed_negated_multiple_slices_failures:
        failures.append(
            "Valid prefixed multiple-slices negation unexpectedly triggered "
            "current multi-slice carrier enforcement: "
            + "; ".join(prefixed_negated_multiple_slices_failures[:5])
        )

    slice_map_only_multi_slice_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        )
        .replace(
            "Multi-Slice Carrier: FAM-007 provider consent shell and artifact "
            "exclusion control.\n",
            "",
        )
        .replace(
            "Shared Owner / Worktree: One FAM-007 branch/worktree owns all "
            "slices because they serve the same public-safe provider-boundary "
            "route and one package objective.\n\n",
            "",
        )
    )
    if "Multi-slice carrier missing Shared Owner / Worktree:" not in "\n".join(
        slice_map_only_multi_slice_failures
    ):
        failures.append(
            "Invalid Slice Map-only multi-slice fixture did not infer current "
            "multi-slice carrier enforcement"
        )

    slc_id_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: SLC-001 implements consent-shell disabled-state source-truth "
            "and review copy. slc-002 implements public artifact exclusion "
            "validator/helper enforcement.",
        )
    )
    if slc_id_slice_map_failures:
        failures.append(
            "Valid SLC-ID Slice Map fixture unexpectedly failed: "
            + "; ".join(slc_id_slice_map_failures[:5])
        )

    multiline_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map:\n"
            "- Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy.\n"
            "- Slice 2 / SLC-002 implements public artifact exclusion "
            "validator/helper enforcement.\n"
            "- Slice 3 / SLC-003 implements packet proof and future-gated "
            "boundary preservation.",
        )
    )
    if multiline_slice_map_failures:
        failures.append(
            "Valid multiline Slice Map fixture unexpectedly failed: "
            + "; ".join(multiline_slice_map_failures[:5])
        )

    numbered_multiline_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map:\n"
            "1. Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy.\n"
            "2. Slice 2 / SLC-002 implements public artifact exclusion "
            "validator/helper enforcement.\n"
            "3. Slice 3 / SLC-003 implements packet proof and future-gated "
            "boundary preservation.",
        )
    )
    if numbered_multiline_slice_map_failures:
        failures.append(
            "Valid numbered multiline Slice Map fixture unexpectedly failed: "
            + "; ".join(numbered_multiline_slice_map_failures[:5])
        )

    colon_labeled_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map:\n"
            "- SLC-001: consent-shell disabled-state source-truth and review copy.\n"
            "- SLC-002: public artifact exclusion validator/helper enforcement.\n"
            "- SLC-003: packet proof and future-gated boundary preservation.",
        )
    )
    if colon_labeled_slice_map_failures:
        failures.append(
            "Valid colon-labeled Slice Map fixture unexpectedly failed: "
            + "; ".join(colon_labeled_slice_map_failures[:5])
        )

    same_sentence_slc_id_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: SLC-001 and SLC-002 implement consent-shell disabled-state "
            "source-truth, review copy, and public artifact exclusion "
            "validator/helper enforcement.",
        )
    )
    if same_sentence_slc_id_slice_map_failures:
        failures.append(
            "Valid same-sentence SLC-ID Slice Map fixture unexpectedly failed: "
            + "; ".join(same_sentence_slc_id_slice_map_failures[:5])
        )

    single_slc_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy.",
        )
    )
    if "Multi-slice carrier must map at least two slices" not in "\n".join(
        single_slc_slice_map_failures
    ):
        failures.append(
            "Invalid single SLC Slice Map fixture did not reject one deliverable "
            "written with Slice plus SLC wording"
        )

    mismatched_slice_slc_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: Slice 1 / SLC-002 implements consent-shell disabled-state "
            "source-truth and review copy.",
        )
    )
    if "Multi-slice carrier must map at least two slices" not in "\n".join(
        mismatched_slice_slc_slice_map_failures
    ):
        failures.append(
            "Invalid mismatched Slice/SLC Slice Map fixture did not reject one "
            "mapped entry written with two label namespaces"
        )

    mismatched_pair_plus_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: Slice 1 / SLC-002 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 3 / SLC-003 implements public "
            "artifact exclusion validator/helper enforcement.",
        )
    )
    if (
        "Multi-slice carrier Slice Map contains mismatched Slice/SLC alias pair"
        not in "\n".join(mismatched_pair_plus_slice_map_failures)
    ):
        failures.append(
            "Invalid mismatched Slice/SLC pair plus another slice fixture did not "
            "reject ambiguous alias-pair wording"
        )

    duplicate_slice_id_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: Slice 1 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 1 implements public artifact "
            "exclusion validator/helper enforcement.",
        )
    )
    if "Multi-slice carrier must map at least two slices" not in "\n".join(
        duplicate_slice_id_slice_map_failures
    ):
        failures.append(
            "Invalid duplicate Slice ID Slice Map fixture did not reject two "
            "mapped entries for the same slice"
        )

    duplicate_slice_slc_pair_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 1 / SLC-001 implements public "
            "artifact exclusion validator/helper enforcement.",
        )
    )
    if "Multi-slice carrier must map at least two slices" not in "\n".join(
        duplicate_slice_slc_pair_slice_map_failures
    ):
        failures.append(
            "Invalid duplicate Slice/SLC pair Slice Map fixture did not reject "
            "two mapped entries for the same zero-padded SLC alias"
        )

    repeated_generic_slice_map_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Slice Map: Slice 1 / SLC-001 implements consent-shell disabled-state "
            "source-truth and review copy. Slice 2 / SLC-002 implements public "
            "artifact exclusion validator/helper enforcement. Slice 3 / SLC-003 "
            "implements packet proof and future-gated boundary preservation.",
            "Slice Map: The current slice implements consent-shell disabled-state "
            "source-truth and review copy. The same slice validates helper "
            "enforcement. This slice records packet proof.",
        )
    )
    if "Multi-slice carrier must map at least two slices" not in "\n".join(
        repeated_generic_slice_map_failures
    ):
        failures.append(
            "Invalid repeated generic slice-map fixture did not reject prose-only "
            "slice mentions without distinct Slice/SLC identifiers"
        )

    slc_id_branch_ambiguity_failures = _validate_slice_slc_seam_model_text(
        """
# Invalid SLC ID Branch Split Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLC-001 is a separate branch for the consent shell.
"""
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        slc_id_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid SLC-ID branch ambiguity fixture did not reject SLC-as-branch "
            "wording after valid alias wording"
        )

    plural_slc_branch_ambiguity_failures = _validate_slice_slc_seam_model_text(
        """
# Invalid Plural SLC Branch Split Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLCs are separate branches for the consent shell and artifact boundary.
"""
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        plural_slc_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid plural SLC branch ambiguity fixture did not reject SLCs-as-branches "
            "wording after valid alias wording"
        )

    coordinated_slc_branch_ambiguity_failures = _validate_slice_slc_seam_model_text(
        """
# Invalid Coordinated SLC Branch Split Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLC-001 and SLC-002 are separate branches for the consent shell and artifact boundary.
"""
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        coordinated_slc_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid coordinated SLC branch ambiguity fixture did not reject "
            "numbered SLCs-as-branches wording after valid alias wording"
        )

    bare_slc_branch_ambiguity_failures = _validate_slice_slc_seam_model_text(
        """
# Invalid Bare SLC Branch Identity Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLC-001 is a branch for the consent shell.
"""
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        bare_slc_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid bare SLC branch identity fixture did not reject SLC-as-branch "
            "wording without the word separate"
        )

    plural_bare_slc_branch_ambiguity_failures = _validate_slice_slc_seam_model_text(
        """
# Invalid Plural Bare SLC Branch Identity Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLCs are branches for the consent shell and artifact boundary.
"""
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        plural_bare_slc_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid plural bare SLC branch identity fixture did not reject "
            "SLCs-as-branches wording without the word separate"
        )

    coordinated_bare_slc_branch_ambiguity_failures = (
        _validate_slice_slc_seam_model_text(
            """
# Invalid Coordinated Bare SLC Branch Identity Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLC-001 and SLC-002 are branches for the consent shell and artifact boundary.
"""
        )
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        coordinated_bare_slc_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid coordinated bare SLC branch identity fixture did not reject "
            "numbered SLCs-as-branches wording without the word separate"
        )

    adjective_slc_branch_ambiguity_failures = _validate_slice_slc_seam_model_text(
        """
# Invalid SLC Branch Adjective Ambiguity

SLC is shorthand for Slice and remains a Slice-level deliverable.
The SLC-001 branch owns the consent shell while SLC-002 branch owns the artifact boundary.
"""
    )
    if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
        adjective_slc_branch_ambiguity_failures
    ):
        failures.append(
            "Invalid SLC branch adjective fixture did not reject numbered "
            "SLC-as-branch wording after valid alias wording"
        )

    slc_branch_identity_matrix = (
        "SLC-001 branch owns the consent shell.",
        "SLC-001 owns a branch for the consent shell.",
        "SLC-002 has its own branch for the artifact boundary.",
        "SLC 1 is a branch for the consent shell.",
        "SLC 1 owns a branch for the consent shell.",
        "SLC 1 and SLC 2 own branches for the consent shell and artifact boundary.",
        "SLCs own branches for the consent shell and artifact boundary.",
        "SLC-001 and SLC-002 own branches for the consent shell and artifact boundary.",
        "SLC-001 and SLC-002 have branches for the consent shell and artifact boundary.",
        "Create a branch for SLC-003.",
        "Each SLC has a branch for implementation.",
    )
    for phrase in slc_branch_identity_matrix:
        matrix_failures = _validate_slice_slc_seam_model_text(
            f"""
# Invalid SLC Branch Identity Matrix Case

SLC is shorthand for Slice and remains a Slice-level deliverable.
{phrase}
"""
        )
        if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(matrix_failures):
            failures.append(
                "Invalid SLC branch identity matrix fixture did not reject: "
                + phrase
            )

    branch_planning_alias_failures = _validate_slice_slc_seam_model_text(
        """
# Valid SLC Branch-Planning Alias Wording

SLC is a branch-planning alias for Slice-level line items and preserved
historical Slice IDs, not a seam or separate branch.
"""
    )
    if branch_planning_alias_failures:
        failures.append(
            "Valid SLC branch-planning alias fixture unexpectedly failed: "
            + "; ".join(branch_planning_alias_failures[:5])
        )

    branch_material_alias_failures = _validate_slice_slc_seam_model_text(
        """
# Valid SLC Branch-Material Alias Wording

SLC is shorthand for Slice and remains a Slice-level deliverable.
SLC-001 branch-material scaffolding is historical wording for one Slice-level
line item, not a seam or separate branch.
"""
    )
    if branch_material_alias_failures:
        failures.append(
            "Valid SLC branch-material alias fixture unexpectedly failed: "
            + "; ".join(branch_material_alias_failures[:5])
        )

    negated_same_branch_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Decision: Split not required; same branch remains legal because "
            "the slices share one FAM, one package, one selected implementation "
            "route, one owner/worktree, aligned PR timing, and one validation/proof path.",
            "Split Decision: same branch is not legal for this work; split required.",
        )
    )
    if "Multi-slice carrier must prove why the grouped branch is legal" not in "\n".join(
        negated_same_branch_failures
    ):
        failures.append(
            "Invalid negated same-branch multi-slice fixture did not reject split-required wording"
        )

    undecided_same_branch_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Decision: Split not required; same branch remains legal because "
            "the slices share one FAM, one package, one selected implementation "
            "route, one owner/worktree, aligned PR timing, and one validation/proof path.",
            "Split Decision: pending decision whether same branch can remain "
            "legal after USER review.",
        )
    )
    if "Multi-slice carrier must prove why the grouped branch is legal" not in "\n".join(
        undecided_same_branch_failures
    ):
        failures.append(
            "Invalid undecided same-branch multi-slice fixture did not reject "
            "pending split-decision wording"
        )

    affirmative_same_branch_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Decision: Split not required; same branch remains legal because "
            "the slices share one FAM, one package, one selected implementation "
            "route, one owner/worktree, aligned PR timing, and one validation/proof path.",
            "Split Decision: The same branch can remain legal because the slices "
            "share one FAM, one package, one selected implementation route, one "
            "owner/worktree, aligned PR timing, and one validation/proof path.",
        )
    )
    if affirmative_same_branch_failures:
        failures.append(
            "Valid affirmative same-branch multi-slice fixture unexpectedly failed: "
            + "; ".join(affirmative_same_branch_failures[:5])
        )

    no_split_required_same_branch_failures = _validate_slice_slc_seam_model_text(
        VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Decision: Split not required; same branch remains legal because "
            "the slices share one FAM, one package, one selected implementation "
            "route, one owner/worktree, aligned PR timing, and one validation/proof path.",
            "Split Decision: No split required; same branch remains legal because "
            "the slices share one FAM, one package, one selected implementation "
            "route, one owner/worktree, aligned PR timing, and one validation/proof path.",
        )
    )
    if no_split_required_same_branch_failures:
        failures.append(
            "Valid no-split-required same-branch multi-slice fixture unexpectedly failed: "
            + "; ".join(no_split_required_same_branch_failures[:5])
        )

    no_separate_branch_required_same_branch_failures = (
        _validate_slice_slc_seam_model_text(
            VALID_MULTI_SLICE_IMPLEMENTATION_CARRIER_FIXTURE.read_text(
                encoding="utf-8"
            ).replace(
                "Split Decision: Split not required; same branch remains legal because "
                "the slices share one FAM, one package, one selected implementation "
                "route, one owner/worktree, aligned PR timing, and one validation/proof path.",
                "Split Decision: No separate branch required; same branch remains legal "
                "because the slices share one FAM, one package, one selected "
                "implementation route, one owner/worktree, aligned PR timing, and "
                "one validation/proof path.",
            )
        )
    )
    if no_separate_branch_required_same_branch_failures:
        failures.append(
            "Valid no-separate-branch-required same-branch multi-slice fixture unexpectedly failed: "
            + "; ".join(no_separate_branch_required_same_branch_failures[:5])
        )

    negated_split_required_failures = _validate_slice_slc_seam_model_text(
        VALID_REQUIRED_SEPARATE_BRANCH_CASE_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Required: Yes. The private Owner lane memory route must wait "
            "for a separate USER-approved carrier because it crosses private "
            "storage, provider/runtime/cache/memory behavior, and owner/worktree "
            "boundaries.",
            "Split Required: Not required; keep same branch.",
        )
    )
    if (
        "Required separate branch case must explicitly require a split"
        not in "\n".join(negated_split_required_failures)
    ):
        failures.append(
            "Invalid negated required-separate-branch fixture did not reject "
            "not-required same-branch wording"
        )

    generic_required_split_failures = _validate_slice_slc_seam_model_text(
        VALID_REQUIRED_SEPARATE_BRANCH_CASE_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Required: Yes. The private Owner lane memory route must wait "
            "for a separate USER-approved carrier because it crosses private "
            "storage, provider/runtime/cache/memory behavior, and owner/worktree "
            "boundaries.",
            "Split Required: USER approval required before deciding whether to split.",
        )
    )
    if (
        "Required separate branch case must explicitly require a split"
        not in "\n".join(generic_required_split_failures)
    ):
        failures.append(
            "Invalid generic-required separate-branch fixture did not reject "
            "undecided split wording"
        )

    blocked_same_branch_required_split_failures = _validate_slice_slc_seam_model_text(
        VALID_REQUIRED_SEPARATE_BRANCH_CASE_FIXTURE.read_text(
            encoding="utf-8"
        ).replace(
            "Split Required: Yes. The private Owner lane memory route must wait "
            "for a separate USER-approved carrier because it crosses private "
            "storage, provider/runtime/cache/memory behavior, and owner/worktree "
            "boundaries.",
            "Split Required: Yes. Same branch is blocked; separate branch required "
            "because the route crosses private storage, provider/runtime/cache/memory "
            "behavior, and owner/worktree boundaries.",
        )
    )
    if blocked_same_branch_required_split_failures:
        failures.append(
            "Valid blocked-same-branch required-separate-branch fixture "
            "unexpectedly failed: "
            + "; ".join(blocked_same_branch_required_split_failures[:5])
        )

    planning_only_route_failures = _validate_implementation_bearing_route_text(
        INVALID_IMPLEMENTATION_ROUTE_PLANNING_ONLY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_IMPLEMENTATION_ROUTE_FAILURE_SNIPPET not in "\n".join(
        planning_only_route_failures
    ):
        failures.append(
            "Invalid planning-only implementation-route fixture did not reject "
            "lane/setup-only carrier admission"
        )

    for fixture, label in (
        (
            VALID_IMPLEMENTATION_ROUTE_SECURITY_BOUNDARY_FIXTURE,
            "security/trust-boundary implementation route",
        ),
        (
            VALID_IMPLEMENTATION_ROUTE_BP2_HOLD_ACTION_GATE_FIXTURE,
            "BP2 HOLD exact USER action gate route",
        ),
        (
            VALID_IMPLEMENTATION_ROUTE_RETARGET_RENAME_FIXTURE,
            "retarget/rename implementation route",
        ),
    ):
        route_failures = _validate_implementation_bearing_route_text(
            fixture.read_text(encoding="utf-8")
        )
        if route_failures:
            failures.append(
                f"Valid {label} fixture unexpectedly failed: "
                + "; ".join(route_failures[:5])
            )

    external_retarget_failures = external_state.validate_implementation_route_values(
        VALID_IMPLEMENTATION_ROUTE_RETARGET_RENAME_FIXTURE.read_text(encoding="utf-8")
    )
    if external_retarget_failures:
        failures.append(
            "External-state validator retarget/rename fixture unexpectedly failed: "
            + "; ".join(external_retarget_failures[:5])
        )

    br2_blocker_failures = _validate_br2_route_blocker_packet_text(
        VALID_BR2_ROUTE_BLOCKER_PACKET_FIXTURE.read_text(encoding="utf-8")
    )
    if br2_blocker_failures:
        failures.append(
            "Valid BR2 route blocker packet fixture unexpectedly failed: "
            + "; ".join(br2_blocker_failures[:5])
        )

    br2_none_word_failures = _validate_br2_route_blocker_packet_text(
        VALID_BR2_ROUTE_BLOCKER_NONE_WORD_ROUTE_FIXTURE.read_text(encoding="utf-8")
    )
    if br2_none_word_failures:
        failures.append(
            "Valid BR2 none-word route blocker packet fixture unexpectedly failed: "
            + "; ".join(br2_none_word_failures[:5])
        )

    no_route_continue_failures = _validate_br2_route_blocker_packet_text(
        INVALID_BR2_ROUTE_BLOCKER_NO_ROUTE_CONTINUE_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_BR2_NO_ROUTE_CONTINUE_FAILURE_SNIPPET not in "\n".join(
        no_route_continue_failures
    ):
        failures.append(
            "Invalid BR2 no-route continue-planning fixture did not reject "
            "continued planning after no concrete route remained"
        )

    marker_only_deferral_failures = _validate_br2_route_blocker_packet_text(
        INVALID_BR2_ROUTE_BLOCKER_MARKER_ONLY_DEFERRAL_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_BR2_MARKER_ONLY_DEFERRAL_FAILURE_SNIPPET not in "\n".join(
        marker_only_deferral_failures
    ):
        failures.append(
            "Invalid BR2 marker-only deferral fixture did not reject missing "
            "deferral decision wording outside marker labels"
        )

    fake_feature_label_failures = _validate_implementation_bearing_route_text(
        INVALID_IMPLEMENTATION_ROUTE_FAKE_FEATURE_LABEL_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_FAKE_FEATURE_LABEL_FAILURE_SNIPPET not in "\n".join(
        fake_feature_label_failures
    ):
        failures.append(
            "Invalid fake-feature-label implementation-route fixture did not "
            "reject setup/readiness/packet feature wording"
        )

    proof_boundary_label_failures = _validate_implementation_bearing_route_text(
        INVALID_IMPLEMENTATION_ROUTE_PROOF_BOUNDARY_LABEL_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_PROOF_BOUNDARY_LABEL_FAILURE_SNIPPET not in "\n".join(
        proof_boundary_label_failures
    ):
        failures.append(
            "Invalid proof/boundary-label implementation-route fixture did not "
            "reject proof or boundary-control wording without implemented behavior"
        )

    tbd_output_failures = _validate_implementation_bearing_route_text(
        INVALID_IMPLEMENTATION_ROUTE_TBD_OUTPUT_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_TBD_IMPLEMENTATION_OUTPUT_FAILURE_SNIPPET not in "\n".join(
        tbd_output_failures
    ):
        failures.append(
            "Invalid TBD implementation-output fixture did not reject BP2-will-decide-later wording"
        )

    blank_selected_route_failures = _validate_implementation_bearing_route_text(
        INVALID_IMPLEMENTATION_ROUTE_BLANK_SELECTED_ROUTE_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_BLANK_SELECTED_ROUTE_FAILURE_SNIPPET not in "\n".join(
        blank_selected_route_failures
    ):
        failures.append(
            "Invalid blank selected-route fixture did not reject missing route marker value"
        )

    negated_route_behavior_failures = _validate_implementation_bearing_route_text(
        INVALID_IMPLEMENTATION_ROUTE_NEGATED_BEHAVIOR_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_NEGATED_ROUTE_BEHAVIOR_FAILURE_SNIPPET not in "\n".join(
        negated_route_behavior_failures
    ):
        failures.append(
            "Invalid negated-behavior route fixture did not reject explicit "
            "non-implementation wording"
        )

    proof_only_br2_failures = _validate_br2_route_blocker_packet_text(
        INVALID_BR2_ROUTE_BLOCKER_PROOF_ONLY_ROUTE_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_BR2_PROOF_ONLY_ROUTE_FAILURE_SNIPPET not in "\n".join(
        proof_only_br2_failures
    ):
        failures.append(
            "Invalid BR2 proof-only route fixture did not reject proof/readiness route wording"
        )

    active_external_source = inspect.getsource(_validate_active_external_branch_plan_posture)
    if 'Path("C:/Nexus Governance State")' in active_external_source:
        failures.append(
            "Active external branch-plan posture validation must use DEFAULT_EXTERNAL_STATE_ROOT"
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_state_root = Path(temp_dir)
        temp_central = temp_state_root / "central"
        temp_branch = temp_state_root / "branches" / "feature_fixture"
        temp_central.mkdir(parents=True)
        temp_branch.mkdir(parents=True)
        temp_plan = temp_branch / "branch_plan.md"
        temp_plan.write_text(
            "# Fixture Active Branch Plan\n\n"
            "Selected Implementation Route: Concrete control shell\n",
            encoding="utf-8",
        )
        (temp_central / "active_branch_authority_state.md").write_text(
            "# Fixture Active Branch Authority State\n\n"
            f"Branch Runtime Engineering Plan: `{temp_plan}`\n"
            "Next Legal Phase: `BP1 USER Branch Vision Review`\n",
            encoding="utf-8",
        )
        central_only_failures = _validate_active_external_branch_plan_posture(
            temp_state_root
        )
        external_validator_failures = external_state.validate_active_branch_plan_posture(
            temp_state_root
        )
        if (
            "External active branch state routes to BP1 without implementation-bearing route fields in active branch plan"
            not in "\n".join(central_only_failures)
        ):
            failures.append(
                "Central active-state Next Legal Phase fixture did not reject "
                "missing implementation-bearing route fields"
            )
        if (
            "External active branch state routes to BP1 without implementation-bearing route fields in active branch plan"
            not in "\n".join(external_validator_failures)
        ):
            failures.append(
                "External-state validator fixture did not reject missing "
                "implementation-bearing route fields"
            )
        temp_plan.write_text(
            "# Fixture Active Branch Plan\n\n"
            "Selected Implementation Route: Planning feature for later branch selection\n"
            "Implementation Route Class: governance/source-truth planning\n"
            "Concrete Deliverable: Readiness proof packet that documents route options only\n"
            "Implementation Output: BP2 will decide implementation output later\n"
            "Infrastructure / Setup Relationship: Lane setup only\n"
            "USER Action Gate: USER chooses later after more options\n"
            "Route Disposition: PROCEED\n"
            "Retarget / Rename Recommendation: None\n",
            encoding="utf-8",
        )
        marker_only_route_failures = external_state.validate_active_branch_plan_posture(
            temp_state_root
        )
        marker_only_route_failure_text = "\n".join(marker_only_route_failures)
        if (
            "External active branch plan route values cannot defer implementation output"
            not in marker_only_route_failure_text
            or "External active branch plan route values cannot label planning"
            not in marker_only_route_failure_text
        ):
            failures.append(
                "External-state validator fixture did not reject populated "
                "planning-only/TBD route values"
            )

        temp_plan.write_text(
            "# Fixture Active Branch Plan\n\n"
            "- Selected Implementation Route: Implement source-truth validator "
            "control for security trust-boundary enforcement behavior\n"
            "- Implementation Route Class: governance/source-truth validator "
            "implementation\n"
            "- Concrete Deliverable: Validator enforcement behavior blocks public "
            "provider execution when required consent markers are missing.\n"
            "- Implementation Output: Workstream implements validator behavior "
            "that rejects unsafe public trust-boundary state transitions before "
            "BP1.\n"
            "- Infrastructure / Setup Relationship: Execution-enabling for the "
            "selected implementation route and exact USER action gate.\n"
            "- USER Action Gate: USER approves this implementation-bearing "
            "validation route before BP1 proceeds.\n"
            "- Route Disposition: PROCEED\n"
            "- Retarget / Rename Recommendation: None\n\n"
            "SLC is the seam.\n",
            encoding="utf-8",
        )
        external_terminology_failures = (
            external_state.validate_active_branch_plan_posture(temp_state_root)
        )
        if EXPECTED_SLC_SLICE_SEAM_FAILURE_SNIPPET not in "\n".join(
            external_terminology_failures
        ):
            failures.append(
                "External-state validator fixture did not reject active branch-plan "
                "SLC/Slice/Seam terminology ambiguity"
            )

        temp_plan.write_text(
            "# Fixture Active Branch Plan\n\n"
            "- Selected Implementation Route: Implement source-truth validator "
            "control for security trust-boundary enforcement behavior\n"
            "- Implementation Route Class: governance/source-truth validator "
            "implementation\n"
            "- Concrete Deliverable: Validator enforcement behavior blocks public "
            "provider execution when required consent markers are missing.\n"
            "- Implementation Output: Workstream implements validator behavior "
            "that rejects unsafe public trust-boundary state transitions before "
            "BP1.\n"
            "- Infrastructure / Setup Relationship: Execution-enabling for the "
            "selected implementation route and exact USER action gate.\n"
            "- USER Action Gate: USER approves this implementation-bearing "
            "validation route before BP1 proceeds.\n"
            "- Route Disposition: PROCEED\n"
            "- Retarget / Rename Recommendation: None\n\n"
            "SLC is shorthand for Slice and remains a Slice-level deliverable, "
            "not a seam or separate branch.\n",
            encoding="utf-8",
        )
        external_shorthand_failures = (
            external_state.validate_active_branch_plan_posture(temp_state_root)
        )
        if external_shorthand_failures:
            failures.append(
                "External-state validator shorthand-for-Slice fixture unexpectedly failed: "
                + "; ".join(external_shorthand_failures[:5])
            )

        temp_plan.write_text(
            "# Fixture Active Branch Plan\n\n"
            "- Selected Implementation Route: Implement source-truth validator "
            "control for security trust-boundary enforcement behavior\n"
            "- Implementation Route Class: governance/source-truth validator "
            "implementation\n"
            "- Concrete Deliverable: Validator enforcement behavior blocks public "
            "provider execution when required consent markers are missing.\n"
            "- Implementation Output: Workstream implements validator behavior "
            "that rejects unsafe public trust-boundary state transitions before "
            "BP1.\n"
            "- Infrastructure / Setup Relationship: Execution-enabling for the "
            "selected implementation route and exact USER action gate.\n"
            "- USER Action Gate: USER approves this implementation-bearing "
            "validation route before BP1 proceeds.\n"
            "- Route Disposition: PROCEED\n"
            "- Retarget / Rename Recommendation: None\n",
            encoding="utf-8",
        )
        (temp_central / "active_branch_authority_state.md").write_text(
            "# Fixture Active Branch Authority State\n\n"
            f"- Branch Runtime Engineering Plan: `{temp_plan}`\n"
            "- Next Legal Phase: `BP1 USER Branch Vision Review`\n",
            encoding="utf-8",
        )
        bulleted_marker_failures = external_state.validate_active_branch_plan_posture(
            temp_state_root
        )
        if bulleted_marker_failures:
            failures.append(
                "External-state validator bulleted-marker fixture unexpectedly failed: "
                + "; ".join(bulleted_marker_failures[:5])
            )

        (temp_central / "active_branch_authority_state.md").write_text(
            "# Fixture Active Branch Authority State\n\n"
            "- Branch Runtime Engineering Plan: Accepted\n"
            f"- Branch Runtime Engineering Plan Path: `{temp_plan}`\n"
            "- Next Legal Phase: `BP1 USER Branch Vision Review`\n",
            encoding="utf-8",
        )
        plan_path_marker_failures = external_state.validate_active_branch_plan_posture(
            temp_state_root
        )
        if plan_path_marker_failures:
            failures.append(
                "External-state validator Branch Runtime Engineering Plan Path fixture "
                "unexpectedly failed: "
                + "; ".join(plan_path_marker_failures[:5])
            )

        temp_plan.write_text(
            "# Fixture Active Branch Plan\n\n"
            "- Selected Implementation Route: Implement source-truth validator "
            "control for security trust-boundary enforcement behavior\n"
            "- Implementation Route Class: governance/source-truth validator "
            "implementation\n"
            "- Concrete Deliverable: Validator enforcement behavior blocks public "
            "provider execution when required consent markers are missing.\n"
            "- Implementation Output: Workstream implements validator behavior "
            "that rejects unsafe public trust-boundary state transitions before "
            "BP1.\n"
            "- Infrastructure / Setup Relationship: Execution-enabling for the "
            "selected implementation route and exact USER action gate.\n"
            "- USER Action Gate: USER approves this implementation-bearing "
            "validation route before BP1 proceeds.\n"
            "- Route Disposition: hold\n"
            "- Retarget / Rename Recommendation: None\n",
            encoding="utf-8",
        )
        lowercase_hold_failures = external_state.validate_active_branch_plan_posture(
            temp_state_root
        )
        if (
            "External active branch state routes to BP1 while active branch plan "
            "is still HOLD/RETARGET route resolution"
            not in "\n".join(lowercase_hold_failures)
        ):
            failures.append(
                "External-state validator fixture did not reject lowercase "
                "HOLD/RETARGET route disposition before BP1"
            )

    active_packet_metadata_failures = _validate_user_packet_metadata_text(
        INVALID_USER_PACKET_ACTIVE_BRANCH_METADATA_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_USER_PACKET_ACTIVE_METADATA_FAILURE_SNIPPET not in "\n".join(
        active_packet_metadata_failures
    ):
        failures.append(
            "Invalid USER packet active-metadata fixture did not reject branch metadata"
        )

    zip_hash_packet_failures = _validate_user_packet_metadata_text(
        INVALID_USER_PACKET_ZIP_HASH_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_USER_PACKET_ZIP_HASH_FAILURE_SNIPPET not in "\n".join(
        zip_hash_packet_failures
    ):
        failures.append(
            "Invalid USER packet ZIP-hash fixture did not reject hash metadata"
        )

    desktop_upload_packet_failures = _validate_user_packet_metadata_text(
        INVALID_USER_PACKET_DESKTOP_ACTIVE_UPLOAD_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_USER_PACKET_DESKTOP_ACTIVE_UPLOAD_FAILURE_SNIPPET not in "\n".join(
        desktop_upload_packet_failures
    ):
        failures.append(
            "Invalid USER packet Desktop/OneDrive upload fixture did not reject active upload path"
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

    valid_cross_fam_text = VALID_CROSS_FAM_DEPENDENCY_CANDIDATE_FIXTURE.read_text(
        encoding="utf-8"
    )
    valid_cross_fam_failures = _validate_cross_fam_dependency_packet_text(
        valid_cross_fam_text
    )
    if valid_cross_fam_failures:
        failures.append(
            "Valid cross-FAM dependency candidate fixture unexpectedly failed: "
            + "; ".join(valid_cross_fam_failures[:5])
        )

    for documented_scope_class in (
        "Awareness Only",
        "Compatibility Default",
        "Future Adoption",
    ):
        documented_scope_text = re.sub(
            r"Dependency Scope Class: .+",
            f"Dependency Scope Class: {documented_scope_class}",
            valid_cross_fam_text,
        )
        documented_scope_failures = _validate_cross_fam_dependency_packet_text(
            documented_scope_text
        )
        if documented_scope_failures:
            failures.append(
                "Documented cross-FAM dependency scope class unexpectedly failed "
                f"({documented_scope_class}): "
                + "; ".join(documented_scope_failures[:5])
            )

    invalid_cross_fam_failures = _validate_cross_fam_dependency_packet_text(
        INVALID_CROSS_FAM_DEPENDENCY_UNCLASSIFIED_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_CROSS_FAM_UNCLASSIFIED_FAILURE_SNIPPET not in "\n".join(
        invalid_cross_fam_failures
    ):
        failures.append(
            "Invalid cross-FAM dependency fixture did not reject unclassified "
            "affected-FAM dependency work"
        )

    invalid_cross_fam_text = INVALID_CROSS_FAM_DEPENDENCY_UNCLASSIFIED_FIXTURE.read_text(
        encoding="utf-8"
    )
    mixed_cross_fam_failures = _validate_cross_fam_dependency_packet_text(
        invalid_cross_fam_text + "\n\n" + valid_cross_fam_text
    )
    if EXPECTED_CROSS_FAM_UNCLASSIFIED_FAILURE_SNIPPET not in "\n".join(
        mixed_cross_fam_failures
    ):
        failures.append(
            "Mixed cross-FAM dependency fixture did not reject an invalid record "
            "before a valid record"
        )

    bulleted_mixed_cross_fam_failures = _validate_cross_fam_dependency_packet_text(
        invalid_cross_fam_text.replace(
            "Cross-FAM Dependency Map:", "- Cross-FAM Dependency Map:"
        )
        + "\n\n"
        + valid_cross_fam_text.replace(
            "Cross-FAM Dependency Map:", "- Cross-FAM Dependency Map:"
        )
    )
    if EXPECTED_CROSS_FAM_UNCLASSIFIED_FAILURE_SNIPPET not in "\n".join(
        bulleted_mixed_cross_fam_failures
    ):
        failures.append(
            "Bulleted mixed cross-FAM dependency fixture did not reject an invalid "
            "record before a valid record"
        )

    compact_ffv_owner = _owning_fam_from_ffv(
        Path("Docs/family_feature_visions/F8-FF01.md"),
        "# FAM-008 Packaging Update Visibility\n\n"
        "Durable feature-category direction for packaging, update, and restart continuity.",
    )
    if compact_ffv_owner != "FAM-008":
        failures.append(
            "Compact Family Feature Vision filename fixture did not resolve owning FAM"
        )

    valid_ffv_failures = _validate_family_feature_vision_text(
        VALID_FAMILY_FEATURE_VISION_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_ffv_failures:
        failures.append(
            "Valid Family Feature Vision fixture unexpectedly failed: "
            + "; ".join(valid_ffv_failures[:5])
        )

    slice_scoped_ffv_failures = _validate_family_feature_vision_text(
        INVALID_FAMILY_FEATURE_VISION_SLICE_SCOPED_FIXTURE.read_text(encoding="utf-8")
    )
    if "Family Feature Vision Slice-Scoped" not in "\n".join(slice_scoped_ffv_failures):
        failures.append(
            "Invalid Family Feature Vision slice-scoped fixture did not reject "
            "Slice/SLC/branch-route feature identity"
        )

    live_state_ffv_failures = _validate_family_feature_vision_text(
        INVALID_FAMILY_FEATURE_VISION_LIVE_STATE_FIXTURE.read_text(encoding="utf-8")
    )
    if "FFV Live-State Leakage" not in "\n".join(live_state_ffv_failures):
        failures.append(
            "Invalid Family Feature Vision live-state fixture did not reject "
            "active branch-state wording in deferred carryforward"
        )

    valid_deferred_matrix_failures = _validate_br2_deferred_carryforward_matrix_text(
        VALID_BR2_DEFERRED_CARRYFORWARD_MATRIX_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_deferred_matrix_failures:
        failures.append(
            "Valid BR2 Deferred Carryforward matrix fixture unexpectedly failed: "
            + "; ".join(valid_deferred_matrix_failures[:5])
        )

    invalid_deferred_matrix_failures = _validate_br2_deferred_carryforward_matrix_text(
        INVALID_BR2_DEFERRED_CARRYFORWARD_MATRIX_FIXTURE.read_text(encoding="utf-8")
    )
    if "Deferred Carryforward Applicability Missing" not in "\n".join(
        invalid_deferred_matrix_failures
    ):
        failures.append(
            "Invalid BR2 Deferred Carryforward matrix fixture did not reject "
            "missing applicability/dependency/grouping proof"
        )

    valid_rar_failures = _validate_rebaseline_adoption_review_text(
        VALID_REBASELINE_ADOPTION_REVIEW_FIXTURE.read_text(encoding="utf-8")
    )
    if valid_rar_failures:
        failures.append(
            "Valid RAR adoption review fixture unexpectedly failed: "
            + "; ".join(valid_rar_failures[:5])
        )

    marker_only_rar_failures = _validate_rebaseline_adoption_review_text(
        INVALID_REBASELINE_ADOPTION_MARKER_ONLY_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_RAR_MARKER_ONLY_FAILURE_SNIPPET not in "\n".join(
        marker_only_rar_failures
    ):
        failures.append(
            "Invalid marker-only RAR fixture did not reject shallow adoption markers"
        )

    missing_code_trace_rar_failures = _validate_rebaseline_adoption_review_text(
        INVALID_REBASELINE_ADOPTION_MISSING_CODE_TRACE_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_RAR_CODE_TRACE_FAILURE_SNIPPET not in "\n".join(
        missing_code_trace_rar_failures
    ):
        failures.append(
            "Invalid RAR fixture did not reject missing code-to-visual trace"
        )

    unresolved_green_rar_failures = _validate_rebaseline_adoption_review_text(
        INVALID_REBASELINE_ADOPTION_UNRESOLVED_GREEN_FIXTURE.read_text(encoding="utf-8")
    )
    if EXPECTED_RAR_UNRESOLVED_GREEN_FAILURE_SNIPPET not in "\n".join(
        unresolved_green_rar_failures
    ):
        failures.append(
            "Invalid RAR fixture did not reject unresolved nonconformance claimed green"
        )

    missing_issue_candidate_rar_failures = _validate_rebaseline_adoption_review_text(
        INVALID_REBASELINE_ADOPTION_MISSING_ISSUE_CANDIDATE_FIXTURE.read_text(
            encoding="utf-8"
        )
    )
    if EXPECTED_RAR_ISSUE_CANDIDATE_FAILURE_SNIPPET not in "\n".join(
        missing_issue_candidate_rar_failures
    ):
        failures.append(
            "Invalid RAR fixture did not reject missing historical issue candidate disposition"
        )

    failures.extend(_validate_family_feature_vision_scaffolding_source_truth())
    failures.extend(_validate_current_worktree_family_feature_vision_files())
    failures.extend(_validate_current_worktree_ffv_dependency_records())

    failures.extend(_validate_merge_stable_projection_helpers())

    failures.extend(_validate_rebaseline_overlap_helper_matrix())

    failures.extend(_validate_user_review_bundle_identity_guard())
    failures.extend(_validate_workstream_entry_packet_existing_bp1_substance_guard())
    failures.extend(_validate_user_review_bundle_export_zip_identity_guard())
    failures.extend(_validate_user_review_bundle_export_zip_cleanup_guard())
    failures.extend(_validate_local_user_packet_folder_zip_guard())
    failures.extend(_validate_active_overlay_user_branch_plan_review_metadata_guard())
    failures.extend(_validate_fam007_workstream_approval_packet_metadata_guard())
    failures.extend(_validate_fam007_bp3_packet_generation_guard())
    failures.extend(_validate_fam007_workstream_implementation_packet_priority_guard())

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
