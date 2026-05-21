# Governance Process Efficiency Reform Plan

## Purpose

This source-truth planning record captures a repo-wide governance and source-truth audit focused on reducing execution errors, reducing prompt/token load, and improving branch-output quality without weakening the safety gates that protect the multi-worktree workflow.

This plan is not an implementation branch by itself. It is a reform inventory for later focused planning packets and USER-approved governance passes.

## Audit Snapshot

- Audit date: 2026-05-19.
- Audit carrier: `C:\Nexus Worktrees\Governance` on `feature/release-readiness-source-truth-intake`.
- Source-truth baseline: `origin/main` at `81701d4b351ae7bb4c146daf88a8d884f6bc7981`.
- Validation baseline before recording this plan:
  - `python dev\orin_branch_governance_validation.py`: PASS, 5757 checks.
  - `python dev\orin_branch_readiness_planning_fixture_validation.py`: PASS.
  - `python dev\orin_release_body_validation.py`: PASS, 37 published pre-Beta release bodies.

## Reform Principles

- Preserve safety before speed. Any compaction must keep protections for protected `main`, Release Readiness file freeze, multi-worktree identity, pre-rebaseline audit, branch-local authority, and PR/release body firewalls.
- Reduce duplicated prose first. Repetition across `Docs/phase_governance.md`, `Docs/development_rules.md`, `Docs/codex_modes.md`, `Docs/orin_task_template.md`, `Docs/codex_user_guide.md`, and `Docs/Main.md` is the largest token-cost driver.
- Prefer small reform passes. Each category below should become a focused planning packet or branch pass instead of one broad rewrite.
- Keep canonical names stable until aliases are proven. User-facing aliases can reduce confusion, but validators should keep the current canonical phase enum until a deliberate rename migration is approved.
- Let validators enforce markers and let docs explain intent. Long policy paragraphs should shrink into canonical rule IDs, packet templates, and validator-backed marker sets.
- Separate derived live truth from governance receipts. Git/GitHub and approved helpers should derive volatile facts such as `HEAD`, PR state, tags, releases, dirty state, and merge base; docs should record intent, USER decisions, receipts, and historical interpretation.

## Category 1: Governance Doc Compaction

Current finding:
- The same top rules and phase contracts are repeated across multiple large docs.
- `Docs/phase_governance.md`, `Docs/development_rules.md`, `Docs/codex_modes.md`, `Docs/orin_task_template.md`, and `Docs/codex_user_guide.md` all carry overlapping versions of Pre-PR Durability, Release Readiness file freeze, Release Candidate Anchor, Pre-Rebaseline Impact Audit, Branch Readiness planning, Runtime Branch Engineering Contract, PR Readiness, and Standing Governance Intake rules.
- This makes prompts expensive and increases drift risk because a future repair can update one owner while missing another mirror.

Recommendation:
- Adopt a `Rule ID + owner + compact mirror` model.
- Keep full normative policy in `Docs/phase_governance.md`.
- Convert other docs to short pointers plus only the minimal operational fields they uniquely need.
- Add a "do not duplicate full policy prose" rule for future governance edits.

Focused planning pass:
- `Governance Doc Compaction Pass`.
- Preserve validator-required phrases until validators are updated to source-check the new IDs.

Priority:
- High.

## Category 2: Phase Naming And User-Facing Aliases

Current finding:
- Current canonical names are precise but user-heavy, especially the Stage 1 / Stage 2 pairs.

Recommendation:
- Preserve canonical phase enum for validator stability.
- Add optional user-facing aliases:
  - `Branch Readiness Stage 1` -> `Plan Review`.
  - `Branch Readiness Stage 2` -> `Setup / Admission`.
  - `Workstream` -> `Build`.
  - `Hardening` -> `Stabilize`.
  - `Live Validation` -> `User Proof`.
  - `PR Readiness Stage 1` -> `Merge Readiness Audit`.
  - `PR Readiness Stage 2` -> `PR Execution / Watch`.
  - `Release Readiness` -> `Release Validation`.
  - `Standing Governance Intake` -> `Policy Repair Lane`.

Focused planning pass:
- `Phase Alias UX Pass`.

Priority:
- Medium.

## Category 3: Packet And Digest Slimming

Current finding:
- Phase digests can become full governance restatements.
- The user usually needs changed values, blockers, validation, and next legal phase rather than a complete policy replay.

Recommendation:
- Define digest profiles:
  - `Decision Packet`: only facts needed for USER approval.
  - `Return Digest`: worktree-specific unblock packet with exact identity and next legal phase.
  - `Validation Digest`: commands, results, failures, and residual risks.
  - `Full Audit Packet`: only for explicit audit/planning requests.
  - `Delta Digest`: changed values since last accepted packet.
- Require default final responses to use the smallest legal profile that satisfies the phase.
- Keep detailed source truth in docs, not in every chat output.

Focused planning pass:
- `Digest Profile Standardization Pass`.

Priority:
- High.

## Category 4: Branch Readiness Planning Quality

Current finding:
- Recent repairs added strong Branch Readiness planning requirements and Runtime Branch Engineering Contract enforcement.
- The quality gate is good, but the required packet is now large enough that USER critique can become harder, not easier.

Recommendation:
- Split Branch Readiness planning into:
  - `Product Intent Summary`.
  - `Engineering Contract`.
  - `Decision Ledger`.
  - `Deferred/Future Ledger`.
  - `Implementation Sequence`.
  - `Proof Plan`.
- Keep validator markers, but let the user-facing packet summarize each section and link to source-truth details.
- Add a planning critique checklist focused on system shape, scope, expected user-facing behavior, and rejected shallow plans.

Focused planning pass:
- `Branch Planning UX And Template Pass`.

Priority:
- High.

## Category 5: Multi-Worktree Identity And Rebaseline Safety

Current finding:
- Identity and Pre-Rebaseline Impact Audit rules are now strong.
- Each thread still has to manually construct the same audit packet before rebaseline.

Recommendation:
- Create or extend a reusable no-mutation `dev/orin_worktree_rebaseline_audit.py` helper.
- It should output current cwd, git root, worktree role, branch, upstream, HEAD, origin/main, merge base, incoming commits, incoming changed files, local changed files, shared surface overlap, active branch record identity, current-main reconciliation identity guard recommendation, and safe operation recommendation.

Focused planning pass:
- `Worktree Rebaseline Audit Helper Pass`.

Priority:
- High.

Implementation record:
- Focused pass admitted `dev/orin_worktree_rebaseline_audit.py` as a reusable report-only helper.
- The helper emits the required `Pre-Rebaseline Impact Audit:` and `Current-Main Reconciliation Identity Guard:` markers without fetching, merging, rebasing, checking out, resetting, or mutating files.
- The helper emits `Rebaseline Mutation Approval:` and `Rebaseline Mutation Status:` so every baseline request remains report-only until USER approves mutation.
- Bot-review hardening requires incoming changed files to compare `merge_base..target_ref`, branch changed files to compare `merge_base..HEAD`, and active authority matching to use the exact `- Branch:` field instead of substring matching.
- Registry owner: `Docs/validation_helper_registry.md`.
- Validator source-check owner: `dev/orin_branch_governance_validation.py`.

## Category 5A: Source-Truth Ownership And Worktree Slot Model

Current finding:
- The repo has moved from one neutral folder to a multi-worktree workflow, but old language can make current FAM worktrees look like permanent structural lanes.
- Backlog and roadmap carry too many current-state mirrors, while Git/GitHub already own many volatile operational facts.
- Without a stable slot model, branch identity, GitHub Desktop binding, and originating-lane prompts can drift between current family labels and actual worktree roles.

Recommendation:
- Adopt `Docs/worktree_slots.md` as the slot registry and intended assignment layer.
- Use stable slot IDs: `neutral-main`, `governance-standing`, `runtime-active-1`, `runtime-active-2`, `runtime-active-3`, and `archived-historical`.
- Make the slot registry own intended assignment receipts, not raw live Git facts.
- Keep branch authority records as the legal source for active, historical, blocked, waiting, and next-phase posture.
- Keep Branch Runtime Engineering Plans canonical while runtime branches are active, then fold down or promote them during PR Readiness.

