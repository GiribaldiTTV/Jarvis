# Nexus ChatGPT Loader Prompt Contract

## Purpose

This document is the ChatGPT-facing loader prompt contract for Nexus Desktop AI chats.

Use it to generate complete new-chat prompts without pasting the full governance stack into the user prompt.
It is an interface and prompt-loader layer only.
It does not replace the owning canon documents, and it must not define or override Codex execution behavior, phase transitions, seam continuation, durability, validation, release rules, branch authority, or stop conditions.

Codex may read this file as a compact loader map, but Codex execution authority comes only from the owning source-of-truth documents after they are loaded.
Local ChatGPT custom instructions should stay compact; this repo loader/source-truth may hold longer ChatGPT-facing continuity rules, review memory, and prompt-generation guardrails.
Do not paste this loader doc into Codex prompts. Codex prompts should load `Docs/Main.md` and the owning canon for execution authority, using this loader only when prompt generation, new-chat bootstrapping, or loader/source-truth drift review is actually in scope.
Generated prompts must preserve the Main-first loader chain: load `Docs/Main.md` first, then the directly relevant owner docs, including `Docs/nexus_vision.md`, `Docs/family_visions/`, `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` for active branch planning, and `Docs/branch_plans/<branch_slug>.md` only when historical repo branch-plan receipts are in scope.
Seam workflow logic is intentionally out of scope for this contract.
When seam behavior matters, route to `Docs/phase_governance.md`, `Docs/codex_modes.md`, and the active workstream record.
When prompt generation recommends Codex plugins or connectors, route plugin/connector authority through `Docs/governance_efficiency_operating_model.md`, `Docs/phase_governance.md`, and `Docs/validation_helper_registry.md`. Generated prompts should ask for a `Plugin / Connector Use Plan:` when tool evidence affects phase advancement, PR/release decisions, source-truth repair, provider/API setup, private/public boundary work, or USER review proof. The prompt must not ask Codex to persist live connector auth/session state, API key state, current PR reactions, current review-thread state, temporary plugin output, or raw docs lookup text as repo source truth.

## Owning Canon

This loader routes to these authorities:

