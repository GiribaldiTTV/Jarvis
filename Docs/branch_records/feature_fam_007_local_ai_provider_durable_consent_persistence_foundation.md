# Branch Record: feature/fam-007-local-ai-provider-durable-consent-persistence-foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-durable-consent-persistence-foundation; surface=branch-record; status=canonical

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-durable-consent-persistence-foundation`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Branch Class: `implementation`
- Family: `FAM-007`
- Package: `PKG-007`
- Branch Runtime Engineering Plan Path: `Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md`
- Created From: `origin/main@10c32804370ee5480416e68e55823e5997d18291`
- Latest Public Prerelease: `v1.7.16-prebeta`
- Latest Public Release Commit: `10c32804370ee5480416e68e55823e5997d18291`

## Current Phase

Phase: `Branch Readiness`

## Phase Status

- Branch Authority Marker: `Active Branch`
Phase Status: `Active Branch - Branch Readiness Stage 2 setup complete for FAM-007 Durable Consent Persistence Foundation. Runtime implementation remains blocked until Workstream Entry and later USER implementation approval.`
Bounded State: `Granted for Branch Readiness Stage 2 setup, v1.7.16 post-release canon closure, FAM-007 branch authority, Product Definition Plan, Runtime Branch Engineering Contract, Branch Runtime Engineering Plan, bounded Workstream admission, and family-scoped Branch Readiness confinement repair only.`

## Branch Class

Branch Class: `implementation`

## Blockers

Blockers: `Workstream Entry approval pending; runtime implementation pending USER decision.`

## Entry Basis

Entry Basis: `USER approved FAM-007 Branch Readiness Stage 2 in C:\Nexus Worktrees\FAM-007 after v1.7.16-prebeta release and explicitly approved repairing Branch Readiness sibling-lane drift on this branch.`

## Exit Criteria

Exit Criteria: `Stage 2 is complete when source truth records the fresh FAM-007 branch authority, v1.7.16 release closure, durable consent persistence planning scope, family-scoped confinement repair, validation is green, and the branch is committed and pushed.`

## Rollback Target

Rollback Target: `Branch Readiness`

## Planning-Loop Guardrail

Implementation Delta Class: `backend/runtime`

Docs-Only Workstream: No

Planning-Loop Bypass User Approval: `None`

Planning-Loop Bypass Reason: None

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`

Backlog-Split User Approval: `None`

Backlog-Split Reason: None

## Next Legal Phase

`Workstream`

## Branch Objective

Prepare the next FAM-007 successor after PR #201 by admitting durable local consent persistence foundation as the next local-only prerequisite before user-operated consent UX, provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, or functional AI.

## Target End-State

The branch should be ready for Workstream Entry analysis with a clear plan to persist consent records durably and locally, preserve setup/execution consent separation, preserve revocation/reset semantics, prove no provider-visible data leaves the machine, and keep provider setup/model execution blocked.

## Backlog Completion Strategy

Branch Completion Goal: `Durable local consent persistence foundation is implemented, validator-proven, H1 green, LV1 green or explicitly waived for static/local-only proof, PR-ready, merged, and later released only after USER approval.`
Known Future-Dependent Blockers: `User-operated consent UX, provider setup completion, provider SDK/adapter integration, prompt/model execution, downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`
Branch Closure Rule: `The branch may close after durable local consent persistence foundation is proven or blocked/deferred with USER waiver; it must not claim functional AI, provider execution, or user-operated consent capture beyond the admitted persistence foundation.`

## Expected Seam Families And Risk Classes

- Seam Family 1: Durable Consent Persistence State And Schema - medium risk, local-only state/storage boundary.
- Seam Family 2: Consent Record Storage Boundary And Migration Posture - medium risk, local filesystem/config boundary only.
- Seam Family 3: Revocation, Reset, And Expiry Persistence Semantics - medium risk, fail-closed local state behavior.
- Seam Family 4: Setup Consent / Execution Consent Durable Separation - high risk, provider-execution boundary.
- Seam Family 5: Core/Desktop/ORIN Status Proof And Hidden Telemetry - medium risk, status-only UI/proof.
- Seam Family 6: Validator Fixtures And Future Handoff Criteria - medium risk, static validator/proof coverage.

## User Test Summary Strategy

