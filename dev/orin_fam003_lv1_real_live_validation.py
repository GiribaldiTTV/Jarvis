"""Fail-closed FAM-003 LV1 adjudicator for external visible human-client proof.

The helper never launches the product, invokes product handlers, or injects
validation environment variables. The formal interaction producer is
``dev/orin_fam003_human_client_live_validation.ps1``. This module validates its
current pushed-HEAD manifest and keeps UTS NOT_REQUESTED until every required
pre-UTS row is genuinely green.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_lv1_real_live_validation"
HUMAN_CLIENT_ROOT = ROOT / "dev" / "logs" / "fam003_human_client_live_validation"
HUMAN_CLIENT_LATEST = HUMAN_CLIENT_ROOT / "latest_manifest.json"
FORMAL_USER_LAUNCHER = Path.home() / "OneDrive" / "Desktop" / "Nexus Desktop Launcher.lnk"
REQUIRED_STEP_IDS = (
    "formal_launcher_provenance",
    "visible_exact_launcher_activation",
    "runtime_process_provenance",
    "tray_compact_hierarchy",
    "hud_dashboard_resident_doorway",
    "settings_visible_route_and_live_resize",
    "ncp_visible_keyboard_flow",
)


def _git_value(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _run(command: list[str], timeout: int = 480) -> dict[str, object]:
    result = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, timeout=timeout
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "ok": result.returncode == 0,
    }


def _step_map(manifest: dict[str, object]) -> dict[str, dict[str, object]]:
    steps = manifest.get("steps")
    if not isinstance(steps, list):
        return {}
    return {
        str(step.get("id")): step
        for step in steps
        if isinstance(step, dict) and step.get("id")
    }


def _normalized_path(value: object) -> str:
    try:
        return str(Path(str(value)).resolve()).casefold()
    except Exception:
        return str(value or "").casefold()


def adjudicate_human_client_manifest(
    manifest: dict[str, object], *, current_head: str
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return status rows and blockers without permitting substitute evidence."""

    steps = _step_map(manifest)
    rows: list[dict[str, str]] = []

    def add(row_id: str, passed: bool, basis: str) -> None:
        rows.append({"id": row_id, "status": "PASS" if passed else "BLOCKED", "basis": basis})

    add(
        "human_client_child_status",
        manifest.get("status") == "PASS",
        f"childStatus={manifest.get('status') or 'missing'}",
    )
    add(
        "pushed_head_provenance",
        str(manifest.get("head") or "") == current_head,
        f"childHead={manifest.get('head') or 'missing'}; currentHead={current_head}",
    )
    launcher_path = manifest.get("formalLauncherPath")
    add(
        "exact_user_desktop_launcher",
        _normalized_path(launcher_path) == _normalized_path(FORMAL_USER_LAUNCHER),
        f"required={FORMAL_USER_LAUNCHER}; observed={launcher_path or 'missing'}",
    )
    add(
        "visible_launcher_activation",
        manifest.get("launcherActivationMethod")
        == "visible-windows-desktop-icon-pointer-double-click",
        f"activation={manifest.get('launcherActivationMethod') or 'missing'}",
    )
    add(
        "no_runtime_proof_bypass",
        manifest.get("directHandlerBypass") is False
        and manifest.get("environmentInjectedRuntimeProof") is False,
        "directHandlerBypass and environmentInjectedRuntimeProof must both be false",
    )

    for required_id in REQUIRED_STEP_IDS:
        step = steps.get(required_id, {})
        add(
            f"required_step_{required_id}",
            step.get("status") == "PASS" and step.get("codexPrecheck") == "PASS",
            f"status={step.get('status') or 'missing'}; codexPrecheck={step.get('codexPrecheck') or 'missing'}",
        )

    settings = steps.get("settings_visible_route_and_live_resize", {})
    settings_evidence = settings.get("evidence") if isinstance(settings, dict) else {}
    add(
        "visible_control_at_input",
        isinstance(settings_evidence, dict)
        and settings_evidence.get("buttonVisibleAtInput") is True,
        f"buttonVisibleAtInput={(settings_evidence or {}).get('buttonVisibleAtInput') if isinstance(settings_evidence, dict) else 'missing'}",
    )

    hud = steps.get("hud_dashboard_resident_doorway", {})
    hud_evidence = hud.get("evidence") if isinstance(hud, dict) else {}
    external_state = (
        str(hud_evidence.get("externalParentLauncherState") or "")
        if isinstance(hud_evidence, dict)
        else ""
    )
    add(
        "resident_doorway_target_not_dead",
        hud.get("status") == "PASS"
        and external_state not in {"", "dead", "stale", "route-child-missing", "not-exercisable-while-user-disabled"},
        f"hudStatus={hud.get('status') or 'missing'}; externalParentLauncherState={external_state or 'missing'}",
    )

    tray = steps.get("tray_compact_hierarchy", {})
    tray_evidence = tray.get("evidence") if isinstance(tray, dict) else {}
    add(
        "tray_no_direct_handler_bypass",
        isinstance(tray_evidence, dict) and tray_evidence.get("usedDirectHandler") is False,
        f"usedDirectHandler={(tray_evidence or {}).get('usedDirectHandler') if isinstance(tray_evidence, dict) else 'missing'}",
    )
    add(
        "ordered_visual_evidence",
        int(manifest.get("orderedFrameCount") or 0) >= 8,
        f"orderedFrameCount={int(manifest.get('orderedFrameCount') or 0)}",
    )

    blockers = [row for row in rows if row["status"] != "PASS"]
    return rows, blockers


