# Branch Authority Record: feature/repo-wide-source-owner-marker-adoption

## Branch Identity

- Branch: `feature/repo-wide-source-owner-marker-adoption`
- Workstream: `Repo-Wide High-Risk Source Owner Marker Adoption`
- Branch Class: `implementation`
- Backlog Record State: `Registry-only active branch`
- Package Fit: `Repo-wide source-truth, validator, and dev-tooling planning package; not a production runtime package`
- Primary Source-Truth Owner: `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`
- Branch Runtime Engineering Plan Path: `Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 carrier for the post-FAM-006 Repo-Wide High-Risk Source Owner Marker Adoption candidate.

The branch exists because merged `main` after PR #181 and `v1.7.9-prebeta` recorded `No Active Branch`, selected no runtime successor, and preserved Repo-Wide High-Risk Source Owner Marker Adoption as the strongest required governance/package candidate after the FAM-006 UI proof loop exposed repeated acceptance-critical visual/control-proof misses.

This branch may set up branch authority, branch planning, source-truth policy, high-risk surface inventory planning, marker-to-ledger validation planning, and dev-only review-mode disposition planning. It must not change production runtime behavior, expose element numbers in production UI, mutate FAM-007, mutate Compact-AI-Status-Card, use the standing Governance intake carrier, create a PR, merge, release, tag, create artifacts, mutate GitHub issues, or perform additional branch/worktree cleanup.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

Stage 1 Basis: `Complete - verified clean main at origin/main 26bb76becd4089d2e451d44e969939f0f074371f, No Active Branch source truth, selected-next None, FAM-006 historical/merged, and Repo-Wide High-Risk Source Owner Marker Adoption as the recorded candidate`
Stage 2 USER Approval: `Granted - USER approved branch/worktree creation and directly supporting branch authority, branch plan, source-truth, and validator planning setup`
Active Branch: `feature/repo-wide-source-owner-marker-adoption`
`Active Branch`: `feature/repo-wide-source-owner-marker-adoption`
Branch Creation Base: `26bb76becd4089d2e451d44e969939f0f074371f`
Current origin/main: `26bb76becd4089d2e451d44e969939f0f074371f`
Origin/Main Advanced Since Branch Creation: `NO`
Worktree Path: `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`
Branch Runtime Engineering Plan: `Accepted for Branch Readiness Stage 2 setup only`
Engineering Plan Status: `Accepted - marker policy, high-risk surface inventory plan, marker-to-ledger consistency plan, validator planning, and dev-only review-mode disposition plan are recorded; marker insertion and validator implementation remain pending USER decision`
Runtime Implementation Approval: `Pending/Blocked - production runtime behavior changes and product UI changes remain blocked`
Marker Insertion Approval: `Pending/Blocked except for setup/planning source truth; high-risk runtime/product source marker insertion remains pending later USER decision`
Package/Slice Admission: `Admitted for source-truth/validator/dev-tooling planning only; no existing FAM runtime package is claimed complete`
Element Validation Ledger Posture: `Ledger remains canonical; source-owner markers are optional dev-only backlinks and cannot satisfy user-facing acceptance proof`
Dev Toolkit Review Mode Posture: `Planning admitted; runtime/toolkit implementation remains pending USER decision`

## Branch Class

- `implementation`

Implementation Delta Class: `docs-only`

## Planning-Loop Guardrail

Implementation Delta Class: `docs-only`
Docs-Only Workstream: `Yes`
Planning-Loop Bypass User Approval: `APPROVED`
Planning-Loop Bypass Reason: `USER approved the branch/worktree creation plus directly supporting branch authority, branch plan, source-truth, and validator planning setup. Runtime/product changes, marker insertion, validator implementation, PR, merge, release, issue mutation, and cleanup remain blocked.`

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

## Bounded State

Bounded State: `Active - Branch Readiness Stage 2 setup / feature/repo-wide-source-owner-marker-adoption / C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers / repo-wide source-owner marker policy and validation planning only / no production runtime behavior, product UI, marker insertion into runtime files, PR, merge, release, issue mutation, FAM-007, Governance, Compact-AI, or cleanup work`

Expected Worktree Root: `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`

Actual Worktree Root: `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`

No Cross-Worktree Mutation: `Required - do not mutate C:\Nexus Desktop AI except for branch/worktree creation already completed from main, and do not mutate C:\Nexus Worktrees\FAM-007, C:\Nexus Worktrees\Governance, or C:\Nexus Worktrees\Compact-AI-Status-Card`

GitHub Desktop-bound worktree: `Not claimed for this branch during Stage 2 setup`

## Blockers

- `Runtime Implementation Approval Missing`: `Active - no production runtime behavior, UI behavior, provider/model, dashboard, monitor, or toolkit runtime implementation is authorized`
- `Marker Insertion Approval Missing`: `Active for high-risk product/runtime source files until Workstream implementation is separately approved`
- `Validator Implementation Approval Missing`: `Active for new or changed marker validators beyond planning unless USER approves Workstream implementation`
- `Dev Toolkit Runtime Approval Missing`: `Active - review-mode runtime/toolkit affordances remain planning only`
- `PR Creation Approval Missing`: `Active`
- `Merge Approval Missing`: `Active`
- `Release Execution Approval Missing`: `Active`
- `Issue Mutation Approval Missing`: `Active`

## Entry Basis

- Repo root before branch creation: `C:/Nexus Desktop AI`
- Current branch before branch creation: `main`
- Upstream before branch creation: `origin/main`
- HEAD before branch creation: `26bb76becd4089d2e451d44e969939f0f074371f`
- origin/main before branch creation: `26bb76becd4089d2e451d44e969939f0f074371f`
- Worktree state before branch creation: `clean`
- Active worktrees before branch creation: `C:\Nexus Desktop AI`, `C:\Nexus Worktrees\Compact-AI-Status-Card`, `C:\Nexus Worktrees\FAM-007`, and `C:\Nexus Worktrees\Governance`
- FAM-006 worktree cleanup state: `C:\Nexus Worktrees\FAM-006 removed before this branch`
- Candidate evidence: `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, and FAM-006 historical records identify Repo-Wide High-Risk Source Owner Marker Adoption and branch feature/repo-wide-source-owner-marker-adoption`

## Exit Criteria

- Branch authority record exists and is indexed.
- Branch Runtime Engineering Plan exists and is linked from this branch authority record.
- Backlog and roadmap keep compact active-branch pointers without absorbing detailed plan narrative.
- Marker policy defines purpose, format, placement, ownership, ledger relationship, production UI exclusion, and validator expectations.
- Element Validation Ledger remains canonical.
- High-risk surface inventory, marker-to-ledger consistency, marker coverage, production UI exclusion, and Dev Toolkit review-mode disposition planning are recorded.
- Validation passes.
- Stage 2 setup commit is pushed.
- Next legal phase is reported for USER approval.

## Branch Objective

Create the legal source-truth, branch-plan, marker-policy, validator-planning, and dev-tooling-planning carrier for repo-wide high-risk source owner marker adoption without changing production runtime behavior or product UI.

## Target End-State

Stage 2 exits with an active branch authority record, linked branch plan, compact backlog/roadmap pointers, marker policy, high-risk inventory plan, marker-to-ledger validation plan, production UI exclusion plan, Dev Toolkit review-mode disposition plan, green validation, committed/pushed setup, and a precise Workstream approval request.

## Backlog Completion Strategy

Branch Completion Goal: `Complete the marker-adoption planning and, after later USER approval, execute a bounded Workstream that can scan, map, mark, validate, harden, and fold down source-owner marker adoption without creating production runtime behavior.`

Known Future-Dependent Blockers: `Workstream implementation approval, marker insertion approval, validator implementation approval, Dev Toolkit runtime approval, PR creation approval, merge approval, release execution approval, issue mutation approval, branch cleanup approval, FAM-007/provider/model/memory/shortcut/installer approval, Compact-AI approval, Governance intake approval, and AI Product approval remain pending.`

Branch Closure Rule: `Before PR green, this active authority record must be made merge-stable or historical/no-active, backlog/roadmap must return to compact post-merge truth, and the Element Validation Ledger canonicality rule must remain intact.`

## Expected Seam Families And Risk Classes

Expected Seam Families: `High-risk source inventory; marker syntax and placement policy; canonical ledger mapping; limited marker insertion; marker coverage validation; production UI exclusion validation; Dev Toolkit review-mode disposition planning.`

Risk Classes: `marker noise, stale marker comments, orphaned markers, ledger drift, marker-only proof substitution, production UI element-number leakage, over-broad runtime edits, cross-worktree contamination, FAM-007/provider scope creep, Governance intake confusion, and Dev Toolkit runtime scope creep.`

## User Test Summary Strategy

Formal UTS is not required for Stage 2 setup because no production UI or runtime behavior changes. Future dev-only review-mode UI or production-visible work requires focused visual proof and UTS or explicit USER waiver.

## Later-Phase Expectations

Workstream should begin with a bounded scan/inventory and validator approach before broad marker insertion. Hardening must compare actual marker and validator behavior against this plan. Live Validation may be static/validator proof if no runtime-visible changes are admitted. PR Readiness must fold down active branch truth and preserve the ledger-as-canonical rule before PR creation.

## Initial Workstream Seam Sequence

Seam 1: `High-risk source surface inventory and marker format proof`

Goal: `Identify high-risk product/proof-bearing source regions and define a compact marker format that can be validated before inserting markers broadly.`

Scope: `Scan approved source surfaces, classify candidate high-risk regions, map candidates to canonical ledger rows or not-applicable reasons, and update source truth/validators as approved.`

Non-Includes: `Production runtime behavior changes, production UI changes, Dev Toolkit runtime implementation, FAM-007 mutation, Compact-AI mutation, Governance intake mutation, PR creation, merge, release, issue mutation, artifact handling, provider/model/memory/shortcut/installer work, and branch cleanup.`

## Active Seam

Active seam: `Branch Readiness Stage 2 setup - no Workstream seam is active until USER approves Workstream Entry.`

## Rollback Target

Rollback Target: `Branch Readiness`

Rollback Commit: `26bb76becd4089d2e451d44e969939f0f074371f`

Rollback Path: return to Branch Readiness Stage 1 decision posture if validation fails or USER rejects the setup. Branch deletion, worktree removal, and cleanup remain blocked unless USER separately approves exact cleanup scope and no-unique-commit-loss proof. Do not mutate main, FAM-007, Governance, Compact-AI, production runtime, product UI, releases, issues, or artifacts while rolling back.

## Next Legal Phase

- `Workstream`

Next Legal Phase Gate: USER must explicitly approve Workstream Entry analysis before Codex prepares the engineering design packet for marker implementation. Workstream implementation remains a later USER decision.

## Formal Next Legal Phase Digest

Current Phase: `Branch Readiness Stage 2 setup`

Next Legal Phase: `Workstream`

Next Legal Seam: `Workstream Entry analysis`

Why This Phase Is Next: `Stage 2 setup creates the legal carrier and source-truth plan; Workstream Entry must produce the engineering design packet before marker insertion, validator implementation, and any dev-toolkit review-mode work can be approved.`

Approval Required: `USER approval for Workstream Entry analysis`

Exact USER Approval Text: `Approve Workstream Entry analysis for feature/repo-wide-source-owner-marker-adoption in C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers. Codex may inspect source truth and high-risk product/proof-bearing source surfaces, map candidate regions to canonical Element Validation Ledger rows, recommend marker syntax and placement rules, recommend marker-to-ledger / coverage / production-UI-exclusion validators, assess Compact-AI-Status-Card preservation and cleanup/rebinding posture, and return the bounded implementation decision packet. Do not insert source-owner markers, implement validators, change production runtime behavior, expose production UI element numbers, mutate FAM-007, Compact-AI, Governance, release/tag/artifact work, GitHub issues, PR creation, merge, provider/model/memory/shortcut/installer work, or branch cleanup.`

Allowed Scope: `Read-only source-truth and source inspection, high-risk marker surface design, ledger mapping recommendation, validator/helper design, dev-only review-mode disposition planning, cleanup/rebinding planning, and next implementation approval text.`

Explicit Exclusions: `Production runtime behavior changes, production product UI changes, production element-number exposure, FAM-007 work, Compact-AI work, Governance standing intake mutation, PR creation, merge, release/tag/artifact work, issue mutation, branch cleanup, provider/model/memory/shortcut/installer work, and unrelated refactors.`

Validation Required: `branch governance validation, branch readiness planning fixture validation, release body validation, governance efficiency validation, compileall, diff checks, and any read-only helper validation required by source truth.`

Stop Conditions: `origin/main advances before Workstream Entry, worktree starts dirty outside approved setup changes, marker policy cannot preserve the Element Validation Ledger as canonical, implementation is needed before USER approval, validation fails, or source truth redirects to a different carrier.`

## Product Definition Plan

Product Vision: `Make high-risk product and proof-bearing source ownership inspectable enough that future UI, windowing, proof, and validation changes can be traced back to canonical element-ledger rows without turning code comments into the source of truth.`

User-Facing Goal: `Indirectly improve user-facing quality by making future risky UI/control/proof changes easier to inspect before USER testing, while keeping this branch's Stage 2 setup invisible to production users.`

