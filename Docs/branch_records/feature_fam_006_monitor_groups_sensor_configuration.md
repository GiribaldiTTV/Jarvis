# Branch Authority Record: feature/fam-006-monitor-groups-sensor-configuration

## Branch Authority

- Branch: `feature/fam-006-monitor-groups-sensor-configuration`
- Expected Worktree Root: `C:\Nexus Worktrees\FAM-006`
- Actual Worktree Root: `C:\Nexus Worktrees\FAM-006`
- Upstream / Creation Base: `origin/main`
- Creation Base Commit: `74185039beb0fa0d8b8f06d5cb2c593c94608870`
- Family: `FAM-006`
- Package: `PKG-006 - Monitoring and HUD`
- Branch Class: `implementation`
- Branch Authority State: `Active Hardening H1`
- Bounded State: `Hardening H1 complete - FAM-006 Monitor Groups sensor configuration runtime, directly supporting validators, helper proof, and source truth`
- Runtime-Specific Carrier: `FAM-006 Dashboard Monitor Groups sensor/data-source configuration`
- Source-Truth Authority: `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
- No Cross-Worktree Mutation: `Required - this branch writes only inside C:\Nexus Worktrees\FAM-006`
- GitHub Desktop-bound worktree: `FAM-006` recommended alias after USER adds or refreshes the repository in GitHub Desktop

## Worktree Recovery And Stale Branch Cleanup

FAM-006 Stable Worktree Path: `C:\Nexus Worktrees\FAM-006`

Recovery Reason: `The initial Stage 2 setup created the active Monitor Groups branch in C:\Nexus Worktrees\FAM-006-Monitor-Groups and then removed the retired settings-panel worktree at C:\Nexus Worktrees\FAM-006 during stale-branch cleanup, which caused GitHub Desktop to lose the stable FAM-006 repository path. The active Monitor Groups worktree was moved to the stable FAM-006 path so GitHub Desktop and future helpers have one durable FAM-006 repository target.`

Retired Branch Cleanup Result: `COMPLETE - former feature/fam-006-dashboard-settings-panel worktree C:\Nexus Worktrees\FAM-006 was removed only after merge/equality proof, the remote branch feature/fam-006-dashboard-settings-panel was deleted, and the local stale branch was deleted. The active FAM-006 worktree now points to feature/fam-006-monitor-groups-sensor-configuration.`

## Current Phase

Phase: `Hardening`

Stage: `Hardening H1`

## Phase Status

Branch Authority Marker: `Active Branch`

Workstream implementation is complete and Hardening H1 is green for the USER-approved FAM-006 Monitor Groups sensor-configuration runtime seam. Next Active Seam: `Live Validation Stage 1`. Current Hardening Seam: `Complete`. Current Live Validation Seam: `Pending USER approval`. Current PR Readiness Seam: `Not started`. Current Release Readiness Seam: `Not started`.

## Branch Class

`implementation`

This branch is a FAM-006 runtime carrier. It may carry the bounded source-truth and governance setup needed before implementation, but it must not become a governance-only branch.

## Entry Basis

- FAM-006 Release Readiness for `v1.7.1-prebeta` is closed green.
- Latest public prerelease is `v1.7.1-prebeta`.
- FAM-006 Dashboard work from PR #129, PR #132, and PR #142 is released historical scope.
- FAM-006 issues #123, #124, #125, #126, #127, #137, and #140 are closed / fixed or completed with release traceability preserved.
- Merged main records `No Active Branch / USER decision gate`.
- USER selected this FAM-006-only runtime carrier for Branch Readiness Stage 2.

## Branch Purpose

Implement the FAM-006 runtime carrier for Monitor Groups and sensor configuration. The branch exists so Monitor Groups can become real configurable groups with monitor list management, sensor/data-source assignment, per-sensor settings where the current runtime supports them, and a clear handoff to later HUD Overlay visual customization.

## Branch Objective

Implement the FAM-006 Monitor Groups sensor-configuration runtime flow admitted during Branch Readiness, while preserving Overlay visual display, provider expansion, FAM-007, release, PR, and cleanup work as later USER-gated decisions.

## Target End-State

Hardening H1 ends with a pushed branch containing the Monitor Groups manage/edit runtime flow, list/create/edit/delete behavior, delete confirmation, truthful supported source assignment, per-sensor settings where supported, directly supporting validators, live-helper self-QA proof, and source truth ready for Live Validation Stage 1.

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing, backend/runtime`

