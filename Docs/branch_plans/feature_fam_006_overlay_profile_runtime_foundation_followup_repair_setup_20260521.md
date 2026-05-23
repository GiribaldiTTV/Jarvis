# Branch Readiness Stage 2 Follow-Up Repair Setup - FAM-006 Overlay Profile UX

Setup Date: `2026-05-21`
Branch: `feature/fam-006-overlay-profile-runtime-foundation`
Worktree: `C:\Nexus Worktrees\FAM-006`
Setup Base Commit: `98800f05ff302dad28ea492b77396df1fced5cc1`
Origin Main Basis: `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`
Reference Digest: `Docs/branch_plans/feature_fam_006_overlay_profile_runtime_foundation_followup_uts_reference_20260521.md`

## Setup Result

Status: `Accepted - follow-up returned USER UTS repair setup`

The USER follow-up rejects hardening the current returned-UTS Workstream result as-is. The next legal implementation must repair the Overlay Profile manager workflow, dropdown styling, delete affordance, Manage Monitors assignment/status flow, and source-list sensor-settings information architecture without expanding beyond FAM-006 Overlay Profile / Sensor Command Center scope.

## Overlay Profile Manager Repair Scope

- Replace native/basic filter affordances with NDAI-styled bounded dropdown controls.
- Apply a five-visible-option target before dropdown menus scroll.
- Use NDAI-native scrollbar styling for dropdown menus with more than five entries.
- Default Overlay Profile manager state should present:
  - `Create Overlay Profile`.
  - `Edit Overlay Profile` disabled until an explicit profile selection.
  - A right-side Overlay Profile selector dropdown.
- Selecting a profile enables `Edit Overlay Profile`.
- `Edit Overlay Profile` opens the selected profile settings surface.
- Profile settings surface must preserve existing create/rename/save/discard behavior where still relevant.
- Add a Delete Overlay Profile danger action with confirmation and red styling.
- Preserve Overlay Profile / Monitor Group / Recording Profile concept separation.

## Manage Monitors Repair Scope

- Make the Dashboard `Manage Monitors` button visually match the `Overlay Profile Settings` button size/treatment.
- Prove parity with focused screenshot comparison.
- Convert the `Assigned Overlay` summary/count row into a clickable control.
- Open a bounded status card/window listing overlays for the selected group/monitor context.
- Provide assign/unassign action based on the current assignment state.
- Remove the user-facing `Enabled for Overlay` checkbox where explicit assignment controls now own participation.
- Preserve Warning Notifications as a settings concept and Provider Readiness as readiness/status/future capability.

## Source-List Sensor Settings IA Scope

- Move away from generated detail cards for enabled sensors where current runtime supports the bounded migration.
- Add source-list sensor settings entry points.
- Add or plan a sensor-specific settings window that owns sensor-specific settings.
- Include Polling Rate in the sensor-specific settings path.
- Include copy that changing Polling Rate away from `Default` overrides the monitor's generalized polling-rate setting.
- Include future-warning-settings placeholders only as truthful future posture, not implemented notification runtime.
- Preserve Sensor Library as source discovery and Monitor Groups as organization/configuration.

## Validator / Proof Planning

Required implementation validators and proof should cover:

- NDAI filter/profile dropdown styling and absence of native/basic select visuals.
- Five-visible-option dropdown/list target and NDAI scrollbar behavior.
- Default Overlay Profile manager state: Create visible, Edit disabled, selector visible.
- Edit enabled after explicit profile selection.
- Edit opens selected profile settings.
- Delete Overlay Profile danger confirmation and red styling.
- Dashboard `Manage Monitors` button parity with `Overlay Profile Settings`.
- Assigned Overlay clickable status surface, overlay list, and assign/unassign action.
- `Enabled for Overlay` removed from user-facing Manage Monitors UI or replaced by assignment controls.
- Source-list sensor settings entry points and Polling Rate override disclaimer where implemented.
- Existing Dashboard resize, Overlay Profile state, Monitor Groups, Source Filter, Polling Rate, Source Picker, dirty guard, and Sensor Command Center preservation.

## Pending USER Decisions

- Follow-up Workstream implementation after this setup.
- H1 after follow-up implementation.
- Refreshed LV1/UTS after H1.
- PR Readiness, PR creation, merge, release, issues, artifacts, and cleanup.
- Recording Profile runtime, tray recording controls, export/share, provider/model work, broad theme/skin work, FAM-007, Governance, Compact-AI, AI Product, and sibling-worktree mutation.

## Exact Implementation Approval Text

Approve bounded follow-up returned-UTS Workstream implementation for `feature/fam-006-overlay-profile-runtime-foundation` in `C:\Nexus Worktrees\FAM-006`. Codex may implement only the admitted follow-up Overlay Profile and Manage Monitors repair scope: NDAI-styled Overlay Profile filter/profile dropdowns with max-five visible menu targets and NDAI scrollbars, default manager state with Create plus disabled Edit until profile selection, Edit opening selected profile settings, profile Delete with danger confirmation, Dashboard Manage Monitors button visual parity with Overlay Profile Settings, clickable Assigned Overlay status/assignment surface, removal of the user-facing Enabled for Overlay checkbox where assignment supersedes it, source-list sensor settings entry points with Polling Rate default/override disclaimer where current runtime supports it, validators/helpers/source-truth/UTS updates, focused proof, validation, and commit/push if green. Do not implement Recording Profile runtime, tray recording, export/share, provider/model work, broad theme/skin work, FAM-007 work, Governance mutation, Compact-AI work, PR creation, merge, release, issue mutation, branch cleanup, or sibling-worktree changes without separate approval.
