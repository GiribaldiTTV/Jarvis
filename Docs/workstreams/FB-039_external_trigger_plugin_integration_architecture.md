# FB-039 External Trigger And Plugin Integration Architecture

## ID And Title

- ID: `FB-039`
- Title: `External trigger and plugin integration architecture`

## Record State

- `Promoted`

## Status

- `Workstream`

## Release Stage

- `pre-Beta`

## Target Version

- `TBD`

## Canonical Branch

- `feature/fb-039-external-trigger-plugin-integration-architecture`

## Current Phase

- Phase: `Workstream`

## Phase Status

- `Active Branch`
- branch: `feature/fb-039-external-trigger-plugin-integration-architecture`
- branch created from updated `main` after FB-038 release/post-release confirmation green
- FB-038 remains `Released (v1.4.1-prebeta)` / `Closed`
- release debt is clear
- no runtime/product implementation has started

## Branch Class

- `implementation`

## Blockers

- None.

## Entry Basis

- `main` was aligned with `origin/main` before branch creation.
- FB-038 is released and closed in `v1.4.1-prebeta`.
- Latest public prerelease truth is `v1.4.1-prebeta`.
- Repo-level admission gate passed: no release debt, no stale FB-038 canon, no active implementation branch, and no existing FB-039 branch.
- FB-039 was selected in backlog and roadmap as the next implementation workstream before this branch was created.
- Branch Readiness is admitted to define the FB-039 source map, lifecycle ownership, trust/safety boundaries, validation contract, non-goals, and first Workstream seam before implementation.
- Branch Readiness durability is committed and pushed; Workstream is admitted for WS-1 only.

## Branch Objective

- Establish the architecture-first authority for FB-039 external trigger and plugin integration before any runtime implementation begins.
- Define how external trigger origins are named, owned, trusted, admitted, validated, and later routed into existing Nexus action authority.
- Keep this branch bounded to external trigger and plugin integration architecture; do not use it to implement Stream Deck, protocol transport, installer, settings, or runtime plugin behavior during WS-1.

## Target End-State

- FB-039 has a durable source map for candidate external trigger origins and the vocabulary needed to discuss ownership without implementation ambiguity.
- Lifecycle ownership is explicit for trigger discovery, registration, enablement, invocation, teardown, failure handling, and user-visible safety boundaries.
- Trust/safety and validation/admission contracts are explicit enough to admit later Workstream implementation seams without inventing validation scope midstream.
- The first Workstream seam is architecture-first, non-implementing, and bounded to source-map plus ownership vocabulary.

## Expected Seam Families And Risk Classes

- Source-map and vocabulary seam family; risk class: architecture/governance because it defines nouns, owners, and system boundaries before runtime code exists.
- Lifecycle and trust/safety seam family; risk class: integration/safety because external inputs can cross user intent, saved-action authority, and local execution boundaries.
- Validation/admission seam family; risk class: validator/governance because later implementation must prove negative paths, trust boundaries, and no unauthorized execution.
- User-facing integration seam family is later-phase only; risk class: desktop/manual validation if future implementation introduces operator-visible trigger setup or invocation behavior.

## User Test Summary Strategy

- Branch Readiness had no meaningful manual User Test Summary because it did not change runtime or user-visible product behavior; WS-1 is also documentation-only and has no meaningful manual User Test Summary.
- If a later Workstream seam introduces user-visible setup, trigger invocation, tray/overlay interaction, settings, prompt, or desktop shortcut behavior, the workstream must add a User Test Summary section and follow the returned-results blocker model before Live Validation or PR Readiness can advance.
- If later implementation remains headless or architecture-only, the workstream must explicitly record why no meaningful manual User Test Summary applies.

## Later-Phase Expectations

- Workstream began only after this Branch Readiness scaffold became durable and Seam 1 was explicitly admitted.
- Hardening must pressure-test trust boundaries, lifecycle cleanup, negative-path handling, and regression risk against saved-action, callable-group, overlay, tray, and built-in catalog baselines if implementation touches those paths.
- Live Validation is required only if FB-039 introduces user-visible desktop behavior or operator-facing integration setup; otherwise validation may remain repo-side with a documented no-meaningful-manual-test rationale.
- PR Readiness must confirm no helper sprawl, no scope drift into FB-040 monitoring/HUD, no unapproved runtime/plugin surface, and no stale release or branch-authority canon.

## Initial Workstream Seam Sequence

### Seam 1: External Trigger Source Map And Ownership Vocabulary

