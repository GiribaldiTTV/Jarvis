"""FAM-003 LV1 real-live validation gate.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 Settings resize proof / Option C Live Validation
Reason Reusable Helper Was Not Extended: The existing reusable desktop
    entrypoint validator and FAM-003 proof helpers produce strong supporting
    evidence, but none owns the FAM-003 LV1 gate that separates automated
    support, Codex live-client evidence, USER-operated UTS evidence, and final
    LV1 status for this branch.
Consolidation Target: Future reusable desktop LV1 proof-class orchestrator
    after multiple FAM branches need the same normal-launcher plus visible
    control-surface gate.
Promotion Decision Point: Before PR Readiness for this branch.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_lv1_real_live_validation"
SETTINGS_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_settings_repair_visual_validation"
OPTION_C_LOG_ROOT = ROOT / "dev" / "logs" / "fam003_option_c_workstream_proof"
DESKTOP_ENTRYPOINT_LOG_ROOT = ROOT / "dev" / "logs" / "desktop_entrypoint_validation"
DESKTOP_ENTRYPOINT_REPORT_ROOT = DESKTOP_ENTRYPOINT_LOG_ROOT / "reports"
REAL_CLIENT_TRAY_MANIFEST = (
    DESKTOP_ENTRYPOINT_LOG_ROOT
    / "real_client_tray_shortcut"
    / "real_client_tray_precheck_manifest.json"
)
NORMAL_WORKTREE_LAUNCHER = ROOT / "Nexus Desktop Launcher - FAM-003.lnk"
UTS_PATH = Path(r"C:\Nexus USER\UTS - FAM-003.txt")


def _run(command: list[str], *, timeout: int = 480, normal_qt_platform: bool = False) -> dict[str, object]:
    env = os.environ.copy()
    if normal_qt_platform:
        env.pop("QT_QPA_PLATFORM", None)
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def _git_value(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True)
    return proc.stdout.strip()


def _latest_dir(root: Path) -> Path | None:
    if not root.exists():
        return None
    dirs = [path for path in root.iterdir() if path.is_dir()]
    if not dirs:
        return None
    return max(dirs, key=lambda path: path.stat().st_mtime)


def _latest_file(root: Path, pattern: str) -> Path | None:
    if not root.exists():
        return None
    files = [path for path in root.glob(pattern) if path.is_file()]
    if not files:
        return None
    return max(files, key=lambda path: path.stat().st_mtime)


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_if_exists(source: Path | None, target_dir: Path, copied: list[dict[str, str]]) -> Path | None:
    if source is None or not source.exists() or not source.is_file():
        return None
    target = target_dir / source.name
    shutil.copy2(source, target)
    copied.append({"source": str(source), "packetArtifact": str(target), "name": target.name})
    return target


def _copy_key_artifacts(log_dir: Path) -> tuple[list[dict[str, str]], list[str]]:
    artifacts_dir = log_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, str]] = []
    missing: list[str] = []

    settings_dir = _latest_dir(SETTINGS_LOG_ROOT)
    option_dir = _latest_dir(OPTION_C_LOG_ROOT)
    desktop_report = _latest_file(DESKTOP_ENTRYPOINT_REPORT_ROOT, "DesktopEntrypointValidationReport_*.txt")

    for label, directory, names in (
        (
            "settings",
            settings_dir,
            (
                "01_default_global_settings_shell.png",
                "03b_window_resized.png",
                "03c_window_minimum_size.png",
                "04d_left_pane_compressed_horizontal_overflow.png",
                "07_dropdown_list_state.png",
                "08_close_guard.png",
                "16_defect_closure_contact_sheet.png",
            ),
        ),
        (
            "option_c",
            option_dir,
            (
                "00_option_c_workstream_contact_sheet.png",
                "01_tray_styled_popup_focused.png",
                "02_tray_popup_route_after_reopen.png",
                "10_ncp_entry_typed_request.png",
                "11_ncp_choose_visible_choices.png",
                "12_ncp_confirm_selected_action.png",
                "13_ncp_result_launch_requested.png",
            ),
        ),
    ):
        if directory is None:
            missing.append(f"{label} latest proof directory missing")
            continue
        for name in names:
            target = _copy_if_exists(directory / name, artifacts_dir, copied)
            if target is None:
                missing.append(f"{label} artifact missing: {name}")

    if _copy_if_exists(desktop_report, artifacts_dir, copied) is None:
        missing.append("desktop entrypoint latest report missing")
    if _copy_if_exists(REAL_CLIENT_TRAY_MANIFEST, artifacts_dir, copied) is None:
        missing.append("desktop real-client tray precheck manifest missing")

    return copied, missing


def _write_run_report(log_dir: Path, name: str, result: dict[str, object]) -> Path:
    report = log_dir / f"{name}.txt"
    report.write_text(
        "COMMAND: "
        + " ".join(str(part) for part in result["command"])
        + "\nRETURN CODE: "
        + str(result["returncode"])
        + "\n\nSTDOUT:\n"
        + str(result["stdout"])
        + "\n\nSTDERR:\n"
        + str(result["stderr"])
        + "\n",
        encoding="utf-8",
    )
    return report


def _uts_status() -> str:
    if not UTS_PATH.exists():
        return "MISSING"
    text = UTS_PATH.read_text(encoding="utf-8", errors="replace")
    if "Final USER Result: PASS" in text:
        return "PASS_RETURNED_NOT_DIGESTED_BY_THIS_HELPER"
    if "Final USER Result: FAIL" in text:
        return "FAIL_RETURNED_NOT_DIGESTED_BY_THIS_HELPER"
    if "Final USER Result: WAIVED" in text:
        return "WAIVED_RETURNED_NOT_DIGESTED_BY_THIS_HELPER"
    return "PENDING"


def _make_status_rows(
    *,
    run_results: dict[str, dict[str, object]],
    real_client_manifest: dict[str, object],
    missing_artifacts: list[str],
) -> list[dict[str, object]]:
    proof_classes = real_client_manifest.get("proofClasses") if isinstance(real_client_manifest, dict) else {}
    steps = real_client_manifest.get("steps") if isinstance(real_client_manifest, dict) else []
    real_user_tray = proof_classes.get("realUserOperatedTrayProof") if isinstance(proof_classes, dict) else None
    fake_model = proof_classes.get("fakeOffscreenModelProof") if isinstance(proof_classes, dict) else None
    all_supporting_green = all(result["ok"] for result in run_results.values()) and not missing_artifacts
    precheck_steps_green = bool(steps) and all(step.get("codexPrecheck") == "PASS" for step in steps)
    real_tray_complete = real_user_tray not in {None, "", "USER_LV1_REQUIRED"}

    return [
        {
            "id": "automated_supporting_evidence",
            "status": "PASS" if all_supporting_green else "FAIL",
            "basis": "settings visual, Option C proof, and desktop-entrypoint helper commands completed and key artifacts were copied",
        },
        {
            "id": "normal_launcher_supporting_precheck",
            "status": "PASS" if precheck_steps_green else "FAIL",
            "basis": str(REAL_CLIENT_TRAY_MANIFEST),
        },
        {
            "id": "fake_or_offscreen_proof_class",
            "status": "SUPPORTING_ONLY",
            "basis": fake_model or "not reported",
        },
        {
            "id": "codex_operated_visible_tray_control_surface",
            "status": "PASS" if real_tray_complete else "BLOCKED",
            "basis": real_user_tray or "missing realUserOperatedTrayProof field",
            "requiredBeforeUts": True,
        },
        {
            "id": "settings_transient_interaction_frame_sequence",
            "status": "PARTIAL_SUPPORTING_ONLY",
            "basis": "focused settings screenshots copied; no normal-launcher visible frame sequence produced by the existing helper family",
            "requiredBeforeUts": True,
        },
        {
            "id": "ncp_interaction_frame_sequence",
            "status": "PARTIAL_SUPPORTING_ONLY",
            "basis": "NCP typed/choose/confirm/result screenshots copied; no normal-launcher visible input frame sequence produced by the existing helper family",
            "requiredBeforeUts": True,
        },
    ]


def main() -> int:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = LOG_ROOT / stamp
    log_dir.mkdir(parents=True, exist_ok=True)

    head = _git_value("rev-parse", "HEAD")
    origin_main = _git_value("rev-parse", "origin/main")
    merge_base = _git_value("merge-base", "HEAD", "origin/main")
    branch = _git_value("branch", "--show-current")
    upstream = _git_value("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")

    runs = {
        "settings_visual": _run([sys.executable, "dev/orin_fam003_settings_repair_visual_validation.py"], timeout=360, normal_qt_platform=True),
        "desktop_entrypoint": _run([sys.executable, "dev/orin_desktop_entrypoint_validation.py"], timeout=540, normal_qt_platform=True),
        "option_c_workstream_proof": _run([sys.executable, "dev/orin_fam003_option_c_workstream_proof_validation.py"], timeout=720, normal_qt_platform=True),
    }
    run_reports = {name: str(_write_run_report(log_dir, name, result)) for name, result in runs.items()}
    copied_artifacts, missing_artifacts = _copy_key_artifacts(log_dir)
    real_client_manifest = _read_json(REAL_CLIENT_TRAY_MANIFEST)
    status_rows = _make_status_rows(
        run_results=runs,
        real_client_manifest=real_client_manifest,
        missing_artifacts=missing_artifacts,
    )
    blocking_rows = [
        row
        for row in status_rows
        if row.get("requiredBeforeUts") is True and row.get("status") != "PASS"
    ]
    helper_status = "BLOCKED" if blocking_rows else "PASS_READY_FOR_USER_UTS"
    final_lv1 = "BLOCKED_NOT_GREEN" if blocking_rows or _uts_status() == "PENDING" else "PENDING_UTS_DIGEST"

    manifest = {
        "status": helper_status,
        "timestamp": stamp,
        "worktree": str(ROOT),
        "branch": branch,
        "head": head,
        "originMain": origin_main,
        "mergeBase": merge_base,
        "upstream": upstream,
        "normalWorktreeLauncher": str(NORMAL_WORKTREE_LAUNCHER),
        "normalWorktreeLauncherExists": NORMAL_WORKTREE_LAUNCHER.exists(),
        "desktopShortcutRealClientTrayManifest": str(REAL_CLIENT_TRAY_MANIFEST),
        "runReports": run_reports,
        "copiedArtifacts": copied_artifacts,
        "missingArtifacts": missing_artifacts,
        "statusRows": status_rows,
        "blockingRows": blocking_rows,
        "utsPath": str(UTS_PATH),
        "utsStatus": _uts_status(),
        "finalLv1Status": final_lv1,
        "proofClassPolicy": {
            "automatedSupportingEvidence": "evidence-only",
            "codexExecutedLiveEvidence": "must include visible user-level control-surface proof before UTS handoff",
            "userOperatedUtsEvidence": "downstream of real LV helper evidence",
            "finalLv1": "not green while UTS or required real live evidence is pending",
        },
    }
    manifest_path = log_dir / "fam003_lv1_real_live_validation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    matrix = log_dir / "FAM003_LV1_REAL_LIVE_VALIDATION.md"
    lines = [
        "# FAM-003 LV1 Real Live Validation",
        "",
        f"Status: `{helper_status}`",
        f"Final LV1 Status: `{final_lv1}`",
        f"Source Repo HEAD: `{head}`",
        f"Source origin/main: `{origin_main}`",
        f"Merge Base: `{merge_base}`",
        f"Proof Root: `{log_dir}`",
        "",
        "## Result Matrix",
        "",
        "| Evidence Class | Status | Basis |",
        "| --- | --- | --- |",
    ]
    for row in status_rows:
        lines.append(f"| `{row['id']}` | `{row['status']}` | {row['basis']} |")
    lines.extend(
        [
            "",
            "## Gate Disposition",
            "",
            "- UTS-first handoff is superseded for this run.",
            "- UTS remains downstream of real LV helper evidence and is not marked complete here.",
            "- Product/runtime repair, issue mutation, PR readiness, merge, release, and cleanup were not performed.",
        ]
    )
    if blocking_rows:
        lines.extend(["", "## Blocking Rows", ""])
        for row in blocking_rows:
            lines.append(f"- `{row['id']}`: `{row['status']}` - {row['basis']}")
    matrix.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"FAM-003 LV1 REAL LIVE VALIDATION: {helper_status}")
    print(f"Proof Root: {log_dir}")
    print(f"Manifest: {manifest_path}")
    print(f"Matrix: {matrix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
