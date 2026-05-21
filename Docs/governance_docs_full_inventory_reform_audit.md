# Governance Docs Full Inventory Reform Audit

## Audit Identity

- Audit Type: Full `Docs/` source-truth inventory and restructuring assessment.
- Audit Workspace: `C:\Nexus Worktrees\Governance`
- Audit Branch: `feature/release-readiness-source-truth-intake`
- Audit Base: `origin/main` / `HEAD` at `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`
- Audit File Count: 136 files under `Docs/`
- Mutation Scope: planning and audit record only.
- Runtime Mutation: none.
- FAM-006 / FAM-007 / Compact-AI Mutation: none.
- Release / Tag / GitHub Release / Issue Work: none.

## Audit Purpose

This audit exists because the previous governance-efficiency reform defined the right ownership model but did not migrate enough existing source truth out of duplicate live-state surfaces. The current repository still repeats active branch, current phase, release window, worktree, package/slice, and next-legal-phase information across multiple docs.

The goal of the restructuring pass is to make each file prove its relevance, reduce drift and token load, route detailed history to the right long-term owner, and move live operational facts to Git/GitHub/helper-derived truth wherever source truth does not need to manually record them.

## Method

Every file under `Docs/` was read and scanned line by line for headings, current-state markers, Git/GitHub operational markers, package/slice/trace markers, phase markers, worktree markers, validator/helper markers, file size, inferred ownership role, reform action, and drift risk.

Marker counts are evidence, not final judgment. Some historical receipts may legitimately contain old PR/release language. The reform target is not to erase history; it is to stop multiple current-state owners from carrying the same live truth.

## Risk Summary

| Risk | File Count |
| --- | ---: |
| Critical | 2 |
| High | 39 |
| Medium | 64 |
| Low | 31 |

## Source-Truth Ownership Target

| Fact Class | Target Owner | Must Not Be Repeated As Current Truth In |
| --- | --- | --- |
| Live HEAD, branch state, dirty state, ahead/behind, merge base | Git helpers / preflight output | Backlog, roadmap, branch records, worktree slots |
| Live PR state, review state, mergeability | GitHub helper / PR watcher output | Backlog, roadmap, branch records except bounded PR receipt |
| Latest tag / latest GitHub Release | GitHub Releases / tag helpers | Backlog and roadmap current-state prose |
| Feature family identity, priority, broad status, compact scope | `Docs/feature_backlog.md` | Workstream docs as duplicated registry |
| Package and slice trace detail | `Docs/workstreams/` family dossiers | `Docs/feature_backlog.md` |
| Release sequencing and public milestone plan | `Docs/prebeta_roadmap.md` if retained | Branch records and backlog current-state blocks |
| Active branch legal authority | active branch authority record / `Docs/branch_records/index.md` | Backlog, roadmap, worktree slots |
| Active branch detailed plan | `Docs/branch_plans/<branch>.md` | Backlog, roadmap, branch authority record |
| Durable implementation history | `Docs/workstreams/<id>.md` or family dossier | Backlog, roadmap, worktree slots |
| Worktree slot definition and intended assignment receipt | `Docs/worktree_slots.md` | Backlog, roadmap, branch records |
| Normative phase rules | `Docs/phase_governance.md` | Main, user guide, codex modes, task template, development rules |
| Operator/user explanation of governance | `Docs/codex_user_guide.md` | Phase-rule owner files |
| Prompt packet templates | `Docs/orin_task_template.md` | Phase-rule owner files |

## Critical Findings

