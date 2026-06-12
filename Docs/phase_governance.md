# Nexus Phase Governance

## Top Rule: Pre-PR Durability

**DO THIS ALWAYS before `PR Readiness`: when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state. This includes `Branch Readiness`, `Workstream`, `Hardening`, and `Live Validation`; a prompt-level request not to commit is not enough to stop durability. The only exceptions are a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker; when that self-imposed blocker is lifted, Codex must automatically commit and push.**

**Release Readiness is file-frozen: block ANY source, docs, canon, validator, helper registry, release-note, or handoff-file changes discovered or needed during `Release Readiness`. Do not edit, stage, commit, or push in `Release Readiness`; route the change back to `PR Readiness` before merge, or to the next active `Branch Readiness` after merge.**

## Purpose

This document defines the governed execution phases used for Nexus Desktop AI work.

It exists so:

- workstream truth
- validation truth
- closeout truth
- prompt routing
- next-phase recommendations

all use the same phase names, blocker rules, and transition rules.

This is the canonical cross-workstream governance layer.
It does not replace:

- `Docs/Main.md` as the routing index
- canonical workstream docs as branch-local feature-state, evidence, and closure records
- release or rebaseline docs as milestone summaries

## Exact Prompt Contract

For phase-sensitive execution, prompts must include:

- `Mode: <mode name>`
- `Phase: <exact canonical phase name>`
- `Workstream: <workstream id or equivalent authority record>`
- `Branch: <branch name or No Active Branch>`

Add these fields when relevant:

- `Branch Class: <implementation / release packaging / historical repair context only as canon allows>`
- `Active Seam: <seam name>`
- `Seam Sequence: <ordered seam list>` when the current phase permits a bounded multi-seam pipeline
- `Validation Contract: <summary or authority reference>`
- `Timeout Contract: <summary or authority reference>`

If `Phase` is missing or is not one of the exact canonical phase names below, execution is blocked and only truth-validation or analysis may continue.
If `Seam Sequence` is present, it is structure only.
Prompt text may name the entry seam and downstream planned seams, but it does not define seam behavior, bypass phase rules, or authorize continuation by itself.
The canonical seam workflow contract below controls whether Codex may continue, must stop, or may split a backlog item across branches only with explicit USER approval.

## Mandatory Bounded State Gate

Bounded State is mandatory for every execution pass that can mutate repo files, create or switch branches/worktrees, commit, push, create a PR, handle PR comments, run release actions, launch runtime validation, mutate shortcuts, install providers/models, or hand off GitHub Desktop state.

Before mutation or execution, Codex must prove and report a `Bounded State:` with all of these fields:

- exact phase and stage
- active workspace, git root, branch, upstream, `HEAD`, `origin/main`, worktree role, and write target
- owning workstream or branch authority record
- active package, slice, and seam, or an explicit non-FAM repair carrier allowed by source truth
- exact allowed scope, affected surfaces, and validation contract
- explicit non-includes and pending USER decisions
- stop/report conditions and the next legal phase

If any required bounded-state field is missing, stale, contradictory, or cannot be resolved from source truth, Codex must stop on `Bounded State Missing` before mutation. Analysis may continue only far enough to report the missing field and the exact USER decision needed.

Broad work requests do not authorize implementation. Phrases such as `continue`, `complete all`, `all remaining work`, `finish FAM-007`, `do whatever is next`, or similar broad wording must resolve to the next named bounded same-branch seam already recorded in source truth. If they do not resolve to exactly one active bounded seam, Codex must stop on `Bounded State Missing` or `Next Bounded Workstream Seam Approval Missing`.

Widening beyond the current bounded state requires explicit USER waiver text recorded as `Bounded State User Waiver: Granted`. The waiver must name the branch/worktree, phase, slice/seam, the exact bound being relaxed, allowed extra seams/slices/files, expiration or stop condition, required validation, and still-pending USER decisions. If a task needs wider scope and that waiver is absent, stop on `Bounded State Waiver Missing`.

Clean validation, a clean git tree, branch existence, prior broad approval, Codex discretion, ChatGPT wording, or prompt output shape cannot infer a bounded-state waiver. `Bounded State User Waiver: None` means execute only the named active bounded seam at a time, then continue to the next admitted same-branch seam or slice when the Workstream continuation latch remains active. It does not authorize treating the first seam as a terminal Workstream boundary.

## Prompt-Entry Origin/Main Freshness Gate

`Prompt-Entry Origin/Main Freshness Gate` is mandatory at the start of every new Codex thread, resumed thread, post-PR-merge handoff, post-watcher wakeup, and before any repo-affecting work continues. It applies before planning, patching, validation-green claims, phase entry or continuation, Branch Readiness, Workstream Entry, Workstream, Hardening, Live Validation, PR Readiness, Release Readiness, PR creation, merge handling, release work, branch/worktree mutation, runtime mutation, GitHub Desktop handoff, or same-branch current-main reconciliation.

The freshness packet must include:

- `Prompt-Entry Freshness Check:`
- `Fetched origin/main:`
- `Current Worktree:`
- `Current Branch:`
- `HEAD:`
- `Upstream:`
- `origin/main:`
- `Merge Base With origin/main:`
- `Origin/Main Advanced Since Last Action:`
- `Pre-Rebaseline Impact Audit Required:`
- `Rebaseline/Reconciliation Status:`

Passing posture means Codex fetched or otherwise proved current `origin/main`, the active worktree identity was verified, and `HEAD` plus merge base were compared against current `origin/main` before any phase continuation or mutation. If `origin/main` advanced, if the merge base differs in a way that requires review, or if current `origin/main` cannot be proven, Codex must stop on `Prompt-Entry Origin/Main Freshness Missing` or `Origin/Main Advanced Rebaseline Required`, return a report-only `Pre-Rebaseline Impact Audit` / reconciliation packet, and wait for the exact USER decision before any merge, rebase, fast-forward, branch switch, conflict resolution, file mutation, validation-green claim, PR readiness claim, release-readiness claim, or next-phase execution. Validating locally is not enough when `origin/main` may have advanced.

## Pre-Rebaseline Impact Audit

`Pre-Rebaseline Impact Audit` is mandatory before any branch, worktree, neutral-main folder, or standing governance lane merges, rebases, fast-forwards, conflict-resolves, branch-switches, or otherwise baselines itself against a newer `origin/main`.

No Baseline By Inertia: Codex must never treat "behind origin/main", "clean worktree", "already merged", "just housekeeping", or "fast-forward only" as approval to rebaseline without first reporting the audit and receiving USER approval for the recommended mutation path.

The audit packet must include:

- `Pre-Rebaseline Impact Audit:`
- `Incoming Main Change Set:`
- `Incoming Changed Files:`
- `Current Worktree Changed Files:`
- `Branch Changed Files:`
- `Rebaseline Overlap Files:`
- `Incoming Runtime / Source-Truth Risk:`
- `Shared Surface / Worktree Overlap Forecast:`
- `Validation Before Rebaseline:`
- `Recommendation Only:`
- `Rebaseline Mutation Approval:`
- `Rebaseline Mutation Status:`

`Recommendation Only:` must state that the pass reports findings and does not mutate the branch/worktree. `Rebaseline Mutation Approval:` must be `Pending` until the USER approves the exact worktree, branch, target commit, and operation type. `Rebaseline Mutation Status:` must remain `Not started` or `Blocked` until approval exists. If the worktree is dirty, if incoming files touch runtime/provider/UI/source-truth/validator surfaces, if sibling worktrees share files, or if validation fails, the next legal lane is a reported reconciliation decision rather than automatic baseline.

`Rebaseline Overlap Files:` is the intersection of incoming changed files and the current branch/worktree changed files. Current branch/worktree changed files means branch changed files from `merge_base..HEAD` plus staged, unstaged, untracked, or current-worktree changed files when present. When this field is `None`, `Rebaseline Overlap Intent Gate` reports `Not Applicable` and the normal Pre-Rebaseline Impact Audit still controls mutation approval. When this field names any file, Codex must freeze rebaseline mutation, classify every overlapping file, and inspect branch-owned intent before recommending merge, rebase, fast-forward, conflict resolution, or acceptance.

