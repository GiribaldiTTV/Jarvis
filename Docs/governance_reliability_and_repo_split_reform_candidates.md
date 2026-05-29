# Governance Reliability And Repo Split Reform Candidates

Document Status: Non-Binding Planning
Created: 2026-05-28
Source Basis: `C:\Nexus USER\Governance\Nexus_Project_Governance_Full_Digest.md`, current repo source truth, and USER-provided ChatGPT recommendation text.
Current Worktree: `C:\Nexus Worktrees\Governance`
Current Branch: `feature/release-readiness-source-truth-intake`
Current Baseline: `origin/main@8d7ccd4c98fb2418e27ee3a96fd775c51cbcc718`

## First Step - Post-Idle Rebaseline And Plan Reconciliation

Before any governance reliability reform cycle begins, wait until the active FAM worktrees have finished their current PR / merge / release flow or USER explicitly approves starting earlier.

After the worktrees are idle, rebaseline and reconcile the relevant worktrees against the new `origin/main` baseline. Then analyze this plan against the new baseline before implementation. The analysis must:

- reload `Docs/Main.md` first and follow the routed source-truth owners
- compare this plan against the new repo baseline, current external operational state, and any newly merged FAM-006 / FAM-007 source-truth changes
- identify plan items that are still valid, stale, superseded, duplicated, missing, or now better owned by a different source-truth file
- reconcile Main / Dev / Owner split assumptions against current FAM-007 source truth
- update this planning file with recommendations before any reform cycle mutates binding source truth
- return a digest with changed recommendations, blockers, owner-file impacts, and exact USER decisions needed

This first step is a planning/reconciliation gate. It does not authorize source-truth contract edits, helper code, validator code, PR Readiness, PR creation, merge, release, repo split execution, private repo creation, runtime work, FAM worktree mutation, file movement, file deletion, or file archival.

## Purpose

This planning reference preserves candidate improvements for repo-wide governance, source truth, efficiency, reliability, error checking, drift prevention, and future Main / Dev / Owner repo separation.

This file is intentionally non-binding. It does not create new governance law, validators, helper requirements, source-truth owners, branch scope, external state records, repo split execution, private repos, file moves, or migration authority. Future implementation requires a separate USER-approved source-truth patch that names the owner files and exact write set.

## Source-Truth Boundary

Current repo truth already provides the first-order rules that control these recommendations:

- `Docs/Main.md` is the first loader and source-truth router.
- `Docs/phase_governance.md` owns phase law.
- `Docs/governance_efficiency_operating_model.md` owns the repo-docs-as-index/context model and external operational state contract.
- `Docs/feature_backlog.md` owns backlog identity and taxonomy.
- `Docs/ai_runtime_and_trust_architecture.md` already owns AI-native architecture and cross-family AI trust/cache/provider/capability direction.
- `Docs/validation_helper_registry.md` owns validator/helper interpretation and reuse.
- `Docs/external_operational_state_store_reform_plan.md` preserves the completed External Operational State Store transition and future cleanup boundaries.

Because source truth says to run `Source-Truth Placement Preflight` and extend existing owners first, this file treats every proposed new file or registry as a candidate only. A later implementation pass must prove `No Existing Owner Fits` before creating new durable owners.

## Current Branch Scope Correction - 2026-05-28

Scope Classification:

`RRI-20260528-001` contains the completed USER Review Gate semantics repair and the completed admitted Governance Reliability / Repo Split Reform source-truth contract cycles. Helper/validator code beyond already-committed review-gate false-green prevention, external-state mutation, repo split execution, FAM worktree mutation, main mutation, private repo creation, runtime work, release work, PR creation, and merge remain separate USER decisions.

PR Readiness Posture:

The admitted Governance Reliability / Repo Split Reform cycles and final integration hardening are complete. The next legal phase is PR Readiness Stage 1 analysis after USER approval.

Legal Path Options:

| Path | Meaning | Legal Next Phase | PR Readiness Status |
| --- | --- | --- | --- |
| Limited PR path | Superseded by USER approval to complete all admitted reform cycles in this branch | Not current | Not current |
| Full reform continuation path | Completed admitted docs/source-truth contract cycles before one consolidated PR | PR Readiness Stage 1 after USER approval | Ready for Stage 1 analysis |

USER Preference Captured:

The USER approved all remaining phases/cycles in bounded mode on 2026-05-28, with USER gates and approvals waived/accepted for completing the admitted reform plan. That approval does not authorize PR creation, merge, release, runtime work, FAM worktree mutation, external-state mutation, repo split execution, private repo creation, file movement/deletion/archival, or helper/validator code mutation beyond the already-committed review-gate false-green prevention.

Current Commit Completion Matrix:

| Plan Section | Current Branch Status | Evidence / Notes |
| --- | --- | --- |
| Active Failure Class - USER Review Gate Bypass | Completed in current branch | Binding source truth, helper behavior, validator checks, fixtures, incident pattern, and USER review packet were updated. |
| Worktree-Delta Reconciliation Findings | Completed for this cycle | Read-only audit of Main, Governance, FAM-006, and FAM-007 was recorded; product worktrees were not mutated. |
| Governance Reliability / Repo Split Reform Planning File | Completed as planning evidence | This file exists as non-binding planning and candidate sequencing evidence. |
| Cycle 1 - Taxonomy / Owner Discipline | Completed for source-truth contract | `Docs/feature_backlog.md`, `Docs/governance_efficiency_operating_model.md`, `Docs/phase_governance.md`, and compact `Docs/Main.md` routing now preserve taxonomy, family rejection, `No Existing Owner Fits`, and owner-discipline rules. |
| Cycle 2 - Architecture / Experience / Policy Impact Matrix | Completed for source-truth contract | `Docs/phase_governance.md` and `Docs/branch_plans/README.md` require the matrix; existing owners remain `Docs/ai_runtime_and_trust_architecture.md`, product vision, and family visions. |
| Cycle 3 - Hypothesis-Driven Reliability | Completed for source-truth contract | `Docs/ai_runtime_and_trust_architecture.md` now records reliability classes and the Observation / Hypothesis / Validation loop. |
| Cycle 4 - PR / Review Drift Prevention | Completed for source-truth contract | USER Review Gate false-green prevention, PR body drift checks, review packet readability QA, and helper/validator evidence boundaries are recorded. |
| Cycle 5 - Main / Dev / Owner Boundary Planning | Completed for public-safe governance boundary | `Docs/governance_efficiency_operating_model.md` records the Main / Dev / Owner boundary contract; concrete private/runtime/FAM-007 work remains separate. |
| Governance Quickstart | Deferred / future candidate | Orientation-only artifact; not required before this reform can proceed unless USER admits it. |
| Optional explicit registries | Deferred / future candidate | May be created only after `No Existing Owner Fits` is proven. |
| Helper / validator implementation beyond current bypass checks | Deferred / separate USER decision | Current branch changed helper/validator only for the USER Review Gate false-green prevention; later code hardening must be separately admitted if needed. |
| Repo split execution, external-state migration, file movement, deletion, archival, private repo creation | Requires separate branch or later cycle | Not authorized and not performed. |
| Final integration hardening | Completed for current admitted source-truth contract | Owner conflicts, mirror drift, phase wording, taxonomy consistency, helper/validator guidance, PR/review drift, packet readability, private/public boundary leakage, and source-truth placement were checked before PR Readiness Stage 1 recommendation. |