- `Docs/Main.md` owns source-of-truth routing and protected-main law.
- `Docs/development_rules.md` owns implementation, validation, cleanup, and durability expectations.
- `Docs/phase_governance.md` owns phase names, blockers, branch classes, phase transitions, proof governance, and seam-governance rules.
- `Docs/codex_modes.md` owns Analysis and Workflow collaboration posture.
- `Docs/feature_backlog.md` owns tracked work identity and `Record State`.
- `Docs/workstreams/index.md` owns canonical workstream-record routing, including feature-family anchors, historical family-pass records, and other closed trace records.
- live backlog-family IDs use broad `FAM-###`; legacy `FB-###` IDs are historical trace only and must not be reused for new parseable backlog entries.
- canonical backlog identity model is `FAM` broad product family -> `Package` bulk branch/release package -> `Slice` traceable deliverable area -> `Seam` execution/validation checkpoint; PR numbers are evidence only.
- package admission, branch creation, backlog splits, successor promotion, and single-slice package waivers require explicit USER approval; otherwise the loader must preserve the `Backlog Addition User Approval Missing` stop posture and require the not-closed FAM plus not-complete package/slice list.
- only `Admission State: Admitted` slice rows count toward package admission; historical evidence, future placeholders, deferred ideas, and future-package-required rows are trace only.
- named blockers for package drift are `Single-Slice Package User Approval Missing` and `Package Completion Unproven`.
- Element Coverage is a non-identity checklist for user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact; Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.
- Dev Toolkit Interface Review Mode is the repo-wide dev-only inspection standard for USER-facing elements after the tooling is admitted. Existing and future interface elements should be callable or deferred through the owning Element Validation Ledger, with element badges, hover highlighting, ledger ID/name tooltips, and screenshot-friendly annotations available only in Dev Toolkit/dev mode; production UI must not expose element numbers.
- `Branch Readiness` is organized as `Branch Readiness Stage 1 - Analysis Gate` followed by `Branch Readiness Stage 2 - Execution Gate`; Stage 1 requires `## Branch Readiness Stage 1 Analysis Packet`, including product vision, project-wide vision alignment, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, deferred ideas/future-package ledger, and `Branch Readiness Planning Incomplete` blocker review for family/package product work, allows no repository file mutation, branch creation, package admission, docs sync, PR work, release work, selected-next truth, or canon edits, and stops on `Branch Readiness Execution User Approval Missing` until USER approval to enter Stage 2 is recorded.
- Family-package Workstream, Hardening, Live Validation, or PR Readiness entry or continuation is blocked while `Product Vision Input Missing`, `Project-Wide Vision Alignment Missing`, `Branch-Specific Vision Alignment Missing`, `USER Vision Question Packet Missing`, `USER Vision Recommendation Missing`, `USER Vision Questions Unanswered`, `USER Vision Input Pending`, `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, `System Concept Model Missing`, `Entity / Profile Model Missing`, `User Workflow Model Missing`, `Scale / Data Volume Model Missing`, `Configuration And State Model Missing`, `Expected User-Facing Outcomes Missing`, `Codex Additional Recommendations Missing`, `USER Critique Loop Missing`, `USER Decision Ledger Missing`, `Deferred Ideas / Future Package Ledger Missing`, `Planning Adequacy Review Missing`, `Rejected Shallow Plan Missing`, `Alternatives And Tradeoffs Missing`, `Whole-System Interaction Map Missing`, `Minimum Viable vs Full System Boundary Missing`, `Open Questions / USER Decision Points Missing`, `Branch Reach Unproven`, `Feature Element Breakdown Missing`, `Acceptance Criteria Missing`, `User-Facing Proof Standard Missing`, `Current Branch vs Future Package Boundary Missing`, or `Branch Readiness Planning Incomplete` remains active unless explicit USER waiver text is recorded; these are planning blockers, not implementation blockers. When USER input is needed, the question packet must explain each decision with Codex recommendation, rationale, alternatives, tradeoffs, current-branch impact, future-package impact, safe default, waiver/defer posture, and exact response format. When USER needs a durable editable handoff, Codex may generate or refresh a USER-facing `User Vision Input.txt` desktop artifact with accept/change/defer answer paths; the artifact is not repo source truth until a later USER-approved digest pass records completed answers. `Planning Packet Status: Complete` is not valid if broad-package planning uses placeholder or self-assessed values such as `simple`, `basic`, `minimal`, `see above`, or `not applicable`.
- Runtime-focused implementation branches require `## Runtime Branch Engineering Contract` before Branch Planning begins, with `USER Engineering Planning Review:`, `Runtime Implementation Approval:`, `Current Runtime Baseline:`, `Planned Runtime Delta:`, `User-Facing Runtime Delta:`, `State / Config / Schema Delta:`, `Validator / Helper Delta:`, `Expected Changed Files / Surfaces:`, `Approval-Boundary Audit:`, `Future-Gated Items:`, `Workstream Seam Map:`, `Proof Expectations:`, `Risk Forecast:`, `Recommendations And Alternatives:`, `Plan Version / Revision Status:`, and `Plan-To-Implementation Traceability:` so ChatGPT/Codex prompts preserve engineering intent from Branch Readiness through Release Readiness instead of letting Workstream invent shallow deltas. New or re-entering runtime branches also use a Branch Runtime Engineering Plan under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`; backlog and roadmap remain compact pointer/status surfaces while branch-specific per-seam details live in that external plan until PR Readiness fold-down. Branch Planning prompts must require a local USER hub packet under `C:\Nexus USER\<label>` with matching timestamped `C:\Nexus USER\<label>-YYYYMMDD-HHMMSS.zip`, root `START_HERE.md`, exactly one primary current-gate decision file under `USER Review`, generated supporting digests/checklists under `Review Aids`, and copied branch vision, active external branch plan or historical repo receipt, branch authority, relevant Nexus/family vision, matrix, UFD/change-intent, and source-truth context under `Source Truth Context` before asking USER to green-light implementation. Prompts must require BP1 `USER_BRANCH_VISION_REVIEW.md`, BP2 `USER_BRANCH_PLAN_REVIEW.md`, and BP3 Workstream Entry / Orchestration Validation, and preserve `BP1 Branch Vision Review Missing`, `BP2 Branch Plan Review Missing`, `BP3 Orchestration Validation Missing`, `USER Review Packet Stale`, and `USER Review Packet Not Digested` blockers when review files, USER response, Codex digest, scope dispositions, exact USER decision, or `USER Review Packet Finding:` are missing or stale. When multiple slices or seams are admitted, prompts must also require Workstream Entry whole-package analysis before entry-seam implementation and preserve `Workstream Entry Whole-Package Analysis Missing` as a blocker.
- Branch Planning reinforcement: prompts must require `USER_BRANCH_VISION_REVIEW.md` as the BP1 Branch Vision Contract and `USER_BRANCH_PLAN_REVIEW.md` as the BP2 Branch Plan Contract so USER can inspect branch vision and engineering plan before implementation approval. The named BP2 checkpoint is the `USER Branch Plan Review Gate`, and packets must expose `Packet Reviewability State`, `USER Gate State`, `USER Review Response`, and Codex digest proof or an explicit waiver. Prompts must treat Draft, Pending USER Response, Pending Codex Digest, and Pending USER Confirmation Contract Status values as implementation blockers; only Complete or Waived by USER plus accepted/waived USER gate proof can unlock BP3, and BP3 approval still requires a separate USER implementation decision before Workstream. If USER feedback changes direction, UI behavior, workflow, scope, boundaries, or seam order, prompts must require source-truth updates, local USER hub packet/ZIP refresh, and USER confirmation of the revised contract or explicit waiver. Prompts must not turn the review into a per-slice decision packet; SLC/slice/seam details are only implementation staging after the end-state is clear.
- Completed USER input digests may add package-specific planning blockers such as legacy product-name drift, telemetry provider selection, polling floor, warning modality, external telemetry privacy model, cross-family audio approval, and persona/model switching scope; Workstream must not resume until Branch Readiness revalidates, defers, or waives those blockers. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.
- Candidate-only family-package planning is incomplete. ChatGPT should surface candidate-only scope, future deferrals, provider path, polling posture, warning modality, privacy model, naming/product-copy handling, acceptance criteria, or proof standards as a Branch Readiness planning blocker until Codex finalizes them in source truth and Stage 1 revalidates.
- `PR Readiness` is organized as `PR Readiness Stage 1 - Analysis Gate` followed by `PR Readiness Stage 2 - Execution Gate`; Stage 1 is an analysis-first readiness-lock gate that requires `## PR Readiness Stage 1 Analysis Packet`. `PR Readiness Stage 1 Repair Pending` blocks Stage 2 whenever Stage 1 finds repairable PR-readiness drift/blockers that are not repaired, validated, committed, and pushed on the current branch under a USER-approved legal current-branch repair seam. Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection, rooted in Nexus Vision, family vision, branch vision, current completed work, and the next implementation need. PR Readiness does not require selected-next truth or a waiver by default; Stage 1 owns repair or validation of selected-next truth only when USER explicitly approves PR-time selected-next sync or selected-next truth already exists and would merge as durable repo truth. Stage 1 also owns merge-target `No Active Branch` projection, no-release-debt posture, any unavoidable merged-unreleased release-debt owner contract, and active-branch-authority cleanup when it finds them. Stage 1 must analyze release-debt impact, release-debt handling status, required current-branch source-truth sync, Stage 2 sync plan, Stage 2 execution plan, PR title/base/head/summary, watcher plan, blockers, and USER decisions. Stage 1 remains active until one outcome is recorded: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`. Stage 2 begins only after `Stage 1 Ready For Stage 2` plus explicit USER approval and owns final PR execution only: verifying durable Stage 1 projection, commit/push only for bounded operator metadata if legally needed, PR creation, watcher provisioning, bot-review handling, mergeability validation, and merge-watch. Stage 1 still cannot create a PR, provision a watcher, create a branch, admit a package, waive single-slice rules, create a tag, create release artifacts, draft or publish a GitHub Release, or execute a release. Stage 1 may encode selected-next truth only when USER explicitly approves selected-next sync, and branch creation plus runtime package admission must stay blocked for Branch Readiness. It stops on `PR Readiness Execution User Approval Missing` until USER approval to enter Stage 2 is recorded.
- `PR Readiness Stage 2` must retain the same-PR Codex bot-review repair loop and watcher runtime-proof boundary before final handoff: Stage 2 final handoff cannot be green until bot-review closeout is verified, and Stage 2 final handoff cannot be green until watcher runtime proof is present or the runtime-proof blocker remains active. When a live Codex-created PR is waiting on `Bot Review Signal Pending`, Codex must provision or update a PR watcher before handoff; the watcher must inspect bot reactions/comments/threads, post exactly one PR conversation nudge for the current head SHA if no Codex bot comment or thumbs-up/approval signal appears after at least two minutes, and be authorized to perform bounded same-PR repairs for valid Codex bot comments inside the approved PR scope, then validate, commit, push, and report closeout. Out-of-scope bot requests must be reported as blockers. Watcher configuration is not runtime proof.
  This preserves the existing analysis-first blocker repair gate inside the readiness lock.
- PR Readiness Stage 1 may include a no-work `## Next Branch Pre-Plan` gate only when USER asks PR Readiness for successor-selection analysis or selected-next truth already exists. Normal next-branch package-shape proof belongs to Branch Readiness Stage 1. `Next Branch Package Shape Unproven`, `Single-Slice Branch Drift Risk Unresolved`, and `Family Organization Drift Risk Unresolved` block Stage 1 continuation only for USER-approved PR-time selected-next truth or already-encoded selected-next truth that would merge as durable repo truth.
- PR Readiness Stage 1 must also audit the governance/source-of-truth ledger. Identity model drift, FAM taxonomy drift, package/branch rule drift, USER approval blocker drift, real-carrier routing drift, branch-authority lifecycle drift, watcher/automation proof drift, release readiness/execution boundary drift, Element Coverage misuse, ChatGPT loader/source-truth drift, project direction drift, current workflow drift, after-release workflow drift, or absolute-guardrail drift that cannot be cleared as bounded current-branch PR Stage 1 repair requires `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required` according to legal carrier ownership. Branch Readiness fallback is real carrier branch/package analysis and the normal owner of next runtime implementation pipeline selection.
- post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript; if missing proof blocks a release and the branch has not merged, return to PR Readiness, and if the branch has already merged, route it through the next real runtime package carrier's Branch Readiness before implementation begins.
- Merge-target post-merge-stable authority projection is mandatory before PR green and is a PR Readiness Stage 1 repair responsibility when Stage 1 finds it. `Merge-Target Authority Projection Unproven` blocks Stage 2 and PR green when the PR branch would merge an active branch authority record into `main`; the active authority record must be moved to historical/no-active posture or otherwise made merge-stable during Stage 1 before Stage 2 can execute. Post-merge `No Active Branch` does not require selected-next waiver truth when no USER-approved selected-next truth exists; normal successor selection waits for Branch Readiness Stage 1. Historical branch records must not retain active PR Readiness phase, active seam ownership, live/open PR wording, merge-watch ownership, or `PR Merge Verification Pending`. This loader is ChatGPT-facing continuity memory only; Codex execution authority remains `Docs/Main.md` and owning repo canon.
- source-truth and governance fixes ride real carriers: no direct-main repair, no standalone cleanup branch by default, release-support carrier when release is the blocked work, runtime package carrier when runtime work is next, and current legal carrier when the drift belongs there.
- FAM-006 Monitoring and HUD selected-next truth is allowed only after explicit USER approval; loader recommendations do not authorize a FAM-006 branch, package admission, runtime package, or single-slice waiver.
- release execution requires separate explicit USER approval; tag creation, GitHub Release draft/publication, and release artifact creation remain blocked until that approval is recorded.
- release execution and post-release canon closure are separate; post-release canon drift must land in remote source truth through the approved Branch Readiness carrier before implementation begins.
- a local-only post-release closure commit is a blocker, not completed source truth; protected-main branch rejection must route to the next approved Branch Readiness Stage 2 canon/governance repair carrier.
- post-release validation must compare published GitHub release/tag truth and release-body format against remote repo source truth.
- runtime implementation remains blocked until release publication exists, post-release canon drift is explicitly recorded or repaired through the approved Branch Readiness carrier, and owning validation reports green.
- runtime work starts only after release publication and canon closure both land and validate; FAM-006 Monitoring and HUD selected-next truth requires explicit USER approval, and branch creation plus runtime package admission remain separately blocked until later Branch Readiness approval.
- generated prompts should require `Thread / Worktree Identity Preflight` plus `Thread Launch / Write-Target Identity Lock` before Stage 2, phase entry, branch/worktree creation, commit, push, PR work, release work, meaningful repo work, file mutation, runtime validation, shortcut mutation, provider/model installation, or GitHub Desktop handoff; the preflight verifies current working directory, git root, branch, upstream, `HEAD`, `origin/main`, `git worktree list`, clean/dirty state, workspace role, expected phase/seam, intended write target, runtime/process ownership, and GitHub Desktop folder binding when relevant, and stops on `Thread / Worktree Identity Mismatch` with a routing packet when the thread is in the wrong folder, branch, lane, or write target
- generated prompts should require the `Prompt-Entry Origin/Main Freshness Gate` before any new or resumed repo-affecting Codex pass, including post-PR-merge handoffs, phase work, validation-green claims, PR/merge/release work, runtime work, and branch/worktree mutation. The prompt should request `Prompt-Entry Freshness Check:`, `Fetched origin/main:`, current worktree, current branch, `HEAD`, `origin/main`, merge base, `Origin/Main Advanced Since Last Action:`, `Pre-Rebaseline Impact Audit Required:`, and `Rebaseline/Reconciliation Status:`. If `origin/main` advanced or cannot be proven current, the executing assistant must stop on `Prompt-Entry Origin/Main Freshness Missing` or `Origin/Main Advanced Rebaseline Required` before mutation or phase continuation; validating locally is not enough.
- generated prompts for execution must require `Bounded State:` before mutation, with exact phase/stage, workspace, branch, write target, authority record, package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase; if missing, the task stops on `Bounded State Missing`
- broad work requests do not authorize implementation; generated prompts must not treat `continue`, `complete all`, `all remaining work`, `finish the branch`, or similar wording as executable unless source truth resolves it to one exact active bounded seam
- widening beyond the current bounded state requires `Bounded State User Waiver: Granted`; without explicit USER waiver text naming the branch/worktree, phase, slice/seam, relaxed bound, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions, the task stops on `Bounded State Waiver Missing`
- generated prompts for assigned parallel worktree mode must name the assigned thread/worktree owner, expected branch, expected path, intended write set, source-truth owner, branch health markers, file health markers, runtime/interactive-validation owner, Git operation owner, and GitHub Desktop binding rule; the default limit is two active branch worktrees, and overlap or unknown ownership stops on `Parallel Worktree Coordination Missing`
- generated prompts may declare an assigned lane as `Waiting For Updated Main` when it is in Release Readiness analysis, Branch Readiness Stage 1 analysis, or another file-freeze analysis posture with no created branch yet; such prompts must keep the lane read-only until the required merge lands in `origin/main` and a new preflight confirms the next legal action
- local Nexus workspace prompts should treat `C:\Nexus Desktop AI` as the local main/consolidator workspace by default after workspace reconsolidation and as an active branch workspace only when current branch authority plus identity preflight assign it, `C:\Nexus Worktrees\` as the governed local active-branch worktree root, D-drive repo/worktree folders as fallback or historical unless current preflight assigns them, `D:\Nexus Dev ORIN\` and `D:\Nexus Artifacts\` as private/dev or artifact roots whose contents are evidence only until legally imported, and `codex/ai-llm-lab` as historical AI Lab planning traceability with no active local/remote branch ref unless USER-approved repo governance recreates or imports it
- Nexus project direction remains Windows-first, modular, GPU-aware, privacy/local-first where practical, with a lean default install, optional heavy local AI capability packs, preferred GPU use for supported model workloads, and CPU fallback preserved.
- the active workstream doc owns branch-local phase truth, evidence, blockers, and next legal phase for promoted work.
- `Docs/incident_patterns.md` owns generalized recurring drift or validation lessons.
- `Docs/validation_helper_registry.md` owns durable helper naming, status, reuse, and consolidation obligations when helpers are in scope.

This file owns loader prompt shape only.
If this loader and an owning canon document conflict, live repo truth plus the owning canon document wins.
Repair this loader later if it drifted.

## ChatGPT-To-Codex Prompt Addition And Review Neutrality

ChatGPT's role is repo-state analysis, drift detection, Codex prompt generation, and Codex-output review. Codex executes. Repo source truth governs. Codex output is evidence, not authority.

ChatGPT may add analysis steps, evidence checks, review questions, validation reminders, source-truth checks, and candidate blocker checks for Codex to reconcile against the repository governance files loaded in the Codex prompt.

ChatGPT must not act as Codex's governing authority by removing, replacing, narrowing, reordering, or prohibiting Codex-planned steps through ChatGPT-authored limiting phrases, restriction lists, or replacement logic.

When ChatGPT sees a flaw, stale assumption, missing step, unsafe scope, governance mismatch, blocker risk, source-truth drift, validation gap, or approval gap, ChatGPT should elevate the concern as an analysis finding or candidate blocker. The finding should include enough detail for USER review and should identify any USER decision needed.

USER approval is required before Codex is asked to change repo source truth, change an approved plan, drop a planned step, widen scope, grant a waiver, create or admit a new FAM/package, or treat a ChatGPT finding as an execution change.

Preferred ChatGPT prompt-framing pattern:

- preserve Codex's outlined steps
- add missing analysis/review steps when useful
- identify suspected flaws as candidate blockers or analysis findings
- provide evidence and decision context for USER review
- ask Codex to reconcile the plan against loaded repo governance
- let repo governance and USER approval determine execution

Prompts should favor neutral scope language such as `Codex should analyze`, `choose the best path`, `update what is needed`, and `report repair candidates`. Safety boundaries should be stated as repo-truth facts and USER-approval boundaries, not as broad ChatGPT-authored command boxes.

ChatGPT Project Settings may carry a compact form of this rule, but Project Settings text must remain below 8,000 characters. This character limit applies only to ChatGPT Project Settings / custom instructions. It does not apply to this repo loader/source-truth file.

## Nexus Prompt Gate

Before outputting a Codex prompt, ChatGPT or any other prompt-generation layer must run a final Nexus Prompt Gate.

The gate rewrites boundaries as:

- current authorization state
- future USER approval checkpoints
- source-truth facts
- phase, seam, branch, and worktree status
- stop/report conditions
- exact USER decisions needed

The gate must mechanically scrub broad command-box wording before prompt output. Flag and rewrite:

- standalone `do not` phrasing when it creates a broad negative boundary list instead of a current authorization or future approval statement
- standalone `this is not` framing when it defines scope by negation instead of source-truth state
- standalone `not allowed` phrasing when it can be expressed as a pending USER approval checkpoint, blocker, or stop condition
- standalone `never` phrasing unless it quotes durable repo law from an owning canon document
- standalone `forbidden` phrasing unless it quotes durable repo law from an owning canon document
- broad negative boundary lists that read like a command wall
- command-box restriction walls that replace source-truth routing, blocker names, or approval-checkpoint language

The gate preserves hard repo law when the owning canon requires it. Durable rules such as protected-main law, phase blockers, branch-prefix law, release file-freeze, and USER approval checkpoints should be stated as source-truth facts with the owning document or blocker name where practical.

Preferred prompt wording uses phrases such as `current authorization covers`, `future USER approval checkpoint`, `source truth records`, `surface before continuing`, `stop and report`, `preserve separation from`, and `exact decision needed`.

If a generated prompt cannot pass the Nexus Prompt Gate without changing USER intent, the prompt should report the conflict as a prompt-generation blocker and ask for the exact USER decision needed rather than outputting an ambiguous command wall.

## Loader Contract

When ChatGPT or another interface layer generates a Nexus prompt, the generated prompt must require the executing assistant to:

1. Read `Docs/Main.md`.
2. Read `Docs/development_rules.md`.
3. Read `Docs/phase_governance.md`.
4. Read `Docs/codex_modes.md`.
5. Read `Docs/nexus_startup_contract.md` only as a ChatGPT/new-chat loader map when prompt generation, bootstrap continuity, or loader/source-truth drift review is in scope.
6. Load the directly relevant authority docs for the task.
7. If the task maps to a tracked item, load `Docs/feature_backlog.md` and determine its `Record State`.
8. If the tracked item is `Promoted` or `Closed`, load its canonical workstream doc from the backlog and `Docs/workstreams/index.md`.
9. If the tracked item declares a `Lifetime Dossier Doc`, or if it is a `Feature Family` anchor or historical family-pass trace row routed through a family dossier, load that dossier too.
10. If helpers, validation scripts, live-validation harnesses, or shared support are in scope, load `Docs/validation_helper_registry.md`.
11. If drift, recurrence, release correction, or governance repair is in scope, load `Docs/incident_patterns.md`.
12. Validate current repo truth before acting:
    - current branch
    - branch cleanliness and tracked-file mutations
    - whether the branch is the legal execution base
    - current phase from the authority record
    - phase status
    - branch class
    - blockers
    - next legal phase
13. State the startup assessment before narrowing scope:
    - `Source-of-Truth`
    - `Record State`
    - `Branch Truth`
    - `Canonical Workstream`
    - `Reuse Baseline`
    - `Next Safe Move`

If any required file cannot be read, any authority owner is ambiguous, or live repo truth contradicts the requested phase or branch, the generated prompt must tell the executing assistant to stop and report the conflict.

## Authority Model

- Backlog defines identity and `Record State`; it does not own full execution history.
- Roadmap defines sequencing and release posture; it does not override workstream phase truth.
- Workstream docs own promoted-work feature-state, branch-local evidence, phase truth, blockers, active seam references, artifact history, and closure history.
- Phase governance owns phase definitions, blockers, proof hierarchy, branch classes, and phase transitions.
- Development rules own validation depth, cleanup, runtime evidence, helper reuse, and pre-PR durability behavior.
- Codex modes define Analysis versus Workflow posture.
- Incident patterns are reusable lessons, not case-history authority.
- `main` is protected for Codex work and may be read but not mutated.
- Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
- Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
- For user-facing family/package branches, Branch Readiness must declare an `Interface Release Boundary` and `Primary Interface Release Surface:` before Workstream begins or resumes. One primary user-facing interface release surface per branch is the default; multiple released interfaces require explicit `Interface Bundle User Approval: Granted`. This limits interface-release sprawl while preserving bounded multi-seam/multi-slice Workstream execution inside the approved interface boundary.
- Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
- Docs-only Workstreams require explicit USER approval.
- Planning-loop bypass requires `Planning-Loop Bypass User Approval: APPROVED` and `Planning-Loop Bypass Reason:`.
- Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.

Do not create parallel governance systems.
Add narrow routing pointers here, and put detailed policy in the owning canon document.

## Phase Rules

Use only the canonical normal phases from `Docs/phase_governance.md`:

- `Branch Readiness`
- `Workstream`
- `Hardening`
- `Live Validation`
- `PR Readiness`
- `Release Readiness`

`No Active Branch` is repo state, not a normal phase. `Post-Release Canon Repair` is not a normal phase or standalone branch lane.

Phase-sensitive prompts and outputs must identify:

- `Mode`
- `Phase`
- `Workstream`
- `Branch`
- `Branch Class` when branch-sensitive
- `Implementation Delta Class` when an implementation branch is in `Branch Readiness`, `Workstream`, `Hardening`, `Live Validation`, or `PR Readiness`
- `Docs-Only Workstream` when an implementation branch is in `Branch Readiness`, `Workstream`, `Hardening`, `Live Validation`, or `PR Readiness`
- `Planning-Loop Bypass User Approval` and `Planning-Loop Bypass Reason` whenever a docs-only implementation lane is being requested
- `Active Seam` when seam-sensitive
- `Validation Contract` when validation-sensitive

The generated prompt must not infer a later phase from user intent.
If the requested phase conflicts with the authority record, it must require the executing assistant to stop and report `Prompt Phase Mismatch` or the closest canon blocker.

## Loader Validation Requirements

Generated prompts must require default startup validation:

- `git status --short --branch`
- current branch check
- authority-record phase check
- `python dev\orin_branch_governance_validation.py` when repo governance truth is in scope
- `git diff --check` after edits

Additional validation is phase- and workstream-specific and must be read from the active workstream doc and `Docs/phase_governance.md`.
This file does not own those execution validation rules.

For historical docs/governance-only records, which are traceability-only rather than a future repair path, validation must include:

- governance alignment check against owning canon
- duplication check so the new doc routes rather than re-owning detailed policy
- conflict check against phase governance, protected-main law, and durability rules
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.

## Loader Stop Conditions

Generated prompts must include stop instructions for these conditions:

- `Docs/nexus_startup_contract.md` or a required owning canon document cannot be read.
- current branch truth is unclear.
- the requested branch is not the checked-out branch and switching/creating it is not authorized by canon.
- the requested phase does not match the authority record.
- the workstream `Record State` is missing or contradictory.
- `main` would need file mutation.
- `Release Readiness` would need file mutation.
- repo truth is `No Active Branch` with unresolved blockers.
- validation fails.
- implementing the task would require runtime/product work outside the approved phase.
- seam workflow policy would need to be defined or redesigned during a pass that explicitly excludes seam workflow logic.

## Loader Output Expectations

Generated prompts for startup-sensitive passes should request:

- `Source-of-Truth`
- `Record State`
- `Branch Truth`
- `Canonical Workstream`
- `Reuse Baseline`
- `Active Seam` when applicable
- `Seam Status`
- `Slice Status`
- `Completion Status`
- `Blockers`
- `Waiver Status`
- `Continue Decision`
- `Continuation Execution Latch`
- `Stop Basis`
- `Validation Results`
- `Ready-To-Commit Decision` when files changed
- `Next Legal Phase`
- `Next Safe Move`

Generic `Results` or `Validation` headings are not enough by themselves for governed execution output.
A green seam does not authorize stop while `Slice Status` remains non-green.
A green slice does not authorize stop while `Completion Status` remains non-green.
A green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice.
If `Completion Status` is `In Progress` and no named blocker or waiver stops work, the generated prompt must require continuation rather than `Await Next Instruction`.
Use these governed state markers as execution control, not just reporting.
If `Continue Decision` is `Continue`, the generated prompt must not let Codex end on a seam-complete final response, rollback path, or next-seam recommendation; it must require continued execution until a lawful `Stop` decision exists.
A prompt `Return:` block is an output shape only; it cannot override governed continuation markers or authorize a terminal response while `Continue Decision` remains `Continue`.
A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
`Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.
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
Treat `Completion Status` as the exact `Phase: Workstream Status` gate after load.

