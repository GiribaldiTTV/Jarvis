# Branch Runtime Engineering Plan - FAM-006 Overlay Display Acceptance Foundation

Branch: `feature/fam-006-overlay-display-acceptance-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
Created From: `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8`
Current Plan Phase: `Workstream / SLC-042 through SLC-045 implemented pending final validation / Hardening H1 next`
Runtime Implementation Approval: `Granted for bounded multi-seam Workstream execution across admitted SLC-042 through SLC-045`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Overlay Display Acceptance Foundation`
Owning Branch: `feature/fam-006-overlay-display-acceptance-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
Current Phase: `Workstream / SLC-045 validation`
Branch Runtime Engineering Plan: `Accepted Stage 2 setup, Workstream Entry plan, bounded SLC-042 implementation, JavaScript proof closure, governed Workstream continuation, bounded SLC-043 active display implementation, bounded SLC-044 Dashboard / Overlay independence implementation, and bounded SLC-045 readiness proof for the FAM-006 Overlay Display Acceptance successor branch.`
Engineering Plan Status: `Accepted`
Current Runtime Baseline: `Released FAM-006 Dashboard, Sensor Command Center, Monitor Groups, and Overlay Profile Runtime Foundation with historical visual-governance closure.`
Branch Purpose: `Prepare the overlay display acceptance successor lane so later seams can prove profile-aware HUD Overlay display behavior without broad theme/skin or Recording Profile scope.`
Planned Runtime Delta: `SLC-042 adds the overlay display acceptance baseline and active-profile state bridge, including rendered-card proof driven by active Overlay Profile state, stale-card cleanup, null-state proof, high-volume proof, and renderer signal proof. SLC-043 adds a compact overlay-display active-profile status strip, active-profile display proof helper, and renderer signal proof. SLC-044 adds Dashboard / Overlay independence proof markers, proof helper, and renderer signal proof. SLC-045 adds Workstream readiness proof and renderer signal proof while preserving H1/LV1/UTS as later phases.`
User-Facing Delta: `SLC-043 adds visible active Overlay Profile status on the overlay display surface only; SLC-044 proves Dashboard and Overlay remain visually/functionally independent while sharing approved state. No new profile editor controls, Recording Profile runtime, broad theme/skin work, or Monitor Group ownership changes are included.`
Source-Truth Delta: `Stage 2 adds branch authority, branch plan, and compact backlog/roadmap pointers for the new FAM-006 successor lane.`
State / Config / Schema Delta: `SLC-042 adds HUD page bridge/proof metadata and renderer signal payloads only; persisted Overlay Profile, Monitor Group, and Recording Profile schemas remain unchanged.`
Validator / Helper Delta: `FAM-006 HUD surface/internal sandbox validators assert SLC-042 proof hook coverage, SLC-043 active-display proof hook coverage, SLC-044 independence proof hook coverage, SLC-045 readiness proof hook coverage, renderer signal coverage, null/high-volume proof, stale-card cleanup proof, visual acceptance baseline proof, H1/LV1 routing posture, and non-recording/non-theme boundaries. Bundled Codex runtime Node closes JavaScript syntax proof for nexus_visual/monitoring_hud.js when local node.exe is blocked by Access is denied.`
Expected Changed Files / Surfaces: `Setup touches branch record, branch plan, backlog, and roadmap. Future implementation may touch nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, desktop renderer/state/control/placement surfaces, and FAM-006 validators/helpers.`
Workstream / Seam Map: `SLC-042 baseline/state bridge; SLC-043 active profile display behavior; SLC-044 Dashboard/Overlay independence and visual acceptance; SLC-045 validation/live proof and UTS handoff readiness.`
Per-Seam Implementation Checklist: `SLC-042 bridge/baseline seam complete; SLC-043 active display behavior complete; SLC-044 Dashboard/Overlay independence complete; SLC-045 validation/live proof readiness implemented pending validation/commit.`
Per-Seam Validation Checklist: `Each seam must run diff checks, governance as needed, HUD surface/internal validators when touched, compileall, syntax/runtime checks as supported, and focused proof helpers where user-facing behavior changes.`
Per-Seam User-Facing Proof Checklist: `Future user-facing seams must capture focused per-element screenshots, short video/frame-sequence proof, null/high-volume stress proof for variable lists/dropdowns, and Codex Visual Adjudication before UTS.`
Future-Gated Items: `Recording Profile runtime, tray recording, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007, Governance mutation, Compact-AI, stale branch cleanup, PR creation, merge, release, issues, and artifacts remain pending USER decisions.`
Approval-Boundary Audit: `Stage 2 setup only is approved; runtime implementation and all future-gated work are blocked until separately approved.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 HUD surfaces are expected; FAM-007/provider surfaces, Governance worktree, Compact-AI, and Repo-Wide markers are sibling context only.`
Open Questions: `SLC-042 through SLC-045 implementation/proof readiness is complete pending validation/commit; Hardening H1 is next after green closure and requires USER approval.`
USER Planning Decisions: `USER approved Stage 2 setup from current origin/main and did not approve runtime implementation, PR creation, merge, release, issue mutation, artifacts, cleanup, or sibling-worktree mutation.`
Plan Revision History: `v1 - Stage 2 setup created from origin/main a42b7e50eb012722b140f3874dbf50826bd797c8. v2 - governed current-main reconciliation merged origin/main 6681131c974d99945c494c0e4ff3c436f9347422, preserved PR #200 governance/source-truth context, preserved the feature_vision_update_decision_matrix active pointer as current-main context, and reasserted FAM-006 branch-local authority. v3 - Workstream Entry source-truth/validator sync repaired compact FAM-006 roadmap and HUD validator expectations, created/refreshed the Workstream Entry Review Bundle, and selected SLC-042 as the first bounded implementation seam pending USER approval. v4 - bounded SLC-042 implementation added overlay display acceptance bridge/proof runtime markers, renderer proof signal, HUD validators, and traceability updates. v5 - continuation decision selected SLC-043 active Overlay Profile display behavior because SLC-043 through SLC-045 remain admitted and implementable before Hardening. v6 - bounded SLC-043 implementation added visible active-profile display status, active display proof helper, renderer signal, validator coverage, and source-truth traceability. v7 - bounded SLC-044 implementation added Dashboard / Overlay independence markers, proof helper, renderer signal, validator coverage, and source-truth traceability. v8 - bounded SLC-045 implementation added Workstream readiness proof, H1/LV1/UTS routing posture, renderer signal, validator coverage, and Workstream Green source-truth routing.`
Plan-To-Implementation Traceability Table: `Planned SLC-042 implementation delta was the overlay display acceptance baseline and active-profile state bridge. Actual SLC-042 implementation file trace: nexus_visual/monitoring_hud.html adds acceptance markers; nexus_visual/monitoring_hud.js adds proof helper, active-profile rendered-card behavior, stale-card cleanup, null/high-volume proof, and boundary proof; desktop/desktop_renderer.py adds MONITORING_HUD_OVERLAY_DISPLAY_ACCEPTANCE_BRIDGE_READY; dev/orin_monitoring_hud_surface_validation.py and dev/orin_monitoring_hud_internal_sandbox_validation.py add validator coverage. Actual SLC-043 implementation file trace: nexus_visual/monitoring_hud.html adds the active-profile display status strip; nexus_visual/monitoring_hud.css styles the compact display status; nexus_visual/monitoring_hud.js adds SLC-043 display state, null/stale/high-volume proof, and state export; desktop/desktop_renderer.py adds MONITORING_HUD_ACTIVE_OVERLAY_PROFILE_DISPLAY_READY; HUD validators add SLC-043 proof coverage. Actual SLC-044 implementation file trace: nexus_visual/monitoring_hud.js adds Dashboard / Overlay independence markers and proof helper; desktop/desktop_renderer.py adds MONITORING_HUD_DASHBOARD_OVERLAY_INDEPENDENCE_READY; HUD validators add SLC-044 proof coverage. Actual SLC-045 implementation file trace: nexus_visual/monitoring_hud.js adds Workstream readiness proof and H1/LV1 routing posture; desktop/desktop_renderer.py adds MONITORING_HUD_OVERLAY_DISPLAY_WORKSTREAM_READY; HUD validators add SLC-045 proof coverage. JavaScript proof uses bundled Codex runtime Node --check for nexus_visual/monitoring_hud.js after local node.exe Access is denied.`
Hardening Comparison Checklist: `Future H1 must compare completed SLC-042 through SLC-045 implementation against planned runtime, state/schema, user-facing, validation, and boundary deltas, including null/high-volume membership proof, stale-card cleanup, renderer signal payload, non-recording/non-theme scope, active-profile display behavior, Dashboard/Overlay independence, and preservation of existing FAM-006 surfaces.`
Live Validation Proof Or Waiver Checklist: `Future LV1 must use real user-facing launcher proof where feasible, OneDrive focused screenshots, short video/frame-sequence proof, visual adjudication, and USER_TEST_REQUIRED until returned review.`
PR Readiness Fold-Down / Retention Checklist: `Pending - PR Readiness will decide what active plan detail folds into durable historical source truth.`
Release Readiness Public-Scope Translation Checklist: `Pending - release wording must describe only validated user-facing display acceptance, not future-gated recording/theme/provider work.`
USER Planning Review: `Accepted for Stage 2 setup, Workstream Entry review, bounded SLC-042 implementation, SLC-042 proof closure, and governed Workstream continuation through admitted seams.`
PR Fold-Down Packet: `Pending`
Runtime Implementation Approval: `Granted by USER for bounded multi-seam Workstream execution across admitted SLC-042 through SLC-045`