Docs-Only Workstream: `No`

Planning-Loop Bypass User Approval: `None`

Planning-Loop Bypass Reason: `None`

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`

Backlog-Split User Approval: `None`

Backlog-Split Reason: `None`

## Product Definition Plan

Product Vision: `Monitor Groups should become the USER-facing place to create and manage logical monitoring groups, choose the available sensor/data sources that belong in those groups, and configure supported per-sensor monitor settings before those groups are displayed elsewhere.`

User-Facing Goal: `Give the USER a clear Monitor Groups management flow with created monitors listed, Create available from the manage/edit window, Edit opening monitor-specific settings, and Delete protected by confirmation.`

USER Vision Questions: `No open questions for Stage 2 setup. Runtime implementation must stop for USER decision if sensor/data-source support is broader than current runtime truth, if Overlay display ownership is required, or if app-wide Theme/Skins scope becomes necessary.`

Codex Product Interpretation: `The Monitor Groups branch should focus on data/sensor membership and monitor management. HUD Overlay settings/customization should own visual display styling, presets, and Overlay-specific presentation. App-wide Theme/Skins remains a separate future candidate.`

Codex Implementation Recommendation: `Implement the Monitor Groups manage/edit flow first, backed by truthful available sensor/data-source capability state and validators. Keep Overlay visual customization deferred until monitor data structures and group membership are stable.`

USER/ChatGPT Review Checkpoint: `Complete - USER approved Hardening H1 for the manage/edit window, delete confirmation, in-window Create action, and sensor assignment together. Live Validation Stage 1 is the next USER review checkpoint.`

Full Feature Element Breakdown: `Monitor group list; created monitor rows; Create button inside manage/edit window; per-monitor Edit action; per-monitor Delete action; delete confirmation prompt; monitor-specific settings panel; sensor/data-source assignment; per-sensor settings where supported; empty/no-sensor truthful state; validation and UTS proof hooks.`

Current Branch vs Future Package Boundaries: `Current branch owns Monitor Groups membership and sensor configuration. Future HUD Overlay customization owns visual display of groups/sensors, colors, borders, text presentation, presets, and Overlay-specific font/display choices. Future NDAI Theme/Skins owns app-wide uniform reskin behavior only after separate USER admission.`

Affected Surfaces: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py`; `desktop/monitoring_hud_controls.py`; FAM-006 HUD validators/helpers as needed by implementation.

Data/Control Model: `Monitor Groups own group membership and monitor-level settings. Sensor/data-source choices must come from current runtime-capable monitor inputs and must not fake unavailable provider, overlay, external telemetry, or hardware data.`

Branch Reach / Package-Size Review: `Large enough for one runtime branch because it spans UI flow, monitor list operations, create/edit/delete behavior, data-source assignment, per-sensor settings boundaries, validation, and source truth.`

Why Branch Is Large Enough: `A useful Monitor Groups implementation requires several linked controls and state paths; splitting Create, Edit, Delete, and sensor assignment into separate branches would create partial UI and stale proof risk.`

Why Not Split Into Tiny Branches: `The USER-facing flow needs list management and sensor assignment to make sense together; tiny branches would produce dead-end windows or fake-ready controls.`

Acceptance Criteria: `Monitor Groups manage/edit flow lists created monitors; Create is available inside the manage/edit window; Edit opens monitor-specific settings; Delete asks for confirmation; available sensor/data-source assignment is truthful; per-sensor settings appear only when supported; existing Dashboard controls regressions are guarded; no Overlay display acceptance or app-wide theme work is implied.`

Validation Proof Requirements: `Static HUD validator, internal sandbox validator, branch governance validation, release body validation, compileall, and later runtime-specific Monitor Groups proof beyond marker presence.`

Screenshot / Live / User Test Summary Proof Requirements: `Runtime implementation should provide user-visible proof of list/create/edit/delete/confirm/sensor assignment behavior, then Hardening and Live Validation should use the real USER-facing launcher/shortcut path and a compact UTS handoff if USER-facing behavior is changed.`

Implementation Sequence Proposal: `Inspect current Create/Edit Monitor windows; design the manage/edit list and confirmation flow; wire truthful sensor/data-source capability state; update validators; run Workstream validation; then request Hardening.`