1. `Docs/feature_backlog.md` is still a live-state and history ledger, not a compact registry. It carries `Package Trace`, `Slice Trace`, release-window posture, branch history, issue posture, current branch posture, and next legal phase.
2. `Docs/prebeta_roadmap.md` duplicates the backlog current-decision pattern. This creates two mandatory current-state edits for the same event.
3. `Docs/worktree_slots.md` correctly says it must not own live truth, but it still includes branch-specific historical assignment narration that belongs in compact slot receipts or branch records.
4. Many historical branch records are no longer compact branch receipts. They are execution diaries with hundreds or thousands of lines.
5. `Docs/Main.md`, `Docs/phase_governance.md`, `Docs/development_rules.md`, `Docs/codex_modes.md`, `Docs/orin_task_template.md`, and `Docs/codex_user_guide.md` repeat phase governance in multiple voices.
6. The existing governance-efficiency validator passes despite this drift because it checks exact forbidden phrases, not the repeated-source-truth pattern.

## Complete File Inventory And Reform Classification

Legend: `H` = heading count, `Live` = current/live-state marker count, `Git` = Git/GitHub operational marker count, `Trace` = package/slice/branch/worktree trace marker count, `Phase` = phase lifecycle marker count, `WT` = worktree marker count, `Val` = validator/helper marker count.