## Purpose

This plan admits the next FAM-006 runtime successor after the released Overlay Profile Runtime Foundation. The branch implements bounded admitted Workstream seams after Workstream execution approval so the HUD Overlay display path can rely on active Overlay Profile state while preserving Monitor Groups, Sensor Command Center, Recording Profile boundaries, and the visual-validation hardening learned from the historical Overlay Profile lane.

## Historical Closure Carry-Forward

Historical Overlay Profile Repairs: `Closed / PASS`
Historical Evidence Basis: `feature_fam_006_overlay_profile_runtime_foundation records Codex Visual Adjudication PASS, HUD-wide visual inspection matrix PASS, mandatory OneDrive focused per-element screenshots, short video/frame-sequence proof, returned USER UTS PASS, null-profile proof, 125-profile stress proof, and dropdown/list clipping repairs.`
Carry-Forward Rule: `Those repairs are baseline requirements for this branch. They are not reopened unless regression appears, and future LV1 cannot clear without the same artifact-by-artifact visual adjudication discipline for current surfaces.`

## Package And Slice Admission

Family: `FAM-006 - Monitoring and HUD`
Package: `PKG-006 - Monitoring and HUD`
Package Posture: `Released baseline / open successor branch`

| Slice | Admission State | Purpose | Current Status |
| --- | --- | --- | --- |
| `SLC-042` Overlay display acceptance baseline and state bridge | Admitted | Implement the smallest display-acceptance baseline that can consume active Overlay Profile state without changing broad HUD skins or Recording Profile behavior. | Implemented / proof closed |
| `SLC-043` Active Overlay Profile display behavior | Admitted | Prove the visible overlay display path reacts to active Overlay Profile state and remains deterministic across null and high-volume profile/member states. | Implemented / validation pending |
| `SLC-044` Dashboard / Overlay display independence and visual acceptance | Admitted | Prove Dashboard, Overlay display, and Monitor Groups stay visually and functionally independent while sharing approved state. | Implemented / proof closed |
| `SLC-045` Validation/live proof and UTS handoff readiness | Admitted | Extend focused validators/live proof as needed, route to H1/LV1, and prepare USER-facing UTS only after Codex Visual Adjudication passes in Live Validation. | Implemented / validation pending |