`Rebaseline Overlap Intent Gate` uses the active branch planning owner as the full-detail owner. Runtime branches use the Branch Runtime Engineering Plan shape. Branches with `Rebaseline Overlap Files:` must admit or update the active external Branch Engineering Plan under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` before rebaseline mutation can proceed. Repo branch-plan files under `Docs/branch_plans/` may provide schema, transition, or historical fallback evidence only; they must not be the active overlap-intent owner after the External Operational State Store transition. The required section is `Branch Change Intent Ledger`; each `Changed Surface: <path>` block records `Surface Class:`, `Change Intent:`, `Why This File Was Touched:`, `Owned Behavior / Fact Class:`, `Canonical Owner / Source Owner:`, `Resolution Owner:`, `Shared Surface:`, `Overlap Risk:`, `Expected Conflict Risk:`, `Semantic Merge Risk:`, `Regression / Gating Impact:`, `Conflict Resolution Rule:`, `Rebaseline Handling:`, `Validation Proof:`, `Fallback Evidence:`, `USER Decision / Waiver:`, and `Fold-Down Target:`. `Regression / Gating Impact:` uses `None`, `Low`, `Medium`, `High`, or `Unknown`; fixture/test overlap with `Medium`, `High`, or `Unknown` impact blocks until evidence or USER decision resolves it.

`Rebaseline Overlap Failure Procedure` triggers when an overlapping file has missing, weak, stale, or conflicting intent evidence. The packet must include `Overall Overlap Gate Result:`, `Rebaseline Overlap Files:`, per-file `File:`, `Surface Class:`, incoming and current branch change summaries, `Branch Change Intent Present:`, `Incoming Intent Evidence Present:`, `Fallback Evidence:`, `Risk:`, `Per-File Result: PASS / WARN / BLOCKED`, `Recommended Resolution:`, `Resolution Owner:`, `Validation Required:`, `USER Decision Needed:`, and `Rebaseline Mutation Status:`. `Overall Overlap Gate Result:` is the highest per-file severity. Any `BLOCKED` file keeps mutation blocked by `Rebaseline Overlap Intent Missing` until repaired, waived, deferred by USER decision, or sequencing changes. Fallback evidence supports classification and USER decision-making only; after the effective point, fallback evidence alone cannot produce `PASS`.

When the USER approves the recommendation, the rebaseline operation must still be constrained to the approved operation type, usually `git merge --ff-only origin/main` for neutral/main or standing-governance sync and an explicit merge/rebase/recreate strategy for active implementation branches. After the operation, `Current-Main Reconciliation Identity Guard` must prove origin/main stayed context, not identity, before validation, commit, push, PR Readiness, Release Readiness, or handoff.

### Merged Vision / Proof Standard Adoption Gate

Rule Name: `Merged Vision / Proof Standard Adoption Gate`
Owner: `Docs/phase_governance.md` for phase blocking; the affected Project Vision, Family Vision, Family Feature Vision, branch plan, validation registry, or incident-pattern owner for the standard being adopted.
Applies To: any active, paused, re-entering, or rebased worktree after `origin/main` receives merged source-truth changes that alter product vision, UI/UX standards, FFV sufficiency, deferred carryforward, proof hierarchy, Live Validation expectations, helper/validator interpretation, or USER review packet requirements.
Required State: The next legal BR1, BR2, BP1, BP2, BP3, Hardening, Live Validation, or PR Readiness packet for the affected worktree must report whether the merged standard applies to its existing branch work, list affected surfaces or claims, and either repair branch-local output, route back to the correct earlier gate, future-gate the impact with reason, or record an explicit USER waiver. This adoption check is a phase packet requirement, not a live-state ledger in repo docs.
Allowed Values: `Applies - Repair Required`, `Applies - Already Satisfied`, `Applies - Route Back To Earlier Gate`, `Applies - USER Waiver Required`, `Not Applicable With Reason`, `Blocked`.
Invalid Values: `Ignored Because Branch Started Earlier`, `Validator Green Before Standard`, `Will Reconcile Later Without Gate`, `Sibling Worktree Owns It`, `Repo Docs Track Current Adoption State`.
Blocking Conditions: `Merged Vision Standard Adoption Missing`, `Merged UI Standard Adoption Missing`, `Merged Proof Standard Adoption Missing`, `Rebaseline Adoption Impact Unclassified`, and `Repo File-State Tracking`.
Repair Owner: The affected worktree repairs its own branch-local surfaces under its own legal carrier. Standing Governance intake repairs reusable source-truth ambiguity. No worktree may mutate a sibling worktree to perform adoption by convenience.
Repair Path: During the next legal gate after rebaseline, compare branch output and plans against the new merged standard, name changed files/surfaces/claims, decide whether to repair now or route back, update only the owning branch-local source truth or external operational state allowed for that gate, and validate before advancing.
USER Decision Required: Required for waiver, route-back acceptance, broad scope expansion, sibling-worktree mutation, or applying the merged standard in a way that changes product/runtime behavior beyond current approval.
Validation Owner: Future helper/validator hardening should extend rebaseline, branch planning, PR Readiness, and Live Validation checks where machine-checkable. Until then, Codex must perform the comparison in the phase digest.
Final Disposition: A branch cannot rely on pre-rebaseline green proof when a newly merged vision/UI/proof standard applies and the adoption impact is unclassified.

## Branch Naming Prefix Rule

Active Nexus branch names and active branch authority records must not use the `codex/` prefix.
Use `feature/` or another USER-approved non-`codex/` prefix for current branch carriers.
Historical `codex/` branch names remain preserved traceability only and must not be treated as precedent for new or active branch naming.

## Canonical Phase Enum

The only normal branch phases are:

- `Branch Readiness`
- `Branch Planning`
- `Workstream`
- `Hardening`
- `Live Validation`
- `PR Readiness`
- `Release Readiness`

These are not normal phases:

- `No Active Branch`
- `Post-Release Canon Repair`

`No Active Branch` is a repo-level state, not a normal phase.
It may be:

- a blocked state when an admission gate or another required repair path is still open
- a steady-state resting posture when no implementation lane is currently selected and no branch should open by inertia

`Post-Release Canon Repair` is not a normal branch phase and is not a governance-only branch.
Codex must not use direct-main repair; `main` is protected and file-frozen for Codex work.

## Phase Alias UX Boundary

`Docs/governance_efficiency_operating_model.md` owns the governance efficiency operating model's human-facing alias map for phase names. The canonical phase names remain unchanged for source truth, validators, branch records, prompt contracts, and phase resolvers.

Aliases such as `Plan Review`, `Build`, `User Proof`, or `Release Validation` may explain a phase to the USER, but they must not replace canonical phase markers in repo files.

`Branch Planning` is the canonical phase between `Branch Readiness` and `Workstream`. It contains BP1, BP2, and BP3:

- BP1 - `USER Branch Vision Review`, using `USER_BRANCH_VISION_REVIEW.md`.
- BP2 - `USER Branch Plan Review`, using `USER_BRANCH_PLAN_REVIEW.md`.
- BP3 - `Workstream Entry / Orchestration Validation`.

`Workstream Entry` is BP3 inside `Branch Planning`; it is not inside `Workstream` and is not a standalone canonical phase. The `Workstream` phase begins only after BP1 and BP2 are accepted or explicitly waived, BP3 is green, and USER approves bounded Workstream implementation for the admitted same-branch package or explicitly named initial seam sequence. The first seam is the entry checkpoint, not stop authority.

### Implementation-Bearing Branch Standard

Rule Name: `Implementation-Bearing Branch Standard`
Owner: `Docs/phase_governance.md`
Applies To: Branch Readiness Stage 1, Branch Readiness Stage 2, BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, active external branch plans, local USER hub Branch Planning packets, helper output, validator output, and fixtures.
Required State: Branch Readiness Stage 2 is the legal stage for identifying infrastructure prerequisites, lane groundwork, missing private/public boundary setup, and route blockers before branch admission completes. Every runtime, product, source-truth, helper, validator, or governance repair branch admitted green from Branch Readiness Stage 2 must name a `Selected Implementation Route:` before BP1 begins. The selected route must be concrete enough for BP1 to define what the branch becomes, BP2 to plan how it will be built, BP3 to verify readiness to execute it, and Workstream to complete bounded implementation without inventing the branch purpose midstream.
Real Feature Implementation Definition: A real implementation route names the actual behavior, control, surface, state transition, workflow, source-truth enforcement, helper behavior, validator behavior, or runtime behavior that Workstream will create, change, or enforce. Proofs, packets, readiness matrices, registries, setup themes, boundary-control labels, decision paths, and validation plans are evidence or infrastructure unless they are tied to a named implemented control or behavior. A `boundary control` counts only when BP1/BP2 name the exact control and Workstream is expected to implement or enforce that control; a proof of a boundary is not the feature.
Deterministic Enforcement Preference: When a route-admission rule can be machine-checked, it should be backed by deterministic validator or fixture coverage. Simulation or fixture coverage must include prompt-like bypass attempts where implementation is deferred to BP2/TBD, proof packets are labeled as feature routes, or boundary-control language appears without a named implemented behavior. Semantic judgments that cannot be machine-checked must be called out as human review requirements instead of reported as validator-proof green.
Required Route Fields: `Selected Implementation Route:`, `Implementation Route Class:`, `Concrete Deliverable:`, `Implementation Output:`, `Infrastructure / Setup Relationship:`, `USER Action Gate:`, `Route Disposition:`, and `Retarget / Rename Recommendation:`.
Infrastructure / Setup Rule: lane setup, repo/root/remote setup, skeleton setup, packet generation, registry creation, manifest creation, or other groundwork is branch-worthy only when it is execution-enabling for the selected implementation route or when USER approves an exact setup action gate that names the allowed setup action and blocked actions. Creating User/Public, Developer, or Owner lanes by itself is groundwork, not a feature implementation carrier.
BR2 Blocker Packet Rule: If BR2 discovers that User/Public, Developer, or Owner lane work cannot proceed until infrastructure or groundwork exists, BR2 must stop with `Route Disposition: HOLD` or `Route Disposition: RETARGET / RENAME` and return a USER decision packet. That packet must name `Infrastructure / Lane Groundwork Blockers:`, `Required Before This Route Can Proceed:`, `Concrete Feature Routes Available Now:`, `Deferrable Groundwork:`, `Non-Deferrable Groundwork:`, `Codex Recommendation:`, and `Exact USER Decision Needed:`. USER may approve the prerequisite groundwork, defer it and select a different concrete worktree-focused feature route that can proceed now, rename/retarget the branch, or hold with No Active Branch. Repeated deferral is legal until the remaining candidate routes all depend on non-deferrable groundwork; at that point BR2 must report the exact non-deferrable blocker instead of inventing a planning-only carrier.
Invalid Route Shapes: planning-only carriers, readiness-only carriers, infrastructure-only carriers, lane-setup-only carriers, branches whose deliverable is to choose later implementation branches, branches whose BP2 can green with orchestration only, and branches that defer every concrete deliverable to a later branch without an exact USER action gate are invalid for BR2 admission.
Terminology Rule: Use `User/Public lane`, `Developer lane`, and `Owner lane` as lanes or environments, not product version numbers. New and current branch-planning text must say `Developer lane`, not `Dev lane`. Historical branch names, previously accepted private repo placeholders, and clearly marked receipts may preserve older wording only as traceability, not current lane law.
Blocking Conditions: `Implementation-Bearing Route Missing`, `Planning-Only Carrier`, `Infrastructure-Only Carrier`, `Exact USER Action Gate Missing`, `Branch Retarget/Rename Decision Required`, and `Developer Lane Terminology Drift`.
Repair Path: BR1 recommends continue, retarget, rename, or hold. BR2 investigates route prerequisites, presents blockers and options, and admits green only after the selected implementation route is named or USER explicitly chooses a legal setup/action-gate path. BP1, BP2, and BP3 serve that route. If the route changes, Codex must return to BR1/BR2 or BP1 as source truth requires instead of continuing Branch Planning by inertia.

### Family Feature Vision Scope And Element Proof Chain

Rule Name: `Family Feature Vision Scope And Element Proof Chain`
Owner: `Docs/phase_governance.md` for phase gates and blockers; `Docs/family_visions/README.md` for Family Feature Vision naming, compact ID, category scope, deferred carryforward, and owner relationship; `Docs/branch_plans/README.md` for branch-plan element traceability.
Applies To: Branch Readiness Stage 1, Branch Readiness Stage 2, BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, Workstream, Hardening, Live Validation, active external branch plans, Family Feature Vision files, USER review packets, helper output, validator output, and future fixtures.
Required State: A Family Feature Vision is a durable feature-category owner inside exactly one FAM. It must use a stable FFV ID or approved transition alias, a human-readable category title, a durable feature element inventory, deferred carryforward facts, proof expectations, and BP1 consumption notes. It must not be named or scoped as a branch route, Slice/SLC, seam, current implementation package, or live operational state record.
Allowed Values: `Category-Level FFV`, `Transition Alias Pending Rename`, `Feature Vision Not Applicable`, `FFV Repair Required`, `USER Decision Required`.
Invalid Values: `Slice-Specific FFV`, `SLC-Specific FFV`, `Seam-Specific FFV`, `Branch-Route FFV`, `Implementation-Package FFV`, `Selected-Next FFV`, `Active-State FFV`, `Live Branch Ledger FFV`.
Required FFV Inventory Rule: Before BP1 begins for a selected feature-bearing route, Codex must inventory all tracked `Docs/family_feature_visions/*.md` files in the owning worktree when the directory exists. The inventory must classify every FFV as `Valid Category-Level FFV`, `Rename / Reframe Required`, `Compact ID Missing`, `Pointer Migration Required`, `Live-State Wording Repair Required`, `Historical Transition Alias`, or `USER Decision Required`. If the current approval covers FFV content mutation, all affected FFVs in that worktree must be repaired or explicitly deferred with a blocker before BP1. If mutation is not approved, Codex must return the blocker and exact approval text.
Required Pointer Rule: Any FFV rename, compact-ID migration, or category reframe must update every in-scope source-truth pointer, branch record pointer, branch plan pointer, active external-state pointer, USER packet context pointer, backlog/roadmap pointer, and generated review reference that names the old FFV path or title. Stale references block on `Family Feature Vision Pointer Migration Missing`.
Required Element Rule: BP1 must classify relevant FFV elements as `Selected`, `Deferred`, or `Blocked` and explain grouping, deferral reason, dependency trigger, owner, proof expectation, and return path. BP2/BP3 must map selected elements to branch-local Slice/SLC/seam work, validation, proof, rollback, and future-gated boundaries. Workstream, Hardening, and Live Validation must carry selected element IDs forward until each implemented element is proven, waived, deferred, or blocked.
Required Proof Chain: `FFV element -> BP1 selected/deferred -> BP2/BP3 mapped to branch-local Slice/SLC/seam -> Workstream implemented -> Hardening inspected -> Live Validation proven -> USER packet evidence`.
External State Guardrail: Family Feature Vision files may own durable visioned elements, deferred facts, and proof expectations. They must not own active branch status, current selected-next state, current BP gate state, live branch lifecycle state, current worktree binding, implementation approval, live PR/release state, or active branch planning ledgers. Those facts belong to `C:\Nexus Governance State`, Git/GitHub/helper-derived truth, active Branch Planning packets, or USER decision packets as routed by source truth.
Blocking Conditions: `Family Feature Vision Required For Selected Feature`, `Feature Vision Sufficiency Check Failed`, `Family Feature Vision Slice-Scoped`, `Family Feature Vision Compact ID Missing`, `Family Feature Vision Inventory Repair Required`, `Family Feature Vision Pointer Migration Missing`, `FFV Live-State Leakage`, `FFV Element Selection Matrix Missing`, `FFV Element Proof Chain Missing`, `Deferred Carryforward Applicability Missing`, and `Deferred Carryforward Branch Sprawl`.
Repair Owner: owning family/worktree for FFV content repair; active branch-planning owner for selected/deferred element and proof-chain repair; standing Governance intake for source-truth rule repair; USER for new FFV content-file creation, rename, file movement, deletion, external-state mutation, or waiver decisions.
Repair Path: Reframe the FFV as a category-level feature owner, assign or preserve the compact ID/transition alias, repair the element inventory and deferred carryforward rows, update every pointer in the owning worktree and approved external records, regenerate USER review packets when they named the old FFV, and rerun the relevant validators. If the repair would mutate a sibling worktree, external state, helper code, validator code, or generated packet outside the current approval, stop and return the exact USER decision needed.
USER Decision Required: Required for first FFV folder/index creation, new FFV content files, FFV file renames, file movement, deletion, archival, sibling-worktree mutation, external-state pointer mutation, helper/validator implementation, or any waiver that lets BP1 proceed without a sufficient FFV for a selected feature-bearing route.
Validation Owner: Future helper/validator hardening should extend `dev/orin_branch_governance_validation.py`, `dev/orin_branch_readiness_planning_fixture_validation.py`, and `dev/orin_user_review_bundle.py`; green validation remains evidence and Codex must still inspect the actual FFV scope, pointers, and USER packet state.
Final Disposition: The branch may proceed to BP1 only when the relevant FFV is category-level, sufficient, pointer-consistent, no-live-state-clean, and element-selection-ready, or when source truth records a valid `Family Feature Vision Not Applicable` reason or explicit USER waiver.

### BR1 Candidate Viability / Grouping Matrix

Rule Name: `BR1 Candidate Viability / Grouping Matrix`
Owner: `Docs/phase_governance.md`
Applies To: Branch Readiness Stage 1 candidate selection, successor-branch analysis, family-scoped Branch Readiness, Branch Readiness packets that consume Family Feature Vision or Deferred Feature Carryforward, helper output, validator output, and future fixtures.
Required State: Before BR1 recommends USER-selectable branch candidates, it must provide a candidate viability and grouping matrix that proves each candidate is an implementation-bearing package option rather than a planning, readiness, manifest, setup, or support-only branch. The matrix is analysis evidence only; it must not create selected-next truth, active branch state, branch authority, PR state, or release-window state in repo docs.
Required Matrix Fields: `Option name`, `Owning FAM / worktree`, `Main feature/package objective`, `Concrete feature outcome`, `Implementation-bearing route class`, `Behavior change classification`, `Support / infrastructure relationship`, `Family Feature Vision context`, `Deferred Feature Carryforward consumed`, `Cross-FAM Dependency Map`, `Affected FAMs`, `Affected FFV / Element or Not Created`, `Shared Surface Overlap Forecast`, `Dependency Scope Class`, `Carry-In / Deferral / Transfer Decision`, `Platform Contract Adoption Matrix when applicable`, `Repo-Wide Migration Neutralization Proof when applicable`, `Grouping recommendation`, `Split reason if not grouped`, `Expected Slice/SLC/seam map`, `Proof path`, `Largest safe coherent package explanation`, `Tiny-branch sprawl review`, `Blockers`, and `Exact USER decision needed`.
Allowed Implementation-Bearing Route Classes: `User-visible behavior change`, `Runtime behavior change`, `Developer tooling behavior change`, `Source-truth enforcement change`, `Helper behavior change`, `Validator behavior change`, `Control / permission / policy behavior change`, or `Governance rule enforcement change`.
Invalid Candidate Shapes: planning-only branches, readiness-only branches, support-only branches, infrastructure-only branches, manifest-only branches, registry-only branches, proof-only branches, setup/skeleton-only branches without exact USER action gate, candidates whose purpose is to choose later candidates, candidates that defer every concrete deliverable to another branch, and tiny branches that split work when one FAM/package objective, owner/worktree, route, release timing, and validation path can safely carry the grouped scope.
Family Feature Vision Handling: If the candidate is a selected feature-bearing route and no sufficient USER-approved Family Feature Vision exists for the feature category, BR1 must report `Family Feature Vision Required For Selected Feature` and make the next legal phase Family Feature Vision planning/admission on the current legal carrier before BP1. If the candidate is governance-only, release-support, pure helper/validator, source-truth-only, or otherwise non-product, BR1 may report `Family Feature Vision Not Applicable` with a reason.
Deferred Feature Carryforward Handling: BR1 must identify deferred carryforward items from the relevant Family Feature Vision when that owner exists. For each option, BR1 must state which deferred items apply, why the dependency trigger is satisfied, which items remain future-gated, why they remain deferred, and whether the grouped option is the largest safe coherent package. Deferred carryforward is durable planning context; it is not selected-next truth and does not authorize implementation by itself.
Cross-FAM Dependency Handling: BR1 must identify cross-FAM dependency candidates that are relevant to each option, including dependencies discovered by the originating FAM and durable dependency candidates already recorded in the affected FAM or FFV. BR1 must classify each dependency using the `Cross-FAM Dependency And Shared Surface Overlap Model`, state whether the dependency is awareness-only, dependency-bounded, a priority carry-in, a platform contract, a coordinated cross-FAM patch, a repo-wide migration / halt, or transferred FAM work, and explain why the option can proceed, defer, narrow, transfer, or stop. Cross-FAM dependency analysis is durable planning evidence; it must not create selected-next truth, active branch state, current assignment, PR state, release-window state, or a repo-tracked live dependency ledger.
Grouping Rule: BR1 must recommend grouping support, infrastructure, helper, validator, source-truth, and deferred carryforward work into the selected implementation-bearing package when the work shares the same FAM, package objective, route, owner/worktree, release timing, risk class, and validation/proof path. If Codex recommends a split, the packet must name the split reason and the future owner. Missing split reason blocks on `BR1 Candidate Split Reason Missing`.
Blocking Conditions: `BR1 Candidate Implementability Missing`, `BR1 Candidate Grouping Matrix Missing`, `BR1 Planning-Only Candidate Drift`, `BR1 Support-Only Candidate Drift`, `BR1 Readiness-Only Candidate Drift`, `BR1 Manifest-Only Candidate Drift`, `BR1 Tiny-Branch Sprawl`, `BR1 Feature Vision Context Missing`, `BR1 Candidate Split Reason Missing`, `Implementation-Bearing Route Unproven`, `Cross-FAM Dependency Undocumented`, `Cross-FAM Dependency Scope Unclassified`, `Cross-FAM Carry-In Not Evaluated At BR1`, `Transferred FAM Work Requires Owning Branch`, `Affected FAM Receipt Missing`, `Platform Contract Adoption Matrix Missing`, `Repo-Wide Migration Neutralization Missing`, `Worktree-To-Worktree Mutation Approval Missing`, `FFV Dependency Candidate Missing`, and `Cross-FAM Dependency Fold-Down Missing`.
Repair Path: BR1 must revise the candidate matrix, group support work into a coherent implementation-bearing package, route to Family Feature Vision planning/admission, hold with No Active Branch, or return a USER decision packet before Stage 2. BR2 may admit only candidates whose BR1 matrix clears the blockers or records an explicit USER waiver/action gate.
Validation Owner: Future helper/validator enforcement should extend `dev/orin_branch_governance_validation.py` and `dev/orin_branch_readiness_planning_fixture_validation.py`; this docs-only pass does not authorize helper, validator, or fixture mutation.

### Cross-FAM Dependency And Shared Surface Overlap Model

Rule Name: `Cross-FAM Dependency And Shared Surface Overlap Model`
Owner: `Docs/phase_governance.md` for phase gates and blockers; `Docs/family_visions/README.md` for durable Family Vision / Family Feature Vision dependency candidate shape; `Docs/worktree_slots.md` for worktree mutation confinement; `Docs/feature_backlog.md` for compact taxonomy mirrors.
Applies To: Branch Readiness Stage 1, Branch Readiness Stage 2, BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, Workstream, Hardening, Live Validation, PR Readiness, active external branch plans, Family Vision records, Family Feature Vision records, USER review packets, helper output, validator output, rebaseline / reconciliation packets, and future fixtures.
Required State: A branch has one `Owning FAM` and one legal owning worktree. The branch may identify and, when admitted, perform dependency-bounded cross-FAM work only when that work is required for the owning FAM's selected implementation route, is smaller than a separate branch-worthy package for the affected FAM, has an explicit dependency ID, records the affected FAM / FFV / element or `Not Created`, and preserves proof, rollback, fold-down, and affected-FAM receipt expectations. Shared-file overlap between independently owned worktrees is legal when each branch owns its own reason for touching the shared surface and rebaseline / reconciliation handles the merge. Direct worktree-to-worktree mutation remains blocked unless USER grants a bounded waiver.
Allowed Values:

- `Local FAM Only`
- `Cross-FAM Awareness`
- `Dependency-Bounded Cross-FAM Work`
- `Priority Carry-In`
- `Platform Contract`
- `Coordinated Cross-FAM Patch`
- `Repo-Wide Migration / Halt`
- `Transferred FAM Work`

Invalid Values:

- `Unclassified Cross-FAM Dependency`
- `Hidden Dependency`
- `Another FAM As Dependency Queue`
- `Borrowed Branch Scope`
- `FAM-002 Generic UI Polish Carrier`
- `Worktree-To-Worktree Mutation`
- `Shared Surface Overlap Treated As Mutation`
- `Live Dependency Ledger In Repo Docs`
- `Repo File-State Tracking`

Shared Surface Overlap Safe Harbor: Shared-file overlap is not automatically cross-worktree work. Two FAM branches may independently touch the same repo file when each branch has a legal owning-FAM reason, records its intended write set in the active external branch plan, and resolves overlap through Pre-Rebaseline Impact Audit, Branch Change Intent Ledger evidence, PR Readiness, merge sequencing, and post-merge reconciliation. This safe harbor does not authorize one thread to edit another active worktree, assume another branch's scope, or hide cross-FAM dependency work as generic overlap.
FAM-002 Presentation Consumption Safe Harbor: FAM-002 is the shared Desktop Interface / UI presentation authority and may be consumed by other FAM branches without opening a FAM-002 worktree when the consuming branch owns the feature behavior and the UI work is necessary for its accepted Family Vision, Family Feature Vision, branch plan, and proof path. This safe harbor does not authorize generic app-wide UI polish, broad visual redesign, FAM-002 selected-next truth, another FAM's feature behavior, or direct sibling-worktree mutation. A dedicated FAM-002 branch requires USER admission of a concrete Desktop Interface feature category that no consuming FAM owns.
Worktree-To-Worktree Mutation Boundary: Worktree-to-worktree mutation means one thread edits, stages, commits, rebases, merges, cleans, validates-as-owner, or otherwise mutates another active worktree or branch. It is blocked by default on `Worktree-To-Worktree Mutation Approval Missing`, `Parallel Worktree Coordination Missing`, or `Governance Routing Barrier` unless USER explicitly approves a bounded waiver with scope, expiration, validation, and return path.
Dependency-Bounded Work Rule: The owning branch may carry bounded affected-FAM work only when BR1/BR2 prove the work is necessary for the owning route, does not become the affected FAM's whole branch objective, has a clear affected-FAM receipt / carry-in / fold-down target, and does not require direct sibling-worktree mutation. If the work becomes large, user-visible, architecture-defining, package-defining, or independently branch-worthy for the affected FAM, it must be classified as `Transferred FAM Work` and routed to that FAM's Branch Readiness path.
Priority Carry-In, Not Scope Capture: A platform contract or dependency candidate that creates required future work for an affected FAM must be evaluated by that FAM's next BR1. It does not automatically become the only branch objective; the affected FAM should group the carry-in into the relevant FFV or coherent package when practical and split only when the grouping would blur ownership, weaken proof, or create unsafe release timing.
Platform Contract Rule: Platform contract work defines a durable contract, compatibility default, schema, path, update/patch behavior, permission boundary, setup behavior, or adoption expectation other FAMs may consume later. The originating branch must prove existing affected families are not broken, document adoption classes, and avoid forcing every FAM to patch immediately unless the dependency is classified as `Coordinated Cross-FAM Patch` or `Repo-Wide Migration / Halt`.
Repo-Wide Migration / Halt Rule: A branch that changes install, update, patch, launch, repo split, external state, validation, reconciliation, or workflow assumptions broadly enough to affect multiple active FAMs must be admitted as `Repo-Wide Migration / Halt` before Workstream. BP3 must prove affected worktrees are neutral, clean, paused, or explicitly waived; Workstream may then perform only the admitted cross-FAM migration work in one carrier branch; Hardening and Live Validation must prove each affected FAM surface and return-digest / reconciliation path.
Implementation Ownership Split: The branch that introduces a dependency owns the introduced contract, compatibility default, and proof that existing affected families are not broken. The affected FAM owns later feature-specific adoption, FFV creation or repair, polish, expansion, and user-facing follow-through unless the current branch explicitly admits dependency-bounded affected-FAM work.
Repo / External State Boundary: Repo docs may record durable dependency classes, dependency candidates, source-truth owner rules, FFV element IDs, durable dispositions, fold-down receipts, and review requirements. Repo docs must not track live changed-file state, current branch status, current worktree assignment, selected-next truth, active dependency queues, PR state, release-window state, or mutable validation posture. Live operational state belongs to `C:\Nexus Governance State`, Git/GitHub/helper-derived truth, USER review packets, active external branch plans, or Codex digests as routed by source truth.
Blocking Conditions: `Cross-FAM Dependency Undocumented`, `Cross-FAM Dependency Scope Unclassified`, `Cross-FAM Carry-In Not Evaluated At BR1`, `Transferred FAM Work Requires Owning Branch`, `Affected FAM Receipt Missing`, `Platform Contract Adoption Matrix Missing`, `Repo-Wide Migration Neutralization Missing`, `Worktree-To-Worktree Mutation Approval Missing`, `FFV Dependency Candidate Missing`, `Cross-FAM Dependency Fold-Down Missing`, `Shared Surface Overlap Misclassified`, `FAM-002 Presentation Consumption Ambiguous`, and `Repo File-State Tracking Regression`.
Repair Owner: owning branch/worktree for dependency classification and branch-local proof; affected FAM/worktree for future adoption and FFV content repair; standing Governance intake for source-truth rule repair; USER for cross-worktree mutation waivers, repo-wide migration / halt admission, new worktree creation, or transferred FAM branch admission.
Repair Path: Classify the dependency, identify the owning and affected FAMs, record the dependency candidate or affected-FAM receipt, update BR1/BR2 matrices, move live operational facts to external state or helper evidence, route branch-worthy affected-FAM work to that FAM, clarify whether FAM-002 is supplying presentation law or attempting to own implementation, or request USER approval for a coordinated cross-FAM patch / repo-wide migration / halt. If direct sibling-worktree mutation would be required, stop and return the exact USER decision needed.
USER Decision Required: Required for worktree-to-worktree mutation, repo-wide migration / halt admission, transferred FAM branch creation, new worktree creation, external-state mutation beyond approved branch planning, helper/validator implementation, or any waiver that lets dependency-bounded work proceed without the required classification, proof, or affected-FAM receipt.
Validation Owner: Future helper/validator hardening should extend `dev/orin_branch_governance_validation.py`, `dev/orin_branch_readiness_planning_fixture_validation.py`, `dev/orin_worktree_rebaseline_audit.py`, and `dev/orin_user_review_bundle.py`. Green validation is evidence only; Codex must still inspect dependency scope, overlap classification, active-state leakage, and USER decision state.
Final Disposition: A branch may proceed only when cross-FAM dependencies are classified, shared-surface overlap is documented without becoming live repo state, direct worktree mutation is absent or USER-waived, affected-FAM receipts / carry-ins are preserved, and any platform contract or repo-wide migration proof required by the selected dependency class is present.

### Runtime Failure / Recovery Carrydown Gate

Rule Name: `Runtime Failure / Recovery Carrydown Gate`
Owner: `Docs/phase_governance.md` for phase gates and blockers; `Docs/family_visions/FAM-001_boot_interface.md` for fatal launcher/runtime diagnostics and future recovery-surface vision; `Docs/workstreams/FB-034_recoverable_diagnostics.md` for historical bounded `launch_failed` evidence only; `Docs/family_visions/FAM-002_desktop_interface.md` for visible diagnostics/failure panel presentation standards; the consuming FAM / FFV / active external branch plan for feature-specific failure, degraded, blocked, unavailable, and proof behavior.
Applies To: Branch Readiness Stage 1, Branch Readiness Stage 2, BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, Workstream, Hardening, Live Validation, PR Readiness, Family Vision records, Family Feature Vision records, active external branch plans, USER review packets, helper output, validator output, and future fixtures when a branch creates, changes, exposes, routes, diagnoses, degrades, blocks, launches, recovers, retries, repairs, or validates runtime/user-facing behavior.
Required State: Every relevant branch must classify how its feature behaves when it fails, degrades, is blocked, is unavailable, or cannot launch. The packet or active external branch plan must name `Failure Class:`, `USER-Facing Failure State:`, `Recovery Option:`, `Fallback Behavior:`, `Support / Log / Bundle Behavior:`, `Privacy / Safety Boundary:`, `Photo / Video Or USER Manual Proof:`, `Owning FAM:`, and `Consumed Failure / Recovery Rules:`. Fatal launcher/runtime diagnostics and recovery surfaces route to FAM-001. Bounded repeated recoverable `launch_failed` evidence routes to FB-034 only as released historical evidence until USER admits a new owner. Visible diagnostics or failure panels consume FAM-002 presentation standards. Feature-specific disabled, degraded, blocked, no-data, unavailable, provider/privacy, setup, repair, or retry behavior remains owned by the FAM whose feature surface is changing.
Allowed Values:

- `Fatal Launcher / Runtime Failure`
- `Recoverable Action / Launch Failure`
- `Degraded But Running`
- `Blocked By Policy`
- `Disabled / Deferred Feature`
- `Unavailable Prerequisite`
- `No Failure Surface Impact`

Invalid Values:

- `Unclassified Failure Behavior`
- `FB-034 As Active Product Owner`
- `Fatal Path Collapsed Into Recoverable Popup`
- `Recoverable Path Treated As Fatal Crash`
- `Hidden Failure`
- `Helper PASS As Recovery Proof`
- `Logs Only As USER-Facing Proof`
- `Generic Fallback`
- `Support Bundle Without Privacy Boundary`
- `Feature Failure Owned By Another FAM`

Future FAM-001 FFV Route: The actual user-facing diagnostics/recovery/support surface should be admitted through a later USER-approved FAM-001 Family Feature Vision, with candidate titles such as `F1-FF01 Runtime Diagnostics And Recovery Surface` or `F1-FF01 Failure Recovery And Support Reporting`. That future FFV may define fatal launcher failure, repeated recoverable failure, startup abort, recovery exhaustion, support-bundle preparation, manual issue draft, privacy warning, retry/close/repair options, and proof expectations. This gate does not create that FFV file or open a FAM-001 worktree by itself.
Blocking Conditions: `Runtime Failure / Recovery Carrydown Missing`, `Failure Class Unclassified`, `USER-Facing Failure State Missing`, `Recovery Option Missing`, `Fallback Behavior Missing`, `Support / Log / Bundle Boundary Missing`, `Privacy / Safety Boundary Missing`, `Failure Proof Path Missing`, `FAM-001 Diagnostics Ownership Bypassed`, `FB-034 Historical Evidence Misused As Active Owner`, `FAM-002 Failure Panel Presentation Missing`, and `Feature-Specific Failure Ownership Ambiguous`.
Repair Owner: The current branch/worktree repairs feature-local failure behavior and proof classification; standing Governance intake repairs reusable phase/source-truth rule drift; FAM-001 owns future diagnostics/recovery surface planning when USER admits it; FAM-002 owns reusable visual/presentation standards; the USER owns any waiver that allows a branch to proceed without the required failure/recovery classification.
Repair Path: Classify the failure class, identify FAM-001/FAM-002/consuming-FAM responsibilities, route fatal/recovery-surface product work to future FAM-001 FFV planning when needed, keep FB-034 as historical evidence unless a new branch admits a broader recoverable diagnostics scope, add feature-local degraded/blocked/unavailable behavior and proof expectations to the active branch plan, or stop for USER decision when ownership or proof remains ambiguous.
USER Decision Required: Required for new FAM-001 FFV content-file creation, new diagnostics/recovery implementation, helper/validator enforcement, support-bundle behavior changes, privacy/support reporting behavior changes, broad recoverable diagnostics expansion, fatal launcher/runtime behavior changes, or any waiver of this carrydown gate.
Validation Owner: Future helper/validator hardening should extend `dev/orin_branch_governance_validation.py`, `dev/orin_branch_readiness_planning_fixture_validation.py`, live-validation helpers, and diagnostics/recoverable-failure validators where machine-checkable. Green validation is evidence only; Codex must still inspect failure/recovery ownership, privacy boundary, and visible proof.
Final Disposition: Workstream, Hardening, Live Validation, and PR Readiness may proceed only when relevant failure/recovery behavior is classified, owner-routed, user-facing proof is planned or captured, and no branch is silently relying on logs, helper output, historical FB-034 evidence, or another FAM to own its feature-specific failure state.

### Visual Inheritance Matrix Gate

Rule Name: `Visual Inheritance Matrix Gate`
Owner: `Docs/phase_governance.md` for phase gates and blockers; `Docs/nexus_vision.md` for Project UI Vision; `Docs/family_visions/FAM-002_desktop_interface.md` for reusable presentation standards; the owning Family Vision / Family Feature Vision / active external branch plan for feature-specific UI grammar and proof.
Applies To: Branch Readiness Stage 1, Branch Readiness Stage 2, BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, Workstream, Hardening, Live Validation, PR Readiness, USER review packets, helper output, validator output, and future fixtures when a branch creates or changes user-facing UI, controls, windows, cards, HUDs, overlays, setup flows, status indicators, folder pickers, evidence surfaces, diagnostics panels, or failure/recovery panels.
Required State: The branch must include a `Visual Inheritance Matrix` before Workstream implementation when visible UI changes are admitted. Each row must name `New / Changed Element:`, `Surface Classification:`, `Inherited Existing Element Or Surface:`, `Owning UI Rule:`, `FAM-002 Component Grammar:`, `Window Chrome / Frame Treatment:`, `Platform Exception:`, `Shape / Radius Comparison:`, `Spacing / Density Comparison:`, `Typography Comparison:`, `Card / Row / Divider Treatment:`, `Color / Shadow / Glow Treatment:`, `Hover / Focus / Disabled State:`, `Scrollable / Resize / Transient State Proof:`, `Allowed Exception Or New Grammar:`, `Proof Artifact:`, and `Verdict:`. If no existing element is a valid ancestor, the branch must say why and record the USER-approved new visual grammar before implementation.
Allowed Values:

- `Inherited`
- `Inherited With Explicit Exception`
- `New Grammar USER Accepted`
- `Nexus-Owned Product Surface`
- `Platform-Native Exception`
- `Diagnostic / Developer Surface`
- `External Surface`
- `Not Applicable`
- `Needs Repair`
- `USER Decision Required`

Invalid Values:

- `Helper Green`
- `Looks Fine`
- `Generic Nexus Style`
- `No Comparison Needed`
- `Screenshot Exists`
- `Marker PASS`
- `Deferred Visual Review`
- `FAM-002 Owns It`
- `Default OS Chrome By Accident`
- `Native Title Bar Accepted By Inertia`
- `Window Chrome Not Inspected`
- `Surface Class Assumed`
- `Platform Exception By Inertia`

Blocking Conditions: `Visual Inheritance Matrix Missing`, `Existing Element Sample Missing`, `Visual Exception Not USER Accepted`, `Helper Green Treated As Visual Proof`, `Screenshot Without Adjudication`, `Per-Element Visual Verdict Missing`, `FAM-002 Presentation Consumption Missing`, `Feature UI Ownership Ambiguous`, `NDAI Window Chrome Missing`, `Default OS Chrome Used Without Exception`, `Nexus-Owned Surface Classification Missing`, `Platform Exception Unclassified`, `FAM-002 Component Grammar Missing`, and `Obvious UI Failure Passed To USER`.
Repair Owner: The current branch/worktree repairs branch-local UI and proof; FAM-002 supplies reusable presentation law but does not take over the feature implementation; standing Governance intake repairs reusable rule drift; USER decides deliberate new grammar or waiver.
Repair Path: Identify the inherited element, compare the required visual dimensions, repair mismatches before USER handoff when approval covers repair, route deliberate new grammar through BP1/BP2/BP3 and USER acceptance, or return a blocker instead of asking USER to rediscover obvious UI defects during UTS.
USER Decision Required: Required for a new visual grammar, broad app-wide redesign, waiver of visual inheritance proof, or FAM-002 branch admission.
Validation Owner: Future helper/validator hardening should extend branch-readiness fixture validation, USER review bundle validation, visual proof/live-validation helpers, and source-owner checks where machine-checkable. Green validation is evidence only; Codex must still inspect the actual visual artifacts and compare them to the matrix.
Final Disposition: A user-facing UI branch is not ready for UTS handoff, PR Readiness, or release-facing closeout while unwaived visual matrix rows are missing, unproven, or inconsistent with screenshots/video/frame evidence.

### Evidence Independence / Anti-Circular Validation Gate

Rule Name: `Evidence Independence / Anti-Circular Validation Gate`
Owner: `Docs/phase_governance.md` for phase blocking; `Docs/validation_helper_registry.md` for helper/validator interpretation; `Docs/branch_plans/README.md` for branch proof-plan shape; the applicable vision owner for product claim source truth.
Applies To: BR1, BR2, BP1, BP2, BP3, Workstream, Hardening, Live Validation, PR Readiness, USER packets, helper output, validator output, and Codex closeout claims when a branch claims a product, UI, runtime, vision, proof, or phase-gate result is green.
Required State: Each gate-relevant claim must name the claim, source-truth owner, independent evidence source, evidence class, limitation, Codex adjudication result, and next disposition. A branch may use its own BP1/BP2/BP3 plan to define expected behavior, but it may not use that same plan, marker presence, helper green, generated manifest, screenshot existence, or Codex assertion as the only proof that the behavior or UI actually satisfies the vision.
Allowed Values:

- `Independent Evidence Present`
- `Supporting Evidence Only`
- `Manual USER Validation Required`
- `USER Waiver Required`
- `Not Applicable With Reason`
- `Repair Required`

Invalid Values:

- `Claim Proven By Own Plan`
- `Green Because Helper Passed`
- `Screenshot Exists Therefore Accepted`
- `Manifest Exists Therefore Accepted`
- `Vision Cited But Not Compared`
- `Self-Attested`

Blocking Conditions: `Circular Validation Detected`, `Claim Proven By Own Plan`, `Independent Evidence Missing`, `Vision Proof Alignment Missing`, `Helper Green Treated As Product Proof`, `Screenshot Without Adjudication`, `Manifest Treated As Acceptance Proof`, and `Manual USER Validation Not Elevated`.
Repair Owner: The current branch/worktree repairs branch-local proof gaps; standing Governance intake repairs reusable rule drift; helper/validator owners repair confirmed false-green or false-red tooling; USER decides waivers or manual validation.
Repair Path: Identify the claim, cite the source-truth owner, gather independent evidence from runtime behavior, visual artifacts, real user-path interaction, code/diff review, Git/GitHub live truth, helper output, or USER manual validation as appropriate, record limitations, and classify every unresolved claim as `Repair Required`, `Manual USER Validation Required`, `USER Waiver Required`, or `Blocked`.
USER Decision Required: Required to waive independent proof, accept manual validation as the final evidence layer, approve a deliberate UI/vision exception, or expand helper/validator implementation.
Validation Owner: Future helper/validator hardening should extend branch governance validation, branch-readiness fixture validation, USER review bundle validation, visual/live-validation helpers, and source-owner checks where machine-checkable. Green validation is evidence only; Codex must still review the actual claim/evidence relationship.
Final Disposition: Phase advancement, UTS handoff, PR Readiness, and release-facing closeout are invalid when a material claim is circularly proven, unadjudicated, or supported only by the artifact that made the claim.

### Branch / Slice / SLC / Seam Terminology Model

Rule Name: `Branch / Slice / SLC / Seam Terminology Model`
Owner: `Docs/phase_governance.md`
Applies To: Branch Readiness, Branch Planning, Workstream, active external branch plans, backlog/workstream package trace, local USER hub planning packets, helper output, validator output, fixtures, and historical receipts that use SLC identifiers.
Branch Definition: A branch is the coherent implementation carrier admitted through Branch Readiness. It must carry one selected implementation route, one owning branch/worktree authority, and one bounded package objective. A branch is not a planning loop, a placeholder for choosing future branches, or a container for unrelated family/package work.
Slice Definition: `Slice` is the canonical package deliverable unit. A slice is a traceable deliverable area inside one admitted package under one FAM; it must name the concrete deliverable, FAM/package relationship, admission posture, completion state, and seam trace when it is active or folded down.
SLC Classification: `SLC` is the current branch-planning alias for a Slice-level implementation line item or historical slice ID. It is not a separate backlog identity, not a seam, and not automatic branch-split authority. Current BP2/BP3 packets may keep labels such as `SLC / Seam Plan:` and historical IDs such as `SLC-051` for traceability, but their meaning must resolve to Slice-level deliverable trace. New source truth should prefer `Slice` when naming canonical package deliverables and may include `SLC` only as an alias or historical trace label.
Seam Definition: `Seam` is the execution or validation checkpoint inside or between slices. A seam is the current bounded checkpoint Codex executes and validates; it cannot replace the slice deliverable, cannot become the branch identity, and cannot authorize stopping while the slice or package remains incomplete.
Relationship Rule: BP1 may mention slices/SLCs/seams only as later implementation staging, because BP1 is the vision gate. BP2 maps the accepted or waived BP1 route into Slice/SLC deliverables, seam sequence, files, validators, proof, rollback, risks, and USER gates. BP3 verifies the BP2 slice/seam map against BP1 and returns Workstream entry approval only for the admitted same-branch package. Workstream executes one active seam at a time and keeps moving through the accepted slice chain until Workstream Green, a real blocker, future dependency, or explicit USER waiver is recorded.
Multi-Slice Branch Rule: Multi-slice branches are legal when the slices share one FAM, one package objective, one selected implementation route, one owner/worktree, aligned release/PR timing, and a validation/proof path that can cover the grouped scope. A branch should split when family ownership, package objective, implementation route, private/runtime/provider action gate, release timing, validation path, risk class, or ownership diverges enough that one bounded Workstream package would blur authority or weaken proof.
Terminology Drift Blockers: `SLC / Slice / Seam Ambiguity`, `SLC Treated As Seam`, `SLC Treated As Separate Branch`, `Slice Treated As Proof Artifact`, `Seam Treated As Branch Deliverable`, and `Multi-Slice Package Shape Unproven`.
Validation Preference: Machine-checkable packets and fixtures must reject ambiguous SLC/Slice/Seam language, fake feature labels, proof/setup/boundary labels posing as implementation, planning-only lane setup, first-seam-only Workstream entry, and multi-slice packages that omit shared FAM/package/route/owner/validation evidence.

### Branch Planning Review Gate State Model

Rule Name: `Branch Planning Review Gate State Model`
Owner: `Docs/phase_governance.md`
Applies To: BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, local USER hub packets, branch planning digests, branch records, branch plans, helper output, and validator output.
Required State: Branch Planning gate evidence must track two independent axes: `Packet Reviewability State` and `USER Gate State`.
Allowed Values:

- `Packet Reviewability State`: `Missing`, `Generated`, `Validation Failed`, `Reviewable`, `Stale`, `Superseded`
- `USER Gate State`: `Pending USER Review`, `USER Revision Requested`, `USER Accepted`, `USER Approved`, `USER Waived`, `USER Rejected`, `USER Blocked`, `Superseded`

Invalid Values: `Implementation-ready`, `validated`, `green`, `generated`, `reviewable`, helper `PASS`, validator `PASS`, Codex agreement, ChatGPT agreement, or packet file-count proof must not be used as USER acceptance, USER waiver, USER approval, or Workstream implementation authority.
Blocking Condition: `Packet Validation Treated As USER Acceptance`, `Review Gate Bypass`, `USER Review Packet Phase-State Conflict`, `USER Review Packet Not Digested`, `Branch Planning Acceptance Receipt Missing`, `Helper False Green On Review Gate State`, or `Codex Digest Conflicts With USER Packet` blocks progression whenever the two axes conflict or when Codex asks for a later gate without accepted/waived prior USER gate proof.
Repair Owner: The current branch/worktree owner repairs branch-local review packets; reusable failures route to the standing Governance intake lane and update `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, `Docs/validation_helper_registry.md`, and helper/fixture owners when machine-checkable.
Repair Path: regenerate or repair the USER packet until `Packet Reviewability State: Reviewable`, return the packet to USER, digest the USER response, record the receipt, then set `USER Gate State` to the legal USER disposition. Chat-only correction text cannot replace the packet receipt.
USER Decision Required: Required for `USER Accepted`, `USER Approved`, `USER Waived`, `USER Rejected`, and any revision closure that changes branch vision, branch plan, Workstream orchestration, scope, or implementation authority.
Validation Owner: `dev/orin_user_review_bundle.py`, `dev/orin_branch_governance_validation.py`, and `dev/orin_branch_readiness_planning_fixture_validation.py` validate reusable packet shape and false-green regressions; their output is evidence, not USER acceptance.
Final Disposition: A Branch Planning gate exits only through a recorded USER disposition or a named blocker. A `Reviewable` packet starts USER review; it does not complete USER review.

Transition Rule:

- BP1.1 prepares and repairs `USER_BRANCH_VISION_REVIEW.md` until `Packet Reviewability State: Reviewable`.
- BP1.2 is the USER Branch Vision Review Gate with `USER Gate State: Pending USER Review` until USER responds.
- BP1.3 records `USER Accepted`, `USER Waived`, `USER Rejected`, `USER Revision Requested`, or `USER Blocked` before BP2 preparation.
- BP2.1 prepares and repairs `USER_BRANCH_PLAN_REVIEW.md` only after BP1 is `USER Accepted` or `USER Waived`.
- BP2.2 is the USER Branch Plan Review Gate with `USER Gate State: Pending USER Review` until USER responds.
- BP2.3 records `USER Accepted`, `USER Waived`, `USER Rejected`, `USER Revision Requested`, or `USER Blocked` before BP3 preparation.
- BP3.1 prepares and repairs Workstream Entry / Orchestration Validation only after BP1 and BP2 are `USER Accepted` or `USER Waived`.
- BP3.2 is the USER Workstream Entry / Orchestration Review Gate with `USER Gate State: Pending USER Review` until USER responds.
- BP3.3 records `USER Approved`, `USER Waived`, `USER Revision Requested`, or `USER Blocked` before first Workstream implementation approval may be requested.
- Workstream implementation remains blocked until BP1 is `USER Accepted` or `USER Waived`, BP2 is `USER Accepted` or `USER Waived`, BP3 is `USER Approved` or `USER Waived`, and USER separately approves bounded Workstream implementation for the admitted same-branch package or explicitly named initial seam sequence.

## Cross-Phase Rules

- repo canon is the detailed authority
- prompt and instruction layers should mirror the same exact phase names rather than aliases
- active promoted workstream docs are the single authoritative phase owners for their lane
- backlog, roadmap, and prompts may reference phase state but must not override the workstream doc
- a phase must never be inferred from user intent alone
- if the validation contract, timeout contract, harness behavior, active seam, or blocker set changes materially during late-phase work, canon must be updated before continued execution is recommended
- auxiliary guidance docs should be timeless by default and must not quietly become current-state owners

## Governed Output State Contract

For phase-sensitive execution in `Branch Readiness`, `Branch Planning`, `Workstream`, `Hardening`, `Live Validation`, or `PR Readiness`, Codex must not rely on generic headings such as `Results` or `Validation` alone.

The response or status handoff must explicitly report:

- `Seam Status:`
- `Slice Status:`
- `Completion Status:`
- `Blockers:`
- `Waiver Status:`
- `Continue Decision:`
- `Continuation Execution Latch:`
- `Stop Basis:`

`Green` means complete for the level it names.
A green seam does not authorize stop while `Slice Status` is not green.
A green slice does not authorize stop while `Completion Status` is not green.
A green seam or green slice is continuation proof, not Hardening authority, while any admitted same-branch seam or slice remains implementable; the next legal unit is the next named Workstream seam or the next admitted slice.

`Completion Status` is the `Workstream`-level bounded gate:
It is the exact `Phase: Workstream Status` field for stop authority.

- `In Progress` = more same-branch `Workstream` work remains and continuation is required
- `Red` = a named blocker or waiver currently stops bounded `Workstream` continuation
- `Green` = every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; `Workstream` backlog completion is proven complete and `Hardening` is the next legal phase

`Phase: Workstream` must remain bounded at all times.
The only lawful `Workstream` stop conditions are:

- `Completion Status: Green`, with `Hardening` as the next legal phase
- `Completion Status: Red`, justified by a named blocker or waiver

`Phase: Workstream` must remain bounded at all times, and the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.

`Phase: Workstream` must remain bounded at all times; the only lawful `Workstream` stop conditions are `Completion Status: Green` with `Hardening` next, or `Completion Status: Red` justified by a named blocker or waiver.

Phase Boundary Stop Required: A phase-exit seam named in `Next Active Seam` is a handoff target, not current-phase execution authority.
Bounded Workstream continuation ends at phase boundaries; it never crosses from Workstream into Hardening by inertia.
Codex must not execute Hardening, Live Validation, PR Readiness, Release Readiness, release work, or any other next phase in the same run unless USER explicitly admits that phase after reviewing the handoff.

Crossing into a new seam, slice, seam family, slice family, or work family is not stop authority by itself.

If `Completion Status` is `In Progress` and no named stop-authorizing blocker or waiver is recorded, `Continue Decision` must be `Continue` and Codex must start the next seam or next admitted slice instead of returning `Await Next Instruction`.

`Await Next Instruction` is only legal in `Workstream` when `Completion Status: Green`, or when `Completion Status: Red` is justified by a named blocker or waiver.

`Backlog Completion Unproven` keeps the branch in `Workstream`; by itself it is not authority to return `Await Next Instruction` while `Completion Status` remains `In Progress`.
`Backlog Completion Unproven` is a completion latch, not a stop-authorizing Workstream blocker.
After Workstream execution is admitted for a multi-seam or multi-slice package, the approval covers bounded execution of the admitted same-branch Workstream package unless USER explicitly records a single-seam waiver, backlog split, or named stop condition. `First Bounded Implementation Seam Approval Missing`, `Next Bounded Seam Approval Missing`, `SLC implementation pending USER approval`, or equivalent per-seam approval-missing / approval-pending wording is not a real blocker. Bounded Workstream execution continues one active seam at a time until Workstream Green, a real named blocker, or an explicit USER waiver is recorded.

Before any final response during `Workstream`, Codex must run a `Post-Seam Continuation Self-Audit` against the governed markers it just wrote or validated. If `Completion Status: In Progress` and `Continue Decision: Continue`, the self-audit result must be `Continue Same Workstream` and Codex must start the next active Workstream seam in the same bounded run. If Codex cannot start the next seam after that self-audit, it must record `Completion Status: Red` with the exact named blocker or USER waiver needed; it must not return a green seam closeout as terminal.
Use these governed state markers as execution control, not as documentation-only summary fields.
If `Continue Decision` is `Continue`, Codex must not end on a final seam-closeout response, rollback path, or next-seam recommendation; it must keep executing until a lawful `Stop` decision exists.
A prompt `Return:` block is an output shape only; it cannot override governed continuation markers or authorize a terminal response while `Continue Decision` remains `Continue`.
A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
If `Completion Status` is `In Progress`, `Next Active Seam` must remain a `Workstream` seam; phase-exit seams require `Completion Status: Green`, `Completion Status: Red` with a named blocker/waiver, or explicit USER single-seam/backlog-split waiver.
If `Completion Status` is `Red`, `Continuation Action` must explicitly state the blocker-clearing action or waiver-clearing action needed before bounded `Workstream` continuation may resume.
Single-seam or single-slice Workstream authority is forbidden unless explicit USER waiver text is recorded.
If only one seam or one slice is planned or visible, stop immediately on `Single-Seam Or Single-Slice Workstream Blocker` until Branch Readiness expands the plan or USER grants a waiver.
Only USER can grant a single-seam or single-slice Workstream waiver; Codex, ChatGPT, validators, prompt wording, clean validation, or a green seam cannot infer it.
A Workstream with `Completion Status: In Progress` and no waiver must show remaining same-branch implementable work beyond the current seam.

`User Test Summary Results Pending` is not a Workstream stop condition.
Workstream may plan manual user acceptance and may prepare later UTS strategy content, but formal UTS export, returned-result digestion, and the `User Test Summary Results Pending` blocker belong to `Live Validation Stage 1`.
User Test Summary is exclusive to Live Validation Stage 1.
Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.
PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact.
If user-facing implementation is not product-complete, Workstream must continue implementation, internal sandbox validation, and branch-local proof instead of asking the USER to complete a UTS as the Workstream completion gate.

## Canonical Governance Rules

### Source-Of-Truth Enforcement

- `Docs/phase_governance.md` is the repo-wide authority for exact phase names, blocker rules, proof governance, timeout governance, seam governance, stop-loss rules, branch classes, the Governance Drift Audit, and the phase resolver contract
- workstream docs must consume this model rather than redefining repo-wide process rules locally
- workstream docs may record branch-local validation contracts, tighter time budgets, active seams, artifact references, and explicit waivers, but those narrower contracts must be explicit

### Source-Truth Placement Preflight

Before Codex creates a new governance/source-truth file, active artifact, ledger, registry, or durable authority surface, it must perform a `Source-Truth Placement Preflight`.

The preflight must report:

- existing authority owner for the concept
- whether the change extends an existing owner or needs a new artifact
- why workstream docs, branch records, backlog, roadmap, validation helper registry, family dossiers, Element Coverage, or phase governance are insufficient if a new artifact is recommended
- whether a new artifact would duplicate, conflict with, or bypass an existing owner
- validator updates needed to prevent placement drift

Default rule: extend the existing owner first. A new active source-truth file requires a clear `No Existing Owner Fits` finding or an explicit companion-file pointer from the owning workstream doc or branch authority record.

When the proposed concept touches backlog identity, family vision, architecture, cross-family policy, experience design, runtime subsystem behavior, capability-pack domains, AI-native planning, or AI operational cache behavior, the preflight must also run the `Backlog Taxonomy And Source-Truth Placement Gate` from `Docs/feature_backlog.md`. The packet must classify the concept as exactly one or more of `Backlog family`, `Family vision`, `Architecture layer`, `Cross-family policy owner`, `Experience layer`, `Runtime subsystem`, `Capability-pack domain`, or `Package/slice/seam`; name rejected owner classes; name existing owner files to extend first; and state whether USER approval is required for any new backlog family or new source-truth owner. Missing or ambiguous classification blocks on `Backlog Taxonomy Gate Missing`; creating a new FAM without explicit USER approval remains blocked on `Backlog Addition User Approval Missing`.

AI Operational Cache Governance must not be promoted as a new FAM by inertia. Cache is not memory: cache is operational, purpose-bound, explainable, clearable, and policy-governed, while memory is durable user-personal knowledge and requires separate explicit consent. Cross-family cache architecture, replay safety, provenance, invalidation, Trust Journal cache events, and policy placement route through `Docs/ai_runtime_and_trust_architecture.md`; family-specific cache placement routes through existing FAM-007 AI/runtime/capability-pack owners, FAM-008 setup/install/cache-root UX owners, the relevant implementing family vision for local data/privacy implications, and the active external branch planning owner for implementation-specific cache behavior. Any further new AI architecture or policy owner is legal only after the placement preflight records `No Existing Owner Fits` or USER approves a companion source-truth file.

### Codex Plugin / Connector Use Boundary

`Docs/governance_efficiency_operating_model.md` owns the `Codex Plugin / Connector Evidence Split Compatibility Contract`. Phase governance consumes that contract as a phase-gate boundary.

Codex app plugins and connectors may support any phase only as evidence tools inside the existing phase machine. They do not create a new phase, bypass Branch Readiness / Branch Planning / Workstream / Hardening / Live Validation / PR Readiness / Release Readiness, waive USER gates, authorize implementation, or clear blockers by themselves.

Before Codex relies on a plugin or connector for phase advancement, PR readiness, release readiness, source-truth repair, provider/API setup, private/public boundary work, or governed review evidence, the phase packet must include `Plugin / Connector Use Plan:` with tool, use case, phase/stage, authority class, read/write mode, mutation risk, privacy/secret risk, expected evidence, evidence owner, fallback, USER approval requirement, and repo persistence.

`Plugin / Connector Use Plan Missing`, `Plugin Evidence Treated As Source Truth`, `Plugin Live-State Ledger In Repo`, `Sensitive Connector Setup In Repo`, and `External Plugin Evidence Schema Premature` block phase advancement when applicable.

GitHub connector PR facts remain Git/GitHub/helper-derived live truth. OpenAI Docs lookups are evidence for durable rule review. OpenAI Developers/API key/provider setup is sensitive setup state and remains blocked unless USER approves that exact setup path. Browser, Chrome, Computer Use, Documents, Spreadsheets, and Presentations outputs are review or validation evidence until digested into an owning source-truth file or historical receipt.

### Architecture / Experience / Policy Impact Matrix

Branch Readiness Stage 1 and Branch Planning packets for product, runtime, UI, provider, cache, AI-native, capability-pack, privacy, trust, or source-truth ownership work must include an `Architecture / Experience / Policy Impact Matrix`.

The matrix must classify each touched or plausibly affected owner class as one of:

- `Architecture Layer`
- `Experience Layer`
- `Cross-Family Policy Owner`
- `Runtime Subsystem`
- `Capability-Pack Domain`
- `Family Vision`
- `Package/slice/seam`
- `No Impact`

Allowed impact values are `No Impact`, `Consume Existing`, `Extend Existing`, `Change Existing`, `New Candidate`, and `USER Decision Required`.

The packet must name the existing owner file, current-branch scope, deferred/future scope, rejected owner classes, and proof or validation needed. A `New Candidate` impact is illegal until `Source-Truth Placement Preflight` proves `No Existing Owner Fits` or USER explicitly approves a new owner. Missing or ambiguous matrix rows block on `Architecture Impact Unclassified`, `Experience Layer Impact Unclassified`, `Cross-Family Policy Impact Unclassified`, or `New Owner Candidate Without Placement Preflight`.

`Element Ledger Placement Drift` blocks Stage 2 completion when Codex adds or recommends a new active source-truth artifact without this preflight, when a new artifact duplicates an existing owner, or when the owning record does not point to a large companion ledger file.

### Element Validation Ledger

The `Element Validation Ledger` is the row-level proof ledger for product-significant elements created, touched, affected, deferred, preserved as future, classified as dependency-only, or kept as non-gating supporting evidence.

The ledger is canonical only inside the existing authority owner:

- Promoted workstream: canonical workstream doc.
- Registry-only active branch: external branch state or the standing Governance intake exception while legally active.
- Large active ledger: external branch state, optional companion file with canonical pointer from the owning workstream doc, or transition-approved branch authority receipt.
- Family dossier: aggregate or historical trace only.
- Feature backlog: identity and registry only.
- Roadmap: stage-breakpoint schedule outline and broad milestone checkpoints only.
- Validation helper registry: helper inventory only.
- Element Coverage: non-identity checklist only.

Every active ledger row should identify the element ID, element name, category, parent surface, primary interface, classification, user-facing status, visibility, expected behavior, functional requirement, regression risk, affected source surfaces, source-owner marker or source-owner-not-applicable reason, validation required, Workstream proof, Hardening proof, Live Validation proof, UTS question or waiver, phase owner, current status, open issues, and notes.

Element Validation Ledger status values should use this vocabulary unless an owning record explicitly defines a narrower branch-local set: `Planned`, `Implemented Pending Proof`, `Workstream-Proven`, `Hardening-Proven`, `LV1 Handoff`, `USER Accepted`, `Blocked`, `Deferred`, `Future`, `Dependency-Only Supporting`, and `Non-Gating Supporting`.

Each seam must run an `Element Delta Capture` for product/runtime/UI/source-truth changes. New or changed UI, window behavior, focus/click-through, clipping/z-order, movement/drag/resize, copy/content, telemetry truth, provider states, persistence, validation artifacts, screenshots, UTS questions, lifecycle behavior, and source-truth boundaries must either update an existing ledger row or add a new one.

Marker-only proof cannot satisfy user-facing element acceptance. User-facing and hidden-user-facing ledger rows require screenshot/live proof and Live Validation / UTS coverage unless an explicit waiver is recorded. Deferred, future, dependency-only, and non-gating supporting rows must name their boundary so they neither block nor falsely satisfy the current release.

The active external branch planning owner must carry an `Element-to-Phase Proof Matrix` before Workstream implementation begins or resumes when a branch plans, creates, touches, affects, defers, or preserves user-facing, runtime, UI, provider, validation/helper, source-truth, or workflow elements. The matrix is a USER-reviewable pre-implementation bridge from element coverage to Workstream implementation, Workstream proof, Hardening proof, Live Validation proof or waiver, UTS / USER acceptance, future/deferred boundaries, USER decision state, and source owner / ledger owner. It extends the Element Validation Ledger model and does not create a global ledger or live-state owner. Matrix status markers must use the allowed values in `Docs/branch_plans/README.md`, owner markers must name concrete source-truth owners, external operational-state owners, or repo-relative historical receipt paths, and Element IDs must be unique inside the matrix.

Branch Readiness Stage 2 and Branch Planning must produce or admit the matrix before Workstream implementation. Workstream seam closeout updates matrix rows with implemented, skipped, deferred, or future-gated status. Hardening compares actual implementation against the matrix. Live Validation compares observed behavior, user-facing proof, UTS posture, and waiver posture against the matrix. PR Readiness folds durable matrix outcomes into the branch record, workstream doc, family dossier, or Element Validation Ledger owner.

Branch Planning Review Bundle: Before USER can green-light Workstream implementation for a runtime/user-facing/source-truth branch, Codex must complete BP1, BP2, and BP3 and create or refresh the active worktree's local USER review packet under `C:\Nexus USER\<worktree-label>` with a matching timestamped upload ZIP at `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip`. The packet root contains `START_HERE.md`; `USER Review` contains exactly one primary USER-facing decision file for the current BP gate; `Review Aids` contains generated supporting digests/checklists; and `Source Truth Context` contains copied context files for the Project Vision, Family Vision, Branch Vision, Branch Plan, Element-to-Phase Proof Matrix owner, branch authority record, relevant UFD/change-intent surfaces when applicable, and any other source-truth files needed for USER inspection. The digest must include the local USER hub path, copied file list, validation summary, exact planning or implementation decision requested, and pending USER decisions. Active branch status, current HEAD/origin/main, ahead/behind, validation log detail, current PR state, and ZIP hash belong in helper output, validator output, Codex chat digest, or external operational state rather than as the content focus of USER-facing review files. Missing review packet proof blocks on `Branch Planning Review Packet Missing`.

BP1 USER Branch Vision Review Gate: BP1 must wrap Project Vision Context, Family Vision Context, Feature Vision Context, selected implementation route, Codex understanding, Branch Goal, End-State Vision, what USER will actually see and where, how it will function, user experience flow, Surface Map, product options/design paths, Codex recommendations with USER response space, Nexus-fit rationale, USER design questions, USER response, Codex digest, Accepted Branch Vision, family-vision versus branch-only impact, must-have behavior, must-not-do/regression-risk rules, deferred and future-gated ideas, Vision Question Queue, Design Assumption Ledger, Contract Status, Contract Revision, and acceptance/revision/rejection/waiver decision area into `USER_BRANCH_VISION_REVIEW.md`. BP1 must define the vision for the BR2-selected implementation route; it must not turn planning, setup, or later branch selection into the branch vision. BP1 becomes green only when USER accepts the Branch Vision or explicitly waives BP1.

BP2 USER Branch Plan Review Gate: BP2 must wrap the accepted or waived BP1 result, selected implementation route, implementation package summary, branch scope size test, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, Element-to-Phase Proof Matrix, H1 expectations, LV/UTS expectations, rollback/safety plan, open engineering risks, future-gated boundaries, line-item USER plan review list, plan acceptance checklist, Contract Status, and exact BP3 approval text into `USER_BRANCH_PLAN_REVIEW.md`. `Draft`, `Pending USER Response`, `Pending Codex Digest`, and `Pending USER Confirmation` Contract Status values block implementation until USER confirms or waives the final plan. BP2 asks whether the implementation plan correctly builds the accepted BP1 vision. BP2 cannot green an infrastructure-only or orchestration-only route; when setup groundwork is required before implementation, BP2 must name the exact USER action gate, blocked scope, rollback/safety posture, and route disposition. BP2 routes back to BP1 if the engineering plan exposes a vision gap or changes the accepted Branch Vision. BP2 becomes green only when USER accepts the Branch Plan or explicitly waives BP2.

BP3 Workstream Entry / Orchestration Validation Gate: BP3 loads accepted or waived BP1 and BP2 outputs and proves the branch plan matches the accepted branch vision, the package is the largest safe feature-focused implementation package, SLCs are an engineering route inside one branch rather than automatic separate branches, affected files and validators are ready, Hardening and Live Validation proof paths are planned, rollback is understood, the selected implementation route remains concrete, and future-gated boundaries are preserved. BP3 may return bounded Workstream implementation approval for the admitted same-branch package, naming the entry seam or initial seam sequence, only when BP1 and BP2 are accepted or explicitly waived and BP3 validation is green. BP3 cannot convert continued planning, lane setup, or a future branch selection exercise into Workstream approval. Implementation remains blocked on `BP1 Branch Vision Review Missing`, `BP2 Branch Plan Review Missing`, `BP3 Orchestration Validation Missing`, `Implementation-Bearing Route Missing`, `USER Review Packet Stale`, or `USER Review Packet Not Digested` until these gates are green or waived.

USER Branch Planning review reinforcement: BP1 / `USER_BRANCH_VISION_REVIEW.md` owns product/design direction, end-state vision, user-facing behavior, surfaces, options, Codex recommendations, USER response, Codex digest, accepted Branch Vision, deferred/future-gated ideas, and decision state. BP2 / `USER_BRANCH_PLAN_REVIEW.md` owns the engineering plan derived from accepted or waived BP1: accepted Branch Vision summary, implementation package summary, branch scope size test, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, Element-to-Phase Proof Matrix, H1 expectations, LV/UTS expectations, rollback/safety plan, open engineering risks, future-gated boundaries, line-item USER plan review, plan acceptance checklist, and exact BP3 approval text when ready. BP2 may retain readable context such as surface map, implementation options, and recommended direction, but its primary decision surface is whether the engineering plan correctly builds the accepted BP1 vision. If BP2 changes product direction, user-facing behavior, surfaces, scope, or future-gated boundaries, it must route back to BP1 before implementation approval.

Branch Planning packet acceptance requires more than identity and file count. The active packet must self-validate required BP1/BP2/BP3 file presence, exact USER decision text, and next-legal-phase consistency across `START_HERE.md`, `USER_REVIEW_FOLDER_AND_FILE_DIGEST.md`, `WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`, and `BRANCH_VISION_VALIDATION_CHECKLIST.md`. Active branch status, current source HEAD, current `origin/main`, current PR state, and validation log proof belong in helper output, validator output, external operational state, or Codex chat digest instead of becoming the content focus of USER-facing review files. If packet files disagree about whether the next legal phase is BP1 review, BP2 review, BP3 orchestration validation, Workstream implementation approval, or repair/revalidation, entry blocks on `Branch Planning Packet Decision Path Conflict`. A packet that names Branch Readiness Stage 2 repair/revalidation, or otherwise states that Workstream implementation remains blocked, cannot be used as Workstream implementation approval until the local USER hub packet is reissued or updated and the decision path validates inside the packet itself. Chat-only correction text cannot replace missing packet evidence.

Workstream Entry Whole-Package Analysis Gate: for any runtime-focused branch with multiple admitted slices or seams, Workstream Entry analysis must inspect and report on the entire admitted Workstream package before recommending the entry implementation seam. The packet must include all admitted slices/seams, completion strategy, entry-seam recommendation, seam dependency map, future-gated boundaries, preservation surfaces, validation plan, Hardening H1 expectations, Live Validation LV1 expectations, visual/user-facing proof requirements, UTS handoff criteria, and exact implementation approval text that preserves bounded continuation until Workstream Green, a real blocker, or an explicit USER waiver. A first-seam-only analysis is insufficient and blocks Workstream entry on `Workstream Entry Whole-Package Analysis Missing`. This gate plans Hardening and Live Validation obligations but does not authorize executing those phases; executing Workstream implementation, Hardening, Live Validation, UTS handoff, PR creation, merge, or release work still requires the separately legal phase approval.

Source-code ownership markers are optional backlinks from code to the canonical ledger, not the ledger itself. High-risk elements such as window ownership, drag/move behavior, focus/click-through, clipping/z-order, provider truth, warning behavior, scrollbar/product styling, persistence, proof generation, UTS generation, major UI sections, renderer boundaries, state transitions, and lifecycle/cleanup behavior should carry a source-owner marker or a source-owner-not-applicable reason. Existing source files may adopt this marker format gradually through a later repo-wide marker adoption branch/package.

Dev Toolkit Interface Review Mode is the repo-wide standard dev-only inspection path for USER-facing interface elements once that tooling is admitted. Existing and future USER-facing interface elements, including NCP, Core visualization, Dashboard, Overlay/display when admitted, and other windows/components, should record a Dev Toolkit review disposition in the owning Element Validation Ledger: callable in Dev Toolkit Interface Review Mode, deferred to a named repo-wide adoption branch/package, or not-applicable with reason. The mode is tabled for a planning-heavy Dev Toolkit branch/package and may choose per-interface launchers, a generalized dev-version launch where all eligible surfaces run in review mode, or both. The mode must use dev-only launch surfaces with element badges, hover highlighting, ledger ID/name tooltips, and screenshot-friendly annotations. Production UI must not expose element numbers, and Dev Toolkit review evidence cannot replace Live Validation, screenshot proof, or returned User Test Summary acceptance.

Element ledger blockers include `Element Validation Ledger Missing`, `Element-to-Phase Proof Matrix Missing`, `Element-to-Phase Proof Path Missing`, `Workstream Entry Review Bundle Missing`, `USER Branch Plan Review Missing`, `Workstream Entry Whole-Package Analysis Missing`, `Created Element Untracked`, `Touched Element Proof Missing`, `Affected Element Validation Missing`, `User-Facing Element Acceptance Missing`, `Deferred Element Boundary Missing`, `Element Proof Stale`, `Marker-Only Element Proof`, `Element Ledger Placement Drift`, `Feature Element Source Marker Orphaned`, `High-Risk Element Source Owner Missing`, `Feature Element Marker Proof Insufficient`, `Feature Element Source Marker Stale`, and `Feature Element Source Marker Mismatch`.

### ChatGPT Interface And Codex Execution Authority Rule

ChatGPT, prompt generators, and loader templates are interface layers.
They may package task context, request source-of-truth loading, and describe requested task boundaries for Codex to validate against canon.
They are not execution authority.

ChatGPT-authored prompt additions are analysis and review surfaces. They may add evidence checks, validation reminders, review questions, source-truth checks, and candidate blocker findings for Codex to reconcile against loaded repo governance, but they must not become a second governing authority by removing, replacing, narrowing, reordering, or prohibiting canon-required Codex steps through prompt-layer wording. When ChatGPT finds a flaw, stale assumption, missing step, unsafe scope, governance mismatch, blocker risk, source-truth drift, validation gap, or approval gap, it must frame the concern as an analysis finding, candidate blocker, evidence gap, or USER decision needed; USER approval is required before Codex treats that finding as a source-truth change, approved-plan change, scope widening, waiver, or new FAM/package admission.

Codex execution is governed only by live repo truth plus the owning source-of-truth documents:

- `Docs/Main.md`
- `Docs/development_rules.md`
- `Docs/phase_governance.md`
- `Docs/codex_modes.md`
- `Docs/feature_backlog.md` for tracked identity and `Record State`
- `Docs/workstreams/index.md` and the active workstream doc for promoted branch-local authority
- any directly relevant owning canon document for the task

`Docs/nexus_startup_contract.md` owns loader prompt shape only.
It does not own execution behavior, phase transitions, seam continuation, durability, validation, release rules, or branch authority.
Local ChatGPT custom instructions should stay compact, while the repo loader/source-truth may hold longer ChatGPT-facing continuity rules and review memory.
Do not paste the loader doc into Codex prompts. Codex prompts should load `Docs/Main.md` and owning canon for execution authority, and use the loader only when prompt generation, new-chat bootstrapping, or loader/source-truth drift review is in scope.
Loader/source-truth continuity must preserve the FAM -> Package -> Slice -> Seam model, PR evidence-only rule, legacy global FB historical-only rule, single-slice package blocker, package-completion blocker, Element Coverage as non-identity, Branch Readiness Stage 1 / Stage 2, PR Readiness Stage 1 / Stage 2, next-branch hierarchy review, real-carrier repair routing, no direct-main repair, no standalone cleanup branch by default, post-release canon closure through the next approved Branch Readiness Stage 2 carrier, runtime package carrier when runtime work is next, FAM-006 Monitoring and HUD selected-next truth only after explicit USER approval while branch creation and runtime package admission remain separately blocked, separate release-execution approval, and Windows-first, modular, GPU-aware project direction with optional heavy local AI capability packs and CPU fallback.

Prompt text cannot override source-of-truth, restrict required continuation, define seam behavior, bypass phase rules, create durability exceptions, weaken validation, mutate `main`, mutate files during `Release Readiness`, or change branch authority.
If prompt text conflicts with owning canon, Codex must follow canon, report the conflict, and either continue inside the canon-legal boundary or stop on the canon blocker.

### Single Phase Authority Rule

For active promoted work, the canonical workstream doc must own:

- `Current Phase`
- `Phase Status`
- `Branch Class`
- `Blockers`
- `Entry Basis`
- `Exit Criteria`
- `Rollback Target`
- `Next Legal Phase`

If any of those are missing for active promoted work, the branch is blocked by `Workstream Phase Authority Missing`.

### Branch Authority Record Rule

When an approved branch does not yet map to a promoted backlog workstream, it must use a repo-owned branch authority record under `Docs/branch_records/`.

That branch authority record becomes the single authoritative owner of:

- `Current Phase`
- `Phase Status`
- `Branch Class`
- `Blockers`
- `Entry Basis`
- `Exit Criteria`
- `Rollback Target`
- `Next Legal Phase`

This path is for:

- selected backlog items that remain `Registry-only` during `Branch Readiness`
- explicitly approved non-backlog branch classes such as `release packaging`
- active runtime-focused branches that must carry bounded governance/source-of-truth repairs before PR green
- preserved historical repair records

`docs/governance` branch records may exist as historical records, but new governance-only branches are not used in the normal Nexus flow.
Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
The only standing exception is the `Standing Governance Intake Branch`, `feature/release-readiness-source-truth-intake`, at `C:\Nexus Worktrees\Governance`, and it may accept a `Release Readiness digest`, USER-approved `automation/worktree governance intake`, or USER-approved `phase-gate governance intake` with an `RRI-YYYYMMDD-NNN` cycle ID, operational `One Active Cycle`, the pre-intake `Sync Rule`, originating-lane `Waiting For Governance Intake` / `Waiting For Updated Main` pause semantics, and a post-merge `Return Digest` with `Neutral Main Workspace Rebaseline:` proof. This standing branch is the only branch class exempt from a dedicated post-merge closeout PR solely to clear cycle-ledger wording; after merge, sync, and return digest, the next intake may overwrite the ledger.
If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
Tightly coupled governance and canon repair must ride on the active branch that owns the affected truth.
It must not be used to avoid carrying supporting canon sync on an already-active implementation branch.
If a stale-canon or governance-drift class is discovered, the same branch or next legal repair surface must patch the canon or validator rule that allowed it before the repair is considered complete.
Escaped drift prevention proof is mandatory: every repair for a miss discovered after the phase that should have caught it must include source-truth, governance, validator, helper, or prompt-contract hardening that prevents the same class from passing again, or must record why the gap is not machine-checkable yet and what human review marker replaces it before green.

### Protected Main Law

`main` is protected for Codex work.

Allowed on `main`:

- read-only truth validation
- release review
- merge verification
- post-release verification

Forbidden on `main`:

- editing repository files
- staging files
- committing files
- generating or refreshing source, docs, canon, validator, helper, release-note, or handoff artifacts
- direct canon repair

There is no emergency direct-main repair path for Codex.
Any tracked file mutation while Codex is on `main` is a `Main Write Attempt` blocker.
If drift is discovered before merge, return to the owning branch and repair it before PR green.
If drift is discovered after merge, do not open or resurrect a standalone repair branch for that drift; block the next legitimate runtime-focused backlog branch's `Branch Readiness` and repair there before implementation.

While the branch is active, that branch authority record is the branch-local phase owner.
Before PR merge, merged truth must no longer treat that record as an active branch owner by inertia.
The branch must either:

- move the record into the historical branch-record list with merge-safe phase-status wording, or
- remove the record entirely if no durable historical value remains
- when post-merge truth will remain `No Active Branch`, merge-stable pointer surfaces such as backlog and roadmap must not mirror transient repair-branch ownership; that transient execution truth belongs only in external operational state, Git/GitHub/helper-derived truth, or the standing Governance intake exception until merge

### Repo-Level Admission Gate

Before any next implementation branch may enter `Branch Readiness`, all of the following must be true on updated `main`:

- `main` is aligned with `origin/main`
- merged canon is internally consistent
- no emergency canon repair is outstanding
- no unresolved governance-drift blocker exists
- no unresolved release-debt blocker exists
- no unresolved prior-branch release, branch-authority, or current-state canon cleanup exists
- no PR Readiness scope miss is being deferred into a later phase
- no current branch is being treated as executable if it is stale, merged, or identical to `main`

If any of those fail:

- repo state becomes `No Active Branch`
- next implementation branch execution is blocked
- the next safe move is blocker repair, not a later phase
- if a next active branch has already been created, it must stay in `Branch Readiness` and repair the blocker before any implementation begins

This gate controls next-lane implementation admission.
It does not authorize a governance-only branch.
Release packaging branches still satisfy their own admission rules below.

### Pre-PR Durability Rule

Before `PR Readiness`, when a bounded phase pass or durability seam changes source, docs, canon, validator, helper registry, workstream authority, or branch-truth files and validation is green, Codex must commit and push those changes on the active branch instead of stopping at a copy-ready, staged-only, or uncommitted state.

A prompt-level request to stop before commit/push is not a durability exception. Only a documented `Durability Waiver`, failed validation, a legally file-frozen phase such as `Release Readiness`, or a named Codex self-imposed blocker may stop commit/push. If Codex names a self-imposed blocker, the authority record or response must say what lifts it; once lifted, Codex must automatically commit and push without requiring a second durability prompt.

This rule applies through:

- `Branch Readiness`
- `Workstream`
- `Hardening`
- `Live Validation`

If validation fails, Codex must not commit and push; it must report the blocker and keep the branch in the current phase until the blocker is lifted.
`PR Readiness` remains the later merge-target gate and must still prove clean durable branch truth before PR creation.

### Blocker Catalog

The default named blockers are:

- `Prompt Phase Missing`
- `Prompt Phase Mismatch`
- `Workstream Phase Authority Missing`
- `Branch Base Invalid`
- `Merged Canon Drift`
- `Stale Canon`
- `Phase Exit Unmet`
- `Next Workstream Undefined`
- `Successor Lock Missing`
- `Post-Merge State Unresolved`
- `Dirty Branch`
- `Docs Sync Incomplete`
- `Release Debt`
- `Release Target Undefined`
- `Release Readiness File Mutation Attempt`
- `User-Facing Shortcut Validation Pending`
- `User Test Summary Results Pending`
- `PR Creation Pending`
- `PR Validation Pending`
- `PR State Unknown`
- `PR Readiness Execution User Approval Missing`
- `PR Merge Status Unproven`
- `Merge-Target Authority Projection Unproven`
- `PR Merge Verification Pending`
- `PR Watcher Provisioning Unproven`
- `PR Watcher Routing Unverified`
- `PR Readiness Scope Missed`
- `Release Window Audit Incomplete`
- `Release Readiness Scope Drift`
- `Prior Branch Canon Unresolved`
- `Between-Branch Canon Repair Attempt`
- `Main Write Attempt`
- `Next Branch Created Too Early`
- `Governance Drift`
- `Current-State Claim Drift`
- `Phase Waiver Missing`
- `Planning-Loop Guardrail`
- `Backlog Completion Unproven`
- `Backlog Addition User Approval Missing`
- `Backlog Exhaustion User Decision Pending`
- `Single-Slice Package User Approval Missing`
- `Package Completion Unproven`
- `Exact USER Desktop Launcher Proof Missing`
- `Launcher Parity Proof Missing`
- `Photo Or Video Proof Missing`
- `Unphotographable Proof Not Elevated To USER`
- `Direct Runtime Proof Misclassified`
- `Troubleshooting Consent Missing`
- `Live Validation Evidence Packet Incomplete`
- `User-Visible Internal Path Leakage`

Blockers stop progression immediately and must be reported before any later-phase recommendation.

### Planning-Loop Guardrail

Purpose:

- prevent planning-only branches from being mistaken for implementation progress
- prevent Workstream from becoming a planning/canon sink on implementation branches
- prevent repeated docs-only release trains from becoming the default delivery path
- keep repair-only branches as blocker-clearing surfaces rather than normal product-progress lanes

Core rule:

- Branch Readiness owns planning, framing, affected-surface mapping, implementation delta classification, admitted-slice definition, and whole-backlog closure strategy before Workstream begins.
- Branch Readiness must evaluate the whole backlog item, define the first admitted slice, record the same-branch continuation posture until `Completion Status` becomes green, and record any known future-dependent blockers before Workstream begins.
- Workstream must execute admitted implementation slices one slice at a time, keep re-evaluating the backlog item after each seam and slice, and keep later slices on the same branch by default when scope, phase, risk, and validation authority remain green unless the USER explicitly approves a docs-only bypass or backlog split.
- Docs-only Workstreams require explicit USER approval.
- Planning-loop bypass requires `Planning-Loop Bypass User Approval: APPROVED` and `Planning-Loop Bypass Reason:`.
- Release-bearing implementation work with no runtime/user-facing, backend/runtime, or developer-tooling delta is blocked unless the USER explicitly approves that release window.
- `Workstream` may not advance to `Hardening` while remaining implementable work is still available on the current backlog item.
- branch existence, branch rename, backlog promotion, repair-only traceability, or release-bearing posture do not count as Workstream progress by themselves
- repair-only branches are blocker-clearing surfaces, not normal implementation progress

Runtime Branch Engineering Contract:

- runtime-focused implementation branches must carry `## Runtime Branch Engineering Contract` beside the Product Definition Plan before Workstream begins or any later phase resumes
- the contract must translate USER-reviewed product intent into engineering intent with `USER Engineering Planning Review:`, `Runtime Implementation Approval:`, `Current Runtime Baseline:`, `Planned Runtime Delta:`, `User-Facing Runtime Delta:`, `State / Config / Schema Delta:`, `Validator / Helper Delta:`, `Expected Changed Files / Surfaces:`, `Approval-Boundary Audit:`, `Future-Gated Items:`, `Workstream Seam Map:`, `Proof Expectations:`, `Risk Forecast:`, `Recommendations And Alternatives:`, `Plan Version / Revision Status:`, and `Plan-To-Implementation Traceability:`
- Branch Readiness Stage 1 proposes the contract and stops for USER planning review; Branch Readiness Stage 2 may admit or revise it, but `Runtime Implementation Approval:` remains pending until Workstream is separately approved
- Workstream seam start/closeout, Workstream Green, Hardening, Live Validation, PR Readiness, and Release Readiness must compare actual deltas, visible behavior, validator/helper proof, skipped items, and public release scope against the admitted contract
- if implementation discovers the contract is too narrow, stale, or wrong, Codex must stop with a plan revision packet that names the current approved plan, discovered repo truth, proposed revision, affected seams, approval-boundary impact, and exact USER decision needed

Branch Runtime Engineering Plan:

- new or re-entering runtime-focused branches must create or admit the detailed active-branch execution plan under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` during Branch Readiness Stage 2 when repo truth supports runtime work
- the branch authority record must remain the control surface and must include `Branch Runtime Engineering Plan:`, `Branch Runtime Engineering Plan Path:`, and `Engineering Plan Status:` when the plan is required, present, accepted, revised, folded, or historical
- backlog and roadmap remain compact pointer/status surfaces; detailed runtime baseline, planned delta, per-seam checklist, validation checklist, user-facing proof checklist, future-gated ledger, approval-boundary audit, and plan-to-implementation traceability belong in the Branch Runtime Engineering Plan or folded historical record
- Branch Readiness Stage 2 and Workstream Entry must admit a USER-reviewable `Element-to-Phase Proof Matrix` in the active external branch planning owner when the branch plans, creates, touches, affects, defers, or preserves product/runtime/UI/source-truth/helper/workflow elements; each current planned/created/touched/affected element must name Workstream implementation, Workstream proof, Hardening proof, Live Validation proof or waiver, UTS / USER acceptance, USER decision state, and source owner / ledger owner before Workstream begins or resumes
- BP1/BP2/BP3 Branch Planning must include a full non-compacted Branch Planning / Workstream Entry Review Digest and the active worktree's local USER hub packet under `C:\Nexus USER\<worktree-label>`, with a matching timestamped upload ZIP at `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip`, root `START_HERE.md`, exactly one current-gate primary decision file under `USER Review`, generated supporting digests/checklists under `Review Aids`, and copied project vision, family vision, branch vision, branch plan, branch authority, matrix, UFD/change-intent, and source-truth context under `Source Truth Context` before USER can green-light implementation.
- BP1 must include the named `USER Branch Vision Review Gate`; BP2 must include the named `USER Branch Plan Review Gate`; BP3 must include `Workstream Entry / Orchestration Validation` for runtime/user-facing/source-truth work. The review packet summarizes the accepted branch vision, planned user-facing outcome, implementation plan, Element-to-Phase Proof Matrix summary, Hardening plan, Live Validation / UTS plan, open USER questions, Codex recommendations, implementation options, alternatives/tradeoffs, accepted/deferred/rejected scope, exact USER decision needed, `USER Review Response:`, `Codex Response Digest:`, and `USER Review Packet Finding:`. The finding must prove the local USER hub packet was loaded and digested or name the exact waiver/blocker. Workstream implementation stays blocked on `BP1 Branch Vision Review Missing`, `BP2 Branch Plan Review Missing`, `BP3 Orchestration Validation Missing`, `USER Review Packet Stale`, or `USER Review Packet Not Digested` until BP1/BP2 are accepted or waived and BP3 is green.
- Workstream Entry reads the plan and returns whole-package analysis before entry-seam implementation, each seam updates traceability, Hardening compares actual implementation against it, Live Validation records proof or waiver posture, PR Readiness produces the `PR Fold-Down Packet:`, and Release Readiness translates the plan into public scope without internal governance jargon
- a missing or shallow Branch Runtime Engineering Plan keeps runtime implementation blocked on Branch Readiness planning until USER accepts, revises, or explicitly waives the plan boundary

USER Feedback Disposition:

- meaningful USER feedback during Branch Readiness, Workstream, Hardening, Live Validation, or PR Readiness must be classified through `USER Feedback Disposition` when it affects branch scope, accepted vision, user-facing behavior, runtime behavior, validation proof, future work, reusable product standards, approval boundaries, or a USER decision
- the active external branch planning owner owns full UFD detail while the branch is active; branch records, repo branch-plan receipts, backlog, roadmap, Nexus Vision, family vision, workstream docs, and family dossiers may carry compact pointers or folded outcomes only when they are the correct owner for the final disposition
- UFD ledger markers include `USER Feedback Disposition Required:`, `UFD Ledger Status:`, `UFD Ledger Owner:`, `Open UFD Count:`, `Blocking UFD Count:`, and `Fold-Down Status:`
- each meaningful feedback item uses a repeatable `### UFD Item: UFD-<scope>-YYYYMMDD-NNN` block with `Feedback ID:`, `Feedback Summary:`, `Feedback Source:`, `Feedback Phase:`, `Disposition Type:`, `USER Decision State:`, `Owner Class:`, `Canonical Owner File:`, `Workstream Severity:`, `Status:`, `Fold-Down Target:`, and `Pointer Locations:`
- Codex may recommend UFD disposition, owner, severity, and no-action posture, but USER decision controls accepted branch scope; Codex and ChatGPT recommendations remain proposed until USER accepts, revises, rejects, defers, waives, or supersedes them
- pointer locations may carry only UFD ID, short title, canonical owner, compact status, and fold-down status; full feedback text, full decision history, and live implementation state stay with the active external branch planning owner until PR Readiness fold-down
- `No Durable Owner Needed` is valid only when the item is closed as minor/no-action, duplicate, superseded, or non-actionable, with `No-Action Reason:` recorded in the active external branch planning owner or return digest
- UFD IDs use `UFD-<scope>-YYYYMMDD-NNN`; do not use `FBK-*` because it collides visually with historical `FB-###` workstream records

Vision Contract / Vision-to-Plan loop:

- runtime/user-facing branches must not silently convert Codex or ChatGPT design recommendations into implementation truth
- Nexus Vision owns project-wide product principles; optional family vision or family dossier sections own broad feature-family direction only when the family is large enough; USER-approved Family Feature Vision records under `Docs/family_feature_visions/` own detailed feature-category direction and Deferred Feature Carryforward inside one FAM; the active external branch planning owner owns the Branch Vision Contract Snapshot for branch-specific accepted vision
- `Vision Contract Required:` is `Yes` for user-facing UI/UX behavior changes, runtime behavior changes, workflow hierarchy changes, visual standard changes, setup/activation behavior changes, provider/model/memory/voice/Core behavior, returned UTS that changes target behavior, broad family planning, ambiguous acceptance criteria, conflicting prior source truth, or any Codex recommendation that would otherwise become product/design truth
- `Vision Contract Required:` may be `No` only for mechanical docs-only repair, validator-only repair with no product/runtime/user-facing impact, release-body formatting repair, source-truth typo/format repair, or branch metadata repair, and the reason must be recorded
- valid design assumption states are `Proposed by Codex`, `Recommended by ChatGPT`, `Accepted by USER`, `Revised by USER`, `Rejected by USER`, `Deferred by USER`, `Deferred With Waiver`, `Superseded`, and `Needs USER Decision`; only `Accepted by USER`, `Revised by USER`, or `Deferred With Waiver` are implementation-safe for product/runtime/user-facing behavior
- before Workstream implementation, a required Branch Vision Contract Snapshot must record `Branch Vision Snapshot Status: Accepted`, `Open Vision Questions: None` or `Deferred With Waiver`, `USER Vision Green: Yes`, accepted implementation scope, accepted seam map, accepted stop conditions, a design assumption ledger, a vision question queue, and vision-to-implementation traceability
- after USER Vision Green, Codex should preserve the accepted plan during implementation; new Level 1 non-blocking questions are queued, Level 2 seam-blocking questions pause only the affected seam and require a Vision Question Digest, and Level 3 workstream-breaking questions require a Branch Plan Revision Packet before affected scope continues
- accepted assumptions expire or require review when branch scope changes, returned UTS changes the accepted target, family vision changes, source truth contradicts prior assumptions, new user-facing behavior appears, or implementation would apply an old decision to a new family/surface
- Hardening compares implementation against accepted vision and accepted branch plan; Live Validation compares observed user-facing behavior against accepted vision and accepted branch plan; PR Readiness folds reusable vision updates into Nexus Vision, family vision/family dossier, workstream docs, structured branch receipts, or validated historical receipts without creating permanent branch-specific vision-file sprawl
- Vision Question Digest must include question, why it matters, affected branch/seam, current accepted vision, Codex recommendation, alternatives, risk of each option, whether work can continue without the answer, recommended USER decision, and exact USER decision needed
- Branch Plan Revision Packet must include current accepted plan, discovered issue, why current plan is insufficient, proposed revision, affected seams, files/surfaces affected, validation impact, current Workstream versus future branch routing, Codex recommendation, and exact USER decision needed

Vision Update Decision Matrix:

| Input or update type | Active owner while unresolved or branch-local | Durable owner when USER accepted | Update trigger |
| --- | --- | --- | --- |
| Branch-specific design, behavior, seam, or implementation detail | Active external branch plan Branch Vision Contract Snapshot, UFD item, question queue, or Branch Plan Revision Packet | Branch receipt, workstream doc, family dossier, or validated historical receipt only if PR Readiness fold-down finds durable value | Record during Branch Readiness or Workstream; fold down during PR Readiness |
| Reusable family-level product direction or design standard | Active external branch plan first, with family vision as alignment reference | `Docs/family_visions/FAM-XXX_*.md` or family dossier section | USER accepts the standard, it applies beyond one branch, and it avoids branch-local implementation detail |
| Detailed feature-category direction inside one FAM | Active external branch plan first, with Family Vision and existing Family Feature Vision as alignment references | `Docs/family_feature_visions/FAM-XXX_<feature_slug>.md` after USER-approved content-file creation | USER accepts the feature-category direction, it applies beyond one branch, and it is more detailed than Family Vision but not branch-local implementation detail |
| Durable deferred feature carryforward inside one FAM | Active external branch plan UFD/future-package queue while unresolved or branch-local | `Docs/family_feature_visions/FAM-XXX_<feature_slug>.md` Deferred Feature Carryforward section after USER-approved disposition | USER accepts or defers the item for future feature grouping, names the dependency trigger, and assigns durable disposition without live branch state |
| Project-wide or cross-family product principle, long-term standard, AI/privacy/execution direction, or foundational behavior | Active external branch plan or governance intake until USER acceptance and scope are clear | `Docs/nexus_vision.md` | USER accepts the standard and it affects multiple families or Nexus-wide principles |
| Proposed, uncertain, conflicting, or ChatGPT/Codex-recommended idea | Active external branch plan question queue, UFD item, assumption ledger, or Vision Question Digest | No durable owner until USER accepts, revises, defers with waiver, rejects, or supersedes it | USER decision or waiver is required before implementation-safe product/runtime/user-facing scope |
| Future feature/package idea outside current branch scope | Active external branch planning owner UFD/future-package queue while active | Backlog compact pointer, family dossier, or future branch plan only after accepted/deferred disposition | USER accepts future-work posture or PR Readiness assigns a named future owner |
| Mechanical docs-only, validator-only, release-body-format, typo/format, or branch-metadata repair with no product/runtime/user-facing impact | Current repair branch plan or return digest with `Vision Contract Required: No` reason | Relevant governance receipt only if the repair creates durable interpretation | Record the not-required reason; do not promote to Nexus or family vision |

Branch plan first. Family Feature Vision only when the update is durable feature-category direction or deferred carryforward inside one FAM and USER accepts or defers it to that owner. Family vision only when reusable and USER accepted at broad family level. Nexus Vision only when project-wide or cross-family. Proposed or unresolved ideas must not be promoted to durable vision owners by Codex inference.

Required active authority markers for implementation branches in `Branch Readiness`, `Workstream`, `Hardening`, `Live Validation`, `PR Readiness`, or merged-unreleased release-debt truth:

- `## Admitted Implementation Slice`
- `## Planning-Loop Guardrail`
- `Implementation Delta Class:`
- `Docs-Only Workstream:`
- `Planning-Loop Bypass User Approval:`
- `Planning-Loop Bypass Reason:`
- in `Branch Readiness`, also require:
  - `## Backlog Completion Strategy`
  - `Branch Completion Goal:`
  - `Known Future-Dependent Blockers:`
  - `Branch Closure Rule:`
- in `Workstream`, `Hardening`, `Live Validation`, and `PR Readiness`, also require:
  - `## Backlog Completion Status`
  - `Backlog Completion State:`
  - `Remaining Implementable Work:`
  - `Future-Dependent Blockers:`
- in `Workstream`, also require:
  - `Completion Status:`

Allowed `Implementation Delta Class:` values:

- `runtime/user-facing`
- `backend/runtime`
- `developer-tooling`
- `docs-only`
- or a comma-separated combination of the non-docs-only values above

Allowed `Backlog Completion State:` values:

- `In Progress`
- `Implemented Complete`
- `Implemented Complete Except Future Dependency`

Interpretation:

- `docs-only` means the lane does not currently deliver runtime/user-facing, backend/runtime, or developer-tooling implementation delta
- `docs-only` must not be mixed with another implementation delta class
- `Docs-Only Workstream: Yes` is legal only when explicit USER approval is recorded through the planning-loop bypass markers
- if those markers are missing, contradictory, or unapproved for a docs-only implementation lane, the branch is blocked by `Planning-Loop Guardrail`

### Blocker Rule

Phase-sensitive work is blocked until the following are explicit and mutually consistent:

- exact current phase
- active workstream or equivalent authority record
- branch class when branch-sensitive execution is in scope
- validation contract when validation is in scope
- timeout contract when interactive validation is in scope
- current active seam when the branch is in governed recovery
- current blocker set

If live behavior and the documented timeout contract drift, execution is blocked until they are reconciled.

### Branch Class And Phase Waiver Rule

Every active branch must declare a `Branch Class`:

- `implementation`
- `docs/governance`
- `emergency canon repair`
- `release packaging`

The same six normal phases apply to all branch classes.
`docs/governance` remains a recognized historical branch class, but it is not an approved new-branch lane in the normal Nexus flow.
Phases may be waived only when:

- the waiver is explicit in the active workstream or branch authority record
- the reason is recorded
- the waiver does not weaken merge-target canon completeness, successor lock, or release-debt protections

Silent phase skipping is prohibited.

### Branch-Class Admission Rule

Branch admission is class-sensitive.

### Family-Scoped Branch Readiness Candidate Rule

When Branch Readiness is scoped to a specific feature family or assigned lane, candidate selection must stay inside that family or lane unless USER explicitly approves cross-family routing. Codex may inspect other families only for same-file overlap, dependency, conflict, pending-decision, or sequencing context. If no legal in-family carrier is selected or admissible, Codex must return `STOP / USER DECISION REQUIRED` with the exact in-family decision needed instead of selecting another family's branch.

`implementation`

- the full repo-level admission gate must pass before the branch may enter `Branch Readiness`
- the active promoted workstream doc is the default authority record
- docs-only governance or canon refinements may ride on the active implementation branch when they are directly required to keep that branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct
- those refinements do not change the branch class; they must stay inside the current phase, remain explicit in scope, preserve validation and stop conditions, and avoid unrelated governance churn

`docs/governance`

- is preserved only for historical records and explicit legacy interpretation
- must not be opened as a new governance-only branch in the normal Nexus flow
- must not be used for between-branch canon repair
- must not be used to carry PR Readiness work after the branch that owned that work has merged
- if governance or canon work is directly required to keep the current branch truthful, executable, phase-correct, readiness-correct, validation-correct, closeout-correct, or release-correct, that work must ride on the active current branch inside its current phase and branch class
- if a PR Readiness miss is discovered after merge, the next legitimate runtime-focused backlog branch's `Branch Readiness` must carry the repair before implementation begins
- if no active branch exists and no next workstream can be selected, the repo remains `No Active Branch`; Codex must not repair directly on `main`

`release packaging`

- may begin from updated `main` when merged-unreleased implementation, release notes, tagging, or another release-facing packaging task is explicitly opened
- the branch must not widen into implementation work

`emergency canon repair`

- is preserved only as historical vocabulary
- is not a normal branch lane in the current Nexus flow
- does not authorize direct-main repair by Codex
- does not authorize new temporary blocker-clearing branch surfaces for future Nexus work
- it does not promote the associated workstream and does not satisfy or consume selected-next implementation-branch creation
- if escaped canon drift exists, the default repair is the next legitimate runtime-focused backlog branch's `Branch Readiness`

### Merge-Target Canon Completeness Gate

Rule:

- a branch is not `PR Readiness`-complete if merging it would leave `main` canon-stale

This gate is mandatory when a branch would:

- close a workstream
- become the latest released or merged-unreleased implementation milestone
- change the current rebaseline or closeout baseline
- change the current closeout-index pointer
- change backlog status, roadmap stage-breakpoint/checkpoint posture, or workstream-index release posture
- change `Docs/Main.md` routing for the current baseline

When this gate applies, the branch must already contain the required release-facing canon updates before PR creation is allowed:

- canonical workstream record closure or equivalent release-state update
- `Docs/feature_backlog.md`
- `Docs/prebeta_roadmap.md`
- `Docs/workstreams/index.md`
- `Docs/closeout_index.md`
- the new or updated closeout or rebaseline file when current baseline routing changed
- `Docs/Main.md` routing updates when the current baseline pointer changed
- `Docs/branch_records/index.md` plus any relevant branch authority record when the branch still relies on branch-record authority and would otherwise remain incorrectly active after merge

If any required merge-target canon update is missing, the branch remains blocked in `PR Readiness`.

### Exceptional Merged-Unreleased Release-Debt Owner Contract

Release debt is not a normal acceptable merge state. When an implementation branch would unavoidably merge unreleased product behavior beyond the latest public prerelease, PR Readiness Stage 1 must first record explicit USER approval for that exception, the named owner, the release target/floor semantics, Release Window Audit posture, and the real carrier plan. Selected-next truth is not part of the default release-debt exception; PR Readiness records it only when USER explicitly approves PR-time successor selection or already-encoded selected-next truth would merge as durable source truth. Only then may PR Readiness leave exact post-merge release-debt truth in canon before PR green.

After the External Operational State Store contract is implemented, release debt means durable public release truth is missing or wrong. Wrong tag/body/release notes, invalid or missing artifacts, missing durable public milestone summaries, and released capabilities absent from durable product history remain release debt. Stale repo-file active branch records, repo-file active branch plans, worktree slots, selected-next operational posture, PR watcher state, release-window operational state, and post-release closure status become `Repo Live-State Leakage` or `External Operational State Conflict`, not release debt. This reclassification does not take effect as a migration until the USER approves external-state implementation and validator transition.

Required machine-checkable fields:

- `Merged-Unreleased Release-Debt Owner:`
- `Repo State: No Active Branch`
- `Release Target:`
- `Release Floor:`
- `Version Rationale:`
- `Release Scope:`
- `Release Artifacts:`
- `Post-Release Truth:`

Conditional machine-checkable fields, required only when USER explicitly approved PR-time successor selection or already-encoded selected-next truth would merge as durable source truth:

- `Selected Next Workstream:`
- `Next-Branch Creation Gate:`

Required owner docs:

- `Docs/feature_backlog.md` names the workstream as merged-unreleased release debt, not active execution truth
- `Docs/prebeta_roadmap.md` names the current release-debt owner, release target, release scope, and release artifacts as durable pointers; it names selected-next and branch-creation gate truth only when USER explicitly approved PR-time successor selection or selected-next truth already exists
- `Docs/workstreams/index.md` moves the workstream from `Active` to `Merged / Release Debt Owners`
- the canonical workstream doc records the same merged-unreleased release-debt owner contract

Release Readiness consumes this inherited release truth only after PR Readiness Stage 1 made the exception explicit before PR creation.
Release Readiness may validate target, scope, artifacts, and post-release truth, but it must not create or repair those fields in repository files.

Release target correctness is semantic, not marker-only.
PR Readiness must derive the target from the latest public prerelease and the declared `Release Floor:` before green:

- `patch prerelease` increments only the patch number, for example `v1.4.0-prebeta` -> `v1.4.1-prebeta`
- `minor prerelease` increments the minor number and resets patch to zero, for example `v1.4.0-prebeta` -> `v1.5.0-prebeta`

Release floor ownership:

- `patch prerelease` is the default floor for bug fixes, UX polish, governance fixes, documentation/canon repair, architecture-only planning, admission contracts, validation-only work, and non-user-facing milestones that do not add executable product behavior.
- `minor prerelease` is allowed only when the release delivers a new executable, runtime, operator-facing, user-facing, or materially expanded product capability lane.
- Opening a future planning lane, writing architecture, defining vocabulary, or creating an admission contract is not enough by itself to justify `minor prerelease`.
- If a public tag has already been published with a larger bump than the corrected law would choose, do not rewrite the public tag; record the published tag as latest release truth, classify the mismatch as version-advancement drift, and harden future `Release Floor:` validation.

If the declared target, artifacts, or post-release truth do not match the semantic release floor, keep `Release Target Undefined` active and repair the mismatch in PR Readiness before Release Readiness.

Post-release closure is mandatory after release execution:

- once a public prerelease tag exists for a merged-unreleased release-debt owner, durable canon must move that workstream to Released / Closed
- `Docs/prebeta_roadmap.md` must advance latest public prerelease truth to the published tag
- `Docs/feature_backlog.md` must mark the owner `Record State: Closed` and `Status: Released`
- `Docs/workstreams/index.md` must remove the owner from `Merged / Release Debt Owners` and list it under `Closed`
- the canonical workstream doc must record `Latest Public Prerelease:`, `Release Title:`, released/closed state, and cleared release debt
- release execution and post-release canon closure are separate; post-release canon drift must land in remote source truth through the approved Branch Readiness carrier before implementation begins
- a local-only post-release closure commit is a blocker, not completed source truth
- protected-main branch rejection must route to the next approved Branch Readiness Stage 2 canon/governance repair carrier instead of direct-main mutation, standalone cleanup, or a default release-support branch
- post-release validation must compare published GitHub release/tag truth and release-body format against remote repo source truth
- runtime implementation remains blocked until release publication exists, post-release canon drift is explicitly recorded or repaired through the approved Branch Readiness carrier, and owning validation reports green
- when release-dependent source truth cannot exist until after publication, backlog and roadmap may record bounded transitional drift using `Post-Release Canon Closure Drift: Recorded`, `Published Release Pending Canon Closure: <tag>`, `Closure Repair Surface: Next Branch Readiness Stage 2`, `Closure Drift Scope: release-dependent fields only`, and `Implementation Entry: Blocked until closure repair validates green`
- if this closure is missed after merge or release, the next legitimate runtime-focused backlog branch's `Branch Readiness` is blocked until the closure is repaired and validator coverage is updated so the miss cannot recur; this is containment for an exception, not a normal cleanup/canon-sync branch path

### Successor Lane Lock Gate

Rule:

- Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection.
- Branch selection is rooted in project vision, family vision, branch vision, current completed work, and the next implementation need. It must not be selected by PR Readiness inertia, release-debt avoidance, old selected-next ledgers, or stale backlog/roadmap posture.
- PR Readiness does not require selected-next truth or a waiver by default. Its default job is to prove the current branch is merge-ready, merge-stable, and free of stale active operational state.
- PR Readiness validates selected-next truth only when USER explicitly approves PR-time successor selection or repo/external state already encodes a USER-approved successor selection.
- When no USER-approved selected-next truth exists, the next implementation carrier is selected later through Branch Readiness Stage 1 after the current PR merges and updated `main` / external operational state are revalidated.

Exception:

- If USER approval for a new or successor backlog identity is absent, Codex must not select, split, promote, or create a successor backlog identity by inertia.
- If selected-next truth already exists, PR Readiness must verify it is USER-approved, vision-aligned, merge-stable, not stale, and not a live operational ledger in repo docs.
- If selected-next truth is absent, that absence is not a PR Readiness blocker. The future branch decision moves to Branch Readiness Stage 1, where Codex must evaluate vision alignment, current work, dependency boundaries, family ownership, implementation need, package/slice shape, and USER questions before admitting any branch.

### Backlog Identity Admission Gate

Backlog IDs are major user-facing feature-family or major release/support lanes.
The live backlog-family namespace is broad `FAM-###`, starting at `FAM-001`; the current admitted registry ends at `FAM-008`, and the old `FB-###` namespace is historical-only and must not be reused for parseable backlog entries.

Canonical identity model:

- `FAM` is a broad long-lived product family.
- `Package` is a bulk branch/release package under exactly one FAM.
- `Slice` is a traceable deliverable area inside exactly one package.
- `Seam` is an execution or validation checkpoint.
- `PR` is merge/review evidence only.
- legacy global `FB` is historical trace only.

Branch scope standard:

- branches should carry one family package with multiple admitted slices by default
- packages must record `Package Completion State:`
- package slices must trace to exactly one FAM and exactly one package
- Workstream must continue through every admitted package slice before Hardening unless package state is truthfully `Complete`, `Released Baseline / Open`, `Blocked`, or `Deferred`
- a package with exactly one admitted slice is blocked by `Single-Slice Package User Approval Missing` unless explicit USER approval records `Single-Slice Package User Approval: Granted`
- admitted-slice counting is explicit: only `Admission State: Admitted` rows count toward the multi-slice package rule
- `Historical Evidence`, `Merged Evidence`, `Future Placeholder`, `Deferred Placeholder`, future package required rows, and deferred ideas preserve trace but do not count as admitted slices
- every admitted slice must have concrete scope, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder rows cannot satisfy the multi-slice rule
- `Package Completion State: Complete` is blocked while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while another admitted package slice remains incomplete

They are not default identities for:

- small single-seam runtime proofs
- governance repairs
- validation follow-through
- hotfixes
- blocker-clearing repair traces
- branch-readiness or PR-readiness closeout details

Codex must not create a new backlog item, split an existing backlog identity, admit a new package, create a new family branch, promote a new selected-next backlog identity, waive a single-slice package, or encode successor selection without explicit USER approval in the prompt or source-of-truth.

When Codex believes a new backlog item, package admission, branch creation, backlog split, promotion, selected-next successor, or single-slice package waiver is needed but USER approval is absent, Codex must stop on `Backlog Addition User Approval Missing`.
The blocker output must include all FAM entries that are still not closed and all package/slice rows that are not complete, with:

- ID
- title
- Status
- Record State
- Priority
- Package ID
- Package Completion State
- Slice ID
- Slice Status
- Selection / Unblock, deferred-context, branch, and minimal-scope fields when present

If no backlog entries remain open, Codex must stop on `Backlog Exhaustion User Decision Pending` and wait for USER direction.

Small or single-seam runtime follow-through inside an existing family must be recorded in a package/slice trace, canonical workstream, lifetime family dossier, branch authority record, or historical PR trace as family evidence or aggregation material.
It must not mint a standalone backlog identity, single-slice package, successor lane, branch family, or release-version driver unless the USER explicitly approves a larger feature-family release, release aggregation, backlog split, or single-slice package waiver.

Historical pass aliases, support/governance lanes, and old registry-only implemented IDs are trace rows, not selectable backlog items. Re-promoting one into a parseable backlog identity requires explicit USER approval and a recorded reason that family/workstream/branch traceability is insufficient.
Any approved new backlog identity must use the fresh broad FAM namespace, not `FB-###`.

When USER-approved successor selection already exists and PR Readiness is asked to preserve or validate that existing selected-next truth, this gate requires all of the following before PR creation is allowed:

- the next workstream identity is selected from current canon using open backlog `Priority` plus deferred-context readiness, not `Target Version`
- that workstream exists in `Docs/feature_backlog.md`
- that workstream is recorded in `Docs/prebeta_roadmap.md`
- that workstream has a canon-valid `Record State`
- that workstream is a real runtime `Feature Family` candidate
- that workstream has `Priority` defined
- if that workstream is deferred, the backlog entry records `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:`
- that workstream has minimal scope defined before PR green
- no branch has been created for that next workstream yet
- successor branch creation is deferred to `Branch Readiness` after the current branch merges and updated `main` is revalidated

`Target Version` is not a next-workstream selection field. Do not use it to rank, select, defer, or skip open backlog candidates. Release targets are assigned by release-floor and release-readiness governance when a release-bearing branch requires them. Closed, released, implemented, or release-debt entries may preserve `Target Version` as historical release evidence.

Machine-checkable canon markers:

- the selected backlog entry must include `Next Workstream: Selected`
- the selected backlog entry must include `Minimal Scope:`
- when USER-approved selected-next truth exists, the roadmap must include `## Selected Next Workstream`
- when USER-approved selected-next truth exists, the roadmap selected-next section must include the same workstream id, its `Record State`, `Minimal Scope:`, and truthful branch status such as `Branch: Not created` before branch creation or the active Branch Readiness branch name after creation

When post-merge `No Active Branch` handling applies, the branch must instead:

- make the post-merge `No Active Branch` state explicit in current-state canon
- name the blocking admission item explicitly
- keep selected-next truth absent by default unless USER explicitly approved PR-time successor selection or selected-next truth already exists
- avoid creating or executing the next implementation branch by inertia

Temporary `emergency canon repair` branches that are explicitly recorded as repair-only must not be treated as the selected-next implementation branch for this gate. Validator and canon checks should distinguish those repair branches from real successor implementation-branch creation.

If selected-next truth is present but not recorded in backlog and roadmap, lacks valid record state, or lacks minimal scope, the branch is blocked by `Next Workstream Undefined`.
If USER approval for new or successor backlog selection is absent, PR Readiness must not create selected-next truth. The next branch decision waits for Branch Readiness Stage 1.
Explicit PR-time successor-selection approval must be machine-recorded as `Successor Selection User Approval: Granted`; otherwise PR Readiness treats successor recommendations as non-binding planning context only.
When post-merge `No Active Branch` truth is merge-stable and no selected-next entry exists, PR Readiness may proceed without `Next Workstream User Waiver:` because the next runtime implementation pipeline belongs to the next Branch Readiness Stage 1 pass.
If a selected deferred workstream lacks deferred-context fields, the branch is blocked by `Deferred Selection Context Missing`.
If a successor branch is created before `Branch Readiness`, the branch is blocked by `Successor Lock Missing`.

### PR Readiness Hard Blocker Gates

PR Readiness must not report green while any pre-merge process blocker remains unresolved.

Hard blockers:

- canonical shorthand: `stale-canon`, `post-merge`, `dirty`, `docs-sync`, `next-workstream-if-selected`, `Backlog Addition User Approval Missing`, `Backlog Exhaustion User Decision Pending`, `Single-Slice Package User Approval Missing`, `Package Completion Unproven`, `PR Readiness Execution User Approval Missing`, `deferred-context`, `desktop-shortcut`, `uts-results`
- `Stale Canon`:
  current-state canon and merge-target canon must already reflect the branch's true state and the state that will be true after merge
- `Post-Merge State Unresolved`:
  post-merge truth must already be merge-stable for the current branch and must not leave stale active branch authority, live PR state, release-window ownership, or repo-ledger operational state. `No Active Branch` is allowed when no USER-approved successor selection exists; the next runtime implementation pipeline is then selected during Branch Readiness Stage 1.
- `Next Workstream Undefined`:
  If selected-next truth is already encoded or USER explicitly approves PR-time successor selection, PR Readiness cannot be green until that selected workstream exists in canon, is recorded in backlog and roadmap, has a valid record state, has minimal scope defined, and has no branch created yet. If selected-next truth is absent, this blocker does not apply.
- `Next Runtime Candidate Selection Pending`:
  Retired as a default PR Readiness blocker after the external-state/index-only reform. Use this only for inconsistent already-encoded selected-next truth or explicit USER-approved PR-time successor selection that cannot be made coherent. Normal next runtime candidate selection belongs to Branch Readiness Stage 1.
- `Backlog Addition User Approval Missing`:
  PR Readiness and Branch Readiness cannot add, split, promote, package-admit, branch-create, waive a single-slice package, or select a backlog identity without explicit USER approval. When this blocker is active, Codex must output the still-not-closed FAM list plus every not-complete package/slice instead of creating selected-next truth.
- `Backlog Exhaustion User Decision Pending`:
  If the still-not-closed FAM plus not-complete package/slice list is empty and new work would require a new backlog identity, Codex must stop for USER direction instead of inventing the next lane.
- `Branch Readiness Execution User Approval Missing`:
  Branch Readiness Stage 1 - Analysis Gate is a no-work review pass. Branch Readiness cannot enter Branch Readiness Stage 2 - Execution Gate, mutate repository files, create a branch, admit a package, sync docs, create selected-next truth, prepare PR work, or perform release work until the Stage 1 packet is returned and explicit USER approval to enter Stage 2 is recorded.
- `Thread / Worktree Identity Mismatch`:
  Any phase, branch creation, worktree creation, commit, push, PR creation, release action, or GitHub Desktop handoff must stop when the active local folder, git root, branch, upstream, `HEAD`, `origin/main`, worktree role, runtime/process ownership, or GitHub Desktop binding does not match the requested thread/workstream. Codex must report the expected workspace, actual workspace, expected branch, actual branch, expected thread/workstream role, actual repo state, and safest next correction before continuing.
- `Single-Slice Package User Approval Missing`:
  Branch Readiness and Workstream cannot greenlight a package with exactly one admitted slice unless explicit USER approval records `Single-Slice Package User Approval: Granted`. Historical evidence rows, merged evidence rows, future placeholders, deferred ideas, and future-package-required rows do not count as admitted slices.
- `Package Completion Unproven`:
  Workstream cannot advance to Hardening until every admitted package slice is complete, deferred, blocked, or explicitly preserved as released-baseline/open package truth with `Package Completion State:` recorded. Package completion cannot be green while admitted slices remain incomplete.
- `Deferred Selection Context Missing`:
  PR Readiness cannot be green when the selected next workstream is deferred but lacks `Deferred Since:`, `Deferred Because:`, or `Selection / Unblock:` in the backlog entry
- `Dirty Branch`:
  PR Readiness cannot be green while the worktree is dirty, required docs changes are uncommitted, required canon exists only in the working tree, or branch truth is not durable in commit history
- `Docs Sync Incomplete`:
  docs sync, Governance Drift Audit, validator alignment, and any required post-merge state wording must be complete and mutually consistent
  merge-target pointer surfaces must be merge-stable: during explicitly USER-approved exceptional merged-unreleased release-handling windows, `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, and the canonical workstream `## Phase Status` block may describe only the durable evidence-pointer truth that will still be correct after merge
  merge-target branch-head hash assertions such as ``origin/main` is `<sha>`` or ``origin/main` remains at `<sha>`` are operator facts only and must not appear in merge-stable current-state owner sections
- `User-Facing Shortcut Validation Pending`:
  Live Validation and PR Readiness cannot be final-green for a relevant desktop user-facing workstream until the final Live Validation closeout has launched through the declared user-facing desktop shortcut or equivalent user entrypoint, recorded `User-Facing Shortcut Validation: PASS` or `User-Facing Shortcut Validation: WAIVED`, and preserved the evidence before User Test Summary handoff
- `User Test Summary Results Pending`:
  Live Validation and PR Readiness cannot be green while a user-facing workstream has a required User Test Summary handoff outstanding and returned results have not been submitted, waived, digested into the active authority record, and reevaluated. Workstream must not list this blocker as the reason to stop implementation; unresolved product work belongs to `Backlog Completion Unproven`, named implementation blockers, or the next bounded Workstream seam.
- `PR Creation Pending`:
  PR Readiness package-ready is not PR Readiness green. PR Readiness Stage 1 may record `Pre-PR Live State: No live PR`, `PR Creation Approval: Pending USER approval`, and `Stage 2 PR Creation: Pending USER approval` while it is still analyzing and repairing pre-PR posture; that state is lawful only before Stage 2 approval and must not be reported as PR-ready green. PR Readiness cannot be green until Stage 2 has USER approval and the GitHub PR exists for the current head branch and base branch.
- `PR Validation Pending`:
  PR Readiness cannot be green until the existing PR has been validated as open, non-draft, conflict-free, aligned to the merge-target canon, and clear of unresolved Codex comments/issues or requested changes.
- `PR State Unknown`:
  PR Readiness cannot be green if Codex cannot inspect the PR state, mergeability/conflict state, base/head alignment, or Codex review-thread state.
- `PR Readiness Execution User Approval Missing`:
  PR Readiness Stage 1 - Analysis Gate is an analysis-first readiness-lock gate. PR Readiness cannot enter PR Readiness Stage 2 - Execution Gate, create the PR, create recurring PR watcher automation, create a next branch, or perform release work until the Stage 1 packet is returned, all USER-approved current-branch Stage 1 repair/re-entry items are validated and durable on the current branch, `Stage 1 Ready For Stage 2` is recorded, and explicit USER approval to enter Stage 2 is recorded.
  This preserves the existing analysis-first blocker repair gate inside the readiness lock.
- `PR Readiness Stage 1 Repair Pending`:
  When PR Readiness Stage 1 finds repo drift, source-truth drift, validator drift, branch-authority drift, or a PR-readiness blocker that can be repaired on the current branch, Stage 1 records `PR Readiness Stage 1 Repair Required` and must remain in Stage 1 until the repair is complete. Stage 1 repair/sync may mutate, stage, commit, and push the active branch only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that bounded PR-readiness repair work; Stage 1 specifically owns repair or validation of already-encoded selected-next truth, merge-target `No Active Branch` projection, no-release-debt posture, any unavoidable merged-unreleased release-debt owner contract, and active-branch-authority cleanup when those items are found, and they must not be deferred to Stage 2 as planned sync. Stage 1 still cannot create a PR, create recurring PR watcher automation, create a branch, admit a package, waive single-slice rules, create a tag, create release artifacts, draft or publish a GitHub Release, or execute a release. Stage 1 may encode selected-next truth only when USER explicitly approves that selected-next sync, and it still must leave branch creation plus runtime package admission blocked for Branch Readiness.
- `No Successor Runtime Branch By Inertia`:
  Retired as a default PR Readiness waiver requirement after the external-state/index-only reform. Source-only, docs-only, governance, validator, or repo-wide support branches must not invent the next runtime carrier merely to satisfy selected-next gates. When no USER-approved selected-next truth exists, post-merge `No Active Branch` is allowed and the next runtime implementation pipeline waits for Branch Readiness Stage 1; this does not create, select, or admit a runtime successor.
- `Stage 1 USER Waiver Required`:
  PR Readiness Stage 1 may request an explicit USER waiver for a required Stage 1 review item only when repo truth allows a waiver. A selected-next waiver is not required merely because selected-next truth is absent; normal successor selection belongs to Branch Readiness Stage 1.
- `Next Workstream User Waiver Missing`:
  Retired as a default PR Readiness continuation blocker. PR Readiness does not require selected-next truth or a waiver by default. If USER explicitly asks PR Readiness to encode selected-next truth, the packet must record the USER decision and validate that selected-next truth; otherwise the next runtime implementation pipeline is selected later in Branch Readiness Stage 1.
- `Next Branch Package Shape Unproven`:
  Branch Readiness Stage 1 owns normal next-branch package-shape proof. PR Readiness uses this blocker only when USER explicitly approved PR-time selected-next encoding or when already-encoded selected-next truth is inconsistent.
- `Single-Slice Branch Drift Risk Unresolved`:
  Branch Readiness Stage 1 owns normal single-slice drift review for the next branch. PR Readiness uses this blocker only for already-encoded selected-next truth that would be merged as durable source truth.
- `Family Organization Drift Risk Unresolved`:
  Branch Readiness Stage 1 owns normal family-organization review for the next branch. PR Readiness uses this blocker only for already-encoded selected-next truth that drifts away from the FAM -> Package -> Slice -> Seam model.
- `Current-Branch Branch Readiness Re-entry Required`:
  PR Readiness Stage 1 cannot continue to Stage 2 when next-workstream, next-branch, or governance/source-of-truth ledger blockers show that the current branch is still the legal carrier, but the fix is broader than bounded PR-readiness sync and must re-enter Branch Readiness on the same branch. This includes branch-shape drift, package/slice admission drift, or ledger repair that needs the current carrier's Branch Readiness authority before PR execution.
- `New Carrier Branch Required`:
  PR Readiness Stage 1 cannot continue to Stage 2 when the current branch is stale, merged, invalid, or legally cannot own the blocker, so a new real carrier branch is required. This applies to selected-next and next-branch shape blockers only when USER-approved PR-time selected-next truth or already-encoded selected-next truth is in scope, or to ledger items that cannot be cleared without USER approval or a new Branch Readiness carrier. Ledger-triggered fallback covers identity model drift, FAM taxonomy drift, package/branch rule drift, USER approval blocker drift, Branch Readiness or PR Readiness staging drift, selected-next recommendation drift when in scope, real-carrier routing drift, branch-authority lifecycle drift, watcher/automation proof drift, release readiness/execution boundary drift, Element Coverage misuse, ChatGPT loader/source-truth drift, project direction drift, current workflow drift, after-release workflow drift, and absolute-guardrail drift. The Stage 1 packet must output `Governance Ledger Fallback:` and `Branch Readiness Fallback:` and route the next legal work to Branch Readiness rather than create a PR, watcher, branch, package, selected-next truth, or release artifact by inertia. Branch Readiness fallback is real carrier branch/package analysis when PR Stage 1 cannot legally clear the blocker on the current branch; it is not workstream selection by default.
- `PR Merge Status Unproven`:
  PR Readiness cannot be green until the live PR has explicitly reported a green merge status. Treat unknown, unset, conflicting, dirty, blocked, or otherwise non-green mergeability/merge-state results as an active blocker until GitHub reports the PR merge status as green.
- `Bot Review Signal Pending`:
  for Codex-created PRs, PR Readiness cannot be green until the live PR has received a thumbs-up reaction or green approval comment from the Codex Connector bot. A bot comment is not approval; it keeps `PR Validation Pending` active until the branch fixes the comment on the same PR, pushes, replies to and resolves the review thread, requests Codex Connector bot revalidation, and receives a later Codex Connector bot thumbs-up reaction or green approval comment for the repaired live PR head. That approval proof must be bound to the current live PR head by review commit SHA, PR timeline order, or equivalent GitHub live-head evidence, not by local commit time alone. This is the same-PR Codex bot-review repair loop. Stage 2 final handoff cannot be green until the post-repair bot thumbs-up/approval latch is verified.
  When this blocker is active on a live Codex-created PR, Stage 2 must use direct PR verification before handoff; a manual "check later" plan is not enough, and recurring PR watcher automation is denied by default. Direct PR verification must inspect bot reactions, bot comments, review threads, PR comments, inline comments, PR state, status checks, and mergeability, and may perform bounded same-PR repairs for valid Codex bot comments that stay inside the approved PR scope. If no Codex bot comment or thumbs-up/approval signal appears after the current PR head has been live for at least two minutes, Codex may post exactly one PR conversation nudge for that head SHA asking the Codex bot for the review signal, and must not repeat that nudge for the same head. Every Codex Connector review-request or revalidation PR comment must be 3-5 words only, preferably `@codex review please`; head SHAs, validation summaries, repair narratives, and governance proof belong in the Codex thread digest, helper output, validator output, or external operational state, not in the PR comment. The required repair loop is: verify identity, evaluate the bot comment against source truth, repair only approved same-PR scope, rerun required validation, commit and push to the same branch, reply/resolve only when the review-thread contract requires it, request Codex Connector bot revalidation, and continue direct PR verification until the later thumbs-up/approval latch clears. The Direct PR2 Continuation Rule blocks quiet handoff: after any revalidation request or repair push, bounded PR2 must keep checking the live PR in the active Codex turn until a new actionable Codex comment is repaired or blocked, a current-head Codex approval latch plus green mergeability allows merge, the PR merges/closes, or a real blocker prevents further direct verification. Out-of-scope bot requests must be reported as `BLOCKED`, not repaired.
- `PR Watcher Provisioning Unproven`:
  recurring PR watcher automation is denied by default for bounded PR Readiness Stage 2. This blocker applies only when the USER explicitly approves a named watcher exception for the live PR. If an exception is approved, the watcher target, approved reporting surface, routing proof, runtime path, run-proof method, fallback, teardown rule, replacement provisioning for the next live PR, and the live bot-review action contract must be explicit and proven before watcher-based proof can support PR Readiness. Watcher configuration is not runtime proof. Manual rollout-file or transcript-file injection does not count as proof.
  The action contract is part of any approved exception: thumbs-up reaction means report green for PR-entry validation; one or more actionable bot comments means trigger the bounded same-branch PR comment-repair worker, fix the issue, commit, push, reply, resolve the corresponding review thread, request Codex Connector bot revalidation with a 3-5 word PR comment only, and then keep `PR Validation Pending` active until a later thumbs-up reaction or green approval comment clears the repaired head. If the repair worker cannot complete safely, keep `PR Validation Pending` active and surface the exact blocking comment.
  PR watcher mode must be explicit under the PR Watcher Mode Contract in `Docs/pr_watcher_mode_contract.md`: `Silent Monitor`, `Verify Once`, `Repair Mode`, or `Blocked Mode`. Every approved watcher exception Verify Once post must include `Watcher Health Proof:` with `Watcher Mode:`, `Configured CWD:`, `Worktree / Branch:`, `PR:`, `Head SHA:`, `Mergeability:`, `Unresolved Review Threads:`, `Latest Bot Review:`, `Repair Authority:`, `Delivery Route Proof:`, `Runtime Proof:`, and `Next Watcher Posture:`.
- `PR Watcher Routing Unverified`:
  applies only to a USER-approved watcher exception. Even after watcher provisioning exists and run proof is present, watcher-based proof cannot support PR Readiness until the approved reporting surface is explicitly recorded and a validation pass confirms the configured thread/host target, state-file target, transcript target, and delivery proof all point to that recorded surface and that at least one watcher emission has landed there. Direct PR verification is the bounded PR2 default when no watcher exception exists.
- `PR Merge Verification Pending`:
  after PR creation, live PR validation, green merge status, and bot-review approval are complete, PR Readiness stays non-green until direct GitHub/GitHub-connector verification proves that the live PR is actually `merged`. If the USER approved a watcher exception, that watcher may provide additional merge evidence, but recurring watcher automation is not the default merge-verification owner.
  Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript. If missing proof blocks a release and the branch has not merged, return to `PR Readiness`; if the branch has already merged, carry it on the next real runtime package carrier's `Branch Readiness`.
- `Automation Runtime Unproven`:
  phase-critical automation cannot clear a gate merely because its card, config, or automation list says `ACTIVE`; `ACTIVE` is configuration state, not run proof. Accept run evidence only from thread or inbox output, automation memory/log/state-file updates, or scheduler last-run evidence. If the preferred Codex automation remains `ACTIVE` without run evidence, keep the owning phase blocked until run evidence exists or a bounded fallback is activated. Any bounded fallback must be target-scoped, phase-scoped, read-only, and self-terminating or explicitly deleted when its terminal condition or phase exit occurs.
- `Automation Observability Review Pending`:
  standing automations report into Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`; those reports become source-of-truth work only after `dev/automation_observability_report.py` or a live automation report classifies them as `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED`. Informational green or waiting reports remain `REVIEW_INFO` unless contradicted by repo truth. Any admitted automation finding must enter a bounded repair seam before repo canon changes.
  Multi-worktree automation must also prove its configured cwd, git root, worktree role, branch, `HEAD`, and `origin/main` posture before a report may influence active-lane truth. `Automation CWD Worktree Mismatch` is the blocker when a standing automation runs from a missing, stale, neutral-main, parked, or wrong-lane worktree for the prompt it is carrying. Lane-sensitive prompts that mention active branch, PR Readiness, Release Readiness, post-merge, release-window, selected-next, toolchain, or branch governance cannot run from stale neutral main as if it were an assigned FAM or Governance lane. Automation memory is evidence only; stale `$CODEX_HOME/automations/*/memory.md`, Codex automation run/inbox summaries, or historical prompt assumptions must report `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED`, not mutate canon directly.
  Background-observability-only automations cannot clear phase gates, bot-review gates, PR merge verification, release readiness, or same-PR repair proof. A stale historical toolchain-path report is `REVIEW_INFO` unless a current source-truth owner still declares that exact path active; otherwise the repair is to update the automation contract, not to recreate old files by inertia.
- `PR Readiness Scope Missed`:
  PR Readiness cannot be green if branch-authority cleanup, merge-target canon, post-merge truth, next-workstream selection, next-branch deferral, or release-debt routing is incomplete or being deferred to Release Readiness, updated `main`, or a later governance-only branch
- `Release Window Audit Incomplete`:
  PR Readiness cannot be green inside an unreleased release window until the active branch has audited that window, listed the currently known blocker set, and either clears those blockers on the same branch or records an explicit split waiver with user approval. Do not merge one blocker-clearing PR while already knowing that another blocker-clearing PR is queued behind it in the same unreleased window by default.
- `Release Readiness Health Pass Incomplete`:
  PR Readiness must prove post-merge source truth before PR creation or merge readiness. PR Readiness cannot be green until the active PR branch has run and recorded the `Release Readiness Health Pass`, using `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`, so projected merged `main` would enter Release Readiness without stale source-truth cleanup.
- `Between-Branch Canon Repair Attempt`:
  PR Readiness cannot rely on any canon repair that is planned between branches rather than committed on the active branch before merge
- `Next Branch Created Too Early`:
  PR Readiness cannot be green if the next implementation branch already exists before the current branch has merged and updated `main` has been revalidated

The PR-readiness validator gate must be run in its PR-specific mode before reporting `PR READY: YES`.
If the normal governance validator passes but the PR-specific gate reports dirty worktree or unresolved PR blockers, the result is not PR-ready.

### PR Readiness Stage Gates

`PR Readiness` remains one canonical phase. It is organized into two internal stage gates:

- `PR Readiness Stage 1 - Analysis Gate`: analysis-first readiness-lock gate. Stage 1 must analyze repo truth, identify PR-readiness drift/blockers, output the full `## PR Readiness Stage 1 Analysis Packet` for USER review, including Stage 2 execution plan, and remain active until one outcome is recorded: `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, or `Stage 1 USER Waiver Required`. Bounded Stage 1 repair/sync is allowed only when the current branch is the legal carrier and the USER-approved current phase/seam authorizes that repair; repair truth must be validated, committed, and pushed before Stage 1 can be declared ready. Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection, rooted in Nexus Vision, family vision, branch vision, current completed work, and the next implementation need. PR Readiness does not require selected-next truth or a waiver by default; Stage 1 owns repair or validation of selected-next truth only when USER explicitly approves PR-time selected-next sync or selected-next truth already exists and would merge as durable repo truth. Stage 1 also owns merge-target `No Active Branch` projection, no-release-debt posture, release target/floor semantics and Release Window Audit when relevant, any unavoidable merged-unreleased release-debt owner contract, and active-branch-authority cleanup when Stage 1 finds them. Stage 1 still cannot create the PR, create recurring PR watcher automation, create the next branch, execute release work, create tags/artifacts/releases, admit packages, or grant waivers without explicit USER approval. Stage 1 may encode selected-next truth only when USER explicitly approves that selected-next sync, and Stage 2 must verify the synced truth before PR creation.
  This preserves the existing analysis-first blocker repair gate inside the readiness lock.
