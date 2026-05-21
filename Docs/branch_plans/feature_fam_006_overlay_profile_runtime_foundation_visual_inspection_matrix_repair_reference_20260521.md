# FAM-006 Visual Inspection Matrix Repair Reference - 2026-05-21

## Returned USER Result

Classification: `REPAIR`

USER found that HUD button glow was not uniform and that Hardening / Live Validation failed to catch visual elements that did not meet the feature vision. The returned scope explicitly includes button glow, page breaks, background glow, background graphics, bleed-through, clipping, scaling, and individual inspection of every HUD visual element.

## Repair Admission

This reference is branch-local evidence for `feature/fam-006-overlay-profile-runtime-foundation` in `C:\Nexus Worktrees\FAM-006`.

The repair is bounded to FAM-006 HUD runtime, proof helpers, validators, and source truth. It does not admit Recording Profile runtime, tray recording controls, export/share, provider/model work, broad NDAI theme/skin work, FAM-007 work, Governance branch mutation, PR creation, merge, release, issue mutation, or artifact handling.

## Repair Contract

- HUD-wide clickable controls must share a visible Nexus hover / active / focus glow contract.
- Danger actions retain red illumination; safe Cancel actions retain safe-cancel illumination; disabled controls remain visibly disabled.
- Validation must prove the visual state matrix rather than infer visual acceptability from helper PASS, marker PASS, screenshot existence, or DOM presence.
- H1 and LV1 must inspect the whole current HUD feature, including legacy elements and adjacent proof-bearing surfaces, when a visual failure is returned.

## Required Proof Markers

- `runMonitoringHudVisualInspectionMatrixProof`
- `hudWideVisualInspectionMatrix`
- `buttonGlowUniformity`
- `visualInspectionScopeCovered`
- `pageBreakVisualInspection`
- `backgroundBleedClippingInspection`
- `scope=buttons-dropdowns-rows-chips-fields-page-breaks-backgrounds-bleed-clipping-scaling`

## Workstream Repair Result

Classification: `GREEN`

Active-client live self-QA passed at `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_160228_031\monitoring_hud_live_client_interaction_manifest.json`.

The visual inspection matrix reported `hudWideVisualInspectionMatrix=true`, `buttonGlowUniformity=true`, `targetCount=36`, `surfaceCount=3`, and no matrix failures.

## Next Legal Phase

After validation-green Workstream repair, the next legal phase is Hardening H1 for the HUD-wide button glow uniformity and visual inspection matrix repair.