Single-Slice Package User Approval: `Not required - this branch admits multiple concrete slices under FAM-006 / PKG-006.`
Package Completion State: `Open / not package-complete`

## Product Definition Plan

Project-Wide Vision Alignment: `The HUD should be trustworthy, compact, visually uniform, and validated with real user-facing proof rather than helper-only marks. Overlay display acceptance is part of making the monitoring surface feel like a real product rather than a disconnected settings demo.`
Branch-Specific Vision Alignment: `The branch should convert historical Overlay Profile state into accepted display behavior while preserving the hard-earned UI quality rules from returned USER review: readable controls, unclipped selectors, NDAI scrollbars, no grid bleed-through, uniform button states, and per-element proof.`
System Concept Model: `Overlay Profile is a state/config profile. Overlay display is the rendered display behavior. Monitor Groups configure monitors and sources. Recording Profile is future runtime scope. Dashboard is the entry and status surface.`
Entity / Profile Model: `Overlay Profile, active Overlay Profile, overlay display state/read model, monitor membership read model, HUD Overlay display card/window, Dashboard state, validation artifact, and USER issue/UTS result are separate entities from Monitor Group and Recording Profile.`
User Workflow Model: `A user should be able to open Dashboard, understand which Overlay Profile is active, open or observe HUD Overlay display behavior, and trust that the displayed overlay matches the selected profile and remains readable under scale.`
Scale / Data Volume Model: `Every variable dropdown/list/selection surface introduced or touched later must receive null-state and high-volume stress proof. Overlay/profile surfaces should assume 0 profiles, 1 profile, and 100+ profiles; monitor/source surfaces should assume 0 and 100+ where legal.`
Configuration And State Model: `SLC-037 Overlay Profile persisted state remains canonical. Any new display acceptance state must be additive, normalized, migration-safe, and clearly separated from Recording Profile state.`
Expected User-Facing Outcomes: `No user-facing runtime delta in Stage 2 setup. Later user-facing outcomes should be accepted HUD Overlay display behavior that is profile-aware, responsive, and visually adjudicated before UTS.`
Codex Additional Recommendations: `Start with SLC-042 as an analysis and baseline proof seam before expanding render behavior. The branch should avoid redesigning the entire HUD, even if visual polish rules are preserved.`
USER Critique Loop: `USER has repeatedly identified visual defects missed by validation. This plan treats visual proof as a product requirement, not a courtesy artifact.`
USER Decision Ledger: `USER approved Stage 2 setup. USER has not approved runtime implementation, PR creation, merge, release, issue mutation, stale branch cleanup, artifacts/raw evidence handling, FAM-007, Governance mutation, Recording Profile runtime, tray recording, export/share, provider/model work, or broad theme/skin work.`
Deferred Ideas / Future Package Ledger: `Recording Profile, tray recording, export/share/import, visual theme/skin packs, profile duplication/deletion expansion beyond existing released baseline, layout personalization, provider telemetry parity, FAM-007, Compact-AI, and AI Product remain future-gated.`
Planning Adequacy Review: `Adequate for Stage 2 setup and Workstream Entry; implementation details must be selected in Workstream Entry before runtime mutation.`
Rejected Shallow Plan: `Rejected: reuse old overlay/deferred markers or helper screenshots as acceptance. Acceptance must prove the actual display path and user-visible behavior.`
Alternatives And Tradeoffs Reviewed: `A broad HUD redesign would risk scope creep; a Recording Profile branch would violate pending decisions; a narrow Overlay Display Acceptance Foundation follows the released FAM-006 sequence.`
Whole-System Interaction Map: `Dashboard -> active Overlay Profile -> HUD Overlay display -> proof/validation -> USER UTS. Manage Monitors and Sensor Command Center are preservation surfaces.`
Minimum Viable vs Full System Boundary: `Minimum viable branch proves overlay display acceptance foundation. Full system includes recording/export/theme/provider integrations and remains outside this branch.`
Open Questions / USER Decision Points: `Workstream continues through SLC-043, SLC-044, and SLC-045 unless blocked by validation, source-truth conflict, current-main reconciliation, USER stop, or a real named blocker; later decisions cover H1, LV1/UTS, PR creation, merge, release, and future-gated scope.`

