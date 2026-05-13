# Branch Authority Record: feature/fam-006-issue-readiness-governance-repair

## Branch Identity

- Branch: `feature/fam-006-issue-readiness-governance-repair`
- Workstream: `FAM-006 Issue Readiness Governance Repair`
- Branch Class: `repair/dev-tooling-governance`
- Backlog Record State: `No promoted backlog workstream`
- Package ID: `None`
- Package Name: `None`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 carrier for a bounded FAM-006 issue-readiness source-truth cleanup.

It exists because FAM-006 is already merged and released historical traceability, `main` is protected against direct Codex mutation, and the existing FAM-006 branch authority record plus companion ledger need a small consistency repair before USER can responsibly decide whether to create GitHub issue threads.

This branch does not admit runtime implementation, GitHub issue creation, issue-resolution branches, PR creation, release/tag/artifact work, FAM-007 implementation, local AI planning, AI Product Contract import, old `C:\` folder mutation, or `codex/ai-llm-lab` mutation.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Stage 1: `Complete - FAM-006 issue-readiness analysis found stale UTS/source-truth wording and recommended bounded source-truth cleanup before any issue creation`
- Stage 2 USER Approval: `Granted for FAM-006 issue-readiness/source-truth cleanup only`
- Branch Creation: `Created at D:\Nexus Worktrees\Nexus Desktop AI FAM-006 Issue Readiness from origin/main commit 88c11d53845f67bbf2490b8e4ce2b224bd62437b`
- Branch Naming State: `Renamed to feature/fam-006-issue-readiness-governance-repair after USER clarified active Nexus branch names must not use the codex/ prefix`
- Branch Authority State: `Active Branch`
- Current Authority: `This branch authority record owns only the bounded repair carrier state`
- FAM-006 RUI Authority: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md owns the Returned USER Issue Register; Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md owns row-level proof/disposition detail`
- Branch Scope: `Reconcile LV2 waiver/passable UTS wording, issue-readiness classifications, stale current-state FAM-006 backlog/roadmap wording, and issue-creation boundaries`
- USER-Confirmed Issue Queue: `Locked as 5 FAM-006 Dashboard issue threads; issue creation remains a future approval checkpoint`
- Evidence Policy: `Summary-only for future GitHub issue bodies; raw screenshots/videos stay local/external unless USER later approves upload, import, or linking`
- Branch Grouping: `Branch 1 feature/fam-006-dashboard-render-layout-hardening carries Issues 1, 2, and 5; Branch 2 feature/fam-006-dashboard-ia-controls-followthrough carries Issues 3 and 4`
- GitHub Issue Creation: `Blocked pending later explicit USER approval`
- Issue-Resolution Branches: `Blocked pending later explicit USER approval`
- Runtime Implementation: `Blocked`
- FAM-007 / Local AI Authority: `Blocked and out of scope`

## Branch Class

- `repair/dev-tooling-governance`

## Blockers

- `GitHub Issue Creation Approval Missing`: `Active`
- `Issue-Resolution Branch Approval Missing`: `Active`
- `Runtime Implementation Approval Missing`: `Active`
- `PR Creation Approval Missing`: `Active`
- `Release Execution Approval Missing`: `Active`
- `FAM-007 Admission Missing`: `Active`
- `AI Product Contract Import Approval Missing`: `Active`
- `Raw Evidence Import Decision Pending`: `Active - raw desktop UTS, screenshots, and video evidence remain external unless USER later approves a governed evidence import or link strategy`

## Entry Basis

- Updated `main` was clean and aligned with `origin/main` at `88c11d53845f67bbf2490b8e4ce2b224bd62437b`.
- Workspace identity preflight confirmed `D:\Nexus Repos\Nexus Desktop AI Main` as the main/consolidator clone.
- A separate D-drive FAM-007 worktree existed during preflight and was treated as metadata only, not as FAM-006 authority.
- Stage 1 found FAM-006 LV2 acceptance is USER WAIVED/PASSABLE, not a filled-UTS PASS.
- Stage 1 found the exact FAM-006 `## User Test Summary` wording and some current-state rows still carried stale pre-waiver, pre-merge, pre-release, or FAM-007 successor language.

## Source-Truth Placement Preflight

- Existing Authority Owner: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md` for the Returned USER Issue Register and FAM-006 UTS digest truth.
- Existing Row-Level Owner: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md`.
- Current-State Owners: `Docs/feature_backlog.md` and `Docs/prebeta_roadmap.md`.
- Placement Decision: extend the existing FAM-006 branch record and companion ledger; do not create a separate issue tracker or issue artifact.
- New Branch Authority Reason: this approved non-backlog repair branch needs its own branch-state authority under `Docs/branch_records/` while it is active.
- Duplication Check: no GitHub issues, issue drafts, runtime artifacts, or new evidence archives are created by this repair.
- Validator Posture: docs/governance validation should prove source-truth consistency; no runtime validator is required.

## Exit Criteria

