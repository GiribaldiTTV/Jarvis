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
- Branch Authority State: `Active Repair Workstream implementation for returned LV1 interactive-control reliability and visual-affordance failure`
- Bounded State: `Current-main reconciliation through origin/main 6e2e743fd1d8d688c8046eb0a788b1a7109e66c2 is complete on this FAM-006 branch; origin/main PR #169 governance/source-truth changes are context, not identity; right-edge rediscovery repair and Hardening H1 are green with Dashboard product edge math preserved; the returned LV1 interactive-control reliability and visual-affordance repair is implemented. Runtime now adds visible Nexus hover/active/focus-visible/disabled/open/selected states across current Dashboard and Manage Monitors interactables, a reliable activation layer with first-click and click-interception proof data, Polling Floor renamed to Polling Rate, and a Nexus-styled Polling Rate bounded dropdown. PR Readiness remains blocked until Hardening H1 and refreshed LV1/UTS pass or are waived with reason, and blockers are reevaluated.`
- Runtime-Specific Carrier: `FAM-006 Dashboard Monitor Groups sensor/data-source configuration`
- Source-Truth Authority: `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
- No Cross-Worktree Mutation: `Required - this branch writes only inside C:\Nexus Worktrees\FAM-006`
- GitHub Desktop-bound worktree: `FAM-006` recommended alias after USER adds or refreshes the repository in GitHub Desktop

## Worktree Recovery And Stale Branch Cleanup

FAM-006 Stable Worktree Path: `C:\Nexus Worktrees\FAM-006`

Recovery Reason: `The initial Stage 2 setup created the active Monitor Groups branch in C:\Nexus Worktrees\FAM-006-Monitor-Groups and then removed the retired settings-panel worktree at C:\Nexus Worktrees\FAM-006 during stale-branch cleanup, which caused GitHub Desktop to lose the stable FAM-006 repository path. The active Monitor Groups worktree was moved to the stable FAM-006 path so GitHub Desktop and future helpers have one durable FAM-006 repository target.`

Retired Branch Cleanup Result: `COMPLETE - former feature/fam-006-dashboard-settings-panel worktree C:\Nexus Worktrees\FAM-006 was removed only after merge/equality proof, the remote branch feature/fam-006-dashboard-settings-panel was deleted, and the local stale branch was deleted. The active FAM-006 worktree now points to feature/fam-006-monitor-groups-sensor-configuration.`

## Current Phase

Phase: `Workstream`

Stage: `Repair Workstream implementation - returned LV1 interactive-control reliability and visual-affordance failure`

## Phase Status

Branch Authority Marker: `Active Branch`

Refreshed Live Validation Stage 1 after right-edge H1 PASS found a new returned USER/UTS failure: Dashboard and Manage Monitors clickable controls do not consistently light up on hover, intermittent first-click actions can miss or appear intercepted for monitor switching and close controls, and the Polling Floor label/dropdown remains product/UI-polish incorrect. Current-Main Reconciliation Identity Guard: `origin/main is context, not identity; Docs/feature_backlog.md and Docs/prebeta_roadmap.md reassert feature/fam-006-monitor-groups-sensor-configuration and this authority record as branch-local FAM-006 truth before commit`. Current Branch Readiness Seam: `Stage 2 repair setup admitted for interactive-control visual affordance and first-click reliability`. Current Repair Workstream Seam: `Implemented in bounded FAM-006 runtime/helper/source-truth surfaces`. Current Hardening Seam: `Pending after this implementation`. Current Live Validation Seam: `Returned LV1/UTS failure recorded; previous automated helper evidence is superseded by returned USER findings until H1 and refreshed LV1 recheck pass`. Current PR gate: `Blocked until interactive-control reliability/visual-affordance repair H1, refreshed LV1/UTS, and returned USER result are PASS or explicitly waived with reason and digested`. Current Release Readiness Seam: `Not started`.

## Branch Class

`implementation`

This branch is a FAM-006 runtime carrier. It may carry the bounded source-truth and governance setup needed before implementation, but it must not become a governance-only branch.

## Runtime Branch Engineering Contract

Engineering Contract Status: Accepted after PR #164 current-main reconciliation, preserved through PR #169 current-main reconciliation, and current after returned LV1 interactive-control reliability and visual-affordance repair implementation for this active FAM-006 runtime branch.
USER Engineering Planning Review: USER approved the FAM-006 Monitor Groups planning, repair setup, and close-guard implementation sequencing before this Workstream continuation.
Runtime Implementation Approval: `Approved and used for the bounded returned LV1 interactive-control reliability and visual-affordance Repair Workstream implementation. This approval did not authorize app-wide theme/skin work, base NCP settings architecture, provider expansion, Overlay Profile runtime UI, tray recording, release execution, PR creation, or issue mutation.`
Branch Purpose: This branch implements the FAM-006 Monitor Groups runtime surface for configurable monitor groups, Sensor Library assignment, and proof-backed user interactions.
Current Runtime Baseline: The desktop HUD runtime already has Dashboard state, Manage Monitors UI, Sensor Library source discovery, provider-truthful disabled sources, and validator/helper proof.
Planned Runtime Delta: The approved bounded repair plan was to add visible hover/active/focus-visible/disabled/open/selected states for FAM-006 Dashboard and Manage Monitors interactables; add repeated first-click reliability proof and click-interception diagnostics for close, monitor switching, create, save, cancel, discard, delete, Source Filter, Polling Rate, Dashboard settings/warning/hub actions, and Dashboard close; rename Polling Floor to Polling Rate; and replace the native/basic polling select with a Nexus-styled bounded Polling Rate dropdown.
Implemented Runtime Delta: The bounded runtime delta adds visible hover/active/focus-visible/click states for FAM-006 Dashboard and Manage Monitors interactables, a reliable activation layer for close, monitor switch, create, save, cancel, discard, delete, Source Filter, Polling Rate, Dashboard settings/warning/hub actions, and Dashboard close, first-click stress proof data, click-interception diagnostics, Polling Floor copy repair to Polling Rate, and a Nexus-styled Polling Rate bounded dropdown.
User-Facing Runtime Delta: The user-visible UI now makes Dashboard and Manage Monitors controls visibly respond to hover/focus/active states, first clicks route through a reliable activation path for current controls, and the Polling Rate copy/status/control behaves like a Nexus/NDAI dropdown instead of a native/basic select.
State / Config / Schema Delta: No product schema migration was added; proof manifests and runtime state gained interactive-control stress fields for target control identity, state coverage, first-click attempt/result, intercepted element, stale/disabled/aria state, z-index/pointer-events context, and repeated pass counts.
Validator / Helper Delta: Validators/helpers now require code inspection and focused visual inspection for user-facing interactables, repeated first-click stress proof for Dashboard and Manage Monitors controls, dropdown proof for Source Filter plus Polling Rate normal/hover/active/focus/open/selected states, and focused visual proof that is not a full-desktop-only substitute.
Expected Changed Files / Surfaces: Expected files and surfaces include HUD CSS/HTML/JS, desktop renderer/live proof helpers, HUD validators, FAM-006 branch docs, backlog/roadmap source truth, and runtime proof manifests.
Approval-Boundary Audit: The approved boundary excludes recording runtime, Overlay Profile UI, provider expansion, FAM-007 work, release execution, issue mutation, and broad theme or installer work.
Future-Gated Items: Future-gated items remain Overlay Profile runtime, Recording Profile runtime, tray recording, provider/model work, external telemetry, bulk packs, alert rules, and historical data.
Workstream Seam Map: Seam sequence is Branch Readiness Stage 2 repair setup -> Repair Workstream implementation -> Hardening H1 -> refreshed Live Validation / UTS -> PR Readiness, with validation checkpoints at each transition.
Proof Expectations: Proof expectations include validators, helper fixtures, screenshot evidence, user test handoff, compile validation, live-client manifest evidence, and later returned USER UTS digest.
Risk Forecast: Risks include stale main governance overlap, shallow branch planning, proof-only UI artifacts, lost draft state, source classification drift, and release-note overclaiming.
Recommendations And Alternatives: Recommend preserving the bounded close-guard repair; alternative broader UI redesign or provider work should remain future-gated because it raises risk.
Plan Version / Revision Status: Plan v4 is implemented for returned LV1 interactive-control reliability and visual-affordance repair; Hardening H1 remains pending.
Plan-To-Implementation Traceability: Planned deltas are compared with implementation by matching each approved repair item to concrete HUD CSS/HTML/JS changes, desktop renderer proof helper fields, validator markers, refreshed UTS wording, and live self-QA proof. Implemented deltas trace to the returned USER LV1/UTS feedback about missing hover lighting, intermittent first-click failures, Manage Monitors close/selection unreliability, Polling Floor copy, native-looking Polling dropdown, the active-client focused proof root `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_085500_741`, HUD interactable CSS/HTML/JS, desktop renderer proof helpers, validator updates, and refreshed UTS instructions.

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

Live Validation Stage 1 ends only after returned USER UTS failures are repaired and revalidated, or explicitly WAIVED with reason, and that result is digested into source truth. The current branch contains the original Monitor Groups runtime flow plus admitted Sensor Command Center repairs for visible resize-proof contamination, compact monitor selection, right-side detail editing, final delete/empty state, Sensor Library / Source Picker scale, source classification cleanup, first-launch flicker, compact dropdown controls, close-while-dirty queued action proof through the real Manage Monitors close target, Manage Monitors screenshot-sequence proof, and directly supporting validators.

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

Interactive Control Visual QA Critique Loop: `USER review of the refreshed LV1 focused empty-state screenshot returned REPAIR because the UI still displays SAVE MONITOR and CANCEL when no monitor exists, the buttons stretch into oversized vertical pills, Create Monitor is not the primary empty-state recovery action, and the empty-state copy reads like internal QA language. This setup admits the rule that every user-facing interactable must pass code inspection and focused visual inspection before Live Validation can pass.`

Dashboard Right-Edge Rediscovery Critique Loop: `Refreshed LV1 real-client validation stopped after Dashboard initial right-edge proof and corner resize proof passed. The active blocker is post-corner right-edge resize cursor rediscovery near the visible edge before the right-edge resize action. Manage Monitors focused proof states remain pending recheck because the run stopped first on the Dashboard rediscovery blocker.`

Historical Repair Trigger Marker: `returned USER UTS FAIL` - preserved for source-truth validator traceability; active state is refreshed LV1 automated/live helper evidence green after right-edge rediscovery H1 PASS, with returned USER UTS results pending.

USER Decision Ledger: `USER approved Branch Readiness Stage 2 repair setup and bounded Repair Workstream implementation for the refreshed LV1 close-guard and visual-proof blocker after prior H1 PASS, approved the interactive-control visual QA repair path, approved Branch Readiness Stage 2 repair setup for the Dashboard right-edge resize rediscovery blocker, approved the bounded Dashboard right-edge rediscovery Repair Workstream implementation after PR #169 reconciliation, and approved/run Hardening H1. Returned USER UTS result, GitHub issue #127 mutation, PR creation, merge, release execution, raw evidence handling, Overlay Profile runtime, Recording Profile runtime, provider expansion, FAM-007 work, AI Product work, and NDAI-wide Theme/Skins remain pending USER decisions.`

