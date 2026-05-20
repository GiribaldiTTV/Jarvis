# Nexus Feature Backlog

This file is the controlled registry for tracked work, deferred planning items, historical implemented items, and future promoted bug identities.

Rules:

- ideas must not be implemented immediately
- ideas must not silently expand current scope
- backlog identity remains controlled and approval-gated
- `Status` is the delivery or work field
- `Record State` is the canonical-record lifecycle field
- `Priority` is the primary backlog selection signal for open candidate work
- `Target Version` is not an open-backlog selection field and must not be used to rank, select, defer, or skip open backlog candidates
- open `Registry-only` and active `Promoted` entries should not carry `Target Version`; release target truth is assigned later through roadmap, workstream, PR Readiness, and Release Readiness governance when release-bearing work exists
- closed, released, implemented, or release-debt entries may preserve `Target Version` as historical release evidence
- if `Status` is `Deferred`, the entry must also state `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:` so next-workstream selection can evaluate it without guessing
- allowed `Record State` values are `Registry-only`, `Promoted`, and `Closed`
- if `Record State` is not `Registry-only`, `Canonical Workstream Doc` must exist
- backlog entries keep the short registry story, not the full execution story

Record-state meaning:

- `Registry-only` = tracked identity only; no canonical workstream execution record is required yet
- `Promoted` = canonical workstream doc required and used as the durable execution and traceability record while the lane is active
- `Closed` = canonical workstream doc remains stable historical lane truth after closure

Backlog-identity guardrails:

- feature backlog items default to user-facing feature families
- Codex must not create, split, promote, or select a backlog identity without explicit USER approval
- if that approval is absent, stop on `Backlog Addition User Approval Missing` and output the still-not-closed FAM list plus every not-complete package and slice; if the list is empty, stop on `Backlog Exhaustion User Decision Pending`
- a separate backlog identity for non-user-facing runtime, developer-tooling, docs/governance, or canon-only work requires explicit USER approval and a rationale that branch/workstream traceability is insufficient
- continuation, blocker-clearing, or validation follow-through on an existing feature family should stay inside that same backlog identity by default; do not mint a new backlog item unless the USER explicitly approves a backlog split or the work is materially a new user-facing feature family
- small single-seam runtime proofs, governance repairs, validation follow-through, and blocker-clearing traces are family evidence or branch/workstream history by default, not standalone release-version drivers
- canonical workstream docs and branch authority records own multi-slice, multi-branch, and repair-traceability history for one backlog identity; backlog IDs should not fragment that history by default
- the old `FB-###` namespace is historical-only after this one-time repair; new live backlog-family identities use `FAM-###`, starting at `FAM-001`, and Codex must not create or reuse a parseable `FB-###` backlog ID
- backlog-family registry sections must keep parseable `### [ID: FAM-XXX]` records only for true feature-family backlog entries; historical pass aliases, support/governance lanes, and old registry-only implemented records are trace tables, not backlog items
- entries within the live feature-family registry must be kept in ascending `FAM-XXX` order so the fresh namespace remains simple and conflict-free

Historical note:

- older implemented entries may preserve older Nexus-era titles as historical identity
- those preserved titles are not current runtime-path claims
- older entries may also preserve earlier backlog-admission behavior that split docs/governance work or same-family continuation into separate backlog identities
- preserve that history for traceability, but do not treat it as the default backlog model going forward

## Promoted Canonical Workstreams

- `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
- `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md`
- `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md`
- `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md`

## Active Promoted Workstream

None.

## Current Decision Surface

Latest Public Prerelease Recorded In Source Truth: `v1.7.8-prebeta`
Post-Release Canon Closure Drift: Recorded in current main as release-window source-truth context; PR #178 repairs the v1.7.8-prebeta release-window source truth and does not replace this worktree's branch-local FAM-006 identity.
Published Release Pending Canon Closure: `None for current public release; v1.7.8-prebeta source truth is closed in current main. PR #177 FAM-007 provider path and consent readiness plus PR #178 release-window source-truth repair are current-main context only; FAM-006 branch-local identity remains Monitor Groups / Sensor Command Center.`
Merged-Unreleased PRs: None for current main after `v1.7.8-prebeta`; PR #177 FAM-007 provider path and consent readiness and PR #178 release-window source-truth repair are released/current-main context only, while this FAM-006 branch remains unmerged branch-local work.
Current-Main Reconciliation Update: `origin/main` is reconciled through `2bd54f0e34c6759e9618f42d104d80b975ecc1c3`; PR #178 release-window source-truth repair, PR #177 FAM-007 provider path/consent readiness, and PR #174 through PR #176 governance/worktree-safety truth are context only, and FAM-006 branch-local authority remains `feature/fam-006-monitor-groups-sensor-configuration`.
Active Runtime Branch: Branch-local FAM-006 runtime carrier `feature/fam-006-monitor-groups-sensor-configuration` in `C:\Nexus Worktrees\FAM-006`; origin/main remains context.
Active Governance Branch: `feature/release-readiness-source-truth-intake` in `C:\Nexus Worktrees\Governance`.
Selected-Next Posture: Branch-local FAM-006 refreshed Live Validation / UTS review after bounded action-row, Source Picker checkmark, dirty-delete, and Manage Monitors Close hitbox repairs; successor selection remains USER-gated.
Release Blockers: None for `v1.7.8-prebeta` current-main tag context; current-main release-window posture remains Governance context, and FAM-006 PR Readiness remains blocked until returned USER UTS is PASS or USER gives an explicit waiver with reason.
Next Legal Phase: FAM-006 returned USER UTS digest for the automated refreshed LV1 PASS handoff; release execution, issue work, branch cleanup, FAM-007 work, and successor selection remain separate USER decisions.

FB-044 Boot-to-desktop handoff outcome refinement and FB-045 Active-session relaunch outcome refinement are Released / Closed historical proof through `v1.6.9-prebeta`; FB-046 Active-session relaunch reacquisition and settled re-entry proof is Released / Closed historical proof through `v1.6.10-prebeta`; FB-047 Active-session relaunch decline session-preservation proof is Released / Closed historical proof through `v1.6.11-prebeta`; FB-048 Active-session relaunch signal-failure and wait-timeout truth is Released / Closed historical proof through `v1.6.12-prebeta`; latest public prerelease truth is `v1.7.8-prebeta`; FAM-006 Monitoring HUD Dashboard Product Surface is released historical traceability in `v1.7.0-prebeta`, the FAM-006 Dashboard issue-resolution/settings-panel release window plus FAM-007 provider-boundary/no-provider shell support note are released in `v1.7.1-prebeta`, the PR #152 FAM-007 local AI foundation continuation plus release-governance support through PR #154 are released in `v1.7.2-prebeta`, PR #155 through PR #161 are released in `v1.7.3-prebeta`, PR #162 plus PR #163 are released in `v1.7.4-prebeta`, PR #164 through PR #168 are released in `v1.7.5-prebeta`, PR #170 FAM-007 provider activation foundation is released/context in `v1.7.6-prebeta`, PR #171 Branch Runtime Engineering Plan governance and PR #172 FAM-007 execution-readiness gates are released in `v1.7.7-prebeta`, and PR #173 through PR #178 are current main release-window/source-truth context at `v1.7.8-prebeta` only for this FAM-006 branch. The backlog-family governance reform package, automation-catalog package, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof remain released historical traceability; PR #108 is merged and released as FAM-004 historical proof after watcher-verified merge proof; PR #109 is merged historical FAM-003 legacy FB-027 family evidence for shutdown-hotkey availability/direct-shutdown validation, with visible confirmation owned by tray Exit only, and is not a standalone release-version driver.
Released baseline truth is aligned: FB-040 is released and closed in `v1.6.0-prebeta`, FB-031 is released and closed in `v1.6.1-prebeta`, FB-032 is released and closed in `v1.6.2-prebeta`, FB-004 is released and closed in `v1.6.3-prebeta`, FB-015 plus FB-029 are released and closed in `v1.6.4-prebeta`, FB-030 is released and closed in `v1.6.5-prebeta`, FB-005 is released and closed in `v1.6.6-prebeta`, FB-042 is released and closed in `v1.6.7-prebeta`, FB-043 is released and closed in `v1.6.8-prebeta`, FB-044 plus FB-045 are released and closed in `v1.6.9-prebeta`, FB-046 is released and closed in `v1.6.10-prebeta`, FB-047 is released and closed in `v1.6.11-prebeta`, FB-048 is released and closed in `v1.6.12-prebeta`, and the FAM-001 legacy FB-049 runtime proof plus FAM-004 legacy FB-030 runtime diagnostics proof are released historical traceability in `v1.6.13-prebeta`.
FB-039 is released and closed in `v1.5.0-prebeta`.
FB-038 remains released and closed in `v1.4.1-prebeta`.

## Current Branch Execution Posture

