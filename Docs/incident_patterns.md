# Incident Patterns

## Purpose

This document captures short reusable debugging and validation patterns extracted from closed workstreams.

It is a generalized knowledge layer, not a case-history diary.

Use:

- canonical workstream docs for the full story of a specific lane
- this document for reusable symptom-to-fix patterns
- the relevant canonical workstream doc first for branch-local reuse notes, artifact guidance, and seam history

Add material here only when the lesson has generalized beyond one lane.
Branch-local "what worked" notes should stay in the canonical workstream doc first and only be distilled here once the pattern is broad enough to help future branches outside that lane.

## Pattern: Automation CWD Worktree Mismatch Must Not Become Lane Truth

- symptom:
  a standing watcher or automation reports blockers from stale `C:\Nexus Desktop AI`, a parked worktree, a missing configured cwd, or the wrong FAM/Governance lane while the actual active worktree has different branch truth
- layer:
  Automation Observability, multi-worktree identity, and PR/Release Readiness reporting
- root-cause pattern:
  Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md` were treated as lane truth without first proving the automation's configured cwd, worktree role, branch, `HEAD`, and `origin/main`
- fix pattern:
  run `dev/automation_observability_report.py`, classify stale or wrong-lane automation reports as `Automation CWD Worktree Mismatch`, and let only `BLOCKER_CANDIDATE` or `REVIEW_REQUIRED` findings enter a bounded repair seam. Lane-sensitive prompts for active branch, PR Readiness, Release Readiness, post-merge, release-window, selected-next, toolchain, or branch governance must be rebound to the intended worktree or reported as stale evidence instead of mutating canon. Background-observability-only automations cannot clear watcher-exception proof, merge verification, release readiness, or same-PR repair proof, and stale historical toolchain-path memory remains `REVIEW_INFO` unless current source truth still owns the referenced path. USER-approved `automation/worktree governance intake` may use the `Standing Governance Intake Branch` only for non-runtime multi-worktree automation safety repair under `RRI-YYYYMMDD-NNN`, `One Active Cycle`, `Sync Rule`, `Waiting For Governance Intake`, and `Return Digest`.
- validation pattern:
  run `python dev\automation_observability_report.py` and `python dev\orin_branch_governance_validation.py`; the report must surface missing/stale/wrong configured cwd as a blocker candidate and the governance validator must require the automation/worktree contract across the source-truth homes
- source references:
  - `Docs/phase_governance.md`
  - `Docs/Main.md`
  - `dev/automation_observability_report.py`
  - `dev/orin_branch_governance_validation.py`

## Pattern: PR Readiness Green Must Require Durable Process Truth

- symptom:
  PR Readiness can appear green while required canon sync, post-merge state handling, docs changes, PR creation, or PR validation still have not completed
- layer:
  branch governance, merge-target canon, and PR-state validation
- root-cause pattern:
  validation proves branch behavior or produces a copy-ready PR package, but process blockers are not named strongly enough as pre-merge gates
- fix pattern:
  require PR Readiness to clear stale canon, post-merge-state handling, next-workstream selection with runtime minimal scope and no branch created yet, `Next Runtime Candidate Selection Pending`, dirty branch / durable commit state, docs-sync / Governance Drift Audit blockers, Automation Observability Review Pending via `dev/automation_observability_report.py` over Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`, with `BLOCKER_CANDIDATE` and `REVIEW_REQUIRED` findings treated as repair candidates, PR creation, explicit green merge-status proof, and PR validation before reporting `PR READY: YES` or `PR Readiness GREEN`; `PR package ready` is not green, missing PRs carry `PR Creation Pending`, unknown PR inspection carries `PR State Unknown`, mergeability or merge-state that has not explicitly reported green carries `PR Merge Status Unproven`, unresolved live PR issues carry `PR Validation Pending`, the same-PR Codex bot-review repair loop requires actionable bot comments to be fixed on the same PR, pushed, replied to, resolved, revalidation-requested with a 3-5 word PR comment, and then cleared by a later Codex Connector bot thumbs-up reaction or green approval comment before PR green, and Stage 2 final handoff cannot be green until the post-repair bot thumbs-up/approval latch is verified. Bounded PR2 uses direct PR verification by GitHub connector, `gh`, GraphQL review-thread inspection, status checks, reactions where available, mergeability, head SHA, and merge/close state. The Direct PR2 Continuation Rule blocks quiet handoff after revalidation requests or repair pushes while direct verification can continue. Recurring PR watcher automation is denied by default; watcher-based PR monitoring is exception-only after explicit USER approval for the exact PR, and then `PR Watcher Routing Unverified`, watcher delivery proof, source-of-truth shaped watcher output, and watcher teardown/retirement proof apply only to that exception path. `PR Merge Verification Pending` stays active until direct GitHub/GitHub-connector verification proves the PR is actually merged.
  Treat review-risk/adversarial coverage as a normal PR Readiness Stage 1 field rather than a special optional blocker. For helper, validator, fixture, packet, RAR, UIREF, Product Experience, PR, release, or issue-governance changes, Stage 1 must include rule-to-code-to-fixture mapping and adversarial negative/false-positive coverage for the changed parser or proof family before PR creation, so GitHub PR review is not the first place marker-only, malformed-table, path-root, casing, hyphenation, negation, contradictory-prose, or sibling fixture gaps are discovered.

- validation pattern:
  run the normal branch governance validator plus the PR-readiness gate mode; the gate must fail while the worktree is dirty, while required post-merge truth is not encoded, while the next runtime workstream is undefined, unscoped, not runtime, or already branched, while `Next Runtime Candidate Selection Pending` is active, while the PR does not exist, or while PR state cannot be inspected
- source references:
  - `Docs/phase_governance.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: PR Review Churn Means Adversarial Coverage Failed

- trigger:
  an open PR accumulates repeated actionable Codex Connector comments in the same helper, validator, parser, fixture, RAR, UIREF, Product Experience, packet, PR, release, or issue-governance family, total Codex Connector review comments exceed the configured review-churn budget, or each repair closes the latest literal comment while a sibling false-green or false-red appears next
- layer:
  PR Readiness Stage 1, PR Readiness Stage 2, same-PR repair loops, helper/validator/fixture changes, generated USER packet checks, RAR adoption reviews, UIREF/Product Experience enforcement, and parser-heavy natural-language/Markdown validators
- root-cause pattern:
  Codex treats each PR comment as an isolated bug, adds an exact fixture, pushes, and re-requests review without first building a comment-family threat model; the PR bot becomes the first adversarial fuzzer and exposes defects that Stage 1 should have caught. Resolved review-thread state can hide the upstream PR1 miss unless high-volume churn itself is treated as failed pre-PR prediction.
- fix pattern:
  stop PR continuation on `Review Churn Root-Cause Gate Active`, build a Review-Comment Pattern Matrix from all same-family comments, identify the missing source-truth rule, parser assumption, helper/validator seam, fixture family, generated mutation/adversarial case, and sibling-risk set, then repair the durable owner and validator harness before any further review request. After the repair, run the local pre-PR adversarial firewall so changed helper/validator/parser files, corpus comments, unknown-comment guardrails, generated mutation variants, and sibling replay variants are green before another `@codex` request.
- validation pattern:
  require proof that each repaired family has source-truth coverage, code enforcement, static positive/negative fixtures, generated mutation/adversarial variants or an equivalent harness, targeted validator output, full registered validation, every GitHub review-thread page and every pull-review-comment page inspected, total/resolved/unresolved/outdated/unresolved-current thread counts reported, every Codex Connector review comment clustered into a covered family, changed helper/validator/parser file coverage proven, review-churn budget status reported, exact root-cause receipt proof when the budget is exceeded, current-head green/approval latch handling that includes Codex Connector thumbs-up reactions when that is the live approval proof, a final local Codex Connector simulation digest listing remaining sibling risks as cleared, waived, routed, or blocked, and a pre-PR firewall result from `dev/orin_pr_review_churn_validation.py --pre-pr-firewall` before PR creation or another review request when helper/validator/parser-family files changed. Pre-PR firewall manifests must run nested Python validation through the portable `{python}` token so Windows-only or POSIX-only launcher assumptions cannot become the first PR-bot finding.
  budget and parser precision checks must also include sibling false-red coverage: total-comment budget overruns and same-family budget overruns are independent receipt triggers, and no-decision wording must not negate affirmative proof/receipt text unless the proof or receipt itself is pending, missing, unrecorded, or unverified. A genuinely multi-family Connector comment must retain every matched covered family; keyword disambiguation may remove a false-positive family but must not discard a real exact-scope family merely because another family also matches. Exact-scope comments with explicit whole-word `RAR` context must retain genuine RAR families; incidental letter sequences such as `rar` inside `arbitrary` are not RAR context.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/validation_helper_registry.md`
  - `Docs/pr_watcher_mode_contract.md`
  - `dev/orin_pr_review_churn_validation.py`
  - `dev/fixtures/pr_review_churn/`
  - `dev/orin_branch_readiness_planning_fixture_validation.py`

## Pattern: Packet Validation Must Not Become USER Acceptance

- symptom:
  BP1, BP2, or BP3 USER review packets validate cleanly while stale wrong-family, wrong-phase, placeholder, prior-gate-pending, or implementation-ready wording still appears in generated USER-facing review aids, and Codex then asks for the next Branch Planning gate or Workstream implementation before the USER response has been accepted, waived, revised, rejected, or blocked in source truth
- layer:
  Branch Planning, USER review hub packets, helper/validator interpretation, and Codex phase handoff digests
- root-cause pattern:
  packet generation, file-list validation, stale-zip checks, or helper `PASS` output was treated as if USER had accepted the Branch Vision, accepted the Branch Plan, approved BP3 orchestration, or authorized Workstream implementation. Reviewability and USER acceptance were not tracked as separate state axes.
- fix pattern:
  require every BP1/BP2/BP3 review packet to preserve `Packet Reviewability State` separately from `USER Gate State`. A `Reviewable` packet starts the USER Review Gate; it does not close it. BP2 preparation requires BP1 `USER Accepted` or `USER Waived`, BP3 preparation requires BP2 `USER Accepted` or `USER Waived`, and first Workstream implementation approval may be requested only after BP3 is `USER Approved` or `USER Waived` plus a separate USER implementation decision path exists. Generated USER-facing files and extra review aids must be stale-scanned separately from copied source-truth context files.
