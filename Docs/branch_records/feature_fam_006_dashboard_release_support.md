# Branch Authority Record: feature/fam-006-dashboard-release-support

## Branch Identity

- Branch: `feature/fam-006-dashboard-release-support`
- Workstream: `FAM-006 Dashboard Release Support / Issue Closeout Planning`
- Branch Class: `release packaging`
- Backlog Record State: `Registry-only issue-resolution / release-support continuation under historical FAM-006 / PKG-006`
- Package ID: `PKG-006`
- Package Name: `Monitoring HUD Dashboard Product Surface`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 carrier for FAM-006 post-merge source-truth repair after PR #129 and PR #132.

It exists because PR #129 merged Dashboard render/layout hardening for issues #123, #124, and #127, PR #132 merged Dashboard IA/control follow-through for issues #125 and #126, and Release Readiness on main is file-frozen. The branch records merged-unreleased FAM-006 Dashboard release debt, cleans stale active/open/watch wording, and prepares issue-closeout and release-readiness sequencing without performing issue closeout or release execution.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Stage 1: `Complete - accepted feature/fam-006-dashboard-release-support as the correct legal FAM-006 carrier for post-PR #129/#132 source-truth drift, issue-closeout planning, and release-readiness sequencing`
- Stage 2 USER Approval: `Granted - USER approved branch creation, source-truth repair, validation, commit, and push`
- `Active Branch`: `feature/fam-006-dashboard-release-support`
- Branch Creation: `Created from main at 98b53fafd63abfe4876b718d5649b4a0df46f2a0, the PR #132 merge commit`
- Source-Truth Repair: `In progress on this branch`
- Runtime Implementation: `Not admitted - this is a source-truth / release-support carrier only`
- GitHub Issue Closeout: `Pending USER approval for #123, #124, #125, #126, and #127`
- Release Execution: `Pending USER approval`

## Branch Class

- `release packaging`

## Blockers

- `GitHub Issue Closeout Approval Missing`: active for comments or state changes on #123, #124, #125, #126, and #127.
- `PR Creation Approval Missing`: active for this release-support branch.
- `Release Execution Approval Missing`: active.
- `Raw Evidence Import Decision Pending`: active.
- `FAM-007 / Local AI Authority Missing`: active and out of scope.
- `Runtime Scope Expansion Approval Missing`: active for provider/model/memory/shortcut/installer work or runtime implementation outside the already merged FAM-006 Dashboard issue-resolution PRs.

## Entry Basis

- PR #129 `FAM-006 Dashboard render/layout hardening` merged on 2026-05-13 at merge commit `96ec36e7be751d444eda8dc220bc4a035d44fca1`.
- PR #129 completed #123 Dashboard initial open flicker, #124 Dashboard scroll content well clipping / scrollbar ownership, and #127 Dashboard resize jitter / catch-up lag in source truth.
- PR #132 `FAM-006 Dashboard IA/control follow-through` merged on 2026-05-13 at merge commit `98b53fafd63abfe4876b718d5649b4a0df46f2a0`.
- PR #132 completed #125 Monitor Groups dead space / Create/Edit window split and #126 redundant open badge / close affordance in source truth.
- GitHub issues #123, #124, #125, #126, and #127 remain open and pending closeout until USER separately approves comments/state changes.
- Raw screenshots, videos, and UTS exports remain local/external unless USER later approves upload, import, or linking.
- FAM-007, Workspace Runtime Isolation Stage 2, AI Product Contract import, runtime/provider/model/memory/shortcut/installer work, release execution, tags, GitHub Releases, and artifacts remain separate USER approval checkpoints.

## Exit Criteria

- Source truth records PR #129 and PR #132 as merged FAM-006 Dashboard issue-resolution work.
- Release debt records PR #129 and PR #132 as merged-unreleased work after `v1.7.0-prebeta`.
- Branch 2 / PR #132 historical records no longer claim open PR, active watcher, bot-review pending, or merge-pending authority.
- #123 through #127 remain pending GitHub issue closeout only.
- Release-readiness sequencing is recorded without executing release work.
- Validation passes.
- Branch is committed and pushed.

## Rollback Target

- `Branch Readiness`

Rollback Path: abandon or repair `feature/fam-006-dashboard-release-support`. Do not mutate main directly, edit GitHub issue state, import raw media, enter FAM-007/local AI work, execute release, create tags, create GitHub Releases, or create artifacts from this branch.

## Next Legal Phase

- `PR Readiness`

Next Legal Phase Gate: After this Branch Readiness Stage 2 source-truth repair validates, commits, and pushes, the next legal step is USER decision on PR Readiness Stage 1 for this release-support branch. GitHub issue comments/closeout, PR creation, merge, release execution, raw evidence handling, FAM-007/runtime work, and AI Product Contract import remain separate USER approval checkpoints.

