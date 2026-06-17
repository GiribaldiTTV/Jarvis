# UIREF-004 Nexus Dialog, Status, Recovery, And Doorway Surface Reference

Reference ID: `UIREF-004`
Reference Name: `Nexus Dialog, Status, Recovery, And Doorway Surface Grammar`
Reference Class: `Status / Failure / Recovery Panel`
Owning Vision Layer: `Project UI Vision -> FAM-001 recovery direction -> FAM-002 Desktop Interface -> F2-FF01 Nexus UI Reference System -> F3-FF01 resident access dependency`

Source Evidence: Consolidated Package A-E proof-collection and runtime-proof receipts in `Docs/branch_records/feature_release_readiness_source_truth_intake.md`, FAM-001/FAM-002/FAM-003 source-truth carrydown, accepted FAM-003 resident-access context, accepted FAM-006 doorway/status comparison evidence, and the Package A-E USER review packets recorded in this branch's source-truth receipts.

USER Acceptance Receipt: `2026-06-17 USER approved bounded completion until all Package A-E lanes are green, with FAM-003/FAM-006 evidence accepted as planning/runtime context and missing final tray/settings/status proof preserved as consuming-FAM proof obligations.`

Applicable Surface Classes: `Nexus-owned child windows, modals, confirmations, status panels, degraded/blocked/unavailable states, failure/recovery panels, support/manual-reporting panels, tray-opened doorway surfaces, settings entry surfaces, and proof-visible recovery surfaces.`

Non-Applicable Surface Classes: `OS security prompts, platform-native file/folder pickers, provider-auth surfaces, installer/update trust prompts, and external surfaces Nexus does not visually own.`

Required Element Groups: `plain-language status, cause where safe, available action, disabled/degraded explanation, recovery action, support/export/manual-report route where applicable, close/cancel/back behavior, and doorway routing to full product surfaces instead of deep tray command walls.`

Required States: `normal, unavailable-prerequisite, disabled, degraded, blocked, recoverable failure, fatal failure, retry, cancel/close, support/manual-report, and platform-native exception where applicable.`

Geometry / Resize / Accessibility Expectations: `Status and recovery surfaces must be readable under stress, avoid debug-wall presentation, keep actions predictable, and preserve Nexus-native presentation unless a platform exception is recorded.`

Proof Artifacts: `FAM-003 desktop-entrypoint recovery logs prove recovery-path context but not final visual tray/settings proof. FAM-006 returned UTS/failure context and tray-menu screenshots provide comparison evidence for doorway/status behavior.`

Known Limitations: `FAM-003 visual tray/settings proof and full modal/status/recovery visual sequences are incomplete. This reference promotes the grammar and proof obligations, not any current runtime implementation as complete.`

Adoption Rule: `Branches creating visible status, failure, recovery, modal, dialog, tray, or settings doorway surfaces must cite UIREF-004, map the runtime truth behind the visible state, and prove the USER-visible result or route unphotographable claims to USER validation/waiver.`

Validator / Helper Guidance: `Future helpers should flag recovery UI with no real recovery route, backend logs used as USER visual proof, tray menus that become deep command walls, missing failure/degraded states, missing status-to-runtime mapping, and unclassified platform-native exception surfaces.`

Promotion Result: `PROMOTED_WITH_KNOWN_LIMITATIONS`

Final Disposition: `Package C dialog/status/recovery/doorway reference green for Governance source-truth promotion. Visual and runtime adoption remains owned by FAM-001/FAM-003/FAM-006/FAM-007/FAM-008 as applicable.`
