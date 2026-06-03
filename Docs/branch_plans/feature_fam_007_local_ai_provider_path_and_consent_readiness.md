# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Path and Consent Readiness

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Path and Consent Readiness runtime plan v1, admitted during Branch Readiness Stage 2 after v1.7.7-prebeta release execution.`

Owning Branch: `feature/fam-007-local-ai-provider-path-and-consent-readiness`

Worktree Path: `C:\Nexus Worktrees\FAM-007`

Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md`

Current Phase: `PR Readiness Stage 1 Ready For Stage 2; PR creation remains pending USER approval`

Branch Runtime Engineering Plan: `Accepted and present for this runtime-focused FAM-007 branch. The plan owns detailed active-branch runtime execution planning for provider path readiness, consent readiness, setup eligibility, UI posture, validator fixtures, and future v1.8.0-prebeta criteria while the branch authority record remains the phase, approval, blocker, and next-legal-phase control surface.`

Engineering Plan Status: `Accepted - implemented provider path and consent readiness planning maps to local-only runtime state, Core/Desktop/ORIN UI posture, validator fixtures, source-truth proof, H1 review, LV1 waiver/static-proof posture, PR Readiness Stage 1 repair, selected-next defer/waiver, pre-PR live-state, and post-merge No Active Branch projection.`

Current Runtime Baseline: `PR #172 released local-only provider execution-readiness gates with execution readiness state, provider path and adapter selection posture, disabled prompt/model/provider execution, sentToProvider false, canAcceptPrompts false, provider-visible-data none, blocked downloads/install, deferred memory/learning/personalization, blocked network egress, gated voice/Core sync, v1.8.0 functional-AI criteria, Core/Desktop/ORIN copy, and validator fixture proof.`

Branch Purpose: `Implement local-only provider path and consent readiness contracts so the branch defines provider path state, consent requirement state, setup eligibility, data visibility, UI copy, validators, and v1.8.0-prebeta criteria without enabling provider setup, consent collection, provider SDKs, model execution, external calls, memory, learning, personalization, or release work.`

Planned Runtime Delta: `Define provider path readiness state, provider path eligibility, provider path blocker state, reason codes, provenance, schema version fields, approval status, execution-readiness-to-provider-path mapping, provider selection posture, provider configuration envelope, consent requirement posture, data visibility requirements, setup eligibility, capability alignment, local/null fallback posture, and release-proof criteria as a local-only runtime delta.`

User-Facing Delta: `Implementation shows user-visible UI copy and desktop/Core status labels that distinguish execution readiness, provider path readiness, consent readiness, provider setup, provider/model execution, provider-visible-data none, setup future-gated, memory/learning deferred, network blocked, and v1.8.0 functional-AI criteria pending.`

Source-Truth Delta: `Source-truth changes keep backlog and roadmap compact as pointer/status surfaces while this branch plan and the branch authority record own detailed runtime planning, approval-boundary proof, per-seam implementation checklists, validation proof, Live Validation waiver posture, PR fold-down posture, and release-readiness translation.`

State / Config / Schema Delta: `Workstream implementation adds local-only provider path readiness state fields, consent requirement fields, provider configuration envelope fields, setup eligibility fields, blocker provenance, schema version fields, safe default config values, and fail-closed missing/invalid config behavior without persistence of credentials, consent records, memory, provider traffic, or learning data.`

Validator / Helper Delta: `Validator and helper work proves provider path readiness fixtures, execution-readiness-to-provider-path mapping, provider selection/config envelope posture, consent requirement posture, provider-visible-data none, no consent collection, no provider setup execution, no prompt send, no model execution, network egress blocked, memory/indexing/learning deferred, v1.8.0 criteria pending, branch-plan pointer integrity, compact backlog/roadmap posture, and Workstream/H1/LV1 proof gates.`

Expected Changed Files / Surfaces: `Implementation surfaces include desktop/ai_provider_state.py, desktop/core_visualization_renderer.py, desktop/desktop_renderer.py, nexus_visual/orin_core.css, nexus_visual/orin_core.html, nexus_visual/orin_core.js, nexus_visual/orin_core_desktop.html, dev/orin_ai_provider_state_validation.py, Docs/feature_backlog.md, Docs/prebeta_roadmap.md, Docs/branch_records/index.md, Docs/branch_records/feature_fam_007_local_ai_provider_path_and_consent_readiness.md, this branch plan, and Docs/validation_helper_registry.md.`