Project-Wide Vision Alignment: `The project has repeatedly needed stronger proof-quality guardrails for user-facing UI, hidden window behavior, validation artifacts, and source-truth boundaries. Source-owner markers support that direction by helping reviewers navigate from risky code regions to canonical ledger rows and proof expectations.`

Branch-Specific Vision Alignment: `This branch is not a user-facing feature branch. It is a repo-wide traceability and validator-readiness branch that turns the recorded post-FAM-006 candidate into a legal work carrier while preserving No Active Branch main truth as the branch-creation basis.`

USER Vision Questions: `None block Stage 2 setup. Later Workstream implementation must ask for USER approval before marker insertion, validator implementation, or Dev Toolkit review-mode runtime work.`

USER Vision Question Packet: `No external USER input artifact is required for Stage 2 setup; branch purpose, exclusions, and next decision are fully stated in this record.`

Codex Product Interpretation: `High-risk source owner markers should be sparse, durable, and review-oriented: they should appear only where source regions carry user-facing, hidden-behavior, proof, state, or lifecycle risk and where a canonical ledger row exists or is added by the legal owner.`

Codex Implementation Recommendation: `Begin Workstream with an inventory and marker format validator before inserting markers broadly. Prefer a small first implementation pass over a noisy repo-wide comment flood.`