## Runtime Branch Engineering Contract

USER Engineering Planning Review: `Accepted for Stage 2 setup, Workstream Entry review, and bounded SLC-042 implementation`
Runtime Implementation Approval: `Granted - bounded multi-seam Workstream execution through admitted SLC-042 through SLC-045`
Current Runtime Baseline: `Released FAM-006 Dashboard, Sensor Command Center, Monitor Groups, and Overlay Profile Runtime Foundation with historical visual-governance closure.`
Planned Runtime Delta: `SLC-042 adds overlay display acceptance bridge/proof runtime markers, active-profile rendered-card proof, stale-card cleanup, null-state proof, high-volume membership proof, and renderer bridge signal MONITORING_HUD_OVERLAY_DISPLAY_ACCEPTANCE_BRIDGE_READY. SLC-043 adds visible active-profile status, active-display proof state, and renderer signal MONITORING_HUD_ACTIVE_OVERLAY_PROFILE_DISPLAY_READY.`
User-Facing Runtime Delta: `No new visible controls in SLC-042; this seam is bridge/proof oriented and preserves existing Dashboard, Manage Monitors, Sensor Command Center, and Overlay Profile controls.`
State / Config / Schema Delta: `SLC-042 uses transient HUD page state and renderer payload metadata; no persisted schema migration is added and Overlay Profile, Monitor Group, and Recording Profile concepts remain separate.`
Validator / Helper Delta: `FAM-006 HUD surface/internal validators now verify SLC-042 and SLC-043 static/runtime proof coverage, renderer signal coverage, null/high-volume proof markers, stale-card removal proof, active display status proof, and boundary proof.`
Expected Changed Files / Surfaces: `Likely future surfaces include nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, desktop/desktop_renderer.py, desktop/monitoring_hud_state.py, desktop/monitoring_hud_controls.py, desktop/monitoring_hud_placement.py, dev/orin_monitoring_hud_surface_validation.py, dev/orin_monitoring_hud_internal_sandbox_validation.py, dev/orin_monitoring_hud_live_validation.ps1, and dev/orin_monitoring_hud_human_client_validation.ps1.`
Approval-Boundary Audit: `Only Stage 2 source-truth setup is approved. Runtime behavior remains blocked.`
Future-Gated Items: `Recording Profile runtime, tray recording controls, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007, Governance worktree mutation, Compact-AI, Repo-Wide markers, stale branch cleanup, PR creation, merge, release, issue mutation, artifacts/raw evidence handling.`
Workstream Seam Map: `SLC-042 baseline/state bridge; SLC-043 active profile display behavior; SLC-044 Dashboard/Overlay independence and visual acceptance; SLC-045 validation/live proof and UTS handoff readiness.`
Proof Expectations: `Identity/freshness proof, H1 pressure tests, LV1 real user-facing desktop launcher proof where applicable, per-element focused screenshots in OneDrive, mandatory short video/frame-sequence proof, Codex Visual Adjudication, null/high-volume stress proof for variable selectors/lists, unclipped/responsive geometry proof, and preservation proof for existing FAM-006 surfaces.`
Risk Forecast: `Visual false-green, selector/list clipping, overlay display and Dashboard state coupling, Recording Profile boundary drift, broad theme/skin creep, and stale source-truth carry-forward are primary risks.`
Recommendations And Alternatives: `Prefer Workstream Entry to choose a small first SLC-042 seam and leave SLC-043 render behavior until the baseline bridge and proof method are clear.`
Plan Version / Revision Status: `v4 - SLC-042 Workstream implementation recorded after Stage 2 setup, current-main reconciliation, Workstream Entry source-truth/validator sync, and review-bundle traceability repair.`
Plan-To-Implementation Traceability: `SLC-042 implementation updates the HUD overlay display acceptance marker, JS proof helper, renderer signal, HUD validators, branch authority record, and this plan. SLC-043 implementation updates the overlay display status strip, active display proof helper, renderer signal, validators, branch authority record, and this plan. SLC-044 implementation updates Dashboard / Overlay independence markers, proof helper, renderer signal, validators, branch authority record, and this plan. SLC-045 implementation updates Workstream readiness proof, H1/LV1 routing markers, renderer signal, validators, branch authority record, and this plan.`

