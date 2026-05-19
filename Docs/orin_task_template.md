# ORIN Task Template

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**
**Release Readiness Candidate Anchor: require `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, and `Candidate Includes Later Governance Repairs:`; default to current fetched `origin/main` unless USER explicitly selects another release target; historical PR merge commits are audit evidence only unless USER selects a historical commit as the release target, and missing anchor fields block as `Release Candidate Anchor Missing`.**
**Release Window Aggregation Ownership: merge order does not decide release ownership; require `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, and `FAM Contributor Routing:` so multiple FAM/worktree contributors in the selected target release as an aggregated release window unless USER selects a narrower target.**

You are working inside the Nexus Desktop AI project as an implementation and analysis partner.

## Authoritative Source Of Truth

Treat the following files as authoritative unless a direct verified implementation-state conflict is found:

- `C:\Nexus Desktop AI\Docs\development_rules.md`
- `C:\Nexus Desktop AI\Docs\Main.md`
- `C:\Nexus Desktop AI\Docs\phase_governance.md`
- `C:\Nexus Desktop AI\Docs\architecture.md`
- `C:\Nexus Desktop AI\Docs\orin_vision.md`
- `C:\Nexus Desktop AI\Docs\feature_backlog.md`
- `C:\Nexus Desktop AI\Docs\orchestration.md`
- `C:\Nexus Desktop AI\Docs\[relevant canonical workstream docs]`
- `C:\Nexus Desktop AI\Docs\[relevant rebaseline or closeout docs]`

If anything in the request conflicts with those docs, call it out explicitly before proceeding.

## Prompt Hygiene

- Use `C:\Nexus Desktop AI\Docs\Main.md` as the routing index for selecting the correct authority baseline.
- The default prompt baseline should usually be `development_rules.md`, `Main.md`, `phase_governance.md`, the directly relevant authority docs, and the evidence inputs needed to validate live truth.
- If a canonical workstream, rebaseline, or consolidated design doc exists for the active question, prefer that authority doc over a stack of superseded slice docs.
- Include prior closeout docs and older slice docs only when they are still materially relevant to the specific task.
- Treat canonical workstream docs as branch-local feature-state, evidence, validation-contract, and active-seam references.
- Treat `phase_governance.md` as the repo-wide authority for phase names, stop-loss rules, proof ownership, timeout governance, validation-helper rules, desktop UI audit rules, and truth-drift enforcement.

Concise prompts are acceptable.
They do not reduce the required depth of analysis.

When ChatGPT is generating a Codex prompt, treat this template as a construction checklist rather than prompt text to paste wholesale.
Planning-loop prevention belongs in ChatGPT preflight analysis; once prompt generation is allowed, keep the prompt thin, neutral, and repo-aligned.
Local ChatGPT custom instructions should stay compact while the repo loader/source-truth may hold longer ChatGPT-facing continuity rules and review memory.
Do not paste `Docs/nexus_startup_contract.md` into Codex prompts; Codex prompts should load `Docs/Main.md` and owning canon for execution authority.
Prompt-generation review must preserve FAM -> Package -> Slice -> Seam, PR evidence-only handling, legacy global FB historical-only handling, single-slice/package-completion blockers, Element Coverage as non-identity, Branch/PR Readiness Stage 1 / Stage 2, next-branch hierarchy review, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and the Windows-first, modular, GPU-aware direction with optional heavy local AI capability packs and CPU fallback.
PR Readiness Stage 1 is the Stage 2 readiness-lock gate. Stage 1 must analyze next-workstream/package hierarchy, release-debt impact, release-debt handling status, selected-next / no-release-debt handling status, ranked runtime FAM candidates, recommended next package or explicit USER waiver, package-size risk, single-slice drift risk, Element Coverage risk, required current-branch source-truth sync, Stage 2 sync plan, PR title/base/head/summary, watcher plan, blockers, and USER decisions before Stage 2 can begin. Stage 1 selected-next/no-release-debt handling is complete only when the next selected branch/workstream is recorded in source truth before PR creation or an explicit USER waiver says no next branch/workstream is selected, release target/floor semantics and Release Window Audit are resolved when relevant, branch-authority cleanup is durable, stale-canon risk is cleared, and any unavoidable release debt has an explicit USER decision, named owner, and real-carrier plan before Stage 2; otherwise Stage 1 must stop on `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required` instead of reporting Stage 2-ready. Allowed Stage 1 outcomes are `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, and `Stage 1 USER Waiver Required`. Bounded Stage 1 repair/sync may mutate durable source truth only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair. Stage 2 begins only after `Stage 1 Ready For Stage 2` plus explicit USER approval and owns final PR execution only: final PR package sync, commit/push if needed, PR creation, watcher provisioning, bot-review handling, mergeability validation, and merge-watch.
Stage 2 owns final PR execution only after the readiness-lock outcome is green. Stage 2 final handoff cannot be green until bot-review closeout is verified. Stage 2 final handoff cannot be green until watcher runtime proof is present or the runtime-proof blocker remains active. Use the same-PR Codex bot-review repair loop for actionable bot comments, and remember that Watcher configuration is not runtime proof.
Automation Observability is a multi-worktree evidence gate, not a source-truth shortcut. When a prompt asks Codex to inspect or act on automations, use `dev/automation_observability_report.py` over Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`; only `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED` findings may enter a bounded repair seam. Lane-sensitive automation prompts must declare a configured cwd and prove the intended worktree, branch, `HEAD`, and `origin/main`; otherwise report `Automation CWD Worktree Mismatch`. USER-approved `automation/worktree governance intake` may use the `Standing Governance Intake Branch` only for non-runtime multi-worktree safety repair, and USER-approved `phase-gate governance intake` may use it only for repeatable non-runtime phase-gate miss prevention, under `RRI-YYYYMMDD-NNN`, operational `One Active Cycle`, `Sync Rule`, `Waiting For Governance Intake`, `Return Digest`, and `Neutral Main Workspace Rebaseline`. The standing Governance branch must not require a dedicated closeout PR solely to clear cycle-ledger wording.

## Current Project State

Version:
[fill in version]

Branch:
[fill in branch]

Mode:
[analysis-only / planning-only / docs-only / patch / review / release-workflow]

Workstream:
[fill in workstream id or authority record]

Phase:
[Branch Readiness / Workstream / Hardening / Live Validation / PR Readiness / Release Readiness]

Branch Readiness Stage:
[Branch Readiness Stage 1 - Analysis Gate / Branch Readiness Stage 2 - Execution Gate / not applicable]

Branch Readiness Stage 2 Approval:
[USER approval to enter Stage 2 recorded / Branch Readiness Execution User Approval Missing / not applicable]

PR Readiness Stage:
[PR Readiness Stage 1 - Analysis Gate / PR Readiness Stage 2 - Execution Gate / not applicable]

PR Readiness Stage 2 Approval:
[USER approval to enter Stage 2 recorded / PR Readiness Execution User Approval Missing / not applicable]

Origin/Main Freshness Check:
[PASS / Origin Main Reconciliation Packet Required / not applicable]

Pre-Rebaseline Impact Audit:
[PASS / Required Before Mutation / not applicable]

No Baseline By Inertia:
[Required - no merge/rebase/fast-forward/branch switch before audit report and USER approval / not applicable]

Incoming Main Change Set:
[commit range, PRs, merge commits, and summary of incoming origin/main changes / not applicable]

