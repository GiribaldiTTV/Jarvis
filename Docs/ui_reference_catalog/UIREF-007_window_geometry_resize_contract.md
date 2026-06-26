# UIREF-007 Nexus Window Geometry And Resize Contract

Reference ID: `UIREF-007`

Reference Name: `Nexus Window Geometry And Resize Contract`

Reference Class: `Window Geometry / Resize`

Owning Vision Layer: `Project UI Vision -> FAM-002 Desktop Interface -> F2-FF01 Nexus UI Reference System`

Source Evidence: `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/UIREF-001_top_level_window_frame.md`, `Docs/ui_reference_catalog/UIREF-002_window_control_cluster.md`, `Docs/ui_reference_catalog/UIREF-003_control_state_and_selector_grammar.md`, `Docs/ui_reference_catalog/UIREF-004_dialog_status_recovery_and_doorway_surfaces.md`, `Docs/ui_reference_catalog/UIREF-005_design_token_and_shared_rule_baseline.md`, `Docs/ui_reference_catalog/UIREF-006_negative_example_and_enforcement_contract.md`, and the USER-approved Governance Window Geometry / Resize Contract + Per-FAM Dependency Planning intake.

USER Acceptance Receipt: `2026-06-25 USER approved bounded Governance source-truth routing for project-wide window geometry / resize rules and per-FAM dependency planning records, without FAM worktree mutation, runtime UI repair, external-state mutation, GitHub issue mutation, PR creation, merge, release, or cleanup.`

Applicable Surface Classes: `Nexus-owned top-level windows, standalone windows, restorable windows, independently opened windows, movable windows, resizable windows, geometry-persisted windows, dashboard / parent-class windows, compact settings / tool windows, detached child windows, detached child dashboards / child-parent windows, modal or dirty-guard surfaces, and embedded child surfaces when those surfaces own visible geometry, resize, scroll, wrap, or responsive behavior.`

Non-Applicable Surface Classes: `OS file or folder pickers, OS security or permission prompts, provider-auth browser surfaces, installer/update trust surfaces owned by platform convention, external/provider windows Nexus does not visually own, and temporary troubleshooting-only diagnostics when explicitly classified as not final product UI.`

Required Element Groups: `window frame, title/header, content well, resize edges/corners, scrollbar, active content region, footer/action region, window control cluster, modal/dirty-guard layer, child-surface container, empty/wide-state treatment, truncation/wrap/collapse treatment, and geometry recovery route when applicable.`

Required States: `minimum supported size, default size, medium size, wide size, maximum useful size, fullscreen or maximize when applicable, restored, monitor-change or missing-monitor recovery, display-scale/DPI variation, portrait or narrow-monitor posture, content-overflow posture, hover/focus/cursor transition for resize affordances, disabled or Not Applicable control states, and USER-reviewed exception or waiver where applicable.`

Geometry / Resize / Accessibility Expectations: `Windows must remain usable, readable, deterministic, intuitive, immersive, predictable, reliable, and consistent at every supported size. Compact windows should not grow indefinitely into useless empty space unless a purposeful wide-state treatment exists. Dashboard windows may use additional space, but they must use it meaningfully through reflow, columns, richer information density, or bounded scroll rather than leaving tiny UI floating in a large shell. Minimum size is the smallest mature usable size. Default size should fit the active content and role. Maximum useful size should prevent broken or sparse layouts unless fullscreen/maximize has a defined composition. Responsive behavior must use breakpoints, bounded content, reflow, scroll, wrap, truncate, collapse, or added real content; it must not use global browser-zoom style scaling as a substitute for layout design.`

Proof Artifacts: `FAM-007 AI Control Center remains the strongest accepted compact top-level geometry seed where UIREF-001, UIREF-002, and UIREF-007 apply. FAM-006 HUD Dashboard remains comparison and adoption-target evidence for dashboard / parent-class layout. Manage Monitors, Global Settings, Recording Studio, Log Viewer Studio, AI Command Center, tray-opened surfaces, and future installer/update surfaces require their own owning-FAM proof before they can claim adoption.`

Known Limitations: `This record defines source-truth geometry and resize grammar only. It does not implement shared primitives, design tokens, runtime layout code, product-window repairs, FAM adoption, live screenshot/video proof, issue creation, or helper/validator executable enforcement. Consuming branches must still classify each surface and prove actual rendered behavior through their legal phase, accepted references, code-to-visual trace, screenshots/video/contact sheets, and USER review or waiver where needed.`

Adoption Rule: `When a branch creates, changes, accepts, or repairs a Nexus-owned product window or surface with geometry, resize, scroll, breakpoint, fullscreen, or multi-monitor behavior, it must cite UIREF-007 or record a USER-approved exception. The branch must classify the surface, define minimum/default/maximum/fullscreen policy, prove resize mechanics and responsive layout against accepted references, and preserve UIREF-001 through UIREF-006 obligations for frame, controls, states, status/recovery, design baseline, and enforcement boundaries.`

