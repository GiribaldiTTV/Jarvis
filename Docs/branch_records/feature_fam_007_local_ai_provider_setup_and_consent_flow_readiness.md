# Branch Record: feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness

## Record State

Record State: `Active Workstream implementation complete`

## Status

Status: `Workstream Green - local-only setup and consent flow readiness contracts, display suppression proof, validator coverage, and source truth recorded; Hardening H1 pending USER approval`

## Branch Identity

- Branch: `feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness`
- Worktree: `C:\Nexus Worktrees\FAM-007`
- Family: `FAM-007`
- Package: `PKG-007`
- Workstream Label: `FAM-007 Local AI Provider Setup and Consent Flow Readiness`
- Branch Source: `origin/main` at `2bd54f0e34c6759e9618f42d104d80b975ecc1c3`

## Canonical Branch

Canonical Branch: `feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness`

## Current Phase

Phase: `Workstream`

Stage: `FAM-007 Local AI Provider Setup and Consent Flow Readiness implementation`

Seam: `Bounded multi-seam Workstream complete`

## Phase Status

Active Branch: `feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness`

Branch Authority State: `Active Branch - fresh FAM-007 runtime carrier created from origin/main after v1.7.8-prebeta release execution`

Authority Marker: `Active Branch`

Fresh Branch Authority: `Active - source truth, Product Definition Plan, Runtime Branch Engineering Contract, Branch Runtime Engineering Plan, and bounded Workstream planning are recorded for this carrier.`

Implementation Entry: `Complete - USER-approved bounded Workstream implementation is recorded and ready for Hardening H1 review.`

Desktop Display Revision: `Implemented - the long AI-owned readiness display is hidden/suppressed by default on Core/Desktop ORIN surfaces while provider state remains available as telemetry.`

## Branch Class

`implementation`

## Branch Scope

This branch is the USER-approved fresh FAM-007 runtime carrier created from current `origin/main` after `v1.7.8-prebeta` was published. It closes release-dependent source-truth drift from the `v1.7.8-prebeta` release window, records fresh FAM-007 branch authority, records the Product Definition Plan, Runtime Branch Engineering Contract, and Branch Runtime Engineering Plan for the next bounded FAM-007 layer, and admits the planning basis for the FAM-007 Local AI Provider Setup and Consent Flow Readiness Workstream.

Provider Setup and Consent Flow Readiness means contracts, setup flow eligibility state, consent flow requirement posture, setup blocker state, provider selection/config confirmation posture, UI posture, proof expectations, and validation planning for a future provider setup path. This setup does not enable provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external provider/API calls, memory/indexing, learning, persistence, personalization, voice/Core runtime sync, shortcut/installer work, release execution, issue work, FAM-006 mutation, Governance mutation, branch cleanup, AI Product Contract import, Private Dev ORIN import, or the `v1.8.0-prebeta` release.

## Worktree Identity

Expected Worktree Root: `C:\Nexus Worktrees\FAM-007`

Actual Worktree Root: `C:\Nexus Worktrees\FAM-007`

No Cross-Worktree Mutation: `Required - this branch may inspect FAM-006 and Governance overlap but must not mutate those worktrees without separate USER approval.`

GitHub Desktop-bound worktree: `No - this branch is a Codex-managed FAM-007 worktree with normal Git remote tracking.`

## Branch Readiness Stage 2 Authority

Branch Readiness Stage 2 USER Approval: `Granted - USER approved creating feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness from current origin/main 2bd54f0e34c6759e9618f42d104d80b975ecc1c3, carrying v1.7.8-prebeta post-release canon closure into Stage 2 setup, recording fresh FAM-007 branch authority, Product Definition Plan fields, Runtime Branch Engineering Contract fields, Branch Runtime Engineering Plan fields, bounded Provider Setup and Consent Flow Readiness Workstream planning, v1.8.0-prebeta direction, validation, commit, and push.`

Branch Readiness Revision: `Accepted - USER specifically required this branch to include validation that the visible desktop AI-owned readiness display is removed because the previous branch did not solve that issue.`

Runtime Workstream Implementation Approval: `Granted for the bounded local-only setup and consent flow readiness Workstream only.`

Current Workstream State: `Green - setup flow readiness, consent flow readiness, provider handoff/approval gates, desktop display suppression, UI posture, validator fixtures, and source-truth proof complete`

Current Hardening State: `Pending - H1 begins after USER approval`

Current Live Validation State: `Pending - LV1 begins only after H1 is green and USER approves LV1`

## Blockers

