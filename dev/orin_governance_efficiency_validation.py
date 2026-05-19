"""Validate the governance efficiency operating model.

This helper is intentionally small and report-only. It checks that the compact
governance reform model exists, is discoverable from the routing docs, and keeps
backlog/roadmap from absorbing detailed runtime-branch planning narrative.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPERATING_MODEL = Path("Docs/governance_efficiency_operating_model.md")

REQUIRED_MODEL_PHRASES = (
    "Rule ID And Owner Model",
    "Source-Truth Ownership Matrix",
    "Derived Live Truth Versus Historical Receipt",
    "Duplicate Live-State Guard",
    "Current Summary And Historical Appendix Split",
    "Phase Alias UX",
    "Branch Planning UX Standard",
    "Standing Governance Ledger Compaction",
    "Release Ownership UX",
    "Public Language Mapping",
    "Validator Modularization Boundary",
    "Validation Runner And Registry Query Rule",
    "Naming Drift Scan Rule",
    "Reform Pass Completion Model",
)

POINTER_REQUIREMENTS = {
    Path("Docs/Main.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "governance efficiency operating model",
    ),
    Path("Docs/phase_governance.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "canonical phase names remain unchanged",
    ),
    Path("Docs/development_rules.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "Rule ID",
    ),
    Path("Docs/codex_modes.md"): (
        "Docs/governance_efficiency_operating_model.md",
        "smallest legal",
    ),
    Path("Docs/validation_helper_registry.md"): (
        "dev/orin_governance_efficiency_validation.py",
        "governance efficiency operating model",
    ),
    Path("Docs/governance_process_efficiency_reform_plan.md"): (
        "Consolidated Governance Reform Pass",
        "Docs/governance_efficiency_operating_model.md",
    ),
}

BACKLOG_ROADMAP_COMPACTNESS_FORBIDDEN = (
    "Per-Seam Implementation Checklist:",
    "Per-Seam Validation Checklist:",
    "Per-Seam User-Facing Proof Checklist:",
    "Plan-To-Implementation Traceability Table:",
    "Hardening Comparison Checklist:",
    "Live Validation Proof Or Waiver Checklist:",
    "PR Readiness Fold-Down / Retention Checklist:",
    "Release Readiness Public-Scope Translation Checklist:",
)


def _read(relative_path: Path) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def validate() -> list[str]:
    failures: list[str] = []

    model_text = _read(OPERATING_MODEL)
    if not model_text:
        failures.append(f"{OPERATING_MODEL}: missing governance efficiency operating model")
    else:
        for phrase in REQUIRED_MODEL_PHRASES:
            if phrase not in model_text:
                failures.append(
                    f"{OPERATING_MODEL}: missing required section or phrase {phrase!r}"
                )

    for path, required_phrases in POINTER_REQUIREMENTS.items():
        text = _read(path)
        if not text:
            failures.append(f"{path}: missing required pointer document")
            continue
        for phrase in required_phrases:
            if phrase not in text:
                failures.append(f"{path}: missing governance efficiency pointer {phrase!r}")

    for path in (Path("Docs/feature_backlog.md"), Path("Docs/prebeta_roadmap.md")):
        text = _read(path)
        if not text:
            failures.append(f"{path}: missing compact current-state owner")
            continue
        for phrase in BACKLOG_ROADMAP_COMPACTNESS_FORBIDDEN:
            if phrase in text:
                failures.append(
                    f"{path}: detailed Branch Runtime Engineering Plan marker {phrase!r} "
                    "belongs in Docs/branch_plans or folded historical receipts, not backlog/roadmap"
                )

    return failures


def main() -> int:
    failures = validate()
    if failures:
        print("FAIL: governance efficiency validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: governance efficiency validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
