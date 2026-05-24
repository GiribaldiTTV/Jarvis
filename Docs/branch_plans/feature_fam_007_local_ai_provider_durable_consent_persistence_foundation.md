# Branch Runtime Engineering Plan: FAM-007 Local AI Provider Durable Consent Persistence Foundation

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-durable-consent-persistence-foundation; surface=branch-plan; status=canonical

## Branch Runtime Engineering Plan

Plan Identity: `FAM-007 Local AI Provider Durable Consent Persistence Foundation - Branch Runtime Engineering Plan v1`
Owning Branch: `feature/fam-007-local-ai-provider-durable-consent-persistence-foundation`
Worktree Path: `C:\Nexus Worktrees\FAM-007`
Branch Authority Record Pointer: `Docs/branch_records/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md`
Current Phase: `Branch Readiness`
Branch Runtime Engineering Plan: Required and present for the FAM-007 durable consent persistence foundation runtime carrier.
Engineering Plan Status: Accepted - Stage 2 setup records the detailed runtime plan while Workstream Entry and implementation remain separately gated.
Current Runtime Baseline: Released FAM-007 evidence through v1.7.16-prebeta includes setup/consent-flow readiness, setup contract readiness, setup implementation foundation, consent collection foundation, and PR #201 local consent capture/write-path implementation foundation. Current safety posture remains provider-visible data none, sentToProvider false, canAcceptPrompts false, prompt/model execution disabled, downloads/network blocked, memory inactive or deferred, voice/Core sync gated, and desktop readiness display suppression preserved.
Branch Purpose: Admit the next FAM-007 successor that turns local consent capture/write-path proof into durable local consent persistence planning before any user-operated consent UX, provider setup completion, SDK/model execution, or functional AI.
Planned Runtime Delta: Add durable local consent record persistence, consent schema versioning, storage-boundary proof, revocation/reset durable semantics, setup consent and execution consent durable separation, local provenance/audit metadata, fail-closed persistence behavior, Core/Desktop/ORIN status proof, and validator fixtures.
User-Facing Delta: Any user-visible change must be status-only and truthful: durable local consent persistence is local-only and does not imply provider setup completion, consent UX completion, prompt acceptance, provider/model execution, downloads, network, memory, voice/Core sync, or functional AI.
Source-Truth Delta: Stage 2 records FAM-007 branch authority, v1.7.16 release closure for PR #201, compact FAM-007 pointer updates, family-scoped Branch Readiness confinement repair, validator/helper posture, and this plan.
State / Config / Schema Delta: Planned fields include durable consent record schema, schema version, setup consent durable flag, execution consent durable flag, revoked/reset/expired state, local storage boundary marker, provenance source, audit timestamp, no-secrets marker, fail-closed reason code, and future handoff metadata.
Validator / Helper Delta: Extend branch governance validation for family-scoped Branch Readiness confinement and later extend FAM-007 provider-state validation for durable persistence fixtures, missing/invalid/stale/revoked/reset states, setup/execution durable separation, local-only storage boundary, provider-visible-data none, sentToProvider false, and canAcceptPrompts false.
Expected Changed Files / Surfaces: Stage 2 source-truth files include this plan, the branch record, branch index, backlog, roadmap, worktree slots, validation helper registry, phase governance, and branch governance validator. Later Workstream surfaces may include desktop/ai_provider_state.py, desktop/desktop_renderer.py, desktop/core_visualization_renderer.py, nexus_visual/orin_core.*, and dev/orin_ai_provider_state_validation.py.
Workstream / Seam Map: Seam 1 -> durable consent persistence state and schema; Seam 2 -> local storage boundary and migration posture; Seam 3 -> revocation/reset/expiry persistence semantics; Seam 4 -> setup consent and execution consent durable separation; Seam 5 -> Core/Desktop/ORIN status proof and desktop readiness display suppression continuity; Seam 6 -> validator fixtures, fail-closed behavior, and future provider setup handoff criteria.
Per-Seam Implementation Checklist: Each seam must name implementation files, source-truth updates, state/schema changes, no-provider/no-network/no-memory boundaries, validator changes, and stop conditions before coding begins.
Per-Seam Validation Checklist: Run diff checks, branch governance, worktree confinement gate, release-readiness health gate, governance efficiency, release body, source-owner marker validation, branch-readiness planning fixtures, AI provider state validation, runtime-fam007 validation suite, rebaseline audit, compileall, and any new persistence fixtures.
Per-Seam User-Facing Proof Checklist: If visible status changes, prove copy through static Core/Desktop/ORIN inspection or focused screenshots as Workstream Entry requires; if no visible UX is admitted, record the static/hidden-telemetry waiver basis.
Future-Gated Items: Future USER approval gates remain for user-operated consent UX, provider setup completion, provider SDK integration, provider/model execution, model downloads, external calls, memory/indexing/learning/personalization, voice/Core sync, shortcut/installer work, release execution, issue work, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.
Approval-Boundary Audit: Stage 2 authorizes planning and governance/source-truth repair only. Workstream implementation, visible user consent UX, provider setup/model/memory/network/voice/shortcut/installer work, PR creation, merge, release, cleanup, and sibling-worktree mutation remain pending USER decisions.
FAM / Shared-Surface Overlap Forecast: FAM-006 is a separate sibling lane and overlap context only; Governance is standing intake context; Compact-AI is historical released/salvaged evidence. None is successor authority for this FAM-007 branch.
Open Questions: Whether durable persistence uses an existing config/profile store or a dedicated local consent store; whether visible consent UX belongs in the next branch; when provider setup completion becomes admissible after durable consent persistence.
USER Planning Decisions: USER approved FAM-007 Branch Readiness Stage 2 and the bounded confinement repair on this branch. USER has not approved runtime implementation, PR creation, merge, release, provider setup completion, SDK/model execution, downloads/network, memory, voice/Core sync, shortcuts/installers, cleanup, AI Product Contract import, Private Dev ORIN import, or v1.8.0-prebeta execution.
Plan Revision History: v1 created during Branch Readiness Stage 2 from origin/main@10c32804370ee5480416e68e55823e5997d18291 after v1.7.16-prebeta release.
Plan-To-Implementation Traceability Table: Planned persistence state maps to desktop provider-state implementation and fixtures; planned storage boundary maps to local-only no-network proof; revocation/reset maps to fail-closed validator cases; setup/execution separation maps to provider execution blockers; status proof maps to Core/Desktop/ORIN static proof; continuation criteria map to H1, LV1, PR Readiness, and Release Readiness fold-down.
Hardening Comparison Checklist: H1 must compare durable consent schema, storage boundary, revocation/reset, setup/execution separation, no-provider/no-network/no-memory posture, UI/status copy, validator fixtures, branch plan, Runtime Branch Engineering Contract, Product Definition Plan, and confinement repair against implementation.
Live Validation Proof Or Waiver Checklist: LV1 must classify the branch, prove static/runtime validator state, prove any visible status surface or record a source-truth-supported waiver, and keep provider-visible data none, prompt execution disabled, downloads/network/memory blocked, and voice/Core sync gated.
PR Readiness Fold-Down / Retention Checklist: PR Readiness must fold durable consent persistence scope into branch record/source truth, resolve selected-next or USER waiver truth, prove release-window/no-release-debt posture, preserve branch-authority cleanup, and keep live PR/watcher state out of merged current-state owners.
Release Readiness Public-Scope Translation Checklist: Release Readiness must describe this branch as durable local consent persistence foundation only and exclude provider setup completion, SDK/model execution, functional AI, memory, voice/Core, downloads/network, and v1.8.0 execution unless later USER-approved proof changes that scope.
USER Planning Review: Pending Workstream Entry review. Stage 2 records the review bundle files in the branch record.
PR Fold-Down Packet: Pending until PR Readiness.
Runtime Implementation Approval: Pending - Workstream Entry and implementation require later USER approval.

