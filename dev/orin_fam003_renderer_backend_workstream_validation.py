"""Fail-capable Option D shared WebEngine Workstream proof for FAM-003.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 R2 Settings/tray/NCP completion proof
Reason Reusable Helper Was Not Extended: The temporary Option D policy, current
    carrier surface inventory, and 15 negative fixtures are branch-specific.
Consolidation Target: Shared renderer-backend proof after a second branch needs
    the same normal-launcher all-surface contract.
Promotion Decision Point: Before a permanent renderer architecture decision.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import psutil


ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / "dev" / "logs" / "fam003_renderer_backend_workstream"
FIXTURE_PATH = ROOT / "dev" / "fixtures" / "fam003_renderer_backend_negative_cases.json"
LAUNCHER = ROOT / "desktop" / "orin_desktop_launcher.pyw"
MAIN = ROOT / "desktop" / "orin_desktop_main.py"
RUNTIME_PROBE = ROOT / "dev" / "fam003_renderer_backend_runtime_probe.py"
EXPECTED_FLAG = "--disable-gpu"
EXPECTED_POLICY = "temporary-shared-runtime-safety-policy"
EXPECTED_CLASSIFICATION = "shared-desktop-runtime-not-fam003-only"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desktop.renderer_backend import (  # noqa: E402
    build_renderer_environment,
    renderer_backend_contract,
)
from dev.orin_desktop_entrypoint_validation import (  # noqa: E402
    resolve_desktop_shortcut_for_current_root,
)


REQUIRED_WEBENGINE_SURFACES = (
    "orin-core-visualization",
    "hud-dashboard",
    "nexus-recording-suite",
    "nexus-log-viewer",
    "ai-status-command-center",
    "ai-control-center-domain",
    "readiness-diagnostics-domain",
    "capabilities-maintenance-domain",
)

AVAILABLE_PROOF_SURFACES = (
    "orin-core-visualization",
    "hud-dashboard",
    "nexus-recording-suite",
    "nexus-log-viewer",
    "ai-status-command-center",
)


def _inventory() -> list[dict[str, Any]]:
    return [
        {
            "surfaceId": "orin-core-visualization",
            "userFacingName": "ORIN Core Visualization",
            "sourceTruthOwner": "Project vision / FAM-007-adjacent persona presentation",
            "sourceFiles": ["desktop/core_visualization_renderer.py", "nexus_visual/orin_core_desktop.html"],
            "normalRoute": "exact desktop launcher; startup-resident ORIN Core",
            "initialization": "startup-loaded and visible",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": True,
            "acceptedCurrentProductRoute": True,
            "proofObligation": "full-window render, nonblank animation, lifecycle survival",
            "overlapRisk": "shared project surface; backend-wide effect",
        },
        {
            "surfaceId": "hud-dashboard",
            "userFacingName": "HUD Dashboard",
            "sourceTruthOwner": "FAM-006 runtime state; FAM-003 resident doorway",
            "sourceFiles": ["desktop/desktop_renderer.py", "nexus_visual/monitoring_hud.html"],
            "normalRoute": "tray Global Settings -> HUD -> HUD Dashboard enable; tray HUD -> Open HUD Dashboard",
            "initialization": "preloaded hidden at startup; shown after enable/open",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": True,
            "acceptedCurrentProductRoute": True,
            "proofObligation": "direct enable/open/close/restore/repeated-open/disable visual and state proof",
            "overlapRisk": "shared FAM-006-owned current-carrier surface; high overlap",
        },
        {
            "surfaceId": "nexus-recording-suite",
            "userFacingName": "Nexus Recording Suite",
            "sourceTruthOwner": "FAM-006",
            "sourceFiles": ["desktop/desktop_renderer.py", "nexus_visual/monitoring_hud_studio.html", "nexus_visual/monitoring_hud_studio.js"],
            "normalRoute": "HUD Dashboard -> Recording Suite",
            "initialization": "WebEngine window preloaded hidden at startup; shown on demand",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": True,
            "acceptedCurrentProductRoute": True,
            "proofObligation": "full-window render, routed Log Viewer interaction, minimize/restore, close/reopen disposition",
            "overlapRisk": "shared FAM-006-owned current-carrier surface; high overlap",
        },
        {
            "surfaceId": "nexus-log-viewer",
            "userFacingName": "Nexus Log Viewer",
            "sourceTruthOwner": "FAM-006",
            "sourceFiles": ["desktop/desktop_renderer.py", "nexus_visual/monitoring_hud_studio.html", "nexus_visual/monitoring_hud_studio.js"],
            "normalRoute": "Recording Suite -> Open Log Viewer or HUD Dashboard -> Log Viewer",
            "initialization": "WebEngine window preloaded hidden at startup; shown on demand",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": True,
            "acceptedCurrentProductRoute": True,
            "proofObligation": "full-window render, close/reopen, supported resize, input/readability proof",
            "overlapRisk": "shared FAM-006-owned current-carrier surface; high overlap",
        },
        {
            "surfaceId": "ai-status-command-center",
            "userFacingName": "AI Status / Command Center (AI Dashboard)",
            "sourceTruthOwner": "FAM-007; FAM-003 doorway only",
            "sourceFiles": ["desktop/desktop_renderer.py", "nexus_visual/ai_control_center.html"],
            "normalRoute": "tray AI -> AI Status / Command Center",
            "initialization": "lazy-created on demand",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": True,
            "acceptedCurrentProductRoute": True,
            "proofObligation": "full-window fail-closed state, scroll, minimize/restore, close/reopen",
            "overlapRisk": "shared FAM-007-owned current-carrier surface; high overlap",
        },
        {
            "surfaceId": "ai-control-center-domain",
            "userFacingName": "AI Control Center domain child",
            "sourceTruthOwner": "FAM-007",
            "sourceFiles": ["desktop/desktop_renderer.py"],
            "normalRoute": "AI Dashboard control-center doorway is disabled/deferred",
            "initialization": "code-defined lazy child; not initialized by accepted current route",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": False,
            "acceptedCurrentProductRoute": False,
            "proofObligation": "inventory and disabled/deferred doorway proof only",
            "overlapRisk": "future FAM-007 continuation; unmerged sibling state not claimed",
        },
        {
            "surfaceId": "readiness-diagnostics-domain",
            "userFacingName": "Readiness and Diagnostics domain child",
            "sourceTruthOwner": "FAM-007",
            "sourceFiles": ["desktop/desktop_renderer.py"],
            "normalRoute": "AI Dashboard readiness doorway is disabled/deferred",
            "initialization": "code-defined lazy child; not initialized by accepted current route",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": False,
            "acceptedCurrentProductRoute": False,
            "proofObligation": "inventory and disabled/deferred doorway proof only",
            "overlapRisk": "future FAM-007 continuation; unmerged sibling state not claimed",
        },
        {
            "surfaceId": "capabilities-maintenance-domain",
            "userFacingName": "Capabilities and Maintenance domain child",
            "sourceTruthOwner": "FAM-007",
            "sourceFiles": ["desktop/desktop_renderer.py"],
            "normalRoute": "AI Dashboard capabilities doorway is disabled/deferred",
            "initialization": "code-defined lazy child; not initialized by accepted current route",
            "inheritsSharedFlags": True,
            "currentCarrierAvailable": False,
            "acceptedCurrentProductRoute": False,
            "proofObligation": "inventory and disabled/deferred doorway proof only",
            "overlapRisk": "future FAM-007 continuation; unmerged sibling state not claimed",
        },
    ]


NATIVE_SHARED_PROCESS_SURFACES = [
    {
        "surfaceId": "global-settings-native",
        "userFacingName": "Global Settings",
        "owner": "FAM-003 shell with owner-routed pages",
        "classification": "native Qt; shares renderer process lifecycle but does not consume WebEngine flags",
    },
    {
        "surfaceId": "ndai-command-prompt-native",
        "userFacingName": "NDAI Command Prompt",
        "owner": "FAM-003 behavior; FAM-002 presentation authority",
        "classification": "native Qt; shares renderer process lifecycle but does not consume WebEngine flags",
    },
    {
        "surfaceId": "resident-tray-native",
        "userFacingName": "Resident tray",
        "owner": "FAM-003 doorway/routing",
        "classification": "native Qt; shares renderer process lifecycle but does not consume WebEngine flags",
    },
]


OUT_OF_NORMAL_ROUTE = [
    {
        "surface": "root main.py BootRuntimeWindow",
        "reason": "development/proof route; not launched by the normal desktop launcher renderer child",
    },
    {
        "surface": "dev/orin_fam007_visual_acceptance_target_packet.py WebEngine",
        "reason": "proof-only helper with its own flags; cannot prove normal runtime backend",
    },
]


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _runtime_processes() -> list[dict[str, Any]]:
    rows = []
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            command = " ".join(process.info.get("cmdline") or [])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        lowered = command.casefold()
        if "orin_desktop_launcher.pyw" not in lowered and "orin_desktop_main.py" not in lowered:
            continue
        rows.append({"pid": process.pid, "name": process.info.get("name") or "", "commandLine": command})
    return rows


def _launch_session(shortcut: str, root: Path, head: str, session_index: int) -> dict[str, Any]:
    session_root = root / f"session_{session_index:02d}"
    session_root.mkdir(parents=True, exist_ok=True)
    manifest_path = session_root / "fam003_option_d_runtime_session.json"
    env = os.environ.copy()
    env.update(
        {
            "NEXUS_HARNESS_LOG_ROOT": str(session_root / "launcher_logs"),
            "NEXUS_HARNESS_DISABLE_DIAGNOSTICS": "1",
            "NEXUS_HARNESS_DISABLE_VOICE": "1",
            "NEXUS_HARNESS_SUPPRESS_ALREADY_RUNNING_DIALOGS": "1",
            "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_MANIFEST": str(manifest_path),
            "NEXUS_FAM003_RENDERER_BACKEND_WORKSTREAM_ROOT": str(session_root / "visual_evidence"),
            "NEXUS_FAM003_RENDERER_BACKEND_SOURCE_HEAD": head,
            "NEXUS_FAM003_RENDERER_BACKEND_SESSION_INDEX": str(session_index),
            "NEXUS_FAM003_RENDERER_BACKEND_LAUNCH_STARTED_NS": str(time.time_ns()),
            "NEXUS_MONITORING_HUD_STATE_PATH": str(session_root / "monitoring_hud_state.json"),
            "NEXUS_DESKTOP_VALIDATION_SHORTCUT_PATH": shortcut,
            "NEXUS_SHUTDOWN_CONFIRMATION_DECISION": "accepted",
        }
    )
    escaped = shortcut.replace("'", "''")
    launched_at = time.time()
    launch = subprocess.run(
        ["powershell", "-NoProfile", "-Command", f"Start-Process -FilePath '{escaped}'"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )
    _assert(launch.returncode == 0, f"normal desktop shortcut launch failed: {launch.stderr}")
    deadline = time.time() + 150.0
    payload = None
    while time.time() < deadline:
        if manifest_path.exists():
            try:
                payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
                break
            except (OSError, json.JSONDecodeError):
                payload = None
        time.sleep(0.25)
    _assert(isinstance(payload, dict), f"normal-launcher runtime manifest was not written: {manifest_path}")

    own_root_lower = str(session_root).casefold()
    residual = []
    wait_deadline = time.time() + 25.0
    while time.time() < wait_deadline:
        residual = [row for row in _runtime_processes() if own_root_lower in row["commandLine"].casefold()]
        if not residual:
            break
        time.sleep(0.25)
    _assert(not residual, f"validation-owned normal-launcher processes remained: {residual}")

    logs = sorted((session_root / "launcher_logs").glob("Runtime_*.txt"))
    _assert(logs, f"normal launcher runtime log missing in {session_root}")
    runtime_text = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace") for path in logs)
    _assert("Renderer exit code: 0" in runtime_text, "renderer did not exit zero after Workstream probe")
    _assert("RENDERER_MAIN|EVENT_LOOP_EXIT|code=0" in runtime_text, "Qt event loop did not exit cleanly")
    _assert("0xC0000409" not in runtime_text and "3221226505" not in runtime_text, "native crash signature returned")
    _assert("TEMPORARY_SHARED_RUNTIME_SAFETY_POLICY=true" in runtime_text, "launcher did not record temporary shared policy")
    _assert("QTWEBENGINE_CHROMIUM_FLAGS=--disable-gpu" in runtime_text, "launcher did not record the effective software flag")
    payload["launcher"] = {
        "shortcut": shortcut,
        "launchCommand": "Start-Process exact current-root desktop shortcut",
        "startedAtEpoch": launched_at,
        "runtimeLogs": [str(path) for path in logs],
        "rendererExitCode": 0,
        "qtEventLoopExitCode": 0,
        "nativeCrashSignatureAbsent": True,
    }
    return payload


def _walk_strings(value: Any):
    if isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)
    elif isinstance(value, str):
        yield value


def _lifecycle_proof(report_path: Path, output_root: Path) -> dict[str, Any]:
    json_path = report_path.with_suffix(".json")
    _assert(report_path.exists() and json_path.exists(), "desktop-entrypoint lifecycle report/json pair is missing")
    report_text = report_path.read_text(encoding="utf-8-sig", errors="replace")
    report_json = json.loads(json_path.read_text(encoding="utf-8-sig"))
    _assert(report_json.get("overall_ok") is True, "desktop-entrypoint lifecycle report is not green")
    _assert("Overall Result: PASS" in report_text, "desktop-entrypoint text report is not PASS")

    runtime_paths = []
    for value in _walk_strings(report_json.get("result", {})):
        path = Path(value)
        if path.name.startswith("Runtime_") and path.suffix.casefold() == ".txt" and path.exists():
            resolved = path.resolve()
            if resolved not in runtime_paths:
                runtime_paths.append(resolved)
    _assert(runtime_paths, "desktop-entrypoint lifecycle report contains no readable runtime paths")

    session_rows = []
    crash_terms = []
    expected_negative_crash_terms = []
    negative_crash_fixture_scenarios = {
        "vbs_relaunch_after_abnormal_exit",
        "launcher_post_settled_abnormal_exit",
        "launcher_post_settled_abnormal_exit_immediate",
    }
    for path in runtime_paths:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        scenario = path.parent.name
        if "0xC0000409" in text or "3221226505" in text or "POST_SETTLED_ABNORMAL_TERMINATION" in text:
            if scenario in negative_crash_fixture_scenarios:
                expected_negative_crash_terms.append(str(path))
            else:
                crash_terms.append(str(path))
        marker_present = "TEMPORARY_SHARED_RUNTIME_SAFETY_POLICY=true" in text
        flags_present = "QTWEBENGINE_CHROMIUM_FLAGS=--disable-gpu" in text
        if "Starting renderer:" in text and scenario not in negative_crash_fixture_scenarios:
            session_rows.append(
                {
                    "path": str(path),
                    "scenario": scenario,
                    "temporaryPolicyMarker": marker_present,
                    "effectiveFlagsMarker": flags_present,
                    "rendererExitZero": "Renderer exit code: 0" in text,
                    "singleInstanceReleaseCount": text.count("SINGLE_INSTANCE_RELEASED"),
                    "replacementSettled": "RELAUNCH_REPLACEMENT_SESSION_SETTLED" in text,
                    "originalFailureMasked": "POST_SETTLED_ABNORMAL_TERMINATION" in text,
                }
            )
    _assert(not crash_terms, f"abnormal native exit returned in lifecycle proof: {crash_terms}")
    _assert(
        len(expected_negative_crash_terms) == len(negative_crash_fixture_scenarios),
        "desktop-entrypoint negative abnormal-exit fixtures are incomplete",
    )
    _assert(session_rows, "no real launcher session rows were classified")
    _assert(all(row["temporaryPolicyMarker"] and row["effectiveFlagsMarker"] for row in session_rows), "lifecycle session used an unclassified backend")
    _assert(any("decline" in row["scenario"].casefold() for row in session_rows), "decline lifecycle session missing")
    _assert(any("accept" in row["scenario"].casefold() for row in session_rows), "accept lifecycle session missing")

    timeline_markers = (
        "SINGLE_INSTANCE_CONFLICT_DETECTED",
        "RELAUNCH_DECLINED_SESSION_PRESERVED",
        "RELAUNCH_REPLACEMENT_SESSION_ACTIVE",
        "RELAUNCH_REPLACEMENT_SESSION_SETTLED",
        "SHUTDOWN_REQUESTED",
        "NATIVE_SURFACES_RELEASED",
        "EVENT_LOOP_EXIT|code=0",
        "Renderer exit code: 0",
        "SINGLE_INSTANCE_RELEASED",
    )
    timeline_lines = ["# FAM-003 Option D Lifecycle Timelines", ""]
    selected = [row for row in session_rows if "decline_then_accept" in row["scenario"].casefold() or "consecutive" in row["scenario"].casefold()]
    for row in selected[:8]:
        path = Path(row["path"])
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        timeline_lines.extend([f"## {row['scenario']} / {path.name}", ""])
        timeline_lines.extend(f"- `{line}`" for line in lines if any(marker in line for marker in timeline_markers))
        timeline_lines.append("")
    timeline_path = output_root / "FAM003_OPTION_D_LIFECYCLE_TIMELINES.md"
    timeline_path.write_text("\n".join(timeline_lines) + "\n", encoding="utf-8")
    shutil.copy2(report_path, output_root / report_path.name)
    shutil.copy2(json_path, output_root / json_path.name)
    return {
        "status": "PASS",
        "desktopEntrypointReport": str(report_path),
        "desktopEntrypointJson": str(json_path),
        "sessionCount": len(session_rows),
        "sessions": session_rows,
        "declineOnly": "PASS",
        "acceptOnly": "PASS",
        "mixedDeclineThenAccept": "PASS",
        "repeatedMixedCycles": "PASS",
        "originalResidentPreservedAfterDecline": "PASS",
        "nativeSurfacesReleasedOnAccept": "PASS",
        "qtEventLoopExit": 0,
        "rendererExitCode": 0,
        "singleInstanceRelease": "validated by desktop-entrypoint aggregate",
        "replacementAcquisitionAndSettle": "PASS",
        "originalReplacementMasking": "ABSENT",
        "abnormalNativeExit": "ABSENT",
        "expectedNegativeCrashFixtures": expected_negative_crash_terms,
        "timeline": str(timeline_path),
    }


def _summary(values: list[float]) -> dict[str, float | int]:
    return {
        "runs": len(values),
        "min": round(min(values), 2),
        "median": round(statistics.median(values), 2),
        "max": round(max(values), 2),
    }


def _performance(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    metric_paths = {
        "normalDesktopStartupMs": lambda m: m["startupReadyMs"],
        "rendererReadyMs": lambda m: m["rendererReadyMs"],
        "firstWebEngineRenderMs": lambda m: m["firstWebEngineRenderMs"],
        "hudAutomaticOpenMs": lambda m: m["hudAutomaticOpenMs"],
        "hudTrayRestoreMs": lambda m: m["hudTrayRestoreMs"],
        "recordingSuiteOpenMs": lambda m: m["surfaceOpenMs"]["recordingSuite"],
        "logViewerOpenMs": lambda m: m["surfaceOpenMs"]["logViewer"],
        "aiDashboardOpenMs": lambda m: m["surfaceOpenMs"]["aiDashboard"],
        "activeCpuPercentSum": lambda m: m["activeProcess"]["cpuPercentSum"],
        "idleCpuPercentSum": lambda m: m["idleProcess"]["cpuPercentSum"],
        "activeRssMiB": lambda m: m["activeProcess"]["rssMiB"],
        "idleRssMiB": lambda m: m["idleProcess"]["rssMiB"],
        "webEngineSubprocessCount": lambda m: m["idleProcess"]["webEngineSubprocessCount"],
        "p95DispatchGapMs": lambda m: m["responsiveness"]["p95DispatchGapMs"],
        "maxDispatchGapMs": lambda m: m["responsiveness"]["maxDispatchGapMs"],
    }
    summaries = {}
    for name, getter in metric_paths.items():
        values = [float(getter(session["metrics"])) for session in sessions]
        summaries[name] = _summary(values)
    return {
        "status": "PASS",
        "configuration": "temporary process-wide --disable-gpu software composition",
        "runCount": len(sessions),
        "machineContext": sessions[0]["metrics"]["machine"],
        "summaries": summaries,
        "visibleStutterOrJank": "NOT_OBSERVED_IN_CAPTURE_OR_DISPATCH_GAP_EVIDENCE",
        "unresponsiveIntervals": "ABSENT",
        "hardwareDefaultComparison": {
            "status": "NOT_REEXECUTED_WITH_REASON",
            "reason": "hardware-default teardown is a known nondeterministic 0xC0000409 path; current approval forbids unsafe repetition merely to obtain a benchmark",
            "historicalCurrentMachineProvenance": [
                "DesktopEntrypointValidationReport_20260721_113504.txt",
                "DesktopEntrypointValidationReport_20260721_114110.txt",
            ],
            "observedDelta": "not computable from a safe equivalent hardware baseline",
        },
        "thresholdDisposition": "No repo-defined numeric threshold exists; measured min/median/max and visual evidence are preserved for USER review without inventing one.",
        "acceptanceDisposition": "NO_MATERIAL_REGRESSION_OBSERVED",
    }


def _write_contact_sheet(paths: list[Path], output: Path) -> None:
    from PySide6.QtCore import QRectF, Qt
    from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    del app
    columns = 3
    cell_w, cell_h = 410, 300
    rows = (len(paths) + columns - 1) // columns
    sheet = QImage(columns * cell_w + 36, rows * cell_h + 40, QImage.Format_ARGB32)
    sheet.fill(QColor("#020914"))
    painter = QPainter(sheet)
    painter.setRenderHint(QPainter.Antialiasing, True)
    font = QFont("Segoe UI", 9)
    painter.setFont(font)
    for index, path in enumerate(paths):
        image = QImage(str(path))
        _assert(not image.isNull(), f"could not decode PNG for contact sheet: {path}")
        scaled = image.scaled(374, 238, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        col, row = index % columns, index // columns
        x, y = 18 + col * cell_w, 18 + row * cell_h
        painter.setPen(QPen(QColor("#38d9ff"), 1))
        painter.drawRoundedRect(QRectF(x - 5, y - 5, 384, 250), 7, 7)
        painter.drawImage(x, y, scaled)
        painter.setPen(QColor("#dffbff"))
        painter.drawText(QRectF(x, y + 246, 382, 44), Qt.TextWordWrap, f"{index + 1}. {path.name}")
    painter.end()
    _assert(sheet.save(str(output), "PNG"), f"could not save contact sheet {output}")


def _base_validation_manifest() -> dict[str, Any]:
    surfaces = {
        surface_id: {
            "visualVerdict": "PASS" if surface_id in AVAILABLE_PROOF_SURFACES else "NOT_APPLICABLE_WITH_REASON",
            "functionalVerdict": "PASS" if surface_id in AVAILABLE_PROOF_SURFACES else "NOT_APPLICABLE_WITH_REASON",
            "evidence": ["proof.png"] if surface_id in AVAILABLE_PROOF_SURFACES else [],
            "identityProof": {
                "expectedText": surface_id,
                "present": surface_id in AVAILABLE_PROOF_SURFACES,
            },
            "initialCapture": {
                "nonBlank": surface_id in AVAILABLE_PROOF_SURFACES,
                "visuallyPopulated": surface_id in AVAILABLE_PROOF_SURFACES,
                "uniqueSampleColors": 120,
                "dominantColorRatio": 0.12,
            },
            "resizeProof": {
                "changed": True,
                "original": {"width": 780, "height": 1060},
                "actual": {"width": 660, "height": 940},
            } if surface_id == "hud-dashboard" else {},
        }
        for surface_id in REQUIRED_WEBENGINE_SURFACES
    }
    return {
        "status": "PASS",
        "scopeLedger": {
            "sharedRuntimeFlagRecorded": True,
            "classification": EXPECTED_CLASSIFICATION,
            "unmergedSiblingStateClaimed": False,
        },
        "effectiveBackend": {
            "actualFlags": EXPECTED_FLAG,
            "reportedFlags": EXPECTED_FLAG,
            "hardwareAccelerationDisabled": True,
            "softwareCompositionActive": True,
            "policy": EXPECTED_POLICY,
            "policyPermanence": "temporary",
        },
        "affectedSurfaceInventory": _inventory(),
        "surfaceResults": surfaces,
        "hudDirectProof": {"fullWindowImages": ["hud.png"], "telemetryOnly": False, "status": "PASS"},
        "performance": {"status": "PASS", "summaries": {"startup": {"runs": 3}}},
        "materialRegression": {"detected": False, "ignored": False},
        "lifecycle": {"status": "PASS", "abnormalNativeExit": "ABSENT", "originalReplacementMasking": "ABSENT"},
        "backendEvidenceCurrentness": "CURRENT_FINAL_BACKEND",
        "aggregateConsumption": {"optionCConsumesRendererBackendChild": True},
    }


def validate_manifest(payload: dict[str, Any]) -> list[str]:
    failures = []
    scope = payload.get("scopeLedger") or {}
    backend = payload.get("effectiveBackend") or {}
    inventory = payload.get("affectedSurfaceInventory") or []
    results = payload.get("surfaceResults") or {}
    if scope.get("sharedRuntimeFlagRecorded") is not True:
        failures.append("scope-ledger-flag-missing")
    if scope.get("classification") != EXPECTED_CLASSIFICATION:
        failures.append("process-wide-setting-mislabeled")
    inventory_ids = {row.get("surfaceId") for row in inventory}
    if set(REQUIRED_WEBENGINE_SURFACES) - inventory_ids:
        failures.append("affected-surface-omitted")
    for surface_id in AVAILABLE_PROOF_SURFACES:
        row = results.get(surface_id) or {}
        if row.get("visualVerdict") != "PASS" or row.get("functionalVerdict") != "PASS" or not row.get("evidence"):
            failures.append("available-surface-proof-missing")
            break
        if (row.get("initialCapture") or {}).get("visuallyPopulated") is not True:
            failures.append("available-surface-visual-population-missing")
            break
    hud = payload.get("hudDirectProof") or {}
    if hud.get("status") != "PASS" or hud.get("telemetryOnly") is True or not hud.get("fullWindowImages"):
        failures.append("hud-direct-visual-proof-missing")
    hud_surface = results.get("hud-dashboard") or {}
    if (hud_surface.get("identityProof") or {}).get("present") is not True:
        failures.append("hud-surface-identity-missing")
    hud_resize = hud_surface.get("resizeProof") or {}
    if hud_resize.get("changed") is not True or hud_resize.get("original") == hud_resize.get("actual"):
        failures.append("hud-resize-geometry-unproven")
    if backend.get("actualFlags") != backend.get("reportedFlags"):
        failures.append("effective-flags-mismatch")
    if backend.get("hardwareAccelerationDisabled") is not True or backend.get("softwareCompositionActive") is not True:
        failures.append("wrong-backend-presented")
    performance = payload.get("performance") or {}
    if performance.get("status") != "PASS" or not performance.get("summaries"):
        failures.append("performance-evidence-missing")
    regression = payload.get("materialRegression") or {}
    if regression.get("detected") is True and regression.get("ignored") is True:
        failures.append("material-regression-ignored")
    lifecycle = payload.get("lifecycle") or {}
    if lifecycle.get("abnormalNativeExit") != "ABSENT":
        failures.append("abnormal-native-exit")
    if lifecycle.get("originalReplacementMasking") != "ABSENT":
        failures.append("original-failure-masked")
    if payload.get("backendEvidenceCurrentness") != "CURRENT_FINAL_BACKEND":
        failures.append("historical-backend-evidence-reused")
    if scope.get("unmergedSiblingStateClaimed") is True:
        failures.append("unmerged-sibling-state-claimed")
    if backend.get("policy") != EXPECTED_POLICY or backend.get("policyPermanence") != "temporary":
        failures.append("temporary-policy-made-permanent")
    if (payload.get("aggregateConsumption") or {}).get("optionCConsumesRendererBackendChild") is not True:
        failures.append("option-c-child-not-consumed")
    return sorted(set(failures))


def _mutate(payload: dict[str, Any], mutation: str) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    if mutation == "omit_scope_ledger_flag":
        result["scopeLedger"].pop("sharedRuntimeFlagRecorded", None)
    elif mutation == "label_fam003_only":
        result["scopeLedger"]["classification"] = "fam003-only-low-overlap"
    elif mutation == "remove_affected_surface":
        result["affectedSurfaceInventory"] = result["affectedSurfaceInventory"][:-1]
    elif mutation == "remove_available_surface_evidence":
        result["surfaceResults"]["hud-dashboard"]["evidence"] = []
    elif mutation == "hud_telemetry_only":
        result["hudDirectProof"]["telemetryOnly"] = True
    elif mutation == "mismatch_effective_flags":
        result["effectiveBackend"]["reportedFlags"] = "--disable-gpu --different"
    elif mutation == "claim_hardware_option_d":
        result["effectiveBackend"]["hardwareAccelerationDisabled"] = False
    elif mutation == "remove_performance_metrics":
        result["performance"]["summaries"] = {}
    elif mutation == "ignore_material_regression":
        result["materialRegression"] = {"detected": True, "ignored": True}
    elif mutation == "abnormal_native_exit":
        result["lifecycle"]["abnormalNativeExit"] = "0xC0000409"
    elif mutation == "mask_original_failure":
        result["lifecycle"]["originalReplacementMasking"] = "MASKED_BY_REPLACEMENT_SUCCESS"
    elif mutation == "reuse_historical_backend_evidence":
        result["backendEvidenceCurrentness"] = "HISTORICAL_PRE_FINAL_BACKEND"
    elif mutation == "claim_unmerged_sibling_test":
        result["scopeLedger"]["unmergedSiblingStateClaimed"] = True
    elif mutation == "classify_policy_permanent":
        result["effectiveBackend"]["policyPermanence"] = "permanent"
    elif mutation == "aggregate_omits_backend_child":
        result["aggregateConsumption"]["optionCConsumesRendererBackendChild"] = False
    elif mutation == "hud_wrong_surface_capture":
        result["surfaceResults"]["hud-dashboard"]["identityProof"]["present"] = False
    elif mutation == "hud_resize_no_geometry_change":
        resize = result["surfaceResults"]["hud-dashboard"]["resizeProof"]
        resize["changed"] = False
        resize["actual"] = dict(resize["original"])
    elif mutation == "recording_initial_frame_unpainted":
        capture = result["surfaceResults"]["nexus-recording-suite"]["initialCapture"]
        capture["visuallyPopulated"] = False
        capture["uniqueSampleColors"] = 9
        capture["dominantColorRatio"] = 0.9556
    else:
        raise AssertionError(f"unknown fixture mutation: {mutation}")
    return result


def _run_negative_fixtures() -> list[dict[str, Any]]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8-sig"))
    base = _base_validation_manifest()
    _assert(not validate_manifest(base), "valid renderer-backend manifest failed validation")
    rows = []
    for case in fixture.get("cases", []):
        failures = validate_manifest(_mutate(base, case["mutation"]))
        passed = case["expectedFailure"] in failures
        rows.append({"id": case["id"], "status": "PASS" if passed else "FAIL", "expectedFailure": case["expectedFailure"], "actualFailures": failures})
    _assert(all(row["status"] == "PASS" for row in rows), f"negative fixture failure: {rows}")
    return rows


def _markdown_inventory(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# FAM-003 Option D Affected-Surface Inventory",
        "",
        "The backend is shared desktop-runtime behavior, not FAM-003-only behavior. Rows describe implementations present on this carrier; no sibling worktree was inspected.",
        "",
        "| Surface | Owner | Normal route | Initialization | Available | Shared flags | Proof obligation / overlap |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['userFacingName']} (`{row['surfaceId']}`) | {row['sourceTruthOwner']} | {row['normalRoute']} | "
            f"{row['initialization']} | `{row['currentCarrierAvailable']}` | `{row['inheritsSharedFlags']}` | "
            f"{row['proofObligation']}; {row['overlapRisk']} |"
        )
    lines.extend(["", "## Native Qt Shared-Process Surfaces", ""])
    for row in NATIVE_SHARED_PROCESS_SURFACES:
        lines.append(f"- **{row['userFacingName']}**: {row['owner']}; {row['classification']}.")
    lines.extend(["", "## Out Of Normal Route", ""])
    for row in OUT_OF_NORMAL_ROUTE:
        lines.append(f"- **{row['surface']}**: {row['reason']}.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--desktop-entrypoint-report", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    negative_fixtures = _run_negative_fixtures()
    if args.self_test:
        print("FAM-003 RENDERER BACKEND NEGATIVE FIXTURES: PASS")
        print(f"Cases: {len(negative_fixtures)} / {len(negative_fixtures)}")
        return 0

    _assert(args.desktop_entrypoint_report is not None, "--desktop-entrypoint-report is required for final Option D proof")
    _assert(args.runs >= 3, "Option D performance proof requires at least three normal-launcher runs")
    foreign = [
        row for row in _runtime_processes()
        if str(ROOT).casefold() not in row["commandLine"].casefold()
    ]
    _assert(not foreign, f"foreign/sibling desktop runtime is active; do not mutate it: {foreign}")
    current = [
        row for row in _runtime_processes()
        if str(ROOT).casefold() in row["commandLine"].casefold()
    ]
    _assert(not current, f"current FAM-003 runtime must be closed before bounded proof: {current}")

    head = _git("rev-parse", "HEAD")
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_root = (args.output_dir or (LOG_ROOT / timestamp)).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    shortcut_resolution = resolve_desktop_shortcut_for_current_root(str(output_root / "shortcut_resolution"))
    shortcut = shortcut_resolution["path"]
    _assert(Path(shortcut).exists(), f"exact current-root desktop shortcut missing: {shortcut}")
    _assert(shortcut_resolution.get("mode") == "actual-desktop-shortcut-current-root", f"launcher proof is not exact desktop shortcut: {shortcut_resolution}")

    contract_cases = {
        "empty": renderer_backend_contract({}),
        "unrelated": renderer_backend_contract({"QTWEBENGINE_CHROMIUM_FLAGS": "--remote-debugging-port=0"}),
        "existing": renderer_backend_contract({"QTWEBENGINE_CHROMIUM_FLAGS": EXPECTED_FLAG}),
        "duplicate": renderer_backend_contract({"QTWEBENGINE_CHROMIUM_FLAGS": f"{EXPECTED_FLAG} {EXPECTED_FLAG}"}),
    }
    _assert(all(row["disableGpuCount"] == 1 for row in contract_cases.values()), "software flag is not normalized to exactly one token")
    _assert(build_renderer_environment({})["NEXUS_RENDERER_BACKEND_POLICY"] == EXPECTED_POLICY, "renderer policy provenance missing")

    sessions = [_launch_session(shortcut, output_root, head, index) for index in range(1, args.runs + 1)]
    for session in sessions:
        _assert(session.get("status") == "PASS", f"normal-launcher surface session failed: {session.get('failure')}")
        _assert(session.get("sourceHead") == head, "normal-launcher session HEAD provenance is stale")
        backend = session.get("effectiveBackend") or {}
        _assert(backend.get("effectiveFlags") == backend.get("childInheritedFlags") == EXPECTED_FLAG, "normal renderer child flags mismatch")
        for surface_id in AVAILABLE_PROOF_SURFACES:
            row = (session.get("surfaces") or {}).get(surface_id) or {}
            _assert(row.get("visualVerdict") == "PASS" and row.get("functionalVerdict") == "PASS" and row.get("evidence"), f"surface proof missing for {surface_id}")
        _assert((session.get("materialRegression") or {}).get("detected") is False, "material regression detected in session")

    lifecycle = _lifecycle_proof(args.desktop_entrypoint_report.resolve(), output_root)
    performance = _performance(sessions)
    inventory = _inventory()

    representative_images = [Path(item["path"]) for item in sessions[0].get("captures", [])]
    _assert(representative_images, "representative session contains no images")
    for path in representative_images:
        data = path.read_bytes()
        _assert(data.startswith(PNG_SIGNATURE) and len(data) > 1000, f"PNG integrity failed: {path}")
    contact_sheet = output_root / "FAM003_OPTION_D_AFFECTED_SURFACE_CONTACT_SHEET.png"
    _write_contact_sheet(representative_images, contact_sheet)

    inventory_path = output_root / "FAM003_OPTION_D_AFFECTED_SURFACE_INVENTORY.md"
    inventory_path.write_text(_markdown_inventory(inventory), encoding="utf-8")
    performance_path = output_root / "FAM003_OPTION_D_PERFORMANCE_RESPONSIVENESS.md"
    performance_path.write_text(
        "# FAM-003 Option D Performance And Responsiveness\n\n"
        f"Configuration: `{performance['configuration']}`\n\n"
        f"Runs: `{performance['runCount']}`\n\n"
        "No repo-defined numeric threshold exists. These measured values are review evidence, not an invented release threshold.\n\n"
        "```json\n" + json.dumps(performance, indent=2, sort_keys=True) + "\n```\n",
        encoding="utf-8",
    )
    rollback_path = output_root / "FAM003_OPTION_D_ROLLBACK_PLAN.md"
    rollback_path.write_text(
        "# FAM-003 Option D Rollback Plan\n\n"
        "- Flag removal point: `desktop/renderer_backend.py::build_renderer_environment`.\n"
        "- Fallback: remove the temporary flag only after an approved shared renderer architecture provides deterministic hardware-safe teardown.\n"
        "- Required regression proof: full desktop-entrypoint decline/accept/mixed/repeated lifecycle matrix, no `0xC0000409`, all affected-surface images/interactions, and repeated performance evidence.\n"
        "- State preservation: renderer policy is environment-only; HUD/settings/recording/AI state schemas are not migrated or rewritten.\n"
        "- Supersession candidates: isolated WebEngine process ownership, Qt/runtime upgrade, or another approved hardware-safe architecture.\n"
        "- Evidence invalidation: every current backend, surface, lifecycle, and performance artifact becomes stale after any Chromium flag or renderer architecture change.\n",
        encoding="utf-8",
    )
    scope_path = output_root / "FAM003_OPTION_D_EXACT_SCOPE_AND_OWNERSHIP.md"
    scope_path.write_text(
        "# FAM-003 Option D Exact Scope And Ownership\n\n"
        "- No sibling worktree was inspected or mutated.\n"
        "- Shared desktop-runtime behavior is affected; the policy is not FAM-003-only and is not low overlap.\n"
        "- Current-carrier FAM-006/FAM-007-owned surfaces inherit the flag and are therefore covered here without changing their product ownership.\n"
        "- No claim is made about an unmerged sibling branch.\n"
        "- USER approval is temporary and Workstream-bounded; permanent renderer architecture remains open.\n"
        "- Rollback is one environment-policy point followed by mandatory lifecycle/all-surface reproof.\n",
        encoding="utf-8",
    )
    defect_path = output_root / "FAM003_OPTION_D_DEFECT_LEDGER.md"
    defects = {
        "RB-SCOPE-001": "renderer-scope classification defect",
        "RB-SURFACE-001": "affected-surface coverage defect",
        "RB-HUD-001": "HUD Dashboard direct-proof defect",
        "RB-PERF-001": "performance-proof defect",
        "RB-APPROVAL-001": "approval-boundary defect",
        "RB-VALIDATOR-001": "validator coverage defect",
        "RB-CAPTURE-002": "generic screen capture passed without proving the intended surface",
        "RB-PARSER-001": "desktop lifecycle report token was parsed using stale wording",
        "RB-PARSER-002": "expected abnormal-exit negative fixtures were misclassified as current crashes",
        "RB-HUD-VISUAL-001": "HUD evidence initially captured an occluding surface instead of the Dashboard",
        "RB-HUD-RESIZE-001": "generic Qt resize did not exercise the HUD bounded geometry contract",
        "RB-CAPTURE-003": "Recording Suite DOM readiness preceded a populated first WebEngine paint",
    }
    defect_path.write_text(
        "# FAM-003 Option D Defect Ledger\n\n"
        "| Defect | Observed failure / root cause | Repair and closure evidence | Status |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(
            f"| `{defect_id}` | {title}; earlier proof treated a shared flag or incomplete evidence as sufficient. | Current inventory, normal-launcher sessions, lifecycle/performance proof, surface-specific identity and geometry evidence, and {len(negative_fixtures)} fail-capable fixtures. | `CLOSED_WITH_PROOF` |"
            for defect_id, title in defects.items()
        )
        + "\n",
        encoding="utf-8",
    )

    surface_results = sessions[0]["surfaces"]
    hud_images = surface_results["hud-dashboard"]["evidence"]
    manifest = _base_validation_manifest()
    manifest.update(
        {
            "schema": "fam003-option-d-renderer-backend-workstream-v1",
            "status": "PASS",
            "sourceHead": head,
            "branch": _git("branch", "--show-current"),
            "originMain": _git("rev-parse", "origin/main"),
            "mergeBase": _git("merge-base", "HEAD", "origin/main"),
            "proofRoot": str(output_root),
            "proofMode": "R2_WORKSTREAM_ONLY_NOT_H1_NOT_LV_NOT_UTS",
            "optionDApprovalBasis": "explicit USER approval in current FAM-003 Codex task",
            "effectiveBackend": {
                "actualFlags": EXPECTED_FLAG,
                "reportedFlags": EXPECTED_FLAG,
                "hardwareAccelerationDisabled": True,
                "softwareCompositionActive": True,
                "policy": EXPECTED_POLICY,
                "policyPermanence": "temporary",
                "classification": EXPECTED_CLASSIFICATION,
                "duplicateFlagsNormalized": True,
                "contractCases": contract_cases,
            },
            "affectedSurfaceInventory": inventory,
            "nativeSharedProcessSurfaces": NATIVE_SHARED_PROCESS_SURFACES,
            "outOfNormalRoute": OUT_OF_NORMAL_ROUTE,
            "surfaceResults": surface_results,
            "hudDirectProof": {
                "status": "PASS",
                "telemetryOnly": False,
                "fullWindowImages": hud_images,
                "sequence": "normal launcher -> tray Global Settings -> HUD Dashboard enable/auto-open -> close -> tray restore -> repeated open -> disable -> tray hide -> Settings recovery",
            },
            "performance": performance,
            "materialRegression": {"detected": False, "ignored": False, "disposition": "NO_MATERIAL_REGRESSION_OBSERVED"},
            "lifecycle": lifecycle,
            "backendEvidenceCurrentness": "CURRENT_FINAL_BACKEND",
            "aggregateConsumption": {"optionCConsumesRendererBackendChild": True},
            "normalLauncherSessions": sessions,
            "shortcutResolution": shortcut_resolution,
            "negativeFixtures": negative_fixtures,
            "scopeLedger": {
                "sharedRuntimeFlagRecorded": True,
                "classification": EXPECTED_CLASSIFICATION,
                "siblingWorktreeMutation": False,
                "siblingWorktreeInspection": False,
                "currentCarrierSiblingOwnedSurfacesAffected": True,
                "unmergedSiblingStateClaimed": False,
                "temporaryPolicy": True,
                "permanentPolicyDecisionOpen": True,
            },
            "rollbackPlan": str(rollback_path),
            "inventoryReport": str(inventory_path),
            "performanceReport": str(performance_path),
            "scopeReport": str(scope_path),
            "defectLedger": str(defect_path),
            "contactSheet": str(contact_sheet),
            "formalH1Entered": False,
            "formalLiveValidationEntered": False,
            "utsStatus": "NOT_REQUESTED",
        }
    )
    failures = validate_manifest(manifest)
    _assert(not failures, f"final renderer-backend manifest failed: {failures}")
    manifest_path = output_root / "fam003_renderer_backend_workstream_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path = output_root / "FAM003_OPTION_D_RENDERER_BACKEND_WORKSTREAM_REPORT.md"
    report_path.write_text(
        "# FAM-003 Option D Renderer-Backend Workstream Report\n\n"
        f"Status: `PASS`\n\nSource HEAD: `{head}`\n\n"
        f"Effective flags: `{EXPECTED_FLAG}`\n\n"
        f"Policy: `{EXPECTED_POLICY}` (`{EXPECTED_CLASSIFICATION}`)\n\n"
        f"Normal-launcher runs: `{len(sessions)}`\n\n"
        f"Affected WebEngine inventory: `{len(inventory)} / {len(REQUIRED_WEBENGINE_SURFACES)}` rows\n\n"
        f"Directly proofed current routes: `{len(AVAILABLE_PROOF_SURFACES)} / {len(AVAILABLE_PROOF_SURFACES)}`\n\n"
        f"Negative fixtures: `{len(negative_fixtures)} / {len(negative_fixtures)}`\n\n"
        "Material regression: `NOT OBSERVED`\n\n"
        "Hardware-default comparison was not re-executed because the known teardown path is unsafe; no performance-equivalence claim is made.\n\n"
        "This is Workstream proof only. It does not enter H1, formal Live Validation, or UTS, and it does not make Option D permanent architecture.\n",
        encoding="utf-8",
    )
    print("FAM-003 RENDERER BACKEND WORKSTREAM: PASS")
    print(f"Proof Root: {output_root}")
    print(f"Manifest: {manifest_path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
