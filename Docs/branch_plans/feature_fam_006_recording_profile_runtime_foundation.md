# Branch Runtime Engineering Plan - FAM-006 Recording Profile Runtime Foundation

Branch: `feature/fam-006-recording-profile-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
Created From: `origin/main` at `26dded3f84c526e0525c7d3b18fcd2607e16590d`
Current Plan Phase: `Branch Readiness Stage 2 setup`
Runtime Implementation Approval: `Pending - runtime implementation is not admitted by this setup pass`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Recording Profile Runtime Foundation`
Owning Branch: `feature/fam-006-recording-profile-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
Current Phase: `Branch Readiness Stage 2`
Branch Runtime Engineering Plan: `Recording Profile Runtime Foundation branch setup and planning admission.`
Engineering Plan Status: `Accepted for Stage 2 setup`
Current Runtime Baseline: `FAM-006 Overlay Profile Runtime Foundation and Overlay Display Acceptance Foundation are released historical evidence. Recording Profile runtime is not implemented.`
Branch Purpose: `Admit a coherent Recording Profile runtime foundation package while preserving released FAM-006 evidence and repairing post-merge active-authority drift from the prior release-posture branch.`
Planned Runtime Delta: `None during Stage 2. Future Workstream may admit Recording Profile data/state, selection/edit shell, relationship boundaries, Dashboard/Manage Monitors integration, and validation/live proof.`
User-Facing Delta: `None during Stage 2 setup; future user-visible UI/status/copy deltas are limited to Recording Profile selector/editing or compact Dashboard/Manage Monitors status surfaces after Workstream Entry approval.`
Source-Truth Delta: `Move merged/deleted FAM-006 release-posture carry-forward record from active to historical/no-active posture; add this active branch authority and branch plan; update compact backlog/roadmap pointers for the active Recording Profile planning branch; record cleanup/no-unique-commit proof.`
State / Config / Schema Delta: `None during Stage 2. Future SLC-046 may define Recording Profile state/schema.`
Validator / Helper Delta: `None expected during Stage 2; existing validation must pass after source-truth setup.`
Expected Changed Files / Surfaces: `Docs/branch_records/index.md; Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_records/feature_fam_006_v1_7_19_release_posture_carry_forward.md; Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md; Docs/branch_plans/retirement_index.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `SLC-046 Recording Profile data/state foundation; SLC-047 profile selection/editing entry points; SLC-048 Recording Profile relationship mapping and boundaries; SLC-049 Dashboard / Manage Monitors Recording Profile status integration; SLC-050 validation/live proof readiness.`
Per-Seam Implementation Checklist: `SLC-046 must name state/schema files before runtime edits; SLC-047 must name visible selector/editing files before UI edits; SLC-048 must name relationship/boundary files; SLC-049 must name Dashboard/Manage Monitors surfaces; SLC-050 must name validator/helper/proof files.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks where changed, H1 checks, LV1 real-input proof where user-facing, and regression proof for Overlay Profile, Monitor Group, Dashboard, Sensor Command Center, and Recording Profile separation.`
Per-Seam User-Facing Proof Checklist: `Pending Workstream Entry; any user-facing seam must carry real-input desktop validation and focused per-element screenshot requirements.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, and artifacts/raw evidence handling.`
Approval-Boundary Audit: `Approval boundary: USER approved Branch Readiness Stage 2 setup only; runtime implementation, Workstream execution, PR, merge, release, issue, artifact, sibling-worktree, tray/export/provider/theme work are blocked pending separate USER approval.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. FAM-007 and Governance worktrees are sibling context and not mutable. Future runtime seams may touch HUD/Dashboard/Manage Monitors surfaces and must forecast overlap before implementation.`
Open Questions: `Workstream Entry must select the first implementation seam and confirm exact runtime surfaces.`
USER Planning Decisions: `USER approved Stage 1 analysis and Stage 2 setup for this Recording Profile branch.`
Plan Revision History: `v1 - Created after PR #212 merge and FAM-006 branch cleanup from current origin/main 26dded3f84c526e0525c7d3b18fcd2607e16590d.`
Plan-To-Implementation Traceability: `Stage 2 records branch setup only. Workstream Entry and later implementation seams must fill implementation evidence, changed files, validation proof, user-facing proof, H1 findings, LV1 artifacts, and UTS disposition for each admitted slice.`
Plan-To-Implementation Traceability Table: `Pending Workstream Entry; each future row must map SLC ID, planned delta, files touched, validator/helper proof, H1 result, LV1/UTS proof, deferred boundaries, and commit evidence.`
Hardening Comparison Checklist: `Pending Workstream implementation. H1 must compare actual behavior against the Element-to-Phase Proof Matrix and concept separation.`
Live Validation Proof Or Waiver Checklist: `Pending Workstream implementation. LV1 must use real user-facing launcher where feasible, real user-level input, compact/default window proof, per-element screenshots, and UTS handoff when user-facing behavior changes.`
PR Readiness Fold-Down / Retention Checklist: `Future PR Readiness must decide what branch-plan details fold into branch record, family vision/dossier, workstream record, or retirement index.`
Release Readiness Public-Scope Translation Checklist: `Future Release Readiness must describe only implemented and validated user-facing Recording Profile work; future-gated tray/export/provider/theme work must remain excluded.`
USER Planning Review: `Accepted for Branch Readiness Stage 2 setup only.`
Runtime Implementation Approval: `Pending USER approval - runtime implementation is blocked until Workstream Entry returns an exact bounded implementation approval packet and USER approves it.`
PR Fold-Down Packet: `Pending future PR Readiness.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Recording Profile Runtime Foundation`
Package Posture: `Active planning branch / runtime implementation pending`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-046` Recording Profile data/state foundation | Admitted | Define durable Recording Profile state/schema, defaults, normalization, migration, and persistence boundaries. | Pending Workstream Entry |
| `SLC-047` Recording Profile selection/editing entry points | Admitted | Add or plan visible selector/edit shell only after state foundation is safe. | Pending Workstream Entry |
| `SLC-048` Recording Profile relationship mapping and boundaries | Admitted | Keep Recording Profile distinct from Overlay Profile, Monitor Group, and source selection while preparing future recording membership. | Pending Workstream Entry |
| `SLC-049` Dashboard / Manage Monitors Recording Profile status integration | Admitted | Add compact status/integration points only where source truth supports them. | Pending Workstream Entry |
| `SLC-050` validation/live proof readiness | Admitted | Add validators/helpers/proof plan for null/stress states, real-input UI proof, H1, LV1, and UTS handoff. | Pending Workstream Entry |

Single-Slice Package User Approval: `Not required - multiple concrete slices are admitted.`
Package Completion State: `Not started`

## Element-to-Phase Proof Matrix

Matrix Status: `Present`
USER Review Status: `Pending Workstream Entry review`
Open Element Questions: `Queued`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md`
Element Validation Ledger Owner: `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RPF-001` | Recording Profile data/state model | Planned | SLC-046 will implement only after Workstream Entry names exact state/schema files, default profile rules, normalization/migration behavior, and persistence boundary. | Workstream proof must include state-shape validation, save/load proof, null profile proof, high-volume profile proof, and concept-separation assertions. | H1 must pressure-test missing/stale/duplicate references, migration from legacy FAM-006 state, and preservation of Overlay Profile/Monitor Group behavior. | LV1 waiver path allowed only if SLC-046 is state-only with no visible UI; if any visible status appears, capture focused screenshots and real-input proof. | UTS path is waived for pure state-only proof, but required if user-visible status/control changes land. | Actual recording execution, tray controls, export/share, and provider/model work remain outside SLC-046. | Needs USER Decision | This plan |
| `RPF-002` | Recording Profile selection/editing shell | Planned | SLC-047 will implement only after SLC-046 state proof and must name exact HTML/CSS/JS/Python surfaces for selector/editing UI. | Workstream proof must include selector/edit/create/rename/save/discard behavior, dirty guard if applicable, compact/default geometry, and no recording execution. | H1 must stress null profiles, many profiles, long names, dirty changes, close/cancel/save/discard, and regression against Overlay Profile controls. | LV1 must use real user-level clicks, hover/focus screenshots, compact/default screenshots, and focused per-element artifacts if visible controls are implemented. | UTS required for visible Recording Profile controls with issue-form tracking for any returned defects. | Tray recording controls and export/share buttons are excluded from SLC-047. | Needs USER Decision | This plan |
| `RPF-003` | Recording Profile / Overlay Profile separation | Planned | SLC-048 will implement only boundary/mapping proof approved by Workstream Entry; it must not mutate Overlay Profile membership semantics by inertia. | Workstream proof must assert Recording Profile state is separate from overlayProfiles and activeOverlayProfileId and does not alter overlay display acceptance. | H1 must compare Recording Profile, Overlay Profile, Monitor Group, and future Recording Profile concepts for leaked state or shared mutation. | LV1 must visually prove separation only if any UI labels/status rows are added; otherwise record state-only waiver and validator evidence. | UTS required if the user can see or edit relationship state; otherwise no visible UTS item. | Overlay Profile display membership remains owned by historical/released Overlay Profile and Overlay Display surfaces. | Needs USER Decision | This plan |
| `RPF-004` | Recording Profile / Monitor Group separation | Planned | SLC-048/SLC-049 may read Monitor Group names/counts only if approved; it must not make Monitor Groups recording controls by default. | Workstream proof must assert Monitor Group organization and Sensor Command Center behavior stay green after Recording Profile state is introduced. | H1 must stress existing monitor groups, source assignments, sensor settings, and dirty guards to ensure no Recording Profile bleed-through. | LV1 must capture Manage Monitors/Dashboard focused proof if these surfaces change; otherwise record no-visible-change waiver. | UTS required if Manage Monitors or Dashboard visible behavior changes. | Monitor Groups remain organization/source configuration, not Recording Profile execution. | Needs USER Decision | This plan |
| `RPF-005` | Dashboard / Manage Monitors status integration | Planned | SLC-049 will add only compact status/integration points approved by Workstream Entry and must preserve existing Dashboard layout standards. | Workstream proof must include HUD surface validation, compact/default layout proof, button/dropdown parity, and preservation of existing Dashboard cards. | H1 must stress responsive sizing, high-volume data, nested windows, dirty guards, and no page/window clipping. | LV1 must use real launcher, real user-level input, per-element screenshots, normal/compact comparison, and USER-inspectable OneDrive artifacts. | UTS required because this is user-facing if implemented. | Export/share, tray recording controls, provider/model work, and broad theme/skin work remain future branches. | Needs USER Decision | This plan |
| `RPF-006` | Validation/live proof readiness | Planned | SLC-050 will implement validators/helpers/proof manifests only after prior seams define changed runtime surfaces and proof needs. | Workstream proof must include branch governance, HUD validators, internal sandbox, validation suite, JS syntax/load proof when JS changes, and proof manifest coverage. | H1 must run full package comparison against the plan, matrix, source truth, validators, UI proof, and future-gated boundaries. | LV1 must use real user-facing launcher where feasible, real mouse/keyboard input, focused screenshots/videos, compact/default stress, null/high-volume selectors, and pessimistic Codex photo review. | UTS handoff only after LV1 is green or explicitly waived with reason. | PR creation, merge, release, artifacts/raw evidence handling, and issue mutation remain later phases. | Needs USER Decision | This plan |
| `RPF-007` | Tray recording controls | Future | No Workstream implementation in SLC-046 through SLC-050; any tray control requires separate USER-approved future branch or scope revision. | Workstream proof for current branch is a boundary scan showing no tray control was added or implied. | H1 must confirm no tray recording execution or tray button appeared from Recording Profile foundation work. | LV1 must confirm absence only if user-facing Recording Profile UI could imply tray controls; otherwise record boundary proof in H1. | Future USER acceptance belongs to a later tray recording branch, not this branch. | Boundary: outside current SLC-046 through SLC-050 release gating and blocked by pending USER decision for tray recording controls. | Deferred With Waiver | This plan |
| `RPF-008` | Export/share recording output | Future | No Workstream implementation in SLC-046 through SLC-050; export/share requires separate USER-approved future branch or scope revision. | Workstream proof for current branch is a boundary scan showing no export/share output path was added or implied. | H1 must confirm no export/share buttons, files, or workflows were added by Recording Profile foundation work. | LV1 must confirm absence only if user-facing Recording Profile UI could imply export/share; otherwise record boundary proof in H1. | Future USER acceptance belongs to a later export/share branch, not this branch. | Boundary: outside current SLC-046 through SLC-050 release gating and blocked by pending USER decision for export/share behavior. | Deferred With Waiver | This plan |
| `RPF-009` | Provider/model/memory integration | Future | No Workstream implementation in SLC-046 through SLC-050; provider/model/memory work remains FAM-007 or future USER-approved scope. | Workstream proof for current branch is a boundary scan showing no provider/model/memory dependency was introduced. | H1 must confirm Recording Profile state works without provider/model execution and does not alter FAM-007 consent/provider boundaries. | LV1 must confirm absence only if user-facing UI could imply provider/model integration; otherwise record boundary proof in H1. | Future USER acceptance belongs to FAM-007 or another USER-approved branch, not this branch. | Boundary: outside current SLC-046 through SLC-050 release gating and blocked by pending USER decision for provider/model/memory work. | Deferred With Waiver | This plan |

