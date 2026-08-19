# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=workspace-root-paths; status=shared
"""Canonical current Nexus filesystem roots.

The canonical neutral-main repository is on D:. The former C workspace is
retained only as rollback and historical evidence. All other substantive Nexus
work and evidence uses the single approved D-drive data root.
"""

from __future__ import annotations

from pathlib import Path


NEUTRAL_MAIN_ROOT = Path(r"D:\Nexus Desktop AI\Product Repository")
NEXUS_DATA_ROOT = Path(r"D:\Nexus Desktop AI")
WORKTREES_ROOT = NEXUS_DATA_ROOT / "Worktrees"
EXTERNAL_STATE_ROOT = NEXUS_DATA_ROOT / "Governance State"
USER_HUB_ROOT = NEXUS_DATA_ROOT / "USER"
REPOS_ROOT = NEXUS_DATA_ROOT / "Repository Recovery"
DEV_ORIN_ROOT = NEXUS_DATA_ROOT / "Project Support" / "Dev ORIN"
ARTIFACTS_ROOT = NEXUS_DATA_ROOT / "Project Support" / "Artifacts"
CODEX_WORKTREES_ROOT = NEXUS_DATA_ROOT / "Codex Worktrees"
MIGRATION_EVIDENCE_ROOT = NEXUS_DATA_ROOT / "Migration"
GOVERNANCE_WORKTREE = WORKTREES_ROOT / "Governance"


def windows_text(path: Path) -> str:
    """Return a stable Windows display path for packets and diagnostics."""

    return str(path)
