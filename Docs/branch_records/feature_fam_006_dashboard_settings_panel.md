# Branch Authority Record: feature/fam-006-dashboard-settings-panel

## Branch Identity

- Branch: `feature/fam-006-dashboard-settings-panel`
- Worktree: `C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard Settings Panel`
- Workstream: `FAM-006 Dashboard Settings Panel`
- Branch Class: `implementation`
- Runtime Carrier Status: `USER-approved FAM-006 runtime-focused Dashboard settings-panel carrier; not a governance-only branch`
- Current Delta Status: `Branch Readiness Stage 2 source-truth setup only; runtime code implementation begins only after later USER approval`
- Backlog Record State: `Registry-only runtime continuation under historical FAM-006 / PKG-006`
- Package ID: `PKG-006`
- Package Name: `Monitoring HUD Dashboard Product Surface`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 carrier for the next FAM-006 runtime-focused Dashboard surface after PR #133 merged the release-support source truth into main.

It exists because the Dashboard settings cog/settings panel remained a deferred FAM-006 Dashboard controls/settings surface after the Dashboard product-surface release and the later issue-resolution PRs. This is not a governance-only branch: the accepted carrier is the FAM-006 Dashboard settings-panel runtime branch. The current Stage 2 commit is source-truth setup only because runtime implementation remains a future USER approval checkpoint. The branch also carries the bounded post-PR #133 source-truth drift repair that must land on the next legitimate runtime-focused FAM-006 carrier before implementation begins.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- `Active Branch`: `feature/fam-006-dashboard-settings-panel`
- Branch Readiness Stage 1: `Complete - USER selected the FAM-006 Dashboard settings panel as the next runtime-focused carrier after PR #133 merge`
- Branch Readiness Stage 2: `Complete - USER approved worktree creation from updated origin/main, branch creation, PR #133 post-merge source-truth drift repair, branch authority setup, validation, commit, and push`
- Runtime Implementation: `Pending USER approval after Branch Readiness Stage 2 completes`
- GitHub Issue Closeout: `Pending USER approval for #123, #124, #125, #126, and #127`
- Release Execution: `Pending USER approval`
- Branch Authority State: `Active`

## Branch Class

- `implementation`

Implementation Delta Class: `docs-only`

## Planning-Loop Guardrail

Implementation Delta Class: `docs-only`
Docs-Only Workstream: `Yes`
Planning-Loop Bypass User Approval: `APPROVED`
Planning-Loop Bypass Reason: `USER approved Branch Readiness Stage 2 setup and bounded post-PR #133 source-truth drift repair on the runtime-focused settings-panel branch; runtime implementation remains blocked until later USER approval.`
Runtime Carrier Marker: `Yes - this is the FAM-006 Dashboard settings-panel runtime carrier; the docs-only delta applies only to Branch Readiness setup before USER-approved runtime implementation.`

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

## Blockers

- `Runtime Implementation Approval Missing`: active until USER approves settings-panel runtime implementation on this branch.
- `PR Creation Approval Missing`: active after Branch Readiness setup until USER approves PR Readiness / PR creation.
- `GitHub Issue Closeout Approval Missing`: active for comments or state changes on #123, #124, #125, #126, and #127.
- `Release Execution Approval Missing`: active.
- `Raw Evidence Import Decision Pending`: active.
- `FAM-007 / Local AI Authority Missing`: active and out of scope for this branch.
- `Provider/Model/Memory/Shortcut/Installer Approval Missing`: active and out of scope for this branch.
- `AI Product Contract Import Approval Missing`: active and out of scope for this branch.

## Entry Basis

