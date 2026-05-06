# Branch Authority Record: codex/fam-006-monitoring-hud-product-surface

## Branch Identity

- Branch: `codex/fam-006-monitoring-hud-product-surface`
- Workstream: `FAM-006 Monitoring and HUD Product Surface Package`
- Branch Class: `implementation`
- Branch Class Note: `runtime package`
- Backlog Record State: `Registry-only`
- Package ID: `PKG-006`
- Package Name: `Monitoring and HUD Product Surface Package`

## Purpose / Why It Exists

This branch is the USER-approved runtime package carrier for FAM-006 Monitoring and HUD.

It exists because `v1.6.13-prebeta` release execution and post-release canon closure are complete, release debt is clear, merged `main` validated as `No Active Branch`, and USER-approved selected-next truth identified FAM-006 Monitoring and HUD as the next runtime direction. Branch Readiness Stage 2 is approved to create this branch from updated `main`, admit the concrete multi-slice `PKG-006` runtime package, sync source truth, validate, commit, and push the Branch Readiness state.

This branch must not start runtime implementation during Branch Readiness Stage 2, create a PR, provision a watcher, create a tag, draft or publish a GitHub Release, create release artifacts, execute release work, mutate `main` directly, grant a single-slice waiver, create a new FAM/package beyond FAM-006, or admit optional voice/audio widening beyond narrow HUD-status presentation without later explicit USER approval.

## Record State

- `Registry-only`

## Status

- `Branch Readiness Active`

## Canonical Branch

- `codex/fam-006-monitoring-hud-product-surface`

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Branch Readiness Stage: `Stage 2 - Execution Gate`
- Active Branch: `codex/fam-006-monitoring-hud-product-surface`
- Branch Authority Mode: `Active Branch`
- Branch Readiness Stage 2 USER Approval: `Granted for FAM-006 branch creation, PKG-006 multi-slice package admission, source-truth sync, validation, commit, and push`
- Branch Creation: `Created from updated main at 3c68cd881a9f6bf447f09ac0949d556e97bce4f4`
- Branch Existence Check: `No local or remote branch existed before creation`
- Branch Authority State: `Active branch authority`
- Selected Next Source: `USER-approved selected-next truth matured into active FAM-006 Branch Readiness`
- Package Admission State: `Admitted`
- Admitted Slice Count: `6`
- Package Completion State: `In Progress`
- Single-Slice Package User Approval: `Not required - PKG-006 has six concrete admitted slices; no waiver granted`
- Runtime Implementation State: `Not started`
- PR Creation State: `Not approved in Branch Readiness`
- Watcher Provisioning State: `Not approved in Branch Readiness`
- Release Work State: `Not approved; v1.6.13-prebeta release execution is already complete and no new release work is in scope`
- Optional Voice/Status Integration: `Deferred unless later proven to be narrow HUD-status copy inside FAM-006`
- Element Coverage State: `Coverage-only; not counted as admitted slices`
- ChatGPT Loader / Source-Truth Sync State: `Evaluated during Stage 2 only as ChatGPT-facing continuity; Codex authority remains Docs/Main.md and owning canon`

## Branch Class

- `implementation`

## Blockers

None for Branch Readiness Stage 2 admission after this source-truth sync validates green.

Cleared / inactive blockers:

- `Branch Readiness Execution User Approval Missing`: `Cleared for this Stage 2 pass only`
- `Single-Slice Package User Approval Missing`: `Not active - six admitted slices`
- `Package Completion Unproven`: `Not active - package completion is not claimed complete`
- `Backlog Addition User Approval Missing`: `Cleared for FAM-006 branch creation and PKG-006 admission only; active for any new FAM/package, backlog split, family promotion beyond this branch authority, runtime branch outside this carrier, or single-slice waiver`

## Entry Basis

- Updated `main` was clean and matched `origin/main` at `3c68cd881a9f6bf447f09ac0949d556e97bce4f4`.
- `codex/fam-006-monitoring-hud-product-surface` did not exist locally or remotely before creation.
- `v1.6.13-prebeta` is the latest public prerelease and release debt is clear.
- `Docs/branch_records/index.md` reported `No Active Branch` before this Branch Readiness pass.
- `Docs/feature_backlog.md` and `Docs/prebeta_roadmap.md` recorded USER-approved FAM-006 selected-next truth, branch not created, and runtime package not admitted before this Stage 2 approval.
- USER approval cleared Branch Readiness Stage 2 execution for this branch, package admission, source-truth sync, validation, commit, and push.

