# Nexus Source-Of-Truth Index

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**
**Release Readiness anchor, aggregation, and contributor-inventory rules are owned by `Docs/phase_governance.md`. `Docs/Main.md` only routes to that owner so release-window details are not duplicated across governance files. Required field names: `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, `Candidate Includes Later Governance Repairs:`, `Release Window Contributor Inventory:`, `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, and `FAM Contributor Routing:`. Blockers: `Release Candidate Anchor Missing` and `Release Window Contributor Inventory Missing`.**
**Merge-stable source-truth projection is owned by `Docs/phase_governance.md` and `Docs/branch_records/index.md`, with validation in `dev/orin_branch_governance_validation.py --release-readiness-health-gate`. `Docs/Main.md` only routes to that owner. Required blockers: `Merge-Stable Source Truth Projection Missing` when merged-main current-state owners, compact pointer rows, worktree slot receipts, external active branch planning owners, or canonical branch records retain pre-PR / PR-creation-pending wording after a PR has merged; `Merged Active Branch Authority Not Folded Down` when a non-standing active branch authority record points to a branch ref that is already merged into `origin/main`; and `Merge-Stable Projection Shadowed By Active Authority` when a post-merge projection receipt exists but the same branch still remains under `Active Branch Authority Records`.**

## Purpose

This document is the routing authority for the merged Nexus Desktop AI canon.

Its job is to:

- define the current source-of-truth layers
- separate ownership between those layers
- point prompts and reviews toward the right authority docs
- prevent local branch overlays from being mistaken for merged truth

`Docs/Main.md` is a routing document.
It does not replace the authority of the docs it points to.

## Authoritative Baseline

Use these rules before trusting any planning or governance claim:

- `origin/main` is the authoritative baseline after merge and release
- the latest public tag or release is authoritative for released-version truth
- local unmerged branches, stashes, and docs overlays are reference material only until revalidated against updated `origin/main`
- if code, logs, and merged docs disagree, validate the live repo truth first and then repair the docs

## Derived Live Truth And Governance Receipts

Git and GitHub own volatile operational facts such as `HEAD`, worktree clean/dirty state, ahead/behind state, merge base, local/remote ref existence, live PR state, latest tag, latest GitHub Release, and issue state.

Repo docs are durable index/context files. They own governance law, USER decisions, phase approvals, product/architecture vision, source-truth routing, compact branch/document evidence pointers, release interpretation, and historical receipts after live truth has been checked.

Do not make backlog, roadmap, branch records, repo branch-plan files, worktree-slot records, or generated review surfaces manually own operational ledger material. They may point to the branch, PR, release, external-state owner, workstream, family vision, or historical receipt that proves context; they must not become the place where active status, current assignment, open PR state, release-window state, selected-next posture, or active branch-plan rows are maintained. Current operational truth and active branch planning must be derived from Git, GitHub, approved helpers, or `C:\Nexus Governance State` before mutation.

External operational state is a separate local coordination layer after USER-approved initialization. `Docs/governance_efficiency_operating_model.md` owns the External Operational State Store contract and transition drift gate: repo docs remain durable source truth, `C:\Nexus Governance State` is the accepted operational-state root after local bootstrap approval, `<worktree>\.nexus_state_staging\` is proposed staging only, and external governance candidates do not become binding governance until a USER-approved repo source-truth update merges. `Docs/external_operational_state_store_reform_plan.md` owns the Docs Split implementation plan, target matrix, annotations, approved-stage boundaries, completion posture, and future-work sequencing reference. External-state helpers may report, validate, preview, and produce dry-run packets unless a later USER-approved apply step explicitly authorizes mutation. Root initialization, Stage 4 active-state migration execution, Stage 5 validator transition, Stage 6 cleanup planning, Stage 6A compact pointer cleanup, Stage 6B branch-authority routing planning, Stage 6C branch-authority routing cleanup, Stage 6D branch-detail-record / branch-plan cleanup planning, and Stage 6E no-loss cleanup closure have occurred after separate USER approvals. `Docs/branch_records/index.md` keeps durable branch-record law, historical receipt routing, and the single standing Governance intake routing exception while non-standing active operational branch authority routes to `C:\Nexus Governance State\central\active_branch_authority_state.md`, branch-specific external records, and Git/GitHub/helper live checks. Branch detail records, repo branch-plan files, backlog, roadmap, and worktree slots may keep durable branch/document evidence pointers and historical receipts, but they must not own active/complete/pending lifecycle posture, selected-next current state, PR state, release-window state, watcher state, worktree assignment, or active branch-plan detail. Active branch plans live under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`; repo branch-plan files under `Docs/branch_plans/` are schema, transition evidence, retirement-index entries, or durable historical receipts only. Broad rewrites, movement, deletion, archive, worktree-local staging, FAM worktree mutation, and mandatory clean-clone external-state validation remain separate USER decisions.

## Workspace And Thread Identity Baseline

Nexus may use multiple local folders for the same GitHub repository, but `origin/main` remains the canonical remote source truth.

`Docs/worktree_slots.md` owns the stable slot registry and intended lane assignment model. It defines reusable slots such as `neutral-main`, `governance-standing`, `runtime-active-1`, `runtime-active-2`, `runtime-active-3`, and `archived-historical`.

Slot assignment is not active branch authority by itself. Repo branch records own durable authority law and historical receipts; accepted live posture belongs to `C:\Nexus Governance State` or Git/GitHub/helper-derived truth, with the standing Governance intake record as the only repo active-authority exception. A slot says where work is intended to happen; Git/GitHub and identity preflight prove what is actually checked out and mutable.

Current local workspace roles:

- `C:\Nexus Desktop AI` is the local main/consolidator workspace by default after workspace reconsolidation; tracked file edits on `main` remain blocked, and the folder becomes an active branch workspace only when the current branch record and Thread / Worktree Identity Preflight assign it
- `C:\Nexus Worktrees\` is the governed local root for active branch worktrees after workspace reconsolidation; retired worktrees there are not active carriers unless a current branch record names them
- `C:\Nexus Worktrees\Governance` is the only `Standing Governance Intake Branch` worktree; it uses `feature/release-readiness-source-truth-intake`, accepts a `Release Readiness digest` for release-blocker repair, USER-approved `automation/worktree governance intake` for non-runtime multi-worktree safety repair, and USER-approved `phase-gate governance intake` for repeatable non-runtime phase-gate miss prevention, uses `RRI-YYYYMMDD-NNN`, enforces `One Active Cycle`, requires the clean pre-intake `Sync Rule` to `origin/main`, pauses originating lanes in `Waiting For Governance Intake` or `Waiting For Updated Main`, and returns a post-merge `Return Digest` with exact originating branch, originating worktree, operating workspace, expected branch, and `Neutral Main Workspace Rebaseline:` proof copied from the accepted/closed intake instead of inferred from `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Governance`, GitHub Desktop, or current shell CWD
- A USER-approved bounded governance/source-truth repair branch may temporarily use `C:\Nexus Worktrees\Governance` only when `Docs/branch_records/index.md` lists an active branch authority record for that exact branch. That record must define the bounded scope, source-truth owners, validation posture, and merge-stable fold-down path, and it does not replace or rename the `Standing Governance Intake Branch`.
- `D:\Nexus Repos\Nexus Desktop AI Main` and `D:\Nexus Worktrees\` are retained fallback/historical workspace paths unless later USER-approved governance or identity preflight assigns them a current role
- `D:\Nexus Dev ORIN\` is the private/dev workspace root; content there is evidence only unless legally imported through repo governance
- `D:\Nexus Artifacts\` is the artifact/model/eval output root; content there is evidence only unless legally imported through repo governance
- other old `C:\` Nexus folders, including `C:\Nexus Desktop AI FAM-006`, are parked or fallback workspaces unless explicitly reactivated
- `codex/ai-llm-lab` is historical AI Lab planning traceability only; after USER-approved consolidation into the current feature branch it has no active local/remote branch ref and must not be recreated or reused without USER-approved repo governance
- active branch names must not use the `codex/` prefix; use `feature/` or another USER-approved non-`codex/` prefix, and treat historical `codex/` branch names as traceability only

Assigned parallel worktrees are allowed only when USER explicitly assigns separate Codex threads to separate branch worktrees and each thread's Thread / Worktree Identity Preflight proves the expected path, branch, upstream, `HEAD`, `origin/main`, clean state, write target, active thread owner, thread assignment status, worktree ownership ledger, intended write set, same-worktree/same-branch collision check, dirty-worktree collision check, dirty-worktree recovery packet posture, off-worktree work routing, Governance routing barrier, and new worktree decision gate.

Default assigned-worktree limit: two active branch worktrees across the repo. More than two active branch worktrees, or two worktrees touching the same files or source-truth owners, requires an explicit USER decision before work continues.

Parallel worktree governance markers that must be tracked when more than one branch worktree is active:

- Assigned Thread: which Codex thread owns the worktree
- Worktree Role: `active branch worktree`, `main/consolidator`, `parked fallback`, or `historical/lab context`
- Expected Branch / Upstream / HEAD / `origin/main`
- Source-Truth Owner and intended write target
- Changed-file set and shared-file overlap forecast against the other active worktree
- Branch health: clean/dirty state, ahead/behind state, merge-base freshness, merge forecast, PR state, and branch-retirement plan
- File health: uncommitted files, generated/log artifacts, validator/helper files, source-truth files, line-ending warnings, and cross-branch conflict risk
- Runtime/process owner and interactive validation owner
- Git operation owner, because related worktrees should use one Git operation at a time where practical
- GitHub Desktop folder binding if Desktop is used
- Worktree Ownership Ledger: external branch state/branch plan, the durable branch authority receipt, or approved helper output that records active thread owner and write set
- Same Worktree / Same Branch Collision Check: blocks when two active Codex threads target the same worktree or branch until USER selects one owner
- Dirty Worktree Collision Check: blocks unowned dirty tracked files before a new thread claims a worktree
- Dirty Worktree Recovery Packet: freeze mutation, inventory dirty files, identify owning thread per file, preserve or discard only with USER approval, and resume with one active owner
- Off-Worktree Work Routing: work discovered outside the assigned worktree or unrelated to the active branch must route to `C:\Nexus Worktrees\Governance`
- Governance Routing Barrier: Governance decides whether the work belongs to the current owner, an existing worktree/thread, a new worktree/thread, or a USER waiver
- New Worktree Decision Gate: new worktree/thread creation, activation, reassignment, or GitHub Desktop repo binding remains USER-gated after Governance routing analysis

Main/consolidator worktrees remain read-only for Codex file mutation. A parked or historical worktree does not become active merely because it exists on disk; it becomes active only when a current branch record plus preflight names it as the assigned worktree.

Assigned lane waiting posture is valid. A second Codex thread may sit in Release Readiness analysis, Branch Readiness Stage 1 analysis, or updated-main wait state with no created branch when it is waiting for another branch to merge before it can safely create or continue its own branch. In that posture, it must not mutate files, create a branch, or treat stale local source truth as authority; it must report `Waiting For Updated Main` or the closest canonical blocker until `origin/main` contains the needed merge data and the thread reruns identity preflight.

`Prompt-Entry Origin/Main Freshness Gate` is mandatory before every new or resumed repo-affecting Codex pass. Before planning, patching, validating, claiming green, entering or continuing a phase, handling PR/merge/release work, mutating a worktree, or recommending next work, Codex must fetch or prove current `origin/main`, compare the active worktree `HEAD`, upstream, and merge base to `origin/main`, and report `Prompt-Entry Freshness Check:`, `Fetched origin/main:`, `Origin/Main Advanced Since Last Action:`, `Pre-Rebaseline Impact Audit Required:`, and `Rebaseline/Reconciliation Status:`. If `origin/main` advanced or cannot be proven current, stop on `Prompt-Entry Origin/Main Freshness Missing` or `Origin/Main Advanced Rebaseline Required` and return the report-only freshness/rebaseline packet before any mutation or phase continuation; validating locally is not enough.

`Pre-Rebaseline Impact Audit` is the repo-wide safety gate before any worktree baselines to newer `origin/main`. No Baseline By Inertia: being clean, behind, or fast-forwardable does not authorize mutation. The audit must report `Incoming Main Change Set:`, `Incoming Changed Files:`, `Current Worktree Changed Files:`, `Branch Changed Files:`, `Rebaseline Overlap Files:`, `Incoming Runtime / Source-Truth Risk:`, `Shared Surface / Worktree Overlap Forecast:`, `Validation Before Rebaseline:`, `Recommendation Only:`, `Rebaseline Mutation Approval:`, and `Rebaseline Mutation Status:` before Codex may merge, rebase, fast-forward, branch-switch, conflict-resolve, or run current-main reconciliation. When `Rebaseline Overlap Files:` is not `None`, `Rebaseline Overlap Intent Gate` applies: the active branch planning owner in external operational state owns full `Branch Change Intent Ledger` evidence; repo branch-plan files may only provide historical or transition fallback evidence. The packet must report `Overall Overlap Gate Result:`, and `Rebaseline Overlap Intent Missing` blocks mutation until overlap intent is repaired, waived, deferred by USER decision, or sequencing changes.

Automation Observability is multi-worktree aware. `dev/automation_observability_report.py` reads Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`, but those reports are evidence only until classified as `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED`. Each standing automation must declare a configured cwd that resolves to a known worktree, and reports must include cwd/worktree/branch/`HEAD`/`origin/main` evidence before lane-sensitive findings affect source truth. `Automation CWD Worktree Mismatch` blocks any active-branch, PR Readiness, Release Readiness, post-merge, release-window, selected-next, toolchain, or branch-governance automation that runs from stale neutral main, a missing cwd, or the wrong assigned worktree.