- PR #129 `FAM-006 Dashboard render/layout hardening` merged on 2026-05-13 at merge commit `96ec36e7be751d444eda8dc220bc4a035d44fca1`.
- PR #129 completed #123 Dashboard initial open flicker, #124 Dashboard scroll content well clipping / scrollbar ownership, and #127 Dashboard resize jitter / catch-up lag in source truth.
- PR #132 `FAM-006 Dashboard IA/control follow-through` merged on 2026-05-13 at merge commit `98b53fafd63abfe4876b718d5649b4a0df46f2a0`.
- PR #132 completed #125 Monitor Groups dead space / Create/Edit window split and #126 redundant open badge / close affordance in source truth.
- PR #133 `FAM-006 Dashboard release-support source truth` merged on 2026-05-13 at merge commit `228f18e73faabf6ffb6e3b9a5cf32d2f92cd3060`.
- PR #133 recorded PR #129 and PR #132 as merged-unreleased FAM-006 Dashboard release debt and preserved #123 through #127 as pending USER-approved GitHub closeout.
- Main still needed post-PR #133 release-support active-state drift repaired on the next real runtime-focused FAM-006 carrier.
- USER approved this branch/worktree as the FAM-006 runtime-focused carrier and confirmed the multi-worktree waiver for separate FAM-006 and FAM-007 worktrees.

## Exit Criteria

- Worktree `C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard Settings Panel` exists and is clean on `feature/fam-006-dashboard-settings-panel`.
- Branch is created from updated `origin/main` at `228f18e73faabf6ffb6e3b9a5cf32d2f92cd3060`.
- Source truth records PR #133 as merged/historical and no longer treats release-support as the active FAM-006 carrier.
- Source truth establishes this branch as the active FAM-006 settings-panel runtime carrier.
- PR #129 and PR #132 remain merged-unreleased FAM-006 Dashboard release debt.
- #123 through #127 remain completed in source truth and pending USER-approved GitHub closeout.
- FAM-007, provider/model/memory/shortcut/installer work, release execution, artifacts, raw evidence handling, AI Product Contract import, and Private Dev ORIN import remain pending USER decisions.
- Validation passes.
- Branch is committed and pushed.

## Rollback Target

- `Branch Readiness`

Rollback Path: if this setup fails validation, current authorization covers bounded source-truth repair on `feature/fam-006-dashboard-settings-panel` or stopping with the exact USER decision needed. Future USER approval checkpoints remain for runtime implementation, PR creation, merge, GitHub issue state changes, raw media import/linking, FAM-007/local AI work, release execution, tags, GitHub Releases, artifacts, provider/model/memory/shortcut/installer work, AI Product Contract import, and Private Dev ORIN import.

## Next Legal Phase

- `Workstream`

Next Legal Phase Gate: after Branch Readiness Stage 2 setup validates, commits, and pushes, the next legal step is USER decision on runtime implementation for the FAM-006 Dashboard settings panel. PR creation, merge, issue closeout/comments, release execution, raw evidence handling, FAM-007/runtime provider work, AI Product Contract import, and Private Dev ORIN import remain separate USER approval checkpoints.

## Branch Objective

Create the FAM-006 Dashboard settings-panel runtime-focused carrier from updated main, repair PR #133 post-merge source-truth drift, and preserve a clear stop before runtime implementation. The branch is runtime-focused even though the Branch Readiness setup commit is docs/source-truth only.

## Target End-State

- The FAM-006 settings-panel worktree and branch exist from updated `origin/main`.
- Active branch authority points to `feature/fam-006-dashboard-settings-panel`.
- Release-support source truth is historical after PR #133 merge.
- PR #129 and PR #132 remain merged-unreleased release debt.
- Issues #123 through #127 remain completed in source truth and pending USER-approved GitHub closeout.
- Runtime implementation remains blocked until USER approves Workstream entry.

## Product Definition Plan

Product Vision: `Finish the deferred Dashboard settings/control surface by giving the Dashboard a real settings-panel carrier after the issue-resolution PRs are merged.`

User-Facing Goal: `The Dashboard should expose a deliberate settings panel for user-adjustable Dashboard behavior instead of leaving settings/control visibility as a deferred placeholder.`