Full Feature Element Breakdown: `Sensor Command Center shell; compact action-light monitor list; row/icon selection; right-side detail panel; detail-pane Delete action; Save / Discard / Cancel guard for unsaved changes; final-monitor delete; true empty state with Create reachable; Sensor Library / Source Picker replacing basic dropdown/checklist assignment; Warning Notifications as settings checkbox outside sensor assignment; Provider Readiness as readiness/status/future capability outside assignable sources; source breadcrumbs using provider > device > category > metric > instance; source status metadata; scalable search plus dropdown/facets; large fixture proof; Overlay Profile planning; Recording Profile planning; validation and UTS proof hooks.`

System Concept Model: `Sensor Library exposes available or planned data sources; monitors are configured tracked items; Monitor Groups organize monitor collections; Overlay Profiles later choose visible monitors and layout; Recording Profiles later choose monitors or sensors to log. This branch repairs the Monitor Groups management surface and proof gates while preserving other concepts as future-gated boundaries.`

Entity / Profile Model: `Sensor Library = all available or planned data sources; Monitor = one configured tracked item; Monitor Group = organization/configuration collection; Overlay Profile = selected monitors plus layout visible on overlay; Recording Profile = selected monitors or sensors logged to file. A monitor may later be enabled, visible, recorded, warning-enabled, or hidden independently.`

User Workflow Model: `USER opens Dashboard, opens Monitor Groups / Manage Monitors, scans compact monitor rows, selects a monitor by row/icon click, edits the right-side detail pane, gets a Save / Discard / Cancel guard before losing unsaved edits, creates monitors from the command surface, deletes from the detail pane with confirmation including the final monitor, reaches a true empty state with Create still available, searches/facets Sensor Library sources, and sees Warning Notifications / Provider Readiness outside assignable sensor rows. The repair also requires Dashboard move/resize proof without visible proof artifacts in the product UI.`

Scale / Data Volume Model: `Manage Monitors must feel like a scalable Sensor Command Center, not a compact modal. It must scale to 100+ monitors and 1,000+ sources using compact rows, source search, dropdown/facets, grouped/statused results, Nexus-styled controls, and fixture validation. The UI must handle duplicate names, long names, deferred sources, missing sources, and source classification without requiring every monitor/source to be visible at once.`

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

Acceptance Criteria: `Sensor Command Center lists monitors compactly without row-level Edit/Delete buttons; row/icon click selects and opens details; detail-pane Delete asks for confirmation and can delete the final monitor; empty state is truthful and Create remains reachable; unsaved monitor changes are protected by Save / Discard / Cancel before switching; Sensor Library / Source Picker replaces basic dropdown/checklist assignment; Warning Notifications is a setting checkbox outside sensor assignment; Provider Readiness is readiness/status/future capability outside assignable sources; source rows show provider > device > category > metric > instance breadcrumbs and status metadata; dropdown/facets cover supported categories; visible proof-only resize artifacts are rejected in normal user-facing validation; source truth distinguishes Sensor Library, Monitor, Monitor Group, Overlay Profile, and Recording Profile; no Overlay Profile runtime, Recording Profile runtime, Overlay display acceptance, tray recording controls, export/share behavior, templates/import/export, backup/restore, or app-wide theme work is implied.`

Expected User-Facing Outcomes: `After repair implementation and revalidation, the USER should see Dashboard movement/resizing without visible validation artifacts, plus a Manage Monitors / Sensor Command Center surface that feels scalable, action-light, Nexus-styled, and usable with large monitor/source inventories. PR Readiness remains unavailable until those outcomes are proven or explicitly waived.`

Validation Proof Requirements: `Static HUD validator, internal sandbox validator, branch governance validation, release body validation, compileall, and later runtime-specific Monitor Groups proof beyond marker presence. Validators must reject proof-only visible artifacts in normal user-facing resize/move validation; prove shrink/grow during-drag behavior before mouse release using invisible/test-gated real UI frame, screenshot, pixel-signature, or equivalent evidence; prove post-corner right-edge rediscovery after prior resize actions; prove 100+ monitors, 1,000+ sources, duplicate names, long names, deferred sources, missing sources, warning state classification, and non-assignable readiness/settings classification; distinguish Monitor Group, Overlay Profile, and Recording Profile concepts without requiring runtime recording controls before separate USER admission.`

Screenshot / Live / User Test Summary Proof Requirements: `Runtime implementation should provide user-visible proof of list/create/edit/delete/confirm/sensor assignment behavior, then Hardening and Live Validation should use the real USER-facing launcher/shortcut path and a compact UTS handoff if USER-facing behavior is changed. Refreshed LV1 must first clear the Dashboard right-edge rediscovery blocker with real-client proof after corner resize; after that, proof must include screenshot-sequence or video-style evidence for Manage Monitors open state, Source Filter dropdown open/hover/reset, unsaved guard with close queued, Save / Discard / Cancel close outcomes, delete confirmation, final empty state, and 20+ / 100+ monitor-list scrollbar behavior. Full-desktop screenshots are locator/context evidence only; acceptance-critical UI states require focused local proof. Dashboard-only screenshots are insufficient for Manage Monitors acceptance-critical states.`

Implementation Sequence Proposal: `Remove or test-gate visible resize proof artifacts; convert Manage Monitors to compact Sensor Command Center list/detail behavior; implement unsaved-change guard; allow final-delete empty state; replace source checklist/dropdown filtering with Nexus source picker/facets; remove Warning Notifications and Provider Readiness from assignable sensors; add breadcrumbs/status metadata; update validators/helpers/UTS; run Workstream validation; then request Hardening.`

Deferred Ideas / Future Package Ledger: `Templates, monitor list import/export, full app backup/restore through base NCP settings architecture, bulk packs, recommended packs, alert/rule engine, historical sensor data, Overlay Profile runtime, Recording Profile runtime, tray recording controls, local recording output, export/share actions, provider expansion, Overlay acceptance, external telemetry parity, FAM-007 runtime work, AI Product work, and NDAI-wide Theme/Skins are deferred future packages or separately gated work. They must not be implemented by this repair setup.`

Planning Blockers: `Returned Refreshed USER UTS FAIL`; `Refreshed Live Validation / UTS Recheck Pending`; `Overlay Profile Runtime Approval Missing`; `Recording Profile Runtime Approval Missing`; `Tray Recording Controls Approval Missing`; `Export/Share Runtime Approval Missing`; `Overlay Acceptance Approval Missing`; `Provider/Model/Memory/Shortcut/Installer Approval Missing`; `External Telemetry Parity Approval Missing`; `AI Product Contract Import Approval Missing`; `PR Creation Approval Missing`.

USER Decisions Needed: `Approve Hardening H1 after repair; approve refreshed Live Validation / UTS recheck after green H1; approve GitHub issue #127 mutation if desired; return refreshed UTS results or explicit waiver with reason after Live Validation; approve PR creation later; approve merge later; approve release/artifacts/raw evidence/branch cleanup separately; approve templates/import/export, full backup/restore, Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, Overlay acceptance, FAM-007, provider/model/memory/shortcut/installer, external telemetry, or AI Product work separately.`

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

Planning Completion Waiver: `Not required - required product/system/profile/workflow/scale/state planning fields are recorded for this branch-local Stage 2 repair setup.`

User Test Summary Strategy: `No UTS is generated during Branch Readiness Stage 2 setup. The compact UTS handoff remains a Live Validation Stage 1 artifact. The current active-client LV1 returned REPAIR before a green USER handoff because unsaved_close_queued_action=false and Manage Monitors visual proof was missing, so PR Readiness remains blocked until repair implementation, Hardening, refreshed Live Validation / UTS recheck, and returned USER result are PASS or explicitly waived with reason and digested.`

## Returned UTS FAIL Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2`

Current-Main Reconciliation Confirmation: `current-main reconciliation is complete through PR #169 / origin/main 6e2e743fd1d8d688c8046eb0a788b1a7109e66c2; incoming governance, validation-suite, and worktree-rebaseline-audit helper truth is preserved as context while FAM-006 Monitor Groups / Sensor Command Center remains this worktree's branch-local identity. Final commit/push evidence belongs to the reconciliation packet.`

Returned UTS Scope Admitted: `Returned UTS Steps 1-8 passed; Step 9 failed Dashboard resize/move smoothness, especially shrink behavior where rendering appears frozen until resize completes; Step 10 failed Manage Monitors design/scalability because the scrollbar appears native Windows styled and the flow does not scale to hundreds of monitors and thousands of data sources.`

Resize/Move Repair Scope: `Dashboard resize/move live render smoothness; shrink and grow resize visual continuity; during-drag frame, pixel-signature, or video-style proof before mouse release; proof must show the Dashboard renders during drag rather than only after mouse release.`

Manage Monitors Repair Scope: `Manage Monitors scalable split layout; Nexus-styled scrollbars in child windows, monitor list, detail pane, sensor tree, sensor result list, and sensor preview/details pane; large-monitor and large-source fixtures for hundreds of monitors and thousands of data sources; searchable/filterable Sensor Library scale requirements already admitted in source truth.`

Profile Boundary Preservation: `Monitor Groups remain organization/configuration only. Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, provider expansion, Overlay acceptance, FAM-007 work, AI Product work, and NDAI-wide Theme/Skins remain pending USER decisions.`

Validator Planning Update: `Directly supporting validators must prove shrink and grow resize continuity, during-drag render evidence before mouse release, Nexus-styled scrollbar usage in Manage Monitors panes, and large fixture behavior beyond marker-only proof.`

PR Readiness Blocker State: `PR Readiness remains blocked pending Hardening H1 for the implemented repair, refreshed Live Validation, and returned USER UTS PASS or explicit waiver with reason digested into source truth. Historical setup phrase preserved for validator traceability: PR Readiness remains blocked pending repair implementation.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to removing visible resize-proof contamination, adding invisible/test-gated grow/shrink during-drag proof, implementing the Sensor Command Center compact monitor list/detail-pane repair, adding final-monitor delete and true empty state, replacing basic dropdown/checklist source assignment with Nexus Sensor Library / Source Picker search/facets, classifying Warning Notifications and Provider Readiness outside assignable sensors, adding breadcrumbs/status metadata, updating validators/helpers/UTS, validation, commit, and push.`

## Returned Refreshed UTS FAIL Sensor Command Center Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2`

