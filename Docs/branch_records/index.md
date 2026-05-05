# Branch Authority Records Index

## Purpose

This index routes repo-owned authority records for approved branches that do not map to a promoted backlog workstream.

Use this layer for:

- active `Registry-only` backlog branches in `Branch Readiness` before a promoted canonical workstream exists
- `release packaging` branches
- active `repair/dev-tooling-governance` feature branches when USER-admitted repair scope includes developer-tooling plus governance hardening
- preserved historical `docs/governance` or `emergency canon repair` records

when those branches need a durable repo-owned phase authority record.

Do not use this layer to replace:

- `Docs/workstreams/` for promoted backlog-backed workstreams
- merge-target canon sync that belongs on an already-active implementation branch

## Rules

- branch authority records are for approved branches that do not yet map to a promoted canonical workstream
- active `Registry-only` backlog branches may use this layer during `Branch Readiness` before promotion
- active-branch-first remains the default during `pre-Beta`
- new governance-only branches are not used for Nexus work
- Standalone docs/governance, emergency canon repair, and repair-only feature branches are blocked for future Nexus work.
- Governance, docs, source-of-truth, and validator repairs must ride inside the next legitimate runtime-focused backlog branch during `Branch Readiness` or `PR Readiness`.
- If USER explicitly admits a real release-support or release-packaging carrier before the next runtime-focused branch, blocker-clearing governance closeout may ride inside that carrier's `Branch Readiness` before release-readiness work begins.
- If no runtime-focused branch is legally admitted yet, record the drift as a blocker and wait instead of creating a repair branch by inertia.
- Historical repair-only branch records remain traceability only and do not authorize new repair-only branch creation.
- Post-merge closeout proof must be in merged source truth, not only in a deleted branch, reflog, automation memory, or conversation transcript. If missing proof blocks release, carry the closeout on a real release-support carrier; if product work is next, carry it on the next real runtime package carrier.
- The one-time `codex/one-time-backlog-governance-repair` branch is USER-admitted as `repair/dev-tooling-governance` to repair the blocker rule that allowed FB-027/PR #109 drift; it does not reopen governance-only branch creation as a default path.
- between-branch canon repair is blocked
- missed PR Readiness canon work must be carried by the next legitimate runtime-focused backlog branch's `Branch Readiness` before implementation begins
- the `Active Branch Authority Records` list is only for branches that are still the current execution base
- when merged-main truth is `No Active Branch`, merge-stable current-state owners such as backlog and roadmap must not mirror transient repair-branch ownership; that transient repair execution truth belongs only in the active branch authority record until merge
- before PR merge, any branch that still relies on an active branch authority record must either move that record into `Historical Branch Authority Records` or remove it entirely so merged truth does not leave a stale active branch owner behind
- if a stale-canon or governance-drift class is discovered on a branch, that branch or the next legal repair surface must patch the canon or validator rule that allowed it before the repair is considered complete
- package/slice governance drift blockers are named `Single-Slice Package User Approval Missing` and `Package Completion Unproven`; active branch authority records that repair package admission drift must preserve those names exactly, and only `Admission State: Admitted` rows count toward package admission
- Element Coverage is a non-identity checklist for user-facing surface, runtime/backend behavior, fail-safe/recovery, security/privacy, voice/audio, external integration, local AI/capability packs, packaging/install, monitoring/HUD, validation, and release impact; Element Coverage rows never count as `Admission State: Admitted`, slices, seams, packages, FAMs, selected-next truth, or release drivers
- Branch Readiness stage-gate governance uses `Branch Readiness Stage 1 - Analysis Gate` as a no repository file mutation, no branch creation, no package admission, no docs sync review pass and `Branch Readiness Stage 2 - Execution Gate` as the approved work pass; `Branch Readiness Execution User Approval Missing` remains active until USER approval to enter Stage 2 is recorded
- PR Readiness stage-gate governance uses `PR Readiness Stage 1 - Analysis Gate` as a no repository file mutation review pass and `PR Readiness Stage 2 - Execution Gate` as the approved work pass; Stage 1 must include a user-facing `## Next Workstream` block with `Recommended Next Workstream:`, `User-Facing Output:`, candidate slices, dependencies/blockers, validation needs, release impact, selection-truth status, and branch-creation status; `Next Workstream Candidate Not Found` blocks Stage 1 when no legal candidate is found; `PR Readiness Execution User Approval Missing` remains active until USER approval to enter Stage 2 is recorded
- `PR Watcher Provisioning Unproven` is the standard blocker when a branch expects watcher-based PR monitoring but its watcher target, approved reporting surface, runtime path, run-proof method, fallback, teardown, or replacement provisioning for the next live PR is not yet explicit and proven
- `PR Watcher Routing Unverified` is the standard blocker when a branch expects watcher-based PR monitoring but the configured watcher target and delivery proof have not yet been cross-checked against the recorded reporting surface and proven to land there
- PR watcher delivery proof requires assistant-message transcript presence plus Codex thread-state refresh plus automation run/inbox visibility for the approved reporting surface; a watcher must not retire after merge until that final delivery proof is present
- Automation Observability Review Pending is checked with `dev/automation_observability_report.py`; Codex automation run/inbox rows and `$CODEX_HOME/automations/*/memory.md` are review inputs, while `BLOCKER_CANDIDATE` and `REVIEW_REQUIRED` findings require a bounded repair seam before repo canon changes
- historical branch authority records are preserved traceability records, not live execution authority
- historical-only closeout traceability records must report `Phase: Historical Traceability` and must not retain live PR state, active seam ownership, or open-PR narration
- each active branch authority record must carry the modern phase-state block:
  - `## Current Phase`
  - `## Phase Status`
  - `## Branch Class`
  - `## Blockers`
  - `## Entry Basis`
  - `## Exit Criteria`
  - `## Rollback Target`
  - `## Next Legal Phase`