Codex Additional Recommendations: `Option 1 is inventory-only first for lowest risk; option 2 is a limited high-risk marker pilot for faster proof; option 3 is broader adoption only after validators prove marker-to-ledger consistency. Codex recommends option 2 after inventory because it balances progress with stale-marker risk.`

USER/ChatGPT Review Checkpoint: `USER approved Stage 2 setup only; Workstream implementation remains pending. ChatGPT review is not repo source truth.`

USER Critique Loop: `USER may approve, change, defer, critique, reject, or give feedback on marker format, source-owner naming, coverage threshold, and Dev Toolkit review-mode scope before Workstream inserts markers broadly.`

USER Decision Ledger: `USER approved Stage 1 analysis and Stage 2 setup. USER decisions pending: Workstream implementation, marker insertion, validator implementation, Dev Toolkit runtime, PR, merge, release, issue mutation, and cleanup. USER-deferred: production runtime behavior and product UI changes unless separately admitted.`

Deferred Ideas / Future Package Ledger: `Per-interface Dev Toolkit launchers, generalized all-surfaces review-mode launch, dev-only badges, hover highlighting, ledger tooltips, screenshot annotations, and future Overlay/display markers are deferred until Workstream or later USER approval.`

Planning Adequacy Review: `PASS for Stage 2 setup because it identifies carrier, worktree, branch authority, branch plan, marker policy, high-risk inventory plan, validator plan, ledger canonicality, affected surfaces, exclusions, and next legal phase.`

