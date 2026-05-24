# Branch Runtime Engineering Plan: FAM-007 Local AI Provider User-Operated Consent UX Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-user-operated-consent-ux-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider User-Operated Consent UX Foundation - Branch Runtime Engineering Plan v1`
Owning Branch: `feature/fam-007-local-ai-provider-user-operated-consent-ux-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-007`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
Current Phase: `Branch Readiness`
Branch Runtime Engineering Plan: Required and present for the FAM-007 user-operated consent UX foundation runtime carrier.
Engineering Plan Status: Present - created during Branch Readiness Stage 2 and ready for Workstream Entry whole-package analysis and USER plan review.
Current Runtime Baseline: `origin/main@f072be65fc5f00202a684a20b3cbb4611536ab51` after PR #203 released durable local consent persistence in `v1.7.17-prebeta`, with provider-state, durable consent schema/state, Core/Desktop status, desktop UI, and validation surfaces still local-only and provider/model execution disabled.
Branch Purpose: Admit the next FAM-007 successor that turns durable local consent persistence into USER-reviewable user-operated consent UX/status planning before provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, or functional AI.
Planned Runtime Delta: Future USER-approved Workstream may add local user-operated consent UX state, local controls/status, durable consent handoff, revocation/reset UX mapping, setup/execution consent labels, Core/Desktop/ORIN status proof, validator fixtures, and LV1/UTS proof posture.
User-Facing Delta: The planned branch is expected to create or refine a user-facing consent control/status surface. Copy must say this is local consent preparation and must not imply provider setup completion, prompt acceptance, provider/model execution, network/download readiness, memory activity, or functional AI.
Source-Truth Delta: Stage 2 records the branch authority, v1.7.17 post-release canon closure, PR #203 released evidence, Product Definition Plan, Runtime Branch Engineering Contract, Branch Vision Snapshot / USER plan review gate, Element-to-Phase Proof Matrix, Workstream admission, and compact pointer updates.
State / Config / Schema Delta: Potential Workstream fields include local consent UX intent state, setup consent display state, execution consent display state, revocation/reset action posture, durable consent reference, local-only audit/provenance labels, provider-boundary blockers, and future setup handoff markers.
Validator / Helper Delta: Future Workstream should extend FAM-007 provider-state and UI/status validation to cover every implemented consent UX behavior, durable handoff, setup/execution separation, provider-boundary preservation, display-suppression continuity, and LV1/UTS route.
Expected Changed Files / Surfaces: Stage 2 source-truth files include this plan, the branch record, branch records index, backlog, roadmap, worktree slots, plan retirement index if needed, and generated docs inventory surfaces if validation requires regeneration. Future Workstream surfaces may include desktop/ai_provider_state.py, desktop/core_visualization_renderer.py, desktop/desktop_renderer.py, nexus_visual/orin_core files if admitted, and dev/orin_ai_provider_state_validation.py.
Workstream / Seam Map: Seam 1 -> Consent UX State And Intent Contract; Seam 2 -> User-Operated Consent Controls And Local UX Boundary; Seam 3 -> Durable Consent Handoff And Revocation / Reset UX Mapping; Seam 4 -> Core/Desktop/ORIN Visible Or Hidden Status Proof And Display-Suppression Continuity; Seam 5 -> Provider Setup / Execution Gate Alignment From User Consent UX; Seam 6 -> Validator Fixtures, Live Validation Strategy, And Functional-AI / v1.8.0 Continuation Criteria.
Per-Seam Implementation Checklist: Each seam must name implementation files, state/schema changes, visible copy changes, durable-consent handoff behavior, no-provider/no-network/no-memory boundaries, validator changes, UI proof, and stop conditions before coding begins.
Per-Seam Validation Checklist: Run diff checks, branch governance, worktree confinement gate, release-readiness health gate, governance efficiency, release body, source-owner marker validation, branch-readiness planning fixtures, AI provider state validation, runtime-fam007 validation suite, rebaseline audit, compileall, and any seam-specific consent UX fixtures.
Per-Seam User-Facing Proof Checklist: If the seam changes visible UI, prove copy and layout through source inspection plus screenshots/live-client proof as required. If a seam remains hidden/status-only, record the waiver basis and prove no user-facing overclaim.
Future-Gated Items: `Future-gated and pending USER approval: provider setup completion, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, release execution, issue work, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.`
Approval-Boundary Audit: Stage 2 authorizes planning and source-truth setup only. Workstream Entry and implementation require later USER approval; provider/model/network/memory/voice/shortcut/release/cleanup/sibling mutation remains blocked.
FAM / Shared-Surface Overlap Forecast: FAM-006 is a separate sibling lane and overlap context only; Governance PR #204 is in baseline; Compact-AI is protected historical work. None is successor authority for this FAM-007 branch.
Open Questions: Which visible surface carries consent controls, whether controls write durable consent directly or stage intent, exact setup/execution consent copy, revocation/reset UX wording, and LV1/UTS route.
USER Planning Decisions: USER approved Branch Readiness Stage 2 setup. USER has not approved Workstream Entry, Workstream implementation, H1, LV1, PR creation, merge, release, provider setup completion, SDK/model execution, downloads/network, memory, voice/Core sync, shortcuts/installers, cleanup, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.
Plan Revision History: v1 created during Branch Readiness Stage 2 from origin/main@f072be65fc5f00202a684a20b3cbb4611536ab51 after v1.7.17-prebeta and Governance PR #204.
Plan-To-Implementation Traceability Table: Pending Workstream Entry. Planned UX state maps to provider-state/UI implementation; controls map to selected user-facing surface; durable handoff maps to existing durable consent persistence; revocation/reset maps to fail-closed UX proof; setup/execution labels map to provider-boundary blockers; validators map to AI provider state and UI/status proof; LV1 maps to UTS/live-client or waiver path.
Hardening Comparison Checklist: H1 must compare implementation against this plan, Product Definition Plan, Runtime Branch Engineering Contract, Branch Vision Snapshot, Element-to-Phase Proof Matrix, UI copy, provider-boundary preservation, validators, display-suppression continuity, and source-truth fold-down.
Live Validation Proof Or Waiver Checklist: LV1 must classify the implemented surface, prove user-facing UX if present, run Codex Live Client Self-QA when applicable, record User Test Summary PASS or WAIVED, preserve provider-visible data none, and keep provider/model/network/memory/voice execution blocked.
PR Readiness Fold-Down / Retention Checklist: PR Readiness must project merge-stable branch authority, release-window posture, selected-next/defer truth, live PR/watcher state separation, branch cleanup plan, and source-truth retention/retirement decisions.
Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as local user-operated consent UX foundation only and exclude provider setup completion, SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.
USER Planning Review: Pending Workstream Entry. Stage 2 closeout must tell USER this plan is the next review object and can be accepted, revised, waived, or rejected before implementation.
PR Fold-Down Packet: Pending.
Runtime Implementation Approval: Pending USER decision.