Automation reliability is graded by current source-truth ownership, not by stale automation memory. Background observability automations may report historical path drift, but stale toolchain-path findings are informational unless current source truth still owns the referenced path. Neutral-main background audits must require fresh main equality before reporting blockers. A PR watcher, merge watcher, or same-PR repair loop is phase-critical only when it has current PR binding, configured-cwd proof, delivery/runtime proof, and approved repair authority for the current branch; otherwise it is background observability and cannot clear PR Readiness, Release Readiness, or merge-watch gates.

`Docs/pr_watcher_mode_contract.md` owns the PR Watcher Mode Contract. PR watchers must declare `Silent Monitor`, `Verify Once`, `Repair Mode`, or `Blocked Mode`, and PR Readiness Stage 2 must include `Watcher Health Proof:` with configured cwd, PR number, head SHA, unresolved review-thread count, latest bot review, repair authority, delivery route proof, runtime proof, and next watcher posture.

PR Readiness Stage 2 approval includes watcher provisioning by default. Codex must not require a separate watcher-specific approval after USER approves PR creation / Stage 2 execution; skipping the watcher requires an explicit USER watcher waiver or a documented platform/runtime blocker.

`Docs/governance_efficiency_operating_model.md` owns the governance efficiency operating model. Use it for Rule ID / owner / compact mirror decisions, duplicate live-state prevention, the External Operational State Store contract, current-summary versus historical-appendix split, phase alias UX, release ownership UX, public language mapping, and the reform pass completion boundary.

Docs Source-Truth Reform Model: Compact Pointer Layer. `Docs/governance_docs_full_inventory_reform_audit.md` is the full Docs inventory and reform audit. The accepted ownership direction is backlog as compact product registry, roadmap as pre-Beta/Beta/release stage-breakpoint schedule outline, worktree slots as reusable slot assignment receipts, branch records as authority/structured traceability receipts, external operational state as the active branch status and active branch planning owner, repo branch-plan files as schema/transition/historical receipts that retire after fold-down, workstreams/family dossiers as durable package/slice/proof history, and Git/GitHub/helpers as live operational truth.

Before branch creation, worktree creation, phase entry, commit, push, PR work, release work, or GitHub Desktop handoff, run a `Thread / Worktree Identity Preflight` and prove the active thread is operating in the intended workspace, repository root, branch, upstream, `HEAD`, `origin/main`, worktree role, clean state, write target, active thread owner, thread assignment status, and intended write set. If the identity does not match the requested work, stop on `Thread / Worktree Identity Mismatch`; if another active thread owns the same worktree or branch, stop on `Parallel Worktree Coordination Missing`; if the target worktree is already dirty and ownership is unclear, stop for a `Dirty Worktree Recovery Packet`; if the work belongs outside the assigned worktree or active branch scope, route it to Governance instead of self-activating a sibling worktree.

Thread Launch / Write-Target Identity Lock:

- before meaningful repo work or file mutation, Codex must verify chat lane identity, repo path identity, branch identity, upstream/origin-main identity, worktree role, expected phase/seam, intended write target, clean/dirty state, runtime/process ownership when relevant, and GitHub Desktop folder binding when relevant
- stale parked branches, lab context, old worktrees, fallback folders, or mismatched GitHub Desktop bindings must stop with a routing packet before mutation
- the routing packet must report expected workspace, actual workspace, expected branch, actual branch, expected write target, actual write target, expected phase/seam, actual repo state, mismatch evidence, and safest next correction
- no source-truth update, branch/worktree creation, commit, push, PR action, release action, shortcut mutation, runtime launch for validation, provider/model install, or GitHub Desktop handoff may proceed until the identity lock passes or USER explicitly routes the work to the corrected target

Bounded State Lock:

- before mutation or execution, Codex must also prove `Bounded State:` for the exact phase/stage, workspace, branch, write target, owning authority record, active package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase
- if any bounded-state field is missing, stale, or ambiguous, stop on `Bounded State Missing`
- broad work requests do not authorize implementation; `continue`, `complete all`, `all remaining work`, `finish the branch`, or similar wording may execute only when source truth resolves it to one exact active bounded seam
- widening beyond that seam requires `Bounded State User Waiver: Granted`; without explicit waiver text naming the branch/worktree, phase, slice/seam, relaxed bound, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions, stop on `Bounded State Waiver Missing`
- clean validation, branch existence, prompt wording, Codex discretion, or ChatGPT wording cannot infer a bounded-state waiver

Formal Next Legal Phase Digest:

`Docs/phase_governance.md` owns the formal `Next Legal Phase Digest` field contract and the `Next Legal Phase Digest Missing` blocker. `Docs/Main.md` only routes Codex to that owner; it must not duplicate the full digest-field policy.

## Protected Main Law

`main` is a protected branch for Codex work.

Codex must not edit, stage, commit, generate, refresh, or directly repair repository files on `main`.
`main` may be read for truth validation, release review, merge verification, and post-release verification only.

There is no emergency direct-main repair path for Codex.
If drift is discovered:

- before merge, return to the owning branch and repair it before PR green
- after merge, do not open or resurrect a standalone repair branch for that drift
- block the next legitimate runtime-focused backlog branch in `Branch Readiness` and repair the drift there before implementation

Any tracked file mutation while Codex is on `main` is a `Main Write Attempt` blocker.

## Layered Ownership Model

Use this ownership split unless a validated source conflict requires a temporary narrower override:

- backlog = identity and registry
- workstream docs = promoted-work feature-state, branch-local evidence, active seam references, artifact history, branch-local reuse notes, and closure history
- roadmap = stage-breakpoint schedule outline and broad milestone checkpoints, not a release ledger
- rebaselines and closeouts = epoch or milestone summaries
- incident patterns = generalized reusable lessons
- bug tracking = backlog-first, with promoted bug docs only when warranted
- User Test Summary = validation-contract layer owned by the relevant workstream
- phase governance = repo-wide execution, proof, timeout, seam, stop-loss, validation-helper, and desktop UI audit contract
- validation helper registry = repo-wide helper naming, ownership, reuse, workstream-scoped exception, and consolidation contract
- branch authority records = repo-owned phase owners for selected `Registry-only` backlog branches in `Branch Readiness`, approved `release packaging` branches, active runtime-focused branches that must carry bounded governance/source-of-truth repairs before PR green, the single standing Release Readiness source-truth intake lane, and preserved historical repair records; standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work
- worktree slots = stable slot registry and intended lane assignment model in `Docs/worktree_slots.md`; it records slot roles and assignment receipts but does not own volatile live Git/GitHub facts or active branch authority
- Branch Runtime Engineering Plan = branch/worktree-specific detailed runtime execution blueprint for runtime-focused branches under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`; the branch authority record remains the durable receipt/control pointer, backlog and roadmap remain compact pointer/status surfaces, and PR Readiness fold-down decides what becomes historical branch receipt or promoted workstream/family-dossier truth
- USER Feedback Disposition = active branch-plan feedback preservation model under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`; full feedback text lives in one active owner, while branch records, repo branch-plan receipts, backlog, roadmap, vision docs, workstreams, and family dossiers carry compact UFD pointers or folded outcomes only
- Element Validation Ledger = row-level created/touched/affected/deferred/future element proof tracking owned by the existing workstream doc or branch authority record; it is not a new standalone active source-truth layer by default
- `Docs/nexus_startup_contract.md` = ChatGPT/new-chat loader map and prompt-generation guardrail owner, including the Nexus Prompt Gate final scrub rule; it is not Codex execution authority unless prompt generation, bootstrap continuity, or loader/source-truth drift review is in scope
- `Docs/Main.md` = routing authority aligned to merged truth

## Main-First Loader Chain

`Docs/Main.md` is the first repo loader for Codex execution. Codex should load Main first, then follow this index to the directly relevant owner docs instead of treating a prompt, context doc, branch overlay, or copied review file as complete source truth.

Main routes Codex to:

- execution posture: `Docs/development_rules.md`, `Docs/phase_governance.md`, and `Docs/codex_modes.md`
- ChatGPT prompt-generation guardrails: `Docs/nexus_startup_contract.md`
- project-wide product/design vision: `Docs/nexus_vision.md`
- AI runtime/trust architecture, permission-state, deterministic-routing, Trust Journal, AI operational cache, and cross-family AI-native placement: `Docs/ai_runtime_and_trust_architecture.md`
- public-safe AI edition/trust-boundary planning: `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`
- reusable family vision: `Docs/family_visions/`
- branch authority law, standing Governance intake exception, and historical receipts: `Docs/branch_records/`
- active branch vision, planning, UFD, Element-to-Phase Proof Matrix, and Branch Change Intent Ledger: `C:\Nexus Governance State\branches\<branch_slug>\`
- workstream and family implementation history: `Docs/workstreams/`
- digest profiles and non-compaction standards: `Docs/governance_intake_triage_and_digest_profiles.md`
- source-truth ownership, External Operational State Store contract, and USER review bundle rules: `Docs/governance_efficiency_operating_model.md`
- external-state Docs Split implementation plan, target matrix, approved-stage boundaries, migration-map helper posture, annotations, and future-work sequencing: `Docs/external_operational_state_store_reform_plan.md`
- helper and validator ownership plus the rule that validation output is evidence, not final authority: `Docs/validation_helper_registry.md`

Context docs may explain, summarize, or point to the owners above. They must not supersede Main or the named owner. If a context doc conflicts with Main or the relevant owner, Codex must follow Main to the owner, report the conflict, and repair through the legal branch/phase instead of inferring behavior.

Vision routing follows this chain: `Docs/nexus_vision.md` for project-wide vision, `Docs/ai_runtime_and_trust_architecture.md` for cross-family AI-native runtime/trust architecture, `Docs/family_visions/` for reusable family-level vision, and the active external branch planning owner for the Branch Vision Contract Snapshot and implementation proof. Codex must not promote proposed product/design ideas into durable vision owners by inference.

## Analysis-First Prompt Baseline

For system analysis, post-release review, branch-start planning, or source-of-truth audit:

1. read `Docs/Main.md`
2. read `Docs/development_rules.md`
3. read `Docs/phase_governance.md`
4. read `Docs/codex_modes.md`
5. add the directly relevant authority docs for the task
6. add only the live repo evidence needed to validate current truth

Do not narrow the docs set before the system structure, drift, and authority boundaries are understood.

## ChatGPT Loader Contract

For prompt generation and new-chat bootstrapping, use `Docs/nexus_startup_contract.md` as the compact loader map.

That file is ChatGPT-facing and interface-only.
It helps generate complete prompts that load the correct source-of-truth without pasting the full governance stack.
Local ChatGPT custom instructions should stay compact; the repo loader/source-truth may hold longer ChatGPT-facing continuity rules and review memory without becoming Codex execution authority.
Do not paste the loader doc into Codex prompts. Codex prompts should load `Docs/Main.md` and the owning canon for execution authority, using the loader only when prompt generation, new-chat bootstrapping, or loader/source-truth drift review is in scope.
Planning-loop blocking belongs in ChatGPT preflight analysis before prompt generation.
Once a prompt is allowed, it should stay thin, neutral, and repo-aligned instead of carrying behavior-management lists or protective governance narration.
It does not own Codex execution behavior, phase transitions, seam continuation, durability, validation, release rules, or branch authority.
Codex execution remains governed by the owning canon documents listed in this index, especially `Docs/development_rules.md`, `Docs/phase_governance.md`, `Docs/codex_modes.md`, and the active workstream or branch authority record.
ChatGPT-authored prompt additions are analysis/review input only: they may add evidence checks, validation reminders, review questions, and candidate blockers for Codex to reconcile against repo canon, but they must not become a second governing authority or remove, narrow, reorder, or prohibit canon-required Codex steps without USER-approved source-truth change.

If repo truth resolves to blocked `No Active Branch`, `Next Safe Move` must report the blocking repair path instead of inventing a later phase.
If repo truth resolves to steady-state `No Active Branch`, `Next Safe Move` may truthfully say that no branch should open yet or may name a release-packaging branch whose admission rules pass.
Governance-only branches are not used for new Nexus work.
Family-scoped Branch Readiness candidate selection must stay inside the assigned family/lane unless USER explicitly approves cross-family routing; other families may be inspected only for overlap, dependency, conflict, or pending-decision context.
Loader/source-truth continuity must preserve the broad FAM model, PR evidence-only handling, legacy global FB historical-only handling, single-slice and package-completion blockers, Element Coverage as non-identity, Branch/PR Readiness Stage 1 / Stage 2, Branch Readiness Stage 1 successor-selection ownership, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and the Windows-first, modular, GPU-aware direction with optional heavy local AI capability packs and CPU fallback.

## Routing Layers

### Governance And Prompting

Use these for workflow posture, prompt framing, lifecycle rules, and execution scaffolding:

- `Docs/nexus_startup_contract.md`
- `Docs/development_rules.md`
- `Docs/phase_governance.md`
- `Docs/Main.md`
- `Docs/codex_modes.md`
- `Docs/orin_task_template.md`
- `Docs/codex_user_guide.md`
- `Docs/worktree_slots.md`
- `Docs/governance_process_efficiency_reform_plan.md`
- `Docs/governance_efficiency_operating_model.md`
- `Docs/governance_phase_lifecycle_reform_context_plan.md`
- `Docs/governance_intake_triage_and_digest_profiles.md`

Repo-wide validation-helper rules also live in this governance layer.
Broad governance reform uses the `Governance Intake Triage Packet`, smallest legal `Digest Profile`, and `Digest Non-Compaction Rule` standards from `Docs/governance_intake_triage_and_digest_profiles.md`; selecting a focused profile must not compact the digest ever.
Formal Next Legal Phase Digest guidance is owned by `Docs/phase_governance.md`; use that owner for the required field contract, plan-review fields, non-compaction rule, and `Next Legal Phase Digest Missing` blocker.
When a governance change risks duplicating policy or live state, use the governance efficiency operating model instead of creating another current-state owner.
When a governance change concerns active branch state, active external branch plans, worktree assignment, release-window assembly, PR watcher state, review-bundle manifests, rebaseline packets, handoff digests, fold-down previews, cross-worktree lessons, governance candidates, worktree acknowledgements, external-state schema, state-promotion packets, repo live-state leakage, Docs split migration, or external-state helper/bootstrap work, load `Docs/governance_efficiency_operating_model.md` and `Docs/external_operational_state_store_reform_plan.md` before adding or updating repo-tracked state. Report `External State Transition Gate:` before PR Readiness on any external-state reform branch so Stage 0 planning, helper/bootstrap approval, root initialization, validator transition, active-state migration, repo cleanup, and completion cannot be blurred together. Treat any new repo-file ownership of active branch status or active branch-plan rows as governance drift.
When Codex asks USER to inspect repo files or approve a review packet, the `USER Review Hub Rule` in `Docs/governance_efficiency_operating_model.md` requires the local active hub `C:\Nexus USER`, a worktree-labeled child folder derived from the active worktree when USER does not provide one, root `START_HERE.md`, exactly one primary current-gate decision file under `USER Review`, generated supporting digests/checklists under `Review Aids`, copied repo context under `Source Truth Context`, and exactly one timestamped USER upload zip named `C:\Nexus USER\<worktree-label>__YYYYMMDD-HHMMSS.zip`. Codex should tell USER to upload that timestamped zip so repeated same-name uploads do not collide in ChatGPT or other review surfaces. The stable folder remains canonical for readable local review; no same-name stable upload zip is generated. Cloud-backed Desktop / OneDrive review locations are backup or convenience mirrors only. For Branch Planning, this packet supports BP1 `USER Branch Vision Review`, BP2 `USER Branch Plan Review`, and BP3 `Workstream Entry / Orchestration Validation`, and must include the files USER needs to accept, revise, defer with waiver, reject, or request more analysis before implementation begins. `USER_BRANCH_VISION_REVIEW.md` is the required BP1 Branch Vision Contract when branch vision review applies. `USER_BRANCH_PLAN_REVIEW.md` is the required BP2 Branch Plan Contract when engineering plan review applies. The Branch Planning digest must include `USER Review Packet Finding:` proving the packet was loaded and digested, or naming the exact waiver/blocker. It must distinguish `Packet Reviewability State` from `USER Gate State`; a reviewable or validator-green packet starts USER inspection and is not USER acceptance. Implementation remains blocked until BP1/BP2 are accepted or waived, BP3 is approved or waived, and USER separately approves the bounded implementation seam or sequence. If USER feedback changes direction, UI behavior, workflow, scope, boundaries, or seam order, Codex must refresh source truth and the packet, set Contract Status to Pending USER Confirmation, and wait for USER confirmation.
Use `Docs/nexus_startup_contract.md` as the compact ChatGPT/new-chat loader map only.

Branch Planning Review Reinforcement: `USER_BRANCH_VISION_REVIEW.md` is the BP1 user-facing Branch Vision gate and `USER_BRANCH_PLAN_REVIEW.md` is the BP2 user-facing engineering Branch Plan gate before bounded Workstream implementation, not a normal Codex status digest. The named BP2 checkpoint is the `USER Branch Plan Review Gate`. BP1 must include Project Vision Context, Family Vision Context, Feature Vision Context, End-State Vision, what USER will actually see and where, functional flow, Surface Map, options, Codex recommendations, USER response, Codex digest, accepted Branch Vision, deferred/future-gated ideas, and decision status. BP2 must include Accepted Branch Vision Summary, implementation package summary, branch scope size test, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, H1/LV/UTS expectations, rollback/safety plan, risks, future-gated boundaries, plan review list, and BP3 approval text. SLC details are implementation staging notes only and must not be presented as the main thing USER is deciding.
Do not treat it as execution authority.
Use `Docs/phase_governance.md` for the exact phase enum, blocker rules, branch classes, phase resolver, validation helper contract, proof hierarchy, default-budget closeout rule, and desktop UI audit rule instead of recreating those rules inside a workstream doc.

### Product And Boundary Truth

Use these for current product posture, architecture boundaries, and release-stage meaning:

- `Docs/architecture.md`
- `Docs/nexus_vision.md`
- `Docs/ai_runtime_and_trust_architecture.md`
- `Docs/family_visions/`
- `Docs/orchestration.md`

These remain authoritative for their layer even where older naming or path references still need later normalization.
When a task depends on future post-Beta AI behavior, AI-native operating experience, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, privacy posture, local-vs-external execution boundaries, capability-pack architecture, or AI/UI identity, route first to `Docs/nexus_vision.md` for project-wide vision, then to `Docs/ai_runtime_and_trust_architecture.md` for cross-family architecture/policy, and then to `Docs/family_visions/` for family-specific durable direction rather than duplicating that intent in roadmap, backlog, or workstream docs.
When a branch touches architecture, experience, cross-family policy, AI reliability, provider/cache/trust behavior, privacy boundaries, capability-pack domains, or source-truth ownership, require the `Architecture / Experience / Policy Impact Matrix` from `Docs/phase_governance.md` and `Docs/branch_plans/README.md`. The matrix routes impact to existing owners first and cannot create a new owner or FAM without `No Existing Owner Fits` proof and USER approval.
When AI behavior is planned, classify user-facing AI output by the reliability model in `Docs/ai_runtime_and_trust_architecture.md`: deterministic facts require proof, high-confidence conclusions require evidence and uncertainty basis, advisory outputs require tradeoffs, exploratory outputs must label hypotheses, and creative outputs require USER acceptance before implementation.

### Registry And Sequencing

Use these for tracked identity and near-term sequencing:

- `Docs/feature_backlog.md`
- `Docs/prebeta_roadmap.md`

Rules:

- backlog owns identity
- backlog identity is the user-facing feature-family registry by default
- canonical backlog identity model: `FAM` is a broad long-lived product family; `Package` is a bulk branch/release package under exactly one FAM; `Slice` is a traceable deliverable area inside one package; `Seam` is an execution/validation checkpoint; `PR` is merge/review evidence only; legacy global `FB` is historical trace only
- live backlog-family identities use the fresh broad `FAM-###` namespace starting at `FAM-001`; the current admitted registry ends at `FAM-008`, and legacy `FB-###` IDs are historical trace only and must not be reused for new parseable backlog entries
- the next USER-approved backlog family may use `FAM-009`; workspace/data and safety/privacy concepts are folded into existing owners instead of occupying backlog-family numbers
- branches should be family packages containing multiple admitted slices by default, not one branchable item per small feature or seam
- backlog families are not dependency queues for each other; if a branch needs another family's work, it must defer or wait for the owning family/worktree instead of implementing another family's responsibilities
- single-slice packages are blocked by `Single-Slice Package User Approval Missing` unless explicit USER approval records `Single-Slice Package User Approval: Granted`
- package slices must trace to exactly one FAM and exactly one package, and Workstream must continue through all admitted package slices until package completion state is recorded before Hardening
- Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.
- If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.
- Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.
- A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.
- A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
- Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
- Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
- Before any final response during `Workstream`, Codex must run a `Post-Seam Continuation Self-Audit` against the governed markers it just wrote or validated.
- If `Completion Status: In Progress` and `Continue Decision: Continue`, the self-audit result must be `Continue Same Workstream` and Codex must start the next active Workstream seam in the same bounded run.
- If Codex cannot start the next seam after that self-audit, it must record `Completion Status: Red` with the exact named blocker or USER waiver needed; it must not return a green seam closeout as terminal.
- `Continuation Execution Latch` remains active whenever `Continue Decision: Continue`, `Stop Basis: None`, and a same-phase `Next Active Seam` are recorded; Codex must execute the next seam in the same bounded Workstream run instead of returning a terminal report.
- user-facing family/package branches must declare an `Interface Release Boundary` in Branch Readiness before Workstream begins or resumes
- the default is one primary user-facing interface release surface per branch, recorded as `Primary Interface Release Surface:` with fallback point, acceptance criteria, and proof path
- multiple released user-facing interfaces in one branch require explicit `Interface Bundle User Approval: Granted`; otherwise block on `Interface Release Boundary Missing`, `Primary Interface Undefined`, `Multiple Interface Release Drift`, `Fallback Point Missing`, `Interface Acceptance Missing`, or `Branch Readiness Interface Planning Incomplete`
- this interface-release rule limits release sprawl; it does not authorize single-seam or single-slice Workstream behavior, and multiple seams/slices remain expected inside the approved primary interface boundary
- Element Coverage is a non-identity checklist owned by FAM/package analysis only; coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact
- Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers
- admitted-slice counting is explicit: only `Admission State: Admitted` slice rows count toward the multi-slice package rule; historical evidence rows, future placeholders, deferred ideas, and future-package-required rows preserve trace but do not satisfy package admission
- an admitted slice must be concrete and carry `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder slices cannot be marked admitted
- `Package Completion State: Complete` is blocked while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while another admitted package slice remains incomplete
- separate backlog identities for non-user-facing runtime, developer-tooling, docs/governance, or canon-only work require explicit USER approval
- Codex must not create, split, promote, or select a new backlog identity without explicit USER approval
- if Codex reaches a point where it believes a backlog identity, package admission, branch creation, backlog split, promotion, selected-next successor, or single-slice package waiver is needed but approval is absent, stop on `Backlog Addition User Approval Missing` and output the still-not-closed FAM list plus every not-complete package and slice; if that list is empty, stop on `Backlog Exhaustion User Decision Pending`
- small single-seam runtime proofs, validation follow-through, governance repairs, and blocker-clearing traces belong in workstream docs, family dossiers, branch records, or historical PR trace by default, not as new backlog IDs or standalone release-version drivers
- backlog is not the seam-by-seam traceability surface for continuation, blocker-clearing, or validator follow-through; canonical workstreams and branch authority records own that history
- historical pass aliases, support/governance lanes, old registry-only implemented IDs, and all legacy `FB-###` references in `Docs/feature_backlog.md` are trace rows only; do not treat them as live backlog identities or selected-next candidates
- continuation or reopening on an existing feature family should reuse that same backlog identity by default unless the USER explicitly approves a backlog split or the work is materially a new user-facing feature family
- Assigned Worktree Confinement is required for assigned Codex threads: branch records must report `Active Thread Owner:`, `Thread Assignment Status:`, `Worktree Ownership Ledger:`, `Intended Write Set:`, `Same Worktree / Same Branch Collision Check:`, `Dirty Worktree Collision Check:`, `Dirty Worktree Recovery Packet:`, `Off-Worktree Work Routing:`, `Governance Routing Barrier:`, `New Worktree Decision Gate:`, `Expected Worktree Root:`, `Actual Worktree Root:`, `No Cross-Worktree Mutation:`, and `GitHub Desktop-bound worktree`; operating outside the assigned root blocks on `Worktree Escape User Waiver Missing` until USER grants `Worktree Escape User Waiver: Granted` with exact scope, duration, validation, and return path
- backlog candidate selection is priority-led; `Priority` and deferred-context fields are the selection inputs for open items
- `Target Version` is not an open-backlog selection input and belongs only to release posture, release debt, or historical closed/implemented evidence
- deferred open backlog entries must explain `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:` before they can be selected efficiently
- roadmap owns stage-breakpoint schedule outline and broad milestone checkpoints
- neither backlog nor roadmap should retain the full execution story once a canonical workstream record exists

