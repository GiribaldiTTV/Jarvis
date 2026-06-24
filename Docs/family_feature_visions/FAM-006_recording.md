# FAM-006 Recording Family Feature Vision

Family Feature Vision ID: `F6-FF01`
Parent FAM: `FAM-006`
Feature Category: `Recording`
Category-Level Purpose: `Durable Recording feature-category direction for capturing trusted local Monitoring/HUD output through Overlay Profile targets, native NDAI logs, USER-requested exports, and compact user-facing control surfaces.`
USER-Facing Surfaces: `Dashboard Recording Card; Dashboard quick access when admitted; Recording Studio; Log Viewer Studio shell and later viewer; native log folder; exported-log folder; tray/keybind/settings surfaces when later admitted.`
Experience Flow: `USER selects or creates an Overlay Profile, sees Recording target/readiness on the Dashboard, starts/stops through an admitted control surface, receives native NDAI output, and later reviews or exports logs through admitted Log Viewer Studio flows.`
Included Capabilities: `Target/status display; Overlay Profile target mirroring; Start/Stop when admitted; native NDAI output/readback; exported-log access when admitted; Recording Studio planning; Log Viewer Studio planning; tray/keybind/settings planning; Overlay Profile persistence dependency review.`
Explicit Non-Goals: `Runtime implementation by this file; Workstream approval; PR/merge/release/issue closeout; provider/model work; FAM-007 mutation; Governance worktree mutation; neutral-main mutation; full Native Log Loader implementation; automatic third-party-readable export; separate Recording Profile system.`
Durable Feature Element Inventory: `F6-FF01-E01 - Dashboard Recording Card target/status surface and visual inheritance proof; F6-FF01-E02 - Recording Studio focused control/status surface and window proof; F6-FF01-E03 - Log Viewer Studio native/export shell and future viewer boundary; F6-FF01-E04 - native NDAI log artifact model and readback proof; F6-FF01-E05 - USER-requested export artifact model and readability proof; F6-FF01-E06 - tray/keybind/settings future-control boundaries; F6-FF01-E07 - Overlay Profile persistence dependency for recording target reliability.`
Deferred Feature Carryforward: `deferred item rows preserve title, dependency trigger, grouping recommendation, proof expectation, and durable disposition for Recording Studio, Log Viewer Studio, exported logs, tray controls, keybinds, settings, warning dismissal, Overlay Profile persistence dependency, Dashboard quick access, and Native Log Loader relationship.`
Design Options: `Option F planning solidification before implementation-shape selection; Option C/C-lite Dashboard Recording Card plus Recording Studio plus minimal Log Viewer Studio shell; Start/Stop ownership options; Studio minimize behavior options; direct log-folder button versus Log Viewer Studio access; native-only versus native-plus-explicit-export artifact options.`
Proof Expectations: `BP1 must produce a real Recording branch vision; BP2 must translate accepted vision into a concrete engineering plan; BP3 must prove Workstream readiness; Hardening and Live Validation must provide photo/video or ordered-frame proof for admitted controls, windows, actions/effects, visual-system inheritance, native/export boundaries, UTS coverage, rollback, and USER-elevated manual validation where visual proof is impossible. Before formal Live Validation or UTS handoff, Recording UI must pass a Pre-LV Visual Purpose Conformance Gate that proves the window looks like its accepted purpose and vision contract requires; Live Validation then proves it functions.`
Pre-Live Visual Gate: `Before any formal Live Validation pass or UTS handoff for Recording Studio, Log Viewer Studio, Dashboard Recording Card, or other admitted Recording UI, Codex must inspect recorded photo/video evidence against the window's accepted purpose and vision contract, inventory every visible element group, compare shared primitives to the admitted reference surfaces, record PASS/REPAIR/BLOCKED/WAIVED_WITH_REASON for each group, and only then run functional interaction proof. Live Validation proves the already-inspected UI and then proves behavior; it must not be the first place obvious visual drift is discovered.`
Branch Readiness Consumption Notes: `BR1/BR2 should load this file as feature-category context, present branch-lane options against it, surface applicable deferred carryforward dynamically, and reject issue-shaped or single-slice drift unless USER explicitly selects that path.`
BP1 Context Notes: `BP1 should decompose Recording by Dashboard access, Recording card, Recording Studio, Log Viewer Studio, tray, keybind, native log model, export model, settings, and Overlay Profile dependency, then return USER-editable options, recommendations, risks, proof expectations, and exact decisions.`
Fold-Down History: `Created from USER-approved FAM-006 Recording planning/admission evidence and later updated during FAM-006 current-main reconciliation to satisfy the formal Family Feature Vision marker contract.`
Active-State Wording Scan: `PASS - durable feature-category vision only; not a branch route, selected-next, PR, worktree, or release-window ledger.`

## Purpose

