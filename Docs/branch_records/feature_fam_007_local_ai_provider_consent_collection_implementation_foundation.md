# Branch Record: feature/fam-007-local-ai-provider-consent-collection-implementation-foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-consent-collection-implementation-foundation; surface=branch-record; status=canonical

## Record State

Record State: `Active Branch Authority`

## Status

Status: `Workstream implementation active - Seam 1 local consent capture state transition and local write-path foundation is implemented pending final validation/commit; Seam 2 remains pending USER approval.`

## Canonical Branch

Canonical Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`

## Current Phase

Phase: `Workstream`

Stage: `Seam 1`

Seam: `FAM-007 Local AI Provider Consent Collection Implementation Foundation`

## Phase Status

- Branch Authority Marker: `Active Branch Authority`
- Branch Authority Type: `Active Branch`
- Active Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`
- Branch Evidence: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`
- Branch Authority State: `Active FAM-007 runtime carrier for bounded Workstream implementation`
- Stage 2 Status: `Complete after source-truth setup, branch plan creation, validation, commit, and push`
- Workstream Status: `In progress - Seam 1 local consent capture state transition and local write-path foundation implemented; Seam 2 pending USER approval`
- Prior FAM-007 Evidence: `PR #193 FAM-007 consent collection foundation is merged and released evidence from v1.7.13-prebeta; PR #192 setup implementation foundation remains released evidence from v1.7.12-prebeta; PR #190 setup contract readiness and PR #179 setup/consent-flow readiness remain released historical evidence`
- Consent Collection Implementation State: `Seam 1 implemented - local consent capture transition/write-path snapshot fields, local record normalization, missing/invalid/no-selection/revoked/reset/captured-local-only fail-closed behavior, and validator fixtures are present; durable storage boundary and expanded revocation model remain Seam 2 pending USER approval`
- Provider Execution State: `Blocked - provider setup completion, provider SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, AI Product import, and v1.8.0-prebeta execution remain pending USER decisions`
- Next Active Seam: `Seam 2 consent record schema, storage boundary, and revocation model after USER approval`

## Branch Class

`implementation`

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8`
- Latest public prerelease baseline: `v1.7.15-prebeta`
- Latest public prerelease release commit: `3e769d0670937232afc3f5e767f5a3baf2f2c945`
- Current origin/main at branch creation: `a42b7e50eb012722b140f3874dbf50826bd797c8`
- Current origin/main includes post-release governance commits after `v1.7.15-prebeta`: `PR #198` and `PR #199`
- Prior consent foundation branch: `feature/fam-007-local-ai-provider-consent-collection-foundation`
- Prior consent foundation PR: `PR #193`

## Carrier Lifecycle Decision

Carrier Lifecycle Classification: `Fresh current branch`

Remote Branch State: `Absent before Stage 2 setup; remote branch is created by this Stage 2 push`

Unique Branch Diff: `None at creation - branch created from current origin/main before Stage 2 source-truth edits`

Origin/Main Ancestry: `Created from origin/main at a42b7e50eb012722b140f3874dbf50826bd797c8`

Origin/Main Advanced Since Branch Creation: `NO at setup time`

Open PR State: `No PR exists for this branch during Stage 2 setup; PR creation remains pending USER approval`

Worktree Checkout State: `Checked out in C:\Nexus Worktrees\FAM-007`

Recommended Stage 2 Carrier Action: `Use this fresh branch as the FAM-007 consent collection implementation foundation carrier`

Stale Branch Cleanup Plan: `Deferred - previous FAM-007 branches are historical released evidence and remain protected until later USER-approved cleanup/rebinding analysis`

Branch Cleanup Execution Gate: `Blocked - no branch deletion, worktree removal, or GitHub Desktop cleanup is authorized by this Stage 2 setup`

Recreate From Current origin/main: `Complete - branch created from current origin/main`

No Unique Commit Loss Proof: `PASS - no existing target branch or unique target commits were overwritten`

## Bounded State

Allowed Scope: `Current approval covers Seam 1 local consent capture state transition and local write-path foundation, provider-state validator fixtures, and directly required branch-local source-truth updates. Seam 2 and all provider/model/network/memory/voice/release/PR/merge/cleanup work remain excluded.`

Write Target: `C:\Nexus Worktrees\FAM-007` on `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`

