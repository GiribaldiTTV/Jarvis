from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SCAN_PATHS = (
    Path("Docs/Main.md"),
    Path("Docs/branch_records/index.md"),
    Path("Docs/branch_records"),
    Path("Docs/branch_plans"),
    Path("Docs/feature_backlog.md"),
    Path("Docs/prebeta_roadmap.md"),
    Path("Docs/worktree_slots.md"),
    Path("Docs/workstreams"),
    Path("Docs/governance_efficiency_operating_model.md"),
    Path("Docs/external_operational_state_store_reform_plan.md"),
)

RULE_SURFACES = {
    Path("Docs/Main.md"),
    Path("Docs/phase_governance.md"),
    Path("Docs/governance_efficiency_operating_model.md"),
    Path("Docs/external_operational_state_store_reform_plan.md"),
    Path("Docs/branch_plans/README.md"),
    Path("Docs/branch_plans/retirement_index.md"),
    Path("Docs/validation_helper_registry.md"),
}

LIVE_STATE_PATTERNS = {
    "active-branch-state": re.compile(
        r"\b(Active Branch Authority|Active Branch|Branch Authority State|Current Phase|Phase Status|"
        r"Active RRI Cycle|Intake State|Return Digest Status)\b",
        re.IGNORECASE,
    ),
    "worktree-assignment": re.compile(
        r"\b(Assignment Status|Assigned Branch|Active Thread Owner|Thread Assignment Status|"
        r"Intended Write Set|Dirty Worktree|Same Worktree|GitHub Desktop-bound worktree)\b",
        re.IGNORECASE,
    ),
    "pr-state": re.compile(
        r"\b(Live PR State|No live PR|PR creation pending|PR Creation Approval|"
        r"PR Readiness Stage 1 Ready For Stage 2|PR Readiness Stage 2|review-thread|"
        r"mergeability|watcher)\b",
        re.IGNORECASE,
    ),
    "release-window": re.compile(
        r"\b(Latest Public Prerelease|Latest Public Release|Release Candidate Anchor|"
        r"Release Window|Merged-Unreleased|Target Commit|release-window)\b",
        re.IGNORECASE,
    ),
    "selected-next": re.compile(
        r"\b(Selected Next Workstream|Selected Next Implementation Branch|Selection Truth Status|"
        r"selected-next|Next Workstream)\b",
        re.IGNORECASE,
    ),
    "derived-git-truth": re.compile(
        r"\b(origin/main|HEAD|merge base|ahead|behind|dirty|clean|git status|git rev-parse)\b",
        re.IGNORECASE,
    ),
}

HISTORICAL_RECEIPT_WORDS = (
    "historical",
    "receipt",
    "retired",
    "released",
    "merged",
    "fold-down",
    "folded",
    "preserved",
    "evidence",
)

BLOCKING_PHRASES = (
    "No live PR",
    "PR creation pending",
    "PR Creation Approval: Pending",
    "Stage 2 PR Creation: Pending",
    "PR Readiness Stage 1 Ready For Stage 2",
)

