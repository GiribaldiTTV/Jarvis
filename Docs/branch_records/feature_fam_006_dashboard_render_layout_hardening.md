# Branch Authority Record: feature/fam-006-dashboard-render-layout-hardening

## Branch Identity

- Branch: `feature/fam-006-dashboard-render-layout-hardening`
- Workstream: `FAM-006 Dashboard Render/Layout Hardening`
- Branch Class: `implementation`
- Backlog Record State: `Registry-only issue-resolution continuation under historical FAM-006 / PKG-006`
- Package ID: `PKG-006`
- Package Name: `Monitoring HUD Dashboard Product Surface`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 setup carrier for the first FAM-006 Dashboard issue-resolution branch.

It exists because PR #122 merged the FAM-006 issue-readiness governance repair, the five locked FAM-006 Dashboard GitHub issues were created from updated main using summary-only evidence, and USER approved this first branch to carry the released Dashboard render/layout confidence issues before IA/control follow-through begins.

Current authorization covers post-merge cleanup, branch creation, branch authority setup, summary-only issue traceability for issues #123, #124, and #127, validation, commit, and push. Runtime implementation, PR creation, raw evidence upload/import/linking, release/tag/artifact work, FAM-007/local AI work, AI Product Contract import, old C:\ folder reactivation/reconciliation, and codex/ai-llm-lab reactivation/reconciliation remain future USER approval checkpoints.

## Record State

- `Active Branch Readiness setup`

## Status

- `Branch Readiness Stage 2 setup active - runtime implementation not approved`

## Canonical Branch

- `feature/fam-006-dashboard-render-layout-hardening`

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Stage 1: `Complete - USER approved Branch 1 grouping for issues #123, #124, and #127 after FAM-006 issue-readiness review`
- Stage 2 USER Approval: `Granted for cleanup, branch creation, branch authority setup, GitHub issue traceability comments, validation, commit, and push only`
- Branch Creation: `Created at D:\Nexus Worktrees\Nexus Desktop AI FAM-006 Dashboard Render Layout Hardening from origin/main commit fc17a16679cb3c61b31c939da18beb2aa6d90ef2`
- Branch Authority State: `Active Branch`
- Source-Truth Owner: `This branch record owns active Branch 1 authority; Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md owns historical FAM-006 RUI and issue-queue truth`
- Carried Issues: `#123 FAM-006 Dashboard: initial open flicker`; `#124 FAM-006 Dashboard: scroll content well clipping and scrollbar ownership`; `#127 FAM-006 Dashboard: resize jitter and catch-up lag`
- Held Issues: `#125 FAM-006 Dashboard: Monitor Groups dead space and Create/Edit window split`; `#126 FAM-006 Dashboard: remove redundant open badge and add close affordance`
- Future / Deferred Items: `Dashboard settings cog/settings panel`; `Overlay/display acceptance`; `Provider/external telemetry parity`; `Dev Toolkit/source-owner markers`
- Evidence Policy: `Summary-only for GitHub issue and branch source-truth references`
- Raw Media Status: `Raw screenshots, videos, and UTS exports remain local/external unless USER later approves upload, import, or linking`
- Runtime Implementation: `Blocked pending later explicit USER approval`
- GitHub Issue Traceability: `Branch carrier comments added to #123, #124, and #127 during this Stage 2 setup; issue body edits beyond planning references remain blocked`
- FAM-007 / Local AI Authority: `Blocked and out of scope`

## Branch Class

- `implementation`

## Blockers

- `Runtime Implementation Approval Missing`: `Active - this Stage 2 setup does not admit runtime edits`
- `PR Creation Approval Missing`: `Active - PR creation remains a future USER approval checkpoint`
- `Release Execution Approval Missing`: `Active`
- `Raw Evidence Import Decision Pending`: `Active - raw desktop media stays local/external unless USER later approves upload, import, or linking`
- `FAM-007 Admission Missing`: `Active - preserve separation from FAM-007/local AI`
- `AI Product Contract Import Approval Missing`: `Active`

## Entry Basis

