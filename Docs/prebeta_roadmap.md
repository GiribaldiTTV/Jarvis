# Nexus Pre-Beta Roadmap
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=SHARED-DOCS; ledger=SRCOWN-FIRSTPASS-DOCS-011; surface=compact-current-state-owner; status=shared -->

## Purpose

`Docs/prebeta_roadmap.md` owns the pre-Beta schedule outline: the release-stage breakpoints, milestone gates, and broad feature-family checkpoints that explain what must be true before the project moves from pre-Beta toward Beta and release.

Docs Source-Truth Reform Model: Compact Pointer Layer.

This file is a reference outline, not a release ledger. It does not own live latest-release state, live tag state, active branch state, open PR state, current review state, worktree freshness, or release-window inventories. Those are derived from Git, GitHub, and approved helpers at the time of Release Readiness or release execution.

## Authority And Boundaries

Roadmap owns:

- pre-Beta, Beta, and release breakpoint criteria
- broad feature checkpoint ordering
- high-level user-facing milestone grouping
- schedule reference language for what must be finished before later release stages
- pointers to backlog, branch records, branch plans, workstreams, and GitHub Releases
- historical interpretation only when it is compact and explicitly receipt-oriented

Roadmap does not own:

- latest public prerelease as manually maintained active truth
- current `origin/main`, release target commit, or tag commit
- merged-unreleased PR lists as active truth
- active runtime branch identity
- PR Readiness, watcher, mergeability, or review-thread state
- Package Trace or Slice Trace detail
- branch execution diaries

## Derived Live Truth

Use these sources instead of manually updating live release facts here:

| Fact | Source |
| --- | --- |
| Latest public prerelease | `gh release view`, GitHub Releases API, or `dev/orin_release_body_validation.py` |
| Latest tag / tag commit | `git ls-remote --tags origin` or local tag lookup after fetch |
| Release candidate anchor | fetched `origin/main` unless USER explicitly selects a different target |
| Release window PR inventory | GitHub PR search / compare range helper output |
| PR state / merge commit / review state | `gh pr view` or GitHub GraphQL |
| Worktree branch freshness | `git status`, `git merge-base`, and `dev/orin_worktree_rebaseline_audit.py` |

Historical receipts may cite releases, PRs, and commits when the receipt is intentionally preserved as interpretation. Do not promote those receipts into live current-state ownership.

## Stage Breakpoint Schedule

The roadmap is a release-stage outline. It should be referenced often and edited rarely. Edits should change only the stage-breakpoint model, milestone criteria, or broad feature-family checkpoint order.

Package/slice release blockers remain named `Single-Slice Package User Approval Missing` and `Package Completion Unproven`. Only `Admission State: Admitted` rows in the owning workstream, branch plan, family dossier, or branch receipt count as admitted release/package slices; this roadmap points to those owners instead of duplicating their detailed ledgers.

| Release Stage | Public Meaning | Breakpoint / Gate Posture |
| --- | --- | --- |
| Pre-Beta snapshots | public iterative proof of working systems | continue until core desktop, monitoring/HUD, local AI readiness, packaging/install, and safety/privacy checkpoints have enough validated evidence for Beta planning |
| Beta readiness | broader public stabilization milestone | requires USER-approved Beta criteria, stable package boundaries, validation confidence, user-facing readiness proof, and no unresolved governance/source-truth blockers |
| Release readiness | public release milestone | requires separate USER-approved release criteria, installer/package posture, support posture, privacy/safety posture, and durable rollback/traceability evidence |
| Patch prerelease | bugfix, readiness, source-truth, validation, or narrow user-facing improvements inside the current stage | default when the public surface is incremental |
| Minor prerelease | broader user-facing package milestone inside the current stage | requires Release Readiness scope proof and USER approval |

## Public Milestone Pointers

Cross-family AI-native runtime/trust architecture, including permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, capability-pack architecture, routine/continuity boundaries, Windows Health recommendation boundaries, and competitive-integrity policy, routes through `Docs/ai_runtime_and_trust_architecture.md`. Those concepts do not create new milestone families by themselves; implementation still requires future Branch Readiness classification and USER approval.

