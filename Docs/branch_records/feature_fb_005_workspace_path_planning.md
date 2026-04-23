# Branch Authority Record: feature/fb-005-workspace-path-planning

## Branch Identity

- Branch: `feature/fb-005-workspace-path-planning`
- Workstream: `FB-005`
- Branch Class: `implementation`

## Purpose / Why It Exists

This branch exists because `v1.6.5-prebeta` is published and validated, FB-030 post-release canon closure must ride the next legal branch surface, and FB-005 remains the selected-next planning-only lane after release debt cleared.

FB-005 remains selected-only / `Registry-only` on this branch. This branch is limited to post-release canon closure plus Branch Readiness blocker assessment and must not admit workspace movement, file relocation, import rewiring, launcher-route changes, log-root changes, or broader restructuring until explicit path-sensitive workspace approval exists.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Current execution surface is `Active Branch`.
- branch was created from updated `main` at `7c2933d6427feb08a1139ba7f5ba2393eb61f1e1`
- `v1.6.5-prebeta` is live at `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.5-prebeta` on target commit `7c2933d6427feb08a1139ba7f5ba2393eb61f1e1`
- FB-030 is Released / Closed in `v1.6.5-prebeta`, latest public prerelease truth is `v1.6.5-prebeta`, and merged-unreleased release debt is clear
- FB-005 remains selected-next planning-only / `Registry-only`
- Branch Readiness is active on `feature/fb-005-workspace-path-planning`, but Workstream is not admitted
- explicit path-sensitive workspace approval remains unresolved
- no bounded FB-005 workspace/path slice is admitted yet
- no workspace movement, import rewiring, launcher-path change, log-root change, or user-facing path change has started

## Branch Class

- `implementation`

## Blockers

- `Explicit Path-Sensitive Workspace Approval Missing`
- `Bounded Workspace/Path Slice Not Yet Admitted`

## Entry Basis

- `v1.6.5-prebeta` is published and validated at `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.5-prebeta` on commit `7c2933d6427feb08a1139ba7f5ba2393eb61f1e1`
- updated `main` is revalidated after release publication
- FB-030 release debt is live-cleared and post-release canon closure must now become durable on the next legal branch surface
- FB-005 remains the selected-next planning-only backlog item
- historical closeouts already preserve completed FB-005 Step 3 and Step 4 slices, while Step 5 and broader workspace follow-through remain deferred and path-sensitive

## Exit Criteria

- latest public prerelease truth is advanced to `v1.6.5-prebeta` across canon
- FB-030 is durably Released / Closed and merged-unreleased release debt is clear in canon
- FB-005 remains truthfully selected-only / `Registry-only` unless Branch Readiness completes
- explicit path-sensitive workspace approval is recorded
- one bounded FB-005 workspace/path slice is admitted with exact file/path ownership, migration limits, validation coverage, and rollback instructions
- only then may FB-005 promote and advance to `Workstream`

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Branch Readiness`