- Goal: define candidate trigger-origin classes, ownership nouns, authority boundaries, and non-runtime vocabulary for later implementation planning.
- Scope: document source categories, owner roles, allowed/disallowed trigger authority, and how the existing saved-action/callable-group/confirmation model constrains future trigger behavior.
- Non-Includes: no plugin runtime, no Stream Deck integration, no protocol transport, no installer work, no settings UI, no trigger execution, and no helper creation.

### Seam 2: Trigger Lifecycle And Trust/Safety Contract

- Goal: define the lifecycle and safety contract for discovery, registration, enablement, invocation request handling, teardown, failure visibility, and blocked input paths.
- Scope: map lifecycle states and trust decisions needed before any executable integration code is admitted.
- Non-Includes: no lifecycle implementation, no persisted schema changes, no external device/API integration, and no user-facing setup surface.

### Seam 3: Validation And Admission Contract For Later Implementation Seams

- Goal: define the validation families, runtime markers, negative-path proof, cleanup proof, and user-facing/manual gates required before implementation seams can be admitted.
- Scope: specify what later validators or helper reuse must prove and when helper creation would be justified under the registry.
- Non-Includes: no new validator/helper creation during WS-1 or WS-3 planning unless a concrete validation gap blocks later implementation admission.

## Active Seam

- Active seam: `WS-1 External Trigger Source Map And Ownership Vocabulary`.
- WS-1 status: active in this pass and architecture-only.
- WS-2 status: planned only.
- WS-3 status: planned only.

## WS-1 External Trigger Source Map

An external trigger source is a local or locally-adjacent origin outside the core Nexus command overlay that asks Nexus to consider starting an action, workflow, or future plugin-owned entry path.

External trigger sources are not themselves Nexus action authority. They may request attention or route a trigger request into a Nexus-owned entry point, but they do not bypass Nexus confirmation, saved-action authority, callable-group behavior, trust boundaries, or user-visible failure handling.

Candidate trigger-origin categories for FB-039 planning:

- Hardware-adjacent trigger tools: local devices or device-control applications that expose user-initiated buttons, macro keys, decks, or equivalent physical/near-physical trigger surfaces.
- Desktop automation tools: local automation utilities that can initiate user-configured actions or shortcuts from the desktop environment.
- Local companion apps: installed local applications that could request Nexus action handling through a future approved integration path.
- Future plugin-hosted sources: Nexus-adjacent plugin surfaces that may later host trigger affordances once lifecycle, trust/safety, and validation contracts exist.
- Explicitly unsupported origins for WS-1: remote network callers, untrusted web pages, cloud webhook ingress, background services without user-visible ownership, arbitrary script injection, and any source that would require transport or security enforcement design in this seam.

## WS-1 Ownership Vocabulary

- External trigger: a user-initiated or tool-originated signal outside the core Nexus overlay asking Nexus to consider action handling.
- Trigger origin: the named source category or concrete surface that produced an external trigger.
- Trigger event: the occurrence at the origin, before Nexus accepts or interprets it.
- Trigger request: the Nexus-facing request concept created after a trigger event is intentionally handed toward Nexus ownership.
- Nexus entry point: the architecture-level receiving boundary where Nexus may later validate, route, reject, or surface a trigger request.
- Supported origin: an origin category admitted by workstream truth and later validation as eligible for a Nexus entry point.
- Unsupported origin: an origin category excluded by scope, trust posture, missing validation, or lack of user-visible ownership.
- External-owned surface: the UI, hardware, automation tool, companion app, or plugin-hosted surface outside Nexus that emits the trigger event.
- Nexus-owned surface: any Nexus-controlled confirmation, overlay, execution, saved-action, callable-group, failure visibility, or audit surface reached after a trigger request is accepted.

## WS-1 Ownership Boundaries

External systems own:

- the physical, desktop, app, or future plugin-hosted surface where the trigger event begins
- local user configuration inside that external surface
- whether their surface presents a button, shortcut, macro, or equivalent origin affordance
- non-Nexus device/app availability, naming, and native UI state

Nexus owns:

- whether an origin category is supported or unsupported
- the Nexus entry point boundary for accepting, rejecting, or deferring a trigger request
- any later mapping from a trigger request into existing saved-action, callable-group, overlay, confirmation, or result behavior
- user-visible Nexus failure messaging and audit markers once a trigger request crosses into Nexus ownership
- preservation of existing action authority, confirmation, and execution semantics

Not-owned / non-goal surfaces for WS-1:

