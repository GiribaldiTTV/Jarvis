# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing Desktop review bundle from selected repo files.

This helper copies review files to a stable worktree-labeled folder on the
user's Desktop so USER review does not depend on manually browsing the
worktree. It never edits repo files.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import subprocess
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEW_ROOT_NAME = "Nexus USER Review"
CUSTOM_REVIEW_PATH_NONE = "None - stable review root enforced"
PUBLIC_REVIEW_BUNDLE_LEAK_PREVENTION_STATUS = (
    "PASS - copied file list and START_HERE file-list metadata are repo-relative "
    "and exclude Owner/Dev private path patterns; copied file content remains "
    "source truth for USER inspection."
)
REVIEW_EXPORT_ZIP_STALE_GUARD_STATUS = (
    "PASS - helper overwrote the stable review zip from the freshly refreshed "
    "worktree review folder after START_HERE was written for this Source HEAD."
)
USER_BRANCH_PLAN_REVIEW_FILE = "USER_BRANCH_PLAN_REVIEW.md"


PRIVATE_REVIEW_BUNDLE_PATH_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "owner-private-path",
        re.compile(
            r"(?:^|[\\/ _.-])(?:owner[-_ ]?private|private[-_ ]?owner|"
            r"nexus[-_ ]?desktop[-_ ]?ai[-_ ]?owner|owner[-_ ]?edition)(?:[\\/ _.-]|$)",
            re.IGNORECASE,
        ),
    ),
    (
        "dev-private-path",
        re.compile(
            r"(?:^|[\\/ _.-])(?:private[-_ ]?dev|dev[-_ ]?private|"
            r"private[-_ ]?orin|dev[-_ ]?orin)(?:[\\/ _.-]|$)",
            re.IGNORECASE,
        ),
    ),
    (
        "private-artifact-path",
        re.compile(
            r"(?:^|[\\/ _.-])private[-_ ]?"
            r"(?:prompt|memory|log|eval|screenshot|automation|handoff|artifact|model|capability)"
            r"(?:[\\/ _.-]|$)",
            re.IGNORECASE,
        ),
    ),
    (
        "private-repo-path",
        re.compile(
            r"(?:^|[\\/ _.-])(?:owner|dev)[-_ ]?repo(?:[\\/ _.-]|$)|"
            r"(?:^|[\\/])\.codex[\\/](?:worktrees|private|owner|dev)(?:[\\/]|$)",
            re.IGNORECASE,
        ),
    ),
)


def _desktop_path() -> Path:
    home = Path.home()
    onedrive_desktop = home / "OneDrive" / "Desktop"
    if onedrive_desktop.is_dir():
        return onedrive_desktop
    return home / "Desktop"


def _sanitize_folder_name(name: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*]+', "_", name).strip(" .")
    sanitized = re.sub(r"\s+", " ", sanitized)
    if not sanitized:
        raise ValueError("Review bundle folder name is empty after sanitization")
    return sanitized


def _worktree_label(explicit_label: str | None) -> str:
    if explicit_label:
        return _sanitize_folder_name(explicit_label)
    return _sanitize_folder_name(ROOT.name)


def _safe_target(desktop: Path, review_root_name: str, worktree_label: str) -> tuple[Path, Path]:
    review_root = (desktop / _sanitize_folder_name(review_root_name)).resolve()
    target = (review_root / _sanitize_folder_name(worktree_label)).resolve()
    desktop_resolved = desktop.resolve()
    if review_root == desktop_resolved or desktop_resolved not in review_root.parents:
        raise ValueError(f"Refusing to write review root outside Desktop: {review_root}")
    if target == review_root or review_root not in target.parents:
        raise ValueError(f"Refusing to write outside Desktop: {target}")
    return review_root, target


def _clear_readonly(function, path: str, _exc_info) -> None:
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
    function(path)


def _clear_target(target: Path) -> None:
    try:
        shutil.rmtree(target, onexc=_clear_readonly)
    except TypeError:
        shutil.rmtree(target, onerror=_clear_readonly)


