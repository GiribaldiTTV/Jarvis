# Branch Authority Record: codex/fb-037-release-debt-packaging

## Branch Identity

- Branch: `codex/fb-037-release-debt-packaging`
- Workstream: `FB-037`
- Branch Class: `release packaging`

## Historical Pass Record Identity

- Family Anchor ID: `FB-027`
- Family Anchor Title: `Interaction and shared-action family anchor`
- Family Dossier Doc: `Docs/workstreams/FB-027_interaction_shared_action_family_dossier.md`
- Backlog Registry Class: `Historical Pass Alias`
- Historical Alias Of: `FB-027`
- Pass ID: `F027-P04`
- Alias Role: `Historical Pass Record`
- Standalone Selection Status: `Not independently selectable`
- Converted By Seam: `Phase 5 - Historical Pass Record Conversion / Slice R5-S3 - Convert corresponding branch records`
- Corresponding Historical Workstream Record: `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`
- Preservation Rule: `This record keeps the preserved release-packaging trace for the historical pass; the family dossier owns cross-pass indexing.`

## Purpose / Why It Exists

Open the release-packaging lane for FB-037 after the implementation branch merged to `main` as unreleased implementation debt.

This branch exists to prepare the public prerelease, release-state canon transitions, baseline or release-note artifacts, and tag/release plan needed to clear `Release Debt` for FB-037 without admitting FB-038 or reopening product implementation work.

## Current Phase

- Phase: `Release Readiness`

## Phase Status

- Historical completed branch record.
- branch was created from updated `main`
- local `main` and `origin/main` resolve to merge commit `d1277e65cf348073c73f636c8dd1b5965543f1a8`
- this branch is based on that merge commit and carries release-packaging commits on top of it
- branch merged to `main` in merge commit `1bab4b2`
- FB-037 is released as `v1.4.0-prebeta` on this release-execution branch
- FB-037 `Release Debt` is cleared in release-state canon
- while this release branch was active, FB-038 remained selected in canon only and had no branch
- Branch Readiness, Workstream Slice 1, release-artifact Hardening, release-packaging Live Validation, and PR Readiness are complete
- release-packaging PR Readiness closed after merge-target canon, release-boundary proof, successor branch deferral, Governance Drift Audit, and PR gate validation passed
- Release Readiness executed the release-state canon transition for FB-037; Git tag `v1.4.0-prebeta` is the supported public release artifact in this environment
- GitHub Release publication is not supported in this environment because `gh` and API credentials are unavailable; the API lookup remains the publication proof point
- this record is preserved for historical traceability only and is not active execution authority after merge

## Branch Class

- `release packaging`

## Release-Bearing Markers

- Release Target: `v1.4.0-prebeta`
- Release Scope: FB-037 curated built-in Windows utility catalog prerelease, including Task Manager, Calculator, Notepad, and Paint built-ins plus saved-action override, authoring collision, confirm/result preservation, callable-group regression preservation, and reusable helper proof support.
- Release Artifacts: release notes, active `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`, release-state transition checklist, `v1.4.0-prebeta` Git tag, and public prerelease notes content.

## Blockers

- None

## Entry Basis

- updated `main` is aligned with `origin/main`
- at branch admission, FB-037 was the current merged-unreleased release-debt owner
- repo truth before this branch resolved to `Release Readiness`, `No Active Branch`, and `Release Debt` (FB-037)
- the release floor for FB-037 is `minor prerelease`
- latest public prerelease is `v1.3.1-prebeta`
- target release version is planned as `v1.4.0-prebeta`
- at branch admission, FB-038 was selected as the next implementation workstream in canon only
- at branch admission, no FB-038 branch existed

## Exit Criteria

- release target, release scope, and release artifacts are explicit and validated
- release-state canon transitions mark FB-037 `Released (v1.4.0-prebeta)` and `Closed`
- `Release Debt` for FB-037 is cleared
- the `v1.4.0-prebeta` rebaseline is active
- release-state transition checklist remains complete and ordered as historical proof
- this release branch preserved FB-038 as selected in canon only and unbranched until updated `main` was revalidated
- no product or runtime work is introduced