Returned Refreshed UTS Classification: `REPAIR REQUIRED - Step 9 visible resize/move artifact is a blocking user-facing validation contamination bug; Step 3/4 Manage Monitors still behaves like a compact modal with row buttons; Step 6 final monitor delete is blocked; Step 8 basic/native dropdown behavior fails Nexus UI expectations; Warning Notifications and Provider Readiness are misclassified as assignable source/data-source items.`

Visible Resize-Proof Contamination Setup: `Admit repair to remove or test-gate normal-user-visible CSS monitoring-hud__chrome::after proof layer, JS --monitoring-hud-live-resize-proof-* visual effects, native monitoringHudResizeProofOverlay, and any helper/debug overlay or proof marker that appears in normal user-facing validation. Normal Dashboard move/resize must not show proof-only bands, overlays, masks, or glow artifacts.`

Invisible / Test-Gated Resize Proof Setup: `Resize proof must use invisible/test-gated real UI frame, screenshot, pixel-signature, geometry, or equivalent evidence. Validators must prove shrink and grow during-drag behavior before mouse release while rejecting proof-only visible artifacts in normal user-facing validation.`

Sensor Command Center Setup: `Manage Monitors remains a split layout but becomes a Sensor Command Center: compact action-light monitor list, row/icon selection, right-side detail panel, detail-pane Delete, Save / Discard / Cancel guard for unsaved changes, final-monitor delete, true empty state with Create still reachable, and large-fixture proof for 100+ monitors.`

Sensor Library / Source Picker Setup: `Replace basic dropdown/checklist assignment with Sensor Library / Source Picker behavior: scalable search plus dropdown/facets; categories for CPU, GPU, Memory, Disk, Network, Temperature, Load, Clock, Power, Fan, Voltage, Supported, Deferred, Missing, and Warning where source truth supports them; source rows with provider > device > category > metric > instance breadcrumbs; and source status metadata for supported, deferred, missing, warning, and provider-required states.`

Sensor / Source Classification Setup: `Warning Notifications classified as a monitor/settings checkbox outside sensor assignment. Provider Readiness classified as readiness/status/future capability outside assignable sources. Supported runtime-capable sources remain assignable; provider-required, deferred, missing, warning, readiness, and settings entries must not be over-credited as assignable sensors.`

Dropdown Repair And Proof Setup: `Current native/basic dropdown controls in Monitor Groups / Sensor Library are admitted for repair or replacement with Nexus-styled dropdown/facet controls. Proof must cover open, hover, close, reopen, keyboard/mouse selection, and visual style using video, frame-sequence, screenshot sequence, or equivalent visual evidence.`

Large Fixture / Edge Case Proof Setup: `Direct validators/helpers must prove 100+ monitors, 1,000+ sources, duplicate source names, long monitor names, long source names, deferred sources, missing sources, source classification, true empty state, final delete, unsaved-change guard, and no proof-only visible artifacts during normal user-facing resize/move validation.`

Profile Boundary Preservation: `Sensor Library = all available or planned data sources; Monitor = one configured tracked item; Monitor Group = organization/configuration collection; Overlay Profile = selected monitors plus layout visible on overlay; Recording Profile = selected monitors or sensors logged to file. Monitor Groups do not own overlay visibility, recording selection, recording output, Overlay Profile runtime, or Recording Profile runtime.`

Future Workflow Preservation: `Monitor-first, sensor-first, and group-first workflows remain future planning unless directly needed for this repair. Templates, import/export, bulk packs, recommended packs, alert/rule engine, historical data, Overlay Profile runtime, Recording Profile runtime, tray recording, local CSV/JSON/manifest recording output, event markers, auto-record triggers, rolling buffer capture, full app backup/restore, and base NCP settings architecture remain pending USER decisions.`

PR Readiness Blocker State: `PR Readiness remains blocked pending Hardening, refreshed Live Validation / UTS recheck, and returned USER UTS PASS or explicit waiver with reason digested into source truth.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to removing visible resize-proof contamination, adding invisible/test-gated grow/shrink during-drag proof, implementing the Sensor Command Center compact monitor list/detail-pane repair, adding final-monitor delete and true empty state, replacing basic dropdown/checklist source assignment with Nexus Sensor Library / Source Picker search/facets, classifying Warning Notifications and Provider Readiness outside assignable sensors, adding breadcrumbs/status metadata, updating validators/helpers/UTS, validation, commit, and push.`

## Returned UTS FAIL Repair Workstream Implementation

Repair Implementation Status: `COMPLETE - corrected returned refreshed UTS FAIL repair implementation committed and pushed at 7c88b94896232103dbdc7a61ac0e3a6417bbbfaf; Hardening H1 added proof-strength repairs and is green.`

Resize/Move Runtime Repair: `Implemented. Normal user-facing Dashboard move/resize no longer shows proof bands, debug tint, native proof overlay, or proof-only graphics. CSS proof visuals are gated behind explicit test-visible mode; JS resize proof stores invisible real-UI frame/pixel-signature markers; native monitoringHudResizeProofOverlay stays hidden/transparent in normal validation.`

During-Drag Proof Repair: `Implemented. Live helper proof records invisible/test-gated grow and shrink evidence through real UI frame/pixel-signature/geometry markers and rejects proof-only visible artifacts during normal user-facing validation.`

Manage Monitors Runtime Repair: `Implemented. Manage Monitors is a compact Sensor Command Center with action-light monitor rows, row/icon selection, right-side detail panel, detail-pane Delete, Save / Discard / Cancel guard, final-monitor delete, true empty state, and Create recovery.`

Sensor Library Runtime Repair: `Implemented. Sensor assignment uses Nexus Sensor Library / Source Picker search and facets rather than a native dropdown/checklist; source rows expose provider > device > category > metric > instance breadcrumbs, metadata/status, supported assignment, and disabled provider-required/deferred/missing/warning states. Warning Notifications is a monitor/settings checkbox and Provider Readiness is readiness/status/future capability outside assignable sources.`

Large Fixture Repair: `Runtime support now includes a 125-monitor fixture path and 1,200-source Sensor Library fixture proof path through window.setMonitoringHudLargeFixtureMode, monitoringHudLargeMonitorFixtureCount, and monitoringHudLargeSensorFixtureCount, including duplicate and long source-name cases. The fixture path is validation/support only and does not imply bulk creation, recommended packs, provider expansion, historical sensor data, alert/rule engine, recording runtime, or Overlay Profile runtime approval.`

Nexus Scrollbar Repair: `Nexus-styled scrollbar treatment is applied to child windows, the monitor list pane, selected-monitor detail pane, sensor result list, sensor settings pane, and sensor preview/details pane. Native-looking scrollbar regressions remain in scope for Hardening and Live Validation verification.`

UTS Handoff Refresh: `The compact User Test Summary handoff now separates resize proof contamination, Sensor Command Center layout, final-delete empty state, Sensor Library scale/scrollbar review, source picker visuals, classification cleanup, Dashboard resize/move smoothness, and Dashboard control regressions so returned USER results can distinguish repaired findings.`

PR Readiness Blocker State: `PR Readiness remains blocked until refreshed Live Validation/UTS PASS or explicit USER waiver with reason is digested.`

## Returned Refreshed UTS FAIL Repair Hardening H1

Hardening Status: `GREEN - H1 found a proof-strength gap in live self-QA coverage, then repaired helper/fixture proof for final-monitor delete, unsaved Save / Discard / Cancel, source-picker facets, source classification, duplicate/long source fixtures, and large monitor/source evidence. A later USER H1 addendum identified a functional unsaved-draft blocker and compact-control layout correction; this branch repaired the guard so draft edits remain visible and are saved/discarded/cancelled before queued selection/create/delete/close actions run, and Polling Floor/Search/Filter controls now use compact inline placement where practical.`

Resize/Render Proof Result: `PASS - normal Dashboard move/resize proof artifacts are hidden/test-gated; CSS monitoring-hud__chrome::after visible proof is allowed only in explicit test-visible mode; JS proof stores invisible real-UI frame/pixel-signature metadata; native monitoringHudResizeProofOverlay remains hidden and transparent in normal user-facing validation.`

Manage Monitors / Sensor Library Result: `PASS - live self-QA proves command-center layout, row actions removed, row selection opens detail, detail-pane delete, unsaved guard buttons and Save / Discard / Cancel behavior using changed draft values, queued create/delete/close actions behind the same guard, final-monitor delete empty state, Create recovery, source picker browser/facets, source breadcrumbs/metadata, supported/deferred classification, Provider Readiness outside assignable sources, and Warning Notifications as setting-only.`

Bounded H1 Repair: `Applied - strengthened desktop live self-QA proof, large-source fixture generation, compact inline bounded controls, and the unsaved-draft guard. No scope expansion into runtime recording, Overlay Profile runtime UI, tray recording, provider expansion, Overlay acceptance, app-wide themes/skins, base NCP settings architecture, or FAM-007 work.`

Nexus Scrollbar Result: `Nexus-styled scrollbar coverage remains required for child windows, monitor list, selected-monitor detail, sensor result list, sensor settings, and sensor preview/details panes.`

Planning Adequacy Preservation: `PR #157/#158 planning adequacy fields remain present: Planning Adequacy Review, Rejected Shallow Plan, Alternatives And Tradeoffs Reviewed, Whole-System Interaction Map, Minimum Viable vs Full System Boundary, and Open Questions / USER Decision Points.`

Hardening Validation Evidence: `powershell -NoProfile -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -RunInteractionSelfQA PASS after H1 addendum repair; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260515_141844_405; interaction manifest C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260515_141844_405\monitoring_hud_live_client_interaction_manifest.json; screenshot evidence root C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_monitoring_hud_live_validation\20260515_141844_405. The manifest records commandCenterLayout=true, rowActionsRemoved=true, rowSelectionOpensDetail=true, detailPaneDelete=true, unsavedGuardOpened=true, unsavedGuardButtons=true, unsavedCancelPreservedSelection=true, unsavedCancelPreservedDraft=true, unsavedDiscardSwitchedSelection=true, unsavedDiscardDroppedDraft=true, unsavedSaveSwitchedSelection=true, unsavedSavePersistedDraft=true, unsavedCreateQueuedAction=true, unsavedDeleteQueuedAction=true, unsavedCloseQueuedAction=true, finalMonitorDeleteEmptyState=true, finalMonitorCreateReachable=true, sourcePickerBrowser=true, sourceFilterFacets=true, sourceFilterReopen=true, sourceBreadcrumbMetadata=true, supportedSourcesAssignable=true, deferredSourcesDisabledExplained=true, warningNotificationsSettingOnly=true, providerReadinessNotAssignable=true, largeMonitorFixture=true, largeSourceFixture=true, and duplicateLongSourceFixture=true. UTS export skipped because UTS belongs to refreshed Live Validation Stage 1.`

