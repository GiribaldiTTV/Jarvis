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

## Next Legal Phase

- Recommended next phase: USER review of the updated Docs reform dossier and review index.
- PR creation: held until USER accepts the updated review surface and explicitly approves PR Readiness Stage 2.
- Merge: pending USER approval.
- Runtime implementation: blocked.
- FAM-006 mutation: blocked.
- FAM-007 mutation: blocked.
- Release/tag/artifact work: blocked.
