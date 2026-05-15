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
- Branch Authority State: `Active Repair Workstream implementation complete / Hardening H1 pending`
- Bounded State: `Returned refreshed USER UTS FAIL repair implementation is complete; visible resize-proof contamination is removed from normal UI, Sensor Command Center/source picker/final-delete repairs are implemented, and Hardening H1 is pending`
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

Stage: `Repair Workstream implementation complete / Hardening H1 pending`

## Phase Status

Branch Authority Marker: `Active Branch`

Refreshed Live Validation Stage 1 returned FAIL after the prior H1 repair. Current-main reconciliation is complete at `b7a7114af30ff1d378fbdb06e4a86a1410c2cc06` with `origin/main` `cb620709acb95f4457f317b5369bade7d9564724` as an ancestor of the branch. Current Branch Readiness Seam: `Returned refreshed UTS FAIL Sensor Command Center repair setup admitted`. Current Repair Workstream Seam: `Implementation complete for visible proof contamination removal, compact Sensor Command Center, final-delete empty state, faceted Sensor Library source picker, and source classification cleanup`. Current PR Readiness Seam: `Blocked until Hardening, refreshed Live Validation, and returned USER UTS result are PASS or explicitly waived with reason and digested`. Current Release Readiness Seam: `Not started`.

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

Live Validation Stage 1 ends only after returned USER UTS failures are repaired and revalidated, or explicitly WAIVED with reason, and that result is digested into source truth. The current branch contains the original Monitor Groups runtime flow plus an admitted Sensor Command Center repair setup for visible resize-proof contamination, compact monitor selection, right-side detail editing, final delete/empty state, Sensor Library / Source Picker scale, source classification cleanup, directly supporting validators, and refreshed compact USER UTS handoff expectations.

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

USER/ChatGPT Review Checkpoint: `Returned refreshed UTS FAIL - USER screenshots show the implemented UI still treats Manage Monitors as a compact modal with row-level Edit/Delete buttons and a checklist/dropdown source picker, and Step 9 shows visible resize-proof contamination during move/resize. This Stage 2 setup admits the corrected Sensor Command Center repair path before PR Readiness.`

USER Critique Loop: `USER critique/feedback returned the refreshed UTS as FAIL and can still approve, change, defer, or critique the next repair before Workstream implementation. Step 9 functionality improved, but the resize/move proof artifact visibly leaks into the normal Dashboard UI during drag/resize and disappears after release. Step 3/4 show Manage Monitors still has row-level Edit/Delete actions instead of row/icon selection plus detail-pane Delete. Step 6 shows final monitor deletion is blocked instead of allowing a true empty state. Step 8 shows native/basic dropdown behavior and weak Sensor Library scale presentation. USER also required Warning Notifications and Provider Readiness to be removed from assignable sensors and classified as settings/readiness status.`

Historical Repair Trigger Marker: `returned USER UTS FAIL` - preserved for source-truth validator traceability; active state is returned refreshed USER UTS FAIL repair implementation complete with Hardening pending.

USER Decision Ledger: `USER approved bounded Repair Workstream implementation for the returned refreshed UTS FAIL. GitHub issue #127 mutation, PR creation, merge, release execution, raw evidence handling, Overlay Profile runtime, Recording Profile runtime, provider expansion, FAM-007 work, AI Product work, and NDAI-wide Theme/Skins remain pending USER decisions.`

Full Feature Element Breakdown: `Sensor Command Center shell; compact action-light monitor list; row/icon selection; right-side detail panel; detail-pane Delete action; Save / Discard / Cancel guard for unsaved changes; final-monitor delete; true empty state with Create reachable; Sensor Library / Source Picker replacing basic dropdown/checklist assignment; Warning Notifications as settings checkbox outside sensor assignment; Provider Readiness as readiness/status/future capability outside assignable sources; source breadcrumbs using provider > device > category > metric > instance; source status metadata; scalable search plus filter chips/facets; large fixture proof; Overlay Profile planning; Recording Profile planning; validation and UTS proof hooks.`

System Concept Model: `Sensor Library exposes available or planned data sources; monitors are configured tracked items; Monitor Groups organize monitor collections; Overlay Profiles later choose visible monitors and layout; Recording Profiles later choose monitors or sensors to log. This branch repairs the Monitor Groups management surface and proof gates while preserving other concepts as future-gated boundaries.`

Entity / Profile Model: `Sensor Library = all available or planned data sources; Monitor = one configured tracked item; Monitor Group = organization/configuration collection; Overlay Profile = selected monitors plus layout visible on overlay; Recording Profile = selected monitors or sensors logged to file. A monitor may later be enabled, visible, recorded, warning-enabled, or hidden independently.`

User Workflow Model: `USER opens Dashboard, opens Monitor Groups / Manage Monitors, scans compact monitor rows, selects a monitor by row/icon click, edits the right-side detail pane, gets a Save / Discard / Cancel guard before losing unsaved edits, creates monitors from the command surface, deletes from the detail pane with confirmation including the final monitor, reaches a true empty state with Create still available, searches/facets Sensor Library sources, and sees Warning Notifications / Provider Readiness outside assignable sensor rows. The repair also requires Dashboard move/resize proof without visible proof artifacts in the product UI.`