- validation pattern:
  run `python dev\orin_user_review_bundle.py` for packet validation when applicable, `python dev\orin_branch_readiness_planning_fixture_validation.py`, and `python dev\orin_branch_governance_validation.py`. The validators must reject `Packet Validation Treated As USER Acceptance`, `Review Gate Bypass`, `USER Review Packet Phase-State Conflict`, `USER Review Packet Not Digested`, `Branch Planning Acceptance Receipt Missing`, `Helper False Green On Review Gate State`, and `Codex Digest Conflicts With USER Packet`.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/validation_helper_registry.md`

## Pattern: USER Packet Folder/ZIP Drift Can Hide Stale Review Evidence

- symptom:
  a USER review packet folder looks current, but `C:\Nexus USER` still contains a previous same-label timestamped ZIP, a legacy stable-name ZIP such as `Governance.zip`, a ZIP whose contents no longer match the folder, more than one primary review file, stale stage wording, or manually assembled packet files outside the approved layout
- layer:
  local USER review hub, Governance review/evidence packets, Branch Planning packets, PR Readiness packet proof, helper/validator interpretation, and ChatGPT upload artifacts
- root-cause pattern:
  Codex manually assembled or regenerated a packet without running the same deterministic cleanup and validation path as `dev/orin_user_review_bundle.py`, so folder readability, timestamped filename, or successful upload was mistaken for proof that stale same-label artifacts and wrong-stage surfaces were gone
- fix pattern:
  treat `C:\Nexus USER\<worktree-label>` as a clean-regenerated packet root, not an incremental folder. Before USER review or PR Readiness, prove root `START_HERE.md`, `USER Review` / `Review Aids` / `Source Truth Context` layout, exactly one current-gate primary file under `USER Review`, mandatory timestamped ZIP `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip`, no legacy stable `C:\Nexus USER\<worktree-label>.zip`, no previous same-label timestamped ZIPs, ZIP-beside-folder placement, duplicate ZIP entry rejection, folder/ZIP file-list plus content-hash parity, unresolved-placeholder absence, stale-stage scan, and final packet proof reporting. If a packet was assembled outside the normal build path, run `dev/orin_user_review_bundle.py --validate-local-user-packet <folder> --review-export-zip <timestamped-zip> --worktree-label <label> --packet-validation-mode active-review --expected-branch <branch> --expected-head <HEAD> --expected-origin-main <origin-main>` before treating it as current.
- validation pattern:
  run `python dev\orin_user_review_bundle.py --validate-local-user-packet <folder> --review-export-zip <timestamped-zip> --worktree-label <label> --packet-validation-mode active-review --expected-branch <branch> --expected-head <HEAD> --expected-origin-main <origin-main>` for existing current local packets. Active-review validation requires all three explicit identity values; do not omit them or treat a structural PASS as currentness proof. Run `python dev\orin_branch_readiness_planning_fixture_validation.py` for regression fixtures and the normal governance-efficiency validation. Any stale same-label ZIP, stable-name ZIP, copied ZIP outside the packet folder parent, duplicate ZIP entry, layout drift, primary-file count drift, folder/ZIP file-list mismatch, or folder/ZIP content-hash mismatch blocks on `USER Review Packet Stale`.
- source references:
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/development_rules.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_user_review_bundle.py`

## Pattern: Active Packet Identity Can Be Masked By Structural PASS

- symptom:
  an existing USER packet passes folder layout, ZIP readability, substantive-content, or folder/ZIP parity checks while its active branch, HEAD, origin/main, or copied source context belongs to an older checkout
- layer:
  USER packet generation, active-review validation, accepted-historical evidence, and PR Readiness packet proof
- root-cause pattern:
  the validation-only path accepted identity as contextual text and did not require explicit expected branch/HEAD/baseline inputs, so structural PASS was mistaken for current active-review proof
- fix pattern:
  active-review validation fails closed without expected identity arguments and independently validates both folder and ZIP identity; accepted-historical mode preserves its recorded historical identity without requiring current Git equality
- validation pattern:
  run active-review positive, wrong-branch, wrong-HEAD, wrong-baseline, missing-argument, stale-folder, stale-ZIP, and folder/ZIP-disagreement fixtures, then run accepted-historical preservation fixtures
- source references:
  - `Docs/phase_governance.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_user_review_bundle.py`
  - `dev/orin_user_review_bundle_false_green_fixture_validation.py`

## Pattern: One External Root HEAD Cannot Prove Every Target Current

- symptom:
  a strict external-state validator reports many unrelated records as stale because it applies one expected source HEAD to multiple worktrees, or a target-scoped PASS is interpreted as proof that the complete external root is current
- layer:
  External Operational State Store, worktree/branch projections, root manifest, target reconciliation, and local governance validation
- root-cause pattern:
  the root manifest and global strict validator were used without a target-currentness contract that distinguishes live projections from historical receipts, names the selected target, and records per-target identity expectations
- fix pattern:
  preserve global modes, add target-scoped validation with one relative target, per-target branch/head/baseline/worktree/slot values, hash precondition, path security, TOCTOU detection, record-class checks, and explicit scoped-PASS output; reconcile records only through `dev/orin_external_state_target_reconcile.py`, then release locks through `dev/orin_external_state_lock_release.py`
- validation pattern:
  run valid, wrong-identity, stale-hash, missing/duplicate/alias, traversal/off-root, reparse/symlink, malformed, historical, multi-head, stale-manifest, TOCTOU, global-regression, and scoped-PASS fixture families
- source references:
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/phase_governance.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_external_state_validation.py`
  - `dev/orin_external_state_common.py`
  - `dev/orin_external_state_target_reconcile.py`
  - `dev/orin_external_state_lock_release.py`

## Pattern: Backend Runtime Truth Hidden Behind UI Green

- symptom:
  Codex validates UI shape, screenshots, helper output, or logs while the runtime/backend state owner, deterministic inputs/outputs, lifecycle/state machine, failure/fallback/recovery route, schema/config compatibility, rollback path, or user-facing status/error mapping remains unspecified
- layer:
  runtime/backend Branch Readiness, BP2/BP3 engineering plans, Workstream, Hardening, Live Validation, PR Readiness, USER review packets, and branches that expose user-visible state from runtime/backend behavior
- root-cause pattern:
  UI/UX proof became more explicit than backend/runtime proof, allowing a surface to appear green, disabled, blocked, successful, recovered, or degraded without proving that runtime truth supports that visible state
- fix pattern:
  require a Backend Predictability / Reliability Contract for runtime/backend-affecting work; require frontend/backend contract consistency so every user-visible state label, disabled action, blocked action, recovery option, success claim, failure claim, degraded state, and unavailable state maps to runtime truth, policy truth, or a USER-approved exception; treat backend logs as diagnostic evidence, not USER-facing proof by themselves; if rebaseline/re-entry discovers issues in already-implemented or previous branch output outside the current legal repair scope, prepare a USER-reviewed issue-candidate packet and stop before GitHub mutation
- validation pattern:
  future helpers should fail on `Backend Predictability Contract Missing`, `Runtime State Owner Missing`, `Runtime State Machine Missing`, `Nondeterministic Backend Behavior`, `Failure Path Missing`, `Fallback Behavior Hidden`, `Schema Migration Proof Missing`, `Config Compatibility Proof Missing`, `Backend/UI Contract Mismatch`, `User-Facing State Not Backed By Runtime Truth`, `Backend Logs Treated As User Proof`, `Recovery Route Missing`, `Rollback Path Missing`, `Issue Candidate Disposition Missing`, or `Issue Mutation Approval Missing` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/development_rules.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Template Or Golden Reference Claimed Before Promotion

- symptom:
  Codex treats a good active branch output, ChatGPT example, screenshot, control cluster, design discussion, or current FAM-007 packet as if it were a promoted template, golden reference, shared primitive, or design-token authority
- layer:
  FAM-002 presentation governance, UI/UX planning, Visual Inheritance Matrix rows, Scope Coverage Manifest rows, Live Validation visual adjudication, USER packets, and Governance PR-hold decisions
- root-cause pattern:
  future template/golden-reference work is needed, but a branch collapses the future USER-reviewed promotion decision into current proof and causes other branches to inherit an unapproved or stale UI surface
- fix pattern:
  keep FAM-002 presentation grammar binding now, but keep templates/golden references/design tokens/shared primitives blocked until the dependency chain clears and USER approves promotion; until then, branches must compare against current source-truth grammar, accepted reference surfaces where they already exist, screenshots/video/manual validation, and USER review, not a claimed future template
- validation pattern:
  future helpers should fail on `Template Dependency Unresolved`, `Golden Reference Promotion Blocked`, `Shared Primitive Promotion Blocked`, `Limited PR Path USER Approval Missing`, or `Template Treated As Existing Proof` when a branch claims a reference without a valid promoted `Docs/ui_reference_catalog/UIREF-*` record. When a UIREF record exists, helpers should enforce the record's known limitations and adoption rule rather than keeping the entire reference class blocked.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/governance_reliability_and_repo_split_reform_candidates.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_user_review_bundle.py`
  - `dev/orin_branch_readiness_planning_fixture_validation.py`
  - `dev/orin_branch_governance_validation.py`

## Pattern: GitHub Issue Live State Must Not Become Repo Ledger

- symptom:
  Branch Readiness, PR Readiness, or Release Readiness references issue numbers, returned UTS issue forms, diagnostics issue flows, or PR review issue evidence without a deterministic scan/disposition, then repo docs start acting like the current issue queue or Release Readiness misses closeout candidates.
- layer:
  Branch Readiness issue intake, PR body generation, Release Readiness closeout, branch records, branch plans, and GitHub issue state.
- root-cause pattern:
  GitHub issue state is live operational truth, but source truth only had broad live-state boundary language. Without a named issue intake and closeout gate, Codex could skip relevant open issues, preserve inconsistent receipt field names, or put stale open/closed/current issue posture into repo docs.
- fix pattern:
  run the `GitHub Issue Relevance Intake Gate` during Branch Readiness and rebaseline/reconciliation when issue evidence can affect scope; classify each issue as current-FAM, other-FAM, cross-FAM, duplicate/superseded, not applicable, USER triage, or live-state unknown; disposition current/cross-FAM issues; keep temporary scan evidence in helper output, Codex digest, USER packets, or external state; and fold down only durable issue receipts in branch records.
