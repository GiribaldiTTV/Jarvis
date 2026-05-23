# Branch Runtime Engineering Plan - FAM-006 Overlay Display Acceptance Foundation

Branch: `feature/fam-006-overlay-display-acceptance-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
Created From: `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8`
Current Plan Phase: `Workstream / SLC-042 implementation and proof closure complete / SLC-043 pending USER approval`
Runtime Implementation Approval: `Granted for bounded SLC-042 implementation only`

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Overlay Display Acceptance Foundation`
Owning Branch: `feature/fam-006-overlay-display-acceptance-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-006`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
Current Phase: `Workstream / SLC-042 implementation complete`
Branch Runtime Engineering Plan: `Accepted Stage 2 setup, Workstream Entry plan, bounded SLC-042 implementation, and JavaScript proof closure for the FAM-006 Overlay Display Acceptance successor branch; bounded SLC-043 implementation is pending USER approval.`
Engineering Plan Status: `Accepted for SLC-043 implementation approval packet`
Current Runtime Baseline: `Released FAM-006 Dashboard, Sensor Command Center, Monitor Groups, and Overlay Profile Runtime Foundation with historical visual-governance closure.`
Branch Purpose: `Prepare the overlay display acceptance successor lane so later seams can prove profile-aware HUD Overlay display behavior without broad theme/skin or Recording Profile scope.`
Planned Runtime Delta: `SLC-042 adds the overlay display acceptance baseline and active-profile state bridge, including rendered-card proof driven by active Overlay Profile state, stale-card cleanup, null-state proof, high-volume proof, and renderer signal proof.`
User-Facing Delta: `No new visible profile editor controls in SLC-042; existing Dashboard, Manage Monitors, Sensor Command Center, and released Overlay Profile controls are preservation surfaces.`
Source-Truth Delta: `Stage 2 adds branch authority, branch plan, and compact backlog/roadmap pointers for the new FAM-006 successor lane.`
State / Config / Schema Delta: `SLC-042 adds HUD page bridge/proof metadata and renderer signal payloads only; persisted Overlay Profile, Monitor Group, and Recording Profile schemas remain unchanged.`
Validator / Helper Delta: `FAM-006 HUD surface/internal sandbox validators now assert SLC-042 proof hook coverage, renderer signal coverage, null/high-volume membership proof, stale-card cleanup proof, and non-recording/non-theme boundaries. Bundled Codex runtime Node closes JavaScript syntax proof for nexus_visual/monitoring_hud.js when local node.exe is blocked by Access is denied.`
Expected Changed Files / Surfaces: `Setup touches branch record, branch plan, backlog, and roadmap. Future implementation may touch nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, desktop renderer/state/control/placement surfaces, and FAM-006 validators/helpers.`
Workstream / Seam Map: `SLC-042 baseline/state bridge; SLC-043 active profile display behavior; SLC-044 Dashboard/Overlay independence and visual acceptance; SLC-045 validation/live proof and UTS handoff readiness.`
Per-Seam Implementation Checklist: `SLC-042 choose bridge/baseline seam; SLC-043 implement display behavior if approved; SLC-044 harden Dashboard/Overlay independence; SLC-045 complete validation/live proof readiness.`
Per-Seam Validation Checklist: `Each seam must run diff checks, governance as needed, HUD surface/internal validators when touched, compileall, syntax/runtime checks as supported, and focused proof helpers where user-facing behavior changes.`
Per-Seam User-Facing Proof Checklist: `Future user-facing seams must capture focused per-element screenshots, short video/frame-sequence proof, null/high-volume stress proof for variable lists/dropdowns, and Codex Visual Adjudication before UTS.`
Future-Gated Items: `Recording Profile runtime, tray recording, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007, Governance mutation, Compact-AI, stale branch cleanup, PR creation, merge, release, issues, and artifacts remain pending USER decisions.`
Approval-Boundary Audit: `Stage 2 setup only is approved; runtime implementation and all future-gated work are blocked until separately approved.`
FAM / Shared-Surface Overlap Forecast: `FAM-006 HUD surfaces are expected; FAM-007/provider surfaces, Governance worktree, Compact-AI, and Repo-Wide markers are sibling context only.`
Open Questions: `SLC-042 implementation and proof closure are complete; USER must approve bounded SLC-043 implementation before active Overlay Profile display behavior can mutate runtime surfaces.`
USER Planning Decisions: `USER approved Stage 2 setup from current origin/main and did not approve runtime implementation, PR creation, merge, release, issue mutation, artifacts, cleanup, or sibling-worktree mutation.`
Plan Revision History: `v1 - Stage 2 setup created from origin/main a42b7e50eb012722b140f3874dbf50826bd797c8. v2 - governed current-main reconciliation merged origin/main 6681131c974d99945c494c0e4ff3c436f9347422, preserved PR #200 governance/source-truth context, preserved the feature_vision_update_decision_matrix active pointer as current-main context, and reasserted FAM-006 branch-local authority. v3 - Workstream Entry source-truth/validator sync repaired compact FAM-006 roadmap and HUD validator expectations, created/refreshed the Workstream Entry Review Bundle, and selected SLC-042 as the first bounded implementation seam pending USER approval. v4 - bounded SLC-042 implementation added overlay display acceptance bridge/proof runtime markers, renderer proof signal, HUD validators, and traceability updates. v5 - continuation decision selected SLC-043 active Overlay Profile display behavior because SLC-043 through SLC-045 remain admitted and implementable before Hardening.`
Plan-To-Implementation Traceability Table: `Planned SLC-042 implementation delta was the overlay display acceptance baseline and active-profile state bridge. Actual implementation file trace: nexus_visual/monitoring_hud.html adds acceptance markers; nexus_visual/monitoring_hud.js adds proof helper, active-profile rendered-card behavior, stale-card cleanup, null/high-volume proof, and boundary proof; desktop/desktop_renderer.py adds MONITORING_HUD_OVERLAY_DISPLAY_ACCEPTANCE_BRIDGE_READY; dev/orin_monitoring_hud_surface_validation.py and dev/orin_monitoring_hud_internal_sandbox_validation.py add validator coverage; Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md and this plan add source-truth traceability. JavaScript proof closure uses bundled Codex runtime Node --check for nexus_visual/monitoring_hud.js after local node.exe Access is denied. SLC-043 through SLC-045 remain pending.`
Hardening Comparison Checklist: `Future H1 must compare completed SLC-042 through SLC-045 implementation against planned runtime, state/schema, user-facing, validation, and boundary deltas, including null/high-volume membership proof, stale-card cleanup, renderer signal payload, non-recording/non-theme scope, active-profile display behavior, Dashboard/Overlay independence, and preservation of existing FAM-006 surfaces.`
Live Validation Proof Or Waiver Checklist: `Future LV1 must use real user-facing launcher proof where feasible, OneDrive focused screenshots, short video/frame-sequence proof, visual adjudication, and USER_TEST_REQUIRED until returned review.`
PR Readiness Fold-Down / Retention Checklist: `Pending - PR Readiness will decide what active plan detail folds into durable historical source truth.`
Release Readiness Public-Scope Translation Checklist: `Pending - release wording must describe only validated user-facing display acceptance, not future-gated recording/theme/provider work.`
USER Planning Review: `Accepted for Stage 2 setup, Workstream Entry review, bounded SLC-042 implementation, and SLC-042 proof closure; SLC-043 implementation approval is required next.`
PR Fold-Down Packet: `Pending`
Runtime Implementation Approval: `Granted by USER for bounded SLC-042 implementation only`