Scale / Data Volume Model: `Manage Monitors must feel like a scalable Sensor Command Center, not a compact modal. It must scale to 100+ monitors and 1,000+ sources using compact rows, source search, filter chips/facets, grouped/statused results, Nexus-styled controls, and fixture validation. The UI must handle duplicate names, long names, deferred sources, missing sources, and source classification without requiring every monitor/source to be visible at once.`

Configuration And State Model: `Monitor configuration includes group membership, enabled state, polling interval, supported source assignment, and supported per-sensor display settings. Warning Notifications is a monitor/settings checkbox, not an assignable sensor. Provider Readiness is readiness/status/future capability, not an assignable sensor. Overlay visibility, recording inclusion, recording output, export/share, provider expansion, templates/import/export, base NCP backup/restore, and app-wide theme state remain separate future models unless explicitly admitted.`

Planning Adequacy Review: `The corrected plan is not shallow because it covers the end-to-end Sensor Command Center system: Dashboard entry, compact monitor navigation, selected-monitor detail editing, unsaved-change safety, final delete and empty state, Sensor Library / Source Picker discovery, source classification, supported/deferred/missing/warning states, large inventory scale, validation proof that rejects visible proof contamination, compact UTS return, and future Overlay/Recording/Profile boundaries.`

Rejected Shallow Plan: `Rejected shallow plan: hide the visible resize artifact and lightly restyle the current modal/checklist. That is insufficient because USER screenshots show the structure is still row-button/checklist driven rather than a scalable Sensor Command Center, and validation instrumentation itself contaminated the product UI.`

Alternatives And Tradeoffs Reviewed: `Alternative option 1 is a full virtualized data-grid/tree with bulk operations, which improves huge-list performance but risks bulk-management scope drift. Alternative option 2 is a Sensor Command Center split surface with compact monitor rows, faceted source picker, capped render lists, and large fixtures, which fits this repair. Tradeoff accepted: keep templates/import/export, bulk packs, recommended packs, alert rules, historical data, and app-wide backup/restore as future planning unless separately admitted.`

Whole-System Interaction Map: `Dashboard card -> Sensor Command Center child window; compact left monitor list/search -> row/icon selection -> unsaved-change Save/Discard/Cancel guard if dirty -> right detail pane; detail-pane Delete -> confirmation/cancel/confirm -> final delete can reach empty state -> Create remains reachable; Sensor Library search/facets -> grouped source rows with breadcrumbs/status -> supported assignment only -> per-sensor settings; resize/move proof -> invisible/test-gated evidence -> compact UTS; Monitor Group configuration stays separate from Overlay Profile visibility and Recording Profile logging.`

Minimum Viable vs Full System Boundary: `Minimum viable current-branch repair scope is visible proof-contamination removal, invisible/test-gated resize proof, Sensor Command Center monitor navigation/detail editing, final delete/empty state, source picker/facets, source classification cleanup, and validation. Full future system scope includes templates, import/export, full app backup/restore in base NCP settings, Overlay Profile runtime UI, Recording Profile runtime, local recording output, tray recording controls, export/share, provider expansion, bulk creation, recommended packs, alert/rule engine, historical sensor data, and NDAI-wide Theme/Skins.`

Open Questions / USER Decision Points: `USER decisions remain pending for runtime repair implementation, GitHub issue #127 mutation, refreshed Live Validation/UTS return or waiver after implementation, PR creation, merge, release work, branch/worktree cleanup, recording runtime, Overlay Profile runtime, tray recording controls, provider/model/shortcut/installer work, Overlay acceptance, external telemetry, FAM-007, AI Product, templates/import/export, base NCP backup/restore architecture, and NDAI-wide Theme/Skins.`

Current Branch vs Future Package Boundaries: `Current branch owns Monitor Groups membership/configuration, Sensor Command Center repair, Sensor Library / Source Picker classification, and source-truth admission for profile-model boundaries. Monitor Groups remain organization/configuration only and do not own overlay visibility or recording selection. Future Overlay Profile runtime owns selected monitors plus Overlay layout/visibility. Future Recording Profile runtime owns selected monitors or sensors logged to local files. Future HUD Overlay customization owns visual display of groups/sensors, colors, borders, text presentation, presets, and Overlay-specific font/display choices. Future templates/import/export and base NCP backup/restore require separate admission. Future NDAI Theme/Skins owns app-wide uniform reskin behavior only after separate USER admission.`

