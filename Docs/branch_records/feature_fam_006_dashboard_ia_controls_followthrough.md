# Branch Authority Record: feature/fam-006-dashboard-ia-controls-followthrough

## Branch Identity

- Branch: `feature/fam-006-dashboard-ia-controls-followthrough`
- Workstream: `FAM-006 Dashboard IA / Controls Follow-Through`
- Branch Class: `implementation`
- Backlog Record State: `Registry-only issue-resolution continuation under historical FAM-006 / PKG-006`
- Package ID: `PKG-006`
- Package Name: `Monitoring HUD Dashboard Product Surface`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 setup carrier and Workstream implementation carrier for the second FAM-006 Dashboard issue-resolution branch.

It exists because PR #129 merged the first FAM-006 Dashboard issue-resolution branch for render/layout hardening, issues #125 and #126 remain open and held for Dashboard IA/control follow-through, and USER approved Branch Readiness Stage 2 setup for `feature/fam-006-dashboard-ia-controls-followthrough` from current `origin/main`.

Current authorization covers Hardening/H1 validation for issues #125 and #126 only, directly supporting validator/source-truth updates, validation, commit, and push. GitHub issue comments/state updates, raw evidence upload/import/linking, PR creation, release/tag/artifact work, Workspace Runtime Isolation Stage 2, FAM-007/local AI work, AI Product Contract import, and branch expansion beyond #125/#126 remain future USER approval checkpoints.

## Record State

- `Active Hardening H1 repair/validation complete for #125/#126; next phase pending USER decision`

## Status

- `Dashboard IA/control follow-through H1 validation complete for issues #125 and #126; GitHub issue closeout/comment updates and PR creation remain blocked pending USER approval`

## Canonical Branch

- `feature/fam-006-dashboard-ia-controls-followthrough`

## Current Phase

- Phase: `Hardening`

## Phase Status

- Stage 1: `Complete - Stage 1 analysis recommended carrying #125 and #126 together because they share the Dashboard IA/control surface, validation path, and USER-facing proof path`
- Stage 2 USER Approval: `Granted - USER approved Branch Readiness Stage 2 for feature/fam-006-dashboard-ia-controls-followthrough from current main, carrying existing GitHub issues #125 and #126 only`
- Branch Creation: `Created in C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough from origin/main commit 96ec36e7be751d444eda8dc220bc4a035d44fca1`
- GitHub Desktop Association: `GitHub Desktop was asked to open/add the new C-drive worktree; local GitHub Desktop log records adding the repository at C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough; GitHub Desktop local alias is FAM-006`
- Workstream USER Approval: `Granted - USER approved runtime implementation on feature/fam-006-dashboard-ia-controls-followthrough in the isolated Branch 2 worktree for GitHub issues #125 and #126 only`
- Workstream Implementation: `Complete - Monitor Groups card flow now uses dedicated Create Monitor and Edit Monitor child-window flows, the Dashboard-home dropdown is removed, the redundant HUD Dashboard Open badge is removed, and a top-chrome Dashboard close affordance hides the Dashboard without disabling the HUD Feature`
- Hardening H1 Admission: `Granted - USER approved H1 validation/hardening for FAM-006 Branch 2 on 2026-05-13 from the isolated Branch 2 worktree`
- Hardening H1 Status: `PASS - active-client H1 validation completed from C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough on 2026-05-13 for #125 and #126 after bounded stale-selector cleanup; formal UTS export remains blocked unless a later governed Live Validation phase is admitted`
- `Active Branch`: `feature/fam-006-dashboard-ia-controls-followthrough`
- Branch Authority State: `Active after Hardening H1; PR Readiness Stage 1 pending USER decision`
- Source-Truth Owner: `This branch record owns Branch 2 setup and issue traceability; Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md owns historical FAM-006 RUI and issue-queue truth`
- Carried Issues: `#125 FAM-006 Dashboard: Monitor Groups dead space and Create/Edit window split`; `#126 FAM-006 Dashboard: remove redundant open badge and add close affordance`
- Completed-By-PR-129 Issues Pending GitHub Closeout: `#123`; `#124`; `#127`
- Future / Deferred Items: `Dashboard settings cog/settings panel`; `Overlay/display acceptance`; `Provider/external telemetry parity`; `Dev Toolkit/source-owner markers`
- Evidence Policy: `Summary-only for GitHub issue and branch source-truth references`
- Raw Media Status: `Raw screenshots, videos, and UTS exports remain local/external unless USER later approves upload, import, or linking`
- Runtime Implementation: `Approved for #125/#126 and completed on this branch`
- FAM-007 / Local AI Authority: `Blocked and out of scope`

