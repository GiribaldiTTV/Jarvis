# Worktree Slots
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-CLEANUP-REBINDING-013; surface=worktree-slot-rebinding-posture; status=canonical -->

## Purpose

`Docs/worktree_slots.md` is the stable slot registry for the Nexus multi-worktree workflow.

It exists to prevent hard-coding temporary family names such as FAM-006 or FAM-007 as permanent lanes. The stable concept is the slot role. The branch, family, and workstream assigned to that slot may change only through USER-approved assignment or retirement.

This document records intended lane assignment and governance pointers. It does not replace Git, GitHub, branch authority records, or live preflight proof.

## Ownership Boundary

This file owns:

- slot IDs and slot roles
- expected path patterns or known standing paths
- intended assignment status
- assigned branch or family/workstream when USER-approved and non-transient
- branch authority record pointer
- Branch Runtime Engineering Plan pointer when a runtime branch requires one
- USER decision pointer or branch authority receipt
- worktree ownership ledger requirements for active thread owner, intended write set, and collision checks
- off-worktree routing and new-worktree decision gate requirements
- last reviewed posture
- where live operational truth must be derived from

This file does not own:

- `HEAD`
- clean or dirty state
- ahead or behind state
- merge base
- remote branch existence
- open, merged, or closed PR state
- current review-thread state
- latest public release
- latest tag
- GitHub issue state

Those facts are derived live truth and must come from Git, GitHub, or approved helpers.

## Derived Live Truth Versus Governance Receipt

Derived live truth is the current operational fact. Examples:

- current `HEAD`
- current `origin/main`
- worktree clean or dirty state
- branch ahead/behind state
- merge-base freshness
- local and remote ref existence
- live PR state and mergeability
- latest GitHub Release and tag truth
- GitHub issue state

Governance receipt is the recorded interpretation or USER decision after live truth is checked. Examples:

- USER assigned a branch to a slot
- USER retired a slot assignment
- a branch authority record admitted a legal phase
- a release scope was accepted as historical interpretation
- a Branch Runtime Engineering Plan was accepted or folded down
- a PR or release result was digested into source truth

Do not copy derived live truth into this file as canonical state. If live truth is needed, run the relevant preflight or helper and report it as evidence.

## Slot Assignment Is Not Branch Authority

Assigned slot does not equal active branch authority.

The branch authority record owns whether a branch is legally active, historical, waiting, blocked, or ready for the next phase. A slot assignment only says which local lane is intended to host that branch or family while the owning branch authority remains valid.

If this document and the branch authority record disagree, stop on identity drift and validate live Git/GitHub truth before mutating files.

## Slot ID Standard

Use these slot IDs for current and future workspace planning:

- `neutral-main`
- `governance-standing`
- `runtime-active-1`
- `runtime-active-2`
- `runtime-active-3`
- `archived-historical`

Do not create permanent slot IDs named after a current feature family. A FAM, package, or branch can be assigned to a runtime slot, but the slot itself remains reusable.

## Slot Field Standard

Each slot assignment or retirement receipt should use these fields when a slot is actively assigned:

- Slot ID:
- Role:
- Expected Path:
- Assignment Status:
- Assigned Branch:
- Assigned Family / Workstream:
- Branch Authority Record:
- Branch Runtime Engineering Plan:
- USER Decision Pointer:
- Active Thread Owner:
- Thread Assignment Status:
- Worktree Ownership Ledger:
- Intended Write Set:
- Same Worktree / Same Branch Collision Check:
- Dirty Worktree Collision Check:
- Dirty Worktree Recovery Packet:
- Off-Worktree Work Routing:
- Governance Routing Barrier:
- New Worktree Decision Gate:
- Last Reviewed Posture:
- Operational Truth Source:

`Operational Truth Source:` should point to Git, GitHub, or an approved helper such as `dev/orin_worktree_rebaseline_audit.py`; it should not manually restate volatile live values.

## Standing Slot Definitions

### neutral-main

- Slot ID: `neutral-main`
- Role: neutral main / consolidator workspace
- Expected Path: `C:\Nexus Desktop AI`
- Assignment Status: standing neutral slot
- Assigned Branch: `main`
- Assigned Family / Workstream: none
- Branch Authority Record: not applicable
- Branch Runtime Engineering Plan: not applicable
- USER Decision Pointer: protected-main governance in `Docs/Main.md`
- Last Reviewed Posture: source edits blocked on `main`; use for truth validation, release review, merge verification, and post-release verification only
- Operational Truth Source: `git status`, `git rev-parse HEAD`, `git rev-parse origin/main`, and Pre-Rebaseline Impact Audit before any fast-forward or branch-state mutation

### governance-standing

