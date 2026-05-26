# Branch Runtime Engineering Plan - FAM-006 Active Overlay Recording Runtime Foundation

Branch: `feature/fam-006-active-overlay-recording-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md`
Created From: `feature/fam-006-recording-profile-runtime-foundation` at `1f399003d2e6d13b34b567cd7f7900a709254bc9`
Current Plan Phase: `Branch Readiness Stage 2 setup`
Runtime Implementation Approval: `Blocked - Workstream Entry analysis and separate USER implementation approval are required before runtime mutation`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Active Overlay Recording Runtime Foundation`
Owning Branch: `feature/fam-006-active-overlay-recording-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md`
Current Phase: `Branch Readiness Stage 2 setup`
Branch Runtime Engineering Plan: `Corrected active-overlay-driven recording carrier setup and planning admission.`
Engineering Plan Status: `Accepted for Stage 2 setup; Workstream Entry pending USER approval`
Current Runtime Baseline: `FAM-006 Overlay Profile Runtime Foundation and Overlay Display Acceptance Foundation are released historical evidence. The profile-loaded Recording Profile Workstream route was rolled back by USER request and is preserved as historical receipt only.`
Branch Purpose: `Admit a corrected FAM-006 recording carrier where recording is driven by the active Overlay Profile membership rather than a separate loaded Recording Profile.`
Planned Runtime Delta: `None during Stage 2. Workstream Entry will analyze future runtime deltas for active-overlay recording target, HUD Overlay quick access, standalone Recording Settings, durable output contract, and validation/live proof.`
User-Facing Delta: `None during Stage 2. Future user-facing changes require USER implementation approval after Workstream Entry.`
Source-Truth Delta: `Add this active branch authority and branch plan; move the old Recording Profile branch from active authority to historical/rollback receipt posture; update compact backlog/roadmap pointers to this corrected carrier; preserve released Overlay Profile and Overlay Display evidence.`
State / Config / Schema Delta: `None during Stage 2. Future state/schema must target active Overlay Profile membership and recording settings without reintroducing profile-loaded Recording Profile membership unless USER explicitly re-approves it.`
Validator / Helper Delta: `No runtime validator/helper mutation during Stage 2 unless source-truth validators require pointer updates. Future validators must cover real user-level input, compact/default photo comparison, output-file proof when implemented, null/stress states, and boundary preservation.`
Expected Changed Files / Surfaces: `Docs/branch_records/index.md; Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md; Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md; Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/retirement_index.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `SLC-051 through SLC-055 are admitted for whole-package Workstream Entry analysis; first implementation seam is not selected until USER approves Workstream Entry.`
Per-Seam Implementation Checklist: `SLC-051 must name state/target surfaces; SLC-052 must name HUD Overlay card surfaces; SLC-053 must name standalone Recording Settings window surfaces; SLC-054 must name output-file contract surfaces; SLC-055 must name validator/helper/proof surfaces.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks when JavaScript changes, H1 checks, LV1 real-input proof where user-facing, compact/default photo comparison, null/stress proof, and regression proof for Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, and Overlay Display.`
Per-Seam User-Facing Proof Checklist: `Pending Workstream Entry. Any visible control/window/status must carry real user-level mouse/keyboard proof, hover/focus screenshots, compact/default screenshots, dirty/state transition proof where applicable, and UTS handoff criteria.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, old branch cleanup/deletion, and artifacts/raw evidence handling beyond approved review bundles.`
Approval-Boundary Audit: `Stage 2 setup only. The old Recording Profile Workstream was rolled back by USER request and receipt-complete on its historical carrier. This plan does not ratify runtime implementation.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. Future runtime seams may touch HUD Dashboard, HUD Overlay card, Overlay Profile, Overlay Display, Manage Monitors, Sensor Command Center, and visual validation helpers; Workstream Entry must forecast exact overlap before implementation.`
Open Questions: `Pending Workstream Entry analysis: first bounded seam, exact output file contract proposal, permanent HUD Overlay card placement, Recording Settings fields beyond folder path/open folder/Start/Stop, and whether actual recording execution belongs in this package or a later USER-approved seam.`
USER Planning Decisions: `USER clarified that recording should live in the HUD Overlay card, record active Overlay Profile membership, use lightweight quick access, use a compact standalone Recording Settings window, and avoid separate profile-loaded Recording Profile selection. USER approved Stage 2 setup for this corrected carrier from current FAM-006 rollback receipt HEAD.`
Plan Revision History: `v1 - Created during Branch Readiness Stage 2 setup after rollback of the profile-loaded Recording Profile Workstream route.`
Plan-To-Implementation Traceability: `Future implementation must start from this plan and map each SLC-051 through SLC-055 delta to changed files, validator/helper proof, H1 result, LV1/UTS proof, deferred boundaries, and commit evidence.`
Plan-To-Implementation Traceability Table: `Planned table owner is this branch plan: SLC-051 will trace active overlay target files and validators; SLC-052 will trace HUD Overlay card files and visual proof; SLC-053 will trace Recording Settings window files and real-input proof; SLC-054 will trace output contract files/helpers and readback proof; SLC-055 will trace validator/helper/LV1/UTS files and evidence. Actual changed files, commits, validation output, H1 result, LV1 artifacts, and UTS disposition must be filled or summarized before PR Readiness.`
Hardening Comparison Checklist: `Pending future Workstream implementation. H1 must compare actual behavior against active-overlay-driven recording vision, compact/default UI behavior, concept separation, output contract, and future-gated boundaries.`
Live Validation Proof Or Waiver Checklist: `Pending future Workstream implementation. LV1 must use the real user-facing launcher where feasible, real user-level mouse/keyboard input, focused screenshots/videos, compact/default stress, null/high-volume selectors, output-file proof where applicable, and pessimistic Codex visual review before UTS handoff.`
PR Readiness Fold-Down / Retention Checklist: `Future PR Readiness must decide what branch-plan details fold into branch record, family vision/dossier, workstream record, or retirement index.`
Release Readiness Public-Scope Translation Checklist: `Future Release Readiness must describe only implemented and validated user-facing active-overlay recording work; future-gated tray/export/provider/theme work must remain excluded.`
USER Planning Review: `Required through the Stage 2 USER branch-plan review packet and future Workstream Entry review bundle.`
PR Fold-Down Packet: `Pending future PR Readiness.`
Runtime Implementation Approval: `Blocked - runtime implementation requires Workstream Entry analysis and separate USER approval.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Active Overlay Recording Runtime Foundation`
Package Posture: `Admitted for Workstream Entry analysis`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-051` Active Overlay recording target foundation | Admitted | Define active Overlay Profile membership as the recording target while preserving Overlay Profile, Overlay Display, and Monitor Group separation. | Pending Workstream Entry |
| `SLC-052` HUD Overlay recording quick access and active-monitor transparency | Admitted | Plan lightweight HUD Overlay Start/Stop access and active monitored monitor transparency without tray/export/provider scope. | Pending Workstream Entry |
| `SLC-053` standalone Recording Settings window foundation | Admitted | Plan compact normal OS-level Recording Settings window behavior, folder path, open folder, Start/Stop parity, minimization/independent lifetime, and NDAI window styling. | Pending Workstream Entry |
| `SLC-054` durable recording output contract | Admitted | Propose graph/plot-ready output file contract and proof expectations before or alongside approved recording execution. | Pending Workstream Entry |
| `SLC-055` validation/live proof readiness | Admitted | Plan validators, helper proof, H1, LV1, photo comparison, UTS strategy, null/stress coverage, and future-gated boundary proof. | Pending Workstream Entry |

Single-Slice Package User Approval: `Not required - five concrete slices are admitted for analysis.`
Package Completion State: `Not started`

## Element-to-Phase Proof Matrix

Matrix Status: `Present`
USER Review Status: `Needs USER Decision`
Open Element Questions: `Queued`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md`
Element Validation Ledger Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AOR-001` | Active Overlay Profile recording target | Planned | SLC-051 will define how recording derives membership from the active Overlay Profile without adding a separate Recording Profile selector. | Workstream proof must assert active Overlay Profile membership drives target selection and that Overlay Profile state remains display-owned. | H1 must stress null active profile, switched active profile, deleted profile, high-volume profiles, and stale membership references. | LV1 required if user-visible target/status is added; otherwise state-only waiver must name validator proof. | UTS required for visible target/status; waived only for pure state-only proof. | Actual recording execution remains blocked until USER approves implementation scope. | Needs USER Decision | This plan |
| `AOR-002` | HUD Overlay card recording quick access | Planned | SLC-052 will plan lightweight Start Recording / Stop Recording affordance in the HUD Overlay card after Workstream approval. | Workstream proof must include button state, enabled/disabled state, active monitor transparency, and no tray/export/provider coupling. | H1 must stress compact/default layout, dirty/state transitions where relevant, and regression against Dashboard card controls. | LV1 must use real user-level mouse/keyboard input, before/after screenshots, compact/default photos, hover/focus proof, and pessimistic visual review. | UTS must include a user-facing item that asks USER to verify HUD Overlay card recording controls, active monitor transparency, compact/default visual correctness, and absence of tray/export/provider scope; any waiver must name why no visible runtime shipped. | Tray recording controls and recording execution are separate pending USER decisions unless explicitly admitted later. | Needs USER Decision | This plan |
| `AOR-003` | Active monitored monitors transparency | Planned | SLC-052 will plan which currently active monitors are shown under the selected Overlay Profile in the HUD Overlay card. | Workstream proof must include null monitors, hidden monitors, active/visible counts, and no Monitor Group mutation. | H1 must compare Dashboard, Manage Monitors, Overlay Profile, and Overlay Display behavior for regressions. | LV1 must capture focused card screenshots at default and compact sizes if visible. | UTS required if visible in Dashboard/HUD Overlay card. | Monitor Group configuration remains owned by Manage Monitors / Sensor Command Center. | Needs USER Decision | This plan |
| `AOR-004` | Standalone Recording Settings window | Planned | SLC-053 will plan an independent compact OS-level NDAI Recording Settings window that can remain open when Dashboard is closed/minimized. | Workstream proof must include launch, close/minimize, folder path, open folder, Start/Stop parity, focus/dirty guard if settings mutate, and no child-window dependency. | H1 must stress window lifetime, compact minimum size, real resize behavior, close/minimize, save/discard/cancel if dirty state exists, and no Dashboard input bleed-through. | LV1 must use visible real mouse movements/clicks, keyboard input where relevant, photos before/after every user-facing state, and compact/default comparison. | UTS required because this is a user-facing window. | Advanced bulky settings should move behind secondary surfaces only after USER approval. | Needs USER Decision | This plan |
| `AOR-005` | Durable recording output contract | Planned | SLC-054 will propose and, if approved, implement or validate the output file contract needed for future graph/plot workflows. | Workstream proof must include schema/header/row determinism, timestamp/value/source identity, path handling, null/no-data behavior, and parse/readback proof. | H1 must stress file path errors, long recordings, high-volume sensors, interrupted write, and compatibility with future graph/plot usage. | LV1 requires user-facing proof only if output settings or recording execution are visible; otherwise helper proof can satisfy file-contract validation. | UTS required if a user can create/select/open output files; otherwise Workstream/H1 proof may be sufficient. | Export/share/import remains a future package and is not authorized by an output contract alone. | Needs USER Decision | This plan |
| `AOR-006` | Recording execution | Future | Not implemented by Stage 2. Workstream Entry must decide whether actual Start/Stop execution belongs in this package or needs a separate USER approval seam. | Boundary proof must show no runtime recording execution is added before USER approval. | H1 must confirm no fake recording or unauthorized file writes. | LV1 absence proof if visible buttons exist without execution; otherwise future branch owns execution proof. | USER acceptance belongs to the approved implementation seam that admits execution. | Boundary keeps recording execution out of current release gating until USER grants explicit implementation approval for file-writing/runtime recording behavior in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-007` | Tray recording controls | Future | No implementation in this package unless USER separately approves tray scope. | Boundary proof must show no tray Start/Stop control was added. | H1 must confirm tray behavior unchanged. | LV1 absence proof only if visible UI could imply tray controls. | Future USER acceptance belongs to a tray-controls branch or approved scope revision. | Boundary keeps tray recording controls out of current release gating until USER grants a tray-control scope decision in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-008` | Export/share recording output | Future | No export/share/import implementation in this package. | Boundary proof must show no export/share UI or workflow was added. | H1 must confirm output contract does not become export/share behavior. | LV1 absence proof only if user-facing UI could imply export/share. | Future USER acceptance belongs to export/share branch or approved scope revision. | Boundary keeps export/share/import out of current release gating until USER grants an export/share scope decision in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-009` | Provider/model integration | Future | No provider/model/memory work in this package. | Boundary proof must show active-overlay recording has no provider/model dependency. | H1 must confirm FAM-007 boundaries remain unchanged. | LV1 absence proof only if UI could imply provider/model integration. | Future USER acceptance belongs to FAM-007 or other approved branch. | Boundary keeps provider/model/memory integration out of current release gating until USER grants provider/model scope in FAM-007 or another approved carrier. | Deferred With Waiver | This plan |
| `AOR-010` | Validation/live proof governance for recording surfaces | Planned | SLC-055 will update validators/helpers only as required by implemented runtime seams. | Workstream proof must include source-truth validators, HUD validators, internal sandbox, validation suite, JS checks when changed, output-file helper proof when relevant, and matrix coverage. | H1 must be pessimistic and compare planned behavior to actual code, screenshots, and helper outputs. | LV1 must use real user-facing launcher where feasible, real cursor movement/clicks, compact/default photo comparison, and explicit blocker if real input is impossible. | UTS handoff required after LV1 for user-facing changes unless explicitly waived. | Validator fallbacks must not replace real input without USER-visible blocker/digest. | Needs USER Decision | This plan |

