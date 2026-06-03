# Branch Runtime Engineering Plan: FAM-007 Local AI Provider User-Operated Consent UX Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-user-operated-consent-ux-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider User-Operated Consent UX Foundation - Branch Runtime Engineering Plan v1`
Owning Branch: `feature/fam-007-local-ai-provider-user-operated-consent-ux-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-007`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
Current Phase: `PR Readiness`
Branch Runtime Engineering Plan: Required and present for the FAM-007 user-operated consent UX foundation runtime carrier.
Engineering Plan Status: Present - Workstream implementation completed after current-main reconciliation to origin/main@63cf3ff45f238ef47836972e9e6ed54f2a49ede1; Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair are green, and the branch is ready for PR Readiness Stage 2 approval.
Current Runtime Baseline: `origin/main@63cf3ff45f238ef47836972e9e6ed54f2a49ede1` after PR #205 governance changes were accepted as authoritative and the FAM-007 branch was reconciled; PR #203 durable local consent persistence remains released evidence in `v1.7.17-prebeta`, with provider/model execution still disabled.
Branch Purpose: Admit the next FAM-007 successor that turns durable local consent persistence into USER-reviewable user-operated consent UX/status planning before provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, or functional AI.
Planned Runtime Delta: Implemented local user-operated consent UX state, local intent/control posture, durable consent handoff, revocation/reset UX mapping, setup/execution consent labels, Core/Desktop/ORIN status proof, validator fixtures, and LV1/UTS proof posture.
User-Facing Delta: The branch adds a safe consent UX/status surface contract and hidden-by-default Core/Desktop/ORIN status labels. Copy says this is local consent preparation and does not imply provider setup completion, prompt acceptance, provider/model execution, network/download readiness, memory activity, or functional AI.
Source-Truth Delta: Stage 2 recorded branch authority and planning truth; Workstream fold-down records current-main reconciliation to PR #205, Workstream Green, direct provider-state/UI/status validation, H1 Green, LV1 Green, and PR Readiness Stage 1 repair for selected-next defer / USER waiver truth, pre-PR live-state truth, post-merge No Active Branch projection, and Stage 2 PR creation routing.
State / Config / Schema Delta: Added local consent UX intent state, setup consent display state, execution consent display state, revocation/reset action posture, durable consent reference, local-only audit/provenance labels, provider-boundary blockers, and future setup handoff markers.
Validator / Helper Delta: Extended FAM-007 provider-state and UI/status validation to cover implemented consent UX behavior, durable handoff, setup/execution separation, provider-boundary preservation, display-suppression continuity, and LV1/UTS route.
Expected Changed Files / Surfaces: Implemented source-truth fold-down in this plan and the branch record, plus provider-state, Core/Desktop/ORIN status surfaces, and `dev/orin_ai_provider_state_validation.py`; compact pointer docs are updated only where validation requires.
Workstream / Seam Map: Seam 1 -> Consent UX State And Intent Contract; Seam 2 -> User-Operated Consent Controls And Local UX Boundary; Seam 3 -> Durable Consent Handoff And Revocation / Reset UX Mapping; Seam 4 -> Core/Desktop/ORIN Visible Or Hidden Status Proof And Display-Suppression Continuity; Seam 5 -> Provider Setup / Execution Gate Alignment From User Consent UX; Seam 6 -> Validator Fixtures, Live Validation Strategy, And Functional-AI / v1.8.0 Continuation Criteria.
Per-Seam Implementation Checklist: Each seam must name implementation files, state/schema changes, visible copy changes, durable-consent handoff behavior, no-provider/no-network/no-memory boundaries, validator changes, UI proof, and stop conditions before coding begins.
Per-Seam Validation Checklist: Run diff checks, branch governance, worktree confinement gate, release-readiness health gate, governance efficiency, release body, source-owner marker validation, branch-readiness planning fixtures, AI provider state validation, runtime-fam007 validation suite, rebaseline audit, compileall, and any seam-specific consent UX fixtures.
Per-Seam User-Facing Proof Checklist: If the seam changes visible UI, prove copy and layout through source inspection plus screenshots/live-client proof as required. If a seam remains hidden/status-only, record the waiver basis and prove no user-facing overclaim.
Future-Gated Items: `Future-gated and pending USER approval: provider setup completion, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, release execution, issue work, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`
Approval-Boundary Audit: Workstream implementation was USER-approved and completed only for the local user-operated consent UX foundation. Provider/model/network/memory/voice/shortcut/release/cleanup/sibling mutation remains blocked.
FAM / Shared-Surface Overlap Forecast: FAM-006 is a separate sibling lane and overlap context only; Governance PR #204 is in baseline; Compact-AI is protected historical work. None is successor authority for this FAM-007 branch.
Open Questions: None for LV1; the implemented surface is hidden/status-only, writes no provider payload, keeps setup/execution labels separate, maps revocation/reset as local-only status, and uses a UTS waiver because no meaningful manual user path exists.
USER Planning Decisions: USER approved Branch Readiness Stage 2 setup, Workstream Entry, current-main reconciliation, bounded Workstream implementation, H1, and LV1. PR creation, merge, release, provider setup completion, SDK/model execution, downloads/network, memory, voice/Core sync, shortcuts/installers, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain pending.
Plan Revision History: v1 created during Branch Readiness Stage 2 from origin/main@f072be65fc5f00202a684a20b3cbb4611536ab51 after v1.7.17-prebeta and Governance PR #204.
Plan-To-Implementation Traceability Table: Implemented. UX state maps to `desktop/ai_provider_state.py`; local controls/status posture maps to consent UX intent fields and suppressed Core/Desktop/ORIN status labels; durable handoff maps to PR #203 durable consent persistence helpers; revocation/reset maps to fail-closed UX labels; setup/execution labels map to provider-boundary blockers; validators map to `dev/orin_ai_provider_state_validation.py`; LV1 maps to hidden/status proof plus UTS waiver review unless H1 admits a visible manual path.
Hardening Comparison Checklist: H1 must compare implementation against this plan, Product Definition Plan, Runtime Branch Engineering Contract, Branch Vision Snapshot, Element-to-Phase Proof Matrix, UI copy, provider-boundary preservation, validators, display-suppression continuity, and source-truth fold-down.
Live Validation Proof Or Waiver Checklist: LV1 must classify the implemented surface, prove user-facing UX if present, run Codex Live Client Self-QA when applicable, record User Test Summary PASS or WAIVED, preserve provider-visible data none, and keep provider/model/network/memory/voice execution blocked.
PR Readiness Fold-Down / Retention Checklist: PR Readiness must project merge-stable branch authority, release-window posture, selected-next/defer truth, live PR/watcher state separation, branch cleanup plan, and source-truth retention/retirement decisions.
Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as local user-operated consent UX foundation only and exclude provider setup completion, SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.
USER Planning Review: Completed through Workstream Entry approval and current-main reconciliation approval for this bounded Workstream.
PR Fold-Down Packet: Pending.
Runtime Implementation Approval: USER-approved bounded Workstream implementation completed.

