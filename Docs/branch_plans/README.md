# Branch Runtime Engineering Plans

`Docs/branch_plans/<branch_slug>.md` is the source-truth home for a runtime-focused branch's active Branch Runtime Engineering Plan.

Docs Source-Truth Reform Model: Compact Pointer Layer.

This layer sits under the branch authority record. It does not replace the branch authority record, backlog, roadmap, or canonical workstream doc.
Codex reaches this layer through the Main-first loader chain: load `Docs/Main.md`, then the governing phase/vision/branch authority owners, then the active branch plan for branch-local engineering detail.

## Ownership Model

- Backlog entries remain compact registry, status, and pointer surfaces.
- Roadmap entries remain compact stage-breakpoint schedule and milestone-checkpoint reference surfaces.
- Branch authority records remain control surfaces for branch identity, phase, approvals, blockers, and legal next phase.
- Branch Runtime Engineering Plans own detailed active-branch runtime execution planning for the current branch/worktree.
- Canonical workstream docs and family dossiers receive durable promoted lessons only after PR Readiness fold-down decides what should survive beyond the active branch.

## Required Runtime Plan Markers

Runtime-focused plans must include:

- Plan Identity:
- Owning Branch:
- Worktree Path:
- Branch Authority Record Pointer:
- Current Phase:
- Branch Runtime Engineering Plan:
- Engineering Plan Status:
- Current Runtime Baseline:
- Branch Purpose:
- Planned Runtime Delta:
- User-Facing Delta:
- Source-Truth Delta:
- State / Config / Schema Delta:
- Validator / Helper Delta:
- Expected Changed Files / Surfaces:
- Workstream / Seam Map:
- Per-Seam Implementation Checklist:
- Per-Seam Validation Checklist:
- Per-Seam User-Facing Proof Checklist:
- Future-Gated Items:
- Approval-Boundary Audit:
- FAM / Shared-Surface Overlap Forecast:
- Open Questions:
- USER Planning Decisions:
- Plan Revision History:
- Plan-To-Implementation Traceability Table:
- Hardening Comparison Checklist:
- Live Validation Proof Or Waiver Checklist:
- PR Readiness Fold-Down / Retention Checklist:
- Release Readiness Public-Scope Translation Checklist:
- USER Planning Review:
- PR Fold-Down Packet:
- Runtime Implementation Approval:

## Element-to-Phase Proof Matrix

Runtime/user-facing branches that plan, create, touch, affect, defer, or preserve product/runtime/UI/source-truth/helper/workflow elements must include a USER-reviewable `## Element-to-Phase Proof Matrix` before Workstream implementation begins or resumes.

The matrix extends the active Branch Runtime Engineering Plan and points to the existing Element Validation Ledger owner. It proves the planned Workstream implementation path, Workstream proof path, Hardening proof path, Live Validation proof or waiver path, UTS / USER acceptance path, and current/future boundary for every element before implementation begins. It must not create a new global ledger or duplicate backlog, roadmap, worktree-slot, or Main live state.

Matrix markers:

- Matrix Status: allowed values are `Required`, `Present`, `Accepted`, `Blocked`, `Folded`, `Historical`, or `Not Required with reason`
- USER Review Status: allowed values are `Pending`, `Accepted`, `Revised`, `Waived`, or `Needs USER Decision`
- Open Element Questions: allowed values are `None`, `Queued`, `Blocking`, or `Deferred With Waiver`
- Element Coverage Owner: must name the active `Docs/branch_plans/<branch_slug>.md` owner before implementation, or a concrete folded source-truth owner after PR Readiness
- Element Validation Ledger Owner: must name the concrete Element Validation Ledger owner path or source-truth owner

Required table shape:

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed `Element Classification` values are `Planned`, `Created`, `Touched`, `Affected`, `Deferred`, `Future`, `Dependency-Only`, and `Non-Gating Supporting`.