## Branch Change Intent Ledger

### Changed Surface: Docs/branch_records/index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Replace the active FAM-006 Recording Profile rollback carrier pointer with this active-overlay-driven recording carrier pointer and move the old Recording Profile record to historical receipt posture.`
- Why This File Was Touched: `Branch Readiness Stage 2 is the legal carrier for active branch authority admission and rollback carrier fold-down.`
- Owned Behavior / Fact Class: `Branch authority routing.`
- Canonical Owner / Source Owner: `Docs/branch_records/index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium if origin/main advances before PR.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve standing non-FAM-006 active pointers, preserve incoming current-main governance context, keep this active branch pointer in Active Branch Authority Records, and keep the old Recording Profile branch pointer in Historical Branch Authority Records only.`
- Rebaseline Handling: `Run the pre-reconciliation overlap audit before any future current-main reconciliation if origin/main advances.`
- Validation Proof: `Branch governance validation, worktree-confinement gate, release-readiness health gate, branch-readiness planning fixture validation, source-owner marker validation, FAM-006 validators, runtime-fam006 validation suite, and compileall.`
- Fallback Evidence: `Use this branch plan and active branch authority record as branch-owned intent evidence; compatibility still requires preserving current-main governance context and validating after reconciliation.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup for this corrected carrier; no waiver authorizes runtime implementation or old branch deletion.`
- Fold-Down Target: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md remains historical rollback receipt; this branch becomes active FAM-006 planning authority.`

### Changed Surface: Docs/feature_backlog.md

- Surface Class: `governance/source-truth`
- Change Intent: `Update the compact FAM-006 status and canonical detail owner from the rollback carrier to the active-overlay-driven recording carrier.`
- Why This File Was Touched: `The backlog compact pointer must route active FAM-006 planning to the current branch authority.`
- Owned Behavior / Fact Class: `Feature-family status and canonical pointer routing.`
- Canonical Owner / Source Owner: `Docs/feature_backlog.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium if origin/main advances before PR.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve compact family status, historical released Overlay evidence, rollback receipt context, and route active detail owner to this branch.`
- Rebaseline Handling: `If main overlaps, preserve current-main family statuses and this FAM-006 active pointer.`
- Validation Proof: `Branch readiness planning fixture validation and FAM-006 HUD validators must pass.`
- Fallback Evidence: `Use this plan and branch record as FAM-006 active planning evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup for the corrected carrier.`
- Fold-Down Target: `Future PR Readiness decides durable family dossier or branch-record retention.`

### Changed Surface: Docs/prebeta_roadmap.md

- Surface Class: `governance/source-truth`
- Change Intent: `Update FAM-006 public milestone pointer to this active-overlay-driven recording carrier while preserving historical Overlay Display and rollback receipt context.`
- Why This File Was Touched: `Roadmap compact pointer must not route active recording planning to the rolled-back profile-loaded carrier.`
- Owned Behavior / Fact Class: `Pre-Beta milestone pointer routing.`
- Canonical Owner / Source Owner: `Docs/prebeta_roadmap.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium if origin/main advances before PR.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve current-main roadmap family statuses, released FAM-006 evidence, rollback receipt context, and this active carrier pointer.`
- Rebaseline Handling: `If main overlaps, preserve current-main release-stage context and this branch-local FAM-006 active pointer.`
- Validation Proof: `Roadmap/backlog pointer validators and branch governance validation must pass.`
- Fallback Evidence: `Use this plan and branch record as active FAM-006 recording carrier evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup for this corrected carrier.`
- Fold-Down Target: `Future PR Readiness decides compact roadmap fold-down text.`

### Changed Surface: Docs/branch_plans/retirement_index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Retire the old Recording Profile branch plan from active planning posture and set this active branch plan as current active plan posture.`
- Why This File Was Touched: `The old carrier remains as rollback receipt only; the active plan pointer must route to this corrected carrier.`
- Owned Behavior / Fact Class: `Branch plan lifecycle and active plan posture.`
- Canonical Owner / Source Owner: `Docs/branch_plans/retirement_index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low to Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Keep historical plan rows, add old Recording Profile plan as retired, and point Active Plan Posture to this plan.`
- Rebaseline Handling: `Preserve incoming current-main retired-plan rows and this active FAM-006 posture.`
- Validation Proof: `Branch readiness planning fixture validation must pass.`
- Fallback Evidence: `Use this plan, active record, and retirement index row as lifecycle evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup and did not authorize old branch deletion.`
- Fold-Down Target: `Future PR Readiness may retire this plan after merge/release.`

