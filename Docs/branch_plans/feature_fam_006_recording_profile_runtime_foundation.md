# Branch Runtime Engineering Plan - FAM-006 Recording Profile Runtime Foundation

Branch: `feature/fam-006-recording-profile-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
Created From: `origin/main` at `26dded3f84c526e0525c7d3b18fcd2607e16590d`
Current Plan Phase: `SLC-047 Hardening H1 green`
Runtime Implementation Approval: `Granted for bounded SLC-046 Recording Profile data/state foundation and bounded SLC-047 Recording Profile selection/editing entry point implementation only`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Recording Profile Runtime Foundation`
Owning Branch: `feature/fam-006-recording-profile-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
Current Phase: `Hardening H1 complete - SLC-047`
Branch Runtime Engineering Plan: `Recording Profile Runtime Foundation branch setup and planning admission.`
Engineering Plan Status: `Accepted`
Current Runtime Baseline: `FAM-006 Overlay Profile Runtime Foundation and Overlay Display Acceptance Foundation are released historical evidence. SLC-046 adds Recording Profile data/state foundation only.`
Branch Purpose: `Admit a coherent Recording Profile runtime foundation package while preserving released FAM-006 evidence and repairing post-merge active-authority drift from the prior release-posture branch.`
Planned Runtime Delta: `SLC-047 implements the first visible Recording Profile selection/editing entry point on top of the SLC-046 state foundation. Relationship UI, Dashboard/Manage Monitors status beyond the compact entry point, and live proof remain later seams.`
User-Facing Delta: `SLC-047 adds a compact Dashboard/HUD Recording Profile selector/status entry point and a Recording Profile Settings child window for selecting, creating, renaming, and guarded deleting profiles without recording execution.`
Source-Truth Delta: `Move merged/deleted FAM-006 release-posture carry-forward record from active to historical/no-active posture; add this active branch authority and branch plan; update compact backlog/roadmap pointers for the active Recording Profile planning branch; record cleanup/no-unique-commit proof.`
State / Config / Schema Delta: `SLC-046 adds recordingProfiles, activeRecordingProfileId, Recording Profile schema/default constants, default active Recording Profile creation, membership/source normalization, and state proof fields.`
Validator / Helper Delta: `SLC-047 updates FAM-006 HUD surface/internal sandbox validators and renderer bridge proof for Recording Profile selector/create/rename/delete/save/discard controls, read-only membership posture, JS syntax/load proof, and concept-separation proof.`
Expected Changed Files / Surfaces: `Docs/branch_records/index.md; Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_records/feature_fam_006_v1_7_19_release_posture_carry_forward.md; Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md; Docs/branch_plans/retirement_index.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `SLC-046 Recording Profile data/state foundation; SLC-047 profile selection/editing entry points; SLC-048 Recording Profile relationship mapping and boundaries; SLC-049 Dashboard / Manage Monitors Recording Profile status integration; SLC-050 validation/live proof readiness.`
Per-Seam Implementation Checklist: `SLC-046 must name state/schema files before runtime edits; SLC-047 must name visible selector/editing files before UI edits; SLC-048 must name relationship/boundary files; SLC-049 must name Dashboard/Manage Monitors surfaces; SLC-050 must name validator/helper/proof files.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks where changed, H1 checks, LV1 real-input proof where user-facing, and regression proof for Overlay Profile, Monitor Group, Dashboard, Sensor Command Center, and Recording Profile separation.`
Per-Seam User-Facing Proof Checklist: `Pending Workstream Entry; any user-facing seam must carry real-input desktop validation and focused per-element screenshot requirements.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, and artifacts/raw evidence handling.`
Approval-Boundary Audit: `Approval boundary: USER approved bounded SLC-046 Recording Profile data/state foundation, SLC-046 H1, governed Workstream continuation decision, bounded SLC-047 Recording Profile selection/editing implementation, and bounded SLC-047 H1 only; SLC-048 through SLC-050, PR, merge, release, issue, artifact, sibling-worktree, tray/export/provider/theme work remain pending separate USER approval.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. FAM-007 and Governance worktrees are sibling context and not mutable. Future runtime seams may touch HUD/Dashboard/Manage Monitors surfaces and must forecast overlap before implementation.`
Open Questions: `Workstream Entry must select the first implementation seam and confirm exact runtime surfaces.`
USER Planning Decisions: `USER approved Stage 1 analysis, Stage 2 setup, Workstream Entry analysis, bounded SLC-046 implementation/H1, governed SLC-047 continuation, bounded SLC-047 implementation, and bounded SLC-047 H1 for this Recording Profile branch.`
Plan Revision History: `v1 - Created after PR #212 merge and FAM-006 branch cleanup from current origin/main 26dded3f84c526e0525c7d3b18fcd2607e16590d.`
Plan-To-Implementation Traceability: `SLC-046 and SLC-047 implementation evidence is recorded below; later implementation seams must fill implementation evidence, changed files, validation proof, user-facing proof, H1 findings, LV1 artifacts, and UTS disposition for each admitted slice.`
Plan-To-Implementation Traceability Table: `SLC-046 and SLC-047 rows are recorded in the Element-to-Phase Proof Matrix and implementation traces; SLC-048 through SLC-050 remain pending.`
Hardening Comparison Checklist: `SLC-046 and SLC-047 H1 hardening are green. Future H1 passes must compare actual implementation behavior, validator output, proof copy, and runtime plan expectations against the Element-to-Phase Proof Matrix and concept separation.`
Live Validation Proof Or Waiver Checklist: `Pending Workstream implementation. LV1 must use real user-facing launcher where feasible, real user-level input, compact/default window proof, per-element screenshots, and UTS handoff when user-facing behavior changes.`
PR Readiness Fold-Down / Retention Checklist: `Future PR Readiness must decide what branch-plan details fold into branch record, family vision/dossier, workstream record, or retirement index.`
Release Readiness Public-Scope Translation Checklist: `Future Release Readiness must describe only implemented and validated user-facing Recording Profile work; future-gated tray/export/provider/theme work must remain excluded.`
USER Planning Review: `Accepted for Branch Readiness Stage 2 setup only.`
Runtime Implementation Approval: `Granted for SLC-046 Recording Profile data/state foundation and bounded SLC-047 Recording Profile selection/editing entry points only.`
PR Fold-Down Packet: `Pending future PR Readiness.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Recording Profile Runtime Foundation`
Package Posture: `Active Workstream branch / SLC-046 implementation and H1 green; SLC-047 implementation and H1 green; SLC-048 through SLC-050 pending`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-046` Recording Profile data/state foundation | Admitted | Define durable Recording Profile state/schema, defaults, normalization, migration, and persistence boundaries. | Workstream implementation and H1 green |
| `SLC-047` Recording Profile selection/editing entry points | Admitted | Add or plan visible selector/edit shell only after state foundation is safe. | Workstream implementation and H1 green |
| `SLC-048` Recording Profile relationship mapping and boundaries | Admitted | Keep Recording Profile distinct from Overlay Profile, Monitor Group, and source selection while preparing future recording membership. | Pending Workstream Entry |
| `SLC-049` Dashboard / Manage Monitors Recording Profile status integration | Admitted | Add compact status/integration points only where source truth supports them. | Pending Workstream Entry |
| `SLC-050` validation/live proof readiness | Admitted | Add validators/helpers/proof plan for null/stress states, real-input UI proof, H1, LV1, and UTS handoff. | Pending Workstream Entry |

Single-Slice Package User Approval: `Not required - multiple concrete slices are admitted.`
Package Completion State: `In progress - SLC-046 implemented and H1 green; SLC-047 implemented and H1 green; SLC-048 through SLC-050 pending`

## Element-to-Phase Proof Matrix

Matrix Status: `Present`
USER Review Status: `Pending Workstream Entry review`
Open Element Questions: `Queued`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md`
Element Validation Ledger Owner: `Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RPF-001` | Recording Profile data/state model | Touched | SLC-046 adds recordingProfiles, activeRecordingProfileId, schema/default constants, default active profile creation, normalization/migration, persistence support, and renderer bridge proof without visible UI. | Workstream proof includes state-shape validation, save/load proof, null/default profile proof, high-volume profile proof, and concept-separation assertions. | H1 must pressure-test missing/stale/duplicate references, migration from legacy FAM-006 state, and preservation of Overlay Profile/Monitor Group behavior. | LV1 waiver path remains valid because SLC-046 is state-only with no visible UI. | UTS path is waived for pure state-only proof unless later seams introduce visible status/control changes. | Actual recording execution, tray controls, export/share, and provider/model work remain outside SLC-046. | Accepted | This plan |
| `RPF-002` | Recording Profile selection/editing shell | Touched | SLC-047 implements a compact Dashboard/HUD selector/status entry point and a Recording Profile Settings child window for select/create/name-edit/delete/save/discard behavior. | Workstream proof includes selector/create/rename/delete/save/discard markers, read-only membership, renderer bridge signal, HUD validators, runtime-fam006 validation, and JS syntax/load proof. | H1 stresses null profiles, many profiles, long names, dirty changes, close/cancel/save/discard/delete, compact/default geometry, default-profile delete blocking, and regression against Overlay Profile controls. | LV1 must use real user-level clicks, hover/focus screenshots, compact/default screenshots, and focused per-element artifacts if visible controls proceed beyond H1. | UTS required for visible Recording Profile controls with issue-form tracking for any returned defects after LV1. | Tray recording controls and export/share buttons are excluded from SLC-047. | Accepted | This plan |
| `RPF-003` | Recording Profile / Overlay Profile separation | Planned | SLC-048 will implement only boundary/mapping proof approved by Workstream Entry; it must not mutate Overlay Profile membership semantics by inertia. | Workstream proof must assert Recording Profile state is separate from overlayProfiles and activeOverlayProfileId and does not alter overlay display acceptance. | H1 must compare Recording Profile, Overlay Profile, Monitor Group, and future Recording Profile concepts for leaked state or shared mutation. | LV1 must visually prove separation only if any UI labels/status rows are added; otherwise record state-only waiver and validator evidence. | UTS required if the user can see or edit relationship state; otherwise no visible UTS item. | Overlay Profile display membership remains owned by historical/released Overlay Profile and Overlay Display surfaces. | Needs USER Decision | This plan |
| `RPF-004` | Recording Profile / Monitor Group separation | Planned | SLC-048/SLC-049 may read Monitor Group names/counts only if approved; it must not make Monitor Groups recording controls by default. | Workstream proof must assert Monitor Group organization and Sensor Command Center behavior stay green after Recording Profile state is introduced. | H1 must stress existing monitor groups, source assignments, sensor settings, and dirty guards to ensure no Recording Profile bleed-through. | LV1 must capture Manage Monitors/Dashboard focused proof if these surfaces change; otherwise record no-visible-change waiver. | UTS required if Manage Monitors or Dashboard visible behavior changes. | Monitor Groups remain organization/source configuration, not Recording Profile execution. | Needs USER Decision | This plan |
| `RPF-005` | Dashboard / Manage Monitors status integration | Planned | SLC-049 will add only compact status/integration points approved by Workstream Entry and must preserve existing Dashboard layout standards. | Workstream proof must include HUD surface validation, compact/default layout proof, button/dropdown parity, and preservation of existing Dashboard cards. | H1 must stress responsive sizing, high-volume data, nested windows, dirty guards, and no page/window clipping. | LV1 must use real launcher, real user-level input, per-element screenshots, normal/compact comparison, and USER-inspectable OneDrive artifacts. | UTS required because this is user-facing if implemented. | Export/share, tray recording controls, provider/model work, and broad theme/skin work remain future branches. | Needs USER Decision | This plan |
| `RPF-006` | Validation/live proof readiness | Planned | SLC-050 will implement validators/helpers/proof manifests only after prior seams define changed runtime surfaces and proof needs. | Workstream proof must include branch governance, HUD validators, internal sandbox, validation suite, JS syntax/load proof when JS changes, and proof manifest coverage. | H1 must run full package comparison against the plan, matrix, source truth, validators, UI proof, and future-gated boundaries. | LV1 must use real user-facing launcher where feasible, real mouse/keyboard input, focused screenshots/videos, compact/default stress, null/high-volume selectors, and pessimistic Codex photo review. | UTS handoff only after LV1 is green or explicitly waived with reason. | PR creation, merge, release, artifacts/raw evidence handling, and issue mutation remain later phases. | Needs USER Decision | This plan |
| `RPF-007` | Tray recording controls | Future | No Workstream implementation in SLC-046 through SLC-050; any tray control requires separate USER-approved future branch or scope revision. | Workstream proof for current branch is a boundary scan showing no tray control was added or implied. | H1 must confirm no tray recording execution or tray button appeared from Recording Profile foundation work. | LV1 must confirm absence only if user-facing Recording Profile UI could imply tray controls; otherwise record boundary proof in H1. | Future USER acceptance belongs to a later tray recording branch, not this branch. | Boundary: outside current SLC-046 through SLC-050 release gating and blocked by pending USER decision for tray recording controls. | Deferred With Waiver | This plan |
| `RPF-008` | Export/share recording output | Future | No Workstream implementation in SLC-046 through SLC-050; export/share requires separate USER-approved future branch or scope revision. | Workstream proof for current branch is a boundary scan showing no export/share output path was added or implied. | H1 must confirm no export/share buttons, files, or workflows were added by Recording Profile foundation work. | LV1 must confirm absence only if user-facing Recording Profile UI could imply export/share; otherwise record boundary proof in H1. | Future USER acceptance belongs to a later export/share branch, not this branch. | Boundary: outside current SLC-046 through SLC-050 release gating and blocked by pending USER decision for export/share behavior. | Deferred With Waiver | This plan |
| `RPF-009` | Provider/model/memory integration | Future | No Workstream implementation in SLC-046 through SLC-050; provider/model/memory work remains FAM-007 or future USER-approved scope. | Workstream proof for current branch is a boundary scan showing no provider/model/memory dependency was introduced. | H1 must confirm Recording Profile state works without provider/model execution and does not alter FAM-007 consent/provider boundaries. | LV1 must confirm absence only if user-facing UI could imply provider/model integration; otherwise record boundary proof in H1. | Future USER acceptance belongs to FAM-007 or another USER-approved branch, not this branch. | Boundary: outside current SLC-046 through SLC-050 release gating and blocked by pending USER decision for provider/model/memory work. | Deferred With Waiver | This plan |