Rejected Shallow Plan: `Rejected - a generic "add comments everywhere" pass would create marker noise, stale code comments, and false proof. This branch requires ledger-backed high-risk-only markers and validators.`

Alternatives And Tradeoffs Reviewed: `Option A: no markers and ledger only, rejected because reviewers lose code-to-ledger navigation. Option B: markers on every element, rejected as noisy and stale-prone. Option C: high-risk-only markers mapped to ledger rows, selected for bounded traceability.`

Whole-System Interaction Map: `Canonical ledger rows own element identity and proof; source-owner markers backlink code regions to ledger rows; validators check marker syntax, ledger existence, coverage thresholds, and production UI exclusion; Dev Toolkit review-mode planning may later expose ledger metadata only in dev mode.`

System Concept Model: `Ledger -> marker mapping -> validator checks -> review/navigation aids -> future dev-only review-mode surfaces. Production runtime remains unchanged.`

Entity / Profile Model: `Element Validation Ledger row, source-owner marker, high-risk source region, proof surface, validator rule, dev-only review-mode disposition, and production UI exclusion are separate entities.`

User Workflow Model: `Developers and reviewers can inspect high-risk source regions, follow marker backlinks to ledger rows, confirm proof expectations, and avoid asking USER to validate unreviewed UI/control behavior. End users do not see markers.`

