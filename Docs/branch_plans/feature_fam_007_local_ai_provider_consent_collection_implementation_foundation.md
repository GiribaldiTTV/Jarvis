# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Consent Collection Implementation Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-consent-collection-implementation-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Consent Collection Implementation Foundation - Branch Runtime Engineering Plan v1`

Owning Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`

Current Phase: `Historical / Retired after PR #201 merge - merged-unreleased evidence pending Release Readiness`

Branch Runtime Engineering Plan: Accepted - this plan is present for the FAM-007 consent collection implementation foundation carrier.

Engineering Plan Status: Historical / retired from active planning posture after PR #201 merged. Stage 2 setup, Workstream implementation, Hardening H1, Live Validation LV1, PR Readiness Stage 1, PR Readiness Stage 2 / PR creation, and merge are complete; release execution and future provider setup/execution work remain separate USER decisions.

Current Runtime Baseline: Released FAM-007 evidence includes provider readiness, activation, execution-readiness, provider path/consent readiness, setup/consent-flow readiness, setup contract readiness, setup implementation foundation, and disabled/status-only consent collection foundation through PR #193. Provider-visible data remains none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads/network blocked, memory disabled or deferred, voice/Core sync gated, desktop readiness display suppression preserved, and validation helper coverage in `dev/orin_ai_provider_state_validation.py`.

Branch Purpose: Move FAM-007 from disabled/status-only consent collection foundation toward an actual local consent capture/write-path implementation foundation while preserving provider setup completion, SDK/model execution, external calls, memory, voice/Core sync, shortcuts/installers, and functional AI as future USER decisions.

Planned Runtime Delta: The completed Workstream adds local consent state transitions, local write-path validation, consent record schema, setup consent and execution consent capture separation, provenance/audit posture, provider-visible-data/no-secrets contract, local-only Core/Desktop/ORIN status proof, validator fixtures, fail-closed behavior, and future provider setup/execution handoff.

Implemented Runtime Delta: `The completed Workstream adds local consent capture transition/write-path snapshot state, local record normalization, missing/invalid/no-selection/revoked/reset/captured-local-only fail-closed behavior, consent record schema/storage-boundary proof, durable-storage-deferred posture, local-only revocation/reset model, setup/execution consent separation, audit/no-secrets proof, hidden-telemetry UI/status proof, future provider setup handoff, functional-AI/v1.8.0 continuation criteria, and validator fixture proof.`

User-Facing Delta: The completed Workstream adds truthful local consent capture/status posture as hidden telemetry only. It does not imply provider setup completion, consent-to-execute approval, prompt acceptance, provider/model execution, provider-visible data, downloads, network calls, memory, voice/Core sync, or functional AI.

User-Facing Runtime Delta: The completed Workstream exposes only concise, truthful consent capture/status proof through hidden telemetry. No long desktop AI-owned readiness display should reappear unless a later USER-approved interface plan changes that suppression posture.

Source-Truth Delta: Historical fold-down records the FAM-007 branch authority as merged-unreleased PR #201 evidence, preserves this retired Branch Runtime Engineering Plan as a planning receipt, keeps current release baseline and PR #193 predecessor evidence intact, updates compact FAM-007 pointer surfaces, retires the worktree slot assignment from active PR posture, preserves validation helper posture, and keeps future-gated approval boundaries.

State / Config / Schema Delta: Completed implementation introduces local consent record schema, schema versioning, setup consent status, execution consent status, capture eligibility, write-path result, blocker/reason codes, provenance markers, audit posture, revocation/reset posture, provider profile/config references, provider-visible-data posture, and future handoff fields. It does not store secrets, provider credentials, prompt payloads for provider use, memory indexes, model artifacts, or network/API tokens.

Validator / Helper Delta: `dev/orin_ai_provider_state_validation.py` extends existing FAM-007 consent foundation coverage for local consent capture/write-path fixtures, missing/blocked/future-gated consent states, fail-closed persistence/write-path behavior, setup/execution consent separation, provider-visible-data none, prompt execution disabled, downloads/network/memory/voice gates, and desktop readiness display suppression continuity.