## Release-Support Repair Scope

Merged-Unreleased Release Debt: `PR #129 FAM-006 Dashboard render/layout hardening` plus `PR #132 FAM-006 Dashboard IA/control follow-through`.

Release Target: `v1.7.1-prebeta`

Release Floor: `patch prerelease`

Version Rationale: PR #129 and PR #132 harden and complete issue-resolution work for an already released FAM-006 Dashboard surface after `v1.7.0-prebeta`; they do not open a new product lane.

Release Scope: `PR #129 FAM-006 Dashboard render/layout hardening for #123/#124/#127 plus PR #132 FAM-006 Dashboard IA/control follow-through for #125/#126.`

Release Artifacts: `Pending - no tag, GitHub Release, release notes, or artifacts are approved or created by this branch.`

Issue Closeout Plan: `#123`, `#124`, and `#127` should be closeout-reviewed as completed by PR #129; `#125` and `#126` should be closeout-reviewed as completed by PR #132. Summary-only GitHub comments and issue closure require later USER approval.

Raw Evidence Policy: Raw screenshots, videos, and UTS exports remain local/external unless USER later approves upload, import, or linking.

FAM-007 Boundary: FAM-007 remains separate historical/current-main context only. This branch does not admit FAM-007 runtime implementation, branch work, local AI work, provider/model/memory/shortcut/installer work, or AI Product Contract import.

## Stage 2 Validation Plan

- `git status --short --branch`
- `git fetch origin --prune`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git worktree list`
- `git diff --check origin/main...HEAD`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_release_body_validation.py`
- `python -m compileall -q dev desktop Audio main.py`

## Branch Objective

Repair FAM-006 post-merge source truth after PR #129 and PR #132, record merged-unreleased release debt, and prepare issue-closeout / release-readiness sequencing without performing issue closeout or release execution.

## Target End-State

- PR #129 and PR #132 are recorded as merged-unreleased FAM-006 Dashboard work after `v1.7.0-prebeta`.
- #123, #124, #125, #126, and #127 are recorded as completed in source truth and pending GitHub closeout only.
- Release execution remains blocked pending USER approval.
- Raw evidence remains local/external.
- FAM-007 and runtime/provider/model/memory/shortcut/installer work remain out of scope.

## Backlog Completion Strategy

Branch Completion Goal: `Complete source-truth release-support repair and prepare the branch for PR Readiness Stage 1.`

Known Future-Dependent Blockers: `GitHub issue closeout/comments, raw evidence upload/import/linking, PR creation, merge, release execution, tags, GitHub Releases, artifacts, FAM-007 runtime/admission, AI Product Contract import, and runtime/provider/model/memory/shortcut/installer work all require later USER approval.`

Branch Closure Rule: `Stop after validation, commit, and push; do not create a PR, close/comment issues, execute release work, import raw evidence, or enter runtime/FAM-007 scope without later USER approval.`

## Expected Seam Families And Risk Classes

- Source-truth drift repair: backlog, roadmap, branch-record index, Branch 1 historical record, Branch 2 historical record, and FAM-006 product-surface record.
- Release-debt routing: PR #129 and PR #132 merged-unreleased work after `v1.7.0-prebeta`.
- Issue-closeout planning: #123 through #127 remain pending USER-approved GitHub comments/state changes.
- Risk class: docs/source-truth only; no runtime code or release artifact changes.

## User Test Summary Strategy

No new User Test Summary is required for this source-truth release-support carrier. Existing H1/live proof remains historical evidence in PR #129 and PR #132 branch records; raw evidence import/linking remains pending USER approval.

## Later-Phase Expectations

- PR Readiness Stage 1 may be requested after this branch validates and is pushed.
- PR creation requires later USER approval.
- Merge requires later USER approval.
- Release Readiness and release execution require later USER approval after the release-support PR path is complete.
- GitHub issue closeout/comments require later USER approval.

## Initial Workstream Seam Sequence

Seam 1: Source-truth release-support repair.

Goal: Record PR #129 and PR #132 as merged-unreleased FAM-006 Dashboard work, clear stale active/open/watch wording, and preserve issue closeout/release execution as pending USER decisions.

Scope: Docs/source-truth updates only for the expected FAM-006 release-support files.

Non-Includes: GitHub issue closeout/comments, PR creation, merge, release execution, tag creation, GitHub Release creation, artifact creation, raw evidence upload/import/linking, FAM-007 work, runtime/provider/model/memory/shortcut/installer work, or runtime implementation.

## Active Seam

Active seam: Source-truth release-support repair.
