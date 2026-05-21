# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Setup Contract Readiness

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-setup-contract-readiness; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Setup Contract Readiness - Branch Runtime Engineering Plan v1`

Owning Branch: `feature/fam-007-local-ai-provider-setup-contract-readiness`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md`

Current Phase: `PR Readiness Stage 1 Ready For Stage 2 - PR creation pending USER approval`

Branch Runtime Engineering Plan: Accepted - this plan is present for the FAM-007 setup contract readiness carrier.

Engineering Plan Status: Accepted - implemented through Workstream Green, inspected through Hardening H1 Green, validated through Live Validation LV1 Green, and PR Readiness Stage 1 fold-down is Green; PR Readiness Stage 2 / PR creation is pending USER approval.

Current Runtime Baseline: PR #179 released FAM-007 setup/consent-flow readiness with provider setup future-gated, consent collection pending, provider-visible data `none`, `sentToProvider=false`, `canAcceptPrompts=false`, prompt/model execution disabled, downloads blocked, network egress blocked, memory/indexing disabled, and voice/Core sync gated.

Branch Purpose: define setup contract readiness as the next FAM-007 layer after setup/consent-flow readiness, preserving a status-only/local posture before any real provider setup, consent collection, SDK integration, or model execution.

Planned Runtime Delta: setup contract state/schema, provider profile/config requirements, setup preconditions, consent prerequisites, setup handoff criteria, approval gate posture, validator fixture expectations, and short status-proof mapping are implemented without activating setup.

User-Facing Delta: Core/Desktop/ORIN setup contract status proof is status-only and validator-visible; the long desktop AI-owned readiness display remains hidden/suppressed by default and copy does not imply provider setup, consent collection, prompt acceptance, or functional AI.

Source-Truth Delta: records fresh FAM-007 branch authority, closed `v1.7.10-prebeta` release-canon drift, admitted this branch plan, folded down Workstream Green, H1 Green, LV1 Green, selected-next defer/waiver, pre-PR live-state, post-merge No Active Branch projection, Release Readiness Health Pass, and Release Window Audit posture, and preserved FAM-006/Governance/Compact-AI overlap as later reconciliation context only.

State / Config / Schema Delta: setup contract readiness fields, setup precondition fields, setup approval fields, provider profile/config requirement fields, consent prerequisite fields, provenance/reason/schema markers, and future handoff markers are implemented as local-only/static contract state.

Validator / Helper Delta: `dev/orin_ai_provider_state_validation.py` now validates setup contract readiness state/schema, profile/config requirements, setup/execution consent prerequisites, approval gates, handoff posture, desktop readiness display suppression continuity, and provider/runtime no-execution fixtures; the validation suite continues to include the FAM-007 provider validator.

Expected Changed Files / Surfaces: branch record, branch plan, backlog, roadmap, worktree slot receipt, validation registry, provider state, Core/Desktop renderers, ORIN visual surfaces, and FAM-007 provider validator.

Workstream / Seam Map: Seam 1 setup contract state/schema; Seam 2 provider profile/config requirements; Seam 3 setup preconditions and consent prerequisites; Seam 4 setup handoff and approval gates; Seam 5 Core/Desktop/ORIN setup contract status proof; Seam 6 functional-AI and v1.8.0 continuation criteria.

Per-Seam Implementation Checklist: for each seam, identify source fields, source-truth records, runtime or UI surfaces if any, validator fixture needs, approval-boundary proof, and future-gated items before editing implementation files.

Per-Seam Validation Checklist: run diff checks, branch governance, release-health, source-owner marker, AI provider state, planning fixture, validation suite, rebaseline audit, compileall, and any new setup contract validator fixtures introduced by the Workstream.

Per-Seam User-Facing Proof Checklist: each seam must include user-visible proof or a waiver; if Core/Desktop/ORIN copy changes, capture visible status-only proof, screenshot/static validator evidence, and confirmation that copy does not imply provider setup, consent collection, provider execution, functional AI, or `v1.8.0-prebeta` release readiness.