Incoming Changed Files:
[complete incoming file list from current HEAD or branch creation base to origin/main / None]

Incoming Runtime / Source-Truth Risk:
[runtime/provider/UI/source-truth/validator/shared-surface risk classification / None]

Validation Before Rebaseline:
[read-only validation results or explicit reason validation could not run before mutation]

Recommendation Only:
[findings reported only; no local branch state mutation yet / not applicable]

Rebaseline Mutation Approval:
[Pending / USER approved exact worktree, branch, target commit, and operation type / not applicable]

Rebaseline Mutation Status:
[Not started / Blocked / Approved and completed with operation proof / not applicable]

Branch Creation Base:
[fill in branch creation base commit or not applicable]

Current origin/main:
[fill in current origin/main commit]

Origin/Main Advanced Since Branch Creation:
[YES / NO / unknown]

Origin/Main Changed Files:
[complete file list from branch creation base to origin/main / None]

Branch Changed Files:
[complete file list from branch creation base to HEAD / None]

Reconciliation Required:
[YES / NO / unknown]

Reconciliation File List:
[complete list of files/data/source-truth owners needing reconciliation / None]

Reconciliation Recommendation:
[analysis-only recommendation for reconciling, or None]

Reconciliation Mutation Status:
[analysis-only; no file fixes during Stage 1]

Current-Main Reconciliation Identity Guard:
[PASS / Worktree Branch Identity Drift / not applicable]

Identity Rule:
[origin/main is context, not identity / not applicable]

Assigned Worktree Branch Identity:
[expected worktree, actual worktree, expected branch, actual branch, active authority record]

Branch-Local Authority Reassertion:
[PASS with current-state owner files updated for this branch / not applicable]

Incoming Main Active-Branch Blocks Accepted: NO
[NO / blocker with explanation]

Sibling Worktree Identity Preservation:
[PASS / blocker with sibling worktree affected]

Branch Class:
[implementation / release packaging / historical repair context only as canon allows]

Bounded State:
[exact phase/stage, workspace, branch, write target, authority record, package/slice/seam, allowed scope, affected surfaces, validation contract, non-includes, pending USER decisions, stop/report conditions, and next legal phase]

Assigned Worktree Confinement:
[Required / not applicable]

Expected Worktree Root:
[fill in assigned worktree root, or not applicable]

Actual Worktree Root:
[fill in current git root from preflight]

No Cross-Worktree Mutation:
[Required / not applicable]

GitHub Desktop-bound worktree:
[fill in bound folder when GitHub Desktop is used, or not applicable]

Automation Observability:
[PASS / BLOCKER_CANDIDATE / REVIEW_REQUIRED / REVIEW_INFO / not applicable]

Automation CWD Worktree Mismatch:
[Active when automation configured cwd is missing, stale neutral main, parked, or wrong worktree / Clear / not applicable]

Configured Automation CWD:
[fill in configured cwd and resolved worktree role when automation affects lane truth / not applicable]

Worktree Escape User Waiver:
[Granted with expected root, actual root, target root, allowed commands/files, expiration or stop condition, required validation, and return path / None]

Worktree Escape User Waiver: Granted is valid only when USER explicitly supplies the expected root, actual root, target root, allowed commands/files, expiration or stop condition, required validation, and return path.

Worktree Escape User Waiver Missing:
[Active when actual root differs from assigned root and no waiver exists / Clear]

Bounded State User Waiver:
[Granted with exact waiver fields / None]

Bounded State Waiver Scope:
[required when waiver is Granted; otherwise None]

Implementation Delta Class:
[runtime/user-facing / backend/runtime / developer-tooling / docs-only / comma-separated non-docs-only values]

Docs-Only Workstream:
[Yes / No]

Planning-Loop Bypass User Approval:
[APPROVED / None]

Planning-Loop Bypass Reason:
[required when approved; otherwise None]

Slice Continuation Default:
[Same-branch backlog completion / blocked by stop condition / USER-approved backlog split]

Backlog-Split User Approval:
[APPROVED / None]

Backlog-Split Reason:
[required when approved; otherwise None]

Backlog Completion State:
[In Progress / Implemented Complete / Implemented Complete Except Future Dependency]

Remaining Implementable Work:
[None / short summary of same-branch work still available]

Future-Dependent Blockers:
[None / short summary of work blocked by another backlog item, dependency, or capability]

Release Branch:
[Yes / No / not applicable]

Release Target:
[required for release-bearing branches]

Release Floor:
[patch prerelease / minor prerelease / no release]

Version Rationale:
[required for release-bearing branches; explain why the floor matches the work]

Release Scope:
[required for release-bearing branches]

Release Artifacts:
[required for release-bearing branches]

Validation Contract:
[fill in only when validation governance matters]

Timeout Contract:
[fill in only when interactive timing governance matters]

User Test Summary Results:
[PENDING / PASS / FAIL / WAIVED / not applicable]

User-Facing Shortcut Path:
[fill in for relevant desktop user-facing Live Validation, or not applicable]

User-Facing Shortcut Validation:
[PENDING / PASS / FAIL / WAIVED / not applicable]

Seam Sequence:
[fill in when a Workstream pass may execute more than one seam]

Source-Truth Placement Preflight:
[existing authority owner / extends existing owner / No Existing Owner Fits / companion file pointer / not applicable]

Element Validation Ledger Owner:
[canonical workstream doc / active branch authority record / companion file with owning-record pointer / not applicable]

Dev Toolkit Interface Review Mode Disposition:
[callable in dev-only review mode / deferred to named repo-wide adoption branch-package / not-applicable with reason]

Element Delta Capture:
[Created / Touched / Affected / Deferred / Future / Dependency-only / Non-gating supporting / not applicable]

Repo state:
[Active Branch / No Active Branch]

Current active seam:
[fill in only when the task is in governed closeout recovery]