### Changed Surface: Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md

- Surface Class: `governance/source-truth`
- Change Intent: `Fold the old Recording Profile branch authority from active planning posture into historical rollback receipt posture.`
- Why This File Was Touched: `Stage 2 must preserve rollback receipt evidence while preventing stale active authority drift.`
- Owned Behavior / Fact Class: `Historical branch receipt and rollback authorization evidence.`
- Canonical Owner / Source Owner: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO`
- Overlap Risk: `Low`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve exact rollback authorization text and released evidence, but mark the record historical/rollback receipt only.`
- Rebaseline Handling: `Preserve source record as historical receipt if current-main overlaps.`
- Validation Proof: `Branch governance validation must not see this old record as active.`
- Fallback Evidence: `Old record remains durable rollback receipt.`
- USER Decision / Waiver: `USER approved Stage 2 setup to fold this branch into historical/rollback receipt posture.`
- Fold-Down Target: `Historical branch authority records.`

### Changed Surface: Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md

- Surface Class: `governance/source-truth`
- Change Intent: `Fold the old Recording Profile branch plan from active planning posture into historical rollback receipt posture.`
- Why This File Was Touched: `The profile-loaded Recording Profile plan is not the active implementation carrier after USER vision correction.`
- Owned Behavior / Fact Class: `Historical branch-plan receipt.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO`
- Overlap Risk: `Low`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve rollback receipt and withdrawn route evidence; do not route future Workstream implementation through this plan.`
- Rebaseline Handling: `Preserve as retired branch plan.`
- Validation Proof: `Branch readiness planning fixture validation and retirement index must pass.`
- Fallback Evidence: `Old plan remains historical rollback receipt.`
- USER Decision / Waiver: `USER approved Stage 2 setup to fold this plan into historical/rollback receipt posture.`
- Fold-Down Target: `Docs/branch_plans/retirement_index.md`

### Changed Surface: Docs/development_rules.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main USER review gate governance and add branch-local clarification that Workstream Entry return digests must explicitly state whether the Desktop review folder and exported ZIP were refreshed, reused as current, waived, or blocked after current-main reconciliation.`
- Why This File Was Touched: `The branch needs a non-ambiguous Workstream Entry handoff rule so a stale Desktop review folder or FAM-006.zip cannot be treated as implied-green after reconciliation.`
- Owned Behavior / Fact Class: `Execution governance for runtime Branch Readiness and Workstream Entry.`
- Canonical Owner / Source Owner: `Docs/development_rules.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High if origin/main carries newer FAM-007 review-gate governance.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 review-gate governance, preserve FAM-006 USER Review Packet Finding governance, and require a named Desktop review folder / ZIP refresh digest in Workstream Entry return packets when implementation approval follows a packet refresh or current-main reconciliation.`
- Rebaseline Handling: `During current-main reconciliation, preserve current-main governance context and this FAM-006 clarification without accepting another branch as FAM-006 identity.`
- Validation Proof: `Branch governance validation and branch readiness planning fixture validation must pass.`
- Fallback Evidence: `This branch plan records the exact overlap intent before current-main reconciliation.`
- USER Decision / Waiver: `USER explicitly requested governance repair so the desktop review folder and ZIP refresh digest is not omitted again.`
- Fold-Down Target: `Docs/development_rules.md and branch plan review governance.`

