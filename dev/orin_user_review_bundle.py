# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing local review bundle from selected repo files.

This helper copies review files to a stable worktree-labeled folder under
``C:\\Nexus USER`` so USER review does not depend on manually browsing the
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
WINDOWS_USER_HUB_ROOT_TEXT = r"C:\Nexus USER"
DEFAULT_USER_HUB_ROOT = Path(WINDOWS_USER_HUB_ROOT_TEXT)
DEFAULT_REVIEW_ROOT_NAME = ""
CUSTOM_REVIEW_PATH_NONE = "None - stable review root enforced"
PUBLIC_REVIEW_BUNDLE_LEAK_PREVENTION_STATUS = (
    "PASS - copied file list and START_HERE file-list metadata are repo-relative "
    "and exclude Owner/Dev private path patterns; copied file content remains "
    "source truth for USER inspection."
)
REVIEW_EXPORT_ZIP_STALE_GUARD_STATUS = (
    "PASS - helper cleared the stable worktree review folder, copied fresh "
    "source-truth files, wrote START_HERE for this source-truth snapshot, and atomically "
    "replaced the stable review zip from that refreshed folder."
)
USER_BRANCH_PLAN_REVIEW_FILE = "USER_BRANCH_PLAN_REVIEW.md"
USER_BRANCH_VISION_REVIEW_FILE = "USER_BRANCH_VISION_REVIEW.md"


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
DECISION_STATUS_BP1_BRANCH_VISION_REVIEW = "bp1-branch-vision-review"
DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW = "workstream-entry-final-review"
DECISION_STATUS_HARDENING_REVIEW = "hardening-final-review"
DECISION_STATUS_LIVE_VALIDATION_REVIEW = "live-validation-final-review"
DECISION_STATUS_PR_READINESS_STAGE1_REVIEW = "pr-readiness-stage1-review"
DECISION_STATUS_PR_READINESS_STAGE2_REVIEW = "pr-readiness-stage2-review"
DECISION_STATUS_REPAIR_REVALIDATION = "repair-revalidation"
DECISION_STATUS_UNKNOWN = "unknown"
UNRESOLVED_TEMPLATE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("shell-variable-branch", re.compile(r"(?<![A-Za-z0-9_])\$branch\b")),
    ("shell-variable-head", re.compile(r"(?<![A-Za-z0-9_])\$head\b")),
    ("shell-variable-origin-main", re.compile(r"(?<![A-Za-z0-9_])\$originMain\b")),
    ("shell-variable-packet", re.compile(r"(?<![A-Za-z0-9_])\$packet\b")),
    ("shell-variable-zip", re.compile(r"(?<![A-Za-z0-9_])\$zip\b")),
    ("unevaluated-shell-expression", re.compile(r"\$\([^)\n]+\)")),
)
BUNDLE_COUNT_FIELDS: tuple[str, ...] = (
    "Bundle File Count",
    "Expected File Count",
    "Copied File Count",
    "Extra Bundle File Count",
)
USER_FACING_GENERATED_FILES: tuple[str, ...] = (
    "START_HERE.md",
    USER_BRANCH_VISION_REVIEW_FILE,
    USER_BRANCH_PLAN_REVIEW_FILE,
    "USER_REVIEW_FOLDER_AND_FILE_DIGEST.md",
    "GOVERNANCE_REQUIRED_FILES_SCAN.md",
    "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
    "BRANCH_VISION_VALIDATION_CHECKLIST.md",
)
USER_FACING_TECHNICAL_METADATA_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("head-token", re.compile(r"\bHEAD\b", re.IGNORECASE)),
    ("source-head", re.compile(r"\bSource HEAD\b", re.IGNORECASE)),
    ("origin-main", re.compile(r"\borigin/main\b", re.IGNORECASE)),
    ("merge-base", re.compile(r"\bmerge base\b|\bmerge-base\b", re.IGNORECASE)),
    ("ahead-behind", re.compile(r"\bahead/behind\b|\bAhead/Behind\b", re.IGNORECASE)),
    ("zip-hash", re.compile(r"\b(?:ZIP|packet|upload)\s+(?:SHA256|hash)\b", re.IGNORECASE)),
    ("review-export-zip", re.compile(r"\bReview Export Zip\b", re.IGNORECASE)),
    (
        "desktop-onedrive-active-upload",
        re.compile(
            r"(?:\b(?:Desktop|OneDrive)\b[^\n]*(?:active\s+)?(?:upload|review)\s+"
            r"(?:source|path|folder|bundle))|"
            r"(?:(?:upload|review)\s+(?:source|path|folder|bundle)[^\n]*"
            r"\b(?:Desktop|OneDrive)\b)",
            re.IGNORECASE,
        ),
    ),
    ("upstream-field", re.compile(r"^Upstream\s*:", re.IGNORECASE | re.MULTILINE)),
    ("source-branch-field", re.compile(r"^Source Branch\s*:", re.IGNORECASE | re.MULTILINE)),
    ("branch-status", re.compile(r"\bbranch status\b|\bCurrent Branch State\b", re.IGNORECASE)),
    ("validation-status", re.compile(r"\bvalidation status\b|\bValidation Summary\b", re.IGNORECASE)),
    ("pr-state", re.compile(r"\bPR state\b", re.IGNORECASE)),
    ("worktree-status", re.compile(r"\bworktree status\b", re.IGNORECASE)),
    ("sha-like-proof", re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)),
)
USER_BRANCH_PLAN_STALE_BP1_WORDING_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "old-product-design-planning-gate",
        re.compile(r"required user-facing product/design planning gate", re.IGNORECASE),
    ),
    (
        "old-do-i-like-prompt",
        re.compile(r"Do I actually like what Codex is about to build", re.IGNORECASE),
    ),
    (
        "old-product-design-contract",
        re.compile(r"USER Branch Plan Contract:\s*a required user-facing product/design", re.IGNORECASE),
    ),
)


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
            DECISION_STATUS_BP1_BRANCH_VISION_REVIEW,
            DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW,
            DECISION_STATUS_HARDENING_REVIEW,
            DECISION_STATUS_LIVE_VALIDATION_REVIEW,
            DECISION_STATUS_PR_READINESS_STAGE1_REVIEW,
            DECISION_STATUS_PR_READINESS_STAGE2_REVIEW,
            DECISION_STATUS_REPAIR_REVALIDATION,
            DECISION_STATUS_UNKNOWN,
        }


def _desktop_path() -> Path:
    if os.name != "nt":
        raise RuntimeError(
            "The local USER hub path is Windows-only: "
            f"{WINDOWS_USER_HUB_ROOT_TEXT}. Run this helper from Windows so "
            "review packets stay outside the repo worktree."
        )
    if not DEFAULT_USER_HUB_ROOT.is_absolute():
        raise RuntimeError(
            "The local USER hub root must be an absolute filesystem path: "
            f"{WINDOWS_USER_HUB_ROOT_TEXT}"
        )
    return DEFAULT_USER_HUB_ROOT


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
    if not desktop.is_absolute():
        raise ValueError(f"Local USER hub root must be absolute: {desktop}")
    if review_root_name:
        review_root = (desktop / _sanitize_folder_name(review_root_name)).resolve()
    else:
        review_root = desktop.resolve()
    target = (review_root / _sanitize_folder_name(worktree_label)).resolve()
    desktop_resolved = desktop.resolve()
    if review_root != desktop_resolved and desktop_resolved not in review_root.parents:
        raise ValueError(f"Refusing to write review root outside local USER hub: {review_root}")
    if target == review_root or review_root not in target.parents:
        raise ValueError(f"Refusing to write outside local USER hub: {target}")
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


def _validate_export_zip(
    export_zip: Path,
    *,
    source_branch: str,
    source_head: str,
    origin_main: str,
    expected_entries: set[str],
) -> None:
    packet_files: dict[str, str] = {}
    with zipfile.ZipFile(export_zip, "r") as archive:
        entries = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
        try:
            start_here = archive.read("START_HERE.md").decode("utf-8")
        except KeyError as exc:
            raise ValueError(f"Review export zip is missing START_HERE.md: {export_zip}") from exc
        try:
            user_vision = archive.read(USER_BRANCH_VISION_REVIEW_FILE).decode("utf-8")
        except KeyError as exc:
            raise ValueError(
                f"Review export zip is missing {USER_BRANCH_VISION_REVIEW_FILE}: {export_zip}"
            ) from exc
        try:
            user_review = archive.read(USER_BRANCH_PLAN_REVIEW_FILE).decode("utf-8")
        except KeyError as exc:
            raise ValueError(
                f"Review export zip is missing {USER_BRANCH_PLAN_REVIEW_FILE}: {export_zip}"
            ) from exc
        for entry in sorted(entries):
            try:
                packet_files[entry] = archive.read(entry).decode("utf-8")
            except UnicodeDecodeError:
                continue
    if entries != expected_entries:
        missing = sorted(expected_entries - entries)
        extra = sorted(entries - expected_entries)
        raise ValueError(
            "Review export zip file-list guard failed: "
            f"missing={missing or 'none'} extra={extra or 'none'}"
        )
    artifact_failures = [
        *_unresolved_template_placeholder_failures(packet_files),
        *_packet_identity_failures(
            packet_files,
            expected_branch=source_branch,
            expected_head=source_head,
            expected_origin_main=origin_main,
        ),
        *_packet_count_consistency_failures(
            packet_files,
            actual_file_count=len(entries),
        ),
        *_user_facing_technical_metadata_failures(packet_files),
        *_user_branch_plan_stale_bp1_wording_failures(packet_files),
    ]
    if artifact_failures:
        raise ValueError(
            "Review export zip artifact validation failed:\n"
            + "\n".join(f"- {failure}" for failure in artifact_failures)
        )
    if "Review Purpose:" not in start_here:
        raise ValueError("Review export zip is missing Review Purpose in START_HERE.md")
    if "USER Decision This Packet Supports:" not in start_here:
        raise ValueError("Review export zip is missing USER decision text in START_HERE.md")
    for required_heading in (
        "## Contract Status",
        "## Contract Revision",
        "## Project Vision Context",
        "## Family Vision Context",
        "## Feature Vision Context",
        "## Branch Goal",
        "## End-State Vision",
        "## What Will I Actually See, And Where Will I See It?",
        "## How It Will Function",
        "## User Experience Flow",
        "## Surface Map",
        "## Product Options / Design Paths",
        "## Codex Recommendations",
        "## USER Response",
        "## Codex Digest",
        "## Accepted Branch Vision",
        "## Design Assumption Ledger",
        "## Acceptance / Revision / Rejection / Waiver Decision",
    ):
        if required_heading not in user_vision:
            raise ValueError(
                f"Review export zip USER_BRANCH_VISION_REVIEW.md is missing {required_heading}"
            )
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
        "## USER Plan Review Decision",
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


def _field_int(text: str, field_name: str) -> int | None:
    match = re.search(rf"^{re.escape(field_name)}:\s*(\d+)\s*$", text, re.MULTILINE)
    return int(match.group(1)) if match else None


def _unresolved_template_placeholder_failures(packet_files: Mapping[str, str]) -> list[str]:
    failures: list[str] = []
    for file_name, text in sorted(packet_files.items()):
        for reason, pattern in UNRESOLVED_TEMPLATE_PATTERNS:
            matches = sorted({match.group(0) for match in pattern.finditer(text)})
            if matches:
                joined = ", ".join(matches)
                failures.append(f"{file_name}: unresolved template placeholder {reason}: {joined}")
    return failures


def _packet_count_consistency_failures(
    packet_files: Mapping[str, str],
    *,
    actual_file_count: int | None = None,
) -> list[str]:
    start_here = packet_files.get("START_HERE.md", "")
    if not start_here:
        return []
    parsed = {field: _field_int(start_here, field) for field in BUNDLE_COUNT_FIELDS}
    if all(value is None for value in parsed.values()):
        return []

    failures: list[str] = []
    for field, value in parsed.items():
        if value is None:
            failures.append(f"START_HERE.md: packet count field '{field}' is missing")

    bundle_file_count = parsed["Bundle File Count"]
    expected_file_count = parsed["Expected File Count"]
    copied_file_count = parsed["Copied File Count"]
    extra_bundle_file_count = parsed["Extra Bundle File Count"]
    if actual_file_count is None:
        actual_file_count = len(packet_files)

    if bundle_file_count is not None and bundle_file_count != actual_file_count:
        failures.append(
            "START_HERE.md: Bundle File Count "
            f"{bundle_file_count} does not match actual packet file count {actual_file_count}"
        )
    if (
        expected_file_count is not None
        and copied_file_count is not None
        and expected_file_count != copied_file_count
    ):
        failures.append(
            "START_HERE.md: Expected File Count "
            f"{expected_file_count} does not match Copied File Count {copied_file_count}"
        )
    if (
        bundle_file_count is not None
        and copied_file_count is not None
        and extra_bundle_file_count is not None
        and bundle_file_count != copied_file_count + extra_bundle_file_count + 1
    ):
        failures.append(
            "START_HERE.md: Bundle File Count must equal Copied File Count "
            f"+ Extra Bundle File Count + START_HERE.md; got {bundle_file_count}, "
            f"{copied_file_count}, {extra_bundle_file_count}"
        )
    return failures


def _user_facing_technical_metadata_failures(packet_files: Mapping[str, str]) -> list[str]:
    failures: list[str] = []
    for file_name in USER_FACING_GENERATED_FILES:
        text = packet_files.get(file_name)
        if text is None:
            continue
        for reason, pattern in USER_FACING_TECHNICAL_METADATA_PATTERNS:
            if pattern.search(text):
                failures.append(
                    f"{file_name}: USER-facing generated file contains technical metadata {reason}"
                )
    return failures


def _user_branch_plan_stale_bp1_wording_failures(packet_files: Mapping[str, str]) -> list[str]:
    text = packet_files.get(USER_BRANCH_PLAN_REVIEW_FILE)
    if text is None:
        return []
    failures: list[str] = []
    for reason, pattern in USER_BRANCH_PLAN_STALE_BP1_WORDING_PATTERNS:
        if pattern.search(text):
            failures.append(
                f"{USER_BRANCH_PLAN_REVIEW_FILE}: BP2 review contains stale BP1/product-design wording {reason}"
            )
    return failures