- Updated D-drive main was clean and aligned with origin/main at `fc17a16679cb3c61b31c939da18beb2aa6d90ef2`.
- PR #122 merged the FAM-006 issue-readiness governance repair into main.
- The merged FAM-006 issue-readiness carrier was verified as historical/no-active and cleaned up locally/remotely before this branch was created.
- GitHub issues #123, #124, #125, #126, and #127 were created from updated main using summary-only evidence only.
- USER approved Branch 1 as `feature/fam-006-dashboard-render-layout-hardening`, carrying issues #123, #124, and #127.
- Issues #125 and #126 remain held for the later IA/control follow-through branch.

## Exit Criteria

- Branch authority is recorded for `feature/fam-006-dashboard-render-layout-hardening`.
- Issues #123, #124, and #127 are recorded as carried-now scope.
- Issues #125 and #126 plus future/deferred Dashboard-related items remain held for later USER decisions.
- Summary-only evidence policy and raw-media external/local status are preserved.
- GitHub issue traceability comments identify this branch as the planned carrier for #123, #124, and #127.
- Docs/governance validation passes.
- Setup changes are committed and pushed.
- Runtime implementation remains blocked pending later explicit USER approval.

## Rollback Target

- `Branch Readiness`

Rollback Path: abandon branch `feature/fam-006-dashboard-render-layout-hardening` before runtime implementation; do not mutate old C:\ folders, FAM-007 worktrees, or codex/ai-llm-lab.

## Next Legal Phase

- `Branch Readiness`

Next Legal Phase Gate: USER may later approve Workstream runtime implementation on this branch. Until that approval is explicit, this branch remains in Branch Readiness and carries no runtime code or test mutation authority.

## Branch Objective

Prepare the first FAM-006 Dashboard issue-resolution branch to harden the released/passable Dashboard render/layout surface: initial open visual stability, scroll/content well ownership, bottom gutter alignment, and resize smoothness.

## Target End-State

- The branch is cleanly created from updated main.
- Active branch authority and issue traceability are recorded.
- The carried issue set is limited to #123, #124, and #127.
- Branch 2 issues #125 and #126 remain out of scope.
- The next USER decision is whether to admit runtime implementation for the carried issues.

## Backlog Completion Strategy

This branch is a FAM-006 issue-resolution continuation under historical PKG-006, not a new backlog identity and not a new package admission.

Branch Completion Goal: complete Branch Readiness Stage 2 setup, trace issues #123/#124/#127 to this branch, validate, commit, push, and stop for USER runtime-implementation approval.
Known Future-Dependent Blockers: runtime implementation, PR creation, raw evidence upload/import/linking, release work, Branch 2, Dashboard settings cog/settings panel, Overlay/display acceptance, Provider/external telemetry parity, Dev Toolkit/source-owner markers, FAM-007/local AI work, and AI Product Contract import all require later explicit USER approval.
Branch Closure Rule: stop after validated setup and push unless USER later approves runtime Workstream implementation; do not expand into Branch 2 or future/deferred items.

## Expected Seam Families And Risk Classes

- Dashboard startup/render lifecycle stabilization for issue #123.
- Dashboard layout/scrollbar/content-well ownership for issue #124.
- Dashboard native-window resize smoothness and catch-up lag hardening for issue #127.

Risk Classes: user-visible startup flicker, CSS/layout/chrome boundary drift, native window resize behavior, screenshot-proof ambiguity, live-client proof requirements, and accidental scope bleed into Monitor Groups IA, close affordance, Dashboard settings, Overlay/display, provider telemetry, Dev Toolkit markers, FAM-007, or local AI.

## User Test Summary Strategy

Formal User Test Summary export remains exclusive to Live Validation Stage 1. During Branch Readiness and Workstream, this branch may maintain UTS strategy and proof expectations, but it must not generate or digest a formal returned UTS unless a later governed Live Validation phase is admitted.

## Planning-Loop Guardrail

Implementation Delta Class: runtime/user-facing
Docs-Only Workstream: No
Planning-Loop Bypass User Approval: None
Planning-Loop Bypass Reason: None

## Admitted Implementation Slice