def _flat_copy_name(relative_file: str) -> str:
    normalized = Path(relative_file).as_posix().replace("\\", "/")
    return normalized.replace("/", "__")


def _copy_names(files: list[str]) -> list[str]:
    basename_counts = Counter(Path(file_name).name for file_name in files)
    names: list[str] = []
    used: set[str] = set()
    for file_name in files:
        basename = Path(file_name).name
        copy_name = basename if basename_counts[basename] == 1 else _flat_copy_name(file_name)
        if copy_name in used:
            copy_name = _flat_copy_name(file_name)
        if copy_name in used:
            raise ValueError(f"Review bundle filename collision: {copy_name}")
        used.add(copy_name)
        names.append(copy_name)
    return names


def _copy_file(relative_file: str, target: Path, copy_name: str) -> tuple[str, str]:
    source = (ROOT / relative_file).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Review source file not found: {relative_file}")
    if ROOT.resolve() not in source.parents:
        raise ValueError(f"Review source file is outside repo: {relative_file}")

    destination = target / copy_name
    shutil.copy2(source, destination)
    return source.relative_to(ROOT).as_posix(), destination.relative_to(target).as_posix()


def _git_output(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "UNKNOWN"


def _markdown_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- None recorded."]
    return [f"- {item}" for item in items]


def _bundle_files(target: Path) -> set[Path]:
    return {path for path in target.rglob("*") if path.is_file()}


def _export_zip_path(review_root: Path, label: str) -> Path:
    return (review_root / f"{_sanitize_folder_name(label)}.zip").resolve()


def _write_export_zip(target: Path, export_zip: Path) -> None:
    if target in export_zip.parents or export_zip == target:
        raise ValueError(f"Refusing to write review zip inside bundle folder: {export_zip}")
    export_zip.parent.mkdir(parents=True, exist_ok=True)
    if export_zip.exists():
        export_zip.unlink()
    with zipfile.ZipFile(export_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(_bundle_files(target)):
            archive.write(path, path.relative_to(target).as_posix())


def _validate_export_zip(export_zip: Path, source_head: str) -> None:
    with zipfile.ZipFile(export_zip, "r") as archive:
        try:
            start_here = archive.read("START_HERE.md").decode("utf-8")
        except KeyError as exc:
            raise ValueError(f"Review export zip is missing START_HERE.md: {export_zip}") from exc
        try:
            archive.read(USER_BRANCH_PLAN_REVIEW_FILE)
        except KeyError as exc:
            raise ValueError(
                f"Review export zip is missing {USER_BRANCH_PLAN_REVIEW_FILE}: {export_zip}"
            ) from exc
    if f"Source HEAD: `{source_head}`" not in start_here:
        raise ValueError(
            "Review export zip stale-head guard failed: START_HERE Source HEAD "
            f"does not match {source_head}"
        )
    if "Review Export Zip Stale Guard: PASS" not in start_here:
        raise ValueError("Review export zip is missing stale-guard proof in START_HERE.md")


def _is_repo_relative_review_path(path: str) -> bool:
    if not isinstance(path, str) or not path:
        return False
    if "://" in path or path.startswith("~"):
        return False
    if Path(path).is_absolute() or PurePosixPath(path).is_absolute():
        return False
    windows_path = PureWindowsPath(path)
    if windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return False
    parts = set(PurePosixPath(path).parts) | set(windows_path.parts)
    return ".." not in parts


def _public_review_bundle_file_list_failures(paths: list[str]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        normalized = path.replace("\\", "/")
        if not _is_repo_relative_review_path(path):
            failures.append(f"{path}: public review bundle file list must stay repo-relative")
        for reason, pattern in PRIVATE_REVIEW_BUNDLE_PATH_PATTERNS:
            if pattern.search(normalized):
                failures.append(f"{path}: public review bundle file list matched {reason}")
    return failures


def _write_user_branch_plan_review(
    *,
    target: Path,
    title: str,
    review_purpose: str,
    source_branch: str,
    source_head: str,
    upstream: str,
    origin_main: str,
    exact_user_decision: str,
    pending_user_decisions: list[str],
    copied: list[tuple[str, str]],
) -> Path:
    active_branch_files = [
        copied_rel
        for source_rel, copied_rel in copied
        if "active_overlay_recording_runtime_foundation" in source_rel
    ]
    rollback_context_files = [
        copied_rel
        for source_rel, copied_rel in copied
        if "recording_profile_runtime_foundation" in source_rel
    ]
    source_truth_files = [
        copied_rel
        for source_rel, copied_rel in copied
        if source_rel
        in {
            "Docs/feature_backlog.md",
            "Docs/prebeta_roadmap.md",
            "Docs/branch_records/index.md",
            "Docs/branch_plans/README.md",
            "Docs/family_visions/FAM-006_monitoring_and_hud.md",
        }
    ]
    lines = [
        f"# USER Branch Plan Review - {title}",
        "",
        "## Purpose",
        "",
        review_purpose,
        "",
        "This file is the standalone USER-facing branch-plan review entrypoint. "
        "It is generated in addition to START_HERE.md so the review packet has "
        "an obvious file for USER branch-plan review instead of relying on a "
        "section buried inside the copied source-truth plan.",
        "",
        "## Current Branch State",
        "",
        f"- Source Branch: `{source_branch}`",
        f"- Source HEAD: `{source_head}`",
        f"- Upstream: `{upstream}`",
        f"- origin/main: `{origin_main}`",
        f"- Source Repo: `{ROOT}`",
        "",
        "## Review Focus",
        "",
        "- Confirm the active branch authority and branch plan match the intended carrier.",
        "- Confirm historical/rollback files are present only as context.",
        "- Confirm pending USER decisions are explicit before implementation.",
        "- Confirm the exact next approval text matches the intended next phase.",
        "",
        "## Active Branch Plan Files",
        "",
        *_markdown_lines(active_branch_files),
        "",
        "## Historical / Rollback Context Files",
        "",
        *_markdown_lines(rollback_context_files),
        "",
        "## Supporting Source-Truth Files",
        "",
        *_markdown_lines(source_truth_files),
        "",
        "## Pending USER Decisions",
        "",
        *_markdown_lines(pending_user_decisions),
        "",
        "## Exact USER Decision Supported",
        "",
        exact_user_decision,
        "",
    ]
    review_path = target / USER_BRANCH_PLAN_REVIEW_FILE
    review_path.write_text("\n".join(lines), encoding="utf-8")
    return review_path.resolve()


def build_bundle(
    *,
    review_root_name: str,
    worktree_label: str | None,
    allow_custom_review_path: bool,
    custom_review_path_reason: str | None,
    files: list[str],
    title: str,
    clear: bool,
    review_purpose: str,
    validation_summary: str,
    review_order: list[str],
    exact_user_decision: str,
    pending_user_decisions: list[str],
    expected_file_count: int | None,
) -> tuple[Path, Path]:
    custom_root = review_root_name != DEFAULT_REVIEW_ROOT_NAME
    custom_label = worktree_label is not None
    if (custom_root or custom_label) and not allow_custom_review_path:
        raise ValueError(
            "Custom review paths are blocked by default. Use the stable "
            "Nexus USER Review/<worktree-label> destination, or pass "
            "--allow-custom-review-path with --custom-review-path-reason."
        )
    if allow_custom_review_path and not custom_review_path_reason:
        raise ValueError("--custom-review-path-reason is required with --allow-custom-review-path")

    desktop = _desktop_path()
    label = _worktree_label(worktree_label)
    review_root, target = _safe_target(desktop, review_root_name, label)
    if clear and target.exists():
        _clear_target(target)
    target.mkdir(parents=True, exist_ok=True)

    copied = [
        _copy_file(file_name, target, copy_name)
        for file_name, copy_name in zip(files, _copy_names(files), strict=True)
    ]
    copied_count = len(copied)
    copied_targets = {(target / copied_rel).resolve() for _source_rel, copied_rel in copied}
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
    export_zip = _export_zip_path(review_root, label)
    user_review_file = _write_user_branch_plan_review(
        target=target,
        title=title,
        review_purpose=review_purpose,
        source_branch=source_branch,
        source_head=source_head,
        upstream=upstream,
        origin_main=origin_main,
        exact_user_decision=exact_user_decision,
        pending_user_decisions=pending_user_decisions,
        copied=copied,
    )
    if allow_custom_review_path:
        custom_review_path_waiver = "Granted"
        custom_review_path_reason_value = custom_review_path_reason or "Not recorded"
    else:
        custom_review_path_waiver = CUSTOM_REVIEW_PATH_NONE
        custom_review_path_reason_value = "Not applicable"
    start_here = (target / "START_HERE.md").resolve()
    actual_bundle_files = _bundle_files(target) | {start_here, user_review_file}
    extra_bundle_files = sorted(
        path.relative_to(target).as_posix()
        for path in actual_bundle_files
        if path not in copied_targets and path != start_here
    )
    bundle_file_count = len(actual_bundle_files)
    leak_prevention_failures = _public_review_bundle_file_list_failures(
        [
            *(source_rel for source_rel, _copied_rel in copied),
            *(copied_rel for _source_rel, copied_rel in copied),
            *extra_bundle_files,
        ]
    )
    if leak_prevention_failures:
        raise ValueError(
            "Public review bundle leak-prevention failed:\n"
            + "\n".join(f"- {failure}" for failure in leak_prevention_failures)
        )

    readme_lines: list[str] = [
        f"# {title}",
        "",
        "## Review Packet",
        "",
        f"Review Purpose: {review_purpose}",
        f"Source Repo: `{ROOT}`",
        f"Review Root: `{review_root}`",
        f"Worktree Review Folder: `{target}`",
        f"Worktree Label: `{label}`",
        f"Custom Review Path Waiver: {custom_review_path_waiver}",
        f"Custom Review Path Reason: {custom_review_path_reason_value}",
        f"Source Branch: `{source_branch}`",
        f"Source HEAD: `{source_head}`",
        f"Upstream: `{upstream}`",
        f"origin/main: `{origin_main}`",
        f"Review Export Zip: `{export_zip}`",
        f"Review Export Zip Source HEAD: `{source_head}`",
        f"Review Export Zip Stale Guard: {REVIEW_EXPORT_ZIP_STALE_GUARD_STATUS}",
        f"Bundle Created: {created_at}",
        f"Bundle File Count: {bundle_file_count}",
        f"Expected File Count: {expected_count}",
        f"Copied File Count: {copied_count}",
        f"Extra Bundle File Count: {len(extra_bundle_files)}",
        f"Public Review Bundle Leak-Prevention: {PUBLIC_REVIEW_BUNDLE_LEAK_PREVENTION_STATUS}",
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
        "## Extra Bundle Files",
        "",
        *_markdown_lines(extra_bundle_files),
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
    _write_export_zip(target, export_zip)
    _validate_export_zip(export_zip, source_head)
    return target, export_zip


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review-root-name",
        default=DEFAULT_REVIEW_ROOT_NAME,
        help="Stable Desktop review root folder name. Custom values require --allow-custom-review-path.",
    )
    parser.add_argument(
        "--worktree-label",
        help="Optional worktree child folder label. Defaults to the current worktree folder name.",
    )
    parser.add_argument(
        "--folder-name",
        help=(
            "Legacy alias for --worktree-label. New governance expects a stable "
            "review root with an auto-derived worktree label. Requires "
            "--allow-custom-review-path."
        ),
    )
    parser.add_argument(
        "--allow-custom-review-path",
        action="store_true",
        help="USER-approved waiver allowing a custom review root or worktree label.",
    )
    parser.add_argument(
        "--custom-review-path-reason",
        help="Required reason when --allow-custom-review-path is used.",
    )
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

    target, export_zip = build_bundle(
        review_root_name=args.review_root_name,
        worktree_label=args.worktree_label or args.folder_name,
        allow_custom_review_path=args.allow_custom_review_path,
        custom_review_path_reason=args.custom_review_path_reason,
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
    print(f"Review export zip: {export_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