Focused planning pass:
- `Source-Truth Ownership And Worktree Slot Model Pass`.

Priority:
- High.

Implementation record:
- Focused pass admitted `Docs/worktree_slots.md` as the stable worktree slot registry.
- `Docs/Main.md` now distinguishes derived live truth from governance receipts and routes worktree slot ownership through `Docs/worktree_slots.md`.
- `Docs/branch_records/index.md` records that slot assignment does not equal active branch authority.
- Hard validator enforcement, helper implementation, backlog/roadmap migration or shrink work, duplicate-live-state detection, and shared-surface ownership enforcement remain deferred to later USER-approved reform passes.

## Category 6: Standing Governance Intake Simplification

Current finding:
- The standing Governance branch now correctly avoids closeout-only PRs.
- Remaining complexity comes from RRI cycle wording, return digest identity, neutral main rebaseline proof, and historical ledger text.

Recommendation:
- Move detailed historical RRI cycle entries into a compact ledger table or appendix.
- Keep the active record focused on active cycle, latest closed cycle, allowed intake source, sync status, return digest status, and next legal phase.
- Preserve validator enforcement for one-active-cycle and return digest identity.

Focused planning pass:
- `Standing Governance Ledger Compaction Pass`.

Priority:
- Medium-high.

## Category 7: PR Watcher And Bot-Review Repair Loop

Current finding:
- Governance requires watchers and same-PR bot-review repair, but the actual user experience still feels unreliable.
- When automation delivery is quiet, the user cannot tell whether the watcher is idle, stuck, or lacking actionable data.

Recommendation:
- Standardize watcher modes:
  - `Silent Monitor`.
  - `Verify Once`.
  - `Repair Mode`.
  - `Blocked Mode`.
- Add a watcher health proof line to PR Readiness Stage 2 final handoff with configured cwd, PR number, head SHA, unresolved thread count, latest bot review time, repair authority status, and delivery route proof.
- Consider a local watcher helper enhancement before relying only on native heartbeat text.

Focused planning pass:
- `Watcher Reliability And Repair-Mode Pass`.

Priority:
- High.

Implementation record:
- Focused pass admitted `Docs/pr_watcher_mode_contract.md` as the compact PR Watcher Mode Contract.
- The standard defines `Silent Monitor`, `Verify Once`, `Repair Mode`, and `Blocked Mode` so quiet watcher behavior, one-time proof, safe same-PR repair, and no-patch blockers are no longer ambiguous.
- The required `Watcher Health Proof:` line records configured cwd, PR number, head SHA, unresolved review-thread count, latest bot review, repair authority, delivery route proof, runtime proof, and next watcher posture before PR Readiness Stage 2 final handoff can be green.
- Follow-up approval-default repair clarifies that USER approval for PR Readiness Stage 2 / PR creation includes watcher provisioning by default. Codex must not ask for a separate watcher-specific approval after Stage 2 is approved; skipping watcher provisioning requires an explicit USER watcher waiver or documented platform/runtime blocker.
- Validator source-check owner: `dev/orin_branch_governance_validation.py`.

## Category 8: Validator Modularization

Current finding:
- `dev/orin_branch_governance_validation.py` is the enforcement center and is very large.
- The breadth is useful, but small repairs are harder to review safely.

Recommendation:
- Split the monolith into internal modules without changing the command interface:
  - phase/base parser utilities.
  - branch authority checks.
  - worktree/rebaseline gates.
  - standing governance intake gates.
  - runtime planning contract gates.
  - PR readiness gates.
  - release readiness gates.
  - historical/source-truth migrations.
- Keep `dev/orin_branch_governance_validation.py` as the stable CLI wrapper.

Focused planning pass:
- `Governance Validator Modularization Pass`.

Priority:
- Medium-high.

## Category 9: Source-Truth Volume And Historical Archiving

Current finding:
- Several branch records mix current state, historical evidence, issue ledgers, release details, and long narrative.
- This preserves evidence but increases routine context size.

Recommendation:
- Adopt a current-state / historical-appendix split:
  - top 100-200 lines: current truth and machine markers.
  - appendix or closeout doc: detailed historical narrative and proof.
- For very large branch records, create compact current-summary sections that validators prefer.

Focused planning pass:
- `Source-Truth Archive And Current-State Split Pass`.

Priority:
- High, but risky.

## Category 10: Release Readiness Scope And Release Ownership

Current finding:
- Release Readiness is file-frozen and validates current `origin/main` by default.
- Multi-FAM merged-unreleased windows can still confuse who owns the release when FAM-006 and FAM-007 merge close together.

Recommendation:
- Add a `Release Captain / Release Assembler` concept for release execution:
  - it does not own implementation.
  - it packages the aggregated release window.
  - it lists all contributing PRs/FAMs.
  - it cannot mutate source truth during Release Readiness.
- Keep aggregated release window as default when current `origin/main` contains multiple unreleased contributors.

Focused planning pass:
- `Release Ownership UX Pass`.

Priority:
- Medium.

## Category 11: Helper Registry And Validation Runner

Current finding:
- `Docs/validation_helper_registry.md` is strong but dense.
- Validator command lists vary by branch and phase.

Recommendation:
- Add a lightweight validation runner or registry query helper:
  - input: phase, branch family, changed files.
  - output: recommended validator list and rationale.
  - no mutation.
- Split helper registry into families only if validators can still find canonical helper status.

Focused planning pass:
- `Validation Runner And Registry Query Pass`.

Priority:
- Medium.

Implementation record:
- Focused pass admitted `dev/orin_validation_suite.py` as a reusable report-only validation suite recommendation helper.
- The helper emits `Recommended Validation Suite:` packets from `--phase` and `--changed-file` inputs, recommends commands with rationale, and does not execute commands or mutate files.
- Registry owner: `Docs/validation_helper_registry.md`.
- Validator source-check owner: `dev/orin_branch_governance_validation.py`.

## Category 12: Backlog And Roadmap Current-State Clarity

Current finding:
- `Docs/feature_backlog.md` and `Docs/prebeta_roadmap.md` carry current state, release history, selected-next posture, and future candidates in dense prose.

Recommendation:
- Add a compact top-level `Current Decision Surface` block to each:
  - latest public prerelease.
  - merged-unreleased PRs.
  - active runtime branch.
  - active governance branch.
  - selected-next posture.
  - release blockers.
  - next legal phase.
- Move longer historical explanation below a stable marker.

Focused planning pass:
- `Backlog/Roadmap Current Decision Surface Pass`.

Priority:
- Medium-high.

Implementation record:
- Focused pass admitted compact `## Current Decision Surface` blocks in `Docs/feature_backlog.md` and `Docs/prebeta_roadmap.md`.
- The blocks keep `Latest Public Prerelease Recorded In Source Truth:`, `Published Release Pending Canon Closure:`, `Merged-Unreleased PRs:`, `Active Runtime Branch:`, `Active Governance Branch:`, `Selected-Next Posture:`, `Release Blockers:`, and `Next Legal Phase:` near the top so routine phase loading can avoid scanning long historical prose.
- Validator source-check owner: `dev/orin_branch_governance_validation.py`.

## Category 13: Naming And Product Identity Drift

Current finding:
- Product/persona naming governance is strict, but legacy names can still surface in old docs, runtime artifacts, validator fixtures, or generated outputs.

Recommendation:
- Keep external GitHub release/tag history as historical.
- Add a future repo-wide naming drift scan helper only when USER approves a naming cleanup carrier.
- Do not mix naming migration into runtime branches unless the branch owns the affected user-facing surface.

Focused planning pass:
- `Tracked Naming Drift Scan Pass`.

Priority:
- Medium.

