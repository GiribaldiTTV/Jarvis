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
3. add browse-assisted target selection for the existing `Application`, `Folder`, and `File` task types without changing persisted action kinds
4. evaluate focused create/edit window visual polish after the routing, explanatory copy, and target-picking flow are settled

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

Confirm that the full FB-036 branch behavior is stable for real desktop use:

- safe custom-task creation
- bounded in-place editing
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
- for repeated-stability checks, plan to create or edit at least two saved actions in one session
- for the unsafe-source checks, back up `saved_actions.json` before intentionally corrupting it

### Steps To Execute

1. Setup: launch the desktop runtime and open the overlay in its normal typed-first way.
Action: inspect the entry-state panel before typing anything.
Expected Behavior: the overlay opens in the normal entry baseline, the initial landing surface stays lightweight, `Create Custom Task` and `Created Tasks` are both visible, and no inline saved-action detail or `Edit` buttons overload the first surface.
Failure Conditions / Edge Cases: the overlay skips entry state, either top-level button is missing, inline inventory/edit detail still clutters the landing surface, or outside text receives stray typing.

2. Setup: stay in entry state with a healthy saved-action source.
Action: click `Create Custom Task`, choose `Folder`, enter `Title = Open Reports`, `Aliases = show reports`, `Target = C:\Reports`, then save.
Expected Behavior: the dialog closes, success feedback appears in entry state, and the new saved action appears in inventory immediately without restart.
Failure Conditions / Edge Cases: the dialog closes without feedback, the inventory does not refresh, the overlay leaves entry state unexpectedly, or the source file is not updated.

3. Setup: with `Open Reports` now visible in inventory.
Action: type the exact title or alias into the normal overlay input and execute it through the existing typed-first flow.
Expected Behavior: the overlay still follows the normal `entry -> confirm -> result` path for an exact match, and the new saved action resolves immediately.
Failure Conditions / Edge Cases: no match is found, resolution becomes ambiguous unexpectedly, confirm behavior changes, or the action only works after restart.

4. Setup: open `Create Custom Task` again.
Action: test invalid creates one at a time:
`Application` with `Target = notepad.exe --help`
`Folder` with `Target = Reports\Daily`
`File` with `Target = C:\Reports\bad?.txt`
`Website URL` with `Target = example.com/docs`
Expected Behavior: each invalid case stays in the dialog, shows a clear validation error, and writes nothing to disk.
Failure Conditions / Edge Cases: any invalid target is accepted, the dialog closes anyway, the inventory changes, or the error text is vague or missing.

5. Setup: with at least one saved action already present.
Action: attempt collision creates:
use a built-in title like `Open Windows Explorer`
use another saved action's existing title or alias
Expected Behavior: the dialog stays open, collision feedback is clear, and no write occurs.
Failure Conditions / Edge Cases: a colliding action is saved, an existing record is overwritten, or inventory count changes.

6. Setup: with `Open Reports` already created successfully.
Action: click `Created Tasks`, confirm the secondary window opens, click `Edit` on `Open Reports`, verify the dialog preloads current values, change the title to `Open Weekly Reports`, change the type to `File`, set the target to `C:\Reports\weekly.txt`, and save.
Expected Behavior: the landing surface stays lightweight, the secondary `Created Tasks` window owns the saved-action detail, the edit dialog preloads the existing title, aliases, type, and target; save closes it; success feedback appears; the same saved action updates in place; and the refreshed values are visible without creating a duplicate.
Failure Conditions / Edge Cases: `Created Tasks` does not open, the wrong item opens for editing, blank preload, duplicate item creation, wrong action updated, missing feedback, or refresh only after restart.

7. Setup: edit an existing saved action again.
Action: go back through `Created Tasks`, then try invalid or colliding edits:
change the target to `Reports\Weekly`
change the title to a built-in title
change the title to another saved action's title
Expected Behavior: the dialog stays open, clear errors appear, the original record remains unchanged, and nothing is written.
Failure Conditions / Edge Cases: invalid edits save, collisions overwrite another action, or the original action mutates despite the error.

8. Setup: prepare at least eight valid saved actions and reopen the overlay.
Action: click `Created Tasks`, scroll the inventory there, find the seventh or eighth saved action, click `Edit`, change it, and save.
Expected Behavior: later items remain reachable through the secondary window, scrolling stays stable, the correct later item opens for editing, and the updated later item refreshes immediately after save.
Failure Conditions / Edge Cases: only the first six items remain editable, `Created Tasks` does not expose later rows cleanly, scroll behavior breaks layout, later `Edit` buttons open the wrong item, or later edits do not refresh correctly.

9. Setup: after one or more successful creates or edits.
Action: close the overlay, reopen it, click `Created Tasks`, and inspect the inventory again.
Expected Behavior: the newly created or edited saved actions are still present with their latest values, showing that the change persisted and reload behavior was not only in-memory.
Failure Conditions / Edge Cases: changes disappear after reopen, stale values return, `Created Tasks` no longer opens cleanly, or the overlay reopens with stale typed request / confirm / result state.

10. Setup: after a successful create and a successful edit, keep the same session open.
Action: create or edit one more valid saved action, close the overlay, reopen it again, open `Created Tasks`, and confirm the full inventory state.
Expected Behavior: repeated authoring operations remain stable, inventory count stays correct, updated values persist, and no stale entry/confirm/result state leaks across reopen cycles.
Failure Conditions / Edge Cases: repeated operations create duplicates, later saves disappear on reopen, stale overlay state returns, `Created Tasks` loses sync with the saved-action catalog, or entry-state feedback becomes inconsistent after multiple cycles.

11. Setup: back up `%LOCALAPPDATA%\Nexus Desktop AI\saved_actions.json`, then intentionally corrupt it with invalid JSON.
Action: reopen the overlay, try `Create Custom Task`, then open `Created Tasks`; if any saved-action rows still show `Edit`, try that too.
Expected Behavior: authoring is blocked cleanly with repair-oriented messaging, no dialog proceeds into a real save path, and the source is not silently rewritten. In a fail-closed invalid-source state, `Created Tasks` may still open for status visibility while edit affordances disappear entirely; that absence is acceptable as long as the UI does not expose a live edit path.
Failure Conditions / Edge Cases: the dialog opens anyway, the source is auto-repaired silently, inventory becomes inconsistent, a live edit path is still reachable against the broken source, or outside text/input-capture behavior regresses while blocked.

### Branch / Slice-Specific Validation Focus

- the entry-state surface remains lightweight and button-led rather than becoming a dense inline management surface
- `Create Custom Task` and `Created Tasks` remain the top-level authoring entry points on the initial NCP opening
- the secondary `Created Tasks` window owns saved-action detail visibility and edit reachability
- create and edit both route through the shared validation-before-write foundation
- `app`, `folder`, `file`, and `url` validation all fail closed before disk write
- successful saves reload the shared catalog immediately and refresh inventory without restart
- edit preserves saved-action identity instead of creating duplicates
- malformed or colliding source states block authoring rather than attempting salvage
- invalid-source fail-closed behavior may remove edit affordances entirely instead of exposing a blocked edit button
- inventories larger than six saved actions keep every item reachable for editing
- repeated create/edit/reopen cycles do not leave stale overlay state or orphaned saved-action records
- the typed-first baseline and input-capture behavior remain unchanged while authoring is added

## Related References

- `Docs/feature_backlog.md`
- `Docs/prebeta_roadmap.md`
- `Docs/workstreams/index.md`
- `Docs/workstreams/FB-027_interaction_system_baseline.md`