Admitted Scope Rule:

Further mutation requires a new legal phase decision. The next legal phase for this branch is PR Readiness Stage 1 analysis; PR creation, merge, release, helper/validator code expansion, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, runtime work, FAM worktree mutation, and main mutation remain separate USER decisions.

## Cycle 1 BR2 Admission - Taxonomy / Owner Discipline

Admission Date: 2026-05-28

Admission Status:

Cycle 1 is admitted as a bounded Governance Reliability / Repo Split Reform cycle for Taxonomy / Owner Discipline.

Current Gate:

Cycle 1 BP1, BP2, BP3, Workstream, Hardening, and LV1/non-applicability were completed under the USER's 2026-05-28 bounded all-phases/all-cycles approval. The earlier BP1 reviewable/pending packet is now superseded by this completion record.

Cycle 1 Packet State:

- Packet Reviewability State: `Superseded`.
- USER Gate State: `USER Waived`.
- BP2 Plan Review: `Completed under bounded all-cycles approval`.
- BP3 Workstream Entry / Orchestration Validation: `Completed under bounded all-cycles approval`.
- Workstream Implementation: `Completed for docs/source-truth contract only`.
- PR Readiness: `Ready for Stage 1 analysis after USER approval`.

Cycle 1 Vision:

Cycle 1 should make taxonomy and owner routing harder to misread. It should prevent Codex from turning architecture layers, policy owners, experience layers, runtime subsystems, capability-pack domains, packages, slices, seams, mirrors, indexes, receipts, or external operational state into backlog families or source-truth owners by inertia.

Cycle 1 Owner Placement:

- `Docs/feature_backlog.md` remains the primary owner for backlog family identity, backlog admission, and the taxonomy gate.
- `Docs/governance_efficiency_operating_model.md` remains the primary owner for source-truth placement discipline, one-owner/mirror rules, compact pointer rules, and repo-docs-as-index/context boundaries.
- `Docs/phase_governance.md` remains the primary owner for phase-gate requirements and Branch Readiness / Branch Planning enforcement.
- `Docs/branch_plans/README.md` remains the primary owner for branch-planning packet structure and BP1/BP2/BP3 artifact expectations.
- `Docs/workstreams/index.md` remains the primary owner for package/slice/seam traceability and workstream-layer identity boundaries.
- `Docs/ai_runtime_and_trust_architecture.md` remains the primary owner for AI-native architecture, policy, reliability, provider, cache, capability-pack, and cross-family AI trust direction.
- `Docs/nexus_vision.md` and `Docs/family_visions/*` remain product-vision owners and should be extended only when Cycle 1 proves a taxonomy/owner-discipline change belongs there.

BP1 Review Questions:

- Does USER accept the Cycle 1 vision that taxonomy/owner discipline is the foundation cycle before architecture/experience/policy impact matrices, reliability classes, PR/review drift prevention, and Main / Dev / Owner boundary planning?
- Does USER agree that Cycle 1 should strengthen existing owners first rather than create new durable registries by default?
- Does USER want Cycle 1 to treat `No Existing Owner Fits` as the required proof before creating any new FAM, source-truth owner, architecture registry, experience registry, or policy registry?
- Does USER want any taxonomy class added, removed, renamed, or split before BP2 engineering/source-truth planning begins?

Forecast Only - Later Gates:

- Later plan gate: define exact owner-file edits, examples, blocker wording, validation expectations, and proof that no binding mutation has occurred by assumption.
- Later orchestration gate: prove the accepted plan is ready for bounded source-truth implementation, with helper/validator code mutation still separate unless explicitly approved.
- Later Workstream: implement only the approved taxonomy/owner-discipline source-truth edits.
- Later Hardening: scan touched owners, mirrors, indexes, packets, and validation guidance for taxonomy drift, owner duplication, and accidental live-state or ledger material.
- Later LV1: record USER-readable proof or `LV1 Applicability: Not Applicable with reason`.

Cycle 1 Stop Conditions:

- Stop if USER wants a new backlog family or durable source-truth owner before `No Existing Owner Fits` is proven.
- Stop if the taxonomy change would mutate FAM-006, FAM-007, main, runtime/provider/model behavior, external operational state, private repo boundaries, file movement, deletion, archival, helper code, or validator code without separate USER approval.
- Stop if packet reviewability is mistaken for BP1 acceptance.
- Stop if BP2, BP3, Workstream, PR Readiness, PR creation, merge, or release is requested before the prior gates close legally.

## Full Reform Completion Record - 2026-05-28

Completion Scope:

The admitted Governance Reliability / Repo Split Reform source-truth contract is complete for the current Governance branch. The completed scope is docs/source-truth governance contract work and USER packet refresh only.

Completed Cycles:

- Cycle 0 - USER Review Gate semantics repair.
- Cycle 1 - Taxonomy / Owner Discipline.
- Cycle 2 - Architecture / Experience / Policy Impact Matrix.
- Cycle 3 - Hypothesis-Driven Reliability.
- Cycle 4 - PR / Review Drift Prevention.
- Cycle 5 - Main / Dev / Owner Boundary Planning, public-safe boundary only.

Cycle Proof Summary:

- Taxonomy / Owner Discipline: backlog taxonomy, family rejection tests, `No Existing Owner Fits`, source-truth authority hierarchy, and mirror drift control are recorded in the existing owners.
- Architecture / Experience / Policy Impact Matrix: Branch Readiness and Branch Planning must classify architecture, experience, policy, runtime subsystem, capability-pack, family vision, package/slice/seam, or no-impact routing before implementation.
- Hypothesis-Driven Reliability: AI runtime/trust architecture records deterministic, high-confidence, advisory, exploratory/hypothesis, and creative reliability classes plus the Observation / Hypothesis / Validation loop.
- PR / Review Drift Prevention: PR body drift checks, USER review packet human-readability QA, packet reviewability versus USER acceptance, and validators-as-evidence boundaries are recorded.
- Main / Dev / Owner Boundary Planning: public-safe repo/source-truth boundary, promotion/disclosure gates, private-reference leak blockers, and FAM-007/private implementation deferral are recorded.

Final Integration Hardening:

- Owner conflicts: no new durable owner file was created; existing owners were extended first.
- Mirror drift: Main and review/packet surfaces remain compact pointers while owner files carry the durable rules.
- Phase wording conflicts: BP1/BP2/BP3 acceptance semantics remain unchanged; this record only notes the USER's all-cycle waiver for this bounded governance run.
- Taxonomy consistency: `FAM-009` remains reusable because workspace/data and safety/privacy fold-source files are not active families or number reservations.
- Validator/helper guidance consistency: helper/validator code expansion remains future/deferred unless separately approved; registry guidance names reuse-first targets.
- PR/review drift: PR body audit and review-packet readability rules are recorded without creating PRs.
- Private/public boundary leakage: Main / Dev / Owner split is public-safe planning only; private repo creation, private remotes, provider/model execution, memory/cache implementation, and private import are still blocked.
- Source-truth placement: no repo docs were moved, deleted, archived, or converted into new ledgers.

Next Legal Phase:

PR Readiness Stage 1 analysis, after USER approval. PR creation, merge, release, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, runtime work, FAM worktree mutation, main mutation, and helper/validator code expansion remain separate USER decisions.

## Active Failure Class - USER Review Gate Bypass / Packet Validation Treated As USER Acceptance

