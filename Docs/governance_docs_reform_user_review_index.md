# Nexus Docs Reform User Review Index

## Start Here

This is the short review index for the full Docs source-truth reform. Use it to decide whether the long dossier is ready for PR Readiness, or whether specific files need more cleanup first.

## Review Proof

- Full dossier: `Docs/governance_docs_full_inventory_reform_audit.md`
- Docs files covered: 194
- Source branch: `feature/release-readiness-source-truth-intake`
- Git proof: derive live `HEAD`, `origin/main`, and merge-base with git at review/validation time.
- Generated hash fields: intentionally not maintained in this docs review index.
- Runtime/FAM/Compact-AI mutation: none.
- PR Readiness: held until validation is green and USER separately approves PR creation.

## Suggested Review Order

1. Read `Executive Summary` and `How To Review This Dossier` in the full dossier.
2. Review `What Was Completed`, `What Remains External`, and `What Requires USER Decision`.
3. Review `USER Response Integration Matrix` and confirm each response changed the model.
4. Review `Single-PR Staged Execution Plan` before deciding whether PR Readiness should proceed.
5. Review the `Completed / External Decision Matrix` for the reform scope.
6. Review `Complete Docs Cleanup / Disposition Table` for every file's keep/organize/migrate/retire/delete posture.
7. Review ambiguity and structure queues before deciding whether cleanup is complete.
8. Scan `High-Risk Files`, `Files Needing Future Migration`, and `Files That May Be Retired Later`.
9. Use the `File-by-File Review Table` for a compact pass over every Docs file.
10. Use the detailed `File-By-File Review Dossier` only for files you want to inspect deeply.
11. Confirm the `PR Readiness Checklist` only after the staged cleanup is accepted.

## Decision Checklist

- [ ] The source-truth ownership split is acceptable.
- [ ] USER response requirements are integrated as model decisions, not just preserved as notes.
- [ ] Remaining reform work should stay on this single Governance branch/final PR path.
- [ ] Backlog and roadmap roles are acceptable.
- [ ] Branch Runtime Engineering Plan lifecycle and retirement rule are acceptable.
- [ ] Historical branch plans are acceptable as retired/indexed records rather than active execution plans.
- [ ] No Docs file should be deleted, archived, or broadly renamed before a later focused USER decision.
- [ ] Every Docs file has a clear disposition in the complete cleanup table.
- [ ] Ambiguous ownership/current-state wording has a clear owner or deferred review action.
- [ ] Structure risks have a migration, organization, or keep-now decision.
- [ ] Validators are enough to stop the worst sprawl from returning.
- [ ] PR Readiness Stage 1 analysis may proceed after final validation and USER acceptance; PR Readiness Stage 2 / PR creation remains a separate USER decision.

## User Response Intake Status

- USER review responses are recorded in `Docs/governance_process_efficiency_reform_plan.md` under the 2026-05-21 review intake.
- This generated index stays pointer-based so audit regeneration does not strand raw USER notes in a generated file.
- Current execution model: this deferred-completion pass updates source truth and review artifacts on the USER-approved bounded governance/source-truth repair branch `feature/release-readiness-source-truth-intake` in `C:\Nexus Worktrees\Governance`; PR creation remains separately USER-gated.
- PR Readiness remains held until validation is green and USER separately approves PR creation.

## USER Response Integration Summary