| File | Lines | KB | H | Live | Git | Trace | Phase | WT | Val | Current Role | Reform Action | Risk |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `Docs/architecture.md` | 164 | 5.0 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/boot_access_design.md` | 165 | 4.9 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | 83 | 14.1 | 3 | 4 | 12 | 0 | 39 | 3 | 41 | Branch runtime engineering plan | Keep while active/historical folded; migrate retained lessons to workstream/dossier at PR closeout | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | 78 | 15.1 | 2 | 5 | 5 | 0 | 48 | 3 | 33 | Branch runtime engineering plan | Keep while active/historical folded; migrate retained lessons to workstream/dossier at PR closeout | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | 81 | 14.0 | 2 | 6 | 4 | 0 | 37 | 4 | 43 | Branch runtime engineering plan | Keep while active/historical folded; migrate retained lessons to workstream/dossier at PR closeout | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | 249 | 24.2 | 24 | 7 | 26 | 0 | 69 | 13 | 64 | Branch runtime engineering plan | Keep while active/historical folded; migrate retained lessons to workstream/dossier at PR closeout | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | 159 | 18.0 | 15 | 7 | 6 | 0 | 57 | 12 | 59 | Branch runtime engineering plan | Keep while active/historical folded; migrate retained lessons to workstream/dossier at PR closeout | Medium |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md` | 89 | 11.6 | 3 | 4 | 12 | 0 | 31 | 9 | 59 | Branch runtime engineering plan | Keep while active/historical folded; migrate retained lessons to workstream/dossier at PR closeout | Medium |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption_inventory.md` | 45 | 5.4 | 3 | 0 | 0 | 0 | 0 | 5 | 39 | Branch plan inventory | Keep while branch receipt needs inventory; fold into relevant dossier later | Medium |
| `Docs/branch_plans/README.md` | 71 | 3.8 | 5 | 3 | 0 | 0 | 19 | 2 | 7 | Branch plan standard | Keep; strengthen lifecycle and fold-down rules | Medium |
| `Docs/branch_records/codex_fam_007_branch_readiness.md` | 187 | 13.5 | 24 | 14 | 10 | 0 | 32 | 20 | 29 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/codex_fb_037_release_debt_packaging.md` | 425 | 21.8 | 30 | 19 | 10 | 0 | 74 | 0 | 38 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/codex_no_active_branch_docs_governance_refinement.md` | 83 | 3.4 | 14 | 10 | 1 | 0 | 4 | 0 | 3 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/codex_one_time_backlog_governance_repair.md` | 223 | 20.4 | 24 | 14 | 29 | 2 | 56 | 0 | 32 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | 435 | 38.7 | 36 | 25 | 60 | 0 | 175 | 0 | 39 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_release_canon_closure.md` | 278 | 22.6 | 26 | 39 | 22 | 0 | 83 | 0 | 29 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_pr112_source_truth_closeout.md` | 296 | 22.8 | 29 | 31 | 56 | 0 | 82 | 0 | 30 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md` | 320 | 21.2 | 32 | 32 | 44 | 0 | 46 | 0 | 48 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/codex_workspace_governance_foundation.md` | 194 | 11.9 | 23 | 12 | 9 | 0 | 40 | 39 | 14 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_automation_planning.md` | 417 | 29.8 | 33 | 27 | 11 | 0 | 89 | 0 | 45 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_automation_planning_post_merge_canon_repair.md` | 144 | 8.1 | 20 | 25 | 12 | 0 | 14 | 0 | 5 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md` | 204 | 15.3 | 27 | 37 | 21 | 0 | 29 | 0 | 13 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | 411 | 37.5 | 42 | 34 | 12 | 0 | 146 | 0 | 90 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md` | 542 | 50.7 | 43 | 21 | 75 | 0 | 88 | 66 | 83 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_dashboard_release_support.md` | 188 | 12.5 | 24 | 14 | 61 | 0 | 21 | 1 | 9 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md` | 614 | 48.5 | 41 | 26 | 63 | 0 | 119 | 64 | 121 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md` | 698 | 82.2 | 49 | 46 | 119 | 0 | 116 | 55 | 229 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_issue_readiness_governance_repair.md` | 245 | 18.4 | 29 | 9 | 15 | 0 | 26 | 2 | 11 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md` | 1000 | 150.1 | 60 | 32 | 94 | 0 | 217 | 115 | 301 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md` | 2563 | 438.9 | 136 | 19 | 86 | 1 | 1004 | 54 | 1009 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md` | 202 | 110.0 | 12 | 0 | 12 | 2 | 140 | 16 | 272 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md` | 503 | 43.6 | 48 | 30 | 68 | 0 | 84 | 34 | 153 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_readiness.md` | 416 | 30.9 | 34 | 12 | 17 | 0 | 40 | 10 | 40 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md` | 452 | 41.3 | 35 | 10 | 69 | 0 | 95 | 32 | 82 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md` | 502 | 63.8 | 42 | 43 | 42 | 0 | 163 | 29 | 106 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | 548 | 74.2 | 45 | 43 | 62 | 0 | 161 | 34 | 152 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | 489 | 77.4 | 41 | 45 | 91 | 0 | 163 | 37 | 118 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md` | 477 | 59.1 | 41 | 31 | 84 | 0 | 170 | 20 | 130 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | 675 | 63.6 | 47 | 38 | 56 | 0 | 165 | 25 | 128 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | 610 | 54.1 | 50 | 29 | 64 | 0 | 152 | 39 | 103 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | 578 | 48.8 | 43 | 30 | 29 | 0 | 133 | 19 | 118 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_runtime_expansion.md` | 489 | 45.3 | 35 | 14 | 68 | 0 | 130 | 40 | 87 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md` | 516 | 44.7 | 36 | 27 | 80 | 0 | 161 | 43 | 72 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_provider_boundary_no_provider_shell.md` | 530 | 60.2 | 34 | 21 | 55 | 0 | 139 | 30 | 121 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fam_007_runtime_provider_boundary.md` | 216 | 18.6 | 25 | 12 | 29 | 0 | 56 | 11 | 29 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fam_007_stage_2_readiness_admission.md` | 296 | 27.3 | 31 | 24 | 40 | 0 | 65 | 10 | 30 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_fb_005_workspace_path_planning.md` | 57 | 2.6 | 11 | 4 | 0 | 0 | 9 | 0 | 1 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_030_orin_voice_audio_direction_refinement.md` | 63 | 3.2 | 11 | 8 | 3 | 0 | 12 | 0 | 0 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_030_release_readiness_canon_repair.md` | 62 | 2.9 | 11 | 9 | 2 | 0 | 5 | 0 | 5 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_030_successor_branch_truth_repair.md` | 65 | 3.2 | 11 | 11 | 5 | 0 | 5 | 0 | 2 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_042_desktop_entrypoint_runtime_refinement.md` | 58 | 2.9 | 11 | 3 | 0 | 0 | 15 | 0 | 3 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_043_top_level_entrypoint_handoff_refinement.md` | 230 | 15.3 | 26 | 16 | 1 | 0 | 32 | 0 | 26 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_044_boot_desktop_handoff_outcome_refinement.md` | 223 | 14.5 | 26 | 14 | 1 | 0 | 33 | 0 | 24 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_045_active_session_relaunch_stability.md` | 222 | 14.8 | 27 | 13 | 0 | 0 | 41 | 0 | 28 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_046_active_session_relaunch_reacquisition.md` | 217 | 13.5 | 26 | 14 | 0 | 0 | 40 | 0 | 21 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_047_active_session_relaunch_decline_preservation.md` | 218 | 13.9 | 26 | 14 | 0 | 0 | 41 | 0 | 22 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md` | 220 | 14.4 | 26 | 15 | 0 | 0 | 39 | 0 | 22 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_fb_049_runtime_branch_readiness.md` | 327 | 24.9 | 33 | 16 | 17 | 0 | 68 | 5 | 60 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_pr101_post_merge_closeout_canon_repair.md` | 149 | 9.1 | 20 | 25 | 23 | 0 | 16 | 0 | 7 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_pr102_post_merge_closeout_canon_repair.md` | 149 | 9.1 | 20 | 24 | 20 | 0 | 16 | 0 | 6 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_pr103_post_merge_closeout_canon_repair.md` | 242 | 16.6 | 30 | 27 | 33 | 0 | 22 | 4 | 24 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/feature_pr104_watcher_next_prompt_format_repair.md` | 164 | 10.4 | 20 | 19 | 22 | 0 | 15 | 0 | 16 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md` | 176 | 11.5 | 20 | 13 | 24 | 0 | 19 | 0 | 15 | Branch authority receipt | Compact as historical receipt; remove live state if branch is historical | Medium |
| `Docs/branch_records/feature_release_readiness_source_truth_intake.md` | 270 | 33.8 | 27 | 24 | 44 | 0 | 81 | 155 | 63 | Standing governance branch record | Keep active but compact cycle history; move old RRI detail to receipts/appendix | High |
| `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md` | 497 | 50.4 | 38 | 19 | 37 | 0 | 105 | 71 | 217 | Historical branch execution diary | Fold down to compact receipt; migrate durable detail to workstream/family dossier; archive raw diary if needed | High |
| `Docs/branch_records/index.md` | 175 | 40.7 | 5 | 36 | 21 | 0 | 99 | 89 | 36 | Branch authority router | Keep but shrink rules; point to phase/worktree/governance owners | High |
| `Docs/closeout_guidance.md` | 106 | 6.0 | 9 | 2 | 4 | 0 | 17 | 0 | 7 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeout_index.md` | 70 | 1.5 | 12 | 0 | 0 | 0 | 0 | 0 | 2 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.2.7-prebeta.md` | 79 | 3.1 | 9 | 1 | 0 | 0 | 11 | 0 | 0 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.2.8-prebeta.md` | 83 | 3.4 | 9 | 1 | 0 | 0 | 12 | 0 | 1 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.2.9-prebeta.md` | 88 | 3.8 | 9 | 1 | 0 | 0 | 12 | 0 | 2 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.3.0-prebeta.md` | 100 | 4.6 | 9 | 1 | 0 | 0 | 13 | 0 | 2 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.3.1-prebeta.md` | 115 | 5.5 | 9 | 1 | 0 | 0 | 15 | 0 | 2 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md` | 108 | 4.3 | 10 | 0 | 0 | 0 | 16 | 0 | 4 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v1.6.0_closeout.md` | 120 | 2.4 | 16 | 0 | 0 | 0 | 0 | 0 | 1 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v1.7.0_closeout.md` | 130 | 4.0 | 16 | 0 | 0 | 0 | 2 | 0 | 2 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v1.8.0_closeout.md` | 141 | 5.6 | 16 | 0 | 0 | 0 | 0 | 0 | 5 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v1.9.0_closeout.md` | 167 | 7.4 | 17 | 0 | 0 | 0 | 1 | 0 | 40 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v2.0_closeout.md` | 197 | 7.9 | 18 | 0 | 0 | 0 | 1 | 0 | 6 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v2.2.0_closeout.md` | 131 | 5.3 | 14 | 0 | 0 | 0 | 0 | 0 | 13 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/closeouts/v2.2.1_closeout.md` | 106 | 4.1 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | Release/epoch closeout receipt | Keep as historical receipt; derive current release state from GitHub | Low |
| `Docs/codex_modes.md` | 782 | 90.2 | 48 | 70 | 34 | 0 | 285 | 77 | 160 | Codex behavior/mode guide | Shrink to mode behavior and pointers; no branch/release truth | High |
| `Docs/codex_user_guide.md` | 844 | 82.0 | 47 | 58 | 35 | 0 | 233 | 68 | 118 | Human operator guide | Shrink to explanatory guide; no machine-state authority | High |
| `Docs/development_rules.md` | 1055 | 123.1 | 25 | 84 | 48 | 0 | 361 | 137 | 236 | Developer execution mirror | Shrink to dev-facing checklist and pointers to phase owner | High |
| `Docs/fb_027_overlay_bug_tracker.md` | 211 | 7.8 | 16 | 1 | 0 | 0 | 1 | 0 | 9 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/feature_backlog.md` | 1540 | 191.0 | 73 | 111 | 311 | 23 | 436 | 26 | 181 | Feature family registry | Major compaction: registry/status/pointers only; migrate package/slice/history/release/current-state detail | Critical |
| `Docs/governance_docs_full_inventory_reform_audit.md` | 531 | 43.6 | 36 | 17 | 11 | 16 | 94 | 31 | 36 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/governance_efficiency_operating_model.md` | 224 | 10.6 | 18 | 6 | 7 | 0 | 23 | 6 | 31 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/governance_intake_triage_and_digest_profiles.md` | 162 | 5.8 | 14 | 8 | 2 | 0 | 10 | 6 | 17 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/governance_process_efficiency_reform_plan.md` | 488 | 23.1 | 25 | 20 | 11 | 0 | 27 | 33 | 90 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/incident_patterns.md` | 342 | 27.0 | 21 | 30 | 9 | 0 | 77 | 12 | 128 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/Main.md` | 587 | 96.0 | 23 | 60 | 40 | 0 | 342 | 137 | 156 | Core governance map | Keep but shrink to recovery/source-truth map; point to owners instead of replaying rules | High |
| `Docs/ncp_hardening_assessment.md` | 108 | 4.4 | 9 | 0 | 0 | 0 | 16 | 0 | 2 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/nexus_startup_contract.md` | 631 | 55.0 | 20 | 34 | 9 | 0 | 194 | 18 | 78 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/orchestration.md` | 126 | 3.3 | 13 | 0 | 0 | 0 | 2 | 0 | 0 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/orin_display_naming_guidance.md` | 124 | 3.9 | 11 | 0 | 0 | 0 | 4 | 0 | 1 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/orin_interaction_architecture.md` | 267 | 10.7 | 22 | 0 | 0 | 0 | 3 | 0 | 2 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/orin_task_template.md` | 1029 | 83.3 | 44 | 59 | 31 | 0 | 244 | 89 | 142 | Prompt/template owner | Shrink to reusable packet templates; no live-state facts | High |
| `Docs/orin_vision.md` | 220 | 10.6 | 21 | 1 | 0 | 0 | 6 | 0 | 4 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/ownership_ip_plan.md` | 111 | 4.4 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/phase_governance.md` | 2548 | 215.1 | 105 | 179 | 89 | 2 | 734 | 192 | 391 | Normative phase governance owner | Keep as phase owner; remove duplicated operator/user-guide prose; split appendices if needed | High |
| `Docs/pr_watcher_mode_contract.md` | 82 | 5.2 | 8 | 0 | 3 | 0 | 4 | 8 | 1 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/prebeta_roadmap.md` | 723 | 90.6 | 51 | 106 | 201 | 2 | 256 | 15 | 65 | Release sequencing layer | Major compaction or retirement: sequencing only; derive live release truth from GitHub | Critical |
| `Docs/user_test_summary_guidance.md` | 333 | 18.8 | 17 | 2 | 0 | 0 | 69 | 0 | 83 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/validation_helper_registry.md` | 211 | 49.8 | 18 | 8 | 20 | 0 | 90 | 78 | 300 | Governance support standard/registry | Keep but enforce one owner per rule and compact mirrors elsewhere | Medium |
| `Docs/workspace_layout_plan.md` | 167 | 4.3 | 10 | 0 | 0 | 0 | 1 | 0 | 7 | Product/architecture/reference doc | Keep if referenced; otherwise archive after pointer audit | Low |
| `Docs/workstreams/FB-004_future_boot_orchestrator_layer.md` | 740 | 64.3 | 69 | 21 | 10 | 0 | 145 | 0 | 202 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-005_workspace_and_folder_organization.md` | 407 | 34.2 | 52 | 34 | 8 | 0 | 91 | 0 | 67 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md` | 740 | 68.5 | 69 | 43 | 14 | 0 | 158 | 0 | 180 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md` | 85 | 2.3 | 19 | 0 | 0 | 0 | 0 | 0 | 2 | Canonical workstream record | Keep if referenced by index; otherwise archive/merge into family dossier | Low |
| `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | 125 | 12.1 | 13 | 0 | 9 | 4 | 38 | 0 | 35 | Family dossier | Keep/promote as destination for backlog trace migration | Medium |
| `Docs/workstreams/FB-027_interaction_system_baseline.md` | 750 | 43.9 | 74 | 16 | 35 | 0 | 62 | 0 | 74 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-028_history_state_relocation.md` | 88 | 2.6 | 19 | 0 | 0 | 0 | 0 | 0 | 2 | Canonical workstream record | Keep if referenced by index; otherwise archive/merge into family dossier | Low |
| `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md` | 527 | 49.3 | 62 | 37 | 11 | 0 | 131 | 0 | 113 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md` | 1009 | 90.1 | 94 | 68 | 42 | 0 | 207 | 0 | 203 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md` | 500 | 44.0 | 53 | 36 | 5 | 0 | 113 | 0 | 141 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md` | 549 | 55.1 | 57 | 29 | 20 | 0 | 133 | 0 | 163 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md` | 89 | 2.5 | 19 | 0 | 0 | 0 | 0 | 0 | 6 | Canonical workstream record | Keep if referenced by index; otherwise archive/merge into family dossier | Low |
| `Docs/workstreams/FB-034_recoverable_diagnostics.md` | 96 | 3.0 | 19 | 0 | 0 | 0 | 1 | 0 | 3 | Canonical workstream record | Keep if referenced by index; otherwise archive/merge into family dossier | Low |
| `Docs/workstreams/FB-035_release_context_fallback_hardening.md` | 99 | 3.6 | 19 | 2 | 0 | 0 | 4 | 0 | 7 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-036_saved_action_authoring.md` | 847 | 66.4 | 46 | 1 | 0 | 0 | 40 | 0 | 123 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md` | 423 | 30.9 | 28 | 7 | 1 | 0 | 108 | 0 | 184 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md` | 924 | 71.0 | 39 | 19 | 4 | 0 | 212 | 3 | 295 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md` | 1888 | 153.2 | 137 | 27 | 14 | 0 | 221 | 0 | 540 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md` | 617 | 49.4 | 67 | 32 | 2 | 0 | 85 | 0 | 117 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md` | 273 | 13.4 | 23 | 2 | 0 | 0 | 13 | 0 | 26 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md` | 412 | 33.3 | 50 | 35 | 7 | 0 | 86 | 0 | 92 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | 128 | 11.8 | 13 | 0 | 0 | 4 | 32 | 0 | 28 | Family dossier | Keep/promote as destination for backlog trace migration | Medium |
| `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md` | 478 | 35.2 | 54 | 30 | 7 | 0 | 64 | 0 | 106 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md` | 419 | 30.6 | 52 | 35 | 7 | 0 | 65 | 0 | 83 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md` | 443 | 32.3 | 53 | 38 | 7 | 0 | 50 | 0 | 92 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md` | 413 | 30.8 | 52 | 35 | 7 | 0 | 49 | 0 | 80 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md` | 419 | 31.1 | 52 | 33 | 7 | 0 | 53 | 0 | 87 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md` | 492 | 39.7 | 60 | 43 | 25 | 0 | 67 | 0 | 102 | Canonical workstream record | Keep as durable implementation/history owner; strip live phase if historical | Medium |
| `Docs/workstreams/index.md` | 195 | 17.0 | 16 | 8 | 3 | 0 | 102 | 0 | 45 | Workstream/dossier router | Keep; make it canonical pointer index for detailed history | Medium |
| `Docs/worktree_slots.md` | 294 | 16.5 | 20 | 2 | 16 | 0 | 33 | 90 | 16 | Worktree slot assignment receipts | Shrink to slot definitions/current intended assignments; move history to receipts | High |