Failure Title:
USER Review Gate bypass caused by treating packet validation as gate acceptance.

FAM-006 Evidence Summary:

- FAM-006 BP1 packet generation produced stale wrong-family and wrong-phase USER review aid wording, including Governance, PR Readiness, FAM-007, AI Runtime, Stage 2, and Workstream Entry language inside generated review surfaces.
- After BP1 repair, BP2 packet validation reported the BP2 branch-plan review path while generated files still contained BP1-pending and BP2-placeholder state.
- After BP2 repair, BP3 was reported as prepared / implementation-ready while the uploaded packet still described BP2 USER Branch Plan Review as pending USER response.
- This proves a repeatable false-green class: helper/validator packet reviewability, file freshness, or Codex digest state can be misread as USER acceptance, waiver, BP3 approval, or implementation authority.

Affected Phases / Stages:
Branch Planning BP1, BP2, BP3, Workstream Entry / Orchestration Validation, and the first Workstream implementation approval handoff.

Root Cause Hypothesis:
Branch Planning had strong language requiring USER review, but it did not consistently model packet reviewability and USER gate closure as separate machine-readable axes. Helpers and digests could therefore say a packet was valid, reviewable, or implementation-ready without proving USER response receipt and Codex digestion for the active gate.

Governance Owner Files:

- `Docs/phase_governance.md`
- `Docs/branch_plans/README.md`
- `Docs/development_rules.md`
- `Docs/codex_modes.md`
- `Docs/nexus_startup_contract.md`
- `Docs/Main.md`
- `Docs/validation_helper_registry.md`
- `Docs/incident_patterns.md`
- `Docs/orin_task_template.md`

Helper / Validator Owner Files:

- `dev/orin_user_review_bundle.py`
- `dev/orin_branch_governance_validation.py`
- `dev/orin_branch_readiness_planning_fixture_validation.py`
- `dev/fixtures/branch_readiness_planning/valid_branch_planning_review_gate_state.md`
- `dev/fixtures/branch_readiness_planning/invalid_packet_validation_treated_as_user_acceptance.md`

Required Canonical State Model:
Branch Planning review gates must carry two independent axes:

- `Packet Reviewability State`: `Missing`, `Generated`, `Validation Failed`, `Reviewable`, `Stale`, or `Superseded`.
- `USER Gate State`: `Pending USER Review`, `USER Revision Requested`, `USER Accepted`, `USER Approved`, `USER Waived`, `USER Rejected`, `USER Blocked`, or `Superseded`.

Required transition semantics:

- BP1.1 prepares/repairs `USER_BRANCH_VISION_REVIEW.md`; BP1.2 is the USER Review Gate; BP1.3 records USER acceptance, waiver, revision, rejection, or blocker.
- BP2.1 prepares/repairs `USER_BRANCH_PLAN_REVIEW.md` only after BP1 is accepted or waived; BP2.2 is the USER Review Gate; BP2.3 records USER acceptance, waiver, revision, rejection, or blocker.
- BP3.1 prepares/repairs Workstream Entry / Orchestration Validation only after BP1 and BP2 are accepted or waived; BP3.2 is the USER orchestration review gate; BP3.3 records USER approval, waiver, revision, or blocker.
- Workstream implementation remains separately USER-gated after legal BP3 posture.

Required Blockers:

- `BP1 Review Packet Ready But USER Response Pending`
- `BP1 USER Acceptance Proof Missing`
- `BP2 Review Packet Ready But USER Response Pending`
- `BP2 USER Acceptance Proof Missing`
- `BP3 Review Packet Ready But USER Response Pending`
- `BP3 USER Approval Proof Missing`
- `Packet Validation Treated As USER Acceptance`
- `Review Gate Bypass`
- `USER Review Packet Phase-State Conflict`
- `USER Review Packet Not Digested`
- `Branch Planning Acceptance Receipt Missing`
- `Helper False Green On Review Gate State`
- `Codex Digest Conflicts With USER Packet`

Required Fixtures:

- valid BP1/BP2/BP3 gate packet where packet is reviewable but USER gate is pending and implementation remains blocked
- valid accepted/waived gate packet where USER response proof is digested
- invalid stale wrong-family / wrong-phase generated USER-facing review aid
- invalid BP1 template-shell review artifact that tells USER what sections should contain instead of applying branch-specific vision
- invalid BP1 copied-file-list-only `Surface Map`
- invalid BP1 generic USER questions that do not drive branch-specific decisions
- invalid shallow or generic Codex recommendations
- invalid BP1-pending packet used as BP2/BP3 proof
- invalid BP2-placeholder or BP2-pending packet misclassified as BP3
- invalid BP3 packet misclassified as implementation-ready before BP3 USER approval
- invalid Codex digest that conflicts with uploaded USER packet state

Substantive Artifact Standard:
BP1, BP2, and BP3 reviewability requires more than clean headings, stale-language hygiene, copied-file freshness, and ZIP consistency. BP1 must be an applied branch vision contract; BP2 must be an applied engineering plan contract derived from accepted or waived BP1; BP3 must be an applied orchestration-readiness contract against accepted or waived BP1/BP2. Copied source-truth files are context and navigation evidence only. Helper output, validators, and fixtures must reject template-shell prose, generic options, generic recommendations, broad questions, and copied-file manifests when they are used as substitutes for USER-facing vision, plan, or orchestration content. This standard applies globally to every branch and worktree packet, including FAM-006, FAM-007, Governance, and future families after they rebaseline to the merged governance.

Required Validation Commands:

- `git diff --check`
- `git diff --check origin/main...HEAD`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_branch_governance_validation.py --worktree-confinement-gate`
- `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`
- `python dev\orin_branch_readiness_planning_fixture_validation.py`
- `python dev\orin_governance_efficiency_validation.py`
- `python dev\orin_source_owner_marker_validation.py`
- `python -m compileall -q dev desktop Audio main.py nexus_visual`

Worktree-Delta Reconciliation Findings:

| Worktree | Branch | HEAD vs `origin/main` orientation | Changed-file summary | Governance / helper overlap | Risk |
| --- | --- | --- | --- | --- | --- |
| `C:\Nexus Desktop AI` | `main` | `git rev-list --left-right --count HEAD...origin/main` = `0 12` (`HEAD` is 0 ahead, 12 behind) | no committed branch diff versus `origin/main`; untracked `Docs/Phase_Governance_Full_Digest.md` | none to mutate in this patch | neutral main is behind; read-only only |
| `C:\Nexus Worktrees\Governance` | `feature/release-readiness-source-truth-intake` | `0 0` versus `origin/main`; `1 0` versus upstream | legal write target; current untracked planning file | all current patch files belong here | low, bounded Governance patch |
| `C:\Nexus Worktrees\FAM-006` | `feature/fam-006-active-overlay-recording-runtime-implementation` | `39 0` versus `origin/main` | branch record/plan, family vision, backlog/roadmap, helper, validation registry, and planning fixtures | `Docs/validation_helper_registry.md`, `dev/orin_user_review_bundle.py`, `dev/orin_branch_readiness_planning_fixture_validation.py` | high reusable-governance overlap; do not mutate product branch |
| `C:\Nexus Worktrees\FAM-007` | `feature/fam-007-dev-owner-skeleton-readiness` | `4 0` versus `origin/main` | branch record/index, generated inventory review files, validation registry, docs audit helper, governance efficiency validator, user review bundle helper | `Docs/validation_helper_registry.md`, `dev/orin_user_review_bundle.py` | medium reusable-governance overlap; do not mutate product branch |

Product-Worktree Carry-Forward Notes:
FAM-006 and FAM-007 branch-local helper repairs show the same false-green family in narrower forms. Governance should generalize them here instead of copying FAM-specific packet-wording lists. Product branch files remain pending USER decisions and must be reconciled after this Governance patch lands.

USER Decision Boundaries:
This candidate does not authorize FAM-006 mutation, FAM-007 mutation, Workstream implementation, SLC implementation, PR creation, merge, release, issue mutation, branch cleanup, runtime/provider/model/shortcut/installer work, private import, or direct-main mutation.

Migration / Backfill Needs:
New or regenerated BP1/BP2/BP3 packets should include both state axes. Existing active product-branch packets may need reissue after rebaseline, but that belongs to the owning product branch after this Governance patch lands and USER approves continuation there.

Rollout Plan:

1. Patch binding source truth with the two-axis Branch Planning Review Gate State Model.
2. Patch helper/validator guidance and fixture checks so reusable false-green cases are machine-checkable.
3. Keep FAM-006/FAM-007 worktrees read-only during this Governance patch.
4. After merge, rebaseline product worktrees and let their owning branches regenerate BP packets under the new model.

Acceptance Criteria:

- Source truth says reviewability is not USER acceptance.
- BP1/BP2/BP3 gate transitions are explicit.
- The helper reports review-packet state separately from implementation approval state.
- Fixture validation rejects a reviewable packet used as implementation approval while USER response is pending.
- Generated USER-facing review aid drift is classified separately from copied source-truth context files.

## Executive Recommendation

The ChatGPT response is directionally correct: the next governance risk is not lack of rules, but owner duplication and architecture/experience drift as AI-native planning grows.

The strongest near-term reform is not to create many new registries immediately. The safer reform is:

1. Add a formal `Architecture / Experience / Policy Impact Matrix` to Branch Readiness / Branch Planning packets.
2. Strengthen the backlog taxonomy rejection tests so architecture layers, experience layers, runtime subsystems, policy owners, and capability domains cannot become FAMs by inertia.
3. Add a compact Source Truth Authority Hierarchy to existing governance owners.
4. Extend `Docs/ai_runtime_and_trust_architecture.md` before creating a separate architecture registry.
5. Add validator guidance to detect architecture/experience/policy owner drift using existing reusable validators first.
6. Add future Main / Dev / Owner repo boundary rules before any private repo split begins.

Cycle Strategy Clarification:

The recommended implementation posture is focused internal governance cycles, not one shallow pass and not one PR per cycle. Each admitted reform area should run through the normal phase path from Branch Readiness through Branch Planning, Workstream, Hardening, and LV1 when applicable. After one reform area completes LV1 or records a documented LV1 not-applicable reason, the work returns to Branch Readiness Stage 1 for the next admitted reform area. PR Readiness, PR creation, merge, and release remain later phases after all admitted cycles and final integration hardening are complete.

## ChatGPT Recommendation Review

| ChatGPT Recommendation | Evaluation | Adjusted Recommendation |
| --- | --- | --- |
| Add `Docs/architecture_layers.md`. | Good problem diagnosis, but premature as a new file unless `No Existing Owner Fits` is proven. | First add an `Architecture Layer Registry` section or appendix to `Docs/ai_runtime_and_trust_architecture.md`. Split to `Docs/architecture_layers.md` only if the owner grows too large or includes non-AI architecture that no existing file owns. |
| Add Branch Readiness Architecture Impact Matrix. | Strongly agree. This is the most practical drift-prevention improvement. | Add a matrix to Branch Readiness / Branch Planning so every branch declares whether it touches Permission-State, Trust Journal, Cache Governance, Deterministic Routing, Provider Orchestration, Competitive Integrity, Experience Layers, and Cross-Family Policies. |
| Add Architecture Drift Validator. | Agree, but use existing validator families first. | Extend `dev/orin_branch_governance_validation.py` and fixture validation before adding a new validator. New helper only after reuse order proves no existing helper fits. |
| Add Formal Experience Layer Registry. | Agree with the need; watch for owner sprawl. | Start with `Experience Layer` rules in `Docs/nexus_vision.md` or `Docs/ai_runtime_and_trust_architecture.md` depending on whether the concept is product-wide UX or AI-runtime behavior. Create `Docs/experience_layers.md` only after placement preflight. |
| Add "What Cannot Become A FAM" rule. | Strongly agree. This is directly aligned with current backlog repair. | Add explicit `Automatic Family Rejection Tests` to `Docs/feature_backlog.md`. |
| Add Governance Memory vs Source Truth Rule. | Agree; partially exists already. | Add a compact `Source Truth Authority Hierarchy` to `Docs/governance_efficiency_operating_model.md`, with a pointer in `Docs/Main.md` only if Main needs it. |
| Add Governance Quickstart. | Agree as onboarding, but it must be non-authoritative. | Create a future `Docs/governance_quickstart.md` as a 15-minute orientation that points to owners and never overrides them. |
| AI Runtime Trust Architecture should become canon. | Mostly already true. | Treat `Docs/ai_runtime_and_trust_architecture.md` as current first-class canon, then strengthen routing and impact checks around it. |
| Add Reliability Class ownership. | Strongly agree. | Add an `AI Reliability Class Model` to `Docs/ai_runtime_and_trust_architecture.md`, with deterministic / high-confidence / advisory / creative classes and proof implications. |
| Biggest risk is governance mirrors. | Strongly agree. | Add a `Governance Mirror Drift Control` rule: one owner, compact mirrors only, generated/index surfaces not hand-authored state. |

## Codex Self-Evaluation

My prior custom-instruction recommendation was useful as a compact app-level behavior shim, but it is not repo source truth and should stay subordinate to Main-first loading.

What it got right:

- Main-first source truth.
- Phase machine.
- Branch Planning before Workstream.
- External state split.
- Protected main.
- Validators as evidence.
- Release Readiness file-freeze.
- Digest non-compaction.

What it should not do:

- Become a parallel governance document.
- Replace `Docs/Main.md`.
- Encode detailed source-truth rules that may drift.
- Add project policy that is not already in repo canon.

Recommended custom-instruction improvement:

Keep app custom instructions compact and stable. They should say "load repo truth and obey it", not try to restate every phase rule.

## Governed Cycle Strategy For This Planning Reform

Cycle Definition:

One governance reliability reform cycle is:

```text
Branch Readiness Stage 1 -> BP1 / BP2 / BP3 -> Workstream -> Hardening -> LV1 if applicable -> return to Branch Readiness Stage 1 for the next admitted cycle
```

The cycle does not include PR Readiness, PR creation, merge, release execution, branch cleanup, FAM worktree mutation, helper implementation, validator implementation, external-state mutation, private repo creation, or repo split execution unless a later USER approval explicitly admits that work in the proper phase.

Cycle Semantics:

- Branch Readiness Stage 1 analyzes the focused reform area, confirms source-truth owner placement, identifies blockers, and asks USER questions.
- BP1 records or confirms the USER-facing vision/reform intent when product, AI behavior, repo split, review UX, or source-truth ownership direction could affect future implementation.
- BP2 records the engineering/source-truth plan for that reform area, including likely files, proof path, checks, stop conditions, and scope exclusions.
- BP3 proves the plan is ready to enter bounded implementation for that reform area.
- Workstream performs only the approved source-truth/planning updates for that area.
- Hardening checks the cycle's actual edits against accepted BP1/BP2 intent, source-truth owner boundaries, and drift risks.
- LV1 applies when USER-facing review, planning digest readability, branch-planning packet shape, PR body shape, or public/private boundary language needs USER-inspectable proof. If LV1 is not materially relevant, record `LV1 Applicability: Not Applicable with reason`.
- After LV1 or documented non-applicability, return to Branch Readiness Stage 1 for the next admitted reform area.

One Final PR Intent:

The preferred outcome is one consolidated PR after all admitted cycles finish and final integration hardening is green. A cycle may require a separate PR only when repo truth or merge-risk analysis shows that combining it would blur source-truth ownership, mix helper/validator code with docs-only contract work, execute private/repo-split work, mutate a FAM worktree, or create release/runtime risk.

### Proposed Cycle Order

| Cycle | Reform Area | Likely Owner Files | LV1 Proof / Waiver | Validation / Check Updates Needed | Drift Risks Introduced | Stop Conditions | Final Hardening Carry-Forward |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Taxonomy / Owner Discipline | `Docs/feature_backlog.md`, `Docs/governance_efficiency_operating_model.md`, compact pointer in `Docs/Main.md` only if needed | USER-readable taxonomy/owner decision proof; LV1 may be not applicable if no USER-facing packet shape changes | Future validator guidance for FAM rejection and owner placement checks | Over-rejecting legitimate future FAMs; duplicating taxonomy across mirrors | `No Existing Owner Fits` unproven; USER wants new FAM identity; owner conflict | Confirm every later cycle uses the same taxonomy vocabulary |
| 2 | Architecture / Experience / Policy Impact Matrix | `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, `Docs/ai_runtime_and_trust_architecture.md`, `Docs/validation_helper_registry.md` | USER-inspectable matrix shape and example decision path | Marker-first validator/fixture guidance after source-truth contract lands | Matrix becomes another ledger; architecture/policy/experience owners conflict | Matrix tries to authorize runtime work; owner class unclear; new owner file requested without preflight | Check Branch Planning, taxonomy, and AI architecture agree |
| 3 | Hypothesis-Driven Reliability | `Docs/ai_runtime_and_trust_architecture.md`, `Docs/nexus_vision.md`, FAM-007 vision pointer if needed | USER-readable explanation that reliability improves accuracy without suppressing adaptive intelligence | Future AI/provider/cache validation guidance for reliability class and evidence labels | Deterministic class flattens ORIN; hypotheses presented as facts; creative/advisory answers over-claim certainty | Reliability class conflicts with AI architecture; FAM-007-specific runtime behavior appears | Check reliability language across architecture, vision, Branch Planning, and FAM-007 |
| 4 | PR / Review Drift Prevention | `Docs/phase_governance.md`, `Docs/workstreams/index.md`, `Docs/branch_plans/README.md`, `Docs/validation_helper_registry.md` | USER-readable PR/review packet shape; stale/readability proof where applicable | Future PR body drift and USER review readability checks | PR body becomes phase digest; USER packet becomes metadata dump; helper green accepted without review | PR body standard conflicts; review packet requires helper code not approved | Check PR Readiness, review hub, helper registry, and digest rules align |
| 5 | Main / Dev / Owner Boundary Planning | `Docs/governance_efficiency_operating_model.md`, `Docs/ai_runtime_and_trust_architecture.md`, `Docs/nexus_vision.md`, `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`, `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md` | USER-readable public/private boundary and promotion-gate proof; no private repo execution | Future private/public leak scan and promotion packet guidance | Governance tries to own FAM-007 implementation; FAM-007 trust work becomes incidental to another branch; private details leak into Main | Requires private repo creation, provider/runtime work, memory/cache implementation, or FAM worktree mutation | Decide whether this stays public-safe governance boundary or moves to a dedicated FAM-007 carrier |

