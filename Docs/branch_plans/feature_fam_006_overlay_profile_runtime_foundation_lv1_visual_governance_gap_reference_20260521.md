# Temporary Reference - FAM-006 LV1 Visual Governance Gap

Reference Date: `2026-05-21`
Branch: `feature/fam-006-overlay-profile-runtime-foundation`
Worktree: `C:\Nexus Worktrees\FAM-006`
Rejected LV1 Commit: `b09ba27f43460760ac63ce4663a7cd4fc227807d`
Human-Client Manifest: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_human_client_validation\20260521_120112_098\human_client_manifest.json`
Active-Client Manifest: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_120557_633\monitoring_hud_live_client_interaction_manifest.json`
Focused Proof Root: `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_120557_633\live_client_interaction\`

## Governance Classification

Returned User Test Summary Result: `FAIL`

The refreshed LV1 handoff is rejected. Helper PASS markers, manifest existence, and screenshot-file existence were not sufficient because Codex did not perform a failure-seeking visual adjudication pass against the FAM-006 feature vision and package-level UI/UX intent before handing the proof to the USER.

PR Readiness remains blocked. The branch must route back to bounded repair planning/implementation before another H1 and refreshed LV1 handoff can be considered.

## Proof Artifacts Inspected

- `03_overlay_profile_settings_window_dirty.png`
- `03_overlay_profile_settings_window_create_clean.png`
- `03_overlay_profile_manage_context.png`
- `03_manage_monitors_open_state.png`
- `11_100_monitor_list_scrollbar_and_1200_source_picker.png`
- `01_initial_live_client_visible.png`
- `03_final_anchored_live_client.png`

## Codex Visual Findings

- Overlay Profile manager proof shows a cramped selector-first row where the profile selector text is clipped (`SELECT PROFI...`) instead of proving a clean, readable, future-scaled manager surface.
- Overlay Profile manager proof does not clearly prove the intended default flow as a high-confidence user choice between creating a new profile and selecting an existing profile before editing.
- Focused proof does not include enough distinct acceptance-critical states for Overlay Profile delete confirmation, assigned-overlay assignment/status interaction, profile selector open state, filter open state, and disabled/enabled Edit transition. Artifact presence was over-counted as visual acceptance.
- Manage Monitors proof shows the `Assigned Overlay` row, but the row reads like static status text rather than a clearly clickable assignment/status control. The LV1 handoff should have treated this as a visual-affordance risk.
- Manage Monitors proof still depends on dense nested panes and scroll regions; the footer action row and high-volume source list need explicit visual-adjudication checks for clipping, readability, button affordance, and inner-only scrollbar ownership.
- Dashboard proof is mostly full-desktop context; it is not enough by itself to prove Dashboard button parity, package-level visual hierarchy, or first-viewport readability.

## Governance Failure

- The LV1 helper validated that controls and screenshots existed, but it did not require Codex to classify every acceptance-critical visual artifact as `PASS`, `REPAIR`, `STOP`, or `WAIVED_WITH_REASON`.
- The active source truth allowed `Focused Proof Result: PASS` while no durable `Codex Visual Adjudication` section recorded artifact-by-artifact visual judgment, product-vision alignment, missing-state proof, or unacceptable UI findings.
- USER vision inputs from the returned UTS repair chain were treated as implementation checklist items, but the final LV1 proof did not require a line-by-line vision-to-artifact verdict before USER handoff.

## Required Governance Repair

- Add a `Codex Visual Adjudication` gate for desktop user-facing Live Validation before a UTS handoff can be treated as ready.
- The gate must prove that Codex inspected the focused proof images, compared them to the branch Product Definition Plan, Runtime Branch Engineering Contract, returned USER vision, and package-level UI/UX expectations, and classified every acceptance-critical state.
- Helper PASS, marker PASS, screenshot existence, and manifest existence are supporting evidence only. They cannot clear visual acceptability.
- If Codex can see unacceptable UI, missing state proof, clipped text, unclear control hierarchy, non-native controls, weak affordance, inconsistent danger styling, or workflow confusion, LV1 must be classified `FAIL` or `REPAIR` before USER intervention.

## Next Legal Repair Target

Next Legal Phase: `Bounded Workstream repair setup/implementation for LV1 visual acceptability defects`

Repair planning should start from the findings above and the previous returned-UTS reference files, then re-run H1 and refreshed LV1 with the new visual-adjudication gate before PR Readiness is considered.
