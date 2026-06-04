# Branch Runtime Engineering Plans

`Docs/branch_plans/<branch_slug>.md` defines the Branch Runtime Engineering Plan shape and preserves durable historical branch-plan receipts. After the External Operational State Store transition, active branch planning state lives in `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` until it folds down as durable repo evidence.

Repo branch-plan files are not the long-term place to maintain active ledger rows. While active, detailed plan rows, UFD items, Branch Change Intent rows, Element-to-Phase rows, Workstream Entry review packets, Hardening plans, and Live Validation plans belong in the active external branch planning owner or in an explicitly USER-approved transition packet. Repo copies should reduce to plan shape, durable evidence pointers, fold-down receipts, and historical lookup paths.

Docs Source-Truth Reform Model: Compact Pointer Layer.

This layer sits under the branch authority model. It does not replace the branch authority record, backlog, roadmap, external operational state, or canonical workstream doc.
Codex reaches this layer through the Main-first loader chain: load `Docs/Main.md`, then the governing phase/vision/branch authority owners, then the active branch plan from external operational state for branch-local engineering detail. Repo branch-plan files are historical or transition receipts only.

## Branch Planning Artifact Lifecycle

`Branch Planning` is the canonical phase between `Branch Readiness` and `Workstream`. It owns USER-facing planning review and orchestration validation before runtime/code implementation begins.

The Branch Planning stages are:

- BP1 - `USER Branch Vision Review`, artifact `USER_BRANCH_VISION_REVIEW.md`.
- BP2 - `USER Branch Plan Review`, artifact `USER_BRANCH_PLAN_REVIEW.md`.
- BP3 - `Workstream Entry / Orchestration Validation`, recorded in the Branch Planning packet, active external branch planning owner, and helper/validator output as required.

Branch Vision and Branch Plan are separate contracts:

- Branch Vision is what the branch is building and what it should become.
- Branch Plan is how Codex will build the accepted or waived Branch Vision.
- SLCs are the engineering route inside a branch after vision acceptance. They should not automatically become separate branches.

## Implementation-Bearing Route Requirement

Every active branch plan for a runtime, product, source-truth, helper, validator, or governance repair carrier must include an implementation-bearing route before BP1 begins. Branch Readiness Stage 2 is allowed to discover infrastructure prerequisites, lane groundwork, and route blockers; it admits the route green only after those blockers are resolved, deferred with a legal alternate route, or converted into an exact USER action gate. BP1 defines the vision for the selected route; BP2 plans how Codex will implement that route; BP3 verifies that the route is ready for bounded Workstream execution.

Required active branch-plan route markers:

- Selected Implementation Route:
- Implementation Route Class:
- Concrete Deliverable:
- Implementation Output:
- Infrastructure / Setup Relationship:
- USER Action Gate:
- Route Disposition:
- Retarget / Rename Recommendation:

`Selected Implementation Route:` must name a concrete deliverable, not only a planning question, lane label, setup theme, skeleton, packet, registry, or later branch selection. `Concrete Deliverable:` and `Implementation Output:` must identify the user-visible, runtime, source-truth, helper, validator, or governance behavior that this branch will actually complete if later gates are accepted. `Infrastructure / Setup Relationship:` must explain whether any repo/root/remote/lane/skeleton work is execution-enabling for that deliverable, future-gated by USER action, or out of scope.

Infrastructure and setup can be branch-worthy only when tied to a selected implementation route or to an exact USER action gate. Creating User/Public, Developer, or Owner lanes by itself is groundwork, not a feature implementation carrier. When the legal answer is to pause, retarget, or rename, the branch plan must say so with `Route Disposition:` and `Retarget / Rename Recommendation:` before BP1 or BP2 continue.

When BR2 cannot complete because infrastructure or lane groundwork blocks the selected route, the active branch plan or BR2 packet must include:

