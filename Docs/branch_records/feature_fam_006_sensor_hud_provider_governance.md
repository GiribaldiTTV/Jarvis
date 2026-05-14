# Branch Authority Record: feature/fam-006-sensor-hud-provider-governance

## Branch Identity

- Branch: `feature/fam-006-sensor-hud-provider-governance`
- Workstream: `FAM-006 Sensor HUD Provider Governance`
- Branch Class: `repair/dev-tooling-governance`
- Backlog Record State: `Registry-only provider/source-truth extension under historical FAM-006 / PKG-006`
- Package ID: `None`
- Package Name: `None`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 carrier for bounded FAM-006 Sensor HUD provider governance.

It exists because FAM-006 Dashboard runtime work is already historical/released, the active FAM-006 worktree must not be dirtied for this planning cleanup, `main` is protected against direct Codex mutation, and the existing future Sensor HUD provider contract needs explicit optional-provider, no-Libre baseline, user-provider-choice, Libre update, and MPL / third-party notice requirements before any later provider implementation branch begins.

This branch does not admit runtime provider implementation, LibreHardwareMonitor bundling, LibreHardwareMonitor installation, hardware polling expansion, Dashboard/Overlay runtime edits, FAM-006 worktree mutation, FAM-007 work, AI Product Contract import, GitHub issue closeout, PR merge, release/tag/artifact work, or third-party evidence upload.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Stage 1: `Complete - analysis-only pass confirmed C:\Nexus Desktop AI was clean on main at origin/main and USER wanted this governance/source-truth work routed there instead of the active FAM-006 worktree`
- Stage 2 USER Approval: `Granted - USER approved a waiver for this governance/source-truth carrier on the normal NDAI worktree`
- Branch Creation: `Created at C:\Nexus Desktop AI from main/origin-main commit 6f9a13d17a65a3385001b8e463113295f5463b01`
- Active Branch: `feature/fam-006-sensor-hud-provider-governance`
- Branch Authority Marker: `Active Branch`
- Branch Authority State: `Active for this Branch Readiness carrier until PR Readiness projects merge-stable historical/no-active truth`
- Runtime Implementation: `Blocked`
- FAM-006 Worktree Mutation: `Blocked`
- Provider Install / Bundle: `Blocked`
- PR / Release Work: `Blocked pending later explicit USER approval`

## Branch Class

- `repair/dev-tooling-governance`

Waiver Basis: USER explicitly approved conducting Branch Readiness for a governance/source-truth repair branch on the normal `C:\Nexus Desktop AI` worktree and explicitly did not want this work to dirty the active FAM-006 worktree.

## Blockers

- `Runtime Implementation Approval Missing`: `Active`
- `Provider Bundling Approval Missing`: `Active`
- `Provider Install Approval Missing`: `Active`
- `FAM-006 Worktree Mutation Blocked`: `Active`
- `GitHub Issue Closeout Approval Missing`: `Active`
- `PR Creation Approval Missing`: `Active`
- `Release Execution Approval Missing`: `Active`
- `FAM-007 Admission Missing`: `Active`
- `AI Product Contract Import Approval Missing`: `Active`

## Entry Basis

- Normal worktree preflight confirmed repository root `C:\Nexus Desktop AI`.
- Current branch before creation was `main`.
- `HEAD` and `origin/main` both resolved to `6f9a13d17a65a3385001b8e463113295f5463b01`.
- `git status --short --branch` reported `## main...origin/main`.
- Existing worktrees were isolated as `C:\Nexus Worktrees\FAM-006` and `C:\Nexus Worktrees\FAM-007`; neither is the write target for this carrier.

## Source-Truth Placement Preflight

- Existing Provider Contract Owner: `Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md` owns the future Sensor HUD beta provider admission contract.
- Existing Family Registry Owner: `Docs/feature_backlog.md` owns FAM-006 family scope, pending gaps, and deferred-provider posture.
- Existing Branch Index Owner: `Docs/branch_records/index.md` owns active branch authority routing.
- Placement Decision: extend FB-040 and the FAM-006 backlog row; create this branch authority record only because the active branch itself needs execution authority while it exists.
- New Artifact Avoidance: no standalone provider specification, issue tracker, third-party notices file, installer manifest, runtime helper, or validation helper is created in this pass.
- Duplication Check: this branch does not duplicate the FAM-006 product-surface historical record; it narrows future provider governance only.
- Validator Posture: docs/governance validation is sufficient for this source-truth pass; no runtime validator is required because no runtime provider code is admitted.

