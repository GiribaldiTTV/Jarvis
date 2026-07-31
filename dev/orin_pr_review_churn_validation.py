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

import orin_docs_inventory_reform_audit as docs_inventory


ROOT = Path(__file__).resolve().parents[1]
MATRIX_DIR = ROOT / "dev" / "fixtures" / "pr_review_churn"
DEFAULT_MATRIX = MATRIX_DIR / "pr_276_rar_review_churn_matrix.json"
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
    "historical receipts",
    "active receipt",
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
        "user-review-source-copy-identity",
        (
            "newline normalization",
            "binary blobs byte-exact",
            "git-normalized text formats",
            "copied source-context files",
            "compare bare carriage returns exactly",
            "bare carriage return",
        ),
    ),
    FamilyRule(
        "user-review-support-authority",
        (
            "direct authorization",
            "direct-authority",
            "direct allows authority wording",
            "allows pr creation",
            "authority verbs",
            "support authority",
            "authority scan",
            "support artifact authorizes",
            "supporting artifact authorizes",
            "supporting context permits",
            "supporting-artifact authority",
            "gated-action matches",
            "exclude analysis nouns",
            "support context attempts to authorize",
            "preserve paragraph boundaries in bare support-authority scans",
            "bare support-authority scans",
            "bare support artifact",
            "bare supporting-context authority subjects",
            "supporting context and review aid",
            "passive supporting-context agents",
            "authorized by this supporting context",
            "scan coordinated authority targets after benign objects",
            "coordinated authority targets",
            "allow primary decision artifacts to grant approved authority",
            "legitimate primary artifact",
            "affirmative adverb",
            "verbal forms of gated authority targets",
            "creating a pr",
            "implementing the plan",
            "past-tense support authorization claims",
            "past, perfect, and progressive forms",
            "recognize auxiliaries in passive authority claims",
            "passive auxiliaries",
            "reject instrumental support-authority instructions",
            "instrumental constructions",
            "support artifact is used to authorize",
            "keep semicolons from erasing authority negation",
            "semicolon as a clause boundary",
            "new authority predicate after it",
            "scan every generated review aid for authority claims",
            "additional allowed review aid",
            "recognize plural support-authority subjects",
            "plural support artifacts",
        ),
    ),
    FamilyRule(
        "user-review-support-state",
        (
            "support context state",
            "support states",
            "support-context failure",
            "support context failure",
            "planning-keyword",
            "planning keyword",
            "semantic state section",
            "state markers inside fenced markdown",
            "exact support-state location",
            "misplaced support state outside stage 1",
            "support-only state",
            "recognize list-prefixed state fields",
            "list field",
        ),
    ),
    FamilyRule(
        "user-review-fixture-execution",
        (
            "regression assertions",
            "fixture suite still passes",
            "run assert_fails",
        ),
    ),
    FamilyRule(
        "user-review-support-reviewability",
        (
            "reviewability on the stage 1 support artifact",
            "nonblank valid reviewability state",
            "per-role contract",
            "reviewability state alongside its support state",
        ),
    ),
    FamilyRule(
        "user-review-firewall-matrix-routing",
        (
            "load the pr 311 matrix",
            "mandated firewall",
            "documented stage 1 command",
            "default matrix",
            "matrix is selected",
            "mandatory pre-pr gate",
            "exclude deleted matrices from automatic selection",
            "deleted matrix",
        ),
    ),
    FamilyRule(
        "user-review-write-set-receipt",
        (
            "record the added firewall work in branch scope",
            "durable confinement/audit record",
            "contradicts the actual committed scope",
            "later review-churn repair files",
            "validate branch receipts in detached head checkouts",
            "discover changed receipts directly in detached head",
            "changed branch receipt not registered in the selected matrix",
            "detached head checkout",
            "silently skips the new intended write set validation",
            "reject duplicate intended write set fields",
            "two intended write set fields",
            "exactly one canonical write-set field",
            "limit write-set enforcement to active receipts",
            "historical receipts",
            "active receipt",
            "active-to-unclassified downgrade",
            "active receipt drops its markers",
            "preserve current confinement and status sections",
            "preserve current sections after historical receipt headings",
            "allow deletion or renaming of historical receipts",
            "inspect a missing changed receipt at the base revision",
            "bulleted intended write set",
            "fold down the receipt before merge",
            "committed merge-target state",
            "assignment fields in a historical section",
            "include source paths when discovering receipt renames",
            "status-aware diff",
            "scope historical status detection to the receipt itself",
            "canonical historical values",
            "canonical receipt phase",
            "generic status prose",
        ),
    ),
    FamilyRule(
        "user-review-comment-family-precision",
        (
            "require fixture context",
            "common review phrase",
            "corrupts observed-family counts",
            "unknown-comment guardrail",
            "scope pr-specific classifier families to their matrix",
            "pr-specific rules are globally active",
            "selected matrix defines the corresponding families",
            "preserve findings that contain green wording",
            "standalone no-findings summary",
            "accept the established connector green response",
            "chef's kiss",
            "require write-set context for receipt keywords",
            "receipt keywords",
        ),
    ),
    FamilyRule(
        "user-review-primary-marker-cardinality",
        (
            "require exact markers on the stage 1 primary artifact",
            "lack the canonical primary user-gate field",
            "exactly one marker on the primary artifact",
            "validate the value of the stage 1 outcome field",
            "invalid stage 1 outcome",
            "contradictory stage 1 outcome qualifiers",
            "outcome qualifier",
        ),
    ),
    FamilyRule(
        "user-review-markdown-semantics",
        (
            "exclude non-semantic markdown from authority scans",
            "indented code example",
            "html comment",
            "equivalent markdown examples",
            "mask inline markdown examples before authority matching",
            "inline code spans",
            "preserves the code span",
            "mask multiline inline-code examples",
            "multiline inline-code",
            "preserve code-formatted contract values",
            "code-formatted contract values",
        ),
    ),
    FamilyRule(
        "user-review-inventory-currentness",
        (
            "regenerate the inventory after final receipt edits",
            "inventory generator's current counting formula",
            "committed audit was produced before the final receipt expansion",
            "stale generated inventory counts",
            "check inventory whenever a branch receipt changes",
            "omits the generated inventory from its diff",
            "changed receipt candidates",
            "track each inventory line-count surface separately",
            "each expected surface by identity",
            "undifferentiated occurrences",
            "inventory removal for deleted receipts",
            "deleted receipt path",
            "validate regenerated inventory content",
            "not only counts",
            "reuse the requested base for inventory rendering",
            "requested base",
            "no-write generator",
            "make inventory rendering independent of checkout branch state",
            "detached ci checkout",
            "stable branch context",
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


def _classify_comment(
    body: str,
    allowed_families: set[str] | None = None,
) -> list[str]:
    normalized = _normalize(body)
    has_classifier_context = any(
        keyword in normalized for keyword in CLASSIFIER_CONTEXT_KEYWORDS
    )
    families: list[str] = []
    for rule in FAMILY_RULES:
        if allowed_families is not None and rule.family_id not in allowed_families:
            continue
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
    user_review_families = [
        family
        for family in families
        if family.startswith("user-review-")
    ]
    return user_review_families or families or ["unknown"]


def _classifier_guardrail_failures() -> list[str]:
    failures: list[str] = []
    unrelated = "A database migration status row has mixed case after cleanup."
    if _classify_comment(unrelated) != ["unknown"]:
        failures.append(
            "Comment-family classifier overmatched unrelated status/case/row wording"
        )
    for unrelated_receipt_comment in (
        "Preserve historical receipts when regenerating the docs index.",
        "The active receipt title is truncated.",
    ):
        if _classify_comment(
            unrelated_receipt_comment,
            {"user-review-write-set-receipt"},
        ) != ["unknown"]:
            failures.append(
                "Comment-family classifier treated generic receipt wording as "
                "write-set confinement evidence: "
                + unrelated_receipt_comment
            )
    for contextual_receipt_comment in (
        "Preserve current sections after historical receipt headings when active confinement follows.",
        "Allow deletion or renaming of historical receipts after base-revision classification.",
    ):
        if "user-review-write-set-receipt" not in _classify_comment(
            contextual_receipt_comment,
            {"user-review-write-set-receipt"},
        ):
            failures.append(
                "Comment-family classifier lost write-set-specific historical receipt "
                "context: "
                + contextual_receipt_comment
            )
    user_review_examples = {
        "user-review-source-copy-identity": (
            "Include repository text formats in newline normalization for copied source-context files."
        ),
        "user-review-support-authority": (
            "Limit authority verbs to USER-gated targets in support authority claims."
        ),
        "user-review-support-state": (
            "Validate Support Context State before the planning-keyword return."
        ),
        "user-review-fixture-execution": (
            "Execute the direct-authority regression assertions; the cases are never checked."
        ),
        "user-review-support-reviewability": (
            "Require reviewability on the Stage 1 support artifact with one nonblank valid reviewability state."
        ),
        "user-review-firewall-matrix-routing": (
            "Load the PR 311 matrix in the mandated firewall instead of relying on the default matrix."
        ),
        "user-review-write-set-receipt": (
            "Record the added firewall work in branch scope and the Intended Write Set."
        ),
        "user-review-comment-family-precision": (
            "Require fixture context before a common review phrase can bypass the unknown-comment guardrail."
        ),
        "user-review-markdown-semantics": (
            "Exclude non-semantic Markdown from authority scans, including an indented code example and HTML comment."
        ),
        "user-review-inventory-currentness": (
            "Regenerate the inventory after final receipt edits so stale generated inventory counts cannot survive."
        ),
        "user-review-primary-marker-cardinality": (
            "Require exact markers on the Stage 1 primary artifact so it cannot lack the canonical primary USER-gate field."
        ),
    }
    for family_id, comment in user_review_examples.items():
        if family_id not in _classify_comment(comment):
            failures.append(
                f"Comment-family classifier did not classify {family_id}"
            )
    generic_review_summary = (
        "### Codex Review\n\n"
        "Here are some automated review suggestions for this pull request.\n\n"
        "**Reviewed commit:** `abc123`\n\n<details>boilerplate</details>"
    )
    if _substantive_review_summary_body(generic_review_summary):
        failures.append(
            "Connector review-summary guardrail treated boilerplate as a finding"
        )
    substantive_review_summary = (
        "### Codex Review\n\n"
        "**Validate the value of the Stage 1 Outcome field**\n\n"
        "The surrounding logic looks good, but an invalid Stage 1 Outcome is accepted.\n\n"
        "<details>boilerplate</details>"
    )
    if not _is_standalone_connector_green("Looks good."):
        failures.append(
            "Connector green-summary guardrail rejected a standalone green signal"
        )
    if _is_standalone_connector_green(substantive_review_summary):
        failures.append(
            "Connector green-summary guardrail treated finding prose as green"
        )
    established_green = "Codex Review: Didn't find any major issues. Chef's kiss."
    if not _is_standalone_connector_green(established_green):
        failures.append(
            "Connector green-summary guardrail rejected the established green response"
        )
    if _is_standalone_connector_green(established_green + " But one path still fails."):
        failures.append(
            "Connector green-summary guardrail accepted a finding appended to green wording"
        )
    synthetic_summary_comments = _connector_review_summary_comments(
        [
            {
                "id": 1,
                "user": {"login": "chatgpt-codex-connector[bot]"},
                "body": substantive_review_summary,
                "submitted_at": "2026-06-25T19:30:00Z",
                "commit_id": "head",
            },
            {
                "id": 2,
                "user": {"login": "chatgpt-codex-connector[bot]"},
                "body": generic_review_summary,
                "submitted_at": "2026-06-25T19:31:00Z",
                "commit_id": "head",
            },
        ],
        {"user-review-primary-marker-cardinality"},
        "head",
    )
    if (
        len(synthetic_summary_comments) != 1
        or synthetic_summary_comments[0]["families"]
        != ["user-review-primary-marker-cardinality"]
    ):
        failures.append(
            "Connector review-summary guardrail did not retain and classify exactly "
            "one substantive finding"
        )
    benign_user_review_text = (
        "A review aid enables source-truth comparison and permits inspection."
    )
    if "user-review-support-authority" in _classify_comment(
        benign_user_review_text
    ):
        failures.append(
            "Comment-family classifier overmatched benign review-aid guidance as authority"
        )
    scoped_comment = (
        "Scope PR-specific classifier families to their matrix because the default matrix "
        "must not activate unrelated rules."
    )
    if _classify_comment(scoped_comment, {"user-review-support-state"}) != ["unknown"]:
        failures.append(
            "Comment-family classifier ignored the selected matrix family scope"
        )
    if "user-review-comment-family-precision" not in _classify_comment(
        scoped_comment,
        {"user-review-comment-family-precision"},
    ):
        failures.append(
            "Comment-family classifier rejected a family permitted by the selected matrix"
        )
    for unrelated_never_checked in (
        "The subprocess return code is never checked.",
        "The HTTP response is never checked before decoding.",
    ):
        if _classify_comment(unrelated_never_checked) != ["unknown"]:
            failures.append(
                "Comment-family classifier treated an unrelated 'never checked' phrase "
                f"as fixture execution: {unrelated_never_checked}"
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


def _connector_review_comments(
    review_comments: list[dict[str, Any]],
    allowed_families: set[str],
) -> list[dict[str, Any]]:
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
            "families": _classify_comment(body, allowed_families),
        }
        comments.append(item)
    return comments


def _connector_review_summary_content(body: str) -> str:
    finding_text = re.split(r"<details\b", body, maxsplit=1, flags=re.IGNORECASE)[0]
    retained_lines: list[str] = []
    for line in finding_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        normalized = stripped.casefold()
        if normalized.startswith("###") and "codex review" in normalized:
            continue
        if normalized.startswith("here are some automated review suggestions"):
            continue
        if normalized.startswith("**reviewed commit:**"):
            continue
        retained_lines.append(stripped)
    return "\n".join(retained_lines)


def _is_standalone_connector_green(body: str) -> bool:
    content = _connector_review_summary_content(body).casefold().replace("\u2019", "'")
    normalized = re.sub(r"[^\w']+", " ", content).strip()
    return normalized in {
        "didn't find any major issues",
        "didnt find any major issues",
        "did not find any major issues",
        "no major issues",
        "looks good",
        "codex didn't find any major issues",
        "codex didnt find any major issues",
        "codex did not find any major issues",
        "codex found no major issues",
        "codex review looks good",
        "codex review didn't find any major issues chef's kiss",
        "codex review didnt find any major issues chef's kiss",
        "codex review did not find any major issues chef's kiss",
    }


def _substantive_review_summary_body(body: str) -> str:
    substantive = _connector_review_summary_content(body)
    return "" if _is_standalone_connector_green(substantive) else substantive


def _connector_review_summary_comments(
    review_summaries: list[dict[str, Any]],
    allowed_families: set[str],
    head_oid: str,
) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    for review in review_summaries:
        author = (review.get("user") or {}).get("login", "")
        if not _is_connector_login(author):
            continue
        body = _substantive_review_summary_body(review.get("body") or "")
        if not body:
            continue
        comments.append(
            {
                "id": f"review-{review.get('id') or ''}",
                "threadId": "",
                "author": {"login": author},
                "body": body,
                "path": "",
                "line": None,
                "originalLine": None,
                "createdAt": review.get("submitted_at") or "",
                "url": review.get("html_url") or "",
                "isResolved": False,
                "isOutdated": review.get("commit_id") not in {None, "", head_oid},
                "families": _classify_comment(body, allowed_families),
            }
        )
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


def _name_status_paths(raw: str) -> set[str]:
    paths: set[str] = set()
    for line in raw.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status = fields[0].strip().upper()
        if status.startswith(("R", "C")) and len(fields) >= 3:
            paths.update(path.strip() for path in fields[1:3] if path.strip())
        elif fields[1].strip():
            paths.add(fields[1].strip())
    return paths


def _changed_files(base: str) -> list[str]:
    status_commands = (
        ["git", "diff", "--name-status", f"{base}...HEAD"],
        ["git", "diff", "--name-status"],
        ["git", "diff", "--cached", "--name-status"],
    )
    paths: set[str] = set()
    for command in status_commands:
        paths.update(_name_status_paths(_run(command)))
    untracked = _run(["git", "ls-files", "--others", "--exclude-standard"])
    paths.update(line.strip() for line in untracked.splitlines() if line.strip())
    return sorted(paths)


def _changed_file_discovery_guardrail_failures() -> list[str]:
    old_receipt = "Docs/branch_records/example_receipt.md"
    renamed_path = "Docs/archive/example_receipt.md"
    parsed = _name_status_paths(
        f"R100\t{old_receipt}\t{renamed_path}\n"
        "M\tdev/orin_pr_review_churn_validation.py\n"
    )
    failures: list[str] = []
    if old_receipt not in parsed or renamed_path not in parsed:
        failures.append("Changed-file discovery omitted a rename source or destination")
    if _branch_receipt_candidates(sorted(parsed)) != [old_receipt]:
        failures.append(
            "Branch receipt discovery did not preserve a receipt renamed outside its owner directory"
        )
    return failures


def _select_matrix_path(
    requested_matrix: str | None,
    changed_files: list[str],
) -> tuple[Path, str]:
    if requested_matrix:
        requested_path = Path(requested_matrix)
        if not requested_path.is_absolute():
            requested_path = ROOT / requested_path
        return requested_path, "explicit --matrix"

    matrix_prefix = MATRIX_DIR.relative_to(ROOT).as_posix().casefold() + "/"
    changed_matrices = sorted(
        {
            path.replace("\\", "/")
            for path in changed_files
            if path.replace("\\", "/").casefold().startswith(matrix_prefix)
            and path.casefold().endswith(".json")
            and (ROOT / path).is_file()
        }
    )
    if len(changed_matrices) > 1:
        raise ValueError(
            "Multiple changed review-churn matrices require an explicit --matrix: "
            + ", ".join(changed_matrices)
        )
    if changed_matrices:
        return ROOT / changed_matrices[0], "single changed review-churn matrix"
    return DEFAULT_MATRIX, "global default"


def _matrix_selection_guardrail_failures() -> list[str]:
    failures: list[str] = []
    default_path, default_reason = _select_matrix_path(None, [])
    if default_path.resolve() != DEFAULT_MATRIX.resolve() or default_reason != "global default":
        failures.append("Matrix selection did not preserve the global default")

    changed_relative = "dev/fixtures/pr_review_churn/pr_311_user_review_bundle_matrix.json"
    deleted_relative = "dev/fixtures/pr_review_churn/pr_deleted_history_matrix.json"
    deleted_path, deleted_reason = _select_matrix_path(None, [deleted_relative])
    if deleted_path.resolve() != DEFAULT_MATRIX.resolve() or deleted_reason != "global default":
        failures.append("Matrix selection treated a deleted matrix as the active matrix")
    changed_path, changed_reason = _select_matrix_path(None, [changed_relative])
    if (
        changed_path.resolve() != (ROOT / changed_relative).resolve()
        or changed_reason != "single changed review-churn matrix"
    ):
        failures.append("Matrix selection did not choose the single changed matrix")

    explicit_path, explicit_reason = _select_matrix_path(changed_relative, [])
    if (
        explicit_path.resolve() != (ROOT / changed_relative).resolve()
        or explicit_reason != "explicit --matrix"
    ):
        failures.append("Matrix selection did not preserve an explicit matrix override")

    try:
        _select_matrix_path(
            None,
            [
                changed_relative,
                "dev/fixtures/pr_review_churn/pr_286_fam003_resident_access_matrix.json",
            ],
        )
    except ValueError:
        pass
    else:
        failures.append("Matrix selection accepted multiple changed matrices without --matrix")
    retained_path, retained_reason = _select_matrix_path(
        None,
        [changed_relative, deleted_relative],
    )
    if (
        retained_path.resolve() != (ROOT / changed_relative).resolve()
        or retained_reason != "single changed review-churn matrix"
    ):
        failures.append(
            "Matrix selection did not ignore a deleted matrix beside one retained matrix"
        )
    return failures


def _matrix_display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return str(resolved)


def _branch_receipt_write_set_text_failures(
    record_relative: str,
    text: str,
    changed_files: list[str],
) -> list[str]:
    matches = re.findall(
        r"^(?:-\s*)?Intended Write Set:\s*`([^`]*)`\s*$",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if not matches:
        if record_relative in changed_files:
            return [
                f"{record_relative}: changed branch receipt omits Intended Write Set"
            ]
        return []
    if len(matches) != 1:
        return [
            f"{record_relative}: changed branch receipt must contain exactly one "
            "Intended Write Set"
        ]
    recorded = {
        item.strip().replace("\\", "/")
        for item in matches[0].split(";")
        if item.strip()
    }
    changed = {item.replace("\\", "/") for item in changed_files}
    failures: list[str] = []
    missing = sorted(changed - recorded)
    stale = sorted(recorded - changed)
    if missing:
        failures.append(
            f"{record_relative}: Intended Write Set omits changed files: "
            + ", ".join(missing)
        )
    if stale:
        failures.append(
            f"{record_relative}: Intended Write Set lists files outside the current diff: "
            + ", ".join(stale)
        )
    return failures


def _branch_receipt_write_set_guardrail_failures() -> list[str]:
    record = "Docs/branch_records/feature_example.md"
    changed = [record, "dev/example_validator.py"]
    exact = (
        "Intended Write Set: `Docs/branch_records/feature_example.md; "
        "dev/example_validator.py`\n"
    )
    failures: list[str] = []
    if _branch_receipt_write_set_text_failures(record, exact, changed):
        failures.append("Branch receipt write-set guardrail rejected an exact diff")
    bulleted_exact = "- " + exact
    if _branch_receipt_write_set_text_failures(record, bulleted_exact, changed):
        failures.append(
            "Branch receipt write-set guardrail rejected a bulleted exact diff"
        )
    missing = _branch_receipt_write_set_text_failures(
        record,
        "Intended Write Set: `Docs/branch_records/feature_example.md`\n",
        changed,
    )
    if not any("omits changed files" in failure for failure in missing):
        failures.append("Branch receipt write-set guardrail missed an omitted changed file")
    stale = _branch_receipt_write_set_text_failures(
        record,
        exact.replace("`\n", "; dev/stale.py`\n"),
        changed,
    )
    if not any("outside the current diff" in failure for failure in stale):
        failures.append("Branch receipt write-set guardrail missed a stale listed file")
    no_field = _branch_receipt_write_set_text_failures(record, "# Branch Receipt\n", changed)
    if not any("omits Intended Write Set" in failure for failure in no_field):
        failures.append("Branch receipt write-set guardrail missed a changed receipt without a field")
    duplicate = _branch_receipt_write_set_text_failures(
        record,
        exact + exact,
        changed,
    )
    if not any("exactly one Intended Write Set" in failure for failure in duplicate):
        failures.append("Branch receipt write-set guardrail missed duplicate fields")
    unmapped_record = "Docs/branch_records/feature_unmapped_example.md"
    candidate_changed = [
        *changed,
        unmapped_record,
        "Docs/branch_records/index.md",
    ]
    candidates = _branch_receipt_candidates(candidate_changed)
    if candidates != [record, unmapped_record]:
        failures.append(
            "Branch receipt write-set guardrail did not discover every changed receipt or included the branch-record index"
        )
    active_receipt = (
        exact
        + "\n## Assigned Worktree Confinement\n\n"
        + "- Active Thread Owner: `Codex`\n"
        + "- Thread Assignment Status: `Assigned`\n"
    )
    if not _is_active_branch_receipt(active_receipt):
        failures.append("Branch receipt write-set guardrail rejected an active receipt")
    for marker in (
        "## Assigned Worktree Confinement\n",
        "- Active Thread Owner: `Codex`\n",
        "- Thread Assignment Status: `Assigned`\n",
    ):
        downgraded = active_receipt.replace(marker, "", 1)
        downgrade_failures = _active_receipt_downgrade_failures(
            record,
            downgraded,
            active_receipt,
        )
        if not any("active-to-unclassified downgrade" in failure for failure in downgrade_failures):
            failures.append(
                "Branch receipt write-set guardrail allowed an active receipt to drop "
                f"{marker.strip()}"
            )
    explicit_historical = "Phase: `Historical Traceability`\n" + active_receipt
    if _active_receipt_downgrade_failures(
        record,
        explicit_historical,
        active_receipt,
    ):
        failures.append(
            "Branch receipt write-set guardrail rejected an explicit historical transition"
        )
    downgraded_receipt = active_receipt.replace(
        "- Thread Assignment Status: `Assigned`\n", "", 1
    )
    for misleading_status in (
        "Status: `Not Historical`\n",
        "Record Status: `Non-Historical`\n",
        "Phase: `No Historical Transition`\n",
        "Status: `Historical fixture preserved`\n",
        "Status: `Historical evidence retained`\n",
    ):
        misleading_transition = misleading_status + downgraded_receipt
        downgrade_failures = _active_receipt_downgrade_failures(
            record,
            misleading_transition,
            active_receipt,
        )
        if not any(
            "active-to-unclassified downgrade" in failure
            for failure in downgrade_failures
        ):
            failures.append(
                "Branch receipt write-set guardrail treated an unrelated or negated historical "
                f"status as an explicit transition: {misleading_status.strip()}"
            )
    unbulleted_active_receipt = active_receipt.replace("- Active", "Active").replace(
        "- Thread", "Thread"
    )
    if not _is_active_branch_receipt(unbulleted_active_receipt):
        failures.append(
            "Branch receipt write-set guardrail rejected an unbulleted active receipt"
        )
    for phase_prefix in ("Phase:", "- Phase:"):
        historical_receipt = (
            f"{phase_prefix} `Historical Traceability`\n" + active_receipt
        )
        if _is_active_branch_receipt(historical_receipt):
            failures.append(
                "Branch receipt write-set guardrail treated a historical receipt as active"
            )
    active_with_historical_appendix = (
        active_receipt
        + "\n## Historical Phase Receipt\n\n"
        + "Current Phase: `Historical Traceability`\n"
    )
    if not _is_active_branch_receipt(active_with_historical_appendix):
        failures.append(
            "Branch receipt write-set guardrail let a historical appendix hide an active current summary"
        )
    active_after_historical_section = (
        exact
        + "\n## Current Phase\n\n"
        + "- Phase: `PR Readiness`\n"
        + "\n## Historical PR Readiness Stage 2 Execution Packet\n\n"
        + "- Status: `Historical Traceability`\n"
        + "\n## Assigned Worktree Confinement\n\n"
        + "- Active Thread Owner: `Codex`\n"
        + "- Thread Assignment Status: `Assigned`\n"
    )
    if not _is_active_branch_receipt(active_after_historical_section):
        failures.append(
            "Branch receipt write-set guardrail discarded current sections after a historical section"
        )
    appendix_only_assignment = (
        "# Historical Receipt\n\n"
        "## Historical Worktree Assignment\n\n"
        + exact
        + "\n### Assigned Worktree Confinement\n\n"
        + "- Active Thread Owner: `Codex`\n"
        + "- Thread Assignment Status: `Assigned`\n"
    )
    if _is_active_branch_receipt(appendix_only_assignment):
        failures.append(
            "Branch receipt write-set guardrail treated historical-only confinement evidence as active"
        )
    historical_without_write_set = (
        "Phase: `Historical Traceability`\n\n"
        "## Assigned Worktree Confinement\n\n"
        "- Active Thread Owner: `Historical receipt only`\n"
        "- Thread Assignment Status: `Closed`\n"
    )
    if _is_active_branch_receipt(historical_without_write_set):
        failures.append(
            "Branch receipt write-set guardrail required current scope from a historical receipt"
        )
    if _missing_branch_receipt_failures(record, historical_without_write_set):
        failures.append(
            "Branch receipt write-set guardrail rejected deletion of a historical receipt"
        )
    missing_active = _missing_branch_receipt_failures(record, active_receipt)
    if not any("missing active branch receipt" in failure for failure in missing_active):
        failures.append(
            "Branch receipt write-set guardrail allowed deletion of an active receipt"
        )
    missing_untracked = _missing_branch_receipt_failures(record, None)
    if not any("missing and absent from base" in failure for failure in missing_untracked):
        failures.append(
            "Branch receipt write-set guardrail allowed an unexplained missing receipt"
        )
    return failures


def _branch_receipt_candidates(
    changed_files: list[str],
) -> list[str]:
    changed = {path.replace("\\", "/") for path in changed_files}
    return sorted(
        path
        for path in changed
        if path.startswith("Docs/branch_records/")
        and path.casefold().endswith(".md")
        and Path(path).name.casefold() != "index.md"
    )


def _current_branch_receipt_summary(text: str) -> str:
    current_lines: list[str] = []
    historical_level: int | None = None
    for line in text.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            if historical_level is not None and level <= historical_level:
                historical_level = None
            if re.search(r"\bhistorical\b", heading.group(2), flags=re.IGNORECASE):
                historical_level = level
                continue
        if historical_level is None:
            current_lines.append(line)
    return "\n".join(current_lines)


def _is_historical_branch_receipt(text: str) -> bool:
    return bool(re.search(
        r"^(?:-\s*)?(?:Phase|Current Phase|Branch Authority Status|Record Status):"
        r"\s*`?\s*(?:historical(?:\s+released)?\s+traceability|"
        r"historical(?:\s+(?:released|rollback|projection))?\s+receipt(?:\s+only)?)\b",
        _current_branch_receipt_summary(text),
        flags=re.IGNORECASE | re.MULTILINE,
    ))


def _is_active_branch_receipt(text: str) -> bool:
    current_summary = _current_branch_receipt_summary(text)
    return bool(
        not _is_historical_branch_receipt(text)
        and re.search(
            r"^## Assigned Worktree Confinement\s*$",
            current_summary,
            flags=re.IGNORECASE | re.MULTILINE,
        )
        and re.search(
            r"^(?:-\s*)?Active Thread Owner:\s*`?\S",
            current_summary,
            flags=re.IGNORECASE | re.MULTILINE,
        )
        and re.search(
            r"^(?:-\s*)?Thread Assignment Status:\s*`?\S",
            current_summary,
            flags=re.IGNORECASE | re.MULTILINE,
        )
    )


def _active_receipt_downgrade_failures(
    record_relative: str,
    current_text: str,
    base_text: str | None,
) -> list[str]:
    if (
        base_text is None
        or not _is_active_branch_receipt(base_text)
        or _is_active_branch_receipt(current_text)
        or _is_historical_branch_receipt(current_text)
    ):
        return []
    return [
        f"{record_relative}: active-to-unclassified downgrade removed required "
        "branch-receipt markers without an explicit historical transition"
    ]


def _missing_branch_receipt_failures(
    record_relative: str,
    base_text: str | None,
) -> list[str]:
    if base_text is None:
        return [f"{record_relative}: routed branch receipt is missing and absent from base"]
    if _is_active_branch_receipt(base_text):
        return [f"{record_relative}: missing active branch receipt from base revision"]
    return []


def _file_text_at_revision(revision: str, relative_path: str) -> str | None:
    normalized_path = relative_path.replace("\\", "/")
    code, output = _run_for_status(
        ["git", "show", f"{revision}:{normalized_path}"]
    )
    return output if code == 0 else None


def _branch_receipt_write_set_failures(
    changed_files: list[str],
    *,
    base: str,
) -> list[str]:
    failures: list[str] = []
    for record_relative in _branch_receipt_candidates(changed_files):
        record_path = ROOT / record_relative
        if not record_path.is_file():
            failures.extend(
                _missing_branch_receipt_failures(
                    record_relative,
                    _file_text_at_revision(base, record_relative),
                )
            )
            continue
        record_text = record_path.read_text(encoding="utf-8")
        if not _is_active_branch_receipt(record_text):
            failures.extend(
                _active_receipt_downgrade_failures(
                    record_relative,
                    record_text,
                    _file_text_at_revision(base, record_relative),
                )
            )
            continue
        failures.extend(
            _branch_receipt_write_set_text_failures(
                record_relative,
                record_text,
                changed_files,
            )
        )
    return failures


def _inventory_receipt_line_count_text_failures(
    record_relative: str,
    record_text: str,
    audit_text: str,
) -> list[str]:
    quoted_record = f"`{record_relative}`"
    observed_counts: dict[str, list[int]] = {
        "inventory table": [],
        "file-review table": [],
        "per-file dossier": [],
    }
    audit_lines = audit_text.splitlines()
    for index, line in enumerate(audit_lines):
        if quoted_record not in line:
            continue
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            try:
                record_index = cells.index(quoted_record)
            except ValueError:
                continue
            for cell in cells[record_index + 1 :]:
                if cell.isdigit():
                    surface = (
                        "file-review table"
                        if record_index == 0
                        else "inventory table"
                    )
                    observed_counts[surface].append(int(cell))
                    break
            continue
        if not stripped.startswith("### "):
            continue
        for detail_line in audit_lines[index + 1 :]:
            if detail_line.startswith("### "):
                break
            match = re.match(r"^- Line count:\s*(\d+)\s*$", detail_line)
            if match:
                observed_counts["per-file dossier"].append(int(match.group(1)))
                break

    expected_count = record_text.count("\n") + (1 if record_text else 0)
    invalid_surfaces = [
        f"{surface}={len(counts)}"
        for surface, counts in observed_counts.items()
        if len(counts) != 1
    ]
    if invalid_surfaces:
        return [
            f"{record_relative}: generated docs inventory must contain exactly one of each "
            "receipt line-count surface; " + ", ".join(invalid_surfaces)
        ]
    stale_counts = sorted(
        {
            count
            for counts in observed_counts.values()
            for count in counts
            if count != expected_count
        }
    )
    if stale_counts:
        return [
            f"{record_relative}: generated docs inventory has stale line counts "
            f"{stale_counts}; expected {expected_count}"
        ]
    return []


def _inventory_receipt_expected_content(
    record_relative: str,
    record_text: str,
    changed_files: list[str],
) -> dict[str, str]:
    changed = {path.replace("\\", "/") for path in changed_files}
    lines = record_text.count("\n") + (1 if record_text else 0)
    owner = docs_inventory.owner_for(record_relative)
    owns, should_record, should_move = docs_inventory.OWNER_DESCRIPTIONS[owner]
    active_branch_plan_paths: set[str] = set()
    action, completed, remaining = docs_inventory.action_for(
        record_relative,
        owner,
        lines,
        changed,
        active_branch_plan_paths=active_branch_plan_paths,
        retired_branch_plan_paths=docs_inventory.retired_branch_plan_paths(),
    )
    counts = {
        name: docs_inventory.count_matches(record_text, patterns)
        for name, patterns in docs_inventory.PATTERNS.items()
    }
    duplicate_classes = [
        fact
        for fact, patterns in docs_inventory.FACT_CLASSES.items()
        if docs_inventory.count_matches(record_text, patterns)
    ]
    ambiguity_risk, ambiguity_hits, ambiguity_action = docs_inventory.ambiguity_for(
        record_text, owner
    )
    structure_risk, structure_action = docs_inventory.structure_for(
        record_text, lines, owner
    )
    risk = "Low"
    if record_relative in {"Docs/feature_backlog.md", "Docs/prebeta_roadmap.md"}:
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
    row: dict[str, Any] = {
        "rel": record_relative,
        "lines": lines,
        "owner": owner,
        "action": action,
        "risk": risk,
        "confidence": confidence,
        "counts": counts,
        "title": docs_inventory.heading_title(record_text, Path(record_relative).stem),
        "owns": owns,
        "should_record": should_record,
        "should_move": should_move,
        "completed": completed,
        "remaining": remaining,
        "duplicate_classes": duplicate_classes,
        "ambiguity_risk": ambiguity_risk,
        "ambiguity_hits": ambiguity_hits,
        "ambiguity_action": ambiguity_action,
        "structure_risk": structure_risk,
        "structure_action": structure_action,
        "active_branch_plan": (
            owner == "branch runtime engineering plan"
            and record_relative in active_branch_plan_paths
        ),
        "live_fields": docs_inventory.snippets(record_text, docs_inventory.PATTERNS["live"]),
        "receipt_fields": docs_inventory.snippets(
            record_text,
            (
                r"Historical",
                r"Receipt",
                r"USER",
                r"Decision",
                r"Approval",
                r"Closeout",
                r"Merge Proof",
            ),
        ),
        "current_markers": docs_inventory.snippets(
            record_text, (r"Current", r"Active", r"Next Legal Phase", r"Phase Status")
        ),
        "trace_markers": docs_inventory.snippets(
            record_text, docs_inventory.PATTERNS["package_slice"]
        ),
        "branch_markers": docs_inventory.snippets(
            record_text, docs_inventory.PATTERNS["branch_phase"]
        ),
        "release_markers": docs_inventory.snippets(
            record_text, docs_inventory.PATTERNS["pr_release_issue"]
        ),
    }
    row["consolidation_target"] = docs_inventory.consolidation_target_for(row)
    row["deletion_posture"] = docs_inventory.deletion_posture_for(row)

    user_decision = (
        "Yes"
        if "USER" in str(row["deletion_posture"]) or "USER" in str(row["action"])
        else "No"
    )
    duplicate_found = bool(row["duplicate_classes"])
    live_found = bool(row["live_fields"]) or counts["live"] > 0
    receipt_found = bool(row["receipt_fields"])
    manifest_tail = (
        f"`{record_relative}` | {owner} | {lines} | {action} | "
        f"{risk} | {confidence} |"
    )
    cleanup_row = (
        f"| `{record_relative}` | {owner} | {action} | "
        f"{docs_inventory.compact_review_value(str(row['consolidation_target']), 140)} | "
        f"{docs_inventory.compact_review_value(str(row['deletion_posture']), 120)} | "
        f"{user_decision} |"
    )
    ambiguity_row = (
        f"| `{record_relative}` | {ambiguity_risk} | "
        f"{docs_inventory.md_list(list(ambiguity_hits))} | "
        f"{docs_inventory.compact_review_value(str(ambiguity_action), 140)} |"
    )
    structure_row = (
        f"| `{record_relative}` | {structure_risk} | "
        f"{docs_inventory.compact_review_value(str(structure_action), 150)} |"
    )
    file_review_row = (
        f"| `{record_relative}` | {lines} | "
        f"{docs_inventory.compact_review_value(str(row['title']))} | {owner} | "
        f"{docs_inventory.compact_review_value(str(owns))} | "
        f"{docs_inventory.compact_review_value(str(should_record))} | "
        f"{docs_inventory.compact_review_value(str(completed))} | "
        f"{docs_inventory.compact_review_value(str(remaining))} | {action} | "
        f"{ambiguity_risk} | {structure_risk} | "
        f"{docs_inventory.bool_text(duplicate_found)} | "
        f"{docs_inventory.bool_text(live_found)} | "
        f"{docs_inventory.bool_text(receipt_found)} | "
        f"{docs_inventory.compact_review_value(docs_inventory.validator_need(owner))} | "
        "_Add notes here._ |"
    )
    repetitive = (
        "Release/phase/branch marker repetition requires owner-pointer discipline."
        if counts["branch_phase"] > 20 or counts["pr_release_issue"] > 20
        else "No major repetitive language flagged by scanner."
    )
    duplicates = ", ".join(duplicate_classes) if duplicate_classes else "None found"
    dossier_lines = [
        f"- File path: `{record_relative}`",
        f"- Line count: {lines}",
        f"- Current purpose: {row['title']}",
        (
            f"- Actual observed use: {owner} with markers live={counts['live']}, "
            f"pr/release/issue={counts['pr_release_issue']}, "
            f"package/slice={counts['package_slice']}, "
            f"branch/worktree/phase={counts['branch_phase']}, "
            f"validator/helper={counts['validator']}."
        ),
        f"- Correct owner category: {owner}",
        f"- What gets recorded here: {owns}.",
        f"- What should be recorded here: {should_record}.",
        f"- What should move elsewhere: {should_move}.",
        f"- Migration target: {should_move}.",
        f"- Recommendation: {action}.",
        f"- Consolidation target: {row['consolidation_target']}.",
        f"- Deletion posture: {row['deletion_posture']}.",
        f"- Ambiguity risk: {ambiguity_risk}.",
        f"- Ambiguity signals: {docs_inventory.md_list(list(ambiguity_hits))}",
        f"- Ambiguity review action: {ambiguity_action}",
        f"- Structure risk: {structure_risk}.",
        f"- Structure action: {structure_action}",
        f"- Duplicate fact classes found: {duplicates}.",
        f"- Live operational truth fields found: {docs_inventory.md_list(row['live_fields'])}",
        f"- Governance receipt fields found: {docs_inventory.md_list(row['receipt_fields'])}",
        f"- Repetitive language found: {repetitive}",
        f"- Current-state markers found: {docs_inventory.md_list(row['current_markers'])}",
        f"- Package Trace / Slice Trace markers found: {docs_inventory.md_list(row['trace_markers'])}",
        f"- Branch/worktree/phase markers found: {docs_inventory.md_list(row['branch_markers'])}",
        f"- Release/PR/issue markers found: {docs_inventory.md_list(row['release_markers'])}",
        f"- Validator rule needed: {docs_inventory.validator_need(owner)}",
        f"- Reform action completed in this branch: {completed}",
        f"- Remaining action needed after this branch: {remaining}",
        "- USER review notes: _Add notes here._",
    ]
    return {
        "manifest_tail": manifest_tail,
        "cleanup_row": cleanup_row,
        "ambiguity_row": ambiguity_row,
        "structure_row": structure_row,
        "file_review_row": file_review_row,
        "dossier_body": "\n".join(dossier_lines),
    }


def _inventory_receipt_content_text_failures(
    record_relative: str,
    record_text: str,
    audit_text: str,
    changed_files: list[str],
) -> list[str]:
    expected = _inventory_receipt_expected_content(
        record_relative, record_text, changed_files
    )
    failures: list[str] = []
    manifest_pattern = re.compile(
        rf"^\| \d+ \| {re.escape(expected['manifest_tail'])}$",
        flags=re.MULTILINE,
    )
    if len(manifest_pattern.findall(audit_text)) != 1:
        failures.append(
            f"{record_relative}: generated docs inventory has stale manifest content"
        )
    for surface, key in (
        ("cleanup/disposition", "cleanup_row"),
        ("ambiguity", "ambiguity_row"),
        ("structure", "structure_row"),
        ("file-review", "file_review_row"),
    ):
        if audit_text.splitlines().count(expected[key]) != 1:
            failures.append(
                f"{record_relative}: generated docs inventory has stale {surface} content"
            )
    dossier_pattern = re.compile(
        rf"^### \d+\. `{re.escape(record_relative)}`\s*$\n\n"
        r"(?P<body>.*?)(?=^### \d+\. `|^## Remaining Risks\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    dossier_matches = list(dossier_pattern.finditer(audit_text))
    if (
        len(dossier_matches) != 1
        or dossier_matches[0].group("body").strip() != expected["dossier_body"]
    ):
        failures.append(
            f"{record_relative}: generated docs inventory has stale dossier content"
        )
    return failures


def _inventory_deleted_receipt_text_failures(
    record_relative: str,
    audit_text: str,
) -> list[str]:
    if record_relative not in audit_text:
        return []
    return [
        f"{record_relative}: generated docs inventory retains a deleted receipt path"
    ]


def _inventory_receipt_line_count_guardrail_failures() -> list[str]:
    record = "Docs/branch_records/feature_example.md"
    record_text = "first\nsecond\n"
    exact_audit = (
        f"| 1 | `{record}` | branch receipt | 3 | Keep |\n"
        f"| `{record}` | 3 | Receipt |\n"
        f"### 1. `{record}`\n\n- Line count: 3\n"
    )
    failures: list[str] = []
    if _inventory_receipt_line_count_text_failures(record, record_text, exact_audit):
        failures.append("Inventory receipt currentness guardrail rejected exact counts")
    stale = _inventory_receipt_line_count_text_failures(
        record,
        record_text,
        exact_audit.replace("| 3 | Keep", "| 2 | Keep", 1),
    )
    if not any("stale line counts" in failure for failure in stale):
        failures.append("Inventory receipt currentness guardrail missed a stale count")
    missing = _inventory_receipt_line_count_text_failures(
        record,
        record_text,
        exact_audit.split("### 1.", 1)[0],
    )
    if not any("exactly one of each" in failure for failure in missing):
        failures.append("Inventory receipt currentness guardrail missed a generated surface")
    duplicate_substitution = _inventory_receipt_line_count_text_failures(
        record,
        record_text,
        (f"| 1 | `{record}` | branch receipt | 3 | Keep |\n" * 3),
    )
    if not any("exactly one of each" in failure for failure in duplicate_substitution):
        failures.append(
            "Inventory receipt currentness guardrail let duplicate rows substitute for missing surfaces"
        )
    content_record_text = "# Example Receipt\nStatus: Active\n"
    expected_content = _inventory_receipt_expected_content(
        record,
        content_record_text,
        [record],
    )
    exact_content_audit = "\n".join(
        (
            f"| 1 | {expected_content['manifest_tail']}",
            expected_content["cleanup_row"],
            expected_content["ambiguity_row"],
            expected_content["structure_row"],
            expected_content["file_review_row"],
            f"### 1. `{record}`",
            "",
            expected_content["dossier_body"],
            "",
            "## Remaining Risks",
        )
    )
    if _inventory_receipt_content_text_failures(
        record,
        content_record_text,
        exact_content_audit,
        [record],
    ):
        failures.append(
            "Inventory receipt currentness guardrail rejected exact generated content"
        )
    for stale_record_text, stale_surface in (
        ("# Renamed Receipt\nStatus: Active\n", "title"),
        ("# Example Receipt\nStatus: Historical\n", "classification"),
        ("# Example Receipt\nStatus: Current\n", "excerpt"),
    ):
        content_failures = _inventory_receipt_content_text_failures(
            record,
            stale_record_text,
            exact_content_audit,
            [record],
        )
        if not any("stale" in failure for failure in content_failures):
            failures.append(
                "Inventory receipt currentness guardrail missed stale generated "
                f"{stale_surface} content"
            )
    if _inventory_deleted_receipt_text_failures(record, "# Current inventory\n"):
        failures.append(
            "Inventory receipt currentness guardrail rejected removal of a deleted receipt"
        )
    retained_deleted = _inventory_deleted_receipt_text_failures(record, exact_audit)
    if not any("retains a deleted receipt path" in failure for failure in retained_deleted):
        failures.append(
            "Inventory receipt currentness guardrail missed a stale deleted-receipt path"
        )
    missing_audit = _docs_inventory_receipt_currentness_failures([record])
    if not any("requires regenerated docs inventory" in failure for failure in missing_audit):
        failures.append(
            "Inventory receipt currentness guardrail missed a changed receipt without inventory regeneration"
        )
    return failures


def _inventory_checkout_independence_guardrail_failures() -> list[str]:
    original_git_output = docs_inventory.git_output
    rendered: list[tuple[str, str]] = []
    try:
        for checkout_branch in (
            "feature/fam-007-local-ai-provider-setup-implementation-foundation",
            "",
        ):
            def checkout_git_output(*args: str, branch: str = checkout_branch) -> str:
                if args == ("branch", "--show-current"):
                    return branch
                return original_git_output(*args)

            docs_inventory.git_output = checkout_git_output
            rendered.append(
                docs_inventory.generate(
                    changed_files=[],
                    write_outputs=False,
                    report=False,
                )
            )
    finally:
        docs_inventory.git_output = original_git_output
    if rendered[0] != rendered[1]:
        return [
            "Docs inventory rendering changes between named-branch and detached checkouts"
        ]
    return []


def _docs_inventory_receipt_currentness_failures(
    changed_files: list[str],
    *,
    base: str = "origin/main",
) -> list[str]:
    audit_relative = "Docs/governance_docs_full_inventory_reform_audit.md"
    changed = {path.replace("\\", "/") for path in changed_files}
    receipt_candidates = _branch_receipt_candidates(changed_files)
    if not receipt_candidates:
        return []
    if audit_relative not in changed:
        return [
            "Changed branch receipt requires regenerated docs inventory in the current diff"
        ]
    audit_path = ROOT / audit_relative
    if not audit_path.is_file():
        return [f"{audit_relative}: changed generated inventory is missing"]
    audit_text = audit_path.read_text(encoding="utf-8")
    failures: list[str] = []
    rendered_audit, rendered_index = docs_inventory.generate(
        base=base,
        changed_files=changed_files,
        write_outputs=False,
        report=False,
    )
    if audit_text != rendered_audit:
        failures.append(
            f"{audit_relative}: committed inventory does not match current generator output"
        )
    index_relative = "Docs/governance_docs_reform_user_review_index.md"
    index_path = ROOT / index_relative
    if not index_path.is_file():
        failures.append(f"{index_relative}: generated review index is missing")
    elif index_path.read_text(encoding="utf-8") != rendered_index:
        failures.append(
            f"{index_relative}: committed review index does not match current generator output"
        )
    for record_relative in receipt_candidates:
        record_path = ROOT / record_relative
        if not record_path.is_file():
            failures.extend(
                _inventory_deleted_receipt_text_failures(
                    record_relative,
                    audit_text,
                )
            )
            continue
        failures.extend(
            _inventory_receipt_line_count_text_failures(
                record_relative,
                record_path.read_text(encoding="utf-8"),
                audit_text,
            )
        )
        failures.extend(
            _inventory_receipt_content_text_failures(
                record_relative,
                record_path.read_text(encoding="utf-8"),
                audit_text,
                changed_files,
            )
        )
    return failures


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
            and _is_standalone_connector_green(body)
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
        is_green_summary = _is_connector_login(author) and _is_standalone_connector_green(
            body
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
    allowed_families = set(entries)
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
            classified = set(_classify_comment(comment, allowed_families))
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
            classified = _classify_comment(comment, allowed_families)
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
    changed_files = _changed_files(args.base)
    matrix_path, matrix_selection = _select_matrix_path(args.matrix, changed_files)
    matrix = _load_matrix(matrix_path)
    changed_helper_files = [
        path for path in changed_files if _is_firewall_gated_path(path, matrix)
    ]
    changed_families = _families_for_changed_files(matrix, changed_helper_files)
    failures: list[str] = []
    failures.extend(_classifier_guardrail_failures())
    failures.extend(_matrix_selection_guardrail_failures())
    failures.extend(_changed_file_discovery_guardrail_failures())
    failures.extend(_branch_receipt_write_set_guardrail_failures())
    failures.extend(_inventory_receipt_line_count_guardrail_failures())
    failures.extend(_inventory_checkout_independence_guardrail_failures())
    failures.extend(_branch_receipt_write_set_failures(changed_files, base=args.base))
    failures.extend(
        _docs_inventory_receipt_currentness_failures(
            changed_files,
            base=args.base,
        )
    )
    failures.extend(_validate_matrix(matrix, changed_families, changed_helper_files))
    firewall_failures, firewall_lines = _validate_pre_pr_firewall(
        matrix, changed_helper_files, skip_commands=args.skip_pre_pr_commands
    )
    failures.extend(firewall_failures)

    lines = [
        "Pre-PR Adversarial Review Firewall",
        f"Base: {args.base}",
        f"Matrix: {_matrix_display_path(matrix_path)} ({matrix_selection})",
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
    review_summaries, review_summary_page_count = _rest_paginated_pages(
        f"repos/{owner}/{name}/pulls/{args.pr}/reviews"
    )
    changed_files = _changed_files(args.base)
    matrix_path, matrix_selection = _select_matrix_path(args.matrix, changed_files)
    matrix = _load_matrix(matrix_path)
    allowed_families = set(_family_entries(matrix))
    comments = _connector_review_comments(review_comments, allowed_families)
    comments.extend(
        _connector_review_summary_comments(
            review_summaries,
            allowed_families,
            pull_request["headRefOid"],
        )
    )
    thread_counts = _thread_counts(threads)
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
    failures.extend(_matrix_selection_guardrail_failures())
    failures.extend(_changed_file_discovery_guardrail_failures())
    failures.extend(_branch_receipt_write_set_guardrail_failures())
    failures.extend(_inventory_receipt_line_count_guardrail_failures())
    failures.extend(_inventory_checkout_independence_guardrail_failures())
    failures.extend(_branch_receipt_write_set_failures(changed_files, base=args.base))
    failures.extend(
        _docs_inventory_receipt_currentness_failures(
            changed_files,
            base=args.base,
        )
    )
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
        f"Matrix: {_matrix_display_path(matrix_path)} ({matrix_selection})",
        f"Mergeability: {pull_request.get('mergeable')} / {pull_request.get('mergeStateStatus')}",
        f"Review-thread pages inspected: {page_count}",
        f"Review-comment pages inspected: {review_comment_page_count}",
        f"Review-summary pages inspected: {review_summary_page_count}",
        (
            "Review-thread counts: "
            f"total={thread_counts['total']}, "
            f"resolved={thread_counts['resolved']}, "
            f"unresolved={thread_counts['unresolved']}, "
            f"unresolved_current={thread_counts['unresolved_current']}, "
            f"outdated={thread_counts['outdated']}"
        ),
        f"Connector review findings collected: {len(comments)}",
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
    parser.add_argument(
        "--matrix",
        help=(
            "Review-churn matrix path. When omitted, use the single changed matrix "
            "or the global default if no matrix changed."
        ),
    )
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
