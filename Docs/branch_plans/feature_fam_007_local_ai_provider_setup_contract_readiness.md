# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Setup Contract Readiness

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-setup-contract-readiness; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Setup Contract Readiness - Branch Runtime Engineering Plan v1`

Owning Branch: `feature/fam-007-local-ai-provider-setup-contract-readiness`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md`

Current Phase: `Branch Readiness`

Branch Runtime Engineering Plan: Accepted - this plan is present for the FAM-007 setup contract readiness carrier.

Engineering Plan Status: Accepted

Current Runtime Baseline: PR #179 released FAM-007 setup/consent-flow readiness with provider setup future-gated, consent collection pending, provider-visible data `none`, `sentToProvider=false`, `canAcceptPrompts=false`, prompt/model execution disabled, downloads blocked, network egress blocked, memory/indexing disabled, and voice/Core sync gated.

Branch Purpose: define setup contract readiness as the next FAM-007 layer after setup/consent-flow readiness, preserving a status-only/local posture before any real provider setup, consent collection, SDK integration, or model execution.

Planned Runtime Delta: add setup contract state/schema planning, provider profile/config requirements, setup preconditions, consent prerequisites, setup handoff criteria, approval gate posture, validator fixture expectations, and short status-proof mapping without activating setup.

User-Facing Delta: no Stage 2 production UI change; future Workstream implementation may add or refine concise Core/Desktop/ORIN status-only setup contract copy that does not imply provider setup, consent collection, prompt acceptance, or functional AI.

Source-Truth Delta: record fresh FAM-007 branch authority, close `v1.7.10-prebeta` release-canon drift, admit this branch plan, update current carrier posture, and preserve FAM-006/Governance/Compact-AI overlap as later reconciliation context only.

State / Config / Schema Delta: planned setup contract readiness fields, setup precondition fields, setup approval fields, provider profile/config requirement fields, consent prerequisite fields, provenance/reason/schema markers, and future handoff markers only.

Validator / Helper Delta: future Workstream should extend `dev/orin_ai_provider_state_validation.py`, `dev/orin_validation_suite.py`, and any setup contract fixtures required by repo truth; Stage 2 validates existing governance, source-owner, provider-state, and release-health gates.

Expected Changed Files / Surfaces: Stage 2 touches branch record, branch plan, backlog, roadmap, branch index, and worktree slot receipt; future Workstream may touch provider state, Core/Desktop renderers, ORIN visual surfaces, and validators only after USER approval.

Workstream / Seam Map: Seam 1 setup contract state/schema; Seam 2 provider profile/config requirements; Seam 3 setup preconditions and consent prerequisites; Seam 4 setup handoff and approval gates; Seam 5 Core/Desktop/ORIN setup contract status proof; Seam 6 functional-AI and v1.8.0 continuation criteria.

Per-Seam Implementation Checklist: for each seam, identify source fields, source-truth records, runtime or UI surfaces if any, validator fixture needs, approval-boundary proof, and future-gated items before editing implementation files.

Per-Seam Validation Checklist: run diff checks, branch governance, release-health, source-owner marker, AI provider state, planning fixture, validation suite, rebaseline audit, compileall, and any new setup contract validator fixtures introduced by the Workstream.

Per-Seam User-Facing Proof Checklist: each seam must include user-visible proof or a waiver; if Core/Desktop/ORIN copy changes, capture visible status-only proof, screenshot/static validator evidence, and confirmation that copy does not imply provider setup, consent collection, provider execution, functional AI, or `v1.8.0-prebeta` release readiness.

Future-Gated Items: future provider setup implementation, consent collection, provider SDK integration, provider/model execution, model downloads, external calls, memory/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release, FAM-006 mutation, Governance mutation outside this branch, Compact-AI mutation, and `v1.8.0-prebeta` remain gated, blocked, and pending later USER approval.

Approval-Boundary Audit: Stage 2 and the planned Workstream may define contracts, state, gates, UI proof, and validators only; real setup execution, consent collection, provider communication, provider-visible data, prompt routing, model workload execution, downloads, network egress, memory, voice/Core sync, shortcut/installer work, release, PR creation, merge, issue work, cleanup, and cross-lane mutation require later USER approval.

FAM / Shared-Surface Overlap Forecast: FAM-006 dirty shared docs are later PR/merge reconciliation risk only; Governance is standing intake context only; Compact-AI has protected unique commits and must not be mutated by this branch; FAM-007 owns only this localized branch/worktree path.

Open Questions: USER must decide whether to approve Workstream Entry, then whether to approve implementation; future questions include whether setup contract status should remain source-only or touch Core/Desktop/ORIN copy, and when real provider setup or consent collection should be admitted.