- Stale FAM-006 UTS wording is reconciled with the LV2 explicit USER waiver/passable digest.
- The RUI issue-readiness map distinguishes closed-by-waiver/passable, deferred, future, unconfirmed/raw-proof-needed, and USER concern / issue-candidate states.
- The USER-confirmed five-thread issue queue, summary-only evidence policy, Branch 1 / Branch 2 grouping, deferred/future items, and post-issue-closure direction are recorded.
- Backlog and roadmap current-state rows no longer imply FAM-006 PR Readiness pending, no PR created, unreleased release debt, or FAM-007/local AI authority for this FAM-006 issue-planning track.
- GitHub issue creation and issue-resolution branches remain blocked pending later USER approval.
- Raw evidence import remains a future USER decision.
- Docs/governance validation passes.

## Rollback Target

- `Branch Readiness`

Rollback Path: abandon branch `feature/fam-006-issue-readiness-governance-repair`; do not mutate old `C:\` folders or the parked `codex/ai-llm-lab` branch.

## Next Legal Phase

- `PR Readiness`

Next Legal Phase Gate: after this bounded source-truth update validates, commits, and pushes, recommend `PR Readiness Stage 1` for this issue-readiness governance branch. Stage 1 may review PR readiness only; GitHub issue creation, issue-resolution branch creation, PR creation, release work, runtime work, FAM-007 work, or local AI work still requires separate explicit USER approval.

## Branch Objective

Repair FAM-006 issue-readiness source truth so the existing FAM-006 branch record, companion ledger, backlog, roadmap, and governance validator agree that PR #118 merged, v1.7.0-prebeta released, LV2 acceptance is USER WAIVED/PASSABLE, and later GitHub issue creation remains a separate USER decision.

## Target End-State

- FAM-006 current-state source truth distinguishes closed-by-waiver/passable, deferred, future, unconfirmed/raw-proof-needed, and USER concern / issue-candidate rows.
- The existing FAM-006 Returned USER Issue Register remains the source owner; no GitHub issues, issue drafts, runtime artifacts, or raw evidence archives are created.
- The confirmed FAM-006 issue queue is locked as five issue threads with summary-only evidence and two recommended future issue-resolution branch groups.
- Backlog and roadmap no longer imply stale FAM-006 PR Readiness, unmerged, unreleased, or FAM-007/local-AI successor authority.

## Backlog Completion Strategy

This carrier does not admit or complete a backlog package. It records a bounded post-release FAM-006 issue-readiness governance/source-truth repair and leaves issue creation, issue-resolution branches, package admission, runtime implementation, FAM-007/local AI work, and AI Product Contract import blocked.

Branch Completion Goal: source-truth cleanup validates, records the USER-confirmed issue queue and branch grouping, commits, pushes, and returns a Stage 2 stop packet with PR Readiness Stage 1 as the recommended next governance step.
Known Future-Dependent Blockers: GitHub issue creation, issue-resolution branches, raw evidence import/linking, runtime implementation, PR creation, release work, FAM-007/local AI work, and AI Product Contract import require later explicit USER approval.
Branch Closure Rule: stop after validated Stage 2 source-truth update; do not continue into issue creation, issue-resolution branch creation, PR creation, release work, runtime implementation, FAM-007, or local AI.

## Expected Seam Families And Risk Classes

- Branch Readiness Stage 2 source-truth repair.
- FAM-006 UTS/LV2 waiver reconciliation.
- RUI issue-readiness classification.
- Backlog/roadmap current-state cleanup.
- Governance-validator stale-current-state sync.

Risk Classes: stale UTS wording, accidental issue creation, accidental issue-resolution branch admission, FAM-006/FAM-007 boundary bleed, raw evidence over-import, stale release/PR posture, and noncanonical package/slice vocabulary.

## User Test Summary Strategy

No User Test Summary is generated, refreshed, imported, or mutated by this carrier. The raw desktop UTS, screenshots, and videos remain external evidence unless USER later approves a governed evidence-import or link strategy.

## USER-Confirmed FAM-006 Issue Queue Lock

Queue Lock State: `USER confirmed 5 FAM-006 Dashboard issue threads for future review. This record creates no GitHub issues and opens no issue-resolution branches.`

Prefix Correction: `USER-provided grouping names that used the old codex/ prefix are recorded with feature/ names because active Nexus branch names must not use codex/.`

| Issue Thread | Confirmed Title | Future Branch Grouping | Current Classification | Evidence Posture |
| --- | --- | --- | --- | --- |
| `FAM006-ISSUE-001` | Dashboard initial open flicker | `feature/fam-006-dashboard-render-layout-hardening` | USER concern / issue-candidate | Summary-only from USER video description and RUI/source-truth mapping; raw video remains local/external |
| `FAM006-ISSUE-002` | Dashboard scroll content well clipping / scrollbar ownership / gutter alignment | `feature/fam-006-dashboard-render-layout-hardening` | USER concern / issue-candidate | Summary-only from USER screenshots and RUI/source-truth mapping; raw screenshots remain local/external |
| `FAM006-ISSUE-003` | Monitor Groups card dead space plus Create/Edit monitor window split | `feature/fam-006-dashboard-ia-controls-followthrough` | USER concern / issue-candidate | Summary-only from USER screenshot description and RUI/source-truth mapping; raw screenshot remains local/external |
| `FAM006-ISSUE-004` | Remove redundant HUD Dashboard Open badge and add close affordance | `feature/fam-006-dashboard-ia-controls-followthrough` | USER concern / issue-candidate, with Dashboard settings cog/panel deferred | Summary-only from USER screenshot description and RUI/source-truth mapping; raw screenshot remains local/external |
| `FAM006-ISSUE-005` | Dashboard resize choppy/jittery | `feature/fam-006-dashboard-render-layout-hardening` | USER concern / issue-candidate | Summary-only from USER description and existing RUI resize-fluidity history; raw screen recording remains local/external unless later approved |

## Evidence Policy

GitHub Issue Evidence Policy: `Future GitHub issue bodies should use summary-only evidence based on repo-truth RUI rows, source-truth summaries, and proof paths. Raw screenshots, videos, and UTS exports remain local/external unless USER later explicitly approves upload, import, or linking.`

Raw Media Status: `No raw media file is imported, copied, uploaded, linked, or converted into a repo artifact by this carrier.`

## Branch Grouping

Branch 1 Recommendation: `feature/fam-006-dashboard-render-layout-hardening`

Branch 1 Carries: `FAM006-ISSUE-001 Dashboard initial open flicker`; `FAM006-ISSUE-002 Dashboard scroll content well clipping / scrollbar ownership / gutter alignment`; `FAM006-ISSUE-005 Dashboard resize choppy/jittery`.

Branch 1 Purpose: `Dashboard render/layout hardening for the released/passable Dashboard surface.`

Branch 2 Recommendation: `feature/fam-006-dashboard-ia-controls-followthrough`

Branch 2 Carries: `FAM006-ISSUE-003 Monitor Groups card dead space plus Create/Edit monitor window split`; `FAM006-ISSUE-004 remove redundant HUD Dashboard Open badge and add close affordance`.

Branch 2 Purpose: `Dashboard IA/control follow-through after render/layout confidence is addressed.`

Branch Creation Boundary: `These are recommendations only. Issue-resolution branch creation remains a future USER approval checkpoint.`

## Future / Deferred Items

- Dashboard settings cog/settings panel.
- Overlay/display acceptance.
- Provider/external telemetry parity.
- Dev Toolkit/source-owner markers.

## Post-FAM-006 Issue Closure Direction

After the confirmed FAM-006 issue threads are resolved, validated, and closed, the next FAM-006 Dashboard-related work should be selected from the highest-priority deferred Dashboard-related feature or the next priority item identified by current repo truth and USER review.

Current likely deferred candidates include Dashboard settings cog / settings panel, Overlay / display acceptance, Provider / external telemetry parity, and Dev Toolkit / source-owner markers.

The next item should be selected through the governed next-work / Branch Readiness path, using current source truth, USER priority, dependency order, and validation readiness.

This statement records forward direction only. It does not itself create a new branch, create issues, approve implementation, or promote a deferred item into active work.

## Later-Phase Expectations

After this source-truth update is validated, committed, and pushed, the recommended next governance step is `PR Readiness Stage 1` for the FAM-006 issue-readiness governance branch. USER may later approve GitHub issue creation, a specific issue-resolution branch, raw evidence upload/import/linking, runtime implementation, or no further FAM-006 issue work; each later action requires separate explicit approval.

## Initial Workstream Seam Sequence

Seam 1: FAM-006 issue-readiness source-truth repair.
Goal: reconcile stale FAM-006 UTS/source-truth wording with the LV2 USER WAIVED/PASSABLE digest and preserve later issue-creation boundaries.
Scope: docs/source-truth/governance only, including existing FAM-006 records, backlog/roadmap current-state owners, branch-record index, and stale governance-validator expectations if directly required for validation.
Non-Includes: runtime code, tests, GitHub issues, issue-resolution branches, PR creation, release work, FAM-007/local AI planning, AI Product Contract import, old C:\ folder mutation, and codex/ai-llm-lab mutation.

## Active Seam

Active seam: FAM-006 issue-readiness source-truth repair.

Active Seam Status: `Stage 2 source-truth repair is complete through the USER-confirmed issue queue lock after validation, commit, and push; this carrier remains active only for approved FAM-006 issue-readiness planning/source-truth organization until PR Readiness Stage 1 is requested.`

Next active seam: `None - later issue creation or branch work requires explicit USER approval.`

## Non-Includes

- GitHub issue creation.
- GitHub issue drafts as repo artifacts.
- Runtime code changes.
- Test or validator code changes unless a docs/governance validator gap blocks this repair.
- PR creation.
- Release, tag, or artifact work.
- FAM-007 planning, FAM-007 package admission, local AI implementation, AI Product Contract import.
- Mutation of old `C:\` folders or `codex/ai-llm-lab`.
