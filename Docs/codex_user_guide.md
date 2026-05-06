# Codex User Guide

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**

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
- `Stop Basis:`

Use owning canon after load to derive the per-seam gate, entry seam, `Next-Seam Continuation Required`, the rule that a slice is a bounded admitted backlog-completion unit and a seam is the current execution checkpoint inside or between slices, the rule that seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress, the rule that there is no repo-wide cap on how many slices a branch or workstream may carry, same-branch backlog completion as a branch-level posture, backlog completion state, future-dependent blockers, `Backlog-Split User Approval`, `Backlog-Split Reason`, the rule that reporting `Next Safe Move` is not a substitute for execution while the current slice still requires seams, the rule that a continue decision must be acted on immediately by starting the next seam needed inside the current slice, the rule that when a slice turns green during `Workstream` Codex advances immediately to the next admitted slice while `Completion Status` remains `In Progress`, and the rule that `Workstream` reaches `Hardening` only when `Completion Status: Green`.
Bounded means one active seam at a time, not one-seam Workstream authority. A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.

A green seam does not authorize stop while `Slice Status` remains non-green.
A green slice does not authorize stop while `Completion Status` remains non-green.
If `Completion Status` is `In Progress` and no named blocker or waiver stops work, Codex must continue instead of returning `Await Next Instruction`.
Use these governed state markers as execution control, not just reporting.
If `Continue Decision` is `Continue`, Codex must not end on a seam-complete final response, rollback path, or next-seam recommendation; it must keep executing until a lawful `Stop` decision exists.
Treat a prompt `Return:` block as the lawful-stop report, not as permission to stop while `Continue Decision` remains `Continue`.
`Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
`Phase: Workstream` must remain bounded at all times; the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
If `Completion Status` is `Red`, `Continuation Action` must report the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume.

For Release Readiness, also include:

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
- planning the post-green live launched-process UI audit when meaningful user-facing desktop UI changed

## Codex Client Screenshot Delivery

When the user wants live screenshot proof to render inside the Codex client, use this as the default delivery path:

1. capture the screenshot from the real launched process and preserve the original file on disk as the durable audit artifact
2. keep the audit manifest and the original capture paths in the evidence trail
3. if in-chat visual confirmation is needed, default to a small inline PNG `data:` image generated from that real file rather than a local-file Markdown image
4. send one image at a time until the user confirms the client is rendering it reliably
5. if the first inline image fails or flashes, reduce the payload further before trying again

Default assumptions:

- local-file Markdown image embeds are not the reliable default for this client
- smaller inline PNG payloads are the proven default for this client state
- WebP should be treated as a fallback path rather than the default unless PNG has stopped working in the current client state
- the in-chat image is a preview convenience layer, not the durable evidence source
- the durable evidence remains the manifest plus the original captured files on disk

When writing a prompt that depends on in-chat screenshot review, say so explicitly:

- `Use live launched-process screenshots.`
- `Preserve original captures on disk and in the audit manifest.`
- `For in-chat image proof, use a small inline PNG data image one at a time until rendering is confirmed.`

If the task remains materially ambiguous after that baseline, Codex should ask one focused clarifying question rather than lowering the quality of analysis.

## Startup Contract For Every Task

Before planning or execution, Codex should follow the startup loading contract in `Docs/Main.md`, using `Docs/nexus_startup_contract.md` only as the ChatGPT/new-chat loader map when prompt generation is in scope.
Local ChatGPT custom instructions should stay compact; the repo loader/source-truth can hold longer ChatGPT-facing continuity rules, prompt-generation guardrails, and review memory.
Do not paste the loader doc into Codex prompts. Codex prompts should load `Docs/Main.md` and the owning canon for execution authority, using the loader only when prompt generation, new-chat bootstrapping, or loader/source-truth drift review is in scope.
ChatGPT loader/source-truth continuity must preserve FAM -> Package -> Slice -> Seam, PR evidence-only handling, legacy global FB historical-only handling, single-slice and package-completion blockers, Element Coverage as non-identity, Branch/PR Readiness Stage 1 / Stage 2, next-branch hierarchy review, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, release-support carrier when release is blocked, runtime package carrier when runtime work is next, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and the Windows-first, modular, GPU-aware product direction with optional heavy local AI capability packs and CPU fallback.

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
10. use `Docs/incident_patterns.md` only for generalized cross-branch patterns
11. state the next safe move before narrowing scope

Promoted workstream docs remain the place to read branch-local feature state, evidence, active seams, artifact history, and branch-local reuse notes.
Repo-wide lifecycle rules such as phases, stop-loss, timeout governance, and proof authority come from `Docs/phase_governance.md`.
Repo-wide validation-helper rules and the desktop UI audit rule also come from `Docs/phase_governance.md`.

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

- `docs-only pass: emergency repair for post-release canon drift on updated main`

This is an emergency-only analysis workflow.
Use it only when merged canon is already stale and that drift could not be prevented before merge or release.
If a plausible next implementation workstream can be selected safely from current truth, do not treat this as the default path.
If that docs pass changes validation or harness behavior assumptions, canon must be updated before further execution is recommended.

This is not a planned `docs/governance` branch from `No Active Branch`.
Do not repair directly on `main`.
Use this recipe to classify escaped canon drift, then record it as a blocker for the next legitimate runtime-focused backlog branch's `Branch Readiness` before implementation.

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
If Release Readiness analysis discovers missing, stale, or ambiguous release truth that requires a file update, do not patch in Release Readiness. Return to `PR Readiness` before merge, or defer the repair to the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge. Treat any file mutation while the authority record says `Release Readiness` as `Release Readiness File Mutation Attempt`.
Release Readiness consumes inherited release truth only; it must not create `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, merged-unreleased owner, or post-release truth in repository files.

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
- `User Test Summary Results Pending` remains the hard blocker
- Live Validation green requires an exact `## User Test Summary` state before final green.
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

