# External Operational State Store / Release Debt Abolition Reform Plan
## Purpose

This planning reference preserves the agreed External Operational State Store / Release Debt Abolition reform so future Governance branch work can implement it without losing scope, sequencing, safeguards, or USER decisions.

This file is a planning reference, not an active external-state migration, helper implementation, validator implementation, or release-unblocker by itself. Binding source-truth rules live in `Docs/governance_efficiency_operating_model.md`, `Docs/phase_governance.md`, and their routed governance owners.

## Current Approved Sequencing

1. PR #220 / FAM-007 post-merge source-truth repair is historical and released through `v1.7.23-prebeta`.
2. PR #222 / FAM-006 Active Overlay Recording Runtime Foundation planning receipt merged without runtime implementation and is included in `v1.7.25-prebeta`.
3. PR #223 folded PR #222 into historical source truth, and PR #224 hardened PR body drift checks; both are included in `v1.7.25-prebeta`.
4. Docs Split Stage 0 landed through PR #225 and recorded the migration plan, split inventory expectations, and transition drift gate while preserving repo docs as durable source truth.
5. Docs Split Stage 1 landed through PR #226 and added report-only helper/bootstrap scaffolding.
6. Stage 2 initialized `C:\Nexus Governance State` after separate USER approval; that local root initialization did not migrate active state or transition repo validators.
7. Stage 3 recorded a no-mutation migration preview packet in external state after separate USER approval.
8. Current posture is Stage 4A: report-only repo live-state leakage scanner and migration-map helper support.
9. Stop at PR Readiness Stage 1 for this Governance repair unless USER separately approves PR Readiness Stage 2 / PR creation.
10. Active-state migration, repo Docs file movement, repo cleanup, and validator transition remain future USER decisions after the Stage 4A helper output is reviewed.

## Current Boundaries

Approved now:

- Stage 4A report-only repo live-state leakage scanner helper under `dev/`
- durable planning record updates for the Stage 4A boundary
- helper registry updates for the scanner helper
- report-only migration-map helper smoke validation
- validation and PR Readiness Stage 1 analysis

Not approved by this planning file:

- validator code transition into mandatory repo gates
- worktree-local staging folder creation
- external state migration
- active branch/worktree/release-window external record creation
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

## Docs Split Stage 1 - Helper Bootstrap Scaffold Plan

Stage Status: `Active helper/bootstrap scaffolding only`
Source Branch: `feature/release-readiness-source-truth-intake`
Source Worktree: `C:\Nexus Worktrees\Governance`
Stage 1 Base: `origin/main@1acb308fead3c61600604dbfd2fdb36fca338262`

This stage creates safe helper scaffolds and a validation plan without initializing `C:\Nexus Governance State`, migrating active state, moving repo Docs files, or changing clean-clone repo validation. The helpers are report-first and dry-run by default; any operation that creates external state requires a later explicit USER decision and an explicit `--apply` command.

Stage 1 deliverables:

- `dev/orin_external_state_common.py` shared scaffold support
- `dev/orin_external_state_init.py` bootstrap packet and optional future `--apply` initialization path
- `dev/orin_external_state_report.py` external-root posture report
- `dev/orin_external_state_validation.py` clean-clone-safe local validation helper
- `dev/orin_external_state_lock.py` dry-run/applied lock packet scaffold
- `dev/orin_external_state_snapshot.py` dry-run/applied snapshot scaffold
- `dev/orin_state_fold_down_preview.py` fold-down preview scaffold
- `dev/orin_external_state_promote_preview.py` promotion preview scaffold
- `dev/orin_external_state_promote.py` promotion apply scaffold with no-loss audit posture
- helper registry registration and smoke validation for the helper family
- no external folder creation, state migration, file movement, deletion, archival, or worktree-local staging creation

Stage 1 review question:

```text
Do you approve Stage 2 root initialization for C:\Nexus Governance State after reviewing the Stage 1 helper/bootstrap scaffold and smoke-validation proof?
```

