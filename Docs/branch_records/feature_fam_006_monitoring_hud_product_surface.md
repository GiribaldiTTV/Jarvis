# Branch Authority Record: feature/fam-006-monitoring-hud-product-surface

## Branch Identity

- Branch: `feature/fam-006-monitoring-hud-product-surface`
- Workstream: `FAM-006 Monitoring and HUD Product Surface Package`
- Branch Class: `implementation`
- Branch Class Note: `runtime package`
- Backlog Record State: `Registry-only`
- Package ID: `PKG-006`
- Package Name: `Monitoring and HUD Product Surface Package`

## Purpose / Why It Exists

This branch is the USER-approved runtime package carrier for FAM-006 Monitoring and HUD.

It exists because `v1.6.13-prebeta` release execution and post-release canon closure are complete, release debt is clear, merged `main` validated as `No Active Branch`, USER-approved selected-next truth identified FAM-006 Monitoring and HUD as the next runtime direction, and Branch Readiness Stage 2 admitted the concrete multi-slice `PKG-006` runtime package.

This branch may execute the admitted PKG-006 implementation slices during Workstream. It must not create a PR, provision a watcher, create a tag, draft or publish a GitHub Release, create release artifacts, execute release work, mutate `main` directly, grant a single-slice waiver, create a new FAM/package beyond FAM-006, or admit optional voice/audio widening beyond narrow HUD-status presentation without later explicit USER approval.

## Record State

- `Registry-only`

## Status

- `Workstream Active`

## Canonical Branch

- `feature/fam-006-monitoring-hud-product-surface`

## Current Phase

- Phase: `Workstream`

## Phase Status

- Workstream Stage: `WS4 - Settings And User Controls Visibility`
- Active Branch: `feature/fam-006-monitoring-hud-product-surface`
- Branch Authority Mode: `Active Branch`
- Workstream Entry Source-Truth Transition: `Performed - Branch Readiness Stage 2 terminal evidence reconciled before runtime implementation`
- Branch Creation: `Created from updated main at 3c68cd881a9f6bf447f09ac0949d556e97bce4f4`
- Branch Admission Commit: `8ae84cb784fc07dfe4f445359de4cf20a13552fa`
- Branch Rename State: `Renamed to feature/fam-006-monitoring-hud-product-surface after USER direction to avoid codex-prefixed active branch names; old origin codex-prefixed branch deleted after feature branch push`
- Branch Authority State: `Active branch authority`
- Selected Next Source: `USER-approved selected-next truth matured into active FAM-006 Workstream`
- Package Admission State: `Admitted`
- Admitted Slice Count: `6`
- Package Completion State: `In Progress`
- Single-Slice Package User Approval: `Not required - PKG-006 has six concrete admitted slices; no waiver granted`
- Runtime Implementation State: `Started - SLC-016 visual baseline, SLC-025 telemetry boundary, and SLC-026 placement ownership complete; SLC-027 active`
- PR Creation State: `Not approved in Workstream`
- Watcher Provisioning State: `Not approved in Workstream`
- Release Work State: `Not approved; v1.6.13-prebeta release execution is already complete and no new release work is in scope`
- Optional Voice/Status Integration: `Deferred unless later proven to be narrow HUD-status copy inside FAM-006`
- Element Coverage State: `Coverage-only; not counted as admitted slices`

## Branch Class

- `implementation`

## Blockers

- `Backlog Completion Unproven`

The blocker above is active because PKG-006 still has admitted implementable slices remaining. It does not stop Workstream continuation while the governed continuation state remains In Progress.

## Cleared Governance Notes

- Branch Readiness Execution User Approval Missing is cleared for the completed Branch Readiness Stage 2 package-admission pass.
- Single-Slice Package User Approval Missing is not active because PKG-006 has six admitted slices and no single-slice waiver is granted.
- Package Completion Unproven prevents package closeout, Hardening admission, and PR readiness while admitted PKG-006 slices remain incomplete.
- Backlog Addition User Approval Missing remains active for any new FAM/package, backlog split, family promotion beyond this branch authority, runtime branch outside this carrier, or single-slice waiver.

## Entry Basis

- Updated `main` was clean and matched `origin/main` at `3c68cd881a9f6bf447f09ac0949d556e97bce4f4` when the branch was created.
- `feature/fam-006-monitoring-hud-product-surface` did not exist locally or remotely before Branch Readiness Stage 2 creation.
- `v1.6.13-prebeta` is the latest public prerelease and release debt is clear.
- `Docs/branch_records/index.md` reported `No Active Branch` before Branch Readiness Stage 2.
- USER approval cleared Branch Readiness Stage 2 execution for this branch, package admission, source-truth sync, validation, commit, and push.
- Branch Readiness Stage 2 committed and pushed `8ae84cb784fc07dfe4f445359de4cf20a13552fa`, admitting PKG-006 and stopping before runtime implementation.
- USER later directed the active branch name to use `feature/` instead of `codex/`; this branch authority record and the active backlog/roadmap/workstream surfaces were renamed to match, while historical codex-prefixed branch records remain historical traceability only.

