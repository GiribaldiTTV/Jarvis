# Branch Runtime Engineering Plan - FAM-006 Overlay Profile Runtime Foundation

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Overlay Profile Runtime Foundation Branch Runtime Engineering Plan`

Owning Branch: `feature/fam-006-overlay-profile-runtime-foundation`

Worktree Path: `C:\Nexus Worktrees\FAM-006`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md`

Current Phase: `Branch Readiness`

Stage Detail: `Branch Readiness Stage 2 setup`

Branch Runtime Engineering Plan: `Accepted for setup - runtime implementation remains pending USER approval after Workstream Entry analysis`

Engineering Plan Status: `Accepted - setup admitted with branch authority, package/slice scope, runtime boundaries, validation planning, and v1.7.10 closure-drift carry-forward recorded`

Current Runtime Baseline: `FAM-006 Dashboard and Monitor Groups / Sensor Command Center are released historical evidence. Monitor Groups organize and configure monitors. Overlay Profile and Recording Profile are source-truth-planned concepts, not implemented runtime surfaces. Overlay/display acceptance remains deferred/non-gating.`

Branch Purpose: `Prepare the next FAM-006 runtime lane by admitting the Overlay Profile foundation: data/state model, selection/editing entry points, monitor-to-overlay-profile mapping, Dashboard / Manage Monitors integration points, and validation/live proof planning.`

Planned Runtime Delta: `Future implementation should add a bounded Overlay Profile state foundation, active profile selection, profile editing shell, monitor membership mapping, and integration points from Dashboard and Manage Monitors while preserving existing Sensor Command Center behavior.`

User-Facing Delta: `Future users should be able to manage which monitors appear through an Overlay Profile and select the profile used by the overlay display. This setup does not change current user-facing runtime behavior.`

Source-Truth Delta: `Docs/feature_backlog.md, Docs/prebeta_roadmap.md, Docs/branch_records/index.md, this plan, and the branch authority record carry active branch truth. Validator registry updates are deferred unless implementation changes helper contracts. v1.7.10 release-dependent closure drift is carried into this setup and must stay resolved before runtime implementation proceeds.`

State / Config / Schema Delta: `Planned schema includes overlayProfileId, profile name, selected monitor ids, optional display metadata where admitted, active overlay profile selection, persistence boundaries, and dirty/clean edit state. Recording profile schema, recording output state, export/share state, provider state, and theme/skin state are excluded.`

Validator / Helper Delta: `Expected validators include branch governance, branch readiness planning fixture validation, release body validation, monitoring HUD surface validation, monitoring HUD internal sandbox validation, source-owner marker validation, compileall, and future live/human-client proof if UI changes are implemented.`

Expected Changed Files / Surfaces: `Likely implementation surfaces are nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.html, nexus_visual/monitoring_hud.css, desktop/monitoring_hud_state.py, desktop/monitoring_hud_controls.py, desktop/monitoring_hud_placement.py, desktop/desktop_renderer.py, dev/orin_monitoring_hud_surface_validation.py, dev/orin_monitoring_hud_internal_sandbox_validation.py, dev/orin_monitoring_hud_live_validation.ps1, dev/orin_monitoring_hud_human_client_validation.ps1, Docs/feature_backlog.md, Docs/prebeta_roadmap.md, this plan, and the branch record.`

Workstream / Seam Map: `Seam 1 / SLC-037 Overlay Profile state foundation; Seam 2 / SLC-038 profile selection and editing entry points; Seam 3 / SLC-039 monitor-to-overlay-profile mapping; Seam 4 / SLC-040 Dashboard / Manage Monitors integration; Seam 5 / SLC-041 focused validator and visual proof; Seam 6 PR readiness fold-down and release-scope translation.`

Per-Seam Implementation Checklist: `Define profile state; add or adapt persistence; add selection/editing entry points; map monitors to overlay profiles; integrate with Dashboard and Manage Monitors; preserve existing Monitor Groups behavior; update validators; update source truth; prove focused UI states.`

