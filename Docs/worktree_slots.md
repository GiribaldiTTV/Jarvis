# Worktree Slots
<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-CLEANUP-REBINDING-013; surface=worktree-slot-rebinding-posture; status=canonical -->

## Purpose

`Docs/worktree_slots.md` is the stable slot registry for the Nexus multi-worktree workflow.

Docs Source-Truth Reform Model: Compact Pointer Layer.

It prevents temporary family names such as FAM-006 or FAM-007 from becoming permanent lane concepts. The stable concept is the slot role. The branch, family, and workstream assigned to that slot may change only through USER-approved assignment or retirement.

This document records stable slot definitions and durable assignment receipt schema. Current root routing is owned by `Docs/nexus_workspace_roots.md`. Current worktree assignment, active thread ownership, and live branch/worktree state belong to Git/GitHub/helpers and `D:\Nexus Desktop AI\Governance State` after the approved single-root relocation. Older C paths below are historical receipt examples unless the root map explicitly says otherwise.

## Ownership Boundary

This file owns:

- stable slot IDs and reusable slot roles
- expected path pattern and clearly labeled historical path provenance
- durable assignment receipt status
- branch authority and branch-plan pointer fields for historical receipts
- USER decision pointer field
- worktree ownership/collision-prevention requirements
- off-worktree routing and new-worktree decision gates
- durable Codex App thread/worktree guard policy for slot-bound mutation boundaries

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
- current phase/status, blockers, task/write owner, assignment, locks/leases and next action, which belong exclusively to the matching external operational record
- installed Codex hook configuration, per-thread lock files, waiver files, or hook audit logs

Git and GitHub own their live facts. Current task, phase, assignment, lock and lease state comes from the matching external operational record under the installed Control Plane; repository receipts do not supply an alternative current value.

## Derived Live Truth Versus Governance Receipt

Derived live truth is the current operational fact. Examples include current `HEAD`, current `origin/main`, worktree clean/dirty state, branch ahead/behind state, merge-base freshness, local/remote ref existence, live PR state, latest GitHub Release, tag truth, and issue state.

Governance receipt is the recorded interpretation or USER decision after live truth is checked. Examples include USER assigning a branch to a slot, USER retiring a slot assignment, an accepted admission snapshot whose current operational effect is resolved externally, a release scope being accepted as historical interpretation, or a Branch Runtime Engineering Plan being folded down.

Do not copy derived live truth into this file as canonical state. If live truth is needed, run the relevant preflight or helper and report it as evidence.

## Slot Assignment Is Not Branch Authority

Assigned slot does not equal active branch authority.

The matching external operational record owns whether a branch is currently active, waiting, blocked or ready for the next action, subject to repository product phase contracts and explicit USER approval. A slot assignment only says which local lane is intended to host that branch or family while the owning branch authority remains valid.

If a current assignment conflicts with live identity, stop and reconcile the exact external owner and Git/GitHub evidence before mutation. A clearly historical receipt is not a competing current assignment.

## Slot ID Standard

Use the reusable slot IDs below for USER-approved workspace planning. The historical slot row is provenance only and cannot be selected as a default or fallback:

| Slot ID | Role | Expected Path |
| --- | --- | --- |
| `neutral-main` | neutral main / consolidator workspace | `D:\Nexus Desktop AI\Product Repository` |
| `governance-standing` | historical standing-intake slot; no current assignment | historical path: `D:\Nexus Desktop AI\Worktrees\Governance` |
| `runtime-active-1` | reusable active runtime/workstream lane | `D:\Nexus Desktop AI\Worktrees\<USER-assigned label>` |
| `runtime-active-2` | reusable active runtime/workstream lane | `D:\Nexus Desktop AI\Worktrees\<USER-assigned label>` |
| `runtime-active-3` | optional USER-approved active runtime/workstream lane | `D:\Nexus Desktop AI\Worktrees\<USER-assigned label>` |
| `archived-historical` | historical or retired workspace trace | recorded in retirement receipt |

Do not create permanent slot IDs named after a current feature family. A FAM, package, or branch can be assigned to a runtime slot, but the slot itself remains reusable.

## Standing Slot Receipts

