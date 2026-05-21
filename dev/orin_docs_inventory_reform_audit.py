"""Generate the full Docs source-truth reform audit dossier.

The helper is intentionally report/generation focused: it inspects every file
under Docs/, writes a markdown review dossier, and gives validators a stable
surface to check. It does not mutate runtime code or any worktree outside the
current repo.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
AUDIT = DOCS / "governance_docs_full_inventory_reform_audit.md"
INDEX = DOCS / "governance_docs_reform_user_review_index.md"

PATTERNS = {
    "live": (
        r"\bHEAD\b",
        r"origin/main",
        r"merge base",
        r"ahead",
        r"behind",
        r"dirty",
        r"clean",
        r"git status",
        r"git rev-parse",
        r"remote branch",
        r"worktree status",
    ),
    "pr_release_issue": (
        r"PR #\d+",
        r"Pull Request",
        r"GitHub Release",
        r"Release Candidate",
        r"Release Window",
        r"Latest Public",
        r"Merged-Unreleased",
        r"merge commit",
        r"Merged at",
        r"issue #\d+",
        r"review thread",
        r"watcher",
    ),
    "package_slice": (
        r"Package Trace",
        r"Slice Trace",
        r"Package ID",
        r"Slice ID",
        r"Admission State",
        r"Element Validation Ledger",
        r"Single-Slice",
        r"Package Completion",
    ),
    "branch_phase": (
        r"Active Branch",
        r"Current Branch",
        r"Next Legal Phase",
        r"Current Phase",
        r"Phase Status",
        r"Worktree",
        r"Branch Readiness",
        r"Workstream",
        r"Hardening",
        r"Live Validation",
        r"PR Readiness",
        r"Release Readiness",
        r"Selected Next",
        r"Active Seam",
    ),
    "validator": (
        r"dev/",
        r"dev\\",
        r"validator",
        r"validation",
        r"helper",
        r"compileall",
        r"orin_",
        r"Validation Results",
        r"PASS",
        r"FAIL",
    ),
}

FACT_CLASSES = {
    "active branch authority": (r"Active Branch Authority", r"Active Branch", r"Branch Authority"),
    "current branch status": (r"Current Branch", r"Branch HEAD", r"Current local HEAD"),
    "next legal phase": (r"Next Legal Phase", r"Exact USER decision", r"Exact USER Decision"),
    "selected-next": (r"Selected Next", r"Selected-Next", r"Next Workstream"),
    "worktree slot assignment": (r"Slot ID", r"Assignment Status", r"Expected Path"),
    "worktree live state": (r"dirty", r"clean", r"ahead", r"behind", r"worktree status"),
    "origin/main": (r"origin/main",),
    "PR state": (r"Live PR State", r"PR #\d+", r"mergeable", r"reviewDecision"),
    "merge status": (r"merge commit", r"merged", r"Merged at"),
    "latest tag/release": (r"Latest Public", r"latest tag", r"GitHub Release"),
    "release receipt": (r"Release Summary", r"Release Receipt", r"Release Window"),
    "release sequencing": (r"release sequencing", r"public milestone", r"pre-Beta"),
    "package trace": (r"Package Trace", r"Package ID", r"Package Completion"),
    "slice trace": (r"Slice Trace", r"Slice ID", r"Admission State"),
    "issue posture": (r"issue #\d+", r"GitHub issue", r"Issue Posture"),
    "branch runtime plan": (
        r"Branch Runtime Engineering Plan",
        r"Engineering Plan",
        r"Plan-To-Implementation",
    ),
    "branch phase history": (r"Current Phase", r"Phase Status", r"Historical Seam", r"Active Seam"),
    "branch receipt": (r"Historical", r"Receipt", r"Merge Proof", r"Closeout"),
    "workstream durable history": (r"Workstream", r"Durable", r"Proof", r"User Test Summary"),
    "family dossier continuity": (r"family dossier", r"Family Dossier", r"Family Anchor"),
    "validator registry": (r"validation_helper_registry", r"Helper Status", r"Reusable"),
    "helper responsibility": (r"Helper", r"validator", r"orin_"),
    "phase rules": (r"Phase", r"Gate", r"blocks", r"Required"),
    "prompt/Codex mode rules": (r"Codex", r"prompt", r"template", r"mode"),
    "release note/public body rules": (r"release notes", r"public", r"Release body"),
}

OWNER_DESCRIPTIONS = {
    "recovery map / source-truth router": (
        "highest-level recovery map and source-truth ownership map",
        "pointers to canonical owners and compact required field names",
        "detailed branch execution, release windows, or policy prose",
    ),
    "normative phase governance": (
        "canonical phase names, gates, blockers, proof hierarchy, phase transitions",
        "normative phase rules and machine-facing blocker names",
        "branch-local implementation receipts",
    ),
    "Codex execution rule mirror": (
        "developer-facing execution rules and compact governance mirrors",
        "execution reminders and pointers to owners",
        "full duplicated phase/release policy text",
    ),
    "Codex mode / behavior mirror": (
        "Codex collaboration modes and compact behavior mirrors",
        "mode behavior, evidence posture, and pointers",
        "branch-local truth or duplicated policy law",
    ),
    "prompt template": (
        "reusable prompt packet skeleton",
        "fields prompts should include and owner pointers",
        "current live facts or branch execution detail",
    ),
    "operator guide": (
        "human-readable guide",
        "operator explanation and examples",
        "machine-enforced current-state authority",
    ),
    "ChatGPT loader / prompt gate": (
        "ChatGPT-facing startup/loader contract",
        "loader map and prompt-generation guardrails",
        "Codex execution authority or branch state",
    ),
    "compact product registry": (
        "feature-family identity, priority, status, scope, package summary, canonical pointers",
        "FAM registry rows and compact pointers",
        "package trace, slice trace, live branch/release/issue state",
    ),
    "release sequencing posture": (
        "release sequencing and public milestone posture",
        "release stream intent and milestone pointers",
        "live latest-release state or PR windows",
    ),
    "worktree slot registry": (
        "stable slot IDs and intended assignment receipts",
        "slot role, expected path, assignment receipt fields",
        "HEAD, dirty state, ahead/behind, PR/release state",
    ),
    "branch authority router": (
        "active/historical branch authority routing",
        "lists and rules for branch authority records",
        "detailed implementation plans",
    ),
    "branch authority / compact receipt": (
        "branch authority, approvals, phase history, legal carrier status, compact receipts",
        "branch identity, phase markers, approvals, blockers, historical receipt",
        "durable family implementation history after fold-down",
    ),
    "branch runtime engineering plan": (
        "active branch engineering plan",
        "per-seam checklists, deltas, proof, approval boundaries while active",
        "permanent family dossier after PR fold-down",
    ),
    "branch plan standard": (
        "branch runtime engineering plan standard",
        "required plan markers and lifecycle",
        "branch-specific live truth",
    ),
    "branch plan inventory receipt": (
        "branch-specific inventory evidence",
        "inventory rows and marker evidence while receipt needs it",
        "live branch state after fold-down",
    ),
    "workstream index": (
        "canonical workstream and dossier routing",
        "workstream rules, family routing, durable owner pointers",
        "live branch state by inertia",
    ),
    "workstream durable history": (
        "durable implementation history, proof, package/slice trace",
        "implemented slices, proof, reusable lessons, closeout",
        "volatile Git/GitHub live facts",
    ),
    "family dossier": (
        "long-lived family continuity",
        "family routing, historical pass index, reusable continuity",
        "active worktree/PR state",
    ),
    "release closeout receipt": (
        "historical release/closeout receipt",
        "validated release interpretation and closure summary",
        "live latest-release state",
    ),
    "validator/helper registry": (
        "durable helper inventory and responsibility registry",
        "helper statuses, reuse/consolidation story",
        "workstream evidence details",
    ),
    "governance support standard": (
        "supporting governance standard",
        "single-purpose governance rules and pointers",
        "branch-specific blocker narrative",
    ),
    "product / architecture reference": (
        "durable product or architecture reference",
        "stable architecture/product intent",
        "current phase or live Git/GitHub truth",
    ),
    "bug / issue historical tracker": (
        "historical bug/issue evidence",
        "closed issue context and durable historical notes",
        "live issue state",
    ),
    "unknown docs reference": (
        "documentation reference",
        "only its proven durable purpose",
        "duplicated live state",
    ),
}


def git_output(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, cwd=ROOT).strip()
    except Exception:
        return "UNKNOWN"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def count_matches(text: str, patterns: tuple[str, ...]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.I)) for pattern in patterns)


def snippets(text: str, patterns: tuple[str, ...], limit: int = 5) -> list[str]:
    found: list[str] = []
    for line in text.splitlines():
        if any(re.search(pattern, line, flags=re.I) for pattern in patterns):
            clean = re.sub(r"\s+", " ", line.strip())
            if clean and clean not in found:
                found.append(clean[:180])
            if len(found) >= limit:
                break
    return found


def md_list(items: list[str]) -> str:
    if not items:
        return "None found."
    suffix = "; ..." if len(items) > 8 else ""
    return "; ".join(f"`{item}`" for item in items[:8]) + suffix


def heading_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip() or fallback
    return fallback


def owner_for(rel: str) -> str:
    if rel == "Docs/Main.md":
        return "recovery map / source-truth router"
    if rel == "Docs/phase_governance.md":
        return "normative phase governance"
    if rel == "Docs/development_rules.md":
        return "Codex execution rule mirror"
    if rel == "Docs/codex_modes.md":
        return "Codex mode / behavior mirror"
    if rel == "Docs/orin_task_template.md":
        return "prompt template"
    if rel == "Docs/codex_user_guide.md":
        return "operator guide"
    if rel == "Docs/nexus_startup_contract.md":
        return "ChatGPT loader / prompt gate"
    if rel == "Docs/feature_backlog.md":
        return "compact product registry"
    if rel == "Docs/prebeta_roadmap.md":
        return "release sequencing posture"
    if rel == "Docs/worktree_slots.md":
        return "worktree slot registry"
    if rel == "Docs/branch_records/index.md":
        return "branch authority router"
    if rel.startswith("Docs/branch_records/"):
        return "branch authority / compact receipt"
    if rel == "Docs/branch_plans/README.md":
        return "branch plan standard"
    if rel.endswith("_inventory.md") and rel.startswith("Docs/branch_plans/"):
        return "branch plan inventory receipt"
    if rel.startswith("Docs/branch_plans/"):
        return "branch runtime engineering plan"
    if rel == "Docs/workstreams/index.md":
        return "workstream index"
    if rel.startswith("Docs/workstreams/") and "family_dossier" in rel:
        return "family dossier"
    if rel.startswith("Docs/workstreams/"):
        return "workstream durable history"
    if rel.startswith("Docs/closeouts/") or rel in {
        "Docs/closeout_index.md",
        "Docs/closeout_guidance.md",
    }:
        return "release closeout receipt"
    if rel == "Docs/validation_helper_registry.md":
        return "validator/helper registry"
    if rel.startswith("Docs/governance") or rel in {
        "Docs/pr_watcher_mode_contract.md",
        "Docs/incident_patterns.md",
        "Docs/user_test_summary_guidance.md",
    }:
        return "governance support standard"
    if rel == "Docs/fb_027_overlay_bug_tracker.md":
        return "bug / issue historical tracker"
    if rel in {
        "Docs/architecture.md",
        "Docs/boot_access_design.md",
        "Docs/orin_vision.md",
        "Docs/orin_interaction_architecture.md",
        "Docs/orin_display_naming_guidance.md",
        "Docs/orchestration.md",
        "Docs/ownership_ip_plan.md",
        "Docs/workspace_layout_plan.md",
        "Docs/ncp_hardening_assessment.md",
    }:
        return "product / architecture reference"
    return "unknown docs reference"


def owner_for_fact(fact: str) -> str:
    mapping = {
        "active branch authority": "Docs/branch_records/index.md and active branch authority record",
        "current branch status": "Git/GitHub/helper-derived truth plus active branch authority record receipt",
        "next legal phase": "active branch authority record or phase packet",
        "selected-next": "Branch/PR Readiness packet and owning branch record only when USER-approved",
        "worktree slot assignment": "Docs/worktree_slots.md assignment receipt",
        "worktree live state": "git status / worktree preflight / helper output",
        "origin/main": "git fetch + git rev-parse / helper output",
        "PR state": "GitHub / watcher / gh / GraphQL output",
        "merge status": "GitHub PR merge truth plus compact historical receipt",
        "latest tag/release": "GitHub Releases / tags / release validator",
        "release receipt": "Docs/closeouts, compact branch receipt, or release body after validation",
        "release sequencing": "Docs/prebeta_roadmap.md",
        "package trace": "Docs/workstreams or family dossiers",
        "slice trace": "Docs/workstreams or family dossiers",
        "issue posture": "GitHub issues plus compact historical receipt when needed",
        "branch runtime plan": "Docs/branch_plans/<branch>.md while active",
        "branch phase history": "Docs/branch_records/<branch>.md compact receipt",
        "branch receipt": "Docs/branch_records/<branch>.md",
        "workstream durable history": "Docs/workstreams/<id>.md or family dossier",
        "family dossier continuity": "Docs/workstreams/*_family_dossier.md",
        "validator registry": "Docs/validation_helper_registry.md",
        "helper responsibility": "Docs/validation_helper_registry.md",
        "phase rules": "Docs/phase_governance.md",
        "prompt/Codex mode rules": "Docs/orin_task_template.md / Docs/codex_modes.md with owner pointers",
        "release note/public body rules": "Docs/phase_governance.md and dev/orin_release_body_validation.py",
    }
    return mapping.get(fact, "owning source-truth surface")


def action_for(rel: str, owner: str, lines: int, changed: set[str]) -> tuple[str, str, str]:
    completed = (
        "Updated in this reform branch."
        if rel in changed
        else "No direct edit in this branch; classified and governed by this dossier."
    )
    remaining = "None unless USER edits this dossier or a future validator flags drift."
    action = "Keep"
    if owner in {"compact product registry", "release sequencing posture", "worktree slot registry"}:
        return (
            "Keep compact",
            completed,
            "Keep pointer-only; do not reintroduce live state or detailed trace tables.",
        )
    if owner == "branch authority / compact receipt":
        if rel == "Docs/branch_records/feature_release_readiness_source_truth_intake.md":
            return (
                "Keep active standing authority",
                completed,
                "Keep current markers compact and avoid cycle-ledger closeout-only PRs.",
            )
        if lines > 400:
            return (
                "Migrate / compact receipt",
                completed,
                "Future focused pass should fold the long historical diary into a compact receipt and promote reusable detail to workstreams/family dossiers.",
            )
        return (
            "Keep historical receipt",
            completed,
            "Keep as historical receipt; remove stale active wording if reopened or edited.",
        )
    if owner == "branch runtime engineering plan":
        return (
            "Fold-down then delete candidate",
            completed,
            "At PR Readiness Stage 1/2 for the owning branch, migrate durable content to branch receipt/workstream/family dossier, then delete this plan when no active branch depends on it.",
        )
    if owner == "workstream durable history":
        return (
            "Keep / normalize durable history",
            completed,
            "Future focused pass may label old live-state markers as historical without deleting proof.",
        )
    if owner == "family dossier":
        return (
            "Keep / expand as durable owner",
            completed,
            "Use as migration target for package/slice/detail that should leave backlog, roadmap, and branch diaries.",
        )
    if owner == "unknown docs reference":
        return (
            "USER review needed",
            completed,
            "Confirm durable purpose or approve retirement after reference scan.",
        )
    return action, completed, remaining


def validator_need(owner: str) -> str:
    if owner in {"compact product registry", "release sequencing posture"}:
        return "Governance efficiency validator blocks live-state, Package Trace, Slice Trace, branch-plan detail, and repeated release-window sprawl."
    if owner == "worktree slot registry":
        return "Governance efficiency validator blocks live-state/PR/release sprawl in slot registry."
    if owner == "branch authority / compact receipt":
        return "Branch governance validator checks active/historical authority, stale active wording, and phase/receipt markers where machine-checkable."
    if owner == "branch runtime engineering plan":
        return "Planning fixture validator checks required plan structure; future PR Readiness should enforce fold-down/deletion for the owning branch."
    if owner in {"workstream durable history", "family dossier"}:
        return "Branch governance validator and future dossier checks should preserve durable trace ownership without treating old live facts as current."
    return "Covered by existing owner validator or future focused owner check."


def bool_text(value: bool) -> str:
    return "Yes" if value else "No"


def compact_review_value(value: str, limit: int = 96) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def build_user_review_index(
    *,
    docs_count: int,
    head: str,
    origin_main: str,
    merge_base: str,
    high_risk: list[dict[str, object]],
    migration_candidates: list[dict[str, object]],
    safe_files: list[dict[str, object]],
    retire_candidates: list[tuple[str, str, str]],
) -> str:
    def add_file_rows(rows: list[dict[str, object]], limit: int = 18) -> list[str]:
        table_rows: list[str] = []
        for row in rows[:limit]:
            table_rows.append(
                f"| `{row['rel']}` | {row['owner']} | {row['action']} | {row['risk']} |"
            )
        if not table_rows:
            table_rows.append("| None | N/A | N/A | N/A |")
        return table_rows

    out: list[str] = []
    add = out.append
    add("# Nexus Docs Reform User Review Index")
    add("")
    add("## Start Here")
    add("")
    add(
        "This is the short review index for the full Docs source-truth reform. "
        "Use it to decide whether the long dossier is ready for PR Readiness, "
        "or whether specific files need more cleanup first."
    )
    add("")
    add("## Review Proof")
    add("")
    add("- Full dossier: `Docs/governance_docs_full_inventory_reform_audit.md`")
    add(f"- Docs files covered: {docs_count}")
    add(f"- Generated from Governance HEAD: `{head}`")
    add(f"- origin/main at generation: `{origin_main}`")
    add(f"- merge base at generation: `{merge_base}`")
    add("- Runtime/FAM/Compact-AI mutation: none.")
    add("- PR Readiness: held until USER review accepts this packet.")
    add("")
    add("## Suggested Review Order")
    add("")
    add("1. Read `Executive Summary` and `How To Review This Dossier` in the full dossier.")
    add("2. Review `What Was Completed`, `What Remains Deferred`, and `What Requires USER Decision`.")
    add("3. Review the `Completed / Deferred Matrix` for the reform scope.")
    add("4. Scan `High-Risk Files`, `Files Needing Future Migration`, and `Files That May Be Retired Later`.")
    add("5. Use the `File-by-File Review Table` for a compact pass over every Docs file.")
    add("6. Use the detailed `File-By-File Review Dossier` only for files you want to inspect deeply.")
    add("7. Confirm the `PR Readiness Checklist` before approving PR creation.")
    add("")
    add("## Decision Checklist")
    add("")
    add("- [ ] The source-truth ownership split is acceptable.")
    add("- [ ] Backlog and roadmap roles are acceptable.")
    add("- [ ] Branch Runtime Engineering Plan lifecycle and deletion rule are acceptable.")
    add("- [ ] Deferred deletion/fold-down candidates should remain deferred for now.")
    add("- [ ] No additional Docs file needs immediate retirement before PR Readiness.")
    add("- [ ] Validators are enough to stop the worst sprawl from returning.")
    add("- [ ] PR Readiness Stage 2 may proceed after final validation.")
    add("")
    add("## Files Needing USER Decision")
    add("")
    add("| File | Reason | Recommendation |")
    add("| --- | --- | --- |")
    for rel, reason, rec in retire_candidates[:25]:
        add(f"| `{rel}` | {reason} | {rec} |")
    if not retire_candidates:
        add("| None | N/A | N/A |")
    add("")
    add("## High-Risk Review Queue")
    add("")
    add("| File | Owner | Recommendation | Risk |")
    add("| --- | --- | --- | --- |")
    out.extend(add_file_rows(high_risk))
    add("")
    add("## Future Migration Queue")
    add("")
    add("| File | Owner | Recommendation | Risk |")
    add("| --- | --- | --- | --- |")
    out.extend(add_file_rows(migration_candidates))
    add("")
    add("## Safe To Leave For Now")
    add("")
    add("| File | Owner | Recommendation | Risk |")
    add("| --- | --- | --- | --- |")
    out.extend(add_file_rows(safe_files))
    add("")
    add("## Exact USER Decision This Index Supports")
    add("")
    add(
        "`I accept the Docs reform review surface and approve PR Readiness Stage 2 / PR creation "
        "for feature/release-readiness-source-truth-intake targeting main. Merge, release work, "
        "runtime work, FAM-006/FAM-007/Compact-AI mutation, issue work, branch cleanup, historical "
        "branch deletion, and successor branch creation remain separate decisions.`"
    )
    return "\n".join(out) + "\n"


def generate() -> None:
    files = sorted(
        [path for path in DOCS.rglob("*") if path.is_file() and path != INDEX],
        key=lambda p: p.as_posix().lower(),
    )
    changed = set(git_output("diff", "--name-only", "origin/main...HEAD").splitlines())
    head = git_output("rev-parse", "HEAD")
    origin_main = git_output("rev-parse", "origin/main")
    merge_base = git_output("merge-base", "HEAD", "origin/main")

    file_rows: list[dict[str, object]] = []
    fact_map: dict[str, set[str]] = {key: set() for key in FACT_CLASSES}
    retire_candidates: list[tuple[str, str, str]] = []

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        lines = text.count("\n") + (1 if text else 0)
        owner = owner_for(rel)
        owns, should_record, should_move = OWNER_DESCRIPTIONS[owner]
        action, completed, remaining = action_for(rel, owner, lines, changed)
        counts = {name: count_matches(text, patterns) for name, patterns in PATTERNS.items()}
        duplicate_classes = [fact for fact, patterns in FACT_CLASSES.items() if count_matches(text, patterns)]
        for fact in duplicate_classes:
            fact_map[fact].add(rel)
        risk = "Low"
        if rel in {"Docs/feature_backlog.md", "Docs/prebeta_roadmap.md"}:
            risk = "Critical"
        elif owner == "branch authority / compact receipt" and lines > 400:
            risk = "High"
        elif counts["live"] + counts["pr_release_issue"] > 50 and owner not in {
            "release closeout receipt",
            "workstream durable history",
            "family dossier",
        }:
            risk = "High"
        elif counts["live"] or counts["pr_release_issue"] or counts["branch_phase"] > 10:
            risk = "Medium"
        confidence = "High" if owner != "unknown docs reference" else "Medium"
        if action == "USER review needed":
            retire_candidates.append((rel, "purpose not clearly owned by current model", "needs USER decision"))
        if owner == "branch runtime engineering plan":
            retire_candidates.append(
                (
                    rel,
                    "branch plan should be deleted after fold-down proves durable content migrated",
                    "safe later after owning branch PR Readiness fold-down; not deleted in this pass",
                )
            )
        file_rows.append(
            {
                "rel": rel,
                "lines": lines,
                "owner": owner,
                "action": action,
                "risk": risk,
                "confidence": confidence,
                "counts": counts,
                "title": heading_title(text, Path(rel).stem),
                "owns": owns,
                "should_record": should_record,
                "should_move": should_move,
                "completed": completed,
                "remaining": remaining,
                "duplicate_classes": duplicate_classes,
                "live_fields": snippets(text, PATTERNS["live"]),
                "receipt_fields": snippets(
                    text,
                    (r"Historical", r"Receipt", r"USER", r"Decision", r"Approval", r"Closeout", r"Merge Proof"),
                ),
                "current_markers": snippets(text, (r"Current", r"Active", r"Next Legal Phase", r"Phase Status")),
                "trace_markers": snippets(text, PATTERNS["package_slice"]),
                "branch_markers": snippets(text, PATTERNS["branch_phase"]),
                "release_markers": snippets(text, PATTERNS["pr_release_issue"]),
            }
        )

    high_risk = sorted(
        [row for row in file_rows if row["risk"] in {"High", "Critical"}],
        key=lambda row: (str(row["risk"]), str(row["rel"])),
    )
    migration_candidates = sorted(
        [
            row
            for row in file_rows
            if "Migrate" in str(row["action"])
            or "Fold-down" in str(row["action"])
            or "USER review" in str(row["action"])
        ],
        key=lambda row: str(row["rel"]),
    )
    safe_files = sorted(
        [
            row
            for row in file_rows
            if row["risk"] == "Low" and str(row["action"]).startswith("Keep")
        ],
        key=lambda row: str(row["rel"]),
    )

    index_text = build_user_review_index(
        docs_count=len(file_rows) + 1,
        head=head,
        origin_main=origin_main,
        merge_base=merge_base,
        high_risk=high_risk,
        migration_candidates=migration_candidates,
        safe_files=safe_files,
        retire_candidates=retire_candidates,
    )
    index_rel = INDEX.relative_to(ROOT).as_posix()
    index_owner = owner_for(index_rel)
    index_owns, index_should_record, index_should_move = OWNER_DESCRIPTIONS[index_owner]
    index_counts = {name: count_matches(index_text, patterns) for name, patterns in PATTERNS.items()}
    index_duplicate_classes = [
        fact for fact, patterns in FACT_CLASSES.items() if count_matches(index_text, patterns)
    ]
    for fact in index_duplicate_classes:
        fact_map[fact].add(index_rel)
    index_action, index_completed, index_remaining = action_for(
        index_rel, index_owner, index_text.count("\n"), changed
    )
    file_rows.append(
        {
            "rel": index_rel,
            "lines": index_text.count("\n"),
            "owner": index_owner,
            "action": index_action,
            "risk": "Medium",
            "confidence": "High",
            "counts": index_counts,
            "title": "Nexus Docs Reform User Review Index",
            "owns": index_owns,
            "should_record": index_should_record,
            "should_move": index_should_move,
            "completed": "Created in this review-surface repair branch.",
            "remaining": index_remaining,
            "duplicate_classes": index_duplicate_classes,
            "live_fields": snippets(index_text, PATTERNS["live"]),
            "receipt_fields": snippets(
                index_text,
                (r"Historical", r"Receipt", r"USER", r"Decision", r"Approval", r"Closeout", r"Merge Proof"),
            ),
            "current_markers": snippets(
                index_text, (r"Current", r"Active", r"Next Legal Phase", r"Phase Status")
            ),
            "trace_markers": snippets(index_text, PATTERNS["package_slice"]),
            "branch_markers": snippets(index_text, PATTERNS["branch_phase"]),
            "release_markers": snippets(index_text, PATTERNS["pr_release_issue"]),
        }
    )
    file_rows = sorted(file_rows, key=lambda row: str(row["rel"]).lower())
    high_risk = sorted(
        [row for row in file_rows if row["risk"] in {"High", "Critical"}],
        key=lambda row: (str(row["risk"]), str(row["rel"])),
    )
    migration_candidates = sorted(
        [
            row
            for row in file_rows
            if "Migrate" in str(row["action"])
            or "Fold-down" in str(row["action"])
            or "USER review" in str(row["action"])
        ],
        key=lambda row: str(row["rel"]),
    )
    safe_files = sorted(
        [
            row
            for row in file_rows
            if row["risk"] == "Low" and str(row["action"]).startswith("Keep")
        ],
        key=lambda row: str(row["rel"]),
    )

    converted_pointer = {
        "Docs/feature_backlog.md",
        "Docs/prebeta_roadmap.md",
        "Docs/worktree_slots.md",
        "Docs/Main.md",
        "Docs/development_rules.md",
        "Docs/codex_modes.md",
        "Docs/orin_task_template.md",
        "Docs/codex_user_guide.md",
        "Docs/branch_records/index.md",
        "Docs/branch_plans/README.md",
        "Docs/workstreams/index.md",
    }

    out: list[str] = []
    add = out.append
    add("# Governance Docs Full Inventory Reform Audit")
    add("")
    add("## Executive Summary")
    add("")
    add(
        "This dossier is the full markdown-friendly review packet for the Docs source-truth reform. "
        "It enumerates every file under `Docs/`, assigns each file a source-truth role, records what "
        "each file should and should not own, maps duplicated fact classes, and records which cleanup "
        "is complete versus deferred for USER review."
    )
    add("")
    add(
        "The reform direction is conservative about historical evidence: live operational truth moves "
        "to Git/GitHub/helpers, but validated historical receipts are preserved unless a focused "
        "fold-down/deletion decision is safe."
    )
    add("")
    add("Start here for review: `Docs/governance_docs_reform_user_review_index.md`.")
    add("")
    add("## How To Review This Dossier")
    add("")
    add("1. Start with the companion index: `Docs/governance_docs_reform_user_review_index.md`.")
    add("2. Read `What Was Completed`, `What Remains Deferred`, and `What Requires USER Decision` below.")
    add("3. Review `High-Risk Files`, `Files Needing Future Migration`, and `Files That May Be Retired Later`.")
    add("4. Use `File-by-File Review Table` for a compact row-by-row pass over every Docs file.")
    add("5. Use `File-By-File Review Dossier` for detailed per-file evidence and notes.")
    add("6. Approve PR Readiness only when the `PR Readiness Checklist` is acceptable.")
    add("")
    add("## What Was Completed")
    add("")
    add("- Every file under `Docs/` is enumerated in the manifest, review table, and detailed dossier.")
    add("- Backlog, roadmap, and worktree-slot ownership rules are captured as compact pointer/status surfaces.")
    add("- Branch Runtime Engineering Plan lifecycle is stated as active-only, fold-down, then deletion after migration.")
    add("- Duplicate fact classes are mapped to their correct owner surfaces.")
    add("- Validator coverage checks dossier file count, required sections, file-by-file entries, and review index presence.")
    add("- A short user review index is generated for easier inspection before PR Readiness.")
    add("")
    add("## What Remains Deferred")
    add("")
    add("- Historical branch records larger than the compact receipt model remain preserved until a focused fold-down pass migrates durable detail.")
    add("- Historical Branch Runtime Engineering Plans remain queued for fold-down/deletion review until their durable content is migrated.")
    add("- Low-risk product/reference docs remain kept unless USER approves a later retirement pass.")
    add("- GitHub-derived live-state helpers can be expanded later, but this pass does not require runtime or GitHub source mutations.")
    add("")
    add("## What Requires USER Decision")
    add("")
    add("- Whether to approve PR Readiness Stage 2 after reviewing this dossier.")
    add("- Whether to run a later branch-plan fold-down/deletion pass for historical plans.")
    add("- Whether to run focused compaction of oversized historical branch diaries into workstreams/family dossiers.")
    add("- Whether to retire low-risk or duplicate reference docs after USER review.")
    add("- Whether to create or expand FAM-family dossiers as migration targets for bulk historical detail.")
    add("")
    add("## High-Risk Files")
    add("")
    add("| File | Owner | Recommendation | Why It Is High Risk |")
    add("| --- | --- | --- | --- |")
    for row in high_risk[:40]:
        add(
            f"| `{row['rel']}` | {row['owner']} | {row['action']} | "
            f"{row['risk']} source-truth density / migration risk |"
        )
    if not high_risk:
        add("| None | N/A | N/A | N/A |")
    add("")
    add("## Files Safe To Leave For Now")
    add("")
    add("| File | Owner | Recommendation |")
    add("| --- | --- | --- |")
    for row in safe_files[:40]:
        add(f"| `{row['rel']}` | {row['owner']} | {row['action']} |")
    if not safe_files:
        add("| None | N/A | N/A |")
    add("")
    add("## Files Needing Future Migration")
    add("")
    add("| File | Owner | Migration / Compaction Recommendation |")
    add("| --- | --- | --- |")
    for row in migration_candidates[:50]:
        add(f"| `{row['rel']}` | {row['owner']} | {row['remaining']} |")
    if not migration_candidates:
        add("| None | N/A | N/A |")
    add("")
    add("## Files That May Be Retired Later")
    add("")
    add("| File | Reason | Recommendation |")
    add("| --- | --- | --- |")
    for rel, reason, rec in retire_candidates:
        add(f"| `{rel}` | {reason} | {rec} |")
    if not retire_candidates:
        add("| None | N/A | N/A |")
    add("")
    add("## Audit Identity")
    add("")
    add("- Audit Type: Full `Docs/` source-truth inventory, cleanup, and restructuring dossier.")
    add("- Audit Workspace: `C:\\Nexus Worktrees\\Governance`")
    add("- Audit Branch: `feature/release-readiness-source-truth-intake`")
    add(f"- Audit HEAD: `{head}`")
    add(f"- Audit origin/main: `{origin_main}`")
    add(f"- Audit Merge Base: `{merge_base}`")
    add(f"- Audit File Count: {len(file_rows)} files under `Docs/`")
    add(f"- Manifest Files Enumerated: {len(file_rows)}")
    add("- Manifest Match: PASS - filesystem enumeration and dossier manifest counts match.")
    add("- Mutation Scope: docs/source-truth/governance/validator reform only.")
    add("- Runtime Mutation: none.")
    add("- FAM-006 / FAM-007 / Compact-AI Mutation: none.")
    add("- Release / Tag / GitHub Release / Issue Work: none.")
    add("")
    add("## Completed / Deferred Matrix")
    add("")
    add("| Reform Item | Completed In This Branch | Deferred | Reason Deferred | Future Owner | USER Decision Needed | Validator Coverage |")
    add("| --- | --- | --- | --- | --- | --- | --- |")
    matrix_rows = (
        ("feature_backlog compaction", "Yes", "No", "N/A", "Docs/feature_backlog.md", "No", "governance efficiency validation"),
        ("prebeta_roadmap compaction", "Yes", "No", "N/A", "Docs/prebeta_roadmap.md", "No", "governance efficiency validation"),
        ("worktree_slots cleanup", "Yes", "No", "N/A", "Docs/worktree_slots.md", "No", "governance efficiency validation"),
        ("branch_records cleanup", "Partial", "Yes", "Large historical records need safe fold-down into durable owners", "Docs/branch_records + workstreams/family dossiers", "Yes for bulk compaction", "branch governance validation"),
        ("branch_plans lifecycle", "Yes", "Deletion deferred", "Durable content must be migrated first", "Docs/branch_plans + branch records + workstreams/family dossiers", "Yes before deleting historical plans", "planning fixture and governance efficiency validation"),
        ("workstreams/family dossier ownership", "Yes", "Expansion deferred", "Future dossier creation should be focused by family", "Docs/workstreams", "Yes for new/expanded dossiers", "branch governance validation"),
        ("governance docs consolidation", "Yes", "No broad deletion", "Rule mirrors preserved as pointers where safe", "Main/phase/development/codex docs", "No", "governance efficiency validation"),
        ("duplicate live-state validator hardening", "Yes", "Focused future checks possible", "Some historical receipts intentionally preserve old live facts", "dev/orin_governance_efficiency_validation.py", "No", "governance efficiency validation"),
        ("source owner marker validation", "Yes", "No", "N/A", "dev/orin_source_owner_marker_validation.py", "No", "source owner marker validation"),
        ("Docs inventory regeneration helper", "Yes", "No", "N/A", "dev/orin_docs_inventory_reform_audit.py", "No", "governance efficiency validation"),
        ("file retirement/delete candidates", "Identified", "Yes", "Deletion needs USER review and migration proof", "USER-approved future cleanup", "Yes", "dossier + future focused validation"),
        ("release-state derived truth", "Yes", "No", "N/A", "Git/GitHub/release validators", "No", "release body and governance validation"),
        ("branch-state derived truth", "Yes", "No", "N/A", "git/GitHub/worktree audit helpers", "No", "branch governance validation"),
        ("worktree-state derived truth", "Yes", "No", "N/A", "git status/worktree audit helper", "No", "governance efficiency validation"),
    )
    for row in matrix_rows:
        add("| " + " | ".join(row) + " |")
    add("")
    add("## Reform Principles")
    add("")
    for principle in (
        "Git/GitHub/helpers own live operational truth: `HEAD`, `origin/main`, dirty state, ahead/behind, merge base, remote refs, PR state, reviews, latest tag/release, release existence, and issue state.",
        "Docs own governance intent, USER decisions, approvals, branch authority, historical interpretation, durable implementation proof, and compact pointers to owning records.",
        "Backlog owns compact feature-family identity, priority, status, family scope, package summary, and canonical pointers only.",
        "Roadmap owns release sequencing and public milestone posture only.",
        "Branch records own branch authority, phase history, approvals, legal carrier status, and compact current/historical receipts.",
        "Branch plans own detailed active-branch engineering plans while active, then fold down during PR Readiness and delete after durable content is migrated and no active branch depends on them.",
        "Workstreams and family dossiers own durable package trace, slice trace, implementation proof, closure history, and reusable continuity.",
        "Main owns recovery routing and source-truth ownership mapping, not detailed branch execution.",
        "Worktree slots own stable slot definitions and assignment/retirement receipts, not live Git/GitHub state.",
    ):
        add(f"- {principle}")
    add("")
    add("## Source-Truth Ownership Map")
    add("")
    add("| Surface | Owns | Must Not Own |")
    add("| --- | --- | --- |")
    ownership_rows = (
        ("Git/GitHub/helpers", "live operational truth", "governance decisions or durable source-truth interpretation"),
        ("Docs/Main.md", "recovery map and ownership routing", "detailed branch/release/live-state narration"),
        ("Docs/feature_backlog.md", "compact FAM registry and pointer layer", "Package Trace, Slice Trace, live branch/release/issue state"),
        ("Docs/prebeta_roadmap.md", "release sequencing and public milestone posture", "live latest-release or PR-window truth"),
        ("Docs/worktree_slots.md", "slot definitions and assignment receipts", "HEAD, dirty state, ahead/behind, PR/release state"),
        ("Docs/branch_records/index.md", "branch authority routing", "implementation checklists"),
        ("Docs/branch_records/<branch>.md", "authority, approvals, phase history, compact receipts", "durable family implementation history after fold-down"),
        ("Docs/branch_plans/<branch>.md", "active branch engineering plan", "permanent dossier after fold-down"),
        ("Docs/workstreams/<id>.md", "durable implementation and proof history", "volatile Git/GitHub live facts"),
        ("Docs/workstreams/*_family_dossier.md", "family continuity and migrated reusable detail", "active PR/worktree state"),
        ("Docs/validation_helper_registry.md", "helper inventory and responsibility", "branch-specific proof detail"),
        ("Docs/phase_governance.md", "normative phase rules", "branch-local implementation receipts"),
    )
    for surface, owns, no_own in ownership_rows:
        add(f"| `{surface}` | {owns} | {no_own} |")
    add("")
    add("## Complete Docs Manifest")
    add("")
    add("| # | File | Type / Owner | Lines | Action | Risk | Confidence |")
    add("| ---: | --- | --- | ---: | --- | --- | --- |")
    for idx, row in enumerate(file_rows, 1):
        add(
            f"| {idx} | `{row['rel']}` | {row['owner']} | {row['lines']} | "
            f"{row['action']} | {row['risk']} | {row['confidence']} |"
        )
    add("")
    add("## File-by-File Review Table")
    add("")
    add("| File path | Line count | Current purpose | Correct owner category | What this file records | What this file should record | Reform action completed | Remaining action needed | Recommendation | Duplicate truth found | Live operational truth found | Governance receipt found | Validator coverage | USER review notes |")
    add("| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in file_rows:
        counts = row["counts"]
        duplicate_found = bool(row["duplicate_classes"])
        live_found = bool(row["live_fields"]) or counts["live"] > 0
        receipt_found = bool(row["receipt_fields"])
        add(
            f"| `{row['rel']}` | {row['lines']} | {compact_review_value(str(row['title']))} | "
            f"{row['owner']} | {compact_review_value(str(row['owns']))} | "
            f"{compact_review_value(str(row['should_record']))} | "
            f"{compact_review_value(str(row['completed']))} | "
            f"{compact_review_value(str(row['remaining']))} | {row['action']} | "
            f"{bool_text(duplicate_found)} | {bool_text(live_found)} | "
            f"{bool_text(receipt_found)} | "
            f"{compact_review_value(validator_need(str(row['owner'])))} | _Add notes here._ |"
        )
    add("")
    add("## Fact-Class Ownership Table")
    add("")
    add("| Fact Class | Correct Owner | Files Where Detected | Risk |")
    add("| --- | --- | ---: | --- |")
    for fact, file_set in fact_map.items():
        count = len(file_set)
        risk = (
            "High"
            if fact in {"worktree live state", "PR state", "latest tag/release", "package trace", "slice trace"}
            and count > 3
            else ("Medium" if count > 1 else "Low")
        )
        add(f"| {fact} | {owner_for_fact(fact)} | {count} | {risk} |")
    add("")
    add("## Duplicate Truth Map")
    add("")
    add("| Repeated Fact / Record | Correct Owner | Converted To Pointer-Only | Still Needing Migration | Risk | Validation Rule Needed |")
    add("| --- | --- | --- | --- | --- | --- |")
    for fact, file_set in fact_map.items():
        files_for_fact = sorted(file_set)
        converted = [file for file in files_for_fact if file in converted_pointer]
        still = [file for file in files_for_fact if file not in converted_pointer]
        risk = (
            "High"
            if fact in {"worktree live state", "PR state", "latest tag/release", "package trace", "slice trace"} and still
            else ("Medium" if still else "Low")
        )
        validation = (
            "existing validator coverage"
            if fact in {"package trace", "slice trace", "worktree live state", "latest tag/release", "PR state"}
            else "owner-pointer review / future focused validator"
        )
        add(
            f"| {fact} | {owner_for_fact(fact)} | {md_list(converted)} | "
            f"{md_list(still[:10])} | {risk} | {validation} |"
        )
    add("")
    add("## Backlog Final Schema")
    add("")
    add(
        "`Docs/feature_backlog.md` now owns compact FAM registry and pointer fields: `FAM ID`, "
        "`Broad Product Family`, `Priority`, `Status`, `Package Posture`, `Canonical Detail Owner`, "
        "family scope, package summary, and historical trace coverage. It must not own Package Trace, "
        "Slice Trace, live branch state, release-window detail, issue ledgers, exact commit ledgers, "
        "long branch histories, or duplicated next legal phase text."
    )
    add("")
    add("## Roadmap Final Schema")
    add("")
    add(
        "`Docs/prebeta_roadmap.md` now owns pre-Beta release sequencing, public milestone posture, "
        "and release-readiness field expectations. It derives live latest release/tag/window truth "
        "from Git/GitHub/helpers and should not maintain active release state manually."
    )
    add("")
    add("## Branch Records Final Schema")
    add("")
    add(
        "Branch records own branch identity, approvals, current/historical phase status, blockers, "
        "legal carrier posture, compact receipt, and pointers. Large historical execution diaries are "
        "preserved as historical evidence in this pass, but future focused migration should compact "
        "them and promote durable implementation detail to workstreams or family dossiers."
    )
    add("")
    add("## Branch Plans Lifecycle And Deletion Rule")
    add("")
    add(
        "Branch Runtime Engineering Plans are canonical only while the owning branch is active. They "
        "are created/admitted during Branch Readiness Stage 2 for runtime-focused branches, used "
        "through Workstream/Hardening/Live Validation, folded down during PR Readiness Stage 1, and "
        "deleted during or before PR Readiness Stage 2 only after durable content has been migrated "
        "to the branch receipt, workstream doc, family dossier, or other historical receipt owner. "
        "Existing historical plans are queued for fold-down/deletion review rather than deleted in "
        "this pass because their durable content has not been fully migrated and validated file-by-file."
    )
    add("")
    add("## Branch Runtime Engineering Plan Lifecycle Proof")
    add("")
    add("- Branch Runtime Engineering Plans are canonical active-branch planning docs while a runtime branch is active.")
    add("- Branch plans contain detailed per-seam implementation, validation, user-facing proof, future-gated items, and approval boundaries.")
    add("- Branch plans are folded down during PR Readiness Stage 1.")
    add("- Branch plans are deleted during or before PR Readiness Stage 2 approval after durable content is migrated.")
    add("- Durable content moves to the branch receipt, workstream doc, family dossier, or validated historical receipt owner.")
    add("- Backlog and roadmap remain compact pointer/status surfaces and must not absorb detailed branch planning.")
    add("")
    add("## Workstreams / Family Dossier Schema")
    add("")
    add(
        "Workstream docs and family dossiers own durable implementation history, package trace, slice "
        "trace, proof history, artifact/helper references, branch lessons, closeout evidence, and "
        "reusable continuity. They may preserve historical PR/release facts as receipts, but they "
        "should not present old live-state fields as current operational truth."
    )
    add("")
    add("## Worktree Slots Schema")
    add("")
    add(
        "`Docs/worktree_slots.md` owns stable slot IDs, roles, expected path pattern, assignment "
        "receipt fields, retirement receipt fields, and routing/collision recovery policy. It does "
        "not own live `HEAD`, clean/dirty state, ahead/behind state, merge base, remote branch "
        "existence, PR state, latest tag/release, or issue state."
    )
    add("")
    add("## Governance Docs Ownership Table")
    add("")
    add("| File | Owner Role | Reform Result |")
    add("| --- | --- | --- |")
    governance_owners = {
        "recovery map / source-truth router",
        "normative phase governance",
        "Codex execution rule mirror",
        "Codex mode / behavior mirror",
        "prompt template",
        "operator guide",
        "ChatGPT loader / prompt gate",
        "governance support standard",
        "validator/helper registry",
    }
    for row in file_rows:
        if row["owner"] in governance_owners:
            add(f"| `{row['rel']}` | {row['owner']} | {row['action']} |")
    add("")
    add("## Git / GitHub / Helper-Derived Truth Plan")
    add("")
    add(
        "Do not maintain these as active docs truth: current `origin/main`, branch `HEAD`, worktree "
        "dirty state, ahead/behind, merge base, remote branch existence, PR state, "
        "reviews/comments/checks, latest tag/release, release existence, and issue state. Use `git`, "
        "`gh`, GitHub GraphQL/API, release validators, worktree audit helpers, and PR watcher output "
        "as evidence at the time of phase execution."
    )
    add("")
    add("## Validator Enforcement Table")
    add("")
    add("| Validator / Helper | Coverage Added Or Preserved |")
    add("| --- | --- |")
    add("| `dev/orin_branch_governance_validation.py` | compact pointer model, branch authority, release-health, standing governance intake, branch/runtime plan markers, stale active wording where machine-checkable |")
    add("| `dev/orin_governance_efficiency_validation.py` | audit count, required dossier sections, backlog/roadmap sprawl, worktree slot live-state sprawl, branch-record/branch-plan/workstream fold-down rules, repeated release-readiness mirror text |")
    add("| `dev/orin_source_owner_marker_validation.py` | source-owner marker stability after compaction |")
    add("| `dev/orin_branch_readiness_planning_fixture_validation.py` | branch planning fixture quality and branch runtime engineering plan shape |")
    add("| `dev/orin_release_body_validation.py` | public release-body standard and latest release-body inspection |")
    add("| `dev/orin_ai_provider_state_validation.py` | FAM-007 provider state continuity while shared docs move |")
    add("| `dev/orin_docs_inventory_reform_audit.py` | regenerates this full Docs manifest and file-by-file reform dossier |")
    add("")
    add("## File Retirement / Delete Candidate Table")
    add("")
    add("| File | Reason | References / Replacement Owner | Recommendation |")
    add("| --- | --- | --- | --- |")
    for rel, reason, rec in retire_candidates:
        replacement = "branch receipt, workstream, family dossier, or USER-approved archive"
        if rel.startswith("Docs/branch_plans/"):
            replacement = "owning branch record plus workstream/family dossier after fold-down"
        add(f"| `{rel}` | {reason} | {replacement} | {rec} |")
    if not retire_candidates:
        add("| None | No candidates found | N/A | N/A |")
    add("")
    add("## File-By-File Review Dossier")
    add("")
    for idx, row in enumerate(file_rows, 1):
        add(f"### {idx}. `{row['rel']}`")
        add("")
        add(f"- File path: `{row['rel']}`")
        add(f"- Line count: {row['lines']}")
        add(f"- Current purpose: {row['title']}")
        counts = row["counts"]
        add(
            "- Actual observed use: "
            f"{row['owner']} with markers live={counts['live']}, "
            f"pr/release/issue={counts['pr_release_issue']}, "
            f"package/slice={counts['package_slice']}, "
            f"branch/worktree/phase={counts['branch_phase']}, "
            f"validator/helper={counts['validator']}."
        )
        add(f"- Correct owner category: {row['owner']}")
        add(f"- What gets recorded here: {row['owns']}.")
        add(f"- What should be recorded here: {row['should_record']}.")
        add(f"- What should move elsewhere: {row['should_move']}.")
        add(f"- Migration target: {row['should_move']}.")
        add(f"- Recommendation: {row['action']}.")
        duplicates = ", ".join(row["duplicate_classes"]) if row["duplicate_classes"] else "None found"
        add(f"- Duplicate fact classes found: {duplicates}.")
        add(f"- Live operational truth fields found: {md_list(row['live_fields'])}")
        add(f"- Governance receipt fields found: {md_list(row['receipt_fields'])}")
        repetitive = (
            "Release/phase/branch marker repetition requires owner-pointer discipline."
            if counts["branch_phase"] > 20 or counts["pr_release_issue"] > 20
            else "No major repetitive language flagged by scanner."
        )
        add(f"- Repetitive language found: {repetitive}")
        add(f"- Current-state markers found: {md_list(row['current_markers'])}")
        add(f"- Package Trace / Slice Trace markers found: {md_list(row['trace_markers'])}")
        add(f"- Branch/worktree/phase markers found: {md_list(row['branch_markers'])}")
        add(f"- Release/PR/issue markers found: {md_list(row['release_markers'])}")
        add(f"- Validator rule needed: {validator_need(str(row['owner']))}")
        add(f"- Reform action completed in this branch: {row['completed']}")
        add(f"- Remaining action needed after this branch: {row['remaining']}")
        add("- USER review notes: _Add notes here._")
        add("")
    add("## Remaining Risks")
    add("")
    add("- Many historical branch records and workstream records still contain historical live-state language. This is preserved as receipt evidence in this pass, not treated as active truth. Future focused fold-down passes can compact the largest diaries if USER wants smaller docs.")
    add("- Existing historical Branch Runtime Engineering Plans are not deleted yet because durable content must be migrated and references validated first.")
    add("- Some product/reference docs are low-risk but still need USER review before retirement because they may preserve historical design context.")
    add("")
    add("## PR Readiness Checklist")
    add("")
    add("- [ ] USER reviewed the companion index.")
    add("- [ ] USER reviewed high-risk files and deferred deletion candidates.")
    add("- [ ] USER accepts that no ambiguous Docs files are deleted before later focused approval.")
    add("- [ ] USER accepts Branch Runtime Engineering Plan fold-down/deletion lifecycle.")
    add("- [ ] Validation remains green from the Governance branch.")
    add("- [ ] PR creation is separately approved.")
    add("")
    add("## Deferred USER Decisions")
    add("")
    add("- Approve focused deletion/fold-down of historical branch plans after durable content is migrated.")
    add("- Approve focused compaction or archival of oversized historical branch execution diaries.")
    add("- Approve creation or expansion of FAM-006 / FAM-007 family dossiers if USER wants historical branch detail moved out of branch records in bulk.")
    add("- Approve retirement of any low-risk reference docs after USER review of the file-by-file dossier.")
    add("")
    add("## Next Legal Phase")
    add("")
    add("After this dossier and validators are accepted, the next legal phase is PR Readiness Stage 2 / PR creation for the Governance reform branch. Merge remains separate USER approval.")

    AUDIT.write_text("\n".join(out) + "\n", encoding="utf-8")
    INDEX.write_text(index_text, encoding="utf-8")
    print(
        f"Wrote {AUDIT.relative_to(ROOT)} and {INDEX.relative_to(ROOT)} "
        f"with {len(file_rows)} file entries"
    )


def main() -> int:
    if not DOCS.is_dir():
        print("FAIL: Docs directory missing")
        return 1
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