Workstream / Seam Map: `Seam 1 implementation and validation covers the Provider Path Readiness Contract. Seam 2 covers Provider Selection And Configuration Envelope. Seam 3 covers Consent Requirement And Data Visibility Contract. Seam 4 covers Setup Eligibility And Capability Alignment. Seam 5 covers Core/Desktop/ORIN Provider Path And Consent UI Planning. Seam 6 covers Functional-AI And v1.8.0 Continuation Criteria.`

Per-Seam Implementation Checklist: `Seam implementation checklist: define provider path readiness state and config fields; define provider selection and configuration envelope metadata; define consent requirement and data visibility contract; define setup eligibility plus capability/install/download/hardware/manifest/safety blockers; define Core/Desktop/ORIN provider path and consent copy; define functional-AI and v1.8.0 criteria; update source-truth files; preserve pending USER gates.`

Per-Seam Validation Checklist: `Seam validation checklist: run provider-state validator fixtures, governance validation, branch-readiness planning fixture validation, validation suite recommendation, compile checks, diff whitespace checks, rebaseline audit report-only helper, and any new validator fixture that proves no provider setup, no consent collection, no prompt send, no model execution, provider-visible data none, blocked downloads/install, blocked network egress, and memory/learning deferral.`

Per-Seam User-Facing Proof Checklist: `Seam user-facing proof checklist: verify visible Core/Desktop/ORIN copy or static source payloads show provider path and consent readiness rather than provider setup or functional AI, confirm screenshots or static validators when UI changes, record UTS waiver if disabled/status-only posture remains, and prove user-facing labels do not imply provider availability, granted consent, setup readiness, or model execution.`

Future-Gated Items: `Future-gated items remain provider path/setup implementation, consent collection implementation, provider SDK integration, provider/model execution, model downloads, external provider/API calls, memory indexing/retrieval/learning/persistence/personalization, voice/Core runtime sync, shortcut/installer work, release/tag/GitHub Release/artifact work, issue work, FAM-006 mutation, Governance mutation, branch cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta release execution.`

Approval-Boundary Audit: `Approval boundary audit: USER approved bounded local-only Workstream implementation for provider path and consent readiness. Provider setup, consent collection, prompt acceptance, provider calls, model workloads, network egress, memory writes, learning updates, personalization stores, voice/Core sync, shortcut/installer changes, PR creation, merge, release execution, issue work, FAM-006 mutation, Governance mutation, AI Product import, and Private Dev ORIN import remain pending separate USER approval.`

FAM / Shared-Surface Overlap Forecast: `FAM-006 has separate active work with shared docs, dev/orin_branch_governance_validation.py, desktop/desktop_renderer.py, and nexus_visual overlap risk; Governance remains a separate standing intake lane. This branch must rerun rebaseline and overlap checks before H1, LV1, PR Readiness, or release-readiness claims.`

Open Questions: `Open questions after Workstream implementation: which provider path should be selected first later; what real consent collection proof should look like before setup; how setup eligibility should transition when hardware/capability/manifest/safety blockers are later approved; whether memory, learning, and personalization stay deferred to v1.8.0-prebeta; and what minimum live proof is required before version-jump readiness.`

USER Planning Decisions: `USER approved Branch Readiness Stage 2 setup, Workstream Entry analysis, bounded Workstream implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair for this branch. USER has not approved PR Readiness Stage 2 / PR creation, merge, provider path/setup implementation, consent collection, provider SDK integration, provider/model execution, model downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, release execution, issue work, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, or v1.8.0-prebeta release execution.`

Plan Revision History: `v1 created during Branch Readiness Stage 2 from origin/main eb8d36b4464ad560a59cfea8ddc641aa6374293f after v1.7.7-prebeta. Reconciliation revision merged origin/main 67727cfeb21ba4b991c930861ce5920416d27e94 after PR #173, preserving branch authority, v1.7.7 canon closure, and provider path/consent readiness planning. Workstream implementation revision records local-only provider path and consent readiness state, UI, fixtures, and source-truth completion. Hardening H1 revision records H1 Green. Live Validation LV1 revision records LV1 Green and disabled/status-only classification. PR Readiness Stage 1 revision records selected-next defer/waiver truth, pre-PR live-state truth, post-merge No Active Branch projection, Release Readiness Health Pass, Release Window Audit, and Stage 2 / PR creation as the next USER-gated phase.`

