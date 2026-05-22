# Temporary User Issue Form - FAM-006 Overlay Profile Runtime Foundation Returned UTS

Reference Date: `2026-05-21`
Branch: `feature/fam-006-overlay-profile-runtime-foundation`
Worktree: `C:\Nexus Worktrees\FAM-006`
Recorded At Head: `b33d38de0aa5d631afa2ed63a3f83274262c3b35`
Current Main Basis: `b3cb321cc525028354e6dbd290c774c3f09ecad4`
Desktop Shortcut: `C:\Users\anden\OneDrive\Desktop\FAM-006 UTS Issue Form.lnk`

## Governance Classification

Returned User Test Summary Result: `REPAIR`

This USER response rejects the latest refreshed LV1 handoff. It is not a PASS or waiver. PR Readiness remains blocked until every issue below is admitted into repair planning, the USER validates the proposed repair intent, implementation is separately approved, H1 and refreshed LV1 prove the repairs with reviewable visual evidence, and returned USER UTS results are PASS or explicitly waived with reason.

This file is a temporary tracked issue form. It exists to prevent returned UTS feedback from being lost between digest, repair setup, implementation, H1, LV1, and PR Readiness. It must be deleted only after PR Readiness Stage 1 is green and every still-relevant detail has been rolled into the appropriate branch record, branch plan, validators, UTS checklist, backlog/roadmap pointer, or future-scope record.

Original Digest Authorization Boundary: `This record began as a digest and planning form only. Runtime implementation was later separately USER-approved for the bounded returned-UTS Workstream; PR creation, merge, release, issue mutation, artifact handling, sibling-worktree mutation, and future package work remain outside this form.`

## Repair Setup Approval

Setup Approval Status: `APPROVED - USER approved Live Validation returned-UTS issue repair setup after commit f7fc6e8af1599f89c4f3cbdd794fd94be67f3027.`

Setup Scope: `Refine issue-by-issue planning, define bounded repair disposition, define validation/proof matrix, update directly supporting source truth, run validation, and commit/push if green.`

Runtime Implementation Authorization: `NOT AUTHORIZED IN THIS SETUP PASS - no UI/CSS/JS/Python runtime repairs, PR Readiness, PR creation, merge, release, issue mutation, artifact handling, sibling-worktree changes, or future package work may occur without separate approval.`

Setup Result: `ADMITTED - all returned UTS issues are accepted as planning inputs. Items are classified below as current-branch repair candidates, proof/validator governance repairs, conditional current-branch repairs, or future-gated planning items.`

## Bounded Workstream Implementation Result

Implementation Result: `GREEN - USER separately approved bounded returned-UTS Workstream implementation for UTS-HUD-001 through UTS-HUD-012. Current FAM-006 HUD runtime, renderer proof, surface validators, internal sandbox validators, and source truth now carry the repaired behavior. Hardening H1 is Green; refreshed LV1 and returned USER PASS or waiver remain required before PR Readiness.`

Implementation Evidence: `Active-client live validation and focused interaction self-QA passed at C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_192129_648\monitoring_hud_live_client_interaction_manifest.json with focused proof artifacts under C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_192129_648\live_client_interaction\. Internal sandbox validation passed at C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_internal_sandbox\20260521_193537_manifest.json.`

Implementation Scope Summary: `The repair adds HUD-wide default glow tokens and semantic hover preservation, stronger card/window background opacity to prevent grid bleed-through, minimum button text padding, checked-source hover persistence, max-five dropdown/list proof with NDAI scrollbars, selected/source hover flicker protection, effective current-HUD polling cadence proof, deterministic sensor settings controls, right-aligned Dashboard actions with Manage Data Sources / Feature Deferred copy, and dirty-change guards for current editable HUD windows.`

Hardening H1 Result: `GREEN - H1 pressure-tested UTS-HUD-001 through UTS-HUD-012 with active-client focused proof, HUD surface validation, HUD internal sandbox validation, branch governance validation, and static syntax/compile checks. H1 found no bounded runtime defect and applied no code repair. Green active-client proof: C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_202230_146\monitoring_hud_live_client_interaction_manifest.json with focused artifacts under C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_202230_146\live_client_interaction\.`

