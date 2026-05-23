# FAM-001 Boot Interface Vision

## Purpose

This family vision records durable product direction for startup, boot, desktop entrypoint, single-instance ownership, launch handoff, relaunch semantics, lifecycle transition proof, and boot-to-runtime trust boundaries.

## Vision Summary

Boot Interface work should make Nexus feel reliable at startup without pretending the current desktop launcher is already the final boot-first product shell. The user should understand when Nexus starts, recovers, relaunches, or hands off control.

## Accepted Direction

- Preserve the current desktop orchestration path until a later USER-approved boot-facing package changes it.
- Prefer recoverable startup and truthful failure reporting over hidden automation.
- Keep boot-first behavior user-controlled before Beta.
- Make handoff, relaunch, and single-instance behavior explicit and testable.

## Implementation Boundaries

- This vision does not admit bootloader, sign-in, installer, or Windows startup mutation.
- Branch Runtime Engineering Plans own any active implementation checklist.
- Durable proof belongs in `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` and related structured branch receipts.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- Backlog registry: `Docs/feature_backlog.md`
- Roadmap posture: `Docs/prebeta_roadmap.md`
- Durable family dossier: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