Validator / Helper Guidance: `Future helpers should reject marker-only geometry conformance, missing minimum/default/medium/wide/maximum evidence, missing fullscreen or maximize disposition, missing display-scale or multi-monitor reasoning, missing accepted-reference comparison, hidden bottom-right resize-grip reliance without policy, global zoom used as a layout substitute, current window coordinates committed as repo source truth, and claims that a window is green while owned surfaces remain unproven or issue candidates are not dispositioned.`

Promotion Result: `PROMOTED_AS_SOURCE_TRUTH_GEOMETRY_CONTRACT_WITH_IMPLEMENTATION_DEFERRED`

Final Disposition: `Window geometry and resize contract green for Governance source-truth promotion. Product adoption remains owned by consuming FAM worktrees at their next legal RAR, BP, Workstream, Hardening, Live Validation, UTS, PR Readiness, or Release Readiness gate.`

## Window Classification Model

Allowed window / surface classifications:

- `Compact Settings / Tool Window`
- `Dashboard / Parent-Class Window`
- `Embedded Child Surface`
- `Detached Child Window`
- `Detached Child Dashboard / Child-Parent Window`
- `Modal / Dirty-Guard / Confirmation Surface`
- `Platform-Native Exception`
- `Temporary Diagnostic / Proof Surface`
- `Not Applicable With Reason`

Invalid or insufficient classifications:

- `Child Window` without embedded/detached/parent relationship
- `Responsive By Global Zoom`
- `Fullscreen Supported Without Composition`
- `Resizable` without min/default/max policy
- `Looks Good At Default Size`
- `Window Geometry Green By Marker`
- `Current Coordinates Stored In Repo Docs`

## Geometry Policy Matrix

Consuming branches must include a `Window Geometry / Resize Matrix:` or equivalent proof surface when UIREF-007 applies.

Required fields:

- `Window / Surface Name:`
- `Owning FAM / Worktree:`
- `Window Classification:`
- `Accepted Reference Set:`
- `Minimum Supported Size:`
- `Default Size:`
- `Maximum Useful Size:`
- `Fullscreen / Maximize Policy:`
- `Resize Mechanics:`
- `Cursor Transition / Resize Grip Policy:`
- `Breakpoint / Reflow Policy:`
- `Scroll / Wrap / Truncate / Collapse Policy:`
- `Active Content / Footer Attachment:`
- `DPI / Display Scale Proof:`
- `Multi-Monitor / Portrait Proof:`
- `Geometry Recovery Route:`
- `Code-To-Visual Trace:`
- `Screenshot / Video / Contact-Sheet Evidence:`
- `Disposition:`

## Per-FAM Dependency Planning Records

| Dependency ID | Owning FAM | Surface / Dependency | Expected Carrydown | Deferred / Future-Gated Work | Source-Truth Boundary |
| --- | --- | --- | --- | --- | --- |
| `UIREF-007-D-FAM003-001` | `FAM-003` | Global Settings, resident tray doorway, quick actions, reset-window-position/size access route, and FAM-specific settings entry points. | FAM-003 owns the user-accessible reset route and global settings shell when admitted; consuming FAMs own their feature settings content. | FAM-003 adoption, runtime implementation, and issue creation remain separate USER decisions. | FAM-003 does not own another FAM's feature behavior by inference. |
| `UIREF-007-D-FAM006-001` | `FAM-006` | HUD Dashboard, Manage Monitors, Recording Studio, Log Viewer Studio, monitoring/recording/log surfaces, and dashboard / child-window relationships. | FAM-006 must classify dashboard/parent and studio/log window geometry, compare against accepted references, and prepare issue candidates for out-of-scope owned drift before normal progression. | Runtime UI repair, Live Validation proof, UTS, and issue mutation remain separate USER decisions. | Governance records the contract only; FAM-006 owns branch-local adoption and proof. |
| `UIREF-007-D-FAM007-001` | `FAM-007` | AI Control Center, AI Status / Command Center, provider/trust/status windows, and public/private AI surfaces when visible to USER. | FAM-007 must preserve the AI Control Center as accepted compact geometry seed where applicable and prove any new AI surface against UIREF-007 and privacy/trust boundaries. | Provider/model/private/cache/memory behavior and runtime AI execution remain separate USER decisions. | UI geometry proof does not authorize provider/model or private edition work. |
| `UIREF-007-D-FAM008-001` | `FAM-008` | Installer, update, patch/restart, shortcut, taskbar, Task Manager, and setup education surfaces. | FAM-008 may explain geometry reset or tray visibility education during setup/installer work when admitted; it owns packaging/update identity and platform trust surface proof. | Installer/update/runtime setup implementation remains separate USER decisions. | FAM-008 does not own runtime reset action unless source truth later grants it. |

## Umbrella Issue Coordination Model

A GitHub issue may be used as a coordination artifact for geometry or resize inconsistencies across multiple FAM-owned windows, but it is not automatic scope approval. The clean pattern is one umbrella issue with one checklist row per owned surface, one branch/PR per owning worktree when work is independent, `Refs` or `Part of` wording for partial PRs, and `Fixes` only on the final closing PR after all rows are merged, validated, and accepted. Same-file/source-owner overlap, active worktree limits, issue mutation, PR creation, and merge remain USER-gated by current source truth.
