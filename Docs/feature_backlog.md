# Nexus Feature Backlog
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=SHARED-DOCS; ledger=SRCOWN-FIRSTPASS-DOCS-011; surface=compact-current-state-owner; status=shared -->

## Purpose

`Docs/feature_backlog.md` is the compact product registry and pointer layer for Nexus feature-family work.

Docs Source-Truth Reform Model: Compact Pointer Layer.

This file is an index. It owns feature-family identity, priority, durable registry posture, family scope, package posture summary, and canonical pointers. It does not own live Git/GitHub state, active branch state, live PR state, latest release state, release-window inventories, package trace tables, slice trace tables, branch-plan ledgers, or long branch-history narration.

Use Git, GitHub, approved helpers, or `C:\Nexus Governance State` for live operational truth. Use branch records, branch plans, workstream records, and family dossiers as durable evidence pointers or historical receipts only; active detailed planning and implementation ledgers belong outside this backlog index.

## Registry Rules

- `Status` is a durable registry posture field, not active operational state.
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
| Durable branch identity, approvals, and historical receipt pointers | `Docs/branch_records/<branch>.md` |
| Active branch lifecycle, current phase, blockers, legal next phase, runtime implementation plan, seam checklist, proof plan, and plan-to-implementation trace | `C:\Nexus Governance State\branches\<branch_slug>\` or approved helper-derived packets |
| Durable package trace, slice trace, proof history, branch lessons, and reusable continuity | `Docs/workstreams/` records or family dossiers |
| Release sequencing and public milestone posture | `Docs/prebeta_roadmap.md` |

Canonical Identity Model: `FAM` = broad long-lived product family; `Package` = bulk branch/release package under one family; `Slice` = traceable deliverable area inside a package; `Seam` = execution or validation checkpoint; `PR` = merge/review evidence only; legacy global `FB` = historical trace only.

Backlog Taxonomy And Source-Truth Placement Gate: before Codex proposes, admits, or syncs any new backlog family, package, source-truth owner, architecture layer, policy owner, experience layer, runtime subsystem, capability-pack domain, or implementation slice/seam, the governing packet must answer: `Is this a backlog family, family vision, architecture layer, cross-family policy owner, experience layer, runtime subsystem, capability-pack domain, or implementation package/slice/seam?`

| Concept Class | Should Own | Must Not Own |
| --- | --- | --- |
| Backlog family | Broad long-lived product identity and compact registry pointer | Every subsystem, dependency, architecture idea, policy, or implementation package |
| Family vision | Durable direction for one family | Cross-family architecture, runtime approval, or active branch authority by default |
| Architecture layer | Reusable structural system concepts | Product-family identity, release identity, or implementation approval by itself |
| Cross-family policy owner | Hard rules, constraints, enforcement requirements, and safety/privacy boundaries across families | Runtime identity or implementation scope by itself |
| Experience layer | Interaction philosophy, UX orchestration, and user-facing behavioral model | Automatic backlog identity or implementation approval |
| Runtime subsystem | Executable behavior, service, tool, state machine, or persistence/control path | Canon identity, release identity, or family vision by itself |
| Capability-pack domain | Modular capability, knowledge, tool, model, manifest, or pack category | Automatic new FAM, provider execution approval, or memory approval |
| Package/slice/seam | Bounded implementation and proof work inside one admitted family/package | Product vision expansion or new backlog identity by itself |

Important concepts do not automatically deserve backlog identity. AI-native, cache, trust, provider, routine, deterministic-routing, Windows Health, gaming/competitive-integrity, or ambient-assistance concepts must pass this gate before they can become a new FAM, package, source-truth file, or implementation scope. `Backlog Taxonomy Gate Missing` blocks Branch Readiness or PR Readiness when a concept is promoted without this classification, and `Backlog Addition User Approval Missing` remains active when a new backlog family would be required.

AI Operational Cache Governance is not a backlog family. Cache is operational, purpose-bound, explainable, clearable, and policy-governed; memory is durable user-personal knowledge and requires separate explicit consent. Cross-family cache architecture and policy route through `Docs/ai_runtime_and_trust_architecture.md`; family-specific cache concepts route through existing AI/runtime, privacy/safety, workspace/data, packaging/setup, capability-pack, and branch-plan owners unless a `Source-Truth Placement Preflight` proves `No Existing Owner Fits`.

AI-native architecture placement is now routed without adding backlog families by default: `Docs/ai_runtime_and_trust_architecture.md` owns cross-family permission-state, deterministic routing, provider-orchestration boundaries, AI Operational Cache Governance, Trust Journal direction, capability-pack architecture, routine/continuity boundaries, Windows Health recommendation pipeline boundaries, and competitive-integrity architecture. Future branches may consume those concepts only after the taxonomy gate names whether the proposed work is a family vision update, architecture layer, cross-family policy owner, experience layer, runtime subsystem, capability-pack domain, or package/slice/seam.

Branch Scope Standard: branches must package multiple related admitted slices under exactly one broad family by default. A package with exactly one admitted slice is blocked by `Single-Slice Package User Approval Missing` unless `Single-Slice Package User Approval: Granted` is recorded with explicit USER approval.

Package Completion Standard: Workstream continues through every admitted package slice until `Package Completion State: Complete`, `Released Baseline / Open`, `Blocked`, or `Deferred` is truthfully recorded before Hardening admission.

Admitted Slice Counting Rule: only rows with `Admission State` equal to `Admitted` count toward a package's admitted-slice total. Package slices must trace to exactly one FAM and exactly one package in the owning workstream or family dossier.

Concrete Admitted Slice Rule: an admitted slice must have a concrete scoped deliverable, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder rows cannot be marked admitted.

Package Completion Guard: `Package Completion State: Complete` is blocked while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while another admitted slice remains incomplete.

Named Package Blockers: `Single-Slice Package User Approval Missing` and `Package Completion Unproven`.

PR Evidence Standard: PR numbers are evidence only and must not become backlog identities, package identities, release-version drivers, or selected-next successors.

Element Coverage Standard: Element Coverage is a non-identity checklist for FAM/package review only. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

The old `FB-###` namespace is historical-only after this one-time repair; live backlog-family identities use `FAM-###`, starting at `FAM-001`, and Codex must not create or reuse a parseable `FB-###` backlog ID.