PR Readiness Blocker State: `PR Readiness remains blocked until refreshed Live Validation / UTS recheck returns PASS, or an explicit USER waiver with reason is digested into source truth.`

## Refreshed LV1 Close-Guard Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2 after refreshed LV1 REPAIR`

Repair Implementation Status: `IMPLEMENTED - the active-client proof now targets data-child-window-close="monitor-group-edit", asserts dirty state and changed draft value before close, records close queued action proof, proves Save / Discard / Cancel close outcomes from visible draft values, and captures named Manage Monitors screenshot-sequence evidence for open state, Source Filter dropdown open/hover/reset, unsaved close guard, close outcomes, delete confirmation, final empty state, and 100+ monitor / 1,200-source scrollbar behavior`

Repair Workstream Validation Evidence: `powershell -NoProfile -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -RunInteractionSelfQA -ProofSeam "FAM-006 refreshed LV1 close guard visual proof Repair Workstream" PASS; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260518_184424_564; interaction manifest C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260518_184424_564\monitoring_hud_live_client_interaction_manifest.json; screenshot sequence includes 03_manage_monitors_open_state, 04_source_filter_dropdown_open_hover_reset, 05_unsaved_guard_close_queued, 06_unsaved_close_cancel_preserves_draft, 07_unsaved_close_save_closes_after_persist, 08_unsaved_close_discard_closes_after_drop, 09_delete_confirmation_bottom, 10_final_empty_state_create_recovery, and 11_100_monitor_list_scrollbar_and_1200_source_picker; manifest booleans record unsavedCloseDirtyBeforeClose=true, unsavedCloseDraftBeforeClose=true, unsavedCloseTargetedManageClose=true, unsavedCloseQueuedAction=true, unsavedCloseCancelPreservedDraft=true, unsavedCloseSavePersistedDraft=true, and unsavedCloseDiscardDroppedDraft=true.`

Hardening H1 Visual QA Repair: `USER screenshot review proved a helper oversight: the prior PASS accepted full-desktop screenshots where Manage Monitors was too broad to review and did not fail visibly stretched/non-compact monitor-list rows. H1 now treats UI/UX proof as visual proof, not only DOM/code proof: Manage Monitors visual screenshots are captured as focused WebView evidence, the live helper requires visualProofQualityGate=true, and proof fails unless monitorListRowsCompact, monitorListCssPreventsStretch, and monitorListSmallSetHasSlack are true. Product CSS prevents small monitor lists from stretching rows to fill the pane by using align-content:start and grid-auto-rows:max-content on the monitor list.`

Hardening H1 Visual QA Evidence: `powershell -NoProfile -ExecutionPolicy Bypass -File dev\orin_monitoring_hud_live_validation.ps1 -RunInteractionSelfQA -ProofSeam "FAM-006 close guard visual proof Hardening H1 visual QA repair" PASS; proof root C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260518_192645_731; interaction manifest C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260518_192645_731\monitoring_hud_live_client_interaction_manifest.json; focused WebView screenshots include 03_manage_monitors_open_state, 05_unsaved_guard_close_queued, and 11_100_monitor_list_scrollbar_and_1200_source_picker; manifest records visualProofQualityGate=true, monitorListRowsCompact=true, monitorListCssPreventsStretch=true, monitorListSmallSetHasSlack=true, and unsavedCloseQueuedAction=true.`

Refreshed LV1 Failure: `The active-client refreshed Live Validation manifest at C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260518_180025_205 recorded unsaved_close_queued_action=false. The Sensor Command Center proof otherwise passed command-center layout, row actions removed, row selection, detail-pane delete, final-monitor empty state, Source Filter dropdown, hover reset, Source Picker, source classification, large fixtures, Save / Discard / Create / Delete queued actions, and draft persistence.`

Close-While-Dirty Functional Blocker: `Manage Monitors close while dirty must route through the same Save / Discard / Cancel guard as selection, create, and delete. The close path must queue pendingMonitorAction="close"; Save must persist the visible draft first and then close; Discard must drop the visible draft and then close; Cancel must keep Manage Monitors open and preserve the visible draft.`

Close Proof Targeting Requirement: `Proof must assert dirty state and changed draft value before clicking close, must target data-child-window-close="monitor-group-edit" instead of a generic document.querySelector('[data-child-window-close]') selector, and must report the close guard pending action plus draft value before any queued action resolves.`

Visual-Proof Coverage Blocker: `The refreshed LV1 screenshot set captured Dashboard/home/travel states only. Refreshed LV1 proof must capture Manage Monitors UI states, including Manage Monitors open state, Source Filter dropdown open/hover/reset, unsaved guard while close is queued, Save / Discard / Cancel close outcomes, delete confirmation, final empty state, and 20+ / 100+ monitor-list scrollbar behavior. Proof artifacts must be named clearly enough for USER review and may use screenshot-sequence, video-style proof, or equivalent visual evidence.`

Preservation Requirements: `Preserve first-launch flicker guard, compact Source Filter dropdown and hover reset, 20+ / 100+ monitor-list stress behavior, lower detail danger-zone Delete placement, top toolbar compaction, taller/bounded-resizable Manage Monitors, Sensor Library pattern, Warning Notifications as a settings checkbox, Provider Readiness as readiness/status/future capability, and Sensor Library / Monitor / Monitor Group / Overlay Profile / Recording Profile boundaries.`

Validator Planning Updates: `Directly supporting validators retain existing Sensor Command Center checks and now require the specific Manage Monitors close target, dirty-state and changed-draft preconditions, Save / Discard / Cancel close outcome proof, and named Manage Monitors screenshot/video-style visual evidence labels. Hardening and refreshed Live Validation remain pending the next USER decisions.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to repairing the refreshed LV1 unsaved close-while-dirty failure and Manage Monitors visual-proof gap. Scope: ensure dirty Manage Monitors close queues pendingMonitorAction="close"; Save persists the visible draft then closes; Discard drops the draft then closes; Cancel keeps Manage Monitors open with the draft visible; update proof to target data-child-window-close="monitor-group-edit", assert dirty state and changed draft value before close, and record close queued action proof; add screenshot-sequence or video-style proof for Manage Monitors open state, Source Filter dropdown open/hover/reset, unsaved guard close-queue state, Save / Discard / Cancel close outcomes, delete confirmation, final empty state, and 20+ / 100+ list scrollbar behavior; preserve all existing FAM-006 Sensor Command Center repairs and profile boundaries; run validation; commit and push if green.`

## Refreshed LV1 Interactive Control Visual QA Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2 after refreshed LV1 interactive-control visual QA failure`

Refreshed LV1 Visual Failure Classification: `REPAIR REQUIRED - focused Manage Monitors empty-state screenshot proved a user-facing interactive control failure that the prior helper/validator over-credited. The empty state shows invalid SAVE MONITOR and CANCEL controls when no monitor exists, the buttons stretch into oversized vertical pills, Create Monitor is not the primary recovery action, the left rail repeats empty-state noise, and empty-state copy says "recover from an empty state" instead of product-facing language.`

Interactive Control Visual QA Gate: `All user-facing interactable controls must pass code inspection and focused visual inspection before Live Validation can pass. This includes buttons, user-facing dropdowns, checkboxes, selectable rows, search fields, filter controls, scrollbars, close controls, delete confirmations, empty-state actions, source-picker controls, and any other interface object the USER can click, type into, hover, focus, select, open, close, scroll, or activate.`

Code Inspection Requirement: `Each user-facing interactive object must have truthful enabled/disabled state, correct event routing, correct dirty-state and queued-action behavior, no stale selection/hover/focus state, valid empty-state logic, and no path that saves already-saved data when a visible draft exists. Code proof alone is insufficient for Live Validation acceptance.`

Focused Visual Inspection Requirement: `Each user-facing interactive object must have focused screenshot, frame-sequence, video-style, or equivalent visual proof for relevant normal, hover, focus, open, active, disabled, destructive, confirmation, empty, and error states where those states exist. Visual proof must be specific enough for USER review and must fail on stretched buttons, native/basic dropdown regression, clipping, overlap, contradictory controls, invalid empty-state actions, dead space that hides the primary action, unreadable copy, or proof artifacts visible in normal product UI.`

Empty-State Repair Scope: `When no monitor exists or no monitor is selected, Save Monitor and Cancel must not appear as valid actions, no action button may stretch into oversized vertical pills, Create Monitor must be the primary recovery action, empty-state copy must be concise and product-facing, duplicate left-rail empty-state noise must be removed or made non-conflicting, and the detail pane must not imply a draft can be saved when no monitor draft exists.`

Dropdown / Source Picker Visual Scope: `Source Filter and bounded dropdown controls remain valid only when Nexus-styled and visually proven for open, hover, move, select, close, reopen, keyboard/mouse behavior, stale-highlight clearing, disabled items, and no native/browser-looking regression. Source assignment must remain Sensor Library / Source Picker discovery and must not collapse back into a basic dropdown/checklist.`

Visual Proof Coverage Setup: `Refreshed LV1 and H1 must inspect focused Manage Monitors screenshots or video-style frames for open state, compact list rows, empty state, Create recovery, Save / Discard / Cancel guard, close control, delete confirmation, final delete, Source Filter dropdown open/hover/reset, source-picker rows, 20+ and 100+ list scrollbars, and large-source results. Broad desktop screenshots may provide context only and cannot satisfy acceptance-critical UI proof by themselves.`

Validator Planning Updates: `Directly supporting validators/helpers must reject manifest-only or DOM-only PASS when focused screenshots show invalid interactive controls. Validators must require visualProofQualityGate=true plus explicit focused visual QA coverage for interactive controls and must add an empty-state control sanity check that fails if Save Monitor / Cancel are visible when no monitor exists, if action buttons stretch into oversized pills, or if Create Monitor is not the primary recovery action.`

Immediate Repair Scope: `Repair the Manage Monitors empty-state action model and visual layout; enforce the code-plus-focused-visual QA gate for all user-facing interactive controls; update helpers/validators/UTS so the next H1/LV1 cannot miss obvious UI defects in focused proof screenshots. Preserve existing close-guard, Sensor Library, dropdown, first-launch flicker, scrollbars, source classification, and profile-boundary repairs.`

Future / Deferred Scope: `This setup does not authorize runtime recording, Overlay Profile runtime UI, Recording Profile runtime UI, tray recording controls, export/share behavior, provider expansion, Overlay acceptance, FAM-007 work, AI Product work, app-wide Theme/Skins, bulk creation, recommended packs, alert/rule engine, historical data, full app backup/restore, or base NCP settings architecture.`

