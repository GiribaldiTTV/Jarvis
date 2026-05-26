# External Operational State Store / Release Debt Abolition Reform Plan
## Purpose

This planning reference preserves the agreed External Operational State Store / Release Debt Abolition reform so future Governance branch work can implement it without losing scope, sequencing, safeguards, or USER decisions.

This file is a planning reference, not an active external-state migration, helper implementation, validator implementation, or release-unblocker by itself. Binding source-truth rules live in `Docs/governance_efficiency_operating_model.md`, `Docs/phase_governance.md`, and their routed governance owners.

## Current Approved Sequencing

1. Clear the current PR #220 / FAM-007 post-merge source-truth blocker under existing repo rules.
2. Stop at PR Readiness Stage 1 for this Governance repair unless USER separately approves PR Readiness Stage 2 / PR creation.
3. Hold while FAM-007 is paused and FAM-006 finishes its current branch.
4. After FAM-006 PR and merge, rebaseline and reconcile neutral main, Governance, FAM-006, and FAM-007.
5. After all worktrees are neutral, reconciled, and current, begin implementation of the External Operational State Store reform as a new USER-approved phase.

## Current Boundaries

Approved now:

- docs-only source-truth contract work
- durable planning record creation
- current FAM-007 PR #220 blocker repair under existing rules
- validation and PR Readiness Stage 1 analysis

Not approved by this planning file:

- helper code creation
- validator code creation or transition
- external folder creation
- worktree-local staging folder creation
- external state migration
- file moves, deletion, or archive execution
- PR creation
- merge
- release execution
- runtime work
- FAM-006, FAM-007, or Compact-AI mutation outside approved carrier scope
- issue work
- branch cleanup
- backup setup
- private repo creation

## Problem Statement

Release Readiness keeps blocking on stale live operational state in repo-tracked Docs after branches merge. Recent examples include:

- branch records remaining listed as active after PR merge
- active branch plans remaining current after their owning branch merges
- roadmap or backlog text carrying selected-next or "no branch exists" posture after live Git truth changes
- worktree slots describing a branch as active after it merges
- release-window and post-release closure state dirtying repo Docs and forcing Governance repair PRs before releases

These are operational coordination problems, not durable public release truth problems. They should not repeatedly require repo PRs when the underlying product, release tag, GitHub Release, and runtime source are already correct.

## Core Split

Repo durable source truth:

- governance laws and phase rules
- development and Codex mode rules
- source-truth ownership and loader routes
- Nexus vision and family visions
- validator/helper registry
- release body and public output standards
- public-safe architecture and durable product direction
- durable folded receipts after USER approval

External operational state:

- active branch state
- active branch plans
- Workstream Entry review packets
- USER Feedback Disposition while active
- Branch Change Intent Ledger while active
- Element-to-Phase Proof Matrix while active
- current worktree assignment
- release-window assembly
- PR watcher and live PR state snapshots
- USER review bundle manifests
- rebaseline audit packets
- temporary Codex handoff digests
- fold-down previews
- cross-worktree lessons
- governance candidates
- state promotion packets
- worktree acknowledgement records

Derived live truth from Git, GitHub, and helpers:

- `HEAD`
- `origin/main`
- merge base
- dirty state
- ahead/behind
- remote branch existence
- open, merged, or closed PR state
- review-thread state
- issue state
- latest tag
- latest GitHub Release
- release body truth

## Canonical Location Model

Canonical external operational state root:

```text
C:\Nexus Governance State
```

Optional worktree-local proposed staging:

```text
<worktree>\.nexus_state_staging\
```

Invalid as canonical operational state unless USER grants a one-off migration waiver:

- repo-root `.nexus_state`
- repo-root `.nexus_local_state`
- repo-root `.nexus_state_staging`
- any folder inside a Git worktree

Repo-root ignored folders may be staging, scratch, or defensive guard paths only. They must not become canonical shared operational truth.

## Proposed External State Layout

