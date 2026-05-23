# Temporary Reference - FAM-006 Overlay Profile Runtime Foundation Returned UTS

Reference Date: `2026-05-21`
Branch: `feature/fam-006-overlay-profile-runtime-foundation`
Worktree: `C:\Nexus Worktrees\FAM-006`
Recorded At Head: `47f231824b55ef97842c1b6b5c285581f802560a`
Current Main Basis: `4ce454cc1e951c2c7b158b912e78ab1113a2b3f0`

## Governance Classification

Returned User Test Summary Result: `REPAIR`

This USER response is not a PASS or waiver. It blocks PR Readiness until the returned concerns are admitted into source truth, repair setup is completed, implementation and hardening are green, and refreshed Live Validation / UTS review returns PASS or is explicitly waived with reason.

The prior SLC-037 through SLC-041 hardening proved the implemented Overlay Profile foundation, visible selector/settings controls, membership mapping, Manage Monitors read-only context/route, and focused proof readiness for the then-admitted scope. It did not prove the newly stated future-volume visible-monitor standard, selector-first profile workflow, or revised Manage Monitors information hierarchy.

## Returned USER Feedback Digest

### Overlay Profile Volume And Future Scale

- Need hardening and planning for future high-volume monitor counts inside Overlay Profiles.
- Visible monitor lists should target a maximum of five visible monitors without a scrollbar where the window size reasonably allows it.
- The five-visible-monitor standard should become a uniform platform guideline, with practical exceptions for smaller windows that may only allow two or three visible rows.
- The containing window should avoid requiring its own scrollbar; only the visible monitor list should scroll when needed.
- The visible monitor list scrollbar must use NDAI-native styling, not native Windows styling.
- Add search and filter controls for visible monitors.
- Tooltips may be needed later for monitor information that cannot fit cleanly in the compact list.

### Overlay Profile Workflow And Information Architecture

- Current Overlay Profile Settings flow is functionally confusing even though the visual style is liked.
- The default opening state should make the user's first choice clear: load an existing profile or create a new one.
- After a profile is selected or created, the flow should either expand the same window into the next settings step or open a second settings surface.
- Profile creation should not feel buried at the bottom of an already-loaded default profile.
- Future Overlay Profile design must reserve space for individual overlay customization, lightweight profiles, resource-conscious loadouts, and future HUD Dashboard / Overlay capabilities.

### Danger Actions And Button Semantics

- Move Discard to the right side; Create and Save should remain on the left.
- Discard must visibly illuminate red when discardable changes exist.
- Discard and Delete are danger actions and should use red active styling wherever they appear across the platform.
- A visible-but-dead-looking Discard button is a UX defect because it makes the action appear non-interactable.

### Manage Monitors Overlay Context

- The Overlay context in Manage Monitors is useful, but the current card consumes too much vertical space.
- Condense the Overlay context to a single row.
- The single row should prioritize the number of assigned overlays, such as zero or twenty.
- Remove the Open Overlay Profile Settings button from Manage Monitors for now to keep overlay editing centralized.
- Tooltip support may be considered later if the condensed row needs extra context, but it is not required yet.

### Manage Monitors Desired Detail Order

The selected Monitor Group detail hierarchy requested by the USER is:

1. Group name.
2. Warning Notifications.
3. `Enabled for Overlay`.
4. Assigned Overlay row.
5. Polling Rate row.
6. Provider Readiness row.
7. Existing remaining detail content.

The current label should change to `Enabled for Overlay` where this meaning is exposed.

### Notification And Profile Customization Vision

- Warning notification settings are still missing from the broader HUD vision.
- The intended HUD feature base is customizable by sensor, monitor, overlay profile, and loadout where technically possible.
- Polling rate, notification style, overlay profile behavior, and similar settings should not be globally locked unless a clear technical or product reason is recorded.
- Lightweight overlay profiles that reduce system resource consumption are part of the future direction.
- If this vision requires rethinking or redesigning the UI/UX while the framework is still early, that should be admitted now instead of deferred silently.

## Immediate Repair Candidates

- Overlay Profile Settings layout and flow repair: selector-first or create-first state, then detail/settings state.
- Visible monitor list scale repair: max-five visible target, scroll containment, NDAI-native scrollbar, search, and filter.
- Overlay Profile action-row repair: Create and Save left, Discard right, danger styling for discardable Discard.
- Manage Monitors overlay context repair: single-row read-only summary and removal of the settings-route button from the Manage Monitors detail surface.
- Manage Monitors hierarchy repair: reorder details and rename the overlay participation label to `Enabled for Overlay`.
- Validator and proof repair: add checks for visible-monitor list volume behavior, native scrollbar class, search/filter controls, no outer window scrollbar under normal size, danger action styling, condensed Manage Monitors row, and updated detail order.

## Future-Scope Or Planning-Heavy Items

- Per-sensor Warning Notification runtime settings.
- Per-overlay-profile notification behavior.
- Per-overlay-profile polling/resource policy.
- Lightweight profile behavior that affects system resource consumption.
- Full HUD/Overlay customization design beyond the current foundation branch.
- Platform-wide danger-button styling standard across all windows.

These items should be recorded as future design or package planning unless the next repair setup explicitly admits them into the current branch.

## Recommended Next Legal Phase

Next Legal Phase: `Branch Readiness Stage 2 returned-UTS repair setup for FAM-006 Overlay Profile UX, scale, and Manage Monitors overlay-context repair`

Repair setup should decide the exact bounded implementation path before runtime mutation. The returned feedback changes workflow, scale, information hierarchy, and design intent enough that direct patching from Live Validation would be too shallow.

## Exact USER Decision Needed

Approve Branch Readiness Stage 2 returned-UTS repair setup for `feature/fam-006-overlay-profile-runtime-foundation` in `C:\Nexus Worktrees\FAM-006`. Codex may admit the returned USER UTS result as `REPAIR`, update branch authority/source truth, define the bounded Overlay Profile UX/scale and Manage Monitors overlay-context repair scope, update validator/proof planning, run required validation, and commit/push setup changes if validation is green. Do not implement runtime UI changes, create PRs, merge, release, mutate issues, touch sibling worktrees, or expand into Recording Profile, tray recording, export/share, provider/model, broad theme/skin, FAM-007, Governance, Compact-AI, or AI Product work without separate approval.