Released Historical Scope: FAM-006 Monitoring HUD Dashboard Product Surface released in v1.7.0-prebeta through PR #118; FAM-006 Dashboard render/layout hardening PR #129, Dashboard IA/control follow-through PR #132, Dashboard settings-panel runtime PR #142, and FAM-007 PR #138 provider-boundary / no-provider shell scaffold support released in v1.7.1-prebeta; FAM-007 PR #152 local AI foundation continuation plus governance/readiness support PRs #148, #149, #150, #151, #153, and #154 released in v1.7.2-prebeta; PR #155, PR #156, PR #157, PR #158, PR #159, PR #160, and PR #161 released in v1.7.3-prebeta; PR #162 FAM-007 local AI runtime contracts and capability foundation plus PR #163 post-PR162 closeout released in v1.7.4-prebeta; PR #164 Runtime Branch Engineering Contract governance, PR #165 FAM-007 provider-readiness/setup-eligibility, PR #166 Governance Intake RRI-20260519-001, PR #167 Governance Intake closeout, and PR #168 Governance standing branch closeout exemption released in v1.7.5-prebeta; PR #169 Governance Process Efficiency Reform and PR #170 FAM-007 Local AI Provider Activation Foundation released in v1.7.6-prebeta; PR #171 Branch Runtime Engineering Plan governance and PR #172 FAM-007 Local AI Provider Execution Readiness Gates released in v1.7.7-prebeta; PR #173 through PR #178 are current-main release-window/source-truth context for v1.7.8-prebeta and are not this FAM-006 branch identity; FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, merged governance/automation proof package, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta.
Repo State: Branch-local FAM-006 Monitor Groups / Sensor Command Center reconciliation on `feature/fam-006-monitor-groups-sensor-configuration` in `C:\Nexus Worktrees\FAM-006`; current `origin/main` through PR #178, PR #177 FAM-007 provider path/consent readiness truth, FAM-007 execution-readiness truth, v1.7.7 canon-closure drift truth, validation-suite/rebaseline-audit helper changes, worktree-slot / PR-watcher / governance-efficiency truth, and v1.7.8-prebeta release-window source truth are preserved as context, not branch identity.
Merged-Main Repo State Before Branch: Current main includes PR #170 FAM-007 provider activation foundation, PR #171 governance, PR #172 FAM-007 execution-readiness gates, PR #173 v1.7.7 canon-closure drift truth, PR #174 through PR #176 governance/worktree safety truth, PR #177 FAM-007 provider path and consent readiness, and PR #178 release-window source-truth repair, while this worktree remains the USER-approved FAM-006 runtime carrier.
Latest Public Prerelease: v1.7.8-prebeta.
Latest Public Release Commit: 2bd54f0e34c6759e9618f42d104d80b975ecc1c3.
Latest Public Prerelease Publication: https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.7.8-prebeta.
Latest Public Prerelease Title: Pre-Beta v1.7.8.
Post-PR #159 Source-Truth Drift: Closed by standing Governance intake RRI-20260515-003 through PR #160; stale PR Readiness / PR creation wording for the already-merged FAM-007 branch is removed before Release Readiness reruns.
Post-PR #162 Source-Truth Drift: Closed by PR #163 and the v1.7.4-prebeta release. PR #162 is released historical FAM-007 runtime-expansion scope.
Post-PR #165 Source-Truth Drift: Closed by PR #166 through PR #168 and the v1.7.5-prebeta release. PR #165 is released historical FAM-007 provider-readiness/setup-eligibility scope.
Post-PR #170 Source-Truth Drift: Closed by the Branch Readiness Stage 2 setup after the v1.7.6-prebeta release. PR #170 is released historical FAM-007 activation-foundation scope.
Post-PR #172 Source-Truth Drift: Closed by this Branch Readiness Stage 2 setup after the v1.7.7-prebeta release. PR #172 is released historical FAM-007 execution-readiness-gates scope.
Post-Release Canon Closure Drift: Recorded in current main and preserved here as context for this FAM-006 branch after PR #178 release-window source-truth repair.
Published Release Pending Canon Closure: None for current public release; preserved as current-main context only for this FAM-006 branch.
Closure Repair Surface: Current-main context only for this FAM-006 branch.
Closure Drift Scope: release-dependent fields only.
Implementation Entry: FAM-006 bounded runtime/helper/source-truth repairs are implemented, H1 Green, and automated refreshed LV1 precheck PASS; returned USER UTS result remains pending.
Release-Debt Avoidance Status: Clear for this FAM-006 branch-local reconciliation. Future FAM-007 runtime expansion, provider/model/memory/shortcut/installer work, Overlay acceptance, AI Product work, and issue work remain separate USER-gated decisions.
Merged-main Current Active Workstream: PR #178 release-window source-truth repair, PR #177 FAM-007 provider path and consent readiness, PR #176 governance efficiency reform, PR #175 PR watcher approval-default governance, PR #174 worktree slot ownership governance, PR #173 v1.7.7 canon-closure drift truth, PR #172 FAM-007 execution-readiness gates, PR #171 Branch Runtime Engineering Plan governance, and PR #170 FAM-007 provider activation foundation are current main context only for this FAM-006 branch-local reconciliation; none of them is this worktree's active runtime carrier.
Current Active Workstream: Branch-local FAM-006 Monitor Groups / Sensor Command Center repair lane on `feature/fam-006-monitor-groups-sensor-configuration`; historical `returned USER UTS FAIL` repair triggers remain preserved for validator traceability; Dashboard post-corner right-edge resize rediscovery repair implementation and H1 are green; the returned LV1/UTS interactive-control reliability and visual-affordance repair is implemented and H1-repaired with hover/active/focus/click states, first-click stress proof, click-interception diagnostics, Polling Floor renamed to Polling Rate, Polling Rate Nexus dropdown proof that cannot pass while Source Filter is open, and whole-manifest failure when any live self-QA step fails; the latest bounded USER regression repair keeps Save Monitor and illuminated footer Discard far left with Delete Monitor far right, constrains Polling Rate activation to the visible dropdown toggle/menu/options instead of blank label-row space, makes Source Picker checkmarks single-path and immediate for row/input/keyboard activation, clears paired native-click suppression after each checkbox event, removes dirty-guard Cancel, places illuminated dirty-guard Discard on the far right, illuminates delete-confirmation Cancel, reveals dirty-delete confirmation after Save/Discard, and preserves Delete Monitor copy; the returned UTS follow-up removes the main-dashboard Create Monitor button, makes per-sensor Display mode selection deterministic on first pointer/click/keyboard activation, disables Save Monitor/Discard while clean, enables and illuminates them only when dirty, and snaps dirty close/leave attempts to the unsaved prompt; H1 is green with focused active-client Manage Monitors/WebView proof at `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260519_153159_493`; returned USER UTS result is USER_TEST_REQUIRED pending refreshed LV1/UTS review; PR Readiness remains blocked pending returned USER UTS PASS or explicit waiver with reason, and blocker reevaluation.
Branch-Local FAM-006 Reconciliation Note: `feature/fam-006-monitor-groups-sensor-configuration` in `C:\Nexus Worktrees\FAM-006` treats `origin/main` through PR #178, PR #177, PR #176, PR #175, PR #174, PR #173, PR #172 FAM-007 execution-readiness truth, PR #171 governance, and PR #170 FAM-007 provider activation truth as context, not identity. The branch-local authority remains FAM-006 Monitor Groups / Sensor Command Center. Implemented repair blockers are first-launch Dashboard flicker guard; Source Filter as Nexus-styled dropdown rather than exposed chips; dropdown open/hover reset so prior hover does not remain highlighted; 20+ monitor-group left-list stress proof with NDAI scrollbar styling; lower-right/bottom Delete Monitor and bottom confirmation placement; reduced top toolbar/search/create headspace; taller default and somewhat resizable Manage Monitors window; copy cleanup for phrases such as "for this monitor group"; preservation of prior visible resize-proof contamination repair; preservation of invisible/test-gated grow/shrink proof; Sensor Library source discovery; Warning Notifications as a setting checkbox; Provider Readiness as readiness/status/future capability; interactive-control reliability/visual-affordance repair; lower detail action-row alignment for Save/footer Discard left and Delete Monitor right; main-dashboard Create Monitor removal; per-sensor Display mode deterministic selection proof; clean-disabled and dirty-enabled Save Monitor / Discard proof; dirty guard scroll-to-prompt proof; Polling Rate toggle-only hitbox proof; Source Picker immediate-checkmark responsiveness stress; dirty-guard Save/Discard no-Cancel proof with right-side illuminated Discard; delete-confirmation Cancel illumination proof; dirty-delete confirmation reveal proof; footer Discard illumination proof; Manage Monitors Close full-height hover/click hitbox proof; and preservation of Sensor Library / Monitor / Monitor Group / Overlay Profile / Recording Profile separation. The accepted Runtime Branch Engineering Contract remains the current compact branch-local runtime plan authority unless a later validator or PR Readiness packet requires a separate branch-plan file pointer.
Deferred FAM-006 Monitor / Overlay Customization Trace: USER idea is recorded on the active FAM-006 settings-panel branch, not admitted as implementation. Monitor Groups future scope should create groups, assign available sensor/data sources, configure sensor-specific monitor settings inside Create Monitor / Edit Monitor flows, and redesign the future Edit Monitor Groups / Edit Monitor window closer to the NCP Create / Manage Task and Manage Group window layout with a created-monitor list, per-monitor Edit/Delete actions, delete confirmation, selected-monitor settings on Edit, and an in-window Create button so users can add a monitor without returning to the Dashboard. HUD Overlay settings/customization should own how monitor groups and sensor values are visually displayed in the Overlay, including colors, borders, text presentation, and presets. Broader NDAI Theme/Skins reskin is a future cross-app settings/theming candidate requiring explicit USER backlog admission; global font customization is not default, while Overlay-specific font/display customization may be planned inside Overlay customization.
Current Active Workstream Before Reform: None.
Current Execution Branch: `feature/fam-006-monitor-groups-sensor-configuration`
Active Branch Authority Record: `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md`.
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md`.
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md`.
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md`.
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_runtime_expansion.md`.
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md`.
Historical Branch Authority Record: `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md`.
Current Active Canonical Workstream Doc: None.
Historical Active Workstream Before Release: Automation Implementation.
Earlier Historical Active Workstream Before Release: FB-048 Active-session relaunch signal-failure and wait-timeout truth.
Historical Active Branch Before Release: feature/automation-planning.
Earlier Historical Active Branch Before Release: feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth.
Selected Next Workstream: FAM-006 Monitor Groups / Sensor Command Center returned LV1 interactive-control reliability, action-row, Polling Rate hitbox, Source Picker checkmark latency, and confirmation-control affordance repair.
Selected Next Record State: Branch-local refreshed LV1 close-guard, visual-proof, interactive-control visual QA, Dashboard post-corner right-edge rediscovery repairs, returned LV1 interactive-control reliability repair, lower detail action-row repair, Polling Rate hitbox proof, Source Picker immediate-checkmark responsiveness proof, dirty-guard Save/Discard no-Cancel proof, delete-confirmation Cancel illumination proof, Delete Monitor copy repair, and Manage Monitors Close full-height hitbox repair are preserved; current main through PR #178 is context only.
Selected Next Runtime Package Candidate: PKG-006 continuation for Monitor Groups / Sensor Command Center only.
Selected Next Implementation Branch: `feature/fam-006-monitor-groups-sensor-configuration`.
Selected Next Status: FAM-006 PR Readiness is blocked pending returned USER UTS PASS or explicit USER waiver with reason after automated refreshed LV1 precheck PASS for the interactive-control reliability/visual-affordance/action-row/Polling Rate hitbox/checkmark latency/confirmation-control affordance repair.
Runtime Package Admission: PKG-006 continuation; package completion not claimed for this Monitor Groups / Sensor Command Center repair lane.
Next Legal Runtime Step: USER return/digest of the refreshed UTS result or explicit waiver with reason for the H1-repaired FAM-006 interactive-control reliability repair and latest action-row/Polling Rate hitbox/checkmark latency/confirmation-control affordance automated LV1 PASS handoff.
Next Legal Analysis Candidate: Digest returned USER UTS results; after PASS or waiver digestion, PR Readiness Stage 1 may be requested. PR creation, merge, release work, issue mutation, FAM-007 work, and provider/model/runtime expansion remain separate USER decisions.
Release Readiness Issue Thread Cleanup Gate: Required later for FAM-006 release readiness after USER approval. GitHub issues #123, #127, #137, and #140 remain open / In Work and are eligible for USER-approved closeout after PR #142 merge; #124, #125, and #126 are already closed / fixed and their posture should be preserved. Required issue updates must summarize what solved the issue, name the solving PR/branch/proof traceability, preserve limitation/waiver notes where applicable, and link source-truth evidence before release execution is treated as complete. This record does not authorize GitHub comments, issue state changes, or issue closure.
Future UI Standardization Issue: GitHub issue #136 `Close Button Standardization Mismatch` records the USER-requested future standardization of the FAM-006 Dashboard window-level Close pill across future secondary NDAI windows. Scope includes NCP-adjacent Create / Manage windows and future Monitor Create/Edit windows when those windows are admitted for work; the main NCP itself is not implied by this issue. Future Overlay/display work should give the unanchored Overlay matching Close and Anchor affordances, then hide both controls when anchored to preserve edge-to-edge immersion. Non-physical evidence is the current branch source truth, commit `76b44afa420f59221f177d89ad0a8df73f9393ed`, latest red-shortcut human-client proof `dev/logs/fam_006_human_client_validation/20260514_111852_225/human_client_manifest.json`, and latest compact UTS handoff root `dev/logs/fam_006_monitoring_hud_live_validation/20260514_112213_466`; no raw evidence upload/import/linking is authorized by this record.
Current Runtime Repair Issue: GitHub issue #137 `Dashboard Rounded Corner Background Bleed` records the USER-observed black native rectangular corner beyond the Dashboard rounded CSS chrome when a light/white window sits behind it. The active settings-panel branch repairs it by applying a native rounded window mask, preserving transparent HUD/WebEngine background posture, clipping resize hit-testing to the same rounded native mask, and extending validators/helpers with white-backdrop corner-pixel proof. Latest red-shortcut proof passed at `dev/logs/fam_006_human_client_validation/20260514_111852_225/human_client_manifest.json`, compact UTS handoff refreshed at `dev/logs/fam_006_monitoring_hud_live_validation/20260514_112213_466`, and returned USER UTS results were digested as PASS. This issue does not authorize PR creation, merge, release execution, raw evidence upload/import/linking, FAM-007 work, provider/model/memory/shortcut/installer work, or Overlay/display acceptance.
Current Runtime Repair Issue: GitHub issue #140 `NCP tray toggle state regression` records the USER-observed regression where left-clicking the tray icon opened the NCP/Command Overlay but no longer closed it, and tray state remained Open instead of changing to Close. The active settings-panel branch repairs it by making tray activation consult live Command Overlay state, toggle open/close intentionally, and update native tray and popup labels to Open or Close Command Overlay. Latest red-shortcut proof passed at `dev/logs/fam_006_human_client_validation/20260514_111852_225/human_client_manifest.json`, including `ncp_tray_icon_left_click_opens`, `ncp_tray_menu_state_changes_to_close`, and `ncp_tray_icon_left_click_closes`; compact UTS handoff refreshed at `dev/logs/fam_006_monitoring_hud_live_validation/20260514_112213_466`; returned USER UTS results were digested as PASS. This issue does not authorize PR creation, merge, release execution, raw evidence upload/import/linking, FAM-007 work, provider/model/memory/shortcut/installer work, or Overlay/display acceptance.
Post-FAM-006 Required Governance/Package Candidate: Repo-Wide High-Risk Source Owner Marker Adoption; candidate branch `feature/repo-wide-source-owner-marker-adoption`; recorded as a future governance/package candidate after FAM-006 issue-planning priority is resolved or USER reorders it, not as an active selected-next implementation branch or newly admitted package. Later readiness must decide the legal carrier and package/admission shape before branch creation. Future scope is to scan existing source files, identify high-risk product/proof-bearing code regions, map them to Element Validation Ledger rows, add high-risk-only source-owner markers where useful, validate marker-to-ledger consistency, and plan repo-wide Dev Toolkit Interface Review Mode dispositions for existing and future USER-facing elements including NCP, Core visualization, Dashboard, Overlay/display when admitted, and other windows/components. The Dev Toolkit design is tabled for that future pass, including whether to use per-interface launchers, a generalized all-surfaces review-mode launch, or both. The future pass must keep production runtime behavior unchanged unless a separately admitted repair is required, and production UI must not expose element numbers.
Backlog Addition User Approval Missing: Cleared for this PR-readiness pass by USER-approved selected-next defer/waiver; no new backlog identity, backlog split, runtime package admission, successor branch, branch cleanup, or selected-next successor is created before PR creation. Active for new backlog item, backlog split, full AI Product Contract import, GitHub issue work beyond later approved closeout/comments, release/tag/artifact work, PR creation outside PR Readiness Stage 2, or any single-slice package waiver.
Historical Repair-Only Branch Handling: `feature/fb-046-post-merge-canon-sync` was a bounded repair-only post-merge canon-sync `feature/` branch and did not imply Branch Readiness admission or active branch truth for FB-046.
Historical Branch Readiness State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Current Branch Readiness State: Complete - source truth records returned LV1 denial, real-client proof-governance failure, WS48 closeout, WS49 follow-up repair closeout, WS50 visual-shell repair closeout, WS51 resize/scrollbar/persistence repair closeout, WS52 resize recovery closeout, WS53 resize discoverability closeout, WS54 resize cursor-alignment closeout, WS55 resize-action recovery closeout, WS56 pre-click resize cursor / resize fluidity closeout, post-main H1 shortcut/launcher proof-boundary truth, and WS57 actual desktop shortcut alignment/proof-gate repair.
Current Workstream State: Green after WS57 - WS43 through WS56 remain supporting history where not superseded; WS57 supplies focused Workstream proof that the actual desktop shortcut targets the active FAM-006 worktree and that human-client proof fails fast on shortcut/worktree mismatch.
Current Hardening State: Green after WS57 plus latest bounded Quick Access/high-refresh resize repair - H1 pressure-tested actual desktop shortcut alignment, launcher/orphan-tray integration, active-owner PID identity, stale/reused PID relaunch, RUI-055/RUI-056 human-client resize cursor/fluidity proof, active-client proof, desktop entrypoint/tray proof, NCP/saved-action proof, static validation, and internal sandbox proof; the latest repair clears screenshot-visible Quick Access warning-notification shadow bleed and proves high-refresh resize tracking through native window-rect samples.
Current Live Validation State: Stage 1 PASS - latest strengthened red shortcut human-client proof passed at `dev/logs/fam_006_human_client_validation/20260514_111852_225/human_client_manifest.json` after Quick Access shadow-clearance, normal-speed movement and high-refresh resize smoothness repair, central-50-percent rounded-corner diagonal resize-zone repair, #137 rounded-corner native-mask repair, and #140 NCP tray toggle/state repair; compact formal UTS handoff refreshed at `dev/logs/fam_006_monitoring_hud_live_validation/20260514_112213_466`; USER returned refreshed UTS results as PASS after confirming all raised issues and testing returned good.
Current PR Surface Owner: PR #118 `FAM-006 Monitoring HUD Dashboard Product Surface`; PR #109 merge/bot-review/watcher proof remains historical in `Docs/workstreams/FB-027_interaction_system_baseline.md`.
Current Branch Class: implementation.
Current Implementation Delta Class: runtime/user-facing, backend/runtime, validator, developer-tooling, and source-truth Live Validation repair.
Historical runtime-proof governance remains preserved: the PR watcher remains the only minute-scale heartbeat automation, `ACTIVE` alone is not treated as run proof, and any fallback helper must stay narrowed to the live PR and bounded to `PR Readiness`.
Historical Workstream State: Automation catalog implementation is merged historical branch proof after PR #99; FB-048 is Released / Closed in `v1.6.12-prebeta`; FB-047 is Released / Closed in `v1.6.11-prebeta`; FB-046 is Released / Closed in `v1.6.10-prebeta`; FB-044 and FB-045 remain Released / Closed historical proof in `v1.6.9-prebeta`.
Historical Hardening State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Historical Live Validation State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Canonical Current-State Rule: merge-target current-state owners stay merge-stable and must not normalize unresolved release debt, stale canon, or cleanup-only branches as the default. Live PR state, conflict/readiness details, review-resolution details, and blocker-clearing repair-lane narration live only in explicit historical PR sections of the canonical workstream and in operator output.
Release Execution State: `v1.7.8-prebeta` is published at `2bd54f0e34c6759e9618f42d104d80b975ecc1c3`; current main closes the release-dependent canon drift in source truth, while this FAM-006 branch preserves that as context.
Release Target: None - `v1.7.8-prebeta` has been published.
Release Floor: none - release execution is complete.
Version Rationale: `v1.7.8-prebeta` publishes PR #173 through PR #178 after `v1.7.7-prebeta`, including v1.7.7 canon-closure drift truth, worktree/pr-watcher/governance-efficiency governance, FAM-007 provider path and consent readiness source truth, and release-window source-truth repair, without enabling provider setup, consent collection, provider/model execution, downloads, external calls, memory, learning, personalization, network egress, or voice/Core sync.
Release Scope: Released in `v1.7.8-prebeta`: PR #173 through PR #178 release-window/source-truth and governance context plus FAM-007 provider path and consent readiness source truth.
Release Artifacts: Published - lightweight tag `v1.7.8-prebeta` and GitHub Release `Pre-Beta v1.7.8` exist at tag commit `2bd54f0e34c6759e9618f42d104d80b975ecc1c3`; release URL `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.7.8-prebeta`; assets none attached.
Post-Release Truth: `v1.7.8-prebeta` is the latest public prerelease; PR #173 through PR #178 are released/current-main context; no active main branch authority is implied by the release.
Next-Branch Creation Gate: Closed by USER-approved Branch Readiness Stage 2 creation of `feature/fam-007-local-ai-provider-path-and-consent-readiness`.
Next Legal Phase: Branch-local FAM-006 returned USER UTS digest, or explicit waiver with reason, after automated refreshed LV1 precheck PASS; current-main FAM-007 PR #177/provider path truth and PR #178 v1.7.8 release-window truth remain context only, and release execution, issue work, provider setup, consent collection, provider SDK/model work, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, successor branch selection, v1.8.0-prebeta release execution, merge, and AI Product Contract import remain separate USER decisions.

## Backlog Governance Sync

Last Reviewed: 2026-04-27 during Backlog Family Governance Reform Phase 4 / Slice R4-S4 validator-helper and artifact index hardening.

Open-candidate priority review:

- FB-004 is released and closed in `v1.6.3-prebeta`; it is no longer an active or selected-next branch candidate.
- FB-015 is released and closed in `v1.6.4-prebeta`; it no longer owns release debt or active branch truth.
- FB-029 is released and closed in `v1.6.4-prebeta`; it no longer owns release debt or active branch truth.
- FAM-004 legacy FB-030 is released historical traceability in `v1.6.13-prebeta` after PR #108; its historical `v1.6.5-prebeta` planning proof remains preserved, and its runtime follow-through delivered bounded voice/audio availability and truthful diagnostics proof with WS1, H1, LV1, PR1, and PR2 complete.
- FAM-003 legacy FB-027 is a released baseline family anchor. PR #109 shutdown-hotkey availability/direct-shutdown validation is preserved as merged historical family evidence and aggregation material, with visible confirmation owned by tray Exit only; it is not an active backlog item or standalone release-version driver.
- FB-005 remains `Low` as historical workspace priority, but it is now Released / Closed in `v1.6.6-prebeta` and no longer owns release debt or selected-next truth.
- FB-042 is now Released / Closed in `v1.6.7-prebeta`; the released launch-path slice is preserved as the first historical proof under the runtime family anchor.
- FB-043 is now Released / Closed in `v1.6.8-prebeta`.
- FB-044 is now Released / Closed in `v1.6.9-prebeta`.
- FB-045 is now Released / Closed in `v1.6.9-prebeta`.
- FB-046 is now Released / Closed in `v1.6.10-prebeta`.
- FB-047 is now Released / Closed in `v1.6.11-prebeta`.
- FB-048 is Released / Closed in `v1.6.12-prebeta`; release debt is clear after publication, validation, and post-release canon closure.
- FAM-001 legacy FB-049 is historical complete after PR #107 merge; GitHub merge truth is valid, the same-thread watcher handoff failed, cleanup is proven, and the stale active-branch authority plus recurrence analysis is carried and repaired inside FAM-004 legacy FB-030 Branch Readiness.

Current-branch clarity: latest public prerelease is `v1.7.8-prebeta`; PR #173 through PR #178 are released/current-main release-window/source-truth context for `v1.7.8-prebeta`; PR #177 merged `feature/fam-007-local-ai-provider-path-and-consent-readiness` as historical FAM-007 provider path and consent readiness evidence; PR #171 Branch Runtime Engineering Plan governance and PR #172 FAM-007 Local AI Provider Execution Readiness Gates are released in `v1.7.7-prebeta`; PR #169 Governance Process Efficiency Reform and PR #170 FAM-007 Local AI Provider Activation Foundation are released in `v1.7.6-prebeta`; PR #164 through PR #168, including PR #165 FAM-007 provider-readiness/setup-eligibility, are released in `v1.7.5-prebeta`; earlier FAM-007 local-only scaffold/runtime evidence remains released historical traceability through v1.7.1-prebeta to v1.7.4-prebeta; no selected-next runtime branch is active after PR #177 in current main, while this worktree remains the active branch-local FAM-006 carrier; later FAM-007 provider setup/model implementation remains USER-gated.

## Registry Items

### User-Facing Feature Families

Selectable user-facing feature-family records now use the fresh `FAM-###` namespace in ascending order from `FAM-001`. Legacy `FB-###` IDs are preserved only as historical trace fields, former-ID tables, workstream filenames, branch filenames, and release/PR evidence.

Canonical Identity Model: `FAM` = broad long-lived product family; `Package` = bulk branch/release package under one family; `Slice` = traceable deliverable area inside a package; `Seam` = execution or validation checkpoint; `PR` = merge/review evidence only; legacy global `FB` = historical trace only.
Branch Scope Standard: branches must package multiple related admitted slices under exactly one broad family by default. A package with exactly one admitted slice is blocked by `Single-Slice Package User Approval Missing` unless `Single-Slice Package User Approval: Granted` is recorded with explicit USER approval.
Package Completion Standard: Workstream continues through every admitted package slice until `Package Completion State: Complete`, `Released Baseline / Open`, `Blocked`, or `Deferred` is truthfully recorded before Hardening admission.
Admitted Slice Counting Rule: only rows with `Admission State` equal to `Admitted` count toward a package's admitted-slice total. Rows represented as `Admission State: Admitted` are the only rows that count; `Historical Evidence`, `Merged Evidence`, `Future Placeholder`, `Deferred Placeholder`, and other non-admitted trace rows preserve context but cannot satisfy the multi-slice package rule.
Concrete Admitted Slice Rule: an admitted slice must have a concrete scoped deliverable, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder rows cannot be marked admitted.
Package Completion Guard: `Package Completion State: Complete` is blocked while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while another admitted slice remains incomplete.
Named Package Blockers: `Single-Slice Package User Approval Missing` and `Package Completion Unproven`.
USER Blocker Output Standard: `Backlog Addition User Approval Missing` must list every not-closed FAM and every not-complete package or slice before stopping.
PR Evidence Standard: PR numbers are evidence only and must not become backlog identities, package identities, release-version drivers, or selected-next successors.
Element Coverage Standard: Element Coverage is a non-identity checklist for FAM/package review only. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