This Family Feature Vision owns durable product direction for Recording inside
FAM-006 Monitoring and HUD. It sits below the broad FAM-006 family vision and
above any branch-specific Branch Vision Contract Snapshot.

It exists so Branch Readiness and BP1 can start from a real Recording feature
vision instead of rediscovering Recording Studio, Log Viewer Studio, tray,
keybind, native-log, export, and settings questions after implementation has
already begun.

## Source Inputs

- Project vision: `Docs/nexus_vision.md`
- Family vision: `Docs/family_visions/FAM-006_monitoring_and_hud.md`
- Planning review packet: `C:\Nexus USER\Planning\FAM-006-Planning-20260608-080430.zip`
- External planning candidate: `C:\Nexus Governance State\governance_candidates\fam006_recording_branch_planning_depth_reform_plan.md`
- Branch receipt evidence: `Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md`
- Branch planning evidence: `C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_plan.md`
- Issue evidence: GitHub issue `#258`, Dashboard HUD Overlay Profiles persistence after app restart

These inputs are evidence. This file owns the durable Recording feature-category
direction after USER-approved admission.

## Feature Purpose

Recording should let the USER capture a trustworthy local record of the selected
HUD/Dashboard Overlay Profile target with clear status, visible control, durable
native NDAI output, and a later export path for third-party-readable files.

Recording must feel like part of the Monitoring and HUD product surface, not a
debug panel, proof panel, or disconnected logging utility.

Visual acceptance is binary for admitted Recording UI. `Better`, `closer`,
`looks acceptable`, `feels good`, or helper-green without Codex visual
adjudication is not green. A visible Recording surface may enter formal Live
Validation only after its shared primitives, purpose-specific layout, and
element states are proven as `PASS`, explicitly `WAIVED_WITH_REASON`, or
`Not Applicable With Reason` against the accepted vision chain and reference
surfaces.

Full-desktop and full-window context proof is controlling when Recording Studio
or Log Viewer Studio acceptance depends on scale, footprint, placement,
parent/child relationship, dead space, or desktop composition. Focused crops are
required for element inspection, but they cannot green-light a material visual
claim by themselves when full-context evidence shows a contradiction. If a USER
or packet review surfaces a full-desktop contradiction after a focused visual
packet claimed green, the packet must reopen as `REPAIR` until the contradiction
is classified, source-truth impact is recorded, and any required options or
runtime repair path is returned to USER review.

Recording visual review packets must include a red-team full-context pass before
they can support renewed H1, Live Validation, UTS, or PR Readiness. The pass must
look for dead space, disconnected controls, oversized footprint, fake-workspace
smell, parent/child placement drift, row-container inheritance gaps,
underglow/divider rhythm mismatch, control label pressure, cropped-proof
masking, and scope drift between a doorway shell and a full workspace.

When a Recording packet asks USER to choose or revise a visual/spatial option,
that option must be shown with rendered media rather than text-card summaries.
Nested-card inheritance options, child-window placement behavior, and Log
Viewer doorway layout options require packet-contained rendered PNGs/contact
sheets or equivalent media. Full desktop/context diagrams are required when
placement, footprint, or parent/child relationship is material. Text-only option
cards, clipped option text, local-path-only proof, or missing command-output
evidence keep the packet in `REPAIR`.

After USER selects a visual/spatial option direction, the next packet must stop
presenting that direction as an open recommendation and must preserve the
selected semantics exactly. Selected Recording/Log Viewer option packets must
include a selected-direction summary, exact labels, selected/rejected/deferred
option dispositions, packet-contained rendered media, validation-output records,
and clean post-commit/post-push Git proof when helper/source changes were
committed. For the current branch selection, A2 revised preserves `TARGET -
Default Overlay Profile`, `STATE - Ready - 2 active monitors`, no bottom helper
copy, and ACTION-002 `OPEN LOG VIEWER STUDIO`; B2 preserves same-session moved
position with restart reset near parent; C2 revised preserves `OPEN NATIVE LOGS`
and `OPEN EXPORTED LOGS`, no local path display by default, and no full-viewer
workspace implication.

## Relationship To FAM-006

Recording belongs to FAM-006 because it depends on Dashboard/HUD visibility,
Overlay Profile state, monitor membership, visual-system inheritance, local file
hygiene, and user-facing validation proof.

Recording does not create a separate Recording Profile system by default. The
Dashboard/HUD Overlay Profile selection remains the recording target source
unless a later USER-accepted feature vision changes that model.

## USER-Facing Surfaces

### HUD Dashboard Recording Access

The Dashboard may provide quick Recording access, but it should not become the
full Recording workspace.

Expected shape:

- a small, obvious Start/Stop affordance when a branch admits quick access
- compact target and status context on a Recording card
- enough information for trust without turning the card into a full studio
- visual-system inheritance from existing Dashboard cards
- truthful disabled, saved, unavailable, and error states

### Dashboard Recording Card