Selectable user-facing feature-family records now use the fresh `FAM-###` namespace in ascending order from `FAM-001`; the current registry ends at `FAM-008` unless USER approves a later backlog-family admission.

Live backlog-family identities use the fresh broad `FAM-###` namespace starting at `FAM-001`; legacy `FB-###` IDs are historical trace only and must not be reused for new parseable backlog entries. Because the current registry ends at `FAM-008`, the next USER-approved backlog family may use `FAM-009`.

Only true broad feature-family backlog entries should remain as parseable `### [ID: FAM-XXX]` backlog records by default.

The live backlog-family namespace is broad `FAM-###`, starting at `FAM-001`; the current admitted registry ends at `FAM-008`, and the old `FB-###` namespace is historical-only and must not be reused for parseable backlog entries.

Backlog Family Worktree Ownership Rule: a backlog family is the local owner for its work. Work related to a backlog family should be planned and implemented inside that family's legal branch/worktree carrier. Backlog families are not dependency work queues for each other. If a branch needs another family's future implementation before it can continue, it must record the dependency as deferred/future-gated work, stop or narrow scope as governance requires, and wait for the owning family/worktree to implement its part through its own Branch Readiness path. A branch must not implement another backlog family's responsibilities merely to unblock itself.

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
| AI runtime and trust architecture | `Docs/ai_runtime_and_trust_architecture.md` |
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
| `FAM-006` | Monitoring and HUD | High | Open / Active Overlay Recording Runtime Implementation Branch Readiness Stage 2 setup | `PKG-006` active-overlay recording implementation carrier is admitted for setup; Workstream Entry and runtime recording implementation remain future-gated and USER-gated; released planning traceability remains preserved in `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md` | `Docs/family_visions/FAM-006_monitoring_and_hud.md` | `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md` |
| `FAM-007` | Local AI and Capability Packs | High | Open / package admitted | `PKG-007` remains admitted and not package-complete; durable planning pointers preserve FAM-007 Breakpoint 2 Dev/Owner skeleton action-gate readiness context while live operational state remains external/Git/GitHub/helper-derived | `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` | `Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md` |
| `FAM-008` | Packaging and Install Experience | Medium | Pending architecture/package | `PKG-008` pending | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` |

### Folded Non-Family Concepts

Workspace/data and safety/privacy concepts are not backlog families in this registry. Their durable constraints are folded into the relevant existing FAM vision records and `Docs/ai_runtime_and_trust_architecture.md`; implementation remains local to the owning backlog family/worktree that is actually building the affected surface.

| Concept Area | Folded Owner Path |
| --- | --- |
| Workspace/data roots, evidence paths, cache storage hygiene, support bundles, cleanup, backup/export implications | `Docs/ai_runtime_and_trust_architecture.md`, `Docs/architecture.md`, `Docs/family_visions/FAM-006_monitoring_and_hud.md`, `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`, and `Docs/family_visions/FAM-008_packaging_and_install_experience.md` as applicable |
| Safety/privacy, provider-visible data, local-only proof, Trust Journal policy, sensitive capabilities, competitive integrity, and privacy lockdown | `Docs/ai_runtime_and_trust_architecture.md`, `Docs/family_visions/FAM-003_interaction_and_actions.md`, `Docs/family_visions/FAM-005_external_integrations.md`, `Docs/family_visions/FAM-006_monitoring_and_hud.md`, `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`, and `Docs/family_visions/FAM-008_packaging_and_install_experience.md` as applicable |

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

Status: Open / Active Overlay Recording Runtime Implementation Branch Readiness Stage 2 setup
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Monitoring HUD, Dashboard, Sensor Command Center, Sensor Library, monitor configuration, Overlay Profile, Recording Profile, local telemetry presentation, and user-facing performance/health surfaces.
Package Summary: `PKG-006` active-overlay recording implementation carrier is admitted for Branch Readiness Stage 2 setup. Active-overlay-driven recording, HUD Overlay launcher/target preview, compact Recording Control window, Native Log Loader boundary, and per-overlay effective polling policy remain governed by the family vision and active branch plan; released planning traceability remains preserved in `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md`, and runtime recording implementation remains future-gated until Workstream Entry and USER implementation approval.
Package Admission State: Branch Readiness Stage 2 setup / runtime implementation pending Workstream Entry and USER approval
Admitted Slice Count: 5 planned slices in `Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Package Completion State: Not started / Workstream Entry pending
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.
Canonical Detail Owner: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
Family Vision Owner: `Docs/family_visions/FAM-006_monitoring_and_hud.md`
Historical Trace Coverage: `FB-040`, FAM-006 branch records, family vision, workstream evidence, and public release receipts. Detailed PR, branch, rollback, UTS, visual-proof, and release interpretation lives in canonical detail owners, not this compact backlog registry.