## Purpose

This plan admits the next FAM-006 runtime successor after the released Overlay Profile Runtime Foundation. The branch will prepare, then later implement only after USER approval, an Overlay Display Acceptance Foundation that proves the HUD Overlay display path can rely on active Overlay Profile state while preserving Monitor Groups, Sensor Command Center, Recording Profile boundaries, and the visual-validation hardening learned from the historical Overlay Profile lane.

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
| `SLC-043` Active Overlay Profile display behavior | Admitted | Prove the visible overlay display path reacts to active Overlay Profile state and remains deterministic across null and high-volume profile/member states. | Planned |
| `SLC-044` Dashboard / Overlay display independence and visual acceptance | Admitted | Prove Dashboard, Overlay display, and Monitor Groups stay visually and functionally independent while sharing approved state. | Planned |
| `SLC-045` Validation/live proof and UTS handoff readiness | Admitted | Extend focused validators/live proof as needed, run H1/LV1, and prepare USER-facing UTS only after Codex Visual Adjudication passes. | Planned |

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
Open Questions / USER Decision Points: `USER must approve bounded SLC-043 implementation; later decisions cover SLC-044 through SLC-045, H1, LV1/UTS, PR creation, merge, release, and future-gated scope.`

## Runtime Branch Engineering Contract

