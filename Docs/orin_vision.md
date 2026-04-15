# Nexus / ORIN Vision

## Purpose

This document defines product intent for Nexus Desktop AI and the ORIN assistant layer.

It does not own:

- workstream closure
- backlog identity
- roadmap sequencing

Use it for product direction, experience intent, and release-stage meaning.

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
- post-Beta grouping/query ideas should not be used to weaken command predictability in the current release

## Trust And Recovery Posture

Nexus should eventually present trust, recovery, and post-login continuity as one coherent experience layer, but the repo is not there yet.

Current merged truth should still be read as:

- desktop orchestration first
- future boot and access planning deferred
- product trust and resident presence concepts still living at planning level

## Historical Relationship

The public Nexus release line begins after the preserved Jarvis historical release line.

That means:

- older Jarvis releases remain preserved as historical records
- they do not define the active public Nexus release line
- current vision and current release posture should be expressed in Nexus / ORIN terms unless a section is explicitly historical

## Relationship To Other Canon Layers

- use `Docs/architecture.md` for architectural boundaries
- use `Docs/orchestration.md` for orchestration behavior and runtime ownership
- use `Docs/boot_access_design.md` for future boot-access planning
- use `Docs/prebeta_roadmap.md` for sequencing and release posture
- use `Docs/workstreams/...` for promoted workstream history