## File Group Reform Plan

### 1. Core Governance Files

Files: `Docs/Main.md`, `Docs/phase_governance.md`, `Docs/development_rules.md`, `Docs/codex_modes.md`, `Docs/orin_task_template.md`, `Docs/codex_user_guide.md`, and `Docs/nexus_startup_contract.md`.

Finding: these files overlap heavily on phase names, phase order, Branch Readiness, PR Readiness, Release Readiness, worktree identity, watcher behavior, durable commit/push rules, and next-legal-phase packet rules.

Plan: make `Docs/phase_governance.md` the only normative phase-rule owner; make `Docs/Main.md` the recovery map and source-truth ownership map; shrink the rest into pointer-based mirrors, templates, or human guides.

### 2. Backlog

File: `Docs/feature_backlog.md`.

Finding: the backlog owns too much. It should not own release candidate anchors, latest public release status, detailed branch history, issue receipts, `Package Trace`, `Slice Trace`, worktree history, or next-legal-phase instructions.

Plan: keep FAM ID, title, priority, status, record state, family scope, compact package status, and active/detail pointers. Move package/slice detail to family dossiers under `Docs/workstreams/`.

### 3. Roadmap

File: `Docs/prebeta_roadmap.md`.

Finding: the roadmap duplicates backlog current-state and release posture.

