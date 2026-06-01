# Branch Runtime Engineering Plan - FAM-006 Active Overlay Recording Runtime Implementation

Branch: `feature/fam-006-active-overlay-recording-runtime-implementation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Created From: `feature/fam-006-recording-profile-runtime-foundation` at `1f399003d2e6d13b34b567cd7f7900a709254bc9`
Current Plan Phase: `Workstream - SLC-051 Active Overlay recording target foundation implemented; SLC-052 HUD Overlay recording launcher and active-monitor transparency implemented; SLC-053 standalone Recording Control window foundation is active same-branch continuation; SLC-054 through SLC-055 remain queued same-branch continuation.`
Runtime Implementation Approval: `Bounded SLC-051 is implemented as target/session truth only. Bounded SLC-052 is implemented as HUD Overlay target preview/launcher-placeholder transparency. Recording execution, file writing, real Start/Stop controls, tray controls, export/share, and provider/model work remain future-gated unless source truth admits them.`
Current-Main Reconciliation Status: `Reconciled - governed current-main reconciliation through origin/main@9b64ac1b4faf4d29033e3a8f299a1293eb26f2d7 completed on this branch using a non-rewrite merge path. Incoming Branch Planning BP1/BP2/BP3, C:\Nexus USER, external operational-state placement, helpers, validators, fixtures, and USER review artifact rules are current-main authority. FAM-006 did not mutate FAM-007 source truth. Pre-PR #248 FAM-006 BP1/BP2/BP3 packets and receipts are superseded legacy evidence for active decision purposes because active Branch Planning now requires distinct Packet Reviewability State and USER Gate State proof. Active FAM-006 BP1 Branch Vision and BP2 Branch Plan are accepted by USER; BP3 is approved by USER; Workstream implementation authority covers bounded same-branch continuation one active seam at a time until Workstream Green, a named blocker, or USER waiver is recorded.`

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
Planned Runtime Delta: `SLC-051 implements target/session truth for active-overlay recording target selection. HUD Overlay launcher/target preview, standalone Recording Control window, secondary settings surfaces, durable output contract, and validation/live proof remain deferred until separate bounded implementation approval on this carrier.`
User-Facing Delta: `None for SLC-051 beyond read-only target/session proof surfaces and data markers. Future visible recording controls or launcher/preview changes require separate USER approval on this active runtime carrier.`
Source-Truth Delta: `Add this active branch authority and branch plan; move the old Recording Profile branch from active authority to historical/rollback receipt posture; update compact backlog/roadmap pointers to this corrected carrier; preserve released Overlay Profile and Overlay Display evidence.`
State / Config / Schema Delta: `SLC-051 adds activeOverlayRecordingTarget and activeOverlayRecordingTargetProof as read-only target/session truth derived from active Overlay Profile membership. It does not create a separate Recording Profile, recording execution state machine, output contract, file writing, tray controls, or Start/Stop behavior.`
Validator / Helper Delta: `SLC-051 extends FAM-006 HUD surface and internal sandbox validators to prove null active profile, empty membership, stale/deleted/missing active profile, high-volume membership, no hidden recording target state, and blocked recording execution/file writing. Future validators must cover real user-level input, compact/default photo comparison, output-file proof when implemented, and boundary preservation.`
Expected Changed Files / Surfaces: `desktop/monitoring_hud_state.py; nexus_visual/monitoring_hud.js; dev/orin_monitoring_hud_surface_validation.py; dev/orin_monitoring_hud_internal_sandbox_validation.py; Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md; Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `SLC-051 through SLC-055 are admitted as the planned implementation package. BP3 is approved; SLC-051 Active Overlay recording target foundation is implemented as the first bounded Workstream seam; SLC-052 HUD Overlay launcher/target preview is implemented as the second bounded Workstream seam; SLC-053 standalone Recording Control window foundation is the active same-branch continuation seam.`
Per-Seam Implementation Checklist: `SLC-051 must name state/target surfaces; SLC-052 must name HUD Overlay card launcher/target-preview surfaces; SLC-053 must name standalone Recording Control window and secondary settings surfaces; SLC-054 must name output-file contract surfaces; SLC-055 must name validator/helper/proof surfaces.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks when JavaScript changes, H1 checks, LV1 real-input proof where user-facing, compact/default photo comparison, null/stress proof, and regression proof for Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, and Overlay Display.`
Per-Seam User-Facing Proof Checklist: `Deferred until approved runtime seams on this active implementation carrier. Any future visible control/window/status must carry real user-level mouse/keyboard proof, hover/focus screenshots, compact/default screenshots, dirty/state transition proof where applicable, and UTS handoff criteria.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, old branch cleanup/deletion, and artifacts/raw evidence handling beyond approved review bundles.`
Approval-Boundary Audit: `Bounded SLC-051 target/session truth and bounded SLC-052 HUD Overlay target preview are implemented. The old Recording Profile Workstream was rolled back by USER request and receipt-complete on its historical carrier. This plan does not ratify recording execution, file writing, Start/Stop controls, tray controls, export/share, provider/model work, or SLC-053 through SLC-055 implementation beyond same-branch Workstream continuation.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. Future runtime seams may touch HUD Dashboard, HUD Overlay card, Overlay Profile, Overlay Display, Manage Monitors, Sensor Command Center, and visual validation helpers; Workstream Entry must forecast exact overlap before implementation.`
Open Questions: `Pending implementation-carrier decisions: first bounded seam after Workstream Entry, exact output file contract proposal, permanent HUD Overlay card placement, Recording Control and secondary settings fields, snapshot-at-recording-start versus live-follow behavior for future execution, future per-overlay effective polling policy handling, and whether actual recording execution belongs in this package or a later USER-approved seam.`
USER Planning Decisions: `USER clarified that recording should be active-overlay-driven, avoid separate Recording Profile selection, use the HUD Overlay card as launcher/target preview, use a compact standalone Recording Control window as the future control surface, keep Native Log Loader separate/future, and preserve per-overlay effective polling policy as future planning. USER approved Stage 2 setup for this corrected carrier from current FAM-006 rollback receipt HEAD.`
Plan Revision History: `v1 - Created during Branch Readiness Stage 2 setup after rollback of the profile-loaded Recording Profile Workstream route. v2/v3 - hardened and revised USER Branch Plan Contract into accepted active-overlay product plan. v4 - USER accepted the plan and redirected the released foundation carrier to planning/governance PR Readiness without runtime Workstream execution. Implementation-carrier v1 imports that accepted contract onto this active runtime implementation carrier.`
Plan-To-Implementation Traceability: `SLC-051 is implemented as target/session truth only in the current HUD / Overlay Profile owners and validators. SLC-052 is implemented in the HUD Overlay card HTML/CSS/JS and FAM-006 surface validator as target preview/launcher-placeholder transparency. Future implementation on this carrier must map SLC-053 through SLC-055 deltas to changed files, validator/helper proof, H1 result, LV1/UTS proof, deferred boundaries, and commit evidence.`
Plan-To-Implementation Traceability Table: `SLC-051 traces to desktop/monitoring_hud_state.py, nexus_visual/monitoring_hud.js, dev/orin_monitoring_hud_surface_validation.py, and dev/orin_monitoring_hud_internal_sandbox_validation.py. SLC-052 traces to nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, nexus_visual/monitoring_hud.js, and dev/orin_monitoring_hud_surface_validation.py. SLC-053 will trace Recording Control window / secondary settings files and real-input proof; SLC-054 will trace output contract files/helpers and readback proof; SLC-055 will trace validator/helper/LV1/UTS files and evidence. Do not fill H1, LV1, or UTS as complete until those phases run or are explicitly waived.`
Hardening Comparison Checklist: `Pending after SLC-051. Hardening H1 validator plan must compare SLC-051 target/session truth implementation against accepted BP1/BP2/BP3 before later release claims or before continuing if source truth routes H1 before the next seam.`
Live Validation Proof Or Waiver Checklist: `Not required for SLC-051 unless H1 discovers a user-visible surface requiring LV1/UTS; future visible seams own LV1/UTS.`
PR Readiness Fold-Down / Retention Checklist: `PR Readiness must fold down whatever this active implementation carrier actually completes, preserve the accepted v3/v4 contract in maintained source truth, and avoid claiming runtime implementation or release-user-facing behavior until approved runtime seams exist and pass proof.`
Release Readiness Public-Scope Translation Checklist: `Release language must describe only changes actually completed on this active implementation carrier; no active-overlay recording runtime, HUD control, Recording Control window, output file, or user-facing recording behavior may be claimed unless later approved runtime seams implement and validate them.`
USER Planning Review: `BP1 accepted, BP2 accepted, and BP3 active under the post-PR #248 two-axis gate model. The imported active-overlay recording contract, revised BP1 packet, and accepted BP2 packet are accepted planning context; prior pre-PR #248 BP1/BP2/BP3 packet receipts remain superseded legacy evidence for active decision purposes. Current BP3 Packet Reviewability State must be Reviewable and USER Gate State remains Pending USER Review until USER responds.`
PR Fold-Down Packet: `Historical reference - PR #222 merged the released planning/governance foundation, PR #223 folded it down, and v1.7.25-prebeta published the release window that included PR #222/#223/#224. This implementation carrier remains active and separate from that released foundation traceability.`
Runtime Implementation Approval: `SLC-051 target/session truth implementation is completed. SLC-052 HUD Overlay recording target preview is completed. BP1 and BP2 are accepted; BP3 is USER Approved; SLC-053 through SLC-055 continue as bounded same-branch Workstream seams. Recording execution and file-writing authority remain future-gated unless admitted by source truth.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Active Overlay Recording Runtime Foundation`
Package Posture: `Workstream active / BP1 accepted / BP2 accepted / BP3 approved / SLC-051 implemented / SLC-052 implemented / SLC-053 active / SLC-054 through SLC-055 queued same-branch continuation`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-051` Active Overlay recording target foundation | Workstream implemented / pending H1 and later proof | Define active Overlay Profile membership as the recording target while preserving Overlay Profile, Overlay Display, and Monitor Group separation. | Implemented as target/session truth only; recording execution and file writing remain blocked |
| `SLC-052` HUD Overlay recording launcher and target transparency | Implemented | HUD Overlay card launcher placeholder, active target/status preview, and active monitored monitor transparency are implemented without real Start/Stop, tray/export/provider scope, recording execution, file writing, or standalone Recording Control window creation. | Complete |
| `SLC-053` standalone Recording Control window foundation | Active same-branch Workstream continuation | Implement compact normal OS-level Recording Control window behavior, independent lifetime, minimization/taskbar restore, target/status summary, and secondary settings-window routing without admitting recording execution. | Active continuation seam on this carrier |
| `SLC-054` durable recording output contract | Queued same-branch Workstream continuation | Propose graph/plot-ready output file contract and proof expectations before or alongside approved recording execution. | Queued continuation after SLC-053 unless Workstream Green, named blocker, or USER waiver is recorded |
| `SLC-055` validation/live proof readiness | Queued same-branch Workstream continuation | Plan validators, helper proof, H1, LV1, photo comparison, UTS strategy, null/stress coverage, and future-gated boundary proof. | Queued continuation after SLC-054 unless Workstream Green, named blocker, or USER waiver is recorded |

Single-Slice Package User Approval: `Not required - five concrete planned slices are admitted; only SLC-051 is implemented in this bounded approval.`
Package Completion State: `In Workstream / SLC-051 complete / SLC-052 complete / SLC-053 in progress / SLC-054 through SLC-055 queued`

## Element-to-Phase Proof Matrix

Matrix Status: `Historical`
USER Review Status: `Accepted`
Open Element Questions: `Queued`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Element Validation Ledger Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AOR-001` | Active Overlay Profile recording target | Touched | SLC-051 defines how recording derives membership from the active Overlay Profile without adding a separate Recording Profile selector. | Workstream proof asserts active Overlay Profile membership drives target selection and that Overlay Profile state remains display-owned. | H1 must stress null active profile, switched active profile, deleted profile, high-volume profiles, and stale membership references. | LV1 required if user-visible target/status is added; otherwise state-only waiver must name validator proof. | UTS required for visible target/status; waived only for pure state-only proof. | Actual recording execution remains future-gated unless source truth admits it. | Accepted | This plan |
| `AOR-002` | HUD Overlay card recording launcher and target preview | Touched | SLC-052 implements HUD Overlay card launcher placeholder, target/status preview, and active monitor transparency while real Start/Stop remains future-gated until recording execution and file writing are admitted. | Workstream proof includes launcher/preview state, future-gated Recording Control launcher state, active monitor transparency, and no tray/export/provider coupling. | H1 must stress compact/default layout, dirty/state transitions where relevant, and regression against Dashboard card controls. | LV1 must use real user-level mouse/keyboard input, before/after screenshots, compact/default photos, hover/focus proof, and pessimistic visual review if visible. | UTS must include a user-facing item that asks USER to verify HUD Overlay card launcher/target preview, active monitor transparency, compact/default visual correctness, and absence of tray/export/provider scope; any waiver must name why no visible runtime shipped. | Tray recording controls, real Start/Stop, file writing, and recording execution remain future-gated unless admitted later. | Accepted | This plan |
| `AOR-003` | Active monitored monitors transparency | Touched | SLC-052 shows which currently active monitors are under the selected Overlay Profile in the HUD Overlay card. | Workstream proof includes null/stale filtering from SLC-051 plus visible count/name transparency in the HUD Overlay card. | H1 must compare Dashboard, Manage Monitors, Overlay Profile, and Overlay Display behavior for regressions. | LV1 must capture focused card screenshots at default and compact sizes if visible. | UTS required if visible in Dashboard/HUD Overlay card. | Monitor Group configuration remains owned by Manage Monitors / Sensor Command Center. | Accepted | This plan |
| `AOR-004` | Standalone Recording Control window | Planned | SLC-053 implements an independent compact OS-level NDAI Recording Control window that opens from the HUD Overlay card and can remain open when Dashboard is closed/minimized. | Workstream proof must include launch, close/minimize, taskbar restore where feasible, independent movement/lifetime, target/status summary, future path/settings routing, focus/dirty guard if settings mutate, and no Dashboard child-window dependency. | H1 must stress window lifetime, compact minimum size, real resize behavior, close/minimize, save/discard/cancel if dirty state exists, and no Dashboard input bleed-through. | LV1 must use visible real mouse movements/clicks, keyboard input where relevant, photos before/after every user-facing state, and compact/default comparison. | UTS required because this is a user-facing window. | Real Start/Stop, file writing, and advanced bulky settings remain future-gated or move behind secondary surfaces only after USER/source-truth admission. | Accepted | This plan |
| `AOR-005` | Durable recording output contract | Planned | SLC-054 will propose and implement or validate the output file contract needed for future graph/plot workflows when source truth admits that seam. | Workstream proof must include schema/header/row determinism, timestamp/value/source identity, path handling, null/no-data behavior, and parse/readback proof. | H1 must stress file path errors, long recordings, high-volume sensors, interrupted write, and compatibility with future graph/plot usage. | LV1 requires user-facing proof only if output settings or recording execution are visible; otherwise helper proof can satisfy file-contract validation. | UTS required if a user can create/select/open output files; otherwise Workstream/H1 proof may be sufficient. | Export/share/import remains a future package and is not authorized by an output contract alone. | Accepted | This plan |
| `AOR-006` | Recording execution | Future | Not implemented by Stage 2. Workstream Entry must decide whether actual Start/Stop execution belongs in this package or needs a separate USER approval seam. | Boundary proof must show no runtime recording execution is added before USER approval. | H1 must confirm no fake recording or unauthorized file writes. | LV1 absence proof if visible buttons exist without execution; otherwise future branch owns execution proof. | USER acceptance belongs to the approved implementation seam that admits execution. | Boundary keeps recording execution out of current release gating until USER grants explicit implementation approval for file-writing/runtime recording behavior in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-007` | Tray recording controls | Future | No implementation in this package unless USER separately approves tray scope. | Boundary proof must show no tray Start/Stop control was added. | H1 must confirm tray behavior unchanged. | LV1 absence proof only if visible UI could imply tray controls. | Future USER acceptance belongs to a tray-controls branch or approved scope revision. | Boundary keeps tray recording controls out of current release gating until USER grants a tray-control scope decision in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-008` | Export/share recording output | Future | No export/share/import implementation in this package. | Boundary proof must show no export/share UI or workflow was added. | H1 must confirm output contract does not become export/share behavior. | LV1 absence proof only if user-facing UI could imply export/share. | Future USER acceptance belongs to export/share branch or approved scope revision. | Boundary keeps export/share/import out of current release gating until USER grants an export/share scope decision in this branch or a later carrier. | Deferred With Waiver | This plan |
| `AOR-009` | Provider/model integration | Future | No provider/model/memory work in this package. | Boundary proof must show active-overlay recording has no provider/model dependency. | H1 must confirm FAM-007 boundaries remain unchanged. | LV1 absence proof only if UI could imply provider/model integration. | Future USER acceptance belongs to FAM-007 or other approved branch. | Boundary keeps provider/model/memory integration out of current release gating until USER grants provider/model scope in FAM-007 or another approved carrier. | Deferred With Waiver | This plan |
| `AOR-010` | Validation/live proof governance for recording surfaces | Planned | SLC-055 will update validators/helpers only as required by implemented runtime seams. | Workstream proof must include source-truth validators, HUD validators, internal sandbox, validation suite, JS checks when changed, output-file helper proof when relevant, and matrix coverage. | H1 must be pessimistic and compare planned behavior to actual code, screenshots, and helper outputs. | LV1 must use real user-facing launcher where feasible, real cursor movement/clicks, compact/default photo comparison, and explicit blocker if real input is impossible. | UTS handoff required after LV1 for user-facing changes unless explicitly waived. | Validator fallbacks must not replace real input without USER-visible blocker/digest. | Accepted | This plan |

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
- Fold-Down Target: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md remains historical rollback receipt; the released foundation branch remains the PR #222 historical planning/governance receipt; this implementation carrier remains active until its own lifecycle closes.`

