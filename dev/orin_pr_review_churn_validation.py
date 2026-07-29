# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=pr-review-churn-validation; status=shared
"""Validate local PR review-churn prevention before re-requesting Codex review.

This helper intentionally treats GitHub/Codex Connector data as live evidence,
not durable repo truth. The durable part is the local review-churn matrix fixture:
it records which parser/helper/validator families must have source-truth,
implementation, fixture, and generated sibling-mutation coverage.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = (
    ROOT
    / "dev"
    / "fixtures"
    / "pr_review_churn"
    / "pr_276_rar_review_churn_matrix.json"
)
DEFAULT_TOTAL_COMMENT_BUDGET = 12
DEFAULT_SAME_FAMILY_COMMENT_BUDGET = 3
CONNECTOR_LOGINS = {"chatgpt-codex-connector", "codex"}
CLASSIFIER_CONTEXT_KEYWORDS = (
    "rar",
    "rebaseline",
    "adoption",
    "review churn",
    "churn gate",
    "review-comment",
    "review comment",
    "codex connector",
    "pr readiness",
    "uiref",
    "code-to-visual",
    "visual acceptance",
)
GENERIC_CLASSIFIER_KEYWORDS = {
    "status",
    "case",
    "row",
    "table",
    "blocked",
    "resolved",
    "unresolved",
    "visual",
    "green",
    "primary decision surface",
    "decision surface",
    "although",
    "though",
    "while",
    "blocked",
    "not blocked",
}
HELPER_FILE_PATTERNS = (
    "validation",
    "validator",
    "helper",
    "parser",
    "bundle",
    "audit",
    "harness",
)
FIREWALL_GATED_PATHS = {
    "docs/branch_plans/readme.md",
    "docs/branch_records/feature_release_readiness_source_truth_intake.md",
    "docs/incident_patterns.md",
    "docs/phase_governance.md",
    "docs/validation_helper_registry.md",
}
FIREWALL_GATED_PREFIXES = (
    "dev/fixtures/branch_readiness_planning/",
    "dev/fixtures/pr_review_churn/",
    "docs/ui_reference_catalog/",
)
PYTHON_COMMAND_TOKENS = {"{python}", "{python_executable}"}
REPO_LIVE_STATE_CURRENT_CYCLE_CONTEXT = (
    "rri",
    "external state",
    "external-state",
    "external operational state",
    "external branch state",
    "c:\\nexus governance state",
    "repo live-state",
    "repo live state",
    "standing governance",
    "active rri cycle",
    "latest closed rri cycle",
    "return digest status",
    "release window",
    "release candidate anchor",
    "target commit",
)


@dataclass(frozen=True)
class FamilyRule:
    family_id: str
    keywords: tuple[str, ...]


FAMILY_RULES: tuple[FamilyRule, ...] = (
    FamilyRule(
        "external-state-transaction-evidence-parser",
        (
            "target-set journal",
            "modern journal",
            "committed journal",
            "malformed journal",
            "modern lock",
            "snapshot evidence",
            "snapshot hash",
            "before text",
            "before sha256",
            "after sha256",
            "transaction state",
            "target-scoped currentness",
            "audit_log",
            "audit root",
            "audit-root",
        ),
    ),
    FamilyRule(
        "durable-carrier-confinement-parser",
        (
            "durable carrier",
            "durable receipt",
            "historical carrier",
            "historical-receipt classifier",
            "receipt subsection heading",
            "durable authority pointer",
        ),
    ),
    FamilyRule(
        "fam003-settings-focus-routing",
        (
            "residentaccesssettingsdialog",
            "set_focus",
            "settings focus",
            "focus target",
            "focus targets",
            "focus=\"tray_visibility\"",
            "focus=\"ai_status\"",
            "focus=\"privacy\"",
            "focus=\"owner_routes\"",
            "tray_visibility",
            "ai_status",
            "owner_routes",
            "quick_access",
            "quick access editor",
            "tray help",
            "settings page",
            "tray parent",
        ),
    ),
    FamilyRule(
        "fam003-native-tray-submenu-winapi",
        (
            "native tray",
            "tray icon",
            "quick access/ai native submenus",
            "createpopupmenu",
            "appendmenuw",
            "trackpopupmenu",
            "hmenu",
            "uint_ptr",
            "mf_popup",
            "submenu handle",
            "handle-sized",
            "ctypes",
        ),
    ),
    FamilyRule(
        "rar-status-green-parser",
        (
            "status",
            "nonconforming",
            "unproven",
            "green",
            "case",
            "disposition",
            "resolved",
            "no applicable impact",
        ),
    ),
    FamilyRule(
        "rar-phase-advancement-parser",
        (
            "normal phase",
            "phase progression",
            "workstream",
            "blocked",
            "not blocked",
            "although",
            "though",
            "while",
            "next legal phase",
            "phase advancement",
            "release impact",
            "continue to pr readiness",
            "proceed to pr readiness",
            "advance to pr readiness",
            "continue to workstream",
            "proceed to workstream",
            "advance to workstream",
        ),
    ),
    FamilyRule(
        "rar-issue-candidate-disposition-parser",
        (
            "issue-candidate",
            "issue candidate",
            "github issue",
            "candidate row",
            "disposition marker",
            "user-reviewed",
            "reviewed packet",
        ),
    ),
    FamilyRule(
        "rar-issue-candidate-durability-parser",
        (
            "external-ledger candidate",
            "external ledger candidate",
            "external rar issue candidate",
            "carrying external candidates",
            "carried candidates",
            "candidate_id in primary_row_ids",
            "primary row",
            "primary packet",
            "candidate disappearance",
            "candidate disappeared",
            "disappeared from active packet",
            "rar issue candidate disappeared",
            "renamed-candidate disappearance",
            "regrouped/renamed-candidate",
            "external rar candidate",
            "active packet",
            "predecessor/successor lineage",
            "candidate lineage",
            "no current user decision",
            "no-decision",
            "proof negation",
            "receipt negation",
            "carrier acceptance",
            "acceptance receipt",
            "independent verification",
            "reason and scope",
        ),
    ),
    FamilyRule(
        "rar-user-packet-proof-parser",
        (
            "user packet",
            "user review packet",
            "packet path",
            "packet zip",
            "zip path",
            "timestamped zip",
            "folder label",
            "zip label",
            "user judgment",
            "user adjudication",
            "user review required",
            "route selection",
            "helper-output",
            "helper output",
            "chat-digest",
            "chat digest",
            "primary user decision",
            "primary decision surface",
            "primary surface",
            "decision surface",
            "review aid",
            "review aids",
            "copied table",
            "copied context",
            "nested path",
            "nested review",
            "active gate",
        ),
    ),
    FamilyRule(
        "rar-code-to-visual-reference-parser",
        (
            "code-to-visual",
            "accepted reference",
            "comparator",
            "missing proof",
            "proof surface",
            "noop",
            "no-op",
            "named material surface",
            "visual match",
            "behavior match",
            "visual",
        ),
    ),
    FamilyRule(
        "visual-acceptance-proof-chain-parser",
        (
            "visual acceptance",
            "visual acceptance target",
            "accepted reference set",
            "comparative synthesis",
            "visual family relation",
            "implementation authority",
            "authority classification",
            "authority value",
            "reference-derived implementation",
            "implementation match proof",
            "pre-live visual purpose conformance",
            "packet reviewability",
            "product acceptance",
            "screenshot-green",
            "screenshot green",
            "helper green",
            "validator green",
            "template claim",
            "template wording",
            "ai control center template",
            "not approved but",
            "template consumer contract",
            "consumer contract",
            "shared primitive",
            "functionality role",
            "role ambiguous",
        ),
    ),
    FamilyRule(
        "rar-table-row-parser",
        (
            "table",
            "row",
            "separator",
            "malformed",
            "overwide",
            "sparse",
            "header",
            "actual table",
        ),
    ),
    FamilyRule(
        "rar-path-suffix-parser",
        (
            "suffix",
            "punctuation",
            "wrapper",
            ".tmp",
            ".md",
            ".zip",
            "inline-code",
            "terminal punctuation",
            "traversal",
        ),
    ),
    FamilyRule(
        "rar-short-marker-parser",
        (
            "canonical short",
            "short marker",
            "short values",
            "bare rar3",
            "rar stage",
            "too shallow",
        ),
    ),
    FamilyRule(
        "repo-live-state-boundary-parser",
        (
            "repo live-state",
            "live-state tracking",
            "live adoption ledger in repo",
            "repo live state",
            "repo doc",
            "repo branch record",
            "repo branch records",
            "external mirror",
            "external branch state",
            "external active-cycle state",
            "external active cycle",
            "external rri gate",
            "c:\\nexus governance state",
            "active rri cycle",
            "current cycle",
            "latest closed rri cycle",
            "return digest status",
            "release candidate anchor",
            "target commit",
            "candidate includes later governance repairs",
            "current fetched origin/main",
            "standing governance",
            "worktree confinement",
            "active thread owner",
            "thread assignment status",
            "intended write set",
            "transition-legal active records",
            "transition legal active records",
        ),
    ),
    FamilyRule(
        "pr2-thread-pagination-and-approval-latch",
        (
            "review thread",
            "unresolved",
            "outdated",
            "resolved",
            "current head",
            "thumbs-up",
            "approval latch",
            "all pages",
            "pagination",
        ),
    ),
    FamilyRule(
        "pr2-comment-family-classifier",
        (
            "comment-family",
            "comment family",
            "family matching",
            "substring matcher",
            "unknown observed families",
            "covered family",
            "matrix",
            "churn gate",
            "review-churn budget",
            "review churn budget",
            "same-family budget",
            "same family budget",
            "total budget",
            "root-cause receipt",
            "root cause receipt",
            "pre-pr firewall",
            "pre pr firewall",
            "adversarial firewall",
            "portable python",
            "python launcher",
            "windows py launcher",
            "validation command",
            "validation_commands",
            "current interpreter",
            "changed-family",
            "changed family",
            "fixture-only",
            "fixture only",
        ),
    ),
    FamilyRule(
        "pr-readiness-review-risk-parser",
        (
            "pr readiness packet",
            "pr-readiness packet",
            "pr readiness field",
            "pr-readiness field",
            "review-risk coverage",
            "review risk coverage",
            "stage 1 packet",
            "stage 2 packet",
            "pr readiness",
        ),
    ),
)


def _run(args: list[str], *, stdin: str | None = None) -> str:
    result = subprocess.run(
        args,
        input=stdin,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"{' '.join(args)} failed with exit {result.returncode}: {result.stderr.strip()}"
        )
    return result.stdout


def _run_for_status(args: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            args,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
            check=False,
        )
    except FileNotFoundError as exc:
        return 127, str(exc)
    output = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    if stderr:
        output = f"{output}\n{stderr}".strip()
    return result.returncode, output


def _resolve_manifest_command(command: list[str]) -> list[str]:
    return [
        sys.executable if part.casefold() in PYTHON_COMMAND_TOKENS else part
        for part in command
    ]


def _python_manifest_command_uses_portable_token(command: list[str]) -> bool:
    if not any(part.replace("\\", "/").casefold().endswith(".py") for part in command):
        return True
    return bool(command) and command[0].casefold() in PYTHON_COMMAND_TOKENS


def _split_repo(repo: str) -> tuple[str, str]:
    if "/" not in repo:
        raise ValueError("--repo must be OWNER/NAME")
    owner, name = repo.split("/", 1)
    return owner, name


def _graphql(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"query": query, "variables": variables})
    raw = _run(["gh", "api", "graphql", "--input", "-"], stdin=payload)
    data = json.loads(raw)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]


def _rest_paginated_pages(path: str) -> tuple[list[dict[str, Any]], int]:
    raw = _run(
        [
            "gh",
            "api",
            "--paginate",
            "--slurp",
            "-H",
            "Accept: application/vnd.github+json",
            path,
        ]
    )
    pages = json.loads(raw)
    items: list[dict[str, Any]] = []
    for page in pages:
        if isinstance(page, list):
            items.extend(page)
    return items, len(pages)


def _rest_paginated(path: str) -> list[dict[str, Any]]:
    items, _ = _rest_paginated_pages(path)
    return items


def _fetch_review_threads(
    owner: str, name: str, number: int
) -> tuple[dict[str, Any], list[dict[str, Any]], int]:
    query = """