Expected Changed Files / Surfaces: Expected Workstream implementation surfaces are `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`, this plan, compact current-state docs, `Docs/validation_helper_registry.md`, `desktop/ai_provider_state.py`, `desktop/desktop_renderer.py`, `desktop/core_visualization_renderer.py`, `nexus_visual/orin_core.*`, and `dev/orin_ai_provider_state_validation.py`; sibling worktrees and non-FAM-007 branches are excluded.

Workstream / Seam Map: Seam 1 consent capture state transition and local write path; Seam 2 consent record schema, storage boundary, and revocation model; Seam 3 setup consent / execution consent capture separation; Seam 4 provenance, audit, provider-visible data, and no-secrets contract; Seam 5 Core/Desktop/ORIN consent capture UI and status proof; Seam 6 validator fixtures, fail-closed behavior, and future provider setup handoff; Seam 7 functional-AI and v1.8.0 continuation criteria.

Per-Seam Implementation Checklist: For each seam, identify exact state/schema fields, write-path behavior, storage boundary, UI/status copy if any, validator fixtures, fail-closed behavior, approval boundary, affected file surface, and rollback expectation before editing implementation files.

Per-Seam Validation Checklist: Run diff checks, branch governance, release-health, governance efficiency, release body, source-owner marker, AI provider state validation, branch-readiness planning fixtures, runtime-fam007 validation suite, worktree rebaseline audit, compileall, and any new consent implementation fixtures introduced by the Workstream.

Per-Seam User-Facing Proof Checklist: If visible consent copy changes, prove the status-only or local-capture surface with static Core/Desktop/ORIN inspection and, if required by Workstream Entry, screenshot/live evidence. Confirm copy does not imply provider setup completion, provider execution, functional AI, downloads, network calls, memory, voice/Core sync, or v1.8.0 completion.

Future-Gated Items: Provider setup completion, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, release execution, issue work, FAM-006 mutation, Governance mutation outside this branch, Compact-AI mutation, branch/worktree cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain gated. PR creation and merge are historical complete through PR #201.

Approval-Boundary Audit: The completed Workstream built only the local consent capture/write-path foundation. Provider setup completion, provider communication, provider-visible prompts, model work, network egress, memory, voice/Core sync, shortcut/installer changes, release, cleanup, and cross-lane mutation require separate USER approval. PR creation and merge are complete through PR #201 and no longer belong to active decision state.

FAM / Shared-Surface Overlap Forecast: FAM-006 is a later PR/merge reconciliation risk only; Governance is standing intake context and must not be mutated here; Compact-AI is historical released/salvaged evidence and remains preserved; shared source-truth and ORIN/Core/Desktop surfaces require careful PR readiness reconciliation if other lanes advance before this branch merges.

Open Questions: USER must later decide whether a future branch may add durable consent persistence beyond this local snapshot boundary, whether a later branch may include a user-operable local consent capture surface, and when provider setup completion and execution proof become admissible.

USER Planning Decisions: USER approved Branch Readiness Stage 2 setup, Workstream Entry analysis, corrected the prior seam-stop drift so the bounded Workstream continued to Workstream Green, approved Hardening H1, approved Live Validation LV1, approved PR Readiness Stage 1 analysis, approved PR Readiness Stage 2 / PR creation, and PR #201 merged. Release execution, provider setup completion, SDK/model work, memory, voice/Core, shortcuts/installers, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0 execution remain pending.

Plan Revision History: v1 created during Branch Readiness Stage 2 from current `origin/main` after `v1.7.15-prebeta` and after PR #193 merged/released as prior FAM-007 consent collection foundation evidence.

Plan-To-Implementation Traceability Table: Planned consent capture state maps to provider-state implementation and fixtures; planned write path maps to local-only validation and fail-closed proof; planned provenance/audit posture maps to source-truth and validator proof; planned UI/status proof maps to Core/Desktop/ORIN status surfaces; planned setup/execution consent boundaries map to future-gated provider setup/execution handoff; planned continuation criteria map to H1, LV1, PR Readiness, and Release Readiness fold-down.

Hardening Comparison Checklist: H1 must compare actual consent capture/write-path implementation, schema, storage boundary, revocation/reset posture, setup/execution consent separation, provenance/audit, provider-visible-data/no-secrets posture, UI/status proof, validator fixtures, no-execution posture, source truth, branch plan, Runtime Branch Engineering Contract, and overlap posture against this plan.

