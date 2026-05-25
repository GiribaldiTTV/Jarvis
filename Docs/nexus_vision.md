# Nexus Vision Contract

## Purpose

This document is the project-wide product vision contract for Nexus Desktop AI and the ORIN assistant layer.

It does not own:

- workstream closure
- backlog identity
- roadmap sequencing
- phase governance, proof ownership, or validation stop-loss rules
- family-specific implementation detail
- active branch execution plans

Use it for product direction, experience intent, and release-stage meaning.

Family-specific vision records live under `Docs/family_visions/` when a broad feature family needs durable USER-reviewed product direction. Active branch plans still own the Branch Vision Contract Snapshot and implementation checklist for the current branch only.

Edition-specific AI deployment planning lives in `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`. That plan records the public-safe Owner / Dev / Public edition capability model, private-repo separation, Public-to-Dev migration direction, GitHub Desktop setup guidance, and release breakpoints without authorizing runtime AI, provider/model execution, memory, packaging, licensing, or private repo implementation.

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
- use `Docs/phase_governance.md` for governed execution phases, proof authority, and closeout discipline
- use `Docs/orchestration.md` for orchestration behavior and runtime ownership
- use `Docs/boot_access_design.md` for future boot-access planning
- use `Docs/prebeta_roadmap.md` for sequencing and release posture
- use `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md` for public-safe Owner / Dev / Public edition boundaries and release breakpoints
- use `Docs/workstreams/...` for promoted workstream history