query($owner:String!,$name:String!,$number:Int!,$cursor:String){
  repository(owner:$owner,name:$name){
    pullRequest(number:$number){
      headRefOid
      mergeable
      mergeStateStatus
      reviewDecision
      reviewThreads(first:100, after:$cursor){
        totalCount
        pageInfo{hasNextPage endCursor}
        nodes{
          id
          isResolved
          isOutdated
        }
      }
    }
  }
}
"""
    cursor: str | None = None
    threads: list[dict[str, Any]] = []
    pull_request: dict[str, Any] | None = None
    page_count = 0
    total_count = 0
    while True:
        data = _graphql(
            query,
            {"owner": owner, "name": name, "number": number, "cursor": cursor},
        )
        pull_request = data["repository"]["pullRequest"]
        page = pull_request["reviewThreads"]
        total_count = int(page["totalCount"])
        page_count += 1
        threads.extend(page["nodes"])
        page_info = page["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]
    assert pull_request is not None
    if len(threads) != total_count:
        raise RuntimeError(
            f"reviewThreads pagination returned {len(threads)} of {total_count} threads"
        )
    return pull_request, threads, page_count


def _load_matrix(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _normalize(text: str) -> str:
    base = re.sub(r"\s+", " ", text.casefold()).strip()
    separator_normalized = re.sub(r"[-_/]+", " ", base)
    return f"{base} {separator_normalized}".strip()


def _is_connector_login(login: str) -> bool:
    normalized = login.casefold().removesuffix("[bot]")
    return normalized in CONNECTOR_LOGINS


def _classify_comment(body: str) -> list[str]:
    normalized = _normalize(body)
    has_classifier_context = any(
        keyword in normalized for keyword in CLASSIFIER_CONTEXT_KEYWORDS
    )
    families: list[str] = []
    for rule in FAMILY_RULES:
        matched_keywords = [
            keyword for keyword in rule.keywords if keyword in normalized
        ]
        if rule.family_id == "repo-live-state-boundary-parser":
            matched_keywords = [
                keyword
                for keyword in matched_keywords
                if keyword != "current cycle"
                or any(
                    context_keyword in normalized
                    for context_keyword in REPO_LIVE_STATE_CURRENT_CYCLE_CONTEXT
                )
            ]
        if not matched_keywords:
            continue
        strong_keywords = [
            keyword
            for keyword in matched_keywords
            if keyword not in GENERIC_CLASSIFIER_KEYWORDS
        ]
        if strong_keywords or (has_classifier_context and len(matched_keywords) >= 2):
            families.append(rule.family_id)
    exact_scope_families = [
        family
        for family in families
        if family
        in {
            "external-state-transaction-evidence-parser",
            "durable-carrier-confinement-parser",
        }
    ]
    if exact_scope_families:
        return exact_scope_families
    return families or ["unknown"]


def _classifier_guardrail_failures() -> list[str]:
    failures: list[str] = []
    external_transaction_comment = (
        "Reject a modern Committed journal when snapshot evidence or the released "
        "lock does not prove the exact target-set journal."
    )
    if _classify_comment(external_transaction_comment) != [
        "external-state-transaction-evidence-parser"
    ]:
        failures.append(
            "External-state transaction evidence comment did not classify into its exact family"
        )
    durable_carrier_comment = (
        "Reject a Durable Carrier Admission Receipt when the durable receipt omits "
        "complete confinement markers."
    )
    if _classify_comment(durable_carrier_comment) != [
        "durable-carrier-confinement-parser"
    ]:
        failures.append(
            "Durable carrier confinement comment did not classify into its exact family"
        )
    unrelated = "A database migration status row has mixed case after cleanup."
    if _classify_comment(unrelated) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched unrelated status/case/row wording"
        )
    classifier_comment = (
        "Tighten comment-family matching so an unrelated comment containing status "
        "or row does not pass as a covered family in the churn gate matrix."
    )
    if "pr2-comment-family-classifier" not in _classify_comment(classifier_comment):
        failures.append(
            "Comment-family classifier did not classify the classifier guardrail family"
        )
    same_family_budget_comment = (
        "Allow same-family-only churn receipts when the same-family budget is exceeded "
        "even if the total budget is still within limit."
    )
    if "pr2-comment-family-classifier" not in _classify_comment(
        same_family_budget_comment
    ):
        failures.append(
            "Comment-family classifier did not classify same-family budget receipt drift"
        )
    total_budget_comment = (
        "Allow total-only churn receipts when the total budget is exceeded even if no "
        "single family exceeds the same-family budget."
    )
    if "pr2-comment-family-classifier" not in _classify_comment(total_budget_comment):
        failures.append(
            "Comment-family classifier did not classify total budget receipt drift"
        )
    standalone_unknown = "An unrelated validator message contains the word unknown."
    if _classify_comment(standalone_unknown) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched standalone unknown wording"
        )
    unrelated_decision_surface = "A settings or migration decision surface changed during backend cleanup."
    if _classify_comment(unrelated_decision_surface) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched unrelated decision-surface wording"
        )
    visual_comment = (
        "A Code-To-Visual row records Visual Match as Mismatch and Behavior Match "
        "as Unproven while status says CONFORMING."
    )
    if "rar-code-to-visual-reference-parser" not in _classify_comment(visual_comment):
        failures.append(
            "Comment-family classifier did not classify code-to-visual comparison drift"
        )
    visual_acceptance_comment = (
        "Reject screenshot-green Visual Acceptance Target claims because packet "
        "reviewability, helper green, and a template claim cannot prove product "
        "acceptance without an accepted reference set and implementation match proof."
    )
    if "visual-acceptance-proof-chain-parser" not in _classify_comment(
        visual_acceptance_comment
    ):
        failures.append(
            "Comment-family classifier did not classify visual acceptance proof-chain drift"
        )
    visual_role_comment = (
        "The diagnostics surface is role ambiguous because the Functionality Role "
        "Contract and Implementation Authority table do not distinguish the child "
        "window from the AI Dashboard comparator."
    )
    if "visual-acceptance-proof-chain-parser" not in _classify_comment(
        visual_role_comment
    ):
        failures.append(
            "Comment-family classifier did not classify visual acceptance role-contract drift"
        )
    authority_contract_comment = (
        "Require exactly one authority classification and require the template "
        "consumer contract when Implementation Template Instantiated is claimed."
    )
    if "visual-acceptance-proof-chain-parser" not in _classify_comment(
        authority_contract_comment
    ):
        failures.append(
            "Comment-family classifier did not classify visual acceptance authority-contract drift"
        )
    unrelated_screenshot = "A screenshot filename changed during a docs cleanup pass."
    if _classify_comment(unrelated_screenshot) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched unrelated screenshot wording"
        )
    durability_comment = (
        "Require candidate lineage before carrying external candidates from the "
        "current external-ledger candidate into the primary packet."
    )
    if "rar-issue-candidate-durability-parser" not in _classify_comment(
        durability_comment
    ):
        failures.append(
            "Comment-family classifier did not classify RAR issue-candidate durability lineage drift"
        )
    disappeared_comment = (
        "RAR Issue Candidate Disappeared From Active Packet after packet "
        "regeneration; candidate disappearance must be treated as durability "
        "parser coverage, not only a disposition wording issue."
    )
    if "rar-issue-candidate-durability-parser" not in _classify_comment(
        disappeared_comment
    ):
        failures.append(
            "Comment-family classifier did not classify active-packet disappearance blocker wording"
        )
    no_decision_proof_comment = (
        "Because validate_text concatenates Proposed Carrier with Exact USER Decision, "
        "No current USER decision is needed because independent verification revalidated "
        "the repair can false-red when broad proof negation sees the leading No."
    )
    if "rar-issue-candidate-durability-parser" not in _classify_comment(
        no_decision_proof_comment
    ):
        failures.append(
            "Comment-family classifier did not classify no-decision proof negation drift"
        )
    no_decision_receipt_comment = (
        "Scope receipt negation away from no-decision wording because carrier "
        "acceptance receipt recorded is valid routed-disposition proof."
    )
    if "rar-issue-candidate-durability-parser" not in _classify_comment(
        no_decision_receipt_comment
    ):
        failures.append(
            "Comment-family classifier did not classify no-decision receipt negation drift"
        )
    helper_output_comment = (
        "Reject helper-output decision tables as primary. START_HERE routes "
        "to helper output or chat digest, so the packet has no real primary "
        "USER Review decision surface and the active gate can pass."
    )
    helper_output_families = _classify_comment(helper_output_comment)
    if "rar-user-packet-proof-parser" not in helper_output_families:
        failures.append(
            "Comment-family classifier did not classify helper-output/chat-digest primary packet drift"
        )
    nested_review_copy_comment = (
        "Exclude nested review-aid/context copies from primary surfaces. "
        "When a packet has no active USER Review decision file but a copied "
        "table sits under a nested path like Review Aids/USER Review or "
        "Source Truth Context/USER Review, it must not satisfy the primary "
        "USER decision surface."
    )
    if "rar-user-packet-proof-parser" not in _classify_comment(
        nested_review_copy_comment
    ):
        failures.append(
            "Comment-family classifier did not classify nested review-aid/context primary packet drift"
        )
    unrelated_lineage = "A migration lineage match failed for a database seed."
    if _classify_comment(unrelated_lineage) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched unrelated lineage wording"
        )
    pr_readiness_comment = (
        "A PR Readiness packet is missing review-risk coverage for another "
        "PR-readiness field."
    )
    pr_readiness_families = _classify_comment(pr_readiness_comment)
    if "pr-readiness-review-risk-parser" not in pr_readiness_families:
        failures.append(
            "Comment-family classifier did not classify generic PR Readiness review-risk drift"
        )
    if "rar-phase-advancement-parser" in pr_readiness_families:
        failures.append(
            "Comment-family classifier overmatched generic PR Readiness drift as RAR phase advancement"
        )
    rar_pr_readiness_advance_comment = (
        "Reject RAR wording that says waiver not approved so continue to "
        "PR Readiness while adoption remains active."
    )
    rar_pr_readiness_advance_families = _classify_comment(
        rar_pr_readiness_advance_comment
    )
    if "rar-phase-advancement-parser" not in rar_pr_readiness_advance_families:
        failures.append(
            "Comment-family classifier did not classify RAR continue-to-PR-Readiness advancement"
        )
    current_head_latch_comment = (
        "Current-head green proof accepted even though a later Connector review/comment signal exists."
    )
    current_head_latch_families = _classify_comment(current_head_latch_comment)
    if "pr2-thread-pagination-and-approval-latch" not in current_head_latch_families:
        failures.append(
            "Comment-family classifier did not classify hyphenated current-head approval latch drift"
        )
    if "rar-phase-advancement-parser" in current_head_latch_families:
        failures.append(
            "Comment-family classifier overmatched current-head approval latch drift as RAR phase advancement"
        )
    release_target_comment = (
        "Pin Target Commit to a parseable release SHA because the release candidate "
        "anchor must derive from current fetched origin/main after later governance repairs."
    )
    if "repo-live-state-boundary-parser" not in _classify_comment(release_target_comment):
        failures.append(
            "Comment-family classifier did not classify release target/external-state boundary drift"
        )
    suffixed_rri_comment = (
        "Reject every in-repo RRI cycle marker when Active RRI Cycle starts with "
        "RRI-20260629-001 and suffix text follows."
    )
    if "repo-live-state-boundary-parser" not in _classify_comment(suffixed_rri_comment):
        failures.append(
            "Comment-family classifier did not classify suffixed Active RRI Cycle live-state drift"
        )
    closeout_comment = (
        "Require external branch state Current Cycle None plus Latest Closed RRI Cycle "
        "and Return Digest Status Complete before accepting closeout."
    )
    if "repo-live-state-boundary-parser" not in _classify_comment(closeout_comment):
        failures.append(
            "Comment-family classifier did not classify external RRI closeout proof drift"
        )
    unrelated_current_cycle = (
        "A current cycle calculation bug changed the retry backoff for product runtime logic."
    )
    if _classify_comment(unrelated_current_cycle) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched unrelated current-cycle wording"
        )
    contextual_current_cycle = (
        "Require external branch state Current Cycle None plus Latest Closed RRI Cycle "
        "before accepting standing Governance closeout."
    )
    if "repo-live-state-boundary-parser" not in _classify_comment(
        contextual_current_cycle
    ):
        failures.append(
            "Comment-family classifier did not classify contextual external Current Cycle drift"
        )
    worktree_confinement_comment = (
        "Restore active worktree confinement markers such as Active Thread Owner, "
        "Thread Assignment Status, and Intended Write Set."
    )
    if "repo-live-state-boundary-parser" not in _classify_comment(worktree_confinement_comment):
        failures.append(
            "Comment-family classifier did not classify standing worktree confinement drift"
        )
    helper_source = Path(__file__).read_text(encoding="utf-8")
    helper_lines = helper_source.splitlines()
    stale_timestamp_binding = any(
        line.strip().startswith("def _head_commit_timestamp(")
        or re.match(r"^\s*head_timestamp\s*=", line) is not None
        for line in helper_lines
    )
    if stale_timestamp_binding:
        failures.append(
            "Approval-latch guardrail found stale timestamp binding helper"
        )
    if (
        "PullRequestCommit" not in helper_source
        or "IssueComment" not in helper_source
        or "hasPreviousPage" not in helper_source
        or "startCursor" not in helper_source
    ):
        failures.append(
            "Approval-latch guardrail must use paginated PR timeline order for current-head review requests"
        )
    synthetic_request = {"created_at": "2026-06-25T19:30:00Z"}
    if _green_proof_after_latest_request("2026-06-25T19:29:59Z", synthetic_request):
        failures.append(
            "Approval-latch guardrail accepted a PR review summary before the latest review request"
        )
    if not _green_proof_after_latest_request(
        "2026-06-25T19:30:01Z", synthetic_request
    ):
        failures.append(
            "Approval-latch guardrail rejected a PR review summary after the latest review request"
        )
    if _green_proof_after_latest_signal(
        "2026-06-25T19:30:01Z", "2026-06-25T19:30:02Z"
    ):
        failures.append(
            "Approval-latch guardrail accepted green proof before the latest Connector signal"
        )
    if not _green_proof_after_latest_signal(
        "2026-06-25T19:30:03Z", "2026-06-25T19:30:02Z"
    ):
        failures.append(
            "Approval-latch guardrail rejected green proof after the latest Connector signal"
        )
    return failures


def _connector_review_comments(review_comments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    for comment in review_comments:
        author = (comment.get("user") or {}).get("login", "")
        if not _is_connector_login(author):
            continue
        body = comment.get("body") or ""
        item = {
            "id": str(comment.get("id") or ""),
            "threadId": str(comment.get("in_reply_to_id") or comment.get("id") or ""),
            "author": {"login": author},
            "body": body,
            "path": comment.get("path") or "",
            "line": comment.get("line") or comment.get("original_line"),
            "originalLine": comment.get("original_line"),
            "createdAt": comment.get("created_at") or "",
            "url": comment.get("html_url") or "",
            "isResolved": False,
            "isOutdated": False,
            "families": _classify_comment(body),
        }
        comments.append(item)
    return comments


def _thread_counts(threads: list[dict[str, Any]]) -> dict[str, int]:
    unresolved = [
        thread for thread in threads if not bool(thread.get("isResolved"))
    ]
    unresolved_current = [
        thread
        for thread in threads
        if not bool(thread.get("isResolved")) and not bool(thread.get("isOutdated"))
    ]
    return {
        "total": len(threads),
        "resolved": len(threads) - len(unresolved),
        "unresolved": len(unresolved),
        "unresolved_current": len(unresolved_current),
        "outdated": sum(1 for thread in threads if bool(thread.get("isOutdated"))),
    }


def _changed_files(base: str) -> list[str]:
    commands = (
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    paths: set[str] = set()
    for command in commands:
        raw = _run(command)
        paths.update(line.strip() for line in raw.splitlines() if line.strip())
    return sorted(paths)


def _is_helper_validator_parser(path: str) -> bool:
    normalized = path.replace("\\", "/").casefold()
    if not normalized.startswith("dev/") or not normalized.endswith(".py"):
        return False
    name = Path(normalized).name
    return any(pattern in name for pattern in HELPER_FILE_PATTERNS)


def _is_firewall_gated_path(path: str, matrix: dict[str, Any]) -> bool:
    normalized = path.replace("\\", "/").casefold()
    file_coverage = matrix.get("changed_file_coverage", {})
    covered_paths = {
        str(key).replace("\\", "/").casefold()
        for key in file_coverage
    } if isinstance(file_coverage, dict) else set()
    return (
        normalized in covered_paths
        or _is_helper_validator_parser(path)
        or normalized in FIREWALL_GATED_PATHS
        or any(normalized.startswith(prefix) for prefix in FIREWALL_GATED_PREFIXES)
    )


def _is_global_churn_matrix_path(path: str) -> bool:
    normalized = path.replace("\\", "/").casefold()
    matrix_path = DEFAULT_MATRIX.relative_to(ROOT).as_posix().casefold()
    return normalized == matrix_path


def _comment_reactions(owner: str, name: str, comment_id: int) -> list[dict[str, Any]]:
    return _rest_paginated(
        f"repos/{owner}/{name}/issues/comments/{comment_id}/reactions"
    )


def _is_at_or_after(timestamp: str, baseline: str) -> bool:
    return bool(timestamp and baseline and timestamp >= baseline)


def _green_proof_after_latest_request(
    timestamp: str, latest_request: dict[str, Any] | None
) -> bool:
    if latest_request is None:
        return True
    return _is_at_or_after(timestamp, latest_request.get("created_at") or "")


def _green_proof_after_latest_signal(timestamp: str, latest_signal_floor: str) -> bool:
    if not latest_signal_floor:
        return bool(timestamp)
    return _is_at_or_after(timestamp, latest_signal_floor)


def _latest_connector_signal_floor(
    issue_comments: list[dict[str, Any]],
    review_summaries: list[dict[str, Any]],
    review_comments: list[dict[str, Any]],
    latest_request: dict[str, Any] | None,
) -> str:
    floor = latest_request.get("created_at") or "" if latest_request else ""
    for item in issue_comments:
        author = (item.get("user") or {}).get("login", "")
        created_at = item.get("created_at") or ""
        if _is_connector_login(author) and _green_proof_after_latest_signal(
            created_at, floor
        ):
            floor = max(floor, created_at)
    for item in review_summaries:
        author = (item.get("user") or {}).get("login", "")
        submitted_at = item.get("submitted_at") or ""
        if _is_connector_login(author) and _green_proof_after_latest_signal(
            submitted_at, floor
        ):
            floor = max(floor, submitted_at)
    for item in review_comments:
        author = (item.get("user") or {}).get("login", "")
        created_at = item.get("created_at") or ""
        if _is_connector_login(author) and _green_proof_after_latest_signal(
            created_at, floor
        ):
            floor = max(floor, created_at)
    return floor


def _latest_review_request_after_head(
    owner: str, name: str, number: int, head_oid: str
) -> dict[str, Any] | None:
    query = """
