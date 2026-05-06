# Nexus Feature Backlog

This file is the controlled registry for tracked work, deferred planning items, historical implemented items, and future promoted bug identities.

Rules:

- ideas must not be implemented immediately
- ideas must not silently expand current scope
- backlog identity remains controlled and approval-gated
- `Status` is the delivery or work field
- `Record State` is the canonical-record lifecycle field
- `Priority` is the primary backlog selection signal for open candidate work
- `Target Version` is not an open-backlog selection field and must not be used to rank, select, defer, or skip open backlog candidates
- open `Registry-only` and active `Promoted` entries should not carry `Target Version`; release target truth is assigned later through roadmap, workstream, PR Readiness, and Release Readiness governance when release-bearing work exists
- closed, released, implemented, or release-debt entries may preserve `Target Version` as historical release evidence
- if `Status` is `Deferred`, the entry must also state `Deferred Since:`, `Deferred Because:`, and `Selection / Unblock:` so next-workstream selection can evaluate it without guessing
- allowed `Record State` values are `Registry-only`, `Promoted`, and `Closed`
- if `Record State` is not `Registry-only`, `Canonical Workstream Doc` must exist
- backlog entries keep the short registry story, not the full execution story

Record-state meaning:

- `Registry-only` = tracked identity only; no canonical workstream execution record is required yet
- `Promoted` = canonical workstream doc required and used as the durable execution and traceability record while the lane is active
- `Closed` = canonical workstream doc remains stable historical lane truth after closure

Backlog-identity guardrails:

- feature backlog items default to user-facing feature families
- Codex must not create, split, promote, or select a backlog identity without explicit USER approval
- if that approval is absent, stop on `Backlog Addition User Approval Missing` and output the still-not-closed FAM list plus every not-complete package and slice; if the list is empty, stop on `Backlog Exhaustion User Decision Pending`
- a separate backlog identity for non-user-facing runtime, developer-tooling, docs/governance, or canon-only work requires explicit USER approval and a rationale that branch/workstream traceability is insufficient
- continuation, blocker-clearing, or validation follow-through on an existing feature family should stay inside that same backlog identity by default; do not mint a new backlog item unless the USER explicitly approves a backlog split or the work is materially a new user-facing feature family
- small single-seam runtime proofs, governance repairs, validation follow-through, and blocker-clearing traces are family evidence or branch/workstream history by default, not standalone release-version drivers
- canonical workstream docs and branch authority records own multi-slice, multi-branch, and repair-traceability history for one backlog identity; backlog IDs should not fragment that history by default
- the old `FB-###` namespace is historical-only after this one-time repair; new live backlog-family identities use `FAM-###`, starting at `FAM-001`, and Codex must not create or reuse a parseable `FB-###` backlog ID
- backlog-family registry sections must keep parseable `### [ID: FAM-XXX]` records only for true feature-family backlog entries; historical pass aliases, support/governance lanes, and old registry-only implemented records are trace tables, not backlog items
- entries within the live feature-family registry must be kept in ascending `FAM-XXX` order so the fresh namespace remains simple and conflict-free

Historical note:

- older implemented entries may preserve older Jarvis-era titles as historical identity
- those preserved titles are not current runtime-path claims
- older entries may also preserve earlier backlog-admission behavior that split docs/governance work or same-family continuation into separate backlog identities
- preserve that history for traceability, but do not treat it as the default backlog model going forward

## Promoted Canonical Workstreams

- `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
- `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md`
- `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md`
- `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md`

## Active Promoted Workstream

None.

FB-044 Boot-to-desktop handoff outcome refinement and FB-045 Active-session relaunch outcome refinement are Released / Closed historical proof through `v1.6.9-prebeta`; FB-046 Active-session relaunch reacquisition and settled re-entry proof is Released / Closed historical proof through `v1.6.10-prebeta`; FB-047 Active-session relaunch decline session-preservation proof is Released / Closed historical proof through `v1.6.11-prebeta`; FB-048 Active-session relaunch signal-failure and wait-timeout truth is Released / Closed historical proof through `v1.6.12-prebeta`; latest public prerelease truth is `v1.6.13-prebeta`; the backlog-family governance reform package, automation-catalog package, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof are released historical traceability in `v1.6.13-prebeta`; PR #108 is merged and released as FAM-004 historical proof after watcher-verified merge proof; PR #109 is merged historical FAM-003 legacy FB-027 family evidence for shutdown-hotkey confirmation and is not a standalone release-version driver.
Released baseline truth is aligned: FB-040 is released and closed in `v1.6.0-prebeta`, FB-031 is released and closed in `v1.6.1-prebeta`, FB-032 is released and closed in `v1.6.2-prebeta`, FB-004 is released and closed in `v1.6.3-prebeta`, FB-015 plus FB-029 are released and closed in `v1.6.4-prebeta`, FB-030 is released and closed in `v1.6.5-prebeta`, FB-005 is released and closed in `v1.6.6-prebeta`, FB-042 is released and closed in `v1.6.7-prebeta`, FB-043 is released and closed in `v1.6.8-prebeta`, FB-044 plus FB-045 are released and closed in `v1.6.9-prebeta`, FB-046 is released and closed in `v1.6.10-prebeta`, FB-047 is released and closed in `v1.6.11-prebeta`, FB-048 is released and closed in `v1.6.12-prebeta`, and the FAM-001 legacy FB-049 runtime proof plus FAM-004 legacy FB-030 runtime diagnostics proof are released historical traceability in `v1.6.13-prebeta`.
FB-039 is released and closed in `v1.5.0-prebeta`.
FB-038 remains released and closed in `v1.4.1-prebeta`.

## Current Branch Execution Posture

Released Historical Scope: FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth plus FAM-004 legacy FB-030 voice/audio runtime diagnostics proof plus merged governance/automation proof package plus PR #112 source-truth closeout / merge-target authority hardening proof plus PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta
Repo State: Active Branch.
Merged-Main Repo State: No Active Branch.
Latest Public Prerelease: v1.6.13-prebeta.
Latest Public Release Commit: faaf991d2579dd6478f78245d56956858cc2f59b.
Latest Public Prerelease Publication: https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.13-prebeta.
Latest Public Prerelease Title: Pre-Beta v1.6.13.
Release Debt: Clear after v1.6.13-prebeta publication, validation, and post-release canon closure.
Merged-main Current Active Workstream: None.
Current Active Workstream: FAM-006 Monitoring and HUD Product Surface Package Branch Readiness USER Vision Input artifact handoff created; Workstream product repair blocked pending USER artifact answers, digest, and planning revalidation.
Current Active Workstream Before Reform: None.
Current Execution Branch: feature/fam-006-monitoring-hud-product-surface.
Current Active Branch Authority Record: Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md.
Current Active Canonical Workstream Doc: None.
Historical Active Workstream Before Release: Automation Implementation.
Earlier Historical Active Workstream Before Release: FB-048 Active-session relaunch signal-failure and wait-timeout truth.
Historical Active Branch Before Release: feature/automation-planning.
Earlier Historical Active Branch Before Release: feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth.
Selected Next Workstream: FAM-006 Monitoring and HUD.
Selected Next Record State: Registry-only.
Selected Next Runtime Package Candidate: Monitoring and HUD Product Surface Package.
Selected Next Implementation Branch: feature/fam-006-monitoring-hud-product-surface.
Selected Next Status: USER-approved selected-next candidate matured into active FAM-006 package execution; product completion reopened after completion-truth drift review.
Runtime Package Admission: Admitted for PKG-006 during USER-approved Branch Readiness Stage 2; product completion is reopened.
Next Legal Runtime Step: USER completes `C:\Users\anden\OneDrive\Desktop\User Vision Input.txt`, then a later USER-approved Branch Readiness digest pass records the completed answers into repo source truth before Branch Readiness Stage 1-R3 revalidates planning; Workstream WS7 remains blocked until USER vision input, digest, and planning revalidation are complete or explicitly USER-waived.
Backlog Addition User Approval Missing: Cleared for USER-approved FAM-006 selected-next successor selection, Branch Readiness Stage 2 branch creation, and PKG-006 runtime package admission only; active for any other attempted new backlog item, backlog split, promotion beyond FAM-006, branch creation outside this carrier, or single-slice package waiver without explicit USER approval.
Historical Repair-Only Branch Handling: `feature/fb-046-post-merge-canon-sync` was a bounded repair-only post-merge canon-sync `feature/` branch and did not imply Branch Readiness admission or active branch truth for FB-046.
Historical Branch Readiness State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Current Branch Readiness State: Stage 2-R4 USER Vision Input artifact governance and handoff creation complete for PKG-006; prior Branch Readiness admission commit `8ae84cb784fc07dfe4f445359de4cf20a13552fa` remains historical admission evidence.
Current Workstream State: Blocked pending USER Vision Input answers, digest, and Branch Readiness planning revalidation - scaffold and boundary contracts exist, but product-visible HUD completion is not proven; SLC-016, SLC-026, SLC-027, SLC-028, and SLC-029 are reopened/in progress, while SLC-025 remains complete as local telemetry-boundary contract proof.
Current Hardening State: Reopened - prior H1 is scaffold/marker hardening evidence only, not product-complete proof.
Current Live Validation State: Blocked until Workstream product repair and Hardening re-complete.
Current PR Surface Owner: None; PR #109 merge/bot-review/watcher proof remains historical in `Docs/workstreams/FB-027_interaction_system_baseline.md`.
Current Branch Class: implementation.
Current Implementation Delta Class: runtime/user-facing.
Historical runtime-proof governance remains preserved: the PR watcher remains the only minute-scale heartbeat automation, `ACTIVE` alone is not treated as run proof, and any fallback helper must stay narrowed to the live PR and bounded to `PR Readiness`.
Historical Workstream State: Automation catalog implementation is merged historical branch proof after PR #99; FB-048 is Released / Closed in `v1.6.12-prebeta`; FB-047 is Released / Closed in `v1.6.11-prebeta`; FB-046 is Released / Closed in `v1.6.10-prebeta`; FB-044 and FB-045 remain Released / Closed historical proof in `v1.6.9-prebeta`.
Historical Hardening State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Historical Live Validation State: Complete on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`.
Canonical Current-State Rule: merge-target current-state owners stay merge-stable during merged-unreleased release-debt windows; live PR state, conflict/readiness details, review-resolution details, and blocker-clearing repair-lane narration live only in explicit historical PR sections of the canonical workstream and in operator output.
Release Execution State: `v1.6.13-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.13-prebeta on commit `faaf991d2579dd6478f78245d56956858cc2f59b`.
Release Target: None - no pending release target after `v1.6.13-prebeta` publication.
Release Floor: none - release execution is complete for the current approved prerelease.
Version Rationale: `v1.6.13-prebeta` published the approved patch-prerelease governance, automation, release-support, and bounded runtime-proof tranche; after publication and post-release closure, USER approved FAM-006 Branch Readiness Stage 2 to create the runtime branch and admit the Monitoring and HUD Product Surface Package.
Release Scope: released historical traceability for PR #110 governance repair, PR #111 release-packaging source-truth closeout, PR #112 post-merge release-support closeout/hardening, PR #113 PR #112 source-truth closeout / merge-target authority hardening, merged automation-catalog truth, `FAM-001` legacy `FB-049` runtime proof, and `FAM-004` legacy `FB-030` voice/audio runtime diagnostics proof.
Release Artifacts: Published tag `v1.6.13-prebeta`; published GitHub prerelease title `Pre-Beta v1.6.13`; Markdown release notes include a generated `## What's Changed` section plus `**Full Changelog**:`.
Post-Release Truth: the backlog-family governance reform, automation-catalog branch, `FAM-001` legacy `FB-049` runtime branch, `FAM-004` legacy `FB-030` runtime diagnostics branch, PR #112 closeout/hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof are released historical traceability; latest public prerelease is `v1.6.13-prebeta`; release debt is clear; USER-approved FAM-006 is active on `feature/fam-006-monitoring-hud-product-surface`, but product completion has been reopened because marker/screenshot capture did not prove a clearly visible HUD, and USER Vision Input answers plus digest remain pending.
Next-Branch Creation Gate: Cleared for `feature/fam-006-monitoring-hud-product-surface` only by USER-approved Branch Readiness Stage 2; any additional branch creation remains blocked.
Next Legal Phase: Branch Readiness.

## Backlog Governance Sync

Last Reviewed: 2026-04-27 during Backlog Family Governance Reform Phase 4 / Slice R4-S4 validator-helper and artifact index hardening.

Open-candidate priority review:

- FB-004 is released and closed in `v1.6.3-prebeta`; it is no longer an active or selected-next branch candidate.
- FB-015 is released and closed in `v1.6.4-prebeta`; it no longer owns release debt or active branch truth.
- FB-029 is released and closed in `v1.6.4-prebeta`; it no longer owns release debt or active branch truth.
- FAM-004 legacy FB-030 is released historical traceability in `v1.6.13-prebeta` after PR #108; its historical `v1.6.5-prebeta` planning proof remains preserved, and its runtime follow-through delivered bounded voice/audio availability and truthful diagnostics proof with WS1, H1, LV1, PR1, and PR2 complete.
- FAM-003 legacy FB-027 is a released baseline family anchor. PR #109 shutdown-hotkey confirmation is preserved as merged historical family evidence and aggregation material, not as an active backlog item or standalone release-version driver.
- FB-005 remains `Low` as historical workspace priority, but it is now Released / Closed in `v1.6.6-prebeta` and no longer owns release debt or selected-next truth.
- FB-042 is now Released / Closed in `v1.6.7-prebeta`; the released launch-path slice is preserved as the first historical proof under the runtime family anchor.
- FB-043 is now Released / Closed in `v1.6.8-prebeta`.
- FB-044 is now Released / Closed in `v1.6.9-prebeta`.
- FB-045 is now Released / Closed in `v1.6.9-prebeta`.
- FB-046 is now Released / Closed in `v1.6.10-prebeta`.
- FB-047 is now Released / Closed in `v1.6.11-prebeta`.
- FB-048 is Released / Closed in `v1.6.12-prebeta`; release debt is clear after publication, validation, and post-release canon closure.
- FAM-001 legacy FB-049 is historical complete after PR #107 merge; GitHub merge truth is valid, the same-thread watcher handoff failed, cleanup is proven, and the stale active-branch authority plus recurrence analysis is carried and repaired inside FAM-004 legacy FB-030 Branch Readiness.

