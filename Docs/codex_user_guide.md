# Codex User Guide

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**
**Release Readiness anchor and aggregation rules are owned by `Docs/phase_governance.md`. This guide gives operator examples, not a second source of release-window law.**

## Purpose

This document explains how to prompt Codex effectively inside Nexus Desktop AI work without sacrificing analysis depth, source-of-truth discipline, or validation quality.

It is an operator guide for prompt construction and collaboration posture.

It is downstream of:

- `Docs/development_rules.md`
- `Docs/Main.md`
- `Docs/phase_governance.md`
- `Docs/codex_modes.md`
- `Docs/user_test_summary_guidance.md`

If this guide conflicts with those files, those files win.

## Core Rule

Concise prompts are allowed.

Concise prompts do **not** mean:

- shallow analysis
- reduced source-of-truth reading
- premature scope compression
- automatic readiness, closure, merge, or release framing

Codex should still:

1. validate live repo truth
2. scan broadly enough to understand the affected system
3. map drift, risk, dependencies, and options
4. report clearly
5. narrow execution only after the user and ChatGPT choose scope

Automation prompts are subject to the same lane identity discipline. `Automation Observability` through `dev/automation_observability_report.py` reviews Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`, but only `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED` findings can become repair work. If a watcher or recurring automation talks about active branch, PR Readiness, Release Readiness, post-merge, release-window, selected-next, toolchain, or branch governance, it must name a configured cwd that resolves to the intended worktree and report branch/`HEAD`/`origin/main` proof; otherwise `Automation CWD Worktree Mismatch` blocks the finding. Background-observability-only automations are advisory, cannot clear PR watcher runtime proof, merge verification, or release-readiness gates, and stale historical toolchain-path reports remain `REVIEW_INFO` unless current source truth still owns the referenced path. USER-approved `automation/worktree governance intake` may use the `Standing Governance Intake Branch` only for non-runtime multi-worktree safety repair, and USER-approved `phase-gate governance intake` may use it only for repeatable non-runtime phase-gate miss prevention, with `RRI-YYYYMMDD-NNN`, `One Active Cycle`, `Sync Rule`, `Waiting For Governance Intake`, `Return Digest`, and `Neutral Main Workspace Rebaseline`.

## Default Prompt Posture

The default prompt posture is:

- one cue
- one anchor
- optional structured fields only when they materially improve anchor clarity

Use:

- `[cue]: [anchor]`

Examples:

- `Analyze and Report: best next workstream after current release`
- `Analyze for drift: post-release canon on updated main`
- `Workflow mode: execute the approved canon phase on current branch`
- `docs-only pass: align README to the merged source-of-truth model`
- `digest latest User Test Summary, reevaluate blockers and phase, then continue only if the next legal phase allows it`

The prompt may be concise.
Codex's investigation should still be complete enough for the task.

When ChatGPT is generating the prompt, planning-loop risk belongs in preflight analysis.
If preflight stays red, return analysis instead of thickening the prompt with control-language blocks.

## Required Phase Anchor

For phase-sensitive work, prompts should explicitly include:

- `Mode: <mode name>`
- `Phase: <exact phase name>`
- `Workstream: <workstream id or authority record>`
- `Branch: <branch name or No Active Branch>`

For governed closeout recovery, also include:

- `Branch Class: <branch class>`
- `Current active seam: <seam name>`
- `Validation Contract: <summary or authority reference>` when validation governance matters
- `Timeout Contract: <summary or authority reference>` when interactive/manual timing governance matters

For bounded multi-seam Workstream execution, also include:

- `Bounded State: <exact phase/stage, workspace, branch, write target, authority record, package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase>`
- `Bounded State User Waiver: <Granted with exact waiver fields / None>`
- `Current active seam: <seam name>`
- `Seam Sequence: <ordered seam list>` when the admitted sequence is already explicit in canon
- `Validation Contract: <summary or authority reference>` when validation governance matters
- `Slice Continuation Policy: <summary or authority reference>` when same-branch continuation or an approved backlog split matters
- `Backlog Completion State: <In Progress / Implemented Complete / Implemented Complete Except Future Dependency>` when Workstream continuation or phase exit matters
- `Remaining Implementable Work: <None / short summary>` when Workstream continuation or phase exit matters
- `Future-Dependent Blockers: <None / short summary>` when Workstream continuation or phase exit matters

For governed execution returns, request or supply these exact output markers:

- `Seam Status:`
- `Slice Status:`
- `Completion Status:`
- `Blockers:`
- `Waiver Status:`
- `Continue Decision:`
- `Continuation Execution Latch:`
- `Stop Basis:`

Use owning canon after load to derive the per-seam gate, entry seam, `Next-Seam Continuation Required`, the rule that a slice is a bounded admitted backlog-completion unit and a seam is the current execution checkpoint inside or between slices, the rule that seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress, the rule that there is no repo-wide cap on how many slices a branch or workstream may carry, same-branch backlog completion as a branch-level posture, backlog completion state, future-dependent blockers, `Backlog-Split User Approval`, `Backlog-Split Reason`, the rule that reporting `Next Safe Move` is not a substitute for execution while the current slice still requires seams, the rule that a continue decision must be acted on immediately by starting the next seam needed inside the current slice, the rule that when a slice turns green during `Workstream` Codex advances immediately to the next admitted slice while `Completion Status` remains `In Progress`, and the rule that `Workstream` reaches `Hardening` only when `Completion Status: Green`.
Bounded means one active seam at a time, not one-seam Workstream authority. A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.
If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.
Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.
A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.

If `Bounded State` is missing, stale, or ambiguous, Codex must stop on `Bounded State Missing` before mutation. Broad work requests do not authorize implementation: `continue`, `complete all`, `all remaining work`, `finish the branch`, or similar wording may execute only when source truth resolves it to one exact active bounded seam. Widening beyond that bounded state requires `Bounded State User Waiver: Granted`; without explicit USER waiver text naming the branch/worktree, phase, slice/seam, relaxed bound, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions, Codex must stop on `Bounded State Waiver Missing`. Clean validation, branch existence, prompt wording, Codex discretion, or ChatGPT wording cannot infer a bounded-state waiver.

A green seam does not authorize stop while `Slice Status` remains non-green.
A green slice does not authorize stop while `Completion Status` remains non-green.
A green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice.
If `Completion Status` is `In Progress` and no named blocker or waiver stops work, Codex must continue instead of returning `Await Next Instruction`.
Use these governed state markers as execution control, not just reporting.
If `Continue Decision` is `Continue`, Codex must not end on a seam-complete final response, rollback path, or next-seam recommendation; it must keep executing until a lawful `Stop` decision exists.
Treat a prompt `Return:` block as the lawful-stop report, not as permission to stop while `Continue Decision` remains `Continue`.
A prompt `Return:` block is an output shape only; it cannot override governed continuation markers or authorize a terminal response while `Continue Decision` remains `Continue`.
A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
`Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
`Phase: Workstream` must remain bounded at all times; the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
Phase Boundary Stop Required: A phase-exit seam named in `Next Active Seam` is a handoff target, not current-phase execution authority.
Bounded Workstream continuation ends at phase boundaries; it never crosses from Workstream into Hardening by inertia.
Codex must not execute Hardening, Live Validation, PR Readiness, Release Readiness, release work, or any other next phase in the same run unless USER explicitly admits that phase after reviewing the handoff.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
If `Completion Status` is `Red`, `Continuation Action` must report the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume.

For Release Readiness, also include:

- `Release Candidate Anchor: <current origin/main unless USER selects another release target>`
- `Release Candidate Anchor Source: <current origin/main / USER-selected historical commit / release branch>`
- `Target Commit: <candidate commit SHA>`
- `Historical Endpoint Handling: <audit evidence only unless USER-selected historical commit>`
- `Candidate Includes Later Governance Repairs: <YES/NO/N/A>`
- `Release Ownership Model: <aggregated release window / release packaging branch / USER-selected narrow target>`
- `Release Window Contributors: <included FAM/worktree contributors>`
- `Merged-Unreleased Scope Inventory: <included unreleased scopes>`
- `Last Runtime PR: <last runtime payload PR in the selected candidate>`
- `Post-Runtime Governance Repairs: <governance/source-truth-only PRs after the last runtime PR>`
- `FAM Contributor Routing: <owning lane for each contributor blocker>`
- `Release Target: <version or identifier>` for release-bearing branches
- `Release Floor: <patch prerelease / minor prerelease / no release>` for release-bearing branches
- `Version Rationale: <why the target follows the floor>` for release-bearing branches
- `Release Scope: <bounded release scope>` for release-bearing branches
- `Release Artifacts: <tag, notes, rebaseline, or other release artifacts>` for release-bearing branches
- `Release Branch: No` only for preserved historical records
- `No file changes` because Release Readiness is analysis-only for repository files
- `Protected Main: main is read-only for Codex work` when the task reads post-merge truth from `main`

## Thin Prompt Discipline

Planning-loop prevention belongs in ChatGPT preflight analysis, not in a thicker Codex prompt body.
If planning-loop risk, branch ambiguity, or runtime-free implementation drift remains unresolved, ChatGPT should block prompt generation and return analysis instead.

Once prompt generation is allowed, keep the Codex prompt thin and neutral.
Use project context, active seam, task, and return format to express scope positively.
Let repo truth, branch authority, canonical workstreams, and admitted slice records supply behavior after load rather than pasting full seam-governance rule blocks into the prompt text.

## What Codex Should Do Automatically

Brief prompts do not waive source-of-truth reading.

When the user gives a short cue such as:

- `Analyze and Report`
- `Analyze for drift`
- `Analysis mode`
- `Workflow mode`
- `docs-only pass`
- `continue on current branch`

Codex should still:

1. load `Docs/Main.md`
2. load `Docs/development_rules.md`
3. load `Docs/phase_governance.md`
4. load `Docs/codex_modes.md`
5. infer the directly relevant authority docs
6. pull the repo evidence needed to validate live truth
7. keep the same reasoning standard as a longer structured prompt

For meaningful interactive desktop hardening or closeout work, that baseline also includes:

- using `Docs/phase_governance.md` for the repo-wide validation helper contract and proof hierarchy
- using `Docs/validation_helper_registry.md` for durable helper naming, `Helper Status:`, owner, reuse, `Workstream-scoped` classification, `Consolidation Target`, and `Temporary probe` handling
- using `Docs/development_rules.md` for evidence, cleanup, and hardening expectations
- reusing existing live-validation helpers before creating new scripts, or recording why reuse is unsafe
- treating one-off live-validation probes as temporary ignored artifacts that must be deleted or promoted into documented reusable tooling before closeout-grade proof
- requiring visible helper progress and a no-progress supervisor; if no tighter helper-specific watchdog is active, `10s` without meaningful progress must abort the run, clean up, and report the last confirmed progress point
- applying the `User-Facing Shortcut Live Validation Gate` for relevant desktop user-facing Live Validation: declare `User-Facing Shortcut Path:`, record `User-Facing Shortcut Validation:`, and clear or waive `User-Facing Shortcut Validation Pending` before User Test Summary handoff
- applying the `Codex Live Client Self-QA Gate` for relevant desktop user-facing Live Validation: declare `Codex Live Client Self-QA:`, `Visual Quality:`, `Live Interaction Evidence:`, `Usability Check:`, and `Platform Uniformity Check:`, then clear or waive `Codex Live Client Self-QA Pending` before User Test Summary handoff
- applying `Codex Visual Adjudication:` for relevant desktop UI Live Validation: record `Visual Artifact Review Scope:`, `Product Vision Alignment:`, `Per-Element Visual Verdicts:`, `Helper Marker Limitation:`, `Unacceptable UI Findings:`, and `LV1 Handoff Disposition:` so helper PASS, marker PASS, screenshot existence, and manifest existence cannot replace artifact-by-artifact product-vision judgment
- for interactive user-facing UI, Codex must exercise the same live-client interactions it would ask the USER to test; screenshot-only, marker-only, or launched-but-not-driven proof cannot clear the self-QA gate
- for desktop UI, Codex must use an active foreground/user-observable client mode; hidden, too-fast, or blink-through helper evidence is supporting proof only
- planning the post-green live launched-process UI audit when meaningful user-facing desktop UI changed

## Codex Client Screenshot Delivery

When the user wants live screenshot proof to render inside the Codex client, use this as the default delivery path:

1. capture the screenshot from the real launched process and preserve the original file on disk as the durable audit artifact
2. for Live Validation visual proof, copy the raw screenshot into `C:\Users\anden\OneDrive\Pictures\Screenshots\<project-or-validation-lane>\<timestamp>\` or the active USER-declared screenshots folder so the USER-facing evidence is not buried only under `dev/logs`
3. keep the audit manifest, `dev/logs` capture path, and `screenshots` raw-image path in the evidence trail
4. surface the raw screenshot path in chat and attach/render that raw file when the client supports it, one image at a time
5. if raw local-file rendering fails or flashes, generate a smaller inline PNG preview from that same raw file and send the preview only as a convenience layer

Default assumptions:

- full virtual-desktop screenshots are the default for desktop Live Validation when window placement, multi-monitor behavior, window separation, clipping, or frame-of-reference matters
- the USER-declared screenshots folder raw file is the USER-inspectable evidence copy for Live Validation visual proof
- local-file Markdown image embeds may work in this client, but if they do not, use the smaller inline PNG fallback
- WebP should be treated as a fallback path rather than the default unless PNG has stopped working in the current client state
- the in-chat image is a preview convenience layer, not the durable evidence source
- the durable evidence remains the manifest plus the original captured files on disk

When writing a prompt that depends on in-chat screenshot review, say so explicitly:

- `Use live launched-process screenshots.`
- `Preserve original captures on disk, copy Live Validation proof into C:\Users\anden\OneDrive\Pictures\Screenshots or the active USER-declared screenshots folder, and record both paths in the audit manifest.`
- `Surface the raw screenshot path in chat; if rendering fails, use a small inline PNG preview generated from that raw file.`

If the task remains materially ambiguous after that baseline, Codex should ask one focused clarifying question rather than lowering the quality of analysis.

## Startup Contract For Every Task

Before planning or execution, Codex should follow the startup loading contract in `Docs/Main.md`, using `Docs/nexus_startup_contract.md` only as the ChatGPT/new-chat loader map when prompt generation is in scope.
Local ChatGPT custom instructions should stay compact; the repo loader/source-truth can hold longer ChatGPT-facing continuity rules, prompt-generation guardrails, and review memory.
Do not paste the loader doc into Codex prompts. Codex prompts should load `Docs/Main.md` and the owning canon for execution authority, using the loader only when prompt generation, new-chat bootstrapping, or loader/source-truth drift review is in scope.
ChatGPT loader/source-truth continuity must preserve FAM -> Package -> Slice -> Seam, PR evidence-only handling, legacy global FB historical-only handling, single-slice and package-completion blockers, Element Coverage as non-identity, Branch/PR Readiness Stage 1 / Stage 2, next-branch hierarchy review, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, post-release canon closure through the next approved Branch Readiness Stage 2 carrier, runtime package carrier when runtime work is next, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and the Windows-first, modular, GPU-aware product direction with optional heavy local AI capability packs and CPU fallback.

For tracked work, that means:

1. read `Docs/Main.md`
2. read `Docs/development_rules.md`
3. read `Docs/phase_governance.md`
4. read `Docs/codex_modes.md`
5. check `Docs/feature_backlog.md` for `Record State`
6. load the canonical workstream doc when the item is `Promoted` or `Closed`
7. if the task is a selected `Registry-only` backlog branch in `Branch Readiness`, or an approved non-backlog branch, load the branch authority record under `Docs/branch_records/`
8. validate current branch truth before trusting prompt framing
9. use the canonical workstream doc first for branch-local reuse, artifact history, and "what worked" notes, or use the branch authority record when no promoted workstream owns the branch
10. run `Source-Truth Placement Preflight` before creating a new governance/source-truth file, active artifact, ledger, registry, or durable authority surface
11. use the owning `Element Validation Ledger` in the canonical workstream doc or active branch authority record for created, touched, affected, deferred, future, dependency-only, and non-gating supporting product elements
12. record a Dev Toolkit Interface Review Mode disposition for USER-facing interface elements, including previous and future implementations: callable in dev-only review mode, deferred to a named repo-wide adoption branch/package, or not-applicable with reason
13. use `Docs/incident_patterns.md` only for generalized cross-branch patterns
14. run `Thread / Worktree Identity Preflight` before Stage 2, phase entry, branch/worktree creation, commit, push, PR work, release work, or GitHub Desktop handoff
15. state the next safe move before narrowing scope

`Thread / Worktree Identity Preflight` proves the current working directory, repository root, branch, upstream, `HEAD`, `origin/main`, `git worktree list`, clean/dirty state, workspace role, active thread owner, thread assignment status, worktree ownership ledger, intended write set, runtime/process ownership, and GitHub Desktop folder binding when relevant. If the thread is in the wrong folder or branch for the requested work, stop on `Thread / Worktree Identity Mismatch` instead of correcting by inertia. If another active thread owns the same worktree or branch, stop on `Parallel Worktree Coordination Missing`.

`Assigned Worktree Confinement` means a thread assigned to one worktree stays inside that worktree for repo mutation, branch/worktree actions, runtime launches, shortcut/provider/model changes, PR/release work, and GitHub Desktop handoff. The preflight must show `Active Thread Owner:`, `Thread Assignment Status:`, `Worktree Ownership Ledger:`, `Intended Write Set:`, `Same Worktree / Same Branch Collision Check:`, `Dirty Worktree Collision Check:`, `Dirty Worktree Recovery Packet:`, `Off-Worktree Work Routing:`, `Governance Routing Barrier:`, `New Worktree Decision Gate:`, `Expected Worktree Root:`, `Actual Worktree Root:`, `No Cross-Worktree Mutation:`, and `GitHub Desktop-bound worktree`. If the actual root is different, stop on `Worktree Escape User Waiver Missing`; only USER can grant `Worktree Escape User Waiver: Granted` with exact root, scope, expiration, validation, and return-path details. If the target worktree is dirty and ownership is unclear, freeze mutation and complete the dirty-worktree recovery packet before continuing. If the work belongs to another active lane or a not-yet-created worktree, route it to Governance instead of entering that worktree directly.

`Pre-Rebaseline Impact Audit` is required before any worktree, branch, neutral-main folder, or standing governance lane baselines itself to newer `origin/main`. No Baseline By Inertia: a clean tree, behind status, or fast-forward-only path is not enough. Report `Incoming Main Change Set:`, `Incoming Changed Files:`, `Current Worktree Changed Files:`, `Incoming Runtime / Source-Truth Risk:`, `Shared Surface / Worktree Overlap Forecast:`, `Validation Before Rebaseline:`, `Recommendation Only:`, `Rebaseline Mutation Approval:`, and `Rebaseline Mutation Status:` first, then wait for USER approval before merge/rebase/fast-forward/branch-switch mutation.

Promoted workstream docs remain the place to read branch-local feature state, evidence, active seams, artifact history, and branch-local reuse notes.
Repo-wide lifecycle rules such as phases, stop-loss, timeout governance, and proof authority come from `Docs/phase_governance.md`.
Repo-wide validation-helper rules and the desktop UI audit rule also come from `Docs/phase_governance.md`.
Element Validation Ledger rows belong in the existing authority owner by default: the canonical workstream doc for promoted work or the active branch authority record for `Registry-only` active branches. Do not prompt Codex to create a parallel active ledger unless the owning record records `No Existing Owner Fits` or points to a companion file.

Dev Toolkit Interface Review Mode is the repo-wide dev-only inspection standard for USER-facing elements after the review tooling is admitted. It should cover existing and future surfaces such as NCP, Core visualization, Dashboard, Overlay/display when admitted, and other user-facing windows/components. The mode uses element badges, hover highlighting, ledger ID/name tooltips, and screenshot-friendly annotations in Dev Toolkit/dev mode only; production UI must remain unbadged.

## Analysis-Phase Prompting

Use analysis-phase prompts when the user wants:

- current-truth validation
- drift review
- sequencing review
- next-move determination
- post-release or post-merge review
- source-of-truth audit
- lane or branch evaluation

Helpful cues:

- `Analyze and Report`
- `Analyze for drift`
- `Analysis mode`
- `analysis-to-plan pass`

Helpful add-ons:

- `analysis only`
- `digest latest User Test Summary before recommending the next legal phase`
- `if User Test Summary results are pending, report User Test Summary Results Pending as the final-green blocker`
- `use origin/main as authoritative truth`
- `do not patch`

Analysis-phase prompts should encourage:

- full-system reasoning first
- branch and release truth validation
- structural and authority drift mapping
- carry-forward / defer / discard classification of prior suggestions

They should **not** push Codex to behave like a narrowly bounded executor before the analysis is complete.

## Execution-Phase Prompting

Execution-phase prompts are for work the user has already approved.

Helpful cues:

- `Workflow mode`
- `docs-only pass`
- `execute the approved phase`
- `continue on current branch`

Useful execution add-ons:

- `do not widen scope`
- `self-validate before handoff`
- `use helper if needed`
- `no PR/release output`

Execution-phase discipline such as:

- bounded patching
- bounded multi-seam workflow
- minimal isolated change
- smallest coherent execution slice
- narrow fix pass

belongs here, after analysis and scope selection are already complete.

## Prompt Recipes

### Active-Branch Governance Or Canon Update

Use:

- `Workflow mode on current branch: docs-only governance or canon refinement`

Use this when:

- the active branch owns the affected truth
- the change is directly required to keep that branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct
- the prompt names the exact canonical phase and current branch class
- the update can stay docs-only and inside the active branch's approved scope, validation rules, and stop conditions

Do not use this recipe for unrelated governance cleanup, broad docs churn, product/runtime changes, or work that would contaminate or confuse the active implementation or release branch.

### Deep Analysis Of The Next Move

Use:

- `Analyze and Report: best next workstream after current branch`

Useful add-ons:

- `analysis only`
- `use origin/main as authoritative truth`

### Drift Review

Use:

- `Analyze for drift: current branch before merge`
- `Analyze for drift: post-release canon on updated main`

Best for:

- mixed-scope branches
- stale prompt assumptions
- source-of-truth mismatch
- release-dependent docs drift
- architecture or workflow drift

### Docs-Only Canon Repair

Use:

- `Branch Readiness Stage 1: classify post-release canon drift on updated main`

This is an analysis workflow.
Use it when merged canon is stale after publication and that drift could not be fully represented before release.
Classify the drift, record the legal carrier, and route the repair into the next approved Branch Readiness Stage 2 carrier before implementation begins.

This is not a planned `docs/governance` branch from `No Active Branch`.
Do not repair directly on `main`.
Use this recipe to classify escaped canon drift, then record it as a blocker for the next legitimate runtime-focused backlog branch's `Branch Readiness Stage 1` and repair it in Stage 2 before implementation.

### Governance Repair On The Active Branch

Use:

- `Analyze and Report: identify the Branch Readiness blocker and repair it on the active branch`

or:

- `Workflow mode: execute the docs-only governance repair on the active branch before implementation`

Use this only when:

- the repair is directly required to keep the active branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct
- a prior PR Readiness miss escaped and must be cleared in the next legitimate runtime-focused backlog branch's `Branch Readiness`
- the work can stay docs/governance-only without changing product/runtime behavior
- the prompt blocks implementation until the Branch Readiness blocker is cleared

Do not use a governance-only branch or between-branch canon repair lane for this work.
Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
The only standing exception is the `Standing Governance Intake Branch`, `feature/release-readiness-source-truth-intake`, at `C:\Nexus Worktrees\Governance`; it accepts a `Release Readiness digest`, USER-approved `automation/worktree governance intake`, or USER-approved `phase-gate governance intake` only, uses `RRI-YYYYMMDD-NNN`, enforces `One Active Cycle`, requires the clean pre-intake `Sync Rule`, pauses the originating lane in `Waiting For Governance Intake` or `Waiting For Updated Main`, and must send a post-merge `Return Digest` with exact originating branch, originating worktree, operating workspace, expected branch, and `Neutral Main Workspace Rebaseline:` proof copied from the accepted intake instead of inferred from `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Governance`, GitHub Desktop, or current shell CWD.
If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.

During `pre-Beta`, this path remains non-default and explicitly justified.
In later Beta, public, or steady-state repo operation, it may become a normal maintenance path.

### Continue An Approved Branch

Use:

- `continue on current branch: [approved remaining task]`
- `Workflow mode on current branch: [approved phase]`

Examples:

- `continue on current branch: finish the approved validator follow-through`
- `Workflow mode on current branch: execute Phase 2 of canon reconstruction`

### Bounded Multi-Seam Workstream Execution

Use:

- `Workflow mode on current branch: execute bounded multi-seam Workstream sequence`

Required add-ons:

- `Phase: Workstream`
- `Current active seam: [seam name]`
- `Seam Sequence: [ordered seam list]` when canon already defines the admitted sequence
- `Validation Contract: [summary or authority reference]`
- `Slice Continuation Policy: [same-branch completion / approved backlog split / authority reference]`

Use this when:

- the seams are in the same workstream, same phase, same branch class, same risk class, and same subsystem family or tightly coupled chain
- the operator wants Codex to keep moving through a coherent seam sequence without a new prompt after every seam
- per-seam validation and evidence recording remain mandatory

Keep the prompt body thin and let owning canon supply the detailed rules after load.
Use the prompt to name the active seam, validate after each seam, and report continue-or-stop.
Source-truth reminders that stay in canon rather than prompt body:

- Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
- Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
- Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
- Docs-only Workstreams require explicit USER approval.
- Planning-Loop Bypass User Approval: APPROVED
- Planning-Loop Bypass Reason:
- Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
- Do not create a `docs/governance`, `emergency canon repair`, or repair-only feature branch for future Nexus work.
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
- the prompt-named seam is the entry seam, not a terminal boundary
- Next-Seam Continuation Required means continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green
- seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress
- same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green
- when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
- `Workstream` reaches `Hardening` only when `Completion Status: Green`
- `Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; one green seam or one green slice cannot move the branch to Hardening while admitted branch material remains.
- `Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation
- stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition
- `Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item
- use `Backlog Completion State: In Progress`, `Implemented Complete`, or `Implemented Complete Except Future Dependency` to record whether more same-branch slices are still required
- reporting Next Safe Move is not a substitute for execution
- A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice.