Note: task mode defines the task type. Codex collaboration posture is defined separately in `C:\Nexus Desktop AI\Docs\codex_modes.md`.
If the task is phase-sensitive and the exact `Phase` field is missing, stop and clarify before execution.
If repo state is blocked `No Active Branch`, implementation is blocked and the task should resolve the blocking repair path instead of starting implementation.
If repo state is steady-state `No Active Branch`, do not start implementation by inertia.
If `Bounded State` is missing, stale, or ambiguous, stop on `Bounded State Missing` before mutation.
Broad work requests do not authorize implementation. `Continue`, `complete all`, `all remaining work`, `finish the branch`, or similar wording may execute only when repo source truth resolves it to one exact active bounded seam.
If execution needs wider scope than the bounded state allows, stop on `Bounded State Waiver Missing` unless `Bounded State User Waiver: Granted` names the branch/worktree, phase, slice/seam, relaxed bound, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions.
Do not open a governance-only branch or between-branch canon repair lane.
Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
The only standing exception is the `Standing Governance Intake Branch`, `feature/release-readiness-source-truth-intake`, at `C:\Nexus Worktrees\Governance`; it accepts a `Release Readiness digest`, USER-approved `automation/worktree governance intake`, or USER-approved `phase-gate governance intake` only, uses `RRI-YYYYMMDD-NNN`, enforces operational `One Active Cycle`, requires the clean pre-intake `Sync Rule`, pauses the originating lane in `Waiting For Governance Intake` or `Waiting For Updated Main`, and must send a post-merge `Return Digest` with exact originating branch, originating worktree, operating workspace, expected branch, and `Neutral Main Workspace Rebaseline:` proof copied from the accepted intake. Do not open a dedicated closeout PR solely to clear `Active RRI Cycle` or cycle-ledger wording on the standing Governance branch.
The standing governance lane must stop on `Return Digest Origin Identity Missing` rather than infer the originating workspace from `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Governance`, GitHub Desktop's selected repository, or the current shell CWD.
If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
Release-packaging branches may proceed only when the branch-class admission rules from `C:\Nexus Desktop AI\Docs\phase_governance.md` allow them.
`main` is protected for Codex work: Codex may read `main` for truth validation, but must not edit, stage, commit, generate, refresh, or directly repair repository files on `main`.
Any tracked file mutation while Codex is on `main` is a `Main Write Attempt`.
There is no emergency direct-main repair path for Codex.
If a governance or canon update is directly required to keep the active current branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct, keep that docs-only update on the active branch inside the current phase and branch class.
Add `Validation Contract`, `Timeout Contract`, and `Current active seam` when the governed task needs them.
Add `Seam Sequence` when the Workstream prompt may use bounded multi-seam workflow.
If `Seam Sequence` is present, Codex must execute one active seam at a time, validate after each seam, and report a continue-or-stop decision before starting the next seam.
If a prompt names an active seam, treat it as the entry seam, not a terminal boundary.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.
If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.
Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.
A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.
After a green seam, `Next-Seam Continuation Required` applies by continuing seam-to-seam inside the current slice until all required seams are complete and the slice status is green when continuation authority conditions pass.
Seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress.
There is no repo-wide cap on how many slices a branch or workstream may carry.
same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green.
Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
Branch Readiness Stage 1 - Analysis Gate is analysis-only and must output `## Branch Readiness Stage 1 Analysis Packet` with product vision, project-wide vision alignment, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable vs full-system boundary, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, rejected shallow plan, alternatives/tradeoffs reviewed, open USER decision points, deferred ideas/future-package ledger, `Stale Branch Cleanup Plan:`, and `Branch Readiness Planning Incomplete` blocker review for family/package product work; it allows no repository file mutation, branch creation, package admission, docs sync, PR work, release work, selected-next truth, or canon edits.
Branch Readiness Stage 1 also outputs `Carrier Lifecycle Decision` with `Carrier Lifecycle Classification:` exactly one of `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, or `Active remote/open PR branch`, plus `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Stale Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`.
Branch Readiness Execution User Approval Missing blocks Branch Readiness Stage 2 - Execution Gate until explicit USER approval to enter Stage 2 is recorded.
Branch Readiness Stage 1 must include FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, validation plan, `Stale Branch Cleanup Plan:`, expected docs sync, blockers and waivers, rollback path, and the exact Stage 2 green-light decision needed. For broad implementation family packages, marker-only planning is insufficient; the packet must include non-empty, concrete `Project-Wide Vision Alignment:`, `Branch-Specific Vision Alignment:`, `System Concept Model:`, `Entity / Profile Model:`, `User Workflow Model:`, `Scale / Data Volume Model:`, `Configuration And State Model:`, `Expected User-Facing Outcomes:`, `Codex Additional Recommendations:`, `USER Critique Loop:`, `USER Decision Ledger:`, `Deferred Ideas / Future Package Ledger:`, `Planning Adequacy Review:`, `Rejected Shallow Plan:`, `Alternatives And Tradeoffs Reviewed:`, `Whole-System Interaction Map:`, `Minimum Viable vs Full System Boundary:`, and `Open Questions / USER Decision Points:` fields so the branch cannot enter Workstream, Hardening, Live Validation, or PR Readiness from a shallow/simple-system plan or Codex self-assessment. When USER input is needed, questions must include Codex recommendation, rationale, alternatives, tradeoffs, current-branch impact, future-package impact, safe default, waiver/defer posture, and exact response format. When USER needs a durable editable handoff, Stage 2 may generate or refresh a USER-facing `User Vision Input.txt` desktop artifact with accept/change/defer answer paths, while preserving that the artifact is not repo source truth until a later USER-approved digest pass records completed answers. For user-facing family/package branches, Stage 1 must also define the `Interface Release Boundary`, `Primary Interface Release Surface:`, `Interface Bundle User Approval:`, fallback point, interface acceptance criteria, and interface proof path; missing or multi-interface drift blocks on `Interface Release Boundary Missing`, `Primary Interface Undefined`, `Multiple Interface Release Drift`, `Fallback Point Missing`, `Interface Acceptance Missing`, or `Branch Readiness Interface Planning Incomplete`. Workstream, Hardening, Live Validation, or PR Readiness entry or continuation remains blocked while `Product Vision Input Missing`, `Project-Wide Vision Alignment Missing`, `Branch-Specific Vision Alignment Missing`, `USER Vision Question Packet Missing`, `USER Vision Recommendation Missing`, `USER Vision Questions Unanswered`, `USER Vision Input Pending`, `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, `System Concept Model Missing`, `Entity / Profile Model Missing`, `User Workflow Model Missing`, `Scale / Data Volume Model Missing`, `Configuration And State Model Missing`, `Expected User-Facing Outcomes Missing`, `Codex Additional Recommendations Missing`, `USER Critique Loop Missing`, `USER Decision Ledger Missing`, `Deferred Ideas / Future Package Ledger Missing`, `Planning Adequacy Review Missing`, `Rejected Shallow Plan Missing`, `Alternatives And Tradeoffs Missing`, `Whole-System Interaction Map Missing`, `Minimum Viable vs Full System Boundary Missing`, `Open Questions / USER Decision Points Missing`, `Branch Reach Unproven`, `Feature Element Breakdown Missing`, `Acceptance Criteria Missing`, `User-Facing Proof Standard Missing`, `Current Branch vs Future Package Boundary Missing`, or `Branch Readiness Planning Incomplete` remains active unless explicit USER waiver text is recorded.
Completed USER input digests may add package-specific planning blockers such as legacy product-name drift, telemetry provider selection, polling floor, warning modality, external telemetry privacy model, cross-family audio approval, and persona/model switching scope; Workstream must not resume until Branch Readiness revalidates, defers, or waives those blockers. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.
Candidate-only family-package planning is incomplete. If scope, future-package deferrals, provider path, polling posture, warning modality, privacy model, naming/product-copy handling, acceptance criteria, or proof standards are still only candidate statements, route through Branch Readiness Stage 2 source-truth repair and then Stage 1 revalidation before Workstream implementation resumes unless USER explicitly waives the requirement.
Element Coverage is a non-identity checklist only; coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact.
Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.
Before creating a new governance/source-truth file, active artifact, ledger, registry, or durable authority surface, perform `Source-Truth Placement Preflight`: identify the existing authority owner, extend the existing owner first, and create a new active artifact only when `No Existing Owner Fits` is recorded or the owning workstream/branch record points to a companion file.
The `Element Validation Ledger` is row-level created/touched/affected/deferred/future element proof tracking. For promoted work, it lives in the canonical workstream doc; for `Registry-only` active branches, it lives in the active branch authority record. Each seam must run `Element Delta Capture` and update ledger rows for product-significant UI, runtime behavior, hidden user-facing behavior, validation artifacts, screenshots, UTS questions, and source-truth boundaries.
Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
Docs-only Workstreams require explicit USER approval.
Planning-loop bypass requires `Planning-Loop Bypass User Approval: APPROVED` and `Planning-Loop Bypass Reason:`.
Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
reporting `Next Safe Move` is not a substitute for execution when continuation authority passes.
reporting Next Safe Move is not a substitute for execution when continuation authority passes.
A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice.
continue decision must be acted on immediately by starting the next seam needed inside the current slice.
when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
`Workstream` reaches `Hardening` only when `Completion Status: Green`
`Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; one green seam or one green slice cannot move the branch to Hardening while admitted branch material remains.
`Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation
Legacy `Single-Seam Fallback` and `Single-Seam Mode Waiver` wording is retired in active source-of-truth.
`Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item.
Use `Backlog Completion State: In Progress`, `Implemented Complete`, or `Implemented Complete Except Future Dependency` to record whether more same-branch slices are still required.
Stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition.
For `Release Readiness`, a release-bearing branch must include `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:` before green status is allowed.
For `PR Readiness`, release-bearing merge-target canon must prove the target is semantically correct from the latest public prerelease and declared release floor before green status is allowed.
For release-version planning, `patch prerelease` is the default for architecture-only planning, admission contracts, validation-only work, documentation/canon repair, governance repair, and non-user-facing milestones that do not add executable product behavior; `minor prerelease` requires a new executable, runtime, operator-facing, user-facing, or materially expanded product capability lane.
After a public prerelease tag exists for a release-debt owner, prompts must route durable closure before implementation: latest public prerelease truth advances, the released owner becomes Released / Closed, release debt clears, and the workstreams index moves the owner to Closed.
`Release Readiness` is analysis-only for repository files. It may produce release package information in the response, but it must not edit, stage, commit, generate, or refresh source, docs, canon, validator, helper, release-note, or handoff files.
If a file change is needed during `Release Readiness`, classify `Release Readiness File Mutation Attempt`, return to `PR Readiness` before merge, or defer to the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge.
Use `Release Branch: No` only for preserved historical records.
Do not use `Release Branch: No` for `implementation` or `release packaging` branches.
If a required User Test Summary handoff is outstanding, use `User Test Summary Results: PENDING`, list `User Test Summary Results Pending` under blockers, and do not report final phase advancement as green until the filled User Test Summary is submitted or waived, digested, and blockers are reevaluated.
Live Validation green requires an exact `## User Test Summary` state before final green.
For relevant desktop user-facing Live Validation, apply the `User-Facing Shortcut Live Validation Gate` / `desktop-shortcut` blocker path before User Test Summary handoff: declare `User-Facing Shortcut Path:`, record `User-Facing Shortcut Validation: PENDING`, `PASS`, `FAIL`, or `WAIVED`, and keep `User-Facing Shortcut Validation Pending` as a blocker until the declared desktop shortcut or equivalent user entrypoint is passable or explicitly waived.
For relevant desktop user-facing Live Validation, apply the `Codex Live Client Self-QA Gate` before User Test Summary handoff: declare `Codex Live Client Self-QA:`, `Visual Quality:`, `Live Interaction Evidence:`, `Usability Check:`, and `Platform Uniformity Check:`, and keep `Codex Live Client Self-QA Pending` as a blocker until Codex has inspected and exercised the launched client like a user or an explicit waiver is recorded.
If the user-facing work is interactive, screenshot-only, marker-only, or launched-but-not-driven proof cannot clear the self-QA gate; Codex must record the same visible interaction checks it would ask the USER to perform.
For desktop UI, use an active foreground/user-observable client mode; hidden, too-fast, or blink-through helper evidence is supporting automation evidence only.