### Canonical Workstream Records

Use these for promoted work that needs a stable feature-state, branch-local validation/evidence record, active seam trail, durable artifact/reuse history, and closure history:

For the family-governance model, use `Docs/workstreams/index.md` first to distinguish feature-family anchors, historical family-pass records, and other closed trace records before loading the specific canonical record.

- `Docs/workstreams/index.md`
- `Docs/workstreams/FB-027_interaction_system_baseline.md`
- `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
- `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
- `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md`
- `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md`
- `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md`
- `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md`
- `Docs/workstreams/FB-005_workspace_and_folder_organization.md`
- `Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md`
- `Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md`
- `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md`
- `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md`
- `Docs/workstreams/FB-004_future_boot_orchestrator_layer.md`
- `Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md`
- `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md`
- `Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md`
- `Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md`
- `Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md`
- `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`
- `Docs/workstreams/FB-036_saved_action_authoring.md`
- `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md`
- `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
- `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`
- `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`
- `Docs/workstreams/FB-028_history_state_relocation.md`

### Family Dossiers And Historical Pass Trace Routing

Use these for additive family-lifetime traceability surfaces that layer over existing workstream history without replacing the canonical workstream docs in one pass:

- load the `Lifetime Dossier Doc` named by backlog or roadmap when the task touches a `Feature Family` anchor or a historical family-pass trace row
- use `Docs/workstreams/index.md` to locate the split feature-family anchor versus historical-pass record set before choosing the exact canonical workstream doc

- `Docs/workstreams/index.md`
- `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
- `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`

### Branch Authority Records

Use these for selected `Registry-only` backlog branches in `Branch Readiness`, and for approved branches that do not map to a promoted backlog workstream but still need durable repo-owned authority law or historical receipt evidence:

- `Docs/branch_records/index.md`
- the relevant standing Governance intake authority record or historical branch receipt under `Docs/branch_records/`

### Rebaselines And Closeouts

Use these for closeout policy, historical closeout lookup, and the modern Nexus-era baseline summary:

- `Docs/closeout_guidance.md`
- `Docs/closeout_index.md`
- `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`

Historical closeout leaf docs are intentionally routed through `Docs/closeout_index.md`.

### Incident Patterns

Use this layer for generalized debugging and validation lessons:

- `Docs/incident_patterns.md`

Keep branch-local "what worked" notes in the canonical workstream doc first.
Distill only generalized cross-branch lessons into `Docs/incident_patterns.md`.

### Validation Guidance

Use this when a task depends on manual validation handoff, User Test Summary structure, returned test-evidence digestion, implementation-output requirements for a `## User Test Summary` section, or the canonical repo-level `UTS` artifact for an active workstream:

- `Docs/user_test_summary_guidance.md`
- `Docs/validation_helper_registry.md` when the task creates, extends, names, promotes, consolidates, or relies on a validation helper, live-validation script, audit helper, harness, or shared validation support under `dev/`
- the relevant canonical workstream doc under `Docs/workstreams/`, which also owns the active lane's canonical repo-level `UTS` artifact and any durable artifact-history or artifact-reference section for branch-local validation/support assets when that workstream has created them
- `Docs/development_rules.md` when the task also depends on implementation-time validation depth, supporting validation artifacts, required evidence trails, hardening expectations, or the interactive OS-level continuation gate
- `Docs/phase_governance.md` when the task also depends on the repo-wide validation helper contract, marker-first proof hierarchy, gating-vs-non-gating observation rules, default-budget closeout expectations, or the desktop UI audit rule

### Auxiliary Planning References

Use these only when the task directly depends on their planning content:

- `Docs/boot_access_design.md`
- `Docs/orin_interaction_architecture.md`
- `Docs/workspace_layout_plan.md`
- `Docs/orin_display_naming_guidance.md`
- `Docs/ncp_hardening_assessment.md`
- `Docs/ownership_ip_plan.md`

These are reference layers, not active workstream or roadmap owners.

## Routing Rules