When a pass creates or changes files before `PR Readiness` and validation is green, generated prompts must point to the Pre-PR Durability Rule in `Docs/development_rules.md` and `Docs/phase_governance.md`.
This loader does not own durability behavior.

## Standard Loader Prompt Pattern

Use this pattern to start a new chat without exceeding prompt limits:

```text
You are continuing the Nexus Desktop AI project.

Mode: <Analysis / Workflow>
Phase: <canonical phase or analysis-only>
Workstream: <FB-XXX or No Active Branch>
Branch: <branch name>
Branch Class: <implementation / release packaging / historical repair context only as canon allows>

First, read as a loader map only:
- Docs/nexus_startup_contract.md

Then load the owning canon documents it points to:
- validate current repo truth
- validate current branch, phase, record state, canonical workstream, blockers, and next legal phase
- stop if the loader cannot be read, if owning canon cannot be read, or if repo truth contradicts this prompt

Task:
<bounded task>

Prompt posture:
- use the loader map to validate live repo truth before execution
- if loader validation fails or planning-loop risk remains unresolved, return analysis instead of execution
- keep the prompt thin and neutral; express scope through context, active seam, task, and return format
- let owning canon supply continuation, validation, phase, release, and slice authority after load

Return:
- Source-of-Truth
- Record State
- Branch Truth
- Canonical Workstream
- Reuse Baseline
- Active Seam, if applicable
- Seam Status
- Slice Status
- Completion Status
- Blockers
- Waiver Status
- Continue Decision
- Continuation Execution Latch
- Stop Basis
- Files Changed
- What Was Written or Found
- Validation Results
- Ready-To-Commit Decision
- Next Legal Phase
- If `Continue Decision: Stop`: Next Safe Move
```