- validation pattern:
  future helpers should report missing issue scans, missing dispositions, live-state unknowns, and repo issue-ledger leakage. Green validation is evidence only; Codex must still verify the issue source and disposition.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/branch_records/index.md`
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Rebaseline Adoption Review Repairs One Sample And Misses Owned Surface Drift

- symptom:
  after a rebaseline or merged governance/UIREF/proof standard, Codex repairs one visible defect or validates marker coverage, then reports the branch green while other owned windows, controls, element groups, previous-branch surfaces, or issue candidates still visibly fail the current Project Vision, NDAI Product Experience Contract, FAM-002 grammar, UIREF reference, or Live Validation proof standard
- layer:
  rebaseline/reconciliation, Merged Vision Standard Adoption Review, RAR, UIREF adoption, active external branch plans, USER packets, Live Validation, and GitHub issue-candidate routing
- root-cause pattern:
  the prompt or phase allowed immediate repair without first forcing a full owned-surface inventory, code-to-visual trace, accepted-reference comparator, UI element inventory, backend/state ownership trace, screenshot/video/contact-sheet evidence, previous-branch issue-candidate ledger, and USER packet. Existing source truth also allowed issue candidates to be optional language in some places, so out-of-scope defects could disappear as "not current branch scope" instead of becoming USER-reviewable issue candidates. Another recurring variant is circular proof: the helper, marker, validator, plan, or attractive screenshot that claimed a surface green became the only evidence that the surface actually matched the accepted UIREF/reference.
- fix pattern:
  require the `Rebaseline Adoption & Reconciliation Phase` when merged standards may affect existing branch work. RAR must inventory owned surfaces, map affected code lines/selectors/widgets to visible element groups, compare UI against promoted UIREF records or the strongest accepted reference seed, compare affected output against the NDAI Product Experience Contract qualities of deterministic, intuitive, immersive, predictable, reliable, and consistent, trace backend/state ownership behind visible claims, classify template/shared-primitive/source-truth/reference gaps, produce a USER packet when findings need review, and prepare issue candidates for prior/out-of-scope owned defects before normal phase progression resumes. The owning worktree repairs only its legal branch-local scope; sibling mutation and issue mutation remain USER-gated.
- validation pattern:
  future helpers should fail on `Rebaseline Adoption Review Missing`, `Affected Surface Inventory Missing`, `Owned Surface Nonconformance Ledger Missing`, `Accepted Reference Comparator Missing`, `NDAI Product Experience Contract Comparison Missing`, `Product Experience Contract Nonconformance Unresolved`, `Code-To-Visual Trace Missing`, `Backend State Ownership Trace Missing`, `Screenshot Contact-Sheet Proof Missing`, `Circular Validation Evidence`, `Visual Comparator Matrix Missing`, `Current Branch Repair Vs Issue Boundary Missing`, `Owned Surface Issue Candidate Missing`, `RAR USER Packet Missing`, `Reference Parity Claim Unsupported`, `Source-Truth Gap Unrouted`, `Reference Gap Unrouted`, `Unproven Owned Surface`, `RAR Live Adoption Ledger In Repo`, `RAR Evidence Lost To Chat Digest`, `RAR Packet Missing For USER Judgment`, or `Partial Repair Reported Complete` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/validation_helper_registry.md`
  - `Docs/user_test_summary_guidance.md`

## Pattern: RAR Issue Candidates Become Packeted-Only And Disappear

- symptom:
  RAR finds owned-surface or previous-branch defects and prepares issue candidates, but a later packet or phase digest treats `packeted only`, `issue candidate packet USER-reviewed`, or copied-context issue tables as closure. The candidate no longer appears as a primary USER decision, has no durable owner/route/GitHub mapping, and can be lost when a newer packet narrows the current branch scope.
- layer:
  RAR, active external branch plans, USER packets, GitHub issue-candidate routing, Branch Planning re-entry, PR Readiness, Release Readiness, and issue-governance helper checks
- root-cause pattern:
  the RAR packet requirement recorded issue-candidate evidence but did not require stable candidate ID/lineage, durable disposition vocabulary, progression-blocking classification, last GitHub state verification, or active USER-packet carry-forward. Packet generation/reviewability was allowed to behave like disposition, and helper checks focused on marker presence instead of candidate continuity.
- fix pattern:
  require the `RAR Issue-Candidate Durability Gate`. Every active candidate must keep a stable ID or lineage fingerprint, owning FAM, surface, element group, defect, evidence pointer, current disposition, blocking status, proposed carrier, GitHub issue state when mapped, last verified source/time, and exact USER decision. Legal exits are repaired and independently verified, USER rejected with reason, USER waived with reason/scope, deferred with durable owner/reason/target/trigger, routed with carrier acceptance receipt, approved for GitHub issue creation pending mutation, mapped to open GitHub issue, or mapped to closed GitHub issue and reconciled against repair evidence. `Packeted only` is transport evidence, not closure.
- validation pattern:
  future helpers should fail on `RAR Issue Candidate Durability Missing`, `RAR Issue Candidate Lineage Missing`, `RAR Issue Candidate Durable Disposition Missing`, `RAR Issue Candidate Disappeared From Active Packet`, `RAR Issue Candidate Packeted Only`, `RAR GitHub Issue State Unknown`, `RAR GitHub Issue Mapping Stale`, `Issue Candidate Table Only In Copied Context`, `Deferred Issue Candidate Owner Missing`, `Duplicate Issue Candidate Lineage`, or `Repaired Issue Candidate Verification Missing` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/validation_helper_registry.md`

Follow-up hardening: the executable durability gate must test packet, ledger, and GitHub snapshot parity together, not only scan one Markdown file. A candidate table in `Review Aids` or copied source-truth context is not a primary USER decision surface. Active external-ledger candidates must either appear in the primary packet decision surface or have explicit predecessor/successor lineage; terminal repaired/rejected/waived/closed-reconciled history may remain external/history-only when no current USER decision remains. GitHub issue mappings require read-only open/closed snapshot agreement and independent reconciliation for closed mappings; a parsed but unused snapshot is a false green.
  - `dev/orin_rar_issue_candidate_durability_validation.py`

## Pattern: Issue Candidates Become GitHub Issue Sprawl

- symptom:
  RAR, UTS, Live Validation, or Branch Readiness identifies many atomic defects and Codex proposes one GitHub issue per tiny element, or requests issue creation without showing how candidates should be grouped.
- layer:
  RAR issue-candidate packets, GitHub issue creation approval, active external branch plans, USER packets, BR1/BR2 successor planning, and PR Readiness fold-down.
- root-cause pattern:
  atomic issue-candidate durability was required, but the USER-facing issue-creation decision did not require a consolidation step that groups related defects by owning FAM, surface, defect class, likely repair carrier, and validation path.
- fix pattern:
  require the `Issue Candidate Consolidation Gate` before GitHub issue creation is requested. Preserve every atomic candidate ID and lineage, but recommend the fewest coherent GitHub issues that preserve traceability. USER must be able to create, map to existing issue, defer to FAM ledger, split, merge, reject, or waive each group.
- validation pattern:
  future helpers should fail on `Issue Candidate Consolidation Missing`, `GitHub Issue Group Without Atomic Traceability`, `Issue Group Missing USER Choice`, or `Issue Mutation Requested Before Consolidation` when machine-checkable.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Reference Standard Vocabulary Collapses Into Ambiguity

- symptom:
  Codex treats a Vision Contract, accepted reference, screenshot, template, shared primitive, helper output, or validator green as interchangeable proof, then branches either improvise standards silently or assume a reference worked even after repeated repair cycles.
- layer:
  Project Vision, Family Vision, Family Feature Vision, UIREF, RAR, BP1/BP2/BP3, Workstream, Hardening, Live Validation, PR Readiness, and future non-UI standard families.
- root-cause pattern:
  UIREF created the first durable reference catalog, but the broader Reference Standard lifecycle and no-confusion vocabulary were not stated compactly across phase carrydown.
- fix pattern:
  use the Reference Standard lifecycle `Candidate -> USER Review -> Promoted Reference -> Consumed By Branch -> Effectiveness Reviewed -> Updated / Superseded / Deferred`. Keep Vision Contract as broad product law; Reference Standard as detailed comparator; Template as scaffold; Shared Primitive as reusable implementation source. RAR enforces/adopts merged standards but does not create them; BP can identify missing standards; PR Readiness Stage 1 reviews whether standards worked and records repair/supersession/defer candidates.
- validation pattern:
  future helpers should fail on `Reference Standard Review Missing`, `Claimed Standard Without USER Promotion`, `Reference Effectiveness Note Missing`, `Reference Standard Repair Candidate Required`, or `Template / Primitive / Reference Collapsed` when machine-checkable.
- source references:
  - `Docs/nexus_vision.md`
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/ui_reference_catalog/README.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Visual Acceptance Reviewability Becomes Product Acceptance

- symptom:
  a branch produces a clean USER packet, screenshot/contact-sheet evidence, UIREF citations, helper output, validator output, or CSS-marker comparison and then treats the surface as visually accepted even though USER did not accept/revise/waive a Visual Acceptance Target, no row-by-row visual-family comparison exists, and implementation-match proof is missing or backfilled after code was already written
- layer:
  BP2/BP3, Workstream, Hardening, Live Validation, RAR, UTS, PR Readiness, USER packets, UIREF adoption, Product Experience Contract proof, and branch-local visual repair loops
- root-cause pattern:
  Visual Acceptance, RAR, UIREF, Vision-To-Proof, Product Experience, and packet validation existed as separate checks, but the phase gate did not force them into one enforceable proof chain. Codex could prove that a packet was reviewable, that a screenshot existed, or that a reference was cited while still missing the USER-facing proof that the new surface belonged to the accepted Nexus visual family and served the intended product role.
- fix pattern:
  require the Visual Acceptance proof chain: `Vision Contract -> UIREF / Accepted Reference Set -> Visual Acceptance Target -> Implementation Match Proof -> Pre-Live Visual Purpose Conformance -> Live Validation -> UTS / PR`. Material visible UI must classify implementation authority, compare each element group against the accepted reference set, record Visual Family Relation Proof, record a Functionality Role Contract for new/detached/child/domain surfaces, keep packet reviewability separate from product acceptance, and stop on `Reference-Derived Parity Unproven`, `Template Gap`, `Shared Primitive Gap`, `Role-Ambiguous Surface Unrouted`, issue candidate, waiver, or repair when proof is incomplete.
- validation pattern:
  helpers and fixtures should fail on `Visual Acceptance Target Missing`, `Implementation Started Before Visual Acceptance`, `Implementation Match Proof Missing`, `Accepted Reference Not Compared`, `Reference-Derived Parity Unproven`, `Template Claim Unsupported`, `Shared Primitive Claim Unsupported`, `One-Off Implementation Overclaimed`, `Functionality Role Contract Missing`, `Packet Reviewability Treated As Product Acceptance`, `Screenshot Path Treated As Visual Acceptance`, `Helper Green Treated As Visual Acceptance`, `CSS Similarity Treated As Visual Family Proof`, `Implementation-First Visual Target Backfill`, and `Pre-Live Visual Purpose Conformance Missing` when machine-checkable.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/nexus_vision.md`
  - `Docs/ui_reference_catalog/README.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_branch_readiness_planning_fixture_validation.py`

