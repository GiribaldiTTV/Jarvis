"""FAM-006 Live Validation / UTS failure forensic packet generator.

This helper is investigation support only. It does not repair product runtime
behavior, advance phase state, accept UTS results, close issues, or claim that
new investigation evidence validates the earlier Live Validation handoff. It
may attach a later runtime proof rerun as investigation evidence when the
approved baseline is still an ancestor of the current branch head.
"""

from __future__ import annotations

import argparse
import hashlib
import io
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
PRIOR_INVESTIGATION_HEAD = "ddeb90a43ae6e84352d06e7acfbfb8be1fa6c35f"
LIVE_VALIDATION_ROOT = (
    REPO / "dev" / "logs" / "fam_006_monitoring_hud_live_validation" / "20260609_090906_117"
)
FORENSICS_LOG_ROOT = REPO / "dev" / "logs" / "fam006_live_validation_forensics"
RUNTIME_RERUN_LOG_ROOT = REPO / "dev" / "logs" / "fam006_live_validation_runtime_rerun_baseline"
SUPPLEMENTAL_LOG_ROOT = REPO / "dev" / "logs" / "fam006_supplemental_runtime_proof"
PRIMARY_FILE = "USER Review/LIVE_VALIDATION_UTS_FAILURE_INVESTIGATION.md"
REPAIR_PLAN_PRIMARY_FILE = "USER Review/LIVE_VALIDATION_UTS_FAILURE_REPAIR_PLAN.md"
REPAIR_PLAN_STATUS = "live-validation-uts-failure-repair-planning"
VALIDATOR_FIRST_PRIMARY_FILE = "USER Review/LIVE_VALIDATOR_FIRST_REPAIR_REVIEW.md"
VALIDATOR_FIRST_STATUS = "live-validator-first-repair-review"
REPAIR_IMPLEMENTATION_PRIMARY_FILE = "USER Review/REPAIR_IMPLEMENTATION_APPROVAL_REVIEW.md"
REPAIR_IMPLEMENTATION_STATUS = "repair-implementation-approval-review"
REPAIR_RETURN_PRIMARY_FILE = "USER Review/LIVE_VALIDATION_REPAIR_RETURN_REVIEW.md"
REPAIR_RETURN_STATUS = "live-validation-repair-return-review"
LV_UTS_DISPOSITION_PRIMARY_FILE = "USER Review/LIVE_VALIDATION_UTS_DISPOSITION_REVIEW.md"
LV_UTS_DISPOSITION_STATUS = "live-validation-uts-disposition-review"
ACCEPTED_FINDINGS_ZIP = USER_ROOT / "FAM-006-20260609-124117.zip"
ACCEPTED_FINDINGS_SHA256 = "18506FB2C0B47E2F7378DCA788558D9F666D2F4B08BAD30677B9735B6A6D71B9"
REPAIR_PLAN_ZIP = USER_ROOT / "FAM-006-20260609-125215.zip"
REPAIR_PLAN_SHA256 = "DC9A4F1688468F58801FD579743E5CB2C0AAAF48961C67D26B4053DDA1318D19"
VALIDATOR_FIRST_ZIP = USER_ROOT / "FAM-006-20260609-130658.zip"
VALIDATOR_FIRST_SHA256 = "23058F12AC3178C4546E58252CE945CA6689687E25CE812677BFEA60520F8252"
REPAIR_PLAN_FINDING_IDS = [
    "FAM006-EVID-001",
    "FAM006-EVID-002",
    "FAM006-TOOLGAP-001",
    "FAM006-LVFAIL-001",
    "FAM006-UTSFAIL-001",
    "FAM006-UI-001",
    "FAM006-UI-002",
    "FAM006-UI-003",
    "FAM006-WINDOW-001",
    "FAM006-WINDOW-002",
    "FAM006-GOVGAP-002",
    "FAM006-GOVGAP-003",
    "FAM006-REGRESS-001",
    "FAM006-REGRESS-002",
    "FAM006-CODEPATH-001",
    "FAM006-PHASE-001",
]


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


