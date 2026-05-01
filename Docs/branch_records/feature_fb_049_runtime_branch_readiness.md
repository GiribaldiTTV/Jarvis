# Branch Authority Record: feature/fb-049-runtime-branch-readiness

## Branch Identity

- Branch: `feature/fb-049-runtime-branch-readiness`
- Workstream: `FB-049`
- Branch Class: `implementation`
- Backlog Record State: `Registry-only`
- Branch Class Note: `runtime-focused backlog candidate`

## Purpose / Why It Exists

This branch is the runtime-focused Branch Readiness surface for FB-049, the selected-next `Registry-only` backlog item.

It also carries the post-merge blocker left after PR #106: `Docs/branch_records/index.md` still listed `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md` as active even though PR #106 merged and its watcher verified merge/shutdown. Per current governance, that stale canon repair must ride inside the next legitimate runtime-focused backlog branch's `Branch Readiness` instead of spawning another repair-only branch.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Repo State: `Active Branch`
- Active Branch: `feature/fb-049-runtime-branch-readiness`
- Branch Authority State: `Active Branch`
- Workstream: `FB-049 Active-session pre-settled incoming-launch conflict truth`
- Backlog Record State: `Registry-only`
- Current Active Canonical Workstream Doc: `None`
- Latest Public Prerelease: `v1.6.12-prebeta`
- Latest Public Release Commit: `b06c359e58b47cfe26fe8c4b39ac04fde519dee9`
- Pending Release Posture: `v1.6.13-prebeta remains the patch prerelease target for merged governance and automation-catalog proof`
- Carried Blocker: `Stale active-branch authority for Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md`
- Carried Blocker Status: `Cleared in BR1 by moving PR105 closeout record to historical-only traceability`
- Selected Next Workstream: `FB-049 Active-session pre-settled incoming-launch conflict truth`
- Selected Next Record State: `Registry-only`
- Selected Next Implementation Branch: `feature/fb-049-runtime-branch-readiness`
- Current Branch Readiness Seam: `BR1 - FB-049 Admission With Carried Post-Merge Blocker`
- Next Active Seam: `Workstream WS1 - Pre-Settled Incoming-Launch Conflict Truth`
- Automation Observability Report: `Strict mode passes; current automation findings are informational only`

## Branch Class

- `implementation`

## Blockers

None. The carried stale active-branch authority blocker is cleared in this Branch Readiness pass, and FB-049 implementation is not started until Workstream.

## Entry Basis

- FB-049 remains selected next, `Registry-only`, and the smallest runtime/user-facing successor after FB-048 because settled-session relaunch now has success, decline, signal-failure, and wait-timeout truth while pre-settled incoming-launch conflicts remain under-proven.
- PR #106 merged into `main` at `2026-05-01T18:21:41Z`.
- The PR #106 same-thread watcher verified `merged=true` at `2026-05-01T18:22:03.963697Z`, emitted the source-of-truth handoff at `2026-05-01T18:22:25.710882Z`, and retired `local-pr106-watch-host`.
- Merged `main` still carried stale active branch authority for `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md`.
- Current governance blocks standalone repair-only branches, so the stale active-branch authority repair is carried by this runtime-focused FB-049 Branch Readiness pass before implementation starts.

## Exit Criteria