Non-Includes: `Runtime implementation, actual consent capture, provider setup completion, provider SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release/tag/GitHub Release/artifact work, issue work, FAM-006 mutation, Governance mutation outside this branch path, Compact-AI mutation, branch/worktree cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`

Pending USER Decisions: `Seam 2 execution, durable consent storage-boundary expansion, provider setup completion, SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release/tag/GitHub Release/artifact work, issue work, branch/worktree cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`

## Blockers

No Seam 1 blocker remains if validation is green. Seam 2 consent record storage-boundary work and all provider/model/network/memory/voice/installer/release/PR/merge/cleanup actions remain blocked until separately approved.

## Entry Basis

USER approved Branch Readiness Stage 2 setup in `C:\Nexus Worktrees\FAM-007` to create `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation` from `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8`. USER also directed that PR #193 consent collection foundation be treated as already merged and released evidence and that this successor distinguish actual local consent capture/write-path implementation foundation from the prior disabled/status-only consent scaffolding.

## Exit Criteria

- Fresh FAM-007 branch exists from current `origin/main`.
- Branch authority record and Branch Runtime Engineering Plan exist.
- Product Definition Plan fields are recorded.
- Runtime Branch Engineering Contract fields are recorded.
- Bounded Workstream plan is admitted for actual local consent capture/write-path implementation foundation.
- PR #193 is recorded as merged and released FAM-007 consent foundation evidence.
- FAM-006 and Governance overlap are recorded as later PR/merge reconciliation risk.
- Compact-AI protected unique-commit work remains preserved as historical released/salvaged evidence.
- Validation is green.
- Stage 2 setup commit is pushed.

## Rollback Target

`Branch Readiness`

Rollback Details: Return `C:\Nexus Worktrees\FAM-007` to `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8` only under explicit USER-approved rollback.

## Planning-Loop Guardrail

Implementation Delta Class: `backend/runtime, runtime/user-facing`

Docs-Only Workstream: No

Planning-Loop Bypass User Approval: `None`

