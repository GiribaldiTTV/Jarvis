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

### Changed Surface: Docs/branch_plans/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main FAM-007 Dev/Owner Skeleton Readiness branch-plan fold-down and source-truth context during FAM-006 current-main reconciliation.`
- Why This File Was Touched: `The FAM-006 branch carries historical context from earlier main states, and origin/main now includes FAM-007 PR #218 fold-down/source-truth updates that overlap this file before FAM-006 can reconcile to current main.`
- Owned Behavior / Fact Class: `FAM-007 historical merged-unreleased branch-plan receipt and public/private readiness traceability.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve incoming current-main FAM-007 fold-down/source-truth context, do not convert this FAM-007 plan into FAM-006 active authority, and keep FAM-006 active-overlay-driven recording authority in this FAM-006 branch plan and record.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main FAM-007 historical/fold-down updates for this file while preserving FAM-006 branch identity, USER_BRANCH_PLAN_REVIEW.md response/digest governance repair, and active-overlay-driven recording carrier state.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, runtime-fam006 validation suite recommendation, source-owner marker validation, and compileall must pass before current-main reconciliation can resume.`
- Fallback Evidence: `origin/main@73b4905cc5e6c626fae56ffd83f9df6c25e116a4 includes FAM-007 fold-down/source-truth context from PR #219 and PR #218 historical evidence; this FAM-006 branch plan remains the active owner for FAM-006 current carrier decisions only.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair to preserve incoming FAM-007 fold-down/source-truth context while keeping FAM-006 active-overlay recording as the current carrier.`
- Fold-Down Target: `FAM-007 historical/fold-down source truth remains owned by the FAM-007 branch plan and current-main history; this FAM-006 ledger entry is reconciliation intent evidence only.`

### Changed Surface: Docs/branch_records/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main FAM-007 Dev/Owner Skeleton Readiness branch-authority fold-down and historical receipt context during FAM-006 current-main reconciliation.`
- Why This File Was Touched: `The FAM-006 branch has branch-history overlap with FAM-007 authority files, and origin/main now carries the FAM-007 PR #218 historical merged-unreleased authority receipt that must not be lost during FAM-006 reconciliation.`
- Owned Behavior / Fact Class: `FAM-007 historical merged-unreleased branch authority receipt, PR #218 evidence, and public/private readiness boundary record.`
- Canonical Owner / Source Owner: `Docs/branch_records/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve incoming current-main FAM-007 historical authority receipt and do not treat the FAM-007 branch as active FAM-006 authority; keep FAM-006 active branch authority in Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main FAM-007 historical/fold-down updates for this file while preserving FAM-006 rollback receipt context, active-overlay-driven recording carrier state, and USER_BRANCH_PLAN_REVIEW.md response/digest gate.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, runtime-fam006 validation suite recommendation, source-owner marker validation, and compileall must pass before current-main reconciliation can resume.`
- Fallback Evidence: `origin/main@73b4905cc5e6c626fae56ffd83f9df6c25e116a4 contains the FAM-007 fold-down/source-truth receipt; this FAM-006 branch record remains separate and continues to own active FAM-006 carrier truth.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair to preserve incoming FAM-007 fold-down/source-truth context while keeping FAM-006 active-overlay recording as the current carrier.`
- Fold-Down Target: `FAM-007 historical branch authority receipt remains owned by the FAM-007 branch record and current-main history; this FAM-006 ledger entry is reconciliation intent evidence only.`

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
- Change Intent: `Preserve and enforce existing USER review packet / Desktop bundle obligations while this branch carries FAM-006 packet-proof hardening.`
- Why This File Was Touched: `The active branch exposed that existing review-packet governance could be missed operationally, so the branch hardened validator/helper proof without changing the underlying governance owner.`
- Owned Behavior / Fact Class: `Development workflow guardrails for USER review packet handling, validation proof, and phase handoff hygiene.`
- Canonical Owner / Source Owner: `Docs/development_rules.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main governance/FAM-007 changes overlap this shared rules file.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main governance context, preserve existing USER review packet requirements, and keep any branch-local FAM-006 wording limited to enforcement/proof rather than duplicate policy ownership.`
- Rebaseline Handling: `During current-main reconciliation, accept compatible current-main wording and retain the requirement that required USER review packets are either refreshed and digested with folder/zip proof or explicitly waived/blocked.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, and source-owner marker validation must pass after reconciliation.`
- Fallback Evidence: `Docs/Main.md, Docs/phase_governance.md, Docs/branch_plans/README.md, and validation helper registry already own the USER review packet rule; this ledger records why shared development rules may overlap.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this file before current-main reconciliation; no waiver permits omitting the USER review packet or ZIP proof.`
- Fold-Down Target: `Shared governance remains in Docs/development_rules.md; branch-local receipt folds into this branch record/plan at PR Readiness.`