Planning Blockers: `Live Validation Approval Missing`; `Overlay Acceptance Approval Missing`; `Provider/Model/Memory/Shortcut/Installer Approval Missing`; `External Telemetry Parity Approval Missing`; `AI Product Contract Import Approval Missing`; `PR Creation Approval Missing`.

USER Decisions Needed: `Approve Live Validation Stage 1 next; approve PR creation later; approve merge later; approve release/artifacts/raw evidence/branch cleanup separately; approve any Overlay, FAM-007, provider/model/memory/shortcut/installer, external telemetry, or AI Product work separately.`

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

User Test Summary Strategy: `No UTS is generated during Stage 2 setup. Runtime implementation should prepare a compact step-based UTS only when user-facing behavior is ready for Live Validation.`

Planning Completion Waiver: `Not required`

## Branch Contents Admitted

- Monitor Groups as real configurable groups.
- Created monitor list inside the manage/edit window.
- Create button inside the edit/manage window.
- Per-monitor Edit action that opens that monitor's specific settings.
- Per-monitor Delete action with confirmation before destructive removal.
- Sensor/data-source assignment for available runtime-capable monitor inputs.
- Per-sensor settings where current runtime support exists.
- Source-truth planning for later HUD Overlay visual display and customization.

## Package / Slice Boundaries

- Primary package: `PKG-006 - Monitoring and HUD`.
- Primary branch slice: `SLC-027 - Settings and user controls visibility`, continued as Monitor Groups management controls.
- Supporting branch slice: `SLC-025 - Runtime telemetry source and adapter boundary`, limited to truthful sensor/data-source availability and assignment boundaries.
- Supporting branch slice: `SLC-029 - Validation and live desktop proof`, limited to proving Monitor Groups behavior, regression boundaries, and user-facing proof quality.
- Interface Release Boundary: `Monitoring HUD Dashboard Monitor Groups management flow`.
- Primary Interface Release Surface: `Dashboard Monitor Groups create/edit/manage child-window flow`.
- Interface Bundle User Approval: `Not granted - this branch has one primary Monitor Groups management flow; later HUD Overlay display/customization remains deferred`.

## Admitted Implementation Slice