Future-Gated Items: provider setup implementation, consent collection, provider SDK integration, provider/model execution, model downloads, external calls, memory/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release, FAM-006 mutation, Governance mutation outside this branch, Compact-AI mutation, and `v1.8.0-prebeta` remain gated, blocked, and pending later USER approval.

Approval-Boundary Audit: Stage 2 and the planned Workstream may define contracts, state, gates, UI proof, and validators only; real setup execution, consent collection, provider communication, provider-visible data, prompt routing, model workload execution, downloads, network egress, memory, voice/Core sync, shortcut/installer work, release, PR creation, merge, issue work, cleanup, and cross-lane mutation require later USER approval.

FAM / Shared-Surface Overlap Forecast: FAM-006 dirty shared docs are later PR/merge reconciliation risk only; Governance is standing intake context only; Compact-AI has protected unique commits and must not be mutated by this branch; FAM-007 owns only this localized branch/worktree path.

Open Questions: USER must decide whether to approve PR Readiness Stage 2 / PR creation; future questions include when real provider setup, consent collection, provider SDK/model work, or functional-AI proof should be admitted.

USER Planning Decisions: USER approved Branch Readiness Stage 2, Workstream Entry, bounded Workstream implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair for this branch; USER decisions remain pending for PR Readiness Stage 2 / PR creation, merge, Release Readiness, release execution, cleanup, provider setup, consent collection, SDK/model execution, and future functional-AI work.

Plan Revision History: v4 - PR Readiness Stage 1 recorded selected-next defer/waiver truth, pre-PR live-state, post-merge No Active Branch projection, Release Readiness Health Pass, Release Window Audit, and Stage 2 / PR creation as the next USER-gated phase; v3 - Live Validation LV1 recorded disabled/status-only classification, static validator/source-truth proof, User Test Summary waiver, desktop readiness display suppression continuity, and PR Readiness Stage 1 as the next legal phase; v2 - Hardening H1 folded down H1 Green posture, validator proof, desktop readiness display suppression continuity, approval-boundary integrity, and LV1-next handoff after Workstream completion; v1 created during Branch Readiness Stage 2 from `origin/main` at `b67e59df0481091bfbeb739c4b5e1954552bb421`, carrying `v1.7.10-prebeta` canon closure and PR #179 FAM-007 released evidence.

Plan-To-Implementation Traceability Table: planned setup contract state maps to provider-state implementation and fixtures; planned profile/config requirements map to metadata/config envelope proof; planned consent prerequisites map to setup/execution consent posture; planned UI proof maps to Core/Desktop/ORIN copy if touched; planned continuation criteria map to H1/LV1/PR Readiness proof.

Hardening Comparison Checklist: Complete - H1 compared actual files, fields, fixtures, UI copy, approval boundaries, source truth, branch plan, Runtime Branch Engineering Contract, and overlap posture against this plan and found no remaining H1 blocker.

Live Validation Proof Or Waiver Checklist: Complete - LV1 classified this branch as disabled/status-only setup contract readiness scaffolding, proved no provider setup, no consent collection, no prompt acceptance, no provider-visible data, no downloads, no network egress, no memory indexing, and no voice/Core sync, and recorded a source-truth-supported User Test Summary waiver.

PR Readiness Fold-Down / Retention Checklist: Complete - PR Readiness Stage 1 folds this plan into branch record/source truth, clears stale active-branch authority by moving this branch to projected historical/no-active posture, proves selected-next defer/waiver truth, proves pre-PR live-state truth, proves no-release-debt posture, and preserves pending USER decisions.

Release Readiness Public-Scope Translation Checklist: release readiness must describe this branch as setup contract readiness/status-only scaffolding; it must not claim provider setup, consent collection, SDK/model execution, functional AI, or `v1.8.0-prebeta` execution.

USER Planning Review: Complete through Live Validation LV1 and PR Readiness Stage 1 source-truth repair; PR Readiness Stage 2 / PR creation is the next USER decision.

