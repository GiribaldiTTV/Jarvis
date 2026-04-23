# FB-030 ORIN Voice/Audio Direction Refinement

## Identity

- ID: `FB-030`
- Title: `ORIN voice/audio direction refinement`

## Record State

- `Promoted`

## Status

- `Active`

## Release Stage

- `pre-Beta`

## Canonical Branch

- `feature/fb-030-orin-voice-audio-direction-refinement`

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- `Branch Readiness is complete on feature/fb-030-orin-voice-audio-direction-refinement after v1.6.4-prebeta release publication, live validation, and post-release canon closure.`
- FB-015 and FB-029 are released and closed in `v1.6.4-prebeta`.
- Latest public prerelease truth is `v1.6.4-prebeta`.
- Release debt is clear after `v1.6.4-prebeta` publication, validation, and post-release canon closure.
- FB-030 now owns active promoted implementation-branch truth on this branch.
- Branch-name reuse is intentional: the earlier emergency repair record with this same branch name remains historical traceability only and does not own live execution authority.
- The voice/audio design goal and affected-surface map are now explicitly recorded before any runtime voice, shutdown voice, recovery voice, diagnostics, UI, asset, or public-claim change is admitted.
- WS-1 current voice/audio surface inventory and ownership map is the admitted next seam.
- No runtime voice behavior, shutdown voice behavior, recovery voice behavior, persona default, public copy, audio asset, or release-note wording change has started.

## Branch Class

- `implementation`

## Blockers

None.

## Entry Basis

- `v1.6.4-prebeta` is live at `d2268b71feefa062c8117eae29f8ec17879a724f`.
- FB-015 and FB-029 release debt is live-cleared and canon is now closed on this branch surface.
- The historical FB-030 repair-only branch records are preserved for traceability, but they do not own current execution truth.
- FB-030 was already selected next in canon and remained blocked only by open release debt plus the missing explicit voice/audio design goal and affected-surface map.
- This Branch Readiness pass supplies that missing planning frame so Workstream can begin without admitting runtime implementation by inertia.

## Exit Criteria

