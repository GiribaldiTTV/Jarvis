# Worktree Slots
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-CLEANUP-REBINDING-013; surface=worktree-slot-rebinding-posture; status=canonical -->

## Purpose

`Docs/worktree_slots.md` is the stable slot registry for the Nexus multi-worktree workflow.

Docs Source-Truth Reform Model: Compact Pointer Layer.

It prevents temporary family names such as FAM-006 or FAM-007 from becoming permanent lane concepts. The stable concept is the slot role. The branch, family, and workstream assigned to that slot may change only through USER-approved assignment or retirement.

This document records slot definitions and intended assignment receipts. It does not replace Git, GitHub, branch authority records, Branch Runtime Engineering Plans, or live preflight proof.

## Ownership Boundary

This file owns:

- stable slot IDs and reusable slot roles
- expected path pattern or standing path
- intended assignment status
- branch authority and branch-plan pointer fields
- USER decision pointer field
- worktree ownership/collision-prevention requirements
- off-worktree routing and new-worktree decision gates

This file does not own:

- `HEAD`
- clean or dirty state
- ahead or behind state
- merge base
- remote branch existence
- open, merged, or closed PR state
- review-thread state
- latest public release
- latest tag
- GitHub issue state
- phase status that is owned by a branch authority record

Those facts are derived live truth and must come from Git, GitHub, or approved helpers.

## Derived Live Truth Versus Governance Receipt

Derived live truth is the current operational fact. Examples include current `HEAD`, current `origin/main`, worktree clean/dirty state, branch ahead/behind state, merge-base freshness, local/remote ref existence, live PR state, latest GitHub Release, tag truth, and issue state.

Governance receipt is the recorded interpretation or USER decision after live truth is checked. Examples include USER assigning a branch to a slot, USER retiring a slot assignment, a branch authority record admitting a legal phase, a release scope being accepted as historical interpretation, or a Branch Runtime Engineering Plan being folded down.

Do not copy derived live truth into this file as canonical state. If live truth is needed, run the relevant preflight or helper and report it as evidence.

## Slot Assignment Is Not Branch Authority

Assigned slot does not equal active branch authority.

The branch authority record owns whether a branch is legally active, historical, waiting, blocked, or ready for the next phase. A slot assignment only says which local lane is intended to host that branch or family while the owning branch authority remains valid.

If this document and the branch authority record disagree, stop on identity drift and validate live Git/GitHub truth before mutating files.

## Slot ID Standard

Use these slot IDs for current and future workspace planning:

| Slot ID | Role | Expected Path |
| --- | --- | --- |
| `neutral-main` | neutral main / consolidator workspace | `C:\Nexus Desktop AI` |
| `governance-standing` | standing governance intake lane | `C:\Nexus Worktrees\Governance` |
| `runtime-active-1` | reusable active runtime/workstream lane | `C:\Nexus Worktrees\<USER-assigned label>` |
| `runtime-active-2` | reusable active runtime/workstream lane | `C:\Nexus Worktrees\<USER-assigned label>` |
| `runtime-active-3` | optional USER-approved active runtime/workstream lane | `C:\Nexus Worktrees\<USER-assigned label>` |
| `archived-historical` | historical or retired workspace trace | recorded in retirement receipt |

Do not create permanent slot IDs named after a current feature family. A FAM, package, or branch can be assigned to a runtime slot, but the slot itself remains reusable.

## Standing Slot Receipts

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
- Operational Truth Source: `git status`, `git rev-parse HEAD`, `git rev-parse origin/main`, `python dev\orin_branch_governance_validation.py --standing-governance-intake-gate`, and Pre-Rebaseline Impact Audit before sync

### runtime-active-1

