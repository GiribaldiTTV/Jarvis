# Draft Nexus Pre-Beta Rebaseline Through v1.4.0-prebeta

## Draft Status

This file is a release-packaging draft for `v1.4.0-prebeta`.

It is not the active current Nexus-era baseline until all of the following are true:

- the `v1.4.0-prebeta` tag exists
- release execution has marked FB-037 released
- `Docs/closeout_index.md` points to this file as the current baseline
- `Docs/prebeta_roadmap.md` records `v1.4.0-prebeta` as the latest public prerelease

Until then, `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.3.1-prebeta.md` remains the current released baseline.

## Purpose

This draft prepares the modern Nexus-era rebaseline that will become active after FB-037 release packaging is executed.

Its job is to:

- summarize the planned shared pre-Beta baseline through `v1.4.0-prebeta`
- capture what becomes locked by the FB-037 built-in catalog milestone
- preserve what remains deferred after the release
- reduce future prompt bloat after the public prerelease exists

## Baseline Scope

When released, this rebaseline will cover shared truth through the public prerelease:

- `v1.4.0-prebeta`

It will stand on top of the preserved historical closeout line indexed in:

- `Docs/closeout_index.md`

## Material Closed Workstreams In This Planned Baseline

When release execution completes, the closed workstreams that materially define this baseline will be:

- `Docs/workstreams/FB-028_history_state_relocation.md`
- `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`
- `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`
- `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
- `Docs/workstreams/FB-027_interaction_system_baseline.md`
- `Docs/workstreams/FB-036_saved_action_authoring.md`
- `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md`
- `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`

## What Will Be Locked By v1.4.0-prebeta

After release execution, the shared pre-Beta baseline will include all `v1.3.1-prebeta` locked truth plus the FB-037 built-in catalog milestone:

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

This planned rebaseline does not authorize automatic continuation into:

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

## Planned Forward-Planning Posture After Release

After release execution clears FB-037 release debt:

- FB-037 should be `Released (v1.4.0-prebeta)` and `Closed`
- `Release Debt` for FB-037 should be cleared
- FB-038 should remain selected in canon only until a fresh Branch Readiness admission from updated `main`
- no FB-038 branch should exist before that Branch Readiness admission
- future implementation must enter through the strict branch-governance admission flow

## Historical Relationship

The preserved historical Jarvis closeout line remains valid historical context.

Use:

- `Docs/closeout_guidance.md` for closeout and rebaseline policy
- `Docs/closeout_index.md` for historical closeout lookup

This draft does not rewrite historical closeouts.

## Carry-Forward Rule

After the public release exists and `Docs/closeout_index.md` points here, future prompts should treat this rebaseline plus the retained workstream records as the modern carry-forward baseline through `v1.4.0-prebeta`.