## SLC-046 Workstream Implementation Trace

SLC-046 Status: `Implemented - H1 green`
Implementation Scope: `Recording Profile data/state foundation only.`
State / Schema Result: `Added recordingProfiles collection, activeRecordingProfileId pointer, Recording Profile schema/default constants, default active Recording Profile creation, membership/source normalization, and state proof fields.`
Default Active Profile Result: `Legacy monitor/card state receives a default active Recording Profile with empty monitor/source membership so existing monitors are not auto-recorded.`
Persistence Result: `Existing HUD state persistence now carries Recording Profile state alongside Overlay Profile state where the current HUD state architecture supports profile persistence.`
Renderer Bridge Result: `Renderer state sync emits MONITORING_HUD_RECORDING_PROFILE_STATE_READY when Recording Profile state is present.`
Concept Boundary Result: `Recording Profile state remains separate from overlayProfiles, activeOverlayProfileId, Monitor Group organization, tray recording controls, export/share, provider/model work, and theme/skin scope.`
User-Facing Delta: `None - SLC-046 adds no visible Recording Profile selector/editor/status surface.`

## SLC-046 Hardening H1 Trace

H1 Status: `Green`
H1 Scope: `Recording Profile data/state foundation pressure test only.`
H1 Result: `No bounded repair required.`
H1 Pressure-Test Coverage: `Missing/invalid Recording Profile state, legacy monitor/card migration, default active profile creation, duplicate/stale monitor references, duplicate source references, high-volume membership normalization, save/load persistence, active profile persistence, Overlay Profile separation, Monitor Group separation, tray recording boundary, export/share boundary, provider/model boundary, and no visible UI delta.`
H1 Evidence Basis: `Focused SLC-046 H1 recording profile pressure test, FAM-006 HUD surface validator, FAM-006 internal sandbox validator, branch governance validation, release-readiness health gate, validation-suite recommendation, JS syntax proof, and compileall.`
Next Legal Phase After H1: `Governed Workstream continuation decision for SLC-047 or a repo-truth-selected phase-boundary route.`