Every planned/current created/touched/affected user-facing, runtime, UI, provider, validation/helper, source-truth, or workflow element must name a Workstream implementation path, Workstream proof path, Hardening proof path, Live Validation proof or waiver path, and UTS / USER acceptance path before Workstream implementation begins or resumes. Future/deferred/dependency-only/non-gating elements must name the boundary that keeps them out of current release gating. Element IDs must be unique inside the matrix. Missing or incomplete matrix coverage blocks Workstream entry or continuation on `Element-to-Phase Proof Matrix Missing` or `Element-to-Phase Proof Path Missing`.

## Workstream Entry Review Bundle

`Workstream Entry` is the pre-implementation review gate inside the `Workstream` phase. It is not a separate canonical phase, but it must produce USER-reviewable evidence before implementation begins or resumes.

Before USER can green-light Workstream implementation, Codex must return a full, non-compacted Workstream Entry Review Digest and create or refresh the active worktree's Desktop `USER Review Desktop Bundle` under the stable `Nexus USER Review\<worktree-label>` root.

The bundle should copy the branch vision and planning files the USER needs to inspect, including:

- active Branch Runtime Engineering Plan or Branch Engineering Plan
- Branch Vision Contract Snapshot owner
- Element-to-Phase Proof Matrix owner
- branch authority record
- relevant Nexus Vision and family vision files
- relevant UFD, Branch Change Intent Ledger, source-truth owner, validator/helper, fixture, or planning files

The bundle must use the active worktree label, copy the selected files flat into that worktree folder, and rely on `START_HERE.md` to map copied filenames back to repo-relative source paths. The digest must report the review folder path, copied files, source branch, source HEAD, validation summary, exact Workstream green-light decision requested, and pending USER decisions. Missing bundle proof blocks Workstream entry on `Workstream Entry Review Bundle Missing`.

## USER Branch Plan Review Gate

`USER Branch Plan Review Gate` is the named USER-facing Workstream Entry checkpoint. It wraps the active branch plan, Branch Vision Contract Snapshot, Element-to-Phase Proof Matrix, Workstream Entry whole-package analysis, Hardening plan, Live Validation / UTS plan, UFD items, and Branch Change Intent Ledger when present into a plain-language review packet before Workstream implementation begins or resumes.

Required review markers:

- USER Branch Plan Review:
- Review Status:
- Desktop Review Bundle:
- USER Review Packet Finding:
- Plain-Language Branch Goal:
- Planned User-Facing Outcome:
- Visual / Behavioral Description:
- Implementation Breakdown:
- Element-to-Phase Proof Matrix:
- Hardening Plan:
- Live Validation / UTS Plan:
- Open USER Questions:
- Codex Recommendations:
- Alternatives / Tradeoffs:
- Accepted Scope:
- Deferred Scope:
- Rejected Scope:
- Exact USER Decision Needed:
- Implementation Approval:

`Review Status:` must use `Accepted by USER`, `Revised by USER`, `Deferred With Waiver`, `Rejected by USER`, or `Needs USER Decision`. The packet must give USER answer paths to accept the recommendation, revise it with USER-written changes, defer/future-package/waive with reason, reject it, or request more analysis. It is a review wrapper, not a duplicate permanent ledger; accepted answers fold into the Branch Vision Contract Snapshot, Branch Runtime Engineering Plan, UFD item, matrix row, or branch record only through a later USER-approved digest/source-truth pass.

Missing or shallow branch goal, user-facing outcome, implementation breakdown, Hardening plan, Live Validation / UTS plan, Desktop review bundle proof, `USER Review Packet Finding:`, or exact USER decision blocks Workstream implementation on `USER Branch Plan Review Missing`. A Desktop USER Review Packet that is stale against current `HEAD`, not loaded, not digested, missing `START_HERE.md`, missing `USER_BRANCH_PLAN_REVIEW.md`, missing the exported zip when required, or not explicitly waived blocks on `USER Review Packet Stale` or `USER Review Packet Not Digested`. A first-seam-only packet cannot satisfy this gate when multiple slices or seams are admitted.

## Workstream Entry Whole-Package Analysis Gate

Runtime-focused branch plans with multiple admitted slices or seams must support whole-package Workstream Entry analysis before implementation begins or resumes.

The active Branch Runtime Engineering Plan must let the Workstream Entry packet identify:

- all admitted slices/seams
- completion strategy for the whole Workstream package
- first-seam recommendation
- seam dependency map
- future-gated or non-included scope
- preservation surfaces
- validation plan
- Hardening H1 expectations
- Live Validation LV1 expectations
- visual/user-facing proof requirements
- UTS handoff criteria
- exact implementation approval text

First-seam selection alone is not enough. A Workstream Entry packet may recommend the first bounded implementation seam, but it must also prove that seam fits the full admitted branch package and does not create drift against later admitted seams. Missing whole-package analysis blocks Workstream entry on `Workstream Entry Whole-Package Analysis Missing`. This gate plans Hardening and Live Validation obligations; it does not authorize executing Hardening, Live Validation, UTS handoff, PR creation, merge, release work, or runtime implementation without the separately legal phase approval.

## Vision Contract Snapshot Markers

Runtime/user-facing branches that affect product behavior, UI/UX, workflow hierarchy, visual standards, setup/activation behavior, provider/model/memory/voice/Core behavior, acceptance criteria, or any design assumption must include a Branch Vision Contract Snapshot before Workstream implementation.

Small docs-only, metadata-only, release-body-format, typo/format, or validator-only branches may record `Vision Contract Required: No` with a reason when there is no product, runtime, or user-facing impact.

Branch Vision Contract Snapshot markers:

- Vision Contract Required:
- Vision Contract Requirement Reason:
- Branch Vision Snapshot Status:
- Open Vision Questions:
- USER Vision Green:
- Implementation Scope:
- Seam Map:
- Stop Conditions:
- Design Assumption Ledger:
- Vision Question Queue:
- Question Severity Policy:
- Vision-to-Implementation Traceability:
- Branch Plan Revision Packet:

Allowed design assumption decision states:

- Proposed by Codex
- Recommended by ChatGPT
- Accepted by USER
- Revised by USER
- Rejected by USER
- Deferred by USER
- Deferred With Waiver
- Superseded
- Needs USER Decision

Only `Accepted by USER`, `Revised by USER`, or `Deferred With Waiver` design states are implementation-safe for user-facing/runtime behavior. Codex and ChatGPT recommendations remain proposed evidence until USER accepts, revises, rejects, defers, waives, or supersedes them.

`USER Vision Green: Yes` means the branch may implement the accepted branch plan without repeatedly reopening broad design unless new repo truth triggers a Level 2 or Level 3 vision question.

Vision update ownership follows the `Vision Update Decision Matrix` in `Docs/phase_governance.md`: branch-specific or unresolved ideas stay in the active branch plan, reusable USER-accepted family standards fold into family vision or family dossiers, and project-wide USER-accepted standards fold into `Docs/nexus_vision.md`. Codex must not promote proposed or unresolved ideas into durable vision owners by inference.

Question severity:

- Level 1 - Non-blocking question: record in the vision/question queue, continue using the accepted plan, and return at the next appropriate review point.
- Level 2 - Seam-blocking question: pause the affected seam, return a Vision Question Digest, and continue unaffected areas only when the plan and source truth support that path.
- Level 3 - Workstream-breaking question: return a Branch Plan Revision Packet and require USER decision before continuing affected Workstream scope.

Vision Question Digest fields:

- Question
- Why it matters
- Affected branch/seam
- Current accepted vision
- Codex recommendation
- Alternative options
- Risk of each option
- Whether work can continue without this answer
- Recommended USER decision
- Exact USER decision needed

Branch Plan Revision Packet fields:

- Current accepted plan
- Discovered issue
- Why current plan is insufficient
- Proposed revision
- Affected seams
- Files/surfaces affected
- Validation impact
- Whether this stays in current Workstream
- Whether this moves to future branch
- Codex recommendation
- Exact USER decision needed

## USER Feedback Disposition Markers

`USER Feedback Disposition` is the active branch-plan mechanism for preserving meaningful USER feedback without creating another permanent feedback ledger.

Meaningful feedback requires a UFD item when it affects branch scope, accepted vision, user-facing behavior, runtime behavior, validation proof, future work, reusable product standards, approval boundaries, or a USER decision.

