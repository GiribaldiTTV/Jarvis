# Branch Runtime Engineering Plan - FAM-007 Local AI Provider Setup and Consent Flow Readiness

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Setup and Consent Flow Readiness Branch Runtime Engineering Plan`

Owning Branch: `feature/fam-007-local-ai-provider-setup-and-consent-flow-readiness`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_and_consent_flow_readiness.md`

Current Phase: `PR Readiness Stage 1 Ready For Stage 2 - PR creation pending USER approval`

Branch Runtime Engineering Plan: `Accepted and implemented for the bounded local-only setup and consent flow readiness Workstream; real setup flow, consent collection, SDK, provider, model, memory, voice/Core, shortcut, installer, release, PR, and merge work remain pending USER decisions.`

Engineering Plan Status: `Accepted - implemented setup/consent-flow readiness contracts, desktop display suppression, validator fixtures, UI telemetry, source-truth proof, H1 review, LV1 static validation, and PR Readiness Stage 1 fold-down are Green; PR Readiness Stage 2 / PR creation is pending USER approval.`

Current Runtime Baseline: `PR #177 released local-only provider path and consent readiness state, provider selection/configuration envelope posture, distinct setup and execution consent posture, provider-visible-data none, sentToProvider false, canAcceptPrompts false, prompt/provider/model execution disabled, downloads/install blocked, memory/indexing/learning/personalization deferred, network egress blocked, voice/Core sync gated, and Core/Desktop/ORIN status copy.`

Branch Purpose: `This branch prepares the next FAM-007 layer after v1.7.8-prebeta by planning provider setup flow readiness and consent flow readiness without enabling a real provider setup wizard, consent collection, provider SDK integration, prompt/model execution, network egress, downloads, memory, voice/Core sync, shortcut, installer, release, issue, PR, or merge behavior.`

Planned Runtime Delta: `The future bounded Workstream should add status-only setup flow readiness contracts, setup start eligibility, consent flow readiness contracts, setup and execution consent separation, provider selection confirmation posture, setup blocker reason codes, flow provenance, schema markers, UI copy rules, and validators proving setup and execution remain future-gated. It must also remove or suppress the always-visible long AI-owned readiness display from the desktop and prove the desktop no longer exposes that display.`

User-Facing Delta: `The visible Core/Desktop/ORIN posture should become quieter and more precise: provider setup flow readiness and consent flow readiness may be represented as compact status labels or gated controls, while the prior long AI-owned readiness/readiness-summary desktop display must not remain visible as an always-displayed box. Copy must distinguish setup readiness, consent readiness, provider setup, provider execution, functional AI, and v1.8.0 future-version criteria.`

Source-Truth Delta: `Docs/feature_backlog.md, Docs/prebeta_roadmap.md, the active branch authority record, this plan, and validation helper registry entries when needed must record v1.7.8 closure, released PR #173 through PR #178 posture, the active setup and consent flow readiness carrier, desktop display removal validation, Workstream seam status, approval boundaries, validation commands, and proof expectations.`

State / Config / Schema Delta: `Expected state/config/schema planning includes setup_flow_readiness status, setup_flow_eligibility, setup_flow_blockers, setup_flow_reason_codes, setup_flow_provenance, consent_flow_readiness, setup_consent_flow_status, execution_consent_flow_status, provider_selection_confirmation_status, provider_config_confirmation_status, provider_visible_data_consent_status, approval status fields, and schema version markers.`

Validator / Helper Delta: `Provider-state validation should gain fixtures for setup flow unavailable, setup flow blocked, setup approval missing, setup consent missing, execution consent missing, provider selection unconfirmed, provider config unconfirmed, provider-visible-data still none, prompt send disabled, model execution disabled, network blocked, memory deferred, voice/Core gated, and desktop AI-owned readiness display absent. UI/static validators should assert the long display is not rendered in the desktop surface.`

Expected Changed Files / Surfaces: `Expected implementation surfaces are desktop/ai_provider_state.py, desktop/core_visualization_renderer.py, desktop/desktop_renderer.py, nexus_visual/orin_core.css, nexus_visual/orin_core.html, nexus_visual/orin_core.js, nexus_visual/orin_core_desktop.html, dev/orin_ai_provider_state_validation.py, optional focused UI validator fixtures, Docs/validation_helper_registry.md if helper registry changes are added, Docs/feature_backlog.md, Docs/prebeta_roadmap.md, this plan, and the branch record.`