## Product Definition Plan

Product Vision: FAM-007 should become useful local AI through explicit user control over setup, consent, provider-visible data, and execution before any model is allowed to run.
User-Facing Goal: Make future consent UI reliable by first proving durable local consent truth, revocation/reset posture, and local-only storage boundaries.
Project-Wide Vision Alignment: Nexus remains a Windows-first local desktop assistant with privacy-explicit, user-controlled local AI layers and honest disabled-state copy before model execution.
Branch-Specific Vision Alignment: This branch owns durable consent persistence foundation only; provider setup completion, consent UX, provider SDK/model execution, and functional AI remain future branches.
USER Vision Questions: No blocking questions for Stage 2. Workstream Entry should ask whether storage location and visible proof need USER selection before implementation.
USER Vision Question Packet: Not required for Stage 2 because visible user UX is excluded; any later visible UX requires USER-approved Branch Readiness or Workstream Entry scope.
Codex Product Interpretation: Durable persistence is the next safest prerequisite because the previous branch proved local capture/write-path snapshot behavior but explicitly deferred durable storage.
Codex Implementation Recommendation: Implement durable persistence and revocation/reset semantics before user-operated consent UX or provider setup completion.
Codex Additional Recommendations: Keep consent persistence local-only, auditable, versioned, fail-closed, and disconnected from prompt acceptance or provider communication.
USER/ChatGPT Review Checkpoint: USER may inspect this plan and branch record before approving Workstream Entry.
USER Critique Loop: USER can accept, revise, reject, defer, or waive this plan before implementation.
USER Decision Ledger: Stage 2 setup approved; runtime implementation and later phases pending.
Deferred Ideas / Future Package Ledger: User-operated consent UX, provider setup completion, provider SDK/adapter, prompt/model execution, provider-visible data behavior proof, memory/indexing/personalization, voice/Core sync, shortcut/installer work, and v1.8.0 release execution.
Planning Adequacy Review: The plan names state, schema, storage, revocation, reset, consent separation, validation, proof, FAM boundaries, and future-gated items; it is not a shallow or single-marker plan.
Rejected Shallow Plan: A shallow plan that only toggles a "consent persisted" flag is rejected because consent durability needs schema, storage boundary, provenance, revocation/reset, and fail-closed proof.
Alternatives And Tradeoffs Reviewed: Provider setup completion would be more product-visible but riskier before durable consent truth. User-operated consent UX is useful but should not precede persistence semantics. SDK/model execution remains premature.
Whole-System Interaction Map: Local consent capture/write path -> durable local consent record -> setup/execution consent gates -> provider setup handoff -> disabled prompt/model execution -> future functional-AI proof.
Open Questions / USER Decision Points: Storage location, visibility of consent status, timing for user-operated consent UX, and timing for provider setup completion remain future decisions.
Minimum Viable vs Full System Boundary: Minimum viable branch proves durable local consent persistence; full system includes visible consent UX, provider setup, provider SDK/model execution, memory, voice/Core sync, and v1.8.0 proof.
Full Feature Element Breakdown: Durable consent record, schema version, storage boundary, setup durable consent, execution durable consent, revoked/reset/expired states, provenance/audit metadata, no-secrets posture, status proof, validator fixtures, future handoff.
System Concept Model: Durable consent is a local prerequisite and audit trail for future setup/execution, not execution authorization.
Entity / Profile Model: Local consent record, provider profile reference, setup consent state, execution consent state, revocation/reset state, storage boundary, schema version, provenance, audit envelope, future handoff.
User Workflow Model: A future user grants or revokes consent through a later UI; this branch makes the underlying durable state trustworthy first.
Scale / Data Volume Model: Handle absent, invalid, stale, reset, revoked, single-profile, and future multi-provider consent records without network or memory scope.
Configuration And State Model: Consent persistence is local, versioned, revocable, resettable, fail-closed, and separate from provider config/model execution state.
Expected User-Facing Outcomes: No functional-AI claim; any status copy must be conservative and local-only.
Acceptance Criteria: Durable persistence schema, local storage boundary, revocation/reset, setup/execution separation, provider-visible-data none, disabled execution, validators, H1, LV1 or waiver, and PR readiness fold-down.
User-Facing Proof Standard: Static or hidden-telemetry proof unless visible UX is admitted; visible UX requires screenshot/live proof and UTS path.
Current Branch vs Future Package Boundary: Current branch: durable persistence. Future package: user consent UX, provider setup completion, SDK/model execution, memory, voice/Core, shortcuts/installers, v1.8.0.
Affected Files / Surfaces: Branch source truth, provider-state model, desktop/Core/ORIN status surfaces, provider-state validator, branch governance validator, and generated inventory if source truth requires.
Data / Control Model: Local consent state may gate future setup but may not send provider data, accept prompts, execute models, download assets, write memory, or call external services.
Branch Reach / Package-Size Proof: The branch is appropriately sized because durability, revocation/reset, consent separation, status proof, and fixtures form one coherent prerequisite.
Why This Branch Should Not Split Smaller: Splitting storage, schema, and revocation/reset would create partial durable consent truth that later branches could misread.
Implementation Sequence Proposal: Stage 2 setup -> Workstream Entry -> bounded Workstream -> H1 -> LV1 -> PR Readiness -> PR -> merge -> Release Readiness.
Planning Blockers: None for Stage 2.
USER Decisions Needed: Workstream Entry, implementation, PR creation, merge, release, cleanup, and future-gated runtime/product work.

