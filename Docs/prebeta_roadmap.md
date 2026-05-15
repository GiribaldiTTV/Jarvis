# Nexus Pre-Beta Roadmap

## Purpose

This document is the sequencing and release-posture layer for current Nexus `pre-Beta` planning.

Use it for:

- latest public prerelease truth
- release-debt posture
- current sequencing posture
- recently closed milestone context

Do not use it as:

- a second backlog
- a workstream execution diary
- a substitute for canonical workstream records

## Authority And Boundaries

This roadmap is subordinate to:

- `Docs/development_rules.md`
- `Docs/phase_governance.md`
- `Docs/codex_modes.md`
- `Docs/feature_backlog.md`
- `Docs/workstreams/index.md`
- `Docs/closeout_guidance.md`

That means:

- backlog owns identity
- live backlog-family identities now use broad `FAM-###` starting at `FAM-001`; legacy `FB-###` IDs remain historical trace only
- roadmap references FAM -> Package -> Slice -> Seam posture from the backlog; PR numbers remain merge/review evidence only and must not become selected-next, package, or release-driver identities
- admitted-slice counting belongs to backlog/source-of-truth validation: only `Admission State: Admitted` rows count, while historical evidence, future placeholders, deferred ideas, and future-package-required rows are sequencing trace only
- backlog historical pass/support/governance/registry rows are traceability only; `Docs/workstreams/index.md`, family dossiers, and canonical workstream records own the durable source-of-truth routing for those former IDs
- workstream docs own promoted-work feature-state, branch-local evidence, and closure records
- phase governance owns repo-wide lifecycle, proof, timeout, and stop-loss rules
- closeouts and rebaselines own epoch summaries
- roadmap owns sequencing and release posture only

## Lane Types And Release Fields

Use these lane types:

- `docs-only`
- `implementation`
- `rebaseline`

Use these release-floor values:

- `no release`
- `patch prerelease`
- `minor prerelease`

Use these release-state values when relevant:

- `active delta`
- `merged unreleased`
- `released`
- `closed`

## Current Release Posture

Current merged truth indicates:

- latest public prerelease: `v1.7.2-prebeta`
- latest public release commit: `3d38630c63965702bb8839f5e0c5f3b4b008e8bb`
- latest public prerelease publication: `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.7.2-prebeta`
- latest public prerelease title: `Pre-Beta v1.7.2`
- unreleased non-doc implementation work: none recorded for the current release window. PR #152 is released in `v1.7.2-prebeta`. GitHub issue closeout/comments, branch/worktree cleanup, provider/model/shortcut/installer work beyond the local-only scaffold, Overlay acceptance, external telemetry parity, raw evidence handling, and AI Product work remain USER-gated.
- the latest public released implementation milestone is the `v1.7.1-prebeta` FAM-006 Dashboard issue-resolution/settings-panel release window, with PR #129, PR #132, and PR #142 released as FAM-006 scope and PR #138 included as under-the-hood FAM-007 support; FAM-006 Monitoring HUD Dashboard Product Surface remains released historical traceability in `v1.7.0-prebeta`; earlier public released implementation milestones include `FAM-001` legacy `FB-049` Active-session pre-settled incoming-launch conflict truth and `FAM-004` legacy `FB-030` voice/audio runtime diagnostics proof in `v1.6.13-prebeta`; FB-048 Active-session relaunch signal-failure and wait-timeout truth in `v1.6.12-prebeta`; FB-047 Active-session relaunch decline session-preservation proof in `v1.6.11-prebeta`; FB-046 Active-session relaunch reacquisition and settled re-entry proof remains released in `v1.6.10-prebeta`; FB-044 Boot-to-desktop handoff outcome refinement and FB-045 Active-session relaunch outcome refinement remain released in `v1.6.9-prebeta`; FB-043 Top-level desktop entrypoint ownership and `main.py` handoff refinement remains released in `v1.6.8-prebeta`; FB-042 Desktop startup runtime family anchor remains released in `v1.6.7-prebeta`; FB-005 Workspace and folder organization remains released in `v1.6.6-prebeta`; FB-030 ORIN voice/audio direction refinement remains released in `v1.6.5-prebeta`; FB-015 Boot and desktop phase-boundary model plus FB-029 ORIN legal-safe rebrand, future ARIA persona option, and repo licensing hardening remain released in `v1.6.4-prebeta`
- current phase after `v1.7.2-prebeta` publication: Branch Readiness Stage 2 on `feature/fam-007-local-ai-runtime-foundation`. PR #152 is released historical FAM-007 local-only scaffold scope in v1.7.2. FAM-007 runtime/provider/model/shortcut/installer work beyond the local runtime foundation plan remains pending USER approval.
- phase status after `v1.6.13-prebeta` release closure: `FAM-001` legacy `FB-049` runtime proof, `FAM-004` legacy `FB-030` runtime diagnostics proof, PR #110 governance repair, PR #111 release-packaging closeout, PR #112 closeout/hardening, PR #113 source-truth closeout / merge-target authority hardening, and merged automation-catalog proof are Released / Closed historical traceability in `v1.6.13-prebeta`; merged-main current-state remains `No Active Branch`; PR #108 merge truth and forced watcher-verification proof are preserved as historical evidence; and PR #109 is merged historical `FAM-003` legacy `FB-027` family evidence for shutdown-hotkey availability/direct-shutdown validation with visible confirmation owned by tray Exit only, not an active backlog lane or standalone release-version driver.
- current active workstream: Branch Readiness Stage 2 planning for FAM-007 Local AI Runtime Foundation. Runtime Workstream implementation is not active until separate USER approval.
- current branch after `v1.7.2-prebeta` release closure: `feature/fam-007-local-ai-runtime-foundation`.
- next concern: validate the FAM-007 Local AI Runtime Foundation Branch Readiness Stage 2 carrier and then request a specific USER approval for the bounded Workstream entry. Runtime/provider/model/shortcut/installer work, AI Product Contract full import, GitHub issue creation or closeout, release/tag/artifact work, raw evidence upload/import/linking, and `codex/ai-llm-lab` mutation remain outside this Branch Readiness carrier.
- future UI standardization note: GitHub issue #136 `Close Button Standardization Mismatch` records the USER-requested future standardization of the FAM-006 Dashboard window-level Close pill across future secondary NDAI windows, including NCP-adjacent Create / Manage windows and future Monitor Create/Edit windows when admitted. Future Overlay/display work should add matching unanchored Overlay Close and Anchor controls, then hide both when the Overlay is anchored to preserve edge-to-edge immersion. This is future traceability only and does not authorize current-branch implementation or raw evidence handling.
- next legal phase after `v1.7.2-prebeta` closure: Workstream entry for the bounded FAM-007 Local AI Runtime Foundation after this Branch Readiness Stage 2 carrier validates green and USER explicitly approves runtime implementation. PR creation, merge, release execution, provider SDK/model work, memory/indexing implementation, voice/Core runtime sync, shortcut/installer work, AI Product Contract import, Private Dev ORIN import, and GitHub issue creation require separate USER approval.
- required post-FAM-006 governance/package candidate: `Repo-Wide High-Risk Source Owner Marker Adoption` on candidate branch `feature/repo-wide-source-owner-marker-adoption`; this is sequencing truth after FAM-006 issue-planning priority is resolved or USER reorders it and does not create/admit the branch, bypass PR Readiness Stage 2, claim package completion, or authorize runtime behavior changes. The future candidate should scan existing source files, identify high-risk product/proof-bearing code regions, map them to Element Validation Ledger rows, add source-owner markers where useful, validate marker-to-ledger consistency, and plan Dev Toolkit Interface Review Mode dispositions for existing and future USER-facing elements including NCP, Core visualization, Dashboard, Overlay/display when admitted, and other windows/components, while preserving the ledger as canonical and markers/review badges as dev-only backlinks or inspection aids only. The Dev Toolkit design is tabled for that future pass, including per-interface launchers, a generalized all-surfaces review-mode launch, or both.

