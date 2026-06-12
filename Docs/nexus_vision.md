# Nexus Vision Contract

## Purpose

This document is the project-wide product vision contract for Nexus Desktop AI and the ORIN assistant layer.

It does not own:

- workstream closure
- backlog identity
- roadmap sequencing
- phase governance, proof ownership, or validation stop-loss rules
- family-specific implementation detail
- active external branch execution plans

Use it for product direction, experience intent, and release-stage meaning.

Family-specific vision records live under `Docs/family_visions/` when a broad feature family needs durable USER-reviewed product direction. USER-approved Family Feature Vision records, when created under the recommended `Docs/family_feature_visions/` pattern, own durable feature-category direction inside one family between Family Vision and active Branch Vision. The preferred durable FFV model uses compact IDs such as `F7-FF01` and element IDs such as `F7-FF01-E01`, with human-readable category titles inside the file and index. Selected feature-bearing branch routes require the relevant Family Feature Vision before BP1 unless the route is non-product and records `Family Feature Vision Not Applicable`; shallow, slice-specific, branch-route-specific, or pointer-stale feature-vision files do not satisfy BP1. Active external branch plans under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` own the Branch Vision Contract Snapshot and implementation checklist for the current branch only; repo branch-plan files are historical receipts after fold-down.

Edition-specific AI deployment planning lives in `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`. That plan records the public-safe Owner / Dev / Public edition capability model, private-repo separation, Public-to-Dev migration direction, GitHub Desktop setup guidance, and release breakpoints without authorizing runtime AI, provider/model execution, memory, packaging, licensing, or private repo implementation.

## Vision Ownership Chain

Project Vision, Family Vision, Family Feature Vision, and Branch Vision are separate source-truth layers.

The required carrydown chain is:

```text
Project Vision -> Family Vision -> Family Feature Vision -> Branch Vision Contract Snapshot -> BP2/BP3 engineering plan -> Workstream/Hardening/Live Validation proof
```

Each lower layer must consume and specialize the layer above it. It must not replace the higher-level owner, duplicate broad principles by copy/paste, or invent missing durable feature direction when the correct owner is absent.

Layer ownership:

- `Docs/nexus_vision.md` owns project-wide product direction, experience intent, Project UI Vision, release-stage meaning, and durable product standards that apply across families.
- `Docs/family_visions/` owns broad durable product direction for one FAM, including family-specific UI/interaction carrydown from the Project Vision.
- `Docs/family_visions/FAM-002_desktop_interface.md` owns reusable Desktop Interface presentation standards that other FAMs normally consume when implementing their own user-facing surfaces; consuming FAMs still own their feature behavior, feature-specific UI implementation, and proof path.
- USER-approved `Docs/family_feature_visions/` records, once created, own detailed durable feature-category direction inside one FAM, including deferred carryforward and feature-specific proof expectations.
- The active external branch plan owns the Branch Vision Contract Snapshot and branch-local implementation choices after USER acceptance or waiver.
- BP1 consumes the vision chain and turns it into a branch-specific USER review contract.
- BP2 and BP3 translate the accepted or waived BP1 contract into engineering, orchestration, proof, rollback, and validation plans.
- Workstream, Hardening, Live Validation, PR Readiness, and Release Readiness must compare claims against the accepted vision chain instead of treating validator output, screenshots, logs, or branch-local prose as product truth by themselves.

Backlog and roadmap files are compact registry, sequencing, and pointer layers. They may point to the vision owners, but they do not own full durable product vision narrative or active Branch Vision state.

## Core Product Goal

Nexus Desktop AI should eventually feel like the system-facing experience layer, not just a normal desktop app launched after Windows.

The long-term direction is:

Windows boots
-> Nexus startup and orchestration begins
-> ORIN becomes the primary visible assistant experience
-> Windows remains the underlying host platform

## Current Reality

The current merged runtime is still a controlled desktop orchestration path:

`launch_orin_desktop.vbs`
-> `desktop/orin_desktop_launcher.pyw`
-> `desktop/orin_desktop_main.py`

That path is foundation work.
It stabilizes startup, recovery, diagnostics, and lifecycle behavior.
It is not yet the final boot-first product experience.

FAM-001 owns fatal launcher/runtime diagnostics and recovery surfaces for the current product. Feature-owning FAMs may expose their own degraded, blocked, unavailable, or recoverable states, but they consume the FAM-001 failure/recovery boundary when launcher/runtime recovery, crash diagnostics, support-bundle preparation, manual issue reporting, retry/close/repair choices, startup abort, or recovery exhaustion is involved. The released FB-034 recoverable `launch_failed` path is historical evidence for one bounded non-crashing incident class, not a live backlog owner for new diagnostics scope.

## Experience Intent

The experience should trend toward:

- Windows as infrastructure
- Nexus Desktop AI as the visible experience layer
- ORIN as the assistant presence that gives the product identity

The product should not feel like:

- Windows as the experience and Nexus as a small overlay
- a generic utility app running on top of the desktop

## Product Principles

Nexus Desktop AI should feel:

- system-facing
- intentional
- calm under normal use
- explicit when trust or recovery posture changes
- recoverable rather than opaque

The system should not rely on:

- hidden state
- unexplained automation
- accidental authority drift between launcher, renderer, planning docs, and user-facing reporting

## Project UI Vision

Nexus UI should feel comfortable, reliable, futuristic, and understandable at the same time. It should make the user feel that the system is capable and alive without becoming noisy, cryptic, or fragile.

Durable UI principles:

- comfort: normal operation should feel calm, readable, and safe to leave open for long sessions
- reliability: surfaces should expose state, failures, disabled paths, and recovery options plainly instead of hiding uncertainty
- futuristic feel: the UI should look intentional and Nexus-native, but visual ambition must not reduce clarity, accessibility, or task completion
- understandable interaction: controls, status labels, and assistant messages should explain what they do, what they changed, and what remains blocked
- consistency: similar actions such as Close, Open, Save, Start, Stop, Select Folder, Clear, Retry, and Export should use consistent placement, labels, affordances, and disabled/degraded states unless BP1/BP2/BP3 accepts a deliberate product-wide exception
- fail-proof behavior: risky actions should be reversible, confirmed when needed, recoverable, or safely disabled until their prerequisites are proven
- readability: layout density, contrast, typography, spacing, and state hierarchy should keep operator-facing information legible under normal desktop use
- versatility and changeability: future configuration, skins, layouts, modes, and edition-specific behavior are valid product goals, but they must be introduced through governed vision/plan/proof layers rather than ad hoc branch styling
- standard control language: families may specialize controls for their surface, but they should inherit the project-wide control grammar before creating unique widgets, button families, folder pickers, or start/stop flows

Family Vision records carry these principles by reference and specialize them only where the FAM has a real product reason. Family Feature Vision records specialize them further for one durable feature category. Branch Vision, BP2, BP3, Workstream, Hardening, and Live Validation must preserve the accepted UI carrydown or record the exact USER-approved exception and proof path.

### Vision Contract Product Detail Quality Bar

Vision contracts are product contracts, not filing instructions. Project Vision, Family Vision, Family Feature Vision, and Branch Vision layers must describe the actual Nexus product outcome, user experience, visible surfaces, trust/recovery behavior, visual standards, interaction model, proof expectations, and non-goals that future work must honor.

A durable vision layer is weak when it only says what the file is for, lists where work should be routed, repeats governance procedure, or says future branches should define the product later. Procedure may appear as compact owner routing, but the durable value of a vision file is the product/design detail it preserves.

Required product-detail anchors for vision work:

- user-visible outcome and end-state experience
- Nexus fit and family/feature purpose
- surfaces, windows, controls, status states, and interaction flow when visible UI is involved
- trust, privacy, failure, recovery, disabled, blocked, or unavailable states when the feature can affect user confidence
- standard control language and visual inheritance expectations
- explicit non-goals and future-gated boundaries
- proof expectations that can later be tested without letting helper output replace product judgment

Invalid vision-only content includes placeholder descriptions, copied source-file lists, branch-local implementation steps without product meaning, SLC/slice/seam labels as the product vision, or "define later" wording for a required product decision. If a lower vision layer discovers durable product detail that the higher layer must own, the branch must route the new fact to the correct vision owner or record a durable deferred disposition before advancing.

### NDAI UI Immersion And Window Chrome Standard

Every Nexus-owned product window, panel, dashboard, studio, command center, settings surface, tray-opened surface, diagnostics surface, and proof-visible user interface should feel like part of Nexus Desktop AI rather than a generic Windows utility.

Nexus-owned product windows must use admitted Nexus / NDAI window presentation: custom product framing or chrome, Nexus control grammar, consistent close/minimize/back/settings affordances, coherent title/header treatment, rounded or intentionally shaped frame behavior where applicable, matching card/button/list/scrollbar style, and visual hierarchy that matches the Project UI Vision and FAM-002 presentation standards.

Surface classification:

- `Nexus-Owned Product Surface`: a window, panel, dashboard, studio, command center, settings surface, tray-opened surface, diagnostics/recovery panel, proof-visible user interface, or persistent/transient product control that Nexus owns and the USER experiences as part of NDAI.
- `Platform-Native Exception`: an OS, browser, provider, installer, permission, file/folder picker, authentication, or platform-trust surface where native chrome is required or more trustworthy than custom chrome.
- `Diagnostic / Developer Surface`: a temporary or explicit troubleshooting/proof surface that is not presented as the normal product UI.
- `External Surface`: a provider, browser, OS, GitHub, or third-party UI surface that Nexus can open or route to but does not visually own.

Default Windows title bars, unstyled native utility windows, generic dialog shells, mismatched button families, and platform-looking popups are invalid for final `Nexus-Owned Product Surface` surfaces unless the branch records an approved platform exception and proof path. Allowed exception candidates include OS file pickers, OS security/permission prompts, installer or update surfaces that must use platform trust affordances, browser/provider-auth surfaces, or temporary troubleshooting-only diagnostics that are explicitly not the product UI. Even then, BP1/BP2/BP3 and Live Validation must classify the exception and prove it is deliberate rather than accidental drift.

FAM-002 is the shared Desktop Interface presentation authority, not the sole owner of every user-facing UI implementation. A consuming FAM branch may implement FAM-002-aligned UI work when that UI is necessary to complete the consuming FAM's accepted Family Vision, Family Feature Vision, Branch Vision Contract Snapshot, BP2/BP3 plan, and proof path. Project Vision owns the global UI principles; FAM-002 owns reusable presentation contracts and control hierarchy; each FAM owns the UI/UX of its own feature behavior; each FFV owns the concrete surface, user flow, and proof expectations for its feature category.

## Runtime Observability And USER Proof

Nexus Desktop AI should be observable enough to prove user-facing behavior without becoming a hidden diagnostic collector.

Durable product direction:

- normal desktop runtime mode is the default USER launch profile
- troubleshooting runtime mode is an explicit USER-consented diagnostic profile
- normal runtime mode should produce only minimal, privacy-safe product logs needed for reliability, recovery, and basic local troubleshooting
- troubleshooting mode should be temporary or scoped, locally stored by default, privacy-safe/redacted where needed, and visibly distinct from normal runtime
- elevated diagnostic logging, Dev Toolkit inspection, provider-visible data, support bundles, or exported evidence must not be enabled silently
- product UI should present client-like product folders and labels; it should not expose worktree, branch, FAM, developer, owner-only, or internal implementation paths unless a source-truth owner explicitly admits that product-facing concept
- developer/proof/evidence paths may use worktree, branch, FAM, or validation-lane labels only when they are clearly developer or validation evidence, not product UI
- branches that create runtime/user-facing behavior must classify fatal, recoverable, degraded, blocked, disabled/deferred, and unavailable-prerequisite behavior through the Runtime Failure / Recovery Carrydown Gate in `Docs/phase_governance.md` before treating the feature as closeout-ready

Formal user-facing proof has a stricter bar than internal diagnosis:

- a visible or user-facing behavior claim is closeout-grade only when proved through photo, video, or ordered frame-sequence evidence from the relevant USER-facing runtime path
- runtime logs, markers, manifests, helper output, and Dev Toolkit events are supporting evidence for diagnosis and consistency; they do not replace photo/video proof for visible USER-facing acceptance
- if a required claim cannot be proved in photo/video, Codex must elevate that claim to USER manual validation, explicit USER waiver, or a named blocker instead of calling it proven
- formal Live Validation for desktop/user-facing behavior must use the exact normal USER desktop runtime launcher path declared for the branch unless a launcher parity proof and USER approval allow the troubleshooting runtime launcher to serve as equivalent proof for that exact claim

Future two-launcher model:

- `Normal Desktop Runtime Launcher`: starts normal NDAI for ordinary USER operation and owns default formal Live Validation proof
- `Troubleshooting Runtime Launcher`: starts NDAI in troubleshooting mode for consented diagnostics, validation, or support
- `Launcher Parity Proof`: proves both launchers start the same product runtime/build, use the same product data roots and user-visible behavior, and differ only by admitted diagnostic flags, diagnostic evidence roots, log level, and troubleshooting disclosure
- if launcher parity is missing, fails, or the claim being validated could be affected by troubleshooting-mode differences, Live Validation must use the normal USER desktop runtime launcher or stop for USER waiver/manual validation

## AI-Native Operating Experience

Nexus should become an AI-native operating experience layer without pretending that provider/model fluency is the same thing as system reliability.

The durable direction is:

- Windows remains the host platform
- Nexus becomes the visible experience layer
- ORIN remains the persistent cooperative assistant identity
- providers, models, and capability packs are replaceable extensions, not the product identity
- objective and safety-sensitive answers prefer deterministic, tool-backed, or validation-backed paths before generative improvisation
- AI state, provider state, permission state, cache state, privacy state, and refusal/uncertainty posture should be visible in plain language when they matter
- trust UX should be calm, explainable, reversible, and understandable to non-technical users

Cross-family AI architecture, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, routine/continuity boundaries, competitive-integrity boundaries, and capability-pack architecture live in `Docs/ai_runtime_and_trust_architecture.md`.

Family-specific direction remains with the family visions. Active branches still require Branch Readiness, accepted branch vision, USER Branch Plan Review, implementation approval, and validation before runtime AI, provider/model work, memory, cache implementation, camera/microphone/desktop vision, installer behavior, or release work can begin.

## Release-Stage Meaning

Across the product:

- `pre-Beta` means architecture, runtime boundaries, validation, and internal product shape are still stabilizing
- `Beta` means the product is coherent enough for broader user-facing evaluation and setup expectations
- `Full` means the product has crossed from staged system foundation into mature product delivery

This means the repo may contain meaningful `pre-Beta` implementation progress without claiming Beta readiness.

## Future Boot Preference Model

Before `Beta`, the Boot portion of Nexus Desktop AI should become a user-controlled preference rather than an assumed always-on behavior.

That future model should mean:

- the user can intentionally enable or disable the Boot experience
- if setup requires Windows login, startup, or boot-configuration changes, the product should guide the user through that setup
- the current desktop runtime path remains valid even when future boot-facing work is deferred

## Future Grouping Direction

Callable groups can be a valid part of the bounded pre-Beta command surface when they stay explicit, exact-match, and member-driven.

Post-Beta expansion may explore richer grouping behavior such as:

- dynamic natural-language grouping requests
- group discovery or query flows like "show me all tasks associated with..."
- broader organizational or recommendation layers above exact callable aliases

That expansion should remain deferred until after the current exact-match callable-group model is proven.

Current vision boundary:

- pre-Beta callable groups should stay explicit and exact-match
- shipped built-in task grouping/taxonomy should stay deferred until the explicit callable-group model is proven and a stable default group strategy exists
- post-Beta grouping/query ideas should not be used to weaken command predictability in the current release

## Trust And Recovery Posture

Nexus should eventually present trust, recovery, and post-login continuity as one coherent experience layer, but the repo is not there yet.

Current merged truth should still be read as:

- desktop orchestration first
- future boot and access planning deferred
- product trust and resident presence concepts still living at planning level

## Resident Access And Privacy Visibility

Nexus should eventually expose a resident access surface that feels like a doorway into the system-facing assistant experience, not a replacement for the full Dashboard, Settings, NCP, or AI Command Center.

Durable direction:

- the primary resident entry should be one Nexus Desktop AI tray icon by default
- the tray icon should provide compact status and route the USER to the right full surface instead of becoming a deep command wall
- privacy-critical AI/provider/permission/cache state should not depend only on Windows tray visibility, because Windows can hide third-party tray icons
- privacy-critical state should also be visible through a Nexus status panel, HUD/status surface, AI Command Center, or equivalent USER-facing surface when those owners are implemented
- USER-configurable quick-access slots are valid, but immutable privacy and control entries should remain easy to find
- future second-icon AI status behavior remains USER-gated and should be justified only if one icon plus status surfaces cannot communicate privacy state safely

The durable feature-category owner is `Docs/family_feature_visions/F3-FF01.md`. FAM-003 owns resident access and quick-action interaction; FAM-002 owns visual presentation; FAM-006 owns Monitoring/HUD, Recording Studio, and Log Viewer surfaces; FAM-007 plus `Docs/ai_runtime_and_trust_architecture.md` own AI/provider/privacy status truth; FAM-008 owns installer/setup education for tray visibility and startup behavior.

## Local AI And Capability-Pack Vision

This section records public-safe FAM-007 local AI and capability-pack direction.

It is product intent and planning truth only.
It does not admit implementation, local models, provider runtime code, memory/indexing, voice/Core sync, setup behavior, or release work by itself.
The USER-provided `Nexus AI Product Contract v0.6.2` is planning evidence for this direction, not repo source truth and not a full imported contract.

`PKG-007` package/slice admission, when recorded by the active FAM-007 Branch Readiness Stage 2 authority, is source-truth readiness only and does not authorize runtime implementation.

FAM-007 should be staged so the base app remains useful without a local LLM and heavy local AI remains optional capability-pack work rather than default installer bloat.

### AI Behavior Goals

- responses should feel organic and dynamic without becoming vague or improvisational
- reasoning should feel smart and practical while staying inside explicit system constraints
- the assistant should stay lightweight enough to feel responsive on normal hardware
- the interaction model should be approachable for everyday use while still supporting deeper reasoning when needed
- conversational behavior should remain grounded, predictable, and easy to trust

### Capability Boundaries

- common everyday queries should be handled locally where practical
- the local system should avoid heavy or expensive workloads that do not fit the machine or the release stage
- external deferral is acceptable when computation is too large, storage or model footprint is impractical, or an outside system is the better execution surface
- when deferral happens, the system should say so clearly rather than hiding the boundary
- no-provider behavior should degrade into an Assisted Desktop Mode rather than feeling broken
- provider choice should not replace ORIN/ARIA as the user-facing assistant layer

### Privacy Model

- privacy-first defaults are non-negotiable
- retain as little user data as practical and avoid unnecessary persistence
- avoid third-party monitoring or exposure where a local or first-party path can satisfy the need
- user trust, visibility, and local control are primary design constraints
- Local Only, Local Network, External API, and No AI Provider states should be visible when those modes exist
- external API use should be opt-in, revocable, and cost/privacy-aware

### Execution Model

- the intended direction is hybrid and local-first
- local logic should handle common tasks, routing, and assistant orchestration
- external fallback should remain optional and reserved for queries that exceed reasonable local capability
- even when external help is used, the product should still feel like a local system extension rather than a thin client for a remote dependency
- provider boundaries should be defined before implementation so local, LAN, external API, and test providers can be swapped without changing the ORIN-facing product shell
- hardware safety, power state, thermals, and model/capability-pack requirements should gate what the user can enable on a given machine

### Technology Exploration

- Python is the primary exploration path for orchestration and rapid iteration
- C++ is a candidate path for performance-critical components
- GPU acceleration is preferred where officially supported and validated; NVIDIA CUDA, AMD-supported paths, Windows DirectML / Windows ML / ONNX Runtime, and CPU fallback should be considered by capability and maintenance cost
- Java and C# remain open integration paths where platform or tooling fit warrants them
- this is exploration space, not a locked implementation stack

### Visual Identity Principles

- the UI should read as a direct extension of the assistant rather than as a separate utility wrapped around it
- the visual layer should represent AI state, handoff state, and boundary changes clearly
- AI behavior and UI feedback should stay aligned so the product feels coherent rather than split into "assistant" and "tool"

### Explicit Non-Goals For Current Release

- do not treat this section as current implementation truth
- do not introduce large local models or heavy local inference in the current release
- do not admit FAM-007 implementation without a later Branch Readiness revalidation and explicit USER approval
- do not mark `PKG-007` or its slices as `Admitted` from vision text alone; admission requires the active branch authority and USER approval
- do not import private/internal-only planning wholesale into public source truth
- do not mutate or repurpose the parked `codex/ai-llm-lab` branch by inertia
- do not reinterpret current workstream, validation, or release-posture docs through this future section

### Public-Safe Planning Carry-Forward

The first FAM-007 package should likely be a foundation package, not a full assistant implementation.

Public-safe planning principles to carry forward:

- define Assisted Desktop Mode and no-provider behavior first
- preserve the Edition Capability / Trust Boundary model in `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md` before implementing provider/model/runtime work
- define provider boundaries before tying ORIN to any model, runtime, or vendor
- define visible privacy/provider state before any external call path exists
- define hardware, power, and performance safeguards before enabling local heavy workloads
- define model/capability-pack license, integrity, disk-space, and update migration rules before distribution
- define data classification, memory, context packing, consent, audit, secrets, and trust reset before indexing or learning work
- keep Windows compatibility and safe repair paths first-class
- keep Boot-Facing Mode and secure sign-in work future/high-risk
- keep full internal Dev ORIN/private prompt/eval/beta-feedback tooling outside public repo truth unless later sanitized and approved

## Historical Relationship

The public Nexus release line begins after the preserved Nexus historical release line.

That means:

- older Nexus releases remain preserved as historical records
- they do not define the active public Nexus release line
- current vision and current release posture should be expressed in Nexus / ORIN terms unless a section is explicitly historical

## Relationship To Other Canon Layers

- use `Docs/architecture.md` for architectural boundaries
- use `Docs/ai_runtime_and_trust_architecture.md` for cross-family AI runtime/trust architecture, AI operational cache governance, permission-state, deterministic routing, Trust Journal, and capability-pack architecture
- use `Docs/phase_governance.md` for governed execution phases, proof authority, and closeout discipline
- use `Docs/orchestration.md` for orchestration behavior and runtime ownership
- use `Docs/boot_access_design.md` for future boot-access planning
- use `Docs/prebeta_roadmap.md` for sequencing and release posture
- use `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md` for public-safe Owner / Dev / Public edition boundaries and release breakpoints
- use USER-approved Family Feature Vision records under the recommended `Docs/family_feature_visions/` compact-ID pattern for durable feature-category direction and deferred carryforward inside one family when Family Vision is too broad and active branch planning is too branch-local; selected feature-bearing branch routes require this layer before BP1 when source truth says the feature category needs durable middle vision detail
- use `Docs/workstreams/...` for promoted workstream history