Workstream / Seam Map: `Seam 1 setup flow readiness contract; Seam 2 setup eligibility and blocker model; Seam 3 setup and execution consent flow readiness; Seam 4 provider selection/config confirmation handoff; Seam 5 Core/Desktop/ORIN setup and consent UI posture plus desktop AI-owned display removal proof; Seam 6 functional-AI and v1.8.0 continuation criteria plus release-readiness translation.`

Per-Seam Implementation Checklist: `Implement setup flow readiness contracts, implement setup blockers and reason codes, implement consent flow readiness separation, implement provider selection/config confirmation posture, update compact UI copy and remove the long always-visible AI-owned readiness display, add validator fixtures, update source truth, and keep all provider setup/execution behavior disabled until later USER approval.`

Per-Seam Validation Checklist: `Run branch governance, release-readiness health, governance efficiency, release body, provider-state, branch-readiness planning fixture, validation suite runtime-fam007, rebaseline audit, monitoring HUD validators, compileall, diff checks, and any new desktop/UI validator proving the AI-owned readiness display is absent.`

Per-Seam User-Facing Proof Checklist: `Workstream proof must show compact visible setup and consent posture, no provider-visible data, sentToProvider false, canAcceptPrompts false, disabled prompt/provider/model execution, blocked downloads/install, blocked network egress, deferred memory, gated voice/Core sync, and the removed/suppressed AI-owned readiness desktop display.`

Future-Gated Items: `Provider setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external provider/API calls, memory indexing/retrieval/learning/persistence/personalization, voice/Core runtime sync, shortcut/installer work, release/tag/artifact work, issue closeout, PR creation, merge, FAM-006 mutation, Governance mutation outside this branch path, branch cleanup, AI Product Contract import, Private Dev ORIN import, successor selection, and v1.8.0-prebeta release execution remain pending USER decisions.`

Approval-Boundary Audit: `USER approved Workstream Entry, the bounded local-only implementation, H1, and LV1; any real provider setup flow, consent capture, SDK selection, model execution, network call, download, memory store, voice/Core sync, shortcut/installer change, issue action, PR, merge, release, or branch cleanup remains out of scope.`

FAM / Shared-Surface Overlap Forecast: `FAM-006 is dirty in its own worktree and carries later shared-doc, desktop_renderer.py, validation, and nexus_visual overlap risk. Governance remains a standing intake lane. This branch may touch Core/Desktop/ORIN and source-truth surfaces, so future reconciliation must preserve active FAM-007 authority while not mutating FAM-006 or Governance without USER approval.`

Open Questions: `None for Workstream implementation, H1, LV1, or PR Readiness Stage 1. LV1 validated the disabled/status-only posture, desktop display absence, and static validator/source-truth proof route; PR Readiness Stage 1 folded down this evidence, selected-next defer/waiver, pre-PR live-state, post-merge No Active Branch projection, and release-window posture before PR creation can be requested.`

USER Planning Decisions: `USER approved Branch Readiness Stage 2 setup with a revision requiring validation that the visible desktop AI-owned readiness display is removed because the previous branch did not solve it, then approved Workstream Entry, bounded implementation, H1, LV1, and PR Readiness Stage 1 source-truth repair. USER has not approved PR Readiness Stage 2 / PR creation, provider setup implementation, consent collection implementation, provider SDK/model execution, release work, merge, or successor runtime implementation.`

Plan Revision History: `v1 - created during Branch Readiness Stage 2 after v1.7.8-prebeta release execution from origin/main 2bd54f0e34c6759e9618f42d104d80b975ecc1c3; includes USER revision requiring desktop AI-owned readiness display removal validation. PR Readiness Stage 1 revision records selected-next defer/waiver, pre-PR live-state, post-merge No Active Branch projection, Release Readiness Health Pass, Release Window Audit, and Stage 2 / PR creation as the next USER-gated phase.`

