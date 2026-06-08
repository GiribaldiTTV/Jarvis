# Nexus Codex Modes

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**
**Release Readiness anchor and aggregation rules are owned by `Docs/phase_governance.md`. This modes file keeps only the compact behavioral mirror: do not mutate files in Release Readiness, and derive candidate/window truth from Git/GitHub/helpers.**
**Post-release external operational state carry-forward is not a Release Readiness blocker by itself after RR2 release publication when release/tag/body/health validation is green. Codex may reconcile only `C:\Nexus Governance State` in bounded RR2 closeout without a new USER decision; otherwise BR1 reports `Post-Release External State Carry-Forward:` and BR2 reconciles it before branch/worktree setup or implementation.**

## Purpose

This document defines the collaboration posture Codex should use while handling Nexus Desktop AI tasks.

It works with:

- `Docs/development_rules.md`
- `Docs/phase_governance.md`
- `Docs/Main.md`
- `Docs/orin_task_template.md`

If those sources conflict, live repo truth and the higher-order governance docs win.

## Why Two Modes Exist

Nexus work benefits from two different postures:

- one for deep truth-mapping, drift analysis, and next-move determination
- one for carrying an approved task through execution and verification

The modes should not be confused.
Analysis mode exists to understand the whole system first.
Workflow mode exists to execute approved work without silent scope drift.

## Required Startup Assessment

Before planning, patching, reviewing, or recommending the next move in either mode, Codex must load the owning source-of-truth documents and validate live repo truth.

`Docs/nexus_startup_contract.md` is a ChatGPT/new-chat loader map, not Codex execution authority.
Codex may use it to locate the owning canon quickly, but execution behavior comes from `Docs/Main.md`, `Docs/development_rules.md`, `Docs/phase_governance.md`, this mode document, and the active workstream or branch authority record.
Local ChatGPT custom instructions should stay compact while the repo loader/source-truth may hold longer ChatGPT-facing continuity rules and review memory.
Do not paste the loader doc into Codex prompts; Codex prompts should load `Docs/Main.md` and owning canon for execution authority.
Main is the first repo loader and routing index. After Main, follow the owner chain to execution posture docs, phase governance, Nexus Vision, family vision, active external branch plans, branch records, workstream records, and helper/validator owners as the task requires.
Before narrowing scope or continuing any repo-affecting work, run the `Prompt-Entry Origin/Main Freshness Gate` from `Docs/phase_governance.md`: report `Prompt-Entry Freshness Check:`, `Fetched origin/main:`, current worktree, current branch, `HEAD`, `origin/main`, merge base, `Origin/Main Advanced Since Last Action:`, `Pre-Rebaseline Impact Audit Required:`, and `Rebaseline/Reconciliation Status:`. If `origin/main` advanced or cannot be proven current, stop on `Prompt-Entry Origin/Main Freshness Missing` or `Origin/Main Advanced Rebaseline Required` before mutation, validation-green claims, phase continuation, PR work, merge work, or release work; validating locally is not enough.
When prompt generation, new-chat bootstrapping, or loader/source-truth drift review is in scope, use `Docs/nexus_startup_contract.md` as the owner of the Nexus Prompt Gate final scrub rule before prompt output.
Loader/source-truth continuity must preserve the FAM -> Package -> Slice -> Seam model, with SLC only as a branch-planning alias or historical ID for Slice-level line items, PR evidence-only handling, legacy global FB historical-only handling, single-slice/package-completion blockers, Element Coverage as non-identity, Branch/PR Readiness Stage 1 / Stage 2, Branch Readiness Stage 1 successor-selection ownership, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, release-support carrier when release is blocked, runtime package carrier when runtime work is next, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and the Windows-first, modular, GPU-aware direction with optional heavy local AI capability packs and CPU fallback.
PR Readiness Stage 1 is the Stage 2 readiness-lock gate. It stays active until one outcome is recorded: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`. Bounded Stage 1 repair/sync may mutate durable source truth only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair. When Branch Readiness or PR Readiness discovers a repo-wide governance or workflow-policy repair that was not already in the approved package, Codex must surface and record a package/carrier decision before editing: classify the repair, name the cleanest carrier, state current approval coverage, list pending USER decisions, and either record why the current carrier is legal or stop with the exact separate-carrier decision needed. Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection, rooted in Nexus Vision, family vision, branch vision, current completed work, and the next implementation need. PR Readiness does not require selected-next truth or a waiver by default; Stage 1 owns repair or validation of selected-next truth only when USER explicitly approves PR-time selected-next sync or selected-next truth already exists and would merge as durable repo truth. Stage 1 also owns merge-target `No Active Branch` projection, no-release-debt posture, any unavoidable merged-unreleased release-debt owner contract, and active-branch-authority cleanup when Stage 1 finds them. Stage 2 begins only after `Stage 1 Ready For Stage 2` plus explicit USER approval, and Stage 2 owns final PR execution only: verifying durable Stage 1 projection, commit/push only for bounded operator metadata if legally needed, PR creation, direct PR verification, bot-review handling, mergeability validation, and direct merge/close verification. Recurring PR watcher automation is denied by default unless USER separately approves a named watcher exception for the exact PR.
Stage 1 must include an `Origin/Main Freshness Check` before Stage 2: `Branch Creation Base:`, `Current origin/main:`, `Origin/Main Advanced Since Branch Creation:`, `Origin/Main Changed Files:`, `Branch Changed Files:`, `Reconciliation Required:`, `Reconciliation File List:`, `Reconciliation Recommendation:`, and `Reconciliation Mutation Status:`. If files or source-truth owners need reconciliation because `origin/main` advanced after branch creation, Stage 1 stops on `Origin Main Reconciliation Packet Required`, reports the complete list and recommendation, and performs no file fixes during Stage 1.
Before Codex mutates local branch state to reconcile with newer `origin/main`, it must run `Pre-Rebaseline Impact Audit`. No Baseline By Inertia: clean status, fast-forward possibility, or "housekeeping" language cannot skip the report. The audit must include `Incoming Main Change Set:`, `Incoming Changed Files:`, `Current Worktree Changed Files:`, `Branch Changed Files:`, `Rebaseline Overlap Files:`, `Incoming Runtime / Source-Truth Risk:`, `Validation Before Rebaseline:`, `Recommendation Only:`, `Rebaseline Mutation Approval:`, and `Rebaseline Mutation Status:`; mutation remains blocked until USER approves the exact worktree, branch, target commit, and operation type. If `Rebaseline Overlap Files:` is not `None`, run `Rebaseline Overlap Intent Gate`, inspect `Branch Change Intent Ledger` evidence in the active external branch plan, and stop on `Rebaseline Overlap Intent Missing` when overlap intent is missing, weak, stale, conflicting, or USER-dependent.
Any multi-worktree current-main reconciliation must pass the `Current-Main Reconciliation Identity Guard`: origin/main is context, not identity. After a merge, rebase, fast-forward, or conflict resolution, the digest must include `Assigned Worktree Branch Identity:`, `Branch-Local Authority Reassertion:`, `Incoming Main Active-Branch Blocks Accepted: NO`, and `Sibling Worktree Identity Preservation:`. Do not accept incoming current-workstream, selected-next, or active-branch blocks wholesale when they belong to another worktree; preserve them as merged-main context, then reassert the assigned branch, active branch record, and GitHub Desktop-bound worktree before validation, commit, push, PR readiness, release readiness, or handoff. If this is not true, stop on `Worktree Branch Identity Drift`.
Automation Observability must be treated as evidence-first in both modes. `dev/automation_observability_report.py` reviews Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`; only `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED` findings can enter a bounded repair seam. Lane-sensitive automation must prove its configured cwd, worktree role, branch, `HEAD`, and `origin/main`; `Automation CWD Worktree Mismatch` blocks stale neutral-main, missing-cwd, or wrong-worktree automation reports. Background-observability-only automations may provide evidence but cannot clear PR Readiness, merge-watch, or Release Readiness gates without current runtime/delivery proof and current source-truth ownership; stale historical toolchain-path memory is `REVIEW_INFO` unless current source truth still owns the referenced path. USER-approved `automation/worktree governance intake` may use the `Standing Governance Intake Branch` only for non-runtime multi-worktree safety repair, and USER-approved `phase-gate governance intake` may use it only for repeatable non-runtime phase-gate miss prevention, under `RRI-YYYYMMDD-NNN`, operational `One Active Cycle`, `Sync Rule`, `Waiting For Governance Intake`, `Return Digest`, and `Neutral Main Workspace Rebaseline`. The standing Governance branch is exempt from dedicated post-merge closeout PRs that only clear cycle-ledger wording.
Broad governance/source-truth/process reform must follow `Docs/governance_intake_triage_and_digest_profiles.md`: return a `Governance Intake Triage Packet` before mutation when the intake is not already exact, and use the smallest legal `Digest Profile` (`Decision Packet`, `Return Digest`, `Validation Digest`, `Full Audit Packet`, or `Delta Digest`) instead of replaying full policy.
Digest profile selection chooses packet shape only. Do not compact the digest ever: do not collapse, omit, or replace required digest fields, USER-requested review detail, blocker detail, validation proof, file lists, decision matrices, changed-surface evidence, or exact next-decision wording.
When governance reform changes ownership, aliases, release ownership, public output, helper families, or current-state compaction, load `Docs/governance_efficiency_operating_model.md`; that governance efficiency operating model keeps the output to the smallest legal digest profile instead of restating the full governance stack, while preserving the full selected digest without compaction.
Active branch names must not use the `codex/` prefix; use `feature/` or another USER-approved non-`codex/` prefix, and treat historical `codex/` branch names as traceability only.
Prompt text may frame requested task scope, but it cannot redefine phase behavior, restrict required continuation, define seam continuation, weaken validation requirements, change durability, or change branch authority.