## Exit Criteria

- Every admitted PKG-006 implementation slice is truthfully complete or legally deferred/split by explicit USER approval.
- `Package Completion State` is not marked complete while admitted slices remain incomplete.
- Optional voice/audio widening remains deferred unless later USER approval expands scope.
- Element Coverage remains a non-identity checklist only.
- The branch reaches Hardening only after Workstream completion is truthfully green.
- PR, watcher, release, tag, GitHub Release, artifact, and direct-main actions remain outside Workstream.

## Stage 2 Terminal Evidence Reconciliation

Finding: `Workstream entry source-truth transition performed`.

The operator-supplied Stage 2 terminal evidence was not sufficient by itself because this branch authority record still listed Branch Readiness Stage 2 as the active phase and seam. This Workstream-entry pass transitioned the active record to Workstream before implementing WS1 so repo source truth, branch authority truth, and runtime edits agree.

## Rollback Target

- `Workstream`

Rollback Path: revert the current Workstream commit on `feature/fam-006-monitoring-hud-product-surface` before PR merge; no tags, releases, artifacts, PR, watcher, or `main` mutation are created by this WS1 pass.

## Next Legal Phase

- `Workstream`

Next Legal Seam: `Workstream WS4 - Settings And User Controls Visibility`

Next Legal Phase Gate: Workstream remains active until every admitted PKG-006 implementation slice is complete, blocked by a named blocker, deferred by valid future dependency, or split by explicit USER approval. Hardening is blocked while admitted implementable slices remain incomplete.

## Branch Objective

Turn the historical FAM-006 monitoring/thermal architecture baseline into a visible, trustworthy user-facing Monitoring/HUD product surface, connecting telemetry/status truth to desktop presentation, user controls, fail-safe/no-data behavior, and later live validation proof without collapsing the package into a single HUD toggle or one-seam proof.

## Target End-State

- PKG-006 completes all admitted implementation slices on this branch.
- The user-facing HUD surface is visible and trustworthy.
- Runtime telemetry adapters, desktop placement/renderer ownership, settings controls, fail-safe states, and live desktop proof are each completed as their own admitted slices.
- Optional voice/audio widening remains deferred unless later USER approval expands scope.
- PR, watcher, release, tag, GitHub Release, artifact, and direct-main actions remain outside Workstream.

## Backlog Completion Status

Backlog Completion State: `In Progress`
Remaining Implementable Work: `SLC-027 settings/user controls, SLC-028 fail-safe/no-data/degraded states, and SLC-029 validation/live desktop proof remain implementable on this branch.`
Future-Dependent Blockers: `SLC-030 optional voice/spoken status integration is deferred and requires later USER widening approval if spoken/audio behavior, voice integration, persona voice, FAM-004, or cross-family behavior is needed.`
Completion Status: `In Progress`

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing, backend/runtime`
Docs-Only Workstream: `No`
Planning-Loop Bypass User Approval: `None`
Planning-Loop Bypass Reason: `None`

- PKG-006 is a runtime-focused implementation branch. Workstream must produce runtime/user-facing implementation and validation evidence, not a docs-only loop.

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`
Single-Seam Workstream Waiver: `None`
Bounded Seam Default: `One active seam at a time; not one-seam Workstream authority`

- The admitted package has six concrete slices and is not a one-slice branch.
- Workstream must continue to the next admitted slice whenever scope, phase, risk, and validation authority remain green.
- Stopping after one seam or one admitted slice while PKG-006 remains incomplete requires a named blocker, future dependency, or explicit USER-approved backlog split/waiver.

## Admitted Implementation Slice