The Recording card is the Dashboard summary and launch surface for Recording.

It should:

- display the selected Overlay Profile target
- show recording readiness and result state
- keep copy concise
- expose admitted Recording actions without crowding the Dashboard
- sample existing Dashboard card chrome, rows, dividers, typography, spacing,
  button treatment, hover/focus/disabled states, glow, and layout density

It should not:

- introduce a separate card visual grammar
- use a unique green-box/table style
- duplicate the HUD Overlay card
- become the long-form recording configuration or log-review surface

### Recording Studio

Recording Studio is the ultra-lightweight detached Recording controller when a
branch admits it. The current Option C carrier admits a bounded compact
standalone-capable controller that owns Start/Stop, recording truth, target
truth, native-log status, and a route to Log Viewer Studio without requiring the
USER to reopen HUD Dashboard.
Dashboard Quick Access may provide a compact Start/Stop shortcut when branch
planning and implementation proof admit it. Tray integration, keybind behavior,
close-while-recording warnings, and bulky settings remain separate future gates
until accepted by later planning.

Expected direction:

- non-child, exclusive, standalone-capable window rather than a Dashboard child
  panel
- compact form factor that behaves like a small detached media-control panel
- standalone window layout that is not a Dashboard card clone and not an AI
  Control Center / command-center clone
- independent lifecycle while Nexus Desktop AI is running: it may launch from HUD
  Dashboard, but it must remain open, truthful, and useful if HUD Dashboard is
  closed where source truth permits
- visual-system inheritance from existing Nexus/FAM-006 windows, including chrome,
  color, typography, spacing, buttons, glow/focus/hover/disabled states, and
  compact density rather than generic utility-window styling
- detached child-window title grammar: Recording Studio is independent and
  taskbar/minimize-capable, but its title/header treatment follows the FAM-006
  child-window header pattern of category line plus strong title; it must not
  render a separate rounded title card or main-window hero/title card
- shared rendered primitive inheritance for same-class window chrome, title/header,
  action buttons, row/divider panels, state text, hover/focus/pressed/disabled
  states, and compact body background. If a promoted global primitive does not
  exist but an accepted rendered Nexus surface does, Recording Studio must reuse
  that rendered CSS/DOM primitive path or stop for side-by-side USER visual
  adjudication; reference-derived approximation is not a closeout-grade substitute.
- bounded shared primitive carry-in for the active returned-UTS repair:
  Recording Studio and Log Viewer Studio may consume
  `nexus_visual/nexus_window_primitives.css` as a FAM-006-carried
  `nexus-window-primitives-v1` implementation candidate for UIREF-001,
  UIREF-002, UIREF-003, and compact feature-studio body primitives. This is not
  broad FAM-002 promotion or proof that other worktrees have adopted the
  primitive. It is the required branch-local code path that prevents this branch
  from recreating AI Control Center / UIREF shared element groups by eye.
- window placement continuity by carrying down the Project UI Vision rule for
  USER-moved windows to restore position safely across sessions where feasible
- Start/Stop control ownership when the branch admits full studio behavior
- selected Overlay Profile target display
- recording state display
- native log status
- Log Viewer Studio doorway/action
- minimal status copy that does not dominate the controller
- close and minimize affordances
- moveable window behavior with safe position memory across launches where
  feasible
- no active resize affordance in the current compact Recording Studio contract;
  Recording Studio should keep its compact controller size while preserving the
  USER-moved position
- deterministic default placement must be proven or optioned before runtime
  implementation closes. Branch-local proposed doctrine is: feature-studio
  child windows open near their parent surface by default unless USER selects a
  different behavior; same-session reopen may restore the last USER-moved
  position; after app or computer restart the window defaults near the parent
  unless USER selects persistent last-position behavior plus a later reset
  route.
- reset-to-default position behavior remains future-gated until the global
  settings/reset-default-window-position surface is admitted

Close behavior needs explicit BP1/BP2 acceptance before implementation. The
preferred warning model is: closing the Studio while recording warns that the
recording continues until the USER stops it or Nexus Desktop AI exits. A local
dismissal preference may be allowed if a later branch admits it.

Minimize behavior also needs explicit acceptance. The durable design question is
whether Studio minimizes to the Windows taskbar or folds into a dedicated
Recording tray icon to avoid taskbar clutter.

### Log Viewer Studio

Log Viewer Studio is the Recording log access shell and future expandable log
workspace when a branch admits it. The current Option C carrier admits only a
compact current-branch shell for native and exported log folder access;
previous-log selection, graph/log viewing, in-app log viewing, export
customization, user-selected export file types, and Native Log Loader
integration remain future gates until accepted by later planning.

Expected direction:

- non-child, exclusive window
- independent from the Dashboard child-window system
- standalone window layout that is not a Dashboard card clone and not an AI
  Control Center / command-center clone