- `Docs/branch_records/index.md` lists this FB-049 branch record as the only active branch authority record.
- `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md` is historical-only traceability and no longer active authority.
- Backlog and roadmap current-state surfaces identify this branch as the active FB-049 Branch Readiness surface without claiming Workstream implementation has started.
- The first bounded FB-049 runtime slice is defined with exact affected paths, non-goals, validation expectations, rollback boundary, and same-branch continuation posture.
- Branch governance validation and automation observability strict report are green before Workstream admission.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Workstream`

## Branch Objective

- clear the carried PR106 post-merge stale active-branch authority blocker on the next legitimate runtime-focused backlog branch
- admit FB-049 Branch Readiness without starting implementation
- define the smallest runtime-bearing slice for pre-settled incoming-launch conflict truth
- keep pending `v1.6.13-prebeta` release posture and FB-049 selected-next truth consistent

## Target End-State

- active branch authority belongs to `feature/fb-049-runtime-branch-readiness`
- PR105/PR106 closeout repair proof is historical-only traceability
- FB-049 remains `Registry-only` until Workstream promotion is warranted by implementation execution
- Workstream can begin with a bounded runtime/user-facing slice focused on pre-settled incoming-launch conflict truth
- same-branch backlog completion remains the default unless only future-dependent blockers remain

## Backlog Completion Strategy

Branch Completion Goal: `Complete FB-049 on this same branch unless only future-dependent blockers remain after the pre-settled incoming-launch conflict truth work is exhausted.`
Known Future-Dependent Blockers: `None proven during Branch Readiness.`
Branch Closure Rule: `Do not leave Workstream after WS-1 while more implementable FB-049 work remains; exit Workstream only when Backlog Completion State becomes Implemented Complete or Implemented Complete Except Future Dependency.`

## Affected Surface Ownership

- `desktop/single_instance.py`: startup-phase guard ownership, incoming launch collision classification, and pre-settled ownership truth before authoritative settled is reached
- `desktop/orin_desktop_launcher.pyw`: truthful incoming-launch exit reporting, branch-specific breadcrumbs, and conflict outcome routing before settled-session semantics apply
- `desktop/orin_desktop_main.py`: minimal renderer-side lifecycle markers if proof needs explicit pre-settled ownership state
- `dev/orin_desktop_entrypoint_validation.py`: reusable production-path proof surface for pre-settled incoming-launch conflict truth
- `dev/orin_boot_transition_verification.py`: reusable boot/desktop transition proof alignment if pre-settled lifecycle truth must stay consistent with boot handoff validation

## Expected Seam Families And Risk Classes

- pre-settled incoming-launch collision family; risk class: incoming launch may collide before authoritative settled and get mislabeled as a settled-session relaunch
- startup-phase ownership family; risk class: logs or state may imply ownership transferred or settled when the owning session has not reached authoritative settled
- truthful exit family; risk class: the incoming launch may exit without durable proof that it exited for the correct pre-settled conflict reason
- validation alignment family; risk class: FB-046 through FB-048 settled relaunch proof may be reused too broadly and mask a distinct pre-settled ownership boundary
- carried-canon repair family; risk class: stale branch authority could recur unless active branch records are cleared before implementation and later PR green

## User Test Summary Strategy

- User-facing runtime behavior is expected during Workstream, so Live Validation must plan a real user-facing shortcut or equivalent entrypoint validation path before PR Readiness.
- Branch Readiness does not require a completed User Test Summary because no runtime implementation has started.
- Workstream must define a concrete `## User Test Summary` checklist once the runtime behavior and validation helper evidence exist.

## Later-Phase Expectations

- Workstream must execute the admitted runtime slice before any Hardening or PR Readiness claim.
- Hardening must pressure-test the pre-settled ownership and truthful-exit paths against existing settled-session relaunch proof.
- Live Validation must use real desktop entrypoint evidence where feasible and record User Test Summary status exactly.
- PR Readiness must provision the current-PR watcher on an approved reporting surface, verify bot-review state, keep PR2 merge watch active until `merged=true`, and prevent stale branch authority from escaping after merge.

## Planning-Loop Guardrail

Implementation Delta Class: `runtime/user-facing`
Docs-Only Workstream: `No`
Planning-Loop Bypass User Approval: `None`
Planning-Loop Bypass Reason: `None`

- FB-049 is a runtime-focused implementation branch. The Branch Readiness repair of carried canon drift is allowed only because governance requires it before this runtime branch can start implementation.

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

- WS-1 is the first admitted FB-049 slice, not a branch cap.
- Additional FB-049 slices should continue on this branch whenever they stay inside the same backlog item, branch class, scope family, and validation surface.
- A bounded stop condition or explicit USER-approved split is required before stopping the branch after only WS-1.

## Admitted Implementation Slice

- Slice ID: `WS-1 pre-settled incoming-launch conflict truthful exit proof`
- Goal: prove and refine the path where an incoming launch collides with an already-owning startup-phase session before authoritative settled is reached, so the incoming launch exits truthfully without false settled-session relaunch, guard-transfer, replacement-session, or authoritative-settled claims.
- Runtime/User-Facing Delta: pre-settled incoming-launch conflicts become explicit lifecycle outcomes instead of borrowing settled-session relaunch semantics.
- Exact Affected Paths:
  - `desktop/single_instance.py`
  - `desktop/orin_desktop_launcher.pyw`
  - `desktop/orin_desktop_main.py`
  - `dev/orin_desktop_entrypoint_validation.py`
  - `dev/orin_boot_transition_verification.py`
- In-Scope Paths:
  - `desktop/single_instance.py`
  - `desktop/orin_desktop_launcher.pyw`
  - `desktop/orin_desktop_main.py`
  - `dev/orin_desktop_entrypoint_validation.py`
  - `dev/orin_boot_transition_verification.py`
  - direct branch-authority, backlog, roadmap, and validator updates required to keep FB-049 truth aligned