Live Validation Proof Or Waiver Checklist: LV1 must classify the branch from repo truth, prove static/runtime validator state, prove any user-facing consent capture/status surface or record a source-truth-supported waiver, and keep provider-visible data none, prompt execution disabled, downloads/network/memory blocked, and voice/Core sync gated.

PR Readiness Fold-Down / Retention Checklist: PR Readiness must fold implementation scope into branch record/source truth, resolve selected-next or USER waiver truth, prove release-window/no-release-debt posture, preserve active branch authority cleanup, and keep live PR/watcher state out of merge-target current-state owners.

Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as local consent capture/write-path implementation foundation only, exclude provider setup completion, provider SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.

USER Planning Review: Complete via Workstream Entry, Hardening H1, Live Validation LV1, and PR Readiness Stage 1; completed Workstream is ready for PR Readiness Stage 2 / PR creation after USER approval.

PR Fold-Down Packet: Complete after PR #201 merge - selected-next defer/waiver, historical pre-PR live-state, post-merge No Active Branch projection, Release Readiness Health Pass, Release Window Audit, branch-authority historical projection, PR Stage 2 execution, and merge proof are recorded in the branch record. Live PR metadata is historical receipt evidence only and must not be treated as active merged-main state.

Runtime Implementation Approval: Approved for the admitted bounded Workstream; provider setup completion, SDK/model execution, downloads/external calls, memory, voice/Core sync, shortcuts/installers, release, cleanup, and v1.8.0 execution remain pending USER decisions. PR creation and merge are historical complete through PR #201.

## Plan Status

