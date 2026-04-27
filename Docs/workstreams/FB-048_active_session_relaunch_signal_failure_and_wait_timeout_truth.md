# FB-048 Active-Session Relaunch Signal-Failure And Wait-Timeout Truth

## Identity

- ID: `FB-048`
- Title: `Active-session relaunch signal-failure and wait-timeout truth`

## Record State

- `Promoted`

## Status

- `In Progress`

## Canonical Branch

- `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`

## Current Phase

- Phase: `Workstream`

## Phase Status

Repo State: `Active Branch`
Current Active Branch: `feature/fb-048-active-session-relaunch-signal-failure-and-wait-timeout-truth`
Current Active Canonical Workstream Doc: `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
Latest Public Prerelease: `v1.6.11-prebeta`
Latest Public Release Commit: `4ca70572fbc8033bc96fcd299dd309464e81393a`
Latest Public Prerelease Publication: `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.11-prebeta`
Latest Public Prerelease Title: `Pre-Beta v1.6.11`
FB-047 is `Released / Closed` historical proof in `v1.6.11-prebeta`.
Merged-unreleased release debt is clear after publication, validation, and post-release canon closure.
FB-048 is now the active promoted runtime/user-facing workstream on this branch.
Active seam: `None.` H-1 is complete and `Live Validation` is next.

## Branch Class

- `implementation`

## Blockers

None.

## Entry Basis

- `v1.6.11-prebeta` is published and validated on commit `4ca70572fbc8033bc96fcd299dd309464e81393a`.
- FB-047 is released and closed, and merged-unreleased release debt is clear after post-release canon closure.
- Accepted relaunch success and declined relaunch preservation are already first-class proven surfaces.
- What was still missing was equally truthful proof for the accepted incoming-launch failure lane when relaunch signaling fails or the active session does not release before the reacquire wait deadline.

## Exit Criteria

- accepted relaunch signal-failure and wait-timeout lanes are proven end to end across launcher path, single-instance ownership truth, and reusable validators
- active-session ownership remains truthful in failure and timeout lanes
- incoming failure-path launches emit explicit preserved-session markers and never emit false replacement-session markers
- repeated and mixed launch scenarios distinguish failure, decline, and success without ownership drift
- the branch does not leave `Workstream` until FB-048 records `Backlog Completion State`

## Rollback Target

- `Workstream`

## Next Legal Phase

- `Live Validation`

## Purpose / Why It Matters

FB-048 exists to make accepted relaunch failure as explicit as accepted relaunch success and declined relaunch preservation. The runtime already knew when a signal failed or when a replacement launch timed out waiting for release, but the launcher still flattened those lanes into a generic already-running story. This workstream turns those outcomes into first-class lifecycle truth with explicit ownership-preserved markers and reusable proof.

## Scope

- bounded accepted-relaunch failure refinement across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, `desktop/orin_desktop_main.py`, and `dev/orin_desktop_entrypoint_validation.py`
- reusable validator proof for repeated signal-failure launches, accepted wait-timeout, and mixed failure-then-success relaunch sequencing
- direct canon updates needed to promote FB-048 into active workstream truth and preserve the historical FB-048 Branch Readiness record
- for FB-048, `bounded` describes scope and blast radius, not partiality; this branch is the full currently implementable FB-048 runtime/user-facing pass unless a later canon change explicitly broadens FB-048 or a new backlog item is opened

## Non-Goals

- no `main.py` ownership rewrite
- no `Audio/` changes
- no `logs/` ownership changes
- no `jarvis_visual/` relocation or reorganization
- no installer or shortcut-registration redesign
- no broader boot-orchestrator implementation
- no rewrite of already-green accepted-success or decline-preservation semantics beyond keeping their proof aligned

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing`
Docs-Only Workstream: `No`
Planning-Loop Bypass User Approval: `None`
Planning-Loop Bypass Reason: `None`

- FB-048 remains a real runtime/user-facing implementation lane and must not collapse into planning-only narration.

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

- WS-1 is the first completed FB-048 slice, not a branch cap.
- Additional FB-048 slices would continue on this same branch if more implementable relaunch-failure work remained.
- For the current FB-048 definition, that continuation rule is now satisfied: no additional implementable FB-048 runtime slices remain on this branch.

## Backlog Completion Status

Backlog Completion State: `Implemented Complete`
Remaining Implementable Work: `None`
Future-Dependent Blockers: `None`

- This branch now represents the full currently implementable FB-048 runtime/user-facing pass.
- Future relaunch-failure or timeout work should create a new backlog item or explicitly broaden FB-048 in source truth before more FB-048 slice work is claimed.

## Validation Contract