## Mandatory Bounded State

Workflow mode is legal only inside a proven `Bounded State:` unless USER grants an explicit bounded-state waiver.

Before any file mutation, branch/worktree creation or switch, commit, push, PR action, release action, runtime validation, shortcut mutation, provider/model installation, or GitHub Desktop handoff, Codex must prove the exact phase/stage, workspace, git root, branch, upstream, `HEAD`, `origin/main`, worktree role, write target, owning authority record, active package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase.

If that bounded state is absent or ambiguous, Codex must stop on `Bounded State Missing`. If the task needs wider scope than the bounded state allows, Codex must stop on `Bounded State Waiver Missing` unless `Bounded State User Waiver: Granted` names the branch/worktree, phase, slice/seam, relaxed bound, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions.

Assigned Worktree Confinement is part of bounded state. A thread assigned to a worktree must report `Active Thread Owner:`, `Thread Assignment Status:`, `Worktree Ownership Ledger:`, `Intended Write Set:`, `Same Worktree / Same Branch Collision Check:`, `Dirty Worktree Collision Check:`, `Dirty Worktree Recovery Packet:`, `Off-Worktree Work Routing:`, `Governance Routing Barrier:`, `New Worktree Decision Gate:`, `Expected Worktree Root:`, `Actual Worktree Root:`, `No Cross-Worktree Mutation:`, and `GitHub Desktop-bound worktree` before mutation or handoff. If the active git root is outside the assigned worktree, stop on `Worktree Escape User Waiver Missing`; if another active thread owns the same worktree or branch, stop on `Parallel Worktree Coordination Missing`; if the target worktree is dirty and ownership is unclear, stop for a `Dirty Worktree Recovery Packet`; if work belongs outside the assigned root or active branch scope, stop on `Governance Routing Barrier` and route it to `C:\Nexus Worktrees\Governance` instead of self-activating another worktree. Only USER can grant `Worktree Escape User Waiver: Granted` or pass the `New Worktree Decision Gate`, and the waiver/decision must name the expected root, actual root, target root, allowed commands/files, expiration or stop condition, required validation, and return path.

Broad work requests do not authorize implementation. `Continue`, `complete all`, `all remaining work`, `finish the branch`, or similar wording can execute only when source truth resolves it to one exact active bounded seam. Clean validation, branch existence, prompt wording, Codex discretion, or ChatGPT wording cannot infer a waiver.

That startup assessment should explicitly answer:

- `Source-of-Truth`
- `Record State`
- `Branch Truth`
- `Canonical Workstream`
- `Reuse Baseline`
- `Next Safe Move`
- `Source-Truth Placement Preflight` when the task may create a new governance/source-truth file, active artifact, ledger, registry, or durable authority surface
- `Element Validation Ledger Owner` when the task creates, touches, affects, defers, or preserves proof-bearing product elements
- `Dev Toolkit Interface Review Mode disposition` for USER-facing interface elements, including previous and future implementations: callable in dev-only review mode, deferred to a named repo-wide adoption branch/package, or not-applicable with reason

This can stay brief, but it should happen before scope is narrowed for execution.

## Analysis Mode

### Goal

Map the real current state of the system before deciding what should happen next.

### When To Use It

Use Analysis mode when the user asks for:

- drift review
- post-release or post-merge review
- workstream planning
- readiness analysis
- sequencing analysis
- source-of-truth audit
- next-lane determination

### What Codex Should Do

In Analysis mode, Codex should:

- validate current repo truth first
- scan broadly enough to understand the whole affected system
- compare code, docs, branches, tags, and release facts where relevant
- identify factual drift, structural drift, and authority drift
- classify prior suggestions as carry-forward, defer, or discard
- determine the correct next workstream-level move

### Required Analysis Depth

Analysis mode should reason at:

- system level
- lane level
- workstream level
- document-ownership level

Do not narrow to the first apparent slice before full drift and dependency mapping is complete.

### What Codex Must Not Do

In Analysis mode, Codex must not:

- default into implementation
- assume PR, merge, release, or closure is the next move
- compress the task into the smallest possible pass before understanding the system
- treat local unmerged overlays as merged truth

### Expected Outputs

Default Analysis mode return packets include:

- validated current truth
- key drift findings
- structural assessment
- sequencing options
- one recommended next workstream move

## Workflow Mode

### Goal

Execute an approved task faithfully, verify it, and keep the resulting truth coherent.

### When To Use It

Use Workflow mode when the user has already approved:

- a docs-only pass
- a bounded patch
- a canon sync
- a workstream closure pass
- another clearly bounded execution task

### What Codex Should Do

In Workflow mode, Codex should:

- validate live repo truth before editing
- stay inside the approved execution boundary
- make the required changes
- verify the changed behavior or changed docs
- report any drift or remaining gaps honestly
- when the approved boundary contains a seam chain, treat prompt-provided seams as structure only and use `Docs/phase_governance.md` as the continuation authority
- when the current Workstream slice contains a seam chain, use bounded multi-seam workflow as the primary model while executing one active seam at a time
- when a prompt names an active seam, treat it as the entry seam, not a terminal boundary
- `Next-Seam Continuation Required` means continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green
- bounded means one active seam at a time, not one-seam Workstream authority
- a single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete
- Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.
- If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.
- Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.
- A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.
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
- reporting `Next Safe Move` is not a substitute for execution when continuation authority passes
- A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice
- `Continuation Execution Latch` remains active whenever `Continue Decision: Continue`, `Stop Basis: None`, and a same-phase `Next Active Seam` are recorded; Codex must execute the next seam in the same bounded Workstream run instead of returning a terminal report.
- A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
- Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
- Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
- stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition
- when the approved boundary is continuous validation inside the current workstream, keep iterating only while the governing phase rules, validation, and stop-loss contract remain green
- Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
- Workstream must execute an admitted implementation slice unless the USER explicitly approves a docs-only bypass.
- Workstream must keep re-evaluating the backlog item after each seam and slice and continue on the same branch until the backlog item is fully implemented or only future-dependent blockers remain.
- Docs-only Workstreams require explicit USER approval.
- Planning-loop bypass requires `Planning-Loop Bypass User Approval: APPROVED` and `Planning-Loop Bypass Reason:`.
- Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
- Codex must not create, split, promote, package-admit, branch-create, select a backlog identity, or waive a single-slice package without explicit USER approval; if approval is absent, stop on `Backlog Addition User Approval Missing` and output the still-not-closed FAM list plus every not-complete package and slice, or `Backlog Exhaustion User Decision Pending` if that list is empty.
- Codex must run the `Backlog Taxonomy And Source-Truth Placement Gate` from `Docs/feature_backlog.md` before proposing, admitting, or syncing AI-native, cache, architecture, policy, experience-layer, runtime-subsystem, capability-pack, new-FAM, or new-owner concepts into repo source truth. Important concepts do not automatically deserve backlog identity. The packet must classify the concept as `Backlog family`, `Family vision`, `Architecture layer`, `Cross-family policy owner`, `Experience layer`, `Runtime subsystem`, `Capability-pack domain`, or `Package/slice/seam`, name rejected classes, name existing owner files to extend first, and stop on `Backlog Taxonomy Gate Missing` or `Backlog Addition User Approval Missing` when classification or USER approval is absent.
- AI Operational Cache Governance is not memory and is not a new backlog family by default. Route cache behavior first through `Docs/ai_runtime_and_trust_architecture.md`, existing FAM-007 AI/runtime/capability-pack owners, FAM-008 setup/install/cache-root UX owners, the relevant implementing family vision for local data/privacy implications, and the active external branch plan for implementation-specific cache behavior; create another architecture/policy source-truth owner only after `Source-Truth Placement Preflight` proves `No Existing Owner Fits` or USER approves a companion file.
- Small single-seam runtime proofs, validation follow-through, governance repairs, and blocker-clearing traces stay inside existing family/workstream/branch-record traceability by default and are not standalone release-version drivers without explicit USER approval.
- if a stale-canon or governance-drift class is discovered, the same branch or next legal repair surface must patch the canon or validator rule that allowed it before the repair is considered complete
- escaped drift prevention proof is mandatory: every repair for a miss discovered after the phase that should have caught it must include source-truth, governance, validator, helper, or prompt-contract hardening that prevents the same class from passing again, or must record why the gap is not machine-checkable yet and what human review marker replaces it before green
- merge-stable pointer surfaces such as backlog and roadmap must not mirror transient repair-branch ownership while merged-main truth remains `No Active Branch`
- before creating a new governance/source-truth file, active artifact, ledger, registry, or durable authority surface, run `Source-Truth Placement Preflight`, extend the existing owner first, and create a new active artifact only when `No Existing Owner Fits` is recorded or the owning record points to a companion file
- maintain the owning `Element Validation Ledger` in the canonical workstream doc for promoted work or in the active branch authority record for `Registry-only` active branches; run `Element Delta Capture` for created, touched, affected, deferred, future, dependency-only, and non-gating supporting product elements