### Changed Surface: Docs/phase_governance.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve the canonical phase gate requiring Workstream Entry USER review packet digestion and keep the active branch aligned with existing review-packet blocker semantics.`
- Why This File Was Touched: `This branch depends on the existing Workstream Entry USER Branch Plan Review Gate and needs current-main reconciliation to preserve that gate while merging incoming FAM-007 governance context.`
- Owned Behavior / Fact Class: `Canonical phase transition and blocker rules for Workstream Entry, review packets, and implementation approval.`
- Canonical Owner / Source Owner: `Docs/phase_governance.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main phase-governance repairs overlap USER review packet or FAM-007 phase-gate wording.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming phase-governance improvements, preserve existing USER Review Packet Finding blockers, and reject duplicate branch-local policy that weakens or obscures the canonical gate.`
- Rebaseline Handling: `Merge current-main phase-gate context as authority while keeping this branch's review-packet proof hardening compatible with the canonical Workstream Entry gate.`
- Validation Proof: `Branch governance validation, release-readiness health gate, branch readiness planning fixture validation, and runtime-fam006 validation suite must pass.`
- Fallback Evidence: `Existing phase governance already names START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, exported zip, source HEAD comparison, stale/not-digested blockers, and waiver/blocker disposition.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this file; no waiver authorizes Workstream implementation without the review packet finding.`
- Fold-Down Target: `Docs/phase_governance.md remains the canonical phase owner; branch-local proof folds down through PR Readiness.`

### Changed Surface: Docs/validation_helper_registry.md

- Surface Class: `governance/source-truth`
- Change Intent: `Record the reusable helper/validator responsibilities for concrete USER review packet folder and ZIP proof.`
- Why This File Was Touched: `This branch hardened dev/orin_user_review_bundle.py and dev/orin_branch_governance_validation.py so review packet proof is machine-visible instead of narrative-only.`
- Owned Behavior / Fact Class: `Validation helper registry ownership for USER review Desktop bundle helper and governance validator behavior.`
- Canonical Owner / Source Owner: `Docs/validation_helper_registry.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main helper registry changes overlap FAM-007 helper ownership or review-bundle helper wording.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming helper registry rows, preserve USER review bundle helper ownership, and keep the helper requirement that START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, exported zip, stale guard, and USER Review Packet Finding are generated/validated.`
- Rebaseline Handling: `During current-main reconciliation, retain both incoming helper registry context and this branch's stricter PASS-finding / zip validation helper responsibilities.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, source-owner marker validation, and compileall must pass.`
- Fallback Evidence: `dev/orin_user_review_bundle.py and dev/orin_branch_governance_validation.py contain the concrete enforcement; registry text is ownership traceability.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this file; no waiver permits treating helper output as optional when a USER review packet is required.`
- Fold-Down Target: `Docs/validation_helper_registry.md remains shared helper registry; branch proof folds into PR Readiness record.`

### Changed Surface: dev/orin_branch_governance_validation.py

- Surface Class: `validator/helper`
- Change Intent: `Enforce that USER Branch Plan Review Gate findings prove concrete Desktop review packet and ZIP freshness instead of accepting vague finding text.`
- Why This File Was Touched: `The branch exposed an operational miss where an existing mandatory review-packet rule was not performed; validator hardening closes that enforcement gap.`
- Owned Behavior / Fact Class: `Machine-checkable governance validation for USER Review Packet Finding substance.`
- Canonical Owner / Source Owner: `dev/orin_branch_governance_validation.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main validator changes overlap FAM-007 packet parser or review gate checks.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming validator fixes and retain the stricter requirement that USER Review Packet Finding names START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, exported zip, Source HEAD/current branch HEAD freshness, and loaded/digested or waiver/blocker status.`
- Rebaseline Handling: `Merge current-main validator improvements first, then reapply only the minimal FAM-006 review-packet finding substance checks if needed.`
- Validation Proof: `Branch governance validation and branch readiness planning fixture validation must pass after reconciliation; compileall must pass for syntax.`
- Fallback Evidence: `Existing fixture validation already checks missing USER Review Packet Finding; this branch adds substance requirements for vague findings.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this validator before current-main reconciliation.`
- Fold-Down Target: `Shared validator remains reusable; PR Readiness records the branch-local hardening result.`