Affected Surfaces: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py`; `desktop/monitoring_hud_controls.py`; FAM-006 HUD validators/helpers as needed by implementation.

Data/Control Model: `Sensor Library equals all available or planned data sources; Monitor equals one configured tracked item; Monitor Group equals an organized monitor collection for organization/configuration; Overlay Profile equals selected monitors plus layout visible on the Overlay; Recording Profile equals selected monitors or sensors logged to file. Sensor/data-source choices must come from current runtime-capable monitor inputs and must not fake unavailable provider, overlay, external telemetry, recording, export/share, or hardware data.`

Branch Reach / Package-Size Review: `Large enough for one runtime branch because it spans UI flow, monitor list operations, create/edit/delete behavior, data-source assignment, per-sensor settings boundaries, validation, and source truth.`

Why Branch Is Large Enough: `A useful Monitor Groups implementation requires several linked controls and state paths; splitting Create, Edit, Delete, and sensor assignment into separate branches would create partial UI and stale proof risk.`

Why Not Split Into Tiny Branches: `The USER-facing flow needs list management and sensor assignment to make sense together; tiny branches would produce dead-end windows or fake-ready controls.`

Acceptance Criteria: `Sensor Command Center lists monitors compactly without row-level Edit/Delete buttons; row/icon click selects and opens details; detail-pane Delete asks for confirmation and can delete the final monitor; empty state is truthful and Create remains reachable; unsaved monitor changes are protected by Save / Discard / Cancel before switching; Sensor Library / Source Picker replaces basic dropdown/checklist assignment; Warning Notifications is a setting checkbox outside sensor assignment; Provider Readiness is readiness/status/future capability outside assignable sources; source rows show provider > device > category > metric > instance breadcrumbs and status metadata; filter chips/facets cover supported categories; visible proof-only resize artifacts are rejected in normal user-facing validation; source truth distinguishes Sensor Library, Monitor, Monitor Group, Overlay Profile, and Recording Profile; no Overlay Profile runtime, Recording Profile runtime, Overlay display acceptance, tray recording controls, export/share behavior, templates/import/export, backup/restore, or app-wide theme work is implied.`

Expected User-Facing Outcomes: `After repair implementation and revalidation, the USER should see Dashboard movement/resizing without visible validation artifacts, plus a Manage Monitors / Sensor Command Center surface that feels scalable, action-light, Nexus-styled, and usable with large monitor/source inventories. PR Readiness remains unavailable until those outcomes are proven or explicitly waived.`

Validation Proof Requirements: `Static HUD validator, internal sandbox validator, branch governance validation, release body validation, compileall, and later runtime-specific Monitor Groups proof beyond marker presence. Validators must reject proof-only visible artifacts in normal user-facing resize/move validation; prove shrink/grow during-drag behavior before mouse release using invisible/test-gated real UI frame, screenshot, pixel-signature, or equivalent evidence; prove 100+ monitors, 1,000+ sources, duplicate names, long names, deferred sources, missing sources, warning state classification, and non-assignable readiness/settings classification; distinguish Monitor Group, Overlay Profile, and Recording Profile concepts without requiring runtime recording controls before separate USER admission.`

Screenshot / Live / User Test Summary Proof Requirements: `Runtime implementation should provide user-visible proof of list/create/edit/delete/confirm/sensor assignment behavior, then Hardening and Live Validation should use the real USER-facing launcher/shortcut path and a compact UTS handoff if USER-facing behavior is changed.`

Implementation Sequence Proposal: `Remove or test-gate visible resize proof artifacts; convert Manage Monitors to compact Sensor Command Center list/detail behavior; implement unsaved-change guard; allow final-delete empty state; replace source checklist/dropdown filtering with Nexus source picker/facets; remove Warning Notifications and Provider Readiness from assignable sensors; add breadcrumbs/status metadata; update validators/helpers/UTS; run Workstream validation; then request Hardening.`

Deferred Ideas / Future Package Ledger: `Templates, monitor list import/export, full app backup/restore through base NCP settings architecture, bulk packs, recommended packs, alert/rule engine, historical sensor data, Overlay Profile runtime, Recording Profile runtime, tray recording controls, local recording output, export/share actions, provider expansion, Overlay acceptance, external telemetry parity, FAM-007 runtime work, AI Product work, and NDAI-wide Theme/Skins are deferred future packages or separately gated work. They must not be implemented by this repair setup.`

Planning Blockers: `Returned Refreshed USER UTS FAIL`; `Visible Resize-Proof Contamination Repair Pending`; `Sensor Command Center Repair Pending`; `Final Monitor Delete / Empty State Repair Pending`; `Nexus Dropdown / Source Picker Repair Pending`; `Source Classification Cleanup Pending`; `Overlay Profile Runtime Approval Missing`; `Recording Profile Runtime Approval Missing`; `Tray Recording Controls Approval Missing`; `Export/Share Runtime Approval Missing`; `Overlay Acceptance Approval Missing`; `Provider/Model/Memory/Shortcut/Installer Approval Missing`; `External Telemetry Parity Approval Missing`; `AI Product Contract Import Approval Missing`; `PR Creation Approval Missing`.

USER Decisions Needed: `Approve runtime repair implementation for this Stage 2 setup; approve GitHub issue #127 mutation if desired; return refreshed UTS results or explicit waiver with reason after implementation and validation; approve PR creation later; approve merge later; approve release/artifacts/raw evidence/branch cleanup separately; approve templates/import/export, full backup/restore, Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, Overlay acceptance, FAM-007, provider/model/memory/shortcut/installer, external telemetry, or AI Product work separately.`

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

Planning Completion Waiver: `Not required - required product/system/profile/workflow/scale/state planning fields are recorded for this branch-local Stage 2 repair setup.`

User Test Summary Strategy: `No UTS is generated during Stage 2 setup. Runtime implementation should prepare a compact step-based UTS only when user-facing behavior is ready for Live Validation. The current compact UTS returned FAIL, so PR Readiness remains blocked until the resize/render-freeze and Manage Monitors scalability findings are repaired and revalidated or explicitly waived.`

## Returned UTS FAIL Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2`

Current-Main Reconciliation Confirmation: `PASS - current-main reconciliation is complete, clean, pushed, validation-green, and origin/main cb620709acb95f4457f317b5369bade7d9564724 is an ancestor of the FAM-006 branch.`

