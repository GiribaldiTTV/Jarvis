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
- Resident access FFV: `Docs/family_feature_visions/F3-FF01.md`
- Backlog registry: `Docs/feature_backlog.md`
- Roadmap posture: `Docs/prebeta_roadmap.md`
- Durable planning owner: `Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md`