High-risk categories such as bug fixes, hotfixes, unclear seams, cross-subsystem changes, settings, protocol, launcher, or UI-model work require smaller seams and stronger gates; they do not automatically cancel bounded multi-seam continuation after a green admitted seam.

When the sequence completes, the normal next phase is `Hardening`.
Do not prompt Codex to treat Workstream completion as direct `PR Readiness`.

### Release Readiness Target Gate

Use:

- `Analyze and Report on current branch: execute Release Readiness target validation without file changes`

Required add-ons for release-bearing branches:

- `Phase: Release Readiness`
- `Release Candidate Anchor: [current origin/main unless USER selects another release target]`
- `Release Candidate Anchor Source: [current origin/main / USER-selected historical commit / release branch]`
- `Target Commit: [candidate commit SHA]`
- `Historical Endpoint Handling: [audit evidence only unless USER-selected historical commit]`
- `Candidate Includes Later Governance Repairs: [YES / NO / N/A]`
- `Release Ownership Model: [aggregated release window / release packaging branch / USER-selected narrow target]`
- `Release Window Contributors: [included FAM/worktree contributors]`
- `Merged-Unreleased Scope Inventory: [included unreleased scopes]`
- `Last Runtime PR: [last runtime payload PR in the selected candidate]`
- `Post-Runtime Governance Repairs: [governance/source-truth-only PRs after the last runtime PR]`
- `FAM Contributor Routing: [owning lane for each contributor blocker]`
- `Release Target: [version or release identifier]`
- `Release Floor: [patch prerelease / minor prerelease / no release]`
- `Version Rationale: [why this is patch/minor/no release]`
- `Release Scope: [bounded release scope]`
- `Release Artifacts: [tag, notes, rebaseline, or other release artifacts]`
- `No file changes`

Required add-on for non-release branches:

- `Release Branch: No`

Use `Release Branch: No` only for preserved historical records.
Do not use `Release Branch: No` for `implementation` or `release packaging` branches.
If a release-bearing branch lacks `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, or `Release Artifacts:`, Release Readiness is blocked by `Release Target Undefined`.
If the declared target is semantically wrong for the latest public prerelease and declared release floor, it is also blocked by `Release Target Undefined`.
If Release Readiness lacks `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, or `Candidate Includes Later Governance Repairs:`, it is blocked by `Release Candidate Anchor Missing`.
If Release Readiness lacks `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, or `FAM Contributor Routing:`, it is blocked by `Release Window Contributor Inventory Missing`.
Unless USER explicitly selects a historical commit as the release target, current fetched `origin/main` is the release candidate anchor and historical PR merge commits are audit evidence only. Do not fail the current release candidate for stale wording that existed only at an older PR endpoint when later merged governance/source-truth PRs repaired the selected candidate.
Merge order does not decide release ownership. When multiple FAM/worktree branches merge before the next release, use `Release Ownership Model: Aggregated release window` and inventory every included merged-unreleased contributor; if one contributor is not release-ready, block or choose a USER-approved narrower target instead of silently excluding it.
`Release Window Contributor Inventory:` must be explicit before Release Readiness can report green.
Governance/source-truth-only PRs merged after the last runtime PR may be included in the release candidate. They do not force the release candidate back to the last runtime merge commit; record `Candidate Includes Later Governance Repairs: YES` and keep those repairs in internal validation/traceability instead of presenting them as user-facing product features when writing release notes.
If Release Readiness analysis discovers missing, stale, or ambiguous release truth that requires a file update, do not patch in Release Readiness. Return to `PR Readiness` before merge, or defer the repair to the next legitimate runtime-focused backlog branch's `Branch Readiness` or the standing governance intake lane after merge. Treat any file mutation while the authority record says `Release Readiness` as `Release Readiness File Mutation Attempt`.
If Release Readiness discovers stale/old branches, retired worktrees, or stale GitHub Desktop entries, output `Branch Cleanup Plan:` and `Branch Cleanup Execution Gate:` only. Do not delete branches, remove worktrees, switch branch targets, or clean up a GitHub Desktop-bound worktree in Release Readiness; execute cleanup only during `Branch Readiness Stage 2 - Execution Gate` after the replacement branch/worktree target is created or validated.
Release Readiness consumes inherited release truth only; it must not create `Release Candidate Anchor:`, `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, merged-unreleased owner, or post-release truth in repository files.

### Run A Narrow Fix Pass

Use:

- `Workflow mode: fix [bug] on current branch`

This recipe is for approved execution work.
It is not the default posture for system analysis.

Useful add-ons:

- `do not widen scope`
- `use helper if needed`
- `self-validate before handoff`

### Governed Closeout Recovery

Use:

- `Workflow mode: governed closeout recovery on current branch`

Use this bounded form when the user wants a stop-and-report recovery pass rather than a continuous run to full green.

Required add-ons:

- `Phase: Hardening`
- `Current active seam: [seam name]`
- `do not widen scope`
- `stop after the governed seam budget is exhausted`

### Continuous Validation To Full Green

Use:

- `Workflow mode: continuous governed validation to full green on current branch`

Required add-ons:

- `Phase: Hardening`
- `use the documented validation timeout profile`
- `reuse existing validation helpers first`
- `check Docs/validation_helper_registry.md before creating or keeping a helper`
- `do not widen scope`
- `do not stop between seam iterations unless blocker, truth drift, stop-loss, or required canon sync appears`
- `continue until the full gate is green or a hard stop is hit`

Helpful add-ons:

- `target no-progress 3s`
- `fallback maximum no-progress 10s when no tighter helper watchdog exists`
- `target transition 3s`
- `target normal seam 60s`

### Review A Returned User Test Summary

Use:

- `review latest User Test Summary to files-of-truth standards`

or:

- `digest latest User Test Summary to files-of-truth standards, reevaluate blockers and phase, and continue only if the next legal phase allows it`

If results have not been returned yet, the correct prompt/output posture is:

- automated validators and live helper evidence may be green
- if shortcut validation has not passed or been waived, `User-Facing Shortcut Validation Pending` remains the hard blocker before User Test Summary handoff
- relevant desktop workstreams must record `User-Facing Shortcut Path:` and `User-Facing Shortcut Validation:` before treating Live Validation as final green
- relevant desktop UI Live Validation must use the real user-facing desktop launcher declared for the UTS path when feasible; sandbox/offscreen/direct-runtime/WebView/helper launches are supporting evidence only and cannot replace that launcher gate
- relevant desktop UI Live Validation must create a per-element visual inventory and USER-inspectable focused screenshots under `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\<validation-lane>\<timestamp>\focused_element_screenshots\`; filenames must include the element label/name plus state/action, full-desktop screenshots are context only, and returned USER issue IDs must map to proof artifacts and visual verdicts
- relevant desktop UI Live Validation must not return a UTS handoff while Codex-visible `REPAIR` or `STOP` findings remain; Codex owns the pre-UTS defect-discovery burden and must either complete the bounded repair/rerun loop when approved or return `BLOCKED` / `REPAIR` with exact approval needed. UTS is USER acceptance review, not Codex defect discovery.
- returned USER UTS, screenshot, or video issues that block acceptance must remain in a temporary issue form until PR Readiness Stage 1 folds the resolved truth into durable source truth; the issue form must not be deleted while any issue lacks proof, disposition, or USER-verifiable status
- User Test Summary is exclusive to Live Validation Stage 1.
- `User Test Summary Results Pending` remains the hard blocker
- Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated
- PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact
- Live Validation green requires an exact `## User Test Summary` state before final green.
- Every Live Validation digest must include an exact `## User Test Summary` section; if User Test Summary is waived, the digest must still include `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`.
- `User Test Summary Results: PENDING.`
- `Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.`
- final phase advancement stays blocked until the filled User Test Summary is submitted or waived, digested into the active authority record, and blockers are reevaluated

### Ask For A Prompt

Use:

- `give me a prompt for ChatGPT to [task]`

Examples:

- `give me a prompt for ChatGPT to analyze post-release canon drift`
- `give me a prompt for ChatGPT to execute the approved docs-only phase`

## Fresh-Branch Rule

After a workstream is closed, released, merged, or otherwise no longer the right execution base, the next implementation workstream should start from updated `main` on a fresh branch.

Prompting should reflect that reality.

PR Readiness selects and minimally scopes the next real runtime workstream in canon only after explicit USER approval for successor selection exists, and it must also prove no successor branch exists yet at PR-package time.
Use machine-checkable markers after approval exists: `Next Workstream: Selected` and runtime `Minimal Scope:` in the backlog entry, plus `## Selected Next Workstream` and branch status such as `Branch: Not created` in the roadmap before the next branch opens or the active Branch Readiness branch name after it legally opens.
Selection must be priority-led: use open backlog `Priority` and deferred-context readiness, not `Target Version`, to choose the next candidate.
If the selected backlog item is deferred, it must already explain `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:` before PR Readiness can treat it as selectable.
If USER approval for a new or successor backlog identity, package admission, branch creation, backlog split, promotion, or single-slice package waiver is absent, `Backlog Addition User Approval Missing` remains active and Codex must output the still-not-closed FAM list plus every not-complete package and slice instead of adding selected-next truth.
If that list is empty, `Backlog Exhaustion User Decision Pending` remains active until USER direction.
If approval exists but no real runtime candidate can be selected, `Next Runtime Candidate Selection Pending` remains active and the branch stops in PR Readiness instead of advancing to Release Readiness.
Create the fresh branch only during the next `Branch Readiness` pass after the current branch merges and updated `main` is revalidated.
If that branch is created and a prior-branch canon miss is discovered, stay in `Branch Readiness`, repair the miss on the active branch, and do not start implementation until the blocker is cleared.

Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation.