No user-operated consent UX is admitted by Stage 2. Workstream Entry must decide whether LV1 can use static validator proof only, a hidden-telemetry proof path, or a later USER-approved visible proof. A formal UTS remains pending until user-facing behavior is admitted or explicitly waived.

## Later-Phase Expectations

Workstream Entry must inspect the full plan, compare it against prior PR #201 evidence, confirm the durable persistence boundary, and return exact implementation approval text. Hardening H1 must compare implementation against this plan, and LV1 must prove local-only/provider-safe posture before PR Readiness.

## Initial Workstream Seam Sequence

Seam 1: `Durable consent persistence state and schema`
Goal: `Define local durable consent record state, storage boundary, schema versioning, and fail-closed default posture.`
Scope: `Local-only consent persistence planning and later implementation; setup consent and execution consent stay distinct.`
Non-Includes: `Provider setup completion, provider SDK/model execution, prompt routing, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, user-operated consent UX beyond persistence proof, release execution, cleanup, and sibling-lane mutation.`

## Active Seam

Active seam: `Branch Readiness Stage 2 setup and Workstream Entry preparation.`

## Admitted Implementation Slice

Slice: FAM-007 durable consent persistence foundation, covering local durable consent record schema, local storage boundary, schema versioning, revocation/reset/expiry semantics, setup consent and execution consent durable separation, provenance/audit metadata, provider-visible-data none, fail-closed validator fixtures, Core/Desktop/ORIN status proof if admitted, and future provider setup handoff without enabling provider setup completion, provider SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, release execution, cleanup, or sibling-lane mutation.

## Product Definition Plan