PR Fold-Down Packet: Ready for Stage 2 - PR Readiness Stage 1 folds down Workstream Green, H1 Green, LV1 Green, setup contract readiness proof, validation, approval-boundary, selected-next defer/waiver, pre-PR live-state, post-merge No Active Branch projection, release-window, and no-runtime-change evidence; PR creation remains pending USER approval.

Runtime Implementation Approval: Granted for the bounded setup contract readiness Workstream only; provider setup, consent collection, SDK/model execution, and provider/runtime execution remain pending USER decisions.

## Plan Status

Branch Readiness Stage 2 admitted this plan for `feature/fam-007-local-ai-provider-setup-contract-readiness`; the bounded Workstream implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair are complete and the branch is ready for PR Readiness Stage 2 / PR creation after USER approval.

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-setup-contract-readiness`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `b67e59df0481091bfbeb739c4b5e1954552bb421`
- Stage 2 setup purpose: create a fresh FAM-007 runtime carrier after `v1.7.10-prebeta` release closure.
- Prior FAM-007 released evidence: PR #179, setup/consent-flow readiness.

## Product Definition Plan Linkage

This branch advances FAM-007 by defining provider setup contract readiness. It does not implement provider setup, consent collection, provider SDK integration, prompt/model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer work, release work, PR creation, or merge.

## Runtime Branch Engineering Contract

- USER Engineering Planning Review: complete through Workstream Entry, bounded implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair; PR Readiness Stage 2 / PR creation approval pending.
- Runtime Implementation Approval: granted for bounded setup contract readiness implementation only.
- Current Runtime Baseline: released FAM-007 setup/consent-flow readiness from PR #179; provider setup future-gated; consent collection pending; provider-visible data `none`; `sentToProvider=false`; `canAcceptPrompts=false`; provider/model execution disabled.
- Planned Runtime Delta: setup contract state/schema, setup handoff criteria, provider profile/config requirements, consent prerequisites, approval gate posture, validator fixtures, and status/proof expectations.
- User-Facing Runtime Delta: status-only setup contract proof is available through Core/Desktop/ORIN state telemetry while the long desktop readiness display remains hidden/suppressed by default.
- State / Config / Schema Delta: setup contract readiness state/schema, provider profile/config requirements, prerequisites, approvals, handoff, and fold-down fields are implemented as local-only/static contract scaffolding.
- Validator / Helper Delta: FAM-007 provider state validation covers setup contract fixtures and suppression continuity.
- Expected Changed Files / Surfaces: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md`, this plan, `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/worktree_slots.md`, `Docs/validation_helper_registry.md`, `desktop/ai_provider_state.py`, Core/Desktop renderers, ORIN visual surfaces, and `dev/orin_ai_provider_state_validation.py`.
- Approval-Boundary Audit: all provider/runtime execution work remains pending USER decision.
- Future-Gated Items: provider setup implementation, consent collection, SDK/model execution, model downloads, external calls, memory/learning/personalization, voice/Core sync, shortcuts/installers, PR/merge/release, and `v1.8.0-prebeta`.
- Workstream Seam Map: admitted below.
- Proof Expectations: source truth, validator coverage, setup contract fixtures, UI/status copy mapping if touched, no provider-visible data, no prompt acceptance, no execution.
- Risk Forecast: FAM-006 dirty shared docs are a later PR/merge reconciliation risk; Compact-AI unique commits remain protected.
- Recommendations And Alternatives: setup contract readiness is preferred before provider adapter/SDK or prompt/model execution proof.
- Plan Version / Revision Status: v1, Stage 2 admitted.
- Plan-To-Implementation Traceability: each seam must map changes, fixtures, validation, and approval-boundary proof back to this plan.

## Current Runtime / Source-Truth Baseline

- FAM-007 provider path and setup/consent-flow readiness evidence has been released.
- Provider path remains local/status-only unless future USER approval changes it.
- Provider setup is not implemented.
- Consent collection is not implemented.
- Provider SDK/model execution is not implemented.
- Provider-visible data remains `none`.
- `sentToProvider` remains `false`.
- `canAcceptPrompts` remains `false`.
- Downloads/install, network egress, memory/indexing/learning/personalization, and voice/Core sync remain gated.
- The long desktop AI-owned readiness display was suppressed by the released setup/consent-flow branch and remains historical FAM-007 evidence.

