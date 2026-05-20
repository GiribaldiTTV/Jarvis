# Branch Runtime Engineering Plan - Repo-Wide High-Risk Source Owner Marker Adoption

## Branch Runtime Engineering Plan

Plan Identity: `Repo-Wide High-Risk Source Owner Marker Adoption Branch Runtime Engineering Plan`

Owning Branch: `feature/repo-wide-source-owner-marker-adoption`

Worktree Path: `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`

Branch Authority Record Pointer: `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`

Current Phase: `Branch Readiness Stage 2 setup`

Branch Runtime Engineering Plan: `Accepted for Stage 2 setup. The plan admits source-truth policy, high-risk surface inventory planning, marker-to-ledger consistency planning, marker coverage planning, production UI exclusion planning, and Dev Toolkit review-mode disposition planning. Runtime/product behavior changes remain blocked.`

Engineering Plan Status: `Accepted - created during Branch Readiness Stage 2 from origin/main 26bb76becd4089d2e451d44e969939f0f074371f. Workstream implementation, marker insertion, validator implementation, Dev Toolkit runtime, PR creation, merge, release, issue mutation, and cleanup remain pending USER decisions.`

Current Runtime Baseline: `origin/main 26bb76becd4089d2e451d44e969939f0f074371f after PR #181 / v1.7.9-prebeta, with production runtime state, config, schema, desktop UI, FAM-006 historical surfaces, FAM-007 provider state, and No Active Branch main truth unchanged before this approved branch creation.`

Branch Purpose: `Create the legal planning and authority carrier for repo-wide high-risk source owner marker adoption while keeping the Element Validation Ledger canonical and markers as dev-only backlinks.`

Planned Runtime Delta: `None for Stage 2 setup. Future Workstream may add dev-only source-owner markers to selected high-risk source files, but those markers must not change executable behavior.`

User-Facing Delta: `None. Production UI must not show element numbers, marker IDs, source-owner labels, review badges, hover outlines, ledger tooltips, or Dev Toolkit review annotations.`

Source-Truth Delta: `Create the active branch authority record and this plan; update branch_records index, backlog, roadmap, and validation helper registry as compact pointer/status surfaces; preserve the historical candidate language required by current governance validation.`

State / Config / Schema Delta: `No production state, config, schema, persistence, telemetry, network, provider, model, memory, voice, shortcut, or installer delta. Future marker metadata remains source/dev-only.`

Validator / Helper Delta: `Stage 2 records validator planning for marker syntax, marker placement, marker-to-ledger consistency, high-risk coverage or not-applicable reasons, production UI exclusion, and future dev-only review-mode gating. Validator implementation remains pending USER approval for Workstream.`

Expected Changed Files / Surfaces: `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md, Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md, Docs/branch_records/index.md, Docs/feature_backlog.md, Docs/prebeta_roadmap.md, Docs/validation_helper_registry.md, and future Workstream-selected validators/source surfaces after approval.`

Workstream / Seam Map: `Seam 1 high-risk inventory; Seam 2 marker format and policy validation; Seam 3 ledger mapping and not-applicable reason model; Seam 4 limited high-risk marker insertion; Seam 5 marker coverage and production UI exclusion validation; Seam 6 Dev Toolkit Interface Review Mode disposition planning.`

Per-Seam Implementation Checklist: `Inventory high-risk source/proof surfaces; define compact marker syntax; map markers to canonical ledger rows; add markers only where useful; implement or update marker validators; prove production UI exclusion; record review-mode dispositions without runtime toolkit implementation unless separately approved.`

Per-Seam Validation Checklist: `Run branch governance, planning fixture validation, release body validation, governance efficiency validation, diff checks, compileall, marker syntax/coverage/ledger validators when implemented, production UI exclusion scans, and any directly affected helper validators.`

Per-Seam User-Facing Proof Checklist: `Stage 2 setup requires no screenshot/live/UTS proof. Future production-visible changes require focused visual proof and UTS or explicit USER waiver. Future dev-only review-mode UI must prove dev-only gating before acceptance.`

Future-Gated Items: `Future-gated and pending approval: marker insertion into product/runtime/proof-bearing source files, marker validator implementation, Dev Toolkit review-mode implementation, production runtime behavior, production UI changes, PR creation, merge, release/tag/artifact work, issue mutation, branch cleanup, FAM-007 work, Governance intake mutation, Compact-AI work, provider/model/memory/shortcut/installer work, AI Product work, and external telemetry parity.`

Approval-Boundary Audit: `USER approved Branch Readiness Stage 2 setup only. Workstream implementation approval is required before inserting markers, changing validators beyond planning, or touching runtime-adjacent source files.`

FAM / Shared-Surface Overlap Forecast: `FAM-006 is historical/merged and owns canonical historical ledger rows; FAM-007 is a separate worktree and provider lane; Governance is the standing intake lane; Compact-AI is separate. Future marker insertion may touch shared runtime/UI/proof surfaces and must run a Pre-Rebaseline Impact Audit if origin/main advances.`

Open Questions: `Whether Workstream should begin with inventory-only proof, a limited high-risk marker pilot, or broader marker adoption; whether Dev Toolkit review-mode remains planning-only or implementation scope.`

USER Planning Decisions: `USER approved Stage 1 analysis and Stage 2 setup. USER has not approved Workstream implementation, marker insertion, validator implementation, Dev Toolkit runtime, PR creation, merge, release, issue mutation, or cleanup.`

Plan Revision History: `v1 - created during Branch Readiness Stage 2 after origin/main 26bb76becd4089d2e451d44e969939f0f074371f, with No Active Branch main truth and recorded candidate feature/repo-wide-source-owner-marker-adoption.`

Plan-To-Implementation Traceability Table: `Stage 2 setup maps to this plan, the branch authority record, branch_records index, compact backlog/roadmap pointers, and validation helper registry planning. Future Workstream must update this field with marker inventory, marker additions, validator implementation, validation commands, and proof outcomes.`

Hardening Comparison Checklist: `H1 must compare implemented marker syntax, coverage, ledger mapping, not-applicable reasons, production UI exclusion, validator scope, dev-only review-mode boundaries, and unchanged runtime behavior against this plan.`

Live Validation Proof Or Waiver Checklist: `Live Validation is not required for setup-only source truth. If Workstream implements only static markers/validators, LV may use static validation proof or USER waiver. If dev-only UI or production-visible UI changes are admitted, focused visual proof and UTS or explicit waiver are required.`

PR Readiness Fold-Down / Retention Checklist: `PR Readiness must decide whether this plan remains as historical branch source truth, whether durable marker policy moves to development_rules or phase_governance, whether the active branch authority record becomes historical/no-active before merge, and whether backlog/roadmap return to compact No Active Branch truth.`

Release Readiness Public-Scope Translation Checklist: `Public release language must describe developer/source-traceability improvements only if there are no production runtime changes. It must not expose internal marker IDs, ledger IDs, element numbers, or governance jargon to end users.`

USER Planning Review: `Complete for Stage 2 setup; Workstream implementation approval remains pending.`

PR Fold-Down Packet: `Pending - no PR exists and PR creation remains unapproved.`

Runtime Implementation Approval: `Pending/Blocked - not granted for Workstream implementation, marker insertion, validator implementation, Dev Toolkit runtime, or production behavior changes.`