## Provider Governance Requirements

- LibreHardwareMonitor must remain optional, not a mandatory runtime dependency.
- The future Sensor HUD / Overlay path must remain usable without LibreHardwareMonitor or any third-party monitoring app.
- No-provider or baseline-provider mode may show built-in/native/operating-system metrics where admitted and must show explicit unavailable, setup-required, partial, stale, or provider-required states for metrics that need advanced providers.
- Advanced CPU thermal, GPU load, GPU thermal, fan, voltage, clock, and board sensor parity remain provider-backed future scope unless a later branch admits and validates a safe native route.
- Users must be able to choose the active provider family where multiple supported sources exist.
- A user-pinned provider choice must not be silently replaced by LibreHardwareMonitor or any other default provider.
- Supported third-party integrations must be explicit, local, read-only, health-reported, and source-labeled; scraping third-party app UI is not admitted.
- Provider merge/dedup behavior must preserve provenance so the user can understand which source owns each value.

## LibreHardwareMonitor Boundary

- LibreHardwareMonitor is an optional advanced local sensor bridge candidate for broad hardware sensor coverage.
- LibreHardwareMonitor may later be supported as a bundled library, a separately detected local provider, or a user-installed integration only if a later branch admits the exact distribution model.
- LibreHardwareMonitor absence, disablement, failure, slowness, or incompatibility must degrade cleanly to baseline/unavailable provider states instead of breaking Dashboard, HUD, Overlay, or layout controls.
- If LibreHardwareMonitor is present but the user selects another supported provider, the selected provider remains authoritative unless the user changes it.

## Update Management Requirements

- LibreHardwareMonitor update monitoring is future scope and must be opt-in or clearly user-consented before network checks occur.
- Update checks must verify the source, version, compatibility, and integrity metadata before presenting an update.
- Updates must be user-approved, not silent.
- The UI must allow users to defer, disable, or roll back a LibreHardwareMonitor bridge/update path where practical.
- Update checks must not become telemetry uploads; user-facing privacy copy must state what is checked and where.
- Update management must distinguish bundled bridge updates from detected external-app updates and user-installed provider updates.

## License / Legal Requirements

- LibreHardwareMonitor is licensed under MPL 2.0 and includes additional third-party license material upstream.
- Commercial use does not require sharing profits or income, but distribution of MPL-covered executable or library material requires recipients to be told how to obtain the MPL-covered source code.
- If Nexus modifies MPL-covered LibreHardwareMonitor source files, those modified MPL-covered files must be made available under MPL 2.0.
- Proprietary Nexus/NDAI files may remain separate when they do not contain MPL-covered source code.
- Any future bundle must include MPL 2.0 license text, third-party notices required by LibreHardwareMonitor, upstream version/source metadata, and a source-availability path for MPL-covered files.
- This record is a planning/legal-compliance summary, not legal advice; release packaging should get a dedicated license review before distributing LibreHardwareMonitor or any provider bridge.

## Exit Criteria

- FB-040 future Sensor HUD provider contract records LibreHardwareMonitor as optional and user-selectable, not mandatory.
- FB-040 records no-provider/baseline usability, provider choice, update-management, and license/notice requirements.
- FAM-006 backlog pending gaps record optional Libre/provider-governance posture without reopening runtime implementation.
- Active branch authority is recorded in `Docs/branch_records/index.md`.
- No runtime, installer, shortcut, provider, FAM-006 worktree, FAM-007, release, or GitHub issue state is changed.
- Docs/governance validation and diff checks pass.

## Branch Objective

Record durable FAM-006 Sensor HUD provider governance so future provider implementation starts from a clear optional-Libre, no-advanced-provider baseline, user-provider-choice, update-management, and license/notice contract instead of reopening provider architecture from conversation memory.

## Target End-State

