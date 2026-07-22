"""Fail-capable Option D shared WebEngine Workstream proof for FAM-003.

Helper Status: Workstream-scoped
Owner Workstream: FAM-003 R2 Settings/tray/NCP completion proof
Reason Reusable Helper Was Not Extended: The temporary Option D policy, current
    carrier surface inventory, and fail-capable performance fixtures are branch-specific.
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
from dev.fam003_renderer_backend_runtime_probe import (  # noqa: E402
    PERFORMANCE_METHODOLOGY_VERSION,
    PERFORMANCE_SAMPLE_DURATION_MS,
    PERFORMANCE_SAMPLE_INTERVAL_MS,
    PERFORMANCE_SETTLE_DURATION_MS,
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

RESTORED_PROOF_SURFACES = (
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


def _preserved_lifecycle_proof(
    manifest_path: Path,
    output_root: Path,
    current_head: str,
) -> dict[str, Any]:
    _assert(manifest_path.exists(), f"preserved lifecycle manifest is missing: {manifest_path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    source_head = str(payload.get("sourceHead") or "")
    lifecycle = copy.deepcopy(payload.get("lifecycle") or {})
    _assert(source_head, "preserved lifecycle manifest has no source HEAD")
    _assert(lifecycle.get("status") == "PASS", "preserved lifecycle receipt is not PASS")
    _assert(lifecycle.get("abnormalNativeExit") == "ABSENT", "preserved lifecycle receipt contains an abnormal native exit")
    _assert(lifecycle.get("originalReplacementMasking") == "ABSENT", "preserved lifecycle receipt masked the original session")
    changed = [
        row.strip()
        for row in _git("diff", "--name-only", f"{source_head}..{current_head}").splitlines()
        if row.strip()
    ] if source_head != current_head else []
    lifecycle_bearing_prefixes = (
        "desktop/",
        "main.py",
        "launch_orin_desktop.vbs",
        "dev/orin_desktop_entrypoint_validation.py",
        "dev/fixtures/desktop_relaunch_lifecycle_cases.json",
    )
    invalidating = [
        row for row in changed
        if row == "main.py" or any(row.startswith(prefix) for prefix in lifecycle_bearing_prefixes)
    ]
    _assert(not invalidating, f"preserved lifecycle proof was invalidated by product/lifecycle changes: {invalidating}")

    source_root = manifest_path.parent
    copied: list[str] = []
    for name in (
        "FAM003_OPTION_D_LIFECYCLE_TIMELINES.md",
        "DesktopEntrypointValidationReport_20260721_143116.txt",
        "DesktopEntrypointValidationReport_20260721_143116.json",
    ):
        source = source_root / name
        if source.exists():
            target = output_root / name
            shutil.copy2(source, target)
            copied.append(str(target))
    lifecycle.update(
        {
            "status": "PASS",
            "currentnessDisposition": "PRESERVED_CURRENT_HELPER_ONLY_DIFF",
            "preservedFromManifest": str(manifest_path),
            "preservedSourceHead": source_head,
            "currentHead": current_head,
            "changedSincePreservedProof": changed,
            "invalidatingLifecycleChanges": invalidating,
            "copiedReceiptArtifacts": copied,
            "freshRerunAttempt": "FAILED_BEFORE_FINAL_PASS_OUTER_TIMEOUT_AND_PARTIAL_REPORT",
            "freshRerunReport": str(
                ROOT
                / "dev"
                / "logs"
                / "desktop_entrypoint_validation"
                / "reports"
                / "DesktopEntrypointValidationReport_20260721_154253.json"
            ),
        }
    )
    return lifecycle


def _summary(values: list[float]) -> dict[str, float | int]:
    return {
        "runs": len(values),
        "min": round(min(values), 2),
        "median": round(statistics.median(values), 2),
        "max": round(max(values), 2),
    }


def _performance(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    metric_paths = {
        "normalDesktopFirstVisiblePaintSignalMs": lambda m: m["startupTimeline"]["firstVisiblePaintSignalMs"],
        "rendererProcessStartMs": lambda m: m["startupTimeline"]["rendererProcessStartMs"],
        "hudAutomaticOpenMs": lambda m: m["hudAutomaticOpenMs"],
        "hudTrayRestoreMs": lambda m: m["hudTrayRestoreMs"],
        "recordingSuiteInteractiveReadyMs": lambda m: m["surfaceTimelines"]["recordingSuite"]["interactiveReadyMs"],
        "logViewerInteractiveReadyMs": lambda m: m["surfaceTimelines"]["logViewer"]["interactiveReadyMs"],
        "aiDashboardInteractiveReadyMs": lambda m: m["surfaceTimelines"]["aiDashboard"]["interactiveReadyMs"],
        "startupResidentCpuCoreEquivalentPercent": lambda m: m["startupResidentIdle"]["totalRendererTree"]["cpuCoreEquivalentPercent"],
        "startupResidentCpuWholeMachinePercent": lambda m: m["startupResidentIdle"]["totalRendererTree"]["cpuWholeMachinePercent"],
        "startupResidentRssMedianMiB": lambda m: m["startupResidentIdle"]["totalRendererTree"]["rssMedianMiB"],
        "startupResidentRssMaxMiB": lambda m: m["startupResidentIdle"]["totalRendererTree"]["rssMaxMiB"],
        "representativeActiveCpuCoreEquivalentPercent": lambda m: m["representativeActive"]["totalRendererTree"]["cpuCoreEquivalentPercent"],
        "representativeActiveCpuWholeMachinePercent": lambda m: m["representativeActive"]["totalRendererTree"]["cpuWholeMachinePercent"],
        "representativeActiveRssMedianMiB": lambda m: m["representativeActive"]["totalRendererTree"]["rssMedianMiB"],
        "representativeActiveRssMaxMiB": lambda m: m["representativeActive"]["totalRendererTree"]["rssMaxMiB"],
        "postUseResidentCpuCoreEquivalentPercent": lambda m: m["postUseResidentIdle"]["totalRendererTree"]["cpuCoreEquivalentPercent"],
        "postUseResidentCpuWholeMachinePercent": lambda m: m["postUseResidentIdle"]["totalRendererTree"]["cpuWholeMachinePercent"],
        "postUseResidentRssMedianMiB": lambda m: m["postUseResidentIdle"]["totalRendererTree"]["rssMedianMiB"],
        "postUseResidentRssMaxMiB": lambda m: m["postUseResidentIdle"]["totalRendererTree"]["rssMaxMiB"],
        "postUseWebEngineSubprocessCount": lambda m: m["postUseResidentIdle"]["totalRendererTree"]["webEngineSubprocessCount"],
        "p95DispatchGapMs": lambda m: m["responsiveness"]["p95DispatchGapMs"],
        "maxDispatchGapMs": lambda m: m["responsiveness"]["maxDispatchGapMs"],
    }
    summaries = {}
    for name, getter in metric_paths.items():
        values = [float(getter(session["metrics"])) for session in sessions]
        summaries[name] = _summary(values)
    return {
        "status": "MEASUREMENT_PASS",
        "methodologyVersion": PERFORMANCE_METHODOLOGY_VERSION,
        "configuration": "temporary process-wide --disable-gpu software composition",
        "runCount": len(sessions),
        "machineContext": sessions[0]["metrics"]["machine"],
        "samplingContract": {
            "settleDurationMs": PERFORMANCE_SETTLE_DURATION_MS,
            "sampleDurationMs": PERFORMANCE_SAMPLE_DURATION_MS,
            "sampleIntervalMs": PERFORMANCE_SAMPLE_INTERVAL_MS,
            "states": ["startup-resident-idle", "representative-active", "post-use-resident-idle"],
        },
        "summaries": summaries,
        "rawSessionEvidence": [
            {
                "sessionIndex": session["sessionIndex"],
                "sourceHead": session["sourceHead"],
                "manifest": session.get("manifestPath", "embedded in normalLauncherSessions"),
            }
            for session in sessions
        ],
        "visibleStutterOrJank": "NO_UNRESPONSIVE_INTERVAL_OVER_1000MS_IN_SUSTAINED_ACTIVE_DISPATCH_EVIDENCE",
        "unresponsiveIntervals": "ABSENT",
        "hardwareDefaultComparison": {
            "status": "NO_SAFE_EQUIVALENT_BASELINE",
            "comparable": False,
            "reason": "hardware-default teardown is a known nondeterministic 0xC0000409 path; current approval forbids unsafe repetition merely to obtain a benchmark",
            "historicalCurrentMachineProvenance": "NOT_COMPARABLE_WITH_REASON: earlier runs used different metric definitions, sub-second intervals, and no process attribution",
            "observedDelta": None,
        },
        "intraOptionDStateDeltas": {
            "postUseMinusStartupCpuCoreEquivalentMedian": round(
                float(summaries["postUseResidentCpuCoreEquivalentPercent"]["median"])
                - float(summaries["startupResidentCpuCoreEquivalentPercent"]["median"]),
                2,
            ),
            "postUseMinusStartupRssMedianMiB": round(
                float(summaries["postUseResidentRssMedianMiB"]["median"])
                - float(summaries["startupResidentRssMedianMiB"]["median"]),
                2,
            ),
        },
        "requiredMetricAdjudication": {
            "startup": "MEASURED",
            "firstVisiblePaint": "MEASURED_FROM_PRODUCT_FIRST_VISIBLE_SIGNAL",
            "surfaceOpening": "MEASURED_TO_VISIBLE_AND_PAGE_READY_WITH_PAINT_LIMITATION_EXPLICIT",
            "cpu": "MEASURED_PER_PROCESS_AND_RENDERER_TREE",
            "memory": "MEASURED_PER_PROCESS_AND_RENDERER_TREE",
            "residentIdle": "MEASURED_AT_STARTUP_AND_POST_USE",
            "activeWorkload": "MEASURED",
            "responsiveness": "MEASURED",
            "baseline": "NO_SAFE_EQUIVALENT_BASELINE",
        },
        "thresholdDisposition": "No repo-defined numeric threshold exists; no threshold was invented.",
        "acceptanceDisposition": "USER_DECISION_REQUIRED",
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


def _base_surface_inventory(state: str, on_demand_visible: bool) -> dict[str, Any]:
    return {
        "stateLabel": state,
        "surfaces": [
            {"surfaceId": "orin-core-visualization", "visible": True, "intentionallyPersistent": True},
            {"surfaceId": "resident-tray-native", "visible": True, "intentionallyPersistent": True},
            {"surfaceId": "hud-dashboard", "visible": on_demand_visible, "intentionallyPersistent": False},
        ],
        "onDemandVisible": ["hud-dashboard"] if on_demand_visible else [],
        "persistentResidentVisible": ["orin-core-visualization", "resident-tray-native"],
    }


def _base_performance_sample(label: str, *, active: bool) -> dict[str, Any]:
    inventory = _base_surface_inventory(label, active)
    process = {
        "pid": 100,
        "parentPid": 1,
        "name": "pythonw.exe",
        "role": "desktop-python-parent",
        "commandLine": "pythonw desktop/orin_desktop_main.py",
        "cpuTimeSeconds": 1.0,
        "cpuCoreEquivalentPercent": 10.0,
        "cpuWholeMachinePercent": 0.625,
        "rssMedianMiB": 400.0,
        "rssMaxMiB": 410.0,
        "rssFinalMiB": 405.0,
        "sampleCount": 40,
    }
    return {
        "methodologyVersion": PERFORMANCE_METHODOLOGY_VERSION,
        "label": label,
        "classification": "REPRESENTATIVE_ACTIVE_WORKLOAD" if active else "IDLE",
        "settleDurationMs": PERFORMANCE_SETTLE_DURATION_MS,
        "sampleDurationMs": PERFORMANCE_SAMPLE_DURATION_MS,
        "requiredMinimumDurationMs": PERFORMANCE_SAMPLE_DURATION_MS,
        "sampleIntervalMs": PERFORMANCE_SAMPLE_INTERVAL_MS,
        "rawSampleCount": 40,
        "logicalProcessorCount": 16,
        "cpuNormalization": {
            "coreEquivalentPercent": "100 percent equals one logical processor fully occupied over the measured wall interval; renderer-tree totals may exceed 100 percent",
            "wholeMachinePercent": "core-equivalent percent divided by logical processor count",
        },
        "surfaceInventoryBefore": inventory,
        "surfaceInventoryAfter": inventory,
        "expectedOnDemandVisible": active,
        "surfaceStateMatchesMethodology": True,
        "validationActivity": {
            "domInspection": False,
            "screenshotOrFileCapture": False,
            "evidenceGeneration": False,
            "eventLoopPump": True,
            "definedProductWorkload": active,
            "contaminationDisposition": "EXPECTED_DEFINED_ACTIVE_WORKLOAD" if active else "NONE",
        },
        "workload": {
            "interactionCount": 40 if active else 0,
            "interactionTargets": ["hud-dashboard"] * 40 if active else [],
            "inputRatePerSecond": 4.0 if active else 0.0,
            "operation": "rotating asynchronous 8px down/up WebEngine scroll pulse" if active else "none",
        },
        "perProcess": [process],
        "totalRendererTree": {
            "processCount": 1,
            "webEngineSubprocessCount": 0,
            "cpuTimeSeconds": 1.0,
            "cpuCoreEquivalentPercent": 10.0,
            "cpuWholeMachinePercent": 0.625,
            "rssMedianMiB": 400.0,
            "rssMaxMiB": 410.0,
            "rssFinalMiB": 405.0,
        },
        "responsiveness": {
            "iterationCount": 800,
            "medianDispatchGapMs": 12.5,
            "p95DispatchGapMs": 14.0,
            "maxDispatchGapMs": 20.0,
            "unresponsiveIntervalOver1000Ms": False,
        },
        "rawSamples": [
            {
                "sampleIndex": index,
                "offsetMs": index * PERFORMANCE_SAMPLE_INTERVAL_MS,
                "durationMs": PERFORMANCE_SAMPLE_INTERVAL_MS,
                "processes": [
                    {
                        "pid": 100,
                        "parentPid": 1,
                        "name": "pythonw.exe",
                        "role": "desktop-python-parent",
                        "cpuTimeSeconds": 0.025,
                        "cpuCoreEquivalentPercent": 10.0,
                        "cpuWholeMachinePercent": 0.625,
                        "rssBytes": 424673280,
                        "rssMiB": 405.0,
                    }
                ],
                "interactionTargets": ["hud-dashboard"] if active else [],
            }
            for index in range(40)
        ],
    }


def _base_runtime_session() -> dict[str, Any]:
    timeline = {
        "definition": "high-resolution launcher invocation to the product CORE_VISUALIZATION_FIRST_VISIBLE callback that schedules this probe",
        "launcherInvocationMs": 0.0,
        "rendererProcessStartMs": 500.0,
        "qApplicationCreatedMs": None,
        "qApplicationCreatedDisposition": "EVENT_EXISTS_IN_RUNTIME_LOG_WITH_SECOND_RESOLUTION_ONLY_NOT_USED_AS_A_PRECISION_METRIC",
        "webEngineViewCreationMs": None,
        "webEngineViewCreationDisposition": "NOT_INSTRUMENTED_BY_CURRENT_ARCHITECTURE",
        "pageLoadStartMs": None,
        "pageLoadStartDisposition": "NOT_INSTRUMENTED_BY_CURRENT_ARCHITECTURE",
        "domContentReadyMs": None,
        "domContentReadyDisposition": "PAGE_READY_PRECEDES_FIRST_VISIBLE_SIGNAL_BUT_HAS_NO_HIGH_RESOLUTION_LAUNCH_RELATIVE_EVENT",
        "firstVisiblePaintSignalMs": 3000.0,
        "stableResidentReadyMs": 3000.0,
        "observerOverheadIncluded": False,
        "screenshotOrDomInspectionIncluded": False,
        "eventProvenance": "DesktopRuntimeWindow.core_visualization_visible / CORE_VISUALIZATION_FIRST_VISIBLE",
    }
    surface_timeline = {
        "routeActivationToVisibleMs": 250.0,
        "interactiveReadyMs": 250.0,
        "firstVisiblePaintMs": None,
        "firstVisiblePaintDisposition": "CURRENT_CHILD_WINDOW_EXPOSES_PAGE_READY_WITHOUT_A_ROUTE_RELATIVE_PAINT_EVENT",
        "evidenceCollectionIncluded": False,
    }
    metrics = {
        "startupReadyMs": 3000.0,
        "startupTimeline": timeline,
        "machine": {"logicalCpuCount": 16, "physicalMemoryGiB": 64.0, "platform": "Windows", "python": "3", "qt": "6"},
        "startupResidentIdle": _base_performance_sample("startup-resident-idle", active=False),
        "representativeActive": _base_performance_sample("representative-active", active=True),
        "postUseResidentIdle": _base_performance_sample("post-use-resident-idle", active=False),
        "surfaceTimelines": {
            "globalSettings": dict(surface_timeline),
            "hudDashboard": dict(surface_timeline),
            "recordingSuite": dict(surface_timeline),
            "logViewer": dict(surface_timeline),
            "aiDashboard": dict(surface_timeline),
            "hudDashboardRestore": dict(surface_timeline),
        },
        "hudAutomaticOpenMs": 250.0,
        "hudTrayRestoreMs": 40.0,
        "responsiveness": _base_performance_sample("representative-active", active=True)["responsiveness"],
    }
    return {
        "status": "PASS",
        "sourceHead": "TEST_HEAD",
        "sessionIndex": 1,
        "effectiveBackend": {"effectiveFlags": EXPECTED_FLAG, "childInheritedFlags": EXPECTED_FLAG},
        "metrics": metrics,
        "materialRegression": {
            "detected": None,
            "disposition": "USER_DECISION_REQUIRED",
            "visualCorruption": False,
            "unresponsiveInterval": False,
            "requiredMetricsAdjudicated": True,
            "baselineComparable": False,
        },
    }


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
            "restoreProof": {
                "status": "PASS",
                "uniqueColorRatio": 1.0,
                "byteRatio": 1.0,
                "dominantColorRatio": 0.08,
                "dominantColorLimit": 0.18,
            } if surface_id in RESTORED_PROOF_SURFACES else {},
        }
        for surface_id in REQUIRED_WEBENGINE_SURFACES
    }
    sessions = []
    for index in range(1, 4):
        session = _base_runtime_session()
        session["sessionIndex"] = index
        sessions.append(session)
    performance = _performance(sessions)
    return {
        "status": "USER_DECISION_REQUIRED",
        "sourceHead": "TEST_HEAD",
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
        "performance": performance,
        "materialRegression": {
            "detected": None,
            "ignored": False,
            "disposition": "USER_DECISION_REQUIRED",
            "requiredMetricsAdjudicated": True,
            "baselineComparable": False,
        },
        "normalLauncherSessions": sessions,
        "lifecycle": {"status": "PASS", "abnormalNativeExit": "ABSENT", "originalReplacementMasking": "ABSENT"},
        "backendEvidenceCurrentness": "CURRENT_FINAL_BACKEND",
        "aggregateConsumption": {"optionCConsumesRendererBackendChild": True},
        "javascriptCallbackResilience": {
            "maxAttempts": 3,
            "exhausted": False,
            "sessions": [{"maxAttempts": 3, "exhausted": False}],
        },
        "javascriptCallbackRetryUnitFixture": {"status": "PASS", "callCount": 2, "recoveredOnAttempt": 2},
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
    for surface_id in RESTORED_PROOF_SURFACES:
        restore = (results.get(surface_id) or {}).get("restoreProof") or {}
        if (
            restore.get("status") != "PASS"
            or float(restore.get("uniqueColorRatio") or 0) < 0.85
            or float(restore.get("byteRatio") or 0) < 0.75
            or float(restore.get("dominantColorRatio") or 1) > float(restore.get("dominantColorLimit") or 0)
        ):
            failures.append(f"{surface_id}-restored-visual-coverage-failed")
    if backend.get("actualFlags") != backend.get("reportedFlags"):
        failures.append("effective-flags-mismatch")
    if backend.get("hardwareAccelerationDisabled") is not True or backend.get("softwareCompositionActive") is not True:
        failures.append("wrong-backend-presented")
    performance = payload.get("performance") or {}
    sessions = payload.get("normalLauncherSessions") or []
    if performance.get("status") != "MEASUREMENT_PASS" or not performance.get("summaries") or len(sessions) < 3:
        failures.append("performance-evidence-missing")
    if performance.get("methodologyVersion") != PERFORMANCE_METHODOLOGY_VERSION:
        failures.append("performance-currentness-invalid")
    required_summary_names = {
        "normalDesktopFirstVisiblePaintSignalMs",
        "rendererProcessStartMs",
        "recordingSuiteInteractiveReadyMs",
        "logViewerInteractiveReadyMs",
        "aiDashboardInteractiveReadyMs",
        "startupResidentCpuCoreEquivalentPercent",
        "startupResidentCpuWholeMachinePercent",
        "startupResidentRssMedianMiB",
        "representativeActiveCpuCoreEquivalentPercent",
        "representativeActiveCpuWholeMachinePercent",
        "representativeActiveRssMedianMiB",
        "postUseResidentCpuCoreEquivalentPercent",
        "postUseResidentCpuWholeMachinePercent",
        "postUseResidentRssMedianMiB",
        "p95DispatchGapMs",
        "maxDispatchGapMs",
    }
    if required_summary_names - set((performance.get("summaries") or {}).keys()):
        failures.append("material-measurement-omitted")
    required_adjudication = {
        "startup",
        "firstVisiblePaint",
        "surfaceOpening",
        "cpu",
        "memory",
        "residentIdle",
        "activeWorkload",
        "responsiveness",
        "baseline",
    }
    if required_adjudication - set((performance.get("requiredMetricAdjudication") or {}).keys()):
        failures.append("performance-adjudication-incomplete")
    baseline = performance.get("hardwareDefaultComparison") or {}
    no_comparable_baseline = baseline.get("comparable") is False
    if no_comparable_baseline and performance.get("acceptanceDisposition") in {
        "PASS",
        "NO_MATERIAL_REGRESSION_OBSERVED",
        "EQUIVALENT",
        "IMPROVED",
    }:
        failures.append("unsupported-performance-equivalence")
    sampling = performance.get("samplingContract") or {}
    if (
        sampling.get("settleDurationMs") != PERFORMANCE_SETTLE_DURATION_MS
        or sampling.get("sampleDurationMs") != PERFORMANCE_SAMPLE_DURATION_MS
        or sampling.get("sampleIntervalMs") != PERFORMANCE_SAMPLE_INTERVAL_MS
    ):
        failures.append("performance-methodology-contract-missing")

    for session in sessions:
        if session.get("sourceHead") != payload.get("sourceHead"):
            failures.append("performance-currentness-invalid")
        session_backend = session.get("effectiveBackend") or {}
        if (
            session_backend.get("effectiveFlags") != EXPECTED_FLAG
            or session_backend.get("childInheritedFlags") != EXPECTED_FLAG
            or backend.get("actualFlags") != session_backend.get("effectiveFlags")
        ):
            failures.append("effective-flags-mismatch")
        metrics = session.get("metrics") or {}
        if "firstWebEngineRenderMs" in metrics:
            failures.append("first-visible-timing-invalid")
        timeline = metrics.get("startupTimeline") or {}
        if (
            timeline.get("firstVisiblePaintSignalMs") is None
            or timeline.get("eventProvenance") != "DesktopRuntimeWindow.core_visualization_visible / CORE_VISUALIZATION_FIRST_VISIBLE"
            or "CORE_VISUALIZATION_FIRST_VISIBLE" not in str(timeline.get("definition") or "")
        ):
            failures.append("first-visible-timing-invalid")
        if timeline.get("observerOverheadIncluded") is not False or timeline.get("screenshotOrDomInspectionIncluded") is not False:
            failures.append("first-visible-timing-contaminated")
        surface_timelines = metrics.get("surfaceTimelines") or {}
        for surface_name in ("globalSettings", "hudDashboard", "recordingSuite", "logViewer", "aiDashboard", "hudDashboardRestore"):
            timeline_row = surface_timelines.get(surface_name) or {}
            if timeline_row.get("routeActivationToVisibleMs") is None or timeline_row.get("interactiveReadyMs") is None:
                failures.append("surface-opening-timing-missing")
                break
            if timeline_row.get("evidenceCollectionIncluded") is not False:
                failures.append("surface-opening-timing-contaminated")
                break
        for sample_name, expected_visible, expected_active in (
            ("startupResidentIdle", False, False),
            ("representativeActive", True, True),
            ("postUseResidentIdle", False, False),
        ):
            sample = metrics.get(sample_name) or {}
            if sample.get("methodologyVersion") != PERFORMANCE_METHODOLOGY_VERSION:
                failures.append("performance-currentness-invalid")
            if float(sample.get("sampleDurationMs") or 0) < PERFORMANCE_SAMPLE_DURATION_MS:
                failures.append("performance-sample-duration-insufficient")
            if sample.get("sampleIntervalMs") != PERFORMANCE_SAMPLE_INTERVAL_MS:
                failures.append("performance-methodology-contract-missing")
            before = sample.get("surfaceInventoryBefore") or {}
            after = sample.get("surfaceInventoryAfter") or {}
            if not before.get("surfaces") or not after.get("surfaces") or sample.get("surfaceStateMatchesMethodology") is not True:
                failures.append("surface-process-inventory-missing")
            observed_visible = bool(before.get("onDemandVisible") or after.get("onDemandVisible"))
            if observed_visible is not expected_visible or sample.get("expectedOnDemandVisible") is not expected_visible:
                failures.append("idle-surface-inventory-invalid" if not expected_visible else "active-surface-inventory-invalid")
            activity = sample.get("validationActivity") or {}
            if not expected_active and (
                activity.get("domInspection") is not False
                or activity.get("screenshotOrFileCapture") is not False
                or activity.get("evidenceGeneration") is not False
                or activity.get("definedProductWorkload") is not False
                or activity.get("contaminationDisposition") != "NONE"
            ):
                failures.append("idle-sample-contaminated")
            workload = sample.get("workload") or {}
            if expected_active and (
                activity.get("definedProductWorkload") is not True
                or int(workload.get("interactionCount") or 0) <= 0
                or float(workload.get("inputRatePerSecond") or 0) <= 0
            ):
                failures.append("active-workload-definition-missing")
            processes = sample.get("perProcess") or []
            total = sample.get("totalRendererTree") or {}
            normalization = sample.get("cpuNormalization") or {}
            if (
                not processes
                or not normalization.get("coreEquivalentPercent")
                or not normalization.get("wholeMachinePercent")
                or sample.get("logicalProcessorCount") is None
                or any(
                    row.get("pid") is None
                    or row.get("parentPid") is None
                    or not row.get("role")
                    or row.get("cpuTimeSeconds") is None
                    or row.get("cpuCoreEquivalentPercent") is None
                    or row.get("cpuWholeMachinePercent") is None
                    for row in processes
                )
                or total.get("cpuCoreEquivalentPercent") is None
                or total.get("cpuWholeMachinePercent") is None
            ):
                failures.append("cpu-attribution-missing")
            if (
                any(
                    row.get("rssMedianMiB") is None
                    or row.get("rssMaxMiB") is None
                    or row.get("rssFinalMiB") is None
                    for row in processes
                )
                or total.get("rssMedianMiB") is None
                or total.get("rssMaxMiB") is None
                or total.get("rssFinalMiB") is None
            ):
                failures.append("memory-attribution-missing")
            raw_samples = sample.get("rawSamples") or []
            if not raw_samples or len(raw_samples) != int(sample.get("rawSampleCount") or -1):
                failures.append("raw-performance-data-missing")
            if raw_samples and any(not row.get("processes") for row in raw_samples):
                failures.append("raw-performance-data-missing")
    if sessions:
        try:
            reproduced = _performance(sessions)
            if reproduced.get("summaries") != performance.get("summaries"):
                failures.append("raw-summary-parity-failed")
        except (KeyError, TypeError, ValueError):
            failures.append("raw-summary-parity-failed")
    regression = payload.get("materialRegression") or {}
    if regression.get("detected") is True and regression.get("ignored") is True:
        failures.append("material-regression-ignored")
    if (
        regression.get("requiredMetricsAdjudicated") is not True
        or regression.get("baselineComparable") is not False
        or regression.get("disposition") != "USER_DECISION_REQUIRED"
        or performance.get("acceptanceDisposition") != "USER_DECISION_REQUIRED"
        or payload.get("status") != "USER_DECISION_REQUIRED"
    ):
        failures.append("performance-adjudication-incomplete")
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
    callback = payload.get("javascriptCallbackResilience") or {}
    if callback.get("maxAttempts") != 3 or callback.get("exhausted") is True:
        failures.append("javascript-callback-exhaustion-ignored")
    if not callback.get("sessions") or any(row.get("exhausted") is True for row in callback.get("sessions") or []):
        failures.append("javascript-callback-exhaustion-ignored")
    callback_unit = payload.get("javascriptCallbackRetryUnitFixture") or {}
    if callback_unit.get("status") != "PASS" or callback_unit.get("recoveredOnAttempt") != 2:
        failures.append("javascript-callback-retry-path-unproven")
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
    elif mutation == "javascript_callback_exhaustion_ignored":
        result["javascriptCallbackResilience"]["exhausted"] = True
        result["javascriptCallbackResilience"]["sessions"][0]["exhausted"] = True
    elif mutation == "omit_javascript_callback_retry_fixture":
        result["javascriptCallbackRetryUnitFixture"] = {"status": "MISSING"}
    elif mutation == "hud_restore_partial_black_region":
        restore = result["surfaceResults"]["hud-dashboard"]["restoreProof"]
        restore.update({"status": "FAIL", "uniqueColorRatio": 0.7939, "byteRatio": 0.6566, "dominantColorRatio": 0.3622})
    elif mutation == "ai_restore_partial_black_region":
        restore = result["surfaceResults"]["ai-status-command-center"]["restoreProof"]
        restore.update({"status": "FAIL", "uniqueColorRatio": 0.7939, "byteRatio": 0.3741, "dominantColorRatio": 0.4812})
    elif mutation == "idle_on_demand_surface_active":
        sample = result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]
        sample["surfaceInventoryBefore"]["onDemandVisible"] = ["hud-dashboard"]
        sample["surfaceStateMatchesMethodology"] = False
    elif mutation == "insufficient_sample_duration":
        result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]["sampleDurationMs"] = 900
    elif mutation == "remove_cpu_attribution":
        sample = result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]
        sample["cpuNormalization"] = {}
        sample["perProcess"] = []
    elif mutation == "remove_surface_inventory":
        sample = result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]
        sample["surfaceInventoryBefore"] = {}
    elif mutation == "first_render_starts_after_ready":
        timeline = result["normalLauncherSessions"][0]["metrics"]["startupTimeline"]
        timeline["definition"] = "timer starts after WebEngine readiness and DOM inspection"
        timeline["eventProvenance"] = "post-ready helper timer"
    elif mutation == "first_render_includes_capture_overhead":
        timeline = result["normalLauncherSessions"][0]["metrics"]["startupTimeline"]
        timeline["observerOverheadIncluded"] = True
        timeline["screenshotOrDomInspectionIncluded"] = True
    elif mutation == "omit_metric_adjudication":
        result["performance"]["requiredMetricAdjudication"].pop("cpu", None)
        result["materialRegression"]["requiredMetricsAdjudicated"] = False
    elif mutation == "claim_equivalence_without_baseline":
        result["performance"]["acceptanceDisposition"] = "NO_MATERIAL_REGRESSION_OBSERVED"
    elif mutation == "omit_post_use_measurement":
        result["normalLauncherSessions"][0]["metrics"].pop("postUseResidentIdle", None)
        result["performance"]["summaries"].pop("postUseResidentCpuCoreEquivalentPercent", None)
    elif mutation == "normal_launcher_flag_mismatch":
        result["normalLauncherSessions"][0]["effectiveBackend"]["childInheritedFlags"] = ""
        result["effectiveBackend"]["reportedFlags"] = ""
    elif mutation == "remove_raw_performance_data":
        sample = result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]
        sample["rawSamples"] = []
    elif mutation == "tamper_performance_summary":
        result["performance"]["summaries"]["startupResidentRssMedianMiB"]["median"] = 9999.0
    elif mutation == "post_use_on_demand_surface_active":
        sample = result["normalLauncherSessions"][0]["metrics"]["postUseResidentIdle"]
        sample["surfaceInventoryAfter"]["onDemandVisible"] = ["ai-status-command-center"]
        sample["surfaceStateMatchesMethodology"] = False
    elif mutation == "contaminate_idle_sample":
        activity = result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]["validationActivity"]
        activity["screenshotOrFileCapture"] = True
        activity["contaminationDisposition"] = "UNCLASSIFIED"
    elif mutation == "reuse_stale_performance_methodology":
        result["performance"]["methodologyVersion"] = "fam003-option-d-performance-v1"
        result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]["methodologyVersion"] = "fam003-option-d-performance-v1"
    elif mutation == "remove_memory_attribution":
        sample = result["normalLauncherSessions"][0]["metrics"]["startupResidentIdle"]
        sample["perProcess"][0].pop("rssMedianMiB", None)
        sample["totalRendererTree"].pop("rssMedianMiB", None)
    elif mutation == "remove_active_workload_definition":
        sample = result["normalLauncherSessions"][0]["metrics"]["representativeActive"]
        sample["workload"] = {"interactionCount": 0, "inputRatePerSecond": 0}
        sample["validationActivity"]["definedProductWorkload"] = False
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


def _run_callback_retry_unit_fixture() -> dict[str, Any]:
    import fam003_renderer_backend_runtime_probe as runtime_probe

    class FakePage:
        def __init__(self) -> None:
            self.calls = 0

        def runJavaScript(self, script: str, callback) -> None:
            del script
            self.calls += 1
            if self.calls == 2:
                callback({"recovered": True})

    class FakeWebView:
        def __init__(self) -> None:
            self.fake_page = FakePage()

        def page(self) -> FakePage:
            return self.fake_page

    runtime_probe._JAVASCRIPT_RETRY_EVENTS.clear()
    view = FakeWebView()
    value = runtime_probe._javascript(view, "({})", timeout_s=0.02)
    events = list(runtime_probe._JAVASCRIPT_RETRY_EVENTS)
    runtime_probe._JAVASCRIPT_RETRY_EVENTS.clear()
    _assert(value == {"recovered": True}, f"callback retry returned wrong value: {value}")
    _assert(view.fake_page.calls == 2, f"callback retry call count was {view.fake_page.calls}")
    _assert(
        any(event.get("attempt") == 2 and event.get("recovered") is True for event in events),
        f"callback recovery event missing: {events}",
    )
    return {"status": "PASS", "callCount": view.fake_page.calls, "recoveredOnAttempt": 2, "events": events}


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


def _legacy_intrusive_main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--desktop-entrypoint-report", type=Path)
    parser.add_argument("--preserved-lifecycle-manifest", type=Path)
    parser.add_argument("--reuse-session-root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    negative_fixtures = _run_negative_fixtures()
    callback_retry_unit_fixture = _run_callback_retry_unit_fixture()
    if args.self_test:
        print("FAM-003 RENDERER BACKEND NEGATIVE FIXTURES: PASS")
        print(f"Cases: {len(negative_fixtures)} / {len(negative_fixtures)}")
        print("JavaScript callback retry path: PASS / recovered on attempt 2")
        return 0

    _assert(
        args.desktop_entrypoint_report is not None or args.preserved_lifecycle_manifest is not None,
        "--desktop-entrypoint-report or --preserved-lifecycle-manifest is required for final Option D proof",
    )
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

    if args.reuse_session_root is not None:
        reuse_root = args.reuse_session_root.resolve()
        sessions = []
        for index in range(1, args.runs + 1):
            source = reuse_root / f"session_{index:02d}" / "fam003_option_d_runtime_session.json"
            _assert(source.exists(), f"reused performance session is missing: {source}")
            session = json.loads(source.read_text(encoding="utf-8-sig"))
            session["manifestPath"] = str(source)
            sessions.append(session)
    else:
        sessions = [_launch_session(shortcut, output_root, head, index) for index in range(1, args.runs + 1)]
    for session in sessions:
        _assert(session.get("status") == "PASS", f"normal-launcher surface session failed: {session.get('failure')}")
        _assert(session.get("sourceHead") == head, "normal-launcher session HEAD provenance is stale")
        backend = session.get("effectiveBackend") or {}
        _assert(backend.get("effectiveFlags") == backend.get("childInheritedFlags") == EXPECTED_FLAG, "normal renderer child flags mismatch")
        for surface_id in AVAILABLE_PROOF_SURFACES:
            row = (session.get("surfaces") or {}).get(surface_id) or {}
            _assert(row.get("visualVerdict") == "PASS" and row.get("functionalVerdict") == "PASS" and row.get("evidence"), f"surface proof missing for {surface_id}")
        regression = session.get("materialRegression") or {}
        _assert(regression.get("detected") is None, "session made an unsupported binary regression claim")
        _assert(regression.get("disposition") == "USER_DECISION_REQUIRED", "session did not preserve the no-baseline decision gate")
        _assert(regression.get("requiredMetricsAdjudicated") is True, "session omitted required performance adjudication")

    lifecycle = (
        _preserved_lifecycle_proof(args.preserved_lifecycle_manifest.resolve(), output_root, head)
        if args.preserved_lifecycle_manifest is not None
        else _lifecycle_proof(args.desktop_entrypoint_report.resolve(), output_root)
    )
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
        f"Methodology: `{performance['methodologyVersion']}` / {PERFORMANCE_SETTLE_DURATION_MS} ms settle / {PERFORMANCE_SAMPLE_DURATION_MS} ms sustained sample / {PERFORMANCE_SAMPLE_INTERVAL_MS} ms raw interval.\n\n"
        "Disposition: `USER_DECISION_REQUIRED`. No repo-defined numeric threshold or safe equivalent baseline exists, so these measurements do not prove equivalence or no material regression.\n\n"
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
        "RB-JS-CALLBACK-001": "a ready WebEngine surface failed to return one JavaScript callback",
        "RB-HUD-RESTORE-001": "one tray-restored HUD frame contained a large partial-black WebEngine region",
        "RB-AI-RESTORE-001": "one restored AI Command Center frame contained a large partial-black WebEngine region",
        "RB-PERF-IDLE-002": "the prior settled-idle sample retained active on-demand surfaces and was not resident idle",
        "RB-PERF-CPU-003": "the prior aggregate CPU percentage lacked PID/role attribution and a defined denominator",
        "RB-PERF-TIMING-004": "the prior firstWebEngineRenderMs timer began after readiness and included DOM/capture work",
        "RB-PERF-ADJUDICATION-005": "the prior no-material-regression result ignored required CPU, memory, startup, opening, and resident-state metrics",
        "RB-PERF-VALIDATOR-006": "the prior validator accepted sub-second, contaminated, unattributed, non-comparable performance evidence",
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
    callback_sessions = [session.get("javascriptCallbackPolicy") or {} for session in sessions]
    manifest = _base_validation_manifest()
    manifest.update(
        {
            "schema": "fam003-option-d-renderer-backend-workstream-v2",
            "status": "USER_DECISION_REQUIRED",
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
            "materialRegression": {
                "detected": None,
                "ignored": False,
                "disposition": "USER_DECISION_REQUIRED",
                "requiredMetricsAdjudicated": True,
                "baselineComparable": False,
                "basis": "sustained absolute Option D measurements are current and reproducible; no safe equivalent baseline or governing threshold exists",
            },
            "lifecycle": lifecycle,
            "backendEvidenceCurrentness": "CURRENT_FINAL_BACKEND",
            "aggregateConsumption": {"optionCConsumesRendererBackendChild": True},
            "javascriptCallbackResilience": {
                "maxAttempts": 3,
                "exhausted": any(row.get("exhausted") is True for row in callback_sessions),
                "sessions": callback_sessions,
            },
            "javascriptCallbackRetryUnitFixture": callback_retry_unit_fixture,
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
        f"Status: `USER_DECISION_REQUIRED`\n\nSource HEAD: `{head}`\n\n"
        f"Effective flags: `{EXPECTED_FLAG}`\n\n"
        f"Policy: `{EXPECTED_POLICY}` (`{EXPECTED_CLASSIFICATION}`)\n\n"
        f"Normal-launcher runs: `{len(sessions)}`\n\n"
        f"Affected WebEngine inventory: `{len(inventory)} / {len(REQUIRED_WEBENGINE_SURFACES)}` rows\n\n"
        f"Directly proofed current routes: `{len(AVAILABLE_PROOF_SURFACES)} / {len(AVAILABLE_PROOF_SURFACES)}`\n\n"
        f"Negative fixtures: `{len(negative_fixtures)} / {len(negative_fixtures)}`\n\n"
        "Material regression: `UNRESOLVED - USER_DECISION_REQUIRED`\n\n"
        "Hardware-default comparison was not re-executed because the known teardown path is unsafe; no performance-equivalence or no-regression claim is made.\n\n"
        "This is Workstream proof only. It does not enter H1, formal Live Validation, or UTS, and it does not make Option D permanent architecture.\n",
        encoding="utf-8",
    )
    print("FAM-003 RENDERER BACKEND WORKSTREAM: USER_DECISION_REQUIRED")
    print(f"Proof Root: {output_root}")
    print(f"Manifest: {manifest_path}")
    print(f"Report: {report_path}")
    return 0


def main() -> int:
    """Route the active Workstream proof through the nonintrusive v3 adjudicator."""

    from dev.orin_fam003_option_d_nonintrusive_performance_validation import (
        main as nonintrusive_main,
    )

    return nonintrusive_main()


if __name__ == "__main__":
    raise SystemExit(main())