That means the released FB-027 interaction and shared-action family anchor remains part of the current public shared pre-Beta baseline, and PR #109 is preserved under that family as aggregation evidence; the released FB-036 authoring-and-callable-group milestone, the released FB-041 deterministic callable-group execution milestone, the released FB-037 built-in catalog milestone, the released FB-038 tray quick-task UX milestone, the released FB-039 external trigger intake architecture milestone, the released FB-040 monitoring/thermal architecture milestone, the released FB-031 UI/UX architecture milestone, the released FB-032 source-of-truth migration milestone, the released FB-004 future boot-orchestrator architecture milestone, the released FB-015 plus FB-029 planning milestones, the released FB-030 voice/audio planning milestone, and the released FB-005 bounded workspace-path slice are also part of the current public shared pre-Beta baseline.

## Current Branch Execution Posture

Released Historical Scope: FAM-006 Monitoring HUD Dashboard Product Surface released in v1.7.0-prebeta through PR #118; FAM-006 Dashboard render/layout hardening PR #129, Dashboard IA/control follow-through PR #132, Dashboard settings-panel runtime PR #142, and FAM-007 PR #138 provider-boundary / no-provider shell scaffold support released in v1.7.1-prebeta; FAM-007 PR #152 local AI foundation continuation plus governance/readiness support PRs #148, #149, #150, #151, #153, and #154 released in v1.7.2-prebeta; FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, merged governance/automation proof package, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta.
Repo State: Active Branch - `feature/fam-007-local-ai-runtime-foundation`.
Merged-Main Repo State: No Active Branch after v1.7.2-prebeta release closure; PR #152 is released historical FAM-007 scope, not an active branch authority.

