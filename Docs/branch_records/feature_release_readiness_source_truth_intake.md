# Branch Authority Record: feature/release-readiness-source-truth-intake

## Branch Identity

- Branch: `feature/release-readiness-source-truth-intake`
- Workstream: `Standing Governance Intake Branch`
- Branch Class: `standing governance intake`
- Worktree: `C:\Nexus Worktrees\Governance`
- Cycle ID Format: `RRI-YYYYMMDD-NNN`

## Purpose / Why It Exists

This branch is the single standing governance lane for Release Readiness source-truth drift intake. It exists so Release Readiness can remain file-frozen while preventable post-merge source-truth blockers are repaired through a short PR cycle on a dedicated worktree instead of direct-main mutation, an ad hoc cleanup branch, or an implementation worktree that should stay isolated.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Branch Authority Marker: `Active Branch`
- Branch Authority State: `standing governance intake lane`
- Intake State: `Idle - no active Release Readiness intake cycle is recorded in merged source truth`
- Bootstrap Setup: `RRI-20260514-001 records the one-time USER-approved exception that creates C:\Nexus Worktrees\Governance and the standing branch from origin/main; this record is written in merge-stable idle posture so the branch must sync to origin/main after the setup PR merges before accepting any Release Readiness digest`
- Active RRI Cycle: `None`

## Branch Class

- `standing governance intake`

## Blockers

- `Release Readiness Digest Missing`: `Active until a Release Readiness blocker packet is handed to this lane`
- `Standing Governance Intake Not Rebased`: `Active whenever the branch is not clean and equal to origin/main before a new intake`
- `Multiple Intake Cycles Blocked`: `Active for any second RRI cycle until the first cycle merges, returns its digest, and the branch syncs to origin/main`
- `Governance PR Merge User Approval Missing`: `Active until USER approves each cycle merge`
- `Runtime Scope Blocked`: `Active always; this branch cannot carry runtime/provider/model/memory/voice/Core/shortcut/installer work`
- `Release Execution Blocked`: `Active always; this branch cannot tag, publish GitHub Releases, generate release artifacts, or execute release work`

## Entry Basis

- USER approved Branch Readiness Stage 2 execution for a permanent governance worktree and branch.
- Worktree created at `C:\Nexus Worktrees\Governance`.
- Branch created from `origin/main` at `926c7c90880419830be99611d741c6bac51252de`.
- Standing branch name is fixed as `feature/release-readiness-source-truth-intake`.

## Standing Governance Intake Contract

- Standing Branch: `feature/release-readiness-source-truth-intake`
- Worktree: `C:\Nexus Worktrees\Governance`
- Intake Source: Release Readiness digest only; bootstrap setup is the one-time USER-approved exception recorded by RRI-20260514-001.
- Cycle ID Format: `RRI-YYYYMMDD-NNN`
- Active RRI Cycle: `None`
- One Active Cycle: Required - a second digest queues until the active cycle merges, returns its digest, and the branch syncs to origin/main.
- Sync Rule: Before each new intake the branch must be clean and match origin/main; otherwise `Standing Governance Intake Not Rebased` blocks work.
- Return Digest: Required after governance PR merge and branch sync.
- Originating Lane Pause: Required - the originating thread/worktree enters `Waiting For Governance Intake` or `Waiting For Updated Main` and must not mutate until return digest and rebaseline.

## Allowed / Forbidden Scope

Allowed:

- Release Readiness digest source-truth drift repair only.
- Governance/source-truth wording that prevents Release Readiness from becoming a cleanup phase.
- Governance/source-truth wording that routes stale/old branch cleanup to Branch Readiness branch/worktree setup instead of Release Readiness.
- Validator support for standing intake, Release Readiness Health Pass, and PR body firewall behavior.
- Helper registry updates tied directly to those validators.
- One PR per active `RRI-*` cycle after validation.

Forbidden:

- Runtime/provider/model/memory/voice/Core/shortcut/installer implementation.
- Release execution, tags, GitHub Releases, release artifacts, or release-note publication.
- Stale branch deletion, worktree removal, branch switching, or GitHub Desktop-bound worktree cleanup during Release Readiness.
- GitHub issue creation or issue-resolution branch work.
- AI Product Contract import or private Dev ORIN import.
- Direct-main mutation, broad docs churn, implementation branch planning, or selected-next runtime branch creation.
- Accepting anything other than a Release Readiness digest after the bootstrap setup cycle.

## Return Digest Contract