Do not ask Codex to keep planning from an old lane branch when live repo truth shows that branch is stale, merged, or identical to `main`.
If repo truth is a steady-state `No Active Branch`, it is still not valid to invent the next real runtime candidate without explicit USER approval.
Do not ask Codex to work directly on `main`; `main` is protected and read-only for Codex work.
There is no emergency direct-main repair path for Codex.
Any tracked file mutation while Codex is on `main` is a `Main Write Attempt`.

## PR Readiness Green Output

`PR Readiness` uses two internal gates without changing the canonical phase enum.
`PR Readiness Stage 1 - Analysis Gate` is an analysis-first readiness-lock gate. It analyzes PR-readiness truth first, records `PR Readiness Stage 1 Repair Required` when bounded current-branch PR-readiness drift/blocker repair is needed, validates and commits/pushes those repairs only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair, and remains blocked by `PR Readiness Stage 1 Repair Pending` until repairs are durable. It still cannot create a PR, provision a watcher, create a branch, admit a package, waive single-slice rules, create a tag, create release artifacts, draft or publish a GitHub Release, or execute a release. It may encode selected-next truth only when USER explicitly approves that selected-next sync, and branch creation plus runtime package admission stay blocked for Branch Readiness.
This preserves the existing analysis-first blocker repair gate inside the readiness lock.
Stage 1 must return `## PR Readiness Stage 1 Analysis Packet` with the planned PR title/base/head/summary, required post-merge path, ranked runtime FAM candidates, recommended next package or explicit USER waiver, package-size / single-slice drift review, Element Coverage review, release-debt impact, required current-branch source-truth sync, planned merge-target canon updates, a user-facing `## Next Workstream` block, planned next-branch block, planned watcher provisioning and reporting surface, planned validations, expected file changes, Stage 2 sync plan, drift findings, blockers, waivers, release-window audit posture, rollback path, and the exact Stage 2 green-light decision needed.
The Stage 1 `## Next Workstream` block must include `Recommended Next Workstream:`, recommended family/package, candidate slices, `Candidate Work To Be Done:`, `User-Facing Output:`, why it is next, dependencies/blockers, validation needs, release impact, selection-truth status, branch-creation status, and `Next Workstream User Waiver:`.
Stage 1 has a hard no-continue gate: it cannot continue to Stage 2 unless the packet analyzes a concrete candidate and the work planned for that candidate, or records `Next Workstream User Waiver: Granted`; otherwise `Next Workstream User Waiver Missing` blocks continuation. If no legal next workstream candidate is found, Stage 1 must stop on `Next Workstream Candidate Not Found`, report the still-not-closed FAM list plus every not-complete package and slice, and record `Stage 1 USER Waiver Required` unless the USER grants a waiver/approval that clears the route.
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
Stage 1 must return `## Branch Readiness Stage 1 Analysis Packet` with governed state markers, FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, product vision, affected surfaces, acceptance criteria, USER vision questions, validation plan, expected docs sync, blockers and waivers, rollback path, and the exact Stage 2 green-light decision needed.
`Branch Readiness Execution User Approval Missing` remains active until explicit USER approval to enter Stage 2 is recorded.
`Branch Readiness Stage 2 - Execution Gate` then performs only the approved branch/package admission work, docs sync, branch creation, and authority-record setup.

Element Coverage is a non-identity checklist owned by FAM/package review. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