## Exit Criteria

- Branch `codex/fam-006-monitoring-hud-product-surface` exists on origin.
- `PKG-006 Monitoring and HUD Product Surface Package` is admitted with multiple concrete slices and no single-slice waiver.
- All admitted slices carry `Admission State: Admitted`, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`.
- Optional voice/audio widening remains deferred unless later USER approval expands scope.
- Element Coverage remains a non-identity checklist only.
- Backlog, roadmap, branch authority index, and this branch authority record agree on active Branch Readiness, package admission, no runtime implementation, no PR creation, no watcher provisioning, no release work, and no direct-main mutation.
- ChatGPT-facing loader/source-truth neutrality wording is either updated where appropriate or reported as a recommendation needing later USER decision.
- Branch governance validation, Python compile validation, diff validation, and automation observability review run after source-truth sync.

## Rollback Target

- `Branch Readiness`

Rollback Path: delete or abandon `codex/fam-006-monitoring-hud-product-surface` before PR merge; no runtime files, tags, releases, artifacts, or `main` mutation are created by this Stage 2 pass.

## Next Legal Phase

- `Workstream`

Next Legal Seam: `Workstream WS1 - HUD Visual And User-Facing Surface Baseline`

Next Legal Phase Gate: Workstream may start only after Branch Readiness Stage 2 source-truth sync validates green, is committed, and is pushed; Workstream still must obey same-branch package completion and cannot advance to Hardening while admitted implementable slices remain incomplete.

## Branch Objective

Admit a concrete multi-slice runtime package that turns the historical FAM-006 monitoring/thermal architecture baseline into a visible, trustworthy user-facing Monitoring/HUD product surface, connecting telemetry/status truth to desktop presentation, user controls, fail-safe/no-data behavior, and later live validation proof.

## Target End-State

- The branch is durably created and pushed as the active FAM-006 runtime package carrier.
- `PKG-006` is admitted with six concrete implementation slices and one deferred optional voice/audio widening placeholder.
- Workstream can begin on the first admitted slice without another docs-only package-admission PR.
- Runtime implementation has not started during Branch Readiness.
- PR, watcher, release, tag, GitHub Release, artifact, and direct-main actions remain outside Branch Readiness Stage 2.

## Backlog Completion Strategy

Branch Completion Goal: `Complete every admitted PKG-006 slice on this same branch unless a named blocker, future dependency, USER-approved backlog split, or USER-approved scope widening changes the legal route.`
Known Future-Dependent Blockers: `Optional voice/audio behavior is deferred and requires later USER widening approval if spoken/audio behavior, voice integration, persona voice, FAM-004, or cross-family behavior is needed.`
Branch Closure Rule: `Do not leave Workstream after only one admitted slice while remaining admitted PKG-006 slices are implementable; exit Workstream only when package completion is truthfully Green, Blocked, Deferred, or covered by explicit USER-approved split/waiver.`

## Expected Seam Families And Risk Classes

- HUD visual/user-facing surface; risk class: desktop/UI because a visible status surface affects readability, focus, trust, and operator comprehension.
- Runtime telemetry source/adapters; risk class: backend/runtime because local CPU/GPU, thermal, performance, and Nexus self-observation signals must be bounded and non-invasive.
- Desktop placement and renderer ownership; risk class: desktop/UI because HUD placement must avoid shell, tray, panel, focus, and renderer-lifecycle drift.
- Settings and user controls visibility; risk class: settings/configuration because users need clear control over visibility and behavior without creating hidden always-on telemetry.
- Fail-safe/no-data/degraded-status behavior; risk class: safety/privacy because unavailable, stale, partial, or unsupported data must be truthful and non-alarming.
- Validation/live desktop proof; risk class: validation/live-test because the package is user-facing and must prove the desktop surface in a real or closest-valid desktop session before closeout.

## User Test Summary Strategy

This package is expected to create a user-facing desktop surface during Workstream, so the active workstream must add a concrete `## User Test Summary` section before Live Validation and must export the user-facing summary to the documented desktop path unless canon records a valid exception.

Branch Readiness does not require a completed User Test Summary because no runtime implementation has started yet.

## Later-Phase Expectations