Workstream prompt notes for ChatGPT preflight live outside the prompt body and come from owning canon after load:
- validate after each seam and report continue-or-stop
- the prompt-named seam is the entry seam, not a terminal boundary
- Next-Seam Continuation Required means continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green
- bounded means one active seam at a time, not one-seam Workstream authority
- a single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete
- there is no repo-wide cap on how many slices a branch or workstream may carry
- seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress
- same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green
- when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
- `Workstream` reaches `Hardening` only when `Completion Status: Green`
- `Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; one green seam or one green slice cannot move the branch to Hardening while admitted branch material remains.
- `Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation
- continue decision must be acted on immediately by starting the next seam needed inside the current slice
- `Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item
- use `Backlog Completion State: In Progress`, `Implemented Complete`, or `Implemented Complete Except Future Dependency` to record whether more same-branch slices are still required
- Backlog-Split User Approval
- Backlog-Split Reason
- reporting Next Safe Move is not a substitute for execution
- continue decision must be acted on immediately
- the prompt `Return:` block describes the lawful-stop report; it is not permission to stop while `Continue Decision` remains `Continue`
- Continuation Execution Latch
- A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
- Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
- Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
- If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
- when continuation remains active, Codex must use commentary/intermediate updates and keep executing instead of ending on a seam-closeout package

## Thin Prompt Discipline

Planning-loop prevention belongs in ChatGPT preflight analysis.
If planning-loop risk is detected, ChatGPT must block prompt generation and return analysis instead of an execution prompt.

Once prompt generation is allowed, the prompt stays thin and neutral.
Prompt text should not include behavior-management lists, protective wording, or freehand `Do not ...` instruction blocks.

Codex prompts should express admitted scope positively through project context, active seam, task, and return format.
Scope limits should come from live repo truth, branch authority, canonical workstreams, and admitted slice records after startup validation rather than from ChatGPT-added restriction language.

Runtime/user-facing progress preference remains enforced before prompt generation during ChatGPT preflight analysis.
When planning and implementation are both canon-legal, ChatGPT preflight should prefer a bounded runtime/user-facing, backend/runtime, or developer-tooling implementation slice that is already admitted by repo truth over planning-only continuation.
If no bounded implementation slice is actually admitted, ChatGPT should return analysis instead of padding the prompt with planning-only control language.
The startup contract should load that authority; it should not leak startup-contract narration into the generated Codex prompt body.
Prompt-generation output must preserve the Main-first freshness handoff: the generated prompt should tell Codex to load `Docs/Main.md`, follow it to `Docs/phase_governance.md`, and run the `Prompt-Entry Origin/Main Freshness Gate` before trusting a branch, phase, PR, merge, release, or local validation claim.

## ChatGPT Prompt Generator Rule

Paste this block into ChatGPT custom instructions when ChatGPT is helping generate Nexus prompts:

```text
When the user asks for a Nexus Desktop AI new-chat prompt, bootstrap prompt, analysis prompt, Branch Readiness prompt, Workstream prompt, PR Readiness prompt, Release Readiness prompt, or similar continuation prompt, run a preflight analysis before generating the prompt.