| FAM ID | Broad Product Family | Family Status | Package Posture | Legacy Trace Coverage |
| --- | --- | --- | --- | --- |
| `FAM-001` | Boot Interface | Open / released-baseline aggregation | `PKG-001` released baseline / open | `FB-042`, `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`, `FB-049`, PR #86-#107 |
| `FAM-002` | Desktop Interface | Open / pending user-facing follow-through | `PKG-002` released baseline / open | `FB-031`, UI/UX planning release evidence |
| `FAM-003` | Interaction and Actions | Open / aggregation-held | `PKG-003` released baseline / open | `FB-027`, `FB-036`, `FB-037`, `FB-038`, `FB-041`, PR #109 |
| `FAM-004` | Voice and Audio | Open / released-baseline aggregation | `PKG-004` released baseline / open | `FB-030`, PR #108, `v1.6.5-prebeta`, `v1.6.13-prebeta` |
| `FAM-005` | External Integrations | Pending implementation | `PKG-005` released baseline / open | `FB-039`, Stream Deck and external trigger gap |
| `FAM-006` | Monitoring and HUD | Returned LV1 denial remains historical evidence; WS56 repaired RUI-055/RUI-056 pre-click resize cursor and resize fluidity as Workstream proof; WS57 repaired actual desktop shortcut/worktree alignment; post-WS57 H1 and LV1 handoff proof are green; LV2 digested explicit USER waiver/passable Dashboard acceptance | `PKG-006` admitted and released as historical traceability in v1.7.0-prebeta | `FB-040`, HUD surface gap |
| `FAM-007` | Local AI and Capability Packs | Package admitted / PR #152 released local-only scaffold chain in v1.7.2-prebeta / PR #159 released runtime foundation in v1.7.3-prebeta / PR #162 released runtime-expansion foundation in v1.7.4-prebeta / PR #165 provider-readiness evidence released in v1.7.5-prebeta / PR #170 activation-foundation evidence released in v1.7.6-prebeta / PR #172 execution-readiness evidence released in v1.7.7-prebeta / PR #177 provider path and consent readiness merged-unreleased candidate scope | `PKG-007` admitted with eight slices / provider path and consent readiness merged-unreleased in PR #177 / package completion not claimed because future provider setup/model/memory/learning/personalization/voice/Core/shortcut/installer work remains USER-gated | `Docs/orin_vision.md` local-AI and capability-pack vision plus historical branch authority `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md`, historical branch authority `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md`, historical branch authority `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md`, historical branch authority `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md`, historical branch authority `Docs/branch_records/feature_fam_007_local_ai_runtime_expansion.md`, historical branch authority `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md`, historical branch authority `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md`, and historical FAM-007 branch records |
| `FAM-008` | Packaging and Install Experience | Pending architecture/package | `PKG-008` pending | `Docs/orin_vision.md`, modular install and GPU-aware architecture gap |
| `FAM-009` | Workspace and Data | Open / deferred follow-through | `PKG-009` released baseline / open | `FB-005`, `FB-020`, `FB-026`, `FB-028`, workspace/data trace |
| `FAM-010` | Safety and Privacy | Pending architecture/package | `PKG-010` pending | `Docs/orin_vision.md`, local execution, privacy, and safety boundaries |

### [ID: FAM-001] Boot Interface

Status: Open / released-baseline aggregation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Startup, boot, desktop entrypoint, single-instance ownership, launch handoff, relaunch semantics, lifecycle transition proof, and boot-to-runtime trust boundaries.
Package Policy: Branchable work must be a bulk boot-interface package with multiple related admitted slices by default.
Known Pending Gaps: Boot-family proof remains released-baseline open until future USER-approved package work closes lifecycle follow-through beyond the historical launch/relaunch baselines.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-001` | `FAM-001` | Startup lifecycle and relaunch truth baseline | Released baseline / open | Released Baseline / Open | `feature/fb-042-desktop-entrypoint-runtime-refinement`; `feature/fb-049-runtime-branch-readiness`; `v1.6.7-prebeta` through `v1.6.13-prebeta` | `FB-042`, `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`, `FB-049`, PR #86-#107 |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-001` | `PKG-001` | `FAM-001` | Desktop entrypoint and launch-path baseline | Historical Evidence | Released | Complete | `FB-042`; Branch Readiness, Workstream, Hardening, Live Validation, PR, Release |
| `SLC-002` | `PKG-001` | `FAM-001` | Top-level entrypoint and boot handoff truth | Historical Evidence | Released | Complete | `FB-043`, `FB-044`; Branch Readiness through Release |
| `SLC-003` | `PKG-001` | `FAM-001` | Active-session relaunch success, decline, failure, and timeout truth | Historical Evidence | Released | Complete | `FB-045`, `FB-046`, `FB-047`, `FB-048`; Branch Readiness through Release |
| `SLC-004` | `PKG-001` | `FAM-001` | Pre-settled incoming-launch conflict truth | Historical Evidence | Released | Complete | `FB-049`; WS1, H1, LV1, PR #107, `v1.6.13-prebeta` |

Summary: Boot Interface owns the long-lived startup and relaunch product surface; old `FB-042` through `FB-049` remain historical proof slices under this family, not reusable live backlog IDs.

### [ID: FAM-002] Desktop Interface

Status: Open / pending user-facing follow-through
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Nexus desktop shell, visual language, operator UI, settings presentation, user-facing desktop interaction surfaces, and coherent UI/UX implementation packages.
Package Policy: Branchable desktop-interface work must package multiple admitted UI/UX slices by default and must not treat one planning pass as a closed family.
Known Pending Gaps: Nexus-era user-facing HUD/shell presentation, settings and desktop UX implementation remain pending after the historical planning release.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-002` | `FAM-002` | Desktop shell and UI/UX baseline | Released baseline / open | Released Baseline / Open | `feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning`; `v1.6.1-prebeta` | `FB-031`, UI/UX planning release evidence |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-005` | `PKG-002` | `FAM-002` | Nexus UI/UX source-map and visual-language baseline | Historical Evidence | Released | Complete | `FB-031`; Branch Readiness through Release |
| `SLC-006` | `PKG-002` | `FAM-002` | User-facing desktop shell implementation follow-through | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Desktop Interface keeps the UI/UX planning baseline as historical proof while leaving the real user-facing desktop work open.

### [ID: FAM-003] Interaction and Actions

Status: Open / aggregation-held
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Typed-first interaction, saved actions, callable groups, built-in actions, tray quick tasks, hotkeys, shared action routing, confirmation flows, and reusable action execution boundaries.
Package Policy: Branchable interaction work must be a family package with multiple admitted slices by default; small runtime proofs aggregate unless USER approves a release driver.
Known Pending Gaps: Shared action authoring, built-in/catalog expansion, tray quick-task follow-through, and shutdown confirmation evidence remain aggregation material until a USER-approved package is admitted.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-003` | `FAM-003` | Shared interaction and action model baseline | Released baseline / open | Released Baseline / Open | `Docs/workstreams/FB-027_interaction_system_baseline.md`; `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `FB-027`, `FB-036`, `FB-037`, `FB-038`, `FB-041`, PR #109 |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-007` | `PKG-003` | `FAM-003` | Typed-first interaction and saved-action baseline | Historical Evidence | Released | Complete | `FB-027`, `FB-036`; historical Branch Readiness through Release |
| `SLC-008` | `PKG-003` | `FAM-003` | Deterministic callable groups, built-ins, settings, and tray quick tasks | Historical Evidence | Released baseline / open | Released Baseline / Open | `FB-037`, `FB-038`, `FB-041`; historical Branch Readiness through Release |
| `SLC-009` | `PKG-003` | `FAM-003` | Shutdown hotkey direct-shutdown and tray-confirmation boundary proof | Merged Evidence | Merged historical evidence | Merged Historical Evidence | PR #109; WS1, H1, LV1, PR Readiness |

Summary: Interaction and Actions replaces the accidental small-branch backlog identity pattern; PR #109 stays trace evidence inside a broader family package.

### [ID: FAM-004] Voice and Audio

Status: Open / released-baseline aggregation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Latest Released Runtime Proof Version: v1.6.13-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md
Family Scope: ORIN voice output, error voice, quiet/bypass behavior, audio availability diagnostics, persona-safe voice claims, and future cross-family voice integration.
Package Policy: Branchable voice/audio work must package multiple admitted runtime or integration slices by default; one diagnostic seam alone is aggregation evidence unless USER approves otherwise.
Known Pending Gaps: Runtime diagnostics proof is released historical traceability; future voice integration across interaction, desktop, and safety/privacy families remains pending.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Released Historical Scope: FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth plus FAM-004 legacy FB-030 voice/audio runtime diagnostics proof plus merged governance/automation proof package plus PR #112 source-truth closeout / merge-target authority hardening proof plus PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta
Latest Public Prerelease: v1.7.0-prebeta
Release Title: Pre-Beta v1.6.13
Release Target: None - released in v1.6.13-prebeta.
Release Floor: none - release execution is complete.
Version Rationale: The voice/audio runtime diagnostics proof added bounded truthfulness for availability states without opening a standalone new family or release-version driver.
Release Scope: released governance reform, automation catalog proof, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof.
Release Artifacts: Published tag `v1.6.13-prebeta`; published GitHub prerelease title `Pre-Beta v1.6.13`; release notes include generated `What's Changed` and `Full Changelog` sections.
Post-Release Truth: merged governance reform, automation catalog, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening, and PR #113 source-truth closeout / merge-target authority hardening are released historical traceability; release debt is clear; and the later runtime package has USER-approved FAM-006 prior Workstream/Hardening evidence on `feature/fam-006-monitoring-hud-product-surface`; product completion is reopened, returned LV1 UTS FAIL evidence has routed the branch back through Branch Readiness rebaseline, and bounded Workstream repair continues after WS18 Core non-interference proof plus WS19 dashboard/minimal-HUD split proof.
Selected Next Workstream: None - FAM-006 merged through PR #118 and is released historical traceability in v1.7.0-prebeta.
Next-Branch Creation Gate: Blocked until the governance/canon repair PR merges, updated main validates, and a later Branch Readiness packet admits implementation.
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-004` | `FAM-004` | Voice/audio truth and integration package | Released baseline / open | Released Baseline / Open | `feature/fb-030-voice-audio-runtime-branch-readiness`; `v1.6.13-prebeta` | `FB-030`, PR #108, `v1.6.5-prebeta` planning release |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-010` | `PKG-004` | `FAM-004` | Voice/audio direction and planning baseline | Historical Evidence | Released | Complete | `FB-030`; `v1.6.5-prebeta` |
| `SLC-011` | `PKG-004` | `FAM-004` | Truthful voice/audio runtime diagnostics | Historical Evidence | Released | Complete | `FB-030`; WS1, H1, LV1, PR #108, `v1.6.13-prebeta` |
| `SLC-012` | `PKG-004` | `FAM-004` | Cross-family voice integration package follow-through | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Voice and Audio carries legacy `FB-030` proof as package evidence while keeping the broader voice integration family open.

### [ID: FAM-005] External Integrations

Status: Pending implementation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Stream Deck, external trigger intake, plugin lifecycle, installed integration points, trusted invocation boundaries, and external action ownership.
Package Policy: Branchable external-integration work must package multiple admitted implementation and validation slices by default.
Known Pending Gaps: Stream Deck and external integration implementation remains pending after the historical architecture-only trigger-intake release.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-005` | `FAM-005` | External trigger and plugin implementation package | Released baseline / open | Released Baseline / Open | `feature/fb-039-external-trigger-plugin-integration-architecture`; `v1.5.0-prebeta` | `FB-039`, Stream Deck/external integration gap |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-013` | `PKG-005` | `FAM-005` | External trigger architecture and lifecycle baseline | Historical Evidence | Released | Complete | `FB-039`; Branch Readiness through Release |
| `SLC-014` | `PKG-005` | `FAM-005` | Stream Deck and installed integration implementation | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: External Integrations keeps the trigger architecture release as proof while leaving implementation work pending.

### [ID: FAM-006] Monitoring and HUD

Status: Released historical traceability in v1.7.0-prebeta / branch-local active Monitor Groups carrier
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Next Workstream: Selected
Next Workstream: FAM-006 Monitor Groups / Sensor Command Center interactive-control reliability and visual-affordance repair after returned LV1/UTS failure; released PR #118/v1.7.0-prebeta evidence remains historical baseline, while this branch carries the later USER-approved Monitor Groups runtime carrier.
Selected Next Workstream: FAM-006 Monitor Groups / Sensor Command Center returned LV1 interactive-control reliability and visual-affordance repair.
Selected Next Runtime Package Candidate: PKG-006 continuation for Monitor Groups / Sensor Command Center only.
Selected Next Status: Branch-local current-main reconciliation preserves current main truth, keeps PR Readiness blocked, and routes returned LV1 interactive-control reliability/visual-affordance setup to bounded Repair Workstream implementation before Hardening H1 and refreshed Live Validation resume.
Selected Next Implementation Branch: `feature/fam-006-monitor-groups-sensor-configuration`
Branch Creation Status: Created in Branch Readiness Stage 2 from updated main at `3c68cd881a9f6bf447f09ac0949d556e97bce4f4`
Runtime Package Admission: Historical - `PKG-006` was admitted on the FAM-006 branch and merged through PR #118.
Active Branch Authority Record: `Docs/branch_records/feature_fam_006_monitor_groups_sensor_configuration.md`
Next Legal Runtime Step: Refreshed LV1 / UTS recheck for the H1-repaired returned FAM-006 Monitor Groups / Sensor Command Center interactive-control reliability and visual-affordance repair after USER approval. PR creation, merge, release work, FAM-007/local AI work, and GitHub issue mutation require separate explicit USER approval.
Minimal Scope: admitted runtime package rebaselined to Dashboard-first current-branch acceptance: optional Nexus/NDAI Monitoring HUD Dashboard/control panel, monitor definition/editing and enablement posture, provider-contract-first telemetry health/setup/unavailable states, settings/control visibility, fail-safe/setup/reconnect/no-data/degraded-status behavior, visual/non-invasive warning posture controls, dashboard-specific validation/live desktop proof, and no fake telemetry; Overlay/display release acceptance, edgeless placement canvas acceptance, anchored uninteractable/click-through overlay acceptance, audio/spoken warnings, Stream Deck/plugin telemetry implementation, full sensor-platform parity, broad hardware provider platform work, advanced graphs/history/persistence, local AI, installer/capability-pack work, and broad repo-wide legacy naming migration remain deferred unless later admitted.
Family Scope: Monitoring surfaces, CPU/GPU thermals, performance telemetry, HUD/overlay presentation, trust-safety display rules, and plugin-fed runtime telemetry.
Package Policy: Branchable monitoring/HUD work must package source, display, and validation slices by default.
Known Pending Gaps: Returned LV1 denial remains proof-governance history for prior handoffs. WS43 through WS57, prior Hardening H1, post-WS50 H1, post-WS53 H1, post-WS56 H1, prior LV1 handoff generation, post-main H1 proof, post-WS57 H1 proof, current LV1 handoff proof, and LV2 USER waiver digest are supporting/acceptance history where not superseded. Overlay Scope Deferred and Core Repair Dependency Only remain non-gating boundary classifications, not release interfaces. Broad provider-platform parity, Overlay/display release acceptance, external/plugin telemetry, audio/spoken alerts, persona switching, Stream Deck, graphs/history/persistence dashboards, local AI/capability packs, installer work, child-window implementation, NCP placement/persistence, Dev Toolkit Interface Review Mode, and ultra-low polling remain future-package deferrals unless later admitted. Future provider-platform work must preserve usable no-advanced-provider/baseline behavior, treat LibreHardwareMonitor as optional, preserve user provider choice, and satisfy third-party notice/MPL/source-availability and user-consented update-management requirements before any LibreHardwareMonitor bundle or update flow is admitted.
Package Admission State: Admitted
Admitted Slice Count: 6
Package Completion State: Released historical traceability in v1.7.0-prebeta
Single-Slice Package User Approval: Not required - `PKG-006` has six concrete admitted slices and no single-slice waiver is granted.
Single-Seam Workstream Waiver: None - bounded means one active seam at a time, not one-seam Workstream authority; single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded; if only one seam or one slice is planned or visible for the whole Workstream, stop on `Single-Seam Or Single-Slice Workstream Blocker`; PKG-006 has a recorded multi-seam/multi-slice Workstream chain and must continue through the remaining same-branch repair work unless a named blocker, future dependency, or explicit USER waiver is recorded.
Interface Release Boundary: Dashboard-first - `Monitoring HUD Dashboard / control panel` is the primary current-branch interface release surface.
Interface Bundle User Approval: Not granted - Overlay/display acceptance is deferred/non-gating and Core repair is dependency-only.
Dashboard Acceptance: USER WAIVED/PASSABLE - returned real-client, visual-shell, resize hit-zone, post-WS51 resize-unavailable, post-WS52 resize discoverability, post-WS53 resize cursor-alignment, post-WS54 resize-action, post-WS55 pre-click cursor/fluidity, scrollbar inset, HUD Feature persistence, and shortcut/worktree alignment feedback remains issue-grounded for traceability; USER explicitly waived the refreshed UTS returned-result test and said Dashboard functionality is passable.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-006` | `FAM-006` | Monitoring and HUD product-surface package | Returned LV1 denial remains historical evidence; WS48 through WS57, post-WS57 H1, and LV1 handoff proof are green supporting proof where not superseded; LV2 digested explicit USER waiver/passable Dashboard acceptance; Overlay/display acceptance deferred/non-gating; Core repair dependency-only; PR #118 merged and v1.7.0-prebeta released | Released historical traceability in v1.7.0-prebeta | `feature/fam-006-monitoring-hud-product-surface`; PR #118; historical baseline `feature/fb-040-monitoring-thermals-performance-hud-surface`; `v1.7.0-prebeta`; `v1.6.0-prebeta` | `FB-040`, HUD user-facing surface gap |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-015` | `PKG-006` | `FAM-006` | Monitoring and thermal architecture baseline | Historical Evidence | Released | Complete | `FB-040`; Branch Readiness through Release |
| `SLC-016` | `PKG-006` | `FAM-006` | HUD visual and user-facing monitoring surface | Admitted | LV2 Waiver Accepted / Released | Dashboard/control panel is the active visual release surface accepted as USER WAIVED/PASSABLE; Overlay/display visual acceptance is deferred/non-gating; PR #118 merged and v1.7.0-prebeta released the package | `BR-S2-S1`; `WS1`; `WS7`; `WS9`; `WS17`; `H1`; `LV1-R1`; `LV2`; `WS19`; `WS22`; `WS24`; `WS25`; `WS26`; `WS27`; `WS28`; `WS29`; `WS30`; `BR-S2-R12`; `BR-S2-R13`; `WS31`; `WS43`; `WS44`; `WS45`; `WS46`; `WS57`; `dev/orin_monitoring_hud_surface_validation.py`; `dev/orin_monitoring_hud_live_validation.ps1` |
| `SLC-025` | `PKG-006` | `FAM-006` | Runtime telemetry source and adapter boundary | Admitted | Green | Provider-contract boundary plus bounded native CPU-load proof; GPU/thermal provider parity deferred | `BR-S2-S2`; `WS2`; `WS14`; `WS15`; `desktop/monitoring_hud_telemetry.py`; `dev/orin_monitoring_hud_internal_sandbox_validation.py` |
| `SLC-026` | `PKG-006` | `FAM-006` | Desktop placement and renderer ownership | Admitted | LV2 Waiver Accepted / Released | Core placement repair remains dependency-only, Overlay/display placement acceptance is deferred/non-gating, and Dashboard standalone window movement/clipping/Core-Overlay decoupling is accepted as USER WAIVED/PASSABLE under the Dashboard-first boundary. | `BR-S2-S3`; `WS3`; `WS10`; `WS12`; `LV1-R1`; `LV2`; `WS18`; `WS19`; `WS21`; `WS22`; `WS25`; `WS26`; `WS28`; `WS29`; `WS30`; `BR-S2-R12`; `BR-S2-R13`; `WS31`; `WS32`; `WS37`; `WS38`; `WS43`; `WS44`; `WS46`; `WS57`; `desktop/monitoring_hud_placement.py`; `desktop/desktop_renderer.py`; `desktop/core_visualization_renderer.py` |
| `SLC-027` | `PKG-006` | `FAM-006` | Settings and user controls visibility | Admitted | LV2 Waiver Accepted / Released | Dashboard settings/control content and monitor-management clarity are accepted as USER WAIVED/PASSABLE; visual/non-invasive warning posture controls remain current-scope accepted, while future editor/detail work remains deferred. | `BR-S2-S4`; `WS4`; `WS11`; `WS13`; `LV1-R1`; `LV2`; `WS19`; `WS20`; `WS21`; `WS28`; `WS29`; `BR-S2-R12`; `BR-S2-R13`; `WS31`; `WS33`; `WS34`; `WS35`; `WS40`; `WS45`; `WS46`; `WS57`; `desktop/monitoring_hud_controls.py`; `desktop/orin_desktop_main.py`; `nexus_visual/monitoring_hud.js` |
| `SLC-028` | `PKG-006` | `FAM-006` | Fail-safe, no-data, and degraded-status behavior | Admitted | LV2 Waiver Accepted / Released | Dashboard provider/setup/no-data/degraded truth is accepted as USER WAIVED/PASSABLE under the Dashboard-first boundary; fake telemetry remains blocked. | `BR-S2-S5`; `WS5`; `WS16`; `LV1-R1`; `LV2`; `WS20`; `WS28`; `WS29`; `BR-S2-R12`; `BR-S2-R13`; `WS31`; `WS34`; `WS35`; `WS45`; `WS46`; `desktop/monitoring_hud_status.py`; `dev/orin_monitoring_hud_surface_validation.py` |
| `SLC-029` | `PKG-006` | `FAM-006` | Validation and live desktop proof | Admitted | LV2 Waiver Accepted / Released | Dashboard-specific proof separates current-interface acceptance from deferred Overlay/display evidence; WS57/H1/LV1 refreshed actual shortcut/human-client proof, and LV2 digested USER's explicit UTS waiver. | `BR-S2-S6`; `WS6`; `WS8`; `WS17`; `H1`; `LV1-R1`; `LV2`; `WS18`; `WS19`; `WS20`; `WS21`; `WS22`; `WS23`; `WS24`; `WS25`; `WS26`; `WS27`; `WS28`; `WS29`; `WS30`; `BR-S2-R12`; `BR-S2-R13`; `WS31`; `WS32`; `WS33`; `WS35`; `WS42`; `WS46`; `WS57`; `dev/orin_monitoring_hud_live_validation.ps1`; `dev/orin_monitoring_hud_internal_sandbox_validation.py` |
| `SLC-030` | `PKG-006` | `FAM-006` | Optional voice or spoken status integration | Deferred Placeholder | Deferred pending cross-family approval | Not Admitted | Future USER widening decision required if voice/audio behavior is needed |

