# Branch Authority Records Index
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=SHARED-DOCS; ledger=SRCOWN-FIRSTPASS-DOCS-011; surface=branch-record-index-owner; status=shared -->

## Purpose

Durable branch identity, product/interface intent and historical receipt pointers
belong here. Current phase, write scope, locks and assignment belong in the matching
external Governance State record. This index grants no live authority.

## Rules

- Follow `Docs/governance_efficiency_operating_model.md#source-truth-authority-hierarchy`.
  Operational Governance source uses an explicitly approved external carrier;
  product/interface changes use their approved repository carrier.
- Protected main and all existing USER changes/commits remain protected. New
  branches and consequential effects require the current explicit USER approval.
- Product branch planning, acceptance, release contracts and required public issue
  receipt fields remain with their product owners. Standard product tests remain.
- Historical standing-intake, relocation and repair exceptions explain prior
  transactions, not future prerequisites or alternate active policy.
- Derive Git facts from Git. A durable receipt is not active authority or proof of
  a current phase. Preserve historical receipts without rewriting them for a new
  source version. The external operational owner defines confinement and rollback.
- Commit, push, PR, merge, release, live activation and storage deletion are
  separately admitted effects. No rule here implies an unapproved effect.

## Durable Branch Issue Receipt Fields

Branch records may preserve issue evidence only as durable receipts after live GitHub truth is checked or the evidence source is named. They must not become live GitHub issue ledgers.

Use these field names when a branch needs durable issue traceability:

- `Carried GitHub Issues:`
- `Held GitHub Issues:`
- `Completed GitHub Issues:`
- `Issue Closeout Candidate Inventory:`
- `Issue Closeout Status:`
- `Issue Closeout Approval:`
- `Issue Closeout Receipt:`
- `Issue Evidence Source:`

Allowed `Issue Closeout Status:` values are `Not Applicable`, `Pending USER Approval`, `Approved For RR2`, `Closed In GitHub`, `Already Closed`, `Routed To Future Branch`, and `USER Decision Required`.

Historical branch records may name issue numbers, PRs, release tags, closeout approval, and evidence pointers when they are receipt facts. Current live issue state remains owned by GitHub, Git/GitHub connectors, helpers, Codex digests, USER review packets, or external operational state according to phase rules.

## Retained Standing-Intake Receipt

The following pointer preserves the former standing-intake receipt as historical routing evidence only. It grants no current authority. Current branch/worktree state is external; no standing-intake exception remains in this index.

- `Docs/branch_records/feature_release_readiness_source_truth_intake.md`

## Historical Branch Authority Records

- `Docs/branch_records/feature_governance_d_root_relocation_closure.md`
- `Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md`
- `Docs/branch_records/feature_fam_006_dashboard_overlay_profile_persistence_repair.md`
- `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
- `Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md`
- `Docs/branch_records/feature_fam_007_dev_owner_skeleton_readiness.md`
- `Docs/branch_records/feature_fam_007_ai_runtime_trust_boundary_readiness.md`
- `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md`
- `Docs/branch_records/feature_fam_007_v1_7_23_post_release_canon_closure.md`
- `Docs/branch_records/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md`
- `Docs/branch_records/feature_fam_007_ai_edition_public_leak_prevention_foundation.md`
- `Docs/branch_records/feature_fam_007_ai_edition_public_leak_prevention_foundation_post_merge_projection.md`
- `Docs/branch_records/feature_fam_006_v1_7_19_release_posture_carry_forward.md`
- `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_setup_completion_foundation.md`
- `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
- `Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_setup_implementation_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md`
- `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`
- `Docs/branch_records/feature_vision_update_decision_matrix.md`
- `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md`
- `Docs/branch_records/feature_fam_007_local_ai_runtime_expansion.md`
- `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md`
- `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md`
- `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md`
- `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md`
- `Docs/branch_records/feature_fam_007_provider_boundary_no_provider_shell.md`
- `Docs/branch_records/feature_fam_006_dashboard_release_support.md`
- `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md`
- `Docs/branch_records/feature_fam_007_runtime_provider_boundary.md`
- `Docs/branch_records/feature_fam_007_stage_2_readiness_admission.md`
- `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md`
- `Docs/branch_records/feature_fam_007_local_ai_foundation_readiness.md`
- `Docs/branch_records/feature_fam_006_issue_readiness_governance_repair.md`
- `Docs/branch_records/codex_workspace_governance_foundation.md`
- `Docs/branch_records/codex_fam_007_branch_readiness.md`
- `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md`
- `Docs/branch_records/codex_v1_6_13_prebeta_post_release_canon_closure.md`
- `Docs/branch_records/codex_v1_6_13_prebeta_pr112_source_truth_closeout.md`
- `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md`
- `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md`
- `Docs/branch_records/codex_one_time_backlog_governance_repair.md`
- `Docs/branch_records/feature_fb_049_runtime_branch_readiness.md`
- `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_pr104_watcher_next_prompt_format_repair.md`
- `Docs/branch_records/feature_pr103_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_pr102_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_pr101_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md`
- `Docs/branch_records/feature_automation_planning_post_merge_canon_repair.md`
- `Docs/branch_records/feature_automation_planning.md`
- `Docs/branch_records/feature_backlog_family_governance_reform.md`
- `Docs/branch_records/feature_fb_048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
- `Docs/branch_records/feature_fb_047_active_session_relaunch_decline_preservation.md`
- `Docs/branch_records/feature_fb_046_active_session_relaunch_reacquisition.md`
- `Docs/branch_records/feature_fb_045_active_session_relaunch_stability.md`
- `Docs/branch_records/feature_fb_044_boot_desktop_handoff_outcome_refinement.md`
- `Docs/branch_records/feature_fb_043_top_level_entrypoint_handoff_refinement.md`
- `Docs/branch_records/codex_fb_037_release_debt_packaging.md`
- `Docs/branch_records/codex_no_active_branch_docs_governance_refinement.md`
- `Docs/branch_records/feature_fb_042_desktop_entrypoint_runtime_refinement.md`
- `Docs/branch_records/feature_fb_005_workspace_path_planning.md`
- `Docs/branch_records/feature_fb_030_orin_voice_audio_direction_refinement.md`
- `Docs/branch_records/feature_fb_030_release_readiness_canon_repair.md`
- `Docs/branch_records/feature_fb_030_successor_branch_truth_repair.md`

## Durable Branch Receipt Records

- `Docs/branch_records/feature_fam_003_resident_access_quick_actions.md`
- `Docs/branch_records/feature_fam_007_ai_control_center_readiness_diagnostics.md`
- `Docs/branch_records/feature_fam_007_three_ndai_assisted_ai_function_slice.md`
- `Docs/branch_records/feature_fam_007_owner_ai_operational_foundation_gates.md`
- `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md` - Companion element-validation ledger owned by `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md`; preserved as released historical proof, not active branch authority.
- `Docs/branch_records/feature_governance_final_d_root_source_truth.md`