USER Vision Questions: `None open for Branch Readiness Stage 2; USER selected the FAM-006 Dashboard settings panel as the next runtime-focused carrier and confirmed the separate-worktree waiver. Runtime implementation details remain pending USER approval.`

Codex Product Interpretation: `This branch should first create durable branch authority and clean post-PR #133 drift, then stop. Later implementation should focus only on the Dashboard settings cog/settings panel and should not reopen #123 through #127 or FAM-007.`

Codex Implementation Recommendation: `Use this branch for Branch Readiness setup now; after USER approval, implement the settings-panel surface in the Dashboard/HUD runtime files with matching validators and user-facing proof.`

USER/ChatGPT Review Checkpoint: `USER approved Stage 2 setup and must separately approve runtime implementation before code changes begin.`

Full Feature Element Breakdown: `Settings cog or entry affordance; settings-panel container; Dashboard control/settings content; visibility/open/close behavior; persistence or state hooks only if USER approves; validation markers and active-client proof for any user-facing runtime changes.`

Current Branch vs Future Package Boundaries: `Current branch may record Branch Readiness setup, PR #133 drift repair, and branch authority. Future Workstream may implement Dashboard settings-panel behavior after USER approval. Future/out-of-scope work includes issue closeout/comments, release execution, raw evidence import/linking, FAM-007 local AI/provider work, provider/model/memory/shortcut/installer work, Workspace Runtime Isolation Stage 2, AI Product Contract import, Private Dev ORIN import, and runtime expansion beyond the Dashboard settings-panel carrier.`

Affected Surfaces: `Docs/feature_backlog.md`; `Docs/prebeta_roadmap.md`; `Docs/branch_records/index.md`; `Docs/branch_records/feature_fam_006_dashboard_release_support.md`; this branch record; future runtime implementation may affect `nexus_visual/monitoring_hud.html`, `nexus_visual/monitoring_hud.css`, `nexus_visual/monitoring_hud.js`, `desktop/desktop_renderer.py`, and HUD validators.

Data/Control Model: `Dashboard remains the user-facing control surface. Settings-panel state should be explicit and local to the Dashboard unless USER approves persistent settings or provider/runtime wiring. Existing release debt and issue-closeout state remain source-truth metadata, not runtime data.`

Branch Reach / Package-Size Review: `This is a focused runtime continuation under already admitted multi-slice PKG-006, with Branch Readiness setup plus later settings-panel implementation. It is not a new FAM or standalone single-slice package.`

Why Branch Is Large Enough: `The branch has a concrete runtime surface, expected HTML/CSS/JS/desktop integration points, validation needs, and source-truth carry-forward from PR #133.`

Why Not Split Into Tiny Branches: `Splitting setup, settings entry, panel UI, and validation into separate branches would recreate source-truth churn and same-file conflict risk across the Dashboard surface.`

Acceptance Criteria: `Branch Readiness acceptance requires clean worktree/branch creation from updated main, active authority setup, PR #133 drift repaired, release debt preserved, issue closeout pending, validation green, commit, and push. Runtime acceptance criteria must be recorded after USER approves implementation.`

Validation Proof Requirements: `Branch Readiness proof requires git identity/status checks, diff checks, branch governance validation, release body validation, and compileall. Runtime proof later must include static/sandbox HUD validators and live/user-facing Dashboard proof if the settings panel changes visible behavior.`

Screenshot / Live / User Test Summary Proof Requirements: `No screenshot/live/UTS proof is required for Branch Readiness source-truth setup. Later settings-panel runtime implementation must define active-client screenshot/live proof and USER visual/UTS expectations or an explicit waiver.`

Implementation Sequence Proposal: `After USER approves Workstream/runtime implementation: inspect current Dashboard settings affordance state; implement the settings entry/panel; add or update validators; run active-client proof; record H1/validation evidence; stop for PR Readiness.`