## Rollback Target

- `PR Readiness`

## Next Legal Phase

- `Release Readiness` (same-phase release execution pass; `Release execution` is not a separate canonical phase)

## Target Release Version

- released version: `v1.4.0-prebeta`
- basis: latest public prerelease is `v1.3.1-prebeta`, and FB-037 carries a `minor prerelease` release floor
- release-state note: release execution marks FB-037 released, clears `Release Debt`, activates the rebaseline, and creates the `v1.4.0-prebeta` Git tag

## Release Scope

FB-037 release packaging covers the merged built-in catalog expansion:

- built-in Task Manager action
- built-in Calculator action
- built-in Notepad action
- built-in Paint action
- saved-action override authority over built-in aliases
- authoring collision protection for built-in phrases
- confirm/result flow preservation for built-ins and saved-action overrides
- callable-group regression preservation from the released FB-041 baseline
- reusable live-validation helper reliability improvements that supported FB-037 proof

## Release-Facing Updates Applied

The release execution slice updates:

- `Docs/feature_backlog.md`
  - move FB-037 from `Merged unreleased on main` to `Released (v1.4.0-prebeta)`
  - move `Record State` from `Promoted` to `Closed`
  - clear `Release Debt`
- `Docs/prebeta_roadmap.md`
  - update latest public prerelease to `v1.4.0-prebeta`
  - update latest public release commit to the release commit
  - remove FB-037 from current release debt
  - preserve FB-038 as selected-next canon only until Branch Readiness after release
- `Docs/workstreams/index.md`
  - move FB-037 from `Merged / Release Debt Owners` to `Closed`
- `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`
  - convert the current release-debt truth to released historical truth
  - clear `Release Debt`
  - finalize release evidence and release notes references
- `Docs/closeout_index.md`
  - update the current Nexus-era baseline pointer if a new rebaseline is created
- `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`
  - activate the Slice 1 draft as the current Nexus-era rebaseline
- Git tag and release artifacts
  - tag: `v1.4.0-prebeta`
  - release notes covering the FB-037 built-in catalog milestone

## Workstream Slice Plan

### Slice 1: Release Artifact And Transition Draft

Boundary:

- draft the `v1.4.0-prebeta` release notes content for FB-037
- decide whether the release needs a new Nexus pre-Beta rebaseline file
- if a rebaseline is needed, prepare the draft baseline file without changing latest-public-release truth yet
- prepare the exact release-state transition checklist for the later release execution pass
- keep FB-037 as `Merged unreleased on main` with `Release Debt` active until tag/release execution happens; this was the pre-release boundary, not current release truth

Explicit non-includes:

- no product or runtime code changes
- no release tag creation
- no publishing
- no marking FB-037 released
- no clearing `Release Debt`
- no FB-038 branch creation
- no next implementation admission

Validation target:

- `python dev/orin_branch_governance_validation.py`
- `git diff --check`
- live branch check that no FB-038 branch exists
- release-truth check that `v1.4.0-prebeta` does not already exist as a tag before release execution

Continuation rule:

- keep this as a single-slice Workstream plan until release artifacts are prepared and validated
- do not run a multi-seam release execution chain because release notes, rebaseline, canon transition, tag creation, and publishing cross release-state boundaries and should be gated separately

## Workstream Progress

- Workstream Slice 1 complete:
  `Release Artifact And Transition Draft`
- release target review passed for `v1.4.0-prebeta`
- release scope review passed and remains limited to FB-037 built-in catalog release packaging
- draft release notes, draft rebaseline, and release-state transition checklist are complete and internally consistent
- at Workstream completion, no tag existed, no release was published, no released-state canon updates had been applied, and `Release Debt` remained active
- no product or runtime work was introduced
- phase authority transitioned from `Workstream` to `Hardening`