- `Provider setup implementation pending USER approval`
- `Consent collection implementation pending USER approval`
- `Provider SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer, release, PR, merge, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution remain pending USER decisions`

## Entry Basis

USER approved Branch Readiness Stage 2 for the fresh FAM-007 runtime branch after `v1.7.8-prebeta` release execution. Stage 1 identified `v1.7.8-prebeta` post-release canon closure drift, recommended FAM-007 as the next runtime carrier because PKG-007 remains admitted and package-incomplete, selected `feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness`, and USER added the revision that this branch must validate removal of the desktop AI-owned readiness display.

## Exit Criteria

- `v1.7.8-prebeta` is recorded as the latest public prerelease.
- Release commit `2bd54f0e34c6759e9618f42d104d80b975ecc1c3` is recorded.
- PR #173, PR #174, PR #175, PR #176, PR #177, and PR #178 are recorded as released in `v1.7.8-prebeta`.
- `feature/fam-007-local-ai-provider-path-and-consent-readiness` is recorded as released historical FAM-007 evidence.
- Fresh FAM-007 branch authority is recorded for `feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness`.
- Product Definition Plan fields are complete.
- Runtime Branch Engineering Contract fields are complete.
- Branch Runtime Engineering Plan fields are complete and point to `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md`.
- The bounded Workstream plan includes provider setup flow readiness, consent flow readiness, compact UI posture, desktop AI-owned readiness display removal validation, v1.8.0-prebeta direction, and all pending USER approval boundaries.
- Workstream validation passes, the implementation commit is pushed, and source truth points to Hardening H1 as the next legal phase.

## Rollback Target

- `Branch Readiness`

Rollback Target: `Branch Readiness`

Rollback Commit: `origin/main 2bd54f0e34c6759e9618f42d104d80b975ecc1c3`

Rollback Rule: `If validation fails and cannot be repaired within Stage 2 setup scope, stop and report the smallest source-truth repair packet. Do not mutate runtime files, FAM-006, Governance worktrees, tags, releases, issues, provider setup paths, consent collection, provider/model execution, memory/indexing, voice/Core sync, shortcuts, installers, AI Product imports, or Private Dev ORIN imports.`

## Next Legal Phase

- `Hardening`

Next Legal Phase: `Hardening`

Next Legal Seam: `Hardening H1 for FAM-007 Local AI Provider Setup and Consent Flow Readiness`

Exact USER Decision Needed: `Approve Hardening H1 for the completed FAM-007 Local AI Provider Setup and Consent Flow Readiness Workstream.`

## Governance Drift Audit

- `v1.7.8-prebeta` is the latest public prerelease.
- Release commit is `2bd54f0e34c6759e9618f42d104d80b975ecc1c3`.
- PR #173, PR #174, PR #175, PR #176, PR #177, and PR #178 are recorded as released in `v1.7.8-prebeta`.
- `feature/fam-007-local-ai-provider-path-and-consent-readiness` is released historical PR #177 FAM-007 provider path and consent readiness evidence.
- `feature/fam-007-local-ai-provider-execution-readiness-gates` is released historical PR #172 FAM-007 execution-readiness evidence.
- `feature/fam-007-local-ai-provider-activation-foundation` is released historical PR #170 FAM-007 activation-foundation evidence.
- `feature/fam-007-local-ai-provider-runtime-readiness` is released historical PR #165 provider-readiness/setup-eligibility evidence.
- FAM-006 remains a separate dirty lane; its shared-doc and UI overlap is a later reconciliation risk, not a Stage 2 blocker under the current USER approval.

## Release Canon Closure

Latest Public Prerelease Recorded In Source Truth: `v1.7.8-prebeta`

Latest Public Release Commit: `2bd54f0e34c6759e9618f42d104d80b975ecc1c3`

Latest Public Release URL: `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.7.8-prebeta`

Released In v1.7.8-prebeta: `PR #173 Record v1.7.7 Canon Closure Drift; PR #174 Governance Reform PR 1 Worktree Slot Ownership Model; PR #175 PR Watcher Approval Default; PR #176 Consolidated Governance Efficiency Reform Model; PR #177 FAM-007 Local AI Provider Path and Consent Readiness; PR #178 Governance release-readiness repair.`

Post-Release Canon Closure Drift: `Recorded and closed by this Branch Readiness Stage 2 setup`

Published Release Pending Canon Closure: `None - v1.7.8-prebeta source truth is closed by this Branch Readiness Stage 2 setup; Stage 1 pending marker was v1.7.8-prebeta.`

Closure Repair Surface: `Next Branch Readiness Stage 2`