Planning Blockers: `Runtime Implementation Approval Missing`; `GitHub Issue Closeout Approval Missing`; `Release Execution Approval Missing`; `Raw Evidence Import Decision Pending`; `FAM-007 / Local AI Authority Missing`; `Provider/Model/Memory/Shortcut/Installer Approval Missing`; `AI Product Contract Import Approval Missing`; `PR Creation Approval Missing`.

USER Decisions Needed: `Approve runtime implementation for the settings panel, approve PR creation later, approve GitHub issue closeout/comments, approve release execution/tags/releases/artifacts, approve raw evidence handling, and approve any FAM-007/provider/model/memory/shortcut/installer work separately.`

Planning Packet Status: Complete

Planning Revalidation Status: PASS

User Test Summary Strategy: `No UTS is generated, refreshed, imported, uploaded, linked, or digested by this Branch Readiness pass. Runtime-visible settings-panel implementation must define UTS/live proof expectations before user-facing closeout.`

Planning Completion Waiver: `Not required - this record supplies the Branch Readiness planning packet for the runtime-focused settings-panel carrier.`

## Interface Release Boundary

Interface Release Boundary: `Dashboard settings panel only`

Primary Interface Release Surface: `Monitoring HUD Dashboard settings panel`

Interface Bundle User Approval: `Not granted - this branch has one primary Dashboard settings-panel surface`

Fallback Point: `If settings-panel runtime scope proves larger than the Dashboard surface, stop and request USER decision before expanding into provider/runtime/installer/FAM-007 work.`

Interface Acceptance Path: `Later runtime implementation must define active-client proof and optional USER visual/UTS acceptance for the settings-panel surface.`

## Admitted Implementation Slice

- Slice ID: `SLC-027`
- Goal: `Continue settings and user controls visibility under the already admitted PKG-006 Dashboard package by implementing the Dashboard settings panel after USER approves runtime work.`
- Runtime/User-Facing Delta: `Dashboard settings cog/settings panel visibility and interaction.`
- Exact Affected Paths: `nexus_visual/monitoring_hud.*`; `desktop/desktop_renderer.py` if native visibility routing is needed; HUD Dashboard validators if implementation changes behavior.
- Carried Issues: `None newly created or closed by Branch Readiness setup`; settings-panel runtime work remains a deferred FAM-006 Dashboard control-surface item.
- Non-Includes: `#123`; `#124`; `#125`; `#126`; `#127`; GitHub issue closeout/comments; release execution; raw evidence import/linking; FAM-007/local AI; provider/model/memory/shortcut/installer work; AI Product Contract import; Private Dev ORIN import.
- Implementation Admission Status: `Pending USER approval after Branch Readiness Stage 2.`

## Expected Runtime Surfaces

- `nexus_visual/monitoring_hud.html`
- `nexus_visual/monitoring_hud.css`
- `nexus_visual/monitoring_hud.js`
- `desktop/desktop_renderer.py`
- HUD/dashboard validators if implementation changes require proof hardening.

No runtime source is changed by Branch Readiness Stage 2.

## Backlog Completion Strategy

Branch Completion Goal: `Complete Branch Readiness setup for the FAM-006 Dashboard settings-panel runtime carrier, then await USER decision on runtime implementation.`

Known Future-Dependent Blockers: `Runtime implementation, PR creation, GitHub issue closeout/comments, raw evidence upload/import/linking, release execution, tags, GitHub Releases, artifacts, FAM-007 runtime/admission, AI Product Contract import, Private Dev ORIN import, and runtime/provider/model/memory/shortcut/installer work all require later USER approval.`

Branch Closure Rule: `Stop after validation, commit, and push; do not begin runtime implementation, create a PR, close/comment GitHub issues, release, tag, create artifacts, import/link raw evidence, mutate FAM-007, or perform provider/model/memory/shortcut/installer work without later USER approval.`

## Release Debt And Issue Closeout

Merged-Unreleased Release Debt: `PR #129 FAM-006 Dashboard render/layout hardening` plus `PR #132 FAM-006 Dashboard IA/control follow-through`.

Release Target: `v1.7.1-prebeta`