- compact folder-access shell composition for the current branch
- visual-system inheritance from existing Nexus/FAM-006 windows, including chrome,
  color, typography, spacing, buttons, glow/focus/hover/disabled states, and
  compact density rather than generic utility-window styling
- detached child-window title grammar: Log Viewer Studio is independent and
  resizable, but its title/header treatment follows the FAM-006 child-window
  header pattern of category line plus strong title; it must not render a
  separate rounded title card or main-window hero/title card
- shared rendered primitive inheritance for same-class window chrome, title/header,
  action buttons, row/divider panels, state text, hover/focus/pressed/disabled
  states, and compact body background. If a promoted global primitive does not
  exist but an accepted rendered Nexus surface does, Log Viewer Studio must reuse
  that rendered CSS/DOM primitive path or stop for side-by-side USER visual
  adjudication; reference-derived approximation is not a closeout-grade substitute.
- bounded shared primitive carry-in for the active returned-UTS repair:
  Log Viewer Studio may consume `nexus_visual/nexus_window_primitives.css` as
  the same FAM-006-carried `nexus-window-primitives-v1` path used by Recording
  Studio for same-class chrome, detached child-window title row, row, body, and control-state
  primitives while keeping its compact log-access-shell composition.
- window placement continuity by carrying down the Project UI Vision rule for
  USER-moved windows to restore position safely across sessions where feasible
- access to the native NDAI log folder
- access to the exported-log folder
- previous-log selection after later planning
- in-app log viewing after later planning
- export flow after later planning
- moveable window behavior with safe position memory across launches where
  feasible
- resize affordance for the admitted Log Viewer Studio shell because later log
  review content and path/status readability need screen-space flexibility
- doorway footprint, row/action relationship, and placement behavior must be
  proven with full-desktop/full-context evidence or packeted visual options. A
  focused screenshot that shows readable rows and buttons does not prove that
  the Log Viewer Studio shell is appropriately compact in the USER's desktop
  context.
- doorway layout options must be actual rendered alternatives when USER review
  is choosing between vertical stack, inline row actions, footer actions, or a
  future-leaning shell; prose-only cards are not enough.
- maximize/fullscreen remains future-gated until source truth decides whether
  loaded-log graph viewing lives inside Log Viewer Studio or opens a separate
  loaded-log viewer window
- reset-to-default position behavior remains future-gated until the global
  settings/reset-default-window-position surface is admitted

Log Viewer Studio should distinguish native NDAI logs from exported files.
Native logs are the product artifact. Exported files are USER-requested
conversions for another reader or tool.

### Tray Recording Visibility And Control

Recording needs visible user-facing transparency when recording behavior is
admitted.

Future tray direction:

- dedicated recording-state visibility when Recording capability is enabled
- left-click Start/Stop only if USER accepts that behavior
- right-click options for Recording Studio, Log Viewer Studio, Start/Stop, and
  related admitted actions
- tray-state clarity that does not hide recording from the USER

Tray behavior is not implementation-authorized by this vision file.

### Keybind Start/Stop

Recording should eventually support a USER-customizable keybind for Start/Stop.

Future settings should decide whether keybind-start opens Recording Studio. The
default may open Studio unless USER accepts a setting that suppresses it.

Keybind behavior is not implementation-authorized by this vision file.

### Settings

Recording settings should be compact and conventional when admitted.

Potential settings:

- what happens when recording starts
- what happens when recording stops
- whether keybind-start opens Recording Studio
- whether stop opens Log Viewer Studio
- warning dismissal preferences
- export defaults
- native log location
- exported log location

Local one-off acknowledgements, such as "do not show this warning again", should
be separated from global categorized settings.

## Native And Export Artifact Model

Normal product recording should save as a native NDAI recording log owned by
Nexus Desktop AI.

Native NDAI log:

- canonical product artifact
- read by NDAI for future in-app viewing and validation
- not designed as the default third-party-readable file
- should preserve local file hygiene and privacy-safe boundaries
- current default root is the flat product folder `Recordings`; feature-named
  child folders such as `Monitoring HUD` must not be introduced unless a later
  USER-accepted export/storage design admits that taxonomy

Exported log:

- USER-requested conversion
- supports selected readable formats only after an export branch admits them
- should be validated in a user-forward way so the exported file is easy to
  inspect in the target class of software
- belongs in an exported-log folder, separate from native NDAI log storage
- current default root is the flat product folder `Exported Logs`; feature-named
  child folders must not replace the exact exported-log root without later
  USER-approved storage planning

Manual validation exports may exist as test artifacts under governed validation
roots, but they must not become normal product flow.

## Experience Flow

1. USER opens the Dashboard and sees a Recording card that matches the Dashboard
   visual system.
2. Recording target follows the Dashboard/HUD Overlay Profile selection.
3. USER can see whether Recording is ready, unavailable, recording, or saved.
4. A branch may admit quick Dashboard Start/Stop, Recording Studio Start/Stop,
   or both, but BP1 must make the ownership and behavior explicit.