### neutral-main

- Slot ID: `neutral-main`
- Role: neutral main / consolidator workspace
- Expected Path: `D:\Nexus Desktop AI\Product Repository`
- Assignment Status: standing neutral slot
- Assigned Branch: `main`
- Assigned Family / Workstream: none
- Branch Authority Record: not applicable
- Branch Runtime Engineering Plan: not applicable
- USER Decision Pointer: protected-main governance in `Docs/Main.md`
- Operational Truth Source: `git status`, `git rev-parse HEAD`, `git rev-parse origin/main`, and Pre-Rebaseline Impact Audit before any fast-forward or branch-state mutation

### governance-standing — historical receipt

- Historical Slot ID: `governance-standing`
- Historical Role: former standing Governance intake lane
- Historical Path: `D:\Nexus Desktop AI\Worktrees\Governance`
- Assignment Status: retired; no current branch, family or workstream assignment
- Historical Branch: `feature/release-readiness-source-truth-intake`
- Historical Receipt: `Docs/branch_records/feature_release_readiness_source_truth_intake.md`
- Historical Validation Token: `--standing-governance-intake-gate`; not a current prerequisite
- Current Assignment And Routing: the matching external operational owner under `Docs/governance_efficiency_operating_model.md#source-truth-authority-hierarchy`, explicit USER assignment and live Git/GitHub identity
- Preservation: the former physical worktree and branch remain preserved; retirement of the standing assignment grants no deletion, reuse, synchronization or relocation authority

Neither this historical path nor its branch is a fallback for current work.

### runtime-active-1

- Slot ID: `runtime-active-1`
- Role: reusable active runtime/workstream lane
- Expected Path: `D:\Nexus Desktop AI\Worktrees\<USER-assigned label>`
- Assignment Status: external operational state owns the current assignment; repo record keeps reusable slot definition only
- Assigned Branch: see `D:\Nexus Desktop AI\Governance State\worktrees\<worktree_label>\worktree_state.md` and live Git/GitHub/helper truth
- Assigned Family / Workstream: see the matching external operational record when a branch is admitted
- Branch Authority Record: resolved by the matching external operational owner, with repository product/admission receipts as durable evidence
- Branch Runtime Engineering Plan: resolved by the matching external operational owner, with repository product/admission receipts as durable evidence
- GitHub Desktop-bound worktree: USER-gated; validate via live worktree preflight before mutation
- Active Thread Owner: the matching external operational record exclusively owns current thread assignment
- Thread Assignment Status: external operational state owns current assignment status
- Worktree Ownership Ledger: external operational state while active; historical branch records only after fold-down
- Intended Write Set: the matching external operational record owns the current write set under explicit USER authorization
- Same Worktree / Same Branch Collision Check: required before mutation and recorded in the matching external operational record
- Dirty Worktree Collision Check: required before mutation and recorded in the matching external operational record
- Dirty Worktree Recovery Packet: required before future mutation if dirty files appear
- Off-Worktree Work Routing: sibling-worktree requests are context only unless USER assigns a legal carrier
- Governance Routing Barrier: active until USER approves a legal carrier
- New Worktree Decision Gate: pending USER approval for worktree creation, deletion, cleanup, or rebinding
- USER Assignment Decision: current assignment decisions are recorded in the matching external operational record
- Operational Truth Source: `git status`, `git rev-parse HEAD`, `git rev-parse origin/main`, `git merge-base HEAD origin/main`, `git worktree list`, GitHub helpers, and Pre-Rebaseline Impact Audit before mutation

## Runtime Slot Assignment Template

Runtime slot assignments are receipts, not live state.

When a runtime branch is assigned to a slot, the matching external operational record must own the current fields below. The Branch Readiness Stage 2 packet and repository receipt may retain an explicitly identified accepted assignment snapshot; they are not second current owners:

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

Current runtime slot assignment truth must resolve from the matching external operational record under `D:\Nexus Desktop AI\Governance State` and identity preflight. Do not add phase narratives, PR readiness narration, latest release references, commit hashes, selected-next posture, live ownership, or long branch histories to the slot registry.

## Active Thread Ownership And Collision Recovery

