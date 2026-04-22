# FB-031 Nexus Desktop AI UI/UX Overhaul Planning

## Identity

- ID: `FB-031`
- Title: `Nexus Desktop AI UI/UX overhaul planning`

## Record State

- `Promoted`

## Status

- `Branch Readiness`

## Release Stage

- `pre-Beta`

## Target Version

- `TBD`

## Canonical Branch

- `feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning`

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- `Active Branch`
- FB-040 is released and closed in `v1.6.0-prebeta`.
- Release debt is clear.
- FB-031 is admitted only for Branch Readiness scaffold, source-map planning, and blocker-clearing governance repair before any UI implementation.

## Branch Class

- `implementation`

## Blockers

None after FB-040 post-release canon repair and release-version governance hardening.

## Entry Basis

- `main` was clean and aligned with `origin/main` before this branch was created.
- Live release truth confirms `v1.6.0-prebeta` exists and points at the FB-040 release commit.
- Durable canon still lagged FB-040 released truth, so this branch's first Branch Readiness seam repairs that escaped post-release drift before any FB-031 implementation can begin.
- FB-031 was the selected successor lane in FB-040 merge-target canon and is now the legal active Branch Readiness surface.

## Branch Objective

- Define the Nexus-era UI/UX overhaul planning lane without implementing UI behavior.
- Establish a deliberate source map, visual-language ownership vocabulary, validation contract, and non-goal boundary before any UI, launcher, settings, overlay, tray, or runtime implementation work is admitted.

## Target End-State

- FB-031 has a complete Branch Readiness scaffold.
- FB-040 release truth is closed and release debt is clear across backlog, roadmap, workstreams index, and FB-040 workstream canon.
- The initial FB-031 Workstream seam sequence is explicit enough for later Workstream execution to begin safely.
- No product/runtime UI implementation is added during Branch Readiness.

## Scope

- Repair carried-forward FB-040 post-release canon drift.
- Harden post-release closure and release-version advancement governance where directly required by the escaped drift.
- Define the FB-031 UI/UX planning objective, target end-state, seam families, validation contract, stop conditions, and first Workstream seam sequence.

## Non-Goals

- No UI implementation.
- No launcher implementation.
- No settings implementation.
- No tray, taskbar, overlay, HUD, shortcut, voice, plugin, installer, or runtime behavior changes.
- No release execution.
- No FB-031 PR or Release Readiness work.

## Expected Seam Families And Risk Classes

- Source-map and ownership seam family; risk class: product architecture, because UI/UX planning needs one owner map before design details spread across surfaces.
- Visual-language boundary seam family; risk class: desktop/UI, because visual direction can affect discoverability, trust, focus, and operator confidence.
- Validation/admission seam family; risk class: governance/validator, because future UI implementation seams must prove evidence depth, user-facing test coverage, and non-regression before they begin.

## User Test Summary Strategy

- Branch Readiness has no user-facing behavior and no manual UTS artifact requirement.
- If later Workstream seams add or modify user-visible UI, the workstream must add a concrete `## User Test Summary` checklist before Live Validation.
- If FB-031 remains architecture/planning-only through a later phase, any UTS waiver must be recorded in the exact `## User Test Summary` section with waiver reasons.

## Later-Phase Expectations

- Workstream must begin with a source map and visual-language ownership vocabulary before any UI implementation can be proposed.
- Hardening must pressure-test ambiguity, surface ownership, validation coverage, accessibility/readability risk, and implementation-readiness gaps.
- Live Validation must classify whether the milestone is user-facing; if no UI is implemented, waiver reasoning must be explicit and machine-checkable.
- PR Readiness must prove merge-target canon, next-workstream selection, helper posture, User Test Summary status, and clean branch truth before PR creation and live PR validation.

## Initial Workstream Seam Sequence

Seam 1: Nexus-era UI/UX source map and visual-language ownership vocabulary