query($owner:String!,$name:String!,$number:Int!,$cursor:String){
  repository(owner:$owner,name:$name){
    pullRequest(number:$number){
      timelineItems(last:100, before:$cursor, itemTypes:[PULL_REQUEST_COMMIT,ISSUE_COMMENT]){
        pageInfo{hasPreviousPage startCursor}
        nodes{
          __typename
          ... on PullRequestCommit { commit { oid } }
          ... on IssueComment { databaseId author{login} body createdAt url }
        }
      }
    }
  }
}
"""
    nodes: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        data = _graphql(
            query,
            {"owner": owner, "name": name, "number": number, "cursor": cursor},
        )
        timeline = data["repository"]["pullRequest"]["timelineItems"]
        page_nodes = timeline["nodes"]
        nodes = page_nodes + nodes
        page_info = timeline["pageInfo"]
        if any(
            node.get("__typename") == "PullRequestCommit"
            and (node.get("commit") or {}).get("oid") == head_oid
            for node in page_nodes
        ):
            break
        if not page_info["hasPreviousPage"]:
            break
        cursor = page_info["startCursor"]

    head_index = -1
    for index, node in enumerate(nodes):
        if (
            node.get("__typename") == "PullRequestCommit"
            and (node.get("commit") or {}).get("oid") == head_oid
        ):
            head_index = index
    if head_index < 0:
        return None

    latest_request: dict[str, Any] | None = None
    for index, node in enumerate(nodes):
        if index <= head_index or node.get("__typename") != "IssueComment":
            continue
        body = node.get("body") or ""
        if "@codex" in body.casefold() and "review" in body.casefold():
            latest_request = {
                "id": node.get("databaseId"),
                "created_at": node.get("createdAt") or "",
                "html_url": node.get("url") or "",
                "body": body,
            }
    return latest_request


def _extract_latest_green(
    owner: str,
    name: str,
    number: int,
    head_oid: str,
    review_comments: list[dict[str, Any]] | None = None,
) -> tuple[bool, str]:
    issue_comments = _rest_paginated(f"repos/{owner}/{name}/issues/{number}/comments")
    review_summaries = _rest_paginated(f"repos/{owner}/{name}/pulls/{number}/reviews")
    if review_comments is None:
        review_comments = _rest_paginated(f"repos/{owner}/{name}/pulls/{number}/comments")
    green_patterns = (
        "didn't find any major issues",
        "didn\u2019t find any major issues",
        "did not find any major issues",
        "didnt find any major issues",
        "no major issues",
        "looks good",
    )
    candidates: list[tuple[str, str, str]] = []
    latest_request = _latest_review_request_after_head(owner, name, number, head_oid)
    latest_request_created = ""
    if latest_request:
        latest_request_created = latest_request.get("created_at") or ""
    latest_signal_floor = _latest_connector_signal_floor(
        issue_comments, review_summaries, review_comments, latest_request
    )
    for item in issue_comments:
        author = (item.get("user") or {}).get("login", "")
        body = item.get("body") or ""
        created_at = item.get("created_at") or ""
        if (
            latest_request is not None
            and _is_at_or_after(created_at, latest_request_created)
            and _green_proof_after_latest_signal(created_at, latest_signal_floor)
            and _is_connector_login(author)
            and any(pattern in body.casefold() for pattern in green_patterns)
        ):
            candidates.append(
                (
                    created_at,
                    body
                    + f"\nTimeline order: current head {head_oid} appeared before latest review request.",
                    item.get("html_url") or "",
                )
            )
    if latest_request:
        request_id = latest_request.get("id")
        if isinstance(request_id, int):
            for reaction in _comment_reactions(owner, name, request_id):
                reaction_author = (reaction.get("user") or {}).get("login", "")
                reaction_created = reaction.get("created_at") or ""
                if (
                    reaction.get("content") == "+1"
                    and _is_connector_login(reaction_author)
                    and _is_at_or_after(reaction_created, latest_request_created)
                    and _green_proof_after_latest_signal(
                        reaction_created, latest_signal_floor
                    )
                ):
                    return (
                        True,
                        (
                            f"{latest_request.get('created_at') or ''} "
                            f"{latest_request.get('html_url') or ''} "
                            "(Codex Connector thumbs-up reaction on latest current-head review request)"
                        ).strip(),
                    )
    for item in review_summaries:
        author = (item.get("user") or {}).get("login", "")
        body = item.get("body") or ""
        commit_id = item.get("commit_id") or ""
        submitted_at = item.get("submitted_at") or ""
        is_green_summary = _is_connector_login(author) and any(
            pattern in body.casefold() for pattern in green_patterns
        )
        if is_green_summary and commit_id == head_oid:
            if not _green_proof_after_latest_request(
                submitted_at, latest_request
            ) or not _green_proof_after_latest_signal(submitted_at, latest_signal_floor):
                continue
            candidates.append(
                (
                    submitted_at,
                    body
                    + f"\nReviewed commit: {commit_id}"
                    + (
                        "\nSubmitted after latest current-head review request."
                        if latest_request is not None
                        else ""
                    ),
                    item.get("html_url") or "",
                )
            )
        elif is_green_summary:
            candidates.append(
                (
                    submitted_at,
                    body + f"\nReviewed commit: {commit_id}",
                    item.get("html_url") or "",
                )
            )
    if not candidates:
        return False, "No Codex Connector green comment/review found."
    candidates.sort(key=lambda item: item[0])
    timestamp, body, url = candidates[-1]
    head_bound = head_oid[:10].casefold() in body.casefold() or head_oid.casefold() in body.casefold()
    detail = f"{timestamp} {url}".strip()
    if not head_bound:
        detail += " (green evidence found, but not text-bound to current head)"
    return head_bound, detail


def _validate_matrix(
    matrix: dict[str, Any],
    observed_families: set[str],
    changed_helper_files: list[str],
) -> list[str]:
    failures: list[str] = []
    family_entries = matrix.get("families")
    if not isinstance(family_entries, list) or not family_entries:
        return ["Review churn matrix has no family entries"]

    entries = {entry.get("family_id"): entry for entry in family_entries}
    if len(entries) != len(family_entries):
        failures.append("Review churn matrix has duplicate or missing family_id values")

    required_list_fields = (
        "source_truth",
        "implementation",
        "fixture_coverage",
        "generated_mutation_coverage",
        "representative_comment_patterns",
        "sibling_variant_replay",
    )
    for family_id, entry in entries.items():
        if not family_id:
            continue
        for field in required_list_fields:
            value = entry.get(field)
            if not isinstance(value, list) or not value:
                failures.append(f"{family_id}: matrix field {field} must be a non-empty list")
                continue
            if any(not isinstance(item, str) or not item.strip() for item in value):
                failures.append(f"{family_id}: matrix field {field} contains a blank item")
        for field in ("source_truth", "implementation", "fixture_coverage"):
            for item in entry.get(field, []):
                if not isinstance(item, str) or item.startswith("generated:"):
                    continue
                path = ROOT / item.replace("\\", "/")
                if not path.exists():
                    failures.append(f"{family_id}: coverage path does not exist: {item}")

    unknown_families = sorted(observed_families - set(entries))
    for family_id in unknown_families:
        failures.append(f"Observed connector family lacks matrix coverage: {family_id}")

    file_coverage = matrix.get("changed_file_coverage", {})
    if not isinstance(file_coverage, dict):
        failures.append("Review churn matrix changed_file_coverage must be an object")
        file_coverage = {}
    for changed_file in changed_helper_files:
        families = file_coverage.get(changed_file)
        if not isinstance(families, list) or not families:
            failures.append(
                f"Changed pre-PR firewall-gated file lacks family coverage: {changed_file}"
            )
            continue
        for family_id in families:
            if family_id not in entries:
                failures.append(
                    f"{changed_file}: changed-file coverage references unknown family {family_id}"
                )
            else:
                entry = entries[family_id]
                coverage_fields = ("source_truth", "implementation", "fixture_coverage")
                if not any(
                    changed_file in entry.get(field, []) for field in coverage_fields
                ) and not _is_global_churn_matrix_path(changed_file):
                    failures.append(
                        f"{changed_file}: family {family_id} does not list the file as source-truth, implementation, or fixture coverage"
                    )
    return failures


def _as_int(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return default


def _review_churn_budget_result(
    matrix: dict[str, Any],
    pr_number: int,
    connector_comment_count: int,
    family_counts: dict[str, int],
) -> tuple[str, list[str]]:
    budget = matrix.get("review_churn_budget")
    if not isinstance(budget, dict):
        return (
            "NOT CONFIGURED",
            ["Review churn matrix missing review_churn_budget"],
        )

    total_budget = _as_int(
        budget.get("max_connector_comments_before_root_cause_receipt"),
        DEFAULT_TOTAL_COMMENT_BUDGET,
    )
    same_family_budget = _as_int(
        budget.get("max_same_family_comments_before_root_cause_receipt"),
        DEFAULT_SAME_FAMILY_COMMENT_BUDGET,
    )
    over_total = connector_comment_count > total_budget
    over_family = any(count > same_family_budget for count in family_counts.values())
    if not over_total and not over_family:
        return (
            (
                f"WITHIN BUDGET - connector_comments={connector_comment_count} "
                f"<= {total_budget}; max_family_count="
                f"{max(family_counts.values(), default=0)} <= {same_family_budget}"
            ),
            [],
        )

    receipts = budget.get("root_cause_receipts")
    if not isinstance(receipts, list):
        return (
            (
                f"EXCEEDED WITHOUT RECEIPTS - connector_comments={connector_comment_count}; "
                f"max_family_count={max(family_counts.values(), default=0)}"
            ),
            ["Review churn budget exceeded but root_cause_receipts is missing"],
        )

    matching_receipts = [
        receipt
        for receipt in receipts
        if isinstance(receipt, dict) and _as_int(receipt.get("pr"), -1) == pr_number
    ]
    if not matching_receipts:
        return (
            (
                f"EXCEEDED WITHOUT PR RECEIPT - connector_comments={connector_comment_count}; "
                f"max_family_count={max(family_counts.values(), default=0)}"
            ),
            [f"Review churn budget exceeded but PR #{pr_number} has no root-cause receipt"],
        )

    failures: list[str] = []
    receipt = matching_receipts[-1]
    if _as_int(receipt.get("connector_comments"), -1) != connector_comment_count:
        failures.append(
            "Review churn root-cause receipt connector_comments does not match live evidence"
        )
    observed_family_counts = receipt.get("observed_family_counts")
    if observed_family_counts != family_counts:
        failures.append(
            "Review churn root-cause receipt observed_family_counts does not match live evidence"
        )
    if receipt.get("pr_readiness_stage_1_failure") is not True:
        failures.append(
            "Review churn root-cause receipt must mark pr_readiness_stage_1_failure true"
        )
    for field in ("root_cause", "prevention_summary", "receipt_marker", "receipt_file"):
        value = receipt.get(field)
        if not isinstance(value, str) or not value.strip():
            failures.append(f"Review churn root-cause receipt missing {field}")
    preventive_changes = receipt.get("preventive_changes")
    if not isinstance(preventive_changes, list) or not preventive_changes:
        failures.append("Review churn root-cause receipt missing preventive_changes")
    elif any(not isinstance(item, str) or not item.strip() for item in preventive_changes):
        failures.append("Review churn root-cause receipt preventive_changes contains a blank item")

    receipt_file = receipt.get("receipt_file")
    receipt_marker = receipt.get("receipt_marker")
    if isinstance(receipt_file, str) and receipt_file.strip():
        path = ROOT / receipt_file.replace("\\", "/")
        if not path.exists():
            failures.append(f"Review churn root-cause receipt file does not exist: {receipt_file}")
        elif isinstance(receipt_marker, str) and receipt_marker.strip():
            text = path.read_text(encoding="utf-8")
            if receipt_marker not in text:
                failures.append(
                    f"Review churn root-cause receipt marker not found in {receipt_file}"
                )

    if failures:
        return (
            (
                f"EXCEEDED WITH INVALID RECEIPT - connector_comments={connector_comment_count}; "
                f"max_family_count={max(family_counts.values(), default=0)}"
            ),
            failures,
        )

    return (
        (
            f"EXCEEDED WITH ROOT-CAUSE RECEIPT - connector_comments={connector_comment_count}; "
            f"max_family_count={max(family_counts.values(), default=0)}; "
            f"receipt={receipt.get('receipt_file')}"
        ),
        [],
    )


def _families_for_changed_files(
    matrix: dict[str, Any], changed_helper_files: list[str]
) -> set[str]:
    file_coverage = matrix.get("changed_file_coverage")
    if not isinstance(file_coverage, dict):
        return set()
    families: set[str] = set()
    for changed_file in changed_helper_files:
        for family_id in file_coverage.get(changed_file, []):
            if isinstance(family_id, str) and family_id.strip():
                families.add(family_id)
    return families


def _family_entries(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = matrix.get("families")
    if not isinstance(entries, list):
        return {}
    return {
        entry.get("family_id"): entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("family_id"), str)
    }


def _validate_pre_pr_firewall(
    matrix: dict[str, Any],
    changed_helper_files: list[str],
    *,
    skip_commands: bool,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    lines: list[str] = []
    firewall = matrix.get("pre_pr_firewall")
    if not isinstance(firewall, dict):
        return ["Review churn matrix missing pre_pr_firewall"], lines

    changed_families = _families_for_changed_files(matrix, changed_helper_files)
    entries = _family_entries(matrix)
    if changed_helper_files and not changed_families:
        failures.append(
            "Pre-PR firewall found changed helper/validator/parser files but no mapped families"
        )
    for family_id in sorted(changed_families):
        entry = entries.get(family_id)
        if not entry:
            failures.append(f"Pre-PR firewall mapped unknown family: {family_id}")
            continue
        mutations = entry.get("generated_mutation_coverage")
        siblings = entry.get("sibling_variant_replay")
        if not isinstance(mutations, list) or len(mutations) < 3:
            failures.append(
                f"{family_id}: pre-PR firewall requires at least three generated mutation variants"
            )
        if not isinstance(siblings, list) or len(siblings) < 2:
            failures.append(
                f"{family_id}: pre-PR firewall requires at least two sibling replay variants"
            )

    replay_rows = firewall.get("connector_corpus_replay")
    if not isinstance(replay_rows, list) or not replay_rows:
        failures.append("pre_pr_firewall.connector_corpus_replay must be a non-empty list")
    else:
        for index, row in enumerate(replay_rows, start=1):
            if not isinstance(row, dict):
                failures.append(f"connector_corpus_replay row {index} must be an object")
                continue
            family_id = row.get("family_id")
            comment = row.get("comment")
            if not isinstance(family_id, str) or family_id not in entries:
                failures.append(
                    f"connector_corpus_replay row {index} references unknown family {family_id}"
                )
                continue
            if not isinstance(comment, str) or not comment.strip():
                failures.append(f"connector_corpus_replay row {index} has no comment text")
                continue
            classified = set(_classify_comment(comment))
            if family_id not in classified:
                failures.append(
                    f"connector_corpus_replay row {index} did not classify as {family_id}: {sorted(classified)}"
                )
            lines.append(
                f"- {family_id}: {'PASS' if family_id in classified else 'FAIL'}"
            )

    unknown_guardrails = firewall.get("unknown_comment_guardrails")
    if not isinstance(unknown_guardrails, list) or not unknown_guardrails:
        failures.append("pre_pr_firewall.unknown_comment_guardrails must be a non-empty list")
    else:
        for index, comment in enumerate(unknown_guardrails, start=1):
            if not isinstance(comment, str) or not comment.strip():
                failures.append(f"unknown_comment_guardrails row {index} is blank")
                continue
            classified = _classify_comment(comment)
            if classified != ["unknown"]:
                failures.append(
                    f"unknown_comment_guardrails row {index} overmatched as {classified}"
                )

    commands = firewall.get("validation_commands")
    if not isinstance(commands, list) or not commands:
        failures.append("pre_pr_firewall.validation_commands must be a non-empty list")
    elif skip_commands:
        lines.append("- local validation commands: SKIPPED by caller")
    else:
        for index, command_entry in enumerate(commands, start=1):
            if not isinstance(command_entry, dict):
                failures.append(f"validation_commands row {index} must be an object")
                continue
            command = command_entry.get("command")
            name = command_entry.get("name") or f"command {index}"
            if (
                not isinstance(command, list)
                or not command
                or any(not isinstance(part, str) or not part.strip() for part in command)
            ):
                failures.append(f"validation_commands row {index} has an invalid command")
                continue
            if not _python_manifest_command_uses_portable_token(command):
                failures.append(
                    f"validation_commands row {index} must use {{python}} for Python scripts"
                )
                continue
            resolved_command = _resolve_manifest_command(command)
            code, output = _run_for_status(resolved_command)
            lines.append(
                f"- {name}: {'PASS' if code == 0 else 'FAIL'} ({' '.join(command)})"
            )
            if code != 0:
                failures.append(
                    f"pre_pr_firewall validation command failed ({' '.join(command)}): {output}"
                )

    return failures, lines


def build_pre_pr_report(args: argparse.Namespace) -> tuple[int, str]:
    matrix = _load_matrix(Path(args.matrix))
    changed_files = _changed_files(args.base)
    changed_helper_files = [
        path for path in changed_files if _is_firewall_gated_path(path, matrix)
    ]
    changed_families = _families_for_changed_files(matrix, changed_helper_files)
    failures: list[str] = []
    failures.extend(_classifier_guardrail_failures())
    failures.extend(_validate_matrix(matrix, changed_families, changed_helper_files))
    firewall_failures, firewall_lines = _validate_pre_pr_firewall(
        matrix, changed_helper_files, skip_commands=args.skip_pre_pr_commands
    )
    failures.extend(firewall_failures)

    lines = [
        "Pre-PR Adversarial Review Firewall",
        f"Base: {args.base}",
        "Changed pre-PR firewall-gated files:",
        *[f"- {path}" for path in changed_helper_files],
        "Mapped connector families:",
        *[f"- {family_id}" for family_id in sorted(changed_families)],
        "Local adversarial replay:",
        *firewall_lines,
    ]
    if failures:
        lines.append("Result: FAIL")
        lines.extend(f"- {failure}" for failure in failures)
        return 1, "\n".join(lines)
    lines.append("Result: PASS")
    return 0, "\n".join(lines)


def build_report(args: argparse.Namespace) -> tuple[int, str]:
    owner, name = _split_repo(args.repo)
    pull_request, threads, page_count = _fetch_review_threads(owner, name, args.pr)
    review_comments, review_comment_page_count = _rest_paginated_pages(
        f"repos/{owner}/{name}/pulls/{args.pr}/comments"
    )
    matrix = _load_matrix(Path(args.matrix))
    comments = _connector_review_comments(review_comments)
    thread_counts = _thread_counts(threads)
    changed_files = _changed_files(args.base)
    changed_helper_files = [
        path for path in changed_files if _is_firewall_gated_path(path, matrix)
    ]
    observed_families = {
        family
        for comment in comments
        for family in comment.get("families", [])
    }
    family_counts = {
        family_id: sum(1 for comment in comments if family_id in comment["families"])
        for family_id in sorted(observed_families)
    }

    failures: list[str] = []
    if thread_counts["unresolved_current"]:
        failures.append(
            f"Unresolved current review threads remain: {thread_counts['unresolved_current']}"
        )
    if "unknown" in observed_families:
        failures.append("At least one connector review comment was not classified")
    failures.extend(_classifier_guardrail_failures())
    failures.extend(_validate_matrix(matrix, observed_families - {"unknown"}, changed_helper_files))
    budget_status, budget_failures = _review_churn_budget_result(
        matrix,
        args.pr,
        len(comments),
        family_counts,
    )
    failures.extend(budget_failures)
    green_bound, green_detail = _extract_latest_green(
        owner, name, args.pr, pull_request["headRefOid"], review_comments
    )
    current_green_failure = "Current-head Codex Connector green approval latch is missing"
    current_head_revalidation_pending = args.require_current_green and not green_bound
    if current_head_revalidation_pending:
        failures.append(current_green_failure)

    lines = [
        "PR Review Churn Validation",
        f"Repository: {args.repo}",
        f"PR: {args.pr}",
        f"Head SHA: {pull_request['headRefOid']}",
        f"Mergeability: {pull_request.get('mergeable')} / {pull_request.get('mergeStateStatus')}",
        f"Review-thread pages inspected: {page_count}",
        f"Review-comment pages inspected: {review_comment_page_count}",
        (
            "Review-thread counts: "
            f"total={thread_counts['total']}, "
            f"resolved={thread_counts['resolved']}, "
            f"unresolved={thread_counts['unresolved']}, "
            f"unresolved_current={thread_counts['unresolved_current']}, "
            f"outdated={thread_counts['outdated']}"
        ),
        f"Connector review comments collected: {len(comments)}",
        f"Review-churn budget: {budget_status}",
        "Connector family counts:",
    ]
    for family_id, count in family_counts.items():
        lines.append(f"- {family_id}: {count}")
    lines.extend(
        [
            "Changed pre-PR firewall-gated files:",
            *[f"- {path}" for path in changed_helper_files],
            f"Latest current-head green proof: {'BOUND' if green_bound else 'NOT BOUND'} - {green_detail}",
        ]
    )
    if current_head_revalidation_pending:
        if failures == [current_green_failure]:
            lines.append(
                "PR2 continuation posture: CURRENT_HEAD_REVALIDATION_PENDING - "
                "merge-ready proof is not green; continue direct PR2 polling or "
                "revalidation instead of treating this as a terminal BLOCKED state."
            )
        else:
            lines.append(
                "PR2 continuation posture: CURRENT_HEAD_REVALIDATION_PENDING with "
                "additional failures; repair non-latch failures before normal "
                "direct PR2 continuation."
            )
    if failures:
        lines.append("Result: FAIL")
        lines.extend(f"- {failure}" for failure in failures)
        return 1, "\n".join(lines)
    lines.append("Result: PASS")
    return 0, "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", type=int)
    parser.add_argument("--repo", default="GiribaldiTTV/Nexus-Desktop-AI")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    parser.add_argument(
        "--pre-pr-firewall",
        action="store_true",
        help="Run local adversarial coverage, corpus, and changed-file family checks before PR review.",
    )
    parser.add_argument(
        "--skip-pre-pr-commands",
        action="store_true",
        help="Validate the pre-PR firewall schema and corpus without executing nested validation commands.",
    )
    parser.add_argument(
        "--require-current-green",
        action="store_true",
        help="Fail unless a Codex Connector green comment/review is bound to the live head.",
    )
    args = parser.parse_args(argv)
    try:
        if args.pre_pr_firewall:
            code, report = build_pre_pr_report(args)
        else:
            if args.pr is None:
                parser.error("--pr is required unless --pre-pr-firewall is used")
            code, report = build_report(args)
    except Exception as exc:  # pragma: no cover - command-line reporting
        print(f"FAIL: PR review churn validation could not complete: {exc}")
        return 1
    print(report)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