### Changed Surface: Docs/branch_plans/README.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve incoming branch-plan governance, status vocabulary, and current-main planning rules while retaining the FAM-006 implementation carrier's branch-plan review and overlap-intent requirements.`
- Why This File Was Touched: `The active FAM-006 implementation carrier carries branch-plan governance hardening from USER Branch Plan Contract and review-bundle freshness repair work, while current origin/main now carries newer repo-wide branch-plan governance from release-readiness source-truth intake.`
- Owned Behavior / Fact Class: `Branch-plan governance index, plan-shape requirements, and reusable planning status semantics.`
- Canonical Owner / Source Owner: `Docs/branch_plans/README.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High when current-main branch-plan governance updates overlap FAM-006 branch-local planning contract and review-bundle hardening text.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main branch-plan governance as authority, preserve FAM-006 USER Branch Plan Contract and review-bundle trust-but-verify requirements only where they remain current and reusable, and do not let FAM-006 branch-local wording weaken newer repo-wide branch-plan rules.`
- Rebaseline Handling: `During FAM-006 current-main reconciliation, accept current-main README updates first, then carry forward only the minimal FAM-006 review-bundle / Branch Plan Contract semantics still required by phase governance, validation helper registry, and the active FAM-006 branch plan.`
- Validation Proof: `Pre-reconciliation overlap audit must pass after this ledger repair; branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `Docs/Main.md routes Branch Change Intent Ledger ownership to active branch plans, Docs/phase_governance.md defines the overlap-intent gate, Docs/validation_helper_registry.md owns review-bundle helper requirements, and this branch plan records the FAM-006-specific intent.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-reconciliation overlap-intent repair for this file; no approval is granted for FAM-007 mutation, Workstream Entry analysis, runtime implementation, PR creation, merge, release, or stale artifact handling beyond approved Stage 2 review materials.`
- Fold-Down Target: `Docs/branch_plans/README.md remains repo-wide branch-plan governance; FAM-006-specific implementation-carrier proof remains in this active branch plan and branch record.`

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
- Fold-Down Target: `PR #222 preserves the released foundation planning receipt; this active implementation carrier now owns the next runtime implementation path after Workstream Entry and separate bounded implementation approval.`

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
- Fold-Down Target: `PR #222 preserves compact roadmap fold-down text for the released foundation; this active implementation carrier now owns the next runtime implementation path after Workstream Entry and separate bounded implementation approval.`

