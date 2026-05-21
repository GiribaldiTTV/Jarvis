# Nexus Docs Reform User Review Index

## Start Here

This is the short review index for the full Docs source-truth reform. Use it to decide whether the long dossier is ready for PR Readiness, or whether specific files need more cleanup first.

## Review Proof

- Full dossier: `Docs/governance_docs_full_inventory_reform_audit.md`
- Docs files covered: 137
- Git proof: derive live `HEAD`, `origin/main`, and merge-base with git at review/validation time.
- Generated hash fields: intentionally not maintained in this docs review index.
- Runtime/FAM/Compact-AI mutation: none.
- PR Readiness: held until USER review accepts this packet.

## Suggested Review Order

1. Read `Executive Summary` and `How To Review This Dossier` in the full dossier.
2. Review `What Was Completed`, `What Remains Deferred`, and `What Requires USER Decision`.
3. Review `USER Response Integration Matrix` and confirm each response changed the model.
4. Review `Single-PR Staged Execution Plan` before deciding whether work should continue.
5. Review the `Completed / Deferred Matrix` for the reform scope.
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
- [ ] Deferred retirement/fold-down candidates should remain deferred for now.
- [ ] No additional Docs file needs immediate retirement before PR Readiness.
- [ ] Every Docs file has a clear disposition in the complete cleanup table.
- [ ] Ambiguous ownership/current-state wording has a clear owner or deferred review action.
- [ ] Structure risks have a migration, organization, or keep-now decision.
- [ ] Validators are enough to stop the worst sprawl from returning.
- [ ] PR Readiness Stage 2 may proceed after final validation.

## User Response Intake Status

- USER review responses are recorded in `Docs/governance_process_efficiency_reform_plan.md` under the 2026-05-21 review intake.
- This generated index stays pointer-based so audit regeneration does not strand raw USER notes in a generated file.
- Current execution model: analysis and model maintenance only until USER accepts the corrected review surface; remaining Docs reform should run in staged internal commits on this single Governance branch/PR path rather than revolving PRs.
- PR Readiness remains held while the USER is correcting the model and execution plan.

## USER Response Integration Summary

| USER Response Area | Model Decision | Execution Effect |
| --- | --- | --- |
| Single PR / staged execution | Run remaining reform as internal stages on this Governance carrier and one final PR path. | R1-R9 staged execution plan; PR Readiness held until USER accepts the corrected surface. |
| Main as canonical pointer ledger | `Docs/Main.md` is the least-updated canonical docs index and recovery map. | Do not add branch/release/current-state ledgers to Main. |
| Canonical docs versus context docs | Canonical docs own law/routing; context docs preserve evidence, product reasoning, and history. | Every Docs file receives owner category, disposition, ambiguity risk, and structure risk. |
| Branch plans retire, not delete by default | Plans are canonical while active, then fold down, migrate durable content, and retire. | Plan files become retirement candidates only after fold-down proof. |
| Traceability compaction is dangerous | Branch records may remain large when they are structured traceability receipts. | Organize receipts instead of compressing away commit/PR/release/validation evidence. |
| Safe docs may delete/collapse only after proof | Deletion requires reference scan, replacement owner, and USER acceptance when ambiguous. | Every Docs file gets keep/organize/migrate/retire/delete posture. |
| Nexus Vision contract | `Docs/orin_vision.md` should be evaluated as a Nexus-wide vision contract. | Record the model now; do not rename/reframe without focused reference update. |
| Backlog family vision discussion | Backlog may point to family vision owners but should not absorb long planning narratives. | Keep backlog compact while preserving product-intent routing. |

## Single-PR Staged Execution Plan

All remaining Docs reform work stays on this Governance branch as staged internal commits until USER accepts the full reform surface. PR creation is not the next move by inertia.