Closure Drift Scope: `release-dependent fields only`

Implementation Entry: `Complete for this bounded Workstream; Hardening H1 is the next legal phase.`

## Active Seam

Active seam: `Workstream Green - all admitted seam families complete`

Seam 1: `Provider Setup Flow Readiness Contract`

Goal: `Admit a bounded plan for setup flow readiness contracts, consent flow readiness, UI proof, validation expectations, and future-gated setup/execution boundaries.`

Scope: `Source-truth setup, branch authority, branch plan, product plan, runtime contract, release-canon closure, and bounded Workstream seam admission.`

Non-Includes: `Provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external calls, memory indexing, voice/Core sync, shortcut/installer work, release work, issue work, PR creation, merge, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution.`

## Branch Readiness Completion

Branch Completion Goal: `Stage 2 is complete when v1.7.8 release-canon closure, fresh branch authority, Product Definition Plan, Runtime Branch Engineering Contract, Branch Runtime Engineering Plan, branch plan file, bounded Workstream plan, desktop AI-owned readiness display validation requirement, validation results, commit, and push are recorded.`

Known Future-Dependent Blockers: `Hardening H1, LV1, PR creation, merge, provider setup implementation, consent collection implementation, provider SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, release execution, issue closeout, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution require later USER approval.`

Branch Closure Rule: `This branch remains active only through USER-approved H1, LV1, PR Readiness, PR creation, and merge decisions; after merge it must become historical branch evidence and post-merge No Active Branch or selected-next truth must be recorded by the proper phase.`

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing, backend/runtime, developer-tooling`

Docs-Only Workstream: `No`

Planning-Loop Bypass User Approval: `None`

Planning-Loop Bypass Reason: `None`

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`

Backlog-Split User Approval: `None`

Backlog-Split Reason: `None`

## Backlog Completion Strategy

Branch Completion Goal: `Complete the setup and consent flow readiness layer as a local-only FAM-007 package slice, including proof that the desktop AI-owned readiness display is removed and setup/execution remain future-gated.`

Known Future-Dependent Blockers: `Real provider setup implementation, consent collection, provider SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcuts, installers, release execution, issue work, PR creation, merge, FAM-006/Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution remain future decisions.`

Branch Closure Rule: `The branch may close only after Workstream, H1, LV1, PR Readiness, PR creation, and merge are separately approved and validated, or after USER stops the branch and records a new carrier.`

## Branch Objective

Record and later implement a local-only setup and consent flow readiness layer that prepares FAM-007 for a future provider setup path while proving that the prior long AI-owned desktop readiness display has been removed and cannot be mistaken for an always-active AI capability.

## Target End-State

The target end-state is a validated disabled/status-only branch where setup flow readiness, consent flow readiness, provider selection/config confirmation, provider-visible-data boundaries, and compact UI copy exist as scaffolding only; provider setup, consent collection, SDK/model execution, network, downloads, memory, voice/Core sync, shortcuts, installers, and functional AI remain future-gated.

## Expected Seam Families And Risk Classes

- Seam 1 Provider Setup Flow Readiness Contract: runtime state/schema risk.
- Seam 2 Setup Eligibility and Blocker Model: setup gate and blocker consistency risk.
- Seam 3 Setup and Execution Consent Flow Readiness: consent boundary and data visibility risk.
- Seam 4 Provider Selection and Config Confirmation Handoff: provider profile/config handoff risk.
- Seam 5 Core/Desktop/ORIN Setup and Consent UI Posture: user-facing copy risk and desktop AI-owned display removal proof risk.
- Seam 6 Functional-AI and v1.8.0 Continuation Criteria: release translation and future-version criteria risk.

## User Test Summary Strategy

User Test Summary Strategy: `Disabled/status-only branch posture allows LV1 static validator substitute unless USER later approves a live setup flow. LV1 must specifically prove the desktop AI-owned readiness display is absent, provider-visible data remains none, sentToProvider remains false, canAcceptPrompts remains false, setup/consent collection are unimplemented, and provider/model execution remains disabled.`

## Later-Phase Expectations

Workstream Entry produced the engineering design packet before implementation. Workstream implementation stayed bounded seam-to-seam. H1 must compare implementation against this branch record, branch plan, Product Definition Plan, and Runtime Branch Engineering Contract. LV1 must prove disabled/status-only behavior and desktop display absence. PR Readiness must fold proof into PR metadata before PR creation.

## Initial Workstream Seam Sequence

Seam 1: `Provider Setup Flow Readiness Contract`

