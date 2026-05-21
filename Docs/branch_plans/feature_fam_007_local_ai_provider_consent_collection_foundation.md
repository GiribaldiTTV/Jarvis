# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Consent Collection Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-consent-collection-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Consent Collection Foundation - Branch Runtime Engineering Plan v1`

Owning Branch: `feature/fam-007-local-ai-provider-consent-collection-foundation`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_foundation.md`

Current Phase: `Workstream implementation complete - FAM-007 consent collection foundation`

Branch Runtime Engineering Plan: Accepted - this plan is present for the FAM-007 consent collection foundation carrier.

Engineering Plan Status: Accepted - Workstream Green after bounded consent collection foundation implementation; Hardening H1 remains pending USER approval.

Current Runtime Baseline: Released FAM-007 state includes setup/consent-flow readiness, setup contract readiness, and setup implementation foundation evidence through PR #192 and `v1.7.12-prebeta`, with provider-visible data none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads and network blocked, memory disabled, voice/Core sync gated, desktop readiness display suppression preserved, and provider-state validation coverage in `dev/orin_ai_provider_state_validation.py`.

Branch Purpose: Move FAM-007 from local setup implementation foundation toward a consent collection foundation that defines consent-state contracts, capture readiness, provenance/audit posture, data visibility boundaries, validator fixtures, and future setup/execution handoff without enabling actual consent capture or provider execution.

Planned Runtime Delta: The Workstream may add consent foundation state/schema, setup consent and execution consent readiness, consent eligibility/blocker/reason/provenance fields, audit/data visibility posture, future consent handoff markers, Core/Desktop/ORIN status proof, validator fixtures, and source-truth fold-down while preserving actual capture, provider setup, SDK/model execution, downloads, network, memory, and voice/Core sync as future USER decisions.

Implemented Runtime Delta: `Complete - local-only consent collection foundation state/schema, eligibility, blockers, reason codes, provenance, approval status, capture-surface posture, audit/data visibility proof, persistence/validation gates, future consent capture handoff, Core/Desktop/ORIN status proof, and provider-state validator fixtures are implemented without actual consent capture or provider execution.`

User-Facing Delta: The future Workstream may add truthful disabled/status-only consent readiness copy if admitted. This branch plan does not authorize actual consent capture, provider setup, prompt acceptance, provider/model execution, provider-visible data, downloads, network calls, memory, voice/Core sync, or functional-AI claims.

User-Facing Runtime Delta: The future Workstream may show truthful disabled/status-only consent readiness if admitted. It must not imply that consent has been captured, provider setup is complete, prompts can be sent, models can run, provider-visible data exists, memory is active, or functional AI is operational.

Source-Truth Delta: Stage 2 records `v1.7.12-prebeta` closure, PR #192 as released setup implementation foundation evidence, active FAM-007 branch authority, Product Definition Plan fields, Runtime Branch Engineering Contract fields, this Branch Runtime Engineering Plan, bounded seam admission, FAM-006/Governance/Compact-AI overlap posture, and future-gated approval boundaries.

State / Config / Schema Delta: Planned implementation may introduce consent foundation schema, setup consent readiness, execution consent readiness, capture eligibility, blockers, reason codes, provenance markers, audit status, provider-visible-data posture, local-only handoff fields, and schema versioning, but it must not store consent grants, credentials, secrets, prompts for provider use, memory indexes, or model artifacts.

Validator / Helper Delta: `dev/orin_ai_provider_state_validation.py` should be extended for consent foundation state/schema, setup consent readiness, execution consent readiness, missing/blocked/future-gated consent fixtures, provenance/audit posture, provider-visible-data none, prompt execution disabled, downloads/network/memory/voice gates, and desktop readiness display suppression continuity.

Expected Changed Files / Surfaces: Expected surfaces are `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_foundation.md`, this plan, `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/worktree_slots.md`, `Docs/validation_helper_registry.md`, `desktop/ai_provider_state.py`, `desktop/desktop_renderer.py`, `desktop/core_visualization_renderer.py`, `nexus_visual/orin_core.*`, and `dev/orin_ai_provider_state_validation.py`; sibling worktrees and non-FAM-007 branches are excluded.

Workstream / Seam Map: Seam 1 consent collection state and schema; Seam 2 consent capture preconditions and eligibility; Seam 3 consent provenance, audit, and data visibility contract; Seam 4 consent UI/status proof and future handoff planning; Seam 5 provider setup and execution consent boundary alignment; Seam 6 functional-AI and v1.8.0 continuation criteria.

Per-Seam Implementation Checklist: For each seam, identify source state, schema fields, copy/status posture if any, validator fixtures, fail-closed behavior, approval boundary, affected file surface, and rollback expectation before editing implementation files.

Per-Seam Validation Checklist: Run diff checks, branch governance, release-health, source-owner marker, AI provider state validation, planning fixtures, runtime-fam007 validation suite, worktree rebaseline audit, compileall, monitoring HUD validators, and any new consent foundation fixtures introduced by the Workstream.

Per-Seam User-Facing Proof Checklist: If visible consent copy changes, prove the status-only user-facing surface with static Core/Desktop/ORIN inspection or screenshot evidence, confirm no long readiness box returns, and confirm copy does not imply consent capture, provider setup, provider execution, functional AI, downloads, network calls, memory, or v1.8.0 completion.

Future-Gated Items: Actual consent collection implementation, provider setup implementation, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release, issue work, FAM-006 mutation, Governance mutation outside this branch, Compact-AI mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain gated.

Approval-Boundary Audit: Stage 2 may record source truth and admit a future Workstream only; Workstream implementation later may build consent foundation contracts and validation scaffolding, but actual consent capture, provider communication, provider-visible prompts, model work, network egress, memory, voice/Core sync, shortcut/installer changes, release, PR creation, merge, cleanup, and cross-lane mutation require separate USER approval.

FAM / Shared-Surface Overlap Forecast: FAM-006 is a later PR/merge reconciliation risk only; Governance is standing intake context and must not be mutated here; Compact-AI has protected unique commits and remains preserved; shared source-truth and ORIN/Core/Desktop surfaces require careful PR readiness reconciliation if other lanes advance before this branch merges.

Open Questions: USER must later decide whether actual consent collection should be enabled in a separate branch, whether visible consent UI should be expanded, and when provider setup/execution proof is strong enough for a v1.8.0-prebeta release decision.

USER Planning Decisions: USER approved Branch Readiness Stage 1, selected consent collection foundation as the next FAM-007 successor, approved Stage 2 setup in the FAM-007 worktree, approved Workstream Entry, and approved bounded Workstream implementation. Actual consent capture, provider setup, SDK/model work, memory, voice/Core, shortcuts/installers, cleanup, AI Product Contract import, and v1.8.0 execution remain pending.

Plan Revision History: v1 created during Branch Readiness Stage 2 from `origin/main` at `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`, after `v1.7.12-prebeta` publication and release-canon closure.

Plan-To-Implementation Traceability Table: Planned consent state maps to provider-state implementation and fixtures; planned provenance/audit posture maps to local-only validation proof; planned UI/status proof maps to Core/Desktop/ORIN status surfaces; planned setup/execution consent boundaries map to future-gated handoff; planned continuation criteria map to H1, LV1, PR Readiness, and Release Readiness fold-down.

Hardening Comparison Checklist: Required after Workstream implementation; H1 must compare actual consent state, schema, eligibility, provenance/audit, UI/status proof, setup/execution boundaries, no-execution posture, source truth, branch plan, Runtime Branch Engineering Contract, and overlap posture against this plan.

Live Validation Proof Or Waiver Checklist: LV1 must classify the branch from repo truth, prove static/runtime validator state when consent remains disabled/status-only, capture user-facing proof or waiver for any visible consent surface, and keep provider-visible data none, prompt execution disabled, downloads/network/memory blocked, and voice/Core sync gated.

PR Readiness Fold-Down / Retention Checklist: PR Readiness must fold consent foundation scope into branch record/source truth, resolve selected-next or USER waiver truth, prove release-window/no-release-debt posture, preserve active branch authority cleanup, and keep live PR/watcher state out of merge-target current-state owners.

Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as consent collection foundation only, exclude actual consent capture, provider setup, provider SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.

USER Planning Review: Accepted for Branch Readiness Stage 2 setup.

PR Fold-Down Packet: Pending - PR Readiness must decide selected-next/defer truth, pre-PR live-state, post-merge projection, release-window posture, branch-authority historical projection, and Stage 2 approval boundary.

Runtime Implementation Approval: Pending - Workstream implementation begins only after later USER approval.

## Plan Status

Workstream implementation is complete for `feature/fam-007-local-ai-provider-consent-collection-foundation`. The plan is current for Hardening H1 review; actual consent capture and provider setup begin only after later USER approval.

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-consent-collection-foundation`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`
- Latest public prerelease baseline: `v1.7.12-prebeta`
- Prior FAM-007 released setup evidence: PR #192 setup implementation foundation, PR #190 setup contract readiness, and PR #179 setup/consent-flow readiness.

## Workstream Label

FAM-007 Local AI Provider Consent Collection Foundation.

## Admitted Seam Families

### 1. Consent Collection State and Schema

- Define consent collection foundation state and schema versioning.
- Preserve actual consent capture as a future USER decision.

### 2. Consent Capture Preconditions and Eligibility

- Define when consent capture is unavailable, blocked, future-gated, or ready for a later implementation branch.
- Preserve provider setup and execution as future USER decisions.

### 3. Consent Provenance, Audit, and Data Visibility Contract

- Define provenance, audit posture, data visibility classes, local-only state, and no-secrets posture.
- Preserve provider-visible prompt data as none.

### 4. Consent UI/Status Proof and Future Handoff Planning

- Define truthful status-only copy and Core/Desktop/ORIN proof expectations.
- Preserve desktop readiness display suppression continuity.

### 5. Provider Setup and Execution Consent Boundary Alignment

- Keep setup consent and execution consent distinct, future-gated, and not collected by this branch.
- Preserve provider setup, SDK/model execution, downloads, network, memory, and voice/Core sync as blocked.

### 6. Functional-AI / v1.8.0 Continuation Criteria

- Define how consent foundation feeds later functional-AI proof.
- Preserve v1.8.0-prebeta release execution as a later USER decision.

## Product Definition Plan

Product Vision: FAM-007 should become useful local AI through cautious, inspectable setup steps that keep users in control of consent, data visibility, provider choice, and local-only safety before any provider/model runtime is enabled.

User-Facing Goal: Prepare a consent foundation that can later support explicit consent capture while truthfully reporting that consent is not yet collected and functional AI is not yet operational.

Project-Wide Vision Alignment: Consent foundation supports the broader modular, local-first AI direction by establishing trust and privacy prerequisites before SDK/model execution.

Branch-Specific Vision Alignment: This branch owns consent foundation planning and future implementation scaffolding only; it does not own provider setup completion, execution, memory, voice/Core sync, shortcut/installer work, or v1.8.0 release execution.

USER Vision Questions: USER prefers detailed branches with higher quality; Hardening H1 should verify that visible consent status proof stays truthful without enabling capture.

Codex Product Interpretation: Consent collection must be built as an explicit, auditable prerequisite rather than inferred from setup state or provider availability.

Codex Implementation Recommendation: Implement consent foundation state/schema, provenance/audit posture, data visibility rules, UI/status proof, validator fixtures, and future handoff criteria before admitting actual capture.

Codex Additional Recommendations: Keep setup consent and execution consent separate; avoid storing secrets or prompt data; keep copy local-only and future-gated.

USER/ChatGPT Review Checkpoint: Hardening H1 should review this implementation before LV1 begins.

Full Feature Element Breakdown: consent foundation state, setup consent posture, execution consent posture, capture eligibility, blockers/reasons, provenance, audit posture, provider-visible data posture, local-only handoff, status copy, validator fixtures, release fold-down.

Current Branch vs Future Package Boundaries: Current branch establishes consent foundation contracts, status proof, fixtures, and future implementation scaffolding; future packages own actual capture, provider setup completion, SDK/model execution, memory, voice/Core sync, shortcuts/installers, and functional-AI proof.

Affected Surfaces: branch record, branch plan, backlog, roadmap, worktree slots, validation helper registry, provider state, desktop/Core renderers, ORIN surfaces, and provider-state validator.

Data/Control Model: Consent readiness remains local and status-only until later approval; no prompt data, provider-visible data, model request, network call, memory record, credential, or secret leaves the local process.

Expected User-Facing Outcomes: Users eventually see truthful consent readiness/status without being told that consent is collected or AI is operational before those branches exist.

Acceptance Criteria: Workstream implementation must prove consent foundation state, UI/status copy integrity, no provider-visible data, disabled prompt/model execution, blocked downloads/network/memory, voice/Core gating, and static validator coverage.

## Next Legal Phase

`Hardening H1 after USER approval`