Completed Workstream implementation, Hardening H1, Live Validation LV1, PR Readiness Stage 1, PR Readiness Stage 2, and PR #201 merge are recorded for `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`. The plan is retired from active planning posture and remains only as historical merged-unreleased evidence until release execution or a later USER-approved Branch Readiness selects a successor.

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-consent-collection-implementation-foundation`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `6681131c974d99945c494c0e4ff3c436f9347422` after Governance PR #200 rebaseline
- Latest public prerelease baseline: `v1.7.15-prebeta`
- Prior FAM-007 released consent evidence: PR #193 consent collection foundation, PR #192 setup implementation foundation, PR #190 setup contract readiness, and PR #179 setup/consent-flow readiness.

## Workstream Label

FAM-007 Local AI Provider Consent Collection Implementation Foundation.

## Admitted Seam Families

### 1. Consent Capture State Transition and Local Write Path

- Status: `Implemented and H1-reviewed.`
- Define local consent capture state transitions.
- Define local write-path behavior and fail-closed outcomes.
- Proof: `desktop/ai_provider_state.py` exposes local capture/write-path snapshot fields and `dev/orin_ai_provider_state_validation.py` validates missing, invalid, no-selection, revoked, reset, setup-only, setup+execution, and blocked-by-collection fixtures.
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

USER/ChatGPT Review Checkpoint: Workstream Entry review covered the admitted consent capture/write-path foundation. H1 verified the completed Workstream against the plan, and LV1 verified the disabled/status-only local consent telemetry posture before PR Readiness.

Full Feature Element Breakdown: local consent state, write path, schema, storage boundary, setup consent, execution consent, provenance, audit, revocation/reset, provider-visible-data posture, no-secrets posture, UI/status proof, validator fixtures, and future handoff.

Current Branch vs Future Package Boundaries: Current branch implements consent capture foundation; future package slices own provider setup completion, adapter/SDK integration, prompt routing, model execution, memory, voice/Core sync, packaging/install, and v1.8.0 release proof.

Affected Surfaces: branch record, branch plan, backlog, roadmap, worktree slots, validation helper registry, provider state, desktop/Core renderers, ORIN surfaces, and provider-state validator.

Data/Control Model: Consent capture remains local control state; it cannot send prompts, provider-visible data, secrets, credentials, model requests, memory records, or network payloads.

Expected User-Facing Outcomes: Users eventually see truthful local consent state without being told that provider setup is complete or AI is operational before those branches exist.

Acceptance Criteria: Workstream implementation must prove local consent capture/write-path behavior, fail-closed validation, no provider-visible data, disabled prompt/model execution, blocked downloads/network/memory, voice/Core gating, desktop readiness display suppression continuity, H1 Green, LV1 Green, and PR readiness fold-down.

## Element-to-Phase Proof Matrix

Matrix Status: Accepted - completed Workstream implementation maps to the PR #200-required active branch planning matrix.
USER Review Status: Accepted - Workstream Entry review was satisfied and completed Workstream evidence passed H1 comparison.
Open Element Questions: Deferred with waiver - exact user-operable consent UI and durable persistence beyond local snapshot remain future-branch questions, not Workstream blockers.
Element Coverage Owner: Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md.
Element Validation Ledger Owner: Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md.

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| :--- | --- | :---: | --- | --- | --- | --- | --- | --- | --- | ---: |
| FAM007-CONSENT-001 | Local consent capture state transition and write path | Touched | The Workstream adds local-only consent capture transition/write-path fields, local record normalization, fail-closed outcomes, and no provider communication. | Workstream proof runs branch governance validation, AI provider state validation, local consent fixtures, static source review, and diff checks against this branch plan. | Hardening H1 compares implemented transition behavior, failure handling, source truth, and validator evidence against the accepted plan and approval boundaries. | LV1 proves the local status or capture posture through static Core Desktop ORIN evidence or records a source-truth-supported waiver because no visible user path is admitted. | USER acceptance uses the Workstream Entry review bundle and later UTS or waiver to verify local-only consent posture before PR readiness. | Provider setup completion, provider execution, network calls, and functional AI remain future boundaries outside this branch unless USER later admits them. | Accepted complete. | Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md and Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md. |
| FAM007-CONSENT-002 | Consent record schema, storage boundary, and revocation model | Touched | The Workstream adds schema versioning, local snapshot storage boundary, durable-storage-deferred posture, local-only revocation/reset model, and local write constraints. | Workstream proof validates schema fields, missing or invalid records, local-null fallback, fail-closed storage behavior, and no secrets or provider payload persistence. | Hardening H1 reviews schema consistency, rollback behavior, storage boundary, no-secrets posture, source truth, and fixture coverage. | LV1 uses static validator evidence and visible status proof or waiver to show local consent record handling does not imply provider execution. | USER acceptance verifies no credential, secret, provider prompt, or provider payload storage is introduced. | Durable persistence beyond local snapshot, credentials, provider secrets, prompt payload persistence, memory indexes, model artifacts, and provider configuration completion remain future or excluded boundaries. | Accepted complete. | Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md and dev/orin_ai_provider_state_validation.py. |
| FAM007-CONSENT-003 | Setup consent and execution consent separation | Touched | The Workstream keeps setup consent and execution consent as separate local record flags and separate captured-state payload fields. | Workstream proof validates setup consent does not imply execution consent, execution consent does not enable prompt routing, and blocked states stay fail-closed. | Hardening H1 compares setup and execution consent separation against Product Definition Plan, Runtime Branch Engineering Contract, provider-state implementation, and fixtures. | LV1 proves setup and execution consent remain semantically distinct through static-validation waiver because no user-visible control exists. | USER acceptance verifies the copy and state model do not grant provider execution or functional AI by inference. | Actual consent collection UX, provider setup completion, execution approval, prompt acceptance, and model routing remain future-gated until separately approved. | Accepted complete. | Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md and desktop/ai_provider_state.py. |
| FAM007-CONSENT-004 | Provenance, audit, provider-visible data, and no-secrets contract | Touched | The Workstream adds local provenance, audit schema/status, provider-visible data none, sentToProvider false, no network egress, and no secret/provider-payload capture posture. | Workstream proof checks provenance fields, audit posture, provider-visible-data none, no-secrets posture, blocked network behavior, and validator fixture coverage. | Hardening H1 reviews audit semantics, provider-visible data, source truth, UI copy, network boundaries, and no hidden provider handoff. | LV1 proves provider-visible data remains none and execution remains disabled through static validation and status-only evidence. | USER acceptance confirms local audit posture without approving external calls, provider SDKs, downloads, memory behavior, or model execution. | External providers, network calls, provider-visible prompts, model execution, downloads, memory, learning, and personalization remain future boundaries. | Accepted complete. | Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md and dev/orin_ai_provider_state_validation.py. |
| FAM007-CONSENT-005 | Core Desktop ORIN consent status and UI proof | Touched | The Workstream maps consent capture proof to centralized provider-state payload fields and hidden telemetry only; no user-operable local consent surface is claimed. | Workstream proof reviews hidden telemetry, desktop readiness display suppression, no functional-AI implication, and source-owner marker coverage. | Hardening H1 compares UI/status payload against centralized state and confirms the long desktop AI-owned readiness display remains suppressed by default. | LV1 proves static Core Desktop ORIN posture or records a source-truth-supported disabled/status-only waiver. | USER acceptance uses the review bundle or UTS waiver to verify no provider setup or execution claim. | Broad UI redesign, shortcut or installer work, voice Core sync, and functional AI claims remain future boundaries outside this branch. | Accepted complete. | Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md and desktop/ai_provider_state.py. |
| FAM007-CONSENT-006 | Validator fixtures, fail-closed behavior, and future provider setup handoff | Touched | The Workstream extends provider-state validators and fixtures for captured, missing, invalid, no-selection, revoked, reset, blocked, and fail-closed local consent states plus future provider setup handoff. | Workstream proof runs AI provider state validation, branch-readiness planning fixtures, validation suite runtime-fam007, source-owner marker validation, diff checks, and compileall. | Hardening H1 verifies fixture breadth, negative cases, handoff fields, no-execution guarantees, and validator registry/source-truth alignment. | LV1 records static validator proof and any visible proof or waiver needed for disabled local-only consent behavior. | USER acceptance confirms validators prove local consent foundation while provider setup completion and execution remain excluded. | Provider setup execution, SDK integration, model execution, external calls, release execution, and v1.8.0 proof remain future boundaries. | Accepted complete. | Docs/validation_helper_registry.md and dev/orin_ai_provider_state_validation.py. |
| FAM007-CONSENT-007 | Functional AI and v1.8.0 continuation criteria | Future | The Workstream records how local consent capture feeds later functional-AI readiness while preserving no provider setup or model behavior in this branch. | Workstream proof records continuation criteria and validates all execution, download, network, memory, and voice Core gates remain closed. | Hardening H1 confirms the branch does not claim v1.8.0 completion, functional AI, provider execution, or release readiness beyond local consent foundation. | LV1 records disabled/status-only proof that functional AI remains pending future approved branches and release execution. | USER acceptance defers v1.8.0 and operational AI decisions until provider setup, adapter, prompt routing, model execution, and release proof exist. | Functional AI, v1.8.0-prebeta execution, provider SDK integration, model downloads, prompt routing, network egress, memory, and voice Core sync remain future release boundaries. | Deferred by USER pending later Branch Readiness and release decisions. | Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md and Docs/prebeta_roadmap.md. |

## Branch Change Intent Ledger

### Changed Surface: Docs/branch_plans/README.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-007 touched branch-plan lifecycle wording during Stage 2 setup and digest-clarity repair/revert history before Governance PR #200 merged.`
- Why This File Was Touched: `The FAM-007 lane needed Stage 2 closeout language that made the next plan-review gate visible after branch setup.`
- Owned Behavior / Fact Class: `FAM-007 owns only its branch-local Stage 2 and Workstream Entry planning posture; Governance PR #200 owns shared Branch Runtime Engineering Plan template, Element-to-Phase Proof Matrix, Workstream Entry review bundle, and whole-package gate rules.`
- Canonical Owner / Source Owner: `Docs/branch_plans/README.md with Governance PR #200 as incoming shared governance owner; FAM-007 branch-local details remain in this plan and its branch record.`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES - branch-plan template and branch-local plan routing surface.`
- Overlap Risk: `Governance-rule drift if FAM-007 keeps older Stage 2 digest wording over PR #200's broader Workstream Entry and matrix rules.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Prefer Governance PR #200 shared template/rule wording; preserve FAM-007-specific plan path, branch identity, and implementation-boundary facts only in FAM-007 branch-local files.`
- Rebaseline Handling: `Accept incoming shared governance-rule content and keep FAM-007 branch-local successor evidence in the active branch plan and branch record.`
- Validation Proof: `Run rebaseline audit validation, branch governance validation, release-readiness health validation, governance efficiency validation, branch-readiness planning fixture validation, and runtime-fam007 validation recommendations after reconciliation.`
- Fallback Evidence: `FAM-007 branch record and this Branch Runtime Engineering Plan record the branch-local authority; Governance PR #200 branch record records incoming shared governance intent. Not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this overlap-resolution policy: Governance PR #200 owns shared governance-rule wording while FAM-007 preserves branch-local facts.`
- Fold-Down Target: `PR Readiness fold-down for this FAM-007 branch after Workstream/H1/LV1; shared governance wording remains owned by merged main governance source truth.`

