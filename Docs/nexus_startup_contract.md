# Nexus ChatGPT Loader Prompt Contract

## Purpose

This document is the ChatGPT-facing loader prompt contract for Nexus Desktop AI chats.

Use it to generate new-chat, handoff, continuation, bootstrap, review, and Codex-prompt requests without pasting the full governance stack into the prompt body. It is an interface and prompt-loader layer only.

Generated prompts must preserve the Main-first loader chain: load `Docs/Main.md` first, then load `Docs/nexus_startup_contract.md` when loader/new-chat continuity, prompt generation, bootstrap continuity, handoff continuity, continuation continuity, loader alignment, or ChatGPT/Codex behavior alignment is in scope, then follow Main to the directly relevant owner docs.

`Docs/nexus_startup_contract.md` does not replace the owning canon documents and does not own Codex execution behavior, phase transitions, seam continuation, durability, validation, release rules, branch authority, or stop conditions. Codex execution authority comes from `Docs/Main.md` and the owning source-truth documents after they are loaded.

Local ChatGPT custom instructions should stay compact. This repo loader may hold longer ChatGPT-facing continuity rules and prompt-generation guardrails, but it must remain a routing contract rather than a duplicate governance system.

Do not paste this loader doc into Codex prompts. Codex prompts should load `Docs/Main.md` and the owning canon for execution authority, using this loader only when prompt generation, new-chat bootstrapping, handoff continuity, or loader/source-truth drift review is actually in scope.

Nexus project direction remains Windows-first, modular, GPU-aware, privacy/local-first where practical, lean by default, and capable of optional heavy local AI capability packs while preserving CPU fallback unless current source truth changes that direction.

## Authority Boundary

Repo source truth governs. Chat memory, uploaded packets, helper output, validator output, plugin output, connector output, prior Codex summaries, and ChatGPT analysis are evidence only until reconciled against current repo source truth.

This loader owns prompt shape, loader continuity, and ChatGPT prompt-generation guardrails. It routes exact policy to the current owners:

- `Docs/Main.md` owns source-truth routing, protected-main law, and the Main-first source-truth index.
- `Docs/phase_governance.md` owns phase definitions, blockers, phase transitions, proof hierarchy, Workstream, Hardening, Live Validation, PR Readiness, Release Readiness, and release-boundary law.
- `Docs/development_rules.md` owns execution, validation depth, durability, cleanup, and implementation behavior.
- `Docs/codex_modes.md` owns Codex collaboration posture.
- `Docs/governance_efficiency_operating_model.md` owns source-truth split, external operational state, USER review bundle model, and duplicate-governance prevention.
- `Docs/validation_helper_registry.md` owns helper and validator status, reuse, interpretation boundaries, and evidence handling.
- `Docs/nexus_vision.md`, `Docs/family_visions/`, and approved family-feature vision owners own project/family/product direction.
- `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` owns active external branch planning, USER feedback disposition, branch-local engineering detail, and active planning ledgers.
- Branch records, workstream records, backlog, roadmap, and worktree-slot docs own only the durable record classes Main assigns to them.

If this loader conflicts with Main or an owning canon file, Main and the owner win. Repair this loader through the legal carrier and phase rather than treating the conflict as an execution shortcut.

## Main-First Load Chain

Every repo-affecting Codex prompt must say, in substance:

1. Load `Docs/Main.md` first.
2. Load `Docs/nexus_startup_contract.md` for loader/new-chat continuity when prompt generation, handoff, continuation, bootstrap, loader alignment, or ChatGPT/Codex behavior alignment is in scope.
3. From Main, load the relevant execution, phase, branch, workstream, vision, validation, external-state, and artifact owners.
4. Treat context docs and review packets as evidence unless Main routes them as source-truth owners.

When vision context matters, route through `Docs/nexus_vision.md`, `Docs/family_visions/`, approved family-feature vision owners when applicable, and the active external branch plan at `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`.

Context docs may explain, summarize, or point to owner docs. They must not become alternate first loaders, duplicate detailed policy, or override Main.

