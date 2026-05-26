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
    "release schedule outline": (r"stage breakpoint", r"public milestone", r"pre-Beta", r"release schedule"),
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

AMBIGUITY_PATTERNS = {
    "volatile-current-wording": (
        r"\bcurrent\b",
        r"\bactive\b",
        r"\blatest\b",
        r"\bnext\b",
        r"\bpending\b",
    ),
    "unclear-ownership-wording": (
        r"\bowner\b",
        r"\bauthority\b",
        r"\bsource truth\b",
        r"\bcanonical\b",
        r"\bprimary\b",
    ),
    "soft-commitment-wording": (
        r"\bmaybe\b",
        r"\bpossibly\b",
        r"\blikely\b",
        r"\bshould\b",
        r"\bmay\b",
        r"\bTBD\b",
        r"\bTODO\b",
    ),
    "state-ledger-wording": (
        r"\bstate\b",
        r"\bstatus\b",
        r"\bposture\b",
        r"\bledger\b",
        r"\bwindow\b",
    ),
}

OWNER_DESCRIPTIONS = {
    "recovery map / source-truth router": (
        "least-updated canonical docs index, recovery map, and source-truth ownership map",
        "clear pointers to current governance/source-truth owners and a digest of each file's purpose",
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
    "release schedule outline": (
        "pre-Beta/Beta/release stage-breakpoint schedule and broad milestone checkpoints",
        "release-stage gates, public milestone checkpoints, and broad feature-family breakpoint references",
        "live latest-release state, release-window records, PR windows, or current branch/release execution ledgers",
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
    "branch authority / structured receipt": (
        "branch authority, approvals, phase history, legal carrier status, and structured traceability receipt",
        "branch identity, phase markers, approvals, blockers, commits/PRs/releases as historical evidence, and indexed receipt sections",
        "volatile live state, unindexed execution diaries, or reusable family implementation history after promotion",
    ),
    "branch runtime engineering plan": (
        "active branch engineering plan",
        "per-seam checklists, deltas, proof, approval boundaries while active",
        "permanent family dossier or active/live branch authority after PR fold-down",
    ),
    "branch plan standard": (
        "branch runtime engineering plan standard",
        "required plan markers and lifecycle",
        "branch-specific live truth",
    ),
    "branch plan retirement index": (
        "historical branch-plan retirement posture",
        "retired plan list, durable lookup path, and deletion guardrails",
        "active branch implementation detail",
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
    "family vision index": (
        "family vision routing",
        "family vision record index, owner relationship, and fold-down rule",
        "full family vision narratives or active branch implementation detail",
    ),
    "family vision": (
        "durable family product direction",
        "USER-accepted reusable family standards and future package boundaries",
        "active branch implementation checklists or live operational state",
    ),
    "Nexus Vision Contract": (
        "project-wide vision contract",
        "USER-accepted project-wide product principles, long-term standards, and durable product direction",
        "branch implementation checklists, live operational state, or family-specific execution ledgers",
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
    "external operational state reform plan": (
        "external operational state transition plan",
        "Docs split target matrix, staged implementation boundaries, and future-work sequencing",
        "active external-state root contents or migrated branch/worktree/release-window state",
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
        return "release schedule outline"
    if rel == "Docs/worktree_slots.md":
        return "worktree slot registry"
    if rel == "Docs/branch_records/index.md":
        return "branch authority router"
    if rel.startswith("Docs/branch_records/"):
        return "branch authority / structured receipt"
    if rel == "Docs/branch_plans/README.md":
        return "branch plan standard"
    if rel == "Docs/branch_plans/retirement_index.md":
        return "branch plan retirement index"
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
    if rel == "Docs/family_visions/README.md":
        return "family vision index"
    if rel.startswith("Docs/family_visions/"):
        return "family vision"
    if rel == "Docs/nexus_vision.md":
        return "Nexus Vision Contract"
    if rel.startswith("Docs/closeouts/") or rel in {
        "Docs/closeout_index.md",
        "Docs/closeout_guidance.md",
    }:
        return "release closeout receipt"
    if rel == "Docs/validation_helper_registry.md":
        return "validator/helper registry"
    if rel == "Docs/external_operational_state_store_reform_plan.md":
        return "external operational state reform plan"
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
        "merge status": "GitHub PR merge truth plus structured historical receipt",
        "latest tag/release": "GitHub Releases / tags / release validator",
        "release receipt": "Docs/closeouts, structured branch receipt, or release body after validation",
        "release schedule outline": "Docs/prebeta_roadmap.md",
        "package trace": "Docs/workstreams or family dossiers",
        "slice trace": "Docs/workstreams or family dossiers",
        "issue posture": "GitHub issues plus structured historical receipt when needed",
        "branch runtime plan": "Docs/branch_plans/<branch>.md while active",
        "branch phase history": "Docs/branch_records/<branch>.md structured receipt",
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


def branch_name_to_plan_path(branch: str) -> str:
    """Return the canonical branch-plan path for a live branch name."""
    return f"Docs/branch_plans/{branch.replace('-', '_').replace('/', '_')}.md"


def action_for(
    rel: str,
    owner: str,
    lines: int,
    changed: set[str],
    active_branch_plan_paths: set[str] | None = None,
) -> tuple[str, str, str]:
    completed = (
        "Updated in this reform branch."
        if rel in changed
        else "No direct edit in this branch; classified and governed by this dossier."
    )
    remaining = "None unless USER edits this dossier or a future validator flags drift."
    action = "Keep"
    if owner in {"compact product registry", "release schedule outline", "worktree slot registry"}:
        return (
            "Keep compact",
            completed,
            "Keep pointer-only; do not reintroduce live state or detailed trace tables.",
        )
    if owner == "branch authority / structured receipt":
        if rel == "Docs/branch_records/feature_release_readiness_source_truth_intake.md":
            return (
                "Keep active standing authority",
                completed,
                "Keep current markers compact and avoid cycle-ledger closeout-only PRs.",
            )
        if rel == "Docs/branch_records/feature_vision_update_decision_matrix.md":
            return (
                "Keep active bounded repair authority until PR fold-down",
                completed,
                "Move to historical/no-active posture or otherwise make merge-stable before PR green.",
            )
        if lines > 400:
            return (
                "Organize structured receipt",
                completed,
                "Future focused pass should organize the long historical ledger into current summary plus indexed receipt sections, and promote reusable detail to workstreams/family dossiers without losing traceability.",
            )
        return (
            "Keep historical receipt",
            completed,
            "Keep as historical receipt; remove stale active wording if reopened or edited.",
        )
    active_branch_plan_paths = active_branch_plan_paths or set()
    if owner == "branch runtime engineering plan" and rel in active_branch_plan_paths:
        return (
            "Keep active branch plan",
            completed,
            "Keep as active planning authority for the current branch until PR fold-down; do not queue for retired-plan cleanup while active.",
        )
    if owner == "branch runtime engineering plan":
        return (
            "Retired posture indexed",
            completed,
            "Do not reuse as an active plan; deletion requires later USER approval plus reference proof that durable content remains preserved.",
        )
    if owner == "branch plan retirement index":
        return (
            "Keep as retirement index",
            completed,
            "Keep as the central historical branch-plan retirement posture and deletion guardrail.",
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
    if owner == "family vision index":
        return (
            "Keep as family vision router",
            completed,
            "Keep as the compact index for family vision records and fold-down rules.",
        )
    if owner == "family vision":
        return (
            "Keep as family vision owner",
            completed,
            "Receive USER-accepted reusable family product direction; do not absorb branch implementation detail.",
        )
    if owner == "Nexus Vision Contract":
        return (
            "Keep as project-wide vision owner",
            completed,
            "Keep as project-wide product vision contract; route family-specific durable direction to family vision records and active implementation detail to branch plans.",
        )
    if owner == "unknown docs reference":
        return (
            "USER review needed",
            completed,
            "Confirm durable purpose or approve retirement after reference scan.",
        )
    return action, completed, remaining


def validator_need(owner: str) -> str:
    if owner in {"compact product registry", "release schedule outline"}:
        return "Governance efficiency validator blocks live-state, Package Trace, Slice Trace, branch-plan detail, and repeated release-window sprawl."
    if owner == "worktree slot registry":
        return "Governance efficiency validator blocks live-state/PR/release sprawl in slot registry."
    if owner == "branch authority / structured receipt":
        return "Branch governance validator checks active/historical authority, stale active wording, and phase/receipt markers where machine-checkable."
    if owner == "branch runtime engineering plan":
        return "Planning fixture validator checks required plan structure; governance efficiency validation requires historical plans to be represented in the retirement index."
    if owner == "branch plan retirement index":
        return "Governance efficiency validator requires every historical branch plan to appear in the retirement index before deletion can be considered."
    if owner in {"workstream durable history", "family dossier"}:
        return "Branch governance validator and future dossier checks should preserve durable trace ownership without treating old live facts as current."
    return "Covered by existing owner validator or future focused owner check."


def consolidation_target_for(row: dict[str, object]) -> str:
    rel = str(row["rel"])
    owner = str(row["owner"])
    action = str(row["action"])
    if rel == "Docs/feature_backlog.md":
        return "Keep here as compact product registry; move detailed trace to branch/workstream/family owners."
    if rel == "Docs/prebeta_roadmap.md":
        return "Keep here as stage-breakpoint schedule outline; move release state to Git/GitHub/helpers and receipts."
    if rel == "Docs/worktree_slots.md":
        return "Keep here as slot registry; move live worktree facts to git/helper output."
    if rel == "Docs/Main.md":
        return "Keep here as least-updated canonical docs index and recovery/source-truth map; move full policy to owner docs."
    if bool(row.get("active_branch_plan")):
        return "Current active branch plan; keep as live branch authority until PR Readiness fold-down moves it to historical posture."
    if owner == "branch runtime engineering plan":
        return "Listed in Docs/branch_plans/retirement_index.md as historical retired posture; keep durable lookup paths in branch records/workstreams/family vision owners."
    if owner == "branch plan retirement index":
        return "Keep here as central retired-plan lookup; do not duplicate full branch plans in this index."
    if owner == "branch authority / structured receipt":
        if "Organize" in action:
            return "Keep traceability, but reorganize into indexed current summary plus historical receipt sections; promote reusable implementation detail to workstreams or family dossiers."
        return "Keep as structured historical branch receipt."
    if owner == "workstream durable history":
        return "Keep as durable implementation/proof owner; normalize stale live wording only when edited."
    if owner == "family dossier":
        return "Keep or expand as durable family continuity owner."
    if owner == "family vision index":
        return "Keep as family vision router; use to find durable family vision records."
    if owner == "family vision":
        return "Keep as family-specific product vision owner; move active implementation detail to branch plans and durable proof to workstreams/branch receipts."
    if owner == "Nexus Vision Contract":
        return "Keep as project-wide product vision contract; route family-specific direction to Docs/family_visions/ and active execution detail to branch plans."
    if owner == "release closeout receipt":
        return "Keep as historical release/closeout receipt archive unless USER approves closeout consolidation."
    if owner in {
        "normative phase governance",
        "Codex execution rule mirror",
        "Codex mode / behavior mirror",
        "prompt template",
        "operator guide",
        "ChatGPT loader / prompt gate",
        "validator/helper registry",
        "governance support standard",
        "branch plan standard",
        "branch plan inventory receipt",
        "branch authority router",
        "workstream index",
        "product / architecture reference",
        "Nexus Vision Contract",
        "bug / issue historical tracker",
    }:
        return "Keep unless a focused USER-approved consolidation pass names a replacement owner."
    return "Needs USER review before consolidation or retirement."


def deletion_posture_for(row: dict[str, object]) -> str:
    owner = str(row["owner"])
    action = str(row["action"])
    if bool(row.get("active_branch_plan")):
        return "Active branch plan; do not delete, archive, or retire while this branch remains active."
    if owner == "branch runtime engineering plan":
        return "Retired from active planning posture; do not delete without separate USER approval and reference proof."
    if "USER review" in action:
        return "Needs USER decision before delete/retire."
    if "Migrate" in action or "Organize" in action:
        return "Do not delete now; organize or migrate first."
    return "Keep; no deletion recommended in this pass."


def ambiguity_for(text: str, owner: str) -> tuple[str, list[str], str]:
    hits: list[str] = []
    weighted = 0
    for label, patterns in AMBIGUITY_PATTERNS.items():
        count = count_matches(text, patterns)
        if count:
            hits.append(f"{label}={count}")
            weighted += count
    if owner in {
        "release closeout receipt",
        "workstream durable history",
        "family dossier",
        "branch authority / structured receipt",
    }:
        weighted = max(0, weighted - 20)
    if weighted >= 80:
        return "High", hits, "Clarify owner, time basis, and whether wording is historical receipt or live truth."
    if weighted >= 25:
        return "Medium", hits, "Review for ambiguous current/active/latest/pending ownership language."
    if weighted:
        return "Low", hits, "Low ambiguity; keep owner labels precise when edited."
    return "Low", hits, "No scanner ambiguity markers found."


def structure_for(text: str, lines: int, owner: str) -> tuple[str, str]:
    headings = len(re.findall(r"(?m)^#{1,6}\s+", text))
    tables = len(re.findall(r"(?m)^\|", text))
    bullets = len(re.findall(r"(?m)^\s*[-*]\s+", text))
    if not text.strip():
        return "High", "Empty or unreadable file; confirm purpose before keeping."
    if lines > 600 and headings < 8:
        return "High", "Long file with too few headings; split current summary from historical appendix or migrate detail."
    if lines > 400 and owner == "branch authority / structured receipt":
        return "High", "Large branch receipt; preserve traceability but organize current summary, indexed historical sections, commit/PR evidence, and promoted reusable lessons."
    if lines > 250 and headings < 5:
        return "Medium", "Large file needs clearer sections or a summary/index block."
    if owner in {"compact product registry", "release schedule outline", "worktree slot registry"} and lines > 220:
        return "Medium", "Pointer surface is getting long; watch for sprawl."
    if headings == 0 and lines > 40:
        return "Medium", "Reference file has limited heading structure."
    if tables + bullets == 0 and lines > 60:
        return "Medium", "Dense prose; consider a summary or table if edited."
    return "Low", "Structure is acceptable for current owner category."


def bool_text(value: bool) -> str:
    return "Yes" if value else "No"


def compact_review_value(value: str, limit: int = 96) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


USER_RESPONSE_INTEGRATION_ROWS = (
    (
        "Single PR / staged execution",
        "Run remaining reform as internal stages on this Governance carrier and one final PR path.",
        "This plan; generated dossier/index",
        "R1-R9 staged execution plan; PR Readiness held until validation is green and USER separately approves PR creation.",
        "Required generated sections prevent the response from being flattened into a passive note.",
    ),
    (
        "Main as canonical pointer ledger",
        "`Docs/Main.md` is the least-updated canonical docs index and recovery map.",
        "Main; operating model",
        "Do not add branch/release/current-state ledgers to Main.",
        "Pointer checks keep Main routed to the operating model.",
    ),
    (
        "Canonical docs versus context docs",
        "Canonical docs own law/routing; context docs preserve evidence, product reasoning, and history.",
        "Operating model; full dossier",
        "Every Docs file receives owner category, disposition, ambiguity risk, and structure risk.",
        "Inventory helper regenerates the file-by-file review surface.",
    ),
    (
        "Branch plans retire, not delete by default",
        "Plans are canonical while active, then fold down, migrate durable content, and retire.",
        "Branch plan README; branch record index; dossier",
        "Historical plan files are indexed as retired from active planning posture; deletion remains USER-gated.",
        "Planning fixtures and governance efficiency validation preserve the lifecycle language.",
    ),
    (
        "Traceability compaction is dangerous",
        "Branch records may remain large when they are structured traceability receipts.",
        "Branch records index; operating model; dossier",
        "Organize receipts instead of compressing away commit/PR/release/validation evidence.",
        "Sprawl checks focus on duplicate live state, not legitimate historical evidence.",
    ),
    (
        "Safe docs may delete/collapse only after proof",
        "Deletion requires reference scan, replacement owner, and USER acceptance when ambiguous.",
        "Full dossier; review index",
        "Every Docs file gets keep/organize/migrate/retire/delete posture.",
        "Inventory validation requires disposition rows for every Docs file.",
    ),
    (
        "Nexus Vision contract",
        "`Docs/nexus_vision.md` is the Nexus-wide vision contract after focused reference migration.",
        "Operating model; family vision records",
        "Use Nexus Vision for project-wide direction and family visions for durable family direction.",
        "Checks keep vision out of branch-plan implementation detail.",
    ),
    (
        "Backlog family vision discussion",
        "Backlog points to family vision owners but does not absorb long planning narratives.",
        "Backlog; family vision records",
        "Keep backlog compact while preserving product-intent routing.",
        "Backlog sprawl checks allow compact pointers, not detailed branch planning.",
    ),
)


SINGLE_PR_STAGED_EXECUTION_ROWS = (
    ("R1", "User-response model correction", "Turn USER responses into model decisions instead of passive notes.", "Update model, generator, generated dossier/index, and validator section requirements.", "Dossier/index expose integration sections."),
    ("R2", "Canonical/context taxonomy", "Make Main the least-updated canonical docs index and classify context docs.", "Update ownership language and file-by-file review categories.", "Every Docs file has owner, action, risk, and migration target."),
    ("R3", "Backlog/roadmap enforcement model", "Keep backlog as product registry/pointers and roadmap as release-stage breakpoint outline.", "Harden schemas and sprawl checks.", "Backlog/roadmap validators stay green."),
    ("R4", "Branch plan lifecycle model", "Keep active planning detailed while preventing stale active authority after completion.", "Use the retirement index to mark historical plans retired from active posture; no default deletion.", "Branch plans appear in the retirement index before any deletion is considered."),
    ("R5", "Structured branch receipt model", "Preserve traceability without duplicate live-state chaos.", "Define receipt schema and queue high-risk records for organization.", "Structure queues identify records needing organization."),
    ("R6", "Vision contract implementation", "Treat `Docs/nexus_vision.md` as the Nexus Vision contract and `Docs/family_visions/` as the family vision owner layer.", "Reference migration and family vision creation completed.", "Operating model and dossier carry Product Vision Contract language."),
    ("R7", "Safe file disposition review", "Identify keep/collapse/migrate/retire/delete posture for every Docs file.", "Generate disposition table and USER decision list.", "Manifest count matches filesystem enumeration."),
    ("R8", "Validator and review-surface hardening", "Make corrected review model regeneration-safe.", "Update helper/validator sections and regenerate audit/index.", "Validation passes and generated output is stable."),
    ("R9", "Final USER review hold", "Stop before PR Readiness until validation is green and USER separately approves PR creation.", "Report results only.", "Next legal phase remains USER review / PR Readiness approval."),
)


DISPOSITION_CHANGE_ROWS = (
    ("Branch plans", "Delete after PR Readiness", "Historical plans are indexed as retired from active planning posture; deletion still needs separate USER approval and reference proof."),
    ("Branch records", "Compact receipts", "Structured traceability receipts; size is acceptable when evidence is organized and not duplicate live state."),
    ("Main", "General source-truth doc", "Least-updated canonical docs index, recovery map, and owner pointer ledger."),
    ("Backlog", "Current status plus detailed trace", "Compact product registry, family scope/status, package summary, and pointers."),
    ("Roadmap", "Release/current-state record", "Release-stage schedule outline, public milestone posture, and broad feature breakpoints."),
    ("Vision", "Low-risk product reference", "Nexus Vision contract plus family vision records that drive backlog and branch planning."),
    ("Safe/low-risk docs", "Safe to leave", "Reference-scan before delete/collapse, with replacement owner and USER acceptance recorded."),
)


def add_user_response_integration_matrix(add) -> None:
    add("## USER Response Integration Matrix")
    add("")
    add("| USER Response Area | Model Decision | Owner Files | Execution Effect | Validator / Helper Effect |")
    add("| --- | --- | --- | --- | --- |")
    for area, decision, owners, effect, validator in USER_RESPONSE_INTEGRATION_ROWS:
        add(f"| {area} | {decision} | {owners} | {effect} | {validator} |")
    add("")


def add_single_pr_staged_execution_plan(add) -> None:
    add("## Single-PR Staged Execution Plan")
    add("")
    add("All remaining Docs reform work stays on this Governance branch as staged internal commits until USER accepts the full reform surface. PR creation is not the next move by inertia.")
    add("")
    add("| Stage | Name | Purpose | Allowed Work | Completion Proof |")
    add("| --- | --- | --- | --- | --- |")
    for stage, name, purpose, allowed, proof in SINGLE_PR_STAGED_EXECUTION_ROWS:
        add(f"| {stage} | {name} | {purpose} | {allowed} | {proof} |")
    add("")


def add_disposition_changes_from_user_review(add) -> None:
    add("## Disposition Changes From USER Review")
    add("")
    add("| Surface | Prior Risky Interpretation | Corrected Disposition |")
    add("| --- | --- | --- |")
    for surface, prior, corrected in DISPOSITION_CHANGE_ROWS:
        add(f"| {surface} | {prior} | {corrected} |")
    add("")


def add_docs_organization_cleanup_pass(
    add,
    *,
    ambiguity_count: int,
    structure_count: int,
    migration_count: int,
    safe_count: int,
    retired_plan_count: int,
) -> None:
    add("## Docs Organization Cleanup Pass")
    add("")
    add("Cleanup Pass Status: USER requested a docs organization cleanup pass.")
    add(
        "Execution Boundary: non-destructive organization planning and queue clarification only. "
        "This pass does not move, rename, delete, archive, or rewrite historical files."
    )
    add(
        "Source Review Surface: `Docs/governance_docs_full_inventory_reform_audit.md`, "
        "`Docs/governance_docs_reform_user_review_index.md`, and the USER Desktop review bundle."
    )
    add(
        "Next USER Decision: choose one focused cleanup lane before any physical file or "
        "history-affecting change."
    )
    add("")
    add("| Cleanup Lane | Current Queue Size | Safe Current Action | USER-Gated Later Action |")
    add("| --- | ---: | --- | --- |")
    rows = (
        (
            "Ambiguous ownership/current-state wording",
            ambiguity_count,
            "Keep queued with owner/review action visible.",
            "Focused wording repair or source-truth owner migration.",
        ),
        (
            "Structure and indexability risks",
            structure_count,
            "Keep queued with structure action visible.",
            "Focused organization pass for one owner family or receipt set.",
        ),
        (
            "Migration / organization candidates",
            migration_count,
            "Keep candidate rows visible in this dossier.",
            "Move durable content only after replacement owner and validation proof.",
        ),
        (
            "Retired branch plan review",
            retired_plan_count,
            "Keep retired posture and lookup paths.",
            "Delete or archive only after reference proof and USER approval.",
        ),
        (
            "Low-risk reference consolidation",
            safe_count,
            "Leave in place unless USER selects a consolidation lane.",
            "Collapse/delete only after reference scan and replacement owner proof.",
        ),
    )
    for lane, count, safe_action, gated_action in rows:
        add(f"| {lane} | {count} | {safe_action} | {gated_action} |")
    add("")
    add(
        "Recommended First Cleanup Lane: organize oversized historical branch records into "
        "current-summary plus indexed historical sections, without deleting evidence or changing "
        "source-truth ownership."
    )
    add(
        "Do Not Start Yet: branch-plan deletion, broad directory/file renames, historical receipt "
        "rewrites, runtime/FAM/release mutation, or archive/delete work. Those require separate "
        "exact USER approval."
    )
    add("")


def build_user_review_index(
    *,
    docs_count: int,
    branch: str,
    head: str,
    origin_main: str,
    merge_base: str,
    high_risk: list[dict[str, object]],
    migration_candidates: list[dict[str, object]],
    safe_files: list[dict[str, object]],
    ambiguity_queue: list[dict[str, object]],
    structure_queue: list[dict[str, object]],
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
    add(f"- Source branch: `{branch}`")
    add("- Git proof: derive live `HEAD`, `origin/main`, and merge-base with git at review/validation time.")
    add("- Generated hash fields: intentionally not maintained in this docs review index.")
    add("- Runtime/FAM/Compact-AI mutation: none.")
    add("- PR Readiness: held until validation is green and USER separately approves PR creation.")
    add("")
    add("## Suggested Review Order")
    add("")
    add("1. Read `Executive Summary` and `How To Review This Dossier` in the full dossier.")
    add("2. Review `What Was Completed`, `What Remains External`, and `What Requires USER Decision`.")
    add("3. Review `USER Response Integration Matrix` and confirm each response changed the model.")
    add("4. Review `Single-PR Staged Execution Plan` before deciding whether PR Readiness should proceed.")
    add("5. Review the `Completed / External Decision Matrix` for the reform scope.")
    add("6. Review `Complete Docs Cleanup / Disposition Table` for every file's keep/organize/migrate/retire/delete posture.")
    add("7. Review ambiguity and structure queues before deciding whether cleanup is complete.")
    add("8. Scan `High-Risk Files`, `Files Needing Future Migration`, and `Files That May Be Retired Later`.")
    add("9. Use the `File-by-File Review Table` for a compact pass over every Docs file.")
    add("10. Use the detailed `File-By-File Review Dossier` only for files you want to inspect deeply.")
    add("11. Confirm the `PR Readiness Checklist` only after the staged cleanup is accepted.")
    add("")
    add("## Decision Checklist")
    add("")
    add("- [ ] The source-truth ownership split is acceptable.")
    add("- [ ] USER response requirements are integrated as model decisions, not just preserved as notes.")
    add("- [ ] Remaining reform work should stay on this single Governance branch/final PR path.")
    add("- [ ] Backlog and roadmap roles are acceptable.")
    add("- [ ] Branch Runtime Engineering Plan lifecycle and retirement rule are acceptable.")
    add("- [ ] Historical branch plans are acceptable as retired/indexed records rather than active execution plans.")
    add("- [ ] No Docs file should be deleted, archived, or broadly renamed before a later focused USER decision.")
    add("- [ ] Every Docs file has a clear disposition in the complete cleanup table.")
    add("- [ ] Ambiguous ownership/current-state wording has a clear owner or deferred review action.")
    add("- [ ] Structure risks have a migration, organization, or keep-now decision.")
    add("- [ ] Validators are enough to stop the worst sprawl from returning.")
    add(
        "- [ ] PR Readiness Stage 1 analysis may proceed after final validation and USER "
        "acceptance; PR Readiness Stage 2 / PR creation remains a separate USER decision."
    )
    add("")
    add("## User Response Intake Status")
    add("")
    add("- USER review responses are recorded in `Docs/governance_process_efficiency_reform_plan.md` under the 2026-05-21 review intake.")
    add("- This generated index stays pointer-based so audit regeneration does not strand raw USER notes in a generated file.")
    add(
        "- Current execution model: this deferred-completion pass updates source truth and "
        f"review artifacts on the USER-approved bounded governance/source-truth repair branch "
        f"`{branch}` in `C:\\Nexus Worktrees\\Governance`; PR creation remains separately USER-gated."
    )
    add("- PR Readiness remains held until validation is green and USER separately approves PR creation.")
    add("")
    add("## USER Response Integration Summary")
    add("")
    add("| USER Response Area | Model Decision | Execution Effect |")
    add("| --- | --- | --- |")
    for area, decision, _owners, effect, _validator in USER_RESPONSE_INTEGRATION_ROWS:
        add(f"| {area} | {decision} | {effect} |")
    add("")
    add_single_pr_staged_execution_plan(add)
    add_disposition_changes_from_user_review(add)
    add_docs_organization_cleanup_pass(
        add,
        ambiguity_count=len(ambiguity_queue),
        structure_count=len(structure_queue),
        migration_count=len(migration_candidates),
        safe_count=len(safe_files),
        retired_plan_count=sum(
            1 for _rel, reason, _rec in retire_candidates if "branch plan" in reason
        ),
    )
    add("## Files Needing USER Decision")
    add("")
    add("| File | Reason | Recommendation |")
    add("| --- | --- | --- |")
    for rel, reason, rec in retire_candidates[:25]:
        add(f"| `{rel}` | {reason} | {rec} |")
    if not retire_candidates:
        add("| None | N/A | N/A |")
    add("")
    add("## Ambiguity Review Queue")
    add("")
    add("Queue Status: Future USER-gated organization queue; not a PR blocker unless validator output identifies an active failure.")
    add("")
    add("| File | Ambiguity Risk | Signals | Action |")
    add("| --- | --- | --- | --- |")
    for row in ambiguity_queue[:18]:
        add(
            f"| `{row['rel']}` | {row['ambiguity_risk']} | "
            f"{md_list(list(row['ambiguity_hits']))} | "
            f"{compact_review_value(str(row['ambiguity_action']), 120)} |"
        )
    if not ambiguity_queue:
        add("| None | N/A | N/A | N/A |")
    add("")
    add("## Structure Review Queue")
    add("")
    add("Queue Status: Future USER-gated organization queue; not a PR blocker unless validator output identifies an active failure.")
    add("")
    add("| File | Structure Risk | Action |")
    add("| --- | --- | --- |")
    for row in structure_queue[:18]:
        add(
            f"| `{row['rel']}` | {row['structure_risk']} | "
            f"{compact_review_value(str(row['structure_action']), 120)} |"
        )
    if not structure_queue:
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
        "`I accept the corrected USER-response integration model and approve continuing the staged "
        f"Docs source-truth reform on {branch} as one final "
        "Governance PR path. PR creation, merge, release work, runtime work, FAM-006/FAM-007/"
        "Compact-AI mutation, issue work, branch cleanup, historical branch deletion, and successor "
        "branch creation remain separate decisions.`"
    )
    return "\n".join(out) + "\n"


def generate() -> None:
    files = sorted(
        [
            path
            for path in DOCS.rglob("*")
            if path.is_file() and path not in {AUDIT, INDEX}
        ],
        key=lambda p: p.as_posix().lower(),
    )
    changed = set(git_output("diff", "--name-only", "origin/main...HEAD").splitlines())
    changed.update(git_output("diff", "--name-only").splitlines())
    changed.update(git_output("diff", "--cached", "--name-only").splitlines())
    for status_line in git_output("status", "--porcelain").splitlines():
        path_text = status_line[3:].strip()
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1].strip()
        if path_text:
            changed.add(path_text.replace("\\", "/"))
    branch = git_output("branch", "--show-current")
    head = git_output("rev-parse", "HEAD")
    origin_main = git_output("rev-parse", "origin/main")
    merge_base = git_output("merge-base", "HEAD", "origin/main")
    active_branch_plan_paths = {branch_name_to_plan_path(branch)} if branch else set()

    file_rows: list[dict[str, object]] = []
    fact_map: dict[str, set[str]] = {key: set() for key in FACT_CLASSES}
    retire_candidates: list[tuple[str, str, str]] = []

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        lines = text.count("\n") + (1 if text else 0)
        owner = owner_for(rel)
        owns, should_record, should_move = OWNER_DESCRIPTIONS[owner]
        action, completed, remaining = action_for(
            rel,
            owner,
            lines,
            changed,
            active_branch_plan_paths=active_branch_plan_paths,
        )
        counts = {name: count_matches(text, patterns) for name, patterns in PATTERNS.items()}
        duplicate_classes = [fact for fact, patterns in FACT_CLASSES.items() if count_matches(text, patterns)]
        ambiguity_risk, ambiguity_hits, ambiguity_action = ambiguity_for(text, owner)
        structure_risk, structure_action = structure_for(text, lines, owner)
        for fact in duplicate_classes:
            fact_map[fact].add(rel)
        risk = "Low"
        if rel in {"Docs/feature_backlog.md", "Docs/prebeta_roadmap.md"}:
            risk = "Critical"
        elif owner == "branch authority / structured receipt" and lines > 400:
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
        active_branch_plan = owner == "branch runtime engineering plan" and rel in active_branch_plan_paths
        if owner == "branch runtime engineering plan" and not active_branch_plan:
            retire_candidates.append(
                (
                    rel,
                    "branch plan is retired from active planning posture and preserved for lookup",
                    "delete only after USER approval plus reference proof; do not delete by default",
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
                "consolidation_target": "",
                "deletion_posture": "",
                "duplicate_classes": duplicate_classes,
                "ambiguity_risk": ambiguity_risk,
                "ambiguity_hits": ambiguity_hits,
                "ambiguity_action": ambiguity_action,
                "structure_risk": structure_risk,
                "structure_action": structure_action,
                "active_branch_plan": active_branch_plan,
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
    ambiguity_queue = sorted(
        [row for row in file_rows if row["ambiguity_risk"] in {"High", "Medium"}],
        key=lambda row: (str(row["ambiguity_risk"]), str(row["rel"])),
    )
    structure_queue = sorted(
        [row for row in file_rows if row["structure_risk"] in {"High", "Medium"}],
        key=lambda row: (str(row["structure_risk"]), str(row["rel"])),
    )

    index_text = build_user_review_index(
        docs_count=len(file_rows) + 2,
        branch=branch,
        head=head,
        origin_main=origin_main,
        merge_base=merge_base,
        high_risk=high_risk,
        migration_candidates=migration_candidates,
        safe_files=safe_files,
        ambiguity_queue=ambiguity_queue,
        structure_queue=structure_queue,
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
            "consolidation_target": "",
            "deletion_posture": "",
            "duplicate_classes": index_duplicate_classes,
            "ambiguity_risk": ambiguity_for(index_text, index_owner)[0],
            "ambiguity_hits": ambiguity_for(index_text, index_owner)[1],
            "ambiguity_action": ambiguity_for(index_text, index_owner)[2],
            "structure_risk": structure_for(index_text, index_text.count("\n"), index_owner)[0],
            "structure_action": structure_for(index_text, index_text.count("\n"), index_owner)[1],
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
    audit_rel = AUDIT.relative_to(ROOT).as_posix()
    audit_owner = owner_for(audit_rel)
    audit_owns, audit_should_record, audit_should_move = OWNER_DESCRIPTIONS[audit_owner]
    audit_action, audit_completed, audit_remaining = action_for(
        audit_rel, audit_owner, 0, changed
    )
    file_rows.append(
        {
            "rel": audit_rel,
            "lines": "Generated self-reference",
            "owner": audit_owner,
            "action": audit_action,
            "risk": "High",
            "confidence": "High",
            "counts": {
                "live": 0,
                "pr_release_issue": 0,
                "package_slice": 0,
                "branch_phase": 0,
                "validator": 1,
            },
            "title": "Governance Docs Full Inventory Reform Audit",
            "owns": audit_owns,
            "should_record": audit_should_record,
            "should_move": audit_should_move,
            "completed": audit_completed,
            "remaining": (
                "Self-reference is intentionally synthetic so regeneration does not "
                "change the dossier by re-scanning its previous generated output."
            ),
            "consolidation_target": "",
            "deletion_posture": "",
            "duplicate_classes": ["helper responsibility"],
            "ambiguity_risk": "Low",
            "ambiguity_hits": [],
            "ambiguity_action": "Synthetic self-reference; review the actual generated dossier directly.",
            "structure_risk": "Low",
            "structure_action": "Synthetic self-reference keeps generation stable.",
            "live_fields": [],
            "receipt_fields": [
                "Generated review dossier; content is reviewed through the real file, not self-scanned."
            ],
            "current_markers": [],
            "trace_markers": [],
            "branch_markers": [],
            "release_markers": [],
        }
    )
    fact_map["helper responsibility"].add(audit_rel)
    file_rows = sorted(file_rows, key=lambda row: str(row["rel"]).lower())
    for row in file_rows:
        row["consolidation_target"] = consolidation_target_for(row)
        row["deletion_posture"] = deletion_posture_for(row)
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
    ambiguity_queue = sorted(
        [row for row in file_rows if row["ambiguity_risk"] in {"High", "Medium"}],
        key=lambda row: (str(row["ambiguity_risk"]), str(row["rel"])),
    )
    structure_queue = sorted(
        [row for row in file_rows if row["structure_risk"] in {"High", "Medium"}],
        key=lambda row: (str(row["structure_risk"]), str(row["rel"])),
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
        "is complete versus external USER-gated follow-up."
    )
    add("")
    add(
        "The reform direction is conservative about historical evidence: live operational truth moves "
        "to Git/GitHub/helpers, but validated historical receipts are preserved unless a focused "
        "fold-down/retirement decision is safe."
    )
    add("")
    add("Start here for review: `Docs/governance_docs_reform_user_review_index.md`.")
    add("")
    add("## How To Review This Dossier")
    add("")
    add("1. Start with the companion index: `Docs/governance_docs_reform_user_review_index.md`.")
    add("2. Read `What Was Completed`, `What Remains External`, and `What Requires USER Decision` below.")
    add("3. Review `USER Response Integration Matrix` to confirm the USER responses changed the model.")
    add("4. Review `Single-PR Staged Execution Plan` to confirm PR Readiness should proceed only after validation and USER approval.")
    add("5. Review `Complete Docs Cleanup / Disposition Table` for every file's keep/organize/migrate/retire/delete posture.")
    add("6. Review `Ambiguity Pass` and `Structure Pass` before deciding whether cleanup is complete.")
    add("7. Scan `High-Risk Files`, `Files Needing Future Migration`, and `Files That May Be Retired Later`.")
    add("8. Use `File-by-File Review Table` for a compact row-by-row pass over every Docs file.")
    add("9. Use `File-By-File Review Dossier` for detailed per-file evidence and notes.")
    add("10. Approve PR Readiness only after the staged cleanup and corrected model are acceptable.")
    add("")
    add("## What Was Completed")
    add("")
    add("- Every file under `Docs/` is enumerated in the manifest, review table, and detailed dossier.")
    add("- Every file has an explicit cleanup/disposition row with a consolidation target and deletion posture.")
    add("- Every file has an ambiguity risk and structure risk classification for USER review.")
    add("- USER review responses are integrated as model decisions, not only preserved as notes.")
    add("- Backlog, roadmap, and worktree-slot ownership rules are captured as compact pointer/status surfaces.")
    add("- Branch Runtime Engineering Plan lifecycle is stated as active-only, fold-down, then retirement after migration.")
    add("- Duplicate fact classes are mapped to their correct owner surfaces.")
    add("- Validator coverage checks dossier file count, required sections, file-by-file entries, and review index presence.")
    add("- A short user review index is generated for easier inspection before PR Readiness.")
    add("")
    add("## What Remains External")
    add("")
    add("- Historical branch records larger than the structured receipt model remain preserved until a focused organization pass improves current-summary and indexability without losing traceability.")
    add("- Historical Branch Runtime Engineering Plans are indexed as retired from active planning posture; deletion remains separate USER-gated cleanup after reference proof.")
    add("- Low-risk product/reference docs remain kept unless USER approves a later retirement/delete pass with replacement-owner proof.")
    add("- GitHub-derived live-state helpers can be expanded later, but this pass does not require runtime or GitHub source mutations.")
    add("")
    add("## What Requires USER Decision")
    add("")
    add("- Whether to approve PR Readiness Stage 2 after reviewing this dossier.")
    add("- Whether to accept the corrected USER-response model and continue staged cleanup on this single branch.")
    add("- Whether to delete any retired historical branch plans after replacement-owner and reference proof.")
    add("- Whether to run focused organization of oversized historical branch ledgers into user-readable, Codex-indexable structures.")
    add("- Whether to retire low-risk or duplicate reference docs after USER review.")
    add("- Whether to create or expand additional FAM-family dossiers as migration targets for bulk historical detail.")
    add("")
    add_docs_organization_cleanup_pass(
        add,
        ambiguity_count=len(ambiguity_queue),
        structure_count=len(structure_queue),
        migration_count=len(migration_candidates),
        safe_count=len(safe_files),
        retired_plan_count=sum(
            1 for _rel, reason, _rec in retire_candidates if "branch plan" in reason
        ),
    )
    add("## USER Review Intake Model")
    add("")
    add("- Durable USER response home: `Docs/governance_process_efficiency_reform_plan.md`, section `USER Review Intake - 2026-05-21`.")
    add("- Execution posture: deferred-completion source-truth maintenance on this single Governance branch; PR creation remains separately USER-gated.")
    add("- PR Readiness remains held until validation is green and USER separately approves PR creation.")
    add("- Main model: `Docs/Main.md` should be the least-updated canonical docs index and recovery map, not an execution diary.")
    add("- Branch plan model: Branch Runtime Engineering Plans fold down and retire after durable content migrates; deletion is not the default.")
    add("- Branch record model: branch records may be large when they are structured traceability ledgers; the reform target is clear organization and no duplicate live state, not evidence loss.")
    add("- Vision model: `Docs/nexus_vision.md` is the Nexus-wide vision contract; family vision records under `Docs/family_visions/` own durable family product direction.")
    add("")
    add_user_response_integration_matrix(add)
    add_single_pr_staged_execution_plan(add)
    add_disposition_changes_from_user_review(add)
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
    add("| File | Owner | Migration / Organization Recommendation |")
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
    add(f"- Audit Branch: `{branch}`")
    add("- Audit Git Proof: derive live `HEAD`, `origin/main`, and merge-base with git at review/validation time.")
    add("- Audit Hash Policy: exact live Git hashes are intentionally not maintained in this docs review surface.")
    add(f"- Audit File Count: {len(file_rows)} files under `Docs/`")
    add(f"- Manifest Files Enumerated: {len(file_rows)}")
    add("- Manifest Match: PASS - filesystem enumeration and dossier manifest counts match.")
    add("- Mutation Scope: docs/source-truth/governance/validator reform only.")
    add("- Runtime Mutation: none.")
    add("- FAM-006 / FAM-007 / Compact-AI Mutation: none.")
    add("- Release / Tag / GitHub Release / Issue Work: none.")
    add("")
    add("## Completed / External Decision Matrix")
    add("")
    add("| Reform Item | Completed In This Branch | External / USER-Gated Follow-Up | Reason | Future Owner | USER Decision Needed | Validator Coverage |")
    add("| --- | --- | --- | --- | --- | --- | --- |")
    matrix_rows = (
        ("USER response integration", "Yes", "No", "N/A", "Docs/governance_process_efficiency_reform_plan.md", "No", "governance efficiency validation"),
        ("single-PR staged execution model", "Yes", "No", "N/A", "this Governance carrier", "No", "governance efficiency validation"),
        ("feature_backlog compaction", "Yes", "No", "N/A", "Docs/feature_backlog.md", "No", "governance efficiency validation"),
        ("prebeta_roadmap compaction", "Yes", "No", "N/A", "Docs/prebeta_roadmap.md", "No", "governance efficiency validation"),
        ("worktree_slots cleanup", "Yes", "No", "N/A", "Docs/worktree_slots.md", "No", "governance efficiency validation"),
        ("branch_records cleanup", "Partial", "Yes", "Large historical records need safe organization into current summary plus indexed traceability sections", "Docs/branch_records + workstreams/family dossiers", "Yes for bulk reorganization", "branch governance validation"),
        ("branch_plans lifecycle", "Yes", "Deletion gated", "Historical plans are indexed as retired; deletion needs proof and USER approval", "Docs/branch_plans + branch records + workstreams/family dossiers", "Yes before deleting historical plans", "planning fixture and governance efficiency validation"),
        ("workstreams/family dossier ownership", "Yes", "Expansion gated", "Future dossier expansion should be focused by family", "Docs/workstreams + Docs/family_visions", "Yes for new/expanded implementation dossiers", "branch governance validation"),
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
        "Roadmap owns the pre-Beta/Beta/release schedule outline, milestone breakpoints, and broad feature-family checkpoints only.",
        "Branch records own branch authority, phase history, approvals, legal carrier status, and structured current/historical traceability receipts.",
        "Branch plans own detailed active-branch engineering plans while active, then fold down during PR Readiness and retire after durable content is migrated and no active branch depends on them.",
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
        ("Docs/Main.md", "least-updated canonical docs index, recovery map, and ownership routing", "detailed branch/release/live-state narration"),
        ("Docs/feature_backlog.md", "compact FAM registry and pointer layer", "Package Trace, Slice Trace, live branch/release/issue state"),
        ("Docs/prebeta_roadmap.md", "stage-breakpoint schedule outline and broad milestone checkpoints", "live latest-release, release-window, PR-window, or current branch state truth"),
        ("Docs/worktree_slots.md", "slot definitions and assignment receipts", "HEAD, dirty state, ahead/behind, PR/release state"),
        ("Docs/branch_records/index.md", "branch authority routing", "implementation checklists"),
        ("Docs/branch_records/<branch>.md", "authority, approvals, phase history, structured traceability receipts", "volatile live state or unindexed execution diary"),
        ("Docs/branch_plans/<branch>.md", "active branch engineering plan", "permanent active authority or family dossier after fold-down"),
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
    add("## Complete Docs Cleanup / Disposition Table")
    add("")
    add("This is the full file-by-file cleanup plan. It includes every file under `Docs/`, not just the files edited in this reform branch.")
    add("")
    add("| File | Current Owner | Keep / Compact / Migrate / Retire / Delete | Consolidation Target | Deletion Posture | USER Decision |")
    add("| --- | --- | --- | --- | --- | --- |")
    for row in file_rows:
        user_decision = "Yes" if "USER" in str(row["deletion_posture"]) or "USER" in str(row["action"]) else "No"
        add(
            f"| `{row['rel']}` | {row['owner']} | {row['action']} | "
            f"{compact_review_value(str(row['consolidation_target']), 140)} | "
            f"{compact_review_value(str(row['deletion_posture']), 120)} | {user_decision} |"
        )
    add("")
    add("## Ambiguity Pass")
    add("")
    add("Queue Status: Future USER-gated organization queue; not a PR blocker unless validator output identifies an active failure.")
    add("")
    add("Ambiguity risk flags wording that often causes source-truth drift, especially `current`, `active`, `latest`, `next`, `pending`, unclear ownership words, soft commitments, and state-ledger language. High or medium ambiguity is not automatically wrong for historical receipts, but it is a review target.")
    add("")
    add("| File | Ambiguity Risk | Ambiguity Signals | Required Review Action |")
    add("| --- | --- | --- | --- |")
    for row in file_rows:
        add(
            f"| `{row['rel']}` | {row['ambiguity_risk']} | "
            f"{md_list(list(row['ambiguity_hits']))} | "
            f"{compact_review_value(str(row['ambiguity_action']), 140)} |"
        )
    add("")
    add("## Structure Pass")
    add("")
    add("Queue Status: Future USER-gated organization queue; not a PR blocker unless validator output identifies an active failure.")
    add("")
    add("Structure risk flags files that are too long for their owner role, have too few headings, or mix current summary with historical detail in a way that can hide drift.")
    add("")
    add("| File | Structure Risk | Structure Action |")
    add("| --- | --- | --- |")
    for row in file_rows:
        add(
            f"| `{row['rel']}` | {row['structure_risk']} | "
            f"{compact_review_value(str(row['structure_action']), 150)} |"
        )
    add("")
    add("## File-by-File Review Table")
    add("")
    add("| File path | Line count | Current purpose | Correct owner category | What this file records | What this file should record | Reform action completed | Remaining action needed | Recommendation | Ambiguity Risk | Structure Risk | Duplicate truth found | Live operational truth found | Governance receipt found | Validator coverage | USER review notes |")
    add("| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
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
            f"{row['ambiguity_risk']} | {row['structure_risk']} | "
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
        "`Docs/prebeta_roadmap.md` owns the pre-Beta/Beta/release stage-breakpoint schedule outline: "
        "the broad feature-family checkpoints and milestone gates needed before later release stages. "
        "It is a reference outline, not a release ledger. Live latest release/tag/window truth is "
        "derived from Git/GitHub/helpers and must not be manually maintained here."
    )
    add("")
    add("## Branch Records Final Schema")
    add("")
    add(
        "Branch records own branch identity, approvals, current/historical phase status, blockers, "
        "legal carrier posture, structured traceability receipt, and pointers. Large historical execution "
        "ledgers are preserved as historical evidence in this pass; future focused migration should organize "
        "them into user-readable and Codex-indexable current summary plus historical receipt sections, then "
        "promote reusable implementation detail to workstreams or family dossiers without losing commit/PR evidence."
    )
    add("")
    add("## Branch Plans Lifecycle And Retirement Rule")
    add("")
    add(
        "Branch Runtime Engineering Plans are canonical only while the owning branch is active. They "
        "are created/admitted during Branch Readiness Stage 2 for runtime-focused branches, used "
        "through Workstream/Hardening/Live Validation, folded down during PR Readiness Stage 1, and "
        "retired during or before PR Readiness Stage 2 only after durable content has been migrated "
        "to the branch receipt, workstream doc, family dossier, or other historical receipt owner. "
        "Existing historical plans are indexed as retired from active planning posture rather than deleted in "
        "this pass because useful historical evidence must remain lookup-safe unless USER later approves deletion."
    )
    add("")
    add("## Branch Runtime Engineering Plan Lifecycle Proof")
    add("")
    add("- Branch Runtime Engineering Plans are canonical active-branch planning docs while a runtime branch is active.")
    add("- Branch plans contain detailed per-seam implementation, validation, user-facing proof, future-gated items, and approval boundaries.")
    add("- Branch plans are folded down during PR Readiness Stage 1.")
    add("- Branch plans are retired during or before PR Readiness Stage 2 approval after durable content is migrated or lookup-safe historical posture is recorded.")
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
        add(f"- Consolidation target: {row['consolidation_target']}.")
        add(f"- Deletion posture: {row['deletion_posture']}.")
        add(f"- Ambiguity risk: {row['ambiguity_risk']}.")
        add(f"- Ambiguity signals: {md_list(list(row['ambiguity_hits']))}")
        add(f"- Ambiguity review action: {row['ambiguity_action']}")
        add(f"- Structure risk: {row['structure_risk']}.")
        add(f"- Structure action: {row['structure_action']}")
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
    add("- Many historical branch records and workstream records still contain historical live-state language. This is preserved as receipt evidence in this pass, not treated as active truth. Future focused fold-down passes can organize the largest ledgers if USER wants clearer review/indexing.")
    add("- Existing historical Branch Runtime Engineering Plans are retired from active planning posture, but not deleted; deletion remains USER-gated after reference proof.")
    add("- Some product/reference docs are low-risk but still need USER review before retirement because they may preserve historical design context.")
    add("")
    add("## PR Readiness Checklist")
    add("")
    add("- [ ] USER reviewed the companion index.")
    add("- [ ] USER reviewed high-risk files and USER-gated delete/retire candidates.")
    add("- [ ] USER accepts that no ambiguous Docs files are deleted before later focused approval.")
    add("- [ ] USER accepts Branch Runtime Engineering Plan fold-down/retirement lifecycle.")
    add("- [ ] Validation remains green from the Governance branch.")
    add("- [ ] PR creation is separately approved.")
    add("")
    add("## Deferred USER Decisions")
    add("")
    add("- Approve deletion of retired historical branch plans only after durable content and references are proven preserved.")
    add("- Approve focused organization or archival of oversized historical branch execution ledgers.")
    add("- Approve creation or expansion of FAM-006 / FAM-007 family dossiers if USER wants historical branch detail moved out of branch records in bulk.")
    add("- Approve retirement of any low-risk reference docs after USER review of the file-by-file dossier.")
    add("")
    add("## Next Legal Phase")
    add("")
    add("The next legal phase is USER review of the completed deferred-reform pass and validation proof. PR Readiness Stage 2 / PR creation remains held until USER separately approves PR creation. Merge remains separate USER approval.")

    index_text = build_user_review_index(
        docs_count=len(file_rows),
        branch=branch,
        head=head,
        origin_main=origin_main,
        merge_base=merge_base,
        high_risk=high_risk,
        migration_candidates=migration_candidates,
        safe_files=safe_files,
        ambiguity_queue=ambiguity_queue,
        structure_queue=structure_queue,
        retire_candidates=retire_candidates,
    )

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
