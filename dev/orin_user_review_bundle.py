# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing local review bundle from selected repo files.

This helper copies review files to a stable worktree-labeled folder under
``C:\\Nexus USER`` and creates a timestamped upload ZIP beside that folder so
each ChatGPT upload has a unique artifact name. Legacy same-name upload ZIPs
and previous same-label timestamped upload ZIPs are removed during generation.
It never edits repo files.
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
    "created a timestamped review zip from that refreshed folder after removing previous "
    "same-label upload zips."
)
USER_BRANCH_PLAN_REVIEW_FILE = "USER_BRANCH_PLAN_REVIEW.md"
USER_BRANCH_VISION_REVIEW_FILE = "USER_BRANCH_VISION_REVIEW.md"
USER_REVIEW_DIR_NAME = "USER Review"
REVIEW_AIDS_DIR_NAME = "Review Aids"
SOURCE_TRUTH_CONTEXT_DIR_NAME = "Source Truth Context"


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
DECISION_STATUS_BP2_BRANCH_PLAN_REVIEW = "bp2-branch-plan-review"
DECISION_STATUS_BP3_ORCHESTRATION_REVIEW = "bp3-orchestration-review"
DECISION_STATUS_WORKSTREAM_ENTRY_REVIEW = "workstream-entry-final-review"
DECISION_STATUS_HARDENING_REVIEW = "hardening-final-review"
DECISION_STATUS_LIVE_VALIDATION_REVIEW = "live-validation-final-review"
DECISION_STATUS_PR_READINESS_STAGE1_REVIEW = "pr-readiness-stage1-review"
DECISION_STATUS_PR_READINESS_STAGE2_REVIEW = "pr-readiness-stage2-review"
DECISION_STATUS_REPAIR_REVALIDATION = "repair-revalidation"
DECISION_STATUS_UNKNOWN = "unknown"
BRANCH_PLANNING_PACKET_REVIEWABILITY_VALUES = {
    "missing",
    "generated",
    "validation failed",
    "reviewable",
    "stale",
    "superseded",
}
BRANCH_PLANNING_USER_GATE_VALUES = {
    "pending user review",
    "user revision requested",
    "user accepted",
    "user approved",
    "user waived",
    "user rejected",
    "user blocked",
    "superseded",
}
BRANCH_PLANNING_PENDING_USER_GATE_VALUES = {
    "pending user review",
    "user revision requested",
    "user rejected",
    "user blocked",
}
BRANCH_PLANNING_IMPLEMENTATION_REQUEST_MARKERS = (
    "approve bounded workstream package implementation",
    "approve bounded workstream implementation",
    "bounded workstream package implementation",
    "workstream package implementation approval",
    "approve workstream implementation",
    "workstream implementation approval",
    "implementation approval",
)
BRANCH_PLANNING_IMPLEMENTATION_BLOCKING_MARKERS = (
    "implementation remains blocked",
    "implementation not yet authorized",
    "pending separate user approval",
    "pending user approval",
    "implementation approval state: pending",
    "does not authorize workstream implementation",
    "does not request bp3 implementation approval",
    "not a workstream implementation approval",
    "workstream implementation remains pending",
)
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
BP1_PACKET_STALE_LANGUAGE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "workstream-entry-final-decision-path",
        re.compile(r"workstream entry final decision review", re.IGNORECASE),
    ),
    (
        "bp1-compatibility-status",
        re.compile(r"BP1 Branch Vision Review compatibility status", re.IGNORECASE),
    ),
    (
        "compatibility-digest",
        re.compile(r"compatibility digest", re.IGNORECASE),
    ),
    (
        "must-not-do-heading",
        re.compile(r"##\s*Must-Not-Do\s*/\s*Regression-Risk Rules", re.IGNORECASE),
    ),
    (
        "command-wall-do-not-bullet",
        re.compile(r"^\s*-\s*Do not\b", re.IGNORECASE | re.MULTILINE),
    ),
)
USER_BRANCH_VISION_TEMPLATE_SHELL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "project-context-process-shell",
        re.compile(r"must explain how this branch supports", re.IGNORECASE),
    ),
    (
        "family-context-process-shell",
        re.compile(r"asks whether", re.IGNORECASE),
    ),
    (
        "project-context-instruction",
        re.compile(r"Review `Docs/nexus_vision\.md`.*before accepting this Branch Vision", re.IGNORECASE),
    ),
    (
        "family-context-instruction",
        re.compile(r"Review the relevant `Docs/family_visions/` owner", re.IGNORECASE),
    ),
    (
        "generic-branch-goal-instruction",
        re.compile(r"Confirm that this branch goal is the right product direction", re.IGNORECASE),
    ),
    (
        "generic-end-state-instruction",
        re.compile(r"Describe the intended user-visible or source-truth end state", re.IGNORECASE),
    ),
    (
        "generic-copied-file-flow",
        re.compile(r"Review the copied branch-specific files and note any changes", re.IGNORECASE),
    ),
    (
        "generic-accept-revise-waive-reject-options",
        re.compile(
            r"Accept the proposed Branch Vision.*Revise the Branch Vision.*Waive BP1.*Reject this branch direction",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "generic-design-question",
        re.compile(r"Does this Branch Vision match what the USER wants this branch to become", re.IGNORECASE),
    ),
    (
        "process-only-accepted-vision-goal",
        re.compile(r"Create an accepted USER-facing branch vision", re.IGNORECASE),
    ),
    (
        "process-only-bp1-closeout",
        re.compile(r"When BP1 closes", re.IGNORECASE),
    ),
    (
        "process-only-bp1-mechanics",
        re.compile(r"BP1 captures", re.IGNORECASE),
    ),
    (
        "process-only-product-options",
        re.compile(
            r"Option A accepts the vision.*option B revises it.*option C waives",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "process-only-packet-decision",
        re.compile(r"Use this packet to decide", re.IGNORECASE),
    ),
    (
        "generic-outcome-question",
        re.compile(r"what exact outcome should USER expect to see", re.IGNORECASE),
    ),
    (
        "process-centered-user-hub-packet",
        re.compile(r"USER will see a local USER hub packet", re.IGNORECASE),
    ),
    (
        "process-centered-accepted-bp1-target",
        re.compile(r"The accepted BP1 vision will become the target for BP2", re.IGNORECASE),
    ),
    (
        "process-centered-user-reads-packet",
        re.compile(r"USER reads the FAM-007 packet", re.IGNORECASE),
    ),
)
USER_BRANCH_VISION_MINIMUM_SUBSTANTIVE_SECTIONS: tuple[tuple[str, int], ...] = (
    ("Project Vision Context", 18),
    ("Family Vision Context", 18),
    ("Feature Vision Context", 18),
    ("Branch Goal", 18),
    ("End-State Vision", 20),
    ("What Will I Actually See, And Where Will I See It?", 18),
    ("How It Will Function", 20),
    ("User Experience Flow", 18),
    ("Surface Map", 24),
    ("Product Options / Design Paths", 30),
    ("Codex Recommendations", 36),
    ("Why This Fits The Nexus Vision", 18),
    ("USER Design Questions", 24),
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
            DECISION_STATUS_BP2_BRANCH_PLAN_REVIEW,
            DECISION_STATUS_BP3_ORCHESTRATION_REVIEW,
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


def _copy_file(
    relative_file: str,
    target: Path,
    copy_name: str,
    *,
    subdir: str | None = None,
) -> tuple[str, str]:
    source = (ROOT / relative_file).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Review source file not found: {relative_file}")
    if ROOT.resolve() not in source.parents:
        raise ValueError(f"Review source file is outside repo: {relative_file}")

    destination = target / subdir / copy_name if subdir else target / copy_name
    destination.parent.mkdir(parents=True, exist_ok=True)
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


def _packet_file_basename(file_name: str) -> str:
    return PurePosixPath(file_name.replace("\\", "/")).name


def _packet_file_items(
    packet_files: Mapping[str, str],
    file_name: str,
) -> list[tuple[str, str]]:
    return [
        (path, text)
        for path, text in sorted(packet_files.items())
        if _packet_file_basename(path) == file_name
    ]


def _packet_file_text(packet_files: Mapping[str, str], file_name: str) -> str:
    if file_name in packet_files:
        return packet_files[file_name]
    matches = _packet_file_items(packet_files, file_name)
    return matches[0][1] if matches else ""


def _packet_file_path(packet_files: Mapping[str, str], file_name: str) -> str:
    if file_name in packet_files:
        return file_name
    matches = _packet_file_items(packet_files, file_name)
    return matches[0][0] if matches else file_name


def _packet_file_present(packet_files: Mapping[str, str], file_name: str) -> bool:
    return bool(_packet_file_text(packet_files, file_name))


def _primary_user_review_file(exact_user_decision: str) -> str:
    normalized = re.sub(r"\s+", " ", exact_user_decision).casefold()
    stage_patterns = (
        (
            "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
            0,
            (
                r"\bbp3\b",
                r"\borchestration\b",
                r"\bworkstream entry\b",
                r"\bworkstream package implementation\b",
                r"\bbounded workstream package\b",
                r"\bworkstream implementation\b",
                r"\bimplementation approval\b",
            ),
        ),
        (USER_BRANCH_PLAN_REVIEW_FILE, 1, (r"\bbp2\b", r"\bbranch plan\b")),
        (USER_BRANCH_VISION_REVIEW_FILE, 2, (r"\bbp1\b", r"\bbranch vision\b")),
    )
    action_match = re.search(
        r"\b(?:approve|approves|approved|approval|green-light|greenlight)\b",
        normalized,
    )
    if action_match:
        action_text = normalized[action_match.start() :]
        requested_matches: list[tuple[int, int, str]] = []
        for file_name, priority, patterns in stage_patterns:
            for pattern in patterns:
                match = re.search(pattern, action_text)
                if match:
                    requested_matches.append((match.start(), priority, file_name))
        if requested_matches:
            return sorted(requested_matches)[0][2]

    matches: list[tuple[int, int, str]] = []
    for file_name, priority, patterns in stage_patterns:
        for pattern in patterns:
            match = re.search(pattern, normalized)
            if match:
                matches.append((match.start(), priority, file_name))
    if matches:
        return sorted(matches)[0][2]
    return USER_BRANCH_PLAN_REVIEW_FILE


def _move_primary_user_review_file(
    *,
    target: Path,
    review_aids_dir: Path,
    user_review_dir: Path,
    primary_file_name: str,
) -> Path:
    source = review_aids_dir / primary_file_name
    if not source.is_file():
        source = target / primary_file_name
    if not source.is_file():
        raise FileNotFoundError(f"Primary USER review file was not generated: {primary_file_name}")
    destination = user_review_dir / primary_file_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination.resolve():
        shutil.move(str(source), str(destination))
    return destination.resolve()


def _timestamped_zip_stamp(created_at: datetime) -> str:
    return created_at.strftime("%Y%m%d-%H%M%S")


def _export_zip_path(review_root: Path, label: str, created_at: datetime) -> Path:
    stamp = _timestamped_zip_stamp(created_at)
    return (review_root / f"{_sanitize_folder_name(label)}-{stamp}.zip").resolve()


def _legacy_stable_export_zip_path(review_root: Path, label: str) -> Path:
    return (review_root / f"{_sanitize_folder_name(label)}.zip").resolve()


def _remove_stale_same_label_export_zips(review_root: Path, label: str, export_zip: Path) -> None:
    safe_label = _sanitize_folder_name(label)
    timestamped_name = re.compile(rf"^{re.escape(safe_label)}-\d{{8}}-\d{{6}}\.zip$")
    candidates = [_legacy_stable_export_zip_path(review_root, label)]
    candidates.extend(
        path.resolve()
        for path in review_root.glob(f"{safe_label}-*.zip")
        if timestamped_name.fullmatch(path.name)
    )
    for candidate in sorted(set(candidates)):
        if candidate == export_zip:
            continue
        if candidate.exists():
            if not candidate.is_file():
                raise ValueError(f"Refusing to remove non-file stale review zip path: {candidate}")
            candidate.unlink()


def _remove_legacy_stable_export_zip(review_root: Path, label: str) -> None:
    legacy_zip = _legacy_stable_export_zip_path(review_root, label)
    if legacy_zip.exists():
        if not legacy_zip.is_file():
            raise ValueError(f"Refusing to remove non-file legacy review zip path: {legacy_zip}")
        legacy_zip.unlink()


def _timestamped_export_zip_name_failures(export_zip: Path, expected_label: str) -> list[str]:
    safe_label = re.escape(_sanitize_folder_name(expected_label))
    pattern = re.compile(rf"^{safe_label}-\d{{8}}-\d{{6}}\.zip$")
    if pattern.fullmatch(export_zip.name):
        return []
    return [
        "Review export zip filename must include the creation timestamp: "
        f"expected {_sanitize_folder_name(expected_label)}-YYYYMMDD-HHMMSS.zip, "
        f"got {export_zip.name}"
    ]


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
    expected_label: str,
    expected_entries: set[str],
) -> None:
    name_failures = _timestamped_export_zip_name_failures(export_zip, expected_label)
    if name_failures:
        raise ValueError(
            "Review export zip filename validation failed:\n"
            + "\n".join(f"- {failure}" for failure in name_failures)
        )
    packet_files: dict[str, str] = {}
    with zipfile.ZipFile(export_zip, "r") as archive:
        entries = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
        try:
            start_here = archive.read("START_HERE.md").decode("utf-8")
        except KeyError as exc:
            raise ValueError(f"Review export zip is missing START_HERE.md: {export_zip}") from exc
        for entry in sorted(entries):
            try:
                packet_files[entry] = archive.read(entry).decode("utf-8")
            except UnicodeDecodeError:
                continue
    user_vision = _packet_file_text(packet_files, USER_BRANCH_VISION_REVIEW_FILE)
    if not user_vision:
        raise ValueError(
            f"Review export zip is missing {USER_BRANCH_VISION_REVIEW_FILE}: {export_zip}"
        )
    user_review = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    if not user_review:
        raise ValueError(
            f"Review export zip is missing {USER_BRANCH_PLAN_REVIEW_FILE}: {export_zip}"
        )
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
        *_fam007_bp2_plan_substantive_failures(packet_files),
        *_fam007_bp2_support_bp1_context_failures(packet_files),
        *_bp1_packet_phase_language_failures(packet_files),
        *_user_branch_vision_substantive_failures(packet_files),
        *_branch_planning_review_gate_state_failures(packet_files),
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
        "## Review Status",
        "## Contract Status",
        "## Packet Reviewability State",
        "## USER Gate State",
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
        "## Why This Fits The Nexus Vision",
        "## USER Design Questions",
        "## USER Response",
        "## Codex Digest",
        "## USER Response Proof",
        "## USER Response Digested",
        "## Accepted Branch Vision",
        "## Family-Vision Versus Branch-Only Vision Impact",
        "## Must-Have Behavior",
        "## Future-Gated Decisions And Regression-Risk Controls",
        "## Deferred And Future-Gated Ideas",
        "## Vision Question Queue",
        "## Design Assumption Ledger",
        "## Acceptance / Revision / Rejection / Waiver Decision",
    ):
        if required_heading not in user_vision:
            raise ValueError(
                f"Review export zip USER_BRANCH_VISION_REVIEW.md is missing {required_heading}"
            )
    for required_heading in (
        "## Contract Status",
        "## Packet Reviewability State",
        "## USER Gate State",
        "## USER Response Proof",
        "## USER Response Digested",
        "## Acceptance / Waiver / Revision / Rejection Receipt",
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
        text = _packet_file_text(packet_files, file_name)
        if not text:
            continue
        display_name = _packet_file_path(packet_files, file_name)
        for reason, pattern in USER_FACING_TECHNICAL_METADATA_PATTERNS:
            if pattern.search(text):
                failures.append(
                    f"{display_name}: USER-facing generated file contains technical metadata {reason}"
                )
    return failures


def _user_branch_plan_stale_bp1_wording_failures(packet_files: Mapping[str, str]) -> list[str]:
    text = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    if not text:
        return []
    failures: list[str] = []
    display_name = _packet_file_path(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    for reason, pattern in USER_BRANCH_PLAN_STALE_BP1_WORDING_PATTERNS:
        if pattern.search(text):
            failures.append(
                f"{display_name}: BP2 review contains stale BP1/product-design wording {reason}"
            )
    return failures


def _fam007_bp2_plan_substantive_failures(packet_files: Mapping[str, str]) -> list[str]:
    """Block FAM-007 BP2-primary packets that still read like BP2 previews."""

    start_here = packet_files.get("START_HERE.md", "")
    if "USER Review/USER_BRANCH_PLAN_REVIEW.md" not in start_here:
        return []

    text = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    combined = f"{start_here}\n{text}".casefold()
    if "fam-007 dev/owner skeleton readiness" not in combined:
        return []

    failures: list[str] = []
    display_name = _packet_file_path(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    forbidden_patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        (
            "bp2-preview-future-gated",
            re.compile(r"\bBP2 preview\b.*\bfuture-gated\b", re.IGNORECASE | re.DOTALL),
        ),
        (
            "review-accepted-bp1-first-preview",
            re.compile(r"Review accepted BP1 first; this BP2 preview", re.IGNORECASE),
        ),
        (
            "pending-accepted-or-waived-bp1-trace",
            re.compile(r"Pending accepted or waived BP1 trace", re.IGNORECASE),
        ),
        (
            "bp2-pending-until-bp1",
            re.compile(r"BP2 is pending until BP1 is accepted", re.IGNORECASE),
        ),
        (
            "cannot-green-while-bp1-pending",
            re.compile(r"cannot become green while BP1 is pending", re.IGNORECASE),
        ),
        (
            "generic-product-feedback-prompt",
            re.compile(
                r"visual direction,\s*workflow changes,\s*window behavior,\s*"
                r"output-file expectations",
                re.IGNORECASE,
            ),
        ),
    )
    for reason, pattern in forbidden_patterns:
        if pattern.search(text):
            failures.append(f"{display_name}: FAM-007 BP2 packet contains stale preview wording {reason}")

    external_plan_section = _section(
        text, "Active External Branch Plan / Historical Branch Plan Files"
    ).casefold()
    if "none recorded" in external_plan_section:
        failures.append(
            f"{display_name}: FAM-007 BP2 packet must name active external branch plan/state context"
        )

    required_headings = (
        "## Integrated Dev/Owner Readiness Matrix",
        "## Edition / Lane Matrix",
        "## Dev Readiness Matrix",
        "## Owner Readiness Matrix",
        "## Private Root / Remote Matrix",
        "## GitHub Desktop Binding Matrix",
        "## Backup / Import Matrix",
        "## Provider / Runtime / Cache / Memory Deferral Matrix",
        "## Watermark / Identity Matrix",
        "## Proof / Validation Matrix",
        "## Future USER Gate Matrix",
    )
    for heading in required_headings:
        if heading not in text:
            failures.append(f"{display_name}: FAM-007 BP2 packet is missing {heading}")

    accepted_trace = _section(text, "Accepted Branch Vision Summary").casefold()
    if "bp1 accepted" not in accepted_trace or "option a" not in accepted_trace:
        failures.append(
            f"{display_name}: FAM-007 BP2 packet missing accepted BP1 Option A trace"
        )
    return failures


def _fam007_bp2_support_bp1_context_failures(packet_files: Mapping[str, str]) -> list[str]:
    """Block BP2 packets whose supporting BP1 file still reads as pending BP1."""

    start_here = packet_files.get("START_HERE.md", "")
    if "USER Review/USER_BRANCH_PLAN_REVIEW.md" not in start_here:
        return []

    primary = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    combined = f"{start_here}\n{primary}".casefold()
    if "fam-007 dev/owner skeleton readiness" not in combined:
        return []

    support = _packet_file_text(packet_files, USER_BRANCH_VISION_REVIEW_FILE)
    display_name = _packet_file_path(packet_files, USER_BRANCH_VISION_REVIEW_FILE)
    if not support:
        return [f"{display_name}: BP2 packet is missing supporting accepted BP1 context"]

    failures: list[str] = []
    contract_status = _section(support, "Contract Status").casefold()
    user_gate_state = _section(support, "USER Gate State").casefold()
    accepted_vision = _section(support, "Accepted Branch Vision").casefold()
    if not contract_status.startswith(("complete", "waived by user")):
        failures.append(
            f"{display_name}: supporting BP1 context Contract Status must be Complete or Waived by USER for a BP2-primary packet"
        )
    if not user_gate_state.startswith(("user accepted", "user waived")):
        failures.append(
            f"{display_name}: supporting BP1 context USER Gate State must record USER Accepted or USER Waived for a BP2-primary packet"
        )
    if "accepted by user" not in accepted_vision and "waived by user" not in accepted_vision:
        failures.append(
            f"{display_name}: supporting BP1 context Accepted Branch Vision must record accepted or waived BP1 context"
        )

    forbidden_patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        (
            "draft-contract-status",
            re.compile(r"Draft - update to Complete or Waived by USER", re.IGNORECASE),
        ),
        (
            "pending-bp1-user-gate",
            re.compile(r"Pending USER Review - USER must accept, revise, waive, reject, or block BP1", re.IGNORECASE),
        ),
        (
            "final-bp1-acceptance-pending",
            re.compile(r"Final BP1 acceptance remains pending", re.IGNORECASE),
        ),
        (
            "bp1-remains-open",
            re.compile(r"BP1 remains open", re.IGNORECASE),
        ),
        (
            "pending-user-acceptance-or-waiver",
            re.compile(r"Pending USER acceptance or waiver", re.IGNORECASE),
        ),
        (
            "not-final-bp1-acceptance",
            re.compile(r"not final BP1 acceptance", re.IGNORECASE),
        ),
    )
    for reason, pattern in forbidden_patterns:
        if pattern.search(support):
            failures.append(
                f"{display_name}: supporting BP1 context contains stale pending-BP1 wording {reason}"
            )
    return failures


def _bp1_packet_phase_language_failures(packet_files: Mapping[str, str]) -> list[str]:
    combined = "\n".join(
        packet_files.get(file_name, "") for file_name in USER_FACING_GENERATED_FILES
    ).casefold()
    if "bp1 branch vision" not in combined or "authorize bp2 user branch plan review only" not in combined:
        return []

    failures: list[str] = []
    for file_name in USER_FACING_GENERATED_FILES:
        text = packet_files.get(file_name)
        if text is None:
            continue
        for reason, pattern in BP1_PACKET_STALE_LANGUAGE_PATTERNS:
            if pattern.search(text):
                failures.append(
                    f"{file_name}: BP1 packet contains stale phase/boundary language {reason}"
                )
    return failures


def _review_word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", value))


def _user_branch_vision_substantive_failures(packet_files: Mapping[str, str]) -> list[str]:
    text = _packet_file_text(packet_files, USER_BRANCH_VISION_REVIEW_FILE)
    if not text:
        return []
    failures: list[str] = []
    display_name = _packet_file_path(packet_files, USER_BRANCH_VISION_REVIEW_FILE)

    for field_name in (
        "Packet Reviewability State",
        "USER Gate State",
        "USER Response Proof",
        "USER Response Digested",
    ):
        if not _field_value(text, field_name) and not _section(text, field_name):
            failures.append(
                f"{display_name}: BP1 substantive review artifact missing {field_name}"
            )

    for section_name, minimum_words in USER_BRANCH_VISION_MINIMUM_SUBSTANTIVE_SECTIONS:
        value = _section(text, section_name)
        if _review_word_count(value) < minimum_words:
            failures.append(
                f"{display_name}: {section_name} is too shallow for BP1 substantive review"
            )

    for reason, pattern in USER_BRANCH_VISION_TEMPLATE_SHELL_PATTERNS:
        if pattern.search(text):
            failures.append(
                f"{display_name}: template-shell BP1 wording remains ({reason})"
            )

    surface_map = _section(text, "Surface Map")
    normalized_surface_map = re.sub(r"\s+", " ", surface_map).casefold()
    if " copied as " in normalized_surface_map and not any(
        term in normalized_surface_map
        for term in (
            "decision surface",
            "experience surface",
            "review surface",
            "user will see",
            "owner",
        )
    ):
        failures.append(
            f"{display_name}: copied-file list cannot be the BP1 Surface Map"
        )

    user_questions = _section(text, "USER Design Questions")
    question_count = user_questions.count("?")
    if question_count < 2:
        failures.append(
            f"{display_name}: USER Design Questions must ask branch-specific decision-driving questions"
        )

    recommendations = _section(text, "Codex Recommendations")
    normalized_recommendations = recommendations.casefold()
    if "recommendation" not in normalized_recommendations or not any(
        term in normalized_recommendations for term in ("tradeoff", "risk", "because")
    ):
        failures.append(
            f"{display_name}: Codex Recommendations must be branch-specific line-item recommendations with rationale and tradeoffs"
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
    source_file_names = [source_rel for source_rel, _copied_rel in copied]
    copied_context = ", ".join(f"`{source_rel}`" for source_rel in source_file_names[:5])
    if len(source_file_names) > 5:
        copied_context += f", plus {len(source_file_names) - 5} more source-truth files"
    if not copied_context:
        copied_context = "the selected source-truth files"
    decision_text = exact_user_decision.casefold()
    pr_readiness_context_packet = "pr readiness stage 1 analysis" in decision_text
    bp2_context_packet = (
        "bp2 user branch plan review" in decision_text
        or "bp2 branch plan review" in decision_text
    )
    bp3_context_packet = (
        "bp3" in decision_text
        or "workstream entry / orchestration" in decision_text
        or "orchestration validation" in decision_text
    )
    bp2_or_later_context_packet = bp2_context_packet or bp3_context_packet
    active_planning_gate = "BP3" if bp3_context_packet else "BP2"
    review_status = (
        "Context Complete - this packet uses BP1 as review context for PR Readiness Stage 1; "
        "it does not request a new Branch Vision decision."
        if pr_readiness_context_packet
        else (
            "Accepted by USER - this packet uses the accepted BP1 Branch Vision as "
            f"supporting context for {active_planning_gate}; it does not request "
            "a new BP1 decision."
        )
        if bp2_or_later_context_packet
        else "Needs USER Decision unless this packet records an explicit USER acceptance or waiver."
    )
    contract_status = (
        "Complete - Branch Vision context is recorded for this PR Readiness review packet; "
        "implementation remains outside this decision."
        if pr_readiness_context_packet
        else (
            "Complete - BP1 Branch Vision accepted by USER and used as accepted "
            f"context for this {active_planning_gate} packet."
        )
        if bp2_or_later_context_packet
        else "Draft - update to Complete or Waived by USER only after USER accepts or waives BP1 for this branch."
    )
    user_response = (
        "No new BP1 response requested by this packet; PR Readiness Stage 1 analysis remains the next USER decision."
        if pr_readiness_context_packet
        else (
            f"BP1 accepted by USER; {active_planning_gate} is the active USER decision in this packet."
        )
        if bp2_or_later_context_packet
        else "Pending USER response or explicit waiver."
    )
    packet_reviewability_state = (
        "Reviewable - context packet for later-phase review; no new BP1 decision is requested by this helper output."
        if pr_readiness_context_packet
        else (
            f"Reviewable - supporting accepted BP1 context for the active {active_planning_gate} packet."
        )
        if bp2_or_later_context_packet
        else "Reviewable - BP1 packet is ready for USER Branch Vision Review, but acceptance is not recorded."
    )
    user_gate_state = (
        "Superseded - context-only BP1 copy for later-phase review; rely on the accepted branch record or external state for the original BP1 receipt."
        if pr_readiness_context_packet
        else (
            f"USER Accepted - BP1 Branch Vision accepted by USER; {active_planning_gate} is the active gate."
        )
        if bp2_or_later_context_packet
        else "Pending USER Review - USER must accept, revise, waive, reject, or block BP1 before BP2 preparation can be green."
    )
    codex_digest = (
        "Codex records this BP1 file as a context aid for the governance lifecycle reform packet. "
        "Accepted outcomes must fold into durable source-truth owners or external operational state."
        if pr_readiness_context_packet
        else (
            "Codex records the accepted BP1 Option A direction as the planning basis for BP2: "
            "integrated Dev/Owner readiness, future private Dev repo direction after approval, "
            "Owner local-private baseline, GitHub Desktop safety, backup/import lane posture, "
            "provider/runtime/cache/memory deferral, proof expectations, and lane identity labels."
        )
        if bp2_or_later_context_packet
        else "Pending USER response digest."
    )
    accepted_vision = (
        "Accepted context: Governance Phase Lifecycle Reform and local USER hub model are represented by the copied source-truth files."
        if pr_readiness_context_packet
        else (
            "Accepted by USER - integrated Option A Dev/Owner Skeleton Readiness Branch Vision. "
            "Dev and Owner readiness stay planned together in one public-safe trust-boundary package; "
            "future Dev is private-repo-oriented after approval; Owner remains local-private by default; "
            "GitHub Desktop/public-upstream safety, backup/import posture, provider/runtime/cache/memory "
            "deferral, proof expectations, and lane identity labels are BP2 planning requirements."
        )
        if bp2_or_later_context_packet
        else "Pending USER acceptance or waiver."
    )
    profile_text = " ".join(
        [title, review_purpose, exact_user_decision, *source_file_names]
    ).casefold().replace("_", "-")
    fam007_dev_owner_bp1_packet = (
        "fam-007" in profile_text
        and (
            "dev-owner-skeleton-readiness" in profile_text
            or "dev/owner skeleton readiness" in profile_text
        )
        and not pr_readiness_context_packet
    )
    if fam007_dev_owner_bp1_packet:
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
            "## Packet Reviewability State",
            "",
            packet_reviewability_state,
            "",
            "## USER Gate State",
            "",
            user_gate_state,
            "",
            "## Contract Revision",
            "",
            (
                f"v8 - Accepted BP1 Branch Vision context for {active_planning_gate}: integrated Dev/Owner readiness, "
                "Dev private repo future direction, Owner local-private baseline, GitHub Desktop safety, "
                "backup/import lane posture, provider/runtime/cache/memory deferral, and identity labeling."
                if bp2_or_later_context_packet
                else "v6 - USER/ChatGPT BP1 review direction digested: integrated Dev/Owner readiness, Dev private repo future direction, Owner local-private baseline, GitHub Desktop safety, backup/import lane posture, and identity labeling."
            ),
            "",
            "## Project Vision Context",
            "",
            "Nexus is meant to stay Windows-first, local-first, modular, inspectable, privacy-aware, and USER-controlled even as AI capability grows. This Branch Vision keeps the public repo as the place where future Dev and Owner skeleton setup is made understandable before any private roots, remotes, provider behavior, cache behavior, memory, or automation exists.",
            "",
            "## Family Vision Context",
            "",
            "FAM-007 owns local AI, capability packs, Public/Dev/Owner separation, public/private trust boundaries, provider readiness, consent posture, provider-visible data, execution gates, and memory or future learning boundaries. The branch should turn those family rules into a concrete Dev/Owner readiness direction while keeping the base public product useful and safe without local LLM or provider execution.",
            "",
            "## Feature Vision Context",
            "",
            "This successor carrier follows the merged Breakpoint 2 action-gate proof and the Governance USER Review Gate repair. USER selected the integrated Option A direction: Dev and Owner skeleton readiness should be planned together as one public-safe trust-boundary package. The feature vision is not private setup; it is the public-safe readiness layer that lets USER decide how Dev private repo readiness, Owner local-private control, GitHub Desktop posture, backup/import timing, provider/model deferral, runtime cache deferral, memory deferral, and lane identity should be represented before later gates authorize any implementation.",
            "",
            "## Codex Understanding",
            "",
            "Codex understands this BP1 as a product and trust-boundary vision review for the FAM-007 Dev/Owner Skeleton Readiness carrier. The branch should prepare a decision-ready public package for future Dev and Owner skeleton setup, preserve every private/runtime action gate, and give BP2 a concrete accepted vision to translate into an engineering plan. The updated direction keeps Dev and Owner together for planning, treats future Dev as likely private-repo backed after approval, treats Owner as local-private and controlled by default, and requires BP2 to make GitHub Desktop, public-upstream, backup/import, proof, and identity propagation explicit.",
            "",
            "## Branch Goal",
            "",
            "Define a public-safe Dev/Owner skeleton readiness and decision layer around one integrated trust-boundary package. The branch should make future Dev and Owner setup choices understandable before private repositories, local-only roots, private remotes, backup/import behavior, provider or model execution, runtime cache behavior, memory, learning, personalization, or release work exists. BP2 should plan the route toward a future private Dev repo, Owner local Git/version-history safety, optional later Owner remote evaluation, public-upstream safety, and lane identity labels without creating any of those private/runtime surfaces.",
            "",
            "## End-State Vision",
            "",
            "When this branch is complete, USER should have durable source truth, decision matrices, future-gate definitions, proof expectations, validation gates, and review artifacts that name the Dev readiness path, Owner readiness path, public-to-private boundary, private root and remote decision points, GitHub Desktop safety posture, backup/import timing choices, provider/model/cache/memory deferral, lane watermark/identity labels, artifact identity propagation, and later USER action gates. It should be obvious what BP2 is allowed to plan next, what belongs only in a future private Dev repo, what stays Owner-local by default, and what still needs separate approval.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "- An integrated Dev/Owner readiness matrix that treats Dev and Owner as one public-safe trust-boundary package for BP2 planning.",
            "- A Dev readiness matrix that names future private Dev repo direction, local-root staging choices, public-upstream relationship, private-origin expectation, contributor-only boundaries, and future GitHub Desktop private binding after approval.",
            "- A Dev asset inventory posture that asks BP2 to plan how dev-related launchers, assets, and tools are inventoried, classified, transferred, recreated, or removed from the normal User/Public lane over time.",
            "- An Owner readiness matrix that keeps Owner private and controlled, defaults to local Git/version history and no remote, and evaluates a private Owner remote only as a future option if BP2 proves it safer and USER later approves it.",
            "- A private root and remote decision matrix for User/Public, Dev, and Owner lanes covering local-only roots, private hosting, GitHub Desktop binding, private `origin`, fetch-only `public-upstream`, remote identity proof, and public push prevention.",
            "- A backup/import timing choice set for User/Public settings/preferences/config backup, Dev private development recovery tied to the future private Dev repo, and Owner local/private/encrypted recovery with rollback as the safest baseline.",
            "- A provider/runtime/cache/memory deferral proof surface showing provider-visible data remains none, prompt acceptance remains disabled, downloads stay blocked, runtime cache stays inactive, and memory or personalization stays inactive.",
            "- A watermark and identity posture: User/Public should present as `Nexus Desktop AI` or `Nexus Desktop AI · Pre-Beta`, Dev as `Nexus Desktop AI · DEV PRIVATE`, and Owner as `Nexus Owner · Local Private` unless a later approved Owner remote model changes that wording.",
            "- Identity propagation requirements for UI, launchers, diagnostics, logs, review packets, screenshots/proof, backup/export packages, and generated manifests so Dev and Owner proof artifacts are visibly marked where appropriate.",
            "- These surfaces are review and proof targets only; this BP1 vision creates no private repos, roots, remotes, provider calls, cache behavior, memory, runtime UI, GitHub Desktop binding, backup/import execution, or launcher migration.",
            "",
            "## How It Will Function",
            "",
            "The readiness layer should prevent premature private/runtime work while preparing a clear future setup path. It should define action gates, public-safe proof surfaces, decision matrices, and validator expectations that show each private, provider-facing, backup/import, GitHub Desktop, identity-propagation, or launcher/assets action is still pending, with no activation path until later USER approval.",
            "",
            "## User Experience Flow",
            "",
            "1. USER reviews Dev readiness and Owner readiness together as one public-safe trust-boundary package.",
            "2. USER confirms whether BP2 should plan the integrated Option A matrix with Dev private repo direction, Owner local-private baseline, GitHub Desktop posture, backup/import lane posture, and identity/watermark propagation.",
            "3. USER names the private root, private remote, public-upstream, GitHub Desktop, backup/import, provider/cache/memory, launcher/assets, and artifact identity proof expectations that BP2 must make concrete.",
            (
                f"4. USER has accepted this BP1 Branch Vision as the basis for the active {active_planning_gate} review."
                if bp2_or_later_context_packet
                else "4. USER accepts, revises, holds for more options, rejects, or explicitly waives this BP1 Branch Vision."
            ),
            (
                "5. BP2 is accepted; BP3 now validates orchestration before any Workstream implementation can be requested."
                if bp3_context_packet
                else "5. BP2 now turns the accepted vision into an engineering plan, and BP3 later validates orchestration before any Workstream implementation can be requested."
                if bp2_context_packet
                else "5. BP2 later turns only the accepted or waived vision into an engineering plan, and BP3 later validates orchestration before any Workstream implementation can be requested."
            ),
            "",
            "## Surface Map",
            "",
            "- Edition/Lane Matrix: User/Public remains normal `Nexus Desktop AI` or `Nexus Desktop AI · Pre-Beta`; Dev is visibly private; Owner is visibly local-private unless later changed by approved remote policy.",
            "- Dev/Owner Readiness Matrix: Dev and Owner stay together as the accepted planning direction, while their actual private setup remains separately gated.",
            "- Dev readiness surface: a future BP2 matrix should state future private Dev repo direction, local-root staging choices, public-upstream relationship, private-origin expectation, contributor-only boundaries, and dev launcher/assets/tool inventory or migration posture.",
            "- Owner readiness surface: a future BP2 matrix should state Owner local Git/version-history baseline, no default public exposure path, no default remote path, no default GitHub Desktop private remote binding, and the future conditions under which a private Owner remote could be evaluated.",
            "- Private Root / Remote Matrix: public root, future Dev private repo/root, future Owner local/private root, private `origin`, fetch-only `public-upstream`, remote identity proof, and push-prevention need explicit later decisions.",
            "- GitHub Desktop Binding Matrix: User/Public binding stays normal public repo posture; future Dev may use GitHub Desktop with a private Dev repo after approval; Owner defaults to local Git/no remote unless BP2 proves a safer private remote model and USER later approves it.",
            "- Backup / Import Matrix: User/Public should stay product-safe settings/preferences/config backup only; Dev should plan private development recovery that can integrate with the future private Dev repo; Owner should plan local/private/encrypted recovery and rollback as the safest baseline.",
            "- Provider / Runtime / Cache / Memory Deferral Matrix: provider-visible data none, sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, runtime cache inactive, and memory/learning/personalization inactive.",
            "- Watermark / Identity Matrix: UI, launchers, diagnostics, logs, review packets, screenshots/proof, backup/export packages, and generated manifests should carry the right lane identity when BP2 later plans proof.",
            "- Proof and Validation Matrix: later validators and packet checks should prove no private repo, private root, private remote, GitHub Desktop private binding, backup/import execution, provider/model execution, runtime cache behavior, memory behavior, token, secret, prompt, model artifact, private automation, or private artifact enters the public branch.",
            "- Future USER Gate Matrix: BP2, BP3, Workstream implementation, private Dev/Owner setup, backup/import execution, provider/runtime/cache/memory behavior, PR, merge, release, cleanup, AI Product Contract import, Private Dev ORIN import, and v1.8.0 remain separate future decisions.",
            "",
            "## Product Options / Design Paths",
            "",
            "- Option A - selected direction: integrated Dev and Owner readiness matrix. This keeps Dev private repo direction, Owner local-private control, public-upstream safety, GitHub Desktop posture, backup/import posture, provider/model deferral, cache deferral, memory deferral, and identity propagation in one public-safe trust-boundary package. Tradeoff: BP2 is broader, but the gates stay consistent.",
            "- Option B - Dev-private-repo-first planning inside the same package. This emphasizes future private Dev repo, Dev GitHub Desktop posture, and dev launcher/assets migration first. Tradeoff: Owner version-control and no-public-exposure rules could lag unless BP2 keeps the shared matrix.",
            "- Option C - Owner-local-private-first planning inside the same package. This emphasizes local Git/version history, local/private/encrypted recovery, no default remote, no public exposure, and Owner identity first. Tradeoff: Dev private repo and launcher/assets migration could lag.",
            "- Option D - root/remote/GitHub Desktop safety package first. This focuses on public-upstream, private `origin`, remote identity proof, push prevention, and binding proof across User/Public, Dev, and Owner lanes. Tradeoff: backup/import and identity propagation still need matrix detail.",
            "- Option E - backup/import and identity package first. This prioritizes User/Public settings backup, Dev private development recovery, Owner encrypted rollback, lane labels, and artifact identity propagation. Tradeoff: private repo topology and provider/runtime deferral still need expansion.",
            "- Option F - provider/runtime deferral-first package. This proves provider-visible data none, sentToProvider=false, canAcceptPrompts=false, downloads/network blocked, cache inactive, and memory inactive before private setup. Tradeoff: it may under-answer private repo/root topology until BP2 expands it.",
            "",
            "## Codex Recommendations",
            "",
            "- Recommendation 1: keep the USER-selected Option A direction and make BP2 plan Dev plus Owner readiness in one integrated matrix. Placement should stay in the public FAM-007 carrier because the shared trust boundary is the product problem; behavior should stay planning/proof only; tradeoff is a wider BP2, but the risk of inconsistent private gates is lower.",
            "  USER response:",
            "- Recommendation 2: record future Dev as private-repo-oriented after approval and ask BP2 to inventory dev-related launchers, assets, and tools that should not remain in the normal User/Public version long-term. BP2 should plan classification, transfer, recreation, or removal paths without moving files or creating private repos in BP1.",
            "  USER response:",
            "- Recommendation 3: set Owner's default safety model to local Git/version history, local/private/encrypted recovery, no public exposure path, no default remote path, and no default GitHub Desktop private remote binding. A private Owner remote should stay a future option only if BP2 proves it is safer and USER later approves it.",
            "  USER response:",
            "- Recommendation 4: require BP2 to produce Edition/Lane, Dev/Owner Readiness, Private Root/Remote, GitHub Desktop Binding, Backup/Import, Provider/Runtime/Cache/Memory Deferral, Watermark/Identity, Proof and Validation, and Future USER Gate matrices before BP3 can ask for implementation.",
            "  USER response:",
            "- Recommendation 5: keep backup/import execution, provider SDKs, model downloads, provider/model execution, runtime cache behavior, memory, learning, personalization, voice/Core sync, shortcut/installer work, PR, merge, release, and cleanup deferred until named future gates. This protects Main and keeps provider-visible data at none; tradeoff is slower private setup.",
            "  USER response:",
            "- Recommendation 6: require public-safe proof and fixture/validator checks before any later private setup is considered. The proof should cover no private paths, remotes, tokens, secrets, prompts, memory, model artifacts, provider calls, downloads, cache activation, backup/import execution, GitHub Desktop private binding, private automation, or private artifacts in public review output.",
            "  USER response:",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "The branch fits Nexus because it makes powerful AI-edition work deliberate instead of ambient. It keeps the public app local-first and inspection-friendly, preserves the FAM-007 family rule that provider/model/cache/memory behavior needs explicit gates, and gives USER a clear way to choose future Dev/Owner boundaries before any sensitive setup exists.",
            "",
            "## USER Design Questions",
            "",
            "- Does USER confirm Option A as the BP1 vision direction: Dev and Owner skeleton readiness planned together as one integrated public-safe trust-boundary package?",
            "- For the Dev side, should BP2 treat a future private Dev repo as the preferred long-term path while repo creation and GitHub Desktop private binding remain future-gated?",
            "- Which existing or future dev launchers, assets, tools, diagnostics, logs, manifests, or proof artifacts should BP2 inventory as candidates for transfer, recreation, or removal from the normal User/Public lane?",
            "- For the Owner side, does USER accept local Git/version history, no default remote, no public exposure path, and no default GitHub Desktop private remote binding as the baseline?",
            "- What criteria would make a future private Owner remote safer than local-only Owner version history?",
            "- What exact public-upstream, private-origin, remote naming, remote identity proof, fetch/reconcile posture, and push-prevention expectations should BP2 make visible for GitHub Desktop?",
            "- Should backup/import readiness be planned before private roots exist, after private roots exist, or only after Dev/Owner skeleton setup is separately approved?",
            "- What is enough proof for User/Public settings backup, Dev private development recovery, and Owner local/private/encrypted rollback?",
            "- What evidence should prove provider/model execution, downloads, runtime cache behavior, and memory/personalization remain inactive?",
            "- Are the proposed identity labels acceptable: `Nexus Desktop AI` or `Nexus Desktop AI · Pre-Beta` for User/Public, `Nexus Desktop AI · DEV PRIVATE` for Dev, and `Nexus Owner · Local Private` for Owner?",
            "- What proof bar should be required before any later private setup: matrix only, validator fixtures, no-leak scan, provider-state proof, packet walkthrough, visual walkthrough, artifact identity proof, or a combination?",
            "",
            "## USER Response",
            "",
            (
                "USER accepted the updated Option A BP1 Branch Vision: Dev and Owner skeleton readiness stay planned together as one public-safe trust-boundary package; future Dev is private-repo-oriented after approval; dev-related launchers/assets/tools should leave the normal User/Public lane long-term; Owner remains private and controlled with local Git/version history as the baseline; GitHub Desktop safety, public-upstream posture, backup/import lane posture, proof expectations, and lane identity labels must be planned by BP2."
                if bp2_or_later_context_packet
                else "Revision direction received from USER/ChatGPT review: Option A is the selected BP1 direction; Dev should eventually have a private repo; dev-related launchers/assets/tools should leave the normal User/Public lane long-term; Owner should remain private and controlled with local Git/version history as the baseline; GitHub Desktop safety, public-upstream posture, backup/import lane posture, proof expectations, and lane identity labels must be planned by BP2. Final BP1 acceptance remains pending."
            ),
            "",
            "## Codex Digest",
            "",
            (
                f"Codex records this file as accepted BP1 context for the active {active_planning_gate} packet. The accepted vision is one integrated Dev/Owner readiness package with future private Dev repo planning, Dev asset inventory/migration planning, Owner local-private version-control safety, explicit GitHub Desktop binding rules, public-upstream push-prevention proof, backup/import posture for User/Public, Dev, and Owner lanes, provider/runtime/cache/memory deferral proof, and visible lane identity labels."
                if bp2_or_later_context_packet
                else "Codex digested the USER/ChatGPT BP1 review direction into this v6 Branch Vision. The updated vision recommends one integrated Dev/Owner readiness package, future private Dev repo planning, Dev asset inventory/migration planning, Owner local-private version-control safety, explicit GitHub Desktop binding rules, public-upstream push-prevention proof, backup/import posture for User/Public, Dev, and Owner lanes, provider/runtime/cache/memory deferral proof, and visible lane identity labels. This digest is a revision update, not final BP1 acceptance."
            ),
            "",
            "## USER Response Proof",
            "",
            (
                f"Accepted by USER - BP1 Branch Vision acceptance is recorded in external branch planning state and used by this {active_planning_gate} packet as supporting context."
                if bp2_or_later_context_packet
                else "USER/ChatGPT BP1 review direction is recorded in this v6 packet. Final BP1 acceptance, revision, waiver, rejection, or hold remains pending USER decision."
            ),
            "",
            "## USER Response Digested",
            "",
            (
                f"Digested - accepted BP1 direction is preserved as required {active_planning_gate} traceability context."
                if bp2_or_later_context_packet
                else "Partially - USER/ChatGPT revision direction has been digested into v6, but BP1 remains open until USER explicitly accepts, revises, waives, rejects, or holds the updated Branch Vision."
            ),
            "",
            "## Accepted Branch Vision",
            "",
            accepted_vision,
            "",
            "## Family-Vision Versus Branch-Only Vision Impact",
            "",
            "Branch-only by default: this carrier applies existing FAM-007 and AI runtime/trust architecture to Dev/Owner skeleton readiness. The v6 direction may affect future edition identity, Dev asset placement, Owner version-control posture, GitHub Desktop safety, backup/import posture, and proof expectations. If USER changes edition boundaries, provider/cache/memory policy, public/private promotion rules, or the durable Public/Dev/Owner naming model, Codex must route that change to the proper durable family or architecture owner before BP2 relies on it.",
            "",
            "## Must-Have Behavior",
            "",
            (
                f"- BP1 acceptance is recorded; {active_planning_gate} must keep tracing to this accepted Dev/Owner skeleton readiness vision and integrated Option A direction."
                if bp2_or_later_context_packet
                else "- BP1 acceptance or explicit waiver is required before BP2 can claim the engineering plan is valid."
            ),
            "- BP2 must trace every seam or SLC to this accepted Dev/Owner skeleton readiness vision and its integrated Option A direction.",
            "- BP2 must include Edition/Lane, Dev/Owner Readiness, Private Root/Remote, GitHub Desktop Binding, Backup/Import, Provider/Runtime/Cache/Memory Deferral, Watermark/Identity, Proof and Validation, and Future USER Gate matrices.",
            "- The branch must preserve public-safe proof and avoid creating or activating private/runtime/provider/cache/memory behavior, private GitHub Desktop binding, backup/import execution, or dev asset migration.",
            "- USER-facing review files must stay decision-focused while technical proof remains in helper output, validator output, Codex digest, or external operational state.",
            "",
            "## Future-Gated Decisions And Regression-Risk Controls",
            "",
            "- Future-gated decision: private Dev skeleton setup, private Owner skeleton setup, private Dev repo creation, private Owner repo or remote creation, local-only private roots, private remotes, and GitHub Desktop private binding.",
            "- Future-gated decision: dev launcher/assets/tool inventory execution, transfer, recreation, removal from the User/Public lane, or import into a private Dev path.",
            "- Future-gated decision: backup/import behavior, public-to-private import, User/Public backup implementation, Dev recovery implementation, Owner encrypted recovery or rollback implementation, provider SDKs, model downloads, provider/model execution, runtime provider execution, cache behavior, memory, learning, indexing, retrieval, and personalization.",
            "- Future-gated decision: voice/Core sync, shortcut or installer work, PR creation, merge, release, cleanup, issue mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work.",
            "- Regression-risk control: reviewability is not USER acceptance, and packet validation cannot approve BP2, BP3, or Workstream implementation.",
            "- Regression-risk control: any future private, GitHub Desktop, backup/import, identity, or provider-facing proof must be public-safe, synthetic where needed, and free of private paths, secrets, tokens, prompts, memory, model artifacts, private automation, private repository URLs, and private artifacts.",
            "",
            "## Deferred And Future-Gated Ideas",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
            "## Vision Question Queue",
            "",
            (
                "- Use integrated Dev/Owner readiness as the accepted BP1 direction while reviewing whether the BP2 engineering plan faithfully builds it."
                if bp2_context_packet
                else "- Confirm integrated Dev/Owner readiness as the accepted BP1 direction or revise it before BP2."
            ),
            "- Decide the future Dev private repo posture and the dev launcher/assets/tool inventory or migration questions BP2 must answer.",
            "- Decide whether Owner stays local Git/no remote by default and what criteria would justify evaluating a private Owner remote later.",
            "- Decide which public-upstream, private origin, GitHub Desktop binding, backup/import, provider/cache/memory, identity/watermark, artifact-propagation, and public-to-private promotion questions BP2 must answer.",
            "- Decide what proof format USER wants before any future private setup, backup/import execution, GitHub Desktop private binding, provider/runtime behavior, cache behavior, or memory behavior can be considered.",
            "",
            "## Design Assumption Ledger",
            "",
            "- Assumption: the public branch may define readiness, decisions, fixtures, validators, and review proof, but it may not contain private Dev or Owner assets, private repo URLs, private root paths, real private screenshots, private prompts, or private automation.",
            "- Assumption: User/Public remains normal Nexus branding, while Dev and Owner artifacts should be visibly marked where appropriate once BP2 plans identity propagation.",
            "- Assumption: provider-visible data remains none, sentToProvider remains false, canAcceptPrompts remains false, downloads/network/external calls remain blocked, memory and cache runtime behavior remain inactive, and voice/Core sync remains gated until later USER approval.",
            "- Assumption: accepted BP1 changes that alter family, architecture, or edition-boundary policy must fold into the durable source-truth owner before BP2 treats them as implementation scope.",
            "",
            "## Acceptance / Revision / Rejection / Waiver Decision",
            "",
            "- Accept: USER accepts this FAM-007 Dev/Owner Skeleton Readiness Branch Vision and authorizes BP2 preparation only.",
            "- Revise: USER requests specific changes to readiness surfaces, options, proof expectations, private-boundary wording, or future-gated decisions before BP2.",
            "- Hold / More Options: USER wants additional product options, examples, or proof models before accepting or rejecting BP1.",
            "- Reject: USER rejects this branch vision or routes FAM-007 to a different successor candidate.",
            "- Waive: USER explicitly waives BP1 and accepts the risk of planning without a fully accepted Branch Vision.",
            "",
            exact_user_decision,
            "",
        ]
        review_path = target / USER_BRANCH_VISION_REVIEW_FILE
        review_path.write_text("\n".join(lines), encoding="utf-8")
        return review_path.resolve()
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
        "## Packet Reviewability State",
        "",
        packet_reviewability_state,
        "",
        "## USER Gate State",
        "",
        user_gate_state,
        "",
        "## Contract Revision",
        "",
        "v3 - generated by the local USER hub helper with applied BP1 review sections.",
        "",
        "## Project Vision Context",
        "",
        f"`{title}` should keep Nexus USER-controlled, inspectable, and local-first by naming the branch outcome in plain language before engineering planning begins. The copied context ({copied_context}) supports that outcome, but the branch vision must stand on its own as a readable USER decision aid.",
        "",
        "## Family Vision Context",
        "",
        f"`{title}` belongs to the family or governance lane represented by the copied source-truth files. If the USER chooses a direction that changes reusable family behavior, Codex must route that accepted change to the durable owner before BP2 relies on it.",
        "",
        "## Feature Vision Context",
        "",
        f"The selected packet context is `{review_purpose}`. BP1 should settle the feature or governance outcome USER expects from this branch, the boundaries that stay future-gated, and which copied owners are context only rather than active operational ledgers.",
        "",
        "## Codex Understanding",
        "",
        review_purpose,
        "",
        "## Branch Goal",
        "",
        f"Name the concrete branch outcome for `{title}` before engineering planning. The goal is to translate `{review_purpose}` into a clear branch direction: what the branch is meant to accomplish, what USER will inspect, and what remains blocked until later approved gates.",
        "",
        "## End-State Vision",
        "",
        f"When this branch reaches its intended end state, USER should be able to point to the accepted outcome for `{title}`, the surfaces or governance behaviors that should exist, the proof expectations that make the outcome trustworthy, and the deferred outcomes that still require later approval.",
        "",
        "## What Will I Actually See, And Where Will I See It?",
        "",
        f"USER should see an applied explanation of `{title}`, a concrete outcome description, named review surfaces, real decision paths, branch-specific recommendations, and design questions that can change BP2. The copied context files remain supporting evidence rather than the vision itself.",
        "",
        "## How It Will Function",
        "",
        f"The branch vision functions as the product and governance target for `{title}`. It names the expected outcome, the surfaces USER will inspect, the boundaries that remain future-gated, and the proof expectations that later planning must preserve.",
        "",
        "## User Experience Flow",
        "",
        f"1. USER reads the branch outcome and the surfaces affected by `{title}`.\n2. USER compares the design paths and tradeoffs.\n3. USER answers the branch-specific questions that control future planning.\n4. Codex digests the response before any later engineering plan treats the vision as accepted.",
        "",
        "## Surface Map",
        "",
        f"- Review surface: `USER_BRANCH_VISION_REVIEW.md` explains the `{title}` branch vision in plain language for USER decision-making.",
        f"- Context surface: `START_HERE.md` maps copied files such as {copied_context} back to repo source truth without making the copy list the vision.",
        "- Decision surface: `USER Response`, `Codex Digest`, and `Acceptance / Revision / Rejection / Waiver Decision` record whether BP1 closes or returns for revision.",
        "- Future proof surface: BP2 and BP3 may use this accepted vision for traceability, but they cannot replace it with engineering convenience or implementation readiness.",
        "",
        "## Product Options / Design Paths",
        "",
        f"- Option A - strongest implied `{title}` outcome: keep the branch focused on the most concrete product, governance, or source-truth result described by the review purpose. Tradeoff: fastest route to BP2, but only safe when USER can clearly visualize the outcome.",
        "- Option B - narrower surface path: reduce the branch to the subset of surfaces USER can confidently approve now. Tradeoff: less risk of overreach, but later branches may need to reconnect deferred surfaces.",
        "- Option C - broader owner/family impact path: treat the branch as changing reusable family or project direction. Tradeoff: stronger long-term alignment, but it may require source-truth fold-down before BP2.",
        "",
        "## Codex Recommendations",
        "",
        f"- Recommendation: Choose the most concrete `{title}` outcome USER can visualize and make that outcome the BP2 target. Tradeoff: this keeps planning grounded, but it may require revising vague branch language before engineering starts.",
        "  USER response:",
        f"- Recommendation: Require any revision to name the expected USER-visible, governance, or source-truth surface for `{title}`. Tradeoff: stricter response digestion takes more care, but it gives BP2 a real contract to build from.",
        "  USER response:",
        "- Recommendation: Treat copied files as context evidence, not as the Branch Vision itself. Tradeoff: USER may inspect fewer raw lines first, but the decision becomes easier to reason about and harder for a template shell to pass.",
        "  USER response:",
        "",
        "## Why This Fits The Nexus Vision",
        "",
        f"This BP1 structure protects the Nexus pattern of USER-controlled, inspectable, local-first planning by making `{title}` explain its purpose before implementation. It keeps project and family vision above seams, helpers, and validators, while still giving Codex enough branch-specific direction to plan the next gate.",
        "",
        "## USER Design Questions",
        "",
        f"- For `{title}`, which concrete outcome should USER expect to see, inspect, or rely on when this branch is complete?",
        "- Which option above best matches the desired direction, and what specific change would make the branch vision feel correct before BP2?",
        "- Are there family-level, architecture-level, policy-level, experience-level, or future-gated boundaries that Codex must preserve instead of folding into this branch?",
        "",
        "## USER Response",
        "",
        user_response,
        "",
        "## Codex Digest",
        "",
        codex_digest,
        "",
        "## USER Response Proof",
        "",
        user_response,
        "",
        "## USER Response Digested",
        "",
        "No - BP1 remains open until Codex digests an explicit USER response or waiver."
        if not pr_readiness_context_packet
        else "Not applicable - this is a later-phase context copy, not a new BP1 gate.",
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
        "## Future-Gated Decisions And Regression-Risk Controls",
        "",
        "- Regression-risk control: SLCs remain engineering route details inside an accepted branch, not automatic separate branches.",
        "- Regression-risk control: Workstream remains blocked until BP1 and BP2 are accepted or explicitly waived and BP3 is green.",
        "- Regression-risk control: USER-facing review files stay focused on vision, plan context, options, risks, proof expectations, and USER decisions rather than mutable operational metadata.",
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
    is_fam007_dev_owner_skeleton = (
        source_branch == "feature/fam-007-dev-owner-skeleton-readiness"
        or any(
            "feature_fam_007_dev_owner_skeleton_readiness" in source_rel
            for source_rel, _copied_rel in copied
        )
    )
    normalized_decision = exact_user_decision.casefold()
    workstream_package_approval_packet = any(
        marker in normalized_decision
        for marker in BRANCH_PLANNING_IMPLEMENTATION_REQUEST_MARKERS
    ) and not any(
        marker in normalized_decision
        for marker in BRANCH_PLANNING_IMPLEMENTATION_BLOCKING_MARKERS
    )
    pr_readiness_stage1_packet = "pr readiness stage 1 analysis" in normalized_decision
    bp1_branch_vision_packet = (
        "bp1 branch vision" in normalized_decision
        and "authorize bp2 user branch plan review only" in normalized_decision
    )
    bp3_orchestration_packet = (
        "bp3" in normalized_decision
        or "workstream entry / orchestration" in normalized_decision
        or "orchestration validation" in normalized_decision
        or (is_fam007_dev_owner_skeleton and workstream_package_approval_packet)
    )
    bp2_branch_plan_packet = (
        not bp1_branch_vision_packet
        and not bp3_orchestration_packet
        and (
            "bp2 user branch plan review" in normalized_decision
            or "bp2 branch plan review" in normalized_decision
        )
    )
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
    extra_plan_sections: list[str] = []
    user_response_text: str | None = None
    likely_files_lines = [
        f"`{source_rel}` copied as `{copied_rel}`" for source_rel, copied_rel in copied
    ]
    user_decisions_intro = (
        "USER may answer in order or respond generally. Useful feedback includes visual "
        "direction, workflow changes, window behavior, output-file expectations, "
        "deferred scope, or anything that would make the branch plan feel wrong before "
        "implementation planning begins."
    )
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
            "Future-gated boundary controls.",
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
            "and review evidence digest must all agree on decision path, USER decision, and "
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
            "Future-gated boundary controls.",
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
                    "Seam 1 is complete; if the same-branch Workstream package remains in progress, "
                    "continuation must move to Seam 2 unless a real blocker, explicit waiver, or "
                    "backlog split is recorded."
                )
                if seam1_completion_packet
                else (
                    "Until USER accepts or waives this contract and approves bounded Workstream "
                    "implementation, the entry seam and later same-branch seams remain blocked."
                )
            ),
            "The Workstream entry seam is public-safe action-gate registry/proof, deterministic fixtures or validators, source-truth fold-down, packet refresh, and validation; later admitted same-branch seams continue under Workstream governance until Workstream Green, a real blocker, or an explicit USER waiver.",
            "No private Dev repo, private Owner repo, local-only private root, private remote, GitHub Desktop private remote, backup/import behavior, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, FAM-006 mutation, Governance mutation, AI Product Contract import, Private Dev ORIN import, or v1.8.0 work is authorized by this packet.",
            "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior not implemented.",
        ]
        rejected_deferred = [
            "Deferred: private Dev repo creation, private Owner repo creation, local-only private root creation, GitHub Desktop private remote configuration, off-boot backup or recovery root implementation, and Public-to-Dev import implementation.",
            "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, PR creation, merge, release, cleanup, FAM-006/Governance/sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0-prebeta execution.",
            "Rejected for the Workstream entry seam: any hidden private setup, silent provider enablement, cache/memory runtime behavior, or action that would make a USER gate look already completed.",
        ]
        source_truth_impact = [
            "Active external branch plan and branch record should preserve Breakpoint 2 as a real FAM-007 product/workstream carrier.",
            "AI Runtime And Trust Architecture remains the cross-family owner for provider boundaries, permission-state, deterministic routing, Trust Journal, AI Operational Cache Governance, local-only proof, and capability-pack readiness.",
            "Review packet should remain branch-specific, freshness-verified, count-consistent, placeholder-free, and explicit that Workstream approval covers the admitted same-branch package with Seam 1 as the entry proof checkpoint, not a one-seam stop.",
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
            "Exact implementation approval text names bounded Workstream package execution with Seam 1 as the entry checkpoint.",
            "Implementation Constraints Created By USER Response preserve all private/runtime/provider/cache/memory gates.",
            "Helper output verifies packet freshness; USER-facing files stay focused on the plan and decision.",
            "Packet digest files agree that Workstream Entry is green and Workstream approval covers the admitted same-branch package with Seam 1 as the entry proof checkpoint.",
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
                "Future-gated boundary controls.",
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
            "Upload the matching timestamped ZIP beside the local USER hub folder after reviewing the packet.",
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
            "Approve the bounded Workstream package with Seam 1 as the entry checkpoint: implement public-safe action-gate registry and exact USER decision proof first, then continue through admitted same-branch seams until Workstream Green, a real blocker, or an explicit USER waiver. Pros: clearest readiness foundation; Cons: no private setup yet; Risk: low.",
            "Revise Workstream proof expectations before implementation. Pros: lets USER tune proof wording, validator expectations, or seam order; Cons: adds packet/source-truth repair; Risk: low.",
            "Waive unresolved review questions and approve bounded Workstream package execution. Pros: unblocks bounded proof work; Cons: records less design feedback; Risk: medium if important proof expectations are not named.",
            "Reject this branch contract and request a narrower carrier. Pros: maximum scope control; Cons: delays Breakpoint 2 readiness; Risk: low but slower.",
        ]
        recommended_direction = (
            "Codex recommends accepting the repaired branch contract and approving bounded Workstream "
            "package execution when USER agrees that the public-safe proof path is correct. Seam 1 is "
            "the entry checkpoint for action-gate and decision-text proof; it is not stop authority "
            "while admitted same-branch Workstream work remains."
        )
        current_scope = [
            "Branch-specific Workstream Entry contract repair.",
            "Completed Workstream Entry result recorded in the packet.",
            "Recommended first seam recorded as Seam 1, Action-gate registry and exact USER decision proof.",
            "Local USER hub packet and timestamped ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the decision path.",
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
                "Upload the matching timestamped ZIP beside the local USER hub folder after reviewing or revising Hardening H1.",
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
                "Future-gated boundary controls.",
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
                "Local USER hub packet and timestamped ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the Hardening H1 next decision.",
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
                "Upload the matching timestamped ZIP beside the local USER hub folder after reviewing or revising LV1/no-visible-runtime proof.",
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
                "Future-gated boundary controls.",
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
                "Local USER hub packet and timestamped ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the Live Validation LV1 next decision.",
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
                "Upload the matching timestamped ZIP beside the local USER hub folder after reviewing or revising PR Readiness Stage 1 analysis.",
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
                "Future-gated boundary controls.",
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
                "Local USER hub packet and timestamped ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the PR Readiness Stage 1 next decision.",
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
                "Local USER hub packet and timestamped ZIP refreshed with the current decision path, file list, and next decision.",
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
                "Upload the matching timestamped ZIP beside the local USER hub folder after reviewing or revising Stage 2.",
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
                "Future-gated boundary controls.",
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
                "Local USER hub packet and timestamped ZIP refreshed; helper output carries technical freshness proof and USER-facing files carry the Stage 2 next decision.",
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
            "Future-gated boundary controls.",
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
                "PR creation, merge, release, cleanup, runtime implementation, provider/model/cache/memory/private actions, sidecar artifacts, and separate Review/Upload taxonomy remain pending USER decisions; timestamped ZIP naming is mandatory active policy.",
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
            "C:\\Nexus USER\\Governance and C:\\Nexus USER\\Governance-YYYYMMDD-HHMMSS.zip: temporary USER review aids.",
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
            "PR creation, merge, release, cleanup, runtime work, FAM-006/FAM-007 mutation, private/provider/cache/memory actions, sidecars, and separate Review/Upload taxonomy remain pending USER decisions; timestamped ZIP naming is mandatory active policy.",
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
    if is_fam007_dev_owner_skeleton and not is_fam007_breakpoint_2:
        plain_english_summary = (
            "This BP2 preview is future-gated until USER accepts or explicitly waives BP1. "
            "If BP1 is accepted, BP2 should plan the public-safe Dev/Owner skeleton readiness "
            "package: Dev readiness, Owner readiness, private root and remote decisions, "
            "public-upstream safety, backup/import deferral, provider/model/runtime/cache/memory "
            "deferral, review-packet proof, and direct validator coverage."
        )
        end_state_vision = (
            "When BP2 is later accepted or waived, USER should understand which public-safe "
            "source-truth, helper, fixture, validator, packet, H1, LV/UTS, rollback, and proof "
            "surfaces will prepare future Dev/Owner skeleton setup while every private/runtime "
            "action remains separately gated."
        )
        what_user_sees = (
            "USER should see a branch-specific engineering plan derived from the accepted BP1 "
            "Dev/Owner skeleton readiness vision, not a Governance PR Readiness plan and not "
            "private setup. The BP2 packet should name the exact future readiness seams and the "
            "proof expected before implementation."
        )
        why_nexus = (
            "This fits Nexus because it keeps AI-edition growth local-first, visible, and "
            "permission-gated. The public branch plans decision and proof surfaces while private "
            "Dev/Owner roots, provider/model behavior, cache behavior, memory, and promotion back "
            "to Main stay under explicit USER control."
        )
        implementation_constraints = [
            "BP2 is pending until BP1 is accepted or explicitly waived.",
            "BP2 may plan public-safe source-truth, fixture, validator, helper, packet, and proof surfaces only.",
            "Private Dev repo creation, Owner repo creation, local-only roots, private remotes, GitHub Desktop private binding, backup/import behavior, provider/model execution, runtime cache behavior, memory behavior, PR, merge, release, cleanup, and v1.8.0 work remain future USER decisions.",
            "Provider-visible data must remain none; sentToProvider=false, canAcceptPrompts=false, prompt/provider/model execution disabled, downloads/network/external calls blocked, memory/learning/personalization inactive, and runtime cache behavior inactive.",
        ]
        rejected_deferred = [
            "Deferred: actual private Dev skeleton setup and Owner skeleton setup.",
            "Deferred: private repo/root/remote creation, GitHub Desktop private binding, backup/import execution, and Public-to-Dev import.",
            "Deferred: provider SDK/model execution, model downloads, runtime provider execution, runtime cache behavior, memory/learning/indexing/retrieval/personalization, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, sibling-worktree mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work.",
        ]
        source_truth_impact = [
            "FAM-007 family vision and AI runtime/trust architecture remain the durable policy context.",
            "The FAM-007 branch record and external branch plan remain the branch-specific planning owners.",
            "BP2 must fold any USER revision that changes edition boundaries, private/public promotion, provider/cache/memory policy, or proof expectations into the proper source-truth owner before BP3.",
        ]
        contract_change_log = [
            "v1 - BR2 admitted the FAM-007 Dev/Owner Skeleton Readiness carrier.",
            "v2 - BP1 packet generated as Branch Vision Review with BP2 remaining future-gated.",
            "v3 - BP1 primary vision file repaired into applied FAM-007 Dev/Owner readiness content.",
        ]
        completion_checklist = [
            "BP1 is accepted or explicitly waived before BP2 is treated as a plan gate.",
            "Accepted BP1 trace is present.",
            "Implementation package summary names Dev readiness, Owner readiness, private root/remote gates, public-upstream safety, backup/import deferral, provider/model/runtime/cache/memory deferral, validation proof, packet proof, H1, LV/UTS, and rollback/safety expectations.",
            "All private/runtime/provider/cache/memory/PR/merge/release/cleanup boundaries remain pending USER decisions.",
            "BP3 / Workstream Entry remains blocked until BP2 is accepted or explicitly waived and orchestration validation is green.",
        ]
        walkthrough = [
            "Review accepted BP1 first; this BP2 preview cannot become green while BP1 is pending.",
            "Confirm whether BP2 should keep Dev and Owner skeleton readiness in one public-safe branch.",
            "Confirm which private root, private remote, GitHub Desktop, backup/import, provider/cache/memory, and public-to-private promotion decisions need matrix proof.",
            "Confirm the required no-leak, provider-state, packet, fixture, validator, H1, and LV/UTS proof before implementation.",
        ]
        surface_map = [
            "USER packet: BP1 primary vision file now; future BP2 engineering plan only after BP1 acceptance or waiver.",
            "Branch record and external branch plan: branch-specific FAM-007 readiness authority and planning owners.",
            "FAM-007 family vision and AI runtime/trust architecture: provider, model, cache, memory, permission, and public/private boundary owners.",
            "Validation surfaces: public leak-prevention, provider-state, branch-planning fixture validation, packet validation, and branch governance validation.",
            "Future proof surfaces: H1 implementation-vs-plan comparison, Live Validation or UTS waiver/proof, and PR Readiness only after later approvals.",
        ]
        implementation_options = [
            "Option A - Plan one public-safe Dev/Owner readiness package in BP2. Pros: keeps coupled trust-boundary gates consistent; Cons: broader BP2; Risk: low when all private/runtime actions stay gated.",
            "Option B - Split Dev and Owner readiness after BP1. Pros: smaller future packets; Cons: higher risk of inconsistent private/public gates; Risk: medium unless USER wants different timelines.",
            "Option C - Plan only an action-gate registry first. Pros: narrowest engineering scope; Cons: delays Dev/Owner skeleton readiness detail; Risk: low but less useful.",
            "Option D - Require BP2 to include a full decision matrix and proof map. Pros: strongest USER clarity; Cons: more planning detail before Workstream; Risk: low.",
        ]
        recommended_direction = (
            "Codex recommends Option A with the Option D decision matrix: keep Dev and Owner "
            "readiness together for BP2, require explicit proof for each private/runtime gate, and "
            "leave actual setup or execution for later USER-approved phases."
        )
        current_scope = [
            "BP1 Branch Vision Review is the current USER decision.",
            "BP2 content in this packet is preview/context only and cannot close the BP2 gate.",
            "The branch remains public-safe and does not create private roots, remotes, provider behavior, cache behavior, memory, or runtime work.",
        ]
        future_scope = [
            "BP2 should plan Dev readiness, Owner readiness, private root/remote gates, public-upstream safety, backup/import deferral, provider/model/runtime/cache/memory deferral, proof requirements, H1, LV/UTS, and rollback/safety.",
            "BP3, Workstream implementation, private setup, provider/model/runtime/cache/memory behavior, PR, merge, release, cleanup, and v1.8.0 remain pending USER decisions.",
        ]
        slc_package_plan = [
            "SLCs remain future engineering route details inside the accepted branch vision.",
            "Candidate future seam families: Dev skeleton readiness, Owner skeleton readiness, private remote/public-upstream safety, backup/import deferral, and provider/model/runtime/cache/memory deferral.",
            "No future seam may execute the private/runtime action it is proving as gated without a separate USER approval.",
        ]
        user_decisions = [
            "Does USER accept, revise, waive, reject, or hold the BP1 Dev/Owner skeleton readiness Branch Vision?",
            "If BP1 is accepted or waived, should BP2 plan one combined Dev/Owner readiness package or split Dev and Owner later?",
            "Which private root, private remote, GitHub Desktop, backup/import, provider/cache/memory, and public-to-private promotion decisions must BP2 prove?",
            "Does USER confirm all private/runtime/provider/cache/memory/PR/merge/release gates remain pending?",
        ]
    if (
        is_fam007_dev_owner_skeleton
        and not is_fam007_breakpoint_2
        and (bp2_branch_plan_packet or bp3_orchestration_packet)
    ):
        accepted_user_response = (
            "BP1 accepted - USER accepted the updated FAM-007 Dev/Owner Skeleton "
            "Readiness Branch Vision as the integrated Option A direction. BP2 may "
            "plan Dev and Owner readiness together, with future Dev oriented toward "
            "a private repo after approval, Owner kept local-private by default, "
            "GitHub Desktop/public-upstream safety made explicit, backup/import "
            "timing planned, provider/runtime/cache/memory behavior deferred, and "
            "lane identity labels carried into proof expectations."
        )
        user_response_text = (
            "Status: Pending USER Response - this BP2 engineering plan is ready for "
            "USER to accept, revise, hold for more options, reject, or explicitly "
            "waive. BP3 and Workstream implementation remain blocked until that "
            "USER disposition is recorded and digested."
        )
        codex_response_digest = (
            "Codex digested the accepted BP1 vision into a BP2 engineering plan. "
            "The plan keeps Dev and Owner skeleton readiness in one public-safe "
            "package, names matrix proof for each private/runtime gate, and keeps "
            "all setup or execution work future-gated until later USER approval."
        )
        workstream_entry_result = (
            "BP3 not started - Workstream Entry / Orchestration Validation remains "
            "pending until USER accepts or explicitly waives this BP2 plan."
        )
        contract_status = (
            "Pending USER Response - USER must accept, revise, reject, request more "
            "options, hold, or explicitly waive this BP2 engineering plan before BP3."
        )
        contract_version = (
            "v5 - USER/ChatGPT BP2 review conditions digested into the integrated "
            "Dev/Owner readiness engineering plan."
        )
        plain_english_summary = (
            "This BP2 plan keeps the selected route as integrated Dev/Owner Skeleton "
            "Readiness and turns the accepted BP1 vision into a public-safe engineering "
            "route. Dev continues toward future private-repo readiness after approval. "
            "Owner defaults to local Git/version history plus local/private/encrypted "
            "rollback, with an Owner private remote only as a future evaluated option. "
            "The branch plans decision and proof surfaces without creating private repos, "
            "private roots, private remotes, GitHub Desktop private binding, backup/import "
            "execution, provider or model execution, cache behavior, memory behavior, PRs, "
            "merges, releases, or cleanup."
        )
        end_state_vision = (
            "When the BP2 plan is accepted and later implemented through approved phases, "
            "USER should have durable source truth, direct validators, fixtures, packet "
            "proof, and no-leak evidence that make future Dev and Owner skeleton setup "
            "decision-ready. The public branch should say which lane owns each decision, "
            "which files or validators prove it, how rollback works, and which future "
            "USER gate is required before any private or runtime action starts."
        )
        what_user_sees = (
            "USER will inspect one primary BP2 decision file under the local USER hub. "
            "It describes the integrated Dev/Owner implementation package, seam plan, "
            "likely future edit/proof surfaces, named validator lanes, backup/import "
            "planning by lane, watermark/identity propagation, rollback plan, risks, "
            "options, and exact BP3 approval text. It is not a private setup script, "
            "not backup/import execution, and not a Workstream implementation approval."
        )
        why_nexus = (
            "This fits Nexus because Dev/Owner AI-edition readiness is a trust-boundary "
            "problem. Planning Dev, Owner, remotes, backups, provider deferral, cache "
            "deferral, memory deferral, and lane identity together keeps the public repo "
            "local-first, inspectable, and USER-controlled while preventing accidental "
            "private or provider-facing activation."
        )
        slc_package_plan = [
            "Seam 1 - action-gate registry and exact USER decision proof: record every future private/runtime action gate and make the BP2/BP3 approval text machine-checkable.",
            "Seam 2 - Dev/Owner readiness matrices: encode Dev private-repo readiness after approval, Owner local Git/version history plus local/private/encrypted rollback as the default baseline, Owner private remote evaluation as optional future work, and public-safe lane boundaries.",
            "Seam 3 - private root/remote and GitHub Desktop safety proof: plan public-upstream, private origin, remote identity proof, fetch/reconcile posture, and public push-prevention checks without configuring remotes or binding GitHub Desktop to a private repo.",
            "Seam 4 - backup/import and provider/runtime deferral proof: plan User/Public settings/preferences/config backup scope, Dev private development recovery, Owner local/private/encrypted backup and rollback, restore proof, and provider-visible-data/cache/memory inactivity proof.",
            "Seam 5 - packet, fixture, validator, and fold-down proof: refresh USER review packet evidence, add direct fixtures where needed, and update source-truth owners only inside approved public-safe scope.",
        ]
        surface_map = [
            "Active FAM-007 branch record: durable branch authority and historical receipt context; update only if BP2 acceptance changes durable branch authority or future-gate wording.",
            "Active FAM-007 branch plan/receipt and external FAM-007 branch plan/state: active BP2 planning posture, accepted BP1 trace, review-gate state, seam map, proof expectations, and future gates.",
            "USER review bundle helper: packet layout, primary BP2 decision-file routing, support-file phase state, timestamped ZIP creation, placeholder scans, packet count checks, and USER-facing metadata exclusion when packet behavior changes.",
            "Validation helper registry and branch-readiness planning fixtures: reusable proof lanes and false-green prevention when validator coverage changes.",
            "Provider-state, public leak-prevention, external-state, source-owner, USER review packet, and branch-governance validators: named proof lanes for BP3 and later Workstream decisions.",
            "AI runtime/trust architecture: durable trust-boundary wording only if USER changes provider-visible data, prompt acceptance, provider execution, downloads, cache, memory, learning, or personalization policy.",
            "FAM-007 family vision files: family-level direction only if USER changes Public/Dev/Owner edition strategy, capability-pack policy, private/public promotion, or lane identity standards.",
        ]
        likely_files_lines = [
            "Active FAM-007 branch record if durable authority, accepted-gate, or future-gate wording changes.",
            "Active FAM-007 external branch plan and branch state for BP2 review posture, accepted BP1 trace, USER response digestion, and next-gate routing.",
            "Review bundle helper if packet behavior, timestamped ZIP generation, support-file phase state, or primary BP2 routing changes.",
            "Validation helper registry if reusable validator/helper coverage changes.",
            "Branch-readiness planning fixtures for accepted BP1 trace, BP2 engineering-plan substance, BP3 blocking while BP2 remains pending, and future root/remote/GitHub Desktop matrix false-green coverage if needed.",
            "Provider-state and public leak-prevention validators/fixtures for no provider execution, no private artifacts, no private paths, and no private remotes.",
            "External-state validation for active branch plan/state consistency.",
            "Source-owner marker validation for any durable source-truth owner touched by later implementation.",
            "AI runtime/trust architecture only if durable provider/cache/memory trust-boundary policy changes.",
            "FAM-007 family vision files only if USER changes family-level edition, private/public, capability-pack, or lane identity direction.",
        ]
        active_branch_files = [
            "Active external branch plan exists at C:\\Nexus Governance State\\branches\\feature_fam_007_dev_owner_skeleton_readiness\\branch_plan.md; it owns active BP2 planning posture, accepted BP1 trace, review-gate state, seam map, proof expectations, and future gates outside the USER-facing packet.",
            "Active external branch state exists at C:\\Nexus Governance State\\branches\\feature_fam_007_dev_owner_skeleton_readiness\\branch_state.md; it records the current carrier posture and packet pointer outside repo-tracked source truth.",
            "Historical repo branch record remains Docs/branch_records/feature_fam_007_dev_owner_skeleton_readiness.md; it is durable authority/context and not a mutable live-state ledger.",
        ]
        user_decisions_intro = (
            "USER may answer in order or respond generally. Useful BP2 feedback includes "
            "Dev/Owner matrix changes, private root or remote posture, GitHub Desktop "
            "binding assumptions, backup/import lane split, watermark/identity "
            "propagation, named proof lanes, future-gated actions, or anything that "
            "would make this FAM-007 Dev/Owner engineering plan wrong before BP3."
        )
        walkthrough = [
            "Open the primary BP2 file and confirm the accepted BP1 Option A trace matches the integrated Dev/Owner readiness direction.",
            "Review the seam plan from action-gate registry through matrix proof, root/remote safety, backup/import deferral, provider/runtime deferral, and packet/validator proof.",
            "Review each matrix and mark any lane, future gate, proof expectation, or rollback rule that needs revision before BP3.",
            "Confirm that the plan stays public-safe and prepares proof only; any private setup or runtime action remains a later USER gate.",
            "Choose accept, revise, route back to BP1, waive, reject, or hold for more examples before BP3.",
        ]
        implementation_options = [
            "Option A - accept the integrated Dev/Owner BP2 plan as written. Pros: keeps coupled private/public trust decisions in one branch; Cons: broader BP2 and BP3 review; Risk: low when all private/runtime actions stay gated.",
            "Option B - accept with changes to a specific matrix or seam. Pros: tunes the plan before BP3; Cons: requires packet/source-truth refresh; Risk: low.",
            "Option C - route back to BP1. Pros: safest if the engineering plan changes the accepted vision; Cons: delays BP3; Risk: low.",
            "Option D - split Dev and Owner into separate future branches. Pros: smaller packages; Cons: higher risk of inconsistent remote, backup, provider, and identity gates; Risk: medium.",
            "Option E - explicitly waive BP2 details and proceed to BP3. Pros: faster; Cons: accepts less planning detail; Risk: medium to high for private-boundary work.",
            "Option F - hold for more examples or proof models. Pros: improves confidence; Cons: delays implementation; Risk: low.",
        ]
        recommended_direction = (
            "Codex recommends accepting the integrated Dev/Owner readiness route after "
            "reviewing the strengthened proof lanes: keep Dev private-repo readiness as "
            "the future direction, keep Owner local Git/version history plus "
            "local/private/encrypted rollback as the default baseline, treat Owner remote "
            "as future evaluated only, require named validator/fixture proof before BP3, "
            "and keep actual private setup, GitHub Desktop private binding, provider/model "
            "work, backup/import execution, cache, memory, PR, merge, release, and cleanup "
            "under later gates."
        )
        current_scope = [
            "Public-safe source-truth, helper, fixture, validator, packet, and proof planning only.",
            "Accepted BP1 trace, BP2 engineering package, seam/SLC route, affected surfaces, proof expectations, H1/LV/UTS expectations, rollback, risks, and exact BP3 approval text.",
            "No private repo, private root, private remote, GitHub Desktop private binding, backup/import execution, provider/model execution, cache behavior, memory behavior, PR, merge, release, cleanup, or sibling-worktree mutation.",
        ]
        future_scope = [
            "BP3 Workstream Entry / Orchestration Validation after BP2 acceptance or waiver.",
            "Workstream implementation only after BP1 and BP2 are accepted or waived, BP3 is green or waived, and USER separately approves bounded Workstream execution for the admitted same-branch package or explicitly named initial seam sequence.",
            "Private Dev skeleton setup, Owner skeleton setup, private repos, private roots, private remotes, GitHub Desktop private binding, backup/import execution, provider/model/runtime/cache/memory behavior, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, issue mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain later USER decisions.",
        ]
        implementation_constraints = [
            "BP2 may plan public-safe source-truth, helper, fixture, validator, packet, H1, LV/UTS, rollback, and proof surfaces.",
            "BP2 may not execute the private/runtime actions it describes as future gates.",
            "BP2 may not create private repos, private roots, private remotes, GitHub Desktop private binding, backup/import execution, provider/model/runtime/cache/memory behavior, or Dev launcher/assets migration execution.",
            "Provider-visible data remains none; sentToProvider=false; canAcceptPrompts=false; prompt/provider/model execution remains disabled; downloads/network/external calls remain blocked; runtime cache behavior remains inactive; memory/learning/personalization remains inactive.",
            "Any USER change that alters edition boundaries, public-to-private promotion, provider/cache/memory policy, or reusable lane identity must fold into the proper durable source-truth owner before BP3 relies on it.",
        ]
        rejected_deferred = [
            "Deferred: private Dev skeleton setup, private Owner skeleton setup, private Dev repo creation, private Owner repo or remote creation, local-only private roots, private remotes, and GitHub Desktop private binding.",
            "Deferred: dev launcher/assets/tool transfer, recreation, removal from User/Public, or import into a private Dev path.",
            "Deferred: backup/import execution, public-to-private import, User/Public backup implementation, Dev recovery implementation, Owner encrypted recovery or rollback implementation.",
            "Deferred: provider SDKs, model downloads, provider/model execution, runtime provider execution, cache behavior, memory, learning, indexing, retrieval, personalization, voice/Core sync, shortcut/installer work, PR, merge, release, cleanup, issue mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work.",
        ]
        source_truth_impact = [
            "External branch plan should record BP1 accepted and BP2 pending review as active planning posture.",
            "Branch record remains durable authority/history and should not become a mutable live ledger.",
            "FAM-007 family vision and AI runtime/trust architecture remain reusable policy owners; accepted reusable changes route there only if USER changes family-level policy.",
            "Review packet is a temporary USER review aid; accepted BP2 outcomes later fold into durable repo owners or approved external operational state.",
        ]
        contract_change_log = [
            "v1 - BR2 admitted the FAM-007 Dev/Owner Skeleton Readiness carrier.",
            "v2 - BP1 packet generated as Branch Vision Review.",
            "v3 - BP1 repaired into applied integrated Dev/Owner Option A vision.",
            "v4 - USER accepted BP1; BP2 generated as engineering-plan-first review with required matrices and future-gated boundaries.",
            "v5 - USER/ChatGPT BP2 review conditions digested: strengthened future edit/proof surfaces, named validator lanes, backup/import lane details, Owner rollback baseline, Owner remote evaluation boundary, and watermark/identity propagation.",
        ]
        completion_checklist = [
            "Accepted BP1 Option A trace is present.",
            "BP2 implementation package summary, branch scope size test, seams/SLCs, affected surfaces, likely files, validators/helpers, proof requirements, H1/LV/UTS expectations, rollback/safety plan, risks, future gates, and exact BP3 approval text are present.",
            "Edition/Lane, Dev Readiness, Owner Readiness, Private Root/Remote, GitHub Desktop, Backup/Import, Provider/Runtime/Cache/Memory, Watermark/Identity, Proof/Validation, and Future USER Gate matrices are present.",
            "USER-facing files avoid live operational ledgers, raw commit values, upload byte-proof values, mutable validator run state, live pull-request posture, and command-wall boundary wording.",
            "BP3 and Workstream implementation remain blocked until BP2 is accepted or explicitly waived and later gates are green and approved.",
        ]
        user_decisions = [
            "Does USER accept the updated integrated Dev/Owner BP2 engineering plan as written?",
            "Does any listed future implementation/edit surface need to be added, removed, or narrowed before BP3?",
            "Are the named proof lanes sufficient for BP3: provider-state, public leak-prevention, external-state, branch-readiness planning fixtures, USER review packet validation, source-owner marker validation, and future root/remote/GitHub Desktop false-green fixture coverage if needed?",
            "Does USER accept Owner local Git/version history plus local/private/encrypted rollback as the default baseline, with Owner private remote only as a future evaluated option?",
            "Does USER accept the backup/import lane split and watermark/identity propagation requirements as BP2 planning constraints?",
            "Does USER confirm all private/runtime/provider/cache/memory/backup-import-execution/PR/merge/release gates remain pending?",
        ]
        design_ballot = [
            "Accept BP2 as written and authorize BP3 Workstream Entry / Orchestration Validation only.",
            "Accept BP2 with listed changes, then regenerate the BP2 packet for confirmation.",
            "Route back to BP1 because the plan changes the accepted vision.",
            "Explicitly waive remaining BP2 questions and authorize BP3 only.",
            "Reject this branch plan and request a narrower or different carrier.",
            "Hold for more examples, risks, or proof models.",
        ]
        response_structure = [
            "Decision: accept, revise, route back to BP1, waive, reject, or hold.",
            "Matrix or seam changes requested.",
            "Must-have proof requirements.",
            "Future-gated boundary controls.",
            "Questions before BP3.",
            "General response.",
        ]
        digest_structure = [
            "USER BP2 disposition.",
            "Accepted BP2 line items.",
            "Revised BP2 line items.",
            "Rejected or deferred ideas.",
            "Implementation constraints created from USER response.",
            "Source-truth updates required.",
            "Review packet updates required.",
            "Whether BP3 may begin.",
            "Next USER decision needed.",
        ]
        extra_plan_sections = [
            "## Integrated Dev/Owner Readiness Matrix",
            "",
            "| Lane | BP2 planned outcome | Current branch scope | Future USER gate | Proof needed |",
            "| --- | --- | --- | --- | --- |",
            "| Dev | Future private-repo-oriented readiness with public-upstream safety and dev asset inventory planning. | Public-safe plan, fixtures, validators, and review proof only. | Private Dev repo/root/remote creation and GitHub Desktop binding. | Action-gate registry, no-leak scan, public-upstream push-prevention plan, and fixture coverage. |",
            "| Owner | Local-private baseline with local Git/version history, no public exposure, and no default remote. | Public-safe plan and proof of gated Owner choices only. | Owner private root/remote choice, encrypted recovery, and any remote evaluation. | Matrix proof, no private path/remote/token leakage, rollback plan, and future-gate wording. |",
            "",
            "## Edition / Lane Matrix",
            "",
            "| Edition / Lane | Identity posture | Source control posture | Public branch role | Future boundary |",
            "| --- | --- | --- | --- | --- |",
            "| User/Public | Nexus Desktop AI or Nexus Desktop AI - Pre-Beta. | Normal public repo posture. | Keep public-safe product and proof context. | No private assets or provider execution. |",
            "| Dev | Nexus Desktop AI - DEV PRIVATE after approval. | Future private Dev repo with fetch-only public-upstream plan. | Plan readiness and gates only. | Repo/root/remote creation remains future-gated. |",
            "| Owner | Nexus Owner - Local Private unless later revised. | Local Git/version-history baseline; no default remote. | Plan Owner privacy gates only. | Remote or shared backup model remains future-gated. |",
            "",
            "## Dev Readiness Matrix",
            "",
            "| Dev item | BP2 plan | Likely proof | Future USER decision |",
            "| --- | --- | --- | --- |",
            "| Private Dev repo direction | Treat as preferred future path after approval. | Branch plan row and gate registry. | Create private Dev repo/root/remote. |",
            "| Dev launcher/assets/tools inventory | Classify transfer, recreation, removal, or future import candidates. | Public-safe inventory schema or fixture; no private paths. | Execute transfer/import/removal. |",
            "| Public-upstream relationship | Plan fetch/reconcile from public Main and public push prevention. | Validator fixture and packet proof. | Configure private remotes or GitHub Desktop binding. |",
            "",
            "## Owner Readiness Matrix",
            "",
            "| Owner item | BP2 plan | Likely proof | Future USER decision |",
            "| --- | --- | --- | --- |",
            "| Local Git/version history | Baseline Owner safety model. | Branch plan and H1 comparison. | Create Owner root or repo. |",
            "| No public exposure path | Preserve Owner-private boundary. | Public leak-prevention and no private artifact checks. | Any Owner remote or sharing path. |",
            "| Optional private Owner remote | Evaluate only if BP2/BP3 prove it safer than local-only. | Risk matrix and explicit future gate. | Configure Owner private remote. |",
            "",
            "## Private Root / Remote Matrix",
            "",
            "| Surface | Current branch scope | Future gate | Proof / validation |",
            "| --- | --- | --- | --- |",
            "| Private roots | Plan labels and constraints only. | Local-only private root creation. | No private path leakage and gate registry row. |",
            "| Private origin | Plan naming and safety posture only. | Private remote configuration. | Remote identity proof plan and public push-prevention fixture. |",
            "| Public-upstream | Plan fetch-only relationship. | Actual private repo configuration. | Public/upstream terminology checks and no private URL output. |",
            "",
            "## GitHub Desktop Binding Matrix",
            "",
            "| Lane | Default posture | BP2 plan | Future gate |",
            "| --- | --- | --- | --- |",
            "| User/Public | Public repo binding. | Preserve normal binding. | None in BP2. |",
            "| Dev | No binding yet. | Plan private Dev binding proof and safeguards. | GitHub Desktop private remote configuration. |",
            "| Owner | Local Git/no remote baseline. | Evaluate private remote only as future option. | Owner private binding approval. |",
            "",
            "## Backup / Import Matrix",
            "",
            "| Lane | BP2 plan | Current scope | Future gate | Restore / exclusion proof |",
            "| --- | --- | --- | --- | --- |",
            "| User/Public | Settings/preferences/config backup posture and product-safe export/import scope. | Plan and proof only. | Backup/import implementation. | Restore proof must use public-safe settings/config fixtures and exclude private Dev/Owner material. |",
            "| Dev | Private development recovery posture tied to the future private Dev repo relationship. | Plan and proof only. | Dev recovery implementation or Public-to-Dev import. | Dev backup material and private test fixtures must remain outside User/Public output and public review packets. |",
            "| Owner | Local/private/encrypted backup baseline plus local Git rollback expectation. | Plan and proof only. | Owner backup/recovery root execution or future remote evaluation. | Restore proof must preserve Owner-only privacy, stay outside User/Public and Dev, and define criteria before any Owner remote is evaluated. |",
            "",
            "## Provider / Runtime / Cache / Memory Deferral Matrix",
            "",
            "| Boundary | Required BP2 state | Proof |",
            "| --- | --- | --- |",
            "| Provider-visible data | none | Provider-state validator fixture. |",
            "| Prompt acceptance | canAcceptPrompts=false | Provider-state validator fixture. |",
            "| Provider/model execution | disabled | Provider-state and no network/download assertions. |",
            "| Runtime cache | inactive | Source-truth and fixture proof. |",
            "| Memory/learning/personalization | inactive | Memory/private artifact leak-prevention proof. |",
            "",
            "## Watermark / Identity Matrix",
            "",
            "| Artifact / surface | User/Public label | Dev label | Owner label | Propagation proof |",
            "| --- | --- | --- | --- | --- |",
            "| UI/window title | Nexus Desktop AI / Pre-Beta | Nexus Desktop AI - DEV PRIVATE after approval | Nexus Owner - Local Private after approval | UI proof or manifest row before any private lane UI exists. |",
            "| Launcher identity | Public launcher identity | Dev launcher identity after future setup | Owner local launcher identity after future setup | Launcher/shortcut manifest proof; no launcher migration execution in BP2. |",
            "| Diagnostics | Public-safe diagnostic labels | Dev-private diagnostic labels after approval | Owner-local diagnostic labels after approval | Diagnostic sample/fixture excludes private paths and secrets. |",
            "| Logs | Public-safe log labels | Dev-private log labels after approval | Owner-local log labels after approval | Log proof excludes private prompts, memory, tokens, and private paths. |",
            "| Screenshots/proof | Public-safe proof context | Dev proof only after future approval | Owner proof only after future approval | Review-proof labels show lane without exposing private artifacts. |",
            "| Review packets | Public FAM-007 packet labels | Dev packet labels only after future private approval | Owner packet labels only after future private approval | USER packet validation rejects private artifacts in public branch. |",
            "| Backup/export packages | Public-safe export label | Dev-private export label after approval | Owner-local/private export label after approval | Export manifest proof preserves lane and excludes cross-lane leakage. |",
            "| Generated manifests | Public-safe manifest owner | Dev-private manifest owner after approval | Owner-local manifest owner after approval | Manifest fixtures prove lane identity and future-gate state. |",
            "",
            "## Proof / Validation Matrix",
            "",
            "| Proof class | Required proof | Candidate validator/helper |",
            "| --- | --- | --- |",
            "| Branch planning packet | Primary BP2 file, timestamped ZIP, no stale preview text, no metadata drift. | dev/orin_user_review_bundle.py |",
            "| Private-boundary safety | No private path, token, remote URL, prompt, memory, model artifact, private automation, or private artifact in public branch. | dev/orin_public_leak_prevention_validation.py |",
            "| Provider deferral | Provider-visible data none, prompt/model execution disabled, downloads blocked, cache/memory inactive. | dev/orin_ai_provider_state_validation.py |",
            "| Planning gate proof | BP2 requires accepted BP1 trace; BP3 blocks while BP2 pending. | dev/orin_branch_readiness_planning_fixture_validation.py |",
            "| External-state consistency | External branch plan/state records BP2 reviewability and pending USER gate without making repo files live ledgers. | dev/orin_external_state_validation.py |",
            "| Source owner integrity | Any touched durable source-truth owner keeps valid ownership markers. | dev/orin_source_owner_marker_validation.py |",
            "| Future root/remote/GitHub Desktop matrix | Add false-green fixture coverage if BP3 or later implementation introduces root, remote, or GitHub Desktop proof rows. | dev/orin_branch_readiness_planning_fixture_validation.py |",
            "",
            "## Future USER Gate Matrix",
            "",
            "| Future gate | Required before action |",
            "| --- | --- |",
            "| BP3 | USER accepts, revises into confirmation, or explicitly waives BP2. |",
            "| Workstream implementation | BP1 and BP2 accepted or waived, BP3 green or waived, and separate bounded implementation approval. |",
            "| Private Dev / Owner setup | Separate USER approval naming root/repo/remote scope. |",
            "| Provider/model/cache/memory behavior | Separate USER approval plus provider-state proof. |",
            "| PR / merge / release / cleanup | Separate phase approvals after implementation, H1, and LV gates. |",
            "",
        ]
    if is_fam007_dev_owner_skeleton and not is_fam007_breakpoint_2 and bp3_orchestration_packet:
        accepted_user_response = (
            "BP2 accepted - USER accepted the cleaned FAM-007 Dev/Owner Skeleton "
            "Readiness engineering plan. The accepted plan keeps Dev and Owner "
            "readiness together, points Dev toward future private-repo readiness "
            "after approval, keeps Owner local-private by default, evaluates any "
            "Owner private remote only as future work, and preserves every "
            "private/runtime/provider/cache/memory gate."
        )
        user_response_text = (
            "Status: Accepted by USER - this BP2 support file is closed as the "
            "accepted engineering-plan context for the active BP3 Workstream Entry / "
            "Orchestration Validation packet."
        )
        codex_response_digest = (
            "Codex digested USER BP2 acceptance into BP3 readiness context. BP3 "
            "must verify that the accepted BP2 plan implements the accepted BP1 "
            "vision, that seams/SLCs trace to both contracts, and that Workstream "
            "implementation remains blocked until USER later approves a bounded seam."
        )
        workstream_entry_result = (
            "BP3 active - Workstream Entry / Orchestration Validation is the "
            "current review gate. BP3 may recommend the first bounded Workstream "
            "seam, but this packet does not authorize Workstream implementation."
        )
        contract_status = (
            "Complete - USER accepted the BP2 Branch Plan Contract; BP3 is the "
            "active Workstream Entry / Orchestration Validation gate."
        )
        contract_version = (
            "v6 - BP2 acceptance digested into BP3 orchestration-readiness support context."
        )
        plain_english_summary = (
            "This support file records the accepted BP2 engineering plan for the "
            "FAM-007 Dev/Owner Skeleton Readiness carrier. The active packet is BP3: "
            "it checks whether the accepted vision and accepted plan are ready to "
            "become a bounded Workstream implementation request later."
        )
        what_user_sees = (
            "The primary BP3 decision file lives under USER Review. This BP2 file "
            "is supporting context under Review Aids: it shows the accepted plan "
            "that BP3 must trace, including Dev/Owner readiness matrices, root/remote "
            "gates, GitHub Desktop safety, backup/import deferral, provider/runtime/"
            "cache/memory deferral, proof expectations, H1/LV/UTS expectations, and "
            "rollback posture."
        )
        current_scope = [
            "BP3 Workstream Entry / Orchestration Validation packet generation and reviewability.",
            "Accepted BP1 and accepted BP2 traceability proof.",
            "Whole-package Workstream orchestration review only; no Workstream implementation.",
        ]
        future_scope = [
            "Workstream implementation remains pending a later explicit USER decision after BP3 review.",
            "Private Dev/Owner setup, private roots/remotes, GitHub Desktop private binding, backup/import execution, provider/model/runtime/cache/memory behavior, PR, merge, release, cleanup, sibling mutation, AI Product Contract import, Private Dev ORIN import, and v1.8.0 work remain future-gated.",
        ]
        user_decisions = [
            "Does USER approve, revise, waive, reject, or hold BP3 Workstream Entry / Orchestration Validation?",
            "Does USER agree the accepted BP2 plan implements the accepted BP1 vision without changing the Dev/Owner direction?",
            "Does USER agree Seam 1 should be the entry implementation checkpoint for the bounded Workstream package after separate Workstream approval?",
            "Does USER confirm all private/runtime/provider/cache/memory/PR/merge/release gates remain pending?",
        ]
        completion_checklist = [
            "BP1 Contract Status is Complete or Waived by USER.",
            "BP2 Contract Status is Complete or Waived by USER.",
            "BP3 packet reviewability is Reviewable while BP3 USER approval remains pending.",
            "Seam/SLC traceability to BP1 and BP2 is present.",
            "Workstream implementation remains pending separate USER approval.",
        ]
        implementation_options = [
            "Approve BP3 as reviewable and green, then request the separate bounded Workstream package implementation approval packet with the entry seam named.",
            "Revise BP3 orchestration order, proof expectations, or first-seam recommendation before implementation approval is considered.",
            "Waive unresolved BP3 questions and proceed to a separate bounded Workstream approval packet.",
            "Reject or hold BP3 and keep the branch in Branch Planning.",
        ]
        recommended_direction = (
            "Codex recommends BP3 approval only if USER agrees the accepted BP2 plan "
            "faithfully implements BP1, the first Workstream seam starts with "
            "public-safe action-gate registry and exact USER decision proof, and all "
            "private/runtime/provider/cache/memory actions remain future-gated."
        )
        user_decisions_intro = (
            "USER is reviewing BP3 now. This support file confirms BP2 is accepted; "
            "the active decision is whether BP3 orchestration is correct before any "
            "later bounded Workstream approval is requested."
        )
        design_ballot = [
            "Approve BP3 as recommended.",
            "Approve BP3 with changes.",
            "Revise BP3 and regenerate the packet.",
            "Waive unresolved BP3 questions.",
            "Reject or hold BP3.",
        ]
        response_structure = [
            "Decision: approve, revise, waive, reject, or hold BP3.",
            "Required orchestration or proof changes, if any.",
            "First-seam preference or constraints.",
            "Future-gated boundary controls.",
            "General response.",
        ]
        digest_structure = [
            "USER BP3 disposition.",
            "Accepted or revised orchestration order.",
            "First bounded Workstream seam approved for a later packet, if any.",
            "Implementation constraints created by USER response.",
            "Source-truth or packet updates required.",
            "Next USER decision needed.",
        ]
    normalized_contract_status = contract_status.casefold()
    if normalized_contract_status.startswith("waived by user"):
        user_gate_state = "USER Waived - explicit USER waiver recorded for this BP2 gate."
        user_response_proof = "Waived by USER - BP2 gate has explicit USER waiver proof."
        user_response_digested = "Digested - waiver preserved as implementation constraint."
    elif normalized_contract_status.startswith("complete"):
        user_gate_state = "USER Accepted - USER accepted the final BP2 Branch Plan Contract."
        user_response_proof = "Accepted by USER - BP2 gate has USER acceptance proof."
        user_response_digested = "Digested - USER response converted into implementation constraints."
    else:
        user_gate_state = "Pending USER Review - packet is reviewable but USER has not accepted or waived this gate."
        user_response_proof = "Pending USER Response - BP2 gate remains open."
        user_response_digested = "Pending USER Response - Codex has not digested a final USER disposition."
    bp3_approval_text = (
        "BP3 approval text applies only when BP1 and BP2 are accepted or explicitly waived and BP3 validation is green. This PR Readiness packet does not request BP3 implementation approval."
        if pr_readiness_stage1_packet
        else (
            "BP3 is the active Workstream Entry / Orchestration Validation packet. "
            "BP3 may recommend an entry Workstream seam for a later USER "
            "decision, but this packet does not authorize Workstream implementation."
        )
        if bp3_orchestration_packet
        else (
            "BP3 may begin only after USER accepts or explicitly waives this BP2 engineering plan. This BP2 packet does not start BP3 and does not authorize Workstream implementation."
        )
    )

    lines = [
        f"# USER Branch Plan Review - {title}",
        "",
        "## Contract Status",
        "",
        contract_status,
        "",
        "## Packet Reviewability State",
        "",
        "Reviewable - helper generated this packet for USER inspection.",
        "",
        "## USER Gate State",
        "",
        user_gate_state,
        "",
        "## USER Response Proof",
        "",
        user_response_proof,
        "",
        "## USER Response Digested",
        "",
        user_response_digested,
        "",
        "## Acceptance / Waiver / Revision / Rejection Receipt",
        "",
        user_response_proof,
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
        *_markdown_lines(likely_files_lines),
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
        *extra_plan_sections,
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
        bp3_approval_text,
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
        user_decisions_intro,
        "",
        *_markdown_lines(user_decisions),
        "",
        "## USER Response",
        "",
        user_response_text
        or accepted_user_response
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
    normalized_decision = exact_user_decision.casefold()
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
        "pr readiness stage 1 analysis" in normalized_decision
    )
    bp3_packet = (
        source_branch == "feature/fam-007-dev-owner-skeleton-readiness"
        and (
            "bp3" in normalized_decision
            or "workstream entry / orchestration" in normalized_decision
            or "orchestration validation" in normalized_decision
        )
    )
    workstream_package_approval_packet = (
        source_branch == "feature/fam-007-dev-owner-skeleton-readiness"
        and any(
            marker in normalized_decision
            for marker in BRANCH_PLANNING_IMPLEMENTATION_REQUEST_MARKERS
        )
        and not any(
            marker in normalized_decision
            for marker in BRANCH_PLANNING_IMPLEMENTATION_BLOCKING_MARKERS
        )
    )
    bp1_packet = (
        "bp1 branch vision" in normalized_decision
        and "authorize bp2 user branch plan review only" in normalized_decision
    )
    bp2_packet = (
        not bp1_packet
        and not bp3_packet
        and (
            "bp2 user branch plan review" in normalized_decision
            or "bp2 branch plan review" in normalized_decision
        )
    )
    packet_status = (
        "bp1 branch vision review - BP1 Branch Vision Review remains pending "
        "USER acceptance, revision, waiver, rejection, or hold; BP2 remains pending."
        if bp1_packet
        else
        "bp2 branch plan review - accepted BP1 Branch Vision is the planning basis; "
        "BP2 USER Branch Plan Review packet is Reviewable; USER acceptance, revision, "
        "waiver, rejection, or hold remains pending; BP3 remains pending."
        if bp2_packet
        else
        "implementation-ready - BP1, BP2, and BP3 are accepted; bounded Workstream "
        "package implementation is approved by this packet with Seam 1 as the entry "
        "checkpoint and continuation governed until Workstream Green, a real blocker, "
        "or explicit USER waiver."
        if workstream_package_approval_packet
        else
        "bp3 orchestration review - accepted BP1 Branch Vision and accepted BP2 "
        "Branch Plan are the traceability basis; BP3 Workstream Entry / "
        "Orchestration Validation packet is Reviewable; USER BP3 approval, "
        "revision, waiver, rejection, or hold remains pending; Workstream "
        "implementation remains pending separate USER approval."
        if bp3_packet
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
    bp3_readiness_contract = ""
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
    elif bp2_packet:
        analysis_status = (
            "Analysis Summary: BP2 USER Branch Plan Review packet for the active "
            "Branch Planning carrier."
        )
        implementation_posture = (
            "Implementation Posture: BP2 is reviewable but not accepted; BP3, "
            "Workstream implementation, private setup, runtime/provider/cache/memory "
            "behavior, PR, merge, release, cleanup, and sibling-worktree mutation "
            "remain pending USER decisions."
        )
        recommended_seam = (
            "Recommended Next Phase: BP2 USER decision; BP3 Workstream Entry / "
            "Orchestration Validation may be prepared only if USER accepts or "
            "explicitly waives BP2."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes accepted BP1 Branch Vision context, "
            "FAM-007 family vision, Public/Dev/Owner boundary plan, AI Runtime And "
            "Trust Architecture, active branch authority record, branch artifact rules, "
            "phase governance, execution rules, validation registry, backlog, roadmap, "
            "and worktree-slot context needed for the BP2 engineering-plan decision."
        )
        checklist_status = (
            "Checklist Focus: BP2 Branch Plan Review - accepted BP1 trace, branch "
            "scope size, seam/SLC route, affected surfaces, likely files, validators, "
            "proof requirements, H1/LV/UTS expectations, rollback, risks, future-gated "
            "decisions, and exact BP3 approval text are represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER_BRANCH_PLAN_REVIEW.md as the primary "
            "BP2 decision file, USER_BRANCH_VISION_REVIEW.md as supporting accepted "
            "vision context, required digest/checklist files, and copied source-truth "
            "files are loaded and digestible for USER review; BP2 remains pending USER "
            "acceptance, revision, waiver, rejection, or hold."
        )
    elif bp3_packet:
        bp3_readiness_contract = (
            "\n## Plain-Language BP3 Readiness Summary\n\n"
            "BP3 is the final Branch Planning readiness check before a later "
            "Workstream implementation approval can be considered. This packet "
            "confirms that the accepted BP1 Branch Vision and accepted BP2 Branch "
            "Plan give Codex enough public-safe direction to prepare a Workstream "
            "route, while Workstream implementation itself remains a separate "
            "future USER decision.\n\n"
            "The branch vision and plan stay focused on FAM-007 Dev/Owner Skeleton "
            "Readiness: public-safe proof that future Dev and Owner skeleton setup "
            "can be made decision-ready without creating private repos, private "
            "roots, private remotes, provider execution, runtime cache behavior, "
            "memory behavior, backup/import execution, PR work, merge work, release "
            "work, cleanup, or sibling-worktree mutation during BP3.\n\n"
            "## Accepted BP1 Vision Traceability\n\n"
            "- BP1 established the product direction: make Dev/Owner skeleton "
            "readiness understandable, reviewable, and gated before any private "
            "setup occurs.\n"
            "- BP1 kept the public repo as the place for public-safe readiness "
            "contracts, proof expectations, and USER decisions.\n"
            "- BP1 preserved future-gated boundaries for Dev private repo setup, "
            "Owner local-private setup, private remotes, backup/import behavior, "
            "provider/model/runtime/cache/memory behavior, voice/Core sync, "
            "shortcuts/installers, PR, merge, release, cleanup, AI Product "
            "Contract import, Private Dev ORIN import, and v1.8.0 work.\n\n"
            "## Accepted BP2 Plan Traceability\n\n"
            "- BP2 converted the accepted vision into an engineering route: one "
            "coherent FAM-007 branch with sequenced seams instead of separate "
            "single-control branches.\n"
            "- BP2 identified the source-truth fold-down, helper, validator, "
            "fixture, packet, and external-state proof surfaces needed before "
            "implementation can be requested.\n"
            "- BP2 kept Workstream scope public-safe: proof artifacts and validators "
            "may be prepared, while actual private setup, runtime activation, "
            "provider calls, cache/memory behavior, backup/import execution, and "
            "release actions stay future-gated.\n\n"
            "## Proposed Workstream Implementation Order\n\n"
            "1. Seam 1 - Action-gate registry and exact USER decision proof: create "
            "the public-safe registry that lists every gated Dev, Owner, private, "
            "runtime, provider, backup/import, PR, merge, release, cleanup, and "
            "sibling-worktree action with its pending USER decision.\n"
            "2. Seam 2 - Dev/Owner readiness matrices: add public-safe matrices that "
            "show what future Dev and Owner skeleton readiness will require, "
            "without creating private repos, roots, remotes, or runtime behavior.\n"
            "3. Seam 3 - Private root/remote and GitHub Desktop safety proof: prove "
            "that private roots, private remotes, GitHub Desktop private binding, "
            "and related credentials remain absent until USER explicitly approves "
            "that future setup.\n"
            "4. Seam 4 - Backup/import and provider/runtime/cache/memory deferral "
            "proof: prove backup/import, provider/model execution, downloads, "
            "runtime execution, cache behavior, memory, learning, indexing, "
            "retrieval, personalization, and voice/Core sync remain inactive.\n"
            "5. Seam 5 - Packet, fixture, validator, and fold-down proof: fold the "
            "accepted constraints into durable owners, add deterministic validation, "
            "and refresh the USER packet without turning review files into live "
            "operational ledgers.\n\n"
            "## Seam / SLC Readiness Assessment\n\n"
            "- Seam 1 readiness: ready to request after BP3 acceptance because it is "
            "public-safe, decision-proof centered, and reversible.\n"
            "- Seam 2 readiness: depends on Seam 1 registry names and exact pending "
            "decision wording so the matrices trace to accepted gates.\n"
            "- Seam 3 readiness: depends on registry and matrix proof so absence of "
            "private roots/remotes and GitHub Desktop private binding can be checked "
            "directly.\n"
            "- Seam 4 readiness: depends on prior gate proof so backup/import and "
            "provider/runtime/cache/memory deferral can be asserted without runtime "
            "activation.\n"
            "- Seam 5 readiness: depends on completed proof surfaces so fixtures, "
            "validators, packet refresh, and source-truth fold-down can check the "
            "whole accepted route.\n\n"
            "## Expected Files / Helpers / Validators / Fixtures / Review Artifacts\n\n"
            "- Source-truth surfaces: FAM-007 family vision, AI runtime and trust "
            "architecture, phase governance, branch artifact rules, validation "
            "registry, active branch authority, external branch plan, and external "
            "branch state.\n"
            "- Helper surfaces: USER review bundle generation and packet decision-path "
            "checks for BP1, BP2, BP3, Workstream, Hardening, Live Validation, PR "
            "Readiness, and Release Readiness separation.\n"
            "- Validator and fixture surfaces: branch-readiness planning fixtures, "
            "public leak prevention, provider-state inactivity, external-state "
            "validation, governance efficiency checks, source-owner markers, release "
            "body checks, and branch governance checks.\n"
            "- USER review artifacts: START_HERE.md as the plain-language index, this "
            "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md as the primary BP3 decision file, "
            "accepted BP1/BP2 review aids, source-truth context copies, and the "
            "timestamped upload ZIP generated from the local USER hub.\n\n"
            "## Direct Proof Plan\n\n"
            "- No-private-action proof: every private Dev/Owner repo, root, remote, "
            "credential, private artifact, and GitHub Desktop private binding remains "
            "future-gated.\n"
            "- Public-leak prevention: proof artifacts contain public-safe descriptions "
            "only and exclude private URLs, tokens, secrets, private paths, prompt "
            "payloads, model artifacts, memory content, and private automation data.\n"
            "- Provider-state inactivity: provider-visible data remains none, "
            "sentToProvider remains false, canAcceptPrompts remains false, and "
            "prompt/provider/model execution remains disabled until a future USER "
            "decision changes that gate.\n"
            "- Runtime/cache/memory deferral: downloads, network/external calls, runtime "
            "provider execution, cache behavior, memory, learning, indexing, retrieval, "
            "and personalization remain inactive.\n"
            "- GitHub Desktop binding absence: private remote setup and GitHub Desktop "
            "private binding remain pending USER decisions, with proof based on "
            "absence of created private remotes or configured private roots.\n"
            "- Backup/import deferral: off-boot backup roots, recovery roots, and "
            "public-to-private import execution remain pending USER decisions.\n"
            "- Artifact identity proof: packet folder and timestamped ZIP are generated "
            "as a matched pair from the local USER hub without sidecars or reused ZIP "
            "names.\n"
            "- External-state proof: mutable active posture remains in external state, "
            "helper output, validator output, or Codex digest rather than durable repo "
            "docs.\n\n"
            "## Rollback And Reversibility Posture\n\n"
            "The proposed Workstream route is reversible because the first seams create "
            "public-safe source-truth, helper, fixture, validator, packet, and external "
            "state proof only. If a seam introduces drift, Codex can revert the focused "
            "commit, regenerate the local USER packet, and restore the prior external "
            "state receipt without undoing private setup or runtime behavior because "
            "those actions are outside this route.\n\n"
            "## Drift Controls\n\n"
            "- User/Public lane: keep USER review files readable and decision-focused; "
            "technical proof stays in helper output, validator output, Codex digest, or "
            "external state.\n"
            "- Dev lane: keep Dev private repo, private root, private remote, provider "
            "SDK/model execution, downloads, and runtime activation behind explicit "
            "future USER gates.\n"
            "- Owner lane: keep Owner local-private setup, backup/recovery roots, "
            "public-to-private import behavior, memory behavior, voice/Core sync, and "
            "installer/shortcut behavior behind explicit future USER gates.\n"
            "- Governance lane: keep BP1 as vision, BP2 as engineering plan, BP3 as "
            "orchestration validation, Workstream as implementation, Hardening as "
            "pressure-testing, Live Validation as USER proof, and PR/Release as "
            "separate approval boundaries.\n\n"
            "## Unresolved Blockers And Pending USER Decisions\n\n"
            "No BP3 file repair authorizes implementation. USER still decides whether "
            "to accept, revise, waive, reject, or hold BP3. Workstream implementation "
            "requires a separate later approval after BP3 is accepted or waived. Every "
            "private setup, provider/runtime/cache/memory action, backup/import action, "
            "PR, merge, release, cleanup, sibling mutation, AI Product Contract import, "
            "Private Dev ORIN import, and v1.8.0 action remains future-gated.\n\n"
            "## Codex Readiness Recommendation\n\n"
            "Codex recommends accepting BP3 as a Branch Planning readiness contract "
            "only if USER agrees that the accepted BP1 vision and accepted BP2 plan "
            "are still the right traceability basis and that Seam 1 should be the "
            "first future Workstream request. This recommendation is not Workstream "
            "implementation approval.\n\n"
            "## Specific USER Readiness Questions\n\n"
            "- Does the accepted BP1 vision still describe the FAM-007 Dev/Owner "
            "Skeleton Readiness end-state USER wants?\n"
            "- Does the accepted BP2 plan still describe the correct public-safe "
            "engineering route for that vision?\n"
            "- Is Seam 1 the right first future Workstream seam, or should another "
            "proof surface come first?\n"
            "- Are the Dev, Owner, private, provider, runtime, cache, memory, backup, "
            "import, PR, merge, release, and cleanup gates preserved clearly enough?\n"
            "- Is there any extra proof USER wants before later Workstream approval?\n\n"
            "## Exact BP3 USER Decision Options\n\n"
            "- Accept BP3: confirm BP3 is the accepted Workstream Entry / Orchestration "
            "Validation contract and allow Codex to return a separate bounded "
            "Workstream implementation approval packet next.\n"
            "- Revise BP3: identify the readiness question, seam order, proof plan, "
            "rollback posture, drift control, or pending gate that needs correction.\n"
            "- Waive BP3: explicitly waive remaining BP3 concerns and allow Codex to "
            "return a separate bounded Workstream implementation approval packet next.\n"
            "- Reject BP3: stop this carrier route and request a different FAM-007 "
            "successor path.\n"
            "- Hold BP3: keep the branch in BP3 USER review while USER or ChatGPT "
            "continues packet inspection.\n"
        )
        analysis_status = (
            "Analysis Summary: BP3 Workstream Entry / Orchestration Validation "
            "packet for the active Branch Planning carrier.\n"
            "BP1 Contract Status: Complete - USER accepted the integrated FAM-007 "
            "Dev/Owner Skeleton Readiness Branch Vision.\n"
            "BP2 Contract Status: Complete - USER accepted the cleaned FAM-007 "
            "Dev/Owner Skeleton Readiness engineering plan.\n"
            "BP1 USER Gate State: USER Accepted\n"
            "BP2 USER Gate State: USER Accepted\n"
            "BP3 Packet Reviewability State: Reviewable\n"
            "BP3 USER Gate State: Pending USER Review\n"
            "Branch Plan Matches Accepted Branch Vision: PASS - BP2 keeps Dev "
            "and Owner skeleton readiness integrated, preserves Dev private-repo "
            "future direction, Owner local-private baseline, GitHub Desktop safety, "
            "backup/import posture, provider/runtime/cache/memory deferral, and "
            "lane identity proof without changing the accepted BP1 direction.\n"
            "Branch Package Size: PASS - one FAM-007 branch remains the largest "
            "safe coherent package because Dev readiness, Owner readiness, private "
            "root/remote safety, backup/import posture, provider-state deferral, "
            "packet proof, and validation proof share the same trust boundary.\n"
            "SLC Traceability: Complete\n"
            "Future-Gated Boundaries: PASS - private Dev/Owner setup, private "
            "repos/roots/remotes, GitHub Desktop private binding, backup/import "
            "execution, provider/model/runtime/cache/memory behavior, PR, merge, "
            "release, cleanup, AI Product Contract import, Private Dev ORIN import, "
            "and v1.8.0 remain pending USER decisions.\n"
            "First Bounded Workstream Seam: Seam 1 should create public-safe "
            "action-gate registry and exact USER decision proof before later "
            "Dev/Owner matrices, private root/remote safety, backup/import, "
            "provider deferral, packet, fixture, validator, and fold-down proof.\n"
            "Implementation Approval: Pending separate USER approval after BP3 "
            "review; this packet does not authorize Workstream implementation."
        )
        implementation_posture = (
            "Implementation Posture: BP3 is reviewable but USER BP3 approval is "
            "pending; Workstream implementation, private setup, runtime/provider/"
            "cache/memory behavior, PR, merge, release, cleanup, and sibling-worktree "
            "mutation remain pending USER decisions."
        )
        recommended_seam = (
            "Recommended First Bounded Workstream Seam: Seam 1, action-gate "
            "registry and exact USER decision proof, to be considered only after "
            "USER approves or waives BP3 and separately approves Workstream implementation."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes accepted BP1 Branch Vision "
            "context, accepted BP2 Branch Plan context, FAM-007 family vision, "
            "Public/Dev/Owner boundary plan, AI Runtime And Trust Architecture, "
            "active branch authority record, external branch plan/state context, "
            "branch artifact rules, phase governance, execution rules, validation "
            "registry, backlog, roadmap, and worktree-slot context needed for BP3."
        )
        checklist_status = (
            "Checklist Focus: BP3 Workstream Entry / Orchestration Validation - "
            "accepted BP1/BP2 traceability, whole-package seam order, first-seam "
            "recommendation, proof plan, H1/LV/UTS expectations, rollback posture, "
            "drift controls, and future-gated private/runtime decisions are represented "
            "for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md "
            "as the primary BP3 decision file, USER_BRANCH_VISION_REVIEW.md and "
            "USER_BRANCH_PLAN_REVIEW.md as supporting accepted BP1/BP2 context, "
            "required digest/checklist files, and copied source-truth files are "
            "loaded and digestible for USER review; BP3 remains pending USER "
            "approval, revision, waiver, rejection, or hold."
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
            "external-state split, mandatory timestamped ZIP uploads, sidecar deferral, and USER-facing "
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
    elif workstream_package_approval_packet:
        analysis_status = (
            "Analysis Summary: BP3 is accepted; USER is approving bounded Workstream "
            "package implementation for the admitted same-branch package."
        )
        implementation_posture = (
            "Implementation Posture: bounded Workstream package implementation is approved "
            "by this packet decision path with Seam 1 as the entry checkpoint. Continuation "
            "must proceed one active same-branch seam at a time until Workstream Green, a "
            "real named blocker, or explicit USER waiver."
        )
        recommended_seam = (
            "Entry Checkpoint: Seam 1, public-safe action-gate registry and exact USER "
            "decision proof."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, feature backlog, "
            "prebeta roadmap, active branch index, branch record, active branch plan "
            "context, worktree slots, AI Runtime And Trust Architecture, FAM-007 family "
            "vision, AI Edition plan, branch-plan README, phase governance, development "
            "rules, codex modes, validation helper registry, and review surfaces needed "
            "for bounded Workstream package approval."
        )
        checklist_status = (
            "Checklist Focus: Workstream package approval - accepted BP1/BP2/BP3 posture, "
            "entry seam proof, continuation latch, future-gated private/runtime/provider/"
            "cache/memory boundaries, and next lawful phase boundary to Hardening only "
            "after Workstream Green."
        )
        digest_status = (
            "Review Summary: START_HERE.md, WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md, "
            "supporting BP1/BP2 review files, required digest/checklist files, and copied "
            "source-truth files are loaded and digestible for USER review; packet wording "
            "treats Seam 1 as entry checkpoint, not terminal Workstream authority."
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
            "digestible for USER review; Seam 2 remains governed by Workstream continuation, not a new per-seam approval, unless a real blocker, explicit waiver, or backlog split is recorded."
        )
    elif is_fam007_breakpoint_2:
        analysis_status = (
            "Analysis Summary: Workstream Entry analysis is complete/green for the "
            "FAM-007 Breakpoint 2 Dev/Owner skeleton action-gate readiness carrier."
        )
        implementation_posture = (
            "Implementation Posture: Workstream implementation remains pending USER "
            "approval and is not authorized by this packet until USER accepts or "
            "waives the repaired USER_BRANCH_PLAN_REVIEW.md contract and approves "
            "bounded Workstream package execution with Seam 1 as the entry checkpoint."
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
    if bp3_packet:
        common += (
            "BP3 Packet Reviewability State: Reviewable\n"
            "BP3 USER Gate State: Pending USER Review\n"
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
            f"{recommended_seam}"
            f"{bp3_readiness_contract}\n\n"
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
    bp1_markers = (
        "bp1 branch vision review",
        "user_branch_vision_review.md",
        "user branch vision review gate",
    )
    bp2_markers = (
        "bp2 branch plan review",
        "user_branch_plan_review.md",
        "user branch plan review gate",
    )
    bp3_markers = (
        "bp3 orchestration",
        "workstream entry / orchestration",
        "workstream entry orchestration",
    )
    pending_gate_markers = (
        "user gate state: pending user review",
        "user gate state: user revision requested",
        "user gate state: user rejected",
        "user gate state: user blocked",
    )
    reviewable_without_closed_gate = (
        "packet reviewability state: reviewable" in normalized
        and not any(
            marker in normalized
            for marker in (
                "user gate state: user accepted",
                "user gate state: user approved",
                "user gate state: user waived",
            )
        )
    )
    if any(marker in normalized for marker in pending_gate_markers) or reviewable_without_closed_gate:
        if any(marker in normalized for marker in bp3_markers):
            return DECISION_STATUS_BP3_ORCHESTRATION_REVIEW
        if any(marker in normalized for marker in bp2_markers):
            return DECISION_STATUS_BP2_BRANCH_PLAN_REVIEW
        if any(marker in normalized for marker in bp1_markers):
            return DECISION_STATUS_BP1_BRANCH_VISION_REVIEW

    implementation_markers = (
        "approve bounded workstream package implementation",
        "approve bounded workstream implementation",
        "bounded workstream package implementation",
        "workstream package implementation approval",
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

    bp2_review_markers = (
        "bp2 branch plan review",
        "bp2 user branch plan review",
        "user_branch_plan_review.md as the primary bp2 decision file",
    )
    bp2_decision_markers = (
        "accepted bp1 branch vision is the planning basis",
        "bp2 user branch plan review packet is reviewable",
        "bp2 remains pending user acceptance",
        "bp3 remains pending",
    )
    if any(marker in normalized for marker in bp2_review_markers) and any(
        marker in normalized for marker in bp2_decision_markers
    ):
        return DECISION_STATUS_BP2_BRANCH_PLAN_REVIEW

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


def _field_value(text: str, field_name: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(field_name)}\s*:\s*(.+?)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _review_marker_or_section_value(text: str, marker: str) -> str:
    line_value = _field_value(text, marker)
    if line_value:
        return line_value
    return _section(text, marker.removesuffix(":")).strip()


def _normalized_gate_value(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value).strip().casefold()
    return normalized.split(" - ", 1)[0].strip()


def _exact_decision_text(packet_files: Mapping[str, str]) -> str:
    return "\n".join(
        text
        for file_name, text in sorted(packet_files.items())
        if _packet_file_basename(file_name) in WORKSTREAM_ENTRY_PACKET_DECISION_FILES
        or _packet_file_basename(file_name)
        in {USER_BRANCH_VISION_REVIEW_FILE, USER_BRANCH_PLAN_REVIEW_FILE}
    )


def _branch_planning_review_gate_state_failures(
    packet_files: Mapping[str, str],
) -> list[str]:
    failures: list[str] = []
    generated_files = {
        file_name: text
        for file_name, text in packet_files.items()
        if _packet_file_basename(file_name) in USER_FACING_GENERATED_FILES
    }
    all_review_text = _exact_decision_text(packet_files)
    normalized_all_review_text = re.sub(r"\s+", " ", all_review_text).casefold()
    branch_planning_context = any(
        marker in normalized_all_review_text
        for marker in (
            "bp1",
            "bp2",
            "bp3",
            "user_branch_vision_review.md",
            "user_branch_plan_review.md",
            "user branch vision review",
            "user branch plan review",
            "workstream entry / orchestration",
        )
    )
    if not branch_planning_context:
        return failures

    reviewability_values: list[tuple[str, str]] = []
    user_gate_values: list[tuple[str, str]] = []
    for file_name, text in sorted(generated_files.items()):
        reviewability_value = _field_value(text, "Packet Reviewability State")
        if reviewability_value:
            normalized = _normalized_gate_value(reviewability_value)
            reviewability_values.append((file_name, normalized))
            if normalized not in BRANCH_PLANNING_PACKET_REVIEWABILITY_VALUES:
                failures.append(
                    f"{file_name}: invalid Packet Reviewability State '{reviewability_value}'"
                )
        user_gate_value = _field_value(text, "USER Gate State")
        if user_gate_value:
            normalized = _normalized_gate_value(user_gate_value)
            user_gate_values.append((file_name, normalized))
            if normalized not in BRANCH_PLANNING_USER_GATE_VALUES:
                failures.append(f"{file_name}: invalid USER Gate State '{user_gate_value}'")

    if reviewability_values and not user_gate_values:
        failures.append(
            "USER Review Packet Phase-State Conflict: Packet Reviewability State "
            "appears without USER Gate State"
        )
    if user_gate_values and not reviewability_values:
        failures.append(
            "USER Review Packet Phase-State Conflict: USER Gate State appears "
            "without Packet Reviewability State"
        )

    implementation_requested = any(
        marker in normalized_all_review_text
        for marker in BRANCH_PLANNING_IMPLEMENTATION_REQUEST_MARKERS
    ) and not any(
        marker in normalized_all_review_text
        for marker in BRANCH_PLANNING_IMPLEMENTATION_BLOCKING_MARKERS
    )
    pending_gate_files = [
        file_name
        for file_name, normalized in user_gate_values
        if normalized in BRANCH_PLANNING_PENDING_USER_GATE_VALUES
    ]
    if pending_gate_files and implementation_requested:
        failures.append(
            "Packet Validation Treated As USER Acceptance: implementation approval "
            "wording appears while USER Gate State is still pending, revision-requested, "
            f"rejected, or blocked in {', '.join(pending_gate_files)}"
        )

    for file_name in (USER_BRANCH_VISION_REVIEW_FILE, USER_BRANCH_PLAN_REVIEW_FILE):
        text = _packet_file_text(packet_files, file_name)
        if not text:
            continue
        display_name = _packet_file_path(packet_files, file_name)
        reviewability_state = _normalized_gate_value(
            _review_marker_or_section_value(text, "Packet Reviewability State:")
        )
        user_gate_state = _normalized_gate_value(
            _review_marker_or_section_value(text, "USER Gate State:")
        )
        if reviewability_state and reviewability_state not in BRANCH_PLANNING_PACKET_REVIEWABILITY_VALUES:
            failures.append(
                f"{display_name}: invalid Packet Reviewability State "
                f"'{reviewability_state}'"
            )
        if user_gate_state and user_gate_state not in BRANCH_PLANNING_USER_GATE_VALUES:
            failures.append(f"{display_name}: invalid USER Gate State '{user_gate_state}'")
        if (
            implementation_requested
            and user_gate_state in BRANCH_PLANNING_PENDING_USER_GATE_VALUES
        ):
            failures.append(
                "Review Gate Bypass: implementation approval wording appears while "
                f"{display_name} USER Gate State is '{user_gate_state}'"
            )

    branch_plan_review = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    if branch_plan_review:
        contract_status = _normalized_gate_value(
            _review_marker_or_section_value(branch_plan_review, "Contract Status:")
        )
        blocking_contract = contract_status.startswith(
            (
                "draft",
                "pending user response",
                "pending codex digest",
                "pending user confirmation",
            )
        )
        if blocking_contract and implementation_requested:
            failures.append(
                "Packet Validation Treated As USER Acceptance: implementation approval "
                "wording appears while USER_BRANCH_PLAN_REVIEW.md Contract Status "
                f"is '{contract_status}'"
            )
    return failures


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
    failures.extend(_user_branch_plan_stale_bp1_wording_failures(packet_files))
    failures.extend(_fam007_bp2_plan_substantive_failures(packet_files))
    failures.extend(_fam007_bp2_support_bp1_context_failures(packet_files))
    failures.extend(_bp1_packet_phase_language_failures(packet_files))
    failures.extend(_branch_planning_review_gate_state_failures(packet_files))
    failures.extend(_user_branch_vision_substantive_failures(packet_files))
    for required_file in WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES:
        if not _packet_file_present(packet_files, required_file):
            failures.append(f"{required_file}: required Workstream Entry packet file is missing")

    start_here = packet_files.get("START_HERE.md", "")
    if not _field_present(start_here, "USER Decision This Packet Supports"):
        failures.append("START_HERE.md: USER Decision This Packet Supports field is missing")
    workstream_digest = _packet_file_text(packet_files, "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md")
    if "USER Decision" not in workstream_digest:
        failures.append("WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md: USER Decision field is missing")

    file_statuses: dict[str, str] = {}
    for file_name in WORKSTREAM_ENTRY_PACKET_DECISION_FILES:
        text = _packet_file_text(packet_files, file_name)
        if not text:
            continue
        display_name = _packet_file_path(packet_files, file_name)
        status = _packet_text_status(text)
        file_statuses[display_name] = status
        if status == DECISION_STATUS_UNKNOWN:
            failures.append(f"{display_name}: next legal phase / implementation posture is not machine-readable")

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
        sorted(path for path in packet_dir.rglob("*") if path.is_file())
        if packet_dir.exists()
        else []
    )
    for path in all_files:
        if path.suffix.lower() not in {".md", ".txt", ".json"}:
            continue
        packet_files[path.relative_to(packet_dir).as_posix()] = path.read_text(encoding="utf-8")
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
    user_review_dir = target / USER_REVIEW_DIR_NAME
    review_aids_dir = target / REVIEW_AIDS_DIR_NAME
    source_context_dir = target / SOURCE_TRUTH_CONTEXT_DIR_NAME
    user_review_dir.mkdir(parents=True, exist_ok=True)
    review_aids_dir.mkdir(parents=True, exist_ok=True)
    source_context_dir.mkdir(parents=True, exist_ok=True)

    copied = [
        _copy_file(file_name, target, copy_name, subdir=SOURCE_TRUTH_CONTEXT_DIR_NAME)
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
    created_at_dt = datetime.now()
    created_at = created_at_dt.isoformat(timespec="seconds")

    source_branch = _git_output("branch", "--show-current")
    source_head = _git_output("rev-parse", "HEAD")
    upstream = _git_output("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    origin_main = _git_output("rev-parse", "origin/main")
    export_zip = _export_zip_path(review_root, label, created_at_dt)
    normalized_decision = exact_user_decision.casefold()
    workstream_package_approval_packet = (
        source_branch == "feature/fam-007-dev-owner-skeleton-readiness"
        and any(
            marker in normalized_decision
            for marker in BRANCH_PLANNING_IMPLEMENTATION_REQUEST_MARKERS
        )
        and not any(
            marker in normalized_decision
            for marker in BRANCH_PLANNING_IMPLEMENTATION_BLOCKING_MARKERS
        )
    )
    seam1_approval_packet = (
        source_branch == "feature/fam-007-breakpoint-2-dev-owner-skeleton-action-gate-readiness"
        and "approve bounded workstream implementation" in normalized_decision
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
    bp3_packet = (
        source_branch == "feature/fam-007-dev-owner-skeleton-readiness"
        and (
            "bp3" in exact_user_decision.casefold()
            or "workstream entry / orchestration" in exact_user_decision.casefold()
            or "orchestration validation" in exact_user_decision.casefold()
        )
    )
    bp1_packet = (
        "bp1 branch vision" in exact_user_decision.casefold()
        and "authorize bp2 user branch plan review only" in exact_user_decision.casefold()
    )
    bp2_packet = (
        not bp1_packet
        and not bp3_packet
        and (
            "bp2 user branch plan review" in exact_user_decision.casefold()
            or "bp2 branch plan review" in exact_user_decision.casefold()
        )
    )
    machine_readable_packet_status = (
        "bp1 branch vision review - BP1 Branch Vision Review remains pending "
        "USER acceptance, revision, waiver, rejection, or hold; BP2 remains pending."
        if bp1_packet
        else
        "bp2 branch plan review - accepted BP1 Branch Vision is the planning basis; "
        "BP2 USER Branch Plan Review packet is Reviewable; USER acceptance, revision, "
        "waiver, rejection, or hold remains pending; BP3 remains pending."
        if bp2_packet
        else
        "bp3 orchestration review - accepted BP1 Branch Vision and accepted BP2 "
        "Branch Plan are the traceability basis; BP3 Workstream Entry / "
        "Orchestration Validation packet is Reviewable; USER BP3 approval, "
        "revision, waiver, rejection, or hold remains pending; Workstream "
        "implementation remains pending separate USER approval."
        if bp3_packet
        else
        "implementation-ready - BP1, BP2, and BP3 are accepted; bounded Workstream "
        "package implementation is approved by this packet with Seam 1 as the entry "
        "checkpoint and continuation governed until Workstream Green, a real blocker, "
        "or explicit USER waiver."
        if workstream_package_approval_packet
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
    primary_user_review_file_name = _primary_user_review_file(exact_user_decision)
    user_vision_file = _write_user_branch_vision_review(
        target=review_aids_dir,
        title=title,
        review_purpose=review_purpose,
        exact_user_decision=user_facing_decision,
        pending_user_decisions=pending_user_decisions,
        copied=copied,
    )
    user_review_file = _write_user_branch_plan_review(
        target=review_aids_dir,
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
    digest_paths = {
        (review_aids_dir / name).resolve()
        for name in WORKSTREAM_ENTRY_PACKET_REQUIRED_FILES
        if name != "START_HERE.md"
    }
    expected_generated_paths = {user_vision_file.resolve(), user_review_file.resolve(), *digest_paths}
    primary_source_path = (review_aids_dir / primary_user_review_file_name).resolve()
    primary_destination_path = (user_review_dir / primary_user_review_file_name).resolve()
    if primary_source_path in expected_generated_paths:
        expected_generated_paths.remove(primary_source_path)
    expected_generated_paths.add(primary_destination_path)
    actual_bundle_files = copied_targets | expected_generated_paths | {start_here}
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
        target=review_aids_dir,
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
    primary_user_review_file = _move_primary_user_review_file(
        target=target,
        review_aids_dir=review_aids_dir,
        user_review_dir=user_review_dir,
        primary_file_name=primary_user_review_file_name,
    )

    readme_lines: list[str] = [
        f"# {title}",
        "",
        "## Review Packet",
        "",
        f"Review Purpose: {review_purpose}",
        "Review Location: Open this folder in the local USER hub and upload the matching timestamped ZIP beside it.",
        f"Local USER Hub Folder: `{target}`",
        f"Custom Review Path Waiver: {custom_review_path_waiver}",
        f"Custom Review Path Reason: {custom_review_path_reason_value}",
        "Review Safety Note: Copied files are selected repo source-truth and "
        "review-context files for USER inspection; technical freshness proof "
        "stays in Codex chat digest, helper output, validator output, or external state.",
        f"Primary USER Review File: `{primary_user_review_file.relative_to(target).as_posix()}`",
        f"Source Truth Context Folder: `{SOURCE_TRUTH_CONTEXT_DIR_NAME}`",
        f"Review Aids Folder: `{REVIEW_AIDS_DIR_NAME}`",
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
    if bp3_packet:
        readme_lines.extend(
            [
                "BP3 Packet Reviewability State: Reviewable",
                "BP3 USER Gate State: Pending USER Review",
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
        *_fam007_bp2_plan_substantive_failures(packet_files),
        *_fam007_bp2_support_bp1_context_failures(packet_files),
        *_bp1_packet_phase_language_failures(packet_files),
        *_user_branch_vision_substantive_failures(packet_files),
        *_branch_planning_review_gate_state_failures(packet_files),
    ]
    if artifact_failures:
        raise ValueError(
            "Review bundle artifact validation failed:\n"
            + "\n".join(f"- {failure}" for failure in artifact_failures)
        )
    expected_zip_entries = {path.relative_to(target).as_posix() for path in bundle_paths}
    _remove_stale_same_label_export_zips(review_root, label, export_zip)
    _write_export_zip(target, export_zip)
    _validate_export_zip(
        export_zip,
        source_branch=source_branch,
        source_head=source_head,
        origin_main=origin_main,
        expected_label=label,
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