Returned UTS Scope Admitted: `Returned UTS Steps 1-8 passed; Step 9 failed Dashboard resize/move smoothness, especially shrink behavior where rendering appears frozen until resize completes; Step 10 failed Manage Monitors design/scalability because the scrollbar appears native Windows styled and the flow does not scale to hundreds of monitors and thousands of data sources.`

Resize/Move Repair Scope: `Dashboard resize/move live render smoothness; shrink and grow resize visual continuity; during-drag frame, pixel-signature, or video-style proof before mouse release; proof must show the Dashboard renders during drag rather than only after mouse release.`

Manage Monitors Repair Scope: `Manage Monitors scalable split layout; Nexus-styled scrollbars in child windows, monitor list, detail pane, sensor tree, sensor result list, and sensor preview/details pane; large-monitor and large-source fixtures for hundreds of monitors and thousands of data sources; searchable/filterable Sensor Library scale requirements already admitted in source truth.`

Profile Boundary Preservation: `Monitor Groups remain organization/configuration only. Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, provider expansion, Overlay acceptance, FAM-007 work, AI Product work, and NDAI-wide Theme/Skins remain pending USER decisions.`

Validator Planning Update: `Directly supporting validators must prove shrink and grow resize continuity, during-drag render evidence before mouse release, Nexus-styled scrollbar usage in Manage Monitors panes, and large fixture behavior beyond marker-only proof.`

PR Readiness Blocker State: `PR Readiness remains blocked pending repair implementation, Hardening as needed, refreshed Live Validation, and returned USER UTS PASS or explicit waiver with reason digested into source truth.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to removing visible resize-proof contamination, adding invisible/test-gated grow/shrink during-drag proof, implementing the Sensor Command Center compact monitor list/detail-pane repair, adding final-monitor delete and true empty state, replacing basic dropdown/checklist source assignment with Nexus Sensor Library / Source Picker search/facets, classifying Warning Notifications and Provider Readiness outside assignable sensors, adding breadcrumbs/status metadata, updating validators/helpers/UTS, validation, commit, and push.`

## Returned Refreshed UTS FAIL Sensor Command Center Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2`

Returned Refreshed UTS Classification: `REPAIR REQUIRED - Step 9 visible resize/move artifact is a blocking user-facing validation contamination bug; Step 3/4 Manage Monitors still behaves like a compact modal with row buttons; Step 6 final monitor delete is blocked; Step 8 basic/native dropdown behavior fails Nexus UI expectations; Warning Notifications and Provider Readiness are misclassified as assignable source/data-source items.`

Visible Resize-Proof Contamination Setup: `Admit repair to remove or test-gate normal-user-visible CSS monitoring-hud__chrome::after proof layer, JS --monitoring-hud-live-resize-proof-* visual effects, native monitoringHudResizeProofOverlay, and any helper/debug overlay or proof marker that appears in normal user-facing validation. Normal Dashboard move/resize must not show proof-only bands, overlays, masks, or glow artifacts.`

Invisible / Test-Gated Resize Proof Setup: `Resize proof must use invisible/test-gated real UI frame, screenshot, pixel-signature, geometry, or equivalent evidence. Validators must prove shrink and grow during-drag behavior before mouse release while rejecting proof-only visible artifacts in normal user-facing validation.`

Sensor Command Center Setup: `Manage Monitors remains a split layout but becomes a Sensor Command Center: compact action-light monitor list, row/icon selection, right-side detail panel, detail-pane Delete, Save / Discard / Cancel guard for unsaved changes, final-monitor delete, true empty state with Create still reachable, and large-fixture proof for 100+ monitors.`

Sensor Library / Source Picker Setup: `Replace basic dropdown/checklist assignment with Sensor Library / Source Picker behavior: scalable search plus filter chips/facets; categories for CPU, GPU, Memory, Disk, Network, Temperature, Load, Clock, Power, Fan, Voltage, Supported, Deferred, Missing, and Warning where source truth supports them; source rows with provider > device > category > metric > instance breadcrumbs; and source status metadata for supported, deferred, missing, warning, and provider-required states.`

Sensor / Source Classification Setup: `Warning Notifications classified as a monitor/settings checkbox outside sensor assignment. Provider Readiness classified as readiness/status/future capability outside assignable sources. Supported runtime-capable sources remain assignable; provider-required, deferred, missing, warning, readiness, and settings entries must not be over-credited as assignable sensors.`

Dropdown Repair And Proof Setup: `Current native/basic dropdown controls in Monitor Groups / Sensor Library are admitted for repair or replacement with Nexus-styled dropdown/facet controls. Proof must cover open, hover, close, reopen, keyboard/mouse selection, and visual style using video, frame-sequence, screenshot sequence, or equivalent visual evidence.`

Large Fixture / Edge Case Proof Setup: `Direct validators/helpers must prove 100+ monitors, 1,000+ sources, duplicate source names, long monitor names, long source names, deferred sources, missing sources, source classification, true empty state, final delete, unsaved-change guard, and no proof-only visible artifacts during normal user-facing resize/move validation.`

Profile Boundary Preservation: `Sensor Library = all available or planned data sources; Monitor = one configured tracked item; Monitor Group = organization/configuration collection; Overlay Profile = selected monitors plus layout visible on overlay; Recording Profile = selected monitors or sensors logged to file. Monitor Groups do not own overlay visibility, recording selection, recording output, Overlay Profile runtime, or Recording Profile runtime.`