PR Readiness Blocker State: `PR Readiness remains blocked until this interactive-control visual QA repair is implemented, hardened, refreshed Live Validation / UTS is green, and returned USER result is PASS or explicitly waived with reason and digested.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to repairing the refreshed LV1 interactive-control visual QA failure. Scope: remove invalid Save Monitor / Cancel actions from no-monitor and no-selection empty states; make Create Monitor the primary empty-state recovery action; prevent oversized/stretched action buttons; clean empty-state copy and redundant empty-state noise; add code-plus-focused-visual QA gates for all user-facing interactables including buttons, dropdowns, checkboxes, rows, search fields, filters, scrollbars, close controls, delete confirmations, empty-state actions, and source-picker controls; update helpers/validators/UTS so focused screenshots can fail obvious UI defects; preserve existing FAM-006 Sensor Command Center repairs and profile boundaries; run validation; commit and push if green.`

## Refreshed LV1 Interactive Control Visual QA Repair Implementation

Implementation Status: `COMPLETE - bounded Repair Workstream implementation for focused empty-state interactive-control failure; Hardening H1 pending`

Empty-State Repair Result: `The no-monitor Manage Monitors detail pane now presents product-facing copy ("No monitors yet" / "Create a monitor to assign sources and settings."), exposes Create Monitor as the primary empty-state action, hides the Save Monitor / Cancel detail footer when no selected monitor exists, and keeps the left rail empty copy short so the empty state does not read like QA recovery text.`

Button Sizing / Hierarchy Result: `Save Monitor and Cancel remain available only for selected-monitor edit/draft context and are hidden in the no-monitor empty state. Detail footer actions and empty-state actions are bounded to normal button height, align to content instead of stretching, and can fail validation if focused proof shows oversized vertical pills.`

Interactive-Control Visual QA Proof Result: `Runtime helper and validators now require emptyStateNoSaveCancel=true, emptyStateCreatePrimary=true, emptyStateActionsBounded=true, emptyStateProductCopy=true, and interactiveControlVisualQaGate=true in addition to visualProofQualityGate=true. Focused Manage Monitors proof must therefore reject a DOM/manifest PASS when the screenshot shows invalid empty-state actions, stretched buttons, or internal copy.`

Hardening H1 Proof-Target Repair: `Hardening H1 found a visual-proof helper defect rather than a product empty-state defect: the focused screenshot named 09_delete_confirmation_bottom could pass without actually showing the lower detail danger-zone Delete confirmation. The helper now scrolls the monitor-detail pane to the Delete confirmation, asserts deleteConfirmationState=open and deleteConfirmationVisualTargeted=true, and static validators require this targeted visual proof so future H1/LV1 cannot over-credit a mislabeled screenshot.`

UTS Handoff Update: `Step 6 now asks the USER to verify that final delete produces a true empty state with Create Monitor as the primary action and does not show Save Monitor / Cancel or oversized action buttons when no monitor exists. Formal UTS export remains refreshed Live Validation Stage 1 only.`

Preservation Result: `The implementation preserves first-launch flicker guard, compact Source Filter dropdown and hover reset, monitor-list stress proof, lower detail danger-zone Delete, top toolbar compaction, taller/bounded-resizable Manage Monitors, dirty close guard with pendingMonitorAction="close", Save / Discard / Cancel draft-state behavior, Sensor Library / Source Picker, Warning Notifications as a settings checkbox, Provider Readiness as readiness/status, and Sensor Library / Monitor / Monitor Group / Overlay Profile / Recording Profile separation.`

## Refreshed LV1 Dashboard Right-Edge Rediscovery Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2 after refreshed LV1 real-client right-edge rediscovery failure`

Refreshed LV1 Failure Classification: `REPAIR REQUIRED - real USER-facing shortcut/client validation passed initial Dashboard right-edge hit-test, initial right-edge cursor transition, and corner resize proof, then failed post-corner right-edge resize cursor rediscovery before dashboard_mouse_resize_right_edge. This is a Dashboard resize discoverability blocker, not a Manage Monitors implementation blocker.`

Known Passing Evidence: `Initial right-edge hit-test passed with rightEdge10px=htright; initial right-edge transition passed with rightOutside=True / htright / size-west-east / offset=1; corner resize passed and changed the Dashboard from 780x1060 to 860x1130.`

Right-Edge Rediscovery Setup: `Repair scope is post-corner right-edge rediscovery after prior resize actions. The repair must reacquire the Dashboard element, native/root handle, bounding rect, DPI/scale context, virtual desktop bounds, and visible-edge coordinates after each resize action before attempting the next right-edge proof.`

Diagnostic Sweep Planning: `When right-edge discovery fails, proof must record x/y sample coordinates, offset from visible edge, cursor kind, native hit-test result, root/window handle at point, expected Dashboard handle, bounding rect, virtual desktop bounds, timing, and settle state. Failure evidence must identify whether the miss is product cursor behavior, proof coordinates, visible-edge targeting, hit-zone sizing, DPI/scale interaction, rounded-mask state, or helper timing.`

Post-Resize Settle Planning: `Before post-resize rediscovery, validation must prove geometry stable, rounded mask applied, WebView visible, active resize state cleared, and cursor reset. The helper must not continue with stale Dashboard handles or stale pre-resize edge coordinates after a corner resize.`

Validator Planning Updates: `Directly supporting validators must require post-resize right-edge rediscovery planning, diagnostic sweep evidence, and post-resize settle criteria. Runtime proof must cover right-edge, bottom-edge, corner resize, cursor transitions, visible-edge discoverability, and post-corner right-edge rediscovery while preserving the 14px visible-rail discipline unless diagnostics prove a bounded product edge-math adjustment is required.`

Manage Monitors Pending LV1 States: `Manage Monitors focused LV1 states remain pending recheck after the Dashboard blocker clears: empty state, delete confirmation bottom placement, Source Filter dropdown/hover reset, monitor-list visual quality, unsaved close guard, and Sensor Command Center preservation.`

Preservation Requirements: `Preserve corner resize proof, bottom-edge proof, move fluidity, rounded-corner mask, first-launch flicker guard, focused visual proof quality, compact Source Filter dropdown, hover reset, dirty close guard, Sensor Library pattern, Warning Notifications as a settings checkbox, Provider Readiness as readiness/status/future capability, and Sensor Library / Monitor / Monitor Group / Overlay Profile / Recording Profile boundaries.`

Immediate Repair Scope: `Repair setup only. Runtime implementation is not authorized by this Stage 2 setup. The next implementation may update Dashboard resize helper/runtime proof code and directly supporting validators/source truth only as needed for right-edge rediscovery. It must not expand into Manage Monitors implementation, provider expansion, Overlay Profile runtime, Recording Profile runtime, tray recording, release execution, GitHub issue mutation, branch cleanup, FAM-007, AI Product, app-wide theme/skin work, or base NCP settings architecture.`

PR Readiness Blocker State: `PR Readiness remains blocked until right-edge rediscovery repair implementation, Hardening H1, refreshed Live Validation / UTS recheck, and returned USER result are PASS or explicitly waived with reason and digested.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to repairing the refreshed LV1 Dashboard right-edge resize cursor rediscovery failure. Scope: reacquire the Dashboard element, native/root handle, bounding rect, DPI/scale context, virtual desktop bounds, and visible-edge coordinates after each resize action; add diagnostic sweep evidence for x/y samples, offset from visible edge, cursor kind, native hit-test, root/window handle at point, expected Dashboard handle, bounding rect, virtual desktop bounds, timing, rounded-mask state, and settle state; add post-resize settle checks for stable geometry, applied rounded mask, visible WebView, cleared active resize state, and cursor reset; repair product hit-zone math or helper targeting/timing only if diagnostics prove the cause; preserve the 14px visible rail unless bounded evidence requires adjustment; preserve corner resize, bottom-edge resize, move fluidity, first-launch flicker guard, focused visual proof quality, and all existing Sensor Command Center repairs; update directly supporting validators/helpers/source truth/UTS; run validation; commit and push if green.`

## Dashboard Right-Edge Rediscovery Repair Workstream Implementation

Repair Implementation Status: `IMPLEMENTED - bounded Dashboard right-edge rediscovery proof-path repair pending Hardening H1`

Reacquisition Repair: `The human-client helper now reacquires the Dashboard UI element, native/root handle, bounding rect, DPI/scale context, virtual desktop bounds, and visible-edge coordinates after resize actions before attempting post-resize cursor rediscovery. The post-corner right-edge proof no longer reuses the pre-corner native handle or stale edge coordinates.`

Post-Resize Settle Criteria: `The helper requires post-resize geometry stability, rounded-mask continuity, visible Dashboard/WebView basis, cleared active resize state by stable geometry after mouse-up, and cursor reset before rediscovery. The post-corner right-edge check records dashboard_post_resize_settle_before_right_edge before dashboard_right_edge_rediscovery_after_corner_resize.`

Diagnostic Sweep Evidence: `On rediscovery failure the helper records diagnosticSamples containing x/y sample coordinates, offsetFromVisibleEdgePx, cursorKind, nativeHitTest, rootWindowHandleAtPoint, expectedDashboardHandle, rootMatchesExpectedDashboard, elapsedMs, Dashboard context, virtualDesktopBounds, visibleEdgeCoordinates, DPI/scale, and postResizeSettle evidence. The right-edge rediscovery step now also records focusedDashboardScreenshot and focusedRightEdgeScreenshot so acceptance-critical resize proof is local and reviewable; full-desktop screenshots are locator/context only and cannot satisfy the proof gate by themselves.`

Product Behavior vs Proof-Path Finding: `No Dashboard product edge-math or 14px visible-rail runtime behavior was changed in this implementation. The repair selection is proof-path handle/coordinate/timing reacquisition unless diagnostic evidence later proves product edge behavior needs a bounded adjustment. Interior cursor points remain disallowed as false-green proof because rediscovery still requires htright and offset within the visible rail.`

Right-Edge Rediscovery Repair: `The post-corner right-edge rediscovery proof now fails with a classification of helper targeting/timing, coordinate/DPI mismatch, handle/root mismatch, timing/settle mismatch, or product cursor behavior, and passes only when the reacquired Dashboard handle and visible-edge coordinates produce a real htright resize cursor near the visible edge before mouse down.`

Validation Preservation: `Corner resize, right-edge geometry resize, bottom-edge resize, grow/shrink during-drag visual proof, move fluidity, rounded-corner mask proof, first-launch flicker guard, focused visual proof quality, and Sensor Command Center repairs remain preserved. The human-client proof now passed through the real USER-facing shortcut path at dev\logs\fam_006_human_client_validation\20260519_065444_031 with post-corner right-edge rediscovery offset=1, cursor=size-west-east, hitTest=htright, matching reacquired Dashboard handle/root state, and focused local Dashboard/right-edge crops.`

