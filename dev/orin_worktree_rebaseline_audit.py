# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=GOV-SOURCE-TRUTH; ledger=SRCOWN-CLEANUP-REBINDING-013; surface=worktree-rebaseline-audit-helper; status=shared
"""Report-only Pre-Rebaseline Impact Audit for Nexus worktrees.

This helper intentionally performs no fetch, merge, rebase, checkout, or file
mutation. It turns the repo-wide pre-rebaseline governance contract into a
consistent packet that can be pasted into a USER decision before any worktree
baselines itself to a newer origin/main.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path


KNOWN_WORKTREE_ROLES = {
    "C:/Nexus Desktop AI": "neutral main workspace",
    "C:/Nexus Worktrees/Governance": "standing governance intake",
    "C:/Nexus Worktrees/FAM-006": "FAM-006 implementation lane",
    "C:/Nexus Worktrees/FAM-007": "FAM-007 implementation lane",
}

SHARED_SOURCE_TRUTH_PREFIXES = (
    "Docs/",
    "dev/",
)
RUNTIME_PREFIXES = (
    "Audio/",
    "Core/",
    "desktop/",
    "main.py",
    "nexus_visual/",
)
HIGH_RISK_SOURCE_TRUTH_FILES = {
    "Docs/feature_backlog.md",
    "Docs/prebeta_roadmap.md",
    "Docs/branch_records/index.md",
    "Docs/phase_governance.md",
    "Docs/development_rules.md",
    "Docs/codex_modes.md",
    "Docs/orin_task_template.md",
    "Docs/validation_helper_registry.md",
}

HIGH_RISK_SURFACE_CLASSES = {
    "governance/source-truth",
    "runtime",
    "desktop/UI",
    "Core visual",
    "validator/helper",
    "fixture/test",
    "configuration/state/schema",
    "release/public-output",
    "prompt/template",
    "automation/watcher",
    "build/packaging",
}


def _run_git(args: list[str], cwd: Path, *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def _git_output(args: list[str], cwd: Path, default: str = "") -> str:
    result = _run_git(args, cwd)
    if result.returncode != 0:
        return default
    return result.stdout.strip()


def _git_lines(args: list[str], cwd: Path) -> list[str]:
    output = _git_output(args, cwd)
    if not output:
        return []
    return [line.rstrip() for line in output.splitlines() if line.strip()]


def _status_path(line: str) -> str:
    if len(line) >= 4 and line[2] == " ":
        return line[3:].replace("\\", "/")
    parts = line.split(maxsplit=1)
    if len(parts) == 2:
        return parts[1].replace("\\", "/")
    return line.replace("\\", "/")


def _normalize_path(path: str | Path) -> str:
    return Path(path).resolve().as_posix()


def _worktree_role(root: Path) -> str:
    normalized = _normalize_path(root)
    for known_path, role in KNOWN_WORKTREE_ROLES.items():
        if normalized.casefold() == Path(known_path).resolve().as_posix().casefold():
            return role
    return "unregistered worktree"


def _branch() -> str:
    return _git_output(["branch", "--show-current"], Path.cwd(), "detached HEAD")


def _top_level(cwd: Path) -> Path:
    output = _git_output(["rev-parse", "--show-toplevel"], cwd)
    if not output:
        raise SystemExit(f"Not a git worktree: {cwd}")
    return Path(output)


def _is_ancestor(cwd: Path, ancestor: str, descendant: str) -> bool | None:
    if not ancestor or not descendant:
        return None
    result = _run_git(["merge-base", "--is-ancestor", ancestor, descendant], cwd)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def _classify_files(files: list[str]) -> tuple[list[str], list[str], list[str]]:
    source_truth: list[str] = []
    runtime: list[str] = []
    high_risk: list[str] = []
    for file_name in files:
        normalized = file_name.replace("\\", "/")
        if normalized in HIGH_RISK_SOURCE_TRUTH_FILES:
            high_risk.append(normalized)
        if normalized.startswith(SHARED_SOURCE_TRUTH_PREFIXES):
            source_truth.append(normalized)
        if normalized == "main.py" or normalized.startswith(RUNTIME_PREFIXES):
            runtime.append(normalized)
    return sorted(set(source_truth)), sorted(set(runtime)), sorted(set(high_risk))


def _surface_class(file_name: str) -> str:
    normalized = file_name.replace("\\", "/")
    if normalized.startswith(("Docs/branch_records/", "Docs/branch_plans/")):
        return "governance/source-truth"
    if normalized.startswith("Docs/") and normalized.endswith((".md", ".txt")):
        if normalized in {
            "Docs/orin_task_template.md",
            "Docs/nexus_startup_contract.md",
            "Docs/codex_user_guide.md",
            "Docs/codex_modes.md",
        }:
            return "prompt/template"
        if normalized in HIGH_RISK_SOURCE_TRUTH_FILES:
            return "governance/source-truth"
        return "documentation/reference"
    if normalized.startswith("dev/fixtures/"):
        return "fixture/test"
    if normalized.startswith("dev/") or normalized.endswith((".ps1", ".bat", ".cmd")):
        return "validator/helper"
    if normalized.startswith("desktop/"):
        return "desktop/UI"
    if normalized.startswith("Core/"):
        return "Core visual"
    if normalized == "main.py" or normalized.startswith(("Audio/", "nexus_visual/")):
        return "runtime"
    if normalized.startswith((".github/", "scripts/")):
        return "automation/watcher"
    if normalized.endswith((".json", ".toml", ".yaml", ".yml", ".ini")):
        return "configuration/state/schema"
    if normalized.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".mp4", ".wav")):
        return "asset/media"
    return "documentation/reference"


def _overlap_file_result(file_name: str) -> str:
    surface_class = _surface_class(file_name)
    if surface_class in HIGH_RISK_SURFACE_CLASSES:
        return "BLOCKED"
    return "WARN"


def _overall_overlap_gate_result(overlap_files: list[str]) -> str:
    if not overlap_files:
        return "Not Applicable"
    if any(_overlap_file_result(file_name) == "BLOCKED" for file_name in overlap_files):
        return "BLOCKED"
    return "WARN"


def _overlap_detail_lines(overlap_files: list[str]) -> list[str]:
    if not overlap_files:
        return ["- None"]
    lines: list[str] = []
    for file_name in overlap_files:
        surface_class = _surface_class(file_name)
        per_file_result = _overlap_file_result(file_name)
        lines.extend(
            [
                f"- File: `{file_name}`",
                f"  - Surface Class: `{surface_class}`",
                "  - Incoming Change Summary: `Review incoming diff from merge_base..target_ref`",
                "  - Current Branch Change Summary: `Review branch/worktree diff from merge_base..HEAD plus dirty files`",
                "  - Branch Change Intent Present: `Review active Branch Change Intent Ledger`",
                "  - Incoming Intent Evidence Present: `Review branch record, PR body, commit messages, source-owner markers, helper registry, fixtures, or workstream/family dossier`",
                "  - Fallback Evidence: `Available for classification only; not a compatibility bypass`",
                f"  - Risk: `{'High-risk surface requires intent evidence' if per_file_result == 'BLOCKED' else 'Lower-risk overlap requires USER-visible recommendation'}`",
                f"  - Per-File Result: `{per_file_result}`",
                "  - Recommended Resolution: `Inspect intent evidence before mutation`",
                "  - Resolution Owner: `USER Decision until branch-owned intent evidence is proven`",
                "  - Validation Required: `Run phase-required validation after any overlap-intent repair and before mutation`",
                "  - USER Decision Needed: `Approve repair/waiver/defer/sequencing before rebaseline mutation`",
            ]
        )
    return lines


def _worktree_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in _git_lines(["worktree", "list", "--porcelain"], root):
        if line.startswith("worktree "):
            rows.append({"path": line.removeprefix("worktree ").strip()})
        elif rows and line.startswith("HEAD "):
            rows[-1]["head"] = line.removeprefix("HEAD ").strip()
        elif rows and line.startswith("branch "):
            rows[-1]["branch"] = line.removeprefix("branch ").strip().removeprefix("refs/heads/")
        elif rows and line == "detached":
            rows[-1]["branch"] = "detached HEAD"
    return rows


def _dirty_files_for_worktree(path: str) -> list[str]:
    worktree = Path(path)
    if not worktree.exists():
        return []
    return [
        _status_path(line)
        for line in _git_lines(["status", "--short"], worktree)
        if line.strip()
    ]


def _active_authority_record(root: Path, branch: str) -> str:
    index_path = root / "Docs" / "branch_records" / "index.md"
    if not index_path.is_file() or not branch:
        return "Unknown - branch record index missing or branch unknown"
    index_text = index_path.read_text(encoding="utf-8", errors="replace")
    active_section = index_text.split("## Active Branch Authority Records", 1)
    if len(active_section) < 2:
        return "Unknown - active authority section missing"
    active_text = active_section[1].split("## Historical Branch Authority Records", 1)[0]
    candidates = []
    for line in active_text.splitlines():
        if "Docs/branch_records/" in line and ".md" in line:
            start = line.find("Docs/branch_records/")
            end = line.find(".md", start) + len(".md")
            candidates.append(line[start:end])
    for candidate in candidates:
        record_path = root / candidate
        if not record_path.is_file():
            continue
        record_text = record_path.read_text(encoding="utf-8", errors="replace")
        branch_match = re.search(r"(?m)^\s*-\s*Branch:\s*`?([^`\r\n]+)`?\s*$", record_text)
        if branch_match and branch_match.group(1).strip() == branch:
            return candidate
    return "None matched current branch"


def _valid_ref(value: str) -> bool:
    return bool(value and value != "Unknown")


def _recommendation(
    *,
    status_lines: list[str],
    head: str,
    target_sha: str,
    target_is_descendant: bool | None,
    head_is_descendant: bool | None,
    incoming_files: list[str],
    high_risk_files: list[str],
    runtime_files: list[str],
) -> tuple[str, str]:
    if status_lines:
        return (
            "Blocked",
            "Worktree has local changes; do not baseline until the owner reviews or commits/stashes them.",
        )
    if not target_sha:
        return ("Blocked", "Target ref could not be resolved.")
    if head == target_sha:
        return ("No-op", "Current HEAD already matches target ref; no rebaseline is needed.")
    if target_is_descendant:
        if high_risk_files or runtime_files:
            return (
                "USER decision required",
                "Fast-forward appears possible, but incoming changes touch runtime or high-risk source-truth surfaces.",
            )
        return (
            "USER approval required",
            "Fast-forward appears possible; mutation still requires explicit USER approval.",
        )
    if head_is_descendant:
        return (
            "No incoming target changes",
            "Current branch is ahead of target; do not reset or rewrite without a separate USER decision.",
        )
    if incoming_files:
        return (
            "Reconciliation required",
            "Branch and target have diverged; inspect conflicts/overlap before any merge or rebase.",
        )
    return ("Review required", "Could not prove a safe rebaseline posture.")


def build_report(cwd: Path, target_ref: str) -> str:
    root = _top_level(cwd)
    branch = _git_output(["branch", "--show-current"], root, "detached HEAD")
    upstream = _git_output(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], root, "None")
    head = _git_output(["rev-parse", "HEAD"], root)
    target_sha = _git_output(["rev-parse", target_ref], root)
    merge_base = _git_output(["merge-base", "HEAD", target_ref], root, "Unknown")
    status_lines = _git_lines(["status", "--short"], root)
    current_changed_files = [
        _status_path(line)
        for line in status_lines
        if line.strip()
    ]
    incoming_commits = _git_lines(["log", "--oneline", f"HEAD..{target_ref}"], root)
    ahead_commits = _git_lines(["log", "--oneline", f"{target_ref}..HEAD"], root)
    if _valid_ref(merge_base):
        incoming_files = _git_lines(["diff", "--name-only", f"{merge_base}..{target_ref}"], root)
        branch_files = _git_lines(["diff", "--name-only", f"{merge_base}..HEAD"], root)
    else:
        incoming_files = _git_lines(["diff", "--name-only", f"HEAD..{target_ref}"], root)
        branch_files = _git_lines(["diff", "--name-only", f"{target_ref}..HEAD"], root)
    current_branch_worktree_files = sorted(set(branch_files).union(current_changed_files))
    rebaseline_overlap_files = sorted(set(incoming_files).intersection(current_branch_worktree_files))
    source_truth_files, runtime_files, high_risk_files = _classify_files(incoming_files)
    target_is_descendant = _is_ancestor(root, head, target_sha)
    head_is_descendant = _is_ancestor(root, target_sha, head)
    recommendation_state, recommendation = _recommendation(
        status_lines=status_lines,
        head=head,
        target_sha=target_sha,
        target_is_descendant=target_is_descendant,
        head_is_descendant=head_is_descendant,
        incoming_files=incoming_files,
        high_risk_files=high_risk_files,
        runtime_files=runtime_files,
    )
    overlap_gate_result = _overall_overlap_gate_result(rebaseline_overlap_files)
    if overlap_gate_result == "BLOCKED":
        recommendation_state = "Blocked"
        recommendation = (
            "Rebaseline Overlap Intent Gate found high-risk overlapping files; "
            "inspect Branch Change Intent Ledger evidence before mutation."
        )
    elif overlap_gate_result == "WARN":
        recommendation_state = "USER decision required"
        recommendation = (
            "Rebaseline Overlap Intent Gate found lower-risk overlapping files; "
            "return the overlap packet and get USER approval before mutation."
        )
    sibling_rows = []
    overlap_files: set[str] = set()
    incoming_set = set(incoming_files)
    for row in _worktree_rows(root):
        path = row.get("path", "")
        if not path or _normalize_path(path).casefold() == _normalize_path(root).casefold():
            continue
        dirty_files = _dirty_files_for_worktree(path)
        overlap = sorted(incoming_set.intersection(dirty_files))
        overlap_files.update(overlap)
        sibling_rows.append(
            f"- {path} | branch: {row.get('branch', 'unknown')} | HEAD: {row.get('head', 'unknown')[:12]} | dirty files: {len(dirty_files)} | incoming overlap: {', '.join(overlap) if overlap else 'None'}"
        )
    source_truth_risk = []
    if source_truth_files:
        source_truth_risk.append(f"source-truth/dev files touched: {', '.join(source_truth_files[:20])}")
    if runtime_files:
        source_truth_risk.append(f"runtime/UI files touched: {', '.join(runtime_files[:20])}")
    if high_risk_files:
        source_truth_risk.append(f"high-risk current-state files touched: {', '.join(high_risk_files)}")
    if not source_truth_risk:
        source_truth_risk.append("No incoming runtime/source-truth files detected by static path classification.")
    identity_guard = [
        f"Assigned Worktree Branch Identity: `{branch}` in `{root}`",
        f"Branch-Local Authority Reassertion: `{_active_authority_record(root, branch)}`",
        "Incoming Main Active-Branch Blocks Accepted: NO - audit is report-only and performs no conflict resolution.",
        "Sibling Worktree Identity Preservation: No sibling worktree is switched, deleted, merged, rebased, or mutated by this helper.",
    ]
    lines = [
        "Pre-Rebaseline Impact Audit:",
        f"- Current Workspace: `{cwd}`",
        f"- Git Root: `{root}`",
        f"- Worktree Role: `{_worktree_role(root)}`",
        f"- Current Branch: `{branch}`",
        f"- Upstream: `{upstream}`",
        f"- HEAD: `{head or 'unknown'}`",
        f"- Target Ref: `{target_ref}`",
        f"- Target Commit: `{target_sha or 'unknown'}`",
        f"- Merge Base: `{merge_base}`",
        f"- Current Worktree Changed Files: `{', '.join(current_changed_files) if current_changed_files else 'None'}`",
        f"- Incoming Main Change Set: `{len(incoming_commits)} commit(s)`",
        *[f"  - {commit}" for commit in incoming_commits[:30]],
        f"- Incoming Changed Files: `{', '.join(incoming_files) if incoming_files else 'None'}`",
        f"- Branch Changed Files: `{', '.join(branch_files) if branch_files else 'None'}`",
        f"- Rebaseline Overlap Files: `{', '.join(rebaseline_overlap_files) if rebaseline_overlap_files else 'None'}`",
        f"- Rebaseline Overlap Intent Gate: `{'Not Applicable' if not rebaseline_overlap_files else 'Required - inspect Branch Change Intent Ledger before mutation'}`",
        f"- Overall Overlap Gate Result: `{overlap_gate_result}`",
        f"- Rebaseline Overlap Failure Procedure: `{'Not Applicable' if not rebaseline_overlap_files else 'Required - freeze mutation and classify every overlapping file PASS/WARN/BLOCKED'}`",
        f"- Rebaseline Overlap Intent Missing: `{'No' if not rebaseline_overlap_files else 'BLOCKED until branch-owned intent evidence is proven, waived, deferred by USER decision, or sequencing changes'}`",
        "- Overlap File Details:",
        *_overlap_detail_lines(rebaseline_overlap_files),
        f"- Incoming Runtime / Source-Truth Risk: `{'; '.join(source_truth_risk)}`",
        f"- Shared Surface / Worktree Overlap Forecast: `{', '.join(sorted(overlap_files)) if overlap_files else 'No incoming/local dirty-file overlap detected across sibling worktrees.'}`",
        "- Sibling Worktree Snapshot:",
        *(sibling_rows or ["- None detected"]),
        f"- Validation Before Rebaseline: `Not run by helper - report-only helper preserves command selection for the owning phase.`",
        f"- Recommendation Only: `YES - no fetch, merge, rebase, checkout, reset, or file mutation was performed.`",
        f"- Rebaseline Recommendation: `{recommendation_state} - {recommendation}`",
        f"- Rebaseline Mutation Approval: `Pending USER approval for exact worktree, branch, target commit, and operation type.`",
        f"- Rebaseline Mutation Status: `{'Blocked - Rebaseline Overlap Intent Missing pending branch-owned evidence review.' if overlap_gate_result == 'BLOCKED' else 'Not started - helper is report-only.'}`",
        "",
        "Current-Main Reconciliation Identity Guard:",
        *[f"- {line}" for line in identity_guard],
    ]
    if len(incoming_commits) > 30:
        lines.insert(13 + 30, f"  - ... {len(incoming_commits) - 30} more commit(s) omitted")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a report-only Pre-Rebaseline Impact Audit packet."
    )
    parser.add_argument(
        "--target-ref",
        default="origin/main",
        help="Target ref to audit against. Defaults to origin/main.",
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="Worktree path to inspect. Defaults to the current directory.",
    )
    args = parser.parse_args()
    print(build_report(Path(args.cwd), args.target_ref))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
