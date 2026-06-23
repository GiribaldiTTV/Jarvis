# FAM-007 Local AI And Capability Packs Vision

## Purpose

This family vision records durable product direction for local AI, provider setup, provider readiness, consent posture, consent collection, capability packs, model lifecycle, local-only privacy boundaries, provider-visible data, execution gates, memory/future learning boundaries, and Core/Desktop AI state.

## Vision Summary

Local AI and capability packs should make Nexus feel smarter while preserving local-first trust, explicit provider boundaries, clear consent, hardware safety, and useful no-provider behavior.

## Accepted Direction

- The base app should remain useful without a local LLM.
- Heavy local AI should remain optional capability-pack work, not default installer bloat.
- Assisted Desktop Mode and no-provider behavior should be defined before real provider execution.
- Owner, Dev, and Public AI deployment must follow the public-safe Edition Capability / Trust Boundary plan before provider/model/runtime work claims release readiness.
- Provider-visible data, privacy mode, hardware eligibility, network/download behavior, and memory/indexing boundaries must be explicit before runtime execution.
- External API use should be opt-in, revocable, cost/privacy-aware, and visible.
- AI Operational Cache Governance belongs here only for AI runtime/provider cache behavior, capability-pack cache manifests, cache provenance, cache validity windows, deterministic versus advisory cache behavior, and provider-cache sanitization; cache is operational state, not memory.
- ORIN remains the stable assistant identity across local models, external providers, no-provider mode, and capability-pack changes.
- Deterministic routing, reliability tiers, capability self-awareness, provider orchestration, and cache replay safety must follow `Docs/ai_runtime_and_trust_architecture.md` before implementation-specific FAM-007 slices can claim readiness.
- Capability packs should declare what they can do, what they cannot do, what sources they contain, what hardware/storage/provider state they require, what cache/index state they own, and whether they are local-only or provider-assisted.
- Provider recommendation is allowed when local capability is insufficient, but execution remains permission-gated and provider-visible data must be explicit before anything leaves the machine.
- AI status shown in tray, HUD, Dashboard, or future AI Command Center surfaces must reflect real permission, provider, local-only, privacy-lockdown, capability-pack, cache, memory, and blocked/degraded posture; UI copy must not overstate runtime capability.
- The visible top-most AI hub surface name is `AI Dashboard` after the USER-approved FAM-007 Workstream carrydown on `2026-06-22`. `AI Control Center` remains a focused FAM-007 control domain/card inside AI Dashboard, not the whole top-most AI window. Internally, the accepted durable product model is `AI Home / Control Foyer`: the top-level AI orientation and control-entry model that tells the USER what AI exists, what state it is in, what is safe or blocked, and where to go for each AI subsystem.
- AI Dashboard should keep top-level content compact, orienting, trust-critical, immediately useful, or navigational. Detailed reports, diagnostics, setup flows, logs, selectors, provider internals, capability details, memory/cache/private setup, and long workflows should route through categories, focused surfaces, child/drill-down surfaces, Global Settings, or future-gated placeholders instead of becoming permanent stacked top-level cards unless source truth and USER approval create an explicit exception.
- AI Dashboard category cards are doorways, not workspaces. Each top-level category card should contain compact status/summary plus launcher buttons that open the relevant external, domain, focused, child, or drill-down surface. Local AI Check, readiness report generation/results, diagnostics details, provider internals, capability details, setup, settings internals, proof data, and maintenance lifecycle details must run or display inside the opened surface rather than inline in the AI Dashboard hub.
- AI Dashboard and AI Control Center placement decisions must classify AI-related items by role: top-level summary, top-level action, category doorway, focused surface, child/drill-down detail, settings route, maintenance lifecycle detail, diagnostic/status/trust-boundary, concrete USER-facing feature, future-gated placeholder, cross-FAM dependency support, or out-of-scope. The concrete USER-facing feature classification gate remains active: runtime-visible status, blocked-state explanation, provider-visible-data `none`, and truthful unavailable-capability copy do not count as concrete features by themselves.
- AI Control Center category direction should start from USER jobs, including Active AI, AI Readiness, AI Diagnostics, Trust & Provider, Capabilities, Developer / Owner, Activity / Recovery, and AI Settings handoff when an owning surface is approved. The top level may show compact summaries and doorway actions; child/focused surfaces own deeper reports, setup, selectors, settings, logs, and long diagnostic content.
- The FAM-006 shared-rendered primitive lesson applies to future visible FAM-007 surfaces: reference-derived UI approximations cannot close as green when the accepted reference path requires shared rendered DOM/CSS primitives, side-by-side visual adjudication, code-to-visual trace, and USER acceptance or waiver.
- Owner AI Operational Foundation Gates are accepted as a public-safe control-plane route for artifact exclusion controls, provider/runtime disabled-state consent shells, cache-versus-memory consent gates, capability install-intent gates, Developer/Owner lane readiness gates, and future Owner AI memory/agent prerequisite schemas without activating private setup, provider/model execution, runtime cache behavior, real memory, or real agents.
- OpenAI Docs or other provider documentation lookups are planning evidence only until digested into the owning repo source truth. OpenAI Developers tooling, API key creation, provider account setup, connector authentication, billing/quota state, model/runtime setup, and provider-visible data routing remain sensitive setup or implementation concerns and require separate USER approval before execution or durable source-truth claims.

## Implementation Boundaries

- This vision does not admit provider SDK integration, model downloads, external calls, memory/indexing, voice/Core sync, shortcut/installer work, or AI Product Contract import.
- This vision does not admit new AI Control Center child-window implementation, tray AI-status implementation, or a second AI tray icon by itself.
- This vision does not admit persistent memory, learning, personalization, hidden provider residue, or runtime cache implementation by itself.
- Active FAM-007 branches must carry accepted Branch Vision Snapshot and provider-state validation proof before Workstream implementation.
- Active FAM-007 branches that consume AI-native architecture must run the Backlog Taxonomy And Source-Truth Placement Gate, cite `Docs/ai_runtime_and_trust_architecture.md`, and prove provider, cache, permission-state, capability-pack, and local-only boundaries in the USER Branch Plan Review packet before Workstream implementation.
- FAM-007 gate/control-plane branches may implement public-safe disabled states, schemas, validators, and route-back checks only when BP1, BP2, BP3, and Workstream approval are accepted or waived; those gates must keep real private setup, provider/model execution, runtime cache activation, memory persistence, Owner memory, and Owner agents behind later USER decisions.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Resident access FFV: `Docs/family_feature_visions/F3-FF01.md`
- Edition capability / trust boundary release plan: `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`
- Backlog registry: `Docs/feature_backlog.md`
- Durable receipt pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_setup_completion_foundation.md`
- Provider-state validator: `dev/orin_ai_provider_state_validation.py`