## Element-to-Phase Proof Matrix

Matrix Status: Accepted for Stage 2 setup and pending Workstream Entry review.
USER Review Status: Pending Workstream Entry.
Open Element Questions: Deferred with waiver - storage location and visible proof posture may be reviewed at Workstream Entry without blocking Stage 2 setup.
Element Coverage Owner: Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md.
Element Validation Ledger Owner: Docs/branch_records/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md.

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAM007-DCP-001 | Durable consent record state and schema | Planned | Workstream implementation will add a versioned local consent record schema, fail-closed defaults, schema-version provenance, and explicit missing/invalid/stale record handling in the FAM-007 provider-state model. | Workstream proof will add provider-state fixtures for missing, invalid, stale, revoked, reset, and valid durable records while preserving provider-visible-data none and disabled execution. | Hardening H1 will compare the implemented schema, default posture, and reason codes against this plan, the branch record, and Runtime Branch Engineering Contract. | LV1 will use static source/validator proof or a recorded waiver unless Workstream Entry admits a visible status surface for durable persistence. | USER acceptance will use a UTS only if visible consent persistence proof is admitted; otherwise USER acceptance remains the Workstream/H1/LV1 static proof packet. | Provider setup, user-operated consent UX, provider/model execution, and v1.8.0 release proof remain future boundaries. | Proposed pending USER Workstream Entry decision. | Branch plan and branch record. |
| FAM007-DCP-002 | Local storage boundary and migration posture | Planned | Workstream implementation will define the local-only storage boundary, migration/deferred posture, no-secrets envelope, and persistence failure behavior without adding network, provider payload, or memory scope. | Workstream proof will run validators showing no network calls, no downloads, no memory writes, no provider-visible data, and a local-only storage boundary across durable consent states. | Hardening H1 will verify the storage boundary, no hidden external calls, no model artifacts, and no memory/indexing behavior against source truth and implementation. | LV1 will confirm the local-only storage boundary through static validator proof and will not require a live client path unless visible UX is admitted. | USER acceptance will rely on the Stage 2 plan review and later validator proof unless a later Workstream decision admits visible storage/status proof. | Dedicated storage migration, secrets, credentials, model artifacts, and broader persistence stores remain future or excluded boundaries. | Proposed pending USER Workstream Entry decision. | Branch plan and provider-state validator. |
| FAM007-DCP-003 | Revocation, reset, and expiry semantics | Planned | Workstream implementation will add durable revoked, reset, expired, restored, and fail-closed transitions with distinct reason codes and local audit provenance. | Workstream proof will add fixtures proving revoked, reset, expired, restored, and invalid states block prompt acceptance and provider execution. | Hardening H1 will compare fail-closed behavior, reason-code consistency, provenance, and source-truth boundaries against the implemented state model. | LV1 will validate disabled execution after revoked, reset, expired, or invalid durable consent states using static provider-state validator proof. | USER acceptance will inspect the H1/LV1 packet and only require user-facing UTS if Workstream Entry admits a visible revocation/reset path. | User-operated revocation UX, consent editing, and provider execution after consent remain future USER-approved branches. | Proposed pending USER Workstream Entry decision. | Branch plan and provider-state validator. |
| FAM007-DCP-004 | Setup/execution durable consent separation | Planned | Workstream implementation will persist setup consent and execution consent separately so setup consent can never imply execution consent, prompt acceptance, or provider-visible data transfer. | Workstream proof will add fixtures for setup-only, execution-missing, execution-revoked, and both-consents-present local states while keeping canAcceptPrompts false. | Hardening H1 will verify there is no consent conflation and no execution approval side effect from durable setup consent. | LV1 will confirm canAcceptPrompts remains false and sentToProvider remains false even when durable setup consent exists. | USER acceptance will rely on static proof unless visible setup/execution consent status is admitted and then requires focused UTS or screenshot proof. | Execution approval, prompt routing, provider adapter setup, model execution, and provider-visible-data behavior remain future boundaries. | Proposed pending USER Workstream Entry decision. | Branch plan and desktop provider state. |
| FAM007-DCP-005 | Status proof and desktop readiness suppression | Planned | Workstream implementation may map durable persistence posture to hidden telemetry or status-only Core/Desktop/ORIN proof without restoring the long desktop AI-owned readiness display. | Workstream proof will run validators and static source inspection to confirm copy stays conservative and does not claim provider setup, execution, downloads, memory, or functional AI. | Hardening H1 will check UI/status copy, hidden telemetry mapping, desktop readiness suppression continuity, and source-truth consistency. | LV1 will prove static or visible status exactly as admitted by Workstream Entry and record a waiver if no user-facing path exists. | USER acceptance will require UTS only if a user-facing surface is admitted; otherwise the proof packet remains static validator evidence. | User-operated consent UX, broad desktop readiness display, functional-AI copy, and release-marketing claims remain future boundaries. | Proposed pending USER Workstream Entry decision. | Branch plan and source truth. |
| FAM007-DCP-006 | Family-scoped Branch Readiness confinement repair | Touched | Stage 2 adds source-truth and validator guardrails that require Target Family and Sibling Worktree Candidate Exclusion for FAM Branch Readiness records. | Workstream proof for this governance repair is the branch governance validator plus worktree confinement gate proving sibling lanes are overlap context only. | H1 and PR readiness will keep sibling lanes as overlap context only and stop if a future FAM-007 pass drifts into another family. | LV1 is not required for this non-user-facing governance element; static branch governance validation is the live proof substitute. | No UTS is needed because this is a source-truth/validator guardrail rather than a runtime user-visible feature. | Broader governance reform, sibling-lane cleanup, and repo-wide selector policy changes remain future Governance/intake boundaries. | Accepted for Stage 2 with future Workstream proof pending USER decision. | Branch record, phase governance, branch index, validation helper registry, governance validator. |