### Changed Surface: Docs/phase_governance.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming phase-gate governance and add explicit Workstream Entry digest language requiring review folder and exported ZIP freshness/refresh status after packet refreshes or current-main reconciliation.`
- Why This File Was Touched: `Phase governance owns the Workstream Entry and USER Branch Plan Review Gate contracts.`
- Owned Behavior / Fact Class: `Phase gate and blocker behavior.`
- Canonical Owner / Source Owner: `Docs/phase_governance.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High if current-main phase governance changed during FAM-007.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming phase gate additions while retaining the FAM-006 requirement that Workstream Entry cannot return implementation approval unless it reports Desktop folder and exported ZIP refresh/reuse/waiver/blocker status.`
- Rebaseline Handling: `Reconcile additively; do not remove incoming FAM-007 phase gate context.`
- Validation Proof: `Branch governance validation must pass.`
- Fallback Evidence: `This branch plan records the overlap intent before current-main reconciliation.`
- USER Decision / Waiver: `USER explicitly requested governance repair for the omitted desktop folder and ZIP digest.`
- Fold-Down Target: `Docs/phase_governance.md.`

### Changed Surface: Docs/validation_helper_registry.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming helper registry updates and clarify helper/validator ownership for USER review bundle refresh and digest requirements.`
- Why This File Was Touched: `The helper registry owns reusable helper expectations for dev/orin_user_review_bundle.py and branch governance validation.`
- Owned Behavior / Fact Class: `Validation helper ownership and reuse contract.`
- Canonical Owner / Source Owner: `Docs/validation_helper_registry.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High if current-main helper registry changed.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming helper registry context and add/keep the requirement that review bundle helpers prove both the Desktop folder and exported ZIP are current, with return digests naming refresh/reuse/waiver/blocker status.`
- Rebaseline Handling: `Reconcile additively with current-main helper entries.`
- Validation Proof: `Branch governance validation and branch readiness planning fixture validation must pass.`
- Fallback Evidence: `This branch plan records the overlap intent before current-main reconciliation.`
- USER Decision / Waiver: `USER explicitly requested governance repair for the omitted desktop folder and ZIP digest.`
- Fold-Down Target: `Docs/validation_helper_registry.md.`