Plan: decide whether to retain it as a release sequencing index. If retained, it may own planned release cadence and public milestone posture only. Latest public release, tag, PR state, merge commits, and release URLs should be derived from GitHub.

### 4. Branch Records

Files: 56 files under `Docs/branch_records/`.

Finding: many historical branch records are execution diaries.

Plan: active branch records own legal authority, phase, approvals, blockers, allowed scope, and next phase. Historical branch records become compact receipts. Durable implementation detail migrates to workstream/family dossiers.

### 5. Branch Plans

Files: 9 files under `Docs/branch_plans/`.

Finding: this layer is conceptually correct. It should own active branch planning and plan-to-implementation traceability, then fold down during PR Readiness.

Plan: keep active branch plans while branch is active. At PR Readiness, produce a fold-down decision: compact historical branch receipt, durable lessons promoted to workstream/family dossier, and raw planning retired or archived only if still needed.

### 6. Workstreams And Family Dossiers

Files: 29 files under `Docs/workstreams/`.

Finding: this is the correct home for durable detail, but many workstreams still carry historical live-state markers. Existing family dossiers are a good direction and should become the target for package/slice trace migrated out of backlog.

Plan: make workstream/family dossier files the durable history owners. Strip or label old live phase markers as historical. Create or expand family dossiers for FAM-006 and FAM-007.