Do not ask Codex to keep planning from an old lane branch when live repo truth shows that branch is stale, merged, or identical to `main`.
If repo truth is a steady-state `No Active Branch`, it is still not valid to invent the next real runtime candidate without explicit USER approval.
Do not ask Codex to work directly on `main`; `main` is protected and read-only for Codex work.
There is no emergency direct-main repair path for Codex.
For local Nexus work, `D:\Nexus Repos\Nexus Desktop AI Main` is the main/consolidator clone and `D:\Nexus Worktrees\` is the preferred active branch root. Old `C:\` Nexus folders are parked/fallback unless explicitly reactivated, and `C:\Nexus Desktop AI` on `codex/ai-llm-lab` is historical AI lab/planning context only.
Any tracked file mutation while Codex is on `main` is a `Main Write Attempt`.

## PR Readiness Green Output

`PR Readiness` uses two internal gates without changing the canonical phase enum.
`PR Readiness Stage 1 - Analysis Gate` is an analysis-first readiness-lock gate. It analyzes PR-readiness truth first, records `PR Readiness Stage 1 Repair Required` when bounded current-branch PR-readiness drift/blocker repair is needed, validates and commits/pushes those repairs only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair, and remains blocked by `PR Readiness Stage 1 Repair Pending` until repairs are durable. It still cannot create a PR, provision a watcher, create a branch, admit a package, waive single-slice rules, create a tag, create release artifacts, draft or publish a GitHub Release, or execute a release. It may encode selected-next truth only when USER explicitly approves that selected-next sync, and branch creation plus runtime package admission stay blocked for Branch Readiness.
This preserves the existing analysis-first blocker repair gate inside the readiness lock.
Stage 1 must return `## PR Readiness Stage 1 Analysis Packet` with the planned PR title/base/head/summary, required post-merge path, ranked runtime FAM candidates, recommended next package or explicit USER waiver, package-size / single-slice drift review, Element Coverage review, release-debt impact, release-debt handling status, selected-next / no-release-debt handling status, required current-branch source-truth sync, planned merge-target canon updates, a user-facing `## Next Workstream` block, planned next-branch block, planned watcher provisioning and reporting surface, `Pre-PR Live State:`, `PR Creation Approval:`, `Stage 2 PR Creation:`, `No Successor Runtime Branch By Inertia:`, `Selected-Next Defer User Waiver:`, `Post-Merge No Active Branch Projection:`, planned validations, expected file changes, Stage 2 sync plan, drift findings, blockers, waivers, release-window audit posture, rollback path, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed. Stage 1 selected-next/no-release-debt handling is complete only when the next selected branch/workstream is recorded in source truth before PR creation or an explicit USER waiver says no next branch/workstream is selected, release target/floor semantics and Release Window Audit are resolved when relevant, branch-authority cleanup is durable, stale-canon risk is cleared, and any unavoidable release debt has an explicit USER decision, named owner, and real-carrier plan before Stage 2; otherwise Stage 1 must stop on `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required` instead of reporting Stage 2-ready.
When Stage 1 has not yet created a PR, it may record `Pre-PR Live State: No live PR`, `PR Creation Approval: Pending USER approval`, and `Stage 2 PR Creation: Pending USER approval`; this is normal Stage 1 posture, not PR-ready green. For source-only, docs-only, governance, validator, or repo-wide support branches, Stage 1 may avoid selecting a runtime successor by inertia only when USER-approved waiver truth is recorded as `No Successor Runtime Branch By Inertia: USER-waived`, `Selected-Next Defer User Waiver: Granted`, and post-merge `No Active Branch` projection.
Stage 1 must also include `Origin/Main Freshness Check` before Stage 2. It records `Branch Creation Base:`, `Current origin/main:`, `Origin/Main Advanced Since Branch Creation:`, `Origin/Main Changed Files:`, `Branch Changed Files:`, `Reconciliation Required:`, `Reconciliation File List:`, `Reconciliation Recommendation:`, and `Reconciliation Mutation Status:`. If `origin/main` advanced after branch creation and files or source-truth owners need reconciliation, Stage 1 reports the complete data set and recommendation, stops on `Origin Main Reconciliation Packet Required`, and performs no file fixes during Stage 1.
The Stage 1 `## Next Workstream` block must include `Recommended Next Workstream:`, recommended family/package, candidate slices, `Candidate Work To Be Done:`, `User-Facing Output:`, why it is next, dependencies/blockers, validation needs, release impact, selection-truth status, branch-creation status, and `Next Workstream User Waiver:`.
Stage 1 has a hard no-continue gate: it cannot continue to Stage 2 unless the packet analyzes a concrete candidate and the work planned for that candidate, records approved selected-next truth, or records `Next Workstream User Waiver: Granted`; otherwise `Next Workstream User Waiver Missing` blocks continuation. If no legal next workstream candidate is found, Stage 1 must stop on `Next Workstream Candidate Not Found`, report the still-not-closed FAM list plus every not-complete package and slice, and record `Stage 1 USER Waiver Required` unless the USER grants a waiver/approval that clears the route.
Stage 1 must also include a no-work `## Next Branch Pre-Plan` section with `Next Branch Package Shape:`, proposed FAM/package, multiple concrete candidate slices, `Candidate Work To Be Done:`, `Single-Slice Drift Review:`, `Family Organization Review:`, `Element Coverage Review:`, dependencies/blockers, validation/live-test needs, branch creation status, and USER approvals required.
If the next branch cannot be shown as a broad FAM/package with multiple concrete candidate slices, `Next Branch Package Shape Unproven` blocks Stage 1 continuation; if the pre-plan looks like single-seam or single-slice drift, `Single-Slice Branch Drift Risk Unresolved` blocks; if the pre-plan drifts away from FAM -> Package -> Slice -> Seam or revives old live `FB-###` identity behavior, `Family Organization Drift Risk Unresolved` blocks. Any unresolved next-workstream or next-branch shape blocker must be classified as `Current-Branch Branch Readiness Re-entry Required` when the current branch remains the legal carrier, or `New Carrier Branch Required` when the current branch is stale, merged, invalid, or legally cannot own the blocker. The same fallback classification applies when the governance/source-of-truth ledger audit finds identity, FAM taxonomy, package/branch, USER approval, real-carrier, branch-authority, watcher/automation, release execution, Element Coverage, ChatGPT loader, project direction, current workflow, after-release workflow, or absolute-guardrail drift that cannot be cleared as bounded current-branch PR Stage 1 repair.
Stage 1 remains active until one outcome is recorded: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`.
`PR Readiness Execution User Approval Missing` remains active until `Stage 1 Ready For Stage 2` is recorded and explicit USER approval to enter Stage 2 is recorded.
`PR Readiness Stage 2 - Execution Gate` then performs final PR execution only: final PR package sync, commit/push if needed, PR creation, watcher provisioning, bot-review handling, mergeability validation, and merge-watch.
Stage 2 owns final PR execution only after the readiness-lock outcome is green.
PR creation is blocked while any Stage 1 blocker, Stage 1 repair item, next-workstream hierarchy item, branch-shape review item, or Stage 2 sync prerequisite remains unresolved.
Next-workstream/package hierarchy is reviewed in PR Readiness Stage 1, not selected in Branch Readiness by default. Branch Readiness fallback is real carrier branch/package analysis after the work direction has been identified; current-branch re-entry keeps the same legal carrier, while new-carrier fallback requires a new real carrier branch.

## Branch Readiness Review Gate

`Branch Readiness` also uses two internal gates without changing the canonical phase enum.
`Branch Readiness Stage 1 - Analysis Gate` is a no-work review pass: no repository file mutation, branch creation, package admission, docs sync, PR work, release work, selected-next truth, or canon edits.
Stage 1 must return `## Branch Readiness Stage 1 Analysis Packet` with governed state markers, FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, product vision, project-wide vision alignment, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable vs full-system boundary, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, rejected shallow plan, alternatives/tradeoffs reviewed, open USER decision points, deferred ideas/future-package ledger, validation plan, `Stale Branch Cleanup Plan:`, expected docs sync, blockers and waivers, rollback path, `Branch Readiness Planning Incomplete` blocker review, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed.
Stage 1 must also include `Carrier Lifecycle Decision` for the requested branch/worktree: `Carrier Lifecycle Classification:` must be exactly `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, or `Active remote/open PR branch`; the packet must include `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Stale Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`.
For broad implementation family packages, Stage 1 planning must be complete and USER-reviewable before Workstream, Hardening, Live Validation, or PR Readiness implementation begins or resumes. It must include non-empty, concrete product-system planning fields for `Project-Wide Vision Alignment:`, `Branch-Specific Vision Alignment:`, `System Concept Model:`, `Entity / Profile Model:`, `User Workflow Model:`, `Scale / Data Volume Model:`, `Configuration And State Model:`, `Expected User-Facing Outcomes:`, `Codex Additional Recommendations:`, `USER Critique Loop:`, `USER Decision Ledger:`, `Deferred Ideas / Future Package Ledger:`, `Planning Adequacy Review:`, `Rejected Shallow Plan:`, `Alternatives And Tradeoffs Reviewed:`, `Whole-System Interaction Map:`, `Minimum Viable vs Full System Boundary:`, and `Open Questions / USER Decision Points:` so a branch cannot ship a shallow/simple-system plan because Codex thought it was sufficient. When USER input is needed, the `USER Vision Question Packet` must explain each question with Codex recommendation, rationale, alternatives, tradeoffs/risks, current-branch impact, future-package impact, safe default, waiver/defer posture, and exact response format. When USER needs a durable editable handoff, Stage 2 may generate or refresh a USER-facing `User Vision Input.txt` desktop artifact with accept/change/defer answer paths, but that artifact is not repo source truth until a later USER-approved digest pass records completed answers. `Product Vision Input Missing`, `Project-Wide Vision Alignment Missing`, `Branch-Specific Vision Alignment Missing`, `USER Vision Question Packet Missing`, `USER Vision Recommendation Missing`, `USER Vision Questions Unanswered`, `USER Vision Input Pending`, `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, `System Concept Model Missing`, `Entity / Profile Model Missing`, `User Workflow Model Missing`, `Scale / Data Volume Model Missing`, `Configuration And State Model Missing`, `Expected User-Facing Outcomes Missing`, `Codex Additional Recommendations Missing`, `USER Critique Loop Missing`, `USER Decision Ledger Missing`, `Deferred Ideas / Future Package Ledger Missing`, `Planning Adequacy Review Missing`, `Rejected Shallow Plan Missing`, `Alternatives And Tradeoffs Missing`, `Whole-System Interaction Map Missing`, `Minimum Viable vs Full System Boundary Missing`, `Open Questions / USER Decision Points Missing`, `Branch Reach Unproven`, `Feature Element Breakdown Missing`, `Acceptance Criteria Missing`, `User-Facing Proof Standard Missing`, `Current Branch vs Future Package Boundary Missing`, and `Branch Readiness Planning Incomplete` are planning blockers that route the branch back to Branch Readiness until cleared or explicitly USER-waived.
For user-facing family/package branches, Stage 1 must also include an `Interface Release Boundary` review. The default is one primary user-facing interface release surface per branch, recorded as `Primary Interface Release Surface:` with fallback point, acceptance criteria, and proof path. Multiple released user-facing interfaces in one branch require explicit `Interface Bundle User Approval: Granted`; otherwise block on `Interface Release Boundary Missing`, `Primary Interface Undefined`, `Multiple Interface Release Drift`, `Fallback Point Missing`, `Interface Acceptance Missing`, or `Branch Readiness Interface Planning Incomplete`. This interface boundary does not authorize single-seam or single-slice Workstream behavior; bounded multi-seam/multi-slice execution remains expected inside the approved primary interface boundary.
Completed USER input digests can also keep package-specific planning blockers active, including legacy product-name drift, telemetry provider selection, polling floor, warning modality, external telemetry privacy model, cross-family audio approval, and persona/model switching scope. These are cleared by Branch Readiness revalidation, explicit deferral to future package scope, or explicit USER waiver. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.