- Infrastructure / Lane Groundwork Blockers:
- Required Before This Route Can Proceed:
- Concrete Feature Routes Available Now:
- Deferrable Groundwork:
- Non-Deferrable Groundwork:
- Codex Recommendation:
- Exact USER Decision Needed:

The packet should explain plainly what must exist before Owner, Developer, or User/Public AI work can begin, which prerequisites USER may approve now, which routes can proceed without those prerequisites, and when continued deferral leaves no remaining implementation-bearing route. BR2 may remain blocked or recommend No Active Branch, but it must not complete as green by naming only future planning, lane setup, or later branch selection.

Current planning terminology must use `User/Public lane`, `Developer lane`, and `Owner lane` as lanes or environments, not product version numbers. Use `Developer lane`, not `Dev lane`, in new branch planning packets and active branch plans. Historical branch names, accepted private repo placeholders, and clearly labeled receipts may preserve older wording as traceability only.

BP1 becomes green only when USER accepts the Branch Vision or explicitly waives BP1. BP2 becomes green only when USER accepts the Branch Plan or explicitly waives BP2. BP3 may return bounded Workstream implementation approval for the admitted same-branch package, naming the entry seam or initial seam sequence, only when BP1 and BP2 are accepted or waived, BP3 is approved or waived by USER, and orchestration validation is green.

Branch Planning uses two independent state axes:

- `Packet Reviewability State`: `Missing`, `Generated`, `Validation Failed`, `Reviewable`, `Stale`, or `Superseded`.
- `USER Gate State`: `Pending USER Review`, `USER Revision Requested`, `USER Accepted`, `USER Approved`, `USER Waived`, `USER Rejected`, `USER Blocked`, or `Superseded`.

`Packet Reviewability State: Reviewable` means the packet is ready for USER inspection. It is not USER acceptance, waiver, approval, implementation authority, or next-gate authority. USER gate closure requires a USER response, Codex digest of that response, and an acceptance / waiver / revision / rejection receipt recorded in the review packet, branch plan owner, branch authority receipt, or external operational state. Missing proof blocks on `Branch Planning Acceptance Receipt Missing`, and any helper, validator, or Codex digest that treats packet validation as USER acceptance blocks on `Packet Validation Treated As USER Acceptance`.

Every SLC must trace to a BP1 accepted Branch Vision requirement and a BP2 Branch Plan line item. If BP2 exposes a vision gap or changes the accepted Branch Vision, Codex must route back to BP1 instead of treating the engineering plan as a new vision owner.

The active USER hub for Branch Planning packets is:

- Readable packet: `C:\Nexus USER\<label>\`
- Upload artifact: `C:\Nexus USER\<label>-YYYYMMDD-HHMMSS.zip`

Cloud-backed Desktop or OneDrive locations are backup or convenience mirrors only. USER-facing packet files should focus on vision, plan, context, options, risks, proof expectations, and USER decisions. Active branch status, current HEAD, current origin/main, ahead/behind, upstream, worktree cleanliness, current validation state, current PR state, ZIP hash, and similar mutable technical proof belong in helper output, validator output, Codex chat digest, or external operational state.

## Ownership Model

- Backlog entries remain compact registry, status, and pointer surfaces.
- Roadmap entries remain compact stage-breakpoint schedule and milestone-checkpoint reference surfaces.
- Branch authority records remain durable identity, approval, and historical receipt surfaces; non-standing active branch authority lives in external operational state or Git/GitHub/helper-derived truth.
- Branch Runtime Engineering Plans define detailed runtime execution planning. Their active operational copy belongs in external operational state after transition; repo copies are standards, transition evidence, retirement-index entries, or historical receipts.
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

The matrix extends the active Branch Runtime Engineering Plan from external operational state or an approved transition owner and points to the existing Element Validation Ledger owner. It proves the planned Workstream implementation path, Workstream proof path, Hardening proof path, Live Validation proof or waiver path, UTS / USER acceptance path, and current/future boundary for every element before implementation begins. It must not create a new global ledger or duplicate backlog, roadmap, worktree-slot, or Main live state.

Matrix markers:

- Matrix Status: allowed values are `Required`, `Present`, `Accepted`, `Blocked`, `Folded`, `Historical`, or `Not Required with reason`
- USER Review Status: allowed values are `Pending`, `Accepted`, `Revised`, `Waived`, or `Needs USER Decision`
- Open Element Questions: allowed values are `None`, `Queued`, `Blocking`, or `Deferred With Waiver`
- Element Coverage Owner: must name the active `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` owner before implementation, or a concrete folded source-truth owner after PR Readiness
- Element Validation Ledger Owner: must name the concrete Element Validation Ledger owner path or source-truth owner

Required table shape:

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed `Element Classification` values are `Planned`, `Created`, `Touched`, `Affected`, `Deferred`, `Future`, `Dependency-Only`, and `Non-Gating Supporting`.

Every planned/current created/touched/affected user-facing, runtime, UI, provider, validation/helper, source-truth, or workflow element must name a Workstream implementation path, Workstream proof path, Hardening proof path, Live Validation proof or waiver path, and UTS / USER acceptance path before Workstream implementation begins or resumes. Future/deferred/dependency-only/non-gating elements must name the boundary that keeps them out of current release gating. Element IDs must be unique inside the matrix. Missing or incomplete matrix coverage blocks Workstream entry or continuation on `Element-to-Phase Proof Matrix Missing` or `Element-to-Phase Proof Path Missing`.

## Branch Planning Review Packet

BP3 `Workstream Entry / Orchestration Validation` is the pre-implementation review gate inside the `Branch Planning` phase. It must produce USER-reviewable evidence before implementation begins or resumes.

Before USER can green-light Workstream implementation, Codex must return a full, non-compacted Branch Planning / Workstream Entry Review Digest and create or refresh the active worktree's local USER hub packet under `C:\Nexus USER\<worktree-label>` with a matching timestamped upload ZIP at `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip`.

The bundle should copy the branch vision and planning files the USER needs to inspect, including:

- `USER_BRANCH_VISION_REVIEW.md` when BP1 applies
- `USER_BRANCH_PLAN_REVIEW.md` when BP2 applies
- active external Branch Runtime Engineering Plan or transition-approved Branch Engineering Plan
- Branch Vision Contract Snapshot owner
- Element-to-Phase Proof Matrix owner
- branch authority record
- relevant Nexus Vision and family vision files
- relevant UFD, Branch Change Intent Ledger, source-truth owner, validator/helper, fixture, or planning files

The packet must use the active worktree label and stable subfolders inside that worktree folder: `USER Review` contains exactly one primary USER-facing decision file for the current gate, `Review Aids` contains generated supporting digests/checklists, and `Source Truth Context` contains copied repo context files. `START_HERE.md` maps copied context filenames back to source-truth paths and names the primary USER review file. The digest must report the local USER hub packet path, copied files, validation summary, exact Branch Planning or Workstream green-light decision requested, and pending USER decisions. Helper output may report branch/head/origin-main freshness, but USER-facing files should not center mutable technical proof metadata. Missing packet proof blocks Workstream entry on `Branch Planning Review Packet Missing`.

## USER Review Packet Human-Readability QA

USER-facing Branch Planning packets must be readable decision aids, not validator logs, metadata dumps, or Codex status digests.

Every generated USER-facing packet must include:

- plain-language purpose
- exact USER decision requested
- what USER will see, inspect, or approve
- what will change
- options, tradeoffs, and Codex recommendation
- open USER questions
- files to inspect
- explicit pending/not-approved boundaries

Technical freshness proof such as current branch head, origin/main, ahead/behind, live PR state, ZIP hash, and validation logs belongs in helper output, validator output, external operational state, or the Codex return digest unless a copied source-truth file already contains historical receipt text. `USER Review Packet Human-Readability Missing` blocks when the packet is structurally valid but not useful for USER review. `USER Review Packet Metadata Dump` blocks when mutable technical proof becomes the primary USER-facing content.

## Architecture / Experience / Policy Impact Matrix

When Branch Readiness or Branch Planning touches product, runtime, UI, provider, cache, AI-native, capability-pack, privacy, trust, or source-truth ownership work, the packet must include this matrix or an explicit `No Impact` finding:

| Owner Class | Named Owner | Touches? | Impact Type | Current Branch Scope | Deferred / Future Scope | Proof / Validation Needed |
| --- | --- | --- | --- | --- | --- | --- |
| Architecture Layer | `<named architecture layer>` | Yes / No | No Impact / Consume Existing / Extend Existing / Change Existing / New Candidate / USER Decision Required | `<scope>` | `<boundary>` | `<proof>` |
| Experience Layer | `<named experience layer>` | Yes / No | No Impact / Consume Existing / Extend Existing / Change Existing / New Candidate / USER Decision Required | `<scope>` | `<boundary>` | `<proof>` |
| Cross-Family Policy Owner | `<named policy owner>` | Yes / No | No Impact / Consume Existing / Extend Existing / Change Existing / New Candidate / USER Decision Required | `<scope>` | `<boundary>` | `<proof>` |

The matrix is a routing/proof surface, not a ledger and not implementation approval. `New Candidate` rows must cite the `Source-Truth Placement Preflight` and `No Existing Owner Fits` proof before a new owner can be proposed.

## USER Branch Vision Review Gate

`USER Branch Vision Review Gate` is the named BP1 USER-facing checkpoint. It defines the branch goal, end-state, product shape, user-facing behavior, surfaces, options, Codex recommendations, USER decisions, and acceptance status before engineering planning.

Required BP1 markers:

- USER Branch Vision Review:
- Review Status:
- Contract Status:
- Packet Reviewability State:
- USER Gate State:
- Contract Revision:
- Project Vision Context:
- Family Vision Context:
- Feature Vision Context:
- Codex Understanding:
- Branch Goal:
- End-State Vision:
- What Will I Actually See, And Where Will I See It?:
- How It Will Function:
- User Experience Flow:
- Surface Map:
- Product Options / Design Paths:
- Codex Recommendations:
- Why This Fits The Nexus Vision:
- USER Design Questions:
- USER Response:
- Codex Digest:
- USER Response Proof:
- USER Response Digested:
- Accepted Branch Vision:
- Family-Vision Versus Branch-Only Vision Impact:
- Must-Have Behavior:
- Must-Not-Do / Regression-Risk Rules:
- Deferred And Future-Gated Ideas:
- Vision Question Queue:
- Design Assumption Ledger:
- Acceptance / Revision / Rejection / Waiver Decision:

Codex recommendations in BP1 must be line-item recommendations with enough detail for USER to visualize placement, behavior, flow, tradeoffs, risks, and Codex reasoning. Each recommendation should leave USER response space under that item.

Substantive BP1 artifact rule: `USER_BRANCH_VISION_REVIEW.md` must be an applied branch vision contract, not a template, instruction sheet, copied-file manifest, or marker-only packet. It must digest applicable project, family, feature, branch, package, architecture, policy, and experience context into plain language; define the branch goal and end-state vision; explain what USER will actually see, review, decide, and rely on; describe how the intended feature, readiness, source-truth, or governance outcome will function; map review, decision, experience, and proof surfaces; present real product/design paths with tradeoffs; give branch-specific Codex recommendations; explain Nexus/family fit; ask branch-specific USER design questions; and separate accepted branch vision from BP2 planning preview and future-gated implementation. A copied-file list can support `START_HERE.md` or helper manifests, but it cannot satisfy `Surface Map:` by itself. Template-shell language such as "review the relevant owner," "describe the intended end state," generic accept/revise/waive/reject options, generic Codex recommendations, or broad non-decision-driving USER questions blocks BP1 on `BP1 Template-Shell Review Artifact`, `USER Review Artifact Substantive Content Missing`, `Copied File List Treated As Surface Map`, `Generic Codex Recommendations`, or `Generic USER Questions`.

BP1 must not be SLC-centered. SLCs may be mentioned as later engineering route candidates only after the branch vision and product direction are understandable. BP1 must not center active branch technical metadata such as current HEAD, origin/main, ahead/behind, upstream, current validation state, or current PR state.

## USER Branch Plan Review Gate

`USER Branch Plan Review Gate` is the named BP2 USER-facing engineering checkpoint. It wraps the accepted or waived BP1 result, active external branch plan or transition-approved branch plan, Element-to-Phase Proof Matrix, Hardening plan, Live Validation / UTS plan, UFD items, and Branch Change Intent Ledger when present into a plain-language engineering packet before BP3 orchestration validation. The packet must help USER answer whether the implementation plan correctly builds the accepted Branch Vision, not merely prove that governance markers exist.

Required review markers:

- USER Branch Plan Review:
- Review Status:
- Contract Status:
- Packet Reviewability State:
- USER Gate State:
- USER Response Proof:
- USER Response Digested:
- Acceptance / Waiver / Revision / Rejection Receipt:
- Contract Version / Revision:
- Accepted Branch Vision Summary:
- Implementation Package Summary:
- Branch Scope Size Test:
- SLC / Seam Plan:
- Affected Surfaces:
- Likely Files:
- Validators / Helpers:
- Proof Requirements:
- Element-to-Phase Proof Matrix:
- H1 Expectations:
- LV / UTS Expectations:
- Rollback / Safety Plan:
- Open Engineering Risks:
- Future-Gated Boundaries:
- Line-Item USER Plan Review:
- Plan Acceptance Checklist:
- Exact BP3 Approval Text:
- USER Review Hub Packet:
- USER Review Packet Finding:
- Plain-Language Branch Goal:
- What Will I Actually See, And Where Will I See It?:
- Planned User-Facing Outcome:
- End-State Vision:
- Visual / Behavioral Description:
- Visual / Functional Walkthrough:
- Surface Map:
- Implementation Breakdown:
- Element-to-Phase Proof Matrix:
- Hardening Plan:
- Live Validation / UTS Plan:
- Open USER Questions:
- USER Plan Review Questions:
- Codex Recommendations:
- Implementation Options:
- Recommended Direction:
- Why This Fits The Nexus Vision:
- USER Plan Review Decision:
- Current Branch Scope:
- Future-Gated Scope:
- Implementation Staging Notes:
- USER Decisions Needed:
- Alternatives / Tradeoffs:
- USER Review Response:
- Codex Response Digest:
- Implementation Constraints Created By USER Response:
- USER Rejected / Deferred Ideas:
- Vision Delta / Source-Truth Impact:
- Contract Change Log:
- Workstream Entry Result:
- Contract Completion Checklist:
- Accepted Scope:
- Deferred Scope:
- Rejected Scope:
- Exact USER Decision Needed:
- Implementation Approval:

`Review Status:` must use `Accepted by USER`, `Revised by USER`, `Deferred With Waiver`, `Rejected by USER`, or `Needs USER Decision`. `Contract Status:` is the closed-loop BP2 Branch Plan Contract state and must use `Draft`, `Pending USER Response`, `Pending Codex Digest`, `Pending USER Confirmation`, `Complete`, or `Waived by USER`. `Packet Reviewability State:` must use `Missing`, `Generated`, `Validation Failed`, `Reviewable`, `Stale`, or `Superseded`. `USER Gate State:` must use `Pending USER Review`, `USER Revision Requested`, `USER Accepted`, `USER Approved`, `USER Waived`, `USER Rejected`, `USER Blocked`, or `Superseded`. A packet can be reviewable while the USER gate remains pending; helpers and validators must report those states separately. The packet must give USER answer paths to accept the engineering plan, accept with changes, route back to BP1 because the plan changes the accepted Branch Vision, explicitly waive remaining BP2 questions, reject and request a narrower branch or plan, or pause as unclear. `USER_BRANCH_PLAN_REVIEW.md` is the BP2 USER Branch Plan Review: a required user-facing engineering-plan artifact derived from accepted or waived BP1, not the primary product/design vision contract and not a normal Codex status digest. It must present the accepted Branch Vision summary, implementation package summary, branch scope size test, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, Element-to-Phase Proof Matrix, H1 expectations, LV/UTS expectations, rollback/safety plan, open engineering risks, future-gated boundaries, line-item USER plan review, USER response area, Codex response digest, implementation constraints created from USER response, rejected/deferred ideas, source-truth impact, change log, plan acceptance checklist, and exact BP3 approval text when ready. The primary BP2 decision surface is whether the engineering plan correctly builds the accepted BP1 vision and preserves future-gated boundaries; if the engineering plan changes product direction, user-facing behavior, surfaces, scope, or future-gated boundaries, it must route back to BP1 before implementation approval.

Substantive BP2 artifact rule: `USER_BRANCH_PLAN_REVIEW.md` must translate the accepted or waived BP1 branch vision into an applied engineering plan. It must define the largest safe coherent branch scope, describe seams/SLCs as engineering route details inside the accepted vision, identify likely files, helpers, validators, review artifacts, proof outputs, risk controls, rollback/reversibility posture, implementation options with tradeoffs, and Codex recommendation, and prove alignment to BP1. A BP2 packet that merely repeats BP1 vision headings, lists markers, says "see copied files," or presents generic implementation choices blocks on `BP2 Template-Shell Review Artifact` or `USER Review Artifact Substantive Content Missing`. BP2 must keep BP3 and Workstream future-gated until USER accepts or waives BP2 and BP3 validates orchestration.

The BP2 Branch Plan Contract lifecycle is closed loop: Codex proposes the engineering plan derived from BP1, USER responds, Codex digests the response, Codex converts that response into explicit implementation constraints, Codex identifies source-truth and review-packet impact, and any plan-changing digest returns `Contract Status:` to `Pending USER Confirmation`. Codex must update the branch record, branch plan, family vision, backlog, roadmap, validation helper registry, review packet, or other required source truth when USER feedback changes branch direction, feature shape, UI behavior, workflow, end-state vision, implementation scope, future-gated boundaries, or seam order. Codex then refreshes the local USER hub packet and exported ZIP. The cycle repeats until USER explicitly confirms the final contract as `Complete` or explicitly waives the gate. BP3 preparation may proceed only when `Contract Status:` is `Complete` or `Waived by USER` and `USER Gate State:` is `USER Accepted` or `USER Waived`.

Waiver semantics are strict. A waiver must be explicit USER text naming the contract and branch; Codex must record it in the branch record, branch plan, and review packet, set `Contract Status:` to `Waived by USER`, preserve pending boundaries, and cite the waiver in exact implementation approval text. A stale packet is blocking when `START_HERE.md` branch or HEAD differs from the active branch/current HEAD, when ZIP Source HEAD differs from packet Source HEAD, when `USER_BRANCH_PLAN_REVIEW.md` Contract Status conflicts with branch plan or branch record, or when implementation approval text is returned while Contract Status is `Draft`, `Pending USER Response`, `Pending Codex Digest`, or `Pending USER Confirmation`.

Missing or shallow accepted BP1 trace, package summary, branch scope size test, SLC/seam plan, affected surfaces, likely files, validators/helpers, proof requirements, matrix, H1/LV/UTS expectations, rollback/safety plan, risks, future-gated boundaries, USER plan review, USER response/digest or waiver, implementation constraints, source-truth impact, completion checklist, local USER hub packet proof, `USER Review Packet Finding:`, `Packet Reviewability State:`, `USER Gate State:`, USER acceptance/waiver/approval proof, or exact USER decision blocks BP3 and Workstream implementation on `USER Branch Plan Review Missing`, `BP2 Review Packet Ready But USER Response Pending`, or `BP2 USER Acceptance Proof Missing`. A local USER hub packet that is stale against current helper/validator proof, not loaded, not digested, missing `START_HERE.md`, missing `USER_BRANCH_VISION_REVIEW.md` when BP1 applies, missing `USER_BRANCH_PLAN_REVIEW.md` when BP2 applies, missing the exported zip when required, or not explicitly waived blocks on `USER Review Packet Stale` or `USER Review Packet Not Digested`. A first-seam-only packet cannot satisfy BP3 when multiple slices or seams are admitted.

## Workstream Entry Whole-Package Analysis Gate

Runtime-focused branch plans with multiple admitted slices or seams must support whole-package Workstream Entry analysis before implementation begins or resumes.

The active external branch planning owner must let the Workstream Entry packet identify:

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

First-seam selection alone is not enough. A Workstream Entry packet may recommend the entry implementation seam, but it must also prove that seam fits the full admitted branch package, that bounded continuation remains active until Workstream Green, a real blocker, or an explicit USER waiver, and that it does not create drift against later admitted seams. Missing whole-package analysis blocks Workstream entry on `Workstream Entry Whole-Package Analysis Missing`. This gate plans Hardening and Live Validation obligations; it does not authorize executing Hardening, Live Validation, UTS handoff, PR creation, merge, release work, or runtime implementation without the separately legal phase approval.

Substantive BP3 artifact rule: BP3 `Workstream Entry / Orchestration Validation` must verify Workstream readiness against the accepted or waived BP1 and BP2 contracts. It must confirm implementation scope, orchestration order, validation plan, proof plan, rollback posture, drift controls, unresolved USER decisions, and blockers, then return a clear go/repair/blocked recommendation for Workstream Entry. BP3 cannot be satisfied by helper-green hygiene, a first-seam-only packet, a generic command wall, or implementation-ready wording while BP1/BP2 USER gates remain pending. Weak BP3 packets block on `BP3 Template-Shell Review Artifact`, `Workstream Entry Whole-Package Analysis Missing`, `Packet Validation Treated As USER Acceptance`, or `Review Gate Bypass`.

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

Vision update ownership follows the `Vision Update Decision Matrix` in `Docs/phase_governance.md`: branch-specific or unresolved ideas stay in the active external branch planning owner, reusable USER-accepted family standards fold into family vision or family dossiers, and project-wide USER-accepted standards fold into `Docs/nexus_vision.md`. Codex must not promote proposed or unresolved ideas into durable vision owners by inference.

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

Minor comments, acknowledgements, typo-level notes, duplicate remarks, or non-actionable conversation may close with no durable UFD item only when Codex records the no-action reason in the active external branch planning owner or return digest.

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

`No Durable Owner Needed` is valid only when the item is closed as minor/no-action, duplicate, superseded, or non-actionable, with `No-Action Reason:` recorded in the active external branch planning owner or return digest.

Pointer locations may carry UFD ID, short title, canonical owner, compact status, and fold-down status only. They must not carry full feedback text, full decision history, or live implementation state.

UFD IDs use `UFD-<scope>-YYYYMMDD-NNN`. Do not use `FBK-*`, because it collides visually with historical `FB-###` workstream records.