## Branch Vision Contract Snapshot

Branch Vision Snapshot Status: Accepted for this Workstream implementation.
Project-Wide Vision Alignment: Nexus should remain local-first, user-controlled, and honest about disabled provider behavior before model execution.
Family Vision Alignment: FAM-007 requires explicit provider-visible data, privacy, network/download, memory, and consent boundaries before runtime execution.
Branch-Specific Vision Alignment: User-operated consent UX should expose durable consent truth and controls without implying provider setup, prompt acceptance, provider/model execution, or functional AI.
Open Vision Questions: Resolved for LV1 - hidden/status-only proof is valid, formal UTS is waived, and PR Readiness may verify the waiver before PR creation.
USER Vision Green: Yes - USER approved Workstream Entry and bounded implementation after plan review.
Accepted Implementation Scope: Local-only consent UX state/intent contract, safe local controls/status posture, durable consent handoff, revocation/reset mapping, setup/execution consent separation, Core/Desktop/ORIN hidden status proof, validator fixtures, and future functional-AI criteria only.
Accepted Seam Map: All six admitted seam families are implemented in the current Workstream.
Accepted Stop Conditions: Stop only at Workstream Green, named blocker, or explicit USER waiver; current Workstream reached Green and routes next to H1.

## Product Definition Plan