### Changed Surface: Docs/branch_records/index.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-007 registered its active branch authority and earlier plan-review gate clarification before Governance PR #200 changed branch-record index governance.`
- Why This File Was Touched: `The FAM-007 Stage 2 setup needed the active branch authority record indexed for the current runtime carrier.`
- Owned Behavior / Fact Class: `FAM-007 owns the active branch record pointer for feature/fam-007-local-ai-provider-consent-collection-implementation-foundation; Governance PR #200 owns shared branch-class, digest, Workstream Entry, and governance repair routing rules.`
- Canonical Owner / Source Owner: `Docs/branch_records/index.md for branch authority routing; Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md for FAM-007 branch-local authority.`
- Resolution Owner: `USER Decision`
- Shared Surface: `YES - branch authority index plus shared governance rules.`
- Overlap Risk: `Active branch pointer could be dropped or Governance PR #200's source-truth routing could be overwritten by stale FAM-007 wording.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve Governance PR #200 shared governance-rule/index changes and preserve the FAM-007 active branch authority pointer if current source truth still names this branch as active.`
- Rebaseline Handling: `Merge both: incoming governance rules remain authoritative; FAM-007 active branch record remains listed until this branch reaches PR fold-down or another USER-approved state change.`
- Validation Proof: `Run rebaseline audit validation, branch governance validation, release-readiness health validation, governance efficiency validation, branch-readiness planning fixture validation, and source-owner marker validation after reconciliation.`
- Fallback Evidence: `FAM-007 branch record, worktree slot receipt, and live git identity prove this branch remains active. Not a compatibility bypass.`
- USER Decision / Waiver: `USER approved preserving FAM-007 branch-local authority while treating Governance PR #200 as authoritative for shared governance rules.`
- Fold-Down Target: `FAM-007 PR Readiness will retire or fold down active branch authority; governance index rules remain in shared source truth.`