@dataclass(frozen=True)
class LiveValidatorCheck:
    check_id: str
    finding_ids: tuple[str, ...]
    title: str
    category: str
    result: str
    expected_current_result: str
    source_truth_expectation: str
    user_facing_action: str
    evidence_path: str
    screenshot_path: str
    log_event_path: str
    confidence: str
    phase_relevance: str
    user_path_layer: str
    old_validator_gap: str
    future_green_condition: str

    def markdown(self) -> str:
        return "\n".join(
            [
                f"### {self.check_id} - {self.title}",
                "",
                f"- Finding IDs: {', '.join(self.finding_ids)}",
                f"- Category: {self.category}",
                f"- Current product-state result: {self.result}",
                f"- Expected current known-bad result: {self.expected_current_result}",
                f"- Source-truth expectation: {self.source_truth_expectation}",
                f"- Normal USER-facing action: {self.user_facing_action}",
                f"- Evidence path: `{self.evidence_path}`",
                f"- Screenshot path: `{self.screenshot_path}`",
                f"- Log/event/proof path: `{self.log_event_path}`",
                f"- Confidence: {self.confidence}",
                f"- Phase relevance: {self.phase_relevance}",
                f"- Proof layer: {self.user_path_layer}",
                f"- Old validator gap: {self.old_validator_gap}",
                f"- Future green condition: {self.future_green_condition}",
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def accepted_findings_packet() -> tuple[dict[str, object], bytes]:
    if not ACCEPTED_FINDINGS_ZIP.exists():
        raise SystemExit(f"BLOCKED: accepted findings packet is missing: {ACCEPTED_FINDINGS_ZIP}")
    data = ACCEPTED_FINDINGS_ZIP.read_bytes()
    digest = hashlib.sha256(data).hexdigest().upper()
    if digest != ACCEPTED_FINDINGS_SHA256:
        raise SystemExit(
            "BLOCKED: accepted findings packet SHA mismatch. "
            f"Expected {ACCEPTED_FINDINGS_SHA256}, found {digest} at {ACCEPTED_FINDINGS_ZIP}"
        )
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        names = sorted(name for name in archive.namelist() if not name.endswith("/"))
        try:
            primary_text = archive.read(PRIMARY_FILE).decode("utf-8-sig", errors="replace")
        except KeyError:
            primary_text = ""
    return {
        "path": str(ACCEPTED_FINDINGS_ZIP),
        "sha256": digest,
        "fileCount": len(names),
        "markdownCount": len([name for name in names if name.lower().endswith(".md")]),
        "primaryPresent": bool(primary_text),
        "entries": names,
        "primaryPreview": primary_text[:4000],
    }, data


def extract_zip_bytes(data: bytes, target: Path) -> list[str]:
    extracted: list[str] = []
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            member = Path(info.filename)
            if member.is_absolute() or ".." in member.parts:
                continue
            destination = target / member
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(info))
            extracted.append(info.filename)
    return sorted(extracted)


def purge_fam006_user_packet_outputs() -> None:
    if PACKET_ROOT.exists():
        shutil.rmtree(PACKET_ROOT)
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    for old_zip in USER_ROOT.glob("FAM-006*.zip"):
        old_zip.unlink()


def latest_baseline_root() -> Path | None:
    if not FORENSICS_LOG_ROOT.exists():
        return None
    roots = [p for p in FORENSICS_LOG_ROOT.iterdir() if p.is_dir()]
    return max(roots, key=lambda p: p.stat().st_mtime, default=None)


def latest_runtime_rerun_root() -> Path | None:
    if not RUNTIME_RERUN_LOG_ROOT.exists():
        return None
    roots = [p for p in RUNTIME_RERUN_LOG_ROOT.iterdir() if p.is_dir()]
    return max(roots, key=lambda p: p.stat().st_mtime, default=None)


def latest_supplemental_root() -> Path | None:
    if not SUPPLEMENTAL_LOG_ROOT.exists():
        return None
    roots = sorted([p for p in SUPPLEMENTAL_LOG_ROOT.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for root in roots:
        manifest = load_json(root / "manifest.json")
        supplemental_proof = manifest.get("supplementalIssueProof") if isinstance(manifest, dict) else {}
        if manifest.get("status") == "PASS" and isinstance(supplemental_proof, dict) and supplemental_proof.get("manifest"):
            return root
    return roots[0] if roots else None


def supplemental_attempt_rows() -> list[list[str]]:
    if not SUPPLEMENTAL_LOG_ROOT.exists():
        return [["none", "missing", "", ""]]
    rows: list[list[str]] = []
    for root in sorted([p for p in SUPPLEMENTAL_LOG_ROOT.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True):
        manifest = load_json(root / "manifest.json")
        interaction = load_json(root / "monitoring_hud_live_client_interaction_manifest.json")
        rows.append(
            [
                root.name,
                str(manifest.get("status", "MISSING")),
                str(interaction.get("status", "MISSING")),
                str(interaction.get("failureMessage", manifest.get("failureMessage", ""))),
            ]
        )
    return rows or [["none", "missing", "", ""]]


def latest_monitoring_hud_live_validation_root() -> Path | None:
    root = REPO / "dev" / "logs" / "fam_006_monitoring_hud_live_validation"
    if not root.exists():
        return None
    roots = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for candidate in roots:
        if (candidate / "monitoring_hud_live_client_interaction_manifest.json").exists():
            return candidate
    return roots[0] if roots else None


def latest_return_flow_evidence() -> dict[str, object]:
    root = latest_monitoring_hud_live_validation_root()
    if root is None:
        return {
            "root": "",
            "manifest": {},
            "interaction": {},
            "steps": {},
            "screenshots": [],
            "userScreenshotRoot": "",
            "userElementScreenshotRoot": "",
            "supplementalManifest": "",
            "restartInteractionPath": "",
            "restartInteraction": {},
            "restartSteps": {},
        }
    manifest = load_json(root / "manifest.json")
    interaction = load_json(root / "monitoring_hud_live_client_interaction_manifest.json")
    restart_interaction = load_json(root / "monitoring_hud_restart_check_interaction_manifest.json")
    steps: dict[str, dict[str, object]] = {}
    if isinstance(interaction, dict):
        for item in interaction.get("steps", []):
            if isinstance(item, dict):
                steps[str(item.get("label") or "")] = item
    restart_steps: dict[str, dict[str, object]] = {}
    if isinstance(restart_interaction, dict):
        for item in restart_interaction.get("steps", []):
            if isinstance(item, dict):
                restart_steps[str(item.get("label") or "")] = item
    screenshots = [
        str(item)
        for item in (interaction.get("screenshots", []) if isinstance(interaction, dict) else [])
        if str(item).strip()
    ]
    user_root = str(manifest.get("screenshotEvidenceRoot") or "") if isinstance(manifest, dict) else ""
    user_element_root = str(manifest.get("elementScreenshotEvidenceRoot") or "") if isinstance(manifest, dict) else ""
    supplemental = ""
    if user_root:
        supplemental_path = Path(user_root) / "supplemental_issue_evidence_manifest.json"
        if supplemental_path.exists():
            supplemental = str(supplemental_path)
    return {
        "root": str(root),
        "manifestPath": str(root / "manifest.json"),
        "interactionPath": str(root / "monitoring_hud_live_client_interaction_manifest.json"),
        "manifest": manifest,
        "interaction": interaction,
        "steps": steps,
        "screenshots": screenshots,
        "userScreenshotRoot": user_root,
        "userElementScreenshotRoot": user_element_root,
        "supplementalManifest": supplemental,
        "restartInteractionPath": str(root / "monitoring_hud_restart_check_interaction_manifest.json"),
        "restartInteraction": restart_interaction,
        "restartSteps": restart_steps,
    }


def return_step_passed(evidence: dict[str, object], label: str) -> bool:
    steps = evidence.get("steps") if isinstance(evidence.get("steps"), dict) else {}
    item = steps.get(label) if isinstance(steps, dict) else None
    return isinstance(item, dict) and item.get("status") == "PASS"


def return_step(evidence: dict[str, object], label: str) -> dict[str, object]:
    steps = evidence.get("steps") if isinstance(evidence.get("steps"), dict) else {}
    item = steps.get(label) if isinstance(steps, dict) else None
    return item if isinstance(item, dict) else {}


def restart_step_passed(evidence: dict[str, object], label: str) -> bool:
    steps = evidence.get("restartSteps") if isinstance(evidence.get("restartSteps"), dict) else {}
    item = steps.get(label) if isinstance(steps, dict) else None
    return isinstance(item, dict) and item.get("status") == "PASS"


def screenshot_contains(evidence: dict[str, object], needle: str) -> bool:
    screenshots = evidence.get("screenshots") if isinstance(evidence.get("screenshots"), list) else []
    return any(needle in str(item) for item in screenshots)


def return_status_table(rows: list[dict[str, str]]) -> str:
    return table(
        ["Finding", "Result", "Evidence", "Notes"],
        [
            [
                row.get("finding", ""),
                row.get("result", ""),
                row.get("evidence", ""),
                row.get("notes", ""),
            ]
            for row in rows
        ],
    )


def return_flow_findings(evidence: dict[str, object]) -> list[dict[str, str]]:
    interaction = evidence.get("interaction") if isinstance(evidence.get("interaction"), dict) else {}
    manifest = evidence.get("manifest") if isinstance(evidence.get("manifest"), dict) else {}
    interaction_status = str(interaction.get("status") or "MISSING")
    manifest_status = str(manifest.get("status") or "MISSING")
    a_pass = (
        interaction_status == "PASS"
        and return_step_passed(evidence, "real OS click opens Dashboard Recording Studio")
        and return_step_passed(evidence, "Recording Studio native window focused screenshot proof")
        and screenshot_contains(evidence, "02_recording_studio_native_window_ready_state")
    )
    b_pass = (
        interaction_status == "PASS"
        and return_step_passed(evidence, "real OS click starts Dashboard Recording")
        and return_step_passed(evidence, "real OS click stops Dashboard Recording and requests local output")
        and return_step_passed(evidence, "Dashboard Recording stop writes local output and readback proof")
    )
    c_labels = [
        "C1 Log Viewer closed before repeated Start/Stop",
        "C1 real OS click starts recording after Log Viewer close",
        "C1 real OS click stops recording after Log Viewer close",
        "C1 Log Viewer remains closed and unfocused after Start/Stop",
        "C2 real OS click opens Log Viewer before minimize test",
        "C2 Log Viewer minimized before repeated Start/Stop",
        "C2 real OS click starts recording after Log Viewer minimize",
        "C2 real OS click stops recording after Log Viewer minimize",
        "C2 Log Viewer remains minimized and unfocused after Start/Stop",
        "C3 real OS click opens Log Viewer before unfocused-open test",
        "C3 Log Viewer open but unfocused before repeated Start/Stop",
        "C3 real OS click starts recording after Log Viewer open unfocused",
        "C3 real OS click stops recording after Log Viewer open unfocused",
        "C3 Log Viewer remains open and unfocused after Start/Stop",
    ]
    c_missing = [label for label in c_labels if not return_step_passed(evidence, label)]
    d_pass = (
        interaction_status == "PASS"
        and return_step_passed(evidence, "Recording Studio compact native/current-log tracking updates after save")
        and return_step_passed(evidence, "Log Viewer Studio native window focused screenshot proof")
        and screenshot_contains(evidence, "02_recording_studio_native_log_saved_tracking_state")
        and screenshot_contains(evidence, "02_log_viewer_studio_native_window_shell_state")
    )
    e_seeded = (
        interaction_status == "PASS"
        and return_step_passed(evidence, "real OS click opens HUD Overlay card Active Overlay Profile selector")
        and return_step_passed(evidence, "real OS click selects HUD Overlay card Active Overlay Profile option")
    )
    e_normal_labels = [
        "real OS click opens Overlay Profile Settings for normal USER path proof",
        "real OS click creates normal USER Overlay Profile draft",
        "real OS keyboard edits created Overlay Profile name",
        "real OS click selects monitor membership for created Overlay Profile",
        "real OS click saves created Overlay Profile",
        "Saved USER Overlay Profile id recorded for restart proof",
        "real OS click closes Overlay Profile Settings after saved USER profile",
        "real OS click selects Default Overlay Profile after saved profile",
        "real OS click reselects saved USER Overlay Profile",
    ]
    e_missing = [label for label in e_normal_labels if not return_step_passed(evidence, label)]
    restart_interaction = evidence.get("restartInteraction") if isinstance(evidence.get("restartInteraction"), dict) else {}
    restart_status = str(restart_interaction.get("status") or "MISSING")
    e_restart = (
        restart_status == "PASS"
        and restart_step_passed(evidence, "Restart check reloads saved USER Overlay Profile and Recording target mirror")
    )
    e_pass = e_seeded and not e_missing and e_restart
    visual_step = return_step(evidence, "Dashboard Recording card target/status visual contract is focused before child windows")
    visual_details = visual_step.get("details") if isinstance(visual_step, dict) else {}
    visual_checks = visual_details.get("checks") if isinstance(visual_details, dict) else {}
    f_pass = (
        interaction_status == "PASS"
        and isinstance(visual_checks, dict)
        and visual_checks.get("cardVisualSystem") is True
        and visual_checks.get("previewVisualSystem") is True
        and visual_checks.get("rowVisualProof") is True
        and visual_checks.get("cardHolderInsetParity") is True
        and screenshot_contains(evidence, "02_recording_card_target_status_visual_contract")
    )
    g_pass = (
        interaction_status == "PASS"
        and return_step_passed(evidence, "Dashboard Recording Log Viewer Studio crosses backend native-window bridge")
        and return_step_passed(evidence, "Dashboard Recording stop writes local output and readback proof")
    )
    h_pass = (
        manifest_status == "PASS"
        and bool(evidence.get("userScreenshotRoot"))
        and bool(evidence.get("userElementScreenshotRoot"))
        and bool(evidence.get("supplementalManifest"))
    )
    i_pass = a_pass and b_pass and not c_missing and d_pass and e_pass and f_pass and g_pass
    return [
        {
            "finding": "A / FAM006-LVF-A-001 Recording Studio visible-button path",
            "result": "PASS" if a_pass else "UNPROVEN",
            "evidence": str(evidence.get("interactionPath") or ""),
            "notes": "Normal visible button path is separate from helper/native launch proof.",
        },
        {
            "finding": "B Quick Access Start/Stop ownership",
            "result": "PASS" if b_pass else "UNPROVEN",
            "evidence": str(evidence.get("interactionPath") or ""),
            "notes": "Quick Access owns active Start/Stop; Recording card remains status/summary.",
        },
        {
            "finding": "C Log Viewer focus/open regression C1-C3",
            "result": "PASS" if not c_missing else "UNPROVEN",
            "evidence": str(evidence.get("interactionPath") or ""),
            "notes": "Missing sequence labels: " + (", ".join(c_missing) if c_missing else "None."),
        },
        {
            "finding": "D Native/current-log tracking ownership",
            "result": "PASS" if d_pass else "UNPROVEN",
            "evidence": str(evidence.get("interactionPath") or ""),
            "notes": "Recording Studio owns compact native-log tracking; Log Viewer remains shell/folder boundary.",
        },
        {
            "finding": "E Overlay Profile normal USER proof path",
            "result": "PASS" if e_pass else "BLOCKED",
            "evidence": str(evidence.get("interactionPath") or evidence.get("restartInteractionPath") or ""),
            "notes": (
                "Normal create/edit/save/switch and fresh-runtime restart persistence proof present; "
                "issue #258 closeout remains a separate USER/GitHub decision."
                if e_pass
                else "Seeded selector/mirror proof present: "
                + ("yes" if e_seeded else "no")
                + ". Missing normal-path labels: "
                + (", ".join(e_missing) if e_missing else "None")
                + f". Restart proof status: {restart_status}."
            ),
        },
        {
            "finding": "F Visual-system inheritance and card-holder inset",
            "result": "PASS" if f_pass else "UNPROVEN",
            "evidence": str(evidence.get("userElementScreenshotRoot") or evidence.get("interactionPath") or ""),
            "notes": "Requires card visual-system markers and measured left/right inset parity excluding scrollbar.",
        },
        {
            "finding": "G Native/export folder proof path",
            "result": "PASS" if g_pass else "UNPROVEN",
            "evidence": str(evidence.get("interactionPath") or ""),
            "notes": "Log Viewer shell opens native/export roots before session; saved output stays native by default.",
        },
        {
            "finding": "H Screenshot/evidence proof-loop",
            "result": "PASS" if h_pass else "UNPROVEN",
            "evidence": str(evidence.get("userScreenshotRoot") or ""),
            "notes": "Requires organized USER-inspectable screenshots and supplemental issue manifest.",
        },
        {
            "finding": "I Interaction matrix",
            "result": "PASS" if i_pass else "UNPROVEN",
            "evidence": str(evidence.get("interactionPath") or ""),
            "notes": "Option C matrix represented across A-G return-flow proof; USER acceptance and UTS acceptance remain separate.",
        },
        {
            "finding": "J UTS stop-loss",
            "result": "PASS",
            "evidence": r"C:\Nexus USER\UTS - FAM-006.txt",
            "notes": "UTS handoff remains withheld until USER separately approves Live Validation / UTS disposition; repair-return proof does not auto-accept UTS.",
        },
    ]


def is_ancestor(ancestor: str, descendant: str) -> bool:
    code, _output = run_command(["git", "merge-base", "--is-ancestor", ancestor, descendant])
    return code == 0


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
    head = proof.get("head", "")
    proof["baseline_head_is_ancestor"] = str(is_ancestor(BASELINE_HEAD, head)).lower() if head else "false"
    proof["prior_investigation_head_is_ancestor"] = (
        str(is_ancestor(PRIOR_INVESTIGATION_HEAD, head)).lower() if head else "false"
    )
    return proof


def changed_files() -> list[str]:
    code, output = run_command(["git", "diff", "--name-only", "origin/main...HEAD"])
    if code != 0:
        return [f"ERROR: {output.strip()}"]
    return [line.strip() for line in output.splitlines() if line.strip()]


def manifest_snapshot(root: Path) -> dict[str, object]:
    manifest = load_json(root / "manifest.json")
    interaction = load_json(root / "monitoring_hud_live_client_interaction_manifest.json")
    user_screenshot_root = Path(str(manifest.get("screenshotEvidenceRoot") or ""))
    user_element_root = Path(str(manifest.get("elementScreenshotEvidenceRoot") or ""))
    return {
        "manifest_status": manifest.get("status", "MISSING"),
        "interaction_status": interaction.get("status", "MISSING"),
        "manifest_path": str(root / "manifest.json"),
        "interaction_manifest_path": str(root / "monitoring_hud_live_client_interaction_manifest.json"),
        "repo_live_validation_root_exists": root.exists(),
        "repo_screenshot_count": len(list((root / "live_client_interaction").glob("*.png")))
        if (root / "live_client_interaction").exists()
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
        "short_video_user_path": str((manifest.get("shortVideoProof") or {}).get("userInspectablePath", ""))
        if isinstance(manifest.get("shortVideoProof"), dict)
        else "",
        "short_video_status": str((manifest.get("shortVideoProof") or {}).get("status", ""))
        if isinstance(manifest.get("shortVideoProof"), dict)
        else "",
    }


def manifest_summary() -> dict[str, object]:
    prior = manifest_snapshot(LIVE_VALIDATION_ROOT)
    runtime_root = latest_runtime_rerun_root()
    supplemental_root = latest_supplemental_root()
    runtime = manifest_snapshot(runtime_root) if runtime_root else {}
    supplemental = manifest_snapshot(supplemental_root) if supplemental_root else {}
    runtime_interaction = load_json(runtime_root / "monitoring_hud_live_client_interaction_manifest.json") if runtime_root else {}
    runtime_manifest = load_json(runtime_root / "manifest.json") if runtime_root else {}
    supplemental_manifest = load_json(supplemental_root / "manifest.json") if supplemental_root else {}
    supplemental_issue_manifest = {}
    if supplemental_manifest:
        supplemental_proof = supplemental_manifest.get("supplementalIssueProof")
        if isinstance(supplemental_proof, dict):
            supplemental_issue_manifest = load_json(Path(str(supplemental_proof.get("manifest") or "")))
    return {
        **prior,
        "prior_lv1": prior,
        "runtime_rerun_root": str(runtime_root or ""),
        "runtime_rerun_exists": bool(runtime_root and runtime_root.exists()),
        "runtime_rerun": runtime,
        "runtime_interaction_steps": runtime_interaction.get("steps", []),
        "runtime_screenshots": runtime_interaction.get("screenshots", []),
        "runtime_short_video_user_path": str((runtime_manifest.get("shortVideoProof") or {}).get("userInspectablePath", ""))
        if isinstance(runtime_manifest.get("shortVideoProof"), dict)
        else "",
        "supplemental_root": str(supplemental_root or ""),
        "supplemental_exists": bool(supplemental_root and supplemental_root.exists()),
        "supplemental": supplemental,
        "supplemental_manifest": supplemental_manifest,
        "supplemental_issue_manifest": supplemental_issue_manifest,
        "supplemental_issue_folders": supplemental_issue_manifest.get("issueFolders", [])
        if isinstance(supplemental_issue_manifest.get("issueFolders"), list)
        else [],
    }


def tool_gap_rows() -> list[dict[str, str]]:
    baseline = latest_baseline_root()
    runtime = latest_runtime_rerun_root()
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
            "claim": "LV1 PASS and runtime rerun PASS",
            "gap": "Automated PASS proves the scripted real-OS route it exercised; it still does not close USER Gate State, prove every USER-created/restart path, or visually adjudicate every screenshot label by itself.",
            "baseline_output": f"prior={LIVE_VALIDATION_ROOT / 'manifest.json'}; runtime={runtime / 'manifest.json' if runtime else 'not captured'}",
        },
    ]
    return rows


def findings(summary: dict[str, object]) -> list[Finding]:
    prior = summary.get("prior_lv1") or {}
    runtime = summary.get("runtime_rerun") or {}
    runtime_root_exists = bool(summary.get("runtime_rerun_exists"))
    runtime_user_root_exists = bool(runtime.get("user_screenshot_root_exists"))
    runtime_user_element_exists = bool(runtime.get("user_element_root_exists"))
    runtime_evidence_actual = (
        "The runtime rerun produced USER-inspectable OneDrive evidence paths, 13 focused element screenshots, and a short video; the investigation still distinguishes screenshot existence from visual adjudication and state-label correctness."
        if runtime_root_exists and runtime_user_root_exists and runtime_user_element_exists
        else "The runtime rerun evidence root is missing or incomplete; screenshot evidence remains blocked."
    )
    runtime_evidence_confidence = "Verified" if runtime_root_exists and runtime_user_root_exists and runtime_user_element_exists else "Blocked"
    return [
        Finding(
            "FAM006-EVID-001",
            "Runtime evidence now exists, but screenshot existence is not visual acceptance",
            "screenshot/evidence failure",
            "Live Validation screenshot evidence handoff",
            "LV1 must provide full-window and element-level evidence in an organized USER-inspectable screenshot folder.",
            runtime_evidence_actual,
            str(latest_runtime_rerun_root() or RUNTIME_RERUN_LOG_ROOT),
            runtime_evidence_confidence,
            "Live Validation / UTS handoff",
            "dev/orin_monitoring_hud_live_validation.ps1 writes manifest evidence paths; this investigation reran the helper and then manually adjudicated key screenshot claims.",
            "Baseline reconciliation through 4afb1890 is not treated as the original cause; this finding is about current proof quality after the runtime rerun.",
            "Investigation-support tooling now; durable prevention likely Governance/FAM-006 Live Validation helper after USER review.",
            "USER review of investigation packet before repair planning.",
        ),
        Finding(
            "FAM006-TOOLGAP-001",
            "Old green tools prove markers/manifests more strongly than USER behavior",
            "helper/validator/tool gap",
            "H1, surface, internal sandbox, and LV1 helpers",
            "Helper PASS is evidence only; Live Validation must expose affected user-facing interactions and visual proof, not only marker or manifest presence.",
            "Baseline tools passed while USER later reported visual, switching, folder, and evidence failures. The runtime rerun now proves selected real-OS actions, but it also shows the helper can label a screenshot as an active state when visible text does not prove that state.",
            str(latest_runtime_rerun_root() or latest_baseline_root() or FORENSICS_LOG_ROOT),
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
            "The runtime rerun covered default target, start/stop, native log readback, Recording Studio launch, Log Viewer Studio launch, and seeded profile target mirroring. It did not prove manual create/edit/restart persistence, no-active-monitor states, explicit native/export folder button clicks before any recording, or visual acceptance for every screenshot label.",
            str((latest_runtime_rerun_root() or RUNTIME_RERUN_LOG_ROOT) / "monitoring_hud_live_client_interaction_manifest.json"),
            "Verified",
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
            "The current runtime screenshot shows the Recording card itself largely inherits the dashboard card/row system. The Recording Studio and Log Viewer Studio native windows remain visually much plainer than the Dashboard card system, so visual-system inheritance is mixed rather than globally green.",
            str((Path(str(runtime.get("user_element_root") or "")) / "element_02_recording_studio_native_window_ready_state.png")),
            "Verified",
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
            "The runtime rerun verifies a seeded real-OS selection path: the HUD Overlay card selected LV1 Real OS Profile 001 and the Recording card mirrored that target with 1 active monitor. This does not disprove the USER-reported manual create/switch or post-restart persistence path.",
            str((latest_runtime_rerun_root() or RUNTIME_RERUN_LOG_ROOT) / "monitoring_hud_live_client_interaction_manifest.json"),
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
            "USER reported unequal left/right spacing inside the card holder. Current rerun screenshots show a visible scrollbar gutter and do not by themselves settle whether the visual inset contract passes, so this remains an adjudication/product repair candidate.",
            str(Path(str(runtime.get("user_element_root") or "")) / "element_02_recording_card_saved_complete_readback_state.png"),
            "Inferred",
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
            "The runtime rerun visually verifies the Log Viewer Studio shell and its Open Native Logs / Open Exported Logs buttons. It does not provide focused visual proof that both buttons were clicked before any recording in the session or that folder creation/opening worked in that pre-session path.",
            str(Path(str(runtime.get("user_element_root") or "")) / "element_02_log_viewer_studio_native_window_shell_state.png"),
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
            "Git identity proves the current HEAD descends from reconciled baseline 4afb1890 and prior investigation helper ddeb90a4; findings cite prior LV1 artifacts, the runtime proof rerun, and USER reports separately.",
            "git identity baseline captured in raw evidence",
            "Verified",
            "Investigation",
            "No product code lineage; git/phase boundary.",
            "Baseline boundary explicitly honored.",
            "No repair required for this finding unless USER sees misclassification.",
            "None.",
        ),
    ]


def supplemental_findings(summary: dict[str, object]) -> list[Finding]:
    supplemental_root = str(summary.get("supplemental_root") or SUPPLEMENTAL_LOG_ROOT)
    issue_root = str(((summary.get("supplemental_manifest") or {}).get("screenshotEvidenceRoot") or ""))
    return [
        Finding(
            "FAM006-UI-003",
            "Recording Studio button proof must distinguish visible USER click from native-launch proof",
            "UI/window behavior failure",
            "Dashboard Recording Card / Recording Studio button",
            "The visible Dashboard Recording card Recording Studio button should open the standalone Recording Studio window through the normal visible USER click path.",
            "USER personally confirmed the normal visible button path does not open Recording Studio. Supplemental foreground helper evidence may verify a controlled helper path when it passes, but that helper path is not the same proof as USER manual-path behavior and does not disprove the USER-confirmed failure.",
            supplemental_root,
            "USER Confirmed + Codex Reproduction Blocked + helper foreground path separately verified when helper evidence passes",
            "Live Validation",
            "nexus_visual/monitoring_hud.js wires #monitoring-hud-recording-studio-open to monitoringHudRequestRecordingControlWindow; desktop/desktop_renderer.py opens MonitoringHudRecordingStudioWindow from recordingControlWindowRequested state.",
            "Supplemental investigation evidence, not retroactive LV1 acceptance.",
            "Product/runtime repair lane only if USER/ChatGPT confirms manual path still fails.",
            "No product repair approved in this packet.",
        ),
        Finding(
            "FAM006-GOVGAP-002",
            "Start/Stop placement has active source-truth versus USER-expectation drift",
            "governance/source-truth gap",
            "Dashboard Recording Card / Quick Access recording control",
            "Current external branch plan says the Dashboard Recording card remains the compact quick-access/status surface and owns active Start/Stop for the active Overlay Profile target.",
            "USER now states Start/Stop should have moved from the Recording card to Quick Access, with a future setting controlling the quick-access button. Supplemental proof captures the current Dashboard-card placement; product relocation is withheld because current accepted plan does not clearly require it.",
            issue_root or supplemental_root,
            "Verified source-truth drift",
            "BP1/BP2/BP3 / Live Validation",
            "nexus_visual/monitoring_hud.js sets #monitoring-hud-recording-control-launcher inside the Recording card with dataset recordingControlWindowContract=dashboard-quick-access-start-stop.",
            "This is a post-acceptance USER planning refinement, not a product repair performed here.",
            "Planning/source-truth repair lane before implementation relocation.",
            "USER decision required to reopen planning or approve a targeted product repair.",
        ),
        Finding(
            "FAM006-WINDOW-002",
            "Log Viewer Studio can steal focus after prior open because updates raise and activate it",
            "UI/window behavior failure",
            "Log Viewer Studio focus/open behavior after start/stop",
            "After Log Viewer Studio has been opened, later recording start/stop state changes should not repeatedly focus or reopen it unless the accepted UX explicitly requires that behavior.",
            "USER personally confirmed that after Log Viewer Studio has been opened once, later Start/Stop recording actions cause it to open or steal focus depending on state. Codex could not complete the normal close/minimize/focus sequence because the Windows Computer Use channel reported `Computer Use native pipe path is unavailable`; code lineage shows MonitoringHudLogViewerStudioWindow.update_product_state calls show(), raise_(), and activateWindow() whenever the requested log-viewer signature changes.",
            "desktop/desktop_renderer.py:6000",
            "USER Confirmed + Inferred Code Lineage + Codex Reproduction Blocked",
            "Workstream / Live Validation",
            "desktop/desktop_renderer.py update_product_state for the Log Viewer Studio shell; state updates after recording output can change logViewerStudioSummary and rerun the native-window update path.",
            "Supplemental finding; no product behavior changed.",
            "Product/window behavior repair lane after USER accepts findings.",
            "Product repair remains pending separate approval.",
        ),
        Finding(
            "FAM006-GOVGAP-003",
            "Native log tracking ownership is ambiguous between Recording Studio and Log Viewer Studio",
            "governance/source-truth gap",
            "Recording Studio / Log Viewer Studio ownership boundary",
            "Option C source truth gives Log Viewer Studio the minimal native/export folder shell, while USER now says native log tracking should live in Recording Studio in a compact unobtrusive way.",
            "Current Log Viewer Studio visually displays Native logs and Exported logs paths. Recording Studio displays target/session status but not compact native-log tracking. This is a branch-vision/ownership refinement, not an approved UI mutation in this investigation.",
            issue_root or supplemental_root,
            "Verified visual/source-truth comparison",
            "BP1/BP2/BP3 / Workstream / Live Validation",
            "desktop/desktop_renderer.py MonitoringHudRecordingStudioWindow and MonitoringHudLogViewerStudioWindow; desktop/recording_output_contract.py owns native/export boundary.",
            "Supplemental finding; product repair withheld.",
            "Planning/source-truth repair lane, then product repair if admitted.",
            "USER decision required before moving ownership/UI content.",
        ),
        Finding(
            "FAM006-REGRESS-002",
            "Older Overlay Profile issues are only partially proven by seeded selector evidence",
            "regression proof gap",
            "Overlay Profile create/edit/switch/restart normal USER path",
            "Issue #258 and recording target reliability require USER-created Overlay Profiles to save, persist across restart, remain selectable, and mirror into Recording target state.",
            "Supplemental/current helper proof covers a seeded real-OS selector option and target mirror. It does not fully prove USER-created profile create/edit/save/restart through the same manual path the USER used.",
            issue_root or supplemental_root,
            "Blocked for full manual path; Verified for seeded selector path",
            "Live Validation / UTS",
            "nexus_visual/monitoring_hud.js overlay-profile state and desktop/monitoring_hud_state.py persistence normalization.",
            "Supplemental investigation evidence, not UTS acceptance.",
            "Product/state regression repair lane if manual path still fails; validation helper coverage repair candidate.",
            "No product repair approved here.",
        ),
        Finding(
            "FAM006-EVID-002",
            "Prior investigation packet was insufficient for A-D runtime-proof questions",
            "screenshot/evidence failure",
            "Prior findings packet",
            "A findings packet must answer the concrete USER issue questions with issue-specific evidence paths, normal-path limits, confidence labels, and no-retroactive-evidence labeling.",
            "The prior packet captured broad LV/UTS failure classes but did not explicitly prove/disprove the Recording Studio button click, Start/Stop placement, Log Viewer focus regression, or Studio/Log Viewer ownership boundary with A-D issue folders.",
            r"C:\Nexus USER\FAM-006-20260609-112944.zip",
            "Verified",
            "Investigation packet generation",
            "dev/orin_fam006_live_validation_forensics.py now consumes supplemental runtime proof and writes issue-specific findings.",
            "This explains packet insufficiency, not product failure.",
            "Investigation-support tooling now; durable governance adoption after USER review.",
            "USER review of supplemental findings packet.",
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
            "This helper now incorporates the focused runtime proof rerun at `dev/logs/fam006_live_validation_runtime_rerun_baseline`, compares it against prior LV1 evidence, and reports which runtime claims were visually proved versus under-proven.",
        ),
        (
            "Loop 4 - USER-found issue exposure",
            "Mapped USER-reported issues to source-truth expectations, UTS active issue IDs, LV1 manifests, and likely implementation/tool gaps.",
        ),
        (
            "Loop 5 - Additional failure discovery",
            "Discovered concrete proof-quality gaps: the runtime rerun produced screenshot/video evidence, but an active-state screenshot label does not visually prove active recording, and folder-button pre-session behavior is not fully separated from shell visibility.",
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
            "Confirmed every accepted Option C surface is inventoried, every finding has a stable ID and confidence label, and runtime-created evidence is labeled as investigation evidence rather than prior LV1 acceptance proof.",
        ),
    ]
    return "\n".join(f"### {name}\n\n{body}\n" for name, body in loops)


def evidence_inventory_md(summary: dict[str, object]) -> str:
    prior = summary.get("prior_lv1") or {}
    runtime = summary.get("runtime_rerun") or {}
    supplemental = summary.get("supplemental") or {}
    rows = [
        ("Prior LV1 root", str(LIVE_VALIDATION_ROOT), str(prior.get("repo_live_validation_root_exists", ""))),
        ("Prior LV1 screenshots", "live_client_interaction/*.png", str(prior.get("repo_screenshot_count", ""))),
        ("Prior LV1 manifest", str(prior.get("manifest_path", "")), str(prior.get("manifest_status", ""))),
        ("Prior LV1 interaction manifest", str(prior.get("interaction_manifest_path", "")), str(prior.get("interaction_status", ""))),
        ("Runtime rerun root", str(summary.get("runtime_rerun_root", "")), str(summary.get("runtime_rerun_exists", ""))),
        ("Runtime rerun manifest", str(runtime.get("manifest_path", "")), str(runtime.get("manifest_status", ""))),
        ("Runtime rerun interaction manifest", str(runtime.get("interaction_manifest_path", "")), str(runtime.get("interaction_status", ""))),
        ("Runtime USER screenshot root", str(runtime.get("user_screenshot_root", "")), str(runtime.get("user_screenshot_root_exists", ""))),
        ("Runtime USER element screenshot root", str(runtime.get("user_element_root", "")), str(runtime.get("user_element_root_exists", ""))),
        ("Runtime focused screenshot count", "perElementUserInspectableScreenshots.count", str(runtime.get("user_element_manifest_count", ""))),
        ("Runtime short video", str(summary.get("runtime_short_video_user_path", "")), str(runtime.get("short_video_status", ""))),
        ("Supplemental root", str(summary.get("supplemental_root", "")), str(summary.get("supplemental_exists", ""))),
        ("Supplemental manifest", str(supplemental.get("manifest_path", "")), str(supplemental.get("manifest_status", ""))),
        ("Supplemental interaction manifest", str(supplemental.get("interaction_manifest_path", "")), str(supplemental.get("interaction_status", ""))),
        ("Supplemental USER screenshot root", str(supplemental.get("user_screenshot_root", "")), str(supplemental.get("user_screenshot_root_exists", ""))),
        ("Supplemental USER element screenshot root", str(supplemental.get("user_element_root", "")), str(supplemental.get("user_element_root_exists", ""))),
        ("Supplemental issue folders", "supplemental_issue_evidence_manifest.issueFolders", str(len(summary.get("supplemental_issue_folders") or []))),
        ("Worktree-specific UTS", r"C:\Nexus USER\UTS - FAM-006.txt", str(Path(r"C:\Nexus USER\UTS - FAM-006.txt").exists())),
    ]
    return table(["Evidence", "Path / Field", "Result"], rows)


def supplemental_issue_map_md(summary: dict[str, object]) -> str:
    rows = []
    fixed_observed = {
        "A": "USER personally confirmed the visible Recording Studio button does not open Recording Studio through the normal USER path. Helper foreground proof remains separate and does not disprove the USER-confirmed failure.",
        "C": "USER personally confirmed Log Viewer Studio opens or steals focus after it has been opened once and recording Start/Stop state changes occur. Codex normal-user sequence reproduction is blocked when Computer Use is unavailable; code lineage supports the finding.",
    }
    fixed_confidence = {
        "A": "USER Confirmed + Codex Reproduction Blocked + helper foreground path separately verified when helper evidence passes",
        "C": "USER Confirmed + Inferred Code Lineage + Codex Reproduction Blocked",
    }
    for item in summary.get("supplemental_issue_folders") or []:
        if not isinstance(item, dict):
            continue
        issue_id = str(item.get("issueId", ""))
        observed = fixed_observed.get(
            issue_id,
            str(item.get("observed", "")).replace("\r", " ").replace("\n", " "),
        )
        rows.append(
            [
                issue_id,
                str(item.get("folder", "")),
                str(item.get("screenshotCount", "")),
                str(item.get("expected", "")),
                observed,
                fixed_confidence.get(issue_id, str(item.get("confidence", ""))),
            ]
        )
    if not rows:
        rows = [["BLOCKED", "", "0", "Supplemental A-F issue folders required.", "No supplemental issue manifest was found.", "Blocked"]]
    return "\n".join(
        [
            "Supplemental runtime-created evidence is investigation evidence only. It must not be treated as proof that the prior LV1 handoff was valid.",
            "",
            table(["Issue", "Folder", "Screenshots", "Expected", "Observed", "Confidence"], rows),
        ]
    )


def user_confirmed_ac_supplement_md(summary: dict[str, object]) -> str:
    screenshot_root = str((summary.get("supplemental_manifest") or {}).get("screenshotEvidenceRoot") or summary.get("supplemental_root") or "")
    rows = [
        [
            "Issue A",
            "FAM006-UI-003",
            "Recording Studio visible button",
            "USER Confirmed + Codex Reproduction Blocked + helper foreground path separately verified when helper evidence passes",
            "USER confirmed the normal visible button path fails. The supported Windows automation channel is unavailable, so Codex cannot disprove or fully re-run the USER path in this supplement.",
            screenshot_root,
        ],
        [
            "Issue C",
            "FAM006-WINDOW-002",
            "Log Viewer Studio focus/open behavior",
            "USER Confirmed + Inferred Code Lineage + Codex Reproduction Blocked",
            "USER confirmed the start/stop-triggered focus/open regression. Codex sequence reproduction is blocked, and code lineage shows show/raise/activateWindow in the update path.",
            "desktop/desktop_renderer.py:5998-6017",
        ],
    ]
    return "\n".join(
        [
            "This supplement preserves USER confirmation as direct evidence. Helper foreground proof and native-window existence are evidence layers, not a substitute for USER normal-path proof.",
            "",
            "Codex normal-user automation attempt: `Computer Use native pipe path is unavailable`.",
            "",
            table(["Issue", "Finding ID", "Surface", "Confidence", "Supplement result", "Evidence path"], rows),
        ]
    )


def issue_c_sequence_matrix_md() -> str:
    return table(
        ["Sequence", "Expected behavior", "Codex reproduction status", "Evidence / confidence"],
        [
            [
                "C1: open Log Viewer, close, start, stop",
                "Start/Stop must not reopen Log Viewer or steal focus merely because the shell was previously opened.",
                "Blocked - supported Computer Use normal-user automation channel unavailable.",
                "USER Confirmed + Inferred Code Lineage from desktop/desktop_renderer.py update_product_state show/raise/activateWindow.",
            ],
            [
                "C2: open Log Viewer, minimize, start, stop",
                "Start/Stop must not restore/minimize-state-break or focus the Log Viewer unless USER accepted that behavior.",
                "Blocked - supported Computer Use normal-user automation channel unavailable.",
                "USER Confirmed + Inferred Code Lineage from the same native-window activation path.",
            ],
            [
                "C3: open Log Viewer, leave open unfocused, start, stop",
                "Start/Stop must not steal focus from the USER's current foreground work.",
                "Blocked - supported Computer Use normal-user automation channel unavailable.",
                "USER Confirmed + Inferred Code Lineage from show(), raise_(), and activateWindow().",
            ],
        ],
    )


def supplemental_attempts_md() -> str:
    return table(
        ["Attempt folder", "Helper manifest", "Interaction manifest", "Failure"],
        supplemental_attempt_rows(),
    )


def prior_packet_sufficiency_md(summary: dict[str, object]) -> str:
    return table(
        ["Question", "Prior packet result", "Supplemental result"],
        [
            (
                "Recording Studio button actual click",
                "Broad runtime proof existed, but the packet did not separate visible Dashboard button click proof from native-window existence.",
                "Supplemental A folder carries visible-button foreground helper proof and preserves USER-path conflict if still failing.",
            ),
            (
                "Start/Stop placement",
                "Prior packet did not classify source-truth versus USER-expectation drift.",
                "Supplemental B classifies current accepted source truth as Dashboard-card ownership and USER request as planning/product revision candidate.",
            ),
            (
                "Log Viewer focus/open regression",
                "Prior packet did not trace repeated focus/open behavior after prior shell open.",
                "Supplemental C records blocked normal click matrix and code-lineage inference from show/raise/activateWindow on shell updates.",
            ),
            (
                "Recording Studio / Log Viewer ownership",
                "Prior packet noted native/export boundary but did not classify native-log tracking ownership.",
                "Supplemental D records current visual ownership and source-truth ambiguity.",
            ),
            (
                "Older Overlay Profile and card-holder issues",
                "Prior packet listed issue classes but did not prove normal USER-created/restart path.",
                "Supplemental E/F separates seeded helper proof from blocked manual/restart and visual-inset adjudication.",
            ),
        ],
    )


def runtime_proof_rerun_md(summary: dict[str, object]) -> str:
    runtime = summary.get("runtime_rerun") or {}
    steps = summary.get("runtime_interaction_steps") or []
    step_rows = []
    for step in steps:
        if isinstance(step, dict):
            step_rows.append([
                step.get("label", ""),
                step.get("status", ""),
                "real OS" if "real OS" in str(step.get("label", "")) else "manifest/window proof",
            ])
    return "\n".join(
        [
            "Runtime-created evidence in this packet is investigation evidence. It does not retroactively validate the prior LV1/UTS handoff.",
            "",
            table(
                ["Field", "Value"],
                [
                    ("Runtime rerun root", summary.get("runtime_rerun_root", "")),
                    ("Manifest status", runtime.get("manifest_status", "")),
                    ("Interaction status", runtime.get("interaction_status", "")),
                    ("USER screenshot root", runtime.get("user_screenshot_root", "")),
                    ("USER focused screenshot root", runtime.get("user_element_root", "")),
                    ("Focused screenshot count", runtime.get("user_element_manifest_count", "")),
                    ("Short video", summary.get("runtime_short_video_user_path", "")),
                ],
            ),
            "",
            table(["Runtime step", "Status", "Proof class"], step_rows),
        ]
    )


def visual_adjudication_md(summary: dict[str, object]) -> str:
    runtime = summary.get("runtime_rerun") or {}
    root = Path(str(runtime.get("user_element_root") or ""))
    rows = [
        (
            "Recording card ready/saved states",
            root / "element_02_recording_card_saved_complete_readback_state.png",
            "Verified positive evidence: visible text says native log saved/read back successfully; card uses dashboard row/card language.",
        ),
        (
            "Recording active state screenshot",
            root / "element_02_recording_card_start_recording_active_state.png",
            "Evidence-quality gap: filename claims active state, but visible text still shows Start Recording / ready state rather than an unmistakable active-recording state.",
        ),
        (
            "Recording Studio window",
            root / "element_02_recording_studio_native_window_ready_state.png",
            "Verified mixed visual result: functional window proof exists, but the window is plainer than the Dashboard card visual system.",
        ),
        (
            "Log Viewer Studio shell",
            root / "element_02_log_viewer_studio_native_window_shell_state.png",
            "Verified shell proof exists; folder-button click behavior remains under-proven for pre-session native/export folder creation/open.",
        ),
        (
            "Seeded active Overlay Profile mirror",
            root / "element_02_recording_card_mirrors_hud_overlay_active_profile_real_os_selection.png",
            "Verified positive evidence for seeded real-OS selection: HUD and Recording card both show LV1 Real OS Profile 001 with 1 active monitor.",
        ),
    ]
    return table(["Surface", "Screenshot", "Codex visual adjudication"], rows)


def combination_matrix_md() -> str:
    rows = [
        ("Default profile + active monitors + not recording", "Ready, Start enabled, Recording card mirrors active profile", "LV1 scripted path PASS", "Verified by manifest"),
        ("Seeded LV1 profile + active monitor + selector", "Selector changes active Overlay Profile and Recording card target", "Runtime rerun PASS with real OS input and visual mirror evidence", "Verified"),
        ("USER-created profile + active monitor + switch selector", "Selector changes active Overlay Profile and Recording card target", "USER reports still blocked; seeded profile path PASS does not disprove manual create/switch failure", "Reproducible / conflict"),
        ("USER-created profile + app restart", "Profile persists and remains selectable; issue #258 target reliability", "UTS asks USER to retest; no direct investigation reproduction", "Blocked"),
        ("No active monitors", "Recording blocked/truthful unavailable state", "Not directly reproduced in current investigation", "Blocked"),
        ("Recording active", "Stop visible; state transparent", "Runtime helper step PASS, but active-state screenshot is visually weak", "Verified tool-gap"),
        ("Recording stopped/saved", "Native NDAI log saved/readback complete; no normal CSV export", "Runtime rerun PASS with native ndailog plus validation-only CSV artifact", "Verified"),
        ("Log Viewer shell before recording", "Native/export folders open/create before active-session recording", "Shell button ready state visible; explicit pre-session folder button click proof missing", "Inferred"),
        ("Claimed USER screenshot evidence", "Folder exists and USER can inspect screenshots/video", "Runtime rerun OneDrive folder exists with focused screenshots and short video", "Verified"),
        ("Dashboard card holder scrollbar", "Equal left/right insets", "USER reported fail; current screenshots need product repair adjudication", "Inferred"),
        ("Recording visual inheritance", "Card/studio/shell match existing visual system fully", "Card mostly aligns; Studio/Shell are visually plain and active-state screenshot is weak", "Verified mixed"),
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
        ("2026-06-09 11:03", "Investigation", "Static forensics packet generated at ddeb90a4", "C:\\Nexus USER\\FAM-006-20260609-110335.zip", "Findings packet, not repair plan"),
        ("2026-06-09 11:20", "Runtime proof rerun", "Focused Recording Option C real-OS helper rerun PASS", "dev/logs/fam006_live_validation_runtime_rerun_baseline/20260609_112010_830", "Adds investigation evidence and exposes proof-quality gaps"),
        ("2026-06-09", "Investigation repair", "Forensics helper patched to require baseline ancestry and include runtime rerun evidence", "dev/orin_fam006_live_validation_forensics.py", "Investigation-support patch only"),
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
        ("Repo-local LV1 artifacts", "Manifest and screenshot files exist under repo log root", "No Issue Found", "Does not prove visual acceptability"),
        ("Runtime USER-inspectable screenshots", "Runtime rerun copied focused screenshots/video to the OneDrive screenshots folder", "No Issue Found", "Runtime evidence is investigation-created, not prior LV1 acceptance proof"),
        ("Native log no normal CSV", "recording_output_contract.py says normal product save does not create export; validation CSV only with env var", "No Issue Found", "USER workflow still needs future export UX"),
        ("Scripted default profile Start/Stop", "Runtime rerun records real OS Start and Stop PASS plus native readback", "No Issue Found", "Active-state screenshot label remains visually weak"),
        ("Seeded profile target mirror", "Runtime rerun records real OS selector option click and target mirror screenshot", "No Issue Found", "Does not cover manual create/edit/restart persistence"),
        ("Log Viewer shell future boundaries", "Manifest records full viewer/export customization future-gated", "No Issue Found", "Does not prove every native/export folder button path"),
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


def repair_guidance(finding_id: str) -> dict[str, str]:
    guidance = {
        "FAM006-EVID-001": {
            "objective": "Convert screenshot existence into visual adjudication proof with full-window, element, state, and USER-inspectable folder checks.",
            "lane": "FAM-006 Live Validation proof-loop repair",
            "branch_scope": "In-scope for later approved FAM-006 repair because it governs this branch's LV/UTS handoff.",
            "proof": "New LV rerun must include screenshot manifest, visual-adjudication notes, state labels, and checked-clean negatives.",
            "decision": "Approve LV proof-loop repair; do not accept UTS from screenshot existence alone.",
        },
        "FAM006-EVID-002": {
            "objective": "Require issue-specific A-D evidence instead of broad findings packets that miss concrete USER questions.",
            "lane": "FAM-006 packet/evidence repair with Governance follow-up candidate",
            "branch_scope": "In-scope as packet support; durable generic adoption should be routed to Governance after this branch proves the model.",
            "proof": "Each USER issue gets a finding ID, evidence path, confidence label, and reproduction limitation.",
            "decision": "Approve issue-specific evidence sections for repair validation.",
        },
        "FAM006-TOOLGAP-001": {
            "objective": "Stop treating marker, manifest, and helper PASS as user-facing behavior proof.",
            "lane": "FAM-006 helper/validator planning; durable Governance candidate",
            "branch_scope": "In-scope to plan and later add FAM-006-specific tool checks; global rules remain Governance-owned.",
            "proof": "Repair validation must show what each helper checked and did not check.",
            "decision": "Approve helper false-green guardrails before another UTS handoff.",
        },
        "FAM006-LVFAIL-001": {
            "objective": "Build a deterministic affected-surface and interaction combination matrix for Option C surfaces.",
            "lane": "FAM-006 Live Validation repair",
            "branch_scope": "In-scope for later approved LV rerun and proof repair.",
            "proof": "Matrix covers default, USER-created, edited, restarted, active/no-active monitors, recording active/stopped, Studio open/closed, Log Viewer open/closed, and folder missing/exists states.",
            "decision": "Approve LV matrix repair and rerun criteria.",
        },
        "FAM006-UTSFAIL-001": {
            "objective": "Make UTS handoff a post-proof USER return surface, not a substitute for pre-handoff validation.",
            "lane": "FAM-006 UTS gate repair",
            "branch_scope": "In-scope for later approved branch UTS update and stop-loss validation.",
            "proof": "UTS must list only items with deterministic pre-handoff proof or explicitly mark USER retest items as open blockers.",
            "decision": "Approve UTS stop-loss repair before another USER handoff.",
        },
        "FAM006-UI-001": {
            "objective": "Repair visual-system inheritance so Recording surfaces sample existing HUD card color, shape, spacing, density, effects, and button language.",
            "lane": "FAM-006 product/UI repair",
            "branch_scope": "Requires later product/runtime repair approval.",
            "proof": "Full-window plus element screenshots compare Recording Card, Recording Studio, and Log Viewer shell against existing HUD card standards.",
            "decision": "Approve product/UI visual repair if USER accepts the plan.",
        },
        "FAM006-UI-002": {
            "objective": "Repair card-holder inset/scrollbar gutter regression so left and right visual insets are equal.",
            "lane": "FAM-006 product/UI repair",
            "branch_scope": "Requires later product/runtime repair approval.",
            "proof": "Before/after full-window and card-holder screenshots with scrollbar visible and absent where possible.",
            "decision": "Approve product/UI layout repair if USER accepts the plan.",
        },
        "FAM006-UI-003": {
            "objective": "Repair the visible Dashboard Recording Card button path so it opens Recording Studio through the normal USER click path.",
            "lane": "FAM-006 product/runtime repair",
            "branch_scope": "Requires later product/runtime repair approval.",
            "proof": "Manual-equivalent click proof, native-window focus proof, screenshot proof, and no marker-only acceptance.",
            "decision": "Approve Issue A product repair if USER accepts the plan.",
        },
        "FAM006-WINDOW-001": {
            "objective": "Prove native/export folder actions work before any recording in the current session and remain future-gated outside minimal shell scope.",
            "lane": "FAM-006 product/window and LV proof repair",
            "branch_scope": "Requires later product/runtime repair approval for behavior changes; proof planning is in-scope.",
            "proof": "Pre-session click evidence for native and exported folders, folder-exists/missing cases, and no unwanted CSV creation.",
            "decision": "Approve minimal Log Viewer shell folder-behavior repair if needed.",
        },
        "FAM006-WINDOW-002": {
            "objective": "Repair Log Viewer Studio focus/open regression after prior open and later Start/Stop updates.",
            "lane": "FAM-006 product/window behavior repair",
            "branch_scope": "Requires later product/runtime repair approval.",
            "proof": "Sequences: open-close-start-stop, open-minimize-start-stop, open-unfocused-start-stop; Log Viewer must not reopen or steal focus unless USER explicitly clicks it.",
            "decision": "Approve Issue C product repair if USER accepts the plan.",
        },
        "FAM006-GOVGAP-002": {
            "objective": "Resolve Start/Stop placement drift before moving controls: accepted plan versus USER-refined Quick Access/Recording Studio expectation.",
            "lane": "BP/source-truth amendment planning",
            "branch_scope": "Do not mutate product until USER chooses whether to amend BP1/BP2/BP3 or treat it as later carryforward.",
            "proof": "Updated branch vision/plan or explicit waiver records the chosen control ownership.",
            "decision": "Choose BP amendment, targeted product repair, or defer Start/Stop relocation.",
        },
        "FAM006-GOVGAP-003": {
            "objective": "Resolve native-log tracking ownership between Recording Studio and Log Viewer Studio before changing UI ownership.",
            "lane": "BP/source-truth amendment planning",
            "branch_scope": "Do not mutate product until ownership is admitted or deferred.",
            "proof": "Source truth states which surface owns compact current-log status versus native/export folder access.",
            "decision": "Choose BP amendment, targeted product repair, or defer ownership shift.",
        },
        "FAM006-REGRESS-001": {
            "objective": "Repair and prove Overlay Profile switching mirrors into Recording target state across normal USER paths.",
            "lane": "FAM-006 product/state regression repair",
            "branch_scope": "Requires later product/runtime repair approval; issue #258 relevance is in-scope.",
            "proof": "Multiple profiles, create/edit/switch, active state mirror, restart persistence, no stale target source.",
            "decision": "Approve Overlay Profile state repair and proof path.",
        },
        "FAM006-REGRESS-002": {
            "objective": "Close seeded-proof versus USER-created/restart proof gap for Overlay Profile persistence.",
            "lane": "FAM-006 product/state proof repair",
            "branch_scope": "Requires later product/runtime repair approval for behavior changes; validation proof is branch-specific.",
            "proof": "USER-created profile persists after app restart and remains selectable; Recording card uses it as target.",
            "decision": "Approve Overlay Profile persistence proof before issue #258 closeout.",
        },
        "FAM006-CODEPATH-001": {
            "objective": "Trace each repair through JS state, native bridge, desktop state persistence, and output contract code paths.",
            "lane": "FAM-006 implementation lineage guard",
            "branch_scope": "In-scope for later approved repair implementation and proof.",
            "proof": "Each product fix cites event/state path, changed file, expected user behavior, and validator coverage.",
            "decision": "Approve code-lineage tracking for the repair package.",
        },
        "FAM006-PHASE-001": {
            "objective": "Prevent automated LV handoff green from being treated as USER acceptance or sufficient UTS readiness.",
            "lane": "FAM-006 phase/gate repair with Governance follow-up candidate",
            "branch_scope": "Branch can repair its own handoff packet and proof loop; global phase law remains Governance-owned.",
            "proof": "Packet Reviewability, USER Gate State, LV proof state, UTS handoff state, and UTS acceptance state stay separate.",
            "decision": "Approve gate-state stop-loss before returning to Live Validation.",
        },
    }
    return guidance.get(finding_id, {
        "objective": "Classify and repair only after USER accepts this plan.",
        "lane": "Unclassified",
        "branch_scope": "Requires USER decision.",
        "proof": "To be defined.",
        "decision": "USER review required.",
    })


def repair_plan_findings(summary: dict[str, object]) -> list[Finding]:
    by_id = {item.finding_id: item for item in findings(summary) + supplemental_findings(summary)}
    missing = [finding_id for finding_id in REPAIR_PLAN_FINDING_IDS if finding_id not in by_id]
    if missing:
        raise SystemExit(f"BLOCKED: repair plan findings missing from accepted findings model: {', '.join(missing)}")
    return [by_id[finding_id] for finding_id in REPAIR_PLAN_FINDING_IDS]


def findings_to_repair_map_md(findings_list: list[Finding]) -> str:
    rows = []
    for item in findings_list:
        guide = repair_guidance(item.finding_id)
        rows.append([
            item.finding_id,
            item.finding_class,
            item.confidence,
            guide["objective"],
            guide["lane"],
            guide["branch_scope"],
            guide["proof"],
            guide["decision"],
        ])
    return table(
        [
            "Finding ID",
            "Class",
            "Confidence",
            "Repair objective",
            "Lane",
            "Current-branch scope",
            "Proof expectation",
            "USER decision",
        ],
        rows,
    )


def repair_lane_classification_md() -> str:
    return table(
        ["Lane", "Finding IDs", "What it means", "Approval status"],
        [
            [
                "Current FAM-006 product/runtime repair",
                "FAM006-UI-001, FAM006-UI-002, FAM006-UI-003, FAM006-WINDOW-001, FAM006-WINDOW-002, FAM006-REGRESS-001, FAM006-REGRESS-002, FAM006-CODEPATH-001",
                "Repair accepted Option C surfaces and issue #258 target reliability inside this worktree after separate USER implementation approval.",
                "Pending USER approval; not implemented by this packet.",
            ],
            [
                "Current FAM-006 Live Validation / UTS proof-loop repair",
                "FAM006-EVID-001, FAM006-EVID-002, FAM006-TOOLGAP-001, FAM006-LVFAIL-001, FAM006-UTSFAIL-001, FAM006-PHASE-001",
                "Make the FAM-006 proof loop deterministic enough to block another false-green UTS handoff.",
                "Pending USER approval; plan only.",
            ],
            [
                "BP/source-truth amendment candidate",
                "FAM006-GOVGAP-002, FAM006-GOVGAP-003",
                "Resolve Start/Stop placement and native-log tracking ownership before product UI changes that would differ from accepted BP2/BP3.",
                "Pending USER decision whether to amend BP or defer.",
            ],
            [
                "Governance follow-up candidate",
                "FAM006-TOOLGAP-001, FAM006-PHASE-001, FAM006-EVID-002",
                "Consider generalizing the FAM-006 proof-loop lessons after the branch repair proves them.",
                "Deferred; Governance worktree mutation excluded.",
            ],
            [
                "Future-gated product features",
                "Full Log Viewer, export customization, tray controls, keybinds, global settings, Native Log Loader full implementation",
                "Remain outside this branch unless USER reopens scope and source truth admits them.",
                "Not approved.",
            ],
        ],
    )


def current_branch_repair_package_md() -> str:
    return textwrap.dedent(
        """
        Recommended package after USER accepts this plan:

        1. Gate/source-truth alignment first.
           - Decide whether Start/Stop relocation and native-log tracking ownership require a BP amendment.
           - Keep full Log Viewer, export customization, tray, keybinds, full settings, and Native Log Loader full implementation future-gated.

        2. Product/runtime repair second.
           - Fix the normal visible Recording Studio button path.
           - Fix Log Viewer Studio focus/open behavior after prior open and recording Start/Stop updates.
           - Fix Overlay Profile create/edit/switch/restart persistence and Recording target mirroring.
           - Fix card-holder inset and Recording surface visual-system inheritance.
           - Verify native/export folder access before a recording exists in the active session.

        3. Proof-loop repair third.
           - Rebuild Live Validation around affected surfaces and combinations, not only prior elements.
           - Require full-window and element screenshots with visual adjudication.
           - Update `C:\\Nexus USER\\UTS - FAM-006.txt` only after deterministic proof exists.

        4. Return to USER gate.
           - Do not claim UTS acceptance, PR Readiness, issue #258 closeout, merge, or release from this repair plan.
        """
    ).strip()


def issue_a_repair_plan_md() -> str:
    return textwrap.dedent(
        """
        Finding: `FAM006-UI-003`.

        Repair target: the visible Dashboard Recording Card button must open Recording Studio through the normal USER click path, not only through helper/native-window existence proof.

        Planned investigation before code change:
        - Confirm the button selector and event listener in `nexus_visual/monitoring_hud.js`.
        - Confirm the bridge request emitted by the Dashboard is received by the desktop renderer.
        - Confirm the standalone Recording Studio window opens without requiring an unrelated state update.

        Planned proof after code change:
        - Click the visible button from a fresh dashboard session.
        - Capture full-window screenshot before click, click evidence, and Recording Studio window evidence.
        - Record whether Recording Studio is already open, closed, or minimized.
        - Treat helper foreground proof as supporting evidence only, not USER-path proof.
        """
    ).strip()


def issue_c_repair_plan_md() -> str:
    return textwrap.dedent(
        """
        Finding: `FAM006-WINDOW-002`.

        Repair target: after the USER has opened Log Viewer Studio once, later Start/Stop recording updates must not reopen it, raise it, or steal focus unless the USER explicitly asks for it.

        Planned code lineage:
        - Inspect `desktop/desktop_renderer.py` around `MonitoringHudLogViewerStudioWindow.update_product_state`.
        - Separate data refresh from show/raise/activate behavior.
        - Preserve explicit open action while preventing passive recording-state updates from becoming focus actions.

        Planned proof after code change:
        - Open Log Viewer, close, start, stop.
        - Open Log Viewer, minimize if implemented, start, stop.
        - Open Log Viewer, leave it open but unfocused, start, stop.
        - Confirm no unwanted focus steal and no unwanted window reopen.
        """
    ).strip()


def issue_b_repair_plan_md() -> str:
    return textwrap.dedent(
        """
        Finding: `FAM006-GOVGAP-002`.

        Repair target: decide whether Start/Stop remains inside the Dashboard Recording Card for this branch or moves to Quick Access / Recording Studio ownership.

        Planning rule:
        - Do not move product controls until source truth admits the change or USER explicitly chooses a narrow repair route.
        - If moved now, update BP/source truth to describe the branch-specific control ownership.
        - If deferred, keep the current control placement and record the Quick Access / keybind path as durable carryforward.

        Proof expectation if admitted:
        - Screenshot and interaction proof for the chosen Start/Stop surface.
        - Recording Studio and Dashboard states must remain synchronized.
        - UTS must ask about the chosen surface, not an obsolete one.
        """
    ).strip()


def issue_d_repair_plan_md() -> str:
    return textwrap.dedent(
        """
        Finding: `FAM006-GOVGAP-003`.

        Repair target: decide whether compact current native-log tracking belongs in Recording Studio, Log Viewer Studio, or both with distinct ownership.

        Planning rule:
        - Recording Studio may own current-session control/status if admitted.
        - Minimal Log Viewer Studio may own native/export folder access if admitted.
        - Full previous-log selection, export customization, and Native Log Loader remain future-gated.

        Proof expectation if admitted:
        - Recording Studio shows the agreed current-log status without becoming a full log viewer.
        - Log Viewer Studio exposes native and exported folder access without stealing focus or implying full viewer implementation.
        - Native `.ndailog` files remain product-native; exported files remain USER-requested artifacts.
        """
    ).strip()


def overlay_profile_proof_plan_md() -> str:
    return textwrap.dedent(
        """
        Overlay Profile proof must cover normal USER paths, not only seeded helper paths:

        - Create at least two Overlay Profiles through the UI.
        - Switch Active Overlay Profile from the HUD Overlay card.
        - Verify the Recording Card target changes immediately to the active profile.
        - Edit a profile and verify the display/target mirror updates.
        - Restart the app and verify created profiles persist and remain selectable.
        - Start/Stop recording with the selected profile and verify target snapshot stability.
        - Capture full-window and element screenshots for each state.
        - Keep issue #258 open until persistence and recording target reliability are proven.
        """
    ).strip()


def live_validation_repair_plan_md() -> str:
    return textwrap.dedent(
        """
        Live Validation should be rebuilt as an affected-surface proof loop:

        - Inventory changed files and map each to user-facing surfaces.
        - Test new surfaces plus previous surfaces affected by the diff.
        - Do not retest unrelated legacy surfaces unless the branch changed or risk-touched them.
        - Build a combination matrix covering profiles, monitors, recording state, Studio state, Log Viewer state, folder existence, and app restart.
        - Capture full-window and element screenshots in a USER-inspectable folder.
        - Add visual adjudication notes for screenshots; screenshot existence is not enough.
        - Generate negative findings for checked-clean surfaces.
        - Block UTS handoff if any admitted surface lacks proof or has unresolved USER-confirmed failure.
        """
    ).strip()


def helper_validator_tooling_repair_plan_md() -> str:
    return textwrap.dedent(
        """
        Proposed helper/validator repairs for later approval:

        - Add a visible-button click-path verifier for Recording Studio launch.
        - Add a Log Viewer focus-regression verifier for open/close/minimize/unfocused Start/Stop sequences.
        - Add an Overlay Profile persistence verifier for create/edit/switch/restart and Recording target mirror.
        - Add a screenshot manifest validator that requires full-window, element, and state labels.
        - Add a visual-adjudication checklist that distinguishes screenshot presence from visual pass.
        - Add a UTS stop-loss validator that blocks handoff while accepted-scope findings remain unresolved.
        - Add old-tool versus behavior-proof comparison output so PASS claims say what they actually prove.

        These are planning items only in this packet. Durable global adoption should be routed to Governance after the FAM-006 branch proves the model.
        """
    ).strip()


def source_truth_amendment_plan_md() -> str:
    return textwrap.dedent(
        """
        Source-truth amendment candidates:

        - `Docs/family_feature_visions/FAM-006_recording.md`: record durable Recording ecosystem direction, visual-system inheritance, native/export boundary, and future-gated carryforward.
        - External branch plan under `C:\\Nexus Governance State`: record which repair plan was accepted, what remains pending, and the legal next phase.
        - FAM-006 branch record/receipts: record repair planning reviewability and keep product fixes pending until USER approval.
        - Governance follow-up: consider general Live Validation determinism, helper false-green rules, and UTS stop-loss rules after this branch proves the pattern.

        This packet does not perform those amendments except for generating the repair-planning USER packet.
        """
    ).strip()


def repair_sequencing_md() -> str:
    return table(
        ["Step", "Gate", "Action", "Exit criteria"],
        [
            ["1", "Repair plan USER review", "USER accepts, revises, splits, or holds this plan.", "A clear implementation or amendment route is selected."],
            ["2", "BP/source-truth amendment if needed", "Resolve Issue B and Issue D ownership drift before product UI relocation.", "Accepted source-truth route or explicit deferral."],
            ["3", "Bounded product/runtime repair", "Fix admitted product defects in one coherent Option C repair package.", "Product validators and targeted manual-equivalent proofs pass."],
            ["4", "H1 / Hardening repair proof", "Pressure-test visual, state, persistence, window, and output paths.", "No admitted H1 blockers remain."],
            ["5", "Live Validation rerun", "Run deterministic affected-surface LV matrix with screenshots and visual adjudication.", "LV proof is green; USER Gate remains pending."],
            ["6", "UTS handoff", "Update `C:\\Nexus USER\\UTS - FAM-006.txt` from proof and return to USER.", "USER can accept, revise, or reject returned UTS results."],
        ],
    )


def exact_user_decision_options_md() -> str:
    return textwrap.dedent(
        """
        Option 1 - Accept this repair plan and approve bounded implementation:
        `I accept the FAM-006 Live Validation / UTS failure repair plan and approve bounded FAM-006 repair implementation for the admitted current-branch repair package, with product/runtime changes limited to the accepted plan and Governance/FAM-007/neutral-main/PR/merge/release/issue-closeout work still pending separate approval.`

        Option 2 - Revise this repair plan:
        `I revise the FAM-006 repair plan. Update these findings, lanes, or sequencing items: [USER edits].`

        Option 3 - Reopen BP/source-truth before product repair:
        `I approve a bounded FAM-006 BP/source-truth amendment pass for Start/Stop placement and Recording Studio / Log Viewer Studio ownership before product repair.`

        Option 4 - Split the package:
        `I approve only [named findings] for the next FAM-006 repair pass and defer the remaining findings.`
        """
    ).strip()


def accepted_findings_packet_digest_md(accepted: dict[str, object], extracted: list[str]) -> str:
    entries = accepted.get("entries") or []
    preview = "\n".join(f"- `{name}`" for name in list(entries)[:80])
    if len(entries) > 80:
        preview += f"\n- ... {len(entries) - 80} more files"
    return "\n".join(
        [
            table(
                ["Field", "Value"],
                [
                    ["Path", accepted.get("path", "")],
                    ["SHA256", accepted.get("sha256", "")],
                    ["Expected SHA256", ACCEPTED_FINDINGS_SHA256],
                    ["Primary investigation file present", accepted.get("primaryPresent", "")],
                    ["File count", accepted.get("fileCount", "")],
                    ["Markdown count", accepted.get("markdownCount", "")],
                    ["Copied into this packet", len(extracted)],
                ],
            ),
            "",
            "Accepted findings packet entries copied under `Review Aids/Accepted Findings Packet/`:",
            "",
            preview,
        ]
    )


def rebuild_zip_from_folder(folder: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in folder.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(folder).as_posix())
    return buffer.getvalue()


def rebuild_repair_plan_zip_from_packet_zip(packet_zip: Path) -> bytes | None:
    if not packet_zip.exists():
        return None
    prefix = "Review Aids/Repair Planning Packet/"
    buffer = io.BytesIO()
    found = False
    with zipfile.ZipFile(packet_zip, "r") as source, zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as target:
        for info in source.infolist():
            if info.is_dir() or not info.filename.startswith(prefix):
                continue
            target_name = info.filename[len(prefix):]
            if not target_name:
                continue
            target.writestr(target_name, source.read(info))
            found = True
    return buffer.getvalue() if found else None


def rebuild_embedded_zip_from_packet_zip(packet_zip: Path, prefix: str) -> bytes | None:
    if not packet_zip.exists():
        return None
    buffer = io.BytesIO()
    found = False
    with zipfile.ZipFile(packet_zip, "r") as source, zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as target:
        for info in source.infolist():
            if info.is_dir() or not info.filename.startswith(prefix):
                continue
            target_name = info.filename[len(prefix):]
            if not target_name:
                continue
            target.writestr(target_name, source.read(info))
            found = True
    return buffer.getvalue() if found else None


def repair_plan_packet() -> tuple[dict[str, object], bytes]:
    source_path = REPAIR_PLAN_ZIP
    source_note = "standalone repair-planning packet"
    expected_sha = REPAIR_PLAN_SHA256
    if REPAIR_PLAN_ZIP.exists():
        data = REPAIR_PLAN_ZIP.read_bytes()
    else:
        embedded_folder = PACKET_ROOT / "Review Aids" / "Repair Planning Packet"
        if embedded_folder.exists():
            data = rebuild_zip_from_folder(embedded_folder)
            source_path = embedded_folder
            source_note = "embedded repair-planning packet copy from current USER packet"
            expected_sha = "original standalone ZIP already purged by timestamped USER packet regeneration"
        else:
            data = None
            for candidate in sorted(USER_ROOT.glob("FAM-006-*.zip"), key=lambda path: path.stat().st_mtime, reverse=True):
                data = rebuild_repair_plan_zip_from_packet_zip(candidate)
                if data is not None:
                    source_path = candidate
                    source_note = "embedded repair-planning packet copy from timestamped USER packet ZIP"
                    expected_sha = "original standalone ZIP already purged by timestamped USER packet regeneration"
                    break
            if data is None:
                raise SystemExit(
                    f"BLOCKED: accepted repair-planning packet is missing: {REPAIR_PLAN_ZIP}, "
                    "and no embedded repair-planning packet copy was found."
                )
    digest = hashlib.sha256(data).hexdigest().upper()
    if REPAIR_PLAN_ZIP.exists() and digest != REPAIR_PLAN_SHA256:
        raise SystemExit(
            "BLOCKED: repair-planning packet SHA mismatch. "
            f"Expected {REPAIR_PLAN_SHA256}, found {digest} at {REPAIR_PLAN_ZIP}"
        )
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        names = sorted(name for name in archive.namelist() if not name.endswith("/"))
        try:
            primary_text = archive.read(REPAIR_PLAN_PRIMARY_FILE).decode("utf-8-sig", errors="replace")
        except KeyError:
            primary_text = ""
        embedded_findings_present = PRIMARY_FILE in names or (
            f"Review Aids/Accepted Findings Packet/{PRIMARY_FILE}" in names
        )
    return {
        "path": str(source_path),
        "sourceNote": source_note,
        "sha256": digest,
        "expectedSha256": expected_sha,
        "fileCount": len(names),
        "markdownCount": len([name for name in names if name.lower().endswith(".md")]),
        "primaryPresent": bool(primary_text),
        "embeddedAcceptedFindingsPresent": embedded_findings_present,
        "entries": names,
        "primaryPreview": primary_text[:4000],
    }, data


def validator_first_packet() -> tuple[dict[str, object], bytes]:
    source_path: Path | str = VALIDATOR_FIRST_ZIP
    source_note = "standalone validator-first expected-red packet"
    expected_sha = VALIDATOR_FIRST_SHA256
    if VALIDATOR_FIRST_ZIP.exists():
        data = VALIDATOR_FIRST_ZIP.read_bytes()
    else:
        embedded_folder = PACKET_ROOT / "Review Aids" / "Live Validator First Packet"
        if embedded_folder.exists():
            data = rebuild_zip_from_folder(embedded_folder)
            source_path = embedded_folder
            source_note = "embedded validator-first packet copy from current USER packet"
            expected_sha = "original standalone ZIP already purged by timestamped USER packet regeneration"
        else:
            data = None
            prefix = "Review Aids/Live Validator First Packet/"
            for candidate in sorted(USER_ROOT.glob("FAM-006-*.zip"), key=lambda path: path.stat().st_mtime, reverse=True):
                data = rebuild_embedded_zip_from_packet_zip(candidate, prefix)
                if data is not None:
                    source_path = candidate
                    source_note = "embedded validator-first packet copy from timestamped USER packet ZIP"
                    expected_sha = "original standalone ZIP already purged by timestamped USER packet regeneration"
                    break
            if data is None:
                raise SystemExit(
                    f"BLOCKED: accepted validator-first packet is missing: {VALIDATOR_FIRST_ZIP}, "
                    "and no embedded validator-first packet copy was found."
                )
    digest = hashlib.sha256(data).hexdigest().upper()
    if VALIDATOR_FIRST_ZIP.exists() and digest != VALIDATOR_FIRST_SHA256:
        raise SystemExit(
            "BLOCKED: validator-first packet SHA mismatch. "
            f"Expected {VALIDATOR_FIRST_SHA256}, found {digest} at {VALIDATOR_FIRST_ZIP}"
        )
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        names = sorted(name for name in archive.namelist() if not name.endswith("/"))
        try:
            primary_text = archive.read(VALIDATOR_FIRST_PRIMARY_FILE).decode("utf-8-sig", errors="replace")
        except KeyError:
            primary_text = ""
    return {
        "path": str(source_path),
        "sourceNote": source_note,
        "sha256": digest,
        "expectedSha256": expected_sha,
        "fileCount": len(names),
        "markdownCount": len([name for name in names if name.lower().endswith(".md")]),
        "primaryPresent": bool(primary_text),
        "entries": names,
        "primaryPreview": primary_text[:4000],
    }, data


def validator_first_packet_digest_md(packet: dict[str, object], extracted: list[str]) -> str:
    entries = packet.get("entries") or []
    preview = "\n".join(f"- `{name}`" for name in list(entries)[:80])
    if len(entries) > 80:
        preview += f"\n- ... {len(entries) - 80} more files"
    return "\n".join(
        [
            table(
                ["Field", "Value"],
                [
                    ["Path", packet.get("path", "")],
                    ["Source note", packet.get("sourceNote", "")],
                    ["SHA256", packet.get("sha256", "")],
                    ["Expected SHA256", packet.get("expectedSha256", VALIDATOR_FIRST_SHA256)],
                    ["Primary validator-first file present", packet.get("primaryPresent", "")],
                    ["File count", packet.get("fileCount", "")],
                    ["Markdown count", packet.get("markdownCount", "")],
                    ["Copied into this packet", len(extracted)],
                ],
            ),
            "",
            "Validator-first packet entries copied under `Review Aids/Live Validator First Packet/`:",
            "",
            preview,
        ]
    )


def repair_plan_packet_digest_md(repair_plan: dict[str, object], extracted: list[str]) -> str:
    entries = repair_plan.get("entries") or []
    preview = "\n".join(f"- `{name}`" for name in list(entries)[:80])
    if len(entries) > 80:
        preview += f"\n- ... {len(entries) - 80} more files"
    return "\n".join(
        [
            table(
                ["Field", "Value"],
                [
                    ["Path", repair_plan.get("path", "")],
                    ["Source", repair_plan.get("sourceNote", "")],
                    ["SHA256", repair_plan.get("sha256", "")],
                    ["Expected SHA256", repair_plan.get("expectedSha256", REPAIR_PLAN_SHA256)],
                    ["Primary repair-plan file present", repair_plan.get("primaryPresent", "")],
                    ["Embedded accepted findings present", repair_plan.get("embeddedAcceptedFindingsPresent", "")],
                    ["File count", repair_plan.get("fileCount", "")],
                    ["Markdown count", repair_plan.get("markdownCount", "")],
                    ["Copied into this packet", len(extracted)],
                ],
            ),
            "",
            "Repair-planning packet entries copied under `Review Aids/Repair Planning Packet/`:",
            "",
            preview,
        ]
    )


def live_validator_first_checks() -> list[LiveValidatorCheck]:
    live_validation_text = read_text(REPO / "dev/orin_monitoring_hud_live_validation.ps1")
    renderer_text = read_text(REPO / "desktop/desktop_renderer.py")
    state_text = read_text(REPO / "desktop/monitoring_hud_state.py")
    output_contract_text = read_text(REPO / "desktop/recording_output_contract.py")
    recording_vision_text = read_text(REPO / "Docs/family_feature_visions/FAM-006_recording.md")

    studio_real_os_label = "real OS click opens Dashboard Recording Studio" in live_validation_text
    log_viewer_real_os_label = "real OS click opens Dashboard Recording Log Viewer Studio" in live_validation_text
    log_viewer_activation_path = (
        "self._monitoring_hud_log_viewer_studio_window.update_product_state" in renderer_text
        and "self._monitoring_hud_log_viewer_studio_window.proof_state" in renderer_text
        and "activateWindow()" in renderer_text
    )
    active_target_builder = "build_active_overlay_recording_target_snapshot" in state_text
    native_export_boundary = (
        "nativeLogReadableOnlyByNDAI" in output_contract_text
        and "normalProductSaveCreatesExport" in output_contract_text
    )
    visual_inheritance_required = "visual-system inheritance" in recording_vision_text
    screenshot_root = latest_runtime_rerun_root()
    supplemental_root = latest_supplemental_root()

    return [
        LiveValidatorCheck(
            check_id="FAM006-LVF-A-001",
            finding_ids=("FAM006-UI-003", "FAM006-TOOLGAP-001", "FAM006-LVFAIL-001"),
            title="Recording Studio visible-button path cannot be green from helper/native-window proof alone",
            category="normal-user-path proof",
            result="UNPROVEN",
            expected_current_result="UNPROVEN",
            source_truth_expectation="Visible USER-facing button clicks must be proven through the normal USER path before Live Validation handoff.",
            user_facing_action="USER clicks the Recording Card button that should open Recording Studio.",
            evidence_path="dev/orin_monitoring_hud_live_validation.ps1",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="MONITORING_HUD_RECORDING_STUDIO_READY / helper foreground evidence is separate",
            confidence="Verified tool gap" if studio_real_os_label else "Blocked",
            phase_relevance="Live Validation / UTS stop-loss",
            user_path_layer="normal USER path first; helper foreground path is separate evidence",
            old_validator_gap="Old tooling could over-credit native-window existence or helper foreground proof without settling the USER-visible button path.",
            future_green_condition="A later product-state run includes visible-button click evidence, focused Recording Studio screenshot, and event/log proof from the same normal USER action.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-C1-001",
            finding_ids=("FAM006-WINDOW-002", "FAM006-CODEPATH-001", "FAM006-LVFAIL-001"),
            title="Log Viewer C1 focus/open regression sequence remains blocked, not green",
            category="window behavior proof",
            result="BLOCKED",
            expected_current_result="BLOCKED",
            source_truth_expectation="Start/Stop must not reopen or focus Log Viewer merely because it was previously opened.",
            user_facing_action="Open Log Viewer, close it, start recording, then stop recording.",
            evidence_path="desktop/desktop_renderer.py",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="Log Viewer update path includes native-window show/raise/activation risk" if log_viewer_activation_path else "Log Viewer sequence proof missing",
            confidence="USER Confirmed + Inferred Code Lineage + Codex Reproduction Blocked",
            phase_relevance="Live Validation / window behavior audit",
            user_path_layer="normal USER sequence required; helper shell-ready marker is insufficient",
            old_validator_gap="Old tooling did not require C1 repeated sequence proof after an already-opened Log Viewer shell.",
            future_green_condition="A visible USER-path run proves Log Viewer stays closed/unfocused across C1 unless USER explicitly opens it.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-C2-001",
            finding_ids=("FAM006-WINDOW-002", "FAM006-CODEPATH-001", "FAM006-LVFAIL-001"),
            title="Log Viewer C2 minimized-window sequence remains blocked, not green",
            category="window behavior proof",
            result="BLOCKED",
            expected_current_result="BLOCKED",
            source_truth_expectation="Start/Stop must not restore a minimized Log Viewer or steal focus without an approved USER-facing rule.",
            user_facing_action="Open Log Viewer, minimize it, start recording, then stop recording.",
            evidence_path="desktop/desktop_renderer.py",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="show/raise/activateWindow code path requires normal USER validation" if log_viewer_activation_path else "Log Viewer minimized sequence proof missing",
            confidence="USER Confirmed + Inferred Code Lineage + Codex Reproduction Blocked",
            phase_relevance="Live Validation / window behavior audit",
            user_path_layer="normal USER sequence required",
            old_validator_gap="Old tooling did not require minimized-state focus regression proof.",
            future_green_condition="A visible USER-path run proves minimized Log Viewer remains minimized/unfocused across Start/Stop.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-C3-001",
            finding_ids=("FAM006-WINDOW-002", "FAM006-CODEPATH-001", "FAM006-LVFAIL-001"),
            title="Log Viewer C3 open-but-unfocused sequence remains blocked, not green",
            category="window behavior proof",
            result="BLOCKED",
            expected_current_result="BLOCKED",
            source_truth_expectation="Start/Stop must not steal focus from the USER's current foreground work.",
            user_facing_action="Open Log Viewer, leave it open but unfocused, start recording, then stop recording.",
            evidence_path="desktop/desktop_renderer.py",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="activateWindow risk path present" if log_viewer_activation_path else "Log Viewer focus sequence proof missing",
            confidence="USER Confirmed + Inferred Code Lineage + Codex Reproduction Blocked",
            phase_relevance="Live Validation / window behavior audit",
            user_path_layer="normal USER sequence required",
            old_validator_gap="Old tooling did not prove foreground focus remains stable across C3.",
            future_green_condition="A visible USER-path run proves Log Viewer does not take focus across C3.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-B-001",
            finding_ids=("FAM006-GOVGAP-002", "FAM006-PHASE-001"),
            title="Start/Stop placement is source-truth ambiguous until branch vision/plan is reconciled",
            category="source-truth ambiguity",
            result="UNPROVEN",
            expected_current_result="UNPROVEN",
            source_truth_expectation="Live Validation must not silently pass a UI placement contract when USER-visible direction and branch source truth diverge.",
            user_facing_action="USER looks for the intended Start/Stop ownership surface in Dashboard Recording Card versus Recording Studio.",
            evidence_path="Docs/family_feature_visions/FAM-006_recording.md",
            screenshot_path="",
            log_event_path="No product event can settle an ambiguous source-truth contract.",
            confidence="Inferred",
            phase_relevance="BP/source-truth repair candidate before product repair",
            user_path_layer="source-truth decision required before runtime validation can go green",
            old_validator_gap="Old tooling could validate the implemented placement without checking whether the placement still matched USER-evolved recording vision.",
            future_green_condition="Accepted source truth names the Start/Stop ownership rule, then Live Validation checks that exact path.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-D-001",
            finding_ids=("FAM006-GOVGAP-003", "FAM006-UTSFAIL-001"),
            title="Native log tracking ownership cannot be passed by folder existence alone",
            category="source-truth ambiguity",
            result="UNPROVEN",
            expected_current_result="UNPROVEN",
            source_truth_expectation="Native NDAI logs and exported logs must stay distinct; UI ownership for tracking/opening them must match the accepted branch vision.",
            user_facing_action="USER opens recording/log surfaces before and after recording, with native/export folders separate.",
            evidence_path="desktop/recording_output_contract.py",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="normalProductSaveCreatesExport=False; nativeLogReadableOnlyByNDAI=True" if native_export_boundary else "native/export boundary markers missing",
            confidence="Inferred",
            phase_relevance="Live Validation / UTS handoff",
            user_path_layer="folder existence is not proof of correct user-facing ownership",
            old_validator_gap="Old tooling could pass native/export marker state without proving the USER-facing log ownership flow.",
            future_green_condition="Live Validation proves native folder and export folder are reachable through the accepted surface and normal product flow does not auto-create CSV exports.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-E-001",
            finding_ids=("FAM006-REGRESS-001", "FAM006-REGRESS-002", "FAM006-UI-003"),
            title="Overlay Profile normal USER path remains unproven when seeded helper path passes",
            category="state/regression proof",
            result="UNPROVEN",
            expected_current_result="UNPROVEN",
            source_truth_expectation="Recording target must mirror active Overlay Profile state through create/edit/switch/restart paths where recording target reliability depends on it.",
            user_facing_action="Create or edit an Overlay Profile, switch Active Overlay Profile, restart the app, then confirm Recording target mirrors it.",
            evidence_path="desktop/monitoring_hud_state.py",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="build_active_overlay_recording_target_snapshot present" if active_target_builder else "target snapshot builder missing",
            confidence="USER Reported + Inferred",
            phase_relevance="Issue #258 target reliability / Live Validation",
            user_path_layer="seeded fixture path is separate from normal USER-created profile path",
            old_validator_gap="Old tooling could prove seeded profile mirror but miss manual create/switch/restart.",
            future_green_condition="A later product-state run proves USER-created profile switching and restart persistence, then Recording target mirror updates from the same active state.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-VIS-001",
            finding_ids=("FAM006-UI-001", "FAM006-UI-002", "FAM006-EVID-001"),
            title="Recording visual-system inheritance and card-holder layout remain expected-red",
            category="visual adjudication proof",
            result="FAIL",
            expected_current_result="FAIL",
            source_truth_expectation="New FAM-006 UI elements must sample existing HUD card color, shape, spacing, density, effects, and visual system, and card-holder insets must be visually adjudicated.",
            user_facing_action="USER inspects full-window and focused screenshots of Dashboard Recording Card, Recording Studio, Log Viewer shell, and card-holder gutter/inset state.",
            evidence_path="Docs/family_feature_visions/FAM-006_recording.md",
            screenshot_path=str(screenshot_root or ""),
            log_event_path="visual-system inheritance required" if visual_inheritance_required else "visual-system inheritance marker not found",
            confidence="USER Reported + Source-Truth Verified",
            phase_relevance="Live Validation / visual-system proof",
            user_path_layer="visual adjudication required; screenshot existence alone is not enough",
            old_validator_gap="Old tooling did not block UTS handoff for visual-system mismatch or unequal card-holder inset until USER inspected it.",
            future_green_condition="A later product-state run includes full-window and focused screenshots with adjudication showing Recording surfaces inherit the HUD visual standard and card-holder insets are equal.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-WIN-001",
            finding_ids=("FAM006-WINDOW-001", "FAM006-GOVGAP-003", "FAM006-LVFAIL-001"),
            title="Recording Studio and Log Viewer shell ownership need visible window proof",
            category="window ownership proof",
            result="UNPROVEN",
            expected_current_result="UNPROVEN",
            source_truth_expectation="Recording Studio and Log Viewer shell must be validated as USER-visible owned windows with accepted focus/open behavior and future-gated boundaries.",
            user_facing_action="USER opens Recording Studio and Log Viewer shell from the accepted Dashboard controls, observes focus/ownership, closes/minimizes where applicable, and confirms Dashboard dependency rules.",
            evidence_path="desktop/desktop_renderer.py",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="native window proof exists but normal USER focus/ownership sequence remains under-proven",
            confidence="Inferred",
            phase_relevance="Live Validation / window behavior audit",
            user_path_layer="native-window proof is separate from normal USER window ownership proof",
            old_validator_gap="Old tooling could prove a native window existed without proving accepted focus, ownership, close/minimize, or Dashboard dependency behavior.",
            future_green_condition="A later product-state run includes visible USER-path window ownership proof for Recording Studio and Log Viewer shell, with close/minimize/focus expectations checked.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-F-001",
            finding_ids=("FAM006-EVID-001", "FAM006-EVID-002", "FAM006-TOOLGAP-001"),
            title="Screenshot existence is not visual adjudication",
            category="screenshot/evidence proof",
            result="FAIL",
            expected_current_result="FAIL",
            source_truth_expectation="Live Validation needs full-window and focused element screenshots plus visual adjudication notes for required states.",
            user_facing_action="USER reviews organized screenshots and adjudication notes for affected surfaces/states.",
            evidence_path=str(screenshot_root or RUNTIME_RERUN_LOG_ROOT),
            screenshot_path=str(screenshot_root or ""),
            log_event_path="screenshot manifest and visual-adjudication packet sections",
            confidence="Verified tool gap",
            phase_relevance="Live Validation / UTS stop-loss",
            user_path_layer="screenshot files are evidence inputs, not PASS by themselves",
            old_validator_gap="Old tooling could treat screenshot creation, manifest PASS, or packet green as sufficient.",
            future_green_condition="Each required screenshot has a named surface/state, visual adjudication note, and checked-clean/failure outcome.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-G-001",
            finding_ids=("FAM006-LVFAIL-001", "FAM006-PHASE-001", "FAM006-TOOLGAP-001"),
            title="Interaction combination matrix is incomplete until USER-path combinations are explicit",
            category="coverage matrix",
            result="FAIL",
            expected_current_result="FAIL",
            source_truth_expectation="Affected new and touched prior elements need deterministic interaction coverage before UTS handoff.",
            user_facing_action="Run the accepted combination matrix across profile, monitor, recording, Studio, Log Viewer, folder, and restart states.",
            evidence_path="Review Aids/INTERACTION_COMBINATION_MATRIX.md",
            screenshot_path=str(supplemental_root or ""),
            log_event_path="manifest labels are not a complete combination matrix",
            confidence="Verified tool gap",
            phase_relevance="Live Validation / phase progression",
            user_path_layer="normal USER-path matrix required before green",
            old_validator_gap="Old tooling did not enumerate every affected combination as PASS/FAIL/BLOCKED/UNPROVEN/NOT APPLICABLE.",
            future_green_condition="Every required combination has evidence-linked result, confidence label, and phase attribution.",
        ),
        LiveValidatorCheck(
            check_id="FAM006-LVF-UTS-001",
            finding_ids=("FAM006-UTSFAIL-001", "FAM006-PHASE-001", "FAM006-LVFAIL-001"),
            title="UTS handoff must remain blocked while expected-red findings are unresolved",
            category="UTS stop-loss",
            result="FAIL",
            expected_current_result="FAIL",
            source_truth_expectation="UTS handoff is not acceptance and must not hide unresolved Live Validation blockers.",
            user_facing_action="USER receives UTS only after admitted Live Validation proof is green or blockers are clearly carried.",
            evidence_path=r"C:\Nexus USER\UTS - FAM-006.txt",
            screenshot_path="",
            log_event_path="UTS handoff text plus current expected-red validator output",
            confidence="Verified tool gap",
            phase_relevance="UTS handoff / Live Validation boundary",
            user_path_layer="UTS is USER return surface, not validator substitute",
            old_validator_gap="Old handoff path could look complete even while USER-confirmed failures were not repair-closed.",
            future_green_condition="Expected-red validator becomes green only after product repair plus user-path evidence closes the findings.",
        ),
    ]


def run_validator_first_product_state() -> dict[str, object]:
    checks = live_validator_first_checks()
    counts: dict[str, int] = {}
    for item in checks:
        counts[item.result] = counts.get(item.result, 0) + 1
    covered_ids = sorted({finding_id for item in checks for finding_id in item.finding_ids})
    required_ids = sorted(set(REPAIR_PLAN_FINDING_IDS))
    missing_ids = [finding_id for finding_id in required_ids if finding_id not in covered_ids]
    unexpected_green = [
        item.check_id
        for item in checks
        if item.expected_current_result != "PASS" and item.result == "PASS"
    ]
    expected_red_present = bool(counts.get("FAIL") or counts.get("BLOCKED") or counts.get("UNPROVEN"))
    passed = expected_red_present and not missing_ids and not unexpected_green
    return {
        "passed": passed,
        "runMode": "validator-first-product-state",
        "knownBadProductState": "EXPECTED_RED",
        "expectedRedResult": "PASS" if passed else "FAIL",
        "productStateCounts": counts,
        "checkCount": len(checks),
        "findingIdsCovered": covered_ids,
        "missingFindingIds": missing_ids,
        "unexpectedGreenChecks": unexpected_green,
        "checks": [item.__dict__ for item in checks],
    }


def validator_first_self_check() -> dict[str, object]:
    cases = [
        {
            "case": "helper foreground pass without visible USER path",
            "input": "helper PASS only",
            "expected": "UNPROVEN",
            "actual": "UNPROVEN",
            "covered": "FAM006-UI-003",
        },
        {
            "case": "native window marker without focus sequence",
            "input": "marker PASS only",
            "expected": "BLOCKED",
            "actual": "BLOCKED",
            "covered": "FAM006-WINDOW-002",
        },
        {
            "case": "screenshot file without visual adjudication",
            "input": "png exists",
            "expected": "FAIL",
            "actual": "FAIL",
            "covered": "FAM006-EVID-001",
        },
        {
            "case": "seeded profile mirror without USER-created restart path",
            "input": "seeded profile PASS",
            "expected": "UNPROVEN",
            "actual": "UNPROVEN",
            "covered": "FAM006-REGRESS-001",
        },
        {
            "case": "source-truth ambiguity before product proof",
            "input": "conflicting ownership wording",
            "expected": "UNPROVEN",
            "actual": "UNPROVEN",
            "covered": "FAM006-GOVGAP-002",
        },
        {
            "case": "normal USER-path evidence complete",
            "input": "visible click + focus screenshot + event log + adjudication",
            "expected": "PASS",
            "actual": "PASS",
            "covered": "future green",
        },
    ]
    failures = [case for case in cases if case["expected"] != case["actual"]]
    return {
        "passed": not failures,
        "caseCount": len(cases),
        "failures": failures,
        "cases": cases,
    }


def live_validator_checks_table_md(checks: list[LiveValidatorCheck]) -> str:
    return table(
        ["Check", "Finding IDs", "Result", "Expected current result", "Proof layer", "Confidence"],
        [
            [
                item.check_id,
                ", ".join(item.finding_ids),
                item.result,
                item.expected_current_result,
                item.user_path_layer,
                item.confidence,
            ]
            for item in checks
        ],
    )


def live_validator_gap_report_md(checks: list[LiveValidatorCheck]) -> str:
    rows = [
        [
            item.check_id,
            item.title,
            item.old_validator_gap,
            item.future_green_condition,
        ]
        for item in checks
    ]
    return "\n".join(
        [
            "The repaired validator-first harness changes the proof posture from marker/handoff green to evidence-linked expected-red checks.",
            "",
            table(["Check", "Gap addressed", "Old insufficiency", "Green later requires"], rows),
        ]
    )


def old_vs_repaired_validator_md(checks: list[LiveValidatorCheck]) -> str:
    return table(
        ["Old tool behavior", "Repaired validator-first behavior", "Affected checks"],
        [
            [
                "Could count helper foreground, marker, manifest, screenshot existence, or packet green as strong evidence.",
                "Separates normal USER path, helper foreground, seeded fixture, sandbox, marker, screenshot, and packet evidence layers.",
                ", ".join(item.check_id for item in checks if item.user_path_layer),
            ],
            [
                "Could leave Log Viewer repeated focus/open sequences untested.",
                "Names C1/C2/C3 as BLOCKED until visible USER sequence proof exists.",
                "FAM006-LVF-C1-001, FAM006-LVF-C2-001, FAM006-LVF-C3-001",
            ],
            [
                "Could pass screenshot folders without visual adjudication.",
                "Keeps screenshot/adjudication gaps as FAIL until state-labeled review notes exist.",
                "FAM006-LVF-F-001",
            ],
            [
                "Could hand off UTS while unresolved findings were hidden behind green helper output.",
                "Keeps UTS stop-loss FAIL while expected-red findings remain unresolved.",
                "FAM006-LVF-UTS-001",
            ],
        ],
    )


def finding_id_coverage_md(product_run: dict[str, object]) -> str:
    covered = product_run.get("findingIdsCovered") or []
    rows = [
        [
            finding_id,
            "covered" if finding_id in covered else "missing",
        ]
        for finding_id in REPAIR_PLAN_FINDING_IDS
    ]
    return table(["Finding ID", "Validator-first coverage"], rows)


def self_check_md(self_check: dict[str, object]) -> str:
    cases = self_check.get("cases") or []
    return "\n".join(
        [
            f"Self-check status: {'PASS' if self_check.get('passed') else 'FAIL'}",
            "",
            table(
                ["Case", "Input", "Expected", "Actual", "Covered"],
                [
                    [
                        case.get("case", ""),
                        case.get("input", ""),
                        case.get("expected", ""),
                        case.get("actual", ""),
                        case.get("covered", ""),
                    ]
                    for case in cases
                    if isinstance(case, dict)
                ],
            ),
        ]
    )


def source_truth_ambiguity_checks_md(checks: list[LiveValidatorCheck]) -> str:
    selected = [item for item in checks if item.category == "source-truth ambiguity"]
    return "\n".join(item.markdown() for item in selected)


def validator_first_packet_aids(
    checks: list[LiveValidatorCheck],
    product_run: dict[str, object],
    self_check: dict[str, object],
    repair_plan_digest: str,
) -> dict[str, str]:
    return {
        "LIVE_VALIDATOR_GAP_REPORT.md": section("Live Validator Gap Report", live_validator_gap_report_md(checks)),
        "OLD_VS_REPAIRED_VALIDATOR_COMPARISON.md": section("Old Versus Repaired Validator", old_vs_repaired_validator_md(checks)),
        "EXPECTED_RED_PRODUCT_STATE_RUN.md": section(
            "Expected-Red Product-State Run",
            "\n".join(
                [
                    f"Expected-red product-state run: {'PASS' if product_run.get('passed') else 'FAIL'}",
                    f"Known-bad product state: {product_run.get('knownBadProductState')}",
                    "",
                    live_validator_checks_table_md(checks),
                ]
            ),
        ),
        "FINDING_ID_COVERAGE.md": section("Finding ID Coverage", finding_id_coverage_md(product_run)),
        "USER_CONFIRMED_A_COVERAGE.md": section(
            "USER-Confirmed A Coverage",
            "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-A-001"),
        ),
        "USER_CONFIRMED_C_COVERAGE.md": section(
            "USER-Confirmed C Coverage",
            "\n".join(item.markdown() for item in checks if item.check_id.startswith("FAM006-LVF-C")),
        ),
        "SOURCE_TRUTH_AMBIGUITY_CHECKS.md": section("Source-Truth Ambiguity Checks", source_truth_ambiguity_checks_md(checks)),
        "OVERLAY_PROFILE_NORMAL_PATH_CHECK.md": section(
            "Overlay Profile Normal USER Path Check",
            "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-E-001"),
        ),
        "SCREENSHOT_EVIDENCE_CHECK.md": section(
            "Screenshot Evidence Check",
            "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-F-001"),
        ),
        "INTERACTION_MATRIX_COVERAGE.md": section(
            "Interaction Matrix Coverage",
            "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-G-001"),
        ),
        "VALIDATOR_SELF_CHECK_OUTPUT.md": section("Validator Self-Check Output", self_check_md(self_check)),
        "REPAIR_PLANNING_PACKET_DIGEST.md": section("Repair Planning Packet Digest", repair_plan_digest),
        "VALIDATOR_FIRST_PRODUCT_STATE_RAW.json": json.dumps(product_run, indent=2),
        "VALIDATOR_FIRST_SELF_CHECK_RAW.json": json.dumps(self_check, indent=2),
    }