## Branch Class

- `implementation`

## Blockers

- `PR Readiness User Decision Pending`: active after Hardening H1 validation.
- `GitHub Issue Closeout Approval Missing`: active for #123/#124/#127 and any comments/state changes on #125/#126.
- `PR Creation Approval Missing`: active.
- `Raw Evidence Import Decision Pending`: active.
- `Release Execution Approval Missing`: active.
- `Branch Expansion Approval Missing`: active for any work outside #125/#126.
- `Workspace Runtime Isolation Stage 2 Approval Missing`: active.
- `FAM-007 / Local AI Authority Missing`: active and out of scope.
- `AI Product Contract Import Approval Missing`: active and out of scope.

## Entry Basis

- Current `origin/main` is `96ec36e7be751d444eda8dc220bc4a035d44fca1`, the merge commit for PR #129.
- PR #129 is merged and Branch 1 is historical traceability.
- Issues #123, #124, and #127 were implemented by PR #129 and remain pending GitHub issue closeout only.
- Issues #125 and #126 remain open GitHub issues and were held for Branch 2 in FAM-006 issue-readiness source truth.
- USER approved creating this Branch 2 carrier from current main and continuing Stage 2 in a new worktree to avoid mixing with uncommitted FAM-007 changes in `C:\Nexus Desktop AI`.
- The dirty FAM-007 work in `C:\Nexus Desktop AI` remains untouched by this branch; active Branch 2 work is isolated in `C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough`.

## Source-Truth Placement Preflight

- Existing issue-readiness owner: `Docs/branch_records/feature_fam_006_issue_readiness_governance_repair.md`.
- Existing FAM-006 RUI owner: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md`.
- Branch 1 historical owner: `Docs/branch_records/feature_fam_006_dashboard_render_layout_hardening.md`.
- Branch 2 active owner: this record.
- Placement decision: create this active Branch 2 authority record and register it in `Docs/branch_records/index.md`; keep backlog and roadmap merge-stable unless later repo truth requires broader current-state sync.

## Exit Criteria

- Branch authority is recorded for `feature/fam-006-dashboard-ia-controls-followthrough`.
- Issues #125 and #126 are recorded as carried-now scope.
- Issues #123, #124, and #127 remain recorded as completed by PR #129 but pending GitHub issue closeout.
- Summary-only evidence policy and raw-media external/local status are preserved.
- Source truth records that GitHub issue comments/state updates are not approved in this Stage 2 pass.
- Branch 2 non-goals remain explicit.
- Docs/governance validation passes.
- Workstream implementation changes for #125/#126 are committed and pushed after validation.
- Runtime implementation remains limited to #125/#126; any branch expansion requires separate USER approval.

## Rollback Target

- `Branch Readiness`

Rollback Path: abandon or repair branch `feature/fam-006-dashboard-ia-controls-followthrough` if USER rejects the Workstream implementation before PR creation. Do not mutate the dirty FAM-007 work in `C:\Nexus Desktop AI`, delete D-drive folders, edit GitHub issue state, import raw media, or recreate/reuse codex/ai-llm-lab.

## Next Legal Phase

- `PR Readiness`

Next Legal Phase Gate: USER may next choose PR Readiness Stage 1, request an optional USER visual review, or request bounded repair if a visual concern remains. PR creation, GitHub issue comments/state updates, raw evidence upload/import/linking, release/tag/artifact work, Workspace Runtime Isolation Stage 2, FAM-007/local AI work, AI Product Contract import, and any branch expansion remain blocked.

## Branch Objective

Prepare the FAM-006 Dashboard IA/control follow-through branch to resolve the remaining Dashboard issue threads after render/layout hardening:

- #125 Monitor Groups card dead space plus Create/Edit monitor window split.
- #126 Remove redundant HUD Dashboard Open badge and add close affordance.

## Target End-State

- The branch authority is established and pushed.
- Runtime implementation and H1 hardening validation for #125/#126 are complete and ready for USER decision on PR Readiness Stage 1 or optional USER visual review.
- The carried issue set remains limited to #125 and #126.
- Branch 1 issues #123/#124/#127 stay completed-by-PR #129 and pending GitHub issue closeout.
- Future/deferred Dashboard settings cog, Overlay/display acceptance, provider telemetry parity, Dev Toolkit/source-owner markers, Workspace Runtime Isolation, FAM-007/local AI, and AI Product Contract work remain out of scope.

## Planning-Loop Guardrail

Implementation Delta Class: runtime/user-facing

Docs-Only Workstream: No

Planning-Loop Bypass User Approval: None

Planning-Loop Bypass Reason: None

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`