Primary Entry Slice: `SLC-016 HUD visual and user-facing monitoring surface`

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-016` | `PKG-006` | `FAM-006` | HUD visual and user-facing monitoring surface | Admitted | Green | Complete | `BR-S2-S1`; `WS1`; `dev/orin_monitoring_hud_surface_validation.py` |
| `SLC-025` | `PKG-006` | `FAM-006` | Runtime telemetry source and adapter boundary | Admitted | Green | Complete | `BR-S2-S2`; `WS2`; `desktop/monitoring_hud_telemetry.py`; `dev/orin_monitoring_hud_surface_validation.py` |
| `SLC-026` | `PKG-006` | `FAM-006` | Desktop placement and renderer ownership | Admitted | Green | Complete | `BR-S2-S3`; `WS3`; `desktop/monitoring_hud_placement.py`; `dev/orin_monitoring_hud_surface_validation.py` |
| `SLC-027` | `PKG-006` | `FAM-006` | Settings and user controls visibility | Admitted | Workstream active | In Progress | `BR-S2-S4`; `WS4` |
| `SLC-028` | `PKG-006` | `FAM-006` | Fail-safe, no-data, and degraded-status behavior | Admitted | Pending Workstream | In Progress | `BR-S2-S5`; planned `WS5` |
| `SLC-029` | `PKG-006` | `FAM-006` | Validation and live desktop proof | Admitted | Pending Workstream | In Progress | `BR-S2-S6`; planned `WS6` |

## Deferred / Future Slice Ledger

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-030` | `PKG-006` | `FAM-006` | Optional voice or spoken status integration | Deferred Placeholder | Deferred pending cross-family approval | Not Admitted | Future USER widening decision required if voice/audio behavior is needed |

Optional voice/status integration is not admitted because spoken output, audio notification behavior, voice-driven HUD interaction, persona voice, or cross-family FAM-004 behavior would widen scope beyond the approved FAM-006 package. Narrow HUD-facing status copy may be evaluated later inside an admitted visual/status slice if it does not change voice/audio behavior.

## Element Coverage Review

- User-facing surface: `In Scope - HUD visual and user-facing monitoring surface`
- Runtime/backend behavior: `In Scope - telemetry source and adapter boundaries`
- Settings/configuration: `In Scope - settings or user controls visibility`
- Data/state/persistence: `In Scope - no persistence by default unless later Workstream explicitly admits durable state`
- Fail-safe/recovery: `In Scope - no-data, stale, partial, unavailable, degraded, and unsupported states`
- Security/privacy/permissions: `In Scope - local-only, non-invasive telemetry posture and truthful user-facing claims`
- Voice/audio: `Deferred coverage only - no spoken/audio behavior admitted`
- External integration: `Out of Scope - plugin-fed telemetry remains future unless later admitted`
- Local AI/capability packs: `Not Applicable - no local AI or heavy capability-pack work admitted`
- Packaging/install: `Not Applicable - no installer or pack selection work admitted`
- Monitoring/HUD: `In Scope - primary package surface`
- Validation: `In Scope - static validation plus later live desktop proof and User Test Summary`
- Release impact: `Pending Future Package - no release work approved in Workstream`

Element Coverage Admission Rule: `Element Coverage rows are non-identity checklist rows only and do not count as admitted slices, seams, packages, FAMs, selected-next truth, or release drivers.`

## Initial Workstream Seam Sequence

Seam 1: `WS1 - HUD Visual And User-Facing Surface Baseline`
Goal: create a visible, passive Monitoring/HUD surface baseline in the desktop visualization.
Scope: user-facing HUD presentation bounded by FAM-006 package authority; static boundary copy may name later slices without implementing them.
Non-Includes: telemetry collection/adapters, settings/control behavior, fail-safe/no-data logic, voice/audio behavior, plugin-fed telemetry, installer changes, release execution, PR creation, watcher provisioning, or package completion claims.
Status: `Green - SLC-016 complete with durable static helper proof`

Seam 2: `WS2 - Runtime Telemetry Source And Adapter Boundary`
Goal: define and implement the runtime telemetry adapter boundary after WS1 establishes the visible surface.
Scope: local, non-invasive telemetry source boundaries only.
Non-Includes: UI placement ownership, settings controls, fail-safe semantics, voice/audio behavior, release execution, PR creation, watcher provisioning, or package completion claims.
Status: `Green - SLC-025 complete with local runtime telemetry boundary proof`

Seam 3: `WS3 - Desktop Placement And Renderer Ownership`
Goal: clarify desktop placement and renderer ownership after the HUD has a visible surface and a local telemetry adapter boundary.
Scope: desktop placement and renderer ownership only.
Non-Includes: settings controls, fail-safe semantics, live validation proof, voice/audio behavior, release execution, PR creation, watcher provisioning, or package completion claims.
Status: `Green - SLC-026 complete with renderer-owned placement contract proof`

Seam 4: `WS4 - Settings And User Controls Visibility`
Goal: expose settings or user-control visibility for the Monitoring/HUD surface after renderer ownership is explicit.
Scope: settings and user controls visibility only.
Non-Includes: fail-safe semantics, live validation proof, voice/audio behavior, release execution, PR creation, watcher provisioning, or package completion claims.
Status: `Active - SLC-027 in progress`

