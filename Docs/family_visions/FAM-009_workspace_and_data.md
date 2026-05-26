# Pending Fold Source: Workspace And Data

## Purpose

This file is retained only as no-loss source material while workspace/data direction is folded into existing backlog-family visions and architecture owners.

It is not an active backlog family, not a worktree lane, not a package owner, and not a FAM number reservation. The next USER-approved backlog family may reuse the next available FAM number after `FAM-008`.

Workspace layout, data roots, logs/evidence organization, support bundles, dev-toolkit data intake, and local file hygiene now fold into the implementing family vision and `Docs/ai_runtime_and_trust_architecture.md` where relevant.

## Vision Summary

Workspace and Data should keep Nexus understandable on disk. Evidence, logs, support bundles, user data, and dev outputs should have clear owners, retention expectations, and safe cleanup paths.

## Accepted Direction

- Keep live operational truth derived from Git, GitHub, or helpers, not copied into docs.
- Keep evidence roots organized and reviewable.
- Make support bundle and diagnostics paths traceable without exposing private data unnecessarily.
- AI operational cache storage, cache evidence, cache journaling paths, retention windows, corruption quarantine, and clear-cache file hygiene belong here only as workspace/data-root direction; cache contents remain governed by the AI/runtime and privacy owners.
- AI-related roots should distinguish operational cache, Trust Journal entries, support logs, backups, capability-pack indexes, model/capability-pack assets, and user data instead of collapsing them into one hidden data bucket.
- Cache corruption recovery should quarantine or rebuild damaged cache with reviewable evidence rather than silently reusing damaged state.
- Backup/export root guidance must not imply memory, cache, provider data, private Owner material, or capability-pack migration without a later USER-approved package and privacy/safety proof.
- Treat workspace cleanup and branch/worktree deletion as USER-gated operations with no unique commit loss proof.

## Implementation Boundaries

- This vision does not admit cleanup, deletion, data migration, support-bundle behavior changes, or GitHub Desktop rebinding by itself.
- Future workspace/data implementation must be owned by the backlog family whose surface is changing, with Branch Readiness approval and explicit cleanup/recovery proof.

## Fold Targets

- Project vision: `Docs/nexus_vision.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Backlog registry: `Docs/feature_backlog.md`
- Existing FAM vision records when their implementation touches workspace/data roots, evidence, cache storage, support bundles, or cleanup
- Historical workspace/data trace: `Docs/workstreams/FB-005_workspace_and_folder_organization.md`
- Worktree slot registry: `Docs/worktree_slots.md`
