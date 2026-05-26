# AI Runtime And Trust Architecture

## Purpose

This document owns durable cross-family architecture, policy, and experience direction for AI-native behavior in Nexus Desktop AI.

It exists because AI-native planning crosses multiple families and should not turn FAM-007 into a catch-all or turn every important concept into a new backlog family.

Use this document for:

- AI runtime and trust architecture
- permission-state enforcement concepts
- deterministic routing and reliability tiers
- provider orchestration boundaries
- capability registry and capability-pack architecture
- AI Operational Cache Governance
- Trust Journal / AI Activity Journal direction
- routine, continuity, Windows Health, and competitive-integrity architecture boundaries

It does not own:

- backlog family identity
- active branch authority
- provider/model/runtime implementation approval
- memory approval
- installer or shortcut implementation
- private Dev / Owner repo truth
- release execution
- live operational state

## Source-Truth Position

Repo source truth owns durable governance and product/architecture direction.

Git, GitHub, and approved helpers own derived live facts such as branch state, PR state, tags, releases, and dirty state.

External operational state, after USER-approved initialization, owns live Codex/worktree/branch/release-window coordination.

This file is durable repo source truth. It is not operational state and must not be used as a live branch tracker.

## Binding And Directional Language

Binding in this file:

- source-truth ownership boundaries
- taxonomy placement requirements
- explicit non-goals
- Branch Readiness citation requirements
- implementation-approval blockers and routing rules

Directional product language in this file records durable USER-reviewed architecture intent. Words such as `should` describe the target product shape, not current runtime behavior and not implementation approval.

Future branches that implement any AI-native concept from this file must convert the relevant direction into an accepted branch vision, USER Branch Plan Review packet, Element-to-Phase Proof Matrix, implementation proof, Hardening proof, Live Validation / UTS plan, and validator/helper evidence where applicable.

If a future branch cannot tell whether a concept is binding law, product direction, implementation scope, or external operational state, the branch must stop on `Backlog Taxonomy Gate Missing`, `Source-Truth Placement Preflight Missing`, `USER Branch Plan Review Missing`, or the closest repo-supported blocker instead of implementing by inference.

## Relationship To Existing Owners

- `Docs/nexus_vision.md` owns project-wide AI-native product direction and ORIN experience intent.
- `Docs/architecture.md` owns current desktop/runtime stack boundaries.
- `Docs/orin_interaction_architecture.md` owns interaction-system architecture and the shared action model.
- `Docs/feature_backlog.md` owns family identity and taxonomy placement gates.
- `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` owns local AI, provider, capability-pack, and AI runtime family direction.
- `Docs/family_visions/FAM-008_packaging_and_install_experience.md` owns setup, install, cache-root UX, capability-pack installation, and user education direction.
- Existing FAM visions own family-local workspace/data and safety/privacy implications when their implementation touches those surfaces.
- Former workspace/data and safety/privacy backlog labels are not active backlog families. Their reusable AI-specific constraints are folded into this file and the relevant existing FAM visions.
- Active branch plans own implementation-specific Branch Vision Contract Snapshots and proof plans.

## Taxonomy Placement

AI-native planning uses this classification by default:

| Concept | Source-Truth Class | Default Owner |
| --- | --- | --- |
| AI-native operating experience | Project-wide vision plus experience layer | `Docs/nexus_vision.md` and this file |
| AI Runtime And Trust Architecture | Architecture layer plus cross-family policy owner | This file |
| Permission-State System | Architecture layer plus cross-family policy owner | This file and relevant implementing FAM vision |
| Deterministic Routing Layer | Architecture layer | This file; implementation through admitted FAM-007 slices |
| Provider Orchestration Layer | Runtime subsystem plus FAM-007 architecture | FAM-007, constrained by this file and relevant safety/privacy family-vision text |
| Trust Journal / AI Activity Journal | Cross-family trust architecture plus policy-facing experience layer | This file and relevant implementing FAM vision |
| AI Operational Cache Governance | Architecture, policy, and runtime concern | This file, with family-specific ownership below |
| Capability-Pack System | Capability-pack domain plus FAM-007 runtime architecture | This file, FAM-007, and FAM-008; other FAMs consume constraints only when implementing their own surfaces |
| Routine Engine | Runtime subsystem or future package/slice candidate | This file and FAM-003 until USER admits a concrete package |
| Daily Continuity / Ambient Assistance | Experience layer | `Docs/nexus_vision.md`, this file, and future Branch Readiness |
| Competitive Integrity Layer | Cross-family policy plus lower-level runtime enforcement | This file and relevant implementing FAM vision |
| Windows Health Recommendation Pipeline | Architecture/package candidate | This file and future Branch Readiness in the owning FAM |