Product Vision: `FAM-007 should become useful local AI through explicit user control over setup, durable local consent, provider-visible data, and execution before any model is allowed to run.`
User-Facing Goal: `Lay the durable local consent persistence foundation so later user-operated consent UX can be truthful, revocable, auditable, and local-only.`
Project-Wide Vision Alignment: `Nexus remains Windows-first, local-first, privacy-explicit, and honest about disabled AI/provider execution until the user approves each layer.`
Branch-Specific Vision Alignment: `This branch owns durable local consent persistence planning and later proof; it does not own provider setup completion, user-operated consent UX, SDK/model execution, or functional AI.`
USER Vision Questions: `None blocking for Stage 2. Workstream Entry should ask whether visible consent UX belongs in this branch or a later branch if repo truth changes.`
USER Vision Question Packet: `Not required for Stage 2 because this branch admits local persistence foundation only; any visible consent UX requires a later packet or explicit USER approval.`
Codex Product Interpretation: `Durable consent persistence is the next safest FAM-007 layer after local consent capture/write-path proof because it hardens consent truth before provider setup or model execution.`
Codex Implementation Recommendation: `Implement persistence schema, storage boundary, revocation/reset durability, fail-closed validation, and status proof before user-operated consent UX or provider setup completion.`
Codex Additional Recommendations: `Recommendation: keep all provider-visible data none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads/network blocked, memory inactive, and voice/Core sync gated; option: defer visible consent UX until durable storage semantics pass validation.`
USER/ChatGPT Review Checkpoint: `USER may inspect this record and the branch plan before approving Workstream Entry or implementation.`
USER Critique Loop: `USER may accept, revise, reject, or defer durable persistence scope before Workstream implementation.`
USER Decision Ledger: `USER approved Stage 2 setup and the FAM-007 confinement repair; USER decisions for Workstream Entry, runtime implementation, PR creation, merge, release, cleanup, provider/model/memory/voice/shortcut/installer work, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain pending.`
Deferred Ideas / Future Package Ledger: `Future packages or deferred USER decisions own user-operated consent UX, provider setup completion, provider SDK/adapter boundary, prompt/model execution proof, durable memory/indexing, voice/Core sync, shortcuts/installers, and v1.8.0 functional-AI proof.`
Planning Adequacy Review: `The plan is not a one-screen or marker-only plan because it names persistence state, storage boundary, revocation/reset semantics, consent separation, UI/status proof, validators, future boundaries, and phase proof.`
Rejected Shallow Plan: `Rejected: merely marking consent as stored without schema, revocation, reset, storage-boundary, provenance, and fail-closed validation proof.`
Alternatives And Tradeoffs Reviewed: `Provider setup completion is higher-risk before durable consent truth; user-operated consent UX may be next but risks visible behavior before storage semantics; SDK/model execution is premature.`
Whole-System Interaction Map: `Local consent capture state -> durable local consent record -> setup/execution consent separation -> provider setup handoff criteria -> disabled prompt/model execution -> future functional-AI proof.`
Open Questions / USER Decision Points: `USER decision points remain pending for whether visible consent UX joins a later branch, when provider setup completion becomes admissible, and whether durable persistence uses config, profile, or a dedicated local store during implementation.`
Minimum Viable vs Full System Boundary: `Minimum viable branch is durable local consent persistence and validation; full system remains user-operated consent UX, provider setup, SDK/model execution, memory, voice/Core, and release proof.`
Full Feature Element Breakdown: `Consent record state, storage boundary, schema versioning, setup consent durability, execution consent durability, revocation/reset persistence, provenance/audit metadata, hidden/status proof, validator fixtures, future handoff.`
System Concept Model: `Consent is a local prerequisite contract. Durable consent state may inform future setup and execution gates but cannot send data to providers or enable prompts by itself.`
Entity / Profile Model: `Entities include local consent record, setup consent flag, execution consent flag, revocation/reset event, persistence provenance, schema version, provider-visible-data posture, and future handoff metadata.`
User Workflow Model: `Future user grants or revokes consent through a later UX; this branch prepares the durable record so that future UI can truthfully reflect local consent state.`
Scale / Data Volume Model: `The branch should handle missing, invalid, stale, reset, revoked, single-profile, and future multi-provider consent records without broad storage or network scope.`
Configuration And State Model: `Consent persistence remains local-only, versioned, fail-closed, revocable/resettable, and separate from provider profile/config and model execution state.`
Expected User-Facing Outcomes: `No new broad user-facing AI claim; any visible status must say durable consent persistence is local-only and does not mean provider setup or functional AI is complete.`
Acceptance Criteria: `Workstream proof covers durable consent schema, local storage boundary, setup/execution separation, revocation/reset, fail-closed cases, no provider-visible data, disabled execution, validators, H1, LV1/static proof, and PR readiness fold-down.`
User-Facing Proof Standard: `Static Core/Desktop/ORIN proof or hidden telemetry proof is acceptable only if Workstream Entry records the waiver; visible UX requires focused screenshot/live proof.`
Current Branch vs Future Package Boundary: `Current branch is durable consent persistence foundation; future branches own user-operated consent UX, provider setup completion, SDK/model execution, memory, voice/Core, shortcuts/installers, and v1.8.0 release proof.`
Current Branch vs Future Package Boundaries: `Current branch is durable consent persistence foundation; future packages own user-operated consent UX, provider setup completion, SDK/model execution, memory, voice/Core sync, shortcuts/installers, and v1.8.0 release proof.`
Affected Files / Surfaces: `Branch record, branch plan, backlog/roadmap/worktree slots, validation helper registry, governance validator/source truth for confinement repair, desktop provider-state files, Core/Desktop/ORIN status surfaces, and provider-state validator fixtures as admitted later.`
Affected Surfaces: `Branch authority record, Branch Runtime Engineering Plan, feature backlog, prebeta roadmap, worktree slots, validation helper registry, phase governance/index confinement rule, branch governance validator, desktop provider state, Core/Desktop/ORIN status surfaces, and provider-state validator fixtures as admitted by Workstream Entry.`
Data / Control Model: `Local consent data may be persisted locally for future gates; it must not be sent to provider, used to accept prompts, enable model execution, download models, or write memory.`
Data/Control Model: `Durable consent remains local control state only; it may gate later setup decisions but cannot send provider-visible data, accept prompts, execute models, download assets, write memory, call external services, or sync voice/Core runtime.`
Branch Reach / Package-Size Proof: `This branch is large enough for durable consent persistence because it spans schema, storage boundary, revocation/reset, status proof, validation, and phase fold-down, but it remains smaller than provider setup completion or functional AI.`
Branch Reach / Package-Size Review: `PASS - the branch is sized around one coherent prerequisite layer: durable consent persistence schema, local storage boundary, revocation/reset semantics, setup/execution separation, status proof, validator fixtures, and source-truth fold-down.`
Why Branch Is Large Enough: `It contains multiple concrete runtime and proof seams that must agree before provider setup or execution can trust durable consent state.`
Why This Branch Should Not Split Smaller: `Splitting schema, storage boundary, and revocation/reset into separate branches would create fragile partial consent truth; they should be planned together and implemented seam-by-seam.`
Why Not Split Into Tiny Branches: `Splitting schema, storage boundary, revocation/reset, and validation into tiny branches would create partial consent truth and increase release churn before the next FAM-007 provider step.`
Validation Proof Requirements: `Run branch governance validation, worktree confinement gate, release-readiness health gate, governance efficiency validation, release body validation, source-owner marker validation, branch-readiness planning fixture validation, AI provider state validation, runtime-fam007 suite, rebaseline audit, compileall, and any new persistence fixtures.`
Screenshot / Live / User Test Summary Proof Requirements: `No user-operated consent UX is admitted during Stage 2; Workstream Entry must decide whether LV1 uses static source/validator proof, hidden telemetry proof, or later focused screenshot/live proof if visible behavior is admitted.`
Implementation Sequence Proposal: `Stage 2 setup, Workstream Entry whole-package analysis, bounded Workstream implementation, Hardening H1, Live Validation LV1/static proof, PR Readiness, PR creation, merge, and later Release Readiness.`
Planning Blockers: `None for Stage 2; Workstream Entry and runtime implementation approval remain pending.`
USER Decisions Needed: `Approve Workstream Entry analysis next; later approve implementation, PR creation, merge, release, and all future-gated provider/model/memory/voice/shortcut/installer work.`
Planning Packet Status: `Complete`
Planning Revalidation Status: `PASS`
Planning Completion Waiver: `None`
User Test Summary Strategy: `Static validator or hidden-telemetry proof is expected unless Workstream Entry admits visible user-facing consent persistence proof; a formal UTS remains pending or waived until user-operated consent UX exists.`

