# UIREF-005 Nexus Design Token And Shared Rule Baseline

Reference ID: `UIREF-005`
Reference Name: `Nexus Design Token And Shared Rule Baseline`
Reference Class: `Proof / Review Surface`
Owning Vision Layer: `Project UI Vision -> FAM-002 Desktop Interface -> F2-FF01 Nexus UI Reference System`

Source Evidence: `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, selected FAM-006/FAM-007 comparison evidence, and the consolidated Package A-E runtime proof packet.

USER Acceptance Receipt: `2026-06-17 USER approved bounded completion until all Package A-E lanes are green, accepting a source-truth design-rule baseline while preserving code-level token/shared-primitive implementation as a later implementation carrier.`

Applicable Surface Classes: `Nexus-owned product windows, cards, rows, controls, status surfaces, proof surfaces, dialogs, command centers, studios, dashboards, settings surfaces, and resident doorway surfaces.`

Non-Applicable Surface Classes: `External/provider/OS surfaces, platform-native exceptions, and temporary developer-only diagnostics not presented as final Nexus UI.`

Required Element Groups: `color roles, typography roles, spacing and density, radius, border, glow/shadow, disabled/degraded states, scrollbar treatment, window-frame treatment, action hierarchy, and proof-surface readability.`

Required States: `default, hover, focus, pressed, selected, disabled, loading, degraded, blocked, error, empty, and platform-native exception where applicable.`

Geometry / Resize / Accessibility Expectations: `Design rules must preserve readability, predictable interaction, stable hierarchy, and enough contrast for long-session use. Future code-level tokens must prove source-to-visual trace instead of relying on prose alone.`

Proof Artifacts: `Project UI Vision and FAM-002 grammar provide durable product law; FAM-006/FAM-007 evidence provides comparison input. No code-level shared primitive is promoted by this record.`

Known Limitations: `Accepted token values, shared CSS/component implementations, code-to-visual trace, contrast audits, migration/rollback plans, and product-worktree adoption are not implemented in this Governance branch. Those remain future implementation work, not current PR blockers after this disposition.`

Adoption Rule: `Until code-level shared primitives are implemented, branches must treat UIREF-005 as a source-truth design-rule baseline and still prove their own surfaces visually. A future implementation carrier may turn this baseline into concrete tokens/components after USER approval.`

Bounded Carry-In Note: `FAM-006 may carry nexus_visual/nexus_window_primitives.css as a branch-local shared primitive candidate only for the active returned-UTS Recording Studio / Log Viewer Studio repair approved by USER on 2026-06-22. This is a consuming-branch repair path, not global UIREF-005 primitive promotion. The branch must record consumption, proof, limitations, and any future promotion need before claiming reusable program-wide authority.`

Validator / Helper Guidance: `Future helpers should flag branches that claim design-token implementation without a code carrier, claim shared primitives exist by inference, or skip visual proof because a design-rule baseline exists.`

Promotion Result: `PROMOTED_AS_SOURCE_TRUTH_BASELINE_WITH_IMPLEMENTATION_DEFERRED`

Final Disposition: `Package D green for Governance source-truth baseline. Runtime/code implementation of tokens and shared primitives remains future-gated outside this branch.`