### 7. Worktree Slots

File: `Docs/worktree_slots.md`.

Finding: the slot model is right, but the file still records too much branch-specific history.

Plan: keep stable slot definitions and current intended assignment only. Move retired assignment history to compact slot retirement receipts or branch records. Keep live worktree state derived from Git and helpers.

### 8. Closeouts

Files: `Docs/closeout_guidance.md`, `Docs/closeout_index.md`, and 13 files under `Docs/closeouts/`.

Finding: closeouts are mostly healthy historical receipts.

Plan: keep them as durable historical summaries, but derive current release truth from GitHub/tags.

### 9. Product / Architecture Reference Docs

Files include architecture, boot access, ORIN vision, interaction architecture, ownership/IP, workspace layout, and related reference docs.

Finding: these are generally low-risk, but they need a pointer audit.

Plan: keep if referenced by Main, backlog, roadmap, workstreams, validators, or source-owner markers. Archive or fold into product dossiers if unreferenced.

### 10. Governance Support Standards

Files include governance efficiency, governance intake profiles, incident patterns, watcher mode contract, User Test Summary guidance, and validation helper registry.

Finding: useful, but some are descriptive rather than enforceable.

Plan: keep as standards/registries, add one-owner-per-rule IDs, and add hard validators for duplicate current-state ownership and forbidden backlog/roadmap sprawl.