### Changed Surface: Docs/branch_plans/retirement_index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Retire the old Recording Profile branch plan from active planning posture, preserve the released foundation as PR #222 historical planning receipt, and keep this implementation carrier active for the next runtime path.`
- Why This File Was Touched: `The old carrier remains as rollback receipt only; the retirement pointer must not imply this active implementation carrier is also retired or only future planning.`
- Owned Behavior / Fact Class: `Branch plan lifecycle and active plan posture.`
- Canonical Owner / Source Owner: `Docs/branch_plans/retirement_index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low to Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Keep historical plan rows, keep the old Recording Profile and released foundation plans retired where applicable, and do not retire this active implementation carrier until its own PR/merge lifecycle closes.`
- Rebaseline Handling: `Preserve incoming current-main retired-plan rows, released foundation historical posture, and this active implementation carrier posture.`
- Validation Proof: `Branch readiness planning fixture validation must pass.`
- Fallback Evidence: `Use this plan, the active branch record, released foundation historical record, and retirement index rows as lifecycle evidence.`
- USER Decision / Waiver: `USER approved Stage 2 setup and did not authorize old branch deletion.`
- Fold-Down Target: `PR #222 retires the released foundation planning carrier from active planning posture; this implementation carrier remains active until Workstream/PR lifecycle closes or USER separately retires it.`

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
- Conflict Resolution Rule: `Preserve incoming current-main FAM-007 historical authority receipt and do not treat the FAM-007 branch as FAM-006 authority; keep FAM-006 active implementation-carrier authority in Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md and released foundation traceability in its historical record.`
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
- Fallback Evidence: `Docs/validation_helper_registry.md owns helper responsibility; START_HERE.md carries packet/upload proof after helper execution, and pre-generation cleanup removes matching zip artifacts plus prior folder contents before the regenerated folder and one timestamped ZIP artifact are created.`
- USER Decision / Waiver: `USER approved bounded overlap-intent repair for this helper before current-main reconciliation; no waiver authorizes stale ZIP output.`
- Fold-Down Target: `Reusable helper remains shared; branch-specific proof is recorded in the review packet and PR Readiness closeout.`