- branch authority records should also explain:
  - why the branch exists
  - why it cannot or should not ride on an active implementation branch
  - what it must not change

## Active Branch Authority Records

- `Docs/branch_records/codex_v1_6_13_prebeta_post_merge_closeout_hardening.md`

## Historical Branch Authority Records

- `Docs/branch_records/codex_v1_6_13_prebeta_release_packaging.md`
- `Docs/branch_records/codex_one_time_backlog_governance_repair.md`
- `Docs/branch_records/feature_fb_049_runtime_branch_readiness.md`
- `Docs/branch_records/feature_pr105_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_pr104_watcher_next_prompt_format_repair.md`
- `Docs/branch_records/feature_pr103_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_pr102_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_pr101_post_merge_closeout_canon_repair.md`
- `Docs/branch_records/feature_automation_planning_post_merge_closeout_repair.md`
- `Docs/branch_records/feature_automation_planning_post_merge_canon_repair.md`
- `Docs/branch_records/feature_automation_planning.md`
- `Docs/branch_records/feature_backlog_family_governance_reform.md`
- `Docs/branch_records/feature_fb_048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md`
- `Docs/branch_records/feature_fb_047_active_session_relaunch_decline_preservation.md`
- `Docs/branch_records/feature_fb_046_active_session_relaunch_reacquisition.md`
- `Docs/branch_records/feature_fb_045_active_session_relaunch_stability.md`
- `Docs/branch_records/feature_fb_044_boot_desktop_handoff_outcome_refinement.md`
- `Docs/branch_records/feature_fb_043_top_level_entrypoint_handoff_refinement.md`
- `Docs/branch_records/codex_fb_037_release_debt_packaging.md`
- `Docs/branch_records/codex_no_active_branch_docs_governance_refinement.md`
- `Docs/branch_records/feature_fb_042_desktop_entrypoint_runtime_refinement.md`
- `Docs/branch_records/feature_fb_005_workspace_path_planning.md`
- `Docs/branch_records/feature_fb_030_orin_voice_audio_direction_refinement.md`
- `Docs/branch_records/feature_fb_030_release_readiness_canon_repair.md`
- `Docs/branch_records/feature_fb_030_successor_branch_truth_repair.md`