## Branch Change Intent Ledger

### Changed Surface: Docs/branch_records/index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Move the merged/deleted FAM-006 release-posture carry-forward record from active to historical and add this active Recording Profile Runtime Foundation branch pointer.`
- Why This File Was Touched: `Branch Readiness Stage 2 is the legal carrier for post-merge fold-down and next runtime branch admission.`
- Owned Behavior / Fact Class: `Branch authority routing.`
- Canonical Owner / Source Owner: `Docs/branch_records/index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low from current origin/main; rerun Pre-Rebaseline Impact Audit if origin/main advances before PR.`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve the standing governance intake active pointer, move the merged FAM-006 carry-forward pointer to historical, and preserve this Recording Profile active pointer.`
- Rebaseline Handling: `Preserve incoming current-main governance/source-truth context and this branch-local FAM-006 authority.`
- Validation Proof: `Branch governance validation and release-readiness health gate.`
- Fallback Evidence: `Stage 1 packet, branch cleanup proof, and this branch authority record.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup and fold-down.`
- Fold-Down Target: `At PR Readiness/merge, this branch must project its own post-merge historical/no-active state.`

## Workstream Entry Whole-Package Analysis Requirements

Workstream Entry must inspect all SLC-046 through SLC-050 before selecting the first seam. First-seam-only analysis is not enough.

Required Workstream Entry outputs:

- all admitted slices/seams
- package completion strategy
- dependency map
- first bounded seam recommendation
- affected runtime/source-truth/validator/helper surfaces
- Hardening H1 expectations
- Live Validation LV1 expectations
- Codex Visual Adjudication expectations for any visible UI
- stress/null/high-volume proof requirements
- UTS handoff criteria
- exact implementation approval text

## Next Legal Phase

Next Legal Phase: `Workstream Entry`
Exact USER Decision Needed: `Approve Workstream Entry analysis for FAM-006 Recording Profile Runtime Foundation in C:\Nexus Worktrees\FAM-006 on feature/fam-006-recording-profile-runtime-foundation.`