## Category 14: Governance Repair Intake Triage

Current finding:
- The standing Governance branch can accept Release Readiness digests, automation/worktree governance intake, and phase-gate governance intake.
- Broad governance requests risk becoming too large.

Recommendation:
- Add a `Governance Intake Triage Packet` before every non-Release-Readiness governance reform:
  - problem class.
  - source-truth support.
  - smallest safe repair.
  - files likely affected.
  - validator/helper impact.
  - whether a PR is needed.
  - whether the repair should instead ride an active runtime branch.
- This current document can serve as the parent inventory for focused triage packets.

Focused planning pass:
- `Governance Intake Triage Template Pass`.

Priority:
- High.

## Category 15: Public Output Standards

Current finding:
- PR body and release body standards are much better now.
- The next risk is overexplaining public release notes with internal governance repair names.

Recommendation:
- Keep release bodies user-facing and avoid internal process names unless needed for transparency.
- Add public-language mapping from Engineering Contract to release notes:
  - internal scope.
  - user-visible benefit.
  - excluded/future-gated work.
  - validation confidence.
- Add a release-body dry-run preview before release execution when the release window has governance-heavy PRs.

Focused planning pass:
- `Public Language Mapping Pass`.

Priority:
- Medium.

## Recommended Reform Sequence

1. `Governance Intake Triage Template Pass`.
2. `Digest Profile Standardization Pass`.
3. `Worktree Rebaseline Audit Helper Pass`.
4. `Source-Truth Ownership And Worktree Slot Model Pass`.
5. `Watcher Reliability And Repair-Mode Pass`.
6. `Governance Doc Compaction Pass`.
7. `Branch Planning UX And Template Pass`.
8. `Source-Truth Archive And Current-State Split Pass`.
9. `Governance Validator Modularization Pass`.
10. `Backlog/Roadmap Current Decision Surface Pass`.
11. `Release Ownership UX Pass`.
12. `Validation Runner And Registry Query Pass`.
13. `Phase Alias UX Pass`.
14. `Standing Governance Ledger Compaction Pass`.
15. `Public Language Mapping Pass`.
16. `Tracked Naming Drift Scan Pass`.

## Consolidated Governance Reform Pass

USER later approved completing the remaining governance reform categories in one bounded Governance PR instead of separate focused PRs.

This consolidated pass completes the policy and validation scaffolding for:

- `Governance Doc Compaction Pass`
- `Phase Alias UX Pass`
- `Branch Planning UX And Template Pass`
- `Standing Governance Ledger Compaction Pass`
- `Governance Validator Modularization Pass`
- `Source-Truth Archive And Current-State Split Pass`
- `Release Ownership UX Pass`
- `Public Language Mapping Pass`
- `Tracked Naming Drift Scan Pass`

Implementation record:

- `Docs/governance_efficiency_operating_model.md` owns the Rule ID / owner / compact mirror model, source-truth ownership matrix, derived live truth versus governance receipt boundary, duplicate live-state guard, current-summary / historical-appendix split, phase alias UX, branch planning UX, standing-governance ledger compaction, release ownership UX, public language mapping, validator modularization boundary, validation-suite usage, naming drift scan rule, and consolidated pass completion boundary.
- `dev/orin_governance_efficiency_validation.py` validates the operating model, owner-doc pointers, and backlog/roadmap compactness against Branch Runtime Engineering Plan sprawl.
- `Docs/Main.md`, `Docs/phase_governance.md`, `Docs/development_rules.md`, and `Docs/codex_modes.md` carry compact pointers instead of duplicating the full operating model.
- `Docs/validation_helper_registry.md` registers the reusable governance efficiency validator.

Explicit non-scope:

- No broad historical branch-record migration.
- No backlog/roadmap shrink migration beyond compactness enforcement.
- No runtime implementation.
- No FAM-006 or FAM-007 mutation.
- No branch deletion, worktree cleanup, issue work, release execution, tag, GitHub Release, or artifact work.

Post-merge operating rule:

- Future governance efficiency changes should first use `Docs/governance_efficiency_operating_model.md` and `dev/orin_governance_efficiency_validation.py` before creating another live-state owner or duplicating policy prose.

## Highest-Value First Pass

Recommended first focused pass:

`Governance Intake Triage Template Pass` plus `Digest Profile Standardization Pass`.

Why:
- It is low-risk and documentation-first.
- It immediately narrows future governance requests.
- It reduces token usage before touching the huge docs or validator.
- It gives each later reform category a standard decision packet.

Suggested acceptance criteria:
- A reusable triage packet exists in source truth.
- Digest profiles are named and scoped.
- Future governance reform prompts can cite a category from this plan instead of restating all details.
- No phase enum rename, validator split, source-truth archival, or runtime work is attempted in the first pass.

Implementation record:
- First focused pass admitted: `Docs/governance_intake_triage_and_digest_profiles.md`.
- Governance source-truth pointers added to `Docs/phase_governance.md`, `Docs/development_rules.md`, `Docs/codex_modes.md`, `Docs/orin_task_template.md`, `Docs/Main.md`, `Docs/branch_records/index.md`, and `Docs/validation_helper_registry.md`.
- Validator source-check owner: `dev/orin_branch_governance_validation.py`.

## Remaining Deferred Execution Decisions

The consolidated pass records the governance model for the remaining categories, but these physical migrations remain separate USER decisions:

- large historical branch-record migration or archival
- direct modular split of `dev/orin_branch_governance_validation.py`
- branch deletion, stale worktree cleanup, or GitHub Desktop cleanup
- runtime/FAM branch mutation
- release execution or public release publication

Resolved by prior or consolidated reform passes:

- phase aliases are explanatory only; canonical phase names remain unchanged
- validation runner recommendation helper exists as `dev/orin_validation_suite.py`
- watcher approval default and watcher mode contract are recorded
- governance efficiency operating model exists as `Docs/governance_efficiency_operating_model.md`

## USER Review Intake - 2026-05-21

Scope:
- Analysis-only intake for the full Docs source-truth reform review surface.
- Preserve USER review responses from `Docs/governance_docs_reform_user_review_index.md` in this durable planning/model record so the generated review index can be regenerated safely.
- Update the model for this branch's execution without deleting, renaming, archiving, or broadly migrating Docs files in this pass.

USER response integration matrix:

| USER response requirement | Governance interpretation | Model decision | Owner files | Execution effect on this branch | Validator/helper implication |
| --- | --- | --- | --- | --- | --- |
| Complete the remaining reform in staged internal work on this same Governance carrier and one final PR; avoid revolving PRs. | The reform should not become a sequence of small PRs that each leave drift for the next one. | Keep the current carrier as the single reform branch and use internal commits/stages until USER accepts the complete cleanup. | This plan, `Docs/governance_docs_full_inventory_reform_audit.md`, `Docs/governance_docs_reform_user_review_index.md`. | The review packet must show a staged execution plan and must not present PR creation as the next automatic step while USER is still correcting the model. | `dev/orin_governance_efficiency_validation.py` must require the generated dossier/index to expose the user-response integration and single-PR staged execution sections. |
| `Docs/Main.md` should be the least-updated canonical docs index and pointer ledger. | Main is a recovery map and canonical owner index, not a live operations diary. | Main routes to owner docs and explains purpose; context docs preserve evidence and detail. | `Docs/Main.md`, `Docs/governance_efficiency_operating_model.md`. | The cleanup plan must avoid adding live branch/release/current-state ledgers to Main and must flag future Main edits that duplicate owner content. | Governance efficiency validation keeps Main as pointer/routing surface and checks for the operating model pointer. |
| Use a clearer canonical docs versus context docs model. | Some files are law/routing owners; others are evidence/history/reasoning owners. | Add canonical/context taxonomy to the model and dossier so files are not judged only by size. | Operating model, audit dossier, review index. | The file-by-file review must classify each file by owner role and disposition rather than only "keep/delete." | The docs inventory helper must generate owner category, action, consolidation target, ambiguity risk, and structure risk per file. |
| Branch plans should fold down and be retired, not deleted by default. | Planning evidence has value after merge, but it must stop acting like active authority. | Branch plans are canonical only while active; after PR Readiness they fold down, migrate durable content, and get explicit retired posture unless USER later approves deletion. | `Docs/branch_plans/README.md`, operating model, branch record index, audit dossier. | The review packet must list branch plans as fold-down/retirement candidates, not automatic delete candidates. | Planning fixture/governance efficiency validation should preserve fold-down/retirement wording and reject stale active plan authority. |
| Branch receipts may be large for traceability. Compaction for traceability is bad. | The defect is duplicate live state and poor organization, not evidence volume. | Branch records become structured traceability receipts: current summary, indexed historical sections, commit/PR/release evidence, changed-surface map, validation proof, and pointers to promoted durable owners. | `Docs/branch_records/index.md`, operating model, audit dossier. | Large branch records are organized or queued for organization, not blindly compressed. Evidence needed for future bug/rollback analysis is preserved. | Validator wording must distinguish "sprawl/live-state duplication" from legitimate historical receipt evidence. |
| Safe files should be deleted when proven safe or collapsed into current tracked files. | Delete/retire decisions require reference scan, replacement owner, and USER acceptance when ambiguous. | Every Docs file gets a disposition row: keep, organize, migrate, retire, delete candidate, or USER decision needed. | Audit dossier and generated review index. | The branch may identify delete/retire candidates now, but ambiguous deletion stays deferred until USER review. | Inventory helper must keep a full cleanup/disposition table and retirement/delete candidate table. |
| `Docs/orin_vision.md` should become/reframe as Nexus Vision and drive planning. | Product vision should be a durable product contract, not a branch execution plan. | Create a Product Vision Contract model: vision drives backlog planning and Branch Readiness recommendations; branch plans explain implementation/proof. | Operating model, audit dossier, future focused vision pass. | This pass records the decision and queues safe rename/reframe analysis; it does not rename without a focused reference update. | Future validation should prevent vision content from duplicating branch-plan implementation detail. |
| Each backlog family may need USER-reviewed vision discussion. | Family vision belongs above branch plans and should shape plan recommendations. | Backlog points to vision/family owners where needed; it does not absorb long vision/planning narratives. | Backlog, future family dossier/vision surfaces, operating model. | Dossier must record this as a future model requirement and not treat backlog compaction as erasing product intent. | Future backlog sprawl checks should allow compact vision pointers, not full branch planning. |

Corrected analysis:
- The earlier review surface underweighted the USER responses because it recorded them as a receipt, not as requirements that reshape the model. This section is the durable correction.
- The prior "delete branch plans after fold-down" wording was too aggressive and could lose useful planning evidence. The corrected model is "fold down, migrate durable content, then retire by explicit posture"; deletion requires separate USER approval.
- The prior "compact branch receipt" wording was too easy to misread as "make traceability small." The corrected model is "structured branch receipt": current summary first, indexed historical sections, commit/PR/release evidence, changed-surface map, validation proof, and promoted reusable lessons.
- Main should become more canonical and less operational. It should point to owners and explain the file system, while specific policy, branch, plan, workstream, and vision surfaces carry their own detail.
- The Docs reform should separate information by job: canonical index, policy owner, branch ledger, active plan, workstream/family history, product vision, and generated review/audit surface.
- The generated review index should not be the durable home for raw USER responses because it is regenerated by helper. This plan is the durable intake home, and the generated dossier/index must summarize how the responses changed the model.

Single-PR staged execution plan for this branch:

| Stage | Name | Purpose | Allowed work | Completion proof |
| --- | --- | --- | --- | --- |
| R1 | User-response model correction | Turn USER responses into model decisions instead of passive notes. | Update this plan, operating model, generated dossier/index, and validator-required sections. | Dossier/index contain `USER Response Integration Matrix`, `Single-PR Staged Execution Plan`, and `Disposition Changes From USER Review`. |
| R2 | Canonical/context taxonomy | Make Main the least-updated canonical docs index and classify context docs. | Update ownership model and file-by-file dossier language; no broad file deletion. | Every Docs file has owner category, action, migration target, ambiguity risk, and structure risk. |
| R3 | Backlog/roadmap enforcement model | Keep backlog as product registry/pointers and roadmap as release-stage breakpoint outline. | Harden generated schemas and validators; migrate only safe duplicated planning text already approved. | Backlog/roadmap sprawl checks stay green. |
| R4 | Branch plan lifecycle model | Keep detailed active planning but prevent stale active authority after completion. | Fold-down/retirement rules and candidate queues; no deletion without USER review. | Branch plan candidates appear as retirement candidates, not automatic deletion. |
| R5 | Structured branch receipt model | Preserve traceability without duplicate live-state chaos. | Define receipt schema and queue high-risk records for organization. | High-risk/structure queues identify oversized records and their organization action. |
| R6 | Vision contract planning | Treat `Docs/orin_vision.md` as future Nexus Vision contract candidate. | Record rename/reframe analysis and future approval need; do not rename yet. | Operating model and dossier carry Product Vision Contract language. |
| R7 | Safe file disposition review | Identify keep/collapse/migrate/retire/delete posture for every Docs file. | Generate full disposition table and USER decision list. | Manifest count matches filesystem enumeration and every file has a review row. |
| R8 | Validator and review-surface hardening | Make the corrected review model regeneration-safe. | Update helper/validator sections and regenerate audit/index. | Validation passes and generator output is stable. |
| R9 | Final USER review hold | Stop before PR Readiness until USER accepts the complete reform surface. | Report results only. | Next legal phase remains USER review, not PR creation by inertia. |

Disposition changes from USER review:
- Branch plans: from "delete after PR Readiness" to "fold down, migrate durable content, then retire by explicit posture; delete only with separate USER approval."
- Branch records: from "compact receipts" to "structured traceability receipts that may remain large when they are the correct ledger."
- Main: from "general source-truth doc" to "least-updated canonical docs index and recovery map."
- Backlog: from "current status plus detailed trace" to "compact product registry, status, family scope, package summary, and pointers."
- Roadmap: from "release/current-state record" to "release-stage schedule outline, public milestone posture, and broad feature breakpoints."
- Vision: from "low-risk product reference" to "future Nexus Vision contract candidate that drives backlog and branch planning."
- Safe/low-risk docs: from "safe to leave" to "reference-scan before delete/collapse, with replacement owner recorded."

Deferred decisions:
- Whether to rename `Docs/orin_vision.md` to a Nexus vision file and update all references.
- Whether to create a global governance/source-truth file index beyond the generated dossier and existing `Docs/Main.md`.
- Which historical branch plans should be retired first after fold-down proof.
- Which oversized branch records should be reorganized first into structured receipt format.
- Which low-risk reference docs should be deleted, collapsed, or retained.

## Vision Contract Implementation Checkpoint - 2026-05-21

Scope:
- Implement the approved Vision Contract / Vision-to-Plan governance model on this Governance carrier.
- Keep implementation limited to source-truth rules, branch-plan lifecycle updates, packet templates, assumption decision-state markers, USER Vision Green markers, fixture examples, and validator/helper scaffolding.
- Preserve `Docs/orin_vision.md` rename/reframe, broad family vision file creation, PR creation, merge, runtime work, FAM-006/FAM-007 mutation, release work, issue work, branch cleanup, and heavy validator enforcement against historical records as pending USER decisions.