- Out-Of-Scope Paths:
  - `main.py`
  - `Audio/`
  - `logs/`
  - `jarvis_visual/`
  - installer, packaging, or shortcut-registration redesign
  - broad boot-orchestrator implementation
  - unrelated tray, task, automation, or runtime UX expansion
- Allowed Changes:
  - bounded pre-settled conflict classification and ownership truth work
  - bounded launcher/renderer breadcrumbs needed to prove whether authoritative settled was reached
  - bounded validator changes needed to prove the pre-settled conflict path without cleanup masking
  - direct canon updates required to keep active FB-049 Branch Readiness and later PR truth aligned
- Prohibited Changes:
  - no `main.py` ownership rewrite
  - no audio, logging-system, visual asset, installer, or shortcut-registration redesign
  - no broader boot-orchestrator buildout
  - no settled-session relaunch semantics rewrite outside the minimum needed to distinguish the pre-settled lane

## Initial Workstream Seam Sequence

Seam 1: `WS1-A - Pre-Settled Conflict Surface Inventory`
Goal: identify the exact current code paths, markers, and validators that distinguish startup-phase ownership from authoritative settled-session relaunch.
Scope: inspect and minimally instrument the admitted affected paths only enough to define truthful pre-settled conflict proof.
Non-Includes: no runtime behavior change outside the admitted affected paths, no broader launcher redesign, and no Workstream implementation before Branch Readiness is green.

Seam 2: `WS1-B - Truthful Exit Runtime Proof`
Goal: implement the minimum runtime/user-facing proof that an incoming launch exits for the correct pre-settled conflict reason without false replacement or settled claims.
Scope: bounded implementation across admitted paths plus validator updates required for durable proof.
Non-Includes: no unrelated relaunch-path rewrite, no installer work, and no post-settled outcome expansion beyond distinction from this lane.

Seam 3: `WS1-C - Validation And Evidence Closeout`
Goal: run the reusable validation suite, record evidence, and decide whether additional same-branch FB-049 slices remain.
Scope: validation, branch-authority evidence, User Test Summary planning, and backlog-completion state only.
Non-Includes: no PR creation or Release Readiness work.

## Validation Contract

- run `python -m py_compile desktop\single_instance.py desktop\orin_desktop_launcher.pyw desktop\orin_desktop_main.py dev\orin_desktop_entrypoint_validation.py dev\orin_boot_transition_verification.py dev\orin_branch_governance_validation.py dev\automation_observability_report.py`
- run `python dev\orin_branch_governance_validation.py`
- run `python dev\automation_observability_report.py --strict`
- run `git diff --check`
- during Workstream, run the relevant desktop entrypoint and boot-transition validators before any phase advancement

## Active Seam

Active seam: `BR1 - FB-049 Admission With Carried Post-Merge Blocker`
Next active seam: `Workstream WS1 - Pre-Settled Incoming-Launch Conflict Truth`

- BR1 clears the carried post-merge branch-authority blocker, creates this active FB-049 Branch Readiness record, syncs current-state truth, and admits the first bounded runtime slice for later Workstream execution.

## Seam Continuation Decision

Seam Status: `Green`
Slice Status: `Green`
Completion Status: `Green`
Waiver Status: `None`
Continue Decision: `Stop`
Stop Basis: `Workstream green`
Next Active Seam: `Workstream WS1 - Pre-Settled Incoming-Launch Conflict Truth`
Stop Condition: `Branch Readiness BR1 is complete; runtime implementation has not started.`
Continuation Action: `Begin Workstream WS1 only after a Workstream prompt confirms this branch remains clean, current, and governance-green.`

## Governance Drift Audit

- Governance Drift Found: `Yes`
- Drift Type: `Carried post-merge stale active-branch authority`
- Why Current Canon Failed To Prevent It: PR #106 merged before `Docs/branch_records/index.md` was made merge-stable; the stale active branch record escaped onto merged `main`.
- Required Canon Changes: move `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md` to historical-only traceability, list this FB-049 record as the active branch authority, and keep the repair inside this runtime-focused Branch Readiness pass.
- Whether The Drift Blocks Implementation: `Yes until BR1 repair and validation are green`
- Whether User Confirmation Is Required: `No; USER explicitly admitted FB-049 BR1 with this carried blocker`
- Missing Validator Requirement Check: `None added in BR1; existing merged-main active-branch drift validator caught the blocker`
