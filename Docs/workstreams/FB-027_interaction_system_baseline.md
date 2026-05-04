# FB-027 Interaction System Baseline

## ID And Title

- ID: `FB-027`
- Title: `Interaction system baseline and shared action model`
- Lifetime Dossier Doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`

## Record State

- `Promoted`

## Status

- `Active`

## Current Phase

- Phase: `Hardening`

## Phase Status

- Repo State: `Active Branch`
- Active Branch: `feature/fb-027-shutdown-confirmation-runtime-branch-readiness`
- Workstream: `FB-027 interaction and shared-action runtime follow-through`
- Current Active Canonical Workstream Doc: `Docs/workstreams/FB-027_interaction_system_baseline.md`
- Carried Blocker: `FB-030 Post-Merge Canon Drift / Selected-Next Revalidation Required`
- Carried Blocker Status: `Cleared in BR1 by moving FB-030 to merged-unreleased release-debt truth, clearing stale PR2 merge-watch wording from current-state surfaces, and admitting this FB-027 runtime branch from updated main`
- Selected Runtime Candidate: `FB-027 Interaction and shared-action family anchor`
- Selected Runtime Slice: `WS1 shutdown hotkey confirmation runtime proof`
- Current Branch Readiness Seam: `Branch Readiness BR1 - FB-027 Runtime Admission With Carried FB-030 Post-Merge Blocker`
- Current Branch Readiness Seam Status: `Complete / green`
- Current Workstream Seam: `Workstream WS1 - Shutdown Hotkey Confirmation Runtime Proof`
- Current Workstream Seam Status: `Complete / green`
- Current Hardening Seam: `Hardening H1 - Shutdown Hotkey Confirmation Runtime Validation`
- Current Hardening Seam Status: `Complete / green`
- Next Legal Phase: `Live Validation`

## Branch Class

- `implementation`

## Blockers

None.

## Entry Basis

- PR #108 merged into `main`; GitHub merge truth and watcher verification proof are preserved in the FB-030 historical post-merge trace.
- Release Readiness found FB-030 post-merge canon drift after merge, and current governance requires that escaped drift ride the next legitimate runtime-focused backlog branch's Branch Readiness before implementation starts.
- The user explicitly directed Codex to admit a real runtime candidate instead of waiting in a no-candidate stop-state.
- FB-027 is the strongest admissible runtime candidate because it is a user-facing feature-family anchor, has `Priority: High`, and its own released baseline names shutdown-hotkey confirmation as future runtime work before Beta.

## Exit Criteria

- FB-030 no longer appears as the active implementation branch on merged-main current-state surfaces.
- FB-030 is represented as merged-unreleased release debt for `v1.6.13-prebeta`.
- PR #108 merge truth, forced watcher verification, watcher cleanup proof, FB-049 historical merge truth, and pending release posture remain preserved.
- FB-027 is recorded as the active runtime-focused Branch Readiness branch.
- The first bounded runtime slice is explicitly admitted with affected surfaces, non-goals, validation requirements, and rollback path.
- Branch governance validation, automation observability, and diff checks pass before Workstream begins.

## Rollback Target

- `Branch Readiness`

Rollback Path: revert the FB-027 Branch Readiness admission commit and return to updated main at the PR #108 merge commit if the admitted runtime candidate is abandoned.

## Next Legal Phase

- `Live Validation`

## Branch Objective

- Add a bounded, user-visible confirmation step for shutdown hotkeys without changing overlay command resolution, saved-action behavior, relaunch ownership, tray behavior, or broader interaction architecture.
- Repair the carried FB-030 post-merge source-of-truth drift before any FB-027 runtime implementation begins.

## Active Seam

Active seam: `Hardening H1 - Shutdown Hotkey Confirmation Runtime Validation`

- `Branch Readiness BR1 - FB-027 Runtime Admission With Carried FB-030 Post-Merge Blocker`
- Seam Status: `Complete / green`
- `Workstream WS1 - Shutdown Hotkey Confirmation Runtime Proof`
- Seam Status: `Complete / green`
- `Hardening H1 - Shutdown Hotkey Confirmation Runtime Validation`
- Seam Status: `Complete / green`

## Expected Seam Families And Risk Classes

- Workstream: `WS1 shutdown hotkey confirmation runtime proof`; Risk Class: `runtime/user-facing shutdown path`.
- Hardening: validate confirmation accept, cancel, timeout/no-action, and active-session preservation without widening overlay or saved-action behavior.
- Live Validation: require real or closest live-equivalent shutdown-hotkey evidence before PR Readiness.
- PR Readiness: require live PR validation, watcher provisioning/routing proof, and PR2 merge-watch handling before Release Readiness.

## User Test Summary Strategy

- Shutdown hotkey confirmation is user-facing and must produce either direct user-facing shortcut validation proof or an explicit waiver before PR Readiness.
- User validation should cover affirmative confirmation, cancellation/session preservation, and no false shutdown claim when confirmation is declined or expires.

## Later-Phase Expectations

- Workstream may implement only the admitted shutdown-confirmation slice and its validators.
- Hardening must prove the runtime markers are truthful and that existing overlay, saved-action, and callable-group flows remain unchanged.
- Live Validation must digest user-facing shortcut applicability before PR Readiness.
- PR Readiness must provision and prove the current-PR watcher before PR1 can be green.

## Target End-State

- `Ctrl+Alt+End` and `Ctrl+Alt+2` request shutdown confirmation instead of immediately shutting down during normal desktop runtime.
- An affirmative confirmation proceeds through the existing shutdown path and emits truthful runtime markers.
- A decline or timeout preserves the active desktop session and emits truthful cancellation or no-shutdown markers.
- Existing overlay entry, choose, confirm, result, saved-action, callable-group, and built-in-action flows remain unchanged.

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing`
Docs-Only Workstream: `No`
Planning-Loop Bypass User Approval: `None`
Planning-Loop Bypass Reason: `None`