Goal: `Define setup flow readiness state, eligibility, blockers, reason codes, provenance, schema versioning, and approval status without implementing real setup.`

Scope: `Implemented local-only state/UI/validator scaffolding for setup flow readiness plus desktop display suppression validation.`

Non-Includes: `Real provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer work, release work, issue work, PR creation, merge, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution.`

## Admitted Implementation Slice

Admitted Implementation Slice: `FAM-007 Local AI Provider Setup and Consent Flow Readiness`

Slice IDs: `SLC-017, SLC-018, SLC-031, SLC-032, SLC-033, SLC-034, SLC-035, SLC-036`

Implementation Delta Class: `runtime/user-facing, backend/runtime, developer-tooling`

Implementation Slice Scope: `Future bounded local-only setup flow readiness state, consent flow readiness state, setup blocker posture, provider selection/config confirmation, compact Core/Desktop/ORIN copy, desktop AI-owned readiness display removal validation, validator fixtures, and source-truth closeout.`

Implementation Slice Non-Includes: `Provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external calls, memory indexing/retrieval/learning/persistence/personalization, voice/Core runtime sync, shortcut/installer work, release/tag/artifact work, issue work, PR creation, merge, FAM-006 mutation, Governance mutation, branch cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta release execution.`

## Workstream Completion

Workstream Completion State: `Green - bounded multi-seam setup and consent flow readiness implementation complete; H1 pending USER approval.`

Seam Family 1 - Setup Flow Readiness Contract: `Green - desktop/ai_provider_state.py publishes setup flow readiness state, eligibility, blockers, reason codes, provenance, schema/config versioning, approval status, and future setup handoff posture.`

Seam Family 2 - Consent Flow Readiness Contract: `Green - setup and execution consent remain distinct, consent collection remains pending USER approval, consent flow readiness states/blockers/reasons/provenance/schema fields are published, and provider-visible data remains none.`

Seam Family 3 - Provider Setup Handoff And Approval Gates: `Green - provider setup handoff, provider consent handoff, provider path handoff, setup approval, execution approval, data visibility consent, audit envelope, and local-only postures are recorded as future-gated/status-only.`

Seam Family 4 - Desktop AI-Owned Readiness Display Removal/Suppression: `Green - nexus_visual/orin_core.html and nexus_visual/orin_core_desktop.html mark #ai-provider-status hidden and aria-hidden with suppression data markers; nexus_visual/orin_core.css forces the hidden/suppressed status display to none; nexus_visual/orin_core.js preserves telemetry updates while keeping the panel hidden by default.`

Seam Family 5 - Core/Desktop/ORIN Setup And Consent Status UI: `Green - Core/Desktop/ORIN provider state payloads publish setup flow, consent flow, consent collection, provider setup handoff, provider consent handoff, and display suppression telemetry while prompt/provider/model execution remains disabled.`

Seam Family 6 - Functional-AI And v1.8.0 Continuation Criteria: `Green - functional-AI and v1.8.0-prebeta criteria remain pending future USER-approved provider setup, consent collection, prompt/model execution, provider-visible-data behavior, network/external posture, validator proof, and release-readiness translation.`

Desktop AI-Owned Readiness Display Suppression Proof: `Implemented - the long always-visible AI-owned readiness display is not visible by default; #ai-provider-status remains hidden telemetry only and dev/orin_ai_provider_state_validation.py validates suppression markers, CSS suppression, JS enforced hidden state, and setup/consent flow fixture coverage.`

## Backlog Completion Status

Backlog Completion State: Implemented Complete Except Future Dependency

Remaining Implementable Work: None

Future-Dependent Blockers: Provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external provider/API calls, memory indexing/retrieval/learning/persistence/personalization, voice/Core runtime sync, shortcut/installer work, release/tag/artifact work, issue work, PR creation, merge, FAM-006 mutation, Governance mutation outside this branch path, branch cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta release execution remain pending USER decisions.

Completion Status: Green

## Seam Continuation Decision

Seam Status: Green

Slice Status: Green

Completion Status: Green

Waiver Status: None

Continue Decision: Stop

Continuation Execution Latch: Closed

Stop Basis: Workstream Green

Next Active Seam: Hardening H1

Stop Condition: Workstream green; H1 pending USER approval.

Continuation Action: Stop at phase boundary until USER admits the next phase; return Workstream closeout packet and await USER approval for Hardening H1.

Single-Seam Workstream Waiver: None

Single-Seam Or Single-Slice Waiver Authority: USER only; Codex cannot infer single-seam or single-slice authority.

Single-Seam Or Single-Slice Workstream Blocker: One seam or one slice is a blocker unless USER waiver is recorded; no one-seam or one-slice stop is being claimed.

