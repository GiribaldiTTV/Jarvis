# FB-047 Active-Session Relaunch Decline Preservation

## Identity

- ID: `FB-047`
- Title: `Active-session relaunch decline session-preservation proof`

## Record State

- `Promoted`

## Status

- `In Progress`

## Canonical Branch

- `feature/fb-047-active-session-relaunch-decline-preservation`

## Current Phase

- Phase: `Workstream`

## Phase Status

Repo State: `Active Branch`
Current Active Branch: `feature/fb-047-active-session-relaunch-decline-preservation`
Current Active Canonical Workstream Doc: `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
Latest Public Prerelease: `v1.6.10-prebeta`
Latest Public Release Commit: `36cf07495dc8e239b20b11afb5194355b77ffd8b`
Latest Public Prerelease Publication: `https://github.com/GiribaldiTTV/Nexus-Desktop-AI/releases/tag/v1.6.10-prebeta`
Latest Public Prerelease Title: `Pre-Beta v1.6.10`
FB-046 is `Released / Closed` historical proof in `v1.6.10-prebeta`.
Release debt is clear after publication, validation, and post-release canon closure.
FB-047 is now the active promoted workstream on this branch.
WS-1 is complete / validated, `Backlog Completion State` is `Implemented Complete`, and `Hardening` is next.
Active seam: `None.`

## Branch Class

- `implementation`

## Blockers

None.

## Entry Basis

- `v1.6.10-prebeta` is published and validated on commit `36cf07495dc8e239b20b11afb5194355b77ffd8b`.
- FB-046 is live released, and merged-unreleased release debt is clear after publication, validation, and post-release canon closure.
- Accepted relaunch is already proven end to end across shutdown, single-instance release, guard reacquisition, replacement-session settled re-entry, and truthful post-settled lifecycle handling.
- What was still missing was equally truthful proof for the complementary decline lane: when an incoming launch reaches an already-settled active session and replacement is declined, the repo needed to prove that the active session stays owner, the incoming launch exits cleanly, and no replacement-session markers leak into that path.

## Exit Criteria

- declined relaunch is proven end to end across launcher path, single-instance guard truth, and reusable validators
- the active settled session remains owner and unchanged while incoming launches are declined
- incoming declined launches exit truthfully without replacement-session activation, settled, or guard-release markers
- repeated incoming declined launches stay single-owner and do not widen into dual-ownership ambiguity
- the branch does not leave `Workstream` until FB-047 records `Backlog Completion State`

## Rollback Target

- `Workstream`

## Next Legal Phase

- `Hardening`

## Purpose / Why It Matters

FB-047 exists to make relaunch decline just as truthful as accepted relaunch. The runtime already knew how to keep the current session when replacement was declined, but the repo still described that path too loosely. The remaining job was to stop treating it like a generic already-running skip and prove the exact outcome: the active settled session stayed owner, the incoming launch exited cleanly, and no replacement-session lifecycle markers were emitted.

## Scope

- bounded declined-relaunch lifecycle refinement across `desktop/single_instance.py`, `desktop/orin_desktop_launcher.pyw`, and `dev/orin_desktop_entrypoint_validation.py`
- reusable validation proof that the active session remains owner while repeated incoming declined launches exit truthfully
- direct canon updates needed to promote FB-047 into active workstream truth and preserve the historical FB-046 Branch Readiness record
- for FB-047, `bounded` describes scope and blast radius, not partiality; this branch is the full currently implementable FB-047 runtime/user-facing pass unless a later canon change explicitly broadens FB-047 or a new backlog item is opened

## Non-Goals

