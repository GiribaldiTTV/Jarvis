# Branch Authority Record: feature/release-readiness-source-truth-intake

## Branch Identity

- Branch: `feature/release-readiness-source-truth-intake`
- Workstream: `Standing Governance Intake Branch`
- Branch Class: `standing governance intake`
- Worktree: `C:\Nexus Worktrees\Governance`
- Cycle ID Format: `RRI-YYYYMMDD-NNN`

## Purpose / Why It Exists

This branch is the single standing governance lane for Release Readiness source-truth drift intake. It exists so Release Readiness can remain file-frozen while preventable post-merge source-truth blockers are repaired through a short PR cycle on a dedicated worktree instead of direct-main mutation, an ad hoc cleanup branch, or an implementation worktree that should stay isolated.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- Branch Authority Marker: `Active standing governance intake lane`
- `Active Branch`: `feature/release-readiness-source-truth-intake`
- Branch Authority State: `Active standing authority / single-cycle Release Readiness digest, automation/worktree governance intake, or USER-approved phase-gate governance intake only`
- Intake State: `Active - RRI-20260515-001 repairs Branch Readiness product-system planning gate drift reported from the FAM-006 Monitor Groups / Sensor Library planning miss`
- Standing Authority Exception: `Allowed - merged-main No Active Branch means no active runtime, implementation, release packaging, or repair carrier; the single standing governance intake authority may remain active for Release Readiness digest intake, USER-approved automation/worktree governance intake, or USER-approved phase-gate governance intake only`
- Bootstrap Setup: `RRI-20260514-001 records the one-time USER-approved exception that creates C:\Nexus Worktrees\Governance and the standing branch from origin/main; this record now remains the durable active standing authority while each future intake still requires sync to origin/main before work`
- Bootstrap Exception Limit: `Closed after setup merge; after setup PR merge or any origin/main movement, ahead-of-main work requires a USER-approved active RRI cycle sourced from a Release Readiness digest, USER-approved automation/worktree governance intake, USER-approved phase-gate governance intake, or a bot-review repair on an open standing-governance PR that already has USER approval`
- Active RRI Cycle: `RRI-20260515-001`
- Latest Closed RRI Cycle: `RRI-20260514-007`
- Return Digest Status: `Pending - RRI-20260515-001 must merge, sync the standing branch, and return the Branch Readiness planning-gate repair digest before the originating FAM-006 lane treats the governance blocker as resolved`
- Active Cycle Identity: `RRI-20260515-001 / originating lane C:\Nexus Worktrees\FAM-006 / Branch Readiness product-system planning gate drift / no FAM-006 mutation by this governance lane`

## PR Readiness Stage 1 Analysis Packet

- PR Readiness Stage: `PR Readiness Stage 1 - Analysis Gate`
- Pre-PR Live State: `No live PR yet for active RRI-20260515-001`
- Historical Merge Proof: `PR #153 is closed/merged historical proof for RRI-20260514-007 and PR #151 is closed/merged historical proof for RRI-20260514-006; neither is a live PR for a new cycle`
- Next Workstream User Waiver: `Not applicable - standing governance intake PRs do not select runtime successor workstreams, create runtime branches, or admit packages`
- Stage 1 Outcome: `Active - RRI-20260515-001 repairs governance/validator drift before PR readiness`

## Branch Class

- `standing governance intake`

## Blockers

- `Release Readiness Digest Missing`: `Active until a Release Readiness blocker packet is handed to this lane`
- `Standing Governance Intake Not Rebased`: `Active whenever the branch is not clean and equal to origin/main before a new intake`
- `Multiple Intake Cycles Blocked`: `Active for any second RRI cycle until the first cycle merges, returns its digest, and the branch syncs to origin/main`
- `Governance PR Merge User Approval Missing`: `Active until USER approves each cycle merge`
- `Runtime Scope Blocked`: `Active always; this branch cannot carry runtime/provider/model/memory/voice/Core/shortcut/installer work`
- `Release Execution Blocked`: `Active always; this branch cannot tag, publish GitHub Releases, generate release artifacts, or execute release work`

## Entry Basis

- USER approved Branch Readiness Stage 2 execution for a permanent governance worktree and branch.
- Worktree created at `C:\Nexus Worktrees\Governance`.
- Branch created from `origin/main` at `926c7c90880419830be99611d741c6bac51252de`.
- Standing branch name is fixed as `feature/release-readiness-source-truth-intake`.

## Standing Governance Intake Contract