- Slice ID: `SLC-027`
- Goal: `Implement the FAM-006 Dashboard Monitor Groups management flow for created monitor list, in-window Create, per-monitor Edit, delete confirmation, and supported sensor/data-source assignment.`
- Supporting Slice: `SLC-025` for truthful runtime-capable sensor/data-source boundaries.
- Supporting Validation Slice: `SLC-029` for validator and user-facing proof coverage.
- Runtime/User-Facing Delta: `Monitor Groups manage/edit child-window flow and sensor assignment controls.`
- Exact Affected Paths: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py`; `desktop/monitoring_hud_controls.py`; FAM-006 HUD validators/helpers as needed by implementation.
- Carried Issues: `None newly created by Stage 2 setup`; all released FAM-006 issue threads #123, #124, #125, #126, #127, #137, and #140 are closed / fixed or completed.
- Non-Includes: `HUD Overlay visual display acceptance`; `Overlay customization`; `NDAI-wide Theme/Skins`; `FAM-007`; `provider/model/memory/shortcut/installer work`; `external telemetry parity`; `AI Product Contract import`; `raw evidence upload/import/linking`; `release execution`; `PR creation`; `merge`; `future branch/worktree cleanup after this branch closes`.
- Implementation Admission Status: `USER-approved Workstream implementation complete and Hardening H1 green after this packet validates, commits, and pushes.`

## Backlog Completion Strategy

Branch Completion Goal: `Complete the FAM-006 Monitor Groups sensor-configuration runtime flow through implementation, Hardening, Live Validation, PR Readiness, merge, and later release handling after each phase receives USER approval.`

Known Future-Dependent Blockers: `Runtime implementation approval, PR creation, merge, release execution, artifacts, raw evidence handling, future branch/worktree cleanup after this branch closes, FAM-007 work, provider/model/memory/shortcut/installer work, Overlay acceptance, external telemetry parity, AI Product work, and app-wide Theme/Skins all require later USER approval.`

Branch Closure Rule: `Stop after Hardening H1 validation, commit, and push; continue only after USER approves Live Validation Stage 1 on this branch.`

## Explicit Non-Includes

- HUD Overlay acceptance or visual display implementation.
- Overlay display customization, color/border/text rendering, or presets.
- NDAI-wide Theme/Skins implementation.
- FAM-007 work.
- Provider/model/memory/shortcut/installer work.
- External telemetry parity.
- AI Product Contract import.
- Raw evidence upload, import, or linking.
- Release execution, tags, GitHub Releases, or artifacts.
- PR creation or merge.
- Branch deletion or worktree cleanup.

## Governance Repair

Family-Scoped Branch Readiness Rule: `Added during this branch setup. When Branch Readiness is scoped to a specific feature family or assigned lane, candidate selection must stay inside that family/lane unless USER explicitly approves cross-family routing. Other families may be inspected only for same-file overlap, dependency, conflict, pending-decision, or sequencing context.`

Stable Worktree Path Preservation Gate: `Added during this branch setup after recovery from the FAM-006 GitHub Desktop-bound path removal. Branch Readiness Stage 2 cleanup must record Stable Worktree Path, Replacement Binding Path, and the preservation method before deleting an old branch or removing a worktree. If the stable folder would be removed before the successor branch/worktree is bound there, cleanup blocks on Stable Worktree Path At Risk.`

Repair Classification: `Bounded governance/source-truth repair directly caused by FAM-006 Branch Readiness candidate-selection drift and stable-worktree cleanup drift. The repair belongs on this FAM-006 runtime carrier because it prevents the same branch-readiness and GitHub Desktop-bound worktree mistake before this carrier proceeds to implementation.`

## Branch Readiness Stage 2 Validation Plan

- `git status --short --branch`
- `git fetch origin --prune`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git branch --all`
- `git worktree list`
- `git diff --check origin/main...HEAD`
- `git diff --name-only origin/main...HEAD`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_release_body_validation.py`
- `python -m compileall -q dev desktop Audio main.py`

Runtime implementation should later add or update directly relevant FAM-006 Monitor Groups validators and user-facing proof steps. Static marker proof alone is not enough for runtime behavior closure.

## Workstream Implementation Result

Implementation Status: `Complete - committed and pushed at dcd58d3982c8d8a404f41f97371247fd19463f9b`

Runtime Summary: `Monitor Groups now use a Manage Monitors child-window flow with created monitor rows, an in-window Create Monitor action, per-monitor Edit selection, per-monitor Delete with inline confirmation, selected-monitor settings, supported sensor/data-source assignment, and per-sensor display/warning settings where current Dashboard/runtime support exists. CPU Load, Provider Readiness, and Warning Notifications are truthful assignable sources; CPU thermal, GPU load, and GPU thermal remain provider-required/unavailable rather than fake-ready.`

User-Facing Behavior Changed: `The Dashboard Monitor Groups card now opens Manage Monitors for list/create/edit/delete/source assignment. The existing Create Monitor action still creates a monitor group, and Manage Monitors lets the USER add more monitors without returning to the Dashboard. Delete requires confirmation before removing a group. Source assignment is explicit and labels provider-required sensors as unavailable.`

Validator Support Added: `Static HUD validator and internal sandbox validator now assert the manage-list-create-edit-delete-sensor-assignment markers, UI controls, inline delete confirmation, supported sensor assignment, per-sensor settings, and updated runtime contract. Desktop renderer proof state now includes sensor assignments/settings in monitor-management signatures.`

Package / Slice Adherence: `Primary package remains PKG-006. Primary slice remains SLC-027 for Monitor Groups controls. Supporting SLC-025 is limited to truthful sensor/source availability and does not add provider expansion. Supporting SLC-029 is limited to validators/proof hooks.`

Implementation Non-Includes Preserved: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, artifacts, raw evidence handling, and future branch/worktree cleanup remain excluded.`

Workstream Validation Evidence: `python dev\orin_monitoring_hud_surface_validation.py PASS; python dev\orin_monitoring_hud_internal_sandbox_validation.py PASS; node --check nexus_visual\monitoring_hud.js PASS; python -m compileall -q dev desktop Audio main.py PASS before source-truth final validation.`

## Hardening H1 Result

Hardening Status: `Green - bounded H1 validator/proof repair applied`

