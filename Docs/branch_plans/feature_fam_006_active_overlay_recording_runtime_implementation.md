# Branch Runtime Engineering Plan - FAM-006 Active Overlay Recording Runtime Implementation

Branch: `feature/fam-006-active-overlay-recording-runtime-implementation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Created From: `feature/fam-006-recording-profile-runtime-foundation` at `1f399003d2e6d13b34b567cd7f7900a709254bc9`
Current Plan Phase: `Branch Readiness Stage 2 setup`
Runtime Implementation Approval: `Blocked - this branch is not the runtime implementation carrier; SLC-051 and all runtime work are deferred to a future USER-approved carrier`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Active Overlay Recording Runtime Implementation`
Owning Branch: `feature/fam-006-active-overlay-recording-runtime-implementation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Current Phase: `Branch Readiness`
Branch Runtime Engineering Plan: `Fresh runtime implementation carrier imported from the released active-overlay-driven recording planning contract.`
Engineering Plan Status: `Accepted`
Current Runtime Baseline: `FAM-006 Overlay Profile Runtime Foundation and Overlay Display Acceptance Foundation are released historical evidence. The profile-loaded Recording Profile Workstream route was rolled back by USER request and is preserved as historical receipt only.`
Branch Purpose: `Admit a corrected FAM-006 recording carrier where recording is driven by the active Overlay Profile membership rather than a separate loaded Recording Profile.`
Planned Runtime Delta: `None during Stage 2 setup. Future runtime deltas for active-overlay recording target, HUD Overlay launcher/target preview, standalone Recording Control window, secondary settings surfaces, durable output contract, and validation/live proof are deferred to a later USER-approved carrier.`
User-Facing Delta: `None on this branch. Future user-facing changes require USER implementation approval on a later runtime carrier after Workstream Entry.`
Source-Truth Delta: `Add this active branch authority and branch plan; move the old Recording Profile branch from active authority to historical/rollback receipt posture; update compact backlog/roadmap pointers to this corrected carrier; preserve released Overlay Profile and Overlay Display evidence.`
State / Config / Schema Delta: `None during Stage 2. Future state/schema must target active Overlay Profile membership and recording settings without reintroducing profile-loaded Recording Profile membership unless USER explicitly re-approves it.`
Validator / Helper Delta: `No runtime validator/helper mutation during Stage 2 unless source-truth validators require pointer updates. Future validators must cover real user-level input, compact/default photo comparison, output-file proof when implemented, null/stress states, and boundary preservation.`
Expected Changed Files / Surfaces: `Docs/branch_records/index.md; Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md; Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md; Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/retirement_index.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `SLC-051 through SLC-055 are admitted as the planned implementation package; no Workstream seam is active until USER approves Workstream Entry and subsequent implementation.`
Per-Seam Implementation Checklist: `SLC-051 must name state/target surfaces; SLC-052 must name HUD Overlay card launcher/target-preview surfaces; SLC-053 must name standalone Recording Control window and secondary settings surfaces; SLC-054 must name output-file contract surfaces; SLC-055 must name validator/helper/proof surfaces.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks when JavaScript changes, H1 checks, LV1 real-input proof where user-facing, compact/default photo comparison, null/stress proof, and regression proof for Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, and Overlay Display.`
Per-Seam User-Facing Proof Checklist: `Deferred to a future runtime implementation carrier. Any future visible control/window/status must carry real user-level mouse/keyboard proof, hover/focus screenshots, compact/default screenshots, dirty/state transition proof where applicable, and UTS handoff criteria.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, old branch cleanup/deletion, and artifacts/raw evidence handling beyond approved review bundles.`
Approval-Boundary Audit: `Planning/governance closeout only. The old Recording Profile Workstream was rolled back by USER request and receipt-complete on its historical carrier. This plan does not ratify runtime implementation.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. Future runtime seams may touch HUD Dashboard, HUD Overlay card, Overlay Profile, Overlay Display, Manage Monitors, Sensor Command Center, and visual validation helpers; Workstream Entry must forecast exact overlap before implementation.`
Open Questions: `Pending future implementation-carrier decisions: first bounded seam after Workstream Entry, exact output file contract proposal, permanent HUD Overlay card placement, Recording Control and secondary settings fields, snapshot-at-recording-start versus live-follow behavior for future execution, future per-overlay effective polling policy handling, and whether actual recording execution belongs in this package or a later USER-approved seam.`
USER Planning Decisions: `USER clarified that recording should be active-overlay-driven, avoid separate Recording Profile selection, use the HUD Overlay card as launcher/target preview, use a compact standalone Recording Control window as the future control surface, keep Native Log Loader separate/future, and preserve per-overlay effective polling policy as future planning. USER approved Stage 2 setup for this corrected carrier from current FAM-006 rollback receipt HEAD.`
Plan Revision History: `v1 - Created during Branch Readiness Stage 2 setup after rollback of the profile-loaded Recording Profile Workstream route. v2/v3 - hardened and revised USER Branch Plan Contract into accepted active-overlay product plan. v4 - USER accepted the plan and redirected this branch to planning/governance PR Readiness without runtime Workstream execution.`
Plan-To-Implementation Traceability: `This branch has no runtime implementation. Future implementation must start from this plan and map each SLC-051 through SLC-055 delta to changed files, validator/helper proof, H1 result, LV1/UTS proof, deferred boundaries, and commit evidence on the later runtime carrier.`
Plan-To-Implementation Traceability Table: `Planned table owner is this branch plan for future implementation reference only: SLC-051 will trace active overlay target files and validators; SLC-052 will trace HUD Overlay launcher/target-preview files and visual proof; SLC-053 will trace Recording Control window / secondary settings files and real-input proof; SLC-054 will trace output contract files/helpers and readback proof; SLC-055 will trace validator/helper/LV1/UTS files and evidence. This branch must not fill runtime changed files, H1, LV1, or UTS as if implementation occurred.`
Hardening Comparison Checklist: `Not applicable on this branch because no runtime/user-facing implementation occurred. Future implementation carrier owns H1.`
Live Validation Proof Or Waiver Checklist: `Not applicable on this branch because no runtime/user-facing implementation occurred. Future implementation carrier owns LV1/UTS.`
PR Readiness Fold-Down / Retention Checklist: `PR Readiness must fold this branch down as planning/governance truth only, preserve accepted v3 contract in maintained source truth, and avoid claiming runtime implementation or release-user-facing behavior.`
Release Readiness Public-Scope Translation Checklist: `Release language must describe only planning/governance/source-truth changes if this branch merges; no active-overlay recording runtime, HUD control, Recording Control window, output file, or user-facing recording behavior shipped in this branch.`
USER Planning Review: `Completed for planning/governance closeout; USER stated the v3 plan is perfect and requested skipping Workstream on this branch.`
PR Fold-Down Packet: `Historical released - PR #222 merged this planning/governance branch, PR #223 folded it down, and v1.7.25-prebeta published the release window that included PR #222/#223/#224.`
Runtime Implementation Approval: `Blocked - runtime implementation requires a future USER-approved carrier, Workstream Entry analysis, and separate USER approval.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Active Overlay Recording Runtime Foundation`
Package Posture: `Stage 2 setup active / implementation pending Workstream Entry`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-051` Active Overlay recording target foundation | Planned / pending Workstream Entry | Define active Overlay Profile membership as the recording target while preserving Overlay Profile, Overlay Display, and Monitor Group separation. | Pending Workstream Entry and USER implementation approval on this carrier |
| `SLC-052` HUD Overlay recording launcher and target transparency | Planned / pending Workstream Entry | Plan HUD Overlay card launcher, active target/status preview, and active monitored monitor transparency without real Start/Stop, tray/export/provider scope, or recording execution. | Pending Workstream Entry and USER implementation approval on this carrier |
| `SLC-053` standalone Recording Control window foundation | Planned / pending Workstream Entry | Plan compact normal OS-level Recording Control window behavior, independent lifetime, minimization/taskbar restore, target/status summary, and secondary settings-window routing without admitting recording execution. | Pending Workstream Entry and USER implementation approval on this carrier |
| `SLC-054` durable recording output contract | Planned / pending Workstream Entry | Propose graph/plot-ready output file contract and proof expectations before or alongside approved recording execution. | Pending Workstream Entry and USER implementation approval on this carrier |
| `SLC-055` validation/live proof readiness | Planned / pending Workstream Entry | Plan validators, helper proof, H1, LV1, photo comparison, UTS strategy, null/stress coverage, and future-gated boundary proof. | Pending Workstream Entry and USER implementation approval on this carrier |

Single-Slice Package User Approval: `Not required - this branch is no longer implementing slices.`
Package Completion State: `Planning complete / runtime implementation deferred`

## Element-to-Phase Proof Matrix

Matrix Status: `Historical`
USER Review Status: `Accepted`
Open Element Questions: `Queued`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Element Validation Ledger Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AOR-001` | Active Overlay Profile recording target | Planned | SLC-051 will define how recording derives membership from the active Overlay Profile without adding a separate Recording Profile selector. | Workstream proof must assert active Overlay Profile membership drives target selection and that Overlay Profile state remains display-owned. | H1 must stress null active profile, switched active profile, deleted profile, high-volume profiles, and stale membership references. | LV1 required if user-visible target/status is added; otherwise state-only waiver must name validator proof. | UTS required for visible target/status; waived only for pure state-only proof. | Actual recording execution remains blocked until USER approves implementation scope. | Needs USER Decision | This plan |
| `AOR-002` | HUD Overlay card recording launcher and target preview | Planned | SLC-052 will plan HUD Overlay card launcher, target/status preview, and active monitor transparency after Workstream approval, while real Start/Stop remains future-gated until recording execution and file writing are admitted. | Workstream proof must include launcher/preview state, enabled/disabled or future-gated state if visible, active monitor transparency, and no tray/export/provider coupling. | H1 must stress compact/default layout, dirty/state transitions where relevant, and regression against Dashboard card controls. | LV1 must use real user-level mouse/keyboard input, before/after screenshots, compact/default photos, hover/focus proof, and pessimistic visual review if visible. | UTS must include a user-facing item that asks USER to verify HUD Overlay card launcher/target preview, active monitor transparency, compact/default visual correctness, and absence of tray/export/provider scope; any waiver must name why no visible runtime shipped. | Tray recording controls, real Start/Stop, file writing, and recording execution are separate pending USER decisions unless explicitly admitted later. | Needs USER Decision | This plan |
| `AOR-003` | Active monitored monitors transparency | Planned | SLC-052 will plan which currently active monitors are shown under the selected Overlay Profile in the HUD Overlay card. | Workstream proof must include null monitors, hidden monitors, active/visible counts, and no Monitor Group mutation. | H1 must compare Dashboard, Manage Monitors, Overlay Profile, and Overlay Display behavior for regressions. | LV1 must capture focused card screenshots at default and compact sizes if visible. | UTS required if visible in Dashboard/HUD Overlay card. | Monitor Group configuration remains owned by Manage Monitors / Sensor Command Center. | Needs USER Decision | This plan |
| `AOR-004` | Standalone Recording Control window | Planned | SLC-053 will plan an independent compact OS-level NDAI Recording Control window that opens from the HUD Overlay card and can remain open when Dashboard is closed/minimized. | Workstream proof must include launch, close/minimize, taskbar restore where feasible, independent movement/lifetime, target/status summary, future path/settings routing, focus/dirty guard if settings mutate, and no Dashboard child-window dependency. | H1 must stress window lifetime, compact minimum size, real resize behavior, close/minimize, save/discard/cancel if dirty state exists, and no Dashboard input bleed-through. | LV1 must use visible real mouse movements/clicks, keyboard input where relevant, photos before/after every user-facing state, and compact/default comparison. | UTS required because this is a user-facing window. | Real Start/Stop, file writing, and advanced bulky settings remain future-gated or move behind secondary surfaces only after USER approval. | Needs USER Decision | This plan |
| `AOR-005` | Durable recording output contract | Planned | SLC-054 will propose and, if approved, implement or validate the output file contract needed for future graph/plot workflows. | Workstream proof must include schema/header/row determinism, timestamp/value/source identity, path handling, null/no-data behavior, and parse/readback proof. | H1 must stress file path errors, long recordings, high-volume sensors, interrupted write, and compatibility with future graph/plot usage. | LV1 requires user-facing proof only if output settings or recording execution are visible; otherwise helper proof can satisfy file-contract validation. | UTS required if a user can create/select/open output files; otherwise Workstream/H1 proof may be sufficient. | Export/share/import remains a future package and is not authorized by an output contract alone. | Needs USER Decision | This plan |
| `AOR-006` | Recording execution | Future | Not implemented by Stage 2. Workstream Entry must decide whether actual Start/Stop execution belongs in this package or needs a separate USER approval seam. | Boundary proof must show no runtime recording execution is added before USER approval. | H1 must confirm no fake recording or unauthorized file writes. | LV1 absence proof if visible buttons exist without execution; otherwise future branch owns execution proof. | USER acceptance belongs to the approved implementation seam that admits execution. | Boundary keeps recording execution out of current release gating until USER grants explicit implementation approval for file-writing/runtime recording behavior in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-007` | Tray recording controls | Future | No implementation in this package unless USER separately approves tray scope. | Boundary proof must show no tray Start/Stop control was added. | H1 must confirm tray behavior unchanged. | LV1 absence proof only if visible UI could imply tray controls. | Future USER acceptance belongs to a tray-controls branch or approved scope revision. | Boundary keeps tray recording controls out of current release gating until USER grants a tray-control scope decision in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-008` | Export/share recording output | Future | No export/share/import implementation in this package. | Boundary proof must show no export/share UI or workflow was added. | H1 must confirm output contract does not become export/share behavior. | LV1 absence proof only if user-facing UI could imply export/share. | Future USER acceptance belongs to export/share branch or approved scope revision. | Boundary keeps export/share/import out of current release gating until USER grants an export/share scope decision in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-009` | Provider/model integration | Future | No provider/model/memory work in this package. | Boundary proof must show active-overlay recording has no provider/model dependency. | H1 must confirm FAM-007 boundaries remain unchanged. | LV1 absence proof only if UI could imply provider/model integration. | Future USER acceptance belongs to FAM-007 or other approved branch. | Boundary keeps provider/model/memory integration out of current release gating until USER grants provider/model scope in FAM-007 or another approved carrier. | Deferred With Waiver | This plan |
| `AOR-010` | Validation/live proof governance for recording surfaces | Planned | SLC-055 will update validators/helpers only as required by implemented runtime seams. | Workstream proof must include source-truth validators, HUD validators, internal sandbox, validation suite, JS checks when changed, output-file helper proof when relevant, and matrix coverage. | H1 must be pessimistic and compare planned behavior to actual code, screenshots, and helper outputs. | LV1 must use real user-facing launcher where feasible, real cursor movement/clicks, compact/default photo comparison, and explicit blocker if real input is impossible. | UTS handoff required after LV1 for user-facing changes unless explicitly waived. | Validator fallbacks must not replace real input without USER-visible blocker/digest. | Needs USER Decision | This plan |

## Branch Change Intent Ledger

### Changed Surface: Docs/branch_records/index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Record that PR #222 replaced the prior FAM-006 Recording Profile rollback carrier pointer with this active-overlay-driven recording planning receipt and moved the old Recording Profile record to historical receipt posture.`
- Why This File Was Touched: `Branch Readiness Stage 2 is the legal carrier for active branch authority admission and rollback carrier fold-down.`
- Owned Behavior / Fact Class: `Branch authority routing.`
- Canonical Owner / Source Owner: `Docs/branch_records/index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium if origin/main advances before PR.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve standing governance active pointer, preserve incoming current-main governance context, keep this merged PR #222 branch pointer in Historical Branch Authority Records, and keep the old Recording Profile branch pointer in Historical Branch Authority Records only.`
- Rebaseline Handling: `Run the pre-reconciliation overlap audit before any future current-main reconciliation if origin/main advances.`
- Validation Proof: `Branch governance validation, worktree-confinement gate, release-readiness health gate, branch-readiness planning fixture validation, source-owner marker validation, FAM-006 validators, runtime-fam006 validation suite, and compileall.`
- Fallback Evidence: `Use this branch plan and active branch authority record as branch-owned intent evidence; compatibility still requires preserving current-main governance context and validating after reconciliation.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup for this corrected carrier; no waiver authorizes runtime implementation or old branch deletion.`
- Fold-Down Target: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md remains historical rollback receipt; this branch is now historical PR #222 planning/governance receipt.`