```text
C:\Nexus Governance State\README.md
C:\Nexus Governance State\state_index.md
C:\Nexus Governance State\state_manifest.json
C:\Nexus Governance State\schemas\
C:\Nexus Governance State\locks\
C:\Nexus Governance State\central\
C:\Nexus Governance State\worktrees\Governance\
C:\Nexus Governance State\worktrees\FAM-006\
C:\Nexus Governance State\worktrees\FAM-007\
C:\Nexus Governance State\branches\<branch_slug>\
C:\Nexus Governance State\release_windows\<release_slug>\
C:\Nexus Governance State\review_bundles\<worktree_label>\
C:\Nexus Governance State\cross_worktree_lessons\
C:\Nexus Governance State\governance_candidates\
C:\Nexus Governance State\promotion_packets\
C:\Nexus Governance State\acknowledgements\
C:\Nexus Governance State\snapshots\
C:\Nexus Governance State\audit_log\
```

Generated global indexes such as `state_index.md` are reports, not primary state. Primary state lives in branch, worktree, release-window, candidate, promotion, acknowledgement, and fold-down records.

## Proposed Branch State Layout

```text
branch_state.md
branch_plan.md
branch_plan_review.md
ufd_ledger.md
change_intent_ledger.md
element_to_phase_matrix.md
workstream_entry_review.md
hardening_plan.md
live_validation_plan.md
pr_readiness_state.md
fold_down_preview.md
```

## Deterministic Governance Language Contract

Binding external-state rules must use deterministic rule language. Recommendation or planning prose may use softer wording only when explicitly labeled `Non-Binding Planning`.

Every binding rule that controls ownership, mutation, locks, promotion, fold-down, Release Readiness, cross-worktree reconciliation, source-truth ownership, or validator blocking must include:

- Rule Name
- Owner
- Applies To
- Required State
- Allowed Values
- Invalid Values
- Blocking Condition
- Repair Owner
- Repair Path
- USER Decision Required
- Validation Owner
- Final Disposition

Required state models:

- External State Item Status: `Active`, `Queued`, `Promotion Pending`, `Promoted`, `Fold-Down Pending`, `Folded`, `Archived`, `Expired`, `Rejected`, `USER Decision Required`
- Worktree Acknowledgement State: `Pending`, `Accepted`, `Conflict`, `Not Applicable`
- Lock State: `Unlocked`, `Locked`, `Expired`, `Stale`, `Conflict`, `Released`, `Recovery Required`
- Promotion Result: `Approved`, `Rejected`, `Blocked`, `Superseded`, `Folded Into Repo`, `External Only`, `USER Decision Required`
- Release Readiness Live-State Result: `Clear`, `External Operational State Conflict`, `Repo Live-State Leakage`, `Durable Release Truth Defect`, `USER Decision Required`

Required named blockers:

- `External State Lock Missing`
- `External State Version Conflict`
- `External State Owner Conflict`
- `External State Promotion Missing`
- `Governance Candidate Not Promoted`
- `Cross-Worktree Acknowledgement Missing`
- `Repo Live-State Leakage`
- `Fold-Down Decision Missing`
- `Release Debt Misclassified`
- `External State Missing`
- `External State Corrupt`
- `External State Schema Conflict`
- `Stale Lock Recovery Required`

## CI And Clean Clone Boundary

Repo validators running in GitHub Actions or clean clones validate durable repo truth only. They must not require access to `C:\Nexus Governance State`.

Local governance validators may require external state only for:

- active local workflow
- Release Readiness analysis
- worktree coordination
- external-state migration
- external-state validation
- lock, snapshot, or recovery workflows

If external state is unavailable in CI, the result is not a repo failure unless repo docs contain live-state leakage.

## Bootstrap Rule

If external state is missing during active local workflow, Codex returns `External State Missing`.

The bootstrap packet must include:

- desired root: `C:\Nexus Governance State`
- worktree label
- source repo path
- branch
- source repo HEAD
- schema version
- initialization scope
- exact USER decision needed

Expected future helper command:

```powershell
python dev\orin_external_state_init.py --root "C:\Nexus Governance State" --worktree "<label>" --repo "<repo_path>" --schema <schema_version>
```

Until USER approves initialization, active operational workflow waits. Analysis-only work may continue only with an explicit analysis-only waiver.

## Schema Migration Rule

Every external state file must name:

- External State Schema
- State Version
- Last Updated
- Last Updated By
- Worktree
- Branch
- Source Repo HEAD

Schema changes require:

- migration packet
- snapshot
- validation
- USER decision
- audit log entry