Current-branch clarity: latest public prerelease is `v1.6.13-prebeta`; FB-044 and FB-045 are released and closed in `v1.6.9-prebeta`; FB-046 is released and closed in `v1.6.10-prebeta`; FB-047 is released and closed in `v1.6.11-prebeta`; FB-048 is released and closed in `v1.6.12-prebeta`; merged `main` repo state remains `No Active Branch`; the backlog-family governance reform branch, automation-catalog branch, FAM-001 legacy FB-049 runtime branch, FAM-004 legacy FB-030 runtime branch, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof are released historical traceability in `v1.6.13-prebeta`; FAM-003 legacy FB-027 is a released baseline family anchor with PR #109 preserved as aggregation evidence; and USER-approved FAM-006 selected-next truth has matured into active PKG-006 package execution on `feature/fam-006-monitoring-hud-product-surface`, with product completion reopened after scaffold/marker proof failed to prove a clearly visible HUD.

## Registry Items

### User-Facing Feature Families

Selectable user-facing feature-family records now use the fresh `FAM-###` namespace in ascending order from `FAM-001`. Legacy `FB-###` IDs are preserved only as historical trace fields, former-ID tables, workstream filenames, branch filenames, and release/PR evidence.

Canonical Identity Model: `FAM` = broad long-lived product family; `Package` = bulk branch/release package under one family; `Slice` = traceable deliverable area inside a package; `Seam` = execution or validation checkpoint; `PR` = merge/review evidence only; legacy global `FB` = historical trace only.
Branch Scope Standard: branches must package multiple related admitted slices under exactly one broad family by default. A package with exactly one admitted slice is blocked by `Single-Slice Package User Approval Missing` unless `Single-Slice Package User Approval: Granted` is recorded with explicit USER approval.
Package Completion Standard: Workstream continues through every admitted package slice until `Package Completion State: Complete`, `Released Baseline / Open`, `Blocked`, or `Deferred` is truthfully recorded before Hardening admission.
Admitted Slice Counting Rule: only rows with `Admission State` equal to `Admitted` count toward a package's admitted-slice total. Rows represented as `Admission State: Admitted` are the only rows that count; `Historical Evidence`, `Merged Evidence`, `Future Placeholder`, `Deferred Placeholder`, and other non-admitted trace rows preserve context but cannot satisfy the multi-slice package rule.
Concrete Admitted Slice Rule: an admitted slice must have a concrete scoped deliverable, `Package ID`, `FAM ID`, `Slice Status`, `Completion State`, and `Seam Trace`; vague pending/future placeholder rows cannot be marked admitted.
Package Completion Guard: `Package Completion State: Complete` is blocked while any admitted slice remains incomplete, and completing one admitted slice cannot authorize stopping while another admitted slice remains incomplete.
Named Package Blockers: `Single-Slice Package User Approval Missing` and `Package Completion Unproven`.
USER Blocker Output Standard: `Backlog Addition User Approval Missing` must list every not-closed FAM and every not-complete package or slice before stopping.
PR Evidence Standard: PR numbers are evidence only and must not become backlog identities, package identities, release-version drivers, or selected-next successors.
Element Coverage Standard: Element Coverage is a non-identity checklist for FAM/package review only. Coverage categories are user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact. Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers.

| FAM ID | Broad Product Family | Family Status | Package Posture | Legacy Trace Coverage |
| --- | --- | --- | --- | --- |
| `FAM-001` | Boot Interface | Open / released-baseline aggregation | `PKG-001` released baseline / open | `FB-042`, `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`, `FB-049`, PR #86-#107 |
| `FAM-002` | Desktop Interface | Open / pending user-facing follow-through | `PKG-002` released baseline / open | `FB-031`, UI/UX planning release evidence |
| `FAM-003` | Interaction and Actions | Open / aggregation-held | `PKG-003` released baseline / open | `FB-027`, `FB-036`, `FB-037`, `FB-038`, `FB-041`, PR #109 |
| `FAM-004` | Voice and Audio | Open / released-baseline aggregation | `PKG-004` released baseline / open | `FB-030`, PR #108, `v1.6.5-prebeta`, `v1.6.13-prebeta` |
| `FAM-005` | External Integrations | Pending implementation | `PKG-005` released baseline / open | `FB-039`, Stream Deck and external trigger gap |
| `FAM-006` | Monitoring and HUD | Workstream active / runtime package admitted | `PKG-006` admitted / in progress | `FB-040`, HUD surface gap |
| `FAM-007` | Local AI and Capability Packs | Pending architecture/package | `PKG-007` pending | `Docs/orin_vision.md` local-AI and capability-pack vision |
| `FAM-008` | Packaging and Install Experience | Pending architecture/package | `PKG-008` pending | `Docs/orin_vision.md`, modular install and GPU-aware architecture gap |
| `FAM-009` | Workspace and Data | Open / deferred follow-through | `PKG-009` released baseline / open | `FB-005`, `FB-020`, `FB-026`, `FB-028`, workspace/data trace |
| `FAM-010` | Safety and Privacy | Pending architecture/package | `PKG-010` pending | `Docs/orin_vision.md`, local execution, privacy, and safety boundaries |

### [ID: FAM-001] Boot Interface

Status: Open / released-baseline aggregation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Startup, boot, desktop entrypoint, single-instance ownership, launch handoff, relaunch semantics, lifecycle transition proof, and boot-to-runtime trust boundaries.
Package Policy: Branchable work must be a bulk boot-interface package with multiple related admitted slices by default.
Known Pending Gaps: Boot-family proof remains released-baseline open until future USER-approved package work closes lifecycle follow-through beyond the historical launch/relaunch baselines.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-001` | `FAM-001` | Startup lifecycle and relaunch truth baseline | Released baseline / open | Released Baseline / Open | `feature/fb-042-desktop-entrypoint-runtime-refinement`; `feature/fb-049-runtime-branch-readiness`; `v1.6.7-prebeta` through `v1.6.13-prebeta` | `FB-042`, `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`, `FB-049`, PR #86-#107 |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-001` | `PKG-001` | `FAM-001` | Desktop entrypoint and launch-path baseline | Historical Evidence | Released | Complete | `FB-042`; Branch Readiness, Workstream, Hardening, Live Validation, PR, Release |
| `SLC-002` | `PKG-001` | `FAM-001` | Top-level entrypoint and boot handoff truth | Historical Evidence | Released | Complete | `FB-043`, `FB-044`; Branch Readiness through Release |
| `SLC-003` | `PKG-001` | `FAM-001` | Active-session relaunch success, decline, failure, and timeout truth | Historical Evidence | Released | Complete | `FB-045`, `FB-046`, `FB-047`, `FB-048`; Branch Readiness through Release |
| `SLC-004` | `PKG-001` | `FAM-001` | Pre-settled incoming-launch conflict truth | Historical Evidence | Released | Complete | `FB-049`; WS1, H1, LV1, PR #107, `v1.6.13-prebeta` |

Summary: Boot Interface owns the long-lived startup and relaunch product surface; old `FB-042` through `FB-049` remain historical proof slices under this family, not reusable live backlog IDs.

### [ID: FAM-002] Desktop Interface

Status: Open / pending user-facing follow-through
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Nexus desktop shell, visual language, operator UI, settings presentation, user-facing desktop interaction surfaces, and coherent UI/UX implementation packages.
Package Policy: Branchable desktop-interface work must package multiple admitted UI/UX slices by default and must not treat one planning pass as a closed family.
Known Pending Gaps: Nexus-era user-facing HUD/shell presentation, settings and desktop UX implementation remain pending after the historical planning release.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-002` | `FAM-002` | Desktop shell and UI/UX baseline | Released baseline / open | Released Baseline / Open | `feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning`; `v1.6.1-prebeta` | `FB-031`, UI/UX planning release evidence |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-005` | `PKG-002` | `FAM-002` | Nexus UI/UX source-map and visual-language baseline | Historical Evidence | Released | Complete | `FB-031`; Branch Readiness through Release |
| `SLC-006` | `PKG-002` | `FAM-002` | User-facing desktop shell implementation follow-through | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Desktop Interface keeps the UI/UX planning baseline as historical proof while leaving the real user-facing desktop work open.

### [ID: FAM-003] Interaction and Actions

Status: Open / aggregation-held
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Family Scope: Typed-first interaction, saved actions, callable groups, built-in actions, tray quick tasks, hotkeys, shared action routing, confirmation flows, and reusable action execution boundaries.
Package Policy: Branchable interaction work must be a family package with multiple admitted slices by default; small runtime proofs aggregate unless USER approves a release driver.
Known Pending Gaps: Shared action authoring, built-in/catalog expansion, tray quick-task follow-through, and shutdown confirmation evidence remain aggregation material until a USER-approved package is admitted.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-003` | `FAM-003` | Shared interaction and action model baseline | Released baseline / open | Released Baseline / Open | `Docs/workstreams/FB-027_interaction_system_baseline.md`; `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `FB-027`, `FB-036`, `FB-037`, `FB-038`, `FB-041`, PR #109 |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-007` | `PKG-003` | `FAM-003` | Typed-first interaction and saved-action baseline | Historical Evidence | Released | Complete | `FB-027`, `FB-036`; historical Branch Readiness through Release |
| `SLC-008` | `PKG-003` | `FAM-003` | Deterministic callable groups, built-ins, settings, and tray quick tasks | Historical Evidence | Released baseline / open | Released Baseline / Open | `FB-037`, `FB-038`, `FB-041`; historical Branch Readiness through Release |
| `SLC-009` | `PKG-003` | `FAM-003` | Shutdown-hotkey confirmation aggregation proof | Merged Evidence | Merged historical evidence | Merged Historical Evidence | PR #109; WS1, H1, LV1, PR Readiness |

Summary: Interaction and Actions replaces the accidental small-branch backlog identity pattern; PR #109 stays trace evidence inside a broader family package.

### [ID: FAM-004] Voice and Audio

Status: Open / released-baseline aggregation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Latest Released Runtime Proof Version: v1.6.13-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md
Family Scope: ORIN voice output, error voice, quiet/bypass behavior, audio availability diagnostics, persona-safe voice claims, and future cross-family voice integration.
Package Policy: Branchable voice/audio work must package multiple admitted runtime or integration slices by default; one diagnostic seam alone is aggregation evidence unless USER approves otherwise.
Known Pending Gaps: Runtime diagnostics proof is released historical traceability; future voice integration across interaction, desktop, and safety/privacy families remains pending.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Released Historical Scope: FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth plus FAM-004 legacy FB-030 voice/audio runtime diagnostics proof plus merged governance/automation proof package plus PR #112 source-truth closeout / merge-target authority hardening proof plus PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta
Latest Public Prerelease: v1.6.13-prebeta
Release Title: Pre-Beta v1.6.13
Release Target: None - released in v1.6.13-prebeta.
Release Floor: none - release execution is complete.
Version Rationale: The voice/audio runtime diagnostics proof added bounded truthfulness for availability states without opening a standalone new family or release-version driver.
Release Scope: released governance reform, automation catalog proof, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof.
Release Artifacts: Published tag `v1.6.13-prebeta`; published GitHub prerelease title `Pre-Beta v1.6.13`; release notes include generated `What's Changed` and `Full Changelog` sections.
Post-Release Truth: merged governance reform, automation catalog, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening, and PR #113 source-truth closeout / merge-target authority hardening are released historical traceability; release debt is clear; and the later runtime package has USER-approved FAM-006 scaffold/boundary proof on `feature/fam-006-monitoring-hud-product-surface`; product completion is reopened and Workstream WS7 is blocked pending USER Vision Input answers, digest, and Branch Readiness planning revalidation.
Selected Next Workstream: FAM-006 Monitoring and HUD.
Next-Branch Creation Gate: Cleared for `feature/fam-006-monitoring-hud-product-surface` only by USER-approved Branch Readiness Stage 2.
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-004` | `FAM-004` | Voice/audio truth and integration package | Released baseline / open | Released Baseline / Open | `feature/fb-030-voice-audio-runtime-branch-readiness`; `v1.6.13-prebeta` | `FB-030`, PR #108, `v1.6.5-prebeta` planning release |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-010` | `PKG-004` | `FAM-004` | Voice/audio direction and planning baseline | Historical Evidence | Released | Complete | `FB-030`; `v1.6.5-prebeta` |
| `SLC-011` | `PKG-004` | `FAM-004` | Truthful voice/audio runtime diagnostics | Historical Evidence | Released | Complete | `FB-030`; WS1, H1, LV1, PR #108, `v1.6.13-prebeta` |
| `SLC-012` | `PKG-004` | `FAM-004` | Cross-family voice integration package follow-through | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Voice and Audio carries legacy `FB-030` proof as package evidence while keeping the broader voice integration family open.

### [ID: FAM-005] External Integrations

Status: Pending implementation
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Stream Deck, external trigger intake, plugin lifecycle, installed integration points, trusted invocation boundaries, and external action ownership.
Package Policy: Branchable external-integration work must package multiple admitted implementation and validation slices by default.
Known Pending Gaps: Stream Deck and external integration implementation remains pending after the historical architecture-only trigger-intake release.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-005` | `FAM-005` | External trigger and plugin implementation package | Released baseline / open | Released Baseline / Open | `feature/fb-039-external-trigger-plugin-integration-architecture`; `v1.5.0-prebeta` | `FB-039`, Stream Deck/external integration gap |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-013` | `PKG-005` | `FAM-005` | External trigger architecture and lifecycle baseline | Historical Evidence | Released | Complete | `FB-039`; Branch Readiness through Release |
| `SLC-014` | `PKG-005` | `FAM-005` | Stream Deck and installed integration implementation | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: External Integrations keeps the trigger architecture release as proof while leaving implementation work pending.