Use that preflight to verify branch truth, phase truth, repo truth, record state, admitted scope, runtime/user-facing implementation preference, planning-loop risk, backlog-completion state, future-dependent blockers, and whether the requested task belongs in analysis instead of execution.

If preflight detects planning-loop risk, branch ambiguity, runtime-free implementation drift, or repo-truth contradiction, block prompt generation and return analysis instead.

When preflight resolves green, generate a thin loader prompt.
That prompt should tell the new chat to read `Docs/nexus_startup_contract.md` first as a loader map only, load the required owning canon, validate repo/branch/phase/record-state truth before acting, and return analysis if required loader or canon files cannot be read or repo truth contradicts the requested task.

Keep the prompt body thin and neutral.
Do not add behavior-management lists, protective wording, or freehand `Do not ...` instruction blocks to control Codex behavior.

Every generated prompt should include only the task structure needed to anchor work: Mode, Phase, Workstream, Branch, Branch Class when relevant, active seam when relevant, task context, task, and an output format containing Source-of-Truth, Record State, Branch Truth, Canonical Workstream, Reuse Baseline, the governed state markers, Validation Results, and `Next Legal Phase`. Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation. Prompt-generated output instructions must preserve digest non-compaction: do not compact the digest ever, and do not collapse, omit, or replace required digest fields or USER-requested review detail. When Workstream continuation or phase exit matters, include `Backlog Completion State`, `Remaining Implementable Work`, and `Future-Dependent Blockers` from owning canon instead of implying `Hardening` by inertia.
```

## Standard Prompt Templates

### Analysis

```text
You are continuing the Nexus Desktop AI project.