Admitted Slice Shape: HUD visual/user-facing surface; runtime telemetry source/adapters; desktop placement / renderer ownership; settings or user controls visibility; fail-safe / no-data / degraded-status behavior; validation / live desktop proof.
Deferred/Future Slice Shape: optional voice/status integration is not admitted because spoken/audio behavior, voice integration, persona voice, or FAM-004 cross-family widening requires later explicit USER approval.
Element Coverage Review: user-facing surface, runtime/backend behavior, settings/configuration, fail-safe/recovery, voice/audio integration as deferred coverage only, monitoring/HUD/observability, validation/live-test requirements, release/documentation impact, security/privacy posture, external integration, local AI/capability-pack impact, and packaging/install impact are planning coverage only and do not count as admitted slices.
Summary: Monitoring and HUD scaffold/boundary/runtime work remains credited as prior evidence, and prior returned LV1 UTS evidence is historical FAIL only. WS31 records the Dashboard-only acceptance baseline, WS32 records Dashboard standalone movement/clipping/Core-Overlay decoupling proof, WS33 records Dashboard settings/control content polish and monitor-management clarity, WS34 records Dashboard provider/setup/no-data/degraded truth plus warning posture controls, WS35 records Dashboard-specific static/live proof, screenshots, and Live Validation UTS boundary proof, WS36 records Dashboard-focused Workstream green plus Hardening handoff, prior H1 records historical Dashboard-first hardening proof, and prior LV1 records Stage 1 active-client proof plus the prior formal UTS handoff. The completed Element Validation Ledger revalidated green and LV1 generated a ledger-aligned UTS, but USER Dashboard feedback blocked acceptance before LV2. WS43 repairs the current runtime/tray/shutdown safety packet, WS44 repairs Dashboard frame/scroll/resize/visual shell, WS45 repairs Dashboard IA/naming/action cleanup, WS46 records returned-feedback proof readiness, WS47 repairs real-client tray/shortcut proof, WS48 repairs human-client validation governance, WS49 repairs Dashboard/NCP/tray action isolation, WS50 repairs scrollbar/native-window boundary, WS51 repairs resize hit-zone reliability, scrollbar inset precision, and HUD Feature state persistence, WS52 repairs the real resize recovery path, WS53 repairs resize edge discoverability with a forgiving visible rail, WS54 repairs the Windows standard resize cursor alignment at the visible edge/corner rail, WS55 repairs resize action from the discovered cursor transition point, WS56 repairs pre-click hover cursor timing plus fluid resize geometry sampling, WS57 repairs actual desktop shortcut/worktree alignment, and post-WS57 H1/LV1 refreshed actual shortcut proof. LV2 has digested USER's explicit UTS waiver/passable Dashboard acceptance. PR #118 merged, PR #119 repaired pre-release canon drift, and v1.7.0-prebeta released the package. The Dashboard/control panel is the primary release surface, Overlay/display acceptance is deferred/non-gating, Core repair is dependency-only, and future GitHub issues or issue-resolution branches require later explicit USER approval.

### [ID: FAM-007] Local AI and Capability Packs

Status: Package admitted / PR #152 released in v1.7.2-prebeta / PR #159 released in v1.7.3-prebeta / PR #162 released in v1.7.4-prebeta / PR #165 provider runtime readiness released in v1.7.5-prebeta / PR #170 activation foundation released in v1.7.6-prebeta / PR #172 execution-readiness gates released in v1.7.7-prebeta / PR #177 provider path and consent readiness merged-unreleased for v1.7.8-prebeta candidate
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Next Workstream: None selected after PR #177 merge.
Next Workstream Carrier State: `feature/fam-007-local-ai-provider-path-and-consent-readiness` is historical merged-unreleased PR #177 evidence; successor selection remains USER-gated.
Recommended Next Workstream: Provider path and consent readiness contracts/proof planning for a later provider setup and execution path, preserving provider path/setup implementation, consent collection, provider SDK/model execution, downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, AI Product Contract import, issue work, future PR creation/merge, release execution, and v1.8.0-prebeta release execution as gated.
Minimal Scope: Plan local-only provider path readiness state, provider path eligibility, provider selection and configuration envelope, consent requirement state, provider-visible-data requirement posture, setup eligibility/capability alignment, Core/Desktop/ORIN provider path and consent posture, validator fixtures, expected branch-count forecast, and v1.8.0-prebeta direction. This pass does not perform provider setup, consent collection, provider SDK/model/memory/voice/Core/shortcut/installer/release implementation.
Selected Next Implementation Branch: None after PR #177 merge.
Current Carrier Branch: None.
Selected Next Current-Carrier Note: `feature/fam-007-local-ai-provider-path-and-consent-readiness` is historical merged-unreleased PR #177 evidence; `feature/fam-007-local-ai-provider-execution-readiness-gates` is historical released PR #172 evidence; `feature/fam-007-local-ai-provider-activation-foundation` is historical released PR #170 evidence; `feature/fam-007-local-ai-provider-runtime-readiness` is historical released PR #165 evidence.
Current Carrier Branch Note: Branch Readiness Stage 2 created a fresh FAM-007 runtime carrier from current `origin/main` after v1.7.7-prebeta release execution. Historical FAM-007 refs remain preserved until a later USER-approved cleanup/rebaseline gate proves no worktree, open PR, or unique commit depends on them.
Runtime Branch Evidence: `feature/fam-007-provider-boundary-no-provider-shell` - PR #138 merged the completed local-only scaffold chain and now serves as released historical branch evidence in v1.7.1-prebeta.
Post-Merge Successor Selection: None after PR #177; successor selection beyond this merged carrier remains pending USER approval.
Successor Selection User Approval: Granted for this Stage 2 carrier setup only. FAM-006 and Governance worktrees remain separate and untouched.
Family Scope: Local AI execution posture, capability-pack boundaries, model/tool capability distribution, local-vs-external runtime choices, and capability governance.
Package Policy: Branchable local-AI work must package capability boundary, install/runtime, validation, and documentation slices by default.
Known Pending Gaps: Local AI and capability-pack architecture remains in progress beyond the released local-only scaffolds; this branch records provider path and consent readiness as local-only contract/state/UI/validator planning only. Local model/provider runtime beyond readiness gates, real provider setup flow, consent collection implementation, real provider SDKs, model downloads, full AI Product Contract import, GitHub issue creation, release work, shortcut work, installer work, memory/indexing/learning/personalization implementation, voice/Core sync, v1.8.0-prebeta release execution, and old AI lab branch mutation remain blocked.
Package Admission State: Admitted by USER during Branch Readiness Stage 2 on `feature/fam-007-stage-2-readiness-admission`
Admitted Slice Count: 8
Package Completion State: PR #152 local-only scaffold evidence is released historical evidence in v1.7.2-prebeta; PR #159 local AI runtime foundation evidence is released in v1.7.3-prebeta; PR #162 local AI runtime-expansion evidence is released in v1.7.4-prebeta; PR #165 provider-readiness/setup-eligibility evidence is released in v1.7.5-prebeta; PR #170 activation foundation evidence is released in v1.7.6-prebeta; PR #172 execution-readiness gates evidence is released in v1.7.7-prebeta; PR #177 provider path and consent readiness is merged-unreleased candidate scope / Package not complete - provider setup, consent collection, provider/model runtime, memory/indexing/learning/personalization implementation, voice/Core runtime sync, shortcut/installer work, capability-pack execution, AI Product Contract import, and v1.8.0-prebeta release execution remain separate USER-gated phases
Single-Slice Package User Approval: Not required - `PKG-007` admits eight concrete slices and no single-slice waiver is granted.
Active Branch Authority Record: None.
Historical Branch Authority Records: `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md`; `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md`; `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md`; `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md`; `Docs/branch_records/feature_fam_007_local_ai_runtime_expansion.md`; `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md`; `Docs/branch_records/feature_fam_007_local_ai_foundation_runtime_continuation.md`; `Docs/branch_records/feature_fam_007_local_ai_foundation_readiness.md`; `Docs/branch_records/feature_fam_007_stage_2_readiness_admission.md`; `Docs/branch_records/feature_fam_007_runtime_provider_boundary.md`; `Docs/branch_records/feature_fam_007_provider_boundary_no_provider_shell.md`
Planning Branch Trace: `feature/fam-007-local-ai-foundation-readiness` historical planning carrier; `feature/fam-007-stage-2-readiness-admission` historical admission carrier; `feature/fam-007-runtime-provider-boundary` historical PR #131 governance/readiness carrier; `feature/fam-007-provider-boundary-no-provider-shell` historical PR #134/PR #138 provider-boundary carrier released in v1.7.1-prebeta; `feature/fam-007-local-ai-foundation-runtime-continuation` historical PR #152 carrier released in v1.7.2-prebeta; `feature/fam-007-local-ai-runtime-foundation` historical PR #159 carrier released in v1.7.3-prebeta; `feature/fam-007-local-ai-runtime-expansion` historical PR #162 released carrier in v1.7.4-prebeta; `feature/fam-007-local-ai-provider-runtime-readiness` historical PR #165 released provider-readiness/setup-eligibility carrier in v1.7.5-prebeta; `feature/fam-007-local-ai-provider-activation-foundation` historical PR #170 activation-foundation carrier released in v1.7.6-prebeta; `feature/fam-007-local-ai-provider-execution-readiness-gates` historical PR #172 execution-readiness carrier released in v1.7.7-prebeta; `feature/fam-007-local-ai-provider-path-and-consent-readiness` historical PR #177 provider path and consent readiness carrier merged-unreleased for v1.7.8-prebeta candidate.
Planning Worktree Trace: historical D-drive planning worktree removed; GitHub Desktop FAM-007 alias conflict found on `C:\Nexus Desktop AI`; current FAM-007 GitHub Desktop repo/worktree is `C:\Nexus Worktrees\FAM-007` for FAM-007-only work.
AI Product Contract v0.6.2 Status: USER-provided planning evidence only; not repo source truth, not fully imported, and not implementation authority.
Current Branch vs Future Package Boundary: PR #159 released Workstream Green, Hardening H1 Green, Live Validation LV1 Green, and PR Readiness proof for local runtime foundation state covering provider-boundary/no-provider posture, hardware profiling posture, provider routing contracts, capability-pack manifests, data classification, resilience, persona/Core status, proof gates, and merge-stable no-active branch authority. PR #162 completed, hardened, LV1-validated, PR-readied, merged, and released the next local runtime-contract Workstream through SLC-036 as local-only scaffolds. PR #165 released the provider readiness/setup eligibility layer in v1.7.5-prebeta as local-only readiness state, setup eligibility/blocker state, readiness reason/provenance/schema fields, capability-pack eligibility/install-intent posture, Core/Desktop readiness copy, and validator fixtures. PR #170 released activation foundation as local-only activation state, gate, null adapter, functional-AI criteria, v1.8.0-prebeta readiness criteria, visible copy, and validator scaffolding. PR #172 released local-only execution-readiness gates: provider execution readiness state, prompt/model readiness gates, provider path/adapter selection posture, provider-visible-data execution proof, network/data/safety blockers, v1.8.0 criteria, Core/Desktop/ORIN copy, and validator fixtures. PR #177 merged provider path and consent readiness as local-only path readiness, provider selection/config envelope, consent requirement, data visibility, setup eligibility/capability alignment, UI posture, and validator evidence for the v1.7.8-prebeta candidate. Real provider setup, consent collection, provider SDKs, model downloads/execution, external calls, memory/indexing/learning/personalization implementation, voice/Core runtime sync, shortcut/installer work, setup wizard, beta feedback, Dev ORIN surfaces, issue work, release execution, v1.8.0-prebeta release execution, and successor selection remain future USER decisions.
Interface Release Boundary: Primary interface is the existing Core/provider-visible local AI status surface. This branch improves local provider path and consent readiness planning inside that boundary only. It does not ship a real provider, local model, memory, external provider call, capability-pack install/update interface, shortcut, installer, or new multi-interface bundle without later USER approval.
Workstream Blockers: Live Validation LV1 approval is pending after Workstream Green and H1 Green. Provider path/setup implementation, consent collection, release execution, issue closeout, branch/worktree cleanup, successor selection beyond this branch, provider SDK/model execution, downloads, external calls, memory/indexing/learning/personalization, voice/Core runtime sync, shortcut/installer work, AI Product Contract import, Private Dev ORIN import, FAM-006 mutation, Governance mutation, and v1.8.0-prebeta release execution remain separate pending USER decisions. FAM-006 and Governance worktrees are separate lanes and must not be touched by this FAM-007 carrier without a clear USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-007` | `FAM-007` | Local AI foundation and capability-pack architecture package | Admitted / PR #152 released local-only scaffold evidence / PR #159 released runtime foundation evidence / PR #162 released runtime-expansion evidence / PR #165 released provider-readiness evidence / PR #170 released activation-foundation evidence / PR #172 released execution-readiness evidence / PR #177 provider path and consent readiness merged-unreleased evidence | Prior local-only scaffolds are released historical evidence through v1.7.7-prebeta; PR #177 is merged-unreleased candidate scope for provider path and consent readiness while future provider setup/model work remains USER-gated | `feature/fam-007-local-ai-provider-path-and-consent-readiness`; `feature/fam-007-local-ai-provider-execution-readiness-gates`; `feature/fam-007-local-ai-provider-activation-foundation`; `feature/fam-007-local-ai-provider-runtime-readiness`; `feature/fam-007-local-ai-runtime-expansion`; `feature/fam-007-local-ai-runtime-foundation`; `feature/fam-007-local-ai-foundation-runtime-continuation`; `feature/fam-007-stage-2-readiness-admission`; `feature/fam-007-provider-boundary-no-provider-shell`; `Docs/orin_vision.md`; historical branch authority record `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md`; historical branch authority record `Docs/branch_records/feature_fam_007_local_ai_provider_execution_readiness_gates.md`; historical branch authority record `Docs/branch_records/feature_fam_007_local_ai_provider_activation_foundation.md`; historical branch authority record `Docs/branch_records/feature_fam_007_local_ai_provider_runtime_readiness.md`; historical branch authority record `Docs/branch_records/feature_fam_007_local_ai_runtime_expansion.md`; historical branch authority record `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md` | No legacy FB; repo vision trace plus USER planning evidence only |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-017` | `PKG-007` | `FAM-007` | Local AI shell, Assisted Desktop Mode, and no-provider behavior | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; no-provider fallback, provider-selection scaffold, disabled Assisted Desktop no-provider interaction surface, no-provider fallback compatibility, and LV1 waiver proof complete |
| `SLC-018` | `PKG-007` | `FAM-007` | Provider boundary and visible privacy/provider state | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; visible provider/privacy/consent state, provider-visible-data disclosure, local-only consent posture, local provider registry/configuration state, and LV1 waiver proof complete |
| `SLC-031` | `PKG-007` | `FAM-007` | Hardware safety, power state, and GPU/CPU capability routing | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; local hardware/capability state planning, GPU unprobed, CPU fallback preserved, power/thermal guardrail posture, no model execution, and LV1 waiver proof complete |
| `SLC-032` | `PKG-007` | `FAM-007` | Model and capability-pack lifecycle | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; model/capability-pack lifecycle planned, not installed, downloads blocked, and LV1 waiver proof complete |
| `SLC-033` | `PKG-007` | `FAM-007` | Data classification, memory, context, consent, audit, and secrets | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; local-only classification, memory/context disabled, no indexing, no secrets stored, consent/audit posture visible, and LV1 waiver proof complete |
| `SLC-034` | `PKG-007` | `FAM-007` | Windows compatibility, resilience, and installer/platform posture | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; Windows resilience/offline-degraded planning visible, no shortcut/installer/startup/process-owner changes, and LV1 waiver proof complete |
| `SLC-035` | `PKG-007` | `FAM-007` | ORIN/ARIA persona shell, progress presence, and Core/voice sync planning | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; persona/Core/voice planning boundary visible, voice runtime disabled, no Core/voice sync implementation, and LV1 waiver proof complete |
| `SLC-036` | `PKG-007` | `FAM-007` | Validation, evaluation, abuse testing, and release proof gates | Admitted | Live Validation | Green / PR #159 merged-unreleased | `feature/fam-007-local-ai-runtime-foundation`; validation proof gates planned, static proof active, abuse/eval and release proof pending future approval, and LV1 waiver proof complete |

