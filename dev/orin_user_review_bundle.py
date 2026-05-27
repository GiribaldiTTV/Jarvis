# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing Desktop review bundle from selected repo files.

This helper copies review files to a stable worktree-labeled folder on the
user's Desktop so USER review does not depend on manually browsing the
worktree. It never edits repo files.
"""

from __future__ import annotations

import argparse
import hashlib
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
    "PASS - helper moved prior matching zip artifacts and the stable worktree "
    "review folder to governed quarantine, confirmed the recreated folder was "
    "empty before copying, wrote START_HERE for this Source HEAD, and atomically "
    "replaced the stable review zip from that refreshed folder, then checked "
    "active branch record/plan identity against START_HERE."
)
USER_BRANCH_PLAN_REVIEW_FILE = "USER_BRANCH_PLAN_REVIEW.md"
UPLOAD_THIS_ZIP_FILE = "UPLOAD_THIS_ZIP.md"
FAM006_ACTIVE_OVERLAY_RECORDING_IMPLEMENTATION_BRANCH = (
    "feature/fam-006-active-overlay-recording-runtime-implementation"
)
FAM006_ACTIVE_OVERLAY_RECORDING_FOUNDATION_BRANCH = (
    "feature/fam-006-active-overlay-recording-runtime-foundation"
)
FAM006_ACTIVE_OVERLAY_RECORDING_IMPLEMENTATION_PACKET_FILES = frozenset(
    {
        "Docs__branch_records__feature_fam_006_active_overlay_recording_runtime_implementation.md",
        "Docs__branch_plans__feature_fam_006_active_overlay_recording_runtime_implementation.md",
    }
)

ACTIVE_IMPLEMENTATION_CARRIER_STALE_PHRASES = (
    "this branch is not the runtime implementation carrier",
    "not the runtime implementation carrier",
    "deferred to future user-approved implementation carrier",
    "future runtime implementation carrier",
    "future user-approved carrier",
    "future user-approved implementation carrier",
    "later runtime carrier",
    "workstream is skipped",
    "planning/governance branch",
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


def _target_entry_count(target: Path) -> int:
    if not target.exists():
        return 0
    return sum(1 for _path in target.rglob("*"))


@dataclass(frozen=True)
class QuarantineResult:
    source: Path
    destination: Path
    entry_count: int


def _quarantine_root(review_root: Path, label: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return (
        review_root
        / "_stale_review_artifacts"
        / _sanitize_folder_name(label)
        / f"{timestamp}_{os.getpid()}"
    ).resolve()


def _move_to_quarantine(path: Path, quarantine_root: Path, review_root: Path) -> QuarantineResult:
    resolved = path.resolve()
    resolved_review_root = review_root.resolve()
    if resolved != resolved_review_root and resolved_review_root not in resolved.parents:
        raise ValueError(f"Refusing to quarantine review artifact outside review root: {resolved}")
    destination = (quarantine_root / resolved.name).resolve()
    if quarantine_root not in destination.parents:
        raise ValueError(f"Refusing to quarantine outside quarantine root: {destination}")
    if destination.exists():
        raise ValueError(f"Refusing to overwrite quarantined review artifact: {destination}")
    quarantine_root.mkdir(parents=True, exist_ok=True)
    entry_count = _target_entry_count(resolved) if resolved.is_dir() else 1
    shutil.move(str(resolved), str(destination))
    if resolved.exists():
        raise ValueError(f"Review artifact still exists after quarantine move: {resolved}")
    return QuarantineResult(source=resolved, destination=destination, entry_count=entry_count)


def _quarantine_target(target: Path, quarantine_root: Path, review_root: Path) -> QuarantineResult | None:
    if not target.exists():
        return None
    return _move_to_quarantine(target, quarantine_root, review_root)


def _assert_target_empty(target: Path) -> None:
    existing = list(target.iterdir())
    if existing:
        preview = ", ".join(path.name for path in existing[:5])
        raise ValueError(
            "Review bundle folder pre-copy clean check failed: "
            f"{target} still contains {len(existing)} entries"
            + (f" ({preview})" if preview else "")
        )


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


def _branch_slug(branch: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", branch).strip("_").lower()
    if not slug:
        raise ValueError("Cannot derive branch slug from empty source branch")
    return slug


def _active_branch_packet_names(source_branch: str) -> tuple[str, str]:
    slug = _branch_slug(source_branch)
    return (
        f"Docs__branch_records__{slug}.md",
        f"Docs__branch_plans__{slug}.md",
    )


def _active_branch_source_paths(source_branch: str) -> tuple[Path, Path]:
    slug = _branch_slug(source_branch)
    return (
        ROOT / "Docs" / "branch_records" / f"{slug}.md",
        ROOT / "Docs" / "branch_plans" / f"{slug}.md",
    )


def _markdown_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- None recorded."]
    return [f"- {item}" for item in items]


def _extract_marker_from_text(text: str, marker: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(marker)}\s*(.+)$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1].strip()
    return value or None


def _source_marker(relative_file: str, marker: str) -> str | None:
    source = (ROOT / relative_file).resolve()
    if not source.is_file() or ROOT.resolve() not in source.parents:
        return None
    return _extract_marker_from_text(source.read_text(encoding="utf-8"), marker)


def _bundle_files(target: Path) -> set[Path]:
    return {path for path in target.rglob("*") if path.is_file()}


def _export_zip_path(review_root: Path, label: str) -> Path:
    return (review_root / f"{_sanitize_folder_name(label)}.zip").resolve()


def _quarantine_review_exports(
    review_root: Path, label: str, quarantine_root: Path
) -> list[QuarantineResult]:
    """Move previous zip artifacts for this review label before regenerating."""
    sanitized_label = _sanitize_folder_name(label)
    quarantined: list[QuarantineResult] = []
    for path in review_root.glob(f"{sanitized_label}*.zip*"):
        resolved = path.resolve()
        if resolved.parent != review_root.resolve():
            raise ValueError(f"Refusing to quarantine review export outside review root: {resolved}")
        if resolved.is_file():
            quarantined.append(_move_to_quarantine(resolved, quarantine_root, review_root))
    return quarantined


def _write_export_zip(target: Path, export_zip: Path) -> None:
    if target in export_zip.parents or export_zip == target:
        raise ValueError(f"Refusing to write review zip inside bundle folder: {export_zip}")
    export_zip.parent.mkdir(parents=True, exist_ok=True)
    temp_zip = export_zip.with_name(f".{export_zip.name}.{os.getpid()}.tmp")
    if temp_zip.exists():
        temp_zip.unlink()
    try:
        with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(_bundle_files(target)):
                archive.write(path, path.relative_to(target).as_posix())
        temp_zip.replace(export_zip)
    except Exception:
        if temp_zip.exists():
            temp_zip.unlink()
        raise


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _validate_export_zip(
    export_zip: Path,
    *,
    source_branch: str,
    source_head: str,
    origin_main: str,
    merge_base: str,
    expected_entries: set[str],
) -> None:
    active_record_name, active_plan_name = _active_branch_packet_names(source_branch)
    active_record_source, active_plan_source = _active_branch_source_paths(source_branch)
    with zipfile.ZipFile(export_zip, "r") as archive:
        entries = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
        try:
            start_here = archive.read("START_HERE.md").decode("utf-8")
        except KeyError as exc:
            raise ValueError(f"Review export zip is missing START_HERE.md: {export_zip}") from exc
        try:
            user_review = archive.read(USER_BRANCH_PLAN_REVIEW_FILE).decode("utf-8")
        except KeyError as exc:
            raise ValueError(
                f"Review export zip is missing {USER_BRANCH_PLAN_REVIEW_FILE}: {export_zip}"
            ) from exc
        active_record = (
            archive.read(active_record_name).decode("utf-8") if active_record_name in entries else None
        )
        active_plan = (
            archive.read(active_plan_name).decode("utf-8") if active_plan_name in entries else None
        )
    if entries != expected_entries:
        missing = sorted(expected_entries - entries)
        extra = sorted(entries - expected_entries)
        raise ValueError(
            "Review export zip file-list guard failed: "
            f"missing={missing or 'none'} extra={extra or 'none'}"
        )
    if UPLOAD_THIS_ZIP_FILE in entries:
        raise ValueError(
            "Review export zip simplified stable-model guard failed: "
            f"{UPLOAD_THIS_ZIP_FILE} must be absent"
        )
    if f"Source Branch: `{source_branch}`" not in start_here:
        raise ValueError(
            "Review export zip branch guard failed: START_HERE Source Branch "
            f"does not match {source_branch}"
        )
    if f"Source HEAD: `{source_head}`" not in start_here:
        raise ValueError(
            "Review export zip stale-head guard failed: START_HERE Source HEAD "
            f"does not match {source_head}"
        )
    if f"origin/main: `{origin_main}`" not in start_here:
        raise ValueError(
            "Review export zip origin/main guard failed: START_HERE origin/main "
            f"does not match {origin_main}"
        )
    if f"Merge Base: `{merge_base}`" not in start_here:
        raise ValueError(
            "Review export zip merge-base guard failed: START_HERE Merge Base "
            f"does not match {merge_base}"
        )
    if f"Review Export Zip Source HEAD: `{source_head}`" not in start_here:
        raise ValueError(
            "Review export zip stale-head guard failed: Review Export Zip Source HEAD "
            f"does not match {source_head}"
        )
    if "Review Folder Empty Before Copy: PASS" not in start_here:
        raise ValueError(
            "Review export zip folder freshness guard failed: START_HERE does not "
            "prove the review folder was empty before copying fresh files"
        )
    if "Review Cleanup Mode: `Governed quarantine`" not in start_here:
        raise ValueError(
            "Review export zip cleanup guard failed: START_HERE does not prove "
            "USER-visible governed quarantine cleanup"
        )
    if "Review Cleanup Quarantine Root:" not in start_here:
        raise ValueError(
            "Review export zip cleanup guard failed: START_HERE is missing the "
            "cleanup quarantine root"
        )
    if "Review Folder Pre-Clean Removed Count:" not in start_here:
        raise ValueError(
            "Review export zip folder freshness guard failed: START_HERE is missing "
            "folder pre-clean removed count"
        )
    if "Review Export Pre-Clean Removed Count:" not in start_here:
        raise ValueError(
            "Review export zip stale-export guard failed: START_HERE is missing "
            "zip pre-clean removed count"
        )
    if active_record_source.is_file() and active_record_name not in entries:
        raise ValueError(
            "Review export zip active-authority guard failed: exported ZIP is missing "
            f"the active branch record {active_record_name}"
        )
    if active_plan_source.is_file() and active_plan_name not in entries:
        raise ValueError(
            "Review export zip active-plan guard failed: exported ZIP is missing "
            f"the active branch plan {active_plan_name}"
        )
    for file_name, text in (
        (active_record_name, active_record),
        (active_plan_name, active_plan),
    ):
        if text is None:
            continue
        if source_branch not in text:
            raise ValueError(
                "Review export zip active-carrier guard failed: "
                f"{file_name} does not mention active source branch {source_branch}"
            )
        if "runtime_implementation" in file_name or "runtime implementation carrier" in text.casefold():
            normalized_text = text.casefold()
            stale_phrases = [
                phrase
                for phrase in ACTIVE_IMPLEMENTATION_CARRIER_STALE_PHRASES
                if phrase in normalized_text
            ]
            if stale_phrases:
                raise ValueError(
                    "Review export zip active-carrier guard failed: "
                    f"{file_name} contains stale carrier wording: {stale_phrases}"
                )
    if active_record:
        last_reconciled_origin = _extract_marker_from_text(active_record, "Last Reconciled origin/main:")
        if last_reconciled_origin and last_reconciled_origin != origin_main:
            raise ValueError(
                "Review export zip active-authority guard failed: "
                "Last Reconciled origin/main in active branch record does not match START_HERE "
                f"origin/main {origin_main}"
            )
        last_reconciled_merge_base = _extract_marker_from_text(
            active_record, "Last Reconciled Merge Base:"
        )
        if last_reconciled_merge_base and last_reconciled_merge_base != merge_base:
            raise ValueError(
                "Review export zip active-authority guard failed: "
                "Last Reconciled Merge Base in active branch record does not match START_HERE "
                f"Merge Base {merge_base}"
            )
    if active_plan:
        reconciliation_status = _extract_marker_from_text(
            active_plan, "Current-Main Reconciliation Status:"
        )
        if (
            reconciliation_status
            and "reconciled" in reconciliation_status.casefold()
            and origin_main not in reconciliation_status
        ):
            raise ValueError(
                "Review export zip active-plan guard failed: "
                "Current-Main Reconciliation Status in active branch plan does not match "
                f"START_HERE origin/main {origin_main}"
            )
    if source_branch == FAM006_ACTIVE_OVERLAY_RECORDING_IMPLEMENTATION_BRANCH:
        missing_impl_files = sorted(
            FAM006_ACTIVE_OVERLAY_RECORDING_IMPLEMENTATION_PACKET_FILES - entries
        )
        if missing_impl_files:
            raise ValueError(
                "Review export zip FAM-006 implementation-carrier guard failed: "
                f"missing={missing_impl_files}"
            )
        stale_foundation_metadata = (
            f"Source Branch: `{FAM006_ACTIVE_OVERLAY_RECORDING_FOUNDATION_BRANCH}`"
            in start_here
        )
        if stale_foundation_metadata:
            raise ValueError(
                "Review export zip FAM-006 implementation-carrier guard failed: "
                "START_HERE still presents the released foundation carrier as active metadata"
            )
    if "Review Export Zip Stale Guard: PASS" not in start_here:
        raise ValueError("Review export zip is missing stale-guard proof in START_HERE.md")
    if "USER Review Packet Finding: PASS" not in start_here:
        raise ValueError("Review export zip is missing USER Review Packet Finding proof")
    for required_heading in (
        "## Contract Status",
        "## Contract Version / Revision",
        "## Plain-English Branch Summary",
        "## What Will I Actually See, And Where Will I See It?",
        "## End-State Vision",
        "## Visual / Functional Walkthrough",
        "## Surface Map",
        "## Implementation Options",
        "## Recommended Direction",
        "## Why This Fits The Nexus Vision",
        "## USER Design Direction Decision",
        "## USER Decisions Needed",
        "## USER Response",
        "## Codex Response Digest",
        "## Implementation Constraints Created By USER Response",
        "## USER Rejected / Deferred Ideas",
        "## Vision Delta / Source-Truth Impact",
        "## Contract Change Log",
        "## Current Branch Scope",
        "## Future-Gated Scope",
        "## Implementation Staging Notes",
        "## Workstream Entry Result",
        "## Contract Completion Checklist",
    ):
        if required_heading not in user_review:
            raise ValueError(
                f"Review export zip USER_BRANCH_PLAN_REVIEW.md is missing {required_heading}"
            )
    contract_status = _section(user_review, "Contract Status").strip().casefold()
    if not any(
        contract_status.startswith(prefix)
        for prefix in (
            "draft",
            "pending user response",
            "pending codex digest",
            "pending user confirmation",
            "complete",
            "waived by user",
        )
    ):
        raise ValueError(
            "Review export zip USER_BRANCH_PLAN_REVIEW.md has invalid Contract Status"
        )
    exact_decision = _section(user_review, "Exact USER Decision Supported").casefold()
    if contract_status.startswith(
        ("draft", "pending user response", "pending codex digest", "pending user confirmation")
    ) and (
        "approve bounded slc" in exact_decision
        or "approve workstream implementation" in exact_decision
        or "implementation approval" in exact_decision
    ):
        raise ValueError(
            "Review export zip cannot request implementation approval while "
            "USER_BRANCH_PLAN_REVIEW.md Contract Status is blocking"
        )


def _section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    start = text.find("\n", start)
    if start < 0:
        return ""
    next_heading = text.find("\n## ", start + 1)
    if next_heading < 0:
        return text[start:].strip()
    return text[start:next_heading].strip()


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
    is_active_overlay_recording = any(
        "active_overlay_recording_runtime_foundation" in source_rel
        or "active_overlay_recording_runtime_implementation" in source_rel
        for source_rel, _copied_rel in copied
    )
    has_implementation_carrier_files = any(
        "active_overlay_recording_runtime_implementation" in source_rel
        for source_rel, _copied_rel in copied
    )
    active_branch_files = [
        copied_rel
        for source_rel, copied_rel in copied
        if (
            "active_overlay_recording_runtime_implementation" in source_rel
            if has_implementation_carrier_files
            else "active_overlay_recording_runtime_foundation" in source_rel
        )
    ]
    rollback_context_files = [
        copied_rel
        for source_rel, copied_rel in copied
        if "recording_profile_runtime_foundation" in source_rel
        or (
            has_implementation_carrier_files
            and "active_overlay_recording_runtime_foundation" in source_rel
        )
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
    if is_active_overlay_recording:
        active_plan_source = next(
            (
                source_rel
                for source_rel, _copied_rel in copied
                if source_rel.endswith(
                    "Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_implementation.md"
                )
                or source_rel.endswith(
                    "Docs/branch_plans/feature_fam_006_active_overlay_recording_runtime_foundation.md"
                )
            ),
            None,
        )
        accepted_user_response = (
            _source_marker(active_plan_source, "USER Review Response:") if active_plan_source else None
        )
        codex_response_digest = (
            _source_marker(active_plan_source, "Codex Response Digest:") if active_plan_source else None
        )
        workstream_entry_result = (
            _source_marker(active_plan_source, "Workstream Entry Result:") if active_plan_source else None
        )
        contract_status = (
            _source_marker(active_plan_source, "Contract Status:") if active_plan_source else None
        ) or "Pending USER Confirmation - Codex revised this review into the closed-loop USER Branch Plan Contract; USER must confirm the revised contract or explicitly waive it before implementation."
        contract_version = (
            _source_marker(active_plan_source, "Contract Version / Revision:") if active_plan_source else None
        ) or "v3 - USER recording product-model revision."
        what_user_sees = (
            "HUD Overlay card: a compact recording launcher and target/status preview inside the "
            "existing card, showing the active Overlay Profile name, a Recording Target / Active "
            "Recording Target label, a concise target summary, future-gated status, and a future "
            "Open Recording Control action. Recording Control window: a later compact standalone "
            "normal Windows/NDAI window for target summary and future controls/settings, with "
            "secondary settings windows when details would make the main control bulky. Native Log "
            "Loader: a separate future graph/log viewer, not the recording control surface."
        )
        why_nexus = (
            "This fits Nexus because it keeps recording intuitive, avoids a confusing second profile "
            "system, keeps the HUD lightweight, gives the user a compact normal OS window for ongoing "
            "control, keeps graph/log viewing separate from recording control, and protects future "
            "log quality by preserving per-overlay effective polling policy as architecture before "
            "recording execution exists."
        )
        design_ballot = [
            "Accept Codex recommendation.",
            "Accept with changes.",
            "Choose another option.",
            "Request hybrid option.",
            "Reject and ask for more options.",
            "Pause / unclear.",
        ]
        response_structure = [
            "Decision.",
            "Required changes.",
            "Must-have behavior.",
            "Must-not-do boundaries.",
            "Future-gated ideas.",
            "General response.",
        ]
        digest_structure = [
            "USER intent summary.",
            "Accepted USER decisions.",
            "Rejected or deferred USER ideas.",
            "Implementation constraints created from USER response.",
            "Source-truth updates required.",
            "Review packet updates required.",
            "Open questions.",
            "Contract Status after digest.",
            "Next USER decision needed.",
        ]
        implementation_constraints = [
            "This planning/governance branch must not implement SLC-051 or any runtime/user-facing recording work.",
            "Future SLC-051 remains state/proof-only and must not add recording execution, file writing, or real Start/Stop behavior.",
            "Recording target derives only from active Overlay Profile membership and must cover null, empty, selected, switched, deleted/stale, duplicate/stale-ID, and high-volume membership states.",
            "No separate Recording Profile system or recording-specific sensor chooser is admitted.",
            "Start/Stop behavior remains future-gated until an approved seam admits execution; any later placeholder must be clearly disabled or future-gated.",
            "Native Log Loader remains future planning input unless USER separately approves durable source-truth mutation or implementation.",
            "Per-overlay effective polling policy remains future planning/source-truth constraint and SLC-051 must not design against it.",
            "Overlay Profile, Overlay Display, Monitor Group, Dashboard, Manage Monitors, and Sensor Command Center behavior must remain preserved.",
        ]
        rejected_deferred = [
            "Rejected for this branch direction: separate profile-loaded Recording Profile system.",
            "Rejected as the desired long-term polling model: duplicate CPU FAST / CPU SLOW Monitor Groups solely to vary polling cadence.",
            "Deferred: recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup/deletion, per-overlay effective polling policy implementation, and durable Native Log Loader source-truth mutation.",
        ]
        source_truth_impact = [
            "Family vision: record per-overlay effective polling policy as a future FAM-006 planning constraint and keep Native Log Loader as future graph/log viewer input only.",
            "Active branch plan and branch record: record the accepted v3/v4 planning-governance posture, USER vision digest, implementation constraints, Workstream skip, and PR Readiness Stage 1 as the next legal phase.",
            "Backlog/roadmap: record planning-governance PR-readiness posture rather than runtime implementation posture.",
            "Review packet: refresh whenever contract status, response, digest, constraints, source-truth impact, or HEAD changes.",
            "Workstream seam order: target model remains future implementation staging, not current branch work.",
        ]
        contract_change_log = [
            "v1 - USER-facing Branch Plan Review packet introduced with end-state/options sections.",
            "v2 - Hardened into USER Branch Plan Contract with closed-loop response/digest, implementation constraints, source-truth impact, confirmation loop, and waiver semantics.",
            "v3 - Digested USER recording product-model feedback: HUD Overlay launcher/target preview, standalone Recording Control window, Native Log Loader separation, future per-overlay effective polling policy, and target-model-first SLC-051.",
            "v4 - USER accepted the plan and redirected this branch to planning/governance PR Readiness with Workstream skipped and runtime implementation deferred to a future USER-approved carrier.",
        ]
        completion_checklist = [
            "Contract Status is Complete or Waived by USER.",
            "USER response is present, attached, or explicitly waived.",
            "Codex Response Digest is present.",
            "Implementation Constraints Created By USER Response are present.",
            "Vision Delta / Source-Truth Impact is resolved.",
            "USER Rejected / Deferred Ideas are recorded.",
            "Contract Change Log is current.",
            "Packet metadata matches current branch, HEAD, origin/main, and ZIP source HEAD.",
            "Workstream Entry Result is present only after response/digest or waiver.",
            "Exact implementation approval text cites completed or waived contract status.",
        ]
        plain_english_summary = (
            "This branch is setting up the corrected FAM-006 recording direction: "
            "recording should be driven by the currently active Overlay Profile, "
            "not by loading a separate Recording Profile. The intended future "
            "feature uses the HUD Overlay card as the launcher and target/status "
            "preview, a compact standalone Recording Control window as the control "
            "surface, and a separate future Native Log Loader for graph/log viewing."
        )
        end_state_vision = (
            "When this branch's admitted package is complete, the HUD Overlay card should make "
            "recording feel tied to the overlay the user already chose. The user should understand "
            "which active Overlay Profile members are the intended recording target, launch a compact "
            "standalone Recording Control window from the HUD Overlay card, and keep graph/log viewing "
            "separate in a future Native Log Loader. Actual file writing and real Start/Stop remain "
            "separately approved."
        )
        walkthrough = [
            "Dashboard / HUD Overlay card: the recording area should sit inside the existing HUD Overlay card as launcher and target/status preview before Start/Stop execution is admitted.",
            "Active Overlay Profile membership: the selected overlay's active members become the future recording target; no separate Recording Profile selector is introduced.",
            "Target visibility: SLC-051 should prove null, empty, selected, switched, deleted/stale, duplicate/stale-ID, and high-volume target states before visible controls depend on that model.",
            "Recording Control window: later seams plan a small independent NDAI/Windows window that can be moved, minimized, taskbar-restored, and kept open outside Dashboard child-window lifetime.",
            "Secondary settings/details windows: bulky or advanced settings should open outside the compact control surface when USER later approves them.",
            "Output contract and Native Log Loader: later seams plan graph/plot-ready files, while Native Log Loader remains a separate future viewer unless USER separately admits it.",
        ]
        surface_map = [
            "HUD Overlay card: launcher and active target/status preview surface.",
            "Recording Control window: compact standalone control surface for future target summary, Start/Stop, and path/status controls after approval.",
            "Dashboard: hosts the HUD Overlay card and must not regress existing Dashboard behavior.",
            "Manage Monitors / Sensor Command Center: remain monitor/source management owners; recording target proof must not mutate their state.",
            "Overlay Profile / Overlay Display: remain display and membership owners; recording reads active membership without taking ownership.",
            "Monitor Group: reusable sensor/source group; future per-overlay effective polling policy should avoid duplicate FAST/SLOW group workarounds.",
            "Files/output: future graph/plot-ready recording contract only after explicit approval.",
            "Native Log Loader: future separate graph/log viewer for completed recordings.",
            "Tray/export/provider/theme/FAM-007: future-gated surfaces outside this branch unless USER separately approves.",
        ]
        implementation_options = [
            "Option A - Target model proof first: prove the active-overlay recording target model before visible controls depend on it. Pros: safest foundation; Cons: least visible at first; Risk: low. Codex recommends this first.",
            "Option B - Target preview in HUD card: show active target/status preview in the HUD Overlay card after or alongside safe target proof. Pros: strong user clarity; Cons: needs visual proof; Risk: low to medium.",
            "Option C - Standalone Recording Control window shell first: build the compact OS-level window before target proof is complete. Pros: validates window feel early; Cons: weaker target-model foundation; Risk: medium.",
            "Option D - Live Start/Stop planning later: plan real controls only after recording execution and file writing are admitted. Pros: avoids fake execution; Cons: later visible payoff; Risk: low when deferred.",
        ]
        recommended_direction = (
            "Codex recommends Option A first: establish the active Overlay Profile target model, "
            "then use later seams for HUD target preview, the standalone Recording Control window, "
            "output-file contract, and live/user proof. For future recording execution, Codex "
            "recommends snapshot-at-recording-start by default unless USER revises it, while SLC-051 "
            "proves the live current active-overlay target because no recording is occurring yet."
        )
        current_scope = [
            "Preserve the accepted active-overlay recording end-state as maintained source truth.",
            "Record that active Overlay Profile membership is the source of truth for future recording targets.",
            "Keep future SLC-051 target-model-first and avoid blocking future per-overlay effective polling policy.",
            "Confirm this branch does not change Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, Overlay Display, Monitor Group, or recording runtime behavior.",
            "Proceed only to PR Readiness Stage 1 after USER approval; runtime implementation belongs to a later USER-approved carrier.",
        ]
        future_scope = [
            "Recording execution and file writing remain blocked until an approved seam admits them.",
            "Tray recording controls, export/share/import, provider/model work, broad theme/skin work, FAM-007 work, old branch cleanup, PR, merge, release, and issue mutation remain separate USER decisions.",
            "Native Log Loader is early USER input only unless USER separately approves durable source-truth mutation.",
            "Per-overlay effective polling policy is future FAM-006 architecture unless USER separately admits implementation.",
        ]
        slc_package_plan = [
            "Implementation staging note, not the USER decision surface: Codex uses SLC-051 through SLC-055 internally to sequence the accepted end-state safely.",
            "Target model comes first because every later UI/control/output behavior depends on knowing what would be recorded.",
            "HUD target preview, Recording Control window, output contract, and validation/live proof follow as staged implementation only after the end-state and boundaries are accepted.",
        ]
        user_decisions = [
            "Does USER approve PR Readiness Stage 1 analysis for this planning/governance branch?",
            "Does USER agree that no runtime/user-facing recording work, SLC-051 implementation, Workstream implementation, H1, LV1, or UTS is claimed by this branch?",
            "Does USER agree that the accepted active-overlay product contract is preserved for a future implementation carrier?",
            "Does USER want a revision before PR Readiness, or should PR Readiness inspect this no-runtime closeout?",
        ]
        if source_branch == FAM006_ACTIVE_OVERLAY_RECORDING_IMPLEMENTATION_BRANCH:
            implementation_constraints[0] = (
                "This implementation carrier must not implement SLC-051 or any "
                "runtime/user-facing recording work during Stage 2."
            )
            source_truth_impact = [
                "Family vision: keep per-overlay effective polling policy as a future FAM-006 planning constraint and keep Native Log Loader as future graph/log viewer input only.",
                "Active branch plan and branch record: record the accepted v4 planning contract as imported starting implementation truth for this fresh carrier.",
                "Backlog/roadmap: record implementation-carrier Stage 2 setup and Workstream Entry pending posture.",
                "Review packet: refresh whenever contract status, response, digest, constraints, source-truth impact, or HEAD changes.",
                "Workstream seam order: target model remains the first expected implementation seam, pending Workstream Entry analysis and USER implementation approval.",
            ]
            contract_change_log = [
                "v1 - USER-facing Branch Plan Review packet introduced with end-state/options sections.",
                "v2 - Hardened into USER Branch Plan Contract with closed-loop response/digest, implementation constraints, source-truth impact, confirmation loop, and waiver semantics.",
                "v3 - Digested USER recording product-model feedback: HUD Overlay launcher/target preview, standalone Recording Control window, Native Log Loader separation, future per-overlay effective polling policy, and target-model-first SLC-051.",
                "v4 - USER accepted the plan and redirected the released foundation carrier to planning/governance PR Readiness with Workstream skipped.",
                "Implementation-carrier v1 - Imported the accepted v4 contract onto the fresh current-main runtime implementation branch.",
            ]
            current_scope = [
                "Admit the fresh runtime implementation carrier and preserve the accepted active-overlay recording end-state as starting implementation truth.",
                "Record that active Overlay Profile membership is the source of truth for future recording targets.",
                "Keep SLC-051 target-model-first and avoid blocking future per-overlay effective polling policy.",
                "Confirm Stage 2 does not change Dashboard, Manage Monitors, Sensor Command Center, Overlay Profile, Overlay Display, Monitor Group, or recording runtime behavior.",
                "Proceed only to Workstream Entry analysis after USER approval; runtime implementation requires a later bounded implementation approval.",
            ]
            user_decisions = [
                "Does USER approve Workstream Entry analysis for this implementation carrier?",
                "Does USER agree that Stage 2 claims no runtime/user-facing recording work, SLC-051 implementation, Workstream implementation, H1, LV1, or UTS?",
                "Does USER agree that the accepted active-overlay product contract is imported as starting implementation truth for this carrier?",
                "Does USER want a revision before Workstream Entry, or should Workstream Entry inspect this carrier and return the first bounded implementation approval packet?",
            ]
    else:
        accepted_user_response = None
        codex_response_digest = None
        workstream_entry_result = None
        contract_status = "Pending USER Response - USER must accept, revise, reject, request more options, or waive this contract before implementation."
        contract_version = "v1 - Generated USER Branch Plan Contract."
        what_user_sees = "USER should see the feature's planned surfaces, behavior, options, boundaries, and proof path before implementation begins."
        why_nexus = "The recommendation should explain how the branch aligns with the project vision, keeps scope bounded, and preserves user-facing clarity."
        design_ballot = [
            "Accept Codex recommendation.",
            "Accept with changes.",
            "Choose another option.",
            "Request hybrid option.",
            "Reject and ask for more options.",
            "Pause / unclear.",
        ]
        response_structure = [
            "Decision.",
            "Required changes.",
            "Must-have behavior.",
            "Must-not-do boundaries.",
            "Future-gated ideas.",
            "General response.",
        ]
        digest_structure = [
            "USER intent summary.",
            "Accepted USER decisions.",
            "Rejected or deferred USER ideas.",
            "Implementation constraints created from USER response.",
            "Source-truth updates required.",
            "Review packet updates required.",
            "Open questions.",
            "Contract Status after digest.",
            "Next USER decision needed.",
        ]
        implementation_constraints = ["Pending USER response or explicit waiver."]
        rejected_deferred = ["Pending USER response or explicit waiver."]
        source_truth_impact = ["Pending USER response or explicit waiver."]
        contract_change_log = ["v1 - Generated USER Branch Plan Contract."]
        completion_checklist = [
            "Contract Status is Complete or Waived by USER.",
            "USER response is present, attached, or explicitly waived.",
            "Codex Response Digest is present.",
            "Implementation Constraints Created By USER Response are present.",
            "Vision Delta / Source-Truth Impact is resolved.",
            "USER Rejected / Deferred Ideas are recorded.",
            "Contract Change Log is current.",
            "Packet metadata matches current branch, HEAD, origin/main, and ZIP source HEAD.",
            "Workstream Entry Result is present only after response/digest or waiver.",
            "Exact implementation approval text cites completed or waived contract status.",
        ]
        plain_english_summary = (
            "This branch-plan review summarizes the branch's intended product, "
            "runtime, source-truth, and validation direction before Workstream "
            "Entry performs deeper implementation planning."
        )
        end_state_vision = (
            "When the branch is complete, USER should understand what visible/runtime behavior "
            "will exist, which surfaces are affected, and which future-gated items remain outside "
            "the branch before implementation begins."
        )
        walkthrough = [
            "Review the active branch plan to understand the intended user-facing result.",
            "Review the branch authority record to confirm identity and legal next phase.",
            "Review copied source-truth files to confirm active/historical routing and future boundaries.",
        ]
        surface_map = [
            "Active branch plan and authority record.",
            "Relevant family vision, backlog, roadmap, validators, and copied review files.",
        ]
        implementation_options = [
            "Option A - Accept Codex's recommended end-state and keep later implementation staging future-gated. Pros: fastest bounded path; Cons: less redesign; Risk: low when source truth is coherent.",
            "Option B - Revise the end-state before implementation. Pros: better USER fit; Cons: adds planning repair work; Risk: low to medium.",
            "Option C - Waive unresolved end-state questions explicitly. Pros: unblocks implementation; Cons: records less USER design input; Risk: medium.",
        ]
        recommended_direction = (
            "Codex recommends accepting the branch plan only when the user-facing outcome, "
            "surface map, options, proof path, and pending boundaries are understandable enough "
            "for USER to decide whether implementation should begin."
        )
        current_scope = [
            "Confirm the branch outcome and admitted package.",
            "Confirm affected surfaces, validators, proof expectations, and next legal phase.",
        ]
        future_scope = [
            "Any item not explicitly admitted by the active branch plan remains future-gated.",
        ]
        slc_package_plan = [
            "Implementation staging must support the accepted end-state; seam/slice details are background execution scaffolding, not the primary USER decision surface.",
        ]
        user_decisions = [
            "Does USER accept the branch goal and end-state direction?",
            "Does USER want to revise any user-facing behavior, layout, workflow, or future-gated boundary before implementation?",
            "Does USER waive any unanswered design question, or should implementation remain blocked until it is answered?",
        ]
    lines = [
        f"# USER Branch Plan Review - {title}",
        "",
        "## Contract Status",
        "",
        contract_status,
        "",
        "## Contract Version / Revision",
        "",
        contract_version,
        "",
        "## Plain-English Branch Summary",
        "",
        plain_english_summary,
        "",
        "This file is a required user-facing product/design planning gate. It should help USER answer: Do I actually like what Codex is about to build?",
        "",
        "## What Will I Actually See, And Where Will I See It?",
        "",
        what_user_sees,
        "",
        "## End-State Vision",
        "",
        end_state_vision,
        "",
        "## Visual / Functional Walkthrough",
        "",
        *_markdown_lines(walkthrough),
        "",
        "## Surface Map",
        "",
        *_markdown_lines(surface_map),
        "",
        "## Implementation Options",
        "",
        *_markdown_lines(implementation_options),
        "",
        "## Recommended Direction",
        "",
        recommended_direction,
        "",
        "## Why This Fits The Nexus Vision",
        "",
        why_nexus,
        "",
        "## USER Design Direction Decision",
        "",
        "Choose one of these paths, then add any notes or changes you want:",
        "",
        *_markdown_lines(design_ballot),
        "",
        "## USER Decisions Needed",
        "",
        "USER may answer in order or respond generally. Useful feedback includes visual direction, workflow changes, window behavior, output-file expectations, deferred scope, or anything that would make the branch plan feel wrong before implementation planning begins.",
        "",
        *_markdown_lines(user_decisions),
        "",
        "## USER Response",
        "",
        accepted_user_response
        or "Status: Pending USER Response - Workstream implementation remains blocked until USER answers, revises, rejects, accepts, or explicitly waives this contract.",
        "",
        "Required USER Response structure:",
        "",
        *_markdown_lines(response_structure),
        "",
        "## Codex Response Digest",
        "",
        codex_response_digest
        or "Status: Pending USER Response - Codex has not yet digested USER answers for this contract. Workstream implementation requires a later digest or an explicit USER waiver.",
        "",
        "Required Codex Response Digest structure:",
        "",
        *_markdown_lines(digest_structure),
        "",
        "## Implementation Constraints Created By USER Response",
        "",
        *_markdown_lines(implementation_constraints),
        "",
        "## USER Rejected / Deferred Ideas",
        "",
        *_markdown_lines(rejected_deferred),
        "",
        "## Vision Delta / Source-Truth Impact",
        "",
        *_markdown_lines(source_truth_impact),
        "",
        "## Contract Change Log",
        "",
        *_markdown_lines(contract_change_log),
        "",
        "## Current Branch Scope",
        "",
        *_markdown_lines(current_scope),
        "",
        "## Future-Gated Scope",
        "",
        *_markdown_lines(future_scope),
        "",
        "## Implementation Staging Notes",
        "",
        *_markdown_lines(slc_package_plan),
        "",
        "## Current Branch State",
        "",
        f"- Source Branch: `{source_branch}`",
        f"- Source HEAD: `{source_head}`",
        f"- Upstream: `{upstream}`",
        f"- origin/main: `{origin_main}`",
        f"- Source Repo: `{ROOT}`",
        "",
        "## Workstream Entry Result",
        "",
        workstream_entry_result
        or "Status: Pending USER Response - first seam, affected files, validators, proof requirements, USER-facing proof, and exact implementation approval text must be returned only after USER response/digest or explicit waiver.",
        "",
        "## Contract Completion Checklist",
        "",
        *_markdown_lines(completion_checklist),
        "",
        "## Codex Recommendations And Implementation Options",
        "",
        "This compatibility section is retained for older packet validators. See Implementation Options and Recommended Direction above.",
        "",
        *_markdown_lines(implementation_options),
        "",
        "## USER Design Review Questions",
        "",
        "This compatibility section is retained for older packet validators. See USER Decisions Needed above.",
        "",
        *_markdown_lines(user_decisions),
        "",
        "## Appendix - Legacy Validator Compatibility",
        "",
        "Legacy compatibility sections are retained only for older validators and should not replace the contract sections above.",
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


def _packet_text_status(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).casefold()
    implementation_markers = (
        "approve bounded workstream implementation",
        "approve workstream implementation",
        "workstream implementation approval",
    )
    blocking_markers = (
        "implementation remains blocked",
        "implementation not yet authorized",
        "does not approve bounded workstream implementation",
        "does not approve workstream implementation",
        "do not approve bounded workstream implementation",
        "do not approve workstream implementation",
        "not approve bounded workstream implementation",
        "not approve workstream implementation",
        "does not authorize workstream implementation",
        "blocks workstream implementation",
        "before workstream implementation",
        "workstream implementation remains pending",
        "workstream implementation remains a pending user decision",
        "pending user decision: workstream implementation",
    )
    if any(marker in normalized for marker in implementation_markers) and not any(
        marker in normalized for marker in blocking_markers
    ):
        return DECISION_STATUS_IMPLEMENTATION_READY

    repair_markers = (
        "branch readiness stage 2 repair/revalidation",
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
    review_root.mkdir(parents=True, exist_ok=True)
    quarantine_root = _quarantine_root(review_root, label)
    quarantined_exports = _quarantine_review_exports(review_root, label, quarantine_root)
    quarantined_target = _quarantine_target(target, quarantine_root, review_root)
    removed_folder_entries = quarantined_target.entry_count if quarantined_target else 0
    folder_quarantine_path = (
        str(quarantined_target.destination) if quarantined_target else "None - folder absent"
    )
    export_quarantine_paths = (
        ", ".join(str(result.destination) for result in quarantined_exports)
        if quarantined_exports
        else "None - no prior matching zip artifacts"
    )
    target.mkdir(parents=True, exist_ok=True)
    _assert_target_empty(target)
    folder_empty_before_copy = "PASS"

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
    merge_base = _git_output("merge-base", "HEAD", "origin/main")
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
    actual_bundle_files = _bundle_files(target) | {
        start_here,
        user_review_file,
    }
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
        f"Merge Base: `{merge_base}`",
        f"Review Export Zip: `{export_zip}`",
        f"Review Export Zip Source HEAD: `{source_head}`",
        "Review Export Zip SHA256: `Reported by helper stdout after final stable zip replacement`",
        "Review Cleanup Mode: `Governed quarantine`",
        f"Review Cleanup Quarantine Root: `{quarantine_root}`",
        f"Review Folder Quarantine Path: `{folder_quarantine_path}`",
        f"Review Export Quarantine Paths: `{export_quarantine_paths}`",
        f"Review Folder Pre-Clean Removed Count: {removed_folder_entries}",
        f"Review Folder Empty Before Copy: {folder_empty_before_copy}",
        f"Review Export Pre-Clean Removed Count: {len(quarantined_exports)}",
        f"Review Export Zip Stale Guard: {REVIEW_EXPORT_ZIP_STALE_GUARD_STATUS}",
        (
            "USER Review Packet Finding: PASS - helper generated and validated "
            f"`START_HERE.md`, `{USER_BRANCH_PLAN_REVIEW_FILE}`, and exported zip "
            f"`{export_zip}` from refreshed Desktop folder `{target}`; Source HEAD "
            f"`{source_head}` and Review Export Zip Source HEAD `{source_head}` match "
            "the current branch HEAD, and the packet is loaded/digestible for USER review."
        ),
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
    expected_zip_entries = {
        path.relative_to(target).as_posix() for path in _bundle_files(target)
    }
    _write_export_zip(target, export_zip)
    _validate_export_zip(
        export_zip,
        source_branch=source_branch,
        source_head=source_head,
        origin_main=origin_main,
        merge_base=merge_base,
        expected_entries=expected_zip_entries,
    )
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
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Legacy compatibility flag; the helper always clears the Desktop bundle folder before copying.",
    )
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
    print(f"Review export zip SHA256: {_sha256_file(export_zip)}")
    print(
        "USER Review Packet Finding: PASS - START_HERE.md, "
        f"{USER_BRANCH_PLAN_REVIEW_FILE}, and exported zip were generated and "
        "validated against current Source HEAD."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
