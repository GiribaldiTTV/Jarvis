# FB-036 Saved-Action Authoring

## ID And Title

- ID: `FB-036`
- Title: `Limited saved-action authoring and type-first custom task UX`

## Record State

- `Promoted`

## Status

- `Active on feature/fb-036-saved-action-authoring`

## Release Stage

- `pre-Beta`

## Target Version

- `TBD`

## Purpose / Why It Matters

Deliver a bounded in-product path for creating and editing saved actions without reopening the typed-first interaction contract or expanding into Action Studio behavior.

This workstream exists so users can manage non-standard custom tasks safely through the existing shared action model instead of hand-editing JSON.

## Current Branch Truth

- the branch already includes safe saved-action persistence and explicit catalog reload after writes
- the branch already includes a type-first create flow and a bounded edit flow
- the entry-state NCP opening now stays lightweight and button-led, with `Create Custom Task` and `Created Tasks` as the primary authoring entry points
- detailed saved-action inventory viewing and edit reachability now live in the secondary `Created Tasks` window instead of being expanded inline on the initial opening surface
- create/edit dialogs now expose an explicit `Trigger` field with `Launch`, `Open`, `Launch and Open`, and `Custom` options
- callable phrases for saved actions are now generated at runtime from `title`, `aliases`, `trigger_mode`, and optional `custom_triggers` instead of being persisted as alias hacks
- legacy saved actions that do not yet carry trigger fields still remain bare-title and bare-alias only until they are deliberately rewritten through the new model
- create/edit dialogs now use stronger field headers, concise help icons, and a bottom examples box that updates from the current title, aliases, trigger selection, and target kind
- exact-match resolution remains unchanged
- the overlay phase machine remains bounded to `entry` -> `choose` -> `confirm` -> `result`
- current supported saved-action target kinds remain `app`, `folder`, `file`, and `url`
- malformed or colliding saved-action sources still block authoring rather than attempting salvage
- branch-local validation and hardening work now also includes dedicated FB-036 validators, live-style harnesses, interactive runtime helpers, durable validation reports, and exported manual-test artifacts that future slices should reuse rather than recreate blindly

## Scope

- bounded saved-action create and edit UX
- safe persistence and validation-before-write
- immediate catalog reload after successful writes
- explicit user-facing type selection mapped to the current persisted target kinds
- a lightweight landing path for task authoring and management that does not overload the initial NCP opening surface
- richer secondary create/manage windows that can carry the detailed explanations, guidance, and step-by-step authoring copy users need once they choose an action path
- short inline field guidance inside the secondary create/edit windows so users get quick help without overloading the initial landing surface
- title-driven alias suggestions, explicit trigger configuration, and a bottom-of-dialog dynamic invocation examples box inside the secondary create/edit windows
- browse-assisted target selection for `Application`, `Folder`, and `File` that fills the existing validated `Target` field while `Website URL` stays direct-entry only

## Non-Goals

- delete or disable flows
- Action Studio behavior
- taskbar or tray authoring surfaces
- resolution-model changes
- overlay phase changes
- new persisted action kinds
- malformed-source repair logic

## Executed Slices So Far

1. added the safe persistence foundation and catalog reload seam
2. added the type-first create flow
3. added the bounded edit flow with identity-preserving updates
4. tightened target validation for `app`, `folder`, and `file`
5. expanded saved-action inventory reachability so edit is no longer capped to the first six items
6. pivoted the initial NCP authoring entry into a lightweight button-led landing surface with a secondary `Created Tasks` window
7. added browse-assisted target selection for `Application`, `Folder`, and `File` while keeping `Website URL` direct-entry only
8. added the explicit Trigger model, runtime-generated callable phrases, stronger field headers/help icons, and a dynamic examples box for create/edit dialogs

## Idea Impact Analysis And Route Adjustment