Refreshed LV1 Result: `TECHNICAL PASS / USER_TEST_REQUIRED - governance was repaired to make the real user-facing desktop launcher the primary LV1 path and to require detailed OneDrive per-element screenshots plus short video/frame-sequence proof for desktop UI Live Validation. Real shortcut human-client proof passed at C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_human_client_validation\20260521_215945_249\human_client_manifest.json with USER-inspectable evidence under C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_human_client_validation\20260521_215945_249\. Supporting active-client focused proof passed at C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_220614_907\monitoring_hud_live_client_interaction_manifest.json with 17 named per-element screenshots under C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_monitoring_hud_live_validation\20260521_220614_907\focused_element_screenshots\ and short video at C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_monitoring_hud_live_validation\20260521_220614_907\monitoring_hud_lv1_short_video.mp4. Formal UTS handoff refreshed at C:\Users\anden\OneDrive\Desktop\User Test Summary.txt.`

Next Required Gate: `USER UTS review. PR Readiness remains blocked until returned USER PASS or explicit waiver with reason is complete.`

## Evidence And Validation Standard Requested By USER

The USER expects Hardening and Live Validation to inspect every finite visual and functional detail with reviewable evidence, including focused screenshots and video/frame-sequence proof where motion, flicker, dropdown persistence, clipping, or transient state matters.

Validation must inspect individual UI elements, not only helper markers. Required inspection includes buttons, button default state, hover state, active state, focus-visible state, disabled state, danger state, safe-cancel state, row hover, checkbox checked/unchecked/blocked states, dropdown open/hover/selected/reset states, page breaks, divider glow/haze, background grids, background graphics, bleed-through, clipping, scaling, text-to-border padding, scrollbars, window sizes, nested-window flow, dirty guard behavior, and live data behavior.

Helper PASS, manifest PASS, screenshot existence, or DOM presence cannot substitute for artifact-by-artifact visual and functional judgment.

Latest USER Evidence-Governance Correction: `REPAIR - USER rejected the prior LV1 proof because detailed per-element screenshots were not stored as real USER-inspectable images under C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI and because full-desktop screenshots were overused as proof. USER also restated that LV1 must run through the USER-facing desktop launcher with no sandbox/offscreen/direct-runtime substitute as the primary path. This issue form now treats missing OneDrive per-element screenshots, filenames without element labels/names, dev\logs-only images, and helper/direct-runtime proof presented as the USER path as Live Validation blockers.`

Updated LV1 Evidence Requirement: `Every acceptance-critical HUD element/state must have a detailed focused screenshot copied to C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\<validation-lane>\<timestamp>\focused_element_screenshots\ with the element label/name and state/action in the PNG filename. Full desktop screenshots are locator/context evidence only. The human-client shortcut manifest is the primary LV1 path when the desktop launcher is feasible; active-client/WebView/direct-runtime proof is supporting coverage only.`

## Temporary Issue Lifecycle

1. Digest returned USER issues into this form.
2. USER reviews this form and approves, corrects, or rejects the proposed issue framing.
3. Next legal phase should admit a bounded repair setup based on this form, not jump directly into broad runtime patching.
4. Repair setup must decide which items are current-branch repairs, which are validator/proof governance repairs, and which are future-gated.
5. Workstream implementation must reference every issue ID it fixes or explicitly leaves future-gated.
6. H1 must pressure-test each fixed issue with focused screenshots and, where needed, frame/video-style proof.
7. LV1 must rerun real shortcut/client validation and produce a UTS checklist that includes these issue IDs.
8. PR Readiness Stage 1 may delete this temporary form only after all surviving information is folded into durable source truth.

## Issue Index

| ID | Area | USER Classification | Planning Status | Repair Authorization |
| --- | --- | --- | --- | --- |
| UTS-HUD-001 | Button default glow uniformity | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-002 | Background grid bleed-through on cards/windows | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-003 | Default button glow text readability | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-004 | Hover glow must preserve semantic button color | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-005 | Button text-to-border dead-space standard | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-006 | Checked source row hover state | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-007 | Manage Monitors filter max-five menu target | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-008 | Source row hover flicker | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-009 | Polling Rate must affect live source collection rate | REPAIR | Workstream + H1 Green for current HUD source-refresh path; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-010 | Sensor settings window click/state/dropdown/window flow | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-011 | Dashboard button alignment and Data Sources copy/status | REPAIR | Workstream + H1 Green; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |
| UTS-HUD-012 | HUD-wide dirty-change confirmation rule | REPAIR | Workstream + H1 Green for current editable HUD windows; LV1 technical PASS; USER_TEST_REQUIRED | Bounded implementation, H1, and LV1 technical proof complete |

## Repair Setup Disposition Matrix

