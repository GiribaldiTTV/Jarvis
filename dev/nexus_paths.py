# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=workspace-root-paths; status=shared
"""Canonical current Nexus filesystem roots.

The neutral main workspace intentionally remains on C:. All other substantive
Nexus work and evidence uses the single approved D-drive data root.
"""

from __future__ import annotations

from pathlib import Path


NEUTRAL_MAIN_ROOT = Path(r"C:\Nexus Desktop AI")
NEXUS_DATA_ROOT = Path(r"D:\Nexus Desktop AI Data")
WORKTREES_ROOT = NEXUS_DATA_ROOT / "Worktrees"
EXTERNAL_STATE_ROOT = NEXUS_DATA_ROOT / "Governance State"
USER_HUB_ROOT = NEXUS_DATA_ROOT / "USER"
REPOS_ROOT = NEXUS_DATA_ROOT / "Repos"
DEV_ORIN_ROOT = NEXUS_DATA_ROOT / "Dev ORIN"
ARTIFACTS_ROOT = NEXUS_DATA_ROOT / "Artifacts"
CODEX_WORKTREES_ROOT = NEXUS_DATA_ROOT / "Codex Worktrees"
MIGRATION_EVIDENCE_ROOT = NEXUS_DATA_ROOT / "Migration Evidence"
GOVERNANCE_WORKTREE = WORKTREES_ROOT / "Governance"


def windows_text(path: Path) -> str:
    """Return a stable Windows display path for packets and diagnostics."""

    return str(path)