- `PR Readiness Stage 2 - Execution Gate`: begins only after explicit USER approval to enter Stage 2 and only when Stage 1 reports `Stage 1 Ready For Stage 2`. Stage 2 owns final PR execution only: verifying durable Stage 1 projection, commit/push only for bounded operator metadata if legally needed, PR creation, direct PR verification, bot-review handling, mergeability validation, and direct merge/close verification. Recurring PR watcher automation is denied by default and requires a separate USER-approved watcher exception for the exact PR. Direct PR2 does not hand off while waiting for a bot response; it continues by direct PR verification until approval-plus-green-mergeability permits merge, a new comment is repaired or blocked, the PR merges/closes, or a real blocker appears.

The `## PR Readiness Stage 1 Analysis Packet` must include governed state markers, the planned PR title/base/head/summary, required post-merge path, release-debt impact, release-debt handling status, selected-next validation status when selected-next truth exists or PR-time selection is explicitly approved, required current-branch source-truth sync, completed merge-target canon updates when repairable drift is found, planned direct PR verification, planned watcher provisioning posture of `Denied by default` unless a USER-approved exception exists, planned validations, expected Stage 2 execution work, Stage 1 repairs made, Stage 1 repair validation, Governance Ledger fallback status, Branch Readiness fallback status, Stage 2 execution plan, drift findings, blocker and waiver findings, release-window audit posture, rollback path, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed from the USER. Packet field labels include `Selected-Next Validation Status:`, `Selected-Next Scope:`, `Branch Readiness Stage 1 Successor Selection Owner:`, `Optional Next Branch Block:`, and `Planned Watcher Provisioning:` so the output proves selected-next is either out of scope by default or explicitly validated and proves recurring watcher automation will not be created by inertia. It may repair Stage 1 PR-readiness blockers on the current branch, but it must not perform Stage 2, create the PR, or create recurring watcher automation. It may encode selected-next truth only when USER explicitly approves selected-next sync, and branch creation plus runtime package admission must stay blocked for Branch Readiness. PR creation is blocked while any Stage 1 blocker, Stage 1 repair item, selected-next validation item when applicable, branch-shape review item when applicable, merge-target authority projection item, no-release-debt posture, unavoidable release-debt owner contract, or Stage 2 execution prerequisite remains unresolved.

