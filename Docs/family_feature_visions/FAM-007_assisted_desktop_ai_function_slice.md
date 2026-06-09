# FAM-007 Assisted Desktop AI Function Slice Vision

## Purpose

This Family Feature Vision records durable direction for the FAM-007 Assisted Desktop AI function slice.

It sits below the broad FAM-007 Local AI and Capability Packs vision and above branch-specific Branch Vision review. It supplies reusable feature-category context for a product-bearing route that makes ORIN visibly useful in a no-provider posture without authorizing provider/model execution, private edition setup, downloads, memory, or hidden network behavior.

## Vision Basis

FAM: `FAM-007`

Package: `PKG-007`

Feature Category: `Assisted Desktop AI Function Slice`

Route Label: `Three-NDAI Assisted Desktop AI Function Slice`

Owning Context:

- `Docs/nexus_vision.md`
- `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`
- `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`
- `Docs/ai_runtime_and_trust_architecture.md`
- `Docs/family_visions/FAM-008_packaging_and_install_experience.md` for install and capability-pack setup boundaries

## Feature Purpose

This feature should make the Public Edition AI posture feel understandable and useful before any provider is connected. ORIN should no longer present AI as only unavailable or disabled when the base app still has deterministic local facts it can explain.

The user-facing goal is a local-only assisted desktop action that:

- shows the Public Edition AI / ORIN status as a visible product surface
- explains the provider state in plain language
- runs a deterministic no-provider result flow
- shows provider-visible data as `none`
- names safe local actions the user can take
- shows capability-pack eligibility without download or install execution
- preserves Developer lane and Owner lane boundaries as gated edition concepts

## User-Facing Surfaces

- ORIN AI status surface in the desktop visual layer.
- A clickable local assisted action tied to that status surface.
- A deterministic result view that states local capability, provider availability, data-sent posture, and safe follow-up actions.
- Capability-pack eligibility and blocked install-intent copy tied to the same result flow.
- Public Edition, Developer lane, and Owner lane boundary labels that do not expose private content or private setup behavior.

## Experience Flow

1. The user sees an AI / ORIN status surface rather than a hidden or inert provider block.
2. The user clicks a local assisted action.
3. Nexus reads only public-safe local app state and provider-boundary state.
4. The result explains that provider execution is unavailable, provider-visible data is `none`, and no prompt/model path ran.
5. The result names what the local app can do now, what capability packs could add later, and why install intent remains blocked.
6. Developer lane and Owner lane posture remains visible only as gated boundaries, not as private setup, private repository, or private asset behavior.

## Included Capabilities

- Visible Public Edition AI / ORIN status.
- Local-only clickable assisted desktop action.
- Deterministic no-provider result flow.
- Plain-language result text for local capability, provider unavailability, provider-visible data, and safe local follow-up.
- Capability-pack eligibility summary plus blocked install intent.
- Edition-boundary display for Public Edition, Developer lane, and Owner lane.
- Validator or fixture proof that the flow does not send prompts, call providers, download models, write memory, or hide network behavior.

## Explicit Non-Goals

- Provider SDK integration.
- Model execution.
- Prompt acceptance or prompt send.
- Model or capability-pack download.
- Capability-pack install, update, uninstall, or execution.
- External API calls or hidden network behavior.
- Persistent memory, indexing, learning, personalization, or real Owner memory.
- Real Owner agents.
- Private Developer or Owner repositories, roots, remotes, prompts, logs, memory, or assets.
- GitHub Desktop private binding.
- Public-to-Developer import.
- Backup or recovery execution.
- Voice/Core runtime sync.
- Shortcut, installer, packaging identity, or release artifact work.
- AI Product Contract import.
- Private Dev ORIN import.
- Issue mutation, PR creation, merge, release, or v1.8.0 execution.

## Dependency And Deferred Map

| Deferred Item | Owning Surface | Dependency Trigger | Grouping Recommendation | Proof Expectation | Durable Disposition |
| --- | --- | --- | --- | --- | --- |
| Provider/model execution | FAM-007 provider execution gate | USER approves provider/model execution scope, data boundary, cost/privacy posture, and rollback path | Separate provider execution carrier | Direct runtime and validator proof of approved provider-visible data | Later USER decision |
| Capability-pack install execution | FAM-007 plus FAM-008 setup/install owners | USER approves pack source, license, storage, integrity, and setup UX | Separate capability-pack/setup carrier | No hidden download, integrity proof, uninstall/reset proof | Later USER decision |
| Persistent memory or learning | FAM-007 memory gate | USER approves memory scope, retention, reset/export, and edition separation | Separate memory carrier | Consent, storage-boundary, reset/delete/export, and no hidden indexing proof | Later USER decision |
| Developer lane private setup | Edition trust-boundary plan | USER approves private Developer repository or local-only path | Separate private setup carrier | Private origin/public-upstream proof, secret scan posture, no Owner inheritance | Later USER decision |
| Owner lane private setup | Edition trust-boundary plan | USER approves private Owner repository or local-only path | Separate private setup carrier | Owner-private exclusion, path/hosting proof, no Public/Developer inheritance | Later USER decision |
| Packaging/install identity | FAM-008 | USER approves edition names, install paths, data roots, update channels, and setup UX | Separate packaging carrier | Installer/shortcut/source proof and distinct data-root proof | Later USER decision |

## Design Options

Option A - Status-only AI surface:
This would improve visibility, but it would still feel inert because the user could not ask the app to do anything useful inside the no-provider boundary.

Option B - Provider setup path:
This would be too broad for this feature category because provider/model execution, prompt send, data egress, credentials, and cost/privacy posture require later USER gates.

Option C - Local-only assisted desktop action:
This is the recommended product direction. It creates a useful, clickable, deterministic no-provider flow while preserving all private/provider/runtime/memory/install gates.

## Proof Expectations

- The AI / ORIN status surface is visible in the Public Edition desktop surface.
- The local assisted action is clickable and produces a deterministic result.
- The result includes local capability, provider unavailable/degraded posture, provider-visible data `none`, and safe next actions.
- Capability-pack eligibility and blocked install intent appear in the same flow.
- Developer lane and Owner lane labels do not expose private content or private setup behavior.
- Provider/model execution remains disabled.
- Prompt acceptance and prompt send remain disabled.
- Downloads, installs, external calls, memory writes, cache behavior, real Owner memory, and real agents remain blocked.
- Validation includes static contract proof plus UI/result-flow proof once implementation begins.

## Branch Readiness Consumption Notes

Feature Vision Sufficiency Check: `PASS`

Sufficiency Basis: This file defines purpose, surfaces, flow, included capability, non-goals, deferred map, design options, proof expectations, and branch-planning consumption notes for the Assisted Desktop AI function slice.

BP1 Feature Vision Context: Branch Vision review should cite this file and decide the exact Public Edition status wording, local action label, result layout, and capability-pack eligibility copy before Workstream implementation.

BP2 Carryforward: Engineering planning should keep the route grouped when the Public Edition surface, local result flow, edition boundaries, and capability-pack eligibility proof share the same validation path.

BP3 Carryforward: Orchestration review should verify that every deferred item is excluded for the stated reason or routed to the correct later owner.

## Fold-Down Notes

Reusable product standards accepted through later review should fold into this file or the owning broad FAM-007 vision when they outgrow branch-local planning. Branch-specific implementation details, file checklists, live validation evidence, and review packet state belong to the external branch plan, branch receipt, workstream evidence, helper output, or Git/GitHub-derived proof.
