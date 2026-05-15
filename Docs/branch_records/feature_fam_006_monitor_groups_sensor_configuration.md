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
- Branch Authority State: `Active Hardening H1 complete / refreshed Live Validation recheck pending`
- Bounded State: `Returned USER UTS FAIL repair implementation is hardened with bounded fixture-truth repair; refreshed Live Validation / UTS recheck remains pending`
- Runtime-Specific Carrier: `FAM-006 Dashboard Monitor Groups sensor/data-source configuration`
- Source-Truth Authority: `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
- No Cross-Worktree Mutation: `Required - this branch writes only inside C:\Nexus Worktrees\FAM-006`
- GitHub Desktop-bound worktree: `FAM-006` recommended alias after USER adds or refreshes the repository in GitHub Desktop

## Worktree Recovery And Stale Branch Cleanup

FAM-006 Stable Worktree Path: `C:\Nexus Worktrees\FAM-006`

Recovery Reason: `The initial Stage 2 setup created the active Monitor Groups branch in C:\Nexus Worktrees\FAM-006-Monitor-Groups and then removed the retired settings-panel worktree at C:\Nexus Worktrees\FAM-006 during stale-branch cleanup, which caused GitHub Desktop to lose the stable FAM-006 repository path. The active Monitor Groups worktree was moved to the stable FAM-006 path so GitHub Desktop and future helpers have one durable FAM-006 repository target.`

Retired Branch Cleanup Result: `COMPLETE - former feature/fam-006-dashboard-settings-panel worktree C:\Nexus Worktrees\FAM-006 was removed only after merge/equality proof, the remote branch feature/fam-006-dashboard-settings-panel was deleted, and the local stale branch was deleted. The active FAM-006 worktree now points to feature/fam-006-monitor-groups-sensor-configuration.`

## Current Phase

Phase: `Live Validation`

Stage: `Live Validation Stage 1 refreshed UTS recheck pending after Hardening H1`

## Phase Status

Branch Authority Marker: `Active Branch`

Workstream implementation is complete and Hardening H1 is green for the USER-approved FAM-006 Monitor Groups sensor-configuration runtime seam. Live Validation Stage 1 has USER approval and has real red-shortcut human-client proof PASS plus active-client UTS handoff proof PASS, but the returned USER UTS result is FAIL until the repaired H1 path is refreshed and returned/digested. Current-main reconciliation is complete at `84b3780080e0473f1d8ada61c820951f81b9072d` with `origin/main` `9b61858130dac45ab088c1b7f973503c132cce6f` as an ancestor of the branch. Current Hardening Seam: `Returned UTS FAIL repair implementation hardened with fixture-truth and Sensor Library filter proof repair`. Current PR Readiness Seam: `Blocked until refreshed Live Validation / UTS recheck is PASS or explicitly waived with reason and digested`. Current Release Readiness Seam: `Not started`.

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

Live Validation Stage 1 ends only after returned USER UTS failures are repaired and revalidated, or explicitly WAIVED with reason, and that result is digested into source truth. The current branch contains the Monitor Groups manage/edit runtime flow, list/create/edit/delete behavior, delete confirmation, truthful supported source assignment, per-sensor settings where supported, directly supporting validators, red-shortcut human-client proof, active-client proof, and a refreshed compact USER UTS handoff.

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

Project-Wide Vision Alignment: `Nexus Desktop AI should keep monitoring configuration truthful, local-first, and inspectable before expanding overlay display, recording, provider, or AI Product surfaces. This branch strengthens the monitoring configuration layer without implying unsupported provider telemetry, overlay acceptance, recording runtime, or external export behavior.`

Branch-Specific Vision Alignment: `The Monitor Groups branch owns the USER-facing management path for configured monitors, monitor groups, supported source assignment, and direct proof of scalable management UI. It does not own overlay visibility, recording selection, provider expansion, external telemetry parity, or app-wide theming.`

User-Facing Goal: `Give the USER a clear Monitor Groups management flow with created monitors listed, Create available from the manage/edit window, Edit opening monitor-specific settings, and Delete protected by confirmation.`

USER Vision Questions: `No open questions for Stage 2 setup. Runtime implementation must stop for USER decision if sensor/data-source support is broader than current runtime truth, if Overlay display ownership is required, or if app-wide Theme/Skins scope becomes necessary.`

Codex Product Interpretation: `The Monitor Groups branch should focus on data/sensor membership and monitor management. Sensor Library is the searchable/filterable source-discovery model. Monitor Groups organize and configure monitors; Overlay Profiles own selected monitor visibility and layout on the Overlay; Recording Profiles own selected monitor/sensor logging. HUD Overlay settings/customization should own visual display styling, presets, and Overlay-specific presentation. App-wide Theme/Skins remains a separate future candidate.`

Codex Implementation Recommendation: `Implement the Monitor Groups manage/edit flow first, backed by truthful available sensor/data-source capability state and validators. Keep Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, provider expansion, and Overlay visual customization deferred until monitor data structures, source discovery, and group membership are stable and separately admitted.`

Codex Additional Recommendations: `Codex recommends keeping the current option of a scalable split management surface instead of returning to a long single-pane list, and also recommends proof that combines geometry, during-drag screenshots, and pixel-signature changes. An alternative is a virtualized table later, but that should wait until bulk creation, recommended packs, or historical sensor data are admitted.`

USER/ChatGPT Review Checkpoint: `In progress - USER returned compact UTS FAIL for resize/move smoothness and Manage Monitors scalability/scrollbar findings. Repair planning remains active before PR Readiness.`

USER Critique Loop: `USER reported that Steps 1-8 passed, Step 9 still failed on resize/move smoothness with worst shrink freeze/catch-up behavior, and Step 10 failed because Manage Monitors had native-looking scrollbars and weak large-inventory scalability. This Stage 2 setup treats that critique as the active repair authority.`

USER Decision Ledger: `USER approved Branch Readiness Stage 2 repair setup only. Runtime repair implementation, GitHub issue #127 mutation, PR creation, merge, release execution, raw evidence handling, Overlay Profile runtime, Recording Profile runtime, provider expansion, FAM-007 work, AI Product work, and NDAI-wide Theme/Skins remain pending USER decisions.`