## Hardening Progress

- Hardening complete:
  `Release Artifact Pressure Review`
- release target `v1.4.0-prebeta` remains correct and roadmap-aligned
- release scope remains bounded to FB-037 delivered behavior
- draft release notes do not overclaim settings, protocol, new target-kind, launcher-policy, UI, callable-group, or FB-038 work
- draft rebaseline remains internally consistent and explicitly inactive until release execution
- release-state transition checklist is complete, ordered, and preserves FB-038 branch deferral
- at Hardening completion, no tag existed, no release was published, no released-state canon updates had been applied, and `Release Debt` remained active
- no product or runtime work was introduced
- phase authority transitioned from `Hardening` to `Live Validation`

## Live Validation Progress

- Live Validation complete:
  `Release Boundary Proof`
- branch-truth correction was made durable in commit `e1dd905`
- release target `v1.4.0-prebeta` remained planned and unreleased during Live Validation
- release scope remained bounded to FB-037 delivered built-in catalog behavior and supporting proof artifacts
- draft release notes remained accurate and did not claim settings/protocol, new target-kind, launcher-policy, UI, callable-group, or FB-038 work
- draft rebaseline remained explicitly inactive and did not override the active `v1.3.1-prebeta` baseline
- release-state transition checklist remained complete and ordered for the later release execution pass
- local tag check confirmed no `v1.4.0-prebeta` tag exists
- remote tag check confirmed no `v1.4.0-prebeta` tag exists on `origin`
- GitHub release lookup for `v1.4.0-prebeta` returned `404`
- FB-037 remained `Merged unreleased on main` with `Release Debt` active during Live Validation
- during Live Validation, FB-038 remained selected in canon only and no local or remote FB-038 branch existed
- no product or runtime work was introduced
- phase authority transitioned from `Live Validation` to `PR Readiness`

## Governance Drift Audit

- Governance Drift Found: No
- Drift Type: None for this PR Readiness closeout; prior release-target governance drift was already corrected earlier on this branch
- Why Current Canon Failed To Prevent It: Not applicable for this closeout pass; current canon now requires release-bearing branches to carry `Release Target:`, `Release Scope:`, and `Release Artifacts:` markers before Release Readiness can report green
- Required Canon Changes: None
- Whether The Drift Blocks Merge: No
- Whether User Confirmation Is Required: No
- Missing blocker check: no missing PR Readiness blocker remains; stale canon, post-merge state, dirty branch, docs sync, next-workstream selection, and release-target marker gates are all represented in current governance
- Weak phase entry or exit rule check: no unresolved weakness remains; Release Readiness is reached only after PR Readiness validation and this Governance Drift Audit
- Weak source-of-truth ownership rule check: branch authority record remains the phase owner for this release-packaging branch, while the FB-037 workstream doc remains the promoted workstream and release-debt owner
- Stale prompt scaffolding or operator example check: no stale prompt-scaffold drift was found in this closeout pass
- Missing validator requirement check: the normal governance validator and PR-readiness gate mode both pass before this phase transition

## PR Readiness Closeout

- PR Readiness complete:
  - merge-target canon still represented FB-037 as `Merged unreleased on main` with `Release Debt` active until release execution
  - release target, release scope, and release artifacts are explicit in this authority record
  - draft rebaseline remains inactive and does not override the active `v1.3.1-prebeta` baseline
  - no local or remote `v1.4.0-prebeta` tag exists
  - GitHub release lookup for `v1.4.0-prebeta` returned `404`
  - during PR Readiness, FB-038 remained selected in canon only and no FB-038 branch existed
  - Governance Drift Audit completed with no blocking drift
  - no product or runtime work was introduced
- phase authority transitioned from `PR Readiness` to `Release Readiness`

## Release Execution Progress

