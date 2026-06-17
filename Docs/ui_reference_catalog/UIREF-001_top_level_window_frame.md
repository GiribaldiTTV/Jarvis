# UIREF-001 Nexus Top-Level Window Frame Reference

Reference ID: `UIREF-001`
Reference Name: `Nexus Top-Level Window Frame`
Reference Class: `Top-Level Window`
Owning Vision Layer: `Project UI Vision -> FAM-002 Desktop Interface -> F2-FF01 Nexus UI Reference System`

Source Evidence: Consolidated Package A-E proof-collection and runtime-proof receipts in `Docs/branch_records/feature_release_readiness_source_truth_intake.md`, PR #269 AI Control Center H4 resize/visual evidence, accepted FAM-006 HUD/Dashboard comparison evidence, and the Package A-E USER review packets recorded in this branch's source-truth receipts.

USER Acceptance Receipt: `2026-06-17 USER approved bounded completion until all Package A-E lanes are green, after reviewing that FAM-007 AI Control Center is the strongest available top-level-window seed and that HUD/FAM-006 is comparison/adoption evidence.`

Applicable Surface Classes: `Nexus-owned top-level, standalone, restorable, independently opened, movable, resizable, or geometry-persisted product windows.`

Non-Applicable Surface Classes: `OS file/folder pickers, OS security/permission prompts, provider-auth browser surfaces, installer/update trust surfaces, temporary troubleshooting-only diagnostics, and platform-native exceptions with recorded reason.`

Required Element Groups: `custom Nexus frame or chrome, title/header treatment, content frame, resize affordance when applicable, geometry persistence or reset route when applicable, window-control cluster when applicable, product-state surface, and proof-visible surface framing.`

Required States: `default/focused, unfocused where relevant, resized, restored, blocked/unavailable where relevant, platform-exception where relevant, and USER-reviewed visual acceptance or waiver.`

Geometry / Resize / Accessibility Expectations: `Top-level product windows must avoid default Windows title bars, preserve Nexus-native chrome, remain readable at supported sizes, expose a safe position/size recovery path when geometry is persisted, and provide accessible labels for window controls.`

Proof Artifacts: `FAM-007 AI Control Center focused/full-desktop screenshots and resize manifest provide the strongest accepted visual seed; FAM-006 dashboard/HUD screenshots and video provide comparison and future adoption-target evidence.`

Known Limitations: `This reference promotes the top-level-frame grammar, not every current FAM-006/FAM-007 implementation detail. Consuming branches must still prove their own window class, geometry/reset behavior, accessibility, and any platform-native exception through their own BP2/BP3, Hardening, Live Validation, or USER review path.`

Adoption Rule: `When a branch creates or repairs a Nexus-owned top-level product window, it must cite UIREF-001 or record a USER-approved exception, then prove the resulting surface against Project UI Vision, FAM-002 grammar, and its own feature-specific vision.`

Validator / Helper Guidance: `Future helpers should reject final top-level product windows that expose default Windows title bars, unclassified platform chrome, missing reset route for persisted geometry, or no comparison against UIREF-001 when the reference applies.`

Promotion Result: `PROMOTED_WITH_KNOWN_LIMITATIONS`

Final Disposition: `Package A top-level window reference green for Governance source-truth promotion. Product adoption remains owned by consuming FAM worktrees at their next legal gate.`