## Branch Change Intent Ledger

### Changed Surface: Docs/branch_records/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md
- Surface Class: `governance/source-truth`
- Change Intent: `Create the FAM-007 durable consent persistence active branch authority record for Branch Readiness Stage 2.`
- Why This File Was Touched: `The approved Stage 2 setup needed a canonical branch record, release baseline, PDP/RBEC/BREP pointers, plan-review gate, and family-scoped confinement evidence.`
- Owned Behavior / Fact Class: `FAM-007 branch-local authority, Product Definition Plan, Runtime Branch Engineering Contract, Branch Runtime Engineering Plan pointer, release evidence, and next-phase digest.`
- Canonical Owner / Source Owner: `Docs/branch_records/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO - branch-local authority record.`
- Overlap Risk: `Low unless another lane claims FAM-007 successor authority before this branch merges.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve this record as FAM-007 branch-local authority until PR fold-down or a later USER-approved Branch Readiness decision supersedes it.`
- Rebaseline Handling: `Keep branch-local authority fields; reconcile only compact pointers or release baseline if origin/main advances under USER-approved rebaseline.`
- Validation Proof: `Run branch governance validation, worktree confinement validation, branch-readiness planning fixture validation, source-owner marker validation, and rebaseline audit validation.`
- Fallback Evidence: `Git branch identity, worktree slot receipt, branch index pointer, and this plan prove the authority; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved Branch Readiness Stage 2 and the bounded governance repair on this FAM-007 branch.`
- Fold-Down Target: `PR Readiness will convert active authority into historical branch evidence after merge.`