When the active external branch planning owner contains UFD items, PR Readiness Stage 1 must include a USER Feedback Disposition fold-down review. Every `Feedback ID:` must be implemented, rejected/no-action with reason, deferred with waiver, folded into the structured branch receipt, promoted to Nexus/family vision when reusable, carried as a backlog future-candidate pointer only after USER acceptance, or assigned to a named future owner. The fold-down receipt must preserve a lookup path from each UFD ID to its final owner before the external branch plan can retire from active planning posture.

`PR package ready` is the state where local branch truth, merge-target canon, applicable selected-next validation, and copy-ready PR details are complete. It is not `PR Readiness GREEN`.

Live PR creation and validation facts are required for operator output and PR validation, but they are not merge-target current-state truth. Keep live PR state such as `open`, `non-draft`, `mergeable`, review-thread counts, repair-commit containment timing, blocker-clearing branch narration, and merge-target branch-head hash assertions in operator output and explicit historical PR sections only. Do not place those time-sensitive claims in merge-target current-state owner sections such as backlog or roadmap `## Current Branch Execution Posture`, `PR Readiness State:`, `Current Branch Objective:`, `Active Workstream Chain:`, or the canonical workstream merged-unreleased `## Phase Status` block.

Merge-target post-merge-stable authority projection is mandatory before PR green and is a PR Readiness Stage 1 repair responsibility when Stage 1 finds it. The PR branch must not merge an active branch authority record into `main`; the active authority record must be moved to historical/no-active posture or otherwise made merge-stable during Stage 1 before Stage 2 can execute. Post-merge `No Active Branch` does not require selected-next waiver truth when no USER-approved selected-next truth exists; normal successor selection waits for Branch Readiness Stage 1. Historical branch records must not retain active PR Readiness phase, active seam ownership, live/open PR wording, merge-watch ownership, or `PR Merge Verification Pending`. Operational PR/watcher facts may live in operator output or explicit historical PR sections, but merged current-state owners and historical authority records must already describe the post-merge truth that will remain valid after merge.

A post-merge projection receipt is not enough by itself. If a branch creates a separate projection file, PR Readiness Stage 1 must still fold down the real active authority record or remove it from `Active Branch Authority Records` before it reports `Stage 1 Ready For Stage 2`, before Stage 2 PR creation, and before merge approval. Projection-beside-active-authority blocks on `Merge-Stable Projection Shadowed By Active Authority`.

Projection-only fold-down inside the active record is also not enough. If the active branch record's `Release Readiness Health Pass` or `Post-Merge State` says the branch must become historical/no-active, must not remain active branch authority, or must become historical merged-unreleased evidence, PR Readiness Stage 1 must perform that real fold-down before Stage 2, PR green, or merge approval. Leaving the actual record in `Active Branch Authority Records` blocks on `PR Readiness Stage 1 branch-authority fold-down required`.

`Merge-Target Authority Projection Unproven` blocks PR green whenever that post-merge-stable authority projection is missing or would leave active branch-authority truth in merged `main`.

### Release Readiness Health Pass

The `Release Readiness Health Pass` is a PR Readiness pre-merge gate. It must run during PR Readiness Stage 1, after any Stage 2 or bot-review repair that changes source truth, and again before merge approval if the branch source truth changed after the prior run. The command is:

```powershell
python dev\orin_branch_governance_validation.py --release-readiness-health-gate
```

The health pass proves post-merge source truth before PR creation or merge readiness. It must fail if projected merged `main` would force Release Readiness to repair source truth instead of validating release posture.

The owning branch/workstream authority record must include:

- `Post-Merge Branch Authority Projection:`
- `Stale Active Branch Wording Scan:`
- `Stale PR Creation / PR Readiness Pending Wording Scan:`
- `Merged-Unreleased Scope Posture:`
- `Release Execution Gate:`
- `Watcher / Live PR State Projection:`
- `Branch Cleanup Plan:`
- `Branch Cleanup Execution Gate:`
- `FAM Overlap Routing:`
- `Release Candidate Anchor Projection:`
- `Release Window Contributor Inventory:`
- `Governance Intake Routing:`
- `Projected Post-Merge Validation:`

Passing posture means exact post-merge branch-authority projection is recorded, no stale active branch wording lands on `main`, no stale PR creation / PR Readiness Stage 2 pending wording lands on `main`, merged scope is recorded as merged-unreleased when release execution is not being performed, release execution/tag/GitHub Release/artifact work remains gated, watcher/live PR state stays out of merged-main source truth, branch cleanup plan is known, FAM overlap is either non-blocking or routed to the owning lane, release-candidate anchor and release-window contributors are unambiguous, any post-merge source-truth blocker routing says `Governance Intake Routing: send this to C:\Nexus Worktrees\Governance on feature/release-readiness-source-truth-intake`, selected-next or successor truth is not stale, release-window/release-floor posture is resolved, and projected post-merge main would pass validation without a later source-truth repair.

Merge-Stable Source Truth Projection Gate:

- PR Readiness must prove the source truth that will remain valid after the PR merges, not only the pre-PR state that is true before Stage 2.
- Pre-PR markers such as `No live PR`, `PR Creation Approval: Pending`, `Stage 2 PR Creation: Pending`, `PR creation pending`, and `PR Readiness Stage 1 Ready For Stage 2` are lawful only inside clearly labeled historical pre-PR snapshot sections after a PR merges.
- Merged-main current-state owners, compact pointer rows, worktree slot receipts, active external branch planning owners, and canonical branch records must instead project historical merged-unreleased, released/closed, or no-active-branch posture after merge.
- If a merged branch record remains a canonical detail owner, it must name the merge PR/commit when known, clear active PR Readiness / PR creation pending wording from summary fields, retire or historical-label any repo branch-plan receipt, and route release execution as a separate USER decision.
- `Merged Active Branch Authority Not Folded Down` blocks when any non-standing branch listed under `Active Branch Authority Records` points to a branch ref already merged into `origin/main`; the validator must compare the branch ref to `origin/main` instead of relying only on compact `No Active Branch` wording.
- `Merge-Stable Projection Shadowed By Active Authority` blocks when a separate historical projection record exists for a branch but the same branch still has an active authority record in `Active Branch Authority Records`.
- `Merge-Stable Source Truth Projection Missing` blocks PR green, merge approval, or Release Readiness Stage 2 when stale pre-PR or Stage 2-pending wording would land in merged-main source truth.

Branch cleanup is planning-only until Branch Readiness owns a new branch/worktree target. `Branch Cleanup Plan:` records stale/old branch refs, retired worktrees, or GitHub Desktop repository entries that may need cleanup after merge. `Branch Cleanup Execution Gate:` must say cleanup is blocked in Release Readiness and may execute only during the next `Branch Readiness Stage 2 - Execution Gate` that creates or validates the next branch/worktree target. Multi-worktree cleanup must not delete a branch checked out by any worktree, remove a worktree before its replacement target is validated, or leave a GitHub Desktop-bound worktree without a valid branch target; stale/old branch cleanup waits until the replacement branch/worktree is created, Desktop is bound to the intended folder, and `git worktree list` proves no checked-out branch will be orphaned. `Stable Worktree Path Preservation Gate:` is mandatory when cleanup touches a family-stable or GitHub Desktop-bound folder path: record `Stable Worktree Path:`, `Replacement Binding Path:`, and the preservation method, and block on `Stable Worktree Path At Risk` unless the stable folder path remains the active repository target before the retired worktree or branch is removed.

`PR Readiness GREEN` requires all `PR package ready` conditions plus:

- the GitHub PR exists
- the PR is open and not draft
- the PR base/head match merge-target canon
- the PR has no conflicts
- PR state is inspectable rather than unknown
- no unresolved Codex comments/issues or requested changes remain
- direct PR verification has inspected the live PR head, mergeability, checks, Codex comments/reviews, approval latch, and merge/close posture in the active Codex turn or helper output
- the Direct PR2 Continuation Rule has not been bypassed; bounded PR2 did not stop on a quiet bot wait when direct verification could continue
- `PR Watcher Provisioning Unproven` and `PR Watcher Routing Unverified` are not active unless the USER explicitly approved a watcher exception for that PR
- `PR Merge Status Unproven` is clear only after the live PR has explicitly reported a green merge status
- `PR Merge Verification Pending` is clear only after direct GitHub/GitHub-connector verification proves that the live PR is `merged`
- the live PR has a thumbs-up reaction or green approval comment from the Codex Connector bot for the current head; when a bot comment appeared after the last approval, a later thumbs-up/approval signal is required after same-PR repair and comment-resolution closeout

### PR Readiness Response Contract

Every `PR Readiness` response must identify whether it is in `PR Readiness Stage 1 - Analysis Gate` or `PR Readiness Stage 2 - Execution Gate`.
When the response is Stage 1, it must include this packet and stop on `PR Readiness Execution User Approval Missing` until USER approval to enter Stage 2 is recorded:

```markdown
## PR Readiness Stage 1 Analysis Packet
- Current PR Readiness Stage:
- Repository Mutation Status:
- Planned PR Title:
- Planned Base Branch:
- Planned Head Branch:
- Planned PR Summary:
- Required Post-Merge Path:
- Selected-Next Validation Status:
- Selected-Next Scope:
- Branch Readiness Stage 1 Successor Selection Owner:
- Package-Size / Single-Slice Drift Review:
- Element Coverage Review:
- Release-Debt Impact:
- Release-Debt Handling Status:
- No-Release-Debt Handling Status:
- Required Current-Branch Source-Truth Sync:
- Planned Merge-Target Canon Updates:
- Origin/Main Freshness Check:
- Branch Creation Base:
- Current origin/main:
- Origin/Main Advanced Since Branch Creation:
- Origin/Main Changed Files:
- Branch Changed Files:
- Reconciliation Required:
- Reconciliation File List:
- Reconciliation Recommendation:
- Reconciliation Mutation Status:
- Optional Next Branch Block:
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

Selected-next fields in this packet are validation/status fields, not a request for PR Readiness to create successor truth. `Optional Next Branch Block:` must be `Not in scope` unless USER explicitly requested PR-time successor selection, selected-next truth already exists, or Branch Readiness is the next legal phase.

Allowed Stage 1 outcomes are exactly `Stage 1 Ready For Stage 2`, `PR Readiness Stage 1 Repair Required`, `Current-Branch Branch Readiness Re-entry Required`, `New Carrier Branch Required`, and `Stage 1 USER Waiver Required`. `PR Readiness Stage 1 Repair Required` means bounded current-branch PR-readiness repair/sync remains in Stage 1 before Stage 2. `Current-Branch Branch Readiness Re-entry Required` means the current branch is still the legal carrier, but the fix is broader than PR-readiness sync and must re-enter Branch Readiness on the same branch. `New Carrier Branch Required` means the current branch is stale, merged, invalid, or legally cannot own the blocker, so a new real carrier branch is required. Stage 2 may begin only after `Stage 1 Ready For Stage 2` is recorded and explicit USER approval to enter Stage 2 exists.
Stage 2 begins only after `Stage 1 Ready For Stage 2` and explicit USER approval.
Branch Readiness Stage 1 owns the normal next runtime implementation pipeline selection. That selection must be rooted in project vision, family vision, branch vision, current completed work, and the next implementation need. PR Readiness may recommend next-workstream context, but it does not require selected-next truth or a waiver by default and must not create next-branch live state by inertia. Selected-next truth and active branch authority are different states. PR Readiness validates selected-next truth only when USER explicitly approves PR-time successor selection or already-encoded selected-next truth would merge as durable source truth. If no successor is approved before merge, merged `main` may be steady-state `No Active Branch` while carrying valid merged-unreleased release-window truth, and the next implementation carrier must be selected later through Branch Readiness from current `origin/main` and external operational state. Default governance validation and `--pr-readiness-gate` both own stale active-authority closeout so Release Readiness does not discover stale active-authority truth after merge.

After a PR merges, active branch authority is invalid for that merged branch even when backlog, roadmap, or worktree slots do not project `No Active Branch`. `Active Branch Authority Records` may not retain a non-standing branch whose local or remote ref is already an ancestor of `origin/main`; failing to fold that record down to historical/no-active posture blocks on `Merged Active Branch Authority Not Folded Down`.

`Origin/Main Freshness Check` is required during PR Readiness Stage 1 before Stage 2 can begin. Stage 1 must compare `Branch Creation Base:` to `Current origin/main:` and report whether `Origin/Main Advanced Since Branch Creation:` is `YES` or `NO`. When `origin/main` advanced, Stage 1 must list `Origin/Main Changed Files:` from `git diff --name-only <branch-creation-base>..origin/main`, list `Branch Changed Files:` from `git diff --name-only <branch-creation-base>..HEAD`, decide `Reconciliation Required: YES / NO`, and, when reconciliation is needed, output a complete `Reconciliation File List:` plus `Reconciliation Recommendation:`. The `Reconciliation Mutation Status:` must be analysis-only with no file fixes during Stage 1. If changed upstream files/data need review and the packet is missing or incomplete, `Origin Main Reconciliation Packet Required` blocks Stage 2 and PR creation.

`Pre-Rebaseline Impact Audit` is required before any same-branch current-main reconciliation operation actually mutates local branch state. `Origin/Main Freshness Check` identifies whether upstream advanced before PR Stage 2; `Pre-Rebaseline Impact Audit` is the operation-level proof that reports `Incoming Main Change Set:`, `Incoming Changed Files:`, `Current Worktree Changed Files:`, `Branch Changed Files:`, `Rebaseline Overlap Files:`, `Incoming Runtime / Source-Truth Risk:`, `Validation Before Rebaseline:`, `Recommendation Only:`, `Rebaseline Mutation Approval:`, and `Rebaseline Mutation Status:` before Codex may run a fast-forward, merge, rebase, conflict resolution, or branch switch. Any non-empty `Rebaseline Overlap Files:` value triggers the `Rebaseline Overlap Intent Gate` and must resolve or explicitly block on `Rebaseline Overlap Intent Missing` before mutation.

`Current-Main Reconciliation Identity Guard` is required whenever a multi-worktree branch rebases, fast-forwards, or merges current `origin/main`. origin/main is context, not identity. The assigned worktree must preserve and reassert its own branch-local authority before validation, commit, push, PR readiness, release readiness, or handoff. The reconciliation digest must include `Assigned Worktree Branch Identity:`, `Branch-Local Authority Reassertion:`, `Incoming Main Active-Branch Blocks Accepted: NO`, and `Sibling Worktree Identity Preservation:`. Passing posture means the active worktree's expected branch, actual branch, authority record, current-state owner files, and GitHub Desktop-bound worktree are named explicitly; incoming `origin/main` branch/current-workstream/selected-next blocks are treated as context unless they are the assigned branch's own authority; `Docs/feature_backlog.md` and `Docs/prebeta_roadmap.md` reassert the active worktree's branch-local authority after conflict resolution; sibling worktrees such as FAM-006, FAM-007, Governance, or neutral `main` are not switched, deleted, or mutated; and no reconciliation commit lands with another worktree's active branch/current workstream identity copied into the assigned lane. If this guard fails during Branch Readiness, PR Readiness, or a same-branch rebaseline, stop on `Worktree Branch Identity Drift` and repair source truth inside the assigned worktree before committing. If Release Readiness discovers the failure after merge, the output digest must say `Governance Intake Routing: send this to C:\Nexus Worktrees\Governance on feature/release-readiness-source-truth-intake`.

`Release Candidate Anchor Projection` is required during PR Readiness Stage 1 before Stage 2 can begin for any release-bearing or merged-unreleased branch. Stage 1 must name the default post-merge `Release Candidate Anchor:` as current fetched `origin/main` after merge unless USER explicitly selects a historical release target, must name `Target Commit:` projection or source, must state whether later governance/source-truth PRs are part of the candidate, and must keep historical PR endpoints as audit evidence only unless USER approves `Release Candidate Anchor Source: USER-selected historical commit`.

`Release Window Contributor Inventory` is required during PR Readiness Stage 1 before Stage 2 can begin for any release-bearing or merged-unreleased branch. Stage 1 must identify whether the projected release candidate may include multiple FAM/worktree contributors, must name each known merged-unreleased contributor included or expected to be included in the target commit, must state whether the release is `Release Ownership Model: Aggregated release window`, and must route any contributor-specific blocker to the owning lane instead of letting merge order decide release ownership.

Stage 1 may include this user-facing block as non-binding planning context when USER asks for next-workstream recommendations, or when already-encoded selected-next truth must be validated before merge. This block is not required for PR Readiness Stage 2 by default. It may encode selected-next truth only when USER explicitly approves selected-next sync, and it must not create a branch, admit a package, or waive any blocker without separate approval:

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
- Next Workstream User Waiver:
```

Missing next-workstream recommendation, missing selected-next truth, or missing `Next Workstream User Waiver:` does not block PR Readiness Stage 2 by default. If selected-next truth is already encoded, or USER explicitly approves PR-time successor selection, Stage 1 must validate the selected workstream and stop on the applicable selected-next blocker when that truth is inconsistent. Otherwise the next-workstream decision waits for Branch Readiness Stage 1.

Stage 1 may include this next-branch pre-plan gate only when USER asks PR Readiness for a next-branch recommendation or when selected-next truth already exists and must be validated. Normal next-branch package-shape proof belongs to Branch Readiness Stage 1. This block remains analysis-first and cannot create a branch, admit a package, or waive single-slice rules; it may encode selected-next truth only when USER explicitly approves selected-next sync and still leaves branch creation plus runtime package admission blocked for Branch Readiness:

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

If USER-approved PR-time selected-next truth exists and the packet cannot show a broad FAM/package with multiple concrete candidate slices, Stage 1 stops on `Next Branch Package Shape Unproven`. If the pre-plan still looks like a single-seam or single-slice branch, Stage 1 stops on `Single-Slice Branch Drift Risk Unresolved`. If the pre-plan drifts away from the family organization model or revives old live `FB-###` branch identity behavior, Stage 1 stops on `Family Organization Drift Risk Unresolved`. Otherwise those reviews wait for Branch Readiness Stage 1, which is the normal owner for next runtime implementation pipeline selection.

When `PR Readiness` reports package-ready or `PR package ready`, the response must include markdown-friendly PR operator copy blocks. Include a standardized `Next Branch` block only when USER explicitly requested PR-time successor selection, selected-next truth already exists, or Branch Readiness is the next legal phase.
Those package details are the input to PR creation and validation; they are not themselves proof that PR Readiness is GREEN.
This is a response contract, not permission to create the PR, merge the branch, release the branch, or create the next branch.

When included, the `Next Branch` block must distinguish the next legal branch from the selected next implementation branch.
For example, if USER explicitly approves unavoidable post-merge release handling, the next legal branch may be a release-support carrier while the selected next implementation branch remains deferred until after release handling and updated-`main` revalidation.

Optional conditional `Next Branch` block:

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

Required PR operator copy blocks:

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

## What Changed

<concrete implemented work, source-truth changes, behavior/capability changes, and useful historical context; do not repeat the Summary>
```
````

Each PR operator field must be its own copy-ready block and must be usable independently.
The PR summary/GitHub PR body uses exactly two top-level sections: `## Summary` and `## What Changed`.
`## Summary` must be one concise human-readable outcome paragraph, not a duplicated changelog.
`## What Changed` must describe the actual branch work in concrete Markdown-friendly detail without repeating the Summary verbatim or keeping nested `### Summary`, `### Purpose`, or `### Overview` sections that only restate the Summary; use concrete subheads such as `### Source Truth`, `### Runtime`, `### Tooling`, or `### Review Support` only when they improve scanability.
GitHub PR bodies and PR Summary copy must not include top-level or nested `## Validation`, `## PR posture`, `## Branch Evidence`, `Testing`, `Checks`, `Does not include`, `Not Included`, `Non-Includes`, `Deferred`, `Future-Gated`, generic defensive scope dumps, or phase-digest/operator handoff fields such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, `Stop Basis`, `Exact next USER decision`, `Implemented, validated`, or `::git-*`.
GitHub PR bodies and PR Summary copy must not include `## Validation`, `## PR posture`, `## Branch Evidence`, or defensive scope language.
Validation commands, command output, byte-proof evidence, mergeability, bot-review state, watcher state, and PR Readiness posture belong in Codex digests, helper output, status checks, or external operational state, not the GitHub PR body.
Before PR creation, Codex must write the proposed GitHub PR body to a local temporary file and run `python dev\orin_pr_body_quality_audit.py --body-file <path> --body-title "<PR title>"`. If the helper reports `Changed: True` or any warning, PR creation is blocked on `PR Body Drift Check Failed` until Codex reruns the helper with `--apply` or otherwise replaces the proposed body with the normalized body and reruns the check green. After PR creation, Codex must verify the live PR body with `python dev\orin_pr_body_quality_audit.py --limit 1` or a narrower equivalent. All visible PR bodies must be scanned by `dev\orin_pr_body_quality_audit.py`; every nonconforming PR body inside the approved GitHub correction scope must be repaired before the PR-body standard can be reported green. If broad historical PR body mutation is not approved or GitHub access blocks repair, Codex must report the exact blocker instead of calling the all-PR scan green.
When the conditional `Next Branch` block is included and `May Create Now` is `NO`, the subsection must explain the blocking gate rather than implying branch creation is allowed.

### Operator Output Content Rule

Operator-facing PR summaries are evidence-first, and GitHub release notes are inclusion-only.
They must report what exists, what was implemented, what capabilities are available, how the system behaves, and which validation or release facts support the package.
PR summaries must not report generic defensive scope dumps, exclusion lists, deferred work, or PR posture. They should read like human review summaries grounded in the branch's actual changes.
Operator-facing PR summaries must stay evidence-only and must not carry phase-digest handoff fields; a surrounding Codex closeout may include governed phase markers, but the GitHub PR body may not.
Historical PR normalization must preserve useful historical detail inside the same two-section PR body shape and remove redundant Summary/Purpose repetition from `## What Changed`.
Historical PR normalization must not delete Summary paragraphs or bullets merely to make the Summary concise. Any trimmed non-duplicate Summary detail must move into `## What Changed` under a concrete subheading before live GitHub PR bodies are edited.
GitHub release notes must also use the standard Markdown release body shape used by the current pre-Beta releases: the body starts with `## Release Summary` or `## Release Overview`, continues with `## Release Highlights` or release-specific rich sections, then includes GitHub-generated `## What's Changed` and the generated `**Full Changelog**:` compare link to the previous release. The live release body must not start with or repeat the release title as `# <release title>`; the release title belongs in GitHub release metadata and in the separate `Release Title` operator block only.
This rule governs operator output packages; it does not remove normal canon requirements for branch scope, non-goals, stop conditions, or blockers in source-of-truth records.

### User-Facing Shortcut Live Validation Gate

For relevant desktop user-facing workstreams, Live Validation may use validators, direct runtime launches, helper launches, synthetic harnesses, troubleshooting launchers, and targeted manual probes to build scenario coverage.
Those evidence layers are supporting proof, not final green by themselves.

Before User Test Summary handoff, the final Live Validation closeout must launch and exercise the branch through the exact normal USER desktop runtime launcher path declared for the branch.
For desktop UI Live Validation, no sandbox/offscreen/direct-runtime path can be the primary LV1 path when the normal USER desktop launcher is feasible. Direct runtime launches, WebView harnesses, helper launches, generated-equivalent shortcuts, active-client probes, and troubleshooting launcher runs are supporting evidence only unless launcher parity proof and USER approval make the troubleshooting launcher equivalent for the exact claim being validated.
For Nexus Desktop AI, the default normal desktop launcher path is normally `C:\Users\anden\OneDrive\Desktop\Nexus Desktop Launcher.lnk` unless the active authority record declares a different exact USER desktop launcher path. A generated shortcut or non-Desktop equivalent is invalid as final USER-path proof unless USER explicitly grants a waiver with reason.

Two-launcher exception:

- `Normal Desktop Runtime Launcher` owns ordinary USER proof.
- `Troubleshooting Runtime Launcher` is an explicit USER-consented diagnostic profile.
- Troubleshooting launcher evidence may count as formal equivalent proof only when `Launcher Parity Proof: PASS` shows both launchers start the same product runtime/build, use the same product data roots and user-visible behavior, and differ only by admitted diagnostic flags, diagnostic evidence roots, log level, and troubleshooting disclosure.
- If launcher parity is missing, fails, or the validated claim could be affected by troubleshooting-mode differences, Live Validation must use the normal USER desktop runtime launcher, request USER manual validation, or stop on a named blocker.

Named blocker:

- `User-Facing Shortcut Validation Pending`

Machine-checkable authority-record markers:

- `User-Facing Shortcut Path:`
- `User-Facing Shortcut Validation: PENDING`
- `User-Facing Shortcut Validation: PASS`
- `User-Facing Shortcut Validation: FAIL`
- `User-Facing Shortcut Validation: WAIVED`
- `User-Facing Shortcut Waiver Reason:`
- `Exact USER Desktop Launcher Path:`
- `Exact USER Desktop Launcher Validation: PENDING`
- `Exact USER Desktop Launcher Validation: PASS`
- `Exact USER Desktop Launcher Validation: FAIL`
- `Exact USER Desktop Launcher Validation: WAIVED`
- `Exact USER Desktop Launcher Waiver Reason:`
- `Troubleshooting Runtime Launcher Path:`
- `Troubleshooting Runtime Launcher Consent: PENDING`
- `Troubleshooting Runtime Launcher Consent: GRANTED`
- `Troubleshooting Runtime Launcher Consent: WAIVED`
- `Launcher Parity Proof: PENDING`
- `Launcher Parity Proof: PASS`
- `Launcher Parity Proof: FAIL`
- `Launcher Parity Proof: WAIVED`

Required proof:

- the declared exact normal USER desktop runtime launcher path launches the active branch runtime
- startup reaches the expected ready state
- the user-visible entry surface introduced or changed by the branch is visible or intentionally documented where the user must look for it
- relevant runtime markers, UI/manual readback, persisted-state checks, and cleanup evidence match the branch validation contract
- helper-only, direct-Python, WebView-only, sandbox/offscreen, active-client direct-runtime, generated-shortcut, troubleshooting-launcher-without-parity, or harness-only evidence is not treated as a substitute for this final launcher gate when the normal USER desktop launcher path is feasible

Lift condition:

- `User-Facing Shortcut Validation: PASS` and `Exact USER Desktop Launcher Validation: PASS` are recorded with evidence from the declared normal USER desktop launcher path, or both are recorded as `WAIVED` with reasons showing the branch is not desktop/user-facing or the exact normal launcher path is explicitly unavailable
- if troubleshooting launcher proof is used as equivalent, `Troubleshooting Runtime Launcher Consent: GRANTED` and `Launcher Parity Proof: PASS` are required before it can satisfy the exact claim being validated
- the blocker state is reevaluated after the result is digested

Routing:

- while `User-Facing Shortcut Validation: PENDING` remains, list `User-Facing Shortcut Validation Pending` under blockers and do not advance
- if `User-Facing Shortcut Validation: FAIL`, keep an explicit blocker and route back to `Workstream` or `Hardening` before PR Readiness
- if the shortcut gate passes or is waived, User Test Summary handoff may proceed only if all other Live Validation gates are green

Compatibility wording: the legacy phrase `real user-facing desktop launcher` means the exact normal USER desktop runtime launcher path declared for the branch; it is not a weaker substitute for the exact-launcher requirement.

### Runtime Observability / Live Validation Proof Contract

Rule Name: `Runtime Observability / Live Validation Proof Contract`
Owner: `Docs/phase_governance.md`
Applies To: BP2 USER Branch Plan Review, BP3 Workstream Entry / Orchestration Validation, Workstream implementation proof, Hardening H1, Live Validation LV1, User Test Summary handoff, active external branch plans, Live Validation helpers, USER review packets, and Codex return digests for runtime or user-facing desktop work.
Required State: every admitted feature, surface, control, window, bridge path, file/folder action, user-visible state transition, and validation-critical hidden state must receive an observability and proof decision before Workstream implementation begins. The decision must state whether normal runtime logs, troubleshooting-mode logs, Dev Toolkit instrumentation, exact normal desktop launcher proof, launcher parity proof, photo/video evidence, screenshot manifests, interaction matrices, manual USER validation, UTS coverage, privacy/redaction, user-visible disclosure, or future-gated observability are required.
Allowed Values: `Normal Runtime Log Required`, `Troubleshooting Log Required`, `Dev Toolkit Instrumentation Required`, `Exact USER Desktop Launcher Proof Required`, `Launcher Parity Proof Required`, `Photo / Video Proof Required`, `Manual USER Validation Required`, `UTS Coverage Required`, `No Log Needed With Reason`, `Privacy / Redaction Constraint`, `User-Visible Disclosure Required`, `Future-Gated Observability`, `Waived By USER With Reason`.
Invalid Values: `Helper PASS Is Proof`, `Marker PASS Is USER Proof`, `Direct Runtime Equals USER Path`, `Generated Shortcut Equals USER Launcher`, `Troubleshooting Equals Normal Without Parity`, `Screenshot Exists Therefore Accepted`, `Video Exists Without Adjudication`, `Unphotographable But Proven By Codex`, `Troubleshooting Enabled Silently`, `Internal Path Exposed As Product Folder`, `Evidence Packet Omitted`.
Blocking Condition: `Exact USER Desktop Launcher Proof Missing`, `Launcher Parity Proof Missing`, `Photo Or Video Proof Missing`, `Unphotographable Proof Not Elevated To USER`, `Direct Runtime Proof Misclassified`, `Troubleshooting Consent Missing`, `Live Validation Evidence Packet Incomplete`, `User-Visible Internal Path Leakage`, `Codex Live Client Self-QA Pending`, or `User Test Summary Results Pending` blocks the phase when applicable.
Repair Owner: current branch owner for product/runtime defects; owning helper/validator for proven tool defects; `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, and `Docs/validation_helper_registry.md` for reusable governance/validation drift; USER for waivers, manual validation, and troubleshooting consent.
Repair Path: add or repair the observability decision matrix, declare the exact normal USER desktop runtime launcher path, rerun formal LV through that launcher, capture photo/video or ordered frame-sequence evidence for visible claims, adjudicate each artifact against Project Vision / Family Vision / FFV / accepted BP1/BP2 contracts, attach or reference raw evidence in the USER packet, elevate unphotographable claims to USER manual validation or explicit waiver, classify direct-runtime/helper evidence as diagnostic-only when it is not the USER path, and route any implementation defect back to Workstream or Hardening. If a troubleshooting launcher is used as equivalent proof, first prove launcher parity and USER consent; otherwise it remains supporting evidence only.
USER Decision Required: required to waive exact normal launcher proof, accept troubleshooting launcher proof as equivalent, waive photo/video proof, accept manual validation for unphotographable claims, enable troubleshooting mode, export/share diagnostic logs, or accept a product UI folder/path that exposes internal implementation concepts.
Validation Owner: active Live Validation helper, `dev/orin_branch_governance_validation.py` when the rule becomes machine-checkable, `dev/orin_user_review_bundle.py` for USER packet completeness, and the relevant family/runtime validators.
Final Disposition: Live Validation may report green only when exact normal launcher proof or approved parity proof, photo/video proof or USER-elevated waiver, runtime/log consistency, Dev Toolkit or helper evidence, visual adjudication, UTS state, and USER packet evidence are all reconciled. Direct runtime evidence remains diagnostic/supporting proof unless exact USER desktop launcher validation is passed or explicitly waived.

Formal proof hierarchy for user-facing runtime work:

1. Exact normal USER desktop runtime launcher photo/video proof owns visible USER-path acceptance.
2. Troubleshooting runtime launcher proof may substitute only when USER consent is recorded, launcher parity proof is `PASS`, and the exact claim is not affected by allowed troubleshooting differences.
3. USER manual validation or explicit USER waiver owns required claims that cannot be proven in photo/video.
4. Runtime logs, Dev Toolkit events, manifests, validators, and helper output support diagnosis and consistency; they do not replace item 1, item 2, or item 3 for USER-facing acceptance.
5. Direct runtime, WebView, sandbox/offscreen, generated shortcut, or helper launch proof is diagnostic-only unless USER explicitly waives the exact launcher requirement.

Normal versus troubleshooting runtime mode:

- `Normal Runtime Mode` is the default product launch profile. It uses minimal privacy-safe logs and avoids broad diagnostic capture.
- `Troubleshooting Mode` is an explicit USER-consented diagnostic launch profile. It must be local by default, temporary/scoped, privacy-safe/redacted where needed, and visibly different from normal runtime.
- BP2/BP3 must decide whether troubleshooting mode is required for the branch. Workstream may implement instrumentation only when the approved scope admits it. Live Validation may use troubleshooting evidence only as supporting proof unless launcher parity and USER consent make it equivalent for the exact claim being validated.

### Codex Live Client Self-QA Gate

For relevant desktop user-facing workstreams, Codex must perform a live-client self-QA pass before handing the feature to the USER for a formal User Test Summary.
The pass is not a substitute for USER acceptance, but it is Codex-owned product validation: Codex must inspect the launched UI as if it were a user and judge quality, usability, platform uniformity, naming cleanliness, interaction posture, cleanup, and evidence quality before asking the USER to spend time testing.
For desktop UI branches, this inspection must be human-client faithful when the USER will operate visible tray/menu/window behavior. Codex cannot mark Live Validation Stage 1 green from app-side callbacks, fake/offscreen models, marker-only proof, screenshot-only proof, or direct handler calls. The final LV1 handoff requires a manifest that records visible desktop shortcut launch, visible tray/menu selection, mouse/cursor or UIAutomation-backed interaction evidence, window move/resize/open/close evidence where applicable, screenshot or frame-sequence artifacts, and Codex's own visual review of every issue-grounded UTS item. Missing human-client evidence is a Live Validation failure unless USER explicitly waives it.

Named blocker:

- `Codex Live Client Self-QA Pending`

Machine-checkable authority-record markers:

- `Codex Live Client Self-QA: PENDING`
- `Codex Live Client Self-QA: PASS`
- `Codex Live Client Self-QA: FAIL`
- `Codex Live Client Self-QA: WAIVED`
- `Codex Live Client Self-QA Waiver Reason:`
- `Live Client Entry Path:`
- `Evidence Screenshot:`
- `Visual Quality:`
- `Codex Visual Adjudication:`
- `Visual Artifact Review Scope:`
- `Product Vision Alignment:`
- `Per-Element Visual Verdicts:`
- `Helper Marker Limitation:`
- `Unacceptable UI Findings:`
- `LV1 Handoff Disposition:`
- `Interaction Manifest:`
- `Interaction Evidence Root:`
- `Live Interaction Evidence:`
- `Usability Check:`
- `Interaction Check:`
- `Platform Uniformity Check:`
- `NDAI Naming Check:`
- `Cleanup Check:`

Required proof:

- the launched UI is reviewed from the same live client path or declared equivalent used for the shortcut gate
- the visible surface is readable, intentionally placed, and visually coherent with Nexus Desktop AI
- interaction claims such as movement, anchoring, click-through/no-focus posture, tray paths, toggles, cards, snapping, and warnings are exercised in the launched live client when feasible and recorded under `Live Interaction Evidence:`
- screenshot-only, marker-only, or launched-but-not-driven proof cannot clear this gate for interactive user-facing UI
- desktop UI proof must provide an active foreground/user-observable validation path; a fast hidden or blink-through helper run may support automation but cannot be the only Codex live-client self-QA evidence
- desktop UI Live Validation must capture the full virtual desktop by default when placement, multi-monitor behavior, window separation, clipping, or frame-of-reference matters; primary-monitor-only screenshots are supporting detail only and cannot clear those proof needs
- screenshots used for Live Validation closeout must be copied into `C:\Users\anden\OneDrive\Pictures\Screenshots\<project-or-validation-lane>\<timestamp>\` or the active USER-declared screenshots folder, and the raw image path must be surfaced in the Codex chat/handoff for USER inspection; `dev/logs` copies alone are not enough when visual proof is part of the gate
- desktop UI Live Validation must also create a per-element visual inventory for the active user-facing surface, including every current user-facing window, border/frame, card, row, page break/divider, background treatment, scrollbar, button, dropdown, checkbox, input, chip, status field, confirmation, empty/error/deferred state, and every issue-specific element named by USER feedback
- desktop UI Live Validation must create detailed focused screenshots for each inventory element and supported state/action, copy them into `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\<validation-lane>\<timestamp>\focused_element_screenshots\`, and name each PNG with the element label/name plus state or action, such as `element_<label>_<state>.png`; a full desktop screenshot is locator/context proof only and cannot satisfy this per-element gate
- desktop UI Live Validation for resizable desktop windows must create and compare focused screenshots for the default usable size and compact legal minimum size for the Dashboard and every Dashboard child window or equivalent nested surface; this is mandatory, not advisory, and the manifest must prove every button, dropdown, checkbox, input, scroll pane, row, confirmation, empty/deferred/error state, and issue-grounded element remains visible, correctly scaled, readable, clickable or correctly disabled, clipped-free, and functionally usable in both sizes before UTS handoff
- default-versus-compact proof cannot be cleared by source inspection, CSS inspection, marker proof, screenshot existence, or a single-window sample; missing compact/default photos, missing comparison data, unreadable text, clipped controls, unavailable scrolling, unclickable actions, hidden required rows, or a child window that cannot complete its core workflow in either size is a Live Validation `REPAIR`
- every user-facing visible or interactive option in the active surface must have live-client proof for default state, hover/focus or equivalent affordance state, pressed/click transition, resulting state change, and guard/close/save/discard/delete/dropdown/list behavior where applicable; this includes disabled controls proving they are intentionally disabled and visually understandable
- creation workflows are mandatory live-validation scenarios: creating any user-owned entity, profile, monitor, source mapping, preset, configuration object, or comparable item must prove that the new item is draft-only until the user chooses `Save` or the approved equivalent, starts from an intentionally empty/default-safe configuration rather than silently inheriting unrelated selections, triggers dirty-change guardrails on close/navigation/selection changes, can be discarded without persisted residue, and only persists after a successful save path; any auto-persisting creation path without explicit source-truth admission is a Live Validation `REPAIR`
- child-window and nested-window workflows are mandatory live-validation scenarios: every Dashboard child window and nested surface must prove close, save, discard, delete, selection change, dropdown/list open, null state, stressed/high-volume state, compact-size state, and default-size state through visible user-path interactions; required controls and action rows must remain reachable, clickable or intentionally disabled, unclipped, scrollable where needed, and readable at compact and default sizes
- live validation must prove modal/child-window input isolation: pointer, click, hover, focus, keyboard, and dropdown interactions inside a child window must not activate Dashboard controls or surfaces behind it; click-through, focus-through, accidental close, or background-state mutation from a foreground child-window interaction is a Live Validation `REPAIR`
- live validation must include scenario coverage, not just element coverage: for each user-facing window, Codex must enumerate and exercise the plausible USER journeys available in that window, including create -> dirty -> close guard -> save/discard, select existing -> edit -> save/discard, delete -> confirmation/cancel/confirm, dropdown open -> select -> close, null data, high-volume data, compact/default resizing, and disabled/deferred paths where applicable; if a journey is not applicable, the digest must say why
- scenario discovery must be adversarial and exhaustive within the approved surface: Codex must actively look for any and all reasonable user actions, wrong-order actions, repeated clicks, rapid state changes, resize-while-open cases, close/back/navigation attempts, empty-state paths, stress-volume paths, and nested-window interactions that a USER might try; validation that only follows the happy path, only proves one size, only proves one data volume, or omits an available visible control is a Live Validation `REPAIR`
- real user-path interaction is mandatory wherever feasible, using visible desktop launcher/client state plus real OS-level mouse/keyboard input to the same screen coordinates a USER would use instead of direct handler calls; Codex must exhaust feasible real-input routes before using any replacement proof, and replacement proof is exceptional rather than normal-course validation. If any element or scenario cannot be exercised with real OS-level input after those attempts, the Live Validation digest must list the exact element/scenario, attempted real-input routes, why each route was not feasible, what replacement proof was used, what was not proven, and the exact manual USER scrutiny requested. Any unattempted feasible real-input route or vague fallback rationale is a Live Validation `REPAIR`.
- for clickable desktop UI controls, `mouse/cursor or UIAutomation-backed interaction evidence` means the LV1 helper must visibly move the real Windows cursor to the control's screen coordinates, send OS-level mouse down/up input, and then inspect the resulting state. direct JavaScript `.click()`, synthetic DOM events, WebView callbacks that invoke handlers, direct handler calls, state mutation, marker toggles, QTest widget-only events, or anything previously labeled `diagnostic-only` are banned from Live Validation phase interaction testing and may not be present in the active LV1 interaction route. The Live Validation helper must run a no-synthetic-interaction preflight before launch; if the active LV1 interaction route contains synthetic/widget/direct-handler interaction code, the helper must stop on Live Validation `REPAIR` before executing the test. Any Live Validation manifest that treats JS/DOM/synthetic/widget-only actions as proof for a feasible user-clickable control is invalid.
- Live Validation helpers must contain hard blockers that prevent editing the active LV route away from real user-level input. If a real cursor/click/keyboard path fails, Codex must diagnose it first as a possible runtime/user-visible defect, inspect hit targets, z-order, focus, scroll reachability, resize bounds, disabled state, event propagation, native hit testing, and resulting state, then repair the product when the evidence points to product behavior. Changing the validator to use direct JavaScript, synthetic events, handler calls, state mutation, or widget-only input to make the same element green is forbidden unless every feasible real-input route has been attempted, the failure is proven not to be product/runtime behavior, the exact unproven scenario is documented, and USER grants an explicit temporary waiver.
- Live Validation fallback is not a normal path. A fallback request must be a `STOP`/`REPAIR` digest item naming the element, scenario, failed real-input attempts, diagnostic evidence, why the real path cannot proceed, the proposed temporary replacement proof, what the replacement proof cannot prove, and the manual USER scrutiny required. Vague claims such as `automation limitation`, `environment issue`, `code inspection sufficient`, or `synthetic path equivalent` are invalid.
- Live Validation must remain branch-adaptive and cumulative: every branch must rerun the previously required user-facing proof for the affected surface and add focused scenarios for newly created or modified elements, states, data volumes, windows, and workflows. New branch work cannot replace prior branch proof; it extends the regression matrix so drift, regressions, visual clipping, state leakage, and user-path bugs are discovered before UTS.
- Live Validation must prove null, normal, and stressed data states for every dropdown, scrollable selection area, list, picker, card collection, profile/entity selector, and similar multi-choice surface touched by the branch. Stressed proof must use high-volume data appropriate to the feature vision, compact and default window sizes, focused screenshots before and after interaction, and real input for open/hover/select/scroll/close paths.
- Live Validation must exercise combinatorial user paths for active windows and child windows, including compact/default size plus dirty guard, Compact Overlay Profiles delete confirmation, dropdown-open, nested child-window, close/cancel/save/discard, resize-while-open, and background click-through states. A green result for a base window state does not imply green for a child confirmation, dropdown, dirty guard, or compact nested state; each reachable combination must be explicitly proven or explicitly waived.
- The expected USER handoff quality bar is that UTS should not uncover more than one or two non-obscure defects. If returned UTS exposes repeated obvious visual, interaction, compact-size, or workflow failures, Live Validation governance and validators must be treated as defective and repaired before another UTS handoff.
- returned USER UTS or screenshot/video issues must be preserved in a temporary issue form until PR Readiness Stage 1 folds the resolved truth into the active authority, branch plan, backlog, roadmap, validators, and release-scope handoff; the issue form must list the issue, planned repair/disposition, expected proof, validation artifact path, per-element screenshot/video requirement, and USER-verifiable status
- the LV1 manifest must enumerate the USER-inspectable per-element screenshot folder, every per-element screenshot path, the per-element visual inventory, any issue-form IDs covered by each artifact, and a PASS / REPAIR / STOP / WAIVED_WITH_REASON verdict for each element; missing inventory rows, missing element labels, missing issue-form coverage, missing OneDrive copies, screenshots stored only under `dev\logs`, or only full-desktop screenshots must return `REPAIR` before UTS handoff
- platform uniformity is reviewed across current NDAI naming, visual language, copy tone, and surrounding user-facing surfaces touched by the branch
- validators, markers, screenshots, and manifests are treated as supporting evidence, not a replacement for Codex's visual/usability judgment
- Codex must perform pessimistic visual adjudication after every desktop UI Live Validation run and before any UTS handoff claim: assume the validator missed a defect until Codex has opened and inspected the focused screenshots and short video/frame-sequence artifacts itself. The digest must name any Codex-visible visual, interaction, workflow, compact/default, scroll, clipping, alignment, readability, state, or hierarchy concern even when every helper reports `PASS`.
- A helper/validator `PASS` cannot be reported as LV green until Codex has independently reviewed the produced images, compared normal and compact states, checked child-window/confirmation/dropdown combinations, and either records no visible concerns or routes every concern to `REPAIR`, `STOP`, or an explicit USER waiver. Any final packet that says `green` while Codex has not inspected the artifacts is invalid.
- Verbal assurance, implementation description, or intent-language is not proof. If Codex says a UI pattern is implemented, the same turn must either cite the focused screenshot/video artifact that visibly proves the delivered UI matches that description or report `REPAIR`/`BLOCKED`; a mismatch between described behavior and live-client appearance is a Live Validation failure.
- Live Validation closeout must include Codex-owned photo review notes, not just helper status: the notes must identify the artifact folder, the specific screenshots reviewed, the expected UI state for each reviewed artifact, the observed UI state, and any mismatch disposition. Missing photo-review notes, or notes that only restate validator output without visual scrutiny, are `REPAIR`.
- Dirty-change safeguards for user-facing desktop HUD windows must use one shared modal standard wherever a dirty guard is required: the guard must be a direct modal layer owned by the active child window, dim/blur/block the underlying window, hide the normal close control while open, present `Save`, `Discard`, and `Cancel` actions in that order, and stay out of normal form/list/detail layout so it cannot compress, overlap, or scroll as ordinary content. `Save` must persist the draft and continue the queued close/state-change, `Discard` must drop the draft and continue the queued close/state-change, and `Cancel` must interrupt the queued close/state-change without saving or discarding, remove the modal, unsuppress the window, and return the USER to the same window with the same unsaved dirty draft still present. Any branch adding or changing a dirty guard must prove this same format across every affected window with focused screenshots and real user-level input.
- desktop UI Live Validation must include a failure-seeking visual adjudication pass before UTS handoff; Codex must inspect the focused proof images one by one, compare them against the Product Definition Plan, Runtime Branch Engineering Contract, latest USER vision/UTS feedback, active temporary issue form, and package-level UI/UX intent, and record artifact-by-artifact `PASS`, `REPAIR`, `STOP`, or `WAIVED_WITH_REASON` verdicts for all inventoried elements/states
- helper PASS, marker PASS, screenshot existence, manifest existence, or USER execution waiver cannot clear visual acceptability; clipped text, unclear workflow hierarchy, weak hover/click affordance, non-uniform button glow/color, non-uniform divider/page-break haze, background bleed-through, scrollbar mismatch, missing open/disabled/danger/empty/error proof, native/basic controls where Nexus styling is required, or package-vision mismatch must route LV1 back to Workstream or Hardening before USER handoff unless USER gives an explicit visual waiver with reason
- desktop UI Live Validation owns the defect-discovery burden before UTS: Codex must not return a User Test Summary handoff while any unwaived Codex-visible `REPAIR` or `STOP` finding remains in the per-element visual inventory, issue-form coverage matrix, interaction proof, or visual adjudication record
- if Live Validation discovers a current-branch UI/UX/interaction defect and current approval covers bounded continuation, Codex must enter the bounded repair/rerun loop automatically: record the finding, patch the approved surface, rerun focused proof, rerun required validation, update source truth, and only then regenerate the UTS handoff; if approval does not cover the repair, Codex must return `BLOCKED` or `REPAIR` with the exact approval needed rather than asking the USER to find the same defect manually
- the UTS handoff is a USER acceptance review, not a substitute for Codex visual QA; a Live Validation packet that relies on the USER to enumerate obvious clipped, misaligned, flickering, unresponsive, non-uniform, or unusable elements is not green

Routing:

- while `Codex Live Client Self-QA: PENDING` remains, list `Codex Live Client Self-QA Pending` under blockers and do not hand off the User Test Summary as ready
- if `Codex Live Client Self-QA: FAIL`, keep an explicit blocker and route back to `Workstream` or `Hardening` before USER handoff or PR Readiness
- if `Codex Live Client Self-QA: PASS` is recorded, the USER Test Summary handoff may proceed only if the shortcut/equivalent entrypoint gate and all other Live Validation gates are green
- `Codex Live Client Self-QA: WAIVED` requires explicit waiver reason and is valid only when the branch is not user-facing or the live client path is unavailable

### User Test Summary Results Gate

Live Validation Stage 1 must not enter Live Validation Stage 2 while a relevant user-facing workstream has a required User Test Summary handoff outstanding and returned results have not been submitted and digested.
User Test Summary is exclusive to Live Validation Stage 1.
Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.
PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact.
Live Validation green requires an exact `## User Test Summary` state before final green.
Every Live Validation digest must include an exact `## User Test Summary` section. If User Test Summary is waived, that digest section must still declare `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`; validation summaries, blocker summaries, and source-truth references do not replace the digest section.
This is a `Live Validation Stage 1` gate, not a Workstream, Hardening, or PR Readiness completion substitute.
Workstream and Hardening may maintain UTS strategy or readiness notes, but they must not create/refresh the formal desktop UTS export, create a UTS results seam, digest UTS results, or stop on `User Test Summary Results Pending`.

