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

After FAM-007 PR #138 merged and Release Readiness Stage 1 exposed stale post-merge source-truth wording, USER also admitted this held carrier for bounded repo-wide PR Readiness governance and validator repair so future PRs prove post-merge source truth before merge. This is governance repair only, not FAM-007 runtime work.

This branch does not admit runtime provider implementation, LibreHardwareMonitor bundling, LibreHardwareMonitor installation, hardware polling expansion, Dashboard/Overlay runtime edits, FAM-006 worktree mutation, FAM-007 runtime/worktree mutation, AI Product Contract import, GitHub issue closeout, PR merge, release/tag/artifact work, or third-party evidence upload.

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
- Release Readiness Health Pass Governance: `Admitted - USER directed this held carrier to add a pre-merge PR Readiness health pass after FAM-007 PR #138 post-merge stale source-truth findings`
- PR Readiness Stage 2: `Denied by USER - hold this branch out of PR creation while FAM-007 proceeds toward PR/merge`
- PR / Release Work: `Blocked pending later explicit USER approval after FAM-007 reconciliation`

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
- `PR Readiness Stage 2 Denied`: `Active - USER denied PR Readiness Phase 2 and directed this branch to hold until FAM-007 PR/merge reconciliation`
- `FAM-007 PR/Merge Reconciliation Hold`: `Active - keep this branch available to reconcile conflicts or source-truth issues that may surface from FAM-007 before any PR creation`
- `Release Execution Approval Missing`: `Active`
- `FAM-007 Runtime / Worktree Mutation Approval Missing`: `Active`
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

Active seam: `Release Readiness Health Pass Governance Repair`

The active seam is the Branch Readiness Stage 2 docs/governance and validator repair that adds a PR Readiness pre-merge Release Readiness Health Pass without reopening runtime implementation, PR creation, release execution, or FAM-007 worktree mutation.

## Release Readiness Health Pass Governance Repair

- Admission Basis: `USER directed this held governance carrier to repair PR Readiness governance after FAM-007 PR #138 merged cleanly but Release Readiness Stage 1 found stale post-merge source-truth wording`
- Scope Classification: `Governance/validator only - no main repair, release execution, runtime/provider/model/memory/voice/Core/shortcut/installer implementation, AI Product Contract import, private Dev ORIN import, GitHub issue creation, or FAM-007 worktree mutation`
- Required Rule: `PR Readiness must prove post-merge source truth before PR creation or merge readiness`
- Validator Target: `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`
- Health-Pass Required Markers: `Post-Merge Branch Authority Projection:`, `Stale Active Branch Wording Scan:`, `Stale PR Creation / PR Readiness Pending Wording Scan:`, `Merged-Unreleased Scope Posture:`, `Release Execution Gate:`, `Watcher / Live PR State Projection:`, `Branch Cleanup Plan:`, `FAM Overlap Routing:`, `Projected Post-Merge Validation:`
- Release Execution Boundary: `PASS - tag, GitHub Release, artifact, release-note mutation, and release publication work remain separately gated`
- FAM Overlap Routing: `PASS - FAM-007 incident informs repo-wide PR governance only; any FAM-specific runtime or source-truth ownership remains routed to the owning lane`
- PR Readiness Hold Impact: `No PR creation or PR Readiness Stage 2 execution is admitted by this repair`

## Hardening H1 Record