Future Workflow Preservation: `Monitor-first, sensor-first, and group-first workflows remain future planning unless directly needed for this repair. Templates, import/export, bulk packs, recommended packs, alert/rule engine, historical data, Overlay Profile runtime, Recording Profile runtime, tray recording, local CSV/JSON/manifest recording output, event markers, auto-record triggers, rolling buffer capture, full app backup/restore, and base NCP settings architecture remain pending USER decisions.`

PR Readiness Blocker State: `PR Readiness remains blocked pending Repair Workstream implementation, Hardening, refreshed Live Validation / UTS recheck, and returned USER UTS PASS or explicit waiver with reason digested into source truth.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to removing visible resize-proof contamination, adding invisible/test-gated grow/shrink during-drag proof, implementing the Sensor Command Center compact monitor list/detail-pane repair, adding final-monitor delete and true empty state, replacing basic dropdown/checklist source assignment with Nexus Sensor Library / Source Picker search/facets, classifying Warning Notifications and Provider Readiness outside assignable sensors, adding breadcrumbs/status metadata, updating validators/helpers/UTS, validation, commit, and push.`

## Returned UTS FAIL Repair Workstream Implementation

Repair Implementation Status: `HISTORICAL / SUPERSEDED - the earlier returned UTS FAIL repair implementation was validation-green locally, but returned refreshed USER UTS found visible proof contamination and Sensor Command Center design gaps. The current corrected repair implementation remains pending USER approval.`

Resize/Move Runtime Repair: `Historical repair evidence only. The Dashboard fallback resize frame sync updated WebEngine geometry and published during-drag proof markers, but returned refreshed UTS identified proof marker visualization as user-facing contamination. Current repair must remove or test-gate visible proof artifacts and prove real UI frame movement invisibly.`

During-Drag Proof Repair: `The governed human-client helper now has Drag-FromToWithGeometryAndVisualSamples and Test-DashboardDuringDragVisualProof. It captures intermediate screenshots before mouse release and requires both geometry changes and pixel-signature deltas for grow and shrink resize paths, including the returned UTS shrink-freeze failure path.`

Manage Monitors Runtime Repair: `Historical repair evidence only. The prior split management surface kept row-level actions and checklist/dropdown assignment; returned refreshed UTS requires the corrected compact Sensor Command Center repair before PR Readiness.`

Sensor Library Runtime Repair: `Historical repair evidence only. The prior selected-monitor detail pane added search/filter behavior, but returned refreshed UTS requires a Nexus Source Picker / Sensor Library repair that replaces native/basic dropdown/checklist behavior, adds facets, and removes Warning Notifications / Provider Readiness from assignable sources.`

Large Fixture Repair: `Runtime support now includes a 125-monitor fixture path and 1,200-source Sensor Library fixture planning/proof path through window.setMonitoringHudLargeFixtureMode, monitoringHudLargeMonitorFixtureCount, and monitoringHudLargeSensorFixtureCount. The fixture path is validation/support only and does not imply bulk creation, recommended packs, provider expansion, historical sensor data, alert/rule engine, recording runtime, or Overlay Profile runtime approval.`

Nexus Scrollbar Repair: `Nexus-styled scrollbar treatment is applied to child windows, the monitor list pane, selected-monitor detail pane, sensor result list, sensor settings pane, and sensor preview/details pane. Native-looking scrollbar regressions remain in scope for Hardening and Live Validation verification.`

UTS Handoff Refresh: `The compact User Test Summary handoff now separates Sensor Library scale/scrollbar review, Dashboard resize/move smoothness, and Dashboard control regressions so returned USER results can distinguish the repaired Step 9 and Step 10 findings.`

PR Readiness Blocker State: `PR Readiness remains blocked because this earlier repair is superseded by returned refreshed UTS FAIL; the corrected Repair Workstream implementation, Hardening, refreshed Live Validation/UTS PASS, or explicit USER waiver with reason are still required.`

## Returned UTS FAIL Repair Hardening H1

Hardening Status: `HISTORICAL GREEN / SUPERSEDED - bounded H1 fixture-truth, Sensor Library filter, resize hit-zone, native repaint overlay, and during-drag proof repair passed before returned refreshed UTS identified visible proof contamination and Sensor Command Center design gaps.`

Resize/Render Proof Result: `Historical H1 result only. Grow and shrink during-drag proof hooks were present, but returned refreshed UTS identified native monitoringHudResizeProofOverlay / CSS proof bands / proof marker visuals as user-facing contamination. Current repair must move proof to invisible/test-gated real UI frame, screenshot, pixel-signature, or equivalent evidence while rejecting visible proof-only artifacts.`

Manage Monitors / Sensor Library Result: `Historical H1 result only. The split Manage Monitors layout and large fixture proof existed, but returned refreshed UTS found the user-facing structure still too modal/action-heavy and the source picker too dropdown/checklist-like. Current repair must deliver the compact Sensor Command Center and Nexus Source Picker setup admitted above.`

Bounded H1 Repair: `Historical H1 repair evidence only. The large-source fixture and filter improvements remain useful planning/proof inputs, but the native Qt repaint proof overlay and visible proof markers are now admitted repair targets because they leaked into normal user-facing validation.`

Nexus Scrollbar Result: `Nexus-styled scrollbar coverage remains required for child windows, monitor list, selected-monitor detail, sensor result list, sensor settings, and sensor preview/details panes.`

