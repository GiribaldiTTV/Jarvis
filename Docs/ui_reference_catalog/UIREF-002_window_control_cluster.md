# UIREF-002 Nexus Window Control Cluster Reference

Reference ID: `UIREF-002`
Reference Name: `Nexus Compact Window Control Cluster`
Reference Class: `Window Control Cluster`
Owning Vision Layer: `Project UI Vision -> FAM-002 Desktop Interface -> F2-FF01 Nexus UI Reference System`

Source Evidence: Consolidated Package A-E proof-collection and runtime-proof receipts in `Docs/branch_records/feature_release_readiness_source_truth_intake.md`, PR #269 AI Control Center control-cluster evidence, FAM-002 Top-Level Window Control Grammar, and the Package A-E USER review packets recorded in this branch's source-truth receipts.

USER Acceptance Receipt: `2026-06-17 USER approved bounded completion until all Package A-E lanes are green, with the FAM-007 AI Control Center compact control pill accepted as the strongest available standard seed while preserving known proof limitations.`

Applicable Surface Classes: `Nexus-owned top-level, standalone, restorable, independently opened, movable, resizable, or geometry-persisted product windows where close, minimize, maximize, restore, drag, or resize controls are meaningful.`

Non-Applicable Surface Classes: `modal confirmations, child panels, footer/content actions, one-shot proof/dev windows, OS/platform-native surfaces, and product surfaces with a recorded USER-approved control exception.`

Required Element Groups: `close control, minimize control when applicable, maximize/restore control when applicable, disabled/hidden controls when not applicable, hitbox, accessible name, tooltip or equivalent discoverability where needed, hover/focus/pressed states, and content-action separation.`

Required States: `default, hover, focus, pressed/clicked, disabled or hidden when a control is not applicable, blocked/unavailable with explanation when applicable, and platform-native exception when applicable.`

Geometry / Resize / Accessibility Expectations: `Controls must remain compact, clearly window-level rather than content-level, visually secondary except for close when intentional, keyboard/focus reachable where applicable, and large enough for reliable pointer interaction.`

Proof Artifacts: `FAM-007 close-hover and default control screenshots provide accepted proof seed. The recorded duplicate minimize-hover screenshot remains a known limitation rather than independent minimize-hover proof.`

Known Limitations: `Independent minimize-hover, maximize/restore, disabled, focus, pressed, and hitbox proof is incomplete in current evidence. This limitation is accepted for reference promotion with the rule that consuming branches must prove any state they claim or request USER waiver.`

Adoption Rule: `Top-level Nexus product windows should use UIREF-002 for window-level controls or record why a large labeled CLOSE/back/cancel action is a modal, child, footer, content, proof/dev, platform-native, or USER-approved exception.`

Validator / Helper Guidance: `Future helpers should flag default OS chrome, large header CLOSE on a top-level window without exception, missing minimize/maximize applicability, missing accessibility label proof, and screenshots that claim hover state while hashing identically to default state.`

Promotion Result: `PROMOTED_WITH_KNOWN_LIMITATIONS`

Final Disposition: `Package A window-control cluster reference green for Governance source-truth promotion. Consuming branches still own feature-specific implementation and state proof.`