Full Feature Element Breakdown: `Monitor group list; created monitor rows; Create button inside manage/edit window; per-monitor Edit action; per-monitor Delete action; delete confirmation prompt; monitor-specific settings panel; searchable/filterable Sensor Library source discovery planning; sensor/data-source assignment; per-sensor settings where supported; empty/no-sensor truthful state; Overlay Profile planning; Recording Profile planning; validation and UTS proof hooks.`

System Concept Model: `Sensor Library exposes available or planned data sources; monitors are configured tracked items; Monitor Groups organize monitor collections; Overlay Profiles later choose visible monitors and layout; Recording Profiles later choose monitors or sensors to log. This branch repairs the Monitor Groups management surface and proof gates while preserving other concepts as future-gated boundaries.`

Entity / Profile Model: `Sensor Library = all available or planned data sources; Monitor = one configured tracked item; Monitor Group = organization/configuration collection; Overlay Profile = selected monitors plus layout visible on overlay; Recording Profile = selected monitors or sensors logged to file. A monitor may later be enabled, visible, recorded, warning-enabled, or hidden independently.`

User Workflow Model: `USER opens Dashboard, opens Monitor Groups / Manage Monitors, scans or filters created monitors and source choices, creates a monitor, edits monitor-specific settings, assigns a supported source, reviews provider-required/deferred sources truthfully, and deletes only after a confirmation prompt. The returned repair also requires the Dashboard to remain visually smooth while moving or resizing.`

Scale / Data Volume Model: `Manage Monitors must scale to hundreds of monitors and thousands of data sources using scannable panes, search/filter controls, Nexus-styled scrollbars, and fixture validation. The UI should not require all monitors or all source entries to render visibly at once to remain usable.`

Configuration And State Model: `Monitor configuration includes group membership, enabled state, polling interval, supported source assignment, and supported per-sensor display/warning settings. Overlay visibility, recording inclusion, recording output, export/share, provider expansion, and app-wide theme state remain separate future models.`

Planning Adequacy Review: `The plan is not shallow because it covers the end-to-end Monitor Groups configuration system: Dashboard entry, Manage Monitors list/navigation, selected-monitor settings, Sensor Library discovery, supported/deferred source states, large inventory scale, delete confirmation safety, validation proof, compact UTS return, and future Overlay/Recording/Profile boundaries.`

Rejected Shallow Plan: `Rejected shallow plan: only restyle the existing scrollbar and add a geometry-only resize validator. That simple/minimal plan was insufficient because the USER reported perceived freeze during active shrink/grow drag and weak large-inventory management, so the repair must address live visual repaint proof and scalable source discovery.`

Alternatives And Tradeoffs Reviewed: `Alternative option 1 was a full virtualized data-grid/tree, which improves huge-list performance but risks oversized implementation and bulk-management scope drift. Alternative option 2 was a light split pane with capped visible source results and large fixtures, which is lower risk and fits this branch. Tradeoff accepted: keep advanced bulk creation, recommended packs, alert rules, and history outside this repair.`