### Changed Surface: Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md
- Surface Class: `governance/source-truth`
- Change Intent: `Create the FAM-007 durable consent persistence Branch Runtime Engineering Plan and record the Branch Change Intent Ledger.`
- Why This File Was Touched: `The approved Stage 2 setup requires PDP, RBEC, BREP, Element-to-Phase Proof Matrix, and overlap intent evidence before Workstream Entry.`
- Owned Behavior / Fact Class: `FAM-007 branch-local planning, Workstream seam map, validation proof path, phase proof matrix, and changed-surface intent ledger.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_007_local_ai_provider_durable_consent_persistence_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO - branch-local plan file.`
- Overlap Risk: `Low unless a later rebaseline changes active governance planning schema.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve current branch-local planning facts while accepting later merged governance schema changes through explicit rebaseline audit.`
- Rebaseline Handling: `Revalidate with branch governance, planning fixture validation, and rebaseline audit before accepting incoming planning-schema drift.`
- Validation Proof: `Run branch governance validation, branch-readiness planning fixture validation, source-owner marker validation, rebaseline audit validation, and compileall validation.`
- Fallback Evidence: `The active branch record points to this plan and records the same branch/worktree/baseline facts; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved Stage 2 setup and required this repair to happen on the FAM-007 branch.`
- Fold-Down Target: `PR Readiness fold-down retains this plan as branch evidence after merge.`