USER Engineering Planning Review: `Accepted for Stage 2 setup, Workstream Entry review, and bounded SLC-042 implementation`
Runtime Implementation Approval: `Granted - bounded SLC-042 only`
Current Runtime Baseline: `Released FAM-006 Dashboard, Sensor Command Center, Monitor Groups, and Overlay Profile Runtime Foundation with historical visual-governance closure.`
Planned Runtime Delta: `SLC-042 adds overlay display acceptance bridge/proof runtime markers, active-profile rendered-card proof, stale-card cleanup, null-state proof, high-volume membership proof, and renderer bridge signal MONITORING_HUD_OVERLAY_DISPLAY_ACCEPTANCE_BRIDGE_READY.`
User-Facing Runtime Delta: `No new visible controls in SLC-042; this seam is bridge/proof oriented and preserves existing Dashboard, Manage Monitors, Sensor Command Center, and Overlay Profile controls.`
State / Config / Schema Delta: `SLC-042 uses transient HUD page state and renderer payload metadata; no persisted schema migration is added and Overlay Profile, Monitor Group, and Recording Profile concepts remain separate.`
Validator / Helper Delta: `FAM-006 HUD surface/internal validators now verify SLC-042 static/runtime proof coverage, renderer signal coverage, null/high-volume proof markers, stale-card removal proof, and boundary proof.`
Expected Changed Files / Surfaces: `Likely future surfaces include nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, desktop/desktop_renderer.py, desktop/monitoring_hud_state.py, desktop/monitoring_hud_controls.py, desktop/monitoring_hud_placement.py, dev/orin_monitoring_hud_surface_validation.py, dev/orin_monitoring_hud_internal_sandbox_validation.py, dev/orin_monitoring_hud_live_validation.ps1, and dev/orin_monitoring_hud_human_client_validation.ps1.`
Approval-Boundary Audit: `Only Stage 2 source-truth setup is approved. Runtime behavior remains blocked.`
Future-Gated Items: `Recording Profile runtime, tray recording controls, export/share/import, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007, Governance worktree mutation, Compact-AI, Repo-Wide markers, stale branch cleanup, PR creation, merge, release, issue mutation, artifacts/raw evidence handling.`
Workstream Seam Map: `SLC-042 baseline/state bridge; SLC-043 active profile display behavior; SLC-044 Dashboard/Overlay independence and visual acceptance; SLC-045 validation/live proof and UTS handoff readiness.`
Proof Expectations: `Identity/freshness proof, H1 pressure tests, LV1 real user-facing desktop launcher proof where applicable, per-element focused screenshots in OneDrive, mandatory short video/frame-sequence proof, Codex Visual Adjudication, null/high-volume stress proof for variable selectors/lists, unclipped/responsive geometry proof, and preservation proof for existing FAM-006 surfaces.`
Risk Forecast: `Visual false-green, selector/list clipping, overlay display and Dashboard state coupling, Recording Profile boundary drift, broad theme/skin creep, and stale source-truth carry-forward are primary risks.`
Recommendations And Alternatives: `Prefer Workstream Entry to choose a small first SLC-042 seam and leave SLC-043 render behavior until the baseline bridge and proof method are clear.`
Plan Version / Revision Status: `v4 - SLC-042 Workstream implementation recorded after Stage 2 setup, current-main reconciliation, Workstream Entry source-truth/validator sync, and review-bundle traceability repair.`
Plan-To-Implementation Traceability: `SLC-042 implementation updates the HUD overlay display acceptance marker, JS proof helper, renderer signal, HUD validators, branch authority record, and this plan. SLC-043 is selected next to implement active Overlay Profile display behavior; SLC-044 through SLC-045 remain pending.`