## Branch Vision Contract Snapshot

Branch Vision Snapshot Status: Prepared for USER review during Workstream Entry.
Project-Wide Vision Alignment: Nexus should remain local-first, user-controlled, and honest about disabled provider behavior before model execution.
Family Vision Alignment: FAM-007 requires explicit provider-visible data, privacy, network/download, memory, and consent boundaries before runtime execution.
Branch-Specific Vision Alignment: User-operated consent UX should expose durable consent truth and controls without implying provider setup, prompt acceptance, provider/model execution, or functional AI.
Open Vision Questions: Exact surface, copy tone, direct-write versus staged consent intent, revocation/reset behavior, LV1 path, and screenshot/UTS checklist.
USER Vision Green: Pending Workstream Entry.
Accepted Implementation Scope: Pending Workstream Entry.
Accepted Seam Map: Pending Workstream Entry.
Accepted Stop Conditions: Pending Workstream Entry.

## Product Definition Plan

Product Vision: FAM-007 should become useful local AI through explicit user control over setup, consent, provider-visible data, and execution before any model is allowed to run.
User-Facing Goal: Make consent readiness understandable and operable by the user while keeping provider setup and execution disabled.
Project-Wide Vision Alignment: This branch supports the Nexus-wide local-first assistant vision by making AI consent boundaries visible before AI behavior exists.
Branch-Specific Vision Alignment: This branch owns user-operated consent UX foundation only and does not admit provider setup completion or model execution.
USER Vision Questions: Which surface, which copy, which write behavior, which revocation/reset path, and which LV1 user checklist should be accepted?
USER Vision Question Packet: Required at Workstream Entry because this branch is user-facing.
Codex Product Interpretation: Consent UX is the bridge between durable local consent persistence and later provider setup. It must be small, clear, reversible, and local-only.
Codex Implementation Recommendation: Build consent UX/status foundation before provider setup completion.
Codex Additional Recommendations: Keep the first UX modest, use separate setup/execution labels, make reset/revocation obvious, and avoid any functional-AI copy.
USER/ChatGPT Review Checkpoint: USER review is required before implementation.
USER Critique Loop: USER may accept, revise, reject, defer, or waive the plan during Workstream Entry.
USER Decision Ledger: Stage 2 setup approved; all implementation and later phases pending.
Deferred Ideas / Future Package Ledger: Provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, AI Product Contract import, Private Dev ORIN import, v1.8.0 execution.
Planning Adequacy Review: Complete for Stage 2 setup; pending Workstream Entry whole-package analysis.
Rejected Shallow Plan: A single consent button or copy-only label is rejected as insufficient without durable handoff, separation, blockers, proof, and LV1 strategy.
Alternatives And Tradeoffs Reviewed: Provider setup completion now is rejected as premature; SDK/model execution is rejected as out of scope; FAM-006 routing is rejected as sibling drift.
Whole-System Interaction Map: UI consent state reads durable local consent truth, presents safe labels/controls, records only local intent if admitted, feeds status proof, and leaves provider/model/network/memory/voice paths blocked.
Open Questions / USER Decision Points: Surface selection, copy, write posture, revocation/reset semantics, LV1 proof, UTS checklist.
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
Acceptance Criteria: Stage 2 source truth, validation, commit, and push; later Workstream proof for all admitted seams.
Screenshot / Live / User Test Summary Proof Requirements: Expected for visible UX unless explicitly waived later.
Implementation Sequence Proposal: Workstream Entry, seams 1 through 6, H1, LV1, PR Readiness.
Planning Blockers: Workstream Entry and USER plan review pending.
USER Decisions Needed: Workstream Entry approval is next.

