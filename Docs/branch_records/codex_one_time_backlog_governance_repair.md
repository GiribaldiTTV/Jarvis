# One-Time Backlog Governance Repair Branch

## Branch Identity

- Branch: `codex/one-time-backlog-governance-repair`
- Branch Class: `repair/dev-tooling-governance`

## Purpose / Why It Exists

This branch carries the USER-approved one-time governance repair for the backlog-identity drift exposed by legacy FB-027 / PR #109.

It exists because PR #109 merged before the corrected governance could block small single-seam runtime follow-through from becoming active backlog/release truth. The repair cannot be made on `main`, because `main` is protected, and it cannot ride the already-merged PR #109 branch because that branch is no longer the legal execution base.

This branch must not change runtime behavior. Its job is to harden governance, validator behavior, and current-state truth so backlog identities remain large feature-family or release/support lanes and Codex stops before adding backlog items without explicit USER approval.

## Current Phase

- Phase: `Workstream`

## Phase Status

- Repo State: `No Active Branch` in merge-stable current-state owners.
- `Active Branch`: `codex/one-time-backlog-governance-repair`
- Active Branch Authority Record: `Docs/branch_records/codex_one_time_backlog_governance_repair.md`
- Active Branch: `codex/one-time-backlog-governance-repair`
- Workstream: `One-time backlog governance repair`
- USER Approval: explicit in the 2026-05-04 instruction to fix the governance drift in a one-time governance branch.
- Drift Finding: legacy FB-027 / PR #109 was allowed to become active selected-next and release-facing truth even though it was a small single-seam runtime follow-through.
- Repair Scope: backlog identity admission blocker, selected-next permission blocker, FAM-007 legacy FB-027 aggregation-hold correction, PR #109 standalone release-driver removal, historical backlog-item consolidation into family/source-of-truth trace, fresh `FAM-###` namespace introduction, and validator alignment.
- Runtime Scope: none.
- Current Seam: `Governance repair implementation and backlog source-of-truth consolidation`

## Branch Class

- `repair/dev-tooling-governance`

## Blockers

- no active blockers

## Entry Basis

- USER clarified that backlog is for large project and feature-release families, not governance work or small single-seam runtime slices.
- USER stated legacy FB-027 / PR #109 should not have been created as its own release-bearing lane and should be folded into the larger interaction/shared-action family category.
- USER directed a hard blocker for adding any backlog item without explicit USER permission.
- USER directed the blocker output: when reached, Codex must list all backlog items that are still not closed; if all are closed, Codex must stop for the later USER-controlled blocker.
- USER then explicitly approved the one-time backlog/source-of-truth consolidation so former small, support, governance, and registry-only backlog entries could be removed as selectable backlog items while preserving traceability.

## Exit Criteria

- `Docs/phase_governance.md`, `Docs/development_rules.md`, `Docs/Main.md`, and prompt surfaces define `Backlog Addition User Approval Missing` and `Backlog Exhaustion User Decision Pending`.
- Current-state truth no longer marks FAM-007 legacy FB-027 / PR #109 as an active backlog lane, selected-next lane, or standalone release-version driver.
- FAM-007 legacy FB-027 lifetime family trace records PR #109 as aggregation evidence with `Standalone Release Driver: No`.
- Former standalone historical pass aliases, support/governance lanes, and old registry-only implemented IDs are no longer parseable backlog entries; they route through feature-family trace tables, `Docs/workstreams/index.md`, family dossiers, canonical workstream records, or same-file historical trace.
- Live backlog-family entries now use the fresh `FAM-###` namespace starting at `FAM-001`; legacy `FB-###` is historical trace only and must not be reused for new parseable backlog identities.
- FAM-001 legacy FB-049 runtime proof, FAM-006 legacy FB-030 runtime diagnostics proof, pending `v1.6.13-prebeta` posture, FAM-006 merged-unreleased truth, and prior FAM-001 historical merge truth remain preserved.
- Governance validator behavior is aligned so absent USER approval blocks selected-next truth instead of forcing candidate creation.
- Validation commands pass or any residual repair candidate is explicitly listed before PR work.

## Rollback Target

- `Branch Readiness`

Rollback Path: revert this branch to restore the pre-repair governance and current-state interpretation. Do not revert PR #109 runtime behavior unless the USER explicitly requests a product rollback.

## Next Legal Phase

- `Hardening`

## Active Seam

Active seam: `Governance repair implementation and backlog source-of-truth consolidation`

## Seam Continuation Decision

Seam Status: `Green`
Slice Status: `Green`
Completion Status: `Green`
Waiver Status: `None`
Continue Decision: `Stop`
Stop Basis: `Workstream Green`
Stop Condition: `Governance repair implementation and backlog source-of-truth consolidation complete`
Continuation Action: `Proceed to Hardening validation for the one-time governance/source-of-truth repair.`
Decision Basis: `The docs and validator now encode the USER-permission backlog blocker, reclassify FAM-007 legacy FB-027 / PR #109 as family aggregation evidence, consolidate former non-family backlog entries into source-of-truth trace, and reserve legacy FB IDs for historical trace only.`
Next Active Seam: `Hardening H1 - One-Time Backlog Governance Repair Validation`

## Governance Drift Audit

Governance Drift Found: `Yes`

- Drift Type: backlog identity drift, legacy namespace collision risk, and selected-next pressure.
- What Went Wrong: the Successor Lane Lock Gate required a next runtime candidate before PR Readiness closeout, so Codex treated small same-family follow-through as selected-next truth instead of stopping for USER approval.
- Why Existing Canon Failed: backlog guardrails discouraged new identities, but the PR Readiness successor gate was stronger and mandatory.
- Repair Performed: add a higher-priority USER-approval blocker, require the still-not-closed backlog list when blocked, classify small single-seam runtime proof as aggregation evidence unless USER approves a release driver, consolidate former non-family backlog entries into family/source-of-truth trace, and move live family identities from legacy `FB-###` to fresh `FAM-###`.
- Whether The Drift Blocks Merge: `Yes until this branch validates`.
- Whether User Confirmation Is Required: `Already granted for this one-time governance repair; still required for any future backlog addition, split, promotion, successor selection, or standalone release-version driver`.

## Scope

- governance docs
- prompt contracts
- current-state canon
- FAM-007 legacy FB-027 family dossier and historical workstream trace
- branch authority routing
- validator alignment

## Explicit Non-Goals

- no runtime product changes
- no direct edits on `main`
- no new backlog item
- no successor implementation branch
- no release packaging
- no PR #109 runtime rollback