### Changed Surface: Docs/codex_modes.md

- Surface Class: `prompt/template`
- Change Intent: `Preserve incoming origin/main execution-mode guidance for Branch Planning BP1/BP2/BP3, local C:\Nexus USER review hub routing, and external operational-state placement while keeping FAM-006 active-overlay recording as the active implementation carrier.`
- Why This File Was Touched: `The FAM-006 branch carries older mode-mirror wording from review-packet and Stage 2 governance repair work, while incoming origin/main now contains the Governance Phase Lifecycle Reform and USER Review Hub model that should become current repo authority during reconciliation.`
- Owned Behavior / Fact Class: `Compact Codex execution-mode mirror for phase routing, review packet posture, and USER-facing planning handoff behavior.`
- Canonical Owner / Source Owner: `Docs/codex_modes.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium to High when incoming Branch Planning and USER Hub mode guidance overlaps older FAM-006 Workstream Entry / Desktop review packet wording.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `During current-main reconciliation, preserve incoming origin/main mode guidance for BP1, BP2, BP3, C:\Nexus USER, external operational-state routing, and USER-facing technical-metadata boundaries; retain FAM-006-specific active-overlay recording identity only in the FAM-006 branch record, branch plan, family vision, and refreshed USER review artifacts.`
- Rebaseline Handling: `Accept current-main codex mode reforms as authority, then repair only any FAM-006 next-decision or review-packet wording needed to route this branch legally under the merged lifecycle. Do not reintroduce old Desktop/OneDrive active upload wording or BR2-to-Workstream shortcuts.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, runtime-fam006 validation suite, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `Docs/phase_governance.md owns canonical phase law; Docs/branch_plans/README.md owns BP1/BP2/BP3 artifact rules; Docs/governance_efficiency_operating_model.md owns the USER Hub and external operational-state model; this branch plan records why FAM-006 overlaps the compact mirror during reconciliation.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-rebaseline overlap-intent repair for this file; no approval is granted for Workstream implementation, BP3 approval, runtime mutation, FAM-007 mutation, PR creation, merge, release, or Governance worktree mutation.`
- Fold-Down Target: `Docs/codex_modes.md remains a compact mirror of merged governance law; FAM-006 branch-specific planning proof remains in the FAM-006 branch record and active branch plan until the branch lifecycle closes.`