### [ID: FAM-006] Monitoring and HUD

Status: Active
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Next Workstream: Workstream Complete
Selected Next Workstream: FAM-006 Monitoring and HUD - active package execution / product completion reopened.
Selected Next Runtime Package Candidate: Monitoring and HUD Product Surface Package
Selected Next Status: USER-approved selected-next candidate matured into active package execution; product completion reopened after Branch Readiness Stage 2-R1 rebaseline
Selected Next Implementation Branch: feature/fam-006-monitoring-hud-product-surface
Branch Creation Status: Created in Branch Readiness Stage 2 from updated main at `3c68cd881a9f6bf447f09ac0949d556e97bce4f4`
Runtime Package Admission: Admitted for `PKG-006`
Active Branch Authority Record: Docs/branch_records/feature_fam_006_monitoring_hud_product_surface.md
Next Legal Runtime Step: USER completes `C:\Users\anden\OneDrive\Desktop\User Vision Input.txt`, then a later USER-approved digest pass records completed answers into repo source truth before Branch Readiness Stage 1-R3 planning sufficiency revalidation; Workstream WS7 and Live Validation remain blocked until product planning, product repair, and Hardening re-complete.
Minimal Scope: admitted runtime package for HUD visual/user-facing surface, runtime telemetry source/adapters, desktop placement and renderer ownership, settings or user controls visibility, fail-safe/no-data/degraded-status behavior, and validation/live desktop proof; optional voice/status integration remains deferred unless it is later proven to be narrow HUD-status copy inside FAM-006.
Family Scope: Monitoring surfaces, CPU/GPU thermals, performance telemetry, HUD/overlay presentation, trust-safety display rules, and plugin-fed runtime telemetry.
Package Policy: Branchable monitoring/HUD work must package source, display, and validation slices by default.
Known Pending Gaps: clearly visible HUD panel/card, readable placement, intentional visual hierarchy, useful user-facing status information, visual screenshot proof, and User Test Summary acceptance remain pending after scaffold completion.
Package Admission State: Admitted
Admitted Slice Count: 6
Package Completion State: In Progress - product completion reopened
Single-Slice Package User Approval: Not required - `PKG-006` has six concrete admitted slices and no single-slice waiver is granted.
Single-Seam Workstream Waiver: None - bounded means one active seam at a time, not one-seam Workstream authority; PKG-006 must continue through admitted slices unless a named blocker, future dependency, or explicit USER waiver is recorded.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-006` | `FAM-006` | Monitoring and HUD product-surface package | USER Vision Input answers/digest pending; Branch Readiness planning revalidation pending / Workstream product repair blocked | In Progress | `feature/fam-006-monitoring-hud-product-surface`; historical baseline `feature/fb-040-monitoring-thermals-performance-hud-surface`; `v1.6.0-prebeta` | `FB-040`, HUD user-facing surface gap |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-015` | `PKG-006` | `FAM-006` | Monitoring and thermal architecture baseline | Historical Evidence | Released | Complete | `FB-040`; Branch Readiness through Release |
| `SLC-016` | `PKG-006` | `FAM-006` | HUD visual and user-facing monitoring surface | Admitted | Reopened | In Progress - scaffold exists, visible product proof unproven | `BR-S2-S1`; `WS1`; `dev/orin_monitoring_hud_surface_validation.py`; `BR-S2-R1` |
| `SLC-025` | `PKG-006` | `FAM-006` | Runtime telemetry source and adapter boundary | Admitted | Green | Complete - local boundary contract only | `BR-S2-S2`; `WS2`; `desktop/monitoring_hud_telemetry.py`; `dev/orin_monitoring_hud_surface_validation.py` |
| `SLC-026` | `PKG-006` | `FAM-006` | Desktop placement and renderer ownership | Admitted | Reopened | In Progress - placement contract exists, readable visible placement proof unproven | `BR-S2-S3`; `WS3`; `desktop/monitoring_hud_placement.py`; `dev/orin_monitoring_hud_surface_validation.py`; `BR-S2-R1` |
| `SLC-027` | `PKG-006` | `FAM-006` | Settings and user controls visibility | Admitted | Reopened | In Progress - read-only copy exists, useful user-control visibility path unproven | `BR-S2-S4`; `WS4`; `desktop/monitoring_hud_controls.py`; `dev/orin_monitoring_hud_surface_validation.py`; `BR-S2-R1` |
| `SLC-028` | `PKG-006` | `FAM-006` | Fail-safe, no-data, and degraded-status behavior | Admitted | Reopened | In Progress - status contract exists, user-facing behavior proof unproven | `BR-S2-S5`; `WS5`; `desktop/monitoring_hud_status.py`; `dev/orin_monitoring_hud_surface_validation.py`; `BR-S2-R1` |
| `SLC-029` | `PKG-006` | `FAM-006` | Validation and live desktop proof | Admitted | Reopened | In Progress - marker/screenshot capture exists, human-visible HUD proof insufficient | `BR-S2-S6`; `WS6`; `dev/orin_monitoring_hud_live_validation.ps1`; `dev/logs/fam_006_monitoring_hud_live_validation/20260506_100320/manifest.json`; `BR-S2-R1` |
| `SLC-030` | `PKG-006` | `FAM-006` | Optional voice or spoken status integration | Deferred Placeholder | Deferred pending cross-family approval | Not Admitted | Future USER widening decision required if voice/audio behavior is needed |

Admitted Slice Shape: HUD visual/user-facing surface; runtime telemetry source/adapters; desktop placement / renderer ownership; settings or user controls visibility; fail-safe / no-data / degraded-status behavior; validation / live desktop proof.
Deferred/Future Slice Shape: optional voice/status integration is not admitted because spoken/audio behavior, voice integration, persona voice, or FAM-004 cross-family widening requires later explicit USER approval.
Element Coverage Review: user-facing surface, runtime/backend behavior, settings/configuration, fail-safe/recovery, voice/audio integration as deferred coverage only, monitoring/HUD/observability, validation/live-test requirements, release/documentation impact, security/privacy posture, external integration, local AI/capability-pack impact, and packaging/install impact are planning coverage only and do not count as admitted slices.
Summary: Monitoring and HUD scaffold/boundary work is credited, but package completion is reopened. The branch remains active for USER Vision Input artifact completion, digest, and Branch Readiness planning revalidation before Workstream WS7 product visibility and acceptance repair; no PR has been created and no release work is authorized.

### [ID: FAM-007] Local AI and Capability Packs

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Local AI execution posture, capability-pack boundaries, model/tool capability distribution, local-vs-external runtime choices, and capability governance.
Package Policy: Branchable local-AI work must package capability boundary, install/runtime, validation, and documentation slices by default.
Known Pending Gaps: Local AI and capability-pack architecture remains pending as repo-supported project vision and has no USER-approved implementation package yet.
Package Admission State: Pending USER approval / no active package admission
Admitted Slice Count: 0
Package Completion State: Pending
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-007` | `FAM-007` | Local AI and capability-pack architecture package | Pending | Pending | `Docs/orin_vision.md` project vision trace | No legacy FB; repo vision trace only |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-017` | `PKG-007` | `FAM-007` | Local AI runtime boundary and capability-pack source map | Future Placeholder | Pending USER-approved package | Not Admitted | Future Branch Readiness required |
| `SLC-018` | `PKG-007` | `FAM-007` | Capability-pack install, validation, and governance follow-through | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Local AI and Capability Packs starts fresh as a broad family without reusing old `FB` numbering.

### [ID: FAM-008] Packaging and Install Experience

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Installer, modular setup, GPU-aware runtime selection, dependency packaging, desktop-shortcut installation, release packaging ergonomics, and operator install/upgrade experience.
Package Policy: Branchable packaging/install work must package installer architecture, runtime detection, user copy, and validation slices by default.
Known Pending Gaps: Modular install and GPU-aware architecture remain pending and must not be collapsed into a small single-seam branch.
Package Admission State: Pending USER approval / no active package admission
Admitted Slice Count: 0
Package Completion State: Pending
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-008` | `FAM-008` | Modular install and GPU-aware runtime package | Pending | Pending | `Docs/orin_vision.md`; `Docs/architecture.md` | No legacy FB; repo vision trace only |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-019` | `PKG-008` | `FAM-008` | Modular install architecture and desktop installation path | Future Placeholder | Pending USER-approved package | Not Admitted | Future Branch Readiness required |
| `SLC-020` | `PKG-008` | `FAM-008` | GPU-aware runtime/dependency selection and validation | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Packaging and Install Experience keeps installer and GPU-aware runtime work as a broad family package, not a one-off branch.

### [ID: FAM-009] Workspace and Data

Status: Open / deferred follow-through
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Low
Family Scope: Workspace paths, data organization, durable state, conversation/project storage, source-of-truth migration, and folder/data hygiene.
Package Policy: Branchable workspace/data work must package storage, migration, validation, and UX follow-through slices by default.
Known Pending Gaps: Workspace and data follow-through remains open even though earlier folder-organization and migration slices are released historical proof.
Deferred Since: 2026-05-04 one-time backlog governance repair.
Deferred Because: Workspace/data follow-through requires explicit USER-approved package admission under the broad FAM model.
Selection / Unblock: USER approval for a FAM-009 package with multiple workspace/data slices, or an explicit USER-approved deferral change.
Package Admission State: Historical baseline / no active package admission
Admitted Slice Count: 0
Package Completion State: Released Baseline / Open
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-009` | `FAM-009` | Workspace and data truth package | Released baseline / open | Released Baseline / Open | `v1.6.6-prebeta` and historical migration/support trace | `FB-005`, `FB-020`, `FB-026`, `FB-028`, source-of-truth migration evidence |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-021` | `PKG-009` | `FAM-009` | Workspace/folder organization and migration baseline | Historical Evidence | Released | Complete | `FB-005`, `FB-020`, `FB-026`, `FB-028`; historical workstream/release trace |
| `SLC-022` | `PKG-009` | `FAM-009` | Durable workspace/data UX and follow-through | Deferred Placeholder | Deferred USER-approved package | Deferred | Future package seam required |

Summary: Workspace and Data keeps old data/workspace IDs as trace while remaining open for broader data-product follow-through.

### [ID: FAM-010] Safety and Privacy

Status: Pending architecture/package
Record State: Registry-only
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Family Scope: Privacy posture, local execution boundaries, trust/safety copy, consentful integrations, safe automation, model/tool data handling, and license/privacy guardrails.
Package Policy: Branchable safety/privacy work must package policy, runtime behavior, validation, and user-facing copy slices by default.
Known Pending Gaps: Safety/privacy is repo-supported by local-execution and trust/safety vision but has no dedicated USER-approved implementation package yet.
Package Admission State: Pending USER approval / no active package admission
Admitted Slice Count: 0
Package Completion State: Pending
Single-Slice Package User Approval: Not required - no active single-slice package is admitted; future package admission must have multiple concrete admitted slices or USER waiver.

Package Trace:

| Package ID | FAM ID | Package Name | Package Status | Package Completion State | Branch / Release Trace | Legacy FB / PR Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `PKG-010` | `FAM-010` | Safety, privacy, and local-execution package | Pending | Pending | `Docs/orin_vision.md`; `Docs/ownership_ip_plan.md`; governance trace | No legacy FB; repo vision trace only |

Slice Trace:

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Seam Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-023` | `PKG-010` | `FAM-010` | Privacy/local-execution boundary and user-facing claims | Future Placeholder | Pending USER-approved package | Not Admitted | Future Branch Readiness required |
| `SLC-024` | `PKG-010` | `FAM-010` | Safe automation, consent, and integration guardrails | Future Placeholder | Pending USER-approved package | Not Admitted | Future package seam required |

Summary: Safety and Privacy is a broad product family only; it is not a reused legacy `FB` lane.

### Legacy One-To-One FAM Mapping Trace

The following entries preserve the earlier one-time repair mapping as historical analysis only. They are not parseable live family records, not branchable identities, and not selected-next candidates under the broad FAM -> Package -> Slice -> Seam model.

#### [Legacy Mapping: FAM-001] Active-session pre-settled incoming-launch conflict truth

Legacy FB ID: FB-049
Status: Released
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Selection / Unblock: Implemented complete. `feature/fb-049-runtime-branch-readiness` delivered the pre-settled incoming-launch conflict truthful-exit proof, and PR #107 merged into `main` at `2026-05-01T22:17:44Z`.
Next Workstream: Historical complete
Branch Creation Gate: Historical complete; BR1 cleared the carried PR #106 stale active-branch blocker before implementation started.
Branch: feature/fb-049-runtime-branch-readiness
Branch Readiness: Historical complete. BR1 cleared stale active-branch authority from the merged PR #106 closeout branch before runtime implementation started.
Workstream: Historical complete. WS1 implemented and validated the pre-settled incoming-launch conflict truthful-exit proof.
Hardening: Historical complete. `Hardening H1 - Pre-Settled Incoming-Launch Conflict Validation` validated the WS1 runtime proof.
Live Validation: Green. `Live Validation LV1 - Pre-Settled Incoming-Launch Conflict Live Validation` passed with real desktop shortcut evidence, closest available live-equivalent pre-settled conflict proof, and a User Test Summary waiver recorded in the branch authority record.
PR Readiness: Historical complete with failure classification. PR #107 merged, GitHub merge truth is valid, and `PR Watcher Merge Handoff Missing` is preserved because `pr107-same-thread-merge-watch` did not emit the required same-thread merged handoff before cleanup.
Minimal Scope: Prove and refine the pre-settled incoming-launch conflict lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so startup-phase ownership stays explicit, incoming launches exit truthfully before authoritative settled is reached, and settled-session relaunch semantics are not falsely claimed.
Historical Merge Truth: PR #107 merged into `main` at `2026-05-01T22:17:44Z`; merge commit `22dfb15e554472220b9621b01439286b3afe1dda`; head SHA `fc00346b111158c6f57d976fef7a215a940027c1`.
Watcher Failure Truth: same-thread watcher handoff missing; watcher cleanup proven; carried into FAM-004 legacy FB-030 Branch Readiness as `PR Watcher Merge Handoff Missing` plus `Blocker Recurrence Analysis Required`.
Release Stage: Released
Latest Released Runtime Proof Version: v1.6.13-prebeta
Release Title: Pre-Beta v1.6.13
Latest Public Prerelease: v1.6.13-prebeta
Release Readiness: Released historical traceability in `v1.6.13-prebeta`.
Release Execution: `v1.6.13-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.13-prebeta on commit `faaf991d2579dd6478f78245d56956858cc2f59b`.
Summary: Make startup-phase incoming-launch conflicts as truthful as settled-session relaunch conflicts.
Why it matters: Users should get an explicit, proven outcome when a second launch collides with an already-owning startup-phase session before the desktop has reached authoritative settled state.