Implementation model:
- Vision Contract complements the Branch Runtime Engineering Plan rather than replacing it.
- Nexus Vision remains the project-wide product intent layer; optional family vision should live in a family dossier or later USER-approved family vision file only when the feature family is broad enough.
- Branch Vision Contract Snapshot belongs inside the active branch plan so accepted branch-specific vision is close to the seams, files, validators, and proof it governs.
- Codex and ChatGPT recommendations remain proposed until USER accepts, revises, rejects, defers, waives, or supersedes them.
- `USER Vision Green: Yes` is the Workstream continuity lock: after it is recorded, Codex continues on the accepted plan unless a Level 2 seam-blocking or Level 3 workstream-breaking question appears.
- New design questions during Workstream should be classified as Level 1 non-blocking, Level 2 seam-blocking, or Level 3 workstream-breaking so implementation does not churn on harmless questions or silently ignore blocking ones.

Validator/helper posture:
- `dev/orin_branch_governance_validation.py` now carries reusable Branch Vision Contract Snapshot validation scaffolding.
- `dev/orin_branch_readiness_planning_fixture_validation.py` proves valid accepted vision, invalid proposed-only assumptions, and invalid blocking open vision questions through fixtures.
- Heavy enforcement against historical branch records remains deferred so old receipts are not broken by a new model.

## USER Feedback Disposition Implementation Plan - 2026-05-21

Status:
- Planning Status: `Planning / USER review only`.
- Implementation Status: `Not yet implemented as binding governance`.
- This section records the recommended model and future implementation targets. It does not by itself authorize Codex to enforce UFD requirements, mutate branch plans, create new UFD records, rename files, or treat proposed feedback as accepted branch scope.

Scope:
- Plan the USER Feedback Disposition model before implementation.
- Preserve meaningful USER feedback without creating another permanent feedback ledger.
- Keep this as planning/source-truth model work only until USER separately approves source-rule, validator, fixture, or template edits.
- Add repo naming / governance taxonomy reform planning so feedback IDs, phase labels, workstream labels, and file names become easier for USER, ChatGPT, and Codex to call consistently.

Future implementation target files:
- `Docs/branch_plans/README.md`
- `Docs/phase_governance.md`
- `Docs/governance_efficiency_operating_model.md`
- `Docs/validation_helper_registry.md`
- `Docs/nexus_startup_contract.md` (compact owner pointer only; it owns ChatGPT-generated Codex prompt-gate wording and loader/startup continuity)
- `Docs/codex_user_guide.md` (future USER-facing explanation/examples only)
- `Docs/orin_task_template.md` (future prompt-template field examples only)
- `dev/orin_branch_governance_validation.py`
- `dev/orin_branch_readiness_planning_fixture_validation.py`
- `dev/orin_governance_efficiency_validation.py`
- `dev/fixtures/branch_readiness_planning/<ufd_valid_or_invalid_fixture>.md`

Recommended model:
- Active full-detail feedback belongs in the active Branch Runtime Engineering Plan at `Docs/branch_plans/<branch_slug>.md`.
- Every meaningful USER feedback item should have one stable ID, one full-detail active owner, one disposition state, one USER decision state, one current/future branch impact classification, and one fold-down target.
- Branch records carry compact feedback status and a pointer to the active branch plan.
- Backlog carries compact future-candidate pointers only after USER accepts the future-work disposition.
- Roadmap carries no feedback detail unless the accepted feedback changes release-stage breakpoint or public milestone sequencing.
- Worktree slots carry no feedback detail.
- Nexus Vision and family vision/family dossier owners receive only accepted reusable standards, not branch-local unresolved feedback.
- Workstream docs and family dossiers receive folded durable outcomes, proof history, branch lessons, package trace, slice trace, and reusable continuity during PR Readiness fold-down.

Feedback ID recommendation:
- Use `UFD-<scope>-YYYYMMDD-NNN` for USER Feedback Disposition IDs.
- Do not use `FBK-*`; it collides visually with historical `FB-###` records and could be misread as a backlog identity.
- Scope examples: `UFD-FAM006-20260521-001`, `UFD-FAM007-20260521-001`, `UFD-GOV-20260521-001`, `UFD-NEXUS-20260521-001`.
- The ID is the compact pointer used by branch records, backlog, roadmap, workstreams, family dossiers, and PR fold-down receipts. Full feedback text should not be copied into each pointer location.
- UFD IDs remain valid after branch-plan fold-down and retirement. The fold-down receipt becomes the lookup path from the UFD ID to the final owner.

Meaningful feedback threshold:
- Not every USER comment becomes a UFD item.
- UFD disposition is required when USER feedback affects branch scope, accepted vision, user-facing behavior, runtime behavior, validation proof, future work, reusable product standards, approval boundaries, or a USER decision.
- Minor comments, acknowledgements, typo-level notes, duplicate remarks, or non-actionable conversation can close as `Rejected / No Action` or no durable UFD record when Codex states why no source-truth action is needed.

Split-state recommendation:

| Field | Purpose | Allowed planning values |
| --- | --- | --- |
| `Disposition Type:` | What kind of feedback item this is. | Current Branch Requirement; Current Seam Blocker; Current Seam Non-Blocking Queue; Branch Plan Revision Required; Future Branch Candidate; Family Vision Update Candidate; Nexus Vision Update Candidate; Backlog Pointer Candidate; Branch Receipt Item; Workstream / Family Dossier Item; Rejected / No Action |
| `USER Decision State:` | Whether USER has accepted the disposition. | Proposed by Codex; Recommended by ChatGPT; Accepted by USER; Revised by USER; Rejected by USER; Deferred by USER; Deferred With Waiver; Superseded; Needs USER Decision |
| `Workstream Severity:` | How much it affects implementation continuity. | Level 1 Non-Blocking; Level 2 Seam-Blocking; Level 3 Workstream-Breaking |
| `Owner Class:` | Which source-truth layer owns the durable fact. | Branch Plan; Branch Record; Backlog Pointer; Roadmap Pointer; Nexus Vision; Family Vision / Dossier; Workstream Doc; Governance Receipt; No Durable Owner Needed |

Minimum UFD record:
- `Feedback ID:`
- `Feedback Summary:`
- `Disposition Type:`
- `USER Decision State:`
- `Owner Class:`
- `Workstream Severity:`
- `Fold-Down Target:`

Full UFD record:
- `Feedback ID:`
- `Feedback Summary:`
- `Source:` chat, USER file, User Test Summary, ChatGPT review, GitHub review, validation result, or live proof.
- `Date / Phase:`
- `Affected Branch / Seam:`
- `Original Feedback Location:`
- `Disposition Type:`
- `Proposed Disposition:`
- `Accepted Disposition:`
- `USER Decision State:`
- `Workstream Severity:`
- `Canonical Owner File:`
- `Pointer Locations:`
- `Current Branch Impact:`
- `Future Branch Impact:`
- `Codex Recommendation:`
- `ChatGPT Critique / Review:`
- `Follow-Up Required:`
- `Fold-Down Target:`
- `Final Owner After PR Readiness:`

Fold-down receipt rule:
- PR Readiness Stage 1 must compare all open feedback items against the accepted branch plan and accepted Branch Vision Contract Snapshot.
- PR Readiness Stage 2 may proceed only when every meaningful feedback item is migrated, deferred with waiver, rejected/no-action with reason, closed, or explicitly carried to a future owner.
- The fold-down receipt should include `Feedback ID`, original owner, final disposition, final owner, USER decision, proof or migration reference, branch-plan retirement/deletion eligibility, and remaining open items.
- Branch plan deletion remains a separate USER decision. The default post-PR outcome is folded/retired posture, not deletion.
- Default branch-plan lifecycle outcome: folded / retired posture. Deletion requires separate USER approval or a future repo-established deletion rule that includes reference scans and durable-content preservation proof.

Validator/helper implementation posture:
- Initial implementation should add source-truth rule text, branch-plan template markers, fixture examples, and marker-based validator scaffolding.
- Heavy enforcement against historical branch records is deferred because old receipts contain many historical feedback/disposition phrases that were not created under this model.
- False-positive-prone duplicate full-text detection should be report-only until fixtures prove the pattern.
- Initial validators should enforce required markers, owner fields, safe decision-state values, and fold-down status only.
- Natural-language duplicate feedback detection starts as report-only. Blocking duplicate-feedback detection requires fixture coverage and separate USER approval.