Named blocker:

- `User Test Summary Results Pending`

Required status model:

- Automated validators and live helper evidence: GREEN.
- User Test Summary Results: PENDING.
- Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.

Machine-checkable authority-record markers:

- the active authority record must include an exact `## User Test Summary` section; `## User Test Summary Strategy` is planning context and is not the canonical `UTS` artifact
- while pending, the active authority record must include `User Test Summary Results: PENDING`
- while pending, the active authority record must list `User Test Summary Results Pending` under `## Blockers`
- while pending, `## Next Legal Phase` must not advance beyond the current phase
- when passing returned results are digested, the active authority record must include `User Test Summary Results: PASS` and a digest of the returned results before the blocker can clear
- when a waiver is used, the active authority record must include `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:` before the blocker can clear
- when returned results fail or expose ambiguity, the active authority record must keep or replace the blocker with the appropriate Workstream or Hardening blocker and route backward rather than advancing

Lift condition:

- a filled User Test Summary is submitted or a documented waiver exists
- the results or waiver are digested into the active authority record
- the blocker state is reevaluated after digestion

Routing after digestion:

- if returned results pass, `User Test Summary Results Pending` clears and forward progression may continue if all other gates pass
- if returned results expose mismatch, regression, unclear behavior, cleanup failure, or scope drift, route back to `Workstream` or `Hardening` as appropriate
- if returned results raise new feature ideas, keep them out of current scope until backlog carry-forward is explicitly approved

### Release Readiness Candidate Anchor Rule

Release Readiness must validate the selected release candidate, not re-open historical PR endpoint cleanup by default.

Every Release Readiness packet must declare:

- `Release Candidate Anchor:`
- `Release Candidate Anchor Source:`
- `Target Commit:`
- `Historical Endpoint Handling:`
- `Candidate Includes Later Governance Repairs:`
- `Release Window Contributor Inventory:`

Default anchor rule:

- unless USER explicitly selects another release target, `Release Candidate Anchor:` is current fetched `origin/main`
- `Target Commit:` is the current fetched `origin/main` SHA for the repository being released
- later governance/source-truth repair PRs already merged into the selected candidate are part of candidate truth
- a release candidate may include governance/source-truth-only repair PRs after the last runtime PR; those PRs do not disqualify the candidate or force the release target back to the last runtime merge commit
- `Candidate Includes Later Governance Repairs:` must be `YES` when the selected candidate contains governance/source-truth repair PRs after the runtime PR that carried the user-facing release payload, and the release notes may keep those repairs in internal validation/traceability instead of presenting them as user-facing product features
- historical PR merge commits may be inspected as audit evidence, but they do not become the release-validation base unless USER explicitly selects that historical commit as the release target
- if USER selects a historical PR merge commit as the release target, Release Readiness must label `Release Candidate Anchor Source:` as `USER-selected historical commit` and must verify that commit's source truth without silently mixing later `origin/main` repairs

### Release Window Aggregation Ownership

A release is owned by the selected release candidate window, not by whichever implementation PR or worktree merged last.

Every release-bearing candidate must declare:

- `Release Ownership Model:`
- `Release Window Contributors:`
- `Merged-Unreleased Scope Inventory:`
- `Last Runtime PR:`
- `Post-Runtime Governance Repairs:`
- `FAM Contributor Routing:`

Aggregation rule:

- when multiple FAM/worktree branches merge before the next public prerelease, the selected release candidate must inventory every merged-unreleased contributor included in the target commit
- merge order does not determine release ownership; the release owner is `Release Ownership Model: Aggregated release window` unless USER explicitly opens a release packaging branch or selects a narrower historical/release-branch target
- if current fetched `origin/main` contains both FAM-006 and FAM-007 merged-unreleased scope, both scopes are in the release candidate and both must have release-debt, validation, and issue/posture truth before Release Readiness can be green
- if one merged contributor is not release-ready, Release Readiness must block or USER must explicitly select a release target that excludes it, such as a historical commit or release branch; Release Readiness must not silently pretend the contributor is outside the candidate
- governance/source-truth-only PRs after runtime payload PRs are recorded under `Post-Runtime Governance Repairs:` and may be included without becoming user-facing feature claims
- after release publication, durable post-release closure must clear or move every included `Merged-Unreleased Scope Inventory:` item, not just the last merged branch

The blocker for missing or ambiguous contributor inventory is `Release Window Contributor Inventory Missing`.

Post-release closure rule:

- once a public prerelease tag exists, no current-state owner, compact pointer row, canonical detail branch record, retired branch plan, worktree slot receipt, or family vision pointer may keep that published release window's included scope as current `merged-unreleased` posture
- validation must derive the included release window from Git/GitHub/tag truth and first-parent PR/merge commits, resolving prerelease tags to explicit commit IDs or paginated GitHub compare truth before building the scan range so remote-only tag discovery cannot fall back to a tag-text-only check; when the previous prerelease commit is unavailable, validation must use paginated compare truth rather than widening to a full-history scan, then scan release-window branch records, branch plans, retirement rows, and compact pointers by release tag, PR number, merge commit, and branch identity
- included scope must be folded to released/closed or explicitly labeled as historical pre-release snapshot evidence that is not current posture
- Release Readiness must stop on `Post-Release Canon Closure Drift` when the selected candidate has already been published but source truth still describes an included contributor as merged-unreleased for that published tag
- the standing Governance intake lane is the legal carrier for post-release source-truth/governance drift discovered after publication; Release Readiness remains file-frozen and must not patch the drift directly

Scope routing:

- if the selected release candidate is current `origin/main`, stale wording at an older PR endpoint is historical PR Readiness miss evidence, not a current Release Readiness blocker when later merged governance/source-truth repairs fixed the selected candidate
- if the selected release candidate still lacks release target, release floor, release debt, merged-unreleased, contributor inventory, or issue-posture truth, Release Readiness stops and emits a blocker digest only
- if the branch has not merged, the repair routes back to `PR Readiness`
- if the branch has already merged, the repair routes to the next legitimate runtime-focused backlog branch's `Branch Readiness` or to the single standing governance intake lane when the blocker is a Release Readiness source-truth/governance drift digest

The blocker for missing or ambiguous anchor data is `Release Candidate Anchor Missing`.

### Release Readiness Target Gate

Release Readiness must not report green while any release target blocker remains unresolved.

Release Readiness is an analysis-only file-freeze phase. Required release target, scope, artifact truth, and release-candidate anchor truth must already exist before entering Release Readiness, normally as PR-owned merge-target canon or a PR-ready response package. If Release Readiness analysis discovers that those fields are missing, ambiguous, stale, or require source-file changes, do not patch files inside Release Readiness. Return the active branch to `PR Readiness` if it has not merged; if the branch has already merged, defer the repair to the next legitimate runtime-focused backlog branch's `Branch Readiness` or the standing governance intake lane when the issue is Release Readiness source-truth/governance drift.

Hard blocker:

- `Release Target Undefined`:
  Release Readiness fails for a release-bearing branch unless the active branch authority record or active workstream authority record explicitly identifies all required release-bearing markers:
  - `Release Target:`
  - `Release Floor:`
  - `Version Rationale:`
  - `Release Scope:`
  - `Release Artifacts:`

  The target must also be semantically correct from the latest public prerelease and declared release floor; marker presence alone is not enough.

A branch is release-bearing when:

- its branch class is `release packaging`
- or it creates, prepares, validates, tags, publishes, or transitions release-facing artifacts or release-state canon

Small single-seam runtime proof that merges inside an existing family may be marked as aggregation evidence instead of a standalone release driver when the USER has not approved it as a release-version driver.
That record must declare the proof as `Standalone Release Driver: No` or equivalent aggregation-hold truth and identify the larger USER-approved family release or future aggregation target when one exists.
Such aggregation-hold evidence does not by itself justify a new release version, selected-next lane, or release packaging branch.

The only non-release waiver is:

- the active authority record explicitly declares `Release Branch: No`
- the record is preserved historical truth
- the branch does not create, prepare, validate, tag, publish, or transition release-facing artifacts or release-state canon

The non-release waiver is not available to `implementation` or `release packaging` branches.
It does not waive `Release Debt`, merge-target canon completeness, post-merge truth, successor lock, validation, or dirty-branch requirements.

If release target markers are missing on a release-bearing branch, the branch is blocked by `Release Target Undefined`.
If `Release Branch: No` appears outside a preserved historical record, the branch is blocked by `Phase Waiver Missing`.
If any source, docs, canon, validator, helper, or release-note file is modified while the active phase remains `Release Readiness`, the branch is blocked by `Release Readiness File Mutation Attempt` and must return to `PR Readiness` or defer to the next legitimate runtime-focused backlog branch's `Branch Readiness` before the change can be made.

### Release Readiness Scope Boundary

Release Readiness is not a docs-sync phase. It is also not a file-mutation phase.

Release Readiness is analysis-only for repository files:

- it may inspect repo truth, branches, tags, releases, validator output, and release evidence
- it may produce release package information in the response, including tag, title, release notes, and release-execution instructions
- it may run validation commands that do not mutate tracked source files
- it must not edit, stage, commit, generate, or refresh source, docs, canon, validator, helper, release-note, or desktop handoff files

Release Readiness may read External Governance State only after USER-approved initialization. Repo-file validation in GitHub Actions or clean clones must not require `C:\Nexus Governance State`; those environments validate durable repo truth only. If external state is missing during active local Release Readiness analysis, Codex reports `External State Missing` and returns the bootstrap packet from `Docs/governance_efficiency_operating_model.md` instead of inferring active branch, selected-next, worktree assignment, release-window, or watcher state from stale repo docs.

External state mutation during Release Readiness remains blocked unless USER explicitly approves a local operational-state reconciliation, except for bounded RR2 post-release external state carry-forward reconciliation after release publication and green post-publish release/tag/body/health validation. Even when allowed, that mutation is limited to external operational release-window state, external acknowledgement state, external promotion/recovery packets, or external carry-forward records under `C:\Nexus Governance State`; it must not edit repo files, create release artifacts, create branches or PRs, merge, release again, clean branches or worktrees, or touch FAM/runtime/private/provider/cache/memory surfaces.

Allowed in `Release Readiness`:

- release-candidate anchor validation
- release-target validation
- release-scope validation
- release-artifact validation
- GitHub release package information such as tag, title, and release notes
- final release-execution authorization or confirmation
- release-state confirmation after the release execution

Forbidden in `Release Readiness`:

- treating a historical PR endpoint as the release base without explicit USER-selected historical commit approval
- broad canon or docs sync that should have been completed in `PR Readiness`
- branch-authority cleanup that should have been merge-safe before PR green
- next-workstream selection, planning, or branch creation
- between-branch canon repair
- any source, docs, canon, validator, helper, release-note, or handoff-file mutation
- any direct write to protected `main`

### Release Readiness Operator Output Contract

When `Release Readiness` is green for release execution, the response must include markdown-friendly release operator copy blocks for direct GitHub release use.

Required release operator copy blocks:

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

Each release operator field must be its own copy-ready block and must be usable independently.
Release notes must be detailed, descriptive, and user-facing.
They must clearly explain what was built, what capabilities exist, and how the system behaves.
Release notes must follow the operator output content rule: report included work only, with no exclusion lists, `Not Included` sections, negative scope framing, or defensive wording.
The live GitHub release body must use the standard Markdown release body shape:

- `## Release Summary` or `## Release Overview`
- `## Release Highlights` or release-specific rich sections
- `## What's Changed`
- `**Full Changelog**:`

The live release body must not start with or repeat the release title as `# <release title>`. Keep the public title in GitHub release metadata and the separate `Release Title` operator block; keep milestone names, scope, behavior, capabilities, validation, and next-step context inside the Markdown body.
Public GitHub release bodies must be user-facing and must not include internal automation/tooling brand tokens, generated branch-prefix noise, phase-handoff text, operator transcript text, release-candidate anchor hashes, or internal source-truth/release-readiness governance phrasing. If GitHub-generated notes include `[codex]`, `codex/...`, `Release candidate anchor:`, `source-truth governance`, `governance/source-truth`, `release-readiness governance`, or equivalent internal tooling/phase labels, Release Execution must rewrite those line labels into neutral user-facing PR names before publication or repair the release body immediately after publication.
All published Nexus pre-Beta release bodies remain part of the live public release surface. Historical public prereleases must continue to satisfy the same release-body standard unless a release is explicitly legacy-scoped outside the Nexus pre-Beta line.
The `## What's Changed` section and `**Full Changelog**:` compare link must be populated by GitHub-generated release notes, using the GitHub release notes button or the generated-release-notes API with the previous release selected. Release Readiness may prepare the human-written summary and highlights, but Release Execution must combine them with the GitHub-generated notes before publication or repair the release body immediately after publication.

If Release Readiness discovers missing PR-owned canon or docs work, stop immediately and classify the issue as `PR Readiness Scope Missed` and `Release Readiness Scope Drift`.
If the branch has not merged, return to `PR Readiness` and repair the miss there before any Release Readiness output can be treated as green.
If the branch has already merged, the next legitimate runtime-focused backlog branch's `Branch Readiness` or the standing governance intake lane must repair the miss before implementation begins and must update governance or validator coverage so the miss cannot recur.

### Release Window Audit

Inside `PR Readiness`, any branch that is preparing, repairing, or validating truth inside an unreleased release window must run a formal `Release Window Audit` before it may report PR green.

The audit must explicitly answer:

- `Release Window Audit: PASS`
- `Window Scope`
- `Known Window Blockers Reviewed`
- `Remaining Known Release Blockers`
- `Another Pre-Release Repair PR Required`
- `Release Window Split Waiver`

Normal green posture is:

- `Remaining Known Release Blockers: None`
- `Another Pre-Release Repair PR Required: NO`
- `Release Window Split Waiver: None`

If the branch already knows another blocker-clearing PR will be required before release, do not call PR Readiness green by default.
The only allowed exception is an explicit user-approved split:

- `Release Window Split Waiver: APPROVED`
- `Release Window Split Waiver Reason: <why the split is intentional>`
- `Another Pre-Release Repair PR Required: YES`

Without that explicit split waiver, the branch is blocked by `Release Window Audit Incomplete`.
This rule exists to prevent serial blocker-clearing PR chains inside one unreleased window when one repair branch could have cleared the full currently known blocker set.

### Governance Drift Audit

Inside `PR Readiness`, the branch must run a formal Governance Drift Audit before it may advance to `Release Readiness`.

The audit must explicitly answer:

- `Governance Drift Found: Yes/No`
- `Drift Type`
- `Why Current Canon Failed To Prevent It`
- `Required Canon Changes`
- `Whether The Drift Blocks Merge`
- `Whether User Confirmation Is Required`

The audit must explicitly check whether the branch exposed:

- a missing blocker
- a weak phase entry or exit rule
- a weak source-of-truth ownership rule
- stale prompt scaffolding or stale operator examples
- a missing validator requirement
- a serial release-window repair pattern that should be consolidated onto the current branch instead of landing as another pre-release PR
- a repeated or carried blocker class whose repair must include recurrence analysis before green

If governance drift is found and unresolved, the branch is blocked by `Governance Drift`.

### External Operational State Transition Gate

Inside `PR Readiness`, any branch that changes the External Operational State Store contract, Docs split plan, live-state ownership, external-state schema, helper/bootstrap posture, validator transition, repo live-state leakage policy, review-bundle state ownership, or active-state migration plan must run a formal `External State Transition Gate` before Stage 2 / PR creation can be green.

The gate must explicitly answer:

- `External State Transition Gate: PASS / BLOCKED / USER Decision Required`
- `Transition Stage`
- `Docs Split Target Matrix Status`
- `Active-State Owner Boundary`
- `External Root Approval`
- `External Root Status`
- `Premature Migration Scan`
- `Repo Live-State Leakage Scan`
- `Validator / Helper Transition Status`
- `Source-Truth Agreement`
- `Next Approved Step`
- `Remaining USER Decisions`

Stage 0 is docs/source-truth planning only. It does not approve helper code, validator code, `C:\Nexus Governance State` creation, worktree-local staging, state migration, repo file movement, deletion, archival, or release execution. Stage 1 is helper/bootstrap scaffolding and validation planning only; helpers may exist and run report/dry-run checks, but applied mutation remains blocked without later USER approval. Stage 2 is local root initialization only. Stage 3 is migration planning and no-mutation preview packets only. Stage 4A is report-only repo live-state leakage scanning and migration-map helper support only. Stage 4B is active-state migration planning packet only; it may convert scanner output into a USER-reviewable migration plan, but it must not migrate active state, create central branch/worktree/release-window records, move/delete/archive repo docs, transition validators, or require external state in clean-clone validation. Stage 4C is active-state migration execution planning packet only; it may define the exact future execution preflight, external target records, durable receipt preservation, rollback/recovery plan, and USER review question, but it must not run helper `--apply` operations, write central external records, create worktree-local staging, migrate active state, move/delete/archive repo docs, transition validators, or require external state in clean-clone validation. Stage 4 is USER-approved active-state migration execution and may create or update only approved local external operational records, locks, snapshots, and audit logs; it must not move, delete, archive, or rewrite repo Docs and must not mutate FAM worktrees. Stage 5 is validator transition: local external-state validation may require the initialized root and migrated record set for approved local workflows, while GitHub Actions and clean-clone repo validators must remain independent from `C:\Nexus Governance State`. Stage 6 is repo cleanup planning: it may classify cleanup lanes, candidate surfaces, replacement owners, and future execution packets, but it must not edit, move, delete, archive, rename, collapse, or rewrite repo Docs. Stage 6A is compact pointer-surface cleanup execution: it may edit only `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, and `Docs/worktree_slots.md` to remove live operational posture and route it to Git/GitHub/helpers or `C:\Nexus Governance State`; it must not edit branch records, branch plans, workstreams, family visions, generated audits, move/delete/archive files, mutate FAM worktrees, or create worktree-local staging. Stage 6B is branch-authority routing cleanup planning: it may plan how `Docs/branch_records/index.md` keeps durable routing law and standing Governance authority while non-standing active operational branch authority moves external, but it must not edit the index or any branch record yet. Stage 6C is branch-authority routing cleanup execution: it may edit only `Docs/branch_records/index.md` plus stage-boundary source truth so the index keeps durable branch-record law, historical receipt routing, and the single standing Governance active exception while non-standing active operational branch authority routes to external state; it must not edit branch detail records, branch plans, workstreams, family visions, generated audits, move/delete/archive files, mutate FAM worktrees, create worktree-local staging, or make external state mandatory for clean-clone repo validation. Stage 6D is branch-detail-record / branch-plan cleanup planning: it may define future cleanup batches, exact candidate classes, durable receipt preservation rules, external replacement owners, and validation preflight for branch records and branch plans, but it must not edit branch detail records, branch plans, generated audits, move/delete/archive files, create worktree-local staging, mutate FAM worktrees, or make external state mandatory for clean-clone repo validation. Stage 6E is no-loss cleanup closure: it may record that branch records and branch plans remain durable receipts or transition owners when report-only scanners show zero blocking leakage, and that broad branch-record / branch-plan rewrites would create receipt-loss risk. It must not edit branch detail records or branch plans except the standing Governance intake record, move/delete/archive repo files, create worktree-local staging, mutate FAM worktrees, or make external state mandatory for clean-clone repo validation. Repo file movement, deletion, archival, broader repo cleanup execution, worktree-local staging, and release execution remain blocked until USER approves those later stages. During Stage 0 through Stage 4C, repo branch records and branch plans remain legal current owners where current governance still requires them. During Stage 5, Stage 6 planning, Stage 6A compact pointer cleanup, Stage 6B branch-authority planning, Stage 6C branch-authority routing cleanup, Stage 6D branch-detail-record / branch-plan cleanup planning, and Stage 6E no-loss cleanup closure, they remain durable transition owners or historical receipts unless a later USER-approved exact cleanup or fold-down execution stage proves no-loss replacement.

If the gate is missing or source truth disagrees on the current transition stage, active-state owner, helper/bootstrap approval, external root status, migration status, or next legal step, the branch is blocked by `External State Transition Gate Missing` or `External State Transition Drift`.

If the external-state plan lacks a current Docs Split Target Matrix, the branch is blocked by `Docs Split Target Matrix Missing`.

If a branch treats external-state helper/bootstrap/root/migration work as approved, initialized, or required before USER has approved that stage, the branch is blocked by `External State Migration Premature`.

Repo validators running in GitHub Actions or clean clones must not require `C:\Nexus Governance State`. Local governance workflows may require external state only after USER-approved initialization or an explicit local analysis/migration/validator-transition approval, and those checks must report `External State Missing`, `External State Version Conflict`, `External State Schema Conflict`, or `Stale Lock Recovery Required` instead of inferring state from stale repo Docs.

### Governance Drift Escalation Rule

If governance drift is discovered in any earlier phase:

- stop normal progression immediately
- classify it as `Governance Drift`
- fix it on the active branch when the drift is tightly coupled to that branch's truth, phase, readiness, validation, closeout, or release state, or
- produce the exact required canon delta and wait for user confirmation when the repair would exceed the active branch boundary

Do not defer known governance weaknesses silently to a later branch.

Repeated or carried blockers must not be closed by surface cleanup alone.
Before the branch can report green, record what failed, why current governance or validation missed it, what prevents recurrence, and whether canon or validator coverage changed or was explicitly judged sufficient.

### Manual Evidence And Review Digestion Rule

Returned evidence such as:

- `UTS`
- screenshots
- interactive reports
- PR review comments
- release review findings

may satisfy exit criteria, but must never auto-advance phase by implication.

Required sequence:

1. digest the evidence
2. update the authority record
3. reevaluate blockers
4. only then advance phase

### Current-State Claim Containment

Time-sensitive current-state claims must live only in designated operational owners outside repo durable source truth, or be derived from Git/GitHub/helpers at the time of inspection.

After the External Operational State Store contract is implemented, live operational state that exists only to coordinate active branches, PRs, worktrees, release windows, review bundles, watchers, selected-next posture, or temporary handoffs must not be reintroduced into repo docs as current truth. Repo docs may preserve durable branch/document evidence pointers and historical receipts, but they must not own lifecycle posture such as active, complete, pending, no branch created, no live PR, PR creation pending, Stage 2 pending, selected-next current state, release-window ownership, or worktree assignment. If Release Readiness finds that state in repo docs, classify it as `Repo Live-State Leakage` unless it is clearly labeled historical receipt evidence.

Repo docs are index/context files for operational work. They may point to the branch, PR, release, external-state record, workstream, family vision, validator, helper, or receipt that owns detail, but they must not maintain the operational ledger itself. Branch plans, UFD rows, Branch Change Intent rows, Element-to-Phase rows, Workstream Entry review packets, Hardening plans, Live Validation plans, PR watcher state, release-window assembly, and review-bundle manifests belong outside repo docs while active unless USER grants an explicit transition exception.

Allowed operational-state owners after the external-state transition:

- `C:\Nexus Governance State` for accepted local operational state
- `<worktree>\.nexus_state_staging\` for proposed state only after USER approval
- Git/GitHub/helper-derived live truth for branch, PR, release, issue, review-thread, and dirty-state facts
- repo docs only for durable rules, durable vision, branch/document evidence pointers, and historical receipts

Repo durable docs should be timeless or historical by default.
If they contain live-current claims, they must either:

- be converted to historical receipt evidence,
- be replaced with a durable pointer to the external/derived owner, or
- be removed from repo ownership through a USER-approved cleanup or fold-down repair.

### Governance Validator

Repo-wide governance changes should be checked with the machine-readable governance validator:

- `python dev/orin_branch_governance_validation.py`

That validator should verify at minimum:

- the exact phase enum only
- active prompt scaffolds no longer teach deprecated phase names or stale prompt contracts
- active promoted workstreams carry the required phase-state block
- phase values and branch-class values are valid
- backlog, roadmap, workstreams index, and active workstream docs agree on active or merged-unreleased posture
- stale merge-era wording does not remain in active current-state owners
- Governance Drift Audit output exists before `Release Readiness`
- release-bearing branches carry `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:` markers before Release Readiness can report green
- release-target semantics match the latest public prerelease and declared release floor before PR Readiness or Release Readiness can report green
- Release Readiness is analysis-only and cannot mutate files; dirty tracked files while the authority record says `Release Readiness` are a `Release Readiness File Mutation Attempt`
- non-release waiver records use `Release Branch: No` only for preserved historical records
- unresolved blockers prevent phase advancement
- active-branch governance and canon updates remain the primary path when tightly coupled to the active branch's truth, phase, readiness, validation, closeout, or release state
- governance-only branches are not used for new Nexus work, and between-branch canon repair attempts are blocked
- Release Readiness cannot absorb PR Readiness docs sync or canon repair
- prior-branch canon misses block the next legitimate runtime-focused backlog branch in Branch Readiness before implementation can begin
- the canonical `bounded multi-seam workflow` contract is present in governance and operator scaffolds
- prompt scaffolds teach `Seam Sequence`, per-seam validation, and continue-or-stop decisions for multi-seam Workstream execution
- docs do not teach direct `Workstream` -> `PR Readiness` as the default path
- PR Readiness prompt scaffolds require inclusion-only `## PR Creation Details` operator copy blocks before reporting PR green, and require the standardized `## Next Branch` block only when selected-next truth is explicitly in scope or Branch Readiness is the next legal phase
- Release Readiness prompt scaffolds require inclusion-only `## Release Package Details` operator copy blocks when release execution is green

A governance or current-state canon branch is not complete until that validator is green.

When branch authority records are active, the validator should also verify:

- `Docs/branch_records/index.md` exists and routes to the active branch authority records
- active branch authority records carry the required phase-state block
- `No Active Branch` blocked-versus-steady-state handling stays consistent across the governance and operator docs
- new governance-only branches remain blocked during `pre-Beta`; historical `docs/governance` records are allowed only as preserved history

### Phase Resolver Contract

Before any answer about current phase or next move, run this resolver:

1. validate live repo truth
2. determine whether there is an active executable branch, a blocked `No Active Branch`, or a steady-state `No Active Branch`
3. identify the active workstream authority record or branch authority record
4. detect blockers first
5. read the exact `Current Phase`
6. validate entry basis and exit criteria against live truth
7. return only the next legal phase, or no phase if blocked

Required output for any â€œwhat phase are we in?â€ or â€œwhatâ€™s next?â€ answer:

- `Current Phase`
- `Phase Status`
- `Branch Class`
- `Blockers`
- `Governance Drift Found`
- `Next Legal Phase`
- `Plan To Reach That Phase`

Every phase digest must include `Next Legal Phase` as its own output field, even when `Continue Decision: Continue`; `Next Safe Move` may remain lawful-stop or route-specific and must not replace required continuation.
Formal Next Legal Phase Digest is required whenever a phase packet stops for USER approval. The response must include a `Next Legal Phase Digest` with `Current Phase:`, `Next Legal Phase:`, `Why This Phase Is Next:`, `Approval Required:`, `Exact USER Approval Text:`, `Allowed Scope:`, `Explicit Exclusions:`, `Validation Required:`, `Stop Conditions:`, `USER Plan Review Gate:`, `USER Inspection Files:`, `Review Required Because:`, `Implementation Blocker:`, and `Review Waiver Reason:`. Missing fields block on `Next Legal Phase Digest Missing`; `Next Safe Move` or informal recommendations cannot replace the digest.
Formal Next Legal Phase Digests must not be compacted, abbreviated, summarized away, replaced by one-line next-step wording, or omitted because similar information exists elsewhere in the packet. `USER Plan Review Gate:` must state whether USER may accept, revise, waive, or reject the plan. `USER Inspection Files:` must name the exact files or local USER hub packet when review is required. `Review Required Because:` must explain the reason for review. `Implementation Blocker:` must name the blocker when implementation remains unauthorized. `Review Waiver Reason:` must be `Not waived` when review is required, and must explain the waiver when USER plan review is not required.
If a blocker exists, do not recommend a later phase or next-lane execution.
If repo truth is a steady-state `No Active Branch`, do not invent an implementation branch by inertia; either report that no branch should open yet or name the explicitly approved non-implementation branch class that may legally begin.

## Proof Authority Matrix

When multiple evidence layers exist, use this authority order unless a workstream explicitly documents a tighter requirement:

1. runtime markers
2. persisted source truth
3. UIAutomation and readback
4. optional UI observations such as help text, examples boxes, and transient labels

UI-only observations may be logged as notes, but they must not override stronger runtime and persisted-source proof unless the UI interaction itself is the thing being validated.

## Proof Ownership Rule

- repo-wide phase governance defines the allowed proof model
- the active workstream doc defines the branch-local validation contract, active seam, and any explicit tighter requirements
- runtime markers and persisted source truth own correctness for product behavior unless the scenario is explicitly about UI interaction quality or reachability

## Validation Helper Contract

Interactive validation helpers should default to a reusable repo-wide contract unless a workstream explicitly documents a tighter branch-local need.

That contract is:

- runtime markers and runtime logs are the primary proof surface
- persisted source or persisted state snapshots are the secondary proof surface
- UIAutomation, readback, and other live UI inspection are tertiary proof surfaces
- gating observations and non-gating observations must be separated explicitly
- runtime helpers are expected when they materially improve deterministic startup, attach, or runtime-log capture
- a watchdog or equivalent timeout-enforcement path is required for meaningful interactive closeout work
- last-confirmed-progress logging is required for timeout or stall diagnosis
- cleanup guarantees are required for helper processes, launched apps, probe files, and other session artifacts
- saved-state or source snapshots should be preserved when write safety, reopen behavior, or no-write blocking behavior matters
- windows, dialogs, overlays, and controls should be re-resolved live across close/open seams instead of reusing stale references
- validation seams must be classified as `product defect`, `harness defect`, `environment issue`, or `canon / contract drift` before product code is changed

## Validation Helper Registry And Naming Standard

`Docs/validation_helper_registry.md` is the repo-wide registry for durable root `dev/` validators, live-validation scripts, audit helpers, harnesses, and shared helper modules.

The registry must define:

- the canonical helper naming scheme
- the allowed `Helper Status:` values
- which helpers are `Reusable`
- which helpers are `Workstream-scoped`
- which helpers are `Temporary probe`
- the owner, reason, consolidation target, and promotion decision point for every workstream-scoped durable helper

Naming standard:

- repo-side validators use `dev/orin_<domain>_<capability>_validation.py`
- live desktop helpers use `dev/orin_<domain>_<capability>_live_validation.ps1`
- interactive suites use `dev/orin_<domain>_<capability>_interactive_validation.ps1`
- audit helpers use `dev/orin_<domain>_<capability>_audit.ps1`
- reusable harnesses use `dev/orin_<domain>_<capability>_harness.py`
- shared helper modules use `dev/orin_<domain>_<capability>_helper.py`

Workstream-scoped exceptions are allowed only when reuse would contaminate proof ownership, blur workstream truth, or make validation less reliable.
They must use `dev/orin_<workstream_id>_<bounded_capability>_validation.ps1` or `dev/orin_<workstream_id>_<bounded_capability>_live_validation.ps1`, be registered immediately, and carry:

- `Helper Status: Workstream-scoped`
- `Owner Workstream:`
- `Reason Reusable Helper Was Not Extended:`
- `Consolidation Target:`
- `Promotion Decision Point:`

Seam-number helper names are not the default naming model.
They are permitted only as short-lived workstream-scoped bridge names created during active seam proof, and they must be consolidated, promoted, or explicitly justified before PR Readiness.

PR Readiness must fail if a new durable root `dev/` validation helper, live-validation script, audit helper, harness, or shared helper module is unregistered, has no helper status, or is workstream-scoped without a consolidation target.

## Live Validation Reuse-First Rule

Before creating a new live-validation helper, script, or harness, Codex must inventory existing repo helpers and choose the smallest safe reuse path.

Preferred order:

1. inspect `Docs/validation_helper_registry.md`
2. use an existing helper unchanged when it already covers the needed path
3. parameterize or extend an existing helper when the validation belongs to the same desktop/runtime helper family
4. extract shared helper support when multiple helpers need the same watchdog, progress, cleanup, UIAutomation, runtime startup, saved-state snapshot, or artifact-writing behavior
5. create a new workstream-scoped helper only when reuse would contaminate the helper boundary, blur workstream truth, or make validation less reliable

One-off probes are allowed only as temporary exploratory evidence under an ignored evidence root such as `dev/logs/...`.
They must not be used as closeout-grade proof, must not be left behind as de facto reusable tooling, and must either be deleted after the pass or deliberately promoted into a documented reusable helper with workstream artifact-history notes.

If a Live Validation pass needs helper or harness changes before it can produce trustworthy evidence, the branch must reopen to `Hardening` unless the active authority record explicitly allows validation-only support edits in `Live Validation`.

Closeout-grade proof has one extra rule:

- the default budget profile of the validation helper must itself prove green before branch closeout can be claimed

Exploratory command-line overrides may still be used during hardening, but a one-off override profile is not enough to call the branch green unless that same profile becomes the documented default or the documented default also proves green.

## Seam Classification Rule

Validation seams should be classified before they are fixed:

- `product defect`
- `harness defect`
- `environment issue`
- `canon / contract drift`

Do not treat a seam as a product defect merely because the interactive harness failed first.

## Seam Workflow Contract

`Docs/phase_governance.md` is the canonical owner of seam workflow behavior.
Prompts, workstream docs, and mode docs may name a seam chain, active seam, or validation focus, but they do not define continuation authority.
Codex must derive continuation, stopping, fallback, and phase movement from source-of-truth, validation, branch truth, and this contract.

### Phase Scope

Seam workflow applies differently by phase:

- `Branch Readiness` may use planning, admission, or tightly coupled governance-repair seams, but it must not execute product/runtime implementation.
- `Workstream` uses the full bounded multi-seam pipeline as the primary execution model when an approved seam chain remains inside its governed boundary and validation stays green.
- `Hardening` may use a constrained continuous validation loop when the branch is already inside an approved hardening boundary.
- `Live Validation` may use validation, evidence-digestion, waiver, or output-contract seams; it must not become a hidden implementation phase.
- `PR Readiness` uses readiness-gate seams for merge-target canon, drift audit, PR creation, and PR validation; it is not a product implementation seam pipeline.
- `Release Readiness` is analysis-only and file-frozen; it may use review steps in output, but it must not execute file-mutating seams.

### Bounded Multi-Seam Workflow

A bounded multi-seam workflow is an ordered sequence of seams executed inside one approved phase boundary.
It is the default execution model for any governed pass working the current slice through one or more seams.
Every seam in the sequence must stay within:

- the same workstream or equivalent active authority record
- the same normal phase
- the same branch class
- the same approved scope or tightly coupled governance/validation repair scope
- a validation surface strong enough to prove the seam before continuation

Multi-seam does not mean batch execution.
It means Codex continues across a planned seam sequence without requiring a new operator prompt after every seam, while still executing exactly one active seam at a time.
Risky categories such as UI, launcher, settings, protocol, cross-subsystem, or policy work require sharper per-seam boundaries and stronger validation, not an automatic stop.

### Slice And Seam Definitions

A slice is a bounded admitted backlog-completion unit; a seam is the current execution checkpoint inside or between slices.
`bounded` describes scope and blast radius, not partiality by default. A bounded slice may still be the full currently implementable backlog-completion pass for that backlog item or branch lane.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
There is no repo-wide cap on how many slices a branch or workstream may carry.
Same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green.
Future-dependent blockers are remaining backlog work that cannot yet be implemented until another backlog item, dependency, or capability is completed.
Stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition, and leaving `Workstream` requires `Backlog Completion State: Implemented Complete` or `Backlog Completion State: Implemented Complete Except Future Dependency`.

### Default Continuation Duty

`Next-Seam Continuation Required` means continue seam-to-seam inside the current slice until all required seams are complete and the slice status is green.
When a prompt names an `Active Seam`, that seam is the entry seam, not a terminal boundary.
Seams inside the current slice may be predeclared in canon or discovered from repo truth while the slice remains in progress.
After the entry seam validates green, Codex must evaluate whether the current slice is actually green; if not, Codex must continue by default to the next seam needed inside the current slice when the continuation authority conditions pass.
Same-branch backlog completion is the branch-level default: later slices for the same backlog item stay on the same branch when scope, phase, risk, and validation authority remain green.

Codex must not stop merely because:

- the prompt task named only the entry seam
- the output format asks for `Next Safe Move`
- durability commit and push completed
- one seam was successfully recorded

reporting `Next Safe Move` is not a substitute for execution while the current slice still requires seams.
A `continue` decision must be acted on immediately by starting the next seam needed inside the current slice.
Durability commit/push after a green seam is a checkpoint, not a stop.
Do not send a final closeout response after a green entry seam while the next seam remains admitted and no bounded stop condition exists.
A final response after a green seam while `Continue Decision` remains `Continue` is `Post-Seam Final-Stop Drift`.
Post-Seam Final-Stop Drift is a governance blocker until source truth and validation are repaired.
Durability commit/push is not a lawful stop while `Continue Decision` remains `Continue`.
The `Continuation Execution Latch` is active whenever `Continue Decision: Continue`, `Stop Basis: None`, and a same-phase `Next Active Seam` are recorded; Codex must execute the next seam in the same bounded Workstream run instead of returning a terminal report.
when a slice turns green during `Workstream`, advance immediately to the next admitted slice while `Completion Status` remains `In Progress`
`Workstream` reaches `Hardening` only when `Completion Status: Green`
`Completion Status: Green` means every admitted same-branch seam and slice for the current Workstream branch is complete, deferred, blocked, or explicitly waived in source truth; one green seam or one green slice cannot move the branch to Hardening while admitted branch material remains.
`Completion Status: Red` means a named blocker or waiver currently stops bounded Workstream continuation
If `Completion Status` is `Red`, report the blocker or waiver and the action needed to clear it before continuation can resume.

A bounded stop condition blocks continuation; it does not by itself authorize stopping the backlog item after only one slice, advancing to `Hardening`, or closing the branch while `Backlog Completion State` remains `In Progress`.

A prompt-level `execute only <seam>` request does not override this continuation duty unless the request is paired with an explicit `Backlog-Split User Approval` or another named blocker from this contract.
Restrictive wording, cautious wording, and small-slice wording do not create backlog-split authority by themselves.
Prompt language such as `bounded`, `bounded seam`, `single seam`, `one pass`, `small pass`, `narrow pass`, or `only this seam` must be interpreted as active-seam scope control only; it cannot narrow an admitted multi-slice Workstream into a single-seam Workstream unless explicit USER waiver is recorded.
If Codex stops after a green seam or stops the branch after a first slice without one of the recorded reasons above, classify that stop as `Governance Drift` and repair the source-of-truth or validator gap before treating the workflow as healthy.

### Seam Stages

Each active seam follows this governed stage model:

1. `Stage 0 - Startup and admission`: load the required source-of-truth, confirm branch, phase, branch class, blockers, active authority record, and whether multi-seam continuation is legal.
2. `Stage 1 - Seam analysis and plan`: define the seam name, exact boundary, affected files or evidence surfaces, explicit non-includes, validation gate, cleanup expectations, risk class, and `UTS` applicability.
3. `Stage 2 - Execution`: execute only the active seam within the approved boundary.
4. `Stage 3 - Review and validation`: run the seam validation, inspect results, classify defects or drift, and loop back to Stage 2 only for the same seam when validation, stop-loss, and phase rules allow.
5. `Stage 4 - Record truth and continuation decision`: update branch-local workstream evidence, authority records, `UTS` artifacts, helper registry, or governance docs only when truth changed and the phase permits mutation; then report `continue` or `stop`.
6. `Stage 5 - Finalization`: summarize work, validation, cleanup, durability state, remaining blockers, next legal phase, and next safe move.

Stage 4 is not permission to churn canon after every seam.
Repository files are updated only when branch-local truth, evidence, validation contracts, helper records, or governing rules actually changed and the current phase permits file mutation.
Stage 5 becomes a terminal closeout only when `Continue Decision: Stop`; otherwise it is a status checkpoint and execution must continue into the next admitted seam or slice.

### Required Per-Seam Declaration

Before each seam, Codex must state:

- the seam name
- the active phase and branch class
- the exact boundary
- the affected files or evidence surfaces when known
- the explicit non-includes
- the validation gate required for that seam
- cleanup expectations when the seam opens files, processes, windows, helpers, or temporary artifacts
- `User Test Summary` applicability when user-visible or operator-facing behavior may be affected

After each seam, Codex must:

- run the required validation for that seam
- update active workstream evidence when branch-local truth changed
- update the canonical workstream `User Test Summary` when the seam changes user-visible or operator-facing behavior
- verify cleanup for artifacts the pass created or opened
- decide and report `continue` or `stop`
- continue by default to the next seam needed inside the current slice when `Next-Seam Continuation Required` applies and the continuation authority conditions pass
- act on a `continue` decision by starting the next seam before final closeout

### Continuation Authority

Continuation is allowed only when:

- validation passes
- no regression is detected
- no scope drift is detected
- no unplanned risk-class expansion is detected
- no governance drift is detected
- no unresolved manual-validation blocker is present
- branch truth remains consistent with the authority record
- stop-loss has not been reached
- the next seam remains inside the same permitted phase scope

If any continuation condition fails, the whole workflow stops immediately and the next safe move must be reported from the blocking truth.
If continuation would require broader authority, a different phase, unplanned risk expansion, or weaker validation, Codex must stop and report the blocker rather than treating the downstream seam as activated.
If all continuation conditions pass and the current slice still needs another seam, continuation is required under `Next-Seam Continuation Required`; do not downgrade a safe continuation into an optional stop.

### Bounded Stop Conditions

A bounded multi-seam workflow may end before phase completion only when one of these serious stop conditions is recorded:

- validation failure
- regression or failed evidence review
- scope drift or attempted work outside the approved seam chain
- unplanned risk-class expansion that requires a new admission decision
- governance drift that must be repaired before continuation
- branch-truth contradiction or dirty-state contradiction that changes phase authority
- unresolved manual-validation, User Test Summary, or live-evidence blocker
- missing source-of-truth, unreadable authority, or conflicting authority ownership
- stop-loss trigger, timeout/freeze risk, or unsafe tool/process state
- phase boundary reached, phase completion reached, or next seam belongs to a different phase
- the next seam would require weaker validation than the current seam
- explicit operator stop, pause, or waiver that does not conflict with protected-main, Release Readiness, or durability law

Category labels are not stop conditions by themselves.
Bug fix, hotfix, UI-model, launcher, settings, protocol, policy, cross-subsystem, or high-risk labels may require smaller seams and stronger gates, but they do not cancel bounded multi-seam continuation when the next seam remains admitted and green.

## Backlog-Split Rule

Legacy `Single-Seam Fallback` and `Single-Seam Mode Waiver` terms are retired and must not be used in active source-of-truth.
Same-branch backlog completion is the default.
There is no repo-wide cap that forces an admitted multi-slice package to stop after one slice; however package admission defaults to multiple admitted slices, and a package containing exactly one admitted slice requires explicit `Single-Slice Package User Approval: Granted`.
Bounded means one active seam at a time, not one-seam Workstream authority.
A single-seam Workstream requires explicit USER waiver before Workstream may stop after one seam while the package or slice remains incomplete.
A bounded stop condition blocks the workflow. It does not by itself authorize splitting the backlog item across branches.
Stopping after the first slice or splitting the backlog item across branches requires an explicit `Backlog-Split User Approval` or a named bounded stop condition.
A bounded stop condition blocks the workflow. It does not by itself authorize splitting the backlog item across branches, closing the backlog item, or leaving `Workstream` while remaining implementable work still exists.

`Backlog-Split User Approval` may split an otherwise valid same-branch slice chain across branches only when an explicit USER approval is recorded in source-of-truth, the active authority record, or the operator prompt.
If no explicit approval is raised and no bounded stop condition is recorded, keep later slices on the same branch by default and advance into them automatically while `Completion Status` remains `In Progress`.
If a bounded stop condition is recorded but remaining implementable work still exists on the current backlog item, the branch remains in `Workstream` and carries a backlog-completion latch until continuation can resume or the remaining work is proven future-dependent.
When a backlog split is used, the output or authority record must name:

- `Backlog-Split User Approval: APPROVED`
- `Backlog-Split Reason:`
- `Backlog-Split Boundary:`
- `Backlog-Split Resume Point:`

Category labels, restrictive task wording, and cautionary phrases such as `execute WS-1`, `stop after WS-1`, `smallest safe slice`, `high-risk`, `launcher`, `settings`, `protocol`, `UI-model`, or `cross-subsystem` do not create split authority by themselves.
Same-branch slice continuation does not authorize phase skipping, readiness claims, or batching multiple seams without per-seam validation.

## Continuous Validation Loop Rule

When the approved prompt or execution boundary explicitly authorizes a continuous validation pass inside `Hardening`, Codex may continue across seam iterations without waiting for a new user prompt after every rerun.

That is allowed only while all of the following remain true:

- the branch is still in `Hardening`
- the same workstream boundary and closeout goal remain valid
- the proof hierarchy, timeout contract, and helper default profile remain unchanged
- no blocker, truth drift, or required canon-sync stop appears
- the pass is still moving through one active seam at a time

Inside that continuous loop, Codex should:

- identify the first real failing seam
- classify it before changing product code
- fix only that seam
- rerun the full governed gate immediately
- continue until the full gate is green or a hard stop is reached

## Stop-Loss Rule

For governed recovery or another approved continuous validation pass:

- stop immediately if a blocker appears
- stop immediately if truth drift appears
- stop immediately if timeout inflation beyond the documented contract is required
- stop immediately if proof ownership, gating rules, or the helper default profile must change before the next rerun
- stop if `2` consecutive seam fixes fail to move the first-failing seam or otherwise fail to produce material end-to-end progress
- stop if roughly `90 minutes` of validation work pass without material end-to-end progress toward green
- when stop-loss is reached, continued execution is blocked until a decision memo or equivalent phase-state update is recorded

## Timeout Governance

Interactive hardening and live-validation work must use tiered hard stops.

Repo-wide target contract for hardened desktop interactive helpers:

- preflight startup gate: `<= 60s`
- seam or control-acquisition gate: `<= 3s` once the live desktop surface is already open
- no-progress watchdog: `<= 3s`
- normal scenario budget: `<= 60s`
- exceptional scenario budget: `<= 90s`, only when explicitly declared in the workstream doc
- full interactive rerun hard cap: `<= 15 minutes`
- outer execution timeout: only slightly above the harness hard cap

Prohibited without explicit workstream-doc reconciliation:

- undocumented `90s+` scenario budgets
- undocumented `15m+` full-run caps
- silent timeout inflation during closeout

Additional repo-wide rule:

- when hardening proves that a tighter and faster default helper profile is stable, that profile should replace the older relaxed default before closeout-grade proof is claimed
- if a seam keeps breaching the documented `3s` or `60s` targets, treat that as validation-helper or process debt and redesign the proof path instead of silently letting the run sit longer
- every interactive helper or live-validation run must emit visible progress before and during execution, including scenario start, meaningful step progress, scenario result, and last-confirmed-progress evidence
- if a helper does not already enforce a tighter watchdog, `10s` is the maximum allowed no-progress interval before the run must self-abort, clean up, report the last confirmed progress point, and classify the stall
- long-running interactive commands must not hide behind only the shell/tool outer timeout; they must be supervised by a watchdog, monitor job, child process, or equivalent path that can abort and clean up blocked UIAutomation, app launch, screenshot, focus, source-write, or cleanup operations
- Codex should poll or surface helper progress during live validation instead of leaving the operator with a silent long-running command

## Truth-Drift Enforcement Rule

- if validation or harness behavior changes materially, canon must be updated before continued execution is recommended
- if a workstream changes which evidence layer is authoritative for success, that change must be written into the active workstream doc before the next seam-fix iteration
- if a workstream doc, harness defaults, and live execution evidence disagree, the workflow remains in `Hardening` or `Live Validation` until the drift is reconciled

## Preflight Requirement

Before a full interactive gate is used as a closeout proof surface, run or confirm a preflight that proves:

- startup or probe acquisition works
- runtime log creation works
- the overlay or root runtime surface opens
- the cleanup path works
- no stale helper processes, probe windows, or leftover session artifacts are still active from an earlier failed run

If preflight fails, the branch remains in `Hardening`.
Do not burn a full closeout run first.

## Desktop UI Audit Rule

When a branch materially changes user-facing desktop UI and that UI is relevant to the closeout claim:

- a live launched-process UI audit is required before branch closeout is treated as complete
- the audit should happen after the branch is green or effectively green, not during every seam iteration
- the audit evidence should include a manifest or equivalent index plus the captured screenshots or other durable artifacts
- the audit should check layout, readability, visibility, hierarchy, and obvious regressions against the current desktop UI direction

This does not create a repo-wide rule that every validation pass must always take screenshots.
The canonical rule is narrower:

- marker-first proof for behavior
- live launched-process UI audit when meaningful desktop UI changed and closeout depends on user-facing UI quality

### Visual-Claim Proof Lock

When a branch carries a concrete visual/layout concern, H1 or closeout proof must
prove that exact visible concern with geometry assertions, screenshot audit
evidence, or an equivalent durable visual check. Dataset markers, copy presence,
and successful click/action flow cannot by themselves close a visual/layout
claim.

If USER screenshot or video evidence contradicts a green H1 result, the branch
returns to Hardening for that concern. Codex must record why the earlier proof
was insufficient, patch the smallest reliable validator/helper coverage that
would have caught the defect, rerun validation, and only then recommend PR
Readiness or user handoff again.

## Phase Transition Rule

- `Branch Readiness` -> `Branch Planning` only after branch base, branch class, authority record, branch objective, target end-state, complete family-package product planning packet when applicable, project-wide vision alignment, branch-specific vision alignment, product-system concept model, entity/profile model, user workflow model, scale/state planning, expected seam families and risk classes, validation contract, User Test Summary strategy, later-phase expectations, USER critique/decision loop, Codex additional recommendations, and first Branch Planning target are explicit, and no `Branch Readiness Planning Incomplete` blocker remains active unless explicitly USER-waived
- `Branch Planning` -> `Workstream` only after BP1 is accepted or explicitly waived, BP2 is accepted or explicitly waived, BP3 Workstream Entry / Orchestration Validation is green, the admitted Workstream package and entry seam or initial seam sequence are explicit, and no Branch Planning packet, decision-path, vision, plan, or orchestration blocker remains active unless explicitly USER-waived
- `Workstream` -> `Hardening` only after the current Workstream work reports `Completion Status: Green`, every admitted same-branch seam and slice for the current branch is complete, deferred, blocked, or explicitly waived in source truth, no remaining implementable work is still available on that backlog item, `Backlog Completion State` is `Implemented Complete` or `Implemented Complete Except Future Dependency`, direct validation is green, User Test Summary obligations are current for user-facing changes, and no same-slice correctness gap remains
- `Hardening` -> `Live Validation` only after repo-side hardening proof is sufficient for interactive or manual closeout work
- `Live Validation` -> `PR Readiness` only after branch-local proof is sufficient for closeout, returned evidence has been digested into the authority record, and `User Test Summary Results Pending` is absent or cleared by a documented waiver
- `PR Readiness` -> `Release Readiness` only after merge-target canon completeness passes, the Governance Drift Audit passes, the USER-approved next-workstream selection gate passes or a USER-approved next-workstream waiver/defer is explicitly recorded, branch creation remains deferred to `Branch Readiness`, direct GitHub/GitHub-connector verification proves that the live PR is `merged`, and any release candidate anchor/target/scope/artifact truth needed for release review is already available without file mutation
- `Release Readiness` stays restricted to analysis-only release target, scope, artifact, release-execution authorization, and release-state confirmation work; it does not transition into a docs-sync phase or a file-mutation phase

There is no default direct `Branch Readiness` -> `Workstream` transition.
There is no default direct `Workstream` -> `PR Readiness` transition.
If Workstream appears complete, the next normal phase is `Hardening` unless an explicit authority-record waiver says otherwise.

Later phases must not paper over missing earlier-phase requirements.
If a later phase discovers an earlier-phase defect, reopen the branch to the failed earlier phase.

## Phase Definitions

### Branch Readiness

Purpose:

- validate branch base
- declare branch class
- set up or confirm the promoted workstream authority record or branch authority record
- align branch-start canon
- lock execution, validation, and timeout boundaries
- plan the whole branch at phase level before implementation begins

Branch Readiness uses two internal stage gates without changing the canonical phase enum:

- `Branch Readiness Stage 1 - Analysis Gate`: analysis-only; no repository file mutation, branch creation, package admission, docs sync, PR work, release work, selected-next truth, or canon edits are allowed. Stage 1 must output `## Branch Readiness Stage 1 Analysis Packet` for USER review and stop on `Branch Readiness Execution User Approval Missing`.
- `Branch Readiness Stage 2 - Execution Gate`: begins only after explicit USER approval to enter Stage 2. Stage 2 performs approved branch/package admission work, docs sync, branch creation, and authority-record setup only inside the USER-approved FAM/package scope. Stage 2 closeout must clearly distinguish "setup complete" from "implementation approved": it must tell USER that the created/admitted branch is ready for BP1 USER Branch Vision Review, BP2 USER Branch Plan Review, and BP3 Workstream Entry / Orchestration Validation in `Branch Planning`, and that runtime implementation remains blocked until Branch Planning is green or source truth records an explicit USER waiver. When a USER-approved Family Feature Vision exists for the candidate feature category, Stage 2 must load it before final route admission and must not rely on broad Family Vision alone for Feature Vision Context. When the selected feature-bearing route requires Family Feature Vision and none exists or the existing record is shallow, Stage 2 must route to Family Feature Vision planning/admission instead of BP1.

The `## Branch Readiness Stage 1 Analysis Packet` must include governed state markers, FAM/package candidate, package-size review, multiple admitted-slice plan, single-slice drift check, Element Coverage review, `Backlog Taxonomy And Source-Truth Placement Gate:` when the branch proposes or consumes broad AI-native, cache, architecture, policy, experience, runtime-subsystem, capability-pack, new-FAM, new-family-feature-vision, or new-owner concepts, product vision, project-wide vision alignment, family vision alignment, Family Feature Vision alignment or `Family Feature Vision Required For Selected Feature` / `Family Feature Vision Not Applicable` disposition, branch-specific vision alignment, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable vs full-system boundary, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, expected user-facing outcomes, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, rejected shallow plan, alternatives/tradeoffs reviewed, open USER decision points, deferred ideas/future-package ledger, validation plan, `Stale Branch Cleanup Plan:`, expected docs sync, blockers and waivers, rollback path, `Branch Readiness Planning Incomplete` blocker review, `Next Legal Phase:` digest field, and the exact Stage 2 green-light decision needed from the USER.

Before the Stage 1 packet recommends USER-selectable candidates, it must include the `BR1 Candidate Viability / Grouping Matrix` from this file. The matrix must prove every recommended option has a concrete feature outcome, implementation-bearing route class, behavior-change classification, support/infrastructure relationship, Family Feature Vision and Deferred Feature Carryforward disposition, grouping recommendation, split reason when not grouped, expected Slice/SLC/seam map, proof path, largest safe coherent package explanation, and tiny-branch sprawl review. Candidate rows that are planning-only, readiness-only, support-only, manifest-only, or too small without a split reason keep the relevant BR1 blocker active.

`Carrier Lifecycle Decision` is required in Branch Readiness Stage 1 for any requested branch/worktree. Stage 1 must classify the carrier with `Carrier Lifecycle Classification:` as exactly one of `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, or `Active remote/open PR branch`; it must report `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Stale Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `Stable Worktree Path:`, `Replacement Binding Path:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`. Stage 1 analyzes only; when it finds a stale empty local branch that is behind `origin/main`, has no unique commits, and has no governing open PR, the recommendation is to create/recreate the fresh carrier from current `origin/main` during Stage 2 rather than silently reusing stale branch identity. Stage 2 must stop on `Stable Worktree Path At Risk` if cleanup would remove a family-stable folder before the replacement branch/worktree is bound there.

`Stale Branch Cleanup Plan:` is required when Release Readiness, PR Readiness, or multi-worktree preflight identified old/stale branches, retired worktrees, or stale GitHub Desktop entries. Stage 1 analyzes only. The cleanup itself belongs to `Branch Readiness Stage 2 - Execution Gate` alongside branch/worktree creation or validation, because every Git repository and GitHub Desktop-bound worktree must keep a valid branch target until the replacement target is ready. If cleanup touches a stable family alias such as a durable FAM worktree folder, `Stable Worktree Path Preservation Gate:` must prove `Stable Worktree Path:` and `Replacement Binding Path:` before cleanup proceeds.

`Post-Release External State Carry-Forward:` is required in Branch Readiness Stage 1 when the previous Release Readiness Stage 2 release has completed and external operational records still point at the just-released branch, PR, release-window, selected-next state, or old source commit. This is a normal BR1 check, not a blocker by itself. Stage 1 must report whether the carry-forward was already reconciled during bounded RR2 post-release closeout or must be reconciled in Branch Readiness Stage 2 before branch/worktree setup or implementation. It becomes `External Operational State Conflict` only when the external state disagrees with Git/GitHub/repo validation in a way that changes the legal next carrier, requires repo source-truth mutation, requires branch/worktree cleanup, or could authorize stale runtime/FAM/private work.

`Post-Merge Release Readiness Handoff:` is required in Branch Readiness Stage 1 when fetched `origin/main` contains release-bearing merged work after the latest public prerelease, when the current worktree just completed PR2/merge/rebaseline for release-bearing work, or when the requested successor BR1 follows a release-bearing branch merge. BR1 must report whether Release Readiness Stage 1 has run for the current candidate anchor or whether USER explicitly deferred Release Readiness before successor selection. If neither proof exists, BR1 stops on `Post-Merge Release Readiness Decision Missing` or `Release Readiness Handoff Skipped` before recommending successor runtime candidates. This handoff does not execute release, tag, GitHub Release, artifact, issue, cleanup, runtime, provider, private, cache, or memory work; it only prevents successor planning from skipping the file-frozen release-readiness decision point.

Family Feature Vision and Deferred Feature Carryforward BR2 rule:

- `Family Feature Vision` is the durable feature-category layer between Family Vision and Branch Vision Snapshot. When an approved record exists under `Docs/family_feature_visions/`, BR2 must load it before presenting USER-selectable branch options for that feature category.
- `Family Feature Vision Required For Selected Feature` blocks BP1 entry for a selected feature-bearing branch route until the required USER-approved Family Feature Vision exists and passes the `Feature Vision Sufficiency Check`. The next legal phase is Family Feature Vision planning/admission on the current legal carrier, not BP1, when the selected route creates, expands, or depends on a durable feature category that needs more detail than the broad Family Vision can safely preserve.
- `Feature Vision Sufficiency Check` requires branch-consumable durable content: feature purpose, USER-facing surfaces, experience flow, included capabilities, explicit non-goals, dependency/deferred map, design options, proof expectations, Branch Readiness consumption notes, BP1 context notes, fold-down history when applicable, and active-state wording scan. A shallow, generic, copied-list-only, placeholder, or branch-local implementation-only Family Feature Vision does not satisfy BP1 entry and keeps `Family Feature Vision Required For Selected Feature` active.
- `Family Feature Vision Not Applicable` is allowed only for governance-only, release-support, pure helper/validator, source-truth-only, or otherwise non-product branches where no selected product/runtime/user-facing feature category needs a durable middle vision owner. The reason must be stated in BR2 or the branch planning packet.
- If Family Feature Vision planning exposes durable feature ideas, deferrals, surfaces, proof expectations, grouping rules, or routing constraints, Codex must fold those items into the relevant vision owner before BP1 or record a durable deferred disposition. Proposed, unresolved, branch-local, or live operational ideas must not be silently dropped and must not become active branch state in repo vision files.
- BR2 must treat Deferred Feature Carryforward as durable planning preservation, not active branch state. Deferred items are candidates for option evaluation; they do not select a branch, open a PR, set selected-next truth, or authorize implementation by themselves.
- For each USER-selectable BR2 option, BR2 must present an applicability matrix with `Option name`, `Main feature/package objective`, `Applicable deferred carryforward items`, `Reason each deferred item is applicable`, `Dependency trigger that makes the deferred item relevant`, `Recommended grouping`, `Deferred items that remain future-gated`, `Reason future-gated items remain deferred`, and `Validation/proof expectations if the option is selected`.
- If a BR2 option satisfies a deferred item's dependency trigger and shares the same FAM, package objective, owner/worktree, release timing, and validation/proof path, Codex must recommend grouping it into one coherent package rather than splitting it into tiny branches.
- If a deferred item remains future-gated, BR2 must say why: unmet dependency, different Family Feature Vision, different FAM/worktree owner, private/provider/runtime action gate, validation path divergence, release timing divergence, USER decision missing, or unsafe package size.
- BR2 output may use active decision language because BR2 is the dynamic option-evaluation gate. The Family Feature Vision file itself must not store active terms such as `active`, `current branch`, `selected next`, `pending PR`, `in progress`, `next branch`, or release-window status.
- Missing applicable deferred carryforward review blocks on `Deferred Feature Carryforward Review Missing`. Ignoring a relevant deferred item from the selected Family Feature Vision blocks on `Deferred Carryforward Applicability Missing`. Splitting deferred items into tiny branches when dependency and validation proof support one coherent package blocks on `Deferred Carryforward Branch Sprawl`.

Vision Carrydown Contract:

- The governed vision chain is `Project Vision -> Family Vision -> Family Feature Vision -> Branch Vision Contract Snapshot -> BP2/BP3 engineering plan -> Workstream/Hardening/Live Validation proof`.
- Every vision layer must satisfy the product-detail quality bar from its owner: vision contracts describe product outcome, user experience, surfaces, UI/UX expectations, trust/recovery posture, non-goals, and proof expectations, not only file purpose, routing procedure, copied context, or future "define later" placeholders.
- BR1 and BR2 must report which layers apply, which files were loaded, whether a Family Feature Vision exists, whether it is sufficient, and whether any layer is not applicable with a source-truth reason.
- BP1 must digest the applied Project Vision, Family Vision, and Family Feature Vision into a branch-specific vision. BP1 must not invent feature-category direction from branch-local reasoning when the correct Family Feature Vision is missing, shallow, stale, slice-specific, or pointer-stale.
- BP2 must translate the accepted or waived BP1 vision into branch-local Slice/SLC/seam engineering work, proof outputs, rollback, risk controls, and deferred-item dispositions. If BP2 changes product direction, user-facing behavior, UI carrydown, surface scope, or deferred/future-gated boundaries, it must route back to BP1 or record an explicit USER waiver before BP3.
- BP3 must verify that the Workstream package implements the accepted or waived BP1/BP2 vision chain, not merely that markers, fixtures, or command outputs are green.
- Workstream and Hardening must preserve the same selected Family Feature Vision elements, deferred-item decisions, and UI/proof expectations unless source truth routes a revision back to Branch Planning.
- Live Validation must compare observed behavior against the Project Vision, Family Vision, applied Family Feature Vision when present, accepted Branch Vision Contract Snapshot, and accepted BP2/BP3 proof plan. Helper output, runtime logs, screenshots, videos, markers, manifests, or branch-plan prose cannot clear a product/user-facing claim unless Codex also adjudicates the claim against that vision chain, verifies independent evidence for the claim, or records an explicit waiver/manual-validation requirement.
- USER review packets for BP1, BP2, BP3, Hardening, Live Validation, and UTS handoff must show the applied vision layers, selected/deferred elements, user-facing surfaces, proof gathered, evidence paths, PASS/FAIL/BLOCKED/UNPROVEN disposition, and future-gated scope in a USER-readable way.
- Missing vision-layer proof blocks on `Vision Carrydown Chain Missing`. Branch-local invention while a Family Feature Vision is required blocks on `Branch Vision Invented From Local Reasoning`. Missing Live Validation comparison blocks on `Vision Proof Alignment Missing`. A USER packet that omits the applied vision/evidence mapping blocks on `USER Packet Vision Evidence Missing`. Product-vision files that are mostly procedural, placeholder, slice-route-only, or copied-context-only block on `Vision Contract Product Detail Missing` until repaired or explicitly waived for a non-product branch.

For broad implementation family packages, Branch Readiness planning is not complete until the planning packet records USER vision inputs or explicit unanswered-question blockers, project-wide vision alignment, branch-specific vision alignment, Codex product interpretation, Codex implementation recommendation, Codex additional recommendations, USER/ChatGPT review checkpoint, USER critique loop, USER decision ledger, full feature element breakdown, system concept model, entity/profile model, user workflow model, scale/data-volume model, configuration/state model, whole-system interaction map, minimum viable versus full-system boundary, alternatives/tradeoffs reviewed, rejected shallow plan, current-branch versus future-package boundaries, affected files/surfaces, branch reach/package-size proof, expected user-facing outcomes, acceptance criteria, screenshot/live/User Test Summary proof requirements for user-facing work, implementation sequence proposal, deferred ideas/future-package ledger, open USER decision points, and USER decisions needed. Marker-only planning, a one-screen/simple-system plan, scaffold-only proof, or Codex self-assessment that the plan is "simple enough" is insufficient. The same planning proof remains required if the active implementation branch has already moved into Workstream, Hardening, Live Validation, or PR Readiness; later phases must route back to Branch Readiness instead of continuing with shallow planning debt.

The active implementation branch `Product Definition Plan` must include non-empty, concrete, non-placeholder `Project-Wide Vision Alignment:`, `Branch-Specific Vision Alignment:`, `System Concept Model:`, `Entity / Profile Model:`, `User Workflow Model:`, `Scale / Data Volume Model:`, `Configuration And State Model:`, `Expected User-Facing Outcomes:`, `Codex Additional Recommendations:`, `USER Critique Loop:`, `USER Decision Ledger:`, `Deferred Ideas / Future Package Ledger:`, `Planning Adequacy Review:`, `Rejected Shallow Plan:`, `Alternatives And Tradeoffs Reviewed:`, `Whole-System Interaction Map:`, `Minimum Viable vs Full System Boundary:`, and `Open Questions / USER Decision Points:` markers before Workstream, Hardening, Live Validation, or PR Readiness can begin or resume. `Planning Packet Status: Complete` is invalid when those values are placeholder, self-assessed, too shallow, or missing the required USER critique/decision state.

For user-facing family/package branches, Branch Readiness must also declare an `Interface Release Boundary` before Workstream begins or resumes. The packet must record `Primary Interface Release Surface:`, `Interface Bundle User Approval:`, `Fallback Point:`, and interface-specific acceptance/proof requirements. The default is one primary user-facing interface release surface per branch; multiple released user-facing interfaces in the same branch require explicit USER approval recorded as `Interface Bundle User Approval: Granted`, including the bundled surfaces, reason, fallback point, and acceptance plan. This rule does not create single-seam or single-slice Workstream authority: the branch may and usually should still contain multiple seams and slices inside the declared interface boundary. If the primary interface is missing, the branch mixes multiple release interfaces without approval, or no fallback point exists, Workstream entry or continuation is blocked by `Interface Release Boundary Missing`, `Primary Interface Undefined`, `Multiple Interface Release Drift`, `Fallback Point Missing`, `Interface Acceptance Missing`, or `Branch Readiness Interface Planning Incomplete` until Branch Readiness repairs the plan or the USER explicitly waives the interface-bundle rule.

Supporting dependency repairs may ride the current branch only when source truth classifies them as dependency work rather than as released user-facing interfaces. Dormant, experimental, or future interface implementations may remain in the repo only when source truth marks them as non-gating for the current primary interface, records their future branch/package path, and validators/proof helpers separate current-interface acceptance from future-interface evidence.

When USER input is needed, Codex must output a structured `USER Vision Question Packet`. Each question must include question ID, category, decision needed, why this matters, feature area affected, Codex recommendation, why Codex recommends it, alternatives/options, tradeoffs/risks, current-branch impact, future-package impact, safe default if USER is unsure, whether the answer is required before implementation, whether USER may waive/defer it, and exact response format requested. Required categories for user-facing family packages are product goal/user outcome, visual identity/style, layout/placement, information hierarchy, data/source model, controls/settings model, fail-safe/no-data/degraded behavior, interaction model, accessibility/readability, privacy/security boundaries, performance constraints, validation proof standard, User Test Summary acceptance criteria, current-branch versus future-package boundaries, and release impact.

When USER input needs a durable user-editable handoff, Codex must generate or refresh a USER-facing `User Vision Input.txt` desktop artifact. The artifact must present each decision with Codex's recommendation, rationale, options, tradeoffs, current-branch impact, future-package impact, proof impact, and three answer paths: accept Codex recommendation; change recommendation with USER-written changes; or defer/future-package/waive with USER-written reason. This artifact is USER input only and not repo source truth. Codex recommendations, default options, and unanswered prompts must not be treated as USER-approved answers. Repo source truth may record artifact generation and blockers, but USER answers enter repo source truth only after a later USER-approved digest pass reads and summarizes the completed artifact.

For runtime/user-facing branches, the accepted USER answers become the Branch Vision Contract Snapshot inside the active Branch Engineering Plan. Workstream implementation may proceed only when required vision questions are answered, explicitly deferred with waiver, or classified as Level 1 non-blocking queue items. Codex recommendations and ChatGPT recommendations remain proposed until USER accepts, revises, rejects, defers, or waives them.

Allowed planning loop: Branch Readiness Stage 1 analyzes planning sufficiency; USER/ChatGPT reviews the packet; Branch Readiness Stage 2 may repair/source-sync the planning packet after USER approval; Branch Readiness Stage 1 revalidates planning sufficiency; the loop repeats until planning is complete or explicitly USER-waived. Workstream entry or continuation is blocked while `Branch Readiness Planning Incomplete` or any of its planning blockers remain active.

Planning blockers are planning blockers, not implementation blockers. They include `Product Vision Input Missing`, `Project-Wide Vision Alignment Missing`, `Branch-Specific Vision Alignment Missing`, `USER Vision Question Packet Missing`, `USER Vision Recommendation Missing`, `USER Vision Questions Unanswered`, `USER Vision Input Pending`, `USER Vision Input File Missing`, `USER Vision Input Answers Pending`, `USER Vision Input Digest Pending`, `System Concept Model Missing`, `Entity / Profile Model Missing`, `User Workflow Model Missing`, `Scale / Data Volume Model Missing`, `Configuration And State Model Missing`, `Expected User-Facing Outcomes Missing`, `Codex Additional Recommendations Missing`, `USER Critique Loop Missing`, `USER Decision Ledger Missing`, `Deferred Ideas / Future Package Ledger Missing`, `Planning Adequacy Review Missing`, `Rejected Shallow Plan Missing`, `Alternatives And Tradeoffs Missing`, `Whole-System Interaction Map Missing`, `Minimum Viable vs Full System Boundary Missing`, `Open Questions / USER Decision Points Missing`, `Branch Reach Unproven`, `Feature Element Breakdown Missing`, `Acceptance Criteria Missing`, `User-Facing Proof Standard Missing`, `Current Branch vs Future Package Boundary Missing`, and `Branch Readiness Planning Incomplete`. They clear only when the packet is complete and revalidated, when completed USER Vision Input answers are digested into repo source truth, or when explicit USER waiver text is recorded.