- Slot ID: `runtime-active-1`
- Role: reusable active runtime/workstream lane
- Expected Path: `C:\Nexus Worktrees\FAM-007`
- Assignment Status: Historical merged-unreleased after PR #201; slot waits for USER-approved rebaseline and later Branch Readiness before any successor work
- Assigned Branch: `None active - prior branch feature/fam-007-local-ai-provider-consent-collection-implementation-foundation merged through PR #201`
- Assigned Family / Workstream: `FAM-007 Local AI Provider Consent Collection Implementation Foundation - historical merged-unreleased PR #201 evidence`
- Branch Authority Record: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
- Branch Runtime Engineering Plan: `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md` retired from active planning posture after PR #201
- GitHub Desktop-bound worktree: `Preserve C:\Nexus Worktrees\FAM-007 binding; no cleanup/rebinding authorized by this branch`
- Active Thread Owner: `None active after PR #201 merge; future FAM-007 work requires USER-approved Branch Readiness`
- Thread Assignment Status: `Waiting for updated main / future USER-approved Branch Readiness`
- Worktree Ownership Ledger: `Branch authority record plus this slot receipt`
- Intended Write Set: `None while idle after PR #201 merge; release, provider setup completion, model execution, downloads/network, memory, voice/Core sync, cleanup, successor branch creation, and sibling-worktree mutation remain pending USER decisions`
- Same Worktree / Same Branch Collision Check: `PASS at assignment; no second writer assigned`
- Dirty Worktree Collision Check: `PASS at assignment; worktree clean before Stage 2 source-truth edits`
- Dirty Worktree Recovery Packet: `Not required unless unowned dirty files appear`
- Off-Worktree Work Routing: `Route FAM-006, Governance, Compact-AI, neutral-main, and parked-worktree mutation requests to owning lanes`
- Governance Routing Barrier: `Active for governance-only mutation outside this FAM-007 branch path`
- New Worktree Decision Gate: `Pending USER approval for any worktree creation, deletion, cleanup, or rebinding beyond this carrier`
- USER Assignment Decision: `USER approved Branch Readiness Stage 2 setup, Workstream implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 in C:\Nexus Worktrees\FAM-007 for this target branch`
- Operational Truth Source: `git status`, `git rev-parse HEAD`, `git rev-parse origin/main`, `git merge-base HEAD origin/main`, and Pre-Rebaseline Impact Audit before any future baseline mutation`

## Runtime Slot Assignment Template

Runtime slot assignments are receipts, not live state.

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

Current runtime slot assignment truth should be resolved from the active branch authority record and identity preflight, then mirrored here only as a compact assignment receipt when USER-approved. Do not add phase narratives, PR readiness narration, latest release references, commit hashes, or long branch histories to the slot registry.

## Active Thread Ownership And Collision Recovery

An assigned slot has exactly one active Codex thread owner for mutation. A second thread may read the slot for audit, but it must not edit, stage, commit, push, merge, rebase, clean, stash, reset, launch runtime validation, or use GitHub Desktop against that slot until USER assigns ownership or grants a bounded waiver.

Same-worktree or same-branch concurrent mutation blocks on `Parallel Worktree Coordination Missing`. Dirty worktree collision recovery is freeze-first: inventory dirty files, identify the owning thread per file, preserve or discard only with USER approval, then resume with one active owner and a validated worktree ownership ledger.

Off-worktree or out-of-scope work blocks on `Governance Routing Barrier`. The assigned thread reports the requested work, expected/actual worktree and branch, dirty-file risk, known owner if any, and recommendation to the standing Governance lane. Governance decides whether the current owner continues, an existing slot owner handles it, a new worktree/thread is needed, or a USER waiver is required. New worktree/thread creation and reassignment remain USER-gated by `New Worktree Decision Gate`.

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

The Branch Runtime Engineering Plan is canonical while the branch is active. PR Readiness must produce a fold-down or retirement packet deciding what durable content becomes structured branch receipt evidence, what is promoted to canonical workstream or family-dossier history, and when the plan is retired from active planning posture.

Backlog and roadmap remain compact pointer/status surfaces. They should not absorb detailed active-branch execution planning.
