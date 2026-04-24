# Branch Authority Record: feature/fb-042-step5-entrypoint-planning

## Branch Identity

- Branch: `feature/fb-042-step5-entrypoint-planning`
- Workstream: `FB-042`
- Branch Class: `implementation`

## Purpose / Why It Exists

This branch is the active FB-042 planning-only `Branch Readiness` surface after `v1.6.6-prebeta` published and FB-005 release debt was cleared.

It exists to close FB-005 post-release canon, define the exact Step 5 / top-level entrypoint planning boundary, and keep later root-owned entrypoint or broader workspace follow-through deliberate before any Workstream seam is admitted.

This record is the current phase owner while FB-042 remains `Registry-only`. It does not promote FB-042 into a canonical workstream doc yet, and it does not authorize any Step 5, root-entrypoint, launcher/VBS, runtime, audio, log-root, visual-asset, installer, or user-facing desktop-path implementation slice by inertia.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Current branch execution surface is `feature/fb-042-step5-entrypoint-planning`, created from updated `main` at `deeaa691a79dd01897f6aed82f087970db7019b3`.
- `Active Branch`: `feature/fb-042-step5-entrypoint-planning`
- `v1.6.6-prebeta` is live at `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.6-prebeta` on target commit `deeaa691a79dd01897f6aed82f087970db7019b3`.
- FB-005 is Released / Closed in `v1.6.6-prebeta`, and merged-unreleased release debt is now clear in canon.
- Repo-level merge-target truth is released and branchless; this branch is the active planning-only `Branch Readiness` surface.
- FB-042 remains selected-next / `Registry-only`, and no canonical workstream doc exists yet.
- No Step 5 / top-level entrypoint Workstream seam is admitted yet.
- No `main.py`, launcher/VBS, runtime, audio, log-root, visual-asset, installer, or user-facing desktop-path implementation is admitted on this branch.

## Branch Class

- `implementation`

## Blockers

- `Explicit Path-Sensitive Workspace Approval Missing`
- `Bounded Planning-First Slice Not Yet Admitted`

## Entry Basis

- `v1.6.6-prebeta` is published and validated at `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.6-prebeta` on commit `deeaa691a79dd01897f6aed82f087970db7019b3`.
- FB-005 release debt is live-cleared and must now be durably closed in canon on the next legal branch surface.
- Updated `main` is aligned at `deeaa691a79dd01897f6aed82f087970db7019b3`.
- FB-042 was selected next during FB-005 PR Readiness and remains the deferred Step 5 / top-level experience entrypoint and broader workspace follow-through lane.
- `Branch Readiness` may carry planning, admission, and tightly coupled canon-repair work here, but it must not execute product/runtime implementation.

## Exit Criteria

- Latest public prerelease truth is advanced to `v1.6.6-prebeta` across canon.
- FB-005 is durably Released / Closed in canon and merged-unreleased release debt is clear.
- FB-042 branch objective, target end-state, exact owned surfaces, non-goals, expected seam families, validation contract, User Test Summary strategy, and later-phase expectations are explicit.
- One bounded planning-first Step 5 / top-level entrypoint seam is explicitly admitted before Workstream begins.
- Until that admission exists, FB-042 remains selected-next planning-only / `Registry-only`.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Branch Readiness`

## Branch Objective

- Define the planning-first Step 5 / top-level experience entrypoint and broader workspace follow-through lane without silently admitting implementation.
- Separate root-owned entrypoint, launcher/VBS, workspace-layout, and user-facing invocation boundaries so later work cannot guess across them.
- Establish the approval and validation contract for any later Step 5 or broader workspace move before a canonical workstream is promoted.

## Target End-State

- FB-042 has explicit planning-owned boundaries for top-level entrypoints, adjacent workspace follow-through, non-goals, and admission limits.
- Current branch truth clearly distinguishes planning-only `Branch Readiness` from Workstream admission.
- A first bounded planning seam can be approved deliberately later without reopening FB-005 or treating branch existence as implementation authorization.

## Scope

- Planning-only branch-readiness framing for Step 5 / top-level experience entrypoint and broader workspace follow-through.
- Exact owned planning surfaces around `main.py`, `launch_orin_desktop.vbs`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `Docs/workspace_layout_plan.md`, and adjacent branch-truth canon.
- Admission rules for future planning-first seams that touch root-owned entrypoints, launcher paths, broader workspace structure, or user-facing invocation surfaces.

## Non-Goals

- No runtime behavior changes.
- No entrypoint rewiring.
- No launcher/VBS edits.
- No audio-path, logs-path, or visual-asset changes.
- No installer or user-facing shortcut changes.
- No file moves or broader workspace implementation.
- No canonical workstream promotion until a bounded planning seam is explicitly admitted.

## Expected Seam Families And Risk Classes

- Current top-level entrypoint and root-owned surface inventory; risk class: root-entrypoint / launcher / runtime-boundary.
- Workspace follow-through boundary framing; risk class: path-ownership / import / packaging.
- User-facing invocation and rollback framing; risk class: shortcut / installer / operator-facing.
- Implementation admission and stop-loss contract; risk class: governance / scope-control.

## Validation Contract

- Run `python dev\orin_branch_governance_validation.py`.
- Run `git diff --check`.
- Confirm `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/workstreams/index.md`, and this branch authority record all advance latest public prerelease truth to `v1.6.6-prebeta`.
- Confirm FB-005 is durably Released / Closed in canon and no merged-unreleased release debt remains.
- Confirm `Docs/branch_records/index.md` lists this record under Active Branch Authority Records.
- Confirm FB-042 remains `Registry-only`, has no canonical workstream doc yet, and no Workstream seam is admitted.
- Confirm no `main.py`, `launch_orin_desktop.vbs`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `Audio/`, `logs/`, or user-facing desktop-path file changes occur in this `Branch Readiness` pass.

## User Test Summary Strategy

- `Branch Readiness` is planning/canon only and does not change user-facing behavior.
- No desktop shortcut validation, desktop export, or manual `## User Test Summary` artifact is required unless a later admitted seam changes user-facing invocation, launcher, runtime, or installer behavior.

## Later-Phase Expectations

- Workstream may begin only after a bounded planning-first seam is explicitly admitted.
- That first admitted seam must stay docs/canon only unless a later explicit approval widens it.
- Any later implementation-facing Step 5 or broader workspace change must name exact owned paths, rollback, user-facing trigger surfaces, and validation proof before execution.

## Candidate First Workstream Seam

Seam 1: Current top-level entrypoint and adjacent workspace ownership inventory

- Admission Status: Not admitted yet.
- Goal: inventory current ownership around `main.py`, `launch_orin_desktop.vbs`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and `Docs/workspace_layout_plan.md` before any path move or entrypoint change is considered.
- Scope: docs/canon inventory, ownership map, risk capture, boundary notes, rollback notes, and implementation non-goals.
- Non-Includes: no file moves, no runtime edits, no launcher/VBS edits, no shortcut or installer edits, and no broader workspace implementation.
- Gate: explicit path-sensitive approval must admit this bounded planning seam before FB-042 may advance to Workstream.