Planning-Loop Bypass Reason: None

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`

Backlog-Split User Approval: `None`

Backlog-Split Reason: None

## Admitted Implementation Slice

Slice: FAM-007 consent collection implementation foundation, covering local consent capture state transitions, local write-path foundation, consent record schema, storage boundary, revocation/reset posture, setup consent and execution consent separation, provenance/audit posture, provider-visible-data none, no-secrets posture, UI/status proof if later admitted, validator fixtures, fail-closed behavior, and future provider setup handoff without enabling provider setup completion or provider/model execution.

## Branch Objective

Create the FAM-007 consent collection implementation foundation carrier after PR #193 merged and released, recording the exact local consent capture/write-path planning boundary before any runtime implementation begins.

## Target End-State

This branch should become a validated FAM-007 local consent capture/write-path implementation foundation with branch authority, Product Definition Plan, Runtime Branch Engineering Contract, Branch Runtime Engineering Plan, Workstream Entry, implementation, H1, LV1, PR Readiness, and release fold-down complete without claiming provider setup completion, SDK/model execution, downloads, network, memory, voice/Core sync, or functional AI.

## Backlog Completion Strategy

Branch Completion Goal: `Complete a bounded FAM-007 consent collection implementation foundation slice without claiming PKG-007 completion or operational AI.`

Known Future-Dependent Blockers: `Provider setup completion, SDK/model execution, downloads, network/API calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, PR, merge, release, issue work, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain pending USER decisions.`

Branch Closure Rule: `This branch can close only after its admitted Workstream is implemented, hardened, live-validated or waived by source truth, PR-readied, merged, and folded down without stale active-branch or release-canon drift.`

## Backlog Completion Status

Backlog Completion State: In Progress

Remaining Implementable Work: `Remaining bounded seams include Seam 2 consent record schema/storage boundary/revocation model, Seam 3 setup and execution consent separation, Seam 4 provenance/audit/no-secrets contract, Seam 5 Core/Desktop/ORIN proof if admitted, Seam 6 validator/handoff expansion, and Seam 7 functional-AI/v1.8.0 continuation criteria.`

Future-Dependent Blockers: `Provider setup completion, SDK/model execution, downloads, network/API calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, PR, merge, release, issue work, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain pending USER decisions.`

Completion Status: Red

## Expected Seam Families And Risk Classes

- Consent Capture State Transition and Local Write Path: write-path risk; no provider setup completion.
- Consent Record Schema, Storage Boundary, and Revocation Model: storage/privacy risk; no secrets, prompts, model artifacts, or memory indexes.
- Setup Consent / Execution Consent Capture Separation: boundary risk; setup consent must not imply execution approval.
- Provenance, Audit, Provider-Visible Data, and No-Secrets Contract: privacy/audit risk; provider-visible data remains none.
- Core/Desktop/ORIN Consent Capture UI and Status Proof: copy/proof risk; no functional-AI claim.
- Validator Fixtures, Fail-Closed Behavior, and Future Provider Setup Handoff: validator risk; fail-closed posture required.
- Functional-AI and v1.8.0 Continuation Criteria: release/expectation risk; no v1.8.0 execution.

## User Test Summary Strategy

User Test Summary Strategy: Seam 1 remains static/validator-backed with no user-operated consent surface; static Core/Desktop/ORIN source truth plus `dev/orin_ai_provider_state_validation.py` remains the applicable substitute and User Test Summary may be waived by source truth. Later visible consent UI requires a separate USER decision.

## Later-Phase Expectations

Later-Phase Expectations: Workstream Entry defines exact implementation design; Workstream implementation executes only admitted seams; H1 compares implementation against this plan and contract; LV1 proves local-only safety and any visible consent posture; PR Readiness folds down selected-next/defer and release-window truth; Release Readiness remains a later USER decision.

## Initial Workstream Seam Sequence

Seam 1: Consent Capture State Transition and Local Write Path.

Status: `Implemented in this Workstream pass pending validation/commit.`

Goal: Define and implement local consent capture state transitions plus a fail-closed local write path.

Scope: Local consent state, write-path validation, blocker/reason/provenance fields, local record normalization, validator fixtures, and approval-boundary preservation.

Proof: `desktop/ai_provider_state.py` adds local consent capture/write-path snapshot state and `dev/orin_ai_provider_state_validation.py` adds missing, invalid, no-selection, revoked, reset, setup-only, setup+execution, and blocked-by-collection fixtures while preserving provider-visible data none and disabled execution.

Non-Includes: Durable consent storage boundary expansion, provider setup completion, provider SDK/model execution, downloads, network calls, memory, voice/Core sync, shortcuts/installers, PR creation, merge, release, cleanup, and cross-worktree mutation.

Seam 2: Consent Record Schema, Storage Boundary, and Revocation Model.

Seam 3: Setup Consent / Execution Consent Capture Separation.

Seam 4: Provenance, Audit, Provider-Visible Data, and No-Secrets Contract.

Seam 5: Core/Desktop/ORIN Consent Capture UI and Status Proof.

Seam 6: Validator Fixtures, Fail-Closed Behavior, and Future Provider Setup Handoff.

Seam 7: Functional-AI / v1.8.0 Continuation Criteria.

## Active Seam

Active seam: `Seam 2 consent record schema, storage boundary, and revocation model - stopped by USER Seam 1-only waiver until approved`

Goal: Preserve local consent capture/write-path proof and proceed only to Seam 2 when USER approves.

Scope: Seam 1 local consent capture transition/write-path proof, validator fixtures, source-truth update, validation, commit, and push.

Non-Includes: Seam 2 storage-boundary expansion, provider setup completion, provider execution, PR creation, merge, release execution, cleanup, and sibling worktree mutation.

Next Active Seam: `Seam 2 consent record schema, storage boundary, and revocation model after USER approval`

## Seam Continuation Decision

Seam Status: Green

Slice Status: Blocked

Completion Status: Red

Waiver Status: Approved

Continue Decision: Stop

Continuation Execution Latch: Inactive - USER approved this run for Seam 1 only; Seam 2 continuation is paused by USER waiver until the waiver is cleared.

Stop Basis: Waiver

Next Active Seam: Seam 2 consent record schema, storage boundary, and revocation model.

Stop Condition: USER-approved Seam 1-only execution boundary.

Continuation Action: USER approval for Seam 2 clears the waiver and resumes the Workstream on Seam 2; provider setup completion, SDK/model execution, downloads/external calls, memory, voice/Core sync, PR creation, merge, release execution, cleanup, and sibling-worktree mutation remain excluded.

Single-Seam Workstream Waiver: USER approved Seam 1-only execution for this pass and left Seam 2 as a pending USER decision.

Single-Seam Or Single-Slice Waiver Authority: USER only; Codex cannot infer single-seam or single-slice Workstream stop authority.

Single-Seam Or Single-Slice Workstream Blocker: One seam or one slice visible is a blocker unless USER waiver approval records the stop.

Bounded Seam Default: Bounded means one active seam at a time, not one-seam Workstream authority.

Remaining Implementable Work: `Remaining bounded seams include Seam 2 consent record schema/storage boundary/revocation model, Seam 3 setup and execution consent separation, Seam 4 provenance/audit/no-secrets contract, Seam 5 Core/Desktop/ORIN proof if admitted, Seam 6 validator/handoff expansion, and Seam 7 functional-AI/v1.8.0 continuation criteria.`

## Product Definition Plan

Product Vision: FAM-007 should become useful local AI through cautious, inspectable setup and consent steps that keep users in control of consent, provider-visible data, and provider execution before any model can run.

User-Facing Goal: Prepare the next branch to implement a local consent capture/write-path foundation that can record explicit local setup/execution consent intent without implying provider setup completion, prompt acceptance, provider/model execution, network activity, memory activity, or functional AI.

Project-Wide Vision Alignment: The branch advances the local-first AI direction by moving from disabled/status-only consent foundation into a governed local consent write-path prerequisite before provider setup completion or model execution.

Branch-Specific Vision Alignment: This branch owns consent capture/write-path implementation foundation planning and future bounded implementation only; it does not own provider setup completion, SDK/model integration, memory, voice/Core sync, shortcuts/installers, release execution, or v1.8.0 promotion.

USER Vision Questions: USER prefers detailed branches over broad sweeps; this carrier packages a narrow but real prerequisite layer and keeps later provider setup/execution work separate.

Codex Product Interpretation: Consent capture must be explicit, local, auditable, reversible or revocation-aware, and separated between setup consent and execution consent before provider work can be trusted.

Codex Implementation Recommendation: Admit a bounded Workstream that implements local consent state transitions, write-path validation, provenance/audit posture, UI/status proof, fail-closed fixtures, and future provider setup handoff without enabling provider/model execution.

Codex Additional Recommendations: Recommendation: keep the first implementation pass local-only, offer the narrower state/write-path-only option if UI risk is high, use short status copy, preserve provider-visible data as none, and do not store secrets, prompts for provider use, credentials, model artifacts, or memory indexes.

USER/ChatGPT Review Checkpoint: Seam 1 uses the accepted Workstream Entry boundary for local state/write-path and validator proof; Seam 2 should review durable storage-boundary and expanded revocation posture before implementation.

USER Critique Loop: USER may accept the Workstream Entry plan, narrow the implementation to state/write-path only, defer visible UI work, or require additional branch splitting before implementation.

USER Decision Ledger: USER approved Workstream implementation for Seam 1 only; Seam 2 execution, PR creation, merge, release, cleanup, provider setup completion, model execution, and v1.8.0 execution remain pending.

Deferred Ideas / Future Package Ledger: Provider setup completion, provider adapter/SDK boundary, prompt routing, model execution, model downloads, external provider/API calls, memory/indexing/learning/personalization, voice/Core runtime sync, capability packs, shortcuts/installers, and AI Product Contract import remain future branches.

Planning Adequacy Review: This plan is not shallow because it covers end-to-end consent capture boundaries from product intent through state/schema, write path, UI/status proof, validator fixtures, release fold-down, future provider setup handoff, and explicit exclusions for provider/model/network/memory work.

Rejected Shallow Plan: Rejected simple plan: "just add consent capture" without schema, provenance, fail-closed validation, setup/execution separation, UI copy proof, and release fold-down; that would be insufficient because consent affects provider setup, execution approval, privacy, and release claims.

Alternatives And Tradeoffs Reviewed: A narrower docs-only branch would not move FAM-007 toward operational AI; a broader provider setup plus consent branch would be higher risk and blur consent, setup, and execution boundaries. This carrier is the middle path.

Full Feature Element Breakdown: local consent state, setup consent posture, execution consent posture, capture eligibility, write-path validation, blocker/reason codes, provenance, audit posture, revocation or reset posture, provider-visible data posture, Core/Desktop/ORIN status proof, validator fixtures, and future handoff markers.

System Concept Model: Consent state is local application state that gates later provider setup and provider execution; it is not provider communication, model execution, memory, or functional AI.

Entity / Profile Model: The branch may define local consent record fields, provider profile/config references, consent subject/scope labels, setup/execution consent flags, provenance, schema version, and audit timestamps without importing secrets or provider credentials.

User Workflow Model: A later implementation should let the app truthfully move from consent unavailable/blocked/future-gated to locally captured consent posture only after explicit USER-approved UI/write-path work; this Stage 2 does not implement that workflow.

Scale / Data Volume Model: Consent state is small local metadata with a handful of local records across multiple states, provider profiles, config references, UI surfaces, validator fixture files, and future sources; no prompt corpus, model data, provider payload, memory index, external log stream, or long-term personalization store is admitted.

Configuration And State Model: Consent capture write-path state must fail closed when provider path, profile/config, setup approval, execution approval, policy, safety, manifest, network, memory, or voice/Core gates are not satisfied.

Whole-System Interaction Map: FAM-007 consent state feeds later provider setup completion, provider execution approval, UI status, validators, PR/release fold-down, and functional-AI criteria while FAM-006 HUD work and Governance intake remain separate lanes.

Minimum Viable vs Full System Boundary: Minimum viable scope is local consent capture/write-path foundation and proof; full system scope includes provider setup completion, SDK/model execution, prompt routing, external/network behavior, memory, voice/Core, packaging/install, and release milestone work.

Open Questions / USER Decision Points: USER decisions remain required for Seam 2 consent record schema/storage boundary, expanded revocation posture, visible UI scope beyond validator-visible state, and whether later implementation should include any user-operable consent surface or remain internal foundation first.

Expected User-Facing Outcomes: If later implementation is approved, users should see truthful local consent readiness/capture status without any claim that provider setup is complete, prompts can be accepted, models can run, or functional AI is available.

Acceptance Criteria: Stage 2 is complete when branch authority, plan, compact pointers, worktree slot receipt, validation helper registry posture, validation, commit, and push are complete.

Current Branch vs Future Package Boundaries: Current branch may later implement local consent capture/write-path foundation; future package work owns provider setup completion, adapter/SDK integration, prompt routing, model execution, memory, voice/Core sync, capability packs, shortcuts/installers, and v1.8.0 release proof.

Affected Surfaces: Branch authority record, Branch Runtime Engineering Plan, backlog, roadmap, worktree slots, validation helper registry, provider state, desktop/Core renderers, ORIN surfaces, and provider-state validator.

Data/Control Model: Consent capture remains local control state and cannot send prompts, provider-visible data, secrets, credentials, model requests, memory records, or network payloads.

Branch Reach / Package-Size Review: The branch is large enough because it spans local consent state, write path, schema, storage boundary, revocation posture, setup/execution separation, UI/status proof, validators, and release fold-down while staying below provider setup completion and model execution.

Why Branch Is Large Enough: It contains multiple concrete seams and proof surfaces that together form a real FAM-007 prerequisite, not a tiny one-file or marker-only change.

Why Not Split Into Tiny Branches: Splitting state, write path, provenance, validator fixtures, and UI proof into separate branches would increase release churn and weaken consent-boundary traceability before provider setup work.

Validation Proof Requirements: Workstream implementation must pass branch governance, release-health, governance efficiency, release body, source-owner marker, AI provider state, branch-readiness planning fixture, runtime-fam007 suite, rebaseline audit, compileall, and any new consent fixtures.

Screenshot / Live / User Test Summary Proof Requirements: Seam 1 has no user-operated local consent capture path; LV1 should use static validator evidence and record the source-truth-supported User Test Summary waiver unless a later seam admits visible UI.

Implementation Sequence Proposal: First implement local state/schema and write path, then storage/revocation posture, setup/execution separation, provenance/audit/no-secrets posture, UI/status proof if admitted, validator fixtures, and fold-down.

Planning Blockers: Seam 1 implementation is approved and recorded here; Seam 2, provider setup completion, and provider/model execution remain separate blockers.

USER Decisions Needed: USER must approve Seam 2 execution, PR creation, merge, release execution, provider setup completion, SDK/model execution, downloads/external calls, memory, voice/Core sync, shortcuts/installers, cleanup, AI Product import, Private Dev ORIN import, and v1.8.0 execution.

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

Planning Completion Waiver: `None`

User Test Summary Strategy: `Seam 1 uses source-truth-supported static waiver because no user-operated local consent capture path is admitted.`

## Runtime Branch Engineering Contract

Engineering Contract Status: `Accepted for Stage 2 setup; implementation approval remains pending.`

USER Engineering Planning Review: `Complete for Seam 1 via accepted Workstream Entry; required again if Seam 2 scope changes the consent record schema/storage boundary beyond the admitted plan.`

Runtime Implementation Approval: `Approved for Seam 1 only; Seam 2 and later runtime/product work remain pending.`

Branch Purpose: `Move FAM-007 from disabled/status-only consent foundation toward local consent capture/write-path implementation foundation while preserving provider setup completion and model execution as future decisions.`

Current Runtime Baseline: `Released FAM-007 state includes setup/consent-flow readiness, setup contract readiness, setup implementation foundation, and disabled/status-only consent collection foundation evidence through PR #193. Provider-visible data remains none, sentToProvider=false, canAcceptPrompts=false, prompt/model execution disabled, downloads/network blocked, memory disabled or deferred, voice/Core sync gated, and desktop readiness display suppression preserved.`

