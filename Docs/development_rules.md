# Nexus Development Rules

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**
**Release Readiness anchor and aggregation rules are owned by `Docs/phase_governance.md`. This file mirrors only the execution reminder: Release Readiness is file-frozen and must derive release-window truth from Git/GitHub/helpers instead of maintaining duplicate live state.**

## Core Principles

- Analyze first
- Validate live repo truth before making lane, branch, merge, or release recommendations
- One coherent approved change per revision
- Preserve architecture boundaries
- Logs, code, and merged docs are the source of truth for implemented behavior
- No silent scope expansion
- No silent backlog or policy drift
- Bounded State is mandatory before execution, and broad work language cannot widen scope without explicit USER waiver

## Analysis-First Operating Posture

Codex is a full-scan analyst before it becomes an executor.

That means Codex must:

- scan broadly enough to understand the whole affected system
- validate current repo truth
- surface drift, risk, dependencies, and options
- only narrow scope after the analysis is complete and the user approves execution boundaries

Execution language such as:

- `minimal`
- `smallest safe slice`
- `narrow`
- `single patch`

belongs to execution planning after analysis, not to the initial investigative posture.

Short prompts, shorthand cues, or mode-only requests do not waive source-of-truth reading.

## Mandatory Bounded Execution State

Before Codex mutates files, creates or switches branches/worktrees, commits, pushes, creates a PR, handles PR comments, performs release actions, launches runtime validation, mutates shortcuts, installs providers/models, or changes GitHub Desktop handoff state, it must prove a `Bounded State:`.

That bounded state must name the exact phase/stage, workspace, git root, branch, upstream, `HEAD`, `origin/main`, worktree role, write target, owning authority record, active package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase.

If Codex cannot prove that bounded state, it must stop on `Bounded State Missing` before mutation and report the exact missing field or USER decision needed.

Broad work requests do not authorize implementation. `Continue`, `complete all`, `all remaining work`, `finish the branch`, or similar wording may be used only when repo source truth resolves it to one exact active bounded seam. If it does not, Codex must stop on `Bounded State Missing` or `Next Bounded Workstream Seam Approval Missing`.

Widening beyond the current bounded state requires `Bounded State User Waiver: Granted` in the owning source truth or current USER approval. The waiver must name the branch/worktree, phase, slice/seam, relaxed bound, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions. Without that explicit waiver, stop on `Bounded State Waiver Missing`.

Clean validation, clean git state, branch existence, prior broad approval, prompt wording, Codex discretion, or ChatGPT review cannot infer a bounded-state waiver.

## Live-State Validation Gate

Before recommending the next move after a merge, release, or major lane transition, validate:

- current branch
- local `main` versus `origin/main`
- whether referenced PRs are actually merged
- whether referenced branches still exist
- latest public tag or release versus current `main`
- whether docs and canon reflect live repo truth

If prompt framing is stale, report the real state first and plan from that state.
If repo truth resolves to blocked `No Active Branch`, report the blocking repair path instead of inventing a later phase.
If repo truth resolves to steady-state `No Active Branch`, say so explicitly and do not invent a next implementation branch by inertia.

## Prompt-Entry Origin/Main Freshness Gate

Before every new or resumed repo-affecting Codex pass, and before planning, patching, phase work, validation-green claims, PR/merge/release work, runtime work, or branch/worktree mutation, run the `Prompt-Entry Origin/Main Freshness Gate` from `Docs/phase_governance.md`. The packet must include `Prompt-Entry Freshness Check:`, `Fetched origin/main:`, `Current Worktree:`, `Current Branch:`, `HEAD:`, `origin/main:`, `Merge Base With origin/main:`, `Origin/Main Advanced Since Last Action:`, `Pre-Rebaseline Impact Audit Required:`, and `Rebaseline/Reconciliation Status:`. If `origin/main` advanced or cannot be proven current, stop on `Prompt-Entry Origin/Main Freshness Missing` or `Origin/Main Advanced Rebaseline Required` before mutation or phase continuation; validating locally is not enough.

## Pre-Rebaseline Impact Audit

`Pre-Rebaseline Impact Audit` is required before any worktree, branch, neutral-main workspace, or standing governance lane baselines itself to a newer `origin/main` through fast-forward, merge, rebase, conflict resolution, branch switch, or current-main reconciliation.

No Baseline By Inertia: Codex must not run the baseline operation merely because the worktree is clean, behind, or expected to fast-forward. First report `Incoming Main Change Set:`, `Incoming Changed Files:`, `Current Worktree Changed Files:`, `Branch Changed Files:`, `Rebaseline Overlap Files:`, `Incoming Runtime / Source-Truth Risk:`, shared-surface/worktree overlap, `Validation Before Rebaseline:`, `Recommendation Only:`, `Rebaseline Mutation Approval:`, and `Rebaseline Mutation Status:`. The audit is report-only until USER approves the exact worktree, branch, target commit, and operation type.

If the incoming change set touches runtime/provider/UI/source-truth/validator files, if the current worktree is dirty, if validation fails, if sibling worktree overlap exists, or if `Rebaseline Overlap Files:` is not `None`, the correct next move is a reconciliation recommendation and USER decision, not automatic mutation. `Rebaseline Overlap Files:` means incoming changed files intersected with current branch/worktree changed files. Any non-empty intersection triggers `Rebaseline Overlap Intent Gate`: freeze mutation, inspect the active branch plan's `Branch Change Intent Ledger`, classify each overlapping file through the `Rebaseline Overlap Failure Procedure`, and stop on `Rebaseline Overlap Intent Missing` when branch-owned intent evidence is missing, weak, stale, conflicting, or USER-dependent. After an approved baseline, run `Current-Main Reconciliation Identity Guard` before claiming the lane is safe.

## Multi-Worktree Automation Contract

Standing automation is not lane truth by itself. `Automation Observability` must treat Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md` as evidence inputs until `dev/automation_observability_report.py` classifies a finding as `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED`.

Every active automation that can affect branch, PR, Release Readiness, post-merge, release-window, selected-next, toolchain, or branch governance truth must carry a configured cwd that resolves to a known worktree. The report must prove cwd, git root, worktree role, branch, `HEAD`, `origin/main`, and stale-neutral-main posture. `Automation CWD Worktree Mismatch` blocks the finding when the automation is pointed at stale `C:\Nexus Desktop AI`, a missing folder, a parked worktree, the wrong FAM lane, or a Governance worktree that is not the recorded lane. USER-approved `automation/worktree governance intake` may use the `Standing Governance Intake Branch` only for non-runtime multi-worktree automation safety repair, and USER-approved `phase-gate governance intake` may use it only for repeatable non-runtime phase-gate miss prevention; both must preserve `RRI-YYYYMMDD-NNN`, operational `One Active Cycle`, `Sync Rule`, `Waiting For Governance Intake`, `Return Digest`, and `Neutral Main Workspace Rebaseline`. The standing Governance branch must not require a dedicated post-merge closeout PR solely to clear cycle-ledger wording after merge/sync/return digest.

## Governance Intake Triage And Digest Profiles

Broad governance/source-truth/process reform must use `Docs/governance_intake_triage_and_digest_profiles.md`. Before mutation, return a `Governance Intake Triage Packet` unless the approved intake already names exact blockers, carrier, files, and approval boundaries. During output, use the smallest legal `Digest Profile`: `Decision Packet`, `Return Digest`, `Validation Digest`, `Full Audit Packet`, or `Delta Digest`. The `Digest Non-Compaction Rule` applies to every digest: do not compact the digest ever, and do not omit required fields or USER-requested review detail.
Formal Next Legal Phase Digest cannot be compacted into vague next-step wording. When a phase packet stops for USER approval, include `Current Phase:`, `Next Legal Phase:`, `Why This Phase Is Next:`, `Approval Required:`, `Exact USER Approval Text:`, `Allowed Scope:`, `Explicit Exclusions:`, `Validation Required:`, `Stop Conditions:`, `USER Plan Review Gate:`, `USER Inspection Files:`, `Review Required Because:`, `Implementation Blocker:`, and `Review Waiver Reason:`. `USER Plan Review Gate:` must say whether USER may accept, revise, waive, or reject the plan, and `Implementation Blocker:` must name the blocker when implementation remains unauthorized.

## Governance Efficiency Operating Model

Broad governance reform must also use `Docs/governance_efficiency_operating_model.md` before adding another live-state surface, policy mirror, helper family, release ownership rule, alias, or public-output rule. New durable governance rules should name a `Rule ID`, one `Owner File`, compact mirrors, validator/helper owner, and `Do Not Duplicate In:` boundary.

## Source-Of-Truth Ownership Model

Use this layered ownership model:

- backlog = identity and registry
- workstream docs = promoted-work feature-state, branch-local evidence, active seam references, artifact history, branch-local reuse notes, and closure history
- roadmap = stage-breakpoint schedule outline and broad milestone checkpoints, not a release ledger
- rebaselines and closeouts = epoch or milestone summaries
- incident patterns = generalized reusable lessons
- bugs = backlog-first, with promoted bug docs only when warranted
- User Test Summary = validation-contract layer owned by workstreams
- phase governance = repo-wide execution, exact phase enum, blockers, branch classes, proof, timeout, seam, stop-loss, validation-helper, Governance Drift Audit, phase resolver, and desktop UI audit contract
- validation helper registry = repo-wide helper naming, helper ownership, reuse-first inventory, workstream-scoped exception markers, and consolidation contract
- branch authority records = repo-owned phase owners for selected `Registry-only` backlog branches in `Branch Readiness`, approved `release packaging` branches, active runtime-focused branches that must carry bounded governance/source-of-truth repairs before PR green, and preserved historical repair records; standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work
- Element Validation Ledger = row-level created/touched/affected/deferred/future element proof tracking owned by the existing workstream doc or branch authority record; use a companion file only when that owning record points to it canonically
- `Docs/nexus_startup_contract.md` = ChatGPT/new-chat loader map and prompt-generation guardrail owner, including the Nexus Prompt Gate final scrub rule when prompt generation, bootstrap continuity, or loader/source-truth drift review is in scope
- `Docs/Main.md` = routing authority aligned to merged truth
- active branch names must not use the `codex/` prefix; use `feature/` or another USER-approved non-`codex/` prefix, and treat historical `codex/` branch names as traceability only

Use `Docs/phase_governance.md` for:

- named execution phases
- blocker rules and branch classes
- phase entry and exit rules
- rollback and next-legal-phase rules
- proof authority rules
- interactive timeout governance
- validation helper rules
- desktop UI audit rules
- truth-drift enforcement
- governed closeout stop-loss rules

Use these lifecycle fields:

- `Status` = delivery or work state
- `Record State` = canonical-record lifecycle

Allowed `Record State` values are:

- `Registry-only`
- `Promoted`
- `Closed`

Rules:

- if `Record State` is not `Registry-only`, `Canonical Workstream Doc` must exist
- closed workstream docs stay at stable paths
- backlog and roadmap must not continue carrying the full execution story once a canonical workstream doc exists
- workstream docs must not silently redefine repo-wide phase or proof-governance rules that belong to `Docs/phase_governance.md`
- before adding a new governance/source-truth file, active artifact, ledger, registry, or durable authority surface, run the `Source-Truth Placement Preflight` from `Docs/phase_governance.md` and extend the existing owner first unless `No Existing Owner Fits` is recorded
- the active Element Validation Ledger belongs inside the canonical workstream doc for `Promoted` work or inside the branch authority record for `Registry-only` active branches; backlog, roadmap, family dossiers, validation helper registry, and Element Coverage must not become active ledger owners by inertia
- USER-facing interface elements, including previous implementations and future implementations, must record a Dev Toolkit Interface Review Mode disposition in the owning Element Validation Ledger: callable in dev-only review mode, deferred to a named repo-wide adoption branch/package, or not-applicable with reason. The review mode should expose element badges, hover highlighting, ledger ID/name tooltips, and screenshot-friendly annotations only in Dev Toolkit/dev mode; production UI must not expose element numbers.

Record-state meaning:

- `Registry-only` = backlog identity exists, but no canonical workstream execution record is required yet
- `Promoted` = a canonical workstream doc is required and becomes the durable branch record that must stay current throughout the active lane
- `Closed` = the canonical workstream doc remains historical lane truth and must not be treated as active execution authority by inertia

## Required Startup Loading

Before planning, patching, reviewing, or recommending the next move, Codex must load the canonical source-of-truth set.

`Docs/nexus_startup_contract.md` may be used as a compact ChatGPT/new-chat loader map, but it is not Codex execution authority.
Execution behavior is governed by this document, `Docs/Main.md`, `Docs/phase_governance.md`, `Docs/codex_modes.md`, the active workstream or branch authority record, and directly relevant owning canon.
Prompt text and loader templates may describe requested task scope, but they must not override source-of-truth, restrict required continuation, define seam behavior, bypass phase rules, change durability requirements, or weaken validation.
Local ChatGPT custom instructions should stay compact while the repo loader/source-truth may preserve longer ChatGPT-facing continuity rules and review memory.
Do not paste the loader doc into Codex prompts; Codex prompts should load `Docs/Main.md` and the owning canon for execution authority.
Main is the first repo loader and routing index. After loading Main, follow its owner chain to phase governance, execution posture docs, Nexus Vision, family vision, active branch plan, branch record, workstream record, helper registry, and any other directly relevant owner instead of inferring from prompt text or context docs alone.
Loader/source-truth continuity must preserve the broad FAM -> Package -> Slice -> Seam model, PR evidence-only handling, legacy global FB historical-only handling, single-slice/package-completion blockers, Element Coverage as non-identity, Branch/PR Readiness Stage 1 / Stage 2, next-branch hierarchy review, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and the Windows-first, modular, GPU-aware direction with optional heavy local AI capability packs and CPU fallback.

PR Readiness Stage 1 is the Stage 2 readiness-lock gate. It must analyze release-debt impact, release-debt handling status, required current-branch source-truth sync, Stage 2 sync needs, PR title/base/head/summary, watcher plan, blockers, and USER decisions before Stage 2 can begin. Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection, rooted in Nexus Vision, family vision, branch vision, current completed work, and the next implementation need. PR Readiness does not require selected-next truth or a waiver by default; it validates selected-next truth only when USER explicitly approves PR-time selected-next sync or selected-next truth already exists and would merge as durable repo truth. Stage 1 remains active until one outcome is recorded: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`. Bounded Stage 1 repair/sync may mutate durable source truth only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair. Stage 2 begins only after `Stage 1 Ready For Stage 2` plus explicit USER approval, and Stage 2 owns final PR execution only: final PR package sync, commit/push if needed, PR creation, watcher provisioning, bot-review handling, mergeability validation, and merge-watch.

