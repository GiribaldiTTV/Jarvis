# Nexus Feature Backlog
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=SHARED-DOCS; ledger=SRCOWN-FIRSTPASS-DOCS-011; surface=compact-current-state-owner; status=shared -->

## Purpose

`Docs/feature_backlog.md` is the compact product registry and pointer layer for Nexus feature-family work.

Docs Source-Truth Reform Model: Compact Pointer Layer.

This file owns feature-family identity, priority, broad status, family scope, package posture summary, and canonical pointers. It does not own live Git/GitHub state, active branch state, live PR state, latest release state, release-window inventories, package trace tables, slice trace tables, or long branch-history narration.

Use Git, GitHub, or approved helpers for live operational truth. Use branch records, branch plans, workstream records, and family dossiers for detailed planning, implementation proof, package/slice history, and branch receipts.

## Registry Rules

- `Status` is the delivery or work field.
- `Record State` is the canonical-record lifecycle field.
- `Priority` is the primary backlog selection signal for open candidate work.
- `Target Version` is not an open-backlog selection field and must not be used to rank, select, defer, or skip open backlog candidates.
- `Registry-only` means tracked identity only; no canonical workstream execution record is required yet.
- `Promoted` means a canonical workstream or branch-plan owner is required for execution detail.
- `Closed` means the canonical workstream or branch record remains stable historical truth after closure.
- Backlog entries keep the short registry story, not the full execution story.

## Ownership Boundaries

| Fact Class | Owner |
| --- | --- |
| Live branch, worktree, `HEAD`, ahead/behind, PR, review, tag, or release state | Git, GitHub, or approved helper output |
| Feature family identity, broad priority, high-level status, and pointer routing | `Docs/feature_backlog.md` |
| Branch authority, approvals, current phase, blockers, and legal next phase | `Docs/branch_records/<branch>.md` |
| Active runtime implementation plan, seam checklist, proof plan, and plan-to-implementation trace | `Docs/branch_plans/<branch>.md` |
| Durable package trace, slice trace, proof history, branch lessons, and reusable continuity | `Docs/workstreams/` records or family dossiers |
| Release sequencing and public milestone posture | `Docs/prebeta_roadmap.md` |

Canonical Identity Model: `FAM` = broad long-lived product family; `Package` = bulk branch/release package under one family; `Slice` = traceable deliverable area inside a package; `Seam` = execution or validation checkpoint; `PR` = merge/review evidence only; legacy global `FB` = historical trace only.

Branch Scope Standard: branches must package multiple related admitted slices under exactly one broad family by default. A package with exactly one admitted slice is blocked by `Single-Slice Package User Approval Missing` unless `Single-Slice Package User Approval: Granted` is recorded with explicit USER approval.

Package Completion Standard: Workstream continues through every admitted package slice until `Package Completion State: Complete`, `Released Baseline / Open`, `Blocked`, or `Deferred` is truthfully recorded before Hardening admission.

Admitted Slice Counting Rule: only rows with `Admission State` equal to `Admitted` count toward a package's admitted-slice total. Package slices must trace to exactly one FAM and exactly one package in the owning workstream or family dossier.

Concrete Admitted Slice Rule: an admitted slice must have a concrete scoped deliverable, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder rows cannot be marked admitted.

Package Completion Guard: `Package Completion State: Complete` is blocked while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while another admitted slice remains incomplete.

Named Package Blockers: `Single-Slice Package User Approval Missing` and `Package Completion Unproven`.

PR Evidence Standard: PR numbers are evidence only and must not become backlog identities, package identities, release-version drivers, or selected-next successors.

Element Coverage Standard: Element Coverage is a non-identity checklist for FAM/package review only. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

The old `FB-###` namespace is historical-only after this one-time repair; new live backlog-family identities use `FAM-###`, starting at `FAM-001`, and Codex must not create or reuse a parseable `FB-###` backlog ID.

Selectable user-facing feature-family records now use the fresh `FAM-###` namespace in ascending order from `FAM-001`.

Live backlog-family identities use the fresh broad `FAM-###` namespace starting at `FAM-001`; legacy `FB-###` IDs are historical trace only and must not be reused for new parseable backlog entries.

