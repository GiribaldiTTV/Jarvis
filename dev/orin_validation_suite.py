# NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=VALIDATOR-HELPER; ledger=SRCOWN-FIRSTPASS-VALIDATOR-010; surface=validation-suite-recommendation-helper; status=shared
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ValidationCommand:
    command: str
    rationale: str


BASE_COMMANDS = (
    ValidationCommand(
        "git diff --check origin/main...HEAD",
        "checks whitespace and conflict-marker risk across the branch diff",
    ),
    ValidationCommand(
        r"python dev\orin_branch_governance_validation.py",
        "checks repo-wide governance/source-truth invariants",
    ),
)


PHASE_COMMANDS: dict[str, tuple[ValidationCommand, ...]] = {
    "governance": (
        ValidationCommand(
            r"python dev\orin_branch_governance_validation.py --standing-governance-intake-gate",
            "proves the standing Governance intake branch/worktree contract",
        ),
        ValidationCommand(
            r"python dev\orin_branch_governance_validation.py --release-readiness-health-gate",
            "proves release-readiness source-truth health is not weakened",
        ),
        ValidationCommand(
            r"python dev\orin_branch_readiness_planning_fixture_validation.py",
            "proves Branch Readiness planning-quality fixtures still catch shallow plans",
        ),
        ValidationCommand(
            r"python dev\orin_governance_efficiency_validation.py",
            "proves governance efficiency ownership, compact-pointer, and backlog/roadmap compactness rules",
        ),
    ),
    "branch-readiness": (
        ValidationCommand(
            r"python dev\orin_branch_readiness_planning_fixture_validation.py",
            "proves Branch Readiness planning-quality fixtures still catch shallow plans",
        ),
        ValidationCommand(
            r"python dev\orin_branch_governance_validation.py --worktree-confinement-gate",
            "proves assigned worktree identity when the branch record declares a worktree",
        ),
    ),
    "pr-readiness": (
        ValidationCommand(
            r"python dev\orin_branch_governance_validation.py --pr-readiness-gate",
            "checks PR Readiness-specific gate markers and live-state posture",
        ),
        ValidationCommand(
            r"python dev\orin_branch_governance_validation.py --release-readiness-health-gate",
            "proves projected merged-main source truth before PR merge readiness",
        ),
    ),
    "release-readiness": (
        ValidationCommand(
            r"python dev\orin_release_body_validation.py",
            "checks public pre-Beta release body format and prohibited internal wording",
        ),
        ValidationCommand(
            r"python dev\orin_branch_governance_validation.py --release-readiness-health-gate",
            "checks release-window source-truth health markers",
        ),
    ),
    "runtime-fam006": (
        ValidationCommand(
            r"python dev\orin_monitoring_hud_surface_validation.py",
            "checks FAM-006 Monitoring HUD / Dashboard surface source-truth markers",
        ),
        ValidationCommand(
            r"python dev\orin_monitoring_hud_internal_sandbox_validation.py",
            "checks FAM-006 Monitoring HUD internal sandbox proof",
        ),
    ),
    "runtime-fam007": (
        ValidationCommand(
            r"python dev\orin_ai_provider_state_validation.py",
            "checks FAM-007 local AI provider/readiness state contracts",
        ),
    ),
}


ALWAYS_USEFUL_COMMANDS = (
    ValidationCommand(
        r"python dev\orin_release_body_validation.py",
        "keeps public release-note governance from drifting during source-truth work",
    ),
    ValidationCommand(
        r"python dev\orin_ai_provider_state_validation.py",
        "keeps FAM-007 provider-state contracts green when shared docs move",
    ),
    ValidationCommand(
        r"python -m compileall -q dev desktop Audio main.py",
        "checks Python syntax for validator/helper/runtime surfaces",
    ),
)


def _run_git_diff_names() -> tuple[str, ...]:
    commands = (
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    names: list[str] = []
    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        names.extend(
            line.strip().replace("/", "\\")
            for line in result.stdout.splitlines()
            if line.strip()
        )
    return tuple(dict.fromkeys(names))


def _dedupe(commands: list[ValidationCommand]) -> list[ValidationCommand]:
    seen: set[str] = set()
    result: list[ValidationCommand] = []
    for command in commands:
        if command.command in seen:
            continue
        seen.add(command.command)
        result.append(command)
    return result


def _surface_commands(changed_files: tuple[str, ...]) -> tuple[ValidationCommand, ...]:
    normalized = "\n".join(path.replace("/", "\\").casefold() for path in changed_files)
    commands: list[ValidationCommand] = []
    if "desktop\\desktop_renderer.py" in normalized or "monitoring" in normalized or "fam_006" in normalized:
        commands.extend(PHASE_COMMANDS["runtime-fam006"])
    if "ai_provider" in normalized or "fam_007" in normalized or "local_ai" in normalized:
        commands.extend(PHASE_COMMANDS["runtime-fam007"])
    if "docs\\branch_records" in normalized or "docs\\feature_backlog.md" in normalized or "docs\\prebeta_roadmap.md" in normalized:
        commands.append(
            ValidationCommand(
                r"python dev\orin_branch_governance_validation.py --release-readiness-health-gate",
                "shared source-truth files changed, so release-readiness health must be rechecked",
            )
        )
    if "source_owner_marker" in normalized or "source-owner" in normalized:
        commands.append(
            ValidationCommand(
                r"python dev\orin_source_owner_marker_validation.py",
                "checks source-owner marker syntax, ledger linkage, shared-surface coverage, and Compact-AI preservation/fold-down posture",
            )
        )
    return tuple(commands)


def build_suite(phase: str, changed_files: tuple[str, ...]) -> list[ValidationCommand]:
    commands = [*BASE_COMMANDS]
    commands.extend(PHASE_COMMANDS.get(phase, ()))
    commands.extend(_surface_commands(changed_files))
    commands.extend(ALWAYS_USEFUL_COMMANDS)
    return _dedupe(commands)


def render_text(phase: str, changed_files: tuple[str, ...], commands: list[ValidationCommand]) -> str:
    changed = ", ".join(changed_files) if changed_files else "None detected"
    lines = [
        "Recommended Validation Suite:",
        f"- Phase: `{phase}`",
        f"- Changed Files: `{changed}`",
        "- Mutation Policy: `report-only - helper recommends commands but does not execute them`",
        "- Commands:",
    ]
    for command in commands:
        lines.append(f"  - `{command.command}` - {command.rationale}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report-only validation suite recommendation helper for Nexus governance phases."
    )
    parser.add_argument(
        "--phase",
        default="governance",
        choices=(
            "governance",
            "branch-readiness",
            "pr-readiness",
            "release-readiness",
            "runtime-fam006",
            "runtime-fam007",
        ),
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=None,
        help="Changed file path. Omit to inspect git diff --name-only origin/main...HEAD.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    changed_files = tuple(args.changed_file or _run_git_diff_names())
    commands = build_suite(args.phase, changed_files)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "title": "Recommended Validation Suite",
                    "phase": args.phase,
                    "changed_files": changed_files,
                    "mutation_policy": "report-only - helper recommends commands but does not execute them",
                    "commands": [
                        {"command": command.command, "rationale": command.rationale}
                        for command in commands
                    ],
                },
                indent=2,
            )
        )
    else:
        print(render_text(args.phase, changed_files, commands))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