## Element-to-Phase Proof Matrix

Matrix Status: `Accepted for active Workstream implementation.`
USER Review Status: `Accepted - bounded Workstream continuation is active.`
Open Element Questions: `Queued - Workstream Entry must select the first bounded SLC-042 seam and confirm proof depth for SLC-042 through SLC-045.`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_overlay_display_acceptance_foundation.md`
Element Validation Ledger Owner: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ELEM-FAM006-ODA-001 | Overlay display acceptance baseline and active-profile state bridge | Touched | Workstream implemented the approved SLC-042 bridge/proof seam, preserving Overlay Profile, Monitor Group, and Recording Profile separation. | Workstream proof runs branch/source-truth validation plus HUD validators required by changed files and records bridge/state evidence against SLC-042, including active profile selection, stale-card cleanup, null-state, and high-volume membership proof. | Hardening compares actual bridge behavior, state flow, validator coverage, and boundary preservation against this matrix and the Runtime Branch Engineering Contract. | Live Validation records focused proof or a scoped waiver for any user-facing bridge behavior, with per-element screenshots if visible display state is affected. | USER acceptance path uses the LV1 UTS only after H1 and Codex Visual Adjudication are green or explicitly waived. | Recording Profile runtime, tray recording, export/share, provider/model work, broad theme/skin work, FAM-007, and Governance mutation remain outside this element. | Accepted - implemented and proof closed. | Active branch plan and FAM-006 branch authority record. |
| ELEM-FAM006-ODA-002 | Active Overlay Profile display behavior | Touched | Workstream implements SLC-043 as the bounded continuation seam; display behavior reacts deterministically to active Overlay Profile state through a compact display status strip and active-profile rendered cards. | Workstream proof covers null, one-profile, stale active reference, and high-volume profile/member states plus state-read and renderer-signal evidence required by changed files. | Hardening stress-tests active-profile display behavior, stale/missing profile references, state refresh, and preservation of Dashboard and Manage Monitors behavior. | Live Validation captures focused user-facing proof, short video/frame-sequence evidence where behavior changes, and visual adjudication for accepted display surfaces. | USER acceptance path asks the USER to verify profile-aware display behavior only after Codex proof is complete. | Profile duplicate/delete expansion, Recording Profile behavior, and broad UI/theme redesign are future-gated. | Accepted - implemented pending validation/commit. | Active branch plan and FAM-006 branch authority record. |
| ELEM-FAM006-ODA-003 | Dashboard, HUD Overlay, Monitor Groups, and Sensor Command Center independence | Touched | Workstream touches shared FAM-006 surfaces only where SLC-044 proof requires it and preserves current Dashboard/Monitor Groups/Sensor Command Center behavior. | Workstream proof includes changed-file review, HUD surface/internal validation, Dashboard / Overlay independence proof, renderer signal evidence, and source-truth traceability. | Hardening pressure-tests window independence, layout/clipping, control responsiveness, visual uniformity, and preservation of existing FAM-006 behavior under null and stress data. | Live Validation uses the real user-facing launcher where feasible, OneDrive per-element screenshots, and artifact-by-artifact visual adjudication for affected windows/cards/rows/buttons/dropdowns/scrollbars. | USER acceptance path focuses UTS questions on changed or preservation-critical surfaces after Codex-visible defects are repaired. | Deeper Dashboard redesign, layout personalization, and broad theme/skin work remain future package scope unless USER separately approves. | Accepted - implemented pending validation/commit. | Active branch plan and FAM-006 branch authority record. |
| ELEM-FAM006-ODA-004 | Validation, live proof, and UTS handoff readiness | Touched | Workstream updates validators/helpers/source truth only where needed to prove the admitted overlay display acceptance scope and route cleanly to H1/LV1. | Workstream proof confirms validators cover changed surfaces, null/high-volume selectors or lists, visual proof obligations, H1/LV1 routing, and issue-form mapping posture where applicable. | Hardening reruns required validators, stress-proofs high-risk states, and confirms no helper-only or screenshot-existence-only false green remains. | Live Validation must capture mandatory focused screenshots under the OneDrive Nexus screenshots directory, short video/frame-sequence proof, real-client proof where feasible, and Codex Visual Adjudication before UTS handoff. | USER acceptance path is a formal LV1 User Test Summary after all mandatory proof gates are green or waived with reason. | PR creation, merge, release, issue mutation, stale branch cleanup, artifacts/raw evidence handling outside approved proof, and sibling-worktree mutation remain pending decisions. | Accepted - implemented pending validation/commit. | Active branch plan, validation helper registry, and FAM-006 branch authority record. |

## Branch Change Intent Ledger

### Changed Surface: Docs/branch_records/index.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-006 intentionally edits the branch authority router only to add Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md under Active Branch Authority Records for the approved FAM-006 successor branch.`
- Why This File Was Touched: `Branch Readiness Stage 2 setup created and bound feature/fam-006-overlay-display-acceptance-foundation in C:\Nexus Worktrees\FAM-006, so the active branch authority index needed a compact pointer to the new FAM-006 authority record.`
- Owned Behavior / Fact Class: `Active branch authority routing for the FAM-006 Overlay Display Acceptance Foundation branch; not runtime behavior, release state, PR state, issue state, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/branch_records/index.md owns active/historical branch authority routing; this branch plan owns the overlap intent evidence for the FAM-006 branch-local edit.`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - origin/main / PR #200 also edits Docs/branch_records/index.md for current-main governance/source-truth rules and the active feature_vision_update_decision_matrix pointer.`
- Overlap Risk: `High - branch authority router edits can accidentally drop active branch records or incoming governance rules if reconciled by inertia.`
- Expected Conflict Risk: `Medium - both branches edit the Active Branch Authority Records area, but the expected final state should preserve both active pointers and the incoming governance rule additions.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming PR #200 governance additions, preserve the active Docs/branch_records/feature_vision_update_decision_matrix.md pointer, and preserve the active Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md pointer. Do not accept incoming current-main active-branch identity as FAM-006 identity; origin/main is context, not identity.`
- Rebaseline Handling: `After this ledger repair is committed and pushed, rerun the Pre-Rebaseline Impact Audit. If the overlap gate clears, USER may approve a governed non-rewrite merge/reconciliation of origin/main into feature/fam-006-overlay-display-acceptance-foundation.`
- Validation Proof: `Before rebaseline mutation, run the Pre-Rebaseline Impact Audit with this branch plan path plus git diff checks, branch governance validation, worktree-confinement validation, branch readiness planning fixture validation, release body validation, AI provider state validation, source-owner marker validation, and compileall.`
- Fallback Evidence: `Current diffs show the FAM-006 branch adds only its active authority pointer, while PR #200 adds governance/source-truth rules and the feature_vision_update_decision_matrix active pointer; fallback evidence supports classification only and is not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this bounded Branch Change Intent Ledger repair only; rebaseline merge/rebase mutation remains pending separate USER decision.`
- Fold-Down Target: `Keep this overlap-intent evidence in the active branch plan until PR Readiness fold-down decides retention, compaction, or historical projection.`