def run_negative_fixtures() -> list[dict[str, str]]:
    """Prove each known false-green defect changes the aggregate to BLOCKED."""

    head = "fixture-head"
    base = {
        "status": "PASS",
        "head": head,
        "formalLauncherPath": str(FORMAL_USER_LAUNCHER),
        "launcherActivationMethod": "visible-windows-desktop-icon-pointer-double-click",
        "directHandlerBypass": False,
        "environmentInjectedRuntimeProof": False,
        "orderedFrameCount": 12,
        "steps": [
            {
                "id": step_id,
                "status": "PASS",
                "codexPrecheck": "PASS",
                "evidence": {
                    "buttonVisibleAtInput": True,
                    "usedDirectHandler": False,
                    "externalParentLauncherState": "visible-route-activated",
                },
            }
            for step_id in REQUIRED_STEP_IDS
        ],
    }

    fixtures: list[tuple[str, dict[str, object]]] = []
    child_fail = copy.deepcopy(base)
    child_fail["status"] = "FAIL"
    fixtures.append(("child_fail_blocks", child_fail))

    precheck_fail = copy.deepcopy(base)
    _step_map(precheck_fail)["settings_visible_route_and_live_resize"]["codexPrecheck"] = "FAIL"
    fixtures.append(("codex_precheck_fail_blocks", precheck_fail))

    hidden_button = copy.deepcopy(base)
    _step_map(hidden_button)["settings_visible_route_and_live_resize"]["evidence"]["buttonVisibleAtInput"] = False
    fixtures.append(("hidden_button_blocks", hidden_button))

    wrong_launcher = copy.deepcopy(base)
    wrong_launcher["formalLauncherPath"] = str(ROOT / "Nexus Desktop Launcher - FAM-003.lnk")
    fixtures.append(("invalid_launcher_blocks", wrong_launcher))

    explorer_activation = copy.deepcopy(base)
    explorer_activation["launcherActivationMethod"] = "visible-file-explorer-selected-item-double-click"
    fixtures.append(("file_explorer_launcher_fallback_blocks", explorer_activation))

    missing_hud = copy.deepcopy(base)
    missing_hud["steps"] = [step for step in missing_hud["steps"] if step["id"] != "hud_dashboard_resident_doorway"]
    fixtures.append(("missing_doorway_blocks", missing_hud))

    dead_target = copy.deepcopy(base)
    _step_map(dead_target)["hud_dashboard_resident_doorway"]["evidence"]["externalParentLauncherState"] = "dead"
    fixtures.append(("dead_external_target_blocks", dead_target))

    bypass = copy.deepcopy(base)
    bypass["directHandlerBypass"] = True
    fixtures.append(("direct_handler_bypass_blocks", bypass))

    results: list[dict[str, str]] = []
    for fixture_id, payload in fixtures:
        _, blockers = adjudicate_human_client_manifest(payload, current_head=head)
        results.append(
            {
                "id": fixture_id,
                "status": "PASS" if blockers else "FAIL",
                "basis": f"blockingRows={len(blockers)}",
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    negative_results = run_negative_fixtures()
    if args.self_test:
        failed = [row for row in negative_results if row["status"] != "PASS"]
        print(json.dumps({"status": "PASS" if not failed else "FAIL", "fixtures": negative_results}, indent=2))
        return 1 if failed else 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    proof_root = LOG_ROOT / stamp
    artifacts_root = proof_root / "artifacts"
    artifacts_root.mkdir(parents=True, exist_ok=True)
    head = _git_value("rev-parse", "HEAD")

    supporting_runs = {
        "resident_access": _run([sys.executable, "dev/orin_fam003_resident_access_validation.py"]),
        "settings_visual": _run([sys.executable, "dev/orin_fam003_settings_repair_visual_validation.py"]),
    }
    human_manifest = _read_json(HUMAN_CLIENT_LATEST)
    rows, blockers = adjudicate_human_client_manifest(human_manifest, current_head=head)
    for name, result in supporting_runs.items():
        rows.append(
            {
                "id": f"supporting_{name}",
                "status": "PASS" if result["ok"] else "BLOCKED",
                "basis": f"returncode={result['returncode']}",
            }
        )
        if not result["ok"]:
            blockers.append(rows[-1])
        (proof_root / f"{name}.txt").write_text(
            f"COMMAND: {' '.join(result['command'])}\nRETURN CODE: {result['returncode']}\n\nSTDOUT:\n{result['stdout']}\n\nSTDERR:\n{result['stderr']}\n",
            encoding="utf-8",
        )

    for frame in human_manifest.get("orderedFrames") or []:
        if not isinstance(frame, dict):
            continue
        source = Path(str(frame.get("path") or ""))
        if source.exists() and source.is_file():
            shutil.copy2(source, artifacts_root / source.name)
    if HUMAN_CLIENT_LATEST.exists():
        shutil.copy2(HUMAN_CLIENT_LATEST, artifacts_root / HUMAN_CLIENT_LATEST.name)

    status = "BLOCKED_BEFORE_UTS" if blockers else "PASS_PRE_UTS_GATE"
    manifest = {
        "schema": "fam003-lv1-fail-closed-adjudication-v2",
        "status": status,
        "timestamp": stamp,
        "worktree": str(ROOT),
        "branch": _git_value("branch", "--show-current"),
        "head": head,
        "originMain": _git_value("rev-parse", "origin/main"),
        "mergeBase": _git_value("merge-base", "HEAD", "origin/main"),
        "upstream": _git_value("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"),
        "formalUserLauncher": str(FORMAL_USER_LAUNCHER),
        "humanClientManifest": str(HUMAN_CLIENT_LATEST),
        "humanClient": human_manifest,
        "statusRows": rows,
        "blockingRows": blockers,
        "negativeFalseGreenFixtures": negative_results,
        "utsStatus": "NOT_REQUESTED",
        "finalLv1Status": "BLOCKED_NOT_GREEN" if blockers else "PRE_UTS_GATE_GREEN_UTS_NOT_REQUESTED",
        "proofPolicy": {
            "runtimeEnvHooks": "supporting-only-not-consumed",
            "directHandlers": "forbidden",
            "formalLauncher": "exact USER Desktop shortcut via visible Windows Desktop icon and pointer double-click",
        },
    }
    manifest_path = proof_root / "fam003_lv1_real_live_validation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = proof_root / "FAM003_LV1_REAL_LIVE_VALIDATION.md"
    lines = [
        "# FAM-003 LV1 Real Live Validation",
        "",
        f"Status: `{status}`",
        f"UTS Status: `NOT_REQUESTED`",
        f"Pushed-HEAD Candidate: `{head}`",
        f"Proof Root: `{proof_root}`",
        "",
        "| Evidence | Status | Basis |",
        "| --- | --- | --- |",
    ]
    lines.extend(f"| `{row['id']}` | `{row['status']}` | {row['basis']} |" for row in rows)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"FAM-003 LV1 REAL LIVE VALIDATION: {status}")
    print(f"Proof Root: {proof_root}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