| Stage | Name | Purpose | Allowed Work | Completion Proof |
| --- | --- | --- | --- | --- |
| R1 | User-response model correction | Turn USER responses into model decisions instead of passive notes. | Update model, generator, generated dossier/index, and validator section requirements. | Dossier/index expose integration sections. |
| R2 | Canonical/context taxonomy | Make Main the least-updated canonical docs index and classify context docs. | Update ownership language and file-by-file review categories. | Every Docs file has owner, action, risk, and migration target. |
| R3 | Backlog/roadmap enforcement model | Keep backlog as product registry/pointers and roadmap as release-stage breakpoint outline. | Harden schemas and sprawl checks. | Backlog/roadmap validators stay green. |
| R4 | Branch plan lifecycle model | Keep active planning detailed while preventing stale active authority after completion. | Use fold-down/retirement candidate queues; no default deletion. | Branch plans list as retirement candidates only. |
| R5 | Structured branch receipt model | Preserve traceability without duplicate live-state chaos. | Define receipt schema and queue high-risk records for organization. | Structure queues identify records needing organization. |
| R6 | Vision contract planning | Treat `Docs/orin_vision.md` as future Nexus Vision contract candidate. | Record rename/reframe analysis; no rename yet. | Operating model and dossier carry Product Vision Contract language. |
| R7 | Safe file disposition review | Identify keep/collapse/migrate/retire/delete posture for every Docs file. | Generate disposition table and USER decision list. | Manifest count matches filesystem enumeration. |
| R8 | Validator and review-surface hardening | Make corrected review model regeneration-safe. | Update helper/validator sections and regenerate audit/index. | Validation passes and generated output is stable. |
| R9 | Final USER review hold | Stop before PR Readiness until USER accepts the complete reform surface. | Report results only. | Next legal phase remains USER review. |

## Disposition Changes From USER Review

| Surface | Prior Risky Interpretation | Corrected Disposition |
| --- | --- | --- |
| Branch plans | Delete after PR Readiness | Fold down, migrate durable content, then retire by explicit posture; deletion needs separate USER approval. |
| Branch records | Compact receipts | Structured traceability receipts; size is acceptable when evidence is organized and not duplicate live state. |
| Main | General source-truth doc | Least-updated canonical docs index, recovery map, and owner pointer ledger. |
| Backlog | Current status plus detailed trace | Compact product registry, family scope/status, package summary, and pointers. |
| Roadmap | Release/current-state record | Release-stage schedule outline, public milestone posture, and broad feature breakpoints. |
| Vision | Low-risk product reference | Future Nexus Vision contract candidate that drives backlog and branch planning. |
| Safe/low-risk docs | Safe to leave | Reference-scan before delete/collapse, with replacement owner and USER acceptance recorded. |

## Files Needing USER Decision

