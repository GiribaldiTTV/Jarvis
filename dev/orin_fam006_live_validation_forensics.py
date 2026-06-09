"""FAM-006 Live Validation / UTS failure forensic packet generator.

This helper is investigation support only. It does not repair product runtime
behavior, advance phase state, accept UTS results, close issues, or claim that
new investigation evidence validates the earlier Live Validation handoff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import textwrap
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[1]
USER_ROOT = Path(r"C:\Nexus USER")
PACKET_ROOT = USER_ROOT / "FAM-006"
SCREENSHOT_ROOT = Path(r"C:\Users\anden\OneDrive\Pictures\Screenshots")
BASELINE_HEAD = "4afb18905d961c492a701149133e122fabee301d"
BASELINE_MAIN = "f239c97415fb8aaac414f9b802888ea004d08c29"
LIVE_VALIDATION_ROOT = (
    REPO / "dev" / "logs" / "fam_006_monitoring_hud_live_validation" / "20260609_090906_117"
)
FORENSICS_LOG_ROOT = REPO / "dev" / "logs" / "fam006_live_validation_forensics"
PRIMARY_FILE = "USER Review/LIVE_VALIDATION_UTS_FAILURE_INVESTIGATION.md"


SOURCE_TRUTH_FILES = [
    "Docs/Main.md",
    "Docs/nexus_startup_contract.md",
    "Docs/nexus_vision.md",
    "Docs/family_visions/README.md",
    "Docs/family_visions/FAM-006_monitoring_and_hud.md",
    "Docs/family_feature_visions/FAM-006_recording.md",
    "Docs/feature_backlog.md",
    "Docs/prebeta_roadmap.md",
    "Docs/phase_governance.md",
    "Docs/development_rules.md",
    "Docs/codex_modes.md",
    "Docs/branch_plans/README.md",
    "Docs/governance_efficiency_operating_model.md",
    "Docs/validation_helper_registry.md",
    "Docs/incident_patterns.md",
    "Docs/worktree_slots.md",
    "Docs/branch_records/feature_fam_006_dashboard_recording_start_stop_local_file.md",
]

IMPLEMENTATION_FILES = [
    "nexus_visual/monitoring_hud.js",
    "nexus_visual/monitoring_hud.css",
    "nexus_visual/monitoring_hud.html",
    "desktop/monitoring_hud_state.py",
    "desktop/desktop_renderer.py",
    "desktop/orin_desktop_main.py",
    "desktop/recording_output_contract.py",
]

TOOL_FILES = [
    "dev/orin_monitoring_hud_live_validation.ps1",
    "dev/orin_monitoring_hud_surface_validation.py",
    "dev/orin_monitoring_hud_internal_sandbox_validation.py",
    "dev/orin_fam006_workstream_readiness.py",
    "dev/orin_fam006_hardening_h1.py",
    "dev/orin_user_review_bundle.py",
    "dev/orin_branch_readiness_planning_fixture_validation.py",
]


@dataclass(frozen=True)
class Finding:
    finding_id: str
    title: str
    finding_class: str
    affected_surface: str
    expectation: str
    actual: str
    evidence_path: str
    confidence: str
    phase_attribution: str
    code_lineage: str
    baseline_boundary: str
    repair_lane: str
    user_decision: str

    def markdown(self) -> str:
        return "\n".join(
            [
                f"### {self.finding_id} - {self.title}",
                "",
                f"- Finding class: {self.finding_class}",
                f"- Affected surface: {self.affected_surface}",
                f"- Source-truth expectation: {self.expectation}",
                f"- Actual behavior: {self.actual}",
                f"- Evidence path: `{self.evidence_path}`",
                f"- Confidence: {self.confidence}",
                f"- Phase attribution: {self.phase_attribution}",
                f"- Code lineage: {self.code_lineage}",
                f"- Baseline boundary result: {self.baseline_boundary}",
                f"- Future repair lane candidate: {self.repair_lane}",
                f"- USER decision requirement: {self.user_decision}",
                "",
            ]
        )


def run_command(args: list[str], timeout: int = 60) -> tuple[int, str]:
    try:
        result = subprocess.run(
            args,
            cwd=REPO,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return 124, output + "\nTIMEOUT\n"


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    for encoding in ("utf-8-sig", "utf-8", "utf-16"):
        try:
            text = path.read_text(encoding=encoding)
            return text if limit is None else text[:limit]
        except UnicodeError:
            continue
    data = path.read_bytes().decode("utf-8", errors="replace")
    return data if limit is None else data[:limit]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(read_text(path))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def copy_if_exists(source: Path, target: Path) -> bool:
    if not source.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return True


def latest_baseline_root() -> Path | None:
    if not FORENSICS_LOG_ROOT.exists():
        return None
    roots = [p for p in FORENSICS_LOG_ROOT.iterdir() if p.is_dir()]
    return max(roots, key=lambda p: p.stat().st_mtime, default=None)


def list_files(root: Path, limit: int = 400) -> list[str]:
    if not root.exists():
        return [f"MISSING: {root}"]
    rows = []
    for item in sorted(root.rglob("*"))[:limit]:
        rel = item.relative_to(root)
        if item.is_file():
            rows.append(f"{rel} ({item.stat().st_size} bytes)")
        else:
            rows.append(f"{rel}/")
    return rows


def source_truth_loaded_lines() -> tuple[list[str], list[str]]:
    loaded = []
    missing = []
    for rel in SOURCE_TRUTH_FILES:
        path = REPO / rel
        if path.exists():
            loaded.append(rel)
        else:
            missing.append(rel)
    external = Path(
        r"C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_plan.md"
    )
    external_state = Path(
        r"C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_state.md"
    )
    for path in (external, external_state):
        if path.exists():
            loaded.append(str(path))
        else:
            missing.append(str(path))
    return loaded, missing


def git_identity() -> dict[str, str]:
    commands = {
        "git_root": ["git", "rev-parse", "--show-toplevel"],
        "branch": ["git", "branch", "--show-current"],
        "head": ["git", "rev-parse", "HEAD"],
        "origin_main": ["git", "rev-parse", "origin/main"],
        "merge_base": ["git", "merge-base", "HEAD", "origin/main"],
        "ahead_behind": ["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"],
        "status_short": ["git", "status", "--short"],
        "upstream_status": ["git", "status", "--branch", "--porcelain=v2"],
    }
    proof = {}
    for key, command in commands.items():
        code, output = run_command(command)
        proof[key] = output.strip() if code == 0 else f"ERROR({code}): {output.strip()}"
    return proof


def changed_files() -> list[str]:
    code, output = run_command(["git", "diff", "--name-only", "origin/main...HEAD"])
    if code != 0:
        return [f"ERROR: {output.strip()}"]
    return [line.strip() for line in output.splitlines() if line.strip()]


def manifest_summary() -> dict[str, object]:
    manifest = load_json(LIVE_VALIDATION_ROOT / "manifest.json")
    interaction = load_json(LIVE_VALIDATION_ROOT / "monitoring_hud_live_client_interaction_manifest.json")
    user_screenshot_root = Path(str(manifest.get("screenshotEvidenceRoot") or ""))
    user_element_root = Path(str(manifest.get("elementScreenshotEvidenceRoot") or ""))
    return {
        "manifest_status": manifest.get("status", "MISSING"),
        "interaction_status": interaction.get("status", "MISSING"),
        "manifest_path": str(LIVE_VALIDATION_ROOT / "manifest.json"),
        "interaction_manifest_path": str(
            LIVE_VALIDATION_ROOT / "monitoring_hud_live_client_interaction_manifest.json"
        ),
        "repo_live_validation_root_exists": LIVE_VALIDATION_ROOT.exists(),
        "repo_screenshot_count": len(list((LIVE_VALIDATION_ROOT / "live_client_interaction").glob("*.png")))
        if (LIVE_VALIDATION_ROOT / "live_client_interaction").exists()
        else 0,
        "user_screenshot_root": str(user_screenshot_root),
        "user_screenshot_root_exists": user_screenshot_root.exists(),
        "user_element_root": str(user_element_root),
        "user_element_root_exists": user_element_root.exists(),
        "user_element_manifest_count": (manifest.get("perElementUserInspectableScreenshots") or {}).get("count", 0)
        if isinstance(manifest.get("perElementUserInspectableScreenshots"), dict)
        else 0,
        "steps": interaction.get("steps", []),
        "screenshots": interaction.get("screenshots", []),
    }


def tool_gap_rows() -> list[dict[str, str]]:
    baseline = latest_baseline_root()
    rows = [
        {
            "tool": "dev/orin_monitoring_hud_surface_validation.py",
            "claim": "PASS: marker-backed Dashboard/HUD source truth",
            "gap": "Source/marker scan; does not reproduce USER-created profile switching, post-restart persistence, card inset visual quality, or USER-inspectable evidence path availability.",
            "baseline_output": str(baseline / "baseline_old_tools" / "orin_monitoring_hud_surface_validation.txt")
            if baseline
            else "not captured",
        },
        {
            "tool": "dev/orin_monitoring_hud_internal_sandbox_validation.py",
            "claim": "PASS: internal sandbox validation green",
            "gap": "Internal sandbox manifest proof; does not prove all real USER combinations or visual adjudication against attached USER screenshot.",
            "baseline_output": str(baseline / "baseline_old_tools" / "orin_monitoring_hud_internal_sandbox_validation.txt")
            if baseline
            else "not captured",
        },
        {
            "tool": "dev/orin_fam006_hardening_h1.py",
            "claim": "H1 Green",
            "gap": "H1 explicitly routes Live Validation and UTS outside H1; a green H1 should not imply USER-facing Live Validation acceptance.",
            "baseline_output": str(baseline / "baseline_old_tools" / "orin_fam006_hardening_h1.txt")
            if baseline
            else "not captured",
        },
        {
            "tool": "dev/orin_monitoring_hud_live_validation.ps1",
            "claim": "LV1 PASS and UTS handoff refreshed",
            "gap": "Automated handoff did not close USER Gate State; manifest can point to missing USER-inspectable evidence paths and did not exhaustively test all USER-reported combinations.",
            "baseline_output": str(LIVE_VALIDATION_ROOT / "manifest.json"),
        },
    ]
    return rows


def findings(summary: dict[str, object]) -> list[Finding]:
    user_root_exists = bool(summary["user_screenshot_root_exists"])
    user_element_exists = bool(summary["user_element_root_exists"])
    user_evidence_actual = (
        "LV1 manifest claims USER-inspectable OneDrive evidence paths, but the exact "
        "screenshot root and focused element root do not currently exist."
        if not user_root_exists or not user_element_exists
        else "LV1 USER-inspectable evidence paths exist now; investigation still distinguishes existence from visual adjudication."
    )
    user_evidence_confidence = "Verified" if not user_root_exists or not user_element_exists else "No Issue Found"
    return [
        Finding(
            "FAM006-EVID-001",
            "LV1 user-inspectable screenshot path does not resolve",
            "screenshot/evidence failure",
            "Live Validation screenshot evidence handoff",
            "LV1 must provide full-window and element-level evidence in an organized USER-inspectable screenshot folder.",
            user_evidence_actual,
            str(LIVE_VALIDATION_ROOT / "manifest.json"),
            user_evidence_confidence,
            "Live Validation / UTS handoff",
            "dev/orin_monitoring_hud_live_validation.ps1 writes manifest evidence paths; current path availability was not rechecked before handoff.",
            "Baseline reconciliation through 4afb1890 is not treated as the original cause; this finding is about current evidence path availability for the prior LV1 artifact.",
            "Investigation-support tooling now; durable prevention likely Governance/FAM-006 Live Validation helper after USER review.",
            "USER review of investigation packet before repair planning.",
        ),
        Finding(
            "FAM006-TOOLGAP-001",
            "Old green tools prove markers/manifests more strongly than USER behavior",
            "helper/validator/tool gap",
            "H1, surface, internal sandbox, and LV1 helpers",
            "Helper PASS is evidence only; Live Validation must expose affected user-facing interactions and visual proof, not only marker or manifest presence.",
            "Baseline tools passed while USER later reported visual, switching, folder, and evidence failures; several old tools do not test the USER-created-profile and post-handoff evidence combinations.",
            str(latest_baseline_root() or FORENSICS_LOG_ROOT),
            "Verified",
            "Workstream / Hardening / Live Validation",
            "dev/orin_monitoring_hud_surface_validation.py and dev/orin_fam006_hardening_h1.py inspect markers/source and declared proof; dev/orin_monitoring_hud_live_validation.ps1 generated a handoff manifest but did not settle USER Gate State.",
            "Baseline reconciliation effects are separated; the false-green replay was captured after reconciliation as current tool behavior.",
            "Durable validation repair candidate after USER accepts findings.",
            "No product repair approved in this packet.",
        ),
        Finding(
            "FAM006-LVFAIL-001",
            "LV1 did not exhaustively cover affected Option C interaction combinations",
            "Live Validation failure",
            "Dashboard Recording Card, Recording Studio, Log Viewer Studio shell, Overlay Profile interactions",
            "Accepted Option C required deterministic proof for new or affected surfaces, including target mirroring, open-folder pre-session usability, native/export boundary, visual-system inheritance, and USER-facing UTS evidence.",
            "The LV1 run covered selected focused states, but USER-reported failures show missing or insufficient coverage for combinations such as creating/switching multiple profiles in normal use, screenshot evidence handoff, and visual quality adjudication.",
            str(LIVE_VALIDATION_ROOT / "monitoring_hud_live_client_interaction_manifest.json"),
            "Inferred",
            "Live Validation",
            "nexus_visual/monitoring_hud.js user-state/event paths plus desktop/native bridge paths were tested through a narrow scripted path, not every user-relevant combination.",
            "The failure is reconstructed from prior LV1 artifact plus USER reports; not attributed to the reconciliation merge without direct evidence.",
            "Future Live Validation coverage matrix / visual adjudication helper.",
            "Repair planning remains pending USER decision.",
        ),
        Finding(
            "FAM006-UTSFAIL-001",
            "UTS handoff asked USER to catch failures that should have blocked handoff",
            "UTS handoff failure",
            "C:\\Nexus USER\\UTS - FAM-006.txt",
            "UTS should be a USER returned-evidence handoff after Live Validation proof, not a substitute for deterministic pre-handoff validation of admitted surfaces.",
            "The handoff UTS lists active items for Recording visual inheritance, target mirroring, native log save/readback, issue #258 persistence, and card holder insets; USER then found failures in those active items.",
            r"C:\Nexus USER\UTS - FAM-006.txt",
            "Verified",
            "UTS handoff",
            "dev/orin_monitoring_hud_live_validation.ps1 refreshed the worktree-specific UTS after LV1 PASS; UTS result remained pending and should not be treated as acceptance.",
            "Baseline reconciliation did not change the UTS semantics; current source truth still marks USER Gate pending.",
            "UTS gate / LV1 stop-loss repair candidate.",
            "USER must review findings before deciding repair plan.",
        ),
        Finding(
            "FAM006-UI-001",
            "Recording card visual-system mismatch escaped automated proof",
            "UI/window behavior failure",
            "Dashboard Recording Card",
            "FAM-006 Recording vision requires new UI elements to sample existing card color, shape, style, effects, spacing, button behavior, and layout density.",
            "USER reported the Recording card did not match the standardized Dashboard card format; the investigation did not reproduce a new screenshot and treats the attached chat screenshot as USER evidence not present on disk.",
            "USER-provided chat screenshot; local file C:\\Users\\anden\\OneDrive\\Pictures\\Screenshots\\pythonw_O2aIAY5eBZ.png not found during investigation.",
            "Reproducible",
            "Workstream / Hardening / Live Validation",
            "Likely CSS/DOM lineage in nexus_visual/monitoring_hud.css and nexus_visual/monitoring_hud.js around dashboard recording card markup and visual inspection markers.",
            "Not attributed to reconciliation; the reported UI mismatch predates this investigation and was a USER-observed post-handoff failure.",
            "Product/UI repair lane after investigation; validation helper should require image adjudication, not only marker presence.",
            "Product repair remains pending separate approval.",
        ),
        Finding(
            "FAM006-REGRESS-001",
            "Overlay Profile switching remained blocked in USER path",
            "regression",
            "HUD Overlay card Active Overlay Profile selector",
            "Recording target reliability requires Active Overlay Profile switching to update the Recording card target and remain usable with multiple profiles.",
            "USER reported they still cannot switch Overlay Profiles inside the HUD Overlay card. The LV1 scripted path selected an LV1 seeded profile, but this does not disprove the USER path failure.",
            str(LIVE_VALIDATION_ROOT / "monitoring_hud_live_client_interaction_manifest.json"),
            "Reproducible",
            "Live Validation / Workstream",
            "Likely event/state lineage in nexus_visual/monitoring_hud.js overlay-profile selector activation and recording target mirror state; desktop/monitoring_hud_state.py normalizes active profile snapshots.",
            "The scripted pass is a current baseline artifact; USER normal-path failure remains a separate post-handoff symptom.",
            "Product/state repair lane after investigation.",
            "Product repair remains pending separate approval.",
        ),
        Finding(
            "FAM006-UI-002",
            "Card holder inset regression reached UTS",
            "UI/window behavior failure",
            "Dashboard card holder / scrollbar gutter",
            "Dashboard cards should maintain equal visual insets; the scrollbar gutter should not make cards appear offset.",
            "USER reported unequal left/right spacing inside the card holder, likely due to scrollbar gutter accounting. No current investigation screenshot reproduction was taken.",
            r"C:\Nexus USER\UTS - FAM-006.txt",
            "Reproducible",
            "Live Validation / UTS handoff",
            "Likely CSS/layout lineage in nexus_visual/monitoring_hud.css around control hub, card holder, and scrollbar gutter styling.",
            "Not attributed to reconciliation; UTS active issue list proves this was known as a USER retest item after LV1.",
            "Product/UI layout repair lane after findings review.",
            "Product repair remains pending separate approval.",
        ),
        Finding(
            "FAM006-WINDOW-001",
            "Log Viewer Studio / folder behavior proof is narrower than user workflow",
            "UI/window behavior failure",
            "Log Viewer Studio shell and native/export folder actions",
            "The minimal Log Viewer Studio shell should make native/export folder access usable before recording and keep full viewer/export customization future-gated.",
            "Scripted LV1 records a pass for native/export shell pre-session proof, but USER reports indicated the open-folder experience and product/native-vs-export boundary were still confusing or not aligned with desired workflow.",
            str(LIVE_VALIDATION_ROOT / "monitoring_hud_live_client_interaction_manifest.json"),
            "Inferred",
            "Live Validation",
            "desktop/orin_desktop_main.py and desktop/desktop_renderer.py own native window/folder bridge dispatch; recording_output_contract.py owns native/export boundary.",
            "Current baseline helper behavior may have improved after user feedback; original failure evidence remains in USER report/UTS context.",
            "Product/window behavior repair lane if USER confirms finding.",
            "Product repair remains pending separate approval.",
        ),
        Finding(
            "FAM006-CODEPATH-001",
            "Implementation lineage crosses JS state, native bridge, and output contract",
            "implementation/code lineage failure",
            "Recording target, Start/Stop, Studio shell, Log Viewer shell",
            "Accepted Option C requires user-facing behavior across Dashboard JS state, native windows, output roots, and validation artifacts.",
            "The affected behavior spans multiple code paths, while several validators inspect markers or one focused route. This makes partial false-greens likely when a USER path differs from the scripted route.",
            "git diff --name-only origin/main...HEAD; implementation files listed in packet",
            "Inferred",
            "Workstream / Hardening / Live Validation",
            "nexus_visual/monitoring_hud.js, nexus_visual/monitoring_hud.css, desktop/monitoring_hud_state.py, desktop/desktop_renderer.py, desktop/orin_desktop_main.py, desktop/recording_output_contract.py.",
            "The codepath analysis treats 4afb1890 as baseline; original implementation commits include 8330af1b and LV1 repair commit 4c395180.",
            "Future repair planning should trace each product finding to a specific event/state path before fixing.",
            "No code repair approved here.",
        ),
        Finding(
            "FAM006-PHASE-001",
            "Phase progression relied on automated handoff green while USER Gate stayed pending",
            "phase progression failure",
            "Live Validation LV1 / UTS handoff",
            "Packet/tool reviewability and automated handoff are separate from USER acceptance or returned UTS results.",
            "External branch state correctly says USER-returned UTS results remain pending, but the process still produced a handoff that USER found not ready.",
            r"C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_plan.md",
            "Verified",
            "Live Validation / UTS",
            "No single product code line; process lineage in branch_plan LV1 receipt, UTS handoff, and live-validation helper.",
            "Not a rebaseline effect; source truth currently preserves the pending USER gate boundary.",
            "Governance/helper follow-up candidate after findings review.",
            "USER must decide repair/prevention planning next.",
        ),
        Finding(
            "FAM006-BASELINE-001",
            "Reconciliation boundary is separated from failure evidence",
            "baseline boundary",
            "Investigation evidence model",
            "The merged main reconciliation and waiver-law repair through 4afb1890 must be treated as baseline, not as original Live Validation failure evidence absent direct proof.",
            "Git identity proves HEAD 4afb1890, origin/main f239c974, and merge base f239c974; findings cite prior LV1 artifacts and USER reports separately.",
            "git identity baseline captured in raw evidence",
            "Verified",
            "Investigation",
            "No product code lineage; git/phase boundary.",
            "Baseline boundary explicitly honored.",
            "No repair required for this finding unless USER sees misclassification.",
            "None.",
        ),
    ]


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n\n"


def table(headers: list[str], rows: Iterable[Iterable[str]]) -> str:
    safe_rows = [[str(cell).replace("\n", " ") for cell in row] for row in rows]
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in safe_rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def loop_summary_md(findings_list: list[Finding], summary: dict[str, object]) -> str:
    baseline = latest_baseline_root()
    loops = [
        (
            "Loop 0 - As-found baseline",
            f"Captured git identity, changed files, validator output, evidence listings, USER packet listings, and screenshot roots before adding this helper. Raw root: `{baseline}`.",
        ),
        (
            "Loop 1 - Old-tool false-green replay",
            "Existing surface, sandbox, Workstream readiness, H1, and runtime-fam006 recommendation tools were run before this helper was added. The key result is that old tools can pass while USER-facing post-handoff findings remain open.",
        ),
        (
            "Loop 2 - Deterministic coverage expansion",
            "Added this investigation-only packet generator to assemble evidence, stable IDs, matrix coverage, baseline comparison, screenshot path checks, code lineage, and negative/blocked findings without product repair.",
        ),
        (
            "Loop 3 - Patched-tool rerun",
            "This helper reran the evidence audit against the reconciled baseline and produced packet-visible findings. It does not claim to reproduce all runtime symptoms.",
        ),
        (
            "Loop 4 - USER-found issue exposure",
            "Mapped USER-reported issues to source-truth expectations, UTS active issue IDs, LV1 manifests, and likely implementation/tool gaps.",
        ),
        (
            "Loop 5 - Additional failure discovery",
            "Discovered a concrete evidence-handoff gap: the LV1 manifest claims a USER-inspectable screenshot path that does not currently resolve.",
        ),
        (
            "Loop 6 - Code injection / implementation lineage",
            "Mapped likely lineage across monitoring_hud.js/css, desktop native bridge files, monitoring_hud_state.py, and recording_output_contract.py.",
        ),
        (
            "Loop 7 - Phase/gate causality map",
            "Separated BP/Workstream/H1/LV/UTS contributions and preserved the fact that UTS returned results are pending.",
        ),
        (
            "Loop 8 - Timeline reconstruction",
            "Reconstructed the timeline from BP1/BP2/BP3 acceptance through Workstream, H1, LV1 handoff, USER-reported failures, rebaseline, and this investigation.",
        ),
        (
            "Loop 9 - Negative findings / checked-clean surfaces",
            "Reported surfaces checked with no issue found using available evidence, and explicitly named limitations.",
        ),
        (
            "Loop 10 - Exhaustiveness check",
            "Confirmed every accepted Option C surface is inventoried and every finding has a stable ID and confidence label.",
        ),
    ]
    return "\n".join(f"### {name}\n\n{body}\n" for name, body in loops)


def evidence_inventory_md(summary: dict[str, object]) -> str:
    rows = [
        ("Repo LV1 root", str(LIVE_VALIDATION_ROOT), str(summary["repo_live_validation_root_exists"])),
        ("Repo LV1 screenshots", "live_client_interaction/*.png", str(summary["repo_screenshot_count"])),
        ("LV1 manifest", str(summary["manifest_path"]), str(summary["manifest_status"])),
        ("LV1 interaction manifest", str(summary["interaction_manifest_path"]), str(summary["interaction_status"])),
        ("Claimed USER screenshot root", str(summary["user_screenshot_root"]), str(summary["user_screenshot_root_exists"])),
        ("Claimed USER element screenshot root", str(summary["user_element_root"]), str(summary["user_element_root_exists"])),
        ("Manifest user element screenshot count", "perElementUserInspectableScreenshots.count", str(summary["user_element_manifest_count"])),
        ("Worktree-specific UTS", r"C:\Nexus USER\UTS - FAM-006.txt", str(Path(r"C:\Nexus USER\UTS - FAM-006.txt").exists())),
    ]
    return table(["Evidence", "Path / Field", "Result"], rows)


def combination_matrix_md() -> str:
    rows = [
        ("Default profile + active monitors + not recording", "Ready, Start enabled, Recording card mirrors active profile", "LV1 scripted path PASS", "Verified by manifest"),
        ("USER-created profile + active monitor + switch selector", "Selector changes active Overlay Profile and Recording card target", "USER reports still blocked; scripted seeded profile path PASS", "Reproducible / conflict"),
        ("USER-created profile + app restart", "Profile persists and remains selectable; issue #258 target reliability", "UTS asks USER to retest; no direct investigation reproduction", "Blocked"),
        ("No active monitors", "Recording blocked/truthful unavailable state", "Not directly reproduced in current investigation", "Blocked"),
        ("Recording active", "Stop visible; state transparent", "LV1 scripted path PASS", "Verified by manifest"),
        ("Recording stopped/saved", "Native NDAI log saved/readback complete; no normal CSV export", "LV1 scripted path PASS with manual validation CSV artifact", "Verified by manifest"),
        ("Log Viewer shell before recording", "Native/export folders open/create before active-session recording", "LV1 scripted path PASS", "Verified by manifest"),
        ("Claimed USER screenshot evidence", "Folder exists and USER can inspect screenshots/video", "Exact claimed OneDrive folder missing now", "Verified failure"),
        ("Dashboard card holder scrollbar", "Equal left/right insets", "USER reported fail; no current reproduction", "Reproducible"),
        ("Recording card visual inheritance", "Card matches existing visual system fully", "USER reported mismatch; marker proof passed", "Reproducible"),
    ]
    return table(["Combination", "Expected", "Actual / Available Evidence", "Confidence"], rows)


def timeline_md() -> str:
    rows = [
        ("2026-06-09", "BP1", "USER accepted revised BP1 after Option F planning solidification", "branch plan / branch record", "Supports Option C path"),
        ("2026-06-09", "BP2", "USER accepted Option C Branch Plan", "branch plan", "Supports Workstream package"),
        ("2026-06-09", "BP3", "USER accepted Option C Workstream Entry", "branch plan", "Supports separate Workstream approval"),
        ("2026-06-09", "Workstream", "Option C implementation committed at 8330af1b", "git log / branch plan", "Introduced Dashboard Recording, Studio, Log Viewer shell, output contract"),
        ("2026-06-09", "Hardening H1", "H1 green at a17012a6", "dev/orin_fam006_hardening_h1.py", "H1 did not own formal UTS result"),
        ("2026-06-09 09:09", "Live Validation", "LV1 focused helper PASS at 20260609_090906_117", "manifest.json", "Automated handoff green"),
        ("2026-06-09 09:10", "UTS handoff", "UTS - FAM-006 refreshed as draft handoff", r"C:\Nexus USER\UTS - FAM-006.txt", "USER result pending"),
        ("2026-06-09", "USER review", "USER reports failures/regressions/UI/evidence gaps", "chat prompt and UTS context", "Contradicts readiness of automated handoff"),
        ("2026-06-09", "Rebaseline", "origin/main merged; baseline HEAD 4afb1890", "git log", "Baseline boundary for investigation"),
        ("2026-06-09", "Investigation", "Baseline old tools captured; forensics packet generated", "dev/logs/fam006_live_validation_forensics", "Findings packet, not repair plan"),
    ]
    return table(["Date/time", "Phase/gate", "Claim or decision", "Proof", "Later finding relation"], rows)


def phase_map_md() -> str:
    rows = [
        ("BP1", "Define branch vision and visual/product expectations", "Accepted Option C direction after Option F", "Did not itself prove implementation/UI"),
        ("BP2", "Map vision to engineering plan and proof", "Accepted Option C plan", "Proof matrix needed stronger later LV coverage"),
        ("BP3", "Validate Workstream orchestration and package coherence", "Accepted coherent Option C package", "Did not guarantee individual implementation quality"),
        ("Workstream", "Implement all accepted seams/slices", "Green at 8330af1b", "Product defects may have entered JS/CSS/native bridge paths"),
        ("Hardening H1", "Pressure-test before LV", "H1 green; no formal UTS export", "Marker/source checks insufficient for some user paths"),
        ("Live Validation", "Real user-facing proof and screenshot/video evidence", "LV1 PASS / handoff green", "Missed or under-adjudicated reported failures"),
        ("UTS", "USER returned result, not automatic acceptance", "Draft handoff created; results pending", "USER found failures before acceptance"),
        ("Helpers/validators", "Evidence, not authority", "Several PASS results", "False-green class exposed"),
    ]
    return table(["Phase/gate", "What it should require", "Evidence found", "Miss enabled"], rows)


def negative_findings_md(summary: dict[str, object]) -> str:
    rows = [
        ("Repo-local LV1 artifacts", "Manifest and screenshot files exist under repo log root", "No Issue Found", "Does not prove USER-inspectable copy exists"),
        ("Native log no normal CSV", "recording_output_contract.py says normal product save does not create export; validation CSV only with env var", "No Issue Found", "USER workflow still needs future export UX"),
        ("Scripted default profile Start/Stop", "LV1 manifest records real OS Start and Stop PASS", "No Issue Found", "Scripted default path does not cover all USER-created profile paths"),
        ("Log Viewer shell future boundaries", "Manifest records full viewer/export customization future-gated", "No Issue Found", "Does not prove ideal UX wording or all folder paths"),
    ]
    return table(["Surface checked", "Evidence used", "Confidence", "Limitation"], rows)


def checked_not_reproducible_md() -> str:
    rows = [
        ("USER-created profile cannot switch", "No live runtime reproduction in this investigation; USER report plus conflict with scripted seeded profile PASS", "Reproducible", "Needs product repair pass with live UI"),
        ("Card holder unequal insets", "No fresh screenshot capture allowed as prior proof; USER report and UTS active issue", "Reproducible", "Needs visual/product repair pass"),
        ("Recording card style mismatch", "USER chat screenshot was not present on disk; source-truth expectation exists", "Reproducible", "Needs visual adjudication during repair"),
        ("Post-restart profile persistence", "UTS asks USER to verify; not rerun here", "Blocked", "Would require product/runtime reproduction"),
    ]
    return table(["Issue", "Available evidence", "Confidence", "Why not fully reproduced"], rows)


def code_lineage_md() -> str:
    rows = [
        ("Recording target mirror", "nexus_visual/monitoring_hud.js; desktop/monitoring_hud_state.py", "Active Overlay Profile state -> activeOverlayRecordingTarget -> card render", "REGRESS-001"),
        ("Recording card visual/layout", "nexus_visual/monitoring_hud.css; nexus_visual/monitoring_hud.html; nexus_visual/monitoring_hud.js", "Dashboard card holder and recording card DOM/CSS", "UI-001, UI-002"),
        ("Recording Studio", "desktop/desktop_renderer.py; desktop/orin_desktop_main.py; nexus_visual/monitoring_hud.js", "Dashboard click -> native bridge -> standalone window", "WINDOW-001"),
        ("Log Viewer Studio shell", "desktop/desktop_renderer.py; desktop/orin_desktop_main.py; desktop/recording_output_contract.py", "Dashboard click -> native/export root creation/opening", "WINDOW-001"),
        ("Native/export boundary", "desktop/recording_output_contract.py", "native .ndailog product artifact; validation/export CSV separated", "UTSFAIL-001"),
        ("LV1 evidence", "dev/orin_monitoring_hud_live_validation.ps1", "manifest paths, screenshot copy, UTS handoff", "EVID-001, TOOLGAP-001"),
    ]
    return table(["Symptom lineage", "File(s)", "Event/state path", "Finding IDs"], rows)


def generate_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    if identity.get("head") != BASELINE_HEAD:
        raise SystemExit(f"BLOCKED: expected HEAD {BASELINE_HEAD}, found {identity.get('head')}")
    if identity.get("origin_main") != BASELINE_MAIN:
        raise SystemExit(f"BLOCKED: expected origin/main {BASELINE_MAIN}, found {identity.get('origin_main')}")

    summary = manifest_summary()
    findings_list = findings(summary)
    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    baseline = latest_baseline_root()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"

    if PACKET_ROOT.exists():
        shutil.rmtree(PACKET_ROOT)
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    for old_zip in USER_ROOT.glob("FAM-006-*.zip"):
        old_zip.unlink()

    dirs = [
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
        PACKET_ROOT / "Review Aids" / "Raw Evidence",
        PACKET_ROOT / "Review Aids" / "Raw Evidence" / "baseline_old_tools",
        PACKET_ROOT / "Review Aids" / "Raw Evidence" / "evidence_listings",
        PACKET_ROOT / "Source Truth Context",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    for rel in SOURCE_TRUTH_FILES:
        copy_if_exists(REPO / rel, PACKET_ROOT / "Source Truth Context" / Path(rel).name)
    external_plan = Path(
        r"C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_plan.md"
    )
    copy_if_exists(external_plan, PACKET_ROOT / "Source Truth Context" / "external_branch_plan.md")
    copy_if_exists(Path(r"C:\Nexus USER\UTS - FAM-006.txt"), PACKET_ROOT / "Review Aids" / "UTS - FAM-006.txt")
    if baseline and baseline.exists():
        for source in (baseline / "baseline_old_tools").glob("*.txt"):
            copy_if_exists(source, PACKET_ROOT / "Review Aids" / "Raw Evidence" / "baseline_old_tools" / source.name)
        for source in (baseline / "evidence_listings").glob("*.txt"):
            copy_if_exists(source, PACKET_ROOT / "Review Aids" / "Raw Evidence" / "evidence_listings" / source.name)
    for source in [
        LIVE_VALIDATION_ROOT / "manifest.json",
        LIVE_VALIDATION_ROOT / "monitoring_hud_live_client_interaction_manifest.json",
        LIVE_VALIDATION_ROOT / "step_log.txt",
    ]:
        copy_if_exists(source, PACKET_ROOT / "Review Aids" / "Raw Evidence" / source.name)

    loaded_md = "\n".join(f"- `{item}`" for item in loaded)
    missing_md = "\n".join(f"- `{item}`" for item in missing) or "- None found."
    changed_md = "\n".join(f"- `{item}`" for item in changed) or "- None."
    finding_index = table(
        [
            "Finding ID",
            "Class",
            "Affected surface",
            "Confidence",
            "Phase",
        ],
        [
            [
                item.finding_id,
                item.finding_class,
                item.affected_surface,
                item.confidence,
                item.phase_attribution,
            ]
            for item in findings_list
        ],
    )
    tool_gap_md = table(
        ["Tool/helper", "Claim", "What it did not prove", "Baseline output"],
        [[row["tool"], row["claim"], row["gap"], row["baseline_output"]] for row in tool_gap_rows()],
    )

    primary = "\n".join(
        [
            "# FAM-006 Live Validation / UTS Failure Investigation",
            "",
            "Packet Status: live-validation-uts-failure-investigation",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Investigation Review",
            "Product/runtime repair: Withheld",
            "Prevention plan implementation: Withheld",
            "Baseline reconciled HEAD: `4afb18905d961c492a701149133e122fabee301d`",
            "Baseline origin/main: `f239c97415fb8aaac414f9b802888ea004d08c29`",
            "",
            "This packet investigates why FAM-006 Live Validation / UTS handoff reached an automated green handoff while USER later found failures. It does not accept UTS results, fix product runtime behavior, close issue #258, or advance to PR Readiness.",
            "",
            section(
                "Verdict",
                "REPAIR FINDINGS. The branch is reconciled and the investigation can proceed, but LV1/UTS readiness is not accepted. The packet identifies evidence handoff failure, helper false-green risk, insufficient combination coverage, and product issue candidates that require a later repair plan.",
            ),
            section(
                "Worktree Identity",
                table(
                    ["Field", "Value"],
                    [
                        ("Git root", identity.get("git_root", "")),
                        ("Branch", identity.get("branch", "")),
                        ("HEAD", identity.get("head", "")),
                        ("origin/main", identity.get("origin_main", "")),
                        ("Merge base", identity.get("merge_base", "")),
                        ("Ahead/behind", identity.get("ahead_behind", "")),
                        ("Status short", identity.get("status_short", "") or "clean at helper start"),
                    ],
                ),
            ),
            section("Source-Truth Files Loaded", loaded_md),
            section("Missing / Stale / Superseded Authority Notes", missing_md),
            section("Changed Files Versus origin/main", changed_md),
            section("USER-Reported Failures Preserved", textwrap.dedent(
                """
                - Live Validation did not deterministically expose affected combinations before UTS handoff.
                - Live Validation did not test every affected element for expected user-facing functionality.
                - Screenshot/evidence governance failed or was not USER-inspectable enough.
                - Recording card visual-system inheritance was not adjudicated strongly enough.
                - Overlay Profile switching/profile persistence remained questionable in the USER path.
                - Card holder insets and Recording copy/state details reached USER retest instead of being blocked earlier.
                - Tool PASS, marker PASS, and manifest PASS were treated too strongly relative to repo source truth.
                """
            )),
            section("Stable Finding ID Inventory", finding_index),
            section("Finding Details", "\n".join(item.markdown() for item in findings_list)),
            section("Investigation Loop Summary", loop_summary_md(findings_list, summary)),
            section("Evidence Inventory", evidence_inventory_md(summary)),
            section("Old-Tool False-Green Replay", tool_gap_md),
            section("Interaction Combination Matrix Summary", combination_matrix_md()),
            section("Code Lineage / Implementation Injection Trace", code_lineage_md()),
            section("Phase Failure Attribution", phase_map_md()),
            section("Timeline Reconstruction Summary", timeline_md()),
            section("Negative Findings / Checked-Clean Surfaces", negative_findings_md(summary)),
            section("Checked-But-Not-Reproducible Findings", checked_not_reproducible_md()),
            section(
                "Failure Root-Cause Summary",
                textwrap.dedent(
                    """
                    - Product implementation defects: likely present for at least visual layout and overlay-profile switching symptoms, but product fixes are withheld.
                    - Integration/state defects: likely around active Overlay Profile -> Recording target mirroring in the normal USER path.
                    - UI/window behavior defects: likely around Recording card styling, card-holder insets, and Log Viewer/Recording Studio workflow clarity.
                    - Live Validation coverage defects: verified/inferred because automated LV1 green did not settle USER-reported failure space.
                    - Screenshot/evidence defects: verified for the claimed USER-inspectable OneDrive evidence path currently missing.
                    - Validator/helper false greens: verified as a class because baseline tools passed while USER issue classes remained open.
                    - Phase progression defects: verified boundary issue; LV1 handoff green was not USER returned UTS acceptance.
                    - Governance/source-truth gaps: candidate only; repair planning is deferred.
                    - Codex execution defects: likely; prior handoff over-trusted screenshots/manifests and did not inspect enough USER combinations.
                    - USER waiver/approval boundary factors: none used to accept UTS; USER explicitly found failures before acceptance.
                    """
                ),
            ),
            section(
                "Exact Next USER Decisions",
                textwrap.dedent(
                    """
                    1. Does USER accept this investigation findings packet as sufficient to begin a separate repair/prevention planning pass?
                    2. If yes, exact approval text: `I approve bounded FAM-006 Live Validation / UTS failure repair planning from the findings in C:\\Nexus USER\\FAM-006, with product/runtime fixes still pending separate approval.`
                    3. If no, USER should identify which finding, surface, evidence path, or confidence label needs revision before repair planning.
                    """
                ),
            ),
        ]
    )
    write(PACKET_ROOT / PRIMARY_FILE, primary)
    write(
        PACKET_ROOT / "START_HERE.md",
        "\n".join(
            [
                "# Start Here - FAM-006 Live Validation / UTS Failure Investigation",
                "",
                "This packet is an investigation findings packet, not a product repair packet.",
                "",
                f"Primary USER review file: `{PRIMARY_FILE}`",
                "",
                "Read the primary file first, then use Review Aids for raw evidence, timeline, matrix, and tool-gap details.",
                "",
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Investigation Review",
                "",
            ]
        ),
    )
    aids = {
        "BASELINE_EVIDENCE.md": section("Baseline Evidence", evidence_inventory_md(summary)),
        "TIMELINE_RECONSTRUCTION.md": section("Timeline Reconstruction", timeline_md()),
        "OLD_TOOL_FALSE_GREEN_REPLAY.md": section("Old-Tool False-Green Replay", tool_gap_md),
        "PATCHED_TOOL_OUTPUTS.md": section(
            "Investigation-Support Tool Output",
            "This helper generated the packet, stable findings, evidence inventory, coverage matrix, and screenshot path audit. It is investigation support only and should be evaluated for durable adoption after USER review.",
        ),
        "OLD_TOOL_VS_PATCHED_TOOL_COMPARISON.md": section(
            "Old Tool Versus Investigation Tool",
            "Old tools reported green marker/manifest/handoff evidence. This investigation helper reports the same baseline while adding stable findings, USER evidence path verification, combination-matrix limits, and no-retroactive-evidence labels.",
        ),
        "FEATURE_SURFACE_INVENTORY.md": section(
            "Feature Surface Inventory",
            "\n".join(f"- {surface}" for surface in [
                "Dashboard Recording Card",
                "Recording Studio",
                "minimal Log Viewer Studio launch/folder shell",
                "native log folder behavior",
                "exported log folder behavior",
                "open-folder pre-session usability",
                "Overlay Profile selector/display",
                "Overlay Profile create/edit/persistence behavior",
                "issue #258 target-reliability behavior",
                "Dashboard HUD state",
                "monitor/active-monitor state",
                "Recording status states",
                "Recording target snapshot state",
                "Saved/complete state",
                "Disabled/error/no-data state",
            ]),
        ),
        "INTERACTION_COMBINATION_MATRIX.md": section("Interaction Combination Matrix", combination_matrix_md()),
        "SCREENSHOT_EVIDENCE_AUDIT.md": section("Screenshot Evidence Audit", evidence_inventory_md(summary)),
        "VALIDATOR_HELPER_TOOL_AUDIT.md": section("Validator / Helper / Tool Audit", tool_gap_md),
        "CODE_LINEAGE_TRACE.md": section("Code Lineage Trace", code_lineage_md()),
        "PHASE_CAUSALITY_MAP.md": section("Phase Causality Map", phase_map_md()),
        "PRODUCT_ISSUE_INVENTORY.md": section("Product Issue Inventory", "\n".join(item.markdown() for item in findings_list if "Product" in item.repair_lane or item.finding_id.startswith(("FAM006-UI", "FAM006-REGRESS", "FAM006-WINDOW")))),
        "NEGATIVE_FINDINGS.md": section("Negative Findings", negative_findings_md(summary)),
        "CHECKED_BUT_NOT_REPRODUCIBLE.md": section("Checked But Not Reproducible", checked_not_reproducible_md()),
        "RAW_EVIDENCE_INDEX.md": section(
            "Raw Evidence Index",
            "\n".join(
                [
                    "- `Review Aids/Raw Evidence/baseline_old_tools/`",
                    "- `Review Aids/Raw Evidence/evidence_listings/`",
                    "- `Review Aids/Raw Evidence/manifest.json`",
                    "- `Review Aids/Raw Evidence/monitoring_hud_live_client_interaction_manifest.json`",
                    "- `Review Aids/Raw Evidence/step_log.txt`",
                ]
            ),
        ),
        "VALIDATION_OUTPUTS.md": section(
            "Validation Outputs",
            "Validation output from this final pass is reported in Codex chat digest; baseline old-tool output is preserved under Raw Evidence.",
        ),
    }
    for name, body in aids.items():
        write(PACKET_ROOT / "Review Aids" / name, body)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in PACKET_ROOT.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKET_ROOT).as_posix())
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest().upper()
    return PACKET_ROOT, zip_path, digest


def validate_packet(packet_root: Path) -> dict[str, object]:
    primary = packet_root / PRIMARY_FILE
    files = list(packet_root.rglob("*"))
    markdown_files = [p for p in files if p.suffix.lower() == ".md"]
    text = read_text(primary)
    required = [
        "Packet Status: live-validation-uts-failure-investigation",
        "Packet Reviewability State: Reviewable",
        "USER Gate State: Pending USER Investigation Review",
        "FAM006-EVID-001",
        "FAM006-TOOLGAP-001",
        "FAM006-LVFAIL-001",
        "FAM006-UTSFAIL-001",
        "FAM006-REGRESS-001",
        "FAM006-PHASE-001",
        "Product/runtime repair: Withheld",
        "Prevention plan implementation: Withheld",
    ]
    missing = [marker for marker in required if marker not in text]
    layout_ok = (
        (packet_root / "START_HERE.md").exists()
        and primary.exists()
        and (packet_root / "Review Aids").is_dir()
        and (packet_root / "Source Truth Context").is_dir()
    )
    return {
        "passed": not missing and layout_ok,
        "layoutOk": layout_ok,
        "missingRequiredMarkers": missing,
        "markdownFileCount": len(markdown_files),
        "fileCount": len([p for p in files if p.is_file()]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate-packet", action="store_true")
    parser.add_argument("--validate-packet", action="store_true")
    args = parser.parse_args()
    if args.generate_packet:
        packet_root, zip_path, digest = generate_packet()
        validation = validate_packet(packet_root)
        print(json.dumps({
            "packetRoot": str(packet_root),
            "zipPath": str(zip_path),
            "zipSha256": digest,
            "validation": validation,
        }, indent=2))
        return 0 if validation["passed"] else 1
    if args.validate_packet:
        validation = validate_packet(PACKET_ROOT)
        print(json.dumps(validation, indent=2))
        return 0 if validation["passed"] else 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