- run `python -m py_compile desktop\single_instance.py desktop\orin_desktop_launcher.pyw desktop\orin_desktop_main.py dev\orin_desktop_entrypoint_validation.py dev\orin_boot_transition_verification.py`
- run `python dev\orin_desktop_entrypoint_validation.py`
- run `python dev\orin_boot_transition_verification.py`
- run `python dev\orin_branch_governance_validation.py`
- run `git diff --check`
- preserve proof that default launch, accepted relaunch success, declined relaunch preservation, repeated launch, and explicit dev-boot paths remain green while accepted relaunch failure becomes first-class truthful outcome proof

## Artifact History

- `dev/orin_desktop_entrypoint_validation.py`
  - Classification: `Reusable`
  - Purpose: validates canonical production launch paths, accepted relaunch success, declined relaunch preservation, and now accepted relaunch signal-failure plus wait-timeout truth
  - Reuse: continue extending this helper before creating another overlapping relaunch validator
- `dev/orin_boot_transition_verification.py`
  - Classification: `Reusable`
  - Purpose: proves explicit dev boot still converges on the same authoritative settled truth while relaunch semantics evolve around it
  - Reuse: preserve this helper as the explicit dev-boot truth owner when relaunch ownership changes

## Admitted Implementation Slice

### WS-1 accepted relaunch failure-path truthful outcome proof

- Status: `Complete / validated`
- Goal: prove and refine end-to-end accepted relaunch failure so signal-failure or wait-timeout outcomes preserve the active session truthfully, emit explicit preserved-session result markers, and never overclaim replacement-session ownership
- Exact Affected Paths:
  - `desktop/single_instance.py`
  - `desktop/orin_desktop_launcher.pyw`
  - `desktop/orin_desktop_main.py`
  - `dev/orin_desktop_entrypoint_validation.py`
  - `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
  - `Docs/workstreams/index.md`
  - `Docs/feature_backlog.md`
  - `Docs/prebeta_roadmap.md`
  - `Docs/Main.md`
  - `Docs/branch_records/index.md`
  - `Docs/branch_records/feature_fb_048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
  - `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`

### WS-1 Implementation Results

- `desktop/single_instance.py` now exposes harness-only relaunch signal-failure, relaunch wait override, and already-running dialog suppression hooks so accepted failure lanes can be proven without changing production prompt behavior.
- `desktop/orin_desktop_main.py` now exposes a harness-only relaunch-request ignore path so wait-timeout can be exercised while the active session truthfully remains owner.
- `desktop/orin_desktop_launcher.pyw` now classifies accepted relaunch failure as explicit preserved-session outcomes with:
  - `STATUS|WARNING|LAUNCHER_RUNTIME|RELAUNCH_SIGNAL_FAILED_SESSION_PRESERVED`
  - `STATUS|WARNING|LAUNCHER_RUNTIME|RELAUNCH_WAIT_TIMEOUT_SESSION_PRESERVED`
  instead of collapsing those lanes into the generic `ALREADY_RUNNING` skip marker.
- `dev/orin_desktop_entrypoint_validation.py` now proves:
  - repeated accepted relaunch signal-failure launches preserve the active settled owner and emit explicit failure markers
  - accepted relaunch wait-timeout preserves the active owner even after the request is received and ignored
  - mixed signal-failure then accept sequencing keeps failure, decline, and success classification distinct instead of blurring them into one ownership story
- Existing startup, accepted-success relaunch, declined-relaunch preservation, repeated-launch, and explicit dev-boot proof paths stayed green.

### WS-1 Validation Results

- `python -m py_compile desktop\single_instance.py desktop\orin_desktop_launcher.pyw desktop\orin_desktop_main.py dev\orin_desktop_entrypoint_validation.py dev\orin_boot_transition_verification.py`: PASS
- `python dev\orin_desktop_entrypoint_validation.py`: PASS
  - report: `dev/logs/desktop_entrypoint_validation/reports/DesktopEntrypointValidationReport_20260427_045829.txt`
- `python dev\orin_boot_transition_verification.py`: PASS
  - report: `dev/logs/boot_transition_verification/reports/BootTransitionVerificationReport_20260427_045851.txt`
- `python dev\orin_branch_governance_validation.py`: PASS
- `git diff --check`: PASS with line-ending normalization warnings only

## Failure Lifecycle Result

Accepted relaunch failure is now a first-class proven lifecycle:

- if signal delivery fails, the incoming launch records explicit signal-failure preserved-session truth and exits cleanly without claiming replacement ownership
- if the active session receives the request but does not release before the reacquire deadline, the incoming launch records explicit wait-timeout preserved-session truth and exits cleanly without claiming replacement ownership
- repeated failure attempts preserve the same settled owner
- later accepted relaunch success still transfers ownership only when guard release and reacquisition actually happen

## Ownership Integrity

Single-instance ownership stays truthful across failure, decline, and success lanes:

- signal-failure launches never deliver a relaunch request to the active session
- wait-timeout launches may deliver a relaunch request, but the active session can remain owner without shutdown, release, or replacement markers
- failure-path incoming launches never emit replacement-session active, settled, reacquire, or guard-release markers
- accepted relaunch transfer remains isolated to the actual success lane

## H-1 Hardening Record

H-1 pressure-tested the completed FB-048 accepted-failure lane across rapid repeated signal-failure launches, wait-window boundary classification, preserved-session marker timing, single-instance ownership under failure and timeout stress, mixed failure/decline/accept/failure sequencing, and validator classification consistency without widening beyond the admitted runtime/user-facing surfaces.

### Hardening Findings

- Rapid consecutive signal-failure launches remain single-owner: the active settled session stays unchanged, each incoming launch records accepted conflict plus explicit signal-failure preserved-session truth, and no reacquire or replacement-session markers leak into the failed incoming launches.
- Wait-window classification is now stable at the boundary: early release before the deadline reacquires truthfully, exact-boundary release no longer falls through to a false timeout because the guard now gets one final reacquire attempt at the deadline, and late release still resolves to the explicit wait-timeout preserved-session outcome.
- Mixed failure -> decline -> accept -> failure sequencing stays truthful: failure preserves the original owner, decline preserves the same owner without relaunch request delivery, accepted relaunch is still the only lane that transfers guard ownership, and a later failure against the accepted replacement session preserves that replacement owner without triggering another guard transfer.
- The main hidden coupling was in the single-instance wait-loop boundary itself and in validator breadth, not in launcher classification. The launcher already emitted the right preserved-session markers once the boundary reacquire logic and mixed-sequence proof were tightened.
- Accepted-success relaunch proof, declined-preservation proof, repeated-launch proof, default startup proof, and explicit dev-boot proof all remained green while the failure/timeout hardening surface expanded.

### Hardening Corrections

- `desktop/single_instance.py` now sleeps only up to the remaining relaunch wait window and performs one final reacquire attempt at the deadline before classifying the incoming launch as a wait-timeout preserved-session outcome.
- `dev/orin_desktop_entrypoint_validation.py` now adds reusable coverage for:
  - focused single-instance early / exact-boundary / late wait-window classification
  - three rapid consecutive accepted relaunch signal-failure launches
  - mixed failure -> decline -> accept -> failure relaunch sequencing
- No broader runtime correction was needed in `desktop/orin_desktop_launcher.pyw` or `desktop/orin_desktop_main.py`; the launcher failure/timeout outcome model itself held under the new pressure tests once the wait boundary stopped over-timing out.

### H-1 Completion Decision

- H-1 Result: `Complete / green`
- Remaining implementable work inside FB-048: `None`
- Stop condition: phase boundary reached; Hardening is complete after H-1.

### H-1 Validation Results

- `python -m py_compile desktop\single_instance.py desktop\orin_desktop_launcher.pyw desktop\orin_desktop_main.py dev\orin_desktop_entrypoint_validation.py dev\orin_boot_transition_verification.py`: PASS
- `python dev\orin_desktop_entrypoint_validation.py`: PASS
  - report: `dev/logs/desktop_entrypoint_validation/reports/DesktopEntrypointValidationReport_20260427_072445.txt`
- `python dev\orin_boot_transition_verification.py`: PASS
  - report: `dev/logs/boot_transition_verification/reports/BootTransitionVerificationReport_20260427_072001.txt`
- `python dev\orin_branch_governance_validation.py`: PASS
- `git diff --check`: PASS with line-ending normalization warnings only

### H-1 Stability Notes

- Near-deadline accepted relaunch release no longer risks a false wait-timeout classification just because the last poll slept past the boundary.
- Failure-path incoming launches still never emit replacement-session active, settled, reacquire, or guard-release markers.
- Guard transfer remains exclusive to accepted relaunch success; failure, timeout, and decline lanes all preserve the current active owner even under mixed sequencing.
- The shipped startup path, accepted-success relaunch proof, declined-preservation proof, repeated-launch proof, and explicit dev-boot proof remain green after the added failure/timeout hardening coverage.

## User Test Summary

Not yet classified. FB-048 is still pre-Live-Validation; exact User Test Summary status belongs to the later Live Validation pass if the branch advances.

## Seam Continuation Decision

Continue Decision: `Advance after H-1 because backlog completion is implemented complete, hardening is green, and the next legal phase is Live Validation`
Next Active Seam: `FB-048 Live Validation`
Stop Condition: `Reached Live Validation gate after H-1 completion`
Continuation Action: `Validate repo-truth alignment, user-facing shortcut applicability, exact User Test Summary state, production launch path, explicit dev-boot proof, and hardened failure/timeout proof on the active branch`

## Active Seam

Active seam: `None.`

- WS-1 is complete and validated.
- H-1 is complete and green.
- `Backlog Completion State` is `Implemented Complete`.
- `Live Validation` is the next legal phase.