### Changed Surface: Docs/feature_backlog.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-006 intentionally edits the compact backlog pointer/status surface only to preserve the active Overlay Display Acceptance Foundation Workstream Green state, Hardening H1 routing, and branch-local detail owner for the approved FAM-006 successor branch.`
- Why This File Was Touched: `The completed SLC-042 through SLC-045 Workstream updated FAM-006 package status and next-phase routing after Overlay Display Acceptance Foundation implementation and proof closure.`
- Owned Behavior / Fact Class: `Compact FAM-006 package pointer/status truth; not runtime behavior, release state, PR state, issue state, FAM-007 ownership, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/feature_backlog.md owns compact family backlog state; this branch plan owns overlap intent evidence for the FAM-006 branch-local edit.`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - origin/main / PR #201 also edits Docs/feature_backlog.md for FAM-007 consent collection implementation foundation current-main context.`
- Overlap Risk: `High - compact backlog edits can accidentally replace one family package pointer/status with another or drop branch-local next-phase truth during current-main reconciliation.`
- Expected Conflict Risk: `Medium - both branches edit family backlog rows/status language, but the expected final state should preserve incoming FAM-007 consent implementation context and the FAM-006 Overlay Display Acceptance Foundation Workstream Green / Hardening H1 route.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming PR #201 FAM-007 consent collection implementation foundation backlog status and pointers as current-main context, and preserve FAM-006 Overlay Display Acceptance Foundation branch-local status, detail owner, Workstream Green evidence, and Hardening H1 next-phase routing. Do not accept incoming FAM-007 package identity as FAM-006 identity; origin/main is context, not identity.`
- Rebaseline Handling: `After this ledger repair is committed and pushed, rerun the Pre-Rebaseline Impact Audit. If the overlap gate clears, USER may approve governed non-rewrite reconciliation of origin/main into feature/fam-006-overlay-display-acceptance-foundation.`
- Validation Proof: `Before rebaseline mutation, run the Pre-Rebaseline Impact Audit with this branch plan path plus git diff checks, branch governance validation, worktree-confinement validation, branch readiness planning fixture validation, release body validation, AI provider state validation, source-owner marker validation, FAM-006 HUD validators where required by changed files, and compileall.`
- Fallback Evidence: `Current diffs show origin/main updates FAM-007 backlog truth, while this branch updates FAM-006 backlog truth; fallback evidence supports classification only and is not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this bounded Branch Change Intent Ledger repair only; rebaseline merge/rebase mutation remains pending separate USER decision.`
- Fold-Down Target: `Keep this overlap-intent evidence in the active branch plan until PR Readiness fold-down decides retention, compaction, or historical projection.`