## Workstream Label

FAM-007 Local AI Provider Setup Contract Readiness.

## Provider Setup Contract Readiness Definition

Provider Setup Contract Readiness is the FAM-007 layer after setup/consent-flow readiness. It defines setup contract state, setup handoff criteria, provider profile/config requirements, consent prerequisites, validation fixtures, UI/status proof expectations, and future setup execution boundaries while keeping real provider setup pending USER approval.

## Admitted Seam Families

### 1. Provider Setup Contract State and Schema

- Define setup contract readiness state.
- Define setup contract eligibility.
- Define setup contract blockers.
- Define setup contract reason codes.
- Define setup contract provenance.
- Define setup contract schema/version fields.
- Preserve setup execution as pending USER decision.

### 2. Provider Profile / Configuration Contract Requirements

- Define provider profile requirements needed before setup can be implemented later.
- Define provider configuration requirement posture.
- Define local/null fallback dependency posture.
- Define provider availability and capability contract dependencies.
- Preserve real provider configuration and SDK integration as pending USER decisions.

### 3. Setup Preconditions and Consent Prerequisite Contract

- Define setup precondition posture.
- Link setup consent and execution consent prerequisites without collecting consent.
- Link provider-visible-data, audit, data classification, manifest, safety, capability, network, memory, and voice/Core gates.
- Preserve consent collection and execution approval as pending USER decisions.

### 4. Setup Handoff and Approval Gate Planning

- Define future setup handoff fields.
- Define setup approval status.
- Define setup execution approval status.
- Define future setup UX handoff posture.
- Preserve provider setup implementation as pending USER decision.

### 5. Core/Desktop/ORIN Setup Contract Status UI and Proof

- Define status-only copy expectations for setup contract readiness.
- Confirm copy distinguishes setup contract readiness, setup flow readiness, consent readiness, provider setup, provider execution, and functional AI.
- Preserve no provider setup, consent collection, prompt acceptance, provider execution, or functional-AI behavior change.
- Preserve compact/non-invasive status posture established by prior FAM-007 work.

### 6. Functional-AI and v1.8.0 Continuation Criteria

- Define how setup contract readiness feeds future functional-AI criteria.
- Define criteria still unsatisfied before provider setup/execution.
- Preserve `v1.8.0-prebeta` as a later USER-approved release execution target after functional-AI proof.

## Workstream Implementation Result

Workstream Completion State: `Green - bounded setup contract readiness implementation complete; Hardening H1 and Live Validation LV1 are Green`.

Seam Family 1 - Provider Setup Contract State and Schema: `Green - setup contract readiness state, eligibility, blocker, reason, provenance, schema versioning, config schema, approval status, gate state, and future handoff fields are centralized in desktop/ai_provider_state.py`.

Seam Family 2 - Provider Profile / Configuration Contract Requirements: `Green - provider profile required fields, provider config required fields, config readiness posture, profile gate, local/null fallback, setup approval, execution approval, SDK handoff, and validation posture are represented without real config mutation`.

Seam Family 3 - Setup Preconditions and Consent Prerequisite Contract: `Green - setup consent, execution consent, provider-visible-data, audit, data classification, safety/eval, capability, manifest, network, local-only, memory/indexing, and voice/Core prerequisites remain explicit and future-gated`.

Seam Family 4 - Setup Handoff and Approval Gate Planning: `Green - future provider setup branch handoff, setup approval gate, execution approval gate, provider path handoff, consent handoff, config/profile handoff, UI handoff, validator handoff, and PR/release fold-down handoff are recorded as local-only contract proof`.

Seam Family 5 - Core/Desktop/ORIN Setup Contract Status UI and Proof: `Green - Core/Desktop/ORIN state publication includes setup contract telemetry and hidden status rows; the long AI-owned desktop readiness display remains hidden/suppressed by default`.