None of these classifications create a new FAM by themselves.

`Backlog Taxonomy And Source-Truth Placement Gate` remains required before any future branch promotes one of these concepts into a backlog family, new source-truth owner, package, slice, seam, runtime subsystem, or capability-pack domain.

## AI-Native Operating Principles

Nexus Desktop AI should evolve toward an AI-native operating experience where Windows remains the host platform, Nexus becomes the visible experience layer, and ORIN remains the persistent cooperative assistant identity.

AI-native behavior must prioritize:

- truth over fluency
- visible boundaries over hidden state
- deterministic or tool-backed answers before generative improvisation when objective truth is available
- local-first execution where practical
- explicit provider and network boundaries
- user consent before sensitive capability activation
- calm, plain-language trust UX
- recoverable failure instead of opaque automation
- no silent escalation of permission, provider, memory, cache, routine, monitoring, install, or protected-process behavior

Provider fluency must not be mistaken for system reliability.

## Permission-State System

Permission must be enforced app state, not a verbal promise.

Allowed permission/capability states:

- `Installed`
- `Available`
- `Enabled`
- `Disabled`
- `Denied`
- `Suspended`
- `Revoked`
- `Requires Setup`
- `Requires Hardware`
- `Requires Consent`
- `Blocked By Privacy Mode`
- `Blocked By Safety Policy`
- `Blocked By Competitive Integrity Mode`
- `Blocked By Provider State`

The UI may describe these states, but UI copy is not the authority by itself. Runtime behavior, provider/network behavior, cache behavior, and tool access must align with the actual permission state.

Sensitive capability classes include camera, microphone, desktop vision, screen understanding, memory, identity recognition, Windows Health logs, file/document access, email review, finance/bills access, external API/provider use, local model execution, knowledge/capability packs, overlays, gaming/process-sensitive features, and protected-process interaction.

## Deterministic Routing Layer

Objective or safety-sensitive requests should route through deterministic, tool-backed, or validation-backed paths before generative responses when such paths exist.

Reliability tiers:

- `Deterministic`
- `High Confidence`
- `Advisory`
- `Creative/Open-ended`

Deterministic routing should account for:

- source availability
- tool capability
- permission state
- provider state
- confidence threshold
- freshness requirements
- citation or provenance needs
- safety and privacy policy
- refusal or uncertainty behavior

When an answer is advisory or uncertain, the product should say so plainly instead of letting confident wording hide weak proof.

## Provider Orchestration Boundary

ORIN remains the stable assistant identity. Providers, models, local runtimes, external APIs, and capability packs are replaceable capability extensions, not the product identity.

Provider/API behavior must preserve:

- user-controlled provider choice
- revocable external API use
- visible local-only, local-network, external-assisted, and no-provider states when those modes exist
- explicit provider-visible data before prompts or context leave the machine
- no hidden provider residue
- fail-closed behavior when provider state is missing, denied, revoked, or privacy-blocked
- clear no-provider Assisted Desktop Mode

Provider recommendation is allowed when local capability is insufficient, but provider execution remains permission-gated.

## Capability Registry And Capability-Pack System

Capability packs are modular capability domains, not automatic model-weight bundles and not automatic FAMs.

Capability packs may include:

- tools
- retrieval/index layers
- knowledge provenance metadata
- versioned/updateable modules
- source/citation-aware stores
- confidence-aware domain behavior
- storage, VRAM, RAM, power, or hardware requirements
- license metadata
- integrity metadata
- update and removal metadata
- local-only or provider-assisted mode declarations

Capability records should declare:

- what the capability can do
- what it cannot do
- whether it is installed, available, enabled, denied, revoked, blocked, or missing hardware
- which sources it contains
- what data it may read or write
- what cache/index state it owns
- what provider or local-runtime state it requires
- what privacy/safety constraints apply

## AI Operational Cache Governance

Cache is not memory.

Cache is operational, purpose-bound, explainable, clearable, policy-governed state.

Memory is durable user-personal knowledge and requires separate explicit consent.

AI Operational Cache Governance is an architecture, policy, and runtime concern. It is not a new backlog family.