5. Stopping a recording produces native NDAI output.
6. USER can later use Log Viewer Studio to review native logs or export selected
   logs into supported readable formats.
7. Tray and keybind behavior remain future decisions until admitted.

## Included Capabilities

Recording feature planning may include:

- Dashboard Recording card target and status presentation
- Start/Stop behavior when admitted by branch planning
- snapshot-at-start target policy when accepted by branch planning
- native NDAI log output
- native output readback proof
- exported-log folder access when admitted
- Recording Studio planning
- Log Viewer Studio planning
- tray recording visibility planning
- keybind planning
- recording settings planning
- Overlay Profile persistence dependency review

## Explicit Non-Goals

This Family Feature Vision does not authorize:

- runtime implementation
- Workstream implementation
- PR creation
- merge
- release
- issue closeout
- provider/model work
- FAM-007 mutation
- Governance worktree mutation
- neutral-main mutation
- Native Log Loader implementation
- export/share implementation
- tray implementation
- keybind implementation
- broad theme or skin redesign
- creation of a separate Recording Profile system

## Cross-FAM Dependency Classification

Cross-FAM Dependency Map: FAM-006 Recording names FAM-007 only as an explicit non-goal and ownership boundary for provider/model work and AI capability-pack behavior; Recording does not admit FAM-007 implementation, provider/model mutation, or AI package work.

Dependency ID: F6-XFAM-D01

Originating FAM: FAM-006

Originating FFV / Element: F6-FF01 Recording native/log/control surfaces.

Affected FAMs: FAM-007 Local AI and Capability Packs.

Affected FFV / Element or Not Created: Not Created.

Dependency Scope Class: Transferred FAM Work

Carry-In / Deferral / Transfer Decision: Any provider/model or AI capability-pack behavior discovered while planning or validating Recording must transfer to a legal FAM-007 Branch Readiness carrier or remain future-gated; FAM-006 Recording may only preserve the boundary and must not implement that work.

Required Contract / Capability: FAM-007 would own any future provider/model or AI capability-pack contract that Recording might consume later; no such contract is required for the admitted Recording native/log/control surfaces.

Suggested Grouping: Group future provider/model or AI capability-pack work with the relevant FAM-007 feature vision or branch package rather than with FAM-006 Recording.

Proof Expectation: FAM-006 Recording proof must show provider/model work remains absent or future-gated; any future FAM-007 adoption must provide its own Branch Readiness, BP1/BP2/BP3, validation, and USER review proof.

Durable Disposition: Transferred / Future FAM-007 Owner

Affected FAM Receipt / Fold-Down Target: Fold down to the FAM-007 Family Vision or a future FAM-007 Family Feature Vision dependency candidate if USER later admits provider/model or AI capability-pack work.

Worktree-To-Worktree Mutation: None; direct mutation of another active worktree is blocked unless USER separately approves a bounded cross-worktree waiver.

## Design Options To Preserve For BP1

### Planning Solidification Before Scope Selection

Option F is a process route, not a peer implementation package beside the
current-branch scope options.

When USER selects Option F, BP1 must:

- digest the USER-submitted Recording ecosystem planning first
- revise and recommend against that planning before selecting final
  current-branch scope
- keep BP1 USER Gate State pending until USER accepts, waives, rejects, or
  requests another revision
- preserve accepted durable Recording ecosystem direction in this file without
  turning deferred carryforward into active branch state
- return a revised decision surface that lets USER choose the branch
  implementation shape after the vision is solid

Current USER leaning after planning solidification is a refined Option C /
C-lite: keep the Dashboard Recording card as compact quick-access/status
surface, treat Recording Studio as likely current-branch relevant when BP2/BP3
can prove it stays bounded, and admit only a minimal Log Viewer Studio
launch/folder shell when it directly supports Recording native/export log
access. Full Log Viewer Studio, previous-log selection, export customization,
tray controls, keybinds, global settings, and Native Log Loader full
implementation remain future-gated unless BP2/BP3 prove a minimal part is
required for this branch.

### BP2 Consumption After Option F

USER accepted the revised FAM-006 Recording BP1 Branch Vision after Option F
planning solidification and selected Option C as the current-branch
implementation-shape candidate for BP2 planning.

For BP2, Option C means:

- Dashboard Recording Card remains the compact quick-access/status surface.
- Recording Studio may be planned as the focused recording control/status
  surface when BP2/BP3 can prove it remains bounded.
- Minimal Log Viewer Studio launch/folder shell may be planned only where it
  directly supports Recording native/export log access.
- Native NDAI logs remain the normal product artifact.
- Exported logs remain USER-requested export artifacts.
- Open native/export log folder behavior should remain usable before a
  recording is created in the active session.