- no `main.py` ownership rewrite
- no `Audio/` changes
- no `logs/` ownership changes
- no `jarvis_visual/` relocation or reorganization
- no installer or shortcut-registration redesign
- no broader boot-orchestrator implementation
- no accepted-relaunch semantics rewrite beyond preserving already-green proof

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing`
Docs-Only Workstream: `No`
Planning-Loop Bypass User Approval: `None`
Planning-Loop Bypass Reason: `None`

- FB-047 remains a real runtime/user-facing implementation lane and must not collapse back into planning-only narration.

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

- WS-1 is the first completed FB-047 slice, not a branch cap.
- Additional FB-047 slices would continue on this same branch if more implementable relaunch-decline work remained.
- For the current FB-047 definition, that continuation rule is now satisfied: no additional implementable FB-047 runtime slices remain on this branch.

## Backlog Completion Status

Backlog Completion State: `Implemented Complete`
Remaining Implementable Work: `None`
Future-Dependent Blockers: `None`

- This branch now represents the full currently implementable FB-047 runtime/user-facing pass.
- Future relaunch-decline or ownership issues should create a new backlog item or explicitly broaden FB-047 in source truth before more FB-047 slice work is claimed.

## Validation Contract

- run `python -m py_compile desktop\single_instance.py desktop\orin_desktop_launcher.pyw desktop\orin_desktop_main.py dev\orin_desktop_entrypoint_validation.py dev\orin_boot_transition_verification.py`
- run `python dev\orin_desktop_entrypoint_validation.py`
- run `python dev\orin_boot_transition_verification.py`
- run `python dev\orin_branch_governance_validation.py`
- run `git diff --check`
- preserve proof that default launch, accepted relaunch, repeated launch, and explicit dev-boot paths remain green while declined relaunch becomes first-class preserved-session truth

## Artifact History

- `dev/orin_desktop_entrypoint_validation.py`
  - Classification: `Reusable`
  - Purpose: validates canonical production launch paths, accepted relaunch, repeated launch, and now repeated declined incoming-launch preservation proof
  - Reuse: continue extending this helper before creating another overlapping relaunch validator
- `dev/orin_boot_transition_verification.py`
  - Classification: `Reusable`
  - Purpose: proves explicit dev boot still converges on the same authoritative settled truth while relaunch semantics evolve around it
  - Reuse: preserve this helper as the explicit dev-boot truth owner when relaunch ownership changes

## Admitted Implementation Slice

### WS-1 declined relaunch incoming-launch truthful exit proof

- Status: `Complete / validated`
- Goal: prove and refine end-to-end declined relaunch so the active settled session remains owner, incoming launches exit cleanly, and no replacement-session lifecycle markers appear
- Exact Affected Paths:
  - `desktop/single_instance.py`
  - `desktop/orin_desktop_launcher.pyw`
  - `dev/orin_desktop_entrypoint_validation.py`
  - `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md`
  - `Docs/workstreams/index.md`
  - `Docs/feature_backlog.md`
  - `Docs/prebeta_roadmap.md`
  - `Docs/Main.md`
  - `Docs/branch_records/index.md`
  - `Docs/branch_records/feature_fb_047_active_session_relaunch_decline_preservation.md`
  - `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md`

### WS-1 Implementation Results

- `desktop/single_instance.py` now exposes a harness-only auto-decline relaunch path so declined replacement can be exercised without dialog-click masking and without altering production prompt behavior.
- `desktop/orin_desktop_launcher.pyw` now classifies declined replacement as an explicit clean incoming-launch outcome with `RELAUNCH_DECLINED_SESSION_PRESERVED` instead of collapsing that path into the generic `ALREADY_RUNNING` skip marker.
- `dev/orin_desktop_entrypoint_validation.py` now runs a real declined-relaunch cycle with repeated incoming launches and proves:
  - the original session reaches `DESKTOP_OUTCOME|SETTLED|state=dormant`
  - incoming launches detect the single-instance conflict and record decline markers
  - the active session never receives a relaunch request
  - incoming declined launches never emit replacement-session, reacquire, settled, or guard-release markers
  - the preserved active session completes on a truthful clean-shutdown or already-valid post-settled recoverable lane without dual ownership
- Existing accepted-relaunch, repeated-launch, startup, and explicit dev-boot proof paths stayed green.

### WS-1 Validation Results

- `python -m py_compile desktop\single_instance.py desktop\orin_desktop_launcher.pyw desktop\orin_desktop_main.py dev\orin_desktop_entrypoint_validation.py dev\orin_boot_transition_verification.py`: PASS
- `python dev\orin_desktop_entrypoint_validation.py`: PASS
  - report: `dev/logs/desktop_entrypoint_validation/reports/DesktopEntrypointValidationReport_20260426_114807.txt`
- `python dev\orin_boot_transition_verification.py`: PASS
  - report: `dev/logs/boot_transition_verification/reports/BootTransitionVerificationReport_20260426_114236.txt`
- `python dev\orin_branch_governance_validation.py`: PASS
- `git diff --check`: PASS with line-ending normalization warnings only

## Decline Lifecycle Result

Declined relaunch is now a first-class proven lifecycle:

- session 1 reaches `DESKTOP_OUTCOME|SETTLED|state=dormant`
- incoming launch 1 detects active ownership, records decline, and exits cleanly
- incoming launch 2 does the same without changing ownership or emitting replacement-session truth
- the preserved active session remains the sole runtime owner until its own later lifecycle completion

The proof now stops at the right boundary and says what actually happened, rather than implying that a conflict alone is enough to explain the outcome.

## Ownership Integrity

Single-instance ownership remains with the active settled session throughout the decline lane:

- no relaunch request reaches the active session
- no replacement-session reacquire or settled markers appear on incoming declined launches
- no dual ownership or false replacement-session success surface appears during repeated incoming launches

## User Test Summary

User-Facing Shortcut Path: `Pending Live Validation classification`
User-Facing Shortcut Validation: `Pending`
User Test Summary Results: `Pending`

- Workstream proof currently rests on reusable production-path validation and explicit dev-boot proof.
- Live Validation will classify real desktop shortcut applicability and the exact User Test Summary state for this lane.

## Seam Continuation Decision

Continue Decision: `Continue`
Next Active Seam: `Hardening`
Stop Condition: `Stop after FB-047 Hardening only if startup, accepted-relaunch proof, or decline-path ownership truth regresses beyond the admitted runtime/user-facing lane.`
Continuation Action: `Pressure-test the completed decline-preservation pass on this same branch, preserve active-session ownership through repeated declined incoming launches, and keep accepted-relaunch plus default startup proof green.`

## Active Seam

Active seam: `None.`

- WS-1 is complete and validated.
- `Hardening` is now the next legal phase.