Bounded Seam Default: Bounded means one active seam at a time; bounded is not one-seam Workstream authority, and continuation runs through all admitted seams until Workstream Green or a named blocker.

## Branch Runtime Engineering Plan

Branch Runtime Engineering Plan: `Accepted - this branch uses a detailed Branch Runtime Engineering Plan file for setup and consent flow readiness planning, and implementation must map the plan to local-only runtime, UI, validator, and source-truth proof without enabling setup or execution.`

Branch Runtime Engineering Plan Path: `Docs/branch_plans/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md`

Engineering Plan Status: `Accepted - bounded setup/consent-flow readiness Workstream is implemented and pending H1 review`

PR Fold-Down Packet: `Pending - later PR readiness must fold down branch plan, Workstream, H1, LV1, desktop display removal proof, validation, approval-boundary, and release-window evidence.`

## Product Definition Plan

Project-Wide Vision Alignment: `This branch continues the Local AI and Capability Packs vision by preparing a local-only setup and consent flow readiness layer before any provider SDK, model execution, consent collection, or network activity is approved.`

Branch-Specific Vision Alignment: `The branch converts released provider path and consent readiness into setup-flow readiness planning, with a quieter desktop posture that removes the screenshot-visible long AI-owned readiness display and replaces it with validated, compact, future-gated state if implementation is later approved.`

System Concept Model: `Nexus keeps AI provider setup as an explicit future-gated subsystem with setup flow state, consent flow state, provider selection/config confirmation, provider-visible-data boundaries, and functional-AI criteria separated from actual provider execution.`

Entity / Profile Model: `Planned entities include setup flow readiness profile, setup eligibility profile, setup blocker list, consent flow profile, setup consent status, execution consent status, provider selection confirmation, provider config confirmation, provider-visible-data consent posture, and validation proof markers.`

User Workflow Model: `A future user should see compact setup and consent readiness posture without being asked to configure a provider, grant consent, send prompts, download models, or expose data until the USER approves a later setup or execution branch.`

Scale / Data Volume Model: `The planned branch remains local-only status scaffolding with no provider traffic, no prompt payloads, no model outputs, no memory indexes, no consent records, and no external data volume growth.`

Configuration And State Model: `State planning should extend the existing provider state model with setup flow readiness, consent flow readiness, provider selection/config confirmation, blocker/reason/provenance fields, and schema markers while keeping provider-visible data none and prompt/model execution disabled.`

Expected User-Facing Outcomes: `Users should no longer see the long always-visible AI-owned readiness display on the desktop, and any visible FAM-007 status should be compact, truthful, disabled/status-only, and clear that setup, consent collection, provider execution, and functional AI are future-gated.`

Codex Additional Recommendations: `Workstream Entry should choose a narrow implementation path that first removes or suppresses the long desktop display, then adds only the minimal compact status and validator fixtures needed to prove setup and consent flow readiness remains local-only.`

USER Critique Loop: `USER critique is recorded as a hard planning revision: the previous branch did not remove the visible AI-owned readiness display, so this branch must include validation proving that desktop display is gone.`

USER Decision Ledger: `USER approved Stage 2 setup, Workstream Entry, bounded Workstream implementation, and the desktop-display validation revision. Pending decisions include Hardening H1, LV1, provider setup implementation, consent collection implementation, provider SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer work, release/tag/artifact work, issue work, PR creation, merge, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution.`

Deferred Ideas / Future Package Ledger: `Functional AI, real provider setup, actual consent collection, model execution, external provider calls, model downloads, memory/learning/personalization, voice/Core sync, shortcut/installer work, Dev ORIN import, and v1.8.0-prebeta release execution remain deferred future branches or release decisions.`

Planning Adequacy Review: `The Stage 2 plan is not shallow because it covers the whole end-to-end setup-readiness path from source truth, state/schema, UI, validators, desktop display proof, approval boundaries, and later PR/release translation while still requiring Workstream Entry before implementation.`

Rejected Shallow Plan: `A plan that simply renames provider readiness or leaves the long AI-owned desktop display visible is rejected because it would fail the USER revision and blur setup readiness with actual provider setup or execution.`

Alternatives And Tradeoffs Reviewed: `Alternative options and tradeoffs/risks reviewed: a wider setup wizard branch was rejected because consent collection and provider setup implementation are pending USER decisions; a narrower display-only repair was rejected because it would not plan setup and consent flow readiness; the preferred bounded branch carries some shared-UI risk but keeps execution disabled.`