Seam Family 6 - Functional-AI and v1.8.0 Continuation Criteria: `Green - functional AI and v1.8.0-prebeta criteria remain unsatisfied by design until separate USER-approved provider setup, consent, adapter, prompt routing, model execution, provider-visible-data, and release proof work`.

Runtime Safety Posture: `Provider setup not implemented; consent collection not implemented; SDK/model execution not implemented; provider-visible data none; sentToProvider=false; canAcceptPrompts=false; downloads/install blocked; network egress blocked; memory/indexing disabled; voice/Core sync gated`.

Validator Proof: `dev/orin_ai_provider_state_validation.py` covers default setup contract unavailable, blocked-by-provider-path, blocked-by-config, setup consent, execution consent, policy, capability, manifest, safety, future-gated, approval-missing, provider-profile-missing, provider-config-missing, provider-config-invalid, ready-for-future-setup-branch, degraded/fail-closed, desktop readiness display suppression continuity, no provider-visible data, no prompt/model execution, blocked downloads/install, blocked network, disabled memory, and gated voice fixtures.

## Hardening H1 Result

Hardening H1 Result: `Green - implementation matches the admitted Branch Runtime Engineering Plan, Product Definition Plan, Runtime Branch Engineering Contract, and Workstream seam map. Setup contract state/schema, provider profile/config requirements, setup preconditions, setup and execution consent prerequisites, handoff/approval gates, Core/Desktop/ORIN status proof, desktop readiness display suppression continuity, validator fixtures, UI copy integrity, functional-AI/v1.8.0 pending criteria, approval boundaries, and overlap posture were inspected and validated.`

H1 Repairs Applied: `Source-truth fold-down only - this plan, the branch record, backlog/roadmap current-state pointers, and the worktree slot receipt were updated from Workstream Green / H1-next to H1 Green / LV1-next. No provider setup, consent collection, SDK/model execution, runtime behavior, production UI behavior, PR, merge, release, cleanup, FAM-006, Governance, or Compact-AI mutation was performed.`

## Live Validation LV1 Result

Live Validation LV1 Result: `Green - LV1 classified this branch as disabled/status-only local setup contract readiness scaffolding, used static Core/Desktop/ORIN source-truth plus provider-state validator proof as the applicable User Test Summary substitute, proved desktop readiness display suppression continuity, and confirmed provider setup, consent collection, prompt/provider/model execution, downloads, network, memory/indexing/learning/personalization, voice/Core sync, shortcut, installer, release, PR, and merge work remain unapproved.`

User Test Summary Result: `WAIVED - no user-operated provider setup, consent collection, prompt, model, setup, shortcut, installer, network, memory, or voice/Core path is enabled; static validator/source-truth proof is the applicable substitute.`

LV1 Repairs Applied: `Source-truth fold-down only - this plan, the branch record, backlog/roadmap current-state pointers, and the worktree slot receipt were updated from H1 Green / LV1-next to LV1 Green / PR Readiness Stage 1-next. No provider setup, consent collection, SDK/model execution, runtime behavior, production UI behavior, PR, merge, release, cleanup, FAM-006, Governance, or Compact-AI mutation was performed.`

## Validation Plan

Required Workstream validation:

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

This Workstream adds setup contract readiness fixtures in `dev/orin_ai_provider_state_validation.py`.

## Release / Continuation Posture

- `v1.7.10-prebeta` is the latest public prerelease after Stage 2 canon closure.
- PR #182 through PR #187 are recorded as released in `v1.7.10-prebeta`.
- `v1.8.0-prebeta` remains a future functional-AI jump target after separate USER approval and proof.

## Overlap And Cleanup Posture

- FAM-006 overlap: later PR/merge reconciliation risk only.
- Governance overlap: standing intake lane only.
- Compact-AI-Status-Card: protected unique commits remain preserved.
- Cleanup/rebinding: planning only; no branch deletion, worktree deletion, or rebinding execution is admitted by this plan.

## Next Legal Phase

PR Readiness Stage 2 / PR creation after USER approval.

## Exact USER Decision Needed

Approve PR Readiness Stage 1 for `FAM-007 Local AI Provider Setup Contract Readiness`.