### Changed Surface: Docs/phase_governance.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-007 touched phase digest wording during a branch-local clarity repair/revert path before Governance PR #200 merged a broader governance-owned fix.`
- Why This File Was Touched: `The FAM-007 lane exposed a digest clarity gap around USER plan review gates and implementation blockers.`
- Owned Behavior / Fact Class: `Governance PR #200 owns phase digest non-compaction, Workstream Entry review bundle, Element-to-Phase Proof Matrix, whole-package Workstream Entry gate, and vision update matrix rules; FAM-007 owns only the branch-local fact that implementation remains blocked until Workstream Entry/implementation approval.`
- Canonical Owner / Source Owner: `Docs/phase_governance.md with Governance PR #200 as authoritative shared-rule owner.`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES - repo-wide phase governance.`
- Overlap Risk: `High if branch-local wording overwrites the governance-owned phase rules or weakens the broader PR #200 gate set.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Prefer Governance PR #200 for repo-wide governance text; retain FAM-007 implementation blocker only in branch-local record/plan if needed.`
- Rebaseline Handling: `Accept incoming Governance PR #200 phase governance; do not reintroduce FAM-007-only governance wording into shared phase rules.`
- Validation Proof: `Run branch governance validation, release-readiness health validation, governance efficiency validation, branch-readiness planning fixture validation, source-owner marker validation, and compileall after reconciliation.`
- Fallback Evidence: `Governance PR #200 branch record names phase-digest and Workstream Entry hardening as its purpose. Not a compatibility bypass.`
- USER Decision / Waiver: `USER approved Governance PR #200 as authoritative for shared governance-rule content.`
- Fold-Down Target: `Merged main phase governance; FAM-007 branch record keeps only branch-local approval boundaries.`

### Changed Surface: Docs/validation_helper_registry.md