- route through the layer that owns the truth you need
- when work is phase-sensitive, route through `Docs/phase_governance.md` before choosing execution posture
- require the exact prompt contract from `Docs/phase_governance.md` before phase-sensitive execution
- prefer index docs for historical or high-cardinality layers
- do not treat a local-only document as canonical just because it exists in the workspace
- keep future post-Beta AI behavior, privacy, and execution intent in `Docs/nexus_vision.md` until a later selected workstream turns part of it into execution truth
- do not create duplicate authority by making backlog, roadmap, and workstream docs all carry the same execution story
- do not treat workstream docs as the owner of repo-wide phase, timeout, stop-loss, proof-authority, validation-helper, or desktop UI audit rules; those belong to `Docs/phase_governance.md`
- keep historical Nexus material preserved, but mark it as historical rather than current reality
- during the normal active-branch-first `pre-Beta` flow, governance and canon updates should ride on the active current branch when they are directly required to keep that branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct
- active-branch governance or canon updates must stay inside the current branch's approved phase, branch class, and scope; they must not weaken validation, stop conditions, phase authority, or become unrelated documentation churn
- do not open a standalone docs-only canon lane, governance-only branch, or between-branch repair window for routine canon completion
- if PR Readiness misses required canon, branch-authority cleanup, or post-merge truth work, the next active branch must treat that miss as a `Branch Readiness` blocker and repair it before implementation begins
- if a stale-canon or governance-drift class is discovered, the same branch or next legal repair surface must patch the canon or validator rule that allowed it before the repair is considered complete
- escaped drift prevention proof is mandatory: every repair for a miss discovered after the phase that should have caught it must include source-truth, governance, validator, helper, or prompt-contract hardening that prevents the same class from passing again, or must record why the gap is not machine-checkable yet and what human review marker replaces it before green
- when post-merge truth will remain `No Active Branch`, merge-stable pointer surfaces such as backlog and roadmap must not mirror transient repair-branch ownership; that transient execution truth belongs only in external operational state, Git/GitHub/helper-derived truth, or the standing Governance intake exception until merge
- do not write directly to `main`; `main` is protected and any Codex file mutation there is a `Main Write Attempt`
- the normal governed branch lifecycle is:
  1. `Branch Readiness`
  2. `Workstream`
  3. `Hardening`
  4. `Live Validation`
  5. `PR Readiness`
  6. `Release Readiness`
- `Branch Readiness` must plan the whole branch at phase level before Workstream begins, including objective, target end-state, expected seam families and risk classes, validation contract, User Test Summary strategy, later-phase needs, and first seam or seam sequence
- Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
- Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
- during `Workstream`, `bounded multi-seam workflow` is the primary model inside the current slice; execute one active seam at a time, validate it, record evidence, report `continue` or `stop`, and keep going until all required seams in the current slice are complete and the slice status is green, then advance into the next admitted slice while `Completion Status` remains `In Progress`, unless a named blocker or waiver requirement turns `Completion Status` red
- a green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice
- bounded means one active seam at a time, not one-seam Workstream authority.
- a single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
- a task-level `Return:` block, rollback request, commit request, or next-seam recommendation is not stop authority while `Continue Decision` remains `Continue`
- when `Continue Decision` is `Continue`, do not end on a seam-complete final response; keep executing until a lawful `Stop` decision exists
- If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
- `Phase: Workstream` must remain bounded at all times; the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver
- Phase Boundary Stop Required: A phase-exit seam named in `Next Active Seam` is a handoff target, not current-phase execution authority.
- Bounded Workstream continuation ends at phase boundaries; it never crosses from Workstream into Hardening by inertia.
- Codex must not execute Hardening, Live Validation, PR Readiness, Release Readiness, release work, or any other next phase in the same run unless USER explicitly admits that phase after reviewing the handoff.
- if `Completion Status` is `Red`, `Continuation Action` must report the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume
- treat `Completion Status` as the exact `Phase: Workstream Status` gate for stop authority
- Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
- Docs-only Workstreams require explicit USER approval.
- Planning-loop bypass requires `Planning-Loop Bypass User Approval: APPROVED` and `Planning-Loop Bypass Reason:`.
- Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
- branch existence, branch rename, backlog promotion, repair-only traceability, or release-bearing posture do not count as Workstream progress by themselves
- when a prompt names an active seam, treat it as the entry seam, not a terminal boundary; a slice is a bounded admitted backlog-completion unit, while a seam is the current execution checkpoint inside or between slices
- seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress
- `bounded` describes scope and blast radius, not partiality by default; a bounded slice may still be the full currently implementable backlog-completion pass for that backlog item or branch lane
- there is no repo-wide cap on how many slices a branch or workstream may carry
- same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green.
- `Next-Seam Continuation Required` means continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green.
- when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
- `Workstream` reaches `Hardening` only when `Completion Status: Green`
- `Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; only then may `Workstream` hand off to `Hardening`
- `Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation
- `Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item.
- use `Backlog Completion State: In Progress`, `Implemented Complete`, or `Implemented Complete Except Future Dependency` to record whether more same-branch slices are still required
- stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition
- prompt language such as `bounded`, `bounded seam`, `single seam`, `one pass`, `small pass`, `narrow pass`, or `only this seam` is active-seam scope control only; it cannot narrow an admitted multi-slice Workstream into a single-seam Workstream unless explicit USER waiver is recorded
- reporting `Next Safe Move` is not a substitute for execution while the current slice still requires seams; A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice
- category labels such as bug fix, hotfix, high-risk, cross-subsystem, settings, protocol, launcher, or UI-model work require smaller seams and stronger gates; they are not automatic stop authority when the next seam remains admitted and green
- `Workstream` completion does not imply PR readiness; the normal next legal phase is `Hardening`, followed by `Live Validation` and then `PR Readiness`
- `Post-Release Canon Repair` is not a normal phase or branch; escaped canon repair must ride the next legitimate runtime-focused backlog branch's `Branch Readiness`, never direct `main` or a standalone repair branch
- before any next implementation branch may enter `Branch Readiness`, the repo-level admission gate from `Docs/phase_governance.md` must pass on updated `main`
- Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection. That choice is rooted in project vision, family vision, branch vision, current completed work, and the next implementation need. PR Readiness may recommend or validate selected-next context only when USER explicitly asks for PR-time successor selection or already-encoded selected-next truth would merge as durable source truth; PR Readiness does not require selected-next truth or a waiver by default.
- `PR Readiness Stage 1 - Analysis Gate` may include a no-work `## Next Branch Pre-Plan` gate only when USER asks PR Readiness for successor-selection analysis or selected-next truth already exists. Normal next-branch package-shape proof belongs to Branch Readiness Stage 1; `Next Branch Package Shape Unproven`, `Single-Slice Branch Drift Risk Unresolved`, and `Family Organization Drift Risk Unresolved` block Stage 1 continuation only for USER-approved PR-time selected-next truth or already-encoded selected-next truth that would merge as durable repo truth.
- `PR Readiness Stage 1 - Analysis Gate` must also audit the governance/source-of-truth ledger: identity model, FAM taxonomy, package/branch rule, USER approval blockers, Branch Readiness staging, PR Readiness staging, selected-next recommendations when in scope, real-carrier routing, branch authority lifecycle, watcher/automation proof, release readiness/execution separation, Element Coverage, ChatGPT loader/source-truth split, project direction, current workflow, after-release workflow, and absolute guardrails. If any ledger item requires branch/package admission, selected-next truth, runtime package admission, release execution, tag/release/artifact creation, source-truth restructuring, or a new real carrier that cannot be safely cleared as current-branch PR Stage 1 repair, Stage 1 must record `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required` according to legal carrier ownership.
- `PR Readiness Stage 1 - Analysis Gate` must decide the next governed path before PR creation: PR Stage 2 execution, release-support carrier, Branch Readiness carrier, another legal carrier, or explicit USER waiver/defer. Post-merge `No Active Branch` may be projected when no USER-approved selected-next truth exists. Release debt is not a normal acceptable state; if unavoidable, Stage 1 must record explicit USER approval, a named owner, release target/floor semantics, Release Window Audit posture, and the real carrier plan before Stage 2.
- `PR Readiness Stage 1 - Analysis Gate` must run `Origin/Main Freshness Check` before Stage 2. The packet records `Branch Creation Base:`, `Current origin/main:`, `Origin/Main Advanced Since Branch Creation:`, `Origin/Main Changed Files:`, `Branch Changed Files:`, `Reconciliation Required:`, `Reconciliation File List:`, `Reconciliation Recommendation:`, and `Reconciliation Mutation Status:`. If `origin/main` advanced since branch creation and reconciliation is needed, Stage 1 stops on `Origin Main Reconciliation Packet Required`, outputs the complete file/data list and recommendation, and performs no file fixes during Stage 1.
- if repo truth resolves to blocked `No Active Branch`, report the blocking repair path
- if repo truth resolves to steady-state `No Active Branch`, do not invent a next implementation branch by inertia
- governance-only branches are not used for new Nexus work; governance or canon repair rides on the active runtime-focused branch that owns the affected truth, or on the next legitimate runtime-focused backlog branch's `Branch Readiness` if a PR Readiness miss escaped the prior branch
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- If a release is blocked by missing post-merge closeout proof and the branch has not merged, route back to `PR Readiness`; if the branch has already merged, record the drift for the next legitimate runtime-focused branch's `Branch Readiness` and repair it in Stage 2 before implementation. Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
- the normal `Branch Readiness` sequence for a candidate branch is organized inside the same canonical phase:
  0. run `Branch Readiness Stage 1 - Analysis Gate` first. This is analysis-only: no repository file mutation, branch creation, package admission, docs sync, PR work, release work, or selected-next truth is allowed.
  1. Stage 1 outputs `## Branch Readiness Stage 1 Analysis Packet` with the FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, product vision, project-wide vision alignment, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable vs full-system boundary, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, rejected shallow plan, alternatives/tradeoffs, open USER decision points, deferred ideas/future-package ledger, validation plan, `Stale Branch Cleanup Plan:`, expected docs sync, `Branch Readiness Planning Incomplete` blocker review, `Next Legal Phase:` digest field, and explicit USER approval blocker.
  1a. Broad implementation branches must not enter Workstream, Hardening, Live Validation, or PR Readiness from a shallow/simple-system plan. Their `Product Definition Plan` must include non-empty, concrete `Project-Wide Vision Alignment:`, `Branch-Specific Vision Alignment:`, `System Concept Model:`, `Entity / Profile Model:`, `User Workflow Model:`, `Scale / Data Volume Model:`, `Configuration And State Model:`, `Expected User-Facing Outcomes:`, `Codex Additional Recommendations:`, `USER Critique Loop:`, `USER Decision Ledger:`, `Deferred Ideas / Future Package Ledger:`, `Planning Adequacy Review:`, `Rejected Shallow Plan:`, `Alternatives And Tradeoffs Reviewed:`, `Whole-System Interaction Map:`, `Minimum Viable vs Full System Boundary:`, and `Open Questions / USER Decision Points:` fields before implementation or any later execution phase. Self-assessed wording such as `simple`, `basic`, `minimal`, `see above`, or `not applicable` is not planning proof.
  1a. Runtime-focused branches must also carry `## Runtime Branch Engineering Contract` before Workstream begins or resumes. The contract must record `USER Engineering Planning Review:`, `Runtime Implementation Approval:`, `Current Runtime Baseline:`, `Planned Runtime Delta:`, `User-Facing Runtime Delta:`, `State / Config / Schema Delta:`, `Validator / Helper Delta:`, `Expected Changed Files / Surfaces:`, `Approval-Boundary Audit:`, `Future-Gated Items:`, `Workstream Seam Map:`, `Proof Expectations:`, `Risk Forecast:`, `Recommendations And Alternatives:`, `Plan Version / Revision Status:`, and `Plan-To-Implementation Traceability:` so Workstream, Hardening, Live Validation, PR Readiness, and Release Readiness can prove actual implementation against admitted engineering intent. New or re-entering runtime-focused branches must use an active Branch Runtime Engineering Plan under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`; Stage 1 proposes the plan, Stage 2 creates or admits it and links it through `Branch Runtime Engineering Plan Path:`, Workstream and Hardening update plan-to-implementation traceability, Live Validation records proof or waiver posture, and PR Readiness fold-down decides which durable summary becomes a structured branch receipt, repo branch-plan historical receipt, or promoted workstream/family-dossier truth.
  1a. `Carrier Lifecycle Decision` must classify the requested branch/worktree with `Carrier Lifecycle Classification:` as exactly `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, or `Active remote/open PR branch`, and must report `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Stale Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`.
  1b. When USER input is needed, the `USER Vision Question Packet` must explain each decision with question ID, category, decision needed, why it matters, affected feature area, Codex recommendation, rationale, alternatives, tradeoffs/risks, current-branch impact, future-package impact, safe default, whether the answer is required before implementation, waiver/defer posture, and exact response format requested from USER. Missing packets block on `USER Vision Question Packet Missing`; questions without recommendations/rationale/tradeoffs block on `USER Vision Recommendation Missing`.
  1c. When the USER needs to answer a broad family-package planning packet outside chat, Codex must generate or refresh a USER-facing `User Vision Input.txt` desktop artifact with answer paths for accepting Codex's recommendation, changing it, or deferring/future-packaging/waiving it with a reason. The artifact is not repo source truth; Codex recommendations and unanswered prompts are not USER-approved answers. Repo truth updates only after a later USER-approved digest pass reads the completed artifact and summarizes the answers into source truth. `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, and `USER Vision Input Pending` block Workstream entry or continuation until the file exists, answers are complete, and digest/revalidation are done or explicitly USER-waived.
  1d. Before runtime/user-facing/source-truth Workstream implementation begins or resumes, Codex must complete Branch Planning: BP1 `USER Branch Vision Review`, BP2 `USER Branch Plan Review`, and BP3 `Workstream Entry / Orchestration Validation`. BP1 summarizes the branch vision, end-state, product shape, user-facing behavior, surfaces, options, recommendations, and USER acceptance or waiver. BP2 summarizes the accepted Branch Vision, implementation package, branch scope size, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof path, Hardening plan, Live Validation / UTS plan, risks, future-gated boundaries, USER plan review, exact BP3 approval text, `Contract Status:`, `Packet Reviewability State:`, `USER Gate State:`, `USER Review Response:`, `Codex Response Digest:`, and `USER Review Packet Finding:`. BP3 proves the plan implements the accepted Branch Vision and can return first bounded implementation approval request only when BP1 and BP2 are Complete or Waived by USER and BP3 is approved or waived by USER. Missing review blocks on `BP1 Branch Vision Review Missing`, `BP2 Branch Plan Review Missing`, or `BP3 Orchestration Validation Missing`; stale packet metadata blocks on `USER Review Packet Stale`; an omitted packet digest or missing USER response/digest/waiver blocks on `USER Review Packet Not Digested`; treating packet validation as USER acceptance blocks on `Packet Validation Treated As USER Acceptance`.
  1d. When a completed USER input digest exposes package-specific blockers, Branch Readiness must keep implementation blocked until the current branch versus future package boundary is revalidated. Package-specific planning blockers may include legacy product-name drift, telemetry provider selection, polling floor, warning modality, external telemetry privacy model, cross-family audio approval, and persona/model switching scope.
  1e. A family-package plan is not complete while current-branch scope, future-package deferrals, provider path, polling posture, warning modality, naming/product-copy handling, privacy boundary, or acceptance criteria remain candidate-only. Stage 2 may finalize those boundaries, but Workstream resumes only after the next Stage 1 revalidates the finalized plan or records an explicit USER waiver.
  1f. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.
  2. Stage 1 stops on `Branch Readiness Execution User Approval Missing` until explicit USER approval to enter Stage 2 is recorded.
  3. after approval, run `Branch Readiness Stage 2 - Execution Gate` to perform approved branch/package admission work, docs sync, branch creation, and any stale/old branch cleanup that was planned after replacement branch/worktree validation only inside the USER-approved scope.
  3a. Branch cleanup requires `Branch Cleanup Execution Gate:` proof: `git worktree list`, current branch targets, intended replacement branch/worktree, and GitHub Desktop-bound worktree binding must show no repository is left without a valid branch target before deleting a branch or removing a worktree.
  3b. `Stable Worktree Path Preservation Gate:` applies when cleanup touches a GitHub Desktop-bound or family-stable folder path. Stage 2 must record `Stable Worktree Path:`, `Replacement Binding Path:`, and the preservation method before cleanup; removing the stable folder path before the successor branch/worktree is moved, switched, or rebound there blocks on `Stable Worktree Path At Risk`.