Mixed or unsupported schema versions return `External State Schema Conflict`.

## Multi-Worktree Concurrency Contract

State ownership partitions:

- branch state
- worktree state
- release-window state
- review-bundle state
- fold-down state
- generated global index state
- cross-worktree lessons
- governance candidates
- promotion packets

Lock scopes:

- state root lock
- migration lock
- release-window lock
- worktree lock
- branch lock
- review-bundle lock
- fold-down lock
- governance-candidate lock

Lock acquisition order:

1. migration
2. release window
3. worktree
4. branch
5. review bundle
6. fold-down
7. governance candidate

Read/write modes:

- read-only
- write
- migration
- fold-down
- recovery

Required state-file version fields:

- State Version
- Last Updated
- Last Updated By
- Worktree
- Branch
- Source Repo HEAD
- External State Schema

Helper behavior expected in implementation:

- detect state version changes between read and write
- return `External State Version Conflict` on changed versions
- write temp file
- validate temp file
- replace atomically
- append audit log
- release lock

Release-window single-writer rule:

- only the active Release Readiness carrier may hold the release-window write lock
- other workstreams may read release-window state

## Stale-Lock Recovery

Stale-lock recovery requires a recovery packet with:

- stale lock ID
- lock owner
- intended write set
- last state version
- current state version
- recovery risk
- exact USER decision needed

Stale lock recovery must not discard or overwrite state when ownership or version risk is unclear.

## Cross-Worktree Lessons

Proposed path:

```text
C:\Nexus Governance State\cross_worktree_lessons\
```

Each lesson record includes:

- Lesson ID
- Origin Worktree
- Origin Branch
- Issue / Failure
- Affected Surfaces
- Affected Worktrees
- Recommended Rule Change
- Recommended Owner
- Severity
- Current Disposition
- Promotion Target
- USER Decision Needed

Allowed dispositions:

- `Local Only`
- `Share As Warning`
- `Governance Candidate`
- `Validator Candidate`
- `Family Vision Candidate`
- `Branch-Plan Template Candidate`
- `Folded Into Repo Source Truth`
- `Rejected / No Action`
- `USER Decision Required`

## Governance Candidates

Proposed path:

```text
C:\Nexus Governance State\governance_candidates\
```

Each governance candidate includes:

- Candidate ID
- Origin Worktree
- Origin Branch
- Proposed Rule
- Reason
- Affected Worktrees
- Affected Source-Truth Owners
- Proposed Repo Owner File
- Validator Impact
- Risk
- USER Decision Needed
- Current Disposition

External governance candidates are not binding governance. They become governing only after USER-approved repo source-truth update and merge.

## State Promotion Packet

Each packet includes:

- Source State
- Target State
- Proposed Change
- Reason
- Affected Worktrees
- Conflict Scan
- Validation Required
- USER Decision Needed
- Final Disposition

Promotion from worktree staging to central state requires:

- lock acquisition
- central state version check
- conflict scan
- validation
- snapshot when risk warrants it
- audit log
- USER decision when shared state, release-window state, selected-next posture, branch authority, fold-down, or cross-worktree lesson state is affected

Promotion does not delete staging source by default. Promotion updates central state, records final disposition, writes the audit log, and preserves staging source until the promotion result exists. Staging may expire or archive only after promotion result and audit log exist.

## Worktree Acknowledgement After Governance Merge

Active worktrees need acknowledgement records after merged governance/source-truth changes that affect:

- phase rules
- branch plan rules
- validator behavior
- source-truth ownership
- Release Readiness
- review bundles
- external state schema
- worktree slots
- any active branch implementation or proof path

Allowed acknowledgement states:

- `Pending`
- `Accepted`
- `Conflict`
- `Not Applicable`

Acknowledgement conflicts return one of:

- rebaseline packet
- branch-plan revision packet
- external state promotion packet
- USER decision packet

## Release Debt Redefinition

Release debt means durable public release truth is missing or wrong.

Examples of true release debt:

- published release tag/body/release notes wrong
- invalid or missing release artifact
- missing durable public milestone summary
- released capability absent from durable product history

These become external operational state updates or repo live-state leakage findings:

- branch record still active
- branch plan still active
- worktree slot stale
- selected-next stale
- PR watcher stale
- release-window operational state stale
- post-release closure state pending