Only true broad feature-family backlog entries should remain as parseable `### [ID: FAM-XXX]` backlog records by default.

The live backlog-family namespace is broad `FAM-###`, starting at `FAM-001`; the old `FB-###` namespace is historical-only and must not be reused for parseable backlog entries.

## Derived Live Truth

Current release, current PR, branch cleanliness, branch freshness, and tag truth are intentionally not recorded here as active state. Run the relevant Git/GitHub/helper checks when that truth is needed:

- `git status --short --branch`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git merge-base HEAD origin/main`
- `git worktree list`
- `gh pr view`
- `gh release view`
- `git ls-remote --tags origin`
- `python dev\orin_worktree_rebaseline_audit.py --target-ref origin/main`

## Canonical Pointer Summary

| Layer | Pointer |
| --- | --- |
| Branch authority router | `Docs/branch_records/index.md` |
| Branch runtime engineering plans | `Docs/branch_plans/` |
| Family vision records | `Docs/family_visions/` |
| Workstream routing and family dossiers | `Docs/workstreams/index.md` |
| Stable worktree slot registry | `Docs/worktree_slots.md` |
| Stage-breakpoint schedule posture | `Docs/prebeta_roadmap.md` |
| Full reform audit | `Docs/governance_docs_full_inventory_reform_audit.md` |

## Registry Items

### User-Facing Feature Families

| FAM ID | Broad Product Family | Priority | Status | Package Posture | Family Vision Owner | Canonical Detail Owner |
| --- | --- | --- | --- | --- | --- | --- |
| `FAM-001` | Boot Interface | High | Open / released-baseline aggregation | `PKG-001` released baseline / open | `Docs/family_visions/FAM-001_boot_interface.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` |
| `FAM-002` | Desktop Interface | Medium | Open / pending user-facing follow-through | `PKG-002` released baseline / open | `Docs/family_visions/FAM-002_desktop_interface.md` | `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md` |
| `FAM-003` | Interaction and Actions | High | Open / aggregation-held | `PKG-003` released baseline / open | `Docs/family_visions/FAM-003_interaction_and_actions.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` |
| `FAM-004` | Voice and Audio | Medium | Open / released-baseline aggregation | `PKG-004` released baseline / open | `Docs/family_visions/FAM-004_voice_and_audio.md` | `Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md` |
| `FAM-005` | External Integrations | Medium | Pending implementation | `PKG-005` released baseline / open | `Docs/family_visions/FAM-005_external_integrations.md` | `Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md` |
| `FAM-006` | Monitoring and HUD | High | Open / Overlay Display Acceptance Foundation Workstream Green; SLC-042 through SLC-045 complete; Hardening H1 next after current-main reconciliation; released Dashboard, Sensor Command Center, and Overlay Profile foundation evidence preserved | `PKG-006` released baseline / open | `Docs/family_visions/FAM-006_monitoring_and_hud.md` | `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md` |
| `FAM-007` | Local AI and Capability Packs | High | Open / package admitted; consent collection implementation foundation PR Readiness Stage 1 Ready For Stage 2 / PR creation pending USER approval | `PKG-007` admitted / not package-complete | `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` | `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md` |
| `FAM-008` | Packaging and Install Experience | Medium | Pending architecture/package | `PKG-008` pending | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` |
| `FAM-009` | Workspace and Data | Low | Open / deferred follow-through | `PKG-009` released baseline / open | `Docs/family_visions/FAM-009_workspace_and_data.md` | `Docs/workstreams/FB-005_workspace_and_folder_organization.md` |
| `FAM-010` | Safety and Privacy | High | Pending architecture/package | `PKG-010` pending | `Docs/family_visions/FAM-010_safety_and_privacy.md` | `Docs/family_visions/FAM-010_safety_and_privacy.md` |

### [ID: FAM-001] Boot Interface