Minor comments, acknowledgements, typo-level notes, duplicate remarks, or non-actionable conversation may close with no durable UFD item only when Codex records the no-action reason in the active branch plan or return digest.

Minimum UFD ledger markers:

- USER Feedback Disposition Required:
- UFD Ledger Status:
- UFD Ledger Owner:
- Open UFD Count:
- Blocking UFD Count:
- Fold-Down Status:

Each meaningful feedback item uses a repeatable `### UFD Item: UFD-<scope>-YYYYMMDD-NNN` block.

Minimum UFD item markers:

- Feedback ID:
- Feedback Summary:
- Feedback Source:
- Feedback Phase:
- Disposition Type:
- USER Decision State:
- Owner Class:
- Canonical Owner File:
- Workstream Severity:
- Status:
- Fold-Down Target:
- Pointer Locations:

Allowed UFD decision states:

- Proposed by Codex
- Recommended by ChatGPT
- Accepted by USER
- Revised by USER
- Rejected by USER
- Deferred by USER
- Deferred With Waiver
- Superseded
- Needs USER Decision

Allowed UFD ledger status values:

- Open
- Queued
- Blocking
- Closed
- Folded Down
- Deferred
- Superseded
- Pending
- Complete
- Not Required
- Not Applicable

Allowed UFD item status values:

- Open
- Queued
- Blocking
- Closed
- Folded Down
- Deferred
- Superseded

Allowed UFD owner classes:

- Branch Plan
- Branch Record
- Backlog Pointer
- Roadmap Pointer
- Nexus Vision
- Family Vision / Dossier
- Workstream Doc
- Governance Receipt
- No Durable Owner Needed

`No Durable Owner Needed` is valid only when the item is closed as minor/no-action, duplicate, superseded, or non-actionable, with `No-Action Reason:` recorded in the active branch plan or return digest.

Pointer locations may carry UFD ID, short title, canonical owner, compact status, and fold-down status only. They must not carry full feedback text, full decision history, or live implementation state.

UFD IDs use `UFD-<scope>-YYYYMMDD-NNN`. Do not use `FBK-*`, because it collides visually with historical `FB-###` workstream records.

## USER Feedback Disposition Fold-Down

At PR Readiness, every UFD item must be migrated, deferred with waiver, rejected/no-action with reason, closed, or explicitly carried to a future owner.

The fold-down receipt must preserve a lookup path from every UFD ID to its final owner after branch-plan fold-down and retirement.

Branch records carry compact UFD status and pointers only. Backlog carries future-candidate pointers only after USER accepts the future-work disposition. Nexus Vision and family vision owners receive only accepted reusable standards, not branch-local unresolved feedback.

## Branch Change Intent Ledger

`Branch Change Intent Ledger` is required when `Pre-Rebaseline Impact Audit` reports non-empty `Rebaseline Overlap Files:` for the active branch/worktree. It preserves why the branch touched an overlapping file before Codex accepts incoming `origin/main` changes.

Runtime branches keep this ledger inside the Branch Runtime Engineering Plan. Non-runtime branches with overlap must admit or update the smallest source-truth-supported Branch Engineering Plan under `Docs/branch_plans/<branch_slug>.md` before rebaseline mutation can proceed.

Each overlapping file uses a repeatable block:

### Changed Surface: <path>

- Surface Class:
- Change Intent:
- Why This File Was Touched:
- Owned Behavior / Fact Class:
- Canonical Owner / Source Owner:
- Resolution Owner:
- Shared Surface:
- Overlap Risk:
- Expected Conflict Risk:
- Semantic Merge Risk:
- Regression / Gating Impact:
- Conflict Resolution Rule:
- Rebaseline Handling:
- Validation Proof:
- Fallback Evidence:
- USER Decision / Waiver:
- Fold-Down Target:

`Surface Class:` values are `governance/source-truth`, `runtime`, `desktop/UI`, `Core visual`, `validator/helper`, `fixture/test`, `configuration/state/schema`, `release/public-output`, `prompt/template`, `automation/watcher`, `build/packaging`, `documentation/reference`, or `asset/media`.