## SLC-047 Workstream Implementation Trace

SLC-047 Status: `Implemented - H1 green`
Implementation Scope: `Visible Recording Profile selection/editing entry points only.`
Selector Result: `Added compact Dashboard/HUD active Recording Profile selector/status and a Recording Profile Settings child-window selector.`
Create / Rename Result: `Added minimal create profile shell and name-edit shell backed by existing Recording Profile state without recording execution.`
Save / Discard Result: `Added Save/Discard behavior and modal dirty-guard handling for Recording Profile name edits.`
Delete Result: `H1 repair added guarded Recording Profile delete behavior for non-default saved profiles and pending create drafts; default Recording Profile deletion remains blocked.`
Read-Only Detail Result: `Added read-only Recording Profile details and read-only membership list; recording membership mapping remains later-seam work.`
Renderer Bridge Result: `Renderer bridge now reports MONITORING_HUD_RECORDING_PROFILE_STATE_READY with SLC-047 visible editor and read-only membership posture.`
Concept Boundary Result: `Recording Profile remains separate from Overlay Profile, Monitor Group organization, tray recording controls, recording execution, export/share, provider/model work, and broad theme/skin scope.`
User-Facing Delta: `Recording Profile selector and settings child window are now visible; tray recording and recording execution are not visible or functional.`
Validation Basis: `FAM-006 HUD validators, internal sandbox validator, runtime-fam006 validation suite, branch governance validation, release-readiness health gate, bundled Node syntax proof for monitoring_hud.js, and compileall.`
Next Legal Phase After Implementation: `Bounded SLC-047 Hardening H1.`