## Element-to-Phase Proof Matrix

Matrix Status: `Accepted for Workstream Entry review before implementation begins.`
USER Review Status: `Pending - USER approval is required before runtime implementation.`
Open Element Questions: `Queued - Workstream Entry must select the first bounded SLC-042 seam and confirm proof depth for SLC-042 through SLC-045.`
Element Coverage Owner: `Docs/branch_plans/feature_fam_006_overlay_display_acceptance_foundation.md`
Element Validation Ledger Owner: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ELEM-FAM006-ODA-001 | Overlay display acceptance baseline and active-profile state bridge | Touched | Workstream implemented the approved SLC-042 bridge/proof seam, preserving Overlay Profile, Monitor Group, and Recording Profile separation. | Workstream proof runs branch/source-truth validation plus HUD validators required by changed files and records bridge/state evidence against SLC-042, including active profile selection, stale-card cleanup, null-state, and high-volume membership proof. | Hardening compares actual bridge behavior, state flow, validator coverage, and boundary preservation against this matrix and the Runtime Branch Engineering Contract. | Live Validation records focused proof or a scoped waiver for any user-facing bridge behavior, with per-element screenshots if visible display state is affected. | USER acceptance path uses the LV1 UTS only after H1 and Codex Visual Adjudication are green or explicitly waived. | Recording Profile runtime, tray recording, export/share, provider/model work, broad theme/skin work, FAM-007, and Governance mutation remain outside this element. | Accepted - implemented and proof closed. | Active branch plan and FAM-006 branch authority record. |
| ELEM-FAM006-ODA-002 | Active Overlay Profile display behavior | Planned | Workstream may implement SLC-043 only after SLC-042 is green and USER approves the seam; display behavior must react deterministically to active Overlay Profile state. | Workstream proof covers null, one-profile, and high-volume profile/member states plus persistence or state-read evidence required by changed files. | Hardening stress-tests active-profile display behavior, stale/missing profile references, state refresh, and preservation of Dashboard and Manage Monitors behavior. | Live Validation captures focused user-facing proof, short video/frame-sequence evidence where behavior changes, and visual adjudication for accepted display surfaces. | USER acceptance path asks the USER to verify profile-aware display behavior only after Codex proof is complete. | Profile duplicate/delete expansion, Recording Profile behavior, and broad UI/theme redesign are future-gated. | Pending USER approval for later seam implementation. | Active branch plan and FAM-006 branch authority record. |
| ELEM-FAM006-ODA-003 | Dashboard, HUD Overlay, Monitor Groups, and Sensor Command Center independence | Planned | Workstream may touch shared FAM-006 surfaces only where the approved seam requires it and must preserve current Dashboard/Monitor Groups/Sensor Command Center behavior. | Workstream proof includes changed-file review, HUD surface/internal validation when touched, and source-truth traceability for any shared-surface edit. | Hardening pressure-tests window independence, layout/clipping, control responsiveness, visual uniformity, and preservation of existing FAM-006 behavior under null and stress data. | Live Validation uses the real user-facing launcher where feasible, OneDrive per-element screenshots, and artifact-by-artifact visual adjudication for affected windows/cards/rows/buttons/dropdowns/scrollbars. | USER acceptance path focuses UTS questions on changed or preservation-critical surfaces after Codex-visible defects are repaired. | Deeper Dashboard redesign, layout personalization, and broad theme/skin work remain future package scope unless USER separately approves. | Pending USER approval for later seam implementation. | Active branch plan and FAM-006 branch authority record. |
| ELEM-FAM006-ODA-004 | Validation, live proof, and UTS handoff readiness | Planned | Workstream and later SLC-045 update validators/helpers/source truth only where needed to prove the admitted overlay display acceptance scope. | Workstream proof confirms validators cover changed surfaces, null/high-volume selectors or lists, visual proof obligations, and issue-form mapping when applicable. | Hardening reruns required validators, stress-proofs high-risk states, and confirms no helper-only or screenshot-existence-only false green remains. | Live Validation must capture mandatory focused screenshots under the OneDrive Nexus screenshots directory, short video/frame-sequence proof, real-client proof where feasible, and Codex Visual Adjudication before UTS handoff. | USER acceptance path is a formal LV1 User Test Summary after all mandatory proof gates are green or waived with reason. | PR creation, merge, release, issue mutation, stale branch cleanup, artifacts/raw evidence handling outside approved proof, and sibling-worktree mutation remain pending decisions. | Pending USER approval for later validation/live-proof seam work. | Active branch plan, validation helper registry, and FAM-006 branch authority record. |

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