Mode: Analysis
Phase: analysis-only
Workstream: <FB-XXX / No Active Branch / unknown until validated>
Branch: <current claimed branch>

Read first:
- Docs/nexus_startup_contract.md

Use the loader map to load owning canon before analysis. Validate current repo truth, branch truth, phase truth, record state, canonical workstream ownership, blockers, and next legal phase. Keep the pass analysis-only and treat any repo mutation as a routed outcome rather than part of the prompt.

Task:
<analysis task>

Stop if repo truth is unclear, required docs cannot be read, or the requested state conflicts with canon.

Return:
- Source-of-Truth
- Record State
- Branch Truth
- Canonical Workstream
- Reuse Baseline
- Drift Found
- Validation Results
- Next Legal Phase
- Next Safe Move
```

### Branch Readiness

```text
You are continuing the Nexus Desktop AI project.

Mode: Workflow
Phase: Branch Readiness
Workstream: <FB-XXX>
Branch: <branch name>
Branch Class: implementation

Read first:
- Docs/nexus_startup_contract.md

Use the loader map to load owning canon. Validate that the branch is the legal Branch Readiness surface, the workstream Record State is correct, the canonical workstream doc exists, current blockers are explicit, and implementation has not started unless canon already admitted Workstream.

Task:
<Branch Readiness task>

