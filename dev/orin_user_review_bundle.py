# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing Desktop review bundle from selected repo files.

This helper copies review files to a folder on the user's Desktop so USER review
does not depend on manually browsing the worktree. It never edits repo files.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _desktop_path() -> Path:
    home = Path.home()
    onedrive_desktop = home / "OneDrive" / "Desktop"
    if onedrive_desktop.is_dir():
        return onedrive_desktop
    return home / "Desktop"


def _safe_target(desktop: Path, folder_name: str) -> Path:
    target = (desktop / folder_name).resolve()
    desktop_resolved = desktop.resolve()
    if target == desktop_resolved or desktop_resolved not in target.parents:
        raise ValueError(f"Refusing to write outside Desktop: {target}")
    return target


def _copy_file(relative_file: str, target: Path) -> tuple[str, str]:
    source = (ROOT / relative_file).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Review source file not found: {relative_file}")
    if ROOT.resolve() not in source.parents:
        raise ValueError(f"Review source file is outside repo: {relative_file}")

    destination = target / relative_file
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return source.relative_to(ROOT).as_posix(), destination.relative_to(target).as_posix()


def build_bundle(folder_name: str, files: list[str], title: str, clear: bool) -> Path:
    desktop = _desktop_path()
    target = _safe_target(desktop, folder_name)
    if clear and target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    copied = [_copy_file(file_name, target) for file_name in files]
    created_at = datetime.now().isoformat(timespec="seconds")

    readme_lines = [
        f"# {title}",
        "",
        f"Created: {created_at}",
        f"Source repo: `{ROOT}`",
        "",
        "## Start Here",
        "",
        "Review these copied files from this Desktop folder. The repo source paths",
        "are listed below so the review can be traced back to source truth.",
        "",
        "## Files",
        "",
        "| Source path | Copied path |",
        "| --- | --- |",
    ]
    for source_rel, copied_rel in copied:
        readme_lines.append(f"| `{source_rel}` | `{copied_rel}` |")
    readme_lines.append("")

    (target / "START_HERE.md").write_text("\n".join(readme_lines), encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder-name", required=True, help="Desktop folder name to create or refresh.")
    parser.add_argument("--title", default="Nexus Review Bundle", help="Title for START_HERE.md.")
    parser.add_argument("--clear", action="store_true", help="Delete the existing Desktop bundle folder before copying.")
    parser.add_argument("files", nargs="+", help="Repo-relative files to copy into the Desktop review bundle.")
    args = parser.parse_args()

    target = build_bundle(args.folder_name, args.files, args.title, args.clear)
    print(f"Review bundle: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