Plan-To-Implementation Traceability Table: `Implemented state and UI proof maps to desktop/ai_provider_state.py, desktop/core_visualization_renderer.py, desktop/desktop_renderer.py, nexus_visual/orin_core.css, nexus_visual/orin_core.html, nexus_visual/orin_core.js, nexus_visual/orin_core_desktop.html, dev/orin_ai_provider_state_validation.py, this plan, the branch record, feature_backlog, prebeta_roadmap, and validation_helper_registry. H1 compared implemented setup flow readiness, consent flow readiness, desktop display suppression, validators, and source truth against this plan. LV1 proved disabled/status-only behavior and absence of the long AI-owned readiness desktop display. PR Readiness must fold those proofs into branch metadata.`

Hardening Comparison Checklist: `H1 must verify setup flow contracts, consent flow contracts, state/schema consistency, validator coverage, compact UI copy, desktop display removal proof, provider-visible-data none, prompt/provider/model execution disabled, future-gated items, branch authority, and overlap posture.`

Live Validation Proof Or Waiver Checklist: `LV1 must classify the branch as disabled/status-only unless USER later approves a live setup path. Static validator substitute is acceptable only if it proves the desktop display is absent, provider-visible data remains none, sentToProvider remains false, canAcceptPrompts remains false, setup/consent collection remain unimplemented, downloads/network/memory/voice remain gated, and no prompt/model execution occurs.`

PR Readiness Fold-Down / Retention Checklist: `PR readiness must retain this plan, branch record, Workstream/H1/LV1 proof, desktop display absence validation, selected-next/defer posture, historical FAM-007 release refs, approval-boundary audit, validation outputs, and release-window translation before PR creation is requested.`

Release Readiness Public-Scope Translation Checklist: `A future release must describe setup and consent flow readiness as local-only scaffolding, not real provider setup or consent collection. Public notes must mention that provider SDKs, model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, and v1.8.0-prebeta release execution remain future-gated unless separately approved.`

USER Planning Review: `Complete for Workstream Entry, implementation, H1, LV1, and PR Readiness Stage 1; PR Readiness Stage 2 / PR creation is the next USER decision.`

Hardening H1 Result: `Green - H1 compared the implemented setup flow readiness, consent flow readiness, provider setup handoff, setup consent, execution consent, data visibility, audit/local-only posture, desktop AI-owned readiness display suppression, Core/Desktop/ORIN UI copy, validators, source truth, approval boundaries, and overlap posture against this plan and found no runtime or approval-boundary drift.`

PR Fold-Down Packet: `Ready for Stage 2 - PR Readiness Stage 1 folds down Workstream Green, H1 Green, LV1 Green, desktop display suppression validation, selected-next defer/waiver, pre-PR live-state, post-merge No Active Branch projection, release-window, approval-boundary, and validation proof; PR creation remains pending USER approval.`

Live Validation LV1 Result: `Green - LV1 classified the branch as disabled/status-only local setup and consent flow readiness scaffolding, used static Core/Desktop/ORIN source-truth plus provider-state validator proof as the applicable User Test Summary substitute, proved the long desktop AI-owned readiness display remains suppressed/absent, and confirmed provider setup, consent collection, prompt/provider/model execution, downloads, network, memory, voice/Core sync, shortcut, installer, release, PR, and merge work remain unapproved.`

Runtime Implementation Approval: `Granted for the bounded local-only setup and consent flow readiness Workstream only; real setup flow, consent collection, provider SDK, provider/model execution, memory, voice/Core, shortcut, installer, release, PR, and merge work remain pending USER decision.`

Workstream Completion State: `Green - all admitted seam families complete and validation proof is owned by dev/orin_ai_provider_state_validation.py plus the standard FAM-007 validation suite.`

Desktop AI-Owned Readiness Display Suppression: `Implemented - #ai-provider-status is hidden/aria-hidden with suppression markers in Core/Desktop HTML, CSS forces hidden/suppressed status to display none, JS reasserts the hidden state while preserving provider telemetry, and validator fixtures prove the long desktop display is suppressed by default.`

Next Legal Phase: `PR Readiness Stage 2 / PR creation`

Exact USER Decision Needed: `Approve PR Readiness Stage 2 / PR creation for the completed, H1-hardened, LV1-validated, and Stage 1-ready FAM-007 Local AI Provider Setup and Consent Flow Readiness branch.`
