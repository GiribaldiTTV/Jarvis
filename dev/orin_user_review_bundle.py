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
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Mapping


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

WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES: tuple[str, ...] = (
    "START_HERE.md",
    "USER_REVIEW_FOLDER_AND_FILE_DIGEST.md",
    "GOVERNANCE_REQUIRED_FILES_SCAN.md",
    "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
    "BRANCH_VISION_VALIDATION_CHECKLIST.md",
)

WORKSTREAM_ENTRY_PACKET_DECISION_FILES: tuple[str, ...] = (
    "START_HERE.md",
    "USER_REVIEW_FOLDER_AND_FILE_DIGEST.md",
    "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
    "BRANCH_VISION_VALIDATION_CHECKLIST.md",
)

DECISION_STATUS_IMPLEMENTATION_READY = "implementation-ready"
DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW = "workstream-entry-final-review"
DECISION_STATUS_REPAIR_REVALIDATION = "repair-revalidation"
DECISION_STATUS_UNKNOWN = "unknown"


@dataclass(frozen=True)
class WorkstreamEntryPacketDecisionPathResult:
    """Machine-readable result for Workstream Entry packet decision-path checks."""

    status: str
    failures: list[str]

    @property
    def implementation_ready(self) -> bool:
        return self.status == DECISION_STATUS_IMPLEMENTATION_READY and not self.failures

    @property
    def blocks_implementation(self) -> bool:
        return self.status in {
            DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW,
            DECISION_STATUS_REPAIR_REVALIDATION,
            DECISION_STATUS_UNKNOWN,
        }


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


def _packet_text_status(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).casefold()
    repair_markers = (
        "branch readiness stage 2",
        "repair/revalidation",
        "repair before workstream implementation",
        "returning to branch readiness",
    )
    if any(marker in normalized for marker in repair_markers):
        return DECISION_STATUS_REPAIR_REVALIDATION

    final_review_markers = (
        "workstream entry final decision review",
        "final workstream entry decision",
    )
    if any(marker in normalized for marker in final_review_markers):
        return DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW

    implementation_markers = (
        "approve bounded workstream implementation",
        "approve workstream implementation",
        "workstream implementation approval",
    )
    blocking_markers = (
        "implementation remains blocked",
        "implementation not yet authorized",
        "does not authorize workstream implementation",
        "blocks workstream implementation",
        "before workstream implementation",
        "pending user decision",
    )
    if any(marker in normalized for marker in implementation_markers) and not any(
        marker in normalized for marker in blocking_markers
    ):
        return DECISION_STATUS_IMPLEMENTATION_READY

    return DECISION_STATUS_UNKNOWN


def _field_present(text: str, field_name: str) -> bool:
    pattern = re.compile(rf"^{re.escape(field_name)}\s*:", re.IGNORECASE | re.MULTILINE)
    return bool(pattern.search(text))


def _validate_workstream_entry_packet_decision_path(
    packet_files: Mapping[str, str],
    *,
    expected_branch: str,
    expected_head: str,
    expected_origin_main: str,
    require_implementation_ready: bool = False,
) -> WorkstreamEntryPacketDecisionPathResult:
    failures: list[str] = []
    for required_file in WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES:
        if required_file not in packet_files:
            failures.append(f"{required_file}: required Workstream Entry packet file is missing")

    for file_name in WORKSTREAM_ENTRY_PACKET_DECISION_FILES:
        text = packet_files.get(file_name)
        if text is None:
            continue
        if expected_branch not in text:
            failures.append(f"{file_name}: expected branch {expected_branch!r} not found")
        if expected_head not in text:
            failures.append(f"{file_name}: expected HEAD {expected_head!r} not found")
        if expected_origin_main not in text:
            failures.append(f"{file_name}: expected origin/main {expected_origin_main!r} not found")

    start_here = packet_files.get("START_HERE.md", "")
    if not _field_present(start_here, "Exact USER Decision This Bundle Supports"):
        failures.append("START_HERE.md: Exact USER Decision This Bundle Supports field is missing")
    workstream_digest = packet_files.get("WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md", "")
    if "Exact USER Decision" not in workstream_digest:
        failures.append("WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md: Exact USER Decision field is missing")

    file_statuses: dict[str, str] = {}
    for file_name in WORKSTREAM_ENTRY_PACKET_DECISION_FILES:
        text = packet_files.get(file_name)
        if text is None:
            continue
        status = _packet_text_status(text)
        file_statuses[file_name] = status
        if status == DECISION_STATUS_UNKNOWN:
            failures.append(f"{file_name}: next legal phase / implementation posture is not machine-readable")

    distinct_statuses = {status for status in file_statuses.values() if status != DECISION_STATUS_UNKNOWN}
    if len(distinct_statuses) > 1:
        joined = ", ".join(f"{file_name}={status}" for file_name, status in sorted(file_statuses.items()))
        failures.append(f"Workstream Entry packet decision-path conflict: {joined}")

    if len(distinct_statuses) == 1:
        status = next(iter(distinct_statuses))
    else:
        status = DECISION_STATUS_UNKNOWN

    if require_implementation_ready and status != DECISION_STATUS_IMPLEMENTATION_READY:
        joined = ", ".join(f"{file_name}={status_value}" for file_name, status_value in sorted(file_statuses.items()))
        failures.append(
            "Workstream Entry packet blocks implementation approval: "
            f"status={status}; files={joined}"
        )

    return WorkstreamEntryPacketDecisionPathResult(status=status, failures=failures)


