# FAM-006 Recording Family Feature Vision

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

Recording Studio is the future compact Recording control surface.

Expected direction:

- non-child, exclusive window rather than a Dashboard child panel
- compact form factor that respects screen space
- Start/Stop control ownership when the branch admits full studio behavior
- selected Overlay Profile target display
- recording state display
- minimal proof/status copy
- close and minimize affordances

Close behavior needs explicit BP1/BP2 acceptance before implementation. The
preferred warning model is: closing the Studio while recording warns that the
recording continues until the USER stops it or Nexus Desktop AI exits. A local
dismissal preference may be allowed if a later branch admits it.

Minimize behavior also needs explicit acceptance. The durable design question is
whether Studio minimizes to the Windows taskbar or folds into a dedicated
Recording tray icon to avoid taskbar clutter.

### Log Viewer Studio

Log Viewer Studio is the future Recording log review and export surface.

Expected direction:

- non-child, exclusive window
- independent from the Dashboard child-window system
- access to the native NDAI log folder
- access to the exported-log folder
- previous-log selection after later planning
- in-app log viewing after later planning
- export flow after later planning

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

Exported log:

- USER-requested conversion
- supports selected readable formats only after an export branch admits them
- should be validated in a user-forward way so the exported file is easy to
  inspect in the target class of software
- belongs in an exported-log folder, separate from native NDAI log storage

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

### Start/Stop Ownership

Options BP1 should present:

- Dashboard quick access only
- Recording Studio primary control with Dashboard quick access
- Recording Studio only

Recommendation: Recording Studio should own the full Start/Stop control surface,
while Dashboard quick access may provide a compact shortcut if the branch can
prove it stays clear and visually consistent.

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

## Proof Expectations

Branches consuming this feature vision should prove:

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
| Recording Studio full control surface | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Recording Studio | Compact non-child Studio for Start/Stop, target, status, close/minimize warning, and screen-space-efficient control. | Branch admits full recording control surface beyond Dashboard card summary. | Group with Dashboard Recording controls when the same package owns Start/Stop behavior. | FAM-006 / FAM-006 worktree lane | Focused Studio screenshots, Start/Stop proof, close/minimize behavior proof, UTS. | Candidate | Folded from planning packet and external reform candidate into this feature vision. |
| Log Viewer Studio | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Log Viewer Studio | Non-child surface for native log access, exported-log access, previous-log selection, in-app viewing, and export entry. | Branch admits log review or export workflow. | Group with native/export log model; avoid burying it inside Dashboard card only. | FAM-006 / FAM-006 worktree lane | Focused Log Viewer screenshots, native/export folder proof, export/readability proof when export is admitted, UTS. | Candidate | Folded from planning packet and external reform candidate into this feature vision. |
| Native NDAI log model | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Native logs | Recording saves first as NDAI-native product artifact for readback and future in-app review. | Branch writes or reads recording output. | Group with any Recording implementation that saves files. | FAM-006 / FAM-006 worktree lane | Native save/readback helper proof, no automatic readable export, UTS. | Folded Into Branch Vision | Existing branch evidence and USER feedback folded into durable feature direction. |
| Exported log model | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Exports | Readable CSV/Excel/JSON or other files are USER-requested exports, not default product saves. | Branch admits export/share or third-party-readable output. | Group with Log Viewer Studio export workflow. | FAM-006 / FAM-006 worktree lane | Export file readability proof in target software class, output-folder proof, UTS. | Future Package Candidate | Preserved as future-gated direction until export branch admission. |
| Tray recording visibility and control | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Tray | Dedicated recording visibility and optional Start/Stop / Studio / Log Viewer controls through tray. | Branch admits recording transparency or minimized Studio behavior. | Group with Recording Studio minimize behavior when the same package owns transparency. | FAM-006 / FAM-006 worktree lane | Real tray interaction proof, visible state proof, screenshot/video proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Keybind Start/Stop | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Keybind | USER-customizable Start/Stop keybind and setting for whether keybind-start opens Studio. | Branch admits keyboard recording control. | Group with settings and Recording Studio behavior. | FAM-006 / FAM-006 worktree lane | Keybind registration proof, conflict handling, setting proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Recording settings | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Settings | Compact categorized settings for start/stop behavior, Studio opening, Log Viewer opening, warnings, export defaults, and log locations. | Branch admits configurable recording behavior. | Group with the behavior being configured; do not create settings-only drift. | FAM-006 / FAM-006 worktree lane | Settings UI proof, persistence proof, reset/rollback proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Warning dismissal behavior | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Recording Studio warning | Local dismissal for close-while-recording warning, separate from global settings. | Branch admits close-while-recording warning. | Group with Recording Studio close behavior. | FAM-006 / FAM-006 worktree lane | Warning modal proof, dismissal persistence proof, recording continues/stops behavior proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Overlay Profile persistence dependency | FAM-006 | Recording | GitHub issue #258 and FAM-006 recording branch planning | BP2/BP3 amended planning evidence | Overlay Profiles | Recording target reliability depends on saved Overlay Profiles remaining present after restart. | Branch depends on saved Overlay Profile targets across sessions. | Group with Recording target reliability only when implementation touches profile persistence. | FAM-006 / FAM-006 worktree lane | Create/save/restart/reselect proof, recording target mirror proof, UTS. | Implemented Receipt | Issue #258 remains open until USER disposition, but branch evidence records implemented persistence proof. |
| Dashboard quick-access recording affordance | FAM-006 | Recording | FAM-006 recording planning review, 2026-06-08 | Live Validation stop-loss planning | Dashboard | Small obvious Dashboard Start/Stop affordance, possibly icon-led. | Branch admits Dashboard-level quick control. | Group with Recording card when quick access and target/status share state. | FAM-006 / FAM-006 worktree lane | Focused Dashboard card screenshots, click/state proof, visual-system proof, UTS. | Candidate | Folded from USER planning feedback into this feature vision. |
| Native Log Loader relationship | FAM-006 | Recording | FAM-006 family vision and recording planning review | Family vision / planning evidence | Log viewing | Native Log Loader remains separate graph/log viewer unless later planning folds it into Log Viewer Studio. | Branch admits graph/log viewer capability. | Keep separate unless Source-Truth Placement Preflight proves same owner is needed. | FAM-006 / FAM-006 worktree lane | Viewer/readback proof if admitted; otherwise explicit future-gated proof. | Deferred Until Dependency | Preserved as a future dependency boundary. |

## Fold-Down History

This file was created after USER-approved Family Feature Vision planning/admission
for FAM-006 Recording. It folds durable direction from the planning packet,
external candidate, branch receipt, branch planning evidence, UTS handoff, and
issue #258 evidence into a feature-category vision owner.

It does not close issue #258, accept BP1, approve BP2/BP3, authorize Workstream
implementation, or move the branch toward PR Readiness by itself.
