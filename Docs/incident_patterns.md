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
- validation pattern:
  run the normal branch governance validator plus the PR-readiness gate mode; the gate must fail while the worktree is dirty, while required post-merge truth is not encoded, while the next runtime workstream is undefined, unscoped, not runtime, or already branched, while `Next Runtime Candidate Selection Pending` is active, while the PR does not exist, or while PR state cannot be inspected
- source references:
  - `Docs/phase_governance.md`
  - `dev/orin_branch_governance_validation.py`

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
  treat `C:\Nexus USER\<worktree-label>` as a clean-regenerated packet root, not an incremental folder. Before USER review or PR Readiness, prove root `START_HERE.md`, `USER Review` / `Review Aids` / `Source Truth Context` layout, exactly one current-gate primary file under `USER Review`, mandatory timestamped ZIP `C:\Nexus USER\<worktree-label>-YYYYMMDD-HHMMSS.zip`, no legacy stable `C:\Nexus USER\<worktree-label>.zip`, no previous same-label timestamped ZIPs, ZIP-beside-folder placement, duplicate ZIP entry rejection, folder/ZIP file-list plus content-hash parity, unresolved-placeholder absence, stale-stage scan, and final packet proof reporting. If a packet was assembled outside the normal build path, run `dev/orin_user_review_bundle.py --validate-local-user-packet <folder> --review-export-zip <timestamped-zip>` before treating it as current.
- validation pattern:
  run `python dev\orin_user_review_bundle.py --validate-local-user-packet <folder> --review-export-zip <timestamped-zip> --worktree-label <label>` for existing local packets, `python dev\orin_branch_readiness_planning_fixture_validation.py` for regression fixtures, and the normal governance-efficiency validation. Any stale same-label ZIP, stable-name ZIP, copied ZIP outside the packet folder parent, duplicate ZIP entry, layout drift, primary-file count drift, folder/ZIP file-list mismatch, or folder/ZIP content-hash mismatch blocks on `USER Review Packet Stale`.
- source references:
  - `Docs/governance_efficiency_operating_model.md`
  - `Docs/development_rules.md`
  - `Docs/validation_helper_registry.md`
  - `dev/orin_user_review_bundle.py`

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
  BP1, BP2, or BP3 USER review artifacts are structurally valid, stale-language-clean, and ZIP-consistent, but the USER-facing content remains template-like: sections tell Codex or USER what a heading should contain, list copied files instead of mapping decision or experience surfaces, use generic accept/revise/waive/reject options, provide generic Codex recommendations, or ask broad non-decision-driving USER questions. The packet is reviewable as a file, but it is not useful as a branch vision, engineering plan, or orchestration-readiness contract.
- layer:
  Branch Planning, USER review hub packets, `dev/orin_user_review_bundle.py`, Branch Readiness planning fixtures, and future branch/worktree review packets across all families.
- root-cause pattern:
  helper/template output and validator fixtures checked marker presence, stale wording, and metadata hygiene without requiring applied branch-specific substance. The system treated "packet generated and valid" as enough even when USER could not inspect actual branch vision, engineering plan, options, tradeoffs, recommendations, or design questions.
- fix pattern:
  BP1 must be a substantive branch vision contract, BP2 must be a substantive engineering plan contract derived from accepted or waived BP1, and BP3 must be a substantive orchestration-readiness contract against accepted or waived BP1/BP2. `Reviewable` remains separate from `USER Accepted`, `USER Waived`, `USER Approved`, or implementation authority. Copied source-truth files are context, not a substitute for the review artifact.
- validation pattern:
  run `python dev\orin_user_review_bundle.py` packet validation when applicable and `python dev\orin_branch_readiness_planning_fixture_validation.py`. Fixtures must prove that template-shell BP1 content, copied-file-list-only surface maps, generic USER questions, shallow recommendations, and implementation approval while BP1/BP2 are pending fail reviewability checks.
- source references:
  - `Docs/branch_plans/README.md`
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