Whole-System Interaction Map: `Dashboard card -> Manage Monitors child window; left monitor list/search -> selected monitor detail pane; Sensor Library search/filter -> source assignment checkboxes -> per-sensor settings; delete action -> confirmation/cancel/confirm flow; resize/move frame sync -> human-client proof -> compact UTS; Monitor Group configuration stays separate from Overlay Profile visibility and Recording Profile logging.`

Minimum Viable vs Full System Boundary: `Minimum viable current-branch scope is a usable Monitor Groups management flow plus resize/move smoothness repair and proof. Full future system scope includes Overlay Profile runtime UI, Recording Profile runtime, local recording output, tray recording controls, export/share, provider expansion, bulk creation, recommended packs, alert/rule engine, historical sensor data, and NDAI-wide Theme/Skins.`

Open Questions / USER Decision Points: `USER decisions remain pending for Hardening H1, refreshed Live Validation/UTS return or waiver, GitHub issue #127 mutation, PR creation, merge, release work, branch/worktree cleanup, recording runtime, Overlay Profile runtime, tray recording controls, provider/model/shortcut/installer work, Overlay acceptance, external telemetry, FAM-007, AI Product, and NDAI-wide Theme/Skins.`

Current Branch vs Future Package Boundaries: `Current branch owns Monitor Groups membership, sensor configuration, searchable/filterable Sensor Library planning, and source-truth admission for profile-model boundaries. Monitor Groups remain organization/configuration only and do not own overlay visibility or recording selection. Future Overlay Profile runtime owns selected monitors plus Overlay layout/visibility. Future Recording Profile runtime owns selected monitors or sensors logged to local files. Future HUD Overlay customization owns visual display of groups/sensors, colors, borders, text presentation, presets, and Overlay-specific font/display choices. Future NDAI Theme/Skins owns app-wide uniform reskin behavior only after separate USER admission.`

Affected Surfaces: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py`; `desktop/monitoring_hud_controls.py`; FAM-006 HUD validators/helpers as needed by implementation.

Data/Control Model: `Sensor Library equals all available or planned data sources; Monitor equals one configured tracked item; Monitor Group equals an organized monitor collection for organization/configuration; Overlay Profile equals selected monitors plus layout visible on the Overlay; Recording Profile equals selected monitors or sensors logged to file. Sensor/data-source choices must come from current runtime-capable monitor inputs and must not fake unavailable provider, overlay, external telemetry, recording, export/share, or hardware data.`

Branch Reach / Package-Size Review: `Large enough for one runtime branch because it spans UI flow, monitor list operations, create/edit/delete behavior, data-source assignment, per-sensor settings boundaries, validation, and source truth.`

Why Branch Is Large Enough: `A useful Monitor Groups implementation requires several linked controls and state paths; splitting Create, Edit, Delete, and sensor assignment into separate branches would create partial UI and stale proof risk.`

Why Not Split Into Tiny Branches: `The USER-facing flow needs list management and sensor assignment to make sense together; tiny branches would produce dead-end windows or fake-ready controls.`

Acceptance Criteria: `Monitor Groups manage/edit flow lists created monitors; Create is available inside the manage/edit window; Edit opens monitor-specific settings; Delete asks for confirmation; available sensor/data-source assignment is truthful; per-sensor settings appear only when supported; source truth distinguishes Sensor Library, Monitor, Monitor Group, Overlay Profile, and Recording Profile; existing Dashboard controls regressions are guarded; no Overlay Profile runtime, Recording Profile runtime, Overlay display acceptance, tray recording controls, export/share behavior, or app-wide theme work is implied.`

Expected User-Facing Outcomes: `After repair implementation and revalidation, the USER should see smoother Dashboard movement and grow/shrink resize behavior during drag, plus a Manage Monitors window that feels Nexus-styled and usable with large monitor/source inventories. PR Readiness should remain unavailable until those outcomes are proven or explicitly waived.`

Validation Proof Requirements: `Static HUD validator, internal sandbox validator, branch governance validation, release body validation, compileall, and later runtime-specific Monitor Groups proof beyond marker presence. Source-truth validation must distinguish Monitor Group, Overlay Profile, and Recording Profile concepts, and future validator planning must prove a monitor can be enabled, visible, recorded, warning-enabled, or hidden independently without requiring runtime recording controls before separate USER admission.`

Screenshot / Live / User Test Summary Proof Requirements: `Runtime implementation should provide user-visible proof of list/create/edit/delete/confirm/sensor assignment behavior, then Hardening and Live Validation should use the real USER-facing launcher/shortcut path and a compact UTS handoff if USER-facing behavior is changed.`

Implementation Sequence Proposal: `Inspect current Create/Edit Monitor windows; design the manage/edit list and confirmation flow; wire truthful sensor/data-source capability state; update validators; run Workstream validation; then request Hardening.`

Deferred Ideas / Future Package Ledger: `Overlay Profile runtime, Recording Profile runtime, tray recording controls, local recording output, export/share actions, provider expansion, Overlay acceptance, external telemetry parity, FAM-007 runtime work, AI Product work, and NDAI-wide Theme/Skins are deferred future packages or separately gated work. They must not be implemented by this repair setup.`

Planning Blockers: `Returned USER UTS Results FAIL`; `Resize/Move Render Freeze Repair Pending`; `Manage Monitors Scalability Repair Pending`; `Overlay Profile Runtime Approval Missing`; `Recording Profile Runtime Approval Missing`; `Tray Recording Controls Approval Missing`; `Export/Share Runtime Approval Missing`; `Overlay Acceptance Approval Missing`; `Provider/Model/Memory/Shortcut/Installer Approval Missing`; `External Telemetry Parity Approval Missing`; `AI Product Contract Import Approval Missing`; `PR Creation Approval Missing`.

USER Decisions Needed: `Approve runtime repair implementation for returned UTS FAIL findings; approve refreshed UTS return or explicit waiver with reason after repair; approve PR creation later; approve merge later; approve release/artifacts/raw evidence/branch cleanup separately; approve any Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, Overlay acceptance, FAM-007, provider/model/memory/shortcut/installer, external telemetry, or AI Product work separately.`

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

Planning Completion Waiver: `Not required - required product/system/profile/workflow/scale/state planning fields are recorded for this branch-local Stage 2 repair setup.`

User Test Summary Strategy: `No UTS is generated during Stage 2 setup. Runtime implementation should prepare a compact step-based UTS only when user-facing behavior is ready for Live Validation. The current compact UTS returned FAIL, so PR Readiness remains blocked until the resize/render-freeze and Manage Monitors scalability findings are repaired and revalidated or explicitly waived.`

## Returned UTS FAIL Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2`