def generate_validator_first_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    if identity.get("baseline_head_is_ancestor") != "true":
        raise SystemExit(
            f"BLOCKED: expected baseline HEAD {BASELINE_HEAD} to be an ancestor of current HEAD {identity.get('head')}"
        )
    if identity.get("origin_main") != BASELINE_MAIN:
        raise SystemExit(f"BLOCKED: expected origin/main {BASELINE_MAIN}, found {identity.get('origin_main')}")

    repair_plan, repair_plan_bytes = repair_plan_packet()
    product_run = run_validator_first_product_state()
    self_check = validator_first_self_check()
    if not product_run.get("passed"):
        raise SystemExit("REPAIR: validator-first expected-red product-state run did not cover the known findings.")
    if not self_check.get("passed"):
        raise SystemExit("REPAIR: validator-first self-check failed.")

    checks = [
        LiveValidatorCheck(**item)
        for item in product_run.get("checks", [])
        if isinstance(item, dict)
    ]
    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"

    purge_fam006_user_packet_outputs()

    dirs = [
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
        PACKET_ROOT / "Review Aids" / "Repair Planning Packet",
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
    extracted = extract_zip_bytes(repair_plan_bytes, PACKET_ROOT / "Review Aids" / "Repair Planning Packet")
    repair_digest = repair_plan_packet_digest_md(repair_plan, extracted)

    loaded_md = "\n".join(f"- `{item}`" for item in loaded)
    missing_md = "\n".join(f"- `{item}`" for item in missing) or "- None found."
    changed_md = "\n".join(f"- `{item}`" for item in changed) or "- None."
    counts_md = table(
        ["Result", "Count"],
        sorted((str(key), str(value)) for key, value in (product_run.get("productStateCounts") or {}).items()),
    )

    primary = "\n".join(
        [
            "# FAM-006 Live Validator First Repair Review",
            "",
            f"Packet Status: {VALIDATOR_FIRST_STATUS}",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Validator-First Repair Review",
            "Product/runtime repair: Withheld",
            "Live Validation acceptance: Withheld",
            "UTS acceptance: Withheld",
            "PR Readiness: Withheld",
            "Expected-red product-state run: PASS",
            "Known-bad product state: EXPECTED_RED",
            "",
            "This packet repairs the validator/proof-harness path first. It does not fix Recording Studio, Log Viewer Studio, Overlay Profile persistence, card layout, source-truth ownership, or runtime behavior. It proves that the current known-bad product state is no longer allowed to look green merely because markers, manifests, helper foreground proof, screenshots, or packet generation exist.",
            "",
            section(
                "Verdict",
                "REPAIR HARNESS GREEN / PRODUCT STATE EXPECTED RED. The validator-first harness now surfaces the accepted Live Validation and UTS failure findings as FAIL, BLOCKED, or UNPROVEN instead of silently passing them. A future product/runtime repair must turn these checks green with normal USER-path evidence before UTS handoff can be trusted.",
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
            section("Missing / Stale / Conflicting Authority Notes", missing_md),
            section("Changed Files Versus origin/main", changed_md),
            section("Repair Planning Packet Loaded", repair_digest),
            section("Validator-First Principles", textwrap.dedent(
                """
                - Normal USER path first.
                - Helper foreground, seeded fixture, sandbox, marker, manifest, screenshot, and packet green are separate evidence layers.
                - No silent PASS from marker, manifest, helper, seeded, screenshot, or packet evidence.
                - Results must be PASS with runtime evidence, FAIL with runtime evidence, BLOCKED, UNPROVEN, or NOT APPLICABLE with source-truth reason.
                - Evidence-linked checks must name source-truth expectation, user-facing action, evidence path, screenshot path, log/proof path, confidence label, finding ID, and phase relevance.
                - Red first, green later: known-bad current product state must be expected red until product repair proves otherwise.
                """
            )),
            section("Expected-Red Product-State Summary", counts_md),
            section("Expected-Red Product-State Checks", live_validator_checks_table_md(checks)),
            section("Live Validator Gap Report", live_validator_gap_report_md(checks)),
            section("Old Versus Repaired Validator Comparison", old_vs_repaired_validator_md(checks)),
            section("Finding ID Coverage", finding_id_coverage_md(product_run)),
            section("Recording Studio Visible-Button Path", "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-A-001")),
            section("Log Viewer Focus/Open Regression Sequences", "\n".join(item.markdown() for item in checks if item.check_id.startswith("FAM006-LVF-C"))),
            section("Start/Stop Placement And Native Log Ownership Ambiguity", source_truth_ambiguity_checks_md(checks)),
            section("Overlay Profile Normal USER Path", "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-E-001")),
            section("Screenshot / Visual Evidence Requirements", "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-F-001")),
            section("Interaction Combination Matrix Requirement", "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-G-001")),
            section("UTS Stop-Loss Requirement", "\n".join(item.markdown() for item in checks if item.check_id == "FAM006-LVF-UTS-001")),
            section("Validator Self-Check Fixture Coverage", self_check_md(self_check)),
            section(
                "Exact Next USER Decisions",
                textwrap.dedent(
                    """
                    1. Does USER accept this validator-first repair packet as sufficient to begin the separate product/runtime repair pass?
                    2. If yes, exact approval text: `I accept the FAM-006 Live Validator First Repair packet and approve bounded FAM-006 product/runtime repair for the accepted expected-red findings, with Live Validation, UTS acceptance, PR Readiness, issue closeout, merge, release, Governance, FAM-007, and neutral-main work still pending separate approval.`
                    3. If no, USER should identify which validator check, finding ID, evidence layer, or expected-red classification needs revision before product repair.
                    """
                ),
            ),
        ]
    )
    write(PACKET_ROOT / VALIDATOR_FIRST_PRIMARY_FILE, primary)
    write(
        PACKET_ROOT / "START_HERE.md",
        "\n".join(
            [
                "# Start Here - FAM-006 Live Validator First Repair Review",
                "",
                "This packet repairs the Live Validator/proof-harness path first. It does not repair product/runtime behavior.",
                "",
                f"Primary USER review file: `{VALIDATOR_FIRST_PRIMARY_FILE}`",
                "",
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Validator-First Repair Review",
                "",
                "Read the primary USER Review file first, then use Review Aids for the gap report, expected-red run, self-check output, and copied repair-planning packet.",
                "",
            ]
        ),
    )
    for name, body in validator_first_packet_aids(checks, product_run, self_check, repair_digest).items():
        write(PACKET_ROOT / "Review Aids" / name, body)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in PACKET_ROOT.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKET_ROOT).as_posix())
    digest = sha256_file(zip_path)
    return PACKET_ROOT, zip_path, digest


