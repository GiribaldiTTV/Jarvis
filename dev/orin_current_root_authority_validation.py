"""Independent final-D current-root authority adjudicator.

This helper is deliberately declarative and diverse from the prose owners it
checks.  It validates current-root ownership, preserves explicitly historical
or rollback C references, checks the mutable external-state header, proves the
carrier/overlay parity set, and runs negative fixtures for the known false
green classes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CURRENT_REPO = Path(r"D:\Nexus Desktop AI\Product Repository")
CURRENT_WORKTREES = Path(r"D:\Nexus Desktop AI\Worktrees")
CURRENT_STATE = Path(r"D:\Nexus Desktop AI\Governance State")
CURRENT_USER = Path(r"D:\Nexus Desktop AI\USER")
ROLLBACK_REPO = Path(r"C:\Nexus Desktop AI")
OLD_DATA_ROOT = r"D:\Nexus Desktop AI Data"
OLD_STATE_ROOT = r"C:\Nexus Governance State"
OLD_WORKTREE_ROOT = r"C:\Nexus Worktrees"
OLD_USER_ROOT = r"C:\Nexus USER"

ADMITTED_FILES = (
    "Docs/Main.md",
    "Docs/nexus_startup_contract.md",
    "Docs/nexus_workspace_roots.md",
    "Docs/worktree_slots.md",
    "Docs/branch_records/index.md",
    "Docs/validation_helper_registry.md",
    "Docs/development_rules.md",
    "Docs/codex_modes.md",
    "Docs/phase_governance.md",
    "Docs/governance_efficiency_operating_model.md",
    "dev/nexus_paths.py",
    "dev/orin_current_root_authority_validation.py",
)

STRICT_D_DOCS = (
    "Docs/worktree_slots.md",
    "Docs/branch_records/index.md",
    "Docs/validation_helper_registry.md",
    "Docs/development_rules.md",
    "Docs/codex_modes.md",
    "Docs/phase_governance.md",
    "Docs/governance_efficiency_operating_model.md",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def path_text(path: Path) -> str:
    return str(path).replace("/", "\\")


def live_head(repo: Path) -> str:
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def current_line_allowed(line: str) -> bool:
    lowered = line.lower()
    return any(
        marker in lowered
        for marker in (
            "historical",
            "rollback",
            "compatibility",
            "old c-drive",
            "c-drive paths",
            "fallback",
            "fixture",
            "provenance",
            "retained only",
        )
    )


def scan_owner_docs(repo: Path) -> list[str]:
    failures: list[str] = []
    for relative in STRICT_D_DOCS:
        path = repo / relative
        if not path.is_file():
            failures.append(f"missing current-root owner: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for index, line in enumerate(text.splitlines(), 1):
            if any(token in line for token in (OLD_DATA_ROOT, OLD_STATE_ROOT, OLD_WORKTREE_ROOT, OLD_USER_ROOT)):
                failures.append(f"{relative}:{index}: stale current-root token")

    main = repo / "Docs" / "Main.md"
    if not main.is_file():
        failures.append("missing current-root owner: Docs/Main.md")
    else:
        for index, line in enumerate(main.read_text(encoding="utf-8").splitlines(), 1):
            if OLD_STATE_ROOT in line or OLD_DATA_ROOT in line or OLD_WORKTREE_ROOT in line or OLD_USER_ROOT in line:
                if not current_line_allowed(line):
                    failures.append(f"Docs/Main.md:{index}: stale current-root token")
    return failures


def state_header_failures(state: Path, expected_head: str) -> list[str]:
    failures: list[str] = []
    manifest_path = state / "state_manifest.json"
    if not manifest_path.is_file():
        return ["missing mutable state_manifest.json"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"state_manifest.json invalid JSON: {exc}"]
    expected = {
        "External State Schema": "external-state-v1",
        "Root": path_text(CURRENT_STATE),
        "Worktree": "neutral-main",
        "Branch": "main",
        "Source Repo HEAD": expected_head,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            failures.append(f"state_manifest.json {key}={manifest.get(key)!r}; expected {value!r}")
    for relative in (
        "central/active_branch_authority_state.md",
        "central/selected_next_state.md",
        "branches/feature_release_readiness_source_truth_intake/branch_state.md",
        "branches/feature_release_readiness_source_truth_intake/branch_plan.md",
        "worktrees/Governance/worktree_state.md",
    ):
        path = state / relative
        if not path.is_file():
            failures.append(f"missing current external owner: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        # The boundary marker is itself a live classification field and may
        # precede additional live fields.  Stop only at the first historical
        # section heading, matching the external-state validators' live view.
        lines = text.splitlines(keepends=True)
        live_end = next(
            (index for index, line in enumerate(lines) if line.rstrip("\r\n").startswith("## ")),
            len(lines),
        )
        header = "".join(lines[:live_end])
        if path_text(CURRENT_WORKTREES / "Governance") not in header:
            failures.append(f"{relative}: current worktree root is not final D")
        if expected_head not in header:
            failures.append(f"{relative}: current source/origin head is stale")
    return failures


def parity_failures(carrier: Path, overlay: Path) -> tuple[list[str], dict[str, dict[str, str]]]:
    failures: list[str] = []
    rows: dict[str, dict[str, str]] = {}
    for relative in ADMITTED_FILES:
        carrier_path = carrier / relative
        overlay_path = overlay / relative
        if not carrier_path.is_file() or not overlay_path.is_file():
            failures.append(f"admitted parity missing: {relative}")
            continue
        carrier_hash = sha256(carrier_path)
        overlay_hash = sha256(overlay_path)
        rows[relative] = {"carrierSha256": carrier_hash, "overlaySha256": overlay_hash}
        if carrier_hash != overlay_hash:
            failures.append(f"carrier/overlay mismatch: {relative}")
    return failures, rows


def duplicate_owner_failures(records: list[dict[str, str]]) -> list[str]:
    seen: dict[str, str] = {}
    failures: list[str] = []
    for record in records:
        owner = record.get("owner", "")
        root = record.get("root", "")
        classification = record.get("classification", "")
        if classification == "current":
            if not root.startswith(path_text(CURRENT_WORKTREES)) and root not in {
                path_text(CURRENT_STATE),
                path_text(CURRENT_USER),
                path_text(CURRENT_REPO),
            }:
                failures.append(f"current root authority outside final D roots: {root}")
            if root in seen and seen[root] != owner:
                failures.append(f"duplicate current root authority: {root}")
            seen[root] = owner
        elif classification not in {"historical", "rollback", "fixture", "test-only"}:
            failures.append(f"unclassified root authority: {owner}")
    return failures


def negative_proof() -> list[dict[str, object]]:
    cases = (
        ("Main current C state", [{"owner": "Main", "root": OLD_STATE_ROOT, "classification": "current"}], True),
        ("Main old D Data state", [{"owner": "Main", "root": OLD_DATA_ROOT, "classification": "current"}], True),
        ("explicit rollback C", [{"owner": "Main", "root": path_text(ROLLBACK_REPO), "classification": "rollback"}], False),
        ("historical branch receipt", [{"owner": "branch-record", "root": OLD_WORKTREE_ROOT, "classification": "historical"}], False),
        ("slot outside final D", [{"owner": "slot", "root": OLD_DATA_ROOT + r"\Worktrees\Governance", "classification": "current"}], True),
        ("duplicate C and D current owners", [
            {"owner": "Main", "root": OLD_STATE_ROOT, "classification": "current"},
            {"owner": "state", "root": OLD_STATE_ROOT, "classification": "current"},
        ], True),
        ("unclassified owner", [{"owner": "unknown", "root": OLD_STATE_ROOT, "classification": ""}], True),
    )
    result: list[dict[str, object]] = []
    for name, records, should_block in cases:
        failures = duplicate_owner_failures(records)
        blocked = bool(failures)
        result.append({"name": name, "expected": "BLOCK" if should_block else "ALLOW", "actual": "BLOCK" if blocked else "ALLOW", "pass": blocked == should_block})
    return result


def build_report(repo: Path, state: Path, carrier: Path, overlay: Path) -> dict[str, object]:
    head = live_head(repo)
    failures = scan_owner_docs(repo)
    failures.extend(state_header_failures(state, head))
    parity, parity_rows = parity_failures(carrier, overlay)
    failures.extend(parity)
    negatives = negative_proof()
    if not all(bool(item["pass"]) for item in negatives):
        failures.append("independent negative-proof fixture failed")
    return {
        "schemaVersion": "d-root-current-authority-v1",
        "generatedAtUtc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "result": "PASS" if not failures else "BLOCK",
        "currentCanonicalRepository": path_text(repo),
        "currentGovernanceStateRoot": path_text(state),
        "currentWorktreeRoot": path_text(CURRENT_WORKTREES),
        "currentUserRoot": path_text(CURRENT_USER),
        "rollbackPredecessor": path_text(ROLLBACK_REPO),
        "sourceRepoHead": head,
        "cCurrentAuthority": False,
        "oldDDataRootCurrentAuthority": False,
        "duplicateCurrentRootAuthority": "none" if not failures else "review failures",
        "ownerDocsChecked": list(STRICT_D_DOCS) + ["Docs/Main.md"],
        "admittedParity": parity_rows,
        "negativeProof": negatives,
        "failures": failures,
        "validatorScope": "current-root owners only; historical/rollback/fixture references are not current authority",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=CURRENT_REPO)
    parser.add_argument("--state", type=Path, default=CURRENT_STATE)
    parser.add_argument("--carrier", type=Path, default=CURRENT_REPO)
    parser.add_argument("--overlay", type=Path, default=CURRENT_REPO)
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args(argv)
    report = build_report(args.repo, args.state, args.carrier, args.overlay)
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