Whole-System Interaction Map: `The branch touches FAM-007 state, Core/Desktop/ORIN copy, nexus_visual surfaces, provider-state validators, branch records, branch plans, backlog, roadmap, and validation registry if helpers change; FAM-006 and Governance are inspected for overlap but remain separate worktrees.`

Minimum Viable vs Full System Boundary: `Minimum viable scope is local-only setup and consent flow readiness contracts plus desktop display absence validation. Full provider setup, consent capture, SDK integration, model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer work, and functional AI remain outside this branch.`

Open Questions / USER Decision Points: `USER decisions remain pending for the exact UI suppression strategy, validator ownership, compact status copy, setup flow state names, consent flow state names, and whether any setup affordance remains visible before real provider setup is approved.`

Product Vision: `Prepare FAM-007 for a future provider setup and consent flow without making the desktop feel like AI is already running or owned by a provider.`

User-Facing Goal: `Users should see a calm, compact, truthful local-only setup/consent readiness posture and should not see the long AI-owned readiness display that prompted the USER revision.`

USER Vision Questions: `Workstream Entry must ask whether any compact setup status should remain visible after the long AI-owned display is removed, and what proof standard USER expects for desktop display absence.`

Codex Product Interpretation: `The product should communicate readiness as a future-gated setup contract, not as an active AI/provider capability, and it should privilege quiet UI clarity over broad readiness narration.`

Codex Implementation Recommendation: `Use the smallest later implementation that removes or suppresses the long display, adds centralized setup/consent flow state, maps compact labels from that state, and adds validators proving the display is absent.`

USER/ChatGPT Review Checkpoint: `Workstream Entry should return a design packet for USER review before implementation, and H1/LV1 should call out the desktop display proof as a named acceptance item.`

Full Feature Element Breakdown: `Elements include setup flow readiness state, setup eligibility, setup blockers, setup reason codes, consent flow readiness, setup consent status, execution consent status, provider selection/config confirmation, provider-visible-data consent posture, compact UI copy, desktop display absence proof, and validator fixtures.`

Current Branch vs Future Package Boundaries: `This branch may prepare setup and consent flow readiness only; real setup, consent capture, provider SDKs, model execution, downloads, external calls, memory, voice/Core sync, shortcuts, installers, and functional AI remain future packages or branches.`

Affected Surfaces: `Expected affected surfaces are FAM-007 source truth, branch plan, provider state model, Core/Desktop/ORIN renderers, nexus_visual Core files, provider-state validators, optional desktop UI validator, and validation registry if helper ownership changes.`

Data/Control Model: `No user prompt, provider payload, model output, consent record, memory index, external API request, download, or voice/Core command is created by Stage 2; future state remains local status/control metadata only.`

Branch Reach / Package-Size Review: `The branch is large enough because setup readiness, consent readiness, provider confirmation, UI display cleanup, validators, and release-proof boundaries interact across state, UI, docs, and validation surfaces.`

Why Branch Is Large Enough: `The branch carries a coherent readiness layer after PR #177 and adds the USER-requested display proof, which is too cross-cutting to treat as a tiny docs-only correction.`

Why Not Split Into Tiny Branches: `Splitting display removal from setup/consent readiness would risk shipping another incomplete readiness layer and losing the required proof that UI posture matches setup and consent state.`

Acceptance Criteria: `Stage 2 records v1.7.8 canon closure, active branch authority, planning fields, branch plan, desktop display validation requirement, Workstream seams, validation results, commit, and push; later phases must prove setup/execution remain gated.`

Validation Proof Requirements: `Required proof includes governance, release-health, governance-efficiency, release-body, provider-state, planning-fixture, validation-suite, rebaseline audit, compile, diff checks, and later desktop display absence validation.`

Screenshot / Live / User Test Summary Proof Requirements: `Stage 2 records the requirement only; Workstream/H1/LV1 must validate that the screenshot-visible long AI-owned desktop display is removed and provide static or live proof according to LV1 posture.`

Implementation Sequence Proposal: `Sequence should be Workstream Entry design, setup flow state, consent flow state, provider selection/config confirmation, compact UI/display removal, validator fixtures, source-truth closeout, H1, LV1, and PR Readiness.`

Planning Blockers: `Workstream implementation is complete; H1 is pending USER approval, and provider setup, consent collection, SDK/model execution, downloads, external calls, memory, voice/Core sync, shortcut/installer, release, PR, merge, FAM-006, and Governance mutation remain separate decisions.`

USER Decisions Needed: `Approve Hardening H1 next.`

Planning Packet Status: `Complete`