For phase-sensitive execution, the response must explicitly report:

- `Seam Status:`
- `Slice Status:`
- `Completion Status:`
- `Blockers:`
- `Waiver Status:`
- `Continue Decision:`
- `Continuation Execution Latch:`
- `Stop Basis:`

Do not rely on generic `Results` or `Validation` headings by themselves.
A green seam does not authorize stop while `Slice Status` remains non-green.
A green slice does not authorize stop while `Completion Status` remains non-green.
A green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice.
If `Completion Status` is `In Progress` and no named blocker or waiver stops work, Codex must continue instead of returning `Await Next Instruction`.
Use these governed state markers as execution control, not just reporting.
If `Continue Decision` is `Continue`, Codex must not end on a seam-complete final response, rollback path, or next-seam recommendation; it must keep executing until a lawful `Stop` decision exists.
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

Default expectation:

- if task mode is `analysis-only` or `planning-only`, do not patch
- if task mode is `docs-only`, change docs only inside the approved boundary
- if task mode is `patch`, perform the approved implementation work unless blocked by a real conflict

## Current Accepted State

- [fill in the current version status]
- [fill in the relevant completed revisions]
- [fill in the relevant guarantees already established]

## Carry-Forward Review

Classify prior suggestions, branch conclusions, or closeout output as:

- carry forward
- defer
- discard

Do not treat prior suggestions as automatic scope.

For the first planning prompt after a merge or release, this review should be filled in explicitly.

## Evidence Inputs

Use the following as part of the task evidence set when relevant:

- [uploaded files]
- [logs]
- [screenshots]
- [trace output]
- [manual test notes]
- [prior verification artifacts]
- [branch-local validation artifacts created during the pass]
- [validator or harness outputs]

If critical evidence is missing, say so explicitly.

If the task depends on in-chat screenshot review inside the Codex client, add a prompt note such as:

- `Use live launched-process screenshots.`
- `Preserve the originals on disk and in the audit manifest.`
- `For in-chat image proof, use a small inline PNG data image one at a time until rendering is confirmed.`

## Locked Boundaries / Do Not Reopen

Do not casually reopen:

- [locked behavior 1]
- [locked behavior 2]
- [locked behavior 3]

If any future version should intentionally change those, treat that as a deliberate new workstream or system phase, not a cleanup tweak.

## Task

Your job is to:
[describe the exact task in one or two sentences]

## Workstream Identity

Use this section when the task is a coherent workstream:

- subsystem: [one subsystem only]
- end-state: [one concrete end-state]
- approved subproblem: [one coherent approved subproblem]

## Branch And Milestone Context

Use this section when the branch matters to the task:

- milestone value: [why this branch or docs program is worth completing]
- same-branch follow-through: [dependent work that still belongs on this branch before readiness]
- branch posture: [fresh branch from updated main / continue approved active branch / release packaging branch / No Active Branch / protected-main drift repair on legal branch surface]
- branch-level plan: [objective, target end-state, expected seam families and risk classes, validation contract, User Test Summary strategy, later-phase needs, and first seam or seam sequence]

If a lane was already closed, merged, or released, the next workstream should start from updated `main` on a fresh branch.

## Goal

The goal of this task is:
[describe the concrete desired result]

## Scope

In scope:

- [scope item 1]
- [scope item 2]
- [scope item 3]

Out of scope:

- [out-of-scope item 1]
- [out-of-scope item 2]
- [out-of-scope item 3]

## Allowed Changes

You may change:

- [allowed file / module / doc 1]
- [allowed file / module / doc 2]

You may add only if required for the approved scope:

- [new helper / runner / doc if needed]

## What Must Not Change

Do not change:

- [file, subsystem, or behavior 1]
- [file, subsystem, or behavior 2]
- [file, subsystem, or behavior 3]

## Analysis-Phase Rules

Before proposing implementation, Codex should:

- validate live repo truth
- scan broadly enough to understand the affected system
- identify factual, structural, and authority drift where relevant
- report risks, dependencies, and options clearly
- avoid premature scope compression before the user and ChatGPT choose execution boundaries

If the request is analysis-heavy, do not turn it into a bounded executor prompt too early.

## Execution-Phase Rules

After analysis is complete and execution scope is approved, follow these discipline rules:

- verify exact failure path or behavior before changing logic
- no blind iteration
- one coherent approved subproblem per revision
- use bounded multi-seam workflow as the primary Workstream model when the current slice remains same-workstream, same-phase, same-branch-class, same approved scope, and same-subsystem-family or tightly coupled
- execute exactly one active seam at a time and validate, record, and decide continue-or-stop before the next seam
- treat a prompt-named seam as the entry seam, not a terminal boundary
- continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green
- continue by default after a green seam when `Next-Seam Continuation Required` applies and the current slice still needs another seam
- recognize that a slice is a bounded admitted backlog-completion unit while a seam is the current execution checkpoint inside or between slices
- keep same-branch backlog completion as the branch-level default so later slices stay on the same branch whenever validation stays green
- seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress
- when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
- preserve architecture boundaries
- keep source-of-truth docs aligned with actual implemented state
- production behavior must remain unchanged unless explicitly in scope

Execution-specific discipline such as:

- minimal isolated changes
- smallest coherent execution slice
- bounded implementation
- narrow fix pass

belongs here, after scope has been selected.

Additional task-specific constraints:

- [constraint 1]
- [constraint 2]
- [constraint 3]

## Guidance

Operate like a careful senior collaborator.

That means:

- validate assumptions against the docs and current repo state
- reason broadly before deciding execution shape
- call out risks or drift clearly
- avoid speculative rewrites
- do not widen scope without justification
- when code work is the primary deliverable, keep directly supporting truth-doc sync inside the same approved workstream when that preserves canon coherence
- when live truth shows a closed lane or released branch is no longer the right base, call that out and move the next workstream to updated `main` on a fresh branch

If an execution task is too broad for one approved pass, explain the cleaner execution shapes after analysis rather than shrinking the investigation itself.

## Required Workflow

### Before Changing Anything

1. Read the source-of-truth docs.
2. Inspect the relevant repo, code, or doc state.
3. Inspect the provided evidence inputs.
4. Validate branch, release, and current-truth posture when relevant.
5. Report the actual state, risks, conflicts, and dependencies.

### Before Execution