- Standing Branch: `feature/release-readiness-source-truth-intake`
- Worktree: `C:\Nexus Worktrees\Governance`
- Intake Source: Release Readiness digest only for release-blocker intake; USER-approved automation/worktree governance intake may also use this standing lane when the repair is non-runtime, multi-worktree safety related, and held to the same one-cycle/PR-gated contract; USER-approved phase-gate governance intake may also use this standing lane when a live branch exposes a repeatable Branch Readiness, PR Readiness, Release Readiness, or Workstream gate miss and the repair is limited to governance/source-truth/validator/helper prevention; bootstrap setup is the one-time USER-approved exception recorded by RRI-20260514-001, and bot-review repair on an open standing-governance PR may use a same-lane active RRI cycle only to repair that PR before merge.
- Cycle ID Format: `RRI-YYYYMMDD-NNN`
- Active RRI Cycle: `RRI-20260515-001`
- Latest Closed RRI Cycle: `RRI-20260514-007`
- Return Digest Status: `Pending - RRI-20260515-001 must merge, sync the standing branch, and return the Branch Readiness planning-gate repair digest before the originating FAM-006 lane treats the governance blocker as resolved`
- Active Cycle Identity: `RRI-20260515-001 / originating lane C:\Nexus Worktrees\FAM-006 / Branch Readiness product-system planning gate drift / no FAM-006 mutation by this governance lane`
- One Active Cycle: Required - a second digest queues until the active cycle merges, returns its digest, and the branch syncs to origin/main.
- Sync Rule: Before each new intake the branch must be clean and match origin/main; otherwise `Standing Governance Intake Not Rebased` blocks work.
- Bootstrap Exception Limit: Required - the RRI-20260514-001 setup exception cannot authorize future ahead-of-main work after origin/main moves beyond the recorded branch creation base.
- Return Digest: Required after governance PR merge and branch sync.
- Originating Lane Pause: Required - the originating thread/worktree enters `Waiting For Governance Intake` or `Waiting For Updated Main` and must not mutate until return digest and rebaseline.

## Assigned Worktree Confinement

- Assigned Worktree Confinement: `Required`
- Expected Worktree Root: `C:\Nexus Worktrees\Governance`
- Actual Worktree Root: `Must resolve to C:\Nexus Worktrees\Governance before mutation, branch/worktree action, runtime launch, PR/release action, shortcut/provider/model action, or GitHub Desktop handoff`
- No Cross-Worktree Mutation: `Required - this thread must not mutate C:\Nexus Desktop AI, C:\Nexus Worktrees\FAM-006, C:\Nexus Worktrees\FAM-007, parked clones, sibling worktrees, or neutral/main folders by convenience`
- GitHub Desktop-bound worktree: `C:\Nexus Worktrees\Governance`
- Worktree Escape User Waiver: `None; Worktree Escape User Waiver: Granted is valid only when USER explicitly names expected root, actual root, target root, allowed commands/files, expiration or stop condition, required validation, and return path`
- Worktree Escape User Waiver Missing: `Blocks mutation, branch/worktree changes, runtime launch, shortcut/provider/model actions, PR/release actions, and GitHub Desktop handoff outside C:\Nexus Worktrees\Governance`

## Allowed / Forbidden Scope

Allowed:

- Release Readiness digest source-truth drift repair only.
- USER-approved automation/worktree governance repair when the issue is non-runtime, multi-worktree safety related, and limited to source-truth/governance/validator/helper support.
- USER-approved phase-gate governance repair when a live branch exposes a repeatable Branch Readiness, PR Readiness, Release Readiness, or Workstream gate miss and the fix is limited to governance/source-truth/validator/helper prevention.
- Governance/source-truth wording that prevents Release Readiness from becoming a cleanup phase.
- Governance/source-truth wording that defines `Release Readiness Candidate Anchor` and keeps historical PR endpoints audit-only unless USER explicitly selects one as the release target.
- Governance/source-truth wording that defines aggregated release-window ownership when multiple FAM/worktree PRs merge before the next release.
- Governance/source-truth wording that routes stale/old branch cleanup to Branch Readiness branch/worktree setup instead of Release Readiness.
- Governance/source-truth wording that makes Branch Readiness classify stale, empty, merged, wrong-worktree, and open-PR carrier states before Stage 2 branch/worktree creation or cleanup.
- Validator support for standing intake, Release Readiness Health Pass, PR body firewall behavior, and registered source-truth validators when the intake repair changes the expected historical/current branch-record posture those validators enforce.
- Helper registry updates tied directly to those validators.
- Automation observability helper support for configured cwd/worktree identity, stale neutral-main detection, lane-sensitive prompt drift, automation memory/reporting mismatch, and `Automation CWD Worktree Mismatch` blocker reporting from Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md`.
- Assigned Worktree Confinement governance/validator support for this standing worktree.
- PR Readiness Stage 1 `Origin/Main Freshness Check` governance/validator support so Stage 1 reports branch-creation-base drift and reconciliation recommendations without fixing files by surprise.
- Branch Readiness product-system planning gate governance/validator support so broad implementation branches must prove project-wide vision alignment, branch-specific vision alignment, concept/entity/profile modeling, user workflow planning, scale/state planning, expected outcomes, Codex extra recommendations, and the USER critique/decision loop before Workstream.
- One PR per active `RRI-*` cycle after validation.

Forbidden:

- Runtime/provider/model/memory/voice/Core/shortcut/installer implementation.
- Release execution, tags, GitHub Releases, release artifacts, or release-note publication.
- Stale branch deletion, worktree removal, branch switching, or GitHub Desktop-bound worktree cleanup during Release Readiness.
- GitHub issue creation or issue-resolution branch work.
- AI Product Contract import or private Dev ORIN import.
- Direct-main mutation, broad docs churn, implementation branch planning, or selected-next runtime branch creation.
- Accepting anything other than a Release Readiness digest, USER-approved automation/worktree governance intake, USER-approved phase-gate governance intake, or same-PR standing-governance bot-review repair after the bootstrap setup cycle.
- Accepting runtime, implementation, release-execution, or branch-cleanup work through an automation/worktree governance intake.
- Cross-worktree mutation outside `C:\Nexus Worktrees\Governance` without `Worktree Escape User Waiver: Granted`.

## Return Digest Contract

After the governance PR merges and the standing branch syncs back to `origin/main`, the governance thread must output a return digest to the originating worktree/thread with:

- Originating Branch:
- Originating Worktree:
- Operating Workspace:
- Expected Branch:
- RRI Cycle ID:
- Governance PR:
- Merge Commit:
- Updated origin/main:
- Files Changed:
- Blockers Cleared:
- Blockers Remaining:
- Validations:
- Rebaseline Instructions:
- Next Legal Phase:

The originating lane remains paused in `Waiting For Governance Intake` or `Waiting For Updated Main` until this digest is received, `origin/main` is fetched, source truth is revalidated, and the phase resolver reports the next legal phase.

## Return Digest Identity Guard

The return digest must preserve the originating lane identity exactly as recorded by the accepted Release Readiness intake packet and the active `RRI-*` cycle ledger.

- Originating Branch Source: `Copy exactly from the accepted Release Readiness intake digest / recorded cycle identity; do not infer from the governance worktree, neutral main folder, or current shell CWD`
- Originating Worktree Source: `Copy exactly from the accepted Release Readiness intake digest / recorded cycle identity; do not infer from the governance worktree, neutral main folder, or GitHub Desktop's currently selected repository`
- Operating Workspace Requirement: `The originating-lane prompt must name the exact originating assigned worktree as its operating workspace and must also name the expected branch`
- Default Workspace Ban: `The governance lane must not default to C:\Nexus Desktop AI or C:\Nexus Worktrees\Governance unless that exact path is the recorded originating worktree for the accepted intake`
- Return Digest Origin Identity Missing: `Blocks return-digest handoff when the originating branch, originating worktree, operating workspace, or expected branch is absent, generic, contradictory, or inferred`
- Thread / Worktree Identity Mismatch: `Blocks originating-lane continuation when the return digest points at a different worktree or branch than the accepted intake recorded`
- Latest Closed Cycle Identity: `RRI-20260514-006 originated from Release Readiness post-release closure digest for v1.7.1-prebeta plus USER-approved public release-body standardization using the v1.6.13-prebeta structure with internal tooling labels removed`

## PR Body Firewall

GitHub PR bodies for this branch must stay evidence-only. They must use the standard `## Summary`, `## Branch Evidence`, and `## Validation` sections and must not include Codex phase-handoff/operator text such as `Next Legal Phase`, `Next Safe Move`, `Continue Decision`, `Exact next USER decision`, `Implemented, validated`, or `::git-*`.

## Branch Objective

Bootstrap and preserve the one legal standing governance intake lane so Release Readiness drift can be repaired without dirtying FAM-006, FAM-007, `main`, or future runtime worktrees.

## Target End-State