Manage Monitors Pending LV1 States: `Empty state, delete confirmation bottom placement, Source Filter dropdown/hover reset, monitor-list visual quality, unsaved close guard, and Sensor Command Center preservation remain pending refreshed LV1 recheck after the Dashboard right-edge blocker clears.`

Next Legal Phase After Implementation: `Superseded - Hardening H1 is green; refreshed LV1 automated/live helper evidence is green and returned USER UTS results are pending.`

## Implemented vs Deferred Digest For Refreshed UTS

Implemented In This Branch: `Sensor Command Center compact list/detail layout`; `row/icon selection`; `detail-pane Delete`; `Save / Discard / Cancel guard that preserves draft edits until resolved`; `queued selection/create/delete/close actions behind the unsaved guard`; `final-monitor delete with true empty state and Create recovery`; `empty-state Create Monitor primary action`; `no Save Monitor / Cancel footer in no-monitor empty state`; `bounded action button sizing proof`; `product-facing empty-state copy`; `code-plus-focused-visual QA gate for user-facing interactables`; `Sensor Library / Source Picker source discovery`; `search plus faceted filters`; `source breadcrumbs and status metadata`; `Warning Notifications as monitor/settings checkbox`; `Provider Readiness as readiness/status/future capability`; `Nexus-styled source picker/dropdown/facet controls`; `compact inline Polling Floor row`; `Search and Filter controls on the same Source Picker toolbar row where practical`; `invisible/test-gated resize proof without normal UI proof artifacts`; `large monitor/source fixture proof including duplicate and long source names`.

Valid UTS Critique Targets Now: `Whether the inline Polling Floor/Search/Filter layout feels compact enough`; `whether the unsaved guard correctly saves changed draft values before switching, discards draft values before switching, and preserves visible drafts on Cancel`; `whether create/delete/close actions are blocked by the same guard while dirty`; `whether the Sensor Library source discovery still feels scalable and Nexus-styled`; `whether visible resize proof artifacts are absent in normal user-facing validation`.

Returned USER Video / Written Repair Candidates: `ADMITTED for Branch Readiness repair setup after PR #163 current-main reconciliation - first-launch Dashboard flicker regression; Source Filter should become a Nexus-styled dropdown menu rather than bulky exposed chips; dropdown open/hover state must clear the previous hovered item; left monitor-group list needs 20+ group stress proof with NDAI scrollbar styling; Delete Selected Monitor should move to the lower right/bottom area with delete confirmation near the bottom; top toolbar/search/create area consumes too much vertical space and should be redesigned without collapsing source discovery back into a basic dropdown/checklist; Manage Monitors should be somewhat resizable and taller by default; copy such as "for this monitor group" should be removed where current selection already provides context.`

Preserved Implemented FAM-006 Work After PR #162 Reconciliation: `Draft-preserving Save / Discard / Cancel guard; queued selection/create/delete/close actions behind the guard; Sensor Library / Source Picker pattern; Warning Notifications as a setting checkbox; Provider Readiness as readiness/status/future capability; Sensor Library, Monitor, Monitor Group, Overlay Profile, and Recording Profile concept separation.`

Current-Main Reconciliation Identity Guard: `During PR #163 reconciliation, origin/main no-active-main and FAM-007 merged-unreleased truth are treated as source-truth context only. Docs/feature_backlog.md, Docs/prebeta_roadmap.md, and Docs/branch_records/index.md must preserve this branch as the active branch-local FAM-006 authority before validation and commit.`

Returned USER Repair Setup Scope: `Admit repair planning/setup for first-launch Dashboard flicker; Source Filter as a compact Nexus-styled dropdown menu; dropdown open/hover reset so prior item highlight clears; 20+ monitor-group left-list stress fixture with NDAI scrollbar styling; bottom/right Delete Selected Monitor placement and bottom delete confirmation; compacted Manage Monitors top controls without collapsing Sensor Library source discovery into a basic dropdown/checklist; taller default Manage Monitors window and bounded resizability; copy cleanup for redundant phrasing; preservation of draft guard / queued actions / Sensor Library / Warning Notifications setting / Provider Readiness classification / profile model separation.`

Returned USER Repair Setup Non-Includes: `Runtime implementation before USER approval`; `FAM-007 work`; `Governance branch mutation`; `neutral main mutation`; `release execution`; `GitHub issue closeout`; `branch/worktree cleanup`; `runtime recording`; `Overlay Profile runtime`; `Recording Profile runtime`; `tray recording controls`; `provider/model/memory/shortcut/installer work`; `Overlay acceptance`; `external telemetry`; `AI Product work`.

Deferred / Not Implemented In This Branch: `Runtime recording`; `Overlay Profile runtime UI`; `Recording Profile runtime UI`; `tray recording controls`; `local CSV/JSON/manifest recording output`; `export/share/import behavior`; `provider SDK/model/runtime expansion`; `Overlay acceptance`; `bulk creation`; `recommended packs`; `alert/rule engine`; `historical sensor data`; `full app backup/restore`; `base NCP settings architecture`; `NDAI-wide themes/skins`; `FAM-007 work`; `AI Product work`.

## Refreshed LV1 Interactive-Control Reliability And Visual-Affordance Repair Setup Admission

Repair Setup Status: `ADMITTED - Branch Readiness Stage 2 after returned LV1 interactive-control reliability and visual-affordance failure`

Returned LV1 Failure Classification: `REPAIR REQUIRED - USER reported that Dashboard and Manage Monitors clickable controls such as Close, Create, Save, Cancel, Delete, dirty-guard actions, Source Filter, and Polling controls do not consistently light up on hover; monitor row hover is more visible than the rest of the control system; intermittent first-click reliability failures occur when switching monitors and closing Manage Monitors; Polling Floor copy remains wrong and the Polling dropdown still appears native/basic rather than Nexus/NDAI styled. This is a user-facing functional and visual-affordance blocker, not a PR Readiness-ready state.`

Interactable Visual Affordance Setup: `missing hover, active, focus, and click affordance coverage is admitted for all current FAM-006 Dashboard and Manage Monitors user-facing interactables. Required surfaces include Dashboard close / settings / warning / hub actions; Manage Monitors close controls; Create Monitor; Save Monitor; Cancel; Save / Discard / Cancel dirty-guard actions; Delete Selected Monitor; delete confirmation Delete / Cancel; monitor row selection; Source Filter dropdown; Polling Rate dropdown; Source Picker controls where current UI exposes them; and any current FAM-006 Dashboard or Manage Monitors user-facing clickable control surfaced by validators.`

Visual-State Planning: `Each applicable interactable must be planned for normal, hover, active / pressed, focus-visible, disabled, open, selected, and warning/error state proof where the control supports that state. Focused visual proof must show the state change, not only final static layout.`

First-Click Reliability Setup: `Intermittent first-click reliability is admitted as a functional blocker. Repeated first-click stress proof must cover close, row switch, create, save, cancel, discard, delete confirm, delete cancel, Source Filter open/select/close, Polling Rate open/select/close, Dashboard settings/warning/hub actions, and Dashboard close. Stress coverage must run after re-render, dirty guard, delete confirmation, dropdown-open, post-close/reopen, and post-render states so stale DOM, timing, focus, or overlay interception cannot be hidden by a single scripted pass.`

Click Interception Investigation Plan: `Repair implementation must inspect and, if needed, diagnose z-index / overlay interception, pointer-events, disabled state or stale aria state, stale DOM references, focus trap, debounce / timing guard, transition or animation timing, re-render state after guard / delete confirmation / dropdown close, child-window close routing, Manage Monitors focus ownership, and any overlay layer that can intercept first-click events.`

Polling Rate Dropdown Setup: `Polling Floor copy repair to Polling Rate is admitted. The Polling Rate dropdown visual repair must preserve dropdowns for bounded choices, render Polling Rate as a compact Nexus-styled bounded control, align bounded dropdown controls inline or right-side where practical, prove open/hover/active/focus/selected/close/reopen behavior, and preserve Sensor Library / Source Picker as source discovery. Source assignment must not collapse into a basic dropdown/checklist.`

Visual Proof Planning Updates: `focused screenshots, frame-sequence, or video-style proof must cover every acceptance-critical interactable and must be named clearly enough for USER review. Proof must include normal, hover, active, focus-visible, disabled, open, selected, and destructive/confirmation states where applicable. Full-desktop screenshots remain locator/context evidence only and cannot satisfy acceptance-critical UI proof by themselves. Static screenshot proof and repeated first-click stress proof must both be represented where applicable.`

Validator Planning Updates: `Directly supporting validators/helpers must require code inspection, focused visual state proof, and repeated first-click stress proof for user-facing controls. Validators must reject manifest-only or DOM-only PASS when hover/active/focus visual states are missing, when a native/basic dropdown is visible, when Polling Floor copy remains, when a first click is missed or intercepted, when stale hover/focus/selected state persists, or when post-render / dirty-guard / delete-confirmation / dropdown-open state causes close or monitor-switch clicks to fail.`

Preservation Requirements: `Preserve Dashboard resize repair path, right-edge rediscovery proof path, first-launch flicker guard, Sensor Command Center layout, Source Filter dropdown and hover reset, 20+ / 100+ monitor-list stress behavior, delete placement and bottom confirmation, dirty close guard and pendingMonitorAction close behavior, Warning Notifications as a settings checkbox, Provider Readiness as readiness/status/future capability, and Sensor Library / Monitor / Monitor Group / Overlay Profile / Recording Profile boundaries.`

Immediate Repair Scope: `Repair setup only. Runtime implementation is not authorized by this Stage 2 setup. The next implementation may update FAM-006 HUD CSS/HTML/JS, proof helpers, validators, UTS wording, and directly supporting source truth only as needed for interactive-control visual affordance, first-click reliability, click-interception diagnostics, Polling Rate copy, and Polling Rate Nexus-styled bounded dropdown repair.`

Future / Deferred Scope: `This setup does not authorize app-wide Theme/Skins work, base NCP settings architecture, runtime recording, Overlay Profile runtime UI, Recording Profile runtime UI, tray recording controls, export/share behavior, provider/model/memory/shortcut/installer work, Overlay acceptance, external telemetry parity, FAM-007 work, AI Product work, full app backup/restore, release execution, PR creation, issue mutation, artifact upload, raw evidence handling, or branch/worktree cleanup.`

PR Readiness Blocker State: `PR Readiness remains blocked until interactive-control reliability / visual-affordance repair implementation, Hardening H1, refreshed LV1 / UTS recheck, and returned USER result are PASS or explicitly waived with reason and digested.`