### Changed Surface: Docs/feature_backlog.md

- Surface Class: `governance/source-truth`
- Change Intent: `Update the compact FAM-006 status and canonical detail owner from the rollback carrier to the PR #222 active-overlay-driven recording planning receipt.`
- Why This File Was Touched: `The backlog compact pointer must route FAM-006 planning history to the merged PR #222 branch authority receipt without implying active runtime work.`
- Owned Behavior / Fact Class: `Feature-family status and canonical pointer routing.`
- Canonical Owner / Source Owner: `Docs/feature_backlog.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium if origin/main advances before PR.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve compact family status, historical released Overlay evidence, rollback receipt context, and route historical planning detail to this branch receipt.`
- Rebaseline Handling: `If main overlaps, preserve current-main family statuses and this FAM-006 historical planning receipt pointer.`
- Validation Proof: `Branch readiness planning fixture validation and FAM-006 HUD validators must pass.`
- Fallback Evidence: `Use this plan and branch record as FAM-006 historical planning receipt evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup for the corrected carrier.`
- Fold-Down Target: `PR #222 preserves this durable branch-record receipt; future runtime work requires a later USER-approved carrier.`

### Changed Surface: Docs/Main.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main source-truth router and sync-index updates while keeping FAM-006 active-overlay recording planning/governance history routed through this branch's maintained authority record and plan.`
- Why This File Was Touched: `The FAM-006 branch history includes Main/router changes from earlier governance and branch setup work, while origin/main now carries Release Readiness/source-truth-intake updates that must remain the canonical router context before PR Readiness.`
- Owned Behavior / Fact Class: `Primary repo source-truth router, loader map, and sync index.`
- Canonical Owner / Source Owner: `Docs/Main.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High when current-main governance/source-truth router updates overlap branch-local FAM-006 routing context.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main router/source-truth-intake context, preserve any still-current FAM-006 active-overlay planning pointers only where they remain legitimate, and do not let this FAM-006 branch overwrite newer repo-wide source-truth routing.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main Main/router updates as authority and retain FAM-006 planning-governance history only through the historical FAM-006 branch record, branch plan, family vision, backlog, roadmap, and refreshed review packet.`
- Validation Proof: `Pre-reconciliation overlap audit must pass after this ledger repair; branch governance validation, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `origin/main@3dd999f873bb4f4dffb76ad2f3f613a34ccf776c includes Release Readiness/source-truth-intake updates from PR #221; this FAM-006 branch plan remains historical owner only for FAM-006 planning-governance receipt evidence.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair to preserve incoming origin/main source-truth/governance context while preserving the FAM-006 planning/governance closeout posture.`
- Fold-Down Target: `Docs/Main.md remains the repo router; FAM-006 branch-local proof folds into PR Readiness source-truth projection.`