### [ID: FAM-007] Local AI and Capability Packs

Status: Open / package admitted; detailed released-readiness and post-release receipts live in canonical detail owners
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Local AI, provider setup, provider readiness, consent posture, consent collection, capability packs, model lifecycle, local-only privacy boundaries, provider-visible data, execution gates, memory/future learning boundaries, and Core/Desktop AI state.
Package Summary: `PKG-007` is admitted with historical and future-gated slices; not package-complete because provider/model execution, downloads, memory/indexing/learning/personalization, voice/Core runtime sync, shortcut/installer work, capability-pack execution, and AI Product Contract import remain USER-gated.
Package Admission State: Admitted / detailed history is branch-record, branch-plan, workstream, or family-dossier owned
Admitted Slice Count: see `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
Package Completion State: Open / not package-complete
Single-Slice Package User Approval: Not required - package history is multi-slice; future scope still requires USER approval.
Canonical Detail Owner: `Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md`
Family Vision Owner: `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`
Future Planning Evidence: FAM-007 Breakpoint 2 private Dev/Owner skeleton setup decision remains durable planning context for the existing FAM-007 backlog family; current branch-local setup proof is recorded by the Breakpoint 2 action-gate readiness branch record and plan.
Branch Evidence Pointer: `Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md`
Minimal Scope: FAM-007 runtime action-gate planning slice for Breakpoint 2 private Dev/Owner skeleton setup decision, preserving provider/model/runtime/cache/memory execution as later USER-gated work.
Operational Selection Owner: `C:\Nexus Governance State` plus Git/GitHub/helper live checks own selected-next, branch creation, active/complete status, PR state, review state, watcher state, merge state, release-window posture, and worktree posture.
Selection / Unblock Boundary: This compact backlog row may name durable family direction and branch evidence pointers, but it must not create a new backlog family, branch, private repo, private remote, provider/model execution path, runtime cache behavior, memory behavior, release action, or live lifecycle state.
Historical Branch Runtime Engineering Plans: see FAM-007 branch-plan records under `Docs/branch_plans/`.
Historical Trace Coverage: FAM-007 branch records, family vision, branch plans, workstream evidence, and public release receipts. Detailed PR, release-readiness, post-release, and canon-closure interpretation lives in canonical detail owners, not this compact backlog registry.

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