## SLC-047 Hardening H1 Trace

H1 Status: `Green`
H1 Scope: `Recording Profile visible selection/editing entry point pressure test only.`
H1 Defects Found: `Missing bounded Recording Profile delete control/proof while the approved H1 pressure-test scope included delete behavior.`
H1 Repairs Applied: `Added a guarded Recording Profile delete control and confirmation path, kept default Recording Profile deletion blocked, allowed pending create draft deletion without persisted mutation, allowed saved non-default profile deletion through existing state persistence, and updated renderer proof markers plus FAM-006 HUD validators to include delete coverage.`
H1 Pressure-Test Coverage: `Selector/create/name-edit/delete/save/discard behavior, modal dirty-guard posture, default/null/high-volume profile states, read-only membership posture, renderer bridge proof, JS syntax/load proof for monitoring_hud.js, Overlay Profile separation, Monitor Group/Sensor Command Center preservation, and tray recording/export/share/provider/theme boundaries.`
Next Legal Phase After H1: `Governed Workstream continuation decision for SLC-048 or a repo-truth-selected phase-boundary route.`

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

### Changed Surface: Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md

- Surface Class: `governance/source-truth`
- Change Intent: `Record that the merged/deleted FAM-006 release-posture carry-forward branch plan is historical and no longer an active FAM-006 runtime carrier.`
- Why This File Was Touched: `Branch Readiness Stage 2 is the legal carrier for post-merge fold-down of the prior FAM-006 release-support branch before admitting the Recording Profile Runtime Foundation branch.`
- Owned Behavior / Fact Class: `Historical branch-plan posture for the released/deleted FAM-006 carry-forward branch.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low from current origin/main; rerun Pre-Rebaseline Impact Audit if origin/main advances before PR.`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve incoming PR #212 current-main fold-down/history wording and preserve this branch setup truth that the prior release-posture branch is historical, merged, deleted, and not an active runtime carrier.`
- Rebaseline Handling: `Preserve incoming current-main fold-down context and this branch-local Recording Profile setup/fold-down evidence.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, and release-readiness health gate.`
- Fallback Evidence: `Stage 1 packet, branch cleanup proof, and this Recording Profile branch plan.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup and fold-down.`
- Fold-Down Target: `Retain as historical branch-plan evidence only; do not restore as an active branch plan.`