## Pattern: Future-Proofing Becomes Screenshot-Tuned One-Off Repair

- symptom:
  Codex fixes the current visible defect with a magic pixel, hardcoded row count, default-size-only layout, one-state proof, or branch-local state assumption, then reports green even though the next same-class row, button, dropdown, status, resize state, backend state, or recovery path would require another rewrite.
- layer:
  Project Vision, FAM-002 presentation grammar, UIREF, Reference Standard carrydown, BP2/BP3, Workstream, Hardening, Live Validation, UTS, RAR, PR Readiness, and issue-candidate routing.
- root-cause pattern:
  Source truth required deterministic, intuitive, immersive, predictable, reliable, and consistent output, but did not force Codex to name the derivation rule, extension boundary, future-gated items, magic-value justification, template/shared-primitive/reference/source-truth gaps, or reference-effectiveness warnings before implementation and proof.
- fix pattern:
  require `Future-Proof Implementation Review` inside existing phases. BP2 names layout and state/runtime derivation rules; BP3 verifies proof coverage; Workstream implements from derivation rather than screenshot tuning or records a gap; Hardening inspects brittle assumptions; Live Validation proves relevant states and same-class extension behavior; RAR prepares issue candidates for old/out-of-scope non-future-proof output; PR Readiness reviews repeated same-class repairs for reference effectiveness failure. Future-proofing must never authorize speculative future feature implementation.
- validation pattern:
  future helpers should fail on `Future-Proof Review Missing`, `Future-Proof Proof Plan Missing`, `Magic Value Unjustified`, `Brittle Implementation Unresolved`, `Default-Only Future-Proof Proof`, `One-State Future-Proof Proof`, `Future Scope Implemented By Inference`, `Template Gap Unrouted`, `Shared Primitive Gap Unrouted`, `Reference Gap Unrouted`, `Source-Truth Gap Unrouted`, `Issue Candidate Disposition Missing`, or `Reference Effectiveness Warning Unrouted` when machine-checkable.
- source references:
  - `Docs/nexus_vision.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/ui_reference_catalog/UIREF-007_window_geometry_resize_contract.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Parallel Branches Invent Conflicting Reference Candidates

- symptom:
  FAM or Governance worktrees independently propose same-class standards such as token values, font weights, glow/radius/border rules, geometry breakpoints, control-state behavior, backend truth mapping, proof rules, template expectations, or shared-primitive requirements, and each branch assumes its proposal can become the standard because it passed branch-local proof.
- layer:
  Reference Standard lifecycle, UIREF, RAR, BR1/BR2, BP1/BP2/BP3, Workstream, Hardening, Live Validation, PR Readiness, external operational state, and future non-UI reference families.
- root-cause pattern:
  promoted references correctly live in repo source truth, but candidate proposals lacked a shared external synchronization and collision review model. Branch-local candidate evidence could therefore look authoritative inside one worktree while sibling worktrees proposed incompatible same-class traits.
- fix pattern:
  keep promoted Reference Standards in repo catalogs, store branch-owned candidate proposals as external evidence, generate aggregate/collision reports from branch-owned candidates when admitted, and require `Reference Candidate Sync Review` before a branch proposes or consumes same-class standards. Conflicts use the key `Reference Domain + Element / Behavior Class + Trait / State + Applicability Scope` and must produce a USER-reviewable collision row when the branch depends on that standard.
- validation pattern:
  future helpers should fail on `Reference Candidate Sync Missing`, `Reference Candidate Collision Unreviewed`, `Reference Candidate Treated As Canon`, `Promoted Reference Moved External`, `Same-Class Candidate Ignored`, `External Candidate Overrides Promoted Reference`, `Candidate Conflict Key Missing`, or `Candidate Promotion Packet Missing` when machine-checkable.
- source references:
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/ui_reference_catalog/README.md`
  - `Docs/validation_helper_registry.md`

## Pattern: PR Auto-Close Keywords Bypass Issue Approval

- symptom:
  A GitHub PR body says `Fixes #`, `Closes #`, or `Resolves #` and would auto-close an issue on merge even though USER approved PR creation/merge but did not separately approve issue closeout.
- layer:
  PR Readiness Stage 2, PR body quality, GitHub issue closeout, and Release Readiness issue closeout inventory.
- root-cause pattern:
  PR body governance treated the body as human review text but did not classify GitHub auto-close keywords as a mutation path. That can turn PR merge into unreviewed issue mutation.
- fix pattern:
  treat auto-close keywords as issue mutation risk. Use non-closing references such as `Related issue: #123` or `Issue evidence: #123` unless USER explicitly approved the closeout set and the branch intentionally relies on GitHub auto-close.
- validation pattern:
  run PR body quality checks before PR creation and after live PR creation; future PR-body helpers should flag auto-close keywords when closeout approval is absent.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_pr_body_quality_audit.py`

## Pattern: Template-Shell USER Review Artifact Passed Reviewability

- symptom:
  BP1, BP2, or BP3 USER review artifacts are structurally valid, stale-language-clean, and ZIP-consistent, but the USER-facing content remains template-like: sections tell Codex or USER what a heading should contain, list copied files instead of mapping decision or experience surfaces, use generic accept/revise/waive/reject options, provide generic Codex recommendations, ask broad non-decision-driving USER questions, or ask USER to name/select the real runtime item from generic strongest-implied/narrower/broader paths. The packet is reviewable as a file, but it is not useful as a branch vision, engineering plan, or orchestration-readiness contract.
- layer:
  Branch Planning, USER review hub packets, `dev/orin_user_review_bundle.py`, Branch Readiness planning fixtures, and future branch/worktree review packets across all families.
- root-cause pattern:
  helper/template output and validator fixtures checked marker presence, stale wording, and metadata hygiene without requiring applied branch-specific substance. The system treated "packet generated and valid" as enough even when USER could not inspect actual branch vision, engineering plan, options, tradeoffs, recommendations, or design questions.
- fix pattern:
  BP1 must be a substantive branch vision contract, BP2 must be a substantive engineering plan contract derived from accepted or waived BP1, and BP3 must be a substantive orchestration-readiness contract against accepted or waived BP1/BP2. `Reviewable` remains separate from `USER Accepted`, `USER Waived`, `USER Approved`, or implementation authority. Copied source-truth files are context, not a substitute for the review artifact.
- validation pattern:
  run `python dev\orin_user_review_bundle.py` packet validation when applicable and `python dev\orin_branch_readiness_planning_fixture_validation.py`. Fixtures must prove that template-shell BP1 content, runtime-item-selection shells, copied-file-list-only surface maps, generic USER questions, shallow recommendations, and implementation approval while BP1/BP2 are pending fail reviewability checks.
- source references:
  - `Docs/branch_plans/README.md`
  - `Docs/phase_governance.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_user_review_bundle.py`
  - `dev/orin_branch_readiness_planning_fixture_validation.py`

## Pattern: Runtime Focus Selection Collapsed Into Issue Thread

- symptom:
  USER asks Codex to select or recommend the next runtime focus from a full family/runtime source-truth survey, but the packet centers one GitHub issue, names the branch after that issue's failure mode, treats issue evidence as BR2/BP1 branch identity, or recommends a vague `Execution Foundation`, `Persistence Foundation`, `Infrastructure Foundation`, schema, hydration, or groundwork lane without naming the concrete feature outcome USER will receive or inspect.
- layer:
  Branch Readiness Stage 1 / Stage 2, runtime focus options packets, `dev/orin_user_review_bundle.py`, Branch Readiness planning fixtures, and family-scoped runtime carrier selection.
- root-cause pattern:
  a branch-specific helper/template special case or Codex judgment used issue evidence as the selection source instead of loading issue evidence after the neutral family/runtime survey. The resulting packet can look substantive while still skipping the actual family/package selection question.
- fix pattern:
  runtime focus selection must survey family/runtime source truth first, list credible runtime options, classify each option by runtime/UI/governance/bugfix/proof/future-gated role, name the actual user-visible feature outcome, and only then map issue evidence as possible future BP2/BP3 proof input. Issue evidence may support a selected branch plan, but it must not define BR2/BP1 identity unless USER explicitly selects that issue-shaped focus after seeing the neutral options. Infrastructure and groundwork labels are acceptable only as supporting scope inside a named feature outcome.
- validation pattern:
  run `python dev\orin_branch_readiness_planning_fixture_validation.py`. The invalid runtime-focus issue-anchored fixture must fail on `Runtime focus selection cannot use issue evidence as BR2/BP1 branch identity`, and the invalid runtime-focus foundation-label fixture must fail on `Runtime focus selection must name a concrete feature outcome`.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_user_review_bundle.py`
  - `dev/orin_branch_readiness_planning_fixture_validation.py`

## Pattern: Release Readiness Green Must Require Explicit Release Target

- symptom:
  Release Readiness can appear green while the branch has not yet named the release version, release floor, version rationale, bounded release scope, or release artifacts it is supposed to package, or while the named target is semantically wrong
- layer:
  branch governance and release-facing canon
- root-cause pattern:
  release-debt truth is present, but release-bearing branch records lack machine-checkable markers that prove the release target is explicit and semantically correct before green status
- fix pattern:
  require release-bearing branches to declare `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, and `Release Artifacts:`; validate target semantics from the latest public prerelease and declared floor; allow `Release Branch: No` only for preserved historical records
- validation pattern:
  run the branch governance validator; it must fail release-packaging branch records that omit release target markers, declare a semantically wrong target, or use the non-release waiver outside preserved historical records

## Pattern: Release Readiness File Mutation Must Backflow

- symptom:
  Release Readiness discovers missing release target, scope, artifact, canon, helper, or release-note truth and patches files while the authority record still says `Release Readiness`
- layer:
  release readiness boundary and phase backflow
- root-cause pattern:
  canon treated release target/scope/artifact definition as something Release Readiness could repair in-place instead of analysis-only output or a blocker that returns to the owning earlier phase
- fix pattern:
  treat Release Readiness as analysis-only for repository files; it may produce release package information in the response, but any required source, docs, canon, validator, helper, release-note, or handoff-file mutation must return to `PR Readiness` before merge or defer to the next legitimate runtime-focused backlog branch's `Branch Readiness` after merge
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; it must enforce `Release Readiness File Mutation Attempt` file-freeze language in governance docs and fail if tracked files are dirty while an active authority record says `Release Readiness`
- source references:
  - `Docs/phase_governance.md`
  - `Docs/development_rules.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Escaped PR Work Blocks Next Branch Readiness

- Trigger:
  PR Readiness misses required canon, branch-authority cleanup, post-merge truth, or next-branch deferral work, and the miss is discovered during Release Readiness, after merge, on updated `main`, or after the next branch was created
