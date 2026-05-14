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
- Branch Authority State: `Active Branch Readiness Stage 2 setup`
- Bounded State: `Branch Readiness Stage 2 setup only - source-truth authority, package/slice boundaries, validation planning, and bounded governance repair`
- Runtime-Specific Carrier: `FAM-006 Dashboard Monitor Groups sensor/data-source configuration`
- Source-Truth Authority: `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
- No Cross-Worktree Mutation: `Required - this branch writes only inside C:\Nexus Worktrees\FAM-006`
- GitHub Desktop-bound worktree: `FAM-006` recommended alias after USER adds or refreshes the repository in GitHub Desktop

## Worktree Recovery And Stale Branch Cleanup

FAM-006 Stable Worktree Path: `C:\Nexus Worktrees\FAM-006`

Recovery Reason: `The initial Stage 2 setup created the active Monitor Groups branch in C:\Nexus Worktrees\FAM-006-Monitor-Groups and then removed the retired settings-panel worktree at C:\Nexus Worktrees\FAM-006 during stale-branch cleanup, which caused GitHub Desktop to lose the stable FAM-006 repository path. The active Monitor Groups worktree was moved to the stable FAM-006 path so GitHub Desktop and future helpers have one durable FAM-006 repository target.`

Retired Branch Cleanup Result: `COMPLETE - former feature/fam-006-dashboard-settings-panel worktree C:\Nexus Worktrees\FAM-006 was removed only after merge/equality proof, the remote branch feature/fam-006-dashboard-settings-panel was deleted, and the local stale branch was deleted. The active FAM-006 worktree now points to feature/fam-006-monitor-groups-sensor-configuration.`

## Current Phase

Phase: `Branch Readiness`

Stage: `Branch Readiness Stage 2 - Execution Gate`

## Phase Status

Branch Authority Marker: `Active Branch`

Stage 2 setup active. Runtime implementation has not started and requires a later USER decision after this setup validates, commits, and pushes.

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

Prepare the next FAM-006 runtime implementation carrier for Monitor Groups and sensor configuration. The branch exists so Monitor Groups can become real configurable groups with monitor list management, sensor/data-source assignment, per-sensor settings where the current runtime supports them, and a clear handoff to later HUD Overlay visual customization.

## Branch Objective

Admit the FAM-006 Monitor Groups sensor-configuration carrier as the next runtime-focused branch after `v1.7.1-prebeta` release closure, while keeping implementation blocked until USER explicitly approves the Workstream phase.

## Target End-State

Branch Readiness Stage 2 ends with a pushed branch that has source-truth authority, package/slice boundaries, validation planning, and the family-scoped Branch Readiness governance repair in place. The branch should then be ready for a USER decision on runtime implementation.

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

USER/ChatGPT Review Checkpoint: `Review this Stage 2 setup packet before approving runtime implementation. Implementation approval should name whether the first Workstream may build the manage/edit window, delete confirmation, in-window Create action, and sensor assignment together.`

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

Planning Blockers: `Runtime Implementation Approval Missing`; `Overlay Acceptance Approval Missing`; `Provider/Model/Memory/Shortcut/Installer Approval Missing`; `External Telemetry Parity Approval Missing`; `AI Product Contract Import Approval Missing`; `PR Creation Approval Missing`.

USER Decisions Needed: `Approve runtime implementation after Stage 2 setup; approve PR creation later; approve merge later; approve release/artifacts/raw evidence/branch cleanup separately; approve any Overlay, FAM-007, provider/model/memory/shortcut/installer, external telemetry, or AI Product work separately.`

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
- Implementation Admission Status: `Pending USER approval after Branch Readiness Stage 2 setup validates and pushes.`

## Backlog Completion Strategy

Branch Completion Goal: `Complete the FAM-006 Monitor Groups sensor-configuration runtime flow through implementation, Hardening, Live Validation, PR Readiness, merge, and later release handling after each phase receives USER approval.`

Known Future-Dependent Blockers: `Runtime implementation approval, PR creation, merge, release execution, artifacts, raw evidence handling, future branch/worktree cleanup after this branch closes, FAM-007 work, provider/model/memory/shortcut/installer work, Overlay acceptance, external telemetry parity, AI Product work, and app-wide Theme/Skins all require later USER approval.`

Branch Closure Rule: `Stop after Stage 2 setup validation, commit, and push; continue only after USER approves runtime implementation on this branch.`

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

Repair Classification: `Bounded governance/source-truth repair directly caused by FAM-006 Branch Readiness candidate-selection drift. The repair belongs on this FAM-006 runtime carrier because it prevents the same branch-readiness mistake before this carrier proceeds to implementation.`

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

## Expected Seam Families And Risk Classes

Seam Families: `Monitor Groups management UI`; `Create/Edit/Delete monitor flow`; `sensor/data-source assignment`; `per-sensor settings truth`; `Dashboard regression protection`; `validator and proof hardening`; `source-truth governance`.

Risk Classes: `dead-end Monitor Groups controls`; `fake sensor/data-source availability`; `delete without confirmation`; `Create/Edit window flow regression`; `Overlay/display scope creep`; `app-wide Theme/Skins scope creep`; `FAM-007/provider/model bleed`; `marker-only proof`.

## User Test Summary Strategy

Stage 2 setup does not generate a UTS. Runtime implementation should prepare a compact, step-based UTS after Workstream and Hardening prove the feature enough for USER-facing Live Validation.

## Later-Phase Expectations

- Workstream implementation requires separate USER approval.
- Hardening follows implementation and must pressure-test the list, Create/Edit/Delete, delete confirmation, sensor assignment truth, and Dashboard regressions.
- Live Validation follows Hardening and must use the real USER-facing launcher/shortcut path unless USER grants a waiver.
- PR Readiness, PR creation, merge, release execution, artifacts, raw evidence handling, branch cleanup, Overlay acceptance, FAM-007 work, provider/model/memory/shortcut/installer work, external telemetry parity, and AI Product work remain separate USER decisions.

## Initial Workstream Seam Sequence

Seam 1: `Monitor Groups management flow and sensor-configuration design/implementation`

Goal: `Build the Monitor Groups manage/edit flow so users can create, edit, delete, and assign available sensor/data-source inputs to monitors without leaving the manage/edit context.`

Scope: `Dashboard Monitor Groups management UI, child-window flow, list state, Create/Edit/Delete controls, delete confirmation, sensor/data-source assignment truth, per-sensor settings where supported, and validators.`

Non-Includes: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, artifacts, raw evidence handling, and future branch/worktree cleanup after this branch closes.`