- Slot ID: `governance-standing`
- Role: standing governance intake lane
- Expected Path: `C:\Nexus Worktrees\Governance`
- Assignment Status: standing assigned slot
- Assigned Branch: `feature/release-readiness-source-truth-intake`
- Assigned Family / Workstream: Standing Governance Intake Branch
- Branch Authority Record: `Docs/branch_records/feature_release_readiness_source_truth_intake.md`
- Branch Runtime Engineering Plan: not applicable unless a future USER-approved governance runtime plan says otherwise
- USER Decision Pointer: standing governance intake authority record
- Last Reviewed Posture: accepts Release Readiness digest intake, USER-approved automation/worktree governance intake, USER-approved phase-gate governance intake, Governance Routing Barrier packets for off-worktree/out-of-scope work, or same-PR standing-governance bot-review repair only
- Operational Truth Source: `git status`, `git rev-parse HEAD`, `git rev-parse origin/main`, `python dev\orin_branch_governance_validation.py --standing-governance-intake-gate`, and Pre-Rebaseline Impact Audit before sync

## Runtime Slot Definitions

Runtime slots are reusable active-work slots. Their assignment changes as branches complete, merge, retire, or move to historical status.

### runtime-active-1

- Slot ID: `runtime-active-1`
- Role: active runtime/workstream lane
- Expected Path: `C:\Nexus Worktrees\<USER-assigned label>`
- Assignment Status: retired / unassigned after PR #185 merge and USER-approved cleanup
- Assigned Branch: none in merged-main default; historical branch `feature/repo-wide-source-owner-marker-adoption` was merged in PR #185 and deleted locally/remotely after no-unique-commit-loss proof
- Assigned Family / Workstream: none in merged-main default; `Repo-Wide High-Risk Source Owner Marker Adoption` is historical merged evidence
- Branch Authority Record: historical pointer `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`
- Branch Runtime Engineering Plan: historical/folded pointer `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md`
- USER Decision Pointer: USER approved cleanup after PR #185 merge; retired worktree path `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers` was removed after clean-state and ancestor proof
- Last Reviewed Posture: unassigned; no active work, branch authority, PR readiness, or worktree recreation may be inferred from the historical source-owner marker assignment
- Operational Truth Source: Thread / Worktree Identity Preflight, `git worktree list`, `git status`, GitHub PR state, and Pre-Rebaseline Impact Audit

### runtime-active-2