- Phase Admission: `PASS - USER requested hardening and validation pressure-test after Branch Readiness Stage 2 source-truth commit`
- Active Seam: `Hardening H1 - Sensor HUD Provider Governance Source-Truth Pressure Test`
- Scope Classification: `Docs/governance only - no runtime, provider, installer, shortcut, Dashboard, Overlay, FAM-006 worktree, FAM-007 worktree, issue, PR, release, or third-party artifact mutation`
- Changed-File Scope: `PASS - branch delta remains limited to Docs source-truth files`
- Runtime Boundary: `PASS - no desktop, dev, nexus_visual, launcher, provider, or main runtime implementation files changed`
- Optional Libre Boundary: `PASS - source truth now records LibreHardwareMonitor as optional and no longer describes Libre as the primary required backend`
- No-Advanced-Provider Boundary: `PASS - source truth requires usable baseline/no-advanced-provider behavior with explicit setup-required/provider-required/unavailable states and no fake telemetry`
- Provider Choice Boundary: `PASS - user-pinned provider choice is authoritative, and LibreHardwareMonitor must not silently override HWiNFO64, vendor/local, or other admitted providers`
- Update Boundary: `PASS - LibreHardwareMonitor update monitoring is future scope, user-consented, source-verified, integrity-aware, non-silent, deferrable, disable-capable, rollback-aware where practical, and privacy-described`
- License Boundary: `PASS - MPL 2.0, upstream third-party notices, version/source metadata, and source-availability requirements are recorded before bundling or redistributing LibreHardwareMonitor`
- Wording Hardening: `PASS - third-party monitoring app UI scraping wording was tightened to avoid scanner-hostile admitted-scope wording while preserving the intended exclusion`
- FAM-006 Worktree Isolation: `PASS - C:\Nexus Worktrees\FAM-006 remains outside this branch's write target`

## Validation V1 Record

- `git diff --check origin/main...HEAD`: `PASS`
- `python dev\orin_branch_governance_validation.py`: `PASS - branch governance validation passed 4594 checks`
- `python dev\orin_release_body_validation.py`: `PASS - latest release body matches the standard; historical prior-release body drift was reported as historical only`
- `python -m compileall -q dev desktop Audio main.py`: `PASS`
- Changed-file scope scan: `PASS - changed files are docs-only`
- Runtime/dev/visual scope scan: `PASS - no runtime/dev/visual implementation files changed`
- Provider wording scan: `PASS after H1 wording hardening - prohibited mandatory-Libre/provider wording absent`
- User Test Summary Applicability: `Not applicable - source-truth/governance only, no user-facing runtime behavior changed`

## Validation V2 Record

- Scope: `Release Readiness Health Pass governance/validator repair`
- `git diff --check origin/main...HEAD`: `PASS`
- `python dev\orin_branch_governance_validation.py`: `PASS - branch governance validation passed 4668 checks`
- `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`: `PASS - branch governance validation passed 4669 checks; gate is not applicable outside PR Readiness on this held Branch Readiness carrier`
- `python dev\orin_release_body_validation.py`: `PASS - latest release body matches the standard; historical prior-release body drift was reported as historical only`
- `python -m compileall -q dev desktop Audio main.py`: `PASS`
- Runtime Boundary: `PASS - no runtime/provider/model/memory/voice/Core/shortcut/installer implementation files changed`
- Release Boundary: `PASS - no tag, GitHub Release, artifact, release-note, or release publication work performed`

## PR Readiness Status

- PR Readiness Status: `Hold - PR Readiness Stage 2 / PR creation denied by USER after hardening and validation`
- PR Creation Approval: `Denied - no PR should be created while this hold is active`
- Hold Basis: `USER directed this branch to wait for FAM-007 PR/merge so any conflicts or source-truth issues from this provider-governance branch can be reconciled afterward`
- Current Blocker: `PR Readiness Stage 2 Denied; FAM-007 PR/Merge Reconciliation Hold`
- PR Readiness Stage 2 Expected Scope: `project merge-stable historical/no-active branch authority, add required Governance Drift Audit / Post-Merge State truth if needed, rerun validation, commit/push any PR-readiness source-truth sync, create the PR only after explicit USER approval, and stop before merge`
- Merge Approval: `Not granted`
- Release Approval: `Not granted`

## Rollback Target

- `Branch Readiness`

Rollback Path: abandon branch `feature/fam-006-sensor-hud-provider-governance`; do not mutate `C:\Nexus Worktrees\FAM-006`, provider binaries, installer state, or direct `main`.

## Next Legal Phase

- `PR Readiness`

Next Legal Phase Gate: USER denied PR Readiness Stage 2 for now. This branch must hold until FAM-007 PR/merge reconciliation is complete or USER explicitly reopens PR Readiness Stage 2 / PR creation for this carrier. Runtime implementation, provider bundling, Libre update tooling, release work, issue closeout, FAM-007 work, and AI Product Contract import remain separate USER approval checkpoints.