- Risk:
  Release Readiness becomes a docs-sync phase, repair work leaks between branches, direct `main` writes become tempting, or a governance-only branch becomes a side door around the active phase machine
- Common Cause:
  PR Readiness checks prove behavior or release artifacts but do not prove that merged-main branch records, roadmap state, post-merge state, and selected-next branch timing are already durable before green
- Required Response:
  classify the issue as `PR Readiness Scope Missed`; if it appears during Release Readiness, also classify `Release Readiness Scope Drift`; do not open a standalone closeout or canon-repair branch; carry the miss as a blocker into the next legitimate runtime-focused backlog branch's `Branch Readiness` and repair it before any implementation begins
- Prevention:
  block governance-only branches, block repair-only feature branches, block between-branch canon repair, block all Codex direct `main` writes, require branch-authority cleanup before PR green, and extend the validator whenever a miss exposes a machine-checkable gap. Escaped drift prevention proof is mandatory: every repair for a miss discovered after the phase that should have caught it must include source-truth, governance, validator, helper, or prompt-contract hardening that prevents the same class from passing again, or must record why the gap is not machine-checkable yet and what human review marker replaces it before green.
- source references:
  - `Docs/phase_governance.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Merged-Unreleased Release Debt Must Be Durable Before Release Readiness

- symptom:
  an implementation workstream is merged or squash-merged, but canon still represents it as an active PR Readiness branch and Release Readiness must rediscover the release target, scope, artifacts, or release-debt owner
- layer:
  merge-target canon, roadmap stage-breakpoint/checkpoint posture, workstreams index, and branch governance validation
- root-cause pattern:
  PR Readiness recorded future post-merge prose but did not leave machine-checkable merged-unreleased release-debt fields in the exact post-merge shape that `main` needs after merge
- fix pattern:
  require `Merged-Unreleased Release-Debt Owner:`, `Repo State: No Active Branch`, `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, `Post-Release Truth:`, `Selected Next Workstream:`, and `Next-Branch Creation Gate:` before PR green when a branch will merge unreleased implementation work
  validate release target semantics from the latest public prerelease and declared release floor before PR green
- validation pattern:
  run `python dev/orin_branch_governance_validation.py` plus the PR-readiness gate mode; the validator must fail if a promoted merged-unreleased workstream remains under Active, lacks release target/floor/rationale/scope/artifacts, carries a semantically wrong release target, or if `main` carries tracked file mutation during Codex work
- source references:
  - `Docs/phase_governance.md`
  - `Docs/prebeta_roadmap.md`
  - `Docs/workstreams/index.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Protected Main Must Stay Read-Only For Codex

- symptom:
  escaped canon drift makes direct `main` repair look faster than a branch-carried fix
- layer:
  branch governance, release readiness boundary, and protected-branch safety
- root-cause pattern:
  older governance left room for emergency direct-main repair, which can bypass PR review and make protected branch truth harder to audit
- fix pattern:
  `main` is protected for Codex work; there is no emergency direct-main repair path, and any required file mutation after merge must be recorded as a blocker for the next legitimate runtime-focused backlog branch's `Branch Readiness`
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; it must enforce protected-main language and fail with `Main Write Attempt` if tracked file mutation exists while Codex is on `main`
- source references:
  - `Docs/phase_governance.md`
  - `Docs/Main.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Validation Helper Sprawl Must Collapse Into Registered Helper Families

- symptom:
  a feature branch creates seam-specific live validators or helper scripts even though an existing validator family already covers the same desktop, authoring, launcher, or interaction surface
- layer:
  validation helper governance and Workstream evidence
- root-cause pattern:
  the repo requires reuse-first validation, but without a helper registry and naming tiers, a successful seam helper can become accidental permanent tooling
- fix pattern:
  register durable root `dev/` helpers in `Docs/validation_helper_registry.md`, require standardized names and `Helper Status:` values, and force workstream-scoped helpers to declare owner, reason, consolidation target, and promotion decision point
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; it must fail when helper standardization language is missing or a root `dev/` validation/helper script is unregistered
- source references:
  - `Docs/validation_helper_registry.md`
  - `Docs/phase_governance.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: User Test Summary Pending Must Block Final Green

- symptom:
  automated validators and live helpers pass, but final phase output implies the branch can advance before the filled User Test Summary results are submitted and digested
- layer:
  validation evidence digestion and phase governance
- root-cause pattern:
  canon requires returned user evidence digestion, but without a named blocker the result can be summarized as all-green even though the user-facing handoff is still outstanding
- fix pattern:
  require the named blocker `User Test Summary Results Pending`, record `User Test Summary Results: PENDING` in the active authority record, and report that automated/live evidence is green while final phase advancement remains blocked
- validation pattern:
  run `python dev/orin_branch_governance_validation.py` plus the PR-readiness gate mode; the PR gate must fail while `User Test Summary Results Pending` is active or while the result marker is missing for a relevant user-facing Live Validation or PR Readiness workstream
- source references:
  - `Docs/user_test_summary_guidance.md`
  - `Docs/phase_governance.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: UTS Waivers Must Live In The Exact Canonical Artifact

- symptom:
  Live Validation or PR Readiness records `User Test Summary Results: WAIVED` or `User-Facing Shortcut Validation: WAIVED`, but the waiver lives in recap prose, `## User Test Summary Strategy`, or a validation-contract paragraph rather than the exact canonical `## User Test Summary` section
- layer:
  workstream-owned validation evidence, response contract, and branch governance validation
- root-cause pattern:
  the branch has a valid no-meaningful-manual-test rationale, but validator parsing trusts loose markers outside the canonical UTS artifact, allowing the response/output contract to drift
- fix pattern:
  require an exact `## User Test Summary` section for active `Live Validation` and `PR Readiness` workstreams; require `User Test Summary Waiver Reason:` for UTS waivers and `User-Facing Shortcut Waiver Reason:` for shortcut waivers
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; it must fail if `## User Test Summary Strategy` is present but the exact canonical `## User Test Summary` section lacks the required result and waiver-reason markers
- source references:
  - `Docs/phase_governance.md`
  - `Docs/development_rules.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Desktop Shortcut Gate Must Precede User Test Summary Handoff

- symptom:
  validators, live helpers, and direct-runtime launches pass, but the user-facing desktop shortcut path later exposes a visibility, startup, or discoverability failure
- layer:
  Live Validation proof hierarchy and User Test Summary handoff
- root-cause pattern:
  helper evidence proves branch behavior through controlled launch paths, but the final user entrypoint is not named as a machine-checkable gate before `UTS` handoff
- fix pattern:
  require the `User-Facing Shortcut Live Validation Gate`, record `User-Facing Shortcut Path:` and `User-Facing Shortcut Validation:`, and keep `User-Facing Shortcut Validation Pending` active until the declared shortcut or equivalent user entrypoint passes or is explicitly waived before User Test Summary handoff
- validation pattern:
  run `python dev/orin_branch_governance_validation.py` plus the PR-readiness gate mode; relevant desktop user-facing Live Validation and PR Readiness records must fail if the shortcut result is missing, pending, or failed
- source references:
  - `Docs/user_test_summary_guidance.md`
  - `Docs/phase_governance.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Direct Runtime Or Marker Proof Was Treated As USER-Facing Proof

- symptom:
  Live Validation or UTS handoff claims green from logs, markers, helper PASS, direct runtime launch, generated shortcut, troubleshooting launcher, screenshots without adjudication, or Dev Toolkit evidence while the exact normal USER desktop launcher path and visible photo/video proof are missing
- layer:
  Live Validation proof hierarchy, launcher parity, USER packet evidence, and UTS handoff
- root-cause pattern:
  diagnostic evidence proves that code can run, but Codex treats that evidence as proof that the USER path works and looks correct
- fix pattern:
  require exact normal USER desktop runtime launcher proof for user-facing behavior, require photo/video or ordered frame-sequence proof for visible closeout claims, require USER manual validation or waiver for claims that cannot be proven visually, and allow troubleshooting launcher proof as equivalent only after USER consent and `Launcher Parity Proof: PASS`
- validation pattern:
  future helpers should fail on `Exact USER Desktop Launcher Proof Missing`, `Launcher Parity Proof Missing`, `Photo Or Video Proof Missing`, `Unphotographable Proof Not Elevated To USER`, `Direct Runtime Proof Misclassified`, `Troubleshooting Consent Missing`, `Live Validation Evidence Packet Incomplete`, or `User-Visible Internal Path Leakage`
- source references:
  - `Docs/nexus_vision.md`
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Vision Chain Skipped Or Replaced By Branch-Local Invention

- symptom:
  BR2, BP1, BP2, BP3, Workstream, Hardening, Live Validation, or USER review packets proceed with generic project/family references, branch-local reasoning, copied-file lists, helper green output, or implementation-specific SLC/slice language while the applicable Project Vision, Family Vision, Family Feature Vision, accepted Branch Vision, deferred carryforward, or UI/proof carrydown is missing, shallow, stale, or not digested
- layer:
  Vision Contract, Branch Planning, Live Validation proof, USER review packets, and helper/validator interpretation
- root-cause pattern:
  Codex treats the active branch plan or generated packet as the product vision owner, or treats broad Family Vision as enough for a selected feature-bearing route that needs a Family Feature Vision
- fix pattern:
  require the vision carrydown chain `Project Vision -> Family Vision -> Family Feature Vision -> Branch Vision Contract Snapshot -> BP2/BP3 engineering plan -> Workstream/Hardening/Live Validation proof`; block BP1 on `Family Feature Vision Required For Selected Feature` when needed; require BP2/BP3 to preserve accepted vision and deferred-item disposition; require Live Validation and USER packets to compare observed behavior against the applied vision chain
- validation pattern:
  future helpers should fail on `Vision Carrydown Chain Missing`, `Branch Vision Invented From Local Reasoning`, `Vision Proof Alignment Missing`, `USER Packet Vision Evidence Missing`, `Family Feature Vision Required For Selected Feature`, `Feature Vision Sufficiency Check` failure, or `Family Feature Vision Pointer Migration Missing`
- source references:
  - `Docs/nexus_vision.md`
  - `Docs/family_visions/README.md`
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Circular Proof Or Generic UI Chrome Passed As Vision Green

- symptom:
  A branch reports BP, Workstream, Hardening, Live Validation, or PR readiness green while vision files are procedural instead of product-specific, Nexus-owned windows use default/native OS title bars or utility chrome without an approved exception, or the evidence only proves that a plan, marker, manifest, screenshot, or helper output exists.
- layer:
  Vision Contract, FAM-002 presentation authority, Branch Planning proof plans, Live Validation visual adjudication, USER packets, and helper/validator interpretation