Backlog-Split User Approval: None

Backlog-Split Reason: None

## Admitted Implementation Slice

- Slice ID: `FAM-006-BR2-Dashboard-IA-Controls`
- Goal: `Resolve the remaining USER-confirmed Dashboard IA/control follow-through issues #125 and #126 after PR #129 completed render/layout hardening.`
- Runtime/User-Facing Delta: `Monitor Groups card layout/action clarity and Dashboard top-chrome close affordance.`
- Exact Affected Paths: `nexus_visual/monitoring_hud.*`; `desktop/desktop_renderer.py` if Dashboard visibility routing is needed; HUD Dashboard validators if implementation changes behavior.
- Carried Issues: `#125`; `#126`.
- Non-Includes: `#123`; `#124`; `#127`; Dashboard settings cog/settings panel; Overlay/display acceptance; provider telemetry parity; Dev Toolkit/source-owner markers; Workspace Runtime Isolation Stage 2; FAM-007/local AI; AI Product Contract import; raw evidence import/linking; GitHub issue state/comment updates; PR creation; release/tag/artifact work.
- Implementation Admission Status: `Admitted by USER for #125/#126 only and completed in the Workstream implementation pass.`

## Backlog Completion Strategy

Branch Completion Goal: `Complete and validate issues #125 and #126 on this branch, then await USER decision for PR Readiness Stage 1, optional USER visual review, or bounded repair if visual concern remains.`

Known Future-Dependent Blockers: `GitHub issue comments/state updates, raw evidence upload/import/linking, PR creation, release/tag/artifact work, Workspace Runtime Isolation Stage 2, FAM-007/local AI work, AI Product Contract import, and branch expansion beyond #125/#126 all require later explicit USER approval.`

Branch Closure Rule: `Stop after validated runtime implementation, source-truth update, commit, and push; do not begin PR work, GitHub issue closeout/comment updates, release work, raw evidence handling, FAM-007/local AI work, Workspace Runtime Isolation, or any work beyond #125/#126 without later USER approval.`

## Backlog Completion Status

Backlog Completion State: Implemented Complete
Completion Status: Green
Remaining Implementable Work: None
Future-Dependent Blockers: None
Visible User-Facing Proof Required: Yes for Dashboard IA/control confidence - active-client validation has run from the active Branch 2 worktree; USER visual review remains optional/future if USER wants it before PR Readiness.
Visible User-Facing Proof: PASS by active-client H1 proof at dev/logs/fam_006_monitoring_hud_live_validation/20260513_130300_320 after stale Dashboard selector residue was removed and validators were updated to guard the no-Dashboard-dropdown contract.

## Product Definition Plan

Product Vision: `Finish the remaining FAM-006 Dashboard IA/control polish after render/layout hardening by making monitor management clearer and replacing redundant open-state chrome with a useful close affordance.`

User-Facing Goal: `The Dashboard should feel like a deliberate control surface: Monitor Groups should offer obvious Create/Edit flows without wasted space, and the top chrome should give the user a clear way to close the Dashboard instead of restating that it is open.`

USER Vision Questions: `None open for this two-issue branch; USER already selected #125 and #126 as Branch 2 and deferred the settings cog/settings panel.`

