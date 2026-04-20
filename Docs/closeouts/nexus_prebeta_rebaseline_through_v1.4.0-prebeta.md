# Nexus Pre-Beta Rebaseline Through v1.4.0-prebeta

## Status

This file is the active Nexus-era rebaseline for `v1.4.0-prebeta` after FB-037 release execution.

It supersedes `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.3.1-prebeta.md` as the current baseline.

## Purpose

This rebaseline captures the modern Nexus-era baseline after FB-037 release packaging is executed.

Its job is to:

- summarize the shared pre-Beta baseline through `v1.4.0-prebeta`
- capture what is locked by the FB-037 built-in catalog milestone
- preserve what remains deferred after the release
- reduce future prompt bloat after the public prerelease exists

## Baseline Scope

This rebaseline covers shared truth through the public prerelease:

- `v1.4.0-prebeta`

It will stand on top of the preserved historical closeout line indexed in:

- `Docs/closeout_index.md`

## Material Closed Workstreams In This Baseline

The closed workstreams that materially define this baseline are:

- `Docs/workstreams/FB-028_history_state_relocation.md`
- `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`
- `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`
- `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
- `Docs/workstreams/FB-027_interaction_system_baseline.md`
- `Docs/workstreams/FB-036_saved_action_authoring.md`
- `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md`
- `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`

## What Is Locked By v1.4.0-prebeta

The shared pre-Beta baseline includes all `v1.3.1-prebeta` locked truth plus the FB-037 built-in catalog milestone:

- the typed-first desktop interaction baseline remains explicit and validator-defended
- built-in actions and saved actions continue to resolve through one shared action catalog
- saved-action override authority remains intact when a saved action collides with a built-in phrase
- authoring collision protection prevents create/edit paths from silently overriding built-in phrases
- the curated built-in catalog includes first-class Windows utility actions for:
  - Task Manager
  - Calculator
  - Notepad
  - Paint
- built-in catalog entries use the existing `app` target path and do not introduce new target kinds
- built-in execution preserves the existing confirm and result surfaces
- callable-group behavior from the released FB-041 baseline remains unchanged
- reusable live-validation helper hardening remains available as branch-local proof support for future desktop validation work

## What Remains Deferred

This rebaseline does not authorize automatic continuation into:

- Nexus settings or protocol actions
- new built-in target kinds
- shell arguments or launcher-policy changes
- taskbar or tray quick-task entry surfaces
- Create Custom Task shell-facing UX
- external trigger or plugin integration architecture
- monitoring, thermal, or performance HUD surfaces
- scheduling, branching, or multi-step orchestration beyond released deterministic stored-order callable-group execution
- nested callable groups
- parallel callable-group execution
- retries
- Action Studio behavior
- voice invocation
- shutdown exit-confirmation work
- hotkey cleanup before Beta
- broader reporting-policy or upload-behavior work
- broader boot-layer implementation work
- broader interaction, rebrand, voice, or UI follow-through by inertia

## Forward-Planning Posture After Release

After release execution:

- FB-037 is `Released (v1.4.0-prebeta)` and `Closed`
- `Release Debt` for FB-037 is cleared
- FB-038 remains selected in canon only until a fresh Branch Readiness admission from updated `main`
- no FB-038 branch should exist before that Branch Readiness admission
- future implementation must enter through the strict branch-governance admission flow

## Historical Relationship

The preserved historical Jarvis closeout line remains valid historical context.

Use:

- `Docs/closeout_guidance.md` for closeout and rebaseline policy
- `Docs/closeout_index.md` for historical closeout lookup

This rebaseline does not rewrite historical closeouts.

## Carry-Forward Rule

Future prompts should treat this rebaseline plus the retained workstream records as the modern carry-forward baseline through `v1.4.0-prebeta`.