Next Repair Workstream Approval Text: `Approve Repair Workstream implementation for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006, limited to repairing the returned LV1 interactive-control reliability and visual-affordance failure. Scope: add visible Nexus hover, active, focus-visible, disabled, open, selected, and click affordance states for every current FAM-006 Dashboard and Manage Monitors user-facing interactable; repair intermittent first-click reliability for close, monitor switching, create, save, cancel, discard, delete confirmation, Source Filter, Polling Rate, Dashboard settings/warning/hub actions, and Dashboard close; add repeated first-click stress proof after re-render, dirty guard, delete confirmation, dropdown-open, post-close/reopen, and post-render states; investigate and repair z-index, pointer-events, stale aria/disabled state, stale DOM, focus trap, timing, transition, child-window close routing, and Manage Monitors focus ownership issues only where diagnostics prove them; rename Polling Floor to Polling Rate; implement Polling Rate as a compact Nexus-styled bounded dropdown; preserve Sensor Library / Source Picker source discovery and all existing FAM-006 Sensor Command Center, Dashboard resize, source classification, and profile-boundary repairs; update directly supporting validators/helpers/source truth/UTS; run required validation; commit and push if validation is green.`

## Refreshed LV1 Interactive-Control Reliability And Visual-Affordance Repair Implementation

Repair Implementation Status: `IMPLEMENTED - bounded Workstream repair for returned LV1 interactive-control reliability and visual-affordance failure; Hardening H1 remains pending.`

Interactable Visual Affordance Repair: `HUD CSS/HTML/JS now define Nexus visual affordance states for current FAM-006 Dashboard and Manage Monitors interactables: normal, hover, active / pressed, focus-visible, disabled, open, selected, and destructive/confirmation states where applicable. The repair covers Dashboard Close, Settings, Warning Notifications, Create Monitor, Manage Monitors, Manage Monitors child-window Close, Create, Save Monitor, Cancel, dirty-guard Save / Discard / Cancel, Delete Selected Monitor, delete confirmation Delete / Cancel, monitor row selection, Source Filter dropdown, Polling Rate dropdown, Source Picker rows, display-mode chips, search fields, checkboxes, and bounded dropdown controls.`

First-Click Reliability Repair: `Runtime now routes current Dashboard and Manage Monitors click targets through a reliable activation layer with pointerdown/pressed state recording, pointerup/click de-duplication, target identity tracking, and first-click proof data. Repeated first-click stress proof covers close, row switch, create, save, cancel, discard, delete confirm/cancel, Source Filter open/select/close, Polling Rate open/select/close, Dashboard settings/warning/hub actions, Dashboard close, and post-render states after re-render, dirty guard, delete confirmation, dropdown-open, post-close/reopen, and post-render flows.`

Click Interception Diagnostics Repair: `Runtime records z-index, pointer-events, disabled / aria-disabled state, target rect, center point, elementFromPoint/intercepting element, and target/child match proof for relevant controls. This keeps first-click reliability from passing when an overlay, stale state, disabled control, or focus/timing issue intercepts the intended target.`

Polling Rate Dropdown Repair: `Polling Floor user-facing copy is removed from the product surface and replaced with Polling Rate. The monitor Polling Rate control is now a compact Nexus-styled bounded dropdown with a hidden state proxy select for compatibility, explicit open / hover / selected option states, inline placement, and Source Library / Source Picker separation preserved.`

Visual Proof Updates: `Focused WebView proof helpers now include Polling Rate dropdown open/hover/reset proof in addition to Manage Monitors open state, Source Filter dropdown open/hover/reset, dirty close guard, Save / Discard / Cancel close outcomes, delete confirmation, final empty state, and 100+ monitor / 1,200 source list proof. Full-desktop screenshots remain locator/context evidence only.`

UTS Handoff Update: `The compact UTS handoff must ask the USER to verify that Dashboard and Manage Monitors buttons, dropdowns, checkboxes, selectable rows, close controls, and destructive confirmation controls visibly light up on hover/focus/active states; first clicks reliably work during normal, dirty-guard, delete-confirmation, dropdown-open, and post-render states; and Polling Rate reads and behaves as a Nexus-styled bounded dropdown.`

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
- Save / Discard / Cancel guard for unsaved edits when switching monitors, creating a monitor, deleting a monitor, or closing Manage Monitors; Save persists the current draft before the queued action, Discard drops the draft before the queued action, and Cancel keeps the user on the current monitor with the draft visible.
- Final-monitor delete with true empty state and Create still reachable.
- Sensor Library / Source Picker for available runtime-capable monitor inputs.
- Compact inline bounded controls where practical, including Polling Floor as a label/control row and Source Picker Search plus Filter on the same toolbar row.
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
- Implementation Admission Status: `Prior USER-approved returned refreshed UTS FAIL repair implementation is complete and H1 is green; refreshed LV1 close-guard and visual-proof repair implementation is complete and pending Hardening H1.`

## Backlog Completion Strategy

Branch Completion Goal: `Complete the FAM-006 Monitor Groups sensor-configuration runtime flow through implementation, Hardening, Live Validation, PR Readiness, merge, and later release handling after each phase receives USER approval.`

Known Future-Dependent Blockers: `Refreshed Live Validation / UTS recheck, PR creation, merge, release execution, artifacts, raw evidence handling, future branch/worktree cleanup after this branch closes, FAM-007 work, provider/model/memory/shortcut/installer work, Overlay acceptance, external telemetry parity, AI Product work, templates/import/export, full app backup/restore, base NCP settings architecture, and app-wide Theme/Skins all require later USER approval.`

Branch Closure Rule: `Stop after this Repair Workstream implementation validation, commit, and push; continue only after USER explicitly approves Hardening H1 for the refreshed LV1 close-guard and visual-proof repair.`

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

Runtime Summary: `The initial Manage Monitors runtime delivered created monitor rows, in-window Create Monitor, row-level Edit/Delete, selected-monitor settings, supported sensor/data-source assignment, and provider-required unavailable states. The corrected runtime implementation removes row-level Edit/Delete, replaces checklist/dropdown assignment with Sensor Library / Source Picker facets, classifies Warning Notifications as a setting, classifies Provider Readiness as readiness/future capability, and is now hardened green.`

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

Live Validation Status: `REPAIR - returned USER LV1/UTS interactive-control reliability and visual-affordance failure admitted for Stage 2 setup`

Live Validation Summary: `Refreshed Live Validation Stage 1 after right-edge H1 PASS launched through the real USER-facing shortcut/client path and produced supporting automated/live helper evidence, but returned USER results identified a new interactive-control reliability and visual-affordance failure. Dashboard and Manage Monitors controls need visible hover/active/focus/click affordances, first-click stress reliability, click-interception diagnosis, Polling Floor copy repair to Polling Rate, and Polling Rate Nexus-styled bounded dropdown repair. PR Readiness remains blocked until this repair is implemented, hardened, refreshed LV1/UTS is green, and returned USER result is PASS or explicitly waived with reason and digested.`

Real USER-Facing Shortcut Proof: `PASS - dev/logs/fam_006_human_client_validation/20260519_072954_644/human_client_manifest.json`

Shortcut Alignment: `PASS - the canonical red FAM-006 desktop shortcut targets C:\Nexus Worktrees\FAM-006\launch_orin_desktop.vbs with working directory C:\Nexus Worktrees\FAM-006`

Active-Client UTS Handoff Proof: `PASS - dev/logs/fam_006_monitoring_hud_live_validation/20260519_072533_350`

Formal UTS Handoff Path: `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

Formal UTS Handoff Status: `RETURNED REPAIR - interactive-control reliability and visual-affordance failure admitted for Branch Readiness Stage 2 setup`

Focused Visual Proof Path: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_072533_350\live_client_interaction`

Focused Visual Proof Result: `PASS - focused proof includes 03_manage_monitors_open_state.png, 04_source_filter_dropdown_open_hover_reset.png, 05_unsaved_guard_close_queued.png, 09_delete_confirmation_bottom.png, 10_final_empty_state_create_recovery.png, and 11_100_monitor_list_scrollbar_and_1200_source_picker.png; manifest records visualProofQualityGate=true and interactiveControlVisualQaGate=true.`

Dashboard Resize Preservation Result: `PASS - real-client proof records post-corner right-edge rediscovery at offset=1, cursor=size-west-east, hitTest=htright, matching reacquired handle/root, right-edge geometry resize, bottom-edge/corner preservation, grow/shrink proof, move fluidity, rounded-corner mask, first-launch stability, and focused local Dashboard/right-edge crops.`

Sensor Command Center Result: `PASS - manifest records commandCenterLayout=true, rowActionsRemoved=true, rowSelectionOpensDetail=true, detailPaneDelete=true, finalMonitorDeleteEmptyState=true, sourceFilterDropdown=true, sourceFilterHoverReset=true, sourcePickerBrowser=true, warningNotificationsSettingOnly=true, providerReadinessNotAssignable=true, monitorListRowsCompact=true, monitorListCssPreventsStretch=true, monitorListSmallSetHasSlack=true, unsavedCloseQueuedAction=true, unsavedCloseTargetedManageClose=true, unsavedCloseSavePersistedDraft=true, unsavedCloseDiscardDroppedDraft=true, and unsavedCloseCancelPreservedDraft=true.`

Live Validation Repair Files: `desktop/desktop_renderer.py`; `dev/orin_monitoring_hud_human_client_validation.ps1`; `dev/orin_monitoring_hud_live_validation.ps1`; `dev/orin_monitoring_hud_surface_validation.py`; `dev/orin_monitoring_hud_internal_sandbox_validation.py`; `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`; `Docs/feature_backlog.md`; `Docs/prebeta_roadmap.md`.

## Expected Seam Families And Risk Classes

Seam Families: `Sensor Command Center management UI`; `compact monitor selection`; `right-side detail editing`; `final delete and empty state`; `Sensor Library / Source Picker`; `source classification`; `Dashboard resize/move proof isolation`; `validator and proof hardening`; `source-truth governance`.

Risk Classes: `visible validation contamination in product UI`; `dead-end Monitor Groups controls`; `fake sensor/data-source availability`; `settings/readiness items misclassified as sensors`; `delete without confirmation`; `blocked final delete`; `native/basic dropdown regression`; `Overlay/display scope creep`; `app-wide Theme/Skins scope creep`; `FAM-007/provider/model bleed`; `marker-only proof`.

## Codex Live Client Self-QA

Codex Live Client Self-QA: PASS

Live Client Entry Path: `C:\Nexus Worktrees\FAM-006\launch_orin_desktop.vbs`

Evidence Screenshot: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_072533_350\live_client_interaction\03_manage_monitors_open_state.png`

Visual Quality: `PASS - focused/local screenshots are used for acceptance-critical Manage Monitors and Dashboard resize states; full-desktop captures are locator/context only.`

Interaction Manifest: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_072533_350\monitoring_hud_live_client_interaction_manifest.json`