- The new idea set refines FB-036 rather than replacing it. The safe create/edit foundation, validation-before-write, reload seam, and bounded inventory editing all remain valid branch truth.
- The strongest route change is at the landing surface. The initial NCP opening should now be treated as a lightweight action launcher rather than a place that carries dense explanatory copy or full task-management detail inline.
- `Create Custom Task` remains in scope for FB-036, but the user-facing route should pivot so the initial surface stays minimal and the detailed help moves into the secondary create/manage windows.
- An explicit `Created Tasks` or task-management entry point remains compatible with FB-036 and now looks like the right follow-through instead of continuing to expand inline entry-state inventory detail.
- Leaving visual room for future buttons such as plugin integration is a forward-compatibility design constraint, not an authorization to add plugin behavior to FB-036.
- Future voice access is a real planning constraint for this lane, but it should be treated as a naming and action-routing requirement rather than as authorization to implement voice in FB-036. The visible actions and windows added here should map cleanly to future voice-addressable intents.
- A user-facing `Active` / `Inactive` toggle for saved tasks should be deferred. It would introduce new persisted enable/disable semantics, new filtering behavior, and a new execution-state policy that goes beyond the current bounded authoring baseline.
- Field-level explanation is now a higher-priority refinement. `Alias`, `Task type`, and `Target` need clearer in-window guidance so users understand what each field does before more advanced target-picking conveniences are layered on top.
- Browse-assisted target selection for the current `Application`, `Folder`, and `File` kinds remains compatible with FB-036 and is a better fit than adding brand-new target kinds right now. It should populate the existing `Target` field rather than introduce a parallel persistence model.
- Additional task kinds beyond `app`, `folder`, `file`, and `url` should remain deferred until runtime behavior actually exists for them.
- A per-task or global browser-selection policy for website tasks crosses into settings and launch-policy territory. That should be deferred to a later settings or built-in-action lane instead of being silently folded into the current authoring branch.
- A visual polish pass for the create/edit window, including the current title-bar look, belongs in planning for this lane but should follow the routing and field-guidance adjustments rather than precede them.

## Planned Resequencing

1. preserve and stabilize the current branch-local validation and support assets so the existing create/edit baseline remains provable and reusable
2. improve field-level help inside the create/edit windows, especially around `Alias`, `Task type`, and `Target`
3. evaluate focused create/edit window visual polish after the routing, explanatory copy, alias suggestions, examples box, and target-picking flow are settled

## Validation And Support Artifact History

- `dev/orin_saved_action_authoring_validation.py`
  Purpose: lane-specific authoring foundation validator for create/update behavior, collision handling, unsafe-source blocking, and write-safe persistence.
  Introduced: when the safe persistence foundation and bounded create/edit baseline were added to FB-036.
  Classification: `baseline`.
  Reuse: extend this first when saved-action draft rules, identity preservation, or persistence semantics change.

- `dev/orin_saved_action_authoring_ui_validation.py`
  Purpose: supporting headless UI validator for create/edit dialog behavior, invalid target rejection, collision messaging, and inventory edit-button mapping.
  Introduced: when the branch moved from persistence-only authoring support into visible create/edit UX.
  Classification: `supporting`.
  Reuse: extend this when dialog controls, labels, type selection, inventory rendering, or button routing change.

- `dev/orin_saved_action_authoring_live_validation.py`
  Purpose: supporting live-style harness that exercises create/edit/reopen behavior with durable reports and saved-actions snapshots without requiring the full interactive desktop gate.
  Introduced: when evidence-backed hardening became required before normal continuation.
  Classification: `supporting`.
  Reuse: keep this as the fast reusable regression layer before a slower interactive OS-level session.

- `dev/orin_saved_action_authoring_interactive_runtime.py`
  Purpose: branch-local runtime helper that launches the real desktop runtime with a deterministic FB-036 runtime-log target for interactive validation.
  Introduced: during the interactive-validation hardening pass on `2026-04-13`.
  Classification: `interactive-only`.
  Reuse: use this when future FB-036 slices need a reproducible interactive runtime launch path with preserved log evidence.