- Surface Class: `governance/source-truth`
- Change Intent: `FAM-007 added planned provider-state validator coverage for the consent collection implementation foundation branch; Governance PR #200 expanded shared validator/helper responsibilities.`
- Why This File Was Touched: `Stage 2 setup needed the FAM-007 consent collection implementation foundation validator row before Workstream implementation could be planned safely.`
- Owned Behavior / Fact Class: `FAM-007 owns its provider/consent validator registration row; Governance PR #200 owns shared helper registry wording for digest non-compaction, Workstream Entry whole-package gate, Element-to-Phase matrix, review bundles, fixtures, and governance validator ownership.`
- Canonical Owner / Source Owner: `Docs/validation_helper_registry.md with mixed ownership: FAM-007 provider-state row plus Governance PR #200 shared validator/helper registry rules.`
- Resolution Owner: `USER Decision`
- Shared Surface: `YES - repo-wide helper registry with branch-specific validator row.`
- Overlap Risk: `FAM-007 validator row could be lost, or PR #200 helper/fixture ownership could be overwritten by stale branch wording.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve both Governance PR #200 shared helper registry updates and the FAM-007 consent collection implementation foundation validator row.`
- Rebaseline Handling: `Conflict-aware merge: incoming governance helper ownership stays authoritative; FAM-007 row remains as branch-local validator fact.`
- Validation Proof: `Run branch governance validation, release-readiness health validation, governance efficiency validation, branch-readiness planning fixture validation, source-owner marker validation, FAM-007 provider-state validation, and compileall after reconciliation.`
- Fallback Evidence: `FAM-007 branch record and Branch Runtime Engineering Plan require provider-state validator coverage for the consent collection implementation foundation. Not a compatibility bypass.`
- USER Decision / Waiver: `USER approved preserving FAM-007 provider/consent validation facts while accepting Governance PR #200 shared validator changes.`
- Fold-Down Target: `Validation helper registry remains shared source truth; branch-specific row folds down during PR Readiness if this branch changes validator responsibilities.`

### Changed Surface: Docs/governance_docs_full_inventory_reform_audit.md

- Surface Class: `documentation/reference`
- Change Intent: `FAM-007 carried regenerated/current inventory reference changes from Stage 2 setup context before Governance PR #200 regenerated or updated the docs inventory reform audit.`
- Why This File Was Touched: `The file is a generated/reference docs inventory surface affected by source-truth reform and branch setup changes.`
- Owned Behavior / Fact Class: `Governance tooling owns the generated inventory/reference content; FAM-007 owns only branch-local source-truth files that may appear in that inventory.`
- Canonical Owner / Source Owner: `dev/orin_docs_inventory_reform_audit.py and Governance PR #200 generated inventory source truth.`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES - generated/reference inventory surface.`
- Overlap Risk: `Low-to-medium generated-doc churn; accepting stale branch output could hide PR #200's current docs inventory review.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `None`
- Conflict Resolution Rule: `Prefer Governance PR #200 generated/reference inventory output; preserve FAM-007 branch-local files themselves rather than stale inventory text.`
- Rebaseline Handling: `Accept incoming generated/reference inventory or regenerate intentionally only if current repo tooling requires it after merge.`
- Validation Proof: `Run governance efficiency validation, branch governance validation, branch-readiness planning fixture validation, and docs inventory tooling only if current source truth requires regeneration.`
- Fallback Evidence: `Incoming Governance PR #200 includes docs inventory reform audit changes and helper registry ownership for the audit generator. Not a compatibility bypass.`
- USER Decision / Waiver: `USER approved treating generated inventory/review-index overlap according to current repo tooling and Governance PR #200 authority.`
- Fold-Down Target: `Generated/reference governance inventory on merged main.`

### Changed Surface: Docs/governance_docs_reform_user_review_index.md