1. Explain the approved execution scope.
2. Explain the branch or workstream posture.
3. Explain the exact current phase, branch class, and blockers.
4. Explain the next legal phase or say explicitly that repo state is `No Active Branch`.
5. If in `Branch Readiness`, explain the whole-branch execution plan before Workstream admission.
6. If in `Workstream`, explain whether bounded multi-seam workflow is safe; if it is, list the seam sequence, per-seam gates, and stop conditions.
7. If in `PR Readiness`, first identify whether the request is `PR Readiness Stage 1 - Analysis Gate` or `PR Readiness Stage 2 - Execution Gate`. Stage 1 is an analysis-first blocker repair gate: it analyzes repo truth, records `PR Readiness Stage 1 Repair Required` for bounded current-branch PR-readiness drift/blockers, validates those repairs, commits/pushes durable repair truth only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair, and stops on `PR Readiness Stage 1 Repair Pending` until the repair is complete. Stage 1 still cannot create the PR, provision the watcher, create a branch, admit a package, waive single-slice rules, create a tag, create release artifacts, draft or publish a GitHub Release, execute a release, create a runtime branch, or admit a runtime package. Stage 1 may encode selected-next truth only when USER explicitly approves selected-next sync, and branch creation plus runtime package admission must stay blocked for Branch Readiness. Stage 1 selected-next/no-release-debt handling is complete only when the next selected branch/workstream is recorded in source truth before PR creation or an explicit USER waiver says no next branch/workstream is selected, release target/floor semantics and Release Window Audit are resolved when relevant, branch-authority cleanup is durable, stale-canon risk is cleared, and any unavoidable release debt has an explicit USER decision, named owner, and real-carrier plan before Stage 2. Stage 1 outputs `## PR Readiness Stage 1 Analysis Packet` with next-branch hierarchy, required post-merge path, ranked runtime FAM candidates, recommended next package, package-size / single-slice drift review, release-debt impact, release-debt handling status, selected-next / no-release-debt handling status, Stage 1 repairs made, Stage 1 repair validation, Governance Ledger fallback status, Branch Readiness fallback status, a user-facing `## Next Workstream` block containing `Recommended Next Workstream:`, recommended family/package, candidate slices, `Candidate Work To Be Done:`, `User-Facing Output:`, why it is next, dependencies/blockers, validation needs, release impact, selection-truth status, branch-creation status, and `Next Workstream User Waiver:`, a no-work `## Next Branch Pre-Plan` block containing `Next Branch Package Shape:`, proposed FAM/package, multiple concrete candidate slices, `Candidate Work To Be Done:`, `Single-Slice Drift Review:`, `Family Organization Review:`, `Element Coverage Review:`, dependencies/blockers, validation/live-test needs, branch creation status, and USER approvals required, Stage 2 sync plan, and stops on `PR Readiness Execution User Approval Missing` until explicit USER approval to enter Stage 2 is recorded; Stage 1 cannot continue to Stage 2 unless the next-workstream block analyzes a concrete candidate and the work planned for that candidate, records approved selected-next truth, or records `Next Workstream User Waiver: Granted`; otherwise `Next Workstream User Waiver Missing` blocks continuation. If no legal next workstream candidate is found, Stage 1 must also stop on `Next Workstream Candidate Not Found`, report the still-not-closed FAM list plus every not-complete package and slice, and record `Stage 1 USER Waiver Required` unless the USER grants a waiver/approval that clears the route. If the next-branch pre-plan cannot show a broad FAM/package with multiple concrete candidate slices, stop on `Next Branch Package Shape Unproven`; if it looks like single-seam or single-slice branch drift, stop on `Single-Slice Branch Drift Risk Unresolved`; if it drifts from FAM -> Package -> Slice -> Seam or revives old live `FB-###` identity behavior, stop on `Family Organization Drift Risk Unresolved`; unresolved next-workstream or next-branch shape blockers require `Current-Branch Branch Readiness Re-entry Required` when the current branch remains the legal carrier or `New Carrier Branch Required` when the current branch cannot own the blocker. If the governance/source-of-truth ledger audit finds identity model drift, FAM taxonomy drift, package/branch rule drift, USER approval blocker drift, real-carrier routing drift, branch-authority lifecycle drift, watcher/automation proof drift, release readiness/execution boundary drift, Element Coverage misuse, ChatGPT loader/source-truth drift, project-direction drift, current workflow drift, after-release workflow drift, or absolute-guardrail drift that cannot be cleared as bounded current-branch PR Stage 1 repair, report `Governance Ledger Fallback:` and classify the route as `Current-Branch Branch Readiness Re-entry Required` or `New Carrier Branch Required`. Stage 2 may begin only after Stage 1 repair blockers, Next Workstream blockers, Next Branch Pre-Plan blockers, Governance Ledger fallback blockers, and Branch Readiness fallback blockers are clear and USER approval exists, then explicitly plan the stale-canon check, post-merge-state handling, merge-target authority projection check with `Merge-Target Authority Projection Unproven` blocking PR green until active branch authority is merge-stable for any USER-waived post-merge `No Active Branch` truth, release-target semantic check from latest public prerelease plus `Release Floor:` when relevant, priority-led next-workstream selection using open backlog `Priority` and deferred-context readiness rather than `Target Version` only after explicit USER approval exists, next-workstream canon/minimal-scope/no-branch-exists check, required `Next Workstream: Selected`, runtime `Minimal Scope:`, `## Selected Next Workstream`, and `Branch: Not created` markers when approved, `Backlog Addition User Approval Missing` with the still-not-closed FAM list plus every not-complete package and slice when approval is absent, `Backlog Exhaustion User Decision Pending` when that list is empty, `Single-Slice Package User Approval Missing`, admitted-slice counting where only `Admission State: Admitted` rows count and historical evidence/future placeholders/deferred ideas/future-package-required rows do not count, `Package Completion Unproven`, `Next Runtime Candidate Selection Pending` clearance by selecting exactly one real runtime Feature Family candidate before leaving PR Readiness after approval exists, dirty-branch/durable-commit check, docs-sync/drift-audit check, Automation Observability Review Pending with `dev/automation_observability_report.py` for Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`, including `BLOCKER_CANDIDATE` and `REVIEW_REQUIRED` classification, the `Release Window Audit` with default green posture `Remaining Known Release Blockers: None`, `Another Pre-Release Repair PR Required: NO`, and `Release Window Split Waiver: None`, `PR Readiness Scope Missed`, `Release Window Audit Incomplete`, `Between-Branch Canon Repair Attempt`, `Next Branch Created Too Early`, the live PR merge-status check with `PR Merge Status Unproven` until the PR explicitly reports a green merge status, the live PR bot-review signal check with `Bot Review Signal Pending`, `PR Watcher Provisioning Unproven`, `PR Watcher Routing Unverified`, `PR Merge Verification Pending`, thumbs-up reaction versus bot comment handling, watcher target/runtime/run-proof/fallback/teardown and replacement-provisioning proof for the live PR, the approved reporting surface and route cross-check proof for that live PR, accepted watcher proof through native heartbeat run evidence or a bounded local watcher that posts through the official Codex thread-resume path rather than manual rollout-file injection, delivery proof through assistant-message transcript presence plus Codex thread-state and automation run/inbox visibility, minute cadence, the requirement that the watcher reports only when a watched PR status changes, the rule that the current working thread is the default reporting surface but an explicitly recorded dedicated watcher-host thread is allowed when that is the validated user-visible route, the rule that watcher status-change output must be source-of-truth shaped and include a copy/paste Codex prompt basis after `merged=true`, the rule that final merge delivery proof must exist before the watcher retires, the rule that PR Readiness continues into a merge-watch seam after PR creation and live validation, and the rule that no later thumbs-up is required after comment-resolution closeout, normal governance validator, PR-readiness gate mode, required `## Next Workstream`, `## Next Branch Pre-Plan`, and `## Next Branch` response blocks, and inclusion-only `## PR Creation Details` operator copy blocks.
8. Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript. If missing proof blocks a release, carry it on a real release-support carrier; if product work is next, carry it on the next real runtime package carrier.
9. If in `Release Readiness`, explicitly plan the `Release Target Undefined` check, required inherited `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:` markers for release-bearing branches, release operator copy blocks, confirm Release Readiness is not being used for broad docs sync or branch-authority cleanup, record `Branch Cleanup Plan:` and `Branch Cleanup Execution Gate:` when stale/old branches, worktrees, or a GitHub Desktop-bound worktree need later cleanup, and confirm no repository file mutation or branch/worktree cleanup will occur in the phase.
10. Explain the validation plan.
11. If a User Test Summary handoff is relevant, explicitly state whether returned results are `PENDING`, `PASS`, `FAIL`, or `WAIVED`; `PENDING` is the hard blocker `User Test Summary Results Pending`.
11. Apply the Pre-PR Durability Rule: before `PR Readiness`, when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state; only a documented `Durability Waiver`, failed validation, legally file-frozen `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push, and self-imposed blockers must automatically commit and push once lifted.

If the task includes interactive validation, the validation plan should also state:

- existing helper or harness that will be reused first, or the exact reason reuse is unsafe
- `Docs/validation_helper_registry.md` lookup result when a durable root `dev/` helper, live-validation script, audit helper, harness, or shared helper module is created or kept
- the helper's standardized name, `Helper Status:`, owner, and `Consolidation Target` when the helper is `Workstream-scoped`
- any `Temporary probe` handling, including whether it will be deleted or promoted
- whether any temporary one-off probe is being used and how it will be deleted or promoted before closeout-grade proof
- full-run hard timeout
- no-progress timeout
- scenario timeout when relevant
- transition timeout when relevant
- visible progress markers or step-log updates that prove the run is not stalled
- how timeout or freeze will be reported and cleaned up

### During Execution

1. Perform only the approved execution work.
2. For bounded multi-seam workflow, perform exactly one seam, verify it, record evidence, and decide `continue` or `stop` before starting the next seam.
3. Continue by default to the next seam needed inside the current slice after a green seam when `Next-Seam Continuation Required` applies and the continuation authority conditions pass.
4. Reporting `Next Safe Move` is not a substitute for execution when continuation authority passes; A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice.
5. Stop the workflow immediately on validation failure, regression, scope drift, unplanned risk expansion, governance drift, unresolved manual-validation blocker, branch-truth inconsistency, phase boundary, stop-loss trigger, or a declared `Backlog-Split User Approval` boundary.
6. Clean up session-scoped side effects from the pass unless there is an explicit reason to preserve them.
7. Once the current slice is green during `Workstream`, advance into the next admitted slice while `Completion Status` remains `In Progress`; await the next instruction only after a lawful `Stop` decision.

## Verification Requirements

At minimum, verify:

- [verification item 1]
- [verification item 2]
- [verification item 3]

If applicable, also verify:

- healthy path
- failure path
- artifact cleanup
- session cleanup and teardown
- existing-helper reuse or documented justification for any temporary probe
- cleanup verification, including that no test-opened app window, helper process, or temporary probe file was left behind
- no regressions in locked behavior
- no drift outside the allowed surfaces
- interactive validation time budgets and timeout behavior when the pass depends on a real desktop or harness run
- no-progress supervision, using the tighter helper-specific watchdog when present or a `10s` maximum no-progress interval when no tighter watchdog exists

Session cleanup and teardown includes, when relevant:

- closing programs, windows, or dialogs opened during the pass
- stopping helper processes, harnesses, temporary runtimes, or validators started during the pass
- deleting temporary files, scratch documents, probe files, or other temporary outputs created only for the pass
- restoring any local state or source inputs intentionally changed for verification
- explicitly checking that those items are actually closed, stopped, deleted, or restored before handoff rather than assuming they cleaned themselves up

If anything remains intentionally open or preserved after the pass, the output must say so explicitly and explain why.

If an interactive run times out or freezes, the output must also state:

- which time budget tripped
- the last confirmed meaningful progress point
- what cleanup was performed before handoff
- whether the issue is classified as product defect, harness defect, environment issue, or canon / contract drift

If the slice changes user-visible behavior, runtime interaction, UX flow, prompts, startup behavior, voice behavior, or another manual operator-facing path before Live Validation, the final output must include `## User Test Summary Strategy` or Live Validation readiness notes, not a formal `## User Test Summary` artifact.
User Test Summary is exclusive to Live Validation Stage 1.
Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.
PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact.
During Live Validation Stage 1, the output must include a formal `## User Test Summary` section as a concrete manual checklist unless the UTS gate is explicitly waived.
Every Live Validation digest must include an exact `## User Test Summary` section. If the UTS gate is waived, the digest section must still declare `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`.