Stage 2 candidate after this repair merges:

```text
External Operational State Root Initialization
```

Stage 2 candidate scope:

- run `dev/orin_external_state_init.py --apply` only after explicit USER approval
- initialize `C:\Nexus Governance State` with manifest, generated index placeholder, schema folder, locks, central state folders, snapshot folder, and audit-log folder
- keep repo validators clean-clone safe
- keep active branch/worktree/release-window migration deferred until helper validation and USER review are green

Stage 2 non-includes unless separately approved:

- moving repo `Docs` files
- deleting or archiving branch records/plans
- migrating active branch state
- mutating FAM-006 or FAM-007
- changing runtime behavior
- creating a release or tag

## Docs Split Stage 4A - Repo Live-State Leakage Scanner / Migration Map Helper Plan

Stage Status: `Active report-only migration-map helper support`
Source Branch: `feature/release-readiness-source-truth-intake`
Source Worktree: `C:\Nexus Worktrees\Governance`
Stage 4A Base: `origin/main@7f17b97bac1f0ec7d9e424fdfa8792fe420eb885`

This stage adds a report-only helper that scans repo Docs for live operational state, classifies findings, and prints a migration map. It does not edit repo docs, write central branch/worktree/release-window state, move files, delete files, archive files, transition validators, or treat external state as complete.

Stage 4A deliverables:

- `dev/orin_repo_live_state_leakage_scan.py` report-only scanner for repo live-state leakage and migration candidates
- helper registry entry for the scanner
- source-truth plan updates that distinguish scanner output from active migration
- smoke validation showing the scanner reports `CLEAR / MIGRATION CANDIDATES ONLY` when findings are transition-legal or historical receipts

Stage 4A review question:

```text
Do you approve using the report-only migration map as the basis for a later active-state migration plan, without moving repo Docs files or migrating active state yet?
```

Stage 4A non-includes unless separately approved:

- creating branch/worktree/release-window state records from repo docs
- moving active branch plans or branch records out of repo
- deleting, archiving, or renaming repo docs
- transitioning repo validators into mandatory external-state checks
- mutating FAM-006 or FAM-007 worktrees
- changing runtime behavior

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

## Docs Split Target Matrix

Matrix Status: `Current for Docs Split Stage 4A`
Matrix Owner: `Docs/external_operational_state_store_reform_plan.md`
Binding Rule Owner: `Docs/governance_efficiency_operating_model.md`
Phase Gate Owner: `Docs/phase_governance.md`

This matrix is the Stage 4A review surface for preventing drift while repo docs still carry transition-legal active operational owners. It does not move files, create migrated branch/worktree/release-window records, transition validators, or migrate state by itself.

