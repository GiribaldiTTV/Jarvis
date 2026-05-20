# Branch Runtime Engineering Plan - Repo-Wide High-Risk Source Owner Marker Adoption
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FOLDDOWN-LINKAGE-012; surface=branch-plan-pr-release-fold-down; status=canonical -->

## Branch Runtime Engineering Plan

Plan Identity: `Repo-Wide High-Risk Source Owner Marker Adoption Branch Runtime Engineering Plan`

Owning Branch: `feature/repo-wide-source-owner-marker-adoption`

Worktree Path: `Retired after PR #185 cleanup; historical path was C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`

Branch Authority Record Pointer: `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`

Current Phase: `Historical Traceability`

Branch Runtime Engineering Plan: `Implemented for bounded Workstream. The plan admits source-truth policy, high-risk surface inventory, marker-to-ledger consistency validation, marker coverage, production UI exclusion validation, and Dev Toolkit review-mode disposition planning. Runtime/product behavior changes remain blocked.`

Engineering Plan Status: `Historical / folded - created during Branch Readiness Stage 2 from origin/main 26bb76becd4089d2e451d44e969939f0f074371f, completed through bounded Workstream implementation, H1 Green, LV1 Green, PR Readiness, PR #185 merge, and USER-approved branch/worktree cleanup. Release, issue mutation, Compact-AI mutation, stable worktree rebinding, future marker expansion, and runtime/product work remain pending USER decisions.`

Current Runtime Baseline: `origin/main 26bb76becd4089d2e451d44e969939f0f074371f after PR #181 / v1.7.9-prebeta, with production runtime state, config, schema, desktop UI, FAM-006 historical surfaces, FAM-007 provider state, and No Active Branch main truth unchanged before this approved branch creation.`

Branch Purpose: `Create the legal planning and authority carrier for repo-wide high-risk source owner marker adoption while keeping the Element Validation Ledger canonical and markers as dev-only backlinks.`

Planned Runtime Delta: `None for production runtime behavior. Bounded Workstream adds dev-only source-owner comments/backlinks in selected source files and a static validator without changing executable behavior.`

User-Facing Delta: `None. Production UI must not show element numbers, marker IDs, source-owner labels, review badges, hover outlines, ledger tooltips, or Dev Toolkit review annotations.`

Source-Truth Delta: `Create the active branch authority record and this plan; update branch_records index, backlog, roadmap, and validation helper registry as compact pointer/status surfaces; preserve the historical candidate language required by current governance validation.`

State / Config / Schema Delta: `No production state, config, schema, persistence, telemetry, network, provider, model, memory, voice, shortcut, or installer delta. Future marker metadata remains source/dev-only.`

Validator / Helper Delta: `Workstream adds dev/orin_source_owner_marker_validation.py and registers it in the validation helper registry. It validates marker syntax, marker-to-ledger consistency, expected pilot coverage, inventory-only dispositions, duplicate/orphan markers, comment-only placement, and production UI exclusion. Future Dev Toolkit validation remains pending USER approval.`

Expected Changed Files / Surfaces: `Workstream affects source truth, branch plan, high-risk inventory artifact, validation helper registry, source-owner marker validator, selected FAM-006/SRCOWN JS/CSS/Python/PowerShell source comment markers, and no production runtime behavior.`

Workstream / Seam Map: `Seam 1 high-risk inventory; Seam 2 marker format and policy validation; Seam 3 ledger mapping and not-applicable reason model; Seam 4 limited high-risk marker insertion; Seam 5 marker coverage and production UI exclusion validation; Seam 6 Dev Toolkit Interface Review Mode disposition planning.`

Per-Seam Implementation Checklist: `Inventory high-risk source/proof surfaces; define compact marker syntax; map markers to canonical ledger rows; add markers only where useful; implement or update marker validators; prove production UI exclusion; record review-mode dispositions without runtime toolkit implementation unless separately approved.`

Per-Seam Validation Checklist: `Run branch governance, planning fixture validation, release body validation, governance efficiency validation, diff checks, compileall, marker syntax/coverage/ledger validators when implemented, production UI exclusion scans, and any directly affected helper validators.`

Per-Seam User-Facing Proof Checklist: `Stage 2 setup requires no screenshot/live/UTS proof. Future production-visible changes require focused visual proof and UTS or explicit USER waiver. Future dev-only review-mode UI must prove dev-only gating before acceptance.`

Future-Gated Items: `Future-gated and pending approval: marker insertion beyond the selected FAM-006/SRCOWN pilot, Dev Toolkit review-mode implementation, production runtime behavior, production UI changes, PR creation, merge, release/tag/artifact work, issue mutation, branch cleanup, FAM-007 work, Governance intake mutation, Compact-AI work, provider/model/memory/shortcut/installer work, AI Product work, and external telemetry parity.`

Approval-Boundary Audit: `USER approved Branch Readiness Stage 2 setup, bounded Workstream implementation, Hardening H1, and Live Validation LV1. Broader marker insertion, Dev Toolkit runtime, production runtime behavior, product UI, PR creation, merge, release, issue mutation, cleanup, FAM-007, Governance, and Compact-AI remain outside scope.`

FAM / Shared-Surface Overlap Forecast: `FAM-006 is historical/merged and owns canonical historical ledger rows; FAM-007 is a separate worktree and provider lane; Governance is the standing intake lane; Compact-AI is separate. Future marker insertion may touch shared runtime/UI/proof surfaces and must run a Pre-Rebaseline Impact Audit if origin/main advances.`