Codex Product Interpretation: `Issue #125 is the Monitor Groups card/control-flow cleanup; issue #126 is Dashboard top-chrome affordance cleanup. They are related IA/control concerns and should be implemented together unless runtime inspection proves a separate subsystem risk.`

Codex Implementation Recommendation: `Keep the branch limited to Monitor Groups card layout/actions and top Dashboard close/open-state chrome. Preserve tray behavior, Dashboard render/layout repairs from PR #129, and future settings/Overlay/provider/Dev Toolkit deferrals.`

USER/ChatGPT Review Checkpoint: `Runtime implementation and H1 validation have been performed under USER approval for #125/#126 only; next USER review decides whether to request PR Readiness Stage 1, optional USER visual review, or bounded repair if any visual concern remains.`

Full Feature Element Breakdown: `#125 Monitor Groups dead space removal; #125 Create Monitor dedicated window/flow; #125 Edit Monitor dedicated window/flow; #125 Dashboard dropdown removal; #126 redundant HUD Dashboard Open badge removal; #126 Dashboard close affordance; #126 tray open/close regression preservation.`

Current Branch vs Future Package Boundaries: `Current branch carries #125 and #126 only. Future/deferred means Dashboard settings cog/settings panel, Overlay/display acceptance, provider/external telemetry parity, Dev Toolkit/source-owner markers, Workspace Runtime Isolation Stage 2, FAM-007/local AI, and AI Product Contract import.`

Affected Surfaces: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py` if native close/window routing is needed; HUD Dashboard validators.

Data/Control Model: `Dashboard remains a control/settings surface. Monitor Groups remain organizational settings objects for future Overlay/display behavior. Create/Edit actions should route to dedicated flows; close affordance should control Dashboard visibility without toggling HUD Feature state unless repo truth says otherwise.`

Workstream Implementation Record:

Implementation Status: `Complete for #125 and #126 on feature/fam-006-dashboard-ia-controls-followthrough`

Issue #125 Implementation: `Monitor Groups card layout no longer uses the old Dashboard-home dropdown/edit selector. The card now exposes only Create Monitor and Edit Monitor actions; each action opens a dedicated child-window flow. The create flow creates/selects a new Monitor Group and the edit flow owns group name, enabled state, and polling floor controls. Monitor selection moved to the Edit Monitor child window only.`

Issue #126 Implementation: `The top Dashboard chrome no longer shows the redundant HUD Dashboard Open badge. It now exposes a Close button that hides the Dashboard while preserving the HUD Feature enabled state and tray/open restoration path. Native Dashboard header hit-testing now treats the close affordance as a control so it is not swallowed by native move/resize handling.`

Runtime Files Changed: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py`.

Validator Files Changed: `dev/orin_monitoring_hud_surface_validation.py`; `dev/orin_monitoring_hud_internal_sandbox_validation.py`.

Source-Truth Files Changed: `Docs/branch_records/feature_fam_006_dashboard_ia_controls_followthrough.md`.

Validation Evidence: `Static HUD validator PASS; internal sandbox validator PASS; active-client live validation PASS at dev/logs/fam_006_monitoring_hud_live_validation/20260513_124941_575; H1 active-client live validation PASS at dev/logs/fam_006_monitoring_hud_live_validation/20260513_130300_320; interaction manifest proves Dashboard close affordance, restored Dashboard control hub, Create Monitor child-window route, Edit Monitor child-window route, monitor editor mutation, and final monitor management state.`

H1 Repair Note: `A small #125 hardening defect was found during review: the old Dashboard-home dropdown did not render in the Dashboard DOM, but stale .monitoring-hud__selector-control CSS and validator expectations still preserved legacy monitor-selector styling. The stale CSS was removed and validators now assert that the old Dashboard monitor selector/id/copy are absent from the Dashboard home surface.`

Known Proof Boundary: `This Workstream pass uses Codex active-client proof and repo validators. USER visual review, GitHub issue closeout/comment updates, PR creation, raw evidence upload/import/linking, release work, Workspace Runtime Isolation Stage 2, FAM-007/local AI, AI Product Contract import, and any expansion beyond #125/#126 remain future USER approval checkpoints.`