- `dev/orin_saved_action_authoring_interactive_validation.ps1`
  Purpose: branch-local interactive OS-level validation driver for real hotkey, dialog, create/edit, reopen, unsafe-source, and large-inventory scenarios.
  Introduced: during the same `2026-04-13` interactive-validation hardening pass.
  Classification: `interactive-only`.
  Reuse: continue hardening and reuse this as the default FB-036 interactive continuation gate instead of rebuilding one-off probes.

- `dev/logs/fb_036_authoring_live_validation/`
  Purpose: durable report and artifact root for the synthetic/live-style FB-036 validation harness.
  Introduced: when the branch added evidence-backed live validation before continuation.
  Classification: `supporting`.
  Reuse: keep reports and snapshots here so future slices can compare behavior against earlier branch-local authoring evidence.

- `dev/logs/fb_036_authoring_interactive_validation/`
  Purpose: durable report and artifact root for interactive OS-level validation runs, including runtime logs, saved-actions snapshots, and branch-local manual-gate evidence.
  Introduced: during the interactive-validation hardening pass on `2026-04-13`.
  Classification: `interactive-only`.
  Reuse: future slices should append new reports here and cite the exact report used for any continuation recommendation.

- `Docs/workstreams/FB-036_saved_action_authoring.md` `## User Test Summary`
  Purpose: canonical repo-level manual-validation contract for the active workstream.
  Introduced: when FB-036 was promoted into a canonical workstream record.
  Classification: `baseline`.
  Reuse: update this whenever user-visible expectations, fail-closed behavior, or the manual continuation checklist changes.

- `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`
  Purpose: required user-facing exported copy of the active FB-036 manual checklist.
  Introduced: when the lane adopted the stronger desktop-export rule for relevant desktop slices.
  Classification: `supporting`.
  Reuse: keep it aligned with the workstream-owned `## User Test Summary` whenever the manual checklist changes.

- Existing shared baseline validators such as `dev/orin_saved_action_source_validation.py`, `dev/orin_interaction_baseline_validation.py`, `dev/orin_overlay_input_capture_helper.py`, and `dev/orin_recoverable_launch_failed_validation.py` remain part of the required validation stack, but they are reused cross-lane infrastructure rather than FB-036-specific artifact owners.

## User Test Summary

### Test Purpose

Confirm that the full FB-036 branch behavior is stable for real desktop use, including:

- safe custom-task creation
- bounded in-place editing
- explicit Trigger configuration with runtime-generated callable phrases
- validation-before-write for every supported target kind
- immediate catalog reload after save
- fail-closed handling for unsafe saved-action sources
- edit reachability for inventories larger than six items
- no regression in the typed-first overlay baseline

### Scenario / Entry Point

Open the desktop overlay on `feature/fb-036-saved-action-authoring` with a healthy `%LOCALAPPDATA%\Nexus Desktop AI\saved_actions.json` source and use the lightweight button-led entry surface as the authoring landing path:

- `Create Custom Task`
- `Created Tasks`

### Setup / Prerequisites

- start from a clean desktop runtime launch on `feature/fb-036-saved-action-authoring`
- keep a safe outside text target open, such as Notepad, so stray typing is easy to spot
- know where `%LOCALAPPDATA%\Nexus Desktop AI\saved_actions.json` lives
- for the large-inventory checks, prepare at least eight valid saved actions in the source
- for the unsafe-source checks, back up `saved_actions.json` before intentionally corrupting it

### Steps To Execute

1. Setup: launch the desktop runtime and open the overlay in its normal typed-first way.
Action: inspect the entry-state panel before typing anything.
Expected Behavior: the overlay opens in the normal entry baseline, the initial landing surface stays lightweight, `Create Custom Task` and `Created Tasks` are both visible, and no inline saved-action detail or `Edit` buttons overload the first surface.
Failure Conditions / Edge Cases: the overlay skips entry state, either top-level button is missing, inline inventory/edit detail still clutters the landing surface, or outside text receives stray typing.

