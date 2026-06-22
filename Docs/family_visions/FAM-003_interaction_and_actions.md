# FAM-003 Interaction And Actions Vision

## Purpose

This family vision records durable product direction for shared actions, command/action UX, callable groups, taskbar/tray quick-task interaction, saved action authoring, and user-visible confirmation/interaction contracts.

## Vision Summary

Interaction and Actions should feel predictable, explicit, and easy to trust. Advanced grouping and action behavior should grow from proven exact-match and user-controlled primitives instead of hidden inference.

## Accepted Direction

- Keep pre-Beta callable groups explicit, exact-match, and member-driven.
- Preserve confirmation and boundary clarity for user-triggered actions.
- Treat richer grouping, discovery, recommendation, or query behavior as later post-proof expansion.
- Keep action authoring, built-in action expansion, and tray/quick-task behavior tied to clear validation proof.
- Treat the Nexus resident tray icon as a doorway and status beacon, not the full command center.
- Keep the resident tray menu compact, with core Nexus actions, safety/status doorways, state-dependent optional feature doorways, and a small USER-configurable Quick Access section rather than a command wall.
- Treat immutable or unremovable resident routes as stable route identity/order/behavior when a route is admitted and enabled, not as forced visibility after USER opt-out.
- Show optional feature doorways only when enabled/admitted, or show them disabled with an owner-bounded reason when the USER wants the feature but it is temporarily blocked, errored, or not ready. Hide optional feature rows from active tray/menu UI when the USER disables them during setup or Global Settings, when the feature is not installed, when it is unsupported, or when the state is unknown enough that the tray/menu would overclaim.
- Keep Global Settings and Exit Nexus as always-visible core actions unless later source truth records an exception. AI Status / Command Center may remain visible as the resident safety/status doorway while FAM-007 and AI Runtime And Trust own detailed trust status. Privacy Lockdown stays future-gated outside the top-level resident tray menu until FAM-007 admits a real immediate lockdown action; FAM-003 must not claim FAM-007-owned runtime/provider/privacy truth.
- Own the minimal Resident Access / Quick Access settings interaction needed by the resident doorway, including the Global Settings entry/shell foundation for quick-slot configuration, while preserving other settings categories as owner-bounded placeholders, links, or future-gated surfaces.
- Route deep task/group authoring, NCP management, Recording Studio, Log Viewer Studio, AI controls, full app-wide settings, and owner-specific settings internals into their owning full surfaces rather than duplicating every command in the tray menu or resident settings foundation.
- Treat reset-window-position/size actions for standalone Nexus-owned product windows as a resident access / Global Settings / quick-action dependency route when the reset must be user-accessible across families.
- Prefer one primary Nexus tray icon by default; a second AI privacy/status icon is future-gated and requires USER-approved evidence that one icon plus visible status surfaces cannot communicate privacy state safely.
- AI-native routines, ambient assistance, daily continuity, interruption awareness, and assistance intensity are experience-layer concepts by default; they do not become new backlog families or autonomous runtime behavior without the Backlog Taxonomy And Source-Truth Placement Gate and USER-approved Branch Readiness.
- Routine/action UX must preserve inspectable resolution, explicit confirmation, revocation/back-out paths, and plain-language trust posture before sensitive actions run.

## Implementation Boundaries

- This vision does not admit dynamic natural-language grouping, autonomous scheduling, or broad recommendation behavior.
- This vision does not admit AI routine execution, background monitoring, memory, provider calls, Windows Health repair, or sensitive automation by itself.
- This vision does not admit Windows system-tray pinning control, OS-owned Sound/Network/Mic cluster integration, unhide/unpin prevention, or any claim that Nexus can force third-party tray icon permanence.
- This vision does not admit full app-wide Global Settings implementation, other-FAM settings internals, or a settings takeover by itself. FAM-003 settings work is limited to the Resident Access / Quick Access foundation unless Branch Readiness and USER approval admit a broader owner-bounded dependency.
- This vision does not admit runtime implementation of window geometry reset actions by itself; consuming FAMs must first classify their windows and dependency need through Branch Readiness and Branch Planning.
- Active branches must use Branch Readiness to define accepted user workflow, safety boundaries, and validation proof.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- Resident access FFV: `Docs/family_feature_visions/F3-FF01.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Backlog registry: `Docs/feature_backlog.md`
- Durable family dossier: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