TARGET_OWNER_BY_CATEGORY = {
    "active-branch-state": "C:\\Nexus Governance State\\branches\\<branch_slug>\\branch_state.md",
    "worktree-assignment": "C:\\Nexus Governance State\\worktrees\\<worktree_label>\\worktree_state.md",
    "pr-state": "Git/GitHub/helpers for live facts; external branch PR-readiness state for operational snapshots",
    "release-window": "Git/GitHub/helpers for live release facts; C:\\Nexus Governance State\\release_windows\\<release_slug>\\release_window_state.md for assembly",
    "selected-next": "C:\\Nexus Governance State\\central\\selected_next_state.md or branch/family planning state after migration",
    "derived-git-truth": "Git/GitHub/helpers",
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    category: str
    classification: str
    target_owner: str
    reason: str
    excerpt: str


def repo_relative(path: Path, repo: Path) -> Path:
    try:
        return path.relative_to(repo)
    except ValueError:
        return path


def collect_scan_files(repo: Path, paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for relative_path in paths:
        path = repo / relative_path
        if path.is_dir():
            files.extend(sorted(child for child in path.rglob("*.md") if child.is_file()))
        elif path.is_file():
            files.append(path)
    return sorted(set(files))


def load_retired_branch_plans(repo: Path) -> set[Path]:
    retirement_index = repo / "Docs" / "branch_plans" / "retirement_index.md"
    if not retirement_index.exists():
        return set()
    retired: set[Path] = set()
    pattern = re.compile(r"`(Docs/branch_plans/[^`]+\.md)`")
    for match in pattern.finditer(retirement_index.read_text(encoding="utf-8")):
        retired.add(Path(match.group(1)))
    return retired


def load_branch_record_posture(repo: Path) -> tuple[set[Path], set[Path]]:
    index = repo / "Docs" / "branch_records" / "index.md"
    if not index.exists():
        return set(), set()

    active: set[Path] = set()
    historical: set[Path] = set()
    section = ""
    pattern = re.compile(r"`(Docs/branch_records/[^`]+\.md)`")
    for line in index.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            if "Active Branch Authority Records" in stripped:
                section = "active"
            elif "Historical Branch Authority Records" in stripped:
                section = "historical"
            elif stripped.startswith("## "):
                section = ""
        for match in pattern.finditer(line):
            path = Path(match.group(1))
            if section == "active":
                active.add(path)
            elif section == "historical":
                historical.add(path)
    return active, historical


def has_historical_context(lines: list[str], index: int) -> bool:
    start = max(0, index - 2)
    end = min(len(lines), index + 3)
    window = " ".join(lines[start:end]).lower()
    return any(word in window for word in HISTORICAL_RECEIPT_WORDS)


def classify_finding(
    relative_path: Path,
    line: str,
    category: str,
    historical: bool,
    retired_plans: set[Path],
    active_branch_records: set[Path],
    historical_branch_records: set[Path],
) -> tuple[str, str]:
    normalized = relative_path.as_posix()

    if relative_path in RULE_SURFACES:
        return "Durable Rule Reference", "binding governance/source-truth rule surface"

    if relative_path in historical_branch_records:
        return "Durable Historical Receipt", "branch record is listed as historical in Docs/branch_records/index.md"

    if relative_path in active_branch_records:
        return "Transition-Legal Current Owner", "active branch record remains legal until external migration is approved"

    if normalized.startswith("Docs/branch_plans/") and relative_path in retired_plans:
        return "Durable Historical Receipt", "branch plan is listed in retirement index"

    if historical:
        return "Durable Historical Receipt", "nearby text labels the fact as historical/released/retired/receipt evidence"

    if relative_path in {Path("Docs/feature_backlog.md"), Path("Docs/prebeta_roadmap.md")}:
        if category in {"selected-next", "release-window", "pr-state", "active-branch-state"}:
            return "Migration Candidate", "compact pointer surface should not own current operational posture after migration"

    if relative_path == Path("Docs/worktree_slots.md") and category == "worktree-assignment":
        return "Migration Candidate", "stable slot definitions stay repo; active assignment state migrates external"

    if normalized.startswith("Docs/branch_records/") or normalized.startswith("Docs/branch_plans/"):
        return "Migration Candidate", "active branch authority/planning state migrates external after USER-approved migration"

    if normalized.startswith("Docs/workstreams/"):
        return "Migration Candidate", "workstream routing stays durable; live watcher/PR/release-window state should be external or derived"

    return "Review Candidate", "manual review needed to confirm durable receipt versus live operational tracker"


def scan_file(
    path: Path,
    repo: Path,
    retired_plans: set[Path],
    active_branch_records: set[Path],
    historical_branch_records: set[Path],
) -> list[Finding]:
    relative_path = repo_relative(path, repo)
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[Finding] = []

    for index, line in enumerate(lines):
        for category, pattern in LIVE_STATE_PATTERNS.items():
            if not pattern.search(line):
                continue
            historical = has_historical_context(lines, index)
            classification, reason = classify_finding(
                relative_path,
                line,
                category,
                historical,
                retired_plans,
                active_branch_records,
                historical_branch_records,
            )
            normalized_line = line.casefold()
            if (
                any(phrase.casefold() in normalized_line for phrase in BLOCKING_PHRASES)
                and classification == "Migration Candidate"
            ):
                classification = "Repo Live-State Leakage"
                reason = "stale live PR/PR-readiness wording in a repo operational tracker surface"
            findings.append(
                Finding(
                    path=relative_path,
                    line=index + 1,
                    category=category,
                    classification=classification,
                    target_owner=TARGET_OWNER_BY_CATEGORY[category],
                    reason=reason,
                    excerpt=line.strip().lstrip("\ufeff"),
                )
            )
    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report repo live-state leakage and migration-map candidates for the External Governance State reform."
    )
    parser.add_argument("--repo", default=str(ROOT), help="Repository root to scan.")
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Repo-relative file or directory to scan. Defaults to the known live-state risk surfaces.",
    )
    parser.add_argument("--max-findings", type=int, default=160, help="Maximum line-level findings to print.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when Repo Live-State Leakage findings are present.",
    )
    return parser