### Changed Surface: Docs/branch_plans/retirement_index.md

- Surface Class: `governance/source-truth`
- Change Intent: `Record the merged/deleted FAM-006 release-posture carry-forward branch as retired while preserving the active Recording Profile branch path.`
- Why This File Was Touched: `Branch Readiness Stage 2 recorded cleanup/no-unique-commit-loss proof and retired the prior FAM-006 carry-forward branch after release and merge.`
- Owned Behavior / Fact Class: `Retired branch-plan index and branch cleanup evidence.`
- Canonical Owner / Source Owner: `Docs/branch_plans/retirement_index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low from current origin/main; rerun Pre-Rebaseline Impact Audit if origin/main advances before PR.`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve incoming PR #212 retirement-index additions and preserve this branch's cleanup/no-unique-commit-loss receipt for the FAM-006 release-posture carry-forward branch.`
- Rebaseline Handling: `Preserve incoming current-main retirement context and this branch-local FAM-006 cleanup evidence.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, and release-readiness health gate.`
- Fallback Evidence: `Stage 1 packet, branch cleanup proof, and this Recording Profile branch authority record.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup and fold-down.`
- Fold-Down Target: `Retain prior FAM-006 carry-forward branch as retired/historical; do not restore active authority.`

### Changed Surface: Docs/branch_records/feature_fam_006_v1_7_19_release_posture_carry_forward.md