Product Vision: FAM-007 should become useful local AI through explicit user control over setup, consent, provider-visible data, and execution before any model is allowed to run.
User-Facing Goal: Make consent readiness understandable and operable by the user while keeping provider setup and execution disabled.
Project-Wide Vision Alignment: This branch supports the Nexus-wide local-first assistant vision by making AI consent boundaries visible before AI behavior exists.
Branch-Specific Vision Alignment: This branch owns user-operated consent UX foundation only and does not admit provider setup completion or model execution.
USER Vision Questions: Which surface, which copy, which write behavior, which revocation/reset path, and which LV1 user checklist should be accepted?
USER Vision Question Packet: Completed through Workstream Entry review bundle and USER approval.
Codex Product Interpretation: Consent UX is the bridge between durable local consent persistence and later provider setup. It must be small, clear, reversible, and local-only.
Codex Implementation Recommendation: Build consent UX/status foundation before provider setup completion.
Codex Additional Recommendations: Keep the first UX modest, use separate setup/execution labels, make reset/revocation obvious, and avoid any functional-AI copy.
USER/ChatGPT Review Checkpoint: USER reviewed/approved Workstream Entry, implementation, H1, and LV1; PR Readiness remains a later approval phase.
USER Critique Loop: Workstream implementation proceeded under USER-approved bounded scope; H1 found zero repairs and LV1 recorded hidden/status-only proof with UTS waived.
USER Decision Ledger: Stage 2 setup, Workstream Entry, current-main reconciliation, Workstream implementation, H1, and LV1 approved; PR creation, merge, release, provider setup completion, SDK/model execution, downloads/external calls, memory, voice/Core sync, shortcuts/installers, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution remain pending.
Deferred Ideas / Future Package Ledger: Provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, AI Product Contract import, Private Dev ORIN import, v1.8.0 execution.
Planning Adequacy Review: Complete through LV1; PR Readiness must verify branch authority, LV1 waiver, source-truth fold-down, selected-next/defer truth, and pre-PR live-state posture.
Rejected Shallow Plan: A single consent button or copy-only label is rejected as insufficient without durable handoff, separation, blockers, proof, and LV1 strategy.
Alternatives And Tradeoffs Reviewed: Provider setup completion now is rejected as premature; SDK/model execution is rejected as out of scope; FAM-006 routing is rejected as sibling drift.
Whole-System Interaction Map: UI consent state reads durable local consent truth, presents safe labels/controls, records only local intent if admitted, feeds status proof, and leaves provider/model/network/memory/voice paths blocked.
Open Questions / USER Decision Points: PR Readiness Stage 2 / PR creation, merge, release, provider setup/execution, and all functional-AI decisions remain future-gated.
System Concept Model: Local consent UX is a UI/status/control layer, not a provider, model, download, memory, or network system.
Entity / Profile Model: Consent intent, setup consent display, execution consent display, durable consent reference, revocation/reset action posture, local audit/provenance label, provider blocker, future setup handoff marker.
User Workflow Model: User opens the consent/status surface, sees setup and execution consent separately, understands blocked provider behavior, and later may operate approved local consent controls.
Scale / Data Volume Model: Tiny local consent metadata only; no prompt payloads, provider responses, embeddings, model files, downloads, or memory indexes.
Configuration And State Model: Preserve local-only durable state, no-secrets posture, provider-payload exclusion, fail-closed defaults, and setup/execution separation.
Expected User-Facing Outcomes: Truthful local consent readiness copy and controls that do not claim functional AI.
Feature Element Breakdown: Consent UX state, controls/status surface, setup label, execution label, revocation/reset affordance, durable handoff, provider-boundary blockers, proof/fixtures, LV1/UTS path.
Minimum Viable vs Full System Boundary: Minimum is local consent UX foundation; full AI/provider setup/execution is future.
Current Branch vs Future Package Boundary: Current branch stops at consent UX foundation. Future branches own setup completion and execution.
Affected Files / Surfaces: Source truth, provider state, Core/Desktop/ORIN status, desktop renderer/UI surfaces if admitted, validators, LV1/UTS artifacts.
Branch Reach / Package-Size Proof: The branch covers multiple related UX, state, validation, and provider-boundary seams.
Why Branch Is Large Enough: It is the next coherent prerequisite between durable persistence and setup completion.
Why Not Split Into Tiny Branches: Splitting UX, state handoff, copy, and validator proof would make consent readiness less reliable.
Acceptance Criteria: Workstream Green requires source truth, direct validators, UI/status proof, provider-boundary preservation, validation, commit, and push for all admitted seams.
Screenshot / Live / User Test Summary Proof Requirements: H1/LV1 should treat the implemented surface as hidden/status-only unless live proof finds a visible manual path; formal UTS remains required only if visible user-operated controls are exposed.
Implementation Sequence Proposal: Workstream implementation complete; next sequence is H1, LV1, PR Readiness.
Planning Blockers: None for Workstream completion.
USER Decisions Needed: PR Readiness Stage 2 / PR creation approval is next.