### Changed Surface: Docs/prebeta_roadmap.md

- Surface Class: `governance/source-truth`
- Change Intent: `Update FAM-006 public milestone pointer to this PR #222 active-overlay-driven recording planning receipt while preserving historical Overlay Display and rollback receipt context.`
- Why This File Was Touched: `Roadmap compact pointer must not route future recording planning to the rolled-back profile-loaded carrier or imply this merged receipt is active runtime work.`
- Owned Behavior / Fact Class: `Pre-Beta milestone pointer routing.`
- Canonical Owner / Source Owner: `Docs/prebeta_roadmap.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium if origin/main advances before PR.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve current-main roadmap family statuses, released FAM-006 evidence, rollback receipt context, and this PR #222 planning receipt pointer.`
- Rebaseline Handling: `If main overlaps, preserve current-main release-stage context and this branch-local FAM-006 historical planning receipt pointer.`
- Validation Proof: `Roadmap/backlog pointer validators and branch governance validation must pass.`
- Fallback Evidence: `Use this plan and branch record as historical FAM-006 recording planning receipt evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup for this corrected carrier.`
- Fold-Down Target: `PR #222 preserves compact roadmap fold-down text; future runtime work requires a later USER-approved carrier.`

### Changed Surface: Docs/branch_plans/retirement_index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Retire the old Recording Profile branch plan from active planning posture and preserve this branch plan as the PR #222 historical planning receipt.`
- Why This File Was Touched: `The old carrier remains as rollback receipt only; the plan pointer must route future planning history to this corrected PR #222 receipt without implying active runtime work.`
- Owned Behavior / Fact Class: `Branch plan lifecycle and active plan posture.`
- Canonical Owner / Source Owner: `Docs/branch_plans/retirement_index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low to Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Keep historical plan rows, add old Recording Profile plan as retired, and record this plan as retired after PR #222 merge.`
- Rebaseline Handling: `Preserve incoming current-main retired-plan rows and this historical FAM-006 posture.`
- Validation Proof: `Branch readiness planning fixture validation must pass.`
- Fallback Evidence: `Use this plan, historical branch record, and retirement index row as lifecycle evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup and did not authorize old branch deletion.`
- Fold-Down Target: `PR #222 retires this plan from active planning posture; future runtime implementation requires a later USER-approved carrier.`