PR Readiness Stage 1 must also run an `Origin/Main Freshness Check` before Stage 2. It records `Branch Creation Base:`, `Current origin/main:`, `Origin/Main Advanced Since Branch Creation:`, `Origin/Main Changed Files:`, `Branch Changed Files:`, `Reconciliation Required:`, `Reconciliation File List:`, `Reconciliation Recommendation:`, and `Reconciliation Mutation Status:`. If `origin/main` advanced and branch/current-main files or source-truth owners need review, Stage 1 stops on `Origin Main Reconciliation Packet Required`, outputs the complete reconciliation data and recommendation, and performs no file fixes during Stage 1.

Before a merge, rebase, fast-forward, or branch switch performs the reconciliation, Codex must also run `Pre-Rebaseline Impact Audit`. That audit is the mutation-level gate and must record `Incoming Main Change Set:`, `Incoming Changed Files:`, `Current Worktree Changed Files:`, `Branch Changed Files:`, `Rebaseline Overlap Files:`, `Incoming Runtime / Source-Truth Risk:`, `Validation Before Rebaseline:`, `Recommendation Only:`, `Rebaseline Mutation Approval:`, and `Rebaseline Mutation Status:` before any local branch state changes. Non-empty `Rebaseline Overlap Files:` invokes `Rebaseline Overlap Intent Gate`; mutation remains blocked until `Overall Overlap Gate Result:` is not blocked and the USER approves the exact operation.

Current-main reconciliation in a multi-worktree branch must also pass the `Current-Main Reconciliation Identity Guard`. origin/main is context, not identity: after any merge, rebase, fast-forward, or conflict resolution, the assigned worktree must reassert `Assigned Worktree Branch Identity:`, `Branch-Local Authority Reassertion:`, `Incoming Main Active-Branch Blocks Accepted: NO`, and `Sibling Worktree Identity Preservation:` before validation or commit. Do not accept incoming current-workstream, selected-next, or active-branch blocks wholesale when they belong to another worktree; preserve them as merged-main context, then make `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, and the active branch record point back to the assigned branch and authority record. If this is not true, stop on `Worktree Branch Identity Drift`.

PR Readiness must prove post-merge source truth before PR creation or merge readiness through the `Release Readiness Health Pass`. Run `python dev\orin_branch_governance_validation.py --release-readiness-health-gate` during Stage 1, after any Stage 2 or bot-review source-truth repair, and before merge approval. The pass requires the authority record to carry `Post-Merge Branch Authority Projection:`, `Stale Active Branch Wording Scan:`, `Stale PR Creation / PR Readiness Pending Wording Scan:`, `Merged-Unreleased Scope Posture:`, `Release Execution Gate:`, `Watcher / Live PR State Projection:`, `Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `FAM Overlap Routing:`, `Release Candidate Anchor Projection:`, `Release Window Contributor Inventory:`, `Governance Intake Routing:`, and `Projected Post-Merge Validation:` so Release Readiness validates instead of repairing stale merged-main truth. A separate post-merge projection receipt does not clear the pass while the same branch remains listed under `Active Branch Authority Records`; that shape blocks on `Merge-Stable Projection Shadowed By Active Authority`. PR Readiness Stage 1 must also execute the actual branch-authority fold-down when the health pass or `Post-Merge State` projects `historical/no-active`, `must not remain active branch authority`, or `historical merged-unreleased` posture; projection-only text while the actual record remains active blocks on `PR Readiness Stage 1 branch-authority fold-down required` before Stage 2, PR green, or merge approval. If Release Readiness still discovers stale active branch authority, stale phase wording, stale PR Readiness wording, selected-next ambiguity, release-window contributor ambiguity, or `No Active Branch` conflict after merge, the output digest must say `Governance Intake Routing: send this to C:\Nexus Worktrees\Governance on feature/release-readiness-source-truth-intake` and must include the originating worktree, branch, PR, merge commit, blockers, and next legal phase.

`Branch Cleanup Plan:` records stale/old branches, retired worktrees, and stale GitHub Desktop entries that may need cleanup after merge. `Branch Cleanup Execution Gate:` must keep cleanup blocked during Release Readiness; stale/old branch cleanup executes only during the next `Branch Readiness Stage 2 - Execution Gate` that creates or validates the replacement branch/worktree. Before deleting any branch or removing any worktree, Codex must prove `git worktree list`, current branch targets, and GitHub Desktop binding so no GitHub Desktop-bound worktree is left without a valid branch target. `Stable Worktree Path Preservation Gate:` is required when the target is a family-stable or GitHub Desktop-bound folder path; Codex must record `Stable Worktree Path:`, `Replacement Binding Path:`, and the preservation method, and must stop on `Stable Worktree Path At Risk` if cleanup would remove the stable path before the successor branch/worktree is moved, switched, or explicitly rebound there.

Assigned Worktree Confinement is mandatory for every thread assigned to a specific worktree. Before mutation, Stage 2 execution, commit, push, PR work, release work, runtime validation, shortcut/provider/model action, branch/worktree cleanup, or GitHub Desktop handoff, report `Active Thread Owner:`, `Thread Assignment Status:`, `Worktree Ownership Ledger:`, `Intended Write Set:`, `Same Worktree / Same Branch Collision Check:`, `Dirty Worktree Collision Check:`, `Dirty Worktree Recovery Packet:`, `Off-Worktree Work Routing:`, `Governance Routing Barrier:`, `New Worktree Decision Gate:`, `Expected Worktree Root:`, `Actual Worktree Root:`, `No Cross-Worktree Mutation:`, and the `GitHub Desktop-bound worktree`. If the active root is not the assigned root, stop on `Worktree Escape User Waiver Missing`; if another active thread owns the same worktree or branch, stop on `Parallel Worktree Coordination Missing`; if the target worktree is dirty and ownership is unclear, stop for a `Dirty Worktree Recovery Packet`. If the requested work belongs outside the assigned worktree, outside the active branch scope, or to another active lane, stop on `Governance Routing Barrier` and route the packet to `C:\Nexus Worktrees\Governance`; Governance decides whether an existing owner, new worktree/thread, or USER waiver is required. The assigned thread must not mutate sibling worktrees, parked clones, or the neutral/main folder by convenience unless the USER grants `Worktree Escape User Waiver: Granted` with expected root, actual root, target root, allowed commands/files, expiration or stop condition, required validation, and return path.

That startup pass must make explicit:

- source-of-truth layer selection
- `Record State` when the task maps to a tracked item
- current branch truth and whether the branch is the correct execution base
- the canonical workstream doc when one exists
- the reuse baseline
- the next safe move

## Exact Prompt Contract And Phase Resolver

Every phase-sensitive execution prompt must include:

- `Mode`
- `Phase`
- `Workstream`
- `Branch`

Add these when relevant:

- `Branch Class`
- `Active Seam`
- `Validation Contract`
- `Timeout Contract`

If `Phase` is missing or is not one of the exact canonical phase names from `Docs/phase_governance.md`, execution is blocked and only truth-validation or analysis may continue.

Before answering â€œwhat phase are we in?â€ or â€œwhatâ€™s next?â€, run the phase resolver from `Docs/phase_governance.md` and return:

- `Current Phase`
- `Phase Status`
- `Branch Class`
- `Blockers`
- `Governance Drift Found`
- `Next Legal Phase`
- `Plan To Reach That Phase`

For governed execution output, also return:

- `Seam Status`
- `Slice Status`
- `Completion Status`
- `Waiver Status`
- `Continue Decision`
- `Continuation Execution Latch`
- `Stop Basis`
- `Next Legal Phase`

Generic `Results` or `Validation` headings are not enough by themselves.
Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation.
Formal Next Legal Phase Digest is required whenever a phase packet stops for USER approval. The response must include a `Next Legal Phase Digest` with `Current Phase:`, `Next Legal Phase:`, `Why This Phase Is Next:`, `Approval Required:`, `Exact USER Approval Text:`, `Allowed Scope:`, `Explicit Exclusions:`, `Validation Required:`, `Stop Conditions:`, `USER Plan Review Gate:`, `USER Inspection Files:`, `Review Required Because:`, `Implementation Blocker:`, and `Review Waiver Reason:`. Missing fields block on `Next Legal Phase Digest Missing`; `Next Safe Move` or informal recommendations cannot replace the digest.
Formal Next Legal Phase Digests must not be compacted, abbreviated, summarized away, replaced by one-line next-step wording, or omitted because similar information exists elsewhere in the packet. `USER Plan Review Gate:` must state whether USER may accept, revise, waive, or reject the plan. `USER Inspection Files:` must name the exact files or local USER Review Hub Bundle when review is required. `Implementation Blocker:` must name the blocker when implementation remains unauthorized.
A green seam does not authorize stop while `Slice Status` remains non-green.
A green slice does not authorize stop while `Completion Status` remains non-green.
A green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice.
If `Completion Status` is `In Progress` and no named blocker or waiver stops work, Codex must continue rather than returning `Await Next Instruction`.
Use these governed state markers as execution control, not just reporting.
If `Continue Decision` is `Continue`, do not end on a seam-complete final response, rollback path, or next-seam recommendation; keep executing until a lawful `Stop` decision exists.
A prompt `Return:` block is an output shape only; it cannot override governed continuation markers or authorize a terminal response while `Continue Decision` remains `Continue`.
A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
After Workstream execution is admitted for a multi-seam or multi-slice package, the approval covers bounded execution of the admitted same-branch Workstream package unless USER explicitly limits the approval to a named seam and records a waiver/split. Per-seam approval-missing / approval-pending wording such as `First Bounded Implementation Seam Approval Missing`, `Next Bounded Seam Approval Missing`, or `SLC implementation pending USER approval` is not a real blocker. Bounded Workstream execution continues one active seam at a time until Workstream Green, a real named blocker, or explicit USER waiver is recorded.
If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
`Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
`Phase: Workstream` must remain bounded at all times; the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
Phase Boundary Stop Required: A phase-exit seam named in `Next Active Seam` is a handoff target, not current-phase execution authority.
Bounded Workstream continuation ends at phase boundaries; it never crosses from Workstream into Hardening by inertia.
Codex must not execute Hardening, Live Validation, PR Readiness, Release Readiness, release work, or any other next phase in the same run unless USER explicitly admits that phase after reviewing the handoff.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.
If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.
Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.
A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.
If `Completion Status` is `Red`, `Continuation Action` must report the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume.

## Branch And Lane Governance

PR-readiness is not the default checkpoint after a clean slice.

Default checkpoint:

- branch-level lane evaluation

Branch Readiness must establish the branch-level execution plan before Workstream begins.
That plan must name the branch objective, target end-state, expected seam families and risk classes, validation contract, User Test Summary strategy, later-phase needs, and the first Workstream seam or initial seam sequence.
Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
Branch Readiness is organized inside the same canonical phase as `Branch Readiness Stage 1 - Analysis Gate` followed by `Branch Readiness Stage 2 - Execution Gate`.
Stage 1 is analysis-only and outputs `## Branch Readiness Stage 1 Analysis Packet`; it allows no repository file mutation, branch creation, package admission, docs sync, PR work, release work, selected-next truth, or canon edits.
The Branch Readiness Stage 1 packet must include governed state markers, FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, product vision, project-wide vision alignment, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable vs full-system boundary, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, rejected shallow plan, alternatives/tradeoffs, open USER decision points, deferred ideas/future-package ledger, validation plan, `Stale Branch Cleanup Plan:`, expected docs sync, blockers and waivers, rollback path, `Branch Readiness Planning Incomplete` blocker review, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed.
Runtime-focused Branch Readiness Stage 1 must also include `## Runtime Branch Engineering Contract` so the branch cannot proceed from broad seam labels into underspecified implementation. Required markers are `USER Engineering Planning Review:`, `Runtime Implementation Approval:`, `Current Runtime Baseline:`, `Planned Runtime Delta:`, `User-Facing Runtime Delta:`, `State / Config / Schema Delta:`, `Validator / Helper Delta:`, `Expected Changed Files / Surfaces:`, `Approval-Boundary Audit:`, `Future-Gated Items:`, `Workstream Seam Map:`, `Proof Expectations:`, `Risk Forecast:`, `Recommendations And Alternatives:`, `Plan Version / Revision Status:`, and `Plan-To-Implementation Traceability:`. Stage 1 may mark the contract `Proposed` and implementation approval `Pending`; Stage 2 must admit or revise the exact branch purpose, Workstream label, first runtime delta, pending USER decisions, setup list, and contract status before Workstream can begin. New or re-entering runtime-focused branches must create or admit a Branch Runtime Engineering Plan at `Docs/branch_plans/<branch_slug>.md`, link it from the branch authority record with `Branch Runtime Engineering Plan Path:`, carry `Engineering Plan Status:`, keep backlog and roadmap compact pointer/status surfaces, and keep `PR Fold-Down Packet:` pending until PR Readiness compares the branch against the plan. Workstream Entry must create or refresh the active worktree's local USER Review Hub Bundle under `C:\Nexus USER\<worktree-label>` with sibling `C:\Nexus USER\<worktree-label>.zip`, flat copied branch vision, branch plan, branch authority, relevant Nexus/family vision, matrix, UFD/change-intent, and source-truth files before asking USER to green-light implementation. Workstream Entry must also return the `USER Branch Plan Review Gate` packet with the plain-language branch goal, planned user-facing outcome, visual/behavioral description when relevant, implementation breakdown, Hardening plan, Live Validation / UTS plan, USER design review questions, Codex recommendations, implementation options, alternatives/tradeoffs, accepted/deferred/rejected scope, exact USER decision needed, `USER Review Response:`, `Codex Response Digest:`, and `USER Review Packet Finding:` proving the USER hub packet was loaded, digested, and freshness-checked or explicitly waived. `USER_BRANCH_PLAN_REVIEW.md` is the required BP2 user-facing engineering plan review artifact derived from accepted or waived BP1 before bounded Workstream implementation: USER response must be attached or inserted and then digested by Codex, or an explicit USER waiver must be recorded; missing proof blocks on `USER Branch Plan Review Missing`, stale metadata blocks on `USER Review Packet Stale`, and an omitted digest blocks on `USER Review Packet Not Digested`. BP1 / `USER_BRANCH_VISION_REVIEW.md` owns product/design vision; BP2 must not replace or re-center the branch vision contract. Runtime Workstream Entry with multiple admitted slices or seams must also perform whole-package analysis before first-seam implementation and stop on `Workstream Entry Whole-Package Analysis Missing` if that proof is absent. Workstream entry, each seam start packet, seam closeout, Workstream Green, Hardening, Live Validation, PR Readiness, and Release Readiness must compare actual runtime behavior, changed files, UI copy, state/config/schema changes, validator/helper proof, future-gated items, and public release language against the admitted contract and Branch Runtime Engineering Plan. If repo truth proves the contract or plan is too narrow, stale, or wrong, Codex must stop on a plan revision packet instead of improvising runtime behavior.
Branch Planning separates planning from implementation. BP1 creates or revises `USER_BRANCH_VISION_REVIEW.md` as the USER-facing branch vision/end-state contract. BP2 creates or revises `USER_BRANCH_PLAN_REVIEW.md` as the engineering plan derived from accepted or waived BP1. BP3 is Workstream Entry / Orchestration Validation and may return implementation approval only when BP1 and BP2 are accepted or explicitly waived. Workstream itself is runtime/code implementation and code-level validation only; do not use Workstream for vision review, plan review, Hardening, Live Validation, PR Readiness, or Release Readiness work.

