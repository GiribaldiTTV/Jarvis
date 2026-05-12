# Nexus Pre-Beta Rebaseline Through v1.2.7-prebeta

Historical note:

- the current carry-forward Nexus pre-Beta baseline has advanced to `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.2.8-prebeta.md`
- this document remains the historical epoch summary through `v1.2.7-prebeta`

## Purpose

This document is the modern Nexus-era rebaseline through `v1.2.7-prebeta`.

Its job is to:

- summarize the current shared pre-Beta baseline
- capture what is locked versus deferred
- reduce prompt bloat by replacing repeated lane recaps
- point back to preserved historical closeouts without rewriting them

## Baseline Scope

This rebaseline covers merged shared truth through the released public prerelease:

- `v1.2.7-prebeta`

It stands on top of the preserved historical closeout line indexed in:

- `Docs/closeout_index.md`

## Material Closed Workstreams In This Baseline

The closed workstreams that materially define the current baseline are:

- `Docs/workstreams/FB-028_history_state_relocation.md`
- `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`
- `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`
- `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- `Docs/workstreams/FB-035_release_context_fallback_hardening.md`

## What Is Locked Now

Through `v1.2.7-prebeta`, current shared truth includes:

- launcher-owned historical state is not a live root-logs surface
- the startup snapshot harness is a bounded dev-only and opt-in debugging surface
- boot and desktop milestone taxonomy remains clarified without collapsing ownership boundaries
- one recoverable-operational-incident class is closed and shipped:
  - repeated identical `launch_failed` for the same action in a still-running session
- support-report fallback now derives release context from released-canon truth instead of the highest planned prerelease target
- the manual-reporting boundary remains local and manual only

## What Remains Deferred

This rebaseline does not authorize automatic continuation into:

- broader recoverable diagnostics surface work
- broader reporting-policy or upload-behavior work
- broader boot-layer implementation work
- broader interaction, rebrand, or UI follow-through by inertia

## Forward-Planning Posture After This Baseline

Current merged truth does not automatically activate a new non-doc implementation lane.

The next implementation workstream must be chosen from refreshed backlog, workstream, and product-boundary truth rather than by continuing the released FB-035 lane.

## Historical Relationship

The preserved historical Nexus closeout line remains valid historical context.

Use:

- `Docs/closeout_guidance.md` for closeout and rebaseline policy
- `Docs/closeout_index.md` for historical closeout lookup

This document does not rewrite those historical closeouts.

## Carry-Forward Rule

Future prompts should usually treat this rebaseline plus the retained workstream records as the modern carry-forward baseline through `v1.2.7-prebeta` instead of replaying each closed lane narrative in full.