- Issue #258 Overlay Profile persistence may be admitted as a distinct repair
  line item where it affects recording target reliability.

This BP2 consumption note is durable feature-category direction for the accepted
Recording vision. It is not Workstream implementation approval, issue closeout,
PR authority, release authority, or a live branch-state ledger.

### Start/Stop Ownership

Options BP1 should present:

- Dashboard quick access only
- Recording Studio primary control with Dashboard quick access
- Recording Studio only

Recommendation: Recording Studio should own the full Start/Stop control surface,
while Dashboard quick access may provide a compact shortcut if the branch can
prove it stays clear and visually consistent.

Current branch repair direction accepted for the FAM-006 expected-red repair
package: move active Start/Stop out of the Dashboard Recording Card body and
into a compact Dashboard Quick Access section when implementation approval is
granted. Keep the Recording card as status, summary, target, and launch
visibility. Keep Recording Studio as the focused/full recording control and
status surface. Future settings may allow USER to enable or disable Quick
Access Start/Stop, but settings implementation remains future-gated.

### Studio Minimize Behavior

Options BP1 should present:

- taskbar window behavior
- tray-backed minimized behavior
- both, with USER setting later

Recommendation: tray-backed minimized behavior is promising because it supports
recording transparency without adding taskbar clutter, but it needs careful
proof before implementation.

### Log Folder Button Versus Log Viewer Studio

Options BP1 should present:

- keep a direct exported-log folder button as a bounded bridge
- replace the button with Log Viewer Studio access
- expose both only after explicit USER approval

Recommendation: long-term UX should use Log Viewer Studio. A direct folder
button is acceptable only as a clearly bounded bridge or validation aid.

### Native Versus Export Files

Options BP1 should present:

- native NDAI log only
- native NDAI log plus explicit export path
- automatic readable export

Recommendation: native NDAI log plus explicit export path. Automatic readable
export should be rejected unless USER later accepts that product flow.

Current branch repair direction accepted for the FAM-006 expected-red repair
package: Recording Studio may carry compact current/native-log tracking when it
is needed to make recording status trustworthy. Log Viewer Studio remains a
minimal native/export folder access shell for this branch. Full previous-log
selection, in-app log viewing, export customization, Native Log Loader
integration, tray controls, keybinds, and full settings remain future-gated.

## Proof Expectations

Branches consuming this feature vision should prove:

- returned-UTS visual repair contract: a USER-returned visual failure routes to
  bounded Workstream repair first; bounded Hardening checks may run during the
  repair, but formal H1, exact-launcher Live Validation, and UTS handoff must be
  renewed after the repair is visually green
- pre-Live Validation visual purpose conformance before formal LV/UTS: the
  window must first be visually adjudicated from recorded screenshots or video
  against its accepted purpose, the Project Vision, FAM-006 vision, this feature
  vision, and admitted UIREF/reference surfaces; only after that gate is clean
  may Codex use Live Validation to prove behavior and interaction
- element-group visual rows for every visible shared or purpose-specific group,
  including title/header, window controls, buttons, rows, body/background,
  dividers, copy, hover/focus/pressed/disabled/error/empty states, spacing,
  density, radius, glow/shadow/underglow, and resize/placement affordances
- PASS/REPAIR/BLOCKED/WAIVED_WITH_REASON disposition for every inspected
  element group; screenshot existence, helper PASS, runtime markers, logs, DOM
  markers, and code claims are not accepted as visual conformance by themselves
- shared action buttons use a single content-fit primitive: same height,
  typography, radius, border, glow/hover/focus/pressed/disabled behavior, and
  equal left/right inline gutters, with text inserted into the primitive rather
  than per-window stretched grid columns
- purpose-specific geometry affordances are part of visual conformance:
  Recording Studio is moveable with remembered position but not resizable in the
  current compact-controller contract; Log Viewer Studio is moveable and
  resizable; maximize remains future-gated unless later source truth admits the
  loaded-log graph inside Log Viewer Studio
- unique child / standalone-capable feature-studio resize taxonomy: Recording
  Studio and Log Viewer Studio are not exclusive attached Dashboard children;
  Recording Studio must expose no resize affordance in the current compact
  controller contract, while Log Viewer Studio must use independent edge resize
  behavior like a top-level window. A bottom-right attached-child corner grip is
  stale for these unique child feature-studio windows and must fail visual proof.
- Recording Studio uses one stateful Start/Stop control (`Start Recording` when
  ready and `Stop Recording` while active) plus a Log Viewer Studio route; two
  separate visible Start and Stop buttons are stale for the current Option C
  controller contract
