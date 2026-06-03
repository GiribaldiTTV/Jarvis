# Branch Runtime Engineering Plan - FAM-006 Active Overlay Recording Runtime Implementation

Branch: `feature/fam-006-active-overlay-recording-runtime-implementation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Created From: `feature/fam-006-recording-profile-runtime-foundation` at `1f399003d2e6d13b34b567cd7f7900a709254bc9`
Current Plan Phase: `Renewed Live Validation LV1 complete for the first bounded Dashboard Recording card repair seam after USER accepted BP1/BP2, approved BP3, approved bounded Workstream implementation, approved renewed H1, and approved renewed LV1. Prior SLC-051 through SLC-055, H1, and LV1 proof/handoff remain durable superseded-route evidence for the old HUD Overlay placement. The revised Dashboard Recording card route now requires returned User Test Summary disposition before PR Readiness.`
Runtime Implementation Approval: `Bounded Workstream implementation approval was granted for the first Dashboard Recording card repair seam only. Implemented scope moves recording target/status preview to a dedicated Dashboard Recording card, preserves active Overlay Profile membership as the target source, keeps the HUD Overlay card overlay-focused, and keeps any Recording Control or secondary detail surface future/secondary. Recording execution, file writing, real Start/Stop controls, tray controls, export/share, and provider/model work remain future-gated unless source truth admits them.`
Current-Main Reconciliation Status: `Reconciled - governed current-main reconciliation through origin/main@9b64ac1b4faf4d29033e3a8f299a1293eb26f2d7 completed on this branch using a non-rewrite merge path. Incoming Branch Planning BP1/BP2/BP3, C:\Nexus USER, external operational-state placement, helpers, validators, fixtures, and USER review artifact rules are current-main authority. FAM-006 did not mutate FAM-007 source truth. Pre-PR #248 FAM-006 BP1/BP2/BP3 packets and receipts are superseded legacy evidence for active decision purposes because active Branch Planning now requires distinct Packet Reviewability State and USER Gate State proof. Active FAM-006 BP1 Branch Vision and BP2 Branch Plan are accepted by USER; BP3 for the Dashboard Recording card revision is approved by USER; Workstream implementation authority is not active until the separate bounded implementation approval is granted.`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Active Overlay Recording Runtime Implementation`
Owning Branch: `feature/fam-006-active-overlay-recording-runtime-implementation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Current Phase: `Live Validation`
Branch Runtime Engineering Plan: `Fresh runtime implementation carrier imported from the released active-overlay-driven recording planning contract.`
Engineering Plan Status: `Accepted`
Current Runtime Baseline: `FAM-006 Overlay Profile Runtime Foundation and Overlay Display Acceptance Foundation are released historical evidence. The profile-loaded Recording Profile Workstream route was rolled back by USER request and is preserved as historical receipt only.`
Branch Purpose: `Admit a corrected FAM-006 recording carrier where recording is driven by the active Overlay Profile membership rather than a separate loaded Recording Profile.`
Planned Runtime Delta: `The active planned delta must be revised. The accepted target-source model remains active Overlay Profile membership, but the recording target/status surface must move to a dedicated Dashboard Recording card instead of the HUD Overlay card before runtime repair can proceed. Secondary settings surfaces, Native Log Loader implementation, recording execution, file writing, tray controls, and export/share remain future-gated until source truth admits them.`
User-Facing Delta: `BP1 amendment and BP2 engineering plan accepted; BP3 orchestration approved; bounded Workstream repair implemented. The revised user-facing direction is now represented by a separate Dashboard Recording card for recording target/status and future recording controls; the HUD Overlay card remains overlay-focused. Prior HUD Overlay launcher/preview and standalone Recording Control window foundation are superseded-route evidence for active placement decisions.`
Source-Truth Delta: `Add this active branch authority and branch plan; move the old Recording Profile branch from active authority to historical/rollback receipt posture; update compact backlog/roadmap pointers to this corrected carrier; preserve released Overlay Profile and Overlay Display evidence.`
State / Config / Schema Delta: `SLC-051 adds activeOverlayRecordingTarget and activeOverlayRecordingTargetProof as read-only target/session truth derived from active Overlay Profile membership. SLC-054 adds an in-memory recording output contract schema, manifest, deterministic CSV render/parse helpers, and readback proof. It does not create a separate Recording Profile, recording execution state machine, file writing, tray controls, or Start/Stop behavior.`
Validator / Helper Delta: `SLC-051 extends FAM-006 HUD surface and internal sandbox validators to prove null active profile, empty membership, stale/deleted/missing active profile, high-volume membership, no hidden recording target state, and blocked recording execution/file writing. SLC-054 extends FAM-006 validators to prove deterministic output contract headers/rows, manifest shape, null/no-data handling, parse/readback, graph/plot readiness, and blocked recording execution/file writing. SLC-055 adds Workstream readiness proof for the full SLC-051 through SLC-055 package, H1/LV1/UTS routing, future-gated boundary preservation, and blocked execution/file-writing proof.`
Expected Changed Files / Surfaces: `desktop/monitoring_hud_state.py; desktop/desktop_renderer.py; desktop/recording_output_contract.py; nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.js; dev/orin_monitoring_hud_surface_validation.py; dev/orin_monitoring_hud_internal_sandbox_validation.py; Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md; Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `Prior SLC-051 through SLC-055 are implemented for the superseded accepted route. The approved revised Workstream seam implemented SLC-052 as a Dashboard Recording card target/status surface, preserved SLC-051 target-source truth, kept SLC-053 secondary/standalone Recording Control future-gated, preserved SLC-054 output contract boundaries, and refreshed SLC-055 validator proof readiness for the revised route.`
Per-Seam Implementation Checklist: `Complete for the bounded Dashboard Recording card repair seam. SLC-052 is remapped from HUD Overlay launcher/target preview to Dashboard Recording card target/status placement. SLC-053 remains future/secondary; no standalone/native recording control is active. SLC-051 target-source truth, SLC-054 output contract boundaries, and SLC-055 proof readiness remain preserved.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks when JavaScript changes, H1 checks, LV1 real-input proof where user-facing, compact/default photo comparison, null/stress proof, and regression proof for Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, and Overlay Display.`
Per-Seam User-Facing Proof Checklist: `Deferred until approved runtime seams on this active implementation carrier. Any future visible control/window/status must carry real user-level mouse/keyboard proof, hover/focus screenshots, compact/default screenshots, dirty/state transition proof where applicable, and UTS handoff criteria.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, old branch cleanup/deletion, and artifacts/raw evidence handling beyond approved review bundles.`
Approval-Boundary Audit: `Approval boundary pending and blocked for runtime repair. This UFD pass is source-truth routing only and does not grant approval for code repair, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, renewed H1, renewed LV, UTS pass/waiver, or PR Readiness. The old Recording Profile Workstream remains rollback receipt only.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. Future runtime seams may touch HUD Dashboard, HUD Overlay card, Overlay Profile, Overlay Display, Manage Monitors, Sensor Command Center, and visual validation helpers; Workstream Entry must forecast exact overlap before implementation.`
Open Questions: `Active question: does USER return PASS, FAIL/repair feedback, or an explicit waiver for the refreshed User Test Summary at C:\Nexus USER\UTS - FAM-006.txt? Renewed LV1 exercised the Dashboard Recording card route through user-facing proof, confirmed HUD Overlay preservation, proved Recording Control remains future/secondary, and kept snapshot-at-recording-start as the default for future execution unless USER revises it.`
USER Planning Decisions: `USER clarified that recording should be active-overlay-driven, avoid separate Recording Profile selection, and preserve per-overlay effective polling policy as future planning. USER later returned Live Validation feedback on 2026-06-02 that recording should live in its own Dashboard card, not inside the HUD Overlay card. USER then accepted the BP1 Branch Vision amendment, accepted the BP2 Branch Plan revision, and approved BP3 Workstream Entry / Orchestration Validation for that Dashboard Recording card direction. This supersedes prior HUD Overlay card placement authority for active decisions.`
Plan Revision History: `v1 - Created during Branch Readiness Stage 2 setup after rollback of the profile-loaded Recording Profile Workstream route. v2/v3 - hardened and revised USER Branch Plan Contract into accepted active-overlay product plan. v4 - USER accepted the plan and redirected the released foundation carrier to planning/governance PR Readiness without runtime Workstream execution. Implementation-carrier v1 imports that accepted contract onto this active runtime implementation carrier. v14 - Records UFD-FAM006-20260602-001 from returned Live Validation feedback and routes to BP1/BP2/BP3 revision for dedicated Dashboard Recording card placement. v15 - Records USER acceptance of the BP1 Dashboard Recording card amendment and prepares BP2 Branch Plan Review for the revised engineering route. v16 - Records USER acceptance of the revised BP2 Dashboard Recording card engineering plan and prepares BP3 Workstream Entry / Orchestration Validation. v17 - Records USER approval of BP3 and prepares the separate bounded Workstream implementation approval decision. v18 - Records bounded Workstream implementation of the Dashboard Recording card repair seam and routes next to renewed Hardening H1. v19 - Records renewed H1 green for the Dashboard Recording card repair seam and routes next to renewed Live Validation LV1. v20 - Records renewed LV1 green, UTS handoff refresh, and helper robustness repairs; routes next to returned User Test Summary disposition.`
Plan-To-Implementation Traceability: `SLC-051 is implemented as target/session truth only in the current HUD / Overlay Profile owners and validators. SLC-052 is implemented in the Dashboard Recording card HTML/CSS/JS and FAM-006 validators as target/status preview and active monitor transparency. SLC-053 remains future/secondary for active placement decisions; the prior standalone Recording Control window foundation remains durable evidence only and the Dashboard card keeps its control surface disabled/future-gated. SLC-054 is implemented in desktop/recording_output_contract.py and FAM-006 validators as durable output contract schema/readback proof with execution/file-writing blocked. SLC-055 validator proof readiness is refreshed in FAM-006 validators for the revised Dashboard Recording card route. Renewed Hardening H1 and renewed Live Validation LV1 are green for the revised route. Returned User Test Summary disposition is pending after renewed LV1.`
Plan-To-Implementation Traceability Table: `SLC-051 traces to desktop/monitoring_hud_state.py, nexus_visual/monitoring_hud.js, dev/orin_monitoring_hud_surface_validation.py, and dev/orin_monitoring_hud_internal_sandbox_validation.py. Revised SLC-052 traces to nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, nexus_visual/monitoring_hud.js, dev/orin_monitoring_hud_surface_validation.py, and dev/orin_monitoring_hud_internal_sandbox_validation.py. SLC-053 future-secondary boundary traces to nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.js, desktop/desktop_renderer.py as superseded/future evidence, and FAM-006 validators. SLC-054 traces to desktop/recording_output_contract.py, dev/orin_monitoring_hud_surface_validation.py, and dev/orin_monitoring_hud_internal_sandbox_validation.py. SLC-055 traces to dev/orin_fam006_workstream_readiness.py and FAM-006 validators. Renewed H1 and renewed LV1 are complete; returned UTS results are not complete until USER returns PASS, FAIL/repair feedback, or explicit waiver.`
Hardening Comparison Checklist: `Green. Hardening H1 compared SLC-051 through SLC-055 implementation against accepted BP1/BP2/BP3, verified output contract readback, verified source markers for active Overlay Profile target/session truth, HUD target preview, Recording Control window foundation, output contract, and Workstream readiness, and preserved recording execution/file writing/real Start/Stop/tray/export/provider/FAM-007 boundaries.`
Live Validation Proof Or Waiver Checklist: `Green for renewed LV1 proof/handoff. Human-client shortcut validation passed at dev\logs\fam_006_human_client_validation\20260602_162121_890\human_client_manifest.json. The active replacement live-client self-QA passed at dev\logs\fam_006_monitoring_hud_live_validation\20260603_064843_590\manifest.json with PASS interaction manifest dev\logs\fam_006_monitoring_hud_live_validation\20260603_064843_590\monitoring_hud_live_client_interaction_manifest.json, mandatory Recording card visual-system screenshots, short video proof, and C:\Nexus USER\UTS - FAM-006.txt refreshed after LV1 PASS. Returned UTS results remain pending before PR Readiness.`
PR Readiness Fold-Down / Retention Checklist: `PR Readiness must fold down whatever this active implementation carrier actually completes, preserve the accepted v3/v4 contract in maintained source truth, and avoid claiming runtime implementation or release-user-facing behavior until approved runtime seams exist and pass proof.`
Release Readiness Public-Scope Translation Checklist: `Release language must describe only changes actually completed on this active implementation carrier; no active-overlay recording runtime, HUD control, Recording Control window, output file, or user-facing recording behavior may be claimed unless later approved runtime seams implement and validate them.`
USER Planning Review: `BP1 accepted, BP2 accepted, and BP3 approved under the post-PR #248 two-axis gate model for the revised Dashboard Recording card route. The imported active-overlay recording contract, revised BP1 packet, accepted BP2 packet, and approved BP3 packet are planning context; prior pre-PR #248 BP1/BP2/BP3 packet receipts remain superseded legacy evidence for active decision purposes.`
PR Fold-Down Packet: `Historical reference - PR #222 merged the released planning/governance foundation, PR #223 folded it down, and v1.7.25-prebeta published the release window that included PR #222/#223/#224. This implementation carrier remains active and separate from that released foundation traceability.`
Runtime Implementation Approval: `Used for the bounded Dashboard Recording card repair seam only. SLC-051 target/session truth remains accepted evidence; SLC-052 Dashboard Recording card target/status placement is implemented; SLC-053 standalone/native Recording Control remains future-secondary and superseded-route evidence for active placement decisions. Renewed H1, renewed LV, and PR Readiness require later phase proof. Recording execution and file-writing authority remain future-gated unless admitted by source truth.`