### Changed Surface: dev/orin_user_review_bundle.py

- Surface Class: `validator/helper`
- Change Intent: `Make the USER review Desktop bundle helper generate, validate, and print concrete folder/ZIP review packet proof.`
- Why This File Was Touched: `The helper is the reusable path for creating START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, and the uploadable ZIP; this branch needs the helper to fail if that proof is absent or stale.`
- Owned Behavior / Fact Class: `Reusable USER review bundle generation and stale-guard validation behavior.`
- Canonical Owner / Source Owner: `dev/orin_user_review_bundle.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main helper changes overlap FAM-007 review-bundle helper behavior.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming helper improvements, preserve stable Desktop review root and ZIP behavior, and retain validation that exported ZIP contains START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, stale-guard proof, and USER Review Packet Finding PASS for the current Source HEAD.`
- Rebaseline Handling: `During current-main reconciliation, merge helper changes carefully and rerun helper/validator syntax plus governance validation before claiming green.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, source-owner marker validation, and compileall must pass.`
- Fallback Evidence: `Docs/validation_helper_registry.md owns helper responsibility; START_HERE.md carries the packet proof after helper execution.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this helper before current-main reconciliation; no waiver authorizes stale ZIP output.`
- Fold-Down Target: `Reusable helper remains shared; branch-specific proof is recorded in the review packet and PR Readiness closeout.`

## USER Branch Plan Review Gate