Current-Main Reconciliation Confirmation: `PASS - current-main reconciliation is complete, clean, pushed, validation-green, and origin/main 09b44c1923c9e1b032f08a2c19ae0527ed185047 is an ancestor of the FAM-006 branch.`

Returned UTS Scope Admitted: `Returned UTS Steps 1-8 passed; Step 9 failed Dashboard resize/move smoothness, especially shrink behavior where rendering appears frozen until resize completes; Step 10 failed Manage Monitors design/scalability because the scrollbar appears native Windows styled and the flow does not scale to hundreds of monitors and thousands of data sources.`

Resize/Move Repair Scope: `Dashboard resize/move live render smoothness; shrink and grow resize visual continuity; during-drag frame, pixel-signature, or video-style proof before mouse release; proof must show the Dashboard renders during drag rather than only after mouse release.`

Manage Monitors Repair Scope: `Manage Monitors scalable split layout; Nexus-styled scrollbars in child windows, monitor list, detail pane, sensor tree, sensor result list, and sensor preview/details pane; large-monitor and large-source fixtures for hundreds of monitors and thousands of data sources; searchable/filterable Sensor Library scale requirements already admitted in source truth.`

Profile Boundary Preservation: `Monitor Groups remain organization/configuration only. Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, provider expansion, Overlay acceptance, FAM-007 work, AI Product work, and NDAI-wide Theme/Skins remain pending USER decisions.`

Validator Planning Update: `Directly supporting validators must prove shrink and grow resize continuity, during-drag render evidence before mouse release, Nexus-styled scrollbar usage in Manage Monitors panes, and large fixture behavior beyond marker-only proof.`

PR Readiness Blocker State: `PR Readiness remains blocked pending repair implementation, Hardening as needed, refreshed Live Validation, and returned USER UTS PASS or explicit waiver with reason digested into source truth.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to Dashboard resize/move live render smoothness, shrink/grow during-drag visual proof, Manage Monitors scalable split layout, Nexus-styled scrollbars, large monitor/source fixtures, directly supporting validators/source truth, validation, commit, and push.`

## Returned UTS FAIL Repair Workstream Implementation

Repair Implementation Status: `IMPLEMENTED - validation-green locally; Hardening and refreshed Live Validation/UTS remain required before PR Readiness.`

Resize/Move Runtime Repair: `The Dashboard fallback resize frame sync now updates the WebEngine geometry, requests repaint/update work each paced resize frame, dispatches resize on requestAnimationFrame, and publishes during-drag resize proof markers through monitoringHudRecordResizeFrame / monitoringHudFinishResizeFrame. The proof marker records grow, shrink, geometry, frame interval, and a subtle pixel-signature background-position pulse so validation can prove visible content changes while the mouse is still held instead of only after release.`