- Status: Planned.
- Goal: define the candidate UI/UX surfaces, ownership terms, visual-language boundaries, and planning vocabulary for Nexus-era UI/UX overhaul work.
- Scope: architecture-only source map, surface inventory, ownership vocabulary, and explicit non-goals for future implementation admission.
- Non-Includes: no UI code, runtime behavior, launcher changes, settings changes, tray/taskbar changes, overlay/HUD rendering, installer changes, assets, or release work.

Seam 2: UI/UX surface boundary and design-system admission contract

- Status: Planned.
- Goal: define which UI/UX surface classes may be admitted later and what design-system proof is required before implementation.
- Scope: surface categories, user-facing risk classes, accessibility/readability expectations, and implementation-admission evidence.
- Non-Includes: no visual redesign, no component implementation, no CSS/style changes, no interaction runtime, and no release work.

Seam 3: validation and User Test Summary admission contract for future UI implementation seams

- Status: Planned.
- Goal: define the validation, live UI audit, User Test Summary, and cleanup expectations required before future FB-031 implementation seams can begin.
- Scope: evidence requirements, user-facing shortcut/entrypoint classification, manual validation expectations, and validator/harness reuse posture.
- Non-Includes: no helper creation unless a later implementation seam proves one is required, no screenshot capture, no UI implementation, and no release work.

## Active Seam

Active seam: Branch Readiness blocker-clearing repair and scaffold completion.

- BR-1 Status: Completed in this pass; FB-040 post-release canon drift repaired.
- BR-2 Status: Completed in this pass; post-release closure and version-advancement governance/validator hardening added.
- BR-3 Status: Completed in this pass; FB-031 Branch Readiness scaffold established and Workstream admission can be evaluated after validation.

## Validation Contract

- `python dev\orin_branch_governance_validation.py`
- `git diff --check`
- `git status --short --branch`
- Validator must compare latest public prerelease canon against the latest local or remote pre-Beta tag.
- Validator must fail if a workstream whose release tag exists remains represented as merged-unreleased release debt.
- Validator must fail future release-floor claims where architecture-only or non-user-facing planning is treated as `minor prerelease` without an executable, runtime, operator-facing, or user-facing capability rationale.

## Stop Conditions

- Stop if FB-040 remains represented as merged-unreleased release debt after repair.
- Stop if latest public prerelease truth trails the live `v1.6.0-prebeta` release.
- Stop if release-version law cannot distinguish architecture-only planning from actual minor capability expansion.
- Stop if FB-031 scope drifts into UI implementation, launcher work, settings work, runtime behavior, assets, or release work.
- Stop if validator hardening requires broad redesign outside post-release closure or release-version advancement.
- Stop if source-of-truth conflicts make FB-031 Branch Readiness admission unclear.

## Exit Criteria

- FB-040 is Released / Closed in `v1.6.0-prebeta`.
- Latest public prerelease truth is `v1.6.0-prebeta`.
- Release debt is clear across backlog, roadmap, workstreams index, and FB-040 workstream canon.
- FB-031 is represented as the active Branch Readiness workstream.
- Branch objective, target end-state, expected seam families, UTS strategy, later-phase expectations, initial Workstream seam sequence, validation contract, and stop conditions are explicit.
- Validator hardening covers post-release closure drift and release-version advancement drift.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Workstream`

## Governance Drift Audit

Governance Drift Found: Yes, repaired during FB-031 Branch Readiness.

- Drift Type: escaped post-release canon closure drift and release-version advancement drift.
- Finding: FB-040 was live as `v1.6.0-prebeta`, but durable canon still carried latest public prerelease `v1.5.0-prebeta`, FB-040 merged-unreleased release debt, and FB-031 selected-only / branch-not-created wording after this branch was created.
- Version Finding: FB-040 advanced by a minor prerelease despite delivering an architecture-only, non-user-facing planning/admission milestone; the published tag remains canonical, but future equivalent work must not use minor advancement solely because it opens a planning lane.
- Repair: latest public prerelease truth is advanced to `v1.6.0-prebeta`, FB-040 is closed/released, release debt is cleared, FB-031 is admitted as the active Branch Readiness workstream, and validator/governance coverage is tightened for remote tag closure and release-floor semantics.
- Governance Drift Found After Repair: No unresolved drift remains after validation.