#### [Legacy Mapping: FAM-002] Desktop startup runtime family anchor

Legacy FB ID: FB-042
Status: Released (v1.6.7-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Low
Release Stage: Released
Target Version: v1.6.7-prebeta
Release Title: Pre-Beta v1.6.7
Selection / Unblock: Implemented for the first bounded runtime/user-facing slice. `feature/fb-042-desktop-entrypoint-runtime-refinement` delivered WS-1 desktop shortcut launch-path runtime refinement, the branch merged through PR #86, PR #87 cleared the final release-debt marker drift, and `v1.6.7-prebeta` is now published and validated.
Branch: feature/fb-042-desktop-entrypoint-runtime-refinement
Canonical Workstream Doc: Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md
Lifetime Dossier Doc: Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md
Lifetime Dossier State: Structured shell with partial historical pass migration. Phase 4 / Slice R4-S1 introduced the dossier shell, Phase 4 / Slice R4-S3 added pass index and slice/seam ledger templates, Phase 4 / Slice R4-S4 added validator/helper and artifact index templates, Phase 4 / Slice R4-S5 validated dossier stability, Phase 5 / Slice R5-S1 converted FB-043 through FB-048 into explicit historical pass records while populating the dossier pass index plus slice/seam ledger summary rows, and Phase 5 / Slice R5-S3 converted the preserved corresponding branch-readiness records; validator/helper and artifact migration remain pending.
Branch Readiness: Complete. Planning/framing now happens before Workstream, and the admitted WS-1 slice is recorded with owned paths, non-goals, validation coverage, rollback limits, and user-facing shortcut contract in the canonical workstream doc.
Workstream: Released. WS-1 desktop shortcut launch-path runtime refinement is complete and validated on the real `launch_orin_desktop.vbs` -> `desktop/orin_desktop_launcher.pyw` -> `desktop/orin_desktop_main.py` path, H-1 hardening is complete, LV-1 is complete, and release publication is complete.
Branch Meaning: Historical source-branch execution owned the real desktop entrypoint/runtime launch path, and that bounded runtime slice now serves as the first released historical proof under this runtime family anchor.
Release Target: v1.6.7-prebeta
Release Floor: patch prerelease
Version Rationale: FB-042 delivers a bounded runtime/user-facing launch-path reliability and startup-error-handling refinement on the existing desktop entrypoint path, but it does not introduce a new product lane, broader runtime family, or materially expanded capability beyond the shipped launch chain.
Release Scope: WS-1 launch-path fallback hardening in `launch_orin_desktop.vbs`, direct user-facing startup failure dialog handling when no usable windowed Python launcher exists, launch-chain validator expansion across default and forced-fallback VBS paths, H-1 fallback-contract correction for `py -0p` / Python 3 launcher proof, real desktop shortcut validation evidence, PR package history, and merged-unreleased release-debt truth for the bounded FB-042 runtime slice only.
Release Artifacts: Tag v1.6.7-prebeta; release title Pre-Beta v1.6.7; rich Markdown release notes summarize the bounded FB-042 desktop launch-path runtime refinement, fallback hardening, real shortcut evidence, and selected-next top-level entrypoint successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Current Active Workstream: None
Promotion Gate: Historical proof complete. `v1.6.7-prebeta` was published and validated, updated `main` was revalidated, and FB-043 then completed its promoted runtime workstream on `feature/fb-043-top-level-entrypoint-handoff-refinement`.
Minimal Scope: Execute only WS-1 desktop shortcut launch-path runtime refinement across `launch_orin_desktop.vbs`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and `dev/orin_desktop_entrypoint_validation.py`, while keeping `main.py`, broader workspace follow-through, audio, logs, visual assets, and installer redesign out of scope.
Summary: Anchor the desktop startup runtime family at the real launch path while preserving the released FB-042 slice as the first historical proof.
Why it matters: Future launch-path, handoff, and relaunch follow-through should reuse one runtime family identity instead of drifting into separate near-duplicate feature-family records.

#### [Legacy Mapping: FAM-003] Monitoring, thermals, and performance HUD surface

Legacy FB ID: FB-040
Status: Released (v1.6.0-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.0-prebeta
Release Title: Pre-Beta v1.6.0
Branch: feature/fb-040-monitoring-thermals-performance-hud-surface
Canonical Workstream Doc: Docs/workstreams/FB-040_monitoring_thermals_performance_hud_surface.md
Release Target: v1.6.0-prebeta
Release Floor: minor prerelease (historical published tag; future architecture-only milestones must not use minor solely because they define a planning lane)
Version Rationale: FB-040 was published as `v1.6.0-prebeta`; post-release repair records the live release as canonical while governance now treats architecture-only, non-user-facing planning/admission milestones as patch-floor by default unless they deliver an executable or user-facing capability lane.
Release Scope: Architecture-only monitoring and thermal source mapping, ownership vocabulary, lifecycle/trust-safety framing, validation/admission contract definition, hardening pressure test, and Live Validation waiver truth for the current non-user-facing milestone.
Release Artifacts: Tag v1.6.0-prebeta; release title Pre-Beta v1.6.0; inclusion-only release notes summarize the FB-040 monitoring and thermal architecture milestone, source-map boundaries, lifecycle/trust-safety handling, validation/admission contract, hardening result, and Live Validation waivers.
Post-Release Truth: FB-040 is Released / Closed in v1.6.0-prebeta; release debt is clear; FB-031 Branch Readiness is admitted on `feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning`.
Version Drift Note: FB-040 advanced the public prerelease from `v1.5.0-prebeta` to `v1.6.0-prebeta`; because the delivered milestone was architecture-only and non-user-facing, future equivalent milestones must use patch prerelease advancement unless a true runtime, executable, or user-facing capability lane is delivered.
Summary: Track future runtime monitoring and HUD surfaces for GPU / CPU thermals and performance, including possible plugin-fed telemetry inputs.
Why it matters: Monitoring overlays are a separate runtime and status surface and should not be bolted onto the saved-action system without an explicit product boundary.

#### [Legacy Mapping: FAM-004] External trigger and plugin integration architecture

Legacy FB ID: FB-039
Status: Released (v1.5.0-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.5.0-prebeta
Release Title: Pre-Beta v1.5.0
Branch: feature/fb-039-external-trigger-plugin-integration-architecture
Canonical Workstream Doc: Docs/workstreams/FB-039_external_trigger_plugin_integration_architecture.md
Release Target: v1.5.0-prebeta
Release Floor: minor prerelease
Version Rationale: FB-039 created the external trigger and plugin integration architecture lane with an internal trigger intake boundary, so it was a new pre-Beta capability lane rather than patch-only UX, sequencing, or governance repair.
Release Scope: Internal-only external trigger intake architecture and runtime boundary, including source map, ownership vocabulary, lifecycle/trust framing, in-memory registration, bounded invocation follow-through, lifecycle transitions, decision evidence, boundary snapshots, readiness inspection, readiness sweep, readiness summary, and readiness detail snapshot.
Release Artifacts: Tag v1.5.0-prebeta; release title Pre-Beta v1.5.0; inclusion-only release notes summarize the FB-039 internal-only trigger intake milestone, capabilities, system behavior, validation evidence, and Live Validation waivers.
Post-Release Truth: FB-039 is Released / Closed in v1.5.0-prebeta; release debt is clear; FB-040 Branch Readiness is admitted on `feature/fb-040-monitoring-thermals-performance-hud-surface`.
Summary: Track future plugin and integration lifecycle design for external trigger surfaces such as Stream Deck and other installed integration points.
Why it matters: Plugin-backed action triggering needs explicit lifecycle, safety, and ownership boundaries before it becomes part of the product.

#### [Legacy Mapping: FAM-005] Nexus Desktop AI UI/UX overhaul planning

Legacy FB ID: FB-031
Status: Released (v1.6.1-prebeta)
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.1-prebeta
Release Title: Pre-Beta v1.6.1
Branch: feature/fb-031-nexus-desktop-ai-ui-ux-overhaul-planning
Canonical Workstream Doc: Docs/workstreams/FB-031_nexus_desktop_ai_ui_ux_overhaul_planning.md
Minimal Scope: Define the Nexus-era UI/UX overhaul planning boundary, source map, visual-language ownership, lifecycle/interaction-state framing, validation contract, and explicit non-goals before any UI implementation, runtime behavior, settings work, launcher work, or release work is considered.
Release Target: v1.6.1-prebeta
Release Floor: patch prerelease
Version Rationale: FB-031 is architecture-only UI/UX planning and implementation-admission canon with no executable, runtime, operator-facing, user-facing, or materially expanded product capability; per governance, architecture-only planning/admission work used patch prerelease advancement from v1.6.0-prebeta to v1.6.1-prebeta.
Release Scope: Architecture-only Nexus Desktop AI UI/UX source map, visual-language ownership vocabulary, lifecycle and interaction-state framing, future UI implementation admission contract, hardening pressure test, Live Validation repo-truth and waiver classification, PR Readiness merge-target canon, and PR-R1 release-floor validator repair.
Release Artifacts: Tag v1.6.1-prebeta; release title Pre-Beta v1.6.1; inclusion-only release notes summarize the FB-031 UI/UX architecture milestone, source-map and lifecycle/state boundaries, validation/admission contract, hardening result, Live Validation waivers, clean branch history, and PR-R1 release-floor validator repair.
Post-Release Truth: FB-031 is Released / Closed in v1.6.1-prebeta; release debt is clear; FB-032 PR Readiness is green on PR #73.
Summary: Preserved Nexus-era UI/UX overhaul planning as a deliberate design lane rather than piecemeal visual drift.
Why it matters: The Nexus-era visual language should be planned coherently before any later UI implementation pass.

#### [Legacy Mapping: FAM-006] ORIN voice/audio direction refinement

Legacy FB ID: FB-030
Status: Released
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.13-prebeta
Selection / Unblock: Implemented complete. `feature/fb-030-voice-audio-runtime-branch-readiness` delivered the bounded voice/audio runtime availability and truthful diagnostics proof, PR #108 merged into `main`, watcher verification proof exists through a forced run, and PR108 watcher automations are retired.
Next Workstream: Historical complete
Branch: feature/fb-030-voice-audio-runtime-branch-readiness
Canonical Workstream Doc: Docs/workstreams/FB-030_orin_voice_audio_direction_refinement.md
Branch Readiness: Historical complete. BR1 repaired the carried FB-049 post-merge stale-canon blocker, recorded the watcher handoff failure classification, and admitted the first bounded runtime diagnostics slice before implementation.
Workstream: Historical complete. WS1 implemented truthful `available`, `degraded`, `unavailable`, and `bypassed` voice/audio diagnostics without false success claims.
Hardening: Historical complete. H1 validated the diagnostics contract across voice, error-voice, launcher, main runtime, and regression-harness surfaces.
Live Validation: Historical complete. LV1 validated live-equivalent voice/audio diagnostic behavior and preserved launcher/runtime compatibility proof.
PR Readiness: Historical complete. PR #108 merged, watcher verification proof exists through a forced run, and PR108 watcher automations are retired.
Release Readiness: Released historical traceability in `v1.6.13-prebeta`.
Release Execution: Historical `v1.6.5-prebeta` planning release remains live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.5-prebeta on commit `7c2933d6427feb08a1139ba7f5ba2393eb61f1e1`; the runtime diagnostics follow-through is publicly released in `v1.6.13-prebeta` at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.13-prebeta on commit `faaf991d2579dd6478f78245d56956858cc2f59b`.
Released Historical Scope: FAM-001 legacy FB-049 Active-session pre-settled incoming-launch conflict truth plus FAM-004 legacy FB-030 voice/audio runtime diagnostics proof plus merged governance/automation proof package plus PR #112 source-truth closeout / merge-target authority hardening proof plus PR #113 source-truth closeout / merge-target authority hardening proof released in v1.6.13-prebeta
Repo State: Active Branch
Latest Public Prerelease: v1.6.13-prebeta
Release Title: Pre-Beta v1.6.13
Release Target: None - released in v1.6.13-prebeta.
Release Floor: none - release execution is complete.
Version Rationale: FAM-004 legacy FB-030 added bounded runtime diagnostics truth for voice/audio availability without opening a new feature family or materially widening product scope.
Release Scope: released governance reform, automation catalog proof, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 voice/audio runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening proof, and PR #113 source-truth closeout / merge-target authority hardening proof.
Release Artifacts: Published tag `v1.6.13-prebeta`; published GitHub prerelease title `Pre-Beta v1.6.13`; release notes include generated `What's Changed` and `Full Changelog` sections.
Post-Release Truth: merged governance reform, automation catalog, FAM-001 legacy FB-049 runtime proof, FAM-004 legacy FB-030 runtime diagnostics proof, PR #112 source-truth closeout / merge-target authority hardening, and PR #113 source-truth closeout / merge-target authority hardening are released historical traceability; release debt is clear; USER-approved selected-next truth points to FAM-006; and product completion is reopened on `feature/fam-006-monitoring-hud-product-surface` with `PKG-006` admitted and Workstream WS7 blocked pending USER Vision Input answers, digest, and Branch Readiness planning revalidation.
Selected Next Workstream: FAM-006 Monitoring and HUD.
Next-Branch Creation Gate: Cleared for `feature/fam-006-monitoring-hud-product-surface` only by USER-approved Branch Readiness Stage 2.
Historical Planning Release: `v1.6.5-prebeta` remains the released planning/admission proof for the original voice/audio direction milestone.
Minimal Scope: Completed WS1 voice/audio runtime availability and truthful diagnostics proof across `Audio/orin_voice.py`, `Audio/orin_error_voice.py`, `main.py`, `desktop/orin_desktop_launcher.pyw`, and `dev/orin_voice_regression_harness.py`, while preserving ORIN as the only shipped persona, keeping ARIA dormant, avoiding prompt or asset redesign, and avoiding public-copy or release-note changes before release phases.
Summary: Turn the released FAM-004 legacy FB-030 voice/audio planning contract into its first bounded runtime truth proof.
Why it matters: Voice execution, quiet mode, diagnostics, and persona claims must stay truthful when speech succeeds, bypasses, or fails.

#### [Legacy Mapping: FAM-007] Interaction and shared-action family anchor

Legacy FB ID: FB-027
Status: Released (v1.2.9-prebeta) / family aggregation hold
Record State: Closed
Registry Class: Feature Family
Family Anchor: Self
Priority: High
Release Stage: pre-Beta
Selection / Unblock: Released family anchor. Any future same-family runtime continuation requires explicit USER approval before Codex selects, splits, promotes, or branches it.
Next Workstream: None - USER approval required
Selected Next Workstream: None
Selected Next Runtime Slice: None
Selected Next Implementation Branch: Not created
Branch: None
Canonical Workstream Doc: Docs/workstreams/FB-027_interaction_system_baseline.md
Lifetime Dossier Doc: Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md
Lifetime Dossier State: Structured shell with partial historical pass migration. Phase 4 / Slice R4-S2 introduced the dossier shell, Phase 4 / Slice R4-S3 added pass index and slice/seam ledger templates, Phase 4 / Slice R4-S4 added validator/helper and artifact index templates, Phase 4 / Slice R4-S5 validated dossier stability, Phase 5 / Slice R5-S2 converted FB-036, FB-037, FB-038, and FB-041 into explicit historical pass records while populating the dossier pass index plus slice/seam ledger summary rows, and Phase 5 / Slice R5-S3 converted the preserved corresponding branch-record trace where it exists; validator/helper and artifact migration remain pending.
Branch Readiness: Historical PR #109 evidence. BR1 admitted a shutdown-hotkey confirmation proof before this governance correction reclassified it as family aggregation material rather than an active backlog lane.
Workstream: Historical PR #109 evidence. WS1 `shutdown hotkey confirmation runtime proof` routes `Ctrl+Alt+End` and `Ctrl+Alt+2` through confirmation before shutdown, preserves the active session on cancel or timeout, and validates accepted clean shutdown through the desktop entrypoint harness.
Hardening: Historical PR #109 evidence. H1 `Shutdown Hotkey Confirmation Runtime Validation` validated confirmation request, accepted clean shutdown, cancelled/session-preserved behavior, timeout/session-preserved behavior, interaction baseline compatibility, desktop entrypoint compatibility, boot transition compatibility, branch governance, and automation observability review.
Live Validation: Historical PR #109 evidence. LV1 `Shutdown Hotkey Confirmation Live Validation` passed with closest live-equivalent desktop entrypoint shortcut evidence, interaction-baseline proof for both shutdown hotkeys, and User Test Summary results recorded as `PASS`.
PR Readiness: Historical PR #109 evidence. PR #109 merged after PR1 live validation, bot-review closeout, and merge-watch proof; it is not a selected-next or active-lane driver.
Release Readiness: Not started and not required for PR #109 as a standalone release driver; historical `v1.2.9-prebeta` baseline release proof remains preserved.
Current Active Workstream: None
Promotion Gate: Closed family anchor. Future continuation requires explicit USER approval under `Backlog Addition User Approval Missing`.
Standalone Release Driver: No
Aggregation Target: Future USER-approved FAM-003 legacy FB-027 family release or larger approved release aggregation.
Minimal Scope: Historical PR #109 aggregation evidence adds confirm-before-exit behavior for `Ctrl+Alt+End` and `Ctrl+Alt+2`; no next same-family runtime slice is selected.
Summary: Anchor the typed-first interaction and shared-action family while preserving PR #109 as family evidence instead of a release-version driver.
Why it matters: Future authoring, callable-group, built-in action, and tray task follow-through should reuse one interaction/action family identity instead of drifting into separate near-duplicate feature-family records.

### Historical Consolidated Pass Aliases

Former standalone historical pass backlog entries now live here as family traceability only. They are not parseable backlog items, are not independently selectable, and must be loaded through the family dossier plus canonical workstream record named below.

#### FB-042 Desktop Startup Runtime Family Pass Trace

| Former ID | Pass ID | Family Anchor | Source-Of-Truth Record | Lifetime Dossier | Release Trace | Selection State |
| --- | --- | --- | --- | --- | --- | --- |
| `FB-048` | `F042-P07` | `FB-042` | `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.12-prebeta` | Historical family pass only; not selectable |
| `FB-047` | `F042-P06` | `FB-042` | `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.11-prebeta` | Historical family pass only; not selectable |
| `FB-046` | `F042-P05` | `FB-042` | `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.10-prebeta` | Historical family pass only; not selectable |
| `FB-045` | `F042-P04` | `FB-042` | `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.9-prebeta` | Historical family pass only; not selectable |
| `FB-044` | `F042-P03` | `FB-042` | `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.9-prebeta` | Historical family pass only; not selectable |
| `FB-043` | `F042-P02` | `FB-042` | `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md` | `Docs/workstreams/FB-042_desktop_startup_runtime_family_dossier.md` | `v1.6.8-prebeta` | Historical family pass only; not selectable |

#### FB-027 Interaction And Shared-Action Family Pass Trace

| Former ID | Pass ID | Family Anchor | Source-Of-Truth Record | Lifetime Dossier | Release Trace | Selection State |
| --- | --- | --- | --- | --- | --- | --- |
| `FB-041` | `F027-P03` | `FB-027` | `Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.3.1-prebeta` | Historical family pass only; not selectable |
| `FB-038` | `F027-P05` | `FB-027` | `Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.4.1-prebeta` | Historical family pass only; not selectable |
| `FB-037` | `F027-P04` | `FB-027` | `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.4.0-prebeta` | Historical family pass only; not selectable |
| `FB-036` | `F027-P02` | `FB-027` | `Docs/workstreams/FB-036_saved_action_authoring.md` | `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md` | `v1.3.0-prebeta` | Historical family pass only; not selectable |

#### [Former ID: FB-048] Active-session relaunch signal-failure and wait-timeout truth

Status: Released (v1.6.12-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P07
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.12-prebeta
Selection / Unblock: Implemented complete. `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth` delivered the admitted failure/timeout truth slice chain, the follow-up repair and canon/governance containment PRs are merged on `main`, and `v1.6.12-prebeta` is now published, validated, and closed through post-release canon sync.
Historical Follow-Through: repo-level selected-next truth later moved to FB-049 after this release window; this alias record does not independently own successor selection.
Branch Creation Gate: Satisfied during FB-048 Branch Readiness after `v1.6.11-prebeta` publication, validation, updated-`main` revalidation, and first-slice admission.
Branch: feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth
Canonical Workstream Doc: Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md
Historical Branch Readiness Record: Docs/branch_records/feature_fb_048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md
Branch Readiness: Historical complete. The branch objective, target end-state, admitted WS-1 slice, validation coverage, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical Branch Readiness record.
Workstream: Released. WS-1 `accepted relaunch failure-path truthful outcome proof` is complete and validated; H-1 failure/timeout lifecycle hardening is complete and green; LV-1 is complete and green with real desktop shortcut evidence plus reusable failure/timeout lifecycle proof; accepted relaunch signal-failure emits an explicit preserved-session marker and accepted relaunch wait-timeout emits an explicit replacement-unconfirmed marker instead of collapsing into a generic already-running skip; repeated signal-failure launches preserve the active settled owner even under rapid repetition; near-deadline reacquire no longer falls through to a false timeout; mixed failure -> decline -> accept -> failure sequencing keeps failure, decline, and success classification distinct; `Backlog Completion State` is `Implemented Complete`; PR #94, PR #96, and PR #97 are complete historical proof; the lane is released and closed in `v1.6.12-prebeta`; and the branch's governance/validator hardening is now part of the released canonical baseline.
Backlog Completion State: Implemented Complete
PR Readiness: Complete historical proof. PR #94 merged the bounded FB-048 implementation package; PR #96 merged the post-merge review repair that corrected wait-timeout truth and the non-Windows validator guard; and PR #97 merged the post-sync canon plus merge-stable governance containment on `main`.
Release Target: v1.6.12-prebeta
Release Floor: patch prerelease
Version Rationale: FB-048 delivers a bounded runtime/user-facing relaunch signal-failure and wait-timeout refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-048 WS-1 accepted relaunch failure-path truthful outcome proof, H-1 failure/timeout lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, PR package history, merged-unreleased release-debt truth, selected-next FB-049 successor lock, and merge-stable current-state governance hardening plus validator guardrails for the bounded runtime/user-facing lane only.
Release Artifacts: Tag v1.6.12-prebeta; release title Pre-Beta v1.6.12; rich Markdown release notes summarize the bounded FB-048 relaunch failure/timeout runtime/user-facing package, real shortcut evidence, and the FB-049 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-048 is Released / Closed in `v1.6.12-prebeta`; release debt is clear; the governance reform branch may proceed through its approved docs-only branch-authority record; and FB-049 remains selected next, `Registry-only`, and branch-not-created until that branch completes and later FB-049 Branch Readiness admits the first bounded pre-settled incoming-launch conflict truth slice.
Minimal Scope: Prove and refine the accepted relaunch failure lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so relaunch-signal failure or reacquire wait-timeout preserves truthful ownership, emits explicit failure-path markers, and avoids false replacement-session or guard-transfer claims.
Summary: Make accepted-but-unfinished relaunch failures as truthful as accepted and declined success paths.
Why it matters: Users should get an explicit, proven outcome when relaunch was requested but the current session could not be signaled or did not release in time.

#### [Former ID: FB-047] Active-session relaunch decline session-preservation proof

Status: Released (v1.6.11-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P06
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.11-prebeta
Selection / Unblock: Implemented complete. `feature/fb-047-active-session-relaunch-decline-preservation` delivered the admitted decline-preservation slice chain, PR #93 merged into `main`, and `v1.6.11-prebeta` is now published, validated, and closed through post-release canon sync.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-047 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch Creation Gate: Historical complete. `v1.6.10-prebeta` was published and validated, updated `main` was revalidated, and FB-047 Branch Readiness admitted the bounded runtime/user-facing relaunch-decline preservation slice before promotion.
Branch: feature/fb-047-active-session-relaunch-decline-preservation
Canonical Workstream Doc: Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md
Historical Branch Readiness Record: Docs/branch_records/feature_fb_047_active_session_relaunch_decline_preservation.md
Branch Readiness: Historical complete. The branch objective, target end-state, admitted WS-1 slice, validation contract, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical branch-readiness record.
Workstream: Released. WS-1 `declined relaunch incoming-launch truthful exit proof` is complete and validated; harness-driven decline proof records explicit preserved-session success markers instead of a generic already-running skip; repeated incoming declined launches preserve the active settled session and never emit replacement-session markers; H-1 decline-lifecycle hardening is complete / green; LV-1 real desktop shortcut evidence and reusable decline-lifecycle proof are complete / green; `Backlog Completion State` is `Implemented Complete`; PR-1 / PR-2 / PR-3 are complete historical proof; and the branch is now Released / Closed in `v1.6.11-prebeta`.
Backlog Completion State: Implemented Complete
PR Readiness: Complete. PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus validation are complete historical proof; PR #93 merged into `main` at `4ca70572fbc8033bc96fcd299dd309464e81393a`.
Release Target: v1.6.11-prebeta
Release Floor: patch prerelease
Version Rationale: FB-047 delivers a bounded runtime/user-facing relaunch-decline preservation refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-047 WS-1 declined relaunch incoming-launch truthful exit proof, H-1 decline lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, PR package history, release publication, and selected-next FB-048 successor admission for the bounded runtime/user-facing lane only.
Release Artifacts: Tag v1.6.11-prebeta; release title Pre-Beta v1.6.11; rich Markdown release notes summarize the bounded FB-047 relaunch-decline preservation runtime/user-facing package, real shortcut evidence, and the FB-048 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-047 is Released / Closed in `v1.6.11-prebeta`; release debt is clear; and later runtime-family continuation moved through FB-048 on `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth` while this alias entry remained released historical proof.
Minimal Scope: Prove and refine the relaunch-decline lane across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and the minimum required reusable validator surfaces so declining replacement preserves the active settled session and cleanly terminates the incoming launch without dual ownership or false successor markers.
Summary: Make relaunch decline as provable and truthful as accepted relaunch.
Why it matters: The runtime should be just as explicit when the user keeps the current settled session as when the user accepts replacement.

#### [Former ID: FB-046] Active-session relaunch reacquisition and settled re-entry proof

Status: Released (v1.6.10-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P05
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.10-prebeta
Release Title: Pre-Beta v1.6.10
Selection / Unblock: Implemented complete. `feature/fb-046-active-session-relaunch-reacquisition` delivered the admitted relaunch-reacquisition slice chain, PR #92 merged into `main`, and `v1.6.10-prebeta` is now published and validated.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-046 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch: feature/fb-046-active-session-relaunch-reacquisition
Repair-Only Branch Handling: `feature/fb-046-post-merge-canon-sync` is a bounded repair-only post-merge canon-sync `feature/` branch and does not imply Branch Readiness admission or active branch truth for FB-046.
Canonical Workstream Doc: Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md
Historical Branch Readiness Record: Docs/branch_records/feature_fb_046_active_session_relaunch_reacquisition.md
Branch Readiness: Historical complete. The admitted slice, validation contract, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical branch-readiness record.
Workstream: Released. WS-1 accepted relaunch replacement-session settled re-entry proof is complete and validated; accepted relaunch now proves prior-session shutdown, single-instance guard release, replacement-session reacquisition, replacement-session authoritative settled re-entry, and truthful post-settled lifecycle completion without dual ownership; H-1 relaunch lifecycle hardening is complete and green across slow shutdown, recoverable-exit relaunch, and rapid consecutive relaunch-cycle proof; LV-1 is complete and green with real desktop shortcut evidence plus a focused User Test Summary waiver; `Backlog Completion State` is `Implemented Complete`; and the released branch is now historical proof in `v1.6.10-prebeta`.
Backlog Completion State: Implemented Complete
PR Readiness: Complete. PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus validation are complete; PR #92 merged into `main` at `36cf07495dc8e239b20b11afb5194355b77ffd8b`.
Release Readiness: Complete. `main` validated green for `v1.6.10-prebeta` release packaging before release execution.
Release Execution: `v1.6.10-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.10-prebeta on commit `36cf07495dc8e239b20b11afb5194355b77ffd8b`.
Release Target: v1.6.10-prebeta
Release Floor: patch prerelease
Version Rationale: FB-046 delivers a bounded runtime/user-facing relaunch-reacquisition refinement on the existing desktop startup family without opening a new product lane or materially expanded feature family.
Release Scope: completed FB-046 WS-1 accepted relaunch replacement-session settled re-entry proof, H-1 relaunch lifecycle hardening, LV-1 real desktop shortcut evidence, reusable validation evidence, PR package history, merged-unreleased release-debt truth, and selected-next FB-047 successor lock for the bounded runtime/user-facing lane only.
Release Artifacts: Tag v1.6.10-prebeta; release title Pre-Beta v1.6.10; rich Markdown release notes summarize the bounded FB-046 relaunch-reacquisition runtime/user-facing package, real shortcut evidence, and the FB-047 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-046 is Released / Closed in `v1.6.10-prebeta`; release debt is clear; and after merge FB-047 becomes the merged-unreleased release-debt owner for `v1.6.11-prebeta`, while FB-048 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded relaunch-reacquisition runtime/user-facing pass across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_boot_transition_verification.py`, and the minimum required reusable validator surfaces so a confirmed relaunch request closes the active session, reacquires the runtime guard, and returns the replacement session to authoritative settled state without widening into `main.py`, `Audio/`, `logs/`, `jarvis_visual/`, installer work, or broader boot-orchestrator scope.
Summary: Turn accepted relaunch into a full replacement-session completion proof surface instead of a partial signal-and-exit story.
Why it matters: The repo now proves who owns the runtime after relaunch, when the old session is truly gone, and when the replacement session has actually made it back to authoritative settled state.

#### [Former ID: FB-045] Active-session relaunch outcome refinement

Status: Released (v1.6.9-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P04
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.9-prebeta
Release Title: Pre-Beta v1.6.9
Selection / Unblock: FB-045 was selected because updated-main `Release Readiness` for FB-044 found a reproducible post-settled runtime failure after the authoritative settled marker. `feature/fb-045-active-session-relaunch-stability` corrected that lifecycle boundary, merged through PR #90, and is now released historical proof in `v1.6.9-prebeta`.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-045 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch: feature/fb-045-active-session-relaunch-stability
Canonical Workstream Doc: Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md
Historical Branch-Readiness Record: Docs/branch_records/feature_fb_045_active_session_relaunch_stability.md
Branch Readiness: Historical complete. The blocker classification, admitted WS-1 slice, validation contract, rollback conditions, and same-branch backlog-completion posture remain preserved in the historical branch-readiness record.
Workstream: Released. WS-1 `post-settled runtime stability refinement` is complete and validated; H-1 post-settled lifecycle hardening is complete and green; LV-1 live validation is complete and green with real desktop shortcut evidence and a focused User Test Summary waiver; PR-1 / PR-2 / PR-3 are complete historical proof; and the blocker-clearing package is now released historical proof inside `v1.6.9-prebeta`.
Backlog Completion State: Implemented Complete
Minimal Scope: Classify post-settled abnormal renderer exits as a recoverable lifecycle condition after authoritative settled is already proven, keep settled truth authoritative, preserve green startup paths, and avoid widening beyond launcher / validator relaunch-stability scope.
Summary: Clear the FB-044 release blocker by fixing launcher lifecycle classification after settled and proving that result across primary-workspace and disposable-copy validation.
Why it matters: Keeps startup truth honest, prevents post-settled runtime exits from being mislabeled as startup failure, and unblocks the path back to FB-044 `Release Readiness`.

#### [Former ID: FB-044] Boot-to-desktop handoff outcome refinement

Status: Released (v1.6.9-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P03
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.9-prebeta
Release Title: Pre-Beta v1.6.9
Selection / Unblock: Implemented complete. `feature/fb-044-boot-desktop-handoff-outcome-refinement` delivered WS-1 `desktop-settled handoff outcome refinement`; FB-045 on `feature/fb-045-active-session-relaunch-stability` delivered the blocker-clearing lifecycle follow-through inside the same release window; PR #89, PR #90, and PR #91 merged; and `v1.6.9-prebeta` is now published, validated, and in post-release canon closure.
Historical Follow-Through: released / closed historical proof. No remaining implementable FB-044 work remains on this backlog lane, and later runtime-family continuation is preserved elsewhere in family history.
Branch: feature/fb-044-boot-desktop-handoff-outcome-refinement
Canonical Workstream Doc: Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md
Historical Branch Authority Record: Docs/branch_records/feature_fb_044_boot_desktop_handoff_outcome_refinement.md
Branch Readiness: Complete. Historical Branch Readiness truth is preserved in the branch authority record.
Workstream: Released. WS-1 `desktop-settled handoff outcome refinement` is complete and validated; H-1 settled-state hardening is complete and green; LV-1 live validation is complete and green with real desktop shortcut evidence and a narrow User Test Summary waiver; PR-1 / PR-2 / PR-3 are complete historical proof; `Backlog Completion State` is `Implemented Complete`; FB-045's blocker-clearing lifecycle follow-through is released historical proof in the same package; and `v1.6.9-prebeta` is now live and validated.
Release Target: v1.6.9-prebeta
Release Floor: patch prerelease
Version Rationale: FB-044 delivers a bounded runtime/user-facing boot-to-desktop settled-outcome refinement on the existing startup family without opening a new product lane or materially expanded runtime family.
Release Scope: complete the bounded FB-044 settled-outcome slice chain on this same branch across `main.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_boot_transition_verification.py`, and `dev/orin_desktop_entrypoint_validation.py`, along with H-1, LV-1, PR package history, release publication, and the released FB-045 blocker-clearing lifecycle follow-through inside the same `v1.6.9-prebeta` package.
Release Artifacts: Tag v1.6.9-prebeta; release title Pre-Beta v1.6.9; rich Markdown release notes summarize the bounded FB-044 boot-to-desktop settled-outcome refinement, the FB-045 blocker-clearing lifecycle classification result, real shortcut evidence, and the FB-046 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded runtime/user-facing boot-to-desktop handoff refinement lane across `main.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, `dev/orin_boot_transition_verification.py`, and `dev/orin_desktop_entrypoint_validation.py`, while keeping `Audio/`, `logs/`, `jarvis_visual/`, installer work, and broader future boot-orchestrator implementation out of scope.
Summary: Continue the entrypoint/runtime lane by making desktop-settled outcome proof explicit and shared across boot, launcher, renderer, and validation paths.
Why it matters: Builds directly on FB-043's ownership cleanup and turns the remaining boot/desktop proof ambiguity into a bounded runtime-bearing implementation result instead of lingering branch-readiness truth.

#### [Former ID: FB-043] Top-level desktop entrypoint ownership and main.py handoff refinement

Status: Released (v1.6.8-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-042
Pass ID: F042-P02
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: Released
Target Version: v1.6.8-prebeta
Release Title: Pre-Beta v1.6.8
Selection / Unblock: Implemented complete. `feature/fb-043-top-level-entrypoint-handoff-refinement` delivered WS-1 `main.py` direct-launch handoff refinement plus WS-2 explicit launch-intent refinement, the branch merged through PR #88, and `v1.6.8-prebeta` is now published and validated.
Branch: feature/fb-043-top-level-entrypoint-handoff-refinement
Repair-Only Branch Handling: `feature/fb-043-release-debt-marker-repair` is a repair-only `feature/` branch and does not imply Branch Readiness admission or active branch truth.
Canonical Workstream Doc: Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md
Branch Readiness: Complete. The former branch-readiness authority on `feature/fb-043-top-level-entrypoint-handoff-refinement` admitted WS-1 with exact owned paths, validation coverage, rollback conditions, same-branch continuation posture, and the branch-level closure rule before promotion.
Workstream: Released. WS-1 `main.py` direct-launch handoff refinement and WS-2 explicit launch-intent refinement are complete and validated; plain no-argument direct `main.py` launches and explicit `--desktop-entrypoint` launches now hand off to the canonical desktop chain; explicit dev boot paths remain verifiable through recognized boot arguments, including the legacy dev launcher's explicit manual/voice contract; invalid direct-launch args now fail fast with guidance; H-1 entrypoint hardening is complete and green; LV-1 live validation is complete and green with real desktop shortcut evidence and a narrow User Test Summary waiver; PR-1 / PR-2 / PR-3 are complete; `Backlog Completion State` is `Implemented Complete`; and the released branch is now historical proof in `v1.6.8-prebeta`.
Release Target: v1.6.8-prebeta
Release Floor: patch prerelease
Version Rationale: FB-043 delivers a bounded runtime/user-facing top-level desktop entrypoint ownership and `main.py` handoff refinement on the existing launch path without opening a new product lane or materially expanded runtime family.
Release Scope: complete the bounded FB-043 top-level entrypoint slice chain on this same branch: WS-1 `main.py` direct-launch handoff refinement plus WS-2 explicit launch-intent refinement across `main.py`, the minimal required launcher-contract surfaces, `dev/orin_desktop_entrypoint_validation.py`, and `dev/orin_boot_transition_verification.py`, along with H-1, LV-1, PR package history, and merged-unreleased release-debt truth.
Release Artifacts: Tag v1.6.8-prebeta; release title Pre-Beta v1.6.8; rich Markdown release notes summarize the bounded FB-043 top-level entrypoint ownership and `main.py` handoff refinement, explicit launch-intent outcome, real shortcut evidence, and the FB-044 successor lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Release Execution: `v1.6.8-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.8-prebeta on commit `5e695af5fada05e4ad6b25731bce328ede8a09ee`.
Post-Release Truth: FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded top-level entrypoint slice chain on this same branch: WS-1 `main.py` direct-launch handoff refinement plus WS-2 explicit launch-intent refinement across `main.py`, the minimal required launcher-contract surfaces, `dev/orin_desktop_entrypoint_validation.py`, and `dev/orin_boot_transition_verification.py`, while keeping `Audio/`, `logs/`, `jarvis_visual/`, installer work, and broader workspace reshaping out of scope.
Summary: Continue the desktop entrypoint runtime lane by clarifying and tightening top-level ownership and handoff on the shipped launch path.
Why it matters: Builds directly on FB-042's user-facing launch-path improvement and keeps the next branch implementation-bearing instead of slipping back into planning-only governance work.

#### [Former ID: FB-041] Deterministic callable-group execution layer

Status: Released (v1.3.1-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P03
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: pre-Beta
Target Version: v1.3.1-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-041_deterministic_callable_group_execution_layer.md
Summary: Released the first bounded callable-group follow-through execution layer for deterministic linear member execution in stored order with stop-on-failure, terminal success or failure propagation, and runtime progression markers.
Why it matters: FB-041 closes the released FB-036 callable-group execution follow-through by supporting full stored-order group execution without reopening authoring, changing single-action behavior, or widening into scheduling, branching, retries, nested groups, or parallelism.

#### [Former ID: FB-038] Taskbar / tray quick-task UX and Create Custom Task surface

Status: Released (v1.4.1-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P05
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.4.1-prebeta
Release Title: Pre-Beta v1.4.1
Canonical Workstream Doc: Docs/workstreams/FB-038_taskbar_tray_quick_task_ux.md
Summary: Released the FB-038 tray quick-task UX milestone, including tray identity/discoverability, tray Open Command Overlay, tray Create Custom Task dialog-open/no-write route, tray-origin create completion through the existing FB-036 authoring path, catalog reload and exact-match resolution, confirm/result execution, and startup first-visible Core Visualization sequencing repair.
Why it matters: Taskbar and tray interaction now has an explicit released UX lane that remains bounded to the shared action model rather than becoming a parallel authoring or launcher surface.

#### [Former ID: FB-037] Curated built-in system actions and Nexus settings expansion

Status: Released (v1.4.0-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P04
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: pre-Beta
Target Version: v1.4.0-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md
Summary: Released the first curated Windows utility built-in catalog under the shared action model, including Task Manager, Calculator, Notepad, and Paint while preserving saved-action override authority, authoring collision protection, confirm/result surfaces, and callable-group behavior.
Why it matters: Standard product actions now feel native and inspectable under the shared action model instead of being pushed into user-defined saved actions as ad hoc customization. Common Windows actions ship as first-class built-ins, while saved actions remain the seam for personal or non-standard tasks.

#### [Former ID: FB-036] Limited saved-action authoring and type-first custom task UX

Status: Released (v1.3.0-prebeta)
Record State: Closed
Registry Class: Historical Pass Alias
Historical Alias Of: FB-027
Pass ID: F027-P02
Alias Role: Historical Pass Record
Selectable Independently: No
Priority: High
Release Stage: pre-Beta
Target Version: v1.3.0-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-036_saved_action_authoring.md
Summary: Released the bounded custom-task authoring, callable-group management, inline group quick-create, and exact-green validation hardening milestone above the locked FB-027 interaction baseline.
Why it matters: Nexus now supports deliberate in-product custom-task and callable-group authoring without reopening the typed-first overlay contract, widening into Action Studio, or weakening exact-match resolution boundaries.

### Support / Architecture / Governance Lanes

Closed support, architecture, and governance lanes are historical traceability only. They are not parseable backlog items under the new governance unless the USER explicitly approves a future major release/support lane.

| Former ID | Historical Lane | Source-Of-Truth Record | Release Trace | Trace Role |
| --- | --- | --- | --- | --- |
| `FB-035` | Support-report release-context fallback hardening | `Docs/workstreams/FB-035_release_context_fallback_hardening.md` | `v1.2.7-prebeta` | Closed support lane trace |
| `FB-034` | Recoverable incident diagnostics surface and failure-class follow-through | `Docs/workstreams/FB-034_recoverable_diagnostics.md` | `v1.2.6-prebeta` | Closed support lane trace |
| `FB-033` | Dev-only startup snapshot harness follow-through | `Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md` | `v1.2.4-prebeta` | Closed support lane trace |
| `FB-032` | Nexus-era vision and source-of-truth migration | `Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md` | `v1.6.2-prebeta` | Closed architecture/governance trace |
| `FB-029` | ORIN legal-safe rebrand, future ARIA persona option, and repo licensing hardening | `Docs/workstreams/FB-029_orin_identity_licensing_hardening.md` | `v1.6.4-prebeta` | Closed support lane trace |
| `FB-028` | Relocate launcher history state out of root logs | `Docs/workstreams/FB-028_history_state_relocation.md` | `v1.2.3-prebeta` | Closed support lane trace |
| `FB-025` | Boot and desktop milestone taxonomy clarification | `Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md` | `v1.2.5-prebeta` | Closed architecture trace |
| `FB-015` | Boot and desktop phase-boundary model | `Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md` | `v1.6.4-prebeta` | Closed architecture trace |
| `FB-005` | Workspace and folder organization | `Docs/workstreams/FB-005_workspace_and_folder_organization.md` | `v1.6.6-prebeta` | Closed support/workspace trace |
| `FB-004` | Future boot orchestrator layer | `Docs/workstreams/FB-004_future_boot_orchestrator_layer.md` | `v1.6.3-prebeta` | Closed architecture trace |

#### [Former ID: FB-035] Support-report release-context fallback hardening

Status: Released (v1.2.7-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.7-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-035_release_context_fallback_hardening.md
Summary: Hardened support-report fallback release-context derivation so generated artifacts use released-canon truth when `.git` metadata is unavailable.
Why it matters: Prevents support bundles and issue drafts from reporting an unreleased higher planned prerelease.

#### [Former ID: FB-034] Recoverable incident diagnostics surface and failure-class follow-through

Status: Released (v1.2.6-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.6-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-034_recoverable_diagnostics.md
Summary: Closed the first recoverable-diagnostics milestone for one explicitly bounded repeated-identical `launch_failed` incident class.
Why it matters: Makes the Class 2/Class 3 boundary explicit without widening diagnostics policy or breaking the manual-reporting boundary.

#### [Former ID: FB-033] Dev-only startup snapshot harness follow-through

Status: Released (v1.2.4-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.4-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-033_startup_snapshot_harness_follow_through.md
Summary: Stabilized the env-gated startup snapshot harness as bounded dev-only debugging infrastructure.
Why it matters: Preserves a repeatable startup evidence path without turning it into normal user-facing behavior.

#### [Former ID: FB-032] Nexus-era vision and source-of-truth migration

Status: Released (v1.6.2-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.6.2-prebeta
Release Title: Pre-Beta v1.6.2
Branch: feature/fb-032-nexus-era-vision-source-of-truth-migration
Canonical Workstream Doc: Docs/workstreams/FB-032_nexus_era_vision_and_source_of_truth_migration.md
Workstream: WS-1 current-vs-historical source-of-truth inventory and naming policy, WS-2 classification and mapping of canonical vs historical surfaces, and WS-3 validation and admission contract for controlled migration execution are complete.
Hardening: H-1 source-of-truth migration frame pressure test is complete.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: PR-1 merge-target canon, PR-2 durable branch truth, and PR-3 live PR validation are complete; PR #73 merged cleanly into `main`.
Release Execution: `v1.6.2-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.2-prebeta on commit `e282072769ec25694928293ce51e144d6a37f611`.
Branch Readiness Governance Repair: GitHub release notes across the live release history were standardized to Markdown release bodies that do not repeat the release title as a leading H1 and that include generated `## What's Changed` and `**Full Changelog**:` sections; Release Readiness governance and validator coverage now require that format before future release execution can be treated as complete.
Minimal Scope: FB-032 kept Nexus-era source-of-truth migration controlled by current-vs-historical naming policy, canonical vs historical surface classification, AI/UI identity routing, canon migration admission rules, and explicit non-goals before any wording migration, persona work, runtime behavior, UI implementation, rebrand execution, or release work is considered.
Release Target: v1.6.2-prebeta
Release Floor: patch prerelease
Version Rationale: FB-032 was architecture-only and canon-only planning, admission, validation, and governance work with no executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Architecture-only Nexus-era source-of-truth inventory, naming policy, surface classification, controlled migration admission contract, governance repairs, hardening, Live Validation waivers, and PR Readiness merge-target canon.
Release Artifacts: Tag v1.6.2-prebeta; release title Pre-Beta v1.6.2; inclusion-only release notes summarize the FB-032 migration frame and governance/validation outcomes.
Post-Release Truth: FB-032 is Released / Closed in v1.6.2-prebeta; release debt is clear; FB-004 is Released / Closed in `v1.6.3-prebeta`, and FB-015 Branch Readiness is selected next on `feature/fb-015-boot-desktop-phase-boundary-model`.
Summary: Preserved the broader Nexus-era vision and source-of-truth migration foundation above future controlled migration work.
Why it matters: The repo now has a controlled identity, naming, and source-of-truth migration frame before deeper wording or implementation normalization begins.

#### [Former ID: FB-029] ORIN legal-safe rebrand, future ARIA persona option, and repo licensing hardening

Status: Released (v1.6.4-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: High
Release Stage: pre-Beta
Target Version: v1.6.4-prebeta
Release Title: Pre-Beta v1.6.4
Deferred Since: current pre-Beta identity backlog registration before FB-032 promotion.
Deferred Because: legal-safe naming, ORIN/ARIA persona posture, and licensing hardening need explicit product/legal approval for implementation-facing execution and must not ride along with source-of-truth migration, UI, runtime, or release work.
Selection / Unblock: FB-029 is admitted only as a docs/canon-only planning milestone on this branch. Any implementation-facing naming, licensing, persona, release, or runtime edit still requires explicit product/legal approval and must remain out of scope unless a later legal surface admits it.
Branch: feature/fb-029-orin-identity-licensing-hardening
Canonical Workstream Doc: Docs/workstreams/FB-029_orin_identity_licensing_hardening.md
Branch Readiness: Complete. The branch objective, target end-state, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 current identity, persona-option, and licensing source-of-truth inventory, WS-2 canonical vs historical identity, persona-option, and licensing boundary framing, and WS-3 validation and admission contract for future identity and licensing implementation are complete.
Hardening: H-1 pressure test of identity inventory, persona-option framing, licensing boundary framing, and future implementation admission rules is complete.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus authenticated PR state validation are complete; PR #76 merged cleanly into `main` at `0897fab768dc07385f83fab81434ba7926ecc4a1`.
Release Readiness: Included in the validated inherited `v1.6.4-prebeta` package on `main` while FB-015 remained the sole release-debt owner before publication.
Release Execution: `v1.6.4-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.4-prebeta on commit `d2268b71feefa062c8117eae29f8ec17879a724f`.
Release Target: v1.6.4-prebeta
Release Floor: patch prerelease
Version Rationale: FB-029 remains a docs/canon-only identity, persona-option, and licensing-planning milestone with no new executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Identity source-of-truth inventory, persona-option boundary framing, licensing boundary framing, implementation admission contract, hardening corrections, Live Validation waivers, PR package history, merged-unreleased package-state repair, and post-merge current-state cleanup.
Release Artifacts: Tag v1.6.4-prebeta; release title Pre-Beta v1.6.4; rich Markdown release notes summarize the FB-015 boundary model and the FB-029 identity/licensing planning frame without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-029 is Released / Closed in v1.6.4-prebeta; FB-015 is also Released / Closed in the same package; FB-030 is Released / Closed in v1.6.5-prebeta; FB-005 is Released / Closed in v1.6.6-prebeta; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Define the Branch Readiness frame for legal-safe ORIN naming, optional future ARIA persona posture, and repo licensing hardening before any naming, licensing, release, runtime, or persona-facing edits begin; Workstream remains docs/canon only unless a later legal surface explicitly widens scope.
Summary: Track future ORIN-era naming, persona, and licensing hardening work without treating the local rebrand overlay as merged truth.
Why it matters: Product identity, legal posture, and repo ownership still need durable future treatment, but not by accidental carry-forward.

#### [Former ID: FB-028] Relocate launcher history state out of root logs

Status: Released (v1.2.3-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Medium
Release Stage: pre-Beta
Target Version: v1.2.3-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-028_history_state_relocation.md
Summary: Moved launcher-owned historical state out of the live root logs tree into a dedicated state location.
Why it matters: Keeps historical state out of user-visible runtime logs while preserving behavior and fallback rules.

#### [Former ID: FB-025] Boot and desktop milestone taxonomy clarification

Status: Released (v1.2.5-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Low
Release Stage: pre-Beta
Target Version: v1.2.5-prebeta
Canonical Workstream Doc: Docs/workstreams/FB-025_boot_desktop_milestone_taxonomy_clarification.md
Summary: Clarified shared milestone taxonomy between `BOOT_MAIN|...` and `RENDERER_MAIN|...` without collapsing ownership.
Why it matters: Keeps boot and desktop evidence easier to compare while preserving separate ownership boundaries.

#### [Former ID: FB-015] Boot and desktop phase-boundary model

Status: Released (v1.6.4-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: High
Release Stage: Slice-staged
Target Version: v1.6.4-prebeta
Release Title: Pre-Beta v1.6.4
Deferred Since: v2.0 closeout after the FB-015 rev1a phase-boundary clarification.
Deferred Because: the boot/desktop ownership model is clarified at planning level, but no later implementation-facing boundary change has been admitted.
Selection / Unblock: Select when a concrete boot, desktop, startup, trust, or orchestration lane is blocked by unresolved ownership boundaries; Branch Readiness must name the exact ambiguity it resolves.
Priority Review: Raised to High during the FB-004 pre-PR docs governance sync because boot/desktop phase-boundary follow-through is the clearest routine technical successor after FB-004 unless an explicitly approved product/legal, voice, or workspace lane supersedes it.
Branch: feature/fb-015-boot-desktop-phase-boundary-model
Canonical Workstream Doc: Docs/workstreams/FB-015_boot_and_desktop_phase_boundary_model.md
Branch Readiness: Complete. The branch objective, target end-state, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 current boot/desktop boundary inventory and ownership map, WS-2 lifecycle and phase-boundary state framing, and WS-3 validation and admission contract for future boot/desktop boundary implementation are complete.
Hardening: H-1 pressure test of the boot/desktop boundary inventory and ownership map, lifecycle and phase-boundary state framing, and future implementation admission contract is complete.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus authenticated PR state validation are complete; PR #75 merged cleanly into `main` at `3e821e07ff91d814fd7aba9b50819f97d700a301`.
Release Readiness: Complete. `main` validated green for `v1.6.4-prebeta` release packaging before release execution.
Release Execution: `v1.6.4-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.4-prebeta on commit `d2268b71feefa062c8117eae29f8ec17879a724f`.
Release Target: v1.6.4-prebeta
Release Floor: patch prerelease
Version Rationale: FB-015 remains a docs/canon-only boundary inventory, ownership, lifecycle, and implementation-admission milestone with no new executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Boot and desktop phase-boundary inventory, ownership map, lifecycle/state framing, implementation admission contract, hardening corrections, Live Validation waivers, PR package history, post-merge canon repair, and merged-unreleased release-debt truth.
Release Artifacts: Tag v1.6.4-prebeta; release title Pre-Beta v1.6.4; rich Markdown release notes summarize the FB-015 boundary model and governance results without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-015 is Released / Closed in v1.6.4-prebeta; FB-029 is also Released / Closed in the same package; FB-030 is Released / Closed in v1.6.5-prebeta; FB-005 is Released / Closed in v1.6.6-prebeta; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Minimal Scope: Complete the bounded docs/canon seam chain for current boot/desktop phase-boundary ambiguity, starting with current boundary inventory and ownership mapping before lifecycle framing or implementation-admission rules are extended.
Summary: Preserve the future boot and desktop phase-boundary model above the already-closed milestone taxonomy work.
Why it matters: Keeps boot-versus-desktop ownership planning explicit without reopening the closed taxonomy milestone by inertia.

#### [Former ID: FB-005] Workspace and folder organization

Status: Released (v1.6.6-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: Low
Release Stage: Released
Target Version: v1.6.6-prebeta
Release Title: Pre-Beta v1.6.6
Deferred Since: v2.0 closeout after the Step 4 workspace slice; the earlier first workspace slice is preserved in v1.9.0 closeout history.
Deferred Because: remaining workspace movement is path-sensitive and can break imports, launcher routes, logs, or user-facing entrypoints if treated as casual cleanup.
Selection / Unblock: Implemented for the first bounded slice. `feature/fb-005-workspace-path-planning` completed the admitted WS-1 relocation `desktop/orin_desktop_test.py` -> `dev/desktop/orin_desktop_test.py`, the branch merged through PR #83, and `v1.6.6-prebeta` is now published and validated.
Branch: feature/fb-005-workspace-path-planning
Canonical Workstream Doc: Docs/workstreams/FB-005_workspace_and_folder_organization.md
Branch Readiness: Complete. The branch objective, target end-state, approved workspace/path slice, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 `desktop/orin_desktop_test.py` -> `dev/desktop/orin_desktop_test.py` is complete. H-1 is complete. LV-1 is complete. The merged branch delivered its first workspace slice under the earlier path-sensitive posture; future FB-005 follow-through should still prefer same-branch slice completion when that lane is reopened.
PR Readiness: Complete. PR-1 merge-target canon completeness, PR-2 selected-next workstream selection, and PR-3 live PR creation plus validation are complete; PR #83 merged into `main` at `873c9b6801802a05bbcef074595e632c0ec9f1d2`.
Release Readiness: Complete. `main` validated green for `v1.6.6-prebeta` release packaging before release execution.
Release Execution: `v1.6.6-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.6-prebeta on commit `deeaa691a79dd01897f6aed82f087970db7019b3`.
Release Target: v1.6.6-prebeta
Release Floor: patch prerelease
Version Rationale: FB-005 delivers a bounded dev-only workspace/path implementation slice and direct path-truth sync with no change to shipped runtime entrypoints, launcher paths, audio paths, logs, visual assets, installer behavior, or user-facing desktop behavior, so patch prerelease remains the correct floor.
Release Scope: the historically released FB-005 WS-1 dev-only desktop test harness relocation from `desktop/orin_desktop_test.py` to `dev/desktop/orin_desktop_test.py`, local path-math preservation, direct workspace-layout truth sync, hardening corrections, Live Validation waivers, PR package history, and release publication for that bounded released slice.
Release Artifacts: Tag v1.6.6-prebeta; release title Pre-Beta v1.6.6; rich Markdown release notes summarize the bounded FB-005 WS-1 workspace slice, validation evidence, non-user-facing release posture, and selected-next planning lane without repeating the release title inside the notes body, and GitHub-generated `## What's Changed` plus `**Full Changelog**:` must be included.
Post-Release Truth: FB-005 is Released / Closed in v1.6.6-prebeta; FB-042 is Released / Closed in `v1.6.7-prebeta`; FB-043 is Released / Closed in `v1.6.8-prebeta`; FB-044 and FB-045 are Released / Closed in `v1.6.9-prebeta`; release debt is clear; and after merge FB-046 becomes the merged-unreleased release-debt owner for `v1.6.10-prebeta`, while FB-047 is selected next, `Registry-only`, and branch-not-created.
Current Active Workstream: None
Branch Readiness Gate: Complete. `v1.6.7-prebeta` is published and validated, updated `main` is revalidated, and FB-043 has completed its bounded runtime-bearing slice chain, Hardening, Live Validation, and PR Readiness.
Minimal Scope: Historical executed slice: complete WS-1 dev-only desktop test harness relocation from `desktop/orin_desktop_test.py` to `dev/desktop/orin_desktop_test.py`, with direct reference sync and no broader workspace movement.
Summary: Continue workspace organization only through explicitly approved path-sensitive slices, beginning with the now-completed dev-only desktop test harness move.
Why it matters: Keeps folder and ownership cleanup deliberate instead of letting it blur into unrelated feature work.

#### [Former ID: FB-004] Future boot orchestrator layer

Status: Released (v1.6.3-prebeta)
Record State: Closed
Registry Class: Support Lane
Priority: High
Release Stage: Slice-staged
Target Version: v1.6.3-prebeta
Release Title: Pre-Beta v1.6.3
Branch: feature/fb-004-future-boot-orchestrator-layer
Canonical Workstream Doc: Docs/workstreams/FB-004_future_boot_orchestrator_layer.md
Branch Readiness: Complete. The branch objective, target end-state, seam families, validation contract, User Test Summary strategy, later-phase expectations, and first Workstream seam are recorded in the canonical workstream doc.
Workstream: WS-1 current boot-to-desktop source map and ownership boundary, WS-2 lifecycle and orchestration-state framing, and WS-3 validation and admission contract are complete.
Hardening: H-1 boot-orchestrator pressure test is complete. Diagnostics-root canon aligns with runtime-root launcher truth, and stale launcher regression helper reuse is repair-gated.
Live Validation: LV-1 repo-truth alignment, user-facing shortcut applicability, User Test Summary applicability, desktop export applicability, cleanup posture, and waiver handling are complete.
PR Readiness: Merge-target canon, post-merge release-debt truth, selected-next workstream truth, PR package details, and live PR validation were recorded before PR #74 merged.
Release Execution: `v1.6.3-prebeta` is live at https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.3-prebeta on commit `9f5ae9a78c7dbff79322089bca370fa49da38598`.
Release Target: v1.6.3-prebeta
Release Floor: patch prerelease
Version Rationale: FB-004 was a docs/canon-only architecture and admission milestone with no executable, runtime, operator-facing, user-facing, or materially expanded product capability.
Release Scope: Future boot-orchestrator source map, lifecycle/state framing, ownership boundaries, diagnostics evidence-root correction, rollback boundaries, stale launcher helper caveat, implementation admission contract, hardening, Live Validation waivers, backlog governance sync, and PR Readiness merge-target canon.
Release Artifacts: Tag v1.6.3-prebeta; release title Pre-Beta v1.6.3; rich Markdown release notes summarize the FB-004 boot-orchestrator planning frame, validation/admission contract, diagnostics-root correction, waiver posture, backlog sync, and selected-next branch gate with GitHub-generated What's Changed and Full Changelog sections.
Post-Release Truth: FB-004 is Released / Closed in v1.6.3-prebeta; release debt is clear; FB-015 Branch Readiness may continue on `feature/fb-015-boot-desktop-phase-boundary-model` after updated-main revalidation and the repo-level admission gate pass.
Summary: Preserved the future top-level boot-orchestrator direction above the desktop launcher without authorizing runtime delivery yet.
Why it matters: Keeps the longer-term boot-to-desktop product direction explicit while current desktop and diagnostics work stays bounded.

## Historical Implemented Registry-Only Items

Old implemented registry-only IDs are preserved as same-file historical trace. They are not selectable backlog items and do not have standalone canonical workstream records unless a later USER-approved family consolidation creates one.

| Former ID | Historical Title | Historical Status | Trace Authority |
| --- | --- | --- | --- |
| `FB-001` | Repeated identical crash early escalation | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-002` | Mixed failure-pattern policy | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-003` | Retry limit and diagnostics escalation policy | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-006` | Threshold-based recovery outcome summary refinement | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-007` | Max-attempt identical-failure attempt-pattern correction | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-008` | Shutdown voice degradation effect | Implemented `v2.2.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-009` | Align crash-origin mixed markers with stable repeated-failure summaries | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-010` | v1.6.0 closeout and documentation sync | Implemented `v1.6.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-011` | Historical memory contract | Implemented `v1.7.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-012` | Failure fingerprint and recurrence model | Implemented `v1.8.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-013` | Advisory provenance and confidence semantics | Implemented `v1.8.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-014` | Multi-run orchestration regression harness | Implemented `v1.8.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-016` | Recorder-only historical memory groundwork | Implemented `v1.7.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-017` | Support bundle and GitHub issue prefill | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-018` | Voice-path regression validation harness | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-019` | Support bundle to repro triage helper | Implemented `v1.9.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-020` | Dev Toolkit utility split and dev-only evidence roots | Implemented `v2.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-021` | Dev-only Boot Jarvis test lane | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-022` | Boot & Transition Checks Dev Toolkit surfacing | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-023` | Desktop renderer observability gap closure | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-024` | Boot harness edge-path observability refinement | Implemented `v2.1.0` | Historical registry trace in `Docs/feature_backlog.md` |
| `FB-026` | Dev Toolkit uploaded-bundle intake surface | Implemented `v2.2.0` | Historical registry trace in `Docs/feature_backlog.md` |

#### [Former ID: FB-001] Repeated identical crash early escalation

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.6.0
Summary: Early launcher escalation for repeated identical non-`STARTUP_ABORT` crash outcomes.
Why it matters: Prevents stable repeated crash evidence from being masked by unnecessary retries.

#### [Former ID: FB-002] Mixed failure-pattern policy

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.6.0
Summary: Conservative launcher handling for mixed crash and abort failure sequences.
Why it matters: Keeps mixed-pattern outcomes classified without overstating them as stronger than repeated identical failures.

#### [Former ID: FB-003] Retry limit and diagnostics escalation policy

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Defined retry exhaustion and diagnostics-entry policy for repeated `STARTUP_ABORT` and repeated identical crash outcomes.
Why it matters: Makes launcher escalation predictable and evidence-based.

#### [Former ID: FB-006] Threshold-based recovery outcome summary refinement

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v1.6.0
Summary: Refined launcher summary wording for threshold-based early escalation outcomes.
Why it matters: Keeps final failed-run reporting aligned with the actual recovery path.

#### [Former ID: FB-007] Max-attempt identical-failure attempt-pattern correction

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v1.6.0
Summary: Corrected final attempt-pattern reporting for max-attempt identical failures.
Why it matters: Prevents stable repeated failures from being described as varied.

#### [Former ID: FB-008] Shutdown voice degradation effect

Status: Implemented (v2.2.0 rev2)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v2.2.0
Summary: Tuned the shutdown-only voice path so the final line sounds more like controlled power loss.
Why it matters: Improves late-shutdown presentation without widening diagnostics behavior.

#### [Former ID: FB-009] Align crash-origin mixed markers with stable repeated-failure summaries

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Low
Target Version: v1.6.0
Summary: Aligned mixed-pattern classification with final repeated-failure summaries when cause stayed identical.
Why it matters: Keeps summary and classification evidence consistent.

#### [Former ID: FB-010] v1.6.0 closeout and documentation sync

Status: Implemented (v1.6.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.6.0
Summary: Historical closeout and documentation sync for the finalized `v1.6.0` orchestration layer.
Why it matters: Preserved the old baseline before later historical-memory work.

#### [Former ID: FB-011] Historical memory contract

Status: Implemented (v1.7.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v1.7.0
Summary: Defined the contract for passive cross-run historical memory before implementation.
Why it matters: Keeps later history and advisory work deterministic and explainable.

#### [Former ID: FB-012] Failure fingerprint and recurrence model

Status: Implemented (v1.8.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v1.8.0
Summary: Defined how recurring outcomes are recognized across launches without reopening closed runtime classification.
Why it matters: Cross-run recurrence needs stable fingerprint rules to stay trustworthy.

#### [Former ID: FB-013] Advisory provenance and confidence semantics

Status: Implemented (v1.8.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.8.0
Summary: Defined provenance and confidence semantics for advisory outputs.
Why it matters: Keeps advisory intelligence explanatory instead of becoming hidden policy.

#### [Former ID: FB-014] Multi-run orchestration regression harness

Status: Implemented (v1.8.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.8.0
Summary: Added a multi-run regression harness for orchestration and historical-memory validation.
Why it matters: Gives repeated-run behavior a bounded regression surface.

#### [Former ID: FB-016] Recorder-only historical memory groundwork

Status: Implemented (v1.7.0)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v1.7.0
Summary: Established recorder-only groundwork for passive historical memory.
Why it matters: Kept early history capture bounded before broader interpretation layers arrived.

#### [Former ID: FB-017] Support bundle and GitHub issue prefill

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Added support-bundle creation and issue-prefill groundwork around diagnostics workflows.
Why it matters: Improved manual triage and reporting without automatic submission.

#### [Former ID: FB-018] Voice-path regression validation harness

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Added bounded regression coverage for voice-path behavior.
Why it matters: Protects shutdown and diagnostics voice behavior from silent regression.

#### [Former ID: FB-019] Support bundle to repro triage helper

Status: Implemented (v1.9.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v1.9.0
Summary: Added a helper path for turning support-bundle artifacts into reproducible triage input.
Why it matters: Improves internal debugging flow without changing product behavior.

#### [Former ID: FB-020] Dev Toolkit utility split and dev-only evidence roots

Status: Implemented (v2.0 rev2)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v2.0
Summary: Split Dev Toolkit utilities and formalized dev-only evidence roots.
Why it matters: Keeps internal debugging surfaces structured and separate from live runtime logs.

#### [Former ID: FB-021] Dev-only Boot Jarvis test lane

Status: Implemented (v2.1.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v2.1.0
Summary: Added the first dev-only boot test lane for controlled boot-path validation.
Why it matters: Made boot-path validation explicit and reusable inside the toolkit surface.

#### [Former ID: FB-022] Boot & Transition Checks Dev Toolkit surfacing

Status: Implemented (v2.1.0 rev2)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v2.1.0
Summary: Surfaced Boot and Transition Checks inside the Dev Toolkit.
Why it matters: Made transition validation easier to run without ad hoc helper discovery.

#### [Former ID: FB-023] Desktop renderer observability gap closure

Status: Implemented (v2.1.0 rev3)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: High
Target Version: v2.1.0
Summary: Closed key renderer observability gaps needed for desktop-startup investigation.
Why it matters: Strengthened evidence quality for renderer-owned behavior without broad redesign.

#### [Former ID: FB-024] Boot harness edge-path observability refinement

Status: Implemented (v2.1.0 rev4)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v2.1.0
Summary: Refined boot-harness observability for edge-path behavior.
Why it matters: Improved branch and validation clarity for boot edge cases.

#### [Former ID: FB-026] Dev Toolkit uploaded-bundle intake surface

Status: Implemented (v2.2.0 rev1)
Record State: Registry-only
Registry Class: Historical Implemented Registry-Only
Priority: Medium
Target Version: v2.2.0
Summary: Added a dedicated Dev Toolkit intake surface for uploaded support bundles and extracted folders.
Why it matters: Makes internal bundle triage feel like one coherent tooling surface.