def validate_workstream_entry_packet_folder(
    packet_dir: Path,
    *,
    expected_branch: str,
    expected_head: str,
    expected_origin_main: str,
    require_implementation_ready: bool = False,
) -> WorkstreamEntryPacketDecisionPathResult:
    packet_files: dict[str, str] = {}
    for file_name in WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES:
        path = packet_dir / file_name
        if path.is_file():
            packet_files[file_name] = path.read_text(encoding="utf-8")
    return _validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch=expected_branch,
        expected_head=expected_head,
        expected_origin_main=expected_origin_main,
        require_implementation_ready=require_implementation_ready,
    )


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
    if allow_custom_review_path:
        custom_review_path_waiver = "Granted"
        custom_review_path_reason_value = custom_review_path_reason or "Not recorded"
    else:
        custom_review_path_waiver = CUSTOM_REVIEW_PATH_NONE
        custom_review_path_reason_value = "Not applicable"
    start_here = (target / "START_HERE.md").resolve()
    actual_bundle_files = _bundle_files(target) | {start_here}
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
    parser.add_argument("--review-purpose", help="Why USER is reviewing this bundle.")
    parser.add_argument("--validation-summary", help="Validation proof or status supporting the review bundle.")
    parser.add_argument(
        "--review-order",
        action="append",
        default=[],
        help="Repeatable suggested review step for START_HERE.md.",
    )
    parser.add_argument("--exact-user-decision", help="Exact USER decision this bundle is meant to support.")
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
    parser.add_argument(
        "--validate-workstream-entry-packet",
        type=Path,
        help="Validate an existing Workstream Entry Desktop packet decision path.",
    )
    parser.add_argument("--expected-branch", help="Expected source branch for Workstream Entry packet validation.")
    parser.add_argument("--expected-head", help="Expected source HEAD for Workstream Entry packet validation.")
    parser.add_argument("--expected-origin-main", help="Expected origin/main baseline for Workstream Entry packet validation.")
    parser.add_argument(
        "--require-implementation-ready",
        action="store_true",
        help="Fail if the packet is branch-correct but still blocks Workstream implementation approval.",
    )
    parser.add_argument("files", nargs="*", help="Repo-relative files to copy into the Desktop review bundle.")
    args = parser.parse_args()

    if args.validate_workstream_entry_packet:
        for field_name in ("expected_branch", "expected_head", "expected_origin_main"):
            if getattr(args, field_name) is None:
                parser.error(f"--{field_name.replace('_', '-')} is required with --validate-workstream-entry-packet")
        result = validate_workstream_entry_packet_folder(
            args.validate_workstream_entry_packet,
            expected_branch=args.expected_branch,
            expected_head=args.expected_head,
            expected_origin_main=args.expected_origin_main,
            require_implementation_ready=args.require_implementation_ready,
        )
        if result.failures:
            print("FAIL: Workstream Entry packet decision-path validation failed.")
            print(f"Packet status: {result.status}")
            for failure in result.failures:
                print(f"- {failure}")
            return 1
        if result.blocks_implementation:
            print("PASS: Workstream Entry packet is self-consistent and blocks implementation approval.")
            print(f"Packet status: {result.status}")
        else:
            print("PASS: Workstream Entry packet is self-consistent and implementation-ready.")
            print(f"Packet status: {result.status}")
        return 0

    for required_arg in ("review_purpose", "validation_summary", "exact_user_decision"):
        if getattr(args, required_arg) is None:
            parser.error(f"--{required_arg.replace('_', '-')} is required when building a review bundle")
    if not args.files:
        parser.error("at least one repo-relative file is required when building a review bundle")

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