When a `PR Readiness` pass is package-ready, green, or reports `PR READY: YES`, require a standardized `Next Branch` block and inclusion-only copy-ready `PR Creation Details` operator blocks.
This keeps successor-branch handling and PR creation instructions from being reinvented or omitted while keeping operator copy concise.
For Codex-created PRs, `PR Readiness GREEN` also requires the live PR to clear `Bot Review Signal Pending` through either a thumbs-up reaction or a bot comment from the Codex GitHub bot. A bot comment keeps `PR Validation Pending` active until the branch fixes the comment on the same PR, pushes, replies to and resolves the review thread, and records that current-head comment-resolution closeout; no later thumbs-up is required. This is the same-PR Codex bot-review repair loop. Stage 2 final handoff cannot be green until bot-review closeout is verified.
`PR Merge Status Unproven` also keeps PR Readiness non-green until the live PR explicitly reports a green merge status. Unknown, unset, conflicting, dirty, blocked, or otherwise non-green mergeability or merge-state results do not clear the gate. `Merge-Target Authority Projection Unproven` keeps PR Readiness non-green when post-merge truth will be `No Active Branch` but the PR would merge an active branch authority record, active PR Readiness phase, live/open PR wording, merge-watch ownership, or merge-verification blocker into `main`.
If the branch expects watcher-based PR monitoring, `PR Watcher Provisioning Unproven` also keeps the gate blocked until the watcher target, approved reporting surface, routing proof, runtime path, run-proof method, fallback, teardown rule, replacement provisioning for the live PR, and the live bot-review action contract are explicit and proven. Accepted watcher proof may come from native Codex heartbeat run evidence or from a bounded local watcher that posts status-change updates through the official Codex thread-resume path into the approved reporting-surface transcript and records delivery proof through assistant-message transcript presence, Codex thread-state refresh, and automation run/inbox visibility. Manual rollout-file or transcript-file injection does not count as proof. Watcher configuration is not runtime proof. Stage 2 final handoff cannot be green until watcher runtime proof is present or the runtime-proof blocker remains active.
`PR Watcher Routing Unverified` also keeps the gate blocked until the approved reporting surface is explicitly recorded and the configured thread/host target, state-file target, transcript target, and delivery proof have been cross-checked against it.
Standard operating procedure from now on is a watcher on an approved Codex reporting surface at minute cadence that reports only when a watched PR status changes. The current working thread is the default surface, but an explicitly recorded dedicated watcher-host thread is allowed when that is the validated user-visible route. That watcher contract must also say what happens next: thumbs-up reaction means report green for PR-entry validation; one or more actionable bot comments means trigger the bounded same-branch PR comment-repair worker, fix the issue, commit, push, reply, resolve the corresponding review thread, and then report `Comment addressed` / green for the current head.
Watcher status-change output must be source-of-truth shaped with governed state markers, live PR truth, watcher proof, blocker state, continue/stop decision, and, after `merged=true`, a copy/paste Codex prompt basis for the next legal Release Readiness validation. The watcher may clear merge-verification blockers but must not independently claim Release Readiness legality.
If final merge delivery proof is missing, the watcher must keep running and retry instead of retiring.
After live PR creation, live PR validation, merge-status green, and bot-review approval are complete, PR Readiness continues into a merge-watch seam and `PR Merge Verification Pending` stays active until that watcher on the approved reporting surface verifies that the PR is `merged`.
`Backlog Addition User Approval Missing` also keeps PR Readiness non-green when Codex would need to add, split, promote, package-admit, branch-create, waive a single-slice package, or select a backlog identity without explicit USER approval; its output is the still-not-closed FAM list plus every not-complete package and slice.

Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript. If missing proof blocks a release, carry it on a real release-support carrier; if product work is next, carry it on the next real runtime package carrier.

