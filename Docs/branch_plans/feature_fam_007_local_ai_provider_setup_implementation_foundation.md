# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Setup Implementation Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-setup-implementation-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Setup Implementation Foundation - Branch Runtime Engineering Plan v1`

Owning Branch: `feature/fam-007-local-ai-provider-setup-implementation-foundation`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_implementation_foundation.md`

Current Phase: `PR Readiness Stage 1 complete - FAM-007 setup implementation foundation`

Branch Runtime Engineering Plan: Accepted - this plan is present for the FAM-007 setup implementation foundation carrier.

Engineering Plan Status: Accepted - implemented for the bounded Workstream, inspected through H1 Green, validated through LV1 Green, and PR Readiness Stage 1 source-truth repair is complete; PR Readiness Stage 2 / PR creation remains pending USER approval.

Current Runtime Baseline: Released FAM-007 state already includes provider readiness, activation, execution-readiness, provider path/consent readiness, setup/consent-flow readiness, and setup contract readiness, with provider-visible data none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads and network blocked, memory disabled, voice/Core sync gated, desktop readiness display suppression preserved, and validation helper coverage in `dev/orin_ai_provider_state_validation.py`.

Branch Purpose: Move FAM-007 from setup contract planning toward a local provider setup implementation foundation that can create a safe setup entry point, provider profile/config write-path foundation, validation envelope, and status proof while preserving consent collection and provider/model execution as future USER decisions.

Planned Runtime Delta: The Workstream adds local setup entry/foundation state, provider profile/config draft posture, fail-closed validation and persistence posture, local/null fallback proof, future setup implementation handoff, Core/Desktop/ORIN status telemetry, validator fixtures, and source-truth fold-down without enabling provider SDK calls, prompt routing, model execution, model downloads, network egress, memory indexing, or voice/Core runtime sync.

Implemented Runtime Delta: The planned runtime delta is implemented as local-only setup foundation state/schema, telemetry, and validator fixtures with real provider setup still future-gated.

User-Facing Delta: Users should see truthful setup-foundation posture or a disabled/status-only setup entry that explains local setup is not complete, consent collection and execution remain future-gated, provider-visible data remains none, and functional AI is not yet operational; any visible copy must stay short, accurate, and consistent with desktop readiness display suppression.

Source-Truth Delta: Stage 2 records `v1.7.11-prebeta` closure, PR #190 as released setup contract readiness evidence, PR #191 as release-readiness source-truth support, active FAM-007 branch authority, Product Definition Plan fields, Runtime Branch Engineering Contract fields, this Branch Runtime Engineering Plan, bounded seam admission, FAM-006/Governance/Compact-AI overlap posture, and future-gated approval boundaries.

State / Config / Schema Delta: Planned implementation may introduce setup-entry state, profile/config draft fields, validation result fields, schema/provenance markers, local/null fallback persistence posture, setup approval flags, setup handoff markers, and audit/status fields, but it must not store secrets, provider credentials, consent grants, prompts for provider use, memory indexes, or model artifacts.

Validator / Helper Delta: `dev/orin_ai_provider_state_validation.py` now covers default setup foundation, missing/invalid setup foundation config, profile missing/invalid, config missing/invalid, validation failed, setup consent required, execution consent required, approval missing, local-draft ready, future-setup-branch ready, fail-closed persistence, local/null fallback, setup status mapping, provider-visible-data none, prompt execution disabled, downloads/network/memory/voice gates, and desktop readiness display suppression continuity.

Expected Changed Files / Surfaces: Expected surfaces are `Docs/branch_records/feature_fam_007_local_ai_provider_setup_implementation_foundation.md`, this plan, `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/worktree_slots.md`, `Docs/validation_helper_registry.md`, `desktop/ai_provider_state.py`, `desktop/desktop_renderer.py`, `desktop/core_visualization_renderer.py`, `nexus_visual/orin_core.*`, and `dev/orin_ai_provider_state_validation.py`; sibling worktrees and non-FAM-007 branches are excluded.

Workstream / Seam Map: Seam 1 setup entry point and local setup flow shell; Seam 2 provider profile and config write-path foundation; Seam 3 setup validation and fail-closed persistence; Seam 4 setup status UI plus Core/Desktop/ORIN proof; Seam 5 consent boundary preservation and handoff; Seam 6 functional-AI and v1.8.0 continuation criteria.

Per-Seam Implementation Checklist: For each seam, identify source state, config/schema fields, UI/status copy if any, validator fixtures, fail-closed behavior, future-gated approval boundary, affected file surface, and rollback expectation before editing implementation files.

Per-Seam Validation Checklist: Run diff checks, branch governance, release-health, source-owner marker, AI provider state validation, planning fixtures, runtime-fam007 validation suite, worktree rebaseline audit, compileall, and any new setup foundation fixtures introduced by the Workstream.

Per-Seam User-Facing Proof Checklist: If setup copy or visual posture changes, prove the status-only user-facing surface with static Core/Desktop/ORIN inspection or screenshot evidence, confirm no long readiness box returns, and confirm copy does not imply consent collection, provider execution, functional AI, downloads, network calls, memory, or v1.8.0 completion.

Future-Gated Items: Provider setup beyond the admitted foundation, consent collection, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcuts/installers, PR creation, merge, release, issue work, FAM-006 mutation, Governance mutation outside this branch, Compact-AI mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain gated.

Approval-Boundary Audit: Stage 2 may record source truth and admit a future Workstream only; Workstream implementation later may build local setup foundation and validation scaffolding, but real consent collection, provider communication, provider-visible prompts, model work, network egress, memory, voice/Core sync, shortcut/installer changes, release, PR creation, merge, cleanup, and cross-lane mutation require separate USER approval.

FAM / Shared-Surface Overlap Forecast: FAM-006 is a later PR/merge reconciliation risk only; Governance is standing intake context and must not be mutated here; Compact-AI has protected unique commits and remains preserved; shared source-truth and ORIN/Core/Desktop surfaces require careful PR readiness reconciliation if other lanes advance before this branch merges.

Open Questions: USER must later decide when PR Readiness Stage 1, PR creation, real provider setup beyond the local foundation, consent collection, SDK/model execution, and functional-AI proof are admissible, and when that proof is strong enough for a v1.8.0-prebeta release decision.

USER Planning Decisions: USER approved Branch Readiness Stage 1, selected the detailed setup implementation foundation successor, approved Stage 2 setup in the FAM-007 worktree, approved bounded Workstream implementation, approved Hardening H1, approved Live Validation LV1, and approved PR Readiness Stage 1 selected-next defer/pre-PR live-state source-truth repair. PR Readiness Stage 2 / PR creation, merge, release, provider SDK/model work, consent collection, memory, voice/Core, shortcuts/installers, cleanup, AI Product Contract import, and v1.8.0 execution remain pending.

Plan Revision History: v1 created during Branch Readiness Stage 2 from `origin/main` at `2158ff66649f9d2e045fe75c4813c19e88d06762`, after `v1.7.11-prebeta` publication and release-canon closure.

Plan-To-Implementation Traceability Table: Planned setup-entry state maps to provider-state implementation and fixtures; planned profile/config write path maps to local/null fallback and validation proof; planned UI/status proof maps to Core/Desktop/ORIN status surfaces; planned consent boundaries map to future-gated setup and execution consent posture; planned continuation criteria map to H1, LV1, PR Readiness, and Release Readiness fold-down.

Hardening Comparison Checklist: Required after Workstream implementation; H1 must compare actual setup entry state, profile/config write path, validation, UI/status proof, consent boundaries, no-execution posture, source truth, branch plan, Runtime Branch Engineering Contract, and overlap posture against this plan.

Live Validation Proof Or Waiver Checklist: LV1 must classify the branch from repo truth, prove static/runtime validator state when setup remains disabled/status-only, capture user-facing proof or waiver for any visible setup surface, and keep provider-visible data none, prompt execution disabled, downloads/network/memory blocked, and voice/Core sync gated.

PR Readiness Fold-Down / Retention Checklist: PR Readiness must fold setup foundation scope into branch record/source truth, resolve selected-next or USER waiver truth, prove release-window/no-release-debt posture, preserve active branch authority cleanup, and keep live PR/watcher state out of merge-target current-state owners.

Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as local provider setup implementation foundation only, exclude consent collection, provider SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.

USER Planning Review: Accepted for Branch Readiness Stage 2 setup, Workstream Entry, bounded Workstream implementation, Hardening H1, and Live Validation LV1.

PR Fold-Down Packet: Stage 1 complete - selected-next defer/waiver, pre-PR live-state, post-merge No Active Branch projection, Release Readiness Health Pass, Release Window Audit, branch-authority historical projection, and Stage 2 approval boundary are recorded in the branch record. Live PR metadata belongs to PR Readiness Stage 2 after USER approves PR creation.

Runtime Implementation Approval: USER-approved bounded Workstream implementation is complete; provider setup beyond the local foundation remains pending USER approval.

## Plan Status

Workstream implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair are green for `feature/fam-007-local-ai-provider-setup-implementation-foundation`. The plan is current for PR Readiness Stage 2 review; provider setup beyond the local foundation begins only after later USER approval.

## Workstream Green Fold-Down

Workstream Status: `Green - bounded setup implementation foundation complete`

Implementation Summary: Central provider state now publishes `provider_setup_foundation_*` / `providerSetupFoundation*` setup foundation fields, schema versions, config/profile draft posture, validation and persistence posture, local/null fallback proof, approval status, future setup handoff, and fold-down posture. Core/Desktop/ORIN receive hidden telemetry rows and data attributes while the long desktop AI-owned readiness display remains suppressed by default.

Safety Summary: Provider-visible data remains `none`, `sentToProvider=false`, `canAcceptPrompts=false`, prompt/provider/model execution remains disabled, downloads/install remain blocked, network/external calls remain blocked, memory/indexing/learning/personalization remains disabled or deferred, and voice/Core sync remains gated.

Next Legal Phase: `PR Readiness Stage 1`

## Hardening H1 Result

Hardening H1 Result: `Green - H1 compared actual implementation against this Branch Runtime Engineering Plan, Product Definition Plan, Runtime Branch Engineering Contract, and admitted Workstream seams. Setup entry state, provider setup foundation schema, provider profile/config draft posture, fail-closed validation and persistence posture, local/null fallback proof, consent boundary handoff, Core/Desktop/ORIN hidden telemetry, desktop readiness display suppression continuity, validator fixtures, UI copy, functional-AI/v1.8.0 pending criteria, approval boundaries, and overlap posture are aligned.`

H1 Repairs Applied: `Source-truth fold-down only - this plan, the branch record, backlog/roadmap current-state pointers, and the worktree slot receipt were updated from Workstream Green / H1-next to H1 Green / LV1-next. No provider setup beyond the admitted foundation, consent collection, SDK/model execution, runtime behavior, production UI behavior, PR, merge, release, cleanup, FAM-006, Governance, or Compact-AI mutation was performed.`

H1 Validation Posture: `Green after required diff checks, branch governance validation, release-readiness health gate, governance efficiency validation, release body validation, AI provider validation, source-owner marker validation, branch-readiness planning fixture validation, runtime-fam007 validation suite, rebaseline audit, monitoring HUD validators, and compileall.`

Live Validation LV1 Handoff: `Complete - LV1 classified this branch as disabled/status-only local setup implementation foundation and used static Core/Desktop/ORIN plus provider-state validator proof as the applicable proof path.`

Next Legal Phase After LV1: `PR Readiness Stage 1`

## Live Validation LV1 Result

Live Validation LV1 Result: `Green - LV1 classified this branch as disabled/status-only local setup implementation foundation, used static Core/Desktop/ORIN source truth plus provider-state validator proof as the applicable User Test Summary substitute, proved desktop readiness display suppression continuity, and confirmed provider setup beyond the local foundation, consent collection, prompt/provider/model execution, downloads, network, memory/indexing/learning/personalization, voice/Core sync, shortcut, installer, release, PR, and merge work remain unapproved.`

LV1 Repairs Applied: `Source-truth fold-down only - this plan, the branch record, backlog/roadmap current-state pointers, and the worktree slot receipt were updated from H1 Green / LV1-next to LV1 Green / PR Readiness Stage 1-next. No provider setup beyond the admitted foundation, consent collection, SDK/model execution, runtime behavior, production UI behavior, PR, merge, release, cleanup, FAM-006, Governance, or Compact-AI mutation was performed.`

User Test Summary Results: `WAIVED`

User Test Summary Waiver Reason: `Disabled/status-only local setup implementation foundation scaffold with no user-operated setup path enabled; static Core/Desktop/ORIN source truth and provider-state validator proof are the applicable substitute.`

LV1 Validation Posture: `Green after required diff checks, branch governance validation, release-readiness health gate, governance efficiency validation, release body validation, AI provider validation, source-owner marker validation, branch-readiness planning fixture validation, runtime-fam007 validation suite, rebaseline audit, monitoring HUD validators, and compileall.`

PR Readiness Stage 1 Result: `Complete - folded down Workstream Green, H1 Green, LV1 Green, UTS waiver, desktop readiness display suppression continuity, selected-next defer/waiver truth, pre-PR live-state, post-merge No Active Branch projection, release-window posture, approval boundaries, Release Readiness Health Pass, and validation proof before PR creation is requested.`

PR Readiness Stage 2 Next: `Pending USER approval - create the PR, validate live PR state, watcher provisioning, mergeability, checks, review state, and PR body/operator copy before any merge decision is requested.`

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-setup-implementation-foundation`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Base / merge base: `origin/main` at `2158ff66649f9d2e045fe75c4813c19e88d06762`
- Latest public prerelease baseline: `v1.7.11-prebeta`
- Prior FAM-007 released setup evidence: PR #179 setup/consent-flow readiness and PR #190 setup contract readiness.