### Changed Surface: dev/orin_branch_governance_validation.py

- Surface Class: `validator/helper`
- Change Intent: `Preserve incoming validator updates and, if needed, enforce the clarified USER review packet digest rule for Desktop folder and exported ZIP freshness.`
- Why This File Was Touched: `The branch governance validator owns machine-checkable review-gate phrases and branch-plan review fixtures.`
- Owned Behavior / Fact Class: `Governance validation.`
- Canonical Owner / Source Owner: `dev/orin_branch_governance_validation.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High if current-main validator logic changed.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 validator fixes, preserve FAM-006 USER Review Packet Finding checks, and keep or add checks for review folder / exported ZIP digest language where source truth makes it machine-checkable.`
- Rebaseline Handling: `Reconcile validator logic after merge, then run branch governance and fixture validation.`
- Validation Proof: `Branch governance validation and branch readiness planning fixture validation must pass.`
- Fallback Evidence: `This branch plan records the overlap intent before current-main reconciliation.`
- USER Decision / Waiver: `USER explicitly requested governance repair for the omitted desktop folder and ZIP digest.`
- Fold-Down Target: `dev/orin_branch_governance_validation.py and source-truth validation fixtures if changed.`

### Changed Surface: dev/orin_user_review_bundle.py

- Surface Class: `validator/helper`
- Change Intent: `Preserve incoming review-bundle helper fixes and keep the helper responsible for overwriting the Desktop review folder/ZIP from current branch HEAD when a packet refresh is required.`
- Why This File Was Touched: `The helper owns creation and stale-guard proof for the stable Desktop review folder and exported FAM zip.`
- Owned Behavior / Fact Class: `USER review Desktop bundle generation.`
- Canonical Owner / Source Owner: `dev/orin_user_review_bundle.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High if current-main helper behavior changed.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming helper behavior, keep stable Desktop review folder and exported ZIP stale guards, and require return packets to name whether the helper refreshed or reused the folder and ZIP.`
- Rebaseline Handling: `Reconcile helper changes after merge, then regenerate/re-check review packet only when source truth requires it.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, and compileall must pass.`
- Fallback Evidence: `This branch plan records the overlap intent before current-main reconciliation.`
- USER Decision / Waiver: `USER explicitly requested governance repair for the omitted desktop folder and ZIP digest.`
- Fold-Down Target: `dev/orin_user_review_bundle.py and validation helper registry.`