Codex implementation guard:
- Codex may recommend UFD disposition, owner, Workstream severity, and fold-down target.
- Codex may not convert proposed feedback, Codex recommendations, ChatGPT recommendations, or inferred design preference into accepted branch scope without USER decision.
- USER decision controls accepted branch scope, accepted vision, accepted future-work posture, accepted reusable standard, and accepted no-action closure.

### Repo Naming / Governance Taxonomy Reform Addendum

Purpose:
- Make governance names easy for USER to call, easy for Codex to follow, easy for validators to report, and hard to confuse with backlog IDs, branch IDs, feedback IDs, or historical records.
- Reduce ambiguity that causes drift, especially around phase/stage/seam/slice/package/workstream/family and live-state/current-state language.
- Produce naming recommendations only. Bulk rename execution, file moves, directory moves, historical rewrites, and validator enforcement remain pending USER decisions.

Canonical names versus friendly aliases:
- Canonical names are used by validators, source truth, Codex packets, branch records, branch plans, helper output, and commit/PR metadata.
- Friendly aliases are USER-facing helper labels only.
- Friendly aliases never replace canonical phase, stage, marker, or file-owner names unless a future USER-approved rename migration updates source truth, validators, fixtures, templates, and historical compatibility notes.
- When both are useful, write the canonical name first and the alias second, such as `Branch Readiness Stage 1 (Plan Review)`.

Naming inventory:

| Term / Label | Current meaning / context | Correct intended meaning | Ambiguity risk | Recommended future name / usage | Owner documentation | Migration priority | USER decision needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Phase | Lifecycle state in phase governance. | Top-level lifecycle state. | Medium: sometimes used for substeps. | Keep `Phase`; define once. | `Docs/phase_governance.md`, `Docs/Main.md` | Low | No |
| Stage | Ordered sub-step inside a phase. | Stage 1 analysis vs Stage 2 execution/setup. | Medium: sometimes confused with release stage. | Keep `Stage`; always pair with phase name. | `Docs/phase_governance.md` | Low | No |
| Seam | Bounded execution checkpoint inside Workstream. | Workstream execution lane/checkpoint. | High: sometimes treated as final branch scope. | Keep `Seam`; define as bounded checkpoint, not automatic stop. | `Docs/Main.md`, `Docs/phase_governance.md` | Medium | No |
| Slice | Traceable deliverable unit inside a package. | Smaller admitted implementation unit. | High: overlaps seam in conversation. | Keep `Slice`; require `Slice = deliverable`, `Seam = execution checkpoint`. | `Docs/workstreams/index.md` | Medium | No |
| Workstream | Phase name and durable doc family. | Build/implementation phase; also promoted work record. | High: process and file owner share name. | Keep canonical `Workstream`; use `Workstream Doc` for files. | `Docs/workstreams/index.md` | Medium | No |
| Package | Grouped delivery scope under one family. | Branch/release package of related slices. | Medium: can sound like installer package. | Keep `Package`; expand as `Feature Package` at first use. | `Docs/feature_backlog.md` | Medium | No |
| Family | Long-lived product area. | Broad feature family. | Medium: FAM IDs can look temporary. | Keep `Family`; expand `FAM` at first use. | `Docs/feature_backlog.md` | Low | No |
| Backlog Item | Product registry entry. | Broad selectable family/package identity. | Medium: legacy FB rows are historical only. | Use `Backlog Family` for FAM records; `historical trace` for old FB rows. | `Docs/feature_backlog.md` | Medium | No |
| Branch Authority Record | Branch legal control surface. | Branch authority, approvals, phase history, compact receipt. | Low/Medium: often shortened to branch record. | Keep; allow `Branch Record` as alias after first use. | `Docs/branch_records/index.md` | Low | No |
| Branch Runtime Engineering Plan | Active detailed branch plan. | Runtime-focused active execution blueprint. | Medium: long name. | Keep formal name; alias `Branch Plan` after first use. | `Docs/branch_plans/README.md` | Low | No |
| Branch Plan | Short alias. | Alias for Branch Runtime Engineering Plan when context is clear. | Medium: could mean any plan. | Use only after formal name is introduced. | `Docs/branch_plans/README.md` | Medium | No |
| Branch Receipt | Folded historical branch evidence. | Compact/structured historical branch trace. | Medium: not consistently defined. | Define as `Structured Branch Receipt`. | `Docs/branch_records/index.md` | Medium | No |
| Worktree Slot | Stable workspace role assignment. | Intended lane assignment, not live state. | Low/Medium. | Keep; always say slot does not equal active authority. | `Docs/worktree_slots.md` | Low | No |
| Governance Receipt | Historical interpretation after validation. | Recorded decision/evidence, not live truth. | Medium. | Keep; define beside derived live truth. | `Docs/governance_efficiency_operating_model.md` | Low | No |
| Runtime Branch Engineering Contract | Engineering intent contract. | Branch-wide runtime baseline/delta/proof contract. | Medium: overlaps branch plan. | Keep; state contract = intent, plan = execution blueprint. | `Docs/phase_governance.md` | Low | No |
| Vision Contract | Product/design intent layer. | USER-accepted product/design standard. | Medium: can sound like new file. | Keep; use `Nexus Vision`, `Family Vision`, or `Branch Vision Snapshot` by scope. | `Docs/branch_plans/README.md` | Medium | Future file decision |
| Branch Vision Snapshot | Branch-specific accepted vision. | Snapshot inside active branch plan. | Low. | Use `Branch Vision Contract Snapshot` formally. | `Docs/branch_plans/README.md` | Low | No |
| USER Feedback Disposition | Feedback routing model. | Item-level classification and final owner proof. | New term. | Use `USER Feedback Disposition (UFD)` with ID glossary. | This plan; future branch-plan README update | High | Implementation approval |
| USER Decision Ledger | Planning decision record. | USER decisions, waivers, rejects, accepts. | Medium: could duplicate UFD. | Keep; UFD items link to it rather than copy. | `Docs/phase_governance.md` | Medium | No |
| Assumption Ledger | Design assumption states. | Codex/ChatGPT/USER assumption decision states. | Medium. | Use `Design Assumption Ledger`. | `Docs/branch_plans/README.md` | Low | No |
| Vision Question Digest | Packet for design uncertainty. | Question packet when vision/design uncertainty blocks or affects work. | Low. | Keep. | `Docs/branch_plans/README.md` | Low | No |
| Branch Plan Revision Packet | Controlled plan change packet. | Required when accepted scope/vision changes. | Low. | Keep. | `Docs/branch_plans/README.md` | Low | No |
| Hardening | Stabilization/proof phase. | Repo-side stabilization and plan comparison. | Medium for USER. | Keep canonical; optional alias `Stabilize`. | `Docs/phase_governance.md` | Low | No |
| Live Validation | User-observable validation phase. | Live/static proof, UTS, waiver posture. | Medium. | Keep canonical; optional alias `User Proof`. | `Docs/phase_governance.md` | Low | No |
| PR Readiness | Merge-readiness phase. | Stage 1 analysis and Stage 2 PR execution/watch. | Medium. | Keep canonical; aliases `Merge Readiness Audit` and `PR Execution / Watch`. | `Docs/phase_governance.md` | Low | No |
| Release Readiness | Release validation phase. | File-frozen release candidate validation. | Medium: confused with release execution. | Keep; always separate from `Release Execution`. | `Docs/phase_governance.md` | Low | No |
| Branch Readiness | Branch planning/setup phase. | Stage 1 analysis, Stage 2 setup/admission. | Medium. | Keep; aliases `Plan Review` and `Setup / Admission`. | `Docs/phase_governance.md` | Low | No |
| RRI | Standing governance intake cycle ID. | Release Readiness / governance intake cycle. | High: acronym is opaque. | Keep `RRI-*`; expand as `Release Readiness Intake` or `Governance Intake Cycle` at first use. | `Docs/branch_records/index.md` | Medium | Maybe rename later |
| UTS | User Test Summary. | USER validation questionnaire / returned proof. | Medium. | Keep; expand at first use in prompts. | `Docs/user_test_summary_guidance.md` | Low | No |
| SLC | Slice shorthand. | Slice ID or source-owner ledger row depending context. | High collision risk. | Avoid in new USER-facing prose; use `Slice` unless source-owner marker ID requires `SLC`. | `Docs/workstreams/index.md`, source-owner inventory | High | No for prose, yes for ID migration |
| PKG | Package shorthand. | Package ID. | Medium. | Keep in tables; expand `Package` at first use. | `Docs/feature_backlog.md` | Low | No |
| FAM | Feature Family shorthand. | Long-lived feature family ID. | Low/Medium. | Keep; expand `Feature Family (FAM)` at first use. | `Docs/feature_backlog.md` | Low | No |
| FB | Legacy backlog/workstream shorthand. | Historical trace only. | High: conflicts with future feedback IDs. | Preserve historical `FB-###`; never use for new feedback IDs or live backlog identities. | `Docs/feature_backlog.md`, `Docs/workstreams/index.md` | High | No |
| LV | Live Validation shorthand. | Live Validation stage shorthand, often LV1/LV2. | Medium. | Use `Live Validation LV1` at first use. | `Docs/phase_governance.md` | Low | No |
| H1 | Hardening pass shorthand. | Hardening stage/pass evidence. | Medium. | Use `Hardening H1` at first use. | `Docs/phase_governance.md` | Low | No |
| PR | Pull Request. | GitHub pull request evidence only. | Low/Medium. | Keep; never use PR number as backlog/workstream identity. | `Docs/Main.md` | Low | No |
| Release Window | Set of merged PRs since last release. | Derived release inventory for Release Readiness. | Medium: can become live ledger. | Keep; derive from GitHub/helper, record only historical receipt. | `Docs/prebeta_roadmap.md` | Medium | No |
| Current State | Often means live state or compact decision surface. | Avoid as owner unless clearly historical/current-summary. | High. | Prefer `Current Summary`, `Decision Surface`, or derived live truth. | `Docs/governance_efficiency_operating_model.md` | High | No |
| Active Branch | Legal current branch authority. | Active branch authorized by branch record, not slot or git alone. | High. | Use `Active Branch Authority` when legal meaning matters. | `Docs/branch_records/index.md` | High | No |
| Selected Next | USER-approved next branch/workstream posture. | Future selected work, not active branch by inertia. | High. | Use `Selected Next Workstream` or `Selected Next: Deferred/Waived`. | `Docs/phase_governance.md` | High | No |
| No Active Branch | Merged-main runtime/implementation idle posture. | No runtime/implementation/release/repair carrier active; standing governance may still exist. | High. | Keep with explicit standing-governance exception. | `Docs/branch_records/index.md` | High | No |