| Surface | Current Repo Role | Target Owner After Migration | Stage 0 Disposition | Drift Risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| `Docs/Main.md` | first loader and source-truth router | stays repo durable source truth | keep compact pointer to this plan and transition gate | high if Main implies migration is complete | update rarely; route only |
| `Docs/phase_governance.md` | phase rules, blockers, PR/Release gates | stays repo durable source truth | add transition gate and blockers | high if Stage 0, helper bootstrap, and migration blur | keep gate fields deterministic |
| `Docs/governance_efficiency_operating_model.md` | external-state contract and ownership model | stays repo durable source truth | owns binding transition drift gate | high if external candidates become shadow law | keep deterministic rule table |
| `Docs/external_operational_state_store_reform_plan.md` | implementation plan and future-work ledger | stays repo planning/reference surface until migration completes | own matrix, annotations, sequencing | high if treated as active migration authority | label as plan, not root/state |
| `Docs/validation_helper_registry.md` | helper inventory and future validation ownership | stays repo durable source truth | register future external-state helper family and drift-check hook | medium if validators are expected before approved | mark implementation as future |
| `Docs/branch_records/index.md` | active/historical branch authority routing | mixed/split: durable routing stays repo; live active posture migrates external later | keep current until migration stage | high release-loop source | migrate active operational posture later |
| `Docs/branch_records/*.md` | authority, approvals, phase history, receipts | mixed/split: durable receipts stay repo; active branch state migrates external later | current active owners remain legal until migration | high release-loop source | fold historical receipts, migrate active records by stage |
| `Docs/branch_plans/README.md` | branch-plan rules and templates | stays repo durable source truth | keep rules; external active plans later use same contract | medium | update only when plan ownership changes |
| `Docs/branch_plans/*.md` | active engineering plans while branch is active | mixed/split: active plans migrate external; durable retired receipts stay repo if approved | current active plans remain legal until migration | high release-loop source | migrate after helper/bootstrap validation |
| `Docs/worktree_slots.md` | stable slot registry and assignment receipts | mixed/split: durable slot definitions stay repo; live assignment migrates external | keep stable slots only | high if live assignment is copied | strip active assignment later |
| `Docs/feature_backlog.md` | compact feature-family registry | stays repo durable source truth | keep identity/pointers only | medium if selected-next returns | avoid live branch/PR posture |
| `Docs/prebeta_roadmap.md` | stage-breakpoint schedule outline | stays repo durable source truth | keep milestones/checkpoints only | high if release-window live state returns | avoid live release-window assembly |
| `Docs/workstreams/` | durable package/slice/proof history | stays repo durable receipt/history | keep promoted historical truth | medium | no live PR/watcher state |
| `Docs/family_visions/` | reusable family product direction | stays repo durable source truth | keep USER-accepted durable direction | low | do not absorb active plans |
| USER review Desktop bundle | local review/export packet | external/local review-bundle state after helper stage | stable bundle remains helper output | medium if stale zip recurs | keep stale-guard proof |
| Git/GitHub/helper live facts | derived live truth | Git/GitHub/helpers | unchanged | high if copied into docs | derive on demand |

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
- `External State Transition Gate Missing`
- `External State Transition Drift`
- `Docs Split Target Matrix Missing`
- `External State Migration Premature`

## External State Transition Drift Gate

Gate Status: `Required for external-state reform PR Readiness`
Current Stage: `Stage 4A - Report-Only Migration Map Helper`
External Root Approval: `Bootstrap Approved`
External Root Status: `Initialized`
Migration Status: `Not Started`
Validator / Helper Transition Status: `Report-only helper scaffolds and migration-map scanner approved; validator transition not approved`

Required packet fields:

- `External State Transition Gate:`
- `Transition Stage:`
- `Docs Split Target Matrix Status:`
- `Active-State Owner Boundary:`
- `External Root Approval:`
- `External Root Status:`
- `Premature Migration Scan:`
- `Repo Live-State Leakage Scan:`
- `Validator / Helper Transition Status:`
- `Source-Truth Agreement:`
- `Next Approved Step:`
- `Remaining USER Decisions:`

This gate exists so future Codex cannot treat the planning reference, helper scaffolds, root initialization, or report-only scanner as already-executed migration. Stage 4A means helper files may inspect repo docs and print a migration map, while repo docs may still contain transition-legal current active owners required by existing governance. Those owners become migrated external records only after USER approves active-state migration.

Drift blockers:

- `External State Transition Gate Missing`: PR Readiness packet omits the gate.
- `External State Transition Drift`: Main, phase governance, governance efficiency, this plan, branch authority, or helper registry disagree on stage, owner, or next step.
- `Docs Split Target Matrix Missing`: the matrix is absent or stale.
- `External State Migration Premature`: helper/bootstrap/root/migration/file-movement work is treated as approved before USER approves that stage.

Recommended near-term implementation posture:

- keep this branch at Stage 4A until PR/merge and active worktree acknowledgement
- do not create migrated branch/worktree/release-window records in this PR
- do not run helper `--apply` operations in this PR
- do not migrate branch records, branch plans, roadmap, backlog, or worktree slots in this PR
- require the transition gate in the next external-state implementation PR before Stage 2 / PR creation

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
4. Initialize the canonical external root only after explicit USER approval.
5. Record report-only migration preview packets without active-state migration.
6. Implement the report-only repo live-state leakage scanner and migration-map helper.
7. Adopt external state for new or re-entering branches after USER approval.
8. Adopt ignored worktree staging for proposed state only after USER approval.
9. Migrate active branch, worktree, and release-window state out of repo docs after USER approval.
10. Transition validators: repo validators stop requiring live state in repo docs; external validators check operational state.
11. Clean repo docs: remove stale live-state fields and keep durable receipts only.
12. Transition Release Readiness to Git/GitHub truth plus external state plus repo durable truth.
13. Require active worktree acknowledgements after merged governance/source-truth changes.

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

- PR #220 was handled under existing rules and released through `v1.7.23-prebeta`; PR #222, PR #223, and PR #224 are handled through `v1.7.25-prebeta` post-release canon closure before external-state implementation begins.

## Annotated Recommendations For Next Governance Pass

Recommendation A - keep Main as a router:

- Status: `Applied in Stage 0`
- Reason: Main must point to the external-state contract and plan without becoming the detailed migration ledger.
- Future risk: if Main starts carrying detailed live-state migration fields, it becomes another live-state owner.

Recommendation B - require the transition gate before external-state PR creation:

- Status: `Applied in Stage 0`
- Reason: this prevents planning from being mistaken for migration complete and catches disagreement between Main, phase governance, governance efficiency, the plan, branch authority, and helper registry.
- Future risk: without this gate, Codex could initialize helpers or demand external state before USER approves bootstrap.

Recommendation C - keep helper work report-only until active migration is separately approved:

- Status: `Applied through Stage 4A for report-only helpers; validator transition and active migration remain future-gated`
- Reason: scanner output should expose migration candidates without rewriting repo docs or creating central active branch/worktree/release-window records.
- Future risk: if scanner output is treated as migration itself, the repo could lose durable receipts or create shadow external truth.

Recommendation D - migrate active records only after helper bootstrap and migration-map review prove locks, snapshots, version checks, and target owners:

- Status: `Future-gated`
- Reason: moving branch records and plans out of repo without lock/version/snapshot proof risks losing the exact planning receipts the reform is meant to preserve.
- Future risk: premature file movement could trade release debt for external-state corruption.

Recommendation E - keep release debt narrow:

- Status: `Applied in Stage 0`
- Reason: stale operational trackers should become `Repo Live-State Leakage` or external-state updates, not durable release debt.
- Future risk: if Release Readiness keeps treating stale branch/worktree posture as release debt, the repair loop continues.

## Current External-State Sequencing Recommendation

Default path:

1. Complete Stage 4A report-only repo live-state leakage scanner / migration-map helper with no active-state migration.
2. Merge the Stage 4A helper only after validation and USER approval.
3. Rebaseline or acknowledge active worktrees after merge.
4. Review the migration-map output before deciding whether to approve active-state migration, validator transition, repo cleanup, or worktree-local staging.

External-state implementation does not replace post-release canon closure or become a release unblocker unless USER explicitly pauses release flow and approves that route.

## Future Exact USER Decision Shape

Approve the next implementation phase only after this Stage 4A report-only migration-map helper PR merges and active worktrees rebaseline or acknowledge the changed governance:

```text
Approve External Operational State Store active-state migration planning on C:\Nexus Worktrees\Governance after all active worktrees rebaseline or acknowledge the Stage 4A report-only migration-map helper. Scope: use the scanner output to produce a USER-reviewable active-state migration packet naming exact repo fields, external target records, lock/snapshot/version requirements, durable receipt preservation, and no-loss promotion rules. Do not move repo docs, delete or archive files, transition validators, mutate runtime, create releases, clean branches/worktrees, or change FAM-006/FAM-007 without separate USER approval.
```