### Changed Surface: Docs/codex_user_guide.md

- Surface Class: `prompt/template`
- Change Intent: `Preserve incoming origin/main USER-facing guidance that explains the Branch Planning lifecycle, local C:\Nexus USER hub, temporary USER review artifacts, and technical-metadata boundaries without weakening FAM-006 active-overlay recording branch identity.`
- Why This File Was Touched: `The FAM-006 branch contains older user-guide context from review-packet repair history, while incoming origin/main carries updated user-facing governance guidance from the Governance Phase Lifecycle Reform and USER Review Hub repair.`
- Owned Behavior / Fact Class: `USER-facing Codex workflow guidance and phase/review artifact explanation.`
- Canonical Owner / Source Owner: `Docs/codex_user_guide.md`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Medium when incoming USER Hub / Branch Planning guidance overlaps older FAM-006 review-packet wording.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming origin/main user-guide explanations for the reformed lifecycle and local USER hub. Keep FAM-006 branch-specific next decisions and active-overlay recording details out of the shared guide except where repo-wide examples remain accurate.`
- Rebaseline Handling: `During current-main reconciliation, accept current-main user-guide guidance as shared authority and repair any branch-local artifacts separately so the guide does not become a FAM-006-specific status ledger.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; branch governance validation, release-readiness health gate, branch readiness planning fixture validation, FAM-006 validators, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `Docs/Main.md separates durable docs from live operational truth; Docs/governance_efficiency_operating_model.md defines USER Hub review artifacts as temporary USER/ChatGPT context aids; Docs/phase_governance.md and Docs/branch_plans/README.md own the BP1/BP2/BP3 decision model.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-rebaseline overlap-intent repair for this file; no approval is granted to migrate local USER files, change sidecar/unique-ZIP policy, implement runtime work, or mutate unrelated family branches.`
- Fold-Down Target: `Docs/codex_user_guide.md remains shared user guidance; FAM-006-specific accepted outcomes fold into durable FAM-006 source-truth owners after legal Branch Planning and implementation phases.`

### Changed Surface: dev/orin_branch_readiness_planning_fixture_validation.py