- root-cause pattern:
  Codex treats the artifact that makes a claim as the proof of the claim, treats helper green or screenshot existence as product acceptance, or forgets to classify whether a visible surface is a Nexus-owned product surface that must inherit NDAI presentation standards.
- fix pattern:
  require product-detail vision content, classify visible surfaces as `Nexus-Owned Product Surface`, `Platform-Native Exception`, `Diagnostic / Developer Surface`, or `External Surface`, require FAM-002 component grammar for Nexus-owned surfaces, require platform exceptions to name a reason and proof path, require a Visual Inheritance Matrix with window chrome/frame treatment, and require independent evidence plus Codex adjudication before a product/UI claim can advance. Material claims must declare claim class, minimum proof strength, evidence class, limitation, and disposition so supporting diagnostics, helper green, schema/marker presence, generated manifests, screenshot paths, or plan prose cannot be upgraded into direct proof by wording. If a merged standard lands after a branch started, the affected worktree must evaluate adoption at its next legal gate rather than relying on old green proof.
- validation pattern:
  future helpers should fail on `Vision Contract Product Detail Missing`, `NDAI Window Chrome Missing`, `Default OS Chrome Used Without Exception`, `Nexus-Owned Surface Classification Missing`, `Platform Exception Unclassified`, `FAM-002 Component Grammar Missing`, `Circular Validation Detected`, `Claim Proven By Own Plan`, `Independent Evidence Missing`, `Claim Class Missing`, `Evidence Class Missing`, `Proof Strength Overstated`, `Supporting Evidence Treated As Direct Proof`, `Plan-Only Proof`, `Marker Or Schema Proof Misclassified`, `Screenshot Path Treated As Visual Acceptance`, `Live Validation Comparison Missing`, `USER Validation Escalation Missing`, or `Merged Vision Standard Adoption Missing` when the defect is machine-checkable
- source references:
  - `Docs/nexus_vision.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Live Validation Evidence Without Vision Comparison

- symptom:
  Live Validation, Hardening, or a USER handoff reports screenshots, videos, runtime logs, helper output, markers, manifests, or interaction artifacts as green evidence while the branch does not show which accepted vision requirement each artifact proves or how Codex compared observed behavior to the accepted vision chain.
- layer:
  BP2/BP3 proof planning, Hardening proof-gap review, Live Validation comparative proof, User Test Summary handoff, and helper/validator interpretation
- root-cause pattern:
  Codex treats evidence artifacts as self-explanatory proof and skips the row-by-row comparison between accepted Project/Family/Family Feature/Branch Vision requirements, BP2/BP3 proof plan, observed runtime behavior, and reference surfaces.
- fix pattern:
  require a `Vision-To-Proof Matrix` that maps every material accepted requirement to claim class, minimum proof strength, implementation evidence, observed runtime evidence, comparison evidence, reference surface/baseline, Codex adjudication, USER validation need, and final verdict. Hardening must find missing proof rows before Live Validation; Live Validation must fill observed/comparison evidence and route subjective or unprovable claims to USER validation or waiver.
- validation pattern:
  future helpers should fail on `Vision-To-Proof Matrix Missing`, `Accepted Requirement Missing`, `Observed Runtime Comparison Missing`, `Reference Surface Missing`, `Hardening Proof Gap Not Routed`, `Evidence Input Treated As Comparison`, `Screenshot Or Video Not Adjudicated`, `Runtime Log Treated As Visual Proof`, `Helper Output Treated As Runtime Observation`, `Subjective UX Claim Not USER-Routed`, `Vision-To-Proof Verdict Missing`, or `Live Validation Comparative Proof Missing` when the defect is machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/user_test_summary_guidance.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Implementation Started Before Visual Acceptance Target

- symptom:
  USER repeatedly rejects a visible UI/UX result after runtime implementation because the branch implemented from prose, inferred style, screenshots, helper output, or broad reference language instead of first producing a rendered and USER-reviewable visual target.
- layer:
  Branch Planning, Workstream implementation, Hardening visual proof, Live Validation handoff, USER packets, and helper/validator interpretation.
- root-cause pattern:
  Codex treats BP1/BP2/BP3 visual prose, reference names, partial comparator screenshots, or "looks closer" repair language as enough to implement. The branch has no explicit render authority level, no USER-selected Visual Acceptance Target, no rejected-pattern ledger, no state/contact-sheet coverage, or no later Implementation Match Proof comparing actual runtime screenshots/video against the accepted target.
- fix pattern:
  route material visible UI/UX work through the `Visual Acceptance Target Gate` before runtime implementation. Produce reviewable Design Candidate Renders when direction is unresolved, include focused and desktop/context renders, include state renders or contact sheets, provide stable element IDs, record a selection ledger, record rejected patterns, classify source-truth conflicts, obtain USER acceptance/revision/waiver of the target, and only then implement. After implementation, gather actual screenshots/video and compare them to the accepted target before H1/LV/UTS/PR green.
- validation pattern:
  future helpers should fail on `Visual Acceptance Target Missing`, `Visual Acceptance Target Not Reviewable`, `Concept Render Misclassified As Target`, `Design Candidate Media Missing`, `Visual Target State Coverage Missing`, `Visual Selection Ledger Missing`, `Rejected Pattern Ledger Missing`, `Render Authority Level Missing`, `Implementation Started Before Visual Acceptance`, `Implementation Match Proof Missing`, `Implementation Match Proof Not Compared`, `Source-Truth Visual Conflict Unclassified`, `Vague Visual Acceptance Language`, `Visual Target Packet Hygiene Missing`, or `Visual Target USER Decision Missing` when the defect is machine-checkable.
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/validation_helper_registry.md`
  - `Docs/nexus_vision.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`

## Pattern: Broad Or Multi-Issue Repair Reported Complete Without Coverage

- symptom:
  USER reports a broad or multi-item defect such as all window text is wrong, every button needs correction, the whole window breaks immersion, ten named visual/text issues exist, or multiple related UI defects need repair. Codex fixes one item or a sampled subset, then reports green, complete, no drift, LV passed, PR-ready, or all fixed without proving every item or element group was addressed.
- layer:
  Scope Coverage Manifest, Branch Planning proof, Workstream repair closeout, Hardening, Live Validation visual adjudication, UTS handoff, PR Readiness review-risk analysis, USER packets, helper/validator interpretation, and Codex closeout claims
- root-cause pattern:
  Codex treats broad wording as a general instruction instead of a coverage-expanding claim, fails to decompose the complaint into atomic repair targets, accepts validator green or screenshot existence without checking the generated artifacts, or repairs the easiest visible target while leaving the rest of the class uninspected.
- fix pattern:
  require a `Scope Coverage Manifest` before any full-scope success claim. Broad or multi-issue complaints must be classified as `Single Item`, `Multi Item`, `Broad Class`, `Vague Class`, or `All Surface`; anything broader than `Single Item` must create a target ledger or complete-class scan with owner, surface, file/code path, expected fix, proof method, evidence reviewed, and disposition for each target. Sampling requires explicit justification. Vague final acceptance such as `looks good`, `seems fine`, `validator passed`, or `screenshot exists` is invalid unless mapped to evidence and coverage disposition.
- validation pattern:
  future helpers should fail on `Completeness Claim Without Coverage Manifest`, `Broad Request Decomposition Missing`, `Multi-Issue Repair Ledger Missing`, `Quantity-Sensitive Repair Drift`, `Partial Repair Reported Complete`, `All-Claim Coverage Missing`, `Unverified Defect Target`, `Sampling Used Without Justification`, `Generated Artifact Not Checked`, `Element Group Coverage Missing`, or `Validator Green Accepted Without Coverage Review` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/user_test_summary_guidance.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Pre-Repair Hardening Treated As Final After LV Repair

- symptom:
  Live Validation or USER-gated Live Validation finds defects after a prior Hardening pass, Codex repairs the LV defect, and then PR Readiness or USER handoff relies on the earlier Hardening pass as if it still proves the changed branch.
- layer:
  Hardening, Live Validation, UTS/USER validation, PR Readiness, branch planning proof carrydown, and helper/validator interpretation
- root-cause pattern:
  the branch treats Hardening and Live Validation as one-way gates instead of a repair loop. LV proves the real runtime/USER path, so LV-discovered repairs can invalidate the prior Hardening inspection. Conversely, rerunning full Hardening before repairing a known-failing LV path can waste effort and create false confidence.
- fix pattern:
  repair the known LV blocker first, rerun or reconfirm the affected LV proof path to green, rerun Hardening over the changed files/surfaces/proof rows, then rerun or reconfirm LV after Hardening. USER validation and PR Readiness may rely only on the final post-repair Hardening plus LV-green state, not the stale pre-repair pass.
- validation pattern:
  future helpers should fail on `Known-Failing LV Repair First`, `Post-LV-Repair Hardening Rerun Missing`, `Post-Hardening LV Reconfirmation Missing`, `Pre-Repair Hardening Treated As Final`, `Final USER Validation Missing`, or `PR Readiness Uses Superseded Hardening` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/user_test_summary_guidance.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Standalone Product Window Has No Geometry Recovery Path

- symptom:
  A Nexus-owned standalone, top-level, restorable, independently opened, movable, resizable, or geometry-persisted product window can become offscreen, too small, too large, corrupted, or trapped on a missing monitor, and the branch has no user-accessible reset-window-position/size route or Not Applicable reason.
- layer:
  FAM-002 presentation standards, FAM-003 resident/settings/quick-action dependency routing, consuming-FAM window behavior, Branch Planning proof, Hardening, Live Validation, and USER handoff
- root-cause pattern:
  a branch proves that a window opens or looks acceptable in the happy path but does not treat geometry persistence and recovery as part of USER trust. The reset route is assumed to be a future settings detail, or packaging/setup is treated as owner by inertia, leaving no deterministic recovery path.
- fix pattern:
  require window classification for created/touched/affected product windows, declare safe default geometry, record whether geometry is persisted, route shared user-accessible reset behavior through FAM-003 resident access / Global Settings / quick actions when admitted, keep FAM-002 as presentation grammar owner, keep FAM-008 to setup/education only unless explicitly admitted, and require proof or USER waiver before final green.
- validation pattern:
  future helpers should fail on `Window Position / Size Reset Route Missing`, `FAM-003 Window Recovery Dependency Required`, `Child Window Geometry Reset Not Applicable Unproven`, `Offscreen Window Recovery Path Missing`, `Window Geometry Classification Missing`, `FAM-008 Runtime Reset Ownership Drift`, or `Repo File-State Tracking` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/family_visions/FAM-003_interaction_and_actions.md`
  - `Docs/family_feature_visions/F3-FF01.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Top-Level Product Window Uses Content-Style Header Close Control