Latest Public Prerelease: v1.7.2-prebeta
Latest Public Release Commit: 3d38630c63965702bb8839f5e0c5f3b4b008e8bb
Latest Public Prerelease Publication: https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.7.2-prebeta
Latest Public Prerelease Title: Pre-Beta v1.7.2
Post-Release Canon Closure Drift: Closed by `feature/fam-007-local-ai-runtime-foundation` Branch Readiness Stage 2
Published Release Pending Canon Closure: None - v1.7.2-prebeta source truth is recorded on the current FAM-007 Branch Readiness carrier.
Closure Repair Surface: Current approved FAM-007 Branch Readiness Stage 2 carrier `feature/fam-007-local-ai-runtime-foundation`.
Closure Drift Scope: Closed - PR #152 is released historical FAM-007 local-only scaffold scope in v1.7.2-prebeta.
Implementation Entry: Blocked until this Branch Readiness Stage 2 carrier validates green and USER separately approves Workstream entry.
Release-Debt Avoidance Status: Clear for PR #152 after v1.7.2-prebeta publication; FAM-007 runtime expansion, provider/model/memory/shortcut/installer work, Overlay acceptance, and AI Product work remain separate USER-gated decisions.
Merged-main current active workstream: None
Current active workstream: Branch Readiness Stage 2 planning for FAM-007 Local AI Runtime Foundation; runtime Workstream implementation is not active until separate USER approval.
Current Active Workstream Before Reform: None
Current Execution Branch: `feature/fam-007-local-ai-runtime-foundation`
Active Branch Before Release: `feature/automation-planning`
Current Active Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_runtime_foundation.md`
Historical Branch Authority Record: `Docs/branch_records/feature_fam_006_dashboard_settings_panel.md`
Historical Branch Authority Record: `Docs/branch_records/feature_fam_007_provider_boundary_no_provider_shell.md`
Current Active Canonical Workstream Doc: none
Historical Active Workstream Before Release: Automation Implementation
Historical Active Branch Before Release: `feature/automation-planning`
Earlier Historical Active Workstream Before Release: FB-048 Active-session relaunch signal-failure and wait-timeout truth
Earlier Historical Active Branch Before Release: `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`
Selected Next Workstream: FAM-007 Local AI Runtime Foundation.
Selected Next Record State: Branch Readiness Stage 2 active.
Selected Next Runtime Package Candidate: PKG-007 continuation; package remains admitted but not package-complete.
Selected Next Implementation Branch: `feature/fam-007-local-ai-runtime-foundation`.
Selected Next Status: Selected by USER-approved Branch Readiness Stage 2 from current origin/main; Workstream implementation remains blocked until separate USER approval.
Runtime Package Admission: PKG-007 admitted; package completion not claimed.
Next Legal Runtime Step: Workstream entry for the bounded FAM-007 Local AI Runtime Foundation only after this Branch Readiness Stage 2 validates green and USER separately approves Workstream implementation.
Next Legal Analysis Candidate: Workstream entry packet for the bounded FAM-007 Local AI Runtime Foundation.
Release Readiness Issue Thread Cleanup Gate: Required later for FAM-006 release readiness after USER approval. GitHub issues #123, #127, #137, and #140 remain open / In Work and are eligible for USER-approved closeout after PR #142 merge; #124, #125, and #126 are already closed / fixed and their posture should be preserved. Required issue updates must summarize what solved the issue, name the solving PR/branch/proof traceability, preserve limitation/waiver notes where applicable, and link source-truth evidence before release execution is treated as complete. This record does not authorize GitHub comments, issue state changes, or issue closure.
Post-FAM-006 Required Governance/Package Candidate: Repo-Wide High-Risk Source Owner Marker Adoption; candidate branch `feature/repo-wide-source-owner-marker-adoption`; future scope is to scan existing source files, identify high-risk product/proof-bearing code regions, map those regions to existing or new Element Validation Ledger rows, add high-risk-only source-owner markers where useful, validate marker-to-ledger consistency, and plan repo-wide Dev Toolkit Interface Review Mode dispositions/dev-only inspection affordances for existing and future USER-facing elements including NCP, Core visualization, Dashboard, Overlay/display when admitted, and other windows/components without production runtime behavior changes unless a separately admitted repair is required. The Dev Toolkit design is tabled for that future pass, including whether to use per-interface launchers, a generalized all-surfaces review-mode launch, or both. This candidate is recorded as future sequencing after FAM-006 issue-planning priority is resolved or USER reorders it; future branch creation and package admission remain blocked until the appropriate later readiness path.
Backlog Addition User Approval Missing: Cleared for USER-approved FAM-006 settings-panel Branch Readiness Stage 2 setup and bounded Dashboard settings cog/settings panel runtime implementation and for FAM-007 SLC-017/SLC-018 provider-boundary interaction continuation; active for new backlog item, backlog split, full AI Product Contract import, GitHub issue work, release/tag/artifact work, PR creation, or any single-slice package waiver.
Single-Slice Package User Approval Missing: Active for any package with exactly one admitted slice unless explicit USER approval records `Single-Slice Package User Approval: Granted`.
Package Completion Unproven: Active when package completion is claimed green while admitted slices remain incomplete.
Repair-Only Branch Handling: `feature/fb-046-post-merge-canon-sync` is a bounded repair-only post-merge canon-sync `feature/` branch and did not imply Branch Readiness admission or active branch truth for FB-046.
Historical Branch Readiness State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Current Branch Readiness State: Complete - source truth now records returned LV1 denial, real-client proof-governance failure, WS48 closeout, WS49 follow-up repair closeout, WS50 focused visual-shell repair closeout, WS51 resize/scrollbar/persistence repair closeout, WS52 resize recovery closeout, WS53 resize discoverability closeout, WS54 resize cursor-alignment closeout, WS55 resize-action recovery closeout, WS56 pre-click resize cursor / resize-fluidity closeout, post-main H1 shortcut/launcher proof-boundary truth, and WS57 actual desktop shortcut alignment/proof-gate repair.
Current Workstream State: Green after WS57 - WS43 through WS56 remain supporting history where not superseded; WS57 supplies focused proof that the actual desktop shortcut targets the active FAM-006 worktree and that human-client proof fails fast on shortcut/worktree mismatch.
Current Hardening State: Green after WS57 plus latest bounded Quick Access/high-refresh resize repair - H1 pressure-tested actual desktop shortcut alignment, launcher/orphan-tray integration, active-owner PID identity, stale/reused PID relaunch, RUI-055/RUI-056 human-client resize cursor/fluidity proof, active-client proof, desktop entrypoint/tray proof, NCP/saved-action proof, static validation, and internal sandbox proof; latest repair clears screenshot-visible Quick Access warning-notification shadow bleed and proves high-refresh resize tracking through native window-rect samples.
Current Live Validation State: Stage 1 PASS - latest strengthened red shortcut human-client proof passed at `dev/logs/fam_006_human_client_validation/20260514_111852_225/human_client_manifest.json` after Quick Access shadow-clearance, normal-speed movement and high-refresh resize smoothness repair, central-50-percent rounded-corner diagonal resize-zone repair, #137 rounded-corner native-mask repair, and #140 NCP tray toggle/state repair; compact formal UTS handoff refreshed at `dev/logs/fam_006_monitoring_hud_live_validation/20260514_112213_466`; USER returned refreshed UTS results as PASS after confirming all raised issues and testing returned good.
Current PR Surface Owner: PR #118 `FAM-006 Monitoring HUD Dashboard Product Surface`; PR #109 merge/bot-review/watcher proof remains historical in `Docs/workstreams/FB-027_interaction_system_baseline.md`.
Current Branch Class: implementation
Current Implementation Delta Class: runtime/user-facing, backend/runtime, validator, developer-tooling, and source-truth Live Validation repair
Historical runtime-proof governance remains preserved: the PR watcher remains the only minute-scale heartbeat automation, `ACTIVE` alone is not treated as run proof, and any fallback helper must stay narrowed to the live PR and bounded to `PR Readiness`.
Historical Workstream State: automation catalog implementation is merged historical branch proof after PR #99; FB-048 is Released / Closed in `v1.6.12-prebeta`; FB-047 is Released / Closed in `v1.6.11-prebeta`; FB-046 is Released / Closed in `v1.6.10-prebeta`; FB-044 and FB-045 remain Released / Closed historical proof in `v1.6.9-prebeta`.
Historical Hardening State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Historical Live Validation State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Canonical Current-State Rule: merge-target current-state owners stay merge-stable and must not normalize unresolved release debt, stale canon, or cleanup-only branches as the default. Live PR state, conflict/readiness details, review-resolution details, and blocker-clearing repair-lane narration live only in explicit historical PR sections of the canonical workstream and in operator output.
Release Execution State: `v1.7.2-prebeta` is published; this FAM-007 Branch Readiness carrier repairs post-release source truth and creates no tag, GitHub Release, artifact, or release publication.
Release Target: `v1.7.2-prebeta`.
Release Floor: patch prerelease.
Version Rationale: `v1.7.2-prebeta` published PR #152 FAM-007 local-only scaffold continuation plus governance/readiness support after `v1.7.1-prebeta` without opening a new release-version driver or enabling provider/model/runtime expansion.
Release Scope: FAM-007 PR #152 local AI foundation continuation, plus governance/readiness support from PR #148, PR #149, PR #150, PR #151, PR #153, and PR #154.
Release Artifacts: Published - lightweight tag `v1.7.2-prebeta` and GitHub Release `Pre-Beta v1.7.2` exist at tag commit `3d38630c63965702bb8839f5e0c5f3b4b008e8bb`; release URL `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.7.2-prebeta`; assets none attached.
Post-Release Truth: `v1.7.2-prebeta` is the latest public prerelease; PR #152 is released historical FAM-007 local-only scaffold scope; PR #148, PR #149, PR #150, PR #151, PR #153, and PR #154 are released governance/readiness support; no active main branch authority is implied by the release.
Next-Branch Creation Gate: Cleared for `feature/fam-007-local-ai-runtime-foundation` by USER-approved Branch Readiness Stage 2 carrier creation from current origin/main.
Next Legal Phase: Workstream entry for the bounded FAM-007 Local AI Runtime Foundation after Branch Readiness Stage 2 validation is green and USER explicitly approves runtime implementation. PR creation, merge, release work, issue work, provider SDK/model work, memory/indexing implementation, voice/Core runtime sync, shortcut/installer work, and AI Product Contract import remain separate USER decisions.

## Selected Next Workstream

Selected Next Workstream: FAM-007 Local AI Runtime Foundation.
Record State: Branch Readiness Stage 2 active; FAM-007 / PKG-007 remains admitted but not package-complete.
Minimal Scope: Branch Readiness Stage 2 records post-release canon closure for v1.7.2-prebeta, active branch authority, and a bounded same-branch Workstream plan for SLC-017, SLC-018, SLC-031, SLC-032, SLC-033, SLC-034, SLC-035, and SLC-036. Runtime implementation waits for separate USER approval.
Branch: `feature/fam-007-local-ai-runtime-foundation`.
Selection Scope: Selected by USER-approved Branch Readiness Stage 2 from current origin/main. PR #138 remains released historical scaffold evidence in v1.7.1-prebeta, and PR #152 is released historical scaffold continuation in v1.7.2-prebeta.
PR #129 / PR #132 Boundary: released in v1.7.1-prebeta; future FAM-006 issue closeout or release support remains separate and USER-gated.
Runtime Implementation: Planned for the next bounded Workstream only after USER approval; provider SDKs, model downloads/execution, external calls, memory/indexing implementation, voice/Core sync, shortcut/installer work, release work, AI Product Contract import, private Dev ORIN import, and GitHub issue work remain blocked.

## Released Historical Scope

`FAM-001` legacy `FB-049` Active-session pre-settled incoming-launch conflict truth, `FAM-004` legacy `FB-030` voice/audio runtime diagnostics proof, the merged governance/automation proof package, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof are released historical traceability in `v1.6.13-prebeta`; legacy `FB-027` PR #109 is merged `FAM-003` family aggregation evidence and is not merged release debt or a standalone release-version driver.

## Promoted Canonical Workstreams

- `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
- `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
- `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md`
- `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md`
- `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md`

## Historical FAM-006 Branch Readiness

- ID: `FAM-006`
- Active Workstream Direction: `None - PR #118 merged FAM-006`
- Record State: `Registry-only`
- Selected Next Runtime Package Candidate: `None - PKG-006 merged through PR #118`
- Selected Next Status: `Historical / released in v1.7.0-prebeta`
- Runtime Package Admission: `Historical - admitted on the FAM-006 branch and merged through PR #118`
- Minimal Scope: `runtime package for optional Nexus/NDAI hardware-monitoring HUD visual/user-facing surface, provider-contract-first telemetry health/setup/unavailable states, desktop placement and renderer ownership, settings or user controls visibility, fail-safe/setup/reconnect/no-data/degraded-status behavior, visual/non-invasive warning posture, validation/live desktop proof, and audio/spoken warning integration only if later admitted through FAM-004/cross-family approval.`
- Branch: `feature/fam-006-monitoring-hud-product-surface`
- Branch Status: Created from updated main during USER-approved Branch Readiness Stage 2; Workstream WS18 through WS57, post-WS50 H1, post-WS53 H1, post-WS56 H1, post-WS57 H1, LV1 handoff, and LV2 waiver digest are preserved as supporting Dashboard-first repair/proof/acceptance evidence where not superseded. WS57 repaired the actual desktop shortcut/worktree mismatch found by failure-seeking LV1; LV2 digested explicit USER waiver/passable Dashboard acceptance; PR Readiness Stage 2 created and validated PR #118; PR #118 merged on 2026-05-12; v1.7.0-prebeta released the package as historical traceability.
- Selection Basis: USER explicitly approved FAM-006 Monitoring and HUD as the selected-next runtime direction after `v1.6.13-prebeta` post-release canon closure, then explicitly approved Branch Readiness Stage 2 branch creation and package admission; PR numbers remain evidence only.
- Interface Release Boundary: `Dashboard-first - Monitoring HUD Dashboard / control panel is the primary current-branch user-facing interface release surface`
- Interface Bundle User Approval: `Not granted - Overlay/display acceptance is deferred/non-gating and Core repair is dependency-only`
- Next Legal Seam: `Historical FAM-006 branch readiness is closed; later issue-thread creation, issue-resolution branches, runtime implementation, FAM-007 implementation, or FAM-007 package admission require separate explicit USER approval`
- Post-FAM-006 Required Governance/Package Candidate: `Repo-Wide High-Risk Source Owner Marker Adoption` on candidate branch `feature/repo-wide-source-owner-marker-adoption`; recorded as a required post-FAM-006 sequencing candidate only, with branch creation/package admission deferred to later readiness; scope includes repo-wide Dev Toolkit Interface Review Mode disposition/adoption for existing and future USER-facing elements, not just future code.
- Single-Seam Workstream Waiver: `None - bounded means one active seam at a time, not one-seam Workstream authority; single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded; if only one seam or one slice is planned or visible for the whole Workstream, stop on Single-Seam Or Single-Slice Workstream Blocker; PKG-006 has a recorded multi-seam/multi-slice Workstream chain and must continue through the remaining same-branch repair work unless a named blocker, future dependency, or explicit USER waiver is recorded.`
- Candidate Slices: HUD visual/user-facing surface; runtime telemetry source/adapters; desktop placement / renderer ownership; settings or user controls visibility; fail-safe / no-data / degraded-status behavior; validation / live desktop proof; optional voice/status integration only if later admitted.
- Element Coverage Review: user-facing surface, runtime/backend behavior, settings/configuration, fail-safe/recovery, monitoring/HUD/observability, validation/live-test requirements, release/documentation impact, and optional voice/audio integration are planning coverage only and do not count as admitted slices.

