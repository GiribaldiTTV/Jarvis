# Governance Efficiency Operating Model

## Purpose

This document is the compact operating model for governance reform after the multi-worktree transition.

It exists to reduce repeated source-truth updates, shrink routine prompt load, and keep safety gates enforceable by treating repo Docs as durable index/context files, not operational ledgers.

## Scope

This model applies to governance/source-truth/process reform only.

It does not authorize runtime implementation, FAM-006 mutation, FAM-007 mutation, successor branch creation, release execution, tag or GitHub Release work, issue closeout, branch deletion, worktree cleanup, provider/model execution, downloads, memory work, voice/Core sync, shortcut or installer work, AI Product Contract import, or private Dev ORIN import.

External Operational State Store / Release Debt Abolition work advances only through separately USER-approved stages. Docs/source-truth contracts, helper scaffolds, local root initialization, report-only migration-map helpers, active-state migration planning packets, active-state migration execution planning packets, active-state migration execution, validator transition, repo cleanup planning, compact pointer cleanup execution, branch-authority routing planning, branch-authority routing cleanup execution, branch-detail-record / branch-plan cleanup planning, no-loss cleanup closure, broader repo cleanup execution, file moves, file deletion, file archival, PR creation, merge, release execution, runtime work, FAM mutation, issue work, branch cleanup, backup setup, and private repo creation remain separate USER decisions unless the USER explicitly admits that later phase. Stage 4 active-state migration execution has seeded approved local external records, Stage 5 validator transition has made local external-state validation explicit, Stage 6 cleanup planning has classified future cleanup lanes, Stage 6A compact pointer cleanup has cleaned backlog/roadmap/worktree-slot compact surfaces, Stage 6B branch-authority routing planning has defined the `Docs/branch_records/index.md` execution packet, Stage 6C branch-authority routing cleanup has routed the index to external active-authority owners, and Stage 6D has planned branch-detail-record / branch-plan cleanup. Stage 6E no-loss cleanup closure may record that branch detail records and branch plans remain durable receipts or transition owners when scanners find zero blocking leakage; it must not bulk rewrite, move, delete, archive, or require external state in clean clones. Repo Docs movement and mandatory repo-validator enforcement remain separate stages. External-state helpers must default to report/dry-run behavior unless a later explicit USER-approved apply step authorizes mutation.

Planning Reference: `Docs/external_operational_state_store_reform_plan.md` preserves the agreed sequencing, Docs Split Target Matrix, implementation annotations, and future-work design. Use it as the durable future-work reference, not as active migration authority.

## Rule ID And Owner Model

Future governance changes should use a rule ID, one owner, and compact mirrors.

Rule ID format:

- `GEF-001`

Required fields for new reform rules:

- `Rule ID:`
- `Rule Name:`
- `Owner File:`
- `Compact Mirrors:`
- `Validator / Helper Owner:`
- `Allowed Mutation Carrier:`
- `Do Not Duplicate In:`
- `Historical Receipt Rule:`

Full normative policy belongs in the owner file. Mirrors should summarize the rule and point to the owner instead of repeating full policy prose.

## Repo Docs Index-Only Contract

Repo Docs are durable index/context files. They may contain governance law, product vision, architecture contracts, source-truth routing, durable evidence pointers, compact historical receipts, and public-safe explanation needed from a clean clone.

Repo Docs must not contain active operational ledger material for branch state, branch plans, UFD rows, Branch Change Intent rows, Element-to-Phase rows, worktree assignment state, PR watcher state, release-window assembly, selected-next posture, review-bundle manifests, rebaseline packets, or temporary Codex handoff state. Those ledgers belong in `C:\Nexus Governance State`, approved worktree-local staging, Git/GitHub/helper-derived truth, or later USER-approved external owners.

When a repo doc needs to reference operational work, it may record only a compact evidence pointer such as branch name, branch record path, external-state owner path, workstream/family owner, PR/release receipt, or historical interpretation. It must not record whether the operational item is currently active, complete, pending, blocked, open, mergeable, released, selected-next, or no-branch-created unless the line is clearly labeled as historical receipt evidence.

## Source-Truth Ownership Matrix

Use this ownership model before creating or updating a governance/source-truth file:

| Surface | Owns | Must Not Own |
| --- | --- | --- |
| `Docs/Main.md` | least-updated canonical docs index, source-truth layer ownership, recovery pointers, and clear digest of valid governance/source-truth files | detailed branch execution narratives or operational ledgers |
| `Docs/phase_governance.md` | normative phase rules, phase enum, blockers, gates, proof hierarchy | branch-local implementation details |
| `Docs/development_rules.md` | developer-facing execution rules and compact phase mirrors | duplicate full policy blocks already owned elsewhere |
| `Docs/codex_modes.md` | Codex operating posture and mode behavior | branch-local truth or release receipts |
| `Docs/orin_task_template.md` | reusable prompt skeleton fields | current live branch facts |
| `Docs/codex_user_guide.md` | human-readable operator guide | machine-enforced current-state authority |
| `Docs/worktree_slots.md` | stable slot IDs and intended lane labels | active worktree assignment ledger, `HEAD`, dirty state, ahead/behind, PR state, latest tag, latest release |
| `Docs/feature_backlog.md` | compact feature-family registry and pointer layer | detailed active-branch execution planning, package/slice ledgers, or live lifecycle posture |
| `Docs/prebeta_roadmap.md` | release-stage schedule outline, milestone breakpoints, broad feature-family checkpoints, and durable branch evidence pointers | volatile Git/GitHub operational state, active release ledger fields, or active/complete/pending branch posture |
| `Docs/nexus_vision.md` | project-wide product vision contract, long-term standards, and durable product direction | active branch implementation plans or family-specific execution ledgers |
| `Docs/family_visions/` | family-specific durable product direction and reusable USER-accepted standards | active branch authority, live state, or per-seam implementation checklists |
| `Docs/branch_records/index.md` | durable branch-record law, standing Governance active-authority exception, historical receipt routing, and pointers to external active operational branch authority | detailed branch implementation checklists or general live active-branch operations lists |
| `Docs/branch_records/<branch>.md` | durable branch identity, approval evidence, compact historical receipt, and pointers to external operational owners | active branch lifecycle ledger, volatile live state, unindexed execution diary, full feedback text, or reusable family-level implementation history after promotion |
| `Docs/branch_plans/<branch>.md` | Branch Runtime Engineering Plan shape, transition-approved plan receipts, retired/historical branch-plan evidence, and durable lookup paths | canonical live branch status, active/complete/pending lifecycle posture, permanent family-level dossier, active authority after fold-down, duplicate feedback ledger, or live-state ledger |
| `Docs/workstreams/index.md` | canonical workstream and dossier routing | per-branch live state by inertia |
| `Docs/workstreams/<id>.md` | durable promoted implementation history and reusable continuity | volatile branch/PR state |
| `Docs/validation_helper_registry.md` | durable helper inventory, statuses, reuse/consolidation decisions | workstream evidence details already owned by branch/workstream docs |
| `Docs/governance_process_efficiency_reform_plan.md` | reform inventory, sequencing, and implementation records | operational live Git/GitHub facts |
| `Docs/governance_intake_triage_and_digest_profiles.md` | governance intake and digest profile standard | branch-specific blocker narratives |
| `Docs/pr_watcher_mode_contract.md` | watcher mode contract and approval default | live PR state beyond explicit watcher proof packets |
| `Docs/external_operational_state_store_reform_plan.md` | Docs Split implementation plan, target matrix, approved-stage boundaries, migration-map helper posture, annotations, transition sequencing, and future-work checklist | binding migration authority, validator transition authority, active external-state root contents, or migrated branch/worktree/release-window state |

