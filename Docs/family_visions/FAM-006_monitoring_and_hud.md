# FAM-006 Monitoring And HUD Vision

## Purpose

This family vision records durable product direction for Monitoring HUD, Dashboard, Sensor Command Center, Sensor Library, monitor configuration, Overlay Profile, Recording Profile, local telemetry presentation, and user-facing performance/health surfaces.

## Vision Summary

Monitoring and HUD should give the user clear, trustworthy, polished visibility into system and sensor state without fake telemetry, proof clutter, broken/deferred controls, or confusing ownership between Dashboard, Overlay, Core, and settings windows.

## Accepted Direction

- Dashboard should act as the polished control hub, not a debug/proof panel.
- Provider, telemetry, no-data, degraded, disabled, and warning states must be truthful.
- Overlay Profile and Monitor Group concepts should remain distinct and reviewable.
- Recording Profile should remain distinct from Overlay Profile, Monitor Group, tray recording controls, export/share, and provider/model execution.
- Visual proof must include focused per-element review for user-facing changes.
- Deferred actions should be disabled, removed, or clearly labeled; they must not look broken.

## Implementation Boundaries

- This vision does not admit recording runtime, tray recording controls, broad theme/skin work, provider expansion, or external telemetry by itself.
- Active FAM-006 branches must use Branch Runtime Engineering Plans, UFD disposition, and visual proof gates before implementation and Live Validation handoff.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- Backlog registry: `Docs/feature_backlog.md`
- Durable receipt pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
- Active branch pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
- Element ledger: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md`