- This is a runtime-focused branch. Governance/source-of-truth repairs are admitted only as carried blockers that must clear before implementation starts.

## Slice Continuation Policy

Slice Continuation Default: `same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

- Additional FB-027 interaction/shared-action slices may continue on this branch only if they remain inside the same shutdown-confirmation risk envelope and validation authority.
- Broader saved-action authoring, Action Studio, routines, profiles, plugin integration, voice invocation, tray redesign, built-in catalog expansion, hotkey remapping, and unrelated UX redesign remain out of scope.

## Backlog Completion Strategy

Branch Completion Goal: `Complete the admitted shutdown-confirmation runtime proof unless validation exposes a future-dependent blocker.`
Known Future-Dependent Blockers: `None proven during Branch Readiness.`
Branch Closure Rule: `Do not widen beyond shutdown confirmation without explicit same-branch scope admission.`

## Backlog Completion Status

Backlog Completion State: `Implemented Complete`
Remaining Implementable Work: `None`
Future-Dependent Blockers: `None`
Completion Status: `Green`

- WS1 implements the admitted shutdown-hotkey confirmation runtime proof without changing overlay command resolution, saved actions, callable groups, tray behavior, relaunch ownership, hotkey mappings, or release packaging.
- Additional FB-027 work remains out of scope unless a later same-branch seam is explicitly admitted under the slice continuation policy.

## Admitted Implementation Slice

- Slice ID: `WS1 shutdown hotkey confirmation runtime proof`
- Goal: prove shutdown hotkeys enter an explicit confirmation path before shutdown while preserving active-session ownership and the existing overlay interaction contract.
- Runtime/User-Facing Delta: shutdown hotkeys become confirm-before-exit instead of immediate shutdown during normal desktop runtime.
- Exact Affected Paths:
  - `desktop/orin_desktop_main.py`
  - `desktop/hotkeys.py`
  - `desktop/desktop_renderer.py`
  - `dev/orin_desktop_entrypoint_validation.py`
  - `dev/orin_interaction_baseline_validation.py`
- In-Scope:
  - shutdown-hotkey confirmation request, accept, cancel, and timeout/no-action truth
  - runtime markers for requested, accepted, cancelled, and completed shutdown confirmation states
  - validator coverage for confirmation acceptance and cancellation/preservation behavior
  - source-of-truth status updates required for the active branch
- Out-Of-Scope:
  - changing command overlay saved-action resolution
  - changing built-in catalog entries
  - changing tray menu structure
  - adding Action Studio, routines, profiles, plugin integration, or voice invocation
  - remapping hotkeys or removing existing shutdown hotkeys
  - changing relaunch ownership, single-instance semantics, startup behavior, or release packaging
- Rollback Boundary: revert WS1 runtime and validator changes plus WS1 status/proof docs while preserving the BR1 carried FB-030 canon repair unless the entire branch is abandoned.

## Initial Workstream Seam Sequence

Seam 1: `WS1-A - Shutdown Confirmation Surface Map`
Goal: locate the existing shutdown-hotkey path and define the smallest confirmation surface that can reuse current desktop runtime primitives.
Scope: inspect `desktop/orin_desktop_main.py`, `desktop/hotkeys.py`, and renderer-facing surfaces; no implementation beyond preparation if needed.
Non-Includes: no overlay command model redesign, no saved-action changes, no tray redesign.

Seam 2: `WS1-B - Confirmation Runtime Behavior`
Goal: implement the minimal confirmation behavior and runtime markers for accept/cancel paths.
Scope: bounded runtime changes in the admitted paths.
Non-Includes: no new feature family behavior beyond shutdown confirmation.

Seam 3: `WS1-C - Validation And Continuation Decision`
Goal: validate acceptance, cancellation/session preservation, desktop entrypoint compatibility, and interaction baseline preservation.
Scope: validator updates, validation evidence, and continuation decision only.
Non-Includes: no PR creation or release work.

## Branch Readiness BR1 Result

- Source-of-Truth Determination: FB-027 is selected as the next legitimate runtime-focused backlog branch by explicit user direction plus backlog priority and future-work readiness.
- Candidate Basis: FB-027 is a user-facing feature-family anchor with `Priority: High`; its released baseline explicitly names shutdown-hotkey confirmation as future runtime work before Beta.
- Carried Blocker Classification: `FB-030 Post-Merge Canon Drift / Selected-Next Revalidation Required`.
- Carried Blocker Repair: FB-030 is moved to merged-unreleased release-debt truth for `v1.6.13-prebeta`, stale PR2 merge-watch wording is removed from current-state surfaces, PR #108 merge/watcher proof remains historical traceability, and FB-027 becomes the active runtime branch.
- Governance Hardening: PR Readiness now carries `Next Runtime Candidate Selection Pending` as a hard blocker until exactly one real runtime candidate is selected, scoped, mirrored in roadmap, and left unbranched for the next Branch Readiness pass.
- First Runtime Slice Candidate: `WS1 shutdown hotkey confirmation runtime proof`.

## Workstream WS1 Result

- Runtime Path Located: `desktop/hotkeys.py` emitted direct shutdown through `ShutdownBus.shutdown_requested`; `desktop/orin_desktop_main.py` consumed that signal and immediately entered `do_shutdown()`.
- Runtime Behavior Changed: `Ctrl+Alt+End` and `Ctrl+Alt+2` now emit `shutdown_confirmation_requested` and route through an explicit confirmation gate before shutdown.
- Prompt Behavior: the normal runtime displays a top-level confirmation prompt asking whether to shut down Nexus Desktop AI.
- Accepted Path: accepted confirmation emits `RENDERER_MAIN|SHUTDOWN_CONFIRMATION_ACCEPTED|source=hotkey` and `RENDERER_MAIN|SHUTDOWN_CONFIRMATION_CLEAN_SHUTDOWN_REQUESTED|source=hotkey`, then proceeds through the existing `RENDERER_MAIN|SHUTDOWN_REQUESTED` and renderer shutdown path.
- Cancelled Path: declined confirmation emits `RENDERER_MAIN|SHUTDOWN_CONFIRMATION_CANCELLED|source=hotkey` and `RENDERER_MAIN|SHUTDOWN_CONFIRMATION_SESSION_PRESERVED|source=hotkey|reason=cancelled` without calling shutdown.
- Timeout Path: unanswered confirmation expires to `RENDERER_MAIN|SHUTDOWN_CONFIRMATION_TIMEOUT|source=hotkey` and `RENDERER_MAIN|SHUTDOWN_CONFIRMATION_SESSION_PRESERVED|source=hotkey|reason=timeout` without calling shutdown.
- Validation Proof: `dev/orin_interaction_baseline_validation.py` proves both shutdown hotkeys route to confirmation rather than direct shutdown and proves accepted, cancelled, and timeout marker truth.
- Live-Equivalent Runtime Proof: `dev/orin_desktop_entrypoint_validation.py` now runs harness shutdown with `NEXUS_SHUTDOWN_CONFIRMATION_DECISION=accepted` and validates the confirmation-requested, accepted, and clean-shutdown-request markers before the existing clean shutdown markers.
- WS1 Continuation Decision: Workstream WS1 is complete / green; next legal phase is `Hardening H1 - Shutdown Hotkey Confirmation Runtime Validation`.

## Hardening H1 Result

- Phase Admission: branch authority advanced from `Workstream` to `Hardening` and admitted `Hardening H1 - Shutdown Hotkey Confirmation Runtime Validation`.
- Confirmation Behavior Finding: both shutdown hotkeys still route to confirmation instead of direct shutdown.
- Accepted Path Finding: accepted confirmation emits accepted and clean-shutdown-request markers, then proceeds through the existing shutdown path.
- Cancelled Path Finding: cancelled confirmation emits cancellation plus session-preserved markers and does not request shutdown.
- Timeout Path Finding: timed-out confirmation emits timeout plus session-preserved markers and does not request shutdown.
- Runtime Preservation Finding: cancellation and timeout preserve the active session/runtime state by withholding `RENDERER_MAIN|SHUTDOWN_REQUESTED`.
- Compatibility Finding: interaction baseline, desktop entrypoint, and boot transition validation remain green after the confirmation gate.
- Automation Observability Finding: current automation observability findings remain review inputs outside the WS1 runtime behavior; no H1 runtime repair candidate is admitted.
- H1 Continuation Decision: Hardening H1 is complete / green; next legal phase is `Live Validation LV1 - Shutdown Hotkey Confirmation Live Validation`.

## Seam Continuation Decision

Seam Status: `Green`
Slice Status: `Green`
Completion Status: `Green`
Waiver Status: `None`
Continue Decision: `Stop`
Stop Basis: `Workstream Green`
Stop Condition: `None`
Continuation Action: `Advance to Live Validation LV1 for shutdown-hotkey confirmation live validation.`
Decision Basis: `Hardening H1 is complete / green and requires Live Validation before any PR Readiness move.`
Next Active Seam: `Live Validation LV1 - Shutdown Hotkey Confirmation Live Validation`

## Current Release-Truth Note

- the baseline-and-URL milestone in this workstream was the first released FB-027 milestone through `v1.2.8-prebeta`
- the later saved-action inventory and guided-access follow-through is now also released in `v1.2.9-prebeta`
- the released follow-through adds:
  - entry-state saved-action inventory
  - built-in-vs-saved distinction in choose and confirm
  - source-health visibility and guided access for missing, invalid, or colliding saved-action sources
  - directly coupled validator expansion for inventory, origin, and source-state visibility
- the branch that carried that later runtime milestone also carried future-lane planning material, but those planning notes are not themselves released runtime behavior
- release truth no longer treats the inventory-and-guided-access follow-through as unreleased; it is now part of the released FB-027 baseline through `v1.2.9-prebeta`

## Release Stage

- `pre-Beta`

## Target Version

- `v1.2.9-prebeta`

## Purpose / Why It Matters

Define the current typed-first interaction system as an explicit baseline contract and use that locked baseline to deliver the first bounded FB-027 capability milestone.

This workstream exists so future interaction work can extend a defended baseline instead of silently rewriting one.

## Current Truth And Boundaries

- the current shipped interaction surface is the typed desktop command overlay
- the current open hotkeys are `Ctrl+Alt+Home` and `Ctrl+Alt+1`
- the current shutdown hotkeys are `Ctrl+Alt+End` and `Ctrl+Alt+2`
- the current overlay flow is bounded to `entry` -> `choose` -> `confirm` -> `result`
- built-in actions and saved actions resolve through one shared action catalog
- the current saved-action seam lives at `%LOCALAPPDATA%/Nexus Desktop AI/saved_actions.json`
- current saved-action target kinds are `app`, `folder`, `file`, and `url`
- current repo truth does not yet include shipped voice invocation, Action Studio authoring UI, routines, profiles, or broader natural-language resolution
- this workstream locked the typed-first baseline and released the first-class URL saved-action target milestone through the existing shared action model
- this workstream now also includes the later released saved-action inventory and guided-access follow-through above that earlier URL-target milestone

## Milestone Value Statement

If squashed to one milestone, this lane is still worthwhile because it turns the current interaction surface into an explicit contract and then proves that the first bounded capability expansion can land without changing resolution rules, state-machine boundaries, or input-capture behavior.

## Scope

- formalize the current typed-first interaction contract
- define the explicit interaction invariants that future work must defend
- identify which behaviors are baseline guarantees versus implementation details
- define the validator surfaces that must exist before capability expansion proceeds
- implement first-class URL target support for saved actions through the existing shared action model
- extend validator coverage so URL targets are defended as part of the locked baseline
- implement and release a later follow-through that adds saved-action inventory, built-in-vs-saved origin visibility, and guided access without changing exact-match resolution or the typed-first state machine
- extend validator coverage so inventory, origin, and saved-source-state visibility are defended as part of the same bounded released interaction lane
- record directly related deferred follow-through that should remain out of scope for this pass

## Non-Goals

- capability expansion beyond bounded first-class URL target support
- saved-action authoring UX
- voice invocation
- Action Studio
- routines or profiles as shipped features
- fuzzy or semantic intent resolution
- runtime hotkey or shutdown-behavior changes in this pass
- broader diagnostics-policy changes

## Interaction Contract

### Invocation Contract

Guaranteed now:

- the command overlay opens through `Ctrl+Alt+Home` and `Ctrl+Alt+1`
- shutdown remains available through `Ctrl+Alt+End` and `Ctrl+Alt+2`
- opening from the supported overlay hotkeys permits immediate typed interaction without requiring an initial click

Not guaranteed now:

- custom hotkeys
- alternative invocation surfaces
- voice invocation
- shutdown confirmation prompts
- permanent retention of the numeric overlay or shutdown hotkeys through Beta

Must not regress:

- supported overlay hotkeys must continue to open the command surface reliably until an explicitly approved future milestone changes them
- supported shutdown hotkeys must remain predictable until an explicitly approved future milestone changes that path
- initial typing must not leak into the previously focused underlay target

### Overlay State Machine Contract

Guaranteed now:

- the visible interaction flow is bounded to `entry`, `choose`, `confirm`, and `result`
- one exact resolved match moves from `entry` to `confirm`
- ambiguous resolved matches move from `entry` to `choose`
- confirmed execution transitions to `result`
- `Esc` backs out from `choose` or `confirm` to `entry`

Not guaranteed now:

- extra intermediate review phases
- richer multi-step workflows
- alternate execution paths that bypass confirmation

Must not regress:

- the overlay must stay bounded and understandable
- execution must not skip the visible confirmation step
- cancel/back-out behavior must continue to return the user to a clean `entry` state

### Resolution Contract

Guaranteed now:

- command resolution is exact normalized matching against action titles and aliases
- one match yields a confirmable pending action
- multiple matches yield a visible ambiguous-choice state
- zero matches yield a bounded `not_found` state instead of hidden guessing

Not guaranteed now:

- fuzzy matching
- semantic inference
- routines, profiles, or other higher-order command abstractions
- broader natural-language understanding beyond the current normalized title-and-alias model

Must not regress:

- the interaction surface must resolve through one inspectable catalog
- ambiguous outcomes must remain explicit rather than silently choosing a guessed action
- `not_found` must remain bounded and visible

### Saved-Action Contract

Guaranteed now:

- saved actions are sourced from `%LOCALAPPDATA%/Nexus Desktop AI/saved_actions.json`
- built-in actions and saved actions share one effective catalog shape
- supported saved-action target kinds are currently `app`, `folder`, `file`, and `url`
- valid saved-action URL targets open through the existing system-handler launch path
- missing, unreadable, invalid, or colliding saved-action sources fall back to built-ins only

Not guaranteed now:

- a saved-action authoring UI
- partial salvage of malformed saved-action files
- richer target kinds beyond `url`
- routine or profile schemas

Must not regress:

- a bad saved-action source must not break the command overlay
- built-in actions must remain available even when the saved-action source is invalid
- collision handling must stay bounded and predictable
- URL targets must not bypass the shared catalog, confirmation path, or bounded result flow

### Input Capture / Focus Ownership Contract

Guaranteed now:

- fallback global capture owns text, `Enter`, `Esc`, and backspace while the overlay is in no-click entry mode and true local ownership is not yet established
- true manual local focus transfers ownership to the local input field
- outside click suspends no-click fallback capture instead of mirroring typing into the underlay and overlay at the same time
- choose and confirm paths preserve human-delay capture behavior when local focus has not yet been re-established

Not guaranteed now:

- the exact timer values used for launch grace or capture rearm
- any specific renderer timing beyond the behavioral contract above

Must not regress:

- no-click open must remain reliable
- local manual focus takeover must stand fallback capture down
- outside click must keep the overlay from silently mirroring input
- human-delay choose and confirm behavior must remain usable

### Result / Cleanup Contract

Guaranteed now:

- result display clears stale input text, last request text, pending action, and pending ambiguous-match state immediately
- close-and-reopen after success, failure, timeout close, or manual close returns to a clean baseline
- the result state remains bounded and transient rather than becoming a second execution phase

Not guaranteed now:

- exact result copy
- exact result timeout duration
- exact visual layout

Must not regress:

- stale request or confirmation metadata must not survive into the next reopen cycle
- result closure must not leave the command surface in a half-armed state

### Failure / Non-Success Boundary

Guaranteed now:

- `not_found`, `ambiguous`, and launch-failed paths remain bounded inside the current interaction surface
- launch-failed handling preserves the existing manual-reporting boundary
- interaction work does not widen into new diagnostics policy automatically

Not guaranteed now:

- broader recoverable-diagnostics expansion
- automatic reporting
- a richer non-success UX beyond the current bounded result path

Must not regress:

- interaction work must not silently widen reporting, diagnostics, or escalation behavior
- non-success states must remain explicit and bounded

## Invariants

### Behavioral Invariants

- opening the overlay from a supported hotkey must permit immediate typed interaction without an initial click
- `Enter` must never execute a command before the user reaches and accepts the confirm state
- ambiguous requests must require explicit user choice
- `Esc` in `choose` or `confirm` must back out to `entry`
- missing or invalid saved-action sources must degrade to the built-in baseline rather than to a broken overlay

### State Invariants

- `hidden` means no visible overlay state and no pending interaction state
- `entry` means editable request-building state
- `choose` means an ambiguous bounded match set exists
- `confirm` means exactly one pending action is active
- `result` means transient execution state has already been cleared

### Transition Invariants

- `entry` -> `confirm` only on exactly one resolved action
- `entry` -> `choose` only on more than one resolved action
- `choose` -> `confirm` only through explicit user selection
- `choose` -> `entry` and `confirm` -> `entry` must clear stale pending metadata
- `result` -> reopen must restore a clean `entry` baseline

### Fallback Invariants

- fallback capture must not remain active after true local manual focus ownership is established
- fallback capture must not keep mirroring typing after outside-click suspension
- expired capture must stand down instead of intercepting unrelated input
- saved-action fallback must never remove built-ins from the effective catalog
- interaction follow-through must not widen the bounded non-success and reporting contract accidentally

## Validation Coverage And Required Defenses

### Existing Validation Coverage

The current baseline is now defended by:

- `dev/orin_overlay_input_capture_helper.py`
- `dev/orin_shared_action_baseline_validation.py`
- `dev/orin_saved_action_source_validation.py`
- `dev/orin_interaction_baseline_validation.py`

Together, these surfaces now exercise:

- first-open immediate typing
- no-click entry behavior
- local-focus takeover
- outside-click suspension
- choose and confirm human-delay capture behavior
- cancel/retry state cleanup
- result cleanup and clean reopen after success, failure, timeout close, and manual close
- one choose-confirm-execute path
- hotkey launch-grace behavior
- shutdown-hotkey continuity
- underlay suppression for fallback text and submit behavior
- exact-match shared-action resolution behavior
- explicit ambiguous-match behavior
- built-in catalog integrity
- valid saved-action catalog extension behavior
- valid URL saved-action catalog extension behavior
- saved-action inventory visibility and correctness
- built-in-vs-saved origin visibility in choose and confirm
- source-health visibility for missing, invalid, and colliding saved-action sources
- missing, empty, invalid, unsupported, duplicate, and colliding saved-action fallback behavior
- invalid URL saved-action fallback behavior
- URL launch-path behavior without Windows path normalization
- compact end-to-end typed-first `entry` -> `choose` -> `confirm` -> `result` behavior
- compact end-to-end typed-first URL confirm/result behavior
- compact end-to-end entry-state inventory guidance behavior

### Missing Explicit Validator Surfaces

No baseline-blocking validator gap is currently known for the locked typed-first interaction contract.

Future capability-expansion milestones may require additional validators when they deliberately change invocation surfaces, resolution behavior, authoring behavior, or non-success handling.

### Required Validator Surfaces Before Capability Expansion

Before capability expansion proceeds, the baseline must continue to be defended by:

- the existing overlay input-capture helper retained as a baseline regression surface
- a dedicated shared-action baseline validator
- a dedicated saved-action-source validator
- a compact integration validator proving the shipped typed-first contract still holds end to end

### What Expansion Must Defend

Future expansion work must preserve or explicitly re-negotiate:

- invocation reliability
- state-machine boundedness
- explicit confirmation before execution
- explicit ambiguity handling
- bounded saved-action fallback behavior
- clean result and reopen behavior
- the existing manual-reporting and non-success boundary

## Expansion Boundaries

### Baseline Guarantees

The guarantees in this document define the current typed-first baseline that future work must treat as protected behavior unless a later approved milestone explicitly changes it.

### Implementation Details

Current implementation details include:

- exact timer values for launch grace and capture rearm
- exact starter built-in action list and alias wording
- exact status or panel copy
- exact presentation layout details

Those details may change later without violating the baseline if the protected contract stays intact.

### Future Capabilities

Future capabilities explicitly deferred beyond this pass include:

- saved-action authoring UX
- explicit user-facing action-type selection for future saved-action authoring flows
- routines
- profiles
- richer saved-action target kinds beyond `url`
- curated built-in system-action expansion beyond the current starter built-in catalog
- broader natural-language resolution
- voice invocation
- Action Studio
- broader shortcut customization
- taskbar or tray quick-task surfaces such as Create Custom Task
- external trigger and plugin integration architecture
- monitoring, thermals, and performance HUD surfaces

### Deferred Follow-Through Recorded Now

The following directly related FB-027 follow-through is recorded now but not implemented in this pass:

- remove `Ctrl+Alt+1` and `Ctrl+Alt+2` before Beta
- add an `Are you sure you want to exit?` prompt for shutdown hotkeys before Beta
- select the next capability-expansion milestone only through fresh post-release analysis on updated `main`
- future saved-action authoring should present an explicit user-facing type choice without silently redefining the current saved-action contract
- future curated built-in system actions should be tracked separately from user-defined saved-action customization
- future taskbar or tray Create Custom Task affordances, plugin-trigger surfaces, and monitoring HUD work should remain explicit adjacent lanes rather than implicit same-branch continuation

These are deferred forward items, not current-runtime guarantees.

## Stages / Executed Stages

1. promoted FB-027 into a canonical workstream
2. formalized the current typed-first interaction contract
3. defined enforceable invariants
4. mapped current validation coverage and missing validator surfaces
5. added dedicated shared-action, saved-action-source, and compact end-to-end interaction baseline validators
6. re-validated the retained overlay input-capture helper against the current renderer contract
7. recorded directly related deferred follow-through without widening into capability implementation
8. added first-class URL target support to the saved-action seam and shared action model without changing exact-match resolution
9. extended shared-action, saved-action-source, and integration validators to defend the new URL target capability
10. added entry-state saved-action inventory and guided access through the existing typed-first overlay
11. surfaced built-in-vs-saved origin detail plus saved-source health visibility without changing exact-match resolution, state-machine boundedness, or input-capture behavior
12. extended validator coverage to defend inventory, origin, and source-state visibility as part of the merged unreleased follow-through

## Same-Branch Follow-Through

The originally released URL-target milestone is no longer the only released execution truth in this record.

The later inventory-and-guided-access follow-through is now also released in `v1.2.9-prebeta`.

Future runtime or capability work beyond those released steps must still return as an explicitly selected next FB-027 milestone rather than as silent continuation.

## Blockers / Holds / Stop Conditions

- do not widen the URL-target milestone into broader saved-action, resolution, or interaction-surface expansion
- do not widen this workstream into runtime behavior changes without explicit approval
- do not treat deferred hotkey cleanup or shutdown confirmation work as current guarantees

## User Test Summary

This workstream now includes user-facing saved-action capability changes beyond the original URL-target milestone, so a workstream-owned User Test Summary should still be considered before any future release promotion that extends FB-027 beyond the currently released inventory-and-guided-access follow-through.

Future user-facing interaction changes should assume a workstream-owned User Test Summary will likely be needed before closure.

## Baseline Lock Summary

The typed-first interaction baseline remains explicit and validator-defended. The released URL-target milestone and the later released inventory-and-guided-access follow-through both extend that baseline without redefining the state machine, exact-match resolution, or input-capture contract.

## Deferred Forward

- remove `Ctrl+Alt+1` and `Ctrl+Alt+2` before Beta
- add an `Are you sure you want to exit?` prompt for shutdown hotkeys before Beta
- choose the next capability-expansion milestone only through fresh post-release analysis on updated `main`
- if saved-action authoring is selected later, keep explicit user-facing type selection downstream of the bounded shared action model rather than turning it into Action Studio by inertia
- keep standard Windows and Nexus-owned actions as future curated built-ins rather than forcing them into user-defined saved actions
- keep taskbar or tray Create Custom Task work, plugin integration, and monitoring HUD surfaces as separate explicit lanes unless a future approved workstream intentionally merges them

## Related References

- `Docs/feature_backlog.md`
- `Docs/prebeta_roadmap.md`
- `Docs/workstreams/index.md`
- `Docs/orin_interaction_architecture.md`
- `Docs/ncp_hardening_assessment.md`