| USER Response Area | Model Decision | Execution Effect |
| --- | --- | --- |
| Single PR / staged execution | Run remaining reform as internal stages on this Governance carrier and one final PR path. | R1-R9 staged execution plan; PR Readiness held until validation is green and USER separately approves PR creation. |
| Main as canonical pointer ledger | `Docs/Main.md` is the least-updated canonical docs index and recovery map. | Do not add branch/release/current-state ledgers to Main. |
| Canonical docs versus context docs | Canonical docs own law/routing; context docs preserve evidence, product reasoning, and history. | Every Docs file receives owner category, disposition, ambiguity risk, and structure risk. |
| Branch plans retire, not delete by default | Active operational plans live in external state after transition; repo plan files preserve transition evidence or historical receipts, then fold down, migrate durable content, and retire. | Historical plan files are indexed as retired from active planning posture; deletion remains USER-gated. |
| Traceability compaction is dangerous | Branch records may remain large when they are structured traceability receipts. | Organize receipts instead of compressing away commit/PR/release/validation evidence. |
| Safe docs may delete/collapse only after proof | Deletion requires reference scan, replacement owner, and USER acceptance when ambiguous. | Every Docs file gets keep/organize/migrate/retire/delete posture. |
| Nexus Vision contract | `Docs/nexus_vision.md` is the Nexus-wide vision contract after focused reference migration. | Use Nexus Vision for project-wide direction and family visions for durable family direction. |
| Backlog family vision discussion | Backlog points to family vision owners but does not absorb long planning narratives. | Keep backlog compact while preserving product-intent routing. |

## Single-PR Staged Execution Plan

All remaining Docs reform work stays on this Governance branch as staged internal commits until USER accepts the full reform surface. PR creation is not the next move by inertia.

| Stage | Name | Purpose | Allowed Work | Completion Proof |
| --- | --- | --- | --- | --- |
| R1 | User-response model correction | Turn USER responses into model decisions instead of passive notes. | Update model, generator, generated dossier/index, and validator section requirements. | Dossier/index expose integration sections. |
| R2 | Canonical/context taxonomy | Make Main the least-updated canonical docs index and classify context docs. | Update ownership language and file-by-file review categories. | Every Docs file has owner, action, risk, and migration target. |
| R3 | Backlog/roadmap enforcement model | Keep backlog as product registry/pointers and roadmap as release-stage breakpoint outline. | Harden schemas and sprawl checks. | Backlog/roadmap validators stay green. |
| R4 | Branch plan lifecycle model | Keep active planning detailed while preventing stale active authority after completion. | Use the retirement index to mark historical plans retired from active posture; no default deletion. | Branch plans appear in the retirement index before any deletion is considered. |
| R5 | Structured branch receipt model | Preserve traceability without duplicate live-state chaos. | Define receipt schema and queue high-risk records for organization. | Structure queues identify records needing organization. |
| R6 | Vision contract implementation | Treat `Docs/nexus_vision.md` as the Nexus Vision contract and `Docs/family_visions/` as the family vision owner layer. | Reference migration and family vision creation completed. | Operating model and dossier carry Product Vision Contract language. |
| R7 | Safe file disposition review | Identify keep/collapse/migrate/retire/delete posture for every Docs file. | Generate disposition table and USER decision list. | Manifest count matches filesystem enumeration. |
| R8 | Validator and review-surface hardening | Make corrected review model regeneration-safe. | Update helper/validator sections and regenerate audit/index. | Validation passes and generated output is stable. |
| R9 | Final USER review hold | Stop before PR Readiness until validation is green and USER separately approves PR creation. | Report results only. | Next legal phase remains USER review / PR Readiness approval. |

## Disposition Changes From USER Review

| Surface | Prior Risky Interpretation | Corrected Disposition |
| --- | --- | --- |
| Branch plans | Delete after PR Readiness | Historical plans are indexed as retired from active planning posture; deletion still needs separate USER approval and reference proof. |
| Branch records | Compact receipts | Structured traceability receipts; size is acceptable when evidence is organized and not duplicate live state. |
| Main | General source-truth doc | Least-updated canonical docs index, recovery map, and owner pointer ledger. |
| Backlog | Current status plus detailed trace | Compact product registry, family scope/status, package summary, and pointers. |
| Roadmap | Release/current-state record | Release-stage schedule outline, public milestone posture, and broad feature breakpoints. |
| Vision | Low-risk product reference | Nexus Vision contract plus family vision records that drive backlog and branch planning. |
| Safe/low-risk docs | Safe to leave | Reference-scan before delete/collapse, with replacement owner and USER acceptance recorded. |

## Docs Organization Cleanup Pass

Cleanup Pass Status: USER requested a docs organization cleanup pass.
Execution Boundary: non-destructive organization planning and queue clarification only. This pass does not move, rename, delete, archive, or rewrite historical files.
Source Review Surface: `Docs/governance_docs_full_inventory_reform_audit.md`, `Docs/governance_docs_reform_user_review_index.md`, and the local USER hub review packet.
Next USER Decision: choose one focused cleanup lane before any physical file or history-affecting change.