| ID | Disposition | Bounded Implementation Intent | Required Proof |
| --- | --- | --- | --- |
| UTS-HUD-001 | Current-branch repair candidate | Establish one HUD button default-glow token system by semantic role. | Default/hover/focus screenshots for every button role. |
| UTS-HUD-002 | Current-branch repair candidate | Ensure cards, panels, dropdowns, and child windows block unreadable grid bleed-through. | Focused before/after-style screenshots for Dashboard cards and every active HUD child window. |
| UTS-HUD-003 | Current-branch repair candidate | Make default/non-hover glow border-biased so text center remains readable. | Per-button default-state text readability screenshots at normal and compact widths. |
| UTS-HUD-004 | Current-branch repair candidate | Preserve semantic colors on hover/focus for danger, warning/on, close, discard, delete, cancel, blocked, and primary controls. | Semantic role screenshot set showing hover does not force unrelated green/primary color. |
| UTS-HUD-005 | Current-branch repair candidate | Define and apply minimum button text-to-border padding, with overflow/wrap/width rules for long labels. | Clipping/padding proof for long labels, especially Create Overlay Profile and dropdown toggles. |
| UTS-HUD-006 | Current-branch repair candidate | Add additive hover/focus state for checked, unchecked, blocked, and warning source rows without hiding checked state. | Focused row-state proof plus first-click stress for row, checkbox, and settings affordance. |
| UTS-HUD-007 | Current-branch repair candidate | Enforce max-five visible dropdown/list targets with NDAI scrollbar where space allows. | Open-menu screenshots for every HUD dropdown/list with more than five options. |
| UTS-HUD-008 | Current-branch repair candidate | Prevent timed refresh/rerender from flashing source-row hover state. | Five-second frame-sequence/video-style proof on checked, unchecked, and blocked rows during refresh. |
| UTS-HUD-009 | Conditional current-branch repair | If current HUD source-refresh architecture owns cadence, connect Polling Rate to effective refresh cadence; otherwise make the UI truthfully deferred and record the runtime telemetry seam needed. | Measured cadence proof when implemented, or focused deferred-status proof plus source-truth rationale if future-gated. |
| UTS-HUD-010 | Current-branch repair candidate | Repair sensor settings click routing, display-mode state changes, warning checkbox truth, Rate dropdown persistence/placement/scrolling, default size, warning section boundary, and Manage Monitors parent preservation. | First-click stress, dropdown hold proof, clipping proof, parent-window preservation proof, and subissue-specific screenshots. |
| UTS-HUD-011 | Current-branch repair candidate | Right-align Dashboard actions, relabel Data Sources to Manage Data Sources, keep it blocked, and show Feature Deferred status. | Dashboard focused proof with action order, blocked/deferred behavior, and copy/status. |
| UTS-HUD-012 | Current-branch rule plus future standard | Apply dirty-change guard to all current HUD editable windows and record the rule for future editable windows. | Dirty prompt screenshots, snap-into-view proof, Save/Discard outcome proof, and navigation/close interception proof. |

## Implementation Boundary For Next Approval

Current-Branch Repair Candidates: `UTS-HUD-001, UTS-HUD-002, UTS-HUD-003, UTS-HUD-004, UTS-HUD-005, UTS-HUD-006, UTS-HUD-007, UTS-HUD-008, UTS-HUD-010, UTS-HUD-011, and current editable portions of UTS-HUD-012.`

Conditional Current-Branch Repair Candidate: `UTS-HUD-009 may be implemented only if current FAM-006 HUD source-refresh architecture owns live cadence. If actual external telemetry/provider collection is outside this branch, implementation must make the current UI truthful and future-gate the deeper runtime collector work.`

Future-Gated Items: `New Recording Profile runtime, tray recording controls, export/share, provider/model execution, broad theme/skin work, FAM-007 work, Governance mutation, Compact-AI work, AI Product work, and any telemetry architecture not already owned by the FAM-006 HUD source-refresh path.`

Implementation Must Not: `Create PRs, merge, release, mutate GitHub issues, delete this temporary issue form, change sibling worktrees, change unrelated families, or use helper PASS without artifact-by-artifact visual judgment.`

## Validation And Proof Matrix