- Surface Class: `documentation/reference`
- Change Intent: `FAM-007 carried reference review-index updates from Stage 2 setup context before Governance PR #200 updated the docs reform USER review index.`
- Why This File Was Touched: `The file is a generated/reference USER review index for source-truth reform and was affected by branch setup and governance reform context.`
- Owned Behavior / Fact Class: `Governance tooling owns generated review-index content; FAM-007 owns only branch-local branch record, branch plan, and validator facts that may be referenced by the index.`
- Canonical Owner / Source Owner: `dev/orin_docs_inventory_reform_audit.py and Governance PR #200 generated review-index source truth.`
- Resolution Owner: `Incoming/Folded Owner`
- Shared Surface: `YES - generated/reference review-index surface.`
- Overlap Risk: `Low generated/reference drift if stale FAM-007 text overwrites PR #200's current review-index output.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `None`
- Conflict Resolution Rule: `Prefer Governance PR #200 generated/reference review-index output; preserve FAM-007 branch-local files and facts outside this generated surface.`
- Rebaseline Handling: `Accept incoming generated/reference index or regenerate intentionally only if current repo tooling requires it after merge.`
- Validation Proof: `Run governance efficiency validation, branch governance validation, branch-readiness planning fixture validation, and docs inventory tooling only if current source truth requires regeneration.`
- Fallback Evidence: `Incoming Governance PR #200 includes docs reform review-index changes and generator ownership. Not a compatibility bypass.`
- USER Decision / Waiver: `USER approved treating generated inventory/review-index overlap according to current repo tooling and Governance PR #200 authority.`
- Fold-Down Target: `Generated/reference governance review index on merged main.`

## Hardening H1 Result

Hardening H1 Result: `Green - H1 compared completed local consent capture/write-path implementation, consent record schema/storage boundary, durable-storage-deferred posture, local-only revocation/reset model, setup/execution consent separation, provenance/audit/no-secrets posture, provider-visible-data/no-execution posture, hidden telemetry UI proof, desktop readiness display suppression continuity, validator fixtures, source truth, and approval boundaries against this Branch Runtime Engineering Plan, the Product Definition Plan, and the Runtime Branch Engineering Contract.`

H1 Repair Scope: `Source-truth fold-down only - this plan now records H1 Green and routes the next phase to Live Validation LV1.`

Next Handoff: `Live Validation LV1 validated static Core/Desktop/ORIN source truth plus FAM-007 provider-state validator proof, preserved desktop readiness display suppression continuity, confirmed local-only/provider-visible-data none posture, and recorded the User Test Summary/static waiver posture because no user-operated consent path is admitted.`

## Live Validation LV1 Result

Live Validation LV1 Result: `Green - LV1 validated the completed and hardened local consent capture/write-path implementation foundation as disabled/status-only local consent telemetry through static Core/Desktop/ORIN source truth plus FAM-007 provider-state validator proof.`

User Test Summary Results: `WAIVED - no user-operated consent capture path is admitted; static validator proof is the approved proof path.`

Next Handoff: `PR Readiness Stage 1 analyzed PR eligibility, selected-next/defer truth, pre-PR live state, release-window posture, active branch authority, historical refs, overlap posture, validation posture, and Stage 2 PR creation readiness.`

## PR Readiness Stage 1 Result

PR Readiness Stage 1 Result: `Historical complete - Stage 1 reached Ready For Stage 2, USER later approved PR Readiness Stage 2 / PR creation, and PR #201 merged. Workstream Green, H1 Green, LV1 Green, UTS waiver, desktop readiness display suppression continuity, selected-next defer/waiver truth, historical pre-PR live-state, post-merge No Active Branch projection, release-window posture, approval boundaries, Release Readiness Health Pass, and validation proof are retained as branch receipt evidence.`

PR Readiness Stage 1 Repairs Applied: `Historical - Stage 1 source-truth fold-down updated this plan, the branch record, backlog/roadmap current-state pointers, and the worktree slot receipt before PR creation. PR #201 was later created and merged; no provider setup completion, SDK/model execution, runtime behavior beyond the admitted foundation, production UI behavior, release, cleanup, FAM-006, Governance, or Compact-AI mutation was performed.`

Selected-Next Defer User Waiver: `Granted - USER approved selected-next defer/waiver truth for this PR-readiness pass.`

Pre-PR Live State: `Historical pre-PR snapshot - no live PR existed before Stage 2; USER later approved PR Readiness Stage 2, PR #201 was created, and PR #201 merged. This field is not active live PR state.`

Post-Merge No Active Branch Projection: `After merge, merged-main source truth should project No Active Branch until a later USER-approved Branch Readiness decision selects a successor lane.`

PR Readiness Stage 2 Result: `Complete - PR #201 was created and merged into main. Live PR state, watcher proof, and merge metadata are historical receipt evidence only.`

## Next Legal Phase

`Release Readiness`

Next Legal Phase Detail: `Release Readiness Stage 1 may validate the aggregated release window after Governance repairs stale post-merge source truth; release execution remains separately USER-gated.`