An assigned slot has exactly one active Codex thread owner for mutation. A second thread may read the slot for audit, but it must not edit, stage, commit, push, merge, rebase, clean, stash, reset, launch runtime validation, or use GitHub Desktop against that slot until USER assigns ownership or grants a bounded waiver.

Same-worktree or same-branch concurrent mutation blocks on `Parallel Worktree Coordination Missing`. Dirty worktree collision recovery is freeze-first: inventory dirty files, identify the owning thread per file, preserve or discard only with USER approval, then resume with one active owner and a validated worktree ownership ledger.

Off-worktree or out-of-scope work blocks on `Governance Routing Barrier`. The assigned thread reports the requested work, expected/actual worktree and branch, dirty-file risk, known owner if any, and recommendation to the current external operational owner and the relevant product/source owner. Under explicit USER approval, those owners determine whether the current owner continues, an existing slot owner handles it, a new worktree/thread is needed, or a USER waiver is required. New worktree/thread creation and reassignment remain USER-gated by `New Worktree Decision Gate`.

## Codex App Thread Guard Boundary

Slot assignment may be enforced by a USER-local Codex App hook, but the slot registry remains durable policy only. The lock key is the assigned Git root/worktree, not the current branch name. Branch switching or branch creation inside the assigned worktree may be legal when source truth and USER approval allow it; the hook policy must not freeze a valid thread to one branch by itself.

A thread assigned to one slot may inspect sibling worktrees read-only for audit, overlap, rebaseline, or routing analysis. It must not mutate a sibling slot, neutral main, parked fallback, or external operational state by editing files, staging, committing, pushing, merging, rebasing, cleaning, resetting, branch-switching, generating USER packets, writing external records, or running write-capable helpers unless USER grants a bounded `Worktree Escape User Waiver`.

Installed hook state is external/user-local operational state, not repo source truth. Expected local examples include `C:\Users\anden\.codex\hooks.json`, `C:\Users\anden\.codex\hooks\nexus_thread_worktree_guard.ps1`, `C:\Users\anden\.codex\nexus-thread-locks\*.json`, `C:\Users\anden\.codex\nexus-thread-locks\waivers\*.json`, and `C:\Users\anden\.codex\nexus-thread-locks\audit.log`. Repo docs may own the behavior contract and a future USER-approved reference template path only; they must not track live thread locks, current hook installation state, active waivers, or audit-log rows.

## Shared Surface Overlap And Worktree Mutation Boundary

Shared-file overlap across worktrees is legal when each active branch has its own owning-family reason to touch the shared repo surface and overlap is handled by active external branch planning, Branch Change Intent Ledger evidence, Pre-Rebaseline Impact Audit, PR Readiness, merge sequencing, and post-merge reconciliation. Shared overlap is not automatically cross-worktree work.

Worktree-to-worktree mutation is different and remains blocked by default. A thread assigned to one worktree must not edit, stage, commit, rebase, merge, clean, launch owner-only validation from, or otherwise mutate another active worktree or branch unless USER grants a bounded waiver that names the source worktree, target worktree, branch, write set, expiration or stop condition, validation proof, and return path.

This slot registry may define the durable boundary and reusable slot roles, but it must not track live changed-file state, current active assignment, current branch status, PR state, release-window posture, or mutable dependency queues. Those live facts belong to `D:\Nexus Desktop AI\Governance State`, Git/GitHub/helper-derived truth, active external branch plans, USER packets, or Codex digests as routed by source truth.

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

For runtime-focused branches, resolve the current assignment and active Branch Runtime Engineering Plan through the matching external operational owner under `D:\Nexus Desktop AI\Governance State\branches\<branch_slug>\`. Repository branch records supply durable product/admission receipts; repo branch-plan files under `Docs/branch_plans/` are standards or historical receipts, not active slot state.

The Branch Runtime Engineering Plan is canonical while the branch is active. PR Readiness must produce a fold-down or retirement packet deciding what durable content becomes structured branch receipt evidence, what is promoted to canonical workstream or family-dossier history, and when the plan is retired from active planning posture.

Backlog and roadmap remain compact pointer/status surfaces. They should not absorb detailed active-branch execution planning.
