# Branch Authority Record: feature/automation-planning

## Branch Identity

- Branch: `feature/automation-planning`
- Branch Class: `docs/governance`

## Purpose / Why It Exists

This branch carries the USER-approved automation-planning governance pass on the current branch instead of opening a second standalone repair lane.

It begins with the already-landed post-merge canon repair at `0a1c23c` and uses `Branch Readiness` to frame automation monitoring, validation, scheduling, and operator workflow rules before any automation implementation, recurring-job rollout, or release execution begins.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Repo State: `Branch-owned docs/governance surface`
- Merged-Main Repo State: `No Active Branch`
- `Active Branch`: `feature/automation-planning`
- Current Active Branch: `feature/automation-planning`
- Current Active Branch Authority Record: `Docs/branch_records/feature_automation_planning.md`
- Current Active Canonical Workstream Doc: `None`
- Latest Public Prerelease: `v1.6.12-prebeta`
- Latest Public Release Commit: `b06c359e58b47cfe26fe8c4b39ac04fde519dee9`
- Latest Public Prerelease Publication: `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.12-prebeta`
- Latest Public Prerelease Title: `Pre-Beta v1.6.12`
- Selected Next Workstream: `FB-049 Active-session pre-settled incoming-launch conflict truth`
- Selected Next Record State: `Registry-only`
- Selected Next Implementation Branch: `Not created`
- Historical Branch Readiness Seam: `Branch Readiness BR1 - Automation Planning Scope Admission`
- BR1 result: complete and green. The automation-planning purpose is now explicit from repo truth, admitted scope and out-of-scope boundaries are defined, the branch remains `docs/governance` and `docs-only`, the first bounded planning seam chain is explicit, no automation implementation or rollout work has begun, and FB-049 remains the only selected-next user-facing candidate.
- Historical Branch Readiness Seam: `Branch Readiness BR2 - PR Watcher And Recurring Monitor Policy`
- BR2 result: complete and green. PR watcher, bot-review, recurring status-update, signal, output, and prohibited-action boundaries are now explicit; heartbeat-vs-cron policy is defined; the branch remains `docs/governance` and `docs-only`; no automation implementation, activation, deletion, or scheduling work has begun; and FB-049 remains the only selected-next user-facing candidate.
- Current Branch Readiness Seam: `Branch Readiness BR3 - Repo-Hygiene Automation Candidates And Rollout Boundaries`
- Branch Readiness Status: in progress. This branch remains admitted under explicit `Docs/Governance Branch Waiver: APPROVED`, the carried post-merge canon repair from `0a1c23c` remains on this same branch as the required prior-miss closure surface, BR3 is now defining repo-hygiene automation candidates and rollout boundaries, no automation implementation or rollout work has begun, merged backlog-family governance reform truth remains historical traceability only after PR #98 merged, and FB-049 remains the only selected-next user-facing candidate.
- Next Active Seam: `Branch Readiness BR3 - Repo-Hygiene Automation Candidates And Rollout Boundaries`

## Branch Class

- `docs/governance`
- `Docs/Governance Branch Waiver: APPROVED`

## Blockers

None.

## Entry Basis

- The USER explicitly approved `Docs/Governance Branch Waiver: APPROVED` for this branch.
- The current branch already carries the merged-main post-merge canon repair at `0a1c23c`.
- No active implementation branch remains; merged-main repo truth is `No Active Branch`.
- The USER explicitly directed current-branch reuse and branch rename instead of opening a second repair-only branch.
- Automation work is starting in `Branch Readiness` only; no automation implementation or rollout work is admitted yet.

## Exit Criteria