## Active Seam

Active seam: `WS4 - Settings And User Controls Visibility`

Seam Status: `In Progress`
Slice Status: `In Progress`
Completion Status: `In Progress`
Waiver Status: `None`
Continue Decision: `Continue`
Stop Basis: `None`

## Seam Continuation Decision

Seam Status: `In Progress`
Slice Status: `In Progress`
Completion Status: `In Progress`
Waiver Status: `None`
Continue Decision: `Continue`
Stop Basis: `None`
Next Active Seam: `WS4 - Settings And User Controls Visibility`
Stop Condition: `None`
Continuation Action: `Continue SLC-027 by adding settings and user controls visibility without consuming fail-safe, validation, voice/audio, PR, watcher, release, tag, artifact, or direct-main work.`

## WS1 Implementation Record

- Workstream-entry transition: `Performed before runtime implementation`
- Runtime files touched: `desktop/desktop_renderer.py`, `jarvis_visual/orin_core.html`, `jarvis_visual/orin_core.css`, `jarvis_visual/orin_core.js`
- HUD baseline behavior: `DesktopRuntimeWindow enables desktop-mode visualization and emits MONITORING_HUD_BASELINE_READY with package PKG-006, slice SLC-016, baseline visual_only`
- HUD baseline surface: `Static, visible Monitoring HUD card hidden outside desktop mode and surfaced only when DesktopRuntimeWindow enables desktop surface mode`
- HUD baseline validation: `dev/orin_monitoring_hud_surface_validation.py proves the visible desktop-only surface, SLC/package markers, boundary copy for later slices, and no telemetry/settings/fail-safe/voice/audio widening`
- SLC-016 Completion State: `Green / Complete`
- Boundary preservation: `No telemetry adapters, settings controls, fail-safe/no-data logic, voice/audio behavior, plugin-fed telemetry, release work, PR work, watcher work, tags, GitHub Releases, artifacts, or direct-main mutation`

## WS2 Implementation Record

- Runtime files touched: `desktop/monitoring_hud_telemetry.py`, `desktop/desktop_renderer.py`, `jarvis_visual/orin_core.html`, `jarvis_visual/orin_core.css`, `jarvis_visual/orin_core.js`
- Telemetry boundary behavior: `DesktopRuntimeWindow publishes a HUD-ready local runtime readiness snapshot through desktop-runtime-boundary with package PKG-006 and slice SLC-025`
- Telemetry boundary sources: `visual page readiness, desktop surface enabled/pending state, runtime log route presence, and renderer event route presence`
- Telemetry boundary validation: `dev/orin_monitoring_hud_surface_validation.py proves the SLC-025 adapter markers, HUD consumer, runtime marker, no hardware/vendor polling, and no settings/fail-safe/voice/audio widening`
- SLC-025 Completion State: `Green / Complete`
- Boundary preservation: `No hardware sensor polling, vendor telemetry APIs, settings controls, fail-safe/no-data semantics, desktop placement ownership, live validation proof, voice/audio behavior, release work, PR work, watcher work, tags, GitHub Releases, artifacts, or direct-main mutation`

## WS3 Implementation Record

- Runtime files touched: `desktop/monitoring_hud_placement.py`, `desktop/desktop_renderer.py`, `jarvis_visual/orin_core.html`, `jarvis_visual/orin_core.css`, `jarvis_visual/orin_core.js`
- Placement ownership behavior: `DesktopRuntimeWindow publishes a HUD placement contract through desktop-renderer-top-right with package PKG-006 and slice SLC-026`
- Placement ownership surface: `Monitoring HUD shows renderer owner, desktop anchor, and non-interactive pointer model while keeping the HUD inside the desktop visual surface`
- Placement ownership validation: `dev/orin_monitoring_hud_surface_validation.py proves SLC-026 placement markers, renderer-owned placement publication, active SLC-026 surface copy, and no hardware polling, settings-control behavior, fail-safe semantics, or voice/audio widening`
- SLC-026 Completion State: `Green / Complete`
- Boundary preservation: `No settings controls, fail-safe/no-data semantics, live validation proof, voice/audio behavior, release work, PR work, watcher work, tags, GitHub Releases, artifacts, or direct-main mutation`

## Validation Plan

- `git status --short --branch`
- `python dev/orin_branch_governance_validation.py`
- `python dev/orin_monitoring_hud_surface_validation.py`
- `python -m compileall -q dev`
- `git diff --check`
- focused static HUD baseline validation for the desktop visualization markers
- `python dev/automation_observability_report.py`

Later Workstream validation must add focused runtime/HUD validation and live desktop proof after more implementation slices are ready.