## Interface Release Boundary

Primary Interface Release Surface: User-operated local consent UX/status surface to be selected during Workstream Entry.
Interface Bundle User Approval: Pending; one primary interface is assumed.
Fallback Point: Safe status-only local consent copy with explicit USER waiver if controls are not admitted.
Interface Acceptance / Proof Path: Workstream Entry must define screenshots, live-client proof, UTS, and validator expectations.

## Runtime Branch Engineering Contract

USER Engineering Planning Review: Required - pending Workstream Entry USER review.
Engineering Contract Status: Proposed.
Runtime Implementation Approval: Pending USER decision.
Branch Purpose: Admit and plan the FAM-007 user-operated local consent UX foundation after durable consent persistence and before provider setup completion.
Current Runtime Baseline: Durable consent persistence released in v1.7.17-prebeta; provider/model execution remains disabled.
Planned Runtime Delta: Local user-operated consent UX/status foundation over durable consent truth.
User-Facing Runtime Delta: Visible local consent controls/status if admitted.
State / Config / Schema Delta: Local UX intent/status fields and display labels only if Workstream admits them.
Validator / Helper Delta: Extend provider/UI validators for implemented behavior.
Expected Changed Files / Surfaces: Source truth, provider state, renderers/UI, validators, LV1/UTS proof.
Approval-Boundary Audit: Stage 2 setup only; all implementation and future AI/provider work pending.
Future-Gated Items: Provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, release, cleanup, AI Product Contract, Private Dev ORIN, v1.8.0.
Workstream Seam Map: Six seam families listed in the Branch Runtime Engineering Plan.
Proof Expectations: Direct validators, UI/status proof, provider-boundary preservation, LV1/UTS route.
Risk Forecast: High user-facing/provider-boundary risk.
Recommendations And Alternatives: Preferred consent UX foundation now; narrower status-only branch if USER rejects controls; setup completion later.
Plan Version / Revision Status: v1 active.
Plan-To-Implementation Traceability: Pending Workstream Entry and seam updates.

## Workstream Admission

Workstream Label: `FAM-007 Local AI Provider User-Operated Consent UX Foundation`
Admission State: `Admitted for Workstream Entry; implementation pending USER approval`
Package Completion State: `Not started`
Bounded Seam Default: `One active seam at a time; bounded does not mean one-seam Workstream. Continue through admitted seams until Workstream Green, named blocker, or explicit USER waiver.`
Single-Seam Or Single-Slice Waiver Authority: `USER only`
Stop Basis: `Branch Readiness Stage 2 setup complete`

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