Implementation Slice: `FAM006-BRANCH1-DASHBOARD-RENDER-LAYOUT-HARDENING`
Runtime Admission State: `Not admitted - runtime implementation is a future USER approval checkpoint`
Carried GitHub Issues: `#123`; `#124`; `#127`
Held GitHub Issues: `#125`; `#126`

## Slice Continuation Policy

Slice Continuation Default: Same-branch backlog completion
Backlog-Split User Approval: None
Backlog-Split Reason: None

## Product Definition Plan

Product Vision: harden the released Dashboard so its first visual impression, scroll framing, and resize behavior feel stable enough for repeated daily use.
User-Facing Goal: the Dashboard opens without whole-window flicker, presents the scrollable content well with clear ownership and matching gutters, and resizes without visible catch-up lag.
USER Vision Questions: none open for Branch 1 setup; USER already selected the carried issue grouping and held Branch 2/future items.
Codex Product Interpretation: these issues share the Dashboard render/layout confidence surface and should be handled together before IA/control follow-through.
Codex Implementation Recommendation: keep Branch 1 scoped to startup render stabilization, scroll/content-well layout ownership, and resize smoothness; defer Monitor Groups IA, top-bar affordance redesign, settings cog, Overlay/display, provider telemetry, Dev Toolkit markers, FAM-007, and local AI.
USER/ChatGPT Review Checkpoint: runtime implementation requires later explicit USER approval after this setup branch is validated and pushed.
Full Feature Element Breakdown: issue #123 initial open flicker; issue #124 scroll content well clipping, scrollbar ownership, and gutter alignment; issue #127 resize jitter and catch-up lag; held issue #125 Monitor Groups IA; held issue #126 close affordance/open badge.
Current Branch vs Future Package Boundaries: carried now means #123/#124/#127 only; held for later means #125/#126; future/deferred means Dashboard settings cog/settings panel, Overlay/display acceptance, Provider/external telemetry parity, and Dev Toolkit/source-owner markers.
Affected Surfaces: HUD Dashboard native window, Dashboard content frame/content well, scrollbar ownership/inset, startup/open path, resize drag path, and screenshot/live proof path.
Data/Control Model: no data model expansion is authorized during setup; implementation may later adjust Dashboard render timing, layout containment, and resize handling after USER approval.
Branch Reach / Package-Size Review: the branch carries three related Dashboard render/layout confidence issues with shared visual proof, shared user-facing surface, and shared validation path.
Why Branch Is Large Enough: grouping #123/#124/#127 reduces branch churn because they all affect Dashboard visual stability and live-client confidence.
Why Not Split Into Tiny Branches: splitting these issues would multiply setup, validation, proof, and PR overhead while USER confidence depends on the combined Dashboard render/layout feel.
Acceptance Criteria: Branch Readiness setup acceptance is finalized by Stage 2; later runtime acceptance will require #123 no first-second whole-window flicker, #124 content well/scrollbar/gutter ownership proof, and #127 smooth resize proof.
Validation Proof Requirements: governance validation during setup; later runtime validation should include the relevant Dashboard/HUD static validator, live human-client validation, open/close proof, resize-specific proof, and screenshot/crop proof for scroll/gutter/frame boundaries.
Screenshot / Live / User Test Summary Proof Requirements: summary-only evidence remains sufficient for GitHub issue/source-truth references; later implementation proof should include live-client screenshots/video-derived summaries as needed while raw media upload/import/linking remains blocked pending USER approval.
Implementation Sequence Proposal: Stage 2 setup first; after USER implementation approval, begin with startup render/open flicker, then scroll/content-well ownership, then resize smoothness, rerunning shared Dashboard proof after each material change.
Planning Blockers: none for Branch Readiness setup; runtime implementation remains blocked by `Runtime Implementation Approval Missing`.
USER Decisions Needed: approve runtime Workstream implementation when ready; decide later whether raw evidence import/linking is needed; decide later on Branch 2 and future/deferred items.
Planning Packet Status: Complete
Planning Revalidation Status: PASS
Planning Completion Waiver: Not required - USER-approved Stage 2 setup and prior Branch Readiness Phase 1 issue grouping provide the planning basis.
User Test Summary Strategy: no formal UTS is generated in Branch Readiness; formal UTS belongs to later Live Validation if admitted.