During-Drag Proof Repair: `The governed human-client helper now has Drag-FromToWithGeometryAndVisualSamples and Test-DashboardDuringDragVisualProof. It captures intermediate screenshots before mouse release and requires both geometry changes and pixel-signature deltas for grow and shrink resize paths, including the returned UTS shrink-freeze failure path.`

Manage Monitors Runtime Repair: `Manage Monitors is now a scalable split management surface with sticky header, monitor search, visible/total count, always-reachable in-window Create action, left monitor list pane, right detail pane, and existing create/edit/delete/cancel/confirm behavior preserved.`

Sensor Library Runtime Repair: `The selected-monitor detail pane now uses a searchable/filterable Sensor Library instead of a basic assignment list. It supports supported/deferred filtering plus CPU, GPU, Memory, Disk, Network, Temperature, Load, Clock, Power, Fan, and Voltage categories; source rows expose provider, device, category, metric, and sensor instance breadcrumbs. Supported sources remain assignable and provider-required/deferred sources remain visible, disabled, and explained.`

Large Fixture Repair: `Runtime support now includes a 125-monitor fixture path and 1,200-source Sensor Library fixture planning/proof path through window.setMonitoringHudLargeFixtureMode, monitoringHudLargeMonitorFixtureCount, and monitoringHudLargeSensorFixtureCount. The fixture path is validation/support only and does not imply bulk creation, recommended packs, provider expansion, historical sensor data, alert/rule engine, recording runtime, or Overlay Profile runtime approval.`

Nexus Scrollbar Repair: `Nexus-styled scrollbar treatment is applied to child windows, the monitor list pane, selected-monitor detail pane, sensor result list, sensor settings pane, and sensor preview/details pane. Native-looking scrollbar regressions remain in scope for Hardening and Live Validation verification.`

UTS Handoff Refresh: `The compact User Test Summary handoff now separates Sensor Library scale/scrollbar review, Dashboard resize/move smoothness, and Dashboard control regressions so returned USER results can distinguish the repaired Step 9 and Step 10 findings.`

PR Readiness Blocker State: `PR Readiness remains blocked until this repair validates, commits, pushes, passes Hardening as required, and refreshed Live Validation/UTS returns PASS or an explicit USER waiver with reason is digested into source truth.`

## Returned UTS FAIL Repair Hardening H1

Hardening Status: `Green - bounded H1 fixture-truth and Sensor Library filter repair applied`

Resize/Render Proof Result: `Grow and shrink during-drag proof hooks remain present through monitoringHudRecordResizeFrame / monitoringHudFinishResizeFrame, desktop resize frame synchronization, and human-client frame/pixel-signature proof steps. The proof path continues to require visible content changes before mouse release rather than geometry-only proof.`

Manage Monitors / Sensor Library Result: `The scalable split Manage Monitors layout, monitor search, visible count, Create/Edit/Delete/Cancel/Confirm behavior, Nexus-styled scrollbars, and large monitor/source fixture support remain present. H1 found one bounded truth defect: the 1,200-source fixture path was validation/support-only in source truth but was always included in the normal user-facing Sensor Library.`

Bounded H1 Repair: `The large-source fixture path is now disabled during normal user-facing Sensor Library use and only enters the source list when window.setMonitoringHudLargeFixtureMode enables validation/support mode. The Sensor Library preview no longer advertises fixture-backed sources during normal use, while the explicit large-fixture proof path remains available. Sensor filter matching now checks category, metric, id, source, provider, device, and instance so filters such as Load still work when a source is categorized under CPU/GPU but has a Load metric.`

Nexus Scrollbar Result: `Nexus-styled scrollbar coverage remains required for child windows, monitor list, selected-monitor detail, sensor result list, sensor settings, and sensor preview/details panes.`

Planning Adequacy Preservation: `PR #157/#158 planning adequacy fields remain present: Planning Adequacy Review, Rejected Shallow Plan, Alternatives And Tradeoffs Reviewed, Whole-System Interaction Map, Minimum Viable vs Full System Boundary, and Open Questions / USER Decision Points.`

Hardening Validation Evidence: `powershell -NoProfile -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -RunInteractionSelfQA -ProofSeam "FAM-006 Monitor Groups Hardening H1" PASS; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260515_092243_892; UTS export skipped because UTS belongs to refreshed Live Validation Stage 1.`

PR Readiness Blocker State: `PR Readiness remains blocked until refreshed Live Validation / UTS recheck returns PASS or an explicit USER waiver with reason is digested into source truth.`

## Sensor Library And Profile Planning Admission