## USER Feedback Disposition Fold-Down

At PR Readiness, every UFD item must be migrated, deferred with waiver, rejected/no-action with reason, closed, or explicitly carried to a future owner.

The fold-down receipt must preserve a lookup path from every UFD ID to its final owner after branch-plan fold-down and retirement.

Branch records carry compact UFD status and pointers only. Backlog carries future-candidate pointers only after USER accepts the future-work disposition. Nexus Vision and family vision owners receive only accepted reusable standards, not branch-local unresolved feedback.

## Branch Change Intent Ledger

`Branch Change Intent Ledger` is required when `Pre-Rebaseline Impact Audit` reports non-empty `Rebaseline Overlap Files:` for the active branch/worktree. It preserves why the branch touched an overlapping file before Codex accepts incoming `origin/main` changes.

Runtime branches keep this ledger inside the active external Branch Runtime Engineering Plan. Non-runtime branches with overlap must admit or update the smallest source-truth-supported external Branch Engineering Plan under `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md` before rebaseline mutation can proceed.

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

Branch Readiness Stage 2 creates or admits `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`, links it from the branch authority record through `Branch Runtime Engineering Plan Path:`, records `Engineering Plan Status:`, and keeps `Runtime Implementation Approval:` pending until a later USER decision admits runtime work. Stage 2 closeout must explicitly tell USER that the active external plan is now the object of the next review gate and that USER may accept, change, waive, or reject the plan before implementation.