Matrix Status: `Present - pending USER review during Workstream Entry`
USER Review Status: `Pending`
Open Element Questions: `Queued - exact visible surface, copy, write behavior, revocation/reset posture, and LV1 path require Workstream Entry USER review`
Element Coverage Owner: `Docs/branch_plans/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`
Element Validation Ledger Owner: `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md`

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAM007-CUX-001 | Consent UX state and local intent model | Planned | Workstream must define local UX intent fields, setup/execution labels, blocked states, and fail-closed defaults before code changes. | Proof must inspect provider-state payloads and validate local-only intent state without prompt, provider, model, network, or memory activation. | H1 must compare state fields, copy labels, fail-closed blockers, and approval boundaries against the accepted plan. | LV1 must use static proof or live proof based on whether the accepted seam creates a visible consent path. | UTS is required when visible controls exist and must cover setup/execution consent state, blockers, and reset/revocation clarity. | Provider execution remains blocked and outside current release gating | Proposed / needs USER decision | Branch plan and provider state |
| FAM007-CUX-002 | User-operated controls/status surface | Planned | Workstream must implement only the USER-accepted primary surface or a status-only fallback with no extra interface bundle. | Proof must include screenshot or live-client evidence plus copy validation for each admitted visible control or status state. | H1 must review visual/copy integrity, surface count, interface boundary, and absence of false AI readiness. | LV1 must exercise the live client when controls are visible, or record a precise waiver for status-only proof. | USER checklist must verify visible controls, local-only status, blocked provider behavior, and no functional-AI claim. | Multiple surfaces need approval and are outside current release gating unless accepted | Proposed / needs USER decision | Branch plan and UI files |
| FAM007-CUX-003 | Durable consent handoff | Planned | Workstream must read or reference durable consent truth through the existing local persistence boundary without schema overreach. | Proof must use deterministic fixtures showing durable handoff remains local-only, no-secrets, provider-payload-excluded, and fail-closed. | H1 must compare durable-state use against released PR #203 persistence semantics and reject stale/static marker proof. | LV1 must prove the visible or hidden status derives from durable consent truth without enabling provider behavior. | UTS covers the displayed durable-state result if visible, otherwise the waiver must cite hidden/status-only proof. | Schema expansion beyond UX handoff is deferred and outside current release gating | Proposed / needs USER decision | desktop/ai_provider_state.py |
| FAM007-CUX-004 | Revocation/reset UX mapping | Planned | Workstream must map revocation and reset posture to explicit local labels or controls if the surface admits them. | Proof must validate reset/revoked labels, fail-closed reason codes, and no provider-side or network side effects. | H1 must review fail-closed behavior, copy clarity, and preservation of setup/execution separation after reset or revocation. | LV1 must interact with reset/revocation controls if present, or prove status labels through static/hidden telemetry. | USER checklist must confirm reset/revocation copy is understandable and does not imply external provider action. | Provider-side effects are future and outside current release gating | Proposed / needs USER decision | Branch plan and validators |
| FAM007-CUX-005 | Setup vs execution consent copy | Planned | Workstream must keep setup consent and execution consent separate in state, copy, blockers, and future handoff criteria. | Proof must assert setup consent alone never grants execution consent, prompt acceptance, provider visibility, or model readiness. | H1 must audit all copy and state derivation for setup/execution conflation or readiness overclaim. | LV1 must show or validate separate setup and execution consent posture in the accepted surface. | USER acceptance must confirm setup and execution consent are visibly distinct where user-facing copy appears. | Execution remains disabled and outside current release gating | Proposed / needs USER decision | Branch plan, provider state, UI |
| FAM007-CUX-006 | Core/Desktop/ORIN status proof | Planned | Workstream must expose only safe local labels or telemetry and preserve desktop readiness display suppression continuity. | Proof must validate Core/Desktop/ORIN status keys, visible copy if any, and absence of long AI-owned readiness display drift. | H1 must compare renderer/status changes against display-suppression and provider-boundary requirements. | LV1 must include screenshot/live proof for visible status or an explicit hidden-telemetry waiver. | UTS is required if status becomes visible and must verify no AI-ready or provider-ready overclaim. | Readiness display remains suppressed unless approved and outside current release gating | Proposed / needs USER decision | Renderer/status surfaces |
| FAM007-CUX-007 | Provider boundary blockers | Planned | Workstream must preserve blockers for provider-visible data, prompt acceptance, model execution, downloads, network, memory, and voice/Core. | Proof must run AI provider state validation showing providerVisibleData none, sentToProvider false, and canAcceptPrompts false. | H1 must audit provider-boundary assertions across state, UI copy, validators, and source truth. | LV1 must prove no provider/model/network/memory/voice path activates through the consent UX. | USER sees no functional AI claim and no consent wording that implies provider execution or model availability. | Provider setup/execution future-gated and outside current release gating | Proposed / needs USER decision | Provider-state validator |
| FAM007-CUX-008 | Validator fixtures | Planned | Workstream must add deterministic fixtures for every implemented UX state, consent action, blocker, and display-suppression behavior. | Proof must include direct validator output and fixture cases tied to each implemented behavior, not marker-only assertions. | H1 must review coverage against every implemented seam and require repair for missing direct assertions. | LV1 uses validators as supporting proof while visible UX still requires live/user-facing evidence when present. | Validator proof supports but does not replace USER acceptance for visible consent UX behavior. | Helpers cannot bypass live proof and do not release-gate future provider behavior | Proposed / needs USER decision | dev/orin_ai_provider_state_validation.py |
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