### What Codex Must Not Do

In Workflow mode, Codex must not:

- silently widen scope
- silently start a new workstream
- silently create PR, merge, release, or closure output without current-truth justification
- treat a clean first slice as automatic branch readiness
- stop after a green seam merely because the prompt task named only the entry seam, the output asks for `Next Safe Move`, durability completed, or one seam was recorded
- treat branch existence, branch rename, backlog promotion, repair-only traceability, or release-bearing posture as Workstream progress by themselves
- treat planning or canon-only output on an implementation branch as valid Workstream progress without explicit USER-approved bypass markers
- open a `docs/governance`, `emergency canon repair`, or repair-only feature branch for future Nexus work
- create a parallel active source-truth artifact for element tracking when the existing workstream doc or branch authority record already owns the ledger

### Expected Outputs

Default Workflow mode return packets include:

- changes applied
- exact governed state markers: `Seam Status`, `Slice Status`, `Completion Status`, `Blockers`, `Waiver Status`, `Continue Decision`, `Continuation Execution Latch`, `Stop Basis`, and `Next Legal Phase`
- validation performed
- a distinct summary of validator results
- a distinct summary of synthetic or headless validation results and the supporting validation artifacts created or used
- a distinct summary of interactive OS-level execution results when that path is feasible
- the existing helper, harness, or shared support reused for interactive validation, or the explicit reason a temporary probe or new helper was necessary
- session cleanup performed and explicitly verified, including what was closed, stopped, restored, or deleted after the pass
- any remaining simulated-only findings or reasoning-only gaps that still matter
- deeper branch-local validation or hardening findings when the slice changes runtime or user-visible behavior
- any timeout or stall conditions encountered during validation, including the last confirmed meaningful progress point and whether the run aborted cleanly
- whether closeout-grade proof came from the helper's documented default budget profile or only from exploratory overrides
- a detailed `## User Test Summary` manual checklist when the slice changes user-visible behavior, runtime interaction, UX flow, prompts, startup behavior, voice behavior, or another operator-facing path
- the updated canonical repo-level `UTS` artifact when the active workstream owns one and the slice makes that artifact relevant
- the exported or refreshed desktop `User Test Summary.txt` copy when the slice is a relevant desktop user-facing path, or an explicit explanation of why that export was skipped
- for relevant desktop user-facing Live Validation, the `User-Facing Shortcut Live Validation Gate` / `desktop-shortcut` result with `User-Facing Shortcut Path:` and `User-Facing Shortcut Validation:` recorded before User Test Summary handoff
- for relevant desktop user-facing Live Validation, the `Codex Live Client Self-QA Gate` result with `Codex Live Client Self-QA:`, `Visual Quality:`, `Live Interaction Evidence:`, `Usability Check:`, and `Platform Uniformity Check:` recorded before User Test Summary handoff
- when the user-facing change is interactive, Codex must exercise the same visible live-client interactions it would ask the USER to test; screenshot-only, marker-only, or launched-but-not-driven proof cannot clear the self-QA gate
- desktop UI Live Validation must use the real user-facing desktop launcher declared for the UTS path when feasible; sandbox/offscreen/direct-runtime/WebView/helper launches are supporting evidence only and cannot replace that launcher gate
- desktop UI Live Validation requires an active foreground/user-observable client mode; hidden, too-fast, or blink-through helper evidence is supporting proof only
- desktop UI Live Validation requires a per-element visual inventory and named focused screenshots in the USER-inspectable OneDrive screenshots folder for every current user-facing window, border/frame, card, row, page break/divider, background treatment, scrollbar, button, dropdown, checkbox, input, chip, status field, confirmation, empty/error/deferred state, and every issue-specific element named by USER feedback; broad full-desktop screenshots are context only
- desktop UI Live Validation must not return a UTS handoff while any unwaived Codex-visible `REPAIR` or `STOP` remains in visual adjudication, the inventory, interaction proof, or screenshot/video proof; use the bounded repair/rerun loop when approved, otherwise report the exact approval blocker
- returned USER UTS or screenshot/video issues must stay in a temporary issue form until PR Readiness Stage 1 folds resolved truth into durable source truth, and Live Validation must map every issue ID to focused proof artifacts and a visual verdict
- when the user-facing shortcut result is outstanding, the explicit blocker `User-Facing Shortcut Validation Pending`; helper-only, synthetic, harness, or direct-runtime evidence must not be reported as final green while this blocker remains
- when Codex live-client self-QA is outstanding, the explicit blocker `Codex Live Client Self-QA Pending`; marker-only or screenshot-only evidence must not be reported as ready for USER handoff while this blocker remains
- when returned User Test Summary results are still outstanding, the explicit blocker output: `Automated validators and live helper evidence: GREEN.`, `User Test Summary Results: PENDING.`, and `Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.`
- when meaningful desktop UI changed and closeout posture matters, a distinct summary of the live launched-process UI audit results and evidence
- an explicit statement under `## User Test Summary` when no meaningful manual test exists and why
- Every Live Validation digest must include an exact `## User Test Summary` section; if User Test Summary is waived, the digest must still include `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`
- if `User Test Summary Results: WAIVED` is used, the response-level `## User Test Summary` section and the canonical workstream `## User Test Summary` artifact must include `User Test Summary Waiver Reason:`
- if `User-Facing Shortcut Validation: WAIVED` is used, the response-level `## User Test Summary` section and the canonical workstream `## User Test Summary` artifact must include `User-Facing Shortcut Waiver Reason:`
- remaining drift or known gaps
- whether the approved phase is complete

Generic `Results` or `Validation` summaries do not replace the governed state markers above.
Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation.
Formal Next Legal Phase Digest is required whenever a phase packet stops for USER approval. The response must include a `Next Legal Phase Digest` with `Current Phase:`, `Next Legal Phase:`, `Why This Phase Is Next:`, `Approval Required:`, `Exact USER Approval Text:`, `Allowed Scope:`, `Explicit Exclusions:`, `Validation Required:`, `Stop Conditions:`, `USER Plan Review Gate:`, `USER Inspection Files:`, `Review Required Because:`, `Implementation Blocker:`, and `Review Waiver Reason:`. Missing fields block on `Next Legal Phase Digest Missing`; `Next Safe Move` or informal recommendations cannot replace the digest.
Formal Next Legal Phase Digests must not be compacted, abbreviated, summarized away, replaced by one-line next-step wording, or omitted because similar information exists elsewhere in the packet. `USER Plan Review Gate:` must say whether USER may accept, revise, waive, or reject the plan. `USER Inspection Files:` must name exact files or the local USER hub packet when review is required. `Implementation Blocker:` must name the blocker when implementation remains unauthorized.
A green seam does not authorize stop while `Slice Status` is still non-green.
A green slice does not authorize stop while `Completion Status` is still non-green.
A green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice.
If `Completion Status` is `In Progress` and no named blocker or waiver stops work, Workflow mode must continue rather than returning `Await Next Instruction`.
Use these governed state markers as execution control, not just reporting.
If `Continue Decision` is `Continue`, Workflow mode must not end on a seam-complete final response, rollback path, or next-seam recommendation; it must keep executing until a lawful `Stop` decision exists.
A prompt `Return:` block is an output shape only; it cannot override governed continuation markers or authorize a terminal response while `Continue Decision` remains `Continue`.
A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
After Workstream execution is admitted for a multi-seam or multi-slice package, the approval covers bounded execution of the admitted same-branch Workstream package unless USER explicitly records a single-seam waiver, backlog split, or named stop condition. Per-seam approval-missing / approval-pending wording such as `First Bounded Implementation Seam Approval Missing`, `Next Bounded Seam Approval Missing`, or `SLC implementation pending USER approval` is not a real blocker. Workflow mode must keep bounded Workstream execution moving one active seam at a time until Workstream Green, a real named blocker, or explicit USER waiver is recorded.

Before any final response during `Workstream`, Codex must run a `Post-Seam Continuation Self-Audit`. if `Completion Status: In Progress` and `Continue Decision: Continue`, the self-audit result must be `Continue Same Workstream`. If Codex cannot continue, it must record `Completion Status: Red` with the exact named blocker or USER waiver needed instead of returning a green seam closeout as terminal. In short, it must not return a green seam closeout as terminal.
If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
`Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
`Phase: Workstream` must remain bounded at all times; the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
Phase Boundary Stop Required: A phase-exit seam named in `Next Active Seam` is a handoff target, not current-phase execution authority.
Bounded Workstream continuation ends at phase boundaries; it never crosses from Workstream into Hardening by inertia.
Codex must not execute Hardening, Live Validation, PR Readiness, Release Readiness, release work, or any other next phase in the same run unless USER explicitly admits that phase after reviewing the handoff.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
If `Completion Status` is `Red`, `Continuation Action` must report the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume.

Pre-PR Durability Rule:

- before `PR Readiness`, when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state
- this applies through `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`
- a prompt-level request to stop before commit/push is not a durability exception; only a documented `Durability Waiver`, failed validation, legally file-frozen `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push
- if Codex names a self-imposed blocker, it must name the lift condition; once lifted, Codex must automatically commit and push without requiring a second durability prompt
- if validation fails, do not commit and push; report the blocker and keep the branch in the current phase until the blocker is lifted
- `PR Readiness` still performs the final dirty-branch and durable-truth gate before PR creation