Scale / Data Volume Model: `The first adoption should prefer targeted high-risk regions over blanket coverage. Future Workstream should report total scanned files, high-risk candidates, rows mapped, markers added, not-applicable reasons, and validator findings.`

Configuration And State Model: `Markers are source comments or dev-only metadata only. They must not create production config, persistence, state transitions, telemetry, network calls, or product UI state.`

Whole-System Interaction Map: `Branch authority owns active scope; branch plan owns detailed implementation planning; backlog/roadmap provide compact pointers; ledger rows remain canonical; validators enforce marker-to-ledger and production UI exclusion rules.`

Minimum Viable vs Full System Boundary: `Minimum viable Workstream is scan + marker format + limited high-risk marker adoption + validator proof. Full system may add Dev Toolkit review-mode launchers and visual overlays later, but only with USER approval.`

Open Questions / USER Decision Points: `USER must decide whether to approve Workstream implementation, whether initial marker insertion should be inventory-only, limited high-risk pilot, or broader adoption, and whether Dev Toolkit review mode remains planning-only or becomes implementation scope.`

Current Branch vs Future Package Boundaries: `Current Stage 2 setup records policy and planning. Future Workstream may implement marker scan, marker insertion, validator checks, and dev-only review-mode planning. Future runtime/product behavior and production UI remain separate.`

Full Feature Element Breakdown: `Source-owner marker policy; high-risk source inventory; canonical ledger mapping; marker placement model; marker coverage validation; production UI exclusion validation; Dev Toolkit review-mode disposition planning; PR fold-down source-truth cleanup.`

Affected Surfaces: `Docs/branch_records/index.md, this branch record, Docs/branch_plans/feature_repo_wide_source_owner_marker_adoption.md, Docs/feature_backlog.md, Docs/prebeta_roadmap.md, Docs/validation_helper_registry.md, future marker validators under dev/, and high-risk source surfaces only after Workstream approval.`

Data/Control Model: `Source-owner markers should contain a stable marker ID or ledger row reference, ownership/scope tag, and not-applicable reason when no marker is placed. Validators should read source files and ledger rows without executing production code.`

Branch Reach / Package-Size Review: `The branch is large enough because source-owner markers span source truth, validators, proof helpers, runtime-adjacent files, UI surfaces, and dev-tooling review-mode planning. It is bounded because Stage 2 setup does not implement production behavior.`

Why Branch Is Large Enough: `A single-source-file marker pass would miss the cross-repo reason this candidate exists: high-risk UI/proof/source-truth traceability.`

Why Not Split Into Tiny Branches: `Splitting scan, marker format, ledger mapping, validator checks, and review-mode dispositions into separate branches would recreate source-truth churn and leave partial markers without validation.`

Expected User-Facing Outcomes: `No direct production UI output. Indirect outcome is fewer missed UI/proof issues because future implementation reviewers can trace high-risk code to canonical proof rows.`

Acceptance Criteria: `Stage 2 setup is accepted when branch authority, branch plan, compact pointers, marker policy, validator planning, ledger canonicality, validation plan, and next legal phase are recorded and validation passes.`

Screenshot / Live / User Test Summary Proof Requirements: `None for Stage 2 setup. Future Dev Toolkit review-mode UI implementation or production-visible changes require focused visual proof and UTS or explicit USER waiver.`

Validation Proof Requirements: `Stage 2 setup requires branch governance validation, branch readiness planning fixture validation, release body validation, governance efficiency validation, compileall, diff checks, and targeted source-truth searches. Future Workstream requires marker validator proof if implemented.`

Implementation Sequence Proposal: `Stage 2 setup -> Workstream inventory and marker-format validator -> limited marker adoption with ledger mapping -> marker coverage validation -> production UI exclusion validation -> H1 -> LV/static proof or USER waiver -> PR Readiness.`