- Release Readiness release execution complete for FB-037.
- release-state canon marks FB-037 `Released (v1.4.0-prebeta)` and `Closed`
- `Release Debt` for FB-037 is cleared
- `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md` is active
- `Docs/closeout_index.md` points to the `v1.4.0-prebeta` rebaseline
- release notes are preserved in this branch record
- Git tag: `v1.4.0-prebeta`
- GitHub Release publication: unsupported in this environment because no `gh` CLI or API token is available
- at release execution completion, FB-038 remained selected in canon only and unbranched
- no product or runtime work was introduced

## Release Notes

Release notes for `v1.4.0-prebeta`:

Title:

- `v1.4.0-prebeta - Curated built-in actions`

Summary:

- Adds the first curated built-in Windows utility catalog under the existing shared action model.
- Built-ins now include Task Manager, Calculator, Notepad, and Paint.
- Saved actions continue to win over built-ins when a saved action matches the same phrase.
- Authoring collision protection prevents create/edit flows from silently overriding built-in phrases.
- Confirm and result surfaces remain on the existing interaction flow.
- Callable-group execution and single-action behavior remain unchanged.

Included:

- `open_task_manager` targeting `taskmgr.exe`
- `open_calculator` targeting `calc.exe`
- `open_notepad` targeting `notepad.exe`
- `open_paint` targeting `mspaint.exe`
- exact alias coverage for `open ...`, bare utility name, and `launch ...` phrases for each built-in
- source-loaded saved-action override behavior for built-in phrase collisions
- create/edit authoring rejection for built-in phrase collisions
- manifest-backed Live Validation evidence across built-in execution, saved-action override, authoring boundary, mixed environment, and repeated execution scenarios

Not included:

- no Nexus settings or protocol actions
- no new target kinds
- no shell arguments or launcher-policy changes
- no UI redesign or confirm/result copy changes
- no callable-group behavior changes
- no FB-038 taskbar/tray or Create Custom Task work

Validation evidence:

- repo-side shared-action, saved-action source, authoring, interaction, callable-group, and governance validators passed during the FB-037 implementation branch
- closeout-grade Live Validation evidence is preserved at `dev\logs\launcher_live_window_audit\20260420_112713\manifest.json`

## Slice 1 Rebaseline Decision

- Rebaseline required: `Yes`
- Reason: `v1.4.0-prebeta` is a minor prerelease that adds a user-facing built-in catalog milestone and materially updates the shared pre-Beta interaction baseline.
- Draft file prepared:
  - `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`
- Activation rule:
  - release execution activates this baseline by creating the `v1.4.0-prebeta` tag, updating release-state canon, and pointing `Docs/closeout_index.md` at the new baseline.

## Slice 1 Release-State Transition Checklist

Release execution performed these steps in order:

1. Confirm `v1.4.0-prebeta` tag does not already exist.
2. Before release execution, confirm no FB-038 branch exists.
3. Before release execution, confirm FB-037 still remains `Promoted`, `Merged unreleased on main`, and blocked by `Release Debt`.
4. Update `Docs/feature_backlog.md`:
   - `Status: Released (v1.4.0-prebeta)`
   - `Record State: Closed`
   - `Target Version: v1.4.0-prebeta`
   - remove FB-037 `Blocker: Release Debt`
   - remove or replace the planned release-packaging target marker
5. Update `Docs/prebeta_roadmap.md`:
   - latest public prerelease: `v1.4.0-prebeta`
   - latest public release commit: release execution commit
   - remove FB-037 from current release debt
   - move FB-037 into released or recently closed context
   - keep FB-038 selected with release-time branch-deferral wording
6. Update `Docs/workstreams/index.md`:
   - remove FB-037 from `Merged / Release Debt Owners`
   - add FB-037 under `Closed`
7. Update `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`:
   - set `Record State` to `Closed`
   - set `Status` to `Released (v1.4.0-prebeta)`
   - set `Target Version` to `v1.4.0-prebeta`
   - clear the release-debt blocker
   - convert the current release-debt note into historical released truth
   - reference release notes and the `v1.4.0-prebeta` rebaseline