Planning Revalidation Status: `PASS`

User Test Summary Strategy: `LV1 should use static validator substitute unless USER approves a real setup path; either way it must prove desktop display absence and disabled/status-only provider posture.`

Planning Completion Waiver: `Not required - Stage 2 records the required Product Definition Plan and Runtime Branch Engineering Contract fields.`

## Runtime Branch Engineering Contract

Engineering Contract Status: `Accepted for Branch Readiness Stage 2 planning`

USER Engineering Planning Review: `Complete for Workstream Entry; bounded implementation followed the accepted design packet.`

Runtime Implementation Approval: `Granted for bounded local-only setup/consent-flow readiness only; real setup, consent collection, SDK/model execution, downloads, external calls, memory, voice/Core, shortcuts, installers, release, PR, and merge remain pending USER decision.`

Branch Purpose: `Prepare a bounded local-only setup and consent flow readiness layer after v1.7.8-prebeta while preserving provider setup implementation, consent collection, provider SDK/model execution, and functional AI as future USER decisions.`

Current Runtime Baseline: `PR #177 released local-only provider path and consent readiness with provider path unavailable/unselected/future-gated, provider profile/config envelope, distinct setup and execution consent posture, provider-visible data none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads/install blocked, memory deferred, network blocked, voice/Core gated, and validator fixture proof.`

Planned Runtime Delta: `The future Workstream should add setup flow readiness state, setup flow eligibility, setup blockers and reason codes, consent flow readiness state, setup and execution consent handoff fields, provider selection/config confirmation posture, setup approval status, compact UI mapping, and desktop AI-owned readiness display absence validation.`

User-Facing Runtime Delta: `The user-facing delta should remove the long always-visible AI-owned readiness box from the desktop and preserve only compact, truthful, future-gated setup and consent readiness labels if the later Workstream approves any visible status at all.`

State / Config / Schema Delta: `Planned fields include setup_flow_readiness, setup_flow_eligibility, setup_flow_blockers, setup_flow_reason_codes, setup_flow_provenance, setup_flow_schema_version, consent_flow_readiness, setup_consent_flow_status, execution_consent_flow_status, provider_selection_confirmation_status, provider_config_confirmation_status, approval status, and provider-visible-data consent posture.`

Validator / Helper Delta: `Validation must prove setup flow default unavailable, setup approval missing, setup consent missing, execution consent missing, provider selection/config unconfirmed, provider-visible-data none, prompt/model execution disabled, downloads/network/memory/voice gated, and the visible desktop AI-owned readiness display removed.`

Expected Changed Files / Surfaces: `Expected Workstream surfaces include desktop/ai_provider_state.py, desktop/core_visualization_renderer.py, desktop/desktop_renderer.py, nexus_visual/orin_core.css, nexus_visual/orin_core.html, nexus_visual/orin_core.js, nexus_visual/orin_core_desktop.html, dev/orin_ai_provider_state_validation.py, optional desktop UI validator fixtures, Docs/validation_helper_registry.md when registry changes are required, Docs/feature_backlog.md, Docs/prebeta_roadmap.md, this branch record, and the branch plan.`

Approval-Boundary Audit: `This branch may plan setup and consent flow readiness but must not implement provider setup, collect consent, integrate SDKs, execute prompts/models, download models, make external calls, create memory indexes, sync voice/Core runtime, change shortcuts/installers, create issues, open PRs, merge, release, mutate FAM-006, mutate Governance outside this branch path, clean branches, import AI Product Contract, import Private Dev ORIN, or execute v1.8.0-prebeta without separate USER approval.`

Future-Gated Items: `Provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external calls, memory indexing/retrieval/learning/persistence/personalization, voice/Core sync, shortcut/installer work, release/tag/artifact work, issue closeout, PR creation, merge, FAM-006 mutation, Governance mutation, branch cleanup, AI Product Contract import, Private Dev ORIN import, successor selection, and v1.8.0-prebeta release execution.`

Workstream Seam Map: `Seam 1 Provider Setup Flow Readiness Contract; Seam 2 Setup Eligibility and Blocker Model; Seam 3 Setup and Execution Consent Flow Readiness; Seam 4 Provider Selection and Config Confirmation Handoff; Seam 5 Core/Desktop/ORIN Setup and Consent UI Posture plus AI-owned display removal proof; Seam 6 Functional-AI and v1.8.0 Continuation Criteria.`

Proof Expectations: `Proof requires source-truth alignment, branch governance validation, release-readiness health validation, governance efficiency validation, provider-state validation, branch-readiness planning fixture validation, validation suite proof, rebaseline audit proof, compile checks, UI/static proof that the long AI-owned desktop display is absent, approval-boundary audit, and FAM-006/Governance overlap forecast.`