Branch Reach / Package-Size Review: `Two tightly related Dashboard IA/control issues share product surface, proof path, and user acceptance. The branch is narrow enough for focused review and large enough to avoid unnecessary branch churn.`

Why Branch Is Large Enough: `#125 and #126 together cover the remaining user-confirmed Dashboard IA/control concerns after Branch 1, giving one coherent visual/control review pass.`

Why Not Split Into Tiny Branches: `Splitting would create two very small Dashboard chrome/control branches with overlapping files, duplicate validation, and higher review churn. Split only if runtime inspection shows #125 requires a larger monitor-editor subsystem than this issue branch can safely carry.`

Acceptance Criteria: `Issue #125 and #126 acceptance criteria are recorded below in this branch record and must be preserved during Workstream implementation.`

Validation Proof Requirements: `Static HUD/Dashboard validator, internal sandbox validator, compile validation, governance validation, active-client Dashboard proof, and optional USER visual review after H1 if USER wants added confidence before PR Readiness.`

Screenshot / Live / User Test Summary Proof Requirements: `This implementation provides Codex active-client proof for Monitor Groups card layout, Create/Edit actions, close affordance, and tray/open/close regression. Formal UTS export is not required by this Workstream pass and raw media remains external unless USER later approves.`

Implementation Sequence Proposal: `Inspect current Dashboard markup/control routing; implement #126 top-chrome close affordance and redundant badge removal; implement #125 Monitor Groups layout/action split; update validators; run active-client proof; record validation; stop for PR Readiness or USER visual review decision.`

Planning Blockers: `GitHub Issue Closeout Approval Missing`; `Raw Evidence Import Decision Pending`; `PR Creation Approval Missing`; `PR Readiness User Decision Pending`.

USER Decisions Needed: `Choose PR Readiness Stage 1, optional USER visual review, or bounded repair if any visual concern remains; later approve GitHub issue comments/closeout, PR creation, raw evidence handling, and release work if desired.`

Planning Packet Status: Complete

Planning Revalidation Status: PASS

User Test Summary Strategy: `No UTS is generated, refreshed, imported, or digested by this Workstream implementation pass. Active-client proof is recorded; formal UTS remains a later governed decision if USER requests it.`

Planning Completion Waiver: `Not required - Stage 1 analysis and USER Stage 2 approval completed the planning packet for this two-issue branch.`

## Hardening H1 Validation Result

H1 Result Time: `2026-05-13 Branch 2 isolated C-drive worktree validation`

Workspace Identity: `PASS - shell repo root C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough, branch feature/fam-006-dashboard-ia-controls-followthrough, HEAD c11784f2d7b4e2290cc681a8e31d37d8d2f17962 before the H1 repair commit, upstream origin/feature/fam-006-dashboard-ia-controls-followthrough, origin/main 96ec36e7be751d444eda8dc220bc4a035d44fca1`

GitHub Desktop Binding: `Branch 2 worktree was added to GitHub Desktop with local alias FAM-006; if GitHub Desktop is used for this branch, it should point to C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough on feature/fam-006-dashboard-ia-controls-followthrough.`

H1 Validation Commands:

- `PASS - git diff --check`
- `PASS - python dev\orin_branch_governance_validation.py; 4563 checks`
- `PASS - python dev\orin_release_body_validation.py; latest pre-Beta release v1.7.0-prebeta matches the standard, with historical drift only in older releases`
- `PASS - python -m compileall -q dev desktop Audio main.py`
- `PASS - python dev\orin_monitoring_hud_surface_validation.py`
- `PASS - python dev\orin_monitoring_hud_internal_sandbox_validation.py; manifest C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough\dev\logs\fam_006_monitoring_hud_internal_sandbox\20260513_130557_manifest.json`
- `PASS - powershell -NoProfile -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -ActiveUserFacingClient -ProofSeam "FAM-006 Branch2 H1 IA Controls" -MarkerTimeoutSeconds 240 -NoProgressTimeoutSeconds 240 -FinalClientHoldSeconds 0; proof root C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard IA Controls Followthrough\dev\logs\fam_006_monitoring_hud_live_validation\20260513_130300_320; formal UTS export skipped`