## Active Promoted Workstream

None.

### FAM-003 Interaction and Actions (legacy FB-027)

- status: `Released (v1.2.9-prebeta) / family aggregation hold`
- record state: `Closed`
- priority: `High`
- canonical workstream doc: `Docs/workstreams/FB-027_interaction_system_baseline.md`
- lifetime dossier doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- branch: none
- phase status: Released family anchor with merged PR #109 shutdown-hotkey availability/direct-shutdown and tray-confirmation boundary proof preserved as family aggregation evidence; no active workstream or selected-next lane exists.
- next legal seam: none; future same-family continuation requires explicit USER approval.
- historical baseline: released `v1.2.9-prebeta` typed-first interaction baseline plus saved-action inventory and guided-access follow-through remain preserved as the first FB-027 proof.
- Standalone Release Driver: No
- Aggregation Target: Future USER-approved FB-027 family release or larger approved release aggregation.
- Minimal Scope: Historical PR #109 aggregation evidence preserves direct shutdown hotkeys for `Ctrl+Alt+End` and `Ctrl+Alt+2` while tray Exit owns the visible confirmation prompt; no next same-family runtime slice is selected.

### FB-048 Active-session relaunch signal-failure and wait-timeout truth

status: `released`
record state: `Closed`
priority: `High`
canonical workstream doc: `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
roadmap role: `Historical pass alias`
historical alias of: `FB-042`
pass id: `F042-P07`
lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
branch: `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`
phase status: Released / Closed in `v1.6.12-prebeta`; PR #94, PR #96, and PR #97 are merged on `main`; the release is live on commit `b06c359e58b47cfe26fe8c4b39ac04fde519dee9`; release debt is clear; and the next active execution surface is the docs-only governance reform branch authority record on `feature/backlog-family-governance-reform`.
next legal seam: none; this record is now historical released truth
Release Target: `v1.6.12-prebeta`
Release Floor: `patch prerelease`
Version Rationale: FB-048 delivers a bounded runtime/user-facing relaunch signal-failure and wait-timeout refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-048 WS-1 accepted relaunch failure-path truthful outcome proof, H-1 failure/timeout lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, review-repair containment, canon/governance hardening, release publication, and selected-next FB-049 successor preservation for the bounded runtime/user-facing lane only.
Release Artifacts: Tag `v1.6.12-prebeta`; release title `Pre-Beta v1.6.12`; rich Markdown release notes summarize the bounded FB-048 relaunch failure/timeout runtime/user-facing package, real shortcut evidence, and the FB-049 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-048 is Released / Closed in `v1.6.12-prebeta`; release debt is clear; the governance reform branch may proceed through its admitted branch-authority record; and FB-049 remains selected next, `Registry-only`, and branch-not-created until that branch completes and later FB-049 Branch Readiness admission occurs.
Latest Public Baseline: `v1.6.12-prebeta` on `b06c359e58b47cfe26fe8c4b39ac04fde519dee9`
Minimal Scope: Prove and refine accepted relaunch signal-failure and wait-timeout lanes across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so failure-path ownership stays explicit and no false replacement-session truth leaks out.
Current Delta: accepted relaunch signal-failure emits an explicit preserved-session marker, accepted relaunch wait-timeout emits an explicit replacement-unconfirmed marker, rapid repeated signal-failure launches preserve the active owner, near-deadline reacquire no longer falls through to a false timeout, and mixed failure -> decline -> accept -> failure sequencing keeps failure, decline, and success classification distinct.

## Latest Released Workstream Context

### FB-047 Active-session relaunch decline session-preservation proof

status: `released`
record state: `Closed`
priority: `High`
canonical workstream doc: `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
roadmap role: `Historical pass alias`
historical alias of: `FB-042`
pass id: `F042-P06`
lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
branch: `feature/fb-047-active-session-relaunch-decline-preservation`
phase status: Released / Closed in `v1.6.11-prebeta`; PR #93 merged into `main` at `4ca70572fbc8033bc96fcd299dd309464e81393a`; the release is live on the same commit; release debt is clear; and later runtime-family continuation moved through FB-048 on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`, which later completed its own released historical pass.
next legal seam: none; this record is now historical released truth
Release Target: `v1.6.11-prebeta`
Release Floor: `patch prerelease`
Version Rationale: FB-047 delivers a bounded runtime/user-facing relaunch-decline preservation refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-047 WS-1 declined relaunch incoming-launch truthful exit proof, H-1 decline lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, release publication, and selected-next FB-048 successor admission for the bounded runtime/user-facing lane only.
Release Artifacts: Tag `v1.6.11-prebeta`; release title `Pre-Beta v1.6.11`; rich Markdown release notes summarize the bounded FB-047 relaunch-decline preservation runtime/user-facing package, real shortcut evidence, and the FB-048 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-047 is Released / Closed in `v1.6.11-prebeta`; release debt is clear; and later runtime-family continuation moved through FB-048 on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth` while this record remained released historical proof.

### FB-046 Active-session relaunch reacquisition and settled re-entry proof

status: `released`
record state: `Closed`
priority: `High`
canonical workstream doc: `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md`
roadmap role: `Historical pass alias`
historical alias of: `FB-042`
pass id: `F042-P05`
lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
branch: `feature/fb-046-active-session-relaunch-reacquisition`
phase status: Released / Closed in `v1.6.10-prebeta`; PR #92 merged into `main` at `36cf07495dc8e239b20b11afb5194355b77ffd8b`; the release is live on the same commit; FB-047 is now Released / Closed in `v1.6.11-prebeta`; release debt is clear; and later runtime-family continuation moved through FB-048 on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
next legal seam: none; this record is now historical released truth
Release Target: `v1.6.10-prebeta`
Release Floor: `patch prerelease`
Version Rationale: FB-046 delivers a bounded runtime/user-facing relaunch-reacquisition refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-046 WS-1 accepted relaunch replacement-session settled re-entry proof, H-1 relaunch lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, merged-unreleased release-debt truth, and selected-next FB-047 successor lock for the bounded runtime/user-facing lane only.
Release Artifacts: Tag `v1.6.10-prebeta`; release title `Pre-Beta v1.6.10`; rich Markdown release notes summarize the bounded FB-046 relaunch-reacquisition runtime/user-facing package, real shortcut evidence, and the FB-047 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-046 is Released / Closed in `v1.6.10-prebeta`; FB-047 is Released / Closed in `v1.6.11-prebeta`; release debt is clear; and later runtime-family continuation moved through FB-048 on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
minimal scope: complete the bounded accepted relaunch lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_desktop_entrypoint_validation.py`, and `dev/orin_boot_transition_verification.py` so the replacement session reacquires the guard and returns to authoritative settled without widening into `main.py`, `Audio/`, `logs/`, `nexus_visual/`, installer work, or broader boot-orchestrator implementation
branch-readiness carry-forward: preserved in `Docs/branch_records/feature_fb_046_active_session_relaunch_reacquisition.md`