Planned Runtime Delta: `Future Workstream may implement local consent capture/write-path foundation, consent record schema, setup/execution consent separation, provenance/audit posture, fail-closed validation, local-only UI/status proof, and future provider setup/execution handoff.`

User-Facing Runtime Delta: `Future Workstream may add truthful local consent capture/status proof if admitted; it must not imply provider setup completion, provider/model execution, prompt acceptance, network activity, memory activity, voice/Core sync, or functional AI.`

State / Config / Schema Delta: `Future Workstream may add consent capture state, local consent record schema, schema versioning, setup consent and execution consent status, provenance, audit markers, revocation/reset posture, reason/blocker codes, provider profile/config references, and future handoff fields.`

Validator / Helper Delta: `dev/orin_ai_provider_state_validation.py should extend existing FAM-007 consent foundation coverage for local consent capture/write-path fixtures, fail-closed validation, setup/execution consent separation, provider-visible-data none, prompt/model execution disabled, downloads/network/memory/voice gates, and desktop readiness display suppression continuity.`

Expected Changed Files / Surfaces: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`, `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`, compact current-state pointer docs, `Docs/validation_helper_registry.md`, `desktop/ai_provider_state.py`, `desktop/desktop_renderer.py`, `desktop/core_visualization_renderer.py`, `nexus_visual/orin_core.*`, and `dev/orin_ai_provider_state_validation.py` if Workstream implementation is later approved.

Approval-Boundary Audit: `Stage 2 records planning and branch authority only. Actual runtime implementation, consent capture, provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, PR creation, merge, release, issue work, cleanup, cross-lane mutation, AI Product import, Private Dev ORIN import, and v1.8.0 execution remain pending USER decisions.`

Future-Gated Items: `Provider setup completion, provider SDK integration, provider/model execution, model downloads, external/API calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release/tag/GitHub Release/artifact work, issue work, FAM-006 mutation, Governance mutation outside this branch path, Compact-AI mutation, branch/worktree cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`

Workstream Seam Map: `Seam 1 - Consent Capture State Transition and Local Write Path; Seam 2 - Consent Record Schema, Storage Boundary, and Revocation Model; Seam 3 - Setup Consent / Execution Consent Capture Separation; Seam 4 - Provenance, Audit, Provider-Visible Data, and No-Secrets Contract; Seam 5 - Core/Desktop/ORIN Consent Capture UI and Status Proof; Seam 6 - Validator Fixtures, Fail-Closed Behavior, and Future Provider Setup Handoff; Seam 7 - Functional-AI / v1.8.0 Continuation Criteria.`

Proof Expectations: `H1 must compare Seam 1 implementation to this contract with validator fixture proof from dev/orin_ai_provider_state_validation.py. LV1 must prove local-only safety, provider-visible-data none, sentToProvider=false, canAcceptPrompts=false, prompt/model execution disabled, downloads/network/memory/voice gates, and desktop readiness display suppression continuity.`

Risk Forecast: `consent/setup boundary blur, accidental provider-visible data, premature prompt acceptance, stale UI copy, silent consent capture, over-broad storage, network/memory side effects, validator gap, and release expectation drift.`

Recommendations And Alternatives: `Preferred path is this bounded implementation foundation. Safer narrower option is internal state/write-path only with no visible consent UI. Larger future branch is provider setup completion plus consent enforcement after this foundation is validated.`

Plan Version / Revision Status: `v1 - created during Branch Readiness Stage 2 from origin/main at a42b7e50eb012722b140f3874dbf50826bd797c8.`

Plan-To-Implementation Traceability: `Each admitted Workstream seam must map to planned state/config/schema fields, UI/status proof if any, validator fixtures, source-truth fold-down, approval boundary, and rollback expectation; H1 must compare those planned deltas with actual implementation before green.`

## Branch Runtime Engineering Plan

Branch Runtime Engineering Plan Path: `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`

Branch Runtime Engineering Plan: `Accepted for Stage 2 setup and Workstream Entry; Seam 1 implementation maps to the plan and later seams remain pending USER approval.`

Engineering Plan Status: `Accepted / implementation pending`

PR Fold-Down Packet: `Pending - PR Readiness will decide selected-next/defer, release-window, active-authority cleanup, PR metadata, and release fold-down after Workstream, H1, and LV1 are complete.`

## Workstream Admission

Workstream Label: `FAM-007 Local AI Provider Consent Collection Implementation Foundation`

Workstream Admission State: `Admitted for bounded Workstream implementation; Seam 1 implemented and Seam 2 pending USER approval`

Workstream Definition: `Actual local consent capture/write-path implementation foundation is the next FAM-007 layer after disabled/status-only consent collection foundation. It should implement local consent state transitions, local write-path validation, provenance/audit posture, setup/execution consent separation, local-only UI/status proof if admitted, validator fixtures, fail-closed behavior, and future provider setup/execution handoff while keeping provider setup completion and model execution pending.`

Admitted Seam Families:

1. Consent Capture State Transition and Local Write Path.
2. Consent Record Schema, Storage Boundary, and Revocation Model.
3. Setup Consent / Execution Consent Capture Separation.
4. Provenance, Audit, Provider-Visible Data, and No-Secrets Contract.
5. Core/Desktop/ORIN Consent Capture UI and Status Proof.
6. Validator Fixtures, Fail-Closed Behavior, and Future Provider Setup Handoff.
7. Functional-AI / v1.8.0 Continuation Criteria.

Implementation Gate: `Open for Seam 1 only under current USER approval; closed for Seam 2 and later work until USER approves.`

## Release Baseline And Prior Evidence

Latest Public Prerelease: `v1.7.15-prebeta`

Latest Public Release Commit: `3e769d0670937232afc3f5e767f5a3baf2f2c945`

Current origin/main: `a42b7e50eb012722b140f3874dbf50826bd797c8`

Post-Release Governance Context: `origin/main includes PR #198 and PR #199 after the v1.7.15-prebeta release baseline; this Stage 2 branch is created from that current main.`

