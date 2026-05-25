# Branch Runtime Engineering Plan - FAM-006 Recording Profile Runtime Foundation

Branch: `feature/fam-006-recording-profile-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
Created From: `origin/main` at `26dded3f84c526e0525c7d3b18fcd2607e16590d`
Current Plan Phase: `Branch Readiness Stage 1 posture after Workstream rollback`
Runtime Implementation Approval: `Blocked - Recording Profile Workstream implementation was rolled back by USER request; future active-overlay-driven recording implementation requires new Branch Readiness and Workstream approval`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Recording Profile Runtime Foundation`
Owning Branch: `feature/fam-006-recording-profile-runtime-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
Current Phase: `Branch Readiness Stage 1 posture after Workstream rollback`
Branch Runtime Engineering Plan: `Recording Profile Runtime Foundation branch setup and planning admission.`
Engineering Plan Status: `Accepted for Stage 2 setup`
Current Runtime Baseline: `FAM-006 Overlay Profile Runtime Foundation and Overlay Display Acceptance Foundation are released historical evidence. Recording Profile Workstream runtime changes are rolled back.`
Branch Purpose: `Return FAM-006 to Branch Readiness Stage 1 posture after USER rejected the profile-loaded Recording Profile direction and clarified active-overlay-driven recording vision.`
Planned Runtime Delta: `None after rollback. Future Workstream must be replanned around active-overlay-driven recording, not profile-loaded Recording Profile state.`
User-Facing Delta: `None after rollback; future user-visible UI/status/copy deltas must be approved through Branch Readiness and Workstream for HUD Overlay card recording controls or standalone Recording Settings.`
Source-Truth Delta: `Move merged/deleted FAM-006 release-posture carry-forward record from active to historical/no-active posture; add this active branch authority and branch plan; update compact backlog/roadmap pointers for the active Recording Profile planning branch; record cleanup/no-unique-commit proof.`
State / Config / Schema Delta: `None after rollback; future recording state/schema must be replanned from active Overlay Profile membership and recording output settings.`
Validator / Helper Delta: `Recording Profile Workstream validator/helper changes are reverted; future validators must be selected by the next Branch Readiness / Workstream path.`
Expected Changed Files / Surfaces: `Docs/branch_records/index.md; Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/feature_fam_006_recording_profile_runtime_foundation.md; Docs/branch_plans/README.md; Docs/branch_records/feature_fam_006_v1_7_19_release_posture_carry_forward.md; Docs/branch_plans/feature_fam_006_v1_7_19_release_posture_carry_forward.md; Docs/branch_plans/retirement_index.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md.`
Workstream / Seam Map: `Withdrawn for Recording Profile Runtime Foundation; future seam map must be selected by a new Branch Readiness / Workstream Entry path for active-overlay-driven recording.`
Per-Seam Implementation Checklist: `SLC-046 must name state/schema files before runtime edits; SLC-047 must name visible selector/editing files before UI edits; SLC-048 must name relationship/boundary files; SLC-049 must name Dashboard/Manage Monitors surfaces; SLC-050 must name validator/helper/proof files.`
Per-Seam Validation Checklist: `Each seam must define exact validators, fixtures, proof helpers, JS syntax/load checks where changed, H1 checks, LV1 real-input proof where user-facing, and regression proof for Overlay Profile, Monitor Group, Dashboard, Sensor Command Center, and Recording Profile separation.`
Per-Seam User-Facing Proof Checklist: `Pending Workstream Entry; any user-facing seam must carry real-input desktop validation and focused per-element screenshot requirements.`
Future-Gated Items: `Future-gated and pending USER approval: tray recording controls, actual recording execution, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, issue mutation, PR creation, merge, release, and artifacts/raw evidence handling.`
Approval-Boundary Audit: `Recording Profile Workstream implementation was rolled back by USER request. Runtime implementation, Workstream execution, PR, merge, release, issue, artifact, sibling-worktree, tray/export/provider/theme work are blocked pending separate USER approval.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 only. FAM-007 and Governance worktrees are sibling context and not mutable. Future runtime seams may touch HUD/Dashboard/Manage Monitors surfaces and must forecast overlap before implementation.`
Open Questions: `Pending USER decisions: Branch Readiness Stage 1 analysis for the next active-overlay-driven recording carrier, stable Overlay Profile Settings placement, durable recording output format, and any Recording Settings beyond folder path/open folder/Start/Stop.`
USER Planning Decisions: `USER approved Stage 1 analysis and Stage 2 setup for this branch, then requested rollback of all Recording Profile Workstream changes and return to Branch Readiness Stage 1 posture after clarifying active-overlay-driven recording vision.`
Plan Revision History: `v1 - Created after PR #212 merge and FAM-006 branch cleanup from current origin/main 26dded3f84c526e0525c7d3b18fcd2607e16590d.`
Plan-To-Implementation Traceability: `Recording Profile Workstream implementation evidence is superseded by rollback. Future implementation must start from a new Branch Readiness / Workstream trace for active-overlay-driven recording.`
Plan-To-Implementation Traceability Table: `Withdrawn for Recording Profile route; future rows must map active-overlay-driven recording deltas, files touched, validator/helper proof, H1 result, LV1/UTS proof, deferred boundaries, and commit evidence.`
Hardening Comparison Checklist: `Pending future Workstream implementation. H1 must compare actual behavior against the corrected active-overlay-driven recording vision and concept separation.`
Live Validation Proof Or Waiver Checklist: `Pending future Workstream implementation. LV1 must use real user-facing launcher where feasible, real user-level input, compact/default window proof, per-element screenshots, output-file proof where applicable, and UTS handoff when user-facing behavior changes.`
PR Readiness Fold-Down / Retention Checklist: `Future PR Readiness must decide what branch-plan details fold into branch record, family vision/dossier, workstream record, or retirement index.`
Release Readiness Public-Scope Translation Checklist: `Future Release Readiness must describe only implemented and validated user-facing Recording Profile work; future-gated tray/export/provider/theme work must remain excluded.`
USER Planning Review: `Accepted for Branch Readiness Stage 2 setup only.`
Runtime Implementation Approval: `Blocked - Recording Profile Workstream was rolled back. Runtime implementation is blocked until Branch Readiness Stage 1 selects a corrected active-overlay-driven recording path and USER approves later Workstream implementation.`
PR Fold-Down Packet: `Pending future PR Readiness.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Recording Profile Runtime Foundation`
Package Posture: `Rolled back to Branch Readiness Stage 1 posture / runtime implementation withdrawn`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-046` Recording Profile data/state foundation | Withdrawn | Historical route superseded by active-overlay-driven recording vision. | Rolled back |
| `SLC-047` Recording Profile selection/editing entry points | Withdrawn | Historical route superseded by active-overlay-driven recording vision. | Rolled back |
| `SLC-048` Recording Profile relationship mapping and boundaries | Withdrawn | Historical route superseded by active-overlay-driven recording vision. | Rolled back |
| `SLC-049` Dashboard / Manage Monitors Recording Profile status integration | Withdrawn | Historical route superseded by active-overlay-driven recording vision. | Rolled back |
| `SLC-050` validation/live proof readiness | Withdrawn | Historical route superseded by active-overlay-driven recording vision. | Rolled back |

Single-Slice Package User Approval: `Not required - multiple concrete slices are admitted.`
Package Completion State: `Rolled back to Branch Readiness Stage 1 posture`

## Element-to-Phase Proof Matrix

Matrix Status: `Present`
USER Review Status: `Pending Branch Readiness Stage 1 analysis for successor active-overlay-driven recording path`
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
- Validation Proof: `Required validation must include branch governance validation, worktree-confinement gate, release-readiness health gate, branch-readiness planning fixture validation, FAM-006 HUD validators, runtime-fam006 validation suite recommendation, source-owner marker validation, and compileall before current-main reconciliation mutation resumes.`
- Fallback Evidence: `If incoming current-main changes overlap this router, use this branch plan ledger plus the active branch authority record as branch-owned intent evidence; compatibility still requires the explicit conflict-resolution rule and required validation.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup for this branch and later approved rollback to Branch Readiness Stage 1 posture; no waiver authorizes dropping incoming current-main governance context or the FAM-006 rollback/source-truth posture.`
- Fold-Down Target: `Merged/deleted FAM-006 release-posture carry-forward authority remains historical/no-active; this active FAM-006 branch remains the rollback receipt carrier until USER approves the next route.`

### Changed Surface: Docs/branch_plans/README.md

- Surface Class: `governance/source-truth`
- Change Intent: `Carry Branch Readiness Stage 2 branch-plan USER review packet routing context only as needed to reconcile current-main USER branch plan review gate governance with this FAM-006 rollback carrier.`
- Why This File Was Touched: `Current-main PR #217 added USER branch plan review gate governance context to the branch-plan index/README surface, and the FAM-006 branch already carries branch-plan review packet expectations from its Stage 2 setup and rollback posture.`
- Owned Behavior / Fact Class: `Branch plan review packet routing and governance context.`
- Canonical Owner / Source Owner: `Docs/branch_plans/README.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES`
- Overlap Risk: `High`
- Expected Conflict Risk: `Medium until current-main reconciliation completes because incoming main and FAM-006 both touch branch-plan review routing context.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming current-main USER branch plan review gate governance context, preserve this FAM-006 rollback posture, and preserve active-overlay-driven recording planning context without re-admitting Recording Profile runtime work.`
- Rebaseline Handling: `Preserve incoming current-main USER branch plan review gate governance context and this branch-local FAM-006 rollback/source-truth context.`
- Validation Proof: `Required validation must include branch governance validation, worktree-confinement gate, release-readiness health gate, branch-readiness planning fixture validation, FAM-006 HUD validators, runtime-fam006 validation suite recommendation, source-owner marker validation, and compileall before current-main reconciliation mutation resumes.`
- Fallback Evidence: `Use this branch plan ledger as branch-owned intent evidence for the FAM-006 rollback carrier; incoming current-main USER branch plan review gate governance remains authoritative current-main context to preserve.`
- USER Decision / Waiver: `USER approved this bounded pre-reconciliation overlap-intent repair only; no waiver authorizes current-main reconciliation, Branch Readiness Stage 1, runtime implementation, Workstream Entry, PR creation, merge, release, or future-gated recording work.`
- Fold-Down Target: `No branch-plan README fold-down is requested; reconcile by preserving incoming current-main USER branch plan review gate context and FAM-006 rollback planning context.`

## Workstream Entry Whole-Package Analysis Requirements

Superseded: the Recording Profile SLC-046 through SLC-050 package is withdrawn after USER rollback request. Future Workstream Entry must be preceded by Branch Readiness Stage 1 analysis for active-overlay-driven recording.

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

Next Legal Phase: `Branch Readiness Stage 1`
Exact USER Decision Needed: `Approve Branch Readiness Stage 1 analysis for the next FAM-006 active-overlay-driven recording carrier in C:\Nexus Worktrees\FAM-006. This approval covers analysis of the corrected recording vision, carrier/branch path, rollback/source-truth state, current-main freshness, branch cleanup risk, and exact Stage 2 setup decision text only. It does not approve runtime implementation, Workstream implementation, PR creation, merge, release, issue mutation, artifacts/raw evidence handling, sibling-worktree mutation, export/share, provider/model work, broad theme/skin work, FAM-007 work, or Governance worktree mutation.`