Branch Readiness Stage 2 may also create or refresh a USER-reviewable local hub packet for the admitted branch under `C:\Nexus USER\<worktree-label>` with a matching timestamped upload ZIP at `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip`. The packet uses the stable structured local USER hub format: `START_HERE.md` at the root, `USER Review` with exactly one primary decision file for the active gate, `Review Aids` for generated supporting digests/checklists, and `Source Truth Context` for copied repo context such as the active external branch plan or approved transition branch plan, branch authority evidence pointer, branch-record index, relevant family/Nexus vision or source-truth router files, and compact backlog/roadmap/validator/helper files needed for USER review before Workstream implementation approval. Stage 2 closeout must report the review folder path, copied files, validation summary, exact next USER decision requested, and pending USER decisions through helper output or Codex digest rather than making mutable branch status the focus of USER-facing files. Missing local USER hub packet proof, missing/shallow Branch Planning review files, stale packet, packet not loaded/digested, or missing USER response/digest/waiver blocks the handoff on `Branch Readiness Stage 2 Review Bundle Missing`, `BP1 Branch Vision Review Missing`, `BP2 Branch Plan Review Missing`, `USER Review Packet Stale`, or `USER Review Packet Not Digested`.

Branch Readiness Stage 2 also creates or admits the `Element-to-Phase Proof Matrix` when the branch creates, touches, affects, defers, or preserves product/runtime/UI/source-truth elements. BP3 must return that matrix, or a concrete summary of it, for USER review before implementation begins or resumes.