## Validation Plan

Stage 2 Validation: `git diff --check; git diff --cached --check after staging; python dev\orin_branch_governance_validation.py; python dev\orin_branch_governance_validation.py --worktree-confinement-gate; python dev\orin_branch_readiness_planning_fixture_validation.py; python dev\orin_release_body_validation.py; python dev\orin_ai_provider_state_validation.py; python -m compileall -q desktop dev nexus_visual`
Future Workstream Validation: `Use validation-suite recommendations plus FAM-006 HUD surface/internal/live/human-client validators as required by changed files and source truth. SLC-042 requires HUD surface/internal validators, runtime-fam006 validation suite, diff checks, governance checks, source-owner marker validation, compileall, and supported JS syntax/runtime checks; bundled Codex runtime Node is the accepted local alternate when node.exe is blocked by Access is denied.`

## Stage 2 Setup Exit

Exit Criteria: `Branch record, branch plan, compact backlog/roadmap pointers, worktree binding proof, validation, commit, and push are complete.`
Next Legal Phase: `Workstream`
Exact USER Approval Text: `Approve bounded SLC-043 Workstream implementation for FAM-006 Overlay Display Acceptance Foundation in C:\Nexus Worktrees\FAM-006 on feature/fam-006-overlay-display-acceptance-foundation to implement active Overlay Profile display behavior only, preserving Overlay Profile / Monitor Group / Recording Profile separation, preserving existing Dashboard / Manage Monitors / Sensor Command Center behavior, using the SLC-042 active-profile state bridge as the baseline, updating only required HUD overlay display runtime/state/renderer bridge surfaces, validators/helpers, and directly supporting source truth, proving null, one-profile, stale-reference, and high-volume profile/member states, proving overlay display remains non-recording and non-theme scope, running required validation including bundled runtime JavaScript syntax proof if local node.exe is blocked, committing and pushing if green, and returning the SLC-043 Workstream implementation packet without Hardening H1 execution, PR creation, merge, release, issue mutation, stale branch cleanup, artifacts/raw evidence handling beyond approved proof, sibling-worktree mutation, Recording Profile runtime, tray recording controls, export/share, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, or Governance worktree mutation.`