Planning Blockers: `Workstream implementation approval missing; marker insertion approval missing; validator implementation approval missing; Dev Toolkit runtime approval missing; PR/merge/release/issue/cleanup approvals missing.`

USER Decisions Needed: `Approve Workstream implementation, then later approve PR creation, merge, release/tag/artifacts, issue mutation, branch cleanup, and any runtime/product/UI widening.`

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

User Test Summary Strategy: `No UTS required for Stage 2 setup; future UI/toolkit/runtime-visible work needs UTS or explicit USER waiver.`

Planning Completion Waiver: `Not required - Stage 2 setup planning is complete and validation-gated.`

## Runtime Branch Engineering Contract

USER Engineering Planning Review: `Stage 2 approved by USER after Stage 1 selected the candidate. Workstream implementation remains pending USER decision.`

Engineering Contract Status: `Accepted - Stage 2 setup records the contract; Workstream implementation remains pending.`

Branch Purpose: `Prepare repo-wide high-risk source owner marker adoption as a traceability and validator package while keeping runtime behavior and product UI unchanged.`

Runtime Implementation Approval: `Pending/Blocked - this branch is runtime-adjacent because it may later annotate runtime/proof-bearing files, but Stage 2 setup does not change runtime behavior.`

Current Runtime Baseline: `Production behavior is unchanged from origin/main 26bb76becd4089d2e451d44e969939f0f074371f; FAM-006 and FAM-007 runtime work is historical or separate.`

Planned Runtime Delta: `None for Stage 2 setup. Future Workstream may add dev-only source-owner comments/backlinks in source files without changing executable behavior.`

User-Facing Runtime Delta: `None. Production users must not see element numbers, marker IDs, review badges, or Dev Toolkit review-mode annotations.`

State / Config / Schema Delta: `None for production state/config/schema. Future marker metadata must remain source/dev-only and validator-readable.`

Validator / Helper Delta: `Stage 2 records planning for marker placement, marker-to-ledger consistency, marker coverage, and production UI exclusion. Future Workstream may implement or extend validators after USER approval.`

Expected Changed Files / Surfaces: `Stage 2 setup affects source truth and planning only. Future Workstream may affect dev validators and selected high-risk source files after USER approval.`

Approval-Boundary Audit: `Stage 2 setup is approved; runtime behavior, product UI, marker insertion into high-risk runtime files, Dev Toolkit runtime, PR, merge, release, issue mutation, cleanup, FAM-007, Governance, and Compact-AI remain outside scope.`

Future-Gated Items: `Marker insertion, validator implementation, Dev Toolkit review-mode implementation, production UI changes, production runtime behavior changes, PR, merge, release/tag/artifact work, issue mutation, branch cleanup, FAM-007 provider/model/memory/shortcut/installer work, Compact-AI work, Governance intake mutation, AI Product work, and external telemetry parity.`

Workstream Seam Map: `Seam 1 high-risk inventory; Seam 2 marker format and policy validation; Seam 3 ledger mapping and not-applicable reasons; Seam 4 limited marker insertion; Seam 5 marker coverage and production UI exclusion validation; Seam 6 Dev Toolkit review-mode disposition planning.`

Proof Expectations: `Static source-truth validation, diff checks, marker syntax/coverage validation when implemented, ledger existence checks, production UI exclusion checks, and no runtime behavior delta proof.`

Risk Forecast: `Marker noise, stale marker comments, ledger drift, production UI element-number leakage, over-broad runtime edits, cross-worktree contamination, FAM-007/provider scope creep, and Dev Toolkit runtime scope creep.`

Recommendations And Alternatives: `Prefer high-risk-only markers and validator-backed coverage over broad comment insertion; keep ledger canonical and review-mode dev-only.`

Plan Version / Revision Status: `v1 - Branch Readiness Stage 2 setup from origin/main 26bb76becd4089d2e451d44e969939f0f074371f.`

Plan-To-Implementation Traceability: `Stage 2 changes map to this branch record, the branch plan, compact backlog/roadmap pointers, branch_records index, and validation helper registry planning. Future Workstream must compare planned deltas with actual implementation by mapping each marker, validator, inventory result, production UI exclusion check, and not-applicable decision back to this plan and canonical ledger rows.`

