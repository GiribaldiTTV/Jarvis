# PR Watcher Mode Contract

## Purpose

PR watchers exist to prove live PR state, Codex bot-review state, same-branch repair authority, and merge verification on an approved Codex reporting surface.

This contract keeps watcher behavior predictable in multi-worktree PR Readiness by making every watcher declare one mode, one configured cwd, one PR, one branch, one delivery route, and one repair authority posture.

## Stage 2 Approval Default

PR Readiness Stage 2 approval includes watcher provisioning by default.

Do not ask for a separate watcher-specific approval after USER approves PR Readiness Stage 2 / PR creation. The Stage 2 approval authorizes the bounded watcher needed for that PR, including Verify Once, Silent Monitor, safe same-PR Repair Mode within the admitted PR scope, and merge-watch reporting.

Skipping watcher provisioning requires an explicit USER watcher waiver or a documented platform/runtime blocker. Manual live PR inspection may supplement watcher proof, but it does not replace the default watcher requirement unless the waiver or blocker is recorded.

## Watcher Modes

Silent Monitor:
- Default steady mode after initial proof.
- Inspect the live PR at the approved cadence.
- Stay quiet when watched values are unchanged.
- Report only watched-value changes, new or unresolved actionable review/comment state, status-check changes, merge/close state, routing/runtime-proof blockers, or configured-cwd drift.
- Silent Monitor is not a proof substitute; the watcher still needs runtime proof through heartbeat run evidence, thread/inbox output, automation memory/log/state updates, or scheduler last-run evidence.

Verify Once:
- One visible watcher verification post after watcher creation, watcher update, route repair, or USER request.
- Must include `Watcher Health Proof:` with the current configured cwd, worktree/branch, PR number, head SHA, unresolved review-thread count, latest bot review, repair authority, delivery route proof, and runtime proof.
- After the verification post, the watcher returns to Silent Monitor unless a blocker or actionable repair exists.

Repair Mode:
- Active only when an unresolved actionable Codex bot review/comment is safely inside the approved same-PR scope and current worktree identity is proven.
- Required repair loop: verify identity, evaluate the review against repo truth, patch only approved same-PR scope, run required validation, commit, push to the same branch, reply or resolve the addressed review thread when required, record `Comment addressed` for the current head SHA, and post a normal repair digest.
- Repair Mode must not cross worktrees, mutate `main`, perform release work, delete branches/worktrees, close issues, or implement runtime/provider/model/memory/voice/Core/shortcut/installer work unless that exact scope was already admitted for the PR.

Blocked Mode:
- Active when watcher route, cwd, branch, live PR data, delivery proof, review-thread detail, or repair authority is missing, stale, ambiguous, or outside approved scope.
- Must not patch.
- Must report the blocker, the watched value that failed, the exact missing proof, and the exact USER decision needed.

## Watcher Health Proof

PR Readiness Stage 2 final handoff and every Verify Once post must include:

- `Watcher Health Proof:`
- `Watcher Mode:`
- `Configured CWD:`
- `Worktree / Branch:`
- `PR:`
- `Head SHA:`
- `Mergeability:`
- `Unresolved Review Threads:`
- `Latest Bot Review:`
- `Repair Authority:`
- `Delivery Route Proof:`
- `Runtime Proof:`
- `Next Watcher Posture:`

## Delivery Rules

- Watcher configuration is not runtime proof.
- `ACTIVE` is configuration state, not run proof.
- Manual rollout-file or transcript-file injection does not count as delivery proof.
- Accepted delivery proof comes from assistant-message transcript presence, Codex thread-state refresh, automation run/inbox visibility, automation memory/log/state-file updates, or scheduler last-run evidence.
- If final merge delivery proof is missing, the watcher remains in Silent Monitor or Blocked Mode and must not retire.

## Repair Authority Boundaries

Repair Authority values:
- `Enabled - same-PR governance/source-truth scope`
- `Enabled - same-PR runtime scope`
- `Disabled - report only`
- `Blocked - USER decision required`

Out-of-scope bot requests, cross-worktree mutations, release execution, branch cleanup, issue closeout, or ambiguous comments must switch the watcher to Blocked Mode.
