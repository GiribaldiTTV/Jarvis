# FAM-006 Monitoring And HUD Vision

## Purpose

This family vision records durable product direction for Monitoring HUD, Dashboard, Sensor Command Center, Sensor Library, monitor configuration, Overlay Profile, active-overlay-driven recording, local telemetry presentation, and user-facing performance/health surfaces.

## Vision Summary

Monitoring and HUD should give the user clear, trustworthy, polished visibility into system and sensor state without fake telemetry, proof clutter, broken/deferred controls, or confusing ownership between Dashboard, Overlay, Core, and settings windows.

## Accepted Direction

- Dashboard should act as the polished control hub, not a debug/proof panel.
- New Dashboard, HUD, Overlay Profile, Monitor Group, Recording, Sensor Command Center, or child-window UI must sample from the existing FAM-006 visual system before introducing any new visual grammar.
- Provider, telemetry, no-data, degraded, disabled, and warning states must be truthful.
- Overlay Profile and Monitor Group concepts should remain distinct and reviewable.
- Recording should be active-overlay-driven, not a separately loaded Recording Profile. The active Overlay Profile determines what is recorded.
- Visual proof must include focused per-element review for user-facing changes.
- Visual proof must also prove visual-system inheritance: new cards, rows, controls, dividers, empty/deferred states, status fields, and child-window surfaces must match established FAM-006 color tokens, shape/radius, spacing, typography, row/divider treatment, button effects, hover/focus/disabled states, shadows/glows, scrollbar treatment, and layout density unless BP1/BP2/BP3 explicitly accepts a new visual grammar.
- Deferred actions should be disabled, removed, or clearly labeled; they must not look broken.
- Monitoring, HUD, telemetry, screenshots, recordings, logs, and support evidence must preserve local file hygiene, clear evidence roots, privacy-safe review posture, and no fake or hidden data collection.
- Sensitive telemetry, recording, overlay, process, or performance surfaces must make provider/external telemetry boundaries explicit before any external data path is admitted.

## Recording Vision

- Recording should be intuitive and automatically connected to the currently active Overlay Profile.
- Recording should not require a separate Recording Profile, duplicate monitor groups, or a recording-specific sensor chooser. The active Overlay Profile and its active membership define the recording target.
- USER Live Validation feedback on 2026-06-02 changes the active recording surface direction: recording should live in its own small Dashboard Recording card, separate from the HUD Overlay card.
- The Dashboard Recording card should own recording target/status presentation and future recording-specific controls after later approvals. It may read the active Overlay Profile as the target source, but it should not turn the Overlay card into a recording-control surface.
- The Dashboard Recording card must look and behave like an existing Dashboard hub card. It should reuse the standard Dashboard card chrome, badge treatment, state-row/divider grammar, copy scale, action-button style, disabled/future-gated affordance, hover/focus effects, spacing, and density from the HUD Overlay, Monitor Groups, Data Sources, and Readiness cards unless USER accepts a later branch vision that changes the whole Dashboard visual system.
- Recording-specific styling must not introduce a unique card color family, nested boxed table, custom row shape, custom glow, or separate visual hierarchy that makes the Recording card feel detached from the standardized Dashboard card format.
- The HUD Overlay card should stay focused on overlay identity, Overlay Profile state, Overlay Status, and overlay-specific actions. It should not host recording-specific controls or be the primary recording launcher after this vision revision.
- Any future standalone Recording Control window, expanded settings window, or secondary recording-detail surface now requires revised BP1/BP2/BP3 approval because the active design direction centers recording in its own Dashboard card first.
- Recording output should save first as a native NDAI recording log owned by Nexus Desktop AI. The native log is the canonical product artifact for NDAI readback, future in-app viewing, and validation.
- Excel/CSV, JSON, or other third-party readable files are export artifacts, not the default recording save. Export requires a USER-requested export flow with supported file-type choices and validation that the exported file opens/readably displays in the target class of software.
- The Dashboard Recording card may open the exported-log folder, but normal Start/Stop recording must not auto-create CSV or other third-party export files. Until a future export branch exists, manual CSV files may be created only as validation artifacts outside the product-native log folder.
- Native Log Loader is a future separate graph/log viewer that reads completed recording logs over time. It is not the recording control surface and is not admitted for implementation by the active-overlay recording contract alone.

## Future Effective Polling Policy Vision

- Future FAM-006 architecture should support per-overlay effective polling policy so the same Monitor Group can be reused by multiple Overlay Profiles with different effective polling intervals.
- Example future target: a Gaming Overlay can use CPU Group and GPU Group at 1 second polling, while a Lightweight Overlay can use the same groups at 3 second polling.
- The desired long-term model should avoid duplicate Monitor Groups such as CPU Group FAST and CPU Group SLOW merely to change polling cadence.
- Recording should eventually inherit the active overlay's effective runtime policy when recording output is admitted.
- This is a future planning/source-truth constraint, not SLC-051 implementation authority. SLC-051 should avoid designing the recording target model in a way that blocks future per-overlay effective polling policy.

## HUD Overlay Card Vision

- The HUD Overlay card should place Overlay Profile first, then Overlay Status.
- The currently selected Overlay Profile row may show active monitors for overlay clarity, but recording target/status explanation belongs in the Dashboard Recording card after the 2026-06-02 USER design revision.
- Overlay Profile Settings should have a stable location that future additions do not move. Preferred locations are either the HUD Overlay card title row on the right side or the bottom-right action position.
- Future recording controls should not displace the stable Overlay Profile Settings location and should not move back into the HUD Overlay card without a later accepted BP1/BP2/BP3 revision.

## Implementation Boundaries

- This vision does not admit recording runtime, tray recording controls, broad theme/skin work, provider expansion, or external telemetry by itself.
- This vision does not admit hidden monitoring, external telemetry, provider-visible telemetry, support-bundle export, backup/export, or cleanup/deletion behavior by itself.
- The historical `Recording Profile Runtime Foundation` branch introduced Recording Profile state/UI foundation before this active-overlay-driven recording vision correction. Future FAM-006 planning must reconcile or retire that profile-loaded direction before implementing actual recording runtime.
- Active FAM-006 branches must use Branch Runtime Engineering Plans, UFD disposition, and visual proof gates before implementation and Live Validation handoff.
- Implementation must hold itself to this vision contract: any branch that creates or changes FAM-006 user-facing UI must state the existing element(s) it sampled, preserve or intentionally justify differences in color, shape, spacing, typography, effects, interaction states, and layout density, then prove those matches in Workstream, Hardening, and Live Validation. Validator/helper green is not enough when the visible result diverges from this family visual system.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Backlog registry: `Docs/feature_backlog.md`
- Recording Family Feature Vision: `Docs/family_feature_visions/FAM-006_recording.md`
- Durable receipt pointer: `Docs/branch_records/feature_fam_006_overlay_display_acceptance_foundation.md`
- Active branch pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_implementation.md`
- Released planning receipt pointer: `Docs/branch_records/feature_fam_006_active_overlay_recording_runtime_foundation.md`
- Element ledger: `Docs/branch_records/feature_fam_006_monitoring_hud_product_surface_element_ledger.md`