### Changed Surface: Docs/branch_plans/feature_fam_007_v1_7_23_post_release_canon_closure.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main FAM-007 v1.7.23 post-release canon-closure branch-plan context during FAM-006 current-main reconciliation.`
- Why This File Was Touched: `The FAM-006 branch carries older FAM-007 closure context from branch history, and origin/main now includes PR #221 / release-readiness source-truth-intake updates that refine the FAM-007 v1.7.23 post-release canon closure.`
- Owned Behavior / Fact Class: `FAM-007 historical post-release canon-closure planning receipt.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_007_v1_7_23_post_release_canon_closure.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main FAM-007 fold-down/canon-closure updates overlap FAM-006 branch history.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main FAM-007 post-release canon-closure source truth, do not convert this FAM-007 plan into FAM-006 authority, and keep FAM-006 active-overlay recording truth in the FAM-006 branch record/plan.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main FAM-007 v1.7.23 canon-closure updates for this file while preserving FAM-006 planning/governance closeout and avoiding FAM-007 branch/workstream mutation.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, release-readiness health gate, branch readiness planning fixture validation, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `origin/main@3dd999f873bb4f4dffb76ad2f3f613a34ccf776c contains incoming FAM-007 post-release canon-closure and Release Readiness source-truth-intake updates; this ledger is reconciliation intent evidence only.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair; no approval is granted for FAM-007 branch/workstream mutation.`
- Fold-Down Target: `FAM-007 historical/canon-closure source truth remains owned by FAM-007/current-main history; FAM-006 PR Readiness records only that it preserved incoming context.`

### Changed Surface: Docs/branch_records/feature_fam_007_v1_7_23_post_release_canon_closure.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main FAM-007 v1.7.23 post-release canon-closure authority record context during FAM-006 current-main reconciliation.`
- Why This File Was Touched: `The FAM-006 branch carries older FAM-007 closure authority context from branch history, and origin/main now includes PR #221 / release-readiness source-truth-intake updates that refine the FAM-007 v1.7.23 post-release canon closure authority.`
- Owned Behavior / Fact Class: `FAM-007 historical post-release canon-closure branch authority receipt.`
- Canonical Owner / Source Owner: `Docs/branch_records/feature_fam_007_v1_7_23_post_release_canon_closure.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main FAM-007 authority/fold-down updates overlap FAM-006 branch history.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main FAM-007 post-release canon-closure authority receipt, do not route FAM-007 authority through FAM-006, and keep FAM-006 active branch authority in Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main FAM-007 v1.7.23 canon-closure updates for this file while preserving FAM-006 planning/governance closeout and avoiding FAM-007 branch/workstream mutation.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, release-readiness health gate, branch readiness planning fixture validation, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `origin/main@3dd999f873bb4f4dffb76ad2f3f613a34ccf776c contains incoming FAM-007 post-release canon-closure and Release Readiness source-truth-intake updates; this ledger is reconciliation intent evidence only.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair; no approval is granted for FAM-007 branch/workstream mutation.`
- Fold-Down Target: `FAM-007 historical/canon-closure authority remains owned by FAM-007/current-main history; FAM-006 PR Readiness records only that it preserved incoming context.`

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
- Conflict Resolution Rule: `Preserve incoming current-main FAM-007 historical authority receipt and do not treat the FAM-007 branch as FAM-006 authority; keep FAM-006 PR #222 historical branch authority in Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main FAM-007 historical/fold-down updates for this file while preserving FAM-006 rollback receipt context, active-overlay-driven recording planning receipt state, and USER_BRANCH_PLAN_REVIEW.md response/digest gate.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, runtime-fam006 validation suite recommendation, source-owner marker validation, and compileall must pass before current-main reconciliation can resume.`
- Fallback Evidence: `origin/main@73b4905cc5e6c626fae56ffd83f9df6c25e116a4 contains the FAM-007 fold-down/source-truth receipt; this FAM-006 branch record remains separate and now owns historical FAM-006 planning receipt truth.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair to preserve incoming FAM-007 fold-down/source-truth context while keeping FAM-006 active-overlay recording as future planning truth.`
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