When the approved phase is `PR Readiness`, the output must also explicitly include:

- the current PR Readiness stage: `PR Readiness Stage 1 - Analysis Gate` or `PR Readiness Stage 2 - Execution Gate`
- confirmation that Stage 1 is an analysis-first blocker repair gate when the current PR Readiness stage is Stage 1
- for Stage 1, the `## PR Readiness Stage 1 Analysis Packet`, including required post-merge path, release-debt impact, release-debt handling status, selected-next validation status when selected-next truth exists or PR-time selection is explicitly approved, required current-branch source-truth sync, completed merge-target authority/no-release-debt projection repairs when Stage 1 finds repairable drift, Stage 2 execution plan, Stage 1 repairs made and repair validation, `Governance Ledger Fallback:`, `Branch Readiness Fallback:`, `Stage 1 Outcome:`, `Next Legal Phase:`, optional `## Next Workstream` and `## Next Branch Pre-Plan` blocks only when USER asks PR Readiness for successor-selection analysis or selected-next truth already exists, plus `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required` when selected-next, next-branch, or governance ledger audit findings must route to Branch Readiness, plus `PR Readiness Stage 1 Repair Pending` until repairable PR-readiness drift/blockers found during Stage 1 are fixed, validated, committed, and pushed inside a USER-approved legal current-branch repair seam, and `PR Readiness Execution User Approval Missing` as the stop blocker until explicit USER approval to enter Stage 2 is recorded
- for Stage 2, confirmation that USER approval to enter Stage 2 exists before any repository mutation, staging, commit, push, PR creation, recurring PR watcher automation, next-branch creation, release work, or canon edits occur
- confirmation that the merge-target canon completeness gate passed
- confirmation that the Governance Drift Audit ran
- whether governance drift was found
- confirmation that stale-canon, post-merge-state, dirty-branch, docs-sync/drift-audit, conditional selected-next, `Backlog Addition User Approval Missing`, `Backlog Exhaustion User Decision Pending`, `Single-Slice Package User Approval Missing`, `Package Completion Unproven`, and `User Test Summary Results Pending` blockers are clear
- confirmation that `Next Runtime Candidate Selection Pending` is clear only when explicit USER approval for PR-time successor selection exists or selected-next truth already exists; otherwise Branch Readiness Stage 1 owns normal next runtime implementation pipeline selection
- confirmation that only `Admission State: Admitted` slice rows count toward package admission; historical evidence, future placeholders, deferred ideas, and future-package-required rows cannot satisfy the multi-slice rule
- confirmation that `PR Readiness Scope Missed`, `Between-Branch Canon Repair Attempt`, and `Next Branch Created Too Early` are clear
- confirmation that `Release Window Audit Incomplete` is clear, including the normal green posture `Remaining Known Release Blockers: None`, `Another Pre-Release Repair PR Required: NO`, and `Release Window Split Waiver: None`, unless an explicit user-approved split waiver is recorded
- confirmation that the `Release Readiness Health Pass` proves post-merge source truth before PR creation, after any Stage 2 or bot-review source-truth repair, and before merge approval by running `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`; the response must report `Post-Merge Branch Authority Projection:`, `Stale Active Branch Wording Scan:`, `Stale PR Creation / PR Readiness Pending Wording Scan:`, `Merged-Unreleased Scope Posture:`, `Release Execution Gate:`, `Watcher / Live PR State Projection:`, `Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `FAM Overlap Routing:`, `Release Candidate Anchor Projection:`, `Release Window Contributor Inventory:`, `Governance Intake Routing:`, and `Projected Post-Merge Validation:`, and must stop on `Merge-Stable Projection Shadowed By Active Authority` if a separate projection receipt exists while the same branch remains under `Active Branch Authority Records`
- confirmation that `PR Creation Pending`, `PR Validation Pending`, `PR State Unknown`, and `PR Merge Status Unproven` are clear before reporting `PR Readiness GREEN`
- confirmation that `Merge-Target Authority Projection Unproven` is clear before reporting `PR Readiness GREEN`; when post-merge truth will be `No Active Branch`, active branch authority must be moved to historical/no-active or otherwise made merge-stable before PR green
- confirmation that `PR Merge Verification Pending` is clear before reporting `PR Readiness GREEN`
- confirmation that `Bot Review Signal Pending` is clear for the live PR through a Codex Connector bot thumbs-up reaction or green approval comment on the current head; approval proof must be bound to the current live PR head by review commit SHA, PR timeline order, or equivalent GitHub live-head evidence, not by local commit time alone; when a bot comment appeared after the last approval, a later thumbs-up/approval signal is required after same-PR repair and comment-resolution closeout
- confirmation that bounded PR2 uses direct PR verification by GitHub connector, `gh`, GraphQL review-thread inspection, status checks, reactions where available, mergeability, head SHA, and merge/close state; recurring PR watcher automation is denied by default
- confirmation that `PR Watcher Provisioning Unproven` and `PR Watcher Routing Unverified` are active only when the USER explicitly approved a watcher exception for the exact PR; otherwise direct PR verification owns live PR, bot-review, mergeability, and merge/close proof
- confirmation that the PR Watcher Mode Contract in `Docs/pr_watcher_mode_contract.md` is followed only for a USER-approved watcher exception or historical receipt: watcher mode is exactly `Silent Monitor`, `Verify Once`, `Repair Mode`, or `Blocked Mode`, and `Watcher Health Proof:` includes `Watcher Mode:`, `Configured CWD:`, `Worktree / Branch:`, `PR:`, `Head SHA:`, `Mergeability:`, `Unresolved Review Threads:`, `Latest Bot Review:`, `Repair Authority:`, `Delivery Route Proof:`, `Runtime Proof:`, and `Next Watcher Posture:`
- confirmation that every Codex Connector review-request or revalidation PR comment is 3-5 words only, preferably `@codex review please`; one or more actionable bot comments trigger bounded same-branch repair that verifies identity, evaluates source truth, fixes only approved PR scope, reruns validation, commits, pushes, replies/resolves when required by the review-thread contract, requests Codex Connector bot revalidation, and then keeps `PR Validation Pending` active until a later thumbs-up reaction or green approval comment clears the repaired head; out-of-scope bot requests must be reported as blockers instead of repaired
- confirmation that `PR package ready` is not being collapsed into `PR Readiness GREEN`
- confirmation that `PR Readiness Stage 1 Repair Pending` is clear before Stage 2 by repairing any Stage 1-discovered PR-readiness drift/blockers on the current branch and making the repair durable, including selected-next branch/workstream truth or USER waiver, merge-target `No Active Branch` projection only when explicitly waived, no-release-debt posture, any unavoidable merged-unreleased release-debt owner contract, and active-branch-authority cleanup when present
- confirmation that no PR-owned docs or canon work is being deferred to Release Readiness, updated `main`, or a governance-only branch
- confirmation that `main` remains protected and that no Codex file mutation, staging, commit, generation, refresh, or repair work is being performed on `main`
- confirmation that branch truth is committed and durable, not only present in the working tree
- confirmation that the normal governance validator and the PR-readiness gate mode passed
- for the selected next workstream when explicit USER approval for successor selection exists:
  - the selected next workstream identity
  - the next workstream `Record State`
  - the backlog `Priority` used as the primary selection signal
  - confirmation that `Target Version` was not used to rank, select, defer, or skip the open backlog candidate
  - if the selected item is deferred, confirmation that `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:` are present
  - the minimal scope recorded in canon
- confirmation that, when explicit USER approval for PR-time successor selection exists or selected-next truth already exists, backlog includes `Next Workstream: Selected` and `Minimal Scope:` and roadmap includes `## Selected Next Workstream`; otherwise report that selected-next truth is absent by default and normal successor selection belongs to Branch Readiness Stage 1
  - confirmation that the selected next workstream is a real runtime Feature Family candidate and that `Minimal Scope:` names a runtime slice
  - confirmation that no branch exists yet for that next workstream
  - confirmation that successor branch creation is deferred to `Branch Readiness` after merge and updated-`main` revalidation
- when USER explicitly waives/defers selected-next truth and post-merge truth will resolve to `No Active Branch` because unavoidable release handling or another repo-level admission blocker remains open:
  - repo state `No Active Branch`
  - the blocking admission item
  - `Merged-Unreleased Release-Debt Owner:`
  - `Release Target:`
  - `Release Floor:`
  - `Version Rationale:`
  - `Release Scope:`
  - `Release Artifacts:`
  - `Post-Release Truth:`
  - confirmation that the release target is semantically correct from the latest public prerelease and declared release floor
  - confirmation that branch creation remains deferred and no next implementation branch may execute by inertia
- an optional user-facing `## Next Workstream` section with this field shape when USER asks PR Readiness for successor-selection analysis or selected-next truth already exists:

```markdown
## Next Workstream
- Recommended Next Workstream:
- Recommended Family / Package:
- Candidate Slices:
- Candidate Work To Be Done:
- User-Facing Output:
- Why This Is Next:
- Dependencies / Blockers:
- Validation Needs:
- Release Impact:
- Selection Truth Status:
- Branch Creation Status:
```