## Marker Policy Summary

Marker Purpose: `Help reviewers find the canonical ledger row and proof expectations for high-risk source regions.`

Marker Format: `Future Workstream should use a compact stable comment format containing a marker prefix, ledger row ID, and short owner/scope label. Exact syntax remains pending implementation approval.`

Marker Placement Policy: `Place markers only near high-risk code regions that affect user-facing UI, hidden user-facing behavior, proof generation, state/lifecycle cleanup, focus/click routing, windowing, z-order, provider truth, warning behavior, source-truth mutation, UTS generation, or validation acceptance.`

Marker Ownership Rules: `The owning Element Validation Ledger row remains canonical. A marker must reference an existing row or a row added by the legal ledger owner. If no marker is placed for a high-risk row, record a not-applicable reason in the ledger or inventory.`

Production UI Exclusion Rule: `Production UI must not expose marker IDs, ledger IDs, element numbers, source-owner labels, review badges, hover outlines, or ledger tooltips. Dev-only review affordances require later USER approval.`

Validator Expectations: `Future validation should prove marker syntax, marker-to-ledger consistency, high-risk coverage or not-applicable reasons, no orphaned markers, no stale ledger IDs, no production UI exposure, and no marker-only proof substitution.`

## Package / Slice Fit

Package Shape: `Repo-wide source-truth / validator / dev-tooling planning package`

Formal Runtime FAM Package: `Not claimed`

Single-Slice Package User Approval: `Not required for Stage 2 setup because this branch is not claiming completion of a one-slice runtime package and records multiple planned seams.`

Planned Slices:

| Slice | Scope | Admission State | Completion State | Boundary |
| --- | --- | --- | --- | --- |
| `SRCOWN-SLC-001` | High-risk source surface inventory | Admitted for planning | Pending Workstream | Scan only until implementation approval |
| `SRCOWN-SLC-002` | Element Validation Ledger mapping | Admitted for planning | Pending Workstream | Ledger remains canonical |
| `SRCOWN-SLC-003` | Source-owner marker format and placement | Admitted for planning | Pending Workstream | Dev-only backlinks only |
| `SRCOWN-SLC-004` | Marker-to-ledger and coverage validation | Admitted for planning | Pending Workstream | Static validation only unless later approved |
| `SRCOWN-SLC-005` | Production UI exclusion validation | Admitted for planning | Pending Workstream | Production UI must not expose element IDs |
| `SRCOWN-SLC-006` | Dev Toolkit Interface Review Mode disposition planning | Admitted for planning | Pending Workstream | Runtime/toolkit implementation remains blocked |

## High-Risk Surface Inventory Plan