Element Coverage Review: user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD impact, validation, and release impact are planned coverage for the admitted package; Element Coverage remains non-identity and does not add slices beyond the admitted rows.
Acceptance Criteria: current branch acceptance requires branch authority and selected-next truth plus visible no-provider/provider-privacy, provider-selection/consent, provider-registry/configuration, hardware/capability, capability-pack lifecycle, data/memory/consent/audit/secrets, Windows resilience, persona/Core/voice, proof-gate scaffolds, provider readiness/setup eligibility state, setup blocker state, readiness reason/provenance/schema fields, capability-pack eligibility/install-intent posture, Core/Desktop readiness copy, and validator fixtures that validate local-only, disabled/unavailable, future-gated, and no-provider semantics. Future runtime acceptance for real providers, models, memory, voice/Core, shortcuts, installers, and capability packs requires separate Workstream/Hardening/Live Validation proof.
Summary: Local AI and Capability Packs starts fresh as a broad family without reusing old `FB` numbering. PKG-007 remains admitted but not package-complete; PR #138 scaffold evidence is released in v1.7.1-prebeta, PR #152 local-only continuation is released in v1.7.2-prebeta, PR #159 local-only runtime foundation scope is released in v1.7.3-prebeta, PR #162 released `feature/fam-007-local-ai-runtime-expansion` in v1.7.4-prebeta as local runtime-contract scope with SLC-017/SLC-018 and SLC-031 through SLC-036 runtime-contract scaffolds green after Workstream validation, Hardening H1 proof review, Live Validation LV1 waiver/applicability review, and PR Readiness, PR #165 is released provider-readiness/setup-eligibility evidence in v1.7.5-prebeta, PR #170 is released activation-foundation evidence in v1.7.6-prebeta, PR #172 is released execution-readiness evidence in v1.7.7-prebeta, and PR #177 is merged-unreleased provider path and consent readiness evidence for the v1.7.8-prebeta candidate. No local model runtime, real provider setup, consent collection implementation, real provider SDK integration, memory/indexing/learning/personalization implementation, voice/Core runtime sync, Dev ORIN, shortcut, installer, release, v1.8.0-prebeta execution, or capability-pack installation work is admitted without later USER-approved Workstream scope.

### [ID: FAM-008] Packaging and Install Experience

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Installer, modular setup, GPU-aware runtime selection, dependency packaging, desktop-shortcut installation, release packaging ergonomics, and operator install/upgrade experience.
Package Policy: Branchable packaging/install work must package installer architecture, runtime detection, user copy, and validation slices by default.
Known Pending Gaps: Modular install and GPU-aware architecture remain pending and must not be collapsed into a small single-seam branch.
Package Admission State: Pending USER approval / no active package admission
Admitted Slice Count: 0
Package Completion State: Pending
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-008` | `FAM-008` | Modular install and GPU-aware runtime package | Pending | Pending | `Docs/orin_vision.md`; `Docs/architecture.md` | No legacy FB; repo vision trace only |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-019` | `PKG-008` | `FAM-008` | Modular install architecture and desktop installation path | Future Placeholder | Pending USER-approved package | Not Admitted | Future Branch Readiness required |
| `SLC-020` | `PKG-008` | `FAM-008` | GPU-aware runtime/dependency selection and validation | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Packaging and Install Experience keeps installer and GPU-aware runtime work as a broad family package, not a one-off branch.

### [ID: FAM-009] Workspace and Data

Status: Open / deferred follow-through
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Low
Family Scope: Workspace paths, data organization, durable state, conversation/project storage, source-of-truth migration, and folder/data hygiene.
Package Policy: Branchable workspace/data work must package storage, migration, validation, and UX follow-through slices by default.
Known Pending Gaps: Workspace and data follow-through remains open even though earlier folder-organization and migration slices are released historical proof.
Deferred Since: 2026-05-04 one-time backlog governance repair.
Deferred Because: Workspace/data follow-through requires explicit USER-approved package admission under the broad FAM model.
Selection / Unblock: USER approval for a FAM-009 package with multiple workspace/data slices, or an explicit USER-approved deferral change.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-009` | `FAM-009` | Workspace and data truth package | Released baseline / open | Released Baseline / Open | `v1.6.6-prebeta` and historical migration/support trace | `FB-005`, `FB-020`, `FB-026`, `FB-028`, source-of-truth migration evidence |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-021` | `PKG-009` | `FAM-009` | Workspace/folder organization and migration baseline | Historical Evidence | Released | Complete | `FB-005`, `FB-020`, `FB-026`, `FB-028`; historical workstream/release trace |
| `SLC-022` | `PKG-009` | `FAM-009` | Durable workspace/data UX and follow-through | Deferred Placeholder | Deferred USER-approved package | Deferred | Future package seam required |

Summary: Workspace and Data keeps old data/workspace IDs as trace while remaining open for broader data-product follow-through.

### [ID: FAM-010] Safety and Privacy

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Privacy posture, local execution boundaries, trust/safety copy, consentful integrations, safe automation, model/tool data handling, and license/privacy guardrails.
Package Policy: Branchable safety/privacy work must package policy, runtime behavior, validation, and user-facing copy slices by default.
Known Pending Gaps: Safety/privacy is repo-supported by local-execution and trust/safety vision but has no dedicated USER-approved implementation package yet.
Package Admission State: Pending USER approval / no active package admission
Admitted Slice Count: 0
Package Completion State: Pending
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-010` | `FAM-010` | Safety, privacy, and local-execution package | Pending | Pending | `Docs/orin_vision.md`; `Docs/ownership_ip_plan.md`; governance trace | No legacy FB; repo vision trace only |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-023` | `PKG-010` | `FAM-010` | Privacy/local-execution boundary and user-facing claims | Future Placeholder | Pending USER-approved package | Not Admitted | Future Branch Readiness required |
| `SLC-024` | `PKG-010` | `FAM-010` | Safe automation, consent, and integration guardrails | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Safety and Privacy is a broad product family only; it is not a reused legacy `FB` lane.

### Legacy One-To-One FAM Mapping Trace

The following entries preserve the earlier one-time repair mapping as historical analysis only. They are not parseable live family records, not branchable identities, and not selected-next candidates under the broad FAM -> Package -> Slice -> Seam model.

#### [Legacy Mapping: FAM-001] Active-session pre-settled incoming-launch conflict truth

Legacy FB ID: FB-049
Status: Released
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Selection / Unblock: Implemented complete. `feature/fb-049-runtime-branch-readiness` delivered the pre-settled incoming-launch conflict truthful-exit proof, and PR #107 merged into `main` at `2026-05-01T22:17:44Z`.
Next Workstream: Historical complete
Branch Creation Gate: Historical complete; BR1 cleared the carried PR #106 stale active-branch blocker before implementation started.
Branch: feature/fb-049-runtime-branch-readiness
Branch Readiness: Historical complete. BR1 cleared stale active-branch authority from the merged PR #106 closeout branch before runtime implementation started.
Workstream: Historical complete. WS1 implemented and validated the pre-settled incoming-launch conflict truthful-exit proof.
Hardening: Historical complete. `Hardening H1 - Pre-Settled Incoming-Launch Conflict Validation` validated the WS1 runtime proof.
Live Validation: Green. `Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation` passed with real desktop shortcut evidence, closest available live-equivalent pre-settled conflict proof, and a User Test Summary waiver recorded in the branch authority record.
PR Readiness: Historical complete with failure classification. PR #107 merged, GitHub merge truth is valid, and `PR Watcher Merge Handoff Missing` is preserved because `pr107-same-thread-merge-watch` did not emit the required same-thread merged handoff before cleanup.
Minimal Scope: Prove and refine the pre-settled incoming-launch conflict lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so startup-phase ownership stays explicit, incoming launches exit truthfully before authoritative settled is reached, and settled-session relaunch semantics are not falsely claimed.
Historical Merge Truth: PR #107 merged into `main` at `2026-05-01T22:17:44Z`; merge commit `22dfb15e554472220b9621b01439286b3afe1dda`; head SHA `fc00346b111158c6f57d976fef7a215a940027c1`.
Watcher Failure Truth: same-thread watcher handoff missing; watcher cleanup proven; carried into FAM-004 legacy FB-030 Branch Readiness as `PR Watcher Merge Handoff Missing` plus `Blocker Recurrence Analysis Required`.
Release Stage: Released
Latest Released Runtime Proof Version: v1.6.13-prebeta
Release Title: Pre-Beta v1.6.13
Latest Public Prerelease: v1.7.0-prebeta
Release Readiness: Released historical traceability in `v1.6.13-prebeta`.
Release Execution: `v1.6.13-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.13-prebeta on commit `faaf991d2579dd6478f78245d56956858cc2f59b`.
Summary: Make startup-phase incoming-launch conflicts as truthful as settled-session relaunch conflicts.
Why it matters: Users should get an explicit, proven outcome when a second launch collides with an already-owning startup-phase session before the desktop has reached authoritative settled state.

#### [Legacy Mapping: FAM-002] Desktop startup runtime family anchor

Legacy FB ID: FB-042
Status: Released (v1.6.7-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Low
Release Stage: Released
Target Version: v1.6.7-prebeta
Release Title: Pre-Beta v1.6.7
Selection / Unblock: Implemented for the first bounded runtime/user-facing slice. `feature/fb-042-desktop-entrypoint-runtime-refinement` delivered WS-1 desktop shortcut launch-path runtime refinement, the branch merged through PR #86, PR #87 cleared the final release-debt marker drift, and `v1.6.7-prebeta` is now published and validated.
Branch: feature/fb-042-desktop-entrypoint-runtime-refinement
Canonical Workstream Doc: Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md
Lifetime Dossier Doc: Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md
Lifetime Dossier State: Structured shell with partial historical pass migration. Phase 4 / Slice R4-S1 introduced the dossier shell, Phase 4 / Slice R4-S3 added pass index and slice/seam ledger templates, Phase 4 / Slice R4-S4 added validator/helper and artifact index templates, Phase 4 / Slice R4-S5 validated dossier stability, Phase 5 / Slice R5-S1 converted FB-043 through FB-048 into explicit historical pass records while populating the dossier pass index plus slice/seam ledger summary rows, and Phase 5 / Slice R5-S3 converted the preserved corresponding branch-readiness records; validator/helper and artifact migration remain pending.
Branch Readiness: Complete. Planning/framing now happens before Workstream, and the admitted WS-1 slice is recorded with owned paths, non-goals, validation coverage, rollback limits, and user-facing shortcut contract in the canonical workstream doc.
Workstream: Released. WS-1 desktop shortcut launch-path runtime refinement is complete and validated on the real `launch_orin_desktop.vbs` -> `desktop/orin_desktop_launcher.pyw` -> `desktop/orin_desktop_main.py` path, H-1 hardening is complete, LV-1 is complete, and release publication is complete.
Branch Meaning: Historical source-branch execution owned the real desktop entrypoint/runtime launch path, and that bounded runtime slice now serves as the first released historical proof under this runtime family anchor.
Release Target: v1.6.7-prebeta
Release Floor: patch prerelease
Version Rationale: FB-042 delivers a bounded runtime/user-facing launch-path reliability and startup-error-handling refinement on the existing desktop entrypoint path, but it does not introduce a new product lane, broader runtime family, or materially expanded capability beyond the shipped launch chain.
Release Scope: WS-1 launch-path fallback hardening in `launch_orin_desktop.vbs`, direct user-facing startup failure dialog handling when no usable windowed Python launcher exists, launch-chain validator expansion across default and forced-fallback VBS paths, H-1 fallback-contract correction for `py -0p` / Python 3 launcher proof, real desktop shortcut validation evidence, PR package history, and merged-unreleased release-debt truth for the bounded FB-042 runtime slice only.
Release Artifacts: Tag v1.6.7-prebeta; release title Pre-Beta v1.6.7; rich Markdown release notes summarize the bounded FB-042 desktop launch-path runtime refinement, fallback hardening, real shortcut evidence, and selected-next top-level entrypoint successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Current Active Workstream: None
Promotion Gate: Historical proof complete. `v1.6.7-prebeta` was published and validated, updated `main` was revalidated, and FB-043 then completed its promoted runtime workstream on `feature/fb-043-top-level-entrypoint-handoff-refinement`.
Minimal Scope: Execute only WS-1 desktop shortcut launch-path runtime refinement across `launch_orin_desktop.vbs`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and `dev/orin_desktop_entrypoint_validation.py`, while keeping `main.py`, broader workspace follow-through, audio, logs, visual assets, and installer redesign out of scope.
Summary: Anchor the desktop startup runtime family at the real launch path while preserving the released FB-042 slice as the first historical proof.
Why it matters: Future launch-path, handoff, and relaunch follow-through should reuse one runtime family identity instead of drifting into separate near-duplicate feature-family records.

#### [Legacy Mapping: FAM-003] Monitoring, thermals, and performance HUD surface

Legacy FB ID: FB-040
Status: Released (v1.6.0-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.0-prebeta
Release Title: Pre-Beta v1.6.0
Branch: feature/fb-040-monitoring-thermals-performance-hud-surface
Canonical Workstream Doc: Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md
Release Target: v1.6.0-prebeta
Release Floor: minor prerelease (historical published tag; future architecture-only milestones must not use minor solely because they define a planning lane)
Version Rationale: FB-040 was published as `v1.6.0-prebeta`; post-release repair records the live release as canonical while governance now treats architecture-only, non-user-facing planning/admission milestones as patch-floor by default unless they deliver an executable or user-facing capability lane.
Release Scope: Architecture-only monitoring and thermal source mapping, ownership vocabulary, lifecycle/trust-safety framing, validation/admission contract definition, hardening pressure test, and Live Validation waiver truth for the current non-user-facing milestone.
Release Artifacts: Tag v1.6.0-prebeta; release title Pre-Beta v1.6.0; inclusion-only release notes summarize the FB-040 monitoring and thermal architecture milestone, source-map boundaries, lifecycle/trust-safety handling, validation/admission contract, hardening result, and Live Validation waivers.
Post-Release Truth: FB-040 is Released / Closed in v1.6.0-prebeta; release debt is clear; FB-031 Branch Readiness is admitted on `feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning`.
Version Drift Note: FB-040 advanced the public prerelease from `v1.5.0-prebeta` to `v1.6.0-prebeta`; because the delivered milestone was architecture-only and non-user-facing, future equivalent milestones must use patch prerelease advancement unless a true runtime, executable, or user-facing capability lane is delivered.
Summary: Track future runtime monitoring and HUD surfaces for GPU / CPU thermals and performance, including possible plugin-fed telemetry inputs.
Why it matters: Monitoring overlays are a separate runtime and status surface and should not be bolted onto the saved-action system without an explicit product boundary.

#### [Legacy Mapping: FAM-004] External trigger and plugin integration architecture

Legacy FB ID: FB-039
Status: Released (v1.5.0-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.5.0-prebeta
Release Title: Pre-Beta v1.5.0
Branch: feature/fb-039-external-trigger-plugin-integration-architecture
Canonical Workstream Doc: Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md
Release Target: v1.5.0-prebeta
Release Floor: minor prerelease
Version Rationale: FB-039 created the external trigger and plugin integration architecture lane with an internal trigger intake boundary, so it was a new pre-Beta capability lane rather than patch-only UX, sequencing, or governance repair.
Release Scope: Internal-only external trigger intake architecture and runtime boundary, including source map, ownership vocabulary, lifecycle/trust framing, in-memory registration, bounded invocation follow-through, lifecycle transitions, decision evidence, boundary snapshots, readiness inspection, readiness sweep, readiness summary, and readiness detail snapshot.
Release Artifacts: Tag v1.5.0-prebeta; release title Pre-Beta v1.5.0; inclusion-only release notes summarize the FB-039 internal-only trigger intake milestone, capabilities, system behavior, validation evidence, and Live Validation waivers.
Post-Release Truth: FB-039 is Released / Closed in v1.5.0-prebeta; release debt is clear; FB-040 Branch Readiness is admitted on `feature/fb-040-monitoring-thermals-performance-hud-surface`.
Summary: Track future plugin and integration lifecycle design for external trigger surfaces such as Stream Deck and other installed integration points.
Why it matters: Plugin-backed action triggering needs explicit lifecycle, safety, and ownership boundaries before it becomes part of the product.

#### [Legacy Mapping: FAM-005] Nexus Desktop AI UI/UX overhaul planning

Legacy FB ID: FB-031
Status: Released (v1.6.1-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.1-prebeta
Release Title: Pre-Beta v1.6.1
Branch: feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning
Canonical Workstream Doc: Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md
Minimal Scope: Define the Nexus-era UI/UX overhaul planning boundary, source map, visual-language ownership, lifecycle/interaction-state framing, validation contract, and explicit non-goals before any UI implementation, runtime behavior, settings work, launcher work, or release work is considered.
Release Target: v1.6.1-prebeta
Release Floor: patch prerelease
Version Rationale: FB-031 is architecture-only UI/UX planning and implementation-admission canon with no executable, runtime, operator-facing, user-facing, or materially expanded product capability; per governance, architecture-only planning/admission work used patch prerelease advancement from v1.6.0-prebeta to v1.6.1-prebeta.
Release Scope: Architecture-only Nexus Desktop AI UI/UX source map, visual-language ownership vocabulary, lifecycle and interaction-state framing, future UI implementation admission contract, hardening pressure test, Live Validation repo-truth and waiver classification, PR Readiness merge-target canon, and PR-R1 release-floor validator repair.
Release Artifacts: Tag v1.6.1-prebeta; release title Pre-Beta v1.6.1; inclusion-only release notes summarize the FB-031 UI/UX architecture milestone, source-map and lifecycle/state boundaries, validation/admission contract, hardening result, Live Validation waivers, clean branch history, and PR-R1 release-floor validator repair.
Post-Release Truth: FB-031 is Released / Closed in v1.6.1-prebeta; release debt is clear; FB-032 PR Readiness is green on PR #73.
Summary: Preserved Nexus-era UI/UX overhaul planning as a deliberate design lane rather than piecemeal visual drift.
Why it matters: The Nexus-era visual language should be planned coherently before any later UI implementation pass.

#### [Legacy Mapping: FAM-006] ORIN voice/audio direction refinement

Legacy FB ID: FB-030
Status: Released
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.13-prebeta
Selection / Unblock: Implemented complete. `feature/fb-030-voice-audio-runtime-branch-readiness` delivered the bounded voice/audio runtime availability and truthful diagnostics proof, PR #108 merged into `main`, watcher verification proof exists through a forced run, and PR108 watcher automations are retired.
Next Workstream: Historical complete
Branch: feature/fb-030-voice-audio-runtime-branch-readiness
Canonical Workstream Doc: Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md
Branch Readiness: Historical complete. BR1 repaired the carried FB-049 post-merge stale-canon blocker, recorded the watcher handoff failure classification, and admitted the first bounded runtime diagnostics slice before implementation.
Workstream: Historical complete. WS1 implemented truthful `available`, `degraded`, `unavailable`, and `bypassed` voice/audio diagnostics without false success claims.
Hardening: Historical complete. H1 validated the diagnostics contract across voice, error-voice, launcher, main runtime, and regression-harness surfaces.
Live Validation: Historical complete. LV1 validated live-equivalent voice/audio diagnostic behavior and preserved launcher/runtime compatibility proof.
PR Readiness: Historical complete. PR #108 merged, watcher verification proof exists through a forced run, and PR108 watcher automations are retired.
Release Readiness: Released historical traceability in `v1.6.13-prebeta`.
Release Execution: Historical `v1.6.5-prebeta` planning release remains live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.5-prebeta on commit `7c2933d6427feb08a1139ba7f5ba2393eb61f1e1`; the runtime diagnostics follow-through is publicly released in `v1.6.13-prebeta` at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.13-prebeta on commit `faaf991d2579dd6478f78245d56956858cc2f59b`.
Released Historical Scope: FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth plus FAM-004 legacy FB-030 voice/audio runtime diagnostics proof plus merged governance/automation proof package plus PR #112 source-truth closeout / merge-target authority hardening proof plus PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta
Repo State: No Active Branch
Latest Public Prerelease: v1.7.0-prebeta
Release Title: Pre-Beta v1.6.13
Release Target: None - released in v1.6.13-prebeta.
Release Floor: none - release execution is complete.
Version Rationale: FAM-004 legacy FB-030 added bounded runtime diagnostics truth for voice/audio availability without opening a new feature family or materially widening product scope.
Release Scope: released governance reform, automation catalog proof, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof.
Release Artifacts: Published tag `v1.6.13-prebeta`; published GitHub prerelease title `Pre-Beta v1.6.13`; release notes include generated `What's Changed` and `Full Changelog` sections.
Post-Release Truth: merged governance reform, automation catalog, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening, and PR #113 source-truth closeout / merge-target authority hardening are released historical traceability; release debt is clear; USER-approved selected-next truth points to FAM-006; and product completion is reopened on `feature/fam-006-monitoring-hud-product-surface` with `PKG-006` admitted, prior Workstream/H1 evidence preserved, returned LV1 UTS FAIL evidence rebaselined by Branch Readiness Stage 2-R11, and WS18 Core non-interference plus WS19 dashboard/minimal-HUD split repair recorded before bounded Workstream repair continues.
Selected Next Workstream: None - FAM-006 merged through PR #118 and is released historical traceability in v1.7.0-prebeta.
Next-Branch Creation Gate: Blocked until the governance/canon repair PR merges, updated main validates, and a later Branch Readiness packet admits implementation.
Historical Planning Release: `v1.6.5-prebeta` remains the released planning/admission proof for the original voice/audio direction milestone.
Minimal Scope: Completed WS1 voice/audio runtime availability and truthful diagnostics proof across `Audio/orin_voice.py`, `Audio/orin_error_voice.py`, `main.py`, `desktop/orin_desktop_launcher.pyw`, and `dev/orin_voice_regression_harness.py`, while preserving ORIN as the only shipped persona, keeping ARIA dormant, avoiding prompt or asset redesign, and avoiding public-copy or release-note changes before release phases.
Summary: Turn the released FAM-004 legacy FB-030 voice/audio planning contract into its first bounded runtime truth proof.
Why it matters: Voice execution, quiet mode, diagnostics, and persona claims must stay truthful when speech succeeds, bypasses, or fails.