### FB-044 Boot-to-desktop handoff outcome refinement

- status: `released`
- record state: `Closed`
- priority: `High`
- canonical workstream doc: `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-042`
- pass id: `F042-P03`
- lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
- branch: `feature/fb-044-boot-desktop-handoff-outcome-refinement`
- phase status: Released / Closed in `v1.6.9-prebeta`; PR #89 merged into `main` at `f71ccbd77b81276a441386b9762c2aac34ceb827`; the release is live on commit `348fd55b944435e3cae80b97acd0bb857fd65d56`; FB-045 is also Released / Closed in the same package; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- next legal seam: none; this record is now historical released truth.
Release Target: v1.6.9-prebeta
Release Floor: patch prerelease
Version Rationale: FB-044 delivers a bounded runtime/user-facing boot-to-desktop settled-outcome refinement on the existing startup family without opening a new product lane or materially expanded runtime family.
Release Scope: completed FB-044 WS-1 desktop-settled handoff outcome refinement, H-1 settled-state hardening, LV-1 real desktop shortcut evidence, release publication, and the released FB-045 blocker-clearing lifecycle follow-through inside the same package.
Release Artifacts: Tag v1.6.9-prebeta; release title Pre-Beta v1.6.9; rich Markdown release notes summarize the bounded FB-044 settled-outcome package, the released FB-045 blocker-clearing lifecycle follow-through, real shortcut evidence, and the FB-046 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

### FB-045 Active-session relaunch outcome refinement

- status: `released`
- record state: `Closed`
- priority: `High`
- canonical workstream doc: `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-042`
- pass id: `F042-P04`
- lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
- branch: `feature/fb-045-active-session-relaunch-stability`
- phase status: Released / Closed in `v1.6.9-prebeta`; PR #90 merged into `main` at `d7e9e7d3f06f6e17a0b0537e3c45de103febb75a`; the release is live on commit `348fd55b944435e3cae80b97acd0bb857fd65d56`; FB-044 remains the release-scope owner for the same published package; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- next legal seam: none; this record is now historical released truth.
Release Target: v1.6.9-prebeta
Release Floor: patch prerelease
Version Rationale: FB-045 delivers a bounded runtime/user-facing lifecycle-classification follow-through on the existing startup family without opening a new product lane or materially expanded runtime family.
Release Scope: completed FB-045 WS-1 post-settled runtime stability refinement, H-1 post-settled lifecycle hardening, LV-1 real desktop shortcut evidence, PR package history, merge, and live release publication inside the FB-044 `v1.6.9-prebeta` package.
Release Artifacts: Tag v1.6.9-prebeta; release title Pre-Beta v1.6.9; rich Markdown release notes summarize the bounded FB-045 blocker-clearing lifecycle follow-through as part of the FB-044 release package, without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

### FB-042 Desktop startup runtime family anchor

- status: `released`
- record state: `Closed`
- priority: `Low`
- canonical workstream doc: `Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md`
- roadmap role: `Family anchor`
- family anchor: `Self`
- historical pass coverage: `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`
- lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
- lifetime dossier state: structured shell with partial historical pass migration; Phase 4 / Slice R4-S3 added pass index and slice/seam ledger templates, Phase 4 / Slice R4-S4 added validator/helper and artifact index templates, Phase 4 / Slice R4-S5 validated dossier stability, Phase 5 / Slice R5-S1 converted FB-043 through FB-048 into explicit historical pass records while populating the dossier pass index plus slice/seam ledger summary rows, Phase 5 / Slice R5-S3 converted the preserved corresponding branch-readiness records, and Phase 5 / Slice R5-S5 indexed the preserved branch trace; validator/helper and artifact migration remain pending
- branch: `feature/fb-042-desktop-entrypoint-runtime-refinement`
- phase status: Released / Closed in `v1.6.7-prebeta`; PR #86 merged into `main` at `bd25fff6afd089cdc758a0d598eb7a5df520b82b`; PR #87 cleared the final release-debt marker repair; the release is live on commit `8f53d163ad008f7508f55f593b15369749e3ec24`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- next legal seam: none; this record is now historical released truth.
Release Target: v1.6.7-prebeta
Release Floor: patch prerelease
Version Rationale: FB-042 delivers a bounded runtime/user-facing launch-path reliability and startup-error-handling refinement on the existing desktop entrypoint path without opening a new product lane or materially expanding the runtime family.
Release Scope: WS-1 launch-path fallback hardening in `launch_orin_desktop.vbs`, direct user-facing startup failure dialog handling when no usable windowed Python launcher exists, launch-chain validator expansion across default and forced-fallback VBS paths, H-1 launcher-fallback contract correction, real desktop shortcut validation evidence, and release publication for the bounded runtime slice only.
Release Artifacts: Tag v1.6.7-prebeta; release title Pre-Beta v1.6.7; rich Markdown release notes summarize the bounded FB-042 desktop launch-path runtime refinement, fallback hardening, real shortcut evidence, and the FB-043 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

### FB-043 Top-level desktop entrypoint ownership and main.py handoff refinement

- status: `released`
- record state: `Closed`
- priority: `High`
- canonical workstream doc: `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-042`
- pass id: `F042-P02`
- lifetime dossier doc: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
- branch: `feature/fb-043-top-level-entrypoint-handoff-refinement`
- phase status: Released / Closed in `v1.6.8-prebeta`; PR #88 merged into `main` at `5e695af5fada05e4ad6b25731bce328ede8a09ee`; the release is live; FB-044 and FB-045 are now Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- next legal seam: none; this record is now historical released truth.

### FB-005 Workspace and folder organization

- status: `released`
- record state: `Closed`
- priority: `Low`
- canonical workstream doc: `Docs/workstreams/FB-005_workspace_and_folder_organization.md`
- branch: `feature/fb-005-workspace-path-planning`
- phase status: Released / Closed in `v1.6.6-prebeta`; PR #83 merged into `main` at `873c9b6801802a05bbcef074595e632c0ec9f1d2`; the release is live on commit `deeaa691a79dd01897f6aed82f087970db7019b3`; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- next legal seam: none; this record is now historical released truth.
Release Target: v1.6.6-prebeta
Release Floor: patch prerelease
Version Rationale: FB-005 remains a bounded dev-only workspace/path implementation slice with no change to shipped runtime entrypoints, launcher paths, audio paths, logs, visual assets, installer behavior, or user-facing desktop behavior.
Release Scope: the historically released FB-005 WS-1 dev-only desktop test harness relocation from `desktop/orin_desktop_test.py` to `dev/desktop/orin_desktop_test.py`, local path-math preservation, direct workspace-layout truth sync, hardening corrections, Live Validation waivers, PR package history, and release publication for that bounded released slice.
Release Artifacts: Tag v1.6.6-prebeta; release title Pre-Beta v1.6.6; rich Markdown release notes summarize the bounded FB-005 WS-1 workspace slice, validation evidence, non-user-facing release posture, and selected-next planning lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-005 is Released / Closed in `v1.6.6-prebeta`; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