Hardening Summary: `Hardening H1 found no product behavior failure in the Monitor Groups implementation, but it did find a proof-strength gap: the live-helper self-QA proved create/edit/sensor settings but did not dynamically prove in-window Create plus Delete cancel/confirm. The bounded H1 repair extends desktop renderer self-QA and supporting validators so H1 proves in-window Create, delete confirmation open, cancel preserving the monitor, confirm removing the monitor, confirmation closure, supported sensor assignment, per-sensor settings, Dashboard Close, Settings, Warning, and Dashboard/Core/Overlay regression boundaries.`

Hardening Proof Path: `dev/logs/fam_006_monitoring_hud_live_validation/20260514_211312_366`

Hardening Validation Evidence: `powershell -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -RunInteractionSelfQA -ProofSeam "FAM-006 Monitor Groups Hardening H1" PASS; UTS export skipped because UTS belongs to Live Validation Stage 1 only.`

Hardening Repair Files: `desktop/desktop_renderer.py`; `dev/orin_monitoring_hud_surface_validation.py`; `dev/orin_monitoring_hud_internal_sandbox_validation.py`; `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`; `Docs/feature_backlog.md`; `Docs/prebeta_roadmap.md`.

## Expected Seam Families And Risk Classes

Seam Families: `Monitor Groups management UI`; `Create/Edit/Delete monitor flow`; `sensor/data-source assignment`; `per-sensor settings truth`; `Dashboard regression protection`; `validator and proof hardening`; `source-truth governance`.

Risk Classes: `dead-end Monitor Groups controls`; `fake sensor/data-source availability`; `delete without confirmation`; `Create/Edit window flow regression`; `Overlay/display scope creep`; `app-wide Theme/Skins scope creep`; `FAM-007/provider/model bleed`; `marker-only proof`.

## User Test Summary Strategy

Stage 2 setup does not generate a UTS. Runtime implementation should prepare a compact, step-based UTS after Workstream and Hardening prove the feature enough for USER-facing Live Validation.

## Later-Phase Expectations

- Hardening H1 is complete and green for list, Create/Edit/Delete, delete confirmation, sensor assignment truth, and Dashboard regressions.
- Live Validation follows Hardening H1 and must use the real USER-facing launcher/shortcut path unless USER grants a waiver.
- PR Readiness, PR creation, merge, release execution, artifacts, raw evidence handling, branch cleanup, Overlay acceptance, FAM-007 work, provider/model/memory/shortcut/installer work, external telemetry parity, and AI Product work remain separate USER decisions.

## Initial Workstream Seam Sequence

Seam 1: `Monitor Groups management flow and sensor-configuration design/implementation`

Goal: `Build the Monitor Groups manage/edit flow so users can create, edit, delete, and assign available sensor/data-source inputs to monitors without leaving the manage/edit context.`

Scope: `Dashboard Monitor Groups management UI, child-window flow, list state, Create/Edit/Delete controls, delete confirmation, sensor/data-source assignment truth, per-sensor settings where supported, and validators.`