- Surface Class: `validator/helper`
- Change Intent: `Preserve incoming origin/main fixture-validator coverage for Branch Planning BP1/BP2/BP3, USER-facing technical-metadata rejection, local C:\Nexus USER review packet rules, and rebaseline overlap-intent checks while retaining only compatible FAM-006 review-packet hardening semantics.`
- Why This File Was Touched: `The FAM-006 branch carries older fixture-validator changes for USER Branch Plan Review and review-packet proof, while incoming origin/main now introduces broader Branch Planning and USER Hub regression fixtures that should govern future branches.`
- Owned Behavior / Fact Class: `Reusable regression fixture validation for branch planning, USER review artifact structure, Branch Change Intent Ledger coverage, and review packet guardrails.`
- Canonical Owner / Source Owner: `dev/orin_branch_readiness_planning_fixture_validation.py`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High when incoming BP1/BP2/BP3 fixture semantics overlap older FAM-006-specific USER Branch Plan Contract fixture names and review-packet checks.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming origin/main fixture-validator coverage and fixture names for Branch Planning reform, USER Hub metadata guards, and overlap-intent enforcement. Carry forward FAM-006-specific review-packet hardening only where it remains compatible with merged BP1/BP2/BP3 and C:\Nexus USER rules.`
- Rebaseline Handling: `During current-main reconciliation, accept the incoming validator as the base, preserve new BP fixture coverage, remove obsolete FAM-006-only fixture expectations when they conflict with merged governance, and rerun branch-readiness planning fixture validation before claiming green.`
- Validation Proof: `Pre-reconciliation overlap audit must pass; python dev\orin_branch_readiness_planning_fixture_validation.py must pass; branch governance validation, worktree-confinement gate, release-readiness health gate, FAM-006 validators, runtime-fam006 validation suite, source-owner marker validation, and compileall must pass before current-main reconciliation resumes.`
- Fallback Evidence: `Incoming origin/main adds BP1/BP2/BP3 fixtures, technical-metadata fixtures, and Desktop active-upload rejection fixtures; Docs/validation_helper_registry.md owns helper/validator responsibilities; this active branch plan records the FAM-006 overlap intent needed before reconciliation.`
- USER Decision / Waiver: `USER approved bounded FAM-006 pre-rebaseline overlap-intent repair for this validator; no approval is granted for Governance worktree mutation, fixture deletion outside reconciliation needs, runtime implementation, or PR creation.`
- Fold-Down Target: `The fixture validator remains reusable governance infrastructure; FAM-006 branch-specific reconciliation proof folds into the FAM-006 branch plan/record and later PR Readiness packet.`

## USER Branch Plan Review Gate

USER Branch Plan Review: Required - Stage 2 creates a USER branch-plan review packet and future Workstream Entry must present a full readable implementation plan before runtime work begins.
Review Status: Accepted by USER - BP1 USER Branch Vision Review and BP2 USER Branch Plan Review are accepted; BP3 Workstream Entry / Orchestration Validation is approved by USER.
Contract Status: Complete - BP2 Branch Plan Review is accepted by USER and BP3 is approved by USER; neither authorizes Workstream implementation by itself.
Packet Reviewability State: Reviewable when the regenerated `C:\Nexus USER\FAM-006` packet validates.
USER Gate State: USER Accepted for BP2; USER Approved for BP3.
USER Response Proof: BP1 accepted by USER through the BP1 Acceptance And BP2 Preparation approval; BP2 accepted by USER through BP2 Acceptance And BP3 Preparation approval; BP3 approved by USER through BP3 Workstream Entry / Orchestration Validation approval.
USER Response Digested: BP1 and BP2 accepted and digested into BP3 planning constraints; BP3 approved and digested into SLC-051 Workstream implementation guardrails.
Acceptance / Waiver / Revision / Rejection Receipt: BP1 accepted; BP2 accepted; BP3 approved.
Contract Version / Revision: v10 records bounded SLC-051 target/session truth implementation, fixes post-seam final-stop drift, records bounded SLC-052 HUD Overlay target preview implementation, and admits SLC-053 as active same-branch Workstream continuation.
USER Review Hub Packet: `C:\Nexus USER\FAM-006`
Local USER Hub Packet: `C:\Nexus USER\FAM-006`
Local USER Hub ZIP: `C:\Nexus USER\FAM-006__YYYYMMDD-HHMMSS.zip`
USER Review Packet Finding: Complete for BP3 - Branch Planning loaded and digested the local USER hub packet with `START_HERE.md` as a plain-language index, `USER_BRANCH_PLAN_REVIEW.md` as accepted BP2 context under `Review Aids`, `WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md` as the single primary current-gate file under `USER Review`, accepted BP1/BP2 context under `Review Aids`, copied context under `Source Truth Context`, and exactly one timestamped USER upload zip at `C:\Nexus USER\FAM-006__YYYYMMDD-HHMMSS.zip`. Helper output or Codex chat digest must prove Source HEAD/current branch HEAD freshness, copied source truth, loaded/digested or waiver/blocker status, Packet Reviewability State, USER Gate State, and any waiver/blocker status; USER-facing files must not center active branch status, current HEAD, current origin/main, validation state, PR state, or ZIP hash. Technical proof belongs in Codex chat digest, helper output, validator output, or external governance state.
Current-Main / Review-Hub Blocker: `Current-main reconciliation is complete. The next packet-generation pass must use C:\Nexus USER\FAM-006 as the active readable local USER hub folder and exactly one timestamped C:\Nexus USER\FAM-006__YYYYMMDD-HHMMSS.zip upload artifact; cloud-backed Desktop/OneDrive paths are mirror/convenience surfaces only.`
Family Vision Context: `FAM-006 owns Monitoring HUD, Dashboard, Overlay Profile, Overlay Display, Monitor Group, Sensor Command Center, and active-overlay-driven recording planning; this contract must keep recording connected to the overlay system instead of creating a second profile system.`
Feature Vision: `The recording feature should derive its target from the active Overlay Profile, show that target in the HUD Overlay card, later open a compact standalone Recording Control window, and keep graph/log viewing separate as future Native Log Loader work.`
Branch Goal: `Implement the active-overlay-driven recording runtime foundation safely, beginning with trustworthy target proof and only then moving to HUD visibility, Recording Control, output contract, and proof surfaces after USER-approved implementation seams.`
Plain-Language Branch Goal: Establish the corrected FAM-006 recording branch where recording is driven by the active Overlay Profile instead of a separate Recording Profile.
What Will I Actually See, And Where Will I See It?: USER should eventually see the HUD Overlay card act as the recording launcher and target/status preview: active Overlay Profile name, Recording Target / Active Recording Target label, concise active target summary, future-gated recording status, and an Open Recording Control action. The Recording Control window should be a compact standalone normal Windows/NDAI window with target summary, future Start/Stop placement after execution is admitted, folder/path summary after settings are admitted, and route to secondary advanced/settings windows when content would become bulky. Native Log Loader is a separate future graph/log viewer, not the recording control surface.
How It Will Function: `The active Overlay Profile remains the source of recording target membership; future recording reads active overlay membership, preserves Monitor Group and Overlay Profile ownership boundaries, keeps execution and file writing behind explicit approval, and uses future output contracts that can feed graph/plot workflows.`
User Experience Flow: `USER starts in the Dashboard HUD Overlay card, reviews active target/status, opens the standalone Recording Control window when admitted, and uses secondary settings/details windows only for bulky configuration that should not crowd the compact control surface.`
Planned User-Facing Outcome: SLC-051 adds no visible recording controls; future user-facing outcome is HUD Overlay launcher/target preview, transparent active monitor target, and a compact standalone Recording Control window after later approval.
End-State Vision: The completed active-overlay recording foundation should make recording feel automatic and connected to the overlay the USER already loaded. Overlay Profile defines what is visible/tracked; active overlay membership defines the recording target; the HUD Overlay card previews that target and launches the compact Recording Control window; the Recording Control window is a small standalone control surface; the Native Log Loader remains a separate future viewer for graphing and inspecting completed logs.
Visual / Behavioral Description: Future recording should start from the HUD Overlay card as a truthful target/status preview, not from a separate Recording Profile chooser. The user should open a compact, taskbar-restorable Recording Control window from the HUD Overlay card, keep it movable/minimizable independently of the Dashboard, and use secondary settings/details windows only when the main control surface would become too large.
Visual / Functional Walkthrough: USER starts at the Dashboard HUD Overlay card, sees the active Overlay Profile and target/status preview, opens the standalone Recording Control window when ready, and later uses that window for compact recording controls after execution is admitted. Advanced path/format/settings details move to secondary windows. Future log files are designed so a separate Native Log Loader can graph data over time, but loader implementation remains future-gated.
Surface Map: HUD Overlay card = launcher and target/status preview; Recording Control window = compact standalone control surface; secondary settings/advanced windows = bulky configuration surfaces when needed; Overlay Profile = source of active recording target membership; Monitor Group = reusable sensor/source group; files/output = future graph/plot-ready recording data; Native Log Loader = future separate graph/log viewer; tray/export/provider/theme/FAM-007 = future-gated surfaces outside this approval.
Implementation Breakdown: SLC-051 target foundation is implemented as target/session truth only. SLC-052 HUD Overlay launcher/target transparency is implemented as read-only target preview and future-gated launcher placeholder. SLC-053 standalone Recording Control window and secondary settings surfaces, SLC-054 output contract, and SLC-055 validation/live proof readiness remain the planned same-branch implementation package for this active carrier.
Element-to-Phase Proof Matrix: Present in this plan for AOR-001 through AOR-010.
Hardening Plan: Future H1 must pressure-test active overlay membership, Dashboard/HUD Overlay behavior, standalone settings window behavior, output contract, concept separation, compact/default UI, and future-gated boundaries.
Live Validation / UTS Plan: Future LV1 must use real user-level input, visible cursor movement/clicks, compact/default screenshots, focused per-element screenshots, output-file proof where applicable, and UTS handoff or explicit waiver.
Open USER Questions: No per-seam USER approval is required for same-branch continuation while Workstream remains In Progress with no named blocker or waiver. Later seams must still answer output file contract, Recording Control details, snapshot-at-start execution behavior, and per-overlay effective polling policy questions when they become active.
USER Design Review Questions: No per-seam USER approval is pending while Workstream remains In Progress with no named blocker or waiver. USER may still revise/hold/waive, but the active execution route is SLC-052 same-branch continuation.
Codex Recommendations: Accept the active-overlay-driven recording product model: recording targets derive from the active Overlay Profile, the HUD Overlay card previews target/status and launches recording control, the standalone Recording Control window stays compact and OS-level, Native Log Loader remains a separate future viewer, and per-overlay effective polling policy is recorded as future FAM-006 architecture so SLC-051 does not block it.
Implementation Options: Option A - Target model proof first; Option B - target preview in the HUD Overlay card; Option C - standalone Recording Control window shell first; Option D - live Start/Stop planning later after recording execution and file writing are admitted. Codex recommends Option A first, with Option B and C following only after the target model is trustworthy.
Implementation Options / Product Shapes: `Option A - target model proof first; Option B - HUD Overlay target preview; Option C - standalone Recording Control window shell first; Option D - later live Start/Stop after execution/file writing approval. These are product shapes for USER review before engineering staging.`
Recommended Direction: Codex recommends target model proof first for SLC-051, then HUD target preview and the standalone Recording Control window in later seams unless repo truth selects minimal read-only proof markers sooner. For later recording execution, Codex recommends snapshot-at-recording-start as the default log model unless USER revises it, while SLC-051 should prove the live current active-overlay target because no recording is occurring yet.
Why This Fits The Nexus Vision: This direction keeps recording intuitive, avoids a confusing second profile system, keeps the HUD lightweight, gives the user a compact normal OS window for ongoing control, keeps graph/log viewing separate from recording control, and protects future log quality by recording per-overlay effective polling policy as architecture before execution exists.
USER Design Direction Decision: Accepted active BP1 USER response under the post-PR #248 two-axis gate model. Active Overlay Profile membership is the recording target source; snapshot-at-start is the default target model; the HUD recording card remains small and quick-access; the standalone Recording Control window carries richer detail; hidden target state and a separate Recording Profile system remain rejected unless USER later reopens them.
Current Branch Scope: Current branch scope is the accepted active-overlay-driven recording end-state foundation, including target model proof, HUD Overlay card launcher/target-preview planning, Recording Control window planning, secondary settings planning, output-contract planning, and validation/live proof planning after separate implementation approval.
Future-Gated Scope: Future-gated scope includes recording execution, file writing until admitted, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup, PR, merge, release, issue mutation, and durable Native Log Loader source-truth mutation.
How Codex Would Build This After USER Accepts The Direction: `SLC-051 target/session truth is implemented. Because BP3 approved the same-branch Workstream package and no named blocker or waiver is recorded, Codex must continue to SLC-052 with only the HUD Overlay launcher/target-preview surface within accepted guardrails before continuing to later seams.`
Implementation Staging Notes: SLC-051 through SLC-055 remain implementation scaffolding for the accepted end-state until separately approved. Target model work comes first on this active runtime carrier because HUD launcher/preview, Recording Control window, output contract, validators, H1, LV1, and UTS proof all depend on a trustworthy definition of what would be recorded.
Alternatives / Tradeoffs: The prior profile-loaded Recording Profile route is preserved only as historical rollback receipt because it did not match the clarified USER recording vision.
USER Decisions Needed: Bounded Workstream implementation approval for SLC-051 Active Overlay recording target foundation is the next USER decision. Runtime execution, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, release execution, issue mutation, Governance worktree mutation, and durable Native Log Loader implementation remain pending decisions.
USER Review Response: BP1 accepted by USER through the BP1 Acceptance And BP2 Preparation approval; BP2 accepted by USER through BP2 Acceptance And BP3 Preparation approval; BP3 approved by USER through BP3 Workstream Entry / Orchestration Validation approval.
Codex Response Digest: BP1 and BP2 acceptance digested into BP3 planning constraints, BP3 approval digested into SLC-051 guardrails, SLC-051 implementation completed target/session truth, and SLC-052 implementation completed HUD Overlay recording target preview/launcher-placeholder transparency: active Overlay Profile membership is the recording target source; snapshot-at-start is the default target model for future execution; the HUD recording card shows target profile/count/name transparency; the standalone Recording Control window carries richer target/status/readiness/control detail in SLC-053; hidden target state is rejected; separate Recording Profile remains outside this branch; Native Log Loader and per-overlay effective polling remain future-gated; actual current owners were verified as HUD state/JS/HTML/CSS plus validators. SLC-053 through SLC-055 and all recording execution remain future-gated until source truth admits them.
Implementation Constraints Created By USER Response: SLC-051 is complete as target/session truth only; active Overlay Profile membership remains the future recording target source; no separate Recording Profile system or recording-specific sensor chooser is admitted; recording execution, file writing, real Start/Stop behavior, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, and durable Native Log Loader mutation remain blocked; future recording execution should default to snapshot-at-recording-start for clean logs unless USER revises it; SLC-051 proves the live current target because it records nothing; target proof preserves null/empty/selected/switched/deleted-stale/duplicate-stale-ID/high-volume states and existing Overlay Profile, Overlay Display, Monitor Group, Dashboard, Manage Monitors, and Sensor Command Center behavior; per-overlay effective polling policy remains future-planning/source-truth constraint; `desktop/ui/dashboard_hud_panel.py` is not the current owner unless later repo truth creates it.
USER Rejected / Deferred Ideas: Rejected for this direction is the separate profile-loaded Recording Profile system and any duplicated CPU FAST/CPU SLOW Monitor Group workaround as the desired long-term polling model. Deferred are recording execution, file writing, real Start/Stop controls, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup/deletion, durable Native Log Loader implementation/source-truth mutation beyond future planning, per-overlay polling-policy implementation, and advanced/bulky Recording Control settings.
Vision Delta / Source-Truth Impact: Active branch plan, branch record, family vision, and local USER hub BP3 review artifact preserve the accepted active-overlay recording branch identity while treating pre-PR #248 BP1/BP2/BP3 packets as superseded legacy evidence for active decisions. Family vision records per-overlay effective polling policy as a future FAM-006 planning constraint because it affects recording target model design. Backlog/roadmap compact pointers show implementation-carrier setup, BP1/BP2 accepted posture, BP3 approved posture, SLC-051 complete posture, and later-seam pending posture. Native Log Loader remains future planning input only and is not admitted for durable implementation.
Contract Change Log: v1 introduced USER-facing Branch Plan Review packet with end-state/options sections. v2 hardened it into USER Branch Plan Contract with closed-loop USER response/digest, implementation constraints, source-truth impact, confirmation loop, stale-packet protection, and waiver semantics. v3 digested USER recording product-model feedback. v4 recorded pre-PR #248 acceptance evidence on the released foundation planning carrier. Post-PR #248 reset marked those BP receipts superseded for active decisions and returned this implementation carrier to BP1 USER Branch Vision Review. v5 records active BP1 acceptance and prepares BP2 USER Branch Plan Review from the accepted vision. v6 records BP2 acceptance and prepares BP3 Workstream Entry / Orchestration Validation with file-ownership guardrails. v7 records BP3 approval and prepares the separate SLC-051 Workstream implementation approval decision. v8 records bounded SLC-051 target/session truth implementation.
Workstream Entry Result: BP3 approved - BP3 packet was reviewable and USER Gate State is USER Approved; SLC-051 implementation is complete as target/session truth only.
Contract Completion Checklist: BP2 accepted, BP3 approved, and SLC-051 implemented - accepted BP1, accepted BP2, approved BP3, and SLC-051 target/session truth context are preserved; later seams require separate USER approval before runtime expansion.
Accepted Scope: Accepted scope includes Branch Readiness Stage 2 setup, source-truth admission, released foundation traceability preservation, BP1 acceptance recording, BP2 packet regeneration, BP3 approval, and bounded SLC-051 target/session truth implementation.
Deferred Scope: Deferred scope is SLC-053 through SLC-055 beyond bounded same-branch continuation, recording execution, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge, release, issue mutation, artifacts/raw evidence handling beyond approved review packet, sibling-worktree mutation, old branch cleanup/deletion, and Governance mutation.
Rejected Scope: Requiring users to load a separate Recording Profile before recording sensors is rejected for this future recording path unless USER explicitly re-approves it.
Exact USER Decision Needed: No USER decision is required to continue same-branch Workstream execution while Completion Status remains In Progress. USER may still revise, hold, waive, or route to H1, but absent that intervention SLC-053 continues; recording execution remains blocked.
Implementation Approval: SLC-051 target/session truth approved and implemented; later runtime mutation remains blocked until separate USER decision.

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
Exact USER Decision Needed: `No USER decision is required for same-branch SLC-053 continuation because Workstream Completion Status is In Progress, Continue Decision is Continue, and no named blocker or USER waiver is recorded. USER may interrupt with a revision, hold, waiver, or H1 routing decision; recording execution, file writing, real Start/Stop controls, tray controls, export/share, Native Log Loader implementation, provider/model work, FAM-007 mutation, Governance mutation, PR creation, merge, release, issue mutation, and cleanup remain excluded.`
