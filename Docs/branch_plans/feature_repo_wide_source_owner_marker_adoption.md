# Branch Runtime Engineering Plan - Repo-Wide High-Risk Source Owner Marker Adoption
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FOLDDOWN-LINKAGE-012; surface=branch-plan-pr-release-fold-down; status=canonical -->

## Branch Runtime Engineering Plan

Plan Identity: `Repo-Wide High-Risk Source Owner Marker Adoption Branch Runtime Engineering Plan`

Owning Branch: `feature/repo-wide-source-owner-marker-adoption`

Worktree Path: `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`

Branch Authority Record Pointer: `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`

Current Phase: `Workstream implementation`

Branch Runtime Engineering Plan: `Implemented for bounded Workstream. The plan admits source-truth policy, high-risk surface inventory, marker-to-ledger consistency validation, marker coverage, production UI exclusion validation, and Dev Toolkit review-mode disposition planning. Runtime/product behavior changes remain blocked.`

Engineering Plan Status: `Accepted - created during Branch Readiness Stage 2 from origin/main 26bb76becd4089d2e451d44e969939f0f074371f and completed through bounded Workstream implementation. H1, LV, PR creation, merge, release, issue mutation, cleanup, Compact-AI mutation, stable worktree rebinding, and runtime/product work remain pending USER decisions.`

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

Approval-Boundary Audit: `USER approved Branch Readiness Stage 2 setup and bounded Workstream implementation. Broader marker insertion, Dev Toolkit runtime, production runtime behavior, product UI, PR, merge, release, issue mutation, cleanup, FAM-007, Governance, and Compact-AI remain outside scope.`

FAM / Shared-Surface Overlap Forecast: `FAM-006 is historical/merged and owns canonical historical ledger rows; FAM-007 is a separate worktree and provider lane; Governance is the standing intake lane; Compact-AI is separate. Future marker insertion may touch shared runtime/UI/proof surfaces and must run a Pre-Rebaseline Impact Audit if origin/main advances.`

Open Questions: `Whether later marker work should broaden beyond the limited high-risk pilot, and whether Dev Toolkit review-mode remains planning-only or becomes implementation scope.`

USER Planning Decisions: `USER approved Stage 1 analysis, Stage 2 setup, bounded Workstream implementation, selected FAM-006/SRCOWN marker insertion, and reusable marker validator implementation. USER has not approved Hardening H1, broader marker insertion, Dev Toolkit runtime, PR creation, merge, release, issue mutation, or cleanup.`

Plan Revision History: `v2 - bounded Workstream implementation after origin/main 26bb76becd4089d2e451d44e969939f0f074371f, with inventory artifact, reusable marker validator, limited FAM-006/SRCOWN marker pilot, and production UI exclusion proof.`

Plan-To-Implementation Traceability Table: `Planned marker inventory, syntax, ledger mapping, coverage, and production UI exclusion are traced to actual implementation files: Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption_inventory.md, dev/orin_source_owner_marker_validation.py, Docs/validation_helper_registry.md, selected high-risk FAM-006/SRCOWN source-comment markers, inventory-only dispositions for FAM-007/provider/core and Compact-AI surfaces, and production UI exclusion checks.`

Hardening Comparison Checklist: `H1 must compare implemented marker syntax, coverage, ledger mapping, not-applicable reasons, production UI exclusion, validator scope, dev-only review-mode boundaries, and unchanged runtime behavior against this plan.`

Live Validation Proof Or Waiver Checklist: `Live Validation is not required for setup-only source truth. If Workstream implements only static markers/validators, LV may use static validation proof or USER waiver. If dev-only UI or production-visible UI changes are admitted, focused visual proof and UTS or explicit waiver are required.`

PR Readiness Fold-Down / Retention Checklist: `PR Readiness must decide whether this plan remains as historical branch source truth, whether durable marker policy moves to development_rules or phase_governance, whether the active branch authority record becomes historical/no-active before merge, and whether backlog/roadmap return to compact No Active Branch truth.`

Release Readiness Public-Scope Translation Checklist: `Public release language must describe developer/source-traceability improvements only if there are no production runtime changes. It must not expose internal marker IDs, ledger IDs, element numbers, or governance jargon to end users.`

USER Planning Review: `Complete for Stage 2 setup and bounded Workstream implementation; Hardening H1 approval remains pending.`

PR Fold-Down Packet: `Prepared for later PR Readiness - preserve durable marker syntax, validator command, inventory artifact, limited pilot marker list, production UI exclusion rule, and inventory-only dispositions; convert active branch truth to historical/no-active before PR merge if USER later approves PR creation.`

Runtime Implementation Approval: `Pending/Blocked - not granted for runtime behavior, production UI, Dev Toolkit runtime, or product feature changes. Bounded source-only marker insertion and marker validator implementation were granted for this Workstream and are complete.`

## Workstream Implementation Closeout

Workstream Completion State: `Green - bounded multi-seam source-owner marker adoption complete and ready for Hardening H1 after USER approval.`


Implemented Marker Classes: `Selected FAM-006 Dashboard / Sensor Command Center source comments and the source-owner marker validator self-marker; inventory-only dispositions for FAM-007/provider/core, Compact-AI, generic launcher, release-helper, blanket all-file insertion, Dev Toolkit runtime, and cleanup/rebinding execution surfaces.`

First-Pass Adoption Surfaces: `desktop/desktop_renderer.py Dashboard resize hit-test; nexus_visual/monitoring_hud.js interaction proof; nexus_visual/monitoring_hud.css control-affordance styles; dev/orin_monitoring_hud_human_client_validation.ps1 real-client proof; dev/orin_monitoring_hud_surface_validation.py proof-quality source check; dev/orin_source_owner_marker_validation.py marker-ledger consistency validator.`

Deferred Surfaces: `Blanket all-file marker insertion, Compact-AI source mutation, branch/worktree cleanup or deletion, stable worktree rebinding execution, production runtime behavior changes, production UI changes, Dev Toolkit runtime/review-mode implementation, and future runtime/product lanes.`

Validation Command Added: `python dev\orin_source_owner_marker_validation.py`

H1 Focus: `Compare marker syntax, marker-to-ledger mapping, pilot coverage, inventory-only dispositions, production UI exclusion, Compact-AI preservation, approval boundaries, and unchanged runtime/product behavior against this plan.`