Workstream Entry USER hub packet proof must also be decision-path consistent before implementation can be approved. Helper output, validator output, Codex digest, or external governance state owns branch identity, HEAD, baseline, exact USER decision, and next legal phase proof. USER-facing folder files remain plain-language review context. A packet that still says repair/revalidation or implementation-blocked is a valid blocking review artifact only; it cannot be treated as implementation approval through chat-only explanation.
The stable local USER hub review folder and sibling exported zip must be regenerated from clean matched-pair paths, not incrementally reused. `dev/orin_user_review_bundle.py` owns the durable helper path: quarantine or clear the old `C:\Nexus USER\<worktree-label>` folder and `C:\Nexus USER\<worktree-label>.zip`, prove both stable paths are absent, copy fresh repo-relative source truth, write `START_HERE.md` as a plain-language index, atomically replace the stable sibling zip, then validate the zip's branch, `HEAD`, `origin/main`, file list, `USER_BRANCH_PLAN_REVIEW.md`, stale-guard proof, and packet finding internally before claiming the USER packet is current. Technical proof prints in helper output; stale folder contents, stale uploaded zip metadata, missing `USER_BRANCH_PLAN_REVIEW.md`, or mismatched helper proof blocks on `USER Review Packet Stale`. Cloud-backed Desktop / OneDrive copies are mirrors only and must not be the upload source.

Branch Planning review reinforcement: `USER_BRANCH_VISION_REVIEW.md` is the BP1 Branch Vision Contract, a user-facing product/design vision document, decision ballot, and implementation blocker. It must make the branch goal, End-State Vision, Visual / Functional Walkthrough, surfaces, flow, options, risks, recommendations, USER design questions, accepted vision, deferred ideas, assumptions, and waiver/acceptance posture understandable before engineering planning hardens around the wrong product shape. `USER_BRANCH_PLAN_REVIEW.md` is the BP2 USER Branch Plan Contract, a user-facing engineering plan derived from accepted or waived BP1. It must include `Contract Status`, `Contract Version / Revision`, accepted branch vision summary, implementation package, what USER will actually see and where, surface map, SLC/seam plan, affected surfaces/files, validators/helpers, proof requirements, H1/LV/UTS expectations, rollback/safety, open engineering risks, future-gated boundaries, `USER Response`, `Codex Response Digest`, `Implementation Constraints Created By USER Response`, `Vision Delta / Source-Truth Impact`, `Contract Change Log`, `Contract Completion Checklist`, and `Workstream Entry Result`. BP1 and BP2 `Contract Status` must be `Draft`, `Pending USER Response`, `Pending Codex Digest`, `Pending USER Confirmation`, `Complete`, or `Waived by USER`; bounded Workstream implementation remains blocked unless required BP1/BP2 statuses are `Complete` or `Waived by USER` and BP3 validates orchestration. SLC/slice/seam sequencing is BP2 engineering route detail and must not replace the BP1 end-state review. When USER feedback changes branch direction, UI behavior, workflow, scope, boundaries, or seam order, Codex must convert that feedback into testable implementation constraints, update impacted source truth, refresh the local USER hub packet/ZIP, set `Contract Status` to `Pending USER Confirmation`, and repeat the loop until USER confirms the final contract or explicitly waives it.

USER-facing review files must avoid technical Git packet metadata. Branch HEAD, SHA, origin/main, merge base, ZIP hash, and similar freshness values belong in helper output, validator output, Codex chat digest, or external governance state, not in `START_HERE.md`, the readable branch vision, or the branch plan contract.
BP1/BP2 USER review packets are early-phase USER/ChatGPT review aids, not durable evidence or posterity archives. Keep them current only through the active BP1/BP2/BP3 review loop before implementation approval; fold accepted outcomes into source truth, then let later phases use source truth, branch diff, proof artifacts, fold-down receipts, and phase packets unless they explicitly route back to Branch Planning or Branch Readiness for a vision/plan repair.
`Carrier Lifecycle Decision` is mandatory in Branch Readiness Stage 1 for the requested branch/worktree. It records `Carrier Lifecycle Classification:` as exactly one of `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, or `Active remote/open PR branch`, plus `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Stale Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`. Stage 1 must recommend `create/recreate fresh branch` for a stale empty local branch that is behind current `origin/main`, has no unique commits, and has no open PR dependency; Stage 2 may execute that recommendation only after USER approval and must not delete or switch unrelated FAM worktrees.
`Full Feature Element Breakdown` must feed the owning `Element Validation Ledger` before Workstream begins or resumes. Stage 2 source-truth repair must convert created, touched, affected, deferred, future, dependency-only, and non-gating supporting elements into row-level ledger entries or a canonical companion-ledger pointer owned by the active workstream doc or branch authority record.
If Codex creates, touches, or indirectly affects product-significant UI, runtime behavior, hidden user-facing behavior, source-truth boundaries, validation artifacts, screenshots, or UTS questions without updating the owning ledger, stop on `Element Ledger Placement Drift`, `Created Element Untracked`, `Touched Element Proof Missing`, or `Affected Element Validation Missing` as applicable.
For broad implementation family packages, marker-only planning is insufficient. The packet must prove the branch understands the whole product/system, not just the next UI or helper slice: `Project-Wide Vision Alignment:`, `Branch-Specific Vision Alignment:`, `System Concept Model:`, `Entity / Profile Model:`, `User Workflow Model:`, `Scale / Data Volume Model:`, `Configuration And State Model:`, `Expected User-Facing Outcomes:`, `Codex Additional Recommendations:`, `USER Critique Loop:`, `USER Decision Ledger:`, `Deferred Ideas / Future Package Ledger:`, `Planning Adequacy Review:`, `Rejected Shallow Plan:`, `Alternatives And Tradeoffs Reviewed:`, `Whole-System Interaction Map:`, `Minimum Viable vs Full System Boundary:`, and `Open Questions / USER Decision Points:` must be present, concrete, non-placeholder, and non-empty before Workstream, Hardening, Live Validation, or PR Readiness. Codex self-assessment is not enough: the plan must name the shallow/simple plan it rejected, alternatives/tradeoffs considered, how multiple product pieces interact, concrete scale pressure, minimum-vs-full boundary, and USER decision state. When USER input is needed, Codex must provide a `USER Vision Question Packet` with decision context, recommendation, rationale, alternatives, tradeoffs, current-branch impact, future-package impact, safe default, waiver/defer posture, and exact response format. When USER needs a durable editable handoff, Codex must generate or refresh a USER-facing `User Vision Input.txt` desktop artifact with three answer paths for each decision: accept Codex recommendation; change recommendation with USER-written changes; or defer/future-package/waive with USER-written reason. That artifact is not repo source truth, and recommendations or blank answers are not USER approval; repo truth updates only after a later USER-approved digest pass reads and summarizes the completed artifact. Workstream, Hardening, Live Validation, or PR Readiness entry or continuation is blocked while `Product Vision Input Missing`, `Project-Wide Vision Alignment Missing`, `Branch-Specific Vision Alignment Missing`, `USER Vision Question Packet Missing`, `USER Vision Recommendation Missing`, `USER Vision Questions Unanswered`, `USER Vision Input Pending`, `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, `System Concept Model Missing`, `Entity / Profile Model Missing`, `User Workflow Model Missing`, `Scale / Data Volume Model Missing`, `Configuration And State Model Missing`, `Expected User-Facing Outcomes Missing`, `Codex Additional Recommendations Missing`, `USER Critique Loop Missing`, `USER Decision Ledger Missing`, `Deferred Ideas / Future Package Ledger Missing`, `Planning Adequacy Review Missing`, `Rejected Shallow Plan Missing`, `Alternatives And Tradeoffs Missing`, `Whole-System Interaction Map Missing`, `Minimum Viable vs Full System Boundary Missing`, `Open Questions / USER Decision Points Missing`, `Branch Reach Unproven`, `Feature Element Breakdown Missing`, `Acceptance Criteria Missing`, `User-Facing Proof Standard Missing`, `Current Branch vs Future Package Boundary Missing`, or `Branch Readiness Planning Incomplete` remains active unless explicit USER waiver text is recorded.
For user-facing family/package branches, Branch Readiness must declare an `Interface Release Boundary` before Workstream begins or resumes. The default release path is one primary user-facing interface surface per branch, recorded as `Primary Interface Release Surface:` with a clear fallback point, acceptance criteria, and proof path. Multiple released user-facing interfaces in one branch require explicit `Interface Bundle User Approval: Granted`; without it, `Interface Release Boundary Missing`, `Primary Interface Undefined`, `Multiple Interface Release Drift`, `Fallback Point Missing`, `Interface Acceptance Missing`, or `Branch Readiness Interface Planning Incomplete` blocks Workstream. This does not weaken bounded multi-seam execution: multiple seams and slices remain expected inside the approved interface boundary, and supporting dependency repairs must be classified separately from released interface acceptance.
When completed USER input exposes package-specific architecture, telemetry, warning, privacy, cross-family, persona/model, or naming questions, Branch Readiness must keep those blockers active until revalidation clears, defers, or waives them. Package-specific planning blockers include `Legacy Product Name Drift`, `Hardware Telemetry Provider Selection Pending`, `Polling Floor Undecided`, `Warning Delivery Modality Pending`, `External Telemetry Privacy Model Missing`, `Audio Warning Cross-Family Approval Missing`, and `Persona Switch Scope Boundary Pending`. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.
A broad family-package plan remains incomplete while scope, future-package deferrals, provider path, polling posture, warning modality, privacy model, naming/product-copy handling, acceptance criteria, or proof standards are only candidate statements. Stage 2 may finalize those boundaries after USER approval; implementation resumes only after Stage 1 revalidates the finalized plan or records an explicit USER waiver.
`Branch Readiness Execution User Approval Missing` blocks `Branch Readiness Stage 2 - Execution Gate` until explicit USER approval to enter Stage 2 is recorded.
Workstream must execute an admitted implementation slice unless the USER explicitly approves a docs-only bypass.
Workstream must keep re-evaluating the backlog item after each seam and slice and continue on the same branch until the backlog item is fully implemented or only future-dependent blockers remain.
Docs-only Workstreams require explicit USER approval.
Planning-loop bypass requires `Planning-Loop Bypass User Approval: APPROVED` and `Planning-Loop Bypass Reason:`.
Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
Branch existence, branch rename, backlog promotion, repair-only traceability, or release-bearing posture do not count as Workstream progress by themselves.