- external device SDK behavior
- Stream Deck runtime integration
- protocol listeners or transport bindings
- command payload schemas
- installer or settings flows
- trust/safety enforcement logic
- validation matrix design
- new helper or runtime implementation

## WS-1 Entry-Point Architecture Framing

The Nexus entry point is an architecture boundary, not an implementation component in WS-1.

For WS-1, the entry point means: the future Nexus-owned place where a trigger request may be received, classified by origin support, and routed or rejected according to later lifecycle, trust/safety, and validation contracts.

The entry point does not define a listener, transport, payload schema, protocol, plugin API, background service, or UI surface in this seam. Those decisions are intentionally deferred to later seams after WS-2 defines lifecycle/trust-safety boundaries and WS-3 defines validation/admission requirements.

## WS-1 Execution Record

- WS-1 executed as architecture-only documentation on the active FB-039 branch.
- Source map: complete for bounded candidate categories and unsupported origins.
- Ownership vocabulary: complete for later-seam terminology.
- Ownership boundaries: complete at architecture level.
- Entry-point framing: complete as a concept only, with no implementation contract.
- Runtime/product implementation: none.
- Helper creation: none.
- WS-2 and WS-3 remain planned only.
- Continuation decision: WS-2 may be admitted only in a later bounded Workstream pass.

## Scope

- Execute WS-1 only: external trigger source map and ownership vocabulary.
- Keep lifecycle/trust-safety contract work in WS-2 planned-only status.
- Keep validation/admission contract work in WS-3 planned-only status.
- Preserve architecture-level entry-point framing without implementation design, listener design, transport binding, protocol mechanics, payload schema details, settings UI, installer flow, or helper creation.
- Carry the deferred PR #67 connector follow-up as later Workstream governance review only if it remains relevant to validator trust.

## Non-Goals

- No plugin runtime implementation during WS-1.
- No Stream Deck integration implementation during WS-1.
- No protocol handling, installer work, settings surface, taskbar/tray expansion, monitoring HUD work, or release packaging.
- No product/runtime code changes in this Workstream pass.
- No new validation helper creation unless a later Workstream seam proves an actual validation gap and registry rules are satisfied.
- No FB-040 monitoring, thermals, or HUD scope.
- No trust/safety enforcement logic, transport payload schema detail, validation matrix design, user-facing settings/UI, or plugin lifecycle rules in WS-1.

## Validation Contract

- Workstream WS-1 validation:
  - `python dev\orin_branch_governance_validation.py`
  - `git diff --check`
  - `git status --short --branch`
- WS-1 is documentation-only and architecture-first; no runtime helper is required.
- Reuse existing validator families and `Docs/validation_helper_registry.md` guidance first.
- New helpers are blocked until a concrete validation gap exists, the helper purpose is branch-scoped or reusable by design, and registry status/consolidation rules are satisfied.
- Any user-facing behavior introduced later must route through the User Test Summary and user-facing shortcut validation rules if applicable.

## Stop Conditions

- Stop if FB-039 scope expands into plugin/runtime implementation during WS-1.
- Stop if WS-1 starts defining lifecycle/trust-safety enforcement detail, protocol mechanics, payload schemas, validation matrix design, settings UI, installer flow, or helper implementation.
- Stop if WS-2 or WS-3 begins executing in this pass.
- Stop if source map, ownership vocabulary, ownership boundaries, or architecture-only entry-point framing cannot be stated explicitly.
- Stop if any FB-038 release debt or stale release canon reappears.
- Stop if a governance-only branch, direct-main mutation, or between-branch repair path is attempted.
- Stop if new helper creation is proposed before reuse and registry obligations are satisfied.
- Stop if Workstream execution expands beyond WS-1 before WS-1 is recorded and validated.

## Exit Criteria

- FB-039 is represented as the active Workstream in backlog, roadmap, and workstreams index.
- This workstream record contains the required phase authority fields.
- WS-1 external trigger source map, ownership vocabulary, ownership boundaries, and architecture-only entry-point framing are recorded.
- WS-2 and WS-3 remain planned only.
- FB-038 remains released/closed and release debt remains clear.
- Repo state is no longer `No Active Branch`; active branch truth is `feature/fb-039-external-trigger-plugin-integration-architecture`.
- No runtime/product implementation has started.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Workstream`

## Branch Readiness Notes

Branch Readiness durability is complete and WS-1 is now the active Workstream seam. This pass remains architecture-only and does not execute WS-2 or WS-3.