### Final Integration Hardening

After all admitted cycles complete, run one final integration hardening pass before PR Readiness. It must check:

- owner conflicts across every touched source-truth file
- mirror drift and duplicate rule text
- phase wording conflicts
- taxonomy consistency
- validator/helper guidance consistency
- PR/readiness drift
- USER review packet readability
- private/public boundary leakage
- source-truth placement conflicts across all cycles
- whether any cycle introduced a new durable owner without `No Existing Owner Fits`
- whether any FAM-007-specific Main / Dev / Owner implementation detail must be deferred to FAM-007 instead of staying in repo-wide governance

Final PR Decision Rule:

After final integration hardening, decide whether to land the admitted cycles as one consolidated PR, multiple PRs, or a split strategy. Default preference is one consolidated PR for docs-only governance/source-truth contract work. Separate PRs are required when the work mixes docs-only contract with helper/validator code, private repo setup, runtime implementation, external-state mutation, FAM worktree mutation, or high-risk owner-file rewrites.

## Reform Candidate 1 - Architecture Layer Ownership

Problem:

AI-native planning now names durable architecture systems: Permission-State System, Deterministic Routing, Provider Orchestration, Context Engine, Routine Engine, Trust Journal, Competitive Integrity, AI Operational Cache Governance, capability-pack architecture, and Windows Health recommendation boundaries.

Current Owner:

- `Docs/ai_runtime_and_trust_architecture.md`

Risk:

Branches may redefine these architecture layers differently, or treat them as backlog families, runtime implementations, or branch-local details.

Candidate Rule:

Architecture layers are cross-family structural systems. They are not FAMs by default, not runtime authorization by themselves, and not active branch plans. A branch that touches one must cite the owner, classify its impact, and state whether it is extending, consuming, or proposing a change to the architecture layer.

Recommended Owner:

- First pass: `Docs/ai_runtime_and_trust_architecture.md`
- Compact pointer if needed: `Docs/Main.md`
- Validator guidance: `Docs/validation_helper_registry.md`
- Branch packet integration: `Docs/branch_plans/README.md` and `Docs/phase_governance.md`

Implementation Shape:

Add a section such as:

```text
## Architecture Layer Registry

| Layer | Owner | Status | Affected Families | Policy Impact | Runtime Approval Required |
| --- | --- | --- | --- | --- | --- |
```

Do not create `Docs/architecture_layers.md` unless the existing AI runtime/trust owner is proven too broad or non-AI architecture layers require a separate owner.

## Reform Candidate 2 - Experience Layer Ownership

Problem:

Experience concepts such as Calm Technology, Daily Continuity, Ambient Assistance, Session Framing, Interruption Awareness, Assistance Intensity, and Trust-Visible UI may affect many families without being runtime subsystems or backlog families.

Risk:

Experience language may drift between family visions, branch plans, and UI implementation without a clear durable owner.

Candidate Rule:

Experience layers are reusable product interaction principles. They are not FAMs, not active branch plans, and not runtime implementation authority. They route through project vision or a named experience-layer owner before becoming branch acceptance criteria.

Recommended Owner Options:

- `Docs/nexus_vision.md` when the experience layer is project-wide product philosophy.
- `Docs/family_visions/FAM-XXX_*.md` when the experience layer is family-specific.
- `Docs/ai_runtime_and_trust_architecture.md` when the experience layer is AI/trust/provider/cache-specific.
- Future `Docs/experience_layers.md` only after `No Existing Owner Fits`.