Interaction Evidence Root: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_072533_350\live_client_interaction`

Live Interaction Evidence: `PASS - Dashboard resize preservation, Source Filter dropdown, hover reset, unsaved close guard, delete confirmation, empty state, 100+ monitor list, and 1,200-source Sensor Library proof all passed.`

Usability Check: `PASS - Create primary empty state, bounded Save/Cancel/Delete controls, compact monitor rows, bottom delete confirmation, and product-facing copy remain visually reviewable.`

Interaction Check: `PASS - manifest records unsavedCloseQueuedAction=true, unsavedCloseSavePersistedDraft=true, unsavedCloseDiscardDroppedDraft=true, unsavedCloseCancelPreservedDraft=true, sourceFilterHoverReset=true, and sourceFilterReopen=true.`

Platform Uniformity Check: `PASS - Nexus/NDAI styled dropdowns, scrollbars, buttons, and child-window controls are preserved in focused proof.`

NDAI Naming Check: `PASS - Sensor Library, Monitor, Monitor Group, Overlay Profile, and Recording Profile remain distinct source-truth concepts.`

Cleanup Check: `PASS - no raw evidence upload, release, issue mutation, PR creation, or cross-worktree cleanup was performed.`

## User Test Summary Strategy

User Test Summary Strategy: `Branch Readiness Stage 2 setup does not export a new formal UTS. The returned LV1/UTS failure is recorded as repair input; the next Repair Workstream implementation and Hardening H1 must update helpers/validators/UTS wording as needed so refreshed Live Validation Stage 1 can retest interactive-control hover/active/focus/click affordance, repeated first-click reliability, Polling Rate copy/dropdown behavior, and preservation of existing FAM-006 Sensor Command Center repairs.`

## User Test Summary

Automated validators and live helper evidence: SUPPORTING ONLY - superseded by returned USER REPAIR findings.

User-Facing Shortcut Validation: PASS

User-Facing Shortcut Path: `C:\Nexus Worktrees\FAM-006\launch_orin_desktop.vbs`

User Test Summary Results: FAIL.

Final phase advancement is BLOCKED until the returned interactive-control reliability and visual-affordance failure is repaired, hardened, refreshed LV1/UTS passes or is waived with reason, and blockers are reevaluated.

User Test Summary Handoff Path: `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

User Test Summary Proof Root: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_072533_350`

User Test Summary User-Inspectable Screenshot Folder: `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_monitoring_hud_live_validation\20260519_072533_350`

User Test Summary Returned Failure Digest: `Dashboard and Manage Monitors clickable controls need visible hover/active/focus/click affordance states; intermittent first-click failures affect monitor switching and close controls; close can become unreliable after Manage Monitors state changes; full stress testing is required for clickable interfaces; Polling Floor must be renamed Polling Rate; Polling Rate dropdown must be Nexus-styled rather than native/basic.`

## Later-Phase Expectations

- Prior Hardening H1 is complete for the previous repair implementation and the Dashboard right-edge rediscovery H1 is green.
- Refreshed Live Validation Stage 1 launched through the real USER-facing shortcut/client path and produced supporting proof, but returned USER findings require interactive-control reliability and visual-affordance repair before PR Readiness.
- PR Readiness, PR creation, merge, release execution, artifacts, raw evidence handling, branch cleanup, Overlay acceptance, FAM-007 work, provider/model/memory/shortcut/installer work, external telemetry parity, and AI Product work remain separate USER decisions.

## Initial Workstream Seam Sequence

Seam 1: `Monitor Groups management flow and sensor-configuration design/implementation`

Goal: `Repair the Monitor Groups manage/edit flow into a scalable Sensor Command Center so users can select compact monitor rows, edit details safely, delete from the detail pane including the final monitor, and assign supported sources through a searchable/faceted Sensor Library without leaving the manage/edit context.`

Scope: `Dashboard Monitor Groups management UI, child-window flow, compact list state, row/icon selection, detail-pane editing and Delete, Save / Discard / Cancel guard, final-delete empty state, Sensor Library / Source Picker assignment truth, per-sensor settings where supported, invisible/test-gated resize proof, and validators.`

Non-Includes: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, artifacts, raw evidence handling, and future branch/worktree cleanup after this branch closes.`

## Active Seam

Active seam: `Branch Readiness Stage 2 repair setup for returned LV1 interactive-control reliability and visual-affordance failure`

Active Seam Status: `green`

Next active seam: `Repair Workstream implementation for interactive-control visual affordance, first-click reliability, click-interception diagnostics, Polling Rate copy, and Polling Rate Nexus dropdown repair.`

## Backlog Completion Status

Backlog Completion State: `Implemented Complete`

Remaining Implementable Work: `None`

Future-Dependent Blockers: `None`

Completion Status: `green`

## Seam Continuation Decision

Seam Status: `green`

Slice Status: `green`

Completion Status: `green`

Waiver Status: `None`

Continue Decision: `stop`

Continuation Execution Latch: `Closed until USER approves Hardening H1`

Stop Basis: `workstream green`

Next Active Seam: `Hardening H1 for implemented returned LV1 interactive-control reliability and visual-affordance repair`

Stop Condition: `Hardening H1 requires explicit USER approval`

Continuation Action: `Stop at phase boundary until USER admits the next phase: bounded Hardening H1 for the implemented repair`

Single-Seam Workstream Waiver: `None`

Single-Seam Or Single-Slice Waiver Authority: `USER only; Codex cannot infer single-seam or single-slice Workstream authority`

Single-Seam Or Single-Slice Workstream Blocker: `One seam or one slice visible in the Workstream plan is a blocker unless a USER waiver is recorded`

Bounded Seam Default: `Bounded means one active seam at a time, not one-seam Workstream authority; same-branch continuation is required until Workstream Completion Status is Green`

## Blockers

Returned LV1 interactive-control reliability and visual-affordance repair is implemented but not hardened. PR Readiness remains blocked until the repair is hardened, refreshed LV1/UTS passes or is explicitly waived with reason, and blockers are reevaluated. PR creation, merge, release execution, raw evidence handling, FAM-007 scope, provider/model/memory/shortcut/installer work, Overlay Profile runtime, Recording Profile runtime, tray recording controls, export/share behavior, Overlay acceptance, external telemetry parity, and AI Product work remain pending USER decisions for later phases.

## Exit Criteria

- Current-main reconciliation preserves current main truth and the FAM-006 branch-local Sensor Command Center work.
- Refreshed LV1 close-guard, visual-proof, interactive-control visual QA, and right-edge rediscovery repairs are preserved; returned USER findings now require Hardening H1 for the implemented interactive-control reliability and visual-affordance repair.
- Previously implemented draft guard, queued actions, Sensor Library pattern, Warning Notifications setting checkbox, Provider Readiness readiness/status classification, and profile-model separation are preserved.
- Existing Dashboard settings, close, warning notifications, tray-owned HUD control, resize/scroll/source-truth boundaries are preserved as regression requirements.
- FAM-006 v1.7.1-prebeta release closure remains green.
- FAM-006 released issue closeout posture is preserved.
- Directly supporting validators pass.
- PR Readiness remains blocked until returned LV1 interactive-control reliability and visual-affordance repair is hardened, refreshed LV1/UTS is green or waived with reason, and blockers are reevaluated.
- Required validation passes.
- Dashboard right-edge rediscovery Repair Workstream implementation and H1 are validated and pushed; current returned LV1 blocker is interactive-control reliability and visual-affordance repair.

## Rollback Target

`Branch Readiness`

Rollback is the unmerged Workstream implementation on this branch only if USER later decides to abandon this carrier before PR/merge. Do not delete or mutate other FAM-006, FAM-007, Governance, or main worktrees as part of rollback.

## Next Legal Phase

`Hardening`

USER decision to approve Hardening H1 for the implemented returned LV1 interactive-control reliability and visual-affordance repair on `feature/fam-006-monitor-groups-sensor-configuration`.

## Next Legal Phase Digest

Current Phase: `Repair Workstream implementation`

Next Legal Phase: `Hardening H1`

Why This Phase Is Next: `Returned USER LV1/UTS findings exposed missing hover/active/focus/click affordances, intermittent first-click reliability failures, Polling Floor naming, and native/basic Polling dropdown behavior. The bounded runtime/helper/source-truth repair is implemented; Hardening H1 is required before refreshed LV1/UTS can resume.`

Approval Required: `USER approval for Hardening H1.`

Exact USER Approval Text: `Approve Hardening H1 for feature/fam-006-monitor-groups-sensor-configuration in C:\Nexus Worktrees\FAM-006 after the returned LV1 interactive-control reliability and visual-affordance repair implementation. Scope: verify the implementation commit is present; pressure-test Dashboard and Manage Monitors hover, active, focus-visible, disabled, open, selected, and click affordance states; pressure-test repeated first-click reliability for close, monitor switching, create, save, cancel, discard, delete confirmation, Source Filter, Polling Rate, Dashboard settings/warning/hub actions, and Dashboard close; pressure-test click-interception diagnostics after re-render, dirty guard, delete confirmation, dropdown-open, post-close/reopen, and post-render states; verify Polling Floor was renamed to Polling Rate; verify Polling Rate is a compact Nexus-styled bounded dropdown; preserve Sensor Library / Source Picker, Dashboard resize repairs, source classification, profile boundaries, and Runtime Branch Engineering Contract fields; apply bounded H1 repairs if defects are found; run required validation; commit and push if validation is green.`

Allowed Scope: `FAM-006 Dashboard and Manage Monitors interactive-control visual affordance, first-click reliability, click-interception diagnostics, Polling Rate copy/dropdown repair, and directly supporting validators/helpers/UTS/source-truth updates only.`

Explicit Exclusions: `HUD Overlay visual display acceptance, Overlay customization, app-wide Theme/Skins, FAM-007, provider/model/memory/shortcut/installer work, external telemetry parity, AI Product work, PR creation, merge, release execution, tags, GitHub Releases, artifacts, raw evidence upload/import/linking, Governance branch mutation, neutral main mutation, and future branch/worktree cleanup after this branch closes.`

Validation Required: `git status --short --branch; git fetch origin --prune; git rev-parse HEAD; git rev-parse origin/main; git worktree list; git diff --check; git diff --check origin/main...HEAD; python dev\orin_monitoring_hud_surface_validation.py; python dev\orin_monitoring_hud_internal_sandbox_validation.py; python dev\orin_branch_governance_validation.py; python dev\orin_release_body_validation.py; python -m compileall -q dev desktop Audio main.py.`

Stop Conditions: `Stop if branch/worktree identity mismatches C:\Nexus Worktrees\FAM-006 / feature/fam-006-monitor-groups-sensor-configuration, origin/main movement creates required reconciliation, implementation requires excluded Overlay/FAM-007/provider/model/installer/AI Product/release/PR/raw-evidence scope, Sensor Command Center and profile-model boundaries cannot be preserved together, validation fails, or another USER decision is required.`