### Changed Surface: Docs/phase_governance.md
- Surface Class: `governance/source-truth`
- Change Intent: `Record Family-Scoped Branch Readiness Confinement so family-scoped Stage 2 cannot drift into sibling branch selection.`
- Owned Behavior / Fact Class: `Governance phase rule tied to this Stage 2 repair.`
- Why This File Was Touched: `USER identified Branch Readiness drift where a FAM-007 pass treated sibling FAM-006 context as successor authority; the shared phase rule now names the required confinement behavior.`
- Canonical Owner / Source Owner: `Docs/phase_governance.md with this FAM-007 branch carrying a bounded repair approved by USER.`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - repo-wide phase governance.`
- Overlap Risk: `Medium because future governance intake may refine this rule, but the immediate repair prevents sibling-lane drift.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve the family-scoped confinement rule unless a later Governance PR replaces it with an equal or stronger target-family selector guard.`
- Rebaseline Handling: `During rebaseline, keep Target Family and Sibling Worktree Candidate Exclusion semantics for FAM Branch Readiness unless USER explicitly broadens scope.`
- Validation Proof: `python dev\orin_branch_governance_validation.py; python dev\orin_branch_governance_validation.py --worktree-confinement-gate`
- Fallback Evidence: `Branch record and validator source contain the same confinement markers; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved repairing the governance issue on this FAM-007 branch during Stage 2.`
- Fold-Down Target: `Merged phase governance after PR merge; branch record retains branch-local proof.`

### Changed Surface: dev/orin_branch_governance_validation.py
- Surface Class: `validator/helper`
- Change Intent: `Make Target Family and Sibling Worktree Candidate Exclusion machine-checkable for FAM Branch Readiness confinement.`
- Why This File Was Touched: `Source truth alone would not prevent repeat drift; the validator now fails FAM Branch Readiness records that omit target-family and sibling-exclusion evidence.`
- Owned Behavior / Fact Class: `Governance validator guard.`
- Canonical Owner / Source Owner: `dev/orin_branch_governance_validation.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - repo-wide branch governance validator.`
- Overlap Risk: `Medium because validator changes can block unrelated branches if over-broad, so the guard is scoped to FAM Branch Readiness records.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Keep the check narrow to Branch Readiness plus fam-* branch names and require only explicit record markers already added to source truth.`
- Rebaseline Handling: `If incoming governance changes touch this validator, preserve the confinement check or replace it with equivalent stronger validation.`
- Validation Proof: `python dev\orin_branch_governance_validation.py; python dev\orin_branch_governance_validation.py --worktree-confinement-gate; python dev\orin_branch_readiness_planning_fixture_validation.py`
- Fallback Evidence: `Docs/phase_governance.md, Docs/branch_records/index.md, and Docs/validation_helper_registry.md mirror the required phrases; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved a bounded governance repair on this branch to prevent FAM-007/FAM-006 drift.`
- Fold-Down Target: `Validator behavior remains in main after PR merge and is cited by validation helper registry.`

### Changed Surface: Docs/branch_records/index.md
- Surface Class: `governance/source-truth`
- Change Intent: `Register active FAM-007 branch authority and compactly mirror the family-scoped confinement rule.`
- Why This File Was Touched: `The branch index must point to the active FAM-007 successor record and expose the compact confinement rule near branch authority routing.`
- Owned Behavior / Fact Class: `Branch authority routing.`
- Canonical Owner / Source Owner: `Docs/branch_records/index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - branch authority index.`
- Overlap Risk: `Medium because active-branch pointers and shared governance text are common rebaseline conflict surfaces.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve the FAM-007 active branch pointer while keeping sibling lanes as overlap context only; later PR Readiness may retire the pointer.`
- Rebaseline Handling: `Conflict-aware merge required if origin/main advances; keep active FAM-007 pointer unless USER selects another FAM-007 successor.`
- Validation Proof: `python dev\orin_branch_governance_validation.py`
- Fallback Evidence: `Branch record, worktree slot receipt, and git identity prove the active carrier; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this FAM-007 Stage 2 carrier and did not authorize switching to sibling lanes.`
- Fold-Down Target: `PR Readiness and merge fold-down will update active/historical branch authority.`

### Changed Surface: Docs/feature_backlog.md
- Surface Class: `governance/source-truth`
- Change Intent: `Record v1.7.16 release closure for PR #201 and current FAM-007 durable consent persistence Stage 2 posture.`
- Why This File Was Touched: `The compact backlog pointer must show PR #201 as released evidence and identify this FAM-007 successor without treating FAM-006 as current branch authority.`
- Owned Behavior / Fact Class: `Compact FAM/package pointer status.`
- Canonical Owner / Source Owner: `Docs/feature_backlog.md for compact package status; branch record and plan own detailed FAM-007 authority.`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - compact package status.`
- Overlap Risk: `Medium because backlog rows may also be touched by release readiness or governance branches.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve v1.7.16 PR #201 released evidence and current FAM-007 durable consent successor pointer; keep unrelated family rows from becoming FAM-007 authority.`
- Rebaseline Handling: `Accept release/source-truth updates only after verifying origin/main and preserving FAM-007 branch-local successor facts.`
- Validation Proof: `python dev\orin_governance_efficiency_validation.py; python dev\orin_branch_governance_validation.py`
- Fallback Evidence: `Branch record and prebeta roadmap carry matching FAM-007 release and successor facts; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved FAM-007 Stage 2 and explicitly directed ignoring FAM-006 as a successor lane.`
- Fold-Down Target: `Release Readiness and PR Readiness compact-source fold-down after this branch merges.`