### FAM-004 Voice and Audio (legacy FB-030)

- status: `Released`
- record state: `Closed`
- priority: `Medium`
- canonical workstream doc: `Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md`
- branch: `feature/fb-030-voice-audio-runtime-branch-readiness`
- phase status: Released / Closed in `v1.6.13-prebeta`; WS1, H1, LV1, PR1, and PR2 are complete and green, PR #108 is merged, watcher verification proof exists through a forced run, PR108 watcher automations are retired, and historical `v1.6.5-prebeta` planning proof remains preserved.
- next legal seam: none; released historical traceability only until USER approves a future voice/audio package.
Released Historical Scope: FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth plus FAM-004 legacy FB-030 voice/audio runtime diagnostics proof plus merged governance/automation proof package plus PR #112 source-truth closeout / merge-target authority hardening proof plus PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta
Repo State: No Active Branch
Latest Public Prerelease: v1.7.0-prebeta
Release Title: Pre-Beta v1.6.13
Release Target: None - released in v1.6.13-prebeta.
Release Floor: none - release execution is complete.
Version Rationale: FAM-004 legacy FB-030 added bounded runtime diagnostics truth for voice/audio availability without opening a new feature family or materially widening product scope.
Release Scope: released governance reform, automation catalog proof, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof.
Release Artifacts: Published tag `v1.6.13-prebeta`; published GitHub prerelease title `Pre-Beta v1.6.13`; release notes include generated `What's Changed` and `Full Changelog` sections.
Post-Release Truth: merged governance reform, automation catalog, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening, and PR #113 source-truth closeout / merge-target authority hardening are released historical traceability; release debt is clear; and the later runtime package has USER-approved FAM-006 prior Workstream/Hardening evidence on `feature/fam-006-monitoring-hud-product-surface`; product completion is reopened, LV1 returned UTS FAIL evidence blocks Live Validation green, Stage 2-R11 records the dashboard/minimal-HUD and Core non-interference source-truth repair, Stage 1-R8 revalidated it, WS18 repaired/proved Core desktop-layer/non-interference, WS19 repaired/proved the renderer-visible dashboard/minimal-HUD split, WS20 rerouted dashboard technical proof boxes into configuration-centered content, WS21 repaired dashboard movement/scrollbar polish, WS22 repaired/proved native minimal-HUD click-through/non-focus behavior, WS23 through WS28 completed the expanded overlay/control/proof repair chain, WS29 reconciled Workstream green, and WS30 repaired/proved fixed non-movable preset-monitor ORIN/Core plus HUD surface isolation for Hardening rerun.
Selected Next Workstream: None - FAM-006 merged through PR #118 and is released historical traceability in v1.7.0-prebeta.
Next-Branch Creation Gate: Blocked until USER separately approves a specific issue-resolution branch, runtime package branch, or other legal carrier after FAM-006 issue-readiness cleanup.
Historical Planning Release: `v1.6.5-prebeta` remains the released planning/admission proof for the original voice/audio direction milestone.
- Minimal Scope: Completed WS1 voice/audio runtime availability and truthful diagnostics proof across `Audio/orin_voice.py`, `Audio/orin_error_voice.py`, `main.py`, `desktop/orin_desktop_launcher.pyw`, and `dev/orin_voice_regression_harness.py`, while preserving ORIN as the only shipped persona, keeping ARIA dormant, avoiding prompt or asset redesign, and avoiding public-copy or release-note changes before release phases.

## Backlog Priority Review

The 2026-04-23 priority reading is updated during FB-005 Branch Readiness:

- FB-004 is released and closed in `v1.6.3-prebeta`; it is no longer an active or selected-next branch candidate.
- FB-015 is released and closed in `v1.6.4-prebeta`; it no longer owns release debt or active branch truth.
- FB-029 is released and closed in `v1.6.4-prebeta`; it no longer owns release debt or active branch truth.
- FAM-004 legacy FB-030 remains `Medium` as historical planning priority, and its runtime diagnostics follow-through is now released historical traceability in `v1.6.13-prebeta` after PR #108 and release execution.
- FAM-003 legacy FB-027 is `High` as a released baseline family anchor; PR #109 shutdown-hotkey availability/direct-shutdown and tray-confirmation boundary proof is merged family evidence and aggregation material, not an active selected-next lane or standalone release-version driver.
- FB-005 remains `Low` as historical workspace priority, but it is now Released / Closed in `v1.6.6-prebeta` and no longer owns release debt or selected-next truth.
- FB-042 is now Released / Closed in `v1.6.7-prebeta`; the released launch-path slice is preserved as the first historical proof under the runtime family anchor.
- FB-043 is now Released / Closed in `v1.6.8-prebeta`.
- FB-044 and FB-045 are now Released / Closed in `v1.6.9-prebeta`.

Current-branch clarity: latest public prerelease is `v1.7.2-prebeta`; PR #129, PR #132, and PR #142 are released FAM-006 Dashboard implementation scope in `v1.7.1-prebeta`; PR #152 FAM-007 local AI foundation continuation plus governance/readiness support PRs #148, #149, #150, #151, #153, and #154 are released in `v1.7.2-prebeta`; FB-044 and FB-045 are released and closed in `v1.6.9-prebeta`; FB-046 is released and closed in `v1.6.10-prebeta`; FB-047 is released in `v1.6.11-prebeta`; FB-048 is released and closed in `v1.6.12-prebeta`; FAM-001 legacy FB-049, FAM-004 legacy FB-030, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof are released historical traceability in `v1.6.13-prebeta`; FAM-003 legacy FB-027 is released baseline with PR #109 preserved as aggregation evidence; FAM-006 Monitoring HUD Dashboard Product Surface is released historical traceability in `v1.7.0-prebeta`; PR #120 and PR #121 are merged governance/workspace proof; PR #131 made FAM-007 the selected runtime lane; PR #138 provider-boundary / no-provider shell scaffold is released under-the-hood support in `v1.7.1-prebeta`; `feature/fam-007-local-ai-runtime-foundation` is the current Branch Readiness Stage 2 carrier; and later FAM-007 runtime/provider/model work remains USER-gated.

## Current Released Historical Workstream

FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, the merged governance/automation proof package, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof are released historical traceability in `v1.6.13-prebeta`.

## Latest Released Workstream Context

### FB-029 ORIN Legal-Safe Rebrand, Future ARIA Persona Option, And Repo Licensing Hardening

- status: `released`
- record state: `Closed`
- priority: `High`
- canonical workstream doc: `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md`
- selection basis: selected during FB-015 PR Readiness as the highest-priority remaining open backlog candidate, then carried on this branch first for blocker-clearing FB-015 canon repair and now for completed Branch Readiness planning.
- branch: `feature/fb-029-orin-identity-licensing-hardening`
- phase status: Released / Closed in `v1.6.4-prebeta`; PR #76 merged into `main` at `0897fab768dc07385f83fab81434ba7926ecc4a1`; the milestone remains docs/canon-only historical truth, and explicit product/legal approval still blocks any later implementation-facing naming, licensing, release, runtime, or persona-surface change.
- repo-level post-release state: FB-030 is Released / Closed in `v1.6.5-prebeta`; FB-005 is Released / Closed in `v1.6.6-prebeta`; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- next legal seam: none; this record is now historical released truth.
Release Target: v1.6.4-prebeta
Release Floor: patch prerelease
Version Rationale: FB-029 remains a docs/canon-only identity, persona-option, and licensing-planning milestone with no new executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Identity source-of-truth inventory, persona-option boundary framing, licensing boundary framing, implementation admission contract, hardening corrections, Live Validation waivers, PR package history, merged-unreleased package-state repair, and post-merge current-state cleanup.
Release Artifacts: Tag v1.6.4-prebeta; release title Pre-Beta v1.6.4; rich Markdown release notes summarize the FB-015 boundary model and the FB-029 identity/licensing planning frame without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-029 is Released / Closed in `v1.6.4-prebeta`; FB-015 is also Released / Closed in the same package; FB-030 is Released / Closed in `v1.6.5-prebeta`; FB-005 is Released / Closed in `v1.6.6-prebeta`; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- Minimal Scope: Define the legal-safe ORIN naming, optional future ARIA persona posture, and licensing-hardening planning frame before any naming, licensing, release, runtime, or persona-facing edits begin.