After the governance PR merges and the standing branch syncs back to `origin/main`, the governance thread must output a return digest to the originating worktree/thread with:

- Originating Branch:
- Originating Worktree:
- RRI Cycle ID:
- Governance PR:
- Merge Commit:
- Updated origin/main:
- Files Changed:
- Blockers Cleared:
- Blockers Remaining:
- Validations:
- Rebaseline Instructions:
- Next Legal Phase:

The originating lane remains paused in `Waiting For Governance Intake` or `Waiting For Updated Main` until this digest is received, `origin/main` is fetched, source truth is revalidated, and the phase resolver reports the next legal phase.

## PR Body Firewall

GitHub PR bodies for this branch must stay evidence-only. They must use the standard `## Summary`, `## Branch Evidence`, and `## Validation` sections and must not include Codex phase-handoff/operator text such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, `Exact next USER decision`, `Implemented, validated`, or `::git-*`.

## Branch Objective

Bootstrap and preserve the one legal standing governance intake lane so Release Readiness drift can be repaired without dirtying FAM-006, FAM-007, `main`, or future runtime worktrees.

## Target End-State

The setup PR merges, the standing branch is synced to current `origin/main`, no active `RRI-*` cycle remains recorded, GitHub Desktop can open `C:\Nexus Worktrees\Governance`, and the lane waits cleanly for the next Release Readiness digest.

## Backlog Completion Strategy

Branch Completion Goal: `Standing intake lane bootstrapped and validated`

Known Future-Dependent Blockers: `Future RRI cycles require a Release Readiness digest, clean sync to origin/main, USER-gated PR merge, and return digest before originating-lane continuation`

Branch Closure Rule: `The standing branch name persists after merge; each intake cycle closes by PR merge, sync to origin/main, return digest, and Active RRI Cycle returning to None`

## Expected Seam Families And Risk Classes

- Governance scope risk: keep the exception narrow so it does not reopen governance-only branches by default.
- Source-truth projection risk: ensure future Release Readiness blockers are routed before they become main repair work.
- Validator risk: keep standing-intake checks focused on branch identity, cycle count, sync posture, file scope, and return-digest markers.
- GitHub Desktop handoff risk: Desktop must point at `C:\Nexus Worktrees\Governance` when the USER operates this lane.

## User Test Summary Strategy

No runtime User Test Summary is required. Operator validation is repo-side: `git worktree list`, GitHub Desktop folder binding, governance validators, PR body audit, release body validator, and compile checks.

## Later-Phase Expectations

- Workstream: Not applicable unless a later USER-approved validator hardening seam is needed inside this same non-runtime branch class.
- Hardening: Optional repo-side hardening only if validation exposes a validator or source-truth defect in the standing-lane contract.
- Live Validation: Not applicable for runtime UI.
- PR Readiness: Open one governance PR for bootstrap or for one active `RRI-*` cycle after validation.
- Release Readiness: File-frozen validation only; it may produce future intake digests but must not mutate files.

## Initial Workstream Seam Sequence

Seam 1: Standing Governance Intake Bootstrap

Goal: Create the durable branch authority record, governance docs, validator gate, PR body firewall, and helper registry truth for the standing lane.

Scope: `Docs/branch_records/index.md`, this branch authority record, governance/source-truth docs, `dev/orin_branch_governance_validation.py`, `dev/orin_pr_body_quality_audit.py`, and `Docs/validation_helper_registry.md`.

Non-Includes: runtime implementation, provider/model/memory/voice/Core/shortcut/installer changes, release execution, GitHub issues, AI Product Contract import, private Dev ORIN import, next runtime branch creation, or actual stale branch/worktree cleanup.

## Active Seam

- Active seam: `Standing Governance Intake Bootstrap`
- Status: `Merge-stable bootstrap posture - after setup PR merge, the standing lane idles with Active RRI Cycle: None until a Release Readiness digest is handed off`

## Exit Criteria

- `Docs/branch_records/index.md` lists this record under Active Branch Authority Records.
- Governance docs describe the standing exception, allowed/forbidden scope, one-cycle limit, sync-to-main rule, originating-lane pause, and return digest.
- `dev/orin_branch_governance_validation.py --standing-governance-intake-gate` validates the branch identity, clean tracked state, source-truth markers, cycle count, sync/base posture, and file scope.
- `dev/orin_pr_body_quality_audit.py` rejects PR body firewall markers.
- The setup PR is opened from `feature/release-readiness-source-truth-intake` and remains USER-gated for merge.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Branch Readiness`