### Changed Surface: Docs/governance_efficiency_operating_model.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming current-main governance-efficiency/source-truth-intake context while keeping FAM-006 planning/governance closeout limited to this branch's accepted active-overlay recording contract.`
- Why This File Was Touched: `The FAM-006 branch carries older governance-efficiency context from review-packet and governance hardening work, while origin/main now includes PR #221 Release Readiness/source-truth-intake updates that should remain canonical for repo-wide governance efficiency.`
- Owned Behavior / Fact Class: `Repo-wide governance efficiency, source-truth reform, and operating-model guidance.`
- Canonical Owner / Source Owner: `Docs/governance_efficiency_operating_model.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main governance-intake updates overlap FAM-006 branch-local governance hardening history.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main governance-efficiency/source-truth-intake updates; do not let FAM-006 branch-local review-packet hardening weaken or replace repo-wide governance operating-model truth.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main governance-efficiency context as authority and preserve FAM-006-specific planning/governance closeout only in FAM-006 branch source truth and review packet.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, release-readiness health gate, branch readiness planning fixture validation, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `origin/main@3dd999f873bb4f4dffb76ad2f3f613a34ccf776c includes Release Readiness/source-truth-intake governance updates from PR #221; FAM-006 remains the owner only for its branch-local planning closeout.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair to preserve incoming origin/main governance context while preserving the FAM-006 planning/governance closeout posture.`
- Fold-Down Target: `Repo-wide governance-efficiency truth remains in this shared file; branch-local proof folds into FAM-006 PR Readiness only.`

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
- Change Intent: `Make the USER review Desktop bundle helper generate, validate, and print concrete folder/ZIP review packet proof, including pre-generation deletion of prior matching ZIP artifacts.`
- Why This File Was Touched: `The helper is the reusable path for creating START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, and the uploadable ZIP; this branch needs the helper to fail if that proof is absent or stale and needs the USER-visible upload path to be unambiguous.`
- Owned Behavior / Fact Class: `Reusable USER review bundle generation and stale-guard validation behavior.`
- Canonical Owner / Source Owner: `dev/orin_user_review_bundle.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when current-main helper changes overlap FAM-007 review-bundle helper behavior.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming helper improvements, preserve stable Desktop review root and ZIP behavior, and retain validation that previous matching ZIP artifacts and existing review-folder contents are moved to governed quarantine before generation, the recreated folder is confirmed empty before copy, and the exported ZIP contains START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, governed-quarantine proof, stale-guard proof, folder-empty proof, and USER Review Packet Finding PASS for the current Source HEAD.`
- Rebaseline Handling: `During current-main reconciliation, merge helper changes carefully and rerun helper/validator syntax plus governance validation before claiming green.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, source-owner marker validation, and compileall must pass.`
- Fallback Evidence: `Docs/validation_helper_registry.md owns helper responsibility; START_HERE.md carries packet/upload proof after helper execution, and pre-generation cleanup moves matching zip artifacts plus prior folder contents into governed quarantine before the regenerated folder and stable ZIP artifact are created.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this helper before current-main reconciliation; no waiver authorizes stale ZIP output.`
- Fold-Down Target: `Reusable helper remains shared; branch-specific proof is recorded in the review packet and PR Readiness closeout.`

