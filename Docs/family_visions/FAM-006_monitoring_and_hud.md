# FAM-006 Monitoring And HUD Vision

## Purpose

This family vision records durable product direction for Monitoring HUD, Dashboard, Sensor Command Center, Sensor Library, monitor configuration, Overlay Profile, active-overlay-driven recording, local telemetry presentation, and user-facing performance/health surfaces.

## Vision Summary

Monitoring and HUD should give the user clear, trustworthy, polished visibility into system and sensor state without fake telemetry, proof clutter, broken/deferred controls, or confusing ownership between Dashboard, Overlay, Core, and settings windows.

## Accepted Direction

- Dashboard should act as the polished control hub, not a debug/proof panel.
- Provider, telemetry, no-data, degraded, disabled, and warning states must be truthful.
- Overlay Profile and Monitor Group concepts should remain distinct and reviewable.
- Recording should be active-overlay-driven, not a separately loaded Recording Profile. The active Overlay Profile determines what is recorded.
- Visual proof must include focused per-element review for user-facing changes.
- Deferred actions should be disabled, removed, or clearly labeled; they must not look broken.

## Recording Vision

- Recording controls should live inside the HUD Overlay card as a lightweight section.
- The HUD Overlay card should expose a small Quick Access recording control with Start Recording and Stop Recording.
- Recording should capture only the currently active Overlay Profile and the monitors assigned to that overlay. Separate Recording Profile monitor/source selection is no longer the desired product direction.
- Recording output should export to a valid, durable file format that can later be graphed, plotted, or otherwise analyzed reliably and easily.
- A Recording Settings button should open a dedicated Recording Settings window.
- Recording Settings should include the recording folder path, a quick access button to open the log/output folder, Start Recording, Stop Recording, and only other settings explicitly approved by USER after proposal.
- The Recording Settings window should be a separate normal OS-level window, not a Dashboard child window, so the user can keep it open, move it, minimize it, or close/minimize the HUD Dashboard independently.
- Recording Settings should look like an immersive NDAI window while remaining compact and lightweight.
- The Recording Settings window should be small by default because it is likely to stay open while users record. Any future setting that would make it bulky should be moved behind a secondary settings surface or other explicit USER-approved expansion.

## HUD Overlay Card Vision

- The HUD Overlay card should place Overlay Profile first, then Overlay Status.
- The currently selected Overlay Profile row should show the active monitors being monitored so users can understand exactly what will be recorded if they start recording.
- Overlay Profile Settings should have a stable location that future additions do not move. Preferred locations are either the HUD Overlay card title row on the right side or the bottom-right action position.
- Future recording controls should not displace the stable Overlay Profile Settings location.

## Implementation Boundaries

- This vision does not admit recording runtime, tray recording controls, broad theme/skin work, provider expansion, or external telemetry by itself.
- The historical `Recording Profile Runtime Foundation` branch introduced Recording Profile state/UI foundation before this active-overlay-driven recording vision correction. Future FAM-006 planning must reconcile or retire that profile-loaded direction before implementing actual recording runtime.
- Active FAM-006 branches must use Branch Runtime Engineering Plans, UFD disposition, and visual proof gates before implementation and Live Validation handoff.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- Backlog registry: `Docs/feature_backlog.md`
- Durable receipt pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
- Active branch pointer: `Docs/branch_records/feature_fam_006_recording_profile_runtime_foundation.md`
- Element ledger: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md`