## USER Branch Plan Review Gate

USER Branch Plan Review: Required - Stage 2 creates a USER branch-plan review packet and future Workstream Entry must present a full readable implementation plan before runtime work begins.
Review Status: Needs USER Decision - Workstream Entry analysis remains pending after Stage 2 setup.
Desktop Review Bundle: `C:\Users\anden\OneDrive\Desktop\Nexus USER Review\FAM-006`
USER Review Packet Finding: Required before implementation approval - Workstream Entry must load and digest `START_HERE.md`, `USER_BRANCH_PLAN_REVIEW.md`, and `C:\Users\anden\OneDrive\Desktop\Nexus USER Review\FAM-006.zip`; compare packet source HEAD and review zip source HEAD with current branch HEAD; then report loaded, stale, missing, waived, or blocking status before SLC-051 implementation can begin. The return digest must also include `Desktop Review Folder / ZIP Refresh Digest:` naming whether the folder and exported zip were refreshed from current HEAD, reused because they already match current HEAD, waived by exact USER/source-truth text, or blocked with the exact stale/missing artifact.
Plain-Language Branch Goal: Establish the corrected FAM-006 recording branch where recording is driven by the active Overlay Profile instead of a separate Recording Profile.
Planned User-Facing Outcome: No user-facing runtime change in Stage 2; future user-facing outcome is lightweight HUD Overlay recording access, transparent active monitor target, and a compact standalone Recording Settings window after later approval.
Visual / Behavioral Description: Future recording should be visible from the HUD Overlay card, show what active overlay membership will be recorded, and let the user open a small NDAI Recording Settings window that behaves like a normal OS window.
Implementation Breakdown: Stage 2 admits source truth only; Workstream Entry will analyze SLC-051 target foundation, SLC-052 HUD Overlay quick access/transparency, SLC-053 Recording Settings window, SLC-054 output contract, and SLC-055 validation/live proof readiness.
Element-to-Phase Proof Matrix: Present in this plan for AOR-001 through AOR-010.
Hardening Plan: Future H1 must pressure-test active overlay membership, Dashboard/HUD Overlay behavior, standalone settings window behavior, output contract, concept separation, compact/default UI, and future-gated boundaries.
Live Validation / UTS Plan: Future LV1 must use real user-level input, visible cursor movement/clicks, compact/default screenshots, focused per-element screenshots, output-file proof where applicable, and UTS handoff or explicit waiver.
Open USER Questions: Workstream Entry must determine first bounded seam, output file contract recommendation, exact Recording Settings fields, permanent HUD Overlay card arrangement, and whether actual recording execution is in this package or a later package.
Codex Recommendations: Analyze the whole SLC-051 through SLC-055 package before implementation; keep tray, export/share, provider/model, theme, and FAM-007 work out of this carrier unless USER separately approves a scope revision.
Alternatives / Tradeoffs: The prior profile-loaded Recording Profile route is preserved only as historical rollback receipt because it did not match the clarified USER recording vision.
Accepted Scope: Accepted scope is Branch Readiness Stage 2 setup, source-truth admission, old carrier fold-down, Stage 2 review packet creation, validation, commit, and push.
Deferred Scope: Deferred scope is runtime implementation, Workstream Entry, Workstream implementation, recording execution, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge, release, issue mutation, artifacts/raw evidence handling beyond approved review packet, sibling-worktree mutation, old branch cleanup/deletion, and Governance mutation.
Rejected Scope: Requiring users to load a separate Recording Profile before recording sensors is rejected for this future recording path unless USER explicitly re-approves it.
Exact USER Decision Needed: USER may approve Workstream Entry analysis for this branch after Stage 2 setup validation and review packet are green.
Implementation Approval: Blocked - no runtime mutation is approved by this Stage 2 review gate.