Per-Seam Validation Checklist: `Run git diff checks, branch governance validation, branch readiness planning fixture validation, release body validation, monitoring HUD surface validation, monitoring HUD internal sandbox validation, source-owner marker validation, compileall, and live/human-client proof after user-facing runtime changes.`

Per-Seam User-Facing Proof Checklist: `Focused local/WebView screenshots must prove every acceptance-critical UI state. Full-desktop screenshots may locate windows only and cannot be the acceptance proof. Proof must include normal, hover, active, focus, disabled, selected, open, dirty, confirmation, and close states where those controls exist.`

Future-Gated Items: `Recording Profile runtime implementation, tray recording controls, local recording output, export/share/import behavior, provider/model/memory/shortcut/installer work, broad theme/skin work, FAM-007 work, Governance worktree mutation, Compact-AI work, source-owner marker expansion, branch cleanup, PR creation, merge, release, issue mutation, artifacts, and raw evidence handling remain pending USER decisions.`

Approval-Boundary Audit: `USER approved Branch Readiness Stage 2 setup only. Runtime implementation, Workstream code changes, PR creation, merge, release, issues, and cleanup remain blocked until later explicit approval.`

FAM / Shared-Surface Overlap Forecast: `FAM-006 will touch HUD runtime, desktop renderer adjacency, source-truth, and validators. FAM-007 provider/model work remains separate. Governance remains standing intake only. Compact-AI remains untouched. Source-owner marker records are historical context only.`

Open Questions: `Final Overlay Profile UX details, display metadata depth, whether profile editing lives in Dashboard, Manage Monitors, or a separate child window, and any Overlay display acceptance criteria require Workstream Entry analysis before implementation.`

USER Planning Decisions: `USER approved Stage 1 analysis and Stage 2 setup for feature/fam-006-overlay-profile-runtime-foundation. USER has not approved runtime implementation, Recording Profile runtime, tray recording controls, export/share, PR creation, merge, release, issues, artifacts, branch cleanup, stale remote FAM-006 ref update, FAM-007 work, Governance mutation, Compact-AI mutation, or AI Product work.`

Plan Revision History: `v1 - created during Branch Readiness Stage 2 setup from origin/main b67e59df0481091bfbeb739c4b5e1954552bb421 after v1.7.10-prebeta publication and FAM-006 stable worktree restoration.`

Plan-To-Implementation Traceability Table: `Pending Workstream Entry and implementation. Future rows must map each seam to changed files, validators, proof artifacts, source-truth updates, and USER decisions.`

Hardening Comparison Checklist: `H1 must compare implementation against this plan, ensure Overlay Profile boundaries do not collapse into Monitor Groups or Recording Profiles, verify no Recording/Profile/tray/export/provider/theme/FAM-007 scope creep, verify focused visual proof quality, and verify all validators pass.`

Live Validation Proof Or Waiver Checklist: `LV1 must use real user-facing client/shortcut path when runtime UI changes exist, focused local proof for acceptance-critical states, and USER Test Summary only when the Live Validation stage is reached. USER waiver with reason is required for any unavailable live proof.`

PR Readiness Fold-Down / Retention Checklist: `PR Readiness must preserve branch authority, plan-to-implementation traceability, validation proof, selected-next/no-active projection, release-scope wording, future-gated decisions, branch cleanup posture, and stale remote FAM-006 branch hygiene status.`

Release Readiness Public-Scope Translation Checklist: `Release wording must describe Overlay Profile runtime behavior accurately, avoid claiming Recording Profile/tray/export/provider/theme work, and note any deferred Overlay display acceptance separately from implemented foundation behavior.`

USER Planning Review: `Complete for Branch Readiness Stage 2 setup; Workstream Entry analysis is the next USER decision.`

PR Fold-Down Packet: `Pending Workstream implementation, H1, Live Validation, and PR Readiness.`

Runtime Implementation Approval: `Pending - no runtime behavior changes are authorized by this setup.`
