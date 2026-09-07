# Nexus Workspace Roots

<!-- NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=workspace-root-routing; status=shared -->

This file is the durable current workspace-root map for Nexus Desktop AI. It
defines where current work and evidence live after the approved single-root
D-drive relocation. Historical receipts may retain older paths for audit
traceability; those receipts are not current routing authority.

## Current Roots

| Surface | Current canonical path | Authority boundary |
| --- | --- | --- |
| Neutral main / consolidator | `D:\Nexus Desktop AI\Product Repository` | Protected neutral `main`; physical successor of the former C workspace. |
| Active Git worktrees | `D:\Nexus Desktop AI\Worktrees` | Current FAM and Governance worktrees; Git worktree administration is authoritative. |
| Installed Governance Control Plane | `D:\Nexus Desktop AI\Governance Control Plane` | Operational policy and executable implementation selected by `current/manifest.json`; separate from mutable Governance State and temporary source carriers. |
| External operational state | `D:\Nexus Desktop AI\Governance State` | Active branch, worktree, planning, lock, review, and migration state; repo docs remain durable law. |
| USER review hub | `D:\Nexus Desktop AI\USER` | Current USER packet folders and timestamped upload ZIPs. |
| Repository recovery | `D:\Nexus Desktop AI\Repository Recovery` | Transitional fallback clones only; never the canonical product repository. |
| Private/dev ORIN root | `D:\Nexus Desktop AI\Project Support\Dev ORIN` | Private/dev evidence only; no import or runtime activation is implied. |
| Artifact root | `D:\Nexus Desktop AI\Project Support\Artifacts` | Generated evidence, models, and evaluation artifacts. |
| Codex-managed detached worktrees | `D:\Nexus Desktop AI\Codex Worktrees` | Detached Codex checkouts; they remain separate from active assigned lanes. |
| Relocation and rollback evidence | `D:\Nexus Desktop AI\Migration` | Copy manifests, parity receipts, rollback proof, and migration diagnostics only. |

## Routing Rules

1. The neutral main workspace is now `D:\Nexus Desktop AI\Product Repository`; no other copy may be
   treated as canonical main.
2. A current active branch worktree must resolve below
   `D:\Nexus Desktop AI\Worktrees` and must also be registered by Git
   worktree administration and the external state owner.
3. Current external state and USER packets must resolve below the D data root.
   A C-path occurrence in a historical receipt, fixture, or migration rollback
   record is evidence, not a current path.
4. Current operational execution must use the external Control Plane selected
   by its `current/manifest.json` and the explicit paths admitted by current
   approval. Retained repository helpers and `dev/nexus_paths.py` still contain
   their existing imports and historical C/old-Data defaults; this interface
   contract does not rewrite that code or establish that those helpers migrated.
   Their operational entrypoints are legacy references, not authorized entrypoints
   for live Governance work. Use the current external owner's selected entrypoints.
   Retained pure public test-support functions remain usable without machine-local
   operational directories. Legacy-code retention or later disposition is separate
   from the current external operational ownership.
5. No helper may silently fall back from a missing D current root to a C
   historical root. It must report the missing current root and stop or use an
   explicit caller-supplied path.
6. Operational packet and ZIP generation remains outside the repository. The
   external USER publication owner defines the approved workstream collections
   and the zero-or-one temporary selected review ZIP lifecycle. Workstream
   collections are evidence folders, not worktrees. No migration scratch,
   nested archives or stable un-timestamped ZIP belongs in the USER surface.

## Historical Path Handling

Older `C:\Nexus Worktrees`, `C:\Nexus Governance State`, and `C:\Nexus USER`
references remain in historical branch receipts, fixtures, and prior review
evidence where changing the text would destroy provenance. Current source
truth must point to this file instead of copying those historical paths into
new live-state records.
