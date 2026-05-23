# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Consent Collection Implementation Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-consent-collection-implementation-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Consent Collection Implementation Foundation - Branch Runtime Engineering Plan v1`

Owning Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`

Current Phase: `Branch Readiness Stage 2 setup complete - Workstream Entry pending`

Branch Runtime Engineering Plan: Accepted - this plan is present for the FAM-007 consent collection implementation foundation carrier.

Engineering Plan Status: Accepted for Stage 2 setup; implementation remains pending USER approval after Workstream Entry analysis.

Current Runtime Baseline: Released FAM-007 evidence includes provider readiness, activation, execution-readiness, provider path/consent readiness, setup/consent-flow readiness, setup contract readiness, setup implementation foundation, and disabled/status-only consent collection foundation through PR #193. Provider-visible data remains none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads/network blocked, memory disabled or deferred, voice/Core sync gated, desktop readiness display suppression preserved, and validation helper coverage in `dev/orin_ai_provider_state_validation.py`.

Branch Purpose: Move FAM-007 from disabled/status-only consent collection foundation toward an actual local consent capture/write-path implementation foundation while preserving provider setup completion, SDK/model execution, external calls, memory, voice/Core sync, shortcuts/installers, and functional AI as future USER decisions.

Planned Runtime Delta: The future Workstream may add local consent state transitions, local write-path validation, consent record schema, setup consent and execution consent capture separation, provenance/audit posture, provider-visible-data/no-secrets contract, local-only Core/Desktop/ORIN status proof, validator fixtures, fail-closed behavior, and future provider setup/execution handoff.

Implemented Runtime Delta: `None in Stage 2 - implementation remains pending USER approval.`

User-Facing Delta: The future Workstream may add truthful local consent capture/status posture if admitted. It must not imply provider setup completion, consent-to-execute approval, prompt acceptance, provider/model execution, provider-visible data, downloads, network calls, memory, voice/Core sync, or functional AI.

User-Facing Runtime Delta: The future Workstream may expose only concise, truthful consent capture/status proof. No long desktop AI-owned readiness display should reappear unless a later USER-approved interface plan changes that suppression posture.

Source-Truth Delta: Stage 2 records active FAM-007 branch authority, Product Definition Plan fields, Runtime Branch Engineering Contract fields, this Branch Runtime Engineering Plan, current release baseline, PR #193 as released predecessor evidence, compact FAM-007 pointer updates, worktree slot assignment, validation helper posture, FAM-006/Governance overlap posture, and future-gated approval boundaries.

State / Config / Schema Delta: Planned implementation may introduce local consent record schema, schema versioning, setup consent status, execution consent status, capture eligibility, write-path result, blocker/reason codes, provenance markers, audit timestamps, revocation/reset posture, provider profile/config references, provider-visible-data posture, and future handoff fields. It must not store secrets, provider credentials, prompt payloads for provider use, memory indexes, model artifacts, or network/API tokens.

Validator / Helper Delta: `dev/orin_ai_provider_state_validation.py` should extend existing FAM-007 consent foundation coverage for local consent capture/write-path fixtures, missing/blocked/future-gated consent states, fail-closed persistence/write-path behavior, setup/execution consent separation, provider-visible-data none, prompt execution disabled, downloads/network/memory/voice gates, and desktop readiness display suppression continuity.

Expected Changed Files / Surfaces: Expected Workstream implementation surfaces are `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`, this plan, compact current-state docs, `Docs/validation_helper_registry.md`, `desktop/ai_provider_state.py`, `desktop/desktop_renderer.py`, `desktop/core_visualization_renderer.py`, `nexus_visual/orin_core.*`, and `dev/orin_ai_provider_state_validation.py`; sibling worktrees and non-FAM-007 branches are excluded.

Workstream / Seam Map: Seam 1 consent capture state transition and local write path; Seam 2 consent record schema, storage boundary, and revocation model; Seam 3 setup consent / execution consent capture separation; Seam 4 provenance, audit, provider-visible data, and no-secrets contract; Seam 5 Core/Desktop/ORIN consent capture UI and status proof; Seam 6 validator fixtures, fail-closed behavior, and future provider setup handoff; Seam 7 functional-AI and v1.8.0 continuation criteria.

Per-Seam Implementation Checklist: For each seam, identify exact state/schema fields, write-path behavior, storage boundary, UI/status copy if any, validator fixtures, fail-closed behavior, approval boundary, affected file surface, and rollback expectation before editing implementation files.

Per-Seam Validation Checklist: Run diff checks, branch governance, release-health, governance efficiency, release body, source-owner marker, AI provider state validation, branch-readiness planning fixtures, runtime-fam007 validation suite, worktree rebaseline audit, compileall, and any new consent implementation fixtures introduced by the Workstream.

Per-Seam User-Facing Proof Checklist: If visible consent copy changes, prove the status-only or local-capture surface with static Core/Desktop/ORIN inspection and, if required by Workstream Entry, screenshot/live evidence. Confirm copy does not imply provider setup completion, provider execution, functional AI, downloads, network calls, memory, voice/Core sync, or v1.8.0 completion.

Future-Gated Items: Provider setup completion, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release, issue work, FAM-006 mutation, Governance mutation outside this branch, Compact-AI mutation, branch/worktree cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain gated.

Approval-Boundary Audit: Stage 2 may record source truth and admit a future Workstream only. Workstream implementation later may build the local consent capture/write-path foundation, but provider setup completion, provider communication, provider-visible prompts, model work, network egress, memory, voice/Core sync, shortcut/installer changes, release, PR creation, merge, cleanup, and cross-lane mutation require separate USER approval.

FAM / Shared-Surface Overlap Forecast: FAM-006 is a later PR/merge reconciliation risk only; Governance is standing intake context and must not be mutated here; Compact-AI is historical released/salvaged evidence and remains preserved; shared source-truth and ORIN/Core/Desktop surfaces require careful PR readiness reconciliation if other lanes advance before this branch merges.

Open Questions: USER must later decide whether Workstream implementation may include a user-operable local consent capture surface, whether revocation/reset belongs in this branch or the next branch, what storage boundary is acceptable, and when provider setup completion and execution proof become admissible.

USER Planning Decisions: USER approved Branch Readiness Stage 2 setup for this branch from `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8`. Workstream Entry, Workstream implementation, PR creation, merge, release, provider setup completion, SDK/model work, memory, voice/Core, shortcuts/installers, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0 execution remain pending.

Plan Revision History: v1 created during Branch Readiness Stage 2 from current `origin/main` after `v1.7.15-prebeta` and after PR #193 merged/released as prior FAM-007 consent collection foundation evidence.

Plan-To-Implementation Traceability Table: Planned consent capture state maps to provider-state implementation and fixtures; planned write path maps to local-only validation and fail-closed proof; planned provenance/audit posture maps to source-truth and validator proof; planned UI/status proof maps to Core/Desktop/ORIN status surfaces; planned setup/execution consent boundaries map to future-gated provider setup/execution handoff; planned continuation criteria map to H1, LV1, PR Readiness, and Release Readiness fold-down.

Hardening Comparison Checklist: H1 must compare actual consent capture/write-path implementation, schema, storage boundary, revocation/reset posture, setup/execution consent separation, provenance/audit, provider-visible-data/no-secrets posture, UI/status proof, validator fixtures, no-execution posture, source truth, branch plan, Runtime Branch Engineering Contract, and overlap posture against this plan.

Live Validation Proof Or Waiver Checklist: LV1 must classify the branch from repo truth, prove static/runtime validator state, prove any user-facing consent capture/status surface or record a source-truth-supported waiver, and keep provider-visible data none, prompt execution disabled, downloads/network/memory blocked, and voice/Core sync gated.

PR Readiness Fold-Down / Retention Checklist: PR Readiness must fold implementation scope into branch record/source truth, resolve selected-next or USER waiver truth, prove release-window/no-release-debt posture, preserve active branch authority cleanup, and keep live PR/watcher state out of merge-target current-state owners.

Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as local consent capture/write-path implementation foundation only, exclude provider setup completion, provider SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.

USER Planning Review: Pending Workstream Entry analysis.

PR Fold-Down Packet: Pending; live PR metadata belongs to PR Readiness Stage 2 only after USER approves PR creation.

Runtime Implementation Approval: Pending; this Stage 2 setup does not authorize implementation.

## Plan Status

Branch Readiness Stage 2 setup is complete for `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`. The plan is current for Workstream Entry analysis; runtime implementation begins only after later USER approval.

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `a42b7e50eb012722b140f3874dbf50826bd797c8`
- Latest public prerelease baseline: `v1.7.15-prebeta`
- Prior FAM-007 released consent evidence: PR #193 consent collection foundation, PR #192 setup implementation foundation, PR #190 setup contract readiness, and PR #179 setup/consent-flow readiness.

## Workstream Label

FAM-007 Local AI Provider Consent Collection Implementation Foundation.

## Admitted Seam Families

### 1. Consent Capture State Transition and Local Write Path

- Define local consent capture state transitions.
- Define local write-path behavior and fail-closed outcomes.
- Preserve provider setup completion and provider execution as future USER decisions.

### 2. Consent Record Schema, Storage Boundary, and Revocation Model

- Define local consent record schema, schema versioning, storage boundary, and revocation/reset posture.
- Preserve secrets, credentials, provider prompts, memory indexes, and model artifacts as excluded.

### 3. Setup Consent / Execution Consent Capture Separation

- Keep setup consent and execution consent distinct.
- Preserve execution consent and prompt/model execution as future-gated unless explicitly admitted.

### 4. Provenance, Audit, Provider-Visible Data, and No-Secrets Contract

- Define provenance, audit posture, provider-visible-data none, local-only state, and no-secrets posture.
- Preserve external calls and provider-visible prompt data as blocked.

### 5. Core/Desktop/ORIN Consent Capture UI and Status Proof

- Define truthful local consent status/capture proof and Core/Desktop/ORIN mapping if admitted.
- Preserve desktop readiness display suppression continuity.

### 6. Validator Fixtures, Fail-Closed Behavior, and Future Provider Setup Handoff

- Add validator fixtures for unavailable, blocked, invalid, captured-local-only, revoked/reset, future-gated, and fail-closed posture if admitted.
- Define handoff fields for future provider setup completion.

### 7. Functional-AI / v1.8.0 Continuation Criteria

- Define how local consent capture foundation feeds later functional-AI proof.
- Preserve v1.8.0-prebeta release execution as a later USER decision.

## Product Definition Plan

Product Vision: FAM-007 should become useful local AI through explicit user control over setup, consent, provider-visible data, and execution before any model is allowed to run.

User-Facing Goal: Provide the foundation for users to grant, see, and eventually revoke local consent state in a truthful way, while clearly showing that provider setup completion and functional AI remain future work.

Project-Wide Vision Alignment: Local consent capture is a safety and trust prerequisite for the Windows-first local AI roadmap and future capability-pack execution.

Branch-Specific Vision Alignment: This branch owns the local consent capture/write-path foundation and proof, not provider setup completion or model execution.

USER Vision Questions: USER has emphasized detailed, high-quality branches over broad sweeps; this plan keeps consent capture focused and defers later provider/model branches.

Codex Product Interpretation: Consent must be captured as first-class local state with provenance and audit posture, not inferred from setup state or provider availability.

Codex Implementation Recommendation: Implement the consent write path and validator-backed fail-closed rules before admitting provider setup completion or SDK/model execution.

Codex Additional Recommendations: Keep setup consent and execution consent separate; make revocation/reset posture explicit; keep provider-visible data none until a later provider execution branch.

USER/ChatGPT Review Checkpoint: Workstream Entry should decide the exact implementation boundary and whether any user-operable UI appears in this branch.

Full Feature Element Breakdown: local consent state, write path, schema, storage boundary, setup consent, execution consent, provenance, audit, revocation/reset, provider-visible-data posture, no-secrets posture, UI/status proof, validator fixtures, and future handoff.

Current Branch vs Future Package Boundaries: Current branch prepares and may later implement consent capture foundation; future package slices own provider setup completion, adapter/SDK integration, prompt routing, model execution, memory, voice/Core sync, packaging/install, and v1.8.0 release proof.

Affected Surfaces: branch record, branch plan, backlog, roadmap, worktree slots, validation helper registry, provider state, desktop/Core renderers, ORIN surfaces, and provider-state validator.

Data/Control Model: Consent capture remains local control state; it cannot send prompts, provider-visible data, secrets, credentials, model requests, memory records, or network payloads.

Expected User-Facing Outcomes: Users eventually see truthful local consent state without being told that provider setup is complete or AI is operational before those branches exist.

Acceptance Criteria: Workstream implementation, if later approved, must prove local consent capture/write-path behavior, fail-closed validation, no provider-visible data, disabled prompt/model execution, blocked downloads/network/memory, voice/Core gating, desktop readiness display suppression continuity, H1 Green, LV1 Green, and PR readiness fold-down.

## Next Legal Phase

`Workstream Entry analysis after USER approval`
