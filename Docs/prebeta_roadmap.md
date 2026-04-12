# Nexus Pre-Beta Roadmap

## Purpose

This document is the sequencing and release-posture layer for current Nexus `pre-Beta` planning.

Use it for:

- latest public prerelease truth
- release-debt posture
- current sequencing posture
- recently closed milestone context

Do not use it as:

- a second backlog
- a workstream execution diary
- a substitute for canonical workstream records

## Authority And Boundaries

This roadmap is subordinate to:

- `Docs/development_rules.md`
- `Docs/codex_modes.md`
- `Docs/feature_backlog.md`
- `Docs/workstreams/index.md`
- `Docs/closeout_guidance.md`

That means:

- backlog owns identity
- workstream docs own promoted-work execution and closure truth
- closeouts and rebaselines own epoch summaries
- roadmap owns sequencing and release posture only

## Lane Types And Release Fields

Use these lane types:

- `docs-only`
- `implementation`
- `rebaseline`

Use these release-floor values:

- `no release`
- `patch prerelease`
- `minor prerelease`

Use these release-state values when relevant:

- `active delta`
- `merged unreleased`
- `released`
- `closed`

## Current Release Posture

Current merged truth indicates:

- latest public prerelease: `v1.2.7-prebeta`
- latest public release commit: `3168823`
- merged unreleased non-doc implementation debt now exists on `main`
- that merged unreleased implementation debt is the first FB-027 capability milestone for first-class URL saved-action targets
- FB-027 remains the active promoted interaction workstream on `main`

That means `main` is no longer between released non-doc implementation lanes. It now carries one merged unreleased FB-027 capability milestone above the locked interaction baseline, so the next posture should be release review/prep or directly coupled truth-repair and consistency work rather than another unrelated implementation lane.

## Current Promoted Workstream Context

### FB-027 Interaction System Baseline

- status: `merged unreleased on main`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `TBD`
- release state: `merged unreleased`
- canonical workstream doc: `Docs/workstreams/FB-027_interaction_system_baseline.md`
- sequencing note: now preserves the locked typed-first baseline while adding first-class URL saved-action targets without changing exact-match resolution, state-machine boundedness, or input-capture behavior

## Recently Closed Workstreams

### FB-035 Release-Context Fallback Hardening

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.7-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
- sequencing note: closed the support-report release-context hardening milestone and established the current release-context baseline

### FB-034 Recoverable Diagnostics

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.6-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-034_recoverable_diagnostics.md`
- sequencing note: remains a closed recoverable-diagnostics milestone, not an automatically active continuation lane

### FB-025 Boot/Desktop Taxonomy Clarification

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.5-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md`

### FB-033 Startup Snapshot Harness Follow-Through

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.4-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md`

### FB-028 History State Relocation

- status: `closed`
- lane type: `implementation`
- release floor: `patch prerelease`
- target version: `v1.2.3-prebeta`
- release state: `released`
- canonical workstream doc: `Docs/workstreams/FB-028_history_state_relocation.md`

## Current Sequencing Reading

Current merged truth indicates:

- the released FB-035 lane is closed
- the recent released workstreams above remain part of the locked current baseline
- FB-027 now contributes the first bounded merged unreleased implementation milestone above the validated interaction baseline
- the immediate next posture is merged-truth sync and release-context consistency work, then release review/prep before another unrelated implementation lane
- the next FB-027 capability milestone should be chosen only after merged truth and release posture are coherent on `main`
- this milestone does not authorize resolution changes, voice, Action Studio, routines, profiles, hotkey cleanup, or shutdown-confirmation work

Use canonical workstream docs for execution detail.
Use the backlog for item identity.