### Cache Ownership Split

- This file owns shared cache classes, replay safety, provenance, invalidation, and architecture/policy requirements.
- FAM-007 owns AI runtime/provider cache behavior, capability-pack cache manifests, deterministic/advisory cache behavior, and provider-cache sanitization.
- FAM-008 owns setup/install UX for cache roots, clear-cache flow, and user education.
- FAM-008 owns cache-root setup UX, storage-root selection, clear-cache education, and backup/export root guidance when packaging/setup work touches cache.
- Relevant implementing FAM visions own family-local data-root, evidence-path, privacy, Local-Only, Privacy Lockdown, and Trust Journal implications when their own work touches those surfaces.
- Active branch plans own implementation-specific cache behavior, proof, and rollback when cache work is admitted.

### Cache Scope Classes

| Scope Class | Description |
| --- | --- |
| Session cache | Temporary state needed only for the current interaction/session. |
| Operational cache | Short-lived operational state used to avoid recomputing safe local facts. |
| Deterministic validation cache | Cached objective tool results with strict input, provenance, permission, policy, and tool-version matching. |
| Advisory cache | Non-authoritative assistance state that requires freshness and confidence checks before reuse. |
| Provider-response cache | External-provider-derived material with sanitization, visibility, and retention limits. |
| Capability-pack index cache | Retrieval/index/cache data owned by capability packs. |
| Windows Health analysis cache | Diagnostic analysis state with confidence and freshness windows. |
| Temporary routine-context cache | Temporary routine/session context that expires or revalidates before sensitive reuse. |

### Cache Sensitivity Classes

| Sensitivity Class | Example | Required Posture |
| --- | --- | --- |
| Low | non-sensitive UI/session hints | clearable and bounded |
| Medium | Windows Health analysis cache | freshness, provenance, and journalable recovery |
| High | provider-derived summaries or user document-derived cache | provenance, retention limits, and privacy review |
| Very High | identity-sensitive, finance/email-adjacent, private path, or protected workflow cache | encryption expectation, local-only review, and explicit visibility |
| Critical | secrets, tokens, private owner memory, protected repo material | must not enter operational cache without a later explicit encrypted-vault policy |

### Cache Rules

Cache visibility should make operational cache categories understandable to users.

Cache provenance should record source, timestamp, provider/local mode, capability/tool owner, confidence basis, validity window, and whether the cache is deterministic, advisory, provider-derived, capability-pack-owned, or sensitive.

Cache invalidation should occur when source data, permission state, provider state, model version, tool version, capability-pack version, profile, privacy mode, Local-Only Mode, safety policy, or trust boundary changes.

Stale-cache detection must prevent old cache from silently powering objective answers, Windows Health recommendations, finance/email assistance, identity flows, provider-assisted summaries, safety-sensitive workflows, or recovery guidance.

Corruption recovery should detect, quarantine, rebuild, summarize, and journal cache recovery events rather than silently reusing damaged cache.

Deterministic cache and advisory cache must remain distinct. Deterministic validation cache may replay only when inputs, tool version, source provenance, permission state, and policy state still match. Advisory or provider-assisted cache must not replay as current truth without freshness and provenance checks.

Provider-cache sanitization should prevent private prompts, secrets, private paths, memory, identity data, sensitive logs, protected repo material, finance/email content, and private automation content from entering provider-facing cache unless a future USER-approved policy explicitly permits it.

Local-Only Mode should prohibit provider-cache reads/writes and hidden external cache dependencies.

Privacy Lockdown should suspend sensitive cache writes, block provider/cache egress, and make cache-block behavior visible.

The `clear all AI operational cache` flow should clear operational cache without pretending it deleted memory, Trust Journal entries, support logs, backups, or other separately governed records. The UX should explain what was cleared, what was not cleared, and which cache categories may rebuild later.

Trust Journal cache events should include sensitive cache writes, cache clears, stale-cache refusals, provider-cache use, privacy-lockdown blocks, local-only cache blocks, corruption recovery, replay/freshness decisions, and capability-pack cache rebuild/removal events.

## Trust Journal / AI Activity Journal

The Trust Journal should be plain-language, reviewable, and understandable by a non-technical user.

It should explain meaningful AI, provider, permission, cache, privacy, and safety events without becoming a noisy raw log.

Entry classes should include:

- capability access
- provider/network use
- permission-blocked attempt
- memory/index write or explicit no-write
- file/document access
- email/finance access
- routine action
- Windows Health recommendation
- restore/rollback action
- safety refusal
- competitive-integrity block
- privacy lockdown event
- cache writes, clears, stale-cache refusals, and corruption recovery

Trust Journal direction does not authorize telemetry, hidden monitoring, provider calls, memory, or runtime logging changes by itself.

## Routine And Daily Continuity Boundary

Routine and daily-continuity concepts are experience-layer and runtime-subsystem candidates by default, not new backlog families.

Routine states should include:

- `Suggested`
- `Previewed`
- `Approved`
- `Running`
- `Paused`
- `Completed`
- `Blocked`
- `Canceled`
- `Revised Pending Approval`

ORIN may recognize context and ask whether to begin a routine. It must not silently start sensitive or action-oriented routines without approval.

Routine classes such as Morning Routine, School Routine, Financial/Bill Routine, Gaming Routine, Focus Routine, Streaming Routine, Shutdown Routine, and Windows Health Routine require future Branch Readiness classification before implementation.

## Windows Health Recommendation Pipeline

Windows Health support should follow a conservative lifecycle:

1. Diagnose.
2. Recommend.
3. Prepare.
4. Request approval.
5. Execute only when approved and implemented.
6. Verify.
7. Summarize.
8. Log or journal the outcome where policy requires it.

Windows Health recommendations must separate observed evidence, inferred explanation, and uncertain hypothesis.

No Windows repair, system mutation, rollback, backup, installer, or support-bundle behavior is authorized by this architecture text.

## Competitive Integrity Layer

Competitive-integrity enforcement must sit below LLM/tool routing and block protected actions independent of prompt wording.

The system must not assist with hidden automation, anti-cheat bypass, game-memory manipulation, exploit tooling, recoil/aim assistance, botting, packet manipulation, protected-process tampering, or stealthy game advantage behavior.

When competitive-integrity policy blocks an action, the product should explain the block plainly and journal it when the Trust Journal policy requires it.

## Privacy Lockdown And Local-Only Guarantee

Privacy Lockdown should visibly block provider egress, sensitive cache writes, sensitive routine actions, identity-sensitive behavior, and any capability that cannot prove compliant local handling.

Local-Only Mode should be enforceable, not decorative. Provider calls, provider cache, provider-visible data, hidden external dependencies, and external fallback must be blocked while Local-Only Mode is active unless a later USER-approved exception is recorded.

## Identity Recognition Consent

Identity recognition must be consent-based only.

Identity-related capabilities require explicit permission state, clear revocation, visible disabled/degraded posture when denied, and separate handling from generic observation or interaction.

Identity memory is not approved by this document.

## Observation, Inference, And Confidence

Nexus should separate:

- directly observed evidence
- inferred explanation
- uncertain hypothesis

Confidence labels should include:

- `High confidence`
- `Likely`
- `Possible`
- `Uncertain`
- `Needs validation`

This distinction should inform user-facing explanations, Windows Health recommendations, deterministic routing, provider/tool routing, cache replay, and refusal behavior.

## Branch Readiness Requirements

Branches that propose AI-native architecture, provider/model behavior, cache, permission state, routines, daily continuity, Windows Health assistance, identity recognition, Trust Journal, capability packs, or competitive-integrity behavior must:

- run the `Backlog Taxonomy And Source-Truth Placement Gate`
- cite this file when the branch consumes cross-family AI runtime/trust architecture
- cite the relevant family vision owner
- ask USER-facing design questions before Workstream implementation when product behavior is ambiguous
- map planned elements through the Element-to-Phase Proof Matrix
- preserve the USER Branch Plan Review Gate before implementation
- record whether memory, provider execution, external API use, camera/microphone/desktop vision, installer behavior, backup behavior, or private edition work is included or explicitly excluded

## Explicit Non-Goals

This document does not approve:

- provider SDK integration
- model downloads or model execution
- external API calls
- persistent memory, learning, indexing, or personalization
- camera, microphone, desktop vision, or screen understanding
- voice/Core sync
- installer, shortcut, packaging, backup, restore, or release artifact work
- private Dev ORIN or Owner-private planning import
- runtime cache implementation
- Trust Journal implementation
- Windows Health mutation or repair
- gaming/process-sensitive runtime behavior
- release execution

Any such work requires later Branch Readiness, accepted branch vision, USER approval, implementation proof, and validation.