## Docs Source-Truth Reform Model

Docs Source-Truth Reform Model: Compact Pointer Layer.

The post-audit reform model has one owner per fact class and keeps repo Docs index-only:

- backlog owns compact product-family identity and canonical pointers; it does not own live lifecycle posture
- roadmap owns the pre-Beta/Beta/release schedule outline, milestone breakpoints, broad feature-family checkpoints, and durable branch evidence pointers; it does not own active/complete/pending state
- worktree slots own reusable slot definitions and lane labels; external state owns current assignment ledger detail
- branch records own durable branch identity, approval evidence, and compact historical receipts; external state owns active branch lifecycle ledgers
- branch plans define plan shape and may preserve transition-approved or historical plan receipts; external branch state owns active runtime-branch engineering plans, full active USER Feedback Disposition rows, USER-reviewable Element-to-Phase Proof Matrix rows, and active Branch Change Intent rows
- branch records receive compact fold-down receipts only when durable evidence remains useful
- workstreams and family dossiers own durable package trace, slice trace, proof history, and reusable continuity
- Git, GitHub, and approved helpers own live operational truth

Backlog and roadmap must not contain `Package Trace:` or `Slice Trace:` sections. Those detailed ledgers belong in workstream records, family dossiers, external active branch plans, transition-approved branch plans, or structured branch receipts.

Backlog and roadmap must not manually maintain latest public prerelease, latest tag, release URL, target commit, open PR state, active branch identity, review-thread state, worktree dirty state, or ahead/behind state as active truth. The roadmap is a stage-breakpoint reference, not a release ledger. These surfaces may point to the helper or owner that derives live truth.

Historical receipts remain allowed when they are explicitly historical interpretation, compact, and routed to the owning receipt surface.

## Derived Live Truth Versus Historical Receipt

Derived live truth comes from Git, GitHub, or approved helpers. Examples include current `HEAD`, `origin/main`, merge base, dirty state, branch ahead/behind state, remote ref existence, open PR state, review-thread state, latest tag, latest GitHub Release, and issue state.

Governance receipts are recorded after live truth is checked. Examples include USER assignment decisions, branch admission, release scope interpretation, merge closeout, watcher repair proof, and branch-plan fold-down.

Docs may record historical receipts, but they must not pretend to be live operational truth. When a current operational fact is needed, run a helper or live check and report it as evidence.

## External Operational State Store Contract

Rule Name: `External Operational State Store Contract`

Owner: `Docs/governance_efficiency_operating_model.md`

Applies To: active branch state, active branch plans, worktree assignment, release-window assembly, PR watcher state, USER review bundle manifests, rebaseline audit packets, temporary Codex handoff digests, fold-down previews, cross-worktree lessons, governance candidates, state promotion packets, worktree acknowledgements, and any other live operational tracker that exists to coordinate Codex/worktree activity rather than to define durable project truth.

Required State:

- Repo docs own durable source truth.
- `C:\Nexus Governance State` owns accepted operational state after the external-state system is USER-approved and initialized.
- `<worktree>\.nexus_state_staging\` may hold proposed state only after USER approves worktree-local staging.
- Git, GitHub, and approved helpers own derived live facts.
- External governance candidates are not binding governance until folded into repo source truth through a USER-approved repo update and merge.
- Repo docs may keep durable branch/document evidence pointers and historical receipts, but they must not own active/complete/pending lifecycle posture for branches, PRs, worktrees, selected-next decisions, release windows, watcher state, review bundles, or temporary handoffs.

Allowed Values:

- External State Item Status: `Active`, `Queued`, `Promotion Pending`, `Promoted`, `Fold-Down Pending`, `Folded`, `Archived`, `Expired`, `Rejected`, `USER Decision Required`
- Worktree Acknowledgement State: `Pending`, `Accepted`, `Conflict`, `Not Applicable`
- Lock State: `Unlocked`, `Locked`, `Expired`, `Stale`, `Conflict`, `Released`, `Recovery Required`
- Promotion Result: `Approved`, `Rejected`, `Blocked`, `Superseded`, `Folded Into Repo`, `External Only`, `USER Decision Required`
- Release Readiness Live-State Result: `Clear`, `Post-Release External State Carry-Forward`, `External Operational State Conflict`, `Repo Live-State Leakage`, `Durable Release Truth Defect`, `USER Decision Required`

Invalid Values:

- canonical external operational state inside any Git worktree
- repo-root `.nexus_state`, `.nexus_local_state`, or `.nexus_state_staging` treated as accepted central state
- worktree-local staging treated as accepted central state
- external governance candidates treated as binding repo governance
- generated global indexes treated as primary hand-edited state
- active branch, PR, worktree, watcher, release-window, selected-next, or temporary handoff state treated as durable repo source truth by inertia
- backlog, roadmap, branch-record index, branch plans, worktree slots, or review surfaces using current-state words such as `active`, `complete`, `pending`, `no branch created`, `no live PR`, `PR creation pending`, `Stage 2 pending`, or release-window ownership as live operational truth instead of historical evidence or external/derived state

Blocking Condition:

- `External State Missing`: active local workflow requires external operational state but the approved root is absent or uninitialized.
- `External State Schema Conflict`: external state files declare mixed or unsupported `External State Schema` values, or a schema migration would rewrite active state without a migration packet, snapshot, validation, and USER decision.
- `External State Lock Missing`: external state mutation is requested without the relevant lock.
- `External State Version Conflict`: the state version changed between read and write.
- `External State Owner Conflict`: two owners claim the same state partition.
- `External State Promotion Missing`: staged or proposed state is being used as central accepted state without a promotion packet.
- `Governance Candidate Not Promoted`: an external candidate that affects durable release truth, public safety, validator correctness, or source-truth ownership has not been promoted or dispositioned.
- `Cross-Worktree Acknowledgement Missing`: merged governance/source-truth changes that affect an active worktree have not been acknowledged.
- `Repo Live-State Leakage`: repo docs contain live operational state that should be external or derived.
- `Fold-Down Decision Missing`: an operational state item has reached fold-down but lacks final disposition.
- `Release Debt Misclassified`: stale operational tracker state is treated as durable public release debt.
- `External State Corrupt`: external state cannot be parsed, validated, or matched to its schema.
- `Stale Lock Recovery Required`: a lock is expired/stale and the recovery risk is unclear.
- `External State Transition Gate Missing`: an external-state reform branch reaches PR Readiness without reporting the transition gate fields from this model and `Docs/phase_governance.md`.
- `External State Transition Drift`: Main, phase governance, this model, the external-state plan, or the helper registry disagree about current transition stage, approved scope, active-state owner, or next legal step.
- `Docs Split Target Matrix Missing`: the external-state reform plan lacks a current target matrix for repo surfaces that stay durable, move external, split/mix, or derive from Git/GitHub/helpers.
- `External State Migration Premature`: a branch treats external helper/bootstrap/root/migration work as approved, initialized, or required before USER has approved that stage.

Repair Owner: standing Governance intake or the current USER-approved legal carrier named by phase governance.

Repair Path: classify the item, decide whether it belongs in repo durable truth, central external state, worktree-local staging, Git/GitHub/helper-derived live truth, or historical receipt; then repair through the legal carrier. Additional active state migration, helper/validator implementation, and repo cleanup require separate USER approval.

USER Decision Required: required before external root creation, staging folder creation, schema migration, state migration, shared-state promotion, release-window state mutation, selected-next posture mutation, branch authority mutation, fold-down, cloud backup, private repo creation, or any file move/delete/archive.

Validation Owner: repo durable-truth validation remains owned by repo validators. External operational validation is local-workflow evidence after Stage 5 and must not be required by GitHub Actions or clean-clone repo validation.

Final Disposition: external operational state may remain external-only, be folded into repo source truth as a durable receipt, be archived, expire, be rejected, or require USER decision. Governance law becomes binding only after USER-approved repo source-truth update and merge.

## External State Transition Drift Gate

Rule Name: `External State Transition Drift Gate`

Owner: `Docs/governance_efficiency_operating_model.md`

Applies To: any branch, PR Readiness packet, Release Readiness blocker repair, governance reform, helper/bootstrap pass, validator transition, review-bundle change, or repo-doc cleanup that changes the External Operational State Store contract, Docs split plan, live-state ownership, external-state schema, migration sequencing, repo live-state leakage policy, or worktree acknowledgement behavior.

Required State:

- `External State Transition Gate:` is reported before PR Readiness Stage 2 / PR creation for external-state reform branches.
- `Docs/external_operational_state_store_reform_plan.md` carries a current Docs Split Target Matrix and annotated future-work recommendations.
- Stage 0 means docs/source-truth planning only; it does not approve helper code, validator code, folder creation, external state initialization, state migration, or file movement.
- Stage 1 means helper/bootstrap scaffolding and validation planning only; helpers may exist and run report/dry-run checks, but applied mutation remains blocked without later USER approval.
- Stage 2 means USER-approved local root initialization only; it may initialize `C:\Nexus Governance State`, but it does not migrate active branch/worktree/release-window state, transition repo validators, or move repo docs.
- Stage 3 means migration planning and external preview packets only; it may record no-mutation preview packets in external state, but it does not migrate active state.
- Stage 4A means report-only repo live-state leakage scanning and migration-map helper support; it may inspect repo docs and print migration candidates, but it does not edit repo docs, migrate active state, create external branch/worktree/release-window records, or transition validators.
- Stage 4B means active-state migration planning packet only; it may use Stage 4A scanner output to name exact repo surfaces, target external records, lock/snapshot/version requirements, durable receipt preservation, and no-loss promotion rules, but it does not create or update central external records, move/delete/archive repo docs, migrate active state, or transition validators.
- Stage 4C means active-state migration execution planning packet only; it may convert the Stage 4B planning matrix into exact execution preflight, external target record list, durable receipt preservation plan, rollback/recovery plan, and USER review question, but it does not run helper `--apply` operations, create or update central external records, move/delete/archive repo docs, migrate active state, create worktree-local staging, or transition validators.
- Stage 4 means USER-approved active-state migration execution; it may create or update only the approved central external operational records, locks, snapshots, and audit logs. It does not move, delete, archive, or rewrite repo Docs and does not transition validators unless separately approved.
- Stage 5 means validator transition; local external-state validators may require the initialized external root and migrated records only for approved local workflows, while GitHub Actions and clean-clone repo validators remain external-root independent.
- Stage 6 means repo cleanup planning; it may classify cleanup lanes, name candidate surfaces, and recommend future execution packets, but it does not edit, move, delete, archive, or rewrite repo Docs.
- Stage 6A means compact pointer-surface cleanup execution; it may edit only `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, and `Docs/worktree_slots.md` to remove live operational posture and replace it with pointers to Git/GitHub/helpers, `C:\Nexus Governance State`, family visions, branch records, branch plans, workstream dossiers, and release receipts.
- Stage 6B means branch-authority routing cleanup planning; it may define how `Docs/branch_records/index.md` should become durable routing law plus external active-authority pointers, but it must not edit the index, branch records, branch plans, or generated audits.
- Stage 6C means branch-authority routing cleanup execution; it may edit only `Docs/branch_records/index.md` plus stage-boundary source truth so the index keeps durable routing law, historical receipt routing, and the single standing Governance active exception while non-standing active operational branch authority routes to `C:\Nexus Governance State\central\active_branch_authority_state.md`, branch-specific external records, and Git/GitHub/helper live checks.
- Stage 6D means branch-detail-record / branch-plan cleanup planning; it may define exact future cleanup batches, durable receipt preservation rules, external replacement owners, and validation preflight for branch records and branch plans, but it must not edit branch detail records, branch plans, generated audits, move/delete/archive repo files, create worktree-local staging, or mutate FAM worktrees.
- Stage 6E means branch-detail-record / branch-plan no-loss cleanup closure; it may record the execution finding that broad branch-record and branch-plan rewrites are not required when report-only scanners show zero blocking leakage, branch plans are classified as durable historical receipts, and branch records are transition-legal or durable receipt surfaces. It must not edit branch detail records or branch plans except the standing Governance intake record, move/delete/archive repo files, create worktree-local staging, or mutate FAM worktrees.
- Current repo branch records and branch plans remain durable transition owners until a USER-approved repo cleanup stage removes live-state fields, makes them pointer-only, or folds them down as historical receipts.
- Main, phase governance, this model, the external-state plan, branch authority record, and helper registry must agree on the current stage and next legal step.

Allowed Values:

- Transition Stage: `Stage 0 - Docs Plan`, `Stage 1 - Helper Bootstrap Planning`, `Stage 2 - Root Initialization`, `Stage 3 - Migration Preview`, `Stage 4A - Report-Only Migration Map Helper`, `Stage 4B - Active-State Migration Planning Packet`, `Stage 4C - Active-State Migration Execution Planning Packet`, `Stage 4 - Active-State Migration`, `Stage 5 - Validator Transition`, `Stage 6 - Repo Cleanup`, `Stage 6A - Compact Pointer Cleanup`, `Stage 6B - Branch Authority Routing Planning`, `Stage 6C - Branch Authority Routing Cleanup`, `Stage 6D - Branch Detail And Plan Cleanup Planning`, `Stage 6E - No-Loss Cleanup Closure`, `Complete`, `Blocked`, `USER Decision Required`
- Docs Split Matrix Status: `Current`, `Missing`, `Stale`, `Needs USER Review`
- Active-State Owner Boundary: `Repo Current Owners`, `Hybrid Transition`, `External Canonical`, `External Canonical With Repo Transition Receipts`, `Blocked`
- External Root Approval: `Not Approved`, `Bootstrap Approved`, `Migration Waiver Approved`, `Revoked`, `USER Decision Required`
- External Root Status: `Not Approved`, `Approved Not Initialized`, `Initialized`, `Unavailable`, `Invalid Location`
- Drift Result: `Clear`, `External State Transition Gate Missing`, `External State Transition Drift`, `Docs Split Target Matrix Missing`, `External State Migration Premature`, `USER Decision Required`

Invalid Values:

- claiming external migration is active during Stage 0
- requiring `C:\Nexus Governance State` in GitHub Actions or clean-clone repo validation
- treating Stage 5 local external-state validation as permission to move, delete, archive, or rewrite repo Docs
- treating Stage 6 cleanup planning as permission to execute cleanup edits without a later exact-file USER decision
- treating Stage 6A compact pointer cleanup as permission to edit branch records, branch plans, workstreams, family visions, generated audits, move/delete/archive files, or mutate external state
- treating Stage 6B branch-authority routing planning as permission to edit `Docs/branch_records/index.md` or any branch record before the execution packet is approved
- treating Stage 6C branch-authority routing cleanup as permission to edit branch detail records, branch plans, workstreams, family visions, generated audits, move/delete/archive files, create worktree-local staging, mutate FAM worktrees, or make external state mandatory for clean-clone repo validation
- treating Stage 6D branch-detail-record / branch-plan cleanup planning as permission to edit the branch records or branch plans being planned, collapse durable receipts, move/delete/archive files, or rely on external state without no-loss preservation proof
- treating Stage 6E no-loss cleanup closure as permission to skip future exact cleanup if a later validator reports blocking leakage, or as permission to delete/move/archive branch records and branch plans without explicit USER approval
- moving, deleting, archiving, or rewriting repo docs before helper/bootstrap/migration approval
- treating worktree-local staging as canonical central state
- adding new repo live-state owners without either a transition reason, historical-receipt label, or approved migration path

Blocking Condition: `External State Transition Gate Missing`, `External State Transition Drift`, `Docs Split Target Matrix Missing`, `External State Migration Premature`, or `USER Decision Required`.

Repair Owner: standing Governance intake or another USER-approved governance/source-truth carrier named by phase governance.

Repair Path: update Main routing, this model, phase governance, external-state plan, helper registry, and the active branch authority record until they agree on the transition stage, active-state owner boundary, target matrix, validation posture, and next legal step. Do not initialize folders, migrate state, transition validators, move files, or clean repo Docs unless USER approval explicitly admits that stage; report-only helper scaffolds and migration-map helpers must stay no-mutation by default.

USER Decision Required: required before each stage transition, applied external-state mutation, worktree-local staging creation, validator transition, active-state migration, repo cleanup, moving/deleting/archiving files, or treating external state as canonical for active branch/worktree/release-window records. Adding or running report-only helpers, planning packets, or execution-planning packets does not imply active migration approval.

Validation Owner: marker-first repo validation may check the transition gate and source-truth agreement after the validator is updated; local external-state validation may check the initialized root, required migrated record set, source repo HEAD, schema consistency, and released-lock posture only when an approved local workflow supplies the external root. External operational validation must not become a clean-clone repo requirement.

Final Disposition: the branch may proceed only when the gate is `Clear`, or when USER accepts a recorded waiver/decision for a specific stage. Any unresolved drift blocks PR Readiness green.

## Deterministic Binding Language Contract

Binding governance sections that control ownership, mutation, locks, promotion, fold-down, Release Readiness, cross-worktree reconciliation, source-truth ownership, validator blocking, or external operational state must use deterministic rule language.

Each binding rule must include:

- `Rule Name`
- `Owner`
- `Applies To`
- `Required State`
- `Allowed Values`
- `Invalid Values`
- `Blocking Condition`
- `Repair Owner`
- `Repair Path`
- `USER Decision Required`
- `Validation Owner`
- `Final Disposition`

Planning and recommendation sections may use softer wording only when explicitly marked `Non-Binding Planning`.

## CI And Clean Clone Boundary

Repo validators running in GitHub Actions or on clean clones validate durable repo truth only. They must not require access to `C:\Nexus Governance State`.

Local governance validators may require external state only for active local workflow, Release Readiness analysis, worktree coordination, external-state migration, external-state validation, lock/snapshot/recovery workflows, or another USER-approved local operational pass.

If external state is unavailable in CI, the result is not a repo failure unless repo docs contain `Repo Live-State Leakage`.

## External State Bootstrap Rule

If external state is missing during active local workflow, Codex must return `External State Missing` and provide a bootstrap packet instead of inferring active branch, selected-next, worktree assignment, release-window state, or watcher state from stale repo docs.

The bootstrap packet must include:

- desired root: `C:\Nexus Governance State`
- worktree label
- source repo path
- branch
- source repo `HEAD`
- schema version
- initialization scope
- exact USER decision needed

Future helper command expectation:

```text
python dev\orin_external_state_init.py --root "C:\Nexus Governance State" --worktree "<label>" --repo "<repo_path>" --schema <schema_version>
```

Until USER approves initialization, active operational workflow waits. Analysis-only work may continue only with an explicit analysis-only waiver.

## Canonical External State Root Rule

Canonical external operational state must live outside every Git worktree.

Valid canonical root:

- `C:\Nexus Governance State`

Invalid as canonical state:

- repo-root `.nexus_state`
- repo-root `.nexus_local_state`
- repo-root `.nexus_state_staging`
- any folder inside a Git worktree

Repo-root ignored folders are staging or scratch only. Canonical operational state inside a Git worktree is invalid unless USER grants a one-off migration waiver.

## External State Schema Migration Rule

Every external state file must name:

- `External State Schema`
- `State Version`
- `Last Updated`
- `Last Updated By`
- `Worktree`
- `Branch`
- `Source Repo HEAD`

Schema changes require a migration packet, snapshot, validation, USER decision, and audit log entry before active state is rewritten.

Mixed schema versions, unsupported schema values, or schema rewrites without the required packet return `External State Schema Conflict`.

## Generated Index Rule

`state_index.md` and global external-state indexes are generated reports, not primary state.

Primary state lives in branch, worktree, release-window, candidate, promotion, acknowledgement, and fold-down records.

Manual edits to generated indexes are invalid unless helper repair or recovery is USER-approved.

## State Promotion And No-Loss Rule

Worktree-local staging is proposed state only. Central external state is accepted operational state.

Promotion from staging to central state requires a State Promotion Packet, lock acquisition, central state version check, conflict scan, validation, snapshot when risk warrants it, audit log entry, and USER decision when shared state, release-window state, selected-next posture, branch authority, fold-down, or cross-worktree lesson state is affected.

Promotion does not delete the staging source by default. Promotion must update central state, record final disposition, write the audit log, and preserve the staging source until promotion result is recorded. Staging source may expire or archive only after promotion result and audit log exist.

No-loss tracking applies to every external lesson, candidate, staged state change, promotion packet, and fold-down packet. Each item must have owner, status, target, final disposition, validation result, and USER decision state when required.

Allowed no-loss statuses:

- `Open`
- `Queued`
- `Promoted`
- `Folded Down`
- `Rejected`
- `Superseded`
- `Expired`
- `USER Decision Required`

## Worktree Acknowledgement Trigger Rule

After merged repo governance/source-truth changes, acknowledgement is required for active worktrees when the changes affect:

- phase rules
- branch plan rules
- validator behavior
- source-truth ownership
- Release Readiness
- review bundles
- external state schema
- worktree slots
- any active branch implementation or proof path

Other changes may be `Not Applicable`.

Acknowledgement conflicts return one of:

- rebaseline packet
- branch-plan revision packet
- external state promotion packet
- USER decision packet

## Governance Candidate Release Readiness Boundary

Governance candidates affecting durable release truth, public safety, validator correctness, or source-truth ownership may block Release Readiness until promoted, rejected, waived, or dispositioned by USER decision.

Local-only, future-only, unrelated, or advisory governance candidates remain external operational state and do not block Release Readiness.

## Release Debt Redefinition

Release debt means durable public release truth is missing or wrong.

Examples of real release debt:

- wrong tag, body, or release notes
- invalid or missing artifact
- missing durable public milestone summary
- released capability absent from durable product history

These are not release debt after the external-state reform:

- branch record still active
- branch plan still active
- worktree slot stale
- selected-next stale
- PR watcher stale
- release-window operational state stale
- post-release closure state pending

Those become external operational state updates or `Repo Live-State Leakage` findings.

## External-State Reform Sequencing

The default path for the current PR #220 / v1.7.23 release-readiness blocker is to clear PR #220 under existing rules, rerun Release Readiness, and then begin external-state reform.

External-state implementation does not become the immediate release unblocker unless USER explicitly pauses release flow and approves that route.

## Duplicate Live-State Guard

Backlog, roadmap, branch records, worktree slots, and workstream docs must not all manually track the same volatile state.

Allowed compact non-live markers:

- compact backlog/roadmap status and owner pointers that do not manually maintain volatile live facts
- branch authority status in the active branch record
- slot assignment receipt in `Docs/worktree_slots.md`
- historical receipts after live truth is validated

Canonical docs and context docs are distinct. `Docs/Main.md` is the highest-level canonical docs index: it should be updated rarely, point to the current valid governance/source-truth files, and explain each file's intended purpose clearly enough to recover the system. Context docs may preserve historical evidence, workstream detail, branch receipts, product reasoning, or implementation lessons, but they must point back to their canonical owner and must not pretend to be the top-level source of current governance law.

Main-first loader chain: `Docs/Main.md` routes Codex to the owning source-truth files. Context docs and review bundles may point to Main and the relevant owner, but they must not become alternate first loaders or duplicate detailed policy that belongs in phase governance, vision owners, branch plans, branch records, or helper registries.

Prohibited duplication by default:

- raw `HEAD` or `origin/main` hash as current truth outside an operator packet or historical receipt
- open PR state in merged-main current-state sections
- live watcher state in backlog or roadmap
- detailed per-seam runtime plan narrative in backlog or roadmap
- release/latest-tag truth copied into multiple docs without validator or GitHub check
- `Package Trace:` or `Slice Trace:` detail inside backlog or roadmap
- repeated release-window PR lists inside both backlog and roadmap

If duplication is unavoidable for scanability, name the owner and make the mirror explicitly compact.

## Current Summary And Historical Appendix Split

Large branch records should keep current machine-readable truth near the top and move long narrative to a historical appendix or folded receipt.

Preferred structure:

- top current summary and required markers
- current blockers and next legal phase
- active plan pointers
- validation and receipt summary
- historical appendix or fold-down receipt

Validators should prefer the current summary when checking phase posture. Historical appendices must not retain live active-branch, live PR, or pending watcher wording unless clearly labeled historical.

## Phase Alias UX

Canonical phase names for validators are:

- `Branch Readiness`
- `Branch Planning`
- `Workstream`
- `Hardening`
- `Live Validation`
- `PR Readiness`
- `Release Readiness`

Human-facing aliases may be used only as explanatory labels:

- `Branch Readiness Stage 1` -> `Plan Review`
- `Branch Readiness Stage 2` -> `Setup / Admission`
- `Workstream` -> `Build`
- `Hardening` -> `Stabilize`
- `Live Validation` -> `User Proof`
- `PR Readiness Stage 1` -> `Merge Readiness Audit`
- `PR Readiness Stage 2` -> `PR Execution / Watch`
- `Release Readiness` -> `Release Validation`
- `Standing Governance Intake` -> `Policy Repair Lane`

Aliases must never replace canonical phase markers in source truth.

## Branch Planning UX Standard

`Docs/phase_governance.md` owns lifecycle law. This section is only the compact UX mirror for how USER-facing planning should feel after the Branch Planning reform.

`Branch Planning` separates USER vision acceptance from engineering plan acceptance and orchestration validation:

- `BP1 - USER Branch Vision Review`: `USER_BRANCH_VISION_REVIEW.md` explains what the branch is trying to create, how it will look and function, where the USER will see it, which product options exist, what Codex recommends, and what USER accepted, changed, rejected, deferred, or waived.
- `BP2 - USER Branch Plan Review`: `USER_BRANCH_PLAN_REVIEW.md` explains how Codex would build the accepted BP1 vision: scope size, SLC/seam package, affected surfaces/files, validators/helpers, proof, H1/LV/UTS, rollback, risks, future-gated boundaries, and the plan acceptance checklist.
- `BP3 - Workstream Entry / Orchestration Validation`: validates that BP2 implements BP1, that the branch is the largest safe feature-focused package, and that SLCs are the engineering route inside one branch. It cannot return implementation approval while BP1 or BP2 is pending, stale, unclear, rejected, or unwaived.