## Runtime Branch Engineering Contract

Engineering Contract Status: `Accepted for Stage 2 setup; implementation pending Workstream Entry and USER approval.`
USER Engineering Planning Review: `Required - Pending Workstream Entry review.`
Runtime Implementation Approval: `Pending - Stage 2 records planning only.`
Branch Purpose: `Prepare the FAM-007 durable local consent persistence foundation after PR #201 so later user-operated consent UX and provider setup work can rely on versioned, revocable, fail-closed local consent state.`
Current Runtime Baseline: `Released FAM-007 evidence includes setup/consent-flow readiness, setup contract readiness, setup implementation foundation, consent collection foundation, and PR #201 consent capture/write-path foundation released in v1.7.16-prebeta. Provider-visible data remains none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads/network blocked, memory inactive, voice/Core sync gated, and desktop readiness display suppression preserved.`
Planned Runtime Delta: `Durable local consent persistence foundation: consent record persistence schema, local storage boundary, schema versioning, revocation/reset durability, setup/execution consent separation, provenance/audit metadata, fail-closed fixture coverage, and status proof.`
User-Facing Runtime Delta: `Potential status-only proof that durable consent persistence exists locally; no claim of provider setup completion, consent UX completion, provider/model execution, downloads, network, memory, voice/Core sync, or functional AI.`
State / Config / Schema Delta: `Local consent record schema, schema version, storage-boundary marker, setup consent durable state, execution consent durable state, revoked/reset state, provenance, audit timestamp/source fields, and fail-closed reason codes.`
Validator / Helper Delta: `Extend FAM-007 provider-state validation for durable persistence fixtures, revocation/reset, setup/execution durable separation, local-only storage boundary, no provider-visible data, no prompt execution, and static proof/waiver posture; extend branch governance validation for family-scoped Branch Readiness confinement.`
Expected Changed Files / Surfaces: `Docs branch record, branch plan, backlog, roadmap, worktree slot, validation helper registry, phase governance/index confinement rule, branch governance validator, desktop/ai_provider_state.py, desktop/desktop_renderer.py, desktop/core_visualization_renderer.py, nexus_visual/orin_core.* and dev/orin_ai_provider_state_validation.py as admitted by Workstream Entry.`
Approval-Boundary Audit: `Stage 2 changes source truth and validator governance only. Runtime implementation, provider setup completion, user-operated consent UX, provider SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, PR creation, merge, release, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain pending.`
Future-Gated Items: `User-operated consent UX, provider setup completion, SDK/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, release execution, issue work, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta.`
Workstream Seam Map: `Seam 1 -> persistence state/schema; Seam 2 -> local storage boundary and migration posture; Seam 3 -> revocation/reset/expiry persistence semantics; Seam 4 -> setup/execution consent durable separation; Seam 5 -> Core/Desktop/ORIN status proof; Seam 6 -> validator fixtures and future handoff criteria.`
Proof Expectations: `Run branch governance validation, worktree confinement gate, release-readiness health gate, governance efficiency validation, release body validation, source-owner marker validation, branch-readiness planning fixtures, AI provider state validation, runtime-fam007 suite, rebaseline audit, compileall, and any new persistence fixtures before H1/PR readiness.`
Risk Forecast: `Medium risk from consent durability semantics and shared source-truth edits; high-risk provider execution remains excluded.`
Recommendations And Alternatives: `Recommended path is durable consent persistence foundation. Alternative user-operated consent UX is deferred until persistence semantics are stable; provider setup completion and SDK/model execution are premature.`
Plan Version / Revision Status: `v1 created during Branch Readiness Stage 2 after v1.7.16-prebeta release.`
Plan-To-Implementation Traceability: `Each seam maps to planned files, validators, H1 comparison, LV1 proof or waiver, PR fold-down, and release public-scope translation before implementation begins.`