- Workstream executes one admitted slice at a time and continues on this branch while `Package Completion State` remains `In Progress`.
- Hardening must pressure-test telemetry truthfulness, UI placement, settings/control visibility, fail-safe states, and regression risk across touched runtime surfaces.
- Live Validation must include real desktop or closest-valid live desktop proof for the user-facing HUD surface and must preserve User Test Summary results.
- PR Readiness must confirm merge-target authority projection, selected-next successor handling, package completion state, PR summary, watcher plan, bot-review state, mergeability, and merge-watch before PR green.
- Release Readiness remains separate, file-frozen, and requires later release approval if the package becomes release-bearing.

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing, backend/runtime`
Docs-Only Workstream: `No`
Planning-Loop Bypass User Approval: `None`
Planning-Loop Bypass Reason: `None`

- PKG-006 is a runtime-focused implementation branch. This Branch Readiness Stage 2 pass admits package/slice source truth only; actual runtime implementation starts in Workstream.

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

- The admitted package has six concrete slices and is not a one-slice branch.
- Workstream must continue to the next admitted slice whenever scope, phase, risk, and validation authority remain green.
- Stopping after one admitted slice requires a named blocker, future dependency, or explicit USER-approved backlog split/waiver.

## Admitted Implementation Slice

Primary Entry Slice: `SLC-016 HUD visual and user-facing monitoring surface`

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-016` | `PKG-006` | `FAM-006` | HUD visual and user-facing monitoring surface | Admitted | Branch Readiness admitted | In Progress | `BR-S2-S1`; planned `WS1` |
| `SLC-025` | `PKG-006` | `FAM-006` | Runtime telemetry source and adapter boundary | Admitted | Branch Readiness admitted | In Progress | `BR-S2-S2`; planned `WS2` |
| `SLC-026` | `PKG-006` | `FAM-006` | Desktop placement and renderer ownership | Admitted | Branch Readiness admitted | In Progress | `BR-S2-S3`; planned `WS3` |
| `SLC-027` | `PKG-006` | `FAM-006` | Settings and user controls visibility | Admitted | Branch Readiness admitted | In Progress | `BR-S2-S4`; planned `WS4` |
| `SLC-028` | `PKG-006` | `FAM-006` | Fail-safe, no-data, and degraded-status behavior | Admitted | Branch Readiness admitted | In Progress | `BR-S2-S5`; planned `WS5` |
| `SLC-029` | `PKG-006` | `FAM-006` | Validation and live desktop proof | Admitted | Branch Readiness admitted | In Progress | `BR-S2-S6`; planned `WS6` |

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
- Release impact: `Pending Future Package - no release work approved in Branch Readiness`

Element Coverage Admission Rule: `Element Coverage rows are non-identity checklist rows only and do not count as admitted slices, seams, packages, FAMs, selected-next truth, or release drivers.`

## Initial Workstream Seam Sequence

Seam 1: `BR-S2-S1 - Branch Creation And Package Admission`
Goal: create the approved branch, admit the multi-slice PKG-006 runtime package, and sync branch authority/backlog/roadmap truth without runtime implementation.
Scope: branch creation, package/slice ledger admission, current-state source-truth sync, ChatGPT loader/source-truth evaluation, validation, commit, and push.
Non-Includes: runtime/product code edits, PR creation, watcher provisioning, tag/GitHub Release/artifact work, release execution, direct-main mutation, single-slice waiver, new FAM/package creation, or voice/audio widening.

Seam 2: `WS1 - HUD Visual And User-Facing Surface Baseline`
Goal: begin Workstream with the visible HUD/status surface once Branch Readiness is complete.
Scope: user-facing HUD presentation bounded by FAM-006 package authority.
Non-Includes: voice/audio behavior, plugin-fed telemetry, installer changes, release execution, or package completion claims before admitted slices are complete.

## Active Seam

Active seam: Branch Readiness Stage 2 - FAM-006 Monitoring and HUD Product Surface Package Admission.

Seam Status: `In Progress`
Slice Status: `In Progress`
Completion Status: `In Progress`
Waiver Status: `None`
Continue Decision: `Continue through Branch Readiness Stage 2 source-truth sync, validation, commit, and push`
Stop Basis: `None`

## Validation Plan

- `git status --short --branch`
- `python dev/orin_branch_governance_validation.py`
- `python -m compileall -q dev`
- `git diff --check`
- `python dev/automation_observability_report.py`

Later Workstream validation must add focused runtime/HUD validation and live desktop proof after implementation begins.