- Slot ID: `runtime-active-2`
- Role: active runtime/workstream lane
- Expected Path: `C:\Nexus Worktrees\FAM-007`
- Assignment Status: FAM-007 consent collection foundation LV1 Green after `v1.7.12-prebeta`; PR Readiness Stage 1 pending USER approval
- Assigned Branch: `feature/fam-007-local-ai-provider-consent-collection-foundation`
- Assigned Family / Workstream: FAM-007 Local AI Provider Consent Collection Foundation
- Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_foundation.md`
- Branch Runtime Engineering Plan: `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_foundation.md`
- USER Decision Pointer: USER-approved FAM-007 Branch Readiness Stage 1 recommendation, Stage 2 setup, Workstream Entry, bounded Workstream implementation, Hardening H1, and Live Validation LV1 for this detailed carrier after PR #192 and `v1.7.12-prebeta`; PR Readiness Stage 1, actual consent collection, provider setup, PR creation, merge, release, cleanup, provider SDK/model work, memory, voice/Core, shortcuts/installers, AI Product Contract import, and v1.8.0-prebeta execution remain pending USER approval
- Active Thread Owner: Codex in `C:\Nexus Worktrees\FAM-007` for localized FAM-007 consent collection foundation Workstream implementation/H1/LV1 proof and next PR Readiness Stage 1 after USER approval
- Thread Assignment Status: LV1 Green; PR Readiness Stage 1 is the next legal phase after USER approval
- Worktree Ownership Ledger: FAM-007 stable runtime worktree, localized to FAM-007 branch work
- Intended Write Set: FAM-007 branch authority/plan, shared source-truth current-branch posture, validation registry, provider state, Core/Desktop renderers, ORIN visual surfaces, FAM-007 provider validator, and no sibling worktrees
- Same Worktree / Same Branch Collision Check: target branch was absent before creation and was created from current `origin/main`
- Dirty Worktree Collision Check: FAM-007 worktree was clean before Stage 2 edits
- Dirty Worktree Recovery Packet: not required for FAM-007; FAM-006 dirt is recorded as later PR/merge reconciliation risk only
- Off-Worktree Work Routing: FAM-006, Governance, and Compact-AI are context only and must not be mutated by this branch
- Governance Routing Barrier: Governance mutation outside this FAM-007 path remains pending USER decision
- New Worktree Decision Gate: no new worktree is required
- Last Reviewed Posture: `v1.7.12-prebeta` is published and release debt is clear; PR #192 is released historical setup implementation foundation evidence, and this slot now carries the consent collection foundation branch from `origin/main` at `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0` with LV1 Green source truth active
- Operational Truth Source: Thread / Worktree Identity Preflight, `git worktree list`, `git status`, GitHub PR state, and Pre-Rebaseline Impact Audit

### runtime-active-3

- Slot ID: `runtime-active-3`
- Role: optional active runtime/workstream lane
- Expected Path: `C:\Nexus Worktrees\<USER-assigned label>`
- Assignment Status: idle unless USER explicitly approves a third active runtime/workstream lane
- Assigned Branch: none in merged-main default
- Assigned Family / Workstream: none in merged-main default
- Branch Authority Record: required when assigned
- Branch Runtime Engineering Plan: required for runtime-focused branches when the Branch Runtime Engineering Plan gate applies
- USER Decision Pointer: required when assigned
- Last Reviewed Posture: adding a third active runtime lane requires explicit USER approval and overlap forecast
- Operational Truth Source: Thread / Worktree Identity Preflight, `git worktree list`, `git status`, GitHub PR state, and Pre-Rebaseline Impact Audit

### archived-historical

- Slot ID: `archived-historical`
- Role: historical or retired workspace trace
- Expected Path: recorded in the branch cleanup or retirement receipt
- Assignment Status: historical only
- Assigned Branch: none unless preserved as historical evidence
- Assigned Family / Workstream: historical evidence only
- Branch Authority Record: historical pointer when one exists
- Branch Runtime Engineering Plan: historical or folded pointer when retained
- USER Decision Pointer: slot retirement or branch cleanup approval
- Last Reviewed Posture: no active work may be inferred from an archived slot
- Operational Truth Source: branch cleanup packet, `git worktree list`, local refs, remote refs, GitHub PR state, and no-unique-commit-loss proof

## Slot Assignment Receipt

When a runtime branch is assigned to a slot, the branch authority record or Branch Readiness Stage 2 packet must record:

- Slot ID:
- Expected Worktree Root:
- Assigned Branch:
- Assigned Family / Workstream:
- Branch Authority Record:
- Branch Runtime Engineering Plan:
- GitHub Desktop-bound worktree:
- Active Thread Owner:
- Thread Assignment Status:
- Worktree Ownership Ledger:
- Intended Write Set:
- Same Worktree / Same Branch Collision Check:
- Dirty Worktree Collision Check:
- Dirty Worktree Recovery Packet:
- Off-Worktree Work Routing:
- Governance Routing Barrier:
- New Worktree Decision Gate:
- USER Assignment Decision:
- Assignment Status:
- Operational Truth Source:

The assignment receipt must be validated by Thread / Worktree Identity Preflight before mutation.

## Active Thread Ownership And Collision Recovery

An assigned slot has exactly one active Codex thread owner for mutation. A second thread may read the slot for audit, but it must not edit, stage, commit, push, merge, rebase, clean, stash, reset, launch runtime validation, or use GitHub Desktop against that slot until USER assigns ownership or grants a bounded waiver.

Same-worktree or same-branch concurrent mutation blocks on `Parallel Worktree Coordination Missing`. Dirty worktree collision recovery is freeze-first: inventory dirty files, identify the owning thread per file, preserve or discard only with USER approval, then resume with one active owner and a validated worktree ownership ledger.

Off-worktree or out-of-scope work blocks on `Governance Routing Barrier`. The assigned thread reports the requested work, expected/actual worktree and branch, dirty-file risk, known owner if any, and recommendation to the standing Governance lane. Governance decides whether the current owner continues, an existing slot owner handles it, a new worktree/thread is needed, or a USER waiver is required. New worktree/thread creation and reassignment remain USER-gated by `New Worktree Decision Gate`.

`Docs/worktree_slots.md` records the slot model and required receipt fields. It does not claim volatile live ownership facts by itself; live owner proof must come from the branch authority record, Branch Runtime Engineering Plan, prompt packet, automation configured cwd, Git/GitHub evidence, or approved helper output at the time of mutation.

## Slot Retirement Receipt

When a branch merges, is abandoned, or becomes historical, the retirement packet must record:

- Slot ID:
- Historical Branch:
- Local Ref State:
- Remote Ref State:
- Merged PR Proof:
- No Unique Commit Loss Proof:
- Worktree Checkout Proof:
- GitHub Desktop Binding Proof:
- Branch Runtime Engineering Plan Fold-Down Status:
- USER Cleanup Approval:
- Validation Proof:

Retirement is not branch deletion by default. Branch deletion, worktree removal, and GitHub Desktop cleanup remain separately USER-gated.

## Branch Runtime Engineering Plan Relationship

For runtime-focused branches, the slot points to the branch authority record, and the branch authority record points to the Branch Runtime Engineering Plan under `Docs/branch_plans/<branch_slug>.md`.

The Branch Runtime Engineering Plan is canonical while the branch is active. PR Readiness must produce a fold-down or retention packet deciding what remains as historical branch source truth, what becomes compact branch receipt, and what is promoted to canonical workstream or family-dossier history.

Backlog and roadmap remain compact pointer/status surfaces. They should not absorb detailed active-branch execution planning.

## Reform Staging

This first slot-model pass is declarative. It defines ownership and intended assignment shape.

Later USER-approved passes may add:

- a derived truth report helper
- a worktree slot audit helper
- drift severity levels: `INFO`, `WARN`, and `BLOCKED`
- hard validator enforcement for slot assignment consistency
- duplicate live-state detector rules
- backlog and roadmap migration/shrink work
- shared surface ownership matrix enforcement

Until those later passes land, this document is a routing and ownership source, not a hard validator replacement.