USER Branch Plan Review: Required - Stage 2 creates a USER branch-plan review packet and future Workstream Entry must present a full readable implementation plan before runtime work begins.
Review Status: Accepted by USER - USER accepted the active-overlay-driven recording end-state direction and clarified that USER_BRANCH_PLAN_REVIEW.md is an end-state/possibility-space decision ballot, not a per-slice decision packet.
Contract Status: Pending USER Confirmation - Codex revised this review into the closed-loop USER Branch Plan Contract; USER must confirm the revised contract or explicitly waive it before SLC-051 implementation approval is legal.
Contract Version / Revision: v2 - Closed-loop USER Branch Plan Contract revision after USER clarified that the review must drive end-state/possibility-space decisions and implementation constraints before runtime work.
Desktop Review Bundle: `C:\Users\anden\OneDrive\Desktop\Nexus USER Review\FAM-006`
USER Review Packet Finding: Required before implementation approval - Workstream Entry must load and digest `START_HERE.md`, `USER_BRANCH_PLAN_REVIEW.md`, and `C:\Users\anden\OneDrive\Desktop\Nexus USER Review\FAM-006.zip`; compare packet source HEAD and review zip source HEAD with current branch HEAD; then report loaded, stale, missing, waived, or blocking status before SLC-051 implementation can begin.
Plain-Language Branch Goal: Establish the corrected FAM-006 recording branch where recording is driven by the active Overlay Profile instead of a separate Recording Profile.
What Will I Actually See, And Where Will I See It?: USER should eventually see a compact Recording area inside the existing HUD Overlay card with a Recording Target / Active Recording Target label, the active Overlay Profile name, a concise active target summary, and an inactive/future-gated posture before recording execution exists; later, USER should see a compact standalone NDAI Recording Settings window for folder path, open-folder access, output naming/location, and simple recording settings.
Planned User-Facing Outcome: No user-facing runtime change in Stage 2; future user-facing outcome is lightweight HUD Overlay recording access, transparent active monitor target, and a compact standalone Recording Settings window after later approval.
End-State Vision: The completed active-overlay recording foundation should let USER understand recording from the HUD Overlay card as part of the overlay they already use: the card explains which active Overlay Profile members would be recorded, later approved controls provide lightweight access, and a compact standalone Recording Settings window handles path/settings without becoming a Dashboard child window.
Visual / Behavioral Description: Future recording should be visible from the HUD Overlay card, show what active overlay membership will be recorded, and let the user open a small NDAI Recording Settings window that behaves like a normal OS window.
Visual / Functional Walkthrough: USER starts at the Dashboard HUD Overlay card, sees the active Overlay Profile and recording target preview, verifies the active monitored members that would be recorded, then later opens a compact Recording Settings window for folder/path settings while recording execution and file writing remain separately approved.
Surface Map: Primary surface is the HUD Overlay card; supporting surfaces are Dashboard, Overlay Profile, Overlay Display, Manage Monitors, Sensor Command Center, the future standalone Recording Settings window, future graph/plot-ready output files, and explicitly future-gated tray/export/provider/theme/FAM-007 surfaces.
Implementation Breakdown: Stage 2 admits source truth only; Workstream Entry will analyze SLC-051 target foundation, SLC-052 HUD Overlay quick access/transparency, SLC-053 Recording Settings window, SLC-054 output contract, and SLC-055 validation/live proof readiness.
Element-to-Phase Proof Matrix: Present in this plan for AOR-001 through AOR-010.
Hardening Plan: Future H1 must pressure-test active overlay membership, Dashboard/HUD Overlay behavior, standalone settings window behavior, output contract, concept separation, compact/default UI, and future-gated boundaries.
Live Validation / UTS Plan: Future LV1 must use real user-level input, visible cursor movement/clicks, compact/default screenshots, focused per-element screenshots, output-file proof where applicable, and UTS handoff or explicit waiver.
Open USER Questions: Workstream Entry must determine first bounded seam, output file contract recommendation, exact Recording Settings fields, permanent HUD Overlay card arrangement, and whether actual recording execution is in this package or a later package.
USER Design Review Questions: Needs USER Decision - USER must review the generated `USER_BRANCH_PLAN_REVIEW.md` end-state, possibility space, HUD Overlay card concept, Recording Settings direction, output planning posture, Native Log Loader future-planning status, and any desired revisions before bounded Workstream implementation begins. Slice/seam details are background implementation staging, not the main USER decision surface.
Codex Recommendations: Accept the active-overlay-driven recording end-state first: recording lives in the HUD Overlay card, derives target membership from the active Overlay Profile, shows what would be recorded before execution exists, plans a compact standalone Recording Settings window, and keeps tray/export/provider/theme/FAM-007 work out unless USER separately approves a scope revision.
Implementation Options: Recommended option is Target Preview First for the end-state because the HUD Overlay card should explain what would be recorded before controls or file writing exist; alternate options are a disabled future-gated Start/Stop preview affordance, a Settings-window-first direction, or a USER-authored end-state revision before implementation.
Recommended Direction: Codex recommends Target Preview First as the product direction, not as a USER slice decision: establish an understandable active Overlay Profile recording target experience before visible controls, settings windows, output files, or recording execution rely on it.
Why This Fits The Nexus Vision: This direction keeps the HUD lightweight, ties recording to the overlay workflow the USER already understands, avoids a confusing second profile system, preserves modular standalone windows for settings, keeps advanced output/log tooling future-gated, and makes the recording target visible before any execution can surprise the USER.
USER Design Direction Decision: Pending USER Confirmation - USER may accept Codex recommendation, accept with changes, choose another option, request a hybrid option, reject and ask for more options, or pause as unclear.
Current Branch Scope: Current branch scope is the accepted active-overlay-driven recording end-state foundation, including target model proof, HUD Overlay card planning, Recording Settings planning, output-contract planning, and validation/live proof planning after separate implementation approval.
Future-Gated Scope: Future-gated scope includes recording execution, file writing until admitted, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup, PR, merge, release, issue mutation, and durable Native Log Loader source-truth mutation.
Implementation Staging Notes: SLC-051 through SLC-055 remain Codex implementation scaffolding for the accepted end-state, not the USER-facing decision ballot. Target model work comes first because HUD controls, Recording Settings, output contract, validators, H1, LV1, and UTS proof all depend on a trustworthy definition of what would be recorded.
Alternatives / Tradeoffs: The prior profile-loaded Recording Profile route is preserved only as historical rollback receipt because it did not match the clarified USER recording vision.
USER Decisions Needed: USER should decide whether to accept, change, or add to the active-overlay recording end-state; whether the HUD Overlay card should eventually show target preview only, disabled future controls, or another compact recording concept; whether the standalone Recording Settings direction feels right; whether output planning should present CSV-like or multiple format options later; and whether Native Log Loader remains future input only.
USER Review Response: Accepted by USER - USER accepted the improved review format, reaffirmed active-overlay-driven recording, rejected separate Recording Profile direction, chose Option A Target Preview First for SLC-051, required SLC-051 to remain state/proof-only, approved read-only target preview only if repo truth says safe, required no actual recording controls/execution/file writing in SLC-051, kept Start/Stop controls for a later seam unless a clearly disabled/future-gated preview affordance is later proven necessary, kept Recording Settings window for a later compact standalone OS-style NDAI window, requested graph/plot-ready output planning with CSV-like likely first but file-format options before SLC-054, and kept Native Log Loader as future planning input only with no durable source-truth mutation in this gate.
Codex Response Digest: Digested - SLC-051 is constrained to Active Overlay recording target foundation only: prove that the HUD Overlay card/system can derive the would-record target from active Overlay Profile membership, cover null, empty, selected, switched, deleted/stale, duplicate/stale-ID, and high-volume membership states, preserve Overlay Profile, Overlay Display, Monitor Group, Dashboard, Manage Monitors, and Sensor Command Center behavior, and keep recording execution, file writing, real Start/Stop behavior, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, and durable Native Log Loader source-truth mutation future-gated.
Implementation Constraints Created By USER Response: SLC-051 selects Option A Target Preview First only after USER confirms this revised contract; SLC-051 remains state/proof-only; no recording execution, file writing, real Start/Stop behavior, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, or durable Native Log Loader mutation is admitted; active Overlay Profile membership is the recording target source; null/empty/selected/switched/deleted-stale/duplicate-stale-ID/high-volume states must be proven; Overlay Profile, Overlay Display, Monitor Group, Dashboard, Manage Monitors, and Sensor Command Center behavior must be preserved.
USER Rejected / Deferred Ideas: Rejected for this direction is the separate profile-loaded Recording Profile system. Deferred are recording execution, file writing, real Start/Stop controls, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup/deletion, and durable Native Log Loader source-truth mutation.
Vision Delta / Source-Truth Impact: Active branch plan and branch record must record this closed-loop contract and Pending USER Confirmation status; review packet and ZIP must be refreshed at the final HEAD; family vision/backlog/roadmap do not need durable Native Log Loader mutation in this gate; Workstream seam order remains target-model-first as implementation staging rather than USER decision surface.
Contract Change Log: v1 introduced USER-facing Branch Plan Review packet with end-state/options sections. v2 hardens it into USER Branch Plan Contract with closed-loop USER response/digest, implementation constraints, source-truth impact, confirmation loop, stale-packet protection, and waiver semantics.
Workstream Entry Result: Pending USER Confirmation - first seam remains expected to be SLC-051 Active Overlay recording target foundation, but implementation approval text is not legal until USER confirms this revised USER Branch Plan Contract or explicitly waives it. Expected SLC-051 files remain limited to active-overlay target state/proof helpers, HUD Overlay card read-only target proof only if needed, FAM-006 validators/fixtures, and directly supporting branch/source-truth records after confirmation.
Contract Completion Checklist: Pending USER Confirmation - contract is not Complete or Waived by USER yet; USER response is recorded; Codex digest is present; implementation constraints are present; source-truth impact is recorded; rejected/deferred ideas are recorded; contract change log is current; packet metadata must be refreshed to final HEAD and ZIP source HEAD; implementation approval text must cite Complete or Waived by USER status after USER confirms or waives.
Accepted Scope: Accepted scope is Branch Readiness Stage 2 setup, source-truth admission, old carrier fold-down, Stage 2 review packet creation, validation, commit, and push.
Deferred Scope: Deferred scope is runtime implementation, Workstream Entry, Workstream implementation, recording execution, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge, release, issue mutation, artifacts/raw evidence handling beyond approved review packet, sibling-worktree mutation, old branch cleanup/deletion, and Governance mutation.
Rejected Scope: Requiring users to load a separate Recording Profile before recording sensors is rejected for this future recording path unless USER explicitly re-approves it.
Exact USER Decision Needed: USER may confirm the revised USER Branch Plan Contract or explicitly waive the contract gate; the next runtime seam remains blocked while Contract Status is Pending USER Confirmation.
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

Next Legal Phase: `USER Branch Plan Contract confirmation`
Exact USER Decision Needed: `I confirm the revised USER Branch Plan Contract for FAM-006 Active Overlay Recording Runtime Foundation in C:\Nexus Worktrees\FAM-006 on feature/fam-006-active-overlay-recording-runtime-foundation. This approval covers recording USER confirmation of the current contract version as Complete, preserving the active-overlay-driven recording end-state, recording the confirmation in the active branch plan, branch record, USER_BRANCH_PLAN_REVIEW.md, Desktop review packet, and exported ZIP, running required validation, and committing/pushing if green. This does not approve SLC-051 implementation, runtime implementation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, PR creation, merge, release, issue mutation, Governance worktree mutation, or durable Native Log Loader source-truth mutation.`