- Missing next-workstream recommendation, missing selected-next truth, missing `Next Workstream User Waiver:`, or omitted next-workstream block does not block Stage 2 by default. If USER-approved PR-time selected-next truth exists or selected-next truth already exists, validate it and report the applicable selected-next blocker when it is inconsistent.
- Stage 1 must record one outcome before any Stage 2 approval can be accepted: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`
- Stage 2 may begin only after `Stage 1 Ready For Stage 2` is recorded and explicit USER approval exists; PR creation is blocked while any Stage 1 blocker, Stage 1 repair item, applicable selected-next validation item, applicable branch-shape review item, or Stage 2 sync prerequisite remains unresolved
- an optional Stage 1-only `## Next Branch Pre-Plan` section with this field shape when USER asks PR Readiness for next-branch analysis or selected-next truth already exists:

```markdown
## Next Branch Pre-Plan
- Next Branch Package Shape:
- Proposed FAM:
- Proposed Package:
- Candidate Slices:
- Candidate Work To Be Done:
- Single-Slice Drift Review:
- Family Organization Review:
- Element Coverage Review:
- Dependencies / Blockers:
- Validation / Live-Test Needs:
- Branch Creation Status:
- USER Approvals Required:
```

- if an in-scope Next Branch Pre-Plan cannot prove a broad FAM/package with multiple concrete candidate slices, or it looks like single-seam/single-slice drift or family-organization drift, report `Current-Branch Branch Readiness Re-entry Required` when the current branch remains the legal carrier or `New Carrier Branch Required` when the current branch cannot own the blocker, then route the next legal work to Branch Readiness instead of PR Readiness Stage 2
- if the governance/source-of-truth ledger audit finds identity model drift, FAM taxonomy drift, package/branch rule drift, USER approval blocker drift, real-carrier routing drift, branch-authority lifecycle drift, watcher/automation proof drift, release readiness/execution boundary drift, Element Coverage misuse, ChatGPT loader/source-truth drift, project-direction drift, current workflow drift, after-release workflow drift, or absolute-guardrail drift that cannot be cleared as bounded current-branch PR Stage 1 repair, report `Governance Ledger Fallback:` plus either `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required` and route to Branch Readiness

- if the in-scope pre-plan cannot show a broad FAM/package with multiple concrete candidate slices, report `Next Branch Package Shape Unproven`
- if the in-scope pre-plan looks like a single-seam or single-slice branch, report `Single-Slice Branch Drift Risk Unresolved`
- if the in-scope pre-plan drifts from FAM -> Package -> Slice -> Seam or revives old live `FB-###` identity behavior, report `Family Organization Drift Risk Unresolved`
- Optional conditional `Next Branch` response block: an optional `## Next Branch` section with this exact field shape when selected-next truth is explicitly in scope or Branch Readiness is the next legal phase:

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

- when PR Readiness is package-ready or `PR package ready`, inclusion-only PR operator copy blocks with this exact shape:

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

The `Next Branch` section must separate the next legal branch type/name from the selected next implementation workstream branch.
If release debt, updated-`main` revalidation, or another admission gate blocks branch creation, `May Create Now: NO` is required with the reason.
The `PR Creation Details` block is preparation material only; it must not imply PR creation, merge execution, release execution, next-branch creation, or PR Readiness GREEN has occurred.
Each PR operator field must be its own copy-ready block and must be usable independently.
The PR summary/GitHub PR body uses exactly three top-level sections: `## Summary`, `## Branch Evidence`, and `## Validation`.
`## Summary` must be one concise outcome paragraph, and `## Branch Evidence` must not repeat the Summary through nested `### Summary`, `### Purpose`, or `### Overview` sections.
Use concrete Branch Evidence subheads such as `### Changes`, `### Context`, `### Source Truth`, or `### Boundaries` only when they improve scanability.
The PR summary must include implemented branch truth only. Generic exclusion dumps, `Not Included` sections, and defensive scope language remain prohibited; concise branch-specific boundaries are allowed inside `## Branch Evidence` when they clarify reliable branch truth.
`## Validation` must contain validation commands, proof paths, or the historical no-validation sentence only.
GitHub PR bodies and PR Summary copy must not include phase-digest or Codex operator handoff fields such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, `Stop Basis`, `Exact next USER decision`, `Implemented, validated`, or `::git-*`; those belong in governed Codex/source-truth output, not branch evidence copy.
Before PR creation, write the proposed GitHub PR body to a temporary local file and run `python dev\orin_pr_body_quality_audit.py --body-file <path> --body-title "<PR title>"`. If it reports `Changed: True` or warnings, stop on `PR Body Drift Check Failed`, normalize the body with `--apply` or replace the PR body with the normalized output, and rerun the check before calling `gh pr create` or any connector PR-creation action. After PR creation, verify the live PR body with `python dev\orin_pr_body_quality_audit.py --limit 1` or narrower equivalent. The helper must preserve trimmed Summary detail inside `## Branch Evidence`; do not use lossy summary trimming as a shortcut to PR-body green.
PR Readiness GREEN requires the PR to exist, be open, be non-draft, have no conflicts, explicitly report a green merge status, match merge-target canon, clear `Merge-Target Authority Projection Unproven` by ensuring active branch authority will not survive into merged `main` when post-merge truth is `No Active Branch`, have no unresolved Codex comments/issues or requested changes, clear the live PR bot-review signal through a Codex Connector bot thumbs-up reaction or green approval comment on the current head, directly verify the live PR head/checks/comments/reviews/mergeability in the active Codex turn or helper output, clear `PR Watcher Provisioning Unproven` and `PR Watcher Routing Unverified` only when a USER-approved watcher exception exists, clear `PR Merge Verification Pending` only after direct GitHub/GitHub-connector verification proves the PR is `merged`, and avoid `Automation Runtime Unproven`; approval proof must be bound to the current live PR head by review commit SHA, PR timeline order, or equivalent GitHub live-head evidence, not by local commit time alone; when a bot comment appeared after the last approval, a later thumbs-up/approval signal is required after same-PR repair and comment-resolution closeout. This is the same-PR Codex bot-review repair loop: actionable bot comments must be fixed on the same PR, pushed, replied to, resolved, revalidation-requested with a 3-5 word PR comment only, and then approved by a later Codex Connector bot thumbs-up/approval signal before green. Stage 2 final handoff cannot be green until the post-repair bot thumbs-up/approval latch is verified. The Direct PR2 Continuation Rule blocks quiet handoff: bounded PR2 direct verification keeps running in the active Codex turn after revalidation requests and repair pushes until new actionable feedback is repaired or blocked, the current-head approval latch plus green mergeability allows merge, the PR merges/closes, or a real blocker appears. Recurring PR watcher automation is denied by default for bounded PR2; watcher modes and Watcher Health Proof apply only to a USER-approved watcher exception or historical receipt.

Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript. If missing proof blocks a release, carry it on a real release-support carrier; if product work is next, carry it on the next real runtime package carrier.