The USER-facing planning files should avoid branch HEAD, SHA, origin/main, merge base, ZIP hash, and similar technical packet metadata. Technical metadata belongs in `START_HERE.md`, helper output, or Codex chat digests.

Runtime Branch Readiness should separate dense planning into:

- `Product Intent Summary`
- `Engineering Contract`
- `Decision Ledger`
- `Deferred / Future Ledger`
- `Implementation Sequence`
- `Proof Plan`

The user-facing packet should summarize each area and point to the Branch Runtime Engineering Plan for detail. The detailed plan remains in `Docs/branch_plans/<branch_slug>.md`; backlog and roadmap stay compact pointer/status surfaces.

## Branch Record / Plan / Workstream Fold-Down Model

Branch records, branch plans, and workstreams are related but not interchangeable.

Use this split:

- branch records own branch authority, approvals, phase history, blockers, legal next phase, and structured branch traceability receipts
- branch plans own detailed active runtime planning, Element-to-Phase Proof Matrix planning, and current element proof-path mapping while the branch is active
- workstreams and family dossiers own durable package trace, slice trace, proof history, reusable lessons, and family continuity

At PR Readiness, every runtime-focused branch needs a fold-down or retirement decision:

- retire the branch plan after durable content is migrated and no active branch depends on it
- preserve branch-specific evidence in a structured branch receipt when it is needed for later debugging, rollback analysis, or USER memory
- promote reusable lessons, package trace, slice trace, validators, and proof history to workstreams or family dossiers
- leave backlog and roadmap as compact pointers instead of copying the plan or trace tables

Traceability compaction must not mean evidence loss. Large branch records may remain large when they are the correct historical ledger, but they should be organized for USER review and Codex indexing: current summary first, clear historical sections, commit/PR/release evidence, changed-surface map, validation proof, and links to promoted workstream/family-dossier detail. The reform target is less chaos and less duplicate live state, not smaller files at the cost of useful evidence.

Historical receipts may preserve PRs, tags, releases, and commit hashes when they are evidence for a closed decision. They must not be presented as live operational truth or repeated across backlog and roadmap.

## Docs Organization Cleanup Pass Rule

When USER asks for a docs organization cleanup pass, the first pass is non-destructive unless USER explicitly approves exact file moves, renames, deletions, archival, or historical rewrites.

The cleanup pass must use `Docs/governance_docs_full_inventory_reform_audit.md` and `Docs/governance_docs_reform_user_review_index.md` as the review surface. It should classify and prioritize cleanup lanes, preserve source-truth owners, identify replacement owners before any retirement/delete recommendation, and return a Desktop review bundle with the files USER needs to inspect.

Safe cleanup planning may:

- clarify queue status and cleanup lane priority
- label oversized branch records for later structured-receipt organization
- label retired branch plans for later reference-proof review
- label low-risk reference docs for possible future consolidation
- identify missing indexes, README routing gaps, and owner-map ambiguity

Safe cleanup planning must not:

- move, rename, delete, archive, or rewrite historical files
- collapse historical receipts into summaries without replacement-owner proof
- treat branch records, backlog, roadmap, worktree slots, or `Docs/Main.md` as live-state ledgers
- mutate runtime, release, FAM, Compact-AI, issue, branch-cleanup, or worktree state

The default cleanup sequence is: inventory and classify, review queue and owner routing, choose one focused cleanup lane, create a USER review bundle, then request exact USER approval before any physical file or history-affecting change.

## Product Vision Contract Model

`Docs/nexus_vision.md` is the Nexus-wide product vision contract. It was promoted from the former `Docs/orin_vision.md` path after focused reference migration so Branch Readiness has a stable project-wide vision owner.

The vision contract should drive backlog-family planning and Branch Readiness recommendations. A backlog item may need its own family-level vision record or vision section when the product intent is not obvious, but that vision is not a branch plan and should not duplicate per-seam implementation detail. The vision explains what outcome the plan must satisfy; the Branch Runtime Engineering Plan explains how the active branch intends to implement and prove it.

Vision records should support USER/Codex back-and-forth. They may grow as implementation teaches the project, but changes should be explicit USER-reviewed product intent, not accidental branch-local drift.

Family vision records live under `Docs/family_visions/` and receive reusable vision updates folded down from PR Readiness only after USER acceptance. Backlog and roadmap point to those records; they do not copy full family vision narratives.

## Vision-To-Plan Interaction Loop

The Vision Contract layer complements Branch Runtime Engineering Plans. It does not create a parallel planning system.

Use this layer when product/design assumptions would otherwise become implementation truth by Codex inference:

- Nexus Vision owns project-wide principles, long-term standards, and durable product direction through `Docs/nexus_vision.md`.
- Family Vision owns broad feature-family direction through `Docs/family_visions/` when the family is large enough to justify a durable owner.
- Branch Vision Contract Snapshot lives inside the active Branch Engineering Plan and records the USER-accepted branch-specific vision state.
- Branch Engineering Plan translates the accepted snapshot into seams, files, validators, proof, and stop conditions.
- Vision Question Digest is the required packet when product/design uncertainty affects planning or execution.
- Branch Plan Revision Packet is the required packet when accepted vision or accepted branch scope needs controlled revision.
- Plan-to-Implementation Traceability proves that implementation followed accepted vision and the branch plan.

Design assumption states:

- `Proposed by Codex`
- `Recommended by ChatGPT`
- `Accepted by USER`
- `Revised by USER`
- `Rejected by USER`
- `Deferred by USER`
- `Deferred With Waiver`
- `Superseded`
- `Needs USER Decision`

Only `Accepted by USER`, `Revised by USER`, or `Deferred With Waiver` design states are implementation-safe for user-facing/runtime behavior. Codex and ChatGPT recommendations remain proposed evidence until USER acts on them.

Before Workstream implementation, runtime/user-facing branches should record `Branch Vision Snapshot Status: Accepted`, `Open Vision Questions: None` or `Deferred With Waiver`, `USER Vision Green: Yes`, accepted implementation scope, accepted seam map, and accepted stop conditions. After that green point, new questions use the severity ladder: Level 1 non-blocking questions queue for later review, Level 2 seam-blocking questions pause only the affected seam, and Level 3 workstream-breaking questions return a Branch Plan Revision Packet before affected scope continues.