#### [Legacy Mapping: FAM-007] Interaction and shared-action family anchor

Legacy FB ID: FB-027
Status: Released (v1.2.9-prebeta) / family aggregation hold
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Release Stage: pre-Beta
Selection / Unblock: Released family anchor. Any future same-family runtime continuation requires explicit USER approval before Codex selects, splits, promotes, or branches it.
Next Workstream: None - USER approval required
Selected Next Workstream: None
Selected Next Runtime Slice: None
Selected Next Implementation Branch: Not created
Branch: None
Canonical Workstream Doc: Docs/workstreams/FB-027_interaction_system_baseline.md
Lifetime Dossier Doc: Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md
Lifetime Dossier State: Structured shell with partial historical pass migration. Phase 4 / Slice R4-S2 introduced the dossier shell, Phase 4 / Slice R4-S3 added pass index and slice/seam ledger templates, Phase 4 / Slice R4-S4 added validator/helper and artifact index templates, Phase 4 / Slice R4-S5 validated dossier stability, Phase 5 / Slice R5-S2 converted FB-036, FB-037, FB-038, and FB-041 into explicit historical pass records while populating the dossier pass index plus slice/seam ledger summary rows, and Phase 5 / Slice R5-S3 converted the preserved corresponding branch-record trace where it exists; validator/helper and artifact migration remain pending.
Branch Readiness: Historical PR #109 evidence. BR1 admitted shutdown-hotkey proof before this governance correction reclassified it as family aggregation material rather than an active backlog lane.
Workstream: Historical PR #109 evidence. Current executable contract validates `Ctrl+Alt+End` and `Ctrl+Alt+2` as direct shutdown hotkeys while visible confirmation is owned by tray Exit only; desktop entrypoint validation proves the hotkey path and tray validation proves confirmation separately.
Hardening: Historical PR #109 evidence. H1 validated interaction baseline compatibility, desktop entrypoint compatibility, boot transition compatibility, branch governance, and automation observability review; visible confirmation is now classified as tray Exit scope only.
Live Validation: Historical PR #109 evidence. LV1 passed with closest live-equivalent desktop entrypoint shortcut evidence, interaction-baseline proof for both shutdown hotkeys, tray confirmation proof where applicable, and User Test Summary results recorded as `PASS`.
PR Readiness: Historical PR #109 evidence. PR #109 merged after PR1 live validation, bot-review closeout, and merge-watch proof; it is not a selected-next or active-lane driver.
Release Readiness: Not started and not required for PR #109 as a standalone release driver; historical `v1.2.9-prebeta` baseline release proof remains preserved.
Current Active Workstream: None
Promotion Gate: Closed family anchor. Future continuation requires explicit USER approval under `Backlog Addition User Approval Missing`.
Standalone Release Driver: No
Aggregation Target: Future USER-approved FAM-003 legacy FB-027 family release or larger approved release aggregation.
Minimal Scope: Historical PR #109 aggregation evidence preserves direct shutdown hotkeys for `Ctrl+Alt+End` and `Ctrl+Alt+2` while tray Exit owns the visible confirmation prompt; no next same-family runtime slice is selected.
Summary: Anchor the typed-first interaction and shared-action family while preserving PR #109 as family evidence instead of a release-version driver.
Why it matters: Future authoring, callable-group, built-in action, and tray task follow-through should reuse one interaction/action family identity instead of drifting into separate near-duplicate feature-family records.

### Historical Consolidated Pass Aliases

Former standalone historical pass backlog entries now live here as family traceability only. They are not parseable backlog items, are not independently selectable, and must be loaded through the family dossier plus canonical workstream record named below.

#### FB-042 Desktop Startup Runtime Family Pass Trace

| Former ID | Pass ID | Family Anchor | Source-Of-Truth Record | Lifetime Dossier | Release Trace | Selection State |
| --- | --- | --- | --- | --- | --- | --- |
| `FB-048` | `F042-P07` | `FB-042` | `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.12-prebeta` | Historical family pass only; not selectable |
| `FB-047` | `F042-P06` | `FB-042` | `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.11-prebeta` | Historical family pass only; not selectable |
| `FB-046` | `F042-P05` | `FB-042` | `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.10-prebeta` | Historical family pass only; not selectable |
| `FB-045` | `F042-P04` | `FB-042` | `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.9-prebeta` | Historical family pass only; not selectable |
| `FB-044` | `F042-P03` | `FB-042` | `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.9-prebeta` | Historical family pass only; not selectable |
| `FB-043` | `F042-P02` | `FB-042` | `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.8-prebeta` | Historical family pass only; not selectable |

#### FB-027 Interaction And Shared-Action Family Pass Trace

| Former ID | Pass ID | Family Anchor | Source-Of-Truth Record | Lifetime Dossier | Release Trace | Selection State |
| --- | --- | --- | --- | --- | --- | --- |
| `FB-041` | `F027-P03` | `FB-027` | `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.3.1-prebeta` | Historical family pass only; not selectable |
| `FB-038` | `F027-P05` | `FB-027` | `Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.4.1-prebeta` | Historical family pass only; not selectable |
| `FB-037` | `F027-P04` | `FB-027` | `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.4.0-prebeta` | Historical family pass only; not selectable |
| `FB-036` | `F027-P02` | `FB-027` | `Docs/workstreams/FB-036_saved_action_authoring.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.3.0-prebeta` | Historical family pass only; not selectable |

#### [Former ID: FB-048] Active-session relaunch signal-failure and wait-timeout truth