Required Artifact Root: `dev\logs\fam_006_monitoring_hud_live_validation\<timestamp>\live_client_interaction\`

Required Artifact Naming Pattern: `uts_hud_<issue-id>_<surface>_<state-or-action>.<png|json|mp4|frames.txt>`

Static Screenshot Requirements:
- `UTS-HUD-001` through `UTS-HUD-005`: every HUD button role in default, hover, focus-visible, disabled, danger, safe-cancel, selected, open, and blocked/deferred states where supported.
- `UTS-HUD-002`: every Dashboard card and every active HUD child window/panel/dropdown/confirmation over grid/background.
- `UTS-HUD-006` and `UTS-HUD-008`: checked, unchecked, blocked, warning, hover, focus, and active source rows.
- `UTS-HUD-007`: Source Filter, Overlay Profile filter, profile selector, Polling Rate, Rate dropdown, and any bounded list with more than five options.
- `UTS-HUD-010`: display mode card, warning checkbox/section, Rate dropdown open state, sensor settings window at default/minimum size, and Manage Monitors parent context.
- `UTS-HUD-011`: Dashboard action row and Manage Data Sources blocked/deferred status.
- `UTS-HUD-012`: dirty prompt for every current editable HUD window, including prompt-visible and post-action outcome states.

Frame Or Video-Style Requirements:
- `UTS-HUD-008`: pointer held over source rows for at least five seconds during active refresh, with no hover flicker.
- `UTS-HUD-010.3`: Rate dropdown remains open for several seconds during refresh and closes only through valid user action.
- `UTS-HUD-010.7`: opening/closing sensor settings preserves or returns to Manage Monitors context.
- `UTS-HUD-012`: prompt snaps into view when close/navigation/state-switch is attempted from a scrolled edit surface.

Stress Requirements:
- Use high-volume overlay, monitor, source, dropdown-option, and sensor settings fixtures where helper support exists.
- Cover at least one large monitor/source state, one large profile list, one large dropdown/list state, repeated first-click activation for each repaired control, and keyboard activation where the control supports it.
- Validate scaling at normal, minimum supported, and compact-but-legal window sizes.

Visual Adjudication Requirements:
- Codex must inspect every focused artifact and record PASS/REPAIR per issue ID.
- Helper PASS, DOM markers, screenshot existence, or manifest existence cannot clear an issue without visual judgment.
- Full-desktop screenshots are locator/context only; focused UI proof is acceptance evidence.

## Source Truth And Validator Update Plan

Branch Record: `Record setup approved, issue matrix admitted, bounded Workstream implementation Green, PR Readiness blocked, and next governed action as Hardening H1 for the returned-UTS repair.`

Branch Plan: `Record setup approval, issue dispositions, validation/proof matrix, Workstream implementation evidence, and temporary issue form lifecycle.`

Backlog And Roadmap: `Remain compact pointer/status surfaces that mention returned UTS REPAIR, Workstream implementation Green, H1 Green, refreshed LV1 pending, and PR Readiness blocked.`

Validators And Helpers: `HUD surface/internal sandbox/live helpers now prove the issue matrix with per-issue coverage and artifact reviewability gates; H1 and LV1 must pressure-test the same coverage rather than relying on generic marker presence.`

UTS Handoff: `Next refreshed UTS must include UTS-HUD-001 through UTS-HUD-012 as explicit USER checklist items.`

Temporary File Lifecycle: `Keep this form until PR Readiness Stage 1 is green, then delete only after all surviving details are folded into durable source truth.`

## Issue Details And Proposed Planning

### UTS-HUD-001 - Button Default Glow Uniformity

USER Observation: Button glow is uniform while hovering, but default/non-hover button glow is not uniform.

Intent: Every button-like control must have a coherent default visual language before hover. Default glow may differ by role, but the role rules must be consistent: primary, secondary, danger, safe-cancel, disabled, selected, and blocked/deferred.

Likely Surfaces: Dashboard actions, Manage Monitors actions, Overlay Profile Settings actions, source settings actions, dropdown toggles, chip buttons, child-window close controls, delete/discard/cancel controls, disabled Edit controls, blocked/deferred controls.

Planning Actions:
- Inventory every current HUD button-like control by semantic role.
- Define allowed default glow tokens per role.
- Define forbidden default states, including mixed green fill, unreadable center haze, and inconsistent border treatment.
- Plan CSS token repair rather than per-button one-offs if source truth supports it.
- Add validator expectations for default state, not only hover state.

Validation Required:
- Focused screenshots of every button role in default state.
- Focused screenshots of the same controls in hover state for comparison.
- Per-control visual adjudication table with PASS/REPAIR.
- At least one dark/backdrop and grid-adjacent screenshot for bleed-through risk.

USER Review Question: Confirm that default button glow may vary by semantic role only if the rules are visibly consistent and readable.

### UTS-HUD-002 - Background Grid Bleed-Through On Cards And Windows

USER Observation: Dashboard group cards show the underlying grid element. The cards should obscure the underlying grid so readability and legibility are consistent. This applies across Dashboard and all child windows where the same issue exists.

Intent: Cards, panels, rows, and child windows must have sufficient surface opacity or backdrop treatment so background grids/graphics do not reduce text and control readability.

Likely Surfaces: Dashboard group cards, Overlay Profile Settings window, Manage Monitors window, Assigned Overlay/status windows, source settings windows, delete confirmations, dirty guards, dropdown menus, profile/source filter menus.

Planning Actions:
- Inventory every panel/card/window surface where a grid or background graphic is visible behind text.
- Define acceptable background-grid visibility. Decorative grid may remain in empty page background, but not through content-bearing surfaces.
- Plan CSS surface tokens for content surfaces, dropdown menus, and confirmation blocks.
- Separate intentional subtle texture from accidental bleed-through.
- Add proof requirements for readable foreground/background contrast.

Validation Required:
- Focused screenshots for Dashboard cards and every HUD child window.
- Pixel/visual comparison against grid-background areas.
- Visual adjudication for text readability, control legibility, and bleed-through.
- Screenshot set must include default, hover, dropdown-open, confirmation, and dirty states where applicable.

USER Review Question: Confirm that decorative grid may remain visible only outside content-bearing cards/panels/windows.

### UTS-HUD-003 - Default Button Glow Center Must Preserve Text Readability

USER Observation: Button glow should only be around the border in default/non-hover state, leaving the center readable.

Intent: Non-hover glow should read as a border/edge affordance, not as a center haze that competes with button text.

Likely Surfaces: All default-state button-like controls, especially Create Overlay Profile, Save, Discard, Delete, Cancel, Manage Monitors, Overlay Profile Settings, source Settings, display-mode chips, dropdown toggles.

Planning Actions:
- Define default glow as border/ring/outset treatment.
- Keep hover/active states allowed to brighten, while still protecting text contrast.
- Review whether existing box-shadow, inset shadow, background gradient, or overlay layer causes center haze.
- Create role-specific examples before implementation.

Validation Required:
- Focused screenshot of default state for every role.
- Text readability check at normal size and minimum supported window width.
- Visual proof that center fill remains stable and text stays legible.

USER Review Question: Confirm that hover may intensify the control but default state should keep most glow on the border.

### UTS-HUD-004 - Hover Glow Must Preserve Semantic Button Color

USER Observation: Hover glow should not alter the default semantic color of a button. Warning Notifications On, Close, Discard, Delete, and similar controls should not turn green when hovered.

Intent: Hover should illuminate the button while preserving its semantic role. Danger remains red, warning/on remains its own state, safe cancel remains readable/neutral, blocked/deferred remains disabled or blocked, and primary/secondary use the Nexus primary treatment.

Likely Surfaces: Warning Notifications, Close, Discard, Delete, Cancel, disabled/blocked Data Sources, Edit disabled/enabled, profile Delete confirmation, dirty guards, source warning controls.

Planning Actions:
- Define semantic hover tokens for primary, secondary, danger, safe-cancel, warning/on, selected, disabled, and deferred controls.
- Repair any global hover class that forces green/primary hover onto all buttons.
- Add role attributes or classes where current markup cannot distinguish semantics.
- Ensure danger and warning states remain semantically obvious.

Validation Required:
- Before/after screenshots for default and hover states for each semantic role.
- Visual adjudication confirming no danger/warning/safe-cancel control turns green unless it is actually primary.
- Keyboard focus proof for same semantic colors.

USER Review Question: Confirm the final semantic color map before implementation.

### UTS-HUD-005 - Button Text-To-Border Dead Space Requirement

USER Observation: Buttons need a minimum buffer zone between text edge and button border. Create Overlay Profile text exceeds the button border in the Overlay Profiles window.

Intent: Every button must preserve readable horizontal and vertical padding. Text must not clip, touch borders, overflow, or be hidden by icons/glow.

Likely Surfaces: Create Overlay Profile, Edit Overlay Profile, Save Profile, Discard, Delete Overlay Profile, Manage Monitors, Overlay Profile Settings, Manage Data Sources, Source Settings, Source Filter, Polling Rate, profile/source dropdown toggles, dirty-guard buttons.

Planning Actions:
- Define a minimum text-to-border padding standard for HUD buttons.
- Add max-width, min-width, wrapping, ellipsis, or responsive sizing rules by control type.
- Identify buttons that require longer labels and either widen them or shorten labels only if USER approves.
- Verify Create Overlay Profile in the default Overlay Profile manager size.

Validation Required:
- Focused screenshot at normal, minimum, and expected compact window widths.
- Per-button text clipping/padding visual inspection.
- Stress with long profile/source names where labels can grow.
- Proof that glow/border does not reduce the effective text buffer.

USER Review Question: Confirm whether long action labels should prefer wider buttons over label shortening.

### UTS-HUD-006 - Checked Source Row Hover State

USER Observation: Hovering over a checked source in Manage Monitors does not visibly change state to show hover.

Intent: Source rows must show hover affordance regardless of checked, unchecked, blocked, or warning state. The hover treatment must not hide the checked state.

Likely Surfaces: Sensor Library source rows, checked source rows, unchecked source rows, blocked/unavailable rows, warning rows, source settings button within rows.

Planning Actions:
- Define layered source row states: base, checked, unchecked, blocked, warning, hover, focus, active.
- Ensure hover is additive and does not erase checked/blocked/warning identity.
- Coordinate with UTS-HUD-001 through UTS-HUD-004 so the row hover and button glow use the same visual language.

Validation Required:
- Focused screenshots for checked-hover, unchecked-hover, blocked-hover, warning-hover.
- Keyboard focus proof for source rows.
- First-click proof that row hover does not interfere with checkbox or settings button activation.

USER Review Question: Confirm checked-hover should be visually distinct but still clearly checked.

### UTS-HUD-007 - Manage Monitors Filter Max-Five Menu Target

USER Observation: Filters inside Manage Monitors show more than five total entries at a time. Reduce to five and keep the scrollbar.

Intent: Dropdown menus and bounded option lists in the HUD should use the max-five visible option target before internal NDAI-styled scrolling, unless a smaller window forces fewer visible rows.

Likely Surfaces: Manage Monitors Source Filter, Overlay Profile filter, Overlay Profile profile selector, Polling Rate dropdown, sensor settings Rate dropdown, any current bounded dropdown inside the HUD.

Planning Actions:
- Inventory all dropdown/list menus and classify whether the max-five rule applies.
- Define menu item height and max-height tokens to enforce exactly five visible options where practical.
- Ensure scrollbars are NDAI-styled, not native/basic.
- Avoid outer-window scrollbars caused by dropdown expansion.

Validation Required:
- Focused screenshot of each dropdown with more than five options.
- Proof that only five options are visible before scrolling where space allows.
- NDAI scrollbar visual proof.
- Smaller-window exception proof if fewer than five are visible due to viewport constraints.

USER Review Question: Confirm the max-five rule applies to every HUD dropdown/list unless source truth records an exception.

### UTS-HUD-008 - Source Row Hover Flicker

USER Observation: Hover illumination on source rows in the monitors tab flashes periodically, seemingly every one second, for checked, unchecked, and blocked sources.

Intent: Hover illumination must remain stable while the pointer remains over the same row. Background refresh or polling should not reset or flash hover state.

Likely Surfaces: Sensor Library source rows, source list refresh, source state polling, checked-state updates, blocked/unavailable updates, row rerender logic.

Planning Actions:
- Investigate whether timed state refresh rerenders source rows on a one-second interval.
- Preserve stable DOM nodes or stable hover classes during data refresh.
- Separate live value refresh from visual row affordance state.
- Coordinate with polling-rate behavior in UTS-HUD-009.

Validation Required:
- Video or frame-sequence proof with pointer held over checked, unchecked, and blocked rows for at least five seconds.
- Evidence that hover state does not flash during source data refresh.
- Stress proof with many sources and active polling.

USER Review Question: Confirm frame-sequence proof is required for this issue because static screenshots cannot prove flicker absence.

### UTS-HUD-009 - Polling Rate Must Affect Live Source Collection

USER Observation: Polling Rate does not actually change the rate at which data is collected live within the Source section, and it should.

Intent: Polling Rate controls must affect live data collection/refresh cadence for the applicable monitor/source scope. If a setting is a future placeholder, the UI must be clearly labeled deferred or non-functional; otherwise it must work.

Likely Surfaces: Monitor generalized Polling Rate, sensor-specific Polling Rate, Default override behavior, source data refresh loop, source settings window, persistence state.

Planning Actions:
- Determine current actual data collection architecture and whether polling is simulated, fixed, or configurable.
- Define precedence: source-specific value, monitor generalized value, default global value.
- Decide whether this is current-branch runtime scope or requires a separate runtime seam.
- If implemented in current branch, add deterministic test hooks to prove cadence changes without relying only on visual timing.
- If deferred, make copy/status truthful and record why.

Validation Required:
- Runtime proof measuring source refresh intervals before and after Polling Rate changes.
- Screenshot/video proof of UI selection plus log/manifest proof of effective cadence.
- Persistence proof across save/load.
- Default/override proof.

USER Review Question: Confirm whether this must be implemented now or can be explicitly deferred with truthful UI status.

### UTS-HUD-010 - Sensor Settings Window Click/State/Dropdown/Window Flow

USER Observation: Sensor Settings opens, but many interactions are wrong or unreliable. Clicks show a pressed cue, but state does not change. Rate dropdown disappears, clips at the window edge, and cannot scroll. The window needs more room and future warning settings structure. Opening another window inside Manage Monitors closes Manage Monitors, causing the user to reopen it.

Intent: Sensor Settings must be a reliable user-facing settings surface. It must preserve Manage Monitors context, support first-click state changes, provide adequate room for future Warning settings, and avoid clipped dropdowns.

Likely Surfaces: Source Settings button, sensor settings child window, display-mode chips, warning checkbox, Rate dropdown, dropdown menu layer/z-index/overflow, Manage Monitors child-window ownership, close/back/save/discard behavior.

Planning Actions:
- Treat UTS-HUD-010 as a parent issue with subissues UTS-HUD-010.1 through UTS-HUD-010.7.
- Inspect click routing, focus trap, stale DOM references, overlay/z-index, pointer-events, state commit logic, and rerender timing.
- Decide whether sensor settings should be modal child window, nested panel, or Manage Monitors subview.
- Define window ownership so opening/closing sensor settings does not unintentionally close Manage Monitors.
- Increase default sensor settings window size if current layout cannot fit current and near-future settings.
- Add a Warning Settings section boundary with copy for future settings.

Validation Required:
- First-click stress proof for every sensor settings control.
- Focused screenshots for normal, hover, active, focus, selected, dropdown-open, and warning-section states.
- Frame/video proof for Rate dropdown persistence and no auto-close.
- Clipping proof at normal and minimum window positions.
- Parent-window preservation proof: close/back/save/discard from sensor settings returns to Manage Monitors without requiring reopen.

USER Review Question: Confirm whether the preferred UX is a Manage Monitors subview, a child window that keeps Manage Monitors open, or a redesigned flow decided in repair setup.

#### UTS-HUD-010.1 - Display Mode Cannot Switch

Observation: In the display mode card, the user cannot switch between display modes.

Planning Actions: Trace click handler, selected-state commit, rerender, and disabled/stale state. Ensure first-click and keyboard activation both change selected mode.

Validation Required: Row/button click proof, keyboard proof, persistence proof, and repeated first-click stress.

#### UTS-HUD-010.2 - Warning State Checkbox Cannot Be Clicked

Observation: User cannot click the warning state checkbox.

Planning Actions: Verify whether this is an enabled current control or future/deferred placeholder. If current, repair click/state/persistence. If future, disable truthfully with deferred copy.

Validation Required: Click/keyboard toggle proof or clear deferred-disabled proof.

#### UTS-HUD-010.3 - Rate Dropdown Disappears After Opening

Observation: Pressing the Rate dropdown makes it disappear about a second later.

Planning Actions: Investigate refresh/rerender timeout, blur handling, focus trap, and click-away logic. Prevent data refresh from closing active dropdowns.

Validation Required: Frame-sequence proof holding dropdown open for several seconds during source refresh.

#### UTS-HUD-010.4 - Rate Dropdown Clips And Cannot Scroll

Observation: Dropdown is clipped by the window edge and cannot scroll.

Planning Actions: Repair dropdown layer, placement, max-height, overflow, and scroll-pane styling.

Validation Required: Focused screenshot proving no clipping, max-five target where applicable, and NDAI scrollbar.

#### UTS-HUD-010.5 - Increase Default Sensor Settings Window Size

Observation: Default window size should prepare for warning settings.

Planning Actions: Define default/min/max window dimensions for current settings plus warning section placeholder.

Validation Required: Focused screenshot at default and minimum supported size showing no clipping or outer scrollbar unless unavoidable.

#### UTS-HUD-010.6 - Warning Settings Page Break And Future Plan

Observation: Add a page break for `Enable Warning Notifications for this sensor` and future warning settings. Default warning values should follow monitor settings unless overridden at sensor level.

Planning Actions: Define current checkbox copy, page break, future warning-settings placeholder, and default/override precedence without implementing unapproved future notification runtime.

Validation Required: Focused proof of warning section divider/page break, checkbox/default copy, and future-scope boundary.

#### UTS-HUD-010.7 - Nested Window Flow Closes Manage Monitors

Observation: Opening another window inside Manage Monitors closes Manage Monitors. Closing, discarding, saving, or backing out forces the user to reopen Manage Monitors.

Planning Actions: Redesign or repair parent/child ownership so Manage Monitors remains available. Define close/back/save/discard return paths.

Validation Required: Proof that opening sensor settings preserves Manage Monitors, and every exit path returns to the prior Manage Monitors context.

### UTS-HUD-011 - Dashboard Button Alignment And Data Sources Copy/Status

USER Observation: In Dashboard, move buttons so they align right instead of left. Put Settings on the far right and HUD Overlay Deferred to the left. Rename the Data Sources button to `Manage Data Sources`, keep it blocked for now, and change the status field to `Feature Deferred` so the reason is understandable.

Intent: Dashboard action rows should have clear hierarchy, aligned action placement, and truthful deferred status for unavailable features.

Likely Surfaces: Dashboard group cards, Settings button, HUD Overlay Deferred action/status, Data Sources card/action/status, dashboard layout CSS, UTS wording.

Planning Actions:
- Define Dashboard action alignment rule for grouped card buttons.
- Update copy plan for `Manage Data Sources`.
- Define blocked/deferred visual and semantic status token.
- Keep Data Sources blocked until a separate USER-approved implementation.

Validation Required:
- Focused Dashboard screenshot proving right-aligned action buttons.
- Visual comparison of Settings far-right and HUD Overlay Deferred left of it.
- Proof that `Manage Data Sources` is blocked/deferred and status says `Feature Deferred`.
- First-click blocked/deferred proof that it does not start unapproved behavior.

USER Review Question: Confirm the desired exact order of actions in the Dashboard row.

### UTS-HUD-012 - HUD-Wide Dirty-Change Confirmation Rule

USER Observation: The Manage Monitors unsaved-change confirmation rule should apply across the entire HUD so changes are not lost accidentally.

Intent: Any HUD window or flow with unsaved user edits must guard close, navigation, state switching, and window changes with Save/Discard behavior. The prompt must be visible and must not be hidden off-scroll.

Likely Surfaces: Overlay Profile Settings, Manage Monitors, source settings, assigned overlay assignment/status, profile delete confirmation, future data sources/settings windows, any editable child window.

Planning Actions:
- Inventory every current HUD editable state and navigation/close route.
- Define a shared dirty-state guard contract: trigger, visible prompt, Save, Discard, no accidental loss, no hidden prompt, return path.
- Decide whether each current editor needs immediate repair or future-gated adoption.
- Add validator/proof requirements for all dirty flows.

Validation Required:
- Focused screenshot of dirty prompt for each editable window.
- Proof that close/navigation/state switch triggers prompt.
- Proof prompt scrolls/snaps into view if needed.
- Save persists, Discard drops, and Cancel is absent where USER requested no Cancel.
- Reopen proof confirms state outcome.

USER Review Question: Confirm this rule should become a HUD-wide standard before PR Readiness.

## Cross-Issue Repair Planning Requirements

Repair setup must produce:

- A one-by-one disposition for UTS-HUD-001 through UTS-HUD-012.
- A USER-readable design-intent summary before runtime edits.
- A list of current-branch repairs versus future-gated items.
- A validation matrix listing exact screenshots and frame/video proof per issue.
- A first-click and stress-test plan covering large volumes of overlays, monitors, sources, dropdown options, and sensor settings interactions.
- A source-truth update plan for branch record, branch plan, UTS checklist, validators, and compact backlog/roadmap pointers.
- A proof artifact naming convention so USER can review each state without guessing.

## Recommended Next Legal Phase

Next Legal Phase: `Refreshed Live Validation Stage 1 / UTS recheck`

The setup phase, bounded Workstream implementation, and Hardening H1 are Green for the returned-UTS issue matrix. The next governed action is refreshed Live Validation Stage 1 / UTS recheck through the real user-facing client path. PR Readiness remains blocked until refreshed LV1 and returned USER PASS or explicit waiver with reason are recorded.

## Exact USER Decision Needed

Approve refreshed Live Validation Stage 1 / UTS recheck for the bounded returned-UTS issue repair on `feature/fam-006-overlay-profile-runtime-foundation` in `C:\Nexus Worktrees\FAM-006`, using this temporary issue form and H1 proof at `C:\Nexus Worktrees\FAM-006\dev\logs\fam_006_monitoring_hud_live_validation\20260521_202230_146\monitoring_hud_live_client_interaction_manifest.json` as the baseline. Codex may validate through the real user-facing shortcut/client path, capture focused proof for UTS-HUD-001 through UTS-HUD-012, refresh the UTS checklist/handoff, update directly supporting source truth/results, run required validation, and commit/push if green. PR Readiness, PR creation, merge, release, GitHub issue mutation, artifact upload/import, sibling-worktree changes, Recording Profile runtime, tray recording, export/share, provider/model execution, broad theme/skin work, FAM-007, Governance, Compact-AI, AI Product work, and any telemetry/provider architecture outside the current FAM-006 HUD source-refresh path remain separate USER decisions.