- Surface Class: `governance/source-truth`
- Change Intent: `Record the merged/deleted FAM-006 release-posture carry-forward branch authority as historical/no-active after release and branch cleanup.`
- Why This File Was Touched: `Branch Readiness Stage 2 folded down the prior active FAM-006 release-support authority before admitting the Recording Profile Runtime Foundation branch.`
- Owned Behavior / Fact Class: `Historical branch authority for the released/deleted FAM-006 carry-forward branch.`
- Canonical Owner / Source Owner: `Docs/branch_records/feature_fam_006_v1_7_19_release_posture_carry_forward.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `Medium`
- Expected Conflict Risk: `Low from current origin/main; rerun Pre-Rebaseline Impact Audit if origin/main advances before PR.`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve incoming PR #212 current-main historical/fold-down authority state and preserve this branch setup truth that Recording Profile Runtime Foundation is the active FAM-006 authority.`
- Rebaseline Handling: `Preserve incoming current-main fold-down context and this branch-local FAM-006 authority transition evidence.`
- Validation Proof: `Branch governance validation, branch readiness planning fixture validation, and release-readiness health gate.`
- Fallback Evidence: `Stage 1 packet, branch cleanup proof, and this Recording Profile branch authority record.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup and fold-down.`
- Fold-Down Target: `Retain as historical/no-active authority evidence; do not restore as active authority.`

### Changed Surface: Docs/feature_backlog.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve the active FAM-006 Recording Profile Runtime Foundation compact backlog pointer while accepting incoming FAM-007 v1.7.20 release-posture current-main context.`
- Why This File Was Touched: `Branch Readiness Stage 2 and Workstream Entry repair aligned the compact FAM-006 backlog row with the active Recording Profile branch after Overlay Display Acceptance release and branch cleanup.`
- Owned Behavior / Fact Class: `Compact FAM-006 family status and canonical detail pointer; not runtime behavior, release execution, PR state, issue state, FAM-007 ownership, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/feature_backlog.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium - incoming main updates FAM-007 release posture while this branch preserves FAM-006 active runtime-branch status and detail owner.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 v1.7.20 release-posture backlog truth as current-main context and preserve the FAM-006 Recording Profile Runtime Foundation row, active branch pointer, historical Overlay Display Acceptance evidence, and pending Workstream/SLC-046 implementation boundary.`
- Rebaseline Handling: `Preserve incoming current-main FAM-007 release posture and this branch-local FAM-006 active branch authority; do not accept FAM-007 package identity as FAM-006 identity.`
- Validation Proof: `Branch governance validation, release-readiness health gate, FAM-006 HUD validators when required by changed files, source-owner marker validation, and runtime-fam006 validation-suite recommendation.`
- Fallback Evidence: `FAM-006 branch authority record, this branch plan, compact backlog row, and incoming FAM-007 release-posture branch record.`
- USER Decision / Waiver: `USER approved bounded overlap-intent source-truth repair before current-main reconciliation; no waiver to drop incoming current-main or FAM-006 branch-local authority.`
- Fold-Down Target: `At PR Readiness/merge, compact backlog must project merge-stable FAM-006 branch posture without stale active branch wording.`