That checklist must include:

- setup or prerequisites
- exact user actions
- expected visible behavior
- failure signs to watch for
- branch-specific or slice-specific validation focus

A recap-style summary is not sufficient when manual validation is relevant.

If no meaningful manual test exists, the output must still include `## User Test Summary` and explain why manual validation is not materially relevant for that slice.

If a canonical repo-level `UTS` strategy exists for the active desktop workstream, the execution pass must update that strategy as well rather than stopping at response text.

By default, that artifact is the `## User Test Summary` section in the relevant canonical workstream doc unless that doc explicitly declares a different repo path.

For bounded multi-seam Workstream execution, update the canonical workstream `UTS` strategy incrementally as user-visible seams land.
When the Workstream seam chain is complete, do not refresh the formal desktop export; preserve the need for Live Validation Stage 1 instead.

If the artifact is not updated, the final output must explain why the update was skipped.

For relevant desktop Live Validation Stage 1 runs, the execution pass must also export or refresh:

- `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

unless the final output explicitly explains why the desktop export was not relevant or was intentionally skipped.

Response-level `## User Test Summary` text alone is not sufficient during Live Validation Stage 1 when either the canonical repo artifact or the desktop export should exist.

Returned User Test Summary results are a hard phase gate. While results are pending, output the state as:

- Automated validators and live helper evidence: GREEN.
- User Test Summary Results: PENDING.
- Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.

After submission, digest the filled results into the active authority record, reevaluate blockers, and route back to `Workstream` or `Hardening` if user evidence exposes mismatch, regression, ambiguity, cleanup failure, or scope drift.

For runtime, UI, startup, prompt, voice, or other operator-facing implementation slices, validator results alone are not sufficient to justify immediate continuation.

The execution pass must also:

- run a deeper branch-local validation or hardening pass against the implemented path
- add or create the smallest reliable validation infrastructure on-branch when meaningful blind spots remain
- preserve evidence of the validators, synthetic/headless harnesses, helper scripts, fixtures, logs, traces, screenshots, or other validation artifacts actually used
- use synthetic or headless validation as supporting proof rather than the final continuation gate when a real desktop session is feasible
- launch and exercise the real desktop or runtime path through an interactive OS-level session when feasible
- explicitly distinguish validator results, synthetic or headless validation results, simulated reasoning, interactive OS-level execution results, and remaining manual user-test handoff
- explicitly decide whether the next move is to continue implementation, pause for hardening, or fix a specific defect first

If the current validation surface is too thin to support a continuation recommendation, the execution pass must strengthen that surface before recommending continuation.

If a real interactive OS-level session is not feasible, the execution pass must explain why, use the strongest available non-interactive evidence, and state that any continuation recommendation is limited by that missing interactive gate.

## Done When

This task is complete only when:

- [done condition 1]
- [done condition 2]
- [done condition 3]
- no unrelated behavior changed
- the result stays inside approved scope
- verification evidence supports the claimed result

## Stop Conditions

Stop and explicitly report if:

- source-of-truth docs conflict with the request
- critical evidence is missing
- the task would require reopening locked architecture
- safe verification is not possible
- the task is in `Release Readiness` and requires any source, docs, canon, validator, helper, release-note, or handoff-file mutation; return to `PR Readiness` before merge or defer to the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge
- the task is on `main` and requires any repository file mutation; treat it as `Main Write Attempt` and move the repair to a legal branch surface
- the task needs a new branch basis because the current one is stale, merged, or no longer the right execution base
- `User Test Summary Results Pending` remains active while the task attempts to advance phase, PR readiness, merge readiness, or final green status

## Required Output Format

A. Source-of-truth validation result
B. Recommended plan or execution summary
C. Files changed or to be changed
D. Risks, conflicts, or notable design choices
E. Verification summary
F. Any doc updates made or why none were needed
G. Next Legal Phase digest

Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation.

If relevant, also include:

H. Commit summary
I. Commit description
J. PR title
K. PR description

L. `## User Test Summary` manual checklist when manual validation is relevant

If the phase is `PR Readiness`, the final response must include:

```markdown
## PR Readiness Stage 1 Analysis Packet
- Current PR Readiness Stage:
- Repository Mutation Status:
- Planned PR Title:
- Planned Base Branch:
- Planned Head Branch:
- Planned PR Summary:
- Required Post-Merge Path:
- Ranked Runtime FAM Candidates:
- Recommended Next Package:
- Recommended Next Package USER Waiver:
- Package-Size / Single-Slice Drift Review:
- Element Coverage Review:
- Release-Debt Impact:
- Release-Debt Handling Status:
- Selected-Next / No-Release-Debt Handling Status:
- Required Current-Branch Source-Truth Sync:
- Planned Merge-Target Canon Updates:
- Planned Next Branch Block:
- Planned Watcher Provisioning:
- Planned Validation Commands:
- Expected Files To Change:
- Stage 1 Repairs Made:
- Stage 1 Repair Validation:
- Release Readiness Health Pass:
- Release Candidate Anchor Projection:
- Release Window Contributor Inventory:
- Governance Ledger Fallback:
- Branch Readiness Fallback:
- Stage 1 Outcome:
- Stage 2 Sync Plan:
- Drift Findings:
- Blockers And Waivers Needed:
- Release Window Audit Posture:
- Rollback Plan:
- Next Legal Phase:
- Stage 2 Green-Light Decision Needed:
```

If the current stage is `PR Readiness Stage 1 - Analysis Gate`, the final response must also report Stage 1 repair findings, Stage 1 repairs made, validation results, files changed or none, whether `PR Readiness Stage 1 Repair Pending` is clear, and one explicit readiness-lock outcome: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`. It must state `PR Readiness Execution User Approval Missing` and stop for USER approval to enter Stage 2 unless Stage 1 is ready and USER approval already exists.

PR Readiness must prove post-merge source truth before PR creation, after any Stage 2 or bot-review source-truth repair, and before merge approval with the `Release Readiness Health Pass` by running `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`. The packet must report `Post-Merge Branch Authority Projection:`, `Stale Active Branch Wording Scan:`, `Stale PR Creation / PR Readiness Pending Wording Scan:`, `Merged-Unreleased Scope Posture:`, `Release Execution Gate:`, `Watcher / Live PR State Projection:`, `Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `FAM Overlap Routing:`, `Release Candidate Anchor Projection:`, `Release Window Contributor Inventory:`, `Governance Intake Routing:`, and `Projected Post-Merge Validation:` so projected merged main can enter Release Readiness as validation, not cleanup.
If Release Readiness discovers stale active branch authority, stale phase wording, stale PR Readiness wording, selected-next ambiguity, release-window contributor ambiguity, or `No Active Branch` conflict after merge, the digest must say `Governance Intake Routing: send this to C:\Nexus Worktrees\Governance on feature/release-readiness-source-truth-intake` and include the originating worktree, branch, PR, merge commit, blockers, and next legal phase.