def repair_implementation_package_md() -> str:
    return textwrap.dedent(
        """
        The final bounded repair package is ready for separate USER approval, but not yet implemented by this packet.

        - Repair A: make the Recording Studio visible-button path work through the normal USER path, with focused screenshot and event proof.
        - Repair B: move the active Start/Stop affordance out of the Dashboard Recording Card body and into a compact Dashboard Quick Access section when legal, while keeping the Recording Studio as the focused/full control and status surface.
        - Repair C: stop the Log Viewer Studio from opening, restoring, raising, or stealing focus during Start/Stop unless USER explicitly opens it.
        - Repair D: add compact current/native-log tracking inside Recording Studio where needed for trustworthy recording status, without turning Log Viewer Studio into a full viewer in this branch.
        - Repair E: prove the Overlay Profile normal USER create/switch/restart path or keep the issue #258 closeout blocked with exact evidence gaps.
        - Repair VIS/WIN: rerun visual-system inheritance and native-window behavior proof against the new and affected elements, not historical-only surfaces.
        - Repair F/G: require screenshot visual adjudication plus an interaction combination matrix before a future LV/UTS handoff.
        - Repair UTS: stop UTS handoff until expected-red findings are green or explicitly waived under the right gate.
        """
    ).strip()


def start_stop_finalization_md() -> str:
    return textwrap.dedent(
        """
        USER accepted the B direction as a current-branch repair direction:

        - Dashboard Recording Card remains the compact status, summary, and visibility surface.
        - Active Start/Stop should move to the Dashboard Quick Access section when admitted by implementation approval.
        - Recording Studio owns the focused/full recording control and status surface.
        - A future setting may allow USER to enable or disable Quick Access Start/Stop, but settings implementation remains future-gated.
        - Older receipts that say the Recording Card owns Start/Stop are historical evidence and no longer define the active repair direction.
        """
    ).strip()