Candidate Matrix:

```text
| Experience Layer | Product Meaning | Applies To | Default Owner | Branch Planning Question |
| --- | --- | --- | --- | --- |
```

## Reform Candidate 3 - Cross-Family Policy Owner Classification

Problem:

Some rules are policy, not architecture and not backlog identity: privacy lockdown, local-only mode, provider-cache sanitization, competitive integrity, cache clearability, public/private repo promotion, Owner-data privacy, and release/public-output safety.

Risk:

Policy rules can be scattered across family visions, branch plans, and helper outputs.

Candidate Rule:

Cross-family policy owners define constraints and enforcement expectations across families. A branch that touches a policy must cite the policy owner, state whether it is consuming or changing the policy, and identify the validator/helper impact.

Recommended Initial Owner:

- `Docs/ai_runtime_and_trust_architecture.md` for AI/trust policies.
- `Docs/governance_efficiency_operating_model.md` for source-truth/external-state policies.
- `Docs/phase_governance.md` for phase/proof policies.
- Future policy registry only if repeated policies do not fit existing owners.

## Reform Candidate 4 - Branch Readiness Architecture / Experience / Policy Impact Matrix

Problem:

Branch Readiness currently asks strong product/plan questions, but architecture/experience/policy impacts can still be implied instead of declared.

Candidate Rule:

Every Branch Readiness Stage 1 packet and BP1/BP2 Branch Planning packet for product/runtime/UI/provider/cache/AI work must include an Architecture / Experience / Policy Impact Matrix.

Candidate Fields:

```text
## Architecture / Experience / Policy Impact Matrix

| Owner Class | Named Owner | Touches? | Impact Type | Current Branch Scope | Deferred / Future Scope | Proof / Validation Needed |
| --- | --- | --- | --- | --- | --- | --- |
| Architecture Layer | Permission-State System | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Architecture Layer | Deterministic Routing | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Architecture Layer | Provider Orchestration | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Architecture Layer | AI Operational Cache Governance | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Policy Owner | Privacy Lockdown / Local-Only Mode | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Experience Layer | Assistance Intensity / Interruption Awareness | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
```

Allowed Impact Type:

- `No Impact`
- `Consume Existing`
- `Extend Existing`
- `Change Existing`
- `New Candidate`
- `USER Decision Required`

Blocking Condition:

- `Architecture Impact Unclassified`
- `Experience Layer Impact Unclassified`
- `Cross-Family Policy Impact Unclassified`
- `New Owner Candidate Without Placement Preflight`

Recommended Owner Files:

- `Docs/phase_governance.md` for required gate.
- `Docs/branch_plans/README.md` for packet structure.
- `Docs/feature_backlog.md` for taxonomy link.
- `Docs/validation_helper_registry.md` for validator guidance.

## Reform Candidate 5 - Automatic Family Rejection Tests

Problem:

The backlog should not absorb every important concept. FAMs are broad long-lived product families, not architecture layers, policies, runtime subsystems, capability domains, or branch work packets.

Candidate Rule:

Before Codex proposes or admits a new FAM, it must prove the concept is not better classified as:

- Family vision update.
- Architecture layer.
- Cross-family policy owner.
- Experience layer.
- Runtime subsystem.
- Capability-pack domain.
- Package.
- Slice.
- Seam.
- Workstream evidence.
- External operational state.
- Durable receipt.

If any of those owner classes fit, backlog admission is rejected unless USER explicitly approves new family identity.

Recommended Owner:

- `Docs/feature_backlog.md`

Candidate Blocker:

- `Backlog Family Rejection Test Missing`
- `Backlog Identity Created By Inertia`

## Reform Candidate 6 - Source Truth Authority Hierarchy

Problem:

The project repeatedly has to distinguish source truth from evidence, memory, chat, helper output, and review artifacts.

Candidate Hierarchy:

1. Repo durable source truth.
2. External operational state.
3. Git/GitHub/helper-derived live facts.
4. USER-reviewed local artifacts.
5. Validator/helper output.
6. Codex/ChatGPT response text.
7. Codex memory/chat history.

Important nuance:

Git/GitHub live facts outrank stale repo docs for volatile facts, but do not override durable product/governance law. Repo durable source truth owns governance rules; Git/GitHub owns live facts.

Recommended Owner:

- `Docs/governance_efficiency_operating_model.md`
- Compact pointer only in `Docs/Main.md` if needed.

Candidate Blocker:

- `Authority Hierarchy Ambiguous`
- `Evidence Treated As Source Truth`

## Reform Candidate 7 - Hypothesis-Driven Reliability And Reliability Class Model

Problem:

AI-native features need a consistent proof standard for objective, high-risk, advisory, exploratory, and creative output without making ORIN feel like a rigid calculator.

Product Goal:

ORIN should feel like an extension of human reasoning: curious, evidence-seeking, calm about uncertainty, and capable of forming and refining hypotheses. Deterministic routing should improve accuracy without suppressing adaptive intelligence, exploratory reasoning, or creative problem-solving.

Candidate Reliability Classes:

| Class | Meaning | Default Proof Requirement | Example |
| --- | --- | --- | --- |
| Deterministic | Exact answer/action required | Tool-backed or source-derived proof; no LLM-only truth | Health state, file path, release version |
| High Confidence | Strong evidence required, may include model reasoning | Source citations, validator/helper proof, confidence explanation | Policy routing, setup recommendation |
| Advisory | Guidance or recommendation | Explain basis, alternatives, uncertainty | Planning suggestions, workflow advice |
| Exploratory / Hypothesis | Possible explanations, diagnostic reasoning, missing-context discovery, or evidence-gathering plan | Label as hypothesis, separate observations from inference, ask clarifying questions or propose next evidence | Windows Health diagnosis, planning root-cause analysis, ambiguous UX issue |
| Creative | Open-ended generation | USER acceptance and safety boundaries | Copy, layout ideas, naming candidates |

Candidate Rule:

A branch that adds AI/provider/cache/capability-pack behavior must classify each user-facing AI output path by reliability class and define proof, fallback, cache behavior, Trust Journal requirements, and uncertainty communication requirements.

Observation / Hypothesis / Validation Loop:

1. Notice abnormality or user-stated goal.
2. Separate observed evidence, learned pattern, inferred explanation, uncertain hypothesis, and validated truth.
3. Ask who/what/where/when/why/how questions when missing context controls the answer.
4. Form one or more hypotheses when deterministic proof is unavailable.
5. Seek evidence before recommending action when the action has meaningful risk.
6. Communicate uncertainty calmly instead of using ego-like certainty.
7. Refine, reject, or validate hypotheses as evidence arrives.

Invalid Reliability Behaviors:

- treating experience or learned patterns as unquestionable reality
- presenting hypotheses as facts
- using deterministic class to suppress useful exploratory reasoning
- using creative/advisory language to bypass proof for objective facts
- recommending risky action before seeking available evidence

Suggested Durable Concept Names:

- `Hypothesis-Driven Reasoning Model`
- `Evidence-Seeking Reasoning`
- `Observation / Hypothesis / Validation Loop`
- `Truth Over Fluency, With Curiosity Preserved`
- `Human-Readable Reasoning Summary`
- `Confidence-Calibrated Inquiry`

Recommended Owner:

- `Docs/ai_runtime_and_trust_architecture.md`
- Family-specific implementation in FAM-007 or relevant family vision.