Plan-To-Implementation Traceability Table: `Implemented provider path readiness state maps to desktop/ai_provider_state.py; provider selection/config envelope maps to local config/schema fields and provider profile metadata; consent and data visibility gates map to disabled provider-visible-data and no-consent-collection fields; UI copy maps to Core/Desktop/ORIN status surfaces; validators prove no setup, no consent collection, no prompt send, no model execution, provider-visible data none, blocked network egress, deferred memory/learning/personalization, and v1.8.0 criteria pending.`

Hardening Comparison Checklist: `Hardening must compare implementation against this plan for state/config/schema coverage, UI copy integrity, validator fixtures, provider-visible-data none posture, no consent collection, no provider setup, no prompt/model execution, no network egress, no memory/learning/personalization, future-gated item preservation, source-truth consistency, and Workstream seam completion.`

Live Validation Proof Or Waiver Checklist: `Complete - LV1 records static proof and waiver because the branch remains disabled/status-only. It proves visible provider path and consent readiness posture, no consent collection, disabled prompt/provider execution, no model workload, blocked download/install, provider-visible data none, blocked network egress, deferred memory/learning/personalization, gated voice/Core sync, and no shortcut/installer path.`

Live Validation LV1 Result: `Green - disabled/status-only local provider path and consent readiness scaffold validated through static Core/Desktop/ORIN source-truth and provider-state validator proof; User Test Summary, shortcut validation, and Codex live-client self-QA are waived because no live provider setup, consent collection, prompt, model, setup, shortcut, installer, network, memory, or voice/Core path is enabled.`

PR Readiness Fold-Down / Retention Checklist: `PR Readiness must decide whether this plan stays as historical branch source truth, compacts into a branch receipt, or promotes durable provider path/consent readiness lessons into a canonical workstream or family dossier. Fold-down must preserve provider setup gates, consent collection gates, provider/model execution gates, v1.8.0 criteria, release-public-scope translation, and pending USER decisions.`

Release Readiness Public-Scope Translation Checklist: `Release Readiness must translate this plan into public release language by highlighting provider path and consent readiness scaffolding only, listing excluded provider setup/consent collection/SDK/model execution/downloads/external calls/memory/learning/personalization/voice/Core/shortcut/installer work, preserving v1.8.0-prebeta as future functional-AI target, and avoiding internal governance jargon.`

USER Planning Review: `Accepted for Workstream implementation, H1, LV1, and PR Readiness Stage 1 - USER approved Branch Readiness Stage 2 setup, Workstream Entry analysis, bounded local-only provider path and consent readiness implementation, Hardening H1, Live Validation LV1, and PR Readiness Stage 1 source-truth repair. PR Readiness Stage 2 / PR creation remains pending USER approval.`

PR Readiness Stage 1 Result: `Ready for Stage 2 - selected-next defer/waiver truth, pre-PR live-state truth, post-merge No Active Branch projection, Release Readiness Health Pass, Release Window Audit, and successor-selection deferral recorded.`
PR Fold-Down Packet: `Pending - no PR exists for this branch; PR Readiness Stage 2 must create the PR before live PR fold-down/watch state can exist.`

Runtime Implementation Approval: `Granted - USER approved bounded local-only provider path and consent readiness Workstream implementation. Provider path/setup implementation, consent collection, provider SDK integration, provider/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer, release, PR, merge, FAM-006/Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution remain pending USER decisions.`

Workstream Completion Evidence: `Green - all six admitted seam families are implemented as local-only scaffolding: Provider Path Readiness Contract; Provider Selection And Configuration Envelope; Consent Requirement And Data Visibility Contract; Setup Eligibility And Capability Alignment; Core/Desktop/ORIN Provider Path And Consent UI Planning; Functional-AI And v1.8.0 Continuation Criteria.`

Next Legal Phase: `PR Readiness Stage 2 / PR creation after USER approval.`

Historical USER Decision Receipt: `Approve PR Readiness Stage 2 / PR creation for feature/fam-007-local-ai-provider-path-and-consent-readiness targeting main. Merge, provider path/setup implementation, consent collection, provider SDK/model execution, downloads, external calls, memory/learning/personalization, voice/Core sync, shortcut/installer work, release work, issue work, FAM-006 mutation, Governance mutation, branch cleanup, AI Product import, Private Dev ORIN import, and v1.8.0-prebeta release execution remain separate decisions.`
