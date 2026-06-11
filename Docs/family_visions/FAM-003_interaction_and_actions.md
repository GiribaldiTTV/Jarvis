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
- Keep the resident tray menu compact, with immutable core entries for HUD Dashboard, Global Settings, AI Status / Command Center, Privacy Lockdown, and Exit Nexus, plus a small USER-configurable Quick Access section.
- Own the minimal Resident Access / Quick Access settings interaction needed by the resident doorway, including a real Global Settings entry and shell/window foundation for quick-slot configuration, while preserving other settings categories as owner-bounded placeholders, route links, disabled/future-gated sections, or owner-approved existing controls.
- Ensure any FAM-003-owned Global Settings shell/window follows the Nexus Project UI Vision in `Docs/nexus_vision.md` and FAM-002 UI/UX authority for visual hierarchy, layout, polish, accessibility, and Nexus identity.
- Prefer a scalable left-navigation settings layout for the FAM-003 minimal settings shell/window; a tabbed settings UI should not become the primary model unless later source truth and USER approval override that preference.
- Route deep task/group authoring, NCP management, Recording Studio, Log Viewer Studio, AI controls, full app-wide settings, and owner-specific settings internals into their owning full surfaces rather than duplicating every command in the tray menu or resident settings foundation.
- Prefer one primary Nexus tray icon by default; a second AI privacy/status icon is future-gated and requires USER-approved evidence that one icon plus visible status surfaces cannot communicate privacy state safely.
- AI-native routines, ambient assistance, daily continuity, interruption awareness, and assistance intensity are experience-layer concepts by default; they do not become new backlog families or autonomous runtime behavior without the Backlog Taxonomy And Source-Truth Placement Gate and USER-approved Branch Readiness.
- Routine/action UX must preserve inspectable resolution, explicit confirmation, revocation/back-out paths, and plain-language trust posture before sensitive actions run.

## Implementation Boundaries

- This vision does not admit dynamic natural-language grouping, autonomous scheduling, or broad recommendation behavior.
- This vision does not admit AI routine execution, background monitoring, memory, provider calls, Windows Health repair, or sensitive automation by itself.
- This vision does not admit Windows system-tray pinning control, OS-owned Sound/Network/Mic cluster integration, unhide/unpin prevention, or any claim that Nexus can force third-party tray icon permanence.
- This vision does not admit full app-wide Global Settings implementation, other-FAM settings internals, tab-primary settings redesign, or a settings takeover by itself. FAM-003 settings work is limited to the Resident Access / Quick Access foundation unless Branch Readiness and USER approval admit a broader owner-bounded dependency.
- Active branches must use Branch Readiness to define accepted user workflow, safety boundaries, and validation proof.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- Resident access FFV: `Docs/family_feature_visions/F3-FF01.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Backlog registry: `Docs/feature_backlog.md`
- Durable family dossier: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
