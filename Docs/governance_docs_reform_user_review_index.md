# Nexus Docs Reform User Review Index

## Start Here

This is the short review index for the full Docs source-truth reform. Use it to decide whether the long dossier is ready for PR Readiness, or whether specific files need more cleanup first.

## Review Proof

- Full dossier: `Docs/governance_docs_full_inventory_reform_audit.md`
- Docs files covered: 137
- Generated from Governance HEAD: `ff96f2c7451733e01770d755c0da70de47a40708`
- origin/main at generation: `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`
- merge base at generation: `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`
- Runtime/FAM/Compact-AI mutation: none.
- PR Readiness: held until USER review accepts this packet.

## Suggested Review Order

1. Read `Executive Summary` and `How To Review This Dossier` in the full dossier.
2. Review `What Was Completed`, `What Remains Deferred`, and `What Requires USER Decision`.
3. Review the `Completed / Deferred Matrix` for the reform scope.
4. Scan `High-Risk Files`, `Files Needing Future Migration`, and `Files That May Be Retired Later`.
5. Use the `File-by-File Review Table` for a compact pass over every Docs file.
6. Use the detailed `File-By-File Review Dossier` only for files you want to inspect deeply.
7. Confirm the `PR Readiness Checklist` before approving PR creation.

## Decision Checklist

- [ ] The source-truth ownership split is acceptable.
- [ ] Backlog and roadmap roles are acceptable.
- [ ] Branch Runtime Engineering Plan lifecycle and deletion rule are acceptable.
- [ ] Deferred deletion/fold-down candidates should remain deferred for now.
- [ ] No additional Docs file needs immediate retirement before PR Readiness.
- [ ] Validators are enough to stop the worst sprawl from returning.
- [ ] PR Readiness Stage 2 may proceed after final validation.

## Files Needing USER Decision

| File | Reason | Recommendation |
| --- | --- | --- |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | branch plan should be deleted after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted in this pass |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | branch plan should be deleted after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted in this pass |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | branch plan should be deleted after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted in this pass |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | branch plan should be deleted after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted in this pass |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | branch plan should be deleted after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted in this pass |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md` | branch plan should be deleted after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted in this pass |

## High-Risk Review Queue

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/feature_backlog.md` | compact product registry | Keep compact | Critical |
| `Docs/prebeta_roadmap.md` | release sequencing posture | Keep compact | Critical |
| `Docs/Main.md` | recovery map / source-truth router | Keep | High |
| `Docs/branch_records/codex_fb_037_release_debt_packaging.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/codex_one_time_backlog_governance_repair.md` | branch authority / compact receipt | Keep historical receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_pr112_source_truth_closeout.md` | branch authority / compact receipt | Keep historical receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md` | branch authority / compact receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_automation_planning.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md` | branch authority / compact receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_release_support.md` | branch authority / compact receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md` | branch authority / compact receipt | Migrate / compact receipt | High |

## Future Migration Queue

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | branch runtime engineering plan | Fold-down then delete candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | branch runtime engineering plan | Fold-down then delete candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | branch runtime engineering plan | Fold-down then delete candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | branch runtime engineering plan | Fold-down then delete candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | branch runtime engineering plan | Fold-down then delete candidate | Medium |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md` | branch runtime engineering plan | Fold-down then delete candidate | Medium |
| `Docs/branch_records/codex_fb_037_release_debt_packaging.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_automation_planning.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_readiness.md` | branch authority / compact receipt | Migrate / compact receipt | High |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md` | branch authority / compact receipt | Migrate / compact receipt | High |

## Safe To Leave For Now

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/boot_access_design.md` | product / architecture reference | Keep | Low |
| `Docs/closeout_index.md` | release closeout receipt | Keep | Low |
| `Docs/closeouts/v1.6.0_closeout.md` | release closeout receipt | Keep | Low |
| `Docs/closeouts/v1.9.0_closeout.md` | release closeout receipt | Keep | Low |
| `Docs/closeouts/v2.0_closeout.md` | release closeout receipt | Keep | Low |
| `Docs/orin_display_naming_guidance.md` | product / architecture reference | Keep | Low |
| `Docs/orin_vision.md` | product / architecture reference | Keep | Low |
| `Docs/workspace_layout_plan.md` | product / architecture reference | Keep | Low |
| `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md` | workstream durable history | Keep / normalize durable history | Low |
| `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md` | workstream durable history | Keep / normalize durable history | Low |
| `Docs/workstreams/FB-034_recoverable_diagnostics.md` | workstream durable history | Keep / normalize durable history | Low |

## Exact USER Decision This Index Supports

`I accept the Docs reform review surface and approve PR Readiness Stage 2 / PR creation for feature/release-readiness-source-truth-intake targeting main. Merge, release work, runtime work, FAM-006/FAM-007/Compact-AI mutation, issue work, branch cleanup, historical branch deletion, and successor branch creation remain separate decisions.`