Stay inside the active grouped lane until one of these is true:

- the milestone threshold is satisfied
- a real blocker appears
- the next work crosses subsystem boundaries
- the user explicitly stops

After a lane is closed or merged:

- the next implementation workstream must execute from updated `main` on a fresh branch
- the next workstream must be selected, canon-defined, minimally scoped, and explicitly not branched during `PR Readiness`
- the successor branch is created only during `Branch Readiness` after the current branch merges and updated `main` is revalidated

If a branch becomes:

- stale
- merged
- identical to `main`

Codex must call that out explicitly and recommend a fresh branch from updated `main`.

Before any next implementation branch may enter `Branch Readiness`, the repo-level admission gate from `Docs/phase_governance.md` must pass.

If the admission gate fails:

- repo state becomes `No Active Branch`
- no next implementation branch may begin
- the next safe move is blocker repair, not next-lane execution

Release-packaging branches may still begin from `No Active Branch` only when their branch-class admission rules from `Docs/phase_governance.md` pass and their branch authority record is explicit.
Governance-only branches are not used for new Nexus work.
`main` is protected for Codex work: Codex may read it for truth validation but must not edit, stage, commit, generate, refresh, or directly repair files on it.
There is no emergency direct-main repair path for Codex.
If canon drift is discovered before merge, repair it on the owning branch before PR green.
If canon drift is discovered after merge, do not open or resurrect a standalone repair branch for that drift; block the next legitimate runtime-focused backlog branch's `Branch Readiness` and repair there before implementation.
If a stale-canon or governance-drift class is discovered, the same branch or next legal repair surface must also patch the canon or validator rule that allowed it before the repair is considered complete.
Escaped drift prevention proof is mandatory: every repair for a miss discovered after the phase that should have caught it must include source-truth, governance, validator, helper, or prompt-contract hardening that prevents the same class from passing again, or must record why the gap is not machine-checkable yet and what human review marker replaces it before green.
merge-stable pointer surfaces such as backlog and roadmap must not mirror transient repair-branch ownership while merged-main truth remains `No Active Branch`.
Any tracked file mutation while Codex is on `main` is a `Main Write Attempt` blocker.

Active-branch-first remains the normal rule for tightly coupled canon and governance work.
When a governance or canon update is directly required to keep the active branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct, carry that update on the active branch inside its current phase and branch class.
That allowance does not permit unrelated governance churn, product scope expansion, validation weakening, stop-condition weakening, or phase-authority bypass.
Do not use a standalone `docs/governance` branch to carry routine canon or governance work that belongs on an already-active implementation or release branch.
Do not open a governance-only branch for between-branch canon repair.
Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
If PR Readiness missed required canon or docs work and the owning branch has already merged, the next active branch must treat the miss as a `Branch Readiness` blocker and repair it before implementation begins.

Backlog identity is USER-gated:

- Codex must not create, split, promote, or select a new backlog identity without explicit USER approval.
- Backlog items are major user-facing feature-family or major release/support lanes, not small single-seam runtime proofs, governance repairs, validation follow-through, hotfixes, or blocker-clearing repair traces.
- If Codex believes a backlog identity, package admission, branch creation, backlog split, promotion, selected-next successor, or single-slice package waiver is needed but approval is absent, stop on `Backlog Addition User Approval Missing` and output every FAM that is still not closed plus every package or slice that is not complete, including ID, title, Status, Record State, Priority, package state, slice state, and available selection/deferred/minimal-scope fields.
- If that still-not-closed FAM and not-complete package/slice list is empty, stop on `Backlog Exhaustion User Decision Pending` and wait for USER direction.
- Small runtime follow-through inside an existing family is family evidence or aggregation material by default; it must not become a standalone release-version driver without explicit USER approval.

Pre-PR Durability Rule:

- before `PR Readiness`, when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state
- this applies through `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`
- a prompt-level request to stop before commit/push is not a durability exception; only a documented `Durability Waiver`, failed validation, legally file-frozen `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push
- if Codex names a self-imposed blocker, it must name the lift condition; once lifted, Codex must automatically commit and push without requiring a second durability prompt
- if validation fails, do not commit and push; report the blocker and keep the branch in the current phase until the blocker is lifted
- `PR Readiness` still performs the final dirty-branch and durable-truth gate before PR creation

For active promoted work, the canonical workstream doc is the single authoritative owner of:

- `Current Phase`
- `Phase Status`
- `Branch Class`
- `Blockers`
- `Entry Basis`
- `Exit Criteria`
- `Rollback Target`
- `Next Legal Phase`

Backlog, roadmap, and prompt text may reference phase state, but they must not override the workstream doc.

For selected `Registry-only` backlog branches in `Branch Readiness`, and for approved non-backlog branches, the single authoritative owner is the branch authority record under `Docs/branch_records/`.

## Canon Freshness Rules

Supporting canon must stay aligned with live truth.

That means:

- PR Readiness hard blocker shorthand is `stale-canon`, `post-merge`, `dirty`, `docs-sync`, `next-workstream-if-selected`, `Backlog Addition User Approval Missing`, `Backlog Exhaustion User Decision Pending`, `deferred-context`, `uts-results`, `pr-created`, and `pr-validated`
- directly supporting canon and tightly coupled governance may be updated on the active implementation or release branch when that branch changes or depends on the truth
- no PR-ready without canon-ready:
  - a branch is not PR-ready if merging it would leave `main` canon-stale
- no PR-ready with stale canon:
  - current-state canon and merge-target canon must already reflect the branch's true state and the state that will be true after merge
  - Merge-target post-merge-stable authority projection is mandatory before PR green and is a PR Readiness Stage 1 repair responsibility when Stage 1 finds it: `Merge-Target Authority Projection Unproven` blocks Stage 2 and PR green when post-merge truth will be `No Active Branch` but the PR branch would merge an active branch authority record into `main`; default governance validation and `--pr-readiness-gate` must both catch this state before merge; the active authority record must be moved to historical/no-active posture or otherwise made merge-stable during Stage 1 before Stage 2 can execute, and historical branch records must not retain active PR Readiness phase, active seam ownership, live/open PR wording, merge-watch ownership, or `PR Merge Verification Pending`
- when a branch closes a workstream, changes released milestone posture, changes the current rebaseline, changes closeout-index routing, changes backlog status, changes roadmap stage-breakpoint/checkpoint posture, changes workstream-index release posture, or changes `Docs/Main.md` baseline routing, the required release-facing canon updates must already be on that branch before PR creation is allowed
- no PR-ready with inconsistent already-selected next workstream:
  - Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection, rooted in Nexus Vision, family vision, branch vision, current completed work, and the next implementation need.
  - PR Readiness does not require selected-next truth or a waiver by default. If post-merge truth resolves to `No Active Branch` because no USER-approved selected-next truth exists, the next runtime implementation pipeline waits for Branch Readiness Stage 1.
  - PR Readiness may encode or validate selected-next truth only when USER explicitly approves PR-time selected-next sync or selected-next truth already exists and would merge as durable repo truth.
  - when USER-approved PR-time selected-next truth exists, the selected workstream must be a real runtime `Feature Family` candidate selected from canon using open backlog `Priority` plus deferred-context readiness, not `Target Version`.
  - when USER-approved PR-time selected-next truth exists, that workstream must be recorded in `Docs/feature_backlog.md` and `Docs/prebeta_roadmap.md`, have canon-valid `Record State`, define runtime `Minimal Scope:`, and have no implementation branch created yet.
  - when selected-next truth already exists but is incomplete, stale, branch-created too early, or inconsistent across backlog/roadmap, PR Readiness stops on the selected-next blocker until the current branch repairs it or routes the repair to Branch Readiness.
  - `Next Runtime Candidate Selection Pending` applies only when USER-approved PR-time selected-next truth or already-encoded selected-next truth is inconsistent; otherwise normal next runtime candidate selection waits for Branch Readiness Stage 1.
  - successor branch creation is deferred to `Branch Readiness` after the current branch merges and updated `main` is revalidated.
- no PR-ready with unresolved post-merge planning:
  - if post-merge truth needs release-debt handling, no-release-debt posture, branch-authority cleanup, or repair of already-encoded selected-next truth, that handling must already be complete inside PR Readiness Stage 1 when Stage 1 finds it; Stage 2 may verify and execute the PR, but it must not be the first phase that repairs those source-truth projections
  - Post-merge `No Active Branch` is allowed when no USER-approved selected-next truth exists; that state is not a successor-selection waiver, and it routes normal next-branch selection to Branch Readiness Stage 1.
- no PR Readiness Stage 2 without USER review approval:
  - `PR Readiness Stage 1 - Analysis Gate` is an analysis-first blocker repair gate and must produce `## PR Readiness Stage 1 Analysis Packet`
  - Stage 1 must analyze repo truth, identify PR-readiness drift/blockers, repair any current-branch PR-readiness drift or blocker it finds, validate those repairs, and commit/push durable repair truth when files changed before Stage 2 can proceed
  - Stage 1 specifically owns repair of already-encoded selected-next truth, merge-target `No Active Branch` projection, no-release-debt posture, any unavoidable merged-unreleased release-debt owner contract, and active-branch-authority cleanup when those items are found; leaving them as a Stage 2 sync plan keeps `PR Readiness Stage 1 Repair Pending` active
  - `PR Readiness Stage 1 Repair Pending` blocks Stage 2 whenever Stage 1 found repairable PR-readiness drift/blockers that are not yet repaired, validated, and durable
  - Stage 1 still allows no PR creation, watcher provisioning, next-branch creation, release work, tag creation, GitHub Release draft/publication, release artifact creation, runtime package admission, selected-next truth encoding, branch creation, or waiver handling unless explicit USER approval separately grants that action
  - the packet must include governed state markers, planned PR title/base/head/summary, required post-merge path, release-debt impact, release-debt handling status, selected-next validation status when selected-next truth exists or PR-time selection is explicitly approved, planned merge-target canon updates, planned watcher provisioning and reporting surface, planned validations, expected Stage 2 file changes, Stage 1 repairs made, Stage 1 repair validation, Governance Ledger fallback status, Branch Readiness fallback status, Stage 2 sync plan, drift findings, blocker and waiver findings, release-window audit posture, rollback path, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed from the USER
  - a user-facing `## Next Workstream` block and no-work `## Next Branch Pre-Plan` block are optional in PR Readiness and appear only when USER asks PR Readiness for successor-selection analysis or selected-next truth already exists
  - missing next-workstream recommendation, missing selected-next truth, missing `Next Workstream User Waiver:`, or omitted next-branch pre-plan does not block Stage 2 by default
  - `Next Branch Package Shape Unproven`, `Single-Slice Branch Drift Risk Unresolved`, and `Family Organization Drift Risk Unresolved` are Branch Readiness Stage 1 blockers by default; PR Readiness uses them only for USER-approved PR-time selected-next truth or already-encoded selected-next truth that would merge as durable repo truth
  - `Current-Branch Branch Readiness Re-entry Required` blocks Stage 2 when selected-next, next-branch, or governance/source-of-truth blockers cannot be cleared as bounded PR Stage 1 repair but the current branch remains the legal carrier
  - `New Carrier Branch Required` blocks Stage 2 when the current branch is stale, merged, invalid, or cannot legally own the blocker and a new real carrier branch/package analysis is required
  - `PR Readiness Execution User Approval Missing` blocks `PR Readiness Stage 2 - Execution Gate` until explicit USER approval to enter Stage 2 is recorded
  - Stage 2 preserves the existing PR Readiness work sequence after Stage 1 projection is durable: verify required canon, commit and push only bounded operator metadata if legally needed, run the normal validator and PR-readiness gate mode, create the PR, provision and prove the watcher, validate live PR state, handle bot-review signals, and continue merge-watch