Status: Open / released-baseline aggregation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Startup, boot, desktop entrypoint, single-instance ownership, launch handoff, relaunch semantics, lifecycle transition proof, and boot-to-runtime trust boundaries.
Package Summary: `PKG-001` released baseline / open.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
Family Vision Owner: `Docs/family_visions/FAM-001_boot_interface.md`
Historical Trace Coverage: `FB-042`, `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`, `FB-049`, PR #86-#107.

### [ID: FAM-002] Desktop Interface

Status: Open / pending user-facing follow-through
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Nexus desktop shell, visual language, operator UI, settings presentation, user-facing desktop interaction surfaces, and coherent UI/UX implementation packages.
Package Summary: `PKG-002` released baseline / open.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md`
Family Vision Owner: `Docs/family_visions/FAM-002_desktop_interface.md`
Historical Trace Coverage: `FB-031`, UI/UX planning release evidence.

### [ID: FAM-003] Interaction and Actions

Status: Open / aggregation-held
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Shared actions, command/action UX, callable groups, taskbar/tray quick-task interaction, saved action authoring, and user-visible confirmation/interaction contracts.
Package Summary: `PKG-003` released baseline / open.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
Family Vision Owner: `Docs/family_visions/FAM-003_interaction_and_actions.md`
Historical Trace Coverage: `FB-027`, `FB-036`, `FB-037`, `FB-038`, `FB-041`, PR #109.

### [ID: FAM-004] Voice and Audio

Status: Open / released-baseline aggregation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Voice availability, audio path direction, voice diagnostics, truthful disabled/degraded copy, and future persona/audio capability boundaries.
Package Summary: `PKG-004` released baseline / open.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md`
Family Vision Owner: `Docs/family_visions/FAM-004_voice_and_audio.md`
Historical Trace Coverage: `FB-030`, PR #108.

### [ID: FAM-005] External Integrations

Status: Pending implementation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: External trigger intake, plugin integration, external control surfaces, and safe integration boundaries.
Package Summary: `PKG-005` released baseline / open.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md`
Family Vision Owner: `Docs/family_visions/FAM-005_external_integrations.md`
Historical Trace Coverage: `FB-039`, Stream Deck and external trigger planning gap.

### [ID: FAM-006] Monitoring and HUD

Status: Open / Overlay Display Acceptance Foundation Workstream Green; SLC-042 through SLC-045 complete; Hardening H1 next after current-main reconciliation; released Dashboard, Sensor Command Center, and Overlay Profile Runtime Foundation evidence preserved
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Monitoring HUD, Dashboard, Sensor Command Center, Sensor Library, monitor configuration, Overlay Profile, Recording Profile, local telemetry presentation, and user-facing performance/health surfaces.
Package Summary: `PKG-006` released baseline / open; active successor setup is `feature/fam-006-overlay-display-acceptance-foundation`, while detailed Monitor Groups, Sensor Library, Overlay Profile, Recording Profile, returned USER UTS, interactive-control visual QA, right-edge resize rediscovery, visual proof, Warning Notifications, Provider Readiness, and Sensor Command Center history live in FAM-006 branch authority records and related workstream evidence.
Package Admission State: Historical baseline / no active package admission in this backlog file
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
Family Vision Owner: `Docs/family_visions/FAM-006_monitoring_and_hud.md`
Historical Trace Coverage: `FB-040`, HUD surface gap, PR #118, PR #180, PR #194, FAM-006 branch records. Historical Overlay Profile Runtime Foundation detail remains at `Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md`.

### [ID: FAM-007] Local AI and Capability Packs

Status: Open / package admitted; consent collection implementation foundation PR Readiness Stage 1 Ready For Stage 2 / PR creation pending USER approval after released setup implementation and consent foundation evidence
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Local AI, provider setup, provider readiness, consent posture, consent collection, capability packs, model lifecycle, local-only privacy boundaries, provider-visible data, execution gates, memory/future learning boundaries, and Core/Desktop AI state.
Package Summary: `PKG-007` admitted with multiple historical and future-gated slices; not package-complete because provider SDK/model execution, downloads, external calls, memory/indexing/learning/personalization, voice/Core runtime sync, shortcut/installer work, capability-pack execution, and AI Product Contract import remain USER-gated.
Package Admission State: Admitted / detailed history is branch-record, branch-plan, workstream, or family-dossier owned
Admitted Slice Count: see `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
Package Completion State: Open / not package-complete
Single-Slice Package User Approval: Not required - package history is multi-slice; future scope still requires USER approval.
Canonical Detail Owner: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
Family Vision Owner: `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`
Historical Branch Runtime Engineering Plans: `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_implementation_foundation.md`; `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_foundation.md`; active plan `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
Historical Trace Coverage: FAM-007 branch records, PR #138, PR #152, PR #159, PR #162, PR #165, PR #170, PR #172, PR #177, PR #179, PR #190, PR #192, PR #193, and current PR Readiness Stage 1 Ready For Stage 2 posture for `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`.

### [ID: FAM-008] Packaging and Install Experience

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Installer, shortcuts, packaged app experience, model/capability-pack install boundaries, update flow, and user-facing setup lifecycle.
Package Summary: `PKG-008` pending.
Package Admission State: Not admitted
Admitted Slice Count: 0
Package Completion State: Not admitted
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/family_visions/FAM-008_packaging_and_install_experience.md`
Family Vision Owner: `Docs/family_visions/FAM-008_packaging_and_install_experience.md`
Historical Trace Coverage: no legacy FB trace; repo vision trace only.