PR #193 Released Evidence: `Merged and released FAM-007 Local AI Provider Consent Collection Foundation evidence; it is the immediate predecessor and remains disabled/status-only consent scaffolding rather than actual consent capture/write-path implementation.`

Predecessor Distinction: `This successor targets local consent capture/write-path implementation foundation; the predecessor PR #193 remains consent foundation, status proof, and future-gated readiness evidence.`

## FAM / Shared-Surface Overlap Forecast

FAM-006 Overlap Forecast: `Later PR/merge reconciliation risk only; this branch must not mutate C:\Nexus Worktrees\FAM-006 or FAM-006 work. Shared docs, desktop renderer adjacency, nexus_visual surfaces, and validators must be reconciled through governed PR/merge sequencing if both lanes advance.`

Governance Overlap Forecast: `Standing intake context only; this branch must not mutate C:\Nexus Worktrees\Governance. Governance changes after branch creation require Pre-Rebaseline Impact Audit or later reconciliation before merge-sensitive work.`

Compact-AI Preservation Posture: `Preserved as historical released/salvaged evidence; this branch does not mutate Compact-AI content, cleanup, abandonment, or branch/worktree state.`

## Assigned Worktree Confinement

Active Thread Owner: `Current Codex thread assigned by USER for FAM-007 Stage 2 setup`

