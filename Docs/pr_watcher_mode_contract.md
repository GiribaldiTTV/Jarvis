# PR Watcher Mode Contract

## Purpose

This contract now denies recurring PR watcher automation by default for bounded PR Readiness Stage 2 and preserves watcher modes only for explicit exceptions or historical receipts.

Bounded PR Readiness Stage 2 must use direct PR verification through GitHub connector, `gh`, GraphQL, status checks, or the active Codex turn. Direct PR verification owns live PR state, Codex bot-review state, same-branch repair authority, mergeability, merge/close verification, and the post-repair approval latch unless the USER separately approves a watcher exception.

If the USER explicitly approves a watcher exception for one PR, the watcher must declare one mode, one configured cwd, one PR, one branch, one delivery route, and one repair authority posture before it can run.

GitHub connector output is live PR evidence, not durable repo ledger truth. Current PR reactions, unresolved review-thread counts, bot-review state, mergeability, head SHA, reviewer comments, watcher runtime health, and connector availability belong to Git/GitHub/helper-derived truth, watcher proof, Codex digest, or USER review evidence while the PR is active. Repo docs may preserve compact historical receipts after the live fact is checked and digested, but they must not become the current PR-state ledger.

## Stage 2 Direct PR Verification Default

Bounded PR Readiness Stage 2 denies recurring PR watcher automation by default.

Do not create or update heartbeat, cron, same-thread, or fallback PR watcher automations during bounded PR Readiness Stage 2 unless the USER explicitly approves a named watcher exception for that PR after seeing the direct PR verification plan. A normal Stage 2 approval authorizes PR creation, direct live PR inspection, same-PR Codex review repair within admitted scope, validation, push, concise revalidation comments, and direct merge/close verification. It does not authorize recurring watcher provisioning.

The required default proof is `Direct PR Verification Proof:` in the Codex digest or helper output, including configured cwd, PR number, head SHA, mergeability, unresolved review-thread count, latest bot review, status checks, repair authority, approval latch posture, and next PR posture. If a stale watcher automation exists for the same PR, Codex must delete or pause it before relying on direct PR verification.

Direct PR2 Continuation Rule:
- Bounded PR2 direct verification must keep running in the active Codex turn after PR creation, after each same-PR repair push, and after each Codex Connector revalidation request until a terminal PR2 state is reached.
- Terminal PR2 states are: a new actionable Codex Connector comment/review is found and repaired or blocked, a later Codex Connector thumbs-up reaction or green approval comment appears on the current head and mergeability is green, the PR merges/closes, or a real blocker prevents further direct verification.
- No watcher does not mean no loop. Do not stop merely because the Codex bot has not answered yet, because mergeability is temporarily unknown, or because the prior verification pass was quiet.
- When merge authority is already approved and the current head has the required Codex Connector approval latch plus green mergeability, bounded PR2 must merge and then directly verify the merged/closed PR state before handoff.
- When repeated same-family Codex Connector comments trigger `Review Churn Root-Cause Gate`, direct PR2 must pause revalidation requests until a local adversarial review-churn harness inspects every review-thread page and every pull-review-comment page, reports total/resolved/unresolved/outdated/unresolved-current counts, clusters all Codex Connector review comments, proves source-truth / implementation / fixture / generated-mutation coverage for each family, proves every changed helper/validator/parser file has family coverage, and emits a final local Codex Connector simulation digest. A quiet PR thread, resolved latest comment, or validator green is not enough to resume PR2 while this gate is active.

## Exception Watcher Modes

These modes are exception-only. They remain valid for historical receipts and for a future USER-approved watcher exception, not as the bounded PR2 default.

Silent Monitor:
- Exception steady mode after initial proof.
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
- Required repair loop: verify identity, evaluate the review against repo truth, patch only approved same-PR scope, run required validation, commit, push to the same branch, reply or resolve the addressed review thread when required, record `Comment addressed` for the current head SHA, request Codex Connector bot revalidation with a 3-5 word PR comment only, and keep `PR Validation Pending` active until a later Codex Connector bot thumbs-up reaction or green bot approval comment appears on the live PR after the repair. Approval proof must be bound to the current live PR head by review commit SHA, PR timeline order, or equivalent GitHub live-head evidence, not by local commit time alone.
- PR conversation comments that request Codex Connector review or revalidation must be 3-5 words only, preferably `@codex review please`; place head SHAs, validation summaries, repair narratives, and governance proof in the Codex thread digest, helper output, validator output, or external operational state instead.
- Repair Mode must not cross worktrees, mutate `main`, perform release work, delete branches/worktrees, close issues, or implement runtime/provider/model/memory/voice/Core/shortcut/installer work unless that exact scope was already admitted for the PR.

Blocked Mode:
- Active when watcher route, cwd, branch, live PR data, delivery proof, review-thread detail, or repair authority is missing, stale, ambiguous, or outside approved scope.
- Must not patch.
- Must report the blocker, the watched value that failed, the exact missing proof, and the exact USER decision needed.

## Watcher Health Proof

Watcher Health Proof is required only for an explicit USER-approved watcher exception or a historical watcher receipt. Bounded PR Readiness Stage 2 final handoff uses `Direct PR Verification Proof:` by default. Every Verify Once post for an approved watcher exception must include:

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
- If final merge delivery proof is missing for an approved watcher exception, the watcher remains in Silent Monitor or Blocked Mode and must not retire.
- GitHub connector reads may supply live proof for the fields above, but connector output must not be pasted into durable repo docs as current state. If a PR body, branch record, review packet, or release digest needs durable proof, record only a compact historical receipt after the evidence is digested.

## Reliability Degradation

- Recurring PR watcher automation is denied by default for bounded PR Readiness Stage 2 because the current heartbeat/watch runtime has proven inconsistent. Do not create a fallback watcher to compensate for an unreliable watcher unless the USER explicitly approves that exception.
- A configured automation that misses Verify Once, cannot emit into the approved reporting surface, cannot inspect review-thread detail, or cannot perform the admitted same-PR repair loop must be downgraded to `Background Observability` for that PR.
- Background Observability may report evidence, but it cannot clear `PR Watcher Provisioning Unproven`, `PR Watcher Routing Unverified`, `Automation Runtime Unproven`, `Bot Review Signal Pending`, or `PR Merge Verification Pending`.
- If the native Codex heartbeat watcher is unreliable, Codex must stop using the watcher path, delete or pause the stale automation when authorized, and proceed through direct PR verification unless the USER explicitly approves a watcher exception.
- Stale automation memory or historical toolchain-path findings are not current blockers unless a current source-truth owner still declares the path, PR, branch, or worktree as active.

## Repair Authority Boundaries

Repair Authority values:
- `Enabled - same-PR governance/source-truth scope`
- `Enabled - same-PR runtime scope`
- `Disabled - report only`
- `Blocked - USER decision required`

Out-of-scope bot requests, cross-worktree mutations, release execution, branch cleanup, issue closeout, or ambiguous comments must switch the watcher to Blocked Mode.