Use owning canon to keep this pass inside Branch Readiness work only: branch legality, blocker closure, branch-truth repair, admitted-slice definition, and readiness evidence.

Stop if branch truth, phase truth, or admission legality is unclear.

Return:
- Source-of-Truth
- Record State
- Branch Truth
- Canonical Workstream
- Reuse Baseline
- Active Seam, if applicable
- Seam Status
- Slice Status
- Completion Status
- Blockers
- Waiver Status
- Continue Decision
- Stop Basis
- Files Changed
- What Was Written
- Validation Results
- Ready-To-Commit Decision
- Next Legal Phase
- If `Continue Decision: Stop`: Next Safe Move
```

### Workstream

```text
You are continuing the Nexus Desktop AI project.

Mode: Workflow
Phase: Workstream
Workstream: <FB-XXX>
Branch: <branch name>
Branch Class: implementation

Read first:
- Docs/nexus_startup_contract.md

Use the loader map to load owning canon. Validate that Workstream is the current phase in the authority record, that branch truth is correct, that blockers are clear, and that the workstream scope and validation contract are explicit.

Task:
<bounded Workstream task>

Use owning canon to derive the admitted implementation slices, active seam, seam sequence, same-branch continuation posture, and validation contract before execution.
Keep the prompt thin: the prompt names the current seam and task, while owning canon supplies continuation, backlog-split handling, and later-phase boundaries after load.