## Interface Release Boundary

Primary Interface Release Surface: Core/Desktop/ORIN AI provider status payload and hidden-by-default consent UX labels backed by provider-state fixtures.
Interface Bundle User Approval: USER approved the bounded Workstream implementation; no second visible surface was introduced.
Fallback Point: Implemented status/telemetry-first foundation with no provider side effects; LV1 must confirm waiver basis if no meaningful manual path exists.
Interface Acceptance / Proof Path: Direct validators prove state/copy/boundary now; H1/LV1 must decide static/screenshot/live-client/UTS proof based on the hidden-by-default status surface.

## Runtime Branch Engineering Contract

USER Engineering Planning Review: Completed through Workstream Entry approval.
Engineering Contract Status: Accepted and implemented for Workstream scope.
Runtime Implementation Approval: USER-approved bounded Workstream implementation completed.
Branch Purpose: Admit and plan the FAM-007 user-operated local consent UX foundation after durable consent persistence and before provider setup completion.
Current Runtime Baseline: Durable consent persistence released in v1.7.17-prebeta; provider/model execution remains disabled.
Planned Runtime Delta: Local user-operated consent UX/status foundation over durable consent truth.
User-Facing Runtime Delta: Visible local consent controls/status if admitted.
State / Config / Schema Delta: Added user-operated consent UX state schema, intent schema, setup/execution display labels, revocation/reset local posture, durable handoff markers, provider setup/execution UX gates, and fail-closed/provider-boundary labels.
Validator / Helper Delta: Extended `dev/orin_ai_provider_state_validation.py` with direct fixtures for default, blocked, setup-only, execution-only, both-present, revoked, reset, expired, setup intent, execution intent, revoke intent, reset intent, invalid intent, renderer status keys, display suppression, and provider-boundary preservation.
Expected Changed Files / Surfaces: Implemented in source truth, provider state, Core/Desktop renderers, ORIN status markup/script/style, and AI provider-state validator.
Approval-Boundary Audit: Stage 2 setup only; all implementation and future AI/provider work pending.
Future-Gated Items: Provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, release, cleanup, AI Product Contract, Private Dev ORIN, v1.8.0.
Workstream Seam Map: Six seam families listed in the Branch Runtime Engineering Plan.
Proof Expectations: Direct validators, UI/status proof, provider-boundary preservation, LV1/UTS route.
Risk Forecast: High user-facing/provider-boundary risk.
Recommendations And Alternatives: Preferred consent UX foundation now; narrower status-only branch if USER rejects controls; setup completion later.
Plan Version / Revision Status: v1 active.
Plan-To-Implementation Traceability: Implemented and ready for H1 comparison.

## Workstream Admission

Workstream Label: `FAM-007 Local AI Provider User-Operated Consent UX Foundation`
Admission State: `Implemented under USER-approved bounded Workstream scope`
Package Completion State: `Workstream Green - all admitted seams implemented`
Bounded Seam Default: `One active seam at a time; bounded does not mean one-seam Workstream. Continue through admitted seams until Workstream Green, named blocker, or explicit USER waiver.`
Single-Seam Or Single-Slice Waiver Authority: `USER only`
Stop Basis: `Workstream Green; next legal phase is Hardening H1`

### Seam 1: Consent UX State And Intent Contract

Goal: Define local consent UX state, setup/execution display labels, allowed intent states, blocked/future-gated states, and fail-closed defaults.
Non-Includes: Provider setup completion, execution, external calls, memory, voice/Core, shortcuts/installers, release work.

### Seam 2: User-Operated Consent Controls And Local UX Boundary

Goal: Define and later implement approved local consent controls or status-only fallback inside one accepted interface boundary.
Non-Includes: Multiple interfaces without approval, functional AI, provider/model behavior.