- Pre-PR Durability Rule: before `PR Readiness`, when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state
- the Pre-PR Durability Rule applies through `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; `PR Readiness` remains the later merge-target gate and must still prove clean durable branch truth
- prompt-level requests to stop before commit/push are not durability exceptions; only a documented `Durability Waiver`, failed validation, legally file-frozen `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push, and self-imposed blockers must automatically commit and push once lifted
- the normal `PR Readiness` sequence for a branch that changes release-facing canon is organized inside the same canonical phase:
  0. run `PR Readiness Stage 1 - Analysis Gate` first. This is an analysis-first blocker repair gate: Stage 1 analyzes repo truth, records `PR Readiness Stage 1 Repair Required` for bounded current-branch PR-readiness drift/blockers, validates and commits/pushes those repairs only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair, and remains blocked by `PR Readiness Stage 1 Repair Pending` until those repairs are durable.
     Stage 1 is the Stage 2 readiness-lock gate. It stays active until one explicit outcome is recorded: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`.
  1. Stage 1 outputs `## PR Readiness Stage 1 Analysis Packet` with governed state markers, the planned PR title/base/head/summary, required post-merge path, release-debt impact, release-debt handling status, completed merge-target canon updates when drift is repairable on the current branch, selected-next validation only when USER explicitly approved PR-time selection or selected-next truth already exists, planned watcher provisioning and reporting surface, planned validations, expected Stage 2 file changes, Stage 1 repairs made, Stage 1 repair validation, Governance Ledger fallback status, Branch Readiness fallback status, Stage 2 execution plan, drift findings, blocker and waiver findings, release-window audit posture, rollback path, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed from the USER.
  2. Stage 1 stops on `PR Readiness Execution User Approval Missing` until all Stage 1 repair blockers are clear, `Stage 1 Ready For Stage 2` is recorded, and explicit USER approval to enter Stage 2 is recorded.
  3. if Stage 1 records `PR Readiness Stage 1 Repair Required`, bounded current-branch repair/sync remains in Stage 1 and must be validated, committed, and pushed before Stage 1 can be declared ready.
  4. merge-target `No Active Branch` projection, merged-unreleased release-debt owner contracts, selected-next truth that already exists or is explicitly USER-approved for PR-time selection, and active-branch-authority cleanup are Stage 1 repair blockers when Stage 1 finds them; do not defer those source-truth repairs to Stage 2, Release Readiness, updated `main`, or a later branch. PR Readiness does not require selected-next truth or a waiver by default; if no selected-next truth exists, the next runtime implementation pipeline is selected in Branch Readiness Stage 1 after updated `main` and external operational state are revalidated.
  5. if Stage 1 records `Current-Branch Branch Readiness Re-entry Required`, the current branch is still the legal carrier but the fix is broader than PR-readiness sync and must re-enter Branch Readiness on the same branch.
  6. if Stage 1 records `New Carrier Branch Required`, the current branch is stale, merged, invalid, or cannot legally own the blocker, so a new real carrier branch is required.
  7. Branch Readiness fallback is real carrier branch/package analysis when PR Stage 1 cannot legally clear the blocker on the current branch; normal successor selection remains Branch Readiness Stage 1 work.
  8. after Stage 1 is ready and USER approval exists, run `PR Readiness Stage 2 - Execution Gate`; Stage 2 owns final PR execution only: verifying the durable Stage 1 projection, committing/pushing only bounded operator metadata if legally needed, PR creation, watcher provisioning, bot-review handling, mergeability validation, and merge-watch.
  9. validate current branch truth
  10. complete the merge-target canon updates on that same branch
  11. run the Governance Drift Audit
  12. record recurrence analysis for repeated or carried blocker classes before green
  13. clear the stale-canon blocker by proving current-state canon and merge-target canon reflect the branch's true state
  14. validate selected-next truth only when explicit USER approval for PR-time successor selection exists or repo/external state already encodes selected-next truth
  15. when selected-next truth is present, confirm it is recorded in backlog and roadmap as durable evidence only, has canon-valid record state and minimal scope, and has no branch created before Branch Readiness
  16. defer normal successor selection and successor branch creation to `Branch Readiness` after merge and updated-`main` / external operational state revalidation
  17. after explicit USER approval for PR-time successor selection exists, encode the machine-checkable selected-next markers: `Next Workstream: Selected` and runtime `Minimal Scope:` in backlog, plus selected-next roadmap evidence with truthful branch status; without approval, do not invent selected-next truth
  18. Post-merge `No Active Branch` is allowed when no USER-approved selected-next truth exists. If release handling is required, Stage 1 must route release handling to the real carrier before PR creation; otherwise the next implementation carrier is chosen in Branch Readiness Stage 1.
  19. commit all required docs, canon, validator, and branch-truth changes so the worktree is clean and truth is durable in commit history
  20. run the normal branch governance validator and the PR-readiness gate mode
  21. report `PR package ready`, create the PR, and validate the live PR state before reporting `PR READY: YES`
  22. only after the PR exists, has no conflicts, has no unresolved Codex comments/issues, matches merge-target canon, and clears any bot-review signal requirement for the live PR may the branch report `PR Readiness GREEN`