## Active Seam

Active seam: `Branch Readiness Stage 2 setup for FAM-006 Monitor Groups sensor configuration`

Active Seam Status: `Source-truth authority, package/slice boundaries, validation planning, and family-scoped Branch Readiness governance repair are being established before runtime implementation.`

## Blockers

- Runtime Implementation Approval Missing
- PR Creation Approval Missing
- Merge Approval Missing
- Release Execution Approval Missing
- Raw Evidence Handling Approval Missing
- FAM-007 Scope Approval Missing
- Provider/Model/Memory/Shortcut/Installer Approval Missing
- Overlay Acceptance Approval Missing
- External Telemetry Parity Approval Missing
- AI Product Contract Import Approval Missing

## Exit Criteria

- Branch created from current `origin/main`.
- Branch authority record added and indexed.
- Backlog and roadmap identify this branch as the active FAM-006 runtime carrier.
- FAM-006 v1.7.1-prebeta release closure remains green.
- FAM-006 released issue closeout posture is preserved.
- Family-scoped Branch Readiness governance repair is recorded.
- Required validation passes.
- Stage 2 setup commit is pushed.

## Rollback Target

`Branch Readiness`

Delete the unmerged branch/worktree setup only if USER later decides to abandon this carrier and no runtime implementation has begun. Do not delete other FAM-006, FAM-007, Governance, or main worktrees as part of rollback.

## Next Legal Phase

`Workstream`

USER decision for FAM-006 Monitor Groups runtime implementation on `feature/fam-006-monitor-groups-sensor-configuration`.