### Changed Surface: Docs/prebeta_roadmap.md
- Surface Class: `governance/source-truth`
- Change Intent: `Record v1.7.16 release closure for PR #201 and active FAM-007 successor pointer without making the roadmap a live release ledger.`
- Why This File Was Touched: `The roadmap needs the latest FAM-007 progression after v1.7.16 while keeping provider execution and v1.8.0 future-gated.`
- Owned Behavior / Fact Class: `Compact roadmap status.`
- Canonical Owner / Source Owner: `Docs/prebeta_roadmap.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - roadmap source truth.`
- Overlap Risk: `Medium because release readiness and branch readiness both update roadmap posture.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve the roadmap as compact planning truth, not a live release ledger; keep this FAM-007 successor pointer and future-gated provider execution posture.`
- Rebaseline Handling: `If release records advance, update compact roadmap facts only through a governed release/branch readiness pass.`
- Validation Proof: `python dev\orin_governance_efficiency_validation.py; python dev\orin_release_body_validation.py`
- Fallback Evidence: `Release tag v1.7.16 and branch record release fields support the roadmap pointer; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved Stage 2 after v1.7.16 and did not approve v1.8.0 execution.`
- Fold-Down Target: `Future Release Readiness public-scope translation and FAM-007 branch fold-down.`

### Changed Surface: Docs/worktree_slots.md
- Surface Class: `governance/source-truth`
- Change Intent: `Assign runtime-active-1 to the fresh FAM-007 durable consent persistence carrier while preserving stable worktree binding.`
- Why This File Was Touched: `Worktree slot truth must keep this thread and branch bound to C:\Nexus Worktrees\FAM-007 and block sibling-worktree drift.`
- Owned Behavior / Fact Class: `Worktree slot assignment receipt.`
- Canonical Owner / Source Owner: `Docs/worktree_slots.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - worktree assignment source truth.`
- Overlap Risk: `Medium because sibling worktrees may be active but remain overlap context only for this FAM-007 pass.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Conflict Resolution Rule: `Preserve runtime-active-1 as the FAM-007 worktree/branch assignment and route sibling lanes to context-only status unless USER approves broader scope.`
- Rebaseline Handling: `Re-run worktree confinement gate after any rebaseline and before PR readiness.`
- Validation Proof: `python dev\orin_branch_governance_validation.py --worktree-confinement-gate`
- Fallback Evidence: `Git worktree list and active branch record match this slot; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved all FAM-007 work to remain localized to C:\Nexus Worktrees\FAM-007.`
- Fold-Down Target: `PR Readiness worktree-slot receipt and later cleanup only with USER approval.`

### Changed Surface: Docs/validation_helper_registry.md
- Surface Class: `governance/source-truth`
- Change Intent: `Record FAM-007 durable consent persistence validator planning and governance validator confinement repair ownership.`
- Why This File Was Touched: `The helper registry must name the new confinement validation behavior and the planned FAM-007 provider-state validation extension.`
- Owned Behavior / Fact Class: `Validator/helper registry.`
- Canonical Owner / Source Owner: `Docs/validation_helper_registry.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - repo-wide helper registry.`
- Overlap Risk: `Medium because helper registry rows are shared by governance, release readiness, and runtime branches.`
- Expected Conflict Risk: `Medium`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Medium`
- Validation Proof: `python dev\orin_branch_governance_validation.py; python dev\orin_ai_provider_state_validation.py`
- Conflict Resolution Rule: `Preserve the confinement validator registration and FAM-007 durable persistence validation plan while accepting later stronger governance helper wording through rebaseline.`
- Rebaseline Handling: `Re-run helper registry, branch governance, planning fixture, and AI provider state validation after any registry conflict.`
- Fallback Evidence: `Branch record, branch plan, and validator source point to the same validation responsibilities; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved this branch to carry the bounded governance repair and FAM-007 Stage 2 validator planning.`
- Fold-Down Target: `Validation helper registry remains shared source truth after PR merge.`

