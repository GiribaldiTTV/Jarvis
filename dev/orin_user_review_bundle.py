# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing Desktop review bundle from selected repo files.

This helper copies review files to a folder on the user's Desktop so USER review
does not depend on manually browsing the worktree. It never edits repo files.
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
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


def _clear_readonly(function, path: str, _exc_info) -> None:
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
    function(path)


def _clear_target(target: Path) -> None:
    try:
        shutil.rmtree(target, onexc=_clear_readonly)
    except TypeError:
        shutil.rmtree(target, onerror=_clear_readonly)


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


def _git_output(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return "UNKNOWN"


def _markdown_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- None recorded."]
    return [f"- {item}" for item in items]


def build_bundle(
    *,
    folder_name: str,
    files: list[str],
    title: str,
    clear: bool,
    review_purpose: str,
    validation_summary: str,
    review_order: list[str],
    exact_user_decision: str,
    pending_user_decisions: list[str],
    expected_file_count: int | None,
) -> Path:
    desktop = _desktop_path()
    target = _safe_target(desktop, folder_name)
    if clear and target.exists():
        _clear_target(target)
    target.mkdir(parents=True, exist_ok=True)

    copied = [_copy_file(file_name, target) for file_name in files]
    copied_count = len(copied)
    expected_count = expected_file_count if expected_file_count is not None else copied_count
    if expected_count != copied_count:
        raise ValueError(
            "Review bundle file count mismatch: "
            f"expected {expected_count} repo files, copied {copied_count}"
        )
    created_at = datetime.now().isoformat(timespec="seconds")

    source_branch = _git_output("branch", "--show-current")
    source_head = _git_output("rev-parse", "HEAD")
    upstream = _git_output("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    origin_main = _git_output("rev-parse", "origin/main")
    bundle_file_count = copied_count + 1

    readme_lines: list[str] = [
        f"# {title}",
        "",
        "## Review Packet",
        "",
        f"Review Purpose: {review_purpose}",
        f"Source Repo: `{ROOT}`",
        f"Source Branch: `{source_branch}`",
        f"Source HEAD: `{source_head}`",
        f"Upstream: `{upstream}`",
        f"origin/main: `{origin_main}`",
        f"Bundle Created: {created_at}",
        f"Bundle File Count: {bundle_file_count}",
        f"Expected File Count: {expected_count}",
        f"Copied File Count: {copied_count}",
        f"Validation Summary: {validation_summary}",
        f"Exact USER Decision This Bundle Supports: {exact_user_decision}",
        "",
        "## Pending USER Decisions",
        "",
        *_markdown_lines(pending_user_decisions),
        "",
        "## Review Order",
        "",
        *_markdown_lines(review_order),
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
    parser.add_argument(
        "--review-purpose",
        required=True,
        help="Why USER is reviewing this bundle.",
    )
    parser.add_argument(
        "--validation-summary",
        required=True,
        help="Validation proof or status supporting the review bundle.",
    )
    parser.add_argument(
        "--review-order",
        action="append",
        default=[],
        help="Repeatable suggested review step for START_HERE.md.",
    )
    parser.add_argument(
        "--exact-user-decision",
        required=True,
        help="Exact USER decision this bundle is meant to support.",
    )
    parser.add_argument(
        "--pending-user-decision",
        action="append",
        default=[],
        help="Repeatable pending USER decision that remains outside this bundle.",
    )
    parser.add_argument(
        "--expected-file-count",
        type=int,
        help="Expected count of repo files copied into the review bundle.",
    )
    parser.add_argument("files", nargs="+", help="Repo-relative files to copy into the Desktop review bundle.")
    args = parser.parse_args()

    target = build_bundle(
        folder_name=args.folder_name,
        files=args.files,
        title=args.title,
        clear=args.clear,
        review_purpose=args.review_purpose,
        validation_summary=args.validation_summary,
        review_order=args.review_order,
        exact_user_decision=args.exact_user_decision,
        pending_user_decisions=args.pending_user_decision,
        expected_file_count=args.expected_file_count,
    )
    print(f"Review bundle: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