Planning Adequacy Preservation: `PR #157/#158 planning adequacy fields remain present: Planning Adequacy Review, Rejected Shallow Plan, Alternatives And Tradeoffs Reviewed, Whole-System Interaction Map, Minimum Viable vs Full System Boundary, and Open Questions / USER Decision Points.`

Hardening Validation Evidence: `powershell -NoProfile -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -RunInteractionSelfQA -ProofSeam "FAM-006 Monitor Groups Hardening H1" PASS; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260515_092243_892. Focused returned-UTS resize H1 human-client proof PASS with -SkipNcpRegressionChecks; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_human_client_validation\20260515_112558_577; grow proof recorded 42 unique sizes, 5 captured frames, 4 frame-geometry deltas; shrink proof recorded 42 unique sizes, 5 captured frames, 4 frame-geometry deltas, 2 pixel-signature deltas, and 2px max/average shrink tracking lag. Post-repair active-client self-QA PASS; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260515_112924_766. UTS export skipped because UTS belongs to refreshed Live Validation Stage 1.`

PR Readiness Blocker State: `PR Readiness remains blocked until corrected Repair Workstream implementation, Hardening, refreshed Live Validation / UTS recheck returns PASS, or an explicit USER waiver with reason is digested into source truth.`

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
- Compact action-light created monitor list inside the Sensor Command Center / manage window.
- Create button inside the edit/manage window.
- Row/icon selection that opens each monitor's right-side detail settings.
- Detail-pane Delete action with confirmation before destructive removal.
- Save / Discard / Cancel guard for unsaved edits when switching monitors.
- Final-monitor delete with true empty state and Create still reachable.
- Sensor Library / Source Picker for available runtime-capable monitor inputs.
- Warning Notifications as monitor/settings checkbox outside sensor assignment.
- Provider Readiness as readiness/status/future capability outside assignable sources.
- Per-sensor settings where current runtime support exists.
- Source breadcrumbs/status metadata and scalable search/facet proof.
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
- Corrected Runtime/User-Facing Delta: `Sensor Command Center repair for compact monitor selection, right-side details, detail-pane delete, unsaved-change guard, final-delete empty state, Sensor Library / Source Picker, source classification, and invisible/test-gated resize proof.`
- Exact Affected Paths: `nexus_visual/monitoring_hud.html`; `nexus_visual/monitoring_hud.css`; `nexus_visual/monitoring_hud.js`; `desktop/desktop_renderer.py`; `desktop/monitoring_hud_controls.py`; FAM-006 HUD validators/helpers as needed by implementation.
- Carried Issues: `None newly created by Stage 2 setup`; all released FAM-006 issue threads #123, #124, #125, #126, #127, #137, and #140 are closed / fixed or completed.
- Non-Includes: `HUD Overlay visual display acceptance`; `Overlay customization`; `NDAI-wide Theme/Skins`; `FAM-007`; `provider/model/memory/shortcut/installer work`; `external telemetry parity`; `AI Product Contract import`; `raw evidence upload/import/linking`; `release execution`; `PR creation`; `merge`; `future branch/worktree cleanup after this branch closes`.
- Implementation Admission Status: `USER-approved Stage 2 repair setup complete after this packet validates, commits, and pushes; runtime Repair Workstream implementation remains pending USER approval.`

## Backlog Completion Strategy

Branch Completion Goal: `Complete the FAM-006 Monitor Groups sensor-configuration runtime flow through implementation, Hardening, Live Validation, PR Readiness, merge, and later release handling after each phase receives USER approval.`

Known Future-Dependent Blockers: `Repair Workstream runtime implementation approval, PR creation, merge, release execution, artifacts, raw evidence handling, future branch/worktree cleanup after this branch closes, FAM-007 work, provider/model/memory/shortcut/installer work, Overlay acceptance, external telemetry parity, AI Product work, templates/import/export, full app backup/restore, base NCP settings architecture, and app-wide Theme/Skins all require later USER approval.`

Branch Closure Rule: `Stop after Branch Readiness Stage 2 repair setup validation, commit, and push; continue only after USER explicitly approves Repair Workstream implementation for the admitted Sensor Command Center and invisible/test-gated resize proof repair path.`

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

Implementation Status: `Initial implementation complete - committed and pushed at dcd58d3982c8d8a404f41f97371247fd19463f9b; superseded by returned refreshed UTS repair setup for Sensor Command Center and source-classification corrections before PR Readiness.`

Runtime Summary: `The initial Manage Monitors runtime delivered created monitor rows, in-window Create Monitor, row-level Edit/Delete, selected-monitor settings, supported sensor/data-source assignment, and provider-required unavailable states. Returned refreshed UTS now treats row-level Edit/Delete, checklist/dropdown assignment, Warning Notifications as an assignable source, and Provider Readiness as an assignable source as repair targets; the corrected runtime implementation is pending USER approval.`

User-Facing Behavior Changed: `The Dashboard Monitor Groups card opens Manage Monitors for list/create/edit/delete/source assignment, but returned refreshed UTS requires the next repair to convert it into the Sensor Command Center: compact action-light list, row/icon selection, right-side detail pane, detail-pane Delete, Save / Discard / Cancel guard, final-delete empty state, Nexus Source Picker, and corrected source classification.`

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

Live Validation Status: `Returned refreshed USER UTS FAIL / Branch Readiness Stage 2 repair setup admitted`