## Branch Runtime Engineering Plan

Branch Runtime Engineering Plan Path: `Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md`
Branch Runtime Engineering Plan: `Accepted for Stage 2 setup.`
Engineering Plan Status: `Accepted - ready for Workstream Entry analysis; implementation remains pending USER approval.`

## Family-Scoped Branch Readiness Confinement

Target Family: `FAM-007`
Target Worktree: `C:\Nexus Worktrees\FAM-007`
Sibling Worktree Candidate Exclusion: `Sibling worktrees are overlap context only and not successor authority. FAM-006, Governance, neutral main, and historical detached worktrees must not become the selected next branch for this FAM-007 Branch Readiness pass unless USER explicitly broadens scope to repo-wide branch selection.`
Drift Prevention: `If a sibling lane appears active, cleaner, or farther along, report it as overlap context only. Stop on Family-Scoped Branch Readiness Drift instead of switching lanes.`

## Assigned Worktree Confinement

Assigned Worktree Confinement: `Required`
Active Thread Owner: `Current Codex thread assigned by USER for FAM-007 Branch Readiness Stage 2 setup`
Thread Assignment Status: `Active for C:\Nexus Worktrees\FAM-007 only`
Worktree Ownership Ledger: `FAM-007 owns this branch, this branch record, this branch plan, compact FAM-007 source-truth pointers, validation helper registry FAM-007 row, and bounded confinement repair carried by this branch.`
Intended Write Set: `FAM-007 branch authority, branch plan, backlog/roadmap/worktree-slot pointers, validation helper registry, phase/index confinement rule, branch governance validator, generated docs inventory if required by validation.`
Same Worktree / Same Branch Collision Check: `PASS - this branch is checked out in C:\Nexus Worktrees\FAM-007 and no same-branch collision is known.`
Dirty Worktree Collision Check: `PASS - clean tracked worktree before Stage 2 edits; no unowned dirty files.`
Dirty Worktree Recovery Packet: `Not required - worktree clean at Stage 2 start.`
Off-Worktree Work Routing: `FAM-006, Governance, neutral main, Compact-AI, and detached historical worktrees are read-only overlap context unless USER grants explicit worktree escape approval.`
Governance Routing Barrier: `Active for governance-only mutation outside this FAM-007 branch path; this branch carries only the bounded confinement repair tied to the FAM-007 Stage 2 setup.`
New Worktree Decision Gate: `No new worktree, cleanup, deletion, or rebinding is authorized.`
Expected Worktree Root: `C:\Nexus Worktrees\FAM-007`
Actual Worktree Root: `C:\Nexus Worktrees\FAM-007`
No Cross-Worktree Mutation: `Required`
GitHub Desktop-bound worktree: `Preserve C:\Nexus Worktrees\FAM-007 binding; no cleanup/rebinding authorized.`
Worktree Escape User Waiver: `Not granted`
Worktree Escape User Waiver Missing: `Blocks mutation outside C:\Nexus Worktrees\FAM-007.`

