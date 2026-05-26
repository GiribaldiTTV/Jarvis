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
- Monitoring, HUD, telemetry, screenshots, recordings, logs, and support evidence must preserve local file hygiene, clear evidence roots, privacy-safe review posture, and no fake or hidden data collection.
- Sensitive telemetry, recording, overlay, process, or performance surfaces must make provider/external telemetry boundaries explicit before any external data path is admitted.

## Recording Vision

- Recording should be intuitive and automatically connected to the currently active Overlay Profile.
- Recording should not require a separate Recording Profile, duplicate monitor groups, or a recording-specific sensor chooser. The active Overlay Profile and its active membership define the recording target.
- The HUD Overlay card should act as the launcher and target/status preview surface for recording. It should show the active Overlay Profile, the future recording target summary, and a truthful inactive/future-gated status before recording execution exists.
- A future HUD Overlay card action should open the compact Recording Control window. Real Start/Stop controls remain future-gated until recording execution and file writing are explicitly admitted.
- The Recording Control window should be a small standalone normal OS-level NDAI window, not a Dashboard child panel. The user should be able to move it, minimize it, restore it from the taskbar, and keep it open independently of the Dashboard.
- The Recording Control window should stay compact by default because it is likely to remain open while the user records. Any advanced or bulky settings should move behind a secondary settings/details window or another explicitly approved surface.
- Future recording output should use a valid, durable, graph/plot-ready format. CSV-like output is a likely first candidate, but file-format options should be proposed before output/file writing is admitted.
- Native Log Loader is a future separate graph/log viewer that reads completed recording logs over time. It is not the recording control surface and is not admitted for implementation by the active-overlay recording contract alone.

## Future Effective Polling Policy Vision

- Future FAM-006 architecture should support per-overlay effective polling policy so the same Monitor Group can be reused by multiple Overlay Profiles with different effective polling intervals.
- Example future target: a Gaming Overlay can use CPU Group and GPU Group at 1 second polling, while a Lightweight Overlay can use the same groups at 3 second polling.
- The desired long-term model should avoid duplicate Monitor Groups such as CPU Group FAST and CPU Group SLOW merely to change polling cadence.
- Recording should eventually inherit the active overlay's effective runtime policy when recording output is admitted.
- This is a future planning/source-truth constraint, not SLC-051 implementation authority. SLC-051 should avoid designing the recording target model in a way that blocks future per-overlay effective polling policy.

## HUD Overlay Card Vision

- The HUD Overlay card should place Overlay Profile first, then Overlay Status.
- The currently selected Overlay Profile row should show the active monitors being monitored so users can understand exactly what will be recorded if they start recording.
- Overlay Profile Settings should have a stable location that future additions do not move. Preferred locations are either the HUD Overlay card title row on the right side or the bottom-right action position.
- Future recording controls should not displace the stable Overlay Profile Settings location.

## Implementation Boundaries

- This vision does not admit recording runtime, tray recording controls, broad theme/skin work, provider expansion, or external telemetry by itself.
- This vision does not admit hidden monitoring, external telemetry, provider-visible telemetry, support-bundle export, backup/export, or cleanup/deletion behavior by itself.
- The historical `Recording Profile Runtime Foundation` branch introduced Recording Profile state/UI foundation before this active-overlay-driven recording vision correction. Future FAM-006 planning must reconcile or retire that profile-loaded direction before implementing actual recording runtime.
- Active FAM-006 branches must use Branch Runtime Engineering Plans, UFD disposition, and visual proof gates before implementation and Live Validation handoff.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Backlog registry: `Docs/feature_backlog.md`
- Durable receipt pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
- Active branch pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md`
- Element ledger: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md`