### [ID: FAM-009] Workspace and Data

Status: Open / deferred follow-through
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Low
Deferred Since: historical released-baseline migration
Deferred Because: workspace/data follow-through is not the current USER-selected implementation package.
Selection / Unblock: USER-approved Branch Readiness must admit a concrete multi-slice workspace/data package.
Family Scope: Workspace layout, data roots, logs/evidence organization, support bundles, dev-toolkit data intake, and local file hygiene.
Package Summary: `PKG-009` released baseline / open.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/workstreams/FB-005_workspace_and_folder_organization.md`
Family Vision Owner: `Docs/family_visions/FAM-009_workspace_and_data.md`
Historical Trace Coverage: `FB-005`, `FB-020`, `FB-026`, `FB-028`, workspace/data trace.

### [ID: FAM-010] Safety and Privacy

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Local-first privacy, consent, provider-visible data boundaries, safety gates, secrets handling, data egress controls, and future AI safety posture.
Package Summary: `PKG-010` pending.
Package Admission State: Not admitted
Admitted Slice Count: 0
Package Completion State: Not admitted
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/family_visions/FAM-010_safety_and_privacy.md`
Family Vision Owner: `Docs/family_visions/FAM-010_safety_and_privacy.md`
Historical Trace Coverage: no legacy FB trace; repo vision trace only.

## Historical Trace Pointers

Former standalone historical pass backlog entries now live here as family traceability only. Historical pass aliases, support/governance lanes, and old registry-only implemented records are trace tables, not backlog items.

### Historical Family Pass Aliases

