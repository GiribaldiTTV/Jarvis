# Source Owner Marker Inventory - Repo-Wide First Pass
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-SCAN-INVENTORY-002; surface=source-owner-first-pass-inventory; status=canonical -->

Element Validation Ledger rows remain canonical. First-pass source-owner markers are dev-only backlinks; production UI exclusion is required. Compact-AI-Status-Card protected unique commits stay external. Deferred Surfaces and inventory-only decisions remain USER-gated.

Marker syntax: `NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=<OWNER>; ledger=<LEDGER-ID>; surface=<SURFACE>; status=<canonical|shared|external>`

## First-Pass Adoption Surfaces

| Path | Owner | Ledger | Surface | Status |
| --- | --- | --- | --- | --- |
| `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md` | `GOV-SOURCE-TRUTH` | `SRCOWN-GOV-POLICY-001` | `branch-authority-marker-policy` | `canonical` |
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md` | `GOV-SOURCE-TRUTH` | `SRCOWN-FOLDDOWN-LINKAGE-012` | `branch-plan-pr-release-fold-down` | `canonical` |
| `Docs/feature_backlog.md` | `SHARED-DOCS` | `SRCOWN-FIRSTPASS-DOCS-011` | `compact-current-state-owner` | `shared` |
| `Docs/prebeta_roadmap.md` | `SHARED-DOCS` | `SRCOWN-FIRSTPASS-DOCS-011` | `compact-current-state-owner` | `shared` |
| `Docs/branch_records/index.md` | `SHARED-DOCS` | `SRCOWN-FIRSTPASS-DOCS-011` | `branch-record-index-owner` | `shared` |
| `Docs/validation_helper_registry.md` | `VALIDATOR-HELPER` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `validation-helper-registry` | `canonical` |
| `Docs/worktree_slots.md` | `GOV-SOURCE-TRUTH` | `SRCOWN-CLEANUP-REBINDING-013` | `worktree-slot-rebinding-posture` | `canonical` |
| `dev/orin_branch_governance_validation.py` | `GOV-SOURCE-TRUTH` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `branch-governance-validator` | `shared` |
| `dev/orin_governance_efficiency_validation.py` | `GOV-SOURCE-TRUTH` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `governance-efficiency-validator` | `shared` |
| `dev/orin_validation_suite.py` | `VALIDATOR-HELPER` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `validation-suite-recommendation-helper` | `shared` |
| `dev/orin_user_review_bundle.py` | `GOV-SOURCE-TRUTH` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `user-review-bundle-helper` | `shared` |
| `dev/orin_user_review_bundle_false_green_fixture_validation.py` | `GOV-SOURCE-TRUTH` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `user-review-bundle-false-green-fixtures` | `shared` |
| `dev/orin_worktree_rebaseline_audit.py` | `GOV-SOURCE-TRUTH` | `SRCOWN-CLEANUP-REBINDING-013` | `worktree-rebaseline-audit-helper` | `shared` |
| `dev/orin_branch_readiness_planning_fixture_validation.py` | `VALIDATOR-HELPER` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `branch-readiness-planning-fixture-validator` | `shared` |
| `dev/orin_pr_review_churn_validation.py` | `VALIDATOR-HELPER` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `pr-review-churn-validation` | `shared` |
| `dev/orin_rar_issue_candidate_durability_validation.py` | `VALIDATOR-HELPER` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `rar-issue-candidate-durability-validator` | `shared` |
| `dev/orin_ai_provider_state_validation.py` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `fam007-provider-state-validator` | `shared` |
| `dev/orin_public_leak_prevention_validation.py` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `fam007-public-leak-prevention-validator` | `shared` |
| `dev/orin_monitoring_hud_surface_validation.py` | `FAM006-HUD` | `SRCOWN-FIRSTPASS-FAM006-HUD-008` | `fam006-hud-surface-validator` | `shared` |
| `dev/orin_monitoring_hud_internal_sandbox_validation.py` | `FAM006-HUD` | `SRCOWN-FIRSTPASS-FAM006-HUD-008` | `fam006-hud-internal-sandbox-validator` | `shared` |
| `dev/orin_monitoring_hud_human_client_validation.ps1` | `FAM006-HUD` | `SRCOWN-FIRSTPASS-FAM006-HUD-008` | `fam006-hud-human-client-validator` | `shared` |
| `dev/orin_source_owner_marker_validation.py` | `VALIDATOR-HELPER` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `source-owner-marker-validator` | `canonical` |
| `dev/orin_workspace_root_residue_validation.py` | `VALIDATOR-HELPER` | `SRCOWN-RELOCATION-CLOSURE-015` | `workspace-root-residue-validator` | `canonical` |
| `dev/orin_guarded_c_root_cleanup.py` | `VALIDATOR-HELPER` | `SRCOWN-RELOCATION-CLOSURE-015` | `guarded-c-root-cleanup-gate` | `canonical` |
| `dev/nexus_paths.py` | `GOV-SOURCE-TRUTH` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `workspace-root-paths` | `shared` |
| `Docs/nexus_workspace_roots.md` | `GOV-SOURCE-TRUTH` | `SRCOWN-FIRSTPASS-VALIDATOR-010` | `workspace-root-routing` | `shared` |
| `desktop/ai_provider_state.py` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `provider-state-contract` | `shared` |
| `desktop/core_visualization_renderer.py` | `SHARED-DESKTOP-CORE` | `SRCOWN-FIRSTPASS-SHARED-DESKTOP-009` | `core-visualization-provider-state-publisher` | `shared` |
| `desktop/desktop_renderer.py` | `SHARED-DESKTOP-CORE` | `SRCOWN-FIRSTPASS-SHARED-DESKTOP-009` | `desktop-renderer-provider-and-hud-publisher` | `shared` |
| `nexus_visual/orin_core.html` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `orin-core-provider-status-template` | `shared` |
| `nexus_visual/orin_core_desktop.html` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `orin-core-desktop-provider-status-template` | `shared` |
| `nexus_visual/orin_core.css` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `orin-core-provider-status-styles` | `shared` |
| `nexus_visual/orin_core_desktop.css` | `SHARED-DESKTOP-CORE` | `SRCOWN-FIRSTPASS-SHARED-DESKTOP-009` | `orin-core-desktop-layer-styles` | `shared` |
| `nexus_visual/orin_core.js` | `FAM007-AI` | `SRCOWN-FIRSTPASS-FAM007-AI-007` | `orin-core-provider-status-script` | `shared` |
| `nexus_visual/monitoring_hud.html` | `FAM006-HUD` | `SRCOWN-FIRSTPASS-FAM006-HUD-008` | `monitoring-hud-dashboard-template` | `shared` |
| `nexus_visual/monitoring_hud.css` | `FAM006-HUD` | `SRCOWN-FIRSTPASS-FAM006-HUD-008` | `monitoring-hud-dashboard-styles` | `shared` |
| `nexus_visual/monitoring_hud.js` | `FAM006-HUD` | `SRCOWN-FIRSTPASS-FAM006-HUD-008` | `monitoring-hud-dashboard-script` | `shared` |

## Deferred Surfaces

Blanket all-file marker insertion, FAM-006 rebinding, FAM-007 runtime/product mutation, Governance mutation outside this branch path, branch/worktree cleanup or deletion, Dev Toolkit runtime UI, release work, and Compact-AI mutation stay deferred or inventory-only.
| `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption_inventory.md` | `GOV-SOURCE-TRUTH` | `SRCOWN-SCAN-INVENTORY-002` | `source-owner-first-pass-inventory` | `canonical` |
| `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md` | `COMPACT-AI-PROTECTED` | `SRCOWN-COMPACT-AI-PRESERVE-014` | `compact-ai-protected-unique-commit-posture` | `external` |