| Cleanup Lane | Current Queue Size | Safe Current Action | USER-Gated Later Action |
| --- | ---: | --- | --- |
| Ambiguous ownership/current-state wording | 149 | Keep queued with owner/review action visible. | Focused wording repair or source-truth owner migration. |
| Structure and indexability risks | 39 | Keep queued with structure action visible. | Focused organization pass for one owner family or receipt set. |
| Migration / organization candidates | 0 | Keep candidate rows visible in this dossier. | Move durable content only after replacement owner and validation proof. |
| Retired branch plan review | 29 | Keep retired posture and lookup paths. | Delete or archive only after reference proof and USER approval. |
| Low-risk reference consolidation | 19 | Leave in place unless USER selects a consolidation lane. | Collapse/delete only after reference scan and replacement owner proof. |

Recommended First Cleanup Lane: organize oversized historical branch records into current-summary plus indexed historical sections, without deleting evidence or changing source-truth ownership.
Do Not Start Yet: branch-plan deletion, broad directory/file renames, historical receipt rewrites, runtime/FAM/release mutation, or archive/delete work. Those require separate exact USER approval.

## Files Needing USER Decision

| File | Reason | Recommendation |
| --- | --- | --- |
| `Docs/branch_plans/feature_compact_ai_status_card.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_display_acceptance_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_followup_repair_setup_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_followup_uts_reference_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_lv1_visual_governance_gap_reference_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_returned_uts_issue_form_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_returned_uts_repair_setup_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_returned_uts_temporary_reference_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_visual_inspection_matrix_repair_reference_20260521.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_ai_edition_public_leak_prevention_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_ai_runtime_trust_boundary_readiness.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_completion_foundation.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | branch plan is retired from active planning posture and preserved for lookup | delete only after USER approval plus reference proof; do not delete by default |

## Ambiguity Review Queue

Queue Status: Future USER-gated organization queue; not a PR blocker unless validator output identifies an active failure.

| File | Ambiguity Risk | Signals | Action |
| --- | --- | --- | --- |
| `Docs/Main.md` | High | `volatile-current-wording=340`; `unclear-ownership-wording=156`; `soft-commitment-wording=63`; `state-ledger-wording=228` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/ai_runtime_and_trust_architecture.md` | High | `volatile-current-wording=11`; `unclear-ownership-wording=13`; `soft-commitment-wording=37`; `state-ledger-wording=37` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/README.md` | High | `volatile-current-wording=85`; `unclear-ownership-wording=75`; `soft-commitment-wording=26`; `state-ledger-wording=110` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_compact_ai_status_card.md` | High | `volatile-current-wording=30`; `unclear-ownership-wording=18`; `soft-commitment-wording=4`; `state-ledger-wording=52` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md` | High | `volatile-current-wording=187`; `unclear-ownership-wording=151`; `soft-commitment-wording=17`; `state-ledger-wording=109` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_006_overlay_display_acceptance_foundation.md` | High | `volatile-current-wording=163`; `unclear-ownership-wording=79`; `soft-commitment-wording=25`; `state-ledger-wording=136` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation.md` | High | `volatile-current-wording=85`; `unclear-ownership-wording=13`; `soft-commitment-wording=2`; `state-ledger-wording=94` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_returned_uts_issue_form_20260521.md` | High | `volatile-current-wording=133`; `unclear-ownership-wording=21`; `soft-commitment-wording=72`; `state-ledger-wording=223` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md` | High | `volatile-current-wording=94`; `unclear-ownership-wording=23`; `soft-commitment-wording=4`; `state-ledger-wording=58` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md` | High | `volatile-current-wording=36`; `unclear-ownership-wording=33`; `soft-commitment-wording=7`; `state-ledger-wording=45` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md` | High | `volatile-current-wording=177`; `unclear-ownership-wording=257`; `soft-commitment-wording=32`; `state-ledger-wording=75` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_ai_edition_public_leak_prevention_foundation.md` | High | `volatile-current-wording=114`; `unclear-ownership-wording=174`; `soft-commitment-wording=11`; `state-ledger-wording=114` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_ai_runtime_trust_boundary_readiness.md` | High | `volatile-current-wording=27`; `unclear-ownership-wording=32`; `soft-commitment-wording=6`; `state-ledger-wording=46` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md` | High | `volatile-current-wording=60`; `unclear-ownership-wording=66`; `soft-commitment-wording=3`; `state-ledger-wording=54` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_foundation.md` | High | `volatile-current-wording=46`; `unclear-ownership-wording=15`; `soft-commitment-wording=13`; `state-ledger-wording=98` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md` | High | `volatile-current-wording=59`; `unclear-ownership-wording=78`; `soft-commitment-wording=8`; `state-ledger-wording=137` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md` | High | `volatile-current-wording=70`; `unclear-ownership-wording=103`; `soft-commitment-wording=12`; `state-ledger-wording=119` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | High | `volatile-current-wording=22`; `unclear-ownership-wording=11`; `soft-commitment-wording=4`; `state-ledger-wording=53` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |

## Structure Review Queue

Queue Status: Future USER-gated organization queue; not a PR blocker unless validator output identifies an active failure.

| File | Structure Risk | Action |
| --- | --- | --- |
| `Docs/branch_records/codex_fb_037_release_debt_packaging.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_automation_planning.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_ai_edition_public_leak_prevention_foundation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_ai_runtime_trust_boundary_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |

## High-Risk Review Queue

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/feature_backlog.md` | compact product registry | Keep compact | Critical |
| `Docs/prebeta_roadmap.md` | release schedule outline | Keep compact | Critical |
| `Docs/Main.md` | recovery map / source-truth router | Keep | High |
| `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_plans/feature_fam_006_overlay_display_acceptance_foundation.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_plans/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_plans/feature_fam_007_ai_edition_public_leak_prevention_foundation.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_completion_foundation.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_plans/feature_fam_007_v1_7_23_post_release_canon_closure.md` | branch runtime engineering plan | Retired posture indexed | High |
| `Docs/branch_records/codex_fb_037_release_debt_packaging.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/codex_one_time_backlog_governance_repair.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_pr112_source_truth_closeout.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_automation_planning.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | branch authority / structured receipt | Organize structured receipt | High |

## Future Migration Queue

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| None | N/A | N/A | N/A |

## Safe To Leave For Now

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/boot_access_design.md` | product / architecture reference | Keep | Low |
| `Docs/closeout_index.md` | release closeout receipt | Keep | Low |
| `Docs/closeouts/v1.6.0_closeout.md` | release closeout receipt | Keep | Low |
| `Docs/closeouts/v1.9.0_closeout.md` | release closeout receipt | Keep | Low |
| `Docs/closeouts/v2.0_closeout.md` | release closeout receipt | Keep | Low |
| `Docs/family_visions/FAM-001_boot_interface.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/FAM-002_desktop_interface.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/FAM-003_interaction_and_actions.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/FAM-004_voice_and_audio.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/FAM-005_external_integrations.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/FAM-008_packaging_and_install_experience.md` | family vision | Keep as family vision owner | Low |
| `Docs/family_visions/README.md` | family vision index | Keep as family vision router | Low |
| `Docs/nexus_vision.md` | Nexus Vision Contract | Keep as project-wide vision owner | Low |
| `Docs/orin_display_naming_guidance.md` | product / architecture reference | Keep | Low |
| `Docs/workspace_layout_plan.md` | product / architecture reference | Keep | Low |
| `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md` | workstream durable history | Keep / normalize durable history | Low |
| `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md` | workstream durable history | Keep / normalize durable history | Low |

## Exact USER Decision This Index Supports

`I accept the corrected USER-response integration model and approve continuing the staged Docs source-truth reform on feature/release-readiness-source-truth-intake as one final Governance PR path. PR creation, merge, release work, runtime work, FAM-006/FAM-007/Compact-AI mutation, issue work, branch cleanup, historical branch deletion, and successor branch creation remain separate decisions.`