Automation Observability Review Pending uses `dev/automation_observability_report.py` as the local source-of-truth reader for Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`. Treat `BLOCKER_CANDIDATE` and `REVIEW_REQUIRED` findings as bounded repair candidates that must be admitted before repo canon changes; treat `REVIEW_INFO` as informational unless it contradicts repo truth. Background-observability-only automations are advisory and must not be used as watcher-exception proof, bot-review repair proof, merge verification proof, or release-readiness proof. `ACTIVE` is configuration state, not run proof; accepted automation runtime proof must come from thread or inbox output, automation memory/log/state-file updates, scheduler last-run evidence, or a bounded fallback that is target-scoped, phase-scoped, and self-terminating or explicitly deleted.

When the approved phase is `Branch Readiness`, the output must also explicitly include:

- the current Branch Readiness stage: `Branch Readiness Stage 1 - Analysis Gate` or `Branch Readiness Stage 2 - Execution Gate`
- for Stage 1, the `## Branch Readiness Stage 1 Analysis Packet`, including product vision, project-wide vision alignment, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable vs full-system boundary, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, rejected shallow plan, alternatives/tradeoffs reviewed, open USER decision points, deferred ideas/future-package ledger, `Stale Branch Cleanup Plan:`, `Branch Readiness Planning Incomplete` blocker review, `Next Legal Phase:`, interface release boundary review with `Primary Interface Release Surface:`, fallback point, interface acceptance/proof path, and `Interface Bundle User Approval:` status for user-facing family/package branches, plus the `Carrier Lifecycle Decision` with `Carrier Lifecycle Classification:` exactly one of `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, or `Active remote/open PR branch`, and with `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Branch Cleanup Execution Gate:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`; include confirmation that there was no repository file mutation, no branch creation, no package admission, no docs sync, no PR work, no release work, and no selected-next truth, plus `Branch Readiness Execution User Approval Missing` as the stop blocker until explicit USER approval to enter Stage 2 is recorded; when USER input is needed, the question packet must include Codex recommendation, rationale, options, tradeoffs, current-branch impact, future-package impact, safe default, waiver/defer posture, and exact response format; if USER needs a durable editable handoff, Stage 2 may generate or refresh a USER-facing `User Vision Input.txt` desktop artifact, but the artifact is not repo source truth until a later USER-approved digest pass records completed answers; missing recommendation/rationale/tradeoffs blocks on `USER Vision Recommendation Missing`; missing/incomplete/undigested input artifacts block on `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, and `USER Vision Input Pending`; missing or shallow product-system planning blocks on `Project-Wide Vision Alignment Missing`, `Branch-Specific Vision Alignment Missing`, `System Concept Model Missing`, `Entity / Profile Model Missing`, `User Workflow Model Missing`, `Scale / Data Volume Model Missing`, `Configuration And State Model Missing`, `Expected User-Facing Outcomes Missing`, `Codex Additional Recommendations Missing`, `USER Critique Loop Missing`, `USER Decision Ledger Missing`, `Deferred Ideas / Future Package Ledger Missing`, `Planning Adequacy Review Missing`, `Rejected Shallow Plan Missing`, `Alternatives And Tradeoffs Missing`, `Whole-System Interaction Map Missing`, `Minimum Viable vs Full System Boundary Missing`, or `Open Questions / USER Decision Points Missing`; missing or ambiguous primary interface release boundaries block on `Interface Release Boundary Missing`, `Primary Interface Undefined`, `Multiple Interface Release Drift`, `Fallback Point Missing`, `Interface Acceptance Missing`, or `Branch Readiness Interface Planning Incomplete`; Branch Readiness does not select the next workstream by default and instead analyzes/adopts USER-approved selected-next truth from prior PR Readiness when present
- active implementation `Product Definition Plan` entries must include non-empty, concrete `Project-Wide Vision Alignment:`, `Branch-Specific Vision Alignment:`, `System Concept Model:`, `Entity / Profile Model:`, `User Workflow Model:`, `Scale / Data Volume Model:`, `Configuration And State Model:`, `Expected User-Facing Outcomes:`, `Codex Additional Recommendations:`, `USER Critique Loop:`, `USER Decision Ledger:`, `Deferred Ideas / Future Package Ledger:`, `Planning Adequacy Review:`, `Rejected Shallow Plan:`, `Alternatives And Tradeoffs Reviewed:`, `Whole-System Interaction Map:`, `Minimum Viable vs Full System Boundary:`, and `Open Questions / USER Decision Points:` markers before Workstream, Hardening, Live Validation, or PR Readiness begins or resumes; placeholder or self-assessed values such as `simple`, `basic`, `minimal`, `see above`, or `not applicable` do not count as proof
- runtime-focused implementation branches must also carry `## Runtime Branch Engineering Contract` before Branch Planning begins, with `USER Engineering Planning Review:`, `Runtime Implementation Approval:`, `Current Runtime Baseline:`, `Planned Runtime Delta:`, `User-Facing Runtime Delta:`, `State / Config / Schema Delta:`, `Validator / Helper Delta:`, `Expected Changed Files / Surfaces:`, `Approval-Boundary Audit:`, `Future-Gated Items:`, `Workstream Seam Map:`, `Proof Expectations:`, `Risk Forecast:`, `Recommendations And Alternatives:`, `Plan Version / Revision Status:`, and `Plan-To-Implementation Traceability:`; new or re-entering runtime branches must also carry an active Branch Runtime Engineering Plan at `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` or a pending Stage 2 requirement, linked by `Branch Runtime Engineering Plan Path:`, with `Engineering Plan Status:` and `PR Fold-Down Packet:` markers; Branch Planning must create or refresh the active worktree's local USER hub packet under `C:\Nexus USER\<worktree-label>` with root `START_HERE.md`, exactly one primary current-gate decision file under `USER Review`, generated supporting digests/checklists under `Review Aids`, and copied branch vision, active external branch plan or historical repo receipt, branch authority, relevant Nexus/family vision, matrix, UFD/change-intent, and source-truth context under `Source Truth Context` before asking USER to green-light implementation; BP1 must return the `USER Branch Vision Review Gate`, BP2 must return the `USER Branch Plan Review Gate`, and BP3 must return Workstream Entry / Orchestration Validation; stop on `BP1 Branch Vision Review Missing`, `BP2 Branch Plan Review Missing`, `BP3 Orchestration Validation Missing`, `USER Review Packet Stale`, or `USER Review Packet Not Digested` when required planning review, USER response, Codex Response Digest, scope dispositions, exact USER decision, or `USER Review Packet Finding:` is absent or stale; use the accepted Branch Planning contracts and active external plan to compare seam start packets, seam closeouts, Workstream Green, Hardening proof, Live Validation proof, PR Readiness scope integrity, and Release Readiness public scope against admitted engineering intent
- completed USER input digests may add package-specific planning blockers such as legacy product-name drift, telemetry provider selection, polling floor, warning modality, external telemetry privacy model, cross-family audio approval, or persona/model switching scope; these block Workstream entry or continuation until Branch Readiness revalidates or defers them. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.
- Branch Planning reinforcement: BP1 must treat `USER_BRANCH_VISION_REVIEW.md` as the USER Branch Vision Contract, and BP2 must treat `USER_BRANCH_PLAN_REVIEW.md` as the BP2 Branch Plan Contract. BP1 owns branch goal, end-state, product shape, user-facing behavior, surfaces, options, Codex recommendations, USER response, Codex digest, accepted Branch Vision, deferred/future-gated ideas, and decision state. BP2 owns the accepted Branch Vision summary, package summary, branch scope size test, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, H1/LV/UTS expectations, rollback/safety plan, risks, future-gated boundaries, plan review checklist, `USER Review Response`, Codex digest, implementation constraints, and exact BP3 approval text. Branch Planning packets must keep `Packet Reviewability State` separate from `USER Gate State`; reviewable/helper-green packet output is not USER acceptance or implementation authority. `Contract Status` must be `Complete` or `Waived by USER` before implementation approval is legal; `Draft`, `Pending USER Response`, `Pending Codex Digest`, and `Pending USER Confirmation` block implementation. If USER feedback changes direction, UI behavior, workflow, scope, boundaries, or seam order, Codex must update source truth and the local USER hub packet/ZIP, set Contract Status to Pending USER Confirmation, and wait for confirmation or explicit waiver. SLC/slice/seam details are implementation staging only and must not become the primary USER decision surface.
- candidate-only scope, future deferrals, provider path, polling posture, warning modality, privacy model, naming/product-copy handling, acceptance criteria, or proof standards are not enough to resume Workstream; Stage 2 may finalize them, but Stage 1 must revalidate before implementation continues unless USER waives the requirement
- the FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, validation plan, expected docs sync, blockers and waivers, rollback path, and the exact Stage 2 green-light decision needed
- for Stage 2, confirmation that USER approval to enter Stage 2 exists before branch/package admission work, docs sync, branch creation, or authority-record setup occurs
- for Stage 2, the `Thread Launch / Write-Target Identity Lock` result before mutation, including current workspace, git root, branch, upstream, `HEAD`, `origin/main`, worktree role, clean state, expected phase/seam, write target, active thread owner, thread assignment status, worktree ownership ledger, intended write set, same-worktree/same-branch collision check, dirty-worktree collision check, dirty-worktree recovery packet posture, and any runtime/process or GitHub Desktop binding checks relevant to the work; if assigned parallel worktree mode is active, also include assigned thread owner, intended write set, source-truth owner, shared-file overlap forecast, Git operation ownership, runtime/interactive-validation ownership, and branch/file health markers; if any identity does not match, stop on `Thread / Worktree Identity Mismatch` or `Parallel Worktree Coordination Missing` and return a routing packet instead of continuing

Element Coverage is a non-identity checklist only. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

When the approved phase is `Release Readiness`, the output must also explicitly include:

- whether the branch is release-bearing
- confirmation that `Release Target Undefined` is clear
- for release-bearing branches:
  - `Release Target:`
  - `Release Floor:`
  - `Version Rationale:`
  - `Release Scope:`
  - `Release Artifacts:`
  - confirmation that marker presence and semantic target correctness both pass
- for explicitly non-release branches:
  - `Release Branch: No`
  - confirmation that this is only a historical context, not a new governance-only branch or a direct-main repair path
- confirmation that the non-release waiver is not being used for an `implementation` or `release packaging` branch
- confirmation that `Release Debt`, post-merge truth, validation, and successor branch deferral remain governed by their normal blockers
- confirmation that Release Readiness is not being used as a docs-sync or branch-authority cleanup phase
- confirmation that Release Readiness is not deleting stale/old branches, removing worktrees, switching branch targets, or changing a GitHub Desktop-bound worktree; it may record `Branch Cleanup Plan:` plus `Branch Cleanup Execution Gate:` and defer execution to `Branch Readiness Stage 2 - Execution Gate`
- confirmation that cleanup touching a family-stable or GitHub Desktop-bound folder is blocked by `Stable Worktree Path Preservation Gate:` until `Stable Worktree Path:`, `Replacement Binding Path:`, and the preservation method are recorded; stop on `Stable Worktree Path At Risk` if the stable folder would be removed before the successor branch/worktree is moved, switched, or explicitly rebound there
- confirmation that Release Readiness declares `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, and `Candidate Includes Later Governance Repairs:` and stops on `Release Candidate Anchor Missing` when those values are absent or ambiguous
- confirmation that Release Readiness declares `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, and `FAM Contributor Routing:` and stops on `Release Window Contributor Inventory Missing` when multi-FAM/worktree contributor inventory is absent or ambiguous
- confirmation that Release Readiness validates current fetched `origin/main` by default and treats historical PR merge commits as audit evidence only unless USER explicitly selects a historical commit as the release target
- confirmation that merge order does not decide release ownership; multiple FAM/worktree contributors in the selected target are released through `Release Ownership Model: Aggregated release window` unless USER selects a narrower release target
- confirmation that governance/source-truth-only PRs merged after the last runtime PR may be included in the release candidate without forcing the target back to the runtime merge commit, with `Candidate Includes Later Governance Repairs: YES` recorded and internal-only repairs kept out of user-facing release-feature claims
- confirmation that Release Readiness is analysis-only for repository files and that no source, docs, canon, validator, helper, release-note, or handoff files were edited, staged, committed, generated, or refreshed
- if any file change is needed, classification as `Release Readiness File Mutation Attempt`, then return to `PR Readiness` before merge or defer to the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge instead of patching inside Release Readiness
- when Release Readiness is green for release execution, inclusion-only release operator copy blocks with this exact shape:

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