Release Floor: `patch prerelease`

Issue Closeout Plan: `#123`, `#124`, and `#127` should be closeout-reviewed as completed by PR #129; `#125` and `#126` should be closeout-reviewed as completed by PR #132. Summary-only GitHub comments and issue closure require later USER approval.

Raw Evidence Policy: raw screenshots, videos, and UTS exports remain local/external unless USER later approves upload, import, or linking.

## Multi-Worktree Coordination

USER Waiver: USER confirmed FAM-006 and FAM-007 are assigned to two different worktrees and are not cross-editing repo files in the same worktree.

FAM-006 Assigned Worktree: `C:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard Settings Panel`

FAM-007 Assigned Worktree: `C:\Nexus Worktrees\Nexus Desktop AI FAM-007 Provider Boundary No Provider Shell`

Coordination Rule: FAM-006 work in this branch must stay in the FAM-006 settings-panel worktree and must not edit the FAM-007 worktree. FAM-007 remains separate context only for same-file overlap awareness and merge sequencing.

Same-File Overlap Result: overlap exists in repo-wide source-truth owners such as backlog, roadmap, branch-record index, and governance validators. The USER waiver permits the separate worktrees while requiring each branch to validate, push, and reconcile current main before PR or merge actions.

## Branch Readiness Stage 2 Validation Plan

- `git status --short --branch`
- `git fetch origin --prune`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git branch --all`
- `git worktree list`
- `git diff --check origin/main...HEAD`
- `git diff --name-only origin/main...HEAD`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_release_body_validation.py`
- `python -m compileall -q dev desktop Audio main.py`

## Expected Seam Families And Risk Classes

Seam Families: `Dashboard settings-panel branch readiness`; `PR #133 post-merge source-truth drift repair`; `FAM-006 release-debt preservation`; `multi-worktree coordination`; `future Dashboard settings runtime implementation`.

Risk Classes: `stale active release-support truth`; `runtime implementation before USER approval`; `FAM-007 boundary bleed`; `same-file source-truth overlap`; `release-debt accidental normalization`; `issue-closeout overreach`; `raw evidence over-import`; `provider/model/installer scope creep`.

## User Test Summary Strategy

No User Test Summary is required for this Branch Readiness setup. Later runtime settings-panel implementation must define active-client proof, screenshot/live validation, and USER visual or UTS expectations before closeout, unless USER grants a specific waiver.

## Later-Phase Expectations

- USER may approve runtime implementation for the FAM-006 Dashboard settings panel after this setup is pushed.
- PR creation remains a later USER decision after implementation/validation.
- GitHub issue closeout/comments for #123 through #127 remain pending USER approval.
- Release execution, tags, GitHub Releases, artifacts, and raw evidence handling remain pending USER approval.
- FAM-007 local AI/provider work remains in its own lane and worktree.

## Initial Workstream Seam Sequence

Seam 1: `Dashboard settings-panel inspection and bounded implementation`

Goal: `Implement a deliberate Dashboard settings panel after USER approves runtime Workstream entry.`

Scope: `Dashboard settings entry/panel UI, Dashboard visibility/control routing required for that panel, and supporting HUD validators/proof.`

Non-Includes: `GitHub issue closeout/comments, release execution, tags, GitHub Releases, artifacts, raw evidence upload/import/linking, FAM-007 work, provider/model/memory/shortcut/installer work, AI Product Contract import, Private Dev ORIN import, and runtime expansion beyond the Dashboard settings-panel carrier.`

## Active Seam

Active seam: `Branch Readiness Stage 2 setup for FAM-006 Dashboard settings panel`

Active Seam Status: `Complete when validation, commit, and push succeed`

Next active seam: `Runtime implementation only after USER approval`

## Recorded Seam

Recorded seam: Branch Readiness Stage 2 setup for the FAM-006 Dashboard settings-panel runtime carrier, including PR #133 post-merge source-truth drift repair and active branch authority setup.