- PR creation details must use the operator copy-block contract from `Docs/phase_governance.md`: separate copy-ready blocks for `PR Title`, `Base Branch`, `Head Branch`, and `PR Summary`; the PR Summary/GitHub PR body uses exactly three top-level sections, `## Summary`, `## Branch Evidence`, and `## Validation`; `## Summary` must be concise, `## Branch Evidence` must not repeat the Summary through nested Summary/Purpose/Overview sections, concise branch-specific boundaries are allowed only when they clarify reliable branch truth, `## Validation` must stay proof-only, and phase-digest handoff fields such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, or `Stop Basis` remain banned from the PR body
- merge-target pointer surfaces must be merge-stable before PR green. `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, and the canonical workstream `## Phase Status` block may preserve durable branch/workstream evidence pointers or explicit USER waiver/defer receipts before PR creation, but must not own selected-next live posture, stale canon, cleanup-only branch state, or unresolved release debt as an acceptable post-merge default.
- Merge-target post-merge-stable authority projection is mandatory before PR green and is a PR Readiness Stage 1 repair responsibility when Stage 1 finds it. `Merge-Target Authority Projection Unproven` blocks Stage 2 and PR green when post-merge truth will be `No Active Branch` but the PR branch would merge an active branch authority record into `main`; the active authority record must be moved to historical/no-active posture or otherwise made merge-stable during Stage 1 before Stage 2 can execute, and historical branch records must not retain active PR Readiness phase, active seam ownership, live/open PR wording, merge-watch ownership, or `PR Merge Verification Pending`.
- do not pin merge-target branch heads in those current-state owner sections. Statements such as ``origin/main` is `<sha>``, ``origin/main` remains at `<sha>``, or equivalent branch-head hash assertions are time-sensitive operator facts, not merge-stable current-state truth.
- live PR state such as `open`, `non-draft`, `mergeable`, review-thread counts, repair-commit containment timing, or blocker-clearing branch narration belongs only in operator output and explicit historical PR sections such as `## Historical PR Package State`, `## PR Readiness Record`, `## Post-Merge Review Repair`, or `## Follow-Up PR Readiness Record`; do not place that live PR narration in merge-target current-state owner sections such as `Current Branch Execution Posture`, `PR Readiness State:`, `Current Branch Objective:`, `Active Workstream Chain:`, or the merged-unreleased `## Phase Status` block
- PR Readiness also owns `PR Readiness Scope Missed`, `Between-Branch Canon Repair Attempt`, `Next Branch Created Too Early`, and `PR Readiness Execution User Approval Missing`; none may be deferred into Release Readiness or a later side branch, and Stage 2 work may not begin until USER approval clears the Stage 1 stop
- PR Readiness Stage 1 also owns `PR Readiness Stage 1 Repair Pending`; any repairable PR-readiness drift or blocker found during Stage 1 must be fixed, validated, committed, and pushed on the active branch before Stage 2 can begin
- PR Readiness Stage 1 also owns the readiness-lock result; PR creation is blocked while any Stage 1 blocker, Stage 1 repair item, applicable selected-next validation item, applicable branch-shape review item, or Stage 2 sync prerequisite remains unresolved
- Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection; PR Readiness recommendations remain non-binding unless USER explicitly approves PR-time selected-next sync or selected-next truth already exists.
- PR Readiness Stage 1 also owns current-carrier/new-carrier fallback classification; if selected-next truth is in scope and cannot prove a broad family/package with concrete candidate work and multiple slices, and no USER approval clears the gate, PR Readiness Stage 1 must stop and record `Current-Branch Branch Readiness Re-entry Required` when the current branch can still own the repair or `New Carrier Branch Required` when it cannot
- the same fallback classification applies to the full governance/source-of-truth ledger: identity/FAM/package drift, USER approval blockers, real-carrier routing, branch-authority lifecycle, watcher proof, release execution boundaries, Element Coverage misuse, ChatGPT loader drift, project-direction drift, or current/after-release workflow drift must route to same-branch Branch Readiness re-entry or a new real carrier when the resolution is broader than current-branch PR Stage 1 repair
- PR Readiness still blocks accidental backlog mutation: do not add, split, package-admit, branch-create, promote, waive a single-slice package, or select a successor backlog identity without explicit USER approval. `Next Runtime Candidate Selection Pending` applies only to inconsistent already-encoded selected-next truth or explicit USER-approved PR-time successor selection; normal next runtime candidate selection belongs to Branch Readiness Stage 1.
- PR Readiness still preserves package/slice blockers: `Single-Slice Package User Approval Missing` and `Package Completion Unproven` remain current when package admission or same-branch package completion is unproven.
- PR Readiness also owns `Release Window Audit Incomplete`; if the branch is inside an unreleased release window, it must audit the current blocker set and clear it on the same branch by default instead of knowingly teeing up another blocker-clearing PR before release
- the normal green posture for that audit is `Remaining Known Release Blockers: None`, `Another Pre-Release Repair PR Required: NO`, and `Release Window Split Waiver: None`; only an explicit user-approved `Release Window Split Waiver` may allow a deliberate split
- PR Readiness also owns `PR Creation Pending`, `PR Validation Pending`, and `PR State Unknown`; `PR package ready` is not `PR Readiness GREEN`
- PR Readiness also owns `PR Merge Status Unproven`: until the live PR explicitly reports a green merge status, keep PR Readiness blocked; unknown, unset, conflicting, dirty, blocked, or otherwise non-green mergeability/merge-state results do not clear the gate
- PR Readiness also owns `Bot Review Signal Pending` for Codex-created PRs: watch the live PR until the Codex GitHub bot gives either a thumbs-up reaction or a bot comment; a thumbs-up reaction on the live PR clears the gate, while a bot comment keeps `PR Validation Pending` active until the branch fixes the comment on the same PR, pushes, replies to and resolves the review thread, and records that current-head comment-resolution closeout; no later thumbs-up is required. This is the same-PR Codex bot-review repair loop. Stage 2 final handoff cannot be green until bot-review closeout is verified.
- when a live Codex-created PR is waiting on `Bot Review Signal Pending`, PR Readiness Stage 2 must provision or update a PR watcher before handoff; a manual "check back later" instruction is not enough. The watcher contract must include bot reaction/comment/thread inspection and bounded same-PR repair authority for valid Codex bot comments: inspect the comment, repair only docs/governance/source-truth or other already-approved PR scope, rerun validation, commit and push to the same branch, reply/resolve only when the review thread contract requires it, and report back in the approved Codex surface. If no Codex bot comment or thumbs-up/approval signal appears after the current PR head has been live for at least two minutes, the watcher must post exactly one PR conversation nudge for that head SHA asking the Codex bot for the review signal, and must not repeat that nudge for the same head. If a bot comment asks for merge, release/tag/artifact work, runtime/provider/model/memory/shortcut/installer implementation, full AI Product Contract import, private Dev ORIN import, GitHub issue creation, unrelated cleanup, or another out-of-scope action, the watcher must report `BLOCKED` instead of repairing.
- PR Readiness and any earlier planning phase that intends to depend on watcher-based PR monitoring also own `PR Watcher Provisioning Unproven`: if the branch expects watcher-based PR monitoring, the watcher target, approved reporting surface, routing proof, runtime path, run-proof method, fallback, teardown rule, replacement provisioning for the next live PR, and the live bot-review action contract must be explicit and proven before the gate clears; accepted watcher proof may come from native Codex heartbeat run evidence or from a bounded local watcher that posts status-change updates through the official Codex thread-resume path into the approved Codex reporting-surface transcript. Manual rollout-file or transcript-file injection does not count as proof. Watcher configuration is not runtime proof. Stage 2 final handoff cannot be green until watcher runtime proof is present or the runtime-proof blocker remains active.
- PR Readiness also owns `PR Watcher Routing Unverified`: even after watcher provisioning exists and run proof is present, keep the gate blocked until the approved reporting surface is explicitly recorded and a validation pass confirms the configured thread/host target, state-file target, transcript target, and delivery proof all point to that recorded surface and at least one watcher emission has landed there
- Standard PR-watcher operating procedure from now on: every PR-bearing branch provisions a watcher for the current live PR on an approved Codex reporting surface, at minute cadence, and it reports only when a watched PR status changes. The current working thread is the default surface, but an explicitly recorded dedicated watcher-host thread is allowed when that is the validated user-visible route. Its action contract must also be explicit: thumbs-up reaction means report green for PR-entry validation; one or more actionable bot comments means trigger the bounded same-branch PR comment-repair worker, fix the issue, commit, push, reply, resolve the corresponding review thread, and then report `Comment addressed` / green for the current head. If that repair worker cannot complete safely, keep `PR Validation Pending` active and report the exact blocking comment.
- PR-watcher status-change output must be source-of-truth shaped, not a loose chat line: include governed state markers, live PR truth, watcher proof, blocker state, continue/stop decision, and, after `merged=true`, a copy/paste Codex prompt basis for the next legal Release Readiness validation. The watcher must still avoid claiming Release Readiness legality by itself; it may only hand off the source-of-truth validation prompt.
- PR-watcher delivery proof requires assistant-message transcript presence plus Codex thread-state refresh plus automation run/inbox visibility for the same approved reporting surface; if final merge delivery proof is missing, the watcher must keep running and retry instead of retiring.
- Standard PR-watcher continuation rule from now on: after PR creation and live PR validation, PR Readiness continues into a merge-watch seam that stays active until the watcher on the approved reporting surface verifies the PR actually merged
- PR Readiness also owns `PR Merge Verification Pending`: even after bot approval and green merge status, do not advance to `Release Readiness` until the watcher on the approved reporting surface has verified that the live PR is merged
- PR Readiness also owns `Automation Runtime Unproven`: phase-critical automation cannot clear a gate merely because its card, config, or automation list says `ACTIVE`; `ACTIVE` is configuration state, not run proof. Accept run evidence only from thread or inbox output, automation memory/log/state-file updates, or scheduler last-run evidence. If the preferred Codex automation remains `ACTIVE` without run evidence, keep the owning phase blocked until run evidence exists or a bounded fallback is activated. Any bounded fallback must be target-scoped, phase-scoped, read-only, and self-terminating or explicitly deleted when its terminal condition or phase exit occurs.
- Automation Observability Review Pending is a governed source-of-truth review loop: standing automations may report into Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`, but repo canon changes only when `dev/automation_observability_report.py` or a live automation report classifies a finding as `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED` and a bounded repair seam admits it. Informational green or waiting reports stay `REVIEW_INFO` unless they contradict repo truth. `Automation CWD Worktree Mismatch` blocks lane-sensitive automation output when the configured cwd is missing, stale neutral main, parked, or the wrong assigned worktree.
- PR Readiness also owns the merged-unreleased release-debt owner contract when a branch will merge unreleased implementation work; the merge-target canon must already contain the durable release target/floor/scope/artifact posture required by release governance, but it must not require `Selected Next Workstream:` or `Next-Branch Creation Gate:` unless USER explicitly approved PR-time successor selection or selected-next truth already exists.
- Merged-unreleased release-debt contract labels remain `Merged-Unreleased Release-Debt Owner:`, `Repo State: No Active Branch`, `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, and `Post-Release Truth:` when release-bearing unreleased work needs durable public release posture.
- PR Readiness must validate release target semantics from the latest public prerelease and declared `Release Floor:` before green; marker presence is insufficient if the version is wrong
- the normal `Release Readiness` sequence for a release-bearing branch must clear `Release Target Undefined` before reporting green:
  1. confirm whether the branch is release-bearing or explicitly non-release
  2. for release-bearing branches, require machine-checkable `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:` markers before Release Readiness can report green
  3. for non-release branches, require `Release Branch: No`
  4. allow `Release Branch: No` only for preserved historical records
  5. never use the non-release waiver for `implementation` or `release packaging` branches
  6. never let the waiver clear `Release Debt`, weaken post-merge truth, weaken validation, or permit premature next-workstream branch creation