- symptom:
  A mature Nexus-owned top-level, standalone, restorable, independently opened, movable, resizable, or geometry-persisted product window uses a large labeled header `CLOSE` pill as its window-level close control, often while also exposing a footer/content `CLOSE`, `Cancel`, or `Exit` action. The window is technically clear but can read like a content action, compete with footer actions, or blur the difference between window management and workflow completion.
- layer:
  FAM-002 presentation standards, Branch Planning UI carrydown, Hardening visual inspection, Live Validation visual proof, and USER review packet clarity
- root-cause pattern:
  a branch treats any obvious close affordance as sufficient and validates screenshot presence or clickability, but does not classify whether the control is a top-level window control, content action, modal action, or exception. The branch avoids default Windows chrome but still lacks a mature Nexus-native window-control grammar.
- fix pattern:
  require top-level window-control classification, prefer a compact custom NDAI control cluster or recorded equivalent for standalone product windows, keep large labeled close/cancel/exit buttons for content/footer/modal/child/proof/platform exception contexts, classify minimize/maximize/restore applicability, and prove accessibility, hitboxes, hover/focus/pressed states, and header/footer close separation.
- validation pattern:
  future helpers should fail on `Top-Level Window Control Grammar Missing`, `Large Header CLOSE Pill Requires Exception`, `Default Windows Chrome Regression`, `Window-Control / Content-Action Boundary Missing`, `Minimize / Maximize / Restore Applicability Missing`, `Window Control Accessibility Proof Missing`, `Header/Footer Close Conflict Unresolved`, or `Visual Window Control Proof Missing` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Product Window Geometry Green Claimed From One Size Or Marker Proof

- symptom:
  A Nexus-owned product window, dashboard, detached child window, settings/tool window, or studio/log surface is reported visually green because it opens, has a marker, or looks acceptable at one default size, while minimum size, wide size, fullscreen/maximize, DPI/display scale, multi-monitor, portrait/narrow monitor, scroll/wrap/truncate/collapse, resize cursor, or sparse wide-state behavior remains unproven or visibly inconsistent with accepted references.
- layer:
  FAM-002 presentation standards, UIREF-007 geometry/resize contract, RAR, Branch Planning proof matrices, Hardening, Live Validation, USER packets, and issue-candidate routing
- root-cause pattern:
  a branch treats geometry as a secondary visual detail after proving the happy-path surface, or it assumes that a screenshot, helper marker, default-size rendering, hidden bottom-right resize grip, or global zoom behavior is enough. Existing owned surfaces outside the immediate repair sample can remain nonconforming because the packet does not force a full window/surface inventory or issue-candidate disposition.
- fix pattern:
  require a `Window Geometry / Resize Matrix` for applicable branches; classify each surface; define minimum/default/maximum/fullscreen policy; prove resize mechanics, breakpoints/reflow, DPI, multi-monitor, content overflow, active content/footer attachment, and accepted-reference comparison; route out-of-scope owned drift to USER-reviewable issue candidates before normal progression; and keep current window coordinates/live state out of repo docs.
- validation pattern:
  future helpers should fail on `Window Geometry Contract Missing`, `Window Classification Missing`, `Window Min Default Max Policy Missing`, `Window Fullscreen / Maximize Policy Missing`, `Window Resize Mechanics Proof Missing`, `Resize Cursor / Grip Policy Missing`, `DPI Display Scale Proof Missing`, `Multi-Monitor Geometry Proof Missing`, `Responsive Layout Proof Missing`, `Sparse Wide-State Shell`, `Global Zoom Used As Layout Substitute`, `Detached Child Acceptance Missing`, `Embedded Child Inheritance Unproven`, `Geometry Issue Candidate Missing`, `Marker-Only Geometry Conformance`, or `Repo File-State Tracking` when machine-checkable
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/family_visions/FAM-002_desktop_interface.md`
  - `Docs/family_feature_visions/F2-FF01.md`
  - `Docs/ui_reference_catalog/UIREF-007_window_geometry_resize_contract.md`
  - `Docs/validation_helper_registry.md`

## Pattern: Released-Canon Fallback Must Not Use The Highest Planned Prerelease

- symptom:
  support bundles or issue drafts can report an unreleased baseline when `.git` metadata is unavailable
- layer:
  support reporting and release-context derivation
- root-cause pattern:
  fallback logic trusts sequencing or planning truth as if it were released-canon truth
- fix pattern:
  derive fallback release context from the latest released prerelease truth, not from the highest planned prerelease target
- validation pattern:
  prove both `git`-present and `git`-unavailable report-artifact paths resolve to the same released public prerelease truth
- source references:
  - `Docs/workstreams/FB-035_release_context_fallback_hardening.md`
  - `Docs/prebeta_roadmap.md`

## Pattern: Post-Release Canon Must Close Released Release Debt

- symptom:
  a public prerelease tag and GitHub prerelease exist, but canon still reports the released workstream as merged-unreleased release debt or leaves latest public prerelease at the prior tag
- layer:
  post-release confirmation and release-state canon
- root-cause pattern:
  PR Readiness defines pre-release target/scope/artifacts but does not include a machine-checkable release-state closure plan that forces latest public prerelease, released/closed workstream state, and release-debt clearing after the tag exists
- fix pattern:
  during PR Readiness for release-bearing work, require a release-state closure plan that covers latest public prerelease, released/closed workstream state, release-debt clearing, workstream-index movement to Closed, and successor branch deferral; after a release tag exists, the governance validator must fail stale release-debt canon
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; it must fail if the latest local pre-Beta tag is newer than roadmap latest public prerelease, or if the released workstream remains promoted/merged-unreleased instead of closed/released
- source references:
  - `Docs/prebeta_roadmap.md`
  - `Docs/feature_backlog.md`
  - `Docs/workstreams/index.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Architecture-Only Milestones Must Not Force Minor Prerelease Bumps

- symptom:
  a planning, architecture, admission-contract, validation-only, or non-user-facing milestone advances the public pre-Beta version by a minor bump even though no executable, runtime, operator-facing, user-facing, or materially expanded product capability lane was delivered
- layer:
  release-floor governance, PR Readiness release-target semantics, and validator enforcement
- root-cause pattern:
  source-of-truth treats "opens a lane" or "defines architecture" as equivalent to delivering a new capability lane, so `Release Floor: minor prerelease` can pass marker checks without proving user-visible or executable product expansion
- fix pattern:
  make `patch prerelease` the default for architecture-only planning, admission contracts, validation-only work, documentation/canon repair, governance repair, and non-user-facing milestones; require `minor prerelease` rationale to name a new executable, runtime, operator-facing, user-facing, or materially expanded product capability lane
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; the validator must fail a merged-unreleased owner that declares `Release Floor: minor prerelease` while its rationale/scope is architecture-only or non-user-facing without an executable or user-facing capability marker
- source references:
  - `Docs/phase_governance.md`
  - `Docs/prebeta_roadmap.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Pre-Beta Release Title Format Is Concise

- symptom:
  post-release confirmation compares the GitHub release title against a long PR-generated milestone title and treats the published concise title as drift
- layer:
  release artifacts and post-release confirmation
- root-cause pattern:
  source-of-truth does not record the public GitHub prerelease title format separately from release-note summary content
- fix pattern:
  use `Pre-Beta v<major>.<minor>.<patch>` as the public GitHub release title format for Nexus pre-Beta releases; put milestone name, user-facing scope, capabilities, behavior, and evidence in inclusion-only release notes
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; release artifacts and released-state canon should use the concise title format while release notes carry the scoped milestone summary
- source references:
  - `Docs/closeout_guidance.md`
  - `Docs/prebeta_roadmap.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Release Notes Must Not Repeat The Release Title

- symptom:
  live GitHub release notes begin with a repeated H1 copy of the release title, making the GitHub release page show the same title twice
- layer:
  release notes and Release Execution packaging
- root-cause pattern:
  the release body template treated `# <release title>` as part of the Markdown notes instead of keeping the title in GitHub release metadata
- fix pattern:
  keep the public release title in GitHub release metadata and the separate `Release Title` operator block; start the release body with `## Release Summary` or `## Release Overview`, then use `## Release Highlights` or release-specific rich sections, followed by GitHub-generated `## What's Changed` and `**Full Changelog**:`
- validation pattern:
  inspect live GitHub releases for no leading `# <release title>`, require generated `## What's Changed` and `**Full Changelog**:`, and run `python dev/orin_branch_governance_validation.py`
- source references:
  - `Docs/phase_governance.md`
  - `Docs/development_rules.md`
  - `Docs/codex_modes.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Repeated-Identical Recoverable launch_failed Must Stay Bounded

- symptom:
  a repeated recoverable `launch_failed` class starts pulling diagnostics policy toward blanket popup or fatal-path behavior
- layer:
  recoverable diagnostics surface and failure-class handling
- root-cause pattern:
  a bounded high-signal recoverable class is treated as permission to widen every recoverable failure into the same diagnostics surface
- fix pattern:
  keep the selected incident class explicit, preserve the manual reporting boundary, and keep fatal launcher and runtime diagnostics behavior separate
- validation pattern:
  prove only the selected repeated-identical `launch_failed` class gets the intended recoverable handling while fatal-path behavior remains unchanged
- source references:
  - `Docs/workstreams/FB-034_recoverable_diagnostics.md`
  - `Docs/architecture.md`

## Pattern: Green Multi-Seam Workflows Must Continue Until Blocked

- symptom:
  Codex completes and validates one seam inside a valid bounded multi-seam Workstream sequence, then stops because the prompt named only the entry seam or the output format asks for a next safe move
- layer:
  seam workflow governance, prompt interpretation, and active workstream phase truth
- root-cause pattern:
  source-of-truth required a continue-or-stop decision, but did not encode an explicit all-seams default after a green seam; validator enforcement only checked for broad multi-seam markers and missed prompt-as-terminal ambiguity
- fix pattern:
  define `Next-Seam Continuation Required` as the default after a green seam, state that Codex must perform all admitted seams in the bounded multi-seam workflow unless an explicit `Backlog-Split User Approval` or a named bounded stop condition is recorded, treat prompt-named seams inside approved sequences as entry seams rather than terminal boundaries, and require a recorded bounded stop condition, phase boundary, stop-loss trigger, or explicit split approval before stopping
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; governing docs and prompt scaffolds must include `Next-Seam Continuation Required`, entry-seam language, the exact all-seams default, bounded stop conditions, and explicit split-handling markers without recreating category-stop authority
- source references:
  - `Docs/phase_governance.md`
  - `Docs/development_rules.md`
  - `Docs/codex_modes.md`
  - `Docs/orin_task_template.md`
  - `Docs/codex_user_guide.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Category-Based Seam Stops Healthy Chains