- FB-030 is promoted from `Registry-only` to `Promoted`.
- The branch objective, target end-state, design goal, affected-surface map, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are durably recorded.
- FB-015 and FB-029 are durably closed as released workstreams in `v1.6.4-prebeta`, latest public prerelease truth is advanced, and merged-unreleased release debt is cleared in canon.
- Repo truth routes active branch ownership to FB-030 on `feature/fb-030-orin-voice-audio-direction-refinement`.
- Workstream can begin with WS-1 current voice/audio surface inventory and ownership map without admitting runtime voice/audio implementation.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Workstream`

## Branch Objective

- Define the planning frame for ORIN voice/audio direction before any runtime voice, shutdown voice, recovery voice, persona-default, public-claim, or audio-asset implementation begins.
- Separate persona-facing direction, audio/voice execution mechanics, diagnostics evidence, renderer telemetry, launcher recovery speech, and public identity surfaces so later implementation does not collapse them into one ambiguous lane.
- Establish implementation-admission rules so future work must prove the exact affected surfaces, validation boundary, rollback path, and user-facing impact before changing audible or persona-facing behavior.

## Target End-State

- FB-030 has a canonical planning record for ORIN voice/audio direction, affected surfaces, non-goals, and implementation admission boundaries.
- The branch has an explicit distinction between currently shipped ORIN voice posture, dormant ARIA future-option posture, and current runtime voice/audio execution surfaces.
- Workstream can begin with an inventory seam instead of jumping directly into prompt, asset, shutdown, recovery, or persona-default changes.
- Later implementation remains blocked unless a future seam explicitly admits the exact runtime, UI, diagnostics, asset, release, or public-surface changes it will touch.

## Voice/Audio Design Goal

- Define a deliberate ORIN voice/audio direction that keeps shipped ORIN identity coherent across audible behavior, shutdown/recovery behavior, diagnostics traces, and public-facing explanatory surfaces without treating this branch as a runtime rewrite.
- Keep persona direction separate from execution mechanics: ORIN remains the only shipped persona, ARIA remains future-optional and non-default, and this branch does not silently convert dormant persona posture into live runtime exposure.
- Make future implementation choose specific surfaces on purpose by naming which current voice/audio behaviors belong to the boot prototype, the desktop launcher recovery/shutdown path, renderer telemetry, diagnostics evidence, audio assets, and public explanatory docs.

## Affected-Surface Map

### Runtime and launcher surfaces

- `main.py`: current boot-prototype voice flow, `audio_mode`, `OrinSpeaker` usage, voice visualizer, boot prompts, import prompts, and shutdown prompts.
- `desktop/orin_desktop_launcher.pyw`: launcher-owned recovery voice, shutdown-sequence voice orchestration, and `VOICE_SCRIPT` routing into `Audio/orin_error_voice.py`.
- `desktop/orin_desktop_main.py`: desktop runtime shutdown handoff boundary into renderer shutdown.
- `desktop/desktop_renderer.py`: renderer-side voice-level telemetry bridge and shutdown-facing renderer state.

### Persona and audio-asset surfaces

- `assistant_personas.py`: released-persona gate, default persona, ORIN/ARIA voice ids, and future persona-option boundaries.
- `Audio/orin_voice.py`: current ORIN speech synthesis helper used by the boot prototype path.
- `Audio/orin_error_voice.py`: current shutdown/recovery/error voice synthesis path used by the launcher path.

### Diagnostics and evidence surfaces

- `desktop/orin_diagnostics.pyw`: voice-history and current-voice diagnostics surfaces.
- runtime log markers and launcher diagnostics already emitted by `main.py` and `desktop/orin_desktop_launcher.pyw`.
- voice/audio validation helpers that later seams may reuse once exact implementation scope is admitted.

### Public explanatory and naming surfaces

- `README.md`: current product orientation and `Audio/` ownership note.
- `Docs/orin_vision.md`, `Docs/orin_display_naming_guidance.md`, and `Docs/ownership_ip_plan.md`: current ORIN identity, display posture, and future-option context that later voice/persona changes must respect.

### Explicit non-includes for this branch-readiness pass

- no runtime prompt edits
- no audio asset edits
- no persona-default changes
- no launcher or renderer behavior changes
- no diagnostics implementation changes
- no release-note or public-copy sweep

## Scope

- Record the explicit voice/audio design goal for the lane.
- Record the current affected-surface map across runtime, launcher, renderer, persona registry, diagnostics, audio assets, and public explanatory docs.
- Define the initial seam chain for inventory, lifecycle/persona-state framing, and implementation admission.
- Preserve current shipped ORIN posture and dormant ARIA posture while the lane remains planning-only.

## Non-Goals

- No runtime voice behavior changes.
- No shutdown voice behavior changes.
- No launcher recovery voice changes.
- No audio asset or synthesis-setting changes.
- No UI implementation or visual redesign.
- No diagnostics implementation changes.
- No release-note edits or public-claim changes beyond canon closure.
- No persona-default change or ARIA rollout.
- No broad identity or licensing work; that remains historical FB-029 scope.

## Expected Seam Families And Risk Classes

- Current voice/audio surface inventory and ownership family; risk class: runtime/persona-boundary, because current voice behavior spans boot prototype, launcher recovery, renderer telemetry, diagnostics, and persona registry surfaces.
- Lifecycle and persona-state framing family; risk class: lifecycle/user-facing, because boot speech, shutdown speech, recovery speech, quiet mode, and persona posture can drift unless their boundaries are explicit.
- Diagnostics, telemetry, and evidence-root family; risk class: validation/observability, because later voice changes need durable proof without confusing support evidence with public behavior.
- Public explanatory and persona-claim family; risk class: product/persona, because shipped ORIN posture and future ARIA posture must not blur into accidental public claims.
- Implementation admission and rollback contract family; risk class: governance/implementation, because later voice/audio edits must prove exact affected surfaces, validation triggers, rollback, and user-facing impact before execution.

## Validation Contract

- Run `python dev\orin_branch_governance_validation.py`.
- Run `git diff --check`.
- Confirm `Docs/Main.md` routes this promoted FB-030 workstream record.
- Confirm `Docs/feature_backlog.md` marks FB-030 as `Promoted`, `Active`, cites this canonical workstream doc, and records the canonical branch as `feature/fb-030-orin-voice-audio-direction-refinement`.
- Confirm `Docs/workstreams/index.md` lists FB-030 under Active and lists FB-015 plus FB-029 under Closed.
- Confirm `Docs/prebeta_roadmap.md` advances latest public prerelease truth to `v1.6.4-prebeta`, clears merged-unreleased release debt, records FB-030 as the current active workstream, and no longer leaves FB-015 or FB-029 as merged-unreleased.
- Confirm `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/workstreams/index.md`, `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md`, and `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md` agree that FB-015 and FB-029 are Released / Closed in `v1.6.4-prebeta`.
- Confirm `assistant_personas.py` still keeps `RELEASED_PERSONA_IDS = ("orin",)` and `DEFAULT_PERSONA_ID = "orin"`.
- Confirm the historical repair record at `Docs/branch_records/feature_fb_030_orin_voice_audio_direction_refinement.md` remains traceability-only and does not redefine the live FB-030 implementation branch as an emergency repair branch.
- Confirm no runtime, launcher, renderer, diagnostics, audio asset, persona-default, release, or public-copy implementation changed during this Branch Readiness pass.

## Branch Readiness Validation Results

- `python dev\orin_branch_governance_validation.py`: PASS, 1102 checks.
- `git diff --check`: PASS with line-ending normalization warnings only and no whitespace errors.
- Scope validation: PASS; this pass changes docs/canon routing, branch-truth closure, and validator coverage only.
- Admission validation: PASS; FB-030 is promoted, Branch Readiness is complete, and WS-1 current voice/audio surface inventory and ownership map is the admitted next seam.
- Branch-name reuse validation: PASS; the historical FB-030 repair record remains traceability-only, and active branch truth now belongs to the promoted implementation branch without repair-branch misclassification.

## User Test Summary Strategy

- Branch Readiness and the admitted WS-1 through WS-3 seam chain remain docs/canon only and do not change user-facing behavior.
- No desktop shortcut validation, desktop export, or manual User Test Summary handoff is required during Branch Readiness or the planned docs/canon-only Workstream seams.
- If a later seam changes audible user-facing behavior, visible voice-related UI, public persona copy, shutdown/recovery voice behavior, or another operator-facing surface, FB-030 must add the exact `## User Test Summary` artifact and any required shortcut or desktop export evidence before Live Validation can advance.