### Seam 3: Durable Consent Handoff And Revocation / Reset UX Mapping

Goal: Map durable consent persistence truth into visible consent labels and local revocation/reset posture without weakening fail-closed behavior.
Non-Includes: Provider-side revocation, external provider state, network calls.

### Seam 4: Core/Desktop/ORIN Status Proof And Display-Suppression Continuity

Goal: Prove safe labels or telemetry and preserve long desktop AI-owned readiness display suppression unless later approved.
Non-Includes: False readiness, prompt acceptance, functional-AI claims.

### Seam 5: Provider Setup / Execution Gate Alignment

Goal: Prove setup consent never implies execution consent or provider/model readiness.
Non-Includes: Provider setup completion or execution.

### Seam 6: Validator Fixtures And Functional-AI / v1.8.0 Continuation Criteria

Goal: Add proof coverage for every implemented behavior and record future setup/execution continuation criteria.
Non-Includes: Release execution or v1.8.0 functional proof.

## Element-to-Phase Proof Matrix

Matrix Status: `Present - Workstream, H1, and LV1 proof folded down`
USER Review Status: `Accepted - Workstream Entry review and bounded implementation approval completed`
Open Element Questions: `None - LV1 classified the implemented hidden/status-only surface, confirmed the UTS waiver basis because no manual path exists, and kept provider setup/execution future-gated`
Element Coverage Owner: `Docs/branch_plans/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
Element Validation Ledger Owner: `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAM007-CUX-001 | Consent UX state and local intent model | Created | Implemented local UX intent fields, setup/execution labels, blocked states, and fail-closed defaults in provider state. | Direct provider-state fixtures validate local-only intent state without prompt, provider, model, network, or memory activation. | H1 must compare state fields, copy labels, fail-closed blockers, and approval boundaries against the accepted plan. | LV1 must use static proof or live proof based on whether H1 classifies a meaningful visible consent path. | UTS is required only if visible controls exist; otherwise waiver must cite hidden/status-only proof. | Provider execution remains blocked and outside current release gating | Accepted / USER-approved Workstream | Branch plan and provider state |
| FAM007-CUX-002 | User-operated controls/status surface | Created | Implemented a status/telemetry-first local consent UX posture with no extra interface bundle and no provider action. | Renderer/status key validation and source inspection prove safe hidden-by-default consent UX labels. | H1 must review visual/copy integrity, surface count, interface boundary, and absence of false AI readiness. | LV1 must exercise the live client if H1 finds visible controls, or record waiver for status-only proof. | USER checklist applies only if visible controls exist; hidden/status-only proof can be waived with source-truth basis. | Multiple surfaces need approval and remain outside current release gating | Accepted / USER-approved Workstream | Branch plan and UI files |
| FAM007-CUX-003 | Durable consent handoff | Touched | Implemented durable consent truth handoff through released PR #203 local persistence semantics without schema overreach. | Deterministic fixtures prove durable handoff remains local-only, no-secrets, provider-payload-excluded, and fail-closed. | H1 must compare durable-state use against released PR #203 persistence semantics and reject stale/static marker proof. | LV1 must prove visible or hidden status derives from durable consent truth without enabling provider behavior. | UTS covers the displayed durable-state result if visible; otherwise waiver must cite hidden/status-only proof. | Schema expansion beyond UX handoff is deferred and outside current release gating | Accepted / USER-approved Workstream | desktop/ai_provider_state.py |
| FAM007-CUX-004 | Revocation/reset UX mapping | Created | Implemented revocation and reset posture as explicit local labels and fail-closed write posture. | Fixtures validate reset/revoked labels, fail-closed reason codes, and no provider-side or network side effects. | H1 must review fail-closed behavior, copy clarity, and preservation of setup/execution separation after reset or revocation. | LV1 must interact with controls if present, or prove status labels through static/hidden telemetry. | USER checklist applies only if reset/revocation controls are visible. | Provider-side effects are future and outside current release gating | Accepted / USER-approved Workstream | Branch plan and validators |
| FAM007-CUX-005 | Setup vs execution consent copy | Created | Implemented separate setup and execution consent display state, labels, blockers, and future handoff gates. | Direct fixtures assert setup consent alone never grants execution consent, prompt acceptance, provider visibility, or model readiness. | H1 must audit all copy and state derivation for setup/execution conflation or readiness overclaim. | LV1 must show or validate separate setup and execution consent posture in the accepted surface. | USER acceptance must confirm distinction only where copy appears visibly. | Execution remains disabled and outside current release gating | Accepted / USER-approved Workstream | Branch plan, provider state, UI |
| FAM007-CUX-006 | Core/Desktop/ORIN status proof | Created | Implemented safe local labels/telemetry and preserved desktop readiness display suppression continuity. | Validator checks Core/Desktop/ORIN status keys, hidden status rows, and absence of long AI-owned readiness display drift. | H1 must compare renderer/status changes against display-suppression and provider-boundary requirements. | LV1 must include screenshot/live proof for visible status or explicit hidden-telemetry waiver. | UTS is required only if status becomes meaningfully visible. | Readiness display remains suppressed unless approved and outside current release gating | Accepted / USER-approved Workstream | Renderer/status surfaces |
| FAM007-CUX-007 | Provider boundary blockers | Touched | Preserved blockers for provider-visible data, prompt acceptance, model execution, downloads, network, memory, and voice/Core. | AI provider state validation proves providerVisibleData none, sentToProvider false, canAcceptPrompts false, and disabled execution paths. | H1 must audit provider-boundary assertions across state, UI copy, validators, and source truth. | LV1 must prove no provider/model/network/memory/voice path activates through the consent UX. | USER sees no functional AI claim and no consent wording that implies provider execution or model availability. | Provider setup/execution future-gated and outside current release gating | Accepted / USER-approved Workstream | Provider-state validator |
| FAM007-CUX-008 | Validator fixtures | Created | Added deterministic fixtures for every implemented UX state, consent action, blocker, and display-suppression behavior. | Direct validator output proves default, blocked, setup-only, execution-only, both-present, revoked, reset, expired, intent, invalid-intent, renderer, and boundary cases. | H1 must review coverage against every implemented seam and require repair for missing direct assertions. | LV1 uses validators as supporting proof while visible UX still requires live/user-facing evidence when present. | Validator proof supports but does not replace USER acceptance for visible consent UX behavior. | Helpers cannot bypass live proof and do not release-gate future provider behavior | Accepted / USER-approved Workstream | dev/orin_ai_provider_state_validation.py |
| FAM007-CUX-009 | Functional-AI / v1.8.0 criteria | Future | Record criteria only | Source-truth proof | H1 overclaim audit | LV1 wording audit | Future USER decision | v1.8.0 execution remains future-gated and outside current release gating | Deferred / needs USER decision | Branch record and plan |