## Workstream Label

FAM-007 Local AI Provider Setup Implementation Foundation.

## Admitted Seam Families

### 1. Setup Entry Point and Local Setup Flow Shell

- Define setup entry state and disabled/local-only setup flow shell.
- Preserve consent collection and provider execution as future USER decisions.

### 2. Provider Profile / Config Write Path Foundation

- Define provider profile/config draft requirements, validation inputs, and local/null fallback posture.
- Preserve credentials, secrets, SDK integration, and real provider setup as future USER decisions.

### 3. Setup Validation and Fail-Closed Persistence

- Define fail-closed validation behavior, invalid-config blockers, persistence posture, and schema/provenance markers.
- Preserve downloads, external calls, model execution, and memory indexing as blocked.

### 4. Setup Status UI / Core Desktop ORIN Proof

- Define short truthful status-only setup posture and map it to centralized provider state.
- Preserve desktop readiness display suppression continuity.

### 5. Consent Boundary Preservation and Handoff

- Keep setup consent and execution consent distinct, future-gated, and not collected.
- Preserve provider-visible data none and audit posture.

### 6. Functional-AI / v1.8.0 Continuation Criteria

- Define how setup foundation feeds later functional-AI proof.
- Preserve v1.8.0-prebeta release execution as a later USER decision.