The setup PR merges, the standing branch is synced to current `origin/main`, no active `RRI-*` cycle remains recorded, GitHub Desktop can open `C:\Nexus Worktrees\Governance`, the branch authority record sits in historical / idle traceability on merged main, and the lane waits cleanly for the next USER-approved Release Readiness digest or automation/worktree governance intake.

## Backlog Completion Strategy

Branch Completion Goal: `Standing intake lane bootstrapped and validated`

Known Future-Dependent Blockers: `Future RRI cycles require a Release Readiness digest or USER-approved automation/worktree governance intake, clean sync to origin/main, USER-gated PR merge, and return digest before originating-lane continuation`

Branch Closure Rule: `The standing branch name and active standing authority persist after merge; merged main may still report No Active Branch for runtime/product work because the standing governance intake record is the only active-authority exception. Each intake cycle closes by PR merge, sync to origin/main, return digest, and Active RRI Cycle returning to None after the return-digest closeout is recorded by the next admitted intake or governance closeout path.`

## Expected Seam Families And Risk Classes

- Governance scope risk: keep the exception narrow so it does not reopen governance-only branches by default.
- Source-truth projection risk: ensure future Release Readiness blockers are routed before they become main repair work.
- Validator risk: keep standing-intake checks focused on branch identity, cycle count, sync posture, file scope, and return-digest markers.
- GitHub Desktop handoff risk: Desktop must point at `C:\Nexus Worktrees\Governance` when the USER operates this lane.

## User Test Summary Strategy

No runtime User Test Summary is required. Operator validation is repo-side: `git worktree list`, GitHub Desktop folder binding, governance validators, PR body audit, release body validator, and compile checks.

## Later-Phase Expectations

- Workstream: Not applicable unless a later USER-approved validator hardening seam is needed inside this same non-runtime branch class.
- Hardening: Optional repo-side hardening only if validation exposes a validator or source-truth defect in the standing-lane contract.
- Live Validation: Not applicable for runtime UI.
- PR Readiness: Open one governance PR for bootstrap or for one active `RRI-*` cycle after validation.
- Release Readiness: File-frozen validation only; it may produce future intake digests but must not mutate files.

## Active Seam

Active seam: `None - standing lane idle after RRI-20260514-007`

Seam Goal: `Idle until the next USER-approved Release Readiness digest or automation/worktree governance intake. RRI-20260514-007 repaired post-PR #152 active-authority closeout, selected-next/no-active distinction, and validator hardening.`

Seam Scope: `None active. Historical RRI-20260514-007 scope included this authority record, governance docs, helper registry text, dev/orin_branch_governance_validation.py, and registered source-truth validator support.`

Seam Non-Includes: `runtime/provider/model/memory/voice/Core/shortcut/installer work, release execution, issue work, FAM-006 or FAM-007 mutation, broad docs churn, or direct-main mutation.`

## Initial Workstream Seam Sequence

Seam 1: Standing Governance Intake Bootstrap

Goal: Create the durable branch authority record, governance docs, validator gate, PR body firewall, and helper registry truth for the standing lane.

Scope: `Docs/branch_records/index.md`, this branch authority record, governance/source-truth docs, `dev/orin_branch_governance_validation.py`, `dev/orin_pr_body_quality_audit.py`, and `Docs/validation_helper_registry.md`.

Non-Includes: runtime implementation, provider/model/memory/voice/Core/shortcut/installer changes, release execution, GitHub issues, AI Product Contract import, private Dev ORIN import, next runtime branch creation, or actual stale branch/worktree cleanup.

## Historical Seam

- Historical seam: `Standing Governance Intake Bootstrap`
- Status: `Active standing authority - after setup PR merge, the standing lane remains the only allowed active governance intake authority while idling with no runtime carrier; RRI-20260514-002 repaired the validator/source-truth mismatch that treated No Active Branch as requiring the standing authority record to be historical-only`

## Exit Criteria

- `Docs/branch_records/index.md` lists this record under Active Branch Authority Records as the single standing governance intake exception while merged-main runtime/product truth may still report No Active Branch.
- Governance docs describe the standing exception, allowed/forbidden scope, one-cycle limit, sync-to-main rule, originating-lane pause, and return digest.
- `dev/orin_branch_governance_validation.py --standing-governance-intake-gate` validates the branch identity, clean tracked state, source-truth markers, cycle count, sync/base posture, file scope, and return-digest identity guard.
- `dev/orin_pr_body_quality_audit.py` rejects PR body firewall markers.
- The setup PR merged and future intake PRs remain USER-gated for creation and merge.

## Rollback Target

- `Branch Readiness`

## Next Legal Phase

- `Release Readiness`