2. Setup: stay in entry state with a healthy saved-action source.
Action: click `Create Custom Task`, choose `Application`, then inspect the dialog before saving anything.
Expected Behavior: the dialog shows stronger headers for `Title`, `Aliases`, `Trigger`, and `Target`; each header has a help icon; inline guidance stays short; `Trigger` offers `Launch`, `Open`, `Launch and Open`, and `Custom`; `Custom` keeps its comma-separated trigger field hidden until selected; and the bottom examples box stays visible near the action buttons.
Failure Conditions / Edge Cases: headers are not visually distinct, help icons are missing, the trigger dropdown is missing, the custom trigger field is always visible, or the bottom examples box is missing.

3. Setup: stay in the same create dialog.
Action: enter `Title = Nexus`, `Aliases = NDAI`, confirm the default trigger for `Application`, then switch `Trigger` to `Launch and Open`.
Expected Behavior: alias suggestions update from the title without overwriting the aliases field; `Application` defaults to `Launch`; the bottom examples box updates live to the current draft and shows only relevant callable phrases like `Nexus`, `NDAI`, `Launch Nexus`, `Open Nexus`, `Launch NDAI`, and `Open NDAI`; and the target-format reminder stays specific to `Application`.
Failure Conditions / Edge Cases: alias suggestions overwrite typed aliases, the default trigger does not match the selected type, the examples box does not update live, irrelevant examples remain visible, or generated trigger phrases are missing.

4. Setup: still in the create dialog.
Action: change `Trigger` to `Custom`, enter `Force Open, Duck Duck Goose`, then use `Browse...` or manual entry to set `Target = notepad.exe` and save.
Expected Behavior: the custom trigger field appears only for `Custom`; the examples box updates to phrases like `Force Open Nexus`, `Duck Duck Goose Nexus`, `Force Open NDAI`, and `Duck Duck Goose NDAI`; standard `Launch` / `Open` phrases disappear from the examples box in this mode; save succeeds; and the new task appears immediately without restart.
Failure Conditions / Edge Cases: the custom trigger field stays hidden, the examples box still shows standard trigger phrases, custom trigger phrases are ignored, or the task only appears after restart.

5. Setup: with the newly created task present.
Action: type callable phrases through the normal overlay input:
`Nexus`
`NDAI`
`Force Open Nexus`
`Duck Duck Goose NDAI`
Expected Behavior: each exact phrase resolves through the existing typed-first path with no fuzzy expansion.
Failure Conditions / Edge Cases: bare title or alias stops working, custom-trigger phrases do not resolve, resolution becomes fuzzy or ambiguous unexpectedly, or restart is required before the new phrases work.

6. Setup: open `Create Custom Task` again.
Action: test invalid creates one at a time:
`Application` with `Target = notepad.exe --help`
`Folder` with `Target = Reports\Daily`
`File` with `Target = C:\Reports\bad?.txt`
`Website URL` with `Target = example.com/docs`
then set `Trigger = Custom` and enter duplicate custom trigger phrases like `Force Open, force open`.
Expected Behavior: each invalid case stays in the dialog, shows a clear explanation for what failed, and writes nothing to disk.
Failure Conditions / Edge Cases: any invalid target or invalid custom trigger set is accepted, the dialog closes anyway, inventory changes, or the error text is vague or missing.

7. Setup: with at least one saved action already present.
Action: attempt collision creates:
use a built-in title like `Open Windows Explorer`
use another saved action's existing title or alias
use wording that collides only through generated trigger phrases, such as creating `Open Nexus` with `Trigger = Launch` after `Nexus` already exists with `Launch and Open`
Expected Behavior: the dialog stays open, collision feedback is clear, and no write occurs.
Failure Conditions / Edge Cases: a colliding action is saved, an existing record is overwritten, or inventory count changes.