## Workstream Entry Whole-Package Analysis Requirements

Required Workstream Entry outputs:

- all admitted slices/seams from SLC-051 through SLC-055
- whole-package completion strategy
- first bounded seam recommendation
- seam dependency map
- future-gated or non-included scope
- preservation surfaces for Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, and Overlay Display
- validation plan and helper requirements
- Hardening H1 expectations
- Live Validation LV1 expectations
- visual/user-facing proof requirements
- output-file proof requirements where applicable
- UTS handoff criteria
- exact implementation approval text

## Next Legal Phase

Next Legal Phase: `Workstream Entry analysis`
Exact USER Decision Needed: `Approve Workstream Entry analysis for FAM-006 Active Overlay Recording Runtime Foundation in C:\Nexus Worktrees\FAM-006 on feature/fam-006-active-overlay-recording-runtime-foundation. This approval covers analysis only: inspection of source truth and runtime surfaces, analysis of the admitted active-overlay-driven recording package from SLC-051 through SLC-055, selection of the first bounded implementation seam, definition of affected files, validators, helpers, source-truth updates, proof requirements, USER-facing proof requirements, and return of the first implementation approval packet. It does not approve runtime implementation, Workstream implementation, recording execution, tray recording controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge to main, release, issue mutation, artifacts/raw evidence handling beyond approved Workstream Entry review materials, sibling-worktree mutation, old branch cleanup/deletion, or Governance worktree mutation.`