Initial Inventory Surfaces: `nexus_visual/`, `desktop/`, `dev/` proof helpers, branch authority records, Element Validation Ledger companion files, UTS guidance, and validation helper registry.`

High-Risk Classes: `Window ownership, drag/move/resize behavior, focus and click-through, clipping/z-order, source picker/checkable controls, warning behavior, provider truth, persistence/state transitions, cleanup/lifecycle, screenshot/proof generation, UTS generation, branch/source-truth mutation, and release/PR readiness validators.`

Inventory Output: `Future Workstream should record files scanned, candidate high-risk regions, ledger row targets, markers added, not-applicable decisions, and validator findings.`

## Validator Planning

Marker Placement Validation: `Future validator should flag malformed marker syntax, duplicate marker IDs, markers without ledger rows, markers in generated evidence, and markers in production UI text.`

Marker-To-Ledger Consistency Validation: `Future validator should verify referenced ledger IDs exist in canonical owners and that ledger rows list affected source surfaces or not-applicable reasons.`

Marker Coverage Validation: `Future validator should compare high-risk inventory classes against marker or not-applicable coverage without requiring blanket repo coverage.`

Production UI Exclusion Validation: `Future validator should scan production HTML/CSS/JS/Python UI copy for marker prefixes, ledger IDs, element numbers, review-badge copy, and dev-only review text.`

Dev Toolkit Review Mode Validation: `Future validator should prove dev-only gating before any review-mode UI is considered acceptable.`

## Element Validation Ledger Governance

Source-Truth Placement Preflight: `PASS - this branch is the active Registry-only authority owner for marker-adoption planning. Its active Element Validation Ledger lives in this branch authority record. Existing historical FAM-006 ledger rows remain canonical for FAM-006 history and are not moved.`

Existing Authority Owner: `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md`

Placement Decision: `Use this branch authority record for active marker-adoption planning rows; do not create a parallel active ledger file during Stage 2 setup.`

No Existing Owner Fits: `Not claimed`

Canonical Companion Ledger: `None for Stage 2 setup`

High-Risk Source Owner Marker Posture: `Ledger rows are canonical. Source-owner markers are optional backlinks. Marker-only proof cannot satisfy user-facing acceptance.`

## Element Validation Ledger

| Element ID | Element Name | Category | Parent Surface | Classification | User-Facing Status | Expected Behavior | Risk | Affected Source Surfaces | Source Owner Marker Posture | Validation Required | Current Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SRCOWN-GOV-POLICY-001` | Source owner marker policy | Source-truth governance | Branch authority / branch plan | Created | Internal support | Define marker purpose, format, placement, ledger relationship, ownership, and production UI exclusion | High | This record; branch plan; backlog/roadmap pointers | Marker policy owner, no runtime marker yet | Branch governance validation | Stage 2 setup | Ledger remains canonical |
| `SRCOWN-SCAN-INVENTORY-002` | High-risk source surface inventory plan | Source inventory | Repo-wide source | Created | Internal support | Plan scan of high-risk product/proof-bearing regions before marker insertion | High | Future `desktop/`, `nexus_visual/`, `dev/`, docs ledgers | Future marker adoption | Workstream validator / inventory proof | Pending Workstream | No files scanned during Stage 2 setup beyond source-truth inspection |
| `SRCOWN-LEDGER-MAPPING-003` | Marker-to-ledger mapping plan | Validation governance | Element Validation Ledger owners | Created | Internal support | Ensure every marker references a canonical ledger row or not-applicable reason | Critical | Branch records; companion ledgers; future validators | Future marker adoption | Marker-to-ledger consistency validation | Pending Workstream | Prevents orphan/stale markers |
| `SRCOWN-MARKER-PLACEMENT-004` | High-risk-only marker placement | Source marker policy | Runtime/proof-bearing code | Created / future | Internal support | Add sparse markers only where useful and high-risk | Medium | Future selected source files | Future marker adoption | Marker placement and coverage validation | Pending Workstream | Blanket marker insertion is rejected |
| `SRCOWN-PROD-UI-EXCLUSION-005` | Production UI marker exclusion | Product UI safety | Production UI source | Created / future | Hidden user-facing safety | Production UI must not expose marker IDs or element numbers | Critical | Future UI source scans | Future marker adoption | Production UI exclusion validation | Pending Workstream | Dev-only review badges remain future-gated |
| `SRCOWN-DEVTOOLKIT-DISPOSITION-006` | Dev Toolkit Interface Review Mode disposition | Dev tooling planning | Existing and future user-facing interfaces | Created / future | Dev-only | Plan review-mode disposition without implementing runtime/toolkit behavior in Stage 2 setup | Medium | Future dev toolkit source if approved | Future marker adoption | Dev-only gating validation if implemented | Pending Workstream | NCP, Core visualization, Dashboard, Overlay/display when admitted, and other windows/components are in planning scope |

## Multi-Worktree Risk Findings

- `C:\Nexus Worktrees\FAM-007` remains a separate lane; provider/model/memory/shortcut/installer work is out of scope.
- `C:\Nexus Worktrees\Governance` remains the standing governance intake lane and must not be used for this selected marker-adoption branch.
- `C:\Nexus Worktrees\Compact-AI-Status-Card` remains separate and must not be mutated.
- `C:\Nexus Desktop AI` remains neutral/main source for branch creation; after worktree creation, active edits belong in `C:\Nexus Worktrees\Repo-Wide-Source-Owner-Markers`.

## Validation Plan

- `git status --short --branch`
- `git diff --check`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_branch_readiness_planning_fixture_validation.py`
- `python dev\orin_release_body_validation.py`
- `python dev\orin_governance_efficiency_validation.py`
- `python -m compileall -q desktop dev nexus_visual`
- targeted source-truth searches for this branch record, branch plan pointer, marker policy, production UI exclusion, and pending USER decisions