## GitHub / Helper Derived Truth Plan

The following should not be maintained manually as active source truth: latest public prerelease, latest GitHub Release URL, current tag existence, current release target commit, open PR state, merged/closed PR state, PR review state, branch ahead/behind state, worktree dirty state, merge base, and remote branch existence.

These should come from `git rev-parse`, `git merge-base`, `git status --short --branch`, `git worktree list --porcelain`, `git branch --merged origin/main`, `gh pr view`, GitHub GraphQL, `gh release view`, `git ls-remote --tags`, or repo helper wrappers that produce stable digest output.

Docs may record historical receipts after validation, but they should not be the first source for live operational truth.

## Repetitive Record Classes To Eliminate

- Duplicate current decision surfaces.
- `Package Trace` / `Slice Trace` in backlog.
- Long branch history lists in backlog.
- Release-window narration in both backlog and roadmap.
- Phase rules repeated in guides/templates.
- Worktree assignment history inside the slot registry.
- Historical branch records retaining active-phase language.

## Validator Reform Requirements

Add or strengthen validators for: `Package Trace:` forbidden in `Docs/feature_backlog.md`; `Slice Trace:` forbidden in `Docs/feature_backlog.md`; exact commit hashes forbidden in backlog/roadmap current-state sections unless marked historical receipt; identical current-state lines duplicated between backlog and roadmap; latest public release/tag truth repeated in more than one active current-state owner; live branch/worktree paths in backlog/roadmap current-state blocks; branch history lists over a small threshold in backlog; roadmap carrying branch execution diary text; branch records above a size threshold requiring fold-down or explicit active status; historical branch records retaining live active-phase markers; `worktree_slots.md` carrying branch execution history instead of assignment receipts; Main/development/codex/user-guide/template files repeating full phase governance blocks instead of pointers.

## Recommended Reform Sequence

1. Reform PR 1: Audit and ownership lock.
2. Reform PR 2: Backlog compaction.
3. Reform PR 3: Roadmap redefinition.
4. Reform PR 4: Branch record fold-down.
5. Reform PR 5: Core governance deduplication.
6. Reform PR 6: Worktree slot cleanup.
7. Reform PR 7: Validator finalization.

## Immediate Recommended Next Legal Phase

Governance Reform Stage 2 should review this audit, accept or revise the ownership model, then begin Reform PR 1: Audit And Ownership Lock.

Runtime implementation, FAM-006 mutation, FAM-007 mutation, Compact-AI mutation, release execution, tag/GitHub Release work, issue work, branch cleanup, and successor branch creation remain blocked while this reform is in progress unless USER explicitly routes a separate lane.
