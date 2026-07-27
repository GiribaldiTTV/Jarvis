# Governance Intake Triage And Digest Profiles

## Purpose

This standard keeps governance repair efficient. It prevents broad governance requests from turning into mixed-scope rewrites, and it keeps Codex output focused on the legally required packet while preserving exact worktree, branch, validation, and next-phase proof.

## Scope

Use this standard for:

- broad governance/source-truth/process reform requests.
- USER-approved `phase-gate governance intake`.
- USER-approved `automation/worktree governance intake`.
- governance repair requests that are not already fully specified by a Release Readiness intake digest.
- any proposed governance, validator, helper, or prompt-contract change that could affect more than one branch/worktree.

This standard does not authorize runtime implementation, release execution, tag/GitHub Release/artifact work, issue work, direct-main mutation, branch cleanup, FAM-006 mutation, FAM-007 mutation, provider/model/memory/voice/Core/shortcut/installer work, AI Product Contract import, or private Dev ORIN import.

## Smallest Legal Packet Rule

Codex must choose the smallest digest profile that satisfies repo governance for the active phase.

- Do not restate full phase governance when changed values, blockers, validation, and next legal phase are enough.
- Do not paste broad protective rule lists when a source-truth pointer and exact blocker are enough.
- Do not put Codex phase-handoff text, `Next Legal Phase`, `Exact USER Decision Needed`, or `::git-*` directives into GitHub PR bodies or public release bodies.
- Use a `Full Audit Packet` only when the USER explicitly asks for a broad audit, root-cause analysis, or reform plan.

## Digest Non-Compaction Rule

Do not compact the digest ever.

Profile selection may choose the correct packet shape, but it must not shrink, collapse, summarize away, omit, or replace required digest fields, USER-requested review detail, blocker detail, validation proof, file lists, decision matrices, changed-surface evidence, or exact next-decision wording. Any digest means any Decision Packet, Return Digest, Validation Digest, Full Audit Packet, Delta Digest, phase digest, review digest, evidence digest, User Test Summary digest, rebaseline digest, Desktop review digest, or future repo-defined digest label.

When a USER asks for a full digest, review digest, complete breakdown, file-by-file packet, line-referenced packet, or any other explicitly detailed output, Codex must return that complete digest even if a smaller profile would otherwise be legal. A concise summary may be added before or after the digest, but it cannot replace or compact the digest.

Forwarded Digest Non-Compaction Rule: when Codex produces a digest intended to be forwarded to another branch, worktree, governance lane, PR watcher, Release Readiness lane, or future Codex thread, the digest must be complete and non-lossy. It must include repo/worktree identity, branch, HEAD or relevant commits, phase, source-truth owners, decision state, blockers, validation state, what happened, what went wrong, recommended governance/source-truth changes, exact USER decision needed, and explicit exclusions. Codex may organize the digest, but must not compress it into minimal bullets or omit operational details for brevity.

### Current-Gate USER Decision Consolidation

Current-gate decision consolidation is owned by `CDR-001` in
`Docs/phase_governance.md`. A `Decision Packet` must contain all presently
knowable material USER choices for the same gate where practical. Deterministic
same-gate repairs do not create serial USER repair gates; Codex repairs them
under the active approval, publishes one coherent final packet, and returns that
gate at one USER review boundary per gate. Separately gated later actions remain
separate and explicit rather than being combined by inference.

## Governance Intake Triage Packet

Before a broad non-release governance repair mutates source truth, Codex must either cite an already accepted triage packet or return this packet:

- `Problem Class:`
- `Source-Truth Support:`
- `Current Approval Coverage:`
- `Recommended Carrier:`
- `Smallest Safe Repair:`
- `Files Likely Affected:`
- `Validator / Helper Impact:`
- `Runtime / Product Risk:`
- `Active Branch / Worktree Interaction:`
- `PR / Merge Need:`
- `Deferred Items:`
- `Stop / Report Conditions:`
- `Recommended Digest Profile:`
- `Exact USER Decision Needed:`