For single-slice drift hardening, only slice rows with `Admission State: Admitted` count toward package admission. Historical evidence rows, merged evidence rows, future placeholders, deferred ideas, and future-package-required rows keep traceability but do not satisfy the multi-slice rule.
`Backlog Exhaustion User Decision Pending` keeps PR Readiness non-green when that still-not-closed list is empty and USER direction is required.
`Next Runtime Candidate Selection Pending` also keeps PR Readiness non-green after approval exists until exactly one real runtime Feature Family candidate is selected, canon-defined, minimally scoped as a runtime slice, mirrored in roadmap `## Selected Next Workstream`, and explicitly not branched yet.
`Automation Runtime Unproven` also keeps PR Readiness non-green for any phase-critical automation gate. A card, config file, or automation list showing `ACTIVE` is configuration state, not run proof. Accept run evidence only from thread or inbox output, automation memory/log/state-file updates, or scheduler last-run evidence. If the preferred Codex automation remains `ACTIVE` without run evidence, keep the owning phase blocked until run evidence exists or a bounded fallback is activated. Any bounded fallback must be target-scoped, phase-scoped, read-only, and self-terminating or explicitly deleted when its terminal condition or phase exit occurs.
Use `dev/automation_observability_report.py` when you need the current automation health picture. This clears or confirms Automation Observability Review Pending by reading Codex automation run/inbox rows plus `$CODEX_HOME/automations/*/memory.md`; `BLOCKER_CANDIDATE` and `REVIEW_REQUIRED` findings are bounded repair candidates, while `REVIEW_INFO` is informational unless it contradicts repo truth.

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
<implemented work only>
```
````

The `Next Branch` block must state whether branch creation is legal now.
When release debt or updated-`main` revalidation blocks the selected next implementation branch, use `May Create Now: NO` and record the gate.
The PR operator blocks should be markdown-friendly and copy-ready, but they must not create the PR, merge the branch, run release work, or create the next branch by themselves.
The PR summary must report implemented branch truth only and must not include exclusion lists, `Not Included` sections, or defensive scope language.

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
Release notes must use the standard Markdown release body shape: `## Release Summary` or `## Release Overview`, `## Release Highlights` or release-specific rich sections, GitHub-generated `## What's Changed`, and the generated `**Full Changelog**:` compare link to the previous release.
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
- in `PR Readiness`, require Stage 1 to record `PR Readiness Stage 1 Repair Required` for bounded current-branch PR-readiness drift/blockers and keep `PR Readiness Stage 1 Repair Pending` active until those repairs are validated, committed, and pushed under a USER-approved legal current-branch repair seam. Stage 1 then stops on `PR Readiness Execution User Approval Missing` until USER approval to enter Stage 2 exists, and the Stage 1 packet must include next-branch hierarchy, required post-merge path, ranked runtime FAM candidates, recommended next package, package-size / single-slice drift review, release-debt impact, Stage 1 repairs made, Stage 1 repair validation, `Governance Ledger Fallback:`, `Branch Readiness Fallback:`, and Stage 2 sync plan before accepting Stage 2 approval; if next-workstream, next-branch, or governance-ledger blockers cannot be cleared without USER waiver/approval or Branch Readiness carrier analysis, classify the route as `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required` instead of Stage 2. Then require hard blocker checks before accepting `PR READY: YES`: `stale-canon`, `post-merge`, `next-workstream`, `dirty`, `docs-sync`, `desktop-shortcut`, `uts-results`, `Backlog Addition User Approval Missing`, `Backlog Exhaustion User Decision Pending`, `Single-Slice Package User Approval Missing`, `Package Completion Unproven`, `Next Runtime Candidate Selection Pending`, `PR Readiness Scope Missed`, `Release Window Audit Incomplete`, `Between-Branch Canon Repair Attempt`, `Next Branch Created Too Early`, `Merge-Target Authority Projection Unproven` until active branch authority is merge-stable for post-merge `No Active Branch` truth, `PR Merge Status Unproven` until the live PR reports a green merge status, `PR Watcher Provisioning Unproven` until the watcher contract is explicit and proven, `PR Watcher Routing Unverified` until the configured watcher route and delivery proof are proven to match the recorded reporting surface, `PR Merge Verification Pending` until that watcher verifies the live PR is merged, and `Bot Review Signal Pending` for the live PR until a thumbs-up reaction or bot comment-resolution closeout exists
- in `Branch Readiness`, require Stage 1 to stop on `Branch Readiness Execution User Approval Missing` until USER approval to enter Stage 2 exists; the Stage 1 packet must include FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, validation plan, expected docs sync, and USER approval blocker before any branch/package admission work begins
- when the branch is inside an unreleased release window, require a `Release Window Audit` and treat serial blocker-clearing PRs as a failure by default; the green posture is `Remaining Known Release Blockers: None`, `Another Pre-Release Repair PR Required: NO`, and `Release Window Split Waiver: None` unless the user explicitly approves a split waiver
- in `PR Readiness`, require the standardized `## Next Branch` block and, when package-ready or green, the copy-ready `## PR Creation Details` operator blocks
- before `PR Readiness`, apply the Pre-PR Durability Rule: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state; only a documented `Durability Waiver`, failed validation, legally file-frozen `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push, and self-imposed blockers must automatically commit and push once lifted
- if a stale-canon or governance-drift class is discovered, the same branch or next legal repair surface must patch the canon or validator rule that allowed it before the repair is considered complete
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