- Release Readiness is not a docs-sync phase and not a file-mutation phase; it is analysis-only for repository files and is restricted to release-target validation, release-scope validation, release-artifact validation, GitHub release package information, final release-execution authorization or confirmation, and release-state confirmation after release execution
- Release Readiness may record `Branch Cleanup Plan:` for stale/old branches, retired worktrees, or stale GitHub Desktop entries, but `Branch Cleanup Execution Gate:` keeps deletion, worktree removal, branch switching, and GitHub Desktop-bound worktree cleanup blocked until the next `Branch Readiness Stage 2 - Execution Gate` creates or validates the replacement branch/worktree target. If the cleanup involves a family-stable Desktop path, the `Stable Worktree Path Preservation Gate:` must record `Stable Worktree Path:`, `Replacement Binding Path:`, and stop on `Stable Worktree Path At Risk` unless the stable path is preserved or explicitly rebound before removal.
- Release package details must use the operator copy-block contract from `Docs/phase_governance.md`: separate copy-ready blocks for `Release Title`, `Release Tag`, `Target Commit`, and `Release Notes`; release notes are detailed, user-facing, inclusion-only, Markdown-friendly, must not start with or repeat the release title as `# <release title>`, and must be combined with GitHub-generated `## What's Changed` plus the generated `**Full Changelog**:` compare link to the previous release during Release Execution
- Release Readiness must not edit, stage, commit, generate, or refresh source, docs, canon, validator, helper, release-note, or handoff files; if such work is discovered before merge, return to `PR Readiness`, and if discovered after merge, defer it to the next real runtime package carrier's `Branch Readiness`
- tracked file changes while the authority record says `Release Readiness` are blocked as `Release Readiness File Mutation Attempt`
- release execution and post-release canon closure are separate; a local-only post-release closure commit is a blocker, not completed source truth
- protected-main branch rejection must route to the next approved Branch Readiness Stage 2 canon/governance repair carrier rather than direct-main mutation, standalone cleanup, or a default release-support branch
- post-release validation must compare published GitHub release/tag truth and release-body format against remote repo source truth before runtime Branch Readiness can resume
- runtime implementation remains blocked until release publication exists, post-release canon drift is explicitly recorded or repaired through the approved Branch Readiness carrier, and owning validation reports green
- a post-release canon repair must not mutate `main`; if merged canon is stale, record the drift as a blocker for the next legitimate runtime-focused backlog branch's `Branch Readiness Stage 1` and repair it during Stage 2 before implementation begins
- returned `UTS`, screenshot, interactive, PR-review, or release-review evidence must be digested into the authority record before phase advancement is recommended
- User Test Summary is exclusive to Live Validation Stage 1.
- Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.
- while a required User Test Summary handoff is outstanding in `Live Validation`, the active branch must report `User Test Summary Results Pending`; automated validators and live helper evidence may be green, but Live Validation Stage 1 cannot enter Stage 2 until the filled User Test Summary is submitted or waived, digested into the authority record, and blockers are reevaluated
- PR Readiness may verify the previously digested Live Validation User Test Summary state, but it must not create, refresh, or digest UTS as its own phase artifact.
- Live Validation green requires an exact `## User Test Summary` state before final green.
- Every Live Validation digest must include an exact `## User Test Summary` section; if User Test Summary is waived, the digest must still include `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`.
- required pending-UTS wording is: `Automated validators and live helper evidence: GREEN.`, `User Test Summary Results: PENDING.`, and `Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.`
- Workstream may keep User Test Summary strategy and Live Validation readiness current, but it must not create or refresh the formal desktop `User Test Summary.txt`, digest User Test Summary results, or use `User Test Summary Results Pending` as the Workstream completion blocker or stop condition.
- when a slice changes user-visible behavior or another operator-facing path, do not treat `## User Test Summary` as a recap slot; route through `Docs/user_test_summary_guidance.md` and require a real manual checklist unless no meaningful manual test exists
- `## User Test Summary Strategy` is planning context only; the canonical repo-level `UTS` artifact must be the exact `## User Test Summary` section when one is required or waived
- when `User Test Summary Results: WAIVED` is used, the exact `## User Test Summary` section must also include `User Test Summary Waiver Reason:`
- when an active desktop workstream has a canonical repo-level `UTS` artifact, do not stop at response text; update that workstream-owned artifact as well unless an explicit exception from `Docs/user_test_summary_guidance.md` applies
- during bounded multi-seam Workstream execution, update the canonical User Test Summary strategy incrementally as user-visible seams land; refresh the formal desktop User Test Summary export only during Live Validation Stage 1 after the user-facing shortcut or equivalent entrypoint gate is ready
- for relevant desktop user-facing Live Validation Stage 1 runs, export or refresh `C:\Nexus USER\User Test Summary.txt` unless an explicit exception from `Docs/user_test_summary_guidance.md` applies; Desktop / OneDrive copies are mirror-only unless USER grants a later exception
- do not confuse the canonical workstream-owned repo artifact with the required desktop convenience export or with response-level handoff text
- when a user-visible implementation slice is already validator-green, do not assume that alone is enough to continue; route through `Docs/development_rules.md` and require an explicit hardening or continuation judgment
- when a relevant desktop or runtime path can be launched and exercised through a real desktop session, do not treat validators, simulation, or synthetic/headless harnesses as sufficient for continuation on their own; require the smallest reliable validation infrastructure plus an evidence-backed interactive OS-level result before continuation
- when Live Validation concerns a relevant desktop user-facing workstream, route through `Docs/phase_governance.md` and require the `User-Facing Shortcut Live Validation Gate`; this is the canonical `desktop-shortcut` blocker path: the active authority record must declare `User-Facing Shortcut Path:` and `User-Facing Shortcut Validation:` before User Test Summary handoff, and final green is blocked by `User-Facing Shortcut Validation Pending` until the declared user-facing desktop shortcut or equivalent entrypoint is passable or explicitly waived with `User-Facing Shortcut Waiver Reason:`
- when Live Validation concerns desktop UI and the user-facing launcher is feasible, the declared desktop shortcut / launcher path is the primary LV1 execution path; sandbox/offscreen/direct-runtime/WebView/helper-only evidence is supporting proof only and cannot be described as the USER-facing UTS path or used to clear LV1 by itself
- when Live Validation concerns a relevant desktop user-facing workstream, also require the `Codex Live Client Self-QA Gate`: the active authority record must declare `Codex Live Client Self-QA:`, `Visual Quality:`, `Live Interaction Evidence:`, `Usability Check:`, and `Platform Uniformity Check:` before User Test Summary handoff, and final green is blocked by `Codex Live Client Self-QA Pending` until Codex has inspected and exercised the live client like a user or an explicit waiver is recorded
- when Live Validation concerns desktop UI, also require `Codex Visual Adjudication:` with `Visual Artifact Review Scope:`, `Product Vision Alignment:`, `Per-Element Visual Verdicts:`, `Helper Marker Limitation:`, `Unacceptable UI Findings:`, and `LV1 Handoff Disposition:` before User Test Summary handoff; helper PASS, marker PASS, screenshot existence, and manifest existence cannot clear visual acceptability by themselves
- interactive user-facing Live Validation cannot clear Codex self-QA with screenshot-only, marker-only, or launched-but-not-driven proof; Codex must exercise the same live-client interactions it would ask the USER to test and record an interaction manifest or equivalent evidence
- desktop UI Live Validation must include an active foreground/user-observable client path; hidden, too-fast, or blink-through helper runs may support automation proof but cannot be the only Codex self-QA evidence
- desktop UI Live Validation must capture full virtual-desktop screenshots by default when placement, multi-monitor behavior, window separation, clipping, or frame-of-reference matters; those raw PNGs must be copied into `C:\Users\anden\OneDrive\Pictures\Screenshots\<project-or-validation-lane>\<timestamp>\` or the active USER-declared screenshots folder and surfaced in the Codex chat/handoff for USER inspection
- desktop UI Live Validation must also capture detailed focused screenshots per acceptance-critical element/state, copy them into `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\<validation-lane>\<timestamp>\focused_element_screenshots\`, name each file with the element label/name and state/action, and enumerate those real image paths in the manifest; full-desktop screenshots are context only and cannot satisfy this per-element requirement
- if the real interactive desktop path is not feasible, require an explicit explanation of why, require the strongest available synthetic/headless evidence instead, and treat the continuation judgment as limited by that missing interactive layer
- keep validator results, synthetic/headless validation results, interactive OS-level execution results, simulated reasoning, and manual handoff as separate evidence layers rather than collapsing them into one summary
- when a pass opens programs, windows, dialogs, temporary documents, helper processes, probe files, or other session-scoped artifacts, route through `Docs/development_rules.md` and require cleanup plus explicit cleanup verification before handoff unless there is an explicit reason to preserve them
- when a task depends on interactive desktop validation, route through `Docs/development_rules.md` and require explicit time budgets, clean timeout abort behavior, cleanup, and last-progress reporting rather than relying on open-ended waits
- when a task depends on Live Validation or another interactive desktop helper, route through `Docs/phase_governance.md` and require reuse-first selection from existing helpers before creating new scripts; temporary one-off probes must stay ignored, temporary, and non-closeout-grade unless promoted into documented reusable tooling
- when a task creates or keeps a durable root `dev/` validation helper, live-validation script, audit helper, harness, or shared helper, route through `Docs/validation_helper_registry.md` and require the standardized helper name, `Helper Status:`, owner, reuse decision, `Workstream-scoped` classification when applicable, `Consolidation Target`, and `Temporary probe` deletion or promotion handling
- when a live validation helper has no tighter watchdog, require a `10s` maximum no-progress supervisor with visible progress, clean abort, cleanup, and last confirmed progress reporting
- when closeout depends on interactive desktop validation, also route through `Docs/phase_governance.md` and require the helper's documented default budget profile to prove green before calling the branch truly green
- when a branch materially changes user-facing desktop UI, require the post-green live launched-process UI audit before treating closeout as complete; do not reinterpret that as a screenshot requirement for every seam iteration
- when the user also wants those audit screenshots to render inside the Codex client, use the screenshot-delivery guidance in `Docs/codex_user_guide.md`, which now defaults to small inline PNG preview images backed by preserved original files on disk, rather than assuming local-file image embeds will work

## Practical Prompt Rule

If you are unsure what to include in a future Nexus Desktop AI prompt:

1. start with `Docs/nexus_startup_contract.md`
2. treat it as a loader map, not execution authority
3. add `Docs/Main.md`
4. add `Docs/development_rules.md`
5. add `Docs/phase_governance.md`
6. add `Docs/codex_modes.md`
7. add the directly relevant authority docs for the active question
8. add live repo evidence only where the truth could have changed or drifted

Only after that full scan should scope be narrowed for execution.