## Later-Phase Expectations

If USER later approves runtime implementation, Workstream should preserve carried-now scope, update source truth as each issue is addressed, and stop before PR creation until PR approval is explicit.

Expected later proof includes:

- Dashboard open/close proof for issue #123.
- Screenshot/crop or live-client proof for issue #124 gutter, content well, and scrollbar ownership.
- Resize drag proof for issue #127 with smooth intermediate geometry and no visible catch-up lag.
- Governance validation after source-truth updates.
- Static/live Dashboard validation if current repo truth identifies the relevant helpers.

## Initial Workstream Seam Sequence

Seam 1: `Dashboard Startup Render Stabilization`
Goal: prove issue #123 no longer shows whole-window first-second flicker on normal Dashboard open.
Scope: Dashboard open path and initial render stabilization only.
Non-Includes: scroll/content-well layout, resize smoothness, Monitor Groups IA, close affordance, settings cog, Overlay/display, provider telemetry, Dev Toolkit markers, FAM-007, and local AI.

Seam 2: `Dashboard Content Well And Scroll Ownership`
Goal: prove issue #124 content well, scrollbar, and bottom/side gutter alignment render cleanly.
Scope: Dashboard content frame, scroll owner, bottom gutter, side gutter, and clipping boundary.
Non-Includes: Monitor Groups Create/Edit flow, redundant badge removal, Dashboard settings, Overlay/display, provider telemetry, Dev Toolkit markers, FAM-007, and local AI.

Seam 3: `Dashboard Resize Fluidity`
Goal: prove issue #127 live resize follows drag motion smoothly without visible catch-up lag.
Scope: Dashboard native window resize behavior and live-client proof.
Non-Includes: unrelated window IA changes, Branch 2 controls, Dashboard settings, Overlay/display, provider telemetry, Dev Toolkit markers, FAM-007, and local AI.

## Active Seam

Active seam: `Branch Readiness Stage 2 - Source-Truth Setup And Issue Traceability`

Active Seam Status: source-truth setup and GitHub issue traceability only; runtime implementation is not admitted in this phase.

## GitHub Issue Traceability

Traceability Method: `Preferred GitHub Development linkage if available; fallback is concise summary-only issue comments naming this branch as the planned carrier.`

Branch Carrier: `feature/fam-006-dashboard-render-layout-hardening`

Traceability Comments: `#123 comment 4442908549`; `#124 comment 4442909498`; `#127 comment 4442910581`

Carried Issues:

- `#123 FAM-006 Dashboard: initial open flicker`
- `#124 FAM-006 Dashboard: scroll content well clipping and scrollbar ownership`
- `#127 FAM-006 Dashboard: resize jitter and catch-up lag`

Traceability Boundary: issue comments may record branch linkage and carried issue scope only. Raw screenshots/videos remain local/external. Issue body edits beyond planning references, runtime implementation, and PR creation require later USER approval.

## Held Work

- `#125 FAM-006 Dashboard: Monitor Groups dead space and Create/Edit window split` remains Branch 2 work.
- `#126 FAM-006 Dashboard: remove redundant open badge and add close affordance` remains Branch 2 work.
- Dashboard settings cog/settings panel remains future/deferred.
- Overlay/display acceptance remains future/deferred.
- Provider/external telemetry parity remains future/deferred.
- Dev Toolkit/source-owner markers remain future/deferred.

## Validation Expectations

Stage 2 setup validation:

- `git status --short --branch`
- `git diff --name-status origin/main...HEAD`
- `git diff --check origin/main...HEAD`
- `python dev\orin_branch_governance_validation.py`

Later runtime validation should surface before continuing when implementation is admitted and may include:

- relevant HUD/Dashboard static validator
- human-client live validation
- resize-specific proof
- open/close Dashboard proof
- screenshot/crop proof for gutter, scrollbar, and content-well boundaries
- formal UTS only if later Live Validation is admitted