8. Setup: with the created task already present.
Action: click `Created Tasks`, then `Edit`, verify current values preload, change `Trigger` to `Open`, change type to `File`, use `Browse...` to choose `C:\Reports\weekly.txt`, and save.
Expected Behavior: the edit dialog preloads the existing title, aliases, trigger choice, and target; type changes still update the default trigger until you deliberately choose a trigger yourself; the same saved action updates in place; and the examples box refreshes to match the edited trigger and target kind.
Failure Conditions / Edge Cases: preload is blank or incomplete, the trigger resets unexpectedly after a manual choice, browse support disappears for `File`, the examples box stays stale, the save creates a duplicate, or refresh only happens after restart.

9. Setup: after the valid edit succeeds.
Action: run the callable phrases that should still work for the edited task, then verify phrases that should no longer work after the trigger change.
Expected Behavior: bare title and bare aliases still work; the current trigger family works; phrases from trigger families you removed no longer resolve for that task.
Failure Conditions / Edge Cases: old trigger phrases still resolve after the trigger mode changed, current trigger phrases do not resolve, or bare title / alias behavior regresses.

10. Setup: prepare at least eight valid saved actions and reopen the overlay.
Action: click `Created Tasks`, scroll the inventory there, find the seventh or eighth saved action, click `Edit`, change it, and save.
Expected Behavior: later items remain reachable through the secondary window, scrolling stays stable, the correct later item opens for editing, and the updated later item refreshes immediately after save.
Failure Conditions / Edge Cases: only the first six items remain editable, `Created Tasks` does not expose later rows cleanly, scroll behavior breaks layout, later `Edit` buttons open the wrong item, or later edits do not refresh correctly.

11. Setup: back up `%LOCALAPPDATA%\Nexus Desktop AI\saved_actions.json`, then intentionally corrupt it with invalid JSON.
Action: reopen the overlay, try `Create Custom Task`, then open `Created Tasks`; if any saved-action rows still show `Edit`, try that too.
Expected Behavior: authoring is blocked cleanly with repair-oriented messaging, no dialog proceeds into a real save path, and the source is not silently rewritten. In a fail-closed invalid-source state, `Created Tasks` may still open for status visibility while edit affordances disappear entirely; that absence is acceptable as long as the UI does not expose a live edit path.
Failure Conditions / Edge Cases: the dialog opens anyway, the source is auto-repaired silently, inventory becomes inconsistent, a live edit path is still reachable against the broken source, or outside text/input-capture behavior regresses while blocked.

### Branch / Slice-Specific Validation Focus

- the entry-state surface remains lightweight and button-led rather than becoming a dense inline management surface
- `Create Custom Task` and `Created Tasks` remain the top-level authoring entry points on the initial NCP opening
- create and edit dialogs now expose an explicit `Trigger` field instead of relying on alias hacks
- `Launch`, `Open`, `Launch and Open`, and `Custom` stay bounded and exact rather than widening into fuzzy language
- custom trigger phrases are comma-separated, user-authored, and persisted separately from aliases
- runtime-generated callable phrases include bare title, bare aliases, trigger + title, and trigger + aliases
- legacy saved actions without trigger fields stay bare-only until rewritten through the new model
- stronger headers and concise help icons improve readability without creating a text wall
- the bottom examples box shows only current callable phrases plus the relevant current target-format reminder
- `Application`, `Folder`, and `File` expose `Browse...` support while still allowing manual target entry
- `Website URL` stays direct-entry only
- generated trigger phrases participate in collision detection before write
- create and edit both route through the shared validation-before-write foundation
- successful saves reload the shared catalog immediately and refresh inventory without restart
- edit preserves saved-action identity instead of creating duplicates
- inventories larger than six saved actions keep every item reachable for editing
- the typed-first baseline and input-capture behavior remain unchanged while authoring is extended

## Related References

- `Docs/feature_backlog.md`
- `Docs/prebeta_roadmap.md`
- `Docs/workstreams/index.md`
- `Docs/workstreams/FB-027_interaction_system_baseline.md`