Release Readiness must declare `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, and `Candidate Includes Later Governance Repairs:`. Unless USER explicitly selects a historical commit as the release target, current fetched `origin/main` is the release candidate anchor and historical PR merge commits are audit evidence only. Missing or ambiguous anchor data is `Release Candidate Anchor Missing`; do not repair it inside Release Readiness.

Release Readiness must declare `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, and `FAM Contributor Routing:`. Merge order does not decide release ownership; when multiple FAM/worktree branches merge before the next release, use `Release Ownership Model: Aggregated release window` unless USER selects a narrower target. Missing or ambiguous contributor inventory is `Release Window Contributor Inventory Missing`.

If the phase is `Branch Readiness` and the current stage is `Branch Readiness Stage 1 - Analysis Gate`, the final response must include:

```markdown
## Branch Readiness Stage 1 Analysis Packet
- Current Branch Readiness Stage:
- Repository Mutation Status:
- FAM/Package Candidate:
- Package-Size Review:
- Multiple Admitted-Slice Plan:
- Single-Slice Drift Check:
- Element Coverage Review:
- Project-Wide Vision Alignment:
- Branch-Specific Vision Alignment:
- System Concept Model:
- Entity / Profile Model:
- User Workflow Model:
- Scale / Data Volume Model:
- Configuration And State Model:
- Expected User-Facing Outcomes:
- Codex Additional Recommendations:
- USER Critique Loop:
- USER Decision Ledger:
- Deferred Ideas / Future Package Ledger:
- Planning Adequacy Review:
- Rejected Shallow Plan:
- Alternatives And Tradeoffs Reviewed:
- Whole-System Interaction Map:
- Minimum Viable vs Full System Boundary:
- Open Questions / USER Decision Points:
- Runtime Branch Engineering Contract:
- USER Engineering Planning Review:
- Runtime Implementation Approval:
- Current Runtime Baseline:
- Planned Runtime Delta:
- User-Facing Runtime Delta:
- State / Config / Schema Delta:
- Validator / Helper Delta:
- Expected Changed Files / Surfaces:
- Approval-Boundary Audit:
- Future-Gated Items:
- Workstream Seam Map:
- Proof Expectations:
- Risk Forecast:
- Recommendations And Alternatives:
- Plan Version / Revision Status:
- Plan-To-Implementation Traceability:
- Validation Plan:
- Stale Branch Cleanup Plan:
- Expected Docs Sync:
- Blockers And Waivers Needed:
- Rollback Plan:
- Next Legal Phase:
- Stage 2 Green-Light Decision Needed:
```

It must also state `Branch Readiness Execution User Approval Missing`, confirm no repository file mutation occurred, and stop for USER approval to enter Branch Readiness Stage 2.
`Stale Branch Cleanup Plan:` is analysis-only in Stage 1. Stale/old branch cleanup may execute only during `Branch Readiness Stage 2 - Execution Gate` after branch/worktree creation or validation proves the replacement target, `git worktree list`, branch targets, and GitHub Desktop-bound worktree binding are safe.

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

If `PR Readiness` is package-ready, green, or `PR READY: YES`, the final response must also include these inclusion-only copy-ready operator blocks:

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

The `Next Branch` block must separate the next legal branch from the selected next implementation branch.
If the next implementation branch is deferred by release debt, updated-`main` revalidation, or another branch-admission gate, set `May Create Now: NO` and state the reason.
The PR summary/GitHub PR body uses exactly three top-level sections: `## Summary`, `## Branch Evidence`, and `## Validation`.
`## Summary` must be one concise outcome paragraph, and `## Branch Evidence` must not repeat the Summary through nested `### Summary`, `### Purpose`, or `### Overview` sections.
Use concrete Branch Evidence subheads such as `### Changes`, `### Context`, `### Source Truth`, or `### Boundaries` only when they improve scanability.
The PR summary must report implemented branch and validation truth only. Generic exclusion dumps, `Not Included` sections, and defensive scope language remain prohibited; concise branch-specific boundaries are allowed inside `## Branch Evidence` when they clarify reliable branch truth.
`## Validation` must contain validation commands, proof paths, or the historical no-validation sentence only.
GitHub PR bodies and PR Summary copy must not include phase-digest or Codex operator handoff fields such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, `Stop Basis`, `Exact next USER decision`, `Implemented, validated`, or `::git-*`; those belong in governed Codex/source-truth output, not branch evidence copy.

If `Release Readiness` is green for release execution, the final response must include these inclusion-only copy-ready operator blocks:

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

Release notes must clearly explain what was built, what capabilities exist, and how the system behaves. Do not include exclusion lists, `Not Included` sections, negative scope framing, or defensive wording.
Release notes must use the standard Markdown release body shape: `## Release Summary` or `## Release Overview`, `## Release Highlights` or release-specific rich sections, GitHub-generated `## What's Changed`, and the generated `**Full Changelog**:` compare link to the previous release.
The live GitHub release body must not start with or repeat the release title as `# <release title>`; the release title belongs in GitHub release metadata and the separate `Release Title` operator block only.
During Release Execution, use GitHub-generated release notes through the GitHub release notes button or generated-release-notes API so the `## What's Changed` section and previous-release compare link are populated by GitHub.
Public release bodies must not include internal automation/tooling brand tokens, generated branch-prefix noise, phase-handoff text, operator transcript text, or generated `[codex]` / `codex/...` PR labels. Rewrite those labels into neutral user-facing PR names before publication or repair them immediately after publication.
Validate the full published Nexus pre-Beta release set, not only the latest release, before reporting release-body standardization green.

## Important

- Do not write code if this is analysis-only.
- Do not patch files if this is planning-only.
- Do not reopen closed version behavior without explicit approval.
- Do not smuggle in policy or authority changes outside the approved task.
- Do not modify backlog status or add backlog items unless the task explicitly authorizes backlog updates.
- Do not force tightly coupled governance or canon updates onto a separate docs/governance branch when the active runtime-focused branch owns the affected truth and the update can stay inside its current phase, branch class, validation rules, and stop conditions.
- Do not open a governance-only branch or between-branch repair window for missed PR Readiness work; carry the repair in the next legitimate runtime-focused backlog branch's `Branch Readiness` before implementation begins.
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- Exception: the single `Standing Governance Intake Branch`, `feature/release-readiness-source-truth-intake`, may handle a `Release Readiness digest`, USER-approved `automation/worktree governance intake`, or USER-approved `phase-gate governance intake` using `RRI-YYYYMMDD-NNN`, operational `One Active Cycle`, the `Sync Rule`, originating-lane `Waiting For Governance Intake` / `Waiting For Updated Main`, and a `Return Digest` with exact originating branch, originating worktree, operating workspace, expected branch, and `Neutral Main Workspace Rebaseline:` proof copied from the accepted intake. Do not open a dedicated closeout PR solely to clear cycle-ledger wording on this standing branch.
- The standing governance return digest must stop on `Return Digest Origin Identity Missing` if those concrete identity fields are absent, generic, contradictory, or inferred from `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Governance`, GitHub Desktop, or the current shell CWD instead of the accepted intake.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