Stop if scope, phase, branch truth, or validation requirements are unclear.

Return:
- Source-of-Truth
- Record State
- Branch Truth
- Canonical Workstream
- Reuse Baseline
- Active Seam, if applicable
- Seam Status
- Slice Status
- Completion Status
- Blockers
- Waiver Status
- Continue Decision
- Stop Basis
- Files Changed
- What Was Written
- Validation Results
- Ready-To-Commit Decision
- Next Legal Phase
- If `Continue Decision: Stop`: Next Safe Move
```

### PR Readiness

```text
You are continuing the Nexus Desktop AI project.

Mode: Workflow
Phase: PR Readiness
Workstream: <FB-XXX>
Branch: <branch name>
Branch Class: implementation

Read first:
- Docs/nexus_startup_contract.md

Use the loader map to load owning canon. Validate branch truth, authority-record phase truth, clean durable branch state, merge-target canon, USER approval for next-workstream selection, `Backlog Addition User Approval Missing` / `Backlog Exhaustion User Decision Pending` state, release-window audit truth, helper retention, PR creation requirements, and PR validation requirements from owning canon.

Task:
<PR Readiness task>

Use owning canon to keep this pass inside PR-readiness packaging, merge-target validation, USER-approved next-workstream selection, release-window audit truth, and PR creation or PR validation evidence.
Report PR Readiness green only when canon and live PR truth both satisfy the gate.

Stop if PR state, branch truth, post-merge canon, USER approval for next-workstream truth, or required validation is unknown.

Return:
- Source-of-Truth
- Record State
- Branch Truth
- Canonical Workstream
- Reuse Baseline
- Files Changed
- Governance Drift Found
- Release Window Audit
- Validation Results
- Ready-To-Commit Decision
- Whether PR Readiness is GREEN
- PR Creation Details operator copy blocks, if package-ready
- Next Legal Phase
- Next Safe Move
```

PR Creation Details are GitHub operator copy, not phase-digest output. GitHub PR bodies and PR Summary copy must not include phase-digest handoff fields such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, or `Stop Basis`; those belong in the surrounding governed Codex/source-truth response.
The standardized GitHub PR body shape is exactly `## Summary`, `## Branch Evidence`, and `## Validation`; `## Summary` is a concise outcome paragraph, `## Branch Evidence` must not repeat it through nested Summary/Purpose/Overview sections, concise branch-specific boundaries are allowed only when they clarify reliable branch truth, and `## Validation` is proof-only. Historical PR normalization preserves available branch evidence inside that shape, removes redundant Summary/Purpose repetition, and uses `Validation was not recorded in the original PR body.` only when the old body lacked validation evidence.

Release-window audit notes for ChatGPT preflight also stay outside the prompt body and come from owning canon after load:
- Release Window Audit
- Release Window Audit Incomplete
- Remaining Known Release Blockers: None
- Another Pre-Release Repair PR Required: NO
- Release Window Split Waiver: None

### Release Readiness

```text
You are continuing the Nexus Desktop AI project.

Mode: Workflow
Phase: Release Readiness
Workstream: <FB-XXX>
Branch: main or release-review branch as canon permits
Branch Class: <release packaging / implementation release-review context / No Active Branch release review, as canon permits>

Read first:
- Docs/nexus_startup_contract.md

Use the loader map to load owning canon. Validate merged repo truth, release-debt owner truth, release target, release floor, version rationale, release scope, release artifacts, and post-release truth from canon.

Task:
<Release Readiness task>

Release Readiness is analysis-only and file-frozen.
Use owning canon to perform merged-state release review only, and if any repo change is needed classify the drift and route it to the legal repair surface instead of widening the prompt.

Stop if release target, scope, artifacts, post-release truth, or file-frozen state is unclear.

Return:
- Source-of-Truth
- Record State
- Branch Truth
- Canonical Workstream
- Reuse Baseline
- Release Target
- Release Scope
- Release Artifacts
- Post-Release Truth
- Validation Results
- Whether Release Readiness is GREEN
- Release Package Details operator copy blocks, if green
- Remaining Blockers
- Next Legal Phase
- Next Safe Move
```