| Legacy FB ID | Pass ID | Family Anchor | Workstream Record | Family Dossier | Release / Receipt | Posture |
| --- | --- | --- | --- | --- | --- | --- |
| `FB-048` | `F042-P07` | `FB-042` | `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.12-prebeta` | Historical family pass only; not selectable |
| `FB-047` | `F042-P06` | `FB-042` | `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.11-prebeta` | Historical family pass only; not selectable |
| `FB-046` | `F042-P05` | `FB-042` | `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.10-prebeta` | Historical family pass only; not selectable |
| `FB-045` | `F042-P04` | `FB-042` | `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.9-prebeta` | Historical family pass only; not selectable |
| `FB-044` | `F042-P03` | `FB-042` | `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.9-prebeta` | Historical family pass only; not selectable |
| `FB-043` | `F042-P02` | `FB-042` | `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.8-prebeta` | Historical family pass only; not selectable |
| `FB-041` | `F027-P03` | `FB-027` | `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.3.1-prebeta` | Historical family pass only; not selectable |
| `FB-038` | `F027-P05` | `FB-027` | `Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.4.1-prebeta` | Historical family pass only; not selectable |
| `FB-037` | `F027-P04` | `FB-027` | `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | historical receipt | Historical family pass only; not selectable |
| `FB-036` | `F027-P02` | `FB-027` | `Docs/workstreams/FB-036_saved_action_authoring.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.3.0-prebeta` | Historical family pass only; not selectable |

### Historical Support, Architecture, And Governance Lanes

Closed support, architecture, and governance lanes are historical traceability only.

| Legacy FB ID | Title | Canonical Record | Historical Receipt | Posture |
| --- | --- | --- | --- | --- |
| `FB-035` | Support-report release-context fallback hardening | `Docs/workstreams/FB-035_release_context_fallback_hardening.md` | `v1.2.7-prebeta` | Closed support lane trace |
| `FB-034` | Recoverable incident diagnostics surface and failure-class follow-through | `Docs/workstreams/FB-034_recoverable_diagnostics.md` | historical release receipt | Closed support lane trace |
| `FB-033` | Dev-only startup snapshot harness follow-through | `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md` | historical release receipt | Closed support lane trace |
| `FB-032` | Nexus-era vision and source-of-truth migration | `Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md` | `v1.6.2-prebeta` | Closed architecture/governance trace |
| `FB-029` | ORIN identity and licensing hardening | `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md` | `v1.6.4-prebeta` | Closed architecture trace |
| `FB-028` | Relocate launcher history state out of root logs | `Docs/workstreams/FB-028_history_state_relocation.md` | historical release receipt | Closed support lane trace |
| `FB-025` | Boot and desktop milestone taxonomy clarification | `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md` | historical release receipt | Closed architecture trace |
| `FB-015` | Boot and desktop phase-boundary model | `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md` | `v1.6.4-prebeta` | Closed architecture trace |
| `FB-005` | Workspace and folder organization | `Docs/workstreams/FB-005_workspace_and_folder_organization.md` | `v1.6.6-prebeta` | Closed support lane trace |
| `FB-004` | Future boot orchestrator layer | `Docs/workstreams/FB-004_future_boot_orchestrator_layer.md` | `v1.6.3-prebeta` | Closed architecture trace |

### Historical Implemented Registry-Only Items

Old implemented registry-only IDs are preserved as same-file historical trace.

| Legacy FB ID | Title | Historical Receipt |
| --- | --- | --- |
| `FB-001` | Repeated identical crash early escalation | Implemented `v1.6.0`; historical registry trace in `Docs/feature_backlog.md` |
| `FB-002` | Mixed failure-pattern policy | Historical registry trace |
| `FB-003` | Retry limit and diagnostics escalation policy | Historical registry trace |
| `FB-006` | Threshold-based recovery outcome summary refinement | Historical registry trace |
| `FB-007` | Max-attempt identical-failure attempt-pattern correction | Historical registry trace |
| `FB-008` | Shutdown voice degradation effect | Historical registry trace |
| `FB-009` | Align crash-origin mixed markers with stable repeated-failure summaries | Historical registry trace |
| `FB-010` | v1.6.0 closeout and documentation sync | Historical registry trace |
| `FB-011` | Historical memory contract | Historical registry trace |
| `FB-012` | Failure fingerprint and recurrence model | Historical registry trace |
| `FB-013` | Advisory provenance and confidence semantics | Historical registry trace |
| `FB-014` | Multi-run orchestration regression harness | Historical registry trace |
| `FB-016` | Recorder-only historical memory groundwork | Historical registry trace |
| `FB-017` | Support bundle and GitHub issue prefill | Historical registry trace |
| `FB-018` | Voice-path regression validation harness | Historical registry trace |
| `FB-019` | Support bundle to repro triage helper | Historical registry trace |
| `FB-020` | Dev Toolkit utility split and dev-only evidence roots | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-021` | Dev-only Boot Nexus test lane | Historical registry trace |
| `FB-022` | Boot & Transition Checks Dev Toolkit surfacing | Historical registry trace |
| `FB-023` | Desktop renderer observability gap closure | Historical registry trace |
| `FB-024` | Boot harness edge-path observability refinement | Historical registry trace |
| `FB-026` | Dev Toolkit uploaded-bundle intake surface | Implemented `v2.2.0`; historical registry trace in `Docs/feature_backlog.md` |