## New-Chat / Handoff Prompt Requirements

Every Nexus new-chat, handoff, continuation, bootstrap, or loader-alignment prompt should include:

- worktree path, expected branch, target phase, approved scope, pending USER decisions, and next legal phase as known evidence to verify
- Main-first loading and startup-contract loading when loader continuity is in scope
- source-truth owner loading routed by Main
- identity preflight for git root, branch, upstream, `HEAD`, `origin/main`, merge base, cleanliness, worktree role, write target, and current phase
- freshness preflight before mutation or phase continuation
- approval-state and blocker-state checks before acting
- validation expectations routed to the validation registry and phase owner
- stop/report conditions for missing source truth, stale `origin/main`, wrong worktree, wrong branch, unclear phase, unclear approval, validation failure, or scope drift

Prompt templates should keep exact live branch facts in the Codex digest or external operational state, not in USER-facing review files.

## ChatGPT Review And Prompt-Generation Duties

ChatGPT's role is repo-state analysis, drift detection, governance review, Codex prompt generation, and Codex-output review. Codex executes. Repo source truth governs. Codex output is evidence, not authority.

ChatGPT may add evidence checks, review questions, validation reminders, source-truth checks, and candidate blockers for Codex to reconcile against the loaded repository governance files.

ChatGPT must not act as Codex's governing authority by removing, replacing, narrowing, reordering, or prohibiting Codex-planned steps through ChatGPT-authored limiting phrases, restriction lists, or replacement logic. If ChatGPT sees a flaw, stale assumption, unsafe scope, governance mismatch, validation gap, or approval gap, it should surface the issue as an analysis finding with the exact USER decision needed.

## Phase And Stage Progression Discipline

This loader does not define phase law. Load and follow `Docs/phase_governance.md`, `Docs/development_rules.md`, active external branch planning, branch records, and relevant workstream records for exact phase rules.

Prompt generation must preserve stage progression discipline:

- current gate defects block next-stage approval until repaired, waived, or explicitly routed by source truth
- reviewable packet status is not USER acceptance
- Branch Readiness, Branch Planning, Workstream, Hardening, Live Validation, PR Readiness, Release Readiness, and release execution remain separately approved as routed by Main
- Workstream Entry is BP3 inside Branch Planning when current source truth says so
- release execution requires separate explicit USER approval

For Workstream-specific prompt generation, load the current phase owner and preserve its current bounded-continuation markers. Routing phrases that must remain discoverable for validators and prompt review include: Seam Sequence; continue-or-stop; Next-Seam Continuation Required; entry seam, not a terminal boundary; Bounded means one active seam at a time, not one-seam Workstream authority.; A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.; Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.; If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.; Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.; A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.; seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress; there is no repo-wide cap on how many slices a branch or workstream may carry; same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green; continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green; when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`; `Workstream` reaches `Hardening` only when `Completion Status: Green`; green seam or green slice is continuation proof, not Hardening authority; `Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; `Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation; `Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.; Phase Boundary Stop Required; A phase-exit seam named in `Next Active Seam` is a handoff target, not current-phase execution authority.; Bounded Workstream continuation ends at phase boundaries; it never crosses from Workstream into Hardening by inertia.; Codex must not execute Hardening, Live Validation, PR Readiness, Release Readiness, release work, or any other next phase in the same run unless USER explicitly admits that phase after reviewing the handoff.; Backlog Completion State; Backlog-Split User Approval; Backlog-Split Reason.

These phrases are routing and validation anchors. The detailed rule owner remains `Docs/phase_governance.md`.

## Approval And Identity Preflight

Prompt generation should require a preflight before repo-affecting work:

- current worktree path and git root
- current branch and upstream
- current `HEAD`, `origin/main`, and merge base
- clean/dirty state and changed-file scope
- active legal authority owner
- current phase/stage and approved scope
- pending USER decisions
- next legal phase

Generated prompts should request `Bounded State:` before mutation, with exact phase/stage, workspace, branch, write target, authority record, package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase.