Allowed classifications:

- `Adopt`: repo truth supports implementing the recommendation now.
- `Revise`: repo truth supports the goal, but the proposed shape must be narrowed or renamed.
- `Defer`: repo truth supports the idea later, but it should not enter the current repair.
- `Needs USER Decision`: source truth cannot decide safely without a concrete USER choice.
- `Reject`: repo truth conflicts with the recommendation or it would weaken a required gate.

## Digest Profiles

### Decision Packet

Use when the USER needs to approve or deny a next action.

Required sections:

- `Verdict:`
- `Decision Needed:`
- `Why This Is Needed:`
- `Scope If Approved:`
- `Explicit Non-Scope:`
- `Risks / Tradeoffs:`
- `Validation Expected:`
- `Exact USER Decision Needed:`

### Return Digest

Use when one worktree or thread must unblock another lane.

Required sections:

- `Verdict:`
- `Originating Worktree:`
- `Originating Branch:`
- `Operating Workspace:`
- `Expected Branch:`
- `Governance / Source-Truth Change:`
- `Merge / Commit Proof:`
- `Updated origin/main:`
- `Pre-Rebaseline Impact Audit:`
- `Rebaseline Instructions:`
- `Blockers Cleared:`
- `Blockers Remaining:`
- `Validations:`
- `Next Legal Phase:`

### Validation Digest

Use when the main value is proof status.

Required sections:

- `Verdict:`
- `Workspace / Branch:`
- `Commands Run:`
- `PASS Results:`
- `FAIL Results:`
- `Residual Risks:`
- `Next Legal Phase:`

### Full Audit Packet

Use only for explicit broad audits, process reform, root-cause analysis, or repo-wide recommendations.

Required sections:

- `Verdict:`
- `Audit Scope:`
- `Workspace / Branch Identity:`
- `Source Truth Inspected:`
- `Findings By Category:`
- `Recommendations By Category:`
- `Adopt / Revise / Defer / Needs USER Decision Matrix:`
- `Smallest Safe Next Pass:`
- `Validation:`
- `Next Legal Phase:`

### Delta Digest

Use when a prior accepted packet exists and only changed values need to be reported.

Required sections:

- `Verdict:`
- `Changed Since Last Packet:`
- `Unchanged Critical Truth:`
- `New Blockers:`
- `Cleared Blockers:`
- `Validation Delta:`
- `Next Legal Phase:`

## Profile Selection Guide

- Branch Readiness Stage 1 normally uses `Decision Packet` plus required Branch Readiness markers.
- Branch Readiness Stage 2 setup/repair normally uses `Validation Digest` after implementation, unless it must unblock another lane.
- Workstream seam closeout normally uses `Validation Digest` or `Delta Digest`.
- Live Validation returned USER evidence normally uses `Decision Packet` or `Validation Digest`.
- PR Readiness Stage 1 normally uses `Decision Packet`.
- PR Readiness Stage 2 after PR creation normally uses `Validation Digest` plus watcher status.
- Release Readiness Stage 1 normally uses `Decision Packet` when blocked or `Validation Digest` when green.
- Standing Governance Intake post-merge handoff always uses `Return Digest`.
- Broad process audits use `Full Audit Packet`.

## Source-Truth Recording Rule

When a reform pass generates more than one category of recommendation, record the complete inventory in source truth first, then implement focused passes one category or tightly coupled pair at a time.

The default first focused pair is:

- `Governance Intake Triage Template Pass`.
- `Digest Profile Standardization Pass`.

## Next Legal Phase

- Recommended next phase after this standard lands: focused PR Readiness for the governance reform branch if USER wants this standard merged.
- Future reforms should cite this standard and the category from `Docs/governance_process_efficiency_reform_plan.md` instead of restating the full reform inventory.