Planning Admission Status: `ADMITTED - source-truth planning only; no runtime recording, Overlay Profile UI, tray recording controls, export/share behavior, provider expansion, or Overlay acceptance authorized.`

Profile Model: `Sensor Library = all available or planned data sources`; `Monitor = one configured tracked item`; `Monitor Group = organization/configuration collection`; `Overlay Profile = selected monitors plus layout visible on overlay`; `Recording Profile = selected monitors or sensors logged to file`.

Concept Separation: `Monitor Groups organize and configure monitors. Overlay Profiles decide which monitors appear on the Overlay and how they are laid out. Recording Profiles decide which monitors or sensors are logged. Monitor Groups do not own overlay visibility, recording selection, or recording output behavior.`

Sensor Library Scale Planning: `Sensor Library must support searchable and filterable source discovery for large source inventories, including available runtime-capable sources and planned/provider-required sources without fake-ready claims.`

Manage Monitors Scale Planning: `Manage Monitors must scale to hundreds of monitors and thousands of data sources through searchable/filterable source discovery, scannable monitor lists, Nexus-styled scrollbars, and a layout that does not depend on every monitor or data source being visible at once.`

Recording Scope Planning: `Active Overlay Only`; `Active Monitor Group`; `All Enabled Monitors`; `Custom Recording Profile`; `Selected Sensors`.

Tray Recording Planning: `Start Recording`; `Stop Recording`; `Open Recordings Folder`; `Recording Settings`.

Recording State Planning: `idle`; `recording`; `paused`; `error`.

Local Recording Output Planning: `CSV data plus JSON metadata and sensor manifest saved locally unless the USER chooses an export/share action.`

Recording Metadata Planning: `profile name`; `recording scope`; `sensor IDs`; `display names`; `units`; `polling interval`; `hardware snapshot`; `Nexus version`; `start time`; `end time`.

Future Recording Planning: `event markers during recording`; `auto-record triggers based on warning state, temperature threshold, process launch, or overlay profile switch`; `rolling buffer capture such as Save Last 5 Minutes`.

Privacy / Local-First Boundary: `Recordings are saved locally by default. Export, share, upload, import, or external telemetry behavior requires separate USER approval and source-truth admission.`

Profile Validation Planning: `Source-truth validators must distinguish Monitor Group, Overlay Profile, and Recording Profile concepts. Future runtime validators should prove that a monitor can be enabled, visible, recorded, warning-enabled, or hidden independently. Large fixture planning should include many monitors with only a subset visible on overlay and a different subset included in recording.`

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
- Source-truth planning for searchable/filterable Sensor Library scale.
- Source-truth planning for Overlay Profiles as the future visual-display layer for selected monitors.
- Source-truth planning for Recording Profiles as the future local logging layer for selected monitors or sensors.
- Source-truth planning for recording scopes, tray recording commands, recording states, local CSV/JSON/manifest output, metadata, future event markers, future auto-record triggers, future rolling buffers, and local-first privacy boundaries.

## Package / Slice Boundaries

- Primary package: `PKG-006 - Monitoring and HUD`.
- Primary branch slice: `SLC-027 - Settings and user controls visibility`, continued as Monitor Groups management controls.
- Supporting branch slice: `SLC-025 - Runtime telemetry source and adapter boundary`, limited to truthful sensor/data-source availability and assignment boundaries.
- Supporting branch slice: `SLC-029 - Validation and live desktop proof`, limited to proving Monitor Groups behavior, regression boundaries, and user-facing proof quality.
- Interface Release Boundary: `Monitoring HUD Dashboard Monitor Groups management flow`.
- Primary Interface Release Surface: `Dashboard Monitor Groups create/edit/manage child-window flow`.
- Interface Bundle User Approval: `Not granted - this branch has one primary Monitor Groups management flow; later HUD Overlay display/customization, Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, and recording output remain deferred`.

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

Branch Closure Rule: `Stop after Live Validation Stage 1 precheck validation, commit, and push; continue only after returned USER UTS FAIL findings are repaired and revalidated, or explicitly waived with reason, and the result is digested into source truth.`

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

## Live Validation Stage 1 Result

Live Validation Status: `Precheck PASS / returned USER UTS FAIL`

Live Validation Summary: `Live Validation Stage 1 found bounded validation-path defects before USER handoff: the human-client helper used a heuristic Settings point instead of the visible runtime button, allowed tray actions to fall back to in-app controls, and real client-area mouse clicks on the window-level Dashboard Close did not reliably hit the native close handler. The bounded repair makes Settings and Close proof use visible runtime button rectangles, restricts tray proof to native tray popup/native menu-coordinate evidence, and handles client-area left-clicks for Dashboard Settings and Close in the desktop renderer. After repair, the real red-shortcut human-client proof passed and the active-client helper refreshed a compact Monitor Groups UTS handoff. USER returned UTS FAIL for Dashboard resize/move smoothness, especially shrink freeze/catch-up behavior, and Manage Monitors scalability/native scrollbar issues, so PR Readiness is still blocked.`