`Semantic Merge Risk:` values are `None`, `Low`, `Medium`, `High`, or `Unknown`. For high-risk surface classes, `Unknown` is `BLOCKED` until evidence or USER decision resolves it.

`Regression / Gating Impact:` values are `None`, `Low`, `Medium`, `High`, or `Unknown`. For `fixture/test` overlap, `Medium`, `High`, or `Unknown` is `BLOCKED` because it can change validator truth, regression coverage, or release gating; `None` or `Low` may be WARN or PASS only when the ledger and fallback evidence support that classification.

`Resolution Owner:` values are `Current Branch`, `Incoming/Folded Owner`, `Originating Lane`, `Standing Governance`, `USER Decision`, or `Future Branch`.

When overlap evidence is missing, weak, stale, or conflicting, Codex must run `Rebaseline Overlap Failure Procedure` and return a packet with `Overall Overlap Gate Result:`, per-file `Per-File Result: PASS / WARN / BLOCKED`, `Recommended Resolution:`, `Validation Required:`, `USER Decision Needed:`, and `Rebaseline Mutation Status:`. Fallback evidence supports classification and USER decision-making only; after the effective point it cannot produce `PASS` without branch-owned change-intent evidence.

## Lifecycle

Branch Readiness Stage 1 proposes the plan requirements and returns the USER planning-review decision needed.

Branch Readiness Stage 2 creates or admits `Docs/branch_plans/<branch_slug>.md`, links it from the branch authority record through `Branch Runtime Engineering Plan Path:`, records `Engineering Plan Status:`, and keeps `Runtime Implementation Approval:` pending until a later USER decision admits runtime work. Stage 2 closeout must explicitly tell USER that the plan is now the object of the next review gate and that USER may accept, change, waive, or reject the plan before implementation.

Branch Readiness Stage 2 must also create or refresh a USER-reviewable Desktop branch-plan packet for the admitted plan under the stable `Nexus USER Review\<worktree-label>` root. The packet uses the same flat-file `USER Review Desktop Bundle` format as Workstream Entry, but its purpose is Stage 2 branch-plan review: it must include `START_HERE.md`, a standalone `USER_BRANCH_PLAN_REVIEW.md`, the active branch plan, active branch authority record, branch-record index, relevant family/Nexus vision or source-truth router files, and any compact backlog/roadmap/validator/helper files needed for USER review of the admitted plan before Workstream Entry analysis or implementation approval. `USER_BRANCH_PLAN_REVIEW.md` is not a Codex status digest: it must be a plain-language pre-plan digest that explains what the branch is intended to implement overall in a few clear sentences, what thing/product/surface the branch is assigned to create or plan, what the next stage must plan, the major accepted/deferred/rejected boundaries, and where the USER can provide early input before Workstream Entry performs deeper implementation analysis. Stage 2 closeout must report the review folder path, copied files, source branch, source HEAD, validation summary, exact next USER decision requested, and pending USER decisions. Workstream Entry must re-check this packet before implementation approval and include a `USER Review Packet Finding:` that names the packet files, exported zip, source branch, packet source HEAD, current branch HEAD, freshness result, digest status, and waiver/blocker status. Missing Stage 2 branch-plan packet proof, a missing/shallow `USER_BRANCH_PLAN_REVIEW.md`, a stale packet, or a packet that was not loaded and digested blocks the handoff on `Branch Readiness Stage 2 Review Bundle Missing`, `USER Branch Plan Review Missing`, `USER Review Packet Stale`, or `USER Review Packet Not Digested`.

Branch Readiness Stage 2 also creates or admits the `Element-to-Phase Proof Matrix` when the branch creates, touches, affects, defers, or preserves product/runtime/UI/source-truth elements. Workstream Entry must return that matrix, or a concrete summary of it, for USER review before implementation begins or resumes.

Workstream Entry must return the `USER Branch Plan Review Gate` packet before implementation begins or resumes for runtime/user-facing/source-truth work. The packet is the readable "what this branch intends to build" handoff, while the active branch plan remains source truth. The Workstream Entry digest must not omit the USER Review Packet: it must either record an explicit waiver or digest `START_HERE.md`, `USER_BRANCH_PLAN_REVIEW.md`, and the exported zip freshness as a named `USER Review Packet Finding:` before any implementation approval text is legal.