Open Questions: `Whether later marker work should broaden beyond the limited high-risk pilot, and whether Dev Toolkit review-mode remains planning-only or becomes implementation scope.`

USER Planning Decisions: `USER approved Stage 1 analysis, Stage 2 setup, bounded Workstream implementation, selected FAM-006/SRCOWN marker insertion, reusable marker validator implementation, Hardening H1, Live Validation LV1/static proof, PR Readiness, PR #185 merge, and cleanup. USER has not approved broader marker insertion, Dev Toolkit runtime, release execution, issue mutation, Compact-AI mutation, or future branch/worktree recreation.`

Plan Revision History: `v5 - Historical/folded after PR #185 merge at 6643ce8d18c5e3940c1ef1c0d2b531ad7ef5d79b and USER-approved cleanup, preserving bounded Workstream implementation, H1 Green, inventory artifact, reusable marker validator, limited FAM-006/SRCOWN marker pilot, production UI exclusion proof, Compact-AI preservation posture, cleanup proof, and static validator/source-truth LV1 proof.`

Plan-To-Implementation Traceability Table: `Planned marker inventory, syntax, ledger mapping, coverage, and production UI exclusion are traced to actual implementation files: Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption_inventory.md, dev/orin_source_owner_marker_validation.py, Docs/validation_helper_registry.md, selected high-risk FAM-006/SRCOWN source-comment markers, inventory-only dispositions for FAM-007/provider/core and Compact-AI surfaces, and production UI exclusion checks.`

Hardening Comparison Checklist: `H1 must compare implemented marker syntax, coverage, ledger mapping, not-applicable reasons, production UI exclusion, validator scope, dev-only review-mode boundaries, and unchanged runtime behavior against this plan.`

Hardening H1 Result: `Green - H1 compared implemented marker syntax, marker coverage, marker-to-ledger mapping, inventory-only dispositions, production UI exclusion, source-owner validator scope, validation-suite linkage, Compact-AI preservation, cleanup/rebinding planning posture, approval boundaries, and unchanged runtime/product behavior against this plan and found no remaining H1 blocker.`

Live Validation Proof Or Waiver Checklist: `Complete - LV1 used static validator/source-truth proof because this branch is source-only. No production UI, runtime behavior, Dev Toolkit runtime UI, provider/model path, Compact-AI mutation, cleanup/rebinding execution, PR, merge, release, issue, artifact, or external integration was admitted.`

Live Validation LV1 Result: `Green - static proof from source-owner marker validation, branch governance validation, release-readiness health gate, governance efficiency validation, release body validation, provider-state validation, HUD validators, rebaseline audit, compileall, and diff checks proves the source-only marker adoption branch without requiring UTS/live-client proof.`

PR Readiness Fold-Down / Retention Checklist: `Complete - PR #185 merged, this plan remains as historical branch source truth, durable marker policy and validator proof are retained, the branch authority record is historical/no-active, and backlog/roadmap return to compact post-merge truth.`

Release Readiness Public-Scope Translation Checklist: `Public release language must describe developer/source-traceability improvements only if there are no production runtime changes. It must not expose internal marker IDs, ledger IDs, element numbers, or governance jargon to end users.`

USER Planning Review: `Complete for Stage 2 setup, bounded Workstream implementation, Hardening H1, Live Validation LV1, PR Readiness, PR #185 merge, and cleanup.`

PR Fold-Down Packet: `Complete - preserve durable marker syntax, validator command, inventory artifact, limited pilot marker list, production UI exclusion rule, and inventory-only dispositions; active branch truth is historical/no-active after PR #185 merge and cleanup.`

Runtime Implementation Approval: `Pending/Blocked - not granted for runtime behavior, production UI, Dev Toolkit runtime, or product feature changes. Bounded source-only marker insertion and marker validator implementation were granted for this Workstream and are complete.`

## Workstream Implementation Closeout

Workstream Completion State: `Historical Green - bounded multi-seam source-owner marker adoption, H1 Green, LV1 Green, PR Readiness, PR #185 merge, and cleanup are complete.`


Implemented Marker Classes: `Selected FAM-006 Dashboard / Sensor Command Center source comments and the source-owner marker validator self-marker; inventory-only dispositions for FAM-007/provider/core, Compact-AI, generic launcher, release-helper, blanket all-file insertion, Dev Toolkit runtime, and cleanup/rebinding execution surfaces.`

First-Pass Adoption Surfaces: `desktop/desktop_renderer.py Dashboard resize hit-test; nexus_visual/monitoring_hud.js interaction proof; nexus_visual/monitoring_hud.css control-affordance styles; dev/orin_monitoring_hud_human_client_validation.ps1 real-client proof; dev/orin_monitoring_hud_surface_validation.py proof-quality source check; dev/orin_source_owner_marker_validation.py marker-ledger consistency validator.`

Deferred Surfaces: `Blanket all-file marker insertion, Compact-AI source mutation, branch/worktree cleanup or deletion, stable worktree rebinding execution, production runtime behavior changes, production UI changes, Dev Toolkit runtime/review-mode implementation, and future runtime/product lanes.`

Validation Command Added: `python dev\orin_source_owner_marker_validation.py`

H1 Focus: `Compare marker syntax, marker-to-ledger mapping, pilot coverage, inventory-only dispositions, production UI exclusion, Compact-AI preservation, approval boundaries, and unchanged runtime/product behavior against this plan.`