### Changed Surface: Docs/phase_governance.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve branch-local governance clarifications needed for bounded Workstream continuation and validation while accepting incoming FAM-007 release-posture governance context.`
- Why This File Was Touched: `Prior FAM-006 work added governance/validation standards for bounded Workstream continuation and LV1 proof discipline that remain relevant to the Recording Profile Runtime Foundation package.`
- Owned Behavior / Fact Class: `Repo-wide phase governance and approval-boundary behavior; not FAM-006 runtime behavior, release execution, PR creation, issue mutation, FAM-007 ownership, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/phase_governance.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium - incoming main may update release/readiness or FAM-007 governance while this branch preserves bounded Workstream/LV1 governance rules required by FAM-006.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 v1.7.20 release-posture governance additions as current-main context and preserve branch-local bounded Workstream continuation, real-proof, and validation-governance rules already accepted on this FAM-006 branch.`
- Rebaseline Handling: `Preserve both current-main governance additions and this branch-local FAM-006 governance repair; if wording conflicts, keep the stricter phase-gate requirement unless source truth proves it belongs to a different carrier.`
- Validation Proof: `Branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, and compileall when validator code changes.`
- Fallback Evidence: `FAM-006 Workstream Entry repair records, branch authority record, this branch plan, and incoming FAM-007 release-posture records.`
- USER Decision / Waiver: `USER approved bounded overlap-intent source-truth repair before current-main reconciliation; no waiver to weaken phase governance.`
- Fold-Down Target: `Durable repo-wide governance remains after PR merge only where merge-stable; branch-specific narration must fold into branch records/plans.`

### Changed Surface: Docs/prebeta_roadmap.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve the active FAM-006 Recording Profile Runtime Foundation roadmap pointer while accepting incoming FAM-007 v1.7.20 release-posture current-main context.`
- Why This File Was Touched: `Branch Readiness Stage 2 and Workstream Entry repair aligned the compact FAM-006 roadmap row with the active Recording Profile branch and historical Overlay Display Acceptance release evidence.`
- Owned Behavior / Fact Class: `Compact FAM-006 roadmap/milestone pointer truth; not runtime behavior, latest release truth, PR state, issue state, FAM-007 ownership, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/prebeta_roadmap.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium - incoming main updates FAM-007 release-window posture while this branch preserves FAM-006 active runtime-branch roadmap status.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 v1.7.20 release-posture roadmap truth as current-main context and preserve the FAM-006 Recording Profile Runtime Foundation detail owner, historical Overlay Display Acceptance evidence, and pending SLC-046 implementation boundary.`
- Rebaseline Handling: `Preserve incoming current-main FAM-007 roadmap updates and this branch-local FAM-006 active roadmap pointer; do not let either family overwrite the other's compact row.`
- Validation Proof: `Branch governance validation, release-readiness health gate, release body validation, FAM-006 HUD validators when required by changed files, and source-owner marker validation.`
- Fallback Evidence: `FAM-006 branch authority record, this branch plan, compact roadmap row, and incoming FAM-007 release-posture branch record.`
- USER Decision / Waiver: `USER approved bounded overlap-intent source-truth repair before current-main reconciliation; no waiver to drop incoming current-main or FAM-006 branch-local authority.`
- Fold-Down Target: `At PR Readiness/merge, roadmap must project merge-stable FAM-006 branch posture without stale active branch wording.`

### Changed Surface: Docs/validation_helper_registry.md

