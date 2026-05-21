# Branch Readiness Stage 2 Repair Setup - Returned UTS Overlay Profile UX / Scale

Setup Date: `2026-05-21`
Branch: `feature/fam-006-overlay-profile-runtime-foundation`
Worktree: `C:\Nexus Worktrees\FAM-006`
Setup Input Commit: `c19bd9db843f772438fe24b02683e20af51e999d`
Returned UTS Reference: `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_returned_uts_temporary_reference_20260521.md`

## Stage 2 Repair Setup Result

Setup Status: `Green - returned USER UTS result is REPAIR and bounded Workstream implementation is required before PR Readiness`

This setup admits a focused repair lane for Overlay Profile UX, high-volume monitor-list behavior, danger-action affordance, and Manage Monitors Overlay-context compaction. It does not authorize direct PR Readiness, PR creation, merge, release, issue mutation, sibling-worktree mutation, Recording Profile runtime, tray recording, export/share, provider/model work, broad theme/skin work, FAM-007 work, Governance work, Compact-AI work, or AI Product work.

## Repair Purpose

The repair purpose is to turn the returned UTS into a bounded implementation contract:

- Overlay Profile Settings must support future high monitor volume without bloating the window.
- The first Overlay Profile choice must be understandable: load an existing profile or create a new one.
- Visible monitor membership must be compact, searchable, filterable, and scroll-contained.
- Danger actions must be visually obvious and consistently placed.
- Manage Monitors must show Overlay Profile context without becoming an Overlay Profile editor.

## Admitted Repair Scope

### Overlay Profile Settings Information Architecture

- Reshape the Overlay Profile Settings default state into a selector-first / create-first workflow.
- Keep the existing profile selection concept, but make the user's first action clear before profile details consume the window.
- Move profile detail/edit controls into the follow-on selected/create state inside the same child window unless implementation proof shows a second child window is safer.
- Preserve the existing Dashboard selector as the compact active-profile entry point.
- Preserve profile create, rename, Save, and Discard behavior, but reorganize their placement around the new workflow.

### Visible Monitor List Scale Rule

- Target a maximum of five visible monitor rows without a scrollbar where the window has room.
- Permit two or three visible rows only when the window size cannot safely fit five while preserving readability and controls.
- Keep the settings window itself from requiring a scrollbar under normal bounded sizing.
- Keep scrolling contained to the visible-monitor list when monitor volume exceeds the visible-row target.
- Use NDAI-native scrollbar styling for the visible-monitor list.
- Add search and filter controls for visible monitors.
- Preserve readable row names, selection state, included/excluded state, and keyboard/mouse operation.
- Defer richer tooltips to implementation judgment unless row text or metadata becomes clipped.

### Danger Action Placement And Styling

- Keep Create and Save actions on the left.
- Move Discard to the right.
- Make Discard red/illuminated when discardable changes exist.
- Keep Discard disabled/quiet when no discardable changes exist.
- Preserve Delete as a red danger action.
- Establish the branch-local rule that Discard and Delete are danger actions wherever they appear in the current FAM-006 HUD/Overlay Profile/Manage Monitors surfaces.

### Manage Monitors Overlay Context

- Condense the Manage Monitors Overlay Profile context from a card into a single-row read-only summary.
- Prioritize assigned overlay/profile count and active inclusion state using compact wording.
- Remove the `Open Overlay Profile Settings` button from Manage Monitors for this repair unless validator evidence proves a compact route is necessary and USER-visible weight stays low.
- Preserve concept separation: Manage Monitors configures monitors, while Overlay Profile Settings owns profile selection/membership editing.

### Manage Monitors Detail Hierarchy

The selected Monitor Group detail order for this repair is:

1. Group name.
2. Warning Notifications.
3. `Enabled for Overlay`.
4. Assigned Overlay row.
5. Polling Rate row.
6. Provider Readiness row.
7. Existing remaining detail content.

The implementation must rename the exposed overlay participation label to `Enabled for Overlay` where that concept appears.

## Future-Scope Items Preserved, Not Implemented By This Repair Setup

- Per-sensor Warning Notification runtime settings.
- Per-overlay-profile notification settings.
- Per-overlay-profile polling policy or resource mode.
- Lightweight profile resource-consumption behavior.
- Full HUD/Overlay custom layout editor.
- Platform-wide danger-button standard outside the current FAM-006 HUD / Overlay Profile / Manage Monitors surfaces.
- Recording Profile runtime.
- Tray recording controls.
- Export/share behavior.
- Provider/model/runtime AI work.
- Broad NDAI theme/skin work.

These are recorded as future planning requirements. They may inform current UI shape, but this repair setup does not admit their runtime behavior.

## Validator And Proof Planning

Existing reusable FAM-006 validators/helpers should be extended rather than creating new helper families unless implementation proves reuse would blur proof ownership.

Planned validator/proof updates:

- HUD surface validation should assert the Overlay Profile Settings selector-first/create-first structure.
- HUD surface validation should assert visible-monitor search and filter controls.
- HUD surface validation should assert max-five visible-row target markers and NDAI-native scroll-pane class on the visible-monitor list.
- HUD surface validation should assert the settings window avoids an outer scrollbar under normal bounded sizing markers.
- HUD surface validation should assert Create/Save left and Discard right.
- HUD surface validation should assert red danger styling for active Discard/Delete controls.
- HUD surface validation should assert the Manage Monitors Overlay context is single-row read-only and does not expose the settings-route button.
- HUD surface validation should assert the selected Monitor Group detail hierarchy and `Enabled for Overlay` label.
- Internal sandbox validation should prove search/filter state, membership save/discard preservation, dirty state, and concept-boundary preservation.
- Live validation should capture focused proof for default selector/create state, selected-profile detail state, visible-monitor search/filter, five-row/overflow behavior, danger-button active/disabled states, and condensed Manage Monitors context.
- Refreshed UTS must ask the USER to review high-volume monitor behavior, search/filter, danger-button clarity, no outer scrollbar, and Manage Monitors information hierarchy.

## Package / Slice Fit

Package Fit: `FAM-006 / PKG-006 Overlay Profile Runtime Foundation repair`

Slice Fit: `Returned LV1 repair spanning SLC-038 visible Overlay Profile selection/editing controls, SLC-039 monitor membership mapping UX, SLC-040 Manage Monitors context, and SLC-041 validation/live proof readiness.`

The repair is bounded to the active FAM-006 carrier because it corrects returned UTS issues in already-admitted Overlay Profile runtime foundation seams.

## Likely Affected Files

- `nexus_visual/monitoring_hud.html`
- `nexus_visual/monitoring_hud.css`
- `nexus_visual/monitoring_hud.js`
- `desktop/desktop_renderer.py`
- `dev/orin_monitoring_hud_surface_validation.py`
- `dev/orin_monitoring_hud_internal_sandbox_validation.py`
- `dev/orin_monitoring_hud_live_validation.ps1`
- `dev/orin_monitoring_hud_human_client_validation.ps1` only if user-facing shortcut/live proof needs refreshed checks
- `Docs/branch_records/feature_fam_006_overlay_profile_runtime_foundation.md`
- `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation.md`
- `Docs/feature_backlog.md`
- `Docs/prebeta_roadmap.md`
- `Docs/validation_helper_registry.md`

## Preservation Requirements

- Preserve SLC-037 Overlay Profile state/schema/persistence.
- Preserve activeOverlayProfileId and overlayProfiles normalization.
- Preserve profile membership save/discard semantics.
- Preserve Dashboard Overlay Profile selector width rule: minimum 300px, content-growing, maximum 450px or available row width.
- Preserve Monitor Group and Recording Profile concept separation.
- Preserve Sensor Library / Source Picker behavior.
- Preserve Warning Notifications as a settings concept, not an assignable sensor source.
- Preserve Provider Readiness as status/future capability, not an assignable source.
- Preserve Dashboard resize/right-edge and existing FAM-006 Monitor Groups repairs.
- Preserve focused proof discipline: focused WebView/local proof is acceptance evidence, full desktop is context only.

## Stage 2 Setup Validation Status

Validation Status: `Green`

Validation Basis: `git diff --check`; `git diff --check origin/main...HEAD`; `python dev\orin_branch_governance_validation.py`; `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`; `python dev\orin_branch_readiness_planning_fixture_validation.py`; `python dev\orin_release_body_validation.py`; `python dev\orin_ai_provider_state_validation.py`; `python dev\orin_monitoring_hud_surface_validation.py`; `python dev\orin_monitoring_hud_internal_sandbox_validation.py`; `python dev\orin_source_owner_marker_validation.py`; `python -m compileall -q dev desktop Audio main.py`.

## Exact Next Implementation Approval Text

Approve bounded returned-UTS Workstream implementation for `feature/fam-006-overlay-profile-runtime-foundation` in `C:\Nexus Worktrees\FAM-006`. Codex may implement the admitted Overlay Profile UX/scale and Manage Monitors overlay-context repair only: selector-first/create-first Overlay Profile Settings flow, max-five visible monitor target with NDAI-native list scrollbar, visible monitor search/filter, no normal outer settings-window scrollbar, Create/Save left with red illuminated Discard right, red danger styling for current Discard/Delete controls, condensed single-row read-only Manage Monitors Overlay context, removal of the Manage Monitors settings-route button, selected Monitor Group detail hierarchy updates, validator/helper/source-truth/UTS updates, focused proof, validation, and commit/push if green. Do not implement Recording Profile runtime, tray recording, export/share, provider/model work, broad theme/skin work, FAM-007 work, Governance mutation, Compact-AI work, PR creation, merge, release, issue mutation, branch cleanup, or sibling-worktree changes without separate approval.