| File | Reason | Recommendation |
| --- | --- | --- |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | branch plan should be retired after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | branch plan should be retired after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | branch plan should be retired after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | branch plan should be retired after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted by default |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | branch plan should be retired after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted by default |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md` | branch plan should be retired after fold-down proves durable content migrated | safe later after owning branch PR Readiness fold-down; not deleted by default |

## Ambiguity Review Queue

| File | Ambiguity Risk | Signals | Action |
| --- | --- | --- | --- |
| `Docs/Main.md` | High | `volatile-current-wording=320`; `unclear-ownership-wording=130`; `soft-commitment-wording=51`; `state-ledger-wording=155` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/README.md` | High | `volatile-current-wording=23`; `unclear-ownership-wording=26`; `soft-commitment-wording=8`; `state-ledger-wording=26` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | High | `volatile-current-wording=22`; `unclear-ownership-wording=11`; `soft-commitment-wording=4`; `state-ledger-wording=53` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | High | `volatile-current-wording=41`; `unclear-ownership-wording=11`; `soft-commitment-wording=3`; `state-ledger-wording=84` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | High | `volatile-current-wording=27`; `unclear-ownership-wording=16`; `soft-commitment-wording=4`; `state-ledger-wording=76` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/codex_one_time_backlog_governance_repair.md` | High | `volatile-current-wording=57`; `unclear-ownership-wording=7`; `soft-commitment-wording=5`; `state-ledger-wording=33` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | High | `volatile-current-wording=140`; `unclear-ownership-wording=38`; `soft-commitment-wording=7`; `state-ledger-wording=77` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_release_canon_closure.md` | High | `volatile-current-wording=91`; `unclear-ownership-wording=25`; `soft-commitment-wording=2`; `state-ledger-wording=32` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/codex_v1_6_13_prebeta_pr112_source_truth_closeout.md` | High | `volatile-current-wording=74`; `unclear-ownership-wording=59`; `soft-commitment-wording=6`; `state-ledger-wording=47` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md` | High | `volatile-current-wording=53`; `unclear-ownership-wording=22`; `soft-commitment-wording=5`; `state-ledger-wording=53` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_automation_planning.md` | High | `volatile-current-wording=113`; `unclear-ownership-wording=34`; `soft-commitment-wording=8`; `state-ledger-wording=65` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md` | High | `volatile-current-wording=78`; `unclear-ownership-wording=17`; `state-ledger-wording=41` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | High | `volatile-current-wording=106`; `unclear-ownership-wording=25`; `soft-commitment-wording=5`; `state-ledger-wording=51` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md` | High | `volatile-current-wording=124`; `unclear-ownership-wording=35`; `soft-commitment-wording=16`; `state-ledger-wording=95` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md` | High | `volatile-current-wording=99`; `unclear-ownership-wording=31`; `soft-commitment-wording=17`; `state-ledger-wording=50` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md` | High | `volatile-current-wording=134`; `unclear-ownership-wording=39`; `soft-commitment-wording=17`; `state-ledger-wording=163` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_fam_006_issue_readiness_governance_repair.md` | High | `volatile-current-wording=58`; `unclear-ownership-wording=23`; `soft-commitment-wording=6`; `state-ledger-wording=31` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |
| `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md` | High | `volatile-current-wording=187`; `unclear-ownership-wording=61`; `soft-commitment-wording=38`; `state-ledger-wording=279` | Clarify owner, time basis, and whether wording is historical receipt or live truth. |

## Structure Review Queue

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
| `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |
| `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | High | Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evid... |

## High-Risk Review Queue

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/feature_backlog.md` | compact product registry | Keep compact | Critical |
| `Docs/prebeta_roadmap.md` | release schedule outline | Keep compact | Critical |
| `Docs/Main.md` | recovery map / source-truth router | Keep | High |
| `Docs/branch_records/codex_fb_037_release_debt_packaging.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/codex_one_time_backlog_governance_repair.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_pr112_source_truth_closeout.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_automation_planning.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_backlog_family_governance_reform.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_release_support.md` | branch authority / structured receipt | Keep historical receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md` | branch authority / structured receipt | Organize structured receipt | High |
| `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md` | branch authority / structured receipt | Organize structured receipt | High |

## Future Migration Queue

| File | Owner | Recommendation | Risk |
| --- | --- | --- | --- |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_execution_readiness_gates.md` | branch runtime engineering plan | Fold-down then retire candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_path_and_consent_readiness.md` | branch runtime engineering plan | Fold-down then retire candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md` | branch runtime engineering plan | Fold-down then retire candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_contract_readiness.md` | branch runtime engineering plan | Fold-down then retire candidate | Medium |
| `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md` | branch runtime engineering plan | Fold-down then retire candidate | Medium |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md` | branch runtime engineering plan | Fold-down then retire candidate | Medium |

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

`I accept the corrected USER-response integration model and approve continuing the staged Docs source-truth reform on feature/release-readiness-source-truth-intake as one final Governance PR path. PR creation, merge, release work, runtime work, FAM-006/FAM-007/Compact-AI mutation, issue work, branch cleanup, historical branch deletion, and successor branch creation remain separate decisions.`