H1 Active-Client Observed Markers: `MONITORING_HUD_DASHBOARD_SURFACE_READY`; `MONITORING_HUD_DASHBOARD_CONTENT_READY`; `MONITORING_HUD_DASHBOARD_MONITOR_GROUP_CLARITY_READY`; `MONITORING_HUD_LIVE_CLIENT_SELF_QA_READY`; `MONITORING_HUD_DASHBOARD_STANDALONE_WINDOW_TRAVEL_READY`; `MONITORING_HUD_DASHBOARD_CLIPPING_BOUNDARY_READY`; `MONITORING_HUD_LIVE_CLIENT_SELF_QA_INTERACTION_READY`.

Issue #125 H1 Result: `PASS by static, sandbox, and active-client proof - Dashboard-home dropdown/id/copy is absent, stale selector CSS was removed, Create Monitor and Edit Monitor are the only Monitor Groups Dashboard-home actions, each action opens a dedicated child-window flow, and the monitor editor mutation/create-edit-enable-polling state passed active-client proof.`

Issue #126 H1 Result: `PASS by static, sandbox, and active-client proof - the redundant top-chrome HUD Dashboard Open badge is removed, the Dashboard Close button is present and click-tested, native hit-testing treats Dashboard controls as controls, and the active-client close action hides only the Dashboard while preserving HUD Feature/tray restoration behavior.`

Regression Check Result: `PASS by active-client proof - Dashboard runtime launched, settled, captured before/after screenshots, exercised close/restore/Create/Edit control paths, and exited with no remaining Nexus/Python runtime process.`

Proof Strength: `Sufficient for PR Readiness Stage 1 source-truth review. USER visual review may still be requested as an additional confidence step before PR creation, and raw screenshot/video upload/import/linking remains a future USER approval checkpoint.`

## Branch Scope

Carried Now:

- #125 Monitor Groups card dead space plus Create/Edit monitor window split.
- #126 Remove redundant HUD Dashboard Open badge and add close affordance.

Held / Not Carried:

- #123 Dashboard initial open flicker - completed by PR #129, pending GitHub closeout.
- #124 scroll content well clipping / scrollbar ownership - completed by PR #129, pending GitHub closeout.
- #127 resize jitter / catch-up lag - completed by PR #129, pending GitHub closeout.
- Dashboard settings cog/settings panel - future/deferred.
- Overlay/display acceptance - future/deferred.
- Provider/external telemetry parity - future/deferred.
- Dev Toolkit/source-owner markers - future/deferred.
- Workspace Runtime Isolation Stage 2 - separate future USER decision.
- FAM-007/local AI and AI Product Contract import - separate future USER decision.

## Acceptance Criteria

Issue #125:

- Monitor Groups card no longer has obvious center dead space.
- Dashboard exposes only `Create Monitor` and `Edit Monitor` for this card flow.
- Dropdown-driven monitor editing is removed from the Dashboard card flow.
- `Create Monitor` opens a dedicated create window/flow.
- `Edit Monitor` opens a dedicated edit window/flow.
- The interaction model remains consistent with existing NCP-style create/manage child-window expectations.
- Dashboard does not render Overlay/display cards or fake telemetry as part of this issue.

Issue #126:

- The redundant `HUD Dashboard Open` badge/state chip is removed from the top Dashboard chrome.
- A clear close affordance exists in the Dashboard top area.
- The close affordance closes/hides the Dashboard without disabling the HUD Feature unless the established product contract says otherwise.
- Existing tray open/close Dashboard behavior remains truthful and usable.
- Dashboard settings cog/settings panel remains deferred unless USER separately approves it.

## Validation Expectations

Workstream implementation validation:

- HUD/Dashboard static validator.
- HUD/Dashboard internal sandbox validator.
- Active-client Dashboard proof for Create/Edit flow and close affordance.
- USER visual review because both issues are user-facing IA/control polish.

## Issue Traceability

Source-truth issue traceability is established here for #125 and #126. GitHub issue comments, state changes, labels, branch assignments, and closeout remain blocked because this Stage 2 approval explicitly excludes GitHub issue edits.

## User Test Summary Strategy