- FB-040 future Sensor HUD provider truth says LibreHardwareMonitor is optional, not required.
- Baseline/no-advanced-provider behavior remains usable and truthful.
- User provider selection and provider provenance are explicit future acceptance requirements.
- LibreHardwareMonitor update monitoring is consented, non-silent, source-verified, and rollback/disable-aware future scope.
- MPL 2.0, third-party notices, version/source metadata, and source-availability duties are recorded before any LibreHardwareMonitor bundle or redistribution is admitted.
- FAM-006 and FAM-007 runtime worktrees remain untouched.

## Backlog Completion Strategy

This carrier does not admit or complete a new runtime backlog package. It records a bounded source-truth/governance repair under historical FAM-006 provider planning and leaves runtime provider implementation, provider bundling, installer work, update tooling, release work, GitHub issue closeout, and PR creation blocked pending later USER approval.

Branch Completion Goal: Branch Readiness Stage 2 records the source-truth contract, validates, and stops for USER review before any PR Readiness / PR creation step.
Known Future-Dependent Blockers: runtime implementation, provider install/bundle, Libre update tooling, license packaging review, third-party notices file creation, PR creation, release work, FAM-006 worktree mutation, FAM-007 work, and GitHub issue closeout require later explicit USER approval.
Branch Closure Rule: stop after validated source-truth repair unless USER separately approves PR Readiness.

## Expected Seam Families And Risk Classes

- Branch Readiness Stage 2 source-truth repair.
- Optional provider and no-advanced-provider baseline governance.
- LibreHardwareMonitor license/update/source-availability governance.
- Provider precedence, user override, and provenance governance.

Risk Classes: accidental mandatory-Libre wording, accidental runtime provider admission, user-provider-choice regression, no-provider usability ambiguity, license/source-availability omission, silent-update risk, third-party UI scraping drift, FAM-006 worktree contamination, and FAM-007 boundary bleed.

## User Test Summary Strategy

No User Test Summary is generated, refreshed, imported, or mutated by this carrier. The change is source-truth/governance only. Any later user-visible provider implementation must define its own screenshot/live/User Test Summary proof path or receive an explicit USER waiver.

## Later-Phase Expectations

- Workstream: `Blocked - no runtime/provider implementation is admitted by this carrier`
- Hardening: `Not applicable unless a later phase admits runtime/provider implementation or a governance hardening pass`
- Live Validation: `Not applicable for this source-truth-only repair`
- PR Readiness: `Allowed only after separate USER approval; must project this active branch record into historical/no-active merge-target truth before PR green`
- Release Readiness: `Blocked unless a later USER-approved release package includes this source-truth repair`

## Initial Workstream Seam Sequence

Seam 1: `Provider Governance Source-Truth Repair`
Goal: `Record optional LibreHardwareMonitor, no-advanced-provider usability, provider choice, update-management, and license/notice requirements in existing FAM-006 / FB-040 source truth.`
Scope: `Docs/branch_records/index.md`; `Docs/branch_records/feature_fam_006_sensor_hud_provider_governance.md`; `Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md`; `Docs/feature_backlog.md`.
Non-Includes: `runtime code, provider install, Libre bundle, installer work, shortcut work, FAM-006 worktree mutation, FAM-007 work, issue closeout, release work, PR creation`.
Validation: `git diff --check`; `python dev\orin_branch_governance_validation.py`; targeted source-truth search.

## Active Seam

Active seam: `Provider Governance Source-Truth Repair`

The active seam is the Branch Readiness Stage 2 docs/governance repair that updates existing source-truth owners for optional provider behavior, no-Libre baseline usability, provider choice, update governance, and MPL / third-party notice requirements.

## Rollback Target

- `Branch Readiness`

Rollback Path: abandon branch `feature/fam-006-sensor-hud-provider-governance`; do not mutate `C:\Nexus Worktrees\FAM-006`, provider binaries, installer state, or direct `main`.

## Next Legal Phase

- `PR Readiness`

Next Legal Phase Gate: after validation, USER must separately approve PR Readiness / PR creation if this source-truth carrier should be pushed and opened as a PR. Runtime implementation, provider bundling, Libre update tooling, release work, issue closeout, FAM-007 work, and AI Product Contract import remain separate USER approval checkpoints.