Family-package planning may also record package-specific planning blockers when USER input exposes unresolved product architecture or naming scope. Examples include `Legacy Product Name Drift`, `Hardware Telemetry Provider Selection Pending`, `Polling Floor Undecided`, `Warning Delivery Modality Pending`, `External Telemetry Privacy Model Missing`, `Audio Warning Cross-Family Approval Missing`, and `Persona Switch Scope Boundary Pending`. These blockers prevent Workstream entry or continuation until Branch Readiness revalidates the current-branch/future-package boundary, records a safe implementation path, defers the item to a future package, or records an explicit USER waiver. When USER declares legacy product naming invalid for the current product, `Legacy Product Name Drift` blocks Workstream entry or continuation while that naming remains anywhere in tracked repo source, runtime artifact paths, validators, docs, generated-user surfaces, user-facing copy, or persona-facing copy. The only default preservation location is external GitHub release/tag history; tracked repo preservation requires explicit USER waiver or a USER-approved migration carrier. Product identity and persona identity must remain separate: ORIN may be the shipped/default persona, ARIA may be shown only as locked/coming soon planning copy when source truth allows it, and actual persona switching implementation requires later admission.

A broad family-package plan is not complete while current-branch scope, future-package deferrals, provider path, polling posture, warning modality, privacy model, taxonomy/source-truth placement, naming/product-copy handling, acceptance criteria, or proof standards remain candidate-only. Branch Readiness Stage 2 may finalize those boundaries after USER approval, but Workstream entry or continuation remains blocked until a later Branch Readiness Stage 1 pass revalidates the finalized plan or records an explicit USER waiver.

Element Coverage is a non-identity checklist owned by FAM/package analysis only. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

Allowed:

- source-of-truth audit
- branch-base validation
- branch-start canon sync
- workstream promotion, branch-record setup, or authority setup
- execution-boundary definition
- branch-level execution planning

Forbidden:

- implementation
- PR material preparation
- release packaging

Required evidence:

- updated `main` truth
- correct execution base
- explicit branch class
- explicit phase block in the authority record
- branch objective and target end-state
- product vision, USER vision questions, `USER Vision Question Packet`, Codex product interpretation, Codex implementation recommendation, USER/ChatGPT review checkpoint, full feature element breakdown, current branch vs future package boundaries, affected surfaces, branch reach, why the branch is large enough, why it should not split into tiny branches, acceptance criteria, screenshot and User Test Summary proof expectations, implementation sequence proposal, planning blockers, and USER decisions needed for family/package product work before implementation
- affected-surface mapping and implementation delta classification
- expected seam families and risk classes
- backlog-completion strategy for the whole backlog item, including any known future-dependent blockers
- validation contract and User Test Summary strategy
- expected Hardening, Live Validation, PR Readiness, and Release Readiness needs
- admitted implementation slice or explicit USER-approved docs-only bypass markers
- first Workstream seam or initial seam sequence

Exit:

- branch base is valid
- active workstream authority exists
- exact phase state is recorded
- branch-start canon is coherent
- execution boundary is explicit
- implementation delta class is explicit
- admitted implementation slice is explicit, or an explicit USER-approved docs-only bypass is recorded
- branch-level execution plan is explicit enough to enter Workstream without inventing the lane shape mid-execution
- branch-level closure rule is explicit enough to keep the backlog item on one branch until it is fully implementable and complete or only future-dependent blockers remain
- when later PR Readiness is expected, explicit direct PR verification truth for the future PR gate: target-binding rule, live PR inspection method, Codex Connector approval-latch rule, concise revalidation-comment rule, same-PR repair authority, merge/close verification method, and watcher-exception posture. Watcher-based bot monitoring is not default PR2 behavior; it requires a separate USER-approved watcher exception before `PR Watcher Provisioning Unproven` or `PR Watcher Routing Unverified` can become active blockers.

### Branch Planning

Purpose:

- obtain USER-facing branch vision acceptance before engineering planning
- obtain USER-facing branch plan acceptance before orchestration validation
- prove the accepted plan is ready for Workstream implementation
- preserve branch-size law and Slice/SLC traceability without creating sprawl branches

Branch Planning uses three internal stage gates without changing the canonical phase enum:

- `BP1 - USER Branch Vision Review`: uses `USER_BRANCH_VISION_REVIEW.md` to present Project Vision Context, Family Vision Context, Feature Vision Context, Branch Goal, End-State Vision, user-facing behavior, surface map, design options, Codex recommendations, USER response, Codex digest, accepted Branch Vision, deferred/future-gated ideas, question queue, design assumption ledger, and acceptance/revision/rejection/waiver status. BP1 cannot begin while `Family Feature Vision Required For Selected Feature` is active. When a USER-approved Family Feature Vision exists, `Feature Vision Context` must digest that file and its Deferred Feature Carryforward instead of inventing feature direction from branch-local reasoning. The BP1 artifact must be substantive and branch-specific: it digests source-truth context into an applied branch vision, explains what USER will see/review/decide/rely on, names real design options and tradeoffs, asks decision-driving questions, and cannot pass as a template shell, copied-file list, generic options list, or marker-only packet.
- `BP2 - USER Branch Plan Review`: uses `USER_BRANCH_PLAN_REVIEW.md` to present the engineering plan derived from accepted or waived BP1, including package summary, branch scope size test, Slice/SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, Element-to-Phase Proof Matrix, Runtime Observability Decision Matrix when applicable, exact normal USER desktop runtime launcher proof plan, launcher parity proof plan if troubleshooting may substitute, photo/video proof plan, manual USER validation plan, H1 expectations, LV/UTS expectations, rollback/safety plan, risks, future-gated boundaries, and exact BP3 approval text. The BP2 artifact must translate the accepted BP1 vision into a branch-specific engineering contract with scope, slice-level deliverables, seams, proof outputs, risk controls, rollback/reversibility posture, options, tradeoffs, and Codex recommendation; it must preserve the BR2/BP1 disposition of applicable deferred carryforward items and cannot merely repeat BP1, list markers, or point USER at copied files.
- `BP3 - Workstream Entry / Orchestration Validation`: proves BP2 correctly implements BP1, proves package size and Slice/SLC traceability, verifies affected files, validators, helper updates, H1/LV/UTS/rollback/proof paths, validates runtime observability and exact-launcher/photo-video/manual-validation planning when applicable, preserves future-gated boundaries and deferred-item dispositions, and returns bounded Workstream implementation approval for the admitted same-branch package only when BP1 and BP2 are accepted or explicitly waived and BP3 validation is green. The BP3 artifact must name the entry seam or initial seam sequence and must be a substantive orchestration-readiness contract with scope, implementation order, validation/proof plan, rollback posture, drift controls, unresolved USER decisions, blockers, and a go/repair/blocked recommendation; it cannot rely on helper-green hygiene or first-seam-only readiness.

Allowed:

- USER-facing vision and plan packets
- external operational state updates for active branch planning
- source-truth fold-down needed to represent accepted USER decisions
- helper, validator, fixture, and packet repairs needed to make Branch Planning self-validating
- exact bounded Workstream package implementation approval text, including the entry seam or initial seam sequence, when BP3 is green

Forbidden:

- runtime/code implementation
- treating SLCs/slices as automatic separate branches
- using Workstream for planning, Hardening planning execution, Live Validation execution, PR creation, merge, release execution, private/provider/runtime/cache/memory setup, or branch cleanup
- approving implementation while BP1 or BP2 is pending, stale, missing, rejected, or unwaived
- treating BP1, BP2, or BP3 packet generation, stale-language hygiene, marker validation, copied-file lists, helper PASS output, or ZIP consistency as substantive USER review content or USER gate acceptance

Required evidence:

- accepted or explicitly waived BP1
- accepted or explicitly waived BP2
- BP3 orchestration validation with the admitted Workstream package and entry seam
- Slice/SLC traceability from BP1 accepted branch vision requirements to BP2 branch plan line items
- local USER hub packet at `C:\Nexus USER\<worktree-label>` with matching timestamped upload ZIP at `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip` when USER review is required
- packet decision-path consistency and unresolved-placeholder absence
- substantive BP1/BP2/BP3 USER review artifacts that contain applied branch-specific vision, plan, or orchestration content rather than template instructions, copied-file manifests, generic recommendations, or broad non-decision-driving USER questions

Exit:

- BP1 accepted or explicitly waived
- BP2 accepted or explicitly waived
- BP3 green
- admitted Workstream package and entry seam or initial seam sequence are explicit
- implementation approval text preserves all pending USER action gates

### Workstream

Purpose:

- execute the approved bounded runtime/code implementation slice-level deliverable or an explicit USER-approved docs-only bypass
- run normal repo-side regression validation inside that boundary
- use bounded multi-seam workflow as the primary model when the current slice remains inside its governed boundary and validation stays green

Allowed:

- bounded code or docs changes that implement the accepted Branch Planning contract
- direct verification inside the approved scope
- one active seam at a time within the current slice seam chain
- incremental implementation evidence when branch-local truth changes
- admission and execution of additional same-branch slices when they remain inside the backlog item, branch objective, expected seam families, risk class envelope, and validation authority already established in Branch Readiness

Forbidden:

- silent scope expansion
- product/design planning, branch vision negotiation, branch plan negotiation, BP1/BP2/BP3 packet creation as a substitute for Branch Planning
- planning-only or docs-only output as a substitute for implementation on an `implementation` branch without explicit USER-approved bypass markers
- hidden hardening or closure claims
- Hardening execution
- Live Validation execution or UTS handoff
- PR or release packaging
- batching multiple seams without per-seam validation and continue-or-stop gates
- crossing risk class, subsystem family, or phase boundaries under a multi-seam prompt

Required evidence:

- approved execution boundary
- accepted or explicitly waived BP1 and BP2, plus BP3 green
- accepted Branch Vision Contract Snapshot or recorded not-required reason when the branch is runtime/user-facing
- no blocking open vision questions unless they are deferred with USER waiver
- implementation delta classification and planning-loop guardrail markers
- admitted implementation slice
- direct verification of the changed behavior or docs
- seam sequence when multiple seams may execute in one pass
- per-seam validation results and continue-or-stop decisions
- explicit backlog completion status, remaining implementable work, and future-dependent blockers

Exit:

- admitted implementation slice is implemented, or an explicit USER-approved docs-only bypass has completed its approved boundary
- backlog completion is reevaluated after each completed slice and seam sequence
- `Backlog Completion State` is `Implemented Complete` or `Implemented Complete Except Future Dependency` before the branch leaves `Workstream`
- direct verification is complete
- no unresolved same-slice correctness gaps remain
- Workstream evidence and User Test Summary obligations are current for user-facing changes

### Hardening

Purpose:

- pressure-test the current branch truth
- stabilize defects, seams, validators, or harnesses before closeout

Allowed:

- validators
- harness work
- runtime helper work
- small supporting evidence infrastructure
- bounded corrective fixes

Forbidden:

- unrelated feature work
- new lane selection
- release packaging

Required evidence:

- validator results
- runtime results when relevant
- plan-vs-vision comparison when a Branch Vision Contract Snapshot is required
- explicit distinction between product defects, harness defects, environment issues, and canon or contract drift

Exit:

- branch-local hardening gate is green
- no unresolved first-failing seam remains
- no truth-drift contradiction remains

### Live Validation

Purpose:

- prove the user-facing or operator-facing branch truth through interactive, manual, or launched-process evidence
- digest that evidence into canon

Allowed:

- interactive validation
- manual validation digestion
- UI audit when relevant
- validation-only support changes if the branch reopens to `Hardening` first

Forbidden:

- new implementation
- PR packaging
- behavior widening without reopening earlier phase

Required evidence:

- required interactive or manual evidence
- required UI audit evidence when applicable
- exact normal USER desktop runtime launcher proof for desktop/user-facing behavior, or explicit USER waiver with reason
- troubleshooting launcher proof may substitute only with USER consent and `Launcher Parity Proof: PASS`
- photo/video or ordered frame-sequence proof for every visible USER-facing closeout claim, or USER-elevated manual validation/waiver when photo/video cannot prove the claim
- runtime log, Dev Toolkit, manifest, screenshot/video, interaction-matrix, and raw-evidence references in the USER packet when those artifacts support Live Validation
- vision-vs-observed-behavior comparison across the applied Project Vision, Family Vision, Family Feature Vision when present, accepted Branch Vision Contract Snapshot, and accepted BP2/BP3 proof plan, or an explicit waiver when a Branch Vision Contract Snapshot is required
- evidence digestion into the authority record

Exit:

- required interactive or manual evidence is green
- required UI audit exists when applicable
- exact normal USER desktop runtime launcher validation is passing or explicitly waived for desktop/user-facing behavior
- troubleshooting launcher equivalence, when used, has USER consent and launcher parity proof
- photo/video proof is adjudicated for visible claims, and any unphotographable required claims are elevated to USER manual validation or explicit waiver
- required user-facing desktop shortcut validation is `PASS` or explicitly `WAIVED` before User Test Summary handoff; `User-Facing Shortcut Validation Pending` must not remain active
- returned evidence is digested into canon
- required User Test Summary results are `PASS` or explicitly `WAIVED`; `User Test Summary Results Pending` must not remain active
- no unresolved validation contradiction remains

### PR Readiness

Purpose:

- first determine whether the branch is package-ready for PR creation without leaving merged canon stale and with the next lane already locked
- then validate the created PR as the actual merge candidate before reporting PR Readiness green

Allowed:

- readiness review
- merge-target canon sync
- final drift checks
- next-workstream confirmation
- successor-branch absence verification
- Branch Readiness branch-creation deferral
- Governance Drift Audit
- PR material preparation
- PR creation
- PR state validation

Repo-wide governance or workflow-policy repairs discovered during Branch Readiness or PR Readiness require an explicit package/carrier decision before Codex edits files unless that repair was already part of the approved package. The decision must classify the repair, identify the cleanest carrier, state what current authorization covers, list pending USER decisions, name any stop/report condition, and either record why the current branch may legally carry the repair or stop with the exact USER decision needed for a separate carrier. Small tightly coupled repairs may ride the current legitimate carrier only when the current phase authorization covers them, source truth records the carrier decision, and the repair does not expand runtime/product scope.

Forbidden:

- implementation
- hardening
- release tagging
- skipping governance drift review
- reporting PR Readiness GREEN before PR creation and PR validation

Required evidence:

- branch-local proof complete
- validation adequacy review complete under `Docs/validation_helper_registry.md`: helper/validator PASS/GREEN output supports the decision but does not replace Codex responsibility, source-truth review, changed-file inspection, review-bundle freshness, phase-scope checks, or USER-approved acceptance criteria
- accepted vision and accepted branch plan satisfied, revised, waived, or folded down with explicit receipt when a Branch Vision Contract Snapshot is required
- required user-facing desktop shortcut validation digested, passing or explicitly waived, and no `User-Facing Shortcut Validation Pending` blocker
- required User Test Summary results digested, passing or explicitly waived, and no `User Test Summary Results Pending` blocker
- merge-target canon completeness gate passed
- when selected-next truth is explicitly in scope, next workstream selected, canon-defined, assigned valid record state, minimally scoped, and explicitly not branched yet
- when selected-next truth is explicitly in scope, successor branch creation deferred to `Branch Readiness`
- post-merge truth fully encoded before merge
- Governance Drift Audit completed
- docs sync complete and validator-aligned
- inclusion-only `## PR Creation Details` operator copy blocks prepared, plus standardized `## Next Branch` response block only when selected-next truth is explicitly in scope or Branch Readiness is the next legal phase
- clean worktree with required branch truth durable in commit history
- GitHub PR created for the current head branch and intended base branch
- PR exists, is open, non-draft, conflict-free, and inspectable
- PR state matches merge-target canon
- unresolved Codex comments/issues and requested changes are absent or resolved
- branches that still rely on branch-authority truth merge with historical or removed branch-authority truth rather than lingering as active branch owners on `main`
- no active seam
- no unresolved blocker that should have been repaired on the current branch before merge
- no validator/helper result was accepted or patched by inertia; any failed, blocked, red, or suspiciously green helper result was diagnosed as source-truth drift, product/runtime defect, environment/configuration issue, USER decision need, or proven helper defect before repair

Exit:

- PR exists and is validated as ready for merge review
- or returned to the failed earlier phase with explicit blockers

### Release Readiness

Purpose:

- determine whether merged or merge-ready truth is ready for release packaging

Allowed:

- release review
- release notes, tag, title, and release package information
- version or tag recommendations
- final release-candidate verification
- release-state confirmation immediately after release execution

Forbidden:

- implementation
- broad canon-sync mutation that should have been completed before PR green
- hidden fix work
- hidden next-lane planning
- branch-authority cleanup that should have been merge-safe in PR Readiness
- stale/old branch deletion, worktree removal, branch switching, or GitHub Desktop-bound worktree cleanup; Release Readiness may record `Branch Cleanup Plan:` and `Branch Cleanup Execution Gate:` only
- between-branch canon repair
- source, docs, canon, validator, helper, release-note, or handoff-file mutation

Required evidence:

- merged or legitimately merge-ready truth
- public release language translates accepted user-facing vision/scope and excludes future-gated vision items when a Branch Vision Contract Snapshot is part of the release window
- `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, and `Candidate Includes Later Governance Repairs:` for the selected release candidate
- `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, and `FAM Contributor Routing:` for the selected release candidate
- explicit `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:` markers for release-bearing branches
- or explicit `Release Branch: No` only for preserved historical records
- release-context verification
- clean tracked-file state; any required file update must be routed back to `PR Readiness` before merge or to the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge
- no unresolved blocker

Exit:

- ready for release packaging
- or returned to the failed earlier phase with explicit blockers

### Post-Release External Operational State Carry-Forward

After Release Readiness Stage 2 publishes a GitHub prerelease and post-publish release/tag/body/health validation is green, external operational records that still point to the just-closed branch, PR, release window, selected-next state, or previous source commit are normal carry-forward, not a Release Readiness blocker, when Git/GitHub/repo validators prove the release is published and merged repo source truth is already aligned.

Codex may reconcile that external operational carry-forward in the same bounded RR2 post-release closeout without a separate USER decision when the reconciliation only updates `C:\Nexus Governance State` to match live Git/GitHub/repo truth and does not mutate repo source files, create branches or PRs, merge, release again, clean branches or worktrees, or touch FAM/runtime/private/provider/cache/memory surfaces.

If not reconciled during RR2, Branch Readiness Stage 1 must report `Post-Release External State Carry-Forward:` as a normal check and Branch Readiness Stage 2 must reconcile it before branch/worktree setup or implementation. It becomes `External Operational State Conflict` only when the stale external state conflicts with Git/GitHub/repo validation, changes the legal next carrier, requires repo source-truth mutation, requires branch/worktree cleanup, or could permit runtime/FAM/private work from stale authority.

## Thread Launch / Write-Target Identity Lock

Before meaningful repo work, file mutation, phase entry, branch/worktree creation, commit, push, PR creation, release action, runtime validation, shortcut mutation, provider/model installation, or GitHub Desktop handoff, Codex must verify the active chat lane, local workspace path, git root, branch, upstream, `HEAD`, `origin/main`, `git worktree list`, clean state, worktree role, expected phase/seam, and intended write target.

When relevant, the lock must also verify runtime/process ownership and GitHub Desktop folder binding.

Assigned parallel worktree mode is allowed when USER explicitly assigns different Codex threads to different active branch worktrees. The default limit is two active branch worktrees. Each assigned worktree must have one owning thread, one branch, one write target, one worktree ownership ledger, one intended write set, and one source-truth owner set. A third active branch worktree, unknown active thread owner, unknown write target, missing worktree ownership ledger, same-worktree/same-branch collision, dirty-worktree ownership ambiguity, or overlapping same-file/source-truth-owner mutation is `Parallel Worktree Coordination Missing` until USER routes the work.

An assigned thread may also be in `Waiting For Updated Main` posture. This is valid when that thread is in Release Readiness analysis, Branch Readiness Stage 1 analysis, or another file-freeze analysis state and is waiting for a different branch to merge before creating or continuing its branch. A waiting thread is not an active mutation carrier; it must remain read-only, must not create a branch from stale source truth, and must rerun preflight after `origin/main` updates.

Before mutation in assigned parallel worktree mode, each thread must report:

- assigned thread / worktree owner
- Active Thread Owner:
- Thread Assignment Status:
- Worktree Ownership Ledger:
- Intended Write Set:
- Same Worktree / Same Branch Collision Check:
- Dirty Worktree Collision Check:
- Dirty Worktree Recovery Packet:
- Off-Worktree Work Routing:
- Governance Routing Barrier:
- New Worktree Decision Gate:
- expected path, git root, branch, upstream, `HEAD`, and `origin/main`
- worktree role and phase/seam
- intended write target and source-truth owner
- changed-file set and shared-file overlap forecast against the other active worktree
- clean/dirty state, ahead/behind state, merge forecast, and open PR state
- runtime/process ownership and interactive validation ownership
- Git operation ownership
- GitHub Desktop binding when Desktop is used
- waiting status if the assigned lane has no created branch yet and is blocked on updated `origin/main`

Only one related Git operation should run at a time where practical, and only one interactive desktop validation may run at a time. If a branch needs a shared source-truth file already being edited by the other assigned worktree, or if two Codex threads target the same worktree/branch, stop and surface the coordination decision before patching.

If the active folder, branch, upstream, worktree role, phase/seam, write target, runtime/process owner, or GitHub Desktop binding does not match the requested work, `Thread / Worktree Identity Mismatch` blocks entry and Codex must return a routing packet instead of mutating files.

The routing packet must include expected workspace, actual workspace, expected branch, actual branch, expected write target, actual write target, expected phase/seam, actual repo state, mismatch evidence, and safest next correction.

If the requested work belongs outside the assigned worktree, outside the active branch scope, or to another active lane, Codex must stop on `Governance Routing Barrier` and route the packet to `C:\Nexus Worktrees\Governance` on `feature/release-readiness-source-truth-intake`. Governance decides whether the work belongs to the current owner, an existing worktree/thread, a new worktree/thread, or a USER waiver. New worktree/thread creation, activation, reassignment, and GitHub Desktop repo binding remain blocked on `New Worktree Decision Gate` until USER approves the exact path, branch, owner, and validation route.

### Assigned Worktree Confinement

Assigned Worktree Confinement is mandatory once a thread is assigned to a specific worktree. The thread must treat that worktree root as its boundary for repo mutation, branch operations, runtime launch, shortcut mutation, provider/model install, PR work, release work, and GitHub Desktop handoff.

Codex App Thread Worktree Guard Rule:

- Rule Name: `Codex App Thread Worktree Guard`
- Owner: `Docs/phase_governance.md`; compact mirrors may live in `Docs/development_rules.md`, `Docs/codex_modes.md`, `Docs/worktree_slots.md`, `Docs/governance_efficiency_operating_model.md`, and `Docs/validation_helper_registry.md`
- Applies To: Codex App threads, local Codex hook policy, assigned worktree preflight, branch/worktree mutation, Git operations, packet generation, helper execution that writes files, external-state mutation, and GitHub Desktop handoff
- Required State: a Codex App thread that is assigned to a worktree must bind mutation authority to the assigned Git root/worktree, not to the exact branch. The thread may switch or create branches inside that assigned worktree only when normal source truth and USER approvals allow it. The thread may inspect sibling worktrees read-only for audit, overlap, rebaseline, or routing analysis. It must not mutate a sibling worktree, parked worktree, neutral main, external operational state, or USER-local Codex state unless the current phase and USER approval explicitly admit that target.
- Allowed Values: `Assigned Root Mutation Allowed`, `Read-Only Cross-Worktree Analysis`, `First Binding Requires USER Confirmation`, `Worktree Escape User Waiver Granted`, `External Hook State Only`, `Reference Hook Template Only`
- Invalid Values: `Mutate Any Worktree From Current Thread`, `Governance Mutation From Non-Governance Worktree`, `Sibling Worktree Packet Generation`, `Sibling Worktree Git Operation`, `External Lock Ledger In Repo Docs`, `Hook Installed By Repo Patch`, `Branch-Specific Lock Only`
- Blocking Condition: `Codex Thread Assigned Worktree Mismatch`, `Worktree Escape User Waiver Missing`, `Governance Worktree Mutation From Non-Governance Root`, `Codex Hook Live State In Repo`, or `Thread First Binding Unconfirmed` blocks mutation when the assigned root is missing, current root differs from assigned root, a non-Governance thread attempts Governance-owned mutation, live hook/lock/audit state is being committed as repo truth, or an existing thread has not reported its first binding before mutation.
- Repair Owner: assigned thread for preflight/reporting; standing Governance intake for durable policy repair; USER for first-binding confirmation, worktree escape waiver, hook installation, live lock storage, or local Codex configuration mutation.
- Repair Path: stop before mutation, report assigned root, actual root, target root, intended command class, read/write mode, waiver state, and safest routing path. Continue read-only analysis if useful. Mutation may resume only in the assigned worktree, through the standing Governance worktree when Governance owns the repair, or after USER grants a bounded waiver naming source root, target root, branch, command/file scope, expiration or stop condition, validation proof, and return path.
- USER Decision Required: required before installing or modifying `C:\Users\anden\.codex\hooks.json`, local hook scripts, thread lock files, waiver files, audit logs, external operational state schemas, sibling worktree files, neutral main files, or any reference hook template/code in the repo.
- Validation Owner: `dev/orin_branch_governance_validation.py --worktree-confinement-gate` owns marker-first source checks after helper updates are approved; any future local hook is USER-local operational enforcement and is not clean-clone repo validation.
- Final Disposition: repo source truth owns durable policy and optional future reference-template guidance only. Installed hook state, per-thread lock records, waiver records, and audit logs are local Codex operational state outside the repo.

Every assigned branch authority record must carry:

- Assigned Worktree Confinement: Required
- Active Thread Owner:
- Thread Assignment Status:
- Worktree Ownership Ledger:
- Intended Write Set:
- Same Worktree / Same Branch Collision Check:
- Dirty Worktree Collision Check:
- Dirty Worktree Recovery Packet:
- Off-Worktree Work Routing:
- Governance Routing Barrier:
- New Worktree Decision Gate:
- Expected Worktree Root:
- Actual Worktree Root:
- No Cross-Worktree Mutation: Required
- GitHub Desktop-bound worktree:
- Worktree Escape User Waiver: Granted only when USER explicitly names the expected root, actual root, target root, allowed commands/files, expiration or stop condition, required validation, and return path
- Worktree Escape User Waiver Missing: Blocks mutation, branch/worktree changes, runtime launch, shortcut/provider/model actions, PR/release actions, and GitHub Desktop handoff outside the assigned worktree

Read-only identity checks may inspect `git worktree list`, remotes, branch names, dirty-file inventory, and GitHub Desktop binding evidence from the assigned root. Any write, branch switch, cleanup, runtime launch, shortcut edit, or helper execution against a sibling worktree or parked clone is `No Cross-Worktree Mutation` scope and must stop on `Worktree Escape User Waiver Missing` unless the USER grants the waiver in clear text.

Dirty worktree collision recovery is mandatory when a target worktree is dirty before a new owner claims it. Freeze mutation, inventory dirty files, identify which thread owns each file, preserve or discard only with USER approval, and resume with exactly one active owner recorded in the worktree ownership ledger.

Off-worktree work routing is mandatory when a branch thread discovers work that does not belong to its assigned worktree or active branch. The discovering thread reports the issue, expected/actual identity, dirty-file risk, likely owning lane, and recommendation, then waits. It must not self-activate a sibling worktree, take over another active thread's branch, or create a new worktree by convenience.

The active thread must run or report the equivalent of `python dev\orin_branch_governance_validation.py --worktree-confinement-gate` before Stage 2 execution, phase entry, branch/worktree creation, commit, push, PR work, release work, runtime validation, or GitHub Desktop handoff when the assigned branch record declares a worktree.

### Family-Scoped Branch Readiness Confinement

Family-scoped Branch Readiness must keep the requested family and worktree as the selector. The active branch record must name `Target Family:` and `Sibling Worktree Candidate Exclusion:` before Stage 2 mutation. Sibling worktrees are overlap context only; they are not successor authority, selected-next authority, or a reason to switch lanes unless USER explicitly broadens the task to repo-wide branch selection.

If a sibling worktree appears to have an active branch, cleaner validation state, or a tempting next phase, the assigned thread must report it as overlap/reconciliation context only. If current source truth truly conflicts with the requested family/worktree, stop on `Family-Scoped Branch Readiness Drift` and return the routing conflict instead of recommending or entering the sibling branch.

Stale parked branches, old worktrees, fallback folders, AI Lab context, deleted/recreated historical refs, and unknown write targets are stop conditions until USER explicitly routes the work to a legal target.

## Repo-Level State: No Active Branch

`No Active Branch` is the repo-level state when no runtime, implementation, release packaging, or repair lane is currently selected for normal product work. It does not deactivate the single `Standing Governance Intake Branch`; `feature/release-readiness-source-truth-intake` may remain the only active authority record while merged-main product state is still `No Active Branch`.

Use it when:

- the repo-level admission gate is failing
- merged canon drift remains unresolved
- release handling remains unresolved and USER has explicitly waived/deferred selected-next branch/workstream truth
- the only available implementation branch is stale, merged, or identical to `main`
- no branch should open yet by inertia even though repo truth is otherwise stable

`No Active Branch` may be:

- blocked:
  - a blocker or repair path must be cleared before the next implementation lane may begin
- steady-state:
  - no implementation branch is currently selected, and it is valid for the next safe move to be no branch at all until a new approved need exists. PR Readiness may project steady-state `No Active Branch` when no USER-approved selected-next truth exists; it must not invent selected-next truth or create a successor branch by inertia. The next runtime implementation pipeline is selected later through Branch Readiness Stage 1 from current `origin/main`, external operational state, vision, current completed work, and implementation need.

When `No Active Branch` is blocked:

- do not recommend a later branch phase
- do not start next-lane implementation
- report the blocker and the exact repair path instead

When `No Active Branch` is steady-state:

- do not start the next implementation branch by inertia
- it is valid for `Next Safe Move` to say explicitly that no branch should open yet
- a release packaging branch may still enter `Branch Readiness` if its branch-class admission rules pass
- governance-only branches are not used; governance or canon repair must ride on the next legitimate runtime-focused backlog branch's `Branch Readiness`, except for the single `Standing Governance Intake Branch` defined below
- `Docs/branch_records/index.md` must contain no active runtime, implementation, release packaging, or repair authority records; the only active-authority exception is `Docs/branch_records/feature_release_readiness_source_truth_intake.md`

## Standing Governance Intake Branch

Purpose:

- keep Release Readiness file-frozen while routing source-truth drift that Release Readiness discovers to one governed repair lane

Allowed:

- one standing worktree: `C:\Nexus Worktrees\Governance`
- one standing branch: `feature/release-readiness-source-truth-intake`
- one standing active authority record: `Docs/branch_records/feature_release_readiness_source_truth_intake.md`
- one intake source: `Release Readiness digest` for release-blocker repair, plus USER-approved `automation/worktree governance intake` only when the issue is non-runtime, multi-worktree safety related, plus USER-approved `phase-gate governance intake` only when a live branch exposes a repeatable non-runtime phase-gate miss; every intake remains held to the same one-cycle, PR-gated contract
- one cycle ID format: `RRI-YYYYMMDD-NNN`
- `One Active Cycle`: only one active `RRI-*` cycle may be in progress; additional digests queue
- `Sync Rule`: before each new intake, the standing branch must be clean and match current `origin/main`
- `Pre-Rebaseline Impact Audit`: before the standing branch or neutral main workspace fast-forwards to updated `origin/main`, report the incoming change set, incoming changed files, current worktree changed files, branch changed files, `Rebaseline Overlap Files:`, runtime/source-truth risk, validation before rebaseline, recommendation only posture, approval status, mutation status, and `Rebaseline Overlap Intent Gate` result when overlap exists
- `Bootstrap Exception Limit`: the one-time setup exception authorizes only the initial branch/worktree bootstrap while `origin/main` still equals the recorded branch creation base; after setup PR merge or any `origin/main` movement, ahead-of-main work requires an active `RRI-*` cycle sourced from a Release Readiness digest, USER-approved automation/worktree governance intake, USER-approved phase-gate governance intake, or same-PR bot-review repair on the standing governance PR
- source-truth/governance/validator drift repair named by the intake digest
- a post-merge `Return Digest` to the originating worktree/thread with concrete originating branch/worktree identity copied from the accepted intake and `Neutral Main Workspace Rebaseline:` proof for `C:\Nexus Desktop AI`
- Release Readiness blocker digests that discover stale active branch authority, stale phase wording, stale PR Readiness wording, selected-next ambiguity, release-window contributor ambiguity, or `No Active Branch` conflict must explicitly say `Governance Intake Routing: send this to C:\Nexus Worktrees\Governance on feature/release-readiness-source-truth-intake`
- automation observability repair only for configured cwd/worktree identity, stale neutral-main detection, lane-sensitive prompt drift, and automation memory/reporting mismatch; `Automation CWD Worktree Mismatch` must be reported before an automation finding becomes source-truth work
- PR Readiness Stage 1 for this standing branch may report `Pre-PR Live State: No live PR` while the previous governance PR remains historical merge proof; the reusable branch name must not cause a closed historical PR to be treated as the current live PR. Standing governance PRs do not select runtime successor workstreams, create runtime branches, or admit packages.

Forbidden:

- runtime/provider/model/memory/voice/Core/shortcut/installer implementation
- release execution, tags, GitHub Releases, release artifacts, or release-note publication
- GitHub issue creation, AI Product Contract import, private Dev ORIN import, direct-main mutation, broad docs churn, or next runtime branch creation
- accepting anything other than a Release Readiness digest, USER-approved automation/worktree governance intake, USER-approved phase-gate governance intake, or same-PR standing-governance bot-review repair after the one-time bootstrap setup
- widening an automation/worktree governance intake into runtime, implementation, release-execution, stale-branch deletion, worktree cleanup, or FAM-006/FAM-007 mutation

Originating-lane pause:

- when a Release Readiness blocker is handed off, the originating thread/worktree enters `Waiting For Governance Intake` or `Waiting For Updated Main`
- that lane must not mutate repository files until the governance PR merges, the standing branch syncs to `origin/main`, the `Return Digest` arrives, and the originating lane fetches/revalidates updated `origin/main`

The `Return Digest` must include the originating branch/worktree, operating workspace, expected branch, `RRI-*` cycle ID, governance PR, merge commit, updated `origin/main` commit, `Neutral Main Workspace Rebaseline:`, `Pre-Rebaseline Impact Audit:`, files changed, blockers cleared/remaining, validations, rebaseline instructions, and `Next Legal Phase`. After any standing-governance PR merge, Codex must first run and report the `Pre-Rebaseline Impact Audit`, then either fast-forward `C:\Nexus Desktop AI` on `main` to the updated `origin/main` commit after approval and record the proof, or report the blocker that prevents that rebaseline before claiming the governance lane is idle.

Return-digest identity guard:

- the originating branch and originating worktree must be copied exactly from the accepted Release Readiness intake digest or recorded `RRI-*` cycle identity
- the originating-lane prompt must name that exact worktree as the operating workspace and must name the expected branch
- the governance lane must not infer the originating workspace from `C:\Nexus Worktrees\Governance`, `C:\Nexus Desktop AI`, GitHub Desktop's selected repository, or the current shell CWD
- `Return Digest Origin Identity Missing` blocks the handoff when the originating branch, originating worktree, operating workspace, or expected branch is absent, generic, contradictory, or inferred
- `Thread / Worktree Identity Mismatch` blocks originating-lane continuation if the return digest points to a different branch/worktree than the accepted intake recorded

## Governance Intake Triage And Digest Profiles

Broad governance/source-truth/process reform must use `Docs/governance_intake_triage_and_digest_profiles.md` before it mutates source truth, unless a Release Readiness intake digest already names exact blockers, carrier, files, and approval boundaries. The canonical packet name is `Governance Intake Triage Packet`.

The required governance intake triage packet fields are `Problem Class:`, `Source-Truth Support:`, `Current Approval Coverage:`, `Recommended Carrier:`, `Smallest Safe Repair:`, `Files Likely Affected:`, `Validator / Helper Impact:`, `Runtime / Product Risk:`, `Active Branch / Worktree Interaction:`, `PR / Merge Need:`, `Deferred Items:`, `Stop / Report Conditions:`, `Recommended Digest Profile:`, and `Exact USER Decision Needed:`.

Codex must choose the smallest legal digest profile for the phase: `Decision Packet`, `Return Digest`, `Validation Digest`, `Full Audit Packet`, or `Delta Digest`. A `Full Audit Packet` is reserved for explicit broad audits, process reform, root-cause analysis, or repo-wide recommendations. Normal phase handoffs should not restate full governance when changed values, blockers, validation, and `Next Legal Phase` are enough.

Digest non-compaction is mandatory. Choosing the smallest legal digest profile selects the packet shape only; it does not authorize Codex to compact, collapse, omit, or replace any required digest field, USER-requested review detail, blocker detail, validation proof, file list, decision matrix, changed-surface evidence, or exact next-decision wording. When USER asks for a full digest, review digest, complete breakdown, file-by-file packet, line-referenced packet, or any explicitly detailed output, Codex must return the complete digest and may not compact the digest ever.

## Exception Path: Post-Release Canon Repair

Purpose:

- classify escaped canon drift after a release without turning Release Readiness into a mutation phase or using `main` as a work surface
- keep external operational state carry-forward separate from durable repo canon drift

Allowed:

- read-only drift analysis on `main`
- blocker annotation when drift is discovered after merge
- repair in the next legitimate runtime-focused backlog branch's `Branch Readiness` before implementation
- repair in the next approved Branch Readiness Stage 2 canon/governance carrier when release publication has completed and protected `main` prevents post-release canon closure from landing directly

Forbidden:

- treating post-release canon repair as a Release Readiness mutation phase or standalone cleanup lane instead of a standard PR Readiness / next Branch Readiness Stage 2 checkpoint
- treating normal post-release external operational state carry-forward as durable repo canon drift or as a Release Readiness blocker when Git/GitHub/repo validation is green
- using post-release repair instead of the merge-target canon completeness gate
- turning the repair path into a new implementation lane by accident
- opening a governance-only branch
- opening a repair-only feature branch
- treating a local-only post-release closure commit as completed source truth
- using Release Readiness as a broad docs-sync phase
- mutating `main`

Required evidence:

- updated `main`
- latest release truth
- explicit canon drift
- explicit reason the drift could not be prevented before merge or release
- explicit legal repair surface: next legitimate runtime-focused backlog branch's `Branch Readiness`
- if protected-main release closure is the blocker, explicit legal repair surface: the next approved Branch Readiness Stage 2 canon/governance carrier that carries the closure into remote source truth

Exit:

- canon aligned to released truth
- remote source truth contains the post-release closure, not only a local commit