## Release Closure And Prior Evidence

v1.7.16-prebeta Release Truth: `Published GitHub prerelease at 10c32804370ee5480416e68e55823e5997d18291.`
PR #201 Release Closure: `PR #201 FAM-007 Local AI Provider Consent Collection Implementation Foundation is released evidence in v1.7.16-prebeta.`
Prior Released Evidence: `PR #193 consent collection foundation, PR #192 setup implementation foundation, PR #190 setup contract readiness, and PR #179 setup/consent-flow readiness remain released FAM-007 evidence.`

## FAM / Shared-Surface Overlap Forecast

FAM-006 Overlap: `Separate lane; overlap context only; no FAM-006 mutation or successor authority.`
Governance Overlap: `Standing intake context; no Governance worktree mutation.`
Compact-AI Posture: `Historical released/salvaged evidence; no mutation.`

## Validation Plan

Required Validation: `git diff --check origin/main...HEAD; git diff --check; python dev\orin_branch_governance_validation.py; python dev\orin_branch_governance_validation.py --worktree-confinement-gate; python dev\orin_branch_governance_validation.py --release-readiness-health-gate; python dev\orin_governance_efficiency_validation.py; python dev\orin_release_body_validation.py; python dev\orin_source_owner_marker_validation.py; python dev\orin_branch_readiness_planning_fixture_validation.py; python dev\orin_ai_provider_state_validation.py; python dev\orin_validation_suite.py --phase branch-readiness; python dev\orin_validation_suite.py --phase runtime-fam007; python dev\orin_worktree_rebaseline_audit.py --target-ref origin/main --cwd "C:\Nexus Worktrees\FAM-007" --branch-plan-path Docs\branch_plans\feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md; python -m compileall -q dev desktop Audio main.py.`

## Formal Next Legal Phase Digest

Current Phase: `Branch Readiness`
Next Legal Phase: `Workstream`
Why This Phase Is Next: `Stage 2 creates the fresh FAM-007 durable consent persistence carrier, records v1.7.16 release closure, admits the plan and branch authority, and repairs family-scoped Branch Readiness confinement. Workstream Entry must inspect the plan before implementation.`
Approval Required: `USER approval required for Workstream Entry analysis.`
Exact USER Approval Text: `I approve Workstream Entry analysis for feature/fam-007-local-ai-provider-durable-consent-persistence-foundation in C:\Nexus Worktrees\FAM-007 from origin/main@10c32804370ee5480416e68e55823e5997d18291. Scope: inspect the admitted FAM-007 durable local consent persistence foundation plan, Branch Runtime Engineering Plan, Product Definition Plan, Runtime Branch Engineering Contract, family-scoped confinement repair, prior PR #201 released evidence, validation requirements, proof expectations, and approval boundaries; return the engineering design packet and exact implementation decision. Do not implement runtime behavior, create PRs, merge, release, clean branches/worktrees, mutate sibling worktrees, provider setup completion, SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.`
Allowed Scope: `Workstream Entry analysis only after Stage 2; no implementation until later USER approval.`
Explicit Exclusions: `No runtime implementation, provider setup completion, user-operated consent UX, SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release, branch/worktree cleanup, sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.`
Validation Required: `Workstream Entry should rerun branch governance, worktree confinement, release-readiness health, governance efficiency, release body, source-owner marker, planning fixture, AI provider state, runtime-fam007 suite, rebaseline audit, and compileall as applicable.`
Stop Conditions: `Stop if origin/main advances, the worktree is dirty, source truth points to another FAM-007 carrier, family-scoped confinement fails, validation fails, or any step requires a pending USER decision.`
USER Plan Review Gate: `USER may accept, revise, waive, or reject this Stage 2 plan before Workstream Entry or implementation.`
USER Inspection Files: `Docs/branch_records/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md; Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md; Docs/phase_governance.md; Docs/branch_records/index.md; Docs/validation_helper_registry.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md; Docs/worktree_slots.md; dev/orin_branch_governance_validation.py.`
Review Required Because: `The branch admits the next FAM-007 runtime planning carrier and patches Branch Readiness confinement behavior.`
Implementation Blocker: `Runtime implementation remains blocked until Workstream Entry analysis and later USER implementation approval.`
Review Waiver Reason: `Not waived.`
