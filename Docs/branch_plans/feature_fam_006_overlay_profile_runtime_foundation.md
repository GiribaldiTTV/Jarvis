# Branch Runtime Engineering Plan - FAM-006 Overlay Profile Runtime Foundation

## Branch Runtime Engineering Plan

Plan Identity: `FAM-006 Overlay Profile Runtime Foundation Branch Runtime Engineering Plan`

Owning Branch: `feature/fam-006-overlay-profile-runtime-foundation`

Worktree Path: `C:\Nexus Worktrees\FAM-006`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md`

Current Phase: `Workstream`

Stage Detail: `SLC-037 Overlay Profile data/state foundation H1 Green; SLC-038 Workstream Entry analysis next`

Branch Runtime Engineering Plan: `Active - SLC-037 implementation and H1 are mapped to this plan; later SLC-038 through SLC-041 remain pending USER decisions`

Engineering Plan Status: `SLC-037 implemented and H1 Green - Overlay Profile data/state foundation is present, validation-backed, and ready for SLC-038 Workstream Entry analysis`

Current Runtime Baseline: `FAM-006 Dashboard and Monitor Groups / Sensor Command Center are released historical evidence. Monitor Groups organize and configure monitors. Overlay Profile now has a bounded SLC-037 data/state foundation only; visible profile selection/editing, monitor-to-profile UI mapping, Recording Profile runtime, and Overlay/display acceptance remain future-gated.`

Branch Purpose: `Prepare the next FAM-006 runtime lane by admitting the Overlay Profile foundation: data/state model, selection/editing entry points, monitor-to-overlay-profile mapping, Dashboard / Manage Monitors integration points, and validation/live proof planning.`

Planned Runtime Delta: `SLC-037 adds bounded Overlay Profile state/schema, default active profile behavior, monitor membership normalization, persistence, and renderer/state bridge proof. Future SLC-038 through SLC-041 should add selection/editing controls, monitor-to-profile mapping, Dashboard / Manage Monitors integration, and focused live proof while preserving existing Sensor Command Center behavior.`

User-Facing Delta: `SLC-037 intentionally adds no visible profile editor UI. Future users should be able to manage which monitors appear through an Overlay Profile and select the profile used by the overlay display only after later USER-approved seams.`

Source-Truth Delta: `Docs/feature_backlog.md, Docs/prebeta_roadmap.md, Docs/branch_records/index.md, this plan, and the branch authority record carry active branch truth. Validator registry updates are deferred unless implementation changes helper contracts. v1.7.10 release-dependent closure drift is carried into this setup and must stay resolved before runtime implementation proceeds.`

State / Config / Schema Delta: `Implemented schema includes overlayProfileSchemaVersion, overlayProfiles, activeOverlayProfileId, default-overlay-profile, monitorIds membership, displayMode=monitor-cards, and normalization/migration for missing, stale, duplicate, or invalid references. Recording profile schema, recording output state, export/share state, provider state, and theme/skin state are excluded.`

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

Plan-To-Implementation Traceability Table: `SLC-037 -> nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.html, desktop/monitoring_hud_state.py, desktop/desktop_renderer.py, dev/orin_monitoring_hud_surface_validation.py, dev/orin_monitoring_hud_internal_sandbox_validation.py, Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md, Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation.md, Docs/feature_backlog.md, Docs/prebeta_roadmap.md. Proof: default profile migration, active fallback, monitor membership normalization, save/load persistence, MONITORING_HUD_OVERLAY_PROFILE_STATE_READY bridge signal, concept separation, and no visible profile editor UI.`

Hardening Comparison Checklist: `H1 compared implementation against this plan, ensured Overlay Profile boundaries do not collapse into Monitor Groups or Recording Profiles, verified no Recording/Profile/tray/export/provider/theme/FAM-007 scope creep, preserved no-visible-profile-editor posture, and reran validators.`

Hardening H1 Result: `Green - SLC-037 schema/default/migration/persistence/renderer-bridge/concept-boundary proof passed during bounded source-truth posture repair. Evidence basis includes HUD surface validation, HUD internal sandbox validation manifest C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_internal_sandbox\20260520_172108_manifest.json, branch governance validation, worktree-confinement gate, release-readiness health gate, branch readiness planning fixture validation, release body validation, AI provider state validation, source-owner marker validation, compileall, bundled Node syntax check, and runtime-fam006 validation-suite recommendation review.`

Live Validation Proof Or Waiver Checklist: `LV1 must use real user-facing client/shortcut path when runtime UI changes exist, focused local proof for acceptance-critical states, and USER Test Summary only when the Live Validation stage is reached. USER waiver with reason is required for any unavailable live proof.`

PR Readiness Fold-Down / Retention Checklist: `PR Readiness must preserve branch authority, plan-to-implementation traceability, validation proof, selected-next/no-active projection, release-scope wording, future-gated decisions, branch cleanup posture, and stale remote FAM-006 branch hygiene status.`

Release Readiness Public-Scope Translation Checklist: `Release wording must describe Overlay Profile runtime behavior accurately, avoid claiming Recording Profile/tray/export/provider/theme work, and note any deferred Overlay display acceptance separately from implemented foundation behavior.`

USER Planning Review: `Complete for Branch Readiness Stage 2 setup and Workstream Entry; USER approved SLC-037 implementation.`

PR Fold-Down Packet: `Pending SLC-038 through SLC-041 seams, Live Validation when user-facing controls exist, and PR Readiness.`

Runtime Implementation Approval: `Granted for SLC-037 only and now H1 Green; SLC-038 visible profile selection/editing implementation and later seams remain pending USER decisions.`