The Release Notes block must prepare the human-written Markdown release body using the standard release body shape: `## Release Summary` or `## Release Overview`, followed by `## Release Highlights` or release-specific rich sections.
The live GitHub release body must not start with or repeat the release title as `# <release title>`; the release title belongs in GitHub release metadata and the separate `Release Title` operator block only.
During Release Execution, the live GitHub release body must also include GitHub-generated release notes with `## What's Changed` and the generated `**Full Changelog**:` compare link to the previous release, populated through the GitHub release notes button or generated-release-notes API.
Do not hand-write or omit the generated changelog section when publishing or repairing a GitHub release.
Public release bodies must not include internal automation/tooling brand tokens, generated branch-prefix noise, phase-handoff text, or operator transcript text. Rewrite generated `[codex]` / `codex/...` PR labels into neutral user-facing PR names before publication or repair them immediately after publication.
The release-body standard applies to every published Nexus pre-Beta release body, not only the latest release.

- release notes must clearly explain what was built, what capabilities exist, and how the system behaves
- release notes must not include exclusion lists, `Not Included` sections, negative scope framing, or defensive wording

Do not report cleanup as complete unless the pass has explicitly checked for leftover apps, windows, dialogs, helper processes, probe files, or other temporary artifacts it created or opened.

Do not report an interactive validation pass as complete or trustworthy if it exceeded its time budgets or sat stalled without a clean abort path.

Do not create a new live-validation script by default.
For Live Validation, Codex should reuse existing helpers first, then parameterize or extend them, then extract shared support if several helpers need the same watchdog or cleanup behavior.
Temporary one-off probes are allowed only as ignored exploratory artifacts and must be deleted or promoted into documented reusable tooling before closeout-grade proof is claimed.
Durable root `dev/` validators, live-validation scripts, audit helpers, harnesses, and shared helper modules must also be checked against `Docs/validation_helper_registry.md`.
If a new helper is kept, Codex must report its standardized name, `Helper Status:`, owner, reuse decision, and `Consolidation Target` when it is `Workstream-scoped`.
Workstream-scoped seam helpers are bridge tooling, not the default release naming model, and must be consolidated, promoted, or explicitly justified before PR Readiness.
Any `Temporary probe` must stay ignored and be deleted or promoted before closeout-grade proof.

## Workstream And Branch Governance

### Grouped Workstreams

During `pre-Beta`, grouped workstreams are allowed when they remain coherent by subsystem and end-state.

That means:

- one branch may host multiple validated slices for one milestone
- grouped workstreams should not become grab-bags of unrelated ideas
- lane evaluation should stay milestone-driven rather than slice-driven

### Bounded Multi-Seam Workflow

For approved Workstream execution, bounded multi-seam workflow is the primary execution model.
`Docs/phase_governance.md` owns the exact seam workflow contract; this mode doc mirrors the collaboration posture only.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.

That means:

- prompts may name a seam chain and active seam, but source-of-truth and validation decide continuation
- Branch Readiness should plan the branch objective, target end-state, expected seam families, risk classes, validation contract, User Test Summary strategy, later-phase needs, and first Branch Planning target
- Branch Planning must provide BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, and BP3 Workstream Entry / Orchestration Validation before implementation so USER can accept, revise, defer with waiver, reject, or request more analysis on the readable branch vision and branch plan
- BP3 for a runtime branch with multiple admitted slices or seams must analyze the whole admitted Workstream package before recommending the entry implementation seam. The packet must report all admitted slices/seams, completion strategy, entry-seam recommendation, seam dependency map, future-gated boundaries, preservation surfaces, validation plan, Hardening H1 expectations, Live Validation LV1 expectations, visual/user-facing proof requirements, UTS handoff criteria, and exact implementation approval text that preserves bounded continuation until Workstream Green, a real blocker, or an explicit USER waiver. A first-seam-only packet blocks on `Workstream Entry Whole-Package Analysis Missing`.
- Workstream may execute multiple planned seams in one pass when they share the same workstream, phase, branch class, approved scope, and subsystem family or tightly coupled implementation, validation, or governance chain
- each seam is still analyzed, bounded, executed, validated, recorded, and judged before the next seam starts
- Hardening and Live Validation may continue through constrained validation or evidence-digestion seams only when their phase rules allow it
- PR Readiness uses readiness-gate seams for PR package, PR creation, and PR validation rather than implementation continuation
- Release Readiness is review-only and file-frozen; it must not mutate repository files through a seam
- the output must report the per-seam validation result and `continue` or `stop` decision
- reporting `Next Safe Move` is not a substitute for execution when continuation authority passes
- A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice
- a validation failure, regression, scope drift, unplanned risk expansion, governance drift, unresolved manual-validation blocker, branch-truth contradiction, phase boundary, stop-loss trigger, or other bounded stop condition stops the workflow

Legacy `Single-Seam Fallback` and `Single-Seam Mode Waiver` wording is retired in active source-of-truth.
A bounded stop condition blocks continuation; it does not by itself authorize stopping the backlog item after only one slice.
Bug fixes, hotfixes, unclear seams, high-risk seams, cross-subsystem work, settings, protocol, launcher, and UI-model changes require smaller seams and stronger gates; they do not stop a green approved seam chain unless a blocker is recorded or an explicit waiver narrows the pass to one seam.

Completing Workstream seams does not make the branch PR-ready by itself.
The normal next legal phase is `Hardening`, then `Live Validation`, then `PR Readiness`.

### Milestone Gate

Before treating a non-doc implementation branch as ready, Codex should be able to explain:

- the lane milestone target
- the minimum merge-ready threshold
- the milestone value statement
- the same-branch follow-through that still belongs inside the lane

### Worthwhile Milestone Gate

For a non-doc implementation branch, Codex should not recommend readiness until:

- the threshold is reached
- the branch is still worthwhile if squashed today
- the remaining implementable same-branch slices are no longer required, or only future-dependent blockers remain

### No-Release-Debt Gate

If `main` already contains merged unreleased non-doc implementation work beyond the latest public prerelease, treat that as an exceptional release-handling blocker, not normal branch debt.

While that exceptional blocker exists, the default next move is usually:

- release review
- release prep
- directly needed docs support

not another unrelated implementation lane.

That default blocks the next implementation lane by default unless USER explicitly approves a selected-next runtime path and records the release-handling owner/carrier plan.
It does not authorize a governance-only branch.
Release packaging may begin only when `Docs/phase_governance.md` says that branch class may begin from `No Active Branch`.

If release handling, `Backlog Addition User Approval Missing`, `Backlog Exhaustion User Decision Pending`, or another repo-level admission blocker means no next implementation branch may legally begin execution, report repo state as `No Active Branch` only with the explicit blocker or USER waiver/defer instead of inventing a next implementation phase.
If repo truth is a steady-state `No Active Branch`, say so explicitly instead of pretending a new implementation branch should open automatically.

### Fresh Branch Start After A Closed Workstream

After a workstream is merged and closed, the next implementation workstream should execute from updated `main` on a fresh branch.

During `PR Readiness`, selected-next truth is optional and applies only when USER explicitly approves PR-time selected-next sync or selected-next truth already exists. When it applies, the next workstream must be a real runtime candidate, canon-defined, minimally scoped as a runtime slice, and explicitly not branched yet.

That successor branch is created only during `Branch Readiness` after the current branch merges and updated `main` is revalidated.

Post-merge `No Active Branch` is allowed when no USER-approved selected-next truth exists. That state does not select, create, or admit a successor branch; the next runtime implementation pipeline is chosen later in Branch Readiness Stage 1. If USER approval exists for PR-time selected-next selection but no real runtime candidate can be selected, `Next Runtime Candidate Selection Pending` blocks that selected-next path and the branch stops in PR Readiness.

If a branch is stale, merged, or identical to `main`, call it out explicitly and stop using it as the base for next-lane planning.

### Post-Release Canon Repair

Release-dependent truth must be anticipated before PR green.

When release-dependent truth changes:

- carry the canon sync on the active lane when that lane is still open
- require merge-target canon completeness before PR so merged `main` does not become stale in the first place
- after a public prerelease tag exists, require durable closure: latest public prerelease advances, released workstream moves to Released / Closed, release debt clears, and workstreams index moves the record to Closed
- classify any missed durable closure as a Branch Readiness blocker on the next legal active branch before implementation, not as permission to normalize release debt, stale canon, or cleanup-only branches
- treat architecture-only planning, admission contracts, validation-only work, documentation/canon repair, governance repair, and non-user-facing milestones as `patch prerelease` by default unless a new executable, runtime, operator-facing, user-facing, or materially expanded product capability lane is delivered
- do not use Release Readiness as a docs-sync phase
- do not use Release Readiness as a file-mutation phase; release package information may be generated as response text only
- do not open a governance-only branch or between-branch repair window
- if a PR Readiness miss escapes after merge, block the next legitimate runtime-focused backlog branch in `Branch Readiness` and repair the miss before implementation begins
- do not use direct-main emergency repair; `main` is protected for Codex work and repair must ride the next legitimate runtime-focused backlog branch's `Branch Readiness`

## Shared Rules Across Both Modes

- analyze before changing anything
- anchor phase-sensitive work to the current phase named in `Docs/phase_governance.md`
- do not infer a later phase from user intent alone
- verify exact behavior or doc alignment before editing
- preserve architecture boundaries
- call out source-of-truth conflicts explicitly
- backlog owns identity
- roadmap owns the stage-breakpoint schedule outline, not live release state
- workstream docs own promoted-work feature-state, branch-local evidence, active seam references, artifact history, branch-local reuse notes, and closure history
- `Docs/phase_governance.md` owns repo-wide phase, proof, timeout, seam, stop-loss, validation-helper, and desktop UI audit rules
- `Docs/validation_helper_registry.md` owns durable helper naming, helper status, registry, and consolidation expectations
- User Test Summary belongs to workstream-owned validation
- incident patterns are generalized knowledge, not case history
- governance and canon updates should ride on the active current branch when they are directly required to keep that branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct
- governance-only branches are not used for new Nexus work; tightly coupled governance repair rides on the active runtime-focused branch, and escaped PR misses block the next legitimate runtime-focused backlog branch's `Branch Readiness`
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- The only standing exception is the `Standing Governance Intake Branch`, `feature/release-readiness-source-truth-intake`, at `C:\Nexus Worktrees\Governance`; use it only for a `Release Readiness digest`, USER-approved `automation/worktree governance intake`, or USER-approved `phase-gate governance intake`, assign `RRI-YYYYMMDD-NNN`, enforce operational `One Active Cycle`, apply the clean `Sync Rule` against `origin/main` before intake, keep the originating lane in `Waiting For Governance Intake` or `Waiting For Updated Main`, and send the required post-merge `Return Digest` with exact originating branch, originating worktree, operating workspace, expected branch, and `Neutral Main Workspace Rebaseline:` proof copied from the accepted intake. Merged-main `No Active Branch` means no active runtime, implementation, release packaging, or repair carrier; it may coexist only with this standing governance intake authority record. Do not create a dedicated post-merge closeout PR solely to clear this branch's `Active RRI Cycle` or cycle-ledger wording.
- If Release Readiness discovers stale active branch authority, stale phase wording, stale PR Readiness wording, selected-next ambiguity, release-window contributor ambiguity, or `No Active Branch` conflict after merge, the digest must say `Governance Intake Routing: send this to C:\Nexus Worktrees\Governance on feature/release-readiness-source-truth-intake` and include the originating worktree, branch, PR, merge commit, blockers, and next legal phase.
- The standing governance lane must stop on `Return Digest Origin Identity Missing` rather than infer the originating workspace from `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Governance`, GitHub Desktop's selected repository, or the current shell CWD.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
- active-branch governance updates must not weaken validation, stop conditions, phase authority, branch-class authority, or scope control
- `main` is protected for Codex work; Codex may read `main` for truth validation, but any tracked file mutation, staging, commit, generation, refresh, or direct repair on `main` is a `Main Write Attempt`
- There is no emergency direct-main repair path for Codex.

For desktop workstreams, response-level `## User Test Summary` output and the canonical repo-level `UTS` artifact are related but not interchangeable:

- the response section is the current handoff copy
- the workstream-owned repo artifact is the exact `## User Test Summary` section, not `## User Test Summary Strategy`, unless the workstream explicitly declares another repo path
- the local USER hub `C:\Nexus USER\User Test Summary.txt` file is the required user-facing exported copy when relevant, but it is not the default canonical repo record

If a required User Test Summary handoff is outstanding, `User Test Summary Results Pending` is a hard Live Validation Stage 1 blocker. User Test Summary is exclusive to Live Validation Stage 1. Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated. PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact. Codex must route backward to `Workstream` or `Hardening` if the results expose a mismatch, regression, ambiguity, cleanup issue, or scope drift. For desktop UI Live Validation, Codex must also record `Codex Visual Adjudication:` with `Visual Artifact Review Scope:`, `Product Vision Alignment:`, `Per-Element Visual Verdicts:`, `Helper Marker Limitation:`, `Unacceptable UI Findings:`, and `LV1 Handoff Disposition:`; helper PASS, marker PASS, screenshot existence, and manifest existence cannot replace artifact-by-artifact product-vision judgment. A UTS handoff is invalid while Codex-visible visual or functional `REPAIR` / `STOP` findings remain; those must be repaired and revalidated or explicitly blocked before USER acceptance review.
Live Validation green requires an exact `## User Test Summary` state before final green.

For relevant desktop user-facing workstreams, `User-Facing Shortcut Validation Pending` is a hard blocker before User Test Summary handoff.
Codex may use validators, live helpers, harnesses, or direct runtime launches for scenario coverage, but Live Validation closeout must also run the declared user-facing desktop shortcut or equivalent entrypoint and record `User-Facing Shortcut Path:` plus `User-Facing Shortcut Validation: PASS`, `FAIL`, `PENDING`, or `WAIVED`.
If that shortcut gate fails or remains pending, do not report final green; route back to `Workstream` or `Hardening` as appropriate.

When manual validation is relevant, `## User Test Summary` must be a real checklist rather than a recap.

It should include:

- setup or prerequisites
- exact user actions
- expected visible behavior
- failure signs to watch for
- branch-specific or slice-specific validation focus

For runtime or user-visible implementation slices, green validators alone do not authorize automatic continuation.

When a relevant desktop or runtime path can be launched and exercised through a real desktop session in the current environment, synthetic or headless validation does not authorize continuation on its own either.

Codex must also:

- run a deeper branch-local hardening pass against the implemented path
- add or create the smallest reliable validation infrastructure when meaningful blind spots remain
- preserve an evidence trail of the validators, harnesses, helper scripts, fixtures, runtime logs, traces, screenshots, or other validation artifacts actually used
- clean up test-session side effects such as temporary files, launched apps, helper processes, probe documents, or altered local state unless there is an intentional reason to preserve them
- enforce visible progress and a no-progress supervisor for live validation; if no tighter helper-specific watchdog is active, `10s` without meaningful progress must stop the run and report the last confirmed progress point
- use synthetic or headless validators and harnesses as supporting proof rather than the final gate when a real desktop session is feasible
- launch and exercise the real desktop or runtime path through an interactive OS-level session when feasible
- explicitly distinguish validator results, synthetic or headless validation results, simulated reasoning, interactive OS-level execution results, and manual user-test handoff
- make an explicit next-step call between continue, harden, or corrective fix

When meaningful desktop UI changed, Codex should also:

- treat the live launched-process UI audit as a post-green closeout check rather than a per-seam screenshot requirement
- preserve the audit manifest and key captured windows in the final evidence package when closeout or readiness is being claimed
- when the user wants those screenshots to render inside the Codex client, preserve the original files on disk but default the in-chat preview path to one small inline PNG `data:` image at a time instead of local-path Markdown embeds

If that interactive path is not feasible, Codex must explain why, use the strongest available non-interactive evidence, and state that the continuation judgment is limited by the missing interactive validation.

## Phase Anchoring

Modes define collaboration posture.
Phases define the current governed lifecycle state.

For phase-sensitive work, prompts and execution records should explicitly state:

- `Mode: <mode name>`
- `Phase: <exact phase name>`
- `Workstream: <workstream id or authority record>`
- `Branch: <branch name or No Active Branch>`

When a branch is in governed closeout recovery, prompts should also state:

- `Branch Class: <branch class>`
- `Current active seam: <seam name>`
- `Validation Contract: <summary or authority reference>`
- `Timeout Contract: <summary or authority reference>`

If `Phase` is missing or is not one of the exact canonical phase names from `Docs/phase_governance.md`, execution must stop at truth-validation or analysis.

## Live-State Readiness Sanity Check

Before generating any readiness, PR, merge, or release recommendation, validate:

- current branch truth
- branch merge state
- tag or release state
- dirty worktree risk
- whether the prompt framing is stale

If the framing is stale, report the real state instead of producing a hypothetical package.

## Prompt Hygiene

When a canonical workstream or rebaseline doc exists, prompts should prefer that canonical doc over a stack of superseded slice docs.

This does not mean shrinking analysis depth.
It means reducing duplicated prompt inputs once authority is clear.

## Practical Rule Of Thumb

If the user is asking:

- what is true now
- what drift exists
- what should happen next
- whether the current branch is still the right base

start in Analysis mode.

If the user is asking:

- execute this approved docs-only phase
- implement this approved patch
- carry this approved workstream closure or canon sync

use Workflow mode.
