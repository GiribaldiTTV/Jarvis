"""Classify legacy workspace-root strings and reject current C-root routing."""
# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-RELOCATION-CLOSURE-015; surface=workspace-root-residue-validator; status=canonical
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from nexus_paths import EXTERNAL_STATE_ROOT, USER_HUB_ROOT, WORKTREES_ROOT

ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOTS = (
    r"C:\Nexus Worktrees",
    r"C:\Nexus USER",
    r"C:\Nexus Governance State",
)
LEGACY_ROOT_PATTERN = re.compile(
    r"C:[/\\\\]{1,4}Nexus (Worktrees|USER|Governance State)",
    re.IGNORECASE,
)
CURRENT_ROOTS = {
    r"C:\Nexus Worktrees": str(WORKTREES_ROOT),
    r"C:\Nexus USER": str(USER_HUB_ROOT),
    r"C:\Nexus Governance State": str(EXTERNAL_STATE_ROOT),
}
HISTORICAL_WORDS = re.compile(
    r"\b(historical|legacy|older|old|superseded|rollback|fixture|example|snapshot|"
    r"prior|pre[- ]migration|stale|forbidden|cleanup|migration|retired|receipt|"
    r"rejected|known[- ]bad|reconstructed|temporary)\b",
    re.IGNORECASE,
)
TEXT_EXTENSIONS = {
    ".md",
    ".py",
    ".pyw",
    ".ps1",
    ".vbs",
    ".json",
    ".txt",
    ".yaml",
    ".yml",
}
HISTORICAL_DOCUMENTS = {
    "governance_docs_full_inventory_reform_audit.md",
    "governance_reliability_and_repo_split_reform_candidates.md",
    "governance_phase_lifecycle_reform_context_plan.md",
}
HISTORICAL_EVIDENCE_HELPERS = {
    "orin_fam006_full_desktop_false_green_review.py",
    "orin_fam006_live_validation_forensics.py",
}
TEST_ONLY_HELPERS = {
    "orin_branch_governance_validation.py",
    "orin_branch_readiness_planning_fixture_validation.py",
    "orin_external_state_target_currentness_fixture_validation.py",
    "orin_pr_review_churn_validation.py",
    "orin_user_review_bundle_false_green_fixture_validation.py",
}
POLICY_DOCUMENTS = {
    "validation_helper_registry.md",
}


def _iter_files(scan_root: Path):
    if scan_root.is_file():
        yield scan_root
        return
    for path in scan_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def _contains_legacy_root(line: str) -> bool:
    return LEGACY_ROOT_PATTERN.search(line) is not None


def _document_declares_historical(path: Path) -> bool:
    if path.name == "README.md":
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return bool(
        re.search(
            r"Current Phase:\s*`?Historical(?: Traceability| projection)?|"
            r"historical (?:branch|transition) receipt|repo copies are historical|"
            r"returned[- ]UTS|temporary reference|visual inspection matrix|branch-local evidence",
            text,
            re.IGNORECASE,
        )
        or (
            "Branch Runtime Engineering Plan" in text
            and "Branch Authority Record Pointer" in text
        )
    )


def classify_line(
    path: Path,
    line: str,
    *,
    fixture_mode: bool = False,
    context: str = "",
) -> str | None:
    if not _contains_legacy_root(line):
        return None
    if not fixture_mode and path.name in {
        "orin_workspace_root_residue_validation.py",
        "orin_guarded_c_root_cleanup.py",
    }:
        return "policy"
    if not fixture_mode and path.name in TEST_ONLY_HELPERS:
        return "test-only"
    if not fixture_mode and path.name in HISTORICAL_EVIDENCE_HELPERS:
        return "historical"
    if not fixture_mode and path.name in POLICY_DOCUMENTS:
        return "policy"
    if (
        not fixture_mode
        and path.name == "orin_user_review_bundle.py"
        and "FAM-003-20260623-125842" in line
    ):
        return "historical"
    if not fixture_mode and path.name in HISTORICAL_DOCUMENTS:
        return "historical"
    if not fixture_mode and ("fixtures" in path.parts or "branch_records" in path.parts):
        return "historical"
    if not fixture_mode and "branch_plans" in path.parts and _document_declares_historical(path):
        return "historical"
    if HISTORICAL_WORDS.search(line) or HISTORICAL_WORDS.search(context):
        return "historical"
    return "current"


def scan(scan_root: Path, *, fixture_mode: bool = False) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for path in _iter_files(scan_root):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line_number, line in enumerate(lines, 1):
            context = "\n".join(lines[max(0, line_number - 7) : line_number])
            classification = classify_line(
                path,
                line,
                fixture_mode=fixture_mode,
                context=context,
            )
            if classification:
                findings.append(
                    {
                        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                        "line": line_number,
                        "classification": classification,
                        "text": line.strip(),
                    }
                )
    return findings


def run_fixture_tests() -> list[str]:
    fixture_root = ROOT / "dev" / "fixtures" / "workspace_root_residue"
    failures: list[str] = []
    valid = scan(fixture_root / "valid_historical_receipt.md", fixture_mode=True)
    invalid = scan(fixture_root / "invalid_current_helper.py", fixture_mode=True)
    invalid_launcher = scan(fixture_root / "invalid_current_launcher.vbs", fixture_mode=True)
    if not valid or any(item["classification"] != "historical" for item in valid):
        failures.append("valid historical fixture was not classified as historical")
    if not invalid or not any(item["classification"] == "current" for item in invalid):
        failures.append("invalid current-helper fixture was not classified as current")
    if not invalid_launcher or not any(
        item["classification"] == "current" for item in invalid_launcher
    ):
        failures.append("invalid current-launcher fixture was not classified as current")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT), help="Repository root to scan.")
    parser.add_argument("--output", help="Optional JSON report path.")
    parser.add_argument("--run-fixture-tests", action="store_true")
    args = parser.parse_args()

    scan_root = Path(args.root).resolve()
    findings = scan(scan_root / "dev") + scan(scan_root / "Docs")
    fixture_failures = run_fixture_tests() if args.run_fixture_tests else []
    current = [item for item in findings if item["classification"] == "current"]
    report = {
        "canonical_roots": {
            "worktrees": str(WORKTREES_ROOT),
            "user": str(USER_HUB_ROOT),
            "external_state": str(EXTERNAL_STATE_ROOT),
        },
        "finding_count": len(findings),
        "historical_count": len(findings) - len(current),
        "current_count": len(current),
        "findings": findings,
        "current_findings": current,
        "fixture_failures": fixture_failures,
    }
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if current or fixture_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