ID namespace policy:

| Namespace | Meaning | Status | Collision guard |
| --- | --- | --- | --- |
| `FAM-*` | Feature Family. | Live backlog family namespace. | Do not use for branch IDs, feedback IDs, PR IDs, or worktree slot IDs. |
| `PKG-*` | Feature Package under one family. | Live package namespace. | Expand as `Package` at first use. |
| `SLC-*` | Slice or source-owner marker slice row where historically required. | Avoid in new prose; preserve where existing source-owner records require it. | Prefer `Slice` in USER-facing text. |
| `FB-*` | Legacy backlog/workstream trace. | Historical-only. | Never use for new live backlog items or feedback IDs. |
| `UFD-*` | USER Feedback Disposition item. | Proposed future feedback namespace. | Never use `FBK-*`; UFD is not a backlog item. |
| `RRI-*` | Standing governance / Release Readiness Intake cycle. | Existing governance intake namespace. | Expand at first use; do not use for release IDs. |
| `PR #*` | GitHub pull request number. | GitHub evidence only. | PR number is never a backlog, workstream, package, or feedback identity. |

File naming analysis:

| Category | Preferred naming pattern | Preserve | Phase out later | Migration risk | USER decision needed |
| --- | --- | --- | --- | --- | --- |
| Top-level Docs files | `Docs/<clear_topic>.md`; noun phrase matching owner role. | `Docs/Main.md`, `Docs/phase_governance.md`, `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`. | Ambiguous old one-off topic files only after reference scan. | Medium because many prompts reference exact paths. | Yes for deletion/rename. |
| Branch records | `Docs/branch_records/<branch_slug>.md`. | Historical `codex_*` and `feature_*` records as receipts. | New active `codex/` naming; active repair-only naming by inertia. | High for historical links. | Yes for historical rewrites. |
| Branch plans | `Docs/branch_plans/<branch_slug>.md`. | Existing active/historical plans until fold-down review. | Permanent branch-specific plan sprawl after fold-down. | Medium. | Yes before deletion. |
| Workstream docs | `Docs/workstreams/FB-XXX_slug.md` for historical/promoted records. | Existing FB historical trace names. | New live FB IDs. | High; legacy evidence paths. | Yes for rename. |
| Family dossiers | `Docs/workstreams/FB-XXX_slug_family_dossier.md` until a future family-dossier directory is approved. | Existing family dossiers. | Mixing dossier and workstream meaning in text. | Medium. | Yes for directory split. |
| Validators/helpers | `dev/orin_<domain>_<capability>_validation.py`, `_audit.py`, `_harness.py`, `_helper.py`. | Existing reusable helper names. | Seam-number helper names unless temporary with consolidation target. | Low/Medium. | No for new names, yes for bulk rename. |
| Fixtures | `dev/fixtures/<domain>/<valid_or_invalid>_<scenario>.md`. | Existing branch readiness fixture names. | Opaque fixture names without expected result. | Low. | No for new fixtures. |
| README/index files | `README.md` for local standard; `index.md` for routing table. | `Docs/branch_plans/README.md`, `Docs/workstreams/index.md`, `Docs/branch_records/index.md`. | README carrying live branch state. | Low. | No. |

Governance label hierarchy recommendation:
- `Phase`: top-level lifecycle state: Branch Readiness, Workstream, Hardening, Live Validation, PR Readiness, Release Readiness, Release Execution, Post-Release Carry-Forward.
- `Stage`: ordered sub-step inside a phase: Stage 1 analysis; Stage 2 setup/execution.
- `Workstream`: implementation/build phase and promoted durable work record. When referencing files, say `Workstream Doc`.
- `Package`: delivery scope under one feature family.
- `Slice`: deliverable unit inside a package.
- `Seam`: bounded execution/proof checkpoint inside Workstream; not automatically the whole branch scope.
- `Branch Record`: legal authority and structured branch receipt.
- `Branch Plan`: active Branch Runtime Engineering Plan after first formal use.
- `Dossier`: durable family-level continuity surface, not active branch authority.
- `Receipt`: historical/validated interpretation, not live operational truth.