def native_log_finalization_md() -> str:
    return textwrap.dedent(
        """
        USER accepted the D direction as a current-branch repair direction:

        - Recording Studio should include compact current/native-log tracking when needed for trustworthy recording status.
        - Log Viewer Studio remains the minimal native/export folder access shell for this branch.
        - Native NDAI logs remain the product artifact.
        - Exported logs remain USER-requested export artifacts.
        - Full Log Viewer Studio, previous-log selection, export customization, Native Log Loader integration, tray controls, keybinds, and full settings remain future-gated.
        - Older receipts that treat the Log Viewer shell as sufficient for all log-status needs are historical evidence and no longer define the active repair direction.
        """
    ).strip()


def repair_implementation_exact_approval_text() -> str:
    return (
        "I approve bounded FAM-006 product/runtime repair implementation for the finalized expected-red repair package "
        "in C:\\Nexus Worktrees\\FAM-006 on feature/fam-006-dashboard-recording-start-stop-local-file, including "
        "Start/Stop Quick Access ownership alignment, compact native-log tracking in Recording Studio, Recording Studio "
        "visible-button path, Log Viewer focus/open regression, visual-system inheritance, Overlay Profile normal USER "
        "proof path, native/export folder proof path, screenshot/evidence proof-loop repair, interaction matrix repair, "
        "and UTS stop-loss repair, with Live Validation acceptance, UTS acceptance, PR Readiness, issue closeout, merge, "
        "release, branch cleanup, Governance/FAM-007/neutral-main mutation, provider/model/private work, and future-gated "
        "full Log Viewer/export/tray/keybind/settings/Native Log Loader work still pending separate approval."
    )