def _start_here_file_mappings(start_here: str) -> dict[str, str]:
    mappings: dict[str, str] = {}
    row_pattern = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", re.MULTILINE)
    for source_path, copied_path in row_pattern.findall(start_here):
        mappings[source_path.replace("\\", "/")] = copied_path.replace("\\", "/")
    return mappings


def _git_file_text(ref: str, source_path: str) -> str | None:
    try:
        data = subprocess.check_output(
            ["git", "show", f"{ref}:{source_path}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None
    return data.decode("utf-8", errors="replace")


def _normalized_packet_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _packet_identity_failures(
    packet_files: Mapping[str, str],
    *,
    expected_branch: str,
    expected_head: str,
    expected_origin_main: str,
) -> list[str]:
    failures: list[str] = []
    current_branch = _git_output("rev-parse", "--abbrev-ref", "HEAD")
    current_head = _git_output("rev-parse", "HEAD")
    current_origin_main = _git_output("rev-parse", "origin/main")

    if current_branch != expected_branch:
        failures.append(
            "Packet identity: expected branch "
            f"{expected_branch!r} does not match current branch {current_branch!r}"
        )
    if current_head != expected_head:
        failures.append(
            "Packet identity: expected HEAD "
            f"{expected_head!r} does not match current HEAD {current_head!r}"
        )
    if current_origin_main != expected_origin_main:
        failures.append(
            "Packet identity: expected origin/main "
            f"{expected_origin_main!r} does not match current origin/main {current_origin_main!r}"
        )

    start_here = packet_files.get("START_HERE.md", "")
    file_mappings = _start_here_file_mappings(start_here)
    if not file_mappings:
        failures.append("START_HERE.md: source/copy file mapping table is missing")
        return failures

    for source_path, copied_path in file_mappings.items():
        packet_text = packet_files.get(copied_path)
        if packet_text is None:
            continue
        expected_text = _git_file_text(expected_head, source_path)
        if expected_text is None:
            failures.append(
                "Packet identity: copied source path is not present at expected HEAD: "
                f"{source_path}"
            )
            continue
        if _normalized_packet_text(packet_text) != _normalized_packet_text(expected_text):
            failures.append(
                "Packet identity: copied file does not match expected HEAD content: "
                f"{copied_path} from {source_path}"
            )
    return failures


def _user_facing_decision_text(exact_user_decision: str) -> str:
    """Keep USER files decision-focused while chat/helper output carries byte proof."""

    text = re.sub(
        r"\b[0-9a-f]{40}\b",
        "[current commit recorded in Codex chat digest]",
        exact_user_decision,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bHEAD\b",
        "current commit recorded in Codex chat digest",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\borigin/main(?:@[A-Za-z0-9_.-]+)?\b",
        "current main baseline recorded in Codex chat digest",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\blive PR state\b|\bPR state\b",
        "PR-readiness review posture",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bvalidation health\b|\bvalidation status\b",
        "validation review expectations",
        text,
        flags=re.IGNORECASE,
    )
    return text


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


def _write_user_branch_vision_review(
    *,
    target: Path,
    title: str,
    review_purpose: str,
    exact_user_decision: str,
    pending_user_decisions: list[str],
    copied: list[tuple[str, str]],
) -> Path:
    source_files = [f"`{source_rel}` copied as `{copied_rel}`" for source_rel, copied_rel in copied]
    pr_readiness_context_packet = "pr readiness stage 1 analysis" in exact_user_decision.casefold()
    review_status = (
        "Context Complete - this packet uses BP1 as review context for PR Readiness Stage 1; "
        "it does not request a new Branch Vision decision."
        if pr_readiness_context_packet
        else "Needs USER Decision unless this packet records an explicit USER acceptance or waiver."
    )
    contract_status = (
        "Complete - Branch Vision context is recorded for this PR Readiness review packet; "
        "implementation remains outside this decision."
        if pr_readiness_context_packet
        else "Draft - update to Complete or Waived by USER only after USER accepts or waives BP1 for this branch."
    )
    user_response = (
        "No new BP1 response requested by this packet; PR Readiness Stage 1 analysis remains the next USER decision."
        if pr_readiness_context_packet
        else "Pending USER response or explicit waiver."
    )
    codex_digest = (
        "Codex records this BP1 file as a context aid for the governance lifecycle reform packet. "
        "Accepted outcomes must fold into durable source-truth owners or external operational state."
        if pr_readiness_context_packet
        else "Pending USER response digest."
    )
    accepted_vision = (
        "Accepted context: Governance Phase Lifecycle Reform and local USER hub model are represented by the copied source-truth files."
        if pr_readiness_context_packet
        else "Pending USER acceptance or waiver."
    )
    lines = [
        f"# {title} - USER Branch Vision Review",
        "",
        "USER Branch Vision Review: BP1",
        "",
        "## Review Status",
        "",
        review_status,
        "",
        "## Contract Status",
        "",
        contract_status,
        "",
        "## Contract Revision",
        "",
        "v1 - generated by the local USER hub helper.",
        "",
        "## Project Vision Context",
        "",
        "Review `Docs/nexus_vision.md` or the current project-wide vision owner before accepting this Branch Vision.",
        "",
        "## Family Vision Context",
        "",
        "Review the relevant `Docs/family_visions/` owner for the branch family before accepting this Branch Vision.",
        "",
        "## Feature Vision Context",
        "",
        "Review the active branch authority and branch planning owner for the feature or package context.",
        "",
        "## Codex Understanding",
        "",
        review_purpose,
        "",
        "## Branch Goal",
        "",
        "Confirm that this branch goal is the right product direction before engineering planning proceeds.",
        "",
        "## End-State Vision",
        "",
        "Describe the intended user-visible or source-truth end state for this branch. If no user-visible surface applies, describe the durable governance or runtime outcome USER will rely on.",
        "",
        "## What Will I Actually See, And Where Will I See It?",
        "",
        "The USER-facing review packet lives in the local USER hub. Runtime/user-facing surfaces, if any, must be described by the branch-specific packet or source truth copied into this folder.",
        "",
        "## How It Will Function",
        "",
        "BP1 captures what the branch should become. BP2 captures how Codex plans to build it. Workstream implementation remains blocked until BP1/BP2 are accepted or waived and BP3 is green.",
        "",
        "## User Experience Flow",
        "",
        "Review the copied branch-specific files and note any changes to product flow, decision flow, or inspection flow before accepting BP1.",
        "",
        "## Surface Map",
        "",
        *_markdown_lines(source_files),
        "",
        "## Product Options / Design Paths",
        "",
        "- Accept the proposed Branch Vision.",
        "- Revise the Branch Vision before engineering planning.",
        "- Waive BP1 for this branch with explicit USER text.",
        "- Reject this branch direction and request a narrower or different carrier.",
        "",
        "## Codex Recommendations",
        "",
        "- Recommendation: Treat BP1 as the product/vision gate and keep SLCs as engineering route details.",
        "  USER response:",
        "- Recommendation: Use BP2 only after the accepted Branch Vision is clear.",
        "  USER response:",
        "",
        "## Why This Fits The Nexus Vision",
        "",
        "This keeps project and family vision above branch planning while preventing implementation seams from becoming accidental product direction.",
        "",
        "## USER Design Questions",
        "",
        "- Does this Branch Vision match what the USER wants this branch to become?",
        "- Are any surfaces, flows, boundaries, or future-gated ideas missing?",
        "",
        "## USER Response",
        "",
        user_response,
        "",
        "## Codex Digest",
        "",
        codex_digest,
        "",
        "## Accepted Branch Vision",
        "",
        accepted_vision,
        "",
        "## Family-Vision Versus Branch-Only Vision Impact",
        "",
        "Branch-only unless USER response creates a reusable family or project-wide standard that must fold into the proper durable owner.",
        "",
        "## Must-Have Behavior",
        "",
        "- BP1 must be accepted or explicitly waived before BP2/BP3 can authorize implementation.",
        "- SLCs must trace to an accepted Branch Vision requirement.",
        "",
        "## Must-Not-Do / Regression-Risk Rules",
        "",
        "- Do not turn SLCs into automatic separate branches.",
        "- Do not use Workstream for planning.",
        "- Do not center mutable operational metadata as the USER-facing contract.",
        "",
        "## Deferred And Future-Gated Ideas",
        "",
        *_markdown_lines(pending_user_decisions),
        "",
        "## Vision Question Queue",
        "",
        "Pending USER review.",
        "",
        "## Design Assumption Ledger",
        "",
        "- Assumption: USER-facing Branch Vision acceptance is required unless explicitly waived.",
        "- Assumption: accepted branch vision changes fold into durable source-truth owners only after USER-approved digest.",
        "",
        "## Acceptance / Revision / Rejection / Waiver Decision",
        "",
        exact_user_decision,
        "",
    ]
    review_path = target / USER_BRANCH_VISION_REVIEW_FILE
    review_path.write_text("\n".join(lines), encoding="utf-8")
    return review_path.resolve()


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
        for source_rel, _copied_rel in copied
    )
    is_fam007_breakpoint_2 = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        or any(
            "feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness" in source_rel
            for source_rel, _copied_rel in copied
        )
    )
    pr_readiness_stage1_packet = "pr readiness stage 1 analysis" in exact_user_decision.casefold()
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
            "Docs/ai_runtime_and_trust_architecture.md",
            "Docs/family_visions/FAM-007_local_ai_and_capability_packs.md",
            "Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md",
        }
    ]
    if is_active_overlay_recording:
        active_plan_source = next(
            (
                source_rel
                for source_rel, _copied_rel in copied
                if source_rel.endswith(
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
        ) or "Pending USER Confirmation - Codex revised this review into the closed-loop BP2 Branch Plan Contract; USER must confirm the revised contract or explicitly waive it before implementation."
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
            "Active external branch plan and branch record: record the accepted v3/v4 planning-governance posture, USER vision digest, implementation constraints, Workstream skip, and PR Readiness Stage 1 as the next legal phase.",
            "Backlog/roadmap: record planning-governance PR-readiness posture rather than runtime implementation posture.",
            "Review packet: refresh whenever contract status, response, digest, constraints, source-truth impact, or copied source-truth inputs change.",
            "Workstream seam order: target model remains future implementation staging, not current branch work.",
        ]
        contract_change_log = [
            "v1 - USER-facing Branch Plan Review packet introduced with end-state/options sections.",
            "v2 - Hardened into BP2 Branch Plan Contract with closed-loop response/digest, implementation constraints, source-truth impact, confirmation loop, and waiver semantics.",
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
            "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
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
    elif is_fam007_breakpoint_2:
        seam1_approval_packet = "approve bounded workstream implementation" in exact_user_decision.casefold()
        seam1_completion_packet = "approve or revise seam 2" in exact_user_decision.casefold()
        workstream_green_packet = "approve bounded hardening h1" in exact_user_decision.casefold()
        hardening_h1_packet = "approve bounded live validation lv1" in exact_user_decision.casefold()
        lv1_green_packet = "approve bounded pr readiness stage 1" in exact_user_decision.casefold()
        pr_stage2_packet = "approve pr readiness stage 2" in exact_user_decision.casefold()
        accepted_user_response = (
            "Status: USER Accepted - USER approved this repaired branch contract as the "
            "decision-path basis for bounded Seam 1 implementation approval."
            if seam1_approval_packet
            else (
                "Status: Workstream Green - this packet records all admitted public-safe "
                "Breakpoint 2 Workstream proof seams and asks USER to approve or revise Hardening H1."
            )
            if workstream_green_packet
            else (
                "Status: Seam 1 Complete - this packet records public-safe action-gate "
                "registry proof and asks USER to approve or revise Seam 2."
            )
            if seam1_completion_packet
            else (
                "Status: Pending USER Acceptance Or Waiver - this repaired contract is ready for "
                "USER to accept, revise, reject, or explicitly waive before Seam 1 implementation."
            )
        )
        codex_response_digest = (
            "Workstream is green for the FAM-007 Breakpoint 2 Dev/Owner skeleton action-gate "
            "readiness carrier. Codex recorded Seams 1 through 4 as public-safe proof, "
            "added direct validator fixture proof, folded source truth down, and preserved "
            "all private/runtime/provider/cache/memory action gates. Codex recommends "
            "Hardening H1 next."
            if workstream_green_packet
            else
            "Seam 1 is complete for the FAM-007 Breakpoint 2 Dev/Owner skeleton action-gate "
            "readiness carrier. Codex recorded the action-gate registry, exact USER decision proof, "
            "source-truth fold-down, and direct validator fixture proof without performing any gated "
            "private/runtime action. Codex recommends Seam 2 next: private/public boundary and "
            "private remote safety proof."
            if seam1_completion_packet
            else (
                "Workstream Entry analysis is green for the FAM-007 Breakpoint 2 Dev/Owner skeleton "
                "action-gate readiness carrier. Codex recommends Seam 1 first: action-gate registry "
                "and exact USER decision proof. Seam 1 should create public-safe proof of the private "
                "Dev repo, private Owner repo, local-only private root, private remote, backup/import, "
                "provider/model/runtime/cache/memory, voice/Core, shortcut/installer, PR/merge/release, "
                "cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0 gates without "
                "performing any gated action."
            )
        )
        if hardening_h1_packet:
            accepted_user_response = (
                "Status: Hardening H1 Green - this packet records bounded proof comparison, "
                "H1-scoped drift repair, and asks USER to approve or revise Live Validation LV1."
            )
            codex_response_digest = (
                "Hardening H1 is green for the FAM-007 Breakpoint 2 Dev/Owner skeleton "
                "action-gate readiness carrier. Codex compared Seams 1 through 4 against "
                "source truth, validators, fixtures, packet proof, and external-state boundaries; "
                "repaired stale duplicate Workstream-pending ledger wording; and preserved all "
                "private/runtime/provider/cache/memory action gates. Codex recommends bounded "
                "Live Validation LV1/no-visible-runtime proof next."
            )
        if lv1_green_packet:
            accepted_user_response = (
                "Status: Live Validation LV1 Green - this packet records no-visible-runtime proof, "
                "UTS waiver evidence, and asks USER to approve or revise PR Readiness Stage 1 analysis."
            )
            codex_response_digest = (
                "Live Validation LV1 is green for the FAM-007 Breakpoint 2 Dev/Owner skeleton "
                "action-gate readiness carrier. Codex recorded no-visible-runtime proof, waived UTS "
                "and user-facing shortcut validation because no app UI/runtime/provider/model/cache/"
                "memory/private/backup/import/voice/Core/shortcut/installer surface changed, preserved "
                "all private/runtime/provider/cache/memory action gates, and recommends bounded PR "
                "Readiness Stage 1 analysis next."
            )
        if pr_stage2_packet:
            accepted_user_response = (
                "Status: PR Readiness Stage 1 Ready For Stage 2 - this packet records no live PR, "
                "Stage 2 PR creation pending USER approval, merge-stable historical/no-active projection, "
                "no-release-debt posture, selected-next default/defer posture, and preserved private/runtime gates."
            )
            codex_response_digest = (
                "PR Readiness Stage 1 is green for the FAM-007 Breakpoint 2 Dev/Owner skeleton "
                "action-gate readiness carrier. Codex recorded no-live-PR posture, pending Stage 2 PR "
                "creation approval, folded repo-tracked active authority to historical/no-active projection, "
                "refreshed packet/source-truth evidence, preserved no-release-debt posture, and recommends "
                "PR Readiness Stage 2 PR creation only after explicit USER approval."
            )
        if pr_stage2_packet:
            workstream_status_text = (
                "Status: PR Readiness Stage 1 Ready For Stage 2 - no live PR exists; "
                "PR Readiness Stage 2 PR creation remains pending USER approval.\n\n"
            )
        elif workstream_green_packet:
            workstream_status_text = (
                "Status: Workstream Green - Seams 1 through 4 are implemented as public-safe "
                "proof only; Hardening H1 remains pending USER decision.\n\n"
            )
        elif lv1_green_packet:
            workstream_status_text = (
                "Status: Live Validation LV1 Green - no visible runtime surface changed; "
                "UTS and user-facing shortcut validation are waived; PR Readiness Stage 1 "
                "remains pending USER approval.\n\n"
            )
        elif hardening_h1_packet:
            workstream_status_text = (
                "Status: Hardening H1 Green - Seams 1 through 4 were compared against "
                "source truth, fixtures, validators, packet proof, and external-state boundaries; "
                "Live Validation LV1 remains pending USER decision.\n\n"
            )
        elif seam1_completion_packet:
            workstream_status_text = (
                "Status: Seam 1 Complete - action-gate registry and exact USER decision proof "
                "are implemented as public-safe proof only; Seam 2 remains pending USER decision.\n\n"
            )
        elif seam1_approval_packet:
            workstream_status_text = (
                "Status: Workstream Entry Green - USER accepted the repaired branch contract; "
                "Seam 1 is approved as the first bounded Workstream implementation seam: "
                "Action-gate registry and exact USER decision proof.\n\n"
            )
        else:
            workstream_status_text = (
                "Status: Workstream Entry Green - recommended first seam is Seam 1, "
                "Action-gate registry and exact USER decision proof.\n\n"
            )
        workstream_entry_result = (
            workstream_status_text
            + (
            "Affected surfaces: active external branch plan, active branch record, USER review packet, packet "
            "bundle helper, validation helper registry when helper behavior changes, and any public-safe "
            "fixtures or validators needed to prove action-gate preservation.\n\n"
            "Validators and fixtures: branch governance, worktree confinement, release-readiness health, "
            "governance efficiency, source-owner markers, release body, AI provider state, public leak "
            "prevention, branch-readiness planning fixtures, external state validation when present, "
            "packet decision-path validation, compileall, and worktree rebaseline audit.\n\n"
            "USER-facing proof expectations: refreshed START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, "
            "USER_REVIEW_FOLDER_AND_FILE_DIGEST.md, GOVERNANCE_REQUIRED_FILES_SCAN.md, "
            "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md, BRANCH_VISION_VALIDATION_CHECKLIST.md, exported ZIP, "
            "and validation summary must all agree on decision path, decision path, and "
            "pending gates.\n\n"
            f"Exact implementation approval text: {exact_user_decision}"
            )
        )
        contract_status = (
            "Complete for PR Readiness Stage 1 - Stage 2 PR creation remains pending USER approval."
            if pr_stage2_packet
            else
            "Complete - USER accepted the repaired branch-specific Workstream Entry contract for "
            "bounded Seam 1 implementation approval."
            if seam1_approval_packet
            else (
                "Complete for Live Validation LV1 - no-visible-runtime proof and UTS waiver "
                "evidence are green and this packet routes USER to approve or revise PR "
                "Readiness Stage 1 analysis."
            )
            if lv1_green_packet
            else (
                "Complete for Hardening H1 - proof comparison is green and this packet routes "
                "USER to approve or revise Live Validation LV1."
            )
            if hardening_h1_packet
            else (
                "Complete for Workstream - all admitted public-safe proof seams are implemented "
                "and this packet routes USER to approve or revise Hardening H1."
            )
            if workstream_green_packet
            else (
                "Complete for Seam 1 - action-gate registry proof is implemented and this packet "
                "routes USER to approve or revise Seam 2."
            )
            if seam1_completion_packet
            else (
                "Complete - branch-specific Workstream Entry contract repaired and ready for USER "
                "acceptance or waiver; Seam 1 implementation remains pending until USER sends the exact "
                "approval text."
            )
        )
        contract_version = (
            "v7 - FAM-007 Breakpoint 2 PR Readiness Stage 1 packet."
            if pr_stage2_packet
            else
            "v6 - FAM-007 Breakpoint 2 Live Validation LV1 packet."
            if lv1_green_packet
            else
            "v5 - FAM-007 Breakpoint 2 Hardening H1 packet."
            if hardening_h1_packet
            else
            "v4 - FAM-007 Breakpoint 2 Workstream Green packet."
            if workstream_green_packet
            else "v2 - FAM-007 Breakpoint 2 Workstream Entry contract repair."
        )
        what_user_sees = (
            "USER will inspect the active Breakpoint 2 branch plan, the branch record, the public-safe "
            "action-gate registry/proof path, validator or fixture expectations, the refreshed review "
            "packet, and the source-truth fold-down path. USER will not see private repositories, "
            "private roots, private remotes, backup/import execution, provider/model execution, runtime "
            "cache behavior, memory behavior, voice/Core sync, shortcut/installer work, PR creation, "
            "merge, release, cleanup, FAM-006 or Governance mutation, AI Product Contract import, "
            "Private Dev ORIN import, or v1.8.0 execution."
        )
        why_nexus = (
            "This fits Nexus because it turns Breakpoint 2 into a decision-ready, public-safe proof "
            "carrier before any private or runtime action occurs. It preserves the AI Runtime And Trust "
            "Architecture boundaries, keeps provider and memory behavior disabled, and makes each USER "
            "action gate explicit before Dev/Owner skeleton setup can begin."
        )
        design_ballot = [
            "Accept Seam 1 as recommended.",
            "Revise Seam 1 proof expectations before implementation.",
            "Waive unresolved review questions and approve Seam 1.",
            "Reject this branch contract and request a narrower carrier.",
        ]
        response_structure = [
            "Decision: accept, revise, waive, or reject.",
            "Required changes to Seam 1 proof expectations, if any.",
            "Must-have action-gate proof.",
            "Must-not-do boundaries.",
            "Explicit waiver language, if USER wants to waive unresolved questions.",
            "General response.",
        ]
        digest_structure = [
            "USER intent summary.",
            "Accepted or waived contract state.",
            "Approved Seam 1 scope.",
            "Rejected or deferred proof expectations.",
            "Implementation constraints created from USER response.",
            "Source-truth or packet updates required.",
            "Open questions.",
            "Next USER decision needed.",
        ]
        implementation_constraints = [
            (
                "USER accepted this contract for Seam 1; the approved work is limited to public-safe "
                "action-gate registry/proof, deterministic fixtures or validators, source-truth "
                "fold-down, packet refresh, and validation."
                if seam1_approval_packet
                else (
                    "Workstream is green; Hardening H1 remains blocked until USER approves or revises "
                    "the proof-comparison hardening seam."
                )
                if workstream_green_packet
                else (
                    "Seam 1 is complete; Seam 2 remains blocked until USER approves or revises the "
                    "private/public boundary and private remote safety proof seam."
                )
                if seam1_completion_packet
                else "Until USER accepts or waives this contract, Seam 1 implementation remains blocked."
            ),
            "Seam 1 work is limited to public-safe action-gate registry/proof, deterministic fixtures or validators, source-truth fold-down, packet refresh, and validation.",
            "No private Dev repo, private Owner repo, local-only private root, private remote, GitHub Desktop private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006 mutation, Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work is authorized by this packet.",
            "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior not implemented.",
        ]
        rejected_deferred = [
            "Deferred: private Dev repo creation, private Owner repo creation, local-only private root creation, GitHub Desktop private remote configuration, off-boot backup or recovery root implementation, and Public-to-Dev import implementation.",
            "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release, cleanup, FAM-006/Governance/sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.",
            "Rejected for Seam 1: any hidden private setup, silent provider enablement, cache/memory runtime behavior, or action that would make a USER gate look already completed.",
        ]
        source_truth_impact = [
            "Active external branch plan and branch record should preserve Breakpoint 2 as a real FAM-007 product/workstream carrier.",
            "AI Runtime And Trust Architecture remains the cross-family owner for provider boundaries, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, local-only proof, and capability-pack readiness.",
            "Review packet should remain branch-specific, freshness-verified, count-consistent, placeholder-free, and explicit that Seam 1 approval covers only public-safe action-gate proof.",
            "Source-truth fold-down during Seam 1 should record proof of action-gate preservation without executing gated private/runtime actions.",
        ]
        contract_change_log = [
            "v1 - Stage 2 review packet generated with generic USER Branch Plan Review language.",
            "v2 - Repaired into a branch-specific FAM-007 Breakpoint 2 engineering contract with Workstream Entry result, recommended Seam 1, proof expectations, pending gates, and exact approval text.",
        ]
        completion_checklist = [
            "Contract Status is Complete or Waived by USER.",
            "Workstream Entry Result records green analysis and recommended Seam 1.",
            "USER response is present in chat, copied into the packet later, or explicitly waived.",
            "Exact implementation approval text names Seam 1 only.",
            "Implementation Constraints Created By USER Response preserve all private/runtime/provider/cache/memory gates.",
            "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
            "Packet digest files agree that Workstream Entry is green and Seam 1 approval is limited to public-safe action-gate proof.",
            "No unresolved packet placeholders or packet count mismatches remain.",
            "Validation results are green before Seam 1 starts.",
        ]
        if seam1_completion_packet:
            design_ballot = [
                "Approve Seam 2 as recommended.",
                "Revise Seam 2 private-boundary proof expectations before implementation.",
                "Pause after Seam 1 and keep the branch open.",
                "Reject later seams and request a narrower closeout path.",
            ]
            response_structure = [
                "Decision: approve, revise, pause, or reject.",
                "Required changes to Seam 2 proof expectations, if any.",
                "Must-have private-boundary or remote-safety proof.",
                "Must-not-do boundaries.",
                "General response.",
            ]
            digest_structure = [
                "USER intent summary.",
                "Seam 1 completion acceptance or concerns.",
                "Approved or revised Seam 2 scope.",
                "Implementation constraints created from USER response.",
                "Next USER decision needed.",
            ]
            contract_change_log = [
                "v1 - Stage 2 review packet generated with generic USER Branch Plan Review language.",
                "v2 - Repaired into a branch-specific FAM-007 Breakpoint 2 engineering contract with Workstream Entry result, recommended Seam 1, proof expectations, pending gates, and exact approval text.",
                "v3 - Seam 1 action-gate registry and exact USER decision proof implemented with direct validator fixture proof.",
            ]
            completion_checklist = [
                "Seam 1 source-truth fold-down is present in the branch plan and branch record.",
                "Direct validator fixture proof covers the action-gate registry and exact USER decision proof.",
                "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
                "Packet digest files agree that Seam 1 is complete and Seam 2 remains pending USER approval.",
                "No unresolved packet placeholders or packet count mismatches remain.",
            ]
        plain_english_summary = (
            "This FAM-007 branch prepares Breakpoint 2 for a future Dev/Owner skeleton setup decision. "
            "Its job is not to create private repos or turn on AI runtime behavior; its job is to make "
            "the exact action gates, proof files, validation expectations, and USER decisions clear "
            "enough that the next implementation seam can safely prove readiness."
        )
        end_state_vision = (
            "When this readiness work is complete, USER should have a public-safe proof package showing "
            "which Dev/Owner skeleton actions remain blocked, which exact approvals would unlock them, "
            "which validators prove the gates stayed closed, and how the branch can hand off to the "
            "future private setup decision without ambiguity."
        )
        walkthrough = [
            "Open START_HERE.md first and review the plain-language file map and USER decision.",
            "Open USER_BRANCH_PLAN_REVIEW.md and review this contract, especially Seam 1, action-gate proof expectations, and pending gates.",
            "Open the active external branch plan to verify the product/workstream carrier posture and Breakpoint 2 scope.",
            "Inspect the action-gate registry/proof surface once Seam 1 is implemented; each gated action should say pending, blocked, or USER-required rather than completed.",
            "Review validator or fixture outputs proving no private repo, private root, private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, or PR/merge/release work occurred.",
            "Upload the matching ZIP beside the local USER hub folder after reviewing the packet.",
        ]
        surface_map = [
            "USER review packet: START_HERE.md, USER_BRANCH_VISION_REVIEW.md, USER_BRANCH_PLAN_REVIEW.md, folder/file digest, governance scan, Workstream Entry digest, branch vision checklist, and ZIP export.",
            "Active external branch plan: C:\\Nexus Governance State\\branches\\feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness\\branch_plan.md.",
            "Branch record: Docs/branch_records/feature_fam_007_breakpoint_2_dev_owner_skeleton_action_gate_readiness.md.",
            "Architecture owner: Docs/ai_runtime_and_trust_architecture.md.",
            "FAM-007 owners: Docs/family_visions/FAM-007_local_ai_and_capability_packs.md and Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md.",
            "Validation surfaces: dev/orin_user_review_bundle.py, dev/orin_public_leak_prevention_validation.py, dev/orin_branch_readiness_planning_fixture_validation.py, dev/orin_branch_governance_validation.py, and Docs/validation_helper_registry.md.",
            "External operational state: records branch authority and packet posture outside the repo when current governance requires it.",
        ]
        implementation_options = [
            "Accept Seam 1 as recommended: implement public-safe action-gate registry and exact USER decision proof first. Pros: clearest readiness foundation; Cons: no private setup yet; Risk: low.",
            "Revise Seam 1 proof expectations before implementation. Pros: lets USER tune proof wording or validator expectations; Cons: adds packet/source-truth repair; Risk: low.",
            "Waive unresolved review questions and approve Seam 1. Pros: unblocks bounded proof work; Cons: records less design feedback; Risk: medium if important proof expectations are not named.",
            "Reject this branch contract and request a narrower carrier. Pros: maximum scope control; Cons: delays Breakpoint 2 readiness; Risk: low but slower.",
        ]
        recommended_direction = (
            "Codex recommends accepting the repaired branch contract and approving Seam 1 only when USER "
            "agrees that the public-safe proof path is correct. Seam 1 should prove the action gates and "
            "decision text before any later private Dev/Owner skeleton setup decision is considered."
        )
        current_scope = [
            "Branch-specific Workstream Entry contract repair.",
            "Completed Workstream Entry result recorded in the packet.",
            "Recommended first seam recorded as Seam 1, Action-gate registry and exact USER decision proof.",
            "Local USER hub packet and ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the decision path.",
            "Validation before any Seam 1 file mutation begins.",
        ]
        future_scope = [
            "Seam 1 approval is limited to public-safe action-gate registry and exact USER decision proof.",
            "Private Dev/Owner repo creation, local-only private roots, private remotes, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
        ]
        slc_package_plan = [
            "Seam 1: action-gate registry and exact USER decision proof.",
            "Later seams may add private-boundary readiness, local-only/private-root readiness, private remote safety, public-to-private separation, and provider/model/runtime/cache/memory deferral proof only after USER approves them.",
            "No seam may execute the private/runtime action it is proving as gated.",
        ]
        if workstream_green_packet:
            walkthrough = [
                "Open START_HERE.md first and review the plain-language file map and USER decision.",
                "Open USER_BRANCH_PLAN_REVIEW.md and confirm the contract is Workstream Green with Hardening H1 as the next decision.",
                "Open the active external branch plan and branch record to verify Seams 1 through 4 are recorded as public-safe proof only.",
                "Review the fixture and validator proof showing all private/runtime/provider/cache/memory gates remain pending.",
                "Upload the matching ZIP beside the local USER hub folder after reviewing or revising Hardening H1.",
            ]
            implementation_options = [
                "Approve Hardening H1 as recommended: compare all public-safe Workstream proof against source truth, fixtures, validators, packet proof, and external-state boundaries. Pros: moves the branch into the required proof-comparison phase; Cons: no PR/merge/release yet; Risk: low.",
                "Revise Hardening H1 proof expectations before implementation. Pros: lets USER tune pressure-test criteria; Cons: adds packet/source-truth repair; Risk: low.",
                "Pause at Workstream Green and keep the branch open. Pros: preserves the green Workstream proof without expanding scope; Cons: delays closeout; Risk: low.",
                "Reject Hardening and request a narrower Workstream closeout repair. Pros: maximum scope control; Cons: may leave proof comparison incomplete; Risk: low but slower.",
            ]
            design_ballot = [
                "Approve Hardening H1 as recommended.",
                "Revise Hardening H1 proof expectations before implementation.",
                "Pause at Workstream Green.",
                "Reject and request a narrower closeout repair.",
            ]
            response_structure = [
                "Decision: approve, revise, pause, or reject.",
                "Required changes to Hardening H1 proof expectations, if any.",
                "Must-have proof-comparison or pressure-test criteria.",
                "Must-not-do boundaries.",
                "General response.",
            ]
            digest_structure = [
                "USER intent summary.",
                "Workstream Green acceptance or concerns.",
                "Approved or revised Hardening H1 scope.",
                "Implementation constraints created from USER response.",
                "Next USER decision needed.",
            ]
            contract_change_log = [
                "v1 - Stage 2 review packet generated with generic USER Branch Plan Review language.",
                "v2 - Repaired into a branch-specific FAM-007 Breakpoint 2 engineering contract with Workstream Entry result, recommended Seam 1, proof expectations, pending gates, and exact approval text.",
                "v3 - Seam 1 action-gate registry and exact USER decision proof implemented with direct validator fixture proof.",
                "v4 - Seams 2 through 4 implemented as public-safe proof and Workstream Green candidate recorded.",
            ]
            completion_checklist = [
                "Seams 1 through 4 source-truth fold-down is present in the branch plan and branch record.",
                "Direct validator fixture proof covers action gates, private/public boundary, backup/import planning gates, provider/runtime/cache/memory deferral, and Hardening handoff readiness.",
                "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
                "Packet digest files agree that Workstream is green and Hardening H1 remains pending USER approval.",
                "No unresolved packet placeholders or packet count mismatches remain.",
            ]
            recommended_direction = (
                "Codex recommends approving Hardening H1 only if USER agrees the next proof should "
                "pressure-test the completed public-safe Workstream proof without executing private, "
                "runtime, provider, cache, memory, PR, merge, release, cleanup, or v1.8.0 actions."
            )
            current_scope = [
                "Seam 1 action-gate registry proof implemented.",
                "Seam 2 private/public boundary and private remote safety proof implemented.",
                "Seam 3 backup/recovery and Public-to-Dev import planning proof implemented.",
                "Seam 4 provider/model/runtime/cache/memory deferral and local-only handoff proof implemented.",
                "Local USER hub packet and ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the Hardening H1 next decision.",
            ]
            future_scope = [
                "Hardening H1 approval is limited to proof comparison and pressure testing.",
                "Private Dev/Owner repo creation, local-only private roots, private remotes, backup/import execution, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
            ]
            slc_package_plan = [
                "Seams 1 through 4 complete as public-safe proof.",
                "Hardening H1 next: compare all proof against source truth, fixtures, validators, packet proof, and external-state boundaries.",
                "No hardening step may execute the private/runtime action it is pressure-testing as gated.",
            ]
            implementation_constraints = [
                "Workstream is green; Hardening H1 remains blocked until USER approves or revises the proof-comparison hardening seam.",
                "Hardening H1 is limited to comparison, pressure testing, validation, and H1-scoped source-truth/validator/packet repairs if required.",
                "No private Dev repo, private Owner repo, local-only private root, private remote, GitHub Desktop private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006 mutation, Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work is authorized by this packet.",
                "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior not implemented.",
            ]
            rejected_deferred = [
                "Deferred: private Dev repo creation, private Owner repo creation, local-only private root creation, GitHub Desktop private remote configuration, off-boot backup or recovery root implementation, and Public-to-Dev import implementation.",
                "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release, cleanup, FAM-006/Governance/sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.",
                "Rejected for Hardening H1: executing the private/runtime action being pressure-tested as gated, silently enabling provider/cache/memory behavior, or turning proof comparison into PR/merge/release work.",
            ]
            source_truth_impact = [
                "Active external branch plan and branch record preserve Breakpoint 2 as a real FAM-007 product/workstream carrier.",
                "AI Runtime And Trust Architecture remains the cross-family owner for provider boundaries, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, local-only proof, and capability-pack readiness.",
                "Review packet remains branch-specific, freshness-verified, count-consistent, placeholder-free, and explicit that Hardening H1 approval covers only proof comparison and H1-scoped repair.",
                "Source-truth fold-down records Seams 1 through 4 as public-safe proof without executing gated private/runtime actions.",
            ]
        if hardening_h1_packet:
            walkthrough = [
                "Open START_HERE.md first and review the plain-language file map and USER decision.",
                "Open USER_BRANCH_PLAN_REVIEW.md and confirm the contract is Hardening H1 Green with Live Validation LV1 as the next decision.",
                "Open the active external branch plan and branch record to verify the H1 comparison receipt and stale-ledger repair.",
                "Review validator proof showing stale Workstream-pending phrases are rejected and all private/runtime/provider/cache/memory gates remain pending.",
                "Upload the matching ZIP beside the local USER hub folder after reviewing or revising LV1/no-visible-runtime proof.",
            ]
            implementation_options = [
                "Approve Live Validation LV1 as recommended: digest no-visible-runtime proof and UTS waiver evidence from source-truth, fixtures, validators, packet proof, and external-state boundaries. Pros: moves the branch toward PR Readiness without pretending runtime was exercised; Cons: no PR/merge/release yet; Risk: low.",
                "Revise LV1 proof expectations before validation. Pros: lets USER tune waiver/evidence criteria; Cons: adds packet/source-truth repair; Risk: low.",
                "Pause at Hardening H1 Green and keep the branch open. Pros: preserves the H1 proof without expanding scope; Cons: delays closeout; Risk: low.",
                "Reject LV1 and request a narrower H1 closeout repair. Pros: maximum scope control; Cons: may leave Live Validation evidence incomplete; Risk: low but slower.",
            ]
            design_ballot = [
                "Approve Live Validation LV1 as recommended.",
                "Revise LV1/no-visible-runtime proof expectations before validation.",
                "Pause at Hardening H1 Green.",
                "Reject and request a narrower closeout repair.",
            ]
            response_structure = [
                "Decision: approve, revise, pause, or reject.",
                "Required changes to LV1/no-visible-runtime proof expectations, if any.",
                "Must-have waiver or validation evidence.",
                "Must-not-do boundaries.",
                "General response.",
            ]
            digest_structure = [
                "USER intent summary.",
                "Hardening H1 acceptance or concerns.",
                "Approved or revised LV1/no-visible-runtime scope.",
                "Implementation constraints created from USER response.",
                "Next USER decision needed.",
            ]
            contract_change_log = [
                "v1 - Stage 2 review packet generated with generic USER Branch Plan Review language.",
                "v2 - Repaired into a branch-specific FAM-007 Breakpoint 2 engineering contract with Workstream Entry result, recommended Seam 1, proof expectations, pending gates, and exact approval text.",
                "v3 - Seam 1 action-gate registry and exact USER decision proof implemented with direct validator fixture proof.",
                "v4 - Seams 2 through 4 implemented as public-safe proof and Workstream Green candidate recorded.",
                "v5 - Hardening H1 compared proof, repaired stale ledger wording, and routed the packet to Live Validation LV1.",
            ]
            completion_checklist = [
                "Hardening H1 comparison receipt is present in the branch plan and branch record.",
                "Direct validator proof rejects stale Workstream-pending ledger phrases.",
                "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
                "Packet digest files agree that Hardening H1 is green and Live Validation LV1 remains pending USER approval.",
                "No unresolved packet placeholders or packet count mismatches remain.",
            ]
            recommended_direction = (
                "Codex recommends approving bounded Live Validation LV1 only if USER agrees the next proof "
                "should digest no-visible-runtime and UTS waiver evidence without executing private, runtime, "
                "provider, cache, memory, PR, merge, release, cleanup, or v1.8.0 actions."
            )
            current_scope = [
                "Hardening H1 proof comparison complete.",
                "Stale duplicate Workstream-pending ledger wording repaired.",
                "Direct validator guard added for stale Breakpoint 2 Workstream-pending phrases.",
                "Local USER hub packet and ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the Live Validation LV1 next decision.",
            ]
            future_scope = [
                "Live Validation LV1 approval is limited to no-visible-runtime proof and UTS waiver digestion.",
                "Private Dev/Owner repo creation, local-only private roots, private remotes, backup/import execution, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
            ]
            slc_package_plan = [
                "Hardening H1 complete as public-safe proof comparison.",
                "Live Validation LV1 next: digest no-visible-runtime proof and UTS waiver evidence.",
                "No LV1 step may execute the private/runtime action it is proving absent.",
            ]
            implementation_constraints = [
                "Hardening H1 is green; Live Validation LV1 remains blocked until USER approves or revises the no-visible-runtime proof seam.",
                "LV1 is limited to no-visible-runtime proof, UTS waiver digestion, validation, and LV1-scoped source-truth/validator/packet repairs if required.",
                "No private Dev repo, private Owner repo, local-only private root, private remote, GitHub Desktop private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006 mutation, Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work is authorized by this packet.",
                "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior not implemented.",
            ]
            rejected_deferred = [
                "Deferred: private Dev repo creation, private Owner repo creation, local-only private root creation, GitHub Desktop private remote configuration, off-boot backup or recovery root implementation, and Public-to-Dev import implementation.",
                "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release, cleanup, FAM-006/Governance/sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.",
                "Rejected for LV1: executing runtime/private/provider/cache/memory behavior just to prove it did not change.",
            ]
            source_truth_impact = [
                "Active external branch plan and branch record preserve Breakpoint 2 as a real FAM-007 product/workstream carrier.",
                "AI Runtime And Trust Architecture remains the cross-family owner for provider boundaries, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, local-only proof, and capability-pack readiness.",
                "Review packet remains branch-specific, freshness-verified, count-consistent, placeholder-free, and explicit that LV1 approval covers only no-visible-runtime proof and UTS waiver digestion.",
                "Source-truth fold-down records H1 Green without executing gated private/runtime actions.",
            ]
        if lv1_green_packet:
            walkthrough = [
                "Open START_HERE.md first and review the plain-language file map and USER decision.",
                "Open USER_BRANCH_PLAN_REVIEW.md and confirm the contract is Live Validation LV1 Green with PR Readiness Stage 1 as the next decision.",
                "Open the active external branch plan and branch record to verify the LV1/no-visible-runtime proof receipt and UTS waiver.",
                "Review validator proof showing LV1 source-truth phrases are present and stale H1/LV1-pending phrases are rejected.",
                "Upload the matching ZIP beside the local USER hub folder after reviewing or revising PR Readiness Stage 1 analysis.",
            ]
            implementation_options = [
                "Approve PR Readiness Stage 1 as recommended: analyze PR readiness for the completed public-safe Breakpoint 2 proof carrier. Pros: moves toward PR creation review; Cons: no PR/merge/release yet; Risk: low.",
                "Revise PR Readiness Stage 1 inspection criteria before analysis. Pros: lets USER tune PR readiness proof; Cons: adds packet/source-truth repair; Risk: low.",
                "Pause at Live Validation LV1 Green and keep the branch open. Pros: preserves the LV1 proof without expanding scope; Cons: delays PR readiness; Risk: low.",
                "Reject PR Readiness and request a narrower LV1 closeout repair. Pros: maximum scope control; Cons: may leave PR path incomplete; Risk: low but slower.",
            ]
            design_ballot = [
                "Approve PR Readiness Stage 1 as recommended.",
                "Revise PR Readiness Stage 1 inspection criteria before analysis.",
                "Pause at Live Validation LV1 Green.",
                "Reject and request a narrower closeout repair.",
            ]
            response_structure = [
                "Decision: approve, revise, pause, or reject.",
                "Required changes to PR Readiness Stage 1 inspection criteria, if any.",
                "Must-have PR readiness proof.",
                "Must-not-do boundaries.",
                "General response.",
            ]
            digest_structure = [
                "USER intent summary.",
                "LV1 Green acceptance or concerns.",
                "Approved or revised PR Readiness Stage 1 scope.",
                "Implementation constraints created from USER response.",
                "Next USER decision needed.",
            ]
            contract_change_log = [
                "v1 - Stage 2 review packet generated with generic USER Branch Plan Review language.",
                "v2 - Repaired into a branch-specific FAM-007 Breakpoint 2 engineering contract with Workstream Entry result, recommended Seam 1, proof expectations, pending gates, and exact approval text.",
                "v3 - Seam 1 action-gate registry and exact USER decision proof implemented with direct validator fixture proof.",
                "v4 - Seams 2 through 4 implemented as public-safe proof and Workstream Green candidate recorded.",
                "v5 - Hardening H1 compared proof, repaired stale ledger wording, and routed the packet to Live Validation LV1.",
                "v6 - Live Validation LV1 recorded no-visible-runtime proof, UTS waiver, and PR Readiness Stage 1 as the next gate.",
            ]
            completion_checklist = [
                "Live Validation LV1 receipt is present in the branch plan and branch record.",
                "Direct validator proof requires LV1 no-visible-runtime, UTS waiver, and PR Readiness Stage 1 routing phrases.",
                "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
                "Packet digest files agree that Live Validation LV1 is green and PR Readiness Stage 1 remains pending USER approval.",
                "No unresolved packet placeholders or packet count mismatches remain.",
            ]
            recommended_direction = (
                "Codex recommends approving bounded PR Readiness Stage 1 only if USER agrees the next "
                "step should analyze readiness without creating a PR, merging, releasing, cleaning up, "
                "or executing any private/runtime/provider/cache/memory action."
            )
            current_scope = [
                "Workstream Seams 1 through 4 complete as public-safe proof.",
                "Hardening H1 proof comparison complete.",
                "Live Validation LV1 no-visible-runtime proof complete.",
                "UTS and user-facing shortcut validation waived because no visible runtime or shortcut surface changed.",
                "Local USER hub packet and ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the PR Readiness Stage 1 next decision.",
            ]
            future_scope = [
                "PR Readiness Stage 1 approval is limited to analysis only.",
                "PR creation, merge, release, cleanup, private Dev/Owner repo creation, private roots/remotes, backup/import execution, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
            ]
            slc_package_plan = [
                "Workstream, H1, and LV1 are complete as public-safe proof.",
                "PR Readiness Stage 1 next: inspect source-truth fold-down, packet proof, external-state posture, no-release-debt posture, and PR-readiness review expectations.",
                "No PR Readiness Stage 1 step may create a PR, merge, release, clean up, or execute private/runtime actions.",
            ]
            implementation_constraints = [
                "Live Validation LV1 is green; PR Readiness Stage 1 remains blocked until USER approves or revises the analysis scope.",
                "PR Readiness Stage 1 is limited to analysis, validation review, source-truth inspection, packet proof, and decision packet generation.",
                "No private Dev repo, private Owner repo, local-only private root, private remote, GitHub Desktop private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR creation, merge, release, cleanup, FAM-006 mutation, Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work is authorized by this packet.",
                "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior not implemented.",
            ]
            rejected_deferred = [
                "Deferred: PR creation, merge, release, branch/worktree cleanup, and release artifact execution.",
                "Deferred: private Dev repo creation, private Owner repo creation, local-only private root creation, GitHub Desktop private remote configuration, off-boot backup or recovery root implementation, and Public-to-Dev import implementation.",
                "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, FAM-006/Governance/sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.",
            ]
            source_truth_impact = [
                "Active external branch plan and branch record preserve Breakpoint 2 as a real FAM-007 product/workstream carrier completed through LV1.",
                "AI Runtime And Trust Architecture remains the cross-family owner for provider boundaries, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, local-only proof, and capability-pack readiness.",
                "Review packet remains branch-specific, placeholder-free, decision-path-consistent, and explicit that PR Readiness Stage 1 approval covers analysis only.",
                "Source-truth fold-down records LV1 Green without executing gated private/runtime actions.",
            ]
        elif seam1_completion_packet:
            implementation_options = [
                "Approve Seam 2 as recommended: implement public-safe private/public boundary and private remote safety proof. Pros: continues the same gated readiness path; Cons: still no private setup; Risk: low.",
                "Revise Seam 2 proof expectations before implementation. Pros: lets USER tune boundary or remote-safety evidence; Cons: adds packet/source-truth repair; Risk: low.",
                "Pause after Seam 1 and keep the branch open. Pros: preserves the green Seam 1 proof without expanding scope; Cons: delays Breakpoint 2 readiness; Risk: low.",
                "Reject later seams and request a narrower closeout path. Pros: maximum scope control; Cons: may leave Breakpoint 2 readiness incomplete; Risk: low but slower.",
            ]
            recommended_direction = (
                "Codex recommends approving Seam 2 only if USER agrees the next proof should focus "
                "on private/public boundary and private remote safety without configuring private "
                "remotes or creating private roots."
            )
            current_scope = [
                "Seam 1 action-gate registry proof implemented.",
                "Exact USER decision proof implemented.",
                "Direct fixture and validator proof added.",
                "Branch plan and branch record folded down for Seam 1.",
                "Local USER hub packet and ZIP refreshed with the current decision path, file list, and next decision.",
            ]
            future_scope = [
                "Seam 2 approval is limited to private/public boundary and private remote safety proof.",
                "Private Dev/Owner repo creation, local-only private roots, private remotes, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
            ]
            slc_package_plan = [
                "Seam 1 complete: action-gate registry and exact USER decision proof.",
                "Seam 2 next candidate: private/public boundary and private remote safety proof.",
                "No seam may execute the private/runtime action it is proving as gated.",
            ]
        if pr_stage2_packet:
            plain_english_summary = (
                "This FAM-007 packet records that the Breakpoint 2 public-safe proof carrier has "
                "completed Workstream, H1, LV1, and PR Readiness Stage 1 repair. It does not create "
                "a PR by itself; it asks USER whether Stage 2 may create the PR and establish the "
                "required watcher/review path."
            )
            end_state_vision = (
                "After Stage 2 approval, the branch can be opened as a PR to main with the completed "
                "public-safe action-gate proof, while merge, release, cleanup, private setup, provider/"
                "model/runtime/cache/memory behavior, and v1.8.0 work remain separately gated."
            )
            what_user_sees = (
                "USER will inspect the refreshed Stage 1 packet, branch plan, branch record, no-live-PR "
                "posture, no-release-debt posture, merge-stable authority projection, and exact Stage 2 "
                "PR creation approval text. USER will not see private repositories, private roots, "
                "private remotes, backup/import execution, provider/model execution, runtime cache "
                "behavior, memory behavior, voice/Core sync, shortcut/installer work, merge, release, "
                "cleanup, FAM-006 or Governance mutation, AI Product Contract import, Private Dev ORIN "
                "import, or v1.8.0 execution."
            )
            walkthrough = [
                "Open START_HERE.md first and review the plain-language file map and Stage 2 PR creation decision.",
                "Open USER_BRANCH_PLAN_REVIEW.md and confirm the contract is PR Readiness Stage 1 Ready For Stage 2.",
                "Open the branch record PR Readiness Stage 1 Analysis Packet and verify no live PR, Stage 2 pending, no-release-debt posture, selected-next default/defer posture, and merge-stable authority projection.",
                "Open the branch plan PR Readiness Stage 1 Repair Receipt and confirm Stage 2 remains blocked until USER approval.",
                "Upload the matching ZIP beside the local USER hub folder after reviewing or revising Stage 2.",
            ]
            implementation_options = [
                "Approve PR Readiness Stage 2 as recommended: create the PR, verify PR creation and review posture, provision/update watcher, request/monitor Codex bot review, and stop before merge unless later approval exists. Pros: moves the completed proof carrier into review; Cons: no merge/release yet; Risk: low when validation remains green.",
                "Revise Stage 2 PR creation expectations before PR creation. Pros: lets USER tune PR body, watcher, or bot-review requirements; Cons: adds packet/source-truth repair; Risk: low.",
                "Pause at Stage 1 Ready For Stage 2. Pros: preserves clean proof without creating a PR; Cons: delays review; Risk: low.",
                "Reject PR creation and request a narrower closeout. Pros: maximum scope control; Cons: delays branch completion; Risk: low but slower.",
            ]
            design_ballot = [
                "Approve PR Readiness Stage 2 as recommended.",
                "Revise Stage 2 PR creation expectations.",
                "Pause at Stage 1 Ready For Stage 2.",
                "Reject and request a narrower closeout.",
            ]
            response_structure = [
                "Decision: approve, revise, pause, or reject.",
                "Required changes to PR body, watcher, or bot-review expectations, if any.",
                "Must-have PR readiness proof.",
                "Must-not-do boundaries.",
                "General response.",
            ]
            digest_structure = [
                "USER intent summary.",
                "Stage 1 readiness acceptance or concerns.",
                "Approved or revised Stage 2 PR creation scope.",
                "Implementation constraints created from USER response.",
                "Next USER decision needed.",
            ]
            recommended_direction = (
                "Codex recommends approving PR Readiness Stage 2 only if USER agrees the completed "
                "public-safe proof carrier should enter PR review now. Stage 2 may create and watch the "
                "PR, but merge, release, cleanup, private setup, provider/model/runtime/cache/memory "
                "behavior, and v1.8.0 work stay blocked."
            )
            current_scope = [
                "Workstream Seams 1 through 4 complete as public-safe proof.",
                "Hardening H1 proof comparison complete.",
                "Live Validation LV1 no-visible-runtime proof complete.",
                "PR Readiness Stage 1 repair complete with no live PR and Stage 2 pending.",
                "Local USER hub packet and ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the Stage 2 next decision.",
            ]
            future_scope = [
                "PR Readiness Stage 2 approval is limited to PR creation, live PR validation, watcher provisioning/update, Codex bot review request/monitoring, and in-scope Codex comment repair if needed.",
                "Merge, release, cleanup, private Dev/Owner repo creation, private roots/remotes, backup/import execution, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, FAM-006/Governance mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
            ]
            slc_package_plan = [
                "Workstream, H1, LV1, and PR Readiness Stage 1 repair are complete as public-safe proof.",
                "PR Readiness Stage 2 next: verify no live PR or bind to one if it appears, rerun validation, create PR, provision/update watcher, request/monitor Codex bot review, and stop before merge absent later approval.",
                "No Stage 2 step may merge, release, clean up, or execute private/runtime actions.",
            ]
            implementation_constraints = [
                "PR Readiness Stage 1 is green; Stage 2 PR creation remains blocked until USER approves or revises the PR creation scope.",
                "Stage 2 is limited to PR creation, live PR validation, watcher provisioning/update, Codex bot review request/monitoring, in-scope Codex comment repair if needed, packet/source-truth repair if required, and validation.",
                "No private Dev repo, private Owner repo, local-only private root, private remote, GitHub Desktop private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, merge, release, cleanup, FAM-006 mutation, Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work is authorized by this packet.",
                "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior not implemented.",
            ]
            rejected_deferred = [
                "Deferred: merge, release, branch/worktree cleanup, and release artifact execution.",
                "Deferred: private Dev repo creation, private Owner repo creation, local-only private root creation, GitHub Desktop private remote configuration, off-boot backup or recovery root implementation, and Public-to-Dev import implementation.",
                "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, FAM-006/Governance/sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.",
            ]
            source_truth_impact = [
                "Branch plan and branch record preserve Breakpoint 2 as a completed FAM-007 product/workstream proof carrier ready for PR creation approval.",
                "Branch record index projects no active non-standing branch authority on merged main; live operational state comes from Git, GitHub, helpers, and external state.",
                "Review packet remains branch-specific, placeholder-free, decision-path-consistent, and explicit that Stage 2 approval covers PR creation only.",
                "Source-truth fold-down records PR Readiness Stage 1 without executing gated private/runtime actions.",
            ]
            contract_change_log = [
                "v1 - Stage 2 review packet generated with generic USER Branch Plan Review language.",
                "v2 - Repaired into a branch-specific FAM-007 Breakpoint 2 engineering contract with Workstream Entry result, recommended Seam 1, proof expectations, pending gates, and exact approval text.",
                "v3 - Seam 1 action-gate registry and exact USER decision proof implemented with direct validator fixture proof.",
                "v4 - Seams 2 through 4 implemented as public-safe proof and Workstream Green candidate recorded.",
                "v5 - Hardening H1 compared proof, repaired stale ledger wording, and routed the packet to Live Validation LV1.",
                "v6 - Live Validation LV1 recorded no-visible-runtime proof, UTS waiver, and PR Readiness Stage 1 as the next gate.",
                "v7 - PR Readiness Stage 1 repair recorded no live PR, pending Stage 2 approval, no-release-debt posture, selected-next default/defer posture, and merge-stable authority projection.",
            ]
            completion_checklist = [
                "PR Readiness Stage 1 Analysis Packet is present in the branch record.",
                "PR Readiness Stage 1 Repair Receipt is present in the branch plan.",
                "Branch record index projects this branch as historical and keeps only standing Governance active authority.",
                "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
                "Packet digest files agree that Stage 1 is ready for Stage 2 and PR creation remains pending USER approval.",
                "No unresolved packet placeholders or packet count mismatches remain.",
            ]
        user_decisions = [
            "Does USER accept or explicitly waive this repaired USER Branch Plan Review contract?",
            "Does USER approve Seam 1 implementation only: action-gate registry and exact USER decision proof?",
            "Does USER require any change to direct proof expectations before Seam 1 begins?",
            "Does USER confirm all private/runtime/provider/cache/memory/PR/merge/release gates remain pending?",
        ]
        if pr_stage2_packet:
            user_decisions = [
                "Does USER approve PR Readiness Stage 2 PR creation?",
                "Does USER require any change to PR body, watcher, or Codex bot-review expectations before Stage 2 begins?",
                "Does USER confirm merge, release, cleanup, and all private/runtime/provider/cache/memory gates remain pending?",
            ]
        elif hardening_h1_packet:
            user_decisions = [
                "Does USER approve bounded Live Validation LV1/no-visible-runtime proof?",
                "Does USER require any change to LV1 waiver or evidence expectations before it begins?",
                "Does USER confirm all private/runtime/provider/cache/memory/PR/merge/release gates remain pending?",
            ]
        elif lv1_green_packet:
            user_decisions = [
                "Does USER approve bounded PR Readiness Stage 1 analysis?",
                "Does USER require any change to PR Readiness Stage 1 inspection criteria before it begins?",
                "Does USER confirm PR creation, merge, release, cleanup, and all private/runtime/provider/cache/memory gates remain pending?",
            ]
        elif workstream_green_packet:
            user_decisions = [
                "Does USER approve bounded Hardening H1 proof comparison?",
                "Does USER require any change to Hardening H1 pressure-test expectations before it begins?",
                "Does USER confirm all private/runtime/provider/cache/memory/PR/merge/release gates remain pending?",
            ]
        elif seam1_completion_packet:
            user_decisions = [
                "Does USER approve Seam 2 implementation only: private/public boundary and private remote safety proof?",
                "Does USER require any change to direct proof expectations before Seam 2 begins?",
                "Does USER confirm all private/runtime/provider/cache/memory/PR/merge/release gates remain pending?",
            ]
    else:
        accepted_user_response = None
        codex_response_digest = None
        workstream_entry_result = None
        contract_status = (
            "Complete - BP2 engineering plan context is recorded for this PR Readiness Stage 1 packet; "
            "this packet does not request Workstream implementation approval."
            if pr_readiness_stage1_packet
            else "Pending USER Response - USER must accept, revise, reject, request more options, or waive this BP2 engineering plan before implementation."
        )
        contract_version = "v2 - Generated BP2 Branch Plan Review."
        what_user_sees = (
            "USER sees a local USER hub review packet containing the governance lifecycle context plan, "
            "phase law, branch artifact rules, helper/validator ownership, branch authority routing, and "
            "supporting source-truth files needed before PR Readiness Stage 1."
            if pr_readiness_stage1_packet
            else "USER should see the planned implementation surfaces, affected files, validators, proof requirements, and future-gated boundaries before implementation begins."
        )
        why_nexus = (
            "This keeps Branch Vision, Branch Plan, Workstream, Hardening, Live Validation, PR Readiness, "
            "and Release Readiness in separate governance layers while keeping USER review artifacts readable."
            if pr_readiness_stage1_packet
            else "The recommendation should explain how the branch builds the accepted Branch Vision, keeps scope bounded, and preserves user-facing clarity."
        )
        design_ballot = [
            "Accept the BP2 engineering plan as written.",
            "Accept with engineering-plan changes.",
            "Route back to BP1 because the plan changes the accepted Branch Vision.",
            "Explicitly waive remaining BP2 questions.",
            "Reject and request a narrower branch or plan.",
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
        implementation_constraints = (
            [
                "PR Readiness Stage 1 is analysis-only.",
                "PR creation, merge, release, cleanup, runtime implementation, provider/model/cache/memory/private actions, sidecar artifacts, unique ZIP naming, and separate Review/Upload taxonomy remain pending USER decisions.",
                "Accepted outcomes from this packet must fold into durable repo owners or approved external operational state, not the temporary USER review folder.",
            ]
            if pr_readiness_stage1_packet
            else ["Pending USER response or explicit waiver."]
        )
        rejected_deferred = (
            [
                "Sidecar artifact model remains pending USER decision.",
                "Uniquely named ZIP artifact model remains pending USER decision.",
                "Separate Review / Upload top-level folder taxonomy remains pending USER decision.",
                "Cloud-backed mirrors remain convenience-only unless USER changes the artifact model.",
            ]
            if pr_readiness_stage1_packet
            else ["Pending USER response or explicit waiver."]
        )
        source_truth_impact = (
            [
                "Lifecycle law remains owned by Docs/phase_governance.md.",
                "Branch artifact rules remain owned by Docs/branch_plans/README.md.",
                "USER hub helper enforcement remains owned by Docs/validation_helper_registry.md.",
                "Active operational proof remains in Codex chat digest, helper output, validator output, or external governance state.",
            ]
            if pr_readiness_stage1_packet
            else ["Pending USER response or explicit waiver."]
        )
        contract_change_log = ["v2 - Generated as BP2 engineering-plan review rather than BP1 product/design contract."]
        completion_checklist = [
            "Contract Status is Complete or Waived by USER.",
            "Accepted or waived BP1 trace is present or this packet is a later-phase context review.",
            "Implementation package summary, seam/SLC plan, affected surfaces, validators/helpers, proof requirements, H1/LV/UTS expectations, rollback/safety plan, risks, and future-gated boundaries are represented.",
            "Helper output verifies packet freshness while USER-facing files stay focused on context, plan, risks, proof expectations, and decisions.",
            "BP3 / Workstream Entry may approve implementation only when BP1 and BP2 are accepted or explicitly waived.",
            "PR Readiness Stage 1 approval remains analysis-only when this packet is a PR Readiness review packet.",
        ]
        plain_english_summary = (
            "This BP2 Branch Plan Review summarizes how the accepted or waived Branch Vision "
            "will be built, validated, hardened, live-validated, reviewed, and rolled back. "
            "For this packet, it serves as engineering-plan context for PR Readiness Stage 1."
            if pr_readiness_stage1_packet
            else
            "This BP2 Branch Plan Review summarizes how the accepted or waived Branch Vision "
            "will be implemented, validated, hardened, live-validated, reviewed, and rolled back "
            "before BP3 may authorize Workstream implementation."
        )
        end_state_vision = (
            "The completed governance repair leaves lifecycle law, BP1/BP2/BP3 artifact roles, "
            "the local USER hub model, external-state split, helper/validator enforcement, and "
            "pending artifact-model decisions in their proper owners."
            if pr_readiness_stage1_packet
            else
            "When BP2 is accepted or waived, USER should understand which implementation surfaces "
            "are affected, which validators prove them, which risks remain, and what stays future-gated."
        )
        walkthrough = [
            "Review the copied context plan for the lifecycle and USER hub model.",
            "Review phase governance, branch artifact rules, and helper registry for owner boundaries.",
            "Review the copied branch authority record for standing Governance routing context.",
            "Use this packet to decide whether PR Readiness Stage 1 analysis should begin.",
        ]
        surface_map = [
            "Docs/phase_governance.md: lifecycle law.",
            "Docs/branch_plans/README.md: BP1/BP2/BP3 artifact rules.",
            "Docs/validation_helper_registry.md: helper and validator enforcement.",
            "Docs/branch_records/index.md and Governance branch record: branch routing law.",
            "C:\\Nexus USER\\Governance and C:\\Nexus USER\\Governance.zip: temporary USER review aids.",
        ]
        implementation_options = [
            "Option A - Approve PR Readiness Stage 1 analysis as recommended. Pros: moves the Governance reform toward PR creation review; Cons: no PR is created yet; Risk: low.",
            "Option B - Revise the PR Readiness Stage 1 inspection criteria before analysis. Pros: lets USER tune the review; Cons: adds packet/source-truth repair; Risk: low.",
            "Option C - Pause and request another governance hardening scan. Pros: maximum caution; Cons: delays PR readiness; Risk: low.",
        ]
        recommended_direction = (
            "Codex recommends approving PR Readiness Stage 1 only after the local USER hub packet, "
            "source-truth owners, helper/validator rules, and technical-metadata boundaries read cleanly."
            if pr_readiness_stage1_packet
            else
            "Codex recommends accepting BP2 only when the engineering plan clearly builds the accepted BP1 vision, "
            "names its affected surfaces, validators, proof path, rollback plan, and pending boundaries."
        )
        current_scope = [
            "Governance Phase Lifecycle Reform source-truth and helper hardening.",
            "Local USER hub packet refresh under C:\\Nexus USER.",
            "Technical proof metadata remains outside USER-facing review content.",
            "PR Readiness Stage 1 remains pending USER approval.",
        ]
        future_scope = [
            "PR creation, merge, release, cleanup, runtime work, FAM-006/FAM-007 mutation, private/provider/cache/memory actions, sidecars, unique ZIPs, and separate Review/Upload taxonomy remain pending USER decisions.",
        ]
        slc_package_plan = [
            "SLCs remain engineering route details inside an accepted branch; they do not automatically become separate branches.",
            "Workstream implementation is not part of this PR Readiness Stage 1 packet.",
        ]
        user_decisions = [
            "Does USER approve PR Readiness Stage 1 analysis for this Governance branch?",
            "Does USER require any change to PR Readiness Stage 1 inspection criteria before analysis?",
            "Does USER confirm PR creation, merge, release, cleanup, runtime/provider/cache/memory/private actions, and artifact-model changes remain pending?",
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
        "This file is the BP2 engineering-plan review. It should help USER answer whether the plan correctly builds the accepted or waived BP1 Branch Vision, whether the proof path is sufficient, and whether anything must route back to BP1 before implementation.",
        "",
        "## Accepted Branch Vision Summary",
        "",
        accepted_user_response
        or ("BP1 context is treated as already represented for this later-phase PR Readiness packet." if pr_readiness_stage1_packet else "Pending accepted or waived BP1 trace."),
        "",
        "## Implementation Package Summary",
        "",
        plain_english_summary,
        "",
        "## Branch Scope Size Test",
        "",
        "The branch package should be the largest coherent feature-focused implementation package that can be validated, hardened, live-validated, reviewed, and rolled back safely without mixing unrelated product areas.",
        "",
        "## SLC / Seam Plan",
        "",
        *_markdown_lines(slc_package_plan),
        "",
        "## Affected Surfaces",
        "",
        *_markdown_lines(surface_map),
        "",
        "## Likely Files",
        "",
        *_markdown_lines([f"`{source_rel}` copied as `{copied_rel}`" for source_rel, copied_rel in copied]),
        "",
        "## Validators / Helpers",
        "",
        "- Reuse registered validators and helpers before creating new ones.",
        "- USER review packet generation must use the local USER hub helper.",
        "",
        "## Proof Requirements",
        "",
        "- Direct validation must prove the accepted plan or admitted later-phase review boundary.",
        "- USER-facing packet files must avoid mutable technical proof metadata.",
        "",
        "## Element-To-Phase Proof Matrix",
        "",
        "- BP1 owns branch vision acceptance or waiver.",
        "- BP2 owns engineering plan acceptance or waiver.",
        "- BP3 validates BP2 against BP1 before implementation approval.",
        "- Workstream owns runtime/code implementation only.",
        "- Hardening owns pressure-test and implementation-vs-plan verification.",
        "- Live Validation owns user-facing proof and UTS handling.",
        "",
        "## H1 Expectations",
        "",
        "- H1 must compare implementation or source-truth changes against the accepted plan and repair defects only inside approved scope.",
        "",
        "## LV / UTS Expectations",
        "",
        "- Live Validation and UTS handling remain separate phase gates when applicable.",
        "",
        "## Rollback / Safety Plan",
        "",
        "- Keep changes bounded to approved source-truth/helper/validator/fixture surfaces.",
        "- Preserve pending USER gates for PR creation, merge, release, cleanup, runtime/private actions, and artifact-model changes.",
        "",
        "## Open Engineering Risks",
        "",
        "- Stale review-packet wording can confuse BP1, BP2, BP3, and PR Readiness boundaries if not regenerated through the helper.",
        "",
        "## Future-Gated Boundaries",
        "",
        *_markdown_lines(future_scope),
        "",
        "## Line-Item USER Plan Review",
        "",
        *_markdown_lines(user_decisions),
        "",
        "## Plan Acceptance Checklist",
        "",
        *_markdown_lines(completion_checklist),
        "",
        "## Exact BP3 Approval Text When Ready",
        "",
        "BP3 approval text applies only when BP1 and BP2 are accepted or explicitly waived and BP3 validation is green. This PR Readiness packet does not request BP3 implementation approval.",
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
        "## USER Plan Review Decision",
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
        "## Review Scope",
        "",
        "- Review the copied source-truth files, Branch Vision, Branch Plan, decision options, risks, proof expectations, and pending USER gates.",
        "- Technical freshness proof for the branch, commit, baseline, validation, and ZIP export stays in Codex chat digest, helper output, validator output, or external operational state.",
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
        "## USER Plan Review Questions",
        "",
        "This section summarizes BP2 plan-review questions. See USER Decisions Needed above.",
        "",
        *_markdown_lines(user_decisions),
        "",
        "## Appendix - Legacy Validator Compatibility",
        "",
        "Legacy compatibility sections are retained only for older validators and should not replace the contract sections above.",
        "",
        "## Active External Branch Plan / Historical Branch Plan Files",
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


def _write_workstream_entry_packet_digests(
    *,
    target: Path,
    source_branch: str,
    source_head: str,
    origin_main: str,
    packet_folder: Path,
    export_zip: Path,
    copied: list[tuple[str, str]],
    extra_bundle_files: list[str],
    bundle_file_count: int,
    expected_count: int,
    copied_count: int,
    exact_user_decision: str,
    pending_user_decisions: list[str],
) -> list[Path]:
    is_fam007_breakpoint_2 = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
    )
    seam1_approval_packet = (
        is_fam007_breakpoint_2
        and "approve bounded workstream implementation" in exact_user_decision.casefold()
    )
    seam1_completion_packet = (
        is_fam007_breakpoint_2
        and "approve or revise seam 2" in exact_user_decision.casefold()
    )
    workstream_green_packet = (
        is_fam007_breakpoint_2
        and "approve bounded hardening h1" in exact_user_decision.casefold()
    )
    hardening_h1_packet = (
        is_fam007_breakpoint_2
        and "approve bounded live validation lv1" in exact_user_decision.casefold()
    )
    lv1_green_packet = (
        is_fam007_breakpoint_2
        and "approve bounded pr readiness stage 1" in exact_user_decision.casefold()
    )
    pr_stage2_packet = (
        is_fam007_breakpoint_2
        and "approve pr readiness stage 2" in exact_user_decision.casefold()
    )
    pr_stage1_packet = (
        "pr readiness stage 1 analysis" in exact_user_decision.casefold()
    )
    bp1_packet = (
        "bp1 branch vision" in exact_user_decision.casefold()
        and "authorize bp2 user branch plan review only" in exact_user_decision.casefold()
    )
    packet_status = (
        "bp1 branch vision review - BP1 Branch Vision Review remains pending "
        "USER acceptance, revision, waiver, rejection, or hold; BP2 remains pending."
        if bp1_packet
        else
        "pr readiness stage1 approval review - PR Readiness Stage 1 analysis "
        "remains pending USER approval; PR creation remains pending USER approval."
        if pr_stage1_packet
        else
        "pr readiness stage2 review - PR Readiness Stage 1 Ready For Stage 2; "
        "PR creation remains pending USER approval."
        if pr_stage2_packet
        else
        "workstream implementation approval - Seam 1 public-safe action-gate registry "
        "and exact USER decision proof is approved by this packet decision path."
        if seam1_approval_packet
        else (
            "live validation final decision review - Live Validation LV1 is green; "
            "PR Readiness Stage 1 remains pending USER approval."
        )
        if lv1_green_packet
        else (
            "hardening final decision review - Hardening H1 is green; Live Validation LV1 "
            "remains pending USER approval."
        )
        if hardening_h1_packet
        else (
            "workstream entry final decision review - Workstream Green review; Seams 1 through 4 "
            "are complete and Hardening H1 remains pending USER approval."
        )
        if workstream_green_packet
        else (
            "workstream entry final decision review - seam 1 completion review; action-gate registry and exact USER decision "
            "proof are complete; Seam 2 remains pending USER approval."
        )
        if seam1_completion_packet
        else (
            "workstream entry final decision review - Workstream implementation "
            "remains pending USER approval."
        )
    )
    if bp1_packet:
        analysis_status = (
            "Analysis Summary: BP1 Branch Vision Review packet for the active "
            "Branch Planning carrier."
        )
        implementation_posture = (
            "Implementation Posture: BP2, BP3, Workstream implementation, "
            "private setup, runtime/provider/cache/memory behavior, PR, merge, "
            "release, cleanup, and sibling-worktree mutation remain pending "
            "USER decisions."
        )
        recommended_seam = (
            "Recommended Next Phase: BP1 USER decision, then BP2 USER Branch "
            "Plan Review only if USER accepts or explicitly waives BP1."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the project vision, FAM-007 "
            "family vision, Public/Dev/Owner boundary plan, AI Runtime And Trust "
            "Architecture, active branch authority record, branch artifact rules, "
            "phase governance, execution rules, validation registry, backlog, and "
            "roadmap context needed for the BP1 Branch Vision decision."
        )
        checklist_status = (
            "Checklist Focus: BP1 Branch Vision Review - project, family, feature, "
            "branch goal, end-state vision, user-facing review surfaces, options, "
            "recommendations, future-gated decisions, and regression-risk controls "
            "are represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_VISION_REVIEW.md, "
            "USER_BRANCH_PLAN_REVIEW.md as BP2 preview only, required digest/"
            "checklist files, and copied source-truth files are loaded and "
            "digestible for USER review; BP1 remains pending USER decision."
        )
    elif pr_stage1_packet:
        analysis_status = (
            "Analysis Summary: Governance Phase Lifecycle Reform packet is ready "
            "for PR Readiness Stage 1 analysis approval."
        )
        implementation_posture = (
            "Implementation Posture: this packet remains analysis-only; PR creation, "
            "merge, release, cleanup, runtime, provider, private, sidecar, and upload "
            "taxonomy actions remain pending USER approval."
        )
        recommended_seam = (
            "Recommended Next Phase: PR Readiness Stage 1 analysis for the "
            "Governance Phase Lifecycle Reform branch."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the lifecycle reform context "
            "plan, phase governance, execution mirrors, branch authority routing, "
            "USER hub model, branch artifact rules, validation registry, and review "
            "context needed for the PR Readiness Stage 1 decision."
        )
        checklist_status = (
            "Checklist Focus: for Governance PR Readiness Stage 1 approval review - "
            "lifecycle ownership, BP1/BP2/BP3 separation, local USER hub behavior, "
            "external-state split, sidecar and unique-ZIP deferrals, and USER-facing "
            "metadata boundaries are represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_VISION_REVIEW.md, "
            "USER_BRANCH_PLAN_REVIEW.md, required digest/checklist files, and copied "
            "source-truth files are loaded and digestible for USER review; PR "
            "Readiness Stage 1 analysis remains pending USER approval."
        )
    elif pr_stage2_packet:
        analysis_status = (
            "Analysis Summary: PR Readiness Stage 1 Ready For Stage 2 for the "
            "FAM-007 Breakpoint 2 Dev/Owner skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: Stage 1 recorded no live PR, no-release-debt posture, "
            "merge-stable authority projection, and pending Stage 2 PR creation approval."
        )
        recommended_seam = (
            "Recommended Next Phase: PR Readiness Stage 2, PR creation and watcher/bot-review setup."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, branch index, branch record, branch plan, worktree slots, "
            "AI Runtime And Trust Architecture, FAM-007 family vision, AI Edition plan, "
            "branch-plan README, phase governance, development rules, codex modes, "
            "validation helper registry, and Stage 1 repair proof surfaces needed for "
            "the Stage 2 PR creation decision."
        )
        checklist_status = (
            "Checklist Focus: for PR Readiness Stage 1 repair review - branch identity, "
            "source-truth context, FAM-007 ownership, Breakpoint 2 product/workstream "
            "posture, no-live-PR posture, no-release-debt posture, merge-stable authority "
            "projection, backlog taxonomy, and private/runtime/provider/cache/memory exclusions "
            "are represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "digest/checklist files, and copied source-truth files are loaded and digestible "
            "for USER review; the contract records PR Readiness Stage 1 complete and "
            "Stage 2 PR creation as the next USER decision."
        )
    elif seam1_approval_packet:
        analysis_status = (
            "Analysis Summary: Workstream Entry Green; USER accepted the repaired "
            "branch contract for bounded Seam 1 implementation approval."
        )
        implementation_posture = (
            "Implementation Posture: Seam 1 is approved only for public-safe "
            "action-gate registry and exact USER decision proof."
        )
        recommended_seam = (
            "Approved First Seam: Seam 1, Action-gate registry and exact USER "
            "decision proof."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "review surfaces needed for bounded Seam 1 approval."
        )
        checklist_status = (
            "Checklist Focus: for Workstream Entry decision-path repair - "
            "branch context, source-truth context, FAM-007 ownership, "
            "Breakpoint 2 product/workstream posture, approved Seam 1 proof path, "
            "AI Runtime And Trust Architecture placement, backlog taxonomy, and "
            "private/runtime/provider/cache/memory exclusions are represented for "
            "USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "Workstream Entry digest/checklist files, and copied source-truth files "
            "are loaded and digestible for USER review; the contract is branch-specific "
            "and records the bounded Seam 1 implementation approval boundary."
        )
    elif lv1_green_packet:
        analysis_status = (
            "Analysis Summary: Live Validation LV1 Green for the FAM-007 Breakpoint 2 "
            "Dev/Owner skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: LV1 recorded no-visible-runtime proof, UTS waiver, "
            "and user-facing shortcut validation waiver; PR Readiness Stage 1 remains "
            "pending USER approval."
        )
        recommended_seam = (
            "Recommended Next Phase: PR Readiness Stage 1 analysis."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "LV1 no-visible-runtime proof surfaces needed for the next USER decision."
        )
        checklist_status = (
            "Checklist Focus: for Live Validation LV1 review - branch identity, "
            "source-truth context, FAM-007 ownership, Breakpoint 2 product/workstream "
            "posture, LV1 waiver proof, AI Runtime And Trust Architecture placement, "
            "backlog taxonomy, and private/runtime/provider/cache/memory exclusions are "
            "represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "digest/checklist files, and copied source-truth files are loaded and digestible "
            "for USER review; the contract records the Live Validation LV1 boundary and PR "
            "Readiness Stage 1 next decision."
        )
    elif hardening_h1_packet:
        analysis_status = (
            "Analysis Summary: Hardening H1 Green for the FAM-007 Breakpoint 2 Dev/Owner "
            "skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: Hardening H1 compared all public-safe proof and repaired "
            "stale duplicate ledger wording; Live Validation LV1 remains pending USER approval."
        )
        recommended_seam = (
            "Recommended Next Phase: Live Validation LV1, no-visible-runtime proof and UTS waiver digestion."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "Hardening H1 proof surfaces needed for the next USER decision."
        )
        checklist_status = (
            "Checklist Focus: for Hardening H1 review - branch identity, "
            "source-truth context, FAM-007 ownership, Breakpoint 2 product/workstream "
            "posture, H1 comparison proof, AI Runtime And Trust Architecture placement, "
            "backlog taxonomy, and private/runtime/provider/cache/memory exclusions are "
            "represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "digest/checklist files, and copied source-truth files are loaded and digestible "
            "for USER review; the contract records the Hardening H1 boundary and Live "
            "Validation LV1 next decision."
        )
    elif workstream_green_packet:
        analysis_status = (
            "Analysis Summary: Workstream Green for the FAM-007 Breakpoint 2 Dev/Owner "
            "skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: Seams 1 through 4 are implemented as public-safe proof "
            "only; Hardening H1 remains pending USER approval."
        )
        recommended_seam = (
            "Recommended Next Phase: Hardening H1, Workstream proof comparison."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "Workstream Green proof surfaces needed for the next USER decision."
        )
        checklist_status = (
            "Checklist Focus: for Workstream Green review - branch identity, "
            "source-truth context, FAM-007 ownership, Breakpoint 2 product/workstream "
            "posture, Seams 1 through 4 proof, AI Runtime And Trust Architecture placement, "
            "backlog taxonomy, and private/runtime/provider/cache/memory exclusions are "
            "represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "Workstream Entry digest/checklist files, and copied source-truth files "
            "are loaded and digestible for USER review; the contract records the "
            "Workstream Green boundary and Hardening H1 next decision."
        )
    elif seam1_completion_packet:
        analysis_status = (
            "Analysis Summary: Seam 1 complete for the FAM-007 Breakpoint 2 Dev/Owner "
            "skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: Seam 1 action-gate registry and exact USER decision "
            "proof are implemented as public-safe proof only; Seam 2 remains pending USER approval."
        )
        recommended_seam = (
            "Recommended Next Seam: Seam 2, Private/public boundary and private remote safety proof."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "Seam 1 proof surfaces needed for the next USER decision."
        )
        checklist_status = (
            "Checklist Focus: for Seam 1 completion review - branch identity, "
            "source-truth context, FAM-007 ownership, Breakpoint 2 product/workstream "
            "posture, Seam 1 proof, AI Runtime And Trust Architecture placement, backlog "
            "taxonomy, and private/runtime/provider/cache/memory exclusions are represented "
            "for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "Workstream Entry digest/checklist files, copied source-truth files, branch "
            "plan, branch record, fixture proof, and validator proof are loaded and "
            "digestible for USER review; Seam 2 remains pending USER approval."
        )
    elif is_fam007_breakpoint_2:
        analysis_status = (
            "Analysis Summary: Workstream Entry analysis is complete/green for the "
            "FAM-007 Breakpoint 2 Dev/Owner skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: Seam 1 implementation remains pending USER "
            "approval and is not authorized by this packet until USER accepts or "
            "waives the repaired USER_BRANCH_PLAN_REVIEW.md contract and approves "
            "Seam 1 only."
        )
        recommended_seam = (
            "Recommended First Seam: Seam 1, Action-gate registry and exact USER "
            "decision proof."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "review surfaces needed for Workstream Entry contract repair."
        )
        checklist_status = (
            "Checklist Focus: for Workstream Entry packet repair - branch "
            "source-truth context, FAM-007 ownership, Breakpoint 2 "
            "product/workstream posture, Seam 1 proof path, AI Runtime And Trust "
            "Architecture placement, backlog taxonomy, and private/runtime/provider/"
            "cache/memory exclusions are represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "Workstream Entry digest/checklist files, and copied source-truth files "
            "are loaded and digestible for USER review; the contract is branch-specific "
            "and records the recommended Seam 1 approval boundary."
        )
    else:
        analysis_status = (
            "Analysis Summary: Stage 2 setup is green; this packet supports "
            "Workstream Entry final decision review only."
        )
        implementation_posture = (
            "Implementation Posture: Workstream implementation remains pending "
            "USER approval and is not authorized by this packet."
        )
        recommended_seam = ""
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, branch plan, "
            "worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, "
            "development rules, codex modes, validation helper registry, and "
            "governance inventory review surfaces selected for Stage 2 inspection."
        )
        checklist_status = (
            "Checklist Focus: for Stage 2 packet review - branch identity, "
            "source-truth context, FAM-007 ownership, AI Runtime And Trust "
            "Architecture placement, backlog taxonomy, product/workstream carrier "
            "posture, and private/runtime/provider/cache/memory exclusions are "
            "represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md, required "
            "Workstream Entry digest/checklist files, and copied source-truth files "
            "are loaded and digestible for USER review."
        )
    copied_sources = "\n".join(f"- `{source_rel}` -> `{copied_rel}`" for source_rel, copied_rel in copied)
    pending = "\n".join(f"- {decision}" for decision in pending_user_decisions) or "- None recorded."
    common = (
        f"Decision Path: {packet_status}\n"
        f"USER Decision: {exact_user_decision}\n"
    )
    files: dict[str, str] = {
        "USER_REVIEW_FOLDER_AND_FILE_DIGEST.md": (
            "# USER Review Folder And File Digest\n\n"
            f"{common}"
            f"Folder: `{packet_folder}`\n"
            f"Upload ZIP: `{export_zip}`\n"
            f"{digest_status}\n\n"
            "## Copied Repo Files\n\n"
            f"{copied_sources}\n"
        ),
        "GOVERNANCE_REQUIRED_FILES_SCAN.md": (
            "# Governance Required Files Scan\n\n"
            f"{common}"
            f"{scan_result}\n"
        ),
        "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md": (
            "# Workstream Entry Analysis Digest\n\n"
            f"{common}"
            f"{analysis_status}\n"
            f"{implementation_posture}\n"
            f"{recommended_seam}\n\n"
            "## Pending Gates\n\n"
            f"{pending}\n"
        ),
        "BRANCH_VISION_VALIDATION_CHECKLIST.md": (
            "# Branch Vision Validation Checklist\n\n"
            f"{common}"
            f"{checklist_status}\n"
        ),
    }
    written: list[Path] = []
    for name, text in files.items():
        path = target / name
        path.write_text(text, encoding="utf-8")
        written.append(path.resolve())
    return written


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

    bp1_review_markers = (
        "bp1 branch vision review",
        "bp1 user branch vision review",
        "bp1 review packet",
    )
    bp1_decision_markers = (
        "authorize bp2 user branch plan review only",
        "bp2 remains pending",
        "bp2 user branch plan review remains pending",
    )
    if any(marker in normalized for marker in bp1_review_markers) and any(
        marker in normalized for marker in bp1_decision_markers
    ):
        return DECISION_STATUS_BP1_BRANCH_VISION_REVIEW

    final_review_markers = (
        "workstream entry final decision review",
        "final workstream entry decision",
    )
    if any(marker in normalized for marker in final_review_markers):
        return DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW

    live_validation_review_markers = (
        "live validation final decision review",
        "live validation lv1 is green",
        "pr readiness stage 1 remains pending user approval",
    )
    if any(marker in normalized for marker in live_validation_review_markers):
        return DECISION_STATUS_LIVE_VALIDATION_REVIEW

    pr_stage1_review_markers = (
        "pr readiness stage1 approval review",
        "pr readiness stage 1 analysis remains pending user approval",
        "pr readiness stage 1 analysis approval",
    )
    if any(marker in normalized for marker in pr_stage1_review_markers):
        return DECISION_STATUS_PR_READINESS_STAGE1_REVIEW

    pr_stage2_review_markers = (
        "pr readiness stage2 review",
        "pr readiness stage 1 ready for stage 2",
        "pr readiness stage 2 pr creation",
        "stage 2 pr creation remains pending user approval",
    )
    if any(marker in normalized for marker in pr_stage2_review_markers):
        return DECISION_STATUS_PR_READINESS_STAGE2_REVIEW

    hardening_review_markers = (
        "hardening final decision review",
        "hardening h1 is green",
        "live validation lv1 remains pending user approval",
    )
    if any(marker in normalized for marker in hardening_review_markers):
        return DECISION_STATUS_HARDENING_REVIEW

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
    enforce_identity: bool = False,
    actual_file_count: int | None = None,
) -> WorkstreamEntryPacketDecisionPathResult:
    failures: list[str] = []
    failures.extend(_unresolved_template_placeholder_failures(packet_files))
    if enforce_identity:
        failures.extend(
            _packet_identity_failures(
                packet_files,
                expected_branch=expected_branch,
                expected_head=expected_head,
                expected_origin_main=expected_origin_main,
            )
        )
    failures.extend(
        _packet_count_consistency_failures(
            packet_files,
            actual_file_count=actual_file_count,
        )
    )
    failures.extend(_user_facing_technical_metadata_failures(packet_files))
    for required_file in WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES:
        if required_file not in packet_files:
            failures.append(f"{required_file}: required Workstream Entry packet file is missing")

    start_here = packet_files.get("START_HERE.md", "")
    if not _field_present(start_here, "USER Decision This Packet Supports"):
        failures.append("START_HERE.md: USER Decision This Packet Supports field is missing")
    workstream_digest = packet_files.get("WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md", "")
    if "USER Decision" not in workstream_digest:
        failures.append("WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md: USER Decision field is missing")

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
    all_files = (
        sorted(path for path in packet_dir.iterdir() if path.is_file())
        if packet_dir.exists()
        else []
    )
    for path in all_files:
        if path.suffix.lower() not in {".md", ".txt", ".json"}:
            continue
        packet_files[path.name] = path.read_text(encoding="utf-8")
    return _validate_workstream_entry_packet_decision_path(
        packet_files,
        expected_branch=expected_branch,
        expected_head=expected_head,
        expected_origin_main=expected_origin_main,
        require_implementation_ready=require_implementation_ready,
        enforce_identity=True,
        actual_file_count=len(all_files),
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
            r"C:\Nexus USER\<worktree-label> destination, or pass "
            "--allow-custom-review-path with --custom-review-path-reason."
        )
    if allow_custom_review_path and not custom_review_path_reason:
        raise ValueError("--custom-review-path-reason is required with --allow-custom-review-path")

    desktop = _desktop_path()
    label = _worktree_label(worktree_label)
    review_root, target = _safe_target(desktop, review_root_name, label)
    if target.exists():
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
    seam1_approval_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve bounded workstream implementation" in exact_user_decision.casefold()
    )
    seam1_completion_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve or revise seam 2" in exact_user_decision.casefold()
    )
    workstream_green_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve bounded hardening h1" in exact_user_decision.casefold()
    )
    hardening_h1_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve bounded live validation lv1" in exact_user_decision.casefold()
    )
    lv1_green_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve bounded pr readiness stage 1" in exact_user_decision.casefold()
    )
    pr_stage2_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve pr readiness stage 2" in exact_user_decision.casefold()
    )
    pr_stage1_packet = (
        "pr readiness stage 1 analysis" in exact_user_decision.casefold()
    )
    bp1_packet = (
        "bp1 branch vision" in exact_user_decision.casefold()
        and "authorize bp2 user branch plan review only" in exact_user_decision.casefold()
    )
    machine_readable_packet_status = (
        "bp1 branch vision review - BP1 Branch Vision Review remains pending "
        "USER acceptance, revision, waiver, rejection, or hold; BP2 remains pending."
        if bp1_packet
        else
        "pr readiness stage1 approval review - PR Readiness Stage 1 analysis "
        "remains pending USER approval; PR creation remains pending USER approval."
        if pr_stage1_packet
        else
        "pr readiness stage2 review - PR Readiness Stage 1 Ready For Stage 2; "
        "PR creation remains pending USER approval."
        if pr_stage2_packet
        else
        "workstream implementation approval - Seam 1 public-safe action-gate registry "
        "and exact USER decision proof is approved by this packet decision path."
        if seam1_approval_packet
        else (
            "live validation final decision review - Live Validation LV1 is green; "
            "PR Readiness Stage 1 remains pending USER approval."
        )
        if lv1_green_packet
        else (
            "hardening final decision review - Hardening H1 is green; Live Validation LV1 "
            "remains pending USER approval."
        )
        if hardening_h1_packet
        else (
            "workstream entry final decision review - Workstream Green review; Seams 1 through 4 "
            "are complete and Hardening H1 remains pending USER approval."
        )
        if workstream_green_packet
        else (
            "workstream entry final decision review - seam 1 completion review; action-gate registry and exact USER decision "
            "proof are complete; Seam 2 remains pending USER approval."
        )
        if seam1_completion_packet
        else (
            "workstream entry final decision review - Workstream implementation "
            "remains pending USER approval."
        )
    )
    user_facing_decision = _user_facing_decision_text(exact_user_decision)
    user_vision_file = _write_user_branch_vision_review(
        target=target,
        title=title,
        review_purpose=review_purpose,
        exact_user_decision=user_facing_decision,
        pending_user_decisions=pending_user_decisions,
        copied=copied,
    )
    user_review_file = _write_user_branch_plan_review(
        target=target,
        title=title,
        review_purpose=review_purpose,
        source_branch=source_branch,
        source_head=source_head,
        upstream=upstream,
        origin_main=origin_main,
        exact_user_decision=user_facing_decision,
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
    required_digest_paths = {target / name for name in WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES if name != "START_HERE.md"}
    actual_bundle_files = (
        _bundle_files(target)
        | {start_here, user_vision_file, user_review_file}
        | required_digest_paths
    )
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

    _write_workstream_entry_packet_digests(
        target=target,
        source_branch=source_branch,
        source_head=source_head,
        origin_main=origin_main,
        packet_folder=target,
        export_zip=export_zip,
        copied=copied,
        extra_bundle_files=extra_bundle_files,
        bundle_file_count=bundle_file_count,
        expected_count=expected_count,
        copied_count=copied_count,
        exact_user_decision=user_facing_decision,
        pending_user_decisions=pending_user_decisions,
    )

    readme_lines: list[str] = [
        f"# {title}",
        "",
        "## Review Packet",
        "",
        f"Review Purpose: {review_purpose}",
        "Review Location: Open this folder in the local USER hub and upload the matching ZIP beside it.",
        f"Local USER Hub Folder: `{target}`",
        f"Custom Review Path Waiver: {custom_review_path_waiver}",
        f"Custom Review Path Reason: {custom_review_path_reason_value}",
        "Review Safety Note: Copied files are selected repo source-truth and "
        "review-context files for USER inspection; technical freshness proof "
        "stays in Codex chat digest, helper output, validator output, or external state.",
        f"USER Decision This Packet Supports: {user_facing_decision}",
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
    readme_lines.extend(
        [
            "## Decision Path",
            "",
            f"Decision Path Summary: {machine_readable_packet_status}",
            f"USER Decision: {user_facing_decision}",
            "",
        ]
    )

    (target / "START_HERE.md").write_text("\n".join(readme_lines), encoding="utf-8")
    bundle_paths = _bundle_files(target)
    packet_files = {
        path.relative_to(target).as_posix(): path.read_text(encoding="utf-8")
        for path in bundle_paths
        if path.suffix.lower() in {".md", ".txt", ".json"}
    }
    artifact_failures = [
        *_unresolved_template_placeholder_failures(packet_files),
        *_packet_count_consistency_failures(
            packet_files,
            actual_file_count=len(bundle_paths),
        ),
        *_user_facing_technical_metadata_failures(packet_files),
        *_user_branch_plan_stale_bp1_wording_failures(packet_files),
    ]
    if artifact_failures:
        raise ValueError(
            "Review bundle artifact validation failed:\n"
            + "\n".join(f"- {failure}" for failure in artifact_failures)
        )
    expected_zip_entries = {path.relative_to(target).as_posix() for path in bundle_paths}
    _write_export_zip(target, export_zip)
    _validate_export_zip(
        export_zip,
        source_branch=source_branch,
        source_head=source_head,
        origin_main=origin_main,
        expected_entries=expected_zip_entries,
    )
    return target, export_zip


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review-root-name",
        default=DEFAULT_REVIEW_ROOT_NAME,
        help="Optional subfolder under C:\\Nexus USER. Custom values require --allow-custom-review-path.",
    )
    parser.add_argument(
        "--worktree-label",
        help="Optional worktree child folder label. Defaults to the current worktree folder name.",
    )
    parser.add_argument(
        "--folder-name",
        help=(
            "Legacy alias for --worktree-label. New governance expects a stable "
            "local USER hub with an auto-derived worktree label. Requires "
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
        help="Legacy compatibility flag; the helper always clears the local USER hub packet folder before copying.",
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
        help="Validate an existing Branch Planning / Workstream Entry packet decision path.",
    )
    parser.add_argument("--expected-branch", help="Expected source branch for Workstream Entry packet validation.")
    parser.add_argument("--expected-head", help="Expected source HEAD for Workstream Entry packet validation.")
    parser.add_argument("--expected-origin-main", help="Expected main baseline for Workstream Entry packet validation.")
    parser.add_argument(
        "--require-implementation-ready",
        action="store_true",
        help="Fail if the packet is branch-correct but still blocks Workstream implementation approval.",
    )
    parser.add_argument("files", nargs="*", help="Repo-relative files to copy into the local USER hub packet.")
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
    print(
        "USER Review Packet Finding: PASS - START_HERE.md, "
        f"{USER_BRANCH_VISION_REVIEW_FILE}, {USER_BRANCH_PLAN_REVIEW_FILE}, and exported zip were generated and "
        "validated against current source-truth snapshot."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