## Later-Phase Expectations

- Workstream must execute bounded seams and keep the active seam recorded here.
- Workstream must begin with WS-1 current voice/audio surface inventory and ownership mapping before lifecycle framing or implementation-admission rules are extended.
- Hardening must pressure-test the design goal, affected-surface map, lifecycle/persona-state framing, validation boundaries, and implementation-admission rules.
- Live Validation must classify user-facing shortcut applicability and User Test Summary applicability based on the completed FB-030 delta.
- PR Readiness must prove merge-target canon completeness, clean branch truth, selected-next truth when relevant, PR package details, and live PR state before PR green.
- Any implementation-facing prompt, audio asset, recovery voice, shutdown voice, renderer UI, diagnostics behavior, persona-default, or release/public-surface change requires a later explicit seam admission on this branch and must not enter by inertia.

## Initial Workstream Seam Sequence

Seam 1: Current voice/audio surface inventory and ownership map

- Status: Admitted next.
- Goal: inventory current boot voice, shutdown voice, recovery voice, quiet-mode, renderer telemetry, diagnostics, persona-registry, and audio-asset surfaces before implementation is considered.
- Scope: docs/canon source inventory, ownership mapping, evidence roots, ambiguity capture, and current-vs-future classification.
- Non-Includes: no runtime code edits, no prompt changes, no audio asset changes, no UI changes, no persona-default changes, no diagnostics implementation changes, no release edits, and no public release editing.

Seam 2: Lifecycle and persona-state framing for voice/audio transitions

- Status: Planned.
- Goal: define lifecycle and state vocabulary across boot prototype speech, launcher recovery speech, shutdown speech, quiet mode, renderer telemetry, diagnostics capture, and persona-option boundaries.
- Scope: docs/canon lifecycle framing, ownership handoffs, current-vs-future persona posture, ambiguity capture, and implementation-readiness risks.
- Non-Includes: no runtime code edits, no prompt changes, no audio asset changes, no UI changes, no persona-default changes, no diagnostics implementation changes, no release edits, and no public release editing.

Seam 3: Validation and admission contract for future voice/audio implementation

- Status: Planned.
- Goal: define the proof required before future runtime voice, shutdown voice, recovery voice, asset, UI, diagnostics, or public persona-surface changes begin.
- Scope: validation gates, User Test Summary triggers, user-facing classification, release/public-surface triggers, rollback proof, helper reuse posture, and implementation-admission checklist.
- Non-Includes: no runtime code edits, no prompt changes, no audio asset changes, no UI changes, no persona-default changes, no diagnostics implementation changes, no release edits, and no public release editing.

## Active Seam

Active seam: WS-1 current voice/audio surface inventory and ownership map

- Branch Readiness result: complete and green; Workstream may begin with WS-1.
- WS-1 Status: Admitted next.
- WS-1 Boundary: docs/canon current voice/audio surface inventory and ownership mapping only.
- WS-1 Non-Includes: no runtime code edits, no prompt changes, no audio asset changes, no UI changes, no persona-default changes, no diagnostics implementation changes, no release edits, and no public release editing.
