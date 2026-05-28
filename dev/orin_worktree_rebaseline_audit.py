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
    "Docs/Main.md",
    "Docs/branch_records/index.md",
    "Docs/codex_modes.md",
    "Docs/codex_user_guide.md",
    "Docs/development_rules.md",
    "Docs/feature_backlog.md",
    "Docs/governance_efficiency_operating_model.md",
    "Docs/governance_intake_triage_and_digest_profiles.md",
    "Docs/governance_process_efficiency_reform_plan.md",
    "Docs/nexus_startup_contract.md",
    "Docs/orin_task_template.md",
    "Docs/pr_watcher_mode_contract.md",
    "Docs/prebeta_roadmap.md",
    "Docs/phase_governance.md",
    "Docs/user_test_summary_guidance.md",
    "Docs/validation_helper_registry.md",
    "Docs/workstreams/index.md",
    "Docs/worktree_slots.md",
}
PROMPT_TEMPLATE_FILES = {
    "Docs/codex_modes.md",
    "Docs/codex_user_guide.md",
    "Docs/nexus_startup_contract.md",
    "Docs/orin_task_template.md",
    "Docs/pr_watcher_mode_contract.md",
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
BRANCH_CHANGE_INTENT_HEADING = "Branch Change Intent Ledger"
BRANCH_CHANGE_INTENT_MARKERS = (
    "Surface Class:",
    "Change Intent:",
    "Why This File Was Touched:",
    "Owned Behavior / Fact Class:",
    "Canonical Owner / Source Owner:",
    "Resolution Owner:",
    "Shared Surface:",
    "Overlap Risk:",
    "Expected Conflict Risk:",
    "Semantic Merge Risk:",
    "Regression / Gating Impact:",
    "Conflict Resolution Rule:",
    "Rebaseline Handling:",
    "Validation Proof:",
    "Fallback Evidence:",
    "USER Decision / Waiver:",
    "Fold-Down Target:",
)
SEMANTIC_RISK_VALUES = {"none", "low", "medium", "high", "unknown"}
REGRESSION_GATING_IMPACT_VALUES = {"none", "low", "medium", "high", "unknown"}
RESOLUTION_OWNER_VALUES = {
    "current branch",
    "incoming/folded owner",
    "originating lane",
    "standing governance",
    "user decision",
    "future branch",
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


def _extract_marker_value(block: str, label: str) -> str:
    pattern = rf"(?m)^\s*-?\s*{re.escape(label)}\s*`?([^`\r\n]*)`?\s*$"
    match = re.search(pattern, block)
    if not match:
        pattern = rf"(?m)^\s*{re.escape(label)}\s*(.+?)\s*$"
        match = re.search(pattern, block)
    return match.group(1).strip() if match else ""


def _normalize_repo_path(path: str) -> str:
    return path.strip().strip("`").replace("\\", "/")


def _worktree_role(root: Path) -> str:
    normalized = _normalize_path(root)
    slot_role = _slot_role_from_worktree_slots(root, normalized)
    if slot_role:
        return slot_role
    if normalized.casefold() == Path("C:/Nexus Desktop AI").resolve().as_posix().casefold():
        return "neutral-main (neutral main / consolidator workspace)"
    if normalized.casefold() == Path("C:/Nexus Worktrees/Governance").resolve().as_posix().casefold():
        return "governance-standing (standing governance intake lane)"
    worktrees_root = Path("C:/Nexus Worktrees").resolve().as_posix().casefold()
    if normalized.casefold().startswith(worktrees_root + "/"):
        return "runtime-active candidate / USER-assigned runtime slot"
    return "unregistered worktree"


def _slot_role_from_worktree_slots(root: Path, normalized_worktree: str) -> str:
    slots_path = root / "Docs" / "worktree_slots.md"
    if not slots_path.is_file():
        return ""
    text = slots_path.read_text(encoding="utf-8", errors="replace")
    for match in re.finditer(r"(?ms)^###\s+([^\n]+)\n(.*?)(?=^###\s+|\Z)", text):
        section_name = match.group(1).strip()
        section = match.group(2)
        expected_path = _extract_marker_value(section, "Expected Path:")
        role = _extract_marker_value(section, "Role:")
        slot_id = _extract_marker_value(section, "Slot ID:")
        if not expected_path or "<USER-assigned label>" in expected_path:
            continue
        normalized_expected = Path(expected_path).resolve().as_posix().casefold()
        if normalized_worktree.casefold() == normalized_expected:
            role_value = role or section_name
            slot_value = slot_id or section_name
            return f"{slot_value} ({role_value})"
    return ""


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
        if normalized in PROMPT_TEMPLATE_FILES:
            return "prompt/template"
        if (
            normalized in HIGH_RISK_SOURCE_TRUTH_FILES
            or normalized.startswith("Docs/workstreams/")
        ):
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


def _branch_slug(branch: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", branch).strip("_")


def _resolve_branch_plan_path(root: Path, branch: str, explicit_path: str = "") -> tuple[str, str]:
    if explicit_path:
        plan_path = Path(explicit_path)
        if not plan_path.is_absolute():
            plan_path = root / plan_path
        if plan_path.is_file():
            try:
                return plan_path.relative_to(root).as_posix(), "explicit --branch-plan-path"
            except ValueError:
                return plan_path.as_posix(), "explicit --branch-plan-path"
        return explicit_path.replace("\\", "/"), "explicit --branch-plan-path missing"

    authority_record = _active_authority_record(root, branch)
    if authority_record.startswith("Docs/"):
        record_path = root / authority_record
        if record_path.is_file():
            record_text = record_path.read_text(encoding="utf-8", errors="replace")
            for marker in (
                "Branch Runtime Engineering Plan Path:",
                "Branch Engineering Plan Path:",
                "Branch Runtime Engineering Plan:",
            ):
                value = _extract_marker_value(record_text, marker)
                if value and value.casefold() not in {"not applicable", "none", "pending"}:
                    candidate = _normalize_repo_path(value)
                    if candidate.startswith("Docs/branch_plans/"):
                        return candidate, f"{authority_record} marker {marker}"

    inferred = f"Docs/branch_plans/{_branch_slug(branch)}.md"
    if (root / inferred).is_file():
        return inferred, "inferred from branch slug"
    return "", "not resolved"


def _branch_plan_text(root: Path, branch_plan_path: str) -> str:
    if not branch_plan_path:
        return ""
    path = Path(branch_plan_path)
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _branch_change_intent_entries(branch_plan_text: str) -> dict[str, dict[str, object]]:
    if f"## {BRANCH_CHANGE_INTENT_HEADING}" not in branch_plan_text:
        return {}
    ledger = branch_plan_text.split(f"## {BRANCH_CHANGE_INTENT_HEADING}", 1)[1]
    next_heading = re.search(r"(?m)^##\s+", ledger)
    if next_heading:
        ledger = ledger[: next_heading.start()]
    entries: dict[str, dict[str, object]] = {}
    for match in re.finditer(r"(?ms)^### Changed Surface:\s*([^\n]+)\n(.*?)(?=^### Changed Surface:|\Z)", ledger):
        file_name = _normalize_repo_path(match.group(1))
        block = match.group(2).strip()
        fields = {
            marker: _extract_marker_value(block, marker)
            for marker in BRANCH_CHANGE_INTENT_MARKERS
        }
        issues = _change_intent_entry_issues(file_name, fields)
        entries[file_name.casefold()] = {
            "path": file_name,
            "fields": fields,
            "issues": issues,
        }
    return entries


def _change_intent_entry_issues(file_name: str, fields: dict[str, str]) -> list[str]:
    issues: list[str] = []
    for marker in BRANCH_CHANGE_INTENT_MARKERS:
        if not fields.get(marker):
            issues.append(f"missing {marker}")

    surface_class = fields.get("Surface Class:", "").casefold()
    if surface_class and surface_class != _surface_class(file_name).casefold():
        issues.append(
            f"surface class mismatch: ledger={fields.get('Surface Class:')} helper={_surface_class(file_name)}"
        )
    if surface_class and surface_class not in {value.casefold() for value in _surface_class_values()}:
        issues.append("unknown Surface Class")

    semantic_risk = fields.get("Semantic Merge Risk:", "").casefold()
    regression_impact = fields.get("Regression / Gating Impact:", "").casefold()
    resolution_owner = fields.get("Resolution Owner:", "").casefold()
    fallback = fields.get("Fallback Evidence:", "").casefold()
    validation = fields.get("Validation Proof:", "").casefold()
    user_decision = fields.get("USER Decision / Waiver:", "").casefold()

    if semantic_risk and semantic_risk not in SEMANTIC_RISK_VALUES:
        issues.append("invalid Semantic Merge Risk")
    if regression_impact and regression_impact not in REGRESSION_GATING_IMPACT_VALUES:
        issues.append("invalid Regression / Gating Impact")
    if resolution_owner and resolution_owner not in RESOLUTION_OWNER_VALUES:
        issues.append("invalid Resolution Owner")
    if "fallback only" in fallback or (
        "compatibility bypass" in fallback and "not a compatibility bypass" not in fallback
    ):
        issues.append("fallback evidence attempts compatibility bypass")
    if validation and "validation" not in validation and "not run" not in validation:
        issues.append("validation proof does not name validation or not-run reason")
    if user_decision and not any(
        term in user_decision for term in ("user", "waiver", "approved", "pending", "not required")
    ):
        issues.append("USER decision boundary missing")

    helper_surface_class = _surface_class(file_name)
    if helper_surface_class in HIGH_RISK_SURFACE_CLASSES and semantic_risk == "unknown":
        issues.append("Semantic Merge Risk Unknown blocks high-risk overlap")
    if helper_surface_class == "fixture/test" and regression_impact in {"medium", "high", "unknown"}:
        issues.append("Regression / Gating Impact blocks fixture/test overlap")
    return issues


def _surface_class_values() -> tuple[str, ...]:
    return (
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
        "documentation/reference",
        "asset/media",
    )


def _assess_overlap_file(
    file_name: str,
    ledger_entries: dict[str, dict[str, object]],
) -> dict[str, str]:
    normalized = _normalize_repo_path(file_name)
    surface_class = _surface_class(normalized)
    entry = ledger_entries.get(normalized.casefold())
    branch_intent_present = "YES" if entry else "NO"
    entry_issues = list(entry.get("issues", [])) if entry else []
    fields = entry.get("fields", {}) if entry else {}
    semantic_risk = str(fields.get("Semantic Merge Risk:", "")) if isinstance(fields, dict) else ""
    regression_impact = str(fields.get("Regression / Gating Impact:", "")) if isinstance(fields, dict) else ""

    if entry_issues:
        per_file_result = "BLOCKED"
        risk = "; ".join(entry_issues)
    elif entry:
        if semantic_risk.casefold() == "high":
            per_file_result = "WARN"
            risk = "Branch-owned intent evidence exists, but semantic merge risk is High."
        else:
            per_file_result = "PASS"
            risk = "Branch-owned intent evidence exists and marker-first checks passed."
    elif surface_class in HIGH_RISK_SURFACE_CLASSES:
        per_file_result = "BLOCKED"
        risk = "High-risk overlap lacks Branch Change Intent Ledger evidence."
    else:
        per_file_result = "WARN"
        risk = "Lower-risk overlap lacks branch ledger evidence; fallback evidence may support a USER-visible recommendation."

    return {
        "file": normalized,
        "surface_class": surface_class,
        "branch_intent_present": branch_intent_present,
        "entry_issues": "; ".join(entry_issues) if entry_issues else "None",
        "semantic_risk": semantic_risk or "Not recorded",
        "regression_impact": regression_impact or "Not recorded",
        "per_file_result": per_file_result,
        "risk": risk,
    }


def _overall_overlap_gate_result(assessments: list[dict[str, str]]) -> str:
    if not assessments:
        return "Not Applicable"
    if any(assessment["per_file_result"] == "BLOCKED" for assessment in assessments):
        return "BLOCKED"
    if any(assessment["per_file_result"] == "WARN" for assessment in assessments):
        return "WARN"
    return "PASS"


def _overlap_assessments(
    overlap_files: list[str],
    ledger_entries: dict[str, dict[str, object]],
) -> list[dict[str, str]]:
    return [_assess_overlap_file(file_name, ledger_entries) for file_name in overlap_files]


def _legacy_path_only_overlap_result(overlap_files: list[str]) -> str:
    if not overlap_files:
        return "Not Applicable"
    if any(_surface_class(file_name) in HIGH_RISK_SURFACE_CLASSES for file_name in overlap_files):
        return "BLOCKED"
    return "WARN"


def _overlap_intent_missing_status(overlap_gate_result: str) -> str:
    if overlap_gate_result == "Not Applicable":
        return "No"
    if overlap_gate_result == "PASS":
        return "No - branch-owned overlap intent evidence passed marker-first checks"
    if overlap_gate_result == "WARN":
        return "WARN - lower-risk overlap requires USER-visible recommendation and USER approval before mutation"
    return (
        "BLOCKED until branch-owned intent evidence is proven, waived, "
        "deferred by USER decision, or sequencing changes"
    )


def _rebaseline_mutation_status(overlap_gate_result: str) -> str:
    if overlap_gate_result == "BLOCKED":
        return "Blocked - Rebaseline Overlap Intent Missing pending branch-owned evidence review."
    if overlap_gate_result == "WARN":
        return "Not started - WARN overlap requires USER approval before mutation."
    return "Not started - helper is report-only."


def _apply_overlap_recommendation(
    recommendation_state: str,
    recommendation: str,
    overlap_gate_result: str,
) -> tuple[str, str]:
    if overlap_gate_result == "BLOCKED":
        return (
            "Blocked",
            (
                "Rebaseline Overlap Intent Gate found high-risk overlapping files; "
                "inspect Branch Change Intent Ledger evidence before mutation."
            ),
        )
    if overlap_gate_result != "WARN":
        return recommendation_state, recommendation

    warn_recommendation = (
        "Rebaseline Overlap Intent Gate found lower-risk overlapping files; "
        "return the overlap packet and get USER approval before mutation."
    )
    if recommendation_state == "Blocked":
        return (
            recommendation_state,
            f"{recommendation} Overlap warning also present: {warn_recommendation}",
        )
    return "USER decision required", warn_recommendation


def _overlap_detail_lines(assessments: list[dict[str, str]]) -> list[str]:
    if not assessments:
        return ["- None"]
    lines: list[str] = []
    for assessment in assessments:
        lines.extend(
            [
                f"- File: `{assessment['file']}`",
                f"  - Surface Class: `{assessment['surface_class']}`",
                "  - Incoming Change Summary: `Review incoming diff from merge_base..target_ref`",
                "  - Current Branch Change Summary: `Review branch/worktree diff from merge_base..HEAD plus dirty files`",
                f"  - Branch Change Intent Present: `{assessment['branch_intent_present']}`",
                "  - Incoming Intent Evidence Present: `Review branch record, PR body, commit messages, source-owner markers, helper registry, fixtures, or workstream/family dossier`",
                "  - Fallback Evidence: `Available for classification only; not a compatibility bypass`",
                f"  - Semantic Merge Risk: `{assessment['semantic_risk']}`",
                f"  - Regression / Gating Impact: `{assessment['regression_impact']}`",
                f"  - Ledger Entry Issues: `{assessment['entry_issues']}`",
                f"  - Risk: `{assessment['risk']}`",
                f"  - Per-File Result: `{assessment['per_file_result']}`",
                "  - Recommended Resolution: `Repair, waive, defer, or approve only after evidence review`",
                "  - Resolution Owner: `USER Decision unless branch plan evidence names a narrower legal owner`",
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


def build_report(cwd: Path, target_ref: str, branch_plan_path: str = "") -> str:
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
    resolved_branch_plan_path, branch_plan_path_source = _resolve_branch_plan_path(
        root,
        branch,
        branch_plan_path,
    )
    ledger_entries = _branch_change_intent_entries(
        _branch_plan_text(root, resolved_branch_plan_path)
    )
    overlap_assessments = _overlap_assessments(rebaseline_overlap_files, ledger_entries)
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
    overlap_gate_result = _overall_overlap_gate_result(overlap_assessments)
    recommendation_state, recommendation = _apply_overlap_recommendation(
        recommendation_state,
        recommendation,
        overlap_gate_result,
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
        f"- Branch Change Intent Ledger Path: `{resolved_branch_plan_path or 'Not resolved'}`",
        f"- Branch Change Intent Ledger Path Source: `{branch_plan_path_source}`",
        f"- Branch Change Intent Ledger Entries: `{len(ledger_entries)}`",
        f"- Rebaseline Overlap Intent Gate: `{'Not Applicable' if not rebaseline_overlap_files else 'Required - inspect Branch Change Intent Ledger before mutation'}`",
        f"- Overall Overlap Gate Result: `{overlap_gate_result}`",
        f"- Rebaseline Overlap Failure Procedure: `{'Not Applicable' if not rebaseline_overlap_files else 'Required - freeze mutation and classify every overlapping file PASS/WARN/BLOCKED'}`",
        f"- Rebaseline Overlap Intent Missing: `{_overlap_intent_missing_status(overlap_gate_result)}`",
        "- Overlap File Details:",
        *_overlap_detail_lines(overlap_assessments),
        f"- Incoming Runtime / Source-Truth Risk: `{'; '.join(source_truth_risk)}`",
        f"- Shared Surface / Worktree Overlap Forecast: `{', '.join(sorted(overlap_files)) if overlap_files else 'No incoming/local dirty-file overlap detected across sibling worktrees.'}`",
        "- Sibling Worktree Snapshot:",
        *(sibling_rows or ["- None detected"]),
        f"- Validation Before Rebaseline: `Not run by helper - report-only helper preserves command selection for the owning phase.`",
        f"- Recommendation Only: `YES - no fetch, merge, rebase, checkout, reset, or file mutation was performed.`",
        f"- Rebaseline Recommendation: `{recommendation_state} - {recommendation}`",
        f"- Rebaseline Mutation Approval: `Pending USER approval for exact worktree, branch, target commit, and operation type.`",
        f"- Rebaseline Mutation Status: `{_rebaseline_mutation_status(overlap_gate_result)}`",
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
    parser.add_argument(
        "--branch-plan-path",
        default="",
        help=(
            "Optional active external branch_plan.md or repo historical "
            "Docs/branch_plans/<branch_slug>.md path to inspect for Branch "
            "Change Intent Ledger evidence."
        ),
    )
    args = parser.parse_args()
    print(build_report(Path(args.cwd), args.target_ref, args.branch_plan_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