Thread Assignment Status: `Active for C:\Nexus Worktrees\FAM-007 only`

Worktree Ownership Ledger: `This branch record and Docs/worktree_slots.md runtime-active-1 receipt`

Intended Write Set: `FAM-007 branch authority record, branch plan, compact FAM-007 pointers, validation helper registry, worktree slot receipt, and validation-produced source truth if required`

Same Worktree / Same Branch Collision Check: `PASS at Stage 2 setup - target branch created in FAM-007 worktree`

Dirty Worktree Collision Check: `PASS at Stage 2 setup - worktree clean before source-truth edits`

Dirty Worktree Recovery Packet: `Not required unless worktree becomes dirty outside this approved setup`

Off-Worktree Work Routing: `Route FAM-006, Governance, Compact-AI, neutral main, or parked-worktree mutation requests back to the owning lane`

Governance Routing Barrier: `Active - governance-only mutation outside this branch path routes to C:\Nexus Worktrees\Governance`

New Worktree Decision Gate: `Pending USER approval for any new worktree or stable worktree rebinding beyond this FAM-007 carrier`

Expected Worktree Root: `C:\Nexus Worktrees\FAM-007`

Actual Worktree Root: `C:\Nexus Worktrees\FAM-007`

No Cross-Worktree Mutation: `Required`