No User Test Summary is generated, refreshed, imported, uploaded, linked, or digested by this Workstream implementation pass. Raw screenshots, videos, and prior UTS exports remain local/external unless USER later explicitly approves a governed evidence-import or linking path. Active-client proof is summary-recorded in this branch record; USER visual review or a later governed Live Validation/UTS phase remains a future decision.

## Later-Phase Expectations

After this H1 pass is committed and pushed, USER may choose PR Readiness Stage 1, optional USER visual review, or bounded repair if any visual concern remains. GitHub issue closeout/comment updates, PR creation, release/tag/artifact work, raw evidence handling, Workspace Runtime Isolation Stage 2, FAM-007/local AI work, AI Product Contract import, and any branch expansion remain separate approval checkpoints.

## Expected Seam Families And Risk Classes

Seam Families: `Dashboard IA/control follow-through`; `Monitor Groups card layout/action split`; `Dashboard top-chrome close affordance`; `Dashboard tray/open/close regression proof`; `source-truth traceability`.

Risk Classes: `Dashboard IA drift`; `child-window flow overreach`; `tray/HUD Feature state regression`; `Branch 1 render/layout regression`; `settings cog scope creep`; `Overlay/display scope bleed`; `raw evidence over-import`; `FAM-007/local AI boundary bleed`.

## Initial Workstream Seam Sequence

Seam 1: `Dashboard IA/control inspection and bounded implementation for #125/#126`.

Goal: `Implement the Monitor Groups Create/Edit split and Dashboard close-affordance cleanup without expanding beyond #125/#126.`

Scope: `nexus_visual/monitoring_hud.*`, Dashboard control routing, relevant desktop Dashboard visibility handling if needed, and HUD validators.`

Non-Includes: `Dashboard settings cog/settings panel, Overlay/display acceptance, provider telemetry parity, Dev Toolkit/source-owner markers, Workspace Runtime Isolation Stage 2, FAM-007/local AI work, AI Product Contract import, PR creation, release work, raw evidence import/linking, and GitHub issue state/comment updates.`

## Active Seam

Active seam: `Hardening H1 for FAM-006 Dashboard IA/control follow-through`.

Active Seam Status: `H1 repair/validation complete when this record and validator/CSS changes are committed and pushed`.

Next active seam: `PR Readiness Stage 1, optional USER visual review, or bounded repair only after USER selects the next phase`.

Single-Seam Workstream Waiver: None
Single-Seam Or Single-Slice Waiver Authority: USER only; Codex cannot infer single-seam or single-slice authority from branch size, branch name, or a narrow implementation pass.
Single-Seam Or Single-Slice Workstream Blocker: Blocker active if only one seam or one slice is planned or visible without explicit USER waiver; this branch is not relying on such a waiver because Branch Readiness admitted two related GitHub issue threads (#125 and #126) into one bounded Dashboard IA/control follow-through branch.
Bounded Seam Default: Bounded means one active seam at a time, not one-seam Workstream authority.

## Seam Continuation Decision

Seam Status: Green
Slice Status: Green
Completion Status: Green
Waiver Status: None
Continue Decision: Stop
Continuation Execution Latch: Inactive - Workstream and Hardening H1 are green; phase-boundary stop is required before USER may admit PR Readiness Stage 1, optional USER visual review, GitHub issue closeout/comment updates, or PR creation.
Stop Basis: Hardening H1 Green
Next Active Seam: PR Readiness Stage 1 / optional USER visual review / bounded repair pending USER decision
Stop Condition: Workstream implementation and H1 validation for issues #125 and #126 are complete and validated as far as current Codex authority allows.
Continuation Action: Stop at phase boundary until USER admits the next phase; do not create a PR, edit GitHub issue state/comments, upload/link raw evidence, release, start Workspace Runtime Isolation, start FAM-007/local AI work, or expand beyond #125/#126 without later USER approval.

## Non-Includes

- GitHub issue creation.
- GitHub issue comments or state changes.
- Closing #123/#124/#127.
- Raw evidence upload, import, linking, or artifact creation.
- PR creation.
- Release/tag/artifact work.
- Workspace Runtime Isolation Stage 2.
- FAM-007/local AI work.
- AI Product Contract import.
- Branch expansion beyond #125/#126.
