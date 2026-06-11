# FAM-001 Boot Interface Vision

## Purpose

This family vision records durable product direction for startup, boot, desktop entrypoint, single-instance ownership, launch handoff, relaunch semantics, lifecycle transition proof, boot-to-runtime trust boundaries, fatal launcher/runtime diagnostics, and recovery surfaces.

## Vision Summary

Boot Interface work should make Nexus feel reliable at startup without pretending the current desktop launcher is already the final boot-first product shell. The user should understand when Nexus starts, recovers, relaunches, or hands off control.

## Accepted Direction

- Preserve the current desktop orchestration path until a later USER-approved boot-facing package changes it.
- Prefer recoverable startup and truthful failure reporting over hidden automation.
- Keep boot-first behavior user-controlled before Beta.
- Make handoff, relaunch, and single-instance behavior explicit and testable.
- Own fatal launcher/runtime diagnostics and recovery surface direction when Nexus reaches startup abort, recovery exhaustion, crash/failure finalization, support-bundle preparation, manual issue reporting, retry/close/repair choices, or user-facing recovery explanation.
- Treat FB-034 recoverable `launch_failed` as released historical evidence for one bounded non-crashing incident class, not as active authority for broad diagnostics/recovery product scope.
- Future diagnostics/recovery surface planning should route through a USER-approved FAM-001 Family Feature Vision such as `F1-FF01 Runtime Diagnostics And Recovery Surface` or `F1-FF01 Failure Recovery And Support Reporting` before implementation.

## Implementation Boundaries

- This vision does not admit bootloader, sign-in, installer, or Windows startup mutation.
- This vision does not create a FAM-001 diagnostics/recovery FFV content file, diagnostics/recovery implementation branch, support-bundle behavior change, fatal launcher/runtime rewrite, or broad recoverable diagnostics expansion by itself.
- Branch Runtime Engineering Plans own any active implementation checklist.
- Durable proof belongs in `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` and related structured branch receipts.
- Visible diagnostics or recovery panels consume FAM-002 presentation standards, while each consuming FAM owns the failure/degraded/blocked/unavailable behavior for its own feature surface.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- Backlog registry: `Docs/feature_backlog.md`
- Roadmap posture: `Docs/prebeta_roadmap.md`
- Durable family dossier: `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md`
- Recoverable diagnostics historical evidence: `Docs/workstreams/FB-034_recoverable_diagnostics.md`
