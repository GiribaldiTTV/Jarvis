# FAM-002 Desktop Interface Vision

## Purpose

This family vision records durable product direction for the Nexus desktop shell, visual language, operator UI, settings presentation, user-facing desktop interaction surfaces, and coherent UI/UX implementation packages.

FAM-002 is the shared Desktop Interface / UI presentation authority for Nexus. It is normally consumed by other FAM branches when those branches implement their own user-facing surfaces, rather than opened as a standalone worktree by default.

## Vision Summary

The Desktop Interface should feel intentional, native to Nexus, and visually coherent across windows, cards, controls, settings, and proof surfaces. It should not collapse into generic utility UI or proof-heavy engineering panels.

## Accepted Direction

- Keep user-facing surfaces polished enough for USER review before Live Validation handoff.
- Use branch plans to settle concrete layout, control, proof, and acceptance details before implementation.
- Preserve visual identity, control hierarchy, and reviewability as product requirements, not cosmetic afterthoughts.
- Keep dev/proof scaffolding out of production UI unless explicitly admitted.
- Resident status panels, tray-opened panels, Global Settings, AI Status / Command Center, and quick-access configuration surfaces should follow the Nexus visual hierarchy instead of becoming generic utility popups.
- Tray-accessible surfaces should keep the tray as a doorway: compact entry in the tray, full explanation and configuration in polished Nexus windows.
- Visible diagnostics, failure, degraded-state, recovery, support-bundle, manual-reporting, and repair-option panels consume FAM-002 presentation standards when they are shown to the USER.
- Consuming FAM branches inherit FAM-002 presentation standards when their accepted Family Vision, FFV, branch plan, and proof path require UI work for their own feature behavior.
- FAM-003 owns resident tray doorway behavior while consuming FAM-002 presentation standards; FAM-006 owns Recording Studio / Log Viewer behavior and related UI; FAM-007 owns AI Status / Command Center behavior and related UI; FAM-008 owns installer, setup, shortcut, update, patch/restart, and tray-visibility education behavior and related UI.

## NDAI Window Chrome And Immersion Contract

FAM-002 owns the reusable presentation law for Nexus-owned windows and panels. Final product surfaces should not expose default Windows title bars, unstyled native utility chrome, generic button rows, or platform-looking popup shells when the surface is meant to be a Nexus product window.

The expected presentation is Nexus-native: custom product framing or chrome, coherent title/header treatment, matching close/minimize/back/settings affordances where applicable, consistent card/button/list/scrollbar language, readable spacing and density, and deliberate disabled/degraded/recovery states. A consuming FAM may specialize the layout for its feature, but it must inherit this presentation grammar or record a USER-approved exception.

Platform exceptions must be explicit. OS file pickers, OS security prompts, provider-auth surfaces, installer/update flows that require platform trust affordances, and temporary troubleshooting-only diagnostics may use platform chrome only when the branch classifies the exception, explains why Nexus-native chrome is not appropriate, and includes the exception in BP2/BP3 proof and Live Validation visual adjudication.

## Top-Level Window Control Grammar Standard

FAM-002 owns the reusable top-level window-control grammar for Nexus-owned product windows. A Nexus-owned top-level, standalone, restorable, independently opened, movable, resizable, or geometry-persisted product window must distinguish window-level controls from content actions. Window-level close, minimize, maximize, restore, drag, and resize behavior must use a compact Nexus-native control cluster or recorded equivalent window-control grammar when those actions are applicable to the window.

A large labeled header `CLOSE` pill is clear and may remain valid for modal dialogs, child windows, footer actions, content-level actions, confirmation flows, temporary proof/dev surfaces, platform-native exceptions, or USER-approved exceptions. It is not the default top-level window-control grammar for standalone Nexus product windows because it can read as a content action, compete with footer buttons, and blur the boundary between closing a window and completing or cancelling work. If a branch keeps a large header `CLOSE` on a top-level product window, it must record why the exception is intentional and prove it does not conflict with footer/content actions.

Top-level control clusters must remain Nexus-native rather than default Windows chrome. Expected behavior includes compact placement, readable icons or symbols, accessible names, hover tooltips, generous hitboxes, keyboard/focus treatment, default/hover/pressed/focus/disabled states, visually secondary minimize/maximize/restore controls, and a close control that is neutral by default unless danger context or hover treatment is intentionally admitted. Consuming FAM branches own their feature-window behavior and proof. FAM-003 owns only user-accessible reset/recovery routes when a global or doorway-level action is admitted; it does not own normal close/minimize/maximize/restore behavior by inference.

## Standalone Window Geometry Recovery Standard

FAM-002 owns the reusable presentation and geometry standard for Nexus-owned product windows. Any Nexus-owned standalone, top-level, restorable, independently opened, movable, resizable, or geometry-persisted product window must define safe default position/size behavior and a USER-accessible reset path so the USER can recover from offscreen placement, missing-monitor movement, corrupted saved geometry, too-small/too-large windows, or layout changes.

The reset route must preserve Nexus presentation grammar: clear language, predictable placement, visible recovery feedback, and no debug-looking utility popup unless a platform/native or troubleshooting exception is recorded. Consuming FAM branches own their feature window behavior and proof. FAM-003 owns the resident access / quick-actions / settings route when the reset action is a global or user-accessible Nexus command. Child panels, anchored panels, OS dialogs, temporary dev/proof tools, or non-restorable surfaces may be Not Applicable only when the branch records the reason and proof path.

## Window Geometry And Resize Contract Standard

