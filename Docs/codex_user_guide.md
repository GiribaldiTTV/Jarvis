# Codex User Guide

## Purpose

This is a USER-facing quick guide for talking to Codex in the Nexus Desktop AI repo.

This guide is not binding governance. Repo source truth lives in `Docs/Main.md` and the owner files routed by `Docs/Main.md`. If this guide conflicts with source truth, source truth wins.

Use this guide when you want a short prompt that helps Codex understand the task without needing a full ChatGPT-generated packet.

## Quick Prompts

| Goal | Say This |
| --- | --- |
| Rebaseline safely | `Rebaseline and reconcile neutral main and the Governance worktree. Report identity, drift, validation, and next legal phase.` |
| Analyze only | `Analyze only. Load repo source truth first, inspect the issue, and return options with the safest legal path. Do not mutate.` |
| Docs-only repair | `Perform the approved bounded docs-only Governance repair. Keep helper, validator, runtime, FAM worktree, PR, merge, release, issue, cleanup, and external-state mutation blocked unless explicitly approved.` |
| Check everything | `Run a full Scope Coverage Manifest check for this scope. Inventory files, source-truth owners, changed surfaces, UI element groups, runtime/backend behavior, proof artifacts, validators, blind spots, exclusions, and USER-review items. Every target needs PASS, REPAIR, BLOCKED, WAIVED_WITH_REASON, or Not Applicable With Reason.` |
| UI/UX immersion check | `Evaluate all touched UI against Project Vision, FAM-002 presentation grammar, applicable Family / Feature Vision, Visual Inheritance Matrix, element-group acceptance, and screenshot/video or USER-validation proof. List every repair target.` |
| Backend reliability check | `Evaluate all touched runtime/backend behavior against the Backend Predictability / Reliability Contract. Map state owner, deterministic inputs/outputs, lifecycle/state machine, failure/fallback/recovery, logs, rollback, and UI-visible status/error mapping.` |
| Rebaseline after governance changed | `Run the merged-standard adoption review for this rebaselined branch. Compare already-implemented current and previous branch output against merged UI/UX, backend/runtime, proof, template, and vision standards. If out-of-scope defects are found, prepare issue candidates only; do not create GitHub issues without USER approval.` |
| PR Readiness analysis only | `Perform PR Readiness Stage 1 analysis only. Do not create a PR. Return blockers, changed-file scope, validation, PR-body risk, and exact Stage 2 approval text if green.` |
| Release Readiness analysis only | `Perform Release Readiness Stage 1 analysis only. Do not mutate files, tag, publish, create a release, or clean branches. Return release-window truth, blockers, and the exact next legal phase.` |
| User Test Summary review | `Digest the returned User Test Summary, map each USER finding to branch scope, evidence, repair status, waiver/deferral, and next legal phase. Do not treat helper green as USER acceptance.` |
| Ask for a prompt | `Give me a bounded prompt for the next legal phase. Include source-truth load order, approval boundaries, stop conditions, validation expectations, and exact return packet.` |

## Strong "Check Everything" Wording

Weak prompt:

```text
check everything
```

Better prompt:

```text
Run a full Scope Coverage Manifest check for the approved scope. Inventory every changed file, source-truth owner, UI element group, runtime/backend surface, generated artifact, proof claim, validator/helper result, human-judgment item, exclusion, blind spot, and downstream worktree adoption risk. Every target must be labeled PASS, REPAIR, BLOCKED, WAIVED_WITH_REASON, or Not Applicable With Reason before reporting green.
```

Use the stronger wording when the task is broad, visual, phase-sensitive, or has previously produced drift.

## Helpful Fields To Include

Use these fields when the phase or scope matters:

```text
Mode:
Phase:
Workstream:
Branch:
Worktree:
Approved scope:
Not approved:
Validation expected:
Stop conditions:
Return packet:
```

Example:

```text
Mode: Governance repair
Phase: Branch Readiness Stage 1 analysis
Workstream: Governance intake
Branch: feature/release-readiness-source-truth-intake
Worktree: C:\Nexus Worktrees\Governance
Approved scope: analysis only
Not approved: mutation, PR, merge, release, issue mutation, runtime work
Validation expected: read-only identity and source-truth load verification
Stop conditions: wrong worktree, stale origin/main, unclear authority
Return packet: verdict, files loaded, findings, next legal phase
```

## Useful Workflow Prompts

### Governance Drift Review

```text
Load Docs/Main.md first, then the routed governance/source-truth owners. Do a repo-wide source-truth drift review for this topic. Compare current governance against prior reform plans and report fix-now, defer, and no-action recommendations. Do not mutate unless explicitly approved.
```

### Vision / Feature Review

```text
Evaluate the relevant Project Vision, Family Vision, Feature Vision, backlog record, branch record, and branch plan. Confirm the work is rooted in durable vision, not just planning instructions. Flag stale wording, missing Feature Vision, slice/sprawl drift, and deferred carryforward gaps.
```

### UI Element Proof Review

```text
For each touched UI element group, compare visuals and behavior against accepted NDAI patterns. Include screenshots/video or USER validation where required. Check window chrome, close/minimize/maximize controls, spacing, fonts, colors, hover states, disabled states, error states, and whether the result feels deterministic, intuitive, immersive, and predictable.
```

### Backend / UI Truth Mapping

```text
For each touched UI state, identify the backend/runtime truth that drives it. Confirm disabled, loading, unavailable, error, success, fallback, recovery, and degraded states are backed by deterministic state instead of UI-only assumptions.
```

### Issue Candidate Review

```text
If the branch finds defects outside the approved current scope, prepare GitHub issue candidates only. Include title, affected FAM/FFV/surface, evidence, expected behavior, owner recommendation, and severity. Do not create or close GitHub issues without USER approval.
```

## If Codex Misses Something

Use this shape:

```text
This appears to be drift. Re-open the current phase analysis, explain why the prior check missed it, identify the source-truth/validator/helper gap, repair the gap if in scope, and rerun validation. Do not treat prior green validation as authority.
```

If the miss is visual, add:

```text
Include a screenshot or video proof review and an element-by-element comparison against the accepted NDAI visual pattern.
```

If the miss is backend/runtime, add:

```text
Include the runtime state owner, deterministic inputs/outputs, failure/fallback/recovery behavior, and UI-visible status mapping.
```

## Short Glossary

- `Source truth`: The repo-owned files routed by `Docs/Main.md`.
- `External operational state`: Local/private operational records outside repo docs when source truth permits.
- `USER packet`: A review aid for USER/ChatGPT; useful evidence, not source truth by itself.
- `Validator/helper output`: Evidence that must still be checked against repo truth and the actual work.
- `Slice` / `SLC`: A bounded implementation unit. `SLC` is the short written form for Slice-level line items.
- `Seam`: The current execution checkpoint inside or between slices.
- `Issue candidate`: A proposed GitHub issue record prepared for USER review before any issue mutation.

## What This Guide Does Not Do

This guide does not define phase law, approval authority, source-truth ownership, release rules, PR rules, helper behavior, validator behavior, or external-state schema.

For those rules, Codex must load `Docs/Main.md` and the current owner files it routes to.