Live Validation Summary: `Refreshed Live Validation Stage 1 precheck passed the real red-shortcut human-client path and active-client compact UTS handoff, but returned USER results are FAIL. The USER screenshot and UTS identified visible resize-proof contamination during normal move/resize, Manage Monitors row-level Edit/Delete and checklist/dropdown source assignment, blocked final-monitor delete, native/basic dropdown behavior, and incorrect assignment classification for Warning Notifications and Provider Readiness. PR Readiness remains blocked until the admitted repair implementation, Hardening, refreshed Live Validation, and returned USER result are PASS or explicitly waived with reason and digested.`

Real USER-Facing Shortcut Proof: `PASS - dev/logs/fam_006_human_client_validation/20260515_114143_928/human_client_manifest.json`

Shortcut Alignment: `PASS - the canonical red FAM-006 desktop shortcut targets C:\Nexus Worktrees\FAM-006\launch_orin_desktop.vbs with working directory C:\Nexus Worktrees\FAM-006`

Active-Client UTS Handoff Proof: `PASS - dev/logs/fam_006_monitoring_hud_live_validation/20260515_114505_431`

Formal UTS Handoff Path: `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

Formal UTS Handoff Status: `DRAFT HANDOFF REFRESH REQUIRED after Hardening H1 / prior returned USER result remains FAIL until refreshed USER UTS returns PASS or is explicitly waived`

Live Validation Repair Files: `desktop/desktop_renderer.py`; `dev/orin_monitoring_hud_human_client_validation.ps1`; `dev/orin_monitoring_hud_live_validation.ps1`; `dev/orin_monitoring_hud_surface_validation.py`; `dev/orin_monitoring_hud_internal_sandbox_validation.py`; `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`; `Docs/feature_backlog.md`; `Docs/prebeta_roadmap.md`.

## Expected Seam Families And Risk Classes

Seam Families: `Sensor Command Center management UI`; `compact monitor selection`; `right-side detail editing`; `final delete and empty state`; `Sensor Library / Source Picker`; `source classification`; `Dashboard resize/move proof isolation`; `validator and proof hardening`; `source-truth governance`.

Risk Classes: `visible validation contamination in product UI`; `dead-end Monitor Groups controls`; `fake sensor/data-source availability`; `settings/readiness items misclassified as sensors`; `delete without confirmation`; `blocked final delete`; `native/basic dropdown regression`; `Overlay/display scope creep`; `app-wide Theme/Skins scope creep`; `FAM-007/provider/model bleed`; `marker-only proof`.

## User Test Summary Strategy

Repair Workstream implementation updates the compact UTS wording source. The current compact UTS at `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt` was previously returned by USER as FAIL. The UTS handoff must be refreshed after Hardening H1 so the USER can retest visible resize-proof contamination removal, Sensor Command Center behavior, final-delete empty state, Nexus source picker/dropdown behavior, and source-classification cleanup.

## Later-Phase Expectations

- Prior Hardening H1 is complete for the previous repair implementation, but returned refreshed UTS FAIL supersedes it for PR Readiness.
- Refreshed Live Validation Stage 1 has real USER-facing launcher/shortcut proof PASS and active-client UTS handoff proof PASS, but returned USER UTS result is FAIL and must be repaired or explicitly waived with reason.
- PR Readiness, PR creation, merge, release execution, artifacts, raw evidence handling, branch cleanup, Overlay acceptance, FAM-007 work, provider/model/memory/shortcut/installer work, external telemetry parity, and AI Product work remain separate USER decisions.

## Initial Workstream Seam Sequence

Seam 1: `Monitor Groups management flow and sensor-configuration design/implementation`

Goal: `Repair the Monitor Groups manage/edit flow into a scalable Sensor Command Center so users can select compact monitor rows, edit details safely, delete from the detail pane including the final monitor, and assign supported sources through a searchable/faceted Sensor Library without leaving the manage/edit context.`

Scope: `Dashboard Monitor Groups management UI, child-window flow, compact list state, row/icon selection, detail-pane editing and Delete, Save / Discard / Cancel guard, final-delete empty state, Sensor Library / Source Picker assignment truth, per-sensor settings where supported, invisible/test-gated resize proof, and validators.`

Non-Includes: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, artifacts, raw evidence handling, and future branch/worktree cleanup after this branch closes.`

## Active Seam

Active seam: `Repair Workstream implementation for FAM-006 Sensor Command Center returned refreshed UTS FAIL`

Active Seam Status: `Returned refreshed UTS FAIL runtime repair implemented: normal UI no longer shows resize proof artifacts, Sensor Command Center replaces row-button/checklist management, final-monitor delete reaches a true empty state, Source Picker uses Nexus search/facets, and Warning Notifications / Provider Readiness are classified outside assignable sensors.`

Next active seam: `Hardening H1 after repair implementation`

## Backlog Completion Status

Backlog Completion State: `Repair Implementation Complete / Hardening Pending`

Remaining Implementable Work: `No additional runtime work admitted before Hardening. Hardening H1 must pressure-test the implemented repair and may apply bounded same-seam fixes if defects are found.`

Future-Dependent Blockers: `Hardening H1; refreshed Live Validation/UTS after repair; PR Readiness; PR creation; merge; release execution; artifacts; raw evidence handling; future branch/worktree cleanup; FAM-007 work; provider/model/memory/shortcut/installer work; Overlay acceptance; external telemetry parity; AI Product work`