### Changed Surface: Docs/phase_governance.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-006 intentionally edits phase governance to enforce bounded Workstream continuation once USER green-lights an admitted Workstream package, so per-seam approval bookkeeping cannot stop before the Workstream phase is complete and the next phase is green.`
- Why This File Was Touched: `During SLC-042 through SLC-045 continuation, source truth needed to clarify that approved Workstream phase work remains bounded but should continue through the admitted package until Workstream Green or a real stop condition, then route to Hardening H1.`
- Owned Behavior / Fact Class: `Governed phase-routing and approval-boundary behavior for active Workstream execution; not runtime behavior, release execution, PR creation, issue mutation, FAM-007 ownership, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/phase_governance.md owns phase rules; this branch plan owns overlap intent evidence for the FAM-006 branch-local governance clarification.`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - origin/main / PR #201 also edits Docs/phase_governance.md for current-main governance updates.`
- Overlap Risk: `High - phase-governance edits can silently change legal phase routing, approval requirements, or stop conditions if reconciled without intent evidence.`
- Expected Conflict Risk: `Medium - both branches edit governance rules, but the expected final state should preserve incoming PR #201 governance/current-main updates and the FAM-006 bounded Workstream continuation clarification.`
- Semantic Merge Risk: `High`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming PR #201 phase-governance additions as current-main context and preserve the FAM-006 bounded Workstream continuation rule that, after USER approval to start the admitted Workstream package, Codex continues within approved boundaries until Workstream Green or a true stop condition before routing to H1. Do not broaden this into runtime implementation, PR creation, merge, release, issue mutation, or sibling-worktree authority.`
- Rebaseline Handling: `After this ledger repair is committed and pushed, rerun the Pre-Rebaseline Impact Audit. If the overlap gate clears, USER may approve governed non-rewrite reconciliation of origin/main into feature/fam-006-overlay-display-acceptance-foundation.`
- Validation Proof: `Before rebaseline mutation, run the Pre-Rebaseline Impact Audit with this branch plan path plus git diff checks, branch governance validation, worktree-confinement validation, branch readiness planning fixture validation, release body validation, AI provider state validation, source-owner marker validation, and compileall.`
- Fallback Evidence: `Current diffs show origin/main adds PR #201 governance context and this branch adds the FAM-006 Workstream-continuation clarification; fallback evidence supports classification only and is not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this bounded Branch Change Intent Ledger repair only; rebaseline merge/rebase mutation remains pending separate USER decision.`
- Fold-Down Target: `Keep this overlap-intent evidence in the active branch plan until PR Readiness fold-down decides retention, compaction, or historical projection.`