- no PR-ready with an incomplete merged-unreleased release-debt owner contract:
  - PR Readiness must not treat new unreleased implementation release debt as a normal acceptable merge result; if unavoidable, USER must explicitly approve the exception before PR creation and Stage 1 must leave merge-target canon in the exact post-merge shape
  - required machine-checkable fields are `Merged-Unreleased Release-Debt Owner:`, `Repo State: No Active Branch`, `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, and `Post-Release Truth:`. `Selected Next Workstream:` and `Next-Branch Creation Gate:` are required only when USER explicitly approved PR-time selected-next truth or selected-next truth already exists.
  - release-target correctness is semantic, not marker-only: derive the target from the latest public prerelease and the declared `Release Floor:` before PR green
  - `patch prerelease` increments patch only, for example `v1.4.0-prebeta` -> `v1.4.1-prebeta`; `minor prerelease` increments minor and resets patch, for example `v1.4.0-prebeta` -> `v1.5.0-prebeta`
  - `patch prerelease` is the default for architecture-only planning, admission contracts, validation-only work, documentation/canon repair, governance repair, UX polish, bug fixes, and non-user-facing milestones that do not add executable product behavior
  - `minor prerelease` requires a new executable, runtime, operator-facing, user-facing, or materially expanded product capability lane; opening a planning lane or writing architecture is not enough by itself
  - after a public prerelease tag exists for a release-debt owner, durable canon must close that workstream as Released / Closed, advance latest public prerelease truth, clear release debt, and move the workstream index entry to Closed before any next implementation work begins
  - active-branch truth must be removed from main-facing backlog, roadmap, and workstreams index canon before PR green
  - Release Readiness consumes these inherited fields; it must not create or repair them in files
- no PR-ready with a dirty branch:
  - the worktree must be clean before `PR READY: YES`
  - required docs changes must be committed
  - required canon state must not exist only in the working tree
  - branch truth must be durable in commit history
- no PR-ready without docs-sync and drift-audit completion:
  - docs sync, Governance Drift Audit, validator alignment, and required post-merge wording must be complete and mutually consistent
  - run the branch governance validator and its PR-readiness gate mode before reporting `PR READY: YES`
- no PR-ready with an incomplete release-window audit:
  - if the branch is operating inside an unreleased release window, PR Readiness must record a `Release Window Audit`
  - the normal green posture is `Remaining Known Release Blockers: None`, `Another Pre-Release Repair PR Required: NO`, and `Release Window Split Waiver: None`
  - do not knowingly land one blocker-clearing PR while another blocker-clearing PR is already known to be required in the same unreleased window by default
  - the only allowed exception is an explicit user-approved `Release Window Split Waiver`, recorded with a reason
  - missing or incomplete proof keeps the named blocker `Release Window Audit Incomplete` active
- no PR-ready without user-facing desktop-shortcut validation:
  - for relevant desktop user-facing workstreams, `User-Facing Shortcut Live Validation Gate` must pass or be explicitly waived before PR Readiness can report green
  - the active authority record must declare `User-Facing Shortcut Path:` and `User-Facing Shortcut Validation:` before User Test Summary handoff
  - helper-only, direct-runtime, WebView-only, sandbox/offscreen, synthetic, active-client direct-runtime, or harness evidence may support Live Validation, but it does not replace the final real user-facing desktop launcher or shortcut gate when that launcher path is feasible
- no PR-ready without Codex live-client self-QA:
  - for relevant desktop user-facing workstreams, `Codex Live Client Self-QA Gate` must pass or be explicitly waived before User Test Summary handoff and PR Readiness
  - the active authority record must declare `Codex Live Client Self-QA:`, `Visual Quality:`, `Live Interaction Evidence:`, `Usability Check:`, and `Platform Uniformity Check:` so quality, usability, interaction behavior, and NDAI uniformity are not collapsed into marker proof
  - the active authority record must also declare `Codex Visual Adjudication:`, `Visual Artifact Review Scope:`, `Product Vision Alignment:`, `Per-Element Visual Verdicts:`, `Helper Marker Limitation:`, `Unacceptable UI Findings:`, and `LV1 Handoff Disposition:` for desktop UI Live Validation; helper PASS, marker PASS, screenshot existence, and manifest existence cannot clear visual acceptability by themselves
  - interactive user-facing UI must be exercised in the launched live client; screenshot-only, marker-only, or launched-but-not-driven proof cannot clear this gate
  - desktop UI Live Validation requires both reviewable screenshots and short video or ordered frame-sequence proof for acceptance-critical interactive/transient states; the video/frame proof must be a durable artifact referenced by the manifest, not a prose claim
  - desktop UI Live Validation requires a per-element visual inventory and detailed focused screenshots in addition to context screenshots; every current user-facing window, border/frame, card, row, page break/divider, background treatment, scrollbar, button, dropdown, checkbox, input, chip, status field, confirmation, empty/error/deferred state, supported state/action, and USER-named issue element must be copied to `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\<validation-lane>\<timestamp>\focused_element_screenshots\`, include the element label/name and state/action in the PNG filename, map to the active issue-form ID when applicable, and be enumerated in the manifest; full-desktop screenshots are context only and cannot clear per-element visual acceptance
  - returned USER UTS, screenshot, or video issues that block acceptance must live in a temporary issue form until PR Readiness Stage 1 folds the resolved truth into durable source truth; the form must carry the issue ID/name, planned disposition, validation/photo/video requirement, proof artifact path, and USER-verifiable status so future branches do not lose the issue
  - desktop UI proof must include an active foreground/user-observable client mode; hidden, too-fast, or blink-through helper evidence is supporting automation evidence only
  - while `Codex Live Client Self-QA Pending` remains active, do not hand off the feature as ready for USER acceptance
- no PR-ready with `User Test Summary Results Pending`:
  - automated validators and live helper evidence may be green, but final phase advancement remains blocked while a required User Test Summary handoff is outstanding
  - returned User Test Summary results must be submitted or explicitly waived, digested into the active authority record, and reevaluated before PR Readiness can report green
  - if returned results expose mismatch, regression, cleanup failure, ambiguity, or scope drift, route back to `Workstream` or `Hardening` instead of advancing
- no Release Readiness with missing merged closeout proof:
  - post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript
  - if missing proof blocks a release and the branch has not merged, carry it back through PR Readiness; if the branch has already merged, carry it on the next real runtime package carrier's Branch Readiness before implementation begins
  - direct-main repair remains blocked
- no PR-ready before PR creation and PR validation:
  - `PR package ready` is not `PR Readiness GREEN`
  - PR creation is part of PR Readiness completion, not a later phase
  - the GitHub PR must exist before final green
  - the PR must be open, non-draft, conflict-free, inspectable, and aligned to merge-target canon
  - a missing PR keeps `PR Creation Pending` active
  - unresolved Codex comments/issues, requested changes, or inability to inspect the PR keep `PR Validation Pending` or `PR State Unknown` active
  - until the live PR explicitly reports a green merge status, keep `PR Merge Status Unproven` active; unknown, unset, conflicting, dirty, blocked, or otherwise non-green mergeability/merge-state results do not clear the gate
  - for Codex-created PRs, `Bot Review Signal Pending` also keeps PR Readiness non-green until the live PR has a thumbs-up reaction from the Codex GitHub bot on the current PR head. A bot comment keeps `PR Validation Pending` active until the branch fixes the comment on the same PR, pushes, replies to and resolves the review thread, asks Codex to re-analyze the updated head, and records a fresh current-head thumbs-up reaction; an eye/watch reaction or resolved comment alone does not clear the gate. This is the same-PR Codex bot-review repair loop. Stage 2 final handoff and merge execution cannot be green until the current-head thumbs-up closeout is verified
  - when `Bot Review Signal Pending` is active on a live Codex-created PR, Stage 2 must provision or update a PR watcher before handoff; report-only/manual polling is insufficient unless USER explicitly waives watcher repair authority. The watcher must inspect bot reactions, bot comments, review threads, PR comments, inline comments, and mergeability, and it must be authorized to perform bounded same-PR repairs for valid Codex bot comments that stay inside the approved PR scope: repair, validate, commit, push to the same branch, and report the closeout. If no Codex bot comment or thumbs-up/approval signal appears after the current PR head has been live for at least two minutes, the watcher must post exactly one PR conversation nudge for that head SHA asking the Codex bot for the review signal, and must not repeat that nudge for the same head. Out-of-scope bot requests must be reported as blockers instead of repaired.
  - if a branch expects watcher-based PR monitoring, `PR Watcher Provisioning Unproven` also keeps the gate blocked until the watcher target, approved reporting surface, routing proof, runtime path, run-proof method, fallback, teardown rule, and replacement provisioning for the next live PR are explicit and proven; accepted watcher proof may come from native Codex heartbeat run evidence or from a bounded local watcher that posts status-change updates through the official Codex thread-resume path into the approved reporting-surface transcript, records delivery proof through assistant-message transcript presence, Codex thread-state refresh, and automation run/inbox visibility, and manual rollout-file or transcript-file injection does not count as proof. Watcher configuration is not runtime proof. Stage 2 final handoff cannot be green until watcher runtime proof is present or the runtime-proof blocker remains active
  - the PR Watcher Mode Contract lives in `Docs/pr_watcher_mode_contract.md`; every watcher must declare `Silent Monitor`, `Verify Once`, `Repair Mode`, or `Blocked Mode`, and Stage 2 final handoff must include `Watcher Health Proof:` with configured cwd, PR number, head SHA, unresolved review-thread count, latest bot review, repair authority, delivery route proof, runtime proof, and next watcher posture
  - `PR Watcher Routing Unverified` also keeps the gate blocked until the approved reporting surface is explicitly recorded and the configured thread/host target, state-file target, transcript target, and delivery proof have been cross-checked against it
  - standard operating procedure from now on is a watcher on an approved Codex reporting surface at minute cadence that reports only when a watched PR status changes; the current working thread is the default surface, but an explicitly recorded dedicated watcher-host thread is allowed when that is the validated user-visible route
  - watcher status-change output must be source-of-truth shaped with governed state markers, live PR truth, watcher proof, blocker state, continue/stop decision, and, after `merged=true`, a copy/paste Codex prompt basis for the next legal Release Readiness validation; the watcher may clear merge-verification blockers but must not independently claim Release Readiness legality
  - if final merge delivery proof is missing, the watcher must keep running and retry instead of retiring
  - after live PR creation, live PR validation, merge-status green, and bot-review approval, PR Readiness continues into a merge-watch seam
  - `PR Merge Verification Pending` keeps PR Readiness blocked until that watcher on the approved reporting surface verifies that the live PR is `merged`
  - phase-critical automation cannot clear a gate merely because its card, config, or automation list says `ACTIVE`; `ACTIVE` is configuration state, not run proof, so keep `Automation Runtime Unproven` active until thread/inbox output, automation memory/log/state-file updates, scheduler last-run evidence, or another accepted run proof exists
  - Automation Observability Review Pending is checked with `dev/automation_observability_report.py`; standing automation findings in Codex automation run/inbox rows or `$CODEX_HOME/automations/*/memory.md` are promoted into source-of-truth work only when classified as `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED`, and any such finding needs a bounded repair seam before repo canon changes
  - background-observability-only automations are advisory only; stale historical toolchain-path reports are `REVIEW_INFO` unless current source truth still owns the referenced path, and they must not clear PR watcher runtime proof, bot-review repair proof, merge verification proof, or release-readiness proof
  - if the preferred Codex automation remains `ACTIVE` without run evidence, the owning phase stays blocked until run evidence exists or a bounded fallback is activated; any bounded fallback must be target-scoped, phase-scoped, read-only, and self-terminating or explicitly deleted when its terminal condition or phase exit occurs
- no PR-ready with a PR Readiness scope miss:
  - named blockers are `PR Readiness Scope Missed`, `Between-Branch Canon Repair Attempt`, and `Next Branch Created Too Early`
  - PR Readiness must complete branch-authority cleanup, merge-target canon, post-merge truth, next-workstream selection, next-branch deferral, and release-debt routing on the active branch before green
  - do not defer that work to Release Readiness, updated `main`, a later governance-only branch, or a between-branch repair window
  - if the next branch already exists before the current branch merged and updated `main` was revalidated, block as `Next Branch Created Too Early`
- no Release Readiness green with `Release Target Undefined`:
  - Release Readiness must declare `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, and `Candidate Includes Later Governance Repairs:` for the selected release candidate
  - Release Readiness must declare `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, and `FAM Contributor Routing:` for the selected release candidate
  - `Release Candidate Anchor Missing` blocks Release Readiness when those fields are absent or ambiguous
  - `Release Window Contributor Inventory Missing` blocks Release Readiness when multi-FAM/worktree contributor inventory is absent or ambiguous
  - unless USER explicitly selects another release target, Release Readiness validates current fetched `origin/main`; historical PR merge commits are audit evidence only
  - merge order does not decide release ownership; when multiple FAM/worktree branches merge before the next release, the release owner is `Release Ownership Model: Aggregated release window` unless USER explicitly opens a release packaging branch or selects a narrower target
  - if current fetched `origin/main` contains FAM-006 and FAM-007 merged-unreleased scope, both scopes must be inventoried and release-ready before Release Readiness can be green, or USER must select a target that excludes the not-ready scope
  - governance/source-truth-only PRs merged after the last runtime PR may be included in the release candidate; they do not force the release candidate back to the last runtime merge commit
  - when later governance/source-truth repair PRs are included, `Candidate Includes Later Governance Repairs:` must be `YES`, and release notes may keep those repairs in internal validation/traceability instead of presenting them as user-facing product features
  - a release-bearing branch must explicitly declare `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:` before Release Readiness can report green
  - stale or semantically mismatched release target truth is still `Release Target Undefined`, even when all fields are present
  - Release Readiness is analysis-only for repository files; it may produce release package information in the response, but it must not edit, stage, commit, generate, or refresh source, docs, canon, validator, helper, release-note, or handoff files
  - after Release Readiness Stage 2 publishes a release and post-publish release/tag/body/health validation is green, stale external operational records that still point to the just-released branch, PR, release window, selected-next state, or previous source commit are `Post-Release External State Carry-Forward`, not release debt, not durable repo canon drift, and not a Release Readiness blocker by themselves. Codex may reconcile only `C:\Nexus Governance State` in the bounded RR2 post-release closeout without a new USER decision when Git/GitHub/repo validation is green and no repo source, branch/PR, merge, release, cleanup, FAM, runtime, private, provider, cache, or memory surface is mutated. If not reconciled in RR2, BR1 reports `Post-Release External State Carry-Forward:` and BR2 reconciles it before branch/worktree setup or implementation.
  - if Release Readiness analysis discovers missing, stale, or ambiguous release candidate anchor/target/scope/artifact truth, do not patch in Release Readiness; return to `PR Readiness` on the active branch if unmerged, or defer the repair to the next legitimate runtime-focused backlog branch's `Branch Readiness` or the standing governance intake lane if already merged
  - if Release Readiness identifies stale/old branch or worktree cleanup, record `Branch Cleanup Plan:` and `Branch Cleanup Execution Gate:` only; cleanup waits for `Branch Readiness Stage 2 - Execution Gate` branch/worktree creation so no GitHub Desktop-bound worktree loses its valid branch target
  - tracked file changes while the authority record says `Release Readiness` are blocked as `Release Readiness File Mutation Attempt`
  - release-bearing includes `release packaging` branches and any branch that creates, prepares, validates, tags, publishes, or transitions release-facing artifacts or release-state canon
  - small single-seam runtime proof inside an existing family may be recorded as aggregation evidence with `Standalone Release Driver: No`; that evidence does not justify a release version by itself unless the USER approves a larger feature-family release or release aggregation
  - the only non-release waiver is `Release Branch: No`
  - `Release Branch: No` is limited to preserved historical records
  - the non-release waiver is not available to `implementation` or `release packaging` branches
  - the waiver does not clear `Release Debt`, weaken post-merge truth rules, weaken validation, or permit premature successor branch creation
- operator output is evidence-first for PR summaries and inclusion-only for release notes:
  - PR Readiness PR creation details must use separate copy-ready blocks for `PR Title`, `Base Branch`, `Head Branch`, and `PR Summary`
  - Release Readiness release package details must use separate copy-ready blocks for `Release Title`, `Release Tag`, `Target Commit`, and `Release Notes`
  - PR summaries and release notes must report implemented or released work only
  - PR summaries use exactly `## Summary`, `## Branch Evidence`, and `## Validation`; `## Summary` is one concise outcome paragraph, `## Branch Evidence` must not repeat it through nested Summary/Purpose/Overview sections, and `## Validation` must contain proof only
  - concise branch-specific boundaries are allowed inside `## Branch Evidence` when they clarify reliable branch truth
  - GitHub release notes must use the standard Markdown release body shape used by the current pre-Beta releases: start with `## Release Summary` or `## Release Overview`, continue with `## Release Highlights` or release-specific rich sections, then include GitHub-generated `## What's Changed` and the generated `**Full Changelog**:` compare link to the previous release
  - the live GitHub release body must not start with or repeat the release title as `# <release title>`; the release title belongs in GitHub release metadata and the separate `Release Title` operator block only
  - Release Execution must use GitHub-generated release notes, through the GitHub release notes button or generated-release-notes API, so the `## What's Changed` section and previous-release compare link are populated from GitHub instead of hand-written or omitted
  - public release bodies must not include internal automation/tooling brand tokens, generated branch-prefix noise, phase-handoff text, operator transcript text, or public lines such as `[codex]` / `codex/...`; rewrite those labels into neutral user-facing PR names before publication or repair the release body immediately after publication
  - all published Nexus pre-Beta release bodies remain governed public release surfaces and must keep matching the same release-body standard; only explicitly legacy-scoped releases are outside that pre-Beta normalization rule
  - do not include generic `Not Included` sections, exclusion-list dumps, negative scope framing, or defensive wording in operator summaries or release notes
  - keep normal source-of-truth scope, non-goals, stop conditions, and blockers in canon records; the inclusion-only rule applies to operator-facing PR and release packages
- post-release canon closure is standard lifecycle follow-through:
  - prepare closure during PR Readiness when possible, or record bounded release-dependent drift and repair it during the next approved Branch Readiness Stage 2 carrier when publication truth cannot exist before release
  - release execution and post-release canon closure are separate; post-release canon drift must land in remote source truth through the approved Branch Readiness carrier before implementation begins
  - a local-only post-release closure commit is a blocker, not completed source truth
  - protected-main branch rejection must route to the next approved Branch Readiness Stage 2 canon/governance repair carrier, not direct-main mutation, standalone cleanup, or a default release-support branch
  - post-release validation must compare published GitHub release/tag truth and release-body format against remote repo source truth
  - runtime implementation remains blocked until release publication exists, post-release canon drift is explicitly recorded or repaired through the approved Branch Readiness carrier, and owning validation reports green
  - transitional drift is exceptional, not normal; if unavoidable, it requires explicit USER approval, a named owner, a real-carrier repair plan, and blocking source-truth markers before PR creation. It must not be handled by a default cleanup/canon-sync branch.
- governance-only branches are not used for new Nexus work:
  - governance and canon repair ride on the active runtime-focused branch when tied to that branch's truth
  - between-branch canon repair is blocked
  - standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work
  - governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`
  - the only standing exception is the `Standing Governance Intake Branch`, `feature/release-readiness-source-truth-intake`, at `C:\Nexus Worktrees\Governance`; it accepts a `Release Readiness digest`, USER-approved `automation/worktree governance intake`, or USER-approved `phase-gate governance intake` only, uses `RRI-YYYYMMDD-NNN`, enforces operational `One Active Cycle`, requires the pre-intake `Sync Rule` against clean `origin/main`, pauses the originating lane in `Waiting For Governance Intake` or `Waiting For Updated Main`, and must send a post-merge `Return Digest` with the exact originating branch, originating worktree, operating workspace, expected branch, and `Neutral Main Workspace Rebaseline:` proof copied from the accepted intake; it is exempt from dedicated closeout PRs whose only purpose is to clear `Active RRI Cycle`
  - the standing governance lane must stop on `Return Digest Origin Identity Missing` instead of defaulting a return prompt to `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Governance`, GitHub Desktop's selected repository, or the current shell CWD when the accepted intake recorded a different originating worktree
  - merged-main `No Active Branch` means no active runtime, implementation, release packaging, or repair carrier; it may coexist only with the standing governance intake authority record, and any other active branch authority record remains a validation blocker
  - a USER-approved workspace-resilience or dev-tooling governance foundation carrier may exist only when repo truth records a multi-worktree/thread-safety gap that blocks safe future branch work; it must not admit runtime implementation, package admission, release work, issue work, AI Product Contract import, or future standalone governance branch creation
  - if no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia
  - historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation
  - direct writes to `main` are blocked as `Main Write Attempt`
  - Release Readiness must not absorb docs sync or canon cleanup that PR Readiness should have completed
  - Release Readiness must not mutate files to repair a discovered gap; use `PR Readiness` before merge or the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge
- do not use canon sync as an excuse for broad unrelated documentation churn

Thread / Worktree Identity Preflight:

- before `Branch Readiness Stage 2`, `Workstream`, `Hardening`, `Live Validation`, `PR Readiness`, `Release Readiness`, branch creation, worktree creation, commit, push, PR creation, release action, meaningful repo work, file mutation, or GitHub Desktop handoff, Codex must verify the current working directory, git repository root, branch, upstream, `HEAD`, `origin/main`, `git worktree list`, clean/dirty state, intended local workspace role, expected phase/seam, and intended write target
- local workspace roles are `Main/consolidator`, `active branch worktree`, `parked fallback`, `historical/lab context`, `private/dev workspace`, or `artifact output root`
- `C:\Nexus Desktop AI` is the local main/consolidator workspace by default after workspace reconsolidation; tracked file edits on `main` remain blocked, and it becomes an active branch workspace only when the active branch record and Thread / Worktree Identity Preflight assign it
- `C:\Nexus Worktrees\` is the governed local root for active branch worktrees after workspace reconsolidation; retired worktrees there are not active carriers unless a current branch record names them
- `D:\Nexus Repos\Nexus Desktop AI Main` and `D:\Nexus Worktrees\` are retained fallback/historical workspace paths unless later USER-approved governance or identity preflight assigns them a current role; `D:\Nexus Dev ORIN\` and `D:\Nexus Artifacts\` remain private/dev or artifact roots whose contents are evidence only until legally imported
- `codex/ai-llm-lab` is historical AI Lab planning traceability only; after USER-approved consolidation into the current feature branch it has no active local/remote branch ref and must not be recreated or reused as a governance carrier, runtime carrier, or FAM-007 implementation carrier without USER-approved repo governance
- assigned parallel worktrees are allowed when USER explicitly assigns separate Codex threads to separate active branch worktrees; each assigned thread must record its expected path, branch, upstream, `HEAD`, `origin/main`, source-truth owner, write target, active thread owner, thread assignment status, worktree ownership ledger, intended write set, same-worktree/same-branch collision check, dirty-worktree collision check, dirty-worktree recovery packet posture, and worktree role before mutation
- the default repo-wide limit is two active assigned branch worktrees; a third active branch worktree or any same-file, same-source-truth-owner, same-worktree, same-branch, dirty-worktree ownership, unknown active-thread owner, or missing worktree ownership ledger overlap between active worktrees requires a USER decision before continued mutation
- an assigned thread may have no created branch yet when it is intentionally waiting in Release Readiness analysis, Branch Readiness Stage 1 analysis, or updated-main wait posture for another branch to merge; this is `Waiting For Updated Main`, not an active branch worktree, and it must remain file-freeze/read-only until updated `origin/main` is fetched, source truth is revalidated, and USER approves any later branch creation or mutation
- multi-worktree branch health markers are: clean/dirty state, ahead/behind state, merge-base freshness, current `origin/main`, upstream reachability, merge forecast, open PR state, branch retirement/cleanup expectation, and whether the branch has source truth projected to merge-stable posture
- multi-worktree file health markers are: changed-file list, intended write set, shared-file overlap with the other active worktree, generated/log artifacts, validator/helper files, source-truth files, line-ending warnings, and unresolved conflict risk
- future FAM-007 worktrees must branch from updated `origin/main`, not from the parked AI lab branch
- before interactive desktop validation, Codex must confirm no Nexus/Python runtime from another worktree is active; only one interactive desktop validation may run at a time
- across related Nexus worktrees, use one Git operation at a time where practical, and run source-truth freshness checks before phase transitions
- before PR creation, run changed-file overlap review and merge/conflict forecasting against `origin/main`
- before USER-driven GitHub Desktop operations, confirm GitHub Desktop is bound to the intended local repository folder
- for the `Standing Governance Intake Branch`, GitHub Desktop must be bound to `C:\Nexus Worktrees\Governance` before USER-driven Desktop operations so the standing branch is not confused with FAM-006, FAM-007, or the main/consolidator folder
- if the active folder, branch, upstream, workspace role, expected phase/seam, write target, runtime/process owner, or GitHub Desktop binding does not match the requested work, stop on `Thread / Worktree Identity Mismatch` and report expected workspace, actual workspace, expected branch, actual branch, expected write target, actual write target, expected thread/workstream role, actual repo state, mismatch evidence, and the safest next correction
- `Thread Launch / Write-Target Identity Lock` is the permanent pre-mutation gate for Nexus work: a stale parked branch, AI Lab context, old worktree, fallback folder, wrong GitHub Desktop repository, wrong write target, or unknown lane identity requires a routing packet and blocks source edits, branch/worktree creation, commits, pushes, PR work, release work, shortcut mutation, provider/model installation, and runtime validation until corrected
- dirty worktree collision recovery is freeze-first: when a target worktree has uncommitted tracked changes before a new thread claims it, do not clean, stash, reset, overwrite, commit, or continue by inference. Inventory dirty files, identify the owning thread per file, preserve or discard only with USER approval, then resume with one active owner and a validated `Worktree Ownership Ledger`.

Local docs overlays are reference material only until revalidated against updated `origin/main`.

Time-sensitive current-state claims must live only in designated current-state owners, or be part of the merge-target canon update set.

Allowed current-state owners are:

- backlog
- roadmap
- active workstream doc
- workstreams index
- closeout index
- current rebaseline or closeout file
- `Docs/Main.md` routing

Auxiliary guidance docs should be timeless by default.
If they carry live-current claims, they must either be updated as part of canon sync or stop owning current-state truth.

## Governance Drift Rule

If a branch exposes a governance weakness such as:

- a missing blocker
- a weak phase entry or exit rule
- a weak source-of-truth ownership rule
- stale prompt scaffolding or stale examples
- a missing validator requirement

that weakness must be classified as `Governance Drift`.

If governance drift is discovered:

- stop normal progression immediately
- if the drift is directly coupled to the active branch's truth, phase, readiness, validation, closeout, or release state, fix it on that active branch after the boundary is explicit
- otherwise, produce the exact required canon delta and wait for user confirmation
- if the same drift class could recur, the repair must also harden the canon or validator rule that allowed it instead of only patching the one stale surface
- every repeated or carried blocker must include a recurrence analysis before green: what failed, why current governance/validation missed it, what prevents the same failure next time, and whether canon or validator coverage must change

Do not defer known governance weaknesses silently to a later branch.

When a branch changes:

- repo-wide phase governance
- current-state owners
- prompt scaffolds
- active promoted workstream phase-state records

it must also run:

- `python dev/orin_branch_governance_validation.py`

and keep that validator green before calling the branch ready.

## Change Discipline

- one fix per revision means one coherent approved subproblem per revision
- minimal isolated changes means the minimal coherent change set needed to close that approved subproblem
- grouped workstreams are allowed during `pre-Beta` when they remain coherent by subsystem and end-state
- a grouped branch may carry as many validated slices as needed when they all belong to the same backlog item, milestone, and coherent end-state
- `Docs/phase_governance.md` owns seam workflow behavior; prompts and task text may name seams, but they do not define continuation authority
- `bounded multi-seam workflow` is the primary Workstream execution model inside the current slice
- `Next-Seam Continuation Required` means continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green
- bounded means one active seam at a time, not one-seam Workstream authority
- a single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete
- a prompt-named seam is the entry seam, not a terminal boundary
- Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
- Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
- a slice is a bounded admitted backlog-completion unit; a seam is the current execution checkpoint inside or between slices
- seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress
- there is no repo-wide cap on how many slices a branch or workstream may carry
- same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green.
- when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
- `Workstream` reaches `Hardening` only when `Completion Status: Green`
- `Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; one green seam or one green slice cannot move the branch to Hardening while admitted branch material remains.
- `Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation
- `Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item.
- use `Backlog Completion State: In Progress`, `Implemented Complete`, or `Implemented Complete Except Future Dependency` to record whether more same-branch slices are still required
- unrelated ideas must still be split out even if they look convenient to batch

Bounded multi-seam workflow means:

- multiple seams may execute in sequence within one approved phase boundary only when phase governance allows it
- each seam still has one active owner, exact boundary, explicit non-includes, validation gate, cleanup expectation, and continue-or-stop decision
- Codex must continue by default to the next seam needed inside the current slice when the continuation authority conditions pass
- reporting `Next Safe Move` is not a substitute for execution when continuation authority passes.
- A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice.
- durability commit/push after a green seam is a checkpoint, not a stop
- A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
- Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
- Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
- `Continuation Execution Latch` remains active whenever `Continue Decision: Continue`, `Stop Basis: None`, and a same-phase `Next Active Seam` are recorded; Codex must execute the next seam in the same bounded Workstream run instead of returning a terminal report.
- when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
- a bounded stop condition, phase boundary, or stop-loss trigger blocks continuation but does not by itself authorize stopping the backlog item after only one slice
- every seam must remain in the same workstream or active authority record, same phase, same branch class, same approved scope, and same subsystem family or tightly coupled implementation, validation, or governance chain
- Branch Readiness may use planning, admission, or tightly coupled governance-repair seams, but not product/runtime implementation
- Workstream uses the full seam pipeline for safe approved execution
- Hardening and Live Validation may use constrained validation or evidence-digestion loops, but they must not become hidden feature lanes
- PR Readiness uses readiness gates, not product implementation seams
- Release Readiness remains analysis-only and file-frozen

Stop the workflow immediately if validation fails, regression appears, scope drifts, risk class changes, governance drift appears, manual validation becomes blocking, or branch truth no longer matches the authority record.

Do not use category labels as stop authority.
Bug fixes, hotfixes, unclear seams, high-risk seams, cross-subsystem changes, settings, protocol, launcher-policy, and UI-model work require the smallest safe seam, stronger validation, and an explicit continuation check.
They do not require stopping after a green seam when the current slice still needs another validation-backed seam inside the same bounded workflow.
Legacy `Single-Seam Fallback` and `Single-Seam Mode Waiver` wording is retired and must not be used in active source-of-truth.
Stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition.
If no explicit approval is raised and no bounded stop condition is recorded, keep later slices on the same branch by default and advance into them automatically while `Completion Status` remains `In Progress`.

Use the smallest safe slice for:

- architecture clarification
- boundary-setting
- high-risk behavior or policy work

Use the smallest coherent slice for:

- lower-risk follow-through inside an already-approved milestone when a smaller fragment would leave the milestone incomplete

These are execution rules, not analysis-stop rules.

## Testing And Validation

Every revision must include:

- healthy-path verification
- failure or edge-case verification when relevant
- runtime log review
- crash log review when present
- artifact cleanup verification when relevant
- session cleanup verification when relevant

Interactive validation must also be time-budgeted.
Codex must not allow stalled validation runs, harnesses, or desktop exercises to sit indefinitely.

When the branch is in governed closeout recovery, `Docs/phase_governance.md` is the controlling timeout and stop-loss authority unless the active workstream doc explicitly documents a tighter contract.

Interactive validation is reuse-first.
Before creating a new live-validation helper, Codex must inspect the existing repo helper surface and use, parameterize, extend, or extract shared support from existing helpers when that is safe.
Temporary one-off probes may be used only under ignored evidence roots, may not become closeout-grade proof by inertia, and must be deleted after the pass unless deliberately promoted into documented reusable tooling.

Validation helper naming and ownership are registry-governed.
Before adding or keeping a durable root `dev/` validation helper, live-validation script, audit helper, harness, or shared helper module, Codex must route through `Docs/validation_helper_registry.md`.
That registry defines the allowed `Helper Status:` values, naming scheme, owner rules, `Workstream-scoped` exception markers, `Temporary probe` handling, and `Consolidation Target` requirements.
New feature work must extend an existing helper family whenever that is safe; creating a new helper is allowed only after registry lookup proves reuse would contaminate proof ownership, blur branch truth, or make validation less reliable.
Workstream-scoped helpers must be registered before closeout-grade proof can depend on them and must carry a promotion or consolidation decision before PR Readiness.

When an interactive validation pass is relevant, it must use:

- a full-run hard timeout
- a no-progress watchdog timeout
- scenario and/or transition budgets where the flow has distinct multi-step seams
- an outer execution timeout that sits only slightly above the interactive harness hard cap rather than extending it by many additional minutes

For meaningful interactive desktop closeout work, helpers should also follow the repo-wide validation helper contract from `Docs/phase_governance.md`.
That means:

- marker-first proof by default
- explicit separation of gating and non-gating observations
- runtime helper support when it materially improves deterministic startup or runtime logging
- watchdog enforcement plus last-progress logging
- cleanup guarantees
- saved-state or source snapshots when write safety or no-write blocking behavior matters
- live re-resolution of windows, dialogs, overlays, and controls across close/open seams
- seam classification before product code is changed during validation hardening

If no tighter helper-specific watchdog is active, `10s` without meaningful progress is the maximum allowed no-progress interval for live validation.
Meaningful progress means a new runtime marker, step-log entry, scenario transition, UI readback, screenshot/proof artifact, process-state observation, cleanup confirmation, or explicit last-progress update.
If that interval is exceeded, Codex must abort the run, clean up session state, report the last confirmed progress point, and classify the stall before patching anything.

When the approved boundary is a continuous `Hardening` pass on the current branch, Codex should keep iterating through seams without waiting for a new user prompt after every rerun unless:

- a blocker appears
- truth drift appears
- stop-loss is reached
- canon sync becomes required before the next rerun

Do not claim closeout-grade green status from a helper profile that only passed under one-off command-line overrides.
The helper's documented default profile must itself prove green before that branch can be treated as truly green.

If a timeout or freeze is detected, Codex must:

- abort cleanly rather than letting the run continue indefinitely
- perform the required session cleanup
- explicitly report the timeout or stall condition
- explicitly report the last confirmed meaningful progress point
- route helper or harness repair back through `Hardening` unless the authority record explicitly allows validation-only support edits in the current phase

For hardened desktop helpers, the working target is not just eventual completion.
The working target is also responsiveness:

- no-progress or transition waits should normally stay within `3s`
- normal seam or scenario completion should normally stay within `60s`
- if a helper keeps needing longer waits, patch the proof path or helper design rather than silently normalizing the delay

If the timeout contract in the active workstream doc and the live harness behavior drift apart, the workflow is blocked until that drift is reconciled in canon before continued execution is recommended.

After any validation run, test pass, runtime exercise, harness execution, or other operational step, Codex must also clean up what it created or opened during that session unless there is a deliberate reason to preserve it.

This is not satisfied by a best-effort attempt alone. Before handoff, Codex must explicitly verify that the cleanup actually happened for the apps, windows, dialogs, helper processes, temporary files, probe documents, and other session-scoped artifacts it opened, started, or created during the pass.

That includes, when relevant:

- closing programs, dialogs, or windows Codex opened
- stopping helper processes, harnesses, validators, or temporary runtimes Codex started
- deleting temporary files, temporary documents, scratch outputs, or probe files Codex created only for the pass
- restoring source files, settings, or local state Codex intentionally modified for the test
- confirming the machine or workspace is not left in a noisier or more invasive state than necessary for the user
- verifying that user-visible apps or windows opened for the pass, such as Notepad or File Explorer windows, are actually closed rather than assumed closed

If something created during the pass must remain on disk or stay open intentionally, Codex must say so explicitly and explain why it was preserved.

Before handing a user-visible runtime, UI, or manual validation path back to the user, Codex must run that same path or the closest faithful equivalent when feasible.

For relevant desktop, runtime, user-facing, or operator-facing slices, if the implemented path can be launched and exercised through a real desktop session in the current environment, true interactive OS-level validation is the default continuation gate.

In that case:

- validator results remain baseline automated proof
- synthetic or headless harnesses remain stronger supporting proof
- a real interactive OS-level session is the required gate before Codex recommends normal continuation
- manual user handoff remains an additional operator layer, not a substitute for Codex's own feasible interactive validation

If Codex cannot self-run the same path reliably, it must say so explicitly and identify the remaining validation gap.

When a slice materially changes user-facing desktop UI, Codex must also plan a post-green live launched-process UI audit before closeout.
That audit is a closeout-quality check, not a screenshot requirement for every seam iteration.

When the approved issue itself is visual or layout-specific, marker proof and
functional click-path proof are not enough. The H1/live validation path must
include a check that would fail the reported visible defect, such as measured
geometry, overlap/gutter assertions, screenshot audit evidence, or another
durable visual proof tied to the exact user concern. If returned USER media
contradicts the active-client result, treat the active-client result as
insufficient proof, reopen the branch to Hardening, and patch validation before
claiming PR readiness.

For runtime, UI, startup, prompt, voice, or other operator-facing implementation slices, green validators are necessary but not sufficient on their own.

Before continuing to the next implementation slice on the same branch, Codex must also perform a deeper branch-local validation and hardening pass that:

- pressure-tests the implemented path and its likely failure modes
- checks integration seams and branch-local regressions beyond the happy path
- adds or creates the smallest reliable validation infrastructure on-branch when the current suite leaves meaningful blind spots
- uses supporting validation artifacts when needed, such as validators, harnesses, fixtures, scripted helpers, trace capture, screenshots, runtime logs, or reproducible sample inputs
- uses synthetic or headless validators and harnesses as supporting evidence rather than the final continuation gate when a real desktop session is feasible
- launches and exercises the real desktop or runtime path through an interactive OS-level session when feasible rather than stopping at simulated reasoning or headless proof
- preserves evidence of what was run, what passed or failed, and where the supporting artifacts live
- explicitly distinguishes:
  - validator results
  - synthetic or headless validation results
  - simulated reasoning or inspection findings
  - interactive OS-level execution results
  - manual user-test handoff that still remains
- explicitly decides whether the correct next move is:
  - continue implementation
  - pause for internal hardening or validation
  - or fix a specific defect first

Validator-green status plus simulated reasoning, recap-style summary, or synthetic/headless harness results is not enough when the implemented desktop or runtime path can be exercised through a real interactive OS-level session.

When Codex recommends continuing implementation after a user-visible slice, it must be able to explain why the current validation and hardening depth is already sufficient for that continuation.

If the current validation surface is too thin to support that explanation, Codex must first add the smallest reliable validation infrastructure on-branch and re-run the validation pass before continuing.

If a real interactive OS-level session is not feasible, Codex must say so explicitly, explain why, cite the strongest available non-interactive evidence, and state that the continuation recommendation is limited by the missing interactive gate.

When a slice changes user-visible behavior, runtime interaction, UX flow, prompts, startup behavior, voice behavior, or any manual operator-facing path, Codex must include a true manual validation checklist under `## User Test Summary` by default.

That checklist must include:

- setup or prerequisites
- exact user actions
- expected visible behavior
- failure signs to watch for
- branch-specific or slice-specific validation focus

A recap-style summary is not sufficient when manual validation is relevant.

If no meaningful manual test exists for the change, Codex must say so explicitly under `## User Test Summary` and explain why manual validation is not materially relevant for that slice.
`## User Test Summary Strategy` is planning context only; it does not satisfy the canonical repo-level `## User Test Summary` artifact.

For active desktop workstreams, the default canonical repo-level UTS planning surface is the User Test Summary strategy in the relevant canonical workstream doc unless that doc explicitly declares a different repo path. The formal exact `## User Test Summary` returned-results artifact belongs to Live Validation Stage 1 only.
User Test Summary is exclusive to Live Validation Stage 1.
Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.
PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact.

When that strategy exists and supporting docs are in scope on the active branch, Codex must update it as part of the same slice by default.

For bounded multi-seam Workstream execution, User Test Summary strategy handling is incremental plus final Live Validation preparation:

- update the canonical workstream User Test Summary strategy as user-visible or operator-facing seams land
- when the Workstream seam chain is complete, preserve the handoff needs for later Live Validation Stage 1; do not create/refresh the formal desktop UTS export and do not use returned UTS results as a Workstream stop condition
- before User Test Summary handoff in Live Validation, run the `User-Facing Shortcut Live Validation Gate` for relevant desktop user-facing workstreams and record `User-Facing Shortcut Path:` plus `User-Facing Shortcut Validation: PENDING`, `PASS`, `FAIL`, or `WAIVED`
- before User Test Summary handoff in Live Validation, run the `Codex Live Client Self-QA Gate` for relevant desktop user-facing workstreams and record `Codex Live Client Self-QA:`, `Visual Quality:`, `Live Interaction Evidence:`, `Usability Check:`, and `Platform Uniformity Check:`
- before User Test Summary handoff in desktop UI Live Validation, run `Codex Visual Adjudication:` and record artifact-by-artifact PASS / REPAIR / STOP / WAIVED_WITH_REASON verdicts against the Product Definition Plan, Runtime Branch Engineering Contract, latest USER vision, and package UI/UX intent
- before User Test Summary handoff in desktop UI Live Validation, prove the per-element visual inventory, issue-form coverage matrix, USER-inspectable OneDrive focused screenshot folder, and every named focused screenshot path; missing inventory rows, missing issue coverage, missing element-labeled filenames, broad desktop-only proof, or `dev\logs`-only images are `REPAIR`
- if the relevant desktop UI is interactive, exercise the same live-client interactions Codex would ask the USER to test and record the evidence before handoff
- if the relevant desktop UI has hover, dropdown, scroll, resize, flicker, clipping, dirty-guard, confirmation, click-routing, or transient state behavior, LV1 must capture both focused screenshots and short video or ordered frame-sequence proof for those states before exporting the UTS; missing video/frame proof is a `REPAIR` result, not a waiverable Codex shortcut
- before exporting or refreshing a desktop UI UTS handoff, Codex must clear every unwaived Codex-visible `REPAIR` or `STOP` finding from the visual adjudication record, per-element inventory, issue-form matrix, interaction proof, and shortcut/human-client evidence; the UTS handoff is for USER acceptance, not for discovering defects Codex could already see
- when Live Validation discovers a current-branch UI/UX/interaction defect and approval covers bounded continuation, Codex must use the bounded repair/rerun loop: record the defect, repair it, rerun focused proof and required validators, update source truth, and then rerun Live Validation before returning to UTS; when approval does not cover the repair, return `BLOCKED` or `REPAIR` with exact approval needed instead of handing off a known-bad UTS
- digest returned user evidence in `Live Validation Stage 1` before recommending Stage 2 advancement
- route returned evidence back to `Workstream` for in-scope user-facing branch work, to `Hardening` for defects or validation gaps, or to backlog/defer handling for new feature requests

If required user-facing desktop shortcut evidence is outstanding, the active authority record must carry the hard blocker `User-Facing Shortcut Validation Pending`.

The shortcut blocker lifts only after `User-Facing Shortcut Validation: PASS` is recorded with evidence from the declared shortcut path, or `User-Facing Shortcut Validation: WAIVED` is recorded with `User-Facing Shortcut Waiver Reason:` proving the branch is not desktop/user-facing or the shortcut path is explicitly unavailable.
If `User-Facing Shortcut Validation: FAIL`, keep an explicit blocker and route back to `Workstream` or `Hardening` instead of exporting the branch as final-green.

If required Codex live-client self-QA is outstanding, the active authority record must carry the hard blocker `Codex Live Client Self-QA Pending`.
The self-QA blocker lifts only after `Codex Live Client Self-QA: PASS` is recorded with evidence from the launched client path, including `Live Interaction Evidence:` for interactive UI, or `Codex Live Client Self-QA: WAIVED` is recorded with `Codex Live Client Self-QA Waiver Reason:` proving the branch is not user-facing or the live client path is unavailable.
If `Codex Live Client Self-QA: FAIL`, keep an explicit blocker and route back to `Workstream` or `Hardening` before USER handoff.

If a required User Test Summary handoff is outstanding in Live Validation or PR Readiness, the active authority record must carry the hard blocker `User Test Summary Results Pending`.
Live Validation green requires an exact `## User Test Summary` state before final green.
Every Live Validation digest must include an exact `## User Test Summary` section; if User Test Summary is waived, the digest must still include `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`.
Workstream must not list `User Test Summary Results Pending` as the reason to stop implementation; it must continue implementation, internal sandbox validation, or named Workstream repair while current-branch product work remains.

Expected reporting model:

- Automated validators and live helper evidence: GREEN.
- User Test Summary Results: PENDING.
- Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.

The blocker lifts only after the filled User Test Summary is submitted or a documented waiver exists, the returned results or waiver are digested into the active authority record, and blockers are reevaluated.
When a waiver is used, the active authority record must include `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:` inside the exact `## User Test Summary` section.

Completing a User Test Summary update does not move the branch directly from `Workstream` to `PR Readiness`.
The normal next phase after Workstream completion remains `Hardening`.

Response-only `## User Test Summary` output does not satisfy the workstream-owned validation layer when the canonical repo artifact remains stale.

For desktop user-facing slices, Codex must also export or refresh the convenience copy at:

- `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

unless it explicitly explains why the desktop export is not relevant or is being intentionally skipped.

The ownership hierarchy is:

- workstream doc exact `## User Test Summary` section = canonical repo source of truth
- desktop `User Test Summary.txt` = required user-facing exported copy when relevant
- response-level `## User Test Summary` = current handoff text only

If Codex does not update the canonical repo-level `UTS` artifact, it must say explicitly why. Valid reasons are limited to:

- no meaningful manual test exists for the slice
- no canonical workstream doc exists yet for the active lane
- the user explicitly restricted the pass so the relevant artifact could not be updated
- the relevant closed workstream doc already says that no separate ongoing `UTS` artifact remains

If Codex does not export or refresh the desktop `User Test Summary.txt` copy for a relevant desktop slice, it must also say explicitly why.

Returned evidence such as `UTS`, screenshots, interactive reports, PR review comments, or release-review findings may satisfy exit criteria, but they must never auto-advance phase by implication.

Required sequence:

1. digest the evidence
2. update the authority record
3. reevaluate blockers
4. only then advance phase

## Runtime Evidence And Logging

- logs are the source of truth for runtime behavior
- do not assume behavior without log or code evidence
- prefer structured markers over raw output
- preserve or cite the exact validator outputs, helper scripts or harnesses used, runtime logs reviewed, and any created fixtures, traces, or screenshots that materially support a continuation recommendation
- when interactive OS-level validation is required and feasible, preserve or cite the exact session evidence that shows the real path was exercised, such as runtime logs, screenshots, structured markers, traces, or durable validation reports
- when meaningful desktop UI changed and a live launched-process UI audit was required, preserve or cite the audit manifest and the key captured windows as part of the final closeout evidence
- when desktop Live Validation depends on visual proof, capture the full virtual desktop by default for window-position frame of reference, copy the raw PNG into `C:\Users\anden\OneDrive\Pictures\Screenshots\<project-or-validation-lane>\<timestamp>\` or the active USER-declared screenshots folder, and surface that raw path in the Codex handoff/chat for USER inspection
- when the user wants to visually validate those screenshots inside the Codex client, do not rely on local-file image embeds as the default delivery path; keep the original audit captures on disk and use the client-compatible preview path documented in `Docs/codex_user_guide.md`
- the default client-compatible preview path is: preserve the original live capture on disk, generate a smaller derivative from that real file, and send one small inline PNG `data:` image at a time until render reliability is confirmed
- do not claim live-style validation without evidence or a specific explanation of what path was actually exercised

### Root Logs Governance

- the runtime root's ignored `logs/` directory and `logs/crash` child remain reserved for approved live launcher and runtime truth surfaces only
- launcher-owned historical state is not a root-owned live logs surface
- normal runtime historical state resolves under `%LOCALAPPDATA%/Nexus Desktop AI/state/nexus_history_v1.jsonl`
- dev, test, worker, and toolkit evidence must write under the runtime root's ignored `dev/logs/<lane>/...` evidence lanes
- no new dev or worker evidence roots may be introduced under the runtime root's live `logs/` directory without explicit approval
- historical `C:/Nexus/...` wording in older records does not override current root-relative launcher code truth

### Dev-Only Startup Snapshot Harness

For startup-state debugging, Codex may use the env-gated startup snapshot harness when it is the smallest reliable evidence path.

Rules:

- the harness must remain opt-in through `NEXUS_HARNESS_STARTUP_SNAPSHOT_DIR`
- snapshot output must write to an explicitly chosen dev evidence path, not root logs
- the harness is internal debugging infrastructure only
- if the harness is not needed for the active task, leave it disabled

## Historical Intelligence Rules

Cross-run intelligence must stay contract-defined in repo docs before implementation changes begin.

That contract must define:

- schema and versioning
- run identity
- failure fingerprint rules
- provenance labeling
- retention and reset behavior
- corruption and fallback behavior

Historical intelligence must remain explainable and deterministic rather than becoming a second hidden truth source.

## Documentation And Carry-Forward Review

Important architecture, orchestration, planning, and validation decisions should live in repo docs rather than only in chat history.

For every post-merge, post-release, or next-lane review, classify prior recommendations as:

- carry forward
- defer
- discard

Never treat prior suggestions as automatic scope.

For every `PR Readiness` pass, also run the formal Governance Drift Audit from `Docs/phase_governance.md`.
If that audit finds required canon strengthening, do not silently merge past it.

Use `Docs/Main.md` as the routing index for the merged canon.

## Backlog Governance

`Docs/feature_backlog.md` is a controlled registry layer.

Only true broad feature-family backlog entries should remain as parseable `### [ID: FAM-XXX]` backlog records by default. The legacy `FB-###` namespace is historical-only; historical pass aliases, support/governance lanes, and old registry-only implemented IDs are traceability rows that route to family dossiers, canonical workstream records, or same-file historical trace; they must not be selected as backlog items by inertia.

Canonical identity model:

- `FAM` is a broad long-lived product family.
- `Package` is a bulk branch/release package under exactly one FAM.
- `Slice` is a traceable deliverable area inside exactly one package.
- `Seam` is an execution or validation checkpoint.
- `PR` is merge/review evidence only.
- legacy global `FB` is historical trace only.

Branch scope standard:

- a branch should carry a family package with multiple admitted slices by default
- a single-slice package is blocked by `Single-Slice Package User Approval Missing` unless explicit USER approval records `Single-Slice Package User Approval: Granted`
- every slice must trace to exactly one FAM and exactly one package
- Workstream must continue through every admitted package slice before Hardening unless the package is truthfully marked `Complete`, `Released Baseline / Open`, `Blocked`, or `Deferred`
- admitted-slice counting is explicit: only `Admission State: Admitted` rows count; `Historical Evidence`, `Merged Evidence`, `Future Placeholder`, `Deferred Placeholder`, future package required rows, and deferred ideas are not admitted slices
- an admitted slice must have concrete scope, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder rows cannot satisfy the multi-slice rule
- `Package Completion Unproven` remains active when package completion is claimed green while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while other admitted package slices remain incomplete

Element Coverage standard:

- Element Coverage is a non-identity checklist owned by FAM/package analysis, Branch Readiness Stage 1, and PR Readiness Stage 1 review
- coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact
- Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers

Open backlog selection is priority-led:

- `Priority` is the primary selection signal for open candidate work
- `Target Version` must not be used to rank, select, defer, or skip open backlog candidates
- open `Registry-only` and active `Promoted` entries should not carry `Target Version`
- closed, released, implemented, or release-debt entries may keep `Target Version` as historical release evidence
- deferred open entries must state `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:` before they are eligible for next-workstream selection

Codex may:

- propose backlog changes
- draft exact backlog markdown for approval
- carry approved state changes during an explicitly authorized docs pass

Codex may not:

- silently add backlog items
- add, split, promote, package-admit, branch-create, select successor backlog identities, or waive the single-slice package blocker without explicit USER approval
- create or reuse parseable `FB-###` backlog IDs
- turn historical trace rows back into parseable backlog entries without explicit USER approval
- silently change priority or status outside approved work
- silently mark work complete because a branch merely looks clean

If Codex reaches the approval blocker, it must report `Backlog Addition User Approval Missing` and list every FAM that is still not closed plus every package or slice that is not complete.
If no still-not-closed entries exist, report `Backlog Exhaustion User Decision Pending` and stop for USER direction.

## Relationship To `Docs/orin_task_template.md`

`Docs/orin_task_template.md` remains the per-task execution scaffold.

This document defines repo-wide rules.
The task template defines the structure of a specific request.