Workstream Entry reads the plan and returns whole-package analysis plus the first-seam design packet before implementation. Each seam updates plan-to-implementation traceability with planned item, changed files, validator proof, user-facing proof, and future-gated decisions.

Workstream seam closeout updates the matrix with implemented, skipped, deferred, or future-gated status. Hardening compares actual implementation against the matrix. Live Validation compares observed behavior, user-facing proof, UTS posture, and waiver posture against the matrix. PR Readiness folds durable matrix outcomes into the branch record, workstream doc, family dossier, or Element Validation Ledger owner.

If a Branch Vision Contract Snapshot is required, Workstream Entry also proves `Branch Vision Snapshot Status: Accepted`, `Open Vision Questions: None` or `Deferred With Waiver`, `USER Vision Green: Yes`, accepted implementation scope, accepted seam map, and accepted stop conditions before implementation begins.

If USER feedback is meaningful to current branch scope, future branch scope, accepted vision, validation proof, or reusable product standards, Workstream Entry and later seam packets must either add or update a UFD item or state the no-action reason.

Hardening compares actual implementation against the plan and records extra behavior, skipped items, UI copy integrity, validator coverage, and future-gated item checks.

Hardening also compares actual behavior against the accepted Branch Vision Contract Snapshot when one is required.

Hardening also checks UFD items that affect accepted scope, skipped items, user-facing behavior, validation proof, and future-gated items.

Live Validation records proof or waiver posture against the plan. Disabled/status-only branches must include a static proof substitute and waiver reason.

Live Validation compares observed user-facing behavior against accepted vision and records waiver posture when a branch is disabled/status-only or static-proof-only.

Live Validation must not mark user-facing feedback accepted unless the UFD item is implemented, waived, deferred, rejected/no-action with reason, or carried to a named future owner.

PR Readiness compares the whole branch against the plan and produces the `PR Fold-Down Packet:`. That packet decides what durable content moves into the structured branch receipt, what promotes to a canonical workstream or family dossier, and when the plan is retired from active planning posture.

PR Readiness also folds reusable vision updates into the correct durable owner: Nexus Vision, family vision/family dossier, workstream doc, structured branch receipt, or validated historical receipt. Branch-specific snapshots should not become permanent branch-specific vision file sprawl.

Release Readiness translates the plan into public release language: user-visible highlights, excluded work, future-gated capabilities, and public body wording without internal governance jargon.

## Fold-Down Model

Branch plans are canonical while the owning branch is active. They are not permanent backlog, roadmap, or release-state ledgers.

At PR Readiness, the `PR Fold-Down Packet:` must classify plan content into one of these outcomes:

- migrated into the branch authority record as a structured traceability receipt
- promoted to a canonical workstream or family dossier because future branches should reuse it
- retired from active planning posture because it was superseded, rejected, future-gated, or fully folded down

Branch plans are not deleted by default. Deletion requires a separate USER decision after reference scans prove the plan's durable content and useful historical evidence are preserved elsewhere.

Fold-down must preserve USER decisions, approval boundaries, future-gated items, validator/helper proof, user-facing proof, and plan-to-implementation traceability. It must not preserve stale active phase, live PR, latest-release, worktree dirty-state, or watcher state as current truth.

`Docs/branch_plans/retirement_index.md` owns the current historical branch-plan retirement posture. A plan listed there is retained as a historical receipt, not an active execution blueprint. Future branches must create or admit their own active plan instead of reusing a retired plan by inertia.

## Compact Pointer Rule

The backlog and roadmap must not own detailed runtime plan narrative. They may point to the branch authority record, `Docs/branch_plans/<branch_slug>.md`, canonical workstream docs, or family dossiers. Detailed checklist fields such as `Per-Seam Implementation Checklist:`, `PR Readiness Fold-Down / Retention Checklist:`, and `Release Readiness Public-Scope Translation Checklist:` belong in this plan layer or the folded historical record, not in backlog or roadmap.