## Reform Candidate 8 - Governance Mirror Drift Control

Problem:

The digest identifies many governance mirrors. The risk is no longer missing policy; it is duplicated policy drifting across Main, phase governance, development rules, codex modes, loader contracts, helper registry, branch records, branch plans, and generated audits.

Candidate Rule:

Every durable governance rule has exactly one owner file. Mirrors must be compact pointers or execution reminders. If a mirror contains detailed rule text, it must name the owner and must not add new semantics.

Candidate Fields:

```text
Rule Owner:
Mirror Files:
Mirror Purpose:
Do Not Duplicate In:
Validator / Helper Owner:
```

Recommended Owner:

- `Docs/governance_efficiency_operating_model.md`

Potential Future Helper:

- Extend existing governance validation to detect conflicting rule definitions by owner phrase/Rule ID where machine-checkable.

## Reform Candidate 9 - Governance Quickstart

Problem:

The governance stack is too large for a new Codex session or contributor to internalize quickly.

Candidate Artifact:

- `Docs/governance_quickstart.md`

Status:

- Non-authoritative orientation only.

Recommended Contents:

- 15-minute governance tour.
- Source-truth load order.
- Phase lifecycle.
- Repo docs vs external state split.
- Backlog taxonomy.
- Branch Planning BP1/BP2/BP3.
- Validators as evidence.
- Common blockers.
- Where to inspect next.

Guardrail:

The quickstart must state that it is not execution authority and must route to Main and owner docs.

## Reform Candidate 10 - Review Packet Human-Readability QA

Problem:

USER-facing packets can drift into metadata dumps or validator output rather than readable decision packets.

Candidate Rule:

Every USER-facing review packet should pass a human-readability QA:

- Plain-language purpose.
- Exact decision requested.
- What USER will see or inspect.
- What will change.
- Options/tradeoffs.
- Open questions.
- Files to inspect.
- Not a validator log dump.
- Technical metadata moved to helper output, external state, or Codex digest.

Recommended Owner:

- `Docs/branch_plans/README.md`
- `Docs/governance_efficiency_operating_model.md`
- `dev/orin_user_review_bundle.py` guidance only after separately approved.

## Reform Candidate 11 - PR Body / PR Creation Drift Prevention

Problem:

USER observed PR body drift and had to manually delete bad PR content.

Candidate Rule:

PR Readiness Stage 1 should explicitly run a PR Body Drift Check before Stage 2 PR creation. The check compares proposed PR body sections against the repo PR output standard and rejects phase-digest fields, next legal phase language, release execution text, broad governance digests, or unapproved scope.

Candidate PR Body Sections:

- `## Summary`
- `## Branch Evidence`
- `## Validation`

Candidate Blocker:

- `PR Body Drift`
- `PR Body Contains Phase Handoff Fields`
- `PR Body Scope Overrun`

Recommended Owner:

- `Docs/phase_governance.md`
- `Docs/workstreams/index.md` where PR summary contract is already described.
- `Docs/validation_helper_registry.md` for helper/validator guidance.

## Reform Candidate 12 - Future Main / Dev / Owner Repo Split Boundary

Problem:

The future vision includes separate Main, Dev, and Owner repositories or repo-like trust zones. Without deterministic boundaries, private state, provider experiments, owner memory, and public source truth can leak across lanes.

Candidate Repository / Trust-Zone Model:

| Zone | Purpose | May Own | Must Not Own |
| --- | --- | --- | --- |
| Main / Public Current Repo | Public-safe app source, durable public governance, product vision, family visions, public architecture, release truth, public-safe validators | Buildable app, public docs, public-safe source truth, release notes, public validators | Secrets, private Owner memory, private credentials, private provider keys, private Dev experiments as authority |
| Dev / Private Development Repo | Private experiments, provider SDK spikes, internal diagnostics, private implementation prototypes, non-public proof | Experimental code, private test harnesses, Dev-only logs, candidate implementation before promotion | Public release truth, accepted governance law unless promoted to Main, Owner-private data |
| Owner / Private Local Repo Or Vault | USER-private preferences, memory, private profiles, local-only Owner data, secrets when later encrypted vault is approved | Owner data, private memory, local vault config, personal context, encrypted secrets | Public app source truth, public governance law, release artifacts, unredacted import into Main |

Candidate Import / Promotion Gates:

- `Main-to-Dev Import Packet`: imports public Main source into Dev for private experimentation.
- `Dev-to-Main Promotion Packet`: promotes sanitized Dev work to Main with public-safety review, license/security review, source-truth placement, validator expectations, and no private data.
- `Owner-to-Main Disclosure Gate`: blocks Owner data from entering Main unless USER explicitly approves a sanitized durable summary.
- `Owner-to-Dev Access Gate`: controls whether Dev tools may read Owner-private state.

Candidate Blockers:

- `Private Data Boundary Missing`
- `Dev-To-Main Promotion Packet Missing`
- `Owner Disclosure Approval Missing`
- `Private Path Leak`
- `Secret / Credential Leak`
- `Shadow Governance In Private Repo`

Recommended Owners:

- `Docs/governance_efficiency_operating_model.md` for repo/source-truth boundary.
- `Docs/ai_runtime_and_trust_architecture.md` for provider/cache/memory/trust implications.
- `Docs/nexus_vision.md` for project-wide privacy/local-first principle.
- `Docs/validation_helper_registry.md` for future scanner/helper guidance.

Cycle 5 Routing Clarification:

This governance reliability reform may define the public-safe Main / Dev / Owner boundary contract, source-truth ownership split, promotion packet concepts, private/public leak-prevention expectations, and ChatGPT/new-chat prompt boundary. It must not implement the split.

FAM-007 should carry later AI/provider/Dev/Owner trust implementation planning when the work becomes concrete FAM-007 behavior, including provider runtime, model behavior, capability-pack behavior, memory/cache implementation, Dev/Owner private roots, private repo creation, private remotes, or private-to-public sanitization workflows.

Governance may plan now:

- Main/Public repo durable source-truth boundary
- Dev/Owner private boundary as public-safe policy
- promotion and disclosure packet concepts
- private reference/path leak-prevention expectations
- ChatGPT/new-chat prompt rule that split state is source-truth-governed, not memory-governed
- cross-repo external state partitioning concept

FAM-007 or a later dedicated split carrier should own later:

- concrete Dev/Owner repo setup
- private provider/runtime behavior
- memory/cache implementation
- Owner/Dev private prompts, roots, remotes, or hosting
- Public-to-Dev import execution
- Dev-to-Main implementation promotion
- Owner disclosure execution

Separate PR Required When:

- Cycle 5 expands beyond public-safe governance/source-truth boundary
- FAM-007 family vision needs a substantive rewrite rather than a compact pointer
- private repo setup, remotes, roots, secrets, memory, provider/model execution, cache runtime, or FAM worktree mutation enters scope
- helper/validator implementation for private/public leak scanning is included

## Reform Candidate 13 - Cross-Repo External State Partitioning

Problem:

If Main, Dev, and Owner split later, `C:\Nexus Governance State` must coordinate operational state without making private state public or letting one repo's state become another repo's authority.

Candidate Layout Extension:

```text
C:\Nexus Governance State\
  repos\
    main\
    dev\
    owner\
  cross_repo_promotions\
  private_disclosure_packets\
  repo_acknowledgements\
```