## USER Branch Plan Review Gate

USER Branch Plan Review: Required - Stage 2 creates a USER branch-plan review packet and future Workstream Entry must present a full readable implementation plan before runtime work begins.
Review Status: Accepted by USER
Contract Status: Complete - imported from the USER-confirmed released planning contract; Workstream Entry must re-check packet freshness and digest status before any implementation approval.
Contract Version / Revision: v1 implementation-carrier import of the released v4 active-overlay recording contract.
Desktop Review Bundle: `C:\Users\anden\OneDrive\Desktop\Nexus USER Review\FAM-006`
USER Review Packet Finding: Required before Workstream Entry - Workstream Entry analysis must load and digest `START_HERE.md`, `USER_BRANCH_PLAN_REVIEW.md`, and `C:\Users\anden\OneDrive\Desktop\Nexus USER Review\FAM-006.zip`; compare packet source branch, packet source HEAD, review zip source HEAD, and current branch HEAD; prove previous matching ZIP artifacts were moved out of the stable upload location before generation through `Review Export Pre-Clean Removed Count:` and `Review Export Quarantine Paths:`; prove prior review-folder contents were moved out through `Review Folder Pre-Clean Removed Count:`, `Review Folder Quarantine Path:`, and `Review Folder Empty Before Copy: PASS`; prove the implementation carrier branch record and branch plan are present; and report loaded, stale, missing, waived, or blocking status before implementation approval text can be returned.
Plain-Language Branch Goal: Establish the corrected FAM-006 recording branch where recording is driven by the active Overlay Profile instead of a separate Recording Profile.
What Will I Actually See, And Where Will I See It?: USER should eventually see the HUD Overlay card act as the recording launcher and target/status preview: active Overlay Profile name, Recording Target / Active Recording Target label, concise active target summary, future-gated recording status, and an Open Recording Control action. The Recording Control window should be a compact standalone normal Windows/NDAI window with target summary, future Start/Stop placement after execution is admitted, folder/path summary after settings are admitted, and route to secondary advanced/settings windows when content would become bulky. Native Log Loader is a separate future graph/log viewer, not the recording control surface.
Planned User-Facing Outcome: No user-facing runtime change in Stage 2; future user-facing outcome is HUD Overlay launcher/target preview, transparent active monitor target, and a compact standalone Recording Control window after later approval.
End-State Vision: The completed active-overlay recording foundation should make recording feel automatic and connected to the overlay the USER already loaded. Overlay Profile defines what is visible/tracked; active overlay membership defines the recording target; the HUD Overlay card previews that target and launches the compact Recording Control window; the Recording Control window is a small standalone control surface; the Native Log Loader remains a separate future viewer for graphing and inspecting completed logs.
Visual / Behavioral Description: Future recording should start from the HUD Overlay card as a truthful target/status preview, not from a separate Recording Profile chooser. The user should open a compact, taskbar-restorable Recording Control window from the HUD Overlay card, keep it movable/minimizable independently of the Dashboard, and use secondary settings/details windows only when the main control surface would become too large.
Visual / Functional Walkthrough: USER starts at the Dashboard HUD Overlay card, sees the active Overlay Profile and target/status preview, opens the standalone Recording Control window when ready, and later uses that window for compact recording controls after execution is admitted. Advanced path/format/settings details move to secondary windows. Future log files are designed so a separate Native Log Loader can graph data over time, but loader implementation remains future-gated.
Surface Map: HUD Overlay card = launcher and target/status preview; Recording Control window = compact standalone control surface; secondary settings/advanced windows = bulky configuration surfaces when needed; Overlay Profile = source of active recording target membership; Monitor Group = reusable sensor/source group; files/output = future graph/plot-ready recording data; Native Log Loader = future separate graph/log viewer; tray/export/provider/theme/FAM-007 = future-gated surfaces outside this approval.
Implementation Breakdown: Stage 2 admits and preserves source truth only; Workstream is skipped on this branch. SLC-051 target foundation, SLC-052 HUD Overlay launcher/target transparency, SLC-053 standalone Recording Control window and secondary settings surfaces, SLC-054 output contract, and SLC-055 validation/live proof readiness are future implementation planning for a later USER-approved carrier.
Element-to-Phase Proof Matrix: Present in this plan for AOR-001 through AOR-010.
Hardening Plan: Future H1 must pressure-test active overlay membership, Dashboard/HUD Overlay behavior, standalone settings window behavior, output contract, concept separation, compact/default UI, and future-gated boundaries.
Live Validation / UTS Plan: Future LV1 must use real user-level input, visible cursor movement/clicks, compact/default screenshots, focused per-element screenshots, output-file proof where applicable, and UTS handoff or explicit waiver.
Open USER Questions: Workstream Entry must determine the first bounded seam, output file contract recommendation, exact Recording Control / secondary settings fields, permanent HUD Overlay card arrangement, snapshot-at-recording-start versus live-follow behavior for future execution, and whether actual recording execution is in this package or a later package.
USER Design Review Questions: Needs USER Confirmation - USER must review the generated `USER_BRANCH_PLAN_REVIEW.md` v3 end-state, HUD Overlay launcher/target preview, standalone Recording Control window direction, Native Log Loader separation, future per-overlay polling-policy constraint, and any desired revisions before bounded Workstream implementation begins. Slice/seam details remain implementation staging, not the main USER decision surface.
Codex Recommendations: Accept the active-overlay-driven recording product model: recording targets derive from the active Overlay Profile, the HUD Overlay card previews target/status and launches recording control, the standalone Recording Control window stays compact and OS-level, Native Log Loader remains a separate future viewer, and per-overlay effective polling policy is recorded as future FAM-006 architecture so SLC-051 does not block it.
Implementation Options: Option A - Target model proof first; Option B - target preview in the HUD Overlay card; Option C - standalone Recording Control window shell first; Option D - live Start/Stop planning later after recording execution and file writing are admitted. Codex recommends Option A first, with Option B and C following only after the target model is trustworthy.
Recommended Direction: Codex recommends target model proof first for SLC-051, then HUD target preview and the standalone Recording Control window in later seams unless repo truth selects minimal read-only proof markers sooner. For later recording execution, Codex recommends snapshot-at-recording-start as the default log model unless USER revises it, while SLC-051 should prove the live current active-overlay target because no recording is occurring yet.
Why This Fits The Nexus Vision: This direction keeps recording intuitive, avoids a confusing second profile system, keeps the HUD lightweight, gives the user a compact normal OS window for ongoing control, keeps graph/log viewing separate from recording control, and protects future log quality by recording per-overlay effective polling policy as architecture before execution exists.
USER Design Direction Decision: Accepted by USER for the active-overlay recording product direction; Workstream Entry analysis is the next legal review step before implementation.
Current Branch Scope: Current branch scope is the accepted active-overlay-driven recording end-state foundation, including target model proof, HUD Overlay card launcher/target-preview planning, Recording Control window planning, secondary settings planning, output-contract planning, and validation/live proof planning after separate implementation approval.
Future-Gated Scope: Future-gated scope includes recording execution, file writing until admitted, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup, PR, merge, release, issue mutation, and durable Native Log Loader source-truth mutation.
Implementation Staging Notes: SLC-051 through SLC-055 remain future implementation scaffolding for the accepted end-state, not work to execute on this branch. Target model work comes first on the future runtime carrier because HUD launcher/preview, Recording Control window, output contract, validators, H1, LV1, and UTS proof all depend on a trustworthy definition of what would be recorded.
Alternatives / Tradeoffs: The prior profile-loaded Recording Profile route is preserved only as historical rollback receipt because it did not match the clarified USER recording vision.
USER Decisions Needed: Workstream Entry analysis is the next USER decision. Runtime implementation, SLC-051, Workstream implementation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, release execution, issue mutation, Governance worktree mutation, and durable Native Log Loader implementation remain pending decisions.
USER Review Response: Accepted by USER - USER accepted the active-overlay recording product direction on the released planning carrier and later approved this fresh runtime implementation carrier from current origin/main.
Codex Response Digest: Digested - the accepted v4 planning contract is imported as this carrier's starting implementation plan. This branch may proceed only to Workstream Entry analysis next; SLC-051 and all runtime mutation remain blocked until separate USER implementation approval.
Implementation Constraints Created By USER Response: This branch must not implement SLC-051 or any runtime/user-facing recording work during Stage 2; active Overlay Profile membership remains the future recording target source; no separate Recording Profile system or recording-specific sensor chooser is admitted; recording execution, file writing, real Start/Stop behavior, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, and durable Native Log Loader mutation remain blocked; future recording execution should default to snapshot-at-recording-start for clean logs unless USER revises it; future SLC-051 may prove the live current target because it records nothing; future target proof must preserve null/empty/selected/switched/deleted-stale/duplicate-stale-ID/high-volume states and existing Overlay Profile, Overlay Display, Monitor Group, Dashboard, Manage Monitors, and Sensor Command Center behavior; per-overlay effective polling policy remains future-planning/source-truth constraint.
USER Rejected / Deferred Ideas: Rejected for this direction is the separate profile-loaded Recording Profile system and any duplicated CPU FAST/CPU SLOW Monitor Group workaround as the desired long-term polling model. Deferred are recording execution, file writing, real Start/Stop controls, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup/deletion, durable Native Log Loader implementation/source-truth mutation beyond future planning, per-overlay polling-policy implementation, and advanced/bulky Recording Control settings.
Vision Delta / Source-Truth Impact: Active branch plan, branch record, family vision, Desktop review packet, and ZIP must record the accepted v4 contract as imported starting implementation truth for this fresh carrier. Family vision records per-overlay effective polling policy as a future FAM-006 planning constraint because it affects recording target model design. Backlog/roadmap compact pointers should show implementation-carrier Stage 2 setup and Workstream Entry pending posture. Native Log Loader remains future planning input only and is not admitted for durable implementation.
Contract Change Log: v1 introduced USER-facing Branch Plan Review packet with end-state/options sections. v2 hardened it into USER Branch Plan Contract with closed-loop USER response/digest, implementation constraints, source-truth impact, confirmation loop, stale-packet protection, and waiver semantics. v3 digested USER recording product-model feedback: HUD Overlay card launcher/target preview, standalone Recording Control window, Native Log Loader separation, future per-overlay effective polling policy, and target-model-first SLC-051. v4 recorded USER acceptance of the plan and USER-approved skip of Workstream on the released foundation planning carrier. Implementation-carrier v1 imports that accepted v4 contract onto the fresh current-main runtime implementation branch.
Workstream Entry Result: Pending - Workstream Entry analysis must inspect source truth, runtime surfaces, the Stage 2 USER review packet, and SLC-051 through SLC-055 before any implementation approval. No recording execution, file writing, real Start/Stop behavior, HUD recording controls, Recording Control window, or output-file behavior is admitted by Stage 2.
Contract Completion Checklist: Complete for imported starting implementation contract - USER response is recorded; Codex digest is present; implementation constraints are present; source-truth impact is recorded; rejected/deferred ideas are recorded; contract change log is current; packet metadata must be refreshed to final HEAD and ZIP source HEAD; implementation approval remains blocked pending Workstream Entry and separate USER approval.
Accepted Scope: Accepted scope is Branch Readiness Stage 2 setup, source-truth admission, released foundation traceability preservation, Stage 2 review packet creation, accepted contract import, validation, commit, push, and Workstream Entry analysis after USER approval.
Deferred Scope: Deferred scope is runtime implementation, Workstream Entry, Workstream implementation, recording execution, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge, release, issue mutation, artifacts/raw evidence handling beyond approved review packet, sibling-worktree mutation, old branch cleanup/deletion, and Governance mutation.
Rejected Scope: Requiring users to load a separate Recording Profile before recording sensors is rejected for this future recording path unless USER explicitly re-approves it.
Exact USER Decision Needed: USER may approve Workstream Entry analysis for this implementation carrier; runtime implementation remains blocked until Workstream Entry returns a bounded implementation approval packet and USER separately approves it.
Implementation Approval: Blocked - no runtime mutation is approved or performed by this branch.

## Future Workstream Entry Whole-Package Analysis Requirements

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

Next Legal Phase: `Workstream`
Exact USER Decision Needed: `I approve Workstream Entry analysis for FAM-006 Active Overlay Recording Runtime Implementation in C:\Nexus Worktrees\FAM-006 on feature/fam-006-active-overlay-recording-runtime-implementation. This approval covers Workstream Entry analysis only: inspection of source truth, the accepted active-overlay recording contract, Stage 2 USER review packet, runtime surfaces, SLC-051 through SLC-055 package plan, validators/helpers, source-truth updates, proof requirements, USER-facing proof requirements, and return of the first bounded implementation approval packet. This does not approve Workstream implementation, SLC-051 implementation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 mutation, issue mutation, branch cleanup/deletion, PR creation, merge, release execution, durable Native Log Loader implementation, or Governance worktree mutation.`