Vision Contract is required for user-facing UI/UX behavior change, runtime behavior change, workflow hierarchy change, visual standard change, setup or activation behavior change, provider/model/memory/voice/Core behavior, returned UTS that changes target behavior, broad family planning, ambiguous acceptance criteria, conflicting prior source truth, or any Codex recommendation that would otherwise become product/design truth. It may be marked not required for mechanical docs-only repair, validator-only repair with no product/runtime/user-facing impact, release-body formatting repair, source-truth typo/format repair, or branch metadata repair when the reason is recorded.

Accepted assumptions expire or require review when branch scope changes, returned UTS changes the accepted target, family vision changes, source truth contradicts the prior assumption, new user-facing behavior appears, or implementation would apply an old decision to a new family or surface.

## USER Feedback Disposition Model

USER Feedback Disposition (UFD) preserves meaningful USER feedback without creating another permanent feedback ledger.

The active branch planning owner is the full-detail owner for UFD items while the branch is active. After the External Operational State Store transition, that active owner is external operational state or an approved worktree-local staging packet; repo branch plans preserve only transition-approved evidence or historical receipts. Branch records, backlog, roadmap, workstream docs, family dossiers, Nexus Vision, and family vision owners may carry compact UFD pointers or folded outcomes only when they are the correct owner for the final disposition.

The branch plan keeps one ledger-level owner through `UFD Ledger Owner:`, one `UFD Ledger Status:`, `Open UFD Count:`, `Blocking UFD Count:`, and `Fold-Down Status:`. Each meaningful feedback item lives in a repeatable `### UFD Item: UFD-<scope>-YYYYMMDD-NNN` block.

Every meaningful feedback item should have one UFD ID, one canonical owner file, one USER decision state, one disposition type, one item status, one Workstream severity, and one fold-down target. UFD IDs use `UFD-<scope>-YYYYMMDD-NNN`; `FBK-*` is not allowed because it collides visually with historical `FB-###` workstream records.

Meaningful feedback requires UFD disposition when it affects branch scope, accepted vision, user-facing behavior, runtime behavior, validation proof, future work, reusable product standards, approval boundaries, or a USER decision. Minor comments, acknowledgements, typo-level notes, duplicate remarks, or non-actionable conversation may close without durable UFD only when Codex records the no-action reason.

Pointer locations may carry UFD ID, short title, canonical owner, compact status, and fold-down status only. They must not carry full feedback text, full decision history, or live implementation state.

At PR Readiness, each UFD item must be migrated, deferred with waiver, rejected/no-action with reason, closed, or explicitly carried to a future owner. Fold-down must preserve a lookup path from every UFD ID to its final owner after branch-plan fold-down and retirement.

Initial validator support is marker-first. It validates UFD ledger markers, repeated UFD item blocks, UFD IDs, required owner/status/decision markers, `No Durable Owner Needed` guardrails, count consistency, fold-down lookup posture, and exact-normalized duplicate `Feedback Summary:` entries inside one active UFD ledger. Broader fuzzy semantic duplicate or conflict detection remains human-review territory unless future fixtures and false-positive review prove it safe.

## USER Review Integration Decisions

The 2026-05-21 USER review responses are model-changing requirements, not passive review notes.

Required decisions from that intake:

- Complete the Docs reform as staged internal work on this same Governance carrier and one final PR path; avoid revolving PRs for every subtopic.
- Keep `Docs/Main.md` as the least-updated canonical docs index, recovery map, and pointer ledger.
- Distinguish canonical docs from context docs. Canonical docs own law, routing, or source-truth roles; context docs preserve evidence, product reasoning, implementation history, receipts, or review detail.
- Treat Branch Runtime Engineering Plans as canonical planning contracts only in the approved active owner. After external-state transition, repo copies are transition receipts or historical receipts; fold down durable outcomes and retire them after durable content migrates. Deletion is not the default.
- Treat branch records as structured traceability receipts that may remain large when they preserve useful debugging, rollback, commit, PR, release, validation, and changed-surface evidence.
- Do not use "compaction" to erase traceability. The reform target is duplicate live-state removal, clearer organization, and owner routing.
- Delete or collapse low-risk/reference docs only after a reference scan, replacement owner, and USER acceptance prove the move is safe.
- Use `Docs/nexus_vision.md` as the Nexus Vision contract surface that drives backlog-family planning and Branch Readiness recommendations without duplicating branch plans.
- Use `Docs/family_visions/` for family-specific durable product direction while keeping backlog and roadmap compact.

The generated review dossier and index must expose these decisions through a USER response integration matrix, a single-PR staged execution plan, and explicit disposition changes. PR Readiness must stay held while USER is still correcting this model.

## USER Review Desktop Bundle Rule

When Codex asks USER to inspect repo files, review a generated dossier, approve a planning packet, or compare a source-truth reform surface, Codex must create or refresh the USER-facing stable Desktop review folder for the active worktree.

The Desktop bundle must:

- live under one stable Desktop root, `Nexus USER Review`, under the discovered Desktop path, preferring `C:\Users\<user>\OneDrive\Desktop\Nexus USER Review` when available and `C:\Users\<user>\Desktop\Nexus USER Review` otherwise
- use one child folder per active worktree label, derived from the current worktree root folder name when USER does not provide a label, such as `Governance`, `FAM-006`, or `FAM-007`
- refresh the same worktree-labeled child folder instead of creating a new top-level Desktop folder for each review packet
- copy the selected review files as flat files directly inside the worktree-labeled child folder, with traceable filenames when needed to avoid basename collisions, rather than creating constantly changing nested review folders
- block custom review roots, legacy one-off folder names, or manually supplied worktree labels unless USER grants an explicit custom review path waiver; when a waiver is used, `START_HERE.md` must record `Custom Review Path Waiver:` and `Custom Review Path Reason:`
- include a `START_HERE.md` file with `Review Purpose:`, source repo, `Source Branch:`, `Source HEAD:`, upstream, `origin/main:`, `Review Export Zip:`, `Review Export Zip Source HEAD:`, `Review Export Zip Stale Guard:`, `Validation Summary:`, `Review Order`, `Exact USER Decision This Bundle Supports:`, `Pending USER Decisions`, copied source paths, explicit bundle/copy file counts, and an extra-file count for stale artifacts left in non-cleared folders
- copy only the files relevant to the requested review, not the whole repo or unrelated artifacts
- preserve source traceability in `START_HERE.md` so every flat copied file maps back to its repo-relative source path
- be refreshed when the underlying review files change
- never replace source-truth files, commit artifacts, validation proof, or branch authority records