## USER Feedback Disposition

USER Feedback Disposition Required: Yes - returned USER Live Validation feedback changes branch vision, plan, proof, and phase routing.
UFD Ledger Status: Blocking
UFD Ledger Owner: Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md
Open UFD Count: 1
Blocking UFD Count: 1
Fold-Down Status: Pending
### UFD Item: UFD-FAM006-20260602-001
Feedback ID: UFD-FAM006-20260602-001
Feedback Source: `Returned USER Live Validation / User Test Review feedback`
Feedback Phase: Live Validation
Disposition Type: Current Branch Requirement
USER Decision State: Needs USER Decision
Owner Class: Branch Plan
Canonical Owner File: Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md
Workstream Severity: Level 3 - blocking branch vision and branch plan revision
Status: Blocking
Fold-Down Target: Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md owns UFD-FAM006-20260602-001 until the implemented Dashboard Recording card repair is hardened, live-validated, and digested or explicitly waived.
Feedback Summary: `Recording should live in its own Dashboard Recording card and should not live inside the HUD Overlay card. Active Overlay Profile membership remains the target source. Snapshot-at-recording-start remains the future execution default. Hidden target state and separate Recording Profile remain rejected. Native Log Loader and per-overlay polling remain future-gated.`
Pointer Locations: Active branch record, active branch plan, family vision, and USER review packet.
Affected Accepted BP1: `Yes - Surface map, end-state vision, user workflow, and user-facing behavior change from HUD Overlay card launcher/preview to Dashboard Recording card.`
Affected Accepted BP2: `Yes - SLC-052, SLC-053, affected surfaces, likely files, validators/helpers, H1/LV/UTS proof, rollback/safety plan, and exact implementation route require revision.`
Affected BP3: `Yes - Workstream Entry / Orchestration Validation re-checked accepted BP1/BP2 alignment, package size, SLC order, direct proof, and future-gated boundaries before code repair and is now USER Approved.`
Affected Workstream / H1 / LV: `Yes - bounded Workstream repair is implemented for the Dashboard Recording card route; renewed H1 is green; renewed LV1 is green; returned UTS disposition remains pending.`
No-Action Reason: Not Applicable - returned UTS disposition is required after renewed LV1.
Exact Next USER Decision: `Return completed C:\Nexus USER\UTS - FAM-006.txt results as PASS, FAIL/repair feedback, or WAIVED for the implemented, hardened, and live-validated Dashboard Recording card repair seam.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Active Overlay Recording Runtime Foundation`
Package Posture: `Workstream repair implemented / renewed H1 green / renewed LV1 green / UFD-FAM006-20260602-001 blocking until returned UTS disposition or waiver / prior Workstream-H1-LV1 proof preserved as superseded-route evidence / BP1 amendment accepted / BP2 plan accepted / BP3 approved`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-051` Active Overlay recording target foundation | Workstream implemented / pending H1 and later proof | Define active Overlay Profile membership as the recording target while preserving Overlay Profile, Overlay Display, and Monitor Group separation. | Implemented as target/session truth only; recording execution and file writing remain blocked |
| `SLC-052` Recording card target/status placement revision | Implemented and H1 green | Prior HUD Overlay card launcher/preview is superseded for active placement decisions; target/status and future recording controls now live in a dedicated Dashboard Recording card. | Complete pending renewed LV proof |
| `SLC-053` Recording Control / secondary surface decision | Future-gated / secondary | Prior standalone Recording Control window foundation remains durable evidence only; any standalone or secondary recording detail surface stays future/secondary after the Dashboard Recording card becomes primary. | Boundary preserved / future-gated |
| `SLC-054` durable recording output contract | Implemented | Durable graph/plot-ready output contract schema, manifest, deterministic CSV render/parse helpers, null/no-data handling, and readback proof are implemented without recording execution or file writing. | Complete |
| `SLC-055` validation/live proof readiness | Implemented | Validator/helper proof, H1 route, LV1 route, photo comparison expectations, UTS strategy, null/stress coverage, and future-gated boundary proof are recorded without running later phases. | Complete |

Single-Slice Package User Approval: `Not required - five concrete planned slices are admitted and SLC-051 through SLC-055 are implemented.`
Package Completion State: `Blocked for active advancement by UFD-FAM006-20260602-001 / prior Workstream-H1-LV1 evidence preserved / bounded Workstream repair implemented / renewed H1 green / renewed LV required before PR Readiness`

## Element-to-Phase Proof Matrix

Matrix Status: `Required - revision needed for Dashboard Recording card direction`
USER Review Status: `Pending USER Decision - renewed Live Validation LV1 requires USER response`
Open Element Questions: `Blocking - Dashboard Recording card engineering route queued`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Element Validation Ledger Owner: `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AOR-001` | Active Overlay Profile recording target | Touched | SLC-051 defines how recording derives membership from the active Overlay Profile without adding a separate Recording Profile selector. | Workstream proof asserts active Overlay Profile membership drives target selection and that Overlay Profile state remains display-owned. | H1 must stress null active profile, switched active profile, deleted profile, high-volume profiles, and stale membership references. | LV1 required if user-visible target/status is added; otherwise state-only waiver must name validator proof. | UTS required for visible target/status; waived only for pure state-only proof. | Actual recording execution remains future-gated unless source truth admits it. | Accepted | This plan |
| `AOR-002` | Dashboard Recording card target/status and future controls | Touched | Prior SLC-052 HUD Overlay card launcher/preview is superseded for active placement decisions. The repair remaps recording target/status and future recording-specific controls to a dedicated Dashboard Recording card while real Start/Stop remains future-gated until recording execution and file writing are admitted. | Workstream proof includes Dashboard Recording card target/status state, future-gated control state, active Overlay Profile target source, active monitor transparency, and no tray/export/provider coupling. | Revised H1 must stress compact/default Dashboard Recording card layout, dashboard regression, and preservation of Overlay card focus. | Revised LV must use real user-level mouse/keyboard input, before/after screenshots, compact/default photos, hover/focus proof, and pessimistic visual review if visible. | UTS must ask USER to verify the Dashboard Recording card placement, active monitor transparency, compact/default visual correctness, and absence of tray/export/provider scope. | Tray recording controls, real Start/Stop, file writing, and recording execution remain future-gated unless admitted later. | Accepted | This plan |
| `AOR-003` | Active monitored monitors transparency | Touched | SLC-052 shows recording-relevant active monitors in the Dashboard Recording card, while the HUD Overlay card keeps overlay clarity. | Workstream proof includes null/stale filtering from SLC-051 plus visible count/name transparency in the Dashboard Recording card. | H1 must compare Dashboard, HUD Overlay, Manage Monitors, Overlay Profile, and Overlay Display behavior for regressions. | LV1 must capture focused Dashboard Recording card screenshots at default and compact sizes if visible. | UTS required if visible in Dashboard Recording card. | Monitor Group configuration remains owned by Manage Monitors / Sensor Command Center. | Accepted | This plan |
| `AOR-004` | Recording Control or secondary recording detail surface | Deferred | Prior SLC-053 standalone Recording Control window foundation remains durable evidence only. The implementation keeps any standalone Recording Control window as a later secondary surface unless later source truth admits it. | Workstream proof matches the USER-accepted BP2 and approved BP3 route and proves no Dashboard child-window or standalone-window dependency is implied. | H1 must stress the accepted surface only and confirm standalone/native Recording Control remains future-secondary. | LV1 proof applies to the accepted visible Dashboard Recording card surface after H1. | UTS required for the visible Recording card. | Real Start/Stop, file writing, and advanced bulky settings remain future-gated or move behind secondary surfaces only after USER/source-truth admission. | Deferred With Waiver | This plan |
| `AOR-005` | Durable recording output contract | Touched | SLC-054 implements the output contract schema/readback proof needed for future graph/plot workflows without creating output files or recording execution. | Workstream proof includes schema/header/row determinism, timestamp/value/source identity, manifest shape, null/no-data behavior, parse/readback proof, and blocked file-writing/execution boundaries. | H1 must stress file path errors, long recordings, high-volume sensors, interrupted write, and compatibility with future graph/plot usage if file-writing/execution is later admitted. | LV1 requires user-facing proof only if output settings or recording execution are visible; otherwise helper proof can satisfy file-contract validation. | UTS required if a user can create/select/open output files; otherwise Workstream/H1 proof may be sufficient. | Export/share/import remains a future package and is not authorized by an output contract alone. | Accepted | This plan |
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

USER Branch Plan Review: Accepted BP2 context - USER accepted the BP1 Dashboard Recording card amendment and the revised BP2 engineering plan; USER also approved BP3 Workstream Entry / Orchestration Validation for the Dashboard Recording card route.
Review Status: Accepted by USER - BP2 Branch Plan revision is accepted by USER and retained as support context for the approved BP3 and implemented bounded Workstream repair.
Contract Status: Complete - BP2 Branch Plan revision is accepted, BP3 is approved, bounded Workstream repair is implemented, and renewed H1 is green; renewed LV remains pending.
Packet Reviewability State: Reviewable when the regenerated `C:\Nexus USER\FAM-006` packet validates.
USER Gate State: USER Accepted
USER Response Proof: USER accepted the BP1 Branch Vision amendment and then accepted the revised BP2 Branch Plan for the Dashboard Recording card route.
USER Response Digested: BP1 acceptance, BP2 acceptance, BP3 approval, bounded Workstream implementation approval, renewed H1 approval, and renewed LV1 approval digested into the active branch record and branch plan; the next USER response is returned UTS disposition.
Acceptance / Waiver / Revision / Rejection Receipt: BP1 amendment accepted by USER; BP2 revision accepted by USER; BP3 Workstream Entry / Orchestration Validation approved by USER; bounded Workstream implementation approved and executed; renewed H1 approved and green; renewed LV remains pending USER approval, revision, rejection, or hold.
Contract Version / Revision: v21 records the corrected LV1 evidence standard for branch-created Recording card elements, the active Overlay Profile to Recording target mirror repair, and the refreshed UTS disposition path.
USER Review Hub Packet: `C:\Nexus USER\FAM-006`
Local USER Hub Packet: `C:\Nexus USER\FAM-006`
Local USER Hub ZIP: `C:\Nexus USER\FAM-006__YYYYMMDD-HHMMSS.zip`
USER Review Packet Finding: BP3 packet proof accepted for planning; START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, the exported .zip, Source HEAD/current branch HEAD freshness, loaded/digested blocker status, Packet Reviewability State, and USER Gate State are proved by Codex digest/helper output while USER-facing files stay decision-focused. The next Workstream implementation approval must preserve those proof markers without putting live technical proof metadata into USER-facing packet content.
Current-Main / Review-Hub Blocker: `Current-main reconciliation is complete. The next packet-generation pass must use C:\Nexus USER\FAM-006 as the active readable local USER hub folder and exactly one timestamped C:\Nexus USER\FAM-006__YYYYMMDD-HHMMSS.zip upload artifact; cloud-backed Desktop/OneDrive paths are mirror/convenience surfaces only.`
Family Vision Context: `FAM-006 owns Monitoring HUD, Dashboard, Overlay Profile, Overlay Display, Monitor Group, Sensor Command Center, and active-overlay-driven recording planning; this contract must keep recording connected to the overlay system instead of creating a second profile system.`
Feature Vision: `The recording feature should derive its target from the active Overlay Profile, show recording target/status in a dedicated Dashboard Recording card, keep the HUD Overlay card overlay-focused, and keep graph/log viewing separate as future Native Log Loader work.`
Branch Goal: `Revise the active-overlay-driven recording runtime foundation so recording-specific review and future controls live in a dedicated Dashboard Recording card while preserving trustworthy target proof and future-gated execution boundaries.`
Plain-Language Branch Goal: Establish the corrected FAM-006 recording branch where recording is driven by the active Overlay Profile instead of a separate Recording Profile.
What Will I Actually See, And Where Will I See It?: USER should eventually see a dedicated Dashboard Recording card with active Overlay Profile target source, concise target/status summary, and future-gated recording controls when those are admitted. The HUD Overlay card should remain focused on overlay identity, Overlay Profile, Overlay Status, and overlay-specific actions. Native Log Loader is a separate future graph/log viewer, not the recording control surface.
How It Will Function: `The active Overlay Profile remains the source of recording target membership; the Dashboard Recording card previews that target/status, preserves Monitor Group and Overlay Profile ownership boundaries, keeps execution and file writing behind explicit approval, and uses future output contracts that can feed graph/plot workflows.`
User Experience Flow: `USER starts in the Dashboard, reads the dedicated Recording card for recording target/status, and keeps the HUD Overlay card focused on overlay state. Any secondary recording settings/detail surface remains future-gated until BP2/BP3 admits it.`
Planned User-Facing Outcome: SLC-051 target truth remains useful; revised future user-facing outcome is a Dashboard Recording card with transparent active target information and future-gated controls after BP3 approval and later implementation approval.
End-State Vision: The completed active-overlay recording foundation should make recording feel automatic and connected to the overlay the USER already loaded, while keeping the Dashboard layout clear: Overlay Profile defines what is visible/tracked, active overlay membership defines the recording target, and the Dashboard Recording card explains and controls recording without crowding the HUD Overlay card.
Visual / Behavioral Description: Future recording should start from a dedicated Dashboard Recording card as a truthful target/status preview, not from a separate Recording Profile chooser and not from the HUD Overlay card. Any compact secondary window or advanced settings surface requires revised planning and proof.
Visual / Functional Walkthrough: USER starts at the Dashboard Recording card, sees the active Overlay Profile target source and target/status preview, and later uses future-gated recording controls after execution is admitted. Advanced path/format/settings details move to secondary surfaces only if source truth later admits them. Future log files are designed so a separate Native Log Loader can graph data over time, but loader implementation remains future-gated.
Surface Map: Dashboard Recording card = recording target/status and future recording controls; HUD Overlay card = overlay identity/Profile/Status and overlay-specific actions; secondary settings/advanced windows = future bulky configuration surfaces if admitted; Overlay Profile = source of active recording target membership; Monitor Group = reusable sensor/source group; files/output = future graph/plot-ready recording data; Native Log Loader = future separate graph/log viewer; tray/export/provider/theme/FAM-007 = future-gated surfaces outside this approval.
Implementation Breakdown: SLC-051 target foundation remains accepted target/session truth. SLC-052 HUD Overlay launcher/target transparency and SLC-053 standalone Recording Control window foundation are superseded active-placement evidence; accepted BP2 and approved BP3 route the active repair to a dedicated Dashboard Recording card. SLC-054 durable output contract schema/readback proof remains future-useful without recording execution or file writing. SLC-055 validation/live proof readiness must be revised during the approved implementation/hardening path.
Element-to-Phase Proof Matrix: Present in this plan for AOR-001 through AOR-010.
Hardening Plan: Revised H1 must pressure-test active overlay membership, Dashboard Recording card behavior, HUD Overlay preservation, output contract boundaries, concept separation, compact/default UI, and future-gated boundaries.
Live Validation / UTS Plan: Revised LV1 must use real user-level input, visible cursor movement/clicks, compact/default screenshots, focused per-element screenshots for every new branch-created user-facing element, output-file proof where applicable, and UTS handoff or explicit waiver after the repaired route is implemented. For this branch, the mandatory new-element proof includes the Dashboard Recording card target/status visual contract, standard Dashboard state-row target preview, future-control disabled boundary, and visual-system inheritance from existing FAM-006 Dashboard cards.
Open USER Questions: USER must decide whether to return PASS, FAIL/repair feedback, or an explicit waiver for the refreshed UTS handoff at C:\Nexus USER\UTS - FAM-006.txt, while keeping standalone/secondary recording detail future-only, preserving proof expectations, and confirming the seam remains bounded.
USER Design Review Questions: BP1 and BP2 are accepted, BP3 is approved, bounded Workstream repair is implemented, renewed H1 is green, and renewed LV1 is green; the active review question is returned UTS disposition.
Codex Recommendations: Accept the active-overlay-driven recording product model with the USER's revised surface placement: recording targets derive from the active Overlay Profile, the Dashboard Recording card previews target/status and later owns recording-specific controls, the HUD Overlay card stays overlay-focused, Native Log Loader remains a separate future viewer, and per-overlay effective polling policy remains future FAM-006 architecture.
Implementation Options: Option A - return PASS on the refreshed UTS if USER agrees the Dashboard Recording card seam is acceptable; Option B - return FAIL/repair feedback with exact remaining issue IDs; Option C - explicitly waive UTS with reason; Option D - hold UTS and keep the branch before PR Readiness. Codex recommends Option A only if runtime execution, file writing, real Start/Stop, tray/export/provider/FAM-007/Governance/PR/merge/release/cleanup remain blocked.
Implementation Options / Product Shapes: `Option A - Dashboard Recording card primary; Option B - Dashboard Recording card plus future secondary detail window; Option C - hold for narrower UI branch; Option D - reject and preserve old route only as historical evidence.`
Recommended Direction: Codex recommends accepting the BP2 plan only if it keeps the Dashboard Recording card as the primary recording target/status surface, preserves the HUD Overlay card as overlay-focused, treats any standalone/secondary recording detail surface as future unless BP2 explicitly admits it, and keeps recording execution/file writing/real Start/Stop/tray/export/provider/FAM-007/Governance/PR/merge/release/cleanup pending.
Why This Fits The Nexus Vision: This direction keeps recording intuitive, avoids a confusing second profile system, keeps the HUD Overlay card lightweight, gives recording its own scan-friendly Dashboard home, keeps graph/log viewing separate from recording control, and protects future log quality by preserving snapshot-at-start and per-overlay effective polling constraints.
USER Design Direction Decision: BP1 amendment accepted after returned Live Validation feedback. Active Overlay Profile membership remains the recording target source; snapshot-at-start remains the default target model; Dashboard Recording card is the accepted primary recording surface; hidden target state and a separate Recording Profile system remain rejected unless USER later reopens them.
Current Branch Scope: Current branch scope is the active-overlay-driven recording foundation plus the implemented Dashboard Recording card repair from returned USER Live Validation feedback. Further runtime expansion is not admitted.
Future-Gated Scope: Future-gated scope includes recording execution, file writing until admitted, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup, PR, merge, release, issue mutation, and durable Native Log Loader source-truth mutation.
How Codex Would Build This After USER Accepts The Direction: `Implemented, H1 green, and LV1 green: recording target/status and future controls now live in a Dashboard Recording card. If USER returns PASS or waives UTS, Codex may digest the UTS disposition into source truth and then ask for the next legal PR Readiness decision if validation remains green.`
Implementation Staging Notes: SLC-051 target model proof remains the base. The old HUD launcher/preview and standalone window proof cannot be treated as active placement proof after UFD-FAM006-20260602-001; repair staging is complete for the bounded Dashboard Recording card seam, H1 is green, and the corrected LV1 pass now supersedes the earlier LV1 proof that missed the newly created Recording card elements.
Alternatives / Tradeoffs: The prior profile-loaded Recording Profile route is preserved only as historical rollback receipt because it did not match the clarified USER recording vision.
USER Decisions Needed: Return completed C:\Nexus USER\UTS - FAM-006.txt results as PASS, FAIL/repair feedback, or WAIVED for the implemented, hardened, and live-validated Dashboard Recording card repair seam. Runtime execution, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, release execution, issue mutation, Governance worktree mutation, and durable Native Log Loader implementation remain pending decisions.
USER Review Response: Needs USER Response - returned UTS disposition is pending USER PASS, FAIL/repair feedback, waiver, or hold.
Codex Response Digest: USER response was digested for BP1/BP2/BP3/Workstream/H1/LV1 admission; USER accepted the BP1 amendment, accepted the BP2 engineering plan, approved BP3 orchestration, approved bounded Workstream implementation, approved renewed H1, and approved renewed LV1. USER screenshot review then showed LV1 had passed despite a Recording card visual-system mismatch. Codex repaired the Dashboard Recording card to inherit the standardized Dashboard card visual grammar, ensured new Overlay Profile creation mirrors immediately into Recording target/session truth, hardened LV1 to require focused screenshots of new branch-created elements and visual-system inheritance markers, and keeps returned UTS disposition pending after renewed proof.
Implementation Constraints Created By USER Response: SLC-051 is complete as target/session truth only; active Overlay Profile membership remains the future recording target source; no separate Recording Profile system or recording-specific sensor chooser is admitted; recording execution, file writing, real Start/Stop behavior, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, and durable Native Log Loader mutation remain blocked; future recording execution should default to snapshot-at-recording-start for clean logs unless USER revises it; SLC-051 proves the live current target because it records nothing; target proof preserves null/empty/selected/switched/deleted-stale/duplicate-stale-ID/high-volume states and existing Overlay Profile, Overlay Display, Monitor Group, Dashboard, Manage Monitors, and Sensor Command Center behavior; per-overlay effective polling policy remains future-planning/source-truth constraint; `desktop/ui/dashboard_hud_panel.py` is not the current owner unless later repo truth creates it.
USER Rejected / Deferred Ideas: Rejected for this direction is the separate profile-loaded Recording Profile system and any duplicated CPU FAST/CPU SLOW Monitor Group workaround as the desired long-term polling model. Deferred are recording execution, file writing, real Start/Stop controls, tray controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 branch/workstream mutation, old branch cleanup/deletion, durable Native Log Loader implementation/source-truth mutation beyond future planning, per-overlay polling-policy implementation, and advanced/bulky Recording Control settings.
Vision Delta / Source-Truth Impact: Active branch plan, branch record, family vision, and local USER hub packet preserve the active-overlay recording branch identity while recording the Dashboard Recording card placement revision as the accepted BP1 design direction. Family vision records per-overlay effective polling policy as a future FAM-006 planning constraint because it affects recording target model design. Native Log Loader remains future planning input only and is not admitted for durable implementation.
Contract Change Log: v1 introduced USER-facing Branch Plan Review packet with end-state/options sections. v2 hardened it into USER Branch Plan Contract with closed-loop USER response/digest, implementation constraints, source-truth impact, confirmation loop, stale-packet protection, and waiver semantics. v3 digested USER recording product-model feedback. v4 recorded pre-PR #248 acceptance evidence on the released foundation planning carrier. Post-PR #248 reset marked those BP receipts superseded for active decisions and returned this implementation carrier to BP1 USER Branch Vision Review. v5 records active BP1 acceptance and prepares BP2 USER Branch Plan Review from the accepted vision. v6 records BP2 acceptance and prepares BP3 Workstream Entry / Orchestration Validation with file-ownership guardrails. v7 records BP3 approval and prepares the separate SLC-051 Workstream implementation approval decision. v8 records bounded SLC-051 target/session truth implementation. v14 records UFD-FAM006-20260602-001 and routes to BP1 amendment before repair. v17 records USER approval of the revised BP3 Dashboard Recording card route and prepares the separate bounded Workstream implementation approval decision. v18 records bounded Workstream implementation of the Dashboard Recording card repair seam and prepares renewed H1. v19 records renewed H1 green and prepares renewed Live Validation LV1. v20 records renewed LV1 green, helper robustness repair, and UTS handoff refresh. v21 records USER-reported LV proof insufficiency, mandatory new-element focused screenshot proof, Recording card contained-row visual repair, and active Overlay Profile draft-to-Recording target mirror repair. v22 records the USER-reported visual-system mismatch that remained after the contained-row repair, adds the FAM-006 family vision requirement that new UI sample existing visual grammar, and replaces the Recording card proof target with standardized Dashboard state-row inheritance. v23 records the USER-reported UTS handoff mismatch where the helper refreshed proof metadata but left the old Overlay Profiles issue-body; the helper and validator now require the UTS body to name the active Recording-card visual-system and target-mirror retest contract.
Workstream Entry Result: BP3 is USER Approved for the revised Dashboard Recording card repair route; bounded Workstream implementation is complete for the first repair seam; prior BP3 approval for the old HUD Overlay card route remains durable evidence for the superseded route only.
Contract Completion Checklist: BP1 amendment accepted; BP2 revision accepted; BP3 approved; bounded Workstream repair implemented; renewed H1 green; renewed LV1 green; returned UTS disposition pending.
Accepted Scope: Accepted scope for this pass includes source-truth feedback disposition, family vision/branch record/branch plan fold-down, and USER packet refresh if permitted. It excludes runtime code repair.
Deferred Scope: Deferred scope is SLC-055 beyond bounded same-branch continuation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge, release, issue mutation, artifacts/raw evidence handling beyond approved review packet, sibling-worktree mutation, old branch cleanup/deletion, and Governance mutation.
Rejected Scope: Requiring users to load a separate Recording Profile before recording sensors is rejected for this future recording path unless USER explicitly re-approves it.
Exact USER Decision Needed: Return completed C:\Nexus USER\UTS - FAM-006.txt results as PASS, FAIL/repair feedback, or WAIVED for the implemented, hardened, and live-validated Dashboard Recording card repair seam. PR Readiness remains blocked until UTS disposition is complete or waived.
Implementation Approval: Bounded Workstream implementation approval was used for the Dashboard Recording card repair seam only; later runtime mutation remains blocked.

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

## Hardening H1 Active Overlay Recording Runtime Implementation

H1 Admission: `PASS - USER approved renewed FAM-006 Hardening H1 for the implemented Dashboard Recording card repair seam.`
H1 Result: `Green - SLC-051 through SLC-055 evidence matches accepted BP1, accepted BP2, approved BP3, and bounded Workstream implementation for the revised Dashboard Recording card route.`
Accepted BP Trace: `PASS - BP1 Branch Vision, BP2 Branch Plan, BP3 Workstream Entry / Orchestration Validation, and bounded Workstream implementation are accepted or approved.`
SLC-051 Pressure-Test: `PASS - active Overlay Profile target/session truth markers are present and recording execution/file writing remain blocked.`
SLC-052 Pressure-Test: `PASS - Dashboard Recording card target/status markers are implemented and focused Workstream validators are green.`
SLC-053 Pressure-Test: `PASS - standalone/native Recording Control remains future-secondary; Start/Stop remains future-gated.`
SLC-054 Pressure-Test: `PASS - output contract schema/readback and blocked execution markers are present; deterministic in-memory output proof is green.`
SLC-055 Pressure-Test: `PASS - Workstream Green proof and H1/LV1/UTS routing markers are present; later phases are not claimed complete inside Workstream.`
Future-Gated Boundary Check: `PASS - recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, Native Log Loader implementation, and FAM-007 mutation remain blocked.`
UTS Phase Boundary: `PASS - Formal User Test Summary export is exclusive to Live Validation Stage 1; H1 did not refresh, digest, or export UTS.`
Helper Proof: `PASS - python dev\orin_fam006_hardening_h1.py.`
Next Active Seam: Live Validation LV1 - returned User Test Summary disposition

## Next Legal Phase

Next Legal Phase: `Live Validation - returned User Test Summary disposition`
Exact USER Decision Needed: `I completed the renewed FAM-006 User Test Summary at C:\Nexus USER\UTS - FAM-006.txt for the Dashboard Recording card repair seam and return PASS / FAIL / WAIVED results for Codex digestion. Runtime recording execution, file writing, real Start/Stop controls, tray/export/provider/FAM-007/Governance/PR/merge/release/cleanup remain pending separate USER decisions.`