- symptom:
  Codex completes and validates an admitted architecture or planning seam, then stops solely because the seam is labeled UI-model, launcher, protocol, settings, high-risk, or cross-subsystem
- layer:
  seam workflow governance and validator enforcement
- root-cause pattern:
  source-of-truth treated risk categories as automatic stop authority instead of requiring a concrete bounded stop condition
- fix pattern:
  keep bounded multi-seam continuation as the default after green seams; use category labels to require smaller seams and stronger gates, not to stop an otherwise valid chain
- validation pattern:
  run `python dev/orin_branch_governance_validation.py`; the validator must reject governance docs that recreate category-based fallback stop authority
- source references:
  - `Docs/phase_governance.md`
  - `Docs/development_rules.md`
  - `Docs/codex_modes.md`
  - `Docs/orin_task_template.md`
  - `Docs/codex_user_guide.md`
  - `dev/orin_branch_governance_validation.py`

## Pattern: Re-Entering Branch Ignores Merged Vision Standards

- symptom:
  a branch or worktree rebases onto new governance, then continues from an old BP1/BP2/BP3, Hardening, Live Validation, UTS, or PR Readiness packet without checking whether the merged Project Vision, Family Vision, Family Feature Vision, UI immersion, claim/evidence, Vision-To-Proof, proof-strength, or USER-validation standards now affect the branch
- layer:
  rebaseline/reconciliation, Branch Readiness, Branch Planning, Hardening, Live Validation, UTS, and PR Readiness
- root-cause pattern:
  rebaseline proves Git freshness but does not separately force an adoption review for merged standards that were created after the active branch packet or proof plan; Codex treats old green packets as still green even when their proof model, UI inheritance, or USER validation path is now incomplete
- fix pattern:
  require `Merged Vision Standard Adoption:` at the next legal gate after rebaseline or re-entry, classify affected surfaces/proof claims, repair or waive the branch-local packet/proof plan before the next USER handoff or green gate, and keep current adoption state out of repo docs
- validation pattern:
  future validators should fail re-entering branch packets that ignore newly merged standards when the branch touches affected UI, runtime proof, Live Validation proof, failure/recovery behavior, or subjective USER validation, while preserving historical receipts and clean-clone-safe repo validation
- source references:
  - `Docs/phase_governance.md`
  - `Docs/branch_plans/README.md`
  - `Docs/validation_helper_registry.md`
## Incident Pattern: False-Green Transition And Current-Gate Misclassification

When a target-scoped external-state writer validates a record, prepares a
replacement, or reports a structurally valid packet without proving the final
target bytes, recovery snapshot, alias agreement, changed-field audit, and
current-gate artifact class, the result is a false green. The same pattern
appears when a BP2 Branch Plan file is promoted as the primary PR Readiness
Stage 1 decision surface. Prevention requires immediate pre-replacement hash
and byte checks, a same-root snapshot containing the exact pre-write target,
fail-closed path and alias handling, audit details for every added or replaced
field, adversarial mutation fixtures, and a dedicated
`PR_READINESS_STAGE1_REVIEW.md` primary packet artifact. ZIP parity or helper
green alone does not clear this incident class.

## Incident Pattern: Legacy Completed Audit Misclassified As Active Transaction

When a target-set journal validator assumes every receipt that names the
target-set atomic transition must carry the current `Transaction State` field,
immutable completed receipts from the pre-state schema are falsely classified
as incomplete active transactions. Prevention requires parsed JSON selection by
the exact `Transition` field plus an immutable compatibility registry, never
filename, age, raw-text substring, old shape, or completion-token heuristics.
Current journals remain fail-closed. A state-less legacy receipt is compatible
only when its normalized audit path and raw SHA256 match one of the three exact
registry identities in
`dev/orin_external_state_legacy_receipt_compatibility.json`, its accepted
profile matches that identity, and its exact legacy fields, safe unique targets,
released lock, completed workload, non-retention posture, snapshot manifest,
copied-file hashes, and complete target-row completion evidence all agree. Every
live target row must carry the required completion fields, every
completion-bearing field must match the identity-bound profile, and all live
rows must resolve to that profile. Explicit `historical-receipt` rows carry no
live completion evidence. Loose searches for `pass`, `complete`, `completed`, or
the transition phrase are invalid because copied/renamed receipts, byte-tampered
receipts, one positive-looking token, negated or future prose, and one completed
row cannot prove immutable identity or the complete target set. A malformed JSON
record that explicitly declares the exact transition remains blocked, while the
same phrase in notes or another field does not select an unrelated audit.
Every candidate journal, compatibility-registry object, nested target row, and
supporting lock/snapshot object must be decoded with ordered-pair duplicate
detection. Exact duplicate names and case-ambiguous security-critical aliases
must fail closed rather than inherit the JSON parser's last-value-wins result.
Journal parsing and immutable-receipt SHA256 binding must use the same byte read.
Ambiguous shapes or assignments, active locks, partial or contradictory
completion evidence, recovery payloads, and inconsistent hashes must remain
blocked. Temporary-root fixtures, live read-only receipt checks, and controlled
mutations must prove that compatibility cannot expand beyond the exact three
identities or degrade into accepting every missing-state, old, copied, renamed,
tampered, duplicate-key, case-ambiguous, partial-target, contradictory, or
token-bearing record.

The modern-journal path is a separate evidence family and must not inherit a
weaker contract from legacy compatibility. A modern committed journal must
prove a standards-compliant JSON shape, a top-level transition, canonical
string targets, distinct before/after hashes, a confined and hash-valid
snapshot, a released exact-write-set lock, no recovery payload at any depth,
confined case-insensitive audit discovery, and fail-closed handling for BOMs,
reparse points, impossible path characters, and evidence read races.
Any case-insensitive match to the exact target-set transition is a journal
candidate and must fail unless both the `Transition` key and value are canonical.
The released lock's normalized write set must equal the journal audit, snapshot,
and target set exactly; subset proof does not cover an unjournaled extra target.
Evidence-relative paths must use their exact recorded spelling; leading or trailing
whitespace is invalid rather than normalization input. Snapshot content hashing
must remain bound to the same confined regular-file handle across the pathname
check, open, read, and post-read identity check so a replacement cannot redirect
hashing outside the evidence root. Immutable-receipt registry lookup and modern
journal, snapshot, and lock path comparison must use host filesystem case
semantics: case-insensitive on Windows and case-sensitive on POSIX. Journal bytes
must also be read through the same no-follow confined handle whose component and
file identity is checked before and after the read; a pathname check followed by
a separate pathname read leaves an alias-replacement race.
Surrogate code points are invalid evidence-path input and must be rejected before
any filesystem operation. Strict JSON decoding must convert excessive nesting or
decoder resource exhaustion into a normal fail-closed validation result rather
than allowing a traceback to terminate the external-state CLI. Fixture mutation
stubs must use the same host-path normalization as the validator so POSIX case
semantics are exercised instead of accidentally lowercased away.
Every accepted snapshot manifest must bind its `Root` to the resolved current
external-state root; copied bytes and hashes from another root are not valid
recovery provenance. The manifest root must be absolute before resolution, and
the leading `snapshots/` namespace must use host filesystem case semantics.
Transition selection must treat whitespace-trimmed key or
value matches as candidates and then reject them unless the original key and
value are exactly canonical.
Legacy and modern released-lock evidence must prove the exact journal, snapshot,
and target write set with no unjournaled additions. Both legacy and modern
`Released At` evidence must be a canonical UTC timestamp, not merely nonblank text.
PR Readiness must map this family separately from repo/live-state ownership and
generic table-row parsing, then run the target-currentness adversarial fixture
suite before the Connector becomes the first structural or evidence fuzzer.

A durable or historical carrier-admission receipt is also a separate parser
family. PR Readiness must prove exact branch/subsection identity, complete
collision and confinement markers for active durable admission, exact authority
pointers, and the complete absence of active assignment markers after
historical fold-down. Generic worktree-confinement wording is not sufficient
family coverage for compact-receipt parsing. Lookup must use the documented
`Carrier Admission Receipt History` section, retain a receipt's nested
`Assigned Worktree Confinement` section, and stop before later registry law.
`None;` is not sufficient historical proof when the remainder of the same
claim assigns ownership or authorizes mutation, including a contradictory
`but` clause in the same sentence. Active durable admission also requires a
nonblank upstream equal to `origin/<branch>`; an untracked local carrier cannot
use the fallback. Missing-waiver proof must match a closed complete absence
state; a fragment beginning with `No` does not pass when its remainder says
waiver evidence was not recorded. A folded `Historical/no-active` receipt is
identity and admission history only and can never authorize a resumed workload
or PR repair. Current work requires a new active authority. When that authority
is external, the external record must carry the complete current branch,
worktree, owner, collision, write-set, routing, and waiver contract and may point
to the exact historical repo receipt only as durable identity evidence; the
pointer does not reactivate the receipt.
Active durable confinement markers must also prove affirmative, non-contradictory
outcomes. Marker presence alone cannot admit a receipt that reports a collision,
allows off-worktree work, removes the USER-owned new-worktree gate, or negates
the no-cross-worktree claim with wording such as `Not confirmed` or
`Not prohibited`.
Safe-state parsing must reject a positive prefix followed by a contradictory
clause: collision still exists, routing is not blocked or goes directly to a
sibling, USER approval concerns another decision or is explicitly absent for the
new worktree, or cross-worktree mutation can proceed. The accepted claim must
name the safe outcome itself.
A durable bootstrap receipt must point to a specific affirmative USER-approved
bounded carrier admission; pending or absent decision prose is not approval.
The receipt is pre-PR evidence only and must fail once PR review or PR Readiness
review state begins unless it has already folded into historical/no-active form.
A no-open-PR response is insufficient when the all-state fallback fails; absence
proof must come from a successful all-state lookup that finds no PR for the branch.

Comment-family matching must treat generic UI prose such as `before text` as
unknown unless journal, target-set, audit, external-state, or recovery context
proves that the phrase names transaction evidence. A generic phrase cannot consume
the external-state same-family review budget by itself.
Likewise, `historical receipt` requires carrier, admission, confinement, worktree,
assignment, fold-down, or durable-authority context before it maps to the durable
carrier family. When an exact-scope comment also strongly matches another covered
family, preserve both matches even if the prose omits that family's acronym.
Generic `json decoder` wording likewise requires journal, audit, transaction,
target-set, or external-state context before it maps to transaction evidence.

- source references:
  - `dev/orin_external_state_validation.py`
  - `dev/orin_external_state_legacy_receipt_compatibility.json`
  - `dev/orin_external_state_target_currentness_fixture_validation.py`
  - `Docs/validation_helper_registry.md`