Candidate Lock Scope Additions:

- Repo lock.
- Cross-repo promotion lock.
- Private disclosure lock.
- Owner-vault access lock.

Candidate Rule:

External operational state may coordinate Main/Dev/Owner workflow, but accepted public governance still returns to Main by USER-approved repo update and merge. Private Dev or Owner state cannot become public source truth by reference.

## Reform Candidate 14 - Private Reference And Path Leak Scanner

Problem:

Future Dev/Owner split increases risk that private paths, branch names, local-only memory, provider keys, model paths, or owner-specific details leak into Main docs, PRs, releases, or USER review bundles.

Candidate Scanner Behavior:

- Scan Main repo docs and PR bodies for private-root path patterns.
- Detect Owner/Dev private references outside approved public-safe summaries.
- Detect provider key/token/cookie patterns.
- Detect local-only model/cache/memory paths.
- Detect private repo branch names in public release notes.

Recommended Helper Strategy:

- Extend existing public-leak / source-owner / governance validators first.
- Add a dedicated scanner only if reuse is not sufficient.

Candidate Blocker:

- `Private Reference Leak`
- `Owner Data Leak`
- `Dev Private Evidence Leak`

## Reform Candidate 15 - Governance Candidate Promotion Queue Hardening

Problem:

External state can hold lessons and governance candidates, but if candidates are not promoted or rejected, important lessons may be lost.

Candidate Rule:

Every cross-worktree lesson, governance candidate, validator candidate, or source-truth placement candidate must have:

- Owner.
- Status.
- Target owner file.
- Promotion path.
- USER decision state.
- Final disposition.
- Expiration or review trigger.

Recommended Owner:

- `Docs/governance_efficiency_operating_model.md`
- `Docs/external_operational_state_store_reform_plan.md`
- External state schemas after a later approved external-state schema pass.

## Reform Candidate 16 - Error Checking Improvements

Recommended future machine-checkable gates:

- Architecture / Experience / Policy Impact Matrix present when product/runtime/UI/provider/cache/AI scope exists.
- FAM rejection tests completed before any new FAM/package identity proposal.
- Source Truth Authority Hierarchy cited when evidence conflicts.
- PR body drift check before Stage 2 PR creation.
- USER review packet human-readability QA.
- Private Dev/Owner leak scan for Main-facing PR/release/review outputs.
- Governance mirror drift scan for owner/mirror contradictions.
- Reliability class declaration for AI user-facing outputs.
- Dev-to-Main promotion packet check before importing private Dev work.
- Owner disclosure gate before any Owner-private data becomes public durable source truth.

## Reform Candidate 17 - Efficiency Improvements

Recommended future efficiency moves:

- Keep Main compact and router-only.
- Avoid creating one file per concept unless placement preflight proves no existing owner fits.
- Prefer sections in existing owner files for architecture, experience, policy, and reliability until they outgrow the owner.
- Use generated reports for inventory/drift views; do not hand-maintain global indexes.
- Keep active operational state external.
- Keep USER review packets concise and decision-focused.
- Use one consolidated governance reliability PR for related owner-model improvements instead of many tiny PRs, but only after exact owner files and validators are named.

## Reform Candidate 18 - Reliability Improvements

Recommended future reliability moves:

- Add `Reliability Class` to AI/provider/capability Branch Planning packets.
- Require deterministic outputs to cite tool/source proof.
- Require high-confidence outputs to include evidence and confidence basis.
- Require advisory outputs to show alternatives/tradeoffs.
- Require creative outputs to remain USER-accepted before implementation.
- Tie reliability class to cache behavior, Trust Journal recording, provider routing, and fallback.

## Reform Candidate 19 - Drift Prevention Improvements

Recommended future drift controls:

- One owner per durable rule.
- Compact mirrors only.
- New files only after `No Existing Owner Fits`.
- PR body drift check.
- Architecture/experience/policy matrix.
- Private split boundary scan.
- Source-truth authority hierarchy.
- External-state candidate promotion queue.
- Branch Planning packet stale guard remains mandatory.
- Validators remain evidence, not authority.

## Proposed Implementation Staging

This planning file recommends cycle-based implementation, not one shallow source-truth pass and not one PR per reform area.

### Stage A - Planning File Review

Current file only. USER reviews this recommendation set and decides whether to admit the cycles.

No binding source-truth law changes.
No validators.
No helpers.
No PR requirement unless USER wants to preserve this planning artifact.

### Stage B - Admitted Governance Reliability Cycles

Run each admitted reform cycle through the phase-consistent path:

```text
BR1 -> BP1/BP2/BP3 -> Workstream -> Hardening -> LV1 if applicable -> return to BR1
```

Cycle admission should name:

- reform area
- source-truth owner files
- expected write set
- proof needed before leaving the cycle
- LV1 applicability
- validation/check guidance changes
- drift risks
- stop conditions
- carry-forward items for final integration hardening

### Stage C - Final Integration Hardening

After all admitted cycles complete, run a final hardening pass across the combined reform surface. This pass decides whether the cycles are coherent enough for PR Readiness or whether a repair cycle is required.

### Stage D - PR Strategy Decision

After final integration hardening, choose:

- one consolidated PR for docs-only governance/source-truth contract work
- separate PRs when code/helper/validator/private/repo-split/FAM-specific work enters scope
- a split strategy when merge risk or owner conflict makes one PR unsafe

### Stage E - Later Helper / Validator / Repo Split Work

Helper code, validator code, private/public leak scanners, architecture drift scanners, repo split execution, private repo creation, external-state mutation, FAM worktree mutation, and runtime/provider/model/memory/cache behavior remain separate USER decisions after the docs/source-truth contract work.

## Recommended Next USER Decision

The admitted Governance Reliability / Repo Split Reform source-truth contract cycles and final integration hardening are complete. The next legal USER decision is PR Readiness Stage 1 analysis.

Suggested exact decision shape:

```text
I approve PR Readiness Stage 1 analysis for the Governance Reliability / Repo Split Reform source-truth contract on C:\Nexus Worktrees\Governance / feature/release-readiness-source-truth-intake.

Stage 1 may analyze PR readiness, repair only bounded current-branch PR-readiness drift if source truth permits, run validation, and return the Stage 1 packet. This does not approve PR Readiness Stage 2, PR creation, merge, release, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, FAM-006/FAM-007/main mutation, runtime/provider/model/shortcut/installer work, issue mutation, cleanup, Private Dev ORIN import, AI Product Contract import, or helper/validator code expansion beyond already-approved current-branch repair.
```

Other legal USER responses:

- Request more hardening detail before PR Readiness.
- Choose a limited split PR strategy if Stage 1 finds merge-risk.
- Block PR Readiness and request another Governance reform cycle.

## Final Recommendation

ChatGPT's strongest insight is correct: the next governance risk is ownership duplication. The best repair is not "more governance everywhere"; it is better owner classification before new concepts become FAMs, architecture systems, policies, experience layers, or implementation work.

Recommended priority order:

1. Taxonomy / Owner Discipline.
2. Architecture / Experience / Policy Impact Matrix.
3. Hypothesis-Driven Reliability.
4. PR / Review Drift Prevention.
5. Main / Dev / Owner boundary planning, public-safe only unless a later FAM-007 or split carrier is approved.
6. Governance quickstart.
7. Optional explicit registries only after existing owners prove insufficient.