| Family | Public Milestone Posture | Family Vision Owner | Detail Owner |
| --- | --- | --- | --- |
| `FAM-001` Boot Interface | released baseline; future lifecycle follow-through remains open | `Docs/family_visions/FAM-001_boot_interface.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` |
| `FAM-002` Desktop Interface | released UI/UX planning baseline; future UI package remains open | `Docs/family_visions/FAM-002_desktop_interface.md` | `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md` |
| `FAM-003` Interaction and Actions | released shared-action/tray evidence; future interaction package remains open | `Docs/family_visions/FAM-003_interaction_and_actions.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` |
| `FAM-004` Voice and Audio | released voice/audio direction and diagnostics evidence; future voice package remains open | `Docs/family_visions/FAM-004_voice_and_audio.md` | `Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md` |
| `FAM-005` External Integrations | architecture/planning evidence exists; implementation remains future | `Docs/family_visions/FAM-005_external_integrations.md` | `Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md` |
| `FAM-006` Monitoring and HUD | durable planning and release receipts preserved; future recording runtime remains USER-gated | `Docs/family_visions/FAM-006_monitoring_and_hud.md` | `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md` |
| `FAM-007` Local AI and Capability Packs | local AI readiness history preserved; future private Dev/Owner, backup/recovery, provider/model execution, and release work remain USER-gated | `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` | `Docs/branch_records/feature_fam_007_ai_edition_dev_owner_skeleton_readiness_foundation.md` |
| `FAM-008` Packaging and Install Experience | future install/package milestone | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` |

## Selected Next Workstream

Selected Next Workstream: FAM-007 Local AI and Capability Packs - Breakpoint 2 private Dev/Owner skeleton setup decision.
Record State: Registry-only
Minimal Scope: FAM-007 runtime action-gate planning slice for private Dev/Owner skeleton setup decision, private remote safety, and public/private boundary handoff, with provider/model/runtime/cache/memory execution still USER-gated.
Selected Next Implementation Branch: Deferred to Branch Readiness
Branch: Deferred to Branch Readiness
Branch Creation Status: No branch created
Selection Truth Status: USER-approved PR Readiness Stage 1 selected-next sync for the existing FAM-007 family; this is a pre-plan only and not approval to create private repos, configure private remotes, implement backup/import behavior, execute providers/models, enable runtime cache behavior, enable memory, create a PR, merge, release, or run v1.8.0.
Release-Debt Handling Status: No release debt introduced by selecting this next candidate; current branch remains the release-bearing public-safe readiness proof until separate PR/merge/release approvals.

## Folded Non-Family Concept Pointers

Workspace/data and safety/privacy are not roadmap milestone families or independent backlog worktrees after the AI-native taxonomy repair. Existing backlog families consume those constraints inside their own Branch Readiness and family visions.

| Concept Area | Consumed By |
| --- | --- |
| Workspace/data roots, evidence paths, cache storage, support bundles, cleanup, backup/export, and local file hygiene | Existing FAM visions and `Docs/ai_runtime_and_trust_architecture.md` where the implementing family touches those surfaces |
| Safety/privacy, consent, provider-visible data, secrets, Local-Only, Privacy Lockdown, Trust Journal, and sensitive capabilities | Existing FAM visions and `Docs/ai_runtime_and_trust_architecture.md` where the implementing family touches those surfaces |

## Operational Selection Routing

Selected-next, branch-creation, live release-window, live PR, and current worktree assignment truth are not owned by this roadmap. Use Git/GitHub/helpers and `C:\Nexus Governance State` for operational selection state, then route any future implementation carrier through Branch Readiness. Durable family direction remains in the family vision and canonical detail owner.

## Release Readiness Contract

Release Readiness is file-frozen. It must derive live candidate truth from Git/GitHub/helpers and report blockers without mutating docs.

Release packets should include:

- `Release Candidate Anchor:`
- `Release Candidate Anchor Source:`
- `Target Commit:`
- `Historical Endpoint Handling:`
- `Candidate Includes Later Governance Repairs:`
- `Release Ownership Model:`
- `Release Window Contributors:`
- `Merged-Unreleased Scope Inventory:`
- `Last Runtime PR:`
- `Post-Runtime Governance Repairs:`
- `FAM Contributor Routing:`

If Release Readiness finds source-truth drift, the digest must route the repair to the legal carrier named by current governance. It must not make this roadmap a live release-state ledger.

## Historical Receipt Routing

Use GitHub Releases for the authoritative public release list and body text.

Use these repo surfaces for durable internal interpretation:

- `Docs/closeouts/` for release and closeout summaries when present.
- `Docs/branch_records/` for compact branch authority receipts.
- `Docs/branch_plans/` for active branch runtime engineering plans and PR fold-down decisions.
- `Docs/workstreams/` for durable package/slice/proof history and family dossiers.
- `Docs/feature_backlog.md` for compact family identity and pointer routing.

## Current Schedule Reading

The roadmap's current reading is intentionally compact: pre-Beta remains active until the milestone checkpoints above are satisfied. Release execution remains USER-gated, active runtime branch identity is derived from Git/GitHub/helpers plus the approved operational-state layer, and latest release/tag truth is derived live.

No release, tag, GitHub Release, artifact upload, issue closeout, branch cleanup, worktree cleanup, runtime implementation, provider/model execution, downloads, memory/indexing, voice/Core sync, shortcut/installer work, AI Product Contract import, or Private Dev ORIN import is authorized by this roadmap.