Completion Status: `Blocked before PR Readiness`

## Seam Continuation Decision

Seam Status: `Repair Workstream implementation complete; Hardening H1 pending`

Slice Status: `Admitted repair scope implemented; pressure testing pending`

Completion Status: `Blocked by Hardening H1 and refreshed Live Validation / UTS recheck`

Waiver Status: `None`

Continue Decision: `Proceed only after USER approves Hardening H1`

Continuation Execution Latch: `Closed until USER approves Hardening H1`

Stop Basis: `Repair implementation complete / Hardening H1 approval pending`

Next Active Seam: `Hardening H1`

Stop Condition: `Returned refreshed UTS FAIL repair is implemented; Hardening requires explicit USER approval before work resumes`

Continuation Action: `Stop after Repair Workstream implementation until USER approves Hardening H1`

Single-Seam Workstream Waiver: `None`

Single-Seam Or Single-Slice Waiver Authority: `USER only; Codex cannot infer single-seam or single-slice Workstream authority`

Single-Seam Or Single-Slice Workstream Blocker: `One seam or one slice visible in the Workstream plan is a blocker unless a USER waiver is recorded`

Bounded Seam Default: `Bounded means one active seam at a time, not one-seam Workstream authority; same-branch continuation is required until Workstream Completion Status is Green`

## Blockers

Returned refreshed USER UTS was FAIL and the bounded runtime repair has been implemented. PR Readiness remains blocked until Hardening H1 and refreshed Live Validation / returned USER UTS recheck prove the repair or USER explicitly waives remaining gates with reason. PR creation, merge, release execution, raw evidence handling, FAM-007 scope, provider/model/memory/shortcut/installer work, Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, Overlay acceptance, external telemetry parity, and AI Product work remain pending USER decisions for later phases.

## Exit Criteria

- Returned refreshed UTS FAIL repair implementation is complete.
- Visible resize-proof contamination, invisible/test-gated resize proof, Sensor Command Center, final-delete empty state, dropdown/source picker, and source-classification repairs are implemented and ready for H1 pressure testing.
- Existing Dashboard settings, close, warning notifications, tray-owned HUD control, resize/scroll/source-truth boundaries are preserved as regression requirements.
- FAM-006 v1.7.1-prebeta release closure remains green.
- FAM-006 released issue closeout posture is preserved.
- Directly supporting validators pass.
- PR Readiness remains blocked until Hardening, refreshed Live Validation, and returned USER UTS PASS or explicit waiver with reason.
- Required validation passes.
- Repair Workstream implementation commit is pushed.

## Rollback Target

`Workstream`

Rollback is the unmerged Workstream implementation on this branch only if USER later decides to abandon this carrier before PR/merge. Do not delete or mutate other FAM-006, FAM-007, Governance, or main worktrees as part of rollback.

## Next Legal Phase

`Workstream`

USER decision to approve Hardening H1 for `feature/fam-006-monitor-groups-sensor-configuration`.

## Next Legal Phase Digest

Current Phase: `Repair Workstream implementation`

Next Legal Phase: `Hardening H1`

Why This Phase Is Next: `The bounded runtime repair is implemented. Hardening H1 must challenge the visible proof contamination removal, invisible/test-gated proof, Sensor Command Center behavior, final-delete empty state, source picker/dropdown behavior, and source classification cleanup before refreshed Live Validation / UTS recheck.`

Approval Required: `USER approval for Hardening H1.`

Exact USER Approval Text: `Approve Hardening H1 for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006 after the returned UTS FAIL repair implementation, including pressure-testing visible resize-proof contamination removal, invisible/test-gated grow/shrink during-drag proof, Sensor Command Center compact monitor list/detail-pane behavior, final-monitor delete and true empty state, Nexus Sensor Library / Source Picker search/facets, Warning Notifications / Provider Readiness classification, directly supporting validator/helper/source-truth repair if H1 finds same-seam defects, validation, commit, and push if needed.`

Allowed Scope: `Hardening H1 pressure testing inside the admitted FAM-006 Monitor Groups / Sensor Command Center seam, bounded same-seam repair if defects are found, directly supporting validators/helpers/source truth, compact UTS refresh if required, validation, commit, and push if needed.`

Explicit Exclusions: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, tags, GitHub Releases, artifacts, raw evidence upload/import/linking, and future branch/worktree cleanup after this branch closes.`

Validation Required: `git status --short --branch; git fetch origin --prune; git rev-parse HEAD; git rev-parse origin/main; git worktree list; git diff --check; git diff --check origin/main...HEAD; python dev\orin_monitoring_hud_surface_validation.py; python dev\orin_monitoring_hud_internal_sandbox_validation.py; python dev\orin_branch_governance_validation.py; python dev\orin_release_body_validation.py; python -m compileall -q dev desktop Audio main.py.`

Stop Conditions: `Stop if branch/worktree identity mismatches C:\Nexus Worktrees\FAM-006 / feature/fam-006-monitor-groups-sensor-configuration, origin/main movement creates required reconciliation, implementation requires excluded Overlay/FAM-007/provider/model/installer/AI Product/release/PR/raw-evidence scope, Sensor Command Center and invisible/test-gated proof scope cannot be preserved together, validation fails, or another USER decision is required.`