## Branch Change Intent Ledger

Branch Change Intent Ledger Status: `No rebaseline overlap entries required at Stage 2 setup. Pre-rebaseline audit reported Rebaseline Overlap Files: None before the new branch was created from origin/main@f072be65fc5f00202a684a20b3cbb4611536ab51.`

### Changed Surface: No Rebaseline Overlap Files

- Surface Class: `governance/source-truth`
- Change Intent: `Record that Stage 2 branch creation had no overlapping incoming/current changed files while preserving the approved FAM-007 branch-local setup plan.`
- Why This File Was Touched: `The active Branch Runtime Engineering Plan must own overlap-intent evidence or an explicit no-overlap receipt before future rebaseline mutation.`
- Owned Behavior / Fact Class: `Pre-rebaseline audit receipt and branch-local planning authority.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO`
- Overlap Risk: `None`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `If future origin/main changes create overlap, rerun the audit and add real per-file Branch Change Intent Ledger entries before reconciliation.`
- Rebaseline Handling: `No overlap entries are needed for the initial Stage 2 setup; future rebaseline must treat non-empty overlap as blocking until repaired or waived.`
- Validation Proof: `Required validation: python dev\orin_worktree_rebaseline_audit.py --target-ref origin/main --cwd "C:\Nexus Worktrees\FAM-007" --branch-plan-path Docs\branch_plans\feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
- Fallback Evidence: `The pre-rebaseline audit reported Rebaseline Overlap Files: None before branch creation from current origin/main.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 setup for this exact FAM-007 carrier; no overlap waiver was needed.`
- Fold-Down Target: `Stage 2 closeout packet and PR Readiness branch-plan fold-down.`
- File path: `None`
- Overlap source: `Pre-rebaseline audit reported Rebaseline Overlap Files: None.`
- Resolution owner: `Current Branch`
- FAM-007 preservation intent: `Preserve branch-local authority, planning, Product Definition Plan, Runtime Branch Engineering Contract, Branch Runtime Engineering Plan, Element-to-Phase Proof Matrix, and provider-boundary pending decisions.`
- Validation command coverage: `python dev\orin_worktree_rebaseline_audit.py --target-ref origin/main --cwd "C:\Nexus Worktrees\FAM-007" --branch-plan-path Docs\branch_plans\feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`

## Formal Next Legal Phase Digest

Current Phase: `PR Readiness`
Next Legal Phase: `PR Readiness`
Next Active Seam: `PR Readiness Stage 2 / PR creation for FAM-007 Local AI Provider User-Operated Consent UX Foundation`
Why This Phase Is Next: `Workstream Green, H1 Green, LV1 Green, and PR Readiness Stage 1 repair are recorded; LV1 waived User Test Summary on source-truth-supported hidden/status-only proof, and Stage 1 recorded selected-next defer / USER waiver truth plus pre-PR live-state truth. PR Readiness Stage 2 must now create and validate the live PR only after USER approval.`
Approval Required: `USER approval is required for PR Readiness Stage 2 / PR creation.`
Historical USER Approval Text Receipt: `I approve PR Readiness Stage 2 / PR creation for feature/fam-007-local-ai-provider-user-operated-consent-ux-foundation in C:\Nexus Worktrees\FAM-007 from origin/main@63cf3ff45f238ef47836972e9e6ed54f2a49ede1. Scope: verify Stage 1 source-truth repair, confirm no open PR exists or reconcile existing PR truth if one exists, create the PR targeting main, validate live PR state, mergeability, checks, review/comment state, watcher provisioning/runtime proof, provider-boundary preservation, and PR body scope; commit/push only bounded PR metadata if required by source truth. Do not merge, release, tag, create artifacts, clean branches/worktrees, mutate sibling worktrees, implement provider setup completion, SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.`
Allowed Scope: `PR Readiness Stage 2 / PR creation, live PR validation, watcher provisioning/runtime proof, and bounded PR metadata repair only if required for Stage 2 eligibility.`
Explicit Exclusions: `No PR creation, merge, release, tag, artifact work, cleanup, sibling mutation, provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.`
Validation Required: `Identity/freshness checks, open PR check, branch governance, worktree confinement gate, release-readiness health gate, PR-readiness gate if applicable, governance efficiency, release body, source-owner marker validation, branch-readiness planning fixtures, AI provider state validation, runtime-fam007 validation suite, rebaseline audit, monitoring HUD validators, diff checks, compileall, and any PR Readiness validators required by source truth.`
Stop Conditions: `Stop if origin/main advances and reconciliation is required, source truth points to another carrier, selected-next/defer or pre-PR live-state truth is missing and cannot be repaired in Stage 1, LV1 waiver posture is unsupported, provider-boundary assertions weaken, validation fails, a direct FAM-006/Governance/Compact-AI sequencing blocker appears, or PR readiness would require any pending USER decision.`
USER Plan Review Gate: `Completed through Workstream Entry and validated through H1/LV1; PR Readiness Stage 1 source-truth repair is complete, and Stage 2 PR creation remains USER-gated.`
USER Inspection Files: `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md; Docs/branch_plans/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md; Docs/worktree_slots.md; Docs/family_visions/FAM-007_local_ai_and_capability_packs.md; desktop/ai_provider_state.py; desktop/core_visualization_renderer.py; desktop/desktop_renderer.py; dev/orin_ai_provider_state_validation.py.`
Review Required Because: `The branch is runtime-adjacent, source-truth-bearing, and near PR handoff; USER must see PR eligibility, overlap, selected-next/defer, LV1 waiver, and validation posture before PR creation.`
Implementation Blocker: `None - Workstream, H1, LV1, and PR Readiness Stage 1 repair are green; PR creation remains unauthorized until Stage 2.`
Review Waiver Reason: `No PR Readiness Stage 1 review waiver is active. LV1 User Test Summary is waived because the implemented consent UX surface remains hidden/status-only and no meaningful manual user path exists.`