### Changed Surface: Docs/prebeta_roadmap.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-006 intentionally edits the compact prebeta roadmap pointer/status surface only to preserve Overlay Display Acceptance Foundation Workstream Green state, Hardening H1 routing, and future monitoring/HUD USER-gated boundaries.`
- Why This File Was Touched: `The completed FAM-006 Overlay Display Acceptance Foundation Workstream changed the current compact roadmap posture for FAM-006 while preserving historical Overlay Profile foundation evidence and future-gated Monitoring/HUD scope.`
- Owned Behavior / Fact Class: `Compact roadmap status and FAM-006 package pointer truth; not runtime behavior, release state, PR state, issue state, FAM-007 ownership, or sibling-worktree ownership.`
- Canonical Owner / Source Owner: `Docs/prebeta_roadmap.md owns compact prebeta roadmap state; this branch plan owns overlap intent evidence for the FAM-006 branch-local edit.`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - origin/main / PR #201 also edits Docs/prebeta_roadmap.md for FAM-007 consent collection implementation foundation current-main context.`
- Overlap Risk: `High - compact roadmap edits can accidentally drop released/historical FAM-006 evidence, current FAM-006 next-phase routing, or incoming FAM-007 current-main status.`
- Expected Conflict Risk: `Medium - both branches edit family roadmap rows/status language, but the expected final state should preserve incoming FAM-007 consent implementation context and FAM-006 Overlay Display Acceptance Foundation Workstream Green / Hardening H1 route.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve incoming PR #201 FAM-007 consent collection implementation foundation roadmap status and pointers as current-main context, and preserve FAM-006 Overlay Display Acceptance Foundation roadmap status, historical Overlay Profile evidence, future monitoring/HUD USER-gated boundary, and Hardening H1 next-phase routing. Do not accept incoming FAM-007 package identity as FAM-006 identity; origin/main is context, not identity.`
- Rebaseline Handling: `After this ledger repair is committed and pushed, rerun the Pre-Rebaseline Impact Audit. If the overlap gate clears, USER may approve governed non-rewrite reconciliation of origin/main into feature/fam-006-overlay-display-acceptance-foundation.`
- Validation Proof: `Before rebaseline mutation, run the Pre-Rebaseline Impact Audit with this branch plan path plus git diff checks, branch governance validation, worktree-confinement validation, branch readiness planning fixture validation, release body validation, AI provider state validation, source-owner marker validation, FAM-006 HUD validators where required by changed files, and compileall.`
- Fallback Evidence: `Current diffs show origin/main updates FAM-007 roadmap truth, while this branch updates FAM-006 roadmap truth; fallback evidence supports classification only and is not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this bounded Branch Change Intent Ledger repair only; rebaseline merge/rebase mutation remains pending separate USER decision.`
- Fold-Down Target: `Keep this overlap-intent evidence in the active branch plan until PR Readiness fold-down decides retention, compaction, or historical projection.`

## Validation Plan

Stage 2 Validation: `git diff --check; git diff --cached --check after staging; python dev\orin_branch_governance_validation.py; python dev\orin_branch_governance_validation.py --worktree-confinement-gate; python dev\orin_branch_readiness_planning_fixture_validation.py; python dev\orin_release_body_validation.py; python dev\orin_ai_provider_state_validation.py; python -m compileall -q desktop dev nexus_visual`
Future Workstream Validation: `Use validation-suite recommendations plus FAM-006 HUD surface/internal/live/human-client validators as required by changed files and source truth. SLC-042 requires HUD surface/internal validators, runtime-fam006 validation suite, diff checks, governance checks, source-owner marker validation, compileall, and supported JS syntax/runtime checks; bundled Codex runtime Node is the accepted local alternate when node.exe is blocked by Access is denied.`

## Stage 2 Setup Exit

Exit Criteria: `Branch record, branch plan, compact backlog/roadmap pointers, worktree binding proof, validation, commit, and push are complete.`
Next Legal Phase: `Hardening`
Exact USER Approval Text: `Approve Hardening H1 for FAM-006 in C:\Nexus Worktrees\FAM-006 on feature/fam-006-overlay-display-acceptance-foundation to pressure-test the completed SLC-042 through SLC-045 Overlay Display Acceptance Foundation Workstream, including active Overlay Profile display behavior, null/stale/high-volume proof, Dashboard / Overlay independence, visual acceptance readiness, validators/helpers/source truth, and preservation of Dashboard / Manage Monitors / Sensor Command Center behavior, with bounded H1 repairs, validation, commit, and push if green, without executing LV1/UTS, PR creation, merge, release, issue mutation, stale branch cleanup, artifacts/raw evidence handling beyond approved proof, sibling-worktree mutation, Recording Profile runtime, tray recording controls, export/share, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, or Governance worktree mutation.`