Candidate-only planning is not enough for a broad family package. Current-branch scope, future-package deferrals, provider path, polling posture, warning modality, privacy model, naming/product-copy handling, acceptance criteria, and proof standards must be finalized in source truth and revalidated by Stage 1 before Workstream implementation resumes unless USER explicitly waives the requirement.
`Branch Readiness Execution User Approval Missing` remains active until explicit USER approval to enter Stage 2 is recorded.
`Branch Readiness Stage 2 - Execution Gate` then performs only the approved branch/package admission work, docs sync, branch creation, authority-record setup, and any approved stale/old branch cleanup after `Branch Cleanup Execution Gate:` proves the replacement branch/worktree target, `git worktree list`, branch targets, and GitHub Desktop-bound worktree binding are safe.

Element Coverage is a non-identity checklist owned by FAM/package review. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

When a `PR Readiness` pass is package-ready, green, or reports `PR READY: YES`, require a standardized `Next Branch` block and inclusion-only copy-ready `PR Creation Details` operator blocks.
This keeps successor-branch handling and PR creation instructions from being reinvented or omitted while keeping operator copy concise.
For Codex-created PRs, `PR Readiness GREEN` also requires the live PR to clear `Bot Review Signal Pending` through either a thumbs-up reaction or a bot comment from the Codex GitHub bot. A bot comment keeps `PR Validation Pending` active until the branch fixes the comment on the same PR, pushes, replies to and resolves the review thread, and records that current-head comment-resolution closeout; no later thumbs-up is required. This is the same-PR Codex bot-review repair loop. Stage 2 final handoff cannot be green until bot-review closeout is verified.
`PR Merge Status Unproven` also keeps PR Readiness non-green until the live PR explicitly reports a green merge status. Unknown, unset, conflicting, dirty, blocked, or otherwise non-green mergeability or merge-state results do not clear the gate. `Merge-Target Authority Projection Unproven` keeps PR Readiness non-green when post-merge truth will be `No Active Branch` without explicit USER waiver/defer, or when the PR would merge an active branch authority record, active PR Readiness phase, live/open PR wording, merge-watch ownership, or merge-verification blocker into `main`.
If the branch expects watcher-based PR monitoring, `PR Watcher Provisioning Unproven` also keeps the gate blocked until the watcher target, approved reporting surface, routing proof, runtime path, run-proof method, fallback, teardown rule, replacement provisioning for the live PR, and the live bot-review action contract are explicit and proven. Accepted watcher proof may come from native Codex heartbeat run evidence or from a bounded local watcher that posts status-change updates through the official Codex thread-resume path into the approved reporting-surface transcript and records delivery proof through assistant-message transcript presence, Codex thread-state refresh, and automation run/inbox visibility. Manual rollout-file or transcript-file injection does not count as proof. Watcher configuration is not runtime proof. Stage 2 final handoff cannot be green until watcher runtime proof is present or the runtime-proof blocker remains active.
`PR Watcher Routing Unverified` also keeps the gate blocked until the approved reporting surface is explicitly recorded and the configured thread/host target, state-file target, transcript target, and delivery proof have been cross-checked against it.
Standard operating procedure from now on is a watcher on an approved Codex reporting surface at minute cadence that reports only when a watched PR status changes. The current working thread is the default surface, but an explicitly recorded dedicated watcher-host thread is allowed when that is the validated user-visible route. That watcher contract must also say what happens next: thumbs-up reaction means report green for PR-entry validation; one or more actionable bot comments means trigger the bounded same-branch PR comment-repair worker, fix the issue, commit, push, reply, resolve the corresponding review thread, and then report `Comment addressed` / green for the current head.
Watcher status-change output must be source-of-truth shaped with governed state markers, live PR truth, watcher proof, blocker state, continue/stop decision, and, after `merged=true`, a copy/paste Codex prompt basis for the next legal Release Readiness validation. The watcher may clear merge-verification blockers but must not independently claim Release Readiness legality.
If final merge delivery proof is missing, the watcher must keep running and retry instead of retiring.
After live PR creation, live PR validation, merge-status green, and bot-review approval are complete, PR Readiness continues into a merge-watch seam and `PR Merge Verification Pending` stays active until that watcher on the approved reporting surface verifies that the PR is `merged`.
`Backlog Addition User Approval Missing` also keeps PR Readiness non-green when Codex would need to add, split, promote, package-admit, branch-create, waive a single-slice package, or select a backlog identity without explicit USER approval; its output is the still-not-closed FAM list plus every not-complete package and slice.

Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript. If missing proof blocks a release and the branch has not merged, return to PR Readiness; if the branch has already merged, carry it on the next real runtime package carrier's Branch Readiness before implementation begins.

For single-slice drift hardening, only slice rows with `Admission State: Admitted` count toward package admission. Historical evidence rows, merged evidence rows, future placeholders, deferred ideas, and future-package-required rows keep traceability but do not satisfy the multi-slice rule.
`Backlog Exhaustion User Decision Pending` keeps PR Readiness non-green when that still-not-closed list is empty and USER direction is required.
`Next Runtime Candidate Selection Pending` also keeps PR Readiness non-green after approval exists until exactly one real runtime Feature Family candidate is selected, canon-defined, minimally scoped as a runtime slice, mirrored in roadmap `## Selected Next Workstream`, and explicitly not branched yet.
`Automation Runtime Unproven` also keeps PR Readiness non-green for any phase-critical automation gate. A card, config file, or automation list showing `ACTIVE` is configuration state, not run proof. Accept run evidence only from thread or inbox output, automation memory/log/state-file updates, or scheduler last-run evidence. If the preferred Codex automation remains `ACTIVE` without run evidence, keep the owning phase blocked until run evidence exists or a bounded fallback is activated. Any bounded fallback must be target-scoped, phase-scoped, read-only, and self-terminating or explicitly deleted when its terminal condition or phase exit occurs.
Use `dev/automation_observability_report.py` when you need the current automation health picture. This clears or confirms Automation Observability Review Pending by reading Codex automation run/inbox rows plus `$CODEX_HOME/automations/*/memory.md`; `BLOCKER_CANDIDATE` and `REVIEW_REQUIRED` findings are bounded repair candidates, while `REVIEW_INFO` is informational unless it contradicts repo truth. If an automation is background-observability-only, do not treat its `ACTIVE` card, stale memory, or historical toolchain-path report as green proof for a live PR or release gate.

Required `Next Branch` block:

```markdown
## Next Branch
- Next Legal Branch Type:
- Next Branch Name:
- Branch Class:
- Creation Status:
- Creation Gate:
- Selected Next Workstream:
- Selected Next Implementation Branch:
- May Create Now: YES / NO
- Reason:
```

Required `PR Creation Details` operator blocks:

````markdown
## PR Creation Details
### PR Title
```text
<title only>
```

### Base Branch
```text
<base branch only>
```

### Head Branch
```text
<head branch only>
```

### PR Summary
```markdown
## Summary

<concise branch outcome and purpose>

## Branch Evidence

<concrete implemented work, source-truth changes, behavior/capability changes, historical context, branch-specific boundaries when useful, and evidence only; do not repeat the Summary>

## Validation

<validation commands, evidence paths, or "Validation was not recorded in the original PR body.">
```
````

The `Next Branch` block must state whether branch creation is legal now.
When release debt or updated-`main` revalidation blocks the selected next implementation branch, use `May Create Now: NO` and record the gate.
The PR operator blocks should be markdown-friendly and copy-ready, but they must not create the PR, merge the branch, run release work, or create the next branch by themselves.
The PR summary/GitHub PR body uses exactly three top-level sections: `## Summary`, `## Branch Evidence`, and `## Validation`.
`## Summary` must be one concise outcome paragraph, and `## Branch Evidence` must not repeat the Summary through nested `### Summary`, `### Purpose`, or `### Overview` sections.
Use concrete Branch Evidence subheads such as `### Changes`, `### Context`, `### Source Truth`, or `### Boundaries` only when they improve scanability.
The PR summary must report implemented branch truth only. Generic exclusion dumps, `Not Included` sections, and defensive scope language remain prohibited; concise branch-specific boundaries are allowed inside `## Branch Evidence` when they clarify reliable branch truth.
`## Validation` must contain validation commands, proof paths, or the historical no-validation sentence only.
GitHub PR bodies and PR Summary copy must not include phase-digest or Codex operator handoff fields such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, `Stop Basis`, `Exact next USER decision`, `Implemented, validated`, or `::git-*`; those belong in governed Codex/source-truth output, not branch evidence copy.

## Release Readiness Green Output

When a `Release Readiness` pass is green for release execution, require inclusion-only copy-ready `Release Package Details` operator blocks.

Required `Release Package Details` operator blocks:

````markdown
## Release Package Details
### Release Title
```text
<release title only>
```

### Release Tag
```text
<tag only>
```

### Target Commit
```text
<commit sha only>
```

### Release Notes
```markdown
<detailed user-facing release notes>
```
````

Release notes should clearly explain what was built, what capabilities exist, and how the system behaves.
Release notes must report included release work only and must not include exclusion lists, `Not Included` sections, negative scope framing, or defensive wording.
Release notes must use the standard Markdown release body shape: `## Release Summary` or `## Release Overview`, one or more detailed user-facing sections such as `## Release Highlights`, `## Validation`, or release-specific rich sections before generated notes, GitHub-generated `## What's Changed`, and the generated `**Full Changelog**:` compare link to the previous release.
The live GitHub release body must not start with or repeat the release title as `# <release title>`; the release title belongs in GitHub release metadata and the separate `Release Title` operator block only.
During Release Execution, use GitHub-generated release notes through the GitHub release notes button or generated-release-notes API so the `## What's Changed` section and previous-release compare link are populated by GitHub.

## When To Use A Longer Prompt

Use a longer structured prompt when:

- the branch or release state may be stale
- the task spans multiple authority layers
- the work could affect canon, governance, routing, backlog, or roadmap behavior
- the exact approved execution boundary matters
- validation expectations are unusually specific

Use a shorter prompt when the task is already well anchored and the current thread or canon makes the target obvious.

The key distinction is prompt length, not analysis depth.

## Best Operator Habits

- use one cue plus one anchor by default
- prefer ChatGPT preflight analysis over control-language blocks; if risk stays red, return analysis instead of thickening the prompt
- use `Analyze for drift` before merge, release, or major canon carry-forward decisions
- use evidence-digestion language when returned validation evidence should control the next move, rather than implying that phase advancement is automatic
- in `PR Readiness`, require Stage 1 to record `PR Readiness Stage 1 Repair Required` for bounded current-branch PR-readiness drift/blockers and keep `PR Readiness Stage 1 Repair Pending` active until those repairs are validated, committed, and pushed under a USER-approved legal current-branch repair seam. Stage 1 then stops on `PR Readiness Execution User Approval Missing` until USER approval to enter Stage 2 exists, and the Stage 1 packet must include next-branch hierarchy, required post-merge path, ranked runtime FAM candidates, recommended next package, package-size / single-slice drift review, release-debt impact, selected-next / no-release-debt handling status, Stage 1 repairs made, Stage 1 repair validation, `Governance Ledger Fallback:`, `Branch Readiness Fallback:`, and Stage 2 sync plan before accepting Stage 2 approval; if next-workstream, next-branch, no-release-debt, or governance-ledger blockers cannot be cleared without USER waiver/approval or Branch Readiness carrier analysis, classify the route as `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required` instead of Stage 2. Then require hard blocker checks before accepting `PR READY: YES`: `stale-canon`, `post-merge`, `next-workstream`, `dirty`, `docs-sync`, `desktop-shortcut`, `uts-results`, `Backlog Addition User Approval Missing`, `Backlog Exhaustion User Decision Pending`, `Single-Slice Package User Approval Missing`, `Package Completion Unproven`, `Next Runtime Candidate Selection Pending`, `PR Readiness Scope Missed`, `Release Window Audit Incomplete`, `Between-Branch Canon Repair Attempt`, `Next Branch Created Too Early`, `Merge-Target Authority Projection Unproven` until active branch authority is merge-stable and any post-merge `No Active Branch` truth has explicit USER waiver/defer, `PR Merge Status Unproven` until the live PR reports a green merge status, `PR Watcher Provisioning Unproven` until the watcher contract is explicit and proven, `PR Watcher Routing Unverified` until the configured watcher route and delivery proof are proven to match the recorded reporting surface, `PR Merge Verification Pending` until that watcher verifies the live PR is merged, and `Bot Review Signal Pending` for the live PR until a thumbs-up reaction or bot comment-resolution closeout exists
- in `Branch Readiness`, require Stage 1 to stop on `Branch Readiness Execution User Approval Missing` until USER approval to enter Stage 2 exists; the Stage 1 packet must include FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, validation plan, `Stale Branch Cleanup Plan:`, expected docs sync, and USER approval blocker before any branch/package admission work begins
- when the branch is inside an unreleased release window, require a `Release Window Audit` and treat serial blocker-clearing PRs as a failure by default; the green posture is `Remaining Known Release Blockers: None`, `Another Pre-Release Repair PR Required: NO`, and `Release Window Split Waiver: None` unless the user explicitly approves a split waiver
- in `PR Readiness`, require the standardized `## Next Branch` block and, when package-ready or green, the copy-ready `## PR Creation Details` operator blocks
- before `PR Readiness`, apply the Pre-PR Durability Rule: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state; only a documented `Durability Waiver`, failed validation, legally file-frozen `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push, and self-imposed blockers must automatically commit and push once lifted
- if a stale-canon or governance-drift class is discovered, the same branch or next legal repair surface must patch the canon or validator rule that allowed it before the repair is considered complete
- escaped drift prevention proof is mandatory: every repair for a miss discovered after the phase that should have caught it must include source-truth, governance, validator, helper, or prompt-contract hardening that prevents the same class from passing again, or must record why the gap is not machine-checkable yet and what human review marker replaces it before green
- merge-stable current-state owners such as backlog and roadmap must not mirror transient repair-branch ownership while merged-main truth remains `No Active Branch`
- route through `Docs/Main.md` whenever authority is unclear
- treat local unmerged overlays as reference material until revalidated against updated `origin/main`
- treat `main` as protected/read-only for Codex work; any required repository file mutation must move to a legal branch surface

## What This Guide Does Not Do

This guide does not make vague prompts universally safe.

It also does not remove:

- user approval requirements
- backlog control
- scope control
- validation requirements
- branch and release truth checks

The goal is lower prompt overhead with the same analytical rigor, not lower rigor with shorter prompts.