Non-Includes: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, artifacts, raw evidence handling, and future branch/worktree cleanup after this branch closes.`

## Active Seam

Active seam: `Hardening H1 for FAM-006 Monitor Groups sensor configuration`

Active Seam Status: `Hardening H1 green after bounded proof repair: Monitor Groups manage/edit flow, list rows, in-window Create, per-monitor Edit/Delete, delete confirmation open/cancel/confirm, supported source assignment, per-sensor settings, validators, renderer proof hooks, and source truth are pressure-tested.`

Next active seam: `Live Validation Stage 1`

## Backlog Completion Status

Backlog Completion State: `Implemented Complete Except Future Dependency`

Remaining Implementable Work: `None`

Future-Dependent Blockers: `Live Validation; PR Readiness; PR creation; merge; release execution; artifacts; raw evidence handling; future branch/worktree cleanup; FAM-007 work; provider/model/memory/shortcut/installer work; Overlay acceptance; external telemetry parity; AI Product work`

Completion Status: `Green`

## Seam Continuation Decision

Seam Status: `Green`

Slice Status: `Green`

Completion Status: `Green`

Waiver Status: `None`

Continue Decision: `Stop`

Continuation Execution Latch: `Closed until USER approves Live Validation Stage 1`

Stop Basis: `Workstream Green`

Next Active Seam: `Live Validation Stage 1`

Stop Condition: `Hardening H1 is green; Live Validation Stage 1 requires explicit USER approval`

Continuation Action: `Stop at phase boundary until USER admits Live Validation Stage 1`

Single-Seam Workstream Waiver: `None`

Single-Seam Or Single-Slice Waiver Authority: `USER only; Codex cannot infer single-seam or single-slice Workstream authority`

Single-Seam Or Single-Slice Workstream Blocker: `One seam or one slice visible in the Workstream plan is a blocker unless a USER waiver is recorded`

Bounded Seam Default: `Bounded means one active seam at a time, not one-seam Workstream authority; same-branch continuation is required until Workstream Completion Status is Green`

## Blockers

None active inside Hardening H1. Live Validation, PR creation, merge, release execution, raw evidence handling, FAM-007 scope, provider/model/memory/shortcut/installer work, Overlay acceptance, external telemetry parity, and AI Product work remain pending USER decisions for later phases.

## Exit Criteria

- Monitor Groups manage/edit flow is implemented.
- Created monitor list, in-window Create, per-monitor Edit, per-monitor Delete with confirmation, source assignment, and per-sensor settings are present.
- Existing Dashboard settings, close, warning notifications, tray-owned HUD control, resize/scroll/source-truth boundaries remain preserved.
- FAM-006 v1.7.1-prebeta release closure remains green.
- FAM-006 released issue closeout posture is preserved.
- Directly supporting validators pass.
- Required validation passes.
- Hardening H1 repair commit is pushed.

## Rollback Target

`Workstream`

Rollback is the unmerged Workstream implementation on this branch only if USER later decides to abandon this carrier before PR/merge. Do not delete or mutate other FAM-006, FAM-007, Governance, or main worktrees as part of rollback.

## Next Legal Phase

`Live Validation`

USER decision for FAM-006 Monitor Groups Live Validation Stage 1 on `feature/fam-006-monitor-groups-sensor-configuration`.

## Next Legal Phase Digest

Current Phase: `Hardening`

Next Legal Phase: `Live Validation`

Why This Phase Is Next: `Hardening H1 has pressure-tested the FAM-006 Monitor Groups manage/edit runtime flow, truthful sensor/data-source assignment, per-sensor settings, delete confirmation/cancel/confirm behavior, directly supporting validators, and source truth. Live Validation Stage 1 is the next legal phase to prove the user-facing path before PR Readiness.`

Approval Required: `USER approval for FAM-006 Monitor Groups Live Validation Stage 1.`

Exact USER Approval Text: `Approve Live Validation Stage 1 for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006. Scope is FAM-006 Monitor Groups sensor configuration only: validate the real USER-facing shortcut/client path, prove Manage Monitors list/create/edit/delete confirmation and cancel, supported sensor/data-source assignment, per-sensor settings, Dashboard settings/close/warning regression boundaries, generate or refresh the compact User Test Summary handoff if required, digest returned USER results or explicit waiver if provided, run validation, commit, and push any bounded Live Validation source-truth repair.`

Allowed Scope: `Live Validation Stage 1 proof and bounded same-seam repair for Dashboard Monitor Groups management UI, child-window flow, list state, Create/Edit/Delete controls, delete confirmation, supported sensor/data-source assignment truth, per-sensor settings where supported, compact UTS handoff, and directly supporting FAM-006 HUD validators/helpers/source truth.`

Explicit Exclusions: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, tags, GitHub Releases, artifacts, raw evidence upload/import/linking, and future branch/worktree cleanup after this branch closes.`

Validation Required: `git status --short --branch; git fetch origin --prune; git rev-parse HEAD; git rev-parse origin/main; git worktree list; git diff --check; git diff --check origin/main...HEAD; python dev\orin_monitoring_hud_surface_validation.py; python dev\orin_monitoring_hud_internal_sandbox_validation.py; python dev\orin_branch_governance_validation.py; python dev\orin_release_body_validation.py; python -m compileall -q dev desktop Audio main.py.`

Stop Conditions: `Stop if branch/worktree identity mismatches C:\Nexus Worktrees\FAM-006 / feature/fam-006-monitor-groups-sensor-configuration, origin/main movement creates required reconciliation, Live Validation requires excluded Overlay/FAM-007/provider/model/installer/AI Product/release/PR/raw-evidence scope, USER-facing proof or UTS cannot be completed without waiver, or another USER decision is required.`