BP1 must return the `USER Branch Vision Review Gate` before engineering plan acceptance. BP2 must return the `USER Branch Plan Review Gate` before BP3 orchestration validation. BP3 must return Workstream Entry / Orchestration Validation before implementation begins or resumes for runtime/user-facing/source-truth work. The packet is the readable "what this branch intends to build and how Codex will build it" handoff, while the active external branch planning owner remains source truth. The BP3 digest must not omit the USER Review Packet: it must either record an explicit waiver or digest `START_HERE.md`, applicable Branch Planning review files, and the exported zip as a named `USER Review Packet Finding:` before any implementation approval text is legal. It must also report `USER Review Response:` and `Codex Response Digest:` so the next implementation packet proves USER design input was accepted, revised, rejected, deferred with waiver, or is still blocking.

BP3 reads the accepted/waived BP1 and BP2 plan and returns whole-package analysis plus bounded Workstream package implementation approval text before implementation, naming the entry seam or initial seam sequence. Each Workstream seam updates plan-to-implementation traceability with planned item, changed files, validator proof, user-facing proof, and future-gated decisions.

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

The backlog and roadmap must not own detailed runtime plan narrative. They may point to the branch authority record, active external branch plan, repo branch-plan historical receipt, canonical workstream docs, or family dossiers. Detailed checklist fields such as `Per-Seam Implementation Checklist:`, `PR Readiness Fold-Down / Retention Checklist:`, and `Release Readiness Public-Scope Translation Checklist:` belong in the external plan layer or the folded historical record, not in backlog or roadmap.