Acronym policy:
- Keep with first-use expansion: `FAM`, `PKG`, `UTS`, `LV`, `H1`, `PR`.
- Keep but mark historical-only: `FB`.
- Keep but expand aggressively: `RRI`.
- Avoid in new USER-facing prose unless table/ID context requires it: `SLC`.
- Add new: `UFD` for USER Feedback Disposition IDs only.
- Acronym glossary should live in `Docs/Main.md` as the recovery pointer and in the detailed owner docs (`Docs/feature_backlog.md`, `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, `Docs/workstreams/index.md`) for context-specific definitions.

User-facing process names:
- Keep canonical names and add friendly aliases only as presentation aids:
  - `Branch Readiness Stage 1` = `Plan Review`
  - `Branch Readiness Stage 2` = `Setup / Admission`
  - `Workstream Entry` = `Build Entry`
  - `Seam Execution` = `Bounded Build Seam`
  - `Hardening H1` = `Stabilize H1`
  - `Live Validation LV1` = `User Proof LV1`
  - `PR Readiness Stage 1` = `Merge Readiness Audit`
  - `PR Readiness Stage 2` = `PR Execution / Watch`
  - `Release Readiness Stage 1` = `Release Validation`
  - `Release Readiness Stage 2` = `Release Preparation`
  - `Release Execution` = `Publish Release`
  - `Post-Release Carry-Forward` = `Next-Branch Carry-Forward`
- Validators should continue to use canonical names until USER approves any canonical enum rename.

Codex prompt naming standard:
- Every prompt should name exact worktree, exact branch, exact phase, exact stage if applicable, exact source-truth owner, allowed mutation surfaces, pending USER decisions, validation commands, stop/report conditions, and exact return packet fields.
- ChatGPT-generated Codex prompt gates are owned by `Docs/nexus_startup_contract.md`. This plan and Codex prompt naming standards may point to that owner, but must not re-own or restate the Nexus Prompt Gate final scrub rule.
- Governance docs may define direct repo policy for Codex execution. The startup/loader contract owns generated-prompt wording and ChatGPT/new-chat bootstrap continuity.
- If a friendly alias is used, include the canonical name next to it on first use.
- Do not say `current state` without naming whether it means derived live truth, current summary, decision surface, or historical receipt.
- Do not say `branch plan` without naming the file path when mutation or validation is in scope.
- Do not say `feedback` without classifying whether it is UFD current-branch, future-candidate, reusable-vision, no-action, or needs USER decision.

Validator output naming standard:
- Validator messages should include severity, source-truth owner, fact class, phase/stage affected, exact blocking marker, exact repair owner, and exact USER decision needed when human approval is required.
- Recommended shape: `BLOCKED: <owner file>: <fact class>: <phase/stage>: <condition>; repair owner=<owner>; USER decision=<needed or none>`.
- Avoid ambiguous messages such as `current state missing`; prefer `Active Branch Authority marker missing from branch record` or `Derived live truth attempted in backlog`.

Index / README documentation standard:
- `Docs/Main.md`: glossary pointer, acronym first-use map, source-truth owner map, canonical/friendly phase alias table.
- `Docs/nexus_startup_contract.md`: ChatGPT/new-chat loader map and Nexus Prompt Gate owner for generated Codex prompts; other docs should use compact pointers instead of copying its prompt-gate wording.
- `Docs/codex_user_guide.md`: USER-facing explanation and examples.
- `Docs/orin_task_template.md`: reusable prompt packet skeleton and prompt-field examples; it points to the startup contract for prompt-gate wording rather than owning it.
- `Docs/phase_governance.md`: canonical lifecycle names and validator-backed markers.
- `Docs/branch_plans/README.md`: Branch Runtime Engineering Plan, UFD ledger, Branch Vision Snapshot, fold-down fields.
- `Docs/workstreams/index.md`: package/slice/seam/workstream/dossier naming.
- `Docs/branch_records/index.md`: branch authority, branch receipt, active/no-active/selected-next naming.
- `Docs/validation_helper_registry.md`: helper and validator naming standard.
- `Docs/worktree_slots.md`: slot naming and assignment-vs-authority distinction.

Missed source-truth owner coverage audit:

This table is a compact addendum to the complete Docs manifest in `Docs/governance_docs_full_inventory_reform_audit.md`. It records the owner files most likely to be missed by the UFD/naming implementation path and keeps prompt-gate ownership visible without duplicating prompt-gate policy.

| File path | Expected owner role | Manifest represented | Ownership map represented | Reform package represented | Missing / weak area | Repair posture |
| --- | --- | --- | --- | --- | --- | --- |
| `Docs/nexus_startup_contract.md` | ChatGPT/new-chat loader map and Nexus Prompt Gate owner for generated Codex prompts. | Yes | Yes | Weak before this addendum | UFD/naming implementation targets and Codex prompt naming standard did not visibly point to the loader/startup owner. | Repaired with compact target-file, prompt-naming, and documentation-standard pointers; no policy duplication. |
| `Docs/orin_task_template.md` | Reusable Codex task/prompt packet skeleton and prompt-field examples. | Yes | Yes | Present but paired weakly with startup owner | Template can look like prompt-gate owner if the startup contract pointer is missing. | Repaired with compact pointer that template examples route prompt-gate wording to `Docs/nexus_startup_contract.md`. |
| `Docs/codex_user_guide.md` | USER-facing Codex workflow guide and examples. | Yes | Yes | Yes | No source-truth miss found. | No repair beyond keeping it in future implementation targets for examples. |
| `Docs/codex_modes.md` | Codex execution posture and mode behavior. | Yes | Yes | Yes | No source-truth miss found. | No repair; it already points to the startup contract for prompt generation scope. |
| `Docs/pr_watcher_mode_contract.md` | PR watcher mode contract and watcher approval/default behavior. | Yes | Yes | Yes | No source-truth miss found. | No repair. |
| `Docs/user_test_summary_guidance.md` | User Test Summary guidance and UTS artifact expectations. | Yes | Yes | Yes | No source-truth miss found. | No repair. |
| `Docs/governance_intake_triage_and_digest_profiles.md` | Governance intake triage and digest profile standard. | Yes | Yes | Yes | No source-truth miss found. | No repair. |
| `Docs/orin_vision.md` | Current product/architecture vision reference and future Nexus Vision candidate. | Yes | Yes | Yes | Rename/reframe remains a pending USER decision, not a miss. | Deferred; no rename or broad vision migration in this pass. |
| `Docs/validation_helper_registry.md` | Helper/validator responsibility registry. | Yes | Yes | Yes | No source-truth miss found. | No repair. |

Staged naming migration plan:

| Stage | Work | Risk | Approval |
| --- | --- | --- | --- |
| N1 | Add glossary and taxonomy sections to owner docs. | Low. | Future source-edit approval. |
| N2 | Update Codex User Guide and templates with canonical name plus friendly alias rules. | Low/Medium. | Future source-edit approval. |
| N3 | Add validator wording standard and report-only taxonomy checks. | Medium. | Future validator approval. |
| N4 | Add fixture coverage for UFD IDs and ambiguous-name failures. | Low. | Future fixture approval. |
| N5 | Rename or collapse ambiguous top-level Docs files after reference scan. | High. | Separate USER decision per file group. |
| N6 | Consider directory split for family dossiers only if workstreams folder remains confusing after glossary update. | High. | Separate USER decision. |
| N7 | Historical compatibility pass for old FB/codex records; preserve old names as receipts. | High. | Separate USER decision. |

Naming reform acceptance checklist:
- Each term has one intended meaning.
- Each term has one owner doc.
- Each acronym is expanded at first use.
- Each process label fits phase/stage/seam/slice/package/family hierarchy.
- Each file name matches its ownership role.
- Codex prompts can call the term consistently.
- Validator output can report the term clearly.
- USER can understand and invoke the term without knowing internal history.
- Migration risk and rollback risk are documented.
- Historical compatibility is preserved for old branch, PR, release, and FB evidence.

Naming decisions still needing USER approval:
- Whether `RRI` should be re-expanded or renamed in public governance packets.
- Whether to create a dedicated acronym glossary section in `Docs/Main.md` or keep glossary entries distributed across owner docs.
- Whether to split family dossiers out of `Docs/workstreams/` later.
- Whether any top-level context docs should be renamed, collapsed, or deleted.
- Whether validator output should adopt severity prefixes globally.
- Whether friendly aliases should appear in final response packets by default or only in USER-facing guides.

## Next Legal Phase

- Recommended next phase: USER review of the updated Docs reform dossier and review index.
- PR creation: held until USER accepts the updated review surface and explicitly approves PR Readiness Stage 2.
- Merge: pending USER approval.
- Runtime implementation: blocked.
- FAM-006 mutation: blocked.
- FAM-007 mutation: blocked.
- Release/tag/artifact work: blocked.