Real USER-Facing Shortcut Proof: `PASS - dev/logs/fam_006_human_client_validation/20260514_214332_702/human_client_manifest.json`

Shortcut Alignment: `PASS - the canonical red FAM-006 desktop shortcut targets C:\Nexus Worktrees\FAM-006\launch_orin_desktop.vbs with working directory C:\Nexus Worktrees\FAM-006`

Active-Client UTS Handoff Proof: `PASS - dev/logs/fam_006_monitoring_hud_live_validation/20260514_215201_061`

Formal UTS Handoff Path: `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

Formal UTS Handoff Status: `DRAFT HANDOFF COPY - NOT RETURNED RESULTS`

Live Validation Repair Files: `desktop/desktop_renderer.py`; `dev/orin_monitoring_hud_human_client_validation.ps1`; `dev/orin_monitoring_hud_live_validation.ps1`; `dev/orin_monitoring_hud_surface_validation.py`; `dev/orin_monitoring_hud_internal_sandbox_validation.py`; `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`; `Docs/feature_backlog.md`; `Docs/prebeta_roadmap.md`.

## Expected Seam Families And Risk Classes

Seam Families: `Monitor Groups management UI`; `Create/Edit/Delete monitor flow`; `sensor/data-source assignment`; `per-sensor settings truth`; `Dashboard regression protection`; `validator and proof hardening`; `source-truth governance`.

Risk Classes: `dead-end Monitor Groups controls`; `fake sensor/data-source availability`; `delete without confirmation`; `Create/Edit window flow regression`; `Overlay/display scope creep`; `app-wide Theme/Skins scope creep`; `FAM-007/provider/model bleed`; `marker-only proof`.

## User Test Summary Strategy

Stage 2 setup does not generate a UTS. Runtime implementation and Hardening do not generate returned UTS results. Live Validation Stage 1 refreshed a compact, step-based Monitor Groups UTS handoff at `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`; USER returned FAIL for resize/move smoothness and Manage Monitors scalability/scrollbar findings, so repair and revalidation are required before PR Readiness.

## Later-Phase Expectations

- Hardening H1 is complete and green for list, Create/Edit/Delete, delete confirmation, sensor assignment truth, and Dashboard regressions.
- Live Validation Stage 1 has real USER-facing launcher/shortcut proof PASS and active-client UTS handoff proof PASS; returned USER UTS FAIL remains active.
- PR Readiness, PR creation, merge, release execution, artifacts, raw evidence handling, branch cleanup, Overlay acceptance, FAM-007 work, provider/model/memory/shortcut/installer work, external telemetry parity, and AI Product work remain separate USER decisions.

## Initial Workstream Seam Sequence

Seam 1: `Monitor Groups management flow and sensor-configuration design/implementation`

Goal: `Build the Monitor Groups manage/edit flow so users can create, edit, delete, and assign available sensor/data-source inputs to monitors without leaving the manage/edit context.`

Scope: `Dashboard Monitor Groups management UI, child-window flow, list state, Create/Edit/Delete controls, delete confirmation, sensor/data-source assignment truth, per-sensor settings where supported, and validators.`

Non-Includes: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, artifacts, raw evidence handling, and future branch/worktree cleanup after this branch closes.`

## Active Seam

Active seam: `Live Validation Stage 1 for FAM-006 Monitor Groups sensor configuration`

Active Seam Status: `Live Validation Stage 1 precheck green after bounded client-control repair: red-shortcut human-client proof PASS, active-client proof PASS, compact Monitor Groups UTS handoff refreshed, and returned USER UTS FAIL active.`

Next active seam: `Returned USER UTS digestion or explicit waiver`

## Backlog Completion Status

Backlog Completion State: `Implemented Complete Except Future Dependency`

Remaining Implementable Work: `None`

Future-Dependent Blockers: `Returned USER UTS FAIL repair and revalidation; PR Readiness; PR creation; merge; release execution; artifacts; raw evidence handling; future branch/worktree cleanup; FAM-007 work; provider/model/memory/shortcut/installer work; Overlay acceptance; external telemetry parity; AI Product work`

Completion Status: `Green`

## Seam Continuation Decision

Seam Status: `Green`

Slice Status: `Green`

Completion Status: `Green`

Waiver Status: `None`

Continue Decision: `Stop`