### FB-015 Boot And Desktop Phase-Boundary Model

- status: `released`
- record state: `Closed`
- priority: `High`
- canonical workstream doc: `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md`
- selection basis: selected during FB-004 PR Readiness after GOV-PR0 raised FB-015 to High and confirmed it is the clearest routine technical successor after the FB-004 boot-orchestrator architecture frame; PR #75 merged, FB-015 carried release debt through `v1.6.4-prebeta`, and the lane is now released and closed.
- branch: `feature/fb-015-boot-desktop-phase-boundary-model`
- phase status: Released / Closed in `v1.6.4-prebeta`; PR #75 merged into `main` at `3e821e07ff91d814fd7aba9b50819f97d700a301`; WS-1 through WS-3, H-1, LV-1, PR-1, PR-2, and PR-3 are complete; release debt is clear after publication, validation, and post-release canon closure.
- next legal seam: none; this record is now historical released truth.
Release Target: v1.6.4-prebeta
Release Floor: patch prerelease
Version Rationale: FB-015 remains a docs/canon-only boot and desktop phase-boundary architecture plus admission milestone with no new executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: FB-015 boot and desktop phase-boundary inventory, ownership map, lifecycle and state framing, implementation admission contract, hardening corrections, Live Validation waivers, PR package history, post-merge canon repair, and merged-unreleased release-debt framing, plus the FB-029 identity source-of-truth inventory, persona-option boundary framing, licensing boundary framing, implementation admission contract, hardening corrections, Live Validation waivers, and PR Readiness package history.
Release Artifacts: Tag v1.6.4-prebeta; release title Pre-Beta v1.6.4; rich Markdown release notes summarize the FB-015 boundary model and the FB-029 identity/licensing planning frame without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-015 is Released / Closed in `v1.6.4-prebeta`; FB-029 is also Released / Closed in the same package; FB-030 is Released / Closed in `v1.6.5-prebeta`; FB-005 is Released / Closed in `v1.6.6-prebeta`; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
- Minimal Scope: Complete the bounded docs/canon seam chain for current boot/desktop phase-boundary ambiguity, starting with current boundary inventory and ownership mapping before lifecycle framing or implementation-admission rules are extended.

## Prior Released Workstream Context

### FB-004 Future Boot Orchestrator Layer

- status: `released`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.6.3-prebeta`
- release state: `released`
- release title: `Pre-Beta v1.6.3`
- canonical workstream doc: `Docs/workstreams/FB-004_future_boot_orchestrator_layer.md`
- sequencing note: released the docs/canon-only future boot-orchestrator architecture milestone, including source map, lifecycle/state framing, ownership boundaries, diagnostics evidence-root correction, rollback boundaries, stale helper caveat, implementation admission contract, hardening, Live Validation waivers, backlog governance sync, and PR Readiness merge-target canon.
- successor note: FB-015 and FB-029 are released and closed in `v1.6.4-prebeta`, FB-030 is released and closed in `v1.6.5-prebeta`, FB-005 is released and closed in `v1.6.6-prebeta`, FB-042 is released and closed in `v1.6.7-prebeta`, FB-043 is released and closed in `v1.6.8-prebeta`, FB-044 and FB-045 are released and closed in `v1.6.9-prebeta`, and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

## Prior Released Workstream Context

### FB-032 Nexus-Era Vision And Source-Of-Truth Migration

- status: `released`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.6.2-prebeta`
- release state: `released`
- release title: `Pre-Beta v1.6.2`
- canonical workstream doc: `Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md`
- sequencing note: released the architecture-only Nexus-era source-of-truth migration foundation, including current-vs-historical source inventory, naming policy, canonical-vs-historical surface classification, controlled migration admission contract, governance repairs, hardening, Live Validation waivers, and PR Readiness merge-target canon.
- successor note: FB-004 is released and closed in `v1.6.3-prebeta`; FB-015 and FB-029 are released and closed in `v1.6.4-prebeta`; FB-030 is released and closed in `v1.6.5-prebeta`; FB-005 is released and closed in `v1.6.6-prebeta`; FB-042 is released and closed in `v1.6.7-prebeta`; FB-043 is released and closed in `v1.6.8-prebeta`; FB-044 and FB-045 are released and closed in `v1.6.9-prebeta`, and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

## Prior Released Workstream Context

### FB-031 Nexus Desktop AI UI/UX Overhaul Planning

- status: `released`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.6.1-prebeta`
- release state: `released`
- release title: `Pre-Beta v1.6.1`
- canonical workstream doc: `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md`
- sequencing note: released the architecture-only UI/UX planning milestone, including source map, visual-language ownership vocabulary, lifecycle and interaction-state framing, future UI implementation admission contract, Hardening pressure test, Live Validation waivers, PR Readiness merge-target canon, and PR-R1 release-floor validator repair.
- successor note: FB-032 is released and closed in `v1.6.2-prebeta`; FB-004 is released and closed in `v1.6.3-prebeta`; FB-015 and FB-029 are released and closed in `v1.6.4-prebeta`; FB-030 is released and closed in `v1.6.5-prebeta`; FB-005 is released and closed in `v1.6.6-prebeta`; FB-042 is released and closed in `v1.6.7-prebeta`; FB-043 is released and closed in `v1.6.8-prebeta`; FB-044 and FB-045 are released and closed in `v1.6.9-prebeta`; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.

## Prior Released Workstream Context

### FB-040 Monitoring, Thermals, And Performance HUD Surface

- status: `released`
- lane type: `implementation`
- release floor: `minor prerelease` (historical published tag; future architecture-only planning/admission milestones must not use minor solely because they define a planning lane)
- target version: `v1.6.0-prebeta`
- release state: `released`
- release title: `Pre-Beta v1.6.0`
- canonical workstream doc: `Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md`
- sequencing note: released the architecture-only monitoring and thermal planning milestone, including source map, ownership vocabulary, lifecycle/trust-safety framing, validation/admission contract, hardening result, and Live Validation waiver handling.
- version-governance note: FB-040 was already published as `v1.6.0-prebeta`; governance now records that future architecture-only, non-user-facing planning/admission milestones default to patch prerelease advancement unless they deliver a runtime, executable, or user-facing capability lane.

### FB-039 External Trigger And Plugin Integration Architecture

- status: `released`
- lane type: `implementation`
- release floor: `minor prerelease`
- target version: `v1.5.0-prebeta`
- release state: `released`
- release title: `Pre-Beta v1.5.0`
- canonical workstream doc: `Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md`
- sequencing note: released the internal-only external trigger intake architecture milestone, including source map, ownership vocabulary, lifecycle/trust framing, in-memory registration, bounded invocation follow-through, lifecycle transitions, decision evidence, boundary state snapshots, readiness inspection, registry readiness sweep, summary, detail snapshot, reusable validation coverage, and Live Validation waiver handling.

### FB-038 Taskbar / Tray Quick-Task UX And Create Custom Task Surface

- status: `released`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.4.1-prebeta`
- release state: `released`
- release title: `Pre-Beta v1.4.1`
- canonical workstream doc: `Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-027`
- pass id: `F027-P05`
- lifetime dossier doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- sequencing note: released the tray quick-task UX milestone, including tray identity/discoverability, tray Open Command Overlay, tray Create Custom Task dialog-open/no-write route, tray-origin create completion through existing FB-036 authoring, catalog reload, exact-match resolution, confirm/result execution, and startup first-visible Core Visualization sequencing repair

