# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=user-review-bundle-helper; status=shared
"""Create a USER-facing local review bundle from selected repo files.

This helper copies review files to a stable worktree-labeled folder under
``C:\\Nexus USER`` so USER review does not depend on manually browsing the
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
    "created the timestamped review zip from that refreshed folder."
)
USER_BRANCH_PLAN_REVIEW_FILE = "USER_BRANCH_PLAN_REVIEW.md"
USER_BRANCH_VISION_REVIEW_FILE = "USER_BRANCH_VISION_REVIEW.md"
USER_REVIEW_DIR_NAME = "USER Review"
REVIEW_AIDS_DIR_NAME = "Review Aids"
SOURCE_TRUTH_CONTEXT_DIR_NAME = "Source Truth Context"
FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH = (
    "feature/fam-006-active-overlay-recording-runtime-implementation"
)
FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_SLUG = (
    "feature_fam_006_active_overlay_recording_runtime_implementation"
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
USER_REVIEW_PRIMARY_DECISION_FILES: tuple[str, ...] = (
    USER_BRANCH_VISION_REVIEW_FILE,
    USER_BRANCH_PLAN_REVIEW_FILE,
    "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
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
    "approve bounded workstream implementation",
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
FAM006_BP1_GENERATED_STALE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("governance-user-hub-path", re.compile(r"C:\\Nexus USER\\Governance", re.IGNORECASE)),
    ("governance-branch", re.compile(r"\bGovernance branch\b", re.IGNORECASE)),
    ("pr-readiness-stage-1", re.compile(r"\bPR Readiness Stage 1\b", re.IGNORECASE)),
    (
        "workstream-entry-final-review",
        re.compile(r"\bWorkstream Entry final decision review\b", re.IGNORECASE),
    ),
    (
        "stage-2-setup-green",
        re.compile(r"\bStage 2 setup is green\b", re.IGNORECASE),
    ),
    (
        "fam007-ownership",
        re.compile(r"\bFAM-007\b[^\n]*(?:ownership|AI Edition|Breakpoint|Dev/Owner)", re.IGNORECASE),
    ),
    (
        "ai-runtime-trust-architecture",
        re.compile(r"\bAI Runtime And Trust Architecture\b", re.IGNORECASE),
    ),
)
BP2_ACCEPTED_BP1_SUPPORT_STALE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "BP1 pending review",
        re.compile(r"\bBP1\b[^\n]{0,80}\bPending USER Review\b", re.IGNORECASE),
    ),
    (
        "BP1 pending acceptance",
        re.compile(
            r"\bBP1 acceptance remains pending\b|\bPending USER acceptance or waiver\b",
            re.IGNORECASE,
        ),
    ),
    (
        "BP1 must close before BP2",
        re.compile(
            r"\bBP1\b[^\n]{0,120}\b(?:before|until)\b[^\n]{0,80}\bBP2\b|"
            r"\bBP2\b[^\n]{0,120}\b(?:wait|requires|after)\b[^\n]{0,80}\bBP1\b",
            re.IGNORECASE,
        ),
    ),
    (
        "BP2 placeholder",
        re.compile(r"\bBP2\b[^\n]{0,80}\bplaceholder\b", re.IGNORECASE),
    ),
    (
        "active BP1 decision prompt",
        re.compile(
            r"\bactive decision\b[^\n]{0,80}\bBP1\b|"
            r"\baccept(?:s|ed|ance)?\s+or\s+waive(?:s|d|r)?\s+BP1\b",
            re.IGNORECASE,
        ),
    ),
)
USER_BRANCH_VISION_TEMPLATE_SHELL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
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
USER_BRANCH_VISION_DECISION_AID_PATTERNS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    (
        "Product Options / Design Paths",
        "real option labels",
        re.compile(r"\bOption\s+[A-Z]\b", re.IGNORECASE),
    ),
    (
        "Product Options / Design Paths",
        "tradeoff language",
        re.compile(r"\btradeoff\b|\brisk\b|\bdefer", re.IGNORECASE),
    ),
    (
        "Codex Recommendations",
        "line-item recommendation",
        re.compile(r"\brecommendation\b", re.IGNORECASE),
    ),
    (
        "Codex Recommendations",
        "tradeoff language",
        re.compile(r"\btradeoff\b|\brisk\b|\bbecause\b", re.IGNORECASE),
    ),
    (
        "Codex Recommendations",
        "USER response space",
        re.compile(r"\bUSER response\b", re.IGNORECASE),
    ),
    (
        "Surface Map",
        "review surface",
        re.compile(r"\breview surface\b|\bUSER_BRANCH_VISION_REVIEW\.md\b|\bsurface\b", re.IGNORECASE),
    ),
    (
        "Surface Map",
        "decision surface",
        re.compile(r"\bdecision surface\b|\bUSER response\b|\bproof surface\b|\bstatus preview surface\b", re.IGNORECASE),
    ),
    (
        "What Will I Actually See, And Where Will I See It?",
        "visible USER outcome",
        re.compile(
            r"\bUSER (?:sees|will see|reviews|opens|inspects|is deciding)\b|\bUSER-facing\b|\bvisible\b",
            re.IGNORECASE,
        ),
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


def _structured_user_review_packet_layout_failures(
    packet_files: Mapping[str, str],
) -> list[str]:
    failures: list[str] = []
    paths = set(packet_files)
    if "START_HERE.md" not in paths:
        failures.append("START_HERE.md: required packet root index is missing")
    required_dirs = (USER_REVIEW_DIR_NAME, REVIEW_AIDS_DIR_NAME, SOURCE_TRUTH_CONTEXT_DIR_NAME)
    for directory in required_dirs:
        prefix = f"{directory}/"
        if not any(path.startswith(prefix) for path in paths):
            failures.append(f"{directory}: required structured packet folder is missing or empty")

    for file_name in USER_REVIEW_PRIMARY_DECISION_FILES:
        if file_name in paths:
            failures.append(
                f"{file_name}: USER review decision files must not be at packet root"
            )

    primary_paths = [
        path
        for path in paths
        if path.startswith(f"{USER_REVIEW_DIR_NAME}/")
        and _packet_file_basename(path) in USER_REVIEW_PRIMARY_DECISION_FILES
    ]
    if len(primary_paths) != 1:
        failures.append(
            "USER Review: exactly one primary current-gate USER decision file is required; "
            f"found {sorted(primary_paths) or 'none'}"
        )

    for file_name in USER_REVIEW_PRIMARY_DECISION_FILES:
        matches = [path for path in paths if _packet_file_basename(path) == file_name]
        if len(matches) > 1:
            failures.append(
                f"{file_name}: duplicate USER review decision file copies are not allowed; "
                f"found {sorted(matches)}"
            )

    start_here_raw = packet_files.get("START_HERE.md", "")
    start_here = start_here_raw.casefold()
    decision_path_match = re.search(
        r"^Decision Path Summary:\s*(.+)$",
        start_here_raw,
        re.IGNORECASE | re.MULTILINE,
    )
    decision_path_summary = decision_path_match.group(1).casefold() if decision_path_match else start_here
    primary = primary_paths[0] if len(primary_paths) == 1 else ""
    phase_primary_expectations = (
        ("bp1 branch vision review", f"{USER_REVIEW_DIR_NAME}/{USER_BRANCH_VISION_REVIEW_FILE}"),
        ("bp2 branch plan review", f"{USER_REVIEW_DIR_NAME}/{USER_BRANCH_PLAN_REVIEW_FILE}"),
        (
            "bp3 orchestration",
            f"{USER_REVIEW_DIR_NAME}/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
        ),
        (
            "workstream entry / orchestration",
            f"{USER_REVIEW_DIR_NAME}/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md",
        ),
    )
    for marker, expected_path in phase_primary_expectations:
        if marker in decision_path_summary and primary and primary != expected_path:
            failures.append(
                "USER Review primary file does not match packet phase: "
                f"expected {expected_path}, found {primary}"
            )
    if (
        "primary user review file:" in start_here
        and primary
        and f"`{primary.casefold()}`" not in start_here
    ):
        failures.append(
            "START_HERE.md: reported Primary USER Review File does not match actual "
            f"structured primary file {primary}"
        )
    return failures


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


def _export_zip_path(review_root: Path, label: str) -> Path:
    return (review_root / f"{_sanitize_folder_name(label)}.zip").resolve()


def _timestamped_export_zip_path(review_root: Path, label: str, created_at: datetime) -> Path:
    stamp = created_at.strftime("%Y%m%d-%H%M%S")
    return (review_root / f"{_sanitize_folder_name(label)}__{stamp}.zip").resolve()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _copy_timestamped_upload_zip(export_zip: Path, upload_zip: Path) -> None:
    if export_zip == upload_zip:
        raise ValueError("Timestamped upload zip source and destination must be distinct")
    if export_zip.parent != upload_zip.parent:
        raise ValueError("Timestamped upload zip must stay beside the generated export zip")
    shutil.copy2(export_zip, upload_zip)
    stable_hash = _sha256_file(export_zip)
    upload_hash = _sha256_file(upload_zip)
    if stable_hash != upload_hash:
        raise ValueError(
            "Timestamped upload zip hash mismatch: "
            f"source={stable_hash} timestamped={upload_hash}"
        )


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


def _clear_matching_export_zips(review_root: Path, label: str) -> None:
    root = review_root.resolve()
    safe_label = _sanitize_folder_name(label)
    for candidate in sorted(root.glob(f"{safe_label}*.zip")):
        resolved = candidate.resolve()
        if root not in resolved.parents:
            raise ValueError(f"Refusing to remove review zip outside USER hub: {resolved}")
        if candidate.is_file():
            candidate.unlink()


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
        *_structured_user_review_packet_layout_failures(packet_files),
        *_user_facing_technical_metadata_failures(packet_files),
        *_user_branch_plan_stale_bp1_wording_failures(packet_files),
        *_fam006_bp1_generated_stale_failures(packet_files),
        *_bp2_accepted_bp1_support_file_failures(packet_files),
        *_fam006_bp3_support_file_failures(packet_files),
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
        "## Must-Not-Do / Regression-Risk Rules",
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


def _fam006_bp1_generated_stale_failures(packet_files: Mapping[str, str]) -> list[str]:
    generated_text = "\n".join(
        _packet_file_text(packet_files, file_name)
        for file_name in USER_FACING_GENERATED_FILES
    )
    normalized = generated_text.casefold()
    is_fam006_bp1_packet = (
        "fam-006 active overlay recording runtime implementation" in normalized
        and "bp1" in normalized
        and "bp2 user branch plan review remains pending" in normalized
        and "packet reviewability is not user acceptance" in normalized
    )
    if not is_fam006_bp1_packet:
        return []

    failures: list[str] = []
    for file_name in USER_FACING_GENERATED_FILES:
        text = _packet_file_text(packet_files, file_name)
        if not text:
            continue
        display_name = _packet_file_path(packet_files, file_name)
        for reason, pattern in FAM006_BP1_GENERATED_STALE_PATTERNS:
            if pattern.search(text):
                failures.append(
                    f"{display_name}: FAM-006 BP1 generated review file contains stale {reason} wording"
                )
    return failures


def _bp2_accepted_bp1_support_file_failures(packet_files: Mapping[str, str]) -> list[str]:
    start_here = _packet_file_text(packet_files, "START_HERE.md")
    plan_review = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    support_review = _packet_file_text(packet_files, USER_BRANCH_VISION_REVIEW_FILE)
    if not (start_here and plan_review and support_review):
        return []
    normalized_packet = re.sub(r"\s+", " ", f"{start_here}\n{plan_review}").casefold()
    is_bp2_packet = (
        "bp2 branch plan review" in normalized_packet
        or "user_branch_plan_review.md" in normalized_packet
    )
    is_fam006_packet = (
        "fam-006 active overlay recording runtime implementation" in normalized_packet
    )
    if not (is_bp2_packet and is_fam006_packet):
        return []

    failures: list[str] = []
    display_name = _packet_file_path(packet_files, USER_BRANCH_VISION_REVIEW_FILE)
    support_gate_state = _normalized_gate_value(
        _review_marker_or_section_value(support_review, "USER Gate State:")
    )
    support_contract_status = _normalized_gate_value(
        _review_marker_or_section_value(support_review, "Contract Status:")
    )
    if support_gate_state not in {"user accepted", "user approved", "user waived"}:
        failures.append(
            f"{display_name}: BP2 packet support file must carry accepted/waived BP1 "
            f"USER Gate State, found '{support_gate_state or 'missing'}'"
        )
    if support_contract_status.startswith(("draft", "pending")) or not support_contract_status:
        failures.append(
            f"{display_name}: BP2 packet support file must not present BP1 as draft or "
            f"pending, found Contract Status '{support_contract_status or 'missing'}'"
        )
    for reason, pattern in BP2_ACCEPTED_BP1_SUPPORT_STALE_PATTERNS:
        if pattern.search(support_review):
            failures.append(
                f"{display_name}: BP2 packet accepted-BP1 support file contains stale {reason} wording"
            )
    return failures


def _fam006_bp3_support_file_failures(packet_files: Mapping[str, str]) -> list[str]:
    start_here = _packet_file_text(packet_files, "START_HERE.md")
    primary = _packet_file_text(packet_files, "WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md")
    plan_review = _packet_file_text(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    if not (start_here and primary and plan_review):
        return []
    normalized_packet = re.sub(r"\s+", " ", f"{start_here}\n{primary}").casefold()
    is_fam006_bp3_packet = (
        "fam-006 active overlay recording runtime implementation" in normalized_packet
        and "bp3" in normalized_packet
        and "workstream_entry_analysis_digest.md" in normalized_packet
    )
    if not is_fam006_bp3_packet:
        return []

    failures: list[str] = []
    display_name = _packet_file_path(packet_files, USER_BRANCH_PLAN_REVIEW_FILE)
    plan_gate_state = _normalized_gate_value(
        _review_marker_or_section_value(plan_review, "USER Gate State:")
    )
    plan_contract_status = _normalized_gate_value(
        _review_marker_or_section_value(plan_review, "Contract Status:")
    )
    if plan_gate_state not in {"user accepted", "user approved", "user waived"}:
        failures.append(
            f"{display_name}: BP3 packet BP2 support file must carry accepted/waived "
            f"BP2 USER Gate State, found '{plan_gate_state or 'missing'}'"
        )
    if plan_contract_status.startswith(("draft", "pending")) or not plan_contract_status:
        failures.append(
            f"{display_name}: BP3 packet BP2 support file must not present BP2 as "
            f"draft or pending, found Contract Status '{plan_contract_status or 'missing'}'"
        )
    stale_patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        (
            "active BP1 gate",
            re.compile(r"\bactive current gate is BP1\b|\bcurrent gate is BP1\b", re.IGNORECASE),
        ),
        (
            "BP2 pending context",
            re.compile(r"\bBP2\b[^\n]{0,100}\bpending context\b|\bBP2 pending-context\b", re.IGNORECASE),
        ),
        (
            "BP1 must close before BP2",
            re.compile(
                r"\bBP1\b[^\n]{0,120}\b(?:before|until)\b[^\n]{0,80}\bBP2\b|"
                r"\bBP2\b[^\n]{0,120}\b(?:waits?|cannot|blocked|pending|requires closure)\b[^\n]{0,80}\bBP1\b",
                re.IGNORECASE,
            ),
        ),
        (
            "missing BP2 receipt",
            re.compile(r"\bno active BP2 receipt exists\b", re.IGNORECASE),
        ),
        (
            "wrong primary file",
            re.compile(r"USER Review/USER_BRANCH_VISION_REVIEW\.md", re.IGNORECASE),
        ),
        (
            "BP3 blocked until BP1/BP2 close",
            re.compile(r"\bBP3\b[^\n]{0,120}\bblocked\b[^\n]{0,120}\bBP1\b[^\n]{0,80}\bBP2\b", re.IGNORECASE),
        ),
    )
    for reason, pattern in stale_patterns:
        if pattern.search(plan_review):
            failures.append(
                f"{display_name}: BP3 packet BP2 support file contains stale {reason} wording"
            )
    if "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md" not in plan_review:
        failures.append(
            f"{display_name}: BP3 packet BP2 support file must name "
            "USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md as the primary current-gate file"
        )
    if "BP3 remains Pending USER Review" not in plan_review:
        failures.append(
            f"{display_name}: BP3 packet BP2 support file must state BP3 remains Pending USER Review"
        )
    if "Workstream implementation remains blocked" not in plan_review:
        failures.append(
            f"{display_name}: BP3 packet BP2 support file must state Workstream implementation remains blocked"
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

    for section_name, reason, pattern in USER_BRANCH_VISION_DECISION_AID_PATTERNS:
        value = _section(text, section_name)
        if value and not pattern.search(value):
            failures.append(
                f"{display_name}: {section_name} lacks BP1 decision-aid {reason}"
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
    pr_readiness_context_packet = "pr readiness stage 1 analysis" in exact_user_decision.casefold()
    is_fam006_active_overlay_implementation = any(
        FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_SLUG in source_rel
        for source_rel, _copied_rel in copied
    )
    normalized_decision = exact_user_decision.casefold()
    fam006_bp3_packet = (
        is_fam006_active_overlay_implementation
        and (
            "bp3" in normalized_decision
            or "workstream entry" in normalized_decision
            or "orchestration validation" in normalized_decision
        )
    )
    fam006_bp2_packet = (
        is_fam006_active_overlay_implementation
        and ("bp2" in normalized_decision or "branch plan review" in normalized_decision)
        and "bp1" not in normalized_decision
        and not fam006_bp3_packet
    )
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
    packet_reviewability_state = (
        "Reviewable - context packet for later-phase review; no new BP1 decision is requested by this helper output."
        if pr_readiness_context_packet
        else "Reviewable - BP1 packet is ready for USER Branch Vision Review, but acceptance is not recorded."
    )
    user_gate_state = (
        "Superseded - context-only BP1 copy for later-phase review; rely on the accepted branch record or external state for the original BP1 receipt."
        if pr_readiness_context_packet
        else "Pending USER Review - USER must accept, revise, waive, reject, or block BP1 before BP2 preparation can be green."
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
    if is_fam006_active_overlay_implementation and fam006_bp3_packet:
        accepted_bp1_lines = [
            "Active Overlay Profile membership is the recording target source.",
            "Snapshot-at-start is the accepted target model: a recording session uses the sensors and membership active when recording starts.",
            "Sensors added during an active recording become eligible for the next recording session.",
            "The HUD Overlay recording card remains small, quick-access, low-clutter, and easy to understand.",
            "The standalone Recording Control window carries richer target, readiness, status, and future control detail.",
            "Hidden recording target state is rejected.",
            "A separate Recording Profile system remains outside this branch unless USER explicitly reopens it later.",
            "Native Log Loader remains a future separate graph/log viewer.",
            "Per-overlay effective polling policy remains future FAM-006 architecture planning unless separately admitted.",
        ]
        lines = [
            f"# {title} - Accepted BP1 Branch Vision Context",
            "",
            "USER Branch Vision Review: BP1 accepted context for active BP3",
            "",
            "## Review Status",
            "",
            "Accepted Context - BP1 is closed as USER Accepted for this branch; this file is a Review Aid supporting active BP3 Workstream Entry / Orchestration Validation.",
            "",
            f"Title: {title}",
            f"Review Purpose: {review_purpose}",
            "",
            "## Contract Status",
            "",
            "Complete - USER accepted the BP1 Branch Vision; active decision-making has moved through BP2 and is now BP3.",
            "",
            "## Packet Reviewability State",
            "",
            "Reviewable - accepted BP1 context is included to let USER verify BP3 traces accepted BP2 back to the accepted vision.",
            "",
            "## USER Gate State",
            "",
            "USER Accepted - BP1 is accepted. The primary BP3 file carries the separate active USER response state for Workstream Entry / Orchestration Validation.",
            "",
            "## Contract Revision",
            "",
            "v6 - Accepted BP1 context regenerated as BP3 support after BP2 acceptance.",
            "",
            "## Project Vision Context",
            "",
            "Nexus should remain a USER-controlled, inspectable desktop AI system. FAM-006 supports that by making monitoring and recording behavior visible, reviewable, and controlled through local desktop surfaces rather than hidden automation.",
            "",
            "## Family Vision Context",
            "",
            "FAM-006 owns Monitoring and HUD behavior. This branch keeps recording inside that family by treating the active Overlay Profile as the future recording target source, keeping the HUD Overlay card as launcher and target/status preview, and keeping the standalone Recording Control window as the compact control surface.",
            "",
            "## Feature Vision Context",
            "",
            "This branch is the active-overlay-driven recording runtime implementation carrier. It rejects a separate Recording Profile system for the active plan and uses the active Overlay Profile as the target source for future recording sessions.",
            "",
            "## Codex Understanding",
            "",
            "USER accepted the BP1 direction and then accepted the BP2 engineering plan. BP3 must now verify that the accepted BP2 route is still traceable to the accepted BP1 vision before any separate Workstream implementation approval can be legal.",
            "",
            "## Branch Goal",
            "",
            "Build the FAM-006 recording foundation around the active Overlay Profile with a snapshot-at-start recording target and a visible, user-verifiable path from HUD card to Recording Control before any file-writing or recording execution is approved.",
            "",
            "## End-State Vision",
            "",
            "The completed branch should leave behind a concrete runtime direction: active Overlay Profile membership is snapshotted at recording start, sensors added during active recording wait for the next session, the HUD recording card stays small and quick-access, Recording Control owns richer detail, and future proof shows the target model behaved as accepted.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "- USER will see the future HUD Overlay card as a small recording launcher and concise target/status preview.",
            "- USER will open the future Recording Control window for richer target, snapshot, readiness, status, and approved control detail.",
            "- USER will inspect Overlay Profile membership as the source of target membership before recording starts.",
            "- USER will treat Native Log Loader as a separate future graph/log viewer, not part of the BP3 implementation recommendation unless later admitted.",
            "",
            "## How It Will Function",
            "",
            "The future implementation should derive the recording target from active Overlay Profile membership and use snapshot-at-start semantics. BP3 validates whether the accepted BP2 plan can enter Workstream safely while preserving target preview, Recording Control behavior, target-state behavior, stale/missing-target handling, rollback, H1, LV, and UTS expectations.",
            "",
            "## User Experience Flow",
            "",
            "1. USER reviews or selects the active Overlay Profile.",
            "2. USER sees concise recording target/status information in the HUD Overlay card after later implementation approval.",
            "3. USER opens Recording Control for richer target/readiness/status detail.",
            "4. A later approved recording session snapshots target membership at Start.",
            "5. Sensors added during recording become eligible for the next session.",
            "",
            "## Surface Map",
            "",
            "- Active Overlay Profile surface: target source before recording starts.",
            "- Snapshot-at-start target state proof surface: future locked session target evidence.",
            "- HUD Overlay recording card status preview surface: quick-access preview and launcher.",
            "- Recording Control window decision surface: richer status, readiness, target, and control review.",
            "- USER_BRANCH_VISION_REVIEW.md review surface: accepted BP1 context only.",
            "- Output/proof surfaces: future BP3/H1/LV/UTS evidence.",
            "- Native Log Loader and per-overlay effective polling policy: future-gated context.",
            "",
            "## Product Options / Design Paths",
            "",
            "- Option A - accepted path: active Overlay Profile with snapshot-at-start target model.",
            "- Option B - rejected unless later reopened: separate Recording Profile system.",
            "- Option C - accepted surface split: small HUD card plus richer Recording Control window.",
            "- Option D - rejected risk path: hidden target state or file-writing-first implementation.",
            "",
            "## Codex Recommendations",
            "",
            "- Recommendation 1: preserve snapshot-at-start as the implementation target model because it makes target proof concrete.",
            "- Recommendation 2: keep HUD recording card minimal and place richer target detail in Recording Control.",
            "- Recommendation 3: require BP3 to verify actual repo file ownership before recommending the first Workstream seam.",
            "- Recommendation 4: keep runtime execution, file writing, Start/Stop, tray, export/share, Native Log Loader, and provider/model work blocked until separate USER approval.",
            "- USER response should focus on whether BP3 proves enough orchestration readiness to permit a later separate implementation approval request.",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "The accepted BP1 vision keeps recording local, visible, user-controlled, and truthful. USER can inspect what will be recorded before recording behavior or file writing is approved.",
            "",
            "## USER Design Questions",
            "",
            "- Does BP3 preserve the accepted active Overlay Profile target model while checking the accepted BP2 route?",
            "- Does BP3 keep the HUD card small enough while ensuring Recording Control carries enough target detail?",
            "- Does BP3 block hidden target state, Native Log Loader, per-overlay polling implementation, and file-writing-first behavior?",
            "",
            "## USER Response",
            "",
            "USER accepted BP1 and BP2 before BP3 preparation. Active USER response is now needed for BP3 in `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`.",
            "",
            "## Codex Digest",
            "",
            "Codex digested BP1 acceptance into the FAM-006 branch record, branch plan, BP2 packet, and active BP3 review packet. This file is accepted BP1 context only.",
            "",
            "## USER Response Proof",
            "",
            "Accepted by USER - BP1 Branch Vision acceptance is recorded in the FAM-006 branch record and branch plan.",
            "",
            "## USER Response Digested",
            "",
            "Yes - BP1 acceptance has been digested into BP2 planning constraints and BP3 orchestration validation expectations.",
            "",
            "## Accepted Branch Vision",
            "",
            *_markdown_lines(accepted_bp1_lines),
            "",
            "## Family-Vision Versus Branch-Only Vision Impact",
            "",
            "Branch-specific implementation details stay with the FAM-006 branch record and branch plan. Reusable family-level direction may fold into the FAM-006 family vision during later PR readiness only if durable value remains.",
            "",
            "## Must-Have Behavior",
            "",
            "- BP3 must verify accepted BP2 against accepted BP1.",
            "- Future runtime proof must show the accepted target model clearly enough for USER to verify.",
            "- USER must be able to inspect what will be recorded before recording behavior is approved.",
            "",
            "## Must-Not-Do / Regression-Risk Rules",
            "",
            "- Do not create a separate Recording Profile system unless USER explicitly reopens that model.",
            "- Do not hide recording target state from USER review.",
            "- Do not clutter the HUD card with detail that belongs in Recording Control.",
            "- Do not implement recording execution, file writing, Start/Stop controls, tray controls, export/share, provider/model work, or Native Log Loader as part of BP3 review.",
            "- Do not treat this accepted-context Review Aid as BP3 acceptance or implementation approval.",
            "",
            "## Deferred And Future-Gated Ideas",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
            "## Vision Question Queue",
            "",
            "Closed for BP1. New vision questions discovered during BP3 must route back to BP1 or BP2 before Workstream implementation.",
            "",
            "## Design Assumption Ledger",
            "",
            "- Accepted: active Overlay Profile snapshot-at-start target model.",
            "- Accepted: HUD card remains minimal while Recording Control carries richer detail.",
            "- Accepted future boundary: Native Log Loader remains separate.",
            "- Accepted future boundary: per-overlay effective polling policy remains future FAM-006 architecture planning input.",
            "",
            "## Acceptance / Revision / Rejection / Waiver Decision",
            "",
            "BP1 is accepted. The active decision is BP3 acceptance, revision, rejection, hold, request for more options, or waiver in the primary BP3 file.",
            "",
            "## Exact USER Decision Supported By The Current Packet",
            "",
            exact_user_decision,
            "",
        ]
        review_path = target / USER_BRANCH_VISION_REVIEW_FILE
        review_path.write_text("\n".join(lines), encoding="utf-8")
        return review_path.resolve()
    if is_fam006_active_overlay_implementation and fam006_bp2_packet:
        accepted_bp1_lines = [
            "Active Overlay Profile membership is the recording target source.",
            "Snapshot-at-start is the accepted target model: a recording session uses the sensors and membership active when recording starts.",
            "Sensors added during an active recording become eligible for the next recording session.",
            "The HUD Overlay recording card remains small, quick-access, low-clutter, and easy to understand.",
            "The standalone Recording Control window carries richer target, readiness, status, and future control detail.",
            "Hidden recording target state is rejected.",
            "A separate Recording Profile system remains outside this branch unless USER explicitly reopens it later.",
            "Native Log Loader remains a future separate graph/log viewer.",
            "Per-overlay effective polling policy remains future FAM-006 architecture planning unless separately admitted.",
        ]
        lines = [
            f"# {title} - Accepted BP1 Branch Vision Context",
            "",
            "USER Branch Vision Review: BP1 accepted context for active BP2",
            "",
            "## Review Status",
            "",
            "Accepted Context - BP1 is closed as USER Accepted for this branch; this file is a Review Aid supporting the active BP2 USER Branch Plan Review.",
            "",
            "## Contract Status",
            "",
            "Complete - USER accepted the BP1 Branch Vision; active decision-making has moved to BP2.",
            "",
            "## Packet Reviewability State",
            "",
            "Reviewable - accepted BP1 context is included to let USER verify the BP2 plan traces to the accepted vision.",
            "",
            "## USER Gate State",
            "",
            "USER Accepted - BP1 is accepted. The primary BP2 file carries the separate active USER response state for the branch plan.",
            "",
            "## Contract Revision",
            "",
            "v5 - Accepted BP1 context regenerated during BP2 support-file contradiction repair.",
            "",
            "## Project Vision Context",
            "",
            "Nexus should remain a USER-controlled, inspectable desktop AI system. FAM-006 supports that by making monitoring and recording behavior visible, reviewable, and controlled through local desktop surfaces rather than hidden automation.",
            "",
            "## Family Vision Context",
            "",
            "FAM-006 owns Monitoring and HUD behavior. This branch keeps recording inside that family by treating the active Overlay Profile as the future recording target source, keeping the HUD Overlay card as launcher and target/status preview, and keeping the standalone Recording Control window as the compact control surface.",
            "",
            "## Feature Vision Context",
            "",
            "This branch is the active-overlay-driven recording runtime implementation carrier. It rejects a separate Recording Profile system for the active plan and uses the active Overlay Profile as the target source for future recording sessions.",
            "",
            "## Codex Understanding",
            "",
            "USER accepted the BP1 direction: snapshot-at-start target semantics, small HUD card, richer Recording Control detail, explicit target visibility, and no hidden recording target state. BP2 must translate that accepted direction into an engineering plan; this support file does not request a new BP1 decision.",
            "",
            "## Branch Goal",
            "",
            "Build the FAM-006 recording foundation around the active Overlay Profile with a snapshot-at-start recording target and a visible, user-verifiable path from HUD card to Recording Control before any file-writing or recording execution is approved.",
            "",
            "## End-State Vision",
            "",
            "The completed branch should leave behind a concrete runtime direction: active Overlay Profile membership is snapshotted at recording start, sensors added during active recording wait for the next session, the HUD recording card stays small and quick-access, Recording Control owns richer detail, and future proof shows the target model behaved as accepted.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "- USER will see the future HUD Overlay card as a small recording launcher and concise target/status preview.",
            "- USER will open the future Recording Control window for richer target, snapshot, readiness, status, and approved control detail.",
            "- USER will inspect Overlay Profile membership as the source of target membership before recording starts.",
            "- USER will treat Native Log Loader as a separate future graph/log viewer, not part of the active BP2 implementation plan unless later admitted.",
            "",
            "## How It Will Function",
            "",
            "The future implementation should derive the recording target from active Overlay Profile membership and use snapshot-at-start semantics. BP2 plans how to prove target preview, Recording Control behavior, target-state behavior, stale/missing-target handling, rollback, H1, LV, and UTS expectations before BP3 validates orchestration.",
            "",
            "## User Experience Flow",
            "",
            "1. USER reviews or selects the active Overlay Profile.",
            "2. USER sees concise recording target/status information in the HUD Overlay card after later implementation approval.",
            "3. USER opens Recording Control for richer target/readiness/status detail.",
            "4. A later approved recording session snapshots target membership at Start.",
            "5. Sensors added during recording become eligible for the next session.",
            "",
            "## Surface Map",
            "",
            "- Active Overlay Profile surface: target source before recording starts.",
            "- Snapshot-at-start target state proof surface: future locked session target evidence.",
            "- HUD Overlay recording card status preview surface: quick-access preview and launcher.",
            "- Recording Control window decision surface: richer status, readiness, target, and control review.",
            "- USER_BRANCH_VISION_REVIEW.md review surface: accepted BP1 context only.",
            "- Output/proof surfaces: future BP2/H1/LV/UTS evidence.",
            "- Native Log Loader and per-overlay effective polling policy: future-gated context.",
            "",
            "## Product Options / Design Paths",
            "",
            "- Option A - accepted path: active Overlay Profile with snapshot-at-start target model; tradeoff is that sensors added mid-recording wait for the next session.",
            "- Option B - rejected unless later reopened: separate Recording Profile system; risk is duplicate setup and hidden disagreement with Overlay Profile membership.",
            "- Option C - accepted surface split: small HUD card plus richer Recording Control window; tradeoff is two surfaces, but each stays clearer.",
            "- Option D - rejected risk path: hidden target state or file-writing-first implementation; this would make USER proof weaker.",
            "",
            "## Codex Recommendations",
            "",
            "- Recommendation 1: preserve snapshot-at-start as the BP2 plan's default target model because it makes target proof concrete; tradeoff is delayed inclusion for sensors added mid-session.",
            "- Recommendation 2: keep HUD recording card minimal and place richer detail in Recording Control because USER needs fast access without clutter; risk is under-informing the HUD if Recording Control is not easy to open.",
            "- Recommendation 3: require target preview, Recording Control, target-state, stale/missing-target, rollback, H1, LV, and UTS proof planning before BP3 because implementation should not outrun accepted evidence expectations.",
            "- Recommendation 4: keep Native Log Loader and per-overlay effective polling implementation future-gated unless USER separately admits them; USER response should focus on whether BP2 preserves that boundary.",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "The accepted BP1 vision keeps recording local, visible, user-controlled, and truthful. USER can inspect what will be recorded before recording behavior or file writing is approved.",
            "",
            "## USER Design Questions",
            "",
            "- Does the BP2 plan preserve the accepted active Overlay Profile target model without creating a separate Recording Profile system?",
            "- Does the BP2 plan keep the HUD card small enough while giving Recording Control enough detail for USER to understand target and readiness?",
            "- Does the BP2 plan leave hidden target state, Native Log Loader, per-overlay polling policy, and file-writing-first behavior outside the active branch route?",
            "- If BP2 changes the accepted product direction, route back to BP1 instead of advancing to BP3.",
            "",
            "## USER Response",
            "",
            "USER accepted BP1 through the BP1 Acceptance And BP2 Preparation approval. Active USER response is now needed for BP2 in `USER Review/USER_BRANCH_PLAN_REVIEW.md`.",
            "",
            "## Codex Digest",
            "",
            "Codex digested BP1 acceptance into the FAM-006 branch record, branch plan, and BP2 packet. This file is accepted BP1 context only.",
            "",
            "## USER Response Proof",
            "",
            "Accepted by USER - BP1 Branch Vision acceptance is recorded in the FAM-006 branch record and branch plan.",
            "",
            "## USER Response Digested",
            "",
            "Yes - BP1 acceptance has been digested into BP2 planning constraints.",
            "",
            "## Accepted Branch Vision",
            "",
            *_markdown_lines(accepted_bp1_lines),
            "",
            "## Family-Vision Versus Branch-Only Vision Impact",
            "",
            "Branch-specific implementation details stay with the FAM-006 branch record and branch plan. Reusable family-level direction may fold into the FAM-006 family vision during later PR readiness only if durable value remains.",
            "",
            "## Must-Have Behavior",
            "",
            "- BP2 must derive its engineering route from accepted BP1.",
            "- BP3 must validate BP2 against accepted BP1 before any Workstream implementation approval is legal.",
            "- Future runtime proof must show the accepted target model clearly enough for USER to verify.",
            "- USER must be able to inspect what will be recorded before recording behavior is approved.",
            "",
            "## Must-Not-Do / Regression-Risk Rules",
            "",
            "- Do not create a separate Recording Profile system unless USER explicitly reopens that model.",
            "- Do not hide recording target state from USER review.",
            "- Do not clutter the HUD card with detail that belongs in Recording Control.",
            "- Do not implement recording execution, file writing, Start/Stop controls, tray controls, export/share, provider/model work, or Native Log Loader as part of BP2 review.",
            "- Do not treat this accepted-context Review Aid as BP2 acceptance or implementation approval.",
            "",
            "## Deferred And Future-Gated Ideas",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
            "## Vision Question Queue",
            "",
            "Closed for BP1. New vision questions discovered during BP2 must route back to BP1 before BP3.",
            "",
            "## Design Assumption Ledger",
            "",
            "- Accepted: active Overlay Profile snapshot-at-start target model.",
            "- Accepted: HUD card remains minimal while Recording Control carries richer detail.",
            "- Accepted future boundary: Native Log Loader remains separate.",
            "- Accepted future boundary: per-overlay effective polling policy remains future FAM-006 architecture planning input.",
            "",
            "## Acceptance / Revision / Rejection / Waiver Decision",
            "",
            "BP1 is accepted. The active decision is BP2 acceptance, revision, rejection, hold, request for more options, or waiver in the primary BP2 file.",
            "",
            exact_user_decision,
            "",
        ]
        review_path = target / USER_BRANCH_VISION_REVIEW_FILE
        review_path.write_text("\n".join(lines), encoding="utf-8")
        return review_path.resolve()
    if is_fam006_active_overlay_implementation and not pr_readiness_context_packet:
        lines = [
            f"# {title} - USER Branch Vision Review",
            "",
            "USER Branch Vision Review: BP1",
            "",
            "## Review Status",
            "",
            "Needs USER Decision unless this packet records an explicit USER acceptance or waiver.",
            "",
            "## Contract Status",
            "",
            "Draft - update to Complete or Waived by USER only after USER accepts or waives BP1 for this branch.",
            "",
            "## Packet Reviewability State",
            "",
            "Reviewable - BP1 packet is ready for USER Branch Vision Review, but acceptance is not recorded.",
            "",
            "## USER Gate State",
            "",
            "Pending USER Review - USER must accept, revise, waive, reject, request more options, or block BP1 before BP2 preparation can be green.",
            "",
            "## Contract Revision",
            "",
            "v4 - FAM-006-specific BP1 vision revised with USER snapshot-at-start, HUD card, Recording Control window, proof, and hidden-target feedback; BP1 acceptance remains pending USER decision.",
            "",
            "## Project Vision Context",
            "",
            "Nexus should remain a USER-controlled, inspectable desktop AI system. FAM-006 supports that by making monitoring and recording behavior visible, reviewable, and controlled through local desktop surfaces rather than hidden automation.",
            "",
            "## Family Vision Context",
            "",
            "FAM-006 owns Monitoring and HUD behavior. This branch keeps recording inside that family by treating the active Overlay Profile as the future recording target source, keeping the HUD Overlay card as launcher and target/status preview, and keeping the standalone Recording Control window as the compact control surface.",
            "",
            "## Feature Vision Context",
            "",
            "This branch is the active-overlay-driven recording runtime implementation carrier. It replaces the idea of a separate Recording Profile system with a simpler model: the USER chooses or edits the active Overlay Profile, then a future recording session uses a snapshot of that overlay membership at recording start unless USER later approves a different model.",
            "",
            "## Codex Understanding",
            "",
            "USER feedback has been incorporated for review: snapshot-at-start is the gold-standard target model for this branch; the HUD Overlay recording card should stay small and quick-access; the Recording Control window should carry richer target/status/control detail; proof expectations should be planned in BP2; and hidden recording target state is rejected. BP1 acceptance remains pending USER decision.",
            "",
            "## Branch Goal",
            "",
            "Build the FAM-006 recording foundation around the active Overlay Profile with a snapshot-at-start recording target. The product goal is a recording experience where the USER can inspect what will be recorded before recording behavior is approved, where the HUD card gives quick access without clutter, where the Recording Control window owns richer target/status detail, and where proof expectations and rollback posture are clear before any recording writes files.",
            "",
            "## End-State Vision",
            "",
            "The completed branch should leave behind a concrete, source-truth-backed runtime direction: active Overlay Profile membership is snapshotted at recording start as the recording target, sensors added during an active recording become eligible for the next recording session, the HUD Overlay card stays a small quick-access recording affordance, the Recording Control window owns richer target/status/readiness/control detail, and validation/UTS proof can show the target model behaved as accepted. Recording execution, file writing, tray behavior, export/share, and Native Log Loader integration remain future-gated until their legal implementation approvals.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "- In the future runtime, the Dashboard HUD Overlay recording card stays small, quick-access, and easy to understand. It should avoid redundant detail such as showing both current overlay and recording overlay when those values are the same by design.",
            "- The standalone Recording Control window is the richer place for selected recording target, locked snapshot target, readiness state, recording status, approved future Start/Stop controls, and proof-oriented detail.",
            "- The active Overlay Profile remains the USER-facing source for what is eligible to be recorded; when recording starts, the session locks a snapshot of the then-active overlay membership.",
            "- Sensors added to the active Overlay Profile during an active recording do not join the current recording session; they become eligible for the next recording after a new recording starts.",
            "- Hidden recording target state is rejected as a product direction. USER should be able to inspect what will be recorded before recording behavior is approved.",
            "- The branch should not ask USER to manage a separate Recording Profile unless BP1 is revised or USER later reopens that model.",
            "- Native Log Loader remains a separate future graph/log viewer, not part of this branch's durable implementation unless USER later admits it.",
            "- In this BP1 packet, USER is deciding whether that future experience is the right product direction before BP2 planning.",
            "",
            "## How It Will Function",
            "",
            "The future implementation should treat the active Overlay Profile as the recording target source and use snapshot-at-start semantics. A recording session records the sensors and membership active on the Overlay Profile at the moment recording starts. Later Overlay Profile additions become eligible for the next recording session, not the current active one. The HUD Overlay recording card provides quick access and simple action visibility, while the Recording Control window reflects selected target, locked snapshot target, readiness state, recording status, and future control details. BP2 must plan this target model and proof path; BP3 must validate orchestration; Workstream implementation remains blocked until USER separately approves implementation.",
            "",
            "## User Experience Flow",
            "",
            "1. USER reviews or selects the active Overlay Profile before recording.",
            "2. USER sees a small HUD Overlay recording card for quick access and simple recording action visibility.",
            "3. USER opens the Recording Control window for richer target/status/readiness detail, including the selected target and future locked snapshot target.",
            "4. A future approved recording session snapshots the active Overlay Profile membership at Start; sensors added during that session wait for the next recording.",
            "5. Later approved implementation may add real Start/Stop, output-file proof, tray controls, and export/share behavior.",
            "6. Later Live Validation and UTS proof must show the accepted target model, stale/missing-target behavior, rollback posture, and user-visible controls behave as planned.",
            "",
            "## Surface Map",
            "",
            "- Active Overlay Profile: source of truth for target eligibility before recording starts.",
            "- Snapshot-at-start target state: future locked session target derived from active Overlay Profile membership at Start.",
            "- Dashboard HUD Overlay recording card: minimal quick-access and simple action visibility surface, not the rich detail panel.",
            "- Standalone Recording Control window: richer future detail/status/control surface for selected target, locked snapshot target, readiness, recording status, and approved controls.",
            "- Decision surface: USER response to this BP1 packet decides whether snapshot-at-start, minimal HUD card, richer Recording Control detail, and hidden-target rejection are accepted for BP2 planning.",
            "- Output/proof surfaces: future BP2/H1/LV/UTS evidence for target preview, Recording Control window, target-state behavior, stale/missing-target behavior, rollback, and recorded files when file writing is later approved.",
            "- Native Log Loader: future separate graph/log viewer, preserved as context only.",
            "- Per-overlay effective polling policy: future FAM-006 architecture planning input, not implementation authority in BP1.",
            "",
            "## Product Options / Design Paths",
            "",
            "- Option A - Active Overlay Profile with snapshot-at-start target model. Accepted as the gold-standard direction for review: it keeps target selection visible and stable during a recording session. Tradeoff: BP2 must define clear stale/missing-target and next-session behavior.",
            "- Option B - Separate Recording Profile system. Rejected for this branch unless USER later reopens it; it adds another profile concept and raises drift risk between what USER monitors and what USER records.",
            "- Option C - Small HUD card plus richer Recording Control window. Recommended: HUD stays quick-access and low-clutter, while Recording Control carries target, snapshot, readiness, status, and future control detail. Tradeoff: BP2 must be precise about which details live in each surface.",
            "- Option D - Hidden target state or file-writing-first implementation. Rejected as current product direction because USER trust depends on inspecting the recording target before recording behavior is approved.",
            "",
            "## Codex Recommendations",
            "",
            "- Recommendation: Carry snapshot-at-start into BP2 as the accepted direction for review: a recording records the sensors active when Start happens, and sensors added later become eligible for the next recording. Tradeoff: BP2 must define how the UI explains the locked snapshot and next-session eligibility. USER response:",
            "- Recommendation: Keep the HUD Overlay recording card small and quick-access, with future Start/Stop affordance only after separate implementation approval. Tradeoff: richer status detail moves into Recording Control instead of being visible directly on the HUD card. USER response:",
            "- Recommendation: Make the Recording Control window the richer target/status/readiness/control surface because it can explain selected target, locked snapshot target, stale/missing-target behavior, and recording status without cluttering the HUD. Tradeoff: USER may need one extra click for full detail. USER response:",
            "- Recommendation: Require BP2 to plan target preview proof, Recording Control window proof, target-state proof, stale/missing-target behavior proof, rollback proof, and Live Validation / UTS expectations before BP3. Tradeoff: planning takes longer, but hidden target drift is less likely to survive into runtime. USER response:",
            "- Recommendation: Reject hidden recording target state and keep the separate Recording Profile system outside this branch unless USER explicitly reopens it. Tradeoff: this limits flexibility, but it keeps recording understandable and aligned with the active Overlay Profile model. USER response:",
            "- Recommendation: Keep Native Log Loader and per-overlay effective polling policy as future planning inputs unless USER explicitly admits them into this branch because they can widen FAM-006 beyond active-overlay recording. Tradeoff: BP2 may need to name integration placeholders without implementing those systems. USER response:",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "This vision keeps Nexus local, visible, and USER-controlled: the USER can inspect the selected target, understand the snapshot-at-start recording path, and approve proof expectations before runtime work begins. It avoids hidden recording target state, avoids multiplying profile systems without USER approval, and keeps richer status detail in a dedicated local desktop control surface.",
            "",
            "## USER Design Questions",
            "",
            "- Do you accept snapshot-at-start as the final BP1 target model, with added sensors joining the next recording rather than the active one?",
            "- Do you accept the HUD Overlay recording card as a minimal quick-access surface rather than a rich detail/status surface?",
            "- Do you accept the Recording Control window as the richer detail surface for selected target, locked snapshot target, readiness, recording status, and future controls?",
            "- Do you reject hidden recording target state and keep a separate Recording Profile system outside this branch unless later reopened?",
            "- Should BP2 treat target preview proof, Recording Control proof, target-state proof, stale/missing-target proof, rollback proof, and LV/UTS expectations as required plan lines?",
            "",
            "## USER Response",
            "",
            "Pending USER response or explicit waiver.",
            "",
            "## Codex Digest",
            "",
            "Pending USER response digest.",
            "",
            "## USER Response Proof",
            "",
            "Pending USER response or explicit waiver.",
            "",
            "## USER Response Digested",
            "",
            "No - BP1 remains open until Codex digests an explicit USER response or waiver.",
            "",
            "## Accepted Branch Vision",
            "",
            "Pending USER acceptance or waiver.",
            "",
            "## Family-Vision Versus Branch-Only Vision Impact",
            "",
            "Branch-only for this BP1 packet until USER accepts or revises the vision. If accepted, the snapshot-at-start target model, minimal HUD card role, richer Recording Control window role, and hidden-target rejection may need to fold into the FAM-006 family vision or active branch plan during BP2.",
            "",
            "## Must-Have Behavior",
            "",
            "- BP1 must close through USER acceptance or explicit waiver before BP2 becomes active.",
            "- BP2 must derive the engineering route from this accepted active-overlay recording vision.",
            "- BP3 must validate the BP2 plan against accepted BP1 before any Workstream implementation approval is legal.",
            "- Future runtime proof must show the active Overlay Profile snapshot-at-start target model clearly enough for USER to verify.",
            "- USER must be able to inspect what will be recorded before recording behavior is approved.",
            "",
            "## Must-Not-Do / Regression-Risk Rules",
            "",
            "- Do not create a separate Recording Profile system unless USER explicitly revises BP1 in that direction.",
            "- Do not hide recording target state from USER review.",
            "- Do not clutter the HUD card with redundant current-overlay/recording-overlay detail when those values are the same by design.",
            "- Do not implement recording execution, file writing, Start/Stop controls, tray controls, export/share, provider/model work, or Native Log Loader as part of BP1.",
            "- Do not use Workstream for planning or treat this reviewable packet as USER acceptance.",
            "- Do not let copied source-truth files replace the applied FAM-006 branch vision.",
            "",
            "## Deferred And Future-Gated Ideas",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
            "## Vision Question Queue",
            "",
            "Pending USER review of the design questions above.",
            "",
            "## Design Assumption Ledger",
            "",
            "- Assumption: active Overlay Profile snapshot-at-start is the preferred recording target model unless USER revises BP1.",
            "- Assumption: HUD Overlay recording card stays minimal while Recording Control carries richer target/status/readiness/control detail.",
            "- Assumption: Native Log Loader remains future separate graph/log viewer context.",
            "- Assumption: per-overlay effective polling policy remains future FAM-006 architecture planning input.",
            "",
            "## Acceptance / Revision / Rejection / Waiver Decision",
            "",
            "- Accept: USER accepts this active-overlay recording Branch Vision and authorizes BP2 preparation only.",
            "- Revise: USER requests specific changes to the target model, surfaces, options, proof expectations, or future-gated boundaries before BP2.",
            "- Hold / More Options: USER wants additional product options or examples before accepting or rejecting BP1.",
            "- Reject: USER rejects this branch vision or routes the work to a different product direction.",
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
        "v2 - generated by the local USER hub helper with substantive BP1 review sections.",
        "",
        "## Project Vision Context",
        "",
        f"`{title}` must explain how this branch supports Nexus as a USER-controlled, inspectable desktop AI system before engineering planning begins. The copied context ({copied_context}) is evidence for that fit; the USER should judge whether the branch direction belongs in the project vision rather than treating a clean packet as approval.",
        "",
        "## Family Vision Context",
        "",
        f"This BP1 review asks whether `{title}` fits the owning family or governance lane represented by the copied source-truth files. If the branch changes reusable family direction, the USER response must name that family impact so Codex can route it to the proper durable owner before BP2.",
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
        f"Create an accepted USER-facing branch vision for `{title}` before engineering planning. The goal is to turn `{review_purpose}` into a clear decision surface: what the branch is meant to accomplish, what USER will inspect, and what must remain blocked until BP2/BP3 and separate implementation approval.",
        "",
        "## End-State Vision",
        "",
        f"When BP1 closes, USER should be able to say exactly what `{title}` is allowed to become, what future USER-visible or governance behavior should be true, and which outcomes are deliberately deferred. A later green BP2/BP3 must trace to this accepted end-state instead of inventing product direction during implementation.",
        "",
        "## What Will I Actually See, And Where Will I See It?",
        "",
        f"USER sees this Branch Vision review in the stable local USER hub packet beside the copied context files named in `START_HERE.md`. The visible review surface is not the raw file list; it is this applied explanation of `{title}`, the decision options, the recommendation rationale, and the questions USER can answer before BP2.",
        "",
        "## How It Will Function",
        "",
        f"BP1 captures the intended outcome for `{title}`. BP2 must translate only the accepted or waived BP1 vision into an engineering plan, BP3 must validate orchestration against both accepted gates, and Workstream implementation remains blocked until those gates are green plus the USER gives a separate implementation decision.",
        "",
        "## User Experience Flow",
        "",
        f"USER starts at `START_HERE.md`, reads this vision review, checks the source-truth context only as supporting evidence, then responds to the options and design questions below. Codex must digest that response into accepted, revised, waived, rejected, or blocked BP1 state before preparing BP2.",
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
        f"- Option A - accept the `{title}` vision as the right direction: lowest planning churn, but only safe if USER can already visualize the outcome and boundaries.",
        "- Option B - revise the vision before BP2: best when the branch goal is directionally right but USER wants different surfaces, experience flow, proof expectations, or future-gated boundaries.",
        "- Option C - waive or reject BP1: waiver should be rare and explicit; rejection is safer when the branch belongs to another family, architecture owner, policy owner, or later branch.",
        "",
        "## Codex Recommendations",
        "",
        f"- Recommendation: Use this packet to decide the `{title}` branch vision before any BP2 engineering plan is treated as valid, because the main risk is Codex building from a technically clean but weak product direction. Tradeoff: this adds one deliberate review pause, but it prevents expensive Workstream rework.",
        "  USER response:",
        f"- Recommendation: Require any revision to name the expected USER-visible, governance, or source-truth outcome for `{title}` rather than only saying the packet should be clearer. Tradeoff: stricter response digestion takes more care, but it gives BP2 a real contract to build from.",
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
        f"- For `{title}`, what exact outcome should USER expect to see, inspect, or rely on when this branch is complete?",
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
    is_fam006_active_overlay_implementation = (
        source_branch == FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH
        or any(
            FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_SLUG in source_rel
            for source_rel, _copied_rel in copied
        )
    )
    normalized_decision = exact_user_decision.casefold()
    fam006_bp3_packet = (
        is_fam006_active_overlay_implementation
        and (
            "bp3" in normalized_decision
            or "workstream entry" in normalized_decision
            or "orchestration validation" in normalized_decision
        )
    )
    fam006_bp2_packet = (
        is_fam006_active_overlay_implementation
        and ("bp2" in normalized_decision or "branch plan review" in normalized_decision)
        and "bp1" not in normalized_decision
        and not fam006_bp3_packet
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
    if is_fam006_active_overlay_implementation and fam006_bp3_packet:
        accepted_bp2_guardrails = [
            "BP2 is USER accepted and is included here only as Review Aid evidence for active BP3.",
            "BP2 derives the engineering route from accepted BP1 active-overlay recording vision.",
            "SLC-051 Active Overlay recording target foundation remains the default first bounded Workstream seam.",
            "SLC-052 minimal HUD preview may pair only if BP3 proves target proof and minimal preview are inseparable and still safe.",
            "Recording Control window work remains later unless USER separately approves it after BP3.",
            "Durable output contract work remains later; SLC-054 is output-contract planning only until file writing is separately approved.",
            "Recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance mutation remain blocked.",
        ]
        lines = [
            "# USER Branch Plan Review - Accepted BP2 Context For BP3",
            "",
            f"Title: {title}",
            f"Review Purpose: {review_purpose}",
            "",
            "## Contract Status",
            "",
            "Complete - USER accepted the BP2 Branch Plan and approved BP3 preparation.",
            "",
            "## Packet Reviewability State",
            "",
            "Reviewable - this Review Aid preserves accepted BP2 context for active BP3 Workstream Entry / Orchestration Validation.",
            "",
            "## USER Gate State",
            "",
            "USER Accepted - BP2 is accepted. The active current USER gate is BP3, which remains Pending USER Review.",
            "",
            "## USER Response Proof",
            "",
            "Accepted by USER - USER accepted the FAM-006 BP2 Branch Plan and approved Codex to prepare BP3 Workstream Entry / Orchestration Validation.",
            "",
            "## USER Response Digested",
            "",
            "Digested - accepted BP2 guardrails are carried into BP3 reviewability, including actual file ownership verification, SLC-051 as default first seam, SLC-052 pairing limits, runtime/file-writing boundaries, rollback, H1, LV, and UTS expectations.",
            "",
            "## Acceptance / Waiver / Revision / Rejection Receipt",
            "",
            "Accepted - BP2 closure allows BP3 review preparation only. It does not approve BP3, Workstream implementation, SLC-051 implementation, runtime mutation, recording execution, or file writing.",
            "",
            "## Contract Version / Revision",
            "",
            "v4 - Accepted BP2 support context regenerated for active BP3 so Review Aids no longer contradict the active gate.",
            "",
            "## Current Gate",
            "",
            "The active current gate is BP3 Workstream Entry / Orchestration Validation for FAM-006 Active Overlay Recording Runtime Implementation.",
            "The primary current-gate USER decision file is under `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`.",
            "BP3 remains Pending USER Review. Workstream implementation remains blocked.",
            "",
            "## Plain-English Branch Summary",
            "",
            "FAM-006 will build recording around the active Overlay Profile the USER already uses. The accepted BP2 plan keeps the active Overlay Profile as the future target source, keeps snapshot-at-start as the target model, keeps the HUD Overlay card small and quick-access, and keeps Recording Control as the richer future surface.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "After later BP3 acceptance and separate implementation approval, USER should see concise target/status information and an Open Recording Control path in the HUD Overlay card, then richer target/readiness/status/control detail in a compact standalone Recording Control window. This BP3 packet itself changes no runtime UI.",
            "",
            "## End-State Vision",
            "",
            "The accepted BP2 end state is a recording foundation that feels connected to the overlay USER already chose: active Overlay Profile membership defines the future target, Start later locks a snapshot of that target, the HUD card gives quick access without clutter, Recording Control explains richer target/readiness/status detail, and completed logs can later feed a separate Native Log Loader.",
            "",
            "## Visual / Functional Walkthrough",
            "",
            "- USER has or selects an active Overlay Profile.",
            "- HUD Overlay card previews concise recording target/status without redundant current-overlay / recording-overlay detail when the values are intentionally identical.",
            "- USER opens Recording Control for richer target/readiness/status detail after that later surface is approved.",
            "- When recording execution is later admitted, Start snapshots the target membership at that moment.",
            "- Sensors added during an active recording wait for the next session.",
            "- Completed logs are designed for future graphing by Native Log Loader, but the loader remains separate and future-gated.",
            "",
            "## Surface Map",
            "",
            "- Active Overlay Profile: accepted recording target source.",
            "- HUD Overlay recording card: quick launcher and concise target/status preview.",
            "- Standalone Recording Control window: richer future target/readiness/status/control surface.",
            "- Recording output contract: future deterministic graph/plot-ready output planning, not file writing approval.",
            "- Native Log Loader: separate future graph/log viewer.",
            "- USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md: active BP3 decision surface.",
            "",
            "## Implementation Options",
            "",
            "- Option A - SLC-051 target proof first. Recommended because every later surface depends on trustworthy target truth.",
            "- Option B - combine target proof with minimal HUD preview only if BP3 proves inseparability and safety.",
            "- Option C - keep Recording Control shell later so SLC-051 stays bounded.",
            "- Option D - keep output/file-writing work later unless USER separately approves that boundary.",
            "",
            "## Recommended Direction",
            "",
            "Codex recommends BP3 validate SLC-051 Active Overlay recording target foundation as the first bounded Workstream seam. The tradeoff is a slower path to visible recording controls, but it prevents hidden-target, stale-owner, and file-writing drift before target truth is proven.",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "The accepted BP2 plan keeps recording local, visible, user-controllable, and truthful. USER can inspect what will be recorded before recording behavior or file writing is approved.",
            "",
            "## USER Plan Review Decision",
            "",
            "BP2 is already accepted. No new BP2 decision is requested by this Review Aid. The active decision is BP3 acceptance, revision, rejection, hold, request for more options, or waiver in `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`.",
            "",
            "## USER Decisions Needed",
            "",
            "- BP3 Workstream Entry / Orchestration Validation acceptance, revision, rejection, hold, or waiver.",
            "- Workstream implementation and SLC-051 implementation.",
            "- Runtime mutation, recording execution, file writing, real Start/Stop controls, tray controls, export/share behavior, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, branch cleanup, and Governance worktree mutation.",
            "",
            "## USER Response",
            "",
            "BP2 USER response is accepted and digested. Active USER response is now needed for BP3 in `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`.",
            "",
            "## Codex Response Digest",
            "",
            "Codex digested BP2 acceptance into the FAM-006 branch record, branch plan, and active BP3 packet. This file is accepted BP2 context only.",
            "",
            "## Implementation Constraints Created By USER Response",
            "",
            *_markdown_lines(accepted_bp2_guardrails),
            "",
            "## USER Rejected / Deferred Ideas",
            "",
            "- Rejected: hidden recording target state.",
            "- Rejected unless USER later reopens: separate Recording Profile system.",
            "- Deferred: Recording Control implementation, durable output/file writing, Native Log Loader implementation, per-overlay effective polling policy implementation, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, and cleanup.",
            "",
            "## Vision Delta / Source-Truth Impact",
            "",
            "BP2 acceptance is recorded in the FAM-006 branch record and branch plan. BP3 must validate accepted BP2 against accepted BP1 before recommending a first bounded implementation seam.",
            "",
            "## Contract Change Log",
            "",
            "- v1 - Generated as active BP2 after USER accepted the FAM-006 BP1 Branch Vision.",
            "- v4 - Regenerated as accepted BP2 context for active BP3.",
            "",
            "## Current Branch Scope",
            "",
            "- Active-overlay-driven FAM-006 recording runtime foundation planning.",
            "- SLC-051 through SLC-055 as the whole-package engineering route after BP3 closes.",
            "- BP3 reviewability only; no implementation authority.",
            "",
            "## Future-Gated Scope",
            "",
            "BP3 acceptance, Workstream implementation, SLC-051 implementation, runtime mutation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance mutation remain pending.",
            "",
            "## Implementation Staging Notes",
            "",
            *_markdown_lines(accepted_bp2_guardrails),
            "",
            "## Workstream Entry Result",
            "",
            "Active - BP3 is the current USER Review Gate and remains Pending USER Review. This packet may recommend SLC-051 as the first bounded seam, but implementation remains blocked until BP3 is accepted or waived and USER separately approves implementation.",
            "",
            "## Contract Completion Checklist",
            "",
            "- BP1 accepted: complete.",
            "- BP2 accepted: complete.",
            "- BP3 primary review file present: `USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md`.",
            "- BP3 USER response: pending.",
            "- Workstream implementation: blocked pending separate USER approval.",
            "",
            "## Exact USER Decision Supported By The Current Packet",
            "",
            exact_user_decision,
            "",
            "## Pending USER Decisions",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
        ]
        review_path = target / USER_BRANCH_PLAN_REVIEW_FILE
        review_path.write_text("\n".join(lines), encoding="utf-8")
        return review_path.resolve()
    if is_fam006_active_overlay_implementation and fam006_bp2_packet:
        accepted_bp1_decisions = [
            "BP1 is accepted for the active-overlay-driven recording branch vision.",
            "Active Overlay Profile membership is the recording target source.",
            "Snapshot-at-start is the accepted default target model: a recording session uses the sensors and membership active when recording starts.",
            "Sensors added to the active Overlay Profile during a recording become eligible for the next recording session, not the current one.",
            "The HUD Overlay recording card stays small, quick-access, low-clutter, and easy to understand.",
            "The HUD Overlay card should avoid redundant current-overlay / recording-overlay detail when both are intentionally the same.",
            "The standalone Recording Control window carries richer target, readiness, status, and future control detail.",
            "Hidden recording target state is rejected.",
            "A separate Recording Profile system remains outside this branch unless USER explicitly reopens it later.",
            "Native Log Loader remains a future separate graph/log viewer.",
            "Per-overlay effective polling policy remains future FAM-006 architecture planning unless separately admitted.",
        ]
        surface_map = [
            "HUD Overlay recording card: quick launcher, concise target/status preview, and later Start/Stop affordance only after real controls are separately approved.",
            "Standalone Recording Control window: compact normal OS/NDAI window for richer target/readiness/status/control detail, independent from Dashboard lifetime.",
            "Overlay Profile: source of active recording target membership and snapshot-at-start membership.",
            "Monitor Groups / Sensor Command Center: reusable sensor organization surfaces; not mutated into a recording-specific chooser by BP2.",
            "Recording output contract: future graph/plot-ready file contract planned before or alongside admitted recording execution.",
            "Native Log Loader: future separate graph/log viewer, not the recording control surface in this branch.",
        ]
        likely_files = [
            "Confirmed existing owner - `desktop/ui/dashboard_hud_panel.py`: Dashboard/HUD surface owner for future low-redundancy recording card preview and launcher work.",
            "Confirmed existing owner - `dev/orin_monitoring_hud_surface_validation.py`: FAM-006 HUD/Dashboard source-truth and surface validator.",
            "Confirmed existing owner - `dev/orin_monitoring_hud_internal_sandbox_validation.py`: FAM-006 internal sandbox/state-boundary validator.",
            "Confirmed existing owner - `dev/orin_validation_suite.py`: broader FAM-006 runtime validation recommendation owner.",
            "Probable new file - `desktop/ui/recording_control_window.py`: standalone compact Recording Control window if BP3 verifies this is the clean UI owner and USER later approves implementation.",
            "Uncertain owner for BP3 verification - active Overlay Profile state source: BP3 must identify the exact current owner for active Overlay Profile ID/name, membership, stale/deleted profile state, and empty membership behavior before SLC-051 implementation can be approved.",
            "Uncertain owner for BP3 verification - recording target/session model: BP3 must decide whether this belongs in an existing state/model module or a new recording-target planning module before implementation.",
            "Blocked until later implementation approval - recording runtime, file-writing, output-file creation, Start/Stop execution, tray control, export/share, and Native Log Loader implementation owners are not admitted by BP2 and must not be treated as confirmed files.",
        ]
        slc_package_plan = [
            "SLC-051 - Active Overlay recording target foundation: recommended first bounded Workstream seam after BP3 and separate implementation approval. It must prove active Overlay Profile ID/name, target membership snapshot at recording start, immutable session target summary, null/empty/stale/deleted/high-volume target states, and next-session eligibility for sensors added after recording starts before visible controls depend on it.",
            "SLC-052 - HUD Overlay recording launcher and active-monitor transparency: may pair with SLC-051 only if BP3 proves target proof and minimal HUD preview are inseparable and still safe. The HUD card must stay small, quick-access, low-clutter, and avoid redundant current-overlay / recording-overlay text when both values are intentionally the same.",
            "SLC-053 - standalone Recording Control window foundation: create the compact independent control surface and route bulky settings to secondary surfaces when approved.",
            "SLC-054 - durable recording output contract: may define a deterministic graph/plot-ready output contract and readback expectations, but BP2 does not approve recording file writing, output-file creation, output-file proof, export/share, or recording execution.",
            "SLC-055 - validation/live proof readiness: wire H1, LV, screenshot/photo comparison, UTS, stale-target, rollback, and future-gated boundary proof.",
        ]
        proof_requirements = [
            "Target preview proof: active Overlay Profile ID/name and membership summary are visible where planned and match the source state.",
            "Snapshot-at-start proof: future recording state must include the active Overlay Profile ID/name at recording start, the target membership snapshot at recording start, and an immutable session target summary.",
            "Next-session eligibility proof: sensors added after recording starts must be shown as eligible for the next session rather than silently added to the active session target.",
            "Recording Control proof: the standalone window opens from the HUD path, stays compact, is movable/minimizable/restorable, and shows richer target/readiness/status detail.",
            "Target-state proof: null profile, empty membership, selected profile, switched profile, deleted/stale profile, missing profile, duplicate/stale ID, and high-volume membership states are covered.",
            "Stale/missing/deleted-target behavior proof: USER can understand when the target is unavailable, empty, stale, missing, or deleted before recording behavior is approved; no hidden recording target state is allowed.",
            "Rollback proof: disabling or reverting recording surfaces leaves Overlay Profile, Overlay Display, Monitor Groups, Sensor Command Center, and Dashboard behavior intact.",
            "Live Validation / UTS proof: visible surfaces use real user-level input, focused screenshots, compact/default comparison, and USER Test Summary handoff when runtime surfaces ship.",
        ]
        user_decisions = [
            "Accept BP2 as the engineering plan for the accepted BP1 active-overlay recording vision.",
            "Request BP2 revisions to the target model, HUD card details, Recording Control window, proof expectations, SLC route, or future-gated boundaries.",
            "Route back to BP1 only if the plan changes the accepted branch vision.",
            "Explicitly waive BP2 remaining questions with named constraints.",
            "Reject or hold BP2 and name the blocker.",
        ]
        lines = [
            "# USER Branch Plan Review - FAM-006 Active Overlay Recording Runtime Implementation",
            "",
            f"Title: {title}",
            f"Review Purpose: {review_purpose}",
            "",
            "## Contract Status",
            "",
            "Pending USER Response - BP2 engineering plan is reviewable and awaits USER acceptance, revision, rejection, hold, or waiver.",
            "",
            "## Packet Reviewability State",
            "",
            "Reviewable - helper generated a branch-specific BP2 engineering plan from accepted BP1 decisions.",
            "",
            "## USER Gate State",
            "",
            "Pending USER Review - BP2 is not accepted or waived until USER responds.",
            "",
            "## USER Response Proof",
            "",
            "Pending USER Response - BP2 gate remains open.",
            "",
            "## USER Response Digested",
            "",
            "Pending USER Response - Codex has not digested a final BP2 USER disposition.",
            "",
            "## Acceptance / Waiver / Revision / Rejection Receipt",
            "",
            "Pending - this packet requests BP2 review only; it does not approve BP3, Workstream, SLC-051, runtime mutation, recording execution, or file writing.",
            "",
            "## Contract Version / Revision",
            "",
            "v2 - FAM-006 BP2 engineering plan revised after USER/ChatGPT review to tighten file ownership, SLC-054 boundaries, HUD low-redundancy behavior, snapshot-at-start proof concepts, and first-seam recommendation while keeping BP2 pending USER review.",
            "",
            "## Plain-English Branch Summary",
            "",
            "FAM-006 will build recording around the active Overlay Profile the USER already uses. The accepted vision is not a separate Recording Profile chooser: the active Overlay Profile supplies the target, the HUD Overlay card stays small and clear, and the standalone Recording Control window carries richer target/status/control detail after later implementation approval.",
            "",
            "## Accepted Branch Vision Summary",
            "",
            *_markdown_lines(accepted_bp1_decisions),
            "",
            "## Implementation Package Summary",
            "",
            "The branch should remain one coherent active-overlay recording package because target state, HUD visibility, Recording Control behavior, output contract, and validation proof all depend on each other. BP2 plans that package; BP3 must still validate orchestration before any implementation approval can be offered.",
            "",
            "## Branch Scope Size Test",
            "",
            "This is the largest safe feature-focused package for FAM-006 recording: it keeps target selection, visible preview, control surface, output contract, and proof expectations together while excluding unrelated tray, export/share, provider/model, broad theme, FAM-007, and Native Log Loader implementation work.",
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
            *_markdown_lines(likely_files),
            "",
            "## Validators / Helpers",
            "",
            "- `python dev\\orin_monitoring_hud_surface_validation.py` for HUD/Dashboard-facing FAM-006 surface expectations.",
            "- `python dev\\orin_monitoring_hud_internal_sandbox_validation.py` for internal FAM-006 sandbox and state-boundary expectations.",
            "- `python dev\\orin_validation_suite.py --phase runtime-fam006 --format text` for the broader runtime-FAM006 recommendation suite.",
            "- `python dev\\orin_user_review_bundle.py --validate-workstream-entry-packet C:\\Nexus USER\\FAM-006 ...` for packet phase-state and stale-wording checks.",
            "- Existing branch governance, release body, AI provider state, source-owner marker, diff, and compile validations remain required before later gates.",
            "",
            "## Proof Requirements",
            "",
            *_markdown_lines(proof_requirements),
            "",
            "## Snapshot-At-Start State Model",
            "",
            "- Future state concept: record the active Overlay Profile ID/name at recording start.",
            "- Future state concept: record a target membership snapshot at recording start.",
            "- Future state concept: expose an immutable session target summary for USER review and proof.",
            "- Future behavior concept: sensors added after recording starts become eligible for the next session, not the active session.",
            "- Required error-state concept: stale, missing, deleted, null, and empty Overlay Profile membership states must be explicit and user-visible before recording behavior is approved.",
            "- Required UX concept: no hidden recording target state; USER must see or be able to open a clear target explanation before recording execution or file writing is admitted.",
            "- Boundary: this section defines planning/proof concepts only and does not approve runtime mutation, recording execution, file writing, or output-file creation.",
            "",
            "## Element-To-Phase Proof Matrix",
            "",
            "- BP1 accepted vision: active Overlay Profile target source, snapshot-at-start default, minimal HUD card, richer Recording Control window, hidden target rejection, rejected separate Recording Profile.",
            "- BP2 plan: this file maps those accepted vision lines into SLC-051 through SLC-055, affected surfaces, validators, proof outputs, risks, and rollback posture.",
            "- BP3 orchestration: must verify that BP2 traces to BP1 and can recommend the first bounded implementation seam without granting implementation by itself.",
            "- Workstream: runtime/code implementation only after BP3 and a separate USER implementation approval.",
            "- Hardening: pressure-test implementation against accepted BP1/BP2 and repair defects inside approved scope.",
            "- Live Validation / UTS: prove user-facing behavior with real interaction and USER-facing evidence after visible implementation exists.",
            "",
            "## H1 Expectations",
            "",
            "- H1 must stress active target states, compact HUD/Recording Control layout, stale/missing target behavior, Dashboard/Overlay Profile/Overlay Display/Monitor Group regressions, output contract determinism if admitted, and future-gated boundary preservation.",
            "",
            "## LV / UTS Expectations",
            "",
            "- LV must use real mouse/keyboard interaction for visible controls, focused screenshots for HUD card and Recording Control states, compact/default comparison, and output-file proof only if file writing is later admitted.",
            "- UTS must ask USER to confirm target visibility, snapshot-at-start explanation, no hidden target state, no separate Recording Profile requirement, compact control usability, rollback posture, and any implemented output behavior.",
            "",
            "## Rollback / Safety Plan",
            "",
            "- Keep active-overlay recording behind BP3 and separate implementation approval until USER grants it.",
            "- Preserve Overlay Profile and Monitor Group ownership boundaries; do not add a Recording Profile selector as an accidental rollback workaround.",
            "- If future implementation misbehaves, rollback should disable/remediate recording-specific UI/runtime paths without corrupting Overlay Profile membership, Dashboard, Manage Monitors, Sensor Command Center, or existing overlay display behavior.",
            "- If output contract proof fails, keep file-writing blocked or roll it back before claiming Live Validation readiness.",
            "",
            "## Open Engineering Risks",
            "",
            "- The exact runtime owner files for active Overlay Profile state, target/session model state, and future recording output must be confirmed during BP3 before implementation.",
            "- Snapshot-at-start must be explained clearly enough that USER understands sensors added mid-recording are next-session eligible.",
            "- A small HUD card may become cluttered if it repeats current-overlay / recording-overlay labels that are intentionally the same or tries to show details that belong in Recording Control.",
            "- Recording Control can become bulky unless secondary settings/details surfaces are used for advanced fields.",
            "- File-writing must not be admitted through target-preview or UI-shell work by accident.",
            "",
            "## Future-Gated Boundaries",
            "",
            "- BP3 Workstream Entry / Orchestration Validation remains pending.",
            "- Workstream implementation and SLC-051 remain pending separate USER approval.",
            "- Runtime mutation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance mutation remain pending.",
            "- Native Log Loader implementation and per-overlay effective polling policy implementation remain future-gated unless USER separately admits them.",
            "",
            "## Line-Item USER Plan Review",
            "",
            *_markdown_lines(user_decisions),
            "",
            "## Plan Acceptance Checklist",
            "",
            "- BP2 traces every accepted BP1 decision to a planned implementation/proof line.",
            "- SLC-051 through SLC-055 remain the engineering route inside this branch, not automatic separate branches.",
            "- Runtime implementation remains blocked until BP3 is green and USER separately approves implementation.",
            "- The plan preserves active-overlay-driven recording and rejects hidden target state and separate Recording Profile drift.",
            "- Proof covers target preview, Recording Control window, target-state, stale/missing-target, rollback, H1, LV, and UTS expectations.",
            "",
            "## Exact BP3 Approval Text When Ready",
            "",
            "I accept the BP2 Branch Plan for FAM-006 Active Overlay Recording Runtime Implementation and approve Codex to prepare BP3 Workstream Entry / Orchestration Validation in C:\\Nexus Worktrees\\FAM-006 on feature/fam-006-active-overlay-recording-runtime-implementation. Runtime implementation remains pending a separate USER decision.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "After later BP3 and implementation approval, USER should see concise target/status information and an Open Recording Control path in the HUD Overlay card, then richer target/readiness/status/control detail in a compact standalone Recording Control window. This BP2 packet itself changes no runtime UI.",
            "",
            "## End-State Vision",
            "",
            "The accepted end state is a recording foundation that feels connected to the overlay USER already chose: active Overlay Profile membership defines the future target, Start later locks a snapshot of that target, the HUD card gives quick access without clutter, Recording Control explains richer target/readiness/status detail, and completed logs can later feed a separate Native Log Loader.",
            "",
            "## Visual / Functional Walkthrough",
            "",
            "- USER has or selects an active Overlay Profile.",
            "- HUD Overlay card previews concise recording target/status without redundant current-overlay / recording-overlay detail when the values are intentionally identical.",
            "- USER opens Recording Control for richer target/readiness/status detail.",
            "- When recording execution is later admitted, Start snapshots the target membership at that moment.",
            "- Sensors added during an active recording wait for the next session.",
            "- Completed logs are designed for future graphing by Native Log Loader, but the loader remains separate/future.",
            "",
            "## Surface Map",
            "",
            *_markdown_lines(surface_map),
            "",
            "## Implementation Options",
            "",
            "- Option A - SLC-051 target proof first. Recommended because every later surface depends on trustworthy target truth.",
            "- Option B - combine target proof with minimal HUD preview if BP3 finds the files and proof path are tightly coupled.",
            "- Option C - build Recording Control shell before output/file-writing work so the future control surface stays compact and inspectable.",
            "- Option D - defer file-writing/output contract until after target/HUD/control proof if BP3 finds runtime risk too high.",
            "",
            "## Recommended Direction",
            "",
            "Codex recommends BP3 validate SLC-051 Active Overlay recording target foundation as the first bounded Workstream seam. SLC-052 minimal HUD preview may be paired only if BP3 proves target proof and minimal preview are inseparable and still safe. Recording Control window, SLC-054 output contract, file writing, Start/Stop controls, tray controls, and export/share should remain later seams unless separately justified and approved. The tradeoff is slower path to real recording, but it sharply reduces hidden-target and file-writing drift.",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "This keeps recording local, visible, user-controllable, and truthful. It avoids hidden automation, avoids a second profile system, protects output quality for future graphing, and keeps advanced behavior behind explicit USER decisions.",
            "",
            "## USER Plan Review Decision",
            "",
            "Choose whether this BP2 engineering plan correctly builds the accepted BP1 vision. Acceptance allows BP3 preparation only; it does not approve implementation.",
            "",
            "## USER Decisions Needed",
            "",
            *_markdown_lines(user_decisions),
            "",
            "## USER Response",
            "",
            "Pending USER Response - BP2 awaits USER acceptance, revision, rejection, hold, or waiver.",
            "",
            "## Codex Response Digest",
            "",
            "Pending USER Response - Codex must digest USER's BP2 response before BP3 can be prepared.",
            "",
            "## Implementation Constraints Created By USER Response",
            "",
            "- No implementation constraints beyond accepted BP1 and this proposed BP2 plan are final until USER responds.",
            "- Runtime implementation remains blocked.",
            "- Recording execution and file writing remain blocked.",
            "",
            "## USER Rejected / Deferred Ideas",
            "",
            "- Rejected: hidden recording target state.",
            "- Rejected unless USER later reopens: separate Recording Profile system.",
            "- Deferred: Native Log Loader implementation, per-overlay effective polling policy implementation, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, and cleanup.",
            "",
            "## Vision Delta / Source-Truth Impact",
            "",
            "BP1 acceptance is recorded in the FAM-006 branch record and branch plan. If BP2 is accepted, BP3 should validate this branch plan against the accepted vision and then recommend the first bounded Workstream implementation seam without claiming implementation approval.",
            "",
            "## Contract Change Log",
            "",
            "- v1 - Generated as active BP2 after USER accepted the FAM-006 BP1 Branch Vision.",
            "",
            "## Current Branch Scope",
            "",
            "- Active-overlay-driven FAM-006 recording runtime foundation planning.",
            "- SLC-051 through SLC-055 as the whole-package engineering route after BP2/BP3 close.",
            "- No FAM-007, provider/model, tray/export/share, release, PR, cleanup, or Governance mutation scope.",
            "",
            "## Future-Gated Scope",
            "",
            "- BP3, Workstream implementation, SLC-051 implementation, runtime mutation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance mutation remain pending.",
            "",
            "## Implementation Staging Notes",
            "",
            *_markdown_lines(slc_package_plan),
            "",
            "## Workstream Entry Result",
            "",
            "Not active - BP3 remains pending until USER accepts, waives, revises, rejects, or blocks BP2.",
            "",
            "## Contract Completion Checklist",
            "",
            "- BP2 accepted, revised, rejected, held, or explicitly waived by USER.",
            "- BP3 remains pending until BP2 closes.",
            "- Runtime implementation remains blocked until BP3 is green and USER separately approves implementation.",
            "",
            "## Exact USER Decision Supported By The Current Packet",
            "",
            exact_user_decision,
            "",
            "## Pending USER Decisions",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
        ]
        review_path = target / USER_BRANCH_PLAN_REVIEW_FILE
        review_path.write_text("\n".join(lines), encoding="utf-8")
        return review_path.resolve()
    if is_fam006_active_overlay_implementation:
        lines = [
            "# USER Branch Plan Review - BP2 Pending Context",
            "",
            f"Title: {title}",
            f"Review Purpose: {review_purpose}",
            "",
            "## Contract Status",
            "",
            "Draft - BP2 is pending context only until BP1 is accepted or waived.",
            "",
            "## Packet Reviewability State",
            "",
            "Reviewable - supporting context only for BP1; this file is not the current USER decision file.",
            "",
            "## USER Gate State",
            "",
            "Pending USER Review - BP1 must close before BP2 can become active.",
            "",
            "## USER Response Proof",
            "",
            "Pending - active BP1 USER response has not been accepted, revised, rejected, waived, or blocked.",
            "",
            "## USER Response Digested",
            "",
            "Pending - Codex has not digested an active BP1 USER response into BP2.",
            "",
            "## Acceptance / Waiver / Revision / Rejection Receipt",
            "",
            "Pending - no active BP2 receipt exists because BP1 remains the current gate.",
            "",
            "## Contract Version / Revision",
            "",
            "BP2 pending-context v1 for the post-governance-repair FAM-006 BP1 packet.",
            "",
            "## Current Gate",
            "",
            "The active current gate is BP1 USER Branch Vision Review for FAM-006 Active Overlay Recording Runtime Implementation.",
            "The primary current-gate USER decision file is under `USER Review/USER_BRANCH_VISION_REVIEW.md`.",
            "",
            "## Why This BP2 File Exists",
            "",
            "This file is retained under Review Aids as later-gate context so USER can see what BP2 will need after BP1 closes. It is not an accepted Branch Plan and it does not authorize BP3 or Workstream implementation.",
            "",
            "## Future BP2 Plan Requirements",
            "",
            "- Derive the engineering plan from the accepted or waived BP1 Branch Vision.",
            "- Preserve active-overlay-driven recording as the branch identity.",
            "- Keep the active Overlay Profile as the future recording target source.",
            "- Keep the HUD Overlay card as launcher and target/status preview.",
            "- Keep the standalone Recording Control window as the compact future control surface.",
            "- Keep Native Log Loader as a separate future graph/log viewer unless USER later changes source truth.",
            "- Treat SLC-051 through SLC-055 as the engineering route inside this branch after BP1 closes.",
            "- Keep runtime implementation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance mutation blocked unless separately approved.",
            "",
            "## Plain-English Branch Summary",
            "",
            "FAM-006 is preparing an active-overlay-driven recording runtime branch where the active Overlay Profile supplies the future recording target. BP1 decides whether that product direction is right before BP2 turns it into an engineering plan.",
            "",
            "## What Will I Actually See, And Where Will I See It?",
            "",
            "After later approvals and implementation, USER should see recording target/status in the HUD Overlay card and use a compact standalone Recording Control window. This BP1/BP2 planning packet itself changes no runtime UI.",
            "",
            "## End-State Vision",
            "",
            "The desired end state is recording that feels connected to the overlay USER already selected: active Overlay Profile membership defines the future target, the HUD Overlay card previews and launches recording control, and Native Log Loader remains a separate future graph/log viewer.",
            "",
            "## Visual / Functional Walkthrough",
            "",
            "- USER reviews the active Overlay Profile target concept in BP1.",
            "- After BP1 acceptance or waiver, BP2 maps that vision to SLC-051 through SLC-055.",
            "- After BP2 acceptance or waiver, BP3 validates orchestration before any Workstream implementation approval.",
            "",
            "## Surface Map",
            "",
            "- HUD Overlay card: future launcher and target/status preview.",
            "- Recording Control window: future compact standalone control surface.",
            "- Overlay Profile: future recording target source.",
            "- Monitor Group and Sensor Command Center: preserved source organization surfaces.",
            "- Native Log Loader: separate future graph/log viewer.",
            "",
            "## Implementation Options",
            "",
            "- Option A - target model proof first after BP3 and implementation approval.",
            "- Option B - HUD target preview after target model proof.",
            "- Option C - standalone Recording Control window shell after the target concept is stable.",
            "- Option D - live Start/Stop and file writing only after explicit runtime execution approval.",
            "",
            "## Recommended Direction",
            "",
            "Codex recommends preserving target-model-first implementation planning, then HUD preview, then standalone Recording Control, then output/proof work after BP1, BP2, BP3, and separate implementation approval legally close.",
            "",
            "## Why This Fits The Nexus Vision",
            "",
            "This keeps recording lightweight, visible, and user-controllable without creating a second Recording Profile system or hiding target selection from USER.",
            "",
            "## USER Plan Review Decision",
            "",
            "No BP2 decision is requested by this BP1 packet. USER should respond to BP1 first.",
            "",
            "## USER Decisions Needed",
            "",
            "The active decision is BP1 acceptance, revision, rejection, request for more options, or waiver.",
            "",
            "## USER Response",
            "",
            "Pending USER Response - active BP1 has not closed.",
            "",
            "## Codex Response Digest",
            "",
            "Pending USER Response - Codex cannot digest BP2 until BP1 closes.",
            "",
            "## Implementation Constraints Created By USER Response",
            "",
            "- Runtime implementation remains blocked.",
            "- SLC-051 through SLC-055 remain planning route candidates only.",
            "- Recording execution and file writing remain blocked.",
            "",
            "## USER Rejected / Deferred Ideas",
            "",
            "- Separate Recording Profile selection remains rejected unless USER later re-approves it.",
            "- Tray controls, export/share, provider/model work, FAM-007 mutation, and Native Log Loader implementation remain deferred.",
            "",
            "## Vision Delta / Source-Truth Impact",
            "",
            "Accepted BP1 feedback must fold into the FAM-006 branch record, branch plan, family vision where reusable, and later BP2 review artifact. This BP2 context file does not itself close any gate.",
            "",
            "## Contract Change Log",
            "",
            "v1 - Pending-context BP2 Review Aid generated during active BP1 packet preparation.",
            "",
            "## Current Branch Scope",
            "",
            "Current branch scope is FAM-006 active-overlay recording planning and later runtime implementation only after legal BP gate closure and separate implementation approval.",
            "",
            "## Future-Gated Scope",
            "",
            "BP2, BP3, Workstream implementation, SLC-051 implementation, runtime mutation, recording execution, file writing, real Start/Stop controls, tray controls, export/share, provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance mutation remain pending.",
            "",
            "## Implementation Staging Notes",
            "",
            "SLC-051 through SLC-055 remain the likely engineering route inside this branch after BP1 closes and BP2 is prepared, reviewed, and accepted or waived.",
            "",
            "## BP2 Cannot Start Yet",
            "",
            "BP2 preparation requires accepted or waived BP1 proof. Packet reviewability is not USER acceptance.",
            "",
            "## Workstream Entry Result",
            "",
            "Not active - BP3 is blocked until BP1 and BP2 close legally.",
            "",
            "## Contract Completion Checklist",
            "",
            "- BP1 accepted or waived.",
            "- BP2 prepared from accepted or waived BP1.",
            "- BP2 reviewed by USER.",
            "- BP2 accepted, revised, rejected, blocked, or waived by USER.",
            "- BP3 remains pending until BP2 closes.",
            "",
            "## Exact USER Decision Supported By The Current Packet",
            "",
            exact_user_decision,
            "",
            "## Pending USER Decisions",
            "",
            *_markdown_lines(pending_user_decisions),
            "",
        ]
        review_path = target / USER_BRANCH_PLAN_REVIEW_FILE
        review_path.write_text("\n".join(lines), encoding="utf-8")
        return review_path.resolve()
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
            "C:\\Nexus USER\\Governance and C:\\Nexus USER\\Governance__YYYYMMDD-HHMMSS.zip: temporary USER review aids.",
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
    is_fam006_active_overlay_implementation = (
        source_branch == FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH
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
    normalized_decision = exact_user_decision.casefold()
    fam006_bp3_packet = (
        is_fam006_active_overlay_implementation
        and (
            "bp3" in normalized_decision
            or "workstream entry" in normalized_decision
            or "orchestration validation" in normalized_decision
        )
    )
    fam006_bp2_packet = (
        is_fam006_active_overlay_implementation
        and (
            "bp2 user branch plan review" in normalized_decision
            or "bp2 branch plan" in normalized_decision
            or "accept the bp2" in normalized_decision
        )
        and not fam006_bp3_packet
    )
    packet_status = (
        "bp3 orchestration review - packet is reviewable for USER BP3 Workstream Entry / "
        "Orchestration Validation; BP3 USER acceptance, Workstream implementation, SLC-051, "
        "runtime mutation, recording execution, and file writing remain pending USER decisions."
        if fam006_bp3_packet
        else
        "bp2 branch plan review - packet is reviewable for USER BP2 plan review; "
        "BP2 USER acceptance, BP3, and Workstream implementation remain pending USER decisions."
        if fam006_bp2_packet
        else
        "bp1 branch vision review - packet is reviewable for USER BP1 review; "
        "BP1 USER acceptance, BP2, BP3, and Workstream implementation remain pending USER decisions."
        if is_fam006_active_overlay_implementation
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
    if fam006_bp3_packet:
        analysis_status = (
            "Analysis Summary: FAM-006 BP3 Workstream Entry / Orchestration Validation packet "
            "is reviewable; reviewability is not USER BP3 acceptance.\n\n"
            "## Accepted BP1 To Accepted BP2 Trace\n\n"
            "- PASS - accepted BP1 says active Overlay Profile membership is the recording target source.\n"
            "- PASS - accepted BP2 keeps snapshot-at-start as the future recording target model.\n"
            "- PASS - accepted BP2 keeps the HUD Overlay recording card low-redundancy and quick-access.\n"
            "- PASS - accepted BP2 keeps Recording Control as the richer target/readiness/status/control surface.\n"
            "- PASS - accepted BP2 rejects hidden recording target state and a separate Recording Profile system.\n\n"
            "## File Ownership Verification\n\n"
            "- `desktop/ui/dashboard_hud_panel.py`: NOT A CURRENT FILE - treat as stale/proposed path, not an implementation owner.\n"
            "- `desktop/desktop_renderer.py`: current Dashboard/HUD/Overlay Profile runtime owner; contains active Overlay Profile ID/name, membership signatures, HUD card/window runtime signals, and existing Overlay Profile proof chains.\n"
            "- `desktop/monitoring_hud_state.py`: current persisted/normalized Monitoring HUD state owner; owns `activeOverlayProfileId`, `overlayProfiles`, `monitorIds`, empty/default/deleted/stale active profile fallback, and monitor membership normalization.\n"
            "- `desktop/monitoring_hud_controls.py`: current HUD feature/dashboard control contract owner; useful for preserving Dashboard/HUD control boundaries.\n"
            "- `desktop/monitoring_hud_status.py`, `desktop/monitoring_hud_placement.py`, and `desktop/monitoring_hud_telemetry.py`: supporting FAM-006 HUD status, placement, and telemetry/source-truth surfaces that BP3 should keep bounded.\n"
            "- `dev/orin_monitoring_hud_surface_validation.py` and `dev/orin_monitoring_hud_internal_sandbox_validation.py`: current FAM-006 validation owners for HUD/Dashboard source truth and internal sandbox/state-boundary proof.\n"
            "- Proposed only after implementation approval: a future `desktop/recording_target_model.py` or equivalent target/session helper may be cleaner than adding recording-session state directly into the Dashboard renderer; Workstream must choose this inside approved scope.\n"
            "- Proposed only after later approval: `desktop/recording_control_window.py` for the standalone Recording Control surface.\n\n"
            "## SLC-051 First-Seam Recommendation\n\n"
            "Recommend SLC-051 Active Overlay recording target foundation as the first bounded Workstream seam after USER approves BP3 and then separately approves implementation. The first seam should prove target/session truth only: active Overlay Profile ID/name, membership snapshot candidate, null/empty/stale/deleted/missing profile behavior, high-volume membership behavior, and no hidden recording target state.\n\n"
            "## SLC-052 Pairing Assessment\n\n"
            "Do not pair SLC-052 by default. Pair only a minimal read-only HUD target preview with SLC-051 if implementation preflight proves the target proof cannot be inspected without a small HUD preview and the combined change still avoids Start/Stop, file writing, tray controls, export/share, Recording Control window work, and recording execution.\n\n"
            "## Implementation Order For SLC-051\n\n"
            "1. Verify the current owner for active Overlay Profile ID/name, membership, deleted/stale fallback, empty membership behavior, and monitor membership normalization.\n"
            "2. Add or adapt the smallest target/session model surface needed to represent the future recording target without starting recording execution.\n"
            "3. Prove snapshot-at-start candidate state, null/empty/stale/deleted/high-volume target states, and no hidden recording target state.\n"
            "4. Add only the minimum read-only HUD preview if BP3 and implementation approval agree it is inseparable from target proof.\n"
            "5. Stop before Recording Control window work, durable output/file-writing, real Start/Stop controls, tray controls, export/share, and recording execution unless USER separately approves those later seams.\n\n"
            "## BP3 Preflight Checks Before Implementation\n\n"
            "- Confirm BP1 and BP2 accepted receipts are present in the FAM-006 branch record and branch plan.\n"
            "- Confirm `desktop/ui/dashboard_hud_panel.py` is not treated as a current file owner.\n"
            "- Confirm the exact current owner for active Overlay Profile state before any SLC-051 code change.\n"
            "- Confirm the implementation approval prompt names the first seam and keeps runtime/file-writing boundaries blocked.\n"
            "- Confirm validators cover packet gate state, target/session state, HUD source truth, internal sandbox proof, rollback, H1, LV, and UTS expectations.\n\n"
            "## Proof Plan For SLC-051\n\n"
            "- Source-truth proof: accepted BP1/BP2 trace, owner-file verification, and branch-plan implementation constraints.\n"
            "- Runtime proof after separate implementation approval: active Overlay Profile ID/name, membership snapshot candidate, null/empty/stale/deleted/missing target behavior, high-volume membership behavior, and no hidden target state.\n"
            "- UI proof only if admitted: concise HUD target/status preview that avoids redundant current-overlay / recording-overlay text when intentionally identical.\n"
            "- Regression proof: Overlay Profile, Overlay Display, Monitor Groups, Sensor Command Center, Dashboard, and existing HUD behavior remain intact.\n\n"
            "## Drift Controls And Stop Conditions\n\n"
            "- Stop if implementation needs file writing, recording execution, Start/Stop controls, tray controls, export/share, provider/model work, Native Log Loader implementation, FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, or Governance mutation.\n"
            "- Stop if the target model starts to become a separate Recording Profile system or hidden target state.\n"
            "- Stop if actual file ownership contradicts this BP3 packet and route back to BP2/BP3 repair before implementation.\n"
            "- Stop if SLC-052 pairing would make the seam too broad or user-visible behavior too hard to prove.\n\n"
            "## Rollback, H1, Live Validation, And UTS Expectations\n\n"
            "- Rollback: disable or remove recording-specific target/session/HUD preview changes without corrupting Overlay Profile membership, Dashboard, Manage Monitors, Sensor Command Center, or existing overlay display behavior.\n"
            "- H1: pressure-test target states, stale/deleted/missing profiles, empty and high-volume memberships, compact HUD preview if admitted, and future-gated boundaries.\n"
            "- Live Validation: prove visible surfaces with real user-level interaction only after visible implementation exists.\n"
            "- UTS: ask USER to confirm target visibility, snapshot-at-start explanation, no hidden target state, no separate Recording Profile requirement, compact control usability when implemented, rollback posture, and any implemented output behavior.\n\n"
            "## Runtime And File-Writing Boundary\n\n"
            "Recording execution, file writing, real Start/Stop controls, tray controls, export/share, Native Log Loader implementation, provider/model work, and SLC-054 output-file creation remain blocked. SLC-054 may stay as output-contract planning only unless USER separately approves file writing or recording execution."
        )
        implementation_posture = (
            "Implementation Posture: BP3 can recommend a first Workstream seam, but this packet "
            "does not approve Workstream implementation, SLC-051 execution, runtime mutation, "
            "recording execution, file writing, Start/Stop controls, tray controls, export/share, "
            "provider/model work, FAM-007 mutation, PR creation, merge, release, issue mutation, "
            "cleanup, or Governance mutation."
        )
        recommended_seam = (
            "Recommended First Bounded Workstream Seam: SLC-051 Active Overlay recording target "
            "foundation only, with SLC-052 minimal HUD preview excluded unless inseparability is "
            "proved during the separate implementation approval path."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, phase governance, branch-plan "
            "artifact rules, execution mirrors, governance efficiency model, validation helper registry, "
            "incident patterns, FAM-006 family vision, active FAM-006 branch record and plan, backlog, "
            "roadmap, worktree routing, and current HUD/Overlay Profile owner evidence needed for BP3 review."
        )
        checklist_status = (
            "Checklist Focus: for FAM-006 BP3 review - accepted BP1/BP2 trace, actual file ownership, "
            "SLC-051 first-seam recommendation, SLC-052 pairing restraint, snapshot-at-start, "
            "low-redundancy HUD card rule, richer Recording Control boundary, no-hidden-target rule, "
            "SLC-054 output-contract-only boundary, validators, rollback, H1, LV, and UTS expectations."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER Review/WORKSTREAM_ENTRY_ANALYSIS_DIGEST.md, "
            "accepted BP1/BP2 context in Review Aids, and Source Truth Context files are loaded for "
            "BP3 Workstream Entry / Orchestration Validation. BP3 USER Gate State remains Pending USER Review."
        )
    elif fam006_bp2_packet:
        analysis_status = (
            "Analysis Summary: FAM-006 BP2 USER Branch Plan Review packet is reviewable; "
            "reviewability is not USER acceptance."
        )
        implementation_posture = (
            "Implementation Posture: runtime implementation, SLC-051, recording execution, "
            "file writing, Start/Stop controls, tray controls, export/share, provider/model work, "
            "FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance "
            "mutation remain blocked pending later USER decisions."
        )
        recommended_seam = (
            "Recommended Next Phase: BP2 USER response for the FAM-006 Active Overlay Recording "
            "Runtime Implementation branch plan."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, phase governance, branch-plan "
            "artifact rules, execution mirrors, governance efficiency model, validation helper registry, "
            "incident patterns, FAM-006 family vision, active FAM-006 branch record and plan, backlog, "
            "roadmap, and worktree routing needed for BP2 review."
        )
        checklist_status = (
            "Checklist Focus: for FAM-006 BP2 review - accepted BP1 trace, active-overlay-driven "
            "recording identity, snapshot-at-start target model, HUD Overlay launcher/target preview, "
            "compact standalone Recording Control window plan, SLC-051 through SLC-055 route, H1/LV/UTS "
            "proof expectations, BP2/BP3 separation, and runtime implementation blockers are represented "
            "for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER Review/USER_BRANCH_PLAN_REVIEW.md, Review Aids, "
            "and Source Truth Context files are loaded for BP2 USER Branch Plan Review. BP2 USER "
            "Gate State remains Pending USER Review."
        )
    elif is_fam006_active_overlay_implementation:
        analysis_status = (
            "Analysis Summary: FAM-006 BP1 USER Branch Vision Review packet is reviewable; "
            "reviewability is not USER acceptance."
        )
        implementation_posture = (
            "Implementation Posture: runtime implementation, SLC-051, recording execution, "
            "file writing, Start/Stop controls, tray controls, export/share, provider/model work, "
            "FAM-007 mutation, PR creation, merge, release, issue mutation, cleanup, and Governance "
            "mutation remain blocked pending later USER decisions."
        )
        recommended_seam = (
            "Recommended Next Phase: BP1 USER response for the FAM-006 Active Overlay Recording "
            "Runtime Implementation branch vision."
        )
        scan_result = (
            "Source-Truth Coverage: packet includes the Main router, phase governance, branch-plan "
            "artifact rules, execution mirrors, governance efficiency model, validation helper registry, "
            "incident patterns, FAM-006 family vision, active FAM-006 branch record and plan, backlog, "
            "roadmap, and worktree routing needed for BP1 review."
        )
        checklist_status = (
            "Checklist Focus: for FAM-006 BP1 review - active-overlay-driven recording identity, "
            "active Overlay Profile target source, HUD Overlay launcher/target preview, compact "
            "standalone Recording Control window direction, Native Log Loader future boundary, "
            "per-overlay polling-policy future constraint, BP1/BP2/BP3 separation, and runtime "
            "implementation blockers are represented for USER inspection."
        )
        digest_status = (
            "Review Summary: START_HERE.md, USER Review/USER_BRANCH_VISION_REVIEW.md, Review Aids, "
            "and Source Truth Context files are loaded for BP1 USER Branch Vision Review. BP1 USER "
            "Gate State remains Pending USER Review."
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
    gate_state_context = (
        "Packet Reviewability State: Reviewable\n"
        "USER Gate State: Pending USER Review\n"
        if is_fam006_active_overlay_implementation
        else ""
    )
    common = (
        f"Decision Path: {packet_status}\n"
        f"{gate_state_context}"
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
    decision_path_match = re.search(
        r"decision path summary:\s*(.+?)(?:\s+user decision:|\s+##|\Z)",
        normalized,
    )
    if decision_path_match:
        decision_path = decision_path_match.group(1)
        if "bp2 branch plan review" in decision_path:
            return DECISION_STATUS_BP2_BRANCH_PLAN_REVIEW
        if "bp1 branch vision review" in decision_path:
            return DECISION_STATUS_BP1_BRANCH_VISION_REVIEW
        if "bp3 orchestration" in decision_path or "workstream entry / orchestration" in decision_path:
            return DECISION_STATUS_BP3_ORCHESTRATION_REVIEW
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
        if any(marker in normalized for marker in bp1_markers):
            return DECISION_STATUS_BP1_BRANCH_VISION_REVIEW
        if any(marker in normalized for marker in bp2_markers):
            return DECISION_STATUS_BP2_BRANCH_PLAN_REVIEW
        if any(marker in normalized for marker in bp3_markers):
            return DECISION_STATUS_BP3_ORCHESTRATION_REVIEW

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
    failures.extend(_structured_user_review_packet_layout_failures(packet_files))
    failures.extend(_user_facing_technical_metadata_failures(packet_files))
    failures.extend(_bp2_accepted_bp1_support_file_failures(packet_files))
    failures.extend(_fam006_bp3_support_file_failures(packet_files))
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
    timestamped_upload_zip: bool = True,
) -> tuple[Path, Path, Path | None]:
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
    _clear_matching_export_zips(review_root, label)
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
    export_zip = _timestamped_export_zip_path(review_root, label, created_at_dt)
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
    normalized_decision = exact_user_decision.casefold()
    fam006_bp3_packet = (
        source_branch == FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH
        and (
            "bp3" in normalized_decision
            or "workstream entry" in normalized_decision
            or "orchestration validation" in normalized_decision
        )
    )
    fam006_bp2_packet = (
        source_branch == FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH
        and (
            "bp2 user branch plan review" in normalized_decision
            or "bp2 branch plan" in normalized_decision
            or "accept the bp2" in normalized_decision
        )
        and not fam006_bp3_packet
    )
    fam006_bp1_packet = (
        source_branch == FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH
        and not fam006_bp2_packet
        and not fam006_bp3_packet
    )
    machine_readable_packet_status = (
        "bp3 orchestration review - packet is reviewable for USER BP3 Workstream Entry / "
        "Orchestration Validation; BP3 USER acceptance, Workstream implementation, SLC-051, "
        "runtime mutation, recording execution, and file writing remain pending USER decisions."
        if fam006_bp3_packet
        else
        "bp2 branch plan review - packet is reviewable for USER BP2 plan review; "
        "BP2 USER acceptance, BP3, and Workstream implementation remain pending USER decisions."
        if fam006_bp2_packet
        else
        "bp1 branch vision review - packet is reviewable for USER BP1 review; "
        "BP1 USER acceptance, BP2, BP3, and Workstream implementation remain pending USER decisions."
        if fam006_bp1_packet
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
        "Review Location: Open this folder in the local USER hub and upload the matching ZIP beside it.",
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
        *(
            [
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Review",
            ]
            if source_branch == FAM006_ACTIVE_OVERLAY_IMPLEMENTATION_BRANCH
            else []
        ),
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
        *_structured_user_review_packet_layout_failures(packet_files),
        *_user_facing_technical_metadata_failures(packet_files),
        *_user_branch_plan_stale_bp1_wording_failures(packet_files),
        *_fam006_bp1_generated_stale_failures(packet_files),
        *_bp2_accepted_bp1_support_file_failures(packet_files),
        *_fam006_bp3_support_file_failures(packet_files),
        *_user_branch_vision_substantive_failures(packet_files),
        *_branch_planning_review_gate_state_failures(packet_files),
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
    timestamped_zip = export_zip if timestamped_upload_zip else None
    return target, export_zip, timestamped_zip


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
        "--timestamped-upload-zip",
        action="store_true",
        help=(
            "Deprecated compatibility flag. The helper always creates a single "
            "timestamped upload ZIP named <worktree-label>__YYYYMMDD-HHMMSS.zip "
            "for USER-approved upload collision avoidance."
        ),
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

    target, export_zip, timestamped_zip = build_bundle(
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
        timestamped_upload_zip=True,
    )
    print(f"Review bundle: {target}")
    upload_zip = timestamped_zip or export_zip
    print(f"Timestamped upload zip: {upload_zip}")
    print(f"Timestamped upload zip SHA256: {_sha256_file(upload_zip)}")
    print(
        "USER Review Packet Finding: PASS - START_HERE.md, "
        f"{USER_BRANCH_VISION_REVIEW_FILE}, {USER_BRANCH_PLAN_REVIEW_FILE}, and exported zip were generated and "
        "validated against current source-truth snapshot."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