- The current branch is durably recorded as the active automation-planning authority surface across backlog, roadmap, and branch-record routing.
- The branch objective, target end-state, risk classes, validation contract, later-phase needs, and first admitted seam sequence are explicit.
- The carried post-merge repair remains preserved on this same branch without reopening a between-branch canon repair path.
- No automation implementation begins before Branch Readiness closes green.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Workstream`

## Scope

- branch-admission and authority-sync work for automation planning
- automation-governance planning for heartbeat and cron usage boundaries
- PR watcher, bot-review handling, and recurring status-update policy framing
- validator, operator-output, and blocker-handling contract planning for automation-driven monitoring
- rollout-boundary definition for future automation creation without creating automations yet

## Explicit Non-Goals

- no runtime or product behavior changes
- no backend or developer-tooling implementation changes
- no selected-next truth changes
- no backlog-family structure changes
- no automation creation, activation, deletion, or scheduling changes on this seam
- no automation TOML edits and no `automation_update` calls on this seam
- no PR or release execution on this seam
- no FB-049 branch admission or successor-branch work

## Branch Objective

Establish the current branch as the admitted automation-planning authority surface and define the bounded planning contract for PR monitoring, recurring repo-watch automations, and operator-facing automation lifecycle rules without starting implementation work.

## Target End-State

This branch owns a complete Branch Readiness frame for automation planning: truthful branch authority, bounded scope, explicit seams, validation expectations, scheduling-policy boundaries, and a clear handoff into `Workstream` only if the planning surface closes green.

## Backlog Completion Strategy

Branch Completion Goal: Admit automation planning on the current branch, preserve the carried post-merge canon repair, and fully define automation-planning purpose, scope, seam chain, monitoring-policy boundaries, and rollout prerequisites before any later automation implementation or rollout work begins.
Known Future-Dependent Blockers: Live GitHub connector behavior, later automation rollout approval, minute-cadence notification noise tradeoffs, and any release-window or branch-readiness interaction discovered after planning are outside BR1 unless the USER explicitly widens scope.
Branch Closure Rule: Stay in Branch Readiness until the automation-planning authority surface, validation contract, first admitted planning seam chain, and implementation-vs-non-implementation boundaries are explicit and green on this same branch.

## Expected Seam Families And Risk Classes

- branch-authority and current-state truth alignment
- automation catalog and lifecycle-boundary planning
- PR watcher, bot-review, and recurring status-update policy planning
- repo-hygiene watcher and release-sentinel planning
- validator and operator-contract alignment for automation-related governance

## User Test Summary Strategy

Docs/governance planning only. No manual User Test Summary artifact is required unless later seams widen into implemented automations or runtime-facing behavior.

## Later-Phase Expectations

- If Branch Readiness closes green, `Workstream` remains `docs/governance` and planning-only until the USER explicitly widens scope.
- Any reusable live watcher or automation rollout must stay on this same branch unless a later blocker or waiver requires a different legal surface.
- Future automation creation must stay subordinate to the planning seams admitted here and must not silently widen into runtime, backend, or release execution work.
- Selected-next FB-049 truth, backlog-family routing, and release-debt history remain preserved while this branch plans automation work.

## Initial Workstream Seam Sequence

Seam 1: Admit automation-planning scope and branch purpose from repo truth.
Goal: Define the governing automation-planning purpose, admitted scope, explicit non-goals, and the planning-only boundaries that keep this branch `docs/governance` only.
Scope: Docs and governance planning only across branch-local authority truth, automation purpose, in-scope/out-of-scope framing, and selected-next preservation.
Non-Includes: No automation files are created, no heartbeat or cron automations are configured, no PR or release actions are taken, no runtime or product behavior is changed, and no successor branch is admitted in this seam.

Seam 2: Define short-lived PR watcher and recurring monitor policy.
Goal: Normalize the approved watcher lifecycle, polling cadence policy, bot-signal handling, stop conditions, and self-termination behavior for PR-bound automations.
Scope: Planning-only rules for heartbeat use, minute polling, comment-resolution behavior, approval-signal handling, and when monitoring may re-enter later phases.
Non-Includes: No live watcher is created or modified in this seam, no PR bot state is treated as implementation progress, and no release execution or PR merge action is taken.

Seam 3: Define repo-hygiene automation candidates and rollout boundaries.
Goal: Make the later automation implementation surface explicit so reusable watchers, release sentinels, and drift audits do not drift across branch, phase, or release boundaries.
Scope: Planning-only rules for cron versus heartbeat usage, reporting cadence, blocker handling, branch-local ownership, and future rollout prerequisites.
Non-Includes: No automation catalog is activated, no scheduling state is written, and no runtime, backend, or user-facing feature work is admitted.

## PR Watcher Policy

- PR watcher monitoring is planning-approved only for live PR state on the active branch or another PR surface explicitly named by the USER.
- A PR watcher may monitor polling-based PR facts only; this planning surface does not assume webhook or event-driven execution.
- Allowed PR watcher signals are:
  - PR existence, number, URL, base branch, head branch, and current head commit
  - open, closed, merged, draft, mergeable, or merge-state truth when available
  - unresolved review-thread or Codex-comment presence when the available tool surface can prove it
  - bot-review approval or bot-comment state defined in the bot-review policy below
- PR watcher outputs are limited to thread or inbox status updates, governed state markers, blocker names, repair-candidate classification, and ready/not-ready posture for the current phase.
- PR watcher monitoring alone must not be treated as implementation progress, release execution, or selected-next truth mutation.

## Bot-Review Monitor Policy

- Bot-review monitoring is limited to the live PR approval gate and unresolved bot-comment follow-through on a named PR.
- Allowed bot-review signals are:
  - thumbs-up or equivalent approval reaction on the live PR
  - bot comment presence on the live PR
  - comment-resolution closeout for the current PR after a bounded fix path is completed on the same branch
- A live PR thumbs-up clears the approval gate for monitoring purposes.
- A bot comment remains a blocking signal until the later implementation or PR-ready repair path fixes the issue on the same branch, pushes, resolves the comment, and records comment-addressed closeout; no later thumbs-up is required after that closeout path.
- Monitoring output may report `PR Validation Pending`, `Bot Review Signal Pending`, comment-addressed closeout, or ready-to-re-enter later validation phases, but it must not merge the PR, resolve comments, or mutate branch truth from this planning seam.

## Recurring Status-Update Policy

- Recurring status-update monitoring is planning-approved for thread-attached progress reporting only.
- State-change-only updates are the default recurring posture.
- Every-run interval updates are allowed only when the USER explicitly requests high-frequency confirmation for a short-lived watcher.
- Recurring updates may report:
  - current monitored target
  - current head or revision truth
  - latest observed signals
  - whether a blocker remains active
  - whether the branch is ready to re-enter the next legal validation or release phase
- Recurring updates must stay concise and must not claim work completed when only monitoring evidence changed.

## Heartbeat Vs Cron Boundary

- `heartbeat` is the approved planning surface for thread-attached, minute-scale, short-lived monitoring such as live PR watcher checks, bot-review checks, or high-frequency operator confirmation.
- `cron` is the approved planning surface for slower recurring workspace jobs such as repo-hygiene drift sweeps, release sentinels, or periodic audit checks.
- In this planning model, heartbeat is the only approved minute-cadence monitor class.
- Cron-style automation is bounded to hourly-or-slower repo or workspace checks and must not be used to impersonate an active per-minute PR watcher.
- Any future watcher implementation must declare whether it is heartbeat- or cron-owned before activation.

## Allowed Outputs

- governed state markers
- current monitored target and observed signal summary
- blocker names and blocker-clearing action descriptions
- repair-candidate classification
- ready/not-ready or continue/stop decisions for the active phase
- concise recurring status updates to the active thread or inbox surface

## Prohibited Actions

- creating, activating, deleting, pausing, resuming, or rescheduling automations
- calling `automation_update`
- editing automation TOML or automation memory files
- mutating runtime, backend, developer-tooling, or user-facing product files
- auto-merging PRs, auto-closing PRs, or auto-resolving review threads
- staging, committing, or pushing code based only on monitor observations
- changing selected-next truth, admitting FB-049, or opening successor implementation branches
- treating monitoring-only state changes as completed implementation or release execution
- using cron-style automation as a substitute for minute-scale heartbeat monitoring
- using heartbeat monitoring to bypass later phase gates, blockers, waivers, or release controls

## Active Seam

- Active seam: `Branch Readiness BR3 - Repo-Hygiene Automation Candidates And Rollout Boundaries`