- Dashboard Recording card visual-system inheritance with focused screenshots
- selected Overlay Profile target mirroring
- readiness, recording, saved, disabled, and error states
- no fake telemetry or hidden recording state
- native NDAI output save/readback when implementation is admitted
- no automatic CSV/Excel export in normal product flow
- exported-log folder behavior only when admitted
- Overlay Profile persistence when recording target reliability depends on it
- USER-facing UTS coverage for new or affected elements
- rollback path that restores pre-Recording UI/runtime behavior
- profile-specific log consistency when multiple Overlay Profiles have different
  monitor membership: Live Validation must prove selected profile identity,
  selected monitor set, recording target snapshot, generated native log
  contents, and consistency between the snapshot and log contents
- normal USER-path activation for Recording Studio and Log Viewer Studio remains
  mandatory for formal Live Validation: helper foreground, native direct-launch,
  seeded/sandbox, or callback proof is supporting evidence only and cannot clear
  the formal visible manual button path
- Pre-Live visual conformance may use sandbox or rendered proof before formal
  runtime Live Validation. It must be labeled as pre-Live/sandbox evidence,
  inspect the actual rendered element groups against the vision contract, and
  must not substitute for formal Live Validation through the normal runtime path.
- Recording Studio visual proof only after the normal visible activation path is
  proven for formal Live Validation; if activation is blocked, Studio UI visual
  validation is blocked or unproven rather than passed from helper-launched
  screenshots
- Log Viewer Studio visual-system inheritance against Project Vision, this
  family vision, and this feature vision; generic/plain UI cannot pass from
  screenshot existence or window-shell markers alone
- Recording Studio and Log Viewer Studio shared element groups must prove shared
  rendered primitive adoption, not merely reference-derived similarity. The
  focused proof set must include a side-by-side visual adjudication basis against
  the accepted reference surface or a direct rendered-primitive code path showing
  the same CSS/DOM visual source is consumed.
- user-visible native/export folder labels and paths that avoid exposing
  worktree, branch, developer, owner-only, FAM, or other internal implementation
  concepts unless source truth explicitly permits that client-facing model

Live Validation should validate new or affected elements. Previously accepted
elements need retesting only when the branch changes them or their dependencies.

## Branch Readiness Consumption Notes

BR2 packets for FAM-006 Recording should:

- load this file as `Feature Vision Context`
- present branch-lane options against this vision
- identify which deferred carryforward items apply
- explain why applicable items are grouped or left future-gated
- prove that branch scope is one coherent FAM-006 package rather than tiny
  disconnected branches
- reject issue-shaped branch identity unless USER selects it after seeing the
  feature-category options

## BP1 Context Notes

BP1 should create a USER-editable Branch Vision Review that decomposes Recording
by surface:

- Dashboard Recording access
- Recording card
- Recording Studio
- Log Viewer Studio
- tray visibility/control
- keybind Start/Stop
- native log model
- export model
- settings
- Overlay Profile target/persistence dependency

BP1 should ask decision-driving questions for each surface, give Codex's
recommendation, and clearly mark branch-package scope versus future-gated
direction. It must not present a shallow card/output-only vision as complete.

## BR2 Deferred Carryforward Applicability Guidance

BR2 option packets and BP2 branch-plan packets should include this matrix for
each candidate Recording lane or later option:

| Field | Required BR2 Answer |
| --- | --- |
| Option name | Name the candidate branch/package route. |
| Main feature/package objective | Name the concrete user-visible outcome. |
| Applicable deferred carryforward items | List deferred rows from this file that share the same FAM, surface, dependency, and proof path. |
| Reason each item applies | Explain the dependency or workflow connection. |
| Dependency trigger | Name what makes the deferred item relevant now. |
| Recommended grouping | Say whether the item belongs in the same coherent package. |
| Future-gated items | Name items left out and why. |
| Reason future-gated items remain deferred | Explain the risk, dependency, timing, proof, or USER-decision reason each item stays out. |
| Validation/proof expectations | Name focused screenshot, helper, UTS, live, readback, or rollback proof. |

If a deferred item satisfies the same dependency and proof path, Codex should
recommend grouping it into one coherent package unless package size, risk, or
USER direction requires a split.

Deferred carryforward is dynamic. Later BR2/BP2 options must surface only the
deferred items that apply to the selected option, explain why they apply, name
the dependency trigger, group or future-gate them deliberately, and state the
validation/proof expectations that would apply if USER selects that option.

## Deferred Feature Carryforward