FAM-002 also owns the reusable presentation law for window geometry, resize, responsive layout, and size-state composition. `Docs/ui_reference_catalog/UIREF-007_window_geometry_resize_contract.md` is the promoted source-truth contract for minimum/default/maximum/fullscreen policy, breakpoint/reflow behavior, DPI and display-scale posture, multi-monitor and portrait/narrow-monitor proof, content overflow handling, sparse wide-state prevention, and per-FAM dependency carrydown.

Same-class Nexus-owned windows should feel deterministic, intuitive, immersive, predictable, reliable, and consistent across size states. A compact tool window may stay compact or define a purposeful wide-state treatment. A dashboard / parent-class window may grow, but the extra room must be meaningful through composition, reflow, richer density, or bounded scroll. A detached child window or detached child dashboard must say whether it behaves like its parent, owns independent geometry, or needs a USER-approved exception.

Consuming FAM branches own their feature-specific layout, backend behavior, proof, and USER packet. They must classify affected windows, cite UIREF-007 when geometry/resize applies, compare against the accepted reference set, and record any issue candidates or exceptions before claiming product readiness. FAM-002 supplies the visual/geometry grammar; it does not directly mutate FAM-003/FAM-006/FAM-007/FAM-008 runtime UI by inference.

## Reusable Component Grammar

FAM-002 supplies reusable presentation grammar for:

- product window chrome, frame shape, title/header treatment, close/minimize/back/settings affordances, and resize/drag behavior
- panels, studios, dashboards, command centers, settings windows, status panels, diagnostics panels, and tray-opened product surfaces
- cards, rows, dividers, page breaks, chips, badges, status fields, empty/error/degraded/blocked states, warning banners, confirmation dialogs, and recovery panels
- primary, secondary, danger, disabled, hover, focus, selected, dirty, loading, and future-gated control states
- scrollbars, dropdowns, list rows, input fields, folder/file pickers when Nexus owns the presentation, and compact/expanded layout density
- USER-facing proof readability, so validation or diagnostics surfaces remain understandable product surfaces instead of debug walls

Consuming FAM branches may specialize this grammar for their own feature surfaces, but they must name the inherited FAM-002 grammar, classify any platform-native exception, and prove visible inheritance before USER handoff. A branch that introduces a new button family, new window frame, new dialog shell, unique glow/color family, or custom layout density must record whether it is inherited, a USER-accepted new grammar, or a repair/blocker.

## Component Anatomy And Element-Group Acceptance

FAM-002 treats reusable UI components as visible element groups with anatomy, state, and proof expectations. A component is not accepted merely because a helper marker exists or a screenshot was captured.

For shared UI components such as close/minimize/back/settings affordances, primary/secondary/danger buttons, dropdowns, cards, rows, scrollbars, confirmation dialogs, dirty guards, status chips, and window chrome, consuming FAM branches should identify the component anatomy that matters to the USER experience:

- visible label/icon and purpose
- placement and relationship to surrounding controls
- size, spacing, radius, border, shadow, glow, and density
- typography, color, contrast, and disabled/degraded treatment
- default, hover, focus, pressed, selected, dirty, loading, disabled, error, empty, and danger states when applicable
- input behavior for mouse, keyboard, focus, scroll, resize, close, save, discard, cancel, and delete paths when applicable
- inherited reference surface, accepted grammar, or USER-approved exception

Element-group acceptance must be deterministic enough that a future branch can compare a new component to the inherited Nexus grammar. Vague verdicts such as `looks good`, `NDAI-ish`, `matches generally`, or `seems fine` are not enough. Final visual acceptance requires mapped evidence, reference or exception, inspected state coverage, and a PASS / REPAIR / STOP / WAIVED_WITH_REASON / USER Review Required disposition.

## Consumption Model

- Default Rule: FAM-002 is consumed-by-default by feature-owning FAM branches.
- Consuming-FAM Implementation Rule: a consuming FAM may implement FAM-002-aligned UI when the UI is necessary to complete that FAM's accepted feature behavior, Family Feature Vision, branch plan, and validation proof.
- Branch Exception Rule: a dedicated FAM-002 branch or worktree is allowed only when USER admits a concrete Desktop Interface feature category that no consuming FAM owns.
- Ownership Split: FAM-002 supplies presentation law; the consuming FAM owns the feature behavior, feature-specific UI implementation, runtime proof, and fold-down receipt.
- Non-Capture Rule: consuming FAMs must not use FAM-002 as a reason to redesign unrelated app-wide UI, absorb another FAM's feature behavior, or bypass cross-FAM dependency classification.
- Failure/Recovery UI Rule: FAM-002 supplies visual hierarchy, control grammar, disabled/degraded affordance, and panel presentation law for visible diagnostics or recovery UI; FAM-001 owns fatal launcher/runtime recovery meaning, and the consuming FAM owns feature-specific failure behavior.

## Implementation Boundaries

- This vision does not admit a UI overhaul by itself.
- This vision does not create a default FAM-002 worktree, selected-next branch, or generic UI-polish carrier.
- This vision does not admit tray implementation, shortcut mutation, installer behavior, AI Command Center implementation, or privacy-state runtime behavior by itself.
- Active Desktop Interface branches must carry accepted Branch Vision Snapshot, UFD disposition, and proof expectations before Workstream implementation.
- Durable implementation history belongs in the relevant workstream or structured branch receipt.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- UI reference-system FFV: `Docs/family_feature_visions/F2-FF01.md`
- Promoted UI reference catalog: `Docs/ui_reference_catalog/`
- Resident access FFV: `Docs/family_feature_visions/F3-FF01.md`
- Backlog registry: `Docs/feature_backlog.md`
- Roadmap posture: `Docs/prebeta_roadmap.md`
- Durable planning owner: `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md`