Risk Forecast: `Primary risk is repeating the previous branch's failure to remove the visible AI-owned readiness display; secondary risks are shared source-truth overlap with FAM-006/Governance, over-implying real setup or consent collection, and expanding into provider SDK/model execution before USER approval.`

Recommendations And Alternatives: `Preferred path is a bounded local-only readiness Workstream with explicit desktop display removal validation. A narrower display-only branch would under-serve setup flow readiness, while a larger real setup wizard branch would cross pending USER decisions.`

Plan Version / Revision Status: `v1 accepted for Stage 2 setup after USER revision requiring desktop AI-owned readiness display validation.`

Plan-To-Implementation Traceability: `Planned state, UI label, desktop-display suppression checks, validator fixtures, and source-truth markers are mapped to actual runtime, UI, validator, and source-truth implementation files; H1 and LV1 must compare actual proof against this contract before PR Readiness.`

## Workstream Admission

Workstream Label: `FAM-007 Local AI Provider Setup and Consent Flow Readiness`

Workstream Definition: `Provider Setup and Consent Flow Readiness is the bridge from provider path and consent readiness toward future USER-approved provider setup and consent collection work. It defines setup flow readiness contracts, consent flow readiness contracts, setup eligibility, blocker state, compact UI posture, proof expectations, and validation planning without implementing setup or collecting consent.`

Desktop AI-Owned Readiness Display Validation: `Required - the admitted Workstream must prove that the long AI-owned readiness/readiness-summary desktop display seen by USER is removed or suppressed and is not an always-displayed desktop box.`

Seam Family 1: `Provider Setup Flow Readiness Contract - setup flow readiness state, setup flow eligibility, setup flow blockers, setup flow reason codes, setup flow provenance, schema versioning, and setup approval status.`

Seam Family 2: `Setup Eligibility and Blocker Model - setup start eligibility, provider selection/config confirmation linkage, capability/download/install blockers, manifest posture, safety/eval posture, and setup execution approval status.`

Seam Family 3: `Setup and Execution Consent Flow Readiness - setup consent flow status, execution consent flow status, consent blockers, reason codes, provenance, provider-visible-data consent posture, audit posture, and future consent collection handoff fields.`

Seam Family 4: `Provider Selection and Config Confirmation Handoff - provider selection confirmation, provider config confirmation, local/null fallback posture, provider profile metadata, setup handoff markers, SDK handoff markers, and approval status.`

Seam Family 5: `Core/Desktop/ORIN Setup and Consent UI Posture - compact visible setup/consent readiness copy, disabled/future-gated provider setup and execution copy, provider-visible-data none copy, and proof that the desktop AI-owned readiness display is removed.`

Seam Family 6: `Functional-AI and v1.8.0 Continuation Criteria - functional-AI criteria remain unsatisfied until provider setup, consent collection, provider adapter, prompt routing, model execution, provider-visible data behavior, validators, and release-readiness translation are approved and proven.`

## Validation Expectations

Required Validation: `git diff --check origin/main...HEAD; git diff --check; python dev\orin_branch_governance_validation.py; python dev\orin_branch_governance_validation.py --release-readiness-health-gate; python dev\orin_governance_efficiency_validation.py; python dev\orin_release_body_validation.py; python dev\orin_ai_provider_state_validation.py; python dev\orin_branch_readiness_planning_fixture_validation.py; python dev\orin_validation_suite.py --phase runtime-fam007; python dev\orin_worktree_rebaseline_audit.py --target-ref origin/main; python dev\orin_monitoring_hud_surface_validation.py; python dev\orin_monitoring_hud_internal_sandbox_validation.py; python -m compileall -q dev desktop Audio main.py; any new desktop-display validator required by implementation.`

## Overlap Forecast

FAM-006 Overlap Forecast: `FAM-006 remains active and dirty in its own lane with shared docs, desktop_renderer.py, validator, and nexus_visual overlap risk. The current Stage 2 approval routes this as later reconciliation risk and does not authorize FAM-006 mutation.`

Governance Overlap Forecast: `Governance remains the standing intake lane. PR #178 repair truth is released in v1.7.8-prebeta, and later Governance work may require reconciliation before PR or release readiness if it advances origin/main.`

## Next Legal Step

Next Legal Seam: `Hardening H1`

Exact USER Decision Needed: `Approve Hardening H1 for the completed FAM-007 Local AI Provider Setup and Consent Flow Readiness Workstream.`