### Changed Surface: Docs/governance_docs_full_inventory_reform_audit.md
- Surface Class: `documentation/reference`
- Change Intent: `Regenerate the full Docs inventory after adding the FAM-007 durable consent branch record and branch plan.`
- Why This File Was Touched: `Governance efficiency validation requires generated inventory counts to match the current Docs filesystem count.`
- Owned Behavior / Fact Class: `Generated Docs inventory/reference surface; FAM-007 owns only the new branch-local docs that caused the count change.`
- Canonical Owner / Source Owner: `dev/orin_docs_inventory_reform_audit.py and Docs/governance_docs_full_inventory_reform_audit.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - generated documentation reference.`
- Overlap Risk: `Low generated-doc churn if another branch adds or removes Docs files before rebaseline.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `None`
- Conflict Resolution Rule: `Regenerate with current repo tooling after adding or removing Docs files, then validate the generated file count.`
- Rebaseline Handling: `Accept incoming generated inventory only if it matches current Docs count, otherwise regenerate intentionally and record the output.`
- Validation Proof: `Run governance efficiency validation, branch governance validation, branch-readiness planning fixture validation, and docs inventory generator validation output.`
- Fallback Evidence: `Generator output recorded 166 Docs file entries; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved Stage 2 source-truth setup and validation repairs needed to make the branch legal.`
- Fold-Down Target: `Generated inventory remains reference source truth on the PR branch and merged main.`

### Changed Surface: Docs/governance_docs_reform_user_review_index.md
- Surface Class: `documentation/reference`
- Change Intent: `Regenerate the docs reform USER review index after adding the FAM-007 durable consent branch record and branch plan.`
- Why This File Was Touched: `Governance efficiency validation requires the review index to cover the same Docs filesystem count as the full inventory.`
- Owned Behavior / Fact Class: `Generated USER review index; FAM-007 owns only the new branch-local docs and Stage 2 review files it introduces.`
- Canonical Owner / Source Owner: `dev/orin_docs_inventory_reform_audit.py and Docs/governance_docs_reform_user_review_index.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `YES - generated documentation reference.`
- Overlap Risk: `Low generated-doc churn if another branch changes Docs inventory before rebaseline.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `None`
- Conflict Resolution Rule: `Regenerate the review index from current repo tooling instead of manually editing generated counts.`
- Rebaseline Handling: `Accept incoming review index only if generated counts match current Docs count, otherwise regenerate intentionally.`
- Validation Proof: `Run governance efficiency validation, branch governance validation, branch-readiness planning fixture validation, and docs inventory generator validation output.`
- Fallback Evidence: `Generator output recorded 166 Docs file entries; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved Stage 2 source-truth setup and validation repairs needed to make the branch legal.`
- Fold-Down Target: `Generated USER review index remains reference source truth on the PR branch and merged main.`

### Changed Surface: Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md
- Surface Class: `governance/source-truth`
- Change Intent: `Close the prior FAM-007 consent collection implementation carrier as PR #201 released evidence in v1.7.16-prebeta.`
- Why This File Was Touched: `Stage 2 requires the predecessor branch to be historical so the new durable consent persistence carrier is not confused with the merged PR #201 branch.`
- Owned Behavior / Fact Class: `Historical FAM-007 branch evidence, PR #201 release closure, and predecessor proof posture.`
- Canonical Owner / Source Owner: `Docs/branch_records/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO - prior FAM-007 branch-local record.`
- Overlap Risk: `Low unless release readiness rewrites v1.7.16 closure facts.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve PR #201 as historical released evidence and keep provider execution/model work future-gated.`
- Rebaseline Handling: `If release truth advances, update only release closure fields and keep predecessor lifecycle historical.`
- Validation Proof: `Run branch governance validation, release-readiness health validation, governance efficiency validation, and release body validation.`
- Fallback Evidence: `PR #201 merge/release proof and v1.7.16 release tag support this historical closure; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved continuing to the next FAM-007 branch after PR #201 and v1.7.16 release.`
- Fold-Down Target: `Historical branch evidence retained in branch records index and release readiness source truth.`

### Changed Surface: Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md
- Surface Class: `governance/source-truth`
- Change Intent: `Retire the prior FAM-007 consent collection implementation plan from active planning posture after PR #201 and v1.7.16 release.`
- Why This File Was Touched: `The predecessor plan must not remain active once this durable consent persistence successor becomes the Stage 2 carrier.`
- Owned Behavior / Fact Class: `Historical Branch Runtime Engineering Plan evidence and predecessor release closure.`
- Canonical Owner / Source Owner: `Docs/branch_plans/feature_fam_007_local_ai_provider_consent_collection_implementation_foundation.md`
- Resolution Owner: `Current Branch`
- Shared Surface: `NO - prior FAM-007 branch-local plan.`
- Overlap Risk: `Low lifecycle drift if old plan still looks active.`
- Expected Conflict Risk: `Low`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Keep this predecessor plan historical and keep the durable consent persistence plan as active branch authority.`
- Rebaseline Handling: `Verify predecessor lifecycle remains historical during any future rebaseline or release fold-down.`
- Validation Proof: `Run branch governance validation, planning fixture validation, release-readiness health validation, and release body validation.`
- Fallback Evidence: `The new branch record points to the successor plan and PR #201 release proof closes this predecessor; not a compatibility bypass.`
- USER Decision / Waiver: `USER approved selecting the next FAM-007 successor after PR #201 instead of continuing this historical branch.`
- Fold-Down Target: `Historical plan evidence retained for future FAM-007 traceability.`