| Deferred Item | Originating FAM | Originating Feature Vision | Origin Planning Event | Originating Gate | Feature Surface | Description | Dependency Trigger | Future Grouping Recommendation | Owner / Worktree | Validation / Proof Expectation | Durable Disposition | Fold-Down Receipt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Recording Studio full control surface | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Recording Studio | Compact non-child Studio for Start/Stop, target, status, close/minimize warning, and screen-space-efficient control. | Branch admits full recording control surface beyond Dashboard card summary. | Group with Dashboard Quick Access when the same package owns Start/Stop behavior. | FAM-006 / FAM-006 worktree lane | Focused Studio screenshots, Start/Stop proof, close/minimize behavior proof, UTS. | Current-Branch Repair Direction | Folded from planning packet, external reform candidate, and 2026-06-09 expected-red repair finalization into this feature vision. |
| Log Viewer Studio | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Log Viewer Studio | Non-child surface for native log access, exported-log access, previous-log selection, in-app viewing, and export entry. | Branch admits log review or export workflow. | Group with native/export log model; avoid burying it inside Dashboard card only. | FAM-006 / FAM-006 worktree lane | Focused Log Viewer screenshots, native/export folder proof, export/readability proof when export is admitted, UTS. | Minimal Shell Current / Full Viewer Future-Gated | Folded from planning packet, external reform candidate, and 2026-06-09 expected-red repair finalization into this feature vision. |
| Native NDAI log model | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Native logs | Recording saves first as NDAI-native product artifact for readback and future in-app review. | Branch writes or reads recording output. | Group with any Recording implementation that saves files. | FAM-006 / FAM-006 worktree lane | Native save/readback helper proof, no automatic readable export, UTS. | Folded Into Branch Vision | Existing branch evidence and USER feedback folded into durable feature direction. |
| Exported log model | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Exports | Readable CSV/Excel/JSON or other files are USER-requested exports, not default product saves. | Branch admits export/share or third-party-readable output. | Group with Log Viewer Studio export workflow. | FAM-006 / FAM-006 worktree lane | Export file readability proof in target software class, output-folder proof, UTS. | Future Package Candidate | Preserved as future-gated direction until export branch admission. |
| Tray recording visibility and control | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Tray | Dedicated recording visibility and optional Start/Stop / Studio / Log Viewer controls through tray. | Branch admits recording transparency or minimized Studio behavior. | Group with Recording Studio minimize behavior when the same package owns transparency. | FAM-006 / FAM-006 worktree lane | Real tray interaction proof, visible state proof, screenshot/video proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Keybind Start/Stop | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Keybind | USER-customizable Start/Stop keybind and setting for whether keybind-start opens Studio. | Branch admits keyboard recording control. | Group with settings and Recording Studio behavior. | FAM-006 / FAM-006 worktree lane | Keybind registration proof, conflict handling, setting proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Recording settings | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Settings | Compact categorized settings for start/stop behavior, Studio opening, Log Viewer opening, warnings, export defaults, and log locations. | Branch admits configurable recording behavior. | Group with the behavior being configured; do not create settings-only drift. | FAM-006 / FAM-006 worktree lane | Settings UI proof, persistence proof, reset/rollback proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Warning dismissal behavior | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Recording Studio warning | Local dismissal for close-while-recording warning, separate from global settings. | Branch admits close-while-recording warning. | Group with Recording Studio close behavior. | FAM-006 / FAM-006 worktree lane | Warning modal proof, dismissal persistence proof, recording continues/stops behavior proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Overlay Profile persistence dependency | FAM-006 | Recording | GitHub issue #258 and FAM-006 recording branch planning | BP2/BP3 amended planning evidence | Overlay Profiles | Recording target reliability depends on saved Overlay Profiles remaining present after restart. | Branch depends on saved Overlay Profile targets across sessions. | Group with Recording target reliability only when implementation touches profile persistence. | FAM-006 / FAM-006 worktree lane | Create/save/restart/reselect proof, recording target mirror proof, UTS. | Implemented Receipt | Issue #258 remains open until USER disposition, but branch evidence records implemented persistence proof. |
| Dashboard quick-access recording affordance | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Dashboard | Small obvious Dashboard Start/Stop affordance, possibly icon-led. | Branch admits Dashboard-level quick control. | Group with Recording Studio when quick access and full control share state. | FAM-006 / FAM-006 worktree lane | Focused Dashboard Quick Access screenshots, click/state proof, visual-system proof, UTS. | Current-Branch Repair Direction | Folded from USER planning feedback and 2026-06-09 expected-red repair finalization into this feature vision. |
| Native Log Loader relationship | FAM-006 | Recording | FAM-006 family vision and recording planning review | Family vision / planning evidence | Log viewing | Native Log Loader remains separate graph/log viewer unless later planning folds it into Log Viewer Studio. | Branch admits graph/log viewer capability. | Keep separate unless Source-Truth Placement Preflight proves same owner is needed. | FAM-006 / FAM-006 worktree lane | Viewer/readback proof if admitted; otherwise explicit future-gated proof. | Deferred Until Dependency | Preserved as a future dependency boundary. |

## Fold-Down History

This file was created after USER-approved Family Feature Vision planning/admission
for FAM-006 Recording. It folds durable direction from the planning packet,
external candidate, branch receipt, branch planning evidence, UTS handoff, and
issue #258 evidence into a feature-category vision owner.

It does not close issue #258, accept BP1, approve BP2/BP3, authorize Workstream
implementation, or move the branch toward PR Readiness by itself.
