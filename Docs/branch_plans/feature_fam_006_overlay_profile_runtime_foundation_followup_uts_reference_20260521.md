# Temporary Reference - FAM-006 Overlay Profile Runtime Foundation Follow-Up UTS

Reference Date: `2026-05-21`
Branch: `feature/fam-006-overlay-profile-runtime-foundation`
Worktree: `C:\Nexus Worktrees\FAM-006`
Recorded At Head: `98800f05ff302dad28ea492b77396df1fced5cc1`
Current Main Basis: `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`

## Governance Classification

Returned User Test Summary Result: `REPAIR`

This follow-up USER response supersedes the planned returned-UTS H1 gate for commit `98800f05ff302dad28ea492b77396df1fced5cc1`. The prior Workstream implementation is useful evidence, but it is not H1-ready because the USER identified additional Overlay Profile workflow, dropdown styling, delete affordance, Manage Monitors, and sensor-settings information-architecture repairs.

PR Readiness remains blocked until the follow-up repair setup, implementation, hardening, refreshed Live Validation / UTS review, and returned USER PASS or waiver with reason are complete.

## Follow-Up USER Feedback Digest

### Overlay Profiles

- The Overlay Profile visible-monitor `Filter` dropdown still appears native/basic and must become an NDAI-styled bounded dropdown.
- The filter dropdown must follow the same max-five visible option target before an NDAI-native internal scrollbar is used.
- The prior implementation did not fully honor the requested Overlay Profile window workflow.
- Desired default Overlay Profile manager state:
  - A visible `Create Overlay Profile` button.
  - A greyed-out `Edit Overlay Profile` button while no profile is explicitly selected.
  - A profile selector dropdown on the right.
  - The profile selector menu shows all created Overlay Profiles, targets five visible entries, and uses an NDAI-native scrollbar when entries exceed five.
  - Selecting a profile enables `Edit Overlay Profile`.
  - Pressing `Edit Overlay Profile` opens that selected profile's settings.
- The full prior USER response and this follow-up must be digested together and held as acceptance criteria rather than cherry-picked.
- Overlay Profile management is missing a Delete control. A profile delete affordance should be included in the selected profile settings path with red danger styling and confirmation behavior.

### Monitor Groups / Manage Monitors

- The Dashboard `Manage Monitors` button should visually match the `Overlay Profile Settings` button in size and treatment. Screenshot comparison is required.
- The compact `Assigned Overlay` / assigned-count row should become a clickable button.
- Clicking that assigned-overlay control should open a status card/window showing the list of overlays for that group and an assign/unassign action based on current assignment state.
- The `Enabled for Overlay` checkbox should likely be removed. USER reasoning: Overlay participation should be controlled by assigning or not assigning the monitor/group to Overlay Profiles, rather than by a second independent checkbox.
- The CPU Load/generated sensor cards that appear after enabling a sensor should be removed from the selected monitor detail flow.
- Each source/sensor in the Source list should expose a settings button.
- A sensor-specific settings window should own that sensor's exclusive settings, including Polling Rate.
- Sensor-specific Polling Rate should include a disclaimer that changing it away from `Default` overrides the monitor's generalized polling-rate setting.
- Future sensor settings should include warning-notification settings and other sensor-specific controls once they are defined.

## Scope Classification

Immediate bounded follow-up implementation candidates:

- Overlay Profile manager default state and selection workflow.
- NDAI-styled filter/profile selector dropdowns with max-five visible menu target.
- Overlay Profile delete affordance with red danger styling and confirmation.
- Dashboard `Manage Monitors` button visual parity with `Overlay Profile Settings`.
- Clickable assigned-overlay status surface with overlay list and assign/unassign action.
- Removal of the `Enabled for Overlay` checkbox from user-facing Manage Monitors UI where assignment controls supersede it.

Architecture-heavy but admitted for bounded planning and cautious implementation if current runtime supports it:

- Moving sensor-specific settings out of generated monitor detail cards and into Source list settings buttons.
- Sensor-specific settings window with Polling Rate default/override behavior and future warning-setting placeholders.

Future-gated / not admitted by this setup without later USER approval:

- Recording Profile runtime.
- Tray recording controls.
- Export/share behavior.
- Provider/model execution.
- Broad theme/skin work.
- FAM-007, Governance, Compact-AI, AI Product, issue, PR, release, artifact, stale-branch cleanup, or sibling-worktree mutation.

## Recommended Next Legal Phase

Next Legal Phase: `Bounded follow-up returned-UTS Workstream implementation for Overlay Profile manager, Manage Monitors overlay assignment, and source-list sensor settings IA repair`

## Exact USER Decision Needed

Approve bounded follow-up returned-UTS Workstream implementation for `feature/fam-006-overlay-profile-runtime-foundation` in `C:\Nexus Worktrees\FAM-006`. Codex may implement only the admitted follow-up Overlay Profile and Manage Monitors repair scope: NDAI-styled Overlay Profile filter/profile dropdowns with max-five visible menu targets and NDAI scrollbars, default manager state with Create plus disabled Edit until profile selection, Edit opening selected profile settings, profile Delete with danger confirmation, Dashboard Manage Monitors button visual parity with Overlay Profile Settings, clickable Assigned Overlay status/assignment surface, removal of the user-facing Enabled for Overlay checkbox where assignment supersedes it, source-list sensor settings entry points with Polling Rate default/override disclaimer where current runtime supports it, validators/helpers/source-truth/UTS updates, focused proof, validation, and commit/push if green. Do not implement Recording Profile runtime, tray recording, export/share, provider/model work, broad theme/skin work, FAM-007 work, Governance mutation, Compact-AI work, PR creation, merge, release, issue mutation, branch cleanup, or sibling-worktree changes without separate approval.