def print_summary(findings: list[Finding]) -> None:
    by_class: dict[str, int] = {}
    by_file: dict[Path, int] = {}
    for finding in findings:
        by_class[finding.classification] = by_class.get(finding.classification, 0) + 1
        by_file[finding.path] = by_file.get(finding.path, 0) + 1

    print("Classification Summary:")
    for classification, count in sorted(by_class.items()):
        print(f"- {classification}: {count}")

    print("Surface Summary:")
    for path, count in sorted(by_file.items(), key=lambda item: item[0].as_posix()):
        print(f"- {path.as_posix()}: {count}")


def print_migration_map() -> None:
    print("Migration Map:")
    print("- active branch state -> C:\\Nexus Governance State\\branches\\<branch_slug>\\branch_state.md")
    print("- active branch plans -> C:\\Nexus Governance State\\branches\\<branch_slug>\\branch_plan.md")
    print("- UFD / change-intent / element matrix while active -> C:\\Nexus Governance State\\branches\\<branch_slug>\\")
    print("- current worktree assignment -> C:\\Nexus Governance State\\worktrees\\<worktree_label>\\worktree_state.md")
    print("- release-window assembly -> C:\\Nexus Governance State\\release_windows\\<release_slug>\\release_window_state.md")
    print("- live PR/review truth -> Git/GitHub/helpers; optional external operational snapshot under branch PR state")
    print("- selected-next operational posture -> external central or branch/family planning state after migration")
    print("- durable product/governance/release interpretation -> repo Docs historical receipts after USER-approved fold-down")


def finding_sort_key(finding: Finding) -> tuple[int, str, int, str]:
    priority = {
        "Repo Live-State Leakage": 0,
        "Migration Candidate": 1,
        "Transition-Legal Current Owner": 2,
        "Review Candidate": 3,
        "Durable Historical Receipt": 4,
        "Durable Rule Reference": 5,
    }.get(finding.classification, 9)
    return (priority, finding.path.as_posix(), finding.line, finding.category)


def main() -> int:
    args = build_parser().parse_args()
    repo = Path(args.repo).expanduser().resolve(strict=False)
    if not repo.is_dir():
        print(f"ERROR: repo root does not exist or is not a directory: {repo}", file=sys.stderr)
        return 2

    scan_paths = [Path(path) for path in args.path] if args.path else list(DEFAULT_SCAN_PATHS)
    files = collect_scan_files(repo, scan_paths)
    if not files:
        requested_paths = ", ".join(path.as_posix() for path in scan_paths)
        print(
            "ERROR: repo live-state scan found no files; check --repo and --path values. "
            f"Requested paths: {requested_paths}",
            file=sys.stderr,
        )
        return 2

    retired_plans = load_retired_branch_plans(repo)
    active_branch_records, historical_branch_records = load_branch_record_posture(repo)
    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(path, repo, retired_plans, active_branch_records, historical_branch_records))

    blockers = [finding for finding in findings if finding.classification == "Repo Live-State Leakage"]

    print("Repo Live-State Leakage Scan")
    print(f"Repo: {repo}")
    print("Mutation Status: Not started - report only")
    print(f"Scanned Files: {len(files)}")
    print(f"Findings: {len(findings)}")
    print(f"Blocking Leakage Findings: {len(blockers)}")
    print("Repo Live-State Leakage Scan Result: " + ("BLOCKED" if blockers else "CLEAR / MIGRATION CANDIDATES ONLY"))
    print()
    print_summary(findings)
    print()
    print_migration_map()
    print()
    print("Line Findings:")
    ordered_findings = sorted(findings, key=finding_sort_key)
    for finding in ordered_findings[: args.max_findings]:
        print(
            f"- {finding.path.as_posix()}:{finding.line} | {finding.classification} | "
            f"{finding.category} | target: {finding.target_owner} | {finding.reason} | {finding.excerpt}"
        )
    if len(findings) > args.max_findings:
        remaining = len(findings) - args.max_findings
        print(f"- ... {remaining} additional findings omitted by --max-findings")

    return 1 if args.strict and blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