Continuation Execution Latch: `Closed until USER approves returned UTS FAIL repair implementation or explicitly waives the FAIL findings with reason`

Stop Basis: `Live Validation UTS Handoff Pending`

Next Active Seam: `Returned USER UTS digestion or explicit waiver`

Stop Condition: `Live Validation Stage 1 precheck is green; returned USER UTS FAIL repair/revalidation or explicit waiver is required before PR Readiness`

Continuation Action: `Stop inside Live Validation Stage 1 until USER approves UTS FAIL repair implementation, receives a repaired PASS result, or explicitly waives the FAIL findings with reason`

Single-Seam Workstream Waiver: `None`

Single-Seam Or Single-Slice Waiver Authority: `USER only; Codex cannot infer single-seam or single-slice Workstream authority`

Single-Seam Or Single-Slice Workstream Blocker: `One seam or one slice visible in the Workstream plan is a blocker unless a USER waiver is recorded`

Bounded Seam Default: `Bounded means one active seam at a time, not one-seam Workstream authority; same-branch continuation is required until Workstream Completion Status is Green`

## Blockers

Returned USER UTS results are FAIL for Dashboard resize/move smoothness and Manage Monitors scalability/native scrollbar findings. PR Readiness, PR creation, merge, release execution, raw evidence handling, FAM-007 scope, provider/model/memory/shortcut/installer work, Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, Overlay acceptance, external telemetry parity, and AI Product work remain pending USER decisions for later phases.

## Exit Criteria

- Monitor Groups manage/edit flow is implemented.
- Created monitor list, in-window Create, per-monitor Edit, per-monitor Delete with confirmation, source assignment, and per-sensor settings are present.
- Existing Dashboard settings, close, warning notifications, tray-owned HUD control, resize/scroll/source-truth boundaries remain preserved.
- FAM-006 v1.7.1-prebeta release closure remains green.
- FAM-006 released issue closeout posture is preserved.
- Directly supporting validators pass.
- Live Validation Stage 1 real USER-facing shortcut/client precheck passes.
- Compact Monitor Groups UTS handoff is refreshed.
- Required validation passes.
- Live Validation Stage 1 precheck repair commit is pushed.

## Rollback Target

`Workstream`

Rollback is the unmerged Workstream implementation on this branch only if USER later decides to abandon this carrier before PR/merge. Do not delete or mutate other FAM-006, FAM-007, Governance, or main worktrees as part of rollback.

## Next Legal Phase

`Live Validation`

USER decision to approve refreshed Live Validation / UTS recheck for `feature/fam-006-monitor-groups-sensor-configuration`, or explicitly waive the returned UTS FAIL findings with reason.

## Next Legal Phase Digest

Current Phase: `Live Validation`

Next Legal Phase: `Live Validation Stage 1 refreshed UTS recheck`

Why This Phase Is Next: `Returned UTS FAIL repair implementation and Hardening H1 are complete. The next legal step is refreshed real USER-facing Live Validation / UTS recheck for Dashboard resize/move smoothness and Manage Monitors scalability/scrollbar findings.`

Approval Required: `USER approval for refreshed Live Validation / UTS recheck, or explicit waiver of the returned UTS FAIL findings with reason.`

Exact USER Approval Text: `Approve refreshed Live Validation Stage 1 / UTS recheck for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to the repaired Dashboard resize/move smoothness path, Manage Monitors scalability/Sensor Library/Nexus scrollbar behavior, real USER-facing shortcut proof, compact UTS refresh/digestion, required validation, commit, and push if source truth requires a result update.`

Allowed Scope: `Real USER-facing Live Validation recheck, compact UTS refresh/digestion, source-truth update if needed, validation, commit, and push.`

Explicit Exclusions: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, tags, GitHub Releases, artifacts, raw evidence upload/import/linking, and future branch/worktree cleanup after this branch closes.`

Validation Required: `git status --short --branch; git fetch origin --prune; git rev-parse HEAD; git rev-parse origin/main; git worktree list; git diff --check; git diff --check origin/main...HEAD; python dev\orin_monitoring_hud_surface_validation.py; python dev\orin_monitoring_hud_internal_sandbox_validation.py; python dev\orin_branch_governance_validation.py; python dev\orin_release_body_validation.py; python -m compileall -q dev desktop Audio main.py.`

Stop Conditions: `Stop if branch/worktree identity mismatches C:\Nexus Worktrees\FAM-006 / feature/fam-006-monitor-groups-sensor-configuration, origin/main movement creates required reconciliation, returned UTS digestion requires excluded Overlay/FAM-007/provider/model/installer/AI Product/release/PR/raw-evidence scope, USER-facing proof or UTS cannot be completed without waiver, or another USER decision is required.`