## Release Readiness Post-Reform

Release Readiness reads:

1. Git/GitHub/helper truth: latest tag, latest release, release body, candidate commit, PR merge state.
2. External Governance State: active branch posture, branch fold-down state, release-window assembly, worktree assignment, review bundle state, carry-forward blockers, unresolved cross-worktree lessons, unresolved governance candidates.
3. Repo durable docs: product vision, governance contracts, family direction, durable release milestone posture, folded historical receipts.
4. Repo live-state leakage scan: active branch fields in repo, active worktree assignment in repo, PR/watcher state in repo, release-window assembly in repo, selected-next operational posture in repo.

Release Readiness blocks on:

- `Durable Release Truth Defect`
- `External Operational State Conflict`
- `Repo Live-State Leakage`
- `Governance Candidate Not Promoted` when it affects durable release truth, public safety, validator correctness, or source-truth ownership
- `USER Decision Required`

Release Readiness remains repo-file-frozen. External Governance State may be read during Release Readiness after USER-approved initialization. External state mutation during Release Readiness requires explicit USER approval and is limited to operational release-window state or approved external operational state reconciliation.

## Review Bundle Integration

USER review bundles should be able to include external state files when USER review needs them.

External state is local-private by default. Private, Owner, or DEV-sensitive state requires sanitization and USER approval before upload, zip export, public PR attachment, or cloud backup.

## Backup And Snapshot Model

Snapshots are expected before:

- external-state migration
- Release Readiness pass
- branch-plan fold-down
- lock recovery
- high-risk schema migration

Optional daily snapshots may be used during heavy work after USER approval.

Snapshot manifests include:

- schema version
- timestamp
- source root
- checksum
- changed state files

External state must not contain plaintext secrets, tokens, cookies, provider keys, private model files, or owner-private memory unless a later encrypted Owner vault is approved.

## Migration Stages

1. Clear current post-merge source-truth blockers under existing repo rules.
2. Land docs-only source-truth contract for repo durable truth, external operational state, deterministic language, and concurrency model.
3. Implement helper scaffolds: init, report, lock, validate, snapshot, fold-down preview, promotion preview, and promote.
4. Adopt external state for new or re-entering branches.
5. Adopt ignored worktree staging for proposed state only.
6. Migrate active branch, worktree, and release-window state out of repo docs.
7. Transition validators: repo validators stop requiring live state in repo docs; external validators check operational state.
8. Clean repo docs: remove stale live-state fields and keep durable receipts only.
9. Transition Release Readiness to Git/GitHub truth plus external state plus repo durable truth.
10. Require active worktree acknowledgements after merged governance/source-truth changes.

## Risks And Mitigations

Shadow governance:

- External candidates are non-binding until folded into repo source truth by USER-approved update and merge.

Clean clone breakage:

- CI validates durable repo truth only and must not require `C:\Nexus Governance State`.

External state loss:

- Use snapshots, audit logs, schema validation, and no-loss promotion.

Multi-worktree corruption:

- Use lock scopes, version checks, acknowledgement records, and atomic writes.

Stale generated indexes:

- Treat indexes as generated reports only; primary state lives in records.

Release delay:

- Current PR #220 is handled under existing rules unless USER explicitly pauses release flow and approves external-state implementation as the unblocker.

## Immediate PR #220 Recommendation

Default path:

1. Clear PR #220 under existing rules.
2. Rerun Release Readiness.
3. Then begin external-state reform.

External-state implementation does not become the immediate release unblocker unless USER explicitly pauses release flow and approves that route.

## Future Exact USER Decision Shape

Approve the next implementation phase only after FAM-006 and FAM-007 are reconciled and neutral:

```text
Approve External Operational State Store implementation on C:\Nexus Worktrees\Governance after all worktrees are reconciled and neutral. Scope: implement helper scaffolds, external-state bootstrap, lock/version/schema validation, snapshot/audit support, state promotion packets, review-bundle integration, and validator transition according to Docs/external_operational_state_store_reform_plan.md and Docs/governance_efficiency_operating_model.md. Do not migrate active state, delete repo files, archive branch plans, mutate runtime, create releases, clean branches/worktrees, or change FAM-006/FAM-007 without separate USER approval.
```