## Earlier Released Workstream Context

### FB-037 Curated Built-In System Actions And Nexus Settings Expansion

- status: `released`
- lane type: `implementation`
- release floor: `minor prerelease`
- target version: `v1.4.0-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-027`
- pass id: `F027-P04`
- lifetime dossier doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- sequencing note: released the curated built-in Windows utility catalog for Task Manager, Calculator, Notepad, and Paint while preserving saved-action override authority, authoring collision protection, confirm/result surfaces, and callable-group behavior

### FB-041 Deterministic Callable-Group Execution Layer

- status: `released`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.3.1-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-027`
- pass id: `F027-P03`
- lifetime dossier doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- sequencing note: released deterministic stored-order callable-group execution, stop-on-failure semantics, group-aware failure-path reuse, and confirm/result status alignment while preserving single-action behavior

### FB-036 Saved-Action Authoring And Callable Groups

- status: `released`
- lane type: `implementation`
- release floor: `minor prerelease`
- target version: `v1.3.0-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-036_saved_action_authoring.md`
- roadmap role: `Historical pass alias`
- historical alias of: `FB-027`
- pass id: `F027-P02`
- lifetime dossier doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- sequencing note: released bounded custom-task authoring, callable groups, inline group quick-create, explicit trigger modeling, and the final exact-green authoring hardening without changing the locked typed-first overlay contract or widening into Action Studio behavior

## Recently Closed Workstreams

### Historical FB-027 Interaction and shared-action family anchor baseline

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.9-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-027_interaction_system_baseline.md`
- roadmap role: `Family anchor`
- family anchor: `Self`
- historical pass coverage: `FB-036`, `FB-037`, `FB-038`, `FB-041`
- lifetime dossier doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- lifetime dossier state: structured shell with partial historical pass migration; Phase 4 / Slice R4-S3 added pass index and slice/seam ledger templates, Phase 4 / Slice R4-S4 added validator/helper and artifact index templates, Phase 4 / Slice R4-S5 validated dossier stability, Phase 5 / Slice R5-S2 converted FB-036, FB-037, FB-038, and FB-041 into explicit historical pass records while populating the dossier pass index plus slice/seam ledger summary rows, Phase 5 / Slice R5-S3 converted the preserved corresponding branch-record trace where it exists, and Phase 5 / Slice R5-S5 indexed the preserved branch trace; validator/helper and artifact migration remain pending
- sequencing note: preserves the first released interaction baseline and now anchors the later shared-action follow-through family below FB-036, FB-037, FB-038, and FB-041

### FB-035 Release-Context Fallback Hardening

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.7-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
- sequencing note: closed the support-report release-context hardening milestone and established the current release-context baseline

### FB-034 Recoverable Diagnostics

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.6-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- sequencing note: remains a closed recoverable-diagnostics milestone, not an automatically active continuation lane

### FB-025 Boot/Desktop Taxonomy Clarification

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.5-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`

### FB-033 Startup Snapshot Harness Follow-Through

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.4-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`

### FB-028 History State Relocation

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.3-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-028_history_state_relocation.md`

## Current Sequencing Reading

Current merged truth indicates:

- the released FB-027 family anchor remains part of the locked current interaction floor
- the released FB-036 authoring-and-callable-group milestone is now part of the locked current pre-Beta baseline
- the released FB-041 deterministic callable-group execution milestone is now part of the locked current pre-Beta baseline
- the released FB-037 built-in catalog milestone is now part of the locked current pre-Beta baseline
- the released FB-038 tray quick-task UX milestone is now part of the locked current pre-Beta baseline
- the released FB-039 external trigger intake architecture milestone is now part of the locked current pre-Beta baseline
- the released FB-035 lane is closed
- the recent released workstreams above remain part of the locked current baseline
- merged unreleased non-doc implementation debt exists: yes - PR #129 FAM-006 Dashboard render/layout hardening and PR #132 FAM-006 Dashboard IA/control follow-through are merged after `v1.7.0-prebeta` and not yet released
- FB-038 is released and closed in `v1.4.1-prebeta`; H1 identity/discoverability repair, H2 shortcut-launch tray readback validation, H3 window initialization sequencing, H4 post-fix startup visibility validation, fresh post-H4 technical/live validation, user-facing desktop shortcut validation, and UTS waiver digestion are preserved as historical evidence
- FB-039 is released and closed in `v1.5.0-prebeta`; internal-only intake runtime boundaries, reusable validation coverage, Live Validation waivers, PR readiness governance, and post-merge release-truth repairs are preserved as historical evidence
- FB-040 is released and closed in `v1.6.0-prebeta`; architecture-only monitoring and thermal source mapping, lifecycle/trust-safety framing, validation/admission contract, hardening, Live Validation waiver truth, and post-release canon closure are preserved as historical evidence
- FB-031 is released and closed in `v1.6.1-prebeta`; UI/UX source mapping, visual-language ownership vocabulary, lifecycle/interaction-state framing, future implementation admission contract, hardening, Live Validation waiver truth, PR Readiness merge-target canon, and PR-R1 release-floor validator repair are preserved as historical evidence
- FB-032 is released and closed in `v1.6.2-prebeta`; source-of-truth inventory, naming policy, surface classification, controlled migration admission contract, governance repairs, hardening, Live Validation waivers, and PR Readiness merge-target canon are preserved as historical evidence
- FB-004 is released and closed in `v1.6.3-prebeta`; future boot-orchestrator source map, lifecycle/state framing, ownership boundaries, diagnostics evidence-root correction, rollback boundaries, stale helper caveat, implementation admission contract, hardening, Live Validation waivers, backlog governance sync, and PR Readiness merge-target canon are preserved as historical evidence
- post-release repo truth after the `v1.6.4-prebeta` release now carries FB-015 and FB-029 as released and closed while FB-030 owns active Workstream truth on `feature/fb-030-orin-voice-audio-direction-refinement`
- successor-lane branch creation for FB-039 is historical; FB-039 is released and no longer an executable active implementation branch
- if a branch changes release-facing canon, those canon updates must land on that same branch before PR readiness is allowed
- escaped post-merge canon repair must ride a legal branch surface; `main` is protected and must not be patched directly by Codex
- the released FB-027 family anchor does not authorize further saved-action authoring, resolution, voice, Action Studio, routines, profiles, hotkey cleanup, or shutdown-confirmation work by inertia
- remaining open backlog candidates now explicitly recorded in the backlog include:
  - FB-004 for future boot orchestrator layer, released and closed in `v1.6.3-prebeta`
  - FB-015 for boot and desktop phase-boundary model, released and closed in `v1.6.4-prebeta`
  - FB-029 for ORIN legal-safe rebrand, future ARIA persona option, and repo licensing hardening, released and closed in `v1.6.4-prebeta` and still implementation-gated for any later naming, licensing, release, runtime, or persona-facing execution
  - FB-030 for ORIN voice/audio direction refinement, `Medium`, promoted on `feature/fb-030-orin-voice-audio-direction-refinement`, and now carrying the explicit voice/audio design goal, ownership map, and conflict inventory needed for continued Workstream admission
  - FB-005 for workspace and folder organization, `Low`, promoted on `feature/fb-005-workspace-path-planning`, with historical proof that WS-1 `desktop/orin_desktop_test.py` -> `dev/desktop/orin_desktop_test.py` was the released slice on that branch under the earlier path-sensitive posture
- those candidate lanes must be selected deliberately rather than bundled together as one implicit interaction continuation
- FB-037 Branch Readiness does not imply automatic continuation into any remaining candidate lane

Use canonical workstream docs for execution detail.
Use the backlog for item identity.