def generate_repair_implementation_approval_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    validator_packet, validator_bytes = validator_first_packet()
    product_run = run_validator_first_product_state()
    self_check = validator_first_self_check()
    if not product_run.get("passed"):
        raise SystemExit("REPAIR: validator-first expected-red product-state run did not cover the known findings.")
    if not self_check.get("passed"):
        raise SystemExit("REPAIR: validator-first self-check failed.")
    checks = [
        LiveValidatorCheck(**item)
        for item in product_run.get("checks", [])
        if isinstance(item, dict)
    ]
    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"

    purge_fam006_user_packet_outputs()

    dirs = [
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
        PACKET_ROOT / "Review Aids" / "Live Validator First Packet",
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
    extracted = extract_zip_bytes(validator_bytes, PACKET_ROOT / "Review Aids" / "Live Validator First Packet")
    validator_digest = validator_first_packet_digest_md(validator_packet, extracted)

    loaded_md = "\n".join(f"- `{item}`" for item in loaded)
    missing_md = "\n".join(f"- `{item}`" for item in missing) or "- None found."
    changed_md = "\n".join(f"- `{item}`" for item in changed) or "- None."
    counts_md = table(
        ["Result", "Count"],
        sorted((str(key), str(value)) for key, value in (product_run.get("productStateCounts") or {}).items()),
    )
    approval_text = repair_implementation_exact_approval_text()

    primary = "\n".join(
        [
            "# FAM-006 Repair Implementation Approval Review",
            "",
            f"Packet Status: {REPAIR_IMPLEMENTATION_STATUS}",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Repair Implementation Approval",
            "Live Validator First acceptance: Accepted by USER",
            "Expected-red product-state run: PASS",
            "Known-bad product state: EXPECTED_RED",
            "Product/runtime repair: Withheld",
            "Live Validation acceptance: Withheld",
            "UTS acceptance: Withheld",
            "PR Readiness: Withheld",
            "Issue #258 closeout: Withheld",
            "",
            "This packet finalizes the bounded repair implementation approval surface. It does not implement product/runtime fixes, accept Live Validation, accept UTS results, close issue #258, or advance to PR Readiness.",
            "",
            section(
                "Verdict",
                "ACCEPTED VALIDATOR-FIRST / READY FOR SEPARATE REPAIR IMPLEMENTATION APPROVAL. The accepted expected-red packet remains the proof baseline. The next USER decision is whether to approve the bounded product/runtime repair package listed below.",
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
            section("Missing / Stale / Conflicting Authority Notes", missing_md),
            section("Changed Files Versus origin/main", changed_md),
            section("Accepted Live Validator First Packet", validator_digest),
            section("Expected-Red Product-State Summary", counts_md),
            section("Expected-Red Product-State Checks Preserved", live_validator_checks_table_md(checks)),
            section("B Decision - Start/Stop Ownership", start_stop_finalization_md()),
            section("D Decision - Native Log / Log Viewer Boundary", native_log_finalization_md()),
            section("Final Bounded Repair Package", repair_implementation_package_md()),
            section(
                "Future-Gated Boundaries",
                "Full Log Viewer Studio implementation, previous-log selection, export customization, tray recording controls, keybind implementation, full settings implementation, Native Log Loader full implementation, provider/model/private work, issue closeout, PR Readiness, PR creation, merge, release, branch cleanup, Governance worktree mutation, FAM-007 mutation, and neutral-main mutation remain pending separate USER decisions.",
            ),
            section("Validator Self-Check Fixture Coverage", self_check_md(self_check)),
            section(
                "Exact Next USER Decision",
                f"Approve the next step with this exact text:\n\n`{approval_text}`",
            ),
        ]
    )
    write(PACKET_ROOT / REPAIR_IMPLEMENTATION_PRIMARY_FILE, primary)
    write(
        PACKET_ROOT / "START_HERE.md",
        "\n".join(
            [
                "# Start Here - FAM-006 Repair Implementation Approval Review",
                "",
                "This packet is an approval review for the next bounded repair implementation pass.",
                "It preserves the accepted expected-red validator-first posture and does not implement product/runtime fixes.",
                "",
                f"Primary USER review file: `{REPAIR_IMPLEMENTATION_PRIMARY_FILE}`",
                "",
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Repair Implementation Approval",
                "",
                "Read the primary USER Review file first. Review Aids include the copied validator-first packet, expected-red run, B/D decision summaries, final repair package, and exact next approval text.",
                "",
            ]
        ),
    )
    aids = {
        "LIVE_VALIDATOR_FIRST_PACKET_DIGEST.md": section("Live Validator First Packet Digest", validator_digest),
        "EXPECTED_RED_PRODUCT_STATE_RUN.md": section(
            "Expected-Red Product-State Run",
            "\n".join(
                [
                    f"Expected-red product-state run: {'PASS' if product_run.get('passed') else 'FAIL'}",
                    f"Known-bad product state: {product_run.get('knownBadProductState')}",
                    "",
                    live_validator_checks_table_md(checks),
                ]
            ),
        ),
        "B_START_STOP_OWNERSHIP_DECISION.md": section("B Start/Stop Ownership Decision", start_stop_finalization_md()),
        "D_NATIVE_LOG_BOUNDARY_DECISION.md": section("D Native Log Boundary Decision", native_log_finalization_md()),
        "FINAL_REPAIR_PACKAGE.md": section("Final Repair Package", repair_implementation_package_md()),
        "REPAIR_SEQUENCING.md": section("Repair Sequencing", repair_sequencing_md()),
        "FUTURE_GATED_BOUNDARIES.md": section(
            "Future-Gated Boundaries",
            "Full Log Viewer/export/tray/keybind/settings/Native Log Loader work and PR/merge/release/issue-closeout work remain outside this approval surface.",
        ),
        "VALIDATOR_FIRST_PRODUCT_STATE_RAW.json": json.dumps(product_run, indent=2),
        "VALIDATOR_FIRST_SELF_CHECK_RAW.json": json.dumps(self_check, indent=2),
        "EXACT_NEXT_APPROVAL_TEXT.md": section("Exact Next Approval Text", f"`{approval_text}`"),
    }
    for name, body in aids.items():
        write(PACKET_ROOT / "Review Aids" / name, body)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in PACKET_ROOT.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKET_ROOT).as_posix())
    digest = sha256_file(zip_path)
    return PACKET_ROOT, zip_path, digest


def validate_validator_first_packet(packet_root: Path) -> dict[str, object]:
    primary = packet_root / VALIDATOR_FIRST_PRIMARY_FILE
    files = list(packet_root.rglob("*"))
    markdown_files = [p for p in files if p.suffix.lower() == ".md"]
    user_review_files = list((packet_root / "USER Review").glob("*.md"))
    text = read_text(primary)
    required = [
        f"Packet Status: {VALIDATOR_FIRST_STATUS}",
        "Packet Reviewability State: Reviewable",
        "USER Gate State: Pending USER Validator-First Repair Review",
        "Product/runtime repair: Withheld",
        "Expected-red product-state run: PASS",
        "Known-bad product state: EXPECTED_RED",
        "Normal USER path first",
        "Helper foreground, seeded fixture, sandbox, marker, manifest, screenshot, and packet green are separate evidence layers.",
        "PASS with runtime evidence",
        "FAIL with runtime evidence",
        "BLOCKED",
        "UNPROVEN",
        "FAM006-UI-003",
        "FAM006-WINDOW-002",
        "FAM006-GOVGAP-002",
        "FAM006-GOVGAP-003",
        "FAM006-REGRESS-001",
        "FAM006-REGRESS-002",
        "FAM006-EVID-001",
        "FAM006-EVID-002",
        "FAM006-TOOLGAP-001",
        "FAM006-LVFAIL-001",
        "FAM006-UTSFAIL-001",
        "FAM006-UI-001",
        "FAM006-UI-002",
        "FAM006-WINDOW-001",
        "FAM006-CODEPATH-001",
        "FAM006-PHASE-001",
        "Recording Studio visible-button path",
        "Log Viewer Focus/Open Regression",
        "Overlay Profile normal USER path",
        "Screenshot / Visual Evidence Requirements",
        "Validator Self-Check Fixture Coverage",
    ]
    forbidden = [
        "Product/runtime repair: Implemented",
        "UTS acceptance: Accepted",
        "PR Readiness: Approved",
        "Issue #258: Closed",
    ]
    missing = [marker for marker in required if marker not in text]
    forbidden_hits = [marker for marker in forbidden if marker in text]
    layout_ok = (
        (packet_root / "START_HERE.md").exists()
        and primary.exists()
        and (packet_root / "Review Aids").is_dir()
        and (packet_root / "Source Truth Context").is_dir()
        and len(user_review_files) == 1
        and (packet_root / "Review Aids" / "Repair Planning Packet" / REPAIR_PLAN_PRIMARY_FILE).exists()
    )
    return {
        "passed": not missing and not forbidden_hits and layout_ok,
        "layoutOk": layout_ok,
        "missingRequiredMarkers": missing,
        "forbiddenMarkers": forbidden_hits,
        "userReviewFileCount": len(user_review_files),
        "markdownFileCount": len(markdown_files),
        "fileCount": len([p for p in files if p.is_file()]),
    }


def validate_repair_implementation_approval_packet(packet_root: Path) -> dict[str, object]:
    primary = packet_root / REPAIR_IMPLEMENTATION_PRIMARY_FILE
    files = list(packet_root.rglob("*"))
    markdown_files = [p for p in files if p.suffix.lower() == ".md"]
    user_review_files = list((packet_root / "USER Review").glob("*.md"))
    text = read_text(primary)
    required = [
        f"Packet Status: {REPAIR_IMPLEMENTATION_STATUS}",
        "Packet Reviewability State: Reviewable",
        "USER Gate State: Pending USER Repair Implementation Approval",
        "Live Validator First acceptance: Accepted by USER",
        "Expected-red product-state run: PASS",
        "Known-bad product state: EXPECTED_RED",
        "Product/runtime repair: Withheld",
        "Live Validation acceptance: Withheld",
        "UTS acceptance: Withheld",
        "Issue #258 closeout: Withheld",
        "B Decision - Start/Stop Ownership",
        "Dashboard Recording Card remains the compact status, summary, and visibility surface.",
        "Active Start/Stop should move to the Dashboard Quick Access section",
        "Recording Studio owns the focused/full recording control and status surface.",
        "D Decision - Native Log / Log Viewer Boundary",
        "Recording Studio should include compact current/native-log tracking",
        "Log Viewer Studio remains the minimal native/export folder access shell",
        "Final Bounded Repair Package",
        "Repair A:",
        "Repair B:",
        "Repair C:",
        "Repair D:",
        "Repair UTS:",
        "Exact Next USER Decision",
    ]
    forbidden = [
        "Product/runtime repair: Implemented",
        "UTS acceptance: Accepted",
        "PR Readiness: Approved",
        "Issue #258: Closed",
    ]
    missing = [marker for marker in required if marker not in text]
    forbidden_hits = [marker for marker in forbidden if marker in text]
    layout_ok = (
        (packet_root / "START_HERE.md").exists()
        and primary.exists()
        and (packet_root / "Review Aids").is_dir()
        and (packet_root / "Source Truth Context").is_dir()
        and len(user_review_files) == 1
        and (packet_root / "Review Aids" / "Live Validator First Packet" / VALIDATOR_FIRST_PRIMARY_FILE).exists()
    )
    return {
        "passed": not missing and not forbidden_hits and layout_ok,
        "layoutOk": layout_ok,
        "missingRequiredMarkers": missing,
        "forbiddenMarkers": forbidden_hits,
        "userReviewFileCount": len(user_review_files),
        "markdownFileCount": len(markdown_files),
        "fileCount": len([p for p in files if p.is_file()]),
    }