Current Phase: `Branch Readiness`
Next Legal Phase: `Workstream Entry`
Next Active Seam: `Workstream Entry whole-package analysis and USER plan review for FAM-007 Local AI Provider User-Operated Consent UX Foundation`
Why This Phase Is Next: `Stage 2 creates branch authority and planning truth; implementation remains blocked until USER reviews the plan and approves the Workstream path.`
Approval Required: `USER approval is required for Workstream Entry analysis.`
Exact USER Approval Text: `I approve Workstream Entry analysis for feature/fam-007-local-ai-provider-user-operated-consent-ux-foundation in C:\Nexus Worktrees\FAM-007 from origin/main@f072be65fc5f00202a684a20b3cbb4611536ab51. Scope: inspect the active branch record, Branch Runtime Engineering Plan, Product Definition Plan, Runtime Branch Engineering Contract, Branch Vision Snapshot, Element-to-Phase Proof Matrix, USER plan review requirements, prior PR #203 durable consent persistence evidence, provider-boundary posture, validation expectations, UI/status proof expectations, LV1/UTS planning, FAM-006/Governance overlap context, and return the exact bounded Workstream implementation decision text. Do not implement runtime/UI changes, commit, push, create a PR, merge, release, clean branches/worktrees, mutate sibling worktrees, implement provider setup completion, SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.`
Allowed Scope: `Workstream Entry analysis and USER review bundle preparation if required.`
Explicit Exclusions: `No implementation, PR creation, merge, release, cleanup, sibling mutation, provider setup completion, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcuts/installers, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.`
Validation Required: `Identity/freshness checks, branch governance, worktree confinement, planning fixture, AI provider state, runtime-fam007 as applicable, rebaseline audit, diff checks, and any Workstream Entry validators required by source truth.`
Stop Conditions: `Stop if origin/main advances and reconciliation is required, planning gaps remain, USER plan review is missing, validation fails, source truth points to another carrier, or implementation would require pending USER decisions.`
USER Plan Review Gate: `USER may accept, revise, waive, or reject this Stage 2 plan during Workstream Entry before implementation begins.`
USER Inspection Files: `Docs/branch_records/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md; Docs/branch_plans/feature_fam_007_local_ai_provider_user_operated_consent_ux_foundation.md; Docs/feature_backlog.md; Docs/prebeta_roadmap.md; Docs/worktree_slots.md; Docs/family_visions/FAM-007_local_ai_and_capability_packs.md; desktop/ai_provider_state.py; desktop/core_visualization_renderer.py; desktop/desktop_renderer.py; dev/orin_ai_provider_state_validation.py.`
Review Required Because: `This branch is user-facing/runtime-adjacent and must prove vision, interface boundary, element matrix, durable consent handoff, provider-boundary preservation, and LV1/UTS posture before implementation.`
Implementation Blocker: `WORKSTREAM_ENTRY_USER_APPROVAL_MISSING`
Review Waiver Reason: `Not waived.`