Status: Released (v1.6.12-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P07
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.12-prebeta
Selection / Unblock: Implemented complete. `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth` delivered the admitted failure/timeout truth slice chain, the follow-up repair and canon/governance containment PRs are merged on `main`, and `v1.6.12-prebeta` is now published, validated, and closed through post-release canon sync.
Historical Follow-Through: repo-level selected-next truth later moved to FB-049 after this release window; this alias record does not independently own successor selection.
Branch Creation Gate: Satisfied during FB-048 Branch Readiness after `v1.6.11-prebeta` publication, validation, updated-`main` revalidation, and first-slice admission.
Branch: feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth
Canonical Workstream Doc: Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md
Historical Branch Readiness Record: Docs/branch_records/feature_fb_048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md
Branch Readiness: Historical complete. The branch objective, target end-state, admitted WS-1 slice, validation coverage, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical Branch Readiness record.
Workstream: Released. WS-1 `accepted relaunch failure-path truthful outcome proof` is complete and validated; H-1 failure/timeout lifecycle hardening is complete and green; LV-1 is complete and green with real desktop shortcut evidence plus reusable failure/timeout lifecycle proof; accepted relaunch signal-failure emits an explicit preserved-session marker and accepted relaunch wait-timeout emits an explicit replacement-unconfirmed marker instead of collapsing into a generic already-running skip; repeated signal-failure launches preserve the active settled owner even under rapid repetition; near-deadline reacquire no longer falls through to a false timeout; mixed failure -> decline -> accept -> failure sequencing keeps failure, decline, and success classification distinct; `Backlog Completion State` is `Implemented Complete`; PR #94, PR #96, and PR #97 are complete historical proof; the lane is released and closed in `v1.6.12-prebeta`; and the branch's governance/validator hardening is now part of the released canonical baseline.
Backlog Completion State: Implemented Complete
PR Readiness: Complete historical proof. PR #94 merged the bounded FB-048 implementation package; PR #96 merged the post-merge review repair that corrected wait-timeout truth and the non-Windows validator guard; and PR #97 merged the post-sync canon plus merge-stable governance containment on `main`.
Release Target: v1.6.12-prebeta
Release Floor: patch prerelease
Version Rationale: FB-048 delivers a bounded runtime/user-facing relaunch signal-failure and wait-timeout refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-048 WS-1 accepted relaunch failure-path truthful outcome proof, H-1 failure/timeout lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, PR package history, merged-unreleased release-debt truth, selected-next FB-049 successor lock, and merge-stable current-state governance hardening plus validator guardrails for the bounded runtime/user-facing lane only.
Release Artifacts: Tag v1.6.12-prebeta; release title Pre-Beta v1.6.12; rich Markdown release notes summarize the bounded FB-048 relaunch failure/timeout runtime/user-facing package, real shortcut evidence, and the FB-049 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-048 is Released / Closed in `v1.6.12-prebeta`; release debt is clear; the governance reform branch may proceed through its approved docs-only branch-authority record; and FB-049 remains selected next, `Registry-only`, and branch-not-created until that branch completes and later FB-049 Branch Readiness admits the first bounded pre-settled incoming-launch conflict truth slice.
Minimal Scope: Prove and refine the accepted relaunch failure lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so relaunch-signal failure or reacquire wait-timeout preserves truthful ownership, emits explicit failure-path markers, and avoids false replacement-session or guard-transfer claims.
Summary: Make accepted-but-unfinished relaunch failures as truthful as accepted and declined success paths.
Why it matters: Users should get an explicit, proven outcome when relaunch was requested but the current session could not be signaled or did not release in time.

#### [Former ID: FB-047] Active-session relaunch decline session-preservation proof

Status: Released (v1.6.11-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P06
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.11-prebeta
Selection / Unblock: Implemented complete. `feature/fb-047-active-session-relaunch-decline-preservation` delivered the admitted decline-preservation slice chain, PR #93 merged into `main`, and `v1.6.11-prebeta` is now published, validated, and closed through post-release canon sync.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-047 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch Creation Gate: Historical complete. `v1.6.10-prebeta` was published and validated, updated `main` was revalidated, and FB-047 Branch Readiness admitted the bounded runtime/user-facing relaunch-decline preservation slice before promotion.
Branch: feature/fb-047-active-session-relaunch-decline-preservation
Canonical Workstream Doc: Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md
Historical Branch Readiness Record: Docs/branch_records/feature_fb_047_active_session_relaunch_decline_preservation.md
Branch Readiness: Historical complete. The branch objective, target end-state, admitted WS-1 slice, validation contract, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical branch-readiness record.
Workstream: Released. WS-1 `declined relaunch incoming-launch truthful exit proof` is complete and validated; harness-driven decline proof records explicit preserved-session success markers instead of a generic already-running skip; repeated incoming declined launches preserve the active settled session and never emit replacement-session markers; H-1 decline-lifecycle hardening is complete / green; LV-1 real desktop shortcut evidence and reusable decline-lifecycle proof are complete / green; `Backlog Completion State` is `Implemented Complete`; PR-1 / PR-2 / PR-3 are complete historical proof; and the branch is now Released / Closed in `v1.6.11-prebeta`.
Backlog Completion State: Implemented Complete
PR Readiness: Complete. PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus validation are complete historical proof; PR #93 merged into `main` at `4ca70572fbc8033bc96fcd299dd309464e81393a`.
Release Target: v1.6.11-prebeta
Release Floor: patch prerelease
Version Rationale: FB-047 delivers a bounded runtime/user-facing relaunch-decline preservation refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-047 WS-1 declined relaunch incoming-launch truthful exit proof, H-1 decline lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, PR package history, release publication, and selected-next FB-048 successor admission for the bounded runtime/user-facing lane only.
Release Artifacts: Tag v1.6.11-prebeta; release title Pre-Beta v1.6.11; rich Markdown release notes summarize the bounded FB-047 relaunch-decline preservation runtime/user-facing package, real shortcut evidence, and the FB-048 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-047 is Released / Closed in `v1.6.11-prebeta`; release debt is clear; and later runtime-family continuation moved through FB-048 on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth` while this alias entry remained released historical proof.
Minimal Scope: Prove and refine the relaunch-decline lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so declining replacement preserves the active settled session and cleanly terminates the incoming launch without dual ownership or false successor markers.
Summary: Make relaunch decline as provable and truthful as accepted relaunch.
Why it matters: The runtime should be just as explicit when the user keeps the current settled session as when the user accepts replacement.

#### [Former ID: FB-046] Active-session relaunch reacquisition and settled re-entry proof

Status: Released (v1.6.10-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P05
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.10-prebeta
Release Title: Pre-Beta v1.6.10
Selection / Unblock: Implemented complete. `feature/fb-046-active-session-relaunch-reacquisition` delivered the admitted relaunch-reacquisition slice chain, PR #92 merged into `main`, and `v1.6.10-prebeta` is now published and validated.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-046 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch: feature/fb-046-active-session-relaunch-reacquisition
Repair-Only Branch Handling: `feature/fb-046-post-merge-canon-sync` is a bounded repair-only post-merge canon-sync `feature/` branch and does not imply Branch Readiness admission or active branch truth for FB-046.
Canonical Workstream Doc: Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md
Historical Branch Readiness Record: Docs/branch_records/feature_fb_046_active_session_relaunch_reacquisition.md
Branch Readiness: Historical complete. The admitted slice, validation contract, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical branch-readiness record.
Workstream: Released. WS-1 accepted relaunch replacement-session settled re-entry proof is complete and validated; accepted relaunch now proves prior-session shutdown, single-instance guard release, replacement-session reacquisition, replacement-session authoritative settled re-entry, and truthful post-settled lifecycle completion without dual ownership; H-1 relaunch lifecycle hardening is complete and green across slow shutdown, recoverable-exit relaunch, and rapid consecutive relaunch-cycle proof; LV-1 is complete and green with real desktop shortcut evidence plus a focused User Test Summary waiver; `Backlog Completion State` is `Implemented Complete`; and the released branch is now historical proof in `v1.6.10-prebeta`.
Backlog Completion State: Implemented Complete
PR Readiness: Complete. PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus validation are complete; PR #92 merged into `main` at `36cf07495dc8e239b20b11afb5194355b77ffd8b`.
Release Readiness: Complete. `main` validated green for `v1.6.10-prebeta` release packaging before release execution.
Release Execution: `v1.6.10-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.10-prebeta on commit `36cf07495dc8e239b20b11afb5194355b77ffd8b`.
Release Target: v1.6.10-prebeta
Release Floor: patch prerelease
Version Rationale: FB-046 delivers a bounded runtime/user-facing relaunch-reacquisition refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-046 WS-1 accepted relaunch replacement-session settled re-entry proof, H-1 relaunch lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, PR package history, merged-unreleased release-debt truth, and selected-next FB-047 successor lock for the bounded runtime/user-facing lane only.
Release Artifacts: Tag v1.6.10-prebeta; release title Pre-Beta v1.6.10; rich Markdown release notes summarize the bounded FB-046 relaunch-reacquisition runtime/user-facing package, real shortcut evidence, and the FB-047 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-046 is Released / Closed in `v1.6.10-prebeta`; release debt is clear; and after merge FB-047 becomes the merged-unreleased release-debt owner for `v1.6.11-prebeta`, while FB-048 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded relaunch-reacquisition runtime/user-facing pass across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_boot_transition_verification.py`, and the minimum required reusable validator surfaces so a confirmed relaunch request closes the active session, reacquires the runtime guard, and returns the replacement session to authoritative settled state without widening into `main.py`, `Audio/`, `logs/`, `nexus_visual/`, installer work, or broader boot-orchestrator scope.
Summary: Turn accepted relaunch into a full replacement-session completion proof surface instead of a partial signal-and-exit story.
Why it matters: The repo now proves who owns the runtime after relaunch, when the old session is truly gone, and when the replacement session has actually made it back to authoritative settled state.

#### [Former ID: FB-045] Active-session relaunch outcome refinement

Status: Released (v1.6.9-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P04
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.9-prebeta
Release Title: Pre-Beta v1.6.9
Selection / Unblock: FB-045 was selected because updated-main `Release Readiness` for FB-044 found a reproducible post-settled runtime failure after the authoritative settled marker. `feature/fb-045-active-session-relaunch-stability` corrected that lifecycle boundary, merged through PR #90, and is now released historical proof in `v1.6.9-prebeta`.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-045 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch: feature/fb-045-active-session-relaunch-stability
Canonical Workstream Doc: Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md
Historical Branch-Readiness Record: Docs/branch_records/feature_fb_045_active_session_relaunch_stability.md
Branch Readiness: Historical complete. The blocker classification, admitted WS-1 slice, validation contract, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical branch-readiness record.
Workstream: Released. WS-1 `post-settled runtime stability refinement` is complete and validated; H-1 post-settled lifecycle hardening is complete and green; LV-1 live validation is complete and green with real desktop shortcut evidence and a focused User Test Summary waiver; PR-1 / PR-2 / PR-3 are complete historical proof; and the blocker-clearing package is now released historical proof inside `v1.6.9-prebeta`.
Backlog Completion State: Implemented Complete
Minimal Scope: Classify post-settled abnormal renderer exits as a recoverable lifecycle condition after authoritative settled is already proven, keep settled truth authoritative, preserve green startup paths, and avoid widening beyond launcher / validator relaunch-stability scope.
Summary: Clear the FB-044 release blocker by fixing launcher lifecycle classification after settled and proving that result across primary-workspace and disposable-copy validation.
Why it matters: Keeps startup truth honest, prevents post-settled runtime exits from being mislabeled as startup failure, and unblocks the path back to FB-044 `Release Readiness`.

#### [Former ID: FB-044] Boot-to-desktop handoff outcome refinement

Status: Released (v1.6.9-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P03
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.9-prebeta
Release Title: Pre-Beta v1.6.9
Selection / Unblock: Implemented complete. `feature/fb-044-boot-desktop-handoff-outcome-refinement` delivered WS-1 `desktop-settled handoff outcome refinement`; FB-045 on `feature/fb-045-active-session-relaunch-stability` delivered the blocker-clearing lifecycle follow-through inside the same release window; PR #89, PR #90, and PR #91 merged; and `v1.6.9-prebeta` is now published, validated, and in post-release canon closure.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-044 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch: feature/fb-044-boot-desktop-handoff-outcome-refinement
Canonical Workstream Doc: Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md
Historical Branch Authority Record: Docs/branch_records/feature_fb_044_boot_desktop_handoff_outcome_refinement.md
Branch Readiness: Complete. Historical Branch Readiness truth is preserved in the branch authority record.
Workstream: Released. WS-1 `desktop-settled handoff outcome refinement` is complete and validated; H-1 settled-state hardening is complete and green; LV-1 live validation is complete and green with real desktop shortcut evidence and a narrow User Test Summary waiver; PR-1 / PR-2 / PR-3 are complete historical proof; `Backlog Completion State` is `Implemented Complete`; FB-045's blocker-clearing lifecycle follow-through is released historical proof in the same package; and `v1.6.9-prebeta` is now live and validated.
Release Target: v1.6.9-prebeta
Release Floor: patch prerelease
Version Rationale: FB-044 delivers a bounded runtime/user-facing boot-to-desktop settled-outcome refinement on the existing startup family without opening a new product lane or materially expanded runtime family.
Release Scope: complete the bounded FB-044 settled-outcome slice chain on this same branch across `main.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_boot_transition_verification.py`, and `dev/orin_desktop_entrypoint_validation.py`, along with H-1, LV-1, PR package history, release publication, and the released FB-045 blocker-clearing lifecycle follow-through inside the same `v1.6.9-prebeta` package.
Release Artifacts: Tag v1.6.9-prebeta; release title Pre-Beta v1.6.9; rich Markdown release notes summarize the bounded FB-044 boot-to-desktop settled-outcome refinement, the FB-045 blocker-clearing lifecycle classification result, real shortcut evidence, and the FB-046 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded runtime/user-facing boot-to-desktop handoff refinement lane across `main.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_boot_transition_verification.py`, and `dev/orin_desktop_entrypoint_validation.py`, while keeping `Audio/`, `logs/`, `nexus_visual/`, installer work, and broader future boot-orchestrator implementation out of scope.
Summary: Continue the entrypoint/runtime lane by making desktop-settled outcome proof explicit and shared across boot, launcher, renderer, and validation paths.
Why it matters: Builds directly on FB-043's ownership cleanup and turns the remaining boot/desktop proof ambiguity into a bounded runtime-bearing implementation result instead of lingering branch-readiness truth.

#### [Former ID: FB-043] Top-level desktop entrypoint ownership and main.py handoff refinement

Status: Released (v1.6.8-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P02
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.8-prebeta
Release Title: Pre-Beta v1.6.8
Selection / Unblock: Implemented complete. `feature/fb-043-top-level-entrypoint-handoff-refinement` delivered WS-1 `main.py` direct-launch handoff refinement plus WS-2 explicit launch-intent refinement, the branch merged through PR #88, and `v1.6.8-prebeta` is now published and validated.
Branch: feature/fb-043-top-level-entrypoint-handoff-refinement
Repair-Only Branch Handling: `feature/fb-043-release-debt-marker-repair` is a repair-only `feature/` branch and does not imply Branch Readiness admission or active branch truth.
Canonical Workstream Doc: Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md
Branch Readiness: Complete. The former branch-readiness authority on `feature/fb-043-top-level-entrypoint-handoff-refinement` admitted WS-1 with exact owned paths, validation coverage, rollback conditions, same-branch continuation posture, and the branch-level closure rule before promotion.
Workstream: Released. WS-1 `main.py` direct-launch handoff refinement and WS-2 explicit launch-intent refinement are complete and validated; plain no-argument direct `main.py` launches and explicit `--desktop-entrypoint` launches now hand off to the canonical desktop chain; explicit dev boot paths remain verifiable through recognized boot arguments, including the legacy dev launcher's explicit manual/voice contract; invalid direct-launch args now fail fast with guidance; H-1 entrypoint hardening is complete and green; LV-1 live validation is complete and green with real desktop shortcut evidence and a narrow User Test Summary waiver; PR-1 / PR-2 / PR-3 are complete; `Backlog Completion State` is `Implemented Complete`; and the released branch is now historical proof in `v1.6.8-prebeta`.
Release Target: v1.6.8-prebeta
Release Floor: patch prerelease
Version Rationale: FB-043 delivers a bounded runtime/user-facing top-level desktop entrypoint ownership and `main.py` handoff refinement on the existing launch path without opening a new product lane or materially expanded runtime family.
Release Scope: complete the bounded FB-043 top-level entrypoint slice chain on this same branch: WS-1 `main.py` direct-launch handoff refinement plus WS-2 explicit launch-intent refinement across `main.py`, the minimal required launcher-contract surfaces, `dev/orin_desktop_entrypoint_validation.py`, and `dev/orin_boot_transition_verification.py`, along with H-1, LV-1, PR package history, and merged-unreleased release-debt truth.
Release Artifacts: Tag v1.6.8-prebeta; release title Pre-Beta v1.6.8; rich Markdown release notes summarize the bounded FB-043 top-level entrypoint ownership and `main.py` handoff refinement, explicit launch-intent outcome, real shortcut evidence, and the FB-044 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Release Execution: `v1.6.8-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.8-prebeta on commit `5e695af5fada05e4ad6b25731bce328ede8a09ee`.
Post-Release Truth: FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded top-level entrypoint slice chain on this same branch: WS-1 `main.py` direct-launch handoff refinement plus WS-2 explicit launch-intent refinement across `main.py`, the minimal required launcher-contract surfaces, `dev/orin_desktop_entrypoint_validation.py`, and `dev/orin_boot_transition_verification.py`, while keeping `Audio/`, `logs/`, `nexus_visual/`, installer work, and broader workspace reshaping out of scope.
Summary: Continue the desktop entrypoint runtime lane by clarifying and tightening top-level ownership and handoff on the shipped launch path.
Why it matters: Builds directly on FB-042's user-facing launch-path improvement and keeps the next branch implementation-bearing instead of slipping back into planning-only governance work.

#### [Former ID: FB-041] Deterministic callable-group execution layer

Status: Released (v1.3.1-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P03
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: pre-Beta
Target Version: v1.3.1-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md
Summary: Released the first bounded callable-group follow-through execution layer for deterministic linear member execution in stored order with stop-on-failure, terminal success or failure propagation, and runtime progression markers.
Why it matters: FB-041 closes the released FB-036 callable-group execution follow-through by supporting full stored-order group execution without reopening authoring, changing single-action behavior, or widening into scheduling, branching, retries, nested groups, or parallelism.

#### [Former ID: FB-038] Taskbar / tray quick-task UX and Create Custom Task surface

Status: Released (v1.4.1-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P05
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.4.1-prebeta
Release Title: Pre-Beta v1.4.1
Canonical Workstream Doc: Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md
Summary: Released the FB-038 tray quick-task UX milestone, including tray identity/discoverability, tray Open Command Overlay, tray Create Custom Task dialog-open/no-write route, tray-origin create completion through the existing FB-036 authoring path, catalog reload and exact-match resolution, confirm/result execution, and startup first-visible Core Visualization sequencing repair.
Why it matters: Taskbar and tray interaction now has an explicit released UX lane that remains bounded to the shared action model rather than becoming a parallel authoring or launcher surface.

#### [Former ID: FB-037] Curated built-in system actions and Nexus settings expansion

Status: Released (v1.4.0-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P04
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: pre-Beta
Target Version: v1.4.0-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md
Summary: Released the first curated Windows utility built-in catalog under the shared action model, including Task Manager, Calculator, Notepad, and Paint while preserving saved-action override authority, authoring collision protection, confirm/result surfaces, and callable-group behavior.
Why it matters: Standard product actions now feel native and inspectable under the shared action model instead of being pushed into user-defined saved actions as ad hoc customization. Common Windows actions ship as first-class built-ins, while saved actions remain the seam for personal or non-standard tasks.

#### [Former ID: FB-036] Limited saved-action authoring and type-first custom task UX

Status: Released (v1.3.0-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P02
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: pre-Beta
Target Version: v1.3.0-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-036_saved_action_authoring.md
Summary: Released the bounded custom-task authoring, callable-group management, inline group quick-create, and exact-green validation hardening milestone above the locked FB-027 interaction baseline.
Why it matters: Nexus now supports deliberate in-product custom-task and callable-group authoring without reopening the typed-first overlay contract, widening into Action Studio, or weakening exact-match resolution boundaries.

### Support / Architecture / Governance Lanes

Closed support, architecture, and governance lanes are historical traceability only. They are not parseable backlog items under the new governance unless the USER explicitly approves a future major release/support lane.

| Former ID | Historical Lane | Source-Of-Truth Record | Release Trace | Trace Role |
| --- | --- | --- | --- | --- |
| `FB-035` | Support-report release-context fallback hardening | `Docs/workstreams/FB-035_release_context_fallback_hardening.md` | `v1.2.7-prebeta` | Closed support lane trace |
| `FB-034` | Recoverable incident diagnostics surface and failure-class follow-through | `Docs/workstreams/FB-034_recoverable_diagnostics.md` | `v1.2.6-prebeta` | Closed support lane trace |
| `FB-033` | Dev-only startup snapshot harness follow-through | `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md` | `v1.2.4-prebeta` | Closed support lane trace |
| `FB-032` | Nexus-era vision and source-of-truth migration | `Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md` | `v1.6.2-prebeta` | Closed architecture/governance trace |
| `FB-029` | ORIN legal-safe rebrand, future ARIA persona option, and repo licensing hardening | `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md` | `v1.6.4-prebeta` | Closed support lane trace |
| `FB-028` | Relocate launcher history state out of root logs | `Docs/workstreams/FB-028_history_state_relocation.md` | `v1.2.3-prebeta` | Closed support lane trace |
| `FB-025` | Boot and desktop milestone taxonomy clarification | `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md` | `v1.2.5-prebeta` | Closed architecture trace |
| `FB-015` | Boot and desktop phase-boundary model | `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md` | `v1.6.4-prebeta` | Closed architecture trace |
| `FB-005` | Workspace and folder organization | `Docs/workstreams/FB-005_workspace_and_folder_organization.md` | `v1.6.6-prebeta` | Closed support/workspace trace |
| `FB-004` | Future boot orchestrator layer | `Docs/workstreams/FB-004_future_boot_orchestrator_layer.md` | `v1.6.3-prebeta` | Closed architecture trace |

#### [Former ID: FB-035] Support-report release-context fallback hardening

Status: Released (v1.2.7-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.7-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-035_release_context_fallback_hardening.md
Summary: Hardened support-report fallback release-context derivation so generated artifacts use released-canon truth when `.git` metadata is unavailable.
Why it matters: Prevents support bundles and issue drafts from reporting an unreleased higher planned prerelease.

#### [Former ID: FB-034] Recoverable incident diagnostics surface and failure-class follow-through

Status: Released (v1.2.6-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.6-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-034_recoverable_diagnostics.md
Summary: Closed the first recoverable-diagnostics milestone for one explicitly bounded repeated-identical `launch_failed` incident class.
Why it matters: Makes the Class 2/Class 3 boundary explicit without widening diagnostics policy or breaking the manual-reporting boundary.

#### [Former ID: FB-033] Dev-only startup snapshot harness follow-through

Status: Released (v1.2.4-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.4-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md
Summary: Stabilized the env-gated startup snapshot harness as bounded dev-only debugging infrastructure.
Why it matters: Preserves a repeatable startup evidence path without turning it into normal user-facing behavior.

#### [Former ID: FB-032] Nexus-era vision and source-of-truth migration

Status: Released (v1.6.2-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.2-prebeta
Release Title: Pre-Beta v1.6.2
Branch: feature/fb-032-nexus-era-vision-source-of-truth-migration
Canonical Workstream Doc: Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md
Workstream: WS-1 current-vs-historical source-of-truth inventory and naming policy, WS-2 classification and mapping of canonical vs historical surfaces, and WS-3 validation and admission contract for controlled migration execution are complete.
Hardening: H-1 source-of-truth migration frame pressure test is complete.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: PR-1 merge-target canon, PR-2 durable branch truth, and PR-3 live PR validation are complete; PR #73 merged cleanly into `main`.
Release Execution: `v1.6.2-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.2-prebeta on commit `e282072769ec25694928293ce51e144d6a37f611`.
Branch Readiness Governance Repair: GitHub release notes across the live release history were standardized to Markdown release bodies that do not repeat the release title as a leading H1 and that include generated `## What's Changed` and `**Full Changelog**:` sections; Release Readiness governance and validator coverage now require that format before future release execution can be treated as complete.
Minimal Scope: FB-032 kept Nexus-era source-of-truth migration controlled by current-vs-historical naming policy, canonical vs historical surface classification, AI/UI identity routing, canon migration admission rules, and explicit non-goals before any wording migration, persona work, runtime behavior, UI implementation, rebrand execution, or release work is considered.
Release Target: v1.6.2-prebeta
Release Floor: patch prerelease
Version Rationale: FB-032 was architecture-only and canon-only planning, admission, validation, and governance work with no executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Architecture-only Nexus-era source-of-truth inventory, naming policy, surface classification, controlled migration admission contract, governance repairs, hardening, Live Validation waivers, and PR Readiness merge-target canon.
Release Artifacts: Tag v1.6.2-prebeta; release title Pre-Beta v1.6.2; inclusion-only release notes summarize the FB-032 migration frame and governance/validation outcomes.
Post-Release Truth: FB-032 is Released / Closed in v1.6.2-prebeta; release debt is clear; FB-004 is Released / Closed in `v1.6.3-prebeta`, and FB-015 Branch Readiness is selected next on `feature/fb-015-boot-desktop-phase-boundary-model`.
Summary: Preserved the broader Nexus-era vision and source-of-truth migration foundation above future controlled migration work.
Why it matters: The repo now has a controlled identity, naming, and source-of-truth migration frame before deeper wording or implementation normalization begins.

#### [Former ID: FB-029] ORIN legal-safe rebrand, future ARIA persona option, and repo licensing hardening

Status: Released (v1.6.4-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: High
Release Stage: pre-Beta
Target Version: v1.6.4-prebeta
Release Title: Pre-Beta v1.6.4
Deferred Since: current pre-Beta identity backlog registration before FB-032 promotion.
Deferred Because: legal-safe naming, ORIN/ARIA persona posture, and licensing hardening need explicit product/legal approval for implementation-facing execution and must not ride along with source-of-truth migration, UI, runtime, or release work.
Selection / Unblock: FB-029 is admitted only as a docs/canon-only planning milestone on this branch. Any implementation-facing naming, licensing, persona, release, or runtime edit still requires explicit product/legal approval and must remain out of scope unless a later legal surface admits it.
Branch: feature/fb-029-orin-identity-licensing-hardening
Canonical Workstream Doc: Docs/workstreams/FB-029_orin_identity_licensing_hardening.md
Branch Readiness: Complete. The branch objective, target end-state, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 current identity, persona-option, and licensing source-of-truth inventory, WS-2 canonical vs historical identity, persona-option, and licensing boundary framing, and WS-3 validation and admission contract for future identity and licensing implementation are complete.
Hardening: H-1 pressure test of identity inventory, persona-option framing, licensing boundary framing, and future implementation admission rules is complete.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus authenticated PR state validation are complete; PR #76 merged cleanly into `main` at `0897fab768dc07385f83fab81434ba7926ecc4a1`.
Release Readiness: Included in the validated inherited `v1.6.4-prebeta` package on `main` while FB-015 remained the sole release-debt owner before publication.
Release Execution: `v1.6.4-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.4-prebeta on commit `d2268b71feefa062c8117eae29f8ec17879a724f`.
Release Target: v1.6.4-prebeta
Release Floor: patch prerelease
Version Rationale: FB-029 remains a docs/canon-only identity, persona-option, and licensing-planning milestone with no new executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Identity source-of-truth inventory, persona-option boundary framing, licensing boundary framing, implementation admission contract, hardening corrections, Live Validation waivers, PR package history, merged-unreleased package-state repair, and post-merge current-state cleanup.
Release Artifacts: Tag v1.6.4-prebeta; release title Pre-Beta v1.6.4; rich Markdown release notes summarize the FB-015 boundary model and the FB-029 identity/licensing planning frame without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-029 is Released / Closed in v1.6.4-prebeta; FB-015 is also Released / Closed in the same package; FB-030 is Released / Closed in v1.6.5-prebeta; FB-005 is Released / Closed in v1.6.6-prebeta; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Define the Branch Readiness frame for legal-safe ORIN naming, optional future ARIA persona posture, and repo licensing hardening before any naming, licensing, release, runtime, or persona-facing edits begin; Workstream remains docs/canon only unless a later legal surface explicitly widens scope.
Summary: Track future ORIN-era naming, persona, and licensing hardening work without treating the local rebrand overlay as merged truth.
Why it matters: Product identity, legal posture, and repo ownership still need durable future treatment, but not by accidental carry-forward.

#### [Former ID: FB-028] Relocate launcher history state out of root logs

Status: Released (v1.2.3-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.3-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-028_history_state_relocation.md
Summary: Moved launcher-owned historical state out of the live root logs tree into a dedicated state location.
Why it matters: Keeps historical state out of user-visible runtime logs while preserving behavior and fallback rules.

#### [Former ID: FB-025] Boot and desktop milestone taxonomy clarification

Status: Released (v1.2.5-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Low
Release Stage: pre-Beta
Target Version: v1.2.5-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md
Summary: Clarified shared milestone taxonomy between `BOOT_MAIN|...` and `RENDERER_MAIN|...` without collapsing ownership.
Why it matters: Keeps boot and desktop evidence easier to compare while preserving separate ownership boundaries.

#### [Former ID: FB-015] Boot and desktop phase-boundary model

Status: Released (v1.6.4-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: High
Release Stage: Slice-staged
Target Version: v1.6.4-prebeta
Release Title: Pre-Beta v1.6.4
Deferred Since: v2.0 closeout after the FB-015 rev1a phase-boundary clarification.
Deferred Because: the boot/desktop ownership model is clarified at planning level, but no later implementation-facing boundary change has been admitted.
Selection / Unblock: Select when a concrete boot, desktop, startup, trust, or orchestration lane is blocked by unresolved ownership boundaries; Branch Readiness must name the exact ambiguity it resolves.
Priority Review: Raised to High during the FB-004 pre-PR docs governance sync because boot/desktop phase-boundary follow-through is the clearest routine technical successor after FB-004 unless an explicitly approved product/legal, voice, or workspace lane supersedes it.
Branch: feature/fb-015-boot-desktop-phase-boundary-model
Canonical Workstream Doc: Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md
Branch Readiness: Complete. The branch objective, target end-state, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 current boot/desktop boundary inventory and ownership map, WS-2 lifecycle and phase-boundary state framing, and WS-3 validation and admission contract for future boot/desktop boundary implementation are complete.
Hardening: H-1 pressure test of the boot/desktop boundary inventory and ownership map, lifecycle and phase-boundary state framing, and future implementation admission contract is complete.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus authenticated PR state validation are complete; PR #75 merged cleanly into `main` at `3e821e07ff91d814fd7aba9b50819f97d700a301`.
Release Readiness: Complete. `main` validated green for `v1.6.4-prebeta` release packaging before release execution.
Release Execution: `v1.6.4-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.4-prebeta on commit `d2268b71feefa062c8117eae29f8ec17879a724f`.
Release Target: v1.6.4-prebeta
Release Floor: patch prerelease
Version Rationale: FB-015 remains a docs/canon-only boundary inventory, ownership, lifecycle, and implementation-admission milestone with no new executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Boot and desktop phase-boundary inventory, ownership map, lifecycle/state framing, implementation admission contract, hardening corrections, Live Validation waivers, PR package history, post-merge canon repair, and merged-unreleased release-debt truth.
Release Artifacts: Tag v1.6.4-prebeta; release title Pre-Beta v1.6.4; rich Markdown release notes summarize the FB-015 boundary model and governance results without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-015 is Released / Closed in v1.6.4-prebeta; FB-029 is also Released / Closed in the same package; FB-030 is Released / Closed in v1.6.5-prebeta; FB-005 is Released / Closed in v1.6.6-prebeta; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded docs/canon seam chain for current boot/desktop phase-boundary ambiguity, starting with current boundary inventory and ownership mapping before lifecycle framing or implementation-admission rules are extended.
Summary: Preserve the future boot and desktop phase-boundary model above the already-closed milestone taxonomy work.
Why it matters: Keeps boot-versus-desktop ownership planning explicit without reopening the closed taxonomy milestone by inertia.

#### [Former ID: FB-005] Workspace and folder organization

Status: Released (v1.6.6-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Low
Release Stage: Released
Target Version: v1.6.6-prebeta
Release Title: Pre-Beta v1.6.6
Deferred Since: v2.0 closeout after the Step 4 workspace slice; the earlier first workspace slice is preserved in v1.9.0 closeout history.
Deferred Because: remaining workspace movement is path-sensitive and can break imports, launcher routes, logs, or user-facing entrypoints if treated as casual cleanup.
Selection / Unblock: Implemented for the first bounded slice. `feature/fb-005-workspace-path-planning` completed the admitted WS-1 relocation `desktop/orin_desktop_test.py` -> `dev/desktop/orin_desktop_test.py`, the branch merged through PR #83, and `v1.6.6-prebeta` is now published and validated.
Branch: feature/fb-005-workspace-path-planning
Canonical Workstream Doc: Docs/workstreams/FB-005_workspace_and_folder_organization.md
Branch Readiness: Complete. The branch objective, target end-state, approved workspace/path slice, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 `desktop/orin_desktop_test.py` -> `dev/desktop/orin_desktop_test.py` is complete. H-1 is complete. LV-1 is complete. The merged branch delivered its first workspace slice under the earlier path-sensitive posture; future FB-005 follow-through should still prefer same-branch slice completion when that lane is reopened.
PR Readiness: Complete. PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus validation are complete; PR #83 merged into `main` at `873c9b6801802a05bbcef074595e632c0ec9f1d2`.
Release Readiness: Complete. `main` validated green for `v1.6.6-prebeta` release packaging before release execution.
Release Execution: `v1.6.6-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.6-prebeta on commit `deeaa691a79dd01897f6aed82f087970db7019b3`.
Release Target: v1.6.6-prebeta
Release Floor: patch prerelease
Version Rationale: FB-005 delivers a bounded dev-only workspace/path implementation slice and direct path-truth sync with no change to shipped runtime entrypoints, launcher paths, audio paths, logs, visual assets, installer behavior, or user-facing desktop behavior, so patch prerelease remains the correct floor.
Release Scope: the historically released FB-005 WS-1 dev-only desktop test harness relocation from `desktop/orin_desktop_test.py` to `dev/desktop/orin_desktop_test.py`, local path-math preservation, direct workspace-layout truth sync, hardening corrections, Live Validation waivers, PR package history, and release publication for that bounded released slice.
Release Artifacts: Tag v1.6.6-prebeta; release title Pre-Beta v1.6.6; rich Markdown release notes summarize the bounded FB-005 WS-1 workspace slice, validation evidence, non-user-facing release posture, and selected-next planning lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-005 is Released / Closed in v1.6.6-prebeta; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Current Active Workstream: None
Branch Readiness Gate: Complete. `v1.6.7-prebeta` is published and validated, updated `main` is revalidated, and FB-043 has completed its bounded runtime-bearing slice chain, Hardening, Live Validation, and PR Readiness.
Minimal Scope: Historical executed slice: complete WS-1 dev-only desktop test harness relocation from `desktop/orin_desktop_test.py` to `dev/desktop/orin_desktop_test.py`, with direct reference sync and no broader workspace movement.
Summary: Continue workspace organization only through explicitly approved path-sensitive slices, beginning with the now-completed dev-only desktop test harness move.
Why it matters: Keeps folder and ownership cleanup deliberate instead of letting it blur into unrelated feature work.

#### [Former ID: FB-004] Future boot orchestrator layer

Status: Released (v1.6.3-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: High
Release Stage: Slice-staged
Target Version: v1.6.3-prebeta
Release Title: Pre-Beta v1.6.3
Branch: feature/fb-004-future-boot-orchestrator-layer
Canonical Workstream Doc: Docs/workstreams/FB-004_future_boot_orchestrator_layer.md
Branch Readiness: Complete. The branch objective, target end-state, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 current boot-to-desktop source map and ownership boundary, WS-2 lifecycle and orchestration-state framing, and WS-3 validation and admission contract are complete.
Hardening: H-1 boot-orchestrator pressure test is complete. Diagnostics-root canon aligns with runtime-root launcher truth, and stale launcher regression helper reuse is repair-gated.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: Merge-target canon, post-merge release-debt truth, selected-next workstream truth, PR package details, and live PR validation were recorded before PR #74 merged.
Release Execution: `v1.6.3-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.3-prebeta on commit `9f5ae9a78c7dbff79322089bca370fa49da38598`.
Release Target: v1.6.3-prebeta
Release Floor: patch prerelease
Version Rationale: FB-004 was a docs/canon-only architecture and admission milestone with no executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Future boot-orchestrator source map, lifecycle/state framing, ownership boundaries, diagnostics evidence-root correction, rollback boundaries, stale launcher helper caveat, implementation admission contract, hardening, Live Validation waivers, backlog governance sync, and PR Readiness merge-target canon.
Release Artifacts: Tag v1.6.3-prebeta; release title Pre-Beta v1.6.3; rich Markdown release notes summarize the FB-004 boot-orchestrator planning frame, validation/admission contract, diagnostics-root correction, waiver posture, backlog sync, and selected-next branch gate with GitHub-generated What's Changed and Full Changelog sections.
Post-Release Truth: FB-004 is Released / Closed in v1.6.3-prebeta; release debt is clear; FB-015 Branch Readiness may continue on `feature/fb-015-boot-desktop-phase-boundary-model` after updated-main revalidation and the repo-level admission gate pass.
Summary: Preserved the future top-level boot-orchestrator direction above the desktop launcher without authorizing runtime delivery yet.
Why it matters: Keeps the longer-term boot-to-desktop product direction explicit while current desktop and diagnostics work stays bounded.

## Historical Implemented Registry-Only Items

Old implemented registry-only IDs are preserved as same-file historical trace. They are not selectable backlog items and do not have standalone canonical workstream records unless a later USER-approved family consolidation creates one.

| Former ID | Historical Title | Historical Status | Trace Authority |
| --- | --- | --- | --- |
| `FB-001` | Repeated identical crash early escalation | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-002` | Mixed failure-pattern policy | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-003` | Retry limit and diagnostics escalation policy | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-006` | Threshold-based recovery outcome summary refinement | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-007` | Max-attempt identical-failure attempt-pattern correction | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-008` | Shutdown voice degradation effect | Implemented `v2.2.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-009` | Align crash-origin mixed markers with stable repeated-failure summaries | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-010` | v1.6.0 closeout and documentation sync | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-011` | Historical memory contract | Implemented `v1.7.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-012` | Failure fingerprint and recurrence model | Implemented `v1.8.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-013` | Advisory provenance and confidence semantics | Implemented `v1.8.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-014` | Multi-run orchestration regression harness | Implemented `v1.8.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-016` | Recorder-only historical memory groundwork | Implemented `v1.7.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-017` | Support bundle and GitHub issue prefill | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-018` | Voice-path regression validation harness | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-019` | Support bundle to repro triage helper | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-020` | Dev Toolkit utility split and dev-only evidence roots | Implemented `v2.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-021` | Dev-only Boot Nexus test lane | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-022` | Boot & Transition Checks Dev Toolkit surfacing | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-023` | Desktop renderer observability gap closure | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-024` | Boot harness edge-path observability refinement | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-026` | Dev Toolkit uploaded-bundle intake surface | Implemented `v2.2.0` | Historical registry trace in `Docs/feature_backlog.md` |

#### [Former ID: FB-001] Repeated identical crash early escalation

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.6.0
Summary: Early launcher escalation for repeated identical non-`STARTUP_ABORT` crash outcomes.
Why it matters: Prevents stable repeated crash evidence from being masked by unnecessary retries.

#### [Former ID: FB-002] Mixed failure-pattern policy

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.6.0
Summary: Conservative launcher handling for mixed crash and abort failure sequences.
Why it matters: Keeps mixed-pattern outcomes classified without overstating them as stronger than repeated identical failures.

#### [Former ID: FB-003] Retry limit and diagnostics escalation policy

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Defined retry exhaustion and diagnostics-entry policy for repeated `STARTUP_ABORT` and repeated identical crash outcomes.
Why it matters: Makes launcher escalation predictable and evidence-based.

#### [Former ID: FB-006] Threshold-based recovery outcome summary refinement

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v1.6.0
Summary: Refined launcher summary wording for threshold-based early escalation outcomes.
Why it matters: Keeps final failed-run reporting aligned with the actual recovery path.

#### [Former ID: FB-007] Max-attempt identical-failure attempt-pattern correction

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v1.6.0
Summary: Corrected final attempt-pattern reporting for max-attempt identical failures.
Why it matters: Prevents stable repeated failures from being described as varied.

#### [Former ID: FB-008] Shutdown voice degradation effect

Status: Implemented (v2.2.0 rev2)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v2.2.0
Summary: Tuned the shutdown-only voice path so the final line sounds more like controlled power loss.
Why it matters: Improves late-shutdown presentation without widening diagnostics behavior.

#### [Former ID: FB-009] Align crash-origin mixed markers with stable repeated-failure summaries

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v1.6.0
Summary: Aligned mixed-pattern classification with final repeated-failure summaries when cause stayed identical.
Why it matters: Keeps summary and classification evidence consistent.

#### [Former ID: FB-010] v1.6.0 closeout and documentation sync

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.6.0
Summary: Historical closeout and documentation sync for the finalized `v1.6.0` orchestration layer.
Why it matters: Preserved the old baseline before later historical-memory work.

#### [Former ID: FB-011] Historical memory contract

Status: Implemented (v1.7.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v1.7.0
Summary: Defined the contract for passive cross-run historical memory before implementation.
Why it matters: Keeps later history and advisory work deterministic and explainable.

#### [Former ID: FB-012] Failure fingerprint and recurrence model

Status: Implemented (v1.8.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v1.8.0
Summary: Defined how recurring outcomes are recognized across launches without reopening closed runtime classification.
Why it matters: Cross-run recurrence needs stable fingerprint rules to stay trustworthy.

#### [Former ID: FB-013] Advisory provenance and confidence semantics

Status: Implemented (v1.8.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.8.0
Summary: Defined provenance and confidence semantics for advisory outputs.
Why it matters: Keeps advisory intelligence explanatory instead of becoming hidden policy.

#### [Former ID: FB-014] Multi-run orchestration regression harness

Status: Implemented (v1.8.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.8.0
Summary: Added a multi-run regression harness for orchestration and historical-memory validation.
Why it matters: Gives repeated-run behavior a bounded regression surface.

#### [Former ID: FB-016] Recorder-only historical memory groundwork

Status: Implemented (v1.7.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v1.7.0
Summary: Established recorder-only groundwork for passive historical memory.
Why it matters: Kept early history capture bounded before broader interpretation layers arrived.

#### [Former ID: FB-017] Support bundle and GitHub issue prefill

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Added support-bundle creation and issue-prefill groundwork around diagnostics workflows.
Why it matters: Improved manual triage and reporting without automatic submission.

#### [Former ID: FB-018] Voice-path regression validation harness

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Added bounded regression coverage for voice-path behavior.
Why it matters: Protects shutdown and diagnostics voice behavior from silent regression.

#### [Former ID: FB-019] Support bundle to repro triage helper

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Added a helper path for turning support-bundle artifacts into reproducible triage input.
Why it matters: Improves internal debugging flow without changing product behavior.

#### [Former ID: FB-020] Dev Toolkit utility split and dev-only evidence roots

Status: Implemented (v2.0 rev2)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v2.0
Summary: Split Dev Toolkit utilities and formalized dev-only evidence roots.
Why it matters: Keeps internal debugging surfaces structured and separate from live runtime logs.

#### [Former ID: FB-021] Dev-only Boot Nexus test lane

Status: Implemented (v2.1.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v2.1.0
Summary: Added the first dev-only boot test lane for controlled boot-path validation.
Why it matters: Made boot-path validation explicit and reusable inside the toolkit surface.

#### [Former ID: FB-022] Boot & Transition Checks Dev Toolkit surfacing

Status: Implemented (v2.1.0 rev2)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v2.1.0
Summary: Surfaced Boot and Transition Checks inside the Dev Toolkit.
Why it matters: Made transition validation easier to run without ad hoc helper discovery.

#### [Former ID: FB-023] Desktop renderer observability gap closure

Status: Implemented (v2.1.0 rev3)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v2.1.0
Summary: Closed key renderer observability gaps needed for desktop-startup investigation.
Why it matters: Strengthened evidence quality for renderer-owned behavior without broad redesign.

#### [Former ID: FB-024] Boot harness edge-path observability refinement

Status: Implemented (v2.1.0 rev4)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v2.1.0
Summary: Refined boot-harness observability for edge-path behavior.
Why it matters: Improved branch and validation clarity for boot edge cases.

#### [Former ID: FB-026] Dev Toolkit uploaded-bundle intake surface

Status: Implemented (v2.2.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v2.2.0
Summary: Added a dedicated Dev Toolkit intake surface for uploaded support bundles and extracted folders.
Why it matters: Makes internal bundle triage feel like one coherent tooling surface.