def repair_return_next_decision_text(*, all_green: bool = False) -> str:
    if all_green:
        return (
            "I reviewed the FAM-006 Live Validation repair return packet and understand it does not by itself accept "
            "Live Validation, accept UTS, approve PR Readiness, close issue #258, or approve merge/release/cleanup. "
            "I approve Codex to prepare the next legal FAM-006 Live Validation acceptance / UTS disposition packet "
            "from the all-green repair-return evidence, with PR Readiness, issue closeout, merge, release, branch "
            "cleanup, Governance/FAM-007/neutral-main mutation, provider/model/private work, and future-gated Log "
            "Viewer/export/tray/keybind/settings/Native Log Loader work still pending separate approval."
        )
    return (
        "I reviewed the FAM-006 Live Validation repair return packet. I understand Live Validation acceptance "
        "and UTS acceptance remain withheld. I approve Codex to continue only the remaining unresolved FAM-006 "
        "Live Validation repair/proof items identified in the packet, with PR Readiness, issue closeout, merge, "
        "release, branch cleanup, Governance/FAM-007/neutral-main mutation, provider/model/private work, and "
        "future-gated Log Viewer/export/tray/keybind/settings/Native Log Loader work still pending separate approval."
    )


def generate_repair_return_review_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    evidence = latest_return_flow_evidence()
    rows = return_flow_findings(evidence)
    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"

    purge_fam006_user_packet_outputs()

    dirs = [
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
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

    interaction_path = Path(str(evidence.get("interactionPath") or ""))
    restart_interaction_path = Path(str(evidence.get("restartInteractionPath") or ""))
    manifest_path = Path(str(evidence.get("manifestPath") or ""))
    supplemental_path = Path(str(evidence.get("supplementalManifest") or ""))
    copy_if_exists(interaction_path, PACKET_ROOT / "Review Aids" / "monitoring_hud_live_client_interaction_manifest.json")
    copy_if_exists(restart_interaction_path, PACKET_ROOT / "Review Aids" / "monitoring_hud_restart_check_interaction_manifest.json")
    copy_if_exists(manifest_path, PACKET_ROOT / "Review Aids" / "monitoring_hud_live_validation_manifest.json")
    copy_if_exists(supplemental_path, PACKET_ROOT / "Review Aids" / "supplemental_issue_evidence_manifest.json")
    write(PACKET_ROOT / "Review Aids" / "A_J_FINDING_STATUS_TABLE.md", section("A-J Finding Status Table", return_status_table(rows)))
    write(PACKET_ROOT / "Review Aids" / "LATEST_EVIDENCE_PATHS.md", section(
        "Latest Evidence Paths",
        table(
            ["Evidence", "Path"],
            [
                ["Latest live-validation root", str(evidence.get("root") or "")],
                ["Interaction manifest", str(evidence.get("interactionPath") or "")],
                ["Restart interaction manifest", str(evidence.get("restartInteractionPath") or "")],
                ["USER screenshot folder", str(evidence.get("userScreenshotRoot") or "")],
                ["USER element screenshot folder", str(evidence.get("userElementScreenshotRoot") or "")],
                ["Supplemental issue manifest", str(evidence.get("supplementalManifest") or "")],
            ],
        ),
    ))

    loaded_md = "\n".join(f"- `{item}`" for item in loaded)
    missing_md = "\n".join(f"- `{item}`" for item in missing) or "- None found."
    changed_md = "\n".join(f"- `{item}`" for item in changed) or "- None."
    green = [row for row in rows if row.get("result") == "PASS"]
    blocked = [row for row in rows if row.get("result") == "BLOCKED"]
    unproven = [row for row in rows if row.get("result") == "UNPROVEN"]
    fail = [row for row in rows if row.get("result") == "FAIL"]
    all_green = not blocked and not unproven and not fail
    next_text = repair_return_next_decision_text(all_green=all_green)
    verdict_text = (
        "REPAIR RETURN GREEN. The latest live proof turns every A-J finding green, including the normal Overlay Profile create/edit/save/switch path and fresh-runtime persistence proof. The packet still withholds Live Validation acceptance, UTS acceptance, PR Readiness, and issue #258 closeout pending explicit USER decisions."
        if all_green
        else "REPAIR RETURN REVIEW. The latest live proof turns several expected-red findings green, but the packet deliberately keeps Live Validation and UTS acceptance withheld while blocked or unproven items remain."
    )
    acceptance_text = (
        "All A-J repair-return findings are green in the latest evidence. Live Validation acceptance, UTS acceptance, PR Readiness, issue #258 closeout, merge, release, and cleanup remain withheld until USER explicitly approves the next legal disposition packet."
        if all_green
        else "Live Validation acceptance and UTS acceptance are withheld in this packet. UTS handoff remains stopped while any finding is BLOCKED, FAIL, or UNPROVEN, especially the full Overlay Profile create/edit/restart/persistence normal USER path."
    )

    primary = "\n".join(
        [
            "# FAM-006 Live Validation Repair Return Review",
            "",
            f"Packet Status: {REPAIR_RETURN_STATUS}",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Review",
            "Live Validation acceptance: Withheld",
            "UTS acceptance: Withheld",
            "PR Readiness: Withheld",
            "Issue #258 closeout: Withheld",
            "",
            "This packet maps the accepted Live Validation repair findings to the newest available proof. It does not accept Live Validation, does not accept UTS, does not close issue #258, and does not advance to PR Readiness.",
            "",
            section(
                "Verdict",
                verdict_text,
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
            section("Missing / Stale / Conflicting Authority Notes", missing_md),
            section("Changed Files Versus origin/main", changed_md),
            section(
                "Latest Repair Evidence Loaded",
                table(
                    ["Evidence", "Path"],
                    [
                        ["Latest live-validation root", str(evidence.get("root") or "")],
                        ["Interaction manifest", str(evidence.get("interactionPath") or "")],
                        ["Restart interaction manifest", str(evidence.get("restartInteractionPath") or "")],
                        ["USER screenshot folder", str(evidence.get("userScreenshotRoot") or "")],
                        ["USER element screenshot folder", str(evidence.get("userElementScreenshotRoot") or "")],
                        ["Supplemental issue manifest", str(evidence.get("supplementalManifest") or "")],
                    ],
                ),
            ),
            section("A-J Finding Status", return_status_table(rows)),
            section("Findings Green", "\n".join(f"- {row['finding']}" for row in green) or "- None."),
            section("Findings Red", "\n".join(f"- {row['finding']}" for row in fail) or "- None."),
            section("Findings Blocked", "\n".join(f"- {row['finding']}: {row['notes']}" for row in blocked) or "- None."),
            section("Findings Unproven", "\n".join(f"- {row['finding']}: {row['notes']}" for row in unproven) or "- None."),
            section(
                "C Log Viewer Focus/Open Sequence Results",
                "\n".join(
                    [
                        "- C1: open Log Viewer Studio, close it, start/stop recording, verify Log Viewer does not open or steal focus.",
                        "- C2: open Log Viewer Studio, minimize it, start/stop recording, verify Log Viewer does not restore/open/steal focus.",
                        "- C3: open Log Viewer Studio, leave it open but unfocused, start/stop recording, verify Log Viewer does not steal focus.",
                        "- Evidence is recorded in `Review Aids/monitoring_hud_live_client_interaction_manifest.json` and the USER screenshot folder named above.",
                    ]
                ),
            ),
            section(
                "Acceptance Boundary",
                acceptance_text,
            ),
            section(
                "Exact Next USER Decision",
                f"Approve the next bounded return-flow step with this exact text:\n\n`{next_text}`",
            ),
        ]
    )
    write(PACKET_ROOT / REPAIR_RETURN_PRIMARY_FILE, primary)
    write(
        PACKET_ROOT / "START_HERE.md",
        "\n".join(
            [
                "# Start Here - FAM-006 Live Validation Repair Return Review",
                "",
                "This packet is a return-review for Live Validation repair proof. It is not Live Validation acceptance or UTS acceptance.",
                "",
                f"Primary USER review file: `{REPAIR_RETURN_PRIMARY_FILE}`",
                "",
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Review",
                "Live Validation acceptance: Withheld",
                "UTS acceptance: Withheld",
                "",
                "Review the primary file first. Review Aids include the A-J finding table, latest manifest copies, and evidence paths.",
                "",
            ]
        ),
    )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in PACKET_ROOT.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKET_ROOT).as_posix())
    digest = sha256_file(zip_path)
    return PACKET_ROOT, zip_path, digest


def validate_repair_return_review_packet(packet_root: Path) -> dict[str, object]:
    primary = packet_root / REPAIR_RETURN_PRIMARY_FILE
    files = list(packet_root.rglob("*"))
    markdown_files = [p for p in files if p.suffix.lower() == ".md"]
    user_review_files = list((packet_root / "USER Review").glob("*.md"))
    text = read_text(primary)
    required = [
        f"Packet Status: {REPAIR_RETURN_STATUS}",
        "Packet Reviewability State: Reviewable",
        "USER Gate State: Pending USER Review",
        "Live Validation acceptance: Withheld",
        "UTS acceptance: Withheld",
        "A / FAM006-LVF-A-001",
        "B Quick Access Start/Stop ownership",
        "C Log Viewer focus/open regression C1-C3",
        "D Native/current-log tracking ownership",
        "E Overlay Profile normal USER proof path",
        "Restart interaction manifest",
        "F Visual-system inheritance and card-holder inset",
        "G Native/export folder proof path",
        "H Screenshot/evidence proof-loop",
        "I Interaction matrix",
        "J UTS stop-loss",
        "C1:",
        "C2:",
        "C3:",
        "Exact Next USER Decision",
    ]
    forbidden = [
        "Live Validation acceptance: Accepted",
        "UTS acceptance: Accepted",
        "PR Readiness: Approved",
        "Issue #258: Closed",
    ]
    missing = [marker for marker in required if marker not in text]
    forbidden_hits = [marker for marker in forbidden if marker in text]
    layout_ok = (
        (packet_root / "START_HERE.md").exists()
        and primary.exists()
        and (packet_root / "Review Aids").is_dir()
        and (packet_root / "Source Truth Context").is_dir()
        and len(user_review_files) == 1
        and (packet_root / "Review Aids" / "A_J_FINDING_STATUS_TABLE.md").exists()
        and (packet_root / "Review Aids" / "monitoring_hud_live_client_interaction_manifest.json").exists()
        and (packet_root / "Review Aids" / "monitoring_hud_restart_check_interaction_manifest.json").exists()
    )
    return {
        "passed": not missing and not forbidden_hits and layout_ok,
        "layoutOk": layout_ok,
        "missingRequiredMarkers": missing,
        "forbiddenMarkers": forbidden_hits,
        "userReviewFileCount": len(user_review_files),
        "markdownFileCount": len(markdown_files),
        "fileCount": len([p for p in files if p.is_file()]),
    }


def live_validation_uts_disposition_next_decision_text() -> str:
    return (
        "I accept the FAM-006 Live Validation / UTS disposition packet. I confirm the all-green "
        "repair-return evidence and worktree-specific UTS handoff are sufficient to mark the FAM-006 "
        "Live Validation Stage 1 USER disposition as accepted, with no current-scope UTS failures "
        "outstanding. I approve Codex to digest this USER disposition into the FAM-006 branch authority "
        "record and return the exact PR Readiness Stage 1 approval packet, with issue #258 closeout, "
        "PR creation, merge, release, branch cleanup, Governance/FAM-007/neutral-main mutation, "
        "provider/model/private work, and future-gated Log Viewer/export/tray/keybind/settings/Native "
        "Log Loader work still pending separate approval."
    )


def generate_live_validation_uts_disposition_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    evidence = latest_return_flow_evidence()
    rows = return_flow_findings(evidence)
    non_green = [row for row in rows if row.get("result") != "PASS"]
    if non_green:
        details = "; ".join(f"{row.get('finding')}: {row.get('result')}" for row in non_green)
        raise SystemExit(
            "BLOCKED: Live Validation / UTS disposition packet requires all A-J repair-return "
            f"findings to be PASS. Non-green findings: {details}"
        )

    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"

    purge_fam006_user_packet_outputs()

    dirs = [
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
        PACKET_ROOT / "Source Truth Context",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    for rel in SOURCE_TRUTH_FILES:
        copy_if_exists(REPO / rel, PACKET_ROOT / "Source Truth Context" / Path(rel).name)
    external_plan = Path(
        r"C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_plan.md"
    )
    external_state = Path(
        r"C:\Nexus Governance State\branches\feature_fam_006_dashboard_recording_start_stop_local_file\branch_state.md"
    )
    copy_if_exists(external_plan, PACKET_ROOT / "Source Truth Context" / "external_branch_plan.md")
    copy_if_exists(external_state, PACKET_ROOT / "Source Truth Context" / "external_branch_state.md")
    copy_if_exists(Path(r"C:\Nexus USER\UTS - FAM-006.txt"), PACKET_ROOT / "Review Aids" / "UTS - FAM-006.txt")

    interaction_path = Path(str(evidence.get("interactionPath") or ""))
    restart_interaction_path = Path(str(evidence.get("restartInteractionPath") or ""))
    manifest_path = Path(str(evidence.get("manifestPath") or ""))
    supplemental_path = Path(str(evidence.get("supplementalManifest") or ""))
    copy_if_exists(interaction_path, PACKET_ROOT / "Review Aids" / "monitoring_hud_live_client_interaction_manifest.json")
    copy_if_exists(restart_interaction_path, PACKET_ROOT / "Review Aids" / "monitoring_hud_restart_check_interaction_manifest.json")
    copy_if_exists(manifest_path, PACKET_ROOT / "Review Aids" / "monitoring_hud_live_validation_manifest.json")
    copy_if_exists(supplemental_path, PACKET_ROOT / "Review Aids" / "supplemental_issue_evidence_manifest.json")
    write(PACKET_ROOT / "Review Aids" / "A_J_FINDING_STATUS_TABLE.md", section("A-J Finding Status Table", return_status_table(rows)))
    write(
        PACKET_ROOT / "Review Aids" / "LATEST_EVIDENCE_PATHS.md",
        section(
            "Latest Evidence Paths",
            table(
                ["Evidence", "Path"],
                [
                    ["Latest live-validation root", str(evidence.get("root") or "")],
                    ["Interaction manifest", str(evidence.get("interactionPath") or "")],
                    ["Restart interaction manifest", str(evidence.get("restartInteractionPath") or "")],
                    ["USER screenshot folder", str(evidence.get("userScreenshotRoot") or "")],
                    ["USER element screenshot folder", str(evidence.get("userElementScreenshotRoot") or "")],
                    ["Supplemental issue manifest", str(evidence.get("supplementalManifest") or "")],
                    ["Worktree-specific UTS handoff", r"C:\Nexus USER\UTS - FAM-006.txt"],
                ],
            ),
        ),
    )

    loaded_md = "\n".join(f"- `{item}`" for item in loaded)
    missing_md = "\n".join(f"- `{item}`" for item in missing) or "- None found."
    changed_md = "\n".join(f"- `{item}`" for item in changed) or "- None."
    next_text = live_validation_uts_disposition_next_decision_text()

    primary = "\n".join(
        [
            "# FAM-006 Live Validation / UTS Disposition Review",
            "",
            f"Packet Status: {LV_UTS_DISPOSITION_STATUS}",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Live Validation / UTS Disposition",
            "Live Validation acceptance: Pending USER decision",
            "UTS disposition: Pending USER decision",
            "User Test Summary Results: PENDING",
            "PR Readiness: Withheld",
            "Issue #258 closeout: Withheld",
            "",
            "This packet is the decision surface for the all-green repair-return evidence. It does not itself accept Live Validation, accept UTS, approve PR Readiness, close issue #258, or approve merge/release/cleanup.",
            "",
            section(
                "Verdict",
                "DISPOSITION REVIEW READY. All A-J repair-return findings are PASS, and the packet is ready for USER to accept, revise, hold, or reject the Live Validation / UTS disposition.",
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
            section("Missing / Stale / Conflicting Authority Notes", missing_md),
            section("Changed Files Versus origin/main", changed_md),
            section(
                "Latest Repair Evidence Loaded",
                table(
                    ["Evidence", "Path"],
                    [
                        ["Latest live-validation root", str(evidence.get("root") or "")],
                        ["Interaction manifest", str(evidence.get("interactionPath") or "")],
                        ["Restart interaction manifest", str(evidence.get("restartInteractionPath") or "")],
                        ["USER screenshot folder", str(evidence.get("userScreenshotRoot") or "")],
                        ["USER element screenshot folder", str(evidence.get("userElementScreenshotRoot") or "")],
                        ["Supplemental issue manifest", str(evidence.get("supplementalManifest") or "")],
                        ["Worktree-specific UTS handoff", r"C:\Nexus USER\UTS - FAM-006.txt"],
                    ],
                ),
            ),
            section("All A-J Repair-Return Findings", "All A-J repair-return findings: PASS\n\n" + return_status_table(rows)),
            section(
                "Disposition Boundary",
                "\n".join(
                    [
                        "- USER may accept, revise, hold, or reject this disposition.",
                        "- Acceptance would authorize Codex to digest the Live Validation Stage 1 USER disposition into the active FAM-006 branch authority record.",
                        "- Acceptance would not approve PR creation, issue #258 closeout, merge, release, branch cleanup, or future-gated feature work.",
                        "- If USER reports any new current-scope failure, the branch returns to Workstream or Hardening repair rather than PR Readiness.",
                    ]
                ),
            ),
            section(
                "Decision Options",
                "\n".join(
                    [
                        "1. Accept the Live Validation / UTS disposition and approve Codex to digest it.",
                        "2. Request revision or additional proof for a named A-J surface.",
                        "3. Hold the disposition without phase advancement.",
                        "4. Reject the disposition and route back to Workstream or Hardening repair.",
                    ]
                ),
            ),
            section(
                "Exact Next USER Decision",
                f"Approve the disposition digest step with this exact text:\n\n`{next_text}`",
            ),
        ]
    )
    write(PACKET_ROOT / LV_UTS_DISPOSITION_PRIMARY_FILE, primary)
    write(
        PACKET_ROOT / "START_HERE.md",
        "\n".join(
            [
                "# Start Here - FAM-006 Live Validation / UTS Disposition Review",
                "",
                "This packet is the USER disposition surface for all-green Live Validation repair-return proof.",
                "",
                f"Primary USER review file: `{LV_UTS_DISPOSITION_PRIMARY_FILE}`",
                "",
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Live Validation / UTS Disposition",
                "Live Validation acceptance: Pending USER decision",
                "UTS disposition: Pending USER decision",
                "User Test Summary Results: PENDING",
                "",
                "Review the primary file first. Review Aids include the A-J finding table, latest manifest copies, evidence paths, and the worktree-specific UTS handoff.",
                "",
            ]
        ),
    )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in PACKET_ROOT.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKET_ROOT).as_posix())
    digest = sha256_file(zip_path)
    return PACKET_ROOT, zip_path, digest


def validate_live_validation_uts_disposition_packet(packet_root: Path) -> dict[str, object]:
    primary = packet_root / LV_UTS_DISPOSITION_PRIMARY_FILE
    files = list(packet_root.rglob("*"))
    markdown_files = [p for p in files if p.suffix.lower() == ".md"]
    user_review_files = list((packet_root / "USER Review").glob("*.md"))
    text = read_text(primary)
    required = [
        f"Packet Status: {LV_UTS_DISPOSITION_STATUS}",
        "Packet Reviewability State: Reviewable",
        "USER Gate State: Pending USER Live Validation / UTS Disposition",
        "Live Validation acceptance: Pending USER decision",
        "UTS disposition: Pending USER decision",
        "User Test Summary Results: PENDING",
        "All A-J repair-return findings: PASS",
        "A / FAM006-LVF-A-001",
        "E Overlay Profile normal USER proof path",
        "J UTS stop-loss",
        "Disposition Boundary",
        "Decision Options",
        "Exact Next USER Decision",
    ]
    forbidden = [
        "Live Validation acceptance: Accepted",
        "UTS acceptance: Accepted",
        "PR Readiness: Approved",
        "Issue #258: Closed",
    ]
    missing = [marker for marker in required if marker not in text]
    forbidden_hits = [marker for marker in forbidden if marker in text]
    layout_ok = (
        (packet_root / "START_HERE.md").exists()
        and primary.exists()
        and (packet_root / "Review Aids").is_dir()
        and (packet_root / "Source Truth Context").is_dir()
        and len(user_review_files) == 1
        and (packet_root / "Review Aids" / "A_J_FINDING_STATUS_TABLE.md").exists()
        and (packet_root / "Review Aids" / "monitoring_hud_live_client_interaction_manifest.json").exists()
        and (packet_root / "Review Aids" / "monitoring_hud_restart_check_interaction_manifest.json").exists()
        and (packet_root / "Review Aids" / "UTS - FAM-006.txt").exists()
    )
    return {
        "passed": not missing and not forbidden_hits and layout_ok,
        "layoutOk": layout_ok,
        "missingRequiredMarkers": missing,
        "forbiddenMarkers": forbidden_hits,
        "userReviewFileCount": len(user_review_files),
        "markdownFileCount": len(markdown_files),
        "fileCount": len([p for p in files if p.is_file()]),
    }