GitHub Desktop-bound worktree: `Preserve C:\Nexus Worktrees\FAM-007 binding; no cleanup/rebinding authorized`

## Validation Plan

Required Validation:

- `git diff --check origin/main...HEAD`
- `git diff --check`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`
- `python dev\orin_governance_efficiency_validation.py`
- `python dev\orin_release_body_validation.py`
- `python dev\orin_ai_provider_state_validation.py`
- `python dev\orin_source_owner_marker_validation.py`
- `python dev\orin_branch_readiness_planning_fixture_validation.py`
- `python dev\orin_validation_suite.py --phase runtime-fam007`
- `python dev\orin_worktree_rebaseline_audit.py --target-ref origin/main`
- `python -m compileall -q dev desktop Audio main.py`

## Next Legal Phase

`Workstream`

## Formal Next Legal Phase Digest

Current Phase: `Workstream`

Next Legal Phase: `Workstream`

Why This Phase Is Next: `Seam 1 records local consent capture state transition/write-path foundation and validator proof; the next seam expands consent record schema, storage boundary, and revocation model, which remains a separate USER decision.`

Approval Required: `USER approval to execute Seam 2 for feature/fam-007-local-ai-provider-consent-collection-implementation-foundation in C:\Nexus Worktrees\FAM-007.`

Exact USER Approval Text: `Approve Seam 2 Workstream implementation for feature/fam-007-local-ai-provider-consent-collection-implementation-foundation in C:\Nexus Worktrees\FAM-007 from origin/main@6681131c974d99945c494c0e4ff3c436f9347422. Scope: implement consent record schema, storage boundary, and revocation model on top of the Seam 1 local consent capture/write-path foundation; update required validator fixtures and branch-local source truth; keep provider setup completion, SDK/model execution, downloads/external calls, memory/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release execution, cleanup, sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution pending.`

USER Plan Review Gate: `Seam 1 plan review was satisfied by Workstream Entry; USER may accept, narrow, change, or defer Seam 2 before storage-boundary work begins.`

Implementation Blocker: `Seam 2 and all later runtime/product work remain blocked until USER approval.`

Allowed Scope: `Next phase is Seam 2 implementation only if USER approves.`

Explicit Exclusions: `Runtime implementation, actual consent capture, provider setup completion, SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release/tag/artifact work, issue work, branch/worktree cleanup, cross-lane mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`

Validation Required: `Diff checks, branch governance, release health, governance efficiency, release body, source-owner marker, branch-readiness planning fixture validation, FAM-007 provider-state validation, runtime-fam007 suite, worktree rebaseline audit, compileall, and any Seam 2-specific consent validator fixture checks.`

Stop Conditions: `Stop if origin/main advances and reconciliation is needed, source truth points to another carrier, FAM-006/Governance/Compact-AI posture creates a direct sequencing decision, or implementation would be required before USER approval.`