If any bounded-state field is missing, stale, or ambiguous, the prompt should stop on `Bounded State Missing`. Widening beyond the current bounded state requires `Bounded State User Waiver: Granted`; otherwise the prompt should stop on `Bounded State Waiver Missing`. Broad work requests do not authorize implementation; broad work requests do not authorize implementation without source-truth resolution to one exact active bounded seam or an explicit waiver.

## Prompt Shape Doctrine

Prompts should be thin, neutral, repo-aligned, evidence-driven, and source-truth based.

Use positive scope framing: current authorization covers, source truth routes, pending USER approval checkpoint, stop and report, exact decision needed, and validation required.

Avoid broad restriction walls, behavior-management lists, and freehand command boxes. Scope limits should come from current repo truth, branch authority, phase owner, active external planning owner, workstream record, and USER approval state.

Prompt-generation output should not leak startup-contract narration into the generated Codex prompt body. The startup contract should load that authority; it should not leak startup-contract narration into the generated Codex prompt body.

## Prompt Wording Scrub

Before outputting a Codex prompt, ChatGPT or any prompt-generation layer should scrub wording into:

- current authorization state
- future USER approval checkpoints
- source-truth facts and owner routes
- phase, branch, worktree, and scope status
- stop/report conditions
- exact USER decisions needed

Rewrite broad `do not`, `not allowed`, `this is not`, `never`, and `forbidden` language into source-truth state, blocker names, pending approvals, or exact stop/report conditions unless quoting durable repo law from the owning canon.

If prompt wording cannot be made source-truth aligned without changing USER intent, report a prompt-generation blocker and ask for the exact USER decision needed.

## Pre-PR Hardening Recommendation

When review risk is high, ChatGPT may recommend a pre-PR hardening or drift pass. Exact PR Readiness, mergeability, bot-review, watcher, PR-comment, release-window, and post-merge rules are owned by `Docs/phase_governance.md`, `Docs/Main.md`, `Docs/pr_watcher_mode_contract.md`, branch records, and validation helpers routed by Main.

source-truth and governance fixes ride real carriers. They do not create standalone repair-only branches by inertia. Use the current legitimate carrier only when source truth and USER approval make it legal; otherwise route the drift to Branch Readiness, Governance intake, release-support, or another owner that Main identifies.

FAM-006 Monitoring and HUD selected-next truth is allowed only after explicit USER approval. Loader recommendations do not authorize a FAM-006 branch, package admission, runtime package, selected-next mutation, or single-slice waiver.

## Connector / Plugin Evidence Handling

Plugin and connector output is evidence, not authority. Generated prompts should request a `Plugin / Connector Use Plan:` when tool evidence affects phase advancement, PR/release decisions, source-truth repair, provider/API setup, private/public boundary work, or USER review proof.

Connector auth/session state, API key state, current PR reactions, current review-thread state, temporary plugin output, and raw docs lookup text must not become repo source truth. GitHub and helper checks may own volatile live facts; durable repo docs should keep owner routing, accepted decisions, and historical receipts only.

## Machine-Check Routing Anchors

This section preserves validator marker phrases as routing anchors. It does not make this loader the owner of the detailed rules. Load and follow Main plus the current owner docs for the live policy.

Feature-branch repair anchors:

- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.

Planning-loop and thin-prompt anchors:

- Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
- Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
- Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
- Docs-only Workstreams require explicit USER approval.
- Planning-Loop Bypass User Approval: APPROVED
- Planning-Loop Bypass Reason:
- Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
- `Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item
- Planning-loop prevention belongs in ChatGPT preflight analysis.
- If planning-loop risk is detected, ChatGPT must block prompt generation and return analysis instead of an execution prompt.
- Once prompt generation is allowed, the prompt stays thin and neutral.
- Codex prompts should express admitted scope positively through project context, active seam, task, and return format.

Package and Element Coverage anchors:

- Single-Slice Package User Approval Missing
- Package Completion Unproven
- Admission State: Admitted
- Element Coverage
- user-facing surface
- runtime/backend behavior
- fail-safe/recovery
- security/privacy
- voice/audio
- external integration
- local AI/capability packs
- packaging/install
- monitoring/HUD
- release impact
- Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers

Branch Planning and runtime-plan anchors:

- Workstream Entry whole-package analysis
- entry-seam implementation
- Workstream Entry Whole-Package Analysis Missing
- USER_BRANCH_VISION_REVIEW.md
- USER_BRANCH_PLAN_REVIEW.md
- USER Branch Plan Review Gate
- Contract Status
- USER Review Response
- BP3 Orchestration Validation Missing
- Branch Readiness Stage 1 - Analysis Gate
- BR1 Candidate Viability / Grouping Matrix
- BR1 Candidate Implementability Missing
- BR1 Candidate Grouping Matrix Missing
- BR1 Planning-Only Candidate Drift
- BR1 Support-Only Candidate Drift
- BR1 Readiness-Only Candidate Drift
- BR1 Manifest-Only Candidate Drift
- BR1 Tiny-Branch Sprawl
- BR1 Feature Vision Context Missing
- BR1 Candidate Split Reason Missing
- Implementation-Bearing Route Unproven
- Post-Merge Release Readiness Handoff
- Post-Merge Release Readiness Decision Missing
- Release Readiness Handoff Skipped
- Branch Readiness Stage 2 - Execution Gate
- Branch Readiness Execution User Approval Missing
- no repository file mutation
- Runtime Branch Engineering Contract
- USER Engineering Planning Review:
- Runtime Implementation Approval:
- Current Runtime Baseline:
- Planned Runtime Delta:
- User-Facing Runtime Delta:
- State / Config / Schema Delta:
- Validator / Helper Delta:
- Workstream Seam Map:
- Proof Expectations:
- Plan-To-Implementation Traceability:
- Branch Runtime Engineering Plan
- local USER hub packet
- backlog and roadmap remain compact pointer/status surfaces

Freshness and PR Readiness anchors:

- Prompt-Entry Origin/Main Freshness Gate
- Prompt-Entry Freshness Check:
- Fetched origin/main:
- Origin/Main Advanced Since Last Action:
- Pre-Rebaseline Impact Audit Required:
- Rebaseline/Reconciliation Status:
- Prompt-Entry Origin/Main Freshness Missing
- Origin/Main Advanced Rebaseline Required
- validating locally is not enough
- PR Readiness Stage 1 - Analysis Gate
- PR Readiness Stage 2 - Execution Gate
- PR Readiness Execution User Approval Missing
- analysis-first blocker repair gate
- PR Readiness Stage 1 Repair Pending
- USER approval to enter Stage 2
- analysis-first readiness-lock gate
- Stage 1 Ready For Stage 2
- PR Readiness Stage 1 Repair Required
- Current-Branch Branch Readiness Re-entry Required
- New Carrier Branch Required
- Stage 1 USER Waiver Required
- Stage 2 begins only after
- Stage 2 sync plan
- Branch Readiness fallback is real carrier branch/package analysis
- PR Readiness does not require selected-next truth or a waiver by default
- direct PR verification
- recurring PR watcher automation
- Direct PR2 Continuation Rule

Release-window and post-merge anchors:

- Release Window Audit
- Release Window Audit Incomplete
- Remaining Known Release Blockers: None
- Another Pre-Release Repair PR Required: NO
- Release Window Split Waiver: None
- post-merge closeout proof must be in merged source truth
- not only in a deleted branch, reflog, automation memory, or conversation transcript
- next real runtime package carrier
- release execution and post-release canon closure are separate
- a local-only post-release closure commit is a blocker
- protected-main branch rejection must route to the next approved Branch Readiness Stage 2 canon/governance repair carrier
- post-release validation must compare published GitHub release/tag truth and release-body format against remote repo source truth
- runtime implementation remains blocked until release publication exists, post-release canon drift is explicitly recorded or repaired through the approved Branch Readiness carrier, and owning validation reports green

Governed output and continuation anchors:

- Seam Status
- Slice Status
- Waiver Status
- Continue Decision
- Continuation Execution Latch
- Stop Basis
- Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation.
- If `Completion Status` is `In Progress` and no named blocker or waiver stops work, the generated prompt must require continuation rather than `Await Next Instruction`.
- Use these governed state markers as execution control, not just reporting.
- If `Continue Decision` is `Continue`, the generated prompt must not let Codex end on a seam-complete final response, rollback path, or next-seam recommendation; it must require continued execution until a lawful `Stop` decision exists.
- reporting Next Safe Move is not a substitute for execution
- continue decision must be acted on immediately by starting the next seam needed inside the current slice
- the prompt `Return:` block describes the lawful-stop report; it is not permission to stop while `Continue Decision` remains `Continue`
- A prompt `Return:` block is an output shape only; it cannot override governed continuation markers or authorize a terminal response while `Continue Decision` remains `Continue`.
- A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
- Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
- Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
- If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
- If `Completion Status` is `Red`, `Continuation Action` must report the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume.
- Treat `Completion Status` as the exact `Phase: Workstream Status` gate after load.

## Output Expectations

Formal next-phase, review, validation, PR, release, or handoff digests must not be compacted. They should preserve required fields, exact blockers, decisions, files, validation status, and next legal phase as routed by Main and the owner docs.

Generated prompts should ask Codex to report:

- source-truth files loaded
- identity and freshness proof
- authority conflicts, stale owners, missing owners, or superseded owners
- changed files, if mutation is approved
- validation commands and results
- commit and push result when applicable
- next legal phase
- exact USER decision text when a decision is required

## Standard New-Chat Prompt Pattern

Use this pattern when generating a new Nexus repo-affecting Codex prompt:

```text
You are Codex acting in the Nexus Desktop AI repo. Repo truth governs.