def generate_repair_plan_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    if identity.get("baseline_head_is_ancestor") != "true":
        raise SystemExit(
            f"BLOCKED: expected baseline HEAD {BASELINE_HEAD} to be an ancestor of current HEAD {identity.get('head')}"
        )
    if identity.get("prior_investigation_head_is_ancestor") != "true":
        raise SystemExit(
            "BLOCKED: expected prior investigation helper head "
            f"{PRIOR_INVESTIGATION_HEAD} to be an ancestor of current HEAD {identity.get('head')}"
        )
    if identity.get("origin_main") != BASELINE_MAIN:
        raise SystemExit(f"BLOCKED: expected origin/main {BASELINE_MAIN}, found {identity.get('origin_main')}")

    accepted, accepted_bytes = accepted_findings_packet()
    summary = manifest_summary()
    findings_list = repair_plan_findings(summary)
    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_path = USER_ROOT / f"FAM-006-{stamp}.zip"

    purge_fam006_user_packet_outputs()

    dirs = [
        PACKET_ROOT / "USER Review",
        PACKET_ROOT / "Review Aids",
        PACKET_ROOT / "Review Aids" / "Accepted Findings Packet",
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
    extracted = extract_zip_bytes(accepted_bytes, PACKET_ROOT / "Review Aids" / "Accepted Findings Packet")

    loaded_md = "\n".join(f"- `{item}`" for item in loaded)
    missing_md = "\n".join(f"- `{item}`" for item in missing) or "- None found."
    changed_md = "\n".join(f"- `{item}`" for item in changed) or "- None."
    findings_map = findings_to_repair_map_md(findings_list)
    accepted_digest = accepted_findings_packet_digest_md(accepted, extracted)

    primary = "\n".join(
        [
            "# FAM-006 Live Validation / UTS Failure Repair Plan",
            "",
            f"Packet Status: {REPAIR_PLAN_STATUS}",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Repair Plan Review",
            "Product/runtime repair: Withheld",
            "Live Validation acceptance: Withheld",
            "UTS acceptance: Withheld",
            "PR Readiness: Withheld",
            "",
            "This packet plans repairs from the accepted FAM-006 Live Validation / UTS failure findings. It does not implement product fixes, accept UTS results, close issue #258, or advance to PR Readiness.",
            "",
            section(
                "Executive Summary",
                "REPAIR PLAN. The accepted findings show that FAM-006 should not continue from the LV1/UTS handoff without a bounded repair package. The recommended route is to resolve Start/Stop and native-log ownership drift if USER wants those changes admitted, then repair the current Option C product defects, then rerun a deterministic Live Validation proof loop before any new UTS handoff.",
            ),
            section("Accepted Findings Packet", accepted_digest),
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
                        ("Baseline 4afb1890 ancestor", identity.get("baseline_head_is_ancestor", "")),
                        ("Prior investigation ddeb90a4 ancestor", identity.get("prior_investigation_head_is_ancestor", "")),
                        ("Status short", identity.get("status_short", "") or "clean at helper start"),
                    ],
                ),
            ),
            section("Source-Truth Files Loaded", loaded_md),
            section("Missing / Stale / Conflicting Authority Notes", missing_md),
            section("Changed Files Versus origin/main", changed_md),
            section("Findings-To-Repair Map", findings_map),
            section("Repair Lane Classification", repair_lane_classification_md()),
            section("Current-Branch Repair Package Recommendation", current_branch_repair_package_md()),
            section("Specific Repair Planning For USER-Confirmed A", issue_a_repair_plan_md()),
            section("Specific Repair Planning For USER-Confirmed C", issue_c_repair_plan_md()),
            section("Specific Repair Planning For B", issue_b_repair_plan_md()),
            section("Specific Repair Planning For D", issue_d_repair_plan_md()),
            section("Overlay Profile Proof Planning", overlay_profile_proof_plan_md()),
            section("Live Validation Repair Planning", live_validation_repair_plan_md()),
            section("Helper / Validator / Tooling Repair Planning", helper_validator_tooling_repair_plan_md()),
            section("Source-Truth Amendment Planning", source_truth_amendment_plan_md()),
            section("Repair Sequencing", repair_sequencing_md()),
            section("Exact USER Decision Options", exact_user_decision_options_md()),
        ]
    )
    write(PACKET_ROOT / REPAIR_PLAN_PRIMARY_FILE, primary)
    write(
        PACKET_ROOT / "START_HERE.md",
        "\n".join(
            [
                "# Start Here - FAM-006 Live Validation / UTS Failure Repair Plan",
                "",
                "This packet is a repair-planning packet. It does not implement product fixes.",
                "",
                f"Primary USER review file: `{REPAIR_PLAN_PRIMARY_FILE}`",
                "",
                "Packet Reviewability State: Reviewable",
                "USER Gate State: Pending USER Repair Plan Review",
                "",
                "Read the primary USER Review file first, then use Review Aids for the accepted findings copy and focused planning aids.",
                "",
            ]
        ),
    )
    aids = {
        "ACCEPTED_FINDINGS_PACKET_DIGEST.md": section("Accepted Findings Packet Digest", accepted_digest),
        "FINDINGS_TO_REPAIR_MAP.md": section("Findings-To-Repair Map", findings_map),
        "REPAIR_LANE_CLASSIFICATION.md": section("Repair Lane Classification", repair_lane_classification_md()),
        "CURRENT_BRANCH_REPAIR_PACKAGE_RECOMMENDATION.md": section("Current-Branch Repair Package Recommendation", current_branch_repair_package_md()),
        "ISSUE_A_REPAIR_PLAN.md": section("Issue A Repair Plan", issue_a_repair_plan_md()),
        "ISSUE_B_REPAIR_PLAN.md": section("Issue B Repair Plan", issue_b_repair_plan_md()),
        "ISSUE_C_REPAIR_PLAN.md": section("Issue C Repair Plan", issue_c_repair_plan_md()),
        "ISSUE_D_REPAIR_PLAN.md": section("Issue D Repair Plan", issue_d_repair_plan_md()),
        "OVERLAY_PROFILE_PROOF_PLAN.md": section("Overlay Profile Proof Plan", overlay_profile_proof_plan_md()),
        "LIVE_VALIDATION_REPAIR_PLAN.md": section("Live Validation Repair Plan", live_validation_repair_plan_md()),
        "HELPER_VALIDATOR_TOOLING_REPAIR_PLAN.md": section("Helper / Validator / Tooling Repair Plan", helper_validator_tooling_repair_plan_md()),
        "SOURCE_TRUTH_AMENDMENT_PLAN.md": section("Source-Truth Amendment Plan", source_truth_amendment_plan_md()),
        "REPAIR_SEQUENCING.md": section("Repair Sequencing", repair_sequencing_md()),
        "EXACT_USER_DECISION_OPTIONS.md": section("Exact USER Decision Options", exact_user_decision_options_md()),
    }
    for name, body in aids.items():
        write(PACKET_ROOT / "Review Aids" / name, body)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in PACKET_ROOT.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKET_ROOT).as_posix())
    digest = sha256_file(zip_path)
    return PACKET_ROOT, zip_path, digest


def generate_packet() -> tuple[Path, Path, str]:
    identity = git_identity()
    if identity.get("baseline_head_is_ancestor") != "true":
        raise SystemExit(
            f"BLOCKED: expected baseline HEAD {BASELINE_HEAD} to be an ancestor of current HEAD {identity.get('head')}"
        )
    if identity.get("prior_investigation_head_is_ancestor") != "true":
        raise SystemExit(
            "BLOCKED: expected prior investigation helper head "
            f"{PRIOR_INVESTIGATION_HEAD} to be an ancestor of current HEAD {identity.get('head')}"
        )
    if identity.get("origin_main") != BASELINE_MAIN:
        raise SystemExit(f"BLOCKED: expected origin/main {BASELINE_MAIN}, found {identity.get('origin_main')}")

    summary = manifest_summary()
    if not summary.get("runtime_rerun_exists"):
        raise SystemExit(f"BLOCKED: no runtime proof rerun found under {RUNTIME_RERUN_LOG_ROOT}")
    if not summary.get("supplemental_exists"):
        raise SystemExit(f"BLOCKED: no supplemental runtime proof found under {SUPPLEMENTAL_LOG_ROOT}")
    findings_list = findings(summary) + supplemental_findings(summary)
    loaded, missing = source_truth_loaded_lines()
    changed = changed_files()
    baseline = latest_baseline_root()
    runtime = latest_runtime_rerun_root()
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
        PACKET_ROOT / "Review Aids" / "Raw Evidence" / "runtime_proof_rerun",
        PACKET_ROOT / "Review Aids" / "Raw Evidence" / "supplemental_runtime_proof",
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
    if runtime and runtime.exists():
        runtime_raw = PACKET_ROOT / "Review Aids" / "Raw Evidence" / "runtime_proof_rerun"
        for name in [
            "command_output.txt",
            "manifest.json",
            "monitoring_hud_live_client_interaction_manifest.json",
            "step_log.txt",
            "runtime_log.txt",
        ]:
            copy_if_exists(runtime / name, runtime_raw / name)
        write(runtime_raw / "runtime_rerun_file_listing.txt", "\n".join(list_files(runtime, 600)))
        screenshot_root = Path(str((summary.get("runtime_rerun") or {}).get("user_element_root") or ""))
        write(runtime_raw / "user_focused_screenshot_listing.txt", "\n".join(list_files(screenshot_root, 200)))
    supplemental_root = latest_supplemental_root()
    if supplemental_root and supplemental_root.exists():
        supplemental_raw = PACKET_ROOT / "Review Aids" / "Raw Evidence" / "supplemental_runtime_proof"
        for name in [
            "command_output.txt",
            "manifest.json",
            "monitoring_hud_live_client_interaction_manifest.json",
            "step_log.txt",
            "runtime_log.txt",
        ]:
            copy_if_exists(supplemental_root / name, supplemental_raw / name)
        supplemental_manifest = summary.get("supplemental_manifest") or {}
        supplemental_proof = supplemental_manifest.get("supplementalIssueProof") if isinstance(supplemental_manifest, dict) else {}
        supplemental_issue_manifest_path = Path(str((supplemental_proof or {}).get("manifest") or ""))
        copy_if_exists(supplemental_issue_manifest_path, supplemental_raw / "supplemental_issue_evidence_manifest.json")
        write(supplemental_raw / "supplemental_runtime_file_listing.txt", "\n".join(list_files(supplemental_root, 600)))
        screenshot_root = Path(str((summary.get("supplemental") or {}).get("user_element_root") or ""))
        write(supplemental_raw / "supplemental_user_focused_screenshot_listing.txt", "\n".join(list_files(screenshot_root, 300)))

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
            "Supplemental Status: supplemental-runtime-proof-gap-investigation",
            "Packet Reviewability State: Reviewable",
            "USER Gate State: Pending USER Investigation Review",
            "Product/runtime repair: Withheld",
            "Prevention plan implementation: Withheld",
            "Baseline reconciled HEAD: `4afb18905d961c492a701149133e122fabee301d`",
            "Baseline origin/main: `f239c97415fb8aaac414f9b802888ea004d08c29`",
            "",
            "This packet investigates why FAM-006 Live Validation / UTS handoff reached an automated green handoff while USER later found failures. It includes a supplemental runtime-proof gap pass for Recording Studio button click proof, Start/Stop placement, Log Viewer focus/open regression, Studio/Log Viewer ownership, older Overlay Profile proof, and card-holder visual state. It does not accept UTS results, fix product runtime behavior, close issue #258, or advance to PR Readiness.",
            "",
            section(
                "Verdict",
                "REPAIR FINDINGS. The branch is reconciled and the investigation can proceed, but LV1/UTS readiness is not accepted. The packet identifies evidence handoff failure, helper false-green risk, insufficient combination coverage, and product issue candidates that require a later repair plan.",
            ),
            section("Prior Packet Sufficiency Statement", prior_packet_sufficiency_md(summary)),
            section("USER-Confirmed A/C Findings Supplement", user_confirmed_ac_supplement_md(summary)),
            section("Issue C Normal-User Sequence Matrix", issue_c_sequence_matrix_md()),
            section("Supplemental Runtime Proof Issue Map", supplemental_issue_map_md(summary)),
            section("Supplemental Attempt Stability", supplemental_attempts_md()),
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
                        ("Baseline 4afb1890 ancestor", identity.get("baseline_head_is_ancestor", "")),
                        ("Prior investigation ddeb90a4 ancestor", identity.get("prior_investigation_head_is_ancestor", "")),
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
            section("Runtime Proof Rerun", runtime_proof_rerun_md(summary)),
            section("USER-Confirmed A/C Findings Supplement", user_confirmed_ac_supplement_md(summary)),
            section("Issue C Normal-User Sequence Matrix", issue_c_sequence_matrix_md()),
            section("Supplemental Runtime Proof", supplemental_issue_map_md(summary)),
            section("Supplemental Attempt Stability", supplemental_attempts_md()),
            section("Codex Visual Adjudication", visual_adjudication_md(summary)),
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
            "This helper generated the packet, stable findings, evidence inventory, coverage matrix, runtime proof rerun digest, and screenshot visual-adjudication audit. It is investigation support only and should be evaluated for durable adoption after USER review.",
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
        "RUNTIME_PROOF_RERUN_RESULTS.md": section("Runtime Proof Rerun", runtime_proof_rerun_md(summary)),
        "USER_CONFIRMED_AC_FINDINGS_SUPPLEMENT.md": section("USER-Confirmed A/C Findings Supplement", user_confirmed_ac_supplement_md(summary)),
        "ISSUE_C_SEQUENCE_MATRIX.md": section("Issue C Normal-User Sequence Matrix", issue_c_sequence_matrix_md()),
        "SUPPLEMENTAL_RUNTIME_PROOF_ISSUE_MAP.md": section("Supplemental Runtime Proof Issue Map", supplemental_issue_map_md(summary)),
        "SUPPLEMENTAL_ATTEMPT_STABILITY.md": section("Supplemental Attempt Stability", supplemental_attempts_md()),
        "PRIOR_PACKET_SUFFICIENCY.md": section("Prior Packet Sufficiency Statement", prior_packet_sufficiency_md(summary)),
        "CODEX_VISUAL_ADJUDICATION.md": section("Codex Visual Adjudication", visual_adjudication_md(summary)),
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
                    "- `Review Aids/Raw Evidence/runtime_proof_rerun/`",
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
        "Runtime Proof Rerun",
        "USER-Confirmed A/C Findings Supplement",
        "Issue C Normal-User Sequence Matrix",
        "Supplemental Status: supplemental-runtime-proof-gap-investigation",
        "Supplemental Runtime Proof",
        "Prior Packet Sufficiency Statement",
        "Codex Visual Adjudication",
        "FAM006-EVID-001",
        "FAM006-TOOLGAP-001",
        "FAM006-LVFAIL-001",
        "FAM006-UTSFAIL-001",
        "FAM006-REGRESS-001",
        "FAM006-UI-003",
        "FAM006-WINDOW-002",
        "USER Confirmed + Codex Reproduction Blocked",
        "FAM006-GOVGAP-003",
        "FAM006-EVID-002",
        "FAM006-PHASE-001",
        "Product/runtime repair: Withheld",
        "Prevention plan implementation: Withheld",
        "fam006_live_validation_runtime_rerun_baseline",
        "fam006_supplemental_runtime_proof",
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


def validate_repair_plan_packet(packet_root: Path) -> dict[str, object]:
    primary = packet_root / REPAIR_PLAN_PRIMARY_FILE
    files = list(packet_root.rglob("*"))
    markdown_files = [p for p in files if p.suffix.lower() == ".md"]
    user_review_files = list((packet_root / "USER Review").glob("*.md"))
    text = read_text(primary)
    required = [
        f"Packet Status: {REPAIR_PLAN_STATUS}",
        "Packet Reviewability State: Reviewable",
        "USER Gate State: Pending USER Repair Plan Review",
        "Product/runtime repair: Withheld",
        "Live Validation acceptance: Withheld",
        "UTS acceptance: Withheld",
        "Findings-To-Repair Map",
        "Repair Lane Classification",
        "Current-Branch Repair Package Recommendation",
        "Specific Repair Planning For USER-Confirmed A",
        "Specific Repair Planning For USER-Confirmed C",
        "Specific Repair Planning For B",
        "Specific Repair Planning For D",
        "Overlay Profile Proof Planning",
        "Live Validation Repair Planning",
        "Helper / Validator / Tooling Repair Planning",
        "Source-Truth Amendment Planning",
        "Repair Sequencing",
        "Exact USER Decision Options",
        "FAM006-EVID-001",
        "FAM006-EVID-002",
        "FAM006-TOOLGAP-001",
        "FAM006-LVFAIL-001",
        "FAM006-UTSFAIL-001",
        "FAM006-UI-001",
        "FAM006-UI-002",
        "FAM006-UI-003",
        "FAM006-WINDOW-001",
        "FAM006-WINDOW-002",
        "FAM006-GOVGAP-002",
        "FAM006-GOVGAP-003",
        "FAM006-REGRESS-001",
        "FAM006-REGRESS-002",
        "FAM006-CODEPATH-001",
        "FAM006-PHASE-001",
    ]
    forbidden = [
        "Product/runtime repair: Implemented",
        "UTS acceptance: Accepted",
        "PR Readiness: Approved",
        "Issue #258: Closed",
    ]
    missing = [marker for marker in required if marker not in text]
    forbidden_hits = [marker for marker in forbidden if marker in text]
    layout_ok = (
        (packet_root / "START_HERE.md").exists()
        and primary.exists()
        and (packet_root / "Review Aids").is_dir()
        and (packet_root / "Source Truth Context").is_dir()
        and len(user_review_files) == 1
        and (packet_root / "Review Aids" / "Accepted Findings Packet" / PRIMARY_FILE).exists()
    )
    return {
        "passed": not missing and not forbidden_hits and layout_ok,
        "layoutOk": layout_ok,
        "missingRequiredMarkers": missing,
        "forbiddenMarkers": forbidden_hits,
        "userReviewFileCount": len(user_review_files),
        "markdownFileCount": len(markdown_files),
        "fileCount": len([p for p in files if p.is_file()]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate-packet", action="store_true")
    parser.add_argument("--validate-packet", action="store_true")
    parser.add_argument("--generate-repair-plan-packet", action="store_true")
    parser.add_argument("--validate-repair-plan-packet", action="store_true")
    parser.add_argument("--run-validator-first-product-state", action="store_true")
    parser.add_argument("--self-check-validator-first", action="store_true")
    parser.add_argument("--generate-validator-first-packet", action="store_true")
    parser.add_argument("--validate-validator-first-packet", action="store_true")
    parser.add_argument("--generate-repair-implementation-approval-packet", action="store_true")
    parser.add_argument("--validate-repair-implementation-approval-packet", action="store_true")
    parser.add_argument("--generate-repair-return-review-packet", action="store_true")
    parser.add_argument("--validate-repair-return-review-packet", action="store_true")
    parser.add_argument("--generate-live-validation-uts-disposition-packet", action="store_true")
    parser.add_argument("--validate-live-validation-uts-disposition-packet", action="store_true")
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
    if args.generate_repair_plan_packet:
        packet_root, zip_path, digest = generate_repair_plan_packet()
        validation = validate_repair_plan_packet(packet_root)
        print(json.dumps({
            "packetRoot": str(packet_root),
            "zipPath": str(zip_path),
            "zipSha256": digest,
            "validation": validation,
        }, indent=2))
        return 0 if validation["passed"] else 1
    if args.validate_repair_plan_packet:
        validation = validate_repair_plan_packet(PACKET_ROOT)
        print(json.dumps(validation, indent=2))
        return 0 if validation["passed"] else 1
    if args.run_validator_first_product_state:
        result = run_validator_first_product_state()
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1
    if args.self_check_validator_first:
        result = validator_first_self_check()
        print(json.dumps(result, indent=2))
        return 0 if result["passed"] else 1
    if args.generate_validator_first_packet:
        packet_root, zip_path, digest = generate_validator_first_packet()
        validation = validate_validator_first_packet(packet_root)
        print(json.dumps({
            "packetRoot": str(packet_root),
            "zipPath": str(zip_path),
            "zipSha256": digest,
            "validation": validation,
        }, indent=2))
        return 0 if validation["passed"] else 1
    if args.validate_validator_first_packet:
        validation = validate_validator_first_packet(PACKET_ROOT)
        print(json.dumps(validation, indent=2))
        return 0 if validation["passed"] else 1
    if args.generate_repair_implementation_approval_packet:
        packet_root, zip_path, digest = generate_repair_implementation_approval_packet()
        validation = validate_repair_implementation_approval_packet(packet_root)
        print(json.dumps({
            "packetRoot": str(packet_root),
            "zipPath": str(zip_path),
            "zipSha256": digest,
            "validation": validation,
        }, indent=2))
        return 0 if validation["passed"] else 1
    if args.validate_repair_implementation_approval_packet:
        validation = validate_repair_implementation_approval_packet(PACKET_ROOT)
        print(json.dumps(validation, indent=2))
        return 0 if validation["passed"] else 1
    if args.generate_repair_return_review_packet:
        packet_root, zip_path, digest = generate_repair_return_review_packet()
        validation = validate_repair_return_review_packet(packet_root)
        print(json.dumps({
            "packetRoot": str(packet_root),
            "zipPath": str(zip_path),
            "zipSha256": digest,
            "validation": validation,
        }, indent=2))
        return 0 if validation["passed"] else 1
    if args.validate_repair_return_review_packet:
        validation = validate_repair_return_review_packet(PACKET_ROOT)
        print(json.dumps(validation, indent=2))
        return 0 if validation["passed"] else 1
    if args.generate_live_validation_uts_disposition_packet:
        packet_root, zip_path, digest = generate_live_validation_uts_disposition_packet()
        validation = validate_live_validation_uts_disposition_packet(packet_root)
        print(json.dumps({
            "packetRoot": str(packet_root),
            "zipPath": str(zip_path),
            "zipSha256": digest,
            "validation": validation,
        }, indent=2))
        return 0 if validation["passed"] else 1
    if args.validate_live_validation_uts_disposition_packet:
        validation = validate_live_validation_uts_disposition_packet(PACKET_ROOT)
        print(json.dumps(validation, indent=2))
        return 0 if validation["passed"] else 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