8. Update `Docs/closeout_index.md`:
   - point current Nexus-era baseline to `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`
9. Finalize `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`:
   - remove draft-only wording
   - make it the active released baseline only after the tag/release step is authorized
10. Update this branch authority record for PR-safe merge truth:
    - move it from active branch authority to historical branch authority before PR readiness, or remove it if no durable record is needed
11. Run:
    - `python dev/orin_branch_governance_validation.py`
    - `git diff --check`
12. Create or confirm the Git tag:
    - `v1.4.0-prebeta`
13. Prepare/publish release notes using the Slice 1 draft notes above.
14. Confirm no stale FB-037 `Release Debt` references remain in current-state canon.
15. Confirm FB-038 remains unbranched through release execution until updated `main` is revalidated for Branch Readiness.

## Explicit Non-Goals

- no product or runtime code changes
- no new built-in actions
- no settings or protocol behavior
- no launcher-policy changes
- no UI or confirm/result changes
- no release tag creation before the explicit Release Readiness execution pass
- no marking FB-037 released before the explicit Release Readiness execution pass
- no FB-038 branch creation
- no next implementation admission work

## Reuse Baseline

- `Docs/workstreams/FB-037_built_in_actions_and_settings_expansion.md`
- `Docs/closeouts/nexus_prebeta_rebaseline_through_v1.4.0-prebeta.md`
- `Docs/prebeta_roadmap.md`
- `Docs/feature_backlog.md`
- `Docs/workstreams/index.md`
- prior FB-037 Live Validation evidence at `dev\logs\launcher_live_window_audit\20260420_112713\manifest.json`

## Validation Contract

Branch Readiness validation proved:

- branch authority record exists and declares `release packaging`
- branch authority record carries `Release Target:`, `Release Scope:`, and `Release Artifacts:`
- branch remains based on updated `main`
- FB-037 remained merged unreleased until release execution
- planned target version did not imply release completion
- at Branch Readiness validation time, FB-038 remained selected in canon only and no FB-038 branch existed
- no product or runtime files changed
- `python dev/orin_branch_governance_validation.py` passes
- `git diff --check` passes

Workstream planning validation proved:

- branch authority record now owns `Workstream` for this release-packaging branch
- branch authority record keeps explicit release-bearing markers for `Release Target:`, `Release Scope:`, and `Release Artifacts:`
- FB-037 remained `Merged unreleased on main`
- `Release Debt` remained active until release execution
- planned target version did not imply release completion
- at Workstream planning validation time, FB-038 remained selected in canon only and no FB-038 branch existed
- no product or runtime files changed

Hardening validation proved:

- branch authority record now owns `Hardening` for this release-packaging branch
- release artifact set remains complete and internally consistent
- draft rebaseline remained inactive until release execution
- no `v1.4.0-prebeta` tag existed before release execution
- FB-037 remained `Merged unreleased on main` with `Release Debt` active
- at Hardening validation time, FB-038 remained selected in canon only and no FB-038 branch existed
- no product or runtime files changed

Live Validation proved:

- branch authority record now owns `Live Validation` for this release-packaging branch
- release-boundary evidence confirmed `v1.4.0-prebeta` remained planned and unreleased
- `Release Debt` remained active until release execution
- draft rebaseline remained inactive until release execution
- no `v1.4.0-prebeta` tag existed before release execution
- no release was published before release execution
- no released-state canon updates were applied before release execution
- at Live Validation time, FB-038 remained selected in canon only and no FB-038 branch existed
- no product or runtime files changed

Release execution validation must prove:

- release-state canon transitions are complete
- release artifacts are present and internally consistent
- `Release Target Undefined` is not active because release-bearing markers remain explicit
- the release tag points to the intended release commit
- no stale FB-037 release-debt references remain after release
- next implementation admission remains deferred until updated `main` is revalidated
