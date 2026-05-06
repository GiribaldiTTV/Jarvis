# Nexus Pre-Beta Rebaseline Through v1.3.0-prebeta

## Purpose

This document is the modern Nexus-era rebaseline through `v1.3.0-prebeta`.

Its job is to:

- summarize the current shared pre-Beta baseline
- capture what is locked versus deferred
- reduce prompt bloat by replacing repeated lane recaps
- point back to preserved historical closeouts without rewriting them

## Baseline Scope

This rebaseline covers merged shared truth through the released public prerelease:

- `v1.3.0-prebeta`

It stands on top of the preserved historical closeout line indexed in:

- `Docs/closeout_index.md`

## Material Closed Workstreams In This Baseline

The closed workstreams that materially define the current baseline are:

- `Docs/workstreams/FB-028_history_state_relocation.md`
- `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`
- `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`
- `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
- `Docs/workstreams/FB-027_interaction_system_baseline.md`
- `Docs/workstreams/FB-036_saved_action_authoring.md`

## What Is Locked Now

Through `v1.3.0-prebeta`, current shared truth includes:

- launcher-owned historical state is not a live root-logs surface
- the startup snapshot harness is a bounded dev-only and opt-in debugging surface
- boot and desktop milestone taxonomy remains clarified without collapsing ownership boundaries
- one recoverable-operational-incident class is closed and shipped:
  - repeated identical `launch_failed` for the same action in a still-running session
- support-report fallback now derives release context from released-canon truth instead of the highest planned prerelease target
- the manual-reporting boundary remains local and manual only
- the typed-first desktop interaction baseline is explicit and validator-defended
- built-in actions and saved actions resolve through one shared action catalog
- the first bounded interaction capability milestone is released:
  - first-class URL target support for saved actions without changing exact-match resolution, state-machine boundedness, or input-capture behavior
- the later bounded FB-027 follow-through is also released:
  - saved-action inventory and guided access
  - built-in-vs-saved distinction in choose and confirm
  - saved-source health visibility for missing, invalid, template-only, and colliding states
  - directly coupled validator expansion for inventory, origin, and source-state visibility
- the released FB-036 milestone is now also part of the locked shared pre-Beta baseline:
  - bounded custom-task create, edit, and delete flows
  - explicit trigger modeling with alias-root invocation for newly created tasks
  - bounded callable-group create, manage, and exact invocation
  - bounded single-group assignment and inline group quick-create
  - immediate catalog reload and fail-closed malformed-source blocking for authoring paths
  - final exact-green interactive proof plus launched-process UI audit for the released authoring baseline

## What Remains Deferred

This rebaseline does not authorize automatic continuation into:

- curated built-in system actions and Nexus settings expansion
- taskbar or tray quick-task entry surfaces
- external trigger and plugin integration architecture
- monitoring, thermal, or performance HUD surfaces
- scheduling, branching, or multi-step execution logic for callable groups
- Action Studio behavior
- voice invocation
- shutdown exit-confirmation work
- hotkey cleanup before Beta
- broader reporting-policy or upload-behavior work
- broader boot-layer implementation work
- broader interaction, rebrand, voice, or UI follow-through by inertia

## Forward-Planning Posture After This Baseline

Current merged truth is again between released non-doc implementation lanes.

The next implementation workstream must be chosen from refreshed backlog, workstream, product-boundary, and release truth on updated `main` rather than by continuing FB-027 or FB-036 by inertia.

## Historical Relationship

The preserved historical Nexus closeout line remains valid historical context.

Use:

- `Docs/closeout_guidance.md` for closeout and rebaseline policy
- `Docs/closeout_index.md` for historical closeout lookup

This document does not rewrite those historical closeouts.

## Carry-Forward Rule

Future prompts should usually treat this rebaseline plus the retained workstream records as the modern carry-forward baseline through `v1.3.0-prebeta` instead of replaying each closed lane narrative in full.
