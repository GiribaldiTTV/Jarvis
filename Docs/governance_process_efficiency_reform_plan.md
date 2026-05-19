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
4. `Watcher Reliability And Repair-Mode Pass`.
5. `Governance Doc Compaction Pass`.
6. `Branch Planning UX And Template Pass`.
7. `Source-Truth Archive And Current-State Split Pass`.
8. `Governance Validator Modularization Pass`.
9. `Backlog/Roadmap Current Decision Surface Pass`.
10. `Release Ownership UX Pass`.
11. `Validation Runner And Registry Query Pass`.
12. `Phase Alias UX Pass`.
13. `Standing Governance Ledger Compaction Pass`.
14. `Public Language Mapping Pass`.
15. `Tracked Naming Drift Scan Pass`.

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

## Deferred / Needs USER Decision

- Whether to rename phases publicly or keep canonical-only phase names.
- Whether to split `dev/orin_branch_governance_validation.py` into modules in one pass or over several passes.
- Whether to archive large branch records now or wait until active FAM lanes are stable.
- Whether to create a no-mutation validation runner helper.
- Whether watcher repair-mode should depend on native Codex heartbeat behavior, local helper behavior, or both.

## Next Legal Phase

- Recommended next phase: focused governance planning for `Governance Intake Triage Template Pass` and `Digest Profile Standardization Pass`.
- PR creation: pending USER approval.
- Merge: pending USER approval.
- Runtime implementation: blocked.
- FAM-006 mutation: blocked.
- FAM-007 mutation: blocked.
- Release/tag/artifact work: blocked.