For Workstream Entry, the Desktop bundle is required before USER green-lights implementation when the branch has runtime, user-facing, source-truth, helper/validator, or workflow impact. The bundle must copy the branch vision, active external Branch Runtime Engineering Plan or approved transition Branch Engineering Plan, Element-to-Phase Proof Matrix owner, branch authority evidence pointer, relevant Nexus/family vision files, UFD/change-intent surfaces when applicable, and any other source-truth files the USER needs to inspect. The Workstream Entry digest must report the folder path, copied files, `USER Branch Plan Review Gate` status, `USER Review Packet Finding:`, and whole-package analysis status when multiple slices or seams are admitted. `USER Review Packet Finding:` must name `START_HERE.md`, `USER_BRANCH_PLAN_REVIEW.md`, the exported zip, packet source HEAD, current branch HEAD, freshness result, digest status, and waiver/blocker status. `USER_BRANCH_PLAN_REVIEW.md` must act as the USER-facing design review: it presents planned feature behavior, accessible surfaces, Codex recommendations, implementation options, design/scope questions, and a USER response area. Workstream implementation cannot begin until USER response is attached or inserted and Codex digests it into the Workstream Entry decision, or until USER explicitly waives that response/digest requirement. The bundle supports USER accepting, revising, deferring with waiver, rejecting, or requesting more analysis before implementation begins.

Branch Planning review reinforcement: BP1 / `USER_BRANCH_VISION_REVIEW.md` is the USER-facing product/design branch vision contract. BP2 / `USER_BRANCH_PLAN_REVIEW.md` is the USER Branch Plan Contract and engineering plan derived from accepted or waived BP1. BP1 helps USER decide whether the End-State Vision, Visual / Functional Walkthrough, planned feature look, feel, flow, and Nexus fit are right before bounded Workstream implementation. BP2 helps USER decide whether the engineering route correctly builds that accepted vision, with implementation package, scope size, SLC/seam route, affected surfaces/files, validators/helpers, proof requirements, H1/LV/UTS, rollback/safety, risks, future-gated boundaries, USER response, Codex digest, implementation constraints, Vision Delta / Source-Truth Impact, Contract Change Log, Contract Completion Checklist, waiver path, and Workstream Entry result area. `Contract Status` must be `Complete` or `Waived by USER` for required BP1/BP2 gates before implementation approval is legal; `Draft`, `Pending USER Response`, `Pending Codex Digest`, and `Pending USER Confirmation` block implementation. If USER feedback changes branch direction, feature shape, UI behavior, workflow, scope, boundaries, or seam order, Codex must update source truth, refresh the Desktop packet/ZIP, set Contract Status to Pending USER Confirmation, and wait for USER confirmation or explicit waiver.

For governance review or PR-readiness review, the Desktop bundle should be self-checking: `Bundle File Count:` reports the actual file count present in the worktree review folder after copy plus `START_HERE.md`, `Copied File Count:` counts copied repo files only, `Expected File Count:` must match the intended copied repo-file count, and `Extra Bundle File Count:` reports stale or unrelated files that remain when a bundle is refreshed without `--clear`. Use `dev/orin_user_review_bundle.py` for repeatable local bundle creation; the helper defaults to `Nexus USER Review\<worktree-label>` and should not require USER to name a new folder for active worktrees. The helper must also overwrite a stable zip export at `Nexus USER Review\<worktree-label>.zip` from the freshly refreshed worktree folder and record `Review Export Zip:`, `Review Export Zip Source HEAD:`, and `Review Export Zip Stale Guard:` in `START_HERE.md`; USER-uploadable review zips created outside this helper are stale-risk evidence and must be regenerated before review or PR Readiness. `--review-root-name`, `--worktree-label`, or legacy `--folder-name` customizations require `--allow-custom-review-path` plus a recorded reason. If the Desktop path cannot be discovered or the folder/zip cannot be created, stop with `USER Review Desktop Bundle Missing` and return the exact blocker plus the copy command or helper command USER can run.

## Standing Governance Ledger Compaction

The standing Governance record may keep one compact current cycle summary plus a latest closed cycle pointer.

Detailed historical RRI cycles should be folded into compact historical receipts, PR links, or appendices instead of forcing dedicated closeout PRs that only clear cycle wording.

Required current fields:

- `Active RRI Cycle:`
- `Latest Closed RRI Cycle:`
- `Intake State:`
- `Return Digest Status:`
- `Sync Rule:`
- `Next Legal Phase:`

## Release Ownership UX

Release Readiness remains file-frozen. Release execution requires separate approval.

When multiple runtime or governance PRs merge before the next release, the default release ownership model is:

- `Release Ownership Model: Aggregated release window`

A release assembler or release captain packages the selected release window. This role does not own implementation and may not mutate source truth during Release Readiness.

Release packets must distinguish:

- implementation contributors
- governance/readiness contributors
- excluded or future-gated work
- public user-facing highlights
- internal validation support that should not dominate public notes

## Public Language Mapping

Release and public-facing text should translate internal engineering work into user value.

Mapping fields:

- `Internal Scope:`
- `Public-Facing Scope:`
- `User-Visible Benefit:`
- `Excluded Work:`
- `Future-Gated Capabilities:`
- `Validation Confidence:`
- `Internal Jargon Review:`

Internal governance names, branch names, helper names, and automation wording should appear in public release notes only when needed for transparency.

## Validator Modularization Boundary

`dev/orin_branch_governance_validation.py` remains the stable CLI wrapper.

Future modularization may split internals into helper modules only if:

- the command interface stays stable
- existing validation output remains understandable
- module ownership is registered in `Docs/validation_helper_registry.md`
- the split is validated before any behavior-changing enforcement is added

Do not mix broad validator modularization with runtime implementation.

## Validation Runner And Registry Query Rule

Use `dev/orin_validation_suite.py` when a branch needs a validation recommendation packet.

That helper is report-only. It recommends commands with rationale and does not execute commands or mutate files.

## Naming Drift Scan Rule

Product/persona naming cleanup requires a named governance or product-surface carrier.

Historical GitHub tags, release titles, old branch records, and prior evidence may preserve old names as historical truth. Current public UI, release notes, branch plans, and new docs should avoid introducing retired/internal names unless the owning source truth explicitly allows historical context.

## Reform Pass Completion Model

The consolidated governance reform PR may complete the policy, pointer, and validator scaffolding for all reform categories in `Docs/governance_process_efficiency_reform_plan.md`.

For `RRI-20260521-001` and related USER-approved bounded governance/source-truth repair carriers, the USER direction is one single final PR with staged internal commits rather than revolving PRs. Analysis, model updates, and planning refinements may continue on the currently approved Governance worktree carrier until USER accepts the reform review surface; cleanup execution remains bounded by this model and PR Readiness stays held until USER approval.

It must not perform broad historical migration, branch deletion, worktree cleanup, runtime mutation, release execution, or FAM lane mutation. Those remain separate USER decisions.

## Next Legal Phase

After this operating model merges, future governance efficiency work should use the owner matrix and helper validation instead of creating new duplicate current-state surfaces.