- Surface Class: `governance/source-truth`
- Change Intent: `Preserve validator/helper registry entries needed for FAM-006 Workstream validation while accepting incoming FAM-007 v1.7.20 validator/helper registry context.`
- Why This File Was Touched: `FAM-006 Workstream Entry repair aligned HUD validators and validation-suite expectations with the active Recording Profile branch and preserved historical Overlay Profile/Overlay Display evidence.`
- Owned Behavior / Fact Class: `Validation helper ownership, helper reuse, and validator scope registry; not runtime behavior, release execution, PR state, or family ownership by itself.`
- Canonical Owner / Source Owner: `Docs/validation_helper_registry.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium - incoming main may add FAM-007 release-posture validator expectations while this branch preserves FAM-006 HUD/runtime validation routing.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 v1.7.20 validator/helper registry additions as current-main context and preserve FAM-006 HUD validator, internal sandbox, runtime-fam006 validation-suite, and branch-governance helper routing needed for SLC-046 through SLC-050.`
- Rebaseline Handling: `Preserve both families' validator registry entries without collapsing FAM-007 provider/release validation into FAM-006 Recording Profile validation or vice versa.`
- Validation Proof: `Branch governance validation, source-owner marker validation, FAM-006 HUD validators, FAM-006 internal sandbox validation, runtime-fam006 validation-suite recommendation, and compileall when helper code changes.`
- Fallback Evidence: `Validation helper registry, FAM-006 branch plan, FAM-006 branch authority record, and incoming FAM-007 branch records.`
- USER Decision / Waiver: `USER approved bounded overlap-intent source-truth repair before current-main reconciliation; no waiver to remove required validator routing.`
- Fold-Down Target: `Merge-stable helper registry entries remain durable; branch-specific helper exceptions must be resolved before PR Readiness unless source truth grants an explicit carry-forward.`

### Changed Surface: dev/orin_branch_governance_validation.py

- Surface Class: `validator/helper`
- Change Intent: `Preserve validator behavior needed for FAM-006 bounded Workstream, branch authority, overlap-intent, and release-readiness checks while accepting incoming FAM-007 v1.7.20 validator updates.`
- Why This File Was Touched: `Prior branch-local governance/validator repair extended repo-wide validation so FAM-006 Workstream and LV1 proof standards are machine-checkable before implementation and PR readiness.`
- Owned Behavior / Fact Class: `Repo-wide branch governance validator behavior; not product runtime behavior, recording execution, tray controls, export/share, provider/model work, or family ownership by itself.`
- Canonical Owner / Source Owner: `dev/orin_branch_governance_validation.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `High - incoming main may update validator logic for FAM-007 release posture while this branch carries FAM-006 governance/Workstream validation behavior.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming FAM-007 v1.7.20 validator changes and preserve FAM-006 bounded Workstream, overlap-intent, active branch authority, and proof-governance validation behavior; after reconciliation, rerun governance, worktree-confinement, release-health, planning fixture, source-owner, HUD, runtime-fam006 recommendation, and compileall validation.`
- Rebaseline Handling: `Manual inspection required during current-main reconciliation; do not accept one side wholesale if it would drop either incoming FAM-007 release-posture checks or branch-local FAM-006 Workstream/proof checks.`
- Validation Proof: `git diff checks, branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, source-owner marker validation, FAM-006 HUD validators, runtime-fam006 validation-suite recommendation, and compileall.`
- Fallback Evidence: `Validator registry, branch governance validator output, FAM-006 branch authority record, this branch plan, and incoming FAM-007 release-posture records.`
- USER Decision / Waiver: `USER approved bounded overlap-intent source-truth repair before current-main reconciliation; no waiver to weaken validator coverage.`
- Fold-Down Target: `Durable validator behavior remains repo-wide after merge only if all validation passes; branch-specific assumptions must fold into branch records/plans or be removed before PR Readiness.`

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

Next Legal Phase: `Governed Workstream continuation decision`
Exact USER Decision Needed: `Approve governed FAM-006 Workstream continuation decision in C:\Nexus Worktrees\FAM-006 on feature/fam-006-recording-profile-runtime-foundation after SLC-047 H1 green. This approval covers verifying repo/worktree identity and current source truth, inspecting the SLC-046 through SLC-050 package state, determining whether the next legal route is SLC-048 Recording Profile relationship mapping and boundaries or a repo-truth-selected phase-boundary route, applying only narrow source-truth updates if required, running required validation, committing and pushing if files change, and returning the exact next implementation or phase approval packet. It does not approve SLC-048 implementation, tray recording controls, recording execution, export/share, provider/model work, broad theme/skin work, FAM-007 work, PR creation, merge, release, issue mutation, sibling-worktree mutation, or artifacts/raw evidence handling.`