USER Planning Decisions: USER approved Branch Readiness Stage 2 setup for this branch; USER decisions remain pending for Workstream implementation, provider setup, consent collection, SDK/model execution, PR creation, merge, release, cleanup, and future functional-AI work.

Plan Revision History: v1 created during Branch Readiness Stage 2 from `origin/main` at `b67e59df0481091bfbeb739c4b5e1954552bb421`, carrying `v1.7.10-prebeta` canon closure and PR #179 FAM-007 released evidence.

Plan-To-Implementation Traceability Table: planned setup contract state maps to provider-state implementation and fixtures; planned profile/config requirements map to metadata/config envelope proof; planned consent prerequisites map to setup/execution consent posture; planned UI proof maps to Core/Desktop/ORIN copy if touched; planned continuation criteria map to H1/LV1/PR Readiness proof.

Hardening Comparison Checklist: H1 must compare actual files, fields, fixtures, UI copy, approval boundaries, source truth, branch plan, Runtime Branch Engineering Contract, and overlap posture against this plan before reporting green.

Live Validation Proof Or Waiver Checklist: LV1 must classify source/static/status-only behavior, prove no provider setup, no consent collection, no prompt acceptance, no provider-visible data, no downloads, no network egress, no memory indexing, and no voice/Core sync, or record a source-truth-supported waiver for non-UI changes.

PR Readiness Fold-Down / Retention Checklist: PR Readiness must retain or fold this plan into branch record/source truth, clear stale active-branch wording, prove selected-next or waiver truth, prove no-release-debt posture, and preserve pending USER decisions.

Release Readiness Public-Scope Translation Checklist: release readiness must describe this branch as setup contract readiness/status-only scaffolding unless later Workstream evidence proves more; it must not claim provider setup, consent collection, SDK/model execution, functional AI, or `v1.8.0-prebeta` execution.

USER Planning Review: Pending Workstream Entry approval; USER may approve, change, defer, or reject the plan before implementation.

PR Fold-Down Packet: Pending

Runtime Implementation Approval: Pending USER approval; Stage 2 does not grant Workstream implementation or provider/runtime execution approval.

## Plan Status

Branch Readiness Stage 2 setup admitted this plan for `feature/fam-007-local-ai-provider-setup-contract-readiness`. Workstream implementation has not started and requires later USER approval.

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-setup-contract-readiness`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `b67e59df0481091bfbeb739c4b5e1954552bb421`
- Stage 2 setup purpose: create a fresh FAM-007 runtime carrier after `v1.7.10-prebeta` release closure.
- Prior FAM-007 released evidence: PR #179, setup/consent-flow readiness.

## Product Definition Plan Linkage

This branch advances FAM-007 by defining provider setup contract readiness. It does not implement provider setup, consent collection, provider SDK integration, prompt/model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer work, release work, PR creation, or merge.

## Runtime Branch Engineering Contract

- USER Engineering Planning Review: required at Workstream Entry.
- Runtime Implementation Approval: pending USER decision.
- Current Runtime Baseline: released FAM-007 setup/consent-flow readiness from PR #179; provider setup future-gated; consent collection pending; provider-visible data `none`; `sentToProvider=false`; `canAcceptPrompts=false`; provider/model execution disabled.
- Planned Runtime Delta: setup contract state/schema, setup handoff criteria, provider profile/config requirements, consent prerequisites, approval gate posture, validator fixtures, and status/proof expectations.
- User-Facing Runtime Delta: none during Stage 2; future Workstream may add short status-only Core/Desktop/ORIN setup contract proof if repo truth supports it.
- State / Config / Schema Delta: setup contract readiness planning only until implementation approval.
- Validator / Helper Delta: extend FAM-007 provider state validation and validation suite coverage during Workstream implementation if repo truth supports it.
- Expected Changed Files / Surfaces: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_contract_readiness.md`, this plan, `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/branch_records/index.md`, `Docs/worktree_slots.md`, and future Workstream files discovered by source truth.
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
- Preserve no production UI behavior change unless future Workstream implementation is approved.
- Preserve compact/non-invasive status posture established by prior FAM-007 work.

### 6. Functional-AI and v1.8.0 Continuation Criteria

- Define how setup contract readiness feeds future functional-AI criteria.
- Define criteria still unsatisfied before provider setup/execution.
- Preserve `v1.8.0-prebeta` as a later USER-approved release execution target after functional-AI proof.

## Validation Plan

Required Stage 2 validation:

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

Future Workstream validation should add any setup contract readiness fixtures required by repo truth.

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

Workstream Entry analysis after USER approval.

## Exact USER Decision Needed

Approve Workstream Entry analysis for `FAM-007 Local AI Provider Setup Contract Readiness`.