Load Docs/Main.md first.
Then load Docs/nexus_startup_contract.md for loader/new-chat continuity.
From Docs/Main.md, load the directly relevant source-truth owners for the requested work, including phase governance, development rules, Codex modes, branch/workstream records, active external branch planning under C:\Nexus Governance State when applicable, vision owners, validation registry, helper owners, and any task-specific owner routed by Main.

Before mutation, prove worktree, git root, branch, upstream, HEAD, origin/main, merge base, clean/dirty state, legal authority owner, current phase, allowed scope, pending USER decisions, and next legal phase.

Treat validators, helper output, prior summaries, uploaded packets, and ChatGPT analysis as evidence, not authority.
Act only inside the approved scope. If source truth routes the work elsewhere or freshness cannot be proven, stop and return the exact blocker plus the exact USER decision needed.
```

## Standard Review Prompt Pattern

Use this pattern when asking Codex to review an artifact, packet, prompt, PR, or source-truth change:

```text
Load Docs/Main.md first.
Load Docs/nexus_startup_contract.md if the review concerns loader/new-chat continuity, prompt generation, handoff quality, ChatGPT/Codex behavior alignment, or startup-source-truth drift.
From Main, load the current owner docs for phase, branch, workstream, vision, validation, external state, USER artifact rules, and PR/release behavior.

Inspect the artifact as evidence.
Classify findings against the owner docs.
Separate USER-facing review content from technical proof metadata.
Report accepted, repaired, blocked, stale, conflicting, missing, duplicated, or superseded authority.
Return exact next USER decision text when a decision is needed.
```

## Drift Repair Rule

If this loader contains stale wording, a Main-first contradiction, duplicated detailed governance, or a rule that belongs to another owner, repair this loader through the current legal carrier and phase.

Keep the repair narrow:

- convert duplicate policy into owner-routing language
- preserve required validator marker phrases as routing anchors
- avoid moving live operational state into repo docs
- avoid changing phase law here unless Main routes the change to the owning canon and USER approval covers that broader repair
- keep source-truth and governance fixes on real carriers, not standalone repair-only branches by default

When validation and source truth disagree, diagnose the validator against the owner docs before patching it. Validators and helpers are evidence, not authority.
